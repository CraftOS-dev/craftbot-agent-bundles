<!--
Looker: https://cloud.google.com/looker/docs
LookML reference: https://cloud.google.com/looker/docs/lookml-quick-reference
Lightdash (OSS alt): https://docs.lightdash.com/
Companion: role.md → "Dashboard design playbook → Looker / Lightdash"
-->

# Looker / LookML modeling (and Lightdash OSS alternative)

Author LookML — the governed metrics + dimensions layer that turns a warehouse into a self-serve analytics product. Build models, explores, views, measures, and dashboards; embed via SSO; manage with Git-versioned LookML. Lightdash is the OSS alternative that reads dbt metadata directly.

## When to use

- "Set up a governed metric layer" / "ensure everyone calculates revenue the same way"
- Enterprise BI with row-level security + permissioned data access
- Embedded analytics with SSO and per-tenant filtering
- Cross-team self-serve where finance/marketing/product all need the same KPI definitions
- Already on Google Cloud + want native warehouse integration

Defer Metabase-style ad-hoc to `metabase-self-serve-dashboards`. Defer notebook-style work to `hex-notebooks-apps`. Defer markdown reports to `evidence-streamlit-marimo-reports`.

## Setup

```bash
# Looker — managed SaaS on Google Cloud
# Provisioned via Google Cloud Console → Looker → Create instance
# CLI for managing LookML (formerly called LAMS)
gem install lookml-gen     # generation tool (one option)

# Looker SDK
pip install looker-sdk

# Lightdash (OSS alternative)
npm install -g @lightdash/cli
# Or self-host via Docker:
docker run -d -p 8080:8080 lightdash/lightdash:latest
```

Auth requirements:
- Looker: instance URL + API3 credentials (client_id + client_secret) generated under Admin → Users → API3 Keys.
- Lightdash: API key + project ID; for self-host, `LIGHTDASH_API_KEY` env var.
- dbt project (Lightdash reads dbt metadata).

## LookML core concepts

| Concept | LookML keyword | Maps to |
|---|---|---|
| Project | `manifest.lkml` | Git repo |
| Model | `model.lkml` | One per warehouse connection or domain |
| View | `view.lkml` | One per table (or derived table) |
| Explore | `explore:` in model | Join graph — what fields are joinable |
| Dimension | `dimension:` in view | Column or expression that groups |
| Measure | `measure:` in view | Aggregation (sum/count/avg/...) |
| Derived table | `derived_table:` in view | SQL CTE that becomes a virtual table |

## Common recipes

### Recipe 1 — Project + connection setup

In Looker UI:
1. Admin → Connections → New Connection
2. Provide warehouse credentials (Snowflake / BigQuery / etc.)
3. Develop → New LookML Project → choose Git repo

### Recipe 2 — A View

```lookml
# views/fct_orders.view.lkml

view: fct_orders {
  sql_table_name: marts.fct_orders ;;

  dimension: order_id {
    primary_key: yes
    type: string
    sql: ${TABLE}.order_id ;;
  }

  dimension: customer_id {
    type: string
    sql: ${TABLE}.customer_id ;;
  }

  dimension_group: order {
    type: time
    timeframes: [raw, date, week, month, quarter, year]
    sql: ${TABLE}.order_date ;;
    convert_tz: yes
  }

  dimension: amount_usd {
    type: number
    sql: ${TABLE}.amount_usd ;;
    value_format_name: usd
  }

  dimension: status {
    type: string
    sql: ${TABLE}.status ;;
  }

  measure: revenue {
    type: sum
    sql: ${amount_usd} ;;
    value_format_name: usd_0
    description: "Total gross revenue (USD)"
  }

  measure: order_count {
    type: count
    drill_fields: [order_id, customer_id, order_date, amount_usd]
  }

  measure: avg_order_value {
    type: number
    sql: ${revenue} / NULLIF(${order_count}, 0) ;;
    value_format_name: usd
  }

  measure: paid_revenue {
    type: sum
    sql: ${amount_usd} ;;
    filters: [status: "paid"]      # measure-level filter
  }
}
```

### Recipe 3 — A Model + Explore

