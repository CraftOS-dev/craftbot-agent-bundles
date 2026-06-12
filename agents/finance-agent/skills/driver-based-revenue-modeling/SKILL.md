<!--
Source: https://baremetrics.com/blog/saas-financial-model
Source: https://foresight.is/standard-financial-model/
Source: https://founderpath.com/blog/saas-financial-model
Reference role.md: "Driver-based revenue playbook"
-->

# Driver-based revenue modeling — SaaS / e-com / marketplace

Builds the revenue forecast that feeds the three-statement model. Lead with cohort logic; track per-segment, per-channel. 2026 standard: monthly cohort tracking, segment-level unit economics, channel-level CAC attribution. The output here plugs into `three-statement-financial-model-tied` (Revenue section).

## When to use

- Forecasting subscription / transaction / GMV revenue for the next 12-60 months.
- Stress-testing pricing changes, churn assumptions, or sales-motion shifts.
- Diagnosing where revenue growth comes from (logos vs ACV vs expansion).
- Sizing a Series A/B raise based on the next $XM-ARR plan.
- Trigger phrases: "revenue model", "cohort revenue", "ARR build", "NRR roll", "GMV model", "marketplace take-rate model".

NOT for: total model tying (use `three-statement-financial-model-tied`); CAC / LTV (use `ltv-cohort-strategic`).

## Setup

```bash
uvx --with pandas --with numpy --with openpyxl python -c "import pandas; print(pandas.__version__)"

# Stripe Sigma for revenue + churn cohorts
export STRIPE_API_KEY="<from Stripe Dashboard → Developers>"

# PostHog / Mixpanel / Amplitude for behavioral cohort retention
export POSTHOG_API_KEY="<PostHog Project Settings>"
```

## The three motion archetypes

### SaaS — subscription revenue

```
ARR(t) = ARR(t-1) × NRR + (New Logos × ACV)
       = Net retention applied to existing book + new acquisition

NRR = (Start MRR + expansion - churn - contraction) / Start MRR
```

### E-commerce — transactional revenue

```
Revenue(t) = Sessions × Conversion × AOV × Repeat Rate Adjustment
Sessions = Paid sessions + Organic + Direct + Email + Referral
Repeat Rate = 1 + (avg orders per customer beyond first - 1) × probability
```

### Marketplace — take-rate × GMV

```
Net Revenue = GMV × Take Rate
GMV = Active Buyers × Avg Orders/Buyer × Avg Order Value
```

## Common recipes

### Recipe 1 — SaaS cohort triangle from Stripe Sigma

```sql
WITH cohorts AS (
  SELECT customer_id, DATE_TRUNC('month', MIN(subscription_started_at)) AS cohort_month
  FROM subscriptions GROUP BY customer_id
),
monthly_mrr AS (
  SELECT s.customer_id, DATE_TRUNC('month', s.invoice_date) AS active_month,
         SUM(s.subtotal_amount)/100.0 AS mrr
  FROM invoices s
  WHERE s.status = 'paid' AND s.billing_cycle = 'monthly'
  GROUP BY 1, 2
)
SELECT c.cohort_month, m.active_month,
       DATE_DIFF('month', c.cohort_month, m.active_month) AS months_since,
       SUM(m.mrr) AS cohort_mrr
FROM cohorts c JOIN monthly_mrr m USING (customer_id)
GROUP BY 1, 2, 3 ORDER BY 1, 2;
```

### Recipe 2 — Build SaaS ARR forecast (Python)

```python
import pandas as pd

def forecast_arr(starting_arr, nrr_monthly, new_logos_per_month, acv, months=36):
    rows = []
    arr = starting_arr
    for m in range(1, months + 1):
        retained = arr * nrr_monthly
        new = new_logos_per_month * acv
        arr = retained + new
        rows.append({"month": m, "retained_arr": retained, "new_arr": new, "ending_arr": arr})
    return pd.DataFrame(rows)

nrr_monthly = 1.18 ** (1/12)
df = forecast_arr(starting_arr=4_200_000, nrr_monthly=nrr_monthly, new_logos_per_month=22, acv=24_000)
print(df.tail())
```

### Recipe 3 — Sales capacity model (constrains new logos)

```python
def sales_capacity(num_aes, quota_per_ae_annual, ramp_months=4, productivity_factor=0.7):
    full_capacity = num_aes * quota_per_ae_annual * productivity_factor
    return full_capacity / 12

cap = sales_capacity(num_aes=8, quota_per_ae_annual=600_000)
print(f"Monthly new ARR capacity: ${cap:,.0f}")
```

### Recipe 4 — E-commerce funnel model

```python
def ecom_revenue(sessions_per_channel, conv_rate, aov, repeat_orders_per_buyer):
    total_sessions = sum(sessions_per_channel.values())
    orders = total_sessions * conv_rate
    new_customers = orders / (1 + repeat_orders_per_buyer)
    repeat_orders = orders - new_customers
    return {"sessions": total_sessions, "orders": orders,
            "new_customers": new_customers, "repeat_orders": repeat_orders,
            "revenue": orders * aov}

print(ecom_revenue(
    sessions_per_channel={"paid": 120_000, "organic": 85_000, "email": 32_000, "direct": 28_000},
    conv_rate=0.024, aov=78, repeat_orders_per_buyer=1.4
))
```

### Recipe 5 — Marketplace GMV → Net Revenue

