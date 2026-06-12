<!--
Source: https://corporatefinanceinstitute.com/resources/financial-modeling/capital-stack-structure-debt-equity/
Source: https://www.axisgroupventures.com/post/capital-stack-optimization-how-founders-are-blending-debt-equity-and-secondaries-in-2026
Source: https://www.re-cap.com/blog/capital-structure-vs-capital-stack
Reference role.md: "Capital structure playbook"
-->

# Capital structure — debt vs equity mix by stage

Designs the optimal blended capital stack per stage using WACC framework + 2026 SOTA blended-stack trend (Axis Group). Early stage = mostly equity; Series A-B = +20-30% venture debt; Series C+ = sophisticated debt + RBF + secondaries. 2026 trend: blended capital stack with secondaries for founder/early-employee liquidity is dominant.

## When to use

- Post-raise: lock in optimal stack for next 18-24 months.
- Pre-fundraise: decide what mix maximizes value.
- Refinancing event: replace existing debt with cheaper instrument.
- Pre-IPO: optimize for public-market WACC profile.
- Trigger phrases: "capital structure", "capital stack", "debt vs equity mix", "WACC", "leverage", "blended stack".

NOT for: term sheet review (use `term-sheet-nvca-grade-review`); fundraising strategy (use `fundraising-strategy-priced-safe-venture-debt-rbf`).

## Setup

```bash
uvx --with pandas --with numpy --with scipy python -c "import pandas, numpy, scipy"

# Damodaran 2026 capital structure datasets (free)
curl -O https://pages.stern.nyu.edu/~adamodar/pc/datasets/dbtfund.xlsx
curl -O https://pages.stern.nyu.edu/~adamodar/pc/datasets/optimalcap.xlsx
```

## Stage-graded capital structure

```
PRE-SEED / SEED
  Equity:  85-95%   (founders + angel + seed VCs)
  Debt:    5-15%    (founder loans, micro-credit)
  Other:   0
  WACC:    Heavy on cost-of-equity (~18-25% for seed)

SERIES A-B
  Equity:  70-85%   (Series A/B priced equity)
  Debt:    15-30%   (venture debt 20-35% of last equity round, RBF for revenue-positive)
  Other:   0
  WACC:    14-18%

SERIES C+
  Equity:  60-75%   (later rounds, crossover)
  Debt:    25-40%   (ARR term loans, growth debt, mezzanine, revolving)
  Secondaries: 0-10% (founder + early-employee liquidity)
  WACC:    11-15%

LATE STAGE / IPO-TRACK
  Equity:  55-70%
  Debt:    30-45%   (sophisticated stack: term + revolver + convertibles)
  Secondaries: 5-15%
  WACC:    10-13%
  Optimized for public-market profile

PUBLIC (POST-IPO)
  Equity:  60-75%   (public + secondary issuances)
  Debt:    25-40%   (investment-grade bonds, revolvers)
  WACC:    8-12%
```

## Common recipes

### Recipe 1 — Compute WACC

```python
def wacc(weights, costs, tax_rate):
    """weights: {equity, debt, ...} sum to 1. costs: {equity, debt, ...} pre-tax."""
    wacc = 0
    for kind, weight in weights.items():
        cost = costs[kind]
        # Debt is tax-deductible; equity is not
        after_tax = cost * (1 - tax_rate) if "debt" in kind else cost
        wacc += weight * after_tax
    return wacc

# Series B SaaS: 80% equity at 16%, 15% venture debt at 9%, 5% RBF at 14%
weights = {"equity": 0.80, "debt_venture": 0.15, "debt_rbf": 0.05}
costs   = {"equity": 0.16, "debt_venture": 0.09, "debt_rbf": 0.14}
print(f"WACC: {wacc(weights, costs, tax_rate=0.21):.2%}")
```

### Recipe 2 — Cost of equity (CAPM)

```python
def cost_of_equity_capm(rf, beta, erp, country_risk_premium=0):
    return rf + beta * (erp + country_risk_premium)

# 2026: rf=3.7% (10yr UST), erp=5.5% (Damodaran), SaaS beta ~1.4
ke = cost_of_equity_capm(rf=0.037, beta=1.4, erp=0.055)
print(f"Cost of equity (SaaS Series B): {ke:.2%}")
```

### Recipe 3 — Cost of debt by instrument

```python
COST_OF_DEBT_2026 = {
    "venture_debt":     0.085,    # 8-10% + warrants (5-15% of loan amount)
    "growth_debt":      0.105,    # 10-12% + warrants
    "rbf":              0.16,     # 1.3-1.5× multiple → effective 12-20% APR
    "asset_term_loan":  0.075,    # ARR-multiple-based; senior secured
    "mezzanine":        0.13,     # PIK + cash interest
    "revolver":         0.065,    # SOFR + spread
    "founder_loan":     0.05,     # below-market
    "convertible_note": 0.06,     # cash int + conversion premium
}

# Convert to after-tax for WACC
def after_tax_cost_of_debt(pre_tax, tax_rate=0.21):
    return pre_tax * (1 - tax_rate)
```

