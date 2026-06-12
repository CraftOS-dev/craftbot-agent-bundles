<!--
Snowflake: https://docs.snowflake.com/
BigQuery: https://cloud.google.com/bigquery/docs
Databricks SQL: https://docs.databricks.com/sql/
Companion playbook: role.md → "Warehouse dialect cheat sheet" + "SQL refactor playbook"
-->

# Snowflake / BigQuery / Databricks — warehouse SDK + dialect patterns

Connect to each major warehouse, write idiomatic SQL per dialect, profile via EXPLAIN + native query history, and apply partitioning / clustering for performance. Use `sqlglot` for dialect transpilation when porting queries.

## When to use

- "Write Snowflake SQL for X" / "convert this BigQuery query to Databricks" / "why is this query slow on Redshift"
- New warehouse credentials need a connection test
- Cross-dialect porting (transpile via sqlglot, then hand-tune)
- Performance debugging — read the query profile / execution plan
- Pick the right partitioning + clustering strategy for a new fact table

Defer cost analytics + credit/slot attribution to `warehouse-cost-optimization-snowflake-bq`. Defer dbt-specific patterns to `dbt-modeling-staging-marts`. Defer local prototyping to `duckdb-motherduck-local-olap`.

## Setup

```bash
# Snowflake
pip install snowflake-connector-python snowflake-sqlalchemy

# BigQuery
pip install google-cloud-bigquery google-cloud-bigquery-storage pandas-gbq

# Databricks SQL
pip install databricks-sql-connector databricks-sdk

# Redshift
pip install redshift_connector

# Transpiler + linter
pip install sqlglot sqlfluff
```

Auth requirements:
- Snowflake: account + user + role + warehouse + database. Recommended: key-pair auth (`SNOWFLAKE_PRIVATE_KEY_PATH`) or OAuth, not password.
- BigQuery: service-account JSON via `GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json` or ADC (`gcloud auth application-default login`).
- Databricks: host + HTTP path + personal access token (`DATABRICKS_TOKEN`); or OAuth M2M.
- Redshift: username/password or IAM-based via `iam_role` parameter.

## Common recipes

### Recipe 1 — Snowflake connection + query

```python
import snowflake.connector

conn = snowflake.connector.connect(
    account="ab12345.us-east-1",
    user="analyst",
    password=os.environ["SNOWFLAKE_PASSWORD"],   # or private_key for key-pair
    warehouse="COMPUTE_WH",
    database="ANALYTICS",
    schema="MARTS",
    role="ANALYST_ROLE",
)

cur = conn.cursor()
cur.execute("USE WAREHOUSE COMPUTE_WH")
df = cur.execute("""
    SELECT customer_id, COUNT(*) AS orders
    FROM fct_orders
    WHERE order_date >= DATEADD(day, -30, CURRENT_DATE)
    GROUP BY 1
    QUALIFY ROW_NUMBER() OVER (ORDER BY orders DESC) <= 100
""").fetch_pandas_all()
```

`fetch_pandas_all()` uses Arrow under the hood — faster than `fetchall()` for large results.

### Recipe 2 — BigQuery connection + query

```python
from google.cloud import bigquery

client = bigquery.Client(project="my-project")

query = """
WITH ranked AS (
  SELECT
    customer_id,
    COUNT(*) AS orders,
    ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS rn
  FROM `my-project.marts.fct_orders`
  WHERE order_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  GROUP BY 1
)
SELECT * FROM ranked WHERE rn <= 100
"""

df = client.query(query).to_dataframe(create_bqstorage_client=True)   # BQ Storage API → faster
```

### Recipe 3 — Databricks SQL connection + query

