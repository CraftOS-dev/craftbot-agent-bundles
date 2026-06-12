<!--
Source: https://www.smartsheet.com/content/best-ppm-software
Source: https://asana.com/uses/portfolios
Source: https://www.planview.com
-->
# Project Portfolio Management (PPM) — SKILL

Portfolio = collection of projects sharing strategic objectives. Alignment scoring + resource demand vs supply + financial roll-up + risk heat map. SOTA tools: Smartsheet Control Center, Asana Portfolios, Wrike Portfolios, Planview (enterprise), monday.com Portfolios.

## When to use

- Standing up a portfolio (group of related projects) at quarterly planning.
- Computing strategic alignment scores for project intake.
- Resource demand vs supply forecasting across the portfolio.
- Quarterly portfolio review for sponsors / leadership.
- Project intake prioritization when multiple initiatives compete.

Trigger phrases: "portfolio", "PPM", "roll up", "across projects", "portfolio dashboard", "intake", "strategic alignment", "portfolio review".

## Setup

```bash
# Smartsheet Control Center (enterprise, blueprint-driven)
curl -fsSL "https://control-api.smartsheet.com/portfolios" \
  -H "Authorization: Bearer $SMARTSHEET_TOKEN"

# Asana Portfolios (Business plan+)
curl -fsSL "https://app.asana.com/api/1.0/portfolios" \
  -H "Authorization: Bearer $ASANA_PAT"

# Wrike Portfolios (Business plan+)
curl -fsSL "https://www.wrike.com/api/v4/folders?fields=metadata" \
  -H "Authorization: bearer $WRIKE_TOKEN"

# monday.com — uses Workspaces + boards (no native "portfolio" object)
# Notion roll-up DB — free fallback
```

Auth: per-platform (paid plans for native PPM).

## Common recipes

### Recipe 1: Portfolio composition
```
Portfolio = grouped projects sharing:
- Strategic objective / OKR
- Sponsor or executive owner
- Funding source (budget allocation)
- Time horizon (e.g., Q3, FY2026, multi-year)

Typical portfolio sizes:
- Team portfolio:    5-12 projects
- Department:        10-30 projects
- BU / division:     30-100 projects
- Enterprise:        100-1000+ projects

Each project in portfolio reports:
- RAG status (overall, scope, schedule, budget, risk)
- % complete (EV / BAC)
- Strategic alignment score
- Top-3 risks
- Decisions needed
- Resource demand
```

### Recipe 2: Strategic alignment scoring
```python
# alignment.py
# Score each project 0-100 on strategic fit; rank for portfolio decisions

def alignment_score(project):
    score = 0
    # Direct OKR linkage (40 pts)
    if project["primary_okr_link"]:
        score += 40
    if len(project["additional_okr_links"]) > 0:
        score += 10
    # Sponsor priority (20 pts)
    score += {"P0":20, "P1":15, "P2":10, "P3":5}.get(project["sponsor_priority"], 0)
    # Customer impact (15 pts) — reach × confidence
    score += min(15, project["reach"] / 1000 * project["confidence"] * 15)
    # Strategic theme (15 pts) — must be a current org theme
    if project["theme"] in CURRENT_THEMES:
        score += 15
    # Risk-adjusted upside (10 pts)
    score += min(10, project["upside_value"] / 100000 * project["confidence"] * 10)
    return min(100, score)
```

### Recipe 3: Portfolio dashboard schema (Notion)
```yaml
Database: "Portfolio — Q3 2026"
Properties:
  Project_name:           title
  Sponsor:                person
  PM:                     person
  Strategic_alignment:    number   # 0-100
  Sponsor_priority:       select   # P0/P1/P2/P3
  Primary_OKR:            relation # → OKR DB
  Phase:                  select   # G0/G1/G2/G3/G4/G5
  RAG_overall:            select   # derived from dimensions
  RAG_schedule:           select
  RAG_budget:             select
  RAG_risk:               select
  Pct_complete:           number
  BAC:                    number
  EAC:                    number
  Variance_pct:           formula
  CPI:                    number
  SPI:                    number
  Resource_demand_hrs:    number
  Top_risk:               rich_text
  Decisions_needed:       rich_text
  Target_date:            date
  Linked_status:          relation # → status archive
  Last_updated:           date
```

