<!--
Polars: https://pola.rs/
pandas: https://pandas.pydata.org/docs/
Ibis: https://ibis-project.org/
Companion: role.md → "Capability reference → Dataframe libraries"
-->

# Polars + pandas 2.x + Ibis — modern Python dataframes

Use Polars for >1GB / multi-core dataframes (Rust-backed, lazy, deterministic), pandas 2.x with PyArrow backend for legacy compatibility, and Ibis when you want to write code once and execute against any backend (Polars / pandas / DuckDB / Snowflake / BigQuery / Spark).

## When to use

- "Process this 5GB CSV / Parquet" → Polars (lazy + parallel)
- "Quick analysis matches pandas tutorials" → pandas 2.x (PyArrow + CoW)
- "Code needs to run against multiple warehouses without rewrite" → Ibis
- "I'm joining + aggregating > memory" → Polars streaming or DuckDB
- "Existing pandas code is slow" → port to Polars (90% API parity for analytics workflows)

Defer SQL-only workflows to warehouse skills. Defer distributed (TB-scale) to Spark / Ray.

## Setup

```bash
pip install polars                      # ~30MB; includes Arrow + parquet
pip install pandas pyarrow              # pandas 2.x with PyArrow backend
pip install 'ibis-framework[duckdb,snowflake,bigquery,polars]'   # backends as needed
```

No auth for local; backends inherit warehouse credentials.

## When to pick which

| Need | Polars | pandas | Ibis |
|---|---|---|---|
| <100MB dataset | OK | best ergonomics | overkill |
| >1GB dataset | best | OOM risk | depends on backend |
| Lazy / query optimization | yes | no | yes (compiles to SQL) |
| Multi-core | yes (auto) | no (single core) | depends on backend |
| Streaming larger-than-RAM | yes | no | backend-dependent |
| Run on warehouse | no (export first) | no | yes (native) |
| Sklearn / ML library compatibility | via `.to_numpy()` | native | via Polars / pandas backend |
| Familiar API | needs learning | most familiar | new |

## Common recipes — Polars

### Recipe 1 — Read, transform, write

```python
import polars as pl

# Eager
df = pl.read_parquet("orders.parquet")
df.filter(pl.col("amount") > 100).group_by("customer_id").agg(
    pl.col("amount").sum().alias("revenue"),
    pl.col("order_id").count().alias("orders"),
).sort("revenue", descending=True).write_parquet("customer_summary.parquet")

# Lazy (recommended for >100MB) — query plan optimized + executed in one shot
result = (
    pl.scan_parquet("data/orders/*.parquet")
      .filter(pl.col("status") == "paid")
      .group_by([pl.col("customer_id"), pl.col("order_date").dt.month_start().alias("month")])
      .agg(pl.col("amount").sum().alias("revenue"))
      .sort(["customer_id", "month"])
      .collect(streaming=True)        # streaming engine for larger-than-RAM
)
```

### Recipe 2 — Joins + window functions

```python
import polars as pl

orders = pl.scan_parquet("orders.parquet")
customers = pl.scan_parquet("customers.parquet")

result = (
    orders.join(customers, on="customer_id", how="left")
          .with_columns(
              # Running total per customer
              pl.col("amount")
                .cum_sum()
                .over("customer_id", order_by="order_date")
                .alias("lifetime_revenue"),
              # Rank within day
              pl.col("amount")
                .rank(method="dense", descending=True)
                .over("order_date")
                .alias("daily_rank"),
          )
          .collect()
)
```

### Recipe 3 — Polars expression API (composable)

```python
# Expressions are first-class — compose without re-querying
revenue_expr = pl.col("amount") * pl.col("quantity")
margin_expr = (revenue_expr - pl.col("cost")) / revenue_expr

df.with_columns(
    revenue=revenue_expr,
    margin=margin_expr,
    high_margin=margin_expr > 0.5,
)

# Conditional logic (when/then/otherwise)
df.with_columns(
    segment=pl.when(pl.col("revenue") > 10_000).then(pl.lit("whale"))
              .when(pl.col("revenue") > 1_000).then(pl.lit("regular"))
              .otherwise(pl.lit("casual"))
)
```

