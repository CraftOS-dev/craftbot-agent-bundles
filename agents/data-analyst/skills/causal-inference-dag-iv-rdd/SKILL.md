<!--
DoWhy: https://www.pywhy.org/dowhy/
linearmodels: https://bashtage.github.io/linearmodels/
CausalImpact: https://google.github.io/CausalImpact/
EconML: https://econml.azurewebsites.net/
Companion: role.md → "Causal inference playbook"
-->

# Causal inference — DAGs, IV, RDD, DiD, synthetic control, double ML

When you can't run an RCT but still need to answer "did X cause Y?". Tools: DoWhy for DAG-based identification + estimation, linearmodels for 2SLS instrumental variables and Panel OLS difference-in-differences, CausalImpact for synthetic control on time series, EconML for heterogeneous treatment effects via double ML.

## When to use

- "Did campaign / launch / price change / outage cause the metric move?"
- "We can't randomize — how confident can we be in this estimate?"
- "Need to control for confounders we can name"
- "Two-stage least squares for endogenous treatment" (IV)
- "Regression discontinuity around a cutoff" (RDD)
- "Synthetic control for a time-series intervention" (CausalImpact)
- "Heterogeneous treatment effect per segment" (EconML CATE)

Defer A/B test math (gold-standard RCT) to `ab-test-significance-mde-sequential`. Defer Bayesian primitives to `bayesian-pymc-numpyro-ab-testing`. Defer MMM to `attribution-multi-touch-mmm`.

## Setup

```bash
pip install dowhy                       # DAG-based identification + estimation
pip install linearmodels                # 2SLS, Panel OLS, fixed effects
pip install pycausalimpact              # Google's CausalImpact Python port
pip install econml                      # heterogeneous treatment effects
pip install statsmodels                 # OLS + RDD primitives
pip install rdrobust                    # local-linear RDD with optimal bandwidth
pip install graphviz                    # DAG visualization (system: brew install graphviz)
```

## Method-selection ladder

| Strongest → Weakest | Method | When |
|---|---|---|
| 1 | **RCT (A/B)** | You can randomize |
| 2 | **RDD** | Sharp cutoff in treatment assignment (passing a threshold) |
| 3 | **DiD** | Pre/post × treated/control with parallel trends |
| 4 | **IV (2SLS)** | Instrument affects treatment but not outcome directly |
| 5 | **Synthetic control** | Single treated unit, many controls, time-series |
| 6 | **Propensity score matching** | Match on probability of treatment |
| 7 | **OLS with controls** | Observational; "no unobserved confounders" — rarely true |

## Common recipes

### Recipe 1 — DoWhy DAG-based workflow (the safety-rail)

```python
from dowhy import CausalModel
import pandas as pd

# Step 1: draw a DAG of the data-generating process
graph = """
digraph {
    age -> campaign_exposed;
    age -> conversion;
    plan -> campaign_exposed;
    plan -> conversion;
    tenure -> conversion;
    campaign_exposed -> conversion;
}
"""

model = CausalModel(
    data=df,
    treatment="campaign_exposed",
    outcome="conversion",
    common_causes=["age", "plan", "tenure"],
    graph=graph,
)
model.view_model()                              # renders DAG

# Step 2: identify (what assumptions are needed?)
identified_estimand = model.identify_effect()
print(identified_estimand)

# Step 3: estimate
estimate = model.estimate_effect(
    identified_estimand,
    method_name="backdoor.propensity_score_matching",   # or "linear_regression", "doubly_robust"
)
print(f"Estimated ATE: {estimate.value:.4f}")

# Step 4: refute (sensitivity / placebo)
refute_placebo = model.refute_estimate(
    identified_estimand, estimate,
    method_name="placebo_treatment_refuter", placebo_type="permute"
)
refute_subset = model.refute_estimate(
    identified_estimand, estimate,
    method_name="data_subset_refuter", subset_fraction=0.8
)
refute_unobserved = model.refute_estimate(
    identified_estimand, estimate,
    method_name="add_unobserved_common_cause",
    confounders_effect_on_treatment="binary_flip",
    confounders_effect_on_outcome="linear",
    effect_strength_on_treatment=0.05, effect_strength_on_outcome=0.05,
)
print(refute_placebo, refute_subset, refute_unobserved)
```

