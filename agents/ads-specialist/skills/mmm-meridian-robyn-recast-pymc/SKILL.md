<!--
Source: https://developers.google.com/meridian
Source: https://facebookexperimental.github.io/Robyn/
Source: https://www.pymc-marketing.io/
Marketing Mix Modeling: Google Meridian (May 2026 SOTA with GeoX) + Meta Robyn + PyMC-Marketing.
-->
# Marketing Mix Modeling — Meridian + Robyn + PyMC — SKILL

MMM is the post-cookie / post-pixel attribution model. **Google Meridian** (May 2026 SOTA, with GeoX geo-incrementality) + **Meta Robyn** (R-based, mature) + **PyMC-Marketing** (Python-native Bayesian). This skill ships the data prep, the model run, the response curves, and the budget allocation — without pretending MMM is right for $5K/month accounts.

## When to use this skill

- **Monthly paid spend > $50K** — below, MMM is noise.
- **Cross-channel attribution debate** — MTA (Triple Whale / Northbeam) disputed; MMM resolves.
- **Annual budget planning** — MMM response curves drive allocation.
- **Channel incrementality question** — "does brand search incrementally lift?"
- **Post-cookie attribution** — MMM doesn't need per-user tracking.

**Do NOT use this skill when:**
- Spend <$50K/month — MTA + UTM + last-click warehouse view is enough.
- <12 months of weekly data — MMM needs history to fit response curves.
- Single-channel account — MMM is for mix.

## Setup

### Tool comparison (2026)

| Tool | Lang | Pros | Cons | Cost |
|---|---|---|---|---|
| **Google Meridian** | Python | SOTA Bayesian + GeoX geo-incrementality + reach/frequency curves | New (May 2026); steeper learning curve | Free OSS |
| **Meta Robyn** | R | Mature, hyperparameter tuning, Prophet seasonality, budget allocator | R-based, slower iteration | Free OSS |
| **PyMC-Marketing** | Python | Bayesian, CLV integration, transparent priors | Slower than Meridian | Free OSS |
| **Recast.ai** | managed | No-DevOps, faster to results | Paid SaaS ($50K+/year typical) | Paid |
| **lightweight_mmm** | Python | Older Google lib, simpler API | Slower than Meridian, less feature | Free OSS |

### Install (Meridian + PyMC)

```bash
uvx pip install google-meridian
uvx pip install pymc-marketing
# Or via uv:
uv pip install google-meridian pymc-marketing
```

### Install (Robyn)

```bash
# Requires R
R -e "install.packages('Robyn', repos='https://cran.r-project.org')"
R -e "install.packages('reticulate')"   # for Prophet via Python
```

### Data input schema

```
date          DATE       (weekly recommended)
geo           TEXT       (DMA/state/country — for Meridian GeoX)
revenue       NUMERIC    (KPI — usually revenue or conversions)
spend_meta    NUMERIC    (channel spend; one column per channel)
spend_google  NUMERIC
spend_tiktok  NUMERIC
spend_linkedin NUMERIC
spend_reddit  NUMERIC
impressions_meta NUMERIC (for reach/frequency curves on Meridian)
...
seasonality   NUMERIC    (week-of-year sinusoidal or dummy)
promo_flag    INTEGER    (0/1)
holiday_flag  INTEGER    (per-region calendar)
gtrends_index NUMERIC    (Google Trends category index)
competitor_sov NUMERIC   (Pathmatics / SimilarWeb if available)
```

## Common recipes

### Recipe 1: Data prep — pull from postgresql-mcp warehouse

```sql
WITH weekly_spend AS (
  SELECT 
    DATE_TRUNC('week', date) AS week,
    platform,
    SUM(spend) AS spend,
    SUM(impressions) AS impressions
  FROM ads_warehouse.platform_daily_spend
  WHERE date BETWEEN '2024-06-01' AND '2026-06-01'
  GROUP BY 1, 2
),
weekly_revenue AS (
  SELECT DATE_TRUNC('week', created_at::date) AS week,
         SUM(total_price) AS revenue
  FROM shopify.orders
  WHERE created_at BETWEEN '2024-06-01' AND '2026-06-01'
    AND financial_status = 'paid'
  GROUP BY 1
)
SELECT 
  r.week AS date,
  'US' AS geo,
  r.revenue,
  MAX(CASE WHEN s.platform='meta' THEN s.spend END) AS spend_meta,
  MAX(CASE WHEN s.platform='google' THEN s.spend END) AS spend_google,
  MAX(CASE WHEN s.platform='tiktok' THEN s.spend END) AS spend_tiktok,
  MAX(CASE WHEN s.platform='linkedin' THEN s.spend END) AS spend_linkedin,
  MAX(CASE WHEN s.platform='reddit' THEN s.spend END) AS spend_reddit,
  EXTRACT(WEEK FROM r.week) AS week_of_year
FROM weekly_revenue r
LEFT JOIN weekly_spend s ON s.week = r.week
GROUP BY 1, 2, 3
ORDER BY date;
```

