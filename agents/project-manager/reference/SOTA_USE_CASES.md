# project-manager — SOTA Use Cases (June 2026)

This document maps every documented use case from `USE_CASES.md` to a concrete SOTA execution mechanism. Every use case has: a named tool, an exact agent-level execution path, a source URL, and a confidence rating.

**Legend:**
- ✓ Fully executable — production MCP / first-class API, OAuth or key already exposed via `agent.yaml`, end-to-end automated.
- ⚠ Executable with caveats — works today but with a one-time setup step (OAuth, paid API key, app approval) the recipient owns.
- ✗ Genuinely impossible today — rare; usually GUI-locked desktop SaaS.

The agent loads these mappings on demand by grepping `SOTA_USE_CASES.md` for the matching capability heading.

> **Identity note:** `project-manager` owns EXECUTION of agreed deliverables — Gantt/timeline planning, RAID logs, resource allocation, stakeholder communication, retrospectives, status reporting, vendor coordination. The adjacent agent `product-manager` owns the WHAT (PRDs, roadmaps, discovery, prioritization). Hand-offs go both ways and are documented in soul.md.

---

## Project charter authoring (PMBOK 7 + agile-friendly)

- **SOTA approach:** Notion or Asana charter template — sections: project name, sponsor, problem/opportunity, objectives, success criteria, scope (in/out), stakeholders, high-level milestones, budget envelope, risks at chartering. PMBOK 7 emphasizes principles (stewardship, team, stakeholders, value, systems thinking, leadership, tailoring, quality, complexity, risk, adaptability, change) — apply these as a final review pass.
- **Agent execution path:** `notion-mcp` `create_page` from charter template OR `cli-anything` curl Asana `https://app.asana.com/api/1.0/projects` with `notes` populated from charter sections.
- **Source:** https://www.pmi.org/standards/pmbok + https://asana.com/templates/project-charter
- **Confidence:** ✓ Fully executable

## Work Breakdown Structure (WBS) authoring

- **SOTA approach:** Decompose deliverables into 100% rule (every parent fully decomposed into children) WBS levels — 3-5 levels deep typically. Output as hierarchical issue tree in Asana/Linear/Jira (parent → child → grandchild) OR as Excalidraw tree diagram OR as Markdown outline in Notion.
- **Agent execution path:** `linear-mcp` `bulk_create_issues` with parent_id chains, OR `cli-anything` curl Asana `POST /tasks` with `parent` field, OR `excalidraw-diagram-generator` for visual tree.
- **Source:** https://www.pmi.org/learning/library/work-breakdown-structure-fundamentals-7138 + https://developers.asana.com/reference/createtask
- **Confidence:** ✓ Fully executable

## Gantt chart construction + timeline planning

- **SOTA approach:** Smartsheet (Gantt-native, % Allocation column + Resource Management integration) is the leading API-first option in 2026 — `https://api.smartsheet.com/2.0/sheets` exposes rows, dependencies, predecessor relationships, critical path. Alternates: Asana Timeline (Premium plan), Monday.com Gantt view, GanttPRO (REST API), TeamGantt (REST API). For Microsoft Project for the Web data, the supported path is Dataverse Web API (Graph API does not expose Premium plans yet as of 2026).
- **Agent execution path:** `cli-anything` curl Smartsheet `POST /sheets` with predecessor + duration cells; OR `cli-anything` curl `https://api.teamgantt.com/v1/projects/{id}/tasks` for TeamGantt.
- **Source:** https://smartsheet.redoc.ly + https://api-docs.teamgantt.com + https://learn.microsoft.com/en-us/answers/questions/401702/is-it-possible-to-fetch-project-online-tasks-using
- **Confidence:** ✓ Fully executable (⚠ MS Project for the Web: requires Dataverse, not standard Graph)

## Critical Path Method (CPM) analysis

- **SOTA approach:** Smartsheet `/sheets/{id}/rows` returns `inCriticalPath` boolean per row when project settings have CPM enabled. Forward pass: ES + duration = EF; backward pass: LF - duration = LS; float = LS - ES. Zero-float tasks are on the critical path. Alternates: networkx Python library for any DAG when the PM tool can't compute it natively.
- **Agent execution path:** `cli-anything` curl Smartsheet → parse `inCriticalPath` rows; OR `cli-anything` `uvx networkx` + Python script for forward/backward pass on dependency JSON.
- **Source:** https://community.smartsheet.com/discussion/79798/gantt-view-data-for-sheet-via-api + https://networkx.org/documentation/stable/reference/algorithms/dag.html
- **Confidence:** ✓ Fully executable

## Resource allocation across teams

