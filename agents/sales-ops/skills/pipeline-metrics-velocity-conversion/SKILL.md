<!--
Source: https://www.salesforce.com/resources/articles/sales-reports/ + https://www.gong.io/blog/sales-pipeline-management/
Pipeline metrics — velocity, stage conversion, deal age, stage criteria (June 2026 SOTA).
-->
# Pipeline Metrics — Velocity + Conversion + Stage Criteria — SKILL

Standard pipeline metrics: stage-to-stage conversion %, time-in-stage median, sales velocity (Win × Deals × Value / Cycle days), pipeline coverage (3-4× quota), pipeline-to-revenue ratio. Stage criteria defined + enforced via validation rules. Render to Salesforce CRMA, HubSpot Reports, Looker, Sigma, or warehouse via dbt.

## When to use

- **Build a pipeline velocity dashboard** — quarterly + YoY view.
- **Stage conversion analysis** — find the leakiest stage.
- **Stage criteria definition** — entry + exit requirements per stage.
- **Time-in-stage / aging** — median + p90; flag stalled.
- **Pipeline coverage check** — current $ vs upcoming quota.
- **dbt model deploy** — `fct_opportunities` etc.
- **Trigger phrases**: "pipeline velocity", "conversion by stage", "deal age", "coverage ratio", "stage criteria", "fct_opportunities".

Do NOT use this skill for: **forecasting commit/best/pipe** (use `forecasting-clari-boostup-aviso`); **stalled deal alerts** (use `stalled-deal-alerts-engagement-signals`); **rep dashboards** (use `rep-performance-dashboards`).

## Setup

```bash
# Salesforce / HubSpot via api-gateway
export MATON_API_KEY="<key>"

# Warehouse (postgres-mcp)
export PG_URI="postgresql://..."

# dbt (if using)
pip install dbt-postgres
# Or
pip install dbt-snowflake dbt-bigquery
```

Required:
- CRM admin read access (SOQL/HubSpot API)
- Warehouse + dbt (optional but recommended for trend analysis)
- Quota source-of-truth (notion / Anaplan / spreadsheet)

## Common recipes

### Recipe 1: Sales Velocity formula

```
Sales Velocity = (Win Rate × Avg Deal Size × Open Opps) / Sales Cycle Days

Example:
  Win Rate = 28%
  Avg Deal Size = $45,000
  Open Opps = 120
  Sales Cycle Days = 60

  Velocity = (0.28 × 45000 × 120) / 60 = $25,200/day

  Annualized: ×365 = $9.2M/year per pipeline-snapshot
```

### Recipe 2: SOQL for stage conversion (last 4 quarters)

```bash
sf data query --target-org prod --query \
  "SELECT StageName, COUNT(Id) total_in_stage, COUNT_DISTINCT(Account.Id) accounts
   FROM Opportunity
   WHERE CreatedDate >= LAST_N_QUARTERS:4
   GROUP BY StageName
   ORDER BY StageName"
```

For true conversion: requires snapshots (which deals entered each stage, which advanced). Pull stage history via:

```bash
sf data query --target-org prod --query \
  "SELECT OpportunityId, StageName, CreatedDate, NewValue, OldValue
   FROM OpportunityFieldHistory
   WHERE Field = 'StageName'
     AND CreatedDate >= LAST_N_QUARTERS:4
   ORDER BY OpportunityId, CreatedDate"
```

### Recipe 3: Time-in-stage median (Python)

```python
import pandas as pd

history = pd.read_csv('opportunity_field_history.csv')  # from Recipe 2
history = history.sort_values(['OpportunityId', 'CreatedDate'])

# For each Opp + stage entry, compute days until next stage change
history['next_change'] = history.groupby('OpportunityId')['CreatedDate'].shift(-1)
history['days_in_stage'] = (pd.to_datetime(history['next_change']) -
                             pd.to_datetime(history['CreatedDate'])).dt.days
# For open opps still in stage: now() - CreatedDate
open_now = history['next_change'].isna()
history.loc[open_now, 'days_in_stage'] = (pd.Timestamp.now() -
                                            pd.to_datetime(history.loc[open_now, 'CreatedDate'])).dt.days

# Median per stage
median_by_stage = history.groupby('NewValue')['days_in_stage'].median()
p90_by_stage = history.groupby('NewValue')['days_in_stage'].quantile(0.90)

print("Median days-in-stage:")
print(median_by_stage)
print("\nP90 (stall threshold):")
print(p90_by_stage)
```

### Recipe 4: Stage conversion % (per stage)

