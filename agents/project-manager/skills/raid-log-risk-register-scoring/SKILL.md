<!--
Source: https://asana.com/resources/raid-log
Source: https://raidlog.com
Source: https://www.notion.com/templates/raid-log-for-project-management
-->
# RAID Log + Risk Register with P×I Scoring — SKILL

Centralized Risks / Assumptions / Issues / Dependencies log + 5×5 P×I risk scoring + heat map + risk burn-down + risk velocity. The single load-bearing PM artifact — risks unaddressed become issues become incidents.

## When to use

- Standing up a project's RAID log at kickoff.
- Logging a new risk / assumption / issue / dependency mid-project.
- Reviewing top-5 risks weekly + all open risks biweekly.
- Generating risk heat map + burn-down + velocity charts for status reports.
- Migrating a RAID log between Notion / RAIDLOG.com / Asana / Wrike.

Trigger phrases: "RAID log", "risk register", "score this risk", "risk heatmap", "risk burndown", "log an issue", "track dependency", "P×I", "risk review".

## Setup

```bash
# Notion DB (default — free)
mcp tool notion.search_pages --query "RAID"

# RAIDLOG.com (paid SaaS, AI-enabled)
curl -fsSL "https://api.raidlog.com/v1/items" \
  -H "Authorization: Bearer $RAIDLOG_TOKEN"

# Asana RAID custom template
curl -fsSL "https://app.asana.com/api/1.0/projects/<gid>/sections" \
  -H "Authorization: Bearer $ASANA_PAT"
```

Auth:
- `NOTION_TOKEN` — internal integration from https://www.notion.so/my-integrations (free)
- `RAIDLOG_TOKEN` — from raidlog.com → Settings → API (paid)
- `ASANA_PAT` — same as Asana setup

## Common recipes

### Recipe 1: Notion RAID DB schema
```yaml
Database: "RAID Log — [Project]"
Properties:
  ID:                    title          # auto: R-001, I-001, A-001, D-001
  Type:                  select         # Risk / Issue / Assumption / Dependency
  Title:                 rich_text
  Description:           rich_text
  Category:              multi_select   # Technical/Schedule/Budget/Scope/Quality/Resource/External/Org
  Probability:           number         # 1-5 (Risk only)
  Impact:                number         # 1-5 (Risk only)
  Score:                 formula        # P × I (1-25)
  Heat_zone:             formula        # if Score >= 13 then "RED" elif Score >= 6 then "AMBER" else "GREEN"
  Severity:              select         # Critical/High/Medium/Low  (Issue only)
  Validation_status:     select         # Validated / Pending / Invalid (Assumption only)
  Response:              select         # Avoid / Mitigate / Transfer / Accept
  Mitigation_plan:       rich_text
  Owner:                 person
  Due_date:              date
  Status:                select         # Open / In progress / Mitigated / Closed
  Last_review:           date
  Escalation_level:      select         # PM / Eng Lead / Sponsor / Steering
  Linked_CR:             relation       # → CR DB
  Created_at:            created_time
```

### Recipe 2: P×I 5×5 risk scoring matrix
```
              Impact
        1     2     3     4     5
P 5  | 5  | 10 | 15 | 20 | 25 |
P 4  | 4  |  8 | 12 | 16 | 20 |
P 3  | 3  |  6 |  9 | 12 | 15 |
P 2  | 2  |  4 |  6 |  8 | 10 |
P 1  | 1  |  2 |  3 |  4 |  5 |

Zones:
  1-5:    LOW    (GREEN)  — log + monitor
  6-12:   MEDIUM (AMBER)  — mitigation plan + owner
  13-25:  HIGH   (RED)    — sponsor visibility + weekly review

Probability scale:
  1 = remote (<10%)
  2 = unlikely (10-30%)
  3 = possible (30-50%)
  4 = likely (50-70%)
  5 = almost certain (>70%)

Impact scale:
  1 = trivial (no schedule/budget/quality impact)
  2 = minor (<5% delta on any axis)
  3 = moderate (5-15% delta)
  4 = major (15-30% delta)
  5 = severe (>30% or project-killing)
```

