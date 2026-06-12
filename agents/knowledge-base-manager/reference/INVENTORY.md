# knowledge-base-manager — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`).

For future tightening: pull 4-6 reference agents from `wshobson/agents`, `VoltAgent/awesome-claude-code-subagents`, `msitarzewski/agency-agents`, `vijaythecoder/awesome-claude-agents` into `reference/agents/` (search for `knowledge-base`, `documentation-engineer`, `content-strategist`, `support-engineer`, `internal-comms` slugs), and 6-10 reference skills into `reference/skills/` (e.g., `kb-taxonomy`, `algolia-docsearch`, `notion-kb`, `confluence-mgmt`, `kapa-ai-integration`).

## Sibling agent context

This specialist sits one tier under `technical-writer` and shares the content category. The taxonomy / lifecycle / governance lane has different load-bearing tools than the dev-doc lane (developer portals, ADRs, API references) — hence the dedicated specialist.

Related agents already in the catalog:
- `agents/technical-writer/` — parent. Owns developer docs, OpenAPI, ADRs.
- `agents/customer-support-agent/` — KB consumer; deflection metric owner.
- `agents/operations-agent/` — internal-process docs; SOP runbooks.
- `agents/community-manager/` — community-driven KB contribution.
- `agents/seo-specialist/` — public-KB SERP / AEO / GEO depth.
