<!--
Source: https://www.morganstanley.com/im/publication/insights/articles/article_capitalallocation.pdf
Source: https://aswathdamodaran.substack.com/p/data-update-8-for-2026-dividends
Source: https://www.wallstreetprep.com/knowledge/capital-allocation/
Reference role.md: "Capital allocation playbook"
-->

# Capital allocation framework — ROIC vs WACC ladder

Applies the Damodaran lens to startup decisions: **reinvest until marginal ROIC > WACC; return excess only after profitable reinvestment is exhausted**. For private companies the ladder is (1) reinvest in growth → (2) reserve runway buffer → (3) opportunistic M&A → (4) return capital. 2026 S&P 500 buybacks at record >$1T, but private-side reinvestment still dominates.

## When to use

- Excess-cash decision: invest in growth vs reserve vs M&A vs buyback.
- Founder pitch on "where should we deploy the next $5M".
- Board strategy session on capital priorities for the year.
- Tradeoff: hire 10 AEs vs invest in product R&D vs acquire a smaller competitor.
- Trigger phrases: "capital allocation", "ROIC", "WACC", "marginal return", "reinvest vs return", "use of capital".

NOT for: capital structure (use `capital-structure-debt-equity-mix-stage`); treasury implementation (use `treasury-yield-ladder-risk-tier`).

## Setup

```bash
uvx --with pandas --with numpy python -c "import pandas, numpy"

# Damodaran 2026 datasets (free)
curl -O https://pages.stern.nyu.edu/~adamodar/pc/datasets/wacc.xlsx
curl -O https://pages.stern.nyu.edu/~adamodar/pc/datasets/totalbeta.xlsx
curl -O https://pages.stern.nyu.edu/~adamodar/pc/datasets/ctryprem.xlsx
```

## The capital allocation ladder

```
PRIORITY 1 — REINVEST IN GROWTH (until marginal ROIC < WACC)
  Test: LTV:CAC ≥ 3:1, CAC payback < 18 months, NRR ≥ 100%
  Mechanism: hire S&M, scale R&D, geographic expansion, new products
  ROIC proxy for SaaS: ARR generated / capital deployed

PRIORITY 2 — RESERVE RUNWAY BUFFER (24 months minimum at burn rate)
  Test: ending cash ≥ 24× monthly burn
  Mechanism: treasury (T-bills, money market)
  Yield ~3.7% on 1-3mo T-bills (2026); survival floor, not return

PRIORITY 3 — OPPORTUNISTIC M&A (only with strategic fit + accretive economics)
  Test: accretive on revenue multiple OR fills genuine product gap
  Mechanism: acquihire → tuck-in → strategic consolidation
  Reality: 70-90% of M&A destroys value (HBR/McKinsey). High bar.

PRIORITY 4 — RETURN CAPITAL (rare for private)
  Mechanism: dividend (steady), buyback (opportunistic), secondaries
  Test: no profitable reinvestment opportunity at ROIC > WACC
  Private: secondaries for founder/early-employee liquidity (Forge, EquityZen, CrossFlow)
```

## Damodaran 2026 framework summary

- **Marginal ROIC > WACC** = the only test that matters for "more growth investment is good."
- **Cash earns ~risk-free rate** ≈ 3.7% in 2026. If WACC = 12%, idle cash destroys 8.3% of value/year.
- **Buybacks at S&P 500 record >$1T in 2025** → signal mature firms exhausting growth opportunities.

## Common recipes

### Recipe 1 — Compute WACC (CAPM)

```python
def cost_of_equity_capm(rf, beta, erp, country_risk_premium=0):
    return rf + beta * (erp + country_risk_premium)

def wacc(equity_weight, debt_weight, equity_cost, debt_cost_after_tax):
    return equity_weight * equity_cost + debt_weight * debt_cost_after_tax

# 2026 reference: rf=3.7% (10yr UST), erp=5.5% (Damodaran 2026 implied), beta SaaS ~1.4
ke = cost_of_equity_capm(rf=0.037, beta=1.4, erp=0.055)
kd_after_tax = 0.085 * (1 - 0.21)  # 8.5% venture debt × (1 - 21% fed corp tax)
w = wacc(0.85, 0.15, ke, kd_after_tax)
print(f"Cost of equity: {ke:.2%}, WACC: {w:.2%}")  # Series B SaaS WACC: 11-14%
```

