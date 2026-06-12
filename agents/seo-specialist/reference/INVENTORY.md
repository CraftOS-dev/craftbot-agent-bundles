# seo-specialist — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`) plus the parent `marketing-agent`'s SEO sections (which themselves draw from `msitarzewski-seo-specialist.md`).

For future tightening: pull 4-6 reference agents from `wshobson/agents`, `VoltAgent/awesome-claude-code-subagents`, `msitarzewski/agency-agents`, `vijaythecoder/awesome-claude-agents` into `reference/agents/` (priority: msitarzewski's `marketing-seo-specialist`, wshobson's `seo-` family in plugins/marketing, VoltAgent's `08-business-product/seo-content-strategist`, plus any dedicated technical-SEO / log-analyst agents), and 6-10 reference skills into `reference/skills/` (priority: any existing GSC / Screaming Frog / log-analyzer / AEO / schema / programmatic-SEO skill packs).

## Inherited from parent (marketing-agent)

For the SEO sections already present at `agent_bundle/agents/marketing-agent/role.md` (`SEO playbook`, `Cannibalization audit template`, `Technical SEO audit template`, `Keyword strategy template`, `On-page SEO checklist`, `Link building tactics`, `AI search adaptation`), the upstream sources are listed in `agent_bundle/agents/marketing-agent/reference/INVENTORY.md` — most load-bearing entry is `msitarzewski-marketing-seo-specialist.md`. This agent inherits and DEEPENS those treatments rather than re-deriving them; see `reference/SOTA_USE_CASES.md` for the per-use-case SOTA mapping that drives the depth beyond what the parent covers.

## Sources considered but not downloaded (v1 build pass)

- `msitarzewski/agency-agents/marketing/marketing-seo-specialist.md` — parent agent already pulls this; deeper-SEO duplications would just be re-extraction.
- `wshobson/agents` plugins/marketing/agents/* — Round 2 (skill-pack creation) should pull a few of these for ground-truthing the bundled skill packs.
- VoltAgent `08-business-product/seo-content-strategist.md` — same.
- Direct vendor docs (Screaming Frog CLI, Sitebulb, Botify, OnCrawl, Ahrefs, DataForSEO, Moz, Lumar, AthenaHQ, Profound, Surfer, MarketMuse, Schema.org validator, PageSpeed Insights, CrUX API) — referenced inline in `SOTA_USE_CASES.md`. Each bundled skill pack created in Round 2 will pull verbatim API/CLI docs into its own `references/` subfolder.