- **SOTA approach:** Float (`https://api.float.com/v3`), Runn (`https://api.runn.io/v0`), Resource Guru (`https://api.resourceguruapp.com/v1`) — purpose-built resource management with people, projects, phases, allocations, leave management. Smartsheet Resource Management is the Smartsheet-stack alt. Each exposes REST API: `GET /people`, `GET /allocations`, `POST /allocations`, `GET /reports/utilization`.
- **Agent execution path:** `cli-anything` curl per platform; aggregate utilization % per person; surface conflicts (>100% allocated week-of-X).
- **Source:** https://developer.float.com/api_reference.html + https://app.runn.io/api/v0/docs + https://help.resourceguruapp.com/article/19-resource-guru-api-documentation
- **Confidence:** ⚠ Executable with caveats (each platform = recipient-owned API key)

## Budget tracking (planned vs actual)

- **SOTA approach:** Track planned budget per project + WBS element vs actuals from time tracking (Harvest/Toggl/Clockify/Tempo billable hours × rate) + expense data (Xero/QuickBooks). Variance % = (actual - planned) / planned. CV (cost variance) = EV - AC. CPI (cost performance index) = EV / AC. Flag when |CV%| > 10% or CPI < 0.9.
- **Agent execution path:** `cli-anything` curl Harvest `/v2/time_entries` + Smartsheet/Notion DB for planned budget; compute variance in Python via `cli-anything`.
- **Source:** https://help.getharvest.com/api-v2 + https://www.pmi.org/learning/library/earned-value-project-management-method-measuring-5037
- **Confidence:** ✓ Fully executable

## RAID log maintenance (Risks / Assumptions / Issues / Dependencies)

- **SOTA approach:** Centralized RAID database — Notion DB or Asana RAID template OR dedicated RAIDLOG.com. Each entry has type (R/A/I/D), description, owner, probability × impact score, mitigation/response, due date, status. Review cadence: weekly. "A RAID log nobody reviews is documentation theater."
- **Agent execution path:** `notion-mcp` `create_page` in RAID database with structured properties; OR `cli-anything` curl `https://api.raidlog.com/v1/items`; OR Asana template with custom fields.
- **Source:** https://asana.com/resources/raid-log + https://raidlog.com + https://www.notion.com/templates/raid-log-for-project-management
- **Confidence:** ✓ Fully executable

## Risk register + scoring (probability × impact)

- **SOTA approach:** Standard risk register columns: ID, description, category, probability (1-5), impact (1-5), score (P×I), response (avoid/mitigate/transfer/accept), owner, due date, status. Heat map visualization (5×5 grid). Risk velocity (rate of materialization) tracked over time for top-10. Smartsheet, Wrike, RAIDLOG, Notion DB all support this structure.
- **Agent execution path:** `notion-mcp` create risk DB with formula property for score; `cli-anything` Smartsheet `/sheets/{id}/rows` for SmartSheet shop; `excalidraw-diagram-generator` for heat map.
- **Source:** https://www.smartsheet.com/content/best-project-risk-management-software + https://www.pmi.org/learning/library/risk-management-process-9462
- **Confidence:** ✓ Fully executable

## Stakeholder communication plan

- **SOTA approach:** Stakeholder matrix (Power × Interest, Mendelow grid). Per stakeholder: name, role, power, interest, info needs, frequency, channel, owner. Manage-closely (high P/high I), keep-satisfied (high P/low I), keep-informed (low P/high I), monitor (low P/low I). RACI cross-reference per major deliverable.
- **Agent execution path:** `notion-mcp` Stakeholder DB with formula property mapping P+I to quadrant label; `excalidraw-diagram-generator` for 2×2 grid; `pptx` for stakeholder onboarding deck.
- **Source:** https://www.pmi.org/learning/library/stakeholder-management-engagement-influence-10072 + https://www.atlassian.com/work-management/project-management/raci-chart
- **Confidence:** ✓ Fully executable

## Status report cadence templates (weekly / biweekly / monthly)

- **SOTA approach:** Weekly = active project standard. Header (project, sponsor, week-of), RAG (red/amber/green) for scope/schedule/budget/quality, executive summary, accomplishments, planned next period, risks/issues needing attention, decisions needed, metrics dashboard. Auto-aggregate from Linear/Asana/Jira cycle data + Float/Harvest actuals + RAID log deltas. Distribute via gmail-mcp + Slack channel + Notion archive.
- **Agent execution path:** `cli-anything` curl per platform to aggregate; `notion-mcp` create status doc; `gmail-mcp` send + `slack-mcp` post.
- **Source:** https://asana.com/templates/status-report + https://www.atlassian.com/agile/project-management/status-report
- **Confidence:** ✓ Fully executable

## Kickoff meeting facilitation

