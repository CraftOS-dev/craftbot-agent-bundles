<!--
Census: https://docs.getcensus.com/
Hightouch: https://hightouch.com/docs
Polytomic: https://docs.polytomic.com/
dlt: https://dlthub.com/docs/
Companion: role.md → "Reverse ETL playbook"
-->

# Reverse ETL — Census, Hightouch, Polytomic, dlt-based custom syncs

Push warehouse data back into operational SaaS tools (Salesforce, HubSpot, Marketo, Iterable, Segment, Slack). Managed platforms: Census / Hightouch / Polytomic. Custom code-first: dlt + per-SaaS API. Includes triggers, mapping, monitoring, idempotency.

## When to use

- "Sync warehouse customer LTV scores to Salesforce so AEs see them"
- "Push propensity-to-churn to Marketo as a list"
- "Trigger a Slack alert when key-account health drops"
- "Update HubSpot contact records nightly with warehouse fields"
- "Send segment audiences to ad networks (Meta, Google, TikTok)"

Defer ELT (warehouse ingestion) to `dlt-fivetran-airbyte-elt`. Defer dashboards to `metabase-self-serve-dashboards`. Defer pure warehouse modeling to `dbt-modeling-staging-marts`.

## Setup

```bash
# Managed platforms — provision via web UI
# Census:    app.getcensus.com (free tier, then paid)
# Hightouch: app.hightouch.com (free tier, then paid)
# Polytomic: polytomic.com (paid)

# Auth tokens for API-driven runs
export CENSUS_API_TOKEN="..."
export HIGHTOUCH_API_TOKEN="..."
export POLYTOMIC_API_TOKEN="..."

# Custom code-first (dlt)
pip install dlt
pip install salesforce-bulk             # or hubspot-api-client, mailchimp_marketing, etc.
```

## Tool comparison

| Aspect | Census | Hightouch | Polytomic | dlt (custom) |
|---|---|---|---|---|
| Pricing | Free tier (10k MTU), then paid | Free tier (10k MTU), then paid | Paid only | Free (OSS) |
| Connectors | 200+ | 200+ | 150+ | unlimited (build yourself) |
| dbt integration | first-class (dbt artifact) | first-class | yes | manual |
| Reverse + forward ETL | reverse only | reverse only | both | both |
| Idempotency | built-in | built-in | built-in | DIY |
| Best for | enterprise, governance | broad coverage, dbt-native | small teams | custom logic, OSS-first |

## Common recipes

### Recipe 1 — Census API: trigger a sync

```bash
# Trigger sync run
curl -X POST \
  -H "Authorization: Bearer $CENSUS_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://app.getcensus.com/api/v1/syncs/12345/trigger" \
  -d '{"force_full_sync": false}'

# Response: {"status":"success", "data":{"sync_run_id":98765, "status":"working"}}

# Poll status
curl -H "Authorization: Bearer $CENSUS_API_TOKEN" \
  "https://app.getcensus.com/api/v1/sync_runs/98765"

# List recent runs
curl -H "Authorization: Bearer $CENSUS_API_TOKEN" \
  "https://app.getcensus.com/api/v1/syncs/12345/sync_runs?per_page=10"
```

### Recipe 2 — Census model (in warehouse)

In Census UI:
1. Connect Source (Snowflake / BigQuery / etc.)
2. Create Model → SQL or dbt-model reference:
   ```sql
   SELECT
       customer_id,
       email,
       lifetime_value_usd,
       churn_propensity_score,
       last_login_at,
       health_score
   FROM marts.customer_360
   WHERE updated_at > current_timestamp - interval '7 days'
   ```
3. Choose Primary Key (`customer_id`) — required for idempotent updates.
4. Create Sync → Destination (Salesforce / HubSpot / etc.) → field mapping → schedule.

### Recipe 3 — Hightouch via API

```python
import requests
import os

HIGHTOUCH_API = "https://api.hightouch.com/api/v1"
headers = {"Authorization": f"Bearer {os.environ['HIGHTOUCH_API_TOKEN']}"}

# Trigger sync
r = requests.post(f"{HIGHTOUCH_API}/syncs/12345/trigger", headers=headers,
                  json={"fullResync": False})
print(r.json())   # {"id": "run_xyz", ...}

# Get run status
status = requests.get(f"{HIGHTOUCH_API}/syncs/12345/runs/run_xyz", headers=headers).json()

# Pause a sync
requests.put(f"{HIGHTOUCH_API}/syncs/12345", headers=headers, json={"schedule": {"type": "manual"}})
```