```python
def marketplace_revenue(active_buyers, orders_per_buyer, aov, take_rate):
    gmv = active_buyers * orders_per_buyer * aov
    return {"GMV": gmv, "take_rate": take_rate, "net_revenue": gmv * take_rate}

print(marketplace_revenue(active_buyers=14_500, orders_per_buyer=3.2, aov=140, take_rate=0.14))
```

### Recipe 6 — Cohort-based churn fit (lifelines)

```python
from lifelines import KaplanMeierFitter
import pandas as pd

df = pd.read_csv("customer_lifetimes.csv")  # months_active, churned (0/1)
kmf = KaplanMeierFitter()
kmf.fit(durations=df.months_active, event_observed=df.churned)
print(kmf.median_survival_time_)  # median lifetime in months
```

### Recipe 7 — Per-segment ARPU + churn split

```python
customers = pd.read_csv("customers.csv")  # id, segment, mrr, churned_at
segment_stats = customers.groupby("segment").agg(
    arpu_monthly=("mrr", "mean"),
    customer_count=("id", "count"),
    churn_rate_monthly=("churned_at", lambda x: x.notna().sum() / len(x) / 12)
)
print(segment_stats)
```

### Recipe 8 — Expansion / contraction tracker

```python
def classify_mrr_change(mrr_prev, mrr_curr):
    if mrr_prev == 0 and mrr_curr > 0: return "new"
    if mrr_prev > 0 and mrr_curr == 0: return "churn"
    if mrr_curr > mrr_prev: return "expansion"
    if mrr_curr < mrr_prev: return "contraction"
    return "stable"
```

### Recipe 9 — Net New ARR waterfall

```
Starting ARR:         $4,200,000
+ New Logo ARR:         $528,000
+ Expansion ARR:        $186,000
- Contraction ARR:      ($42,000)
- Churned ARR:          ($96,000)
= Ending ARR:         $4,776,000
Net New ARR:            $576,000
NRR (excl new):           113%
```

### Recipe 10 — Stripe Sigma NRR query

```sql
WITH base AS (
  SELECT customer_id, SUM(amount)/100.0 AS start_mrr
  FROM subscription_line_items WHERE active_at = '2025-06-01'
  GROUP BY 1
),
end_state AS (
  SELECT customer_id, COALESCE(SUM(amount), 0)/100.0 AS end_mrr
  FROM subscription_line_items WHERE active_at = '2026-06-01'
  GROUP BY 1
)
SELECT SUM(b.start_mrr) AS start_book, SUM(e.end_mrr) AS end_book,
       SUM(e.end_mrr) / SUM(b.start_mrr) AS nrr_ttm
FROM base b LEFT JOIN end_state e USING (customer_id);
```

## Examples

### Example 1: Series A revenue model — $4M ARR → $15M plan

**Goal:** 24-month plan; what NRR + logos × ACV gets to $15M ARR EoY2.

**Steps:**
1. Recipe 1 → cohort triangle, fit current NRR (118% TTM).
2. Recipe 3 → sales capacity model; how many AEs needed.
3. Recipe 2 → forecast ARR forward; iterate logos/ACV until $15M EoY2.
4. Pressure-test sensitivity (if NRR drops to 105%).
5. Document driver assumptions in Drivers tab.

**Result:** Concrete monthly ARR plan with named assumptions.

### Example 2: Pricing change impact

**Goal:** Raise ACV $24K → $30K; model NRR + churn impact.

**Steps:**
1. Recipe 1 cohort triangle at $24K baseline.
2. Apply elasticity (SaaS 0.3-0.6 absolute churn lift per 25% price increase).
3. Cohort-segment impact (SMB more sensitive than Enterprise).
4. Recipe 2 with new ACV + elevated churn first 6 months.
5. Compare 12-month ARR delta vs baseline.

**Result:** Quantified net ARR gain (or loss) from price move.

## Edge cases / gotchas

- **ARR vs bookings:** ARR = active monthly run-rate × 12. Annual prepay is cash, not ARR.
- **Cohort vs aggregate NRR:** Same-month-cohort differs from book NRR. Be explicit.
- **Churn timing:** Stripe records at cancel-at; align to reporting convention.
- **Free trials:** Don't count in MRR until conversion. Track as pipeline.
- **Multi-year deals:** $300K 3-yr = $100K ARR, not $300K.
- **Usage-based revenue:** ARR proxy = trailing 12-month, not run-rate of last month.
- **Marketplace take-rate creep:** Raising erodes seller trust; model GMV push-back.
- **Sales ramp time:** New AEs at 0%/25%/50%/75%/100% over months 1-5. Don't assume instant.
- **E-com seasonality:** Holiday Q4 = 40-60% of annual for many DTC. Don't flat-average.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions.**

## Sources

- Baremetrics SaaS model: https://baremetrics.com/blog/saas-financial-model
- Foresight Standard Model: https://foresight.is/standard-financial-model/
- Founderpath SaaS model: https://founderpath.com/blog/saas-financial-model
- Bessemer 2026 SaaS Metrics: https://beancount.io/blog/2026/05/10/saas-metrics-founders-must-track-2026-ltv-cac-nrr-churn-cac-payback-benchmarks-guide
- Eagle Rock CFO Benchmarks: https://www.eaglerockcfo.com/blog/research/saas-finance-metrics-benchmarks
- Stripe Sigma: https://docs.stripe.com/sigma
- PostHog cohorts: https://posthog.com/docs/product-analytics/cohorts
- lifelines: https://lifelines.readthedocs.io/

## Related skills

- `three-statement-financial-model-tied` — receives Revenue output.
- `ltv-cohort-strategic` — LTV from these cohorts.
- `scenario-planning-monte-carlo` — sensitizes drivers.
