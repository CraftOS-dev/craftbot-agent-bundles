<!--
Source: https://partnerstack.com/blog/partner-scorecard + https://www.gartner.com/en/sales/topics/partner-relationship-management
Quarterly partner scorecard authoring with 4-6 KPIs per partner type (June 2026 SOTA).
-->
# Partner Scorecard Authoring — SKILL

Author quarterly partner scorecards with **4-6 KPIs per partner type**, threshold-banded health (Green / Yellow / Red), drives tier upgrades/downgrades and QBR talking points. Per-type KPI sets: **Referral** (leads sent/accepted/closed-won/commission). **Reseller** (certs/pipeline/closed-won/sat/MDF utilization). **Integration** (health/joint customers/co-marketing/NPS).

## When to use

- **Quarterly scorecard cycle** — produce per-partner scorecard for QBR.
- **Tier-eligibility review** — quarterly upgrade/downgrade.
- **Partner-pipeline health check** — mid-quarter checkpoint.
- **Pre-QBR prep** — pre-read deck for partner meeting.
- **Year-end performance review** — annual partner summary.
- **Trigger phrases**: "partner scorecard", "QBR deck for X", "Green Yellow Red health", "tier review", "partner-pipeline rollup".

Do NOT use this skill for: **the actual QBR meeting** (use this scorecard + `partner-led-webinars-events`); **commission accounting** (defer to `finance-controller`); **per-deal review** (use `sales-agent`); **strategy session** (use `partner-advisory-board-pab`).

## Setup

```bash
export MATON_API_KEY="<key>"
# postgresql-mcp for warehouse KPI queries
# Notion for scorecard template + per-partner records
# xlsx / google-sheets for trend lines
# pptx / canva-mcp for QBR deck
```

## Common recipes

### Recipe 1: Referral partner scorecard template

```yaml
partner: "Acme Solutions"
quarter: "2026-Q3"
tier: "Silver"
motion: "referral"

kpis:
  leads_sent:
    target: 30
    actual: 38
    band: "green"
    trend: "+15% QoQ"
  leads_accepted_pct:
    target: 70
    actual: 68
    band: "yellow"      # close to target; flag
    trend: "stable"
  closed_won_count:
    target: 4
    actual: 5
    band: "green"
  closed_won_amount_usd:
    target: 80000
    actual: 110000
    band: "green"
  commission_earned_usd:
    target: 12000
    actual: 16500
    band: "green"

overall_health: "green"
talking_points:
  - "Strong quarter — closed-won 38% above plan; commission accordingly"
  - "Lead acceptance at 68% (below 70% target); review lead qualification with their team"
  - "Tier-eligibility unchanged at Silver; Gold within reach at next-quarter $20K higher revenue"
next_quarter_targets:
  leads_sent: 35
  leads_accepted_pct: 75
  closed_won_amount: 130000
```

### Recipe 2: Reseller partner scorecard template

```yaml
partner: "Acme Reseller EMEA"
quarter: "2026-Q3"
tier: "Gold"
motion: "channel_reseller"

kpis:
  active_certs_count:
    target: 8
    actual: 9
    band: "green"
  pipeline_sourced_usd:
    target: 500000
    actual: 620000
    band: "green"
  closed_won_amount_usd:
    target: 150000
    actual: 145000
    band: "yellow"
  closed_won_count:
    target: 6
    actual: 5
    band: "yellow"
  customer_sat_nps:
    target: 40
    actual: 52
    band: "green"
  mdf_utilization_pct:
    target: 80
    actual: 92
    band: "green"

overall_health: "green"
talking_points:
  - "Pipeline strong; conversion slight miss — review deal velocity in detail"
  - "Customer-sat outstanding (52 vs 40 target); leverage in references"
  - "MDF healthy utilization (92%) — increase allocation Q4"
  - "Gold tier maintained; consider strategic-account designation for Q4"
next_quarter_targets:
  pipeline_sourced: 600000
  closed_won_amount: 200000
  closed_won_count: 7
```

### Recipe 3: Integration partner scorecard template

