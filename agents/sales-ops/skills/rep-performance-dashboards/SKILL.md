<!--
Source: https://developer.salesforce.com/docs/atlas.en-us.bi_dev_guide_rest.meta/bi_dev_guide_rest/ + https://docs.looker.com/reference/api-and-integration
Rep performance dashboards — Salesforce CRMA + Looker + Sigma + Hex (June 2026 SOTA).
-->
# Rep Performance Dashboards — Salesforce CRMA + Looker + Sigma + Hex — SKILL

Per-AE + per-SDR + per-team dashboards. Salesforce CRMA (Tableau CRM / Einstein Analytics) for native dashboards. **Looker** for enterprise. **Sigma** for spreadsheet-native. **Hex** for notebook + dashboard hybrid. Pipeline created, demos run, opps advanced, win rate, average deal size, sales cycle, commit accuracy, quota attainment.

## When to use

- **Build an AE scorecard dashboard** — pipeline, conversion, attainment.
- **SDR activity dashboard** — calls, emails, meetings, SQL acceptance rate.
- **Team rollup** — segment + region + tier view.
- **CRMA dataset deploy** — refresh data + new dashboards.
- **Looker LookML** — explore + view + dashboard.
- **Sigma or Hex notebook** — interactive analysis.
- **Trigger phrases**: "rep scorecard", "AE dashboard", "SDR activity", "quota attainment dashboard", "CRMA dataset", "LookML", "Sigma", "Hex notebook".

Do NOT use this skill for: **pipeline metrics methodology** (use `pipeline-metrics-velocity-conversion`); **forecasting** (use `forecasting-clari-boostup-aviso`); **ramp analysis** (use `ramp-to-quota-analysis`); **win/loss reporting** (use `win-loss-reporting-at-scale`).

## Setup

```bash
# Salesforce CRMA — standard SF auth + sf wave plugin
sf plugins install analytics
sf org login web --alias prod

# Looker — SDK4 API
export LOOKER_BASE="https://your-co.looker.com:19999/api/4.0"
export LOOKER_CLIENT_ID="<id>"
export LOOKER_CLIENT_SECRET="<secret>"

# Sigma — API key
export SIGMA_TOKEN="<token>"
export SIGMA_BASE="https://api.sigmacomputing.com/v2"

# Hex — API token
export HEX_TOKEN="<token>"
export HEX_BASE="https://app.hex.tech/api/v1"

# Warehouse
export PG_URI="postgresql://..."
```

Required:
- Salesforce CRMA: $75-150/user/mo
- Looker: enterprise (~$3K+/user/yr)
- Sigma: ~$30-120/user/mo
- Hex: ~$30-90/user/mo

## Common recipes

### Recipe 1: Dashboard inventory (canonical)

```yaml
ae_scorecard:
  audience: AE + their manager
  refresh: daily
  metrics:
    - pipeline_created_qtd (target: > 3× quota)
    - demos_run_qtd
    - opps_advanced_qtd
    - win_rate_ttm (target: > 25%)
    - avg_deal_size_ttm
    - avg_cycle_days_ttm (target: < 60d enterprise; < 30d MM)
    - commit_accuracy_last_4q
    - quota_attainment_qtd (color: green > 90%, yellow 70-90%, red < 70%)

sdr_scorecard:
  audience: SDR + their manager
  refresh: daily
  metrics:
    - outbound_touches_per_day
    - qualified_meetings_booked_qtd
    - sql_acceptance_rate
    - meeting_show_rate
    - sql_to_opp_conversion
    - opps_sourced_qtd

team_rollup:
  audience: VP Sales + CRO
  refresh: weekly
  metrics:
    - team_quota_attainment_qtd (by segment + region)
    - top_5_deals_in_play
    - pipeline_coverage_ratio (target: 3-4×)
    - team_win_rate_ttm
    - team_avg_cycle_days
```

### Recipe 2: Salesforce CRMA dataset deploy

