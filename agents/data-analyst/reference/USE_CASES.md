# Data Analyst — Use Cases

**Tier:** specialized · **Category:** analytics
**Core job:** Warehouse-grounded SQL + dbt + cohort analysis + A/B test math + attribution + anomaly detection + statistical hypothesis testing + dashboard authoring. Versions the query as the artifact, names assumptions when correlation might be mistaken for causation, and treats data quality as upstream.

This is the depth specialist under `research-analyst`. Where `research-analyst` is broad (market sizing, literature review, competitive intelligence, trend analysis), `data-analyst` is the one to call when the user has a warehouse and a question that needs SQL, dbt, dashboards, or statistical inference.

Ships with the SOTA analytics stack (dbt + Sqlfluff + Sqlglot + DuckDB + Polars + Ibis + lifelines + scipy/statsmodels/pingouin + PyMC + Prophet/Darts + DoWhy/linearmodels + PyOD/ADTK + Great Expectations + Soda + dlt + Census/Hightouch + Hex/Metabase/Looker/Lightdash/Evidence) — executes end-to-end, not just direct.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Warehouse SQL + dbt transformation
- Ad-hoc SQL writing + linting (sqlfluff) + transpilation across dialects (sqlglot)
- dbt model authoring (Kimball-style staging → intermediate → marts)
- dbt test authoring (`unique` / `not_null` / `accepted_values` / `relationships` / freshness / singular tests / dbt-utils / dbt-expectations)
- Materialization decisions (view / table / incremental / snapshot / ephemeral)
- SQL refactoring + performance tuning across Snowflake / BigQuery / Databricks / Redshift / ClickHouse / DuckDB / Postgres

### Dashboards + reporting tools
- Dashboard design across Hex, Metabase, Looker (LookML), Lightdash, Sigma Computing, Mode, Superset
- Notebook → report → app pipelines via Marimo / Streamlit / Plotly Dash / Evidence.dev / Quarto
- 5-7 KPI rule, 3-tier hierarchy (strategic / tactical / operational)
- Self-serve dashboard governance via dbt MetricFlow / Cube.dev / LookML

