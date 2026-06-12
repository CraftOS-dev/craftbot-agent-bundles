# Data Analyst — Source Attribution

Section-to-source map for `soul.md` and `role.md`. This file is part of the bundle but is **not** loaded into context — it exists for human verification and future refreshes.

For per-use-case SOTA mapping with confidence flags, see `reference/SOTA_USE_CASES.md`. For the master inventory of references, see `reference/INVENTORY.md`.

---

## soul.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Opening identity + load-bearing convictions | composition synthesis; the three convictions ("query is the artifact" / "correlation is not causation" / "data quality is upstream") are standard analytics-engineering principles, codified in dbt Labs best practices + Knaflic + Pearl | |
| "You are the depth specialist under research-analyst" | sibling-agent framing from CraftBot agent catalog; mirrors how `senior-python-engineer` sits below `engineer-agent` (not implemented but referenced) | |
| Purpose | composition synthesis across dbt Labs analytics-engineering guide + storytelling-with-data + standard data-analyst job descriptions in 2026 | |
| Execution stack | `reference/SOTA_USE_CASES.md` — one bullet per skill pack, mapped 1:1 to bundled list in agent.yaml | |
| When invoked — Ad-hoc SQL / dbt mode | dbt Labs project structure guide (https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview) | |
| When invoked — A/B test mode | scipy.stats + statsmodels.stats.power docs + Kohavi/Tang/Xu "Trustworthy Online Controlled Experiments" (2020) for sequential testing + CUPED | |
| When invoked — Cohort retention mode | lifelines docs + VoltAgent cohort-analysis subagent (parent agent inherits this) + Andrew Chen's "Aha Moment" framing | |
| When invoked — Attribution / MMM mode | Google Meridian docs + lightweight_mmm README + Meta Robyn project | |
| When invoked — Forecasting mode | Prophet docs + Hyndman & Athanasopoulos "Forecasting: Principles and Practice" (free online) + Darts docs | |
| When invoked — Causal inference mode | DoWhy docs + Pearl "Causality" + Angrist & Pischke "Mostly Harmless Econometrics" + Imbens & Rubin (2015) | |
| When invoked — Anomaly detection + data quality mode | Great Expectations + Soda docs + PyOD/ADTK docs | |
| When invoked — Dashboard / report mode | dbt MetricFlow docs + LookML docs + Knaflic + KPI framework patterns from wshobson business-analyst | |
| When invoked — Reverse ETL / ELT mode | Census + Hightouch + dlt docs | |
| When invoked — Warehouse cost mode | Snowflake QUERY_HISTORY docs + BigQuery INFORMATION_SCHEMA.JOBS_BY_PROJECT docs + Databricks Query Profile | |
| Core operating rules | composition synthesis from: "the query is the artifact" (dbt), "correlation is not causation" (Pearl), "data quality is upstream" (Great Expectations), Kohavi on A/B sequential, Imbens on causal | |
| Mode-specific decisions | per-mode best practices from the tool docs listed above | |
| Quality gates | composition synthesis from dbt project standards + statistical-reporting best practices (Wasserstein & Lazar 2016 ASA p-value statement) | |
| Output format | composition synthesis from data-storytelling skill pack (already in research-analyst) + standard analytics deliverable patterns | |
| Communication style | Knaflic ("Storytelling with Data") + standard scientific writing conventions for stats reporting | |
| When to push back | composition synthesis: ASA p-value statement on multiple comparisons + dbt test discipline + causal inference assumption discipline | |
| When to defer | sibling-agent hand-off conventions: `research-analyst` (parent), `product-manager` (analytics consumer), `senior-python-engineer` (pipeline eng), `devops-engineer` (warehouse infra), `marketing-agent` (creative) | |
| PROACTIVE self-init footer | standard PROACTIVE.md pattern (per METHODOLOGY.md); questions tailored to analytics work (warehouse, BI tool, top question) | per build instructions |
| Closing rule | restates the three convictions verbatim from the intro | |

---

