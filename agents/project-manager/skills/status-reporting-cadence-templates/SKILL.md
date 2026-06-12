<!--
Source: https://asana.com/templates/status-report
Source: https://www.atlassian.com/agile/project-management/status-report
Source: https://www.lennysnewsletter.com/p/how-to-write-a-great-weekly-update
-->
# Status Reporting Cadence Templates — SKILL

Weekly + biweekly + monthly + sponsor brief templates with RAG dashboard + auto-aggregation from Linear / Asana / Jira + Harvest + RAID. Distribution via gmail + Slack + Notion archive. Replaces activity-log status reports with outcome-led, decision-driving updates (Lenny Rachitsky format).

## When to use

- Drafting the weekly status report (default cadence for active projects).
- Drafting sponsor brief (1-page Manage-Closely format).
- Drafting monthly steering or quarterly board variants.
- Auto-aggregating data from Linear cycles + Harvest budget + RAID for variance.
- Archiving status reports in Notion for searchable history.

Trigger phrases: "status report", "weekly update", "sponsor brief", "RAG", "what's our status", "biweekly", "monthly board update", "status archive".

## Setup

```bash
# linear-mcp + asana-api + notion-mcp + gmail-mcp + slack-mcp + harvest
# CraftBot ships these by default
```

Auth: per-platform (see linear, harvest, notion skills).

## Common recipes

### Recipe 1: Weekly status template (active project default)
```markdown
# [Project Name] — Status — Week of [YYYY-MM-DD]

## Header
- Sponsor: [Name] · PM: [Name] · Methodology: [Agile/Waterfall/Hybrid]
- Phase: [G2 Planning / G3 Execution / G4 Launch / etc.]
- Days to next milestone: [N]
- Charter version: v1.0  |  Baseline locked: [date]

## RAG dashboard
| Dimension | RAG | Note |
|---|---|---|
| Scope | 🟢 | Baseline locked; no open CRs |
| Schedule | 🟠 | Critical-path task 3.1.3 slipped 3 days; mitigating via fast-track |
| Budget | 🟢 | CPI 1.02; SPI 0.96 |
| Quality | 🟢 | No critical defects open |
| Risk | 🟠 | 2 risks moved to high zone this week (R-007, R-002) |
| Resource | 🟢 | No over-allocated weeks; design contractor PO landed Tue |

## Executive summary (3-5 lines)
Beta to 5 design partners shipped Tue (milestone hit). Critical-path SSO refactor (3.1.3) overrunning planned hours by 50% due to vendor cert dep — mitigation R-007 in flight; recovery via fast-track viable. Need sponsor sign on $7k crash decision by Fri to hold ship date.

## Accomplishments this period
- Beta v0 to 5 design partners launched Tue (M2 hit)
- Activation event schema sign-off; 3 events live in Amplitude
- Onboarding flow map signed off Wed
- 2 risks closed (R-003, R-004 mitigations landed)

## Planned next period
- Beta partner feedback synthesis (Wed)
- Stage-gate G3 review (Fri)
- SSO refactor crash decision implementation (pending sponsor)
- Sprint 28 planning Mon

## Risks / issues needing attention
- R-007 (Score 12) — SSO vendor cert renewal — Eng Lead — pre-emptive renewal Fri
- R-002 (Score 12) — Design capacity — PM — contractor onboarding W3
- I-003 — Activation event Android flake — Eng — patch in QA, ETA Fri

## Decisions needed THIS WEEK
- [ ] Approve $7k crash (3.1.3 + 2.2.2) for 5d schedule recovery — by Fri — VP Product
- [ ] Approve scope cut: mobile parity → P2 (CR-009) — by Mon — Sponsor

## Metrics dashboard
| Metric | This week | Last week | Δ |
|---|---|---|---|
| % complete (EV/BAC) | 55% | 47% | +8% |
| CPI | 1.02 | 1.05 | -0.03 |
| SPI | 0.96 | 0.98 | -0.02 |
| Open risks (RED zone) | 2 | 0 | +2 |
| Velocity (last cycle, pts) | 28 | 25 | +3 |
| Defects open (P1) | 0 | 0 | 0 |

## Calendar (next 2 weeks)
- Mon 6/22: Sprint 28 planning
- Tue 6/23: Design review
- Wed 6/24: Sponsor 1:1
- Fri 6/26: Stage-gate G3 review
- Mon 6/29: Cycle 27 retro
```

