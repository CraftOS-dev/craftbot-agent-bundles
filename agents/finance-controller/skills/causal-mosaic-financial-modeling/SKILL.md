<!--
Source: https://valueaddvc.com/blog/best-financial-modeling-tools-for-startups-excel-vs-runway-vs-causal-vs-mosaic
Source: https://www.cubesoftware.com/
Source: https://www.mosaic.tech/
Source: https://causal.app/
Source: https://www.drivetrain.ai/post/mosaic-competitors-and-alternatives
-->

# Causal + Mosaic + Cube + Runway — driver-based FP&A modeling

Modern financial planning tools that replace spreadsheet sprawl with driver-based, multidimensional models. Causal (Seed–Series B; acquired by LucaNet Oct 2024); Mosaic (Series C+ standard; acquired by Hibob Feb 2025); Cube (AI agent + native Excel/Sheets); Runway (UX-first early stage); Drivetrain (mid-market alt).

## When to use

- Build 3-statement model (P&L + BS + CF) with linked drivers.
- Scenario modeling (base / upside / downside).
- Headcount planning with sequenced hires and fully-loaded cost.
- Revenue forecasting by segment / product / cohort.
- Budget vs actual (BvA) variance dashboards.
- Multi-entity consolidation (Series C+).
- Trigger phrases: "build our budget", "scenario model", "what if we hire 10 engineers", "5-year forecast", "consolidate entities".

NOT for: monthly close mechanics (use `monthly-close-procedure`); ASC 606 schedules (use `stripe-revenue-recognition-asc606`); cap-table modeling (use `carta-pulley-cap-table`).

## Platform selection matrix

| Stage / need | Recommended | Why |
|---|---|---|
| Seed / pre-Series A | Causal OR xlsx | Causal cheap; xlsx universal |
| Series A → B | Causal OR Cube | Driver-based; integrate with ERP |
| Series C+, multi-entity | Mosaic OR Drivetrain | Consolidation; broader integrations |
| Excel-first team | Cube | Native Excel/Sheets — no platform shift |
| Enterprise (Series D+) | Anaplan / Vena / Workday Adaptive | Mature, expensive |
| Founder DIY | xlsx (this skill helps) | No platform required |

## Setup

### Causal

```bash
# Account at causal.app → workspace settings → API tokens
export CAUSAL_API_KEY="..."

# Public API limited; primary integration via Causal's app + CSV/Sheets sync
curl -H "Authorization: Bearer $CAUSAL_API_KEY" \
  https://api.causal.app/v1/models | jq .
```

### Mosaic

```bash
# Mosaic API: dashboard → Settings → API → Generate Token
export MOSAIC_API_KEY="..."

curl -H "Authorization: Bearer $MOSAIC_API_KEY" \
  https://app.mosaic.tech/api/v1/metrics
```

### Cube

```bash
# Cube has REST + Excel/Sheets connectors
export CUBE_API_KEY="..."
curl -H "Authorization: Bearer $CUBE_API_KEY" \
  https://api.cube.dev/v1/dimensions
```

### Runway (financial planning, not the security tool)

```bash
# Runway financial planning — runwayfp.com
# API: contact Runway team; primary interface is webapp + Notion-like docs
```

### xlsx fallback (always works)

Use the `xlsx` skill + pandas. Template structure below.

## Driver-based 3-statement model — xlsx template

### Drivers tab (single source of truth)

```
DRIVER                          BASE     UPSIDE   DOWNSIDE
Starting cash                $1,500,000  ...      ...
Starting ARR                 $2,400,000  ...      ...
ARR growth rate (annual)         100%     150%      50%
Logo churn rate (annual)          10%       5%      18%
Net revenue retention            115%     130%     100%
Avg ACV                      $   24,000  ...      ...
CAC                          $   12,000  ...      ...
Gross margin                      78%      82%      72%
S&M as % of revenue               45%      35%      55%
R&D as % of revenue               30%      25%      35%
G&A as % of revenue               15%      12%      18%
Headcount end-of-year             45        60       30
Avg fully loaded cost        $  185,000  ...      ...
```

