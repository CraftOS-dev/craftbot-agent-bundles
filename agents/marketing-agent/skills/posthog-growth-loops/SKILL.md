<!--
Source: https://posthog.com/docs/model-context-protocol
PostHog MCP at mcp.posthog.com
-->
# PostHog Growth Loops — SKILL

PostHog MCP exposes HogQL — PostHog's SQL dialect — via the `query` tool. The SOTA path for measuring growth loops: viral coefficient (K), cycle time, retention curves, CAC payback, activation rate, LTV:CAC. Works for product-led, content-led, or viral loops.

## When to use this skill

- **Growth loop measurement** — K, cycle time, leakage at each step.
- **Retention curves** — Day 1, 7, 30, 90 cohort retention.
- **Activation rate** — % of new users hitting the "aha" moment.
- **Funnel analysis** — conversion at each step.
- **A/B test result analysis** (post-experiment, paired with GrowthBook).
- **Cohort analysis** — behavior by sign-up source, plan, etc.
- **CAC payback** — revenue per cohort / acquisition cost.

**Do NOT use this skill when:**
- **GA4-style attribution** (last-click, multi-touch) — use `google-analytics-mcp-attribution` skill.
- **Experiment orchestration** (flag flipping, traffic allocation) — use `growthbook-experiments` skill.
- **Email-specific metrics** (CTR, CTOR, revenue per email) — use `klaviyo-email-lifecycle` skill.

## Setup

### Install / connect

```bash
# PostHog hosts MCP at mcp.posthog.com (remote)
export POSTHOG_PROJECT_API_KEY="phc_<key>"          # public ingest
export POSTHOG_PERSONAL_API_KEY="phx_<key>"         # for query
export POSTHOG_HOST="https://app.posthog.com"        # or self-hosted URL
export POSTHOG_PROJECT_ID="<numeric>"
```

```json
// claude-config.json
{
  "posthog": {
    "transport": "https",
    "url": "https://mcp.posthog.com/v1",
    "auth": {"type":"bearer","token":"${POSTHOG_PERSONAL_API_KEY}"}
  }
}
```

### Tools available

- `query` — HogQL execution
- `events_list` — recent event stream
- `actions_list`, `actions_create` — saved actions
- `cohorts_list`, `cohorts_create`
- `funnel` — funnel definition + conversion
- `retention` — retention table
- `insights_list`, `insights_create`
- `dashboards_list`, `dashboards_create`
- `experiments_list` (results-only; orchestrate via GrowthBook)

## Common recipes

### Recipe 1: Retention curves (HogQL)

```sql
-- 30-day retention curve by signup week
SELECT
  toStartOfWeek(min_signup) AS signup_week,
  count(DISTINCT person_id) AS cohort_size,
  countDistinctIf(person_id, days_to_action <= 1) AS day_1,
  countDistinctIf(person_id, days_to_action <= 7) AS day_7,
  countDistinctIf(person_id, days_to_action <= 30) AS day_30,
  countDistinctIf(person_id, days_to_action <= 90) AS day_90
FROM (
  SELECT
    person_id,
    min(if(event='user signed up', timestamp, null)) AS min_signup,
    dateDiff('day', min(if(event='user signed up', timestamp, null)), timestamp) AS days_to_action
  FROM events
  WHERE event IN ('user signed up','core action completed')
  GROUP BY person_id, timestamp
)
GROUP BY signup_week
ORDER BY signup_week DESC
LIMIT 12
```

Run via:

```bash
mcp tool posthog.query --query "$(cat retention.sql)"
```

Targets per role.md (Growth metrics):
- Day 7: > 40%
- Day 30: > 20%
- Day 90: > 10%

### Recipe 2: Viral coefficient K