### Recipe 4 — Optimal mix solver (minimize WACC under constraints)

```python
import numpy as np
from scipy.optimize import minimize

def optimal_capital_mix(equity_cost, debt_cost_after_tax, max_debt_ratio=0.35, tax_rate=0.21):
    """Minimize WACC subject to debt ratio ceiling (covenants + risk)."""
    def neg_wacc_objective(x):
        we, wd = x[0], x[1]
        return -(we * equity_cost + wd * debt_cost_after_tax) * -1  # minimize WACC = neg of neg

    def constraint_sum(x): return x[0] + x[1] - 1.0
    def constraint_max_debt(x): return max_debt_ratio - x[1]

    constraints = [
        {"type": "eq", "fun": constraint_sum},
        {"type": "ineq", "fun": constraint_max_debt}
    ]
    bounds = [(0, 1), (0, 1)]
    res = minimize(neg_wacc_objective, x0=[0.7, 0.3], bounds=bounds, constraints=constraints)
    return {"equity_weight": res.x[0], "debt_weight": res.x[1], "wacc": -res.fun}

# Series B example
ke = 0.16
kd_after_tax = 0.085 * (1 - 0.21)
print(optimal_capital_mix(ke, kd_after_tax, max_debt_ratio=0.30))
```

### Recipe 5 — Stage-graded recommended stack

```python
def recommended_stack(stage, arr=None, ebitda=None, predictability=None):
    if stage in ("pre-seed", "seed"):
        return {"equity": 0.90, "debt": 0.10, "rbf": 0.0, "secondaries": 0.0}
    if stage == "Series A":
        # Capital-efficient companies can take 20% venture debt
        if arr and arr > 1_000_000 and predictability == "high":
            return {"equity": 0.75, "debt": 0.20, "rbf": 0.05, "secondaries": 0.0}
        return {"equity": 0.85, "debt": 0.15, "rbf": 0.0, "secondaries": 0.0}
    if stage == "Series B":
        return {"equity": 0.70, "debt": 0.25, "rbf": 0.05, "secondaries": 0.0}
    if stage == "Series C":
        return {"equity": 0.60, "debt": 0.30, "rbf": 0.05, "secondaries": 0.05}
    if stage == "Late stage":
        return {"equity": 0.55, "debt": 0.35, "rbf": 0.05, "secondaries": 0.05}
    return {"equity": 1.0, "debt": 0, "rbf": 0, "secondaries": 0}

print(recommended_stack("Series B"))
```

### Recipe 6 — Debt capacity model

```python
def debt_capacity(monthly_arr, monthly_burn, gross_margin, target_dscr=2.0):
    """Debt service coverage ratio test: lender requires CFO ≥ 2× debt service."""
    annual_gross_profit = monthly_arr * 12 * gross_margin
    # Assume 50% of GP available for debt service (rest for opex)
    avail_for_debt = annual_gross_profit * 0.50
    max_annual_debt_service = avail_for_debt / target_dscr
    # Convert to principal: at 9% APR, 3yr term, monthly payments
    monthly_rate = 0.09 / 12
    n_payments = 36
    if monthly_rate > 0:
        principal_capacity = (max_annual_debt_service / 12) * (1 - (1 + monthly_rate) ** -n_payments) / monthly_rate
    else:
        principal_capacity = max_annual_debt_service * 3
    return {
        "annual_gross_profit": annual_gross_profit,
        "available_for_debt_service": avail_for_debt,
        "max_annual_debt_service": max_annual_debt_service,
        "principal_capacity": principal_capacity
    }

# $400K MRR, $450K burn, 78% GM
print(debt_capacity(400_000, 450_000, 0.78))
```

### Recipe 7 — Covenant model

```python
def model_covenants(actuals_df, covenant_rules):
    """Test covenant compliance.
    covenant_rules: dict of {metric_name: {threshold, direction}}"""
    results = []
    for _, row in actuals_df.iterrows():
        period_results = {"period": row["period"]}
        for metric, rule in covenant_rules.items():
            value = row.get(metric, None)
            if value is None: continue
            if rule["direction"] == ">=":
                period_results[metric] = "OK" if value >= rule["threshold"] else "BREACH"
            elif rule["direction"] == "<=":
                period_results[metric] = "OK" if value <= rule["threshold"] else "BREACH"
        results.append(period_results)
    return pd.DataFrame(results)

import pandas as pd
actuals = pd.DataFrame([
    {"period": "Q1 2026", "min_cash": 6_500_000, "min_arr": 4_000_000, "burn_multiple": 1.4},
    {"period": "Q2 2026", "min_cash": 5_800_000, "min_arr": 4_200_000, "burn_multiple": 1.35},
])
covenants = {
    "min_cash":      {"threshold": 5_000_000, "direction": ">="},
    "min_arr":       {"threshold": 3_500_000, "direction": ">="},
    "burn_multiple": {"threshold": 2.0, "direction": "<="},
}
print(model_covenants(actuals, covenants))
```

### Recipe 8 — Refinance analysis

