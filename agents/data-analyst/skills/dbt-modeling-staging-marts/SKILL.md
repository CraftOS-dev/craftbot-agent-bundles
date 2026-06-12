<!--
Source: https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview
sqlfluff: https://docs.sqlfluff.com/
Companion playbook: role.md → "dbt project structure playbook" + "SQL refactor playbook"
-->

# dbt modeling — staging / intermediate / marts

End-to-end recipe for authoring dbt models in the Kimball-style three-layer structure: `staging/` (1:1 source rename + type cast), `intermediate/` (reusable business-logic primitives), `marts/` (final fact/dim tables organized by domain). Includes materialization decisions, sqlfluff linting, and patterns that survive code review.

## When to use

- "Set up a dbt project" / "add a model for entity X" / "refactor this messy SQL into dbt"
- New analytics workload that needs versioning, tests, docs, lineage
- Stage a raw source table so downstream models stop joining on undocumented column names
- Reach for an incremental model because a fact table takes >5 minutes to rebuild
- Convert ad-hoc analyst SQL into a governed mart with a documented grain

Defer test-authoring (uniqueness / freshness / dbt-expectations) to `dbt-test-authoring-utils-expectations`. Defer warehouse-cost tuning to `warehouse-cost-optimization-snowflake-bq`.

## Setup

```bash
# Install dbt-core + adapter for your warehouse
pip install dbt-core dbt-snowflake          # or dbt-bigquery / dbt-databricks / dbt-postgres / dbt-duckdb
pip install sqlfluff sqlfluff-templater-dbt # SQL linter

# Initialize a project
dbt init analytics
cd analytics
dbt deps          # install packages from packages.yml
dbt debug         # verify warehouse connection
dbt build         # run all models + tests in DAG order
```

Auth requirements:
- `profiles.yml` in `~/.dbt/` — warehouse credentials (one profile per env: `dev` / `prod`)
- `DBT_PROFILES_DIR` env var if profile lives next to project
- Recipient supplies warehouse account, role, schema, password / key-pair / OAuth

## Project layout (canonical)

```
analytics/
  dbt_project.yml
  packages.yml
  profiles.yml             # or ~/.dbt/profiles.yml
  models/
    staging/
      stripe/
        _stripe__sources.yml      # source declarations + freshness
        _stripe__models.yml       # column docs + tests
        stg_stripe__customers.sql
        stg_stripe__charges.sql
    intermediate/
      finance/
        int_charges__joined_with_customers.sql
    marts/
      finance/
        _finance__models.yml
        fct_orders.sql            # fact: events at a grain (one row per order)
        dim_customers.sql         # dimension: entity attributes (one row per customer)
  seeds/                          # static CSVs (small reference data)
  snapshots/                      # SCD2 history tracking
  macros/                         # reusable Jinja
  tests/                          # singular .sql tests
  analyses/                       # one-off (NOT run by `dbt run`)
```

## Common recipes

### Recipe 1 — Stage a raw source

```sql
-- models/staging/stripe/stg_stripe__charges.sql
{{ config(materialized='view') }}

with source as (
    select * from {{ source('stripe', 'charges') }}
),

renamed as (
    select
        id                   as charge_id,
        customer              as customer_id,
        amount / 100.0        as amount_usd,
        currency              as currency_code,
        status                as charge_status,
        created::timestamp    as created_at,
        _fivetran_synced::timestamp as loaded_at
    from source
    where _fivetran_deleted = false
)

select * from renamed
```

Staging models are **always** views (cheap, always fresh, no warehouse-cost concern). One model per source table, 1:1 column mapping.

### Recipe 2 — Declare the source + freshness

```yaml
# models/staging/stripe/_stripe__sources.yml
version: 2

sources:
  - name: stripe
    description: Raw Stripe data loaded via Fivetran
    database: raw
    schema: stripe
    loaded_at_field: _fivetran_synced
    freshness:
      warn_after: { count: 12, period: hour }
      error_after: { count: 24, period: hour }
    tables:
      - name: charges
        description: One row per Stripe charge event
        columns:
          - name: id
            description: Stripe charge ID (primary key)
            tests: [unique, not_null]
          - name: customer
            description: FK to stripe.customers.id
            tests:
              - relationships:
                  to: source('stripe', 'customers')
                  field: id
```

