<!--
Source: https://beancount.io/blog/2026/05/10/saas-metrics-founders-must-track-2026-ltv-cac-nrr-churn-cac-payback-benchmarks-guide
Source: https://www.eaglerockcfo.com/blog/research/saas-finance-metrics-benchmarks
Reference role.md: "LTV cohort strategic playbook"
-->

# Customer LTV — strategic cohort + bottom-up

Computes LTV the right way: cohort-bottom-up, surfaced by segment and acquisition channel. Strategic version (this skill) drives fundraise / board / pricing decisions. (Operational metric pack lives in finance-controller's `unit-economics-saas-metrics`.) 2026 benchmarks: NRR ≥100% healthy / ≥120% elite; LTV:CAC ≥3:1 healthy / ≥5:1 elite.

## When to use

- Pre-fundraise: how to argue valuation upside via cohort LTV asymmetry.
- Board strategy: which segment / channel to double-down on, which to deprecate.
- Pricing change defense: model LTV impact of moving SMB tier.
- Sales-motion change defense: model LTV impact of moving upmarket.
- Trigger phrases: "cohort LTV", "segment economics", "channel ROI", "strategic LTV", "LTV by ICP".

NOT for: monthly metric pack (use finance-controller `unit-economics-saas-metrics`); cohort retention triangle build (use `driver-based-revenue-modeling`).

## Setup

```bash
uvx --with pandas --with numpy --with lifelines --with matplotlib python -c "import pandas, lifelines, matplotlib"
export STRIPE_API_KEY="<from Stripe Dashboard>"
export POSTHOG_API_KEY="<from PostHog Project Settings>"
```

## The strategic LTV stack

### LTV — three depths of precision

```
1. Naive (per investor deck — quick):
   LTV = ARPU_monthly × GM / monthly_churn_rate

2. Cohort-fitted (per board pack — defensible):
   LTV = Σ(month_t cohort_revenue × GM × discount_factor_t)
   where discount_factor_t = 1 / (1 + WACC_monthly)^t

3. Survival-curve (per Series B+ / IPO — rigorous):
   LTV = Σ(P(active at t) × ARPU_t × GM × discount_factor_t)
   P(active at t) fitted via Kaplan-Meier or Cox proportional hazards
```

### Segment / channel decomposition

```
                       SMB        Mid-market    Enterprise
ARPU monthly          $290        $1,400        $5,800
Logo churn / mo       3.0%        1.4%          0.6%
Gross margin          74%         78%           82%
LTV (naive)           $7,153      $78,000       $792,667
CAC                   $1,200      $14,000       $48,000
LTV:CAC               6.0:1       5.6:1         16.5:1
CAC payback (mo)      5.6         13.4          10.1
```

Same company, three different businesses.

## Common recipes

### Recipe 1 — Naive LTV (quick + dirty)

```python
def ltv_naive(arpu_monthly, gross_margin, monthly_churn_rate):
    if monthly_churn_rate <= 0:
        return float('inf')
    return (arpu_monthly * gross_margin) / monthly_churn_rate

print(ltv_naive(290, 0.74, 0.030))  # SMB → $7,153
```

### Recipe 2 — Cohort-fitted LTV (defensible)

```python
import pandas as pd

def ltv_cohort_fitted(cohort_revenue_curve, gross_margin, wacc_annual=0.12):
    wacc_monthly = (1 + wacc_annual) ** (1/12) - 1
    total = 0
    for t, rev in enumerate(cohort_revenue_curve, start=1):
        df = 1 / (1 + wacc_monthly) ** t
        total += rev * gross_margin * df
    return total

# Example: $100 cohort starts at $100/mo, retention curve fit
cohort_curve = [100, 95, 91, 88, 86, 84, 82, 81, 80, 79, 78, 77]  # 12 months
print(ltv_cohort_fitted(cohort_curve, 0.78))
```

### Recipe 3 — Survival-curve LTV (lifelines)

```python
from lifelines import KaplanMeierFitter
import numpy as np

def ltv_survival(durations, events, arpu_monthly, gross_margin, wacc_annual=0.12, horizon_months=60):
    kmf = KaplanMeierFitter()
    kmf.fit(durations=durations, event_observed=events)
    wacc_monthly = (1 + wacc_annual) ** (1/12) - 1
    total = 0
    for t in range(1, horizon_months + 1):
        try:
            p_active = kmf.survival_function_at_times(t).iloc[0]
        except Exception:
            p_active = 0
        df = 1 / (1 + wacc_monthly) ** t
        total += p_active * arpu_monthly * gross_margin * df
    return total

# durations = months_active, events = churned (0/1)
durations = pd.Series([3, 12, 8, 24, 36, 6, 18])
events = pd.Series([1, 1, 1, 0, 0, 1, 1])
print(ltv_survival(durations, events, 1400, 0.78))
```

### Recipe 4 — Segment LTV decomposition (Stripe data)

```python
import pandas as pd

customers = pd.read_csv("stripe_customers.csv")  # id, segment, mrr, gross_margin, churned_at, started_at

def segment_ltv(df):
    out = []
    for seg, g in df.groupby("segment"):
        n = len(g)
        churned = g["churned_at"].notna().sum()
        active_avg_months = (g["churned_at"].fillna(pd.Timestamp.today()) - g["started_at"]).dt.days.mean() / 30
        monthly_churn = churned / n / active_avg_months if active_avg_months else 0
        arpu = g["mrr"].mean()
        gm = g["gross_margin"].mean()
        ltv = ltv_naive(arpu, gm, monthly_churn) if monthly_churn else float('inf')
        out.append({"segment": seg, "n": n, "arpu": arpu, "monthly_churn": monthly_churn, "ltv": ltv})
    return pd.DataFrame(out)
```

### Recipe 5 — Channel LTV (CAC included)

```python
def channel_ltv_cac(df_cohort, channel_spend):
    """df_cohort: customer-level w/ channel + arpu + churned. channel_spend: dict channel→$"""
    out = []
    for ch, g in df_cohort.groupby("channel"):
        ltv = segment_ltv(g.assign(segment=ch))
        cac = channel_spend[ch] / len(g) if len(g) else float('inf')
        out.append({"channel": ch, "n": len(g), "ltv": ltv.iloc[0]["ltv"], "cac": cac,
                    "ltv_cac": ltv.iloc[0]["ltv"] / cac if cac > 0 else float('inf')})
    return pd.DataFrame(out)
```

### Recipe 6 — Expansion-adjusted LTV (NRR > 100%)

```python
def ltv_with_expansion(arpu_monthly, gross_margin, monthly_churn_rate, monthly_expansion_rate, wacc_annual=0.12):
    """Net retention = (1 - churn) × (1 + expansion). When NRR > 100%, LTV is theoretically infinite,
    so cap at 60-month horizon for usable answer."""
    wacc_monthly = (1 + wacc_annual) ** (1/12) - 1
    total = 0
    arpu = arpu_monthly
    survival = 1.0
    for t in range(1, 61):
        df = 1 / (1 + wacc_monthly) ** t
        total += survival * arpu * gross_margin * df
        survival *= (1 - monthly_churn_rate)
        arpu *= (1 + monthly_expansion_rate)
    return total

# Example: 1.4%/mo expansion + 0.6% churn → NRR ≈ 110% annualized
print(ltv_with_expansion(5800, 0.82, 0.006, 0.014))
```

### Recipe 7 — Strategic decision matrix (segment-level)

```python
def segment_strategic_matrix(segment_df):
    out = []
    for _, r in segment_df.iterrows():
        if r["ltv_cac"] >= 5.0 and r["cac_payback"] < 12:
            verdict = "DOUBLE DOWN"
        elif r["ltv_cac"] >= 3.0 and r["cac_payback"] < 18:
            verdict = "INVEST"
        elif r["ltv_cac"] >= 2.0 and r["cac_payback"] < 24:
            verdict = "HOLD"
        else:
            verdict = "DEPRECATE / REPRICE"
        out.append({**r.to_dict(), "verdict": verdict})
    return pd.DataFrame(out)
```

### Recipe 8 — Pricing-change LTV impact

```python
def pricing_change_ltv(baseline_arpu, new_arpu, baseline_churn_mo, elasticity, gm, wacc_annual=0.12):
    """elasticity: absolute pp churn lift per 25% price increase"""
    pct_change = (new_arpu - baseline_arpu) / baseline_arpu
    churn_lift = elasticity * (pct_change / 0.25)
    new_churn = baseline_churn_mo + churn_lift
    return {
        "baseline_ltv": ltv_naive(baseline_arpu, gm, baseline_churn_mo),
        "new_ltv":      ltv_naive(new_arpu, gm, new_churn),
        "churn_lift":   churn_lift,
        "pct_change_price": pct_change,
    }

# Raise SMB price 25% with elasticity 0.5pp/25%
print(pricing_change_ltv(290, 363, 0.030, 0.005, 0.74))
```

## Examples

### Example 1: Series B raise — argue valuation upside via segment LTV

**Goal:** Show why enterprise segment LTV justifies 12× ARR multiple vs SMB-blended 8×.

**Steps:**
1. Recipe 4 → segment LTV table (SMB / Mid / Enterprise).
2. Recipe 5 → channel LTV (paid / organic / partner).
3. Recipe 7 → strategic matrix.
4. Frame: "Enterprise is 30% of ARR but 60% of LTV; investors should value blended at 11× given enterprise multiple expansion."
5. Stress test with `scenario-planning-monte-carlo` (LTV under bear churn).

**Result:** Valuation argument grounded in cohort math, not vibes.

### Example 2: Pricing change defense

**Goal:** Show that 25% price lift on SMB tier is net-positive even at 2× elasticity.

**Steps:**
1. Recipe 8 → run baseline vs price+25% with elasticity 0.5pp.
2. Repeat at elasticity 1.0pp (2× expected).
3. Compute LTV delta per scenario.
4. Pair with CAC unchanged → new LTV:CAC.
5. Recommend if LTV:CAC remains ≥3:1 even at 2× elasticity.

**Result:** Defensible pricing-change memo.

## Edge cases / gotchas

- **LTV horizon matters.** Naive formula assumes infinite horizon; for high-NRR or expansion-heavy businesses, cap at 60 months — investors discount infinite LTV.
- **Discount rate must match company WACC.** Using flat 10% when WACC is 14% inflates LTV.
- **Segment definitions must be stable.** "Mid-market" today vs 2 years ago must use same revenue band. Re-tag historicals if you change bands.
- **Expansion LTV at NRR > 100%.** Math diverges to infinity. Always cap horizon.
- **CAC denominator misuse.** "New logos" = closed-won net-new. Exclude expansion deals; they're not acquisitions.
- **Channel CAC needs fully-loaded S&M attribution.** Direct ad spend + sales-team allocation by channel + tools + content. Don't undercount.
- **Cohort-fitted LTV requires 18+ months of history.** Younger cohorts → use survival fit (Recipe 3) with confidence intervals.
- **Don't compare LTV across companies with different definitions.** Bessemer / SaaStr / Eagle Rock use slightly different formulas; pick one and stick.
- **Gross margin must exclude S&M.** GM = (Revenue - COGS) / Revenue. Including S&M in COGS = wrong.
- **Discount factor convention.** Annual vs monthly; check before reporting.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions.**

## Sources

- 2026 SaaS metrics: https://beancount.io/blog/2026/05/10/saas-metrics-founders-must-track-2026-ltv-cac-nrr-churn-cac-payback-benchmarks-guide
- Eagle Rock CFO benchmarks: https://www.eaglerockcfo.com/blog/research/saas-finance-metrics-benchmarks
- Bessemer Burn Multiple + LTV: https://www.bvp.com/atlas
- David Skok SaaS metrics canon: https://www.forentrepreneurs.com/saas-metrics-2/
- lifelines: https://lifelines.readthedocs.io/
- Stripe Sigma: https://docs.stripe.com/sigma
- PostHog cohorts: https://posthog.com/docs/product-analytics/cohorts

## Related skills

- `driver-based-revenue-modeling` — feeds cohorts.
- `market-sizing-tam-sam-som-strategic` — segment LTV → SAM by segment.
- `pitch-deck-financial-slides` — surfaces this skill's output.
- `scenario-planning-monte-carlo` — sensitizes LTV inputs.