```bash
# Step 1: Create dataset from SOQL
sf wave dataset create --target-org prod \
  --name "Opportunity_Velocity_2026Q3" \
  --label "Opportunity Velocity Q3 2026" \
  --app "SalesOps_App"

# Step 2: Upload data (via external CSV or SAQL ETL)
sf wave dataset upload --target-org prod \
  --name "Opportunity_Velocity_2026Q3" \
  --file q3_velocity.csv

# Step 3: Create dashboard from JSON spec
sf wave dashboard create --target-org prod \
  --definition-file pipeline_velocity_dashboard.json
```

Dataset JSON spec:
```json
{
  "name": "Opportunity_Velocity_2026Q3",
  "label": "Opportunity Velocity Q3 2026",
  "type": "dataset",
  "files": [{
    "data": "q3_velocity.csv",
    "metadata": {
      "fileFormat": {
        "charsetName": "UTF-8",
        "fieldsDelimitedBy": ","
      },
      "objects": [{
        "name": "Velocity",
        "fields": [
          {"name": "OpportunityId", "type": "Text"},
          {"name": "OwnerName", "type": "Text"},
          {"name": "Amount", "type": "Numeric", "scale": 2},
          {"name": "StageName", "type": "Text"},
          {"name": "CloseDate", "type": "Date"},
          {"name": "DaysInStage", "type": "Numeric"}
        ]
      }]
    }
  }]
}
```

### Recipe 3: Looker LookML model

```lookml
# models/sales.model.lkml
connection: "warehouse"
include: "/views/*.view"

explore: opportunity {
  join: account {
    sql_on: ${opportunity.account_id} = ${account.id} ;;
    relationship: many_to_one
  }
  join: user {
    sql_on: ${opportunity.owner_id} = ${user.id} ;;
    relationship: many_to_one
  }
}

# views/opportunity.view.lkml
view: opportunity {
  sql_table_name: fct_opportunities ;;

  dimension: id { primary_key: yes }
  dimension: stage_name {}
  dimension: amount { type: number }
  dimension_group: close_date { type: time }
  dimension: is_closed { type: yesno }
  dimension: is_won { type: yesno }

  measure: count { type: count }
  measure: pipeline_amount { type: sum
    sql: ${amount} ;;
    filters: [is_closed: "no"]
    value_format: "$#,##0" }
  measure: won_amount { type: sum
    sql: ${amount} ;;
    filters: [is_won: "yes"]
    value_format: "$#,##0" }
  measure: win_rate {
    type: number
    sql: SAFE_DIVIDE(
      COUNTIF(${is_won}),
      COUNTIF(${is_closed})
    ) ;;
    value_format: "0.0%"
  }
  measure: avg_cycle_days {
    type: average
    sql: DATE_DIFF(${close_date_date}, ${created_date_date}, DAY) ;;
    filters: [is_won: "yes"]
  }
}
```

### Recipe 4: Looker dashboard JSON

```json
{
  "title": "AE Performance Scorecard",
  "filters": [
    {"name": "ae_filter", "title": "Account Executive",
     "type": "field_filter", "model": "sales", "explore": "opportunity",
     "field": "user.full_name"}
  ],
  "elements": [
    {"title": "Pipeline Created QTD", "type": "single_value",
     "query": {"model": "sales", "explore": "opportunity",
               "fields": ["opportunity.pipeline_amount"],
               "filters": {"opportunity.created_date_date": "this quarter"}}},
    {"title": "Win Rate (TTM)", "type": "single_value",
     "query": {"model": "sales", "explore": "opportunity",
               "fields": ["opportunity.win_rate"],
               "filters": {"opportunity.close_date_date": "12 months"}}}
  ]
}
```

### Recipe 5: Create Looker dashboard via API