Export to `mmm_input.csv`.

### Recipe 2: Meridian quickstart (Python)

```python
import pandas as pd
from meridian.model import Meridian
from meridian.data import load_dataframe

df = pd.read_csv("mmm_input.csv")

# Configure channels + control variables
config = {
  "geo_col": "geo",
  "time_col": "date",
  "kpi_col": "revenue",
  "spend_cols": ["spend_meta","spend_google","spend_tiktok","spend_linkedin","spend_reddit"],
  "media_cols": ["spend_meta","spend_google","spend_tiktok","spend_linkedin","spend_reddit"],
  "control_cols": ["week_of_year","promo_flag","holiday_flag","gtrends_index"],
  "reach_cols": ["impressions_meta","impressions_google"],   # for R&F curves
}

# Fit
m = Meridian.from_dataframe(df, **config)
m.sample(n_chains=4, n_draws=2000, n_warmup=1000)

# Posterior summary
print(m.summary())

# Response curves
m.plot_response_curves(save_dir="mmm_outputs/")

# Budget allocation
alloc = m.optimize_budget(total_budget=1_000_000, channel_caps={"spend_meta": 600_000})
print(alloc)

# Save report
m.save_report("mmm_report.html")
```

### Recipe 3: Meridian GeoX — geo-incrementality

```python
# GeoX requires multi-geo data. Configure holdout markets for incrementality.
geox_config = {
  "treatment_geos": ["US-NY","US-CA","US-IL"],
  "control_geos": ["US-TX","US-FL","US-WA","US-MA"],
  "treatment_start": "2026-04-01",
  "treatment_end": "2026-05-15",
  "test_channel": "spend_meta"
}
result = m.geox(**geox_config)
print(f"Incremental lift: {result['lift_pct']*100:.1f}%, CI: {result['ci']}")
```

### Recipe 4: Robyn quickstart (R)

```R
library(Robyn)

# Input
input_data <- robyn_inputs(
  dt_input = read.csv("mmm_input.csv"),
  dt_holidays = dt_prophet_holidays,
  date_var = "date",
  dep_var = "revenue",
  dep_var_type = "revenue",
  prophet_vars = c("trend", "season", "holiday"),
  prophet_country = "US",
  context_vars = c("promo_flag", "gtrends_index"),
  paid_media_spends = c("spend_meta", "spend_google", "spend_tiktok"),
  paid_media_vars = c("spend_meta", "spend_google", "spend_tiktok"),
  organic_vars = NULL,
  window_start = "2024-06-01",
  window_end = "2026-06-01",
  adstock = "geometric"
)

# Hyperparameter limits
hyperparams <- list(
  spend_meta_alphas = c(0.5, 3),
  spend_meta_gammas = c(0.3, 1),
  spend_meta_thetas = c(0, 0.3),
  # ... per channel
)
input_with_hp <- robyn_inputs(InputCollect = input_data, hyperparameters = hyperparams)

# Train
output <- robyn_run(
  InputCollect = input_with_hp,
  iterations = 2000,
  trials = 5,
  cores = 6
)

# Pick model
model_id <- output$allSolutions[1]
robyn_save(InputCollect = input_with_hp, OutputCollect = output, select_model = model_id, dir = "./robyn_out/")

# Budget allocator
allocator <- robyn_allocator(
  InputCollect = input_with_hp,
  OutputCollect = output,
  select_model = model_id,
  scenario = "max_response",
  total_budget = 1000000
)
```

### Recipe 5: PyMC-Marketing — Bayesian with CLV

```python
import pandas as pd
import pymc_marketing as pmm
from pymc_marketing.mmm import DelayedSaturatedMMM

df = pd.read_csv("mmm_input.csv")

model = DelayedSaturatedMMM(
  date_column="date",
  channel_columns=["spend_meta","spend_google","spend_tiktok"],
  adstock_max_lag=8,
  control_columns=["week_of_year","promo_flag","gtrends_index"],
  yearly_seasonality=2
)

model.fit(X=df.drop("revenue", axis=1), y=df["revenue"], chains=4, draws=2000, tune=1000)

# Posterior plots
model.plot_components_contributions()
model.plot_channel_contribution_share_hdi()
model.plot_response_curves()

# Budget optimization
result = model.optimize_channel_budget_for_maximum_contribution(
  total_budget=1_000_000,
  channels=["spend_meta","spend_google","spend_tiktok"],
  budget_bounds={"spend_meta": [200_000, 700_000]}
)
print(result)
```

### Recipe 6: Response curve report (PowerPoint deck)

