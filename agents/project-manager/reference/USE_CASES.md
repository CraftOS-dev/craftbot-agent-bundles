# Project Manager — Use Cases

**Tier:** **general** · **Category:** project-management
**Core job:** Cross-functional EXECUTION of agreed deliverables — project charter, WBS, Gantt + critical path, RAID log, resource allocation, budget tracking, status reports, stakeholder communications, change request control, sprint planning, retrospectives, stage-gate reviews, vendor coordination, EVM reporting, project closure.

> Ships with the SOTA project-management stack (Linear / Jira / Notion / Asana / Monday / ClickUp / Smartsheet / TeamGantt / Float / Runn / Resource Guru / Harvest / Toggl / Clockify / Tempo / EasyRetro / Parabol / Miro / Geekbot / RAIDLOG / Lattice via MCPs + `cli-anything` + curl). Executes end-to-end — drafts charters + writes them to Notion, files WBS as Linear/Asana issue tree, computes critical path, queries time tracking, generates status reports, runs retros, gates phases. Not just direct.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

> **Identity note:** `project-manager` owns DELIVERY of agreed work. The adjacent agent `product-manager` owns the WHAT (PRDs, roadmaps, discovery, prioritization). When asked to decide what to build, hand off. When asked to ship what's agreed — that's this agent.

---

## What this agent is supposed to do

### Charter + initiation
- Project charter authoring (PMBOK 7 + agile-lite variants)
- Sponsor + stakeholder identification
- Charter rubric review + sign-off
- Kickoff meeting facilitation
- Initial RAID population

### Planning
- Work Breakdown Structure (WBS) with dictionary (100% rule)
- Gantt chart construction (Smartsheet / TeamGantt / GanttPRO / MS Project)
- Critical Path Method (CPM) — forward/backward pass + float + crash + fast-track
- Resource allocation + capacity planning (Float / Runn / Resource Guru / Smartsheet RM)
- Budget breakdown + baseline lock
- Risk register at chartering with P×I scoring
- Methodology selection (waterfall / agile / hybrid via Cynefin classification)

### Execution + monitoring
- Status reports (weekly / biweekly / monthly / quarterly / sponsor brief)
- RAID log maintenance + risk review cadence
- Risk burn-down + risk velocity tracking
- Budget tracking (planned vs actual + variance)
- Earned Value Management (EV / PV / AC / CV / SV / CPI / SPI / EAC / ETC / TCPI)
- Schedule variance + critical-path slippage diagnostics
- Resource utilization monitoring (>100% week-of flags)
- Project health score (composite RAG)
- Project status dashboard

### Change + scope control
- Change request management (CR lifecycle + CCB workflow)
- Baseline updates after approved CRs
- Scope creep prevention + traceability monitoring
- Requirements vs delivered comparison

### Agile + flow ceremonies
- Sprint planning (Linear cycles / Jira sprints / Asana sprints)
- Sprint goal definition + capacity-bound commitment
- Backlog grooming + Definition of Ready enforcement
- Sprint review facilitation
- Retrospective facilitation (EasyRetro / Parabol / Miro / FigJam)
- Daily standup (sync or async via Geekbot / Range / Standuply)
- Cross-team scrum-of-scrums coordination
- Kanban flow metrics (WIP / cycle time / lead time / throughput / CFD)

### Stakeholder + comms
- Stakeholder mapping (Power-Interest grid)
- Communication plan + cadence per stakeholder tier
- RACI / DACI / DRI assignment
- Executive sponsor management + sponsor briefs
- Weekly / monthly / quarterly stakeholder updates
- Meeting minutes + action items (Fathom / Otter / Zoom / Teams transcription + action push to PM tool)

### Dependency + coordination
- Task-level dependency mapping (Linear `add_dependency`, Asana, Smartsheet predecessors)
- Cross-team dependency matrix
- Network diagram + critical-chain analysis
- Cross-team standup orchestration

### Stage gates + governance
- Stage-gate reviews (G0 concept / G1 feasibility / G2 planning / G3 execution / G4 launch / G5 close)
- Gate entry criteria checklists
- Go / Kill / Hold / Recycle / Conditional Go decision facilitation
- Gate decision documentation + communication

### Portfolio + program
- Project portfolio management (PPM) — Smartsheet Control Center / Asana Portfolios / Wrike / Planview
- Strategic alignment scoring
- Resource demand vs supply roll-up
- Financial roll-up + portfolio risk heat map
- OKR ↔ project alignment

### Vendor + SOW
- Vendor scorecards (delivery / quality / cost / comms / compliance)
- SOW lifecycle (draft → reviewed → signed → in-progress → accepted → closed)
- Milestone-based payment tracking
- Vendor RAID

### Time + cost
- Time tracking + timesheets (Harvest / Toggl / Clockify / Tempo)
- Billable hours aggregation
- Capacity planning / quarterly forecast
- Budget burn-down

### Closure + learning
- Project closure checklist
- Contracts closed + resources released
- Lessons learned documentation
- Project archive (charter / plans / baselines / status reports / RAID final / retros / CRs)
- Post-implementation review at +30/60/90 days
- Communication archive + knowledge management