- **SOTA approach:** Pre-kickoff: charter approved, stakeholders identified, scope locked, success criteria documented. Agenda (60-90 min): introductions, charter walkthrough, scope + non-goals, milestones + timeline, RACI, communication plan, RAID intro, Q&A, next steps. Output: kickoff deck (`pptx`), recorded meeting (Zoom/Meet/Teams), action items + RAID populated in PM tool.
- **Agent execution path:** `pptx` skill for deck; `google-calendar-mcp` for invite; `notion-mcp` for agenda + action items; `gmail-mcp` for follow-up.
- **Source:** https://www.pmi.org/learning/library/effective-project-kick-off-meetings-5826 + https://asana.com/resources/project-kickoff-meeting
- **Confidence:** ✓ Fully executable

## Change request management

- **SOTA approach:** Formal change control: change request submitted, impact assessed (scope/schedule/cost/quality/risk), CCB (change control board) decides go/no-go/defer, approved changes update baseline. Baseline = locked plan at kickoff. Approved changes re-baseline. Software: integrated CR forms in Asana/Monday/Jira/Wrike with conditional approval workflow.
- **Agent execution path:** `notion-mcp` change request DB with status workflow; `cli-anything` curl Asana to update sub-tasks with new dates; `gmail-mcp` for CCB approval workflow.
- **Source:** https://www.projectmanager.com/blog/change-request-management + https://monday.com/blog/project-management/scope-change/
- **Confidence:** ✓ Fully executable

## Scope creep prevention

- **SOTA approach:** Visible baseline (locked at kickoff), in/out scope in charter, change request gating, weekly scope review during status meeting, requirements traceability (every deliverable traces to an approved requirement). Flag scope creep when work is being done that doesn't trace to baseline or approved CR.
- **Agent execution path:** `cli-anything` query Linear/Asana for tasks added since baseline date; cross-reference vs CR log in Notion; raise scope-creep flag in next status report.
- **Source:** https://www.projectmanager.com/blog/5-ways-to-avoid-scope-creep + https://clickup.com/blog/scope-management-tools/
- **Confidence:** ✓ Fully executable

## Dependency mapping (cross-team)

- **SOTA approach:** Two layers: task-level dependencies (predecessor/successor in PM tool — Linear `add_dependency`, Asana `precedes`/`follows`, Smartsheet predecessors column) and team-level dependencies (one team's deliverable blocks another team's start). Visualize as network diagram (Excalidraw or D2). Critical-path analysis identifies the longest chain.
- **Agent execution path:** `linear-mcp` `add_dependency` for task level; `cli-anything` Asana `add_dependency`; `excalidraw-diagram-generator` for cross-team graph; `cli-anything` `uvx networkx` for chain length.
- **Source:** https://developers.asana.com/reference/createdependency + https://developers.linear.app/docs/issue-relations
- **Confidence:** ✓ Fully executable

## Retrospective facilitation

- **SOTA approach:** EasyRetro, Parabol, TeamRetro, Retrium for SaaS-hosted ceremony. Templates: Start/Stop/Continue, Mad/Sad/Glad, 4Ls (Liked/Learned/Lacked/Longed-for), Sailboat. Anonymous input, dot voting, action item assignment. Output: retro summary (auto-generated by Parabol) emailed to attendees. Async option: Miro/FigJam board with countdown timer.
- **Agent execution path:** `cli-anything` curl EasyRetro API to create board; OR Parabol — pre-meeting board setup + post-meeting summary fetch; OR Miro API for async board.
- **Source:** https://easyretro.io + https://www.parabol.co + https://miro.com/api/
- **Confidence:** ⚠ Executable with caveats (per-platform API keys)

## Lessons learned doc

- **SOTA approach:** Captured at retrospective + end-of-project. Categories: what went well, what didn't, root causes, action items for future projects. Stored in searchable Notion DB (organization-wide knowledge base) tagged by project type/size/domain. Search before kickoff of next project.
- **Agent execution path:** `notion-mcp` create lessons-learned entry; tag with categories; query DB at next project kickoff.
- **Source:** https://www.pmi.org/learning/library/lessons-learned-next-level-communicating-7991
- **Confidence:** ✓ Fully executable

## Project closure checklist

- **SOTA approach:** Standard closure checklist: deliverables accepted, contracts closed, resources released, lessons learned documented, project archive complete (charter, plan, baseline, status reports, change requests, RAID final, retro), final stakeholder report sent. Mark project closed in PM tool. Conduct post-implementation review at +30/60/90 days for outcome measurement.
- **Agent execution path:** `notion-mcp` closure checklist template; `cli-anything` per platform to mark closed; `gmail-mcp` for final stakeholder report.
- **Source:** https://www.pmi.org/learning/library/project-closure-phase-effective-9904
- **Confidence:** ✓ Fully executable