```sql
-- Run against warehouse fact table (dbt-modeled)
WITH stage_entry AS (
  SELECT
    opportunity_id,
    stage,
    entered_at,
    LEAD(stage) OVER (PARTITION BY opportunity_id ORDER BY entered_at) AS next_stage,
    LEAD(entered_at) OVER (PARTITION BY opportunity_id ORDER BY entered_at) AS next_entered_at
  FROM fct_opportunity_stage_history
  WHERE entered_at >= '2026-01-01'
)
SELECT
  stage,
  COUNT(*) AS entered,
  COUNT(next_stage) AS advanced,
  ROUND(100.0 * COUNT(next_stage) / NULLIF(COUNT(*),0), 1) AS conversion_pct
FROM stage_entry
GROUP BY stage
ORDER BY stage;
```

Result example:
```
Prospect → Discovery:     40%
Discovery → Evaluation:   55%
Evaluation → Proposal:    60%
Proposal → Negotiation:   70%
Negotiation → Closed Won: 75%
Overall (Prospect → Won): 40% × 55% × 60% × 70% × 75% = 6.9%
```

### Recipe 5: Stage criteria template + validation rule

```markdown
## Stage 3 — Evaluation

### Entry criteria
- [ ] Champion identified (Salesforce: Champion__c populated + Champion_Advocacy_Note__c populated)
- [ ] Pain articulated (Identified_Pain__c populated, > 50 chars)
- [ ] Technical evaluator named (Technical_Evaluator__c populated)

### Exit criteria (to advance to Proposal)
- [ ] Decision criteria documented (Decision_Criteria__c populated, > 100 chars)
- [ ] Economic buyer named (Economic_Buyer__c populated)
- [ ] Demo completed (Task type=Demo, after stage entry date)
- [ ] Verbal interest confirmed

### Salesforce validation rule
```
AND(
  ISCHANGED(StageName),
  TEXT(PRIORVALUE(StageName)) = "Evaluation",
  TEXT(StageName) = "Proposal",
  OR(
    ISBLANK(Decision_Criteria__c),
    LEN(Decision_Criteria__c) < 100,
    ISBLANK(Economic_Buyer__c)
  )
)
```
```

Deploy via `salesforce-admin-custom-fields-flows` Recipe 3.

### Recipe 6: Pipeline coverage check (quarterly + monthly)

```python
import requests, os

# Pull open pipeline
q = """
SELECT SUM(Amount) total_pipeline, COUNT(Id) opp_count
FROM Opportunity
WHERE IsClosed = FALSE
  AND CloseDate >= 2026-07-01
  AND CloseDate <= 2026-09-30
"""
r = requests.get(f"https://gateway.maton.ai/salesforce/services/data/v60.0/query",
                 params={"q": q},
                 headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"}).json()

pipeline = r['records'][0]['total_pipeline']
team_quota = 2_500_000  # source from notion / Anaplan
coverage = pipeline / team_quota

print(f"Open pipeline: ${pipeline:,.0f}")
print(f"Team quota:    ${team_quota:,.0f}")
print(f"Coverage:      {coverage:.1f}× (target: 3-4×)")

if coverage < 3.0:
    # Slack alert
    print("⚠ Coverage below 3× — pipe-gen sprint needed")
```

### Recipe 7: dbt fct_opportunities model

```sql
-- models/marts/sales/fct_opportunities.sql
{{ config(materialized='incremental', unique_key='opportunity_id') }}

WITH source_opps AS (
  SELECT * FROM {{ source('salesforce', 'opportunity') }}
  {% if is_incremental() %}
  WHERE last_modified_date > (SELECT MAX(last_modified_date) FROM {{ this }})
  {% endif %}
),
stage_history AS (
  SELECT opportunity_id,
         MIN(CASE WHEN new_value = 'Discovery' THEN created_date END) AS entered_discovery_at,
         MIN(CASE WHEN new_value = 'Evaluation' THEN created_date END) AS entered_evaluation_at,
         MIN(CASE WHEN new_value = 'Proposal' THEN created_date END) AS entered_proposal_at,
         MIN(CASE WHEN new_value = 'Negotiation' THEN created_date END) AS entered_negotiation_at,
         MIN(CASE WHEN new_value IN ('Closed Won','Closed Lost') THEN created_date END) AS closed_at
  FROM {{ source('salesforce', 'opportunity_field_history') }}
  WHERE field = 'StageName'
  GROUP BY 1
)
SELECT
  o.opportunity_id,
  o.account_id,
  o.owner_id,
  o.stage_name,
  o.amount,
  o.close_date,
  o.created_date,
  o.is_closed,
  o.is_won,
  sh.entered_discovery_at,
  sh.entered_evaluation_at,
  sh.entered_proposal_at,
  sh.entered_negotiation_at,
  sh.closed_at,
  DATEDIFF('day', o.created_date, COALESCE(sh.closed_at, NOW())) AS days_in_pipeline,
  DATEDIFF('day', sh.entered_evaluation_at, sh.entered_proposal_at) AS days_in_evaluation,
  DATEDIFF('day', sh.entered_proposal_at, sh.entered_negotiation_at) AS days_in_proposal
FROM source_opps o
LEFT JOIN stage_history sh USING (opportunity_id)
```