```sql
-- K = invites_sent_per_user × conversion_rate_of_invites
WITH inviter_stats AS (
  SELECT
    person_id AS inviter,
    count() AS invites_sent
  FROM events
  WHERE event = 'invite sent'
    AND timestamp >= now() - INTERVAL 30 DAY
  GROUP BY person_id
),
invite_conversion AS (
  SELECT
    countIf(event='invite accepted') / countIf(event='invite sent') AS conv_rate
  FROM events
  WHERE event IN ('invite sent','invite accepted')
    AND timestamp >= now() - INTERVAL 30 DAY
)
SELECT
  avg(invites_sent) AS avg_invites_per_user,
  (SELECT conv_rate FROM invite_conversion) AS invite_conv_rate,
  avg(invites_sent) * (SELECT conv_rate FROM invite_conversion) AS viral_coefficient_K
FROM inviter_stats
```

K > 1 = exponential growth. K < 1 = viral decay (still useful but not standalone growth engine).

### Recipe 3: Cycle time (loop iteration length)

```sql
-- Time between signup → first invite sent
SELECT
  quantile(0.5)(dateDiff('hour', signup_time, invite_time)) AS p50_cycle_hours,
  quantile(0.75)(dateDiff('hour', signup_time, invite_time)) AS p75_cycle_hours
FROM (
  SELECT
    person_id,
    min(if(event='user signed up', timestamp, null)) AS signup_time,
    min(if(event='invite sent', timestamp, null)) AS invite_time
  FROM events
  WHERE event IN ('user signed up','invite sent')
  GROUP BY person_id
  HAVING signup_time IS NOT NULL AND invite_time IS NOT NULL
)
```

Shorter cycle = faster loop. Target p50 < 7 days for self-serve products.

### Recipe 4: Activation rate

```sql
-- Activation = completed core action within 7 days of signup
SELECT
  countDistinct(person_id) AS new_users,
  countDistinctIf(person_id, activated) AS activated_users,
  countDistinctIf(person_id, activated) / countDistinct(person_id) AS activation_rate
FROM (
  SELECT
    person_id,
    minIf(timestamp, event='user signed up') AS signup_ts,
    maxIf(timestamp, event='core action completed' AND timestamp <= signup_ts + INTERVAL 7 DAY) IS NOT NULL AS activated
  FROM events
  WHERE event IN ('user signed up','core action completed')
    AND timestamp >= now() - INTERVAL 30 DAY
  GROUP BY person_id
)
```

Target: > 60% activation in first 7 days.

### Recipe 5: Funnel analysis (loop step leakage)

```bash
mcp tool posthog.funnel \
  --name "Growth-Loop-Funnel" \
  --steps '[
    {"event":"user signed up"},
    {"event":"profile completed"},
    {"event":"first content created"},
    {"event":"content shared"},
    {"event":"invitee landed"},
    {"event":"invitee signed up"}
  ]' \
  --conversion_window_seconds 1209600 \
  --date_range "last_30_days"
```

Output: conversion rate at each step. Lowest rate = the constraint to invest in (per role.md loop design process Step 3).

### Recipe 6: CAC payback period

```sql
-- Cohort revenue (cumulative) vs CAC
WITH cohort_acquisition AS (
  SELECT
    toStartOfMonth(min(timestamp)) AS cohort_month,
    person_id,
    properties.source AS source
  FROM events
  WHERE event = 'user signed up'
    AND timestamp >= now() - INTERVAL 12 MONTH
  GROUP BY person_id, properties.source
),
revenue_by_cohort AS (
  SELECT
    c.cohort_month,
    c.source,
    sum(e.properties.amount) AS revenue
  FROM cohort_acquisition c
  JOIN events e ON e.person_id = c.person_id
  WHERE e.event = 'purchase'
  GROUP BY c.cohort_month, c.source
)
SELECT
  cohort_month,
  source,
  revenue,
  -- CAC pulled from external (ad spend / new users this cohort)
  revenue / cohort_size AS arpu
FROM revenue_by_cohort
```

Combine with HubSpot ad spend or Meta Ads spend (via Meta Ads MCP) for full CAC = total_spend / new_users.

Payback period = months until cumulative ARPU > CAC.

### Recipe 7: Cohort creation for marketing

```bash
mcp tool posthog.cohorts_create \
  --name "Activated-Power-Users" \
  --filters '{
    "type":"AND",
    "conditions":[
      {"event":"core action completed","operator":">=","value":10,"window_days":30},
      {"event":"invite sent","operator":">=","value":1,"window_days":30}
    ]
  }'
```

