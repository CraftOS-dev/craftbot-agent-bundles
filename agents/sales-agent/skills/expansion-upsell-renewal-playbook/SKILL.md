<!--
Source: https://www.gainsight.com/blog/account-expansion-strategy/ + https://www.gainsight.com/blog/renewal-management/
Customer expansion + upsell + renewal motion (June 2026 SOTA).
-->
# Expansion + Upsell + Renewal Playbook — SKILL

Post-sale revenue motion: track product usage signals (Pocus / Koala / PostHog), identify expansion triggers (usage > seat threshold, > 2 modules, NPS > 8, champion promotion), run exec QBR + multi-team rollout proposals; for renewals, open pipeline 120 days pre-renewal with health-score-driven save motion for at-risk accounts. Pricing strategy: anchor on closed-won comparables; concession ladder with give-get pairs.

## When to use

- **Existing customer crossed a usage threshold** (PQL: 5+ users / 2+ modules / 30+ sessions/wk).
- **Customer renewal within 120 days** — open renewal pipeline + health-score.
- **NPS > 8 from a key stakeholder** — expansion trigger.
- **Champion promoted internally** — expansion through their new scope.
- **Customer hiring in adjacent department** — new buying center.
- **Trigger phrases**: "expand <customer>", "upsell opportunity", "renewal coming up", "QBR for <account>", "save motion", "at-risk renewal", "pricing for expansion".

Do NOT use this skill for: **new-logo acquisition** (use `outreach-salesloft-sequences`); **post-sale support issues** (handoff to `customer-support-agent`); **enterprise NRR strategy** (this is the ops layer, not the strategy layer).

## Setup

```bash
export MATON_API_KEY="<key>"
export POSTHOG_API_KEY="<key>"   # for product-usage signal
export GAINSIGHT_API_KEY="<key>"  # if using Gainsight CSP
export NOTION_TOKEN="<key>"       # health-score dashboards
```

CRM setup (one-time):
- `renewal_date` (date, computed from contract_start + contract_length)
- `health_score` (number 0-100)
- `nps_latest` (number)
- `usage_score_30d` (number)
- `expansion_potential` (select: low / medium / high)
- `renewal_risk` (select: healthy / at_risk / critical)

## Common recipes

### Recipe 1: Expansion trigger conditions (any one fires)

```yaml
trigger_usage_threshold:
  rule: "active_users >= 5 OR sessions_per_week >= 30 in last 30d"
  signal_source: posthog / pocus / koala
  action: "expansion play kickoff"

trigger_module_adoption:
  rule: "uses_module_count >= 2 AND uses_premium_module = true"
  action: "exec QBR + multi-team rollout proposal"

trigger_nps_high:
  rule: "latest_nps >= 8 from stakeholder with title >= manager"
  action: "expansion conversation + reference candidate"

trigger_champion_promoted:
  rule: "champion title-change detected via LinkedIn (Apollo job-change webhook)"
  action: "congrats + 'now with broader scope, here's how we can support'"

trigger_adjacent_hiring:
  rule: "customer posting >= 3 roles in adjacent department"
  action: "ICP-fit check for that department → land-and-expand pitch"

trigger_renewal_proximity:
  rule: "renewal_date - today() < 120 days"
  action: "renewal pipeline opens; health-score check"
```

### Recipe 2: Product usage pull (PostHog)

```bash
# Daily-active users + sessions over last 30 days per customer org
curl -X POST "https://gateway.maton.ai/posthog/api/projects/<project-id>/insights/trend/" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "events":[{"id":"product_session","type":"events"}],
    "breakdown":"organization_id",
    "interval":"day",
    "date_from":"-30d"
  }'
```

Wire breakdown to your customer ID (set as `organization_id` in PostHog event identify).

### Recipe 3: Compute health score (composite)

