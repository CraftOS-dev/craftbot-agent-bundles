# Data Analyst — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Warehouse dialect cheat sheet", "dbt project structure playbook", "dbt test catalog", "SQL refactor playbook", "Cohort retention playbook", "A/B test playbook", "Bayesian A/B playbook", "Attribution playbook", "Marketing mix modeling playbook", "Forecasting playbook", "Causal inference playbook", "Anomaly detection playbook", "Data quality playbook", "Reverse ETL playbook", "ELT design playbook", "Dashboard design playbook", "Warehouse cost playbook", "Customer segmentation playbook", "Statistical rigor checklist", "Report templates", "SOTA tool reference", "SOTA execution playbook".

For provenance, see `SOURCES.md`. For per-use-case SOTA mapping, see `reference/SOTA_USE_CASES.md`.

---

## Capability reference

### Warehouses supported

- **Snowflake** — credits-based; auto-suspend / multi-cluster / query acceleration / result cache
- **BigQuery** — on-demand or flat-rate slots; partitioning + clustering essential
- **Databricks SQL** — Photon engine; Delta Lake under the hood; warehouse vs job cluster
- **Redshift** — slot-based with workload management; recently RA3 + Spectrum
- **ClickHouse** — column-store OLAP; MergeTree engine; materialized views first-class
- **Firebolt** — recent entrant; Aggregating Indexes
- **StarRocks** — OSS Snowflake-alike on Apache 2.0
- **MotherDuck** — DuckDB cloud; hybrid local/cloud execution
- **DuckDB** — embedded OLAP, ideal for local prototyping + small workloads
- **Postgres** — ad-hoc analytics fallback when warehouse not available

### Dataframe / local-compute libraries

- **Polars** — Rust-backed, lazy execution, multi-core parallelism, drop-in for pandas
- **pandas 2.x** — `pyarrow` backend, Copy-on-Write, nullable dtypes
- **Ibis** — universal dataframe API; compiles to SQL or pandas/Polars backend
- **Vaex** — out-of-memory dataframes for >RAM datasets
- **Dask** — distributed pandas-equivalent
- **Modin** — drop-in pandas with multi-core / distributed backend
- **DuckDB Python** — SQL-on-Python, `.sql()` on a DataFrame

### BI / dashboard / notebook tools

| Tool | OSS? | Strength | When to choose |
|---|---|---|---|
| Hex | No (free tier) | Notebooks-as-products, SQL + Python + chart cells | Analyst-authored apps, collaboration |
| Metabase | Yes (OSS) | Self-serve dashboards, embeddable | OSS-first; small/medium org self-serve |
| Looker | No (Google) | LookML governed metrics, enterprise | Enterprise; governed metric layer mandatory |
| Lightdash | Yes (OSS) | OSS Looker on top of dbt | dbt-first stack, want governance without Looker |
| Sigma Computing | No | Spreadsheet-style power-user BI | Finance / ops teams that live in Excel |
| Mode | No | SQL + Python + R notebooks, then dashboards | Analyst-authored exploratory work |
| Superset | Yes (OSS / Apache) | Dashboard breadth, OSS at scale | OSS Looker-alike for large orgs |
| Redash | Yes (OSS) | Lightweight SQL + chart sharing | Quick wins |
| Evidence.dev | Yes (OSS) | Markdown reports with SQL + Plotly | Code-first reports, version-controlled |
| Observable | No (free tier) | D3.js-native notebooks | Custom visualization-heavy |
| Streamlit | Yes (OSS) | Python-only apps | Quick app prototypes |
| Plotly Dash | Yes (OSS) | Production Python apps | More polish than Streamlit |
| Marimo | Yes (OSS) | Reactive notebooks, git-friendly, no hidden state | Modern Jupyter replacement |
| Quarto | Yes (OSS) | Academic-grade reproducible reports | LaTeX-grade output |

### Visualization libraries

- **Plotly** — interactive HTML/PNG via kaleido
- **Altair** — declarative grammar of graphics (Vega-Lite under the hood)
- **matplotlib + seaborn** — publication-grade static
- **Bokeh** — interactive in-browser
- **Datawrapper API** — embed-grade for media publishers
- **Flourish** — story-driven embed
- **D3.js** — custom via Observable

### Statistical / ML libraries

- **statsmodels** — frequentist regression, GLM, time-series, power analysis
- **scipy.stats** — primitives: t-test, chi-square, ANOVA, non-parametric
- **pingouin** — cleaner stats API with effect sizes + CIs + Bayesian variants
- **lifelines** — survival analysis (Kaplan-Meier, Cox, Aalen)
- **PyMC / NumPyro / Stan** — Bayesian inference
- **scikit-learn** — ML primitives (regression, classification, clustering, dim-reduction)
- **xgboost / LightGBM / CatBoost** — gradient-boosted trees
- **Prophet** — additive forecasting with seasonality + holidays
- **Darts** — unified forecasting (Exponential Smoothing → NBEATS → TFT)
- **skforecast** — scikit-learn regressors as forecasters
- **pmdarima** — auto-ARIMA
- **DoWhy / EconML** — causal inference (DAG-based + double ML)
- **linearmodels** — 2SLS IV, Panel OLS
- **CausalImpact (Google)** — synthetic control for time-series causal
- **PyOD / ADTK** — outlier and time-series anomaly detection
- **lifetimes** — BG/NBD + Gamma-Gamma LTV models (Fader)

### Experimentation platforms

- **Statsig** — proprietary; sequential testing, holdouts, feature flags
- **GrowthBook** — OSS; Bayesian + frequentist, dbt integration
- **Eppo** — proprietary; causal modeling for analyses
- **Optimizely / LaunchDarkly Galaxy** — proprietary; flagging-first then experiments
- **Convert** — proprietary; CRO-focused
- **Hypothesis** — engineering-grade property-based testing (different sense; not an A/B platform)

### Data quality / observability tools

- **Great Expectations** — declarative expectations + Data Docs HTML
- **Soda Core / Cloud** — SodaCL YAML in CI
- **dbt tests** — warehouse-native primitives + dbt-expectations / dbt-utils packages
- **Monte Carlo Data / Bigeye / Acceldata / Sifflet** — observability platforms (paid)
- **OpenMetadata / DataHub / Amundsen** — OSS catalogs with quality features

### ELT / pipeline tools

- **Fivetran** — managed, 300+ connectors, paid
- **Airbyte** — OSS, 300+ connectors, self-hosted or Cloud
- **Stitch (Talend)** — budget alternative
- **Hevo** — managed alt
- **dlt (Data Load Tool)** — Python OSS, code-first ELT, modern (2024+)

### Reverse-ETL tools

- **Census** — paid, warehouse-first reverse ETL
- **Hightouch** — paid, similar to Census
- **Polytomic** — paid alt
- **Rudderstack** — CDP with reverse-ETL capability
- **dlt** — code-first custom syncs

### Catalog / discovery

- **Atlan** — paid; modern catalog
- **DataHub (LinkedIn → Apache)** — OSS
- **Amundsen (Lyft)** — OSS
- **Select Star** — paid; lineage-first
- **OpenMetadata** — OSS, recent