`dbt source freshness` runs the freshness check; wire into CI to alert when Fivetran is stale.

### Recipe 3 — Intermediate model (reusable primitive)

```sql
-- models/intermediate/finance/int_charges__with_refunds.sql
{{ config(materialized='ephemeral') }}

with charges as (
    select * from {{ ref('stg_stripe__charges') }}
),

refunds as (
    select charge_id, sum(amount_usd) as refund_amount_usd
    from {{ ref('stg_stripe__refunds') }}
    group by 1
)

select
    c.charge_id,
    c.customer_id,
    c.created_at,
    c.amount_usd,
    coalesce(r.refund_amount_usd, 0)         as refund_amount_usd,
    c.amount_usd - coalesce(r.refund_amount_usd, 0) as net_amount_usd
from charges c
left join refunds r using (charge_id)
```

Intermediate models encapsulate business logic that >1 mart will reuse. Use `ephemeral` when only one downstream consumer; `view` when 2-3; promote to `table` if many.

### Recipe 4 — Fact model in a mart

```sql
-- models/marts/finance/fct_orders.sql
{{
  config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='append_new_columns',
    incremental_strategy='merge',
    cluster_by=['order_date']
  )
}}

with charges as (
    select * from {{ ref('int_charges__with_refunds') }}

    {% if is_incremental() %}
      -- Only process new rows since last run
      where created_at > (select coalesce(max(created_at), '1900-01-01') from {{ this }})
    {% endif %}
),

customers as (
    select * from {{ ref('dim_customers') }}
)

select
    c.charge_id              as order_id,
    c.customer_id,
    c.created_at,
    c.created_at::date       as order_date,
    c.amount_usd             as gross_revenue,
    c.refund_amount_usd      as refunds,
    c.net_amount_usd         as net_revenue,
    cu.country,
    cu.acquisition_channel
from charges c
left join customers cu using (customer_id)
```

The `is_incremental()` guard means dbt runs the WHERE filter only on subsequent runs (full-refresh on first build).

### Recipe 5 — Materialization decision tree

| Choose | When | Cost |
|---|---|---|
| `view` | Source is small OR freshness > cache value | Re-execute per query |
| `table` | Repeated downstream reads, refresh window allows | Storage + per-build cost |
| `incremental` | Source >10M rows, append-only, can identify new rows | Lowest per-run cost; complexity overhead |
| `snapshot` | Track changes to mutable dimensions (SCD2) | Storage; preserves history |
| `ephemeral` | Reusable CTE used once | Inlined; not queryable in warehouse |
| `materialized_view` (Snowflake/BQ) | Always-fresh aggregate | Warehouse-managed refresh credits |

### Recipe 6 — dbt commands cheat sheet

```bash
dbt run                                          # build all models (no tests)
dbt run --select +marts.finance.fct_orders       # build a model + everything upstream
dbt run --select marts.finance.fct_orders+       # build a model + everything downstream
dbt run --select tag:hourly                      # by tag
dbt run --select state:modified+ --defer --state ./prod-manifest   # only changed models (Slim CI)
dbt build                                        # run + test in DAG order, fail-fast
dbt test --select source:stripe.charges          # test only source freshness + tests
dbt source freshness                             # run freshness checks
dbt docs generate && dbt docs serve              # local docs site with lineage
dbt parse                                        # validate syntax only (CI lint)
dbt compile --select fct_orders                  # render compiled SQL to target/
dbt clean                                        # remove target/ + dbt_packages/
```

### Recipe 7 — sqlfluff linting

`.sqlfluff` in project root:

```ini
[sqlfluff]
templater = dbt
dialect = snowflake
max_line_length = 120
exclude_rules = L036, AM04

[sqlfluff:rules:capitalisation.keywords]
capitalisation_policy = lower

[sqlfluff:rules:capitalisation.identifiers]
extended_capitalisation_policy = lower

[sqlfluff:templater:dbt]
project_dir = ./
profiles_dir = ~/.dbt/
```

Run:

```bash
sqlfluff lint models/                # check all
sqlfluff fix models/marts/           # auto-fix safe rules
sqlfluff lint --dialect bigquery -   < query.sql   # lint stdin
```

CI step (GitHub Actions snippet):

```yaml
- run: sqlfluff lint models/
- run: dbt parse
- run: dbt build --select state:modified+ --defer --state ./prod-manifest
```