### Recipe 2: Sponsor brief (1-page Manage-Closely)
```markdown
# [Project] — Sponsor Brief — Week of [YYYY-MM-DD]

**TL;DR:** Beta shipped Tue; SSO refactor at risk; need $7k crash approval by Fri to hold ship.

## RAG
🟢 Scope · 🟠 Schedule · 🟢 Budget · 🟢 Quality · 🟠 Risk

## Top-3 risks
1. R-007 — SSO cert renewal — Eng Lead — mitigation in flight
2. R-002 — Design capacity — PM — contractor onboarding W3
3. I-003 — Android activation flake — Eng — patch in QA ETA Fri

## Decisions needed
- [ ] Approve $7k crash (3.1.3 + 2.2.2) — by Fri
- [ ] Approve CR-009 mobile parity → P2 — by Mon

## What changed
- Beta to 5 design partners shipped (M2 hit)
- 2 risks moved to RED zone

## Next week
- Beta feedback synthesis (Wed)
- Stage-gate G3 (Fri)
```

### Recipe 3: Biweekly status (slower-tempo project)
```markdown
# [Project] — Biweekly Status — [YYYY-MM-DD → YYYY-MM-DD]

[Same structure as Recipe 1, but cover 2 weeks of accomplishments + next 2 weeks plan]

## Burndown trend (2-week)
[Embed PNG: planned vs actual % complete]

## Risk velocity (2-week)
[Embed PNG: new risks / closed risks]

## EVM detail
[Recipe 1 metrics + 2-week trend lines]
```

### Recipe 4: Monthly steering update
```markdown
# [Project] — Monthly Steering — [YYYY-MM]

## Section 1: TL;DR (Recipe 2 sponsor brief above)

## Section 2: 4-week trend
[Burndown + risk velocity + EVM 4 data points]

## Section 3: OKR check-in
- Project objectives → KR linkage
- KR progress this month
- Forecast vs OKR target

## Section 4: Variance analysis
- Budget vs baseline: actual EAC vs BAC
- Schedule vs baseline: critical path slip vs allowed buffer
- Scope vs baseline: CRs approved this month, queue size

## Section 5: Portfolio context
- Where this project fits in Q3 portfolio
- Cross-project dependency status

## Section 6: Sponsor decisions captured this month
[List with dates]

## Section 7: Lessons learned (mid-project)
[Top 2-3 observations + actions]
```

### Recipe 5: Quarterly board update
```markdown
# [Project] — Quarterly Board Update — Q[N] [YYYY]

## Section 1: Outcomes
- Success criteria vs target (baseline → actual)
- ROI analysis if applicable

## Section 2: Portfolio context
- Strategic alignment score
- Where this project landed in portfolio

## Section 3: Investment summary
- BAC vs EAC
- ROI: outcome $ value / project cost

## Section 4: Next-quarter intent
- Continuing? Pivoting? Closing? Phase 2?
- Resource asks

## Section 5: Lessons learned (final or interim)
[3-5 observations + system changes]
```

### Recipe 6: Auto-aggregate Linear cycle data
```bash
# Pull current cycle status for the Accomplishments + Velocity sections
curl -s "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query":"query($id:String!){ cycle(id:$id){ name progress issues { nodes { title state{ name } estimate completedAt } } } }","variables":{"id":"<cycle-id>"}}' \
| jq '{
    velocity_pts: ([.data.cycle.issues.nodes[] | select(.state.name=="Done") | .estimate | numbers] | add),
    completed_titles: [.data.cycle.issues.nodes[] | select(.state.name=="Done") | .title]
  }'
```

