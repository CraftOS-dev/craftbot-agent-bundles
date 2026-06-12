<!--
Sources: https://gloat.com/
         https://www.eightfold.ai/talent-management/career-hub/
         https://www.cornerstoneondemand.com/products/talent-mobility/
2026 internal mobility data: Gartner — 40% of employees would leave for internal promotion at
competitor; external hire cost = 1.5-2× internal. 5-7 biz days first-look for internal candidates
before external posting. Workforce planning + career pathing defer to operations-agent + ceo-agent.
-->
# Internal Mobility Program — SKILL

Run the internal-mobility operations: internal job board, skill-based matching (Gloat / Eightfold / Cornerstone), 5-7 biz day first-look for internal candidates, manager-mediated transition (90-day notice + project handoff plan), L&D credit for upskilling. Workforce planning + career pathing strategy defers to `operations-agent` + `ceo-agent`.

## When to use

- New req opened: enable internal first-look before external posting.
- Internal candidate interested in role outside their team.
- Quarterly: review internal-mobility metrics + skill-gap analysis.
- Trigger phrases: "internal mobility", "internal job board", "Gloat", "Eightfold Career Hub", "internal posting", "internal candidate", "career pathing", "skills matching".

## Setup

```bash
# ATS internal board
export GREENHOUSE_API_KEY="harvest_xxx"
export GH_USER_ID="123456"
export ASHBY_API_KEY="xxx"

# Skill-matching platforms (paid)
export GLOAT_API_KEY="xxx"                  # https://gloat.com/
export EIGHTFOLD_API_KEY="xxx"              # https://eightfold.ai/talent-management/career-hub/
export CORNERSTONE_API_KEY="xxx"

# Comms
export SLACK_BOT_TOKEN="xoxb-xxx"
export GMAIL_OAUTH_TOKEN="<bearer>"

# HRIS for tenure + role data
export WORKDAY_API_KEY="xxx"                # or BambooHR / Rippling / Sapling
```

Auth model: ATS basic-auth + internal-platform-specific tokens. HRIS as system-of-record for employee + role + manager + tenure.

## Common recipes

### Recipe 1: Post req to internal job board first (Greenhouse)
```bash
# Greenhouse: jobs can be configured "Internal Only" via job_post or custom_field
curl -s -X PATCH -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -H "Content-Type: application/json" \
  "https://harvest.greenhouse.io/v1/jobs/<job_id>" \
  -d '{"custom_fields": {"posting_visibility": "internal"}}'
```
Set 5-7 biz day internal-first window before flipping to external.

### Recipe 2: Pull internal job board (employees only)
```bash
# Greenhouse separate board for internal posts:
curl -s "https://boards-api.greenhouse.io/v1/boards/$GREENHOUSE_INTERNAL_BOARD_TOKEN/jobs" \
  | jq '.jobs[] | {id, title, department: .departments[].name}'
# Hosted behind SSO; employees see via /internal-careers
```

### Recipe 3: Enable Ashby Internal Job Board
```bash
curl -s -X POST -u "$ASHBY_API_KEY:" \
  -H "Content-Type: application/json" \
  "https://api.ashbyhq.com/job.update" \
  -d '{"jobId": "<id>", "internalOnly": true, "internalPostingWindowDays": 5}'
```

### Recipe 4: Notify employees with matching skills (Eightfold Career Hub)
```bash
curl -s -X POST -H "Authorization: Bearer $EIGHTFOLD_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.eightfold.ai/v3/career_hub/notifications" \
  -d '{
    "job_id": "<id>",
    "skill_match_threshold": 0.7,
    "notify_via": ["email", "in_app"],
    "candidate_pool": "all_employees"
  }'
```

### Recipe 5: Gloat — surface candidates per opening
```bash
curl -s -H "Authorization: Bearer $GLOAT_API_KEY" \
  "https://api.gloat.com/v1/marketplace/jobs/<job_id>/candidates" \
  | jq '.candidates[] | {employee_id, name, skill_match, current_role, tenure_years}'
```

