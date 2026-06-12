# ceo-agent — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions (wshobson, VoltAgent, msitarzewski, vijaythecoder) were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`) and from the adjacent worked agents (`marketing-agent`, `product-manager`) whose strategic + cross-functional shape was mirrored.

For future tightening: pull 4-6 reference agents from `wshobson/agents` (chief-of-staff, executive-coach, business-operator), `VoltAgent/awesome-claude-code-subagents` (08-business-product category — strategy, leadership), `msitarzewski/agency-agents` (executive / leadership / strategy agents), `vijaythecoder/awesome-claude-agents` into `reference/agents/`, and 6-10 reference skills (board prep, OKR cascade, all-hands prep, decision frameworks) into `reference/skills/`.

## Sibling agents consulted for shape and convictions

- `c:\Users\zfoong\Desktop\agent\code\git\CraftBot\agent_bundle\agents\marketing-agent\` — general/strategic tier, conviction phrasing pattern, mode-per-verb decomposition, SOTA execution stack format.
- `c:\Users\zfoong\Desktop\agent\code\git\CraftBot\agent_bundle\agents\product-manager\` — strategic + cross-functional defer rules (positioning → marketing-agent, sales → sales-agent, etc.), bundled-vs-default skill grouping, MCP audit pattern.

## Per-agent prompt seeds (validated and extended via web search June 2026)

- 16 use case clusters (≥20 atomic use cases when enumerated) — strategy/vision, board, investor relations, exec hiring, OKRs, decision frameworks, all-hands, QBR, calendar, async comms, KPI dashboard, M&A, partnerships, crisis comms, narrative/positioning, governance.
- 20 bundled skill packs reserved (Round 2 creates `SKILL.md` content).
- ~26 MCPs from CraftBot catalog matched against SOTA execution paths.
