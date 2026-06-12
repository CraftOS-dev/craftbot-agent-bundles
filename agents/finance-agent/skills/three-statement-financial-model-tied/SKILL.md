<!--
Source: https://cfoproanalytics.com/cfo-wiki/fractional-cfo/building-a-3-statement-financial-model-cfos-guide-to-driver-based-forecasting/
Source: https://cfoadvisors.com/blog/mosaic-vs-runway-vs-cube-fpa-software-2026
Source: https://valueaddvc.com/blog/best-financial-modeling-tools-for-startups-excel-vs-runway-vs-causal-vs-mosaic
Reference role.md: "Three-statement model playbook"
-->

# Three-statement financial model — IS / BS / CF tied (driver-based)

Builds an investor-grade three-statement model (Income Statement / Balance Sheet / Cash Flow) tied via balancing identity, with driver-based revenue and cost forecasts. 2026 investor bar: ±5% accuracy next quarter, ±15% next 12 months. Designed to map cleanly to Runway / Causal / Mosaic / Cube tabs and to be portable to Excel/Sheets.

## When to use

- Building or rebuilding the company's master financial model for board / investors / IPO prep.
- Plugging actuals from Xero/QuickBooks into a forecast each month-end.
- Preparing a 36-60 month forecast for a Series A/B/C fundraise.
- Trigger phrases: "three-statement model", "tied model", "build me a model", "IS BS CF", "driver-based forecast", "FP&A model".

NOT for: scenario / sensitivity only (use `scenario-planning-monte-carlo`); cohort revenue logic alone (use `driver-based-revenue-modeling`).

## Setup

```bash
# Python stack for portable models
uvx --with openpyxl --with pandas --with numpy python -c "import openpyxl, pandas, numpy"

# Optional: Causal / Mosaic / Cube via REST (recipient supplies key)
export CAUSAL_API_KEY="<from Causal Settings → API>"
export MOSAIC_API_KEY="<from Mosaic Settings → Integrations>"
export CUBE_API_KEY="<from Cube Admin → API>"
```

Data inputs:
- Actuals: `xero-mcp` (P&L + Balance Sheet trial), `stripe-mcp` (revenue by plan)
- Headcount / payroll: HRIS (Gusto/Rippling/Deel) via `cli-anything`
- Drivers: live cells (growth%, churn%, ACV, headcount plan)

## Three-statement architecture

### Income Statement line items (standard SaaS investor model)

```
Revenue
  Subscription revenue              (driver: cohort × ACV × NRR)
  Services revenue                  (driver: implementation $ × deals)
  Other revenue                     (one-offs)
Total Revenue

Cost of Revenue (COGS)
  Hosting / infrastructure          (% of revenue, declining w/ scale)
  Third-party APIs / LLM inference  (per-call cost × usage)
  Customer support payroll          (FTE × loaded cost)
  Customer success payroll          (FTE × loaded cost)
  Payment processing fees           (~2.9% + $0.30 × txn count)
  Implementation contractor cost    (services delivery)
Total COGS
Gross Profit                        (target SaaS ≥75% GM)

Operating Expenses
  Sales payroll + commissions
  Marketing programs (ads, events, content)
  R&D payroll (engineering, product, design)
  G&A payroll (finance, ops, exec, legal)
  Software / tools                  (Tropic benchmark $X/FTE/mo)
  Rent / occupancy
  Travel + entertainment
  Professional services             (legal, accounting, consulting)
  Other OpEx
Total OpEx

EBITDA = Gross Profit − OpEx
  Less: Depreciation + Amortization
  Less: Stock-based compensation (SBC)
EBIT
  Less: Interest expense (venture debt, RBF)
  Plus: Interest income (treasury yield)
Pre-tax income
  Less: Income tax (R&D credit offset for QSBs)
Net Income
```

### Balance Sheet line items (tied)