### Recipe 4: Project intake scoring (RICE)
```python
# intake.py — score new project proposals for portfolio admission
def rice_score(proposal):
    R = proposal["reach"]                # users / customers affected
    I = proposal["impact"]               # 0.25, 0.5, 1, 2, 3 (massive, high, med, low, min)
    C = proposal["confidence"]           # 0.5-1.0
    E = proposal["effort_person_months"] # >= 1
    return (R * I * C) / E

# Threshold: RICE > 50 → portfolio admission
# Rank ascending RICE; cut at portfolio capacity
```

### Recipe 5: Resource demand vs supply forecast
```python
# rds.py — quarterly capacity
import json

portfolio = json.load(open("portfolio.json"))
demand = sum(p["resource_demand_hrs"] for p in portfolio if p["status"] in ("Active","Tentative"))

# Supply: FTE × hours × focus × weeks
team_size = 12   # FTE
weeks = 13
hrs_per_week = 40
focus = 0.7
supply = team_size * weeks * hrs_per_week * focus  # 4368 hrs

gap = supply - demand
print(f"Q3 demand:  {demand:.0f} hrs")
print(f"Q3 supply:  {supply:.0f} hrs")
print(f"Gap:        {gap:.0f} hrs ({gap/supply*100:.0f}% buffer)")
if gap < 0:
    print(f"OVERCOMMITTED — need {-gap:.0f}h additional or scope cuts")
elif gap < supply * 0.1:
    print(f"TIGHT — <10% buffer; one CR likely tips over")
else:
    print(f"HEALTHY — sufficient buffer")
```

### Recipe 6: Portfolio RAG roll-up
```python
# rag-rollup.py
def portfolio_rag(projects):
    """Worst-of dimension roll-up + count of RED projects"""
    dims = ["RAG_schedule", "RAG_budget", "RAG_risk", "RAG_quality"]
    counts = {dim: {"RED":0,"AMBER":0,"GREEN":0} for dim in dims}
    for p in projects:
        for dim in dims:
            counts[dim][p[dim]] += 1
    print("Portfolio RAG roll-up:")
    for dim in dims:
        c = counts[dim]
        portfolio_color = "RED" if c["RED"] > 0 else ("AMBER" if c["AMBER"] > 0 else "GREEN")
        print(f"  {dim:20} {portfolio_color}  (R={c['RED']} A={c['AMBER']} G={c['GREEN']})")
```

### Recipe 7: Portfolio financial roll-up
```bash
# Pull BAC + AC + EAC across all portfolio projects
mcp tool notion.query_database --database_id "<portfolio-db-id>" \
| jq '{
    total_bac: ([.results[] | .properties.BAC.number] | add),
    total_ac: ([.results[] | .properties.AC.number] | add),
    total_eac: ([.results[] | .properties.EAC.number] | add),
    portfolio_variance: ([.results[] | .properties.EAC.number] | add) - ([.results[] | .properties.BAC.number] | add)
  }'
```

### Recipe 8: Asana Portfolios — pull status
```bash
curl -s "https://app.asana.com/api/1.0/portfolios/<gid>/items?opt_fields=name,current_status_update.text,current_status_update.color,due_on,custom_fields" \
  -H "Authorization: Bearer $ASANA_PAT" \
| jq '.data[] | {name, status: .current_status_update.text, color: .current_status_update.color, due: .due_on}'
```

### Recipe 9: Smartsheet Control Center — portfolio blueprint
```bash
# Control Center deploys project sheets from blueprint
curl -X POST "https://control-api.smartsheet.com/blueprint/<bp-id>/deploy" \
  -H "Authorization: Bearer $SMARTSHEET_TOKEN" \
  -d '{
    "projectName":"Q3-Project-XYZ",
    "metadata":{
      "sponsor":"VP Product",
      "strategic_theme":"Activation",
      "BAC":180000,
      "OKR":"D7-Retention"
    }
  }'

# Roll-up dashboard pulls from all deployed sheets
curl -s "https://api.smartsheet.com/2.0/server/portfolios/<portfolio-id>/rollup" \
  -H "Authorization: Bearer $SMARTSHEET_TOKEN" \
| jq '.summary'
```