```python
from databricks import sql

with sql.connect(
    server_hostname=os.environ["DATABRICKS_SERVER_HOSTNAME"],
    http_path=os.environ["DATABRICKS_HTTP_PATH"],    # /sql/1.0/warehouses/abc123
    access_token=os.environ["DATABRICKS_TOKEN"],
) as conn:
    df = conn.cursor().execute("""
        SELECT customer_id, COUNT(*) AS orders
        FROM marts.fct_orders
        WHERE order_date >= date_sub(current_date(), 30)
        GROUP BY 1
        QUALIFY row_number() OVER (ORDER BY orders DESC) <= 100
    """).fetchall_arrow().to_pandas()
```

### Recipe 4 — Dialect dictionary (most-confused operations)

| Operation | Snowflake | BigQuery | Databricks | Redshift |
|---|---|---|---|---|
| Current date | `CURRENT_DATE` | `CURRENT_DATE()` | `current_date()` | `CURRENT_DATE` |
| Date - N days | `DATEADD(day, -N, d)` | `DATE_SUB(d, INTERVAL N DAY)` | `date_sub(d, N)` | `DATEADD(day, -N, d)` |
| Date diff | `DATEDIFF('day', a, b)` | `DATE_DIFF(b, a, DAY)` | `datediff(b, a)` | `DATEDIFF('day', a, b)` |
| Date trunc | `DATE_TRUNC('week', d)` | `DATE_TRUNC(d, WEEK)` | `date_trunc('week', d)` | `DATE_TRUNC('week', d)` |
| String concat | `||` or `CONCAT` | `||` or `CONCAT` | `||` or `concat()` | `||` |
| Array agg | `ARRAY_AGG(x)` | `ARRAY_AGG(x)` | `collect_list(x)` | `LISTAGG(x, ',')` (string only) |
| Median | `MEDIAN(x)` | `APPROX_QUANTILES(x, 100)[OFFSET(50)]` | `percentile(x, 0.5)` | `PERCENTILE_CONT(0.5)` |
| QUALIFY | yes | yes | yes | no (wrap in CTE + WHERE on row_number) |
| Lateral flatten | `LATERAL FLATTEN(input => arr)` | `UNNEST(arr)` | `LATERAL VIEW EXPLODE(arr)` | `JSON_EXTRACT_ARRAY_TEXT` |
| Pivot | native `PIVOT` | manual `CASE WHEN` | native `pivot` | manual |
| String → array | `STRTOK_TO_ARRAY(s, ',')` | `SPLIT(s, ',')` | `split(s, ',')` | `SPLIT_TO_ARRAY(s, ',')` |
| Generate dates | `GENERATOR(ROWCOUNT=>n)` + DATEADD | `GENERATE_DATE_ARRAY` | `sequence(d1, d2)` | recursive CTE |

### Recipe 5 — sqlglot transpilation

```python
import sqlglot

src = """
SELECT
  customer_id,
  DATE_TRUNC('week', order_date) AS week,
  COUNT(*) AS orders
FROM fct_orders
WHERE order_date >= DATEADD(day, -30, CURRENT_DATE)
GROUP BY 1, 2
QUALIFY ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY week DESC) = 1
"""

print(sqlglot.transpile(src, read="snowflake", write="bigquery", pretty=True)[0])
# DATE_TRUNC becomes DATE_TRUNC(order_date, WEEK)
# DATEADD becomes DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)
# QUALIFY preserved

print(sqlglot.transpile(src, read="snowflake", write="redshift", pretty=True)[0])
# Redshift has no QUALIFY → sqlglot rewrites as subquery
```

### Recipe 6 — EXPLAIN + query profile

```sql
-- Snowflake: profile a query (post-execution)
SELECT * FROM TABLE(GET_QUERY_OPERATOR_STATS(LAST_QUERY_ID()));

-- Snowflake: pre-execution plan
EXPLAIN USING TEXT SELECT ...;

-- BigQuery: dry-run estimate (free, no execution)
client.query(sql, job_config=bigquery.QueryJobConfig(dry_run=True))
# Look at job.total_bytes_processed for cost estimate

-- Databricks: EXPLAIN EXTENDED for SparkSQL plan
EXPLAIN EXTENDED SELECT ...;

-- Redshift
EXPLAIN SELECT ...;
SELECT * FROM SVL_QUERY_REPORT WHERE query = <query_id>;
```