### Recipe 7: Auto-aggregate Harvest for Budget RAG
```bash
ac=$(curl -s "https://api.harvestapp.com/v2/reports/time/projects?from=2026-06-15&to=2026-06-19&project_id=12345" \
  -H "Authorization: Bearer $HARVEST_TOKEN" -H "Harvest-Account-Id: $HARVEST_ACCOUNT_ID" -H "User-Agent: PM-Agent (you@email.com)" \
  | jq '.results[0].total_cost')

pct=$(curl -s "https://api.linear.app/graphql" -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query":"{ project(id:\"<id>\") { progress } }"}' | jq '.data.project.progress')

BAC=180000
EV=$(echo "$BAC * $pct" | bc -l)
CPI=$(echo "$EV / $ac" | bc -l)

case 1 in
  $(echo "$CPI >= 0.95" | bc -l) ) rag="🟢" ;;
  $(echo "$CPI >= 0.90" | bc -l) ) rag="🟠" ;;
  *) rag="🔴" ;;
esac
echo "Budget RAG: $rag (CPI $CPI)"
```

### Recipe 8: Auto-aggregate RAID for Risk RAG
```bash
mcp tool notion.query_database \
  --database_id "<raid-db-id>" \
  --filter '{"and":[{"property":"Status","select":{"does_not_equal":"Closed"}},{"property":"Type","select":{"equals":"Risk"}}]}' \
| jq '{
    open_count: (.results | length),
    high_zone: ([.results[] | select(.properties.Score.formula.number >= 13)] | length),
    rag: (if ([.results[] | select(.properties.Score.formula.number >= 13)] | length) > 0 then "🔴"
          elif ([.results[] | select(.properties.Score.formula.number >= 6)] | length) > 2 then "🟠"
          else "🟢" end)
  }'
```

### Recipe 9: Status report orchestration script (Friday cron)
```bash
#!/usr/bin/env bash
# weekly-status.sh — runs Friday 8am
# Aggregates Linear + Harvest + RAID; renders Recipe 1 template; sends via gmail + slack + Notion archive

set -euo pipefail
WEEK=$(date +%Y-%m-%d)

# Aggregate
linear=$(./agg-linear.sh)
budget=$(./agg-harvest.sh)
raid=$(./agg-raid.sh)

# Render template (jinja2 or substitute)
jinja2 status-template.md.j2 \
  --data "linear=$linear,budget=$budget,raid=$raid,week=$WEEK" \
  > status-$WEEK.md

# Archive to Notion
mcp tool notion.create_page \
  --parent '{"database_id":"<status-archive-id>"}' \
  --properties "{\"Name\":{\"title\":[{\"text\":{\"content\":\"Status $WEEK\"}}]}}" \
  --children "$(cat status-$WEEK.md)"

# Email
mcp tool gmail.send_message \
  --to "$STAKEHOLDER_LIST" \
  --subject "[Onboarding Revamp] Weekly status — $WEEK" \
  --body "$(cat status-$WEEK.md)"

# Slack
mcp tool slack.send_message \
  --channel "#proj-onboarding-revamp" \
  --text "Weekly status posted: <link>"
```

### Recipe 10: RAG semantics (calibration)
```
🟢 GREEN  | On plan or ahead; risks within tolerance; no decisions needed
🟠 AMBER  | Off plan or new risk emerged; mitigation owned; decision may be needed
🔴 RED    | Material slip OR unmitigated risk OR scope/budget breach; DECISION needed THIS week
⚫ BLACK  | Crisis; incident; sponsor escalation; ship-blocker (rare; usually emergency comms)

NEVER mark green when amber: sandbagging RAG destroys trust late-stage.
```

### Recipe 11: Decisions-needed sub-template
```markdown
## Decisions needed
| # | Decision | By date | Owner | Impact if delayed |
|---|---|---|---|---|
| 1 | Approve $7k crash (3.1.3 + 2.2.2) | 2026-06-26 | VP Product | +5d slip persists; Q3 GA at risk |
| 2 | Approve CR-009 mobile → P2 | 2026-06-29 | Sponsor | $5.6k overrun continues |
| 3 | Confirm contractor SOW for design | 2026-06-24 | Sponsor | Design capacity gap W4 |
```

