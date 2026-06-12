<!--
Snowflake QUERY_HISTORY: https://docs.snowflake.com/en/sql-reference/account-usage/query_history
BigQuery INFORMATION_SCHEMA: https://cloud.google.com/bigquery/docs/information-schema-jobs
Databricks query history: https://docs.databricks.com/sql/admin/system-tables.html
Companion: role.md → "Warehouse cost playbook"
-->

# Warehouse cost optimization — Snowflake credits, BigQuery slots, Databricks DBUs

Identify, attribute, and reduce warehouse costs. Build a credit/slot/DBU attribution dashboard from `QUERY_HISTORY` / `INFORMATION_SCHEMA.JOBS_BY_PROJECT` / system tables. Apply auto-suspend, multi-cluster, materialized views, partitioning + clustering, and dbt materialization audits.

## When to use

- "Snowflake bill jumped 30% this month — where did it come from?"
- "Optimize this $X/month BigQuery workload"
- "Set up cost monitoring + budget alerts"
- "Identify the top-10 most-expensive queries"
- "Right-size warehouses; should we move to multi-cluster?"
- "dbt model materialization audit — should X be incremental?"

Defer dialect-specific patterns to `snowflake-bigquery-databricks-warehousing`. Defer dbt structure to `dbt-modeling-staging-marts`. Defer pipeline-side cost (ELT) to `dlt-fivetran-airbyte-elt`.

## Setup

```bash
pip install snowflake-connector-python google-cloud-bigquery databricks-sql-connector
pip install pandas plotly
```

Auth requirements:
- Snowflake: role with `IMPORT SHARE` privilege on `SNOWFLAKE.ACCOUNT_USAGE` (Account Admin grants).
- BigQuery: `bigquery.jobs.listAll` permission for project-wide queries; cross-project requires admin.
- Databricks: SQL Warehouse access + access to `system.access`/`system.compute` schemas.

## Common recipes — Snowflake

### Recipe 1 — Top 20 most-expensive queries (last 7 days)

```sql
USE WAREHOUSE COMPUTE_WH;
USE DATABASE SNOWFLAKE;
USE SCHEMA ACCOUNT_USAGE;

SELECT
    SUBSTR(query_text, 1, 200) AS query_text,
    warehouse_name,
    user_name,
    role_name,
    DATEDIFF('second', start_time, end_time) AS exec_seconds,
    bytes_scanned / 1e9 AS gb_scanned,
    rows_produced,
    credits_used_cloud_services + COALESCE(credits_used, 0) AS total_credits,
    execution_status,
    query_tag
FROM query_history
WHERE start_time > CURRENT_DATE - INTERVAL '7 days'
  AND execution_status = 'SUCCESS'
ORDER BY total_credits DESC
LIMIT 20;
```

### Recipe 2 — Credit attribution by warehouse + user

```sql
SELECT
    warehouse_name,
    user_name,
    DATE_TRUNC('day', start_time) AS query_day,
    COUNT(*) AS query_count,
    SUM(credits_used_cloud_services + COALESCE(credits_used, 0)) AS total_credits,
    SUM(bytes_scanned) / 1e12 AS tb_scanned,
    AVG(DATEDIFF('second', start_time, end_time)) AS avg_exec_seconds
FROM snowflake.account_usage.query_history
WHERE start_time > CURRENT_DATE - INTERVAL '30 days'
GROUP BY 1, 2, 3
ORDER BY total_credits DESC;
```

### Recipe 3 — Warehouse load + concurrency analysis

```sql
SELECT
    warehouse_name,
    DATE_TRUNC('hour', start_time) AS hour_bucket,
    AVG(avg_running) AS avg_concurrency,
    MAX(avg_running) AS max_concurrency,
    AVG(avg_queued_load) AS avg_queued
FROM snowflake.account_usage.warehouse_load_history
WHERE start_time > CURRENT_DATE - INTERVAL '7 days'
GROUP BY 1, 2
ORDER BY 1, 2;

-- If avg_queued > 0.5, consider multi-cluster
-- If max_concurrency < 1, the warehouse is oversized
```

