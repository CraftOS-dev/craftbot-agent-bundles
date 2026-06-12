<!--
Source: https://www.clari.com/blog/sales-forecasting-methods/ + https://boostup.ai/ + https://aviso.com/
Forecasting — Clari + BoostUp + Aviso (June 2026 SOTA).
-->
# Forecasting — Clari + BoostUp + Aviso — SKILL

AI-driven forecasting platforms layer call/email/CRM signals into probability per deal. **Clari Align** enterprise standard. **BoostUp** mid-market. **Aviso** AI-driven alt. Three-bucket discipline (Commit / Best Case / Pipeline). Commit accuracy % per AE per quarter. Slip + pull-in tracking. Manual fallback via CRM + Sheets always works.

## When to use

- **Weekly forecast roll-up** — Friday 5pm; team + per-AE.
- **Commit accuracy review** — quarterly; per AE.
- **Slip + pull-in analysis** — what moved from commit/best-case at quarter end.
- **Coverage ratio monitoring** — daily; alert if < 3×.
- **Three-bucket discipline** — define + enforce bucket criteria.
- **Clari API integration** — sync CRM forecast → Clari snapshots.
- **Trigger phrases**: "forecast roll-up", "commit accuracy", "coverage ratio", "Clari", "BoostUp", "slip analysis", "three-bucket".

Do NOT use this skill for: **per-deal AE coaching** (use parent sales-agent `deal-coaching-next-best-action`); **pipeline data quality** (use `pipeline-metrics-velocity-conversion`); **board reporting** (use rollup output as input).

## Setup

```bash
# Clari — OAuth (Settings → API → Generate token)
export CLARI_API_KEY="<key>"
export CLARI_BASE="https://api.clari.com/v4"

# BoostUp — API token
export BOOSTUP_TOKEN="<token>"

# Aviso — API key
export AVISO_TOKEN="<token>"

# CRM + warehouse
export MATON_API_KEY="<key>"
export PG_URI="postgresql://..."
```

Required:
- Clari: enterprise plan with API access (~$1K-2K/seat/yr)
- BoostUp: mid-market (~$80-150/seat/mo)
- Aviso: enterprise (~$1K+/seat/yr)
- CRM (Salesforce/HubSpot) admin read access

## Common recipes

### Recipe 1: Three-bucket criteria (canonical)

```yaml
commit:
  meaning: "> 80% confidence — AE accountable to close in period"
  criteria:
    - MEDDIC >= 2.5/3 on all fields
    - economic_buyer_confirmed: true
    - mutual_action_plan_signed: true (for > 60-day cycles)
    - close_date <= period_end
    - verbal_close_confirmed: true
    - competition_known_and_position_confirmed: true
  forecast_value: 100% of amount
  miss_consequence: forecast accuracy hit; coaching trigger

best_case:
  meaning: "50-80% confidence — actively working risks"
  criteria:
    - MEDDIC >= 10 (most fields validated)
    - champion_confirmed: true
    - eb_awareness_confirmed: true
    - close_date <= period_end + 30d
  forecast_value: 50-80% of amount (or per-AE historical conversion)
  miss_consequence: tracked as slip

pipeline:
  meaning: "< 50% confidence — discovery complete"
  criteria:
    - discovery_complete: true
    - qualification_in_progress: true
  forecast_value: 0% commit; contributes to coverage only
  miss_consequence: none
```

### Recipe 2: Auto-bucket from MEDDIC score

```python
def auto_bucket(deal, current_period_end):
    """Return commit / best_case / pipeline based on deal data."""
    meddic = int(deal.get("meddic_score", 0) or 0)
    has_map_signed = deal.get("map_signed", False)
    verbal_close = deal.get("verbal_close_confirmed", False)
    champion_confirmed = deal.get("champion_confirmed", False)
    eb_confirmed = deal.get("economic_buyer_confirmed", False)
    close_date = deal.get("close_date")
    close_in_period = close_date and close_date <= current_period_end

    if (meddic >= 14 and has_map_signed and verbal_close
            and eb_confirmed and close_in_period):
        return "commit"
    if (meddic >= 10 and champion_confirmed and close_in_period):
        return "best_case"
    return "pipeline"
```

### Recipe 3: Weekly forecast doc generation

