<!--
Sources: Klue battlecard analytics https://klue.com/
         Klue × Salesforce integration https://klue.com/salesforce
         Klue — Sales Battlecard Software 2026 https://klue.com/topics/best-sales-battlecard-software
         Salesforce Sales Cloud analytics https://www.salesforce.com/sales/analytics/
Companion playbook: role.md → "Battlecard authoring playbook" Step 6 + "QBR deck template" + "Antipattern 8 — Ignoring CI program metrics"
-->

# CI program metrics (sales adoption rate + win-rate uplift + battlecard open-rate)

Three operational KPIs that turn a CI program from shelfware into a measurable ROI surface: (1) rep-side battlecard open-rate per deal; (2) competitive-deal win-rate trend per competitor; (3) CI-influenced revenue (closed-won where rep cites CI use). Quarterly CI program review back to PMM / sales leadership tells the budget-defense story.

## When to use

- "Show me CI program metrics"
- Quarterly QBR for the CI program
- Budget defense round for CI tooling / headcount
- Rep-level engagement diagnostics (top + bottom quartile coaching)
- Per-competitor program-coverage decisions (which to deepen / which to drop)
- Post-launch measurement for a new battlecard / kill sheet

## When NOT to use

- One battlecard's effectiveness review → use the battlecard's individual open-rate + adoption metric (subset of this)
- Generic Salesforce reporting → that's revenue ops, not CI
- Win/loss interview content → use `win-loss-ci-integration-klue-insider`

## Setup

```bash
# Klue / Crayon admin API for delivery metrics (paid)
export KLUE_API_KEY="..."
export KLUE_API_BASE="https://api.klue.com/v1"

# Crayon (alternative)
export CRAYON_API_KEY="..."

# Salesforce REST + Reports
export SF_USERNAME="..."
export SF_PASSWORD="..."
export SF_SECURITY_TOKEN="..."
export SF_INSTANCE_URL="https://your-instance.my.salesforce.com"

# PostgreSQL warehouse (for warehoused funnel)
export PG_DSN="postgresql://..."

# Plotly / Altair for QBR charts via skills
```

MCPs in `agent.yaml`: `salesforce-api`, `postgresql-mcp`, `notion-mcp`, `slack-mcp`, `gmail-mcp`.

## Common recipes

### Recipe 1: Klue admin — battlecard open-rate per rep

```bash
curl -H "Authorization: Bearer $KLUE_API_KEY" \
  "$KLUE_API_BASE/analytics/battlecard-opens?\
group_by=user_id&\
since=2026-04-01&\
end=2026-06-30"
```

Returns: per-rep per-battlecard open counts. Calculate open-rate vs eligible deals (where competitor field set).

### Recipe 2: Klue admin — open-rate per competitor

```bash
curl -H "Authorization: Bearer $KLUE_API_KEY" \
  "$KLUE_API_BASE/analytics/battlecard-opens?\
group_by=competitor_id&\
since=2026-04-01&\
end=2026-06-30"
```

### Recipe 3: Salesforce — eligible deals per competitor

```python
from simple_salesforce import Salesforce
sf = Salesforce(username=os.environ["SF_USERNAME"], password=..., security_token=...)
q = """
SELECT Id, Name, Competitor__c, StageName, Amount, CloseDate, OwnerId
FROM Opportunity
WHERE Competitor__c != NULL
  AND CloseDate >= 2026-04-01
  AND CloseDate <= 2026-06-30
"""
deals = sf.query_all(q)["records"]
```

### Recipe 4: Compute open-rate per rep

```python
import pandas as pd
deals_df = pd.DataFrame(deals)
opens_df = pd.DataFrame(fetch_klue_opens())
# Join on (OwnerId, Competitor__c) → (user_id, competitor_id)
merged = deals_df.merge(opens_df, left_on=["OwnerId","Competitor__c"],
                                  right_on=["user_id","competitor_id"], how="left")
merged["opened"] = merged["open_count"].fillna(0) > 0
open_rate = merged.groupby("OwnerId")["opened"].mean()
```

### Recipe 5: Competitive win-rate trend per competitor

```python
# Per competitor, quarter-over-quarter win-rate
deals_df["quarter"] = pd.PeriodIndex(deals_df["CloseDate"], freq="Q")
deals_df["won"] = deals_df["StageName"] == "Closed Won"
wr = deals_df.groupby(["Competitor__c","quarter"])["won"].mean().unstack()
```

