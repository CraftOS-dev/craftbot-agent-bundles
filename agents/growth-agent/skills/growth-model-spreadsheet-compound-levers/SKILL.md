<!--
Source: Sequoia Capital growth model template + Reforge growth-model frameworks + Causal.app for parameterized models
-->
# Growth Model Spreadsheet — Compound Levers SKILL

> Build a parameterized growth model spreadsheet (Sequoia / Reforge format) with 3 scenarios (base / upside / downside), input sensitivity, and live actuals pull. The numerical mirror of your growth strategy — every lever changes a downstream output, and every projection trains pattern-recognition.

## When to use

Trigger phrases:
- "Build growth model spreadsheet"
- "Forecast revenue"
- "Sensitivity analysis on growth levers"
- "What if we improve activation by X?"
- "LTV / CAC / payback period model"
- "Bottoms-up financial model"

Pair: `north-star-omtm-pirate-metrics-heart` (NSM at top of model), `attribution-last-multi-touch-mmm-meridian-robyn` (CAC inputs), `xlsx` / `google-sheets` skill (delivery), `retention-curve-churn-diagnosis-j-smile` (churn inputs).

## Setup

```bash
# Output format (pick one)
# xlsx skill — local Excel
# google-sheets skill — collaborative

# Data sources
export POSTHOG_PERSONAL_API_KEY="phx_..."
export POSTGRES_URL="postgresql://..."
```

## Canonical model structure (Sequoia / Reforge)

```text
=== INPUTS (assumptions; tunable) ===
  Visit volume / quarter
  Visit → signup % (top-of-funnel)
  Signup → activation % (in-product)
  Activation → trial-to-paid %
  ARPU (average revenue per user)
  Monthly logo churn %
  Monthly NRR (expansion - contraction - churn)
  CAC inputs:
    Total paid spend
    Total content spend
    Total sales spend (if applicable)

=== CALCULATIONS ===
  New paid customers per period
  Cumulative customers (with churn)
  MRR (with NRR applied)
  ARR (12 × MRR)
  LTV = ARPU / monthly_churn_rate (geometric series)
  Blended CAC = total_spend / new_paid_customers
  LTV:CAC ratio
  CAC payback period (months)
  Cohort MRR retention (by acquisition cohort)
  Net new ARR (new + expansion - churn)

=== OUTPUTS (3 scenarios) ===
  Base    — actuals projected forward
  Upside  — improve activation +10pp, reduce churn -1pp
  Downside — churn +2pp, conversion -5pp

=== SENSITIVITY (1pp lever change → 12-month output delta) ===
  Activation rate
  Trial → paid conversion
  NRR
  Churn
  ARPU
```

## Common recipes

### Recipe 1: Generate xlsx scaffold (Python openpyxl)

```python
from openpyxl import Workbook
wb = Workbook()

# Sheet 1: Assumptions
ws_assumptions = wb.active
ws_assumptions.title = "Assumptions"
assumptions = [
    ("Metric", "Value", "Source"),
    ("Visits / month", 50000, "GA4"),
    ("Visit → signup %", 0.05, "PostHog funnel"),
    ("Signup → activation %", 0.31, "PostHog activation skill"),
    ("Activation → paid %", 0.18, "Stripe + PostHog"),
    ("ARPU monthly", 49, "Stripe"),
    ("Logo churn % / month", 0.04, "lifelines model"),
    ("NRR % / month", 1.012, "subscription history"),
    ("CAC paid spend / month", 60000, "Meta + Google ads"),
]
for row in assumptions:
    ws_assumptions.append(row)

# Sheet 2: Calculations
ws_calc = wb.create_sheet("Calculations")
ws_calc.append(["Month", "New visits", "Signups", "Activated", "Paid", "MRR", "ARR"])

# 24-month projection
for m in range(24):
    visits = 50000 * (1 + 0.05) ** m
    signups = visits * 0.05
    activated = signups * 0.31
    paid = activated * 0.18
    # Cumulative with churn
    # ...
    ws_calc.append([m+1, visits, signups, activated, paid, paid * 49, paid * 49 * 12])

# Sheet 3: Scenarios
ws_sc = wb.create_sheet("Scenarios")
ws_sc.append(["Metric", "Base", "Upside", "Downside"])
ws_sc.append(["12-mo ARR", "=Calculations!G12", "=Calculations!G12*1.4", "=Calculations!G12*0.7"])

wb.save("growth_model.xlsx")
```