### Revenue tab (per-month, ratable)

```
                              Jan  Feb  Mar ... Dec   YEAR
Starting MRR (M)             200K ...
+ New MRR (new logos × ACV/12)
+ Expansion MRR (existing × (NRR-1)/12)
- Churn MRR (existing × churn%/12)
= Ending MRR
× 12 = ARR (annualized)
```

### P&L tab (drivers flow through)

```
Revenue (sum monthly MRR × 12 or recognized)
- COGS (Revenue × (1 - Gross Margin))
= Gross Profit
- S&M (Revenue × S&M%)
- R&D (Revenue × R&D%)
- G&A (Revenue × G&A%)
= EBITDA
- D&A
= EBIT
- Tax
= Net Income
```

### Cash flow tab (indirect)

```
Net Income
+ D&A
+ ΔDeferred Revenue
- ΔAR (more AR = cash out)
- Capex
= Free Cash Flow
```

### Balance sheet tab (rolled)

```
Cash (prior + FCF)
AR (Revenue × DSO/30)
Deferred Revenue (annual subs × remaining months)
...
Liabilities + Equity must = Assets
```

## Common recipes

### Recipe 1 — Build a driver-based model in Causal

```python
# Causal's strength is its formula language. Conceptual flow:
# 1. Define drivers (atomic inputs with values + ranges)
# 2. Define derived metrics referencing drivers
# 3. Causal auto-builds visualizations + sensitivity

# Via API (limited):
import requests
requests.post(
  "https://api.causal.app/v1/models",
  headers={"Authorization": f"Bearer {CAUSAL_API_KEY}"},
  json={"name": "FY27 Plan", "template": "saas_3statement"}
)
# Then editing in the Causal UI is the primary workflow
```

### Recipe 2 — Scenario analysis (base/upside/downside)

```python
import pandas as pd
import numpy as np

# Pull base drivers
drivers = pd.read_excel("model.xlsx", sheet_name="Drivers")

# Define scenarios
scenarios = {
  "base":     {"growth": 1.00, "churn": 0.10, "cac": 12000},
  "upside":   {"growth": 1.50, "churn": 0.05, "cac": 10000},
  "downside": {"growth": 0.50, "churn": 0.18, "cac": 16000}
}

for name, s in scenarios.items():
    arr_end = drivers["starting_arr"][0] * (1 + s["growth"]) * (1 - s["churn"])
    new_logos = (arr_end - drivers["starting_arr"][0]) / drivers["avg_acv"][0]
    sm_spend = new_logos * s["cac"]
    print(f"{name:>10}: ARR end ${arr_end:,.0f} | S&M ${sm_spend:,.0f}")
```

### Recipe 3 — Multi-entity consolidation in Mosaic

```bash
# Pull metrics from each entity, consolidated
curl -H "Authorization: Bearer $MOSAIC_API_KEY" \
  "https://app.mosaic.tech/api/v1/metrics?metric=arr&consolidated=true&\
period=2026-Q2&entities=us,uk,emea"
```

### Recipe 4 — Headcount plan with sequencing

```python
import pandas as pd

# Hire plan
hires = pd.DataFrame([
  {"role":"Senior PMM", "function":"S&M", "start":"2026-08-01", "base":160_000, "loaded":208_000},
  {"role":"AE",         "function":"S&M", "start":"2026-09-01", "base":120_000, "loaded":156_000},
  {"role":"SWE",        "function":"R&D", "start":"2026-08-15", "base":180_000, "loaded":234_000},
  {"role":"SWE",        "function":"R&D", "start":"2026-10-01", "base":180_000, "loaded":234_000},
  # ... 20+ hires
])

# Loaded cost = base × 1.30 (US benefits + tax) — use 1.4 for offices with rent share

# Monthly flow to P&L
months = pd.date_range("2026-07-01", "2027-06-30", freq="MS")
monthly_cost = pd.DataFrame(index=months, columns=["S&M","R&D","G&A"]).fillna(0)
for _, h in hires.iterrows():
    start = pd.Timestamp(h.start)
    for m in months:
        if m >= start:
            monthly_cost.loc[m, h.function] += h.loaded / 12
print(monthly_cost.sum(axis=1).cumsum())
```