```python
def refinance_analysis(current_principal, current_apr, current_remaining_months,
                       new_apr, new_principal, refi_fee_pct):
    """Does refinancing save money over the remaining term?"""
    refi_fee = new_principal * refi_fee_pct
    # Current: remaining interest
    current_monthly_rate = current_apr / 12
    current_remaining_interest = current_principal * current_monthly_rate * current_remaining_months
    # New (assume same maturity)
    new_monthly_rate = new_apr / 12
    new_total_interest = new_principal * new_monthly_rate * current_remaining_months
    savings = current_remaining_interest - new_total_interest - refi_fee
    return {
        "current_remaining_interest": current_remaining_interest,
        "new_total_interest": new_total_interest,
        "refi_fee": refi_fee,
        "net_savings": savings,
        "recommendation": "REFINANCE" if savings > 0 else "HOLD"
    }

print(refinance_analysis(3_000_000, 0.11, 24, 0.08, 3_000_000, 0.015))
```

### Recipe 9 — Secondaries planning

```python
def secondaries_plan(founder_holdings_pct, post_money_valuation, target_liquidity_pct=0.05):
    """Plan founder + early-employee secondary sale."""
    target_dollar = post_money_valuation * target_liquidity_pct
    founder_shares_to_sell_pct = target_dollar / (post_money_valuation * founder_holdings_pct)
    return {
        "target_dollar": target_dollar,
        "founder_shares_to_sell_pct_of_founder_holdings": founder_shares_to_sell_pct,
        "discount_to_round_typical": "10-25%",
        "platforms": ["Forge Global", "EquityZen", "Carta CrossFlow", "SecondMarket"],
        "tax_treatment": "LT cap gains if held >1yr; QSBS exclusion if qualifying"
    }

print(secondaries_plan(founder_holdings_pct=0.35, post_money_valuation=120_000_000))
```

## Examples

### Example 1: Series A $15M raise — should we add venture debt?

**Goal:** Maximize value via blended stack.

**Steps:**
1. Recipe 6 → debt capacity (~$3M based on current MRR / burn).
2. Recipe 1 → compare WACC: all-equity vs equity + $3M venture debt.
3. Recipe 7 → model covenants under bear scenario; ensure no breach.
4. Recipe 4 → optimal mix solver.
5. Recommendation: $12M equity + $3M venture debt → WACC ~14% vs 16% all-equity; saves 200bps cost of capital.

**Result:** Defensible blended stack memo.

### Example 2: Series C refinance

**Goal:** Existing $5M venture debt at 11%; refi at 8% with new lender.

**Steps:**
1. Recipe 8 → refinance economics; $300K+ savings.
2. Recipe 7 → cross-test new covenants; verify no tighter trip-wires.
3. Recipe 1 → new WACC under refinanced stack.
4. Approve refinance.

**Result:** Lower cost of capital.

## Edge cases / gotchas

- **WACC inputs noisy at startup stage.** Cost of equity 14-25% range. Use Damodaran 2026 datasets.
- **Venture debt warrants.** 5-15% of loan amount. Adds ~50-200bps to effective cost beyond stated APR.
- **Covenant breaches = serious.** Most venture debt has min cash, min ARR, no material adverse change. Bear-test before signing.
- **RBF is expensive but no equity dilution.** Trade-off: higher cash cost vs no ownership cost.
- **Refinance has fees.** OID, lender legal, transaction fees (1-3% of principal). Recipe 8 must include.
- **Secondaries hit cap-table dynamics.** ROFR (right of first refusal); may need preferred approval.
- **QSBS interaction with secondaries.** Secondary sale resets QSBS holding period clock for the buyer. Disclosure needed.
- **Public market WACC.** Will drop substantially post-IPO (8-12% vs 14-18% private). Plan capital structure with this trajectory.
- **Don't optimize WACC at expense of flexibility.** Higher debt = lower WACC mathematically; but covenants reduce strategic flexibility.
- **Damodaran cautions: "Capital structure follows strategy, not vice versa."** Don't lever up just because debt is cheap.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions.**

## Sources

- CFI capital stack structure: https://corporatefinanceinstitute.com/resources/financial-modeling/capital-stack-structure-debt-equity/
- Axis Group capital stack 2026: https://www.axisgroupventures.com/post/capital-stack-optimization-how-founders-are-blending-debt-equity-and-secondaries-in-2026
- Re-cap capital structure vs stack: https://www.re-cap.com/blog/capital-structure-vs-capital-stack
- Damodaran 2026 data home: https://pages.stern.nyu.edu/~adamodar/New_Home_Page/data.html
- Damodaran 2026 ERP: https://aswathdamodaran.substack.com/p/data-update-1-for-2026-the-push-and
- Founderpath venture debt: https://founderpath.com/learn
- Forge Global secondaries: https://forgeglobal.com

## Related skills

- `fundraising-strategy-priced-safe-venture-debt-rbf` — selects instruments.
- `term-sheet-nvca-grade-review` — reviews preferred + debt terms.
- `capital-allocation-framework` — what to do with raised capital.
- `treasury-yield-ladder-risk-tier` — debt covenants intersect with treasury policy.
