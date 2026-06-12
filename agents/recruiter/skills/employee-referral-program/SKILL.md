<!--
Sources: https://erinapp.com/
         https://teamable.com/
         https://www.boon.co/
         https://www.greenhouse.io/blog/employee-referral-programs
2026 source-of-hire data: referrals = 40% of hires industry-wide, 4× retention vs cold sourcing,
$4K avg savings. Bonus tiers: $1-5K IC, $5-10K senior, $10-25K exec. Differential bonus structure
(URM referral bonus) defers to legal-counsel.
-->
# Employee Referral Program — SKILL

Set up and operate the employee referral program: ERIN / Teamable / Boon platform integration, bonus tier structure, 90-day retention payout cadence, gamified leaderboard, mobile-first submission UI, referral source attribution in ATS. Differential bonus structures (URM uplift) defer to `legal-counsel`.

## When to use

- Net-new program design — bonus tiers, payout rules, eligibility, anti-gaming controls.
- Existing program revival — measure conversion + tweak bonus + comms.
- Per-req referral push for hot reqs (Slack / email + leaderboard nudge).
- Quarterly: referral conversion review + bonus tier adjustment.
- Trigger phrases: "referral program", "referral bonus", "ERIN setup", "Teamable", "Boon", "employee referral leaderboard", "referral payout".

## Setup

```bash
# Platform (pick one — pricing typically per-employee/month)
export ERIN_API_KEY="xxx"                  # https://erinapp.com/api
export TEAMABLE_API_KEY="xxx"              # https://teamable.com/api
export BOON_API_KEY="xxx"                  # https://www.boon.co/

# ATS attribution
export GREENHOUSE_API_KEY="harvest_xxx"
export GH_USER_ID="123456"
export ASHBY_API_KEY="xxx"

# Comms
export SLACK_BOT_TOKEN="xoxb-xxx"          # slack-mcp
export GMAIL_OAUTH_TOKEN="<bearer>"

# Finance handoff (payout coordination)
export XERO_API_KEY="xxx"                  # xero-mcp; or QuickBooks / Workday Payroll
```

Auth model: ERIN / Teamable / Boon are paid SaaS; basic-auth-key pattern; webhooks fire to ATS + comms.

## Common recipes

### Recipe 1: Create ERIN bonus structure
```bash
curl -s -X POST -H "Authorization: Bearer $ERIN_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.erinapp.com/v1/bonus_tiers" \
  -d '{
    "tiers": [
      {"name": "IC", "amount_usd": 2500, "role_levels": ["junior", "mid", "senior_ic"]},
      {"name": "Senior IC + Manager", "amount_usd": 5000, "role_levels": ["staff_ic", "manager"]},
      {"name": "Senior Manager + Director", "amount_usd": 10000, "role_levels": ["senior_manager", "director"]},
      {"name": "VP + C-level", "amount_usd": 25000, "role_levels": ["vp", "c_level"]}
    ],
    "retention_split": {"on_hire_pct": 50, "at_90_days_pct": 50}
  }'
```

### Recipe 2: Submit referral (ERIN)
```bash
curl -s -X POST -H "Authorization: Bearer $ERIN_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.erinapp.com/v1/referrals" \
  -d '{
    "referrer_employee_email": "alice@acme.com",
    "candidate": {
      "first_name": "Bob",
      "last_name": "Smith",
      "email": "bob@example.com",
      "linkedin_url": "https://linkedin.com/in/bobsmith"
    },
    "job_id": "<ats_job_id>",
    "note": "Bob and I worked on payments at Stripe; backend depth + lead experience."
  }'
```

### Recipe 3: Sync referral to Greenhouse with source attribution
```bash
# Create candidate with referral source_id
curl -s -X POST -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -H "Content-Type: application/json" \
  "https://harvest.greenhouse.io/v1/candidates" \
  -d '{
    "first_name": "Bob", "last_name": "Smith",
    "email_addresses": [{"value": "bob@example.com", "type": "personal"}],
    "applications": [{"job_id": <job_id>, "source_id": <referral_source_id>}],
    "tags": ["referral"],
    "custom_fields": {"referred_by_employee_id": "alice@acme.com"}
  }'
```
Find `referral_source_id`: `GET /v1/sources` and pick the "Employee Referral" type.