```python
def health_score(customer):
    """0-100; > 75 healthy, 50-75 at-risk, < 50 critical."""
    score = 0
    # Usage (40 points)
    usage_trend = usage_trend_90d(customer["id"])  # "up" / "flat" / "down"
    if usage_trend == "up": score += 30
    elif usage_trend == "flat": score += 20
    else: score += 5
    if customer.get("active_users_30d", 0) >= customer.get("contracted_seats", 1) * 0.7:
        score += 10
    # NPS (20)
    if customer.get("latest_nps", 0) >= 9: score += 20
    elif customer.get("latest_nps", 0) >= 7: score += 12
    elif customer.get("latest_nps", 0) >= 5: score += 5
    # Support (15)
    p1_tickets = support_tickets_p1_count(customer["id"], days=90)
    if p1_tickets == 0: score += 15
    elif p1_tickets <= 2: score += 8
    # Champion (15)
    if customer.get("champion_status") == "engaged": score += 15
    elif customer.get("champion_status") == "quiet": score += 5
    # Strategic (10)
    if customer.get("logo_strategic"): score += 10
    return min(score, 100)
```

### Recipe 4: Categorize renewal risk

```python
def categorize_renewal(customer):
    h = health_score(customer)
    if h >= 75: return "healthy"
    if h >= 50: return "at_risk"
    return "critical"
```

### Recipe 5: Healthy renewal motion (auto-renew)

```yaml
day_minus_120:
  - Send renewal-confirmation email
  - "We're approaching your renewal on [date]. Pricing locked at [current rate]. Any changes needed?"
day_minus_90:
  - QBR scheduled (light, 30 min) — usage report + roadmap alignment
  - Pricing locked confirmation
day_minus_60:
  - Send pre-signed renewal order form via PandaDoc
day_minus_45:
  - Follow-up if unsigned
day_minus_30:
  - Manager escalation if still unsigned
day_minus_14:
  - Counter-sign + acknowledge confirmation
```

For healthy accounts, ALSO try for expansion at renewal — 50% of NRR > 110% accounts upsell at renewal.

### Recipe 6: At-risk / critical renewal — save motion

```yaml
day_minus_120:
  - Health-score drop alert fires
  - Root-cause diagnosis: which factor (usage / NPS / champion / support)?
  - Schedule exec QBR within 14 days
day_minus_90:
  - Exec QBR: their VP/exec + our VP/exec
  - "Honest read" conversation — surface concern, propose success plan
day_minus_60:
  - Success plan in motion (specific actions: training / re-onboarding / new modules)
  - Coordinate with customer-support-agent for ticket resolution
  - Consider pricing concession if necessary (10-15% off in exchange for 2-year)
day_minus_45:
  - Re-check health-score; if not improved → escalate to leadership
day_minus_30:
  - Decision point: save or accept churn
  - If save = pricing concession + multi-year + success plan
  - If churn = clean exit, post-mortem (win-loss-analysis-structured), retention insights logged
```

### Recipe 7: Expansion play kickoff (when trigger fires)

```yaml
step_1_usage_report:
  - "Past 90 days activity per user, value realized vs baseline"
  - Generate via posthog-mcp + render to pdf / pptx
step_2_exec_qbr:
  - "Schedule 60-min exec QBR"
  - Attendees: customer EB + champion + 1-2 of our exec
  - Agenda: usage review (15) + roadmap (15) + expansion options (20) + ask (10)
step_3_multi_team_rollout_proposal:
  - "Identify adjacent teams that would benefit"
  - Apollo: pull all stakeholders in adjacent function (use account-research-deep recipes)
  - Proposal: additional seats + modules + use cases
step_4_pricing_anchor:
  - "Anchor on % discount off list, NOT % off current price"
  - Closed-won expansion comps from CRM (Recipe 9)
step_5_mutual_action_plan:
  - "Same MAP template as new deals — committed dates + signed by champion"
step_6_close:
  - "PandaDoc proposal with line-item expansion + multi-year option"
```

### Recipe 8: Champion-promoted play (LinkedIn job-change signal)