## role.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Capability reference → Warehouses supported | composition synthesis from per-warehouse vendor docs (Snowflake, BigQuery, Databricks, Redshift, ClickHouse, DuckDB, MotherDuck, Firebolt, StarRocks) | |
| Capability reference → Dataframe libraries | composition synthesis from Polars + pandas + Ibis + Vaex + Dask + Modin docs | |
| Capability reference → BI / dashboard / notebook tools | composition synthesis from per-tool vendor docs (Hex, Metabase, Looker, Lightdash, Sigma, Mode, Superset, Redash, Evidence.dev, Observable, Streamlit, Dash, Marimo, Quarto) | |
| Capability reference → Visualization libraries | composition synthesis from Plotly + Altair + matplotlib + Bokeh + Datawrapper + Flourish docs | |
| Capability reference → Statistical / ML libraries | composition synthesis from statsmodels + scipy.stats + pingouin + lifelines + PyMC + scikit-learn + xgboost + Prophet + Darts + skforecast + pmdarima + DoWhy + EconML + linearmodels + CausalImpact + PyOD + ADTK + lifetimes docs | |
| Capability reference → Experimentation platforms | composition synthesis from Statsig + GrowthBook + Eppo + Optimizely + LaunchDarkly + Convert docs | |
| Capability reference → Data quality / observability | composition synthesis from Great Expectations + Soda + dbt tests + Monte Carlo + Bigeye + Acceldata + Sifflet + DataHub + Amundsen docs | |
| Capability reference → ELT / pipeline tools | composition synthesis from Fivetran + Airbyte + Stitch + Hevo + dlt docs | |
| Capability reference → Reverse-ETL tools | composition synthesis from Census + Hightouch + Polytomic + Rudderstack + dlt docs | |
| Capability reference → Catalog / discovery | composition synthesis from Atlan + DataHub + Amundsen + Select Star + OpenMetadata docs | |
| Capability reference → Transformation tooling | composition synthesis from dbt + SQLMesh + Coalesce + Sqlfluff + Sqlglot docs | |
| Warehouse dialect cheat sheet | per-warehouse SQL reference docs (window functions, array agg, date diff, generate series, median, pivot syntax) | |
| dbt project structure playbook | dbt Labs "How we structure our dbt projects" guide (https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview) + materialization decision tree from dbt docs | |
| dbt test catalog | dbt Labs data tests docs (https://docs.getdbt.com/docs/build/data-tests) + dbt-expectations README + dbt-utils README | |
| SQL refactor playbook | Sqlfluff docs + Sqlglot docs + general warehouse query optimization principles | |
| Cohort retention playbook | lifelines docs + VoltAgent cohort-analysis subagent (inherits from research-analyst) + Andrew Chen Aha Moment framing | |
| A/B test playbook | scipy.stats + statsmodels.stats.power + statsmodels.stats.proportion + Kohavi/Tang/Xu (2020) + Howard et al. (2021) "Time-uniform, nonparametric, nonasymptotic confidence sequences" for sequential | |
| Bayesian A/B playbook | PyMC docs + NumPyro docs + Beta-Binomial conjugate (standard Bayesian textbook) | |
| Attribution playbook | Google Meridian docs + lightweight_mmm README + Meta Robyn project + standard MMM literature (Hill function, adstock) | |
| Forecasting playbook | Prophet docs + statsmodels.tsa + Darts docs + skforecast docs + Hyndman & Athanasopoulos "Forecasting: Principles and Practice" | |
| Causal inference playbook | DoWhy docs + linearmodels docs + CausalImpact docs + EconML docs + Pearl "Causality" + Angrist & Pischke | |
| Anomaly detection playbook | PyOD docs + ADTK docs + Prophet anomaly detection docs + STL decomposition | |
| Data quality playbook | Great Expectations docs + Soda Core docs + dbt tests + dbt-expectations | |
| Reverse ETL playbook | Census docs + Hightouch docs + dlt docs | |
| ELT design playbook | Fivetran docs + Airbyte docs + dlt docs + standard ELT pattern (raw → staging → mart) | |
| Dashboard design playbook | per-BI-tool docs + Knaflic + KPI framework (3-tier, 5-7 limit) | |
| Warehouse cost playbook | Snowflake QUERY_HISTORY docs + BigQuery JOBS_BY_PROJECT docs + Databricks Query Profile docs | |
| Customer segmentation playbook | scikit-learn clustering docs + RFM classical framework + hdbscan docs | |
| Statistical rigor checklist | composition synthesis from ASA p-value statement (2016) + standard reporting standards (Wasserstein & Lazar) | |
| Report templates | composition synthesis from analytics-engineering best practices + Knaflic | |
| SOTA tool reference | `reference/SOTA_USE_CASES.md` + per-tool vendor documentation | per build instructions |
| SOTA execution playbook | maps user requests → first-stop skill pack; synthesized from the use cases in `USE_CASES.md` | |

---

## Notes on "authored from synthesis"

This is a v1 build pass — reference agents were not downloaded individually. The mapping above relies on per-tool vendor documentation (which is highly authoritative and rarely contested) plus composition synthesis where multiple sources combine. The next refresh should pull the following into `reference/agents/`:

- `wshobson/agents/business-analytics/agents/business-analyst.md` — already informs `research-analyst`; sibling
- VoltAgent `quantitative-analyst.md` — finance-specific overlap
- VoltAgent `experimentation-analyst.md` — substantive overlap with this agent's A/B mode (when published)
- VoltAgent `data-engineer.md` — adjacent for ELT design
- msitarzewski `data-analyst.md` — when published
- dbt Labs official "data analyst persona" docs — distributed across multiple guides; pull into one file

Once those exist in `reference/agents/`, audit this SOURCES.md to upgrade specific entries from "composition synthesis" to direct attribution.

---

## How to update this agent

1. Re-fetch source URLs listed below (per-tool vendor docs) — overwrite `reference/agents/*` and `reference/skills/*` once Round 2 downloads them
2. Diff against previous versions to see what changed (new SOTA tools, deprecated APIs, model upgrades)
3. Update corresponding sections of `soul.md` and `role.md`
4. Update this `SOURCES.md` if section names or source URLs changed
5. Run `python verify.py data-analyst` then `python build.py data-analyst` to regenerate `dist/data-analyst.craftbot`

---

## SOTA tool sources (June 2026)

Source map for the SOTA-tool reference section in `role.md` and the bundled skill packs in `skills/` (Round 2). Per-use-case mapping with confidence flags lives in `reference/SOTA_USE_CASES.md`.

| Tool / API | Source URL | Skill pack(s) |
|---|---|---|
| dbt Core best practices | https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview | `dbt-modeling-staging-marts` |
| dbt data tests | https://docs.getdbt.com/docs/build/data-tests | `dbt-test-authoring-utils-expectations` |
| dbt-expectations | https://github.com/calogica/dbt-expectations | `dbt-test-authoring-utils-expectations` |
| dbt-utils | https://github.com/dbt-labs/dbt-utils | `dbt-test-authoring-utils-expectations` |
| dbt MetricFlow | https://docs.getdbt.com/docs/build/metricflow | `looker-lookml-modeling`, `metabase-self-serve-dashboards` |
| SQLMesh | https://sqlmesh.readthedocs.io/ | `dbt-modeling-staging-marts` (alt) |
| Sqlfluff | https://docs.sqlfluff.com/ | `dbt-modeling-staging-marts` |
| Sqlglot | https://sqlglot.com/sqlglot.html | `dbt-modeling-staging-marts`, `snowflake-bigquery-databricks-warehousing` |
| Snowflake SQL API | https://docs.snowflake.com/en/developer-guide/sql-api/ | `snowflake-bigquery-databricks-warehousing`, `warehouse-cost-optimization-snowflake-bq` |
| Snowflake QUERY_HISTORY | https://docs.snowflake.com/en/sql-reference/account-usage/query_history | `warehouse-cost-optimization-snowflake-bq` |
| BigQuery REST API | https://cloud.google.com/bigquery/docs/reference/rest | `snowflake-bigquery-databricks-warehousing` |
| BigQuery INFORMATION_SCHEMA | https://cloud.google.com/bigquery/docs/information-schema-jobs | `warehouse-cost-optimization-snowflake-bq` |
| Databricks SQL Connector | https://docs.databricks.com/sql/ | `snowflake-bigquery-databricks-warehousing` |
| DuckDB | https://duckdb.org/docs/ | `duckdb-motherduck-local-olap` |
| MotherDuck | https://motherduck.com/docs/ | `duckdb-motherduck-local-olap` |
| Polars | https://pola.rs/ · https://docs.pola.rs/ | `polars-pandas-modern-dataframes` |
| pandas 2.x | https://pandas.pydata.org/docs/ | `polars-pandas-modern-dataframes` |
| Ibis | https://ibis-project.org/ | `polars-pandas-modern-dataframes` |
| scipy.stats | https://docs.scipy.org/doc/scipy/reference/stats.html | `ab-test-significance-mde-sequential` |
| statsmodels | https://www.statsmodels.org/stable/ | `ab-test-significance-mde-sequential`, `forecasting-prophet-darts-neural` |
| statsmodels.stats.power | https://www.statsmodels.org/stable/stats.html#power-and-sample-size-calculations | `ab-test-significance-mde-sequential` |
| pingouin | https://pingouin-stats.org/ | `ab-test-significance-mde-sequential` |
| lifelines | https://lifelines.readthedocs.io/ | `cohort-retention-deep-survival` |
| lifetimes (BG/NBD) | https://github.com/CamDavidsonPilon/lifetimes | `cohort-retention-deep-survival` |
| PyMC | https://www.pymc.io/projects/docs/en/stable/learn.html | `bayesian-pymc-numpyro-ab-testing` |
| NumPyro | https://num.pyro.ai/ | `bayesian-pymc-numpyro-ab-testing` |
| Prophet (Meta) | https://facebook.github.io/prophet/ | `forecasting-prophet-darts-neural` |
| Darts (Unit8) | https://unit8co.github.io/darts/ | `forecasting-prophet-darts-neural` |
| skforecast | https://skforecast.org/ | `forecasting-prophet-darts-neural` |
| pmdarima | https://alkaline-ml.com/pmdarima/ | `forecasting-prophet-darts-neural` |
| DoWhy | https://www.pywhy.org/dowhy/ | `causal-inference-dag-iv-rdd` |
| linearmodels | https://bashtage.github.io/linearmodels/ | `causal-inference-dag-iv-rdd` |
| CausalImpact (Google Python port) | https://google.github.io/CausalImpact/ · https://pypi.org/project/pycausalimpact/ | `causal-inference-dag-iv-rdd` |
| EconML (Microsoft) | https://econml.azurewebsites.net/ | `causal-inference-dag-iv-rdd` |
| PyOD | https://pyod.readthedocs.io/ | `anomaly-detection-statistical-ml` |
| ADTK | https://adtk.readthedocs.io/ | `anomaly-detection-statistical-ml` |
| Great Expectations | https://docs.greatexpectations.io/ | `great-expectations-soda-data-quality` |
| Soda Core | https://docs.soda.io/soda-core/overview-main.html | `great-expectations-soda-data-quality` |
| Google Meridian (MMM) | https://developers.google.com/meridian · https://github.com/google/meridian | `attribution-multi-touch-mmm` |
| lightweight_mmm (Google) | https://github.com/google/lightweight_mmm | `attribution-multi-touch-mmm` |
| Meta Robyn (MMM, R) | https://github.com/facebookexperimental/Robyn | `attribution-multi-touch-mmm` |
| ChannelAttribution (R port to Python) | https://cran.r-project.org/web/packages/ChannelAttribution/ · `python-markovify` | `attribution-multi-touch-mmm` |
| Statsig | https://docs.statsig.com/ | `ab-test-significance-mde-sequential` |
| GrowthBook | https://docs.growthbook.io/ | `ab-test-significance-mde-sequential` |
| Eppo | https://docs.geteppo.com/ | `ab-test-significance-mde-sequential` |
| Hypothesis (engineering) | https://hypothesis.readthedocs.io/ | (not bundled; engineering-side) |
| Census reverse-ETL | https://docs.getcensus.com/ | `reverse-etl-census-hightouch` |
| Hightouch | https://hightouch.com/docs · https://hightouch.com/docs/syncs/api | `reverse-etl-census-hightouch` |
| Polytomic | https://docs.polytomic.com/ | `reverse-etl-census-hightouch` |
| Rudderstack (CDP) | https://www.rudderstack.com/docs/ | `reverse-etl-census-hightouch` |
| dlt (Data Load Tool) | https://dlthub.com/docs | `dlt-fivetran-airbyte-elt` |
| Airbyte | https://docs.airbyte.com/ · https://docs.airbyte.com/api-documentation | `dlt-fivetran-airbyte-elt` |
| Fivetran | https://fivetran.com/docs/rest-api | `dlt-fivetran-airbyte-elt` |
| Hex | https://hex.tech/docs/ | `hex-notebooks-apps` |
| Metabase | https://www.metabase.com/docs/ · https://www.metabase.com/docs/latest/api | `metabase-self-serve-dashboards` |
| Metabase signed embedding | https://www.metabase.com/docs/latest/embedding/signed-embedding | `metabase-self-serve-dashboards` |
| Looker / LookML | https://cloud.google.com/looker/docs · https://cloud.google.com/looker/docs/api-and-integration | `looker-lookml-modeling` |
| Lightdash | https://docs.lightdash.com/ | `looker-lookml-modeling` |
| Sigma Computing | https://help.sigmacomputing.com/docs | (not bundled; referenced in role.md) |
| Mode Analytics | https://mode.com/help | (not bundled; referenced in role.md) |
| Superset (Apache) | https://superset.apache.org/docs/ | (not bundled; referenced in role.md) |
| Evidence.dev | https://docs.evidence.dev/ | `evidence-streamlit-marimo-reports` |
| Marimo | https://docs.marimo.io/ | `evidence-streamlit-marimo-reports` |
| Streamlit | https://docs.streamlit.io/ | `evidence-streamlit-marimo-reports` |
| Plotly Dash | https://dash.plotly.com/ | `evidence-streamlit-marimo-reports` |
| Quarto | https://quarto.org/ | `evidence-streamlit-marimo-reports` |
| Plotly Python | https://plotly.com/python/ | `data-storytelling-analytics-narrative` |
| Altair | https://altair-viz.github.io/ | `data-storytelling-analytics-narrative` |
| matplotlib | https://matplotlib.org/ | `data-storytelling-analytics-narrative` |
| seaborn | https://seaborn.pydata.org/ | `data-storytelling-analytics-narrative` |
| kaleido (Plotly PNG export) | https://github.com/plotly/Kaleido | `data-storytelling-analytics-narrative` |
| Datawrapper API | https://developer.datawrapper.de/ | `data-storytelling-analytics-narrative` |
| Pandoc | https://pandoc.org/MANUAL.html | `data-storytelling-analytics-narrative` |
| PostHog HogQL + cohorts | https://posthog.com/docs/hogql · https://posthog.com/docs/api/cohorts | `cohort-retention-deep-survival` |
| Mixpanel API | https://developer.mixpanel.com/ | `cohort-retention-deep-survival` |
| Amplitude API | https://amplitude.com/docs/apis | `cohort-retention-deep-survival` |
| scikit-learn clustering | https://scikit-learn.org/stable/modules/clustering.html | `customer-segmentation-rfm-behavioral-ml` |
| HDBSCAN | https://hdbscan.readthedocs.io/ | `customer-segmentation-rfm-behavioral-ml` |
| Storytelling with Data (Knaflic) | https://www.storytellingwithdata.com/ | `data-storytelling-analytics-narrative` |
| ASA p-value statement | https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf | role.md statistical rigor checklist |
| Trustworthy Online Controlled Experiments (Kohavi/Tang/Xu) | https://experimentguide.com/ | `ab-test-significance-mde-sequential` |
| Forecasting: Principles and Practice (Hyndman & Athanasopoulos) | https://otexts.com/fpp3/ | `forecasting-prophet-darts-neural` |
| DoWhy methodology guide | https://www.pywhy.org/dowhy/v0.11.1/ | `causal-inference-dag-iv-rdd` |

### Bundled skill packs (`skills/`) — file map

(Round 2 will populate these folders with SKILL.md content; Round 1 reserves the names in `agent.yaml`.)

| Skill folder | Companion playbook in role.md |
|---|---|
| `dbt-modeling-staging-marts/` | dbt project structure playbook + SQL refactor playbook |
| `dbt-test-authoring-utils-expectations/` | dbt test catalog |
| `snowflake-bigquery-databricks-warehousing/` | Warehouse dialect cheat sheet + Warehouse cost playbook |
| `duckdb-motherduck-local-olap/` | Capability reference → Warehouses supported |
| `polars-pandas-modern-dataframes/` | Capability reference → Dataframe libraries |
| `hex-notebooks-apps/` | Dashboard design playbook |
| `metabase-self-serve-dashboards/` | Dashboard design playbook |
| `looker-lookml-modeling/` | Dashboard design playbook (governed metrics) |
| `evidence-streamlit-marimo-reports/` | Report templates |
| `ab-test-significance-mde-sequential/` | A/B test playbook |
| `cohort-retention-deep-survival/` | Cohort retention playbook |
| `attribution-multi-touch-mmm/` | Attribution playbook |
| `forecasting-prophet-darts-neural/` | Forecasting playbook |
| `causal-inference-dag-iv-rdd/` | Causal inference playbook |
| `bayesian-pymc-numpyro-ab-testing/` | Bayesian A/B playbook |
| `anomaly-detection-statistical-ml/` | Anomaly detection playbook |
| `great-expectations-soda-data-quality/` | Data quality playbook |
| `reverse-etl-census-hightouch/` | Reverse ETL playbook |
| `dlt-fivetran-airbyte-elt/` | ELT design playbook |
| `warehouse-cost-optimization-snowflake-bq/` | Warehouse cost playbook |
| `customer-segmentation-rfm-behavioral-ml/` | Customer segmentation playbook |
| `data-storytelling-analytics-narrative/` | Report templates + Communication style |

### Per-use-case mapping

See `reference/SOTA_USE_CASES.md` for per-use-case SOTA approach, agent execution path, source URL, and confidence flag (✓ / ⚠ / ✗) — required reading for understanding what the agent can and cannot fully automate today.
