<!--
Source: https://www.gong.io/blog/win-loss-analysis/ + https://www.klue.com/ + https://www.crayon.co/ + https://www.clozd.com/
Win/loss reporting at scale — Klue + Crayon win-loss platforms + Gong call-mining + dbt-modeled CRM rollup (June 2026 SOTA).
-->
# Win/Loss Reporting at Scale — SKILL

Quarterly + annual win/loss rollup with structured tags (industry, deal size tier, sales cycle, primary competitor, loss reason). **Klue** + **Crayon** for competitive win-loss platforms; **Gong** for call-mining loss reasons from actual conversations; **Clozd** for outsourced buyer interviews; CRM + dbt + matplotlib for the analytics layer. Drift detection: which competitors trend up in losses? Which loss reasons are emerging? Scale = pattern-finding across 100s of deals, not per-deal post-mortem.

## When to use

- **Quarterly win/loss rollup** — pivot all closed deals by competitor / segment / loss reason.
- **Drift detection** — competitor X mentioned in 40% of losses, up from 15% last quarter.
- **Loss-reason hygiene** — audit which deals have empty loss_reason, force-fill via flow.
- **Gong call-mining** — extract loss themes from recorded calls (vs. AE self-report).
- **Klue / Crayon battlecard refresh trigger** — competitor wins spike → battlecard update needed.
- **Executive QBR slide** — top 5 win drivers / top 5 loss drivers, year-over-year.
- **Trigger phrases**: "win/loss report", "loss reason rollup", "competitor analysis", "Klue", "Crayon", "Gong call mining", "Clozd interviews", "QBR slide".

Do NOT use this skill for: **per-deal loss post-mortem authoring** (use `sales-agent` win-loss skill); **battlecard authoring** (use `sales-agent` enablement skill); **forecasting** (use `forecasting-clari-boostup-aviso`).

## Setup

```bash
# Klue — API key (Admin → API)
export KLUE_TOKEN="<token>"
export KLUE_BASE="https://api.klue.com/v1"

# Crayon — API key (Settings → Integrations → API)
export CRAYON_TOKEN="<token>"
export CRAYON_BASE="https://api.crayon.co/v1"

# Gong — OAuth client + secret (Settings → API)
export GONG_TOKEN="<token>"
export GONG_BASE="https://api.gong.io/v2"

# Clozd — read-only API (rare; most Clozd consumption is exported reports)
export CLOZD_TOKEN="<token>"

# Salesforce + warehouse
export MATON_API_KEY="<key>"
export PG_CONN="postgres://user:pass@warehouse.host/db"

# Python deps
pip install pandas matplotlib psycopg2-binary requests
```

Required:
- Klue or Crayon competitive-intel subscription (~$2K-10K/mo enterprise)
- Gong Premium for call API + Smart Tracker access
- Salesforce custom field `Loss_Reason__c` populated (validation rule enforced)
- dbt model `fct_opportunities` with `win_loss_status`, `loss_reason`, `primary_competitor` columns

## Common recipes

### Recipe 1: Loss reason taxonomy (canonical)

```yaml
loss_reason_categories:
  - category: "Competitor"
    sub_reasons:
      - "Chose CompetitorA"
      - "Chose CompetitorB"
      - "Chose DIY/In-house"
      - "Chose status quo (no action)"

  - category: "Budget"
    sub_reasons:
      - "Budget reallocated mid-cycle"
      - "Budget too small for our pricing"
      - "Procurement froze spend"

  - category: "Timing"
    sub_reasons:
      - "Project delayed > 6 months"
      - "Re-org, new buyer"
      - "Decision deferred to next FY"

  - category: "Product fit"
    sub_reasons:
      - "Missing feature (specify)"
      - "Integration gap (specify)"
      - "Compliance/security blocker"

  - category: "Process"
    sub_reasons:
      - "Lost champion"
      - "Multi-thread failure"
      - "Pricing rejected (specify discount asked)"

  - category: "Unknown / no decision"
    sub_reasons:
      - "Ghosted"
      - "No formal close"
```