```yaml
partner: "Acme Analytics"
quarter: "2026-Q3"
tier: "Integration"
motion: "integration_partner"

kpis:
  integration_health_uptime:
    target: 99.9
    actual: 99.95
    band: "green"
  integration_error_rate_pct:
    target: 0.5
    actual: 0.3
    band: "green"
  joint_customers_count:
    target: 80
    actual: 95
    band: "green"
  adoption_pct_joint_customers:
    target: 40
    actual: 32
    band: "yellow"     # below target
  co_marketing_activities_count:
    target: 4
    actual: 5
    band: "green"
  partner_nps:
    target: 50
    actual: 64
    band: "green"

overall_health: "green-yellow"
talking_points:
  - "95 joint customers; adoption at 32% (target 40%) — onboarding flow needs work"
  - "Integration health strong; no outages"
  - "Partner NPS 64 — best-in-class; leverage in marketing"
  - "Q4 priority: ship Phase 2 use case (event streaming) to lift adoption to 50%"
next_quarter_targets:
  adoption_pct: 50
  joint_customers: 110
  co_marketing_activities: 5
```

### Recipe 4: KPI query library (warehouse)

```sql
-- Referral KPIs
SELECT
  p.partner_id, p.partner_name,
  COUNT(*) FILTER (WHERE l.created_at >= '2026-07-01' AND l.created_at < '2026-10-01') AS leads_sent,
  COUNT(*) FILTER (WHERE l.created_at >= '2026-07-01' AND l.accepted=true) AS leads_accepted,
  COUNT(d.id) FILTER (WHERE d.closed_at >= '2026-07-01' AND d.status='closed_won') AS closed_won_count,
  SUM(d.amount) FILTER (WHERE d.closed_at >= '2026-07-01' AND d.status='closed_won') AS closed_won_amount,
  SUM(c.amount) FILTER (WHERE c.posted_at >= '2026-07-01') AS commission_earned
FROM partners p
LEFT JOIN partner_leads l ON l.partner_id = p.partner_id
LEFT JOIN partner_deals d ON d.partner_id = p.partner_id
LEFT JOIN partner_commissions c ON c.partner_id = p.partner_id
WHERE p.motion='referral'
GROUP BY p.partner_id, p.partner_name;

-- Reseller KPIs (similar; add cert + sat + MDF)
-- Integration KPIs (different — sourced from product analytics)
```

### Recipe 5: Threshold band assignment

```python
def band(actual, target, kpi_type="standard"):
    """
    standard: green ≥ 100%, yellow 80-99%, red < 80%
    reverse  (lower better): green ≤ 100%, yellow 101-120%, red > 120%
    """
    pct = (actual / target) * 100
    if kpi_type == "reverse":
        if pct <= 100: return "green"
        if pct <= 120: return "yellow"
        return "red"
    if pct >= 100: return "green"
    if pct >= 80:  return "yellow"
    return "red"

# kpi_type for things like error_rate, cycle_time — lower is better
```

### Recipe 6: Per-partner trend chart (xlsx)

```python
import openpyxl
from openpyxl.chart import LineChart, Reference

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Acme — Trend"

# Header row
ws.append(["Quarter","leads_sent","leads_accepted_pct","closed_won","commission"])

# Last 5 quarters
data = [
    ("2025-Q3", 22, 65, 3, 9000),
    ("2025-Q4", 25, 67, 3, 10500),
    ("2026-Q1", 28, 70, 4, 12500),
    ("2026-Q2", 33, 71, 4, 14000),
    ("2026-Q3", 38, 68, 5, 16500),
]
for r in data: ws.append(r)

# Chart
chart = LineChart()
chart.title = "Acme Solutions — 5Q Trend"
data_ref = Reference(ws, min_col=2, max_col=5, min_row=1, max_row=6)
chart.add_data(data_ref, titles_from_data=True)
cats = Reference(ws, min_col=1, min_row=2, max_row=6)
chart.set_categories(cats)
ws.add_chart(chart, "G2")

wb.save("/tmp/acme-scorecard.xlsx")
```

### Recipe 7: QBR pre-read PDF

```python
# Render scorecard YAML → PDF for QBR pre-read
import yaml
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

with open("acme-scorecard.yaml") as f:
    sc = yaml.safe_load(f)

c = canvas.Canvas("/tmp/acme-qbr-pre-read.pdf", pagesize=letter)
c.setFont("Helvetica-Bold", 24)
c.drawString(50, 750, f"{sc['partner']} — Q{sc['quarter']} Scorecard")

c.setFont("Helvetica", 10)
y = 700
for kpi_name, kpi in sc['kpis'].items():
    band_color = {"green": "Green", "yellow": "Yellow", "red": "Red"}[kpi['band']]
    c.drawString(50, y, f"{kpi_name}: {kpi['actual']} (target: {kpi['target']}, band: {band_color})")
    y -= 20

c.drawString(50, 400, "Talking Points:")
y = 380
for tp in sc['talking_points']:
    c.drawString(70, y, f"• {tp}")
    y -= 20

c.showPage()
c.save()
```

