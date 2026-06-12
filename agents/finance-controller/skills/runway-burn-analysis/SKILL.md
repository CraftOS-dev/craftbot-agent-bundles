<!--
Source: https://mercury.com/blog/calculate-startup-cash-burn-rate
Source: https://nstarfinance.com/resources/startup-burn-rate-calculator-runway
Source: https://modelreef.io/solutions/templates/core-business-forecasting/cash-runway-and-burn-rate-forecasting
Source: Paul Graham — Default Alive vs Default Dead — http://paulgraham.com/aord.html
Reference role.md: "Runway and burn analysis playbook"
-->

# Runway and burn analysis — gross / net / Default Alive

Compute current cash position, monthly burn rate, runway months, and Default-Alive vs Default-Dead verdict. 2026 investor expectation: 24-30 months runway post-funding, burn multiple <1.5x.

## When to use

- Any time the founder asks "what's our cash" or "how long do we have".
- Pre-fundraise: runway calc justifies raise size + timing.
- Monthly: include in close memo + investor update.
- Quarterly: sensitivity analysis + Default-Alive test.
- Post-major-spend decision: re-run to validate impact.
- Trigger phrases: "runway", "burn rate", "how long until we run out", "Default Alive", "burn multiple".

NOT for: detailed weekly cash forecast (use `cash-flow-forecasting-13-week`); cap-table dilution (use `carta-pulley-cap-table`).

## Definitions (the only ones that matter)

- **Gross burn:** total monthly cash outflows. All OPEX + capex + debt service. Cash basis, not accrual.
- **Net burn:** gross burn − cash inflows (cash receipts, not accrual revenue). The figure that matters.
- **Runway months:** current cash ÷ trailing-3-month average net burn.
- **Default Alive:** at current growth + current burn, profitable before cash runs out? YES = Default Alive.
- **Default Dead:** same projection → runs out of cash before profitable. Raise or cut now.
- **Burn multiple:** net burn ÷ net new ARR. Elite < 1.0; healthy < 1.5; grow-at-all-costs > 2.

## Setup

Reuses existing skills:

```bash
# Already in CraftBot defaults:
# - xero / xero-mcp for P&L + cash basis revenue
# - stripe-api / stripe-mcp for revenue receipts
# Bundled (per this agent):
# - mercury-modern-treasury-banking for bank balances
# - cash-flow-forecasting-13-week for forward outflows
```

No new env vars beyond what those skills require.

## Common recipes

### Recipe 1 — Pull current cash (all accounts)

```python
import requests, os

def total_cash_now():
    # Mercury (primary)
    mercury_balances = requests.get(
      "https://api.mercury.com/api/v1/accounts",
      headers={"Authorization": f"Bearer {os.environ['MERCURY_API_KEY']}"}
    ).json()["accounts"]
    mercury_total = sum(a["availableBalance"] for a in mercury_balances)

    # Plaid-linked external accounts
    plaid_total = sum(plaid_balances_now())  # see mercury-modern-treasury-banking Recipe 5

    return mercury_total + plaid_total

print(f"Current cash: ${total_cash_now():,.0f}")
```

### Recipe 2 — Compute trailing-3-month net burn

```python
import pandas as pd
from datetime import date, timedelta

today = date.today()
month_starts = [date(today.year, today.month-i, 1) for i in range(4, 0, -1)]

# Get end-of-month bank balances for prior 3 months
balances = {}
for m in month_starts:
    eom = (m + pd.offsets.MonthEnd(0)).date()
    balances[eom] = get_bank_balance_as_of(eom)

# Net burn = (opening cash month N-2) - (closing cash this month) / 3
opening = balances[month_starts[0] - timedelta(days=1)]
closing = balances[month_starts[-1] + pd.offsets.MonthEnd(0).date() - timedelta(days=0)]
net_burn = (opening - closing) / 3
print(f"Net burn (trailing 3mo): ${net_burn:,.0f}/mo")
```

### Recipe 3 — Runway calculation