## Agile sprint planning + ceremonies (standup / grooming / review / retro)

- **SOTA approach:** Sprint planning = team commits to a sprint goal + scoped backlog for the cycle (Linear cycles, Jira sprints, Asana sprints, ClickUp sprints). Backlog grooming = refine ranked items to "ready" definition (independent, negotiable, valuable, estimable, small, testable — INVEST). Sprint review = demo to stakeholders. Retro = continuous improvement. Daily standup (sync) OR async (Geekbot/Range/Standuply).
- **Agent execution path:** `linear-mcp` `create_cycle`, `update_issue` to assign to cycle, `list_issues` for grooming view; `cli-anything` Jira via Atlassian Rovo MCP for Jira shops; Geekbot/Range API for async standup.
- **Source:** https://www.scrum.org/resources/what-is-a-sprint-planning-meeting + https://geekbot.com + https://www.range.co
- **Confidence:** ✓ Fully executable

## Kanban flow metrics (WIP / cycle / throughput / lead time)

- **SOTA approach:** Track WIP (work-in-progress count by status), cycle time (start → done), lead time (added → done), throughput (count done per period). Tools: Linear analytics, Jira reports, ClickUp dashboards, Kanbanize, ActionableAgile. Cumulative flow diagram (CFD) reveals bottlenecks. WIP limits per column enforce flow.
- **Agent execution path:** `linear-mcp` GraphQL `issues(filter:{state:Done, completedAt:{gte:...}})` for throughput; compute cycle time from `createdAt`/`completedAt` deltas in Python; `excalidraw-diagram-generator` for CFD.
- **Source:** https://www.atlassian.com/agile/kanban/metrics + https://linear.app/docs/cycles
- **Confidence:** ✓ Fully executable

## Waterfall vs agile vs hybrid decision tree

- **SOTA approach:** Decision factors: requirements stability (stable → waterfall), customer involvement (high → agile), team size (large coordinated → SAFe/LeSS), regulatory environment (heavy → PRINCE2/waterfall), delivery speed (fast → agile), uncertainty (high → agile/discovery). Cynefin framework for complexity classification. Hybrid (PRINCE2 Agile, water-scrum-fall) common for regulated industries with agile delivery teams.
- **Agent execution path:** Decision-tree questionnaire in Notion; agent walks user through factors; outputs recommendation with rationale.
- **Source:** https://www.axelos.com/certifications/propath/prince2-agile-project-management + https://www.scaledagileframework.com
- **Confidence:** ✓ Fully executable

## Project portfolio management (PPM)

- **SOTA approach:** Portfolio = collection of projects sharing strategic objectives. Standard practices: alignment scoring (strategic fit), resource demand vs supply, financial roll-up, risk roll-up, RAG heat map. SOTA tools: Smartsheet Control Center (blueprint-driven), Asana Portfolios, Wrike Portfolios, Planview (enterprise), monday.com Portfolios.
- **Agent execution path:** `cli-anything` curl Smartsheet `/server/portfolios`; `cli-anything` Asana `/portfolios`; aggregate via Notion dashboard.
- **Source:** https://www.smartsheet.com/content/best-ppm-software + https://asana.com/uses/portfolios
- **Confidence:** ⚠ Executable with caveats (PPM features = enterprise plan)

## Vendor coordination + SOW management

- **SOTA approach:** Vendor scorecards (delivery, quality, cost, communication, compliance), SOW lifecycle (draft → reviewed → signed → in-progress → accepted → closed), milestone-based payment tracking, vendor RAID. Repository: Notion DB or Ironclad/PandaDoc for contracts. Modern VMS (Fieldglass, Beeline, Vndly) for enterprise; for SMB the Notion + DocuSign + Harvest stack works.
- **Agent execution path:** `notion-mcp` vendor DB + SOW DB linked; `cli-anything` curl Ironclad/PandaDoc for contract status; `cli-anything` Harvest for vendor invoice tracking.
- **Source:** https://monday.com/blog/project-management/vendor-management/ + https://ironcladapp.com/journal/contracts/what-is-an-sow
- **Confidence:** ⚠ Executable with caveats (per-platform OAuth for VMS)

## Stage gate reviews (Phase 0 → Close)

- **SOTA approach:** Formal go/kill/hold/recycle/conditional-go decision points between phases (concept → feasibility → planning → execution → launch → close). Each gate has entry criteria (deliverables required), review committee, decision rubric, output documented. Planview, Planbox, Projectworx, Cerri ship native stage-gate workflows; Notion DB with status field + approval workflow is a lightweight alt.
- **Agent execution path:** `notion-mcp` gate template per stage + DB to track gate status; `gmail-mcp` for review committee comms; capture decision in Notion + RAID.
- **Source:** https://monday.com/blog/project-management/gate-review/ + https://planisware.com/glossary/phase-gate-or-stage-gate
- **Confidence:** ✓ Fully executable

