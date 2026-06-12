# operations-agent — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in SOTA_USE_CASES.md and SOURCES.md) and from the seed prompt's curated 2026 SOTA tool lists across HR / ATS / payroll / IT / vendor management / workflow automation / internal tools / device management / SSO / process documentation / travel & expense / insurance / office management / PEO/EOR / knowledge base / AI governance.

The seed prompt enumerated 30+ use cases and ≥22 bundled skill packs, all cross-referenced against the CraftBot MCP catalog and default-skill folder in this build pass. No existing CraftBot agent (`finance-controller`, `devops-engineer`, `legal-counsel`, `data-analyst`) covered the operations / HR ops / vendor ops / internal-tooling surface — this agent fills that gap as the "ops glue" generalist for solo founders and small ops teams.

For future tightening: pull 4-6 reference agents from `wshobson/agents` (any `plugins/operations/` or `plugins/people-ops/`), `VoltAgent/awesome-claude-code-subagents` (`categories/people-ops/` / `categories/operations/` if present), `msitarzewski/agency-agents` (HR / ops / procurement specialists), and 6-10 reference skills (Greenhouse / Lever / Ashby SOTA recipes, n8n / Zapier / Make workflow patterns, Retool / Tooljet / Budibase internal-app recipes, Kandji / Jamf / Intune MDM patterns) into `reference/agents/` and `reference/skills/`.

Sources considered but not downloaded in v1:
- `github.com/wshobson/agents` — no operations / people-ops plugin observed as of build date (June 2026); recheck quarterly.
- `github.com/VoltAgent/awesome-claude-code-subagents` — no dedicated operations agent observed; HR / people-ops adjacent agents may exist under `categories/13-hr/` (recheck).
- `github.com/msitarzewski/agency-agents` — strong on agency / marketing / specialized roles but ops coverage thin (recheck for HR-coordinator / procurement-specialist agents).
- `github.com/JSONbored/claudepro-directory` — search for `ops` / `hr` / `procurement` / `internal-tools` skills.