Then export to Klaviyo/HubSpot for tailored campaigns (advocate program, NPS survey, referral bonuses).

### Recipe 8: A/B test result analysis (post-GrowthBook experiment)

```sql
-- Compare conversion rate by variant
SELECT
  properties.$feature_flag_response AS variant,
  countDistinct(person_id) AS users,
  countDistinctIf(person_id, event='purchase') AS converters,
  countDistinctIf(person_id, event='purchase') / countDistinct(person_id) AS conv_rate
FROM events
WHERE properties.$feature_flag = 'pricing-page-v2'
  AND timestamp >= '2026-05-01'
GROUP BY variant
```

For stat significance, use GrowthBook's built-in tooling (`growthbook-experiments` skill).

## Examples — full loop measurement dashboard

```python
# Pseudo-flow run weekly
loop_metrics = {}

# 1. K
loop_metrics['K'] = posthog.query(viral_k_sql)
# 2. Cycle time
loop_metrics['cycle_p50'] = posthog.query(cycle_time_sql)
# 3. Activation
loop_metrics['activation_rate'] = posthog.query(activation_sql)
# 4. Retention
loop_metrics['retention'] = posthog.query(retention_curve_sql)
# 5. Funnel
loop_metrics['funnel'] = posthog.funnel(steps=loop_steps)
# 6. CAC payback (joined with Meta/Google ads spend)
ad_spend = meta_ads.get_campaign_insights(date_preset='last_30_days')
loop_metrics['CAC'] = ad_spend['spend'] / loop_metrics['retention']['cohort_size']

# Write to Notion dashboard
notion.update_page(growth_dashboard, properties=loop_metrics)

# Alert on regressions
if loop_metrics['K'] < 0.5: alert("Viral K dropped below 0.5")
if loop_metrics['activation_rate'] < 0.50: alert("Activation rate < 50%")
if loop_metrics['retention']['day_30'] < 0.15: alert("Day 30 retention < 15%")
```

## Edge cases

### HogQL vs ClickHouse SQL
HogQL is a thin layer over ClickHouse. Most ClickHouse functions work but some require PostHog-specific syntax:
- `person_id` — PostHog auto-resolved identity
- `properties.<key>` — JSON path into event properties
- `$feature_flag_response` — built-in feature flag tracker

### Person identification
PostHog merges anonymous → identified users. For accurate retention, track `$identify` events on signup and link `distinct_id` to email/userid.

### Event volume + cost
PostHog Cloud: $0.00031 per event after 1M free/month. Bulk loop measurement (10M events) ~$3000/month. Self-host for high-volume cases.

### Identify event timing
Identify before tracking core events for highest match rate. If late-identifying, retroactive merging works but lags.

### Funnel conversion windows
- Short window (1h) = same-session funnels (signup → activation)
- Long window (14d) = lifecycle funnels (signup → core action → invite)
- Set per-funnel; too-short windows undercount conversions

### Retention cohort definition
- "Returning" event MUST be a meaningful action, not just any session
- Use `core action completed` or `key feature used`, not `page_view`

### Stat significance for K
Need ≥30 inviters with ≥10 invites each for reliable K calculation. Below that, report with confidence interval.

### Insights API
For dashboard creation, `insights_create` accepts the same shape as the UI insight builder. Pre-define common templates:
- Loop K (single number)
- Retention curve (heatmap)
- Funnel (steps + conversion)
- Cohort size by source (stacked bar)

### Self-hosted PostHog
Same MCP works; just override `POSTHOG_HOST`. Self-hosted is free at any scale but requires Postgres + ClickHouse ops.

## Sources

- **PostHog MCP docs**: https://posthog.com/docs/model-context-protocol
- **HogQL reference**: https://posthog.com/docs/hogql
- **Viral coefficient math**: https://posthog.com/tutorials/viral-coefficient
- **Retention guide**: https://posthog.com/tutorials/retention
- **Funnels API**: https://posthog.com/docs/api/funnels