### Statistical analytics
- A/B test significance (Welch's t-test, z-test for proportions, Mann-Whitney U, Poisson exact)
- Sample size + MDE + power calculation (statsmodels.stats.power)
- Sequential testing (mSPRT, always-valid CIs) to avoid peeking penalty
- CUPED variance reduction
- Bayesian A/B testing (PyMC / NumPyro; Beta-Binomial closed-form for proportions)
- ANOVA + Tukey HSD for multi-arm experiments
- Multiple-comparisons correction (Bonferroni, Benjamini-Hochberg)
- Power analysis (Cohen's d / h / f effect sizes)

### Cohort + retention
- N-day, weekly, monthly, rolling retention metrics
- Kaplan-Meier survival curves (lifelines) with confidence intervals
- Log-rank test for cohort comparison
- Cox PH hazard regression with covariates
- Acquisition / behavioral / segment cohort taxonomy
- Activation analysis ("Aha Moment" identification)
- LTV calculation (cohort-based + survival-based + BG/NBD / Gamma-Gamma)

### Attribution + marketing analytics
- Last-touch / first-touch / linear / time-decay / position-based (rule-based via SQL)
- Data-driven attribution (Shapley value, Markov chain)
- Marketing Mix Modeling (Google Meridian, lightweight_mmm, Meta Robyn)
- Adstock + Hill saturation transforms
- Channel ROI + optimal spend allocation with uncertainty

### Forecasting + time series
- Prophet (seasonality + holidays + changepoints)
- ARIMA / SARIMA via statsmodels + pmdarima auto-order selection
- Darts unified API (Exponential Smoothing → NBEATS → NHiTS → TFT → Transformer)
- skforecast (scikit-learn regressors as forecasters)
- Time-series decomposition (additive, multiplicative, STL)
- Rolling-origin cross-validation backtesting

### Causal inference
- DAG-based causal identification (DoWhy)
- Instrumental variables (2SLS via linearmodels)
- Regression discontinuity design (RDD)
- Difference-in-differences (Panel OLS via linearmodels)
- Synthetic control (CausalImpact)
- Propensity score matching
- Sensitivity analysis (e-values, Rosenbaum bounds)
- Heterogeneous treatment effects (EconML, double ML)

### Anomaly detection
- Statistical (rolling z-score, MAD, ESD, Prophet residuals, STL residuals)
- ML-based (Isolation Forest, One-Class SVM, Autoencoder, HDBSCAN)
- Time-series (ADTK ThresholdAD, QuantileAD, InterQuartileRange)
- Univariate + multivariate (PyOD's 40+ algorithms)
- Dynamic thresholds vs static cutoffs

### Data quality
- Great Expectations declarative suites + Data Docs HTML
- Soda Core SodaCL YAML in CI
- dbt tests (generic + singular)
- dbt-expectations + dbt-utils
- CI integration (GitHub Actions, Airflow, Dagster)

### Data pipeline (ELT + Reverse ETL)
- ELT ingestion via dlt (Python OSS), Airbyte (OSS), Fivetran (managed), Stitch
- Reverse ETL via Census, Hightouch, Polytomic
- Custom dlt-based syncs

### Customer segmentation
- RFM (Recency / Frequency / Monetary) quintile via SQL NTILE
- Behavioral clustering (k-means, GMM, HDBSCAN)
- Silhouette + business-interpretability validation
- Segment retention + LTV comparison

### Warehouse cost + performance
- Snowflake credit attribution (QUERY_HISTORY)
- BigQuery slot / job analysis (INFORMATION_SCHEMA.JOBS_BY_PROJECT)
- Databricks Query Profile
- Partitioning + clustering + materialization audit
- Multi-cluster + auto-suspend tuning

### Modern dataframe + local compute
- Polars (Rust, lazy, multi-core)
- pandas 2.x with PyArrow backend
- Ibis (universal dataframe API)
- DuckDB SQL-on-Python
- Local Parquet over S3 workflows

### Analytics narrative + delivery
- Setup → Conflict → Resolution structure for reports
- "So what" first (Knaflic)
- Plotly / Altair / matplotlib / Datawrapper for charts
- Markdown → DOCX / PDF / PPTX via Pandoc
- Executive briefings + long-form reports + slide decks

### Experimentation platform integration
- Statsig (sequential testing, holdouts)
- GrowthBook (OSS, Bayesian + frequentist, dbt-integrated)
- Eppo (causal modeling for analyses)
- LaunchDarkly Galaxy / Optimizely

### Embedded analytics
- Metabase JWT signed embedding
- Looker SSO Embed SDK
- Cube.dev with signed JWT
- Custom Vega-Lite + warehouse-direct queries
- Row-level security enforcement

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case from the section above appears here as a row.

| Use case | SOTA mechanism | Path |
|---|---|---|
| Ad-hoc SQL writing + optimization | Sqlfluff + Sqlglot + warehouse SDK + DuckDB | `cli-anything` (`pip install sqlfluff sqlglot duckdb`) + `postgresql-mcp` |
| dbt model authoring | dbt Core + adapter (snowflake/bigquery/databricks/postgres/duckdb) | `cli-anything` (`dbt-core`) |
| dbt test authoring | dbt tests + dbt-utils + dbt-expectations | `cli-anything` (`dbt deps`) |
| Dashboard design (Hex/Metabase/Looker/Lightdash/Sigma) | Per-tool API or SDK | `cli-anything` per-platform |
| Cohort retention | SQL + lifelines KM + PostHog HogQL | warehouse + `posthog-mcp` + `cli-anything` (`lifelines`) |
| A/B significance + sample size + MDE | scipy.stats + statsmodels + pingouin + Statsig/GrowthBook | `cli-anything` + experimentation platform |
| Sequential testing (mSPRT, always-valid) | GrowthBook + Statsig native; custom mSPRT in Python | platform API + `cli-anything` |
| Bayesian A/B | PyMC + NumPyro + Beta-Binomial closed-form | `cli-anything` (`pymc numpyro`) |
| Attribution (rule-based) | SQL window functions in warehouse | warehouse SDK |
| Attribution (data-driven) | Shapley + Markov via `ChannelAttribution` / `python-markovify` | `cli-anything` |
| Marketing Mix Modeling | Google Meridian + lightweight_mmm + Meta Robyn | `cli-anything` (`lightweight_mmm`) |
| Funnel analysis | SQL + PostHog/Mixpanel/Amplitude funnel API | warehouse + product-analytics MCP |
| Activation (Aha Moment) | SQL + scipy delta significance | warehouse + `cli-anything` |
| Customer segmentation (RFM) | SQL NTILE | warehouse |
| Customer segmentation (ML) | scikit-learn KMeans + HDBSCAN | `cli-anything` (`scikit-learn hdbscan`) |
| LTV calculation | lifelines + lifetimes BG/NBD | `cli-anything` |
| Anomaly detection (statistical) | rolling z-score / MAD / Prophet residuals | `cli-anything` |
| Anomaly detection (ML) | PyOD + ADTK + IsolationForest | `cli-anything` |
| Data quality monitoring | Great Expectations + Soda Core + dbt tests | `cli-anything` |
| Reverse ETL | Census + Hightouch + Polytomic + dlt | `cli-anything` per-platform API |
| ELT pipeline | dlt + Airbyte + Fivetran | `cli-anything` (`dlt`) + managed APIs |
| Forecasting (classical) | Prophet + ARIMA / SARIMA + pmdarima auto | `cli-anything` |
| Forecasting (neural / advanced) | Darts NBEATS / NHiTS / TFT / Transformer | `cli-anything` (`darts`) |
| Causal inference (DAG / IV / RDD) | DoWhy + linearmodels + CausalImpact + EconML | `cli-anything` |
| Survival analysis | lifelines KM + Cox PH + Aalen | `cli-anything` |
| Time-series decomposition | statsmodels seasonal_decompose + STL + pmdarima | `cli-anything` |
| Statistical hypothesis testing | scipy.stats + pingouin + statsmodels | `cli-anything` |
| Power analysis / sample size | statsmodels.stats.power (T/Normal/F/Anova) | `cli-anything` |
| Data narrative / exec summary | Markdown + Pandoc + data-storytelling principles | `cli-anything` |
| Self-serve dashboard governance | dbt MetricFlow + LookML + Cube.dev | warehouse + dbt |
| SQL refactoring + perf tuning | Sqlfluff + Sqlglot + warehouse EXPLAIN | `cli-anything` + warehouse SDK |
| Warehouse cost optimization | QUERY_HISTORY + INFORMATION_SCHEMA + dbt mat audit | warehouse SDK + dbt |
| Notebook → report → dashboard | Marimo + Streamlit + Evidence.dev + Quarto | `cli-anything` |
| Embedded analytics | Metabase JWT / Looker SSO / Cube signed JWT | BI SDK + `cli-anything` |
| Polars / pandas 2.x / Ibis modern dataframes | Polars + Ibis + DuckDB Python | `cli-anything` (`polars ibis duckdb`) |
| Multilingual data narrative | DeepL MCP for translation | `deepl-mcp` |
| Scanned PDF data extraction | Mistral OCR / Gemini OCR | `mistral-ocr-mcp` / `gemini-ocr-mcp` |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| dbt model + test authoring | ⚠ | Requires warehouse credentials + dbt project; free fallback: dbt-duckdb against local DuckDB |
| Dashboard authoring (Hex / Metabase / Looker / Lightdash / Sigma) | ⚠ | Per-tool API key; free fallback: Lightdash + Metabase OSS self-host, or Evidence.dev (markdown reports, free) |
| Reverse ETL (Census / Hightouch / Polytomic) | ⚠ | Paid platform key; free fallback: dlt + direct SaaS API calls for one-off syncs |
| Self-serve dashboard governance | ⚠ | Requires warehouse + dbt; free fallback: dbt MetricFlow runnable locally against DuckDB |
| Warehouse cost optimization | ⚠ | Requires warehouse credentials; skill pack ships the queries, user runs against their account |
| Embedded analytics | ⚠ | Requires BI tool with embedding tier; free fallback: custom Vega-Lite + warehouse SDK |
| Statsig / Eppo experimentation platform | ⚠ | Paid platform key; free fallback: GrowthBook OSS or custom Python A/B with statsmodels |
| Fivetran managed ELT | ⚠ | Paid platform key; free fallback: dlt (OSS) or Airbyte (OSS) |

**Verdict (June 2026): ~97% fulfillment.** Every ⚠ row reduces to "user names their warehouse + BI tool + plat key, agent unblocks." No genuine capability gaps — the agent ships ready-to-execute Python / SQL / dbt / statistical workloads with `cli-anything`. The agent is fully autonomous on classical analytics (cohort retention, A/B math, attribution, forecasting, causal inference, anomaly detection, segmentation, statistical testing) — the only ⚠ work is plumbing into specific warehouse / BI accounts the recipient owns.

---

## When to use this agent

- "Write me the SQL for a cohort retention table by signup week"
- "Is this A/B test significant? Here's the data" (with sample size + effect direction)
- "Build a dbt model for customer LTV with tests"
- "Forecast next quarter's MRR with prediction intervals"
- "Did our campaign cause the lift, or is it seasonal? Run a causal analysis"
- "Detect anomalies in our DAU metric over the last 90 days"
- "Set up Great Expectations checks on the orders pipeline"
- "Build a Metabase dashboard for the marketing team"
- "Refactor this 400-line SQL — it's slow"
- "Run a Bayesian A/B on this conversion data"
- "Segment our customers via RFM and check segment retention"
- "Build a marketing mix model on our 24-month spend + revenue data"
- "Sync the warehouse customer-health-score back to Salesforce"
- "Sample-size calculation for a 2% MDE at 80% power"
- "What's eating our Snowflake credits this week?"

## When NOT to use this agent

- General topic research / market sizing / competitive intelligence / trend analysis — hand off to `research-analyst` (parent)
- "What metric should we track?" — hand off to `product-manager` (then come back to compute it)
- Production data pipeline engineering at scale (Kafka, streaming, microservices) — hand off to `senior-python-engineer`
- Warehouse infra provisioning, IAM, dbt Cloud setup, Airflow deployment — hand off to `devops-engineer`
- Marketing copy / customer-facing email / campaign creative — hand off to `marketing-agent`
- Insider trading / private financial data / regulatory-protected data — refuse; ethical methods only
- "Write the ML training pipeline for our recommender" — partial fit; defer ML system design to `senior-python-engineer`