### Recipe 8: Scorecard render in Notion DB

```bash
# Create row in Notion partner-scorecard DB
curl -X POST "https://gateway.maton.ai/notion/v1/pages" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "parent":{"database_id":"<scorecard-db-id>"},
    "properties":{
      "Name":{"title":[{"text":{"content":"Acme — 2026-Q3"}}]},
      "Partner":{"select":{"name":"Acme Solutions"}},
      "Quarter":{"select":{"name":"2026-Q3"}},
      "Tier":{"select":{"name":"Silver"}},
      "Overall Health":{"select":{"name":"green"}},
      "Closed Won Amount":{"number":110000},
      "Leads Sent":{"number":38},
      "Commission Earned":{"number":16500},
      "Last Updated":{"date":{"start":"2026-09-30"}}
    }
  }'
```

### Recipe 9: Bulk scorecard generation (all partners)

```python
# Run end-of-quarter
import requests, os, yaml
from pathlib import Path

partners = run_sql("SELECT partner_id, motion FROM partners WHERE status='active'")
for p in partners:
    if p["motion"] == "referral":
        kpis = query_referral_kpis(p["partner_id"])
    elif p["motion"] == "channel_reseller":
        kpis = query_reseller_kpis(p["partner_id"])
    elif p["motion"] == "integration_partner":
        kpis = query_integration_kpis(p["partner_id"])
    else:
        continue

    sc = {
        "partner": p["partner_name"],
        "quarter": "2026-Q3",
        "kpis": kpis,
        "overall_health": rollup_health(kpis),
        "talking_points": auto_talking_points(kpis),
        "next_quarter_targets": forecast_targets(kpis),
    }
    Path(f"scorecards/{p['partner_id']}.yaml").write_text(yaml.dump(sc))
    create_notion_row(sc)
```

### Recipe 10: Cross-quarter trend rollup (executive summary)

```sql
-- Top 10 partners by trailing-12-month closed-won
SELECT p.partner_name, p.tier,
  SUM(d.amount) FILTER (WHERE d.closed_at >= now() - interval '12 months') AS ttm_revenue,
  COUNT(*) FILTER (WHERE d.closed_at >= now() - interval '3 months') AS recent_count
FROM partners p
LEFT JOIN partner_deals d ON d.partner_id = p.partner_id AND d.status='closed_won'
GROUP BY p.partner_name, p.tier
ORDER BY ttm_revenue DESC
LIMIT 10;
```

### Recipe 11: Auto talking-points generation

```python
def auto_talking_points(kpis):
    tps = []
    # Highlight strong wins
    for name, k in kpis.items():
        if k['band'] == 'green' and k['actual'] >= k['target'] * 1.2:
            tps.append(f"{name} strong: {k['actual']} vs {k['target']} target ({(k['actual']/k['target']-1)*100:.0f}% over)")
    # Surface concerns
    for name, k in kpis.items():
        if k['band'] in ['yellow','red']:
            tps.append(f"{name} below target: {k['actual']} vs {k['target']}; root-cause + remediation plan")
    # Trend
    # (would need historical data fetch)
    return tps[:5]
```

### Recipe 12: QBR deck (pptx)

```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()

# Cover
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Acme Solutions — Q3 2026 QBR"
slide.placeholders[1].text = "Brand × Acme — Quarterly Business Review"

# Scorecard summary
slide = prs.slides.add_slide(prs.slide_layouts[5])
slide.shapes.title.text = "Scorecard — Q3 2026"
# Add table with KPIs vs targets
# ... (use python-pptx or canva-mcp for prettier output)

# Trend chart
slide = prs.slides.add_slide(prs.slide_layouts[5])
slide.shapes.title.text = "5-Quarter Trend"
# Insert chart from Recipe 6

# Talking points
slide = prs.slides.add_slide(prs.slide_layouts[5])
slide.shapes.title.text = "Q3 Highlights + Concerns"

# Next quarter
slide = prs.slides.add_slide(prs.slide_layouts[5])
slide.shapes.title.text = "Q4 Commitments"

# Action items
slide = prs.slides.add_slide(prs.slide_layouts[5])
slide.shapes.title.text = "Action Items + Next Steps"

prs.save("/tmp/acme-qbr-q3-2026.pptx")
```

Prefer `canva-mcp` for prettier QBR decks; `pptx` for fast generation.

## Examples

### Example 1: End-of-quarter scorecard generation for 30 partners

**Goal:** Q3 close; need scorecards for all 30 active partners by Oct 7.

