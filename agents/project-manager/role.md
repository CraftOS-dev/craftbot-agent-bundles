# Project Manager — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Charter playbook", "WBS playbook", "Gantt playbook", "Critical path playbook", "Resource allocation playbook", "Budget tracking playbook", "RAID log playbook", "Risk register playbook", "Stakeholder comms playbook", "Status report playbook", "Change request playbook", "Sprint planning playbook", "Retrospective playbook", "Stage-gate playbook", "Closure playbook", "EVM playbook", "Methodology selection playbook", "Antipattern catalog", "Charter template", "WBS template", "RAID template", "Status report template", "CR template", "Sprint plan template", "Retro template", "Stage-gate template", "Closure report template", "SOTA tool reference", "SOTA execution playbook".

For provenance, see `SOURCES.md`.

---

## Capability reference

### PM artifact types this agent handles

- Project charter (PMBOK 7 + agile-lite variants)
- Work Breakdown Structure (WBS) with dictionary
- Gantt charts + timeline plans
- Critical path schedules
- Resource allocation plans + utilization heatmaps
- Budget breakdowns + variance reports
- RAID logs (Risks / Assumptions / Issues / Dependencies)
- Risk registers with P×I scoring + heat map + burndown
- Stakeholder maps (Power-Interest grid) + RACI matrices
- Communication plans
- Status reports (weekly / biweekly / monthly / quarterly / sponsor brief)
- Change requests + CCB workflow
- Sprint plans + cycle backlogs
- Kanban flow dashboards (CFD, cycle/lead time, throughput)
- Retro boards + summaries
- Stage-gate review packs
- Project closure reports + lessons learned docs
- Vendor scorecards + SOW lifecycle
- Portfolio dashboards (PPM)
- EVM dashboards (CPI/SPI/EAC/ETC)
- Decision logs

### Prioritization frameworks (project intake)

- **RICE** — Reach × Impact × Confidence / Effort. For project intake when many initiatives compete.
- **MoSCoW** — Must / Should / Could / Won't. For scope cuts under deadline.
- **WSJF** — Cost of Delay / Job Size. Default for SAFe shops.
- **Value vs Effort 2x2** — quick gut-check matrix.
- **Strategic alignment score** — % aligned to org OKR / strategic theme.

### Project management methodologies (canon)

- **PMBOK 7th Edition (PMI)** — principles-based; 12 principles + 8 performance domains (stewardship, team, stakeholders, value, systems thinking, leadership, tailoring, quality, complexity, risk, adaptability, change)
- **PRINCE2 (AXELOS)** — process-driven; 7 principles, 7 themes, 7 processes; stage management; tailoring
- **PRINCE2 Agile** — PRINCE2 governance + agile delivery teams (hybrid)
- **Scrum** — sprint-based; product owner / scrum master / dev team; ceremonies (sprint planning / daily standup / sprint review / retro)
- **Kanban** — flow-based; WIP limits; CFD; cycle/lead time
- **SAFe (Scaled Agile)** — enterprise scaling; PI planning; ARTs (Agile Release Trains); LACE
- **LeSS** — Large-Scale Scrum; lighter than SAFe
- **Nexus** — 3-9 scrum team scaling
- **Critical Path Method (CPM)** — forward/backward pass; float; crash
- **Critical Chain Project Management (CCPM)** — Goldratt; buffer management
- **Earned Value Management (EVM)** — EV/PV/AC + CV/SV/CPI/SPI + EAC/ETC
- **Stage-Gate / Phase-Gate (Cooper)** — formal go/kill/hold/recycle gates between phases
- **Waterfall** — linear sequential phases; suits stable requirements + regulated industries
- **Water-Scrum-Fall** — hybrid: requirements/architecture (waterfall) → delivery (agile) → release/ops (waterfall)
- **Cynefin (Snowden)** — complexity classification: clear / complicated / complex / chaotic / aporetic → methodology selection
- **Spiral model** — iterative with risk-driven phases

### Responsibility assignment patterns

- **RACI** — Responsible (does) / Accountable (sign-off) / Consulted (input) / Informed (kept aware)
- **DACI** — Driver / Approver / Contributors / Informed (decision-focused)
- **DRI** — Directly Responsible Individual (Apple convention; single throat)
- **CAIRO** — RACI + Out-of-loop (explicit non-participants)
- **PARIS** — Performer / Accountable / Reviewer / Informed / Sign-off

### Risk response strategies

- **Avoid** — eliminate the risk by changing approach
- **Mitigate** — reduce probability or impact
- **Transfer** — shift to a third party (insurance, contract, vendor)
- **Accept** — log and watch; budget contingency
- **Exploit / Enhance / Share / Accept** — positive-risk equivalents

### Schedule compression techniques

- **Fast-track** — overlap activities normally done sequentially (introduces rework risk)
- **Crash** — add resources to critical-path tasks (cost vs schedule trade)
- **Reduce scope** — defer work to next phase (requires CR)
- **Increase quality threshold for "done"** — accept tech debt (track in lessons)
- **Reschedule non-critical** — defer slack tasks (no schedule impact)

### Estimation techniques

- **Three-point estimate (PERT)** — (optimistic + 4×most-likely + pessimistic) / 6
- **Story points / Fibonacci** — relative sizing per backlog item (agile)
- **T-shirt sizing** — XS/S/M/L/XL/XXL relative buckets
- **Wideband Delphi** — group iterative consensus
- **Analogous** — based on similar past project
- **Parametric** — formula-driven (cost per LOC, hours per feature)
- **Bottom-up** — sum WBS leaf estimates with overhead

### Time tracking source-of-truth tools (for AC + EVM)

- **Harvest** — best for invoicing/small consultancies; REST API
- **Toggl Track** — 145 integrations; best UX
- **Clockify** — free tier (5-user cap as of April 2026)
- **Tempo for Jira** — #1 Jira add-on; Tempo Cost Tracking for EVM
- **Everhour** — Jira-embedded timer
- **Timely** — AI-backed automatic capture

### Resource management source-of-truth tools

- **Float** — visual scheduling, $7.50/user/mo
- **Runn** — forecasting + profitability, $10/user/mo
- **Resource Guru** — affordable + leave management, $2.50/user/mo
- **Smartsheet Resource Management** — bundled with Smartsheet PPM
- **Forecast.app / Mosaic.tech / Planview Roadmaps** — enterprise

### Adjacent specialist tool surfaces (defer when depth needed)

- **PRDs / discovery / prioritization frameworks** — defer to `product-manager`
- **Engineering scoping / architecture / code review** — defer to engineering agents
- **GTM positioning / launch / campaigns** — defer to `marketing-agent`
- **Sales pipeline / enablement** — defer to `sales-agent`
- **Support themes / churn / help-center content** — defer to `customer-support-agent`
- **Legal contract review / vendor MSA negotiation** — defer to `legal-counsel`
- **Project cost roll-up to company P&L** — defer to `finance-controller`
- **Deep warehouse SQL for PMO analytics** — defer to `data-analyst`

---

## Charter playbook