### Recipe 12: Status archive Notion DB schema
```yaml
Database: "Status Reports — [Project]"
Properties:
  Name:                 title          # "Status YYYY-MM-DD"
  Week:                 date
  RAG_overall:          formula        # most-severe of dimensions
  RAG_scope:            select
  RAG_schedule:         select
  RAG_budget:           select
  RAG_quality:          select
  RAG_risk:             select
  Velocity_pts:         number
  CPI:                  number
  SPI:                  number
  Open_risks_red:       number
  Author:               person
  Distribution:         multi_select   # email-sent / slack-posted / notion-archived / steering-presented
```

## Examples

### Example 1: Generate Friday weekly status
**Goal:** 10am Friday, ready to send by 5pm.

**Steps:**
1. Run Recipe 9 cron at 8am — auto-fetches Linear + Harvest + RAID.
2. PM reviews + edits at 10am — adds Executive Summary 3-5 lines.
3. Calibrate RAG (Recipe 10) — no sandbagging.
4. Capture Decisions Needed (Recipe 11).
5. Archive to Notion + email stakeholders + Slack post.
6. Update Sponsor brief (Recipe 2) as separate 1-pager to Alice.

**Result:** Weekly status sent by 5pm; sponsor 1:1 Wed has fresh context.

### Example 2: Sponsor brief for sudden-RED situation
**Goal:** Critical-path slip hit Tue; need same-day sponsor brief.

**Steps:**
1. Pull current cycle state (Recipe 6).
2. Quantify schedule slip + recovery options (cross-link critical-path-method-cpm).
3. Write Recipe 2 sponsor brief — TL;DR + RAG + decision needed.
4. Email + Slack DM sponsor + book emergency 15-min sync.

**Result:** Sponsor briefed by EOD Tue; decision Wed; mitigation Mon.

## Edge cases / gotchas

- **Outcome-led, not activity-led.** "We held 3 meetings" is bad. "We unblocked the SSO refactor; ship date holds" is good.
- **RAG sandbagging.** Marking green when amber to "not alarm sponsor" = late-stage trust destruction. Calibrate honestly.
- **Decisions Needed without owner + date = decisions not made.** Always include both.
- **One TL;DR rule.** Sponsor brief TL;DR ≤ 2 sentences. If you can't summarize that short, you haven't decided what matters.
- **Auto-aggregation drift.** Auto-pulled numbers may be wrong if PM tool data is stale; sanity check before send.
- **Email + Slack + Notion archive.** All 3 channels. Email = stakeholders; Slack = team; Notion = archive. Don't skip any.
- **Status report ≠ minutes.** Minutes are meeting record; status is outcome update. Don't paste minutes into status.
- **Frequency tuning.** Active projects = weekly; mature/maintenance = biweekly or monthly. Don't over-report dormant projects.
- **Audience-tailored views.** Same data, different summaries: sponsor brief (1-page); team status (full); board update (portfolio context).
- **Metrics that don't move = drop them.** If a metric is 0 every week, it's not measuring anything. Trim.
- **Comparing to last week ≠ trend.** Show 4+ data points for trend; 1-week deltas can be noise.
- **Calendar block at top or bottom?** Bottom — events are reference, not headline.
- **Antipattern: "color-coded list of statuses."** RAG is the dashboard; the body must explain WHY.
- **Stale Last_status_update in PM tool.** If you only refresh status in the PM tool monthly, weekly status report numbers will diverge. Sync cadences.
- **Personal voice.** First-person plural ("we shipped"). Not third-person ("the team shipped"). Builds ownership.

## Sources

- [Asana status report templates](https://asana.com/templates/status-report)
- [Atlassian project status report guide](https://www.atlassian.com/agile/project-management/status-report)
- [Lenny Rachitsky: how to write a great weekly update](https://www.lennysnewsletter.com/p/how-to-write-a-great-weekly-update)
- [Smartsheet status templates](https://www.smartsheet.com/free-project-status-templates)
- [PMBOK 7th Edition: stakeholder + communications](https://www.pmi.org/standards/pmbok)
- [Notion status archive template](https://www.notion.com/templates/category/status-tracker)
- [PMI status reporting best practices](https://www.pmi.org/learning/library/effective-project-reporting-9979)
