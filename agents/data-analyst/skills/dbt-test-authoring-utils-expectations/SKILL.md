<!--
Source: https://docs.getdbt.com/docs/build/data-tests
dbt-utils: https://github.com/dbt-labs/dbt-utils
dbt-expectations: https://github.com/calogica/dbt-expectations
Companion playbook: role.md → "dbt test catalog"
-->

# dbt tests — generic, singular, dbt-utils, dbt-expectations

Author and wire up dbt tests for column constraints, business invariants, freshness, and statistical-quality checks. Covers generic tests (built-in + dbt-utils + dbt-expectations), singular tests, source freshness, severity/store_failures, and CI integration.

## When to use

- "Add tests to dbt model X" / "fail the build when Y" / "alert on stale source"
- New model — every PK should have `unique` + `not_null`; every FK should have `relationships`
- Mart with revenue logic — assert `revenue >= 0`, `gross >= net`, business invariants
- Stale source — wire up `freshness:` + `dbt source freshness` in CI
- Statistical drift — column mean / row count outside expected window
- Custom row-level invariant — e.g., "order total = sum of line items"

Defer model authoring + structure to `dbt-modeling-staging-marts`. Defer general data-quality on non-dbt warehouses to `great-expectations-soda-data-quality`.

## Setup

```bash
# dbt-core has built-in tests; install community packages for breadth
# In packages.yml:
cat > packages.yml <<'EOF'
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: calogica/dbt_expectations
    version: 0.10.4
  - package: dbt-labs/dbt_project_evaluator
    version: 0.13.0
EOF

dbt deps              # installs into dbt_packages/
dbt parse             # validate yaml
dbt test --select source:* tag:critical    # smoke test
```

No external API keys needed; runs in-warehouse.

## Test taxonomy

| Type | Where | Use when |
|---|---|---|
| Generic (column-level) | `tests:` in YAML | Reusable: unique, not_null, accepted_values, relationships |
| Singular | `tests/<name>.sql` | One-off business invariant (rare logic) |
| dbt-utils generic | YAML | Multi-column unique, expression-is-true, equality of two tables |
| dbt-expectations | YAML | Statistical: column-mean-in-range, recent-data, regex-match |
| Source freshness | `_*__sources.yml` | "Has the raw table loaded in last N hours?" |

## Common recipes

### Recipe 1 — Built-in generic tests

```yaml
# models/marts/finance/_finance__models.yml
version: 2

models:
  - name: fct_orders
    description: One row per order
    columns:
      - name: order_id
        description: Primary key
        tests:
          - unique
          - not_null
      - name: customer_id
        description: FK to dim_customers
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id
      - name: status
        tests:
          - accepted_values:
              values: ['pending', 'paid', 'refunded', 'cancelled']
              severity: warn
      - name: amount_usd
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 1000000
```

Run:

```bash
dbt test --select fct_orders                # all tests on this model
dbt test --select fct_orders,test_name:unique     # specific generic
dbt test --select source:stripe              # source tests only
```

### Recipe 2 — Singular test (business invariant)

```sql
-- tests/assert_order_total_equals_lineitems.sql
-- Returns rows that VIOLATE the assertion. Empty = pass.

with order_totals as (
    select order_id, sum(line_amount) as line_sum
    from {{ ref('fct_order_lines') }}
    group by 1
),

orders as (
    select order_id, total_amount
    from {{ ref('fct_orders') }}
)

select
    o.order_id,
    o.total_amount,
    ot.line_sum,
    o.total_amount - ot.line_sum as diff
from orders o
join order_totals ot using (order_id)
where abs(o.total_amount - ot.line_sum) > 0.01     -- tolerance for floating point
```

Tests in `tests/` are auto-discovered; no YAML wiring needed.

### Recipe 3 — dbt-utils highlights

