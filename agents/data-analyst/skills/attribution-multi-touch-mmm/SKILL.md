<!--
Google Meridian: https://developers.google.com/meridian
lightweight_mmm: https://github.com/google/lightweight_mmm
Robyn (R): https://github.com/facebookexperimental/Robyn
Companion: role.md → "Attribution playbook"
-->

# Attribution — rule-based, Markov-chain, MMM (Meridian / lightweight_mmm)

End-to-end attribution: rule-based (last-touch / first-touch / linear / time-decay / position-based) in SQL, Markov-chain attribution for digital touchpoints, and full Bayesian Marketing Mix Modeling via Google Meridian (NumPyro/JAX) or lightweight_mmm. Output: per-channel ROI, optimal spend allocation, response curves with uncertainty.

## When to use

- "Which channels drove revenue this month?" → last-touch SQL as default
- "Multi-touch journey credit allocation" → linear / time-decay / Markov
- "How should we reallocate $5M across channels next quarter?" → MMM
- "What's the diminishing-return curve for paid search?" → MMM saturation curve
- "Offline channels (TV, radio, OOH) need crediting alongside digital" → MMM only

Defer A/B test math to `ab-test-significance-mde-sequential`. Defer Bayesian primitives to `bayesian-pymc-numpyro-ab-testing`. Defer causal-with-DAGs to `causal-inference-dag-iv-rdd`.

## Setup

```bash
# Rule-based: warehouse SQL only
# Markov-chain
pip install pandas networkx

# Bayesian MMM
pip install lightweight_mmm                  # smaller datasets, simpler
pip install meridian                          # SOTA Bayesian MMM (2024+, JAX backend)
# Meridian install: https://github.com/google/meridian — usually:
git clone https://github.com/google/meridian && cd meridian && pip install -e .
```

No external auth; runs locally. Recipient supplies warehouse credentials for source data.

## Method comparison

| Method | When | Pros | Cons |
|---|---|---|---|
| Last-touch SQL | Default reporting | Simple, explainable | Ignores upper-funnel; biases to bottom-funnel channels |
| First-touch | Brand awareness reports | Credits discovery | Ignores closing channels |
| Linear (1/N) | Need any multi-touch | Easy | Equal credit may be wrong |
| Time-decay | More credit to recent touches | Closer to reality | Decay parameter arbitrary |
| Position-based (40/20/40) | Honor first + last | Captures bookends | Middle gets undervalued |
| Markov-chain | Digital-only, many paths | Data-driven removal-effect | Hard with sparse paths |
| Shapley | Theoretically clean | Game-theory rigor | 2^N coalitions = expensive |
| MMM | Mixed digital + offline | Bayesian uncertainty + spend optimization | Months of weekly data needed |

## Common recipes

### Recipe 1 — Last-touch attribution (SQL)

```sql
WITH conversions AS (
    SELECT user_id, conversion_id, conversion_at, conversion_value
    FROM fct_conversions
),
touches AS (
    SELECT user_id, channel, touch_at
    FROM fct_marketing_touches
),
attributed AS (
    SELECT
        c.conversion_id,
        c.conversion_value,
        t.channel,
        ROW_NUMBER() OVER (PARTITION BY c.conversion_id ORDER BY t.touch_at DESC) AS rn
    FROM conversions c
    LEFT JOIN touches t
      ON t.user_id = c.user_id AND t.touch_at <= c.conversion_at
)
SELECT channel, SUM(conversion_value) AS attributed_revenue, COUNT(*) AS conversions
FROM attributed
WHERE rn = 1
GROUP BY 1
ORDER BY attributed_revenue DESC;
```

For first-touch, swap `ORDER BY t.touch_at DESC` → `ASC`.

### Recipe 2 — Linear + time-decay attribution

```sql
-- Linear (1/N per touch)
WITH paths AS (
  SELECT c.conversion_id, c.conversion_value, t.channel, COUNT(*) OVER (PARTITION BY c.conversion_id) AS n_touches
  FROM conversions c
  LEFT JOIN touches t ON t.user_id = c.user_id AND t.touch_at <= c.conversion_at
)
SELECT channel, SUM(conversion_value * 1.0 / n_touches) AS attributed_revenue
FROM paths
GROUP BY 1;

-- Time-decay (exp(-λ * days_to_conv))
WITH decay AS (
  SELECT c.conversion_id, c.conversion_value, t.channel,
         EXP(-0.1 * DATEDIFF('day', t.touch_at, c.conversion_at)) AS weight
  FROM conversions c
  JOIN touches t ON t.user_id = c.user_id AND t.touch_at <= c.conversion_at
),
normalized AS (
  SELECT *, weight / SUM(weight) OVER (PARTITION BY conversion_id) AS norm_weight
  FROM decay
)
SELECT channel, SUM(conversion_value * norm_weight) AS attributed_revenue
FROM normalized GROUP BY 1;
```

