<!--
Source: https://stripe.com/docs/api/subscriptions + https://developers.hubspot.com/docs/api/crm/deals + https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/
-->
# NRR / GRR — Net & Gross Revenue Retention — SKILL

Compute Net Revenue Retention and Gross Revenue Retention from Stripe subscriptions + CRM deal stage + Postgres warehouse cohorts. Materialize monthly per-cohort views, produce xlsx workbooks for finance, slice-and-dice by tier/vertical/CSM for board summaries. NRR > 115%, GRR > 90% are SaaS best-in-class targets.

## When to use

- **Board / investor reporting** — monthly NRR/GRR for finance dashboard.
- **Cohort drilldown** — "Why did Q2 2024 cohort underperform Q1 2024?"
- **Tier comparison** — Enterprise NRR vs Growth vs Starter.
- **CSM book performance** — average NRR per CSM book of business.
- **Renewal forecast accuracy** — T-90 forecast vs actuals.
- **Annual planning** — model next year NRR under different churn/expansion assumptions.

This skill **complements** `renewal-management-90-day-prep` (which feeds individual renewal data) and `expansion-opportunity-identification` (which drives the expansion side of NRR).

Trigger phrases: "NRR", "GRR", "revenue retention", "cohort retention", "expansion ARR", "churn ARR", "contraction".

## Setup

```bash
# Stripe subscriptions
# stripe-mcp wired in agent.yaml

# CRM (deal-stage cohort)
export HUBSPOT_TOKEN="<pat>"
export SALESFORCE_DOMAIN="acme.my.salesforce.com"
export SALESFORCE_TOKEN="<oauth>"

# Postgres warehouse
# postgresql-mcp wired in agent.yaml
```

Workspace prerequisites:
- Postgres tables: `stripe_invoices`, `stripe_subscriptions`, `crm_deals`, `customers` (with `cohort_month`, `tier`, `vertical`, `csm_owner`).
- dbt model (or raw SQL) running nightly that materializes `customer_revenue_monthly`.
- Standard NRR/GRR definitions agreed with finance-controller (which one team uses sometimes varies on contraction definition).

## Definitions

```
Starting MRR (period start) = sum of MRR at month start
Expansion MRR = upsell + seat expansion + multi-product purchases
Contraction MRR = downgrades + seat reduction (not churn)
Churn MRR = fully cancelled subscriptions

NRR = (Starting + Expansion - Contraction - Churn) / Starting
GRR = (Starting - Contraction - Churn) / Starting     ; expansion stripped
```

NRR can exceed 100%. GRR cannot. Best-in-class SaaS: NRR >= 115%, GRR >= 90%.

## Common recipes

### Recipe 1: Materialize monthly revenue per customer

```sql
-- Run nightly: customer_revenue_monthly
CREATE OR REPLACE VIEW customer_revenue_monthly AS
SELECT
  date_trunc('month', period_start) AS month,
  customer_id,
  sum(amount_decimal) / 100.0 AS mrr,
  count(*) AS invoices,
  array_agg(DISTINCT line_item_product) AS products
FROM stripe_invoices
WHERE status = 'paid'
GROUP BY 1, 2;
```

### Recipe 2: Cohort definition

```sql
-- customer_cohorts: bucket each customer to their signup month
CREATE OR REPLACE VIEW customer_cohorts AS
SELECT
  customer_id,
  date_trunc('month', signup_date) AS cohort_month,
  tier,
  vertical,
  csm_owner
FROM customers;
```

### Recipe 3: Cohort revenue trajectory

```sql
SELECT
  cc.cohort_month,
  rev.month,
  count(DISTINCT cc.customer_id) AS active_customers,
  sum(rev.mrr) AS cohort_mrr,
  lag(sum(rev.mrr)) OVER (PARTITION BY cc.cohort_month ORDER BY rev.month) AS prev_mrr,
  sum(rev.mrr) / nullif(lag(sum(rev.mrr)) OVER (PARTITION BY cc.cohort_month ORDER BY rev.month), 0) AS m_over_m_retention
FROM customer_cohorts cc
JOIN customer_revenue_monthly rev USING (customer_id)
GROUP BY cc.cohort_month, rev.month
ORDER BY cc.cohort_month, rev.month;
```

### Recipe 4: NRR computation (full formula)