```yaml
models:
  - name: fct_orders
    tests:
      # Multi-column unique (composite PK)
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns:
            - customer_id
            - order_date
            - product_id

      # Two tables produce equal rowsets
      - dbt_utils.equality:
          compare_model: ref('fct_orders_v1_legacy')
          compare_columns: [order_id, amount_usd]

    columns:
      - name: status
        tests:
          # Expression-is-true (free-form)
          - dbt_utils.expression_is_true:
              expression: "amount_usd >= refund_amount_usd"

      - name: created_at
        tests:
          - dbt_utils.not_constant            # column has more than 1 distinct value
          - dbt_utils.cardinality_equality:   # join column has same distinct count as ref
              field: id
              to: ref('dim_users')
```

### Recipe 4 — dbt-expectations (statistical / regex)

```yaml
models:
  - name: fct_orders
    columns:
      - name: amount_usd
        tests:
          # Mean lies in expected range — alerts on drift
          - dbt_expectations.expect_column_mean_to_be_between:
              min_value: 50
              max_value: 500

          # Stdev within expectations
          - dbt_expectations.expect_column_stdev_to_be_between:
              min_value: 10
              max_value: 1000

          # No values outside [0, 100k]
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: 100000
              strictly: false                 # inclusive bounds

      - name: email
        tests:
          - dbt_expectations.expect_column_values_to_match_regex:
              regex: "^[^@]+@[^@]+\\.[a-zA-Z]{2,}$"
              row_condition: "email is not null"    # skip nulls

      - name: created_at
        tests:
          # Data must be recent (alerts on stale pipeline)
          - dbt_expectations.expect_row_values_to_have_recent_data:
              datepart: day
              interval: 1
              row_condition: "is_test = false"

      - name: status_history_count
        tests:
          - dbt_expectations.expect_column_pair_values_A_to_be_greater_than_B:
              column_A: end_at
              column_B: start_at
              or_equal: false
```

### Recipe 5 — Source freshness

```yaml
# models/staging/stripe/_stripe__sources.yml
version: 2

sources:
  - name: stripe
    database: raw
    schema: stripe
    loaded_at_field: _fivetran_synced
    freshness:
      warn_after: { count: 12, period: hour }
      error_after: { count: 24, period: hour }
    tables:
      - name: charges
      - name: customers
        loaded_at_field: _fivetran_synced     # per-table override
        freshness:
          warn_after: { count: 24, period: hour }
          error_after: { count: 48, period: hour }
```

Run:

```bash
dbt source freshness                         # check all sources
dbt source freshness --select source:stripe.charges
```

In CI: a `warn` returns exit 0 with a warning; `error` returns exit 1.

### Recipe 6 — Severity, store_failures, where

```yaml
columns:
  - name: amount_usd
    tests:
      - not_null:
          severity: warn               # downgrades from error
          warn_if: ">10"               # warn only if >10 nulls (default >0)
          error_if: ">100"             # error if >100 (default >0)

      - dbt_expectations.expect_column_values_to_be_between:
          min_value: 0
          max_value: 1000000
          config:
            store_failures: true       # write failing rows to <schema>_dbt_test__audit
            where: "is_test = false"   # restrict test to subset
```

`store_failures` writes failures to a queryable table for postmortem; default is true in dbt 1.7+ via `tests.store_failures`.

### Recipe 7 — Custom generic test

```sql
-- macros/test_warn_if_above_p99.sql
{% test warn_if_above_p99(model, column_name, multiplier=2) %}

with stats as (
    select
        percentile_cont(0.99) within group (order by {{ column_name }}) as p99
    from {{ model }}
),

outliers as (
    select {{ column_name }}
    from {{ model }}, stats
    where {{ column_name }} > p99 * {{ multiplier }}
)

select * from outliers

{% endtest %}
```

Use:

```yaml
columns:
  - name: latency_ms
    tests:
      - warn_if_above_p99:
          multiplier: 3
```

### Recipe 8 — Test selection patterns

```bash
dbt test --select state:modified                       # tests on modified models
dbt test --select tag:critical                         # tagged tests
dbt test --select fct_orders,test_type:singular        # only singular tests for model
dbt test --select test_name:unique                     # all unique-tests in project
dbt test --exclude tag:slow                            # exclude slow tests
dbt test --indirect-selection=eager                    # also run tests indirectly attached
```

### Recipe 9 — CI integration (GitHub Actions)

