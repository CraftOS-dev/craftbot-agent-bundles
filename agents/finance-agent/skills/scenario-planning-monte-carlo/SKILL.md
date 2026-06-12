<!--
Source: https://bussinology.com/startups/financial-model-startup-sensitivity-analysis/
Source: https://www.thewallstreetschool.com/blog/sensitivity-analysis-finance-guide/
Source: https://clickup.com/blog/monte-carlo-simulation-software/
Reference role.md: "Scenario and Monte Carlo playbook"
-->

# Scenario planning + Monte Carlo simulation

Generates Base / Bull / Bear scenarios + sensitivity tornado + Monte Carlo simulation on top of the tied three-statement model. Surfaces results as probability distributions ("P(runway < 12 months) = 18%") rather than single-point estimates. 2026 standard: read results as odds, not anxiety.

## When to use

- Board / investor scenario package (base / bull / bear + sensitivities).
- Pre-fundraise risk surfacing — what could go wrong, with what probability.
- Pre-M&A diligence — sensitivity of valuation to assumption variance.
- Treasury allocation under interest-rate / yield-curve uncertainty.
- Trigger phrases: "scenarios", "sensitivity", "tornado chart", "Monte Carlo", "what-if", "stress test", "P(X)".

NOT for: revenue model itself (use `driver-based-revenue-modeling`); the IS/BS/CF (use `three-statement-financial-model-tied`).

## Setup

```bash
uvx --with numpy --with scipy --with pandas --with matplotlib python -c "import numpy, scipy, pandas, matplotlib"
```

For Causal / Mosaic native scenario builders, use platform UI (no scripting needed) but export results to PNG/PDF for board pack.

## The framework

### Three named scenarios (flex same 8-10 drivers)

```
Driver               Base       Bull       Bear
─────────────────────────────────────────────────
Revenue growth MoM    5.0%       7.5%       2.5%
NRR (TTM)            118%       125%       100%
Logo churn / mo      1.5%       1.0%       2.5%
ACV ($)              24,000     26,000     21,000
New logos / mo       22         28         15
Gross margin         78%        80%        72%
S&M as % rev         42%        38%        48%
CAC payback (mo)     14         11         20
CapEx / FTE          2,000      2,500      1,500
Headcount EoY        102        118        88
─────────────────────────────────────────────────
```

Each scenario rolls through IS/BS/CF → produces ending cash, runway, ARR, EBITDA, burn multiple.

### Sensitivity tornado (one variable at a time)

Vary ONE driver ±20% (others fixed at Base); plot impact on target (typically `Runway months`). Rank by impact magnitude → tornado chart.

### Monte Carlo (joint variance)

Draw 1K-10K trials from probability distributions; surface as percentiles.

## Common recipes

### Recipe 1 — Build scenario table

```python
import pandas as pd

scenarios = pd.DataFrame({
    "driver": ["growth_mom", "nrr_ttm", "churn_mo", "acv", "logos_mo",
               "gm_pct", "sm_pct", "cac_payback_mo", "capex_per_fte", "headcount_eoy"],
    "base":   [0.050, 1.18, 0.015, 24000, 22, 0.78, 0.42, 14, 2000, 102],
    "bull":   [0.075, 1.25, 0.010, 26000, 28, 0.80, 0.38, 11, 2500, 118],
    "bear":   [0.025, 1.00, 0.025, 21000, 15, 0.72, 0.48, 20, 1500, 88],
})
```

### Recipe 2 — Roll a scenario through 24 months

```python
def roll_scenario(drivers, starting_arr, starting_cash, months=24):
    arr = starting_arr
    cash = starting_cash
    history = []
    nrr_monthly = drivers["nrr_ttm"] ** (1/12)
    for m in range(1, months + 1):
        retained_arr = arr * nrr_monthly
        new_arr = drivers["logos_mo"] * drivers["acv"]
        arr = retained_arr + new_arr
        monthly_revenue = arr / 12
        cogs = monthly_revenue * (1 - drivers["gm_pct"])
        opex = monthly_revenue * (drivers["sm_pct"] + 0.40)
        ebitda = monthly_revenue - cogs - opex
        cash += ebitda - (drivers["capex_per_fte"] * drivers["headcount_eoy"] / 12)
        history.append({"month": m, "arr": arr, "cash": cash, "ebitda": ebitda})
    return pd.DataFrame(history)
```

