<!--
DuckDB: https://duckdb.org/docs/
MotherDuck: https://motherduck.com/docs/
Companion: role.md → "Capability reference → DuckDB" + "SQL refactor playbook"
-->

# DuckDB + MotherDuck — local-first OLAP

Use DuckDB as the analyst's "embedded warehouse" for prototyping queries before promotion to Snowflake/BigQuery, for analyzing Parquet/CSV/JSON files in-place, and for joining cloud + local data via MotherDuck's hybrid execution. Drop-in SQL, single binary, zero infrastructure.

## When to use

- "I have a 5GB CSV — analyze it" / "join this S3 Parquet to my local data" / "prototype this SQL before running on Snowflake"
- Wholesale dataset arrived as 50 Parquet files — DuckDB reads `*.parquet` directly via glob
- Quick aggregations in a Jupyter / Marimo notebook without spinning up a warehouse
- CI test against a tiny dbt model — `dbt-duckdb` adapter runs offline
- One-off analysis where warehouse credentials are unavailable

Defer warehouse-grade queries to `snowflake-bigquery-databricks-warehousing`. Defer dataframe-level transforms to `polars-pandas-modern-dataframes`.

## Setup

```bash
# CLI binary
brew install duckdb               # macOS
# OR
curl -sSL https://install.duckdb.org | sh    # Linux
duckdb --version                  # verify 1.x

# Python library
pip install duckdb pyarrow         # + pyarrow for zero-copy Arrow integration

# dbt-duckdb adapter
pip install dbt-duckdb

# MotherDuck — cloud-managed DuckDB
# Sign up at app.motherduck.com → copy token
export motherduck_token="..."     # env var DuckDB reads automatically
```

Auth requirements:
- DuckDB local: none.
- MotherDuck: `motherduck_token` env var (free tier available).
- Reading from S3: `aws_access_key_id` / `aws_secret_access_key` env vars or `SET s3_*` in DuckDB.
- Reading from GCS: GCP service-account JSON; `SET s3_*` with GCS interop creds.

## Common recipes

### Recipe 1 — REPL + one-shot query

```bash
# Launch REPL on in-memory DB
duckdb
# > SELECT 1; .quit

# Launch on persistent file
duckdb ~/analytics.duckdb

# One-shot from shell
duckdb -c "SELECT count(*) FROM 'data/sales/*.parquet'"

# Run a SQL script
duckdb analytics.duckdb < query.sql
```

### Recipe 2 — Query Parquet / CSV / JSON in-place

```sql
-- Single file
SELECT customer_id, sum(amount) AS revenue
FROM 'data/orders.parquet'
GROUP BY 1
ORDER BY revenue DESC
LIMIT 10;

-- Glob across many files (parallel + pushdown)
SELECT date_trunc('month', order_date) AS month, sum(amount) AS revenue
FROM 'data/orders/year=2025/*.parquet'
GROUP BY 1;

-- Read with explicit schema + CSV options
SELECT * FROM read_csv(
    'sales.csv',
    delim=',',
    header=true,
    columns={'id':'INTEGER','amount':'DOUBLE','date':'DATE'},
    sample_size=-1
);

-- JSON (newline-delimited)
SELECT * FROM read_json_auto('events.jsonl', format='newline_delimited');

-- All files in S3
INSTALL httpfs; LOAD httpfs;
SET s3_region='us-east-1';
SET s3_access_key_id='...';
SET s3_secret_access_key='...';
SELECT count(*) FROM 's3://my-bucket/data/*.parquet';
```

### Recipe 3 — Python integration (zero-copy)