### Recipe 6: Internal candidate intake (different from external)
```text
Internal candidate handling differs:
1. Application is INTERNAL — manager notified within 48h (transparency policy)
2. No standard cold screen — internal scorecard validates skill + cultural-add for new team
3. Compressed loop (2-3 hr total) — internal team has employee's reputation data
4. Comp framing: internal-equity adjustment (don't underpay internal mover)
5. Transition plan: 90-day notice typical for senior IC+; project handoff + ramp budget
6. L&D credit: company-funded course budget if employee needs skill bridge
```

### Recipe 7: Manager-mediated transition plan
```markdown
# Internal Mobility Transition Plan — {employee_name}

## Current role
- Manager: {current_mgr}
- End date: {date}

## New role
- Manager: {new_mgr}
- Start date: {date}

## Transition cadence
- T-90 days: announcement, project handoff plan started
- T-60 days: replacement plan + cross-training underway
- T-30 days: project ownership transferred
- T-7 days: knowledge transfer + role wrap
- Day 0: ramp in new role; 30-60-90 plan with new manager

## Compensation
- Base: {old} → {new}
- Equity refresh: {if applicable}
- Sign-on (rare): {if needed for retention pressure}

## L&D commitment
- Skill bridge: {course / coaching budget}

## Backfill plan
- Internal candidate: {if available, lower-level promo OR cross-team move}
- External hire: {timeline to backfill}

## Sign-off
- Current manager: ___
- New manager: ___
- HRBP: ___
- Employee: ___
```

### Recipe 8: Internal-first window with auto-flip-to-external (cron)
```python
import requests, os, datetime
JOBS = requests.get(
  "https://harvest.greenhouse.io/v1/jobs?status=open",
  auth=(os.environ["GREENHOUSE_API_KEY"], "")
).json()
for j in JOBS:
  if j.get("custom_fields", {}).get("posting_visibility") == "internal":
    opened = datetime.datetime.fromisoformat(j["opened_at"].rstrip("Z"))
    if (datetime.datetime.utcnow() - opened).days >= 5:
      # No internal candidate advanced → flip to external
      requests.patch(
        f"https://harvest.greenhouse.io/v1/jobs/{j['id']}",
        auth=(os.environ["GREENHOUSE_API_KEY"], ""),
        headers={"On-Behalf-Of": os.environ["GH_USER_ID"], "Content-Type": "application/json"},
        json={"custom_fields": {"posting_visibility": "external"}}
      )
```

### Recipe 9: Skill-gap analysis per req (Eightfold)
```bash
curl -s -H "Authorization: Bearer $EIGHTFOLD_API_KEY" \
  "https://api.eightfold.ai/v3/jobs/<job_id>/skill_gap" \
  | jq '{required_skills, candidate_skill_levels, gap_per_skill, upskill_paths}'
# Use for L&D budget allocation + manager coaching plan.
```

### Recipe 10: Career-path recommendations for an employee (Gloat)
```bash
curl -s -H "Authorization: Bearer $GLOAT_API_KEY" \
  "https://api.gloat.com/v1/employees/<id>/career_paths" \
  | jq '.recommended_paths[] | {target_role, gap_skills, est_time_to_ready_months}'
# Share with employee + manager in career conversation.
```

### Recipe 11: Internal mobility metrics dashboard
```python
import pandas as pd
# Pull hires by source: internal vs external
hires = pd.read_csv("hires_2026.csv")
internal_pct = (hires["source"] == "internal").mean()
print(f"Internal mobility rate: {internal_pct:.1%}  (benchmark: 30-40% for healthy mobility culture)")

# Time-to-fill compare
ttf = hires.groupby("source")["days_to_fill"].mean()
print(ttf)  # Expect internal: ~14-21 days; external: ~30-45 days
```

### Recipe 12: Internal candidate decline (handle carefully)
```text
Internal decline = career risk for employee. Best practice:
1. Manager + HRBP + recruiter joint debrief WITH employee (not without)
2. Specific feedback: "you weren't selected because X" (not "we went a different direction")
3. Concrete next steps: development plan, mentorship, future-role pathway
4. Retention check at 30 + 90 days post-decline (renege/external-search risk)

Template wording in role.md "Decline template library" — internal decline variant; HRBP-approved.
```

## Examples

