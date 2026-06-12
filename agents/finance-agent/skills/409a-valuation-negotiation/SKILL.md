<!--
Source: https://ctacquisitions.com/409a-valuation-methods/
Source: https://getexact.com/409a-valuation-guide/
Source: https://a16z.com/16-things-to-know-about-the-409a-valuation/
Source: https://acumensphere.com/blog/409a-valuation/top-409a-valuation-firms-in-2026
Reference role.md: "409A negotiation playbook"
-->

# 409A valuation negotiation — OPM/PWERM hybrid

Prepares the model and negotiation posture for a defensible 409A common-share valuation. 2026 SOTA: hybrid OPM/PWERM methodology; most private companies fall 12-20% equity discount rate; smaller/riskier 20-25%; late-stage 10-15%. Refresh annually or on material event (fundraise, M&A talks, IPO). Cost $3K-$8K. Top 2026 firms: Carta (~$2K/yr free with cap-table sub), Pulley (5-day delivery, $1K-$3.5K), Aranca, EquityEffect, Eqvista.

## When to use

- Annual 409A refresh due.
- Material event triggered refresh: priced round closed, M&A talks, IPO filing, transfer of large block.
- Negotiating discount rate with 409A provider.
- Pre-grant timing decision (issue ISOs before or after refresh).
- Trigger phrases: "409A", "common share FMV", "OPM", "PWERM", "strike price", "ISO valuation", "fair market value".

NOT for: cap-table mechanics (use Carta/Pulley directly); option pool design (use `equity-comp-design-pool-evergreen`).

## Setup

```bash
uvx --with pandas --with numpy --with scipy python -c "import pandas, scipy"

# Carta in-house 409A: free with cap-table subscription
# Pulley: $1K-$3.5K, 5-day delivery
# Aranca / EquityEffect / Eqvista: $3K-$8K external
```

## The methodology

### OPM (Option Pricing Method)

Treats common share as a call option on enterprise value with strike = liquidation preferences of preferred shares ahead of common. Black-Scholes formula.

```
Common share value per OPM:
  EV → allocated across preferred + common via option-payoff tranches
  Common = residual after all preferred liquidation prefs satisfied
  Apply DLOM (Discount for Lack of Marketability) typically 12-25%
```

### PWERM (Probability-Weighted Expected Return Method)

Lays out scenarios (IPO / strategic exit / acquihire / liquidation), probability-weights each, computes common share value per scenario, weights.

```
Common share value per PWERM:
  Σ (probability_i × common_share_value_in_scenario_i × discount_to_PV)
```

### Hybrid (2026 SOTA)

Most defensible. Use PWERM scenarios for near-term events (IPO/sale within 24mo); use OPM for "remain private" residual scenario.

## Common recipes

### Recipe 1 — Liquidation preference stack (input to OPM)

```python
import pandas as pd

def lp_stack(rounds_df):
    """Compute cumulative liquidation preference."""
    rounds_df = rounds_df.sort_values("seniority", ascending=False).copy()
    rounds_df["cumulative_lp"] = rounds_df["liquidation_preference"].cumsum()
    return rounds_df

rounds = pd.DataFrame([
    {"round": "Series B", "raise": 25_000_000, "lp_multiple": 1.0, "seniority": 3, "participation": "non-participating"},
    {"round": "Series A", "raise": 10_000_000, "lp_multiple": 1.0, "seniority": 2, "participation": "non-participating"},
    {"round": "Seed",     "raise": 3_000_000,  "lp_multiple": 1.0, "seniority": 1, "participation": "non-participating"},
])
rounds["liquidation_preference"] = rounds["raise"] * rounds["lp_multiple"]
print(lp_stack(rounds))
```

### Recipe 2 — OPM common share value (Black-Scholes call option)

```python
from scipy.stats import norm
import math

def opm_common_value(enterprise_value, lp_total, total_shares, common_shares,
                     volatility=0.65, risk_free=0.037, time_to_exit_years=4.0, dlom=0.20):
    """
    Common share value = (call option on EV with strike = LP_total) / common_shares
    Reduced by DLOM (discount for lack of marketability).
    """
    if enterprise_value <= 0:
        return 0
    K = lp_total
    S = enterprise_value
    T = time_to_exit_years
    sigma = volatility
    r = risk_free
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    call_value = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    # Allocate residual to common (simple approximation; full implementation per share class)
    common_total_value = call_value * (common_shares / total_shares)
    per_share = common_total_value / common_shares
    per_share_after_dlom = per_share * (1 - dlom)
    return per_share_after_dlom

# Example: $80M EV, $38M LP stack, 12M FD shares, 8M common
fmv = opm_common_value(80_000_000, 38_000_000, 12_000_000, 8_000_000, dlom=0.20)
print(f"Common share FMV (OPM): ${fmv:.2f}")
```