```python
import duckdb
import pandas as pd
import polars as pl

# Query a pandas DataFrame directly — DuckDB sees it as a table
df = pd.read_csv("sales.csv")
result = duckdb.query("SELECT region, sum(amount) FROM df GROUP BY 1").df()

# Query a Polars DataFrame
pl_df = pl.read_csv("sales.csv")
result = duckdb.query("SELECT region, sum(amount) FROM pl_df GROUP BY 1").pl()

# Persistent connection
con = duckdb.connect("analytics.duckdb")
con.execute("""
    CREATE OR REPLACE TABLE orders AS
    SELECT * FROM 'data/orders/*.parquet'
""")
con.execute("CREATE INDEX idx_orders_customer ON orders(customer_id)")
df_out = con.execute("SELECT * FROM orders WHERE customer_id = 42").pl()
con.close()
```

### Recipe 4 — Materialize a heavy query to a local table

```sql
-- One-time materialization of an expensive aggregation
CREATE TABLE customer_summary AS
SELECT
    customer_id,
    min(order_date) AS first_order,
    max(order_date) AS last_order,
    count(*) AS order_count,
    sum(amount) AS total_spend,
    avg(amount) AS avg_order_value
FROM 's3://bucket/orders/*.parquet'
GROUP BY customer_id;

-- Persist as Parquet for downstream consumers
COPY customer_summary TO 'output/customer_summary.parquet' (FORMAT PARQUET, COMPRESSION ZSTD);
```

### Recipe 5 — EXPLAIN + query profile

```sql
-- Logical plan
EXPLAIN
SELECT customer_id, sum(amount) FROM orders GROUP BY 1;

-- Execution stats (run + measure)
EXPLAIN ANALYZE
SELECT customer_id, sum(amount) FROM orders GROUP BY 1;

-- Inspect storage
PRAGMA storage_info('orders');
PRAGMA show_tables;
DESCRIBE orders;
SUMMARIZE orders;          -- column stats: min/max/distinct/null counts
```

### Recipe 6 — dbt-duckdb (test models locally before warehouse)

`profiles.yml`:

```yaml
analytics:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: ./analytics.duckdb
      threads: 4
      extensions: [httpfs, parquet]
```

Then `dbt build`. Iterate locally in seconds. CI runs against the same DuckDB target.

### Recipe 7 — MotherDuck hybrid execution

```sql
-- Connect from DuckDB CLI/Python to MotherDuck
ATTACH 'md:my_db';        -- env var motherduck_token must be set
USE my_db;

-- Now queries run in cloud
SELECT count(*) FROM big_cloud_table;

-- Hybrid: join cloud and local
SELECT c.customer_id, c.name, sum(o.amount)
FROM md:my_db.dim_customers c
JOIN 'local_orders.parquet' o ON c.customer_id = o.customer_id
GROUP BY 1, 2;

-- Share a db with a teammate
CREATE SHARE my_db_share FROM my_db;
GRANT USAGE ON SHARE my_db_share TO USER 'alice@company.com';
```

### Recipe 8 — Window + QUALIFY + PIVOT (full SQL coverage)

```sql
-- DuckDB supports QUALIFY, PIVOT, EXCLUDE/REPLACE
SELECT * EXCLUDE (raw_payload, _loaded_at)
FROM events
QUALIFY row_number() OVER (PARTITION BY user_id ORDER BY event_at DESC) = 1;

-- PIVOT (native)
PIVOT orders
ON status
USING sum(amount)
GROUP BY order_month;

-- Recursive CTE (date spine)
WITH RECURSIVE dates(d) AS (
    SELECT DATE '2025-01-01'
    UNION ALL
    SELECT d + INTERVAL '1 day' FROM dates WHERE d < DATE '2025-12-31'
)
SELECT * FROM dates;
```

### Recipe 9 — UDFs in Python

```python
import duckdb

def parse_user_agent(ua: str) -> str:
    if "Mobile" in (ua or ""): return "mobile"
    if "Tablet" in (ua or ""): return "tablet"
    return "desktop"

con = duckdb.connect()
con.create_function("device_class", parse_user_agent, ["VARCHAR"], "VARCHAR")
con.sql("SELECT device_class(user_agent), count(*) FROM events GROUP BY 1").show()
```

