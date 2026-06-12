<!--
Metabase docs: https://www.metabase.com/docs/
Companion: role.md → "Dashboard design playbook → Metabase"
-->

# Metabase — self-serve dashboards + embedded analytics

Stand up Metabase (OSS or Cloud), connect a warehouse, build governed self-serve dashboards (Questions → Dashboards), apply row-level security, and embed dashboards into product via signed JWT. Best OSS BI tool for small/medium orgs.

## When to use

- "Set up a BI tool for the team / give marketing self-serve access"
- Embed a dashboard into a customer-facing product (signed embedding)
- Build a tactical dashboard for ops/finance/product (5-7 KPI rule)
- Wire dbt models to a metric layer with row-level access control
- Provide ad-hoc SQL query interface for analysts who don't have warehouse credentials

Defer enterprise governed metrics (LookML) to `looker-lookml-modeling`. Defer notebook-as-app to `hex-notebooks-apps`. Defer markdown reports to `evidence-streamlit-marimo-reports`.

## Setup

```bash
# Self-host via Docker (recommended)
docker run -d -p 3000:3000 \
  --name metabase \
  -v $(pwd)/metabase-data:/metabase-data \
  -e MB_DB_TYPE=postgres \
  -e MB_DB_DBNAME=metabase \
  -e MB_DB_HOST=postgres-host \
  -e MB_DB_USER=metabase \
  -e MB_DB_PASS=$MB_DB_PASS \
  metabase/metabase:latest

# Or via JAR
java -jar metabase.jar           # listens on :3000

# Cloud: signup at metabase.com/start (paid tier from day 1)
```

First-time setup: navigate to http://localhost:3000, create admin, add database connection.

Auth requirements:
- Warehouse credentials (Snowflake / BigQuery / Databricks / Postgres / etc.)
- `MB_ENCRYPTION_SECRET_KEY` env var for encrypting saved connections (production)
- `MB_JWT_SHARED_SECRET` for signed embedding
- `METABASE_SESSION` token or API key for REST access

## Common recipes

### Recipe 1 — API authentication

```bash
# Get session token
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@example.com","password":"'"$MB_PASSWORD"'"}' \
  http://metabase.example.com/api/session
# Returns: {"id":"abc123..."}

export MB_SESSION="abc123..."

# Or use API key (Metabase 0.49+, recommended)
# Generate in UI: Settings → API Keys → Create
export MB_API_KEY="mb_..."
```

```bash
# Use API key in headers
curl -H "X-API-Key: $MB_API_KEY" http://metabase.example.com/api/database
```

### Recipe 2 — Create a Question (native SQL)

```bash
curl -X POST -H "X-API-Key: $MB_API_KEY" \
  -H "Content-Type: application/json" \
  http://metabase.example.com/api/card \
  -d '{
    "name": "Daily Revenue Last 30 Days",
    "dataset_query": {
      "type": "native",
      "native": {
        "query": "SELECT order_date, sum(amount_usd) AS revenue FROM marts.fct_orders WHERE order_date >= current_date - 30 GROUP BY 1 ORDER BY 1",
        "template-tags": {}
      },
      "database": 2
    },
    "display": "line",
    "visualization_settings": {
      "graph.dimensions": ["order_date"],
      "graph.metrics": ["revenue"]
    },
    "collection_id": null
  }'
```

### Recipe 3 — Create a Question with parameters (filter widget)

```sql
-- In the Metabase question editor (Native SQL):
SELECT order_date, sum(amount_usd) AS revenue
FROM marts.fct_orders
WHERE {{date_range}}                 -- Field Filter; binds to a date filter widget
  AND region = {{region}}            -- Text variable
GROUP BY 1
ORDER BY 1
```

Configure variables in the side panel:
- `date_range`: type "Field Filter" → mapped to `fct_orders.order_date`
- `region`: type "Text" → default value "US"

### Recipe 4 — Dashboard via API

```bash
# Create dashboard
curl -X POST -H "X-API-Key: $MB_API_KEY" \
  -H "Content-Type: application/json" \
  http://metabase.example.com/api/dashboard \
  -d '{"name":"Executive Summary","description":"Top-level KPIs"}'
# Returns: {"id":7,...}

# Add a question to dashboard
curl -X POST -H "X-API-Key: $MB_API_KEY" \
  -H "Content-Type: application/json" \
  "http://metabase.example.com/api/dashboard/7/cards" \
  -d '{"cardId":42, "row":0, "col":0, "size_x":6, "size_y":4}'

# Add a dashboard filter
curl -X PUT -H "X-API-Key: $MB_API_KEY" \
  -H "Content-Type: application/json" \
  http://metabase.example.com/api/dashboard/7 \
  -d '{
    "parameters":[
      {"name":"Date","slug":"date","id":"abc","type":"date/range","sectionId":"date"},
      {"name":"Region","slug":"region","id":"def","type":"string/=","sectionId":"string"}
    ]
  }'
```

### Recipe 5 — Row-Level Security via Sandboxing

In UI:
1. Admin → Permissions → Data → choose group → "Sandboxed"
2. Choose table → "Filter by column"
3. Map a user attribute (e.g. `user_attribute("region_id")`) to a column (e.g. `customers.region_id`)
4. All queries by that group now auto-WHERE-clause on region_id

Programmatic:

```bash
# Set user attributes
curl -X PUT -H "X-API-Key: $MB_API_KEY" \
  -H "Content-Type: application/json" \
  http://metabase.example.com/api/user/42 \
  -d '{"login_attributes":{"region_id":"EU","tier":"premium"}}'
```

### Recipe 6 — Signed embedding (public-facing)

