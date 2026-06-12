<!--
Source: https://beancount.io/blog/2026/05/10/saas-metrics-founders-must-track-2026-ltv-cac-nrr-churn-cac-payback-benchmarks-guide
Source: https://www.eaglerockcfo.com/blog/research/saas-finance-metrics-benchmarks
Source: https://www.saasmag.com/saas-capital-efficiency-metrics/
Source: https://www.bvp.com/atlas/the-burn-multiple
Reference role.md: "Unit economics playbook"
-->

# SaaS unit economics — CAC / LTV / NRR / Rule of 40 / Magic Number / Burn Multiple

Computes the SaaS metrics that matter for investor / board / internal decisions. Benchmarked against Bessemer + SaaS Capital + Eagle Rock CFO 2026 data.

## When to use

- Monthly metric pack for investor update.
- Quarterly board prep.
- Pre-fundraise: which metrics support / hurt valuation.
- Pricing change or sales-motion change: track impact on unit economics.
- Hiring / S&M budget decisions: how do they impact payback and burn multiple.
- Trigger phrases: "NRR", "CAC payback", "Rule of 40", "Magic Number", "burn multiple", "LTV:CAC", "unit economics", "SaaS metrics".

NOT for: cash runway (use `runway-burn-analysis`); revenue recognition (use `stripe-revenue-recognition-asc606`).

## Setup

Data sources:

```bash
# MRR/ARR + churn — Stripe MCP (default skill)
# Cohort retention — posthog-mcp / mixpanel-mcp (catalog)
# S&M spend — xero-mcp GL (filter to S&M cost centers)
# CRM funnel — zoho-crm or HubSpot or Salesforce via cli-anything
```

No env vars beyond what those skills require.

## The 2026 SaaS metrics stack (definitions + benchmarks)

| Metric | Formula | Healthy 2026 | Elite 2026 | Source |
|---|---|---|---|---|
| ARR | MRR × 12 | — | — | Stripe |
| Gross margin | (Revenue − COGS) / Revenue | > 75% | > 80% | P&L |
| **CAC** | S&M spend / new logos acquired | — | — | GL + CRM |
| **CAC payback (months)** | CAC / (ARPU × gross margin) | < 18 | < 12 | computed |
| **LTV** | (ARPU × gross margin) / churn% | — | — | computed |
| **LTV:CAC** | LTV / CAC | ≥ 3:1 | ≥ 5:1 | computed |
| **NRR (net revenue retention)** | (Start MRR + expansion − churn − contraction) / Start MRR | ≥ 100% | ≥ 120% | cohort |
| **GRR (gross revenue retention)** | (Start MRR − churn − contraction) / Start MRR | ≥ 90% | ≥ 95% | cohort |
| **Magic Number** | (ΔARR × 4) / S&M spend | > 0.75 | > 1.5 | computed |
| **Rule of 40** | Growth% + EBITDA% | ≥ 40 | ≥ 60 | computed |
| **Burn Multiple** | Net burn / net new ARR | < 1.5 | < 1.0 | computed |
| **ARR per FTE** | ARR / headcount | — | improving YoY | HRIS + Stripe |

### 2026 stage-graded targets (Eagle Rock CFO)

| Stage | NRR | GM | Rule of 40 | Burn Multiple |
|---|---|---|---|---|
| Seed | 90-100% | 65-75% | growth only | 2.0-3.0 |
| Series A | 100-110% | 70-78% | 25-40 | 1.5-2.0 |
| Series B | 110-120% | 75-80% | 40-50 | 1.0-1.5 |
| Series C+ | 115-125%+ | 78-82% | 50-60 | < 1.0 |

## Common recipes

### Recipe 1 — Pull MRR / ARR from Stripe

```bash
curl -G https://api.stripe.com/v1/billing/metering/event_summaries \
  -u $STRIPE_API_KEY: \
  -d "metric_name=mrr" \
  -d "start_time=$(date -d '2026-06-01' +%s)" \
  -d "end_time=$(date -d '2026-06-30' +%s)"
```

