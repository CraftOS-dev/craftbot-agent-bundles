<!--
Source: https://www.clari.com/blog/sales-forecasting-methods/ + https://www.gong.io/forecast/
Forecasting discipline + commit accuracy (June 2026 SOTA).
-->
# Clari + Forecasting + Commit Accuracy — SKILL

Three-bucket forecasting (Commit / Best Case / Pipeline), commit-accuracy tracking per AE per quarter, slip vs pull-in analytics, and coverage-ratio reporting. **Clari** is the enterprise default ($1k+/seat/yr) with predictive ML; **Gong Forecast** integrates call-data signals; **BoostUp** is the mid-market alt. Manual fallback via CRM + Google Sheets always works.

## When to use

- **Weekly forecast roll-up** — every Friday, sum Commit + Best Case + Pipeline by AE.
- **Commit-accuracy tracking** — per AE per quarter, what % of committed deals actually closed.
- **Coverage-ratio monitoring** — pipeline $ ÷ quota; alert if below 3x.
- **Slip + pull-in analysis** — which deals missed close date, which closed early.
- **Trigger phrases**: "what's the forecast", "commit for this quarter", "coverage ratio", "forecast accuracy", "slipped deals", "Friday roll-up".

Do NOT use this skill for: **deal-level prediction** (use `deal-coaching-next-best-action`); **pipeline data quality** (use `pipeline-hygiene-stage-criteria`); **executive board reporting only** (use rollup output here as input to a board deck).

## Setup

```bash
export MATON_API_KEY="<key>"          # CRM access via api-gateway
export CLARI_API_KEY="<key>"          # Clari API — limited public surface; auth via OAuth
export GOOGLE_SHEETS_TOKEN="<token>"  # for manual forecast doc

# Notion / postgres for historical tracking
export NOTION_TOKEN="<key>"
export PG_URI="postgresql://..."
```

Clari + BoostUp APIs are limited; for solo founders + small revenue teams, the manual fallback (CRM + Google Sheets) is recommended and ships with this skill.

## Common recipes

### Recipe 1: Three-bucket categorization (canonical rule set)

```yaml
commit:
  meaning: ">80% confidence this closes this period"
  criteria:
    - all MEDDIC fields scored >= 2
    - mutual action plan signed
    - verbal close confirmed
    - close date this period
  forecast_value: 100% of amount
  ae_accountability: "AE delivers; missing = forecast accuracy hit"

best_case:
  meaning: "50-80% confidence"
  criteria:
    - most MEDDIC fields validated (score >= 2 on 4+ fields)
    - champion confirmed
    - EB engaged
    - close date this period (or early next)
  forecast_value: 50-80% of amount (or use a per-AE historical conversion rate)
  ae_accountability: "AE is actively working risks; one risk away from commit"

pipeline:
  meaning: "<50% confidence"
  criteria:
    - discovery complete
    - qualification in progress
  forecast_value: 0% commit, contributes to coverage ratio only
  ae_accountability: "AE building toward Best Case"
```

### Recipe 2: Auto-bucket from MEDDIC score (manual fallback)

```python
def auto_bucket(deal):
    """Return Commit / Best Case / Pipeline based on deal data."""
    meddic = int(deal.get("meddic_score", 0) or 0)
    has_map_signed = deal.get("map_signed", False)
    verbal_close = deal.get("verbal_close_confirmed", False)
    close_in_period = deal_close_in_current_period(deal)

    if meddic >= 14 and has_map_signed and verbal_close and close_in_period:
        return "commit"
    if meddic >= 10 and deal.get("champion_confirmed") and close_in_period:
        return "best_case"
    return "pipeline"
```

Override is allowed (AE judgment), but flagged and tracked.

### Recipe 3: Weekly forecast doc generation

