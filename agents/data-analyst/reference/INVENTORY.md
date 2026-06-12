# data-analyst — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from the per-agent seed list (warehouse / dbt / BI / dataframe / stats / experimentation / ELT / reverse-ETL / data-quality stacks) supplied by the methodology owner, cross-checked against the adjacent `research-analyst` agent and the wshobson/voltagent reference catalogues.

This is the **depth specialist** under `research-analyst`. Where `research-analyst` is broad (market/competitive/trend/scientific/cohort), `data-analyst` is warehouse-grounded SQL/dbt/BI work — A/B test math, attribution, anomaly detection, statistical hypothesis testing, dashboard authoring, reverse ETL, data quality CI. Defer general-research questions back up to `research-analyst`.

For future tightening: pull 4-6 reference agents from wshobson/agents (`data-engineer`, `business-analyst`, `analytics-engineer`), VoltAgent/awesome-claude-code-subagents (`data-researcher`, `cohort-analysis`, `quant-analyst`, `experimentation-analyst`), msitarzewski/agency-agents into `reference/agents/`, and 6-10 reference skills into `reference/skills/`.

## Sibling agents in the CraftBot catalogue

- **`research-analyst`** — parent. Broader research not warehouse-grounded (literature reviews, market sizing from SEC, trend analysis, competitive intelligence). Hand-off direction: data-analyst → research-analyst when the question becomes about secondary research / general topic investigation.
- **`product-manager`** — analytics consumer. Asks for the question, not the SQL. Hand-off direction: pm → data-analyst when "design the metric" turns into "compute the metric / build the dashboard."
- **`senior-python-engineer`** — data pipeline engineering at scale. Hand-off direction: data-analyst → senior-python-engineer when the work is "write production ingestion / streaming infra" rather than "model + analyze."
- **`devops-engineer`** — warehouse infra ops. Hand-off direction: data-analyst → devops-engineer when the work is "provision the Snowflake account / manage IAM / configure dbt Cloud project" rather than "write models + tests."

## Sources considered but not downloaded (v1 pass)

| Source | Why deferred |
|---|---|
| wshobson `data-engineer` | Adjacent but engineering-leaning; data-analyst sits between analytics-engineer and analyst |
| VoltAgent `quantitative-analyst` | Finance-specific; not core for general analytics |
| VoltAgent `experimentation-analyst` | Substantive overlap with this agent's A/B mode; pull in v2 refresh |
| msitarzewski `data-privacy-officer` | Compliance-focused; orthogonal to analytics craft |
| dbt Labs official "data analyst" persona docs | Not aggregated into a single file; sourced via per-tool documentation URLs in `SOURCES.md` |

## SOTA tool sources (June 2026) — anchor URLs

Full per-tool URL list lives in `SOURCES.md`. Anchor sources for the highest-impact tools:

- dbt Core / dbt Cloud — https://docs.getdbt.com/
- SQLMesh — https://sqlmesh.readthedocs.io/
- Sqlfluff — https://docs.sqlfluff.com/
- Snowflake API — https://docs.snowflake.com/en/developer-guide/sql-api/
- BigQuery API — https://cloud.google.com/bigquery/docs/reference/rest
- Databricks SQL — https://docs.databricks.com/sql/index.html
- DuckDB / MotherDuck — https://duckdb.org/ · https://motherduck.com/
- Polars — https://pola.rs/
- Ibis — https://ibis-project.org/
- Hex — https://hex.tech/docs/
- Metabase — https://www.metabase.com/docs/
- Looker / LookML — https://cloud.google.com/looker/docs
- Lightdash — https://docs.lightdash.com/
- Evidence.dev — https://docs.evidence.dev/
- Marimo — https://docs.marimo.io/
- Streamlit — https://docs.streamlit.io/
- Plotly / Altair / matplotlib — https://plotly.com/python/ · https://altair-viz.github.io/
- statsmodels / scipy.stats / pingouin — https://www.statsmodels.org/ · https://docs.scipy.org/doc/scipy/reference/stats.html · https://pingouin-stats.org/
- PyMC / NumPyro — https://www.pymc.io/ · https://num.pyro.ai/
- lifelines (Kaplan-Meier / Cox) — https://lifelines.readthedocs.io/
- Prophet / Darts — https://facebook.github.io/prophet/ · https://unit8co.github.io/darts/
- Great Expectations / Soda Core — https://greatexpectations.io/ · https://docs.soda.io/
- dlt / Airbyte / Fivetran — https://dlthub.com/docs · https://docs.airbyte.com/ · https://fivetran.com/docs
- Census / Hightouch — https://docs.getcensus.com/ · https://hightouch.com/docs
- Statsig / GrowthBook — https://docs.statsig.com/ · https://docs.growthbook.io/
- PostHog / Mixpanel / Amplitude — https://posthog.com/docs · https://developer.mixpanel.com/ · https://amplitude.com/docs