**Steps:**
1. Recipe 4 — Warehouse queries refreshed.
2. Recipe 9 — Bulk-generate per-partner YAML scorecards.
3. Recipe 11 — Auto talking-points; manual edit for top 10 strategic partners.
4. Recipe 8 — Each scorecard row in Notion DB.
5. Top 10 partners: Recipe 12 — QBR deck generated.
6. QBRs scheduled in coming 2 weeks.

**Result:** All 30 scorecards ready 7 days post-quarter; strategic QBRs go live week 2.

### Example 2: Tier upgrade review during scorecard cycle

**Goal:** Identify Silver partners eligible for Gold based on Q3 numbers.

**Steps:**
1. Recipe 10 — Top 10 trailing-12m revenue partners.
2. Cross-reference with cert counts (`partner-enablement-certification-programs`) + NPS.
3. 2 Silver partners now Gold-eligible.
4. Tier-change communication via `channel-pricing-discount-tiers` Recipe 4.
5. Scorecards updated; QBR centers on tier change.

**Result:** Tier upgrades tied to quarterly performance review; partner feels recognized.

### Example 3: Mid-quarter checkpoint for under-performing partner

**Goal:** Aug 15 (mid-Q3); pull mid-quarter check on Silver partner trending Red.

**Steps:**
1. Recipe 4 — Pull mid-quarter KPIs.
2. 3 of 5 KPIs Yellow/Red.
3. Recipe 11 — Auto talking-points highlight specifics.
4. Mid-Q intervention call with partner; root-cause; remediation plan.
5. Q-end scorecard recovers to green-yellow.

**Result:** Early signal + intervention prevents Q-end surprise.

## Edge cases / gotchas

- **KPI inflation** — agents tend to over-pad targets; partners game easy targets. Calibrate annually against benchmarks.
- **Threshold rigidity** — Green at 100%+ feels punitive when partner hits 99%. Some teams use 95-99% as "green-yellow" lighter category.
- **Small-N stats** — partner with 3 deals; 1 cancellation = -33%. Avoid scorecard panic at small N; use trailing-trends instead.
- **Per-motion KPI sets** — referral KPIs ≠ reseller KPIs ≠ integration KPIs. Don't force one template.
- **Adoption KPI for integration** is hardest to measure — relies on PostHog/Mixpanel tagging discipline.
- **NPS-as-KPI noise** — response counts must be ≥ 5 for trustworthy band; otherwise show "insufficient data."
- **MDF utilization 100%** seems good but might mean over-allocated; track pipeline-per-MDF-dollar as quality companion.
- **Trend visualization** — single-quarter snapshot misleading; always show 4-5 quarter trend on scorecard.
- **Talking-points generation** — auto-generation is starting point; humans need to add context for sensitive topics.
- **Customer-sat KPI source** — varies by motion: referral uses customer-side feedback; reseller uses end-customer NPS; integration uses joint-customer NPS.
- **Quarter-end timing** — scorecards in Notion DB freeze on Day 7 of next quarter; later edits create version history.
- **QBR cadence vs scorecard cadence** — scorecards quarterly; QBRs quarterly or monthly. Sync.
- **Partner sees their scorecard** — write talking-points for partner-facing context, not internal critique.
- **Tier change embedded in scorecard** — when tier shifts, surface clearly; don't hide.
- **Multi-quarter recovery plans** — Red → Green takes 2 quarters minimum. Document multi-Q plans.
- **Per-region segmentation** — global partner has US Green, EMEA Red. Surface separately; don't average.
- **Exclude pilot / pre-launch deals** from closed-won counts; flag as "potential" only.
- **Currency normalization** — partner-in-Euro reported in EUR; warehouse normalizes to USD with quarter-end FX rate.
- **Manual entry quality** — for non-warehouse-tracked KPIs (joint events, customer references), entry by BD lead is error-prone. Audit.

## Sources

- Partnerstack scorecard blog: https://partnerstack.com/blog/partner-scorecard
- Gartner PRM topics: https://www.gartner.com/en/sales/topics/partner-relationship-management
- Forrester partner-program benchmarks: https://www.forrester.com/research/partner-ecosystems/
- HubSpot partner scorecard template: https://blog.hubspot.com/sales/partner-scorecard-template
- Canalys channel program research: https://www.canalys.com/insights/
- Partner-NPS benchmarks (separate skill): see `partner-nps-satisfaction-survey`
- python-pptx: https://python-pptx.readthedocs.io/
- openpyxl charts: https://openpyxl.readthedocs.io/en/stable/charts/introduction.html
