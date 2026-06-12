<!--
Source: https://posthog.com/docs/product-analytics/funnels + https://help.pendo.io/resources/support-library/analytics/index + https://amplitude.com/docs/apis/analytics
-->
# Ramp-to-Value — TTFV / TTRV — SKILL

Track Time-to-First-Value (TTFV: days from signup to first aha event) and Time-to-Repeat-Value (TTRV: days from first aha to second meaningful event). PostHog HogQL funnel queries primary; Mixpanel/Amplitude/Pendo alts. Per-customer + per-cohort. Intervention triggers: Day 5 no TTFV -> CSM outreach; Day 7 -> Pendo card; Day 10 -> 1:1 call.

## When to use

- **TTFV monitoring** — daily cohort report.
- **Onboarding intervention** — Day 5/7/10 progressive escalation if no first_aha_event.
- **Cohort regression** — Q2 cohort TTFV worse than Q1; diagnose.
- **Product feedback loop** — TTFV regression after release -> regression to PM.
- **QBR data prep** — slide 4 adoption snapshot includes customer's TTFV.
- **A/B onboarding flow variant comparison** — variant A TTFV vs variant B.

This skill **complements** `customer-onboarding-day-0-90` (which schedules milestones; this skill measures whether they hit) and `adoption-metric-feature-usage` (which measures sustained adoption beyond first value).

Trigger phrases: "TTFV", "TTRV", "time to first value", "ramp to value", "first aha", "activation funnel", "second value event".

## Setup

```bash
# Product analytics MCPs already in agent.yaml
# posthog-mcp, mixpanel-mcp, amplitude-mcp

# Pendo (alt + Adopt analytics)
export PENDO_API_KEY="<key>"

# Heap
export HEAP_APP_ID="<id>"

# Postgres warehouse for cohort math - postgresql-mcp wired
```

Workspace prerequisites:
- PostHog event taxonomy includes `signup`, `first_aha_event`, `second_aha_event`, with `customer_id` on each.
- Per-product TTFV target documented (e.g., self-serve < 7d; enterprise < 30d).
- Postgres view `customer_ramp` materialized nightly.

## Definitions

- **TTFV (Time to First Value):** days from `signup` to `first_aha_event`. Target < 7d (self-serve) / < 30d (enterprise).
- **TTRV (Time to Repeat Value):** days from `first_aha_event` to `second_aha_event`. Target < 14d. Indicates habit formation.

## Common recipes

### Recipe 1: PostHog HogQL - per-customer TTFV

```sql
SELECT
  properties.customer_id AS customer_id,
  min(timestamp) FILTER (WHERE event = 'signup') AS signup_at,
  min(timestamp) FILTER (WHERE event = 'first_aha_event') AS first_aha_at,
  dateDiff('day',
    min(timestamp) FILTER (WHERE event = 'signup'),
    min(timestamp) FILTER (WHERE event = 'first_aha_event')
  ) AS ttfv_days
FROM events
WHERE event IN ('signup', 'first_aha_event')
GROUP BY properties.customer_id
HAVING min(timestamp) FILTER (WHERE event = 'first_aha_event') IS NOT NULL;
```

Via `posthog-mcp query`. Doc: https://posthog.com/docs/api/queries

### Recipe 2: PostHog HogQL - per-customer TTRV

```sql
SELECT
  properties.customer_id AS customer_id,
  min(timestamp) FILTER (WHERE event = 'first_aha_event') AS first_aha_at,
  min(timestamp) FILTER (WHERE event = 'second_aha_event') AS second_aha_at,
  dateDiff('day',
    min(timestamp) FILTER (WHERE event = 'first_aha_event'),
    min(timestamp) FILTER (WHERE event = 'second_aha_event')
  ) AS ttrv_days
FROM events
WHERE event IN ('first_aha_event', 'second_aha_event')
GROUP BY properties.customer_id;
```

### Recipe 3: Cohort TTFV by signup month

```sql
SELECT
  date_trunc('month', signup_at) AS cohort_month,
  count(*) AS customers_signed,
  count(*) FILTER (WHERE first_aha_at IS NOT NULL) AS reached_first_value,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY ttfv_days) AS p50_ttfv,
  percentile_cont(0.75) WITHIN GROUP (ORDER BY ttfv_days) AS p75_ttfv,
  percentile_cont(0.9) WITHIN GROUP (ORDER BY ttfv_days) AS p90_ttfv,
  100.0 * count(*) FILTER (WHERE first_aha_at IS NOT NULL) / count(*)::numeric AS reached_pct
FROM customer_ramp
WHERE signup_at >= now() - INTERVAL '12 months'
GROUP BY cohort_month
ORDER BY cohort_month;
```

