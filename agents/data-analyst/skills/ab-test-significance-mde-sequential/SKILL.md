<!--
scipy.stats: https://docs.scipy.org/doc/scipy/reference/stats.html
statsmodels power: https://www.statsmodels.org/stable/stats.html#power-and-sample-size-calculations
pingouin: https://pingouin-stats.org/
Companion: role.md → "A/B test playbook"
-->

# A/B test math — significance, MDE, sample size, sequential testing

End-to-end A/B test analysis: choose the right test, compute sample size + MDE before the experiment, run the test, report effect size + CI alongside the p-value, apply CUPED variance reduction, handle sequential/peeking via mSPRT or always-valid p-values, and write a defensible report.

## When to use

- "Is this A/B test significant?" / "Did we win, lose, or is it a wash?"
- "What sample size do I need to detect a 2% lift?"
- "We peeked early — is the result still valid?"
- "Compare two cohorts on a continuous / binary / count metric"
- "Apply CUPED to reduce variance"

Defer Bayesian A/B (PyMC, Beta-Binomial) to `bayesian-pymc-numpyro-ab-testing`. Defer survival-curve A/B (log-rank) to `cohort-retention-deep-survival`. Defer causal-with-observational-data to `causal-inference-dag-iv-rdd`.

## Setup

```bash
pip install scipy statsmodels pingouin pandas numpy
pip install growthbook                      # if using GrowthBook OSS engine
```

No external auth. For platform-grade results, the recipient supplies Statsig / GrowthBook / Eppo credentials.

## Pre-experiment checklist (role.md)

- [ ] Hypothesis (H0 vs H1) written down
- [ ] **Primary metric** singular (or multiple-comparison correction planned)
- [ ] Guardrail metrics named (revenue, latency, refund rate)
- [ ] **MDE** chosen for business relevance
- [ ] Alpha = 0.05, power = 0.8 default; document any deviation
- [ ] Sample size computed **before** experiment
- [ ] Randomization unit declared (user / session / visit)
- [ ] **SRM** (sample-ratio mismatch) check planned

## Common recipes

### Recipe 1 — Sample size for proportions

```python
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import samplesize_proportions_2indep_onetail

# Detect 2 percentage-point lift from 10% baseline at 80% power, alpha=0.05
n_per_arm = samplesize_proportions_2indep_onetail(
    diff=0.02,                  # absolute difference detect
    prop2=0.10,                 # baseline
    power=0.80,
    alpha=0.05,
)
print(f"Need {n_per_arm:.0f} per arm; {2*n_per_arm:.0f} total")
# → 3835 per arm, 7670 total

# Using effect size (Cohen's h)
from statsmodels.stats.proportion import proportion_effectsize
h = proportion_effectsize(0.12, 0.10)
n = NormalIndPower().solve_power(effect_size=h, alpha=0.05, power=0.8, alternative="two-sided")
```

### Recipe 2 — Sample size for means

```python
from statsmodels.stats.power import TTestIndPower

# Detect Cohen's d = 0.1 effect ("small")
analysis = TTestIndPower()
n = analysis.solve_power(effect_size=0.1, alpha=0.05, power=0.8, alternative="two-sided")
print(f"{n:.0f} per arm")
# → ~1571 per arm

# MDE-driven: given a known std dev + sample size, what's the MDE?
# d = (μ_b - μ_a) / σ → MDE = d * σ
mde_d = analysis.solve_power(nobs1=5000, alpha=0.05, power=0.8)
print(f"With n=5000/arm, MDE Cohen's d = {mde_d:.3f}")
mde_absolute = mde_d * historical_std_dev
```

### Recipe 3 — Two-proportion z-test

```python
from statsmodels.stats.proportion import proportions_ztest

# A: 132/1500 = 8.8%; B: 165/1500 = 11.0%
count = [132, 165]
nobs  = [1500, 1500]
zstat, pval = proportions_ztest(count, nobs, alternative="two-sided")
print(f"z = {zstat:.3f}, p = {pval:.4f}")

# Confidence interval on the difference
from statsmodels.stats.proportion import confint_proportions_2indep
ci_low, ci_high = confint_proportions_2indep(
    count1=count[1], nobs1=nobs[1], count2=count[0], nobs2=nobs[0],
    method="wald", alpha=0.05
)
print(f"95% CI on lift: [{ci_low:.3%}, {ci_high:.3%}]")
```

### Recipe 4 — Welch's t-test (continuous, unequal variance)

```python
import scipy.stats as ss
import numpy as np

a = np.random.normal(loc=100, scale=15, size=2000)
b = np.random.normal(loc=102, scale=18, size=2050)

# Welch's t-test (recommended default — don't assume equal var)
t_stat, p_val = ss.ttest_ind(a, b, equal_var=False, alternative="two-sided")

# Effect size + CI via pingouin (cleaner)
import pingouin as pg
result = pg.ttest(a, b, correction="auto")
print(result)
# Returns: T, dof, p-val, CI95%, cohen-d, BF10 (Bayes factor), power
```