### Recipe 3 — Position-based (40/20/40)

```python
import pandas as pd

paths = pd.read_sql("""
    SELECT conversion_id, conversion_value, channel,
           ROW_NUMBER() OVER (PARTITION BY conversion_id ORDER BY touch_at) AS pos,
           COUNT(*)  OVER (PARTITION BY conversion_id) AS n
    FROM ...
""", con)

def weight(pos, n):
    if n == 1: return 1.0
    if n == 2: return 0.5
    if pos == 1: return 0.4
    if pos == n: return 0.4
    return 0.2 / (n - 2)

paths["weight"] = paths.apply(lambda r: weight(r.pos, r.n), axis=1)
paths["attr"] = paths.conversion_value * paths.weight
summary = paths.groupby("channel")["attr"].sum().sort_values(ascending=False)
```

### Recipe 4 — Markov-chain attribution

```python
import pandas as pd
import numpy as np

# Build transition matrix from journey sequences
# journeys: DataFrame with ['user_id', 'channel', 'touch_at', 'converted']
paths = (journeys.sort_values(["user_id", "touch_at"])
                 .groupby("user_id")
                 .agg(seq=("channel", list), converted=("converted", "max"))
                 .reset_index())

# Add Start/Conversion/Null endpoints
def with_endpoints(row):
    return ["Start"] + row.seq + (["Conversion"] if row.converted else ["Null"])
paths["full"] = paths.apply(with_endpoints, axis=1)

# Transition counts
from collections import Counter
trans = Counter()
for seq in paths["full"]:
    for a, b in zip(seq, seq[1:]):
        trans[(a, b)] += 1

# Normalize per source
totals = Counter()
for (a, b), c in trans.items():
    totals[a] += c
P = {(a, b): c / totals[a] for (a, b), c in trans.items()}

# Conversion rate of the full graph
def conv_rate(P, removed=None):
    # Monte Carlo: simulate journeys from Start until Conversion or Null
    states = sorted({a for a, _ in P} | {b for _, b in P})
    rng = np.random.default_rng(42)
    convs = 0
    for _ in range(10000):
        s = "Start"
        while s not in ("Conversion", "Null"):
            choices = [(b, p) for (a, b), p in P.items() if a == s and b != removed]
            if not choices: break
            tot = sum(p for _, p in choices)
            r = rng.random() * tot
            cum = 0
            for b, p in choices:
                cum += p
                if r <= cum: s = b; break
        if s == "Conversion": convs += 1
    return convs / 10000

base_rate = conv_rate(P)
channels = {a for a, _ in P} | {b for _, b in P}
channels -= {"Start", "Conversion", "Null"}

# Removal-effect attribution: drop in conversion rate when channel removed
removal_effect = {c: (base_rate - conv_rate(P, removed=c)) / base_rate for c in channels}
total_re = sum(removal_effect.values())

total_conversions = journeys["converted"].sum()
attribution = {c: total_conversions * re / total_re for c, re in removal_effect.items()}
print(attribution)
```

For production scale, use the R `ChannelAttribution` package (CRAN) or build a Python solver against the linear system.

### Recipe 5 — lightweight_mmm (Bayesian MMM, smaller dataset)