### Transformation tooling

- **dbt Core / dbt Cloud** — SQL-based transformation, tests, docs, lineage
- **SQLMesh** — modern dbt alternative; semantic versioning, dialect-agnostic
- **Coalesce** — visual dbt-alike for Snowflake
- **Sqlfluff** — SQL linter (auto-fix)
- **Sqlglot** — SQL parser / transpiler / optimizer

---

## Warehouse dialect cheat sheet

Common pitfalls when switching dialects:

| Operation | Snowflake | BigQuery | Databricks | Redshift | DuckDB |
|---|---|---|---|---|---|
| Window function name | `QUALIFY` clause supported | `QUALIFY` supported | `QUALIFY` supported | not supported | supported |
| Array agg | `ARRAY_AGG` | `ARRAY_AGG` | `COLLECT_LIST` | `LISTAGG` (string) | `LIST` |
| String split | `SPLIT(s, ',')` returns array | `SPLIT(s, ',')` | `SPLIT(s, ',')` | `SPLIT_TO_ARRAY` | `STRING_SPLIT` |
| Date diff | `DATEDIFF('day', a, b)` | `DATE_DIFF(b, a, DAY)` | `DATEDIFF(DAY, a, b)` | `DATEDIFF('day', a, b)` | `b - a` |
| Date trunc | `DATE_TRUNC('week', d)` | `DATE_TRUNC(d, WEEK)` | `DATE_TRUNC('week', d)` | `DATE_TRUNC('week', d)` | `DATE_TRUNC('week', d)` |
| Generate series | `GENERATOR(ROWCOUNT=>n)` | `GENERATE_ARRAY(0, n)` | `range(0, n)` | recursive CTE | `RANGE(0, n)` |
| Median | `MEDIAN(x)` or `PERCENTILE_CONT(0.5)` | `APPROX_QUANTILES(x, 100)[OFFSET(50)]` | `percentile(x, 0.5)` | `PERCENTILE_CONT(0.5)` | `MEDIAN(x)` |
| Pivot | native PIVOT | manual `CASE WHEN` | `pivot` clause | manual | `PIVOT` |

Use `sqlglot` to transpile when working across dialects: `sqlglot.transpile(sql, read='snowflake', write='bigquery')[0]`.

---

## dbt project structure playbook

### Recommended directory layout (Kimball-style, per dbt Labs best practices)

```
models/
  staging/
    <source-system>/
      _<source>__sources.yml      # source: + freshness:
      _<source>__models.yml       # column docs + tests
      stg_<source>__<entity>.sql  # 1:1 source-table renaming, type-cast, light cleaning
  intermediate/
    int_<entity>_<verb>.sql       # reusable business-logic primitives
  marts/
    <domain>/                     # e.g., finance/, marketing/, product/
      <entity>__<grain>.sql       # final analytics tables (fact_*, dim_*)
      _<domain>__models.yml
seeds/                            # static CSVs
snapshots/                        # SCD2 tracking
macros/                           # reusable Jinja
tests/                            # singular test SQL files
analyses/                         # one-off analyses (not run by `dbt run`)
```

### Materialization decision tree

1. **View** — default. Cheap to refresh, always fresh. Use when the query is cheap and freshness > cache.
2. **Table** — cache result. Use when the query is expensive and refresh cadence allows.
3. **Incremental** — append/merge new rows only. Use when the source is large + append-only (events, logs, transactions).
4. **Snapshot (SCD2)** — track changes to a mutable dimension. Use when you need history (customer plan changes over time).
5. **Ephemeral** — inline CTE. Use only when the model is small + only referenced once.

### Naming conventions

- `stg_*` — staging (1:1 source rename + light type cast)
- `int_*` — intermediate (business-logic primitive, not user-facing)
- `fct_*` / `dim_*` — fact / dimension in marts
- `<entity>__<grain>.sql` — name encodes what's in it: `orders__by_customer_month.sql`

### dbt-utils + dbt-expectations packages

Install via `packages.yml`:

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: calogica/dbt_expectations
    version: 0.10.4
```

dbt-utils offers `surrogate_key`, `date_spine`, `pivot`, `union_relations`. dbt-expectations ports Great Expectations into dbt tests: `expect_column_values_to_be_between`, `expect_column_mean_to_be_between`, etc.

---

## dbt test catalog

### Built-in generic tests (in YAML)

- `unique` — primary-key uniqueness
- `not_null` — column must not have nulls
- `accepted_values: values: [...]` — enum constraint
- `relationships: to: ref('other'), field: id` — FK exists

### Source freshness

```yaml
sources:
  - name: raw
    tables:
      - name: orders
        freshness:
          warn_after: { count: 12, period: hour }
          error_after: { count: 24, period: hour }
        loaded_at_field: _loaded_at
```

### Singular tests (in `tests/` as `.sql`)

```sql
-- tests/assert_orders_total_matches_lineitems.sql
-- Fail rows where order total ≠ sum of line items
select order_id, total, sum(line_item_amount) as line_sum
from {{ ref('fct_orders') }} o
join {{ ref('fct_order_lines') }} l using (order_id)
group by order_id, total
having total != sum(line_item_amount)
```

### dbt-expectations highlights

- `expect_column_values_to_be_between(column_A, min_value=0, max_value=1)`
- `expect_column_mean_to_be_between(revenue, min_value=100, max_value=10000)`
- `expect_column_pair_values_A_to_be_greater_than_B(end_date, start_date)`
- `expect_row_values_to_have_recent_data(timestamp_col, datepart=day, interval=1)`

---

## SQL refactor playbook

### sqlfluff configuration

`.sqlfluff` in repo root:

```ini
[sqlfluff]
dialect = snowflake
templater = dbt
exclude_rules = L029, L036
max_line_length = 120

[sqlfluff:rules:L010]
capitalisation_policy = lower

[sqlfluff:templater:dbt]
project_dir = ./
```

Run: `sqlfluff lint models/marts/finance/fct_orders.sql --dialect snowflake` and `sqlfluff fix` to auto-correct.

### sqlglot transpilation + optimization

```python
import sqlglot
from sqlglot.optimizer import optimize

src_sql = "select * from orders where created_at > '2025-01-01'"
bq_sql = sqlglot.transpile(src_sql, read='snowflake', write='bigquery')[0]

# Or optimize (qualify columns, simplify, predicate pushdown)
optimized = optimize(sqlglot.parse_one(src_sql, read='snowflake'))
print(optimized.sql(pretty=True))
```

### Performance refactors (warehouse-agnostic)

- **Push predicates down** — filter early, join later
- **Project only needed columns** — `SELECT col_a, col_b` not `SELECT *`
- **Use window functions over self-joins** when computing per-group ranks/lags
- **Materialize repeated CTEs** — promote to a dbt model if referenced > 2x
- **Partition / cluster the source table** (warehouse-specific) on the most-used filter column

---

## Cohort retention playbook

### Cohort definition decision tree

1. **Acquisition cohort** — group by signup week/month. Q: is the product getting better over time?
2. **Behavioral cohort** — group by behavior (used X in first 7 days). Q: what behaviors predict retention?
3. **Segment cohort** — group by plan / channel / company size. Q: which segments retain best?

### N-day vs rolling retention

- **N-day** — % active on day N (point measurement). Use for daily-use apps (social, news).
- **Rolling** — % active in window after day N (cumulative). Use for weekly/monthly-use apps (SaaS, finance).

### SQL pattern for N-day retention table

```sql
with cohorts as (
  select user_id, date_trunc('week', signup_at) as cohort_week
  from users
),
events as (
  select user_id, date_trunc('week', event_at) as activity_week
  from product_events
)
select
  c.cohort_week,
  datediff(week, c.cohort_week, e.activity_week) as weeks_since_signup,
  count(distinct c.user_id) as active_users