### Recipe 4 — Pivots + unpivots

```python
# Wide pivot
wide = df.pivot(index="customer_id", on="month", values="revenue", aggregate_function="sum")

# Long unpivot
long = wide.unpivot(index="customer_id", variable_name="month", value_name="revenue")
```

### Recipe 5 — Date handling

```python
df.with_columns(
    pl.col("order_date").dt.year().alias("year"),
    pl.col("order_date").dt.month_start().alias("month"),
    pl.col("order_date").dt.weekday().alias("dow"),
    days_since_signup=(pl.col("order_date") - pl.col("signup_date")).dt.total_days(),
)

# Date range
pl.date_range(date(2025, 1, 1), date(2025, 12, 31), interval="1d", eager=True)
```

## Common recipes — pandas 2.x

### Recipe 6 — PyArrow backend + Copy-on-Write

```python
import pandas as pd

# Set globally
pd.options.mode.copy_on_write = True            # opt-in CoW — eliminates SettingWithCopyWarning

# Read with PyArrow backend (faster, lower memory)
df = pd.read_parquet("orders.parquet", dtype_backend="pyarrow")
df = pd.read_csv("orders.csv", engine="pyarrow", dtype_backend="pyarrow")

# Or per-DataFrame
df = pd.DataFrame({"x": [1, 2, 3]}, dtype="int64[pyarrow]")

# Nullable types (no NaN-coercion of integers)
df = pd.read_csv("orders.csv", dtype_backend="numpy_nullable")
```

### Recipe 7 — pandas → Polars + back

```python
import pandas as pd
import polars as pl

# pandas → polars (zero-copy via Arrow when possible)
pdf = pd.read_csv("data.csv")
pldf = pl.from_pandas(pdf)

# polars → pandas
back = pldf.to_pandas(use_pyarrow_extension_array=True)
```

### Recipe 8 — DuckDB ↔ pandas/Polars zero-copy

```python
import duckdb

# Query a DataFrame directly
df_pandas = pd.read_csv("data.csv")
duckdb.query("SELECT region, sum(amount) FROM df_pandas GROUP BY 1").pl()

df_polars = pl.read_parquet("data.parquet")
duckdb.query("SELECT region, sum(amount) FROM df_polars GROUP BY 1").pl()
```

## Common recipes — Ibis

### Recipe 9 — Write once, run on any backend

```python
import ibis

# Backend = DuckDB local
con = ibis.duckdb.connect("analytics.duckdb")

# Backend = Snowflake (same code below)
# con = ibis.snowflake.connect(account=..., user=..., password=...)

orders = con.table("orders")
customers = con.table("customers")

result = (
    orders.left_join(customers, "customer_id")
          .filter(orders.amount > 100)
          .group_by([orders.customer_id, orders.order_date.month()])
          .aggregate(
              revenue=orders.amount.sum(),
              orders=orders.order_id.count(),
          )
          .order_by(ibis.desc("revenue"))
          .limit(100)
)

# Materialize (compiles to backend SQL, executes, returns DataFrame)
df = result.execute()              # → pandas DataFrame
df = result.to_polars()            # → Polars DataFrame
print(ibis.to_sql(result))         # inspect generated SQL per backend
```

### Recipe 10 — Ibis + dbt for re-usable analytics

```python
# Models defined in Python (reusable across DuckDB + Snowflake)
def customer_cohort_retention(con):
    orders = con.table("orders")
    cohorts = orders.group_by("customer_id").aggregate(
        cohort_month=orders.order_date.truncate("M").min(),
    )
    return (
        orders.left_join(cohorts, "customer_id")
              .group_by([cohorts.cohort_month,
                         (orders.order_date - cohorts.cohort_month).months().name("months_since")])
              .aggregate(active_users=orders.customer_id.nunique())
    )

# Execute on DuckDB for prototyping
local = ibis.duckdb.connect("analytics.duckdb")
df_prototype = customer_cohort_retention(local).execute()

# Same code on Snowflake for production
prod = ibis.snowflake.connect(...)
df_prod = customer_cohort_retention(prod).execute()
```