### Recipe 4 — Auto-suspend optimization

```sql
-- Find warehouses with high idle time
WITH suspend_intervals AS (
    SELECT warehouse_name, start_time, end_time, EVENT_NAME
    FROM snowflake.account_usage.warehouse_events_history
    WHERE start_time > CURRENT_DATE - INTERVAL '7 days'
      AND EVENT_NAME IN ('SUSPEND_WAREHOUSE', 'RESUME_WAREHOUSE')
)
-- Compute time spent running but idle
-- (complex — for production use Snowsight's warehouse insights instead)
SELECT warehouse_name, COUNT(*) AS toggle_count
FROM suspend_intervals GROUP BY 1 ORDER BY toggle_count DESC;
```

Tune auto-suspend:

```sql
-- Tight (default): suspend after 60s idle
ALTER WAREHOUSE compute_wh SET AUTO_SUSPEND = 60;
-- Loose (spiky workloads): suspend after 5 min idle
ALTER WAREHOUSE etl_wh SET AUTO_SUSPEND = 300;
-- Aggressive (interactive BI): suspend after 30s
ALTER WAREHOUSE bi_wh SET AUTO_SUSPEND = 30;
```

### Recipe 5 — Query Acceleration Service eligibility

```sql
-- Find queries that would benefit from QAS
SELECT
    query_id,
    query_text,
    bytes_scanned / 1e9 AS gb_scanned,
    eligible_query_acceleration_time,
    upper_limit_scale_factor
FROM snowflake.account_usage.query_acceleration_eligible
WHERE start_time > CURRENT_DATE - INTERVAL '7 days'
ORDER BY eligible_query_acceleration_time DESC
LIMIT 20;

-- Enable QAS on the warehouse
ALTER WAREHOUSE compute_wh SET QUERY_ACCELERATION_MAX_SCALE_FACTOR = 8;
```

## Common recipes — BigQuery

### Recipe 6 — BigQuery slot + cost analysis

```sql
SELECT
    user_email,
    project_id,
    SUBSTR(query, 1, 200) AS query_text,
    creation_time,
    total_slot_ms / 1000.0 / 3600 AS slot_hours,
    total_bytes_processed / 1e9 AS gb_processed,
    total_bytes_billed / 1e9 AS gb_billed,
    -- On-demand pricing: $5/TB billed (2025)
    total_bytes_billed / 1e12 * 5 AS estimated_cost_usd,
    state
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND job_type = 'QUERY'
  AND state = 'DONE'
ORDER BY total_slot_ms DESC
LIMIT 50;
```

### Recipe 7 — BigQuery slot reservation usage

```sql
SELECT
    reservation_id,
    DATE(period_start) AS day,
    SUM(slots_assigned) AS total_slot_seconds_assigned,
    SUM(slots_used) AS total_slot_seconds_used,
    SAFE_DIVIDE(SUM(slots_used), SUM(slots_assigned)) AS utilization_pct
FROM `region-us`.INFORMATION_SCHEMA.RESERVATIONS_TIMELINE
WHERE period_start > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
GROUP BY 1, 2
ORDER BY 1, 2;
```

### Recipe 8 — Partition pruning effectiveness

```sql
-- Find queries that did not benefit from partition pruning
SELECT
    SUBSTR(query, 1, 200) AS query,
    user_email,
    referenced_tables[OFFSET(0)].dataset_id AS dataset,
    referenced_tables[OFFSET(0)].table_id AS table,
    total_bytes_processed / 1e9 AS gb_processed,
    statement_type
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT,
UNNEST(referenced_tables) AS rt
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
  AND total_bytes_processed > 100e9            -- scanned > 100GB
  AND statement_type = 'SELECT'
ORDER BY total_bytes_processed DESC LIMIT 20;
```

