# qa-engineer — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in SOTA_USE_CASES.md and SOURCES.md).

For future tightening: pull 4-6 reference agents from wshobson/agents, VoltAgent/awesome-claude-code-subagents, msitarzewski/agency-agents, vijaythecoder/awesome-claude-agents into `reference/agents/`, and 6-10 reference skills into `reference/skills/`.

## Reference agents to fetch (v2 backlog)

- `wshobson/agents` — `plugins/backend-development/agents/test-automator.md`
- `wshobson/agents` — `plugins/backend-development/agents/qa-engineer.md` (if exists; else compose from test-automator + performance-engineer)
- `VoltAgent/awesome-claude-code-subagents` — `04-quality-security/qa-engineer.md` (if exists)
- `VoltAgent/awesome-claude-code-subagents` — `04-quality-security/test-automator.md`
- `msitarzewski/agency-agents` — any QA / test automation roles
- `vijaythecoder/awesome-claude-agents` — framework-specific testers (Cypress, Playwright)

## Reference skills to fetch (v2 backlog)

- `playwright-e2e` / `playwright-mcp` (default — already shipped)
- BDD/Gherkin authoring
- Accessibility audit (axe-core, pa11y)
- k6 / Locust load patterns
- Pact contract testing
- Postman/Bruno API collections
- Visual regression (Percy/Chromatic/Applitools)
- Test data management (Faker, Mockaroo)

## Sources considered

- Sibling agent `senior-python-engineer` — used as shape/quality reference (line count, soul.md/role.md split, SOTA tool sections).
- CraftBot MCP catalog `app/config/mcp_config.json` — every MCP in `agent.yaml` cross-checked against this.
- CraftBot default skills folder `<repo>/skills/` — every default skill cross-checked against this.
- Web search aggregator (2026 sources cited in SOTA_USE_CASES.md and SOURCES.md).