### Recipe 7 — Partitioning + clustering

```sql
-- Snowflake: clustering key (auto-managed)
CREATE TABLE fct_orders (
    order_id INT,
    order_date DATE,
    customer_id INT,
    amount FLOAT
)
CLUSTER BY (order_date, customer_id);

ALTER TABLE fct_orders CLUSTER BY (order_date);   -- recluster

-- BigQuery: partition by date + cluster by frequent filter cols
CREATE TABLE my_dataset.fct_orders (
    order_id INT64,
    order_date DATE,
    customer_id INT64,
    amount FLOAT64
)
PARTITION BY order_date
CLUSTER BY customer_id, status
OPTIONS (
    partition_expiration_days = 365,
    require_partition_filter = true       -- enforces partition filter in queries (cost control)
);

-- Databricks (Delta): partition + Z-order
CREATE TABLE marts.fct_orders (
    order_id BIGINT,
    order_date DATE,
    customer_id BIGINT,
    amount DOUBLE
)
USING DELTA
PARTITIONED BY (order_date);

OPTIMIZE marts.fct_orders ZORDER BY (customer_id);

-- Redshift: distkey + sortkey
CREATE TABLE fct_orders (
    order_id BIGINT,
    order_date DATE,
    customer_id BIGINT ENCODE az64,
    amount FLOAT ENCODE az64
)
DISTKEY(customer_id)
SORTKEY(order_date);
```

Rules of thumb:
- **Partition by date** (most common filter), **cluster by ID** (most common join key).
- Partition cardinality ≤ ~4000 (BigQuery limit ~4000 daily for 11 years).
- Snowflake auto-clustering kicks in when table is sufficiently fragmented; check `SYSTEM$CLUSTERING_INFORMATION('table')`.

### Recipe 8 — Window functions (cross-dialect)

```sql
-- Lag / lead — same syntax across all
SELECT
    user_id,
    order_date,
    amount,
    LAG(amount) OVER (PARTITION BY user_id ORDER BY order_date) AS prev_amount,
    LEAD(amount, 1) OVER (PARTITION BY user_id ORDER BY order_date) AS next_amount,
    SUM(amount) OVER (PARTITION BY user_id ORDER BY order_date
                      ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS rolling_7
FROM fct_orders;

-- First-value per customer (uses QUALIFY where supported)
SELECT user_id, order_id, order_date
FROM fct_orders
QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date) = 1;
-- Redshift equivalent:
SELECT * FROM (
    SELECT user_id, order_id, order_date,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date) AS rn
    FROM fct_orders
) WHERE rn = 1;
```

### Recipe 9 — JSON / semi-structured (Snowflake VARIANT, BQ STRUCT, Databricks struct)

```sql
-- Snowflake VARIANT
SELECT
    event_id,
    payload:user_id::INT       AS user_id,
    payload:context.utm:source::STRING AS utm_source,
    payload:tags                AS tags_array
FROM raw_events;

-- BigQuery JSON
SELECT
    event_id,
    CAST(JSON_VALUE(payload, '$.user_id') AS INT64) AS user_id,
    JSON_VALUE(payload, '$.context.utm.source') AS utm_source
FROM raw_events;

-- Databricks (Delta)
SELECT
    event_id,
    payload:user_id::int AS user_id,
    payload:context.utm.source::string AS utm_source
FROM raw_events;
```

### Recipe 10 — Warehouse-specific scaling