### Recipe 5 — Budget vs actual (BvA) variance

```python
budget = xero.reports.budget_summary(fromDate="2026-06-01", toDate="2026-06-30")
actual = xero.reports.profit_and_loss(fromDate="2026-06-01", toDate="2026-06-30")

bva = pd.merge(budget, actual, on="account", suffixes=("_budget","_actual"))
bva["variance"] = bva["amount_actual"] - bva["amount_budget"]
bva["variance_pct"] = bva["variance"] / bva["amount_budget"]
flagged = bva[bva["variance_pct"].abs() > 0.10]   # >10% variance threshold
print(flagged)
```

### Recipe 6 — Sensitivity (tornado chart) on burn

```python
import numpy as np
import pandas as pd

base_burn = 200_000  # monthly
drivers_sensitivity = {
  "Hire pace ±20%":      (-40_000, +40_000),
  "Gross margin ±5pp":   (-25_000, +25_000),
  "S&M efficiency ±15%": (-30_000, +30_000),
  "Hosting cost ±25%":   (-15_000, +15_000),
  "Pricing ±10%":        (-50_000, +50_000),
}

rows = []
for d, (low, high) in drivers_sensitivity.items():
    rows.append({"driver": d, "low": base_burn + low, "high": base_burn + high})
tornado = pd.DataFrame(rows).sort_values("high", ascending=False)
# Plot horizontal bars: low to high range per driver
```

### Recipe 7 — Cube to Excel (live formulas)

```python
# Cube's strength: write formulas in Excel that pull live data from finance systems
# Excel cell formula example:
# =CUBE.QUERY("ARR", "Period=Current Month", "Segment=Enterprise")
# This refreshes when the workbook opens or on demand
```

### Recipe 8 — Reforecast trigger rules

```python
# Standard rule: reforecast when YTD variance > 5%
ytd_actual = sum(actual_by_month[:6])  # H1 actual
ytd_budget = sum(budget_by_month[:6])
ytd_variance_pct = (ytd_actual - ytd_budget) / ytd_budget

if abs(ytd_variance_pct) > 0.05:
    print(f"REFORECAST TRIGGERED: YTD variance {ytd_variance_pct:.1%}")
    # Re-base H2 projections off H1 actual run-rate
```

### Recipe 9 — Causal → Xero data sync

```bash
# Causal can ingest from Google Sheets; Sheets pulls from Xero via add-on
# Workflow: Xero → G-Sheets (via xero-gsheets connector) → Causal (G-Sheets sync)
```

### Recipe 10 — Quarterly board pack auto-generation

```python
# Pull all metrics needed for board pack
metrics = {
  "ARR":          stripe_mcp.get("/v1/billing/metering/event_summaries"),
  "MRR":          stripe_arr / 12,
  "Cash":         mercury_balance,
  "Net burn":     (opening_cash - closing_cash) / 3,
  "Runway":       closing_cash / net_burn,
  "Gross margin": (revenue - cogs) / revenue,
  "Headcount":    hris.headcount(),
  "NRR":          posthog_cohort_nrr(),
  "Rule of 40":   growth_pct + ebitda_pct,
}

# Format into pptx via pptx skill
```

## Examples

### Example 1: Build FY27 budget for Series A SaaS company

**Goal:** End-to-end budget with 3-statement model + scenarios + headcount plan.