```
Assets
  Current
    Cash + cash equivalents         (← from CF statement)
    Short-term investments          (T-bill ladder ≤12mo)
    AR (accounts receivable)        (driver: DSO × revenue)
    Prepaid expenses                (annual SaaS prepays)
    Other current
  Non-current
    Long-term investments           (T-bills >12mo)
    PP&E net of accumulated depreciation
    Capitalized software (if applicable; ASC 350-40)
    Goodwill + intangibles (from M&A)
    Deferred tax asset (R&D credit carryforward)
Total Assets

Liabilities
  Current
    AP (accounts payable)           (driver: DPO × COGS+OpEx)
    Accrued expenses                (payroll accrual, vendor)
    Deferred revenue (current)      (annual prepays unearned)
    Current portion of debt
  Non-current
    Long-term debt (venture debt, RBF)
    Deferred revenue (non-current)
    Other LT liabilities
Total Liabilities

Equity
  Preferred stock (Series Seed/A/B/C; redemption value)
  Common stock
  APIC (additional paid-in capital)
  Accumulated deficit               (← from IS net income)
  AOCI (FX translation, hedge MTM)
Total Equity
```

### Cash Flow statement (indirect method)

```
CFO (Cash from Operations)
  Net income                        (← from IS)
  + D&A
  + SBC
  + Change in working capital
    − ΔAR (more AR = use of cash)
    + ΔAP, ΔAccrued
    + ΔDeferred revenue (cash collected ahead of recognition)
    − ΔPrepaid expenses
CFO

CFI (Cash from Investing)
  − CapEx
  − Purchase of short-term investments
  + Sale of investments
  − M&A consideration
CFI

CFF (Cash from Financing)
  + Equity issuance (priced rounds, SAFE conversions)
  − Stock buybacks (rare for private)
  + Debt issuance (venture debt drawdown)
  − Debt repayment (principal)
  − Dividends (rare for venture-backed)
CFF

Net change in cash = CFO + CFI + CFF
Cash, beginning of period
Cash, end of period                 (→ ties back to BS Cash)
```

## The tied-model rules (the four checks)

1. **Net income on IS = Net income on top of CFO** (no other source).
2. **Ending Cash on CF = Cash on BS** (single integration).
3. **Retained earnings rolls** = Prior RE + Net income − Dividends.
4. **Total Assets = Total Liabilities + Equity** every period (balancing identity).

Build a `Check` row at the bottom of the BS: `=Assets − (Liab + Equity)`. Must be 0 every column. If non-zero, the model is broken.

## Common recipes

### Recipe 1 — Skeleton in Excel (openpyxl)

```python
import openpyxl
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
months = [f"2026-{m:02d}" for m in range(1, 13)] + [f"2027-{m:02d}" for m in range(1, 13)]

ws = wb.active
ws.title = "IS"
ws["A1"] = "Income Statement"
for i, m in enumerate(months, start=2):
    ws.cell(row=1, column=i, value=m)

rows = [
    "Subscription revenue", "Services revenue", "Total Revenue",
    "Hosting", "Support payroll", "Total COGS", "Gross Profit",
    "S&M payroll", "Marketing programs", "R&D payroll", "G&A payroll",
    "Total OpEx", "EBITDA", "D&A", "SBC", "EBIT",
    "Interest expense", "Interest income", "Pre-tax income",
    "Income tax", "Net income"
]
for r, name in enumerate(rows, start=2):
    ws.cell(row=r, column=1, value=name)

wb.create_sheet("BS")
wb.create_sheet("CF")
wb.create_sheet("Drivers")
wb.create_sheet("Checks")
wb.save("master_model_v1.xlsx")
```

### Recipe 2 — Pull Xero actuals into the model

```python
# via xero-mcp
import json, subprocess
actuals = json.loads(subprocess.check_output([
    "mcp", "call", "xero-mcp", "reports.profit_and_loss",
    "--fromDate", "2026-01-01", "--toDate", "2026-05-31",
    "--periods", "5", "--timeframe", "MONTH"
]))
# Map Xero tracking categories → model line items
# Drop into IS sheet columns Jan..May as ACTUAL; Jun+ stays forecast
```