### Recipe 2 — Compute ROIC

```python
def roic(nopat, invested_capital):
    return nopat / invested_capital

forward_ebit = 3_800_000
tax_rate = 0.10  # effective w/ R&D credit
nopat = forward_ebit * (1 - tax_rate)
invested_capital = 18_500_000  # total equity raised + LT debt - cash
print(f"Forward ROIC: {roic(nopat, invested_capital):.2%}")
```

### Recipe 3 — Marginal ROIC on next growth dollar

```python
def marginal_roic_growth_dollar(incremental_arr, gross_margin, churn_mo, capital_spend):
    arr_lifetime_gp = (incremental_arr / 12) * gross_margin / churn_mo
    return arr_lifetime_gp / capital_spend

# Spend $1M S&M → $480K new ARR
mroic = marginal_roic_growth_dollar(480_000, 0.78, 0.015, 1_000_000)
print(f"Marginal ROIC on S&M dollar: {mroic:.1%}")
```

### Recipe 4 — Capital ladder decision tree

```python
def allocate(cash, monthly_burn, ltv_cac, cac_payback_mo, nrr, ma_targets, wacc, marginal_roic):
    runway = cash / monthly_burn
    decisions = []

    # Priority 2: reserve buffer
    target_runway = 24
    reserve_need = max(0, (target_runway - runway) * monthly_burn)
    if reserve_need > 0:
        decisions.append(("Reserve runway", reserve_need))
        cash -= reserve_need

    # Priority 1: reinvest IF healthy
    growth_eligible = ltv_cac >= 3.0 and cac_payback_mo < 18 and nrr >= 1.00 and marginal_roic > wacc
    if growth_eligible:
        growth_alloc = cash * 0.70
        decisions.append(("Reinvest in growth", growth_alloc))
        cash -= growth_alloc

    # Priority 3: M&A
    if ma_targets and cash > 0:
        ma_alloc = cash * 0.40
        decisions.append(("Opportunistic M&A", ma_alloc))
        cash -= ma_alloc

    # Priority 4: return
    if cash > 0:
        decisions.append(("Hold / return (secondaries)", cash))
    return decisions

print(allocate(8_500_000, 420_000, 4.2, 14, 1.18, False, 0.12, 0.18))
```

### Recipe 5 — Pull Damodaran 2026 industry data

```python
import pandas as pd
df_wacc = pd.read_excel("wacc.xlsx", sheet_name="Industry Averages")
print(df_wacc[df_wacc["Industry"].str.contains("Software", case=False)])
df_beta = pd.read_excel("totalbeta.xlsx", sheet_name="Industry Averages")
print(df_beta[df_beta["Industry"].str.contains("Software|Internet", case=False)])
```

### Recipe 6 — Excess cash penalty (Damodaran)

```python
def excess_cash_drag(excess_cash, wacc, risk_free_rate):
    return excess_cash * (wacc - risk_free_rate)

# $5M idle, WACC 12%, T-bills 3.7%
print(f"Value destroyed/yr by $5M idle: ${excess_cash_drag(5_000_000, 0.12, 0.037):,.0f}")
# → $415K/year opportunity cost
```

### Recipe 7 — M&A accretion test (revenue-multiple)

```python
def ma_accretion(acquirer_ev, acquirer_arr, target_arr, deal_value, target_growth, acquirer_growth):
    pre_multiple = acquirer_ev / acquirer_arr
    post_multiple = (acquirer_ev + deal_value) / (acquirer_arr + target_arr)
    blended_growth = (acquirer_growth * acquirer_arr + target_growth * target_arr) / (acquirer_arr + target_arr)
    return {
        "pre_multiple": pre_multiple, "post_multiple": post_multiple,
        "accretive_on_multiple": post_multiple > pre_multiple,
        "blended_growth": blended_growth,
        "accretive_on_growth": blended_growth > acquirer_growth,
    }

print(ma_accretion(80_000_000, 8_000_000, 2_000_000, 12_000_000, 1.20, 1.40))
```

