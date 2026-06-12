# Project Manager — Source Attribution

Section-to-source map for `soul.md` and `role.md`. **Not** loaded into context — for human verification.

URLs in `agent.yaml → sources` and `reference/INVENTORY.md`. Per-use-case mapping in `reference/SOTA_USE_CASES.md`.

---

## soul.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Title + persona intro + three convictions | Composition synthesis from PMBOK 7 (PMI), PRINCE2 (AXELOS), Agile Manifesto, classic PM canon — "scope-time-budget triangle" is canonical PM truism; "risks unaddressed become issues" reflects PMBOK 7 risk performance domain; "meeting without a decision is theatre" is industry idiom across Lenny Rachitsky / Marty Cagan / Reforge PM canon | Triad framing is composed |
| Purpose | Synthesis from PMBOK 7 + PRINCE2 + Scrum Guide + Lenny Rachitsky weekly update format | |
| Execution stack | `reference/SOTA_USE_CASES.md` | Every bullet maps to a row in the SOTA table |
| When invoked — Kickoff mode | PMBOK 7 charter + Asana kickoff template | https://www.pmi.org/standards/pmbok + https://asana.com/templates/project-kickoff-meeting |
| When invoked — Planning mode | PMBOK 7 planning performance domain + PRINCE2 Plans theme + CPM canon | https://www.pmi.org/standards/pmbok + https://instituteprojectmanagement.com/blog/critical-path-method/ |
| When invoked — Status reporting mode | Lenny Rachitsky weekly update format + Atlassian status report template | https://www.lennysnewsletter.com/p/how-to-write-a-great-weekly-update + https://www.atlassian.com/agile/project-management/status-report |
| When invoked — RAID review mode | PMBOK 7 risk performance domain + Asana RAID + RAIDLOG.com canon | https://asana.com/resources/raid-log + https://raidlog.com |
| When invoked — Change request mode | PMBOK 7 change-control + PRINCE2 change theme | https://www.projectmanager.com/blog/change-request-management |
| When invoked — Sprint planning mode | Scrum Guide + Linear cycles + DoR/DoD canon | https://www.scrum.org/resources/scrum-guide + https://linear.app/docs/cycles |
| When invoked — Retrospective mode | EasyRetro + Parabol + Atlassian retro guide canon | https://easyretro.io + https://www.parabol.co |
| When invoked — Stage-gate mode | Cooper stage-gate canon + Planview gate review templates | https://planisware.com/glossary/phase-gate-or-stage-gate + https://monday.com/blog/project-management/gate-review/ |
| When invoked — Project closure mode | PMBOK 7 closure performance domain + PRINCE2 Closing a Project process | https://www.pmi.org/learning/library/project-closure-phase-effective-9904 |
| Core operating rules | Merged: PMBOK 7 principles (12) + PRINCE2 principles (7) + Scrum Guide + Cynefin + classic PM canon (scope-time-budget triangle, RAG honest, baseline lock) | |
| Mode-specific decisions | Per-mode lift from matching reference (PMBOK / PRINCE2 / Scrum / Cooper / Lenny / Asana / Atlassian) | |
| Quality gates | Synthesis from PMBOK 7 quality performance domain + PRINCE2 quality theme + agile DoR/DoD | |
| Output format | Standard PM artifact conventions — Notion + Linear/Asana/Jira/Smartsheet native formats | |
| Communication style | Lenny Rachitsky "writing for execs" + Cagan SVPG "outcome-led communication" + PMBOK 7 stakeholder engagement | |
| When to push back | Synthesis from PMBOK 7 + PRINCE2 + Scrum Guide anti-patterns + industry canon | |
| When to defer | Synthesis of CraftBot agent catalog (product-manager, sales-agent, marketing-agent, customer-support-agent, senior-python-engineer, frontend-engineer, devops-engineer, legal-counsel, finance-controller, data-analyst) responsibility boundaries | |
| First-conversation routine questions | Standard PROACTIVE.md self-init pattern from `METHODOLOGY.md` with PM-specific routine questions | Same wording mechanic across all CraftBot agents |
| Closing rule | Distilled from PMBOK 7 + PRINCE2 + Cagan SVPG closing principles | |

---

