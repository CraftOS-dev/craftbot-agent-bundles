<!--
Source: https://posthog.com/docs/api/queries + https://developer.mixpanel.com/reference/query-api + https://amplitude.com/docs/apis/analytics + https://developers.heap.io/reference
-->
# Adoption Metric — Feature Usage / DAU MAU WAU — SKILL

Per-customer adoption metrics: DAU/MAU/WAU, feature adoption rate, feature breadth, login recency. Rolled up into composite AdoptionScore (0-1). Sources: PostHog HogQL (primary), Mixpanel JQL, Amplitude Chart Query, Heap. Daily writeback to CSP traits feeds health score formula. Triggers: adoption < 0.3 -> at-risk; adoption > 0.6 + sponsor active -> expansion-ready.

## When to use

- **Daily writeback** — push adoption_score to Vitally/Catalyst/Gainsight nightly.
- **At-risk adoption gate** — score < 0.3 triggers churn-save signal.
- **Expansion gate** — score > 0.6 + sponsor active triggers expansion signal.
- **QBR data prep** — DAU/MAU/WAU chart for slide 4.
- **Feature launch tracking** — feature_X adoption rate per customer.
- **Cross-customer benchmarking** — average adoption by tier.

This skill **feeds** `customer-health-scoring-vitally-catalyst-churnzero` (adoption_score = 0.40 weight in composite formula), `at-risk-identification-escalation` (low adoption signal), `expansion-opportunity-identification` (high adoption signal), and `qbr-scheduling-facilitation` (QBR slide 4).

Trigger phrases: "DAU MAU", "adoption score", "feature adoption", "WAU", "feature usage", "active users", "engagement metrics".

## Setup

```bash
# Product analytics MCPs already in agent.yaml
# posthog-mcp, mixpanel-mcp, amplitude-mcp

# Heap (alt)
export HEAP_APP_ID="<id>"
export HEAP_API_KEY="<key>"

# CSP writeback targets
export VITALLY_SUBDOMAIN="acme"
export VITALLY_API_KEY="<key>"
export CATALYST_API_KEY="<key>"
```

Workspace prerequisites:
- PostHog event taxonomy includes `customer_id` property on every event.
- Key-feature taxonomy named consistently (e.g., `key_feature_used` with `feature_name` property).
- Postgres warehouse view `adoption_metrics_daily` materializing per-customer rollup.
- CSP trait names locked: `adoption_score`, `dau_30d`, `mau_30d`, `feature_adoption_score`, `feature_breadth`.

## AdoptionScore formula

```
AdoptionScore = 0.40 * (DAU / MAU normalized)
              + 0.30 * (key_feature_adoption_rate)
              + 0.20 * (feature_breadth normalized)
              + 0.10 * (login_recency_score)
```

## Common recipes

### Recipe 1: PostHog HogQL - per-customer DAU/MAU/WAU

```sql
SELECT
  properties.customer_id AS customer_id,
  uniq(distinct_id) FILTER (WHERE timestamp >= now() - INTERVAL 1 DAY) AS dau,
  uniq(distinct_id) FILTER (WHERE timestamp >= now() - INTERVAL 7 DAY) AS wau,
  uniq(distinct_id) FILTER (WHERE timestamp >= now() - INTERVAL 30 DAY) AS mau,
  uniq(distinct_id) FILTER (WHERE timestamp >= now() - INTERVAL 30 DAY) AS total_users_30d
FROM events
WHERE timestamp >= now() - INTERVAL 30 DAY
  AND event = 'user_action'
GROUP BY properties.customer_id;
```

Doc: https://posthog.com/docs/api/queries

### Recipe 2: PostHog HogQL - feature adoption rate

```sql
SELECT
  properties.customer_id AS customer_id,
  uniq(distinct_id) FILTER (WHERE event = 'key_feature_used') * 1.0
  / nullif(uniq(distinct_id) FILTER (WHERE event = 'user_action'), 0) AS feature_adoption_rate,
  uniq(properties.feature_name) AS distinct_features_used
FROM events
WHERE timestamp >= now() - INTERVAL 30 DAY
GROUP BY properties.customer_id;
```

`feature_adoption_rate` = % of active users using key features.

### Recipe 3: PostHog HogQL - feature breadth

```sql
SELECT
  properties.customer_id,
  uniq(properties.feature_name) AS feature_breadth
FROM events
WHERE event = 'key_feature_used'
  AND timestamp >= now() - INTERVAL 30 DAY
GROUP BY properties.customer_id;
```

Normalize: divide by total key features defined (e.g., 8 -> breadth_normalized = uniq / 8).

### Recipe 4: PostHog HogQL - login recency