```sql
-- Snowflake: resize warehouse for one query
ALTER WAREHOUSE compute_wh SET WAREHOUSE_SIZE = 'LARGE';
-- (after query)
ALTER WAREHOUSE compute_wh SET WAREHOUSE_SIZE = 'SMALL';

-- Multi-cluster (concurrency, not power)
ALTER WAREHOUSE compute_wh SET MIN_CLUSTER_COUNT = 1, MAX_CLUSTER_COUNT = 4;

-- BigQuery: reservation-based slot allocation (flat-rate only)
CREATE RESERVATION analytics_res OPTIONS (slot_capacity = 500);
ALTER ASSIGNMENT analytics_res ASSIGN PROJECT my-project;

-- Databricks: scale SQL warehouse
-- via API:
curl -X PATCH -H "Authorization: Bearer $DATABRICKS_TOKEN" \
  "$DATABRICKS_HOST/api/2.0/sql/warehouses/$WAREHOUSE_ID" \
  -d '{"cluster_size":"LARGE","min_num_clusters":1,"max_num_clusters":4}'
```

## Example end-to-end

**Goal:** New Snowflake mart `fct_subscription_revenue` queries slowly.

1. Identify the slow query in `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY` (top by `total_elapsed_time`).
2. Run `EXPLAIN USING TEXT` to inspect plan; spot full table scan.
3. Check clustering: `SELECT SYSTEM$CLUSTERING_INFORMATION('marts.fct_subscription_revenue', '(month_start)')`.
4. If `average_depth` > 3, re-cluster: `ALTER TABLE marts.fct_subscription_revenue CLUSTER BY (month_start)`.
5. Add `month_start >= ...` predicate to query to enable pruning.
6. Re-run query; verify partitions pruned via `GET_QUERY_OPERATOR_STATS(LAST_QUERY_ID())`.
7. If still slow, materialize as a clustered table (currently view) and schedule incremental refresh.

## Edge cases / gotchas

- **Snowflake case sensitivity** — unquoted identifiers fold to UPPER; quoted preserve case. Always reference unquoted in dbt to avoid `"Order_ID"` mismatches.
- **BigQuery DML quotas** — 1500 UPDATE/DELETE per day per table on old API; use MERGE or partitioned-write patterns.
- **Databricks Photon vs classic engine** — Photon-enabled warehouses are ~3-4x faster for ANSI SQL but cost more credits; benchmark before defaulting.
- **Redshift sort key skew** — if all rows share one sort-key value, sorting buys nothing; choose high-cardinality sort key.
- **Snowflake auto-suspend** — set to 60s default; bump to 300s for spiky workloads to avoid cold-start cost.
- **BigQuery `require_partition_filter`** — without it, an analyst accidentally scanning a 10TB table costs $50. Always set.
- **Snowflake `QUERY_TAG`** — `ALTER SESSION SET QUERY_TAG = 'dashboard:exec_summary'`; lets you attribute cost back to consumer in `QUERY_HISTORY`.
- **`fetchall_arrow()` vs `fetch_pandas_all()`** — Arrow is faster + zero-copy; use when downstream is Polars/DuckDB.
- **BigQuery slot exhaustion** — flat-rate reservations queue queries when slots are saturated; check `INFORMATION_SCHEMA.RESERVATIONS_TIMELINE`.
- **Cross-region transfer cost** — querying us-east BQ dataset from eu-west region costs egress; co-locate data and compute.

## Sources

- [Snowflake Python connector](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector)
- [Snowflake SQL reference](https://docs.snowflake.com/en/sql-reference)
- [BigQuery Python client](https://cloud.google.com/python/docs/reference/bigquery/latest)
- [BigQuery partitioning + clustering](https://cloud.google.com/bigquery/docs/clustered-tables)
- [Databricks SQL connector for Python](https://docs.databricks.com/dev-tools/python-sql-connector.html)
- [Databricks Delta OPTIMIZE + Z-ORDER](https://docs.databricks.com/delta/optimize.html)
- [Redshift performance tuning](https://docs.aws.amazon.com/redshift/latest/dg/c-optimizing-query-performance.html)
- [sqlglot — dialect transpilation](https://sqlglot.com/sqlglot/dialects.html)
- role.md → "Warehouse dialect cheat sheet" + "SQL refactor playbook"