### Recipe 4: Cohort TTFV by acquisition channel

```sql
SELECT
  acquisition_channel,
  count(*) AS customers,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY ttfv_days) AS p50_ttfv,
  count(*) FILTER (WHERE ttfv_days <= 7) * 1.0 / count(*) AS pct_under_7d
FROM customer_ramp r
JOIN customers c USING (customer_id)
WHERE r.signup_at >= now() - INTERVAL '90 days'
GROUP BY acquisition_channel
ORDER BY p50_ttfv ASC;
```

### Recipe 5: Cohort TTFV by tier

```sql
SELECT
  tier,
  count(*) AS customers,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY ttfv_days) AS p50_ttfv,
  count(*) FILTER (WHERE ttfv_days <= 7) * 1.0 / count(*) AS pct_under_7d
FROM customer_ramp r
JOIN customers c USING (customer_id)
WHERE r.signup_at >= now() - INTERVAL '90 days'
GROUP BY tier;
```

Starter typically < 5d (simple); Enterprise 15-30d (complex setup).

### Recipe 6: Pre-aha intervention queue (Day 5+)

```sql
SELECT customer_id, signup_at, days_since_signup
FROM (
  SELECT customer_id, signup_at,
         dateDiff('day', signup_at, now()) AS days_since_signup,
         first_aha_at
  FROM customer_ramp
) x
WHERE first_aha_at IS NULL
  AND days_since_signup BETWEEN 5 AND 10;
```

For each row, fire intervention:
- Day 5: CSM outreach (gmail-mcp)
- Day 7: Pendo in-product card (enroll via `in-app-onboarding-userpilot-appcues-pendo`)
- Day 10: 1:1 call (Calendly link)

### Recipe 7: Mixpanel funnel alt

```bash
curl -sS "https://mixpanel.com/api/2.0/funnels" \
  -u "$MIXPANEL_API_KEY:" \
  --data-urlencode 'events=["signup", "first_aha_event"]' \
  --data-urlencode 'from_date=2026-05-01' \
  --data-urlencode 'to_date=2026-05-31'
```

Doc: https://developer.mixpanel.com/reference/funnel-events

### Recipe 8: Amplitude funnel alt

```bash
curl -sS "https://amplitude.com/api/2/funnels" \
  -u "$AMPLITUDE_API_KEY:$AMPLITUDE_SECRET" \
  --data-urlencode 'e={"event_type":"signup"}' \
  --data-urlencode 'e={"event_type":"first_aha_event"}' \
  --data-urlencode 'start=20260501' \
  --data-urlencode 'end=20260531'
```

Doc: https://amplitude.com/docs/apis/analytics

### Recipe 9: Pendo Adopt funnel

Pendo "Funnels" feature surfaces TTFV natively when configured in UI. Read via:

```bash
curl -sS "https://app.engage.pendo.io/api/v1/funnels/$FUNNEL_ID/aggregations" \
  -H "X-Pendo-Integration-Key: $PENDO_API_KEY"
```

### Recipe 10: Materialize customer_ramp view

```sql
CREATE OR REPLACE VIEW customer_ramp AS
SELECT
  customer_id,
  signup_at,
  first_aha_at,
  second_aha_at,
  EXTRACT(DAY FROM (first_aha_at - signup_at))::int AS ttfv_days,
  EXTRACT(DAY FROM (second_aha_at - first_aha_at))::int AS ttrv_days
FROM (
  SELECT customer_id,
         MIN(timestamp) FILTER (WHERE event = 'signup') AS signup_at,
         MIN(timestamp) FILTER (WHERE event = 'first_aha_event') AS first_aha_at,
         MIN(timestamp) FILTER (WHERE event = 'second_aha_event') AS second_aha_at
  FROM events
  GROUP BY customer_id
) e;
```

Refresh nightly.

### Recipe 11: Weekly TTFV report

```sql
SELECT
  date_trunc('week', signup_at) AS week,
  count(*) AS signups,
  count(first_aha_at) AS reached_first_value,
  count(second_aha_at) AS reached_second_value,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY ttfv_days) AS p50_ttfv_days,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY ttrv_days) FILTER (WHERE ttrv_days IS NOT NULL) AS p50_ttrv_days
FROM customer_ramp
WHERE signup_at >= now() - INTERVAL '12 weeks'
GROUP BY week
ORDER BY week;
```

Pipe to weekly Slack post via `slack-mcp` in #cs-ops.

### Recipe 12: TTFV regression detection