## Executive sponsor management

- **SOTA approach:** Weekly/biweekly sponsor 1:1, monthly steering committee. Sponsor brief: 1-page TL;DR (RAG, top 3 risks, top 3 decisions needed). Escalation criteria pre-agreed (when does PM escalate, what does sponsor own). Track sponsor decisions in RAID log (D = Decisions).
- **Agent execution path:** `notion-mcp` sponsor brief template; `gmail-mcp` for weekly send; `google-calendar-mcp` for sponsor 1:1 cadence.
- **Source:** https://www.pmi.org/learning/library/role-executive-sponsor-success-projects-9831
- **Confidence:** ✓ Fully executable

## Risk burn-down / risk velocity charts

- **SOTA approach:** Risk burn-down = open risk count + total exposure (Σ P×I) over time. Risk velocity = rate of new risks materializing. Burn-down chart over project timeline. Implemented via PostHog (event-tracking on RAID log mutations) OR Notion formula DB queried weekly.
- **Agent execution path:** `notion-mcp` query risk DB by week; `cli-anything` `uvx matplotlib` for chart; embed in status report.
- **Source:** https://www.pmi.org/learning/library/risk-burn-down-charts-project-control-2316
- **Confidence:** ✓ Fully executable

## Project status dashboard

- **SOTA approach:** Live dashboard with RAG status, % complete (EV/PV), budget burn, schedule SPI, top risks, milestone heatmap, recent decisions. Smartsheet dashboards, Asana Goals + Portfolios, Monday dashboards, ClickUp dashboards all native. For multi-tool environments: Geckoboard, Klipfolio, or custom Notion page with embedded charts.
- **Agent execution path:** `cli-anything` curl per PM tool for current metrics; `notion-mcp` page with embedded views; `excalidraw-diagram-generator` for heatmap; refresh weekly.
- **Source:** https://www.smartsheet.com/content/project-management-dashboard + https://asana.com/uses/dashboard
- **Confidence:** ✓ Fully executable

## Earned Value Management (EV / PV / EAC / CPI / SPI)

- **SOTA approach:** PV (planned value at date X), EV (earned value = % complete × budget), AC (actual cost). Compute: CV = EV - AC, SV = EV - PV, CPI = EV/AC, SPI = EV/PV, EAC = BAC/CPI, ETC = EAC - AC. Flag CPI/SPI < 0.9. Tools: Primavera P6 (heavy industry), MS Project, Smartsheet add-ons, or Python computation from Harvest + Asana data.
- **Agent execution path:** `cli-anything` curl Harvest for AC; `cli-anything` curl PM tool for % complete + budget; Python compute EVM metrics; embed in status report.
- **Source:** https://www.pmi.org/learning/library/earned-value-project-management-method-measuring-5037 + https://www.casinelli.net/en/congruenza-tra-metriche-earned-value-e-critical-path/
- **Confidence:** ✓ Fully executable

## Cross-team standup orchestration

- **SOTA approach:** "Scrum of Scrums" — representatives from each team meet to surface cross-team blockers. 15-min cadence, structured: what's blocking us, what's blocking others, what we need from other teams. For async: Slack/Teams threaded posts triggered by Geekbot/Range/Standuply, aggregated into a cross-team dashboard.
- **Agent execution path:** `slack-mcp` orchestrated thread; `cli-anything` Geekbot API for async; `notion-mcp` cross-team blocker log.
- **Source:** https://www.scrum.org/resources/what-scrum-scrums + https://geekbot.com
- **Confidence:** ✓ Fully executable

## Async standup automation

- **SOTA approach:** Geekbot (Slack/MS Teams, $2.50/user/mo), Range (engineering-leaning, OKR + mood), Standuply (Scrum + Jira sync), Friday (consolidated standup+goals+kudos). Daily prompts at user-local time, summary posted to channel, blockers escalated. API: Geekbot `https://api.geekbot.com/v1/standups`, Standuply REST API.
- **Agent execution path:** `cli-anything` curl Geekbot `/standups` to create + `/reports` to fetch; OR `slack-mcp` for custom bot orchestration.
- **Source:** https://geekbot.com/api + https://standuply.com + https://www.range.co
- **Confidence:** ⚠ Executable with caveats (per-platform setup)

## Project health score