## role.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Capability reference → PM artifact types | Industry canon (PMI / AXELOS / Scrum.org); standard PM catalog | |
| Capability reference → Prioritization frameworks | Intercom RICE + ProductPlan MoSCoW + SAFe WSJF canon | https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers |
| Capability reference → Methodologies (PMBOK 7, PRINCE2, Scrum, Kanban, SAFe, LeSS, Nexus, CPM, CCPM, EVM, Stage-Gate, Waterfall, Water-Scrum-Fall, Cynefin, Spiral) | PMI + AXELOS + Scrum.org + SAFe + LeSS + Nexus + Goldratt + Cooper + Snowden canon | https://www.pmi.org/standards/pmbok + https://www.axelos.com + https://www.scrum.org + https://www.scaledagileframework.com + https://less.works + https://thecynefin.co |
| Capability reference → Responsibility assignment (RACI/DACI/DRI/CAIRO/PARIS) | Atlassian RACI + Apple DRI canon + DACI (Atlassian) | https://www.atlassian.com/work-management/project-management/raci-chart |
| Capability reference → Risk response strategies | PMBOK 7 risk performance domain | https://www.pmi.org/learning/library/risk-management-process-9462 |
| Capability reference → Schedule compression (fast-track, crash) | PMBOK 7 schedule performance domain + CPM canon | https://instituteprojectmanagement.com/blog/critical-path-method/ |
| Capability reference → Estimation (PERT, story points, t-shirt, Wideband Delphi, analogous, parametric, bottom-up) | PMI estimation canon + Mike Cohn agile estimating + Wideband Delphi | https://www.mountaingoatsoftware.com/blog |
| Capability reference → Time tracking source-of-truth tools | Harvest / Toggl / Clockify / Tempo / Everhour / Timely | https://help.getharvest.com/api-v2 + https://developers.track.toggl.com + https://clockify.me/developers-api + https://www.tempo.io |
| Capability reference → Resource management source-of-truth tools | Float / Runn / Resource Guru / Smartsheet RM canon | https://developer.float.com/api_reference.html + https://app.runn.io/api/v0/docs + https://help.resourceguruapp.com |
| Capability reference → Adjacent specialist tool surfaces | CraftBot agent catalog | |
| Charter playbook (PMBOK 7 + agile + rubric) | PMBOK 7 + Asana project charter template + PRINCE2 PID equivalent | https://www.pmi.org/standards/pmbok + https://asana.com/templates/project-charter |
| WBS playbook (100% rule + dictionary + Markdown outline) | PMI Practice Standard for Work Breakdown Structures | https://www.pmi.org/learning/library/work-breakdown-structure-fundamentals-7138 |
| Gantt playbook (construction + dependency types FS/SS/FF/SF + slip diagnostics) | PMI scheduling canon + Smartsheet / TeamGantt docs | https://smartsheet.redoc.ly + https://api-docs.teamgantt.com |
| Critical path playbook (forward/backward pass + float + networkx Python) | CPM canon + networkx docs | https://instituteprojectmanagement.com/blog/critical-path-method/ + https://networkx.org |
| Resource allocation playbook (Float allocation API + over-allocation handling + capacity = FTE × hours × focus factor) | Float docs + agile capacity calculation canon | https://developer.float.com/api_reference.html |
| Budget tracking playbook (CV/SV/CPI/SPI/EAC/ETC/TCPI + report structure) | PMI EVM canon | https://www.pmi.org/learning/library/earned-value-project-management-method-measuring-5037 |
| RAID log playbook (R/A/I/D structure + 5×5 P×I + review cadence + DB template) | Asana RAID guide + RAIDLOG canon + Notion templates | https://asana.com/resources/raid-log + https://raidlog.com + https://www.notion.com/templates/raid-log-for-project-management |
| Risk register playbook (categories + burn-down + velocity) | PMI risk performance domain | https://www.pmi.org/learning/library/risk-burn-down-charts-project-control-2316 |
| Stakeholder comms playbook (Power-Interest grid + comms plan + RACI) | Mendelow Power-Interest grid + PMI stakeholder engagement + Atlassian RACI | https://www.pmi.org/learning/library/stakeholder-management-engagement-influence-10072 + https://www.atlassian.com/work-management/project-management/raci-chart |
| Status report playbook (weekly template + monthly/quarterly variants) | Lenny Rachitsky weekly update + Asana status report template + Atlassian guide | https://www.lennysnewsletter.com/p/how-to-write-a-great-weekly-update + https://asana.com/templates/status-report |
| Change request playbook (CR lifecycle + CCB + template) | PMBOK 7 integrated change control + PRINCE2 change theme | https://www.projectmanager.com/blog/change-request-management |
| Sprint planning playbook (procedure + DoR + DoD + template) | Scrum Guide + Mike Cohn Agile Estimating and Planning + DoR/DoD canon | https://www.scrum.org/resources/scrum-guide + https://www.mountaingoatsoftware.com |
| Retrospective playbook (format selection + time-box + summary template) | EasyRetro / Parabol / Retrium canon + Esther Derby & Diana Larsen "Agile Retrospectives" | https://easyretro.io + https://www.parabol.co |
| Stage-gate playbook (G0-G5 sequence + Cooper outcomes + template) | Cooper stage-gate canon + Planview gate review templates | https://planisware.com/glossary/phase-gate-or-stage-gate + https://monday.com/blog/project-management/gate-review/ |
| Closure playbook (checklist + lessons learned categories) | PMBOK 7 closure performance domain + PRINCE2 Closing a Project + PMI lessons-learned canon | https://www.pmi.org/learning/library/project-closure-phase-effective-9904 + https://www.pmi.org/learning/library/lessons-learned-next-level-communicating-7991 |
| EVM playbook (glossary + formulas + interpretation + report section) | PMI EVM canon | https://www.pmi.org/learning/library/earned-value-project-management-method-measuring-5037 + https://www.casinelli.net/en/congruenza-tra-metriche-earned-value-e-critical-path/ |
| Methodology selection playbook (Cynefin + decision matrix + hybrids) | Snowden Cynefin + PRINCE2 Agile + Water-Scrum-Fall canon | https://thecynefin.co/about-us/about-cynefin-framework + https://www.axelos.com/certifications/propath/prince2-agile-project-management |
| Antipattern catalog (12 BAD/GOOD pairs) | Synthesis from PMBOK 7 + PRINCE2 + Scrum Guide + Cooper + Lenny + industry idioms | |
| SOTA tool reference (per-tool entries: Asana/Monday/ClickUp/Wrike, Linear, Smartsheet/TeamGantt/MSProject, Charter, WBS, CPM, Float/Runn/RG, Budget tracking, RAID, Stakeholder comms, Status reports, CR, Scope creep, Dep mapping, Retro, Sprint + ceremonies, Kanban metrics, Waterfall/agile decision, PPM, Vendor + SOW, Stage-gate, EVM, Async standup, Time tracking, RAIDLOG, Lattice) | Per-tool sources cited inline; see SOTA tool sources table below | See SOTA tool sources table |
| SOTA execution playbook (request → skill pack) | Generated from `reference/SOTA_USE_CASES.md` | |

