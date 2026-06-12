<!--
PyMC: https://www.pymc.io/
NumPyro: https://num.pyro.ai/
Companion: role.md → "Bayesian A/B playbook"
-->

# Bayesian A/B testing — PyMC + NumPyro + Beta-Binomial conjugate

End-to-end Bayesian A/B analysis: closed-form Beta-Binomial conjugate for proportions, PyMC for continuous + hierarchical priors, NumPyro/JAX for fast posterior sampling. Avoids the peeking penalty of frequentist tests by reporting full posterior P(B > A), HDI, expected loss/upside.

## When to use

- "Continuously monitor an A/B test without peeking penalty"
- "Report decision-grade outputs (P(B>A), expected loss) for executives"
- "Hierarchical model — A/B across multiple geographies / segments with partial pooling"
- "Small sample size — Bayesian shrinkage stabilizes estimates"
- "Prior information available — encode it into the model"

Defer frequentist A/B math to `ab-test-significance-mde-sequential`. Defer survival-analysis Bayesian models to `cohort-retention-deep-survival`. Defer MMM to `attribution-multi-touch-mmm`.

## Setup

```bash
# PyMC (Python-native, autodiff via PyTensor)
pip install pymc arviz                  # arviz for posterior diagnostics + plots

# NumPyro (faster on GPU, JAX backend)
pip install numpyro jax jaxlib

# Conjugate analysis only
pip install scipy numpy matplotlib
```

No external auth.

## Three flavors

| Flavor | Use when | Speed |
|---|---|---|
| **Beta-Binomial conjugate** | Single proportion comparison (conversion rate) | Instant |
| **PyMC MCMC** | Continuous metrics, hierarchical, full Bayesian regression | Slow (seconds-minutes) |
| **NumPyro NUTS** | Same model, JAX-accelerated, GPU-capable | 5-20× faster than PyMC |

## Common recipes

### Recipe 1 — Beta-Binomial conjugate (proportions, closed-form)

```python
import numpy as np
from scipy.stats import beta

# Observed
conv_a, n_a = 132, 1500       # 8.8% control
conv_b, n_b = 165, 1500       # 11.0% treatment

# Prior: Beta(1, 1) = uniform; or use historical with Beta(α, β)
alpha_prior, beta_prior = 1, 1
post_a = beta(alpha_prior + conv_a, beta_prior + (n_a - conv_a))
post_b = beta(alpha_prior + conv_b, beta_prior + (n_b - conv_b))

# Sample posteriors
samples_a = post_a.rvs(100_000)
samples_b = post_b.rvs(100_000)

# Decision outputs
p_b_better = (samples_b > samples_a).mean()
lift_samples = (samples_b - samples_a) / samples_a
expected_lift = lift_samples.mean()
hdi_lift = np.percentile(lift_samples, [2.5, 97.5])

# Expected loss if you ship B but B is actually worse than A
expected_loss = np.maximum(samples_a - samples_b, 0).mean()
# Expected upside
expected_upside = np.maximum(samples_b - samples_a, 0).mean()

print(f"P(B > A) = {p_b_better:.3f}")
print(f"Expected lift: {expected_lift:.3%}")
print(f"95% HDI on lift: [{hdi_lift[0]:.3%}, {hdi_lift[1]:.3%}]")
print(f"Expected loss if shipping B: {expected_loss:.4f}")
print(f"Expected upside if shipping B: {expected_upside:.4f}")
```

### Recipe 2 — Decision rules

```python
def ship_decision(p_b_better, expected_loss, threshold_loss=0.001, threshold_prob=0.95):
    if p_b_better > threshold_prob and expected_loss < threshold_loss:
        return "SHIP B"
    elif p_b_better < 1 - threshold_prob:
        return "KILL B (A is clearly better)"
    else:
        return "CONTINUE (uncertain)"

decision = ship_decision(p_b_better, expected_loss)
print(decision)
```

