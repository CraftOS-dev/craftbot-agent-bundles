<!--
dlt: https://dlthub.com/docs/
Airbyte: https://docs.airbyte.com/
Fivetran: https://fivetran.com/docs/
Companion: role.md → "ELT design playbook"
-->

# ELT — dlt (Python OSS), Airbyte, Fivetran

Move data from SaaS APIs, databases, and event streams into the warehouse. Code-first OSS via dlt (modern, 2024+); OSS managed via Airbyte; commercial managed via Fivetran. Includes connector authoring, incremental loading, schema evolution, and idempotency patterns.

## When to use

- "Pull data from Stripe / HubSpot / Salesforce / etc. into Snowflake / BigQuery"
- "Build a custom connector for an internal API"
- "Replace expensive Fivetran with OSS Airbyte or code-first dlt"
- "Need code-first ELT with full transparency"
- "Stream change-data-capture from Postgres / MySQL"

Defer warehouse-side transformation (staging → marts) to `dbt-modeling-staging-marts`. Defer warehouse → SaaS to `reverse-etl-census-hightouch`. Defer data-quality assertions to `great-expectations-soda-data-quality`.

## Setup

```bash
# dlt — Python OSS, code-first
pip install dlt
pip install "dlt[snowflake]"          # destination-specific extras

# Airbyte — OSS / Cloud
# Self-host via docker compose:
git clone --depth=1 https://github.com/airbytehq/airbyte && cd airbyte && ./run-ab-platform.sh

# Fivetran — managed only; provision in fivetran.com UI
# REST API for orchestration:
export FIVETRAN_API_KEY="..."
export FIVETRAN_API_SECRET="..."
```

Auth requirements:
- dlt: source-specific (Stripe API key, HubSpot OAuth, etc.); destination (warehouse creds)
- Airbyte Cloud: workspace token; OSS: admin UI password
- Fivetran: API key/secret for orchestration; UI-configured source/dest creds

## Tool comparison

| Aspect | dlt | Airbyte | Fivetran |
|---|---|---|---|
| Cost | Free (OSS) | OSS free / Cloud paid | Paid only |
| Connectors | code-first + 30+ verified | 600+ | 600+ |
| Setup | `pip install` | docker / Cloud signup | UI signup |
| Customization | unlimited (Python) | medium (CDK) | minimal |
| Best for | custom logic, OSS-first | enterprise OSS / Cloud | zero-ops managed |

## Common recipes — dlt

### Recipe 1 — dlt source from REST API (paginated)

```python
import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import JSONResponsePaginator
import os

@dlt.source(name="hubspot")
def hubspot_source(api_key=dlt.secrets.value):
    client = RESTClient(
        base_url="https://api.hubapi.com",
        headers={"Authorization": f"Bearer {api_key}"},
        paginator=JSONResponsePaginator(next_url_path="paging.next.link"),
    )

    @dlt.resource(write_disposition="merge", primary_key="id")
    def contacts():
        for page in client.paginate("/crm/v3/objects/contacts",
                                    params={"limit": 100, "properties": "email,firstname,lastname,lifecyclestage"}):
            yield page

    @dlt.resource(write_disposition="merge", primary_key="id")
    def deals():
        for page in client.paginate("/crm/v3/objects/deals"):
            yield page

    return contacts, deals

p = dlt.pipeline(pipeline_name="hubspot_to_snowflake", destination="snowflake", dataset_name="raw_hubspot")
p.run(hubspot_source())

# Stats
print(p.last_trace)
```

### Recipe 2 — dlt incremental loading

```python
import dlt
from datetime import datetime

@dlt.resource(primary_key="id", write_disposition="merge")
def events(updated_at=dlt.sources.incremental("updated_at", initial_value="2025-01-01T00:00:00Z")):
    """Incremental on updated_at; auto-resumes from last value."""
    cur_max = updated_at.last_value
    while True:
        rows = api.get_events(updated_after=cur_max, limit=1000)
        if not rows: break
        yield rows
        cur_max = max(r["updated_at"] for r in rows)
```

dlt tracks the last `updated_at` value seen and resumes from there on next run.

### Recipe 3 — dlt schema evolution

```python
import dlt

@dlt.resource
def my_table():
    yield [
        {"id": 1, "name": "Alice", "email": "a@x.com"},                       # Run 1
        # Run 2 introduces a new column — dlt auto-adds to destination
        {"id": 2, "name": "Bob", "email": "b@x.com", "phone": "555-1234"},
    ]

p = dlt.pipeline(pipeline_name="evolution_demo", destination="snowflake")
p.run(my_table())

# Schema contract — fail or warn on changes
import dlt
@dlt.source(schema_contract={"tables": "evolve", "columns": "freeze", "data_type": "freeze"})
def strict_source():
    @dlt.resource
    def x(): ...
```