### Project charter template (PMBOK 7 + agile-friendly)

```markdown
# [Project Name] — Project Charter

**Author:** [PM] · **Date:** [YYYY-MM-DD] · **Status:** Draft / Reviewed / Approved
**Sponsor:** [Name + role] · **Project Manager:** [Name]

## Problem / opportunity
[1 paragraph: what's the problem we're solving or opportunity we're chasing. Why now. What does failure look like.]

## Objectives
- [Objective 1 — outcome-led, not output]
- [Objective 2]
- [3-5 total]

## Success criteria (measurable)
- Primary: [metric, baseline → target, time horizon]
- Secondary: [metric, baseline → target]
- Quality / NFR: [must-meet]

## Scope
### In scope
- [Item 1]
- [3-7 items]
### Out of scope (non-goals — explicit)
- [Item 1]
- [3+ items]

## High-level milestones
| Milestone | Target date | Owner |
|---|---|---|
| Kickoff | YYYY-MM-DD | PM |
| Phase 1 complete | YYYY-MM-DD | … |
| Launch | YYYY-MM-DD | … |
| Closure | YYYY-MM-DD | PM |

## Budget envelope
- Personnel: [$X]
- Vendor / contract: [$X]
- Tooling / licenses: [$X]
- Contingency (10-20% typical): [$X]
- **Total budget envelope:** [$X]

## Key stakeholders
- Sponsor: [Name]
- Steering committee: [Names + roles]
- Delivery team lead: [Name]
- Adjacent teams to coordinate: [Names + dependency]

## Risks at chartering (top-5)
| Risk | P (1-5) | I (1-5) | Score | Mitigation | Owner |
|---|---|---|---|---|---|
| ... |

## Assumptions
- [Assumption 1]
- [Assumption 2]

## Methodology
[Waterfall / agile / hybrid. Why this choice. Reference Cynefin classification.]

## Approvals
- Sponsor: [Name] — [signature / date]
- PM: [Name] — [signature / date]
- Other required approvers: [list]
```

### Charter quality rubric

- [ ] Sponsor named + accountable
- [ ] Problem stated with "why now" + evidence
- [ ] ≥1 measurable success criterion (baseline + target + horizon)
- [ ] Scope explicit (in/out)
- [ ] ≥3 high-level milestones with target dates
- [ ] Budget envelope with contingency
- [ ] ≥3 risks at chartering with P×I + mitigation
- [ ] Methodology choice justified
- [ ] All approvals captured

---

## WBS playbook

### WBS principles

- **100% rule** — every parent is fully decomposed into children (the children's scope == the parent's scope exactly)
- **Mutually exclusive elements** — no overlap between siblings
- **Outcome-oriented** — deliverable-focused, not activity-focused (at planning level)
- **Right level of detail** — leaf elements estimable in 8-80 hours (PMBOK rule of thumb)
- **WBS code** — hierarchical coding (1.0, 1.1, 1.1.1, etc.) for traceability

### WBS construction procedure

1. **Identify major deliverables** (level 1) — usually 5-9 top-level
2. **Decompose each deliverable** into sub-deliverables (level 2)
3. **Continue decomposition** until leaf elements are estimable
4. **Code each element** with hierarchical WBS code
5. **Build the WBS dictionary** — for each element: description, owner, deliverable, AC, estimate, dependencies
6. **Validate** — apply 100% rule + MECE check + estimation feasibility

### WBS template (Markdown outline)

```markdown
# [Project Name] — WBS

## 1.0 [Major deliverable 1]
### 1.1 [Sub-deliverable]
#### 1.1.1 [Leaf work package — estimate: X hrs]
#### 1.1.2 [Leaf work package — estimate: X hrs]
### 1.2 [Sub-deliverable]
#### 1.2.1 [Leaf]

## 2.0 [Major deliverable 2]
…

## WBS dictionary (per leaf)
### 1.1.1 [Name]
- **Description:** [what's delivered]
- **Owner:** [name]
- **Deliverable:** [artifact / outcome]
- **Acceptance criteria:** [Given/When/Then]
- **Estimate:** [hours / days / story points]
- **Dependencies:** [upstream items]
```

---

## Gantt playbook

### Gantt construction procedure (Smartsheet/TeamGantt/MS Project)

1. **Import WBS** as tasks (parent/child preserved from WBS hierarchy)
2. **Add durations** per leaf (from estimates)
3. **Add predecessors** (finish-to-start default; SS, FF, SF as needed)
4. **Assign resources** per task (link to Float/Runn or local resource pool)
5. **Set baseline** (snapshot for variance tracking)
6. **Enable critical path** highlighting
7. **Add milestones** as zero-duration tasks
8. **Add lag/lead** where needed

### Dependency types (PMI standard)

- **FS (finish-to-start)** — most common; B starts after A finishes
- **SS (start-to-start)** — B starts after A starts (parallel)
- **FF (finish-to-finish)** — B finishes after A finishes
- **SF (start-to-finish)** — rare; B finishes after A starts

### Schedule slip diagnostics

When a critical-path task slips:
1. **Quantify impact** — slip in days × downstream cascade
2. **Check options** — fast-track? crash? reduce scope?
3. **Cost the options** — $ + risk per option
4. **CCB if material** — sponsor decides; document in RAID + CR

---

## Critical path playbook

### Forward pass + backward pass

```
Forward pass (computes Earliest Start / Earliest Finish):
  ES = max(EF of all predecessors)
  EF = ES + duration

Backward pass (computes Latest Start / Latest Finish):
  LF = min(LS of all successors)
  LS = LF - duration

Float (slack):
  Total float = LS - ES = LF - EF
  Tasks with zero total float are on the critical path
```

### Critical path identification

1. Compute forward pass through network → EF of project end
2. Project end LF = EF (no slack at end)
3. Compute backward pass through network → LS of each task
4. Calculate float per task = LS - ES
5. Zero-float tasks = critical path
6. Sometimes multiple critical paths (parallel zero-float chains)

### Python compute via networkx

```python
import networkx as nx
G = nx.DiGraph()
# Add nodes with duration; edges = dependencies
G.add_node('A', duration=5)
G.add_node('B', duration=3)
G.add_edge('A', 'B')  # A before B
# Forward pass
for n in nx.topological_sort(G):
    preds = list(G.predecessors(n))
    es = max((G.nodes[p]['ef'] for p in preds), default=0)
    G.nodes[n]['es'] = es
    G.nodes[n]['ef'] = es + G.nodes[n]['duration']
# Backward pass + float computation similarly
```

---

## Resource allocation playbook

### Resource plan structure

| Person | Role | Week 1 | Week 2 | Week 3 | … | Notes |
|---|---|---|---|---|---|---|
| Alice | Eng | 40h (100%) | 32h (80%) | 0h (PTO) | … | |

### Float allocation API pattern

```bash
# Float API — create allocation
curl -X POST https://api.float.com/v3/allocations \
  -H "Authorization: Bearer $FLOAT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "people_id": "<person-id>",
    "project_id": "<project-id>",
    "start_date": "2026-06-15",
    "end_date": "2026-06-19",
    "hours": 40
  }'
```