### Recipe 3 — PyMC continuous A/B (Welch-equivalent)

```python
import pymc as pm
import arviz as az

# y_a, y_b: per-user metric values (e.g., revenue per user)
with pm.Model() as model:
    # Priors — weakly informative
    mu_a = pm.Normal("mu_a", mu=y_a.mean(), sigma=y_a.std() * 2)
    mu_b = pm.Normal("mu_b", mu=y_b.mean(), sigma=y_b.std() * 2)
    sigma_a = pm.HalfNormal("sigma_a", sigma=y_a.std() * 2)
    sigma_b = pm.HalfNormal("sigma_b", sigma=y_b.std() * 2)

    # Likelihoods
    pm.Normal("y_a", mu=mu_a, sigma=sigma_a, observed=y_a)
    pm.Normal("y_b", mu=mu_b, sigma=sigma_b, observed=y_b)

    # Derived
    diff = pm.Deterministic("diff", mu_b - mu_a)
    lift = pm.Deterministic("lift", (mu_b - mu_a) / mu_a)

    trace = pm.sample(2000, tune=1000, target_accept=0.9, chains=4, random_seed=42)

# Diagnostics
az.summary(trace, var_names=["mu_a", "mu_b", "diff", "lift"])
# R-hat should be ~1.00 for all params; ESS > 400

# Decision metrics
diff_samples = trace.posterior["diff"].values.flatten()
print(f"P(B > A) = {(diff_samples > 0).mean():.3f}")
print(f"95% HDI on diff: {az.hdi(diff_samples, hdi_prob=0.95)}")

az.plot_posterior(trace, var_names=["diff"], hdi_prob=0.95, ref_val=0)
```

### Recipe 4 — Robust model (t-distribution likelihood for outliers)

```python
import pymc as pm

# Revenue often has long tails — use Student-t likelihood
with pm.Model() as model:
    mu_a = pm.Normal("mu_a", y_a.mean(), y_a.std() * 2)
    mu_b = pm.Normal("mu_b", y_b.mean(), y_b.std() * 2)
    sigma = pm.HalfNormal("sigma", y_a.std() * 2)
    nu = pm.Exponential("nu", 1/30)         # degrees of freedom (small ν = heavier tails)

    pm.StudentT("y_a", nu=nu, mu=mu_a, sigma=sigma, observed=y_a)
    pm.StudentT("y_b", nu=nu, mu=mu_b, sigma=sigma, observed=y_b)
    diff = pm.Deterministic("diff", mu_b - mu_a)

    trace = pm.sample(2000, tune=1000, target_accept=0.95, chains=4)
```

### Recipe 5 — Hierarchical model across segments

```python
import pymc as pm

# Per-segment conversion rates with partial pooling
# segment_idx: integer indexing each segment
n_segments = 5

with pm.Model(coords={"segment": range(n_segments)}) as model:
    # Hyper-priors — pool toward global mean
    mu_alpha = pm.Normal("mu_alpha", 0, 1)         # global treatment effect
    sigma_alpha = pm.HalfNormal("sigma_alpha", 1)

    # Per-segment effects (partial pooling)
    alpha_seg = pm.Normal("alpha_seg", mu_alpha, sigma_alpha, dims="segment")
    beta_baseline = pm.Normal("beta_baseline", -2, 1, dims="segment")

    # Logistic regression — link function for binary outcomes
    logit_p = beta_baseline[segment_idx] + alpha_seg[segment_idx] * treatment

    pm.Bernoulli("y", logit_p=logit_p, observed=conversions)
    trace = pm.sample(2000, tune=1000, target_accept=0.9)

# Per-segment treatment effect
az.summary(trace, var_names=["alpha_seg"])
az.plot_forest(trace, var_names=["alpha_seg"], combined=True)
```

### Recipe 6 — NumPyro for speed (JAX backend)