```sql
WITH this_month AS (
  SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY ttfv_days) AS p50
  FROM customer_ramp
  WHERE signup_at >= date_trunc('month', now())
),
last_month AS (
  SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY ttfv_days) AS p50
  FROM customer_ramp
  WHERE signup_at BETWEEN date_trunc('month', now()) - INTERVAL '1 month'
                     AND date_trunc('month', now()) - INTERVAL '1 day'
)
SELECT tm.p50 AS this_month_p50,
       lm.p50 AS last_month_p50,
       tm.p50 - lm.p50 AS regression_days
FROM this_month tm, last_month lm;
```

If `regression_days > 1d`, alert PM via Linear ("voice-of-customer" + "ttfv-regression" labels).

### Recipe 13: Custom aha event definition per product

Document per-product (in Notion CS playbook):

| Product | First aha event | Second aha event |
|---|---|---|
| Workflow Builder | First workflow published | Workflow re-run within 7d |
| Analytics Tool | First dashboard saved | Second user invited to dashboard |
| API SaaS | First successful API call | 100+ API calls in same day |

Update event taxonomy + Recipe 1/2 queries when product changes.

## Examples

### Example 1: Weekly TTFV monitoring

**Goal:** CSM ops sees TTFV trend Monday morning.

**Steps:**
1. Sunday 23:00 UTC: Recipe 10 materializes view.
2. Monday 06:00 UTC: Recipe 11 weekly report.
3. Monday 06:30 UTC: Recipe 12 regression check; if > 1d, alert PM.
4. Monday 09:00 UTC: Slack post to #cs-ops with summary.

**Result:** TTFV health visible weekly; regressions flagged.

### Example 2: TTFV intervention cascade

**Goal:** Acme signed up 2026-06-04; today's 2026-06-11 (Day 7); still no first_aha.

**Steps:**
1. Recipe 6 - Acme in queue at Day 5; CSM outreach sent.
2. Day 7 (today): still no first_aha. Pendo card enrollment via `in-app-onboarding`.
3. Day 10 if still no first_aha: Calendly 1:1 invite.
4. Day 14 if still no first_aha: escalate to CSM Lead; consider save play (early intervention).

**Result:** Progressive intervention; minimize abandonment.

## Edge cases / gotchas

- **First aha event misdefined** — if event fires too easily (e.g., "first login"), TTFV looks great but doesn't predict retention. Calibrate against churn correlation (validate quarterly).
- **No first_aha_event for enterprise** — they're still in setup at Day 30. Document longer target; don't alarm on Day 7 absence.
- **Customer signup vs user signup** — TTFV per customer = first user to fire first_aha at that customer. Don't confuse with per-user TTFV.
- **Cohort sample size** — < 30 signups/month = noisy. Aggregate quarterly.
- **Second_aha definition drift** — easy to over-engineer; keep it simple: "Did they come back and do the thing again?"
- **TTRV NULL when first_aha very recent** — Recipe 11 filter `ttrv_days IS NOT NULL` matters.
- **Product release breaks first_aha event** — engineering renames event; metric crashes. Add data quality check on event volume.
- **Free fallback** — Postgres + raw event table is fine; no need for paid analytics if event taxonomy is good.
- **B2C vs B2B** — B2C "ramp" measured per user. B2B per customer. Don't mix.
- **Acquisition channel TTFV doesn't mean channel quality** — channel-mix self-select; control for tier/vertical when comparing.
- **Don't share absolute TTFV with customer** — they don't care about "median TTFV is 6.4d." Share customer's own progress: "You're 3d in; first aha typically around day 5 - you're on track."
- **Pendo first-aha tracking native** — Pendo Adopt tracks this out-of-box if events are tagged; might be sufficient without PostHog.

## Sources

- [PostHog Funnels docs](https://posthog.com/docs/product-analytics/funnels)
- [PostHog HogQL Query API](https://posthog.com/docs/api/queries)
- [PostHog Cohorts](https://posthog.com/docs/data/cohorts)
- [Mixpanel Funnels API](https://developer.mixpanel.com/reference/funnel-events)
- [Mixpanel JQL Query API](https://developer.mixpanel.com/reference/query-api)
- [Amplitude Funnels API](https://amplitude.com/docs/apis/analytics)
- [Pendo Analytics docs](https://help.pendo.io/resources/support-library/analytics/index)
- [Heap funnels](https://help.heap.io/reference/funnel-reports/)
- [TTFV best practices (Userpilot blog)](https://userpilot.com/blog/time-to-value/)
- [Activation metrics (Reforge)](https://www.reforge.com/blog/activation-metric)