### Recipe 4: Pull referral candidates (Greenhouse)
```bash
SOURCE_ID=$(curl -s -u "$GREENHOUSE_API_KEY:" "https://harvest.greenhouse.io/v1/sources" | jq '.[] | select(.name == "Employee Referral") | .id')
curl -s -u "$GREENHOUSE_API_KEY:" "https://harvest.greenhouse.io/v1/candidates?source_id=$SOURCE_ID&status=active" \
  | jq '.[] | {id, name: (.first_name + " " + .last_name), referrer: .custom_fields.referred_by_employee_id, status: .applications[0].status}'
```

### Recipe 5: Mark referral hired + trigger payout (ERIN)
```bash
curl -s -X PATCH -H "Authorization: Bearer $ERIN_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.erinapp.com/v1/referrals/<referral_id>" \
  -d '{"status": "hired", "hired_at": "2026-06-15", "payout_on_hire_triggered": true}'
```

### Recipe 6: 90-day retention payout check (cron)
```python
import requests, os, datetime
# Pull hires where 90 days has passed
hires = requests.get(
  "https://api.erinapp.com/v1/referrals?status=hired",
  headers={"Authorization": f"Bearer {os.environ['ERIN_API_KEY']}"}
).json()
cutoff = datetime.date.today() - datetime.timedelta(days=90)
due = [h for h in hires if datetime.date.fromisoformat(h["hired_at"]) <= cutoff and not h.get("90day_payout_triggered")]
for h in due:
  # Verify employee still active via HRIS
  # Then trigger payout
  requests.patch(f"https://api.erinapp.com/v1/referrals/{h['id']}",
                 headers={"Authorization": f"Bearer {os.environ['ERIN_API_KEY']}"},
                 json={"90day_payout_triggered": True})
  # Hand off to finance via xero-mcp; payroll bonus line item
```

### Recipe 7: Open req push to all employees (Slack broadcast)
```bash
# slack-mcp: post to #referrals channel + DM employees with matching profile
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  "https://slack.com/api/chat.postMessage" \
  -d '{
    "channel": "#referrals",
    "text": "Hot req: Senior Backend Engineer (Python/Go). Bonus tier 2 = $5K. Submit a referral: https://acme.erinapp.com/jobs/<id>"
  }'
```

### Recipe 8: Gamified leaderboard pull (ERIN)
```bash
curl -s -H "Authorization: Bearer $ERIN_API_KEY" \
  "https://api.erinapp.com/v1/leaderboard?period=quarter" \
  | jq '.entries[] | {employee: .employee_name, submissions: .referrals_submitted, hires: .referrals_hired, points: .points}'
# Post top 10 to slack-mcp weekly to drive engagement.
```

### Recipe 9: Teamable smart-suggestions integration
```bash
# Teamable scans employee LinkedIn networks → surfaces referral candidates per req.
curl -s -X POST -H "Authorization: Bearer $TEAMABLE_API_KEY" \
  "https://api.teamable.com/v1/jobs/<job_id>/suggestions" \
  -d '{"limit": 20, "min_connection_score": 0.7}'
# Output: ranked list of {candidate_linkedin, employee_referrer, connection_strength, role_match}
```

### Recipe 10: Boon AI-suggested referrals
```bash
curl -s -H "Authorization: Bearer $BOON_API_KEY" \
  "https://api.boon.co/v1/jobs/<job_id>/suggested_referrals" \
  | jq '.suggestions[] | {employee, recommended_candidates}'
```

### Recipe 11: Referral conversion dashboard
```python
import requests, os, pandas as pd
# Pull referrals submitted vs referrals hired by quarter
data = requests.get(
  "https://api.erinapp.com/v1/analytics/conversion?since=2026-01-01",
  headers={"Authorization": f"Bearer {os.environ['ERIN_API_KEY']}"}
).json()
df = pd.DataFrame(data["referrals"])
funnel = df.groupby("quarter").agg(
  submitted=("id", "count"),
  to_screen=("status", lambda s: (s != "rejected_pre_screen").sum()),
  hired=("status", lambda s: (s == "hired").sum())
)
funnel["screen_rate"] = funnel["to_screen"] / funnel["submitted"]
funnel["hire_rate"] = funnel["hired"] / funnel["submitted"]
print(funnel)
# Benchmark: 50-70% screen rate, 8-15% hire rate
```

### Recipe 12: Differential bonus structure (carefully — defer to legal)
```text
# Some companies offer +$500-$2000 bonus uplift for URM referrals.
# Legal posture: structure as voluntary opt-in DEI bonus tied to advancing diversity goals,
# NOT a quota. Title VII risk if structured as race-based payout.
# Defer wording + structure to legal-counsel before launch.
# Alternate structure: same bonus, but priority recruiter outreach + faster decision
# for URM-channel referrals (process-time advantage, not bonus differential).
```