### Recipe 2 — Instrumental Variables (2SLS) with linearmodels

```python
from linearmodels.iv import IV2SLS

# Setting: estimate effect of `treatment` on `outcome`,
# `treatment` correlated with unobserved confounder
# `instrument` correlated with treatment but only affects outcome through treatment

formula = "outcome ~ 1 + exog_controls + [treatment ~ instrument]"
res = IV2SLS.from_formula(formula, df).fit(cov_type="robust")
print(res.summary)

# Diagnostics:
# 1) First-stage F-statistic > 10 (weak instrument check)
# 2) Sargan / Hansen J-test for over-identification (if multiple instruments)
print("First-stage F:", res.first_stage.diagnostics)
print("J-stat:", res.j_stat)
```

### Recipe 3 — Difference-in-Differences (Panel OLS)

```python
from linearmodels.panel import PanelOLS

# Panel data: each row = (unit, time), with treatment indicator + post indicator
df_panel = df.set_index(["unit_id", "date"])

# Two-way fixed effects DiD: includes unit + time FE
model = PanelOLS.from_formula(
    "outcome ~ treated * post + EntityEffects + TimeEffects",
    data=df_panel,
)
res = model.fit(cov_type="clustered", cluster_entity=True)
print(res.summary)
# Coefficient on `treated:post` = DiD ATE estimate
```

### Recipe 4 — Parallel trends check

```python
import matplotlib.pyplot as plt

# Pre-treatment trend should be parallel between treated and control
pre = df[df.post == 0]
trend = pre.groupby(["treated", "date"])["outcome"].mean().unstack(0)
trend.plot(figsize=(10, 5))
plt.axvline(treatment_date, color="red", linestyle="--", label="Treatment")
plt.title("Pre-treatment parallel trends check")
plt.legend(); plt.savefig("parallel_trends.png")

# Quantitative: pre-treatment placebo DiD should be ≈ 0
df_pre = df[df.date < treatment_date]
df_pre["fake_post"] = df_pre.date >= (treatment_date - pd.Timedelta(days=30))
model_pre = PanelOLS.from_formula(
    "outcome ~ treated * fake_post + EntityEffects + TimeEffects",
    data=df_pre.set_index(["unit_id", "date"])
)
print("Placebo DiD (should be ~0):", model_pre.fit(cov_type="clustered", cluster_entity=True).params)
```

### Recipe 5 — Regression Discontinuity Design (RDD)

```python
import statsmodels.api as sm
import numpy as np

# Sharp RDD: treatment = 1 if running_variable >= cutoff
cutoff = 70
df["treated"] = (df["score"] >= cutoff).astype(int)
df["x_centered"] = df["score"] - cutoff

# Local linear regression near the cutoff (bandwidth h)
h = 10
local = df[df["x_centered"].abs() <= h].copy()
local["x_treated"] = local["x_centered"] * local["treated"]

X = sm.add_constant(local[["x_centered", "treated", "x_treated"]])
y = local["outcome"]
res = sm.OLS(y, X).fit(cov_type="HC1")
print(res.summary())
# Coefficient on `treated` = LATE at the cutoff
```

For optimal-bandwidth RDD: install `rdrobust`:

```python
from rdrobust import rdrobust

result = rdrobust(y=df["outcome"], x=df["score"], c=cutoff, deriv=0)
print(result)
# Returns: coef, bias-corrected coef, robust SE, optimal bandwidth (Imbens-Kalyanaraman / CCT)
```

### Recipe 6 — Synthetic control via CausalImpact

```python
from causalimpact import CausalImpact
import pandas as pd

# Build wide DataFrame: response in col 0, covariates (other markets) in subsequent cols
data = pd.DataFrame({
    "treated_market": series_treated,
    "control_market_1": series_c1,
    "control_market_2": series_c2,
    "control_market_3": series_c3,
})

pre_period = ["2025-01-01", "2026-03-31"]      # before intervention
post_period = ["2026-04-01", "2026-06-09"]     # after intervention

ci = CausalImpact(data, pre_period, post_period)
print(ci.summary())
print(ci.summary("report"))      # human-readable narrative
ci.plot()                         # 3 panels: actual vs counterfactual, point effect, cumulative effect
```

