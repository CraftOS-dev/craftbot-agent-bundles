<!--
Great Expectations: https://docs.greatexpectations.io/
Soda Core: https://docs.soda.io/
Companion: role.md → "Data quality playbook"
-->

# Great Expectations + Soda Core — declarative data quality

Stand up data-quality checks via Great Expectations (declarative Python expectations + Data Docs HTML site) or Soda Core (YAML SodaCL checks in CI/Airflow), wire into CI / Airflow / Dagster, and fail builds when checks fail. Pairs with `dbt-test-authoring-utils-expectations` for warehouse-native primitives.

## When to use

- "Run quality checks against the warehouse / lake on a schedule"
- "Halt the pipeline if data is bad"
- "Audit a dataset for nulls, ranges, regex, freshness, custom invariants"
- "Generate human-readable Data Docs for stakeholders"
- "Need broader expectation library than dbt tests offer"

Defer warehouse-native testing inside dbt to `dbt-test-authoring-utils-expectations`. Defer anomaly detection (statistical) to `anomaly-detection-statistical-ml`. Defer source freshness alone to dbt sources.

## Setup

```bash
# Great Expectations (Python library + CLI)
pip install great_expectations
great_expectations --version

# Soda Core (per-warehouse package)
pip install soda-core-snowflake          # or soda-core-bigquery / soda-core-postgres / etc.

# Set up GE project
great_expectations init                  # creates ./gx/ scaffolding
# Or programmatic:
python -c "import great_expectations as gx; gx.get_context(mode='file')"
```

Auth requirements:
- Warehouse credentials in `gx/uncommitted/config_variables.yml` (encrypted at rest if `MB_ENCRYPTION_SECRET_KEY` set).
- Soda Core: `soda-core-snowflake` reads `configuration.yml` with warehouse creds (or env vars).
- Slack / PagerDuty / email webhook URLs for actions/notifications.

## Tool comparison

| | Great Expectations | Soda Core |
|---|---|---|
| Config style | Python + YAML | SodaCL YAML |
| Output | Data Docs HTML + JSON | CLI + Soda Cloud |
| Best for | Rich expectation library, generated docs | Lightweight CI checks |
| dbt integration | indirect (dbt-expectations port) | first-class via dbt artifact |
| Cost | OSS (paid GX Cloud) | OSS + paid Soda Cloud |
| Learning curve | steeper | gentler |

## Common recipes — Great Expectations

### Recipe 1 — GE project init + add a Data Source

```python
import great_expectations as gx

context = gx.get_context()

# Add Snowflake datasource
ds = context.sources.add_snowflake(
    name="warehouse",
    connection_string="snowflake://user:pass@account/db/schema?warehouse=wh&role=role",
)
asset = ds.add_table_asset(name="fct_orders", table_name="fct_orders", schema_name="marts")

batch_request = asset.build_batch_request()
print(context.get_validator(batch_request=batch_request))
```

### Recipe 2 — Define expectations

```python
import great_expectations as gx

context = gx.get_context()
suite = context.suites.add(gx.ExpectationSuite(name="orders_suite"))

# Build via Validator on a batch
batch_request = context.get_datasource("warehouse").get_asset("fct_orders").build_batch_request()
validator = context.get_validator(batch_request=batch_request, expectation_suite_name="orders_suite")

# Generic expectations
validator.expect_column_values_to_not_be_null("order_id")
validator.expect_column_values_to_be_unique("order_id")
validator.expect_column_values_to_be_in_set("status", ["pending", "paid", "refunded", "cancelled"])
validator.expect_column_values_to_be_between("amount_usd", min_value=0, max_value=1_000_000)
validator.expect_column_value_lengths_to_be_between("email", min_value=5, max_value=320)
validator.expect_column_values_to_match_regex("email", r"^[^@]+@[^@]+\.[a-zA-Z]{2,}$")

# Statistical
validator.expect_column_mean_to_be_between("amount_usd", min_value=50, max_value=500)
validator.expect_column_stdev_to_be_between("amount_usd", min_value=10, max_value=1000)

# Aggregate
validator.expect_table_row_count_to_be_between(min_value=1_000_000, max_value=100_000_000)

# Save
validator.save_expectation_suite(discard_failed_expectations=False)
```