from cohorts c
left join events e using (user_id)
group by 1, 2
order by 1, 2
```

Then pivot to wide format for the cohort table.

### Kaplan-Meier survival curve

```python
from lifelines import KaplanMeierFitter

kmf = KaplanMeierFitter()
kmf.fit(durations=df['days_to_churn'], event_observed=df['churned'])
kmf.plot_survival_function(ci_show=True)
kmf.median_survival_time_  # median lifetime
kmf.survival_function_     # full curve
```

Compare cohorts via log-rank test:

```python
from lifelines.statistics import logrank_test
result = logrank_test(d_a, d_b, e_a, e_b)
print(result.p_value, result.test_statistic)
```

### Retention curve diagnosis

```
Healthy:   ████ Flattens to a positive asymptote (some users retain forever)
              ██
                ████████████████ ← holds at X% forever
           +----------------------- time

Dying:     ████  Slopes toward zero
              ████
                  ████
                      ████▼ ← approaching 0
           +----------------------- time
```

If the curve approaches zero, it's a product-market-fit problem, not a growth problem. More acquisition won't fix it.

### Aha Moment identification

1. Bucket users into high-retention (top quartile by day-30 retention) vs low-retention (bottom quartile)
2. For each candidate behavior (added friend, sent message, completed onboarding step X), compute % of high vs low cohort that did it in first N days
3. Behavior with largest delta = Aha Moment candidate
4. Validate via A/B test on onboarding nudge

Classic examples: Facebook 7-friends-in-10-days, Slack 2,000-messages-as-team, Twitter follow-30-users.

### LTV calculation patterns

- **Cohort-based** — `LTV = sum over t of (revenue_per_user_at_t × P(active_at_t))`
- **Survival-based** — `lifelines.CoxPHFitter` with revenue covariate; integrate hazard-adjusted curve
- **BG/NBD + Gamma-Gamma** — `lifetimes` package; canonical for transactional businesses

---

## A/B test playbook

### Pre-experiment checklist

- [ ] Hypothesis stated (H0 vs H1)
- [ ] Primary metric identified (singular; if multiple, mark them and apply correction)
- [ ] Guardrail metrics identified (revenue can't drop, latency can't spike)
- [ ] Expected effect size (MDE) chosen with business context
- [ ] Alpha = 0.05 (default), power = 0.8 (default)
- [ ] Sample size computed BEFORE experiment via `statsmodels.stats.power`
- [ ] Randomization unit declared (user_id vs session vs visit)
- [ ] Sample ratio sanity check planned (SRM test)

### Sample size + MDE calculation

```python
from statsmodels.stats.power import TTestIndPower, NormalIndPower

# T-test for means
analysis = TTestIndPower()
n = analysis.solve_power(effect_size=0.05, alpha=0.05, power=0.8, alternative='two-sided')
# n is per-arm sample size