Enforce via Salesforce validation rule: `Loss_Reason__c` required when `StageName = 'Closed Lost'`.

### Recipe 2: Quarterly rollup SQL (dbt-modeled warehouse)

```sql
-- Run via postgresql-mcp against warehouse
SELECT
  industry,
  CASE
    WHEN amount < 50000 THEN 'SMB'
    WHEN amount < 250000 THEN 'Mid-Market'
    ELSE 'Enterprise'
  END AS deal_size_tier,
  CASE
    WHEN cycle_days < 30 THEN '< 30d'
    WHEN cycle_days < 90 THEN '30-90d'
    WHEN cycle_days < 180 THEN '90-180d'
    ELSE '> 180d'
  END AS cycle_band,
  primary_competitor,
  win_loss_status,
  loss_reason,
  COUNT(*) AS deal_count,
  SUM(amount) AS total_value
FROM fct_opportunities
WHERE close_date >= DATE '2026-07-01' AND close_date < DATE '2026-10-01'
  AND is_closed = TRUE
GROUP BY 1, 2, 3, 4, 5, 6
ORDER BY total_value DESC;
```

### Recipe 3: Salesforce SOQL fallback (no warehouse)

```bash
sf data query --target-org prod \
  --query "SELECT Id, Name, Amount, StageName, CloseDate, Industry, Primary_Competitor__c, Loss_Reason__c, Days_In_Pipeline__c FROM Opportunity WHERE IsClosed = TRUE AND CloseDate >= 2026-07-01 AND CloseDate < 2026-10-01" \
  --bulk --wait 30 --result-format csv > q3_2026_closed.csv
```

### Recipe 4: Drift detection (current quarter vs prior 4Q)

```python
import pandas as pd

current_q = pd.read_csv("q3_2026_closed.csv")
prior_4q = pd.read_csv("prior_4q_closed.csv")

# Filter to losses only
cur_loss = current_q[current_q["StageName"] == "Closed Lost"]
prior_loss = prior_4q[prior_4q["StageName"] == "Closed Lost"]

# Competitor mention rate
cur_rates = cur_loss["Primary_Competitor__c"].value_counts(normalize=True)
prior_rates = prior_loss["Primary_Competitor__c"].value_counts(normalize=True)

drift = (cur_rates - prior_rates).fillna(cur_rates).sort_values(ascending=False)
emerging_threats = drift[drift > 0.10]  # > 10 pp increase
print("Emerging competitive threats:")
print(emerging_threats)

# Loss reason drift
cur_reasons = cur_loss["Loss_Reason__c"].value_counts(normalize=True)
prior_reasons = prior_loss["Loss_Reason__c"].value_counts(normalize=True)
reason_drift = (cur_reasons - prior_reasons).fillna(cur_reasons).sort_values(ascending=False)
print("\nLoss reason drift:")
print(reason_drift[abs(reason_drift) > 0.05])
```

### Recipe 5: Klue — pull competitive intel mentions

```bash
# Get all competitors tracked in Klue
curl -s "$KLUE_BASE/competitors" \
  -H "Authorization: Bearer $KLUE_TOKEN" | jq '.[] | {id, name}'

# Get win-loss insights logged for a competitor
curl -s "$KLUE_BASE/insights?competitor_id=42&type=win_loss&since=2026-07-01" \
  -H "Authorization: Bearer $KLUE_TOKEN" | jq '.results[]'

# Battlecard performance — view + share count last 90 days
curl -s "$KLUE_BASE/battlecards/42/analytics?since=2026-04-01" \
  -H "Authorization: Bearer $KLUE_TOKEN" | jq .
```

### Recipe 6: Crayon — competitor activity timeline