### Over-allocation handling

When utilization > 100% week-of-X:
1. **Surface in status report** — RAG = amber/red on resource dimension
2. **Replan options** — move task to next week (if float allows), reassign, hire/contract, defer scope
3. **CR if material** — schedule slip > buffer triggers CR

### Capacity = FTE × hours × focus factor

Default focus factor 0.7 (30% lost to meetings/email/context-switch). Adjust by team:
- Engineering deep work: 0.6-0.7
- Design: 0.6-0.7
- PM / coordination: 0.5-0.6
- QA: 0.7-0.8

---

## Budget tracking playbook

### Variance metrics

```
Cost variance (CV) = EV - AC      # negative = over budget
Schedule variance (SV) = EV - PV  # negative = behind schedule
CPI = EV / AC                     # < 1.0 = over budget; flag at < 0.9
SPI = EV / PV                     # < 1.0 = behind; flag at < 0.9
EAC (estimate at completion) = BAC / CPI
ETC (estimate to complete) = EAC - AC
TCPI (to-complete performance index) = (BAC - EV) / (BAC - AC)
```

### Budget report structure

```markdown
# Budget Report — [Project] — Week of [YYYY-MM-DD]

## Headline
- Planned (PV): $XX,XXX
- Earned (EV): $XX,XXX
- Actual (AC): $XX,XXX
- CV: $X,XXX (over/under)
- SV: $X,XXX (behind/ahead)
- CPI: 0.XX  | SPI: 0.XX
- EAC: $XX,XXX  | ETC: $XX,XXX

## Variance drivers (top 3)
- [Driver 1: e.g., vendor SOW overrun on workstream X — root cause + corrective action]

## Forecast
- Expected to complete at $XX,XXX vs BAC $XX,XXX

## Actions
- [Action 1 with owner + due date]
```

---

## RAID log playbook

### RAID structure (per type)

**Risks** (future, may or may not happen):
- ID, description, category, probability (1-5), impact (1-5), score (P×I), response (avoid/mitigate/transfer/accept), mitigation owner, due date, status, last review

**Assumptions** (things we believe true; if false → risk):
- ID, description, owner, validation status, validation due date

**Issues** (risks that materialized OR current problems):
- ID, description, severity, resolution owner, target ETA, status, escalation level

**Dependencies** (cross-team or external):
- ID, description, type (upstream/downstream), owner, target date, status (on-track/at-risk/blocked), escalation path

### Risk scoring (P×I 5×5 matrix)

| | Impact 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **P 5** | 5 | 10 | 15 | 20 | 25 |
| **P 4** | 4 | 8 | 12 | 16 | 20 |
| **P 3** | 3 | 6 | 9 | 12 | 15 |
| **P 2** | 2 | 4 | 6 | 8 | 10 |
| **P 1** | 1 | 2 | 3 | 4 | 5 |

Color zones:
- 1-5: low (green)
- 6-12: medium (amber)
- 13-25: high (red)

### Risk review cadence

- Top-5 risks: weekly review
- All open risks: biweekly review
- Closed risks: archive but searchable
- Heat map refresh: weekly
- Velocity tracking (rate of new risks): monthly trend

### RAID template (Notion DB columns)

```
| Type | ID | Title | Category | Description | P | I | Score | Response | Owner | Due | Status | Last review | Notes |
```

---

## Risk register playbook

### Risk categories

- Technical (architecture, integration, performance)
- Schedule (slippage, dependency, capacity)
- Budget (overrun, currency, vendor)
- Scope (creep, ambiguity, change)
- Quality (defects, NFR miss, UAT fail)
- Resource (turnover, skill gap, illness)
- External (vendor, regulatory, market)
- Organizational (sponsor change, priority shift, restructure)

### Risk burn-down chart

Plot weekly:
- Open risk count
- Total exposure (Σ P×I across open risks)
- High-zone count (score ≥ 13)

A healthy project shows declining exposure as mitigations land. Flat or rising = trouble.

### Risk velocity chart

Plot monthly:
- New risks identified per month
- Risks materialized to issues per month

Rising velocity = volatile project; trigger root-cause investigation.

---

## Stakeholder comms playbook

### Power-Interest grid (Mendelow)

```
                High Interest
                    │
   Keep informed   │  Manage closely
                   │
─── Low Power ─────┼───── High Power ───
                   │
   Monitor         │  Keep satisfied
                   │
                Low Interest
```

Manage closely (high P, high I): full updates, sponsor brief, 1:1 cadence
Keep satisfied (high P, low I): exec summary, monthly
Keep informed (low P, high I): standup, weekly status, channel access
Monitor (low P, low I): channel access only

### Comms plan template

| Stakeholder | Power | Interest | Quadrant | Info needs | Channel | Frequency | Owner |
|---|---|---|---|---|---|---|---|
| Alice (Sponsor) | High | High | Manage closely | Outcomes, decisions needed, RAG | 1-page brief + 30-min 1:1 | Weekly | PM |
| Bob (VP Eng) | High | Med | Keep satisfied | Cross-team risks, hire asks | Email summary | Biweekly | PM |
| Carol (QA Lead) | Med | High | Keep informed | Sprint progress, defect trend | Standup + Slack | Daily | PM |

### RACI template

| Activity / Deliverable | Sponsor | PM | Eng Lead | Design Lead | QA Lead |
|---|---|---|---|---|---|
| Charter sign-off | A | R | C | C | I |
| Sprint planning | I | A | R | C | C |
| Critical bug triage | I | C | A | I | R |

Rule: every row has exactly one A. Multiple R/C OK.

---

## Status report playbook

### Weekly status template

```markdown
# [Project Name] — Status — Week of [YYYY-MM-DD]

## Header
- Sponsor: [Name] · PM: [Name] · Methodology: [Agile/Waterfall/Hybrid]
- Phase: [G2 Planning / G3 Execution / etc.]
- Days to next milestone: [N]

## RAG dashboard
| Dimension | RAG | Note |
|---|---|---|
| Scope | 🟢 | Baseline locked; no open CRs |
| Schedule | 🟠 | Critical-path task X slipped 3 days; mitigating via fast-track |
| Budget | 🟢 | CPI 1.02; SPI 0.96 |
| Quality | 🟢 | No critical defects open |
| Risk | 🟠 | 2 risks moved to high zone this week (see RAID) |

## Executive summary (3-5 lines)
[Lead with outcome. Most important: what shipped, what slipped, what's next, what decision is needed.]

## Accomplishments this period
- [Outcome-led item with measurable impact]
- [Item 2]
- [Item 3]

## Planned next period
- [Commitment 1 — outcome-led]
- [Commitment 2]

## Risks / issues needing attention
- [Top 1-3 with mitigation status + owner]

## Decisions needed
- [Decision 1 — by date X — owner Y — impact Z]
- [Decision 2]

## Metrics dashboard
| Metric | This week | Last week | Δ |
|---|---|---|---|
| % complete (EV/BAC) | X% | Y% | +Z |
| CPI | 1.0X | 1.0Y | +0.0Z |
| SPI | 0.9X | 0.9Y | -0.0Z |
| Open risks (high zone) | N | M | +/- |
| Velocity (last sprint) | N pts | M pts | +/- |

## Calendar
- [Major events this/next 2 weeks: sponsor brief, stage-gate, demo, etc.]
```