```sql
SELECT
  properties.customer_id,
  max(timestamp) AS last_login,
  exp(- dateDiff('day', max(timestamp), now()) / 30.0) AS login_recency_score
FROM events
WHERE event = 'login'
GROUP BY properties.customer_id;
```

Exponential decay: 30d half-life. Login today = 1.0; 30d ago = 0.37.

### Recipe 5: Mixpanel JQL alt

```bash
curl -sS "https://mixpanel.com/api/2.0/jql" \
  -u "$MIXPANEL_API_KEY:" \
  --data-urlencode 'script=function main() {
    return Events({from_date: "2026-05-01", to_date: "2026-05-31"})
      .groupByUser(["customer_id"], mixpanel.reducer.count())
      .map(g => ({customer_id: g.key[0], events: g.value}))
  }'
```

Doc: https://developer.mixpanel.com/reference/query-api

### Recipe 6: Amplitude Chart Query alt

```bash
curl -sS "https://amplitude.com/api/2/users/active" \
  -u "$AMPLITUDE_API_KEY:$AMPLITUDE_SECRET" \
  --data-urlencode 'start=20260501' \
  --data-urlencode 'end=20260531' \
  --data-urlencode 'm=active'
```

Doc: https://amplitude.com/docs/apis/analytics

### Recipe 7: Heap query alt

```bash
curl -sS "https://heapanalytics.com/api/v1/queries" \
  -H "Authorization: Bearer $HEAP_API_KEY" \
  -d '{"event": "user_action", "since": "30d_ago", "group_by": "customer_id"}'
```

Doc: https://developers.heap.io/reference

### Recipe 8: Materialize adoption_metrics_daily view

```sql
CREATE OR REPLACE VIEW adoption_metrics_daily AS
SELECT
  customer_id,
  date_trunc('day', now()) AS as_of,
  dau,
  wau,
  mau,
  (dau * 1.0 / nullif(mau, 0)) AS dau_mau,
  feature_adoption_rate,
  feature_breadth,
  feature_breadth * 1.0 / 8 AS feature_breadth_normalized,  -- assuming 8 key features
  login_recency_score,
  -- Composite score
  0.40 * least(1.0, (dau * 1.0 / nullif(mau, 0)) / 0.4)
  + 0.30 * coalesce(feature_adoption_rate, 0)
  + 0.20 * least(1.0, feature_breadth * 1.0 / 8)
  + 0.10 * coalesce(login_recency_score, 0)
  AS adoption_score
FROM (
  SELECT customer_id, dau, wau, mau, feature_adoption_rate, feature_breadth, login_recency_score
  FROM <output of Recipes 1-4 joined>
) x;
```

Schedule nightly via `postgresql-mcp` + cron.

### Recipe 9: Daily writeback to Vitally

```bash
# For each customer in adoption_metrics_daily:
curl -sS -X PUT "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/accounts/external/$CUSTOMER_ID/traits" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" \
  -d '{
    "adoption_score": 0.62,
    "dau_30d": 18,
    "mau_30d": 47,
    "wau_30d": 32,
    "dau_mau_ratio": 0.38,
    "feature_adoption_score": 0.71,
    "feature_breadth": 6
  }'
```

### Recipe 10: Catalyst writeback

```bash
curl -sS -X PATCH "https://api.catalyst.io/v1/companies/$CUSTOMER_ID/properties" \
  -H "Authorization: Bearer $CATALYST_API_KEY" \
  -d '{"properties": {"adoption_score": 0.62, "dau_mau_ratio": 0.38}}'
```

### Recipe 11: Adoption signal triggers

```sql
-- At-risk adoption (< 0.3 sustained 7d)
SELECT customer_id, avg(adoption_score) AS avg_score_7d
FROM adoption_metrics_daily
WHERE as_of >= now() - INTERVAL '7 days'
GROUP BY customer_id
HAVING avg(adoption_score) < 0.3;
```

Route to `at-risk-identification-escalation`.

```sql
-- Expansion-ready (> 0.6 + sponsor active)
SELECT a.customer_id, a.avg_score_7d, s.sponsor_last_seen_days
FROM (
  SELECT customer_id, avg(adoption_score) AS avg_score_7d
  FROM adoption_metrics_daily
  WHERE as_of >= now() - INTERVAL '7 days'
  GROUP BY customer_id
  HAVING avg(adoption_score) > 0.6
) a
JOIN sponsor_activity s USING (customer_id)
WHERE s.sponsor_last_seen_days < 14;
```

Route to `expansion-opportunity-identification`.

### Recipe 12: Per-customer adoption chart (QBR slide 4 data)

