# social-media-manager — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions (wshobson/agents, VoltAgent/awesome-claude-code-subagents, msitarzewski/agency-agents) were not downloaded in this v1 build pass — the SOTA mapping was derived from June 2026 web research (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`).

Adjacent CraftBot v0 agent referenced as a structural mirror: `agent_bundle/agents/marketing-agent/` (parent — general marketing). Shape, token discipline, execution-stack pattern, and PROACTIVE footer all mirror that agent.

## What's in this inventory today

- `reference/SOTA_USE_CASES.md` — 22 use-case sections, each with SOTA approach / agent execution path / source URL / confidence rating. Summary table + verdict line at the end.
- This `INVENTORY.md` — pointer file. No downloaded reference agents/skills under `reference/agents/` or `reference/skills/` in this build pass.

## Sources considered but not downloaded

- **wshobson/agents — plugins/marketing/** — would yield additional community-management and social-listening framing; deferred to a future tightening pass.
- **VoltAgent/awesome-claude-code-subagents — categories/08-business-product/social-media-strategist.md** — single-file definition; deferred.
- **msitarzewski/agency-agents — marketing/marketing-social-media-strategist.md** — already informed `marketing-agent`; cross-pollination is via that agent's `reference/`.
- **Anthropic skills** — no social-media-specific skills in their catalog yet.

## For future tightening

Pull 4-6 reference agents from wshobson/agents, VoltAgent, msitarzewski into `reference/agents/`, plus 6-10 reference skills into `reference/skills/`. Re-derive SOTA mapping with those as primary citation backing rather than web-only.