### Recipe 10: Portfolio risk heat map
```python
# portfolio-risk.py — aggregate top risks across projects
import json
portfolio = json.load(open("portfolio.json"))

heatmap = {(p, i): [] for p in range(1, 6) for i in range(1, 6)}
for proj in portfolio:
    for risk in proj["top_3_risks"]:
        heatmap[(risk["P"], risk["I"])].append(f"{proj['name']}: {risk['title']}")

print("Portfolio risk heatmap (P × I):")
print("        I=1     2     3     4     5")
for p in range(5, 0, -1):
    row = f"P={p}  "
    for i in range(1, 6):
        n = len(heatmap[(p, i)])
        marker = "🔴" if p*i >= 13 else ("🟠" if p*i >= 6 else "🟢")
        row += f" {marker}{n:2}  "
    print(row)

print("\nRED-zone risks (Score ≥ 13):")
for (p, i), risks in heatmap.items():
    if p * i >= 13:
        for r in risks: print(f"  {r}")
```

### Recipe 11: Quarterly portfolio review template
```markdown
# Portfolio Review — Q3 2026 — [Date]

## Section 1: Portfolio snapshot
- Active projects: 14
- Tentative (pending decision): 3
- Completed this quarter: 6
- Total BAC: $1,840,000
- Forecast EAC: $1,920,000 (4.3% over)
- Portfolio CPI: 0.96
- Portfolio SPI: 0.94

## Section 2: Strategic alignment
- 11/14 projects score ≥75 (strong alignment)
- 2/14 score 50-75 (re-evaluate at next quarter)
- 1/14 score <50 (recommend de-prioritize)

## Section 3: Resource demand vs supply
- Demand: 8,400 hrs
- Supply: 9,100 hrs
- Buffer: 7.7%
- Tightness: AMBER (1 CR tips us over)

## Section 4: RAG roll-up
- Schedule: 9G / 3A / 2R
- Budget: 11G / 2A / 1R
- Risk: 8G / 5A / 1R
- Quality: 12G / 2A / 0R

## Section 5: Top portfolio risks
| Risk | Project | Score | Owner |
|---|---|---|---|
| Vendor SLA on auth | Onboarding | 16 | Eng Lead |
| Compliance signoff late | Billing-2 | 15 | Legal |

## Section 6: Decisions needed
- [ ] Approve scope cut on Onboarding (CR-009) — Sponsor
- [ ] De-prioritize Project-XYZ (alignment 42) — Steering
- [ ] Approve $200k contingency for Q3 — CFO

## Section 7: Next quarter intake
[Top-5 RICE-scored proposals]
```

### Recipe 12: Portfolio dashboard visualization
```bash
mcp tool excalidraw.generate_diagram \
  --type "matrix" \
  --xlabel "Strategic alignment" \
  --ylabel "Resource cost" \
  --cells '[
    {"x":"high","y":"low",  "label":"Project A (P0)","color":"green"},
    {"x":"high","y":"high", "label":"Project B (P0)","color":"green"},
    {"x":"high","y":"low",  "label":"Project C (P1)","color":"green"},
    {"x":"med", "y":"med",  "label":"Project D (P1)","color":"amber"},
    {"x":"low", "y":"high", "label":"Project E (P3)","color":"red"}
  ]'
```

### Recipe 13: Portfolio kill / hold / continue rubric
```
For each project, every quarter ask:
- Strategic alignment ≥ 60?
- RAG overall not RED for 2+ months?
- ROI projection > organizational threshold?
- Resources still available?

If YES to all → continue
If 1-2 NO → conditional continue with named conditions
If 3-4 NO → kill / hold

Don't sunk-cost. A project at G3 with low alignment is still a kill candidate.
```