```python
# Pull all open deals, bucket, sum
import requests, os, datetime, collections

QUARTER_START = "2026-04-01"
QUARTER_END   = "2026-06-30"

deals = requests.post(
    "https://gateway.maton.ai/hubspot/crm/v3/objects/deals/search",
    headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"},
    json={"filterGroups":[{"filters":[
        {"propertyName":"dealstage","operator":"NOT_IN","values":["closedwon","closedlost"]},
        {"propertyName":"closedate","operator":"BETWEEN","value":QUARTER_START,"highValue":QUARTER_END}
    ]}],"properties":["dealname","amount","closedate","meddic_score","forecast_bucket","hubspot_owner_id","dealstage"],"limit":200},
).json()["results"]

buckets = collections.defaultdict(lambda: {"count":0,"sum":0,"deals":[]})
for d in deals:
    bucket = d["properties"].get("forecast_bucket") or auto_bucket(d["properties"])
    amount = float(d["properties"].get("amount") or 0)
    buckets[bucket]["count"] += 1
    buckets[bucket]["sum"] += amount
    buckets[bucket]["deals"].append(d)

quota = 750_000  # this quarter, from team config

print(f"Quarter {QUARTER_START} → {QUARTER_END}")
print(f"Quota: ${quota:,}")
for b in ("commit","best_case","pipeline"):
    pct = 100 * buckets[b]["sum"] / quota
    print(f"  {b:10}: {buckets[b]['count']:3} deals, ${buckets[b]['sum']:,.0f}  ({pct:.0f}% of quota)")
total_pipe = buckets["commit"]["sum"] + buckets["best_case"]["sum"] + buckets["pipeline"]["sum"]
print(f"Total pipeline: ${total_pipe:,.0f}, Coverage: {total_pipe / quota:.1f}×  (target: 3-4×)")
```

### Recipe 4: Commit accuracy per AE per quarter

```sql
-- AE-level forecast accuracy: of deals AE committed at start of period, how many closed?
WITH committed_at_start AS (
    SELECT
        owner_id,
        period_id,
        deal_id,
        amount,
        commit_date_as_of_first_friday
    FROM forecast_snapshots
    WHERE bucket = 'commit'
      AND snapshot_date = (
        SELECT MIN(snapshot_date) FROM forecast_snapshots WHERE period_id = '<quarter>'
      )
),
closed_won_in_period AS (
    SELECT deal_id FROM deals
    WHERE dealstage = 'closedwon'
      AND closedate BETWEEN period_start AND period_end
)
SELECT
    c.owner_id,
    COUNT(*) AS committed,
    COUNT(*) FILTER (WHERE c.deal_id IN (SELECT deal_id FROM closed_won_in_period)) AS won,
    ROUND(100.0 * COUNT(*) FILTER (WHERE c.deal_id IN (SELECT deal_id FROM closed_won_in_period)) / NULLIF(COUNT(*),0), 1) AS accuracy_pct
FROM committed_at_start c
GROUP BY c.owner_id
ORDER BY accuracy_pct DESC;
```

Target: > 80% per AE per quarter. < 70% = retraining; < 60% = ride-along on next forecast call.

### Recipe 5: Slip + pull-in analysis

```sql
-- Slip: commit deals whose close-date pushed past period end
WITH slips AS (
    SELECT
        owner_id,
        deal_id,
        original_close_date_committed,
        current_close_date,
        amount
    FROM deals d
    JOIN forecast_snapshots fs ON fs.deal_id = d.deal_id
    WHERE fs.bucket = 'commit'
      AND fs.snapshot_date = '<first-friday-of-quarter>'
      AND d.current_close_date > '<quarter-end>'
),
pullins AS (
    SELECT
        owner_id,
        deal_id,
        amount
    FROM deals d
    JOIN forecast_snapshots fs ON fs.deal_id = d.deal_id
    WHERE fs.bucket = 'best_case'
      AND fs.snapshot_date = '<first-friday-of-quarter>'
      AND d.dealstage = 'closedwon'
      AND d.closedate <= '<quarter-end>'
)
SELECT
    'slip' AS event_type, COUNT(*), SUM(amount) AS amount FROM slips
UNION ALL
SELECT 'pullin', COUNT(*), SUM(amount) FROM pullins;
```