# Z-test for proportions
from statsmodels.stats.proportion import samplesize_proportions_2indep_onetail
n = samplesize_proportions_2indep_onetail(
    diff=0.02, prop2=0.10, power=0.8, alpha=0.05
)
```

### Frequentist test selection

| Metric type | Test | Code |
|---|---|---|
| Continuous, normal | Welch's t-test | `scipy.stats.ttest_ind(a, b, equal_var=False)` |
| Continuous, non-normal | Mann-Whitney U | `scipy.stats.mannwhitneyu(a, b)` |
| Proportion / binary | z-test for proportions | `statsmodels.stats.proportion.proportions_ztest` |
| Count | Poisson exact test | `scipy.stats.poisson_means_test` |
| Survival | log-rank | `lifelines.statistics.logrank_test` |
| Multi-arm | ANOVA + Tukey HSD | `scipy.stats.f_oneway` + `statsmodels.stats.multicomp.pairwise_tukeyhsd` |

### Sequential testing (to avoid peeking penalty)

Standard frequentist: NEVER peek mid-experiment. P-values become invalid if you stop early on positive results.

Sequential frameworks:
- **mSPRT** (mixture Sequential Probability Ratio Test) — always-valid p-values
- **Always-Valid Inference** (Howard et al.) — confidence sequences
- **GrowthBook / Statsig** — built-in mSPRT support
- **Bayesian framework** — peeking is fine if you report posterior, not p-value

### CUPED variance reduction

If you have a pre-experiment covariate `Y_pre` that correlates with `Y` during the experiment, subtract its predicted contribution:

```python
theta = np.cov(Y_pre, Y)[0,1] / np.var(Y_pre)
Y_cuped = Y - theta * (Y_pre - Y_pre.mean())
```

CUPED can reduce required sample size by 30-50%.

### Report template

```
HYPOTHESIS: <H0 vs H1>
METRIC: <primary metric definition>
VARIANT A (control): n=<X>, mean=<μ_a>, SD=<σ_a>
VARIANT B (treat):   n=<Y>, mean=<μ_b>, SD=<σ_b>
EFFECT SIZE: <μ_b - μ_a>, Cohen's d = <d>
95% CI: [<lower>, <upper>]
P-VALUE: <p> (Welch's t-test, two-sided)
POWER: <achieved>
GUARDRAILS: <list of guardrail metrics, status>
SRM (sample ratio): <p-value> — flag if <0.001
RECOMMENDATION: <ship / hold / extend / kill> with confidence
```

---

## Bayesian A/B playbook

### Beta-Binomial conjugate (proportions)

For conversion-rate experiments with proportions, there's a closed-form posterior:

```python
import numpy as np
from scipy.stats import beta

# Prior: Beta(1, 1) = uniform
alpha_a, beta_a = 1 + conversions_a, 1 + (n_a - conversions_a)
alpha_b, beta_b = 1 + conversions_b, 1 + (n_b - conversions_b)

# Sample posteriors
samples_a = beta.rvs(alpha_a, beta_a, size=100_000)
samples_b = beta.rvs(alpha_b, beta_b, size=100_000)

prob_b_better = (samples_b > samples_a).mean()
expected_lift = ((samples_b - samples_a) / samples_a).mean()
hdi_lower, hdi_upper = np.percentile(samples_b - samples_a, [2.5, 97.5])
expected_loss = np.maximum(samples_a - samples_b, 0).mean()  # downside risk

print(f"P(B>A) = {prob_b_better:.3f}, expected lift = {expected_lift:.3%}")
print(f"95% HDI on lift: [{hdi_lower:.3%}, {hdi_upper:.3%}]")
print(f"Expected loss if you ship B: {expected_loss:.4f}")
```

### PyMC for hierarchical / continuous

```python
import pymc as pm

with pm.Model() as model:
    mu_a = pm.Normal('mu_a', 0, 1)
    mu_b = pm.Normal('mu_b', 0, 1)
    sigma = pm.HalfNormal('sigma', 1)
    pm.Normal('y_a', mu_a, sigma, observed=y_a_data)
    pm.Normal('y_b', mu_b, sigma, observed=y_b_data)
    diff = pm.Deterministic('diff', mu_b - mu_a)
    trace = pm.sample(2000, tune=1000, target_accept=0.9)

az.summary(trace, var_names=['mu_a', 'mu_b', 'diff'])
```

### Decision rules

- **Ship B if P(B>A) > 0.95 AND expected loss < tolerance**
- **Kill B if P(B>A) < 0.05 AND HDI excludes meaningful improvement**
- **Continue if HDI straddles zero AND expected loss bearable**

---

## Attribution playbook

### Rule-based (SQL)

```sql
-- Last-touch attribution
with conversions as (
  select user_id, conversion_id, conversion_at, conversion_value
  from fct_conversions
),
touches as (
  select user_id, channel, touch_at
  from fct_marketing_touches
),
last_touch as (
  select c.conversion_id, c.conversion_value,
         t.channel as attributed_channel,
         row_number() over (partition by c.conversion_id
                            order by t.touch_at desc) as rn
  from conversions c
  left join touches t
    on t.user_id = c.user_id and t.touch_at <= c.conversion_at
)
select attributed_channel, sum(conversion_value) as revenue
from last_touch
where rn = 1
group by 1
```

Variants: first-touch, linear (1/N per touch), time-decay (exponential weight), position-based (40/20/40).

### Data-driven (Shapley / Markov)

- **Shapley value** — cooperative game theory; allocate credit by marginal contribution. Computationally expensive (2^N coalitions).
- **Markov chain** — model paths as transitions; attribute by removal effect ("what conversion rate drops if channel X is removed?"). Available via R `ChannelAttribution` or custom Python.

### Marketing Mix Modeling (MMM)

Bayesian regression with adstock + saturation:

```
conversion_t = β_0
             + Σ_channel β_ch × Hill(Adstock(spend_ch_t, decay_ch), K_ch, slope_ch)
             + γ × control_vars_t
             + ε_t
```

Adstock = carryover (today's TV spend still drives tomorrow's conversion). Hill saturation = diminishing returns.

Implementations:
- **Google Meridian** (NumPyro/JAX, 2024+) — current SOTA
- **lightweight_mmm** (Google, 2022) — earlier, smaller datasets
- **Meta Robyn** (R) — Meta's open-source MMM

Output: per-channel ROI, optimal spend allocation, response curves with uncertainty.

---

## Forecasting playbook

### Decision tree

1. **Daily / weekly data with seasonality + holidays** → Prophet
2. **Need interpretability or classical reviewers** → ARIMA / SARIMA via statsmodels
3. **Multiple related series** → Darts (NBEATS, TFT, etc.)
4. **Have ML features beyond the series itself** → skforecast (use any scikit-learn regressor)
5. **Hierarchical (totals must reconcile)** → Darts hierarchical reconciliation

### Prophet quickstart

```python
from prophet import Prophet
df = data.rename(columns={'date': 'ds', 'metric': 'y'})

m = Prophet(yearly_seasonality=True, weekly_seasonality=True,
            changepoint_prior_scale=0.05, seasonality_prior_scale=10)
m.add_country_holidays(country_name='US')
m.fit(df)

future = m.make_future_dataframe(periods=90)
forecast = m.predict(future)
m.plot(forecast)
m.plot_components(forecast)  # decomposition
```

### Backtesting

Use rolling-origin cross-validation, not random split:

```python
from prophet.diagnostics import cross_validation, performance_metrics
df_cv = cross_validation(m, initial='730 days', period='30 days', horizon='90 days')
df_p = performance_metrics(df_cv)  # MAPE, sMAPE, MAE, RMSE per horizon
```

### Always report

- Point forecast
- 80% AND 95% prediction interval
- Train/test MAPE
- Assumptions (stationarity, seasonality, holidays, structural breaks identified)
- Out-of-sample backtest results

---

## Causal inference playbook

### Method selection ladder (strongest → weakest)

1. **RCT (A/B test)** — gold standard. Use whenever feasible.
2. **Regression discontinuity (RDD)** — exploit a sharp cutoff in assignment (passing a threshold).
3. **Difference-in-differences (DiD)** — pre/post × treatment/control with parallel trends.
4. **Instrumental variables (IV)** — find a variable that affects treatment but not outcome directly.
5. **Synthetic control** — construct a weighted combination of control units that matches pre-treatment trajectory.
6. **Propensity score matching** — match treated and untreated on probability of treatment.
7. **Observational regression with controls** — weakest; requires no unobserved confounders (rarely true).

### DoWhy workflow

```python
from dowhy import CausalModel

model = CausalModel(
    data=df,
    treatment='campaign_exposed',
    outcome='conversion',
    common_causes=['age', 'plan', 'tenure'],
    graph="""digraph { age->campaign_exposed; age->conversion;
                       plan->campaign_exposed; plan->conversion;
                       tenure->campaign_exposed; tenure->conversion;
                       campaign_exposed->conversion }"""
)
identified = model.identify_effect()
estimate = model.estimate_effect(identified,
                                 method_name='backdoor.propensity_score_matching')
refute = model.refute_estimate(identified, estimate,
                               method_name='placebo_treatment_refuter')
```

### Causal report template

```
CAUSAL QUESTION: <treatment X → outcome Y?>
DAG:             <ASCII or attached image>
IDENTIFICATION:  <strategy: RCT / RDD / DiD / IV / PSM / SCM / OLS-with-controls>
ASSUMPTIONS:     <list, e.g., "parallel trends pre-treatment", "exogenous instrument", "SUTVA">
ESTIMATE (ATE):  <point estimate>
95% CI:          [<lower>, <upper>]
SENSITIVITY:     <e-value or Rosenbaum bound — how much unobserved confounding would invalidate?>
PLACEBO TEST:    <result>
VIOLATIONS:      <flag anything that breaks the assumptions>
```

---

## Anomaly detection playbook

### Statistical methods (univariate time series)

- **Rolling z-score** — `(x - rolling_mean) / rolling_std > k`
- **MAD (Median Absolute Deviation)** — robust to outliers
- **ESD (Generalized ESD)** — for multiple outliers, statsmodels
- **Prophet residuals** — confidence-interval breach
- **STL decomposition residuals** — robust seasonality + residual check

### ML methods (multivariate)

- **Isolation Forest** — fast, scales
- **One-Class SVM** — slower, more flexible kernel
- **Autoencoder reconstruction error** — deep, requires more data
- **DBSCAN-based outliers** — density-based

### Library cheat sheet

```python
# PyOD
from pyod.models.iforest import IForest
clf = IForest(contamination=0.05).fit(X)
labels = clf.predict(X)  # 1 = outlier, 0 = normal
scores = clf.decision_function(X)

# ADTK for time series
from adtk.detector import ThresholdAD, QuantileAD, InterQuartileRangeAD
detector = QuantileAD(high=0.99, low=0.01)
anomalies = detector.fit_detect(series)
```

### Production monitoring patterns

- **Dynamic thresholds** — rolling quantile (not static value) accommodates trend + seasonality
- **Business-context overlay** — exclude known event windows (launches, holidays, marketing campaigns)
- **Multi-tier alerting** — warn / page tiered by severity
- **Root cause hints** — when an anomaly fires, automatically pull the top-N contributors (drill-down)

---

## Data quality playbook

### Great Expectations quickstart

```python
import great_expectations as gx

context = gx.get_context()
datasource = context.sources.add_pandas('df')
asset = datasource.add_dataframe_asset(name='orders', dataframe=df)
suite = context.add_expectation_suite('orders_suite')
batch = asset.build_batch_request()
validator = context.get_validator(batch_request=batch, expectation_suite_name='orders_suite')

validator.expect_column_values_to_not_be_null('order_id')
validator.expect_column_values_to_be_between('amount', 0, 100000)
validator.expect_column_values_to_be_in_set('status', ['pending', 'paid', 'refunded'])
validator.save_expectation_suite()

checkpoint = context.add_checkpoint(name='orders_checkpoint',
                                     validations=[{'batch_request': batch,
                                                   'expectation_suite_name': 'orders_suite'}])
result = checkpoint.run()
context.build_data_docs()
```

### Soda Core

`checks.yml`:

```yaml
checks for orders:
  - row_count > 1000
  - duplicate_count(order_id) = 0
  - missing_count(customer_id) = 0
  - invalid_count(status) = 0:
      valid values: [pending, paid, refunded]
  - avg(amount) between 50 and 500
```

Run: `soda scan -d warehouse -c configuration.yml checks.yml`

### CI integration

- **GitHub Actions** — run `soda scan` / `great_expectations checkpoint run` on PR; fail PR if check fails
- **Airflow / Dagster** — add data-quality task as a step; downstream tasks block on failure
- **dbt build** — `dbt build` runs tests after each model; the DAG halts on first test failure

---

## Reverse ETL playbook

### When to use

- "Push the warehouse customer-LTV table back to Salesforce so sales reps see it"
- "Sync the propensity-to-churn score to Marketo as a list"
- "Update HubSpot contact records with last-purchase-date from the warehouse"
- "Trigger a Slack alert when a key account's health-score drops"

### Tool selection

| Need | Tool |
|---|---|
| Managed, broad SaaS coverage | Census or Hightouch |
| Polytomic alternative | Polytomic |
| CDP-style with reverse-ETL inside | Rudderstack |
| Custom / one-off / OSS | dlt + per-SaaS API |

### Census / Hightouch pattern

1. Define **model** in warehouse (a query or dbt model) that produces the desired records
2. Define **sync** that maps warehouse columns → SaaS object fields
3. Choose **trigger**: scheduled (cron), event-driven, or warehouse-trigger (PostHog / Snowplow event)
4. Add **monitoring** for sync health and row deltas

### dlt custom example

```python
import dlt

@dlt.resource(name='salesforce_contact_updates')
def get_contacts_to_sync():
    yield from warehouse.execute("select * from mart.contact_sync_payload").fetchall()

p = dlt.pipeline(pipeline_name='warehouse_to_salesforce',
                 destination='salesforce', dataset_name='Contact')
p.run(get_contacts_to_sync())
```

---

## ELT design playbook

### Architecture stages

1. **Source** — SaaS (Stripe, HubSpot), DB (Postgres replica), event stream (Kafka, Snowplow), file (S3)
2. **Ingestion** — Fivetran / Airbyte / dlt → land raw → warehouse `raw` schema
3. **Staging (dbt)** — `stg_<source>__<entity>` — 1:1 type cast + rename
4. **Intermediate (dbt)** — `int_<entity>__<verb>` — reusable logic primitives
5. **Marts (dbt)** — `fct_*` + `dim_*` — final analytics tables
6. **Consumption** — BI tool / reverse ETL / ML model

### Tool decision

| Constraint | Tool |
|---|---|
| Managed, 300+ connectors, budget OK | Fivetran |
| OSS, want self-host, 300+ connectors | Airbyte |
| Code-first Python, custom logic | dlt |
| Budget alt | Stitch |

### dlt example

```python
import dlt
from dlt.sources.helpers.rest_client import RESTClient

@dlt.source
def hubspot_source(api_key):
    client = RESTClient(base_url='https://api.hubapi.com',
                        headers={'Authorization': f'Bearer {api_key}'})
    @dlt.resource(write_disposition='merge', primary_key='id')
    def contacts():
        for page in client.paginate('/crm/v3/objects/contacts'):
            yield page['results']
    return contacts

p = dlt.pipeline(pipeline_name='hubspot_to_snowflake',
                 destination='snowflake', dataset_name='raw_hubspot')
p.run(hubspot_source(api_key=os.getenv('HUBSPOT_KEY')))
```

---

## Dashboard design playbook

### KPI tiers

| Tier | Audience | Update | KPIs |
|---|---|---|---|
| Strategic | Executives | Monthly / Quarterly | 4-6 |
| Tactical | Managers | Weekly / Monthly | 5-7 per dept |
| Operational | Teams | Real-time / Daily | 5-10 per workflow |

### Per-tool patterns

- **Hex** — magic SQL cells with Python downstream; deploy as app with input cells for params
- **Metabase** — Question → Dashboard; row-level security via groups; signed JWT for embedding
- **Looker** — model in LookML (explores, views, measures); governed metrics; embedded SDK
- **Lightdash** — surfaces dbt metrics + dimensions; no separate semantic layer
- **Sigma** — workbooks (Excel-like); column-store fast against warehouse
- **Evidence.dev** — `.md` + ```sql``` + ```js``` chart blocks → static HTML site

### Dashboard checklist

- [ ] Audience tier identified (strategic / tactical / operational)
- [ ] 5-7 KPI limit per view honored
- [ ] "So what" header paragraph above charts
- [ ] Date freshness shown ("As of: 2026-06-09 14:00 UTC")
- [ ] Comparison context (vs last period, vs target)
- [ ] Drill-downs available (not crammed into top-level view)
- [ ] Row-level security implemented (governed metrics layer)
- [ ] Owner + contact info embedded

---

## Warehouse cost playbook

### Snowflake credit attribution

```sql
-- Top 20 most-expensive queries last 7 days
select
  query_text,
  warehouse_name,
  user_name,
  execution_time/1000.0 as exec_seconds,
  credits_used_cloud_services + credits_used as total_credits,
  bytes_scanned/1e9 as gb_scanned
from snowflake.account_usage.query_history
where start_time > current_date - interval '7 days'
order by total_credits desc
limit 20
```

### BigQuery slot / job analysis

```sql
select
  query,
  user_email,
  total_slot_ms / 1000.0 / 3600 as slot_hours,
  total_bytes_processed / 1e9 as gb_scanned,
  cost_estimate_usd
from `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
where creation_time > timestamp_sub(current_timestamp(), interval 7 day)
  and job_type = 'QUERY'
order by total_slot_ms desc
limit 20
```

### Optimization checklist

- [ ] Auto-suspend tuned (Snowflake: 60s default; raise for spiky workloads)
- [ ] Result cache + query cache enabled
- [ ] Partitioning + clustering on warehouse tables (BigQuery / Snowflake / Databricks)
- [ ] dbt models materialized incremental where source is large + append-only
- [ ] Materialized views for frequently-queried aggregates
- [ ] Warehouse right-sizing (don't run XL when M is enough)
- [ ] Multi-cluster for concurrency, not size
- [ ] Predicate pushdown verified via EXPLAIN

---

## Customer segmentation playbook

### RFM (Recency / Frequency / Monetary)

```sql
with rfm as (
  select user_id,
    datediff(day, max(order_at), current_date) as recency,
    count(*) as frequency,
    sum(order_value) as monetary
  from fct_orders
  where order_at > current_date - interval '365 days'
  group by 1
)
select user_id,
  ntile(5) over (order by recency desc)        as r_score,  -- desc: more recent = higher
  ntile(5) over (order by frequency)            as f_score,
  ntile(5) over (order by monetary)             as m_score
from rfm
```

### Behavioral / ML clustering

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

X_scaled = StandardScaler().fit_transform(features_df)

# Pick k via silhouette
for k in range(2, 10):
    km = KMeans(n_clusters=k, random_state=42).fit(X_scaled)
    print(k, silhouette_score(X_scaled, km.labels_))

best_k = 5
km = KMeans(n_clusters=best_k, random_state=42).fit(X_scaled)
df['segment'] = km.labels_
```

For density-based / arbitrary-shape clusters: `hdbscan`.

### Validation

- Inspect feature means per segment — do they make business sense?
- Check segment retention curves — do segments differ?
- Check segment LTV — segments should differ on outcomes you care about

---

## Statistical rigor checklist

For any quantitative claim:

- [ ] Sample size reported?
- [ ] Effect size reported (not just p-value)?
- [ ] Confidence interval / posterior HDI reported?
- [ ] Statistical test named (and assumptions checked)?
- [ ] Multiple-comparisons correction applied where needed?
- [ ] Cohort / sample composition described?
- [ ] Selection bias / survivorship bias flagged?
- [ ] Out-of-sample validation (for predictive claims)?
- [ ] Sensitivity analysis (for causal claims)?
- [ ] Source dataset, as-of date, row count attached?
- [ ] Random seed set (for reproducibility)?

---

## Report templates

### Analytics brief (1-page exec summary)

```
TITLE: <topic + key insight in one line>

BOTTOM LINE: <1-2 sentences — decision this supports>

KEY METRIC:
- <metric>: <value> (<CI>, n=<sample>)
- vs target / vs prior period: <delta>

EVIDENCE:
- <finding 1 with query reference>
- <finding 2>

RECOMMENDED ACTIONS:
1. <action with expected impact + confidence>
2. <action>

CAVEATS:
- <limitation 1>
- <limitation 2>

DATA SOURCES: <tables, as-of date>
QUERY: <link to .sql file in git>
```

### A/B test report

See "A/B test playbook → Report template" above.

### Cohort analysis report

```
COHORT: <definition>
SIZE: <n users across <date range>>

RETENTION CURVE:
<table or chart>

CURVE DIAGNOSIS: <healthy / declining / dying>

AHA MOMENT CANDIDATE:
- Behavior: <X>
- Delta: <high-retention cohort: Y%; low-retention: Z%>
- Significance: <p / CI>

RECOMMENDATIONS (ranked by expected retention impact):
1. <recommendation>
2. <recommendation>

CAVEATS:
- <selection bias / sample considerations>
```

### Forecast report

```
SERIES: <metric>
HORIZON: <N periods>
MODEL: <Prophet / ARIMA / Darts NBEATS / etc.>

POINT FORECAST: <chart>
80% PI: <bounds>
95% PI: <bounds>

BACKTEST (rolling-origin):
- MAPE: <%>
- sMAPE: <%>
- MAE: <unit>

ASSUMPTIONS:
- Seasonality: <yearly / weekly / daily>
- Holidays: <country / events>
- Structural breaks: <none / list>

CAVEATS:
- <out-of-distribution risk>
- <stationarity caveat>
```

---

## SOTA tool reference (June 2026)

Per-tool quick reference. Each entry: when to use, primary endpoint / install, source. Detailed recipes live in the bundled skill packs at `skills/<name>/SKILL.md` — heading text below maps 1:1 to the skill folder name (created in Round 2).

### dbt Core (skill: `dbt-modeling-staging-marts`)

- **When:** any SQL transformation pipeline that needs versioning, tests, docs, lineage. The standard for analytics-engineering in 2026.
- **Install:** `cli-anything` → `pip install dbt-core dbt-<adapter>` (snowflake / bigquery / databricks / postgres / duckdb)
- **Quick start:** `dbt init project_name` → fill `profiles.yml` → `dbt run` + `dbt test`
- **Source:** https://docs.getdbt.com/
- **Skill:** `skills/dbt-modeling-staging-marts/SKILL.md` (Round 2)

### dbt Test (skill: `dbt-test-authoring-utils-expectations`)

- **When:** validate model contracts (uniqueness, not-null, freshness, business invariants); CI integration.
- **Install:** included in dbt-core; install dbt-utils + dbt-expectations via `packages.yml`.
- **Quick start:** add `tests:` block in `.yml` for column tests; `tests/*.sql` for singular tests.
- **Source:** https://docs.getdbt.com/docs/build/data-tests · https://github.com/calogica/dbt-expectations
- **Skill:** `skills/dbt-test-authoring-utils-expectations/SKILL.md` (Round 2)

### SQLMesh (alternative to dbt)

- **When:** want semantic versioning, dialect-agnostic models, virtual data environments. Modern dbt-alternative.
- **Install:** `cli-anything` → `pip install sqlmesh`
- **Source:** https://sqlmesh.readthedocs.io/

### Sqlfluff (skill: `dbt-modeling-staging-marts` companion)

- **When:** lint + auto-fix SQL files across dialects. Standard in CI.
- **Install:** `cli-anything` → `pip install sqlfluff`
- **Quick start:** `.sqlfluff` config + `sqlfluff lint model.sql --dialect snowflake` + `sqlfluff fix`
- **Source:** https://docs.sqlfluff.com/

### Sqlglot

- **When:** parse / transpile / optimize SQL programmatically across dialects.
- **Install:** `cli-anything` → `pip install sqlglot`
- **Quick start:** `sqlglot.transpile(sql, read='snowflake', write='bigquery')`
- **Source:** https://sqlglot.com/sqlglot.html

### Snowflake API (skill: `snowflake-bigquery-databricks-warehousing`)

- **When:** Snowflake SDK for query execution + warehouse management + QUERY_HISTORY analytics.
- **Install:** `cli-anything` → `pip install snowflake-connector-python snowflake-sqlalchemy`
- **Source:** https://docs.snowflake.com/en/developer-guide/sql-api/

### BigQuery API (skill: `snowflake-bigquery-databricks-warehousing`)

- **When:** BigQuery SDK + INFORMATION_SCHEMA.JOBS_BY_PROJECT for slot analytics.
- **Install:** `cli-anything` → `pip install google-cloud-bigquery`
- **Source:** https://cloud.google.com/bigquery/docs/reference/rest

### Databricks SQL Connector (skill: `snowflake-bigquery-databricks-warehousing`)

- **When:** Databricks SQL Warehouse execution.
- **Install:** `cli-anything` → `pip install databricks-sql-connector`
- **Source:** https://docs.databricks.com/sql/

### DuckDB + MotherDuck (skill: `duckdb-motherduck-local-olap`)

- **When:** local OLAP prototyping; Parquet over S3; hybrid local/cloud via MotherDuck.
- **Install:** `cli-anything` → `pip install duckdb`; MotherDuck via `duckdb.connect('md:')` + token
- **Source:** https://duckdb.org/docs/ · https://motherduck.com/

### Polars (skill: `polars-pandas-modern-dataframes`)

- **When:** large dataframes (>1GB), need multi-core, want lazy execution.
- **Install:** `cli-anything` → `pip install polars`
- **Source:** https://pola.rs/

### Ibis (skill: `polars-pandas-modern-dataframes`)

- **When:** write dataframe code once, run on any backend (warehouse, pandas, Polars, Spark).
- **Install:** `cli-anything` → `pip install ibis-framework[snowflake]` (or other backend)
- **Source:** https://ibis-project.org/

### lifelines (skill: `cohort-retention-deep-survival`)

- **When:** Kaplan-Meier survival curves with CIs; log-rank cohort comparison; Cox PH hazard regression.
- **Install:** `cli-anything` → `pip install lifelines`
- **Source:** https://lifelines.readthedocs.io/

### scipy.stats (skill: `ab-test-significance-mde-sequential`)

- **When:** primitive statistical tests (t-test, chi-square, ANOVA, non-parametric).
- **Install:** `cli-anything` → `pip install scipy`
- **Source:** https://docs.scipy.org/doc/scipy/reference/stats.html

### statsmodels (skill: `ab-test-significance-mde-sequential`)

- **When:** power analysis, sample-size calculation, GLM, time-series, formula-based regression.
- **Install:** `cli-anything` → `pip install statsmodels`
- **Source:** https://www.statsmodels.org/

### pingouin (skill: `ab-test-significance-mde-sequential`)

- **When:** cleaner stats API with effect sizes + CIs built in; Bayesian variants.
- **Install:** `cli-anything` → `pip install pingouin`
- **Source:** https://pingouin-stats.org/

### PyMC + NumPyro (skill: `bayesian-pymc-numpyro-ab-testing`)

- **When:** full Bayesian regression; A/B with hierarchical priors; MMM backend.
- **Install:** `cli-anything` → `pip install pymc numpyro jax`
- **Source:** https://www.pymc.io/ · https://num.pyro.ai/

### Prophet (skill: `forecasting-prophet-darts-neural`)

- **When:** daily/weekly forecasting with seasonality + holidays; easy default.
- **Install:** `cli-anything` → `pip install prophet`
- **Source:** https://facebook.github.io/prophet/

### Darts (skill: `forecasting-prophet-darts-neural`)

- **When:** unified forecasting API; advanced models (NBEATS, NHiTS, TFT, Transformer).
- **Install:** `cli-anything` → `pip install darts`
- **Source:** https://unit8co.github.io/darts/

### skforecast (skill: `forecasting-prophet-darts-neural`)

- **When:** use scikit-learn regressors as forecasters with autoregressive features.
- **Install:** `cli-anything` → `pip install skforecast`
- **Source:** https://skforecast.org/

### DoWhy (skill: `causal-inference-dag-iv-rdd`)

- **When:** DAG-based causal identification + estimation + sensitivity analysis.
- **Install:** `cli-anything` → `pip install dowhy`
- **Source:** https://www.pywhy.org/dowhy/

### linearmodels (skill: `causal-inference-dag-iv-rdd`)

- **When:** 2SLS instrumental variables, Panel OLS for diff-in-diff.
- **Install:** `cli-anything` → `pip install linearmodels`
- **Source:** https://bashtage.github.io/linearmodels/

### CausalImpact (skill: `causal-inference-dag-iv-rdd`)

- **When:** synthetic control on time-series; "what would have happened without intervention?"
- **Install:** `cli-anything` → `pip install pycausalimpact` (Google Python port)
- **Source:** https://google.github.io/CausalImpact/

### EconML (skill: `causal-inference-dag-iv-rdd`)

- **When:** heterogeneous treatment effects, double ML, orthogonal random forests.
- **Install:** `cli-anything` → `pip install econml`
- **Source:** https://econml.azurewebsites.net/

### PyOD (skill: `anomaly-detection-statistical-ml`)

- **When:** 40+ outlier detection algorithms (Isolation Forest, AutoEncoder, ABOD, etc.).
- **Install:** `cli-anything` → `pip install pyod`
- **Source:** https://pyod.readthedocs.io/

### ADTK (skill: `anomaly-detection-statistical-ml`)

- **When:** time-series anomaly detection (Threshold / Quantile / IQR / generalized ESD detectors).
- **Install:** `cli-anything` → `pip install adtk`
- **Source:** https://adtk.readthedocs.io/

### Great Expectations (skill: `great-expectations-soda-data-quality`)

- **When:** declarative data quality expectations + Data Docs HTML; CI integration.
- **Install:** `cli-anything` → `pip install great_expectations`
- **Source:** https://docs.greatexpectations.io/

### Soda Core (skill: `great-expectations-soda-data-quality`)

- **When:** SodaCL YAML checks runnable in CI (lighter than Great Expectations).
- **Install:** `cli-anything` → `pip install soda-core-<warehouse>`
- **Source:** https://docs.soda.io/

### Google Meridian (skill: `attribution-multi-touch-mmm`)

- **When:** current SOTA Bayesian MMM (NumPyro/JAX backend).
- **Install:** Follow https://github.com/google/meridian install
- **Source:** https://developers.google.com/meridian

### lightweight_mmm (skill: `attribution-multi-touch-mmm`)

- **When:** Google's earlier MMM library; smaller datasets, simpler API.
- **Install:** `cli-anything` → `pip install lightweight_mmm`
- **Source:** https://github.com/google/lightweight_mmm

### Statsig / GrowthBook / Eppo (skill: `ab-test-significance-mde-sequential` companion)

- **When:** experimentation platform with feature flags + sequential testing + multi-variant analysis.
- **GrowthBook (OSS):** `cli-anything` → `pip install growthbook` + Cloud or self-host
- **Statsig API:** `cli-anything` → `curl -H "STATSIG-API-KEY: $KEY" https://api.statsig.com/console/v1/...`
- **Source:** https://docs.growthbook.io/ · https://docs.statsig.com/ · https://docs.geteppo.com/

### Census / Hightouch (skill: `reverse-etl-census-hightouch`)

- **When:** managed reverse ETL (warehouse → Salesforce / HubSpot / Marketo / Iterable / Segment).
- **Install:** UI-configured; trigger via `cli-anything` → `curl -X POST https://api.getcensus.com/api/v1/syncs/{id}/trigger`
- **Source:** https://docs.getcensus.com/ · https://hightouch.com/docs/

### dlt (skill: `dlt-fivetran-airbyte-elt`)

- **When:** code-first Python ELT; modern OSS alternative to Fivetran/Airbyte; custom connectors easy.
- **Install:** `cli-anything` → `pip install dlt`
- **Source:** https://dlthub.com/docs/

### Airbyte (skill: `dlt-fivetran-airbyte-elt`)

- **When:** OSS ELT with 300+ connectors; self-host or Cloud.
- **Install:** self-host: `airbyte-platform` repo; Cloud via UI; API via `curl`
- **Source:** https://docs.airbyte.com/

### Hex (skill: `hex-notebooks-apps`)

- **When:** cloud-collaborative SQL + Python notebooks deployed as apps.
- **Install:** SaaS — UI-driven; API for programmatic project runs
- **Source:** https://hex.tech/docs/

### Metabase (skill: `metabase-self-serve-dashboards`)

- **When:** OSS self-serve BI; easy self-host; signed-JWT embedded analytics.
- **Install:** Docker / JAR self-host; or Metabase Cloud
- **Source:** https://www.metabase.com/docs/

### Looker / LookML (skill: `looker-lookml-modeling`)

- **When:** enterprise BI with governed metrics layer; LookML for views + explores + measures.
- **Install:** Google Cloud SaaS
- **Source:** https://cloud.google.com/looker/docs

### Lightdash (skill: `looker-lookml-modeling` companion)

- **When:** OSS Looker-alike on top of dbt; no separate semantic layer needed.
- **Install:** `cli-anything` → `npx lightdash deploy` after Lightdash Cloud or self-host
- **Source:** https://docs.lightdash.com/

### Evidence.dev (skill: `evidence-streamlit-marimo-reports`)

- **When:** markdown + SQL + Plotly → static HTML reports; version-controlled, code-first.
- **Install:** `cli-anything` → `npx degit evidence-dev/template my-project` + `npm i` + `evidence dev`
- **Source:** https://docs.evidence.dev/

### Marimo (skill: `evidence-streamlit-marimo-reports`)

- **When:** reactive notebooks with no hidden state, git-friendly, deployable as apps.
- **Install:** `cli-anything` → `pip install marimo` + `marimo edit notebook.py`
- **Source:** https://docs.marimo.io/

### Streamlit (skill: `evidence-streamlit-marimo-reports`)

- **When:** quick Python-only data apps.
- **Install:** `cli-anything` → `pip install streamlit` + `streamlit run app.py`
- **Source:** https://docs.streamlit.io/

### Quarto

- **When:** academic-grade reproducible reports (LaTeX-quality output).
- **Install:** `cli-anything` → `quarto render report.qmd --to pdf`
- **Source:** https://quarto.org/

### Plotly + Altair (skill: `data-storytelling-analytics-narrative`)

- **When:** chart production for deliverables. Plotly = interactive HTML; Altair = declarative grammar.
- **Install:** `cli-anything` → `pip install plotly altair matplotlib seaborn kaleido`
- **Source:** https://plotly.com/python/ · https://altair-viz.github.io/

### PostHog (skill: `cohort-retention-deep-survival` companion)

- **When:** product-analytics cohort fetch; HogQL queries; funnel API.
- **MCP:** `posthog-mcp`
- **Source:** https://posthog.com/docs/

### Mixpanel / Amplitude

- **When:** alt product analytics + behavioral cohorts (when org standardized on these).
- **MCP:** `mixpanel-mcp`, `amplitude-mcp`
- **Source:** https://developer.mixpanel.com/ · https://amplitude.com/docs

### Pandoc (default `markdown-converter` + analytics-narrative skill)

- **When:** markdown → DOCX / PDF / HTML / PPTX for branded deliverables.
- **Install:** `cli-anything` → `pandoc report.md -o report.docx --reference-doc=template.docx`
- **Source:** https://pandoc.org/MANUAL.html

---

## SOTA execution playbook

Maps "user asks for X" → "first-stop skill pack."

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Write me a SQL query for X" | `dbt-modeling-staging-marts` + warehouse skill | Lint with sqlfluff before commit |
| "Refactor this dbt model" | `dbt-modeling-staging-marts` + `dbt-test-authoring-utils-expectations` | Materialization audit + tests |
| "Run cohort retention" | `cohort-retention-deep-survival` | KM curve + log-rank for cohort compare |
| "Is this A/B test significant?" | `ab-test-significance-mde-sequential` | Always include effect size + CI |
| "Bayesian A/B" | `bayesian-pymc-numpyro-ab-testing` | Use Beta-Binomial for proportions |
| "Attribute conversions to channels" | `attribution-multi-touch-mmm` | Rule-based first, Markov for digital, MMM for offline |
| "Forecast next quarter" | `forecasting-prophet-darts-neural` | Prophet default; rolling-origin backtest |
| "Did campaign X cause Y?" | `causal-inference-dag-iv-rdd` | Demand a DAG before estimating |
| "Detect anomalies in this metric" | `anomaly-detection-statistical-ml` | Rolling threshold + PyOD/ADTK for multivariate |
| "Set up data quality checks" | `great-expectations-soda-data-quality` | Wire into dbt build / CI |
| "Sync warehouse → Salesforce" | `reverse-etl-census-hightouch` | Census/Hightouch; dlt for custom |
| "Ingest data from SaaS X" | `dlt-fivetran-airbyte-elt` | dlt for code-first; Airbyte for OSS managed |
| "Build me a Metabase dashboard" | `metabase-self-serve-dashboards` | 5-7 KPI rule, governed metrics |
| "Looker model for X" | `looker-lookml-modeling` | LookML; explore + view + measure |
| "Hex notebook for X" | `hex-notebooks-apps` | Magic SQL + Python + chart cells |
| "Optimize Snowflake credits" | `warehouse-cost-optimization-snowflake-bq` | QUERY_HISTORY analysis + materialization audit |
| "Segment customers" | `customer-segmentation-rfm-behavioral-ml` | RFM for quick; k-means/HDBSCAN for ML |
| "Survival analysis for churn" | `cohort-retention-deep-survival` | lifelines KM + Cox PH |
| "Power / sample size" | `ab-test-significance-mde-sequential` | statsmodels.stats.power before experiment |
| "Generate executive analytics report" | `evidence-streamlit-marimo-reports` + `data-storytelling-analytics-narrative` | Pandoc to DOCX/PDF; markdown source committable |

---

## Closing rules

The query is the artifact — version it, comment it, parameterize it. Correlation isn't causation — name your assumptions. Data quality is upstream — fix the pipeline, not the dashboard.

A number you can't reproduce is rumor. A model you can't interpret is theater. A dashboard nobody acts on is overhead. When in doubt, return to soul.md.