The Bayesian structural time-series model fits a synthetic control from the donor pool (control markets) and reports the cumulative causal effect with credible intervals.

### Recipe 7 — Doubly Robust + Double ML (EconML)

```python
from econml.dml import LinearDML, CausalForestDML
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier

# Step 1: Linear DML for ATE
est = LinearDML(
    model_y=GradientBoostingRegressor(),
    model_t=GradientBoostingClassifier(),
    discrete_treatment=True,
)
est.fit(Y=df["outcome"], T=df["treatment"], X=df[features], W=df[controls])
print("ATE:", est.ate(X=df[features]))
print("ATE CI:", est.ate_interval(X=df[features], alpha=0.05))

# Step 2: Heterogeneous effects (CATE)
forest = CausalForestDML(
    model_y=GradientBoostingRegressor(),
    model_t=GradientBoostingClassifier(),
    discrete_treatment=True,
    n_estimators=500, min_samples_leaf=50,
)
forest.fit(Y=df["outcome"], T=df["treatment"], X=df[features], W=df[controls])

# Predict CATE for each sample
df["cate"] = forest.effect(X=df[features])
print("Top 10 highest-CATE units:", df.nlargest(10, "cate"))
```

### Recipe 8 — Propensity Score Matching (PSM)

```python
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
import numpy as np

# Estimate propensity (P(treated | X))
ps_model = LogisticRegression(max_iter=1000)
ps_model.fit(df[features], df["treated"])
df["propensity"] = ps_model.predict_proba(df[features])[:, 1]

# Match each treated to nearest-propensity control
treated = df[df.treated == 1].copy()
control = df[df.treated == 0].copy()

nn = NearestNeighbors(n_neighbors=1).fit(control[["propensity"]])
distances, idx = nn.kneighbors(treated[["propensity"]])
matched_control = control.iloc[idx.flatten()].reset_index(drop=True)

# ATT: average difference in outcome among matched
att = (treated["outcome"].values - matched_control["outcome"].values).mean()
print(f"ATT estimate: {att:.4f}")

# Check covariate balance pre vs post matching (standardized mean diff)
for f in features:
    before = (df[df.treated == 1][f].mean() - df[df.treated == 0][f].mean()) / df[f].std()
    after  = (treated[f].mean() - matched_control[f].mean()) / df[f].std()
    print(f"{f}: SMD before={before:+.3f}, after={after:+.3f}")
```

### Recipe 9 — Sensitivity analysis (Rosenbaum bounds + e-value)

```python
# E-value: how strong would an unmeasured confounder need to be to nullify the estimate?
def e_value(rr_estimate, rr_ci_lower):
    """Compute E-value for a risk ratio."""
    if rr_estimate > 1:
        e = rr_estimate + (rr_estimate * (rr_estimate - 1)) ** 0.5
        e_ci = max(1, rr_ci_lower + (rr_ci_lower * (rr_ci_lower - 1)) ** 0.5)
    else:
        rr_inv = 1 / rr_estimate
        e = rr_inv + (rr_inv * (rr_inv - 1)) ** 0.5
        e_ci = 1
    return e, e_ci

# For an OR/RR estimate of 1.8 with CI [1.5, 2.2]
e, e_ci = e_value(1.8, 1.5)
print(f"E-value: {e:.2f} (CI: {e_ci:.2f})")
# Interpretation: a confounder must have RR ≥ E with both T and Y to explain away the effect
```

### Recipe 10 — Causal report template