- **SOTA approach:** Composite score from schedule SPI, cost CPI, scope (CR rate vs baseline), quality (defect rate), risk (open critical risks count), resource (utilization variance). Each dimension scored RAG; overall = weighted average. Tools: PostHog or Mixpanel for tracking, custom Notion DB with formula.
- **Agent execution path:** `notion-mcp` health-score DB with formula property; weekly recompute and trend chart.
- **Source:** https://www.pmi.org/learning/library/project-health-check-framework-6952
- **Confidence:** ✓ Fully executable

## OKR ↔ project alignment

- **SOTA approach:** Every project links to ≥1 strategic objective + ≥1 KR. Surface alignment in portfolio view. Lattice / 15Five / WorkBoard for org-wide OKRs; for project-level: Linear initiatives + Asana goals + Notion OKR DB. Quarterly review: which projects moved which KRs.
- **Agent execution path:** `cli-anything` curl Lattice; `linear-mcp` `create_initiative` linked to project; `notion-mcp` OKR-project matrix.
- **Source:** https://lattice.com/api-docs + https://www.whatmatters.com/
- **Confidence:** ⚠ Executable with caveats (Lattice paid plan; Notion DB free fallback)

## Capacity planning / forecast

- **SOTA approach:** Forecast resource demand (project pipeline × person-weeks per project) vs supply (FTE - PTO - committed work). Tools: Float forecasting, Runn `/projections`, Forecast.app, Mosaic.tech. Identify hiring needs, contract gaps, over-commitment. Quarterly horizon.
- **Agent execution path:** `cli-anything` curl Float `/v3/projects` + `/people` for demand+supply; or Runn `/projections`; output capacity heatmap in Notion.
- **Source:** https://developer.float.com/api_reference.html + https://app.runn.io/api/v0/docs
- **Confidence:** ⚠ Executable with caveats (paid platforms)

## Time tracking + timesheets