### Recipe 4 — Hightouch CLI (`htsync`)

```bash
# Install: npm i -g hightouch-cli
htsync auth --token $HIGHTOUCH_API_TOKEN

htsync sync trigger --sync-id 12345
htsync sync list
htsync sync logs --sync-id 12345 --tail
```

### Recipe 5 — dbt + reverse-ETL integration

In dbt project, model the sync payload:

```sql
-- models/marts/reverse_etl/sf_contact_sync.sql
{{ config(materialized='table', tags=['reverse_etl']) }}

SELECT
    c.customer_id                AS sfdc_id,
    c.email,
    c.first_name,
    c.last_name,
    c.lifetime_value_usd         AS sfdc_ltv__c,
    c.churn_propensity_score     AS sfdc_churn_score__c,
    c.health_score               AS sfdc_health__c,
    c.last_activity_at           AS sfdc_last_activity__c
FROM {{ ref('dim_customers') }} c
WHERE c.is_active = true
```

Census/Hightouch detects the `tags: ['reverse_etl']` and surfaces these models as sync sources.

### Recipe 6 — Custom dlt reverse sync (Salesforce)

```python
import dlt
from simple_salesforce import Salesforce
import snowflake.connector

@dlt.resource(name="contact_updates", write_disposition="merge", primary_key="customer_id")
def contact_payload():
    conn = snowflake.connector.connect(**SF_CREDS)
    cur = conn.cursor(snowflake.connector.DictCursor)
    cur.execute("SELECT * FROM marts.reverse_etl.sf_contact_sync WHERE updated_at > current_timestamp - interval '1 day'")
    yield from cur.fetchall()

@dlt.destination(name="salesforce")
def salesforce_destination(items, _table):
    sf = Salesforce(username=SF_USER, password=SF_PASS, security_token=SF_TOKEN)
    for batch in chunked(items, 200):
        upserts = [
            {
                "Id": r["sfdc_id"],
                "LTV__c": r["sfdc_ltv__c"],
                "ChurnScore__c": r["sfdc_churn_score__c"],
                "HealthScore__c": r["sfdc_health__c"],
            }
            for r in batch
        ]
        result = sf.bulk.Contact.upsert(upserts, "Id", batch_size=200)
        # Track failures
        for r, status in zip(upserts, result):
            if not status["success"]:
                print(f"Failed: {r['Id']}: {status['errors']}")

p = dlt.pipeline(pipeline_name="warehouse_to_salesforce", destination=salesforce_destination)
p.run(contact_payload())
```

### Recipe 7 — Trigger sync from dbt run

```yaml
# In dbt_project.yml — post-hook to trigger Census sync after model build
models:
  marts:
    reverse_etl:
      +post-hook: |
        {% set webhook = env_var('CENSUS_WEBHOOK_URL', '') %}
        {% if webhook %}
          {% do run_query("CALL system$send_email('census', '" ~ webhook ~ "', 'Sync triggered', '" ~ this ~ "')") %}
        {% endif %}
```

Or use dbt Cloud / Airflow to schedule sync immediately after dbt build.

### Recipe 8 — Sync configuration via Census API (programmatic)

```python
import requests

# Create sync programmatically (rare; usually UI-driven)
r = requests.post(
    "https://app.getcensus.com/api/v1/syncs",
    headers={"Authorization": f"Bearer {CENSUS_TOKEN}"},
    json={
        "label": "Sync customer LTV to Salesforce",
        "source": {
            "type": "snowflake",
            "id": 1,
            "model_id": 42,
        },
        "destination": {
            "type": "salesforce",
            "id": 5,
            "object": "Contact",
        },
        "operation": "upsert",
        "schedule": {"frequency": "daily", "hour": 3},
        "field_mappings": [
            {"from": "customer_id", "to": "Id"},
            {"from": "lifetime_value_usd", "to": "LTV__c"},
            {"from": "churn_propensity_score", "to": "ChurnScore__c"},
        ],
    },
)
print(r.json())
```

### Recipe 9 — Sync monitoring (CLI poller)