### Recipe 5 — Non-parametric (skewed / non-normal)

```python
# Mann-Whitney U for skewed continuous (e.g., revenue per user)
u_stat, p_val = ss.mannwhitneyu(a, b, alternative="two-sided")

# Effect size (rank-biserial correlation) via pingouin
res = pg.mwu(a, b, alternative="two-sided")
print(res)

# Bootstrap CI for the mean difference (no distributional assumption)
def bootstrap_diff_ci(a, b, n_boot=10000, alpha=0.05):
    rng = np.random.default_rng(42)
    boots = np.array([
        rng.choice(b, len(b)).mean() - rng.choice(a, len(a)).mean()
        for _ in range(n_boot)
    ])
    return np.percentile(boots, [100*alpha/2, 100*(1-alpha/2)])
ci_low, ci_high = bootstrap_diff_ci(a, b)
```

### Recipe 6 — CUPED variance reduction

```python
import numpy as np

# Y_pre: per-user pre-experiment value of the metric (correlated with Y)
# Y    : per-user value during the experiment

theta = np.cov(Y_pre, Y, ddof=1)[0, 1] / np.var(Y_pre, ddof=1)
Y_cuped = Y - theta * (Y_pre - Y_pre.mean())

# Now run the t-test on Y_cuped instead of Y
t, p = ss.ttest_ind(Y_cuped[treatment_idx], Y_cuped[control_idx], equal_var=False)

# Variance reduction
var_ratio = 1 - np.corrcoef(Y_pre, Y)[0, 1] ** 2
print(f"Variance reduction: {1 - var_ratio:.1%} → effective sample-size boost")
# Common: 30-50% sample-size reduction when correlation is 0.5-0.7
```

### Recipe 7 — Sample-Ratio Mismatch (SRM)

```python
# Did the randomizer produce the expected 50/50 split?
n_a, n_b = 4980, 5020         # observed
expected_ratio = [0.5, 0.5]
chi2, p_val = ss.chisquare([n_a, n_b], f_exp=[(n_a+n_b)*r for r in expected_ratio])
print(f"SRM chi2 p = {p_val:.4f}")
if p_val < 0.001:
    print("SRM detected — DO NOT trust the experiment results until you find the leak.")
```

### Recipe 8 — Always-valid p-values (sequential / peeking)

```python
# mSPRT-style: confidence sequences via the GAVI framework (Howard et al.)
# Quick approximation: use the `confseq` library or compute manually.
# For practical use, GrowthBook / Statsig do this server-side.

# GrowthBook OSS engine:
from growthbook import GrowthBook, Experiment

gb = GrowthBook()
exp = Experiment(
    key="checkout_flow_v2",
    variations=[control_data, treatment_data],
    weights=[0.5, 0.5],
)
# Use GrowthBook stats engine via REST:
import requests
r = requests.post(
    f"{GROWTHBOOK_API}/api/v1/experiment-snapshots",
    headers={"Authorization": f"Bearer {GROWTHBOOK_KEY}"},
    json={"experimentId": "exp_abc", "stats_engine": "frequentist", "sequential": True}
)
```

Manual approach: use Bayesian framework instead — see `bayesian-pymc-numpyro-ab-testing`.

### Recipe 9 — Multiple comparisons (multi-metric or multi-variant)

```python
from statsmodels.stats.multitest import multipletests

# Suppose 5 metrics tested, raw p-values:
pvals = [0.04, 0.02, 0.30, 0.01, 0.10]

# Bonferroni (conservative)
reject, pvals_corr, _, _ = multipletests(pvals, alpha=0.05, method="bonferroni")
print("Bonferroni:", reject, pvals_corr)

# Benjamini-Hochberg (FDR — less conservative)
reject, pvals_corr, _, _ = multipletests(pvals, alpha=0.05, method="fdr_bh")
print("BH:", reject, pvals_corr)
```

### Recipe 10 — Full A/B test report function