```python
current_cash = total_cash_now()        # Recipe 1
net_burn = trailing_3mo_net_burn()      # Recipe 2

if net_burn <= 0:
    print(f"Cash flow POSITIVE: ${-net_burn:,.0f}/mo net cash inflow. Runway: infinite.")
else:
    runway_months = current_cash / net_burn
    print(f"Runway: {runway_months:.1f} months at ${net_burn:,.0f}/mo net burn")
```

### Recipe 4 — Sensitivity matrix (±20% revenue, ±20% expense)

```python
import pandas as pd

base_rev = 200_000      # monthly cash inflow
base_exp = 380_000      # monthly cash outflow
base_burn = base_exp - base_rev  # $180K
cash = 2_700_000

scenarios = []
for rev_pct in [0.80, 0.90, 1.00, 1.10, 1.20]:
    row = {}
    for exp_pct in [0.80, 0.90, 1.00, 1.10, 1.20]:
        burn = base_exp * exp_pct - base_rev * rev_pct
        runway = cash / burn if burn > 0 else 999
        row[f"Exp {exp_pct:.0%}"] = round(runway, 1)
    scenarios.append({"Rev %": f"{rev_pct:.0%}", **row})

print(pd.DataFrame(scenarios).set_index("Rev %"))
```

Output (example):
```
        Exp 80%  Exp 90%  Exp 100%  Exp 110%  Exp 120%
Rev 80%   17.4     14.2      11.9       10.3        9.1
Rev 90%   19.7     15.7      13.0       11.1        9.7
Rev 100%  22.5     17.5      14.2       12.0       10.4
Rev 110%  26.2     19.7      15.6       13.0       11.1
Rev 120%  31.4     22.5      17.4       14.2       11.9
```

### Recipe 5 — Default Alive / Default Dead test

```python
# Project growth + burn out N months; find break-even month; compare to runway end
def project_to_breakeven(start_arr, growth_mo, gross_margin, fixed_opex_mo, opex_growth_mo, max_months=60):
    arr = start_arr
    fixed = fixed_opex_mo
    for m in range(1, max_months+1):
        monthly_rev = arr / 12
        monthly_gross_profit = monthly_rev * gross_margin
        monthly_burn = fixed - monthly_gross_profit
        if monthly_burn <= 0:
            return m, arr, fixed
        arr *= (1 + growth_mo)
        fixed *= (1 + opex_growth_mo)
    return None, arr, fixed

# Inputs
start_arr      = 3_000_000
growth_mo      = 0.05         # 5%/mo = 80%/yr
gross_margin   = 0.78
fixed_opex_mo  = 400_000
opex_growth_mo = 0.025        # 2.5%/mo = 35%/yr — hire ramp

# Run
breakeven_month, arr_at_be, opex_at_be = project_to_breakeven(
    start_arr, growth_mo, gross_margin, fixed_opex_mo, opex_growth_mo
)
runway_end_month = int(runway_months_today())  # from Recipe 3

if breakeven_month and breakeven_month <= runway_end_month:
    print(f"DEFAULT ALIVE: breakeven month {breakeven_month}, runway end month {runway_end_month}")
else:
    print(f"DEFAULT DEAD: breakeven month {breakeven_month}, runway end month {runway_end_month}")
```

### Recipe 6 — Burn multiple

```python
# Burn multiple = net burn / net new ARR (per period, typically quarterly)
def burn_multiple(net_burn_quarter, arr_start_q, arr_end_q):
    net_new_arr = arr_end_q - arr_start_q
    if net_new_arr <= 0:
        return float('inf')
    return net_burn_quarter / net_new_arr

bm = burn_multiple(net_burn_quarter=540_000, arr_start_q=3_000_000, arr_end_q=3_600_000)
print(f"Burn multiple: {bm:.2f}x")
# Benchmark: <1.0 elite | <1.5 healthy | >2.0 inefficient growth
```

### Recipe 7 — Gross burn vs net burn breakout