```python
import requests, os, json

# Auth
auth = requests.post(f"{os.environ['LOOKER_BASE']}/login",
                     data={"client_id": os.environ["LOOKER_CLIENT_ID"],
                           "client_secret": os.environ["LOOKER_CLIENT_SECRET"]}).json()
TOKEN = auth["access_token"]

dashboard_spec = json.load(open("ae_scorecard.json"))
r = requests.post(f"{os.environ['LOOKER_BASE']}/dashboards",
                  headers={"Authorization": f"Bearer {TOKEN}"},
                  json=dashboard_spec)
print(r.json())
```

### Recipe 6: Sigma workbook via API

```bash
# Sigma uses workbooks (spreadsheet-style) — programmatic deploy via JSON
curl -X POST "$SIGMA_BASE/workbooks" \
  -H "Authorization: Bearer $SIGMA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AE Scorecard 2026Q3",
    "folder_id": "fld_xyz789",
    "sources": [{
      "connection_id": "conn_warehouse",
      "table": "fct_opportunities"
    }],
    "elements": [
      {"type": "table", "name": "AE Performance",
       "columns": ["owner_name","pipeline_amount","won_amount","win_rate"],
       "filters": {"close_date": "this quarter"}}
    ]
  }'
```

### Recipe 7: Hex notebook project

```python
# Hex projects defined in code — Python cells + SQL cells
# Example: AE scorecard notebook

# SQL cell
"""
SELECT
  owner_name,
  SUM(amount) FILTER (WHERE is_closed = FALSE) AS pipeline,
  SUM(amount) FILTER (WHERE is_won) AS won,
  100.0 * COUNT(*) FILTER (WHERE is_won) / NULLIF(COUNT(*) FILTER (WHERE is_closed), 0) AS win_rate
FROM fct_opportunities
WHERE owner_id IN ({{ae_filter}})
GROUP BY owner_name
ORDER BY won DESC
"""

# Python cell — visualize
import plotly.express as px
fig = px.bar(df, x="owner_name", y="won", color="win_rate",
             color_continuous_scale="Viridis",
             title="AE Won Amount QTD")
fig.show()
```

Deploy via Hex API:
```bash
curl -X POST "$HEX_BASE/projects/<project_id>/runs" \
  -H "Authorization: Bearer $HEX_TOKEN"
```

### Recipe 8: Quota attainment with color coding (Google Sheets)

```python
# Cron-render to Sheets for AEs who don't use BI tool
import pandas as pd
import gspread
from gspread_formatting import CellFormat, Color, format_cell_range

df = pd.read_sql("""
SELECT u.full_name, u.quota_full_year,
       SUM(o.amount) FILTER (WHERE o.is_won) AS won_qtd,
       100.0 * SUM(o.amount) FILTER (WHERE o.is_won) / NULLIF(u.quota_full_year/4, 0) AS attainment_pct
FROM dim_users u
LEFT JOIN fct_opportunities o ON o.owner_id = u.user_id
  AND o.close_date >= DATE_TRUNC('quarter', NOW())
GROUP BY 1, 2
ORDER BY 4 DESC
""", os.environ['PG_URI'])

gc = gspread.service_account()
sh = gc.open("AE Attainment").worksheet("Q3 2026")
sh.update([df.columns.values.tolist()] + df.values.tolist())

# Color-code: green > 90, yellow 70-90, red < 70
for i, row in df.iterrows():
    pct = row['attainment_pct']
    if pct > 90:
        color = Color(0.7, 1.0, 0.7)  # green
    elif pct > 70:
        color = Color(1.0, 1.0, 0.7)  # yellow
    else:
        color = Color(1.0, 0.7, 0.7)  # red
    format_cell_range(sh, f"D{i+2}",
                      CellFormat(backgroundColor=color))
```

### Recipe 9: SDR activity dashboard query