For each result, check if a partition filter would help; add `WHERE order_date BETWEEN ...` clause.

### Recipe 9 — Materialized view candidates

```sql
-- Find frequently-repeated queries — MV candidates
SELECT
    SUBSTR(query, 1, 100) AS query_pattern,
    COUNT(*) AS exec_count,
    SUM(total_bytes_processed) / 1e9 AS total_gb_processed,
    AVG(total_slot_ms) AS avg_slot_ms
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND job_type = 'QUERY'
GROUP BY 1
HAVING exec_count > 100
ORDER BY total_gb_processed DESC LIMIT 20;
```

Create MV:

```sql
CREATE MATERIALIZED VIEW my_dataset.mv_daily_revenue
PARTITION BY order_date
CLUSTER BY region AS
SELECT order_date, region, SUM(amount) AS revenue
FROM my_dataset.fct_orders
GROUP BY 1, 2;
```

## Common recipes — Databricks

### Recipe 10 — Databricks DBU consumption (system tables)

```sql
SELECT
    workspace_id,
    sku_name,
    DATE(usage_date) AS usage_day,
    SUM(usage_quantity) AS dbu_consumed,
    SUM(usage_quantity * list_prices.pricing.default) AS estimated_cost_usd
FROM system.billing.usage u
JOIN system.billing.list_prices ON u.sku_name = list_prices.sku_name AND CURRENT_DATE() BETWEEN list_prices.price_start_time AND COALESCE(list_prices.price_end_time, '2999-12-31')
WHERE usage_date >= current_date - INTERVAL 7 DAYS
GROUP BY 1, 2, 3
ORDER BY estimated_cost_usd DESC;
```

```sql
-- Most expensive queries
SELECT
    statement_id,
    executed_by,
    start_time,
    end_time,
    total_duration_ms / 1000 AS exec_seconds,
    total_task_duration_ms / 1000 AS task_seconds,
    read_bytes / 1e9 AS gb_read,
    statement_text
FROM system.query.history
WHERE start_time >= current_timestamp() - INTERVAL 7 DAYS
ORDER BY total_task_duration_ms DESC
LIMIT 20;
```

## Recipe 11 — dbt materialization audit

```python
import json
from pathlib import Path

# Read dbt manifest.json after `dbt parse`
manifest = json.loads(Path("target/manifest.json").read_text())

models = []
for node_id, node in manifest["nodes"].items():
    if node["resource_type"] == "model":
        models.append({
            "model": node["name"],
            "materialization": node["config"]["materialized"],
            "tags": node["tags"],
            "path": node["path"],
        })

import pandas as pd
df = pd.DataFrame(models)
print(df.materialization.value_counts())

# For "table" models that are large + append-only, consider incremental
# For "incremental" models with small dataset, downgrade to "table"
# For models referenced only once, consider "ephemeral"
```

## Recipe 12 — Cost monitoring dashboard

```sql
-- Daily credit/slot/DBU dashboard query
SELECT
    DATE_TRUNC('day', start_time) AS day,
    warehouse_name,
    SUM(credits_used_cloud_services + COALESCE(credits_used, 0)) AS credits,
    COUNT(*) AS query_count,
    AVG(DATEDIFF('second', start_time, end_time)) AS avg_exec_seconds
FROM snowflake.account_usage.query_history
WHERE start_time > CURRENT_DATE - INTERVAL '30 days'
GROUP BY 1, 2
ORDER BY 1, 2;
```

Then dashboard via Metabase/Hex/Evidence with anomaly alerts (Recipe 13).

## Recipe 13 — Cost anomaly alert

```python
import pandas as pd

def cost_anomaly_check(daily_credits_series, k_sigma=2.5):
    """Alert when today's credits are >k_sigma above 28-day rolling mean."""
    rolling = daily_credits_series.rolling(28, min_periods=7)
    mean = rolling.mean()
    std = rolling.std()
    z = (daily_credits_series - mean) / std
    return daily_credits_series[z > k_sigma].index.tolist()

anomalies = cost_anomaly_check(df.set_index("day")["credits"])
if anomalies:
    print(f"COST SPIKE on: {anomalies}")
```