```bash
dbt run --select fct_opportunities --target prod
dbt test --select fct_opportunities
```

### Recipe 8: Win rate + average deal size (rolling 4 quarters)

```sql
SELECT
  DATE_TRUNC('quarter', closed_at) AS quarter,
  COUNT(*) FILTER (WHERE is_won = TRUE) AS wins,
  COUNT(*) FILTER (WHERE is_closed = TRUE) AS closed,
  ROUND(100.0 * COUNT(*) FILTER (WHERE is_won = TRUE) / NULLIF(COUNT(*) FILTER (WHERE is_closed = TRUE), 0), 1) AS win_rate_pct,
  AVG(amount) FILTER (WHERE is_won = TRUE) AS avg_won_deal_size,
  AVG(amount) FILTER (WHERE is_closed = TRUE) AS avg_closed_deal_size
FROM fct_opportunities
WHERE closed_at >= NOW() - INTERVAL '12 months'
GROUP BY 1
ORDER BY 1 DESC;
```

### Recipe 9: Per-rep velocity scorecard

```sql
SELECT
  o.owner_id,
  u.full_name,
  COUNT(*) FILTER (WHERE o.is_closed = FALSE) AS open_opps,
  AVG(o.amount) FILTER (WHERE o.is_won = TRUE) AS avg_won_deal,
  COUNT(*) FILTER (WHERE o.is_won) * 1.0 / NULLIF(COUNT(*) FILTER (WHERE o.is_closed), 0) AS win_rate,
  AVG(o.days_in_pipeline) FILTER (WHERE o.is_won) AS avg_cycle_days,
  COUNT(*) FILTER (WHERE o.is_won = TRUE) AS deals_won_qtr,
  SUM(o.amount) FILTER (WHERE o.is_won = TRUE) AS amount_won_qtr
FROM fct_opportunities o
JOIN dim_users u ON o.owner_id = u.user_id
WHERE o.closed_at >= DATE_TRUNC('quarter', NOW())
   OR (o.is_closed = FALSE AND o.created_date >= DATE_TRUNC('quarter', NOW()) - INTERVAL '6 months')
GROUP BY 1, 2
ORDER BY 8 DESC;
```

### Recipe 10: Stage-criteria audit (which stages lack validation rules?)

```bash
# Pull all validation rules per stage
sf data query --target-org prod --use-tooling-api --query \
  "SELECT Id, ValidationName, Active, ErrorConditionFormula \
   FROM ValidationRule \
   WHERE EntityDefinitionId IN (SELECT Id FROM EntityDefinition WHERE QualifiedApiName = 'Opportunity')"

# Per stage: presence check. If missing, stage criteria not enforced — pipeline data quality suffers.
```

### Recipe 11: Pipeline aging report (stalled by stage)

```sql
SELECT
  stage_name,
  COUNT(*) AS deals_in_stage,
  AVG(EXTRACT(EPOCH FROM (NOW() - entered_current_stage_at)) / 86400) AS avg_days_in_stage,
  COUNT(*) FILTER (WHERE EXTRACT(EPOCH FROM (NOW() - entered_current_stage_at)) / 86400 > 1.5 *
    (SELECT AVG(days_in_stage_at_close) FROM fct_opportunity_stage_history WHERE stage = fct_opportunities.stage_name))
    AS stalled_count
FROM fct_opportunities
WHERE is_closed = FALSE
GROUP BY 1
ORDER BY 1;
```

### Recipe 12: Pipeline-to-revenue ratio (quarterly trend)

```sql
WITH quarters AS (
  SELECT generate_series('2025-01-01'::date, '2026-12-31'::date, '3 months'::interval)::date AS q_start
)
SELECT
  q.q_start AS quarter,
  (SELECT SUM(amount) FROM fct_opportunities
    WHERE is_closed = FALSE
      AND created_date <= q.q_start
      AND (closed_at IS NULL OR closed_at > q.q_start)) AS pipeline_at_q_start,
  (SELECT SUM(amount) FROM fct_opportunities
    WHERE is_won AND closed_at >= q.q_start AND closed_at < q.q_start + INTERVAL '3 months') AS revenue_in_q,
  -- Ratio = how much pipeline at start of quarter converted to revenue
  ROUND((SELECT SUM(amount) FROM fct_opportunities
         WHERE is_won AND closed_at >= q.q_start AND closed_at < q.q_start + INTERVAL '3 months')::numeric /
        NULLIF((SELECT SUM(amount) FROM fct_opportunities
                WHERE is_closed = FALSE
                  AND created_date <= q.q_start
                  AND (closed_at IS NULL OR closed_at > q.q_start)), 0), 3) AS pipe_to_rev_ratio
FROM quarters q
ORDER BY q_start DESC;
```

