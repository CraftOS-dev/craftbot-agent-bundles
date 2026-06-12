<!--
Source: Amplitude cohort retention guide + Andrew Chen retention curves + Reforge retention frameworks
-->
# Retention Curve Diagnosis — J / Smile / Decay / Flat SKILL

> Plot cohorted retention curves (Day 0/1/7/30/90/180), classify the shape (J / smile / decay / flat-after-drop), and prescribe the right intervention per shape. Retention is the truth — acquisition lies; retention curves rarely do.

## When to use

Trigger phrases:
- "Why are we churning?"
- "What's our retention?"
- "Are we PMF?" (retention curve is the truth test)
- "Should we focus on activation or expansion?"
- "Is our product getting better?" (compare cohort curves over time)

Do NOT use for:
- Churn *prediction* per-user (use `churn-prediction-modeling`)
- Win-back execution (use `win-back-campaigns`)
- Funnel-only metrics (use `signup-activation-conversion-optimization`)

## Setup

```bash
export POSTHOG_PERSONAL_API_KEY="phx_..."
export AMPLITUDE_OAUTH_TOKEN="amp_..."
export MIXPANEL_API_KEY="mx_..."
```

Required event taxonomy:
- `User Signed Up` (cohort entry)
- `Session Started` or `Core Action` (return event — NOT page_view)
- Optionally: subscription events for billing-based retention

## The 4 canonical shapes

| Shape | Looks like | Diagnosis | Intervention |
|---|---|---|---|
| **Smile** | Drop, then climb above start | Strong PMF + re-engagement loop working | Amplify what's working; don't fix |
| **J-curve** | Drop fast, then asymptote > 0 | PMF for a segment | Identify surviving segment; build for them |
| **Decay** | Approaches 0; no asymptote | Pre-PMF or onboarding broken | Fix activation first; expansion will fail |
| **Flat-after-drop** | Drop fast, then steady at low % | Small loyal cohort | NRR expansion on survivors |

Benchmarks (B2B SaaS, 2024 PostHog + Amplitude):
- Day 1 retention: > 60%
- Day 7 retention: > 40%
- Day 30 retention: > 20%
- Day 90 retention: > 10%
- Day 180 retention: > 7% (long-tail asymptote)

## Common recipes

### Recipe 1: PostHog retention curve query

```sql
-- Cohorted retention by signup week, Day 1/7/30/90
WITH signup_cohorts AS (
  SELECT
    person_id,
    toStartOfWeek(min(timestamp)) AS signup_week,
    min(timestamp) AS signup_ts
  FROM events
  WHERE event = 'User Signed Up'
    AND timestamp BETWEEN now() - INTERVAL 26 WEEK AND now() - INTERVAL 1 WEEK
  GROUP BY person_id
),
returns AS (
  SELECT
    s.person_id,
    s.signup_week,
    countDistinctIf(e.timestamp,
      dateDiff('day', s.signup_ts, e.timestamp) = 1) AS d1,
    countDistinctIf(e.timestamp,
      dateDiff('day', s.signup_ts, e.timestamp) BETWEEN 7 AND 13) AS d7,
    countDistinctIf(e.timestamp,
      dateDiff('day', s.signup_ts, e.timestamp) BETWEEN 30 AND 36) AS d30,
    countDistinctIf(e.timestamp,
      dateDiff('day', s.signup_ts, e.timestamp) BETWEEN 90 AND 96) AS d90
  FROM signup_cohorts s
  JOIN events e ON e.person_id = s.person_id
  WHERE e.event IN ('Session Started', 'core_action')
    AND e.timestamp > s.signup_ts
  GROUP BY s.person_id, s.signup_week
)
SELECT
  signup_week,
  count() AS cohort_size,
  countIf(d1 > 0) * 100.0 / count() AS d1_retention_pct,
  countIf(d7 > 0) * 100.0 / count() AS d7_retention_pct,
  countIf(d30 > 0) * 100.0 / count() AS d30_retention_pct,
  countIf(d90 > 0) * 100.0 / count() AS d90_retention_pct
FROM returns
GROUP BY signup_week
ORDER BY signup_week DESC
```

### Recipe 2: Native PostHog `retention` MCP tool

