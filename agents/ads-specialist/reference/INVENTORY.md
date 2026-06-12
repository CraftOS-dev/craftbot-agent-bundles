# ads-specialist — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in SOTA_USE_CASES.md and SOURCES.md) and the per-agent seed prompt's curated SOTA tool list (Meta/Google/TikTok/LinkedIn official MCPs, Triple Whale, Northbeam, Wicked Reports, Hyros, Rockerbox; AppsFlyer/Adjust/Branch/Singular for mobile; Smartly.io, AdCreative.ai, Madgicx; Google Meridian, Meta Robyn, Recast, lightweight_mmm, PyMC-Marketing; GTM Server-side, Stape, Snowplow; Meta CAPI, TikTok Events API, Google Enhanced Conversions, Reddit Conversion API; Meta Ad Library, Google Ads Transparency Center, Pathmatics; Funnel.io, Improvado, Supermetrics).

The parent agent at `agent_bundle/agents/marketing-agent/` is the structural template for this specialist — its `agent.yaml`, `soul.md`, `role.md`, and `USE_CASES.md` shapes were mirrored. Sibling `growth-agent/` informed attribution depth crossover. Sibling `seo-specialist/` informed the "specialist tier" style for cross-references and execution-stack density.

## Sources Considered But Not Downloaded

| Source | Why excluded in v1 pass |
|---|---|
| wshobson/agents plugins/paid-ads/ | URL trail not verified in v1; future tightening would pull these |
| VoltAgent/awesome-claude-code-subagents categories for paid-ads-strategist | Adjacent — names listed below as Round 2 expansion candidates |
| msitarzewski/agency-agents paid/* | Same — Round 2 expansion |
| Anthropic skills | No paid-ads / attribution skills shipped yet in their catalog |

## For Future Tightening (Round 2+)

Pull 4-6 reference agents from:
- `github.com/wshobson/agents` (paid-ads / performance-marketing plugins)
- `github.com/VoltAgent/awesome-claude-code-subagents` (any paid / ads / performance role in 08-business-product)
- `github.com/msitarzewski/agency-agents` (marketing/marketing-ads-* if present, marketing-performance-*)
- `github.com/vijaythecoder/awesome-claude-agents`

Into `reference/agents/`, and 6-10 reference skills (Meta Ads campaign structure, Google PMax, MMM methodology, SKAN 4 mobile attribution playbook, server-side tagging recipe) into `reference/skills/`.