### Async + automation
- Async standup automation (Geekbot / Range / Standuply / Friday)
- Status report auto-aggregation
- Cross-team blocker dashboard

---

## Execution status (SOTA — June 2026)

Every documented use case has a SOTA execution mechanism. Linear / Jira / Notion / Asana / Monday / ClickUp / Smartsheet cover the PM workspace surface; Float / Runn / Resource Guru cover resource management; Harvest / Toggl / Clockify / Tempo cover time tracking; EasyRetro / Parabol / Miro / FigJam cover retros; Geekbot / Range / Standuply cover async standup; RAIDLOG / Notion DB cover RAID; Lattice covers OKRs.

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Project charter authoring | PMBOK 7 + agile template in Notion | `notion-mcp` + template DB |
| Stakeholder identification | Power-Interest grid + Notion stakeholder DB | `notion-mcp` + `excalidraw-diagram-generator` |
| Kickoff meeting facilitation | Notion agenda + pptx deck + Calendar invite | `notion-mcp` + `pptx` + `google-calendar-mcp` |
| WBS authoring | Linear/Asana hierarchical issues + Excalidraw tree | `linear-mcp bulk_create_issues` + `excalidraw-diagram-generator` |
| Gantt chart construction | Smartsheet / TeamGantt / GanttPRO | `cli-anything` per platform |
| Critical Path Method analysis | Smartsheet `inCriticalPath` OR Python networkx | `cli-anything` Smartsheet OR `uvx networkx` |
| Resource allocation across teams | Float / Runn / Resource Guru / Smartsheet RM | `cli-anything` per platform |
| Budget breakdown + baseline | Notion DB + Smartsheet | `notion-mcp` + `cli-anything` Smartsheet |
| Methodology selection (waterfall/agile/hybrid) | Cynefin classification + decision matrix | `notion-mcp` decision tree |
| Status reports (weekly/biweekly/monthly) | Auto-aggregated Lenny-style + RAG | `linear-mcp` + Harvest + RAID + `notion-mcp` + `gmail-mcp` |
| RAID log maintenance | Notion DB / Asana RAID template / RAIDLOG.com | `notion-mcp` + RAID DB |
| Risk register + P×I scoring | 5×5 matrix in Notion DB with formula | `notion-mcp` formula DB |
| Risk burn-down + velocity charts | Notion query + matplotlib | `notion-mcp` + `cli-anything` matplotlib |
| Budget tracking (planned vs actual) | Harvest AC + WBS planned + Python variance | `cli-anything` Harvest + Python |
| Earned Value Management | Harvest AC + PM tool % complete + Python EVM | `cli-anything` Harvest + PM + Python |
| Change request management | Notion CR DB + CCB approval workflow | `notion-mcp` + `gmail-mcp` |
| Scope creep prevention | Baseline + traceability + CR gating | `notion-mcp` + `linear-mcp` queries |
| Cross-team dependency mapping | Linear `add_dependency` + Asana + Excalidraw graph | `linear-mcp` + `excalidraw-diagram-generator` + `uvx networkx` |
| Sprint planning | Linear cycles / Jira sprints / Asana | `linear-mcp` + `cli-anything` Jira/Asana |
| Backlog grooming | Linear/Jira filter views + DoR checklist | `linear-mcp` query + Notion DoR template |
| Sprint review | Linear cycle report + Notion review doc + deck | `linear-mcp` + `notion-mcp` + `pptx` |
| Retrospective facilitation | EasyRetro / Parabol / Miro / FigJam | `cli-anything` per platform + `figma-mcp` for FigJam |
| Daily standup (sync) | Slack/Teams thread orchestration | `slack-mcp` / `ms-teams-mcp` |
| Daily standup (async) | Geekbot / Range / Standuply | `cli-anything` per platform |
| Kanban flow metrics (WIP/cycle/lead/throughput) | Linear analytics + Python | `linear-mcp` + `cli-anything` Python + matplotlib |
| Cumulative Flow Diagram (CFD) | Linear data + matplotlib | `linear-mcp` + `cli-anything` Python |
| Stakeholder comms plan | Power-Interest grid + comms cadence matrix | `notion-mcp` + `excalidraw-diagram-generator` |
| RACI matrix | Notion DB + per-deliverable rows | `notion-mcp` |
| Executive sponsor management | Sponsor 1-page brief + weekly 1:1 cadence | `notion-mcp` + `gmail-mcp` + `google-calendar-mcp` |
| Cross-team standup (scrum of scrums) | Slack/Teams thread + cross-team blocker log | `slack-mcp` + `notion-mcp` |
| Meeting minutes + action items | Fathom / Otter / Zoom-IQ / Teams Recap + action push | `cli-anything` per source + `linear-mcp create_issue` |
| Stage-gate reviews | Notion gate template + decision rubric | `notion-mcp` + `gmail-mcp` |
| Project portfolio management | Smartsheet Control Center / Asana Portfolios / Notion roll-up | `cli-anything` per platform + `notion-mcp` |
| OKR ↔ project alignment | Lattice + Linear initiatives + Notion OKR DB | `cli-anything` Lattice + `linear-mcp` |
| Vendor coordination + SOW management | Notion vendor + SOW DB + Ironclad/PandaDoc | `notion-mcp` + `cli-anything` per platform |
| Time tracking source-of-truth | Harvest / Toggl / Clockify / Tempo | `cli-anything` per platform |
| Capacity planning / forecast | Float / Runn projections | `cli-anything` per platform |
| Project health score (composite) | Notion DB + formula property | `notion-mcp` formula DB |
| Project status dashboard | Notion live page + embedded charts | `notion-mcp` + per-PM-tool curl |
| Project closure checklist | Notion template + per-platform closure marks | `notion-mcp` + `cli-anything` per platform |
| Lessons learned documentation | Notion knowledge base with category tagging | `notion-mcp` |
| Communication archive (knowledge mgmt) | Notion or Confluence workspace | `notion-mcp` + `cli-anything` Confluence |

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Float / Runn / Resource Guru (resource allocation, capacity forecast) | ⚠ | Paid plans ($2.50–$10/user/mo); Notion DB with utilization formula is free fallback |
| Smartsheet Control Center (PPM) | ⚠ | Enterprise plan; Asana Portfolios + Notion roll-up works on standard plans |
| EasyRetro / Parabol (managed retros) | ⚠ | Paid for full features; Miro free tier + Notion async retro DB are free fallbacks |
| Lattice (OKR module) | ⚠ | Paid HR-stack tool; Notion OKR DB + Linear initiatives is free fallback |
| Geekbot / Range / Standuply (async standup) | ⚠ | $2.50–$8/user/mo; custom Slack bot via `slack-mcp` + scheduled posts is free fallback |
| Fathom / Otter (meeting minutes) | ⚠ | $19+/user/mo; Zoom-IQ / Teams Recap bundled with paid Zoom/Teams; manual minutes is fallback |
| Ironclad / PandaDoc (SOW contracts) | ⚠ | Paid platforms; Notion vendor DB + DocuSign works for SMB |
| MS Project for the Web (Premium plans) | ⚠ | Data access requires Dataverse Web API, not standard Graph API as of June 2026 |
| Per-source OAuth (Fathom / Otter / Zoom / Teams / Atlassian / each PM platform) | ⚠ | Each requires one-time OAuth or API key; afterwards fully automated |
| RAIDLOG.com (dedicated RAID SaaS) | ⚠ | Optional; Notion DB with formula is the default and ships free |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a concrete execution path. The ⚠ rows are all paid SaaS the recipient owns (or free alternatives ship by default). No use case is genuinely impossible.