```python
import time
import requests

def wait_for_sync(sync_id, timeout=1800):
    """Block until sync completes or fails."""
    start = time.time()
    while time.time() - start < timeout:
        r = requests.get(
            f"https://app.getcensus.com/api/v1/syncs/{sync_id}/sync_runs?per_page=1",
            headers={"Authorization": f"Bearer {CENSUS_TOKEN}"}
        ).json()
        latest = r["data"][0]
        status = latest["status"]
        if status == "completed":
            return latest
        if status in ("failed", "cancelled"):
            raise RuntimeError(f"Sync failed: {latest}")
        time.sleep(10)
    raise TimeoutError(f"Sync {sync_id} did not finish in {timeout}s")

result = wait_for_sync(12345)
print(f"Rows synced: {result.get('records_processed', '?')}")
print(f"Failures: {result.get('records_failed', 0)}")
```

### Recipe 10 — Idempotency + dedup pattern

```sql
-- Pattern: dedupe + add hash to detect changes
-- Source model (warehouse side)
SELECT
    customer_id,
    -- Compute a hash of fields that should trigger sync
    MD5(CONCAT_WS('|',
        COALESCE(email, ''),
        CAST(lifetime_value_usd AS VARCHAR),
        CAST(churn_propensity_score AS VARCHAR)
    )) AS row_hash,
    email,
    lifetime_value_usd,
    churn_propensity_score
FROM {{ ref('dim_customers') }}
WHERE row_hash != COALESCE(
    -- Reference to previous sync state (read from sync metadata)
    (SELECT row_hash FROM raw.census_sync_log
     WHERE customer_id = dim_customers.customer_id
     ORDER BY synced_at DESC LIMIT 1),
    ''
)
```

Census/Hightouch handle change detection automatically via their `_dbt_state` tables; this manual pattern is for custom dlt syncs.

## Example end-to-end

**Goal:** Sync the warehouse `customer_360` mart to Salesforce so account executives see LTV + churn risk in real-time.

1. dbt model `marts/reverse_etl/sf_contact_sync.sql` exposes the payload.
2. In Census UI: connect Snowflake source → reference the dbt model.
3. Connect Salesforce destination (OAuth flow).
4. Create sync: map `customer_id → Salesforce Contact ID`, `LTV → LTV__c`, etc.
5. Schedule: 4x daily (every 6h).
6. Set alerts: Slack #data-ops on sync failure.
7. Validate: spot-check 20 Salesforce records vs warehouse values.
8. Add a `dbt_run + census_trigger` Airflow DAG that calls Recipe 1 immediately after dbt builds the model.
9. Monitor row failure rate; rate >1% triggers PagerDuty.

## Edge cases / gotchas

- **Salesforce API rate limits** — Bulk API: 5000 batches/day; ensure batch size 100-200, use Bulk 2.0 where possible.
- **HubSpot 10-property update limit** — single contact update API supports ≤10 props; for more, batch via separate calls.
- **Idempotency requires stable PK** — sync target must have a deterministic identifier (email is unreliable for B2B; use external ID).
- **Snake/camel case mismatches** — Salesforce custom fields end in `__c` and are case-sensitive in API; Census/Hightouch UI shows actual API names.
- **Sync orphans** — if you delete a warehouse row, the SaaS record persists unless your sync runs delete-mode. Most platforms default to upsert-only.
- **Authentication refresh** — OAuth tokens expire; managed platforms refresh automatically, dlt custom must implement refresh logic.
- **Bidirectional sync conflicts** — if both warehouse and SaaS edit the same field, last-write-wins data loss. Designate one as source-of-truth per field.
- **PII in sync logs** — Census/Hightouch log row count, not values; verify before treating logs as audit trail.
- **Cost models** — Census/Hightouch price by Monthly Tracked Users (MTU = unique records synced). Filtering to active users saves money.
- **dbt model materialization for reverse-ETL** — `table` materialization is recommended (Census reads full table state); `view` re-executes the source query on every sync.
- **Webhooks vs polling** — Census triggers sync via Snowflake task / dbt webhook for sub-minute latency; polling adds 5-30min lag.
- **Backfill** — first run touches every record; subsequent runs only changed rows. Plan SaaS API quota accordingly.

## Sources

- [Census API documentation](https://docs.getcensus.com/api)
- [Census dbt integration](https://docs.getcensus.com/sources/dbt-cloud)
- [Hightouch API reference](https://hightouch.com/docs/api/overview)
- [Hightouch dbt integration](https://hightouch.com/docs/syncs/sync-source/dbt-models)
- [Polytomic docs](https://docs.polytomic.com/)
- [dlt documentation](https://dlthub.com/docs/)
- [Reverse ETL — Census blog 2025](https://www.getcensus.com/blog/what-is-reverse-etl)
- role.md → "Reverse ETL playbook"