### Example 1: New Senior Backend req with internal first-look
**Goal:** Surface internal candidates before external posting.
**Steps:**
1. Recipe 1: Greenhouse set "Internal Only" + 5-day window.
2. Recipe 4: Eightfold notifies engineering employees with skill match >0.7.
3. Recipe 5: Gloat surfaces marketplace candidates.
4. 5 internal expressions of interest → Recipe 6 compressed intake.
5. 2 strong internal candidates → 1 hire.
6. If no hire: Recipe 8 auto-flips to external.

**Result:** Internal hire chosen; external posting saved; retention signal sent.

### Example 2: Engineer-to-PM career pivot (cross-functional)
**Goal:** Senior engineer wants to move into PM role.
**Steps:**
1. Recipe 10: Gloat career-path → engineer-to-PM identified as 6-12 mo readiness.
2. Recipe 7: transition plan with current eng manager + new PM manager + HRBP.
3. L&D budget: PM bootcamp + APM mentorship.
4. 6 months later: APM role opens; internal candidate slot at top of list.
5. Recipe 6: compressed loop; hire.

**Result:** Talent retained + grown; org learned to support cross-functional moves.

### Example 3: Quarterly mobility metrics
**Goal:** Are we hitting 30%+ internal mobility?
**Steps:**
1. Recipe 11 pulls Q2 data: 24% internal hires (below 30% target).
2. Drill-in: which functions? Eng @ 35% (healthy), Sales @ 8% (low).
3. Hypothesis: Sales managers external-search-default. Action: structured internal-first review at Sales req intake.

**Result:** Q3 sales internal rate lifts to 18%; target trending right way.

## Edge cases / gotchas

- **Manager retention vs business need.** Current manager may block transfer to "keep their headcount." HRBP arbitrates; explicit 90-day notice removes ambiguity.
- **Comp inversion.** Internal candidate at $130K → moving to role with external offer at $165K creates comp gap. Solve by repricing the internal hire to band, not below external.
- **Cross-team poaching dynamics.** "Aren't you stealing from another team?" Defuse: company hires = company wins. Don't compete internally with external recruiting.
- **Compressed loop quality.** Tempting to skip everything because "we know them." Don't — internal hires need cultural-add validation in new team. Run 2-3 hour compressed loop.
- **Comp band: how much for internal mover?** Pay at FTE band, not at promo step. Internal candidate often gets 10-20% bump (vs 3-5% annual raise); below external would be insulting.
- **L&D credit budget.** Often unfunded; budget conversation between HRBP + finance early. Don't promise course budget without approval.
- **Decline communication.** Internal decline mishandled → external job search by employee within 30 days. Recipe 12 is critical.
- **Backfill timing.** Internal mover creates a hole; backfill plan must be ready or current team destabilized.
- **Gloat / Eightfold = paid + skill-graph-dependent.** Skill data quality drives match quality; HRIS-Gloat sync must be current.
- **Promo-vs-move confusion.** A "move" with title bump is a promo (different policy + approval). Clarify upfront.
- **Visa employees.** International employee internal-mobility may trigger visa re-classification (especially L-1, H-1B). Defer to `legal-counsel`.
- **Equity grants.** Internal mover at new level may merit equity refresh; coordinate with comp.
- **Defer to `operations-agent`** for: HRIS role-change execution, payroll adjustment, benefit eligibility re-check.
- **Defer to `ceo-agent`** for: org-design decisions, headcount plan changes triggered by internal mobility.
- **Defer to `legal-counsel`** for: visa-impacted internal moves, non-compete re-evaluation.

## Sources

- [Gloat](https://gloat.com/)
- [Eightfold Career Hub](https://www.eightfold.ai/talent-management/career-hub/)
- [Cornerstone Talent Mobility](https://www.cornerstoneondemand.com/products/talent-mobility/)
- [Gartner — Internal Mobility Research](https://www.gartner.com/en/human-resources/research)
- [SHRM — Internal Mobility Programs](https://www.shrm.org/topics-tools/news/talent-acquisition/internal-mobility-best-practices)
- [Greenhouse Internal Hiring](https://www.greenhouse.io/blog/internal-mobility)
- [Ashby Internal Job Board](https://www.ashbyhq.com/learn/articles/internal-mobility)
- [LinkedIn — Workplace Learning 2024 (internal mobility data)](https://learning.linkedin.com/resources/workplace-learning-report)
