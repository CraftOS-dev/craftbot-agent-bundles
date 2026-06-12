<!--
Hex: https://hex.tech/docs/
Companion: role.md → "Dashboard design playbook → Hex"
-->

# Hex notebooks-as-apps

Build cloud-collaborative SQL + Python + chart notebooks in Hex, deploy them as parameterized apps for non-technical stakeholders, and automate runs via the Hex API. Useful when the deliverable needs interactivity beyond what Metabase/Looker dashboards offer but doesn't justify a full Streamlit/Plotly Dash build.

## When to use

- "Build an interactive cohort explorer the GTM team can self-serve"
- Analyst-authored data app with input controls, conditional cells, and rich charts
- Deliverable that needs both SQL (warehouse-connected) and Python (lifelines / scikit-learn) in one place
- Embedded analytics into another tool (Hex's iframe embedding)
- API-driven runs scheduled by Airflow / Dagster / dbt Cloud

Defer fixed BI dashboards to `metabase-self-serve-dashboards` / `looker-lookml-modeling`. Defer code-first markdown reports to `evidence-streamlit-marimo-reports`. Defer ad-hoc local notebooks to Marimo.

## Setup

```bash
# No CLI install — Hex is SaaS. UI at app.hex.tech.
# Workspaces are free up to 5 contributors; paid tier for production deployments.

# Auth for API calls
export HEX_API_TOKEN="..."           # generated under Settings → API
export HEX_WORKSPACE_ID="..."        # from URL path
export HEX_PROJECT_ID="..."          # project UUID from URL
```

Auth requirements:
- Hex API token (Settings → API tokens). Scopes: `read:project`, `run:project`, `read:run`.
- Warehouse connections configured per Hex workspace (Snowflake / BigQuery / Databricks / Postgres / Redshift / DuckDB).

## Hex project structure

```
Hex Project
├── Cells (mixed types, executed in DAG order)
│   ├── SQL cell        → queries warehouse, returns df named after cell
│   ├── Python cell     → reads prior dataframes, transforms
│   ├── Chart cell      → no-code chart on a dataframe
│   ├── Markdown cell   → narrative
│   ├── Input cell      → text / dropdown / date for app users
│   └── Display cell    → final outputs in app view
├── Schedule (optional cron)
├── Published app view (subset of cells shown to consumers)
└── Permissions (workspace + per-project ACL)
```

## Common recipes

### Recipe 1 — SQL cell with parameterized inputs

```sql
-- Cell name: orders_filtered (resulting DataFrame name)
-- Inputs above: start_date (Date), end_date (Date), region (Dropdown)

SELECT
    customer_id,
    order_date,
    amount_usd,
    region
FROM {{ ref_table }}              -- Jinja vars work in Hex SQL cells
WHERE order_date BETWEEN '{{ start_date }}' AND '{{ end_date }}'
  AND region = '{{ region }}'
```

Hex auto-creates a `DataFrame` named `orders_filtered` available to downstream cells.

### Recipe 2 — Python cell consuming SQL result

```python
# Cell name: cohort_summary
# Inputs: orders_filtered (from previous SQL cell)

import pandas as pd
from lifelines import KaplanMeierFitter

df = orders_filtered
df["days_to_churn"] = (pd.Timestamp.now().normalize() - df["order_date"]).dt.days
df["churned"] = df["days_to_churn"] > 60

kmf = KaplanMeierFitter()
kmf.fit(df["days_to_churn"], df["churned"], label=f"{region} cohort")

cohort_summary = pd.DataFrame({
    "days_active": [7, 14, 30, 60, 90],
    "survival_prob": [kmf.survival_function_at_times(d).iloc[0] for d in [7, 14, 30, 60, 90]],
})
```

### Recipe 3 — Magic SQL — chained dataframe queries

```sql
-- Magic SQL cell — uses dataframe SQL instead of warehouse
-- Source: orders_filtered (Python or SQL cell above)

SELECT
    DATE_TRUNC('week', order_date) AS week,
    region,
    SUM(amount_usd) AS revenue
FROM orders_filtered
GROUP BY 1, 2
```

This runs against an in-memory DuckDB instance — useful for slicing dataframes without re-querying the warehouse.

### Recipe 4 — Input cells (build the app interface)

In the Hex UI:
1. Add **Input cell** → choose type (Text / Dropdown / Date / Slider / Multi-select)
2. Set variable name, e.g. `region`
3. For dropdowns: bind options to a SQL/Python expression (`orders.region.unique()`)
4. Toggle "Required in app view" so app users can't skip it

Reference in downstream cells as `{{ region }}` (SQL) or `region` (Python).

### Recipe 5 — Chart cell (no-code Plotly)

In Hex UI:
1. Add **Chart cell**, choose source dataframe
2. Drag fields to x / y / color / facet
3. Switch chart type (line / bar / scatter / heatmap)
4. Adjust formatting → markdown title, axis labels, hover

Output is a Plotly figure also accessible programmatically as `<cell_name>_figure`.

### Recipe 6 — Display cell (publish to app view)

In Hex UI:
1. Right-click cell → "Show in app"
2. Open "App builder" panel — drag-arrange cells, hide intermediate steps
3. Click **Publish** → generate shareable app URL

### Recipe 7 — Trigger a Hex project run via API

```bash
# Start a run
curl -X POST \
  -H "Authorization: Bearer $HEX_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "inputParams": {"start_date": "2025-06-01", "end_date": "2025-06-30", "region": "EU"},
    "updateCache": true
  }' \
  "https://app.hex.tech/api/v1/projects/$HEX_PROJECT_ID/runs"

# Returns: {"runId":"...","runStatusUrl":"..."}

# Poll for status
curl -H "Authorization: Bearer $HEX_API_TOKEN" \
  "https://app.hex.tech/api/v1/projects/$HEX_PROJECT_ID/runs/<RUN_ID>"

# Retrieve published app URL (already-cached results)
curl -H "Authorization: Bearer $HEX_API_TOKEN" \
  "https://app.hex.tech/api/v1/projects/$HEX_PROJECT_ID/"
```

### Recipe 8 — Hex Python SDK

```python
import requests
import os

class HexClient:
    BASE = "https://app.hex.tech/api/v1"
    def __init__(self, token):
        self.headers = {"Authorization": f"Bearer {token}"}

    def run_project(self, project_id, input_params=None):
        r = requests.post(
            f"{self.BASE}/projects/{project_id}/runs",
            headers=self.headers,
            json={"inputParams": input_params or {}, "updateCache": True},
        )
        r.raise_for_status()
        return r.json()

    def get_run_status(self, project_id, run_id):
        r = requests.get(f"{self.BASE}/projects/{project_id}/runs/{run_id}",
                         headers=self.headers)
        return r.json()

client = HexClient(os.environ["HEX_API_TOKEN"])
run = client.run_project(os.environ["HEX_PROJECT_ID"],
                          {"region": "US", "start_date": "2025-06-01"})
print(run["runId"])
```

### Recipe 9 — Schedule + alerts

In Hex UI:
1. Project → Schedule → "Add schedule" → cron expression
2. Set notification channel (Slack / Email)
3. Choose: notify on success, failure, or both
4. Optional: alert when a computed metric crosses threshold (Notification cell)

### Recipe 10 — Embedded analytics

```html
<!-- Iframe embed (signed token from API) -->
<iframe
  src="https://app.hex.tech/embed/{HEX_WORKSPACE_ID}/hex/{HEX_PROJECT_ID}?embeddedSessionId={signed_jwt}"
  width="100%" height="800"
  frameborder="0">
</iframe>
```

Generate the signed JWT via Hex API; pass per-user filters via `inputParams`.

## Example end-to-end

**Goal:** Self-serve cohort retention explorer for the GTM team. They choose date range + region; app shows cohort table + Kaplan-Meier curve + Aha-moment lift.

1. Create Hex project; connect Snowflake warehouse.
2. Add Input cells: `start_date`, `end_date`, `region` (dropdown bound to `SELECT DISTINCT region FROM dim_customers`).
3. SQL cell `cohort_data`: parameterized query pulling cohort + event data.
4. Python cell `kmf_fit`: lifelines `KaplanMeierFitter().fit(...)`; outputs `survival_df`.
5. Python cell `aha_moments`: compute retention-lift for candidate behaviors; outputs ranked DataFrame.
6. Chart cells: cohort heatmap, KM curve with CI, aha-moment bar chart.
7. Markdown cell: narrative ("So what" section).
8. App builder: arrange cells; hide intermediate Python steps; publish.
9. Schedule: nightly run with default inputs, alert Slack if 30-day retention drops >5%.
10. Share app URL with GTM team; they self-serve via inputs.

## Edge cases / gotchas

- **Cell DAG order matters** — Hex re-runs cells when upstream inputs change. Don't write to warehouse from cells; side effects break idempotency.
- **DataFrame names = cell names** — cells must have unique names; renaming a cell breaks downstream references silently.
- **App view vs. notebook view** — published app hides cells marked "Don't show in app"; test the app view, not just the notebook.
- **Jinja in SQL** — only `{{ var }}` substitution is supported; complex Jinja logic (loops/macros) doesn't work. Use Python cells for dynamic SQL.
- **Magic SQL row limit** — defaults to ~50k rows for performance; for large dataframes use Python cells with proper warehouse queries.
- **Input validation** — date inputs accept any string; sanity-check in the first Python cell.
- **Concurrent run limits** — Hex caps concurrent runs per workspace tier; check Settings → Usage.
- **Warehouse credentials** — managed at workspace level; analyst doesn't see passwords. Service-account governance applies.
- **API token scopes** — generate one token per integration (Airflow, dbt Cloud). Revoke via UI.
- **Outputs caching** — `updateCache: true` forces re-run; without it, embedded apps may show stale data. Set per-project staleness policy.
- **Hex pricing** — free for personal/<5 users; "Apps" feature is paid tier. Confirm before recommending to enterprise.

## Sources

- [Hex documentation](https://learn.hex.tech/docs)
- [Hex API reference](https://learn.hex.tech/docs/api/api-reference)
- [Hex magic SQL cells](https://learn.hex.tech/docs/explore-data/cells/sql-cells/sql-cells-introduction)
- [Hex apps and dashboards](https://learn.hex.tech/docs/share-insights/apps/app-builder)
- [Hex embedded analytics](https://learn.hex.tech/docs/share-insights/embedded-analytics/overview)
- [Hex changelog 2025](https://learn.hex.tech/changelog)
- role.md → "Dashboard design playbook"
