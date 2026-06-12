# project-manager — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions (wshobson/agents, VoltAgent/awesome-claude-code-subagents, msitarzewski/agency-agents, vijaythecoder/awesome-claude-agents) were not downloaded in the v1 build pass — the SOTA mapping was derived from fresh 2026 web research (URLs cited in SOTA_USE_CASES.md and SOURCES.md).

The role and convictions are anchored to canonical project-management literature:

- **PMBOK 7th Edition** (Project Management Institute) — principles + performance domains
- **PRINCE2** (AXELOS) — process-driven control + stage management
- **SAFe / LeSS / Nexus** — scaled agile frameworks
- **Critical Path Method (CPM)** — schedule network analysis
- **Earned Value Management (EVM)** — cost/schedule performance metrics
- **Agile Manifesto** + Scrum Guide + Kanban Method canon
- **RACI / DACI / DRI** — responsibility assignment matrices

## Sources Considered But Not Downloaded

Reference subagent libraries (wshobson, VoltAgent, msitarzewski, vijaythecoder) were skipped because the upstream PM/program-manager personas tend to be brief stubs without the agentic-execution depth needed for a 2026 build. Fresh 2026 web research against vendor docs (Asana, Monday, ClickUp, Linear, Atlassian, Smartsheet, Notion, Float, Resource Guru, Runn, Harvest, Toggl, Clockify, Tempo, Geekbot, EasyRetro, Parabol) directly drove the SOTA mapping — that's what the agent ships against, so research-first is the load-bearing input.

For future tightening: pull 4-6 reference agents into `reference/agents/` (e.g., wshobson `project-task-planner`, VoltAgent `program-manager`, msitarzewski `scrum-master`, msitarzewski `agile-coach`) and 6-10 reference skills into `reference/skills/` (e.g., `gantt-charts`, `raid-log`, `critical-path`, `evm-reporting`, `sprint-planning`, `retrospective-facilitation`). Refresh quarterly — the platform MCP ecosystem (Asana/Monday/ClickUp/Linear/Atlassian/Smartsheet) is shipping new tools every release.