### Recipe 2: LTV calculation (the canonical)

```python
def ltv_simple(arpu_monthly, churn_rate_monthly):
    """Geometric series: LTV = ARPU / churn rate."""
    return arpu_monthly / churn_rate_monthly

# Example: $49 ARPU, 4% monthly churn
# LTV = 49 / 0.04 = $1225

def ltv_with_nrr(arpu_monthly, churn_rate_monthly, nrr_monthly_growth):
    """LTV with expansion. NRR = 1 + (expansion - churn)/start."""
    net_monthly_change = nrr_monthly_growth - 1  # e.g., 0.012 = 1.2% / mo growth
    # Modified geometric series for expansion + churn
    effective_churn = churn_rate_monthly - net_monthly_change
    if effective_churn <= 0:
        return float('inf')  # NRR > 100% + low churn = infinite LTV theoretically
    return arpu_monthly / effective_churn
```

### Recipe 3: CAC payback

```python
def cac_payback_months(cac, arpu_monthly, gross_margin_pct=0.80):
    """Months until cohort contributes back its CAC at gross-margin."""
    monthly_contribution = arpu_monthly * gross_margin_pct
    return cac / monthly_contribution

# Example: $400 CAC, $49 ARPU, 80% gross margin
# payback = 400 / (49 * 0.8) = 400 / 39.2 = 10.2 months
# Healthy: < 12 months. Best-in-class: < 6 months.
```

### Recipe 4: LTV:CAC ratio

```python
def ltv_cac(arpu, churn, cac, gross_margin=0.80):
    ltv = (arpu * gross_margin) / churn
    return ltv / cac

# Healthy: > 3:1
# Best-in-class: > 5:1
# < 3:1 = unsustainable; either reduce CAC or increase LTV
```

### Recipe 5: Sensitivity analysis

```python
def sensitivity(base_inputs, lever, range_pct):
    """Show output delta from changing one input."""
    results = {}
    for delta in [-0.05, -0.02, -0.01, 0, 0.01, 0.02, 0.05]:
        inputs = base_inputs.copy()
        inputs[lever] = base_inputs[lever] + delta
        output = compute_12mo_arr(inputs)
        results[delta] = output
    return results

# Example: how does 1pp activation rate change affect 12-mo ARR?
# Base 31% activation: $5.4M ARR
# +1pp → 32%: $5.58M (3.3% lift)
# +5pp → 36%: $6.5M (20% lift)
```

### Recipe 6: 3-scenario template (Excel formulas)

```text
Cell A1: "Activation %"
Cell B1: 0.31     // Base
Cell C1: 0.41     // Upside (+10pp)
Cell D1: 0.26     // Downside (-5pp)

Cell A2: "Trial-to-paid %"
Cell B2: 0.18
Cell C2: 0.22
Cell D2: 0.15

Cell A10: "12-mo ARR (auto)"
Cell B10: =B1*B2*<other linkage>*49*12
Cell C10: =C1*C2*<other linkage>*49*12
Cell D10: =D1*D2*<other linkage>*49*12
```

### Recipe 7: Pull actuals from PostHog (auto-populate)

```python
def actuals_pull():
    monthly_visits = posthog.query("SELECT count() FROM events WHERE event='pageview' AND ...")
    monthly_signups = posthog.query("SELECT countDistinct(person_id) FROM events WHERE event='User Signed Up' AND ...")
    monthly_activated = posthog.query(activation_sql)
    # ... etc
    return {"visits": monthly_visits, "signups": monthly_signups, ...}

# Update the spreadsheet's Assumptions sheet monthly
update_xlsx("growth_model.xlsx", "Assumptions", actuals_pull())
```

### Recipe 8: Cohort MRR retention chart

```python
import pandas as pd
import matplotlib.pyplot as plt

cohort_data = pd.read_sql("""
  SELECT
    cohort_month,
    month_offset,
    SUM(mrr) as cohort_mrr
  FROM cohort_mrr_history
  GROUP BY cohort_month, month_offset
""", db)

pivot = cohort_data.pivot(index='cohort_month', columns='month_offset', values='cohort_mrr')
# Normalize: each row / row.first
pivot_norm = pivot.div(pivot[0], axis=0)

fig, ax = plt.subplots(figsize=(12, 8))
ax.imshow(pivot_norm, cmap='RdYlGn', aspect='auto', vmin=0.5, vmax=1.5)
plt.title("Cohort MRR retention (1.0 = start of cohort)")
plt.savefig("cohort_mrr.png")
```