### Recipe 8 — Snapshot for SCD2 history

```sql
-- snapshots/customer_plan_changes.sql
{% snapshot customer_plan_changes %}

{{
  config(
    target_schema='snapshots',
    unique_key='customer_id',
    strategy='check',
    check_cols=['plan_tier', 'mrr', 'status']
  )
}}

select * from {{ source('app', 'customers') }}

{% endsnapshot %}
```

Run via `dbt snapshot` (separate from `dbt run`). Schedule hourly or daily; dbt manages `dbt_valid_from` / `dbt_valid_to` columns automatically.

### Recipe 9 — Reusable macro

```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name, decimal_places=2) %}
    (cast({{ column_name }} as numeric) / 100.0)::numeric(16, {{ decimal_places }})
{% endmacro %}
```

Usage:

```sql
select {{ cents_to_dollars('amount') }} as amount_usd from {{ ref('stg_stripe__charges') }}
```

### Recipe 10 — Slim CI (only build changed models)

```bash
# In CI: download production manifest first
aws s3 cp s3://dbt-state/prod/manifest.json ./prod-manifest/manifest.json

dbt build \
  --select state:modified+ \
  --defer \
  --state ./prod-manifest \
  --fail-fast
```

`state:modified+` = changed nodes + descendants. `--defer` makes unbuilt refs resolve to prod tables, so you don't need to rebuild everything in CI.

## Example end-to-end

**Goal:** New mart `fct_subscription_revenue` aggregating monthly recurring revenue per customer.

1. Add source declaration in `_app__sources.yml` for `app.subscriptions`.
2. Create `stg_app__subscriptions.sql` (view, 1:1 rename + cast).
3. Create `int_subscriptions__expanded_monthly.sql` (intermediate, expand subscription rows to monthly granularity using `dbt_utils.date_spine`).
4. Create `marts/finance/fct_subscription_revenue.sql` (incremental on `month_start`, clustered by `month_start`).
5. `sqlfluff lint models/marts/finance/fct_subscription_revenue.sql`
6. `dbt build --select +fct_subscription_revenue`
7. `dbt docs generate && dbt docs serve` — verify lineage graph and column docs.

## Edge cases / gotchas

- **`select *` in staging is brittle** — if upstream adds a column, downstream materialization may fail or pick up untyped data. Always explicit-list columns in staging.
- **Incremental backfill** — adding a column? Use `--full-refresh` once, then resume incremental. `on_schema_change='append_new_columns'` handles additive changes automatically.
- **Ephemeral models can't be queried directly** — they're inlined CTEs. Tests on an ephemeral model run against its compiled inlined form.
- **Circular refs** — dbt detects them; if one fires, check that intermediate models don't accidentally `ref()` a mart.
- **Snapshot strategy choice** — `timestamp` (you have a reliable `updated_at`) is faster than `check` (compare specific columns). `check` is needed when source has no reliable update timestamp.
- **`merge` vs `delete+insert`** — `merge` is faster on Snowflake/BQ for the typical idempotent case; `delete+insert` is the right call on Postgres without proper indexes.
- **profiles.yml secrets** — never commit; use `env_var('SNOWFLAKE_PASSWORD')` in profiles.yml and load from CI vault.
- **`dbt run` does NOT run tests** — use `dbt build` for CI; `dbt run && dbt test` for finer control.
- **`ref()` vs `source()`** — `ref()` references a dbt model (other `.sql` file); `source()` references a raw table declared in sources YAML. Mixing them confuses the lineage DAG.

## Sources

- [dbt — How we structure dbt projects](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview)
- [dbt — Materializations](https://docs.getdbt.com/docs/build/materializations)
- [dbt — Incremental models](https://docs.getdbt.com/docs/build/incremental-models)
- [dbt — Snapshots](https://docs.getdbt.com/docs/build/snapshots)
- [sqlfluff documentation](https://docs.sqlfluff.com/en/stable/)
- [dbt Discourse — Slim CI](https://discourse.getdbt.com/t/performing-a-blue-green-deploy-of-your-dbt-project-on-snowflake/1349)
- [dbt Labs — How we use Jinja](https://docs.getdbt.com/docs/build/jinja-macros)
- role.md → "dbt project structure playbook" (this bundle's authoritative spec)
