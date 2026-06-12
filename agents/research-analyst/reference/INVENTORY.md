# Research Analyst — Reference Inventory

Raw downloaded SOTA material. Every section in `agent.yaml`, `soul.md`, and `role.md` traces back to one of these files.

## Reference Agents (10 files)

| File | Source | Status |
|---|---|---|
| `agents/voltagent-research-analyst.md` | [VoltAgent/categories/10-research-analysis/research-analyst.md](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/10-research-analysis/research-analyst.md) — **PRIMARY** name match; full research methodology, info gathering, source eval, data synthesis, analysis techniques, report creation | full |
| `agents/voltagent-market-researcher.md` | [VoltAgent/categories/10-research-analysis/market-researcher.md](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/10-research-analysis/market-researcher.md) — market sizing, consumer behavior, segmentation, opportunity ID | full |
| `agents/voltagent-competitive-analyst.md` | [VoltAgent/categories/10-research-analysis/competitive-analyst.md](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/10-research-analysis/competitive-analyst.md) — competitor mapping, SWOT, benchmarking, intelligence gathering | full |
| `agents/voltagent-scientific-literature-researcher.md` | [VoltAgent/categories/10-research-analysis/scientific-literature-researcher.md](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/10-research-analysis/scientific-literature-researcher.md) — evidence-based analysis, study quality assessment, BGPT MCP search | full |
| `agents/voltagent-data-researcher.md` | [VoltAgent/categories/10-research-analysis/data-researcher.md](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/10-research-analysis/data-researcher.md) — data discovery, validation, statistical analysis | **summary** |
| `agents/voltagent-search-specialist.md` | [VoltAgent/categories/10-research-analysis/search-specialist.md](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/10-research-analysis/search-specialist.md) — Boolean operators, proximity searching, multi-source retrieval, precision > 90% | **summary** |
| `agents/voltagent-first-principles-thinking.md` | [VoltAgent/categories/10-research-analysis/first-principles-thinking.md](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/10-research-analysis/first-principles-thinking.md) — 5-step method (Define/Assumptions/Challenge/Extract/Rebuild) + 5D Method | **summary** |
| `agents/voltagent-trend-analyst.md` | [VoltAgent/categories/10-research-analysis/trend-analyst.md](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/10-research-analysis/trend-analyst.md) — weak signal detection, pattern validation, scenario planning | **summary** |
| `agents/voltagent-cohort-analysis.md` | [VoltAgent/categories/10-research-analysis/cohort-analysis.md](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/10-research-analysis/cohort-analysis.md) — retention curves, activation analysis, cohort table format | full |
| `agents/wshobson-business-analyst.md` | [wshobson/plugins/business-analytics/agents/business-analyst.md](https://github.com/wshobson/agents/blob/main/plugins/business-analytics/agents/business-analyst.md) — BI platforms, KPI frameworks, statistical analysis, financial modeling | full |

## Reference Skills (2 files)

Bundled inside `.craftbot`:

| File | Source | Status |
|---|---|---|
| `skills/data-storytelling/SKILL.md` | [wshobson/plugins/business-analytics/skills/data-storytelling](https://github.com/wshobson/agents/tree/main/plugins/business-analytics/skills/data-storytelling) — Setup→Conflict→Resolution, "start with so-what" principle, 3 essential elements | **summary** |
| `skills/kpi-dashboard-design/SKILL.md` | [wshobson/plugins/business-analytics/skills/kpi-dashboard-design](https://github.com/wshobson/agents/tree/main/plugins/business-analytics/skills/kpi-dashboard-design) — 3-tier framework, SMART KPIs, 5-7 KPI limit, troubleshooting | **summary** |

## Sources Considered But Not Downloaded

| Source | Why excluded |
|---|---|
| msitarzewski `academic/` folder (anthropologist, geographer, historian, narratologist, psychologist) | Domain-specialist academic personas — too narrow for a general research-analyst |
| msitarzewski `specialized/` matches (pricing analyst, data privacy officer, identity graph operator) | Domain-specific; pricing belongs to a finance specialist, identity-graph is data engineering |
| VoltAgent ab-test-analysis, project-idea-validator | Too narrow / orthogonal to general research |
| wshobson startup-business-analyst, data-engineering plugins | Adjacent but not core for v0 research-analyst |
| Anthropic skills | No research-specific skills exist there yet (design/document/content only) |
| claudepro-directory | Tree not browseable at expected paths |
