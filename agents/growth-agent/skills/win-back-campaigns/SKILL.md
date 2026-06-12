<!--
Source: Customer.io campaigns + Klaviyo win-back flows + lifelines at-risk handoff
-->
# Win-Back Campaigns — Dormant User Reactivation SKILL

> Design and ship win-back sequences (timing, incentive, exit conditions) for dormant or at-risk users. Customer.io for B2B logic-heavy; Klaviyo for e-com. Pairs with churn-prediction-modeling for at-risk handoff.

## When to use

Trigger phrases:
- "Reactivate dormant users"
- "Win back lapsed customers"
- "Send a 'we miss you' email"
- "Dormant 30/60/90 day cohort outreach"
- "Reactivation sequence"

Pair: `churn-prediction-modeling` (at-risk identification), `behavioral-cohort-design` (audience), `in-app-messaging-intercom-drift-pendo` (in-app touch), `expansion-revenue-nrr-optimization` (post-reactivation expansion).

## Setup

```bash
export CUSTOMERIO_API_KEY="cio_..."
export CUSTOMERIO_SITE_ID="..."
export KLAVIYO_API_KEY="pk_..."
export INTERCOM_TOKEN="dG9rOi..."
export POSTHOG_PERSONAL_API_KEY="phx_..."
```

## Dormancy definitions (by motion)

| Motion | "Dormant" definition | Reactivation window |
|---|---|---|
| **DTC e-com** | No purchase 60-90 days (varies by purchase frequency benchmark) | 14-30 day sequence |
| **B2B SaaS PLG** | No core action in 30-45 days | 14-21 day sequence |
| **Consumer subscription** | No engagement 21-30 days | 7-14 day sequence |
| **Mobile app** | No app open 7-14 days | 3-7 day push + email |
| **Newsletter / content** | No open in 90 days | 14-day re-engagement |

## Canonical sequence structure (timing + content)

### B2B SaaS PLG (30-day dormant)

```text
Day 0  → Email 1: "Insight or new feature highlight"
         Soft re-entry. NO sell.
         Goal: open + click.

Day 5  → Email 2: "What you're missing"
         Show usage achievement of similar cohort.
         Social proof + curiosity.

Day 12 → Email 3: "Help getting back in?"
         Personal-tone, offer 1:1 / docs.
         Acknowledges absence.

Day 19 → Email 4: "Last call: 20% off if you come back"
         Discount (B2B) or feature unlock.
         Final commercial nudge.

Day 21 → Hard suppression
         No engage = exit cohort; move to dormant-cold.
         Don't re-engage for 90+ days.
```

### DTC e-com (60-day dormant)

```text
Day 0  → "Here's what's new"
         Product launches since last visit.

Day 7  → "Customer favorites this season"
         Trending + social proof.

Day 14 → "10% off — come back"
         Modest discount.

Day 21 → "Last call: 20% off"
         Bigger discount, urgency.

Day 28 → "We're sorry to see you go"
         Hard end / opt-out option / churn feedback survey.
```

## Common recipes

### Recipe 1: Define dormant cohort (PostHog)

```sql
-- B2B SaaS: dormant = no core action in last 30 days, but had been active before
SELECT person_id, email, last_core_action_at
FROM (
  SELECT
    person_id,
    maxIf(timestamp, event = 'core_action') AS last_core_action_at,
    maxIf(timestamp, event = 'User Signed Up') AS signup_at,
    countIf(event = 'core_action' AND timestamp >= now() - INTERVAL 30 DAY) AS recent_actions,
    countIf(event = 'core_action' AND timestamp BETWEEN signup_at AND signup_at + INTERVAL 30 DAY) AS early_actions
  FROM events
  GROUP BY person_id
)
WHERE recent_actions = 0
  AND early_actions >= 3  -- was activated; not pre-PMF dropout
  AND last_core_action_at >= now() - INTERVAL 90 DAY  -- not too cold
```

### Recipe 2: Sync cohort to Customer.io