```python
import requests, os, collections
from datetime import datetime

QUARTER_START = "2026-07-01"
QUARTER_END   = "2026-09-30"
quota_team    = 2_500_000

# Pull all open deals via api-gateway (Salesforce)
q = f"""
SELECT Id, Name, Amount, CloseDate, StageName, Owner.Name,
       MEDDIC_Score__c, Champion_Confirmed__c, Economic_Buyer__c,
       Map_Signed__c, Verbal_Close__c, Forecast_Bucket_Override__c
FROM Opportunity
WHERE IsClosed = FALSE
  AND CloseDate >= {QUARTER_START}
  AND CloseDate <= {QUARTER_END}
"""
deals = requests.get(f"https://gateway.maton.ai/salesforce/services/data/v60.0/query",
                     params={"q": q},
                     headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"}).json()["records"]

buckets = collections.defaultdict(lambda: {"count":0, "sum":0, "deals":[]})
for d in deals:
    override = d.get("Forecast_Bucket_Override__c")
    bucket = override or auto_bucket(d, QUARTER_END)
    amount = float(d.get("Amount") or 0)
    buckets[bucket]["count"] += 1
    buckets[bucket]["sum"] += amount
    buckets[bucket]["deals"].append(d)

print(f"Forecast {QUARTER_START} → {QUARTER_END}")
print(f"Quota: ${quota_team:,}")
for b in ("commit","best_case","pipeline"):
    pct = 100 * buckets[b]["sum"] / quota_team
    print(f"  {b:10}: {buckets[b]['count']:3} deals, ${buckets[b]['sum']:,.0f} ({pct:.0f}% of quota)")

total = sum(buckets[b]["sum"] for b in ("commit","best_case","pipeline"))
coverage = total / quota_team
print(f"Total open pipeline: ${total:,.0f}  Coverage: {coverage:.1f}× (target 3-4×)")
```

### Recipe 4: Commit accuracy per AE per quarter (SQL)

```sql
WITH committed_at_start AS (
  SELECT owner_id, period_id, deal_id, amount
  FROM forecast_snapshots
  WHERE bucket = 'commit'
    AND snapshot_date = (SELECT MIN(snapshot_date) FROM forecast_snapshots WHERE period_id = '2026Q3')
),
closed_won_in_period AS (
  SELECT deal_id FROM fct_opportunities
  WHERE is_won = TRUE AND close_date BETWEEN '2026-07-01' AND '2026-09-30'
)
SELECT
  c.owner_id,
  COUNT(*) AS committed_deals,
  COUNT(*) FILTER (WHERE c.deal_id IN (SELECT deal_id FROM closed_won_in_period)) AS won,
  ROUND(100.0 * COUNT(*) FILTER (WHERE c.deal_id IN (SELECT deal_id FROM closed_won_in_period)) /
        NULLIF(COUNT(*),0), 1) AS accuracy_pct,
  SUM(c.amount) AS committed_value,
  SUM(c.amount) FILTER (WHERE c.deal_id IN (SELECT deal_id FROM closed_won_in_period)) AS won_value
FROM committed_at_start c
GROUP BY 1
ORDER BY 4 DESC;
```

Target: > 80%. Action: < 70% retrain; < 60% manager ride-along.

### Recipe 5: Slip + pull-in analysis

```sql
WITH commit_at_start AS (
  SELECT deal_id, owner_id, amount
  FROM forecast_snapshots
  WHERE bucket = 'commit' AND snapshot_date = '2026-07-04'  -- first Friday Q3
),
slips AS (
  SELECT c.deal_id, c.owner_id, c.amount, d.close_date
  FROM commit_at_start c
  JOIN fct_opportunities d USING (deal_id)
  WHERE d.close_date > '2026-09-30'  -- slipped past quarter
     OR (d.is_closed = FALSE AND NOW() > '2026-09-30')
),
pullins AS (
  SELECT d.deal_id, d.owner_id, d.amount
  FROM fct_opportunities d
  JOIN forecast_snapshots s ON s.deal_id = d.deal_id AND s.snapshot_date = '2026-07-04'
  WHERE d.is_won AND d.close_date <= '2026-09-30'
    AND s.bucket = 'best_case'   -- was best-case at start; closed early
)
SELECT 'slip' AS event, COUNT(*), SUM(amount) FROM slips
UNION ALL
SELECT 'pullin', COUNT(*), SUM(amount) FROM pullins;
```

### Recipe 6: Forecast snapshot (weekly cron)