```python
# When apollo-clay-lead-enrichment Recipe 8 fires for an existing-customer contact tagged "champion"
def champion_promoted_play(payload):
    person = payload["person"]
    new_title = payload["person"]["title"]
    new_org = payload["new_organization"]["name"]
    old_title = payload["old_person"]["title"]

    if new_org == person["original_company"]:
        # Internal promotion at our existing customer
        send_congrats_email({
            "subject": f"Congrats on the new role, {person['first_name']}!",
            "body": f"""Saw the news — really happy for you. {old_title} → {new_title} is a big step.

With your expanded scope, would love to talk about how we can support your broader org. A few teams that might benefit: [adjacent]. Open to a quick chat?""",
            "to": person["email"],
        })
        # Create expansion opportunity in CRM
        create_expansion_opp(person, new_title)
```

### Recipe 9: Pricing for expansion (closed-won comparables)

```sql
-- For expansion deal pricing — find similar-sized customer expansion comps
SELECT
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY expansion_amount) AS p25,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY expansion_amount) AS p50,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY expansion_amount) AS p75,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY discount_pct) AS discount_p25,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY discount_pct) AS discount_p50,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY discount_pct) AS discount_p75,
    AVG(contract_length_years) AS avg_contract_yrs,
    COUNT(*) AS sample_size
FROM expansion_deals
WHERE
    customer_size BETWEEN 100 AND 500
    AND vertical = 'SaaS'
    AND closed_won_date > NOW() - INTERVAL '12 months';
```

Anchor proposal at the 75th-percentile of comparables; give down to median; floor at 25th-percentile (per role.md pricing strategy).

### Recipe 10: Concession ladder (give-get pairs)

```yaml
# Same as role.md — applies to expansion + renewal price discussion
ask_10pct_discount:
  give: "multi-year (3-yr) commitment"
  get: "cash up-front"

ask_15pct_discount:
  give: "reference call (1 hour with prospect, ours)"
  get: "case study rights (named or anonymized)"

ask_20pct_discount:
  give: "logo on website + co-marketing webinar"
  get: "quarterly exec QBR with their exec"

ask_over_20pct:
  give: "escalate to finance-controller agent"
  get: "—"

never_discount_without_trade: "Every concession has a get; free concessions train buyer to keep asking"
```

### Recipe 11: QBR template (skeleton)

```markdown
# QBR — [Customer] · [Date]
## Attendees — customer + our AE/CSM/exec
## Usage review (15m) — active users / contracted, most-used features, value realized
## Roadmap alignment (15m) — what we ship next 90d, what they solve next 90d, overlaps
## Open issues (10m) — P1 tickets resolved + outstanding with commit dates
## Expansion (15m, healthy accounts only) — adjacent teams, pricing/contract changes
## Next steps — customer commits + we commit + next QBR date
```

### Recipe 12: Renewal-risk dashboard (Notion + Slack)

```python
import datetime
RENEWAL_WINDOW = 120  # days

renewing_soon = pull_customers_renewing_within(RENEWAL_WINDOW)
for c in renewing_soon:
    c["health"] = health_score(c)
    c["risk"] = categorize_renewal(c)

# Render Notion table
table = []
for c in sorted(renewing_soon, key=lambda x: x["renewal_date"]):
    table.append({
        "Customer": c["name"],
        "Renewal date": c["renewal_date"],
        "Days to renewal": (datetime.date.fromisoformat(c["renewal_date"]) - datetime.date.today()).days,
        "ACV": c["acv"],
        "Health": c["health"],
        "Risk": c["risk"],
        "Owner": c["csm_or_ae"],
    })

# At-risk + Critical → Slack alert
at_risk = [c for c in renewing_soon if c["risk"] in ("at_risk","critical")]
if at_risk:
    slack_alert("#cs-leadership", f"{len(at_risk)} renewals at risk — {', '.join(c['name'] for c in at_risk[:5])}")
```