```bash
# Hightouch model syncs PostHog cohort → Customer.io segment
# Or direct Customer.io API
curl -X POST "https://api.customer.io/v1/segments" \
  -H "Authorization: Bearer $CUSTOMERIO_API_KEY" \
  -d '{
    "name": "Dormant 30d",
    "conditions": {
      "and": [
        {"attribute": "days_since_last_action", "operator": "gte", "value": 30},
        {"attribute": "days_since_last_action", "operator": "lt", "value": 90},
        {"attribute": "lifetime_actions", "operator": "gte", "value": 5}
      ]
    }
  }'
```

### Recipe 3: Customer.io — campaign trigger on segment-entry

```bash
curl -X POST "https://api.customer.io/v1/campaigns" \
  -H "Authorization: Bearer $CUSTOMERIO_API_KEY" \
  -d '{
    "name": "Win-back B2B 30d",
    "trigger": {"type": "segment_entered", "segment_id": "dormant_30d"},
    "actions": [
      {"type": "email", "delay_days": 0, "template": "wb_1_insight"},
      {"type": "email", "delay_days": 5, "template": "wb_2_social_proof"},
      {"type": "email", "delay_days": 12, "template": "wb_3_help_offer"},
      {"type": "email", "delay_days": 19, "template": "wb_4_discount_final"}
    ],
    "exit_criteria": [
      "Email clicked AND Session Started within 48h",
      "Day 21 reached"
    ]
  }'
```

### Recipe 4: Klaviyo — DTC win-back flow

```javascript
// Klaviyo flow trigger: "Customer Lapsed - 60 days no order"
// 1. Filter: total_orders >= 1 (was customer), days_since_last_order >= 60
{
  flow_name: "Win-back 60d DTC",
  trigger: {type: "list_added", list: "Lapsed 60+ days"},
  actions: [
    {delay: 0, template: "wb_whats_new"},
    {delay: 7, template: "wb_favorites"},
    {delay: 14, template: "wb_10pct_off", code: "COMEBACK10"},
    {delay: 21, template: "wb_20pct_off", code: "MISSYOU20"},
    {delay: 28, template: "wb_goodbye_survey"}
  ],
  exit_on: "Placed Order"
}
```

### Recipe 5: Incentive escalation logic

```python
# Don't give max incentive day 1 — train discount-only behavior
escalation = {
    "day_0": {"discount_pct": 0, "messaging": "insight"},
    "day_5": {"discount_pct": 0, "messaging": "social_proof"},
    "day_12": {"discount_pct": 10, "messaging": "soft_offer"},
    "day_19": {"discount_pct": 20, "messaging": "final_call"},
}

# Track: which step triggered reactivation? Optimize.
```

### Recipe 6: Per-user personalization

```python
# Pre-populate email with user's last achievement
def personalize_wb_email(user):
    last_actions = posthog.query(f"""
        SELECT event, count() as n
        FROM events WHERE person_id = '{user.id}'
          AND timestamp >= '{user.signup_at}'
          AND timestamp < now() - INTERVAL 30 DAY
        GROUP BY event ORDER BY n DESC LIMIT 3
    """)
    return {
        "user_first_name": user.first_name,
        "last_achievement": f"You created {last_actions[0]['n']} {last_actions[0]['event']}",
        "since_last_visit_days": (now() - user.last_action).days
    }
```

### Recipe 7: Multi-channel — email + in-app + push

```text
For users still logged in (haven't churned, just dormant):
  Day 0: Email + in-app banner ("Welcome back")
  Day 5: Email + push (if mobile)
  Day 12: Email only
  Day 19: Email + 1:1 outreach (if high-value)

For fully-churned (cancelled subscription):
  Email only. No in-app (no access).
  Push only if app installed.
```

### Recipe 8: Survey on opt-out (exit feedback)

```javascript
// Final email: "Sorry to see you go — 30s survey?"
typeform.create({
  questions: [
    {q: "Why did you stop using us?", type: "single_choice", options: [
      "Found better alternative", "Lost need", "Price", "Bugs / quality", "Don't remember", "Other"
    ]},
    {q: "What would bring you back?", type: "text"}
  ]
});
// Feed responses to Claude for theming → product team review monthly
```

### Recipe 9: Measure win-back effectiveness