```bash
# Pull competitor's recent product / pricing / messaging changes
curl -s "$CRAYON_BASE/competitors/42/intel?since=2026-07-01&types=pricing,product,messaging" \
  -H "Authorization: Bearer $CRAYON_TOKEN" | jq .

# Get win-loss linked to a competitor (if Crayon-Salesforce sync enabled)
curl -s "$CRAYON_BASE/competitors/42/deals?status=lost&since=2026-07-01" \
  -H "Authorization: Bearer $CRAYON_TOKEN"
```

### Recipe 7: Gong — call-mining loss themes

```bash
# Find calls on lost deals in period
curl -X POST "$GONG_BASE/calls/extensive" \
  -H "Authorization: Bearer $GONG_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "fromDateTime": "2026-07-01T00:00:00Z",
      "toDateTime": "2026-10-01T00:00:00Z",
      "scopes": [{"workspaceId": "your-ws-id"}]
    },
    "contentSelector": {
      "context": "Extended",
      "exposedFields": {
        "content": {"trackers": true, "topics": true, "brief": true, "highlights": true},
        "interaction": {"sentiment": true}
      }
    }
  }' | jq '.calls[]'
```

### Recipe 8: Gong Smart Trackers — competitor mention rate

```bash
# Smart Trackers are keyword-tracking. Pull mention counts:
curl -s "$GONG_BASE/stats/activity/trackers?fromDateTime=2026-07-01T00:00:00Z&toDateTime=2026-10-01T00:00:00Z" \
  -H "Authorization: Bearer $GONG_TOKEN" | jq '.records[] | {trackerName, callsCount, occurrencesCount}'
```

Pre-configured trackers: `CompetitorA`, `CompetitorB`, `Pricing Objection`, `Integration Gap`, `Lost Champion`. SalesOps maintains.

### Recipe 9: Call-to-deal join (Gong call → SF opp → loss reason)

```python
import requests, pandas as pd

# Pull Gong calls with sentiment + trackers
gong_calls = requests.post(f"{GONG_BASE}/calls/extensive", ...).json()["calls"]

call_df = pd.DataFrame([{
    "callId": c["metaData"]["id"],
    "deal_id": c["context"]["objects"][0].get("objectId") if c.get("context") else None,
    "trackers": [t["name"] for t in c.get("content", {}).get("trackers", [])],
    "sentiment_score": c.get("interaction", {}).get("sentiment", {}).get("score"),
} for c in gong_calls])

# Join to Salesforce losses
sf = pd.read_csv("q3_2026_closed.csv")
losses = sf[sf["StageName"] == "Closed Lost"]
joined = call_df.merge(losses, left_on="deal_id", right_on="Id")

# Common loss themes — which trackers fired on lost deals?
exploded = joined.explode("trackers")
loss_themes = exploded.groupby("trackers").size().sort_values(ascending=False)
print(loss_themes.head(15))
```

### Recipe 10: Win driver inverse — what wins?

```python
wins = sf[sf["StageName"] == "Closed Won"]
win_join = call_df.merge(wins, left_on="deal_id", right_on="Id")
win_exploded = win_join.explode("trackers")
win_themes = win_exploded.groupby("trackers").size().sort_values(ascending=False)

# Sentiment delta — wins should skew positive
print("Win sentiment median:", win_join["sentiment_score"].median())
print("Loss sentiment median:", joined["sentiment_score"].median())
```

### Recipe 11: Render quarterly chart pack

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Win rate by segment
seg_wr = current_q.groupby("deal_size_tier").apply(
    lambda g: (g["StageName"] == "Closed Won").mean()
)
axes[0,0].bar(seg_wr.index, seg_wr.values)
axes[0,0].set_title("Win Rate by Segment — Q3 2026")
axes[0,0].set_ylabel("Win rate")

# Loss reason mix
loss_reasons = cur_loss["Loss_Reason__c"].value_counts()
axes[0,1].pie(loss_reasons.values, labels=loss_reasons.index, autopct="%1.1f%%")
axes[0,1].set_title("Loss Reason Mix — Q3 2026")