```python
# Every Friday 5pm: snapshot all open deals + bucket
from datetime import date
import psycopg, os

snapshot_date = date.today().isoformat()
quarter = "2026Q3"

conn = psycopg.connect(os.environ['PG_URI'])
cur = conn.cursor()
for deal in deals:  # from Recipe 3
    bucket = deal.get("Forecast_Bucket_Override__c") or auto_bucket(deal, "2026-09-30")
    cur.execute("""
      INSERT INTO forecast_snapshots
        (snapshot_date, period_id, deal_id, owner_id, amount, bucket, current_close_date, meddic_score)
      VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
      ON CONFLICT (snapshot_date, deal_id) DO UPDATE
      SET bucket = EXCLUDED.bucket, amount = EXCLUDED.amount
    """, (snapshot_date, quarter, deal["Id"], deal["Owner"]["Name"],
          float(deal.get("Amount") or 0), bucket,
          deal["CloseDate"], int(deal.get("MEDDIC_Score__c") or 0)))
conn.commit()
```

### Recipe 7: Clari forecast snapshot push

```bash
curl -X POST "$CLARI_BASE/forecast/snapshots" \
  -H "Authorization: Bearer $CLARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "period": "2026-Q3",
    "snapshot_date": "2026-06-11",
    "rollup": {
      "team_total_quota": 2500000,
      "team_commit": 1450000,
      "team_best_case": 780000,
      "team_pipeline": 2200000,
      "team_closed_won": 320000
    }
  }'
```

### Recipe 8: Clari AE commit submission

```bash
curl -X POST "$CLARI_BASE/forecast/submissions" \
  -H "Authorization: Bearer $CLARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "period": "2026-Q3",
    "owner_id": "alice@co.com",
    "commit_amount": 425000,
    "best_case_amount": 280000,
    "submitted_at": "2026-06-11T17:00:00Z"
  }'
```

### Recipe 9: BoostUp predictive integration

```bash
# BoostUp computes its own AI-driven probabilities per deal
curl "https://api.boostup.ai/v1/forecast/deals?period=2026-Q3" \
  -H "Authorization: Bearer $BOOSTUP_TOKEN" \
  | jq '.[] | {deal_id, predicted_close_probability, recommended_bucket}'
# Compare predicted_bucket vs human-bucket; flag deltas > 2 levels
```

### Recipe 10: Coverage monitoring (daily)

```python
total_pipe = sum(buckets[b]["sum"] for b in ("commit","best_case","pipeline"))
won_qtd = 320_000  # already closed
quota_remaining = quota_team - won_qtd

coverage = total_pipe / quota_remaining if quota_remaining > 0 else float("inf")

if coverage < 3.0:
    slack_post("#sales-leadership",
               f":warning: COVERAGE: {coverage:.1f}× (target 3-4×). Push outbound + pipe-gen sprint.")
```

### Recipe 11: Weekly Friday digest (Slack + Notion)

```python
import requests, os

today_str = date.today().isoformat()
# Slack
requests.post("https://slack.com/api/chat.postMessage",
              headers={"Authorization": f"Bearer {os.environ['SLACK_TOKEN']}"},
              json={"channel": "#sales-leadership",
                    "text": f"""Forecast — {today_str}
Commit: ${buckets['commit']['sum']:,.0f} ({buckets['commit']['count']} deals)
Best Case: ${buckets['best_case']['sum']:,.0f} ({buckets['best_case']['count']} deals)
Coverage: {coverage:.1f}× quota
Top 3 slip risks: [list]
Top 3 pull-in candidates: [list]"""})

# Notion (via notion-mcp / api)
notion_payload = {
    "parent": {"database_id": os.environ['FORECAST_DB_ID']},
    "properties": {
        "Week": {"title": [{"text": {"content": f"Forecast {today_str}"}}]},
        "Commit": {"number": buckets['commit']['sum']},
        "BestCase": {"number": buckets['best_case']['sum']},
        "Pipeline": {"number": buckets['pipeline']['sum']},
        "Coverage": {"number": round(coverage, 2)}
    }
}
requests.post("https://api.notion.com/v1/pages",
              headers={"Authorization": f"Bearer {os.environ['NOTION_TOKEN']}",
                       "Notion-Version": "2022-06-28"},
              json=notion_payload)
```

### Recipe 12: Per-AE accuracy chart (matplotlib)

```python
import matplotlib.pyplot as plt
import pandas as pd

accuracy_df = pd.read_sql("""
SELECT owner_id, period_id,
       100.0 * SUM(CASE WHEN won THEN 1 ELSE 0 END) / COUNT(*) AS accuracy_pct
FROM commit_accuracy_history
GROUP BY 1,2
ORDER BY 2, 1
""", os.environ['PG_URI'])

# Pivot: one line per AE, x-axis = quarter
pivot = accuracy_df.pivot(index='period_id', columns='owner_id', values='accuracy_pct')
ax = pivot.plot(figsize=(12,6), marker='o')
ax.axhline(y=80, color='gray', linestyle='--', label='Target 80%')
ax.set_title('AE Commit Accuracy Trend')
ax.set_ylabel('Accuracy %')
ax.set_ylim(0, 110)
plt.legend(loc='lower left', ncol=2)
plt.tight_layout()
plt.savefig('ae_commit_accuracy.png', dpi=144)
```