```python
import jax.numpy as jnp
from lightweight_mmm import lightweight_mmm, preprocessing, optimize_media, plot

# Inputs:
# - media_data:     T weeks x C channels (spend or impressions)
# - target:         T weeks (conversions or revenue)
# - extra_features: T weeks x F (controls: promo flags, seasonality dummies, holidays)
# - costs:          C (cost per impression, only if media_data is impressions)

# 1. Scale data (recommended)
media_scaler = preprocessing.CustomScaler(divide_operation=jnp.mean)
target_scaler = preprocessing.CustomScaler(divide_operation=jnp.mean)
media_scaled  = media_scaler.fit_transform(media_data)
target_scaled = target_scaler.fit_transform(target)

# 2. Fit Bayesian model
mmm = lightweight_mmm.LightweightMMM(model_name="hill_adstock")   # or "adstock", "carryover"
mmm.fit(
    media=media_scaled,
    target=target_scaled,
    media_prior=costs * media_data.sum(axis=0),
    extra_features=extra_features_scaled,
    number_warmup=1000,
    number_samples=1000,
    seed=42,
)

# 3. Diagnostics
print(mmm.print_summary())          # R-hat / n_eff / posterior mean per channel
plot.plot_media_channel_posteriors(mmm)
plot.plot_response_curves(mmm)

# 4. Predict
predictions = mmm.predict(media=test_media)

# 5. Optimize spend
solution, kpi_without_optim, kpi_with_optim = optimize_media.find_optimal_budgets(
    n_time_periods=8,
    media_mix_model=mmm,
    budget=jnp.array(8 * 1_000_000),
    prices=costs,
    seed=42,
)
print("Optimal weekly budget per channel:", solution.x)
```

### Recipe 6 — Meridian (current SOTA)

```python
# Meridian uses a unified protobuf-config style + NumPyro/JAX
from meridian import constants
from meridian.data import data_frame_input_data_builder
from meridian.model import model, prior_distribution, spec

# Build InputData
data = data_frame_input_data_builder.DataFrameInputDataBuilder(
    kpi_type=constants.REVENUE,
    media_to_channel=media_to_channel,
).with_kpi(kpi_df).with_population(population_df).with_revenue_per_kpi(revenue_per_kpi_df) \
 .with_media(media_df).build()

# Specify model
spec = spec.ModelSpec(
    prior=prior_distribution.PriorDistribution(),
    media_effects_dist="log_normal",
    hill_before_adstock=False,
    max_lag=8,
)

# Sample posterior
m = model.Meridian(input_data=data, model_spec=spec)
m.sample_prior(500)
m.sample_posterior(n_chains=4, n_adapt=500, n_burnin=500, n_keep=1000)

# Channel ROIs
from meridian.analysis import analyzer
analyzer.Analyzer(m).roi()           # → posterior ROI per channel
analyzer.Analyzer(m).optimal_freq()  # → optimal frequency curves
```

### Recipe 7 — Adstock transformation (when building MMM manually)

```python
import numpy as np

def geometric_adstock(x, decay=0.5, l_max=4):
    """Carryover decay: today's spend influences L future periods."""
    weights = decay ** np.arange(l_max + 1)
    weights /= weights.sum()
    return np.convolve(x, weights, mode="full")[: len(x)]

def hill_saturation(x, K, slope):
    """Diminishing returns: response saturates at K, sharpness = slope."""
    return x ** slope / (x ** slope + K ** slope)

# Pre-process: adstock first, then hill-transform
x_adstocked = geometric_adstock(spend, decay=0.4, l_max=8)
x_response = hill_saturation(x_adstocked, K=50_000, slope=1.5)
```

### Recipe 8 — Response curves + optimal allocation

```python
# After lightweight_mmm fit:
plot.plot_response_curves(mmm, scaler=media_scaler, target_scaler=target_scaler)
# Per-channel: x = spend, y = predicted incremental revenue, with 90% credible band

# Optimal budget allocation under a constraint
from lightweight_mmm.optimize_media import find_optimal_budgets

solution, _, _ = find_optimal_budgets(
    n_time_periods=12,
    media_mix_model=mmm,
    budget=jnp.array(12 * 800_000),     # quarterly budget
    prices=costs,
    bounds_lower_pct=jnp.array([0.3] * n_channels),     # min 30% of current spend
    bounds_upper_pct=jnp.array([2.0] * n_channels),     # max 2x current spend
    seed=42,
)
print(solution.x.reshape(n_time_periods, n_channels))
```

### Recipe 9 — Reporting template

```
ATTRIBUTION REPORT — <campaign / quarter>

METHOD: <last-touch SQL / linear / time-decay / Markov / MMM>
DATA WINDOW: <weeks>, <N conversions>

RESULTS:
| Channel       | Revenue        | Share  | ROI    | 90% CI       |
|---------------|----------------|--------|--------|--------------|
| Paid Search   | $1,200,000     | 35.0%  | 3.2    | [2.7, 3.8]   |
| Email         | $850,000       | 24.8%  | 12.5   | [9.1, 16.2]  |
| Social        | $720,000       | 21.0%  | 1.8    | [1.4, 2.3]   |
| ...

KEY FINDINGS:
- <channel> drove the largest share / highest ROI
- <channel>'s saturation point is around $X/week
- <channel> has highest marginal return at current spend

RECOMMENDATIONS:
1. Shift $X from <low-ROI> to <high-marginal> channel.
2. Reduce <saturated> channel by Y%.
3. Continue tracking; rerun MMM quarterly.

CAVEATS:
- <data quality issues — UTM tagging gaps, etc.>
- <out-of-distribution channels — first month for X>
- <model assumptions — adstock decay, etc.>
```