```sql
SELECT
  u.full_name AS sdr,
  COUNT(*) FILTER (WHERE a.type = 'Call') AS calls,
  COUNT(*) FILTER (WHERE a.type = 'Email') AS emails,
  COUNT(*) FILTER (WHERE a.type = 'Meeting Booked') AS meetings_booked,
  COUNT(DISTINCT o.opportunity_id) FILTER (WHERE o.is_sql) AS sqls,
  COUNT(DISTINCT o.opportunity_id) FILTER (WHERE o.accepted_by_ae) AS sql_accepted,
  ROUND(100.0 * COUNT(DISTINCT o.opportunity_id) FILTER (WHERE o.accepted_by_ae) /
        NULLIF(COUNT(DISTINCT o.opportunity_id) FILTER (WHERE o.is_sql), 0), 1) AS acceptance_rate
FROM dim_users u
LEFT JOIN fct_activities a ON a.owner_id = u.user_id
  AND a.activity_date >= DATE_TRUNC('quarter', NOW())
LEFT JOIN fct_opportunities o ON o.sdr_id = u.user_id
  AND o.created_date >= DATE_TRUNC('quarter', NOW())
WHERE u.role = 'SDR'
GROUP BY 1
ORDER BY meetings_booked DESC;
```

### Recipe 10: CRMA dashboard JSON template (single-value widget)

```json
{
  "label": "AE Performance Scorecard",
  "state": {
    "widgets": [
      {
        "type": "number",
        "label": "Pipeline Created QTD",
        "step": "Pipeline_QTD",
        "compactNumber": true,
        "showTitle": true,
        "showSubtitle": true
      }
    ],
    "steps": {
      "Pipeline_QTD": {
        "datasets": [{"id": "Opportunity_Velocity_2026Q3"}],
        "query": "q = load \"Opportunity_Velocity_2026Q3\"; q = filter q by 'IsClosed' == \"false\"; q = group q by all; q = foreach q generate sum('Amount') as 'pipeline';",
        "type": "saql"
      }
    }
  }
}
```

### Recipe 11: Slack weekly digest

```python
# Friday: per-team digest
import requests, os
import pandas as pd

df = pd.read_sql("""
SELECT segment,
       SUM(amount) FILTER (WHERE is_won) AS won_qtd,
       SUM(quota_qtd) AS quota_qtd,
       100.0 * SUM(amount) FILTER (WHERE is_won) / NULLIF(SUM(quota_qtd), 0) AS attainment_pct
FROM fct_opportunities
JOIN dim_users ON owner_id = user_id
WHERE close_date >= DATE_TRUNC('quarter', NOW())
GROUP BY 1
""", os.environ['PG_URI'])

msg = "Team attainment digest (QTD):\n"
for _, row in df.iterrows():
    icon = "🟢" if row['attainment_pct'] > 90 else ("🟡" if row['attainment_pct'] > 70 else "🔴")
    msg += f"{icon} {row['segment']}: ${row['won_qtd']:,.0f} / ${row['quota_qtd']:,.0f} ({row['attainment_pct']:.0f}%)\n"

requests.post("https://slack.com/api/chat.postMessage",
              headers={"Authorization": f"Bearer {os.environ['SLACK_TOKEN']}"},
              json={"channel": "#sales-leadership", "text": msg})
```

### Recipe 12: Dashboard catalog (notion)

```yaml
# Maintained as notion database — every dashboard registered
- name: AE Scorecard 2026Q3
  platform: Looker
  url: https://co.looker.com/dashboards/123
  owner: SalesOps
  audience: AE + managers
  refresh: daily
  metrics: pipeline_created, win_rate, attainment, cycle_days
  source_of_truth: warehouse.fct_opportunities

- name: SDR Activity Q3
  platform: CRMA
  url: https://co.lightning.force.com/lightning/r/Dashboard/0FK...
  owner: SalesOps
  audience: SDR + managers
  refresh: hourly
  metrics: calls, emails, meetings, sql_acceptance
  source_of_truth: Salesforce native

# Quarterly: review catalog, retire orphans
```

## Examples

### Example 1: Deploy AE scorecard in CRMA

**Goal:** Native Salesforce dashboard for all AEs to check daily.