---

## SOTA tool sources (June 2026)

| Tool | Source URL | Used for |
|---|---|---|
| Asana Official MCP Server v2 | https://developers.asana.com/docs/mcp-server | `skills/asana-monday-clickup-pm-platforms/SKILL.md` |
| Monday.com MCP | https://developer.monday.com/apps/docs/monday-apps-mcp | `skills/asana-monday-clickup-pm-platforms/SKILL.md` |
| ClickUp MCP Server | https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server | `skills/asana-monday-clickup-pm-platforms/SKILL.md` |
| Wrike API | https://developers.wrike.com | `skills/asana-monday-clickup-pm-platforms/SKILL.md` |
| Linear API + MCP | https://developers.linear.app | `skills/linear-pm-software-projects/SKILL.md` |
| Atlassian Rovo MCP (Jira + Confluence) | https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/ | Jira/Confluence integration |
| Smartsheet API | https://smartsheet.redoc.ly | `skills/gantt-msproject-smartsheet-teamgantt/SKILL.md` + critical path |
| TeamGantt API | https://api-docs.teamgantt.com | `skills/gantt-msproject-smartsheet-teamgantt/SKILL.md` |
| MS Project for the Web (Dataverse) | https://learn.microsoft.com/en-us/answers/questions/401702/is-it-possible-to-fetch-project-online-tasks-using | `skills/gantt-msproject-smartsheet-teamgantt/SKILL.md` MS-stack path |
| Notion MCP | https://developers.notion.com/docs/mcp | Charter, RAID, status, knowledge base across all skills |
| PMBOK 7 (PMI) | https://www.pmi.org/standards/pmbok | `skills/project-charter-pmbok-7-agile/SKILL.md` + many playbooks |
| PRINCE2 (AXELOS) | https://www.axelos.com/certifications/propath/prince2-project-management | `skills/project-charter-pmbok-7-agile/SKILL.md` |
| WBS canon (PMI) | https://www.pmi.org/learning/library/work-breakdown-structure-fundamentals-7138 | `skills/wbs-work-breakdown-structure/SKILL.md` |
| CPM canon | https://instituteprojectmanagement.com/blog/critical-path-method/ | `skills/critical-path-method-cpm/SKILL.md` |
| networkx (Python DAG) | https://networkx.org/documentation/stable/reference/algorithms/dag.html | `skills/critical-path-method-cpm/SKILL.md` |
| Float API | https://developer.float.com/api_reference.html | `skills/resource-allocation-float-runn-resource-guru/SKILL.md` |
| Runn API | https://app.runn.io/api/v0/docs | `skills/resource-allocation-float-runn-resource-guru/SKILL.md` |
| Resource Guru API | https://help.resourceguruapp.com/article/19-resource-guru-api-documentation | `skills/resource-allocation-float-runn-resource-guru/SKILL.md` |
| Harvest API v2 | https://help.getharvest.com/api-v2 | `skills/budget-tracking-planned-vs-actual/SKILL.md` + EVM |
| Toggl Track API | https://developers.track.toggl.com | `skills/budget-tracking-planned-vs-actual/SKILL.md` |
| Clockify API | https://clockify.me/developers-api | `skills/budget-tracking-planned-vs-actual/SKILL.md` |
| Tempo for Jira | https://www.tempo.io/products/jira-time-tracking | Jira-shop time tracking |
| EVM canon (PMI) | https://www.pmi.org/learning/library/earned-value-project-management-method-measuring-5037 | `skills/earned-value-management-ev-pv-eac-cpi-spi/SKILL.md` |
| EVM-CPM integration | https://www.casinelli.net/en/congruenza-tra-metriche-earned-value-e-critical-path/ | EVM + CPM synergy |
| Asana RAID guide | https://asana.com/resources/raid-log | `skills/raid-log-risk-register-scoring/SKILL.md` |
| RAIDLOG.com | https://raidlog.com | `skills/raid-log-risk-register-scoring/SKILL.md` |
| Notion RAID template | https://www.notion.com/templates/raid-log-for-project-management | `skills/raid-log-risk-register-scoring/SKILL.md` |
| Risk burn-down (PMI) | https://www.pmi.org/learning/library/risk-burn-down-charts-project-control-2316 | `skills/raid-log-risk-register-scoring/SKILL.md` |
| Mendelow Power-Interest grid (PMI) | https://www.pmi.org/learning/library/stakeholder-management-engagement-influence-10072 | `skills/stakeholder-comms-plan/SKILL.md` |
| Atlassian RACI | https://www.atlassian.com/work-management/project-management/raci-chart | `skills/stakeholder-comms-plan/SKILL.md` |
| Asana status report template | https://asana.com/templates/status-report | `skills/status-reporting-cadence-templates/SKILL.md` |
| Atlassian status report guide | https://www.atlassian.com/agile/project-management/status-report | `skills/status-reporting-cadence-templates/SKILL.md` |
| Lenny Rachitsky weekly update | https://www.lennysnewsletter.com/p/how-to-write-a-great-weekly-update | `skills/status-reporting-cadence-templates/SKILL.md` |
| Change request management (ProjectManager) | https://www.projectmanager.com/blog/change-request-management | `skills/change-request-management/SKILL.md` |
| Scope creep (ProjectManager) | https://www.projectmanager.com/blog/5-ways-to-avoid-scope-creep | `skills/scope-creep-prevention/SKILL.md` |
| Asana dependencies API | https://developers.asana.com/reference/createdependency | `skills/dependency-mapping-cross-team/SKILL.md` |
| Linear issue relations | https://developers.linear.app/docs/issue-relations | `skills/dependency-mapping-cross-team/SKILL.md` |
| EasyRetro | https://easyretro.io | `skills/retrospective-facilitation-easyretro-parabol/SKILL.md` |
| Parabol | https://www.parabol.co | `skills/retrospective-facilitation-easyretro-parabol/SKILL.md` |
| Miro Open API | https://miro.com/api/ | `skills/retrospective-facilitation-easyretro-parabol/SKILL.md` |
| Scrum Guide (scrum.org) | https://www.scrum.org/resources/scrum-guide | `skills/agile-sprint-planning-ceremonies/SKILL.md` |
| Sprint planning guide (scrum.org) | https://www.scrum.org/resources/what-is-a-sprint-planning-meeting | `skills/agile-sprint-planning-ceremonies/SKILL.md` |
| Linear cycles | https://linear.app/docs/cycles | `skills/agile-sprint-planning-ceremonies/SKILL.md` + kanban metrics |
| Atlassian kanban metrics | https://www.atlassian.com/agile/kanban/metrics | `skills/kanban-flow-metrics-wip-cycle/SKILL.md` |
| Cynefin framework | https://thecynefin.co/about-us/about-cynefin-framework | `skills/waterfall-vs-agile-decision-tree/SKILL.md` |
| PRINCE2 Agile | https://www.axelos.com/certifications/propath/prince2-agile-project-management | `skills/waterfall-vs-agile-decision-tree/SKILL.md` |
| SAFe | https://www.scaledagileframework.com | Methodology selection |
| Smartsheet PPM | https://www.smartsheet.com/content/best-ppm-software | `skills/project-portfolio-mgmt-ppm/SKILL.md` |
| Asana Portfolios | https://asana.com/uses/portfolios | `skills/project-portfolio-mgmt-ppm/SKILL.md` |
| Monday.com vendor management | https://monday.com/blog/project-management/vendor-management/ | `skills/vendor-coordination-sow-management/SKILL.md` |
| Ironclad SOW | https://ironcladapp.com/journal/contracts/what-is-an-sow | `skills/vendor-coordination-sow-management/SKILL.md` |
| Cooper stage-gate (Planview) | https://planisware.com/glossary/phase-gate-or-stage-gate | `skills/stage-gate-reviews-phase-zero-to-close/SKILL.md` |
| Monday stage-gate guide | https://monday.com/blog/project-management/gate-review/ | `skills/stage-gate-reviews-phase-zero-to-close/SKILL.md` |
| Geekbot API (async standup) | https://geekbot.com/api | Async standup tool entry |
| Range (async standup) | https://www.range.co | Async standup tool entry |
| Standuply | https://standuply.com | Async standup tool entry |
| Lattice Goals API | https://lattice.com/api-docs | OKR ↔ project alignment |
| PMI project kickoff guide | https://www.pmi.org/learning/library/effective-project-kick-off-meetings-5826 | Kickoff mode + playbook |
| PMI sponsor management | https://www.pmi.org/learning/library/role-executive-sponsor-success-projects-9831 | Executive sponsor management |
| PMI closure guide | https://www.pmi.org/learning/library/project-closure-phase-effective-9904 | Closure playbook |
| PMI lessons learned | https://www.pmi.org/learning/library/lessons-learned-next-level-communicating-7991 | Lessons learned doc |
| PMI risk management | https://www.pmi.org/learning/library/risk-management-process-9462 | Risk response strategies |
| Fathom video API | https://fathom.video/api | Meeting minutes + action items |
| Confluence (Atlassian) | https://developer.atlassian.com/cloud/confluence | Communication archive (KM) for Atlassian shops |
| Native CraftBot MCPs (linear-mcp / jira-mcp / notion-mcp / figma-mcp / figma-context-mcp / drawio-mcp / drawio-mcp-alt / gmail-mcp / outlook-mcp / google-workspace-mcp / slack-mcp / ms-teams-mcp / zoom-mcp / google-calendar-mcp / firecrawl-mcp / brightdata-mcp / playwright-mcp / brave-search / github / postgresql-mcp) | `app/config/mcp_config.json` | Per-platform automation surfaces in agent.yaml |