```sql
SELECT
  date_trunc('week', as_of) AS week,
  avg(dau) AS avg_dau,
  avg(wau) AS avg_wau,
  avg(mau) AS avg_mau,
  avg(feature_adoption_rate) AS avg_feature_adoption,
  avg(adoption_score) AS avg_adoption_score
FROM adoption_metrics_daily
WHERE customer_id = '$CUSTOMER_ID'
  AND as_of >= now() - INTERVAL '90 days'
GROUP BY week
ORDER BY week;
```

Pipe to `pptx` skill chart generation.

### Recipe 13: Cohort benchmarking (compare customers)

```sql
SELECT
  tier,
  count(*) AS customers,
  round(avg(adoption_score)::numeric, 2) AS avg_adoption,
  percentile_cont(0.5) WITHIN GROUP (ORDER BY adoption_score) AS p50,
  percentile_cont(0.9) WITHIN GROUP (ORDER BY adoption_score) AS p90
FROM adoption_metrics_daily a
JOIN customers c USING (customer_id)
WHERE as_of = (SELECT max(as_of) FROM adoption_metrics_daily)
GROUP BY tier
ORDER BY avg_adoption DESC;
```

Enables "your team is in 80th percentile of Enterprise tier" for QBR positioning.

## Examples

### Example 1: Nightly adoption pipeline (zero-touch)

**Goal:** Every morning, CSP has fresh adoption signals; downstream skills can act.

**Steps:**
1. 02:00 UTC: Recipes 1-4 HogQL queries run via `posthog-mcp`.
2. 02:30 UTC: Recipe 8 materializes view in Postgres.
3. 03:00 UTC: Recipe 9 / 10 writeback to CSP.
4. 03:30 UTC: Recipe 11 triggers at-risk + expansion signals.
5. 09:00 UTC: Recipes 12-13 dashboards.

**Result:** Adoption pipeline runs hands-off.

### Example 2: Feature launch tracking

**Goal:** New feature "Workflows" launched Mon; track adoption across customer base.

**Steps:**
1. Recipe 2 modified for `event = 'workflow_used'` instead of generic `key_feature_used`.
2. Day 7: 12% of customers tried it. Day 30: 31%. Plot in Notion.
3. Customers who haven't tried by Day 14 -> route to `feature-adoption-interventions`.
4. Customers who used multiple times Day 30 -> route to `customer-advocacy-case-study-reference` for "show us how you're using Workflows."

**Result:** Feature adoption tracked + interventions fire automatically.

## Edge cases / gotchas

- **DAU spikes from bots / integrations** — auto-actions from CI integrations count as DAU. Filter `properties.is_bot = false`.
- **MAU includes one-time-login users** — defined as "active in last 30d," not "engaged." Use `events >= 5 / 30d` cutoff for "engaged DAU/MAU" alongside raw counts.
- **Feature taxonomy drift** — adding a new feature retroactively changes `feature_breadth`. Maintain feature catalog as source-of-truth.
- **PostHog property cardinality limits** — `customer_id` as event property = fine; full account name = explodes cardinality.
- **Customer-level DAU vs user-level DAU** — for B2B, a "user" is a person; we measure customer-level engagement (any user in account active). Make convention explicit.
- **Multi-product customer** — adoption per product, then composite. Don't average across unrelated products.
- **Tier mix in cohort benchmarking** — Recipe 13 needs N >= 30 per tier to be meaningful.
- **Login event missing** — if you don't fire a login event explicitly, use first daily event. Document choice.
- **CSP rate limit on writeback** — 100 req/min on Vitally. Batch via Recipe 11 in `customer-health-scoring`.
- **Score volatility** — if a customer's adoption jumps from 0.4 to 0.7 day-over-day, may be data issue (event flood). Smooth with 7d rolling average for CSP trait.
- **Free-tier vs paying tier** — free-tier "adoption" doesn't translate to revenue. Don't conflate.
- **Don't expose internal scores to customer directly** — translate to plain English: "Your team is using 6 of 8 key features."

## Sources

- [PostHog HogQL Query API](https://posthog.com/docs/api/queries)
- [PostHog Cohorts](https://posthog.com/docs/data/cohorts)
- [PostHog Person Properties](https://posthog.com/docs/data/persons)
- [Mixpanel Query API JQL](https://developer.mixpanel.com/reference/query-api)
- [Mixpanel Funnels API](https://developer.mixpanel.com/reference/funnel-events)
- [Amplitude Analytics API](https://amplitude.com/docs/apis/analytics)
- [Amplitude Active Users](https://amplitude.com/docs/apis/analytics/users)
- [Heap API reference](https://developers.heap.io/reference)
- [FullStory data export](https://help.fullstory.com/hc/en-us/articles/360020623194)
- [Vitally traits API](https://docs.vitally.io/reference/accounts)
- [DAU MAU SaaS benchmarks (Mixpanel)](https://mixpanel.com/blog/dau-mau-engagement-saas/)