```sql
WITH revenue_movement AS (
  SELECT
    cur.month,
    cur.customer_id,
    cur.mrr AS current_mrr,
    prev.mrr AS prev_mrr,
    CASE
      WHEN prev.mrr IS NULL THEN 'new'
      WHEN prev.mrr > 0 AND cur.mrr IS NULL THEN 'churn'
      WHEN cur.mrr > prev.mrr THEN 'expansion'
      WHEN cur.mrr < prev.mrr THEN 'contraction'
      ELSE 'flat'
    END AS movement,
    coalesce(cur.mrr, 0) - coalesce(prev.mrr, 0) AS delta
  FROM customer_revenue_monthly cur
  FULL OUTER JOIN customer_revenue_monthly prev
    ON prev.customer_id = cur.customer_id
   AND prev.month = cur.month - INTERVAL '1 month'
)
SELECT
  month,
  sum(prev_mrr) FILTER (WHERE movement IN ('flat', 'expansion', 'contraction', 'churn')) AS starting_mrr,
  sum(delta) FILTER (WHERE movement = 'expansion') AS expansion_mrr,
  abs(sum(delta) FILTER (WHERE movement = 'contraction')) AS contraction_mrr,
  abs(sum(delta) FILTER (WHERE movement = 'churn')) AS churn_mrr,
  (sum(prev_mrr) FILTER (WHERE movement IN ('flat', 'expansion', 'contraction', 'churn'))
   + sum(delta) FILTER (WHERE movement = 'expansion')
   - abs(sum(delta) FILTER (WHERE movement = 'contraction'))
   - abs(sum(delta) FILTER (WHERE movement = 'churn')))
  / nullif(sum(prev_mrr) FILTER (WHERE movement IN ('flat', 'expansion', 'contraction', 'churn')), 0)
  AS nrr,
  (sum(prev_mrr) FILTER (WHERE movement IN ('flat', 'expansion', 'contraction', 'churn'))
   - abs(sum(delta) FILTER (WHERE movement = 'contraction'))
   - abs(sum(delta) FILTER (WHERE movement = 'churn')))
  / nullif(sum(prev_mrr) FILTER (WHERE movement IN ('flat', 'expansion', 'contraction', 'churn')), 0)
  AS grr
FROM revenue_movement
GROUP BY month
ORDER BY month;
```

### Recipe 5: NRR by cohort

```sql
SELECT
  cc.cohort_month,
  date_trunc('month', cur.month) AS current_month,
  date_part('month', age(cur.month, cc.cohort_month))::int AS month_n,
  -- Same NRR math as Recipe 4 but partitioned by cohort
  ...
FROM customer_cohorts cc
JOIN customer_revenue_monthly cur USING (customer_id)
WHERE cur.month <= now()
GROUP BY cc.cohort_month, date_trunc('month', cur.month);
```

### Recipe 6: NRR by tier

```sql
SELECT
  cc.tier,
  cur.month,
  -- Recipe 4 math, partitioned by tier
  ...
FROM customer_cohorts cc
JOIN customer_revenue_monthly cur USING (customer_id)
GROUP BY cc.tier, cur.month;
```

Enterprise NRR usually highest (>120%), Growth ~110%, Starter <100%. Use to set per-tier targets.

### Recipe 7: Pull deal-stage cohorts from HubSpot

```bash
# Customers in Closed Won this quarter
curl -sS "https://api.hubapi.com/crm/v3/objects/deals/search" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "filterGroups": [{
      "filters": [
        {"propertyName": "dealstage", "operator": "EQ", "value": "closedwon"},
        {"propertyName": "closedate", "operator": "GTE", "value": "1717200000000"}
      ]
    }],
    "properties": ["amount", "closedate", "dealtype", "hubspot_owner_id"],
    "limit": 100
  }'
```

Tag `dealtype` for expansion/renewal/new logo to slice Recipe 4 properly.

Doc: https://developers.hubspot.com/docs/api/crm/deals

### Recipe 8: Pull Salesforce expansion via SOQL

```bash
curl -sS "https://$SALESFORCE_DOMAIN/services/data/v59.0/query?q=SELECT+Id,Account.Name,Amount,CloseDate,Type+FROM+Opportunity+WHERE+CloseDate=THIS_QUARTER+AND+StageName=%27Closed+Won%27+AND+Type+IN+(%27Expansion%27,%27Upsell%27)" \
  -H "Authorization: Bearer $SALESFORCE_TOKEN" | jq '.records'
```

### Recipe 9: Build the xlsx workbook for finance

```python
# xlsx skill
workbook = xlsx.create()
workbook.add_sheet("Summary",
    data=[
        ["Metric", "M-2", "M-1", "M-0", "YTD"],
        ["NRR", 0.118, 0.121, 0.119, 0.119],
        ["GRR", 0.92, 0.93, 0.91, 0.92],
        ["Expansion MRR", 45000, 52000, 58000, ...],
        ["Contraction MRR", -8000, -7500, -9200, ...],
        ["Churn MRR", -12000, -11000, -14000, ...],
    ],
)
workbook.add_sheet("By Cohort", data=cohort_table_from_recipe_5)
workbook.add_sheet("By Tier", data=tier_table_from_recipe_6)
workbook.add_sheet("Raw Movement", data=movement_table_from_recipe_4)
workbook.save("nrr_grr_2026Q2.xlsx")
```

### Recipe 10: 3-slide board pptx summary