Total: 22 bundled SOTA skill packs + 20 native MCPs + 24 CraftBot default skills covering ≥95% of USE_CASES.md documented use cases. See `reference/SOTA_USE_CASES.md` for the per-use-case confidence map.

---

## Notes on "authored from synthesis"

Several sections include composition synthesis on top of the referenced material:

- **Three opening convictions in soul.md** — synthesized from canonical PM truisms: scope-time-budget triangle (universal in PMBOK / PRINCE2 / agile canon); "risks unaddressed become issues" (PMBOK 7 risk performance domain); "meeting without a decision is theatre" (industry idiom; Lenny Rachitsky / Cagan SVPG variants). Triad framing is composed.
- **Charter template in role.md** — synthesized from PMBOK 7 charter elements + PRINCE2 PID + Asana charter template. Specific section order is composed; each section's existence is from sources.
- **Charter quality rubric** — synthesized from PMBOK 7 charter best practices + Asana rubric + Reforge PM canon. The 9-item checklist is composed; each item maps to a source.
- **RAID DB template** — synthesized from Notion + Asana + RAIDLOG patterns. Column set is composed; each column standard-PM.
- **Risk scoring 5×5 matrix + color zones** — standard PM canon (PMI / many vendors); exact thresholds (low ≤5 / medium 6-12 / high ≥13) are conventional.
- **Status report weekly template (with RAG dashboard + EVM snapshot)** — synthesized from Lenny + Asana + Atlassian + PMI canon. Section order is composed; each section's existence is from sources.
- **Change request template** — synthesized from PMBOK 7 integrated change control + PRINCE2 + ProjectManager.com CR canon. Section order is composed.
- **Sprint plan template + DoR + DoD** — Scrum Guide + Mike Cohn canon + DoR/DoD industry standard. Composed structure.
- **Retro summary template** — synthesized from EasyRetro / Parabol / Atlassian retro guides. Format selection guidance composed.
- **Stage-gate template** — synthesized from Cooper canon + Planview templates + Monday guide. Composed structure.
- **Closure checklist** — synthesized from PMBOK 7 + PRINCE2 Closing a Project + PMI closure paper. Composed checklist.
- **EVM glossary + formulas + interpretation matrix** — standard PMI EVM canon; CPI/SPI < 0.9 flag threshold is conventional.
- **Antipattern catalog (12 BAD/GOOD pairs)** — composed from PMBOK 7 + PRINCE2 + Scrum Guide + Cooper + Lenny PM-anti-pattern commentary; specific BAD/GOOD pairs are illustrative composition.
- **First-conversation PROACTIVE.md self-init** — standard pattern from METHODOLOGY.md with PM-specific routine questions (primary PM tool / typical project duration / methodology mix).