Schema contract values: `evolve` (auto-add), `freeze` (no change allowed → fail), `discard_value` (drop new columns), `discard_row` (skip rows with new columns).

### Recipe 4 — dlt with Snowflake destination

```python
import dlt

# Credentials via env vars or secrets.toml
# DESTINATION__SNOWFLAKE__CREDENTIALS__DATABASE = "RAW"
# DESTINATION__SNOWFLAKE__CREDENTIALS__USERNAME = "..."
# DESTINATION__SNOWFLAKE__CREDENTIALS__PASSWORD = "..."
# DESTINATION__SNOWFLAKE__CREDENTIALS__HOST = "..."
# DESTINATION__SNOWFLAKE__CREDENTIALS__WAREHOUSE = "..."

p = dlt.pipeline(
    pipeline_name="my_pipeline",
    destination="snowflake",
    dataset_name="raw_sources",        # Snowflake schema
    progress="enlighten",               # live progress bar
)

p.run(source())

# Get load summary
print(p.last_trace.last_normalize_info)
print(p.last_trace.last_load_info)
```

### Recipe 5 — dlt SQL database source (CDC-like)

```python
import dlt
from dlt.sources.sql_database import sql_database

# Pull tables from a Postgres replica
source = sql_database(
    credentials="postgresql://reader:pass@host:5432/prod",
    schema="public",
    table_names=["users", "orders", "products"],
)

# Mark `updated_at` as incremental hint
for t in ["users", "orders", "products"]:
    source.resources[t].apply_hints(incremental=dlt.sources.incremental("updated_at"))

p = dlt.pipeline(pipeline_name="pg_to_snowflake", destination="snowflake", dataset_name="raw_pg")
p.run(source)
```

### Recipe 6 — dlt running on schedule (cron / Airflow / Dagster)

```python
# Airflow DAG
from airflow.decorators import dag, task
from datetime import datetime, timedelta

@dag(schedule="@hourly", start_date=datetime(2026, 1, 1), catchup=False)
def hubspot_etl():
    @task
    def run_dlt():
        import dlt
        from my_sources import hubspot_source
        p = dlt.pipeline("hubspot", destination="snowflake", dataset_name="raw_hubspot")
        info = p.run(hubspot_source())
        return str(info)

    run_dlt()

dag_instance = hubspot_etl()
```

## Common recipes — Airbyte

### Recipe 7 — Airbyte CLI (Octavia)

```bash
# Configure source + destination via UI, or programmatically:
airbyte source create --name "Stripe" --connector "Stripe" --config '{"client_secret":"$STRIPE_KEY","start_date":"2025-01-01T00:00:00Z","lookback_window_days":7}'

airbyte destination create --name "Snowflake" --connector "Snowflake" --config '{"host":"...","role":"...","warehouse":"...","database":"RAW","schema":"STRIPE","username":"...","password":"..."}'

airbyte connection create --source-id "..." --destination-id "..." --schedule "*/30 * * * *"

# Trigger a sync
airbyte connection sync --connection-id "..."
```

### Recipe 8 — Airbyte REST API

```bash
# Authenticate
curl -X POST https://api.airbyte.com/v1/applications/token \
  -H "Content-Type: application/json" \
  -d '{"client_id":"$AB_CLIENT_ID","client_secret":"$AB_CLIENT_SECRET","grant-type":"client_credentials"}'
# → access_token

# List connections
curl -H "Authorization: Bearer $TOKEN" "https://api.airbyte.com/v1/connections?workspaceIds=$WS_ID"

# Trigger sync
curl -X POST -H "Authorization: Bearer $TOKEN" "https://api.airbyte.com/v1/jobs" \
  -d '{"jobType":"sync","connectionId":"$CONN_ID"}'

# Monitor
curl -H "Authorization: Bearer $TOKEN" "https://api.airbyte.com/v1/jobs/$JOB_ID"
```

### Recipe 9 — Airbyte custom connector (low-code CDK)

YAML connector spec:

```yaml
# airbyte-integrations/connectors/source-myapi/source_myapi/spec.yaml
version: 0.1.0
type: HttpStream
description: Pull data from MyAPI
streams:
  - name: users
    primary_key: id
    cursor_field: updated_at
    paginator:
      type: OffsetIncrementPaginator
      page_size: 100
      offset_value: "{{ stream_state['page'] }}"
    requester:
      url_base: "https://api.myapi.com"
      path: "/users"
      authenticator:
        type: BearerAuthenticator
        api_token: "{{ config['api_key'] }}"
      request_parameters:
        updated_after: "{{ stream_state['updated_at'] }}"
```