### Recipe 9: Causal.app live model (alternative to spreadsheet)

```text
Causal.app: cloud-based parameterized models with simulation + sharing.
Strong for stakeholder presentation + Monte Carlo (probabilistic) projection.

URL: https://www.causal.app/
Free tier sufficient for solo founders + small teams.
```

Schema mirrors the canonical structure above.

### Recipe 10: Update cadence + ownership

```text
- Actuals (Assumptions sheet): monthly auto-populate
- Scenarios (Scenarios sheet): quarterly review
- Sensitivity (Sensitivity sheet): updated when input weights change
- Major refactor: annually OR when motion changes (PLG → sales-led)

Owner: Growth lead + finance partner
Review cadence: quarterly board prep
```

### Recipe 11: Forecast vs actuals tracking

```python
# Append each month: forecast for next quarter + actual when known
tracking = pd.DataFrame({
    "month": ["2026-01", "2026-02", "2026-03"],
    "forecast_arr": [4.8e6, 5.1e6, 5.4e6],
    "actual_arr":   [4.9e6, 5.0e6, None]
})

tracking["variance_pct"] = (tracking.actual_arr - tracking.forecast_arr) / tracking.forecast_arr
# Investigate variance > 10%
```

## Examples

### Example 1: PLG B2B SaaS, $4M ARR, 12-month projection

Assumptions:
- Visits 80K/mo, growing 3% monthly
- Visit → signup 4%
- Activation 32%
- Trial → paid 18%
- ARPU $59
- Logo churn 3.5%/mo, NRR 105%

Projection: $8.2M ARR Year 1 end (base).

Sensitivity: +5pp activation → +$1.4M (17% lift). Most leveraged lever.

Plan: invest engineering hours in activation per `activation-funnel-aha-moment`. Validates in growth model.

### Example 2: DTC e-com $3M ARR

Different model:
- Visits, Visit → AOV, AOV, Repeat rate, AOV-on-repeat
- LTV = AOV × repeat_count_avg
- CAC vs LTV per cohort by source

Sensitivity: +5pp repeat rate is biggest lever for LTV expansion.

### Example 3: Pre-revenue / Seed

Use Causal.app or Reforge model with placeholder estimates.

Outputs: required activation × conversion × MRR per month to hit $1M ARR in 18 months. Drives prioritization.

## Edge cases / gotchas

- **Garbage-in-garbage-out** — assumptions sheet must reflect actuals; sloppy inputs = sloppy projections.
- **Compound effects mistaken** — improving 5 levers each by 5% does NOT yield 25% lift compounded; each affects different stages.
- **LTV without gross margin = wrong** — LTV must use contribution margin (after CoGS, support, hosting).
- **CAC excludes salaries** — many "CAC" calcs only count ad spend; fully-loaded CAC includes content team, sales salary, ops.
- **NRR > 100% means churn negative on cohort** — easy to miss in compounding; check that NRR isn't artificially smoothing churn issues.
- **Annual vs monthly billing distortion** — annual contracts show big month spikes; smooth with TTM (trailing 12-month).
- **Cohort comparability** — old cohorts had different product; can't apply old curve to new cohort. Track separately.
- **Currency** — multi-region SaaS needs FX adjustment in model.
- **Tax + commissions invisible** — exclude from MRR but include in CAC.
- **Scenario over-confidence** — "upside" assumes 3+ improvements happen simultaneously, which is unlikely. Calibrate.

## Sources

- Sequoia growth model template (classic): https://www.sequoiacap.com/article/preparing-a-board-deck/
- Reforge growth model frameworks: https://www.reforge.com/
- Causal.app: https://www.causal.app/
- ChartMogul SaaS cohorts: https://chartmogul.com/cohort-analysis/
- Brian Balfour growth model: https://brianbalfour.com/four-fits-growth-framework
- Lenny Rachitsky growth math: https://www.lennysnewsletter.com/
- ProductLed PLG metrics: https://www.productled.org/foundations/product-led-growth-metrics
- Patrick Campbell — SaaS metrics: https://www.priceintelligently.com/