### Recipe 3 — Drivers tab (separate from IS/BS/CF)

```
Drivers
  Revenue growth (MoM%)              5.0%   → forecast logo growth
  Net New Logos / mo                 22     → from sales capacity model
  Avg ACV ($)                        24,000 → blended
  Logo churn / mo                    1.5%
  Net Revenue Retention              118%
  Gross margin target                78%
  S&M as % of revenue                42%
  R&D as % of revenue                28%
  G&A as % of revenue                12%
  DSO (days)                         42
  DPO (days)                         35
  Deferred revenue % (annual prepay) 35%
  CapEx per FTE / yr ($)             2,000
  Headcount end-of-period            85 → 102 → 124
```

All IS/BS/CF cells reference Drivers, never hard-code.

### Recipe 4 — Working capital ties

```python
# AR = DSO / 30 × monthly revenue
ar = (dso / 30) * monthly_revenue

# AP = DPO / 30 × (COGS + cash OpEx)
ap = (dpo / 30) * (cogs + opex_cash)

# Deferred revenue (current) = annual_prepay_rate × annual_revenue / 2
def_rev_current = annual_prepay_rate * annual_revenue / 2

# ΔWC = (ARt − ARt-1) − (APt − APt-1) − (DefRevt − DefRevt-1) + (PrepaidExpt − PrepaidExpt-1)
delta_wc = (ar_t - ar_prev) - (ap_t - ap_prev) - (def_rev_t - def_rev_prev) + (prepaid_t - prepaid_prev)
# CFO = NI + DA + SBC − ΔWC
```

### Recipe 5 — Equity rollforward (cap-table linked)

```python
# Common SAFE conversion at Series A
safe_principal = 2_500_000
valuation_cap = 10_000_000
series_a_pre_money = 35_000_000
conversion_price = min(valuation_cap, series_a_pre_money) / pre_money_fdshares
# SAFE shares = principal / conversion_price → add to common at conversion
# Increase APIC by safe_principal; do not add to cash (cash was received earlier)
```

### Recipe 6 — The four checks (always-on)

```python
checks = {
    "NI tied":         abs(is_net_income - cf_top_ni) < 1,
    "Cash tied":       abs(cf_ending_cash - bs_cash) < 1,
    "RE roll":         abs(bs_re - (bs_re_prev + is_net_income - dividends)) < 1,
    "BS balances":     abs(bs_assets - bs_liab_equity) < 1,
}
assert all(checks.values()), checks
```

### Recipe 7 — Variance vs Plan (monthly close drop-in)

```python
def variance_vs_plan(actual, plan):
    var_abs = actual - plan
    var_pct = var_abs / plan if plan else float('inf')
    flag = "RED" if abs(var_pct) > 0.10 else "YELLOW" if abs(var_pct) > 0.05 else "GREEN"
    return {"actual": actual, "plan": plan, "var": var_abs, "var%": var_pct, "flag": flag}
```

### Recipe 8 — Causal upload (when recipient is on Causal)

```bash
curl -X POST "https://api.causal.app/v1/models/$MODEL_ID/data" \
  -H "Authorization: Bearer $CAUSAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d @drivers.json
```

### Recipe 9 — Mosaic / Cube pulls (when on those platforms)

```bash
# Mosaic
curl -H "Authorization: Bearer $MOSAIC_API_KEY" \
  "https://api.mosaic.tech/v1/metrics/arr?from=2026-01-01&to=2026-06-30"

# Cube
curl -H "Authorization: Bearer $CUBE_API_KEY" \
  "https://api.cube.dev/v1/load?query={\"measures\":[\"revenue.total\"]}"
```

## Examples

### Example 1: Build Series A model in 60 minutes

**Goal:** Tied IS/BS/CF, 36-month forecast, driver-based, for Series A pitch.