Configure in Admin → Settings → Embedding:
1. Enable "Static embedding"
2. Note the **embedding secret key**: `MB_JWT_SHARED_SECRET`
3. Make a dashboard "Embeddable" via its UI menu

Generate signed URL per user:

```python
import jwt
import time

METABASE_SITE_URL = "http://metabase.example.com"
METABASE_SECRET_KEY = os.environ["MB_JWT_SHARED_SECRET"]

payload = {
    "resource": {"dashboard": 7},
    "params": {"region": "US", "customer_id": current_user_id},  # locked params
    "exp": round(time.time()) + (60 * 10)  # 10-minute expiry
}
token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")
iframe_url = f"{METABASE_SITE_URL}/embed/dashboard/{token}#bordered=true&titled=false"
```

Drop into your app: `<iframe src="{{ iframe_url }}" width="100%" height="800" />`.

### Recipe 7 — Interactive embedding (full SSO)

For per-user filtering with the full Metabase UI (paid Pro tier):

```javascript
// Frontend integration
const url = `${METABASE_HOST}/auth/sso?jwt=${signed_jwt}&return_to=/dashboard/7`;
window.location = url;
```

Configure JWT SSO in Admin → Settings → Authentication.

### Recipe 8 — Dashboard subscriptions (email + Slack)

In dashboard UI:
1. Sharing menu → "Subscriptions"
2. Choose channel (email / Slack)
3. Schedule (hourly / daily / weekly / monthly)
4. Optional: alert when a metric crosses threshold

Programmatic via `POST /api/pulse` (legacy) or `POST /api/dashboard/<id>/subscription` (current).

### Recipe 9 — Cache management

Performance: enable caching on slow questions.

Admin → Performance → Question caching:
- TTL caching: cache for N minutes per question
- Per-dashboard caching: applied across all its cards
- Aggressive caching for cards >2s

API:

```bash
curl -X PUT -H "X-API-Key: $MB_API_KEY" \
  -H "Content-Type: application/json" \
  http://metabase.example.com/api/card/42 \
  -d '{"cache_ttl": 3600}'        # 1 hour cache
```

### Recipe 10 — Connect dbt MetricFlow (governed metrics)

Metabase supports dbt's Semantic Layer (MetricFlow) since v0.50:

1. Admin → Databases → "Add" → dbt Cloud Semantic Layer connector
2. Supply dbt Cloud account ID + service token + environment ID
3. dbt-defined metrics appear as first-class objects (questions can pick `Metric: revenue` directly)

Or via API:

```bash
curl -X POST -H "X-API-Key: $MB_API_KEY" \
  -H "Content-Type: application/json" \
  http://metabase.example.com/api/database \
  -d '{
    "engine": "dbtcloud",
    "name": "dbt Semantic Layer",
    "details": {
      "account_id": "1234",
      "service_token": "'"$DBT_TOKEN"'",
      "environment_id": "5678"
    }
  }'
```

## Example end-to-end

**Goal:** Self-serve executive dashboard with 5 KPIs, region filter, subscriptions, and embedded view in the company intranet.

1. Connect Snowflake warehouse: Admin → Databases → Add.
2. Build 5 questions: MRR, Active Users, Churn Rate, NPS, Conversion Rate.
3. Create "Executive Summary" dashboard; add 5 cards in a 2-3 grid.
4. Add "Date Range" + "Region" filters; map each filter to all relevant questions.
5. Set up Slack subscription: weekly Monday 9am to #execs channel.
6. Mark dashboard Embeddable; lock the `region` parameter per intranet's logged-in user.
7. Intranet generates signed JWT with `region=<user.region>`, renders iframe.
8. Audit: Admin → Auditing → Dashboard views; monitor adoption.

## Edge cases / gotchas

- **Self-host Metabase H2 default DB** — fine for dev; **switch to Postgres for prod** before scaling (H2 corrupts on crash).
- **Signed embedding param locking** — locked params can't be overridden by users; if you forget to lock `customer_id`, users can spoof.
- **Cache invalidation on dashboard subscription** — subscriptions force a fresh query (bypass cache); plan warehouse cost.
- **`current_date` semantics** — Metabase relative dates ("last 7 days") use server timezone, not warehouse timezone — set both consistently.
- **API key vs session token** — API keys don't expire; revoke proactively when team members leave. Session tokens expire in ~14 days.
- **Static embedding signed URLs cache server-side** — same payload + same secret = same JWT; queries hit cache. Add `exp` claim for freshness.
- **SQL Snippets** — reusable SQL fragments (defined under "SQL Snippets") usable across questions; treat like macros.
- **Pulses (legacy) vs Subscriptions (current)** — older Metabase used pulses; v0.45+ migrated to subscriptions. API endpoints differ.
- **Field metadata sync** — when warehouse schema changes, run "Sync schema now" in DB settings; Metabase doesn't auto-detect new columns instantly.
- **Permission inheritance** — collections inherit from parent; double-check before granting a collection-level permission.
- **OSS vs Pro features** — interactive embedding, advanced auditing, SSO, official models are Pro-only. Confirm tier before recommending.

## Sources

- [Metabase documentation](https://www.metabase.com/docs/latest/)
- [Metabase REST API reference](https://www.metabase.com/docs/latest/api-documentation)
- [Metabase static embedding](https://www.metabase.com/docs/latest/embedding/static-embedding)
- [Metabase interactive embedding](https://www.metabase.com/docs/latest/embedding/interactive-embedding)
- [Metabase row-level sandboxing](https://www.metabase.com/docs/latest/permissions/data-sandboxes)
- [Metabase dbt Semantic Layer connector (2025)](https://www.metabase.com/docs/latest/databases/connections/dbt-semantic-layer)
- role.md → "Dashboard design playbook"