### Recipe 3 — PWERM scenarios

```python
def pwerm_common_value(scenarios):
    """scenarios: list of {label, prob, common_per_share_in_scenario, discount_to_pv}"""
    total = 0
    for s in scenarios:
        contrib = s["prob"] * s["common_per_share_in_scenario"] * s["discount_to_pv"]
        total += contrib
    return total

scenarios = [
    {"label": "IPO in 3yr",      "prob": 0.20, "common_per_share_in_scenario": 18.50, "discount_to_pv": 0.65},
    {"label": "Strategic sale 2yr", "prob": 0.35, "common_per_share_in_scenario": 9.20,  "discount_to_pv": 0.75},
    {"label": "Acquihire 3yr",   "prob": 0.15, "common_per_share_in_scenario": 2.10,  "discount_to_pv": 0.65},
    {"label": "Remain private",  "prob": 0.25, "common_per_share_in_scenario": 1.45,  "discount_to_pv": 1.00},
    {"label": "Liquidation",     "prob": 0.05, "common_per_share_in_scenario": 0.05,  "discount_to_pv": 0.70},
]
print(f"Common share FMV (PWERM): ${pwerm_common_value(scenarios):.2f}")
```

### Recipe 4 — Hybrid OPM/PWERM weight

```python
def hybrid_fmv(opm_value, pwerm_value, opm_weight=0.50):
    return opm_weight * opm_value + (1 - opm_weight) * pwerm_value

# Equal weighting common; tilt PWERM-heavy if near-term IPO/sale highly probable
print(f"Hybrid FMV: ${hybrid_fmv(2.85, 3.22, opm_weight=0.40):.2f}")
```

### Recipe 5 — Discount rate ladder

```python
def equity_discount_rate(stage, public_comparable=True, recent_round=True):
    """Returns equity discount rate range for 409A valuation."""
    if stage in ("pre-seed", "seed"):
        return (0.20, 0.25)  # 20-25%
    if stage in ("Series A", "Series B"):
        return (0.15, 0.20)  # 15-20%
    if stage in ("Series C", "Series D"):
        return (0.12, 0.17)  # 12-17%
    if stage in ("Late stage", "Pre-IPO"):
        return (0.10, 0.15)  # 10-15%
    return (0.15, 0.20)
```

### Recipe 6 — Strike price implication

```python
def strike_impact(option_count, fmv, vesting_years=4):
    """Quantify cost to employee if strike rises."""
    return {
        "strike_per_share": fmv,
        "total_strike_to_exercise": option_count * fmv,
        "tax_implication_amt": "AMT triggered on (FMV at exercise − strike) × shares — see CPA"
    }

print(strike_impact(50_000, 2.85))
```

### Recipe 7 — Refresh trigger checklist

```
Refresh required:
  □ Annual anniversary of last 409A
  □ Priced round closes (Seed/A/B/C)
  □ Convertible / SAFE conversion event
  □ M&A negotiation begins (term sheet received)
  □ IPO filing (S-1 confidential or public)
  □ Tender offer to employees
  □ Material change in business (pivot, large customer loss, major financing)

Refresh NOT required:
  □ New product launch
  □ Hire / departure (even C-level)
  □ Bridge SAFE (typically — confirm w/ provider)
  □ Routine option grants between refreshes
```

### Recipe 8 — Negotiation prep memo