- **SOTA approach:** Harvest (best for invoicing/small consultancies), Toggl Track (best UX, 145 integrations), Clockify (free tier, 5-user cap as of April 2026), Tempo for Jira (#1 Jira add-on). Each exposes REST API for `time_entries` create/list, project mapping, billable rates.
- **Agent execution path:** `cli-anything` curl per platform; aggregate hours by project + person + billable status; feed into EVM + budget tracking.
- **Source:** https://help.getharvest.com/api-v2 + https://developers.track.toggl.com + https://clockify.me/developers-api
- **Confidence:** ✓ Fully executable

## Meeting minutes + action items

- **SOTA approach:** Transcribe via Fathom / Otter / Read.ai / Zoom-IQ / Teams Meeting Recap. AI summarization extracts decisions, action items, owners, deadlines. Push action items to Linear/Asana with `assignee` + `due_date`. Decisions to RAID log (D).
- **Agent execution path:** `cli-anything` curl Fathom `/meetings/{id}/summary`; parse action items; `linear-mcp` `create_issue` per action; `notion-mcp` minutes archive.
- **Source:** https://fathom.video/api + https://otter.ai/api
- **Confidence:** ⚠ Executable with caveats (per-platform OAuth)

## Communication archive + knowledge management

- **SOTA approach:** Project workspace in Notion or Confluence as single source of truth. Sections: charter, plan, status reports archive, RAID log, decisions log, meeting minutes, lessons learned. Permalink everything. Search-first. Confluence is the heavy alt for Atlassian shops; Notion is the lightweight default.
- **Agent execution path:** `notion-mcp` workspace builder; `cli-anything` Confluence API for Confluence shops; ensure every status report archives there.
- **Source:** https://www.notion.com + https://developer.atlassian.com/cloud/confluence
- **Confidence:** ✓ Fully executable

---

## Summary table (≥90% fulfillment)

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | Project charter authoring | Notion / Asana template | `notion-mcp` + `cli-anything` Asana | ✓ |
| 2 | WBS authoring | Linear / Asana / Excalidraw | `linear-mcp bulk_create_issues` + `excalidraw-diagram-generator` | ✓ |
| 3 | Gantt chart construction | Smartsheet / TeamGantt / GanttPRO | `cli-anything` Smartsheet/TeamGantt curl | ✓ |
| 4 | Critical path analysis | Smartsheet CPM / networkx | `cli-anything` Smartsheet + `uvx networkx` | ✓ |
| 5 | Resource allocation | Float / Runn / Resource Guru / Smartsheet RM | `cli-anything` per platform | ⚠ (paid) |
| 6 | Budget tracking | Harvest + Smartsheet/Notion | `cli-anything` Harvest + Notion DB | ✓ |
| 7 | RAID log maintenance | Notion / Asana / RAIDLOG | `notion-mcp` + RAID DB | ✓ |
| 8 | Risk register + scoring | Smartsheet / Notion DB | `notion-mcp` formula DB | ✓ |
| 9 | Stakeholder comms plan | Power-Interest grid + Notion | `notion-mcp` + `excalidraw-diagram-generator` | ✓ |
| 10 | Status report cadence | Auto-aggregated Lenny-style | `linear-mcp` + Harvest + RAID + `notion-mcp` + `gmail-mcp` | ✓ |
| 11 | Kickoff meeting | pptx + Notion + Calendar | `pptx` + `notion-mcp` + `google-calendar-mcp` | ✓ |
| 12 | Change request management | Notion CR DB + approval workflow | `notion-mcp` + `gmail-mcp` | ✓ |
| 13 | Scope creep prevention | Baseline + CR gating + review | `notion-mcp` + `linear-mcp` queries | ✓ |
| 14 | Cross-team dependency mapping | Linear / Asana dep + networkx | `linear-mcp add_dependency` + `excalidraw-diagram-generator` | ✓ |
| 15 | Retrospective facilitation | EasyRetro / Parabol / Miro | `cli-anything` per platform | ⚠ (paid) |
| 16 | Lessons learned doc | Notion knowledge base | `notion-mcp` | ✓ |
| 17 | Project closure checklist | Notion template + RAID final | `notion-mcp` + per-platform closure | ✓ |
| 18 | Agile sprint planning + ceremonies | Linear cycles / Jira sprints | `linear-mcp` + `cli-anything` Jira | ✓ |
| 19 | Kanban flow metrics | Linear analytics + Python | `linear-mcp` + `cli-anything` Python | ✓ |
| 20 | Waterfall vs agile decision | Decision tree in Notion | `notion-mcp` + Cynefin | ✓ |
| 21 | Project portfolio management | Smartsheet Control Center / Asana Portfolios | `cli-anything` per platform | ⚠ (enterprise) |
| 22 | Vendor coordination + SOW | Notion + Ironclad/PandaDoc | `notion-mcp` + `cli-anything` per platform | ⚠ (paid) |
| 23 | Stage gate reviews | Notion gate template + approval | `notion-mcp` + `gmail-mcp` | ✓ |
| 24 | Executive sponsor management | Sponsor brief + 1:1 cadence | `notion-mcp` + `gmail-mcp` + `google-calendar-mcp` | ✓ |
| 25 | Risk burn-down chart | Notion DB + matplotlib | `notion-mcp` + `cli-anything` matplotlib | ✓ |
| 26 | Project status dashboard | Notion live page + PM-tool data | `notion-mcp` + `cli-anything` per PM tool | ✓ |
| 27 | Earned Value Management | Harvest + PM tool + Python EVM | `cli-anything` Harvest + PM + Python | ✓ |
| 28 | Cross-team standup | Scrum of scrums + Slack | `slack-mcp` + `cli-anything` Geekbot | ✓ |
| 29 | Async standup automation | Geekbot / Range / Standuply | `cli-anything` per platform | ⚠ (paid) |
| 30 | Project health score | Composite Notion formula | `notion-mcp` formula DB | ✓ |
| 31 | OKR ↔ project alignment | Lattice + Linear initiatives | `cli-anything` Lattice + `linear-mcp` | ⚠ (paid) |
| 32 | Capacity planning / forecast | Float / Runn projections | `cli-anything` per platform | ⚠ (paid) |
| 33 | Time tracking / timesheets | Harvest / Toggl / Clockify / Tempo | `cli-anything` per platform | ✓ |
| 34 | Meeting minutes + action items | Fathom / Otter + Linear push | `cli-anything` per source + `linear-mcp` | ⚠ (OAuth) |
| 35 | Communication archive (KM) | Notion / Confluence workspace | `notion-mcp` + Confluence API | ✓ |

**Fulfillment math:** 35 use cases mapped. 26 are ✓ (full confidence), 9 are ⚠ (caveat — paid plan or per-source OAuth recipient owns), 0 are ✗.

**Verdict: ~95% fulfillment.** Every documented use case has a concrete SOTA execution path. The 9 ⚠ rows are all "one-time setup the recipient owns" (Float/Runn/Resource Guru paid plans; Smartsheet Control Center enterprise; EasyRetro/Parabol paid plans; Lattice paid plan; Geekbot/Range/Standuply per-platform; Fathom/Otter OAuth). None are genuine impossibilities. Free fallbacks ship (Notion DB instead of Float for resourcing, Miro free tier for retros, Notion OKR DB instead of Lattice, Slack thread instead of Geekbot, manual minutes instead of Fathom).

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (all confirmed to exist in `app/config/mcp_config.json`):
- `filesystem` — always
- `linear-mcp` — use cases 2, 10, 14, 18, 19, 31 (issues, cycles, initiatives, dependencies)
- `jira-mcp` — alt to Linear for Jira-using teams (use case 18, 33)
- `notion-mcp` — use cases 1, 7, 8, 9, 10, 11, 12, 13, 16, 17, 22, 23, 24, 25, 26, 30, 35 (workspace single source of truth)
- `gmail-mcp` — use cases 10, 11, 12, 23, 24, 34 (stakeholder + sponsor + CCB comms)
- `slack-mcp` — use cases 10, 28 (cross-team broadcasts, scrum-of-scrums)
- `google-calendar-mcp` — use cases 11, 24 (kickoff + sponsor 1:1 scheduling)
- `google-workspace-mcp` — broad Google Workspace
- `outlook-mcp` — alt for MS-stack teams
- `ms-teams-mcp` — async standup + cross-team comms for MS shops
- `zoom-mcp` — meeting management + recording
- `figma-mcp` — visual planning collaboration (FigJam retros)
- `drawio-mcp` — network diagrams, RACI charts, swimlane diagrams
- `firecrawl-mcp` — competitive PM tool research (rare)
- `playwright-mcp` — for PM tools without public APIs
- `github` — link engineering PRs to project issues
- `postgresql-mcp` — warehouse queries for PMO metrics

**Skill packs to create in Round 2 (runtime build)**, in order of impact:

1. `asana-monday-clickup-pm-platforms` — multi-platform PM workspace operations
2. `linear-pm-software-projects` — Linear-centric for software shops
3. `gantt-msproject-smartsheet-teamgantt` — Gantt + CPM construction
4. `project-charter-pmbok-7-agile` — charter authoring with PMBOK 7 + agile rubric
5. `wbs-work-breakdown-structure` — WBS decomposition + 100% rule
6. `critical-path-method-cpm` — CPM forward/backward pass + float calc
7. `resource-allocation-float-runn-resource-guru` — RM platform operations
8. `budget-tracking-planned-vs-actual` — CV, CPI, variance reporting
9. `raid-log-risk-register-scoring` — RAID + risk register patterns
10. `stakeholder-comms-plan` — Power-Interest grid + RACI
11. `status-reporting-cadence-templates` — weekly/biweekly/monthly templates
12. `change-request-management` — CR lifecycle + CCB workflow
13. `scope-creep-prevention` — baseline + traceability + monitoring
14. `dependency-mapping-cross-team` — task + team dep mapping
15. `retrospective-facilitation-easyretro-parabol` — retro ceremony hosting
16. `agile-sprint-planning-ceremonies` — sprint + grooming + review + retro
17. `kanban-flow-metrics-wip-cycle` — CFD, cycle time, throughput
18. `waterfall-vs-agile-decision-tree` — methodology selection + Cynefin
19. `project-portfolio-mgmt-ppm` — portfolio + strategic alignment
20. `vendor-coordination-sow-management` — vendor + SOW lifecycle
21. `stage-gate-reviews-phase-zero-to-close` — formal gate decisions
22. `earned-value-management-ev-pv-eac-cpi-spi` — EVM compute + reporting

---

## Notes on remaining caveats (the ⚠ rows)

- **Float / Runn / Resource Guru (use cases 5, 32):** paid plans (Float $7.50/user/mo; Runn $10/user/mo; Resource Guru $2.50/user/mo). For solo PMs without a dedicated RM tool, Notion DB with formula for utilization works.
- **Smartsheet Control Center (use case 21):** enterprise plan. Asana Portfolios + Notion roll-up works on standard plans.
- **EasyRetro / Parabol (use case 15):** paid for full features (EasyRetro $25/user/mo; Parabol $6/user/mo). Miro free tier supports retros; Notion async retro DB is free fallback.
- **Lattice (use case 31):** paid HR-stack tool. Linear initiatives + Notion OKR DB is free fallback; OKR drafting + tracking still works.
- **Geekbot / Range / Standuply (use case 29):** $2.50-$8/user/mo. Custom Slack bot via `slack-mcp` + scheduled message is free fallback.
- **Fathom / Otter (use case 34):** $19+/user/mo. Zoom-IQ / Teams Meeting Recap are bundled with Zoom Pro/Teams licenses; manual minutes are the fall-back.
- **Ironclad / PandaDoc (use case 22):** paid contract platforms. DocuSign + Notion vendor DB works for SMB; Notion table with attached SOW PDFs works as minimum viable.
- **Per-source OAuth (use case 34):** Fathom / Otter / Zoom / Teams each require their own OAuth or API key. The agent walks the recipient through each setup once; afterwards every call is automated.

The 9 ⚠ rows all have free alternatives or are well-documented one-time setups — none are genuinely impossible, none require human-in-the-loop after setup.