### Recipe 3: Risk response strategies
```
Negative risks (threats):
  Avoid     — eliminate cause (change approach, drop scope)
  Mitigate  — reduce P or I (training, redundancy, monitoring)
  Transfer  — shift to third party (insurance, vendor contract clause)
  Accept    — log, watch, hold contingency $ + buffer days

Positive risks (opportunities):
  Exploit   — ensure it happens
  Enhance   — increase P or I
  Share     — partner to capture
  Accept    — log, hope, no plan

Pick exactly one response per risk; document in RAID.
```

### Recipe 4: Create a Risk in Notion via MCP
```bash
mcp tool notion.create_page \
  --parent '{"database_id":"<raid-db-id>"}' \
  --properties '{
    "ID":{"title":[{"text":{"content":"R-007"}}]},
    "Type":{"select":{"name":"Risk"}},
    "Title":{"rich_text":[{"text":{"content":"SSO vendor cert renewal late"}}]},
    "Description":{"rich_text":[{"text":{"content":"Vendor cert expires Jul 5; renewal SLA 14 days unclear."}}]},
    "Category":{"multi_select":[{"name":"Technical"},{"name":"External"}]},
    "Probability":{"number":3},
    "Impact":{"number":4},
    "Response":{"select":{"name":"Mitigate"}},
    "Mitigation_plan":{"rich_text":[{"text":{"content":"Pre-emptive renewal Jun 20; backup IDP provisioned"}}]},
    "Owner":{"people":[{"id":"<eng-lead-id>"}]},
    "Due_date":{"date":{"start":"2026-06-20"}},
    "Status":{"select":{"name":"Open"}},
    "Escalation_level":{"select":{"name":"Eng Lead"}}
  }'
```

### Recipe 5: Create an Issue (materialized risk OR new problem)
```bash
mcp tool notion.create_page \
  --parent '{"database_id":"<raid-db-id>"}' \
  --properties '{
    "ID":{"title":[{"text":{"content":"I-003"}}]},
    "Type":{"select":{"name":"Issue"}},
    "Title":{"rich_text":[{"text":{"content":"Activation event not firing on Android"}}]},
    "Severity":{"select":{"name":"High"}},
    "Owner":{"people":[{"id":"<eng-id>"}]},
    "Due_date":{"date":{"start":"2026-07-02"}},
    "Status":{"select":{"name":"In progress"}}
  }'
```

### Recipe 6: Log a Dependency
```bash
mcp tool notion.create_page \
  --parent '{"database_id":"<raid-db-id>"}' \
  --properties '{
    "ID":{"title":[{"text":{"content":"D-002"}}]},
    "Type":{"select":{"name":"Dependency"}},
    "Title":{"rich_text":[{"text":{"content":"Auth-revamp team unified-session ship"}}]},
    "Description":{"rich_text":[{"text":{"content":"Cross-team upstream; blocks 3.1.3"}}]},
    "Owner":{"people":[{"id":"<auth-pm-id>"}]},
    "Due_date":{"date":{"start":"2026-06-25"}},
    "Status":{"select":{"name":"Open"}},
    "Escalation_level":{"select":{"name":"Sponsor"}}
  }'
```

### Recipe 7: Risk heatmap (5×5 grid) — Excalidraw
```bash
mcp tool excalidraw.generate_diagram \
  --type "matrix" \
  --rows 5 --cols 5 \
  --xlabel "Impact" --ylabel "Probability" \
  --cells '[
    {"x":4,"y":4,"label":"R-007","color":"red"},
    {"x":3,"y":4,"label":"R-002","color":"red"},
    {"x":2,"y":3,"label":"R-004","color":"amber"},
    {"x":3,"y":3,"label":"R-001","color":"amber"},
    {"x":2,"y":2,"label":"R-005","color":"green"}
  ]'
```

### Recipe 8: Risk burn-down chart
```python
# burndown.py — weekly trend of open exposure
import json, matplotlib.pyplot as plt
data = json.load(open("weekly-risk-snapshot.json"))
# [{"week":"2026-W24","open_count":12,"total_exposure":98,"high_zone_count":3}]

weeks = [d["week"] for d in data]
plt.plot(weeks, [d["total_exposure"] for d in data], label="Total exposure (ΣP×I)")
plt.plot(weeks, [d["open_count"] for d in data], label="Open risk count")
plt.plot(weeks, [d["high_zone_count"] for d in data], label="High-zone count")
plt.legend(); plt.xticks(rotation=45); plt.tight_layout()
plt.savefig("risk-burndown.png")
```