### Recipe 10 — Export to a warehouse (DuckDB → Snowflake)

```python
import duckdb
import snowflake.connector

con = duckdb.connect("analytics.duckdb")
arrow_table = con.execute("SELECT * FROM customer_summary").fetch_arrow_table()

sf = snowflake.connector.connect(**creds)
from snowflake.connector.pandas_tools import write_pandas
write_pandas(sf, arrow_table.to_pandas(), "CUSTOMER_SUMMARY",
             auto_create_table=True, overwrite=True)
```

For larger datasets: write Parquet from DuckDB, then `COPY INTO` from S3/stage on Snowflake side.

## Example end-to-end

**Goal:** Analyze 200 Parquet files in S3 with a 10GB join against local reference data, then promote the summary to Snowflake.

1. `INSTALL httpfs; LOAD httpfs; SET s3_*`.
2. `CREATE OR REPLACE VIEW raw_events AS SELECT * FROM 's3://bucket/events/year=2025/*.parquet';`
3. Load reference CSV: `CREATE TABLE dim_segments AS SELECT * FROM 'segments.csv';`
4. Run aggregation: `CREATE TABLE summary AS SELECT segment_id, count(*), sum(revenue) FROM raw_events JOIN dim_segments USING(user_id) GROUP BY 1;`
5. Profile: `EXPLAIN ANALYZE SELECT * FROM summary;` — verify Parquet pushdown + parallel scan.
6. Export: `COPY summary TO 's3://bucket/output/summary.parquet' (FORMAT PARQUET);`
7. Snowflake: `COPY INTO marts.event_summary FROM @my_s3_stage/output/summary.parquet`.

## Edge cases / gotchas

- **Memory pressure on local DuckDB** — DuckDB targets in-memory but spills to disk. Set `PRAGMA memory_limit = '8GB';` and ensure your `temp_directory` has space.
- **Parquet file glob ordering** — `*.parquet` is not ordered; if you need chronological order, add `ORDER BY` or include a date column in the schema.
- **CSV schema inference cost** — `sample_size=-1` reads the full file to infer types but is expensive on large files; specify `columns={...}` if known.
- **S3 region** — `SET s3_region` must match bucket region or requests are slow / fail.
- **MotherDuck token in URL** — `ATTACH 'md:?motherduck_token=...'` works but leaks the token in logs; use env var instead.
- **DuckDB versions are not wire-compatible** — `.duckdb` files written by 0.x can't be read by 1.x without conversion. Pin the version in CI.
- **`PIVOT` evaluates ON values at parse time** — values must be literal-deterministic; for dynamic pivots, use `PIVOT_WIDER` or build SQL programmatically.
- **`COPY ... (FORMAT PARQUET, ROW_GROUP_SIZE n)`** — default 122k rows; tune for downstream consumers (Snowflake prefers larger row groups).
- **dbt-duckdb concurrency** — single-writer; multiple `dbt run` processes against the same `.duckdb` file will collide. Use one-process-per-file pattern.
- **MotherDuck pricing tier limits** — free tier caps storage + compute hours; check usage at app.motherduck.com before promoting to production.
- **Locale-dependent CSV parsing** — `DATE` and `DECIMAL` inference can flip between US and EU formats; pass explicit `dateformat='%Y-%m-%d'`.

## Sources

- [DuckDB documentation](https://duckdb.org/docs/)
- [DuckDB SQL reference](https://duckdb.org/docs/sql/introduction)
- [DuckDB Python API](https://duckdb.org/docs/api/python/overview)
- [DuckDB httpfs (S3 / HTTP)](https://duckdb.org/docs/extensions/httpfs.html)
- [MotherDuck documentation](https://motherduck.com/docs/)
- [dbt-duckdb adapter](https://github.com/duckdb/dbt-duckdb)
- [DuckDB performance benchmarks 2025](https://duckdb.org/2025/03/duckdb-performance.html)
- role.md → "Capability reference → DuckDB"