Slide 1: NRR trend (12-month line chart) + headline number + YoY delta.
Slide 2: Cohort drilldown - heatmap of NRR by cohort/age.
Slide 3: Outlook - next-quarter forecast + risks (top 3 at-risk renewals by ARR).

Use `pptx` skill `populate_from_template`.

### Recipe 11: Renewal forecast accuracy

```sql
SELECT
  date_trunc('month', forecast_date) AS forecast_month,
  count(*) AS forecasts,
  count(*) FILTER (WHERE forecast_classification = actual_outcome) AS correct,
  100.0 * count(*) FILTER (WHERE forecast_classification = actual_outcome) / count(*)::numeric AS accuracy_pct
FROM renewal_forecasts
WHERE forecast_date >= now() - INTERVAL '1 year'
  AND actual_outcome IS NOT NULL
GROUP BY 1 ORDER BY 1;
```

Target: 95% T-90 forecast accuracy.

### Recipe 12: Net new MRR ledger (Stripe-driven)

```bash
# Each event becomes a row in revenue_movement
stripe events list \
  --type=customer.subscription.created \
  --type=customer.subscription.updated \
  --type=customer.subscription.deleted \
  --created.gte=$(date -u -d '7 days ago' +%s) \
  --limit=100 | jq '.data[] | {id, type, created, customer: .data.object.customer, mrr_change: ...}'
```

(Via `stripe-mcp events_list`.) Webhook-fed in production.

## Examples

### Example 1: Monthly finance report (zero-touch)

**Goal:** First business day of month, finance gets the NRR/GRR workbook.

**Steps:**
1. Recipe 1 + 2 materialized nightly.
2. 1st of month, 06:00 UTC: Recipe 4 + 5 + 6 run.
3. Recipe 9 builds xlsx.
4. `gmail-mcp` emails xlsx + 3-line summary to finance + CS leadership.
5. Recipe 10 builds 3-slide pptx for board pack.

**Result:** Finance has fresh NRR/GRR by 06:30 UTC monthly.

### Example 2: Cohort underperformance diagnosis

**Goal:** Q2 2024 cohort NRR at 98%, vs Q1 2024 at 115%. Why?

**Steps:**
1. Recipe 5 - drill into Q2 2024 cohort by month_n.
2. Cross-reference: which customers churned/contracted; were they predominantly one tier/vertical?
3. Pull onboarding TTFV per customer (via `ramp-to-value-tracking`).
4. Hypothesis: Q2 2024 cohort was 60% self-serve onboarding (we switched in May); TTFV was 18d vs Q1's 9d.
5. Recommend: re-enable CSM-led onboarding for Growth tier.

**Result:** Data-backed product/process decision.

## Edge cases / gotchas

- **Contraction vs churn taxonomy fight** — does "downgrade from $500 to $400" count as contraction or partial churn? Lock with finance-controller; don't switch mid-year.
- **Multi-currency** — Stripe normalizes to settlement currency; if you sell in EUR and GBP, FX conversion adds noise. Use month-end FX rate, document choice.
- **Annual vs monthly billing** — annual customer's MRR is contract-amortized; not all warehouses do this right. Use `stripe_subscriptions.plan.interval` to detect.
- **Customer paid late but didn't churn** — invoice failure looks like churn for a month, then recovers. Use 30-day grace period in classification.
- **Net New customers excluded from NRR** — by definition, they're not in starting MRR. Don't conflate with "growth from new logo."
- **Mid-month contract changes** — if customer goes from $1k to $2k on the 15th, was that month's MRR $1k or $1.5k or $2k? Convention: month-end snapshot.
- **Custom invoices outside Stripe** — enterprise customers on NetSuite invoicing not in Stripe. Reconcile manually or add NetSuite tap.
- **Cohort sample size** — < 30 customers in cohort = NRR is noisy; report with caveat.
- **CSM book NRR** — useful trending signal but not perf-review-grade (CSM doesn't control upsell entirely; tier mix matters). Compare like-for-like.
- **Forecast vs actuals retroactive change** — when classification changes after forecast (e.g., Yellow -> Red mid-quarter), record both for Recipe 11; don't overwrite.
- **NRR doesn't include new logo revenue** — that's a separate North Star. Don't sum them.

## Sources

- [Stripe Subscriptions API](https://stripe.com/docs/api/subscriptions)
- [Stripe Invoices API](https://stripe.com/docs/api/invoices)
- [Stripe Billing docs](https://stripe.com/docs/billing/subscriptions/overview)
- [HubSpot Deals API](https://developers.hubspot.com/docs/api/crm/deals)
- [Salesforce REST API SOQL](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_query.htm)
- [NRR vs GRR finance guide (ChartMogul)](https://chartmogul.com/blog/net-revenue-retention/)
- [Bessemer State of the Cloud NRR benchmarks](https://www.bvp.com/atlas/state-of-the-cloud-2023)
- [dbt cohort retention pattern](https://docs.getdbt.com/guides/best-practices)