## Examples

### Example 1: Friday 5pm forecast roll-up

**Goal:** Auto-generated forecast doc + Slack ping every Friday.

**Steps:**
1. Cron 5pm Friday → Recipe 3 buckets all open deals.
2. Recipe 6 snapshots to postgres.
3. Recipe 10 — coverage check; alert if low.
4. Recipe 11 — render to Slack + Notion.
5. Manager 1:1 prep doc auto-generated; AE prep their submissions for Recipe 8.

**Result:** Leadership has roll-up by 5:30pm Friday; AEs prep with data.

### Example 2: Quarterly commit accuracy review

**Goal:** End-of-quarter per-AE accuracy ranking; coaching decisions.

**Steps:**
1. Recipe 4 SQL — accuracy per AE.
2. Recipe 5 SQL — slip + pull-in events.
3. AE with < 70% accuracy + > $200K slip → retraining.
4. AE > 90% + meaningful pull-ins → promote / mentor.
5. Recipe 12 — visualize accuracy trend.
6. Render to manager 1:1 prep deck.

**Result:** Coaching decisions are data-backed; not gut-feel.

### Example 3: Coverage warning mid-quarter

**Goal:** Week 6 of quarter, coverage drops to 2.4×.

**Steps:**
1. Recipe 10 fires Slack alert.
2. Auto-create notion plan "Pipe-Gen Sprint — week 7-10".
3. Hand off to sales-agent `outreach-salesloft-sequences` for new outbound sprint.
4. Daily coverage check during sprint.
5. Coverage recovers to 3.6× by week 10.

**Result:** Quota threat caught early; corrective sprint launched.

## Edge cases / gotchas

- **Auto-bucket isn't the final word** — AE judgment matters (backchannel sponsor, off-CRM signals). Allow override; track override accuracy.
- **Snapshots are everything** — without weekly snapshots, accuracy queries impossible. Start Day 1.
- **AE-inflated commits** — pervasive failure mode. Manager review + published accuracy scores are the only counter-pressure.
- **Period definition** — fiscal quarter vs calendar month vs rolling 90 — pick one; mid-year change destroys trend data.
- **Mid-period quota changes** — snapshot the quota too; otherwise accuracy comparison breaks.
- **< 60% accuracy** = AE red flag; team-wide < 80% = over-committing culture issue.
- **Slip ≠ loss** — slipped commits often close next period; track slip recovery rate.
- **Pull-ins > 30% of best-case** = bucketing too pessimistic; recalibrate.
- **Clari/BoostUp ML is a black box** — review model vs human bucketing monthly; document discrepancies.
- **New AE (< 1 quarter tenure)** — no accuracy history; use team median until data accumulates.
- **Currency** — report in single currency at snapshot moment; FX changes between snapshots = bad data.
- **Don't bucket-shop end of quarter** — AEs move best-case → commit to make number; Friday snapshot anchor prevents this from registering as "accurate".
- **Clari public API is limited** — most config is in-app. Use api-gateway proxy.
- **Stage-name dependency** — bucket criteria reference stage; renaming stages mid-period breaks rules.
- **MEDDIC score field maintenance** — if AE doesn't update, auto-bucket misses. Validation rule (`salesforce-admin-custom-fields-flows`) enforces MEDDIC update on stage advance.
- **Multi-AE deals (splits)** — bucket the deal, not the rep slice. Or split allocation per Spiff.

## Sources

- [Clari forecasting methods](https://www.clari.com/blog/sales-forecasting-methods/)
- [Clari Align product](https://www.clari.com/products/align/)
- [BoostUp (mid-market forecasting)](https://boostup.ai/)
- [Aviso (AI forecasting)](https://aviso.com/)
- [Gong Forecast (call-data-driven)](https://www.gong.io/forecast/)
- [Sales forecasting accuracy benchmark (Gong Labs 2026)](https://www.gong.io/labs/forecast-accuracy/)
- [Three-bucket methodology (Sequoia)](https://www.sequoiacap.com/article/sales-forecasting/)
- [Commit accuracy + coaching (Gong)](https://www.gong.io/blog/commit-accuracy/)
- [Manual forecast template (HubSpot)](https://blog.hubspot.com/sales/sales-forecast-template)