### Recipe 3 — Runway months

```python
def runway_months(history_df):
    negative = history_df[history_df["cash"] < 0]
    if negative.empty: return float('inf')
    return int(negative.iloc[0]["month"])
```

### Recipe 4 — Sensitivity tornado

```python
def sensitivity_tornado(base_drivers, driver_names, target_fn, delta=0.20):
    base_target = target_fn(base_drivers)
    impacts = []
    for d in driver_names:
        up = dict(base_drivers); up[d] = base_drivers[d] * (1 + delta)
        dn = dict(base_drivers); dn[d] = base_drivers[d] * (1 - delta)
        impacts.append({
            "driver": d,
            "up": target_fn(up) - base_target,
            "dn": target_fn(dn) - base_target,
        })
    df = pd.DataFrame(impacts)
    df["abs"] = df["up"].abs() + df["dn"].abs()
    return df.sort_values("abs", ascending=False)
```

### Recipe 5 — Plot tornado (matplotlib)

```python
import matplotlib.pyplot as plt

def plot_tornado(df, save="tornado.png"):
    fig, ax = plt.subplots(figsize=(8, 5))
    y = range(len(df))
    ax.barh(y, df["up"], color="green", label="+20%")
    ax.barh(y, df["dn"], color="red", label="-20%")
    ax.set_yticks(list(y)); ax.set_yticklabels(df["driver"])
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_xlabel("Δ Runway months"); ax.legend()
    plt.tight_layout(); plt.savefig(save, dpi=150)
    return save
```

### Recipe 6 — Monte Carlo on top drivers

```python
import numpy as np

def monte_carlo_runway(base_drivers, n_trials=5000):
    rng = np.random.default_rng(seed=42)
    results = []
    for _ in range(n_trials):
        drivers = dict(base_drivers)
        drivers["nrr_ttm"] = max(0.7, rng.normal(1.18, 0.06))
        drivers["logos_mo"] = max(0, rng.normal(22, 5))
        drivers["acv"] = max(8000, rng.normal(24000, 3000))
        drivers["gm_pct"] = np.clip(rng.normal(0.78, 0.03), 0.50, 0.90)
        drivers["sm_pct"] = np.clip(rng.normal(0.42, 0.05), 0.20, 0.65)
        h = roll_scenario(drivers, 4_200_000, 8_500_000, months=36)
        results.append(runway_months(h))
    return np.array(results)

trials = monte_carlo_runway(base_drivers)
print(f"P5: {np.percentile(trials, 5):.0f}mo")
print(f"P50: {np.percentile(trials, 50):.0f}mo")
print(f"P(runway < 18mo): {(trials < 18).mean():.1%}")
```

### Recipe 7 — Scenario comparison table

```python
def scenario_summary(scenarios_df, target_fn):
    rows = []
    for scenario in ["base", "bull", "bear"]:
        drivers = {row["driver"]: row[scenario] for _, row in scenarios_df.iterrows()}
        rows.append({
            "scenario": scenario,
            "runway_mo": runway_months(roll_scenario(drivers, 4_200_000, 8_500_000, 36)),
            "ending_arr_24mo": roll_scenario(drivers, 4_200_000, 8_500_000, 24)["arr"].iloc[-1],
        })
    return pd.DataFrame(rows)
```

### Recipe 8 — Excel 2-variable sensitivity table

```python
nrr_range = [1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30]
logos_range = [10, 15, 20, 25, 30]
grid = []
for nrr in nrr_range:
    row = []
    for logos in logos_range:
        d = dict(base_drivers); d["nrr_ttm"] = nrr; d["logos_mo"] = logos
        row.append(runway_months(roll_scenario(d, 4_200_000, 8_500_000, 36)))
    grid.append(row)
grid_df = pd.DataFrame(grid,
    index=[f"NRR {x:.0%}" for x in nrr_range],
    columns=[f"{l} logos/mo" for l in logos_range])
```