### Recipe 9: Risk velocity tracker
```python
# velocity.py — monthly: new risks vs materialized (→ issues)
data = json.load(open("monthly-velocity.json"))
# [{"month":"2026-06","new_risks":7,"materialized_to_issues":2}]
months = [d["month"] for d in data]
plt.bar(months, [d["new_risks"] for d in data], label="New risks")
plt.bar(months, [d["materialized_to_issues"] for d in data], label="Materialized to issues", bottom=0)
plt.legend(); plt.savefig("risk-velocity.png")
```

### Recipe 10: Weekly RAID review checklist
```markdown
## RAID Review — Week of [YYYY-MM-DD]

### Top-5 risks (by Score, then by Due_date)
- [ ] R-007 (Score 12) — owner Eng Lead — mitigation plan status?
- [ ] R-002 (Score 12) — owner PM — mitigation plan status?
- [ ] R-001 (Score 12) — owner Eng Lead — mitigation plan status?
- [ ] R-004 (Score 10) — owner Sponsor — sponsor decision pending?
- [ ] R-005 (Score 9)  — owner PM — on track?

### Closed this week
- R-003 (Score 9) closed — mitigation landed

### New risks
- R-008 (Score 8) — new dep on legal review for terms

### Heat-map deltas
- 2 risks moved into RED zone this week → escalate to sponsor
- 1 risk moved out of RED zone (mitigation landed)

### Issues escalated
- I-004 — backend latency on staging; Eng Lead owns; ETA Fri

### Dependencies at-risk
- D-002 — auth-revamp upstream slipped 2d → check buffer
```

### Recipe 11: Auto-aggregate RAID into status report block
```bash
# Pull open RAID items by type
mcp tool notion.query_database \
  --database_id "<raid-db-id>" \
  --filter '{"and":[{"property":"Status","select":{"does_not_equal":"Closed"}},{"property":"Type","select":{"equals":"Risk"}}]}' \
  --sorts '[{"property":"Score","direction":"descending"}]' \
| jq '.results[:5] | map({id: .properties.ID.title[0].plain_text, title: .properties.Title.rich_text[0].plain_text, score: .properties.Score.formula.number, owner: .properties.Owner.people[0].name})'
```

### Recipe 12: RAIDLOG.com API alternative
```bash
# Create item
curl -X POST "https://api.raidlog.com/v1/items" \
  -H "Authorization: Bearer $RAIDLOG_TOKEN" \
  -d '{
    "type":"risk",
    "title":"SSO vendor cert renewal late",
    "probability":3,
    "impact":4,
    "owner_id":"u_abc",
    "due_date":"2026-06-20",
    "response":"mitigate",
    "mitigation":"Pre-emptive renewal Jun 20"
  }'
```

### Recipe 13: Risk DB CSV export schema
```csv
type,id,title,category,description,p,i,score,response,owner,due,status,last_review,notes
Risk,R-007,SSO vendor cert renewal late,Technical;External,"Vendor cert expires Jul 5",3,4,12,Mitigate,Eng Lead,2026-06-20,Open,2026-06-15,"Pre-emptive renewal in flight"
Risk,R-002,Design capacity constrained,Resource,"Design 0.5 FTE; 2 contracts in pipeline",4,3,12,Mitigate,PM,2026-06-22,Open,2026-06-15,"Contractor PO pending"
Issue,I-003,Activation event not firing on Android,Quality,"Specific to Android 14",,,High,,Eng,2026-07-02,In progress,2026-06-15,"Patch in QA"
Assumption,A-001,Eng team retains 3 FTE through Q3,Resource,"No attrition planned",,,,Pending,PM,2026-08-01,Open,2026-06-15,
Dependency,D-002,Auth team unified session,External,"Upstream cross-team",,,,,Auth PM,2026-06-25,Open,2026-06-15,
```

## Examples