```bash
# Build + register
airbyte-ci connectors --name=source-myapi build
```

## Common recipes — Fivetran

### Recipe 10 — Fivetran REST API

```bash
# Trigger a connector sync
curl -X POST \
  -H "Authorization: Basic $(echo -n "$FIVETRAN_API_KEY:$FIVETRAN_API_SECRET" | base64)" \
  "https://api.fivetran.com/v1/connectors/$CONNECTOR_ID/force"

# Check status
curl -H "Authorization: Basic $(echo -n "$FIVETRAN_API_KEY:$FIVETRAN_API_SECRET" | base64)" \
  "https://api.fivetran.com/v1/connectors/$CONNECTOR_ID"

# Modify sync frequency
curl -X PATCH \
  -H "Authorization: Basic $(echo -n "$FIVETRAN_API_KEY:$FIVETRAN_API_SECRET" | base64)" \
  -H "Content-Type: application/json" \
  -d '{"sync_frequency": 60}' \
  "https://api.fivetran.com/v1/connectors/$CONNECTOR_ID"
```

## Example end-to-end

**Goal:** Replace a Fivetran Stripe pipeline with dlt to cut costs while keeping daily syncs.

1. Author dlt source: `dlt init stripe snowflake` → generates scaffold.
2. Implement Stripe REST source with pagination (Recipe 1 pattern) for `charges`, `customers`, `subscriptions`, `invoices`.
3. Mark `updated` field as incremental (Recipe 2).
4. Test locally against DuckDB destination: `dlt.pipeline(destination="duckdb").run(source())`.
5. Deploy to Snowflake destination via env-var credentials.
6. Schedule via Airflow (Recipe 6): hourly sync.
7. Monitor: dbt source freshness check on `raw_stripe.charges` (warn>2h, error>6h).
8. Pause Fivetran connector, validate parity for 1 week before disabling.
9. Estimated savings: $500/mo Fivetran credits → $20/mo Airflow compute.

## Edge cases / gotchas

- **dlt incremental + backfill** — initial run pulls everything from `initial_value`; for huge sources, split into time-windowed runs.
- **API rate limits** — dlt's `RESTClient` supports backoff via `paginator.config`; check destination-specific quotas.
- **Schema contract surprises** — `evolve` mode auto-adds columns; if a downstream dbt model has explicit `select *`, it picks up unexpected columns.
- **Type inference** — dlt infers types from first batch; explicit type hints (`dlt.resource(columns={"id":{"data_type":"bigint"}})`) prevent drift.
- **Snowflake column name case** — dlt normalizes to lowercase; some destinations preserve case. Check with `pipeline.default_schema.tables`.
- **Airbyte resync vs incremental** — destination changes (Snowflake column drop) require `Reset Data` button — incremental won't recover.
- **Fivetran column blocking** — blocked columns aren't recoverable without resync; cost = MAR (Monthly Active Rows).
- **CDC vs polling** — dlt + Postgres replication slots = true CDC; polling-only sources have ~minute latency.
- **Credential rotation** — Fivetran tokens auto-refresh; dlt requires manual rotation or vault integration.
- **Idempotency** — dlt with `primary_key + write_disposition="merge"` is idempotent; without it, dupes accumulate.
- **State storage** — dlt stores incremental state in destination's `_dlt_loads` table by default; if you drop it, next run re-syncs from initial_value.
- **Airbyte OSS upgrade pain** — major version upgrades (0.x → 1.x) often need manual config migration.
- **PII redaction** — dlt has `dlt.transformer` for transforms; Airbyte supports column-level masking; Fivetran has hashed columns. Use any of them for PII at ingestion.

## Sources

- [dlt documentation](https://dlthub.com/docs/)
- [dlt verified sources](https://dlthub.com/docs/dlt-ecosystem/verified-sources/)
- [dlt destinations](https://dlthub.com/docs/dlt-ecosystem/destinations/)
- [Airbyte documentation](https://docs.airbyte.com/)
- [Airbyte API reference](https://reference.airbyte.com/reference/start)
- [Airbyte connector development kit (CDK)](https://docs.airbyte.com/connector-development/)
- [Fivetran REST API](https://fivetran.com/docs/rest-api)
- [Fivetran connector list](https://fivetran.com/connectors)
- [Modern data stack — dlt vs Fivetran vs Airbyte (2025)](https://dlthub.com/why)
- role.md → "ELT design playbook"