### Recipe 3 — Run a Checkpoint

```python
checkpoint = context.add_checkpoint(
    name="orders_daily_checkpoint",
    validations=[{
        "batch_request": batch_request,
        "expectation_suite_name": "orders_suite",
    }],
    action_list=[
        {"name": "update_data_docs", "action": {"class_name": "UpdateDataDocsAction"}},
        {"name": "slack_alert", "action": {
            "class_name": "SlackNotificationAction",
            "slack_webhook": os.environ["SLACK_WEBHOOK_URL"],
            "notify_on": "failure",
            "renderer": {
                "module_name": "great_expectations.render.renderer.slack_renderer",
                "class_name": "SlackRenderer",
            },
        }},
    ],
)

result = checkpoint.run()
print(f"Success: {result.success}")
context.build_data_docs()
```

### Recipe 4 — GE in CI (GitHub Actions)

```yaml
# .github/workflows/ge.yml
name: data quality
on:
  schedule:
    - cron: "0 8 * * *"
  workflow_dispatch: {}

jobs:
  ge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install great_expectations[snowflake]
      - env:
          SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        run: |
          great_expectations checkpoint run orders_daily_checkpoint
      - uses: actions/upload-artifact@v4
        with: { name: data-docs, path: gx/uncommitted/data_docs/ }
```

### Recipe 5 — Custom expectation

```python
# In gx/plugins/expectations/expect_column_revenue_above_5pct_floor.py
from great_expectations.expectations import ColumnAggregateExpectation

class ExpectColumnRevenueAbove5pctFloor(ColumnAggregateExpectation):
    """Revenue mean must be >5% above last-month rolling mean."""

    metric_dependencies = ("column.mean",)

    def _validate(self, **kwargs):
        col_mean = kwargs["metrics"]["column.mean"]
        floor = kwargs["expectation_kwargs"].get("rolling_floor")
        return {"success": col_mean > 1.05 * floor}
```

## Common recipes — Soda Core

### Recipe 6 — Soda configuration + checks YAML

`configuration.yml`:

```yaml
data_source warehouse:
  type: snowflake
  connection:
    account: ${SNOWFLAKE_ACCOUNT}
    username: ${SNOWFLAKE_USER}
    password: ${SNOWFLAKE_PASSWORD}
    warehouse: ${SNOWFLAKE_WAREHOUSE}
    database: ANALYTICS
    schema: MARTS
    role: ANALYST_ROLE
```

`checks.yml`:

```yaml
checks for fct_orders:
  - row_count > 1000:
      name: Orders table not empty
  - duplicate_count(order_id) = 0:
      name: PK is unique
  - missing_count(customer_id) = 0:
      name: FK customer_id never null
  - missing_percent(email) < 1%
  - invalid_count(status) = 0:
      valid values: [pending, paid, refunded, cancelled]
  - avg(amount_usd) between 50 and 500:
      name: Avg order value reasonable
  - freshness(created_at) < 24h:
      name: Pipeline ran in last 24h
  - schema:
      warn:
        when wrong column index:
          customer_id: 1
      fail:
        when forbidden column present: [legacy_field]
        when required column missing: [customer_id, amount_usd]
        when wrong column type:
          amount_usd: numeric

# Cross-table check
checks for marts.fct_orders:
  - values in (customer_id) must exist in marts.dim_customers (customer_id)

# Reference check (Statistical)
checks for fct_orders:
  - change avg amount_usd < 20%:
      name: Avg order value within 20% of last scan
```

### Recipe 7 — Run Soda

```bash
soda scan -d warehouse -c configuration.yml checks.yml
# Exits 0 on pass, 1 on fail (CI-friendly)

soda scan -d warehouse -c configuration.yml --srf scan_results.json checks.yml
# --srf writes scan result file for downstream
```

### Recipe 8 — Soda + Airflow / Dagster

```python
# Airflow operator
from airflow.providers.soda.operators.soda import SodaScanOperator

scan = SodaScanOperator(
    task_id="dq_check_orders",
    data_source="warehouse",
    configuration_yaml="/opt/airflow/dq/configuration.yml",
    checks_yaml="/opt/airflow/dq/checks/fct_orders.yml",
    soda_cloud_api_key=os.environ.get("SODA_CLOUD_API_KEY"),  # optional cloud sync
)

# Downstream tasks block on scan; failure aborts DAG via on_failure_callback
```