---

## When to use this agent

- "Write a project charter for the warehouse migration"
- "Build the WBS for our Q3 platform replatform"
- "Compute the critical path for the launch program and flag zero-float tasks"
- "Plan resources across the eng + design + QA teams for next quarter"
- "Generate the weekly status report for the steering committee"
- "Set up our RAID log and score the top-10 risks"
- "Run the sprint retro for Sprint 14 and push action items to Linear"
- "We're getting scope creep on the API integration — help us regain control"
- "Map cross-team dependencies for the Q4 launch + identify the critical chain"
- "Run the G2 stage-gate review for the planning phase"
- "What's our CPI and EAC vs the $400k budget?"
- "Close out the data-migration project — checklist, lessons learned, archive"
- "Schedule and facilitate the program kickoff for 12 cross-functional stakeholders"
- "Should we use waterfall, agile, or hybrid for this regulated rollout?"
- "Submit a change request for the +2 week schedule extension"

## When NOT to use this agent

- Deciding WHAT to build (PRDs, roadmaps, discovery, prioritization frameworks for product backlog) — hand off to `product-manager`
- Engineering scoping / architecture / technical RFCs / code review — hand off to `senior-python-engineer` / `frontend-engineer` / `devops-engineer`
- GTM positioning / launch campaign / messaging / marketing content — hand off to `marketing-agent`
- Sales pipeline analysis / objection prep / sales enablement collateral — hand off to `sales-agent`
- Support theme synthesis / churn driver investigation / help-center content — hand off to `customer-support-agent`
- Vendor MSA / SOW legal review + redline — draft, but hand off to `legal-counsel` for legal sign-off
- Project cost reporting at company P&L / accounting integration — hand off to `finance-controller`
- HR / talent / vendor onboarding ops at company scale — hand off to `operations-agent` (v1 — until then, defer to `legal-counsel` for vendor contracts)
- Deep warehouse SQL or attribution modeling for PMO analytics — hand off to `data-analyst`
- Writing technical product documentation (API docs, developer guides) — hand off to `technical-writer`
- SEO / content marketing for project launch site — hand off to `seo-specialist` or `marketing-agent`
- Email marketing for project launches — hand off to `email-strategist`
- Building / shipping video assets for project demos — hand off to `video-creator`