**Steps:**
1. Recipe 1 → skeleton with 36 months.
2. Pull last 12 months actuals via Recipe 2 (Xero).
3. Build Drivers tab (Recipe 3): growth, churn, ACV, headcount plan, margin targets.
4. Wire IS (Recipe 3 references); compute COGS / OpEx from drivers.
5. Wire BS working capital (Recipe 4); plug equity rollforward (Recipe 5).
6. Wire CF using indirect method.
7. Run the four checks (Recipe 6); fix until all GREEN.
8. Add `Plan vs Actual` variance tab (Recipe 7).

**Result:** Tied model, every cell traceable to a driver. Investor can change one cell (NRR) and see all three statements update.

### Example 2: Monthly close drop-in

**Goal:** Drop May 2026 actuals into the master model, refresh forecast.

**Steps:**
1. Run Recipe 2 → Xero P&L May 2026 actuals.
2. Replace forecast cells in column "2026-05" with actuals.
3. Recompute downstream forecast months (drivers don't change, but base does).
4. Recipe 7 → Variance report; flag any >10% deviations.
5. Re-tie checks (Recipe 6). Save as `master_model_v_{date}.xlsx` (version controlled).

**Result:** Board pack-ready model in 30 minutes.

## Edge cases / gotchas

- **Deferred revenue trips most models.** Annual prepays = cash up front (CFF/CFO positive), revenue recognized ratably (IS unchanged), deferred revenue liability grows then unwinds. Get this right or BS will not balance.
- **SBC is real on IS but added back on CFO.** Forgetting this breaks the cash tie.
- **Working capital sign conventions.** Increase in AR = use of cash (negative on CFO). Easy to flip.
- **SAFE conversions hit equity, not cash.** Cash was received when SAFE was signed; at conversion only APIC reclassifies — no cash impact.
- **R&D credit timing.** QSB R&D credit offsets payroll tax monthly (not income tax annually). Model in OpEx, not below-the-line.
- **Hard-coded numbers in IS/BS/CF.** All numbers must come from Drivers. If you find a hardcode in IS, find the driver it should reference.
- **Don't forget the Checks tab.** A model that doesn't balance is worse than no model — investors lose trust permanently if they catch an unbalanced model.
- **Headcount-driven OpEx.** Loaded cost per FTE varies by role (eng $200K loaded, sales $250K + comm, support $90K loaded). Use loaded-cost tables.
- **Tropic / Vendr software benchmark.** $5-15K/FTE/yr typical for SaaS startups. Don't undershoot.
- **Equity stripping for ASC 718.** SBC expense ≠ option grant value at grant; spread Black-Scholes value over vesting period.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions.**

## Sources

- CFO Pro Analytics — driver-based three-statement modeling: https://cfoproanalytics.com/cfo-wiki/fractional-cfo/building-a-3-statement-financial-model-cfos-guide-to-driver-based-forecasting/
- Mosaic vs Runway vs Cube 2026: https://cfoadvisors.com/blog/mosaic-vs-runway-vs-cube-fpa-software-2026
- Causal vs Mosaic vs Runway vs Excel 2026: https://valueaddvc.com/blog/best-financial-modeling-tools-for-startups-excel-vs-runway-vs-causal-vs-mosaic
- Damodaran 2026 Data Updates: https://aswathdamodaran.substack.com/p/data-update-1-for-2026-the-push-and
- Damodaran Useful Datasets (NYU): https://pages.stern.nyu.edu/~adamodar/New_Home_Page/data.html
- Causal API: https://docs.causal.app/api
- Mosaic API: https://docs.mosaic.tech/api
- Cube API: https://cube.dev/docs/rest-api
- openpyxl docs: https://openpyxl.readthedocs.io/

## Related skills

- `driver-based-revenue-modeling` — feeds Revenue lines.
- `scenario-planning-monte-carlo` — flexes drivers, rolls through this model.
- `capital-structure-debt-equity-mix-stage` — feeds CFF (debt/equity).
- `board-cfo-financial-package` — consumes this model's output.
