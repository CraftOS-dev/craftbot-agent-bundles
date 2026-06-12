# grant-writer — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`) plus seeds in the per-agent build prompt.

For future tightening: pull 4-6 reference agents from `wshobson/agents`, `VoltAgent/awesome-claude-code-subagents`, `msitarzewski/agency-agents`, and `vijaythecoder/awesome-claude-agents` into `reference/agents/`, and 6-10 reference skills (LOI drafting, federal compliance, logic-model authoring) into `reference/skills/`.

## Sources Considered But Not Downloaded

- **wshobson/agents** — no grant-writer agent; closest is `technical-writer` (writing process generalization).
- **VoltAgent/awesome-claude-code-subagents** — no nonprofit/fundraising vertical agent.
- **msitarzewski/agency-agents** — has a `grant-writer` candidate; queued for v2 pull.
- **anthropics/skills** — `doc-coauthoring` reused indirectly for proposal authoring; not pulled into this folder.

The build pass relies on fresh 2026 web research (June 2026) to anchor every SOTA claim. Re-pulls should refresh `SOURCES.md` and `SOTA_USE_CASES.md` together.