## Example end-to-end

**Goal:** Compute monthly cohort retention from 3GB of order Parquet files; export to CSV for stakeholders.

1. Use Polars lazy: `lf = pl.scan_parquet("orders/*.parquet")`.
2. Extract cohort month: `cohort = lf.group_by("customer_id").agg(pl.col("order_date").min().alias("cohort"))`.
3. Join back and compute months-since-cohort:
   ```python
   retention = (
       lf.join(cohort, on="customer_id")
         .with_columns(
             cohort_month=pl.col("cohort").dt.month_start(),
             months_since=((pl.col("order_date").dt.year() - pl.col("cohort").dt.year()) * 12
                           + (pl.col("order_date").dt.month() - pl.col("cohort").dt.month())),
         )
         .group_by(["cohort_month", "months_since"])
         .agg(pl.col("customer_id").n_unique().alias("active_users"))
         .sort(["cohort_month", "months_since"])
   )
   ```
4. `wide = retention.collect(streaming=True).pivot(index="cohort_month", on="months_since", values="active_users")`.
5. `wide.write_csv("cohort_retention.csv")`.

Total: ~10s on a laptop for 3GB input.

## Edge cases / gotchas

- **Polars vs pandas null semantics** — Polars has `null` (proper SQL semantics); pandas has `NaN` (sentinel that breaks integer types). Polars wins for analytics correctness.
- **Polars `.collect()` is the materialization step** — operating on a `LazyFrame` always returns another `LazyFrame`. Forgetting `.collect()` returns a query plan, not data.
- **`streaming=True` semantics** — only works for ops that can be streamed (filter/select/aggregate). Joins of two large frames may still need RAM.
- **pandas CoW behavior change** — without `copy_on_write = True`, view-vs-copy is implicit; with it, you must explicitly `.copy()` if you need an independent frame. Pandas 3.0 will make CoW default.
- **PyArrow backend missing methods** — some pandas methods aren't implemented on PyArrow-backed series (`.str.normalize()` etc.). Fall back to NumPy-backed for affected ops.
- **Polars `over()` requires an order** — for windowed sums, specify `order_by=` to make results deterministic.
- **Polars datetime precision** — defaults to microseconds; explicit `time_unit="ns"` when interfacing with pandas (which uses ns).
- **Ibis compile-vs-execute** — `result.compile()` returns the SQL but doesn't run it. `result.execute()` runs. Use `compile()` to inspect cost before running on warehouse.
- **Ibis function support varies by backend** — `.array_*()` works on Snowflake/DuckDB but not Postgres. Check via `ibis.backends.<backend>.has_operation(op)`.
- **Memory monitoring** — Polars: `pl.Config.set_tbl_rows(20)` for nice display; for memory: pass `--show-memory` to Python via `tracemalloc`.
- **Polars `set_random_seed`** — `pl.set_random_seed(42)` for reproducible sampling.

## Sources

- [Polars user guide](https://docs.pola.rs/user-guide/)
- [Polars API reference](https://docs.pola.rs/api/python/stable/reference/)
- [pandas 2.x Copy-on-Write](https://pandas.pydata.org/docs/user_guide/copy_on_write.html)
- [pandas PyArrow backend](https://pandas.pydata.org/docs/user_guide/pyarrow.html)
- [Ibis documentation](https://ibis-project.org/)
- [Ibis backend matrix](https://ibis-project.org/support_matrix)
- [Polars vs pandas vs DuckDB benchmarks 2025](https://pola.rs/posts/benchmarks/)
- role.md → "Capability reference → Dataframe libraries"