### Recipe 10 — Validation: incrementality A/B holdout

The gold-standard MMM validation: run a geographic / time-based hold-out experiment. Pick 1-2 markets to pause the channel; measure incremental drop. Compare to MMM prediction.

```sql
-- Holdout test: did paused-market revenue drop as MMM predicted?
WITH per_market AS (
    SELECT market_id, week, sum(revenue) AS revenue, max(channel_active) AS active
    FROM marts.fct_market_weekly
    WHERE week BETWEEN '2026-04-01' AND '2026-06-01'
    GROUP BY 1, 2
)
SELECT
    market_id,
    avg(CASE WHEN week < '2026-05-01' THEN revenue END) AS pre_revenue,
    avg(CASE WHEN week >= '2026-05-01' AND active = false THEN revenue END) AS during_paused,
    avg(CASE WHEN week >= '2026-05-01' AND active = true THEN revenue END) AS during_active
FROM per_market
GROUP BY 1;
```

## Example end-to-end

**Goal:** Re-allocate $4M/quarter across 6 channels using MMM.

1. Pull 104 weeks of spend per channel + conversions + controls (holidays, promotions, seasonality).
2. Fit `lightweight_mmm` with `hill_adstock` model (Recipe 5).
3. Diagnostics: R-hat < 1.05, n_eff > 500 per parameter. Response curves visualized.
4. Compute per-channel ROI with 90% credible intervals.
5. Run `find_optimal_budgets` → reallocates 20% of spend from Social to Paid Search.
6. Validate via geo-holdout: pause Social in 2 test markets; compare to MMM forecast.
7. Deliverable per Recipe 9 template.

## Edge cases / gotchas

- **Last-touch overcredits bottom-funnel** — biases dollar allocation to brand keywords / direct traffic that would have converted anyway.
- **UTM tracking gaps** — "(direct)" / "(none)" bucket inflates first/last-touch results when redirects strip parameters.
- **Markov requires enough paths** — sparse-conversion data produces unstable removal effects; aggregate to channel-group level.
- **MMM needs 2+ years of weekly data** — fewer = high uncertainty + identifiability issues (which channels' lift is which).
- **Adstock decay identifiability** — without sufficient variation in spend timing, the model can't distinguish decay from saturation.
- **Saturation curves outside data range** — extrapolating beyond observed spend levels is unreliable. Stay within sampled budget range.
- **MMM is not causal** — observational; correlation only. Validate via geo / time hold-out experiments.
- **Bayesian convergence** — always check R-hat (target <1.05), n_eff (target >500); rerun with longer chains if fails.
- **Seasonality control** — omit at your peril; you'll attribute holiday spikes to whichever channel happened to be running.
- **Calibration with experiments** — best practice: feed prior posteriors from past A/B tests into MMM as informative priors.
- **Meridian vs lightweight_mmm** — Meridian is SOTA but heavier; lightweight_mmm is faster for <2yr datasets and simpler API.
- **Privacy-regulated channels** — iOS / cookie restrictions limit digital tracking accuracy; MMM is somewhat resilient (uses aggregate spend).

## Sources

- [Google Meridian docs](https://developers.google.com/meridian)
- [Meridian GitHub](https://github.com/google/meridian)
- [lightweight_mmm](https://github.com/google/lightweight_mmm)
- [Meta Robyn (R)](https://github.com/facebookexperimental/Robyn)
- [Markov-chain attribution paper (Anderl et al.)](https://www.semanticscholar.org/paper/Mapping-the-customer-journey%3A-Lessons-learned-from-Anderl-Becker/)
- [Adstock — Broadbent 1979](https://en.wikipedia.org/wiki/Advertising_adstock)
- [Hill saturation function](https://en.wikipedia.org/wiki/Hill_equation_(biochemistry))
- role.md → "Attribution playbook" + "Marketing Mix Modeling"