```bash
mcp tool posthog.retention \
  --target_entity '{"event": "User Signed Up"}' \
  --returning_entity '{"event": "core_action"}' \
  --period "Day" \
  --total_intervals 90 \
  --date_from "-180d"
```

Returns matrix: cohort × day-offset → retention %.

### Recipe 3: Classify the shape (rules)

```python
def classify_retention_curve(d1, d7, d30, d90, d180):
    """Returns one of: smile, J, decay, flat_after_drop, undefined"""
    if d180 is None: d180 = d90 * 0.85  # estimate if not present
    
    if d180 > d30 * 1.1 and d90 > d7 * 0.85:
        return "smile"  # climbs back
    if d180 > 0.07 and (d30 - d90) / d30 < 0.3:
        return "J"  # asymptote sustained
    if d30 < 0.10 and d90 < 0.05:
        return "decay"  # approaches 0
    if d7 < d1 * 0.3 and (d30 - d90) / d30 < 0.2:
        return "flat_after_drop"  # plateaus low
    return "undefined"
```

### Recipe 4: Amplitude retention chart

```javascript
await amplitude.create_chart({
  type: "retention",
  starting_event: "User Signed Up",
  returning_event: "core_action",
  date_range: { last_n: 180, unit: "days" },
  group_by: ["icp_segment", "signup_source"],
  retention_type: "n_day"  // or "unbounded" or "bracket"
});
```

### Recipe 5: Mixpanel retention query

```javascript
// Mixpanel retention
{
  "from_date": "2026-01-01",
  "to_date": "2026-06-01",
  "born_event": "User Signed Up",
  "event": "core_action",
  "interval": "day",
  "interval_count": 90,
  "retention_type": "birth"  // or "compounded"
}
```

### Recipe 6: Cohort slice — find the surviving segment (J-curve case)

```sql
SELECT
  properties.icp_segment AS segment,
  properties.plan_tier AS tier,
  properties.signup_source AS source,
  count() AS cohort_size,
  countIf(active_d90) * 100.0 / count() AS d90_retention_pct,
  countIf(active_d180) * 100.0 / count() AS d180_retention_pct
FROM cohort_with_retention_flags
GROUP BY segment, tier, source
HAVING cohort_size >= 50
ORDER BY d90_retention_pct DESC
LIMIT 20
```

Identify top 3-5 segment combos with highest D90/D180 retention. Build product / pricing / acquisition strategy for that surviving cohort.

### Recipe 7: Curve-over-time comparison (is product getting better?)

```sql
-- Are recent cohorts retaining better than older ones?
SELECT
  toStartOfMonth(signup_ts) AS signup_month,
  count() AS cohort_size,
  avg(d7_retained) AS d7_rate,
  avg(d30_retained) AS d30_rate
FROM cohort_table
WHERE dateDiff('day', signup_ts, now()) >= 30
GROUP BY signup_month
ORDER BY signup_month
```

If newest cohorts retaining better → product improving (intervention working). If flat or worse → ship more activation / feature improvements.

### Recipe 8: Diagnostic decision tree (shape → action)

```text
DECAY
├─ d1 < 30%       → signup-to-aha onboarding broken → activation-funnel-aha-moment skill
├─ d1 > 60%, d7 < 20% → aha was hit but didn't stick → habit-loop redesign + push notifications
└─ d7 > 30%, d30 < 5% → no retention loop → introduce content/email/notification re-engagement

J-CURVE (asymptote > 0)
├─ asymptote 5-15% → niche product fit → narrow ICP, identify surviving segment
├─ asymptote 15-30% → solid PMF → expansion + revenue per user focus (NRR skill)
└─ asymptote > 30% → exceptional → amplify acquisition

SMILE
├─ rare; usually because re-engagement loop drives back inactive users
└─ Action: identify the re-engagement trigger; instrument; amplify

FLAT-AFTER-DROP
├─ Action: NRR expansion on survivors; upsell, cross-sell
└─ Don't waste effort on lower-retention segments
```

### Recipe 9: Slice by acquisition channel (quality filter)

```sql
SELECT
  properties.utm_source,
  properties.utm_medium,
  count() AS cohort,
  avg(d30_retained) AS d30_rate
FROM cohort_with_retention
GROUP BY properties.utm_source, properties.utm_medium
HAVING cohort >= 100
ORDER BY d30_rate DESC
```