```python
import pptx
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
title = prs.slides.add_slide(prs.slide_layouts[0])
title.shapes.title.text = "MMM Results — Q3 2026"

# Per-channel response curve slide
for channel in ["meta","google","tiktok"]:
    s = prs.slides.add_slide(prs.slide_layouts[5])
    s.shapes.title.text = f"{channel.title()} — Response Curve"
    s.shapes.add_picture(f"mmm_outputs/response_{channel}.png", Inches(0.5), Inches(1.5), width=Inches(9))

# Budget allocation slide
alloc_slide = prs.slides.add_slide(prs.slide_layouts[5])
alloc_slide.shapes.title.text = "Recommended Budget Allocation"
alloc_slide.shapes.add_picture("mmm_outputs/allocation.png", Inches(0.5), Inches(1.5))

prs.save("mmm-report-Q3.pptx")
```

### Recipe 7: lightweight_mmm (simpler alternative)

```python
from lightweight_mmm import lightweight_mmm
from lightweight_mmm import preprocessing, optimize_media

# Preprocess
media_scaler = preprocessing.CustomScaler(divide_operation=jnp.mean)
target_scaler = preprocessing.CustomScaler(divide_operation=jnp.mean)
media_scaled = media_scaler.fit_transform(media_data)
target_scaled = target_scaler.fit_transform(target)

# Fit
mmm = lightweight_mmm.LightweightMMM(model_name="hill_adstock")
mmm.fit(media=media_scaled, target=target_scaled, number_warmup=1000, number_samples=2000)

# Optimize
solution = optimize_media.find_optimal_budgets(
  n_time_periods=4,
  media_mix_model=mmm,
  budget=1_000_000,
  prices=jnp.ones(len(media_scaler.scale_factors))
)
```

## Examples — quarterly MMM cycle

```yaml
cycle:
  data_prep_day_1:
    - SQL pull from postgresql-mcp warehouse (104 weeks)
    - export mmm_input.csv
    - QA: no missing weeks, no zero-spend with revenue weeks
  
  model_day_2:
    - Run Meridian (4 chains × 2000 draws, ~30min on M2)
    - Validate convergence (R-hat < 1.05)
    - Generate response curves
  
  validate_day_3:
    - Hold-out last 4 weeks; check MAPE < 15%
    - Compare to MTA (Triple Whale) shadow — document gap
    - Sanity check: contribution by channel matches account knowledge
  
  report_day_4:
    - Generate pptx via Recipe 6
    - Present to CMO / CFO / paid-team lead
    - Capture decisions
  
  apply_day_5:
    - Update next-quarter budget by channel per MMM recommendation
    - Add 20% reserved for testing
    - Document model choice + decision rationale
```

## Edge cases

### MMM lies at small spend
Channels under $5K/month / $20K/quarter contribute too little signal for MMM. Lump into "Other" or exclude.

### Adstock decay misconfigured
Default geometric adstock decay (Robyn `theta`): 0.1-0.5 for short-funnel (search, social DR). 0.3-0.7 for upper-funnel (YouTube, display). Wrong adstock distorts curves.

### Multicollinearity (correlated channels)
When Meta + TikTok scale together, MMM can't disambiguate. Force geo or time-based variance via geo holdouts (Meridian GeoX) or staggered tests.

### Reverse causality
Higher revenue → marketing team spends more → MMM falsely credits spend. Use Granger causality test or lag-explicit modeling.

### Promo + paid overlap
Promo period spend × promo flag confounds. Include `promo_flag` as control variable; let model learn baseline lift.

### Geo / market heterogeneity
National MMM treats all markets equal — wrong for regional brands. Use geo-level Meridian or per-market separate models.

### Bayesian priors matter
Tight priors → quick convergence + bias. Loose priors → slow + variance. PyMC-Marketing's default priors are reasonable; document changes.

### Out-of-sample validation
Always hold out 4-8 weeks. MAPE < 15% acceptable; > 25% — re-spec model.

### Brand search incrementality
Brand search MMM coefficient = controversy. Use geo-test or Holdout Test for true incrementality estimate.

### MMM ≠ MTA
MMM = top-down channel/spend response. MTA = bottom-up per-conversion path. Both useful, different lens. Don't argue which is "right."

### Refresh cadence
Quarterly minimum. After major seasonality shift (Q4 promo) or new channel launch, refresh sooner.

## Sources

- Google Meridian: https://developers.google.com/meridian
- Meridian GitHub: https://github.com/google/meridian
- Meridian GeoX paper: https://research.google/pubs/pub45950/
- Meta Robyn: https://facebookexperimental.github.io/Robyn/
- Robyn GitHub: https://github.com/facebookexperimental/Robyn
- PyMC-Marketing: https://www.pymc-marketing.io/
- PyMC-Marketing GitHub: https://github.com/pymc-labs/pymc-marketing
- lightweight_mmm: https://lightweight-mmm.readthedocs.io/
- Recast.ai: https://getrecast.com/
- Bayesian MMM theory: https://research.google/pubs/bayesian-methods-for-media-mix-modeling-with-carryover-and-shape-effects/
- Geo-test methodology: https://research.google/pubs/pub42936/