Or Stripe Sigma SQL:
```sql
SELECT
  date_trunc('month', invoice_date) AS month,
  SUM(subtotal_amount) / 100 AS mrr
FROM invoices
WHERE status = 'paid' AND billing_cycle = 'monthly'
GROUP BY 1 ORDER BY 1;
```

### Recipe 2 — Compute CAC

```python
# CAC = Total S&M spend / new logos acquired
sm_spend_q = xero.reports.profit_and_loss(
  fromDate="2026-04-01", toDate="2026-06-30",
  trackingCategoryId="$SM_TRACKING_ID"  # filter to S&M cost center
).total

new_logos_q = crm.opportunities(
  stage="Closed Won",
  closed_date__between=("2026-04-01","2026-06-30"),
  is_new_logo=True
).count

cac = sm_spend_q / new_logos_q if new_logos_q > 0 else float('inf')
print(f"CAC: ${cac:,.0f}")
```

### Recipe 3 — CAC payback months

```python
arpu_monthly = mrr / customer_count           # avg revenue per user, monthly
gross_margin_pct = 0.78
cac_payback_months = cac / (arpu_monthly * gross_margin_pct)
print(f"CAC payback: {cac_payback_months:.1f} months")
# Benchmark: <12 elite | <18 healthy | >24 → ICP / sales-motion issue
```

### Recipe 4 — LTV + LTV:CAC

```python
monthly_churn_rate = 0.015  # 1.5%/mo logo churn
ltv = (arpu_monthly * gross_margin_pct) / monthly_churn_rate
ltv_cac = ltv / cac
print(f"LTV: ${ltv:,.0f} | LTV:CAC: {ltv_cac:.1f}:1")
# Benchmark: ≥3:1 healthy | ≥5:1 elite
```

### Recipe 5 — NRR + GRR (net + gross revenue retention)

```python
# Cohort: customers active at start of period
start_mrr = mrr_active_at("2025-06-01")  # MRR sum from a year ago
end_mrr_from_cohort = mrr_active_today_from_cohort  # what those customers pay today

expansion = sum_of_expansion_mrr_in_year
contraction = sum_of_contraction_mrr_in_year
churn = sum_of_churn_mrr_in_year

# NRR = (start + expansion − churn − contraction) / start
nrr = (start_mrr + expansion - churn - contraction) / start_mrr

# GRR = (start − churn − contraction) / start  (no expansion)
grr = (start_mrr - churn - contraction) / start_mrr

print(f"NRR: {nrr:.1%} | GRR: {grr:.1%}")
# 2026 benchmarks: NRR 100% healthy, 120% elite; GRR 90% healthy, 95% elite
```

### Recipe 6 — Magic Number

```python
# Magic Number = (Current ARR − Prior ARR) × 4 / S&M spend
# Quarterly metric; measures S&M efficiency
arr_q_end = 4_200_000
arr_q_start = 3_750_000
sm_spend_q = 320_000

magic_number = (arr_q_end - arr_q_start) * 4 / sm_spend_q
print(f"Magic Number: {magic_number:.2f}")
# Benchmark: >0.75 healthy | >1.5 elite | <0.5 = inefficient sales motion
```

### Recipe 7 — Rule of 40

```python
def rule_of_40(growth_yoy_pct, ebitda_margin_pct):
    return growth_yoy_pct + ebitda_margin_pct

# Example: 80% growth, -25% EBITDA margin
print(f"Rule of 40: {rule_of_40(80, -25):.0f}")  # 55 → above 40 benchmark
```

### Recipe 8 — Burn Multiple

```python
def burn_multiple(net_burn_q, arr_start_q, arr_end_q):
    net_new_arr = arr_end_q - arr_start_q
    return net_burn_q / net_new_arr if net_new_arr > 0 else float('inf')

bm = burn_multiple(540_000, 3_750_000, 4_200_000)
print(f"Burn Multiple: {bm:.2f}x")
# Benchmark: <1.0 elite | <1.5 healthy | >2 → capital inefficient
```

### Recipe 9 — Full metric pack (one-shot)