If a paid channel has D30 < 50% of organic → channel attracting wrong users; cut CAC there or rework messaging.

### Recipe 10: Subscription / billing retention overlay (for SaaS)

```sql
-- Logo retention (active subscription) vs engagement retention
SELECT
  signup_month,
  count() AS cohort,
  countIf(active_subscription_d90) * 100.0 / count() AS logo_d90_pct,
  countIf(active_engagement_d90) * 100.0 / count() AS engagement_d90_pct
FROM subscription_cohort
GROUP BY signup_month
ORDER BY signup_month
```

Logo retention > engagement retention → users paying but disengaging (churn risk; predict via `churn-prediction-modeling`).
Engagement > logo → users getting value but cancelling for cost reasons (pricing skill).

## Examples

### Example 1: SaaS analytics product — decay curve

Curves:
- D1 = 71%, D7 = 28%, D30 = 8%, D90 = 3%

Classification: decay.

Diagnosis: D1 fine (good signup-to-first-session), D7 weak (haven't hit habit), D30 crashes.

Action: NOT win-back campaigns; NOT pricing experiments. Run `activation-funnel-aha-moment` skill — find and fix the activation event.

### Example 2: B2B SaaS PLG — J-curve at 22%

Curves:
- D1 = 68%, D7 = 41%, D30 = 27%, D90 = 22%, D180 = 21%

Classification: J-curve, healthy asymptote.

Diagnosis: PMF achieved. 22% of cohort retains long-term.

Slice analysis: Surviving segment = mid-market B2B (50-500 employees), plan_tier=team. Consumer/solo accounts churn fast.

Action:
1. Narrow ICP — paid acquisition only for mid-market.
2. Build NRR expansion on the 22% (`expansion-revenue-nrr-optimization` skill).
3. Don't waste effort on solo-tier; consider deprecating or repricing.

### Example 3: Consumer social app — smile curve

Curves:
- D1 = 38%, D7 = 22%, D30 = 18%, D90 = 23%, D180 = 28%

Classification: smile.

Diagnosis: rare — re-engagement loop working. Investigate.

Find trigger:
```sql
SELECT event, count() FROM events
WHERE person_id IN (cohort_who_returned_after_drop_off)
  AND timestamp BETWEEN drop_off_end AND return_event
GROUP BY event
ORDER BY count() DESC
```

Likely culprit: push notification, email, social share from another user, content seasonality.

Action: amplify the trigger; ensure it's consistent.

## Edge cases / gotchas

- **Aggregate retention lies** — combining new + old cohorts hides cohort-specific shape. Always cohort by acquisition week.
- **Selection bias from short observation** — D90 retention for a cohort signed up 30 days ago is unknown. Censor / exclude undersaturated cohorts.
- **"Returning" event matters** — page_view inflates retention (users open and bounce). Use core_action or session_meaningful.
- **N-day vs unbounded vs bracket** — N-day = "active on day N exactly"; unbounded = "active anytime ≥ day N"; bracket = "active in day N-(N+6) range". Unbounded inflates; N-day strictest. Default: bracket (Day 7 = days 7-13).
- **Compounded retention** — Mixpanel default; "still active every period". Punishing; rarely matches business reality.
- **Smile illusion** — sometimes a "smile" is just survivorship of one re-engagement campaign. Look at cohort-month consistency.
- **Hot-cold weeks** — holidays + seasonality distort. Annotate; compare to year-ago cohorts.
- **Flat-after-drop misread as decay** — slow decline can look flat in short window. Extend to D180+.
- **Subscription auto-renewal masks churn** — annual contracts mean engagement-churn precedes logo-churn by months. Track both.

## Sources

- Amplitude — Cohort retention analysis: https://amplitude.com/explore/analytics/cohort-retention-analysis
- Andrew Chen — Smile vs J vs decay: https://andrewchen.com/retention-curves/
- Reforge — Casey Winters retention frameworks: https://www.reforge.com/blog/the-retention-roadmap
- PostHog — Retention tutorial: https://posthog.com/tutorials/retention
- Mixpanel — Retention reports: https://docs.mixpanel.com/docs/reports/retention
- Lenny's PLG Handbook (retention): https://plghandbook.com/retention/
- ProductLed PLG metrics: https://www.productled.org/foundations/product-led-growth-metrics
