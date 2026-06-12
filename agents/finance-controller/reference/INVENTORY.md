# finance-controller — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`).

The seed list for SOTA tools came from the per-agent build prompt (Xero / QBO / Stripe / Ramp / Brex / Mercury / Carta / Pulley / Causal / Mosaic / Anrok / Vendr / etc.) and was cross-validated against (a) CraftBot's `app/config/mcp_config.json` and (b) 2025-2026 web sources (Visible.vc, Bessemer, Carta, Pulley, Pilot, Numeric, Truewind, Apideck, Knit, OpenBankingTracker, Solvimon, SaaSMag, ModelReef, Mercury, Spendflo, Tropic, Avalara/Anrok comparisons). See `reference/SOTA_USE_CASES.md` for the full mapping with per-use-case source URLs and confidence flags.

For future tightening: pull 4-6 reference finance/CFO agents from `wshobson/agents` (plugins/finance, plugins/business-analytics), `VoltAgent/awesome-claude-code-subagents` (categories/12-finance if/when published), and `msitarzewski/agency-agents` (CFO / controller / bookkeeper roles) into `reference/agents/`, plus 6-10 reference skills (close-procedure, ASC 606 revenue recognition, cap table modeling, 13-week cash flow, SaaS metrics, audit prep, equity grant 83b, sales tax compliance) into `reference/skills/`. The composition in `soul.md` / `role.md` is built from finance practitioner conventions (CFO / Controller bodies of knowledge — see SOURCES.md) and the SOTA tool reference table is fully grounded in cited URLs.

## Sources considered but not downloaded

- **wshobson/agents** — no dedicated finance/controller agent at the time of the build; closest is `business-analyst` (already pulled into `research-analyst`'s reference set).
- **VoltAgent/awesome-claude-code-subagents** — no finance-controller / accountant / CFO agent in the catalog as of June 2026. Recheck quarterly.
- **msitarzewski/agency-agents** — agency-focused; the bookkeeper / controller / fractional-CFO archetypes were checked but not pulled.
- **Anthropic skills** — no finance-domain skills published; the Intuit × Anthropic partnership (spring 2026) ships QBO/Mailchimp/TurboTax MCPs but the surface is in Intuit's repos, not Anthropic's skills repo.

## Composition basis

The composition in `soul.md` synthesizes finance practitioner conventions: (a) "close monthly, reconcile weekly" Controller mantra; (b) Bessemer / SaaS Capital "Rule of 40 + NRR + LTV:CAC" investor metrics; (c) Y Combinator / Visible.vc "monthly investor update" template; (d) 13-week rolling cash flow forecast methodology (Intuit Enterprise, Graphite Financial, ModelReef); (e) Carta's IPO-readiness ladder; (f) ASC 606 revenue recognition five-step model.

Every claim in `soul.md` / `role.md` either traces to a cited URL in `SOURCES.md` or is operational glue flagged in the "Notes on authored-from-synthesis" section there.