### Example 1: Stand up RAID at kickoff
**Goal:** New project kickoff Monday; need RAID with top-5 chartering risks pre-loaded.

**Steps:**
1. Create Notion RAID DB (Recipe 1).
2. From charter section 8 (top-5 risks): create R-001 through R-005 via Recipe 4.
3. Add 3 known assumptions (Recipe 4 with Type=Assumption).
4. Add 2 known cross-team dependencies (Recipe 6).
5. Schedule weekly RAID review on calendar.
6. Brief team at kickoff: how to submit risks, who reviews, what's the cadence.

**Result:** Live RAID with 10 items, weekly review on books, team knows protocol.

### Example 2: Weekly RAID review for status report
**Goal:** Generate the "Risks needing attention" block for Friday status.

**Steps:**
1. Run Recipe 11 to pull top-5 by Score.
2. Run Recipe 10 checklist with PM + Eng Lead Wednesday standup.
3. Capture deltas: 2 risks moved to RED zone, 1 closed.
4. Update Last_review date on top-5.
5. Generate Recipe 7 heatmap snapshot for status archive.
6. Embed Recipe 9 velocity chart in monthly variant.

**Result:** Status report has Risks block with owner + ETA + heatmap.

## Edge cases / gotchas

- **RAID without review = documentation theatre.** Top-5 weekly, all open biweekly. Stale RAID is worse than no RAID (false sense of safety).
- **Risks ≠ issues.** Risk = future potential. Issue = current reality. Once a risk materializes, transition R-XXX → I-XXX; don't reuse ID.
- **P×I scoring is judgment, not math.** Calibrate per team: 3 PMs scoring same risk may give 2-4 on probability. Re-score at quarterly portfolio review for consistency.
- **5×5 vs 3×3 vs 4×4.** 5×5 is PMI standard. Smaller scales (3×3) lose granularity. Don't go beyond 5×5 (false precision).
- **Exposure ≠ score.** Exposure = sum of P×I across open risks (dollar-or-day-weighted in advanced models). Score = per-risk.
- **Assumptions must be testable.** "Sponsor will fund us" is not an assumption — it's a fact or a risk. "Eng team retains 3 FTE through Q3" can be tested.
- **Dependencies need owners across the boundary.** D-002 (upstream) has owner = upstream team's PM, not yours. Document escalation path.
- **Mitigation cost.** Big-P-big-I risks may justify $5-10k in mitigation effort; small risks should not consume team weeks. Tradeoff in CR if mitigation > 1 sprint of effort.
- **Closing risks too early.** Risks should stay open until truly past; closing because "we feel good" creates re-emergence.
- **Risk register vs RAID log.** Risk register is the R-only subset of RAID. Some shops separate; most consolidate in RAID. Pick one and document.
- **CR linkage.** Approved CRs often close some risks + open others — capture in Linked_CR property.
- **Sponsor visibility on RED-zone risks.** RED-zone (Score ≥13) risks go in sponsor brief regardless of progress. Hiding RED-zone = sandbagging RAG.
- **Risk velocity rising = volatile project.** New risks > closed risks 2+ months = trigger root-cause investigation.
- **RAIDLOG.com pricing.** Paid SaaS; for Notion DB free fallback, build Recipe 1 schema.
- **Asana custom-field RAID.** Works but lacks formula columns native to Notion; compute Score client-side.
- **Smartsheet risk template.** Templated risk register sheet; use if Smartsheet is the SoT.

## Sources

- [Asana RAID log guide](https://asana.com/resources/raid-log)
- [RAIDLOG.com](https://raidlog.com)
- [Notion RAID template](https://www.notion.com/templates/raid-log-for-project-management)
- [PMI risk management process](https://www.pmi.org/learning/library/risk-management-process-9462)
- [Smartsheet risk register templates](https://www.smartsheet.com/free-risk-register-templates)
- [Atlassian Jira risk management](https://www.atlassian.com/agile/project-management/risk-management)
- [PMBOK 7th Edition (PMI) — risk performance domain](https://www.pmi.org/standards/pmbok)
- [Risk burn-down chart guide (PMI)](https://www.pmi.org/learning/library/risk-burn-down-charts-project-control-2316)