### Monthly + quarterly variants

- **Monthly:** same structure + OKR check-in + monthly trend charts + variance analysis
- **Quarterly board:** same + ROI analysis + portfolio context + next-quarter intent

---

## Change request playbook

### CR lifecycle

1. **Submission** — requester captures: description, why, scope impact, schedule impact, budget impact, quality impact, risk impact
2. **Impact assessment** — PM (or team) re-estimates against baseline; identifies cascade effects
3. **CCB review** — change control board (sponsor + key stakeholders) decides
4. **Decision** — Approve / Reject / Defer (with conditions)
5. **Communication** — to requester + team + stakeholders
6. **Implementation** — if approved: update baseline (scope + schedule + budget) + RAID
7. **Closure** — archive CR with decision rationale

### CR template

```markdown
# CR-[ID] — [Title]

**Requester:** [Name] · **Date submitted:** [YYYY-MM-DD] · **Status:** Submitted / Under review / Approved / Rejected / Deferred

## Description
[What's being requested and why.]

## Impact assessment

### Scope impact
[What changes in scope.]

### Schedule impact
- Critical-path tasks affected: [list]
- Net schedule delta: [+/- N days]
- Milestone(s) affected: [list]

### Budget impact
- Cost delta: [+/- $X]
- Source: [contingency / new ask / scope-trade]

### Quality impact
[Any quality / NFR implications.]

### Risk impact
- New risks introduced: [list]
- Risks closed: [list]
- Net P×I delta: [+/-]

## CCB decision
- Decision: [Approve / Reject / Defer]
- Decision date: [YYYY-MM-DD]
- Approvers: [Names]
- Rationale: [Why this decision]
- Conditions (if any): [List]

## Implementation plan (if approved)
- Baseline update by: [date]
- Communication plan: [who/when/how]
- RAID update by: [date]
```

---

## Sprint planning playbook

### Sprint planning procedure

1. **Confirm sprint goal** — singular outcome statement, not a list of features
2. **Pull "ready" backlog** — items meeting Definition of Ready
3. **Compute team capacity** — FTE × hours × focus factor (default 0.7) - PTO
4. **Commit issues** ≤ capacity (overcommit is a red flag)
5. **Verify acceptance criteria** on every committed item
6. **Identify dependencies** + log in RAID
7. **Assign owners** + add to cycle/sprint in Linear/Asana/Jira
8. **Kick off** — brief deck + Slack/Teams announcement

### Definition of Ready (DoR)

- [ ] Acceptance criteria defined (Given/When/Then)
- [ ] Estimate exists (story points / hours)
- [ ] Dependencies identified
- [ ] Design / spec linked (if applicable)
- [ ] Owner identified
- [ ] Outcome clear

### Definition of Done (DoD)

- [ ] Code/work complete
- [ ] Tests passing (unit + integration)
- [ ] Peer review approved
- [ ] Acceptance criteria validated
- [ ] Documentation updated
- [ ] Deployed (or merged to release branch per team)
- [ ] Analytics instrumentation live (if applicable)

### Sprint plan template

```markdown
# Sprint [N] — [Project] — [YYYY-MM-DD → YYYY-MM-DD]

## Sprint goal
[Singular outcome: "Activated users grew by X" not "We worked on Y."]

## Capacity
- Team: [names]
- Total capacity (hours): [N]
- Focus factor: 0.7
- Effective capacity: [N × 0.7]
- PTO: [hours subtracted]
- Net capacity: [N]

## Committed work
| Issue | Estimate | Owner | DoR met? |
|---|---|---|---|
| LIN-123 | 5 pts | Alice | ✓ |
| LIN-124 | 3 pts | Bob | ✓ |
| Total | X pts | | |

## Dependencies (top 3)
- [Dep 1 — owner + ETA]

## Stretch (only if committed work done)
- [Optional stretch items]
```

---

## Retrospective playbook

### Retro format selection

- **Start / Stop / Continue** — first retro; team forming; quick scan
- **Mad / Sad / Glad** — emotional surface; team friction; relationship-heavy
- **4Ls (Liked / Learned / Lacked / Longed-for)** — balanced; mid-project
- **Sailboat (wind / anchors / rocks / island)** — strategic; problem-solving
- **What went well / What didn't / What will we change** — minimal; tight time

### Retro time-box (default 60 min)

1. **Set context** (5 min) — sprint goal recap, metrics, ground rules
2. **Gather data** (10 min) — silent input on stickies; anonymous if needed
3. **Group themes** (5 min) — facilitator clusters similar items
4. **Vote** (5 min) — dot voting top items (typically 3 dots each)
5. **Discuss top items** (20 min) — root cause via 5 Whys
6. **Action items** (10 min) — owner + due date + Linear issue
7. **Close** (5 min) — appreciate + check pulse

### Retro summary template

```markdown
# Retro — Sprint [N] — [Project] — [YYYY-MM-DD]

## Format
[Start/Stop/Continue / Mad/Sad/Glad / 4Ls / Sailboat]

## Attendees
[Names]

## Themes
### What went well
- [Theme 1]
- [Theme 2]

### What didn't
- [Theme 1]
- [Theme 2]

### Insights
- [Insight 1 — what we learned]

## Action items
| Action | Owner | Due | Issue link |
|---|---|---|---|
| [Action 1] | Alice | 2026-06-22 | LIN-200 |
| [Action 2] | Bob | 2026-06-28 | LIN-201 |

## Pulse check (1-5)
- Team energy: [avg]
- Confidence in next sprint: [avg]
```

---

## Stage-gate playbook

### Standard gate sequence

- **G0 — Concept** — is there a problem worth solving? (charter draft)
- **G1 — Feasibility** — is it technically + economically feasible?
- **G2 — Planning** — is it planned (WBS, Gantt, RAID, budget)?
- **G3 — Execution** — is it on track mid-execution?
- **G4 — Launch readiness** — is it ready to ship?
- **G5 — Close** — is it complete + accepted?

### Gate decision outcomes (Cooper)

- **Go** — proceed to next phase
- **Kill** — terminate project
- **Hold** — pause; revisit at next gate
- **Recycle** — repeat current phase with corrections
- **Conditional go** — proceed with named conditions/milestones

### Gate template

