# l10n — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`).

The l10n role draws structurally from its parent `technical-writer` agent (mirrored under `agent_bundle/agents/technical-writer/`) and from adjacent siblings `marketing-agent`, `seo-specialist`, and `frontend-engineer`. The SOTA tool surface (TMS / CAT / MT / i18n libraries / RTL / CLDR / subtitle) was researched per use case against 2025-2026 sources rather than lifted from a single upstream agent.

For future tightening: pull 4-6 reference agents (e.g., wshobson/agents `localization-engineer`, VoltAgent `i18n-specialist`, msitarzewski `engineering-localization-engineer`) into `reference/agents/`, and 6-10 reference skills (e.g., `pseudo-localization`, `icu-messageformat`, `rtl-cjk-testing`) into `reference/skills/`. The v1 pass intentionally skipped this download step to ship the agent on the SOTA mapping alone; the build is correct but provenance for soul.md/role.md sentences is via the URLs in `SOTA_USE_CASES.md` rather than verbatim upstream files.

---

## Sources Considered (not downloaded — v1 SOTA mapping pass)

| Source | Why not downloaded in v1 |
|---|---|
| wshobson/agents — `plugins/i18n/` | Repository did not have a dedicated i18n plugin folder as of June 2026; localization patterns were scattered across `engineering` and `documentation-generation`. Re-check next quarter. |
| VoltAgent/awesome-claude-code-subagents — `localization-engineer` | Existed as a sub-bullet in `categories/07-specialized-domains/` but was incomplete; planned for v2 refresh. |
| anthropics/skills — `localization`, `pseudo-localization` | Not present in the official skills catalog as of June 2026. SOTA mapping drove the bundled skill pack names instead. |
| Mozilla Localization Process docs | Authoritative for Firefox/Mozilla L10n workflows but Firefox-specific. Distilled into RTL guidance in `SOTA_USE_CASES.md`. |
| Unicode CLDR `tr35.html` (LDML spec) | Cited as primary source for locale data; not downloaded verbatim because the LDML spec is normative reference material, not playbook content. |
| W3C i18n techniques | Cited via specific guides (RTL, bidi, language tags) but not bulk-downloaded; treated as standards reference. |

---

## Status check

- v1 build pass produced `SOTA_USE_CASES.md` covering 23 use cases at ~96% fulfillment.
- 22 bundled skill packs reserved (names only — `SKILL.md` contents produced in Round 2).
- 5 MCPs from CraftBot's catalog mapped to SOTA rows (`filesystem`, `deepl-mcp`, `github`, `figma-mcp`, `gemini-ocr-mcp`).
- 18 CraftBot default skills audited and adopted from the top-level `skills/` folder.

Refresh trigger: SOTA in this domain changes monthly (Crowdin AI features, Phrase Strings GA, Lokalise OTA changes, paraglide-js LocalizedString branding, ICU MessageFormat 2.0 progress). Re-check upstream every 60 days.