```yaml
# .github/workflows/dbt-ci.yml
name: dbt CI
on:
  pull_request:
    branches: [main]

jobs:
  dbt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install dbt-snowflake sqlfluff
      - run: dbt deps
      - run: sqlfluff lint models/
      - run: dbt parse
      - name: dbt build (slim CI)
        env:
          DBT_SNOWFLAKE_PASSWORD: ${{ secrets.DBT_SNOWFLAKE_PASSWORD }}
        run: |
          aws s3 cp s3://dbt-state/prod/manifest.json ./prod-manifest/manifest.json
          dbt build --select state:modified+ --defer --state ./prod-manifest --fail-fast
      - run: dbt source freshness --select source:stripe
```

### Recipe 10 — Test debugging

```bash
# After a failing test, query the failing rows
dbt test --select fct_orders 2>&1 | grep "Failure"
dbt show --inline "select * from {{ ref('analytics_dbt_test__audit') }}.dbt_utils_unique_combo_fct_orders limit 20"
# Or via warehouse SQL — dbt logs the audit table name
```

## Example end-to-end

**Goal:** Bullet-proof `fct_subscription_revenue` mart.

1. PK: `unique` + `not_null` on `(customer_id, month_start)` via `dbt_utils.unique_combination_of_columns`.
2. FK: `relationships` on `customer_id` → `dim_customers`.
3. Bounds: `dbt_expectations.expect_column_values_to_be_between(mrr, 0, 1_000_000)`.
4. Drift: `expect_column_mean_to_be_between(mrr, 50, 5000)` with `severity: warn`.
5. Freshness: `_*__sources.yml` declares `warn_after: 12h`, `error_after: 24h`.
6. Business invariant (singular): `tests/assert_mrr_equals_sum_of_subscriptions.sql`.
7. Wire `dbt build` into GitHub Actions as required check on PRs.
8. Schedule `dbt source freshness` hourly via Airflow / dbt Cloud; alert Slack on `error`.

## Edge cases / gotchas

- **`store_failures` storage cost** — auditing test failures writes to warehouse. Set `store_failures_as: table` only for tests you'll review; use `view` to limit cost.
- **`not_null` with warn severity** — `severity: warn` makes the test non-blocking; CI exit code stays 0. Use only when nulls are expected and tolerated.
- **`relationships` is full-scan** — on large tables it's slow. Restrict via `where:` clause or sample with `where: random() < 0.01` for nightly checks.
- **`accepted_values` is case-sensitive** — `['Active']` will fail on `'active'`. Lowercase in staging if comparison is logical.
- **dbt-expectations regex dialect varies** — Snowflake uses POSIX; BigQuery uses re2; doc-test on the right warehouse first.
- **Multiple expectations on same column** — combine into `expect_column_values_to_be_between` with `strictly: false` rather than chaining min/max separately.
- **Source freshness needs `loaded_at_field`** — if your ELT doesn't write a timestamp column, you can't run freshness; consider `dbt-expectations.expect_row_values_to_have_recent_data` on the staging model instead.
- **`dbt build` halts on test failure** — descendants don't run. Use `--no-fail-fast` to continue and gather all failures.
- **Test descriptions** — add `description:` on tests so failures self-document: `tests: [{not_null: {description: "Order ID must be present for billing"}}]`.
- **dbt-project-evaluator** — install for meta-tests (every model has a description, every PK has uniqueness test, etc.).

## Sources

- [dbt — Data tests](https://docs.getdbt.com/docs/build/data-tests)
- [dbt — Source freshness](https://docs.getdbt.com/docs/build/sources#snapshotting-source-data-freshness)
- [dbt-utils package](https://github.com/dbt-labs/dbt-utils)
- [dbt-expectations package](https://github.com/calogica/dbt-expectations)
- [dbt-project-evaluator](https://github.com/dbt-labs/dbt-project-evaluator)
- [dbt blog — Test Smarter, Not Harder (2025)](https://docs.getdbt.com/blog/test-smarter-where-tests-should-go-in-your-pipeline)
- role.md → "dbt test catalog"