### Recipe 6: Forecast snapshot (weekly cron — feeds accuracy + slip queries)

```python
# Every Friday 5pm: snapshot all open deals + their bucket
import datetime, requests, os
snapshot_date = datetime.date.today().isoformat()

for deal in deals:
    bucket = deal["properties"].get("forecast_bucket") or auto_bucket(deal["properties"])
    # Insert to postgresql-mcp via api-gateway or direct
    insert_snapshot({
        "snapshot_date": snapshot_date,
        "period_id": current_quarter(),
        "deal_id": deal["id"],
        "owner_id": deal["properties"]["hubspot_owner_id"],
        "amount": float(deal["properties"].get("amount") or 0),
        "bucket": bucket,
        "current_close_date": deal["properties"]["closedate"],
        "meddic_score": int(deal["properties"].get("meddic_score") or 0),
    })
```

Snapshots are the basis for every accuracy + slip query. Don't skip this — without snapshots, you can't measure forecast quality.

### Recipe 7: Clari API — pull forecast roll-up (if onboarded)

```bash
# Clari's public API surface is limited; main use is pulling roll-up + write-back forecast call
curl "https://gateway.maton.ai/clari/v4/forecast/rollup?period=2026-Q2" \
  -H "Authorization: Bearer $MATON_API_KEY"
```

Returns forecast amounts by bucket + by AE + by team.

### Recipe 8: Clari API — write AE-submitted forecast call

```bash
# When AE manually adjusts their commit (vs system auto-bucket)
curl -X POST "https://gateway.maton.ai/clari/v4/forecast/submissions" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "period":"2026-Q2",
    "owner_id":"<ae-id>",
    "commit_amount":425000,
    "best_case_amount":280000,
    "submitted_at":"2026-06-09T17:00:00Z"
  }'
```

### Recipe 9: Coverage-ratio monitoring (daily)

```python
total_pipe = buckets["commit"]["sum"] + buckets["best_case"]["sum"] + buckets["pipeline"]["sum"]
quota_remaining = quota - already_closed_won_this_quarter

coverage = total_pipe / quota_remaining if quota_remaining > 0 else float("inf")

if coverage < 3.0:
    slack_alert(f"COVERAGE ALERT: {coverage:.1f}× (target 3-4×). Push outbound + pipe-gen sprint.")
```

### Recipe 10: Render forecast doc to Notion + Slack (Friday 5pm)

```python
# Renders the Recipe 3 output to Notion page + Slack ping
notion_blocks = [
    {"type":"heading_1","heading_1":{"rich_text":[{"text":{"content":f"Forecast — week of {today}"}}]}},
    {"type":"paragraph","paragraph":{"rich_text":[{"text":{"content":f"Quota: ${quota:,}, Coverage: {coverage:.1f}×"}}]}},
    {"type":"table_of_contents","table_of_contents":{}},
    # ... per-bucket sections with deal tables
]

# Then Slack:
slack_post("#sales-leadership", f"""
Forecast — {today}
Commit: ${buckets["commit"]["sum"]:,.0f} ({buckets["commit"]["count"]} deals)
Best Case: ${buckets["best_case"]["sum"]:,.0f} ({buckets["best_case"]["count"]} deals)
Coverage: {coverage:.1f}× quota
Top 3 slip-risks: {slip_risks[:3]}
""")
```

### Recipe 11: Forecast cadence (per role.md)

```yaml
weekly_friday_5pm:
  - AE: review own commit + best-case
  - System: snapshot (Recipe 6)
  - Output: Notion doc + Slack roll-up (Recipe 10)
bi_weekly_manager:
  - Manager + AE: 1:1 review of commit deals + slip risks
  - System: per-AE accuracy diff vs prior period
monthly_pipeline_coverage:
  - Leadership: coverage check (Recipe 9), pipe-gen sprint if below 3×
quarterly_close:
  - Commit accuracy roll-up (Recipe 4)
  - Slip + pull-in (Recipe 5)
  - Win/loss roll-up (handoff to win-loss-analysis-structured)
```