```sql
SELECT
  campaign_name,
  variant,
  count() AS sent,
  countIf(opened) AS opens,
  countIf(clicked) AS clicks,
  countIf(reactivated) AS reactivations,
  reactivations * 100.0 / sent AS reactivation_rate,
  sum(post_reactivation_revenue_90d) AS revenue_90d
FROM win_back_campaign_results
GROUP BY campaign_name, variant
ORDER BY reactivation_rate DESC
```

Benchmarks (industry):
- B2B SaaS win-back rate: 2-8%
- DTC e-com: 5-12%
- Consumer subscription: 3-7%

### Recipe 10: Frequency cap + suppression

```python
suppression_rules = {
    "max_win_back_emails_per_quarter": 4,
    "min_days_between_campaigns": 90,
    "hard_suppress_if_3_consecutive_non_opens": True,
    "honor_email_unsubscribe": True,  # legal
    "honor_global_marketing_opt_out": True
}
```

### Recipe 11: A/B test sequence cadence

```javascript
await growthbook.create_experiment({
  name: "win-back-cadence",
  variants: [
    { name: "control_5_email_21day", weight: 0.5 },
    { name: "treatment_3_email_14day", weight: 0.5 }
  ],
  primary_metric: "reactivation_rate",
  secondary_metrics: ["email_open_rate", "unsubscribe_rate"],
  guardrails: ["unsubscribe_rate"],
  sample_size: 2400
});
```

## Examples

### Example 1: B2B SaaS, 22% of MAU dormant after 30 days

Diagnose: most dormancy is post-trial users who didn't convert; some are paid users who lapsed.

Plan:
1. Separate cohorts: post-trial dormant, paid-lapsed.
2. Different sequences per cohort (post-trial = upgrade-focused; paid-lapsed = re-engagement value).
3. Use Recipe 3 + Recipe 6.
4. Track to revenue_90d post-reactivation.

Expected reactivation: 4-7%.

### Example 2: DTC, lapsed 60+ days

Standard 5-touch Klaviyo flow (Recipe 4).
Discount escalation 0% → 10% → 20% (Recipe 5).
Survey on opt-out (Recipe 8).

Expected reactivation: 6-10%.

### Example 3: At-risk users (from churn-prediction-modeling)

Critical-tier (< 40% 30d-survival) → bypass automated, send to CSM for direct outreach.
High-tier (40-55%) → custom email + 20% off retention offer.
Moderate-tier (55-70%) → automated win-back sequence.

## Edge cases / gotchas

- **Win-back ≠ general lifecycle** — these users have shown disengagement; soft-touch first, hard-sell last.
- **Discount training** — if every win-back ends in 20% off, lapsing becomes the route to discount. Vary; cap per user/year.
- **Spammy at-risk targeting** — sending win-back to ALL dormant inflates unsubscribe rate. Filter by lifetime value or engagement quality.
- **Cold cohort handling** — > 90 days dormant rarely reactivates via email. Save effort.
- **Email deliverability degradation** — sending to long-dormant addresses → bounces + spam complaints → IP reputation drop. Suppress 90+ days no-engage.
- **Brand-different sub-brand** — for portfolio brands (parent + sub), win-back sender mismatch confuses. Send from consistent identity.
- **Mobile push fatigue** — push to inactive users is risky; iOS users often turn off if abused.
- **Personalization-data freshness** — referencing stale data ("Your last document from 2025") feels cold; ensure data ≤ 14 days old.
- **GDPR / CAN-SPAM** — honor unsubscribe + global opt-out; track separately from suppression.
- **Reactivation ≠ retention** — re-engaged user may churn fast again. Track post-reactivation retention 30/60/90.

## Sources

- Customer.io campaigns: https://customer.io/docs/journeys/campaigns/
- Klaviyo win-back flows: https://help.klaviyo.com/hc/en-us/articles/115005076647-Win-Back-Flow
- Customer.io vs Braze 2026: https://www.getvero.com/resources/braze-vs-customer-io-which-is-better-in-2026/
- Reforge — Brian Balfour on retention: https://www.reforge.com/blog/
- PostHog cohorts API: https://posthog.com/docs/data/cohorts
- Lenny's PLG Handbook (re-engagement): https://plghandbook.com/
- ProductLed re-engagement: https://www.productled.org/foundations/product-led-growth-metrics