```python
def full_metric_pack():
    # Data pulls
    arr = stripe_arr_now()
    arr_prior_q = stripe_arr_at("2026-03-31")
    arr_prior_y = stripe_arr_at("2025-06-30")

    mrr = arr / 12
    customer_count = stripe_active_customers()
    arpu_monthly = mrr / customer_count

    sm_q = xero_sm_spend("2026-04-01","2026-06-30")
    cac = sm_q / count_new_logos_q()
    gm = (revenue - cogs) / revenue
    cac_payback = cac / (arpu_monthly * gm)

    churn_mo = stripe_logo_churn_rate_monthly()
    ltv = (arpu_monthly * gm) / churn_mo
    ltv_cac = ltv / cac

    nrr, grr = cohort_nrr_grr()
    magic = (arr - arr_prior_q) * 4 / sm_q
    growth_yoy = (arr - arr_prior_y) / arr_prior_y * 100
    ebitda_margin = ebitda / revenue * 100
    rule_of_40 = growth_yoy + ebitda_margin
    net_burn_q = burn_q()
    bm = net_burn_q / (arr - arr_prior_q)

    headcount = hris.headcount()
    arr_per_fte = arr / headcount

    return {
      "ARR": arr,
      "Gross Margin": gm,
      "CAC": cac,
      "CAC Payback (months)": cac_payback,
      "LTV": ltv,
      "LTV:CAC": ltv_cac,
      "NRR": nrr,
      "GRR": grr,
      "Magic Number": magic,
      "Rule of 40": rule_of_40,
      "Burn Multiple": bm,
      "ARR per FTE": arr_per_fte,
    }
```

### Recipe 10 — Improvement levers by metric

```python
# When a metric is below benchmark, surface concrete levers
LEVERS = {
  "NRR < 100%": [
    "Build expansion motion (upsell to higher tier, cross-sell modules)",
    "Re-price existing customers at renewal (10-15% lift typical)",
    "Reduce contraction (proactive CS on downgrade signals)",
    "Reduce churn (root-cause: product gap / champion-change / pricing-shock)",
  ],
  "CAC Payback > 24 months": [
    "Tighten ICP (cut bottom-quartile lead sources)",
    "Shorten sales cycle (better qualification, smaller initial deal)",
    "Reduce S&M waste (kill underperforming channels)",
    "Raise ACV (move upmarket or bundle higher)",
  ],
  "Burn Multiple > 2.0": [
    "Pause S&M experimentation; double down on what's working",
    "Cut headcount in non-revenue functions (G&A first)",
    "Renegotiate top SaaS contracts (10-30% savings typical)",
    "Defer capex (hardware, office moves)",
  ],
  "Rule of 40 < 30": [
    "Growth deficit → increase S&M efficiency, not spend",
    "Margin deficit → COGS audit (hosting, payment fees, support staffing)",
    "Re-segment to highest-Rule-of-40 customer cohort",
  ],
  "Gross Margin < 70%": [
    "Audit COGS: hosting / 3rd-party APIs / support staffing",
    "Move free-tier customers off premium infra",
    "Consolidate vendor stack (especially LLM inference providers)",
    "Increase pricing if pricing is below market median (Tropic benchmark)",
  ],
}
```

## Examples

### Example 1: Monthly metric pack for investor update

**Goal:** 1-table snapshot for monthly Visible.vc-style update.

**Steps:**

1. Run Recipe 9 → full metric pack.
2. Compare each metric to stage-graded 2026 benchmark.
3. Color-code: green = elite, yellow = healthy, red = below.
4. Add MoM + YoY deltas.
5. Format into investor-pack table:

```
2026-06 SaaS Metrics
                  Current   MoM      YoY     Benchmark
ARR              $4.2M    +5.2%   +83%     —
Gross Margin     78.5%    +0.3pp  +2.1pp   75% (✓ healthy)
NRR              118%     -1pp    +8pp     ≥100% (✓ healthy / approaching elite)
CAC              $11,400  -8%     -15%     —
CAC Payback      14.2 mo  -1.3mo  -3.1mo   <18 (✓ healthy)
LTV:CAC          4.2:1    +0.3    +0.8     ≥3:1 (✓ healthy)
Magic Number     0.92     +0.05   +0.18    >0.75 (✓ healthy)
Rule of 40       58       +3      +12      ≥40 (✓ elite)
Burn Multiple    1.35x    -0.10   -0.40    <1.5 (✓ healthy)
```