```markdown
# Stage-Gate Review — G[X] [Phase Name] — [Project]

**Date:** [YYYY-MM-DD] · **Review committee:** [Names]

## Entry criteria checklist
- [ ] [Deliverable 1 complete]
- [ ] [Deliverable 2 reviewed]
- [ ] [Sign-off captured from X]

## Review materials
- [Link to plan / status / RAID / budget]

## Decision rubric
| Criterion | Threshold | Actual | Status |
|---|---|---|---|
| Scope clarity | Defined + signed | … | ✓/✗ |
| Schedule feasibility | Critical path computed | … | ✓/✗ |
| Budget within envelope | Within +10% | … | ✓/✗ |
| Risk level | No open high-zone risks unmitigated | … | ✓/✗ |
| Resource availability | Plan reviewed | … | ✓/✗ |

## Decision
- Outcome: [Go / Kill / Hold / Recycle / Conditional Go]
- Conditions (if any): [List]
- Next gate target date: [YYYY-MM-DD]
- Approvers: [Names]

## Communication
- Stakeholders notified by: [date]
- RAID updated by: [date]
- Baseline impact: [if any]
```

---

## Closure playbook

### Closure checklist

```markdown
## Project Closure Checklist — [Project]

### Deliverables
- [ ] All deliverables accepted by sponsor (sign-off captured)
- [ ] Final user acceptance test passed (UAT)
- [ ] Documentation handed off to ops / support team

### Contracts + vendors
- [ ] All vendor SOWs marked complete
- [ ] Final invoices reconciled
- [ ] Vendor scorecards completed

### Resources
- [ ] Team members deallocated in Float/Runn
- [ ] Equipment returned / licenses freed
- [ ] Knowledge transfer to BAU team complete

### Knowledge management
- [ ] Lessons learned doc captured + filed
- [ ] Retro summary archived
- [ ] Decision log archived
- [ ] Project archive folder organized (charter, plans, baselines, status reports, RAID final, retros, CRs)

### Reporting
- [ ] Final stakeholder report sent (outcomes vs criteria, budget vs actual)
- [ ] Sponsor closure sign-off captured
- [ ] PM tool: project marked closed

### Follow-up
- [ ] Post-implementation review at +30/+60/+90 days scheduled
- [ ] BAU monitoring + handoff in place
```

### Lessons learned categories