### Recipe 6: CI-influenced revenue calc

```python
# Salesforce custom field: CI_Used__c (Boolean) — rep flags during close
# Custom field: CI_Influence__c (Picklist: 'High','Medium','Low','None')
ci_influenced = deals_df[(deals_df["StageName"] == "Closed Won")
                       & (deals_df["CI_Used__c"] == True)
                       & (deals_df["CI_Influence__c"].isin(["High","Medium"]))]
total_influenced = ci_influenced["Amount"].sum()
```

Caveat: rep self-reports influence; not a clean experimental design but the SaaS-CI industry standard.

### Recipe 7: Per-deal open-rate × win-rate scatter (engagement insight)

```python
import plotly.express as px
agg = merged.groupby("OwnerId").agg(
    open_rate=("opened","mean"),
    win_rate=("won","mean"),
    deal_count=("Id","count"),
)
px.scatter(agg, x="open_rate", y="win_rate", size="deal_count",
           title="Per-rep open-rate vs win-rate")
```

Surfaces: high-open + high-win = top performer; low-open + high-win = doesn't need CI; high-open + low-win = needs coaching on application; low-open + low-win = CI gap.

### Recipe 8: Top + bottom quartile rep callouts

```python
q1, q3 = agg["open_rate"].quantile([0.25, 0.75])
top    = agg[agg["open_rate"] >= q3].sort_values("win_rate", ascending=False).head(5)
bottom = agg[agg["open_rate"] <= q1].sort_values("win_rate").head(5)
```

### Recipe 9: Lost-reason histogram per competitor

```python
lost = deals_df[deals_df["StageName"] == "Closed Lost"]
histogram = lost.groupby(["Competitor__c","Lost_Reason__c"])["Id"].count().unstack()
```

### Recipe 10: Auto-generate QBR pptx (10-15 slides)

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()
def add_title_slide(title, subtitle):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = title
    slide.placeholders[1].text = subtitle

# Per role.md QBR template:
add_title_slide("CI Program QBR — Q2 FY2026", "CI Team")
# Slide 2 — Exec summary (numbers); 3 — open-rate per rep; 4 — open-rate per competitor;
# 5 — win-rate trend; 6 — lost-reason histogram; 7 — CI-influenced revenue;
# 8 — case study win; 9 — case study loss; 10 — QoQ vs commits;
# 11 — next-quarter focus; 12 — asks; 13 — sources / methodology
prs.save("ci_qbr_q2_2026.pptx")
```

### Recipe 11: PostgreSQL warehouse query

```sql
-- For deeper longitudinal trends with sufficient deal volume
SELECT
  c.competitor_name,
  date_trunc('quarter', o.close_date) AS quarter,
  COUNT(*) FILTER (WHERE o.stage = 'Closed Won') * 1.0 / COUNT(*) AS win_rate,
  SUM(CASE WHEN o.stage = 'Closed Won' AND o.ci_used THEN o.amount ELSE 0 END) AS influenced_rev
FROM opportunities o
JOIN competitors c ON c.id = o.competitor_id
WHERE o.close_date >= '2024-01-01'
GROUP BY 1, 2
ORDER BY 1, 2;
```

### Recipe 12: Per-battlecard usage analytics

```bash
# Klue — usage by individual battlecard
curl -H "Authorization: Bearer $KLUE_API_KEY" \
  "$KLUE_API_BASE/analytics/battlecards/$BC_ID/usage?since=2026-04-01"
```

Returns: opens, dwell time, pane-by-pane engagement (pane 2 — objections — usually highest).

### Recipe 13: Self-build (no Klue) — Lightning component logging

```javascript
// Each open of the Lightning battlecard component writes an Activity record
// with Type='BattlecardOpen', Subject=competitor, ContactId/OpportunityId
// Salesforce-native analytics on Activity then gives open-rate per rep.
```

### Recipe 14: Slack monthly snapshot

```python
def monthly_snapshot(period):
    return {
        "open_rate_overall": "62%",
        "open_rate_top_quartile_rep": "94%",
        "open_rate_bottom_quartile_rep": "12%",
        "win_rate_competitive": "47% (+4pp QoQ)",
        "ci_influenced_rev": "$2.4M (24% of competitive closed-won)",
        "top_competitor_drag": "Acme (32% win-rate, -8pp QoQ)",
    }