## Examples

### Example 1: Stand up Q3 portfolio
**Goal:** Quarter starting; need 14-project portfolio operational.

**Steps:**
1. Create Notion Portfolio DB (Recipe 3).
2. Score each project (Recipe 2 alignment).
3. Forecast resource demand vs supply (Recipe 5).
4. Run RAG roll-up (Recipe 6) baseline.
5. Generate Recipe 12 alignment-vs-cost matrix.
6. Quarterly review meeting (Recipe 11) with steering.

**Result:** Live portfolio dashboard; resource gaps identified; 1 project recommended for de-prioritization.

### Example 2: Score project intake
**Goal:** 8 new project proposals submitted for next quarter.

**Steps:**
1. Run Recipe 4 RICE per proposal.
2. Rank ascending RICE → top-5 (RICE > 50).
3. Verify resource fit (Recipe 5 simulation).
4. Steering decides which to admit.
5. Approved projects enter portfolio with charter authoring kicked off.

**Result:** Top-5 projects admitted with data-driven justification.

### Example 3: Portfolio quarterly review
**Goal:** Sponsors + steering quarterly review.

**Steps:**
1. Recipe 11 template populated from Notion DB.
2. Recipe 10 risk heatmap.
3. Recipe 9 financial roll-up.
4. Recipe 13 kill/hold/continue review per project.
5. Decisions captured in steering minutes; portfolio updated.

**Result:** Steering ratifies 12 continues, 1 kill, 1 hold; next quarter intake set.

## Edge cases / gotchas

- **Portfolio ≠ list of projects.** Shared strategic objective + governance = portfolio. Random projects in one folder = not a portfolio.
- **Alignment scoring is judgment.** Calibrate quarterly across PMs to ensure consistency.
- **Resource over-commit is the modal portfolio failure.** Demand > supply → projects collide; everything slips.
- **Strategic theme drift.** Themes change every 12-18 months; re-score alignment each quarter.
- **Kill decisions are political.** Sunk cost + sponsor pride. Use objective alignment scoring + RAG history.
- **Hidden portfolio.** Cross-team initiatives often run without portfolio governance. Surface + assimilate.
- **PPM tool overkill.** SMB doesn't need Planview. Notion + alignment score covers it.
- **Smartsheet Control Center enterprise-only.** Alt: Asana Portfolios (Business+); Notion roll-up (free).
- **Asana Portfolios limit.** Asana Business max 5 portfolios per workspace; Enterprise unlimited.
- **Status drift.** Project's current_status_update gets stale; enforce weekly refresh policy.
- **Project-level RAG ≠ portfolio RAG.** Single RED project doesn't necessarily make portfolio RED — depends on weight + strategic importance.
- **Compound budget overrun.** Three projects each +5% over = portfolio +15% over → may breach total budget cap.
- **Multi-stakeholder alignment.** Different sponsors weight strategic themes differently → score variance.
- **Quarterly cadence minimum.** Slower than quarterly = portfolio drift.
- **Cross-portfolio dependencies.** Strategy initiatives may depend on operational initiatives → portfolio-of-portfolios for enterprise.
- **OKR linkage stale.** OKRs change quarterly; portfolio's OKR links need refresh.
- **Tentative projects in resource forecast.** Include at 50% confidence; otherwise resource plan underestimates demand.

## Sources

- [Smartsheet PPM software guide](https://www.smartsheet.com/content/best-ppm-software)
- [Asana Portfolios](https://asana.com/uses/portfolios)
- [Planview PPM](https://www.planview.com)
- [Wrike Portfolios](https://www.wrike.com/features/portfolio-management/)
- [PMI Portfolio Standard](https://www.pmi.org/standards/portfolio-management)
- [Strategic alignment scoring](https://www.workamajig.com/blog/strategic-alignment)
- [RICE prioritization (Intercom)](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers)
- [Monday.com Portfolios](https://monday.com/p/portfolio-management)
- [Smartsheet Control Center](https://www.smartsheet.com/platform/control-center)