```lookml
# models/finance.model.lkml

connection: "snowflake_prod"

include: "../views/*.view.lkml"

datagroup: daily_refresh {
  sql_trigger: SELECT max(order_date) FROM marts.fct_orders ;;
  max_cache_age: "24 hours"
}

persist_with: daily_refresh

explore: orders {
  from: fct_orders
  label: "Orders"
  description: "Order events with customer + product joins"

  join: dim_customers {
    from: dim_customers
    type: left_outer
    relationship: many_to_one
    sql_on: ${orders.customer_id} = ${dim_customers.customer_id} ;;
  }

  join: dim_products {
    from: dim_products
    type: left_outer
    relationship: many_to_one
    sql_on: ${orders.product_id} = ${dim_products.product_id} ;;
  }

  always_filter: {
    filters: [orders.order_date: "30 days"]
  }
}
```

### Recipe 4 — Derived table (analytical)

```lookml
view: customer_cohort_retention {
  derived_table: {
    sql:
      WITH cohorts AS (
        SELECT customer_id, DATE_TRUNC('month', MIN(order_date)) AS cohort_month
        FROM marts.fct_orders
        GROUP BY 1
      )
      SELECT
        c.cohort_month,
        DATEDIFF(month, c.cohort_month, o.order_date) AS months_since,
        COUNT(DISTINCT c.customer_id) AS active_users
      FROM cohorts c
      JOIN marts.fct_orders o USING (customer_id)
      GROUP BY 1, 2 ;;

    datagroup_trigger: daily_refresh
    indexes: [cohort_month]
    distribution: cohort_month   # warehouse-hint
  }

  dimension: cohort_month {
    type: date
    sql: ${TABLE}.cohort_month ;;
  }

  dimension: months_since {
    type: number
    sql: ${TABLE}.months_since ;;
  }

  measure: active_users {
    type: sum
    sql: ${TABLE}.active_users ;;
  }
}
```

### Recipe 5 — Row-Level Security via `access_filter`

```lookml
explore: orders {
  access_filter: {
    field: dim_customers.region
    user_attribute: region
  }
}
```

Then in Admin → Users → Edit user → "User Attributes" → set `region = US` per user.

### Recipe 6 — Constants (single source of truth)

```lookml
# manifest.lkml
constant: revenue_value_format {
  value: "usd_0"
  export: override_optional
}

# In view
measure: revenue {
  type: sum
  sql: ${amount_usd} ;;
  value_format_name: "@{revenue_value_format}"
}
```

### Recipe 7 — LookML Refinements (modify view without forking)

```lookml
# refinements/orders_marketing_refinement.view.lkml
view: +fct_orders {
  measure: paid_signup_revenue {
    type: sum
    sql: ${amount_usd} ;;
    filters: [
      status: "paid",
      acquisition_source: "paid_search,paid_social,paid_display"
    ]
  }
}
```

The `+` prefix adds without overriding; great for cross-team customization.

### Recipe 8 — Looker SDK (Python)

```python
import looker_sdk

sdk = looker_sdk.init40()         # reads looker.ini or env vars

# Run a Look (saved query)
result = sdk.run_look(look_id=42, result_format="csv")
print(result)

# Run an Inline Query (no saved Look)
from looker_sdk.sdk.api40.models import WriteQuery
q = WriteQuery(
    model="finance",
    view="orders",
    fields=["orders.order_date_month", "orders.revenue"],
    filters={"orders.order_date": "30 days"},
    sorts=["orders.order_date_month desc"],
    limit="500",
)
csv = sdk.run_inline_query(result_format="csv", body=q)

# Schedule a Look delivery
from looker_sdk.sdk.api40.models import WriteScheduledPlan
sdk.create_scheduled_plan(WriteScheduledPlan(
    name="Weekly revenue digest",
    look_id=42,
    crontab="0 9 * * 1",          # Mondays 9am
    user_id=current_user_id,
    scheduled_plan_destination=[{
        "format": "csv",
        "type": "email",
        "address": "execs@company.com",
    }]
))
```

### Recipe 9 — SSO embedding (signed JWT)