```python
# Pull P&L for trailing 3 months
pnl = xero.reports.profit_and_loss(fromDate=start_3mo, toDate=eom)

# Gross burn = all OPEX + COGS (cash basis) + capex
gross_burn = (pnl.cogs + pnl.opex + capex_3mo) / 3

# Cash inflows = cash receipts (NOT recognized revenue!)
cash_received = bank_receipts_3mo / 3   # from bank-feed receipts categorized as customer payments

net_burn = gross_burn - cash_received
print(f"Gross burn: ${gross_burn:,.0f}/mo")
print(f"Cash receipts: ${cash_received:,.0f}/mo")
print(f"Net burn: ${net_burn:,.0f}/mo")
```

### Recipe 8 — Runway extension levers

```python
# Standard playbook when runway < 18 months
def runway_extension_options(current_cash, net_burn, target_runway=24):
    target_burn = current_cash / target_runway
    burn_reduction_needed = net_burn - target_burn

    options = {
      "Cut headcount (avg $185K loaded)":
          f"~{burn_reduction_needed * 12 / 185_000:.1f} FTE reduction",
      "Cut S&M by 50%":
          f"≈ ${(pnl.sm_spend * 0.5 / 3):,.0f}/mo savings",
      "Pause non-essential SaaS":
          f"≈ $5-15K/mo (typical 10-15% of SaaS spend is unused — see vendor audit)",
      "Pricing increase 10%":
          f"≈ ${(pnl.revenue * 0.10 / 3):,.0f}/mo (subject to churn risk)",
      "Raise convertible / SAFE":
          f"≈ ${burn_reduction_needed * 24 / 1000:.0f}K minimum to extend 24mo at current burn",
      "Accelerate AR collections":
          f"≈ ${(ar_outstanding * 0.5):,.0f} one-time cash; pull DSO from 45 → 30 days",
    }
    return options
```

### Recipe 9 — Investor expectation framing

```python
# 2026 baseline expectations
def runway_grade(months_runway, burn_multiple_q):
    grade_runway = (
      "ELITE"    if months_runway > 30 else
      "STRONG"   if months_runway > 24 else
      "OK"       if months_runway > 18 else
      "TIGHT"    if months_runway > 12 else
      "DEFAULT DEAD WITHOUT ACTION"
    )
    grade_bm = (
      "ELITE"    if burn_multiple_q < 1.0 else
      "HEALTHY"  if burn_multiple_q < 1.5 else
      "ACCEPTABLE" if burn_multiple_q < 2.0 else
      "INEFFICIENT — DILIGENCE RED FLAG"
    )
    return {"runway_grade": grade_runway, "burn_multiple_grade": grade_bm}
```

### Recipe 10 — Output template (the order the founder needs)

```python
def runway_report(today):
    cash = total_cash_now()
    net_burn = trailing_3mo_net_burn()
    runway = cash / net_burn if net_burn > 0 else float("inf")
    breakeven_month, _, _ = project_to_breakeven(...)
    bm = burn_multiple(...)
    grades = runway_grade(runway, bm)
    sensitivity = sensitivity_matrix(...)

    return f"""
RUNWAY REPORT — {today}

(1) Current cash: ${cash:,.0f}
(2) Net burn (T3M avg): ${net_burn:,.0f}/mo
(3) Runway: {runway:.1f} months → {grades['runway_grade']}
(4) Default Alive verdict: {'ALIVE' if breakeven_month and breakeven_month < runway else 'DEAD'}
   - Projected breakeven month: {breakeven_month}
   - Runway end month: {int(runway)}
(5) Burn multiple (last Q): {bm:.2f}x → {grades['burn_multiple_grade']}
(6) Sensitivity (Rev/Exp ±20%):
{sensitivity}
(7) Recommendations (if runway < 18 months):
   - See runway extension options
"""
```

## Examples

### Example 1: Monthly runway snapshot for board pack

**Goal:** Add 1-page runway slide to monthly investor update.

**Steps:**