**Steps:**
1. Build SAQL query for pipeline, win rate, attainment.
2. Recipe 2 — create CRMA dataset from SOQL or external CSV.
3. Recipe 10 — define dashboard JSON spec.
4. Deploy via `sf wave dashboard create`.
5. Embed in Lightning home page (admin) — Setup → App Manager.
6. Recipe 12 — register in dashboard catalog.

**Result:** Every AE has live scorecard at login; no manual report-pulling.

### Example 2: Modernize to Looker for team rollup

**Goal:** VP Sales wants drill-down by segment + region + tier; CRMA too rigid.

**Steps:**
1. Set up Fivetran Salesforce → warehouse (Snowflake/BigQuery).
2. dbt-model `fct_opportunities` (see `pipeline-metrics-velocity-conversion`).
3. Recipe 3 — write LookML model.
4. Recipe 4 — define dashboard JSON.
5. Recipe 5 — deploy via Looker API.
6. Add embedded analytics to Salesforce home page via iframe.
7. Recipe 11 — Slack digest pulls from Looker queries.

**Result:** VP can slice attainment by any dimension; Excel exports out the back.

### Example 3: Sigma exploratory analysis

**Goal:** Sales analyst wants spreadsheet-style exploration of pipeline data.

**Steps:**
1. Connect Sigma to warehouse (Recipe 6).
2. Build workbook: load fct_opportunities, pivot by segment + stage + AE.
3. Add conditional formatting for attainment.
4. Schedule daily refresh.
5. Share workbook with analyst pod.

**Result:** Analyst self-serves; SalesOps unblocked from ad-hoc requests.

## Edge cases / gotchas

- **CRMA license cost** — $$$. Bundled in some Salesforce SKUs; verify before promising.
- **SAQL is its own language** — neither SQL nor SOQL. Learning curve.
- **Looker LookML is opinionated** — devs love it; analysts struggle.
- **Sigma performance on huge tables** — query optimization needed for > 100M rows.
- **Hex notebook collaboration** — multiple users editing same notebook → version conflicts.
- **CRMA dashboard refresh schedule** — dataflows can be slow (5-15 min); not instant.
- **Embedded analytics security** — make sure FLS enforced; AEs can't see other AEs' deals.
- **Color coding gotcha** — colorblind users; pair with icons or numbers.
- **Quota source-of-truth** — separate from CRM closed-won; commonly notion or Anaplan; sync nightly.
- **Multi-currency** — single-currency dashboards; convert at snapshot rate.
- **Dashboard sprawl** — quarterly catalog audit; retire unused.
- **Salesforce reports vs CRMA dashboards** — different beasts. Reports = ad-hoc. CRMA = curated.
- **dbt model drift** — model schema change breaks downstream LookML; Sigma; Hex.
- **Mobile rendering** — CRMA mobile lacks features; design desktop-first, verify mobile.
- **Embedded charts in Slack** — Looker's Slack integration nice; Sigma has it too.
- **Single source of truth** — multiple dashboards on same metric with different numbers = trust crisis.

## Sources

- [Salesforce CRMA REST API](https://developer.salesforce.com/docs/atlas.en-us.bi_dev_guide_rest.meta/bi_dev_guide_rest/)
- [Salesforce CRMA dataset deploy](https://developer.salesforce.com/docs/atlas.en-us.bi_dev_guide_dataset.meta/bi_dev_guide_dataset/)
- [SAQL Reference](https://developer.salesforce.com/docs/atlas.en-us.bi_dev_guide_saql.meta/bi_dev_guide_saql/)
- [Looker SDK4 API reference](https://docs.looker.com/reference/api-and-integration)
- [LookML overview](https://docs.looker.com/reference/lookml)
- [Sigma Computing API docs](https://help.sigmacomputing.com/reference)
- [Hex API reference](https://learn.hex.tech/docs/api)
- [dbt + Looker integration](https://docs.getdbt.com/blog/dbt-meets-looker)