No domain claims, methodology canon, framework formulas, or PM principles were invented. PMBOK 7 principles, PRINCE2 processes, Scrum Guide ceremonies, CPM forward/backward pass, EVM formulas (CV/SV/CPI/SPI/EAC/ETC), Cynefin framework, Mendelow Power-Interest grid, RACI/DACI/DRI, Cooper stage-gate outcomes, Asana RAID structure — all are cited canon.

---

## How to update this agent

1. Re-pull SOTA tool docs (Asana / Monday / ClickUp / Wrike / Linear / Jira / Smartsheet / TeamGantt / Float / Runn / Resource Guru / Harvest / Toggl / Clockify / Tempo / EasyRetro / Parabol / Miro / Geekbot / Range / Standuply / RAIDLOG / Lattice / Notion) every quarter — SOTA changes monthly. Platform MCP ecosystem is shipping new tools each release.
2. Diff against previous versions; update `reference/SOTA_USE_CASES.md` confidence ratings.
3. Update corresponding sections of `soul.md` and `role.md`.
4. Update this `SOURCES.md` if section names or source URLs changed.
5. Re-run `python verify.py project-manager` to confirm structure intact.
6. Re-run `python build.py project-manager` to regenerate `dist/project-manager.craftbot`.

For canonical PM reference repos:
- `wshobson/agents` — repull every quarter for any new PM agent definitions (e.g., `project-task-planner`).
- `VoltAgent/awesome-claude-code-subagents` — repull every quarter (e.g., `program-manager`).
- `msitarzewski/agency-agents` — repull every quarter (e.g., `scrum-master`, `agile-coach`).
- `vijaythecoder/awesome-claude-agents` — repull every quarter.
