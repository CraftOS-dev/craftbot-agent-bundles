# product-manager — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`).

For future tightening: pull 4-6 reference agents from `wshobson/agents` (product-manager, product-strategist, technical-product-manager), `VoltAgent/awesome-claude-code-subagents` (categories/08-business-product/product-manager), `msitarzewski/agency-agents` (product/product-manager, product/product-discovery, product/product-launch), and `vijaythecoder/awesome-claude-agents` into `reference/agents/`. Pull 6-10 reference skills (PRD-writer, roadmap-builder, user-research-synthesizer, RICE-prioritization, etc.) into `reference/skills/`.

## Reference Agents (planned for v2)

| File | Source | Status |
|---|---|---|
| `agents/wshobson-product-manager.md` | https://github.com/wshobson/agents/tree/main/plugins/product-management/agents/product-manager | not downloaded |
| `agents/voltagent-product-manager.md` | https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/product-manager.md | not downloaded |
| `agents/voltagent-product-strategist.md` | https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/product-strategist.md | not downloaded |
| `agents/msitarzewski-product-manager.md` | https://github.com/msitarzewski/agency-agents/blob/main/product/product-manager.md | not downloaded |
| `agents/msitarzewski-product-discovery.md` | https://github.com/msitarzewski/agency-agents/blob/main/product/product-discovery.md | not downloaded |
| `agents/msitarzewski-product-launch.md` | https://github.com/msitarzewski/agency-agents/blob/main/product/product-launch.md | not downloaded |

## SOTA Research Sources (used in v1 build)

The SOTA mapping in `SOTA_USE_CASES.md` is grounded in 2025-2026 product management practice across these published references (full URLs in `SOTA_USE_CASES.md` and `SOURCES.md`):

- Linear product management API + MCP (linear.app/docs)
- Notion MCP for PRDs/roadmaps (developers.notion.com/docs/mcp)
- Figma Dev Mode MCP (help.figma.com/hc/en-us/articles/dev-mode-mcp-server)
- Dovetail v3 API for user research synthesis (dovetail.com/api)
- Maze API for usability testing (help.maze.co/hc/en-us/articles/api)
- Amplitude/Mixpanel/PostHog MCPs (amplitude.com/docs/mcp, mixpanel.com/docs/mcp, posthog.com/docs/model-context-protocol)
- Statsig + GrowthBook MCPs (statsig.com/docs, blog.growthbook.io)
- Lattice OKRs API (lattice.com/api-docs)
- FullStory + LogRocket session-replay APIs (developers.fullstory.com, docs.logrocket.com)
- Productboard Public API (developer.productboard.com)
- ChatPRD / Kraftful for AI-assisted PRD generation (chatprd.ai, kraftful.com)
- Jeff Patton story mapping methodology (jpattonassociates.com/story-mapping)
- JTBD framework (Christensen + Klement) (jobs-to-be-done.com)
- RICE/ICE/Kano scoring frameworks (intercom.com/blog/rice-simple-prioritization)
- Beta program management — Centercode (centercode.com)
- Release notes automation — git-cliff + conventional commits (git-cliff.org)
- Stakeholder updates — Lenny Rachitsky's weekly update format (lennysnewsletter.com)

## Sources Considered But Not Downloaded

| Source | Why excluded |
|---|---|
| ProductPlan, Roadmunk, Aha! roadmap tools | Public APIs exist but ProductBoard's coverage subsumes most workflows; deferred to v2 |
| Cycle.app, Sherlock | Smaller adoption — covered via cli-anything + curl if user requests |
| Workboard, Mooncamp OKR tools | Lattice + 15Five via public APIs cover the OKR surface; deferred to v2 |
| 15Five OKR | Adjacent to Lattice; covered as fallback in role.md |
| Sprig in-product surveys | Adjacent to Maze/Dovetail; v2 |
| UserTesting | Maze is the SOTA replacement for moderated + unmoderated v2026 |
| Hotjar, Microsoft Clarity, Smartlook | FullStory + LogRocket cover the session-replay surface; Clarity is free fallback |
| Userpilot, Pendo (in-product guides) | Adjacent to onboarding/activation specialist; v2 |
| Lookback, PlaybookUX | Dovetail interview synthesis covers most of this surface |

---

**v1 build approach:** SOTA-driven from published 2025-2026 sources. The agent ships with strong execution paths for every documented use case via Linear/Notion/Figma/Amplitude/Mixpanel/PostHog/Statsig/GrowthBook/FullStory/LogRocket/Dovetail/Maze/Lattice + cli-anything + curl for any remaining gap.