**Result:** Investor-ready snapshot; framing favors the company without misleading.

### Example 2: NRR diagnosis — dropped from 118% to 102%

**Goal:** Identify root cause of NRR decline.

**Steps:**

1. Recompute NRR (Recipe 5) by cohort + segment.
2. Decompose: was the drop driven by churn ↑, contraction ↑, or expansion ↓?
3. Pull churn cohort from PostHog: which customers churned, when, root cause from CSM notes.
4. Cross-tab churn against segments: SMB vs Mid-market vs Enterprise.
5. If concentrated in SMB → expected, take action on tier-gating; if concentrated in Mid-market → flag urgent (largest revenue contributors).
6. Surface levers (Recipe 10 "NRR < 100%" lever set).
7. Founder + Head of CS pick top 2-3 actions.

**Result:** NRR drop attributed to 4 mid-market logos churning in Q2 — same root cause (pricing + competitor switch). Concrete plan to retain remaining at-risk cohort.

## Edge cases / gotchas

- **ARR vs MRR conventions:** ARR = month-end run-rate × 12. Not cumulative bookings, not pipeline. Use the same convention every month.
- **Cohort definitions:** NRR can be calculated by acquisition month, year, customer segment, or by company. Pick one and stick with it. Cross-period comparison only valid with same definition.
- **Churn definition:** logo churn (count of customers) vs revenue churn (MRR). Both matter; report both.
- **CAC denominator:** "new logos acquired" = closed-won deals from net new logos. Exclude expansion deals from existing customers; they're not new acquisitions.
- **Magic Number vs CAC payback:** they measure overlapping but distinct things. Magic Number is annualized; CAC payback is months. Don't conflate.
- **Rule of 40 EBITDA:** can use adjusted EBITDA (add back SBC), but be consistent and disclose. Bessemer typically uses unadjusted for benchmarks.
- **Burn Multiple denominator:** "net new ARR" can be gross new vs net new. Bessemer uses net new (= gross new − churned). Disclose if you use gross.
- **Quarterly vs annualized:** Magic Number × 4 annualizes a quarterly figure; some sources use monthly × 12. Standardize.
- **Stage benchmarks drift:** the 2026 benchmarks are stricter than 2021 due to "efficiency era". Use current vintage for board comparisons.
- **Don't game metrics:** annual prepays inflate "ARR" if you count cash. ARR = run-rate of current subscriptions; not cash collected.
- **Headcount conventions:** fully-loaded FTE only (no contractors counted as 0.5). Same convention across quarters.

## Sources

- 2026 SaaS metrics guide: https://beancount.io/blog/2026/05/10/saas-metrics-founders-must-track-2026-ltv-cac-nrr-churn-cac-payback-benchmarks-guide
- Eagle Rock CFO benchmarks: https://www.eaglerockcfo.com/blog/research/saas-finance-metrics-benchmarks
- SaaS Capital efficiency: https://www.saasmag.com/saas-capital-efficiency-metrics/
- Bessemer Burn Multiple: https://www.bvp.com/atlas/the-burn-multiple
- SaaStr — Magic Number: https://www.saastr.com/the-saas-magic-number-explained/
- Stripe Sigma: https://docs.stripe.com/sigma
- PostHog cohorts: https://posthog.com/docs/product-analytics/cohorts

## Related skills

- `runway-burn-analysis` — burn multiple connects here
- `stripe-revenue-recognition-asc606` — feeds ARR / MRR
- `causal-mosaic-financial-modeling` — Rule of 40 is a model output
- `investor-update-monthly-quarterly` — uses Recipe 9 output
- `cogs-margin-improvement-analysis` — gross margin levers