## Examples

### Example 1: New program launch (Series-A startup, 50 employees)
**Goal:** Stand up ERIN + tiered bonus + Slack comms within 2 weeks.
**Steps:**
1. Recipe 1: configure tiers ($2K / $5K / $10K / $25K).
2. Recipe 7: launch Slack announcement + manager kickoff.
3. Recipe 3: ATS source-attribution set up.
4. Recipe 6: cron for 90-day retention payouts (xero-mcp handoff to finance).
5. Recipe 11: weekly conversion dashboard.

**Result:** Program live in 2 weeks; first referral hire by month 1; 30% source-of-hire by quarter 2.

### Example 2: Hot-req referral push
**Goal:** Director of Engineering open 30 days; team needs senior referrals.
**Steps:**
1. Recipe 9 + Recipe 10: AI-suggested referrals → top 20 list to engineering leadership.
2. Recipe 7: targeted Slack DM to managers + senior ICs with relevant network.
3. Track via Recipe 11 over 14 days.

**Result:** 12 referrals submitted; 2 advanced to onsite; 1 hire.

### Example 3: Q2 referral conversion review
**Goal:** Why is referral hire rate dropping?
**Steps:**
1. Recipe 11 pulls Q1 vs Q2 funnel.
2. Identify drop point (e.g., screen → onsite conversion dropped 15%).
3. Recipe 11 cross-cut by role family — find that senior referrals dropped (anecdote: hiring panel too tough for senior referrals).
4. Action: recalibrate senior-role panel + adjust bonus to encourage senior referrals.

**Result:** Diagnose + fix; recover hire rate Q3.

## Edge cases / gotchas

- **Source attribution drift.** Without ERIN/Teamable, candidate self-reports "referred by Alice" but recruiter forgets to tag in ATS. 30-40% of referrals lose attribution. ERIN/Teamable + ATS source webhook closes this.
- **Self-referral fraud.** Employee adds friend who applied independently. Anti-fraud: candidate must register via the referral link, not direct apply. Audit quarterly.
- **Payout dispute.** Two employees claim same referral. Anti-dispute: first-link-clicked wins (timestamped). Document in program FAQ.
- **90-day attrition.** If hire leaves before 90 days, half of bonus claws back. State labor law varies on clawback (CA has strict rules). Defer wording to `legal-counsel`.
- **Bonus tax treatment.** Referral bonuses are taxable wages (IRS, BIK treatment in UK). Communicate "before-tax" amount + coordinate with payroll.
- **Differential bonus = Title VII risk.** "Extra $1K for URM referral" can be challenged. Structure as opt-in diversity bonus or use process-time advantage (faster decision) instead. **Defer to `legal-counsel`**.
- **Anti-cap-table referral.** Some startups offer equity-grant referral bonus (instead of cash). Tax + securities-law implications; defer to legal.
- **Referrer must be active employee.** If employee leaves before 90-day mark, half bonus typically forfeited (per program rules). Document upfront.
- **Hot-req fatigue.** Daily Slack pings tank engagement. Weekly digest + targeted DMs better than broadcast.
- **Leaderboard gaming.** Quantity-based leaderboards encourage low-quality submissions. Weight by hire-conversion not just submission count.
- **External recruiter referrals.** Should NOT count for employee bonus. Filter ERIN/Teamable to employee-only domains.
- **Defer to `legal-counsel`** for: clawback structure, differential bonus structure, equity-grant referral bonus, tax treatment per geo.
- **Defer to `operations-agent`** for: 90-day retention data + payroll bonus line-item flow.

## Sources

- [ERIN](https://erinapp.com/) + [ERIN API](https://erinapp.com/api)
- [Teamable](https://teamable.com/)
- [Boon](https://www.boon.co/)
- [Greenhouse — Employee Referral Programs](https://www.greenhouse.io/blog/employee-referral-programs)
- [SHRM — Referral Bonus best practices](https://www.shrm.org/topics-tools/news/talent-acquisition/employee-referral-bonus)
- [Greenhouse Sources API](https://developers.greenhouse.io/harvest.html#sources)
- [Title VII — differential compensation guidance](https://www.eeoc.gov/laws/statutes/titlevii.cfm)