## Examples

### Example 1: Champion-promoted expansion

**Goal:** Customer champion promoted Director → VP. Trigger expansion outreach.

**Steps:** Apollo `person_job_changed` webhook fires → CRM tag flags this is an existing-customer champion → Recipe 8 sends congrats + soft expansion ask → on reply, book exec QBR with our exec sponsor → use `account-research-deep` to map their now-broader org → render expansion proposal.

**Result:** Champion promotion turns into a $50-200K expansion conversation within 30 days.

### Example 2: At-risk renewal — save motion

**Goal:** $80K customer health-score 45 (critical); renewal in 90 days.

**Steps:** Daily dashboard (Recipe 12) flags the drop → diagnose (usage -40%, champion silent, 3 P1 unresolved) → Recipe 6 schedules exec QBR within 7 days + coordinate with `customer-support-agent` for P1s → QBR (Recipe 11) builds success plan → decision: 10% concession + 2yr renewal + onboarding co-investment → PandaDoc the contract.

**Result:** Account saved, NRR preserved, structured post-save plan to prevent recurrence.

### Example 3: Healthy renewal with expansion attempt

**Goal:** $120K customer, health-score 88, renewal in 60 days; try for $40K expansion.

**Steps:** Recipe 5 auto-renew motion kicked off at day-120 → QBR reveals customer's marketing team is hiring (adjacent buying center) → `account-research-deep` pulls marketing VP → propose multi-team module add-on with Recipe 9 p75 anchor → bundle renewal + expansion into single PandaDoc with 5% multi-year discount.

**Result:** Renewal + $40K expansion in one deal; NRR > 130% for that account.

## Edge cases / gotchas

- **Don't pitch expansion in QBR before earning the right.** First 30 min is *their* outcomes; only last 15 min introduces expansion.
- **Champion-promoted ≠ company-changed.** Internal promotion = expand. External move = champion-mover (find new champion at same customer + reach champion at new company).
- **Usage trend > absolute usage.** 100% seat utilization but declining is more at-risk than 50% and growing.
- **Pricing concessions cascade.** A 15% discount at renewal trains the next renewal to expect 15%. Document why a concession was given to prevent re-granting.
- **Multi-year terms signal**: buyers ask for shorter terms when uncertain. Short-term + discount = at-risk despite a green health-score.
- **Health-score gaming**: AE/CSM marks accounts "healthy" to avoid scrutiny. Manager-spot-check 5 accounts/quarter for honest scoring.
- **"Strategic" logo doesn't override health.** A bad-fit "strategic" customer churning is honest churn.
- **Renewal date drift**: contracts auto-renew if you miss the cancellation window. For at-risk accounts, opening renewal proactively at day-120 forces a real conversation.
- **Expansion forecast ≠ new-business forecast.** Track separately; inflating expansion coverage to hit team number is common and dangerous.
- **Champion departure** is a renewal risk 1-2 quarters before date. New champion must be onboarded BEFORE the renewal cycle.
- **Pricing transparency**: anchor any price increase at day-120, not day-30. Surprise price increases destroy trust.

## Sources

- Account expansion strategy (Gainsight): https://www.gainsight.com/blog/account-expansion-strategy/
- Renewal management playbook (Gainsight): https://www.gainsight.com/blog/renewal-management/
- "Net Revenue Retention benchmark" (OpenView): https://openviewpartners.com/blog/net-revenue-retention/
- QBR template + facilitation (Pavilion): https://www.joinpavilion.com/blog/qbr-template
- Pricing strategy in expansion (Price Intelligently): https://www.priceintelligently.com/blog/expansion-pricing
- 2026 NRR > 120% playbook (ChartMogul): https://chartmogul.com/blog/net-revenue-retention-2026/
- Customer health scoring (Vitally): https://www.vitally.io/post/customer-health-score
- Champion-mover playbook (Gong, 2024): https://www.gong.io/blog/champion-tracker/