```python
from dataclasses import dataclass
import scipy.stats as ss
import numpy as np

@dataclass
class ABResult:
    test: str
    n_a: int
    n_b: int
    mean_a: float
    mean_b: float
    effect_size: float
    p_value: float
    ci_low: float
    ci_high: float
    cohen_d: float
    srm_p: float
    recommendation: str

def ab_report(a, b, metric_name="metric", alpha=0.05) -> ABResult:
    # SRM check
    _, srm_p = ss.chisquare([len(a), len(b)], f_exp=[(len(a)+len(b))/2]*2)

    # Test
    t, p = ss.ttest_ind(a, b, equal_var=False)
    diff = np.mean(b) - np.mean(a)

    # 95% CI on diff (Welch)
    se = np.sqrt(np.var(a, ddof=1)/len(a) + np.var(b, ddof=1)/len(b))
    df = (np.var(a, ddof=1)/len(a) + np.var(b, ddof=1)/len(b))**2 / (
        (np.var(a, ddof=1)/len(a))**2/(len(a)-1) +
        (np.var(b, ddof=1)/len(b))**2/(len(b)-1)
    )
    crit = ss.t.ppf(1 - alpha/2, df)
    ci_low, ci_high = diff - crit*se, diff + crit*se

    # Cohen's d
    pooled = np.sqrt(((len(a)-1)*np.var(a, ddof=1) + (len(b)-1)*np.var(b, ddof=1)) / (len(a)+len(b)-2))
    cohen_d = diff / pooled

    rec = (
        "KILL"  if (ci_high < 0) else
        "SHIP"  if (ci_low > 0 and p < alpha) else
        "EXTEND" if (p > alpha and abs(cohen_d) < 0.05) else
        "HOLD"
    )
    if srm_p < 0.001:
        rec = "SRM DETECTED — INVESTIGATE FIRST"

    return ABResult(
        test=f"Welch t-test on {metric_name}",
        n_a=len(a), n_b=len(b),
        mean_a=np.mean(a), mean_b=np.mean(b),
        effect_size=diff, p_value=p,
        ci_low=ci_low, ci_high=ci_high,
        cohen_d=cohen_d, srm_p=srm_p,
        recommendation=rec,
    )
```

## Example end-to-end

**Goal:** Did checkout-flow v2 lift conversion from 8.8% to a meaningful level?

1. **Plan:** baseline 8.8%, want to detect 1pp lift → sample-size: `samplesize_proportions_2indep_onetail(diff=0.01, prop2=0.088, power=0.8, alpha=0.05)` → ~13,800/arm.
2. **Run:** ramp to 50/50 over 14 days; collect 14,500 + 14,400 users per arm.
3. **SRM:** `chisquare([14500, 14400], [14450, 14450])` → p = 0.55 → OK.
4. **Test:** `proportions_ztest([1276, 1442], [14500, 14400])` → z=4.2, p<0.0001.
5. **CI:** `confint_proportions_2indep` → 95% CI on lift: [0.5%, 1.8%].
6. **Effect size:** Cohen's h ≈ 0.08 (small but real).
7. **Guardrails:** revenue/user CI excludes 0 lift downside; latency p99 not impacted.
8. **Report:** see template in role.md → "A/B test playbook → Report template".
9. **Recommendation:** SHIP — confident lift of 1.2pp (95% CI [0.5, 1.8]).

## Edge cases / gotchas

- **Sample size assumes a single test** — multi-metric or multi-variant tests need adjustment (Bonferroni/BH).
- **Peeking penalty** — fixed-horizon p-values are invalid if you stop early on positive results. Use mSPRT/CUPED+sequential, or Bayesian, or wait the full horizon.
- **SRM is a red flag, not a finding** — investigate (often: tracking bug, bot traffic, randomizer skew); do NOT report results until resolved.
- **Cohen's d magnitude conventions** — 0.2 small, 0.5 medium, 0.8 large; depends on field. Always pair with practical-significance threshold.
- **Welch's vs Student's t-test** — default to Welch's (`equal_var=False`); equal-variance assumption is rarely justified.
- **Survivorship + selection bias** — if treatment changes who shows up in the data (e.g., a bug makes B users not bucket), inferences are invalid. Check randomization audit log.
- **CUPED requires pre-experiment data** — covariate must predate randomization or you'll bias the estimate.
- **Variance ratio reporting** — always report `var(A)/var(B)`; very different variances often signal a metric definition problem (e.g., extreme outliers in one arm).
- **Bonferroni overcorrects with correlated metrics** — BH (FDR) is the modern default for multiple comparisons in experimentation.
- **Network effects / SUTVA violation** — if treatment users influence control users (e.g., social features), independence assumption fails. Cluster randomization may be required.
- **One-sided vs two-sided** — pre-register one-sided only if business cost of opposite outcome is zero. Default two-sided.

## Sources

- [scipy.stats reference](https://docs.scipy.org/doc/scipy/reference/stats.html)
- [statsmodels power + sample size](https://www.statsmodels.org/stable/stats.html#power-and-sample-size-calculations)
- [pingouin documentation](https://pingouin-stats.org/)
- [Microsoft Trustworthy A/B Testing (Kohavi et al.)](https://exp-platform.com/Documents/2013-02-CHI2013-LongerOnlineExperiments.pdf)
- [GrowthBook docs — sequential testing](https://docs.growthbook.io/statistics/sequential)
- [Statsig docs — sequential testing](https://docs.statsig.com/experiments-plus/sequential-testing)
- [CUPED (Deng et al. 2013)](https://www.researchgate.net/publication/237838291)
- [Always-Valid Inference (Howard et al. 2021)](https://arxiv.org/abs/1810.08240)
- role.md → "A/B test playbook"