# Competitor mentions YoY
axes[1,0].bar(cur_rates.head(10).index, cur_rates.head(10).values, label="Q3 2026")
axes[1,0].bar(prior_rates.reindex(cur_rates.head(10).index).fillna(0).index,
              prior_rates.reindex(cur_rates.head(10).index).fillna(0).values,
              alpha=0.5, label="Prior 4Q avg")
axes[1,0].legend()
axes[1,0].set_title("Competitor Loss Mentions")

# Cycle band x outcome
ct = pd.crosstab(current_q["cycle_band"], current_q["StageName"], normalize="index")
ct.plot(kind="bar", stacked=True, ax=axes[1,1])
axes[1,1].set_title("Outcome by Cycle Length")

plt.tight_layout()
plt.savefig("q3_2026_winloss_chartpack.png", dpi=150)
```

### Recipe 12: Render to Notion QBR page

```bash
# After chart pack generated, push summary + chart to notion via notion-mcp
# Summary doc structure:
# - Headline: "Q3 2026 — 32% win rate; CompetitorA mentions in losses up 12pp"
# - Top 5 win drivers
# - Top 5 loss drivers
# - Drift alerts (competitors trending up, reasons trending up)
# - Battlecard refresh recommendations (from Klue/Crayon)
# - YoY chart pack image
# - AE-level win rate ranking
```

### Recipe 13: Force-fill missing loss reasons (data hygiene)

```bash
# Find closed-lost deals with empty Loss_Reason__c
sf data query --target-org prod \
  --query "SELECT Id, Name, Owner.Name, CloseDate FROM Opportunity WHERE StageName = 'Closed Lost' AND Loss_Reason__c = NULL AND CloseDate >= 2026-07-01" \
  --result-format csv > missing_loss_reason.csv

# Slack the owners with link to fill
python -c "
import pandas as pd, requests
df = pd.read_csv('missing_loss_reason.csv')
for _, r in df.iterrows():
    requests.post('https://slack.com/api/chat.postMessage', json={
        'channel': '@' + r['Owner.Name'].lower().replace(' ', '.'),
        'text': f\"Loss reason missing on {r['Name']} (closed {r['CloseDate']}). Please update: https://app.salesforce.com/{r['Id']}\"
    }, headers={'Authorization': 'Bearer $SLACK_TOKEN'})
"
```

### Recipe 14: api-gateway fallback

```bash
curl "https://gateway.maton.ai/klue/v1/insights?type=win_loss&since=2026-07-01" \
  -H "Authorization: Bearer $MATON_API_KEY"

curl -X POST "https://gateway.maton.ai/gong/v2/calls/extensive" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

## Examples

### Example 1: Q3 QBR win/loss chart pack

**Goal:** Produce the 4-chart deck for CRO's quarterly business review.

**Steps:**
1. Recipe 3 — pull Q3 2026 closed deals from Salesforce.
2. Recipe 2 — same data from dbt warehouse if available (richer joins).
3. Recipe 4 — drift detection against prior 4Q.
4. Recipe 7 + 9 — Gong call mining; join trackers to lost deals.
5. Recipe 11 — render chart pack PNG.
6. Recipe 12 — push to notion QBR page; alert CRO via slack.

**Result:** CRO walks into QBR with quantitative win/loss view + competitor drift alerts + recommended battlecard refreshes.

### Example 2: Competitor X emergent threat detection

**Goal:** Detect that CompetitorX has gone from 5% loss mentions to 25% in two quarters.

**Steps:**
1. Run Recipe 4 monthly (rolling 90-day vs prior 9-month average).
2. Alert in Slack if any competitor's loss mention rate jumps > 10 percentage points.
3. Recipe 5 (Klue) or Recipe 6 (Crayon) — pull CompetitorX recent intel (pricing change? new product?).
4. Recipe 7 — pull Gong call snippets where CompetitorX was mentioned.
5. Render brief to enablement team — battlecard refresh + objection-handling update.