1. Run Recipe 1 + Recipe 2 + Recipe 3.
2. Run Recipe 6 burn multiple for last quarter.
3. Generate Recipe 10 output.
4. Format into 1 slide: cash bar chart trailing-12mo + headline numbers.
5. Verify cash number matches bank statement; flag if drift > $1K.

**Result:** Single slide with cash | runway | burn multiple | verdict.

### Example 2: Crisis runway analysis (cash < 12 months)

**Goal:** Founder asks "are we Default Dead". Cash $1.2M, net burn $180K = 6.7 months runway.

**Steps:**

1. Confirm cash (Recipe 1): $1.2M ✓.
2. Confirm net burn (Recipe 2 + Recipe 7): $180K/mo ✓.
3. Run Default-Alive (Recipe 5):
   - Current ARR $1.5M; growth 8%/mo; gross margin 75%; fixed OPEX $245K/mo; OPEX growth 3%/mo.
   - Breakeven month: 14. Runway end: 7.
   - Verdict: DEFAULT DEAD.
4. Surface to founder: "Without action, cash runs out month 7 (Q1 2027). Breakeven month 14 (Q3 2027) requires extended runway."
5. Run Recipe 8 extension options:
   - Cut 3 FTE → save $46K/mo → extends 1.4 months.
   - Cut S&M 50% → save $48K/mo → extends 1.5 months.
   - Raise $2M SAFE → extends 11 months at current burn.
6. Recommendation: combine 2 FTE cut + raise $1.5M → extends 13 months → past breakeven.

**Result:** Founder has 3 concrete paths to Default-Alive with quantified impact.

## Edge cases / gotchas

- **Cash basis vs accrual:** burn is CASH basis. Don't use accrual revenue (deferred revenue is cash you already have; recognized revenue is paper).
- **One-time items distort T3M:** if there was a big tax refund or one-time SaaS prepayment in the trailing 3 months, normalize them out. Use rolling-12mo as cross-check.
- **Growth-stage burn ramps:** if you just hired 5 people, T3M burn understates forward burn. Use go-forward burn = next 30 days projected from 13-week forecast.
- **Funded round in trailing 3mo:** runway calc breaks if you raised in the window. Use post-raise cash and steady-state burn separately.
- **Treasury yield:** if $5M earning 5% APY = ~$20K/mo. Subtract from net burn (it offsets).
- **FX exposure:** foreign-currency cash translated at period-end spot. Big FX swings can move cash 5-10% on quarterly basis.
- **Default Alive assumes constant growth:** in reality, growth decelerates. Apply 20-30% deceleration per year in optimistic scenarios; flag in cover.
- **Burn multiple can be misleading at small scale:** $50K burn / $30K new ARR = 1.67x looks bad but absolute scale is small. Apply benchmark only at scale.
- **Investor expectations vary by stage:** Series B + raised in 2024 with 18 months runway is fine; Series A in 2026 with 18 months gets pushback. Reference current vintage.
- **Don't conflate runway with timeline:** runway = months of survival; "when do we need to raise" = runway − fundraise duration (3-6 months) − buffer (3 months).

## Sources

- Mercury — calculate startup burn rate: https://mercury.com/blog/calculate-startup-cash-burn-rate
- nStar Finance — burn rate calculator: https://nstarfinance.com/resources/startup-burn-rate-calculator-runway
- Model Reef — cash runway forecasting: https://modelreef.io/solutions/templates/core-business-forecasting/cash-runway-and-burn-rate-forecasting
- Paul Graham — Default Alive: http://paulgraham.com/aord.html
- Bessemer — burn multiple benchmarks: https://www.bvp.com/atlas/the-burn-multiple
- SaaS Capital — efficiency metrics: https://www.saasmag.com/saas-capital-efficiency-metrics/

## Related skills

- `mercury-modern-treasury-banking` — Recipe 1 cash pull
- `cash-flow-forecasting-13-week` — forward 13 weeks for go-forward burn
- `unit-economics-saas-metrics` — burn multiple ties to unit econ
- `investor-update-monthly-quarterly` — runway is mandatory in updates
- `causal-mosaic-financial-modeling` — scenarios drive Recipe 5