### Recipe 9 — Board-ready framing

```
Base:   24 months runway, ARR $9.8M EoY2
Bull:   38 months runway, ARR $14.2M EoY2 (raise at +50% valuation)
Bear:   14 months runway, ARR $6.8M EoY2 (cut burn 25% or bridge by mo 10)

Monte Carlo:
  P(runway < 12mo) = 8%
  P(runway < 18mo) = 22%  → bridge plan needed
  P(ARR > $12M)    = 41%  → bull plausible

Recommendation: Raise Series B starting month 9 at $12M ARR target;
  fallback bridge from existing investors at month 14 if growth < base.
```

## Examples

### Example 1: Series B raise — scenario package

**Goal:** Investor-ready scenario deck for $25M Series B.

**Steps:**
1. Recipe 1 → scenario table; stage-graded benchmarks.
2. Recipe 2 → roll each through 36 months.
3. Recipe 7 → summary table.
4. Recipe 4-5 → tornado chart on Runway.
5. Recipe 6 → Monte Carlo with P5/P25/P50/P75/P95.
6. Recipe 9 → board-ready framing.

**Result:** 3-slide scenario pack: table, tornado, Monte Carlo distribution.

### Example 2: Treasury yield uncertainty

**Goal:** If yields fall 50bps, impact on interest income FY26.

**Steps:**
1. Drivers: yield curve (1M, 3M, 6M, 12M); allocation per tier.
2. Run 3 scenarios: yields flat / -50bps / -100bps.
3. Compute annualized interest income for each.
4. Sensitize allocation mix (50/30/20 vs 70/20/10 short/mid/long).
5. Pick allocation that maintains target yield under -50bps.

**Result:** Defensible allocation surviving plausible yield decline.

## Edge cases / gotchas

- **Distribution choice matters.** Normal works for most; lognormal for skewed (ACV); beta for bounded (churn 0-100%). Wrong shape → wrong tail risk.
- **Independence assumption is wrong.** NRR and churn correlate; logos and ACV correlate. Naive Monte Carlo overstates dispersion. Use copulas for production.
- **Number of trials.** 1K for board; 10K for IPO. Beyond 10K diminishing returns.
- **Seed reproducibility.** Always set `seed=42` so board can re-run.
- **No single-point estimates for risky drivers.** Investors penalize false precision.
- **Bear must be plausible, not catastrophic.** Use 1-2σ downside, not 3σ.
- **Bull must be aspirational, not stretch.** Top-quartile execution of same plan.
- **Three statements must stay tied in every scenario.** Easy to break BS in bear (AR/AP squeezes). Re-run checks.
- **Headcount lags revenue.** Cuts have 1-2 mo lag (severance). Model it.
- **Driver correlation.** S&M cuts in bear → lower logos → lower ARR. Don't only flex top-level.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions.**

## Sources

- Bussinology sensitivity for startups: https://bussinology.com/startups/financial-model-startup-sensitivity-analysis/
- WallStreet School sensitivity: https://www.thewallstreetschool.com/blog/sensitivity-analysis-finance-guide/
- ClickUp Monte Carlo software: https://clickup.com/blog/monte-carlo-simulation-software/
- NumPy random: https://numpy.org/doc/stable/reference/random/index.html
- SciPy stats: https://docs.scipy.org/doc/scipy/reference/stats.html
- Causal scenarios: https://www.causal.app/scenarios
- Mosaic scenarios: https://www.mosaic.tech/product/scenarios

## Related skills

- `three-statement-financial-model-tied` — the model that scenarios roll through.
- `driver-based-revenue-modeling` — drivers that get flexed.
- `capital-structure-debt-equity-mix-stage` — sensitivity on WACC.
- `treasury-yield-ladder-risk-tier` — yield-curve scenarios.