```python
import hmac, hashlib, time, base64, json, urllib.parse

def sign_looker_url(host, embed_secret, user, params):
    nonce = base64.b64encode(os.urandom(16)).decode()
    time_str = str(int(time.time()))
    session_length = 3600

    string_to_sign = "\n".join([
        host, params["embed_url"], nonce, time_str, str(session_length),
        json.dumps(user, separators=(",", ":")), json.dumps(params.get("permissions", []))
    ])
    signature = base64.b64encode(
        hmac.new(embed_secret.encode(), string_to_sign.encode(), hashlib.sha1).digest()
    ).decode()

    qs = urllib.parse.urlencode({
        **user, **params,
        "nonce": nonce, "time": time_str, "session_length": session_length,
        "signature": signature
    })
    return f"https://{host}/login/embed/{params['embed_url']}?{qs}"

url = sign_looker_url(
    host="company.looker.com",
    embed_secret=os.environ["LOOKER_EMBED_SECRET"],
    user={"external_user_id":"u_123","first_name":"Alice","email":"alice@x.com"},
    params={"embed_url":"/embed/dashboards/7?region=US"}
)
```

### Recipe 10 — Lightdash (OSS alternative) deploy

```bash
# Lightdash reads dbt project — no separate semantic layer
cd dbt-project/
echo "lightdash:" >> .gitignore

lightdash login --url https://my-lightdash.company.com
lightdash deploy --project-uuid $LD_PROJECT_UUID

# Lightdash auto-creates explores from dbt models
# Add dimensions/metrics directly to dbt schema.yml:
```

```yaml
models:
  - name: fct_orders
    meta:
      label: "Orders"
      joins:
        - join: dim_customers
          sql_on: ${fct_orders.customer_id} = ${dim_customers.customer_id}
    columns:
      - name: amount_usd
        meta:
          metrics:
            total_revenue:
              type: sum
              format: usd
          dimension:
            type: number
```

## Example end-to-end

**Goal:** Single source of truth for "MRR" across finance, marketing, and execs.

1. Define `fct_subscriptions` and `dim_customers` views in LookML.
2. In `fct_subscriptions.view.lkml`, define `measure: mrr` with clear SQL.
3. Build explore `subscriptions` in `finance.model.lkml`, join `dim_customers`.
4. Build "MRR Trend" Look (line chart, MRR by month).
5. Add to "Executive Summary" dashboard alongside churn, NRR, expansion measures.
6. Apply `access_filter` on `region` so each region head sees only their data.
7. Schedule dashboard email; subscribe Slack channel via Looker action.
8. Embed dashboard into internal portal via signed JWT.
9. PR review every LookML change (Git-versioned); validated by `lookml-parser` in CI.

## Edge cases / gotchas

- **`sql_table_name` lockdown** — fully qualify schemas (`marts.fct_orders` not just `fct_orders`) to avoid surprises across environments.
- **PDT (Persistent Derived Table) caching** — `datagroup_trigger` decides freshness; without it, derived tables can serve stale data forever.
- **Measure dependencies** — measures can reference other measures (`${revenue} / ${order_count}`); if one fails (e.g. NULL division), the dependent fails. Always wrap with `NULLIF` or `COALESCE`.
- **`access_filter` evaluation** — applied as a WHERE in compiled SQL; if user attribute is null, the filter often returns nothing. Provide defaults.
- **LookML refinements ordering** — multiple refinements applied in include order; lock down with explicit `include:` paths.
- **`always_filter` vs `conditionally_filter`** — `always_filter` forces a filter on every query (slow if too broad); `conditionally_filter` allows replacement.
- **Embed signature trustworthiness** — SHA-1 HMAC for legacy SSO embedding. Cookieless mode uses signed JWT with HS256 (newer; recommended).
- **API rate limits** — Looker enforces per-instance rate limits (typically ~200 req/min); batch queries via `create_query_task` for async.
- **LookML linting** — official `lookml-parser` (Node) catches syntax + naming errors in CI: `npx lookml-parser models/`.
- **Lightdash dimension/metric inheritance** — refinements via dbt YAML; doesn't support full LookML expressiveness, but covers ~80% of standard analytics.
- **Cost: Looker pricing** — sold by Google as instance + per-user; not transparent. For OSS path consider Lightdash + dbt MetricFlow.

## Sources

- [Looker documentation](https://cloud.google.com/looker/docs)
- [LookML quick reference](https://cloud.google.com/looker/docs/lookml-quick-reference)
- [Looker API 4.0](https://cloud.google.com/looker/docs/reference/looker-api/latest)
- [Looker SDK Python](https://pypi.org/project/looker-sdk/)
- [Looker SSO embedding](https://cloud.google.com/looker/docs/single-sign-on-embedding)
- [Lightdash documentation](https://docs.lightdash.com/)
- [LookML refinements](https://cloud.google.com/looker/docs/lookml-refinements)
- role.md → "Dashboard design playbook"