```python
import jax
import jax.numpy as jnp
import numpyro
import numpyro.distributions as dist
from numpyro.infer import MCMC, NUTS

def model(y_a, y_b):
    mu_a = numpyro.sample("mu_a", dist.Normal(y_a.mean(), y_a.std() * 2))
    mu_b = numpyro.sample("mu_b", dist.Normal(y_b.mean(), y_b.std() * 2))
    sigma_a = numpyro.sample("sigma_a", dist.HalfNormal(y_a.std() * 2))
    sigma_b = numpyro.sample("sigma_b", dist.HalfNormal(y_b.std() * 2))
    numpyro.sample("obs_a", dist.Normal(mu_a, sigma_a), obs=y_a)
    numpyro.sample("obs_b", dist.Normal(mu_b, sigma_b), obs=y_b)
    numpyro.deterministic("diff", mu_b - mu_a)

mcmc = MCMC(NUTS(model), num_warmup=1000, num_samples=2000, num_chains=4)
mcmc.run(jax.random.PRNGKey(42), y_a=jnp.array(y_a), y_b=jnp.array(y_b))
mcmc.print_summary()
samples = mcmc.get_samples()
print(f"P(B > A) = {(samples['diff'] > 0).mean():.3f}")
```

### Recipe 7 — Diagnostics checklist

```python
import arviz as az

# Sampler diagnostics
print(az.summary(trace, round_to=3))
# Required: r_hat ≤ 1.01 for all params; ess_bulk ≥ 400 for primary params

# Trace plot — visual sampler health
az.plot_trace(trace, var_names=["mu_a", "mu_b", "diff"])
# Look for: 4 chains overlapping; no drift; no large autocorrelation

# Posterior predictive check
with model:
    ppc = pm.sample_posterior_predictive(trace)
az.plot_ppc(ppc)
# Generated data should resemble observed; if not, model mis-specified
```

### Recipe 8 — Sequential testing (Bayesian = no peeking penalty)

```python
# Bayesian inference is valid at every sample size; you can monitor continuously
# Just rerun the posterior with current data and apply the decision rule.

import time

def bayesian_monitor(get_current_data, decision_rule, max_days=30):
    for day in range(1, max_days + 1):
        y_a, y_b = get_current_data()
        result = run_bayesian_ab(y_a, y_b)        # Recipe 1 or 3

        decision = decision_rule(result)
        print(f"Day {day}: P(B>A)={result['p_b_better']:.3f}, decision={decision}")

        if decision in ("SHIP B", "KILL B"):
            return decision
        time.sleep(86400)        # 1 day
    return "INCONCLUSIVE"
```

This is **valid** Bayesian inference — but DO encode opportunity cost (waiting longer = more learning) in your decision rule.

### Recipe 9 — Informative priors from historical data

```python
import pymc as pm

# Historical baseline conversion rate: 8.5% ± 1%
# Encode as Beta prior with same mean/variance
def beta_from_mean_var(mean, var):
    common = mean * (1 - mean) / var - 1
    return mean * common, (1 - mean) * common

alpha_prior, beta_prior = beta_from_mean_var(mean=0.085, var=0.01**2)

with pm.Model() as model:
    p_a = pm.Beta("p_a", alpha=alpha_prior, beta=beta_prior)     # informed prior
    p_b = pm.Beta("p_b", alpha=alpha_prior, beta=beta_prior)
    pm.Binomial("obs_a", n=n_a, p=p_a, observed=conv_a)
    pm.Binomial("obs_b", n=n_b, p=p_b, observed=conv_b)
    pm.Deterministic("lift", p_b - p_a)
    trace = pm.sample(2000, tune=1000)
```

### Recipe 10 — Report template