### Recipe 12: Forecast vs actuals dashboard (Google Sheets fallback)

When Clari/BoostUp isn't onboarded: `gspread` writes a row per AE with columns `Commit $ | Best Case $ | Pipeline $ | Coverage | Last-Week Commit | Diff`. Use `buckets_for_ae(ae_id)` against Recipe 3's bucket dict and `get_last_friday_snapshot(ae_id)` from Recipe 6 snapshot table.

## Examples

### Example 1: Friday 5pm forecast roll-up

**Goal:** Every Friday 5pm, automated forecast doc + Slack ping.

**Steps:** Cron triggers Recipe 3 to bucket all open deals → Recipe 6 snapshots to postgres → Recipe 9 coverage check, alert if < 3x → Recipe 10 renders to Notion + Slack with top-3 slip-risks (from `deal-coaching-next-best-action` Recipe 8).

**Result:** Leadership has roll-up by 5:30pm Friday.

### Example 2: Quarterly commit-accuracy review

**Goal:** End-of-quarter per-AE accuracy ranking; identify retraining needs.

**Steps:** Recipe 4 SQL produces per-AE accuracy % → Recipe 5 SQL produces slip + pull-in events → AEs with < 70% accuracy + > $200K in slips go to retraining; > 90% + pull-ins go to promote / mentor → render to manager 1:1 prep docs.

**Result:** Honest accuracy data; coaching is targeted.

### Example 3: Mid-quarter coverage alert

**Goal:** Coverage drops below 3x with 5 weeks to quota; trigger pipe-gen sprint.

**Steps:** Recipe 9 fires Slack alert → auto-create Notion plan "Pipe-Gen Sprint — June" with target $ → hand off to `outreach-salesloft-sequences` for new outbound + `account-research-deep` for ICP refresh.

**Result:** Coverage gap identified before quarter-end; sprint launches in days.

## Edge cases / gotchas

- **Auto-bucket isn't the final word** — AE judgment matters (e.g., backchannel exec sponsor not visible in MEDDIC). Allow override; log it for accuracy tracking.
- **Snapshots are everything.** Without weekly snapshots (Recipe 6), accuracy queries are impossible retroactively. Snapshot from Day 1.
- **AE-inflated commits** are the default failure mode. Manager review + published accuracy scores are the only counter-pressure.
- **Period definition matters**: fiscal quarter vs calendar month vs rolling 90 — pick one; mid-year change destroys trend data.
- **Quota drifts** — mid-year quota changes break accuracy comparison. Snapshot the quota each period too.
- **< 60% accuracy** = AE red flag; team-wide < 80% = over-committing culture, manager-level issue.
- **Slip ≠ loss.** Slipped commits may close next period; track slip recovery rate separately.
- **Pull-ins > 30% of best-case** = bucketing too pessimistic. Recalibrate.
- **Clari/BoostUp predictive ML is a black box.** Review model vs human bucketing monthly; favor the more accurate, document why.
- **New AE (< 1 quarter tenure)** has no accuracy history; use team median until data accumulates.
- **Currency**: report in one currency at snapshot moment, not at close. FX changes between snapshots = bad data.
- **Don't bucket-shop in the last week** of quarter. AEs move best-case → commit to make their number; the Friday-snapshot anchor prevents this from registering as "accurate".

## Sources

- Clari forecasting methods: https://www.clari.com/blog/sales-forecasting-methods/
- Gong Forecast product: https://www.gong.io/forecast/
- BoostUp forecasting (mid-market alt): https://www.boostup.ai/
- Sales forecasting accuracy 2026 benchmark: https://www.gong.io/labs/forecast-accuracy/
- Three-bucket forecast methodology (Sequoia): https://www.sequoiacap.com/article/sales-forecasting/
- Commit accuracy + AE coaching: https://www.gong.io/blog/commit-accuracy/
- Manual forecast in Google Sheets template: https://blog.hubspot.com/sales/sales-forecast-template