### Recipe 8 — Capital allocation memo template

```markdown
# Capital Allocation Recommendation — Q3 2026

## Inputs
- Cash balance: $8.5M
- Monthly burn: $420K (runway 20mo)
- Unit econ: LTV:CAC 4.2:1, CAC payback 14mo, NRR 118%
- WACC: 12.1%
- Marginal ROIC on S&M dollar: ~18%

## Recommendation
1. Reserve runway top-up to 24mo buffer: $1.68M (T-bill ladder)
2. Reinvest in growth: $4.8M over 18mo (4 AEs + 6 engineers) — marginal ROIC 18% > WACC 12%
3. Opportunistic M&A: none qualified; defer
4. Return: none; secondaries deferred

## Damodaran lens
Marginal ROIC > WACC + healthy unit econ + sub-24mo runway → growth dominates.
Idle-cash drag would be ~$695K/yr on $8.3M at 12% - 3.7% spread.
```

## Examples

### Example 1: "Hire 10 AEs or build new product line?"

**Goal:** Pick higher-ROIC deployment.

**Steps:**
1. Recipe 3 → marginal ROIC of S&M dollar (typically 15-25% healthy SaaS).
2. Estimate marginal ROIC of R&D dollar (PM-projected revenue × execution-risk discount).
3. Compare to WACC (Recipe 1).
4. Pick higher; if both > WACC, split based on execution capacity not capital.

**Result:** Defensible allocation memo.

### Example 2: Excess cash post-Series C

**Goal:** Just raised $40M; accelerate hiring or M&A?

**Steps:**
1. Recipe 4 → ladder. Reserve 24mo buffer first.
2. Compute marginal ROIC of doubling S&M (Recipe 3) — diminishing returns at scale.
3. Run M&A screen + test Recipe 7 accretion.
4. Allocate per ladder priorities.

**Result:** ~60% growth, ~25% M&A reserve, ~15% buffer extension.

## Edge cases / gotchas

- **WACC inputs are noisy.** Damodaran's annual update is the free gold standard; commercial sources (Cap IQ, Bloomberg) for premium.
- **Marginal ROIC declines with scale.** Recipe 3 assumes constant unit econ; re-estimate yearly at scale.
- **R&D ROIC hard to measure.** Proxy: PM-forecasted revenue × probability × GM / capital spend.
- **M&A accretion ≠ value creation.** Recipe 7 tests multiple, not strategic logic. McKinsey: 70-90% destroys value.
- **Cash earns ~3.7%, not zero.** Still drags vs WACC reinvestment.
- **Founder dilution sensitivity.** Returning capital via private buyback = secondaries (Forge, EquityZen, CrossFlow).
- **24-month runway is modern floor.** 2022-23 taught the lesson; investors expect minimum.
- **Buybacks for private are rare and signaling-negative.** Reads as exhaustion of growth.
- **Don't confuse allocation with structure.** Allocation = where dollars go; structure = how dollars are funded.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions.**

## Sources

- Morgan Stanley capital allocation: https://www.morganstanley.com/im/publication/insights/articles/article_capitalallocation.pdf
- Damodaran 2026 dividends/buybacks: https://aswathdamodaran.substack.com/p/data-update-8-for-2026-dividends
- Wall Street Prep capital allocation: https://www.wallstreetprep.com/knowledge/capital-allocation/
- Damodaran data home: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/data.html
- Damodaran 2026 ERP: https://aswathdamodaran.substack.com/p/data-update-1-for-2026-the-push-and
- HBR M&A failure: https://hbr.org/2011/03/the-big-idea-the-new-ma-playbook

## Related skills

- `capital-structure-debt-equity-mix-stage` — how to fund the allocation.
- `treasury-yield-ladder-risk-tier` — implements "reserve" tier.
- `ma-target-screen-and-qoe` — implements M&A tier.
- `three-statement-financial-model-tied` — receives allocation outputs.