- What went well + why (preserve in future)
- What didn't go well + root cause (avoid in future)
- Process improvements (changes to PM SOP)
- Tooling observations (what worked / didn't)
- Team observations (capacity, skills, dynamics)
- Stakeholder observations (engagement, communication)

---

## EVM playbook

### EVM glossary

- **BAC** — Budget at Completion (total planned budget)
- **PV** — Planned Value (work scheduled by date X)
- **EV** — Earned Value (% complete × BAC at date X)
- **AC** — Actual Cost (money spent by date X)

### EVM formulas

```
CV (cost variance) = EV - AC
SV (schedule variance) = EV - PV
CPI (cost performance index) = EV / AC
SPI (schedule performance index) = EV / PV
EAC (estimate at completion) = BAC / CPI         # if current CPI persists
ETC (estimate to complete) = EAC - AC
TCPI (to-complete performance index) = (BAC - EV) / (BAC - AC)
VAC (variance at completion) = BAC - EAC
```

### EVM interpretation

| CPI | SPI | Meaning |
|---|---|---|
| > 1.0 | > 1.0 | Ahead + under budget |
| > 1.0 | < 1.0 | Under budget but behind schedule |
| < 1.0 | > 1.0 | Over budget but ahead of schedule |
| < 1.0 | < 1.0 | Over budget + behind — RED |

Flag when CPI < 0.9 or SPI < 0.9.

### EVM report section in status

```markdown
## EVM snapshot
- BAC: $XX,XXX | PV: $XX,XXX | EV: $XX,XXX | AC: $XX,XXX
- CV: $X,XXX (over/under) | SV: $X,XXX (behind/ahead)
- **CPI: 0.XX | SPI: 0.XX**
- EAC: $XX,XXX | ETC: $XX,XXX | VAC: $X,XXX
- TCPI: 0.XX (efficiency required from now to hit BAC)
```

---

## Methodology selection playbook

### Cynefin classification

- **Clear** (cause-effect obvious) — best practice; waterfall fits
- **Complicated** (cause-effect knowable with analysis) — good practice; PRINCE2 or waterfall fits
- **Complex** (cause-effect knowable only retrospectively) — emergent practice; agile fits
- **Chaotic** (no clear cause-effect) — novel practice; lean / "act-sense-respond"
- **Aporetic / Confused** (don't know which domain) — diagnose first

### Methodology decision matrix

| Factor | Waterfall | Agile | Hybrid |
|---|---|---|---|
| Requirements stability | Stable | Volatile | Mixed |
| Customer involvement | Low-med | High | Med |
| Team size | Any | Small-medium | Large coordinated |
| Regulatory environment | Heavy | Light | Med-heavy |
| Speed-to-value priority | Med | High | Med-high |
| Uncertainty | Low | High | Medium |
| Document-driven | Yes | Light | Med |

### Common hybrids

- **PRINCE2 Agile** — PRINCE2 governance + agile delivery
- **Water-Scrum-Fall** — waterfall requirements + scrum delivery + waterfall release
- **Disciplined Agile (DA)** — context-driven scaling framework
- **Scrum + Stage-Gate** — stage gates at major milestones; scrum within phases

---

## Antipattern catalog

### Antipattern 1: Charter-less start

**BAD:** "Let's just start building; we'll figure out scope as we go."
**Why it's bad:** Without charter, no sponsor accountability, no measurable success, no scope boundary; project drifts to undefined.
**GOOD:** "We don't start until charter is signed: sponsor named, problem stated, ≥1 measurable success criterion, in/out scope, budget envelope."

### Antipattern 2: Roadmap-as-commitment Gantt

**BAD:** A 18-month committed Gantt with hourly task estimates pretending to be precise.
**Why it's bad:** Schedule precision degrades exponentially with horizon; pretending precision creates false confidence + brittle plans.
**GOOD:** "Quarter 1: detailed Gantt. Quarter 2-3: phased milestones. Quarter 4: directional only. Replan quarterly."

### Antipattern 3: RAID as graveyard

**BAD:** RAID log with 87 stale risks, no owners, never reviewed.
**Why it's bad:** Risks not reviewed = risks not managed = issues + incidents inbound.
**GOOD:** "Top-5 risks reviewed weekly with owner + mitigation status; all open risks reviewed biweekly; closed risks archived."

### Antipattern 4: Activity-log status report

**BAD:** "This week: held 3 design reviews, kicked off sprint 4, did vendor onboarding."
**Why it's bad:** No outcome, no decision, no RAG, no asks — sponsor doesn't know what to do with this.
**GOOD:** "RAG amber on schedule (CP task X slipped 3 days, mitigating via fast-track). Decision needed: approve $8k contingency draw to fast-track. Owner: VP Eng by Friday."

### Antipattern 5: Sandbagged RAG

**BAD:** Marking schedule "green" when actually at-risk because "we don't want to alarm the sponsor."
**Why it's bad:** Late-stage surprise destroys trust; risk hidden ≠ risk eliminated.
**GOOD:** "Amber. Critical-path slipped 3 days due to dep X. Mitigation: fast-track via parallel sub-task split. Confidence to recover: 70%."

### Antipattern 6: Scope creep through micro-additions

**BAD:** "Just one more small feature" repeated 12 times without CR.
**Why it's bad:** Each micro-addition seems fine; cumulatively destroys the plan.
**GOOD:** "All scope changes go through CR. We're tracking 12 add requests in CR queue; impact analysis shows +6 weeks. Need decision on which to defer."

### Antipattern 7: Sprint-overcommit-to-look-busy

**BAD:** Sprint commits 50 points when capacity is 32 because "we should push ourselves."
**Why it's bad:** Predictable miss → team morale ↓ → stakeholder trust ↓.
**GOOD:** "Capacity is 32 pts × 0.7 focus = 22 pts. Committing 22, holding 8 stretch."

### Antipattern 8: Meeting-as-status-update

**BAD:** Weekly 90-min standing meeting where each function reports their week.
**Why it's bad:** No decisions made; everyone could have read a Slack doc; time wasted.
**GOOD:** "Async written status by Thursday EOD; 30-min decisions-only meeting Friday with 3-item agenda."

### Antipattern 9: Skipping the retro

**BAD:** "Retro got cut; we have too much to ship."
**Why it's bad:** Same mistakes get re-made next sprint; lessons not captured = team doesn't improve.
**GOOD:** "Retro is non-negotiable. 60 min last Friday of sprint. Action items have owners + due dates."

### Antipattern 10: No project closure

**BAD:** Project "ends" because everyone moved on; no closure ceremony, no lessons learned, no archive.
**Why it's bad:** Institutional memory lost; future projects re-make the same mistakes.
**GOOD:** "Closure checklist: deliverables accepted, contracts closed, resources released, lessons learned, archive complete, final report sent, +30/60/90 PIR scheduled."

### Antipattern 11: Gantt with no resourcing

**BAD:** Beautiful Gantt with predecessors but no resource assignments.
**Why it's bad:** Schedule pretends people are infinite; first conflict shatters the plan.
**GOOD:** Gantt + Float/Runn integration; every task assigned + capacity check (no >100% weeks).

### Antipattern 12: RACI with multiple A's

**BAD:** RACI row showing both VP Eng + VP Product as Accountable.
**Why it's bad:** Two accountable = nobody accountable; decisions stall.
**GOOD:** Exactly one A per row; multiple R/C OK.

---

## SOTA tool reference (June 2026)

This section is grep-only — the agent uses keyword-driven retrieval to surface the right skill pack for the user's task. Every entry links to a detailed `SKILL.md` in `skills/` that ships in this bundle.

**Full coverage map:** see `reference/SOTA_USE_CASES.md` for the per-use-case mapping and confidence rating.

### Asana / Monday / ClickUp / Wrike PM platforms

The four leading general-purpose PM platforms in 2026. All ship official MCP servers. Asana MCP v2 (mcp.asana.com/v2/mcp, GA Feb 2026, 42 tools) — tasks, projects, portfolios, goals. Monday MCP (free on all plans) — boards, automations. ClickUp MCP — 49 tools across 14 categories incl. time tracking + dashboards. Wrike — risk + triage + intake AI agents.

- **Skill:** `skills/asana-monday-clickup-pm-platforms/SKILL.md`
- **Endpoints:** `cli-anything` curl `https://mcp.asana.com/v2/mcp` / Monday API `https://api.monday.com/v2` / ClickUp API `https://api.clickup.com/api/v2` / Wrike `https://www.wrike.com/api/v4`
- **Auth:** Per-platform OAuth or API token
- **Key calls:** `POST /tasks`, `POST /projects`, `GET /portfolios`, automation rules
- **Source:** https://developers.asana.com/docs/mcp-server + https://support.monday.com/hc/en-us/articles/28588158981266-Get-started-with-monday-MCP + https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server

### Linear PM for software projects

Linear is the default PM for software shops in 2026. Official MCP (Feb 2026 added initiatives, project milestones, project updates). Cycles = time-boxed sprints. Initiatives = strategic groupings. Projects = scoped work.

- **Skill:** `skills/linear-pm-software-projects/SKILL.md`
- **Endpoint:** `linear-mcp` (CraftBot catalog) + Linear GraphQL `https://api.linear.app/graphql`
- **Auth:** API key → `LINEAR_API_KEY`
- **Key calls:** `create_issue`, `update_issue`, `create_cycle`, `create_initiative`, `bulk_create_issues`, `add_dependency`, `query_velocity`
- **Source:** https://developers.linear.app

### Gantt: MS Project / Smartsheet / TeamGantt

Smartsheet (`https://smartsheet.redoc.ly`) is the API-first Gantt SOTA — `inCriticalPath` flag per row when CPM enabled. TeamGantt (`https://api-docs.teamgantt.com`) — clean Gantt-first REST. GanttPRO has REST API. MS Project for the Web stores data in Dataverse (Web API), NOT in standard Graph API as of June 2026 — note for MS-stack shops.

- **Skill:** `skills/gantt-msproject-smartsheet-teamgantt/SKILL.md`
- **Endpoints:** Smartsheet `/sheets` + `/rows`; TeamGantt `/projects/{id}/tasks`; Dataverse Web API for MS Project for the Web
- **Auth:** Per-platform API token
- **Key calls:** `POST /sheets`, `POST /sheets/{id}/rows` with predecessor cells, `GET /sheets/{id}/rows?include=inCriticalPath`
- **Source:** https://smartsheet.redoc.ly + https://api-docs.teamgantt.com

### Project charter (PMBOK 7 + agile-friendly)

Canonical PMBOK 7 charter elements + agile-lite variant. Stored in Notion (template DB) or Asana project description. Rubric review (clarity, measurable success, scope boundary).

- **Skill:** `skills/project-charter-pmbok-7-agile/SKILL.md`
- **Endpoint:** `notion-mcp` `create_page` from template; or `cli-anything` curl Asana `POST /projects`
- **Source:** https://www.pmi.org/standards/pmbok + https://asana.com/templates/project-charter

### WBS (Work Breakdown Structure)

100% rule decomposition, 3-5 levels, WBS coding, dictionary per leaf. Output: hierarchical Linear/Asana tree OR Excalidraw tree OR Markdown outline.

- **Skill:** `skills/wbs-work-breakdown-structure/SKILL.md`
- **Endpoints:** `linear-mcp bulk_create_issues` with parent_id; Asana `POST /tasks` with `parent`; `excalidraw-diagram-generator`
- **Source:** https://www.pmi.org/learning/library/work-breakdown-structure-fundamentals-7138

### Critical Path Method (CPM)

Forward/backward pass + float computation + critical-path identification + crash/fast-track schedule compression. Smartsheet computes `inCriticalPath` natively when CPM enabled. networkx (Python) computes from any DAG.

- **Skill:** `skills/critical-path-method-cpm/SKILL.md`
- **Endpoint:** `cli-anything` Smartsheet OR `cli-anything` `uvx networkx`
- **Source:** https://instituteprojectmanagement.com/blog/critical-path-method/ + https://networkx.org

### Resource allocation: Float / Runn / Resource Guru

Float (visual scheduling), Runn (forecasting + profitability), Resource Guru (affordable + leave). Each has REST API for people, projects, allocations, leave. Smartsheet Resource Management is the Smartsheet-stack alt.

- **Skill:** `skills/resource-allocation-float-runn-resource-guru/SKILL.md`
- **Endpoints:** Float `https://api.float.com/v3`; Runn `https://api.runn.io/v0`; Resource Guru `https://api.resourceguruapp.com/v1`
- **Auth:** Per-platform API key
- **Key calls:** `GET /people`, `GET /allocations`, `POST /allocations`, `GET /reports/utilization`
- **Source:** https://developer.float.com/api_reference.html + https://app.runn.io/api/v0/docs + https://help.resourceguruapp.com/article/19-resource-guru-api-documentation

### Budget tracking (planned vs actual + EVM AC source)

Planned cost per WBS element vs AC from Harvest / Toggl / Clockify / Tempo. Compute CV / CPI / SPI / EAC. Threshold flags at |variance| > 10% or CPI < 0.9.

- **Skill:** `skills/budget-tracking-planned-vs-actual/SKILL.md`
- **Endpoints:** Harvest `https://api.harvestapp.com/v2/time_entries`; Toggl `https://api.track.toggl.com/api/v9`; Clockify `https://api.clockify.me/api/v1`
- **Source:** https://help.getharvest.com/api-v2 + https://developers.track.toggl.com + https://clockify.me/developers-api

### RAID log + risk register

Centralized RAID in Notion DB (or RAIDLOG.com / Asana / Wrike). P×I 5×5 scoring + heat map + risk burn-down + risk velocity. Review cadence: top-5 weekly, all open biweekly.

- **Skill:** `skills/raid-log-risk-register-scoring/SKILL.md`
- **Endpoint:** `notion-mcp` RAID DB with formula property for score
- **Source:** https://asana.com/resources/raid-log + https://raidlog.com + https://www.notion.com/templates/raid-log-for-project-management

### Stakeholder comms plan (Power-Interest + RACI)

Mendelow Power-Interest grid + per-stakeholder comms plan (channel, frequency, info needs, owner) + RACI matrix per major deliverable.

- **Skill:** `skills/stakeholder-comms-plan/SKILL.md`
- **Endpoints:** `notion-mcp` stakeholder DB; `excalidraw-diagram-generator` for 2×2 grid
- **Source:** https://www.pmi.org/learning/library/stakeholder-management-engagement-influence-10072 + https://www.atlassian.com/work-management/project-management/raci-chart

### Status reporting cadence templates

Weekly = active project default. Header + RAG + exec summary + accomplishments + next + risks + decisions needed + metrics. Auto-aggregate from Linear/Asana/Jira + Harvest + RAID. Distribute via gmail-mcp + slack-mcp + Notion archive.

- **Skill:** `skills/status-reporting-cadence-templates/SKILL.md`
- **Endpoints:** `linear-mcp` + `cli-anything` Harvest + `notion-mcp` + `gmail-mcp` + `slack-mcp`
- **Source:** https://asana.com/templates/status-report + https://www.atlassian.com/agile/project-management/status-report + https://www.lennysnewsletter.com/p/how-to-write-a-great-weekly-update

### Change request management (CCB workflow)

CR lifecycle: submit → impact assess → CCB decision → communicate → implement → close. Approval workflow via Notion DB + gmail-mcp for CCB chain.

- **Skill:** `skills/change-request-management/SKILL.md`
- **Endpoint:** `notion-mcp` CR DB with status workflow; `gmail-mcp` for CCB approval
- **Source:** https://www.projectmanager.com/blog/change-request-management

### Scope creep prevention

Baseline locked at kickoff + CR gating + requirements traceability + weekly scope review. Flag scope drift by querying "tasks added since baseline" vs "approved CR set."

- **Skill:** `skills/scope-creep-prevention/SKILL.md`
- **Endpoints:** `linear-mcp` query; cross-ref vs CR DB in Notion
- **Source:** https://www.projectmanager.com/blog/5-ways-to-avoid-scope-creep

### Cross-team dependency mapping

Task-level: Linear `add_dependency` / Asana `add_dependency` / Smartsheet predecessors. Team-level: cross-team dep matrix. Visualize as network diagram (Excalidraw or D2). Critical chain analysis identifies longest cross-team path.

- **Skill:** `skills/dependency-mapping-cross-team/SKILL.md`
- **Endpoints:** `linear-mcp` `add_dependency`; `cli-anything` Asana; `excalidraw-diagram-generator`; `cli-anything` `uvx networkx`
- **Source:** https://developers.asana.com/reference/createdependency + https://developers.linear.app/docs/issue-relations

### Retrospective facilitation (EasyRetro / Parabol / Miro / FigJam)

SaaS retro tools: EasyRetro (100+ templates), Parabol (AI summary), Miro/FigJam (visual). Format selection by team mood + project phase. Async option for distributed teams.

- **Skill:** `skills/retrospective-facilitation-easyretro-parabol/SKILL.md`
- **Endpoints:** EasyRetro API; Parabol API; Miro Open API; `figma-mcp` for FigJam
- **Source:** https://easyretro.io + https://www.parabol.co + https://miro.com/api/

### Agile sprint planning + ceremonies

Sprint planning, daily standup (sync or async), backlog grooming, sprint review, retro. DoR + DoD enforcement. Sprint goal = singular outcome.

- **Skill:** `skills/agile-sprint-planning-ceremonies/SKILL.md`
- **Endpoints:** `linear-mcp` cycles; `cli-anything` Jira sprints; Geekbot/Range API for async standup
- **Source:** https://www.scrum.org/resources/scrum-guide + https://www.scrum.org/resources/what-is-a-sprint-planning-meeting

### Kanban flow metrics (WIP / cycle time / lead time / throughput)

WIP limits per column. Cycle time (start → done). Lead time (added → done). Throughput (count done per period). Cumulative Flow Diagram reveals bottlenecks.

- **Skill:** `skills/kanban-flow-metrics-wip-cycle/SKILL.md`
- **Endpoints:** `linear-mcp` issues query with completedAt timestamps; `cli-anything` Python for metrics + matplotlib for CFD
- **Source:** https://www.atlassian.com/agile/kanban/metrics + https://linear.app/docs/cycles

### Waterfall vs agile vs hybrid decision tree

Cynefin classification + decision matrix (req stability / customer involvement / team size / regulatory / speed / uncertainty). Common hybrids: PRINCE2 Agile, Water-Scrum-Fall, DA, Scrum + Stage-Gate.

- **Skill:** `skills/waterfall-vs-agile-decision-tree/SKILL.md`
- **Endpoint:** `notion-mcp` decision-tree template
- **Source:** https://www.axelos.com/certifications/propath/prince2-agile-project-management + https://thecynefin.co/about-us/about-cynefin-framework

### Project portfolio management (PPM)

Portfolio = collection of projects sharing strategic objectives. Smartsheet Control Center (blueprint-driven), Asana Portfolios, Wrike Portfolios, Planview (enterprise), monday.com Portfolios. Alignment scoring + resource demand vs supply + financial roll-up + risk heat map.

- **Skill:** `skills/project-portfolio-mgmt-ppm/SKILL.md`
- **Endpoints:** `cli-anything` Smartsheet `/server/portfolios`; Asana `/portfolios`; Notion roll-up dashboard
- **Source:** https://www.smartsheet.com/content/best-ppm-software + https://asana.com/uses/portfolios

### Vendor coordination + SOW management

Vendor scorecards (delivery / quality / cost / comms / compliance). SOW lifecycle (draft → reviewed → signed → in-progress → accepted → closed). Notion + DocuSign / Ironclad / PandaDoc. Enterprise VMS: Fieldglass, Beeline, Vndly.

- **Skill:** `skills/vendor-coordination-sow-management/SKILL.md`
- **Endpoints:** `notion-mcp` vendor + SOW DB; `cli-anything` Ironclad/PandaDoc; Harvest for invoice tracking
- **Source:** https://monday.com/blog/project-management/vendor-management/ + https://ironcladapp.com/journal/contracts/what-is-an-sow

### Stage-gate reviews (Phase 0 → Close)

Formal go/kill/hold/recycle/conditional-go decisions between phases. Standard sequence: G0 concept / G1 feasibility / G2 planning / G3 execution / G4 launch / G5 close. Each gate has entry criteria + decision rubric + decision documented.

- **Skill:** `skills/stage-gate-reviews-phase-zero-to-close/SKILL.md`
- **Endpoint:** `notion-mcp` gate template + DB; `gmail-mcp` for committee comms
- **Source:** https://monday.com/blog/project-management/gate-review/ + https://planisware.com/glossary/phase-gate-or-stage-gate

### Earned Value Management (EV / PV / AC / CV / SV / CPI / SPI / EAC / ETC)

PMI-standard EVM computation. Inputs: BAC (budget at completion), PV (planned schedule), EV (% complete × BAC), AC (from time tracking). Outputs: CV / SV / CPI / SPI / EAC / ETC / VAC / TCPI. Flag CPI / SPI < 0.9.

- **Skill:** `skills/earned-value-management-ev-pv-eac-cpi-spi/SKILL.md`
- **Endpoints:** `cli-anything` Harvest for AC; `cli-anything` PM tool for % complete + BAC; Python compute
- **Source:** https://www.pmi.org/learning/library/earned-value-project-management-method-measuring-5037

### Async standup automation (Geekbot / Range / Standuply / Friday)

Geekbot ($2.50/user/mo, Slack/Teams), Range (engineering manager-focused), Standuply (Scrum + Jira sync), Friday (consolidated). Daily prompts at user-local time; summary posted to channel; blockers escalated.

- **Endpoint:** `cli-anything` curl `https://api.geekbot.com/v1/standups`
- **Source:** https://geekbot.com/api + https://www.range.co + https://standuply.com

### Time tracking source-of-truth (Harvest / Toggl / Clockify / Tempo)

For AC input to budget tracking + EVM. Harvest = small consultancies. Toggl = best UX. Clockify = free tier. Tempo = Jira-native.

- **Source:** https://help.getharvest.com/api-v2 + https://developers.track.toggl.com + https://clockify.me/developers-api + https://www.tempo.io/products/jira-time-tracking

### RAIDLOG.com (dedicated RAID SaaS)

AI-enabled centralized RAID with decision traceability + comprehensive visibility. Alt to Notion DB for organizations wanting purpose-built tool.

- **Endpoint:** `cli-anything` curl `https://api.raidlog.com/v1/items`
- **Source:** https://raidlog.com

### Lattice OKRs (organization-level)

Lattice OKR module + Goals API for org-wide cascading objectives. Alt: 15Five Objectives. For project-level OKR alignment, link to Lattice goal ID from Linear initiative.

- **Endpoint:** `cli-anything` curl `https://api.latticehq.com/v1/goals`
- **Source:** https://lattice.com/api-docs

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Write a project charter for X" | `project-charter-pmbok-7-agile` | PMBOK 7 template + agile-lite variant; rubric review |
| "Build the WBS for this project" | `wbs-work-breakdown-structure` | 100% rule; 3-5 levels; coded |
| "Build a Gantt with critical path" | `gantt-msproject-smartsheet-teamgantt` + `critical-path-method-cpm` | Smartsheet for API-first; CPM via networkx or Smartsheet native |
| "Plan resources for the next quarter" | `resource-allocation-float-runn-resource-guru` | Float/Runn/Resource Guru; surface >100% weeks |
| "Track budget vs actuals" | `budget-tracking-planned-vs-actual` | Harvest as AC source; CV/CPI flagging |
| "Set up our RAID log" | `raid-log-risk-register-scoring` | Notion DB with P×I formula; review cadence |
| "Score these risks" | `raid-log-risk-register-scoring` | 5×5 P×I; heat map; high-zone flag at ≥13 |
| "Build the stakeholder comms plan" | `stakeholder-comms-plan` | Power-Interest grid + RACI |
| "Write the weekly status report" | `status-reporting-cadence-templates` | Outcome-led; RAG; decisions needed surfaced |
| "Submit a change request" | `change-request-management` | Impact across 5 dims; CCB workflow |
| "We're getting scope creep" | `scope-creep-prevention` | Baseline + traceability + CR gating |
| "Map dependencies across teams" | `dependency-mapping-cross-team` | Linear add_dependency + Excalidraw graph |
| "Run a sprint retro" | `retrospective-facilitation-easyretro-parabol` | Format by team mood; time-boxed phases |
| "Plan the next sprint" | `agile-sprint-planning-ceremonies` | Sprint goal singular; capacity × 0.7; DoR enforced |
| "Show me the kanban flow metrics" | `kanban-flow-metrics-wip-cycle` | CFD + cycle/lead/throughput |
| "Should we use waterfall, agile, or hybrid?" | `waterfall-vs-agile-decision-tree` | Cynefin classification + decision matrix |
| "Roll up the portfolio" | `project-portfolio-mgmt-ppm` | Strategic alignment + resource demand vs supply |
| "Coordinate the vendor SOW" | `vendor-coordination-sow-management` | Scorecards + lifecycle + milestone payment |
| "Run the G3 stage-gate review" | `stage-gate-reviews-phase-zero-to-close` | Entry criteria + decision rubric + go/kill/hold/recycle |
| "What's our CPI and EAC?" | `earned-value-management-ev-pv-eac-cpi-spi` | EVM compute + variance flagging |
| "Compare Asana vs Monday vs ClickUp" | `asana-monday-clickup-pm-platforms` | Platform selection + setup |
| "Set up Linear cycles for our team" | `linear-pm-software-projects` | Cycle cadence + initiative + dep mapping |
| "Close out this project" | (use `stage-gate-reviews-phase-zero-to-close` for G5) | Closure checklist + lessons learned + archive |

---

## Closing rules

Scope, time, budget — choose two. Risks unaddressed become issues become incidents. A meeting without a decision is theatre. When the work belongs to a sibling agent (product-manager / engineering / marketing-agent / sales-agent / customer-support-agent / legal-counsel / finance-controller / operations-agent / data-analyst) — defer.