```python
def bayesian_ab_report(trace_or_samples, metric_name="conversion rate"):
    p_b_better = (samples["diff"] > 0).mean()
    hdi = np.percentile(samples["diff"], [2.5, 97.5])
    expected_lift = samples["diff"].mean() / samples["mu_a"].mean()
    expected_loss = np.maximum(-samples["diff"], 0).mean()

    return f"""
BAYESIAN A/B REPORT — {metric_name}
=====================================

Posterior:
- P(B > A):              {p_b_better:.1%}
- Mean lift:             {expected_lift:+.3%}
- 95% HDI on diff:       [{hdi[0]:.4f}, {hdi[1]:.4f}]

Risk:
- Expected loss if ship B: {expected_loss:.4f}
- (= avg shortfall when B is actually worse)

Sampler diagnostics:
- R-hat:                 {trace.posterior['mu_a'].chain.size and 'OK' or 'CHECK'}
- ESS bulk:              {arviz.ess(trace).to_array().min().item():.0f}

Recommendation: SHIP / KILL / CONTINUE
"""
```

## Example end-to-end

**Goal:** Bayesian analysis of a checkout-flow A/B test with continuous monitoring.

1. Day 1: Beta(1,1) prior; sample 200 + 210 users; P(B>A)=0.62 → CONTINUE.
2. Day 7: P(B>A)=0.78, HDI [-0.5%, 4.2%] → CONTINUE.
3. Day 14: P(B>A)=0.94, HDI [0.2%, 3.8%], expected loss = 0.0008 → still under threshold → CONTINUE.
4. Day 21: P(B>A)=0.97, HDI [0.4%, 3.6%], expected loss = 0.0003 → SHIP.
5. Compose report per Recipe 10.
6. Decision documented; learnings fed into prior for next checkout experiment.

## Edge cases / gotchas

- **Choice of prior matters** — uniform Beta(1,1) is fine for proportions with reasonable sample size. With informed priors, document the source.
- **R-hat > 1.05** → posterior hasn't converged. Increase `tune`, `target_accept`, or reparameterize the model.
- **Low ESS** — `ess_bulk` < 400 means few effective samples; estimates noisy. Run longer or simplify model.
- **Posterior predictive misfit** — if PPC doesn't reproduce observed data, model is wrong; try heavier-tailed likelihood (Student-t) or different family.
- **Bayesian doesn't fix selection bias** — same as frequentist. SRM, randomization audit still required.
- **Decision threshold = business call** — `P(B>A) > 0.95` is convention, not a law. For high-cost ship decisions, raise to 0.99.
- **Expected loss vs HDI** — HDI is what statisticians want to report; expected loss is what execs need (downside $ at risk).
- **Hierarchical pooling pitfalls** — too-strong pooling shrinks segment effects; too-weak doesn't borrow strength. Set hyper-prior scales via prior predictive check.
- **NumPyro requires JAX-friendly code** — vectorize via `vmap` for speed; loops with Python control flow are slow.
- **PyMC versions** — PyMC 5+ uses PyTensor; old `pymc3` syntax differs. Pin to `pymc>=5.0`.
- **JAX precision** — defaults to float32; for tight HDI calcs use `jax.config.update("jax_enable_x64", True)`.
- **Sequential monitoring isn't free** — even though peeking doesn't invalidate inference, premature stopping increases regret if effects are small. Wait long enough for the posterior to be meaningful.

## Sources

- [PyMC documentation](https://www.pymc.io/projects/docs/en/stable/)
- [PyMC A/B example](https://www.pymc.io/projects/examples/en/latest/case_studies/probabilistic_matrix_factorization.html)
- [NumPyro documentation](https://num.pyro.ai/)
- [ArviZ — Bayesian diagnostics](https://python.arviz.org/en/stable/)
- [Beta-Binomial conjugate (Wikipedia)](https://en.wikipedia.org/wiki/Conjugate_prior)
- [Chris Stucchio — Bayesian A/B testing reports](https://www.chrisstucchio.com/blog/2014/bayesian_asymptotics.html)
- [VWO whitepaper — Bayesian A/B](https://vwo.com/downloads/VWO_SmartStats_technical_whitepaper.pdf)
- role.md → "Bayesian A/B playbook"