## Examples

### Example 1: Quarterly stage conversion review

**Goal:** Find the leakiest stage; design intervention.

**Steps:**
1. Recipe 2 — pull stage history for last 4 quarters.
2. Recipe 4 — compute conversion % per stage.
3. Identify leak: e.g., Evaluation → Proposal = 60% but historical = 75%.
4. Drill down: which deals dropped? What was missing at exit criteria (Recipe 5)?
5. Hypothesis: missing demo before Proposal; add validation rule requiring Demo task.
6. Recipe 7 — deploy validation rule in sandbox; smoke test.
7. Monitor 4 weeks; re-run Recipe 4.

**Result:** Evaluation → Proposal conversion recovers to 72% with enforcement.

### Example 2: Pipeline coverage early-warning

**Goal:** Mid-quarter check; alert if quarterly coverage falls below 3×.

**Steps:**
1. Recipe 6 daily cron.
2. If coverage < 3.0: Slack alert to #sales-leadership.
3. Auto-create notion plan "Pipe-Gen Sprint" with required net-new pipeline target.
4. Hand off to sales-agent for outbound sprint coordination.
5. Continue monitoring; close out alert when coverage > 3.5×.

**Result:** Coverage gaps caught at week 6 of quarter, not week 12.

### Example 3: dbt fct_opportunities deploy

**Goal:** Replace ad-hoc SOQL queries with warehouse-modeled fact table for trend analysis.

**Steps:**
1. Configure Fivetran (or Hightouch reverse-ETL) Salesforce → warehouse.
2. Write Recipe 7 model + tests.
3. `dbt run` in dev; `dbt test`.
4. Promote to prod via dbt Cloud or `dbt run --target prod`.
5. Build Looker/Sigma view on fct_opportunities.
6. Deprecate ad-hoc SOQL queries → dashboards point to warehouse.

**Result:** 10× faster dashboard queries; consistent definitions across teams.

## Edge cases / gotchas

- **Stage history requires Field History Tracking enabled** — Salesforce stores 18 months by default. Need history for > 18m? Replicate to warehouse.
- **Backward stage moves complicate conversion** — deal goes Discovery → Proposal → back to Discovery → forward again. Define: total cycle vs current cycle.
- **Stage rename breaks historic comparison** — renaming "Evaluation" to "Demo" breaks 2 years of trend data.
- **Open opps in "days_in_stage" use NOW()** — comparing open vs closed: open skews high. Filter accordingly.
- **Win rate denominator** — closed deals or closed + open? Typically closed-only.
- **Coverage ratio of 3× assumes 33% close rate** — adjust by win rate. If 25% win rate, need 4× coverage.
- **Quota source-of-truth drift** — notion-stored vs Anaplan vs CRM custom field. Pick one canonical.
- **Currency mixing** — multi-currency opps; report in single currency at snapshot exchange rate.
- **Stage criteria-strictness tradeoff** — too strict = AEs game (skip stage); too loose = stage means nothing.
- **Time-in-stage for new opps** — if deal jumped to Proposal in 2 days (warm transfer), median understates real cycle.
- **dbt incremental drift** — late-arriving SF history records can miss incremental window. Use `delete+insert` for stage history.
- **Won deal "Amount" snapshot** — won amount captures final negotiated; pipeline amount evolves. Use `amount_at_close` separately.
- **Stage = Closed Lost + reopened** — happens. Reopened opps appear closed and not closed; rare but breaks aggregates.
- **Lead-to-opportunity conversion lag** — pipeline only counts opps; if lead-to-opp conversion is broken upstream, coverage looks fine but funnel breaks.
- **Pre-pipeline activities** — SDR meetings booked but not yet opportunities. Track separately, not in pipeline metrics.

## Sources

- [Salesforce Pipeline Reports](https://www.salesforce.com/resources/articles/sales-reports/)
- [Gong — Pipeline Management 2026](https://www.gong.io/blog/sales-pipeline-management/)
- [Sales Velocity formula explained](https://www.insightsquared.com/blog/sales-velocity-equation/)
- [Salesforce OpportunityFieldHistory](https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_objects_opportunityfieldhistory.htm)
- [dbt incremental models](https://docs.getdbt.com/docs/build/incremental-models)
- [Pipeline coverage ratio benchmarks (Outreach State of Sales 2026)](https://www.outreach.io/resources/state-of-sales)
- [Stage criteria + MEDDIC enforcement (Force Management)](https://www.forcemanagement.com/blog/meddic-meddpicc)
- [Hubspot Pipeline Reports](https://knowledge.hubspot.com/reports/use-reports)