# Post to #ci-leadership monthly
```

## Examples

### Example 1: Quarterly QBR for sales leadership

**Goal:** Render the QBR deck per role.md template; tell the ROI story.

**Steps:**
1. Recipes 1-9 → pull all metrics.
2. Recipe 10 → render pptx with charts via Plotly export.
3. Sources slide cites methodology + caveats.
4. Send via gmail-mcp; Slack `#ci-leadership` post links.

**Result:** 12-slide deck; 2 case studies; per-rep + per-competitor + lost-reason breakdowns.

### Example 2: Rep coaching — bottom-quartile open-rate

**Goal:** Coach 5 reps with lowest battlecard open-rate.

**Steps:**
1. Recipe 8 → identify bottom 5.
2. Cross-reference Recipe 7 (open vs win) — are they low-win too?
3. If yes → 30-min coaching session per rep.
4. Re-measure 60 days; expected open-rate uplift.

### Example 3: Per-competitor coverage decision

**Goal:** Decide which competitors to deepen vs drop coverage.

**Steps:**
1. Recipes 2 + 5 + 6 → per-competitor open-rate, win-rate trend, influenced revenue.
2. Per role.md: "Drop competitors that haven't been in a deal in 2 quarters."
3. Reallocate coverage budget; document in CI program plan.

### Example 4: Self-build (no Klue) program metrics

**Goal:** Run program metrics without paid Klue/Crayon.

**Steps:**
1. Recipe 13 → instrument Lightning component for opens.
2. Recipe 3 → Salesforce activity + opportunity data.
3. Recipe 11 → warehouse query for trend.
4. Recipe 10 → pptx renderer.

**Result:** ~85% metric coverage on a $0 incremental cost; no per-pane dwell time without Klue.

## Edge cases / gotchas

- **Small deal volume** — competitive deals per competitor may be 10-30/quarter; win-rate has wide CI. Use ≥4 quarters before drawing strong conclusions.
- **Self-reported CI influence bias** — reps under-report influence on losses, over-report on wins. Triangulate with battlecard-opened-in-window signal.
- **Selection bias** — reps who open battlecards more may be better reps; not all uplift attributable to CI. Use difference-in-differences against pre/post battlecard launch.
- **Klue / Crayon native metrics** — usually battlecard-opens; sometimes pane-level. Limit per plan tier.
- **Salesforce custom-field hygiene** — Competitor__c, CI_Used__c, CI_Influence__c, Lost_Reason__c all need to be required during close. RevOps coordination critical.
- **Win-rate trends sensitive to seasonality** — Q1 vs Q4 differ; year-over-year compare, not just QoQ.
- **Stage-change manipulation** — reps move to Closed Lost late in quarter; cohort by opportunity-created-date, not close-date for trend.
- **Open-rate inflation** — rep opens battlecard once at end of quarter to "show usage"; smooth with dwell-time gate (>15s).
- **Lost-reason picklist drift** — Sales Ops changes picklist values; align history with current values via mapping table.
- **PII** — owner-name dropouts at quarter end; lock as of close date.
- **Klue / Crayon ROI claims** — vendor claims (e.g., 30% win-rate uplift) are aggregate; YMMV. Use internal pre/post measurement.
- **Don't measure CI in a vacuum** — pair with: sales enablement training compliance + onboarding speed.
- **PROACTIVE.md cadence** — monthly snapshot (Recipe 14); quarterly QBR (Recipe 10).
- **Provenance footer on QBR** — cite data sources + methodology + caveats; per role.md "QBR deck template" slide 13.

## Sources

- Klue battlecard analytics — https://klue.com/
- Klue × Salesforce integration — https://klue.com/salesforce
- Klue — Sales Battlecard Software 2026 — https://klue.com/topics/best-sales-battlecard-software
- Salesforce Sales Cloud analytics — https://www.salesforce.com/sales/analytics/
- role.md → "Battlecard authoring playbook" Step 6 + "Antipattern 8" + "QBR deck template"

## Related skills

- `ci-delivery-slack-crm-klue-insider` — where the battlecards live (open-rate flows back here)
- `battlecard-authoring-maintenance` — what gets opened
- `win-loss-ci-integration-klue-insider` — win-loss reasons feed lost-reason histogram
- `continuous-competitor-monitoring-klue-kompyte-crayon` — coverage decisions per Example 3
- `hot-deals-ci-deal-level` — deal-level CI flows into CI-influenced revenue