## Example end-to-end

**Goal:** Snowflake bill jumped from $8k to $13k in May. Diagnose + fix.

1. Run Recipe 1 → top-20 expensive queries; spot a 4× spike from `MARKETING_WH`.
2. Recipe 2: drill into `MARKETING_WH` — most credits from `bi_user@company.com`.
3. Inspect query: a Looker dashboard query scanning `fct_events` without partition filter; runs every 5 minutes.
4. Recipe 3: `MARKETING_WH` has `avg_concurrency = 0.3`, `max_queue = 0` → oversized at L; downsize to S.
5. Add `WHERE event_date >= CURRENT_DATE - 7` to Looker LookML; verify pruning via Snowsight Query Profile.
6. Recipe 9: query is repeated → create materialized view `mv_daily_event_summary`.
7. Recipe 11: audit dbt; `fct_events` is `table` but should be `incremental` on `event_date`.
8. Save: Snowflake bill projected $7k for next month.
9. Set up Recipe 12 + 13 dashboard + Slack alert for future spikes.

## Edge cases / gotchas

- **`QUERY_HISTORY` has 45-min lag** — for real-time, use `INFORMATION_SCHEMA.QUERY_HISTORY` (current session) or Snowflake events.
- **`credits_used = NULL` for cached results** — those don't cost compute; filter `credits_used > 0` for cost analysis only.
- **BigQuery on-demand vs reservations** — on-demand bills per TB scanned ($5/TB 2025); reservations bill per slot-hour. Different cost equations.
- **BigQuery `total_bytes_billed` vs `total_bytes_processed`** — billed = processed rounded up to 10MB; on cached/canceled queries billed=0.
- **Auto-suspend too short** — sub-60s causes cold-start cost > savings; tune per workload.
- **Multi-cluster ≠ bigger warehouse** — multi-cluster adds concurrency (more queries in parallel); larger size adds power (each query runs faster). Don't conflate.
- **dbt incremental backfill costs** — first-run is full-refresh; budget the one-time cost.
- **Materialized views autosync** — Snowflake MV maintenance has credit cost; only worth it if MV is queried frequently.
- **Result cache hits don't show in QUERY_HISTORY as expensive** — they're free; if a query is "expensive" only sometimes, cache miss vs hit pattern.
- **Reserved slot waste** — BigQuery reserved capacity bills 100% even at 10% utilization; right-size monthly.
- **Cluster keys vs partition keys (BigQuery)** — partition for date (cardinality ≤4000); cluster for high-cardinality filters (customer_id).
- **`COMPUTE_WH` shared default warehouse** — if all users default to same warehouse, you can't attribute. Per-role/team warehouses help attribution.

## Sources

- [Snowflake — QUERY_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/query_history)
- [Snowflake — WAREHOUSE_LOAD_HISTORY](https://docs.snowflake.com/en/sql-reference/account-usage/warehouse_load_history)
- [Snowflake — Query Acceleration Service](https://docs.snowflake.com/en/user-guide/query-acceleration-service)
- [BigQuery — INFORMATION_SCHEMA.JOBS](https://cloud.google.com/bigquery/docs/information-schema-jobs)
- [BigQuery — slot reservations](https://cloud.google.com/bigquery/docs/reservations-intro)
- [BigQuery — materialized views](https://cloud.google.com/bigquery/docs/materialized-views-intro)
- [Databricks — System tables](https://docs.databricks.com/admin/system-tables/index.html)
- [Databricks — Query history](https://docs.databricks.com/sql/admin/query-history.html)
- [Snowflake cost optimization guide 2025](https://www.snowflake.com/en/blog/cost-optimization/)
- role.md → "Warehouse cost playbook"