**Result:** SalesOps catches competitive threats early, not in the next QBR.

### Example 3: Loss reason data hygiene push

**Goal:** Get loss_reason completion rate from 60% → 90%.

**Steps:**
1. Recipe 13 — find missing-reason deals from last 30 days.
2. Slack auto-nag deal owner + manager.
3. Deploy validation rule (use `salesforce-admin-custom-fields-flows`) requiring loss_reason at Closed Lost stage advance.
4. Weekly completion-rate dashboard in `notion`.
5. Drop in coaching loop with managers when team-level fill rate < 85%.

**Result:** Win/loss reporting moves from "AE remembered to fill" to enforced source of truth.

## Edge cases / gotchas

- **AE-reported loss reason is biased** — AEs prefer "Budget" or "Timing" (not their fault). Gong call-mining (Recipe 7-9) reveals what was actually discussed; reconcile both sources.
- **Free-text loss reasons** — useless for rollup. Force picklist via Salesforce field-type + validation rule.
- **Loss reasons change over time** — last quarter's "lost to CompetitorX" might now be "lost to status quo" after rep talks to buyer. Snapshot the field state at close, not as-of-today.
- **Closed-lost ≠ failed deal** — some closed-lost are "deferred re-engage in 6 months." Tag separately or these distort drift detection.
- **Gong tracker hits include all calls** — including pre-sales conversations with prospects who didn't become deals. Filter to calls linked to opportunity.
- **Klue + Crayon overlap with Salesforce custom field** — three sources of "primary competitor" disagree. Pick CRM as source of truth, Klue/Crayon as enrichment color.
- **Sample-size warning** — < 20 lost deals in a segment doesn't support pattern claims. Bucket smaller segments or annotate confidence.
- **Long sales cycles skew quarter rollup** — deal opened 9 months ago, closed-lost this quarter. Attribute to which quarter's pipeline? Both views (close-date vs created-date cohort).
- **AE turnover noise** — if an AE leaves and their unworked deals close-lost, attribute to "owner transition" reason, not legit loss patterns.
- **Pricing-as-loss-reason is often a proxy** — AEs blame price when real issue was value framing. Cross-check with Gong "Pricing Objection" tracker — did the buyer actually object on dollars or on ROI clarity?
- **Klue battlecard analytics undercount** — battlecards viewed in CRM via embed aren't always tracked. Use Gong tracker hits + Klue views in combination.
- **Clozd / RIVA outsourced interviews** — high-quality but ~$500-1500 per interview. Reserve for top-10 lost deals quarterly. Don't try to scale.
- **Window function performance on dbt model** — running 12-quarter trend on `fct_opportunities` without partitioning crawls. Materialize a `fct_winloss_quarterly` rollup table.
- **Salesforce CloseDate vs LastModifiedDate** — `IsClosed=TRUE` doesn't equal "closed this quarter." Filter on CloseDate.

## Sources

- [Gong Win-Loss Analysis Guide](https://www.gong.io/blog/win-loss-analysis/)
- [Gong Calls API — Extensive](https://app.gong.io/settings/api/documentation#overview)
- [Klue Win-Loss Solution](https://klue.com/use-cases/win-loss/)
- [Klue API Documentation](https://docs.klue.com/api/)
- [Crayon Competitive Intel Platform](https://www.crayon.co/)
- [Crayon Developer Docs](https://help.crayon.co/hc/en-us/sections/360008729494-API)
- [Clozd Buyer Interview Methodology](https://www.clozd.com/methodology)
- [Salesforce Opportunity Loss Reason — Trailhead](https://help.salesforce.com/s/articleView?id=sf.customize_opp_stages.htm)
- [dbt — Modeling Win/Loss in the Warehouse](https://docs.getdbt.com/docs/build/sql-models)
- [Pavilion — Win/Loss Best Practices](https://www.joinpavilion.com/resources/win-loss-analysis-guide)