**Steps:**

1. Pull baseline: current ARR, cash, headcount, gross margin from Xero + Stripe + HRIS.
2. Set drivers (sheet 1): growth rate, churn, NRR, hiring pace, cost ratios.
3. Build revenue model (sheet 2): monthly MRR roll with new/expansion/churn.
4. Compute COGS + OpEx from drivers (sheet 3 = P&L).
5. Compute working capital + cash flow (sheet 4 = CF).
6. Compute Balance Sheet roll (sheet 5).
7. Sensitivity (sheet 6): scenarios + tornado.
8. Headcount plan (sheet 7) with monthly cost flow.
9. Save → review with founder → iterate on drivers → freeze v1.

**Result:** Full FY27 budget — base case shows $5.2M ARR, $1.8M cash burn, 14 months runway at end of year. Surfaces "need to hit upside or raise by Q3 27".

### Example 2: Re-forecast mid-quarter after big enterprise deal

**Goal:** $500K enterprise deal closes May; rebase Q3 + Q4 projections.

**Steps:**

1. Pull YTD actual vs budget (Recipe 5).
2. Identify YTD variance: revenue +$500K vs budget.
3. Trigger reforecast (Recipe 8 — > 5% threshold).
4. Project remaining months using new run-rate + deal recognition schedule.
5. Update cash flow forecast (more cash from collections in Q3).
6. Re-run sensitivity scenarios.
7. Issue revised budget to leadership; update board metrics.

**Result:** Q3 + Q4 rebased to higher run-rate; runway extended 2.3 months.

## Edge cases / gotchas

- **Causal acquisition by LucaNet:** product roadmap shifting toward European mid-market focus. Confirm pricing + features before adopting in 2026.
- **Mosaic acquisition by Hibob:** integration with Hibob HRIS now native. Pricing typically bundled.
- **Tool migration cost:** moving from xlsx → Causal/Mosaic is 2-6 weeks of effort. Don't migrate mid-quarter or pre-fundraise.
- **Driver hierarchy traps:** if multiple drivers cascade, changing one mid-model can break downstream calculations. Always trace upstream/downstream before editing.
- **Hardcoded numbers:** finance teams accumulate hardcodes ("just for this quarter"). Quarterly cleanup audit prevents bit-rot.
- **Currency / FX:** multi-entity models need FX rate handling. Use period-end for BS, period-avg for P&L (per ASC 830).
- **Fully loaded cost factor:** 1.3 is conservative for US (benefits + tax + equipment); use 1.4 with offices (+rent share); use 1.2 for fully remote contractor-heavy teams.
- **Stale base case:** budgets go stale within 6-8 weeks of actuals. Reforecast cadence: monthly variance review; quarterly hard reforecast.
- **Hockey-stick optimism:** every founder model has Q4 hockey stick. Apply 70% probability to Q4 in base case; 100% only in upside.
- **Pre-launch model assumptions:** for pre-revenue / pre-PMF, use range-bound assumptions and flag every cell as "assumption" not "forecast".

## Sources

- Best modeling tools 2026 (ValueAdd VC): https://valueaddvc.com/blog/best-financial-modeling-tools-for-startups-excel-vs-runway-vs-causal-vs-mosaic
- Cube software: https://www.cubesoftware.com/
- Mosaic.tech: https://www.mosaic.tech/
- Mosaic competitors: https://www.drivetrain.ai/post/mosaic-competitors-and-alternatives
- Causal app: https://causal.app/
- Runway financial planning: https://www.runway.com/
- Drivetrain: https://www.drivetrain.ai/

## Related skills

- `headcount-planning-hiring-budget` — uses Recipe 4
- `monthly-close-procedure` — feeds actuals into Recipe 5 BvA
- `runway-burn-analysis` — uses Recipe 6 sensitivity
- `investor-update-monthly-quarterly` — uses Recipe 10 board pack