```markdown
# 409A Negotiation Prep — Aug 2026

## Inputs
- Last 409A: Feb 2026 ($2.85/share); 6 months stale
- Refresh trigger: Series B negotiation (term sheet received Aug 1)
- Series B post-money: $120M
- Cap table: 12M FD shares, $38M LP stack post-A, 8M common
- Volatility (SaaS peer set): 0.62

## Methodology recommendation
Hybrid OPM (60%) + PWERM (40%). Series B closing makes near-term outcomes more crystalline.
PWERM scenarios: IPO 3yr (20%), strategic 2yr (35%), continue private (40%), down round (5%).
OPM with vol 0.62, time-to-exit 3yr, DLOM 20%.

## Target range
Common share FMV: $3.10 - $3.55
DLOM: 18-22% (justify with recent secondaries / restricted shares analysis)
Discount rate: 14-17% (Series B equity)

## Negotiation posture
- Push DLOM higher if minimal secondaries activity
- Push PWERM weight higher if IPO/sale truly probable in 24mo (boosts FMV — vs OPM at high vol)
- Push OPM weight higher to lower FMV (more conservative time-to-exit)
```

## Examples

### Example 1: Annual refresh for Series A SaaS

**Goal:** Defensible 409A common-share FMV.

**Steps:**
1. Recipe 1 → LP stack from cap table (Carta export).
2. Recipe 2 → OPM with stage-typical inputs (vol 0.55-0.70, time-to-exit 4yr, DLOM 18-22%).
3. Recipe 3 → PWERM if material near-term events likely.
4. Recipe 4 → hybrid weight.
5. Submit to Carta / Pulley / external; review final memo against Recipe 8 framework.

**Result:** Defensible FMV; strike for next ISO grant set.

### Example 2: Strike defense during S-1 prep

**Goal:** Justify last 12 months of 409A FMVs during IPO diligence.

**Steps:**
1. Pull every 409A memo from last 12 months.
2. Check refresh-trigger compliance (Recipe 7).
3. Test methodology consistency (Hybrid weights, vol, DLOM).
4. Tie each FMV to event chronology (round close, material change).
5. Build "FMV walk" tying ascending FMVs to enterprise-value milestones.

**Result:** Defense binder for SEC + underwriter Q&A.

## Edge cases / gotchas

- **Stale 409A is the #1 trap.** Material event between refresh and grant → grant fails Sec 409A safe harbor → 20% excise tax + interest on employees. Refresh before grant if any doubt.
- **High DLOM is defensible at early stages, hard at IPO.** Pre-Series A: 20-30%; Series A-B: 15-22%; Series C+: 12-18%; pre-IPO: 8-15%.
- **Volatility sourcing.** Use public-comp peer set median historical volatility (12-24mo). Source: yfinance, EDGAR, Bloomberg.
- **Time-to-exit assumption.** Drives OPM heavily. Typical 3-5yr; longer = higher FMV (more time for value); shorter = lower FMV (less option time).
- **PWERM probabilities must sum to 100%.** Easy to mis-weight; double-check.
- **Carta in-house vs external.** Carta in-house = free, fast; external = more conservative, more defensible in IPO/audit context. Many companies use Carta until Series C, then switch.
- **Refresh chronology matters for grants.** Always: refresh → board approves new strike → grant. Reverse order = risk.
- **AMT trap for employees.** ISO exercise: bargain element (FMV − strike) × shares triggers AMT. Employees exercising at high FMV may owe big AMT bill in April.
- **Hybrid weighting is judgment, not formula.** PWERM-heavy when near-term events are tangible; OPM-heavy when "remain private" dominates.
- **Don't backdate.** SOX + IRS take a dim view; SEC enforcement on equity backdating is severe.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions.**

## Sources

- CT Acquisitions 409A methods: https://ctacquisitions.com/409a-valuation-methods/
- Get Exact 409A guide 2026: https://getexact.com/409a-valuation-guide/
- A16Z 16 things to know about 409A: https://a16z.com/16-things-to-know-about-the-409a-valuation/
- Acumensphere top 2026 409A firms: https://acumensphere.com/blog/409a-valuation/top-409a-valuation-firms-in-2026
- IRS Section 409A: https://www.irs.gov/businesses/small-businesses-self-employed/section-409a-and-deferred-compensation
- Carta 409A: https://carta.com/409a/
- Pulley 409A: https://pulley.com/409a-valuation

## Related skills

- `equity-comp-design-pool-evergreen` — grants priced off this FMV.
- `term-sheet-nvca-grade-review` — preferred LPs drive OPM inputs.
- `ipo-readiness-s1-prep` — FMV walk is S-1 diligence.
- `tax-strategy-qsbs-rd-credit-holdco` — QSBS valuation date interaction.