```
CAUSAL QUESTION: <did treatment X affect outcome Y?>

DAG:                <visual or text — list all assumed common causes>

IDENTIFICATION:     <RCT / RDD / DiD / IV / SCM / PSM / OLS-with-controls>
ASSUMPTIONS:        <list, e.g., "parallel trends pre-treatment", "exogenous instrument", "SUTVA">

ESTIMATE (ATE/ATT/LATE): <point estimate>
95% CI:             [<lower>, <upper>]
SE:                 <standard error>

DIAGNOSTICS:
- <e.g., first-stage F = X (>10 if IV)>
- <parallel trends plot — visually parallel?>
- <covariate balance — SMD < 0.1 post-matching?>
- <residual normality / heteroskedasticity>

SENSITIVITY:
- E-value: <X> (confounder strength needed to nullify)
- Placebo test: <result>
- Subset robustness: <ATE varies between X and Y when subsetting>

VIOLATIONS / CAVEATS:
- <unobserved confounders we can't rule out>
- <selection mechanisms — who got treated?>
- <SUTVA violations — network effects?>

RECOMMENDED ACTIONS:
- Validate via RCT before scaling intervention
- Re-estimate when (data X, control Y) becomes available
```

## Example end-to-end

**Goal:** Did our paid-search bidding increase on March 1st cause the conversion lift?

1. Draw DAG: spend → impressions → clicks → conversions; with confounders (seasonality, brand interest).
2. Identify: no RCT possible (we can't randomize spend by user). Time-series intervention → synthetic control via CausalImpact.
3. Donor pool: organic-search traffic in unaffected markets as controls.
4. Run `CausalImpact(data, pre, post)` — Recipe 6.
5. Output: counterfactual baseline + 95% credible interval; cumulative effect = +$420k (CI [$280k, $560k]).
6. Sensitivity: re-fit excluding noisy donor markets — ATE robust.
7. Placebo: shift "treatment date" 30 days pre — placebo effect ≈ 0 (good).
8. Report per Recipe 10 template; recommend running geo-holdout to validate.

## Edge cases / gotchas

- **DAG mis-specification** — wrong DAG → wrong identification → wrong estimate. Draft DAG explicitly, get domain review.
- **"No unobserved confounders" assumption** — usually wrong in pure observational. Always quantify via E-value / Rosenbaum bounds.
- **Weak instrument problem** — first-stage F < 10 → 2SLS coefficient explodes; use weak-IV-robust inference (Anderson-Rubin).
- **Parallel trends violation** — if pre-trends diverge, DiD is invalid. Consider event-study (multiple pre-leads + post-lags) for visual diagnosis.
- **Discontinuity at the cutoff isn't smooth** — RDD requires manipulation-free assignment; if individuals can game the cutoff (e.g., test-takers retake), McCrary density test should not show a bunching at cutoff.
- **Synthetic control donor pool quality** — controls must not themselves be affected by spillovers from the treated unit.
- **Propensity score overlap** — common-support violation: if some propensity scores are 0 or 1, those units are unmatchable. Trim or use IPW with stabilized weights.
- **SUTVA / network effects** — if treated units affect control units (social features, geographic spillover), all observational methods are biased.
- **CATE interpretation** — large positive CATE in a tiny subgroup may be noise; report uncertainty per segment.
- **EconML cross-fitting** — required for orthogonality; built-in via `n_splits`; running without it biases standard errors.
- **CausalImpact requires stable donor-pool correlation** — if controls' relationship to the treated changes over time, the counterfactual is wrong.
- **Sample size for IV / RDD** — both methods have lower effective power than OLS; expect to need 3-10x the sample for similar precision.

## Sources

- [DoWhy documentation](https://www.pywhy.org/dowhy/)
- [DoWhy tutorial — 4 steps of causal inference](https://www.pywhy.org/dowhy/v0.11/example_notebooks/dowhy_simple_example.html)
- [linearmodels — IV2SLS](https://bashtage.github.io/linearmodels/iv/iv/linearmodels.iv.model.IV2SLS.html)
- [linearmodels — PanelOLS](https://bashtage.github.io/linearmodels/panel/panel/linearmodels.panel.model.PanelOLS.html)
- [CausalImpact Python port](https://github.com/dafiti/causalimpact)
- [Google CausalImpact (R original)](https://google.github.io/CausalImpact/)
- [EconML documentation](https://econml.azurewebsites.net/)
- [rdrobust — local-linear RDD](https://rdpackages.github.io/rdrobust/)
- [E-value sensitivity analysis (VanderWeele & Ding 2017)](https://www.acpjournals.org/doi/10.7326/M16-2607)
- role.md → "Causal inference playbook"