### Recipe 9 — Soda Cloud integration

```yaml
# In configuration.yml
soda_cloud:
  host: cloud.soda.io
  api_key_id: ${SODA_CLOUD_API_KEY_ID}
  api_key_secret: ${SODA_CLOUD_API_KEY_SECRET}
```

```bash
soda scan -d warehouse -c configuration.yml checks.yml --soda-cloud
# Streams results to Soda Cloud for dashboards + alerts
```

### Recipe 10 — Comparison check (drift across runs)

```yaml
# Detect drift: row count more than 10% off from previous scan
checks for fct_orders:
  - change row_count >= -10% and change row_count <= 10%:
      name: Row count stable
  - change avg amount_usd >= -5% and change avg amount_usd <= 5%:
      name: Avg amount stable
```

## Example end-to-end

**Goal:** Daily data-quality scan on warehouse marts; alert Slack on failures; halt downstream Airflow on critical issues.

1. Identify critical tables: `fct_orders`, `fct_subscriptions`, `dim_customers`, `dim_products`.
2. Author Soda `checks.yml` per table (Recipe 6): row count, uniqueness, FK integrity, statistical bounds, freshness.
3. Wire scan into Airflow with `SodaScanOperator` (Recipe 8) — block downstream `dbt run` on scan failure.
4. Add Slack notification via Soda Cloud or Airflow callback on failure.
5. Schedule daily at 6am.
6. Weekly: review historical scan results in Soda Cloud dashboard; tune thresholds.
7. For richer expectations (regex, complex statistics, generated docs), add a Great Expectations checkpoint downstream (Recipe 3).

## Edge cases / gotchas

- **GE vs dbt-expectations** — both implement the GE expectation library. Use dbt-expectations when checks are *part* of the dbt DAG; GE for pre-load source contracts or post-load richer docs.
- **Soda freshness vs dbt freshness** — both check "data loaded recently"; Soda treats it as a check (binary fail), dbt distinguishes warn vs error.
- **Statistical expectations are sample-size sensitive** — `expect_column_mean_to_be_between` with min/max too tight will flap. Set bounds wider than historical mean ± 2σ.
- **GE Checkpoint Actions order** — actions execute in order; put `StoreValidationResultAction` before notification actions.
- **Data Docs hosting** — by default GE writes to `gx/uncommitted/data_docs/`; for shareable links, point to S3 / GCS via `S3StoreBackend`.
- **Soda check name collisions** — without `name:`, Soda auto-generates names that may conflict; always provide explicit names.
- **Soda comparison checks need previous run** — first run has no baseline, "change %" check is skipped. Document this for stakeholders.
- **GE custom expectations need re-import** — restart Python process after adding plugin files; GE caches the registry.
- **Schema drift in Soda** — `schema:` check is strict; an additive column is fine but Soda may flag it. Use `when wrong column index:` carefully.
- **CI cost** — running checks against warehouse incurs credits/slots. Scope to staging/test schemas in CI; full prod scan on schedule.
- **GE 1.x vs 0.x APIs** — major rewrite in 1.0 (2024+). Pin version; 0.x examples online don't work on 1.x.
- **PII in expectations** — `expect_column_distinct_values_to_be_in_set([...])` may log PII; redact or use hashed comparisons.

## Sources

- [Great Expectations documentation](https://docs.greatexpectations.io/docs/)
- [Great Expectations expectation gallery](https://greatexpectations.io/expectations/)
- [Great Expectations checkpoints](https://docs.greatexpectations.io/docs/oss/guides/validation/checkpoints/checkpoint_lp)
- [Soda Core documentation](https://docs.soda.io/soda-core/overview-main.html)
- [SodaCL reference](https://docs.soda.io/soda-cl/soda-cl-overview.html)
- [Soda Airflow integration](https://docs.soda.io/soda-core/orchestrate-scans.html)
- [dbt-expectations](https://github.com/calogica/dbt-expectations) (companion)
- role.md → "Data quality playbook"
