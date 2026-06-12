# Localization (L10n) — Source Attribution

This file maps every section of `soul.md` and `role.md` back to the SOTA research it draws from. It is part of the bundle but is **not** loaded into the agent's context — it exists for human verification and future updates.

The v1 build pass operated from web research (URLs cited in `reference/SOTA_USE_CASES.md` and `agent.yaml → sources`) rather than from verbatim upstream agent files. Future tightening can pull and store the upstream files under `reference/agents/` and `reference/skills/`.

---

## soul.md → source map

| Section in soul.md | Source(s) |
|---|---|
| Title + persona intro (action verbs + convictions) | `reference/SOTA_USE_CASES.md` (per-use-case mechanisms + headliner tool names) |
| "Three load-bearing convictions" | Synthesis: (1) TM-as-asset from memoQ TMS docs + Lilt adaptive MT essay; (2) layout-is-half from Evil Martians + Placeholdertext RTL guides; (3) transcreation framing from Lilt Labs |
| Purpose | Synthesis from TMS comparison sources + Crowdin/Lokalise/Phrase positioning |
| Execution stack | `reference/SOTA_USE_CASES.md` (skill pack names mapped 1:1 from "Recommended agent.yaml additions" section) |
| When invoked — New-locale launch | Synthesis from Crowdin docs + better-i18n TMS guide + Browser-Stack i18n testing 2026 |
| When invoked — Adding a locale | Crowdin Getting Started + next-intl docs + RTL/CJK guides |
| When invoked — TMS pipeline setup | Crowdin CLI + GitHub Action docs + Lokalise CLI 2 + Phrase CLI |
| When invoked — Translation memory cleanup | memoQ TMS docs + Okapi Framework Tikal CLI |
| When invoked — Pseudo-localization gate | dev.to pseudo-l10n + l10n.dev pseudo-localization help + Lokalise qps-ploc docs |
| When invoked — RTL/CJK regression | Evil Martians 600M RTL + Placeholdertext RTL guide + Noto CJK Adobe Fonts |
| When invoked — Translator MQM scoring | themqm.org + TAUS DQF framework |
| When invoked — Source translatability review | SimpleLocalize i18n guide + Vale docs |
| Core operating rules (17 bullets) | Synthesis from Evil Martians + ICU MessageFormat (Phrase) + better-i18n SEO + Lilt adaptive MT + Noto CJK + browser-stack i18n testing |
| Mode-specific decisions | Tool-specific decision matrices from each cited source |
| RTL/CJK/locale gate checklist | Synthesis from Playwright docs + Vale + Lychee + better-i18n hreflang guide |
| Quality gates | Synthesis from ICU MessageFormat lint + MQM scorecard + Noto CJK font-display + subtitle CPS bands |
| Output format | Synthesis from TMS export formats (JSON/XLIFF/PO/YAML/ARB/TMX/TBX) |
| Communication style | Operational glue, role-specific tone |
| When to push back | Operational glue derived from Core operating rules (refuse pseudo skip, refuse `margin-left`, refuse `zh-CN` shorthand) |
| When to defer | Sibling agent boundary map: `technical-writer`, `marketing-agent`, `seo-specialist`, `frontend-engineer`, `video-creator` |
| On first conversation (PROACTIVE init) | `METHODOLOGY.md` standard footer wording — questions adapted to L10n routines |
| Closing rule | Synthesis restating the three convictions |

---

## role.md → source map

| Section in role.md | Source(s) |
|---|---|
| Capability reference → TMS platforms | better-i18n + intlpull comparison + Lokalise/Phrase/Crowdin official docs |
| Capability reference → CAT tools | memoQ + Trados + Phrase TMS official docs + TranslatedRight comparison |
| Capability reference → Translation engines | techno-pulse 2026 MT comparison + DeepL/Google/Amazon/ModernMT/Lilt official |
| Capability reference → LSPs | Smartcat + Lilt vs Unbabel + TransPerfect industry knowledge |
| Capability reference → i18n libraries | Definitive Guide to i18n Libraries 2026 + paraglide-js GitHub + auto18n 2026 React i18n |
| Capability reference → File formats | intlpull JSON vs XLIFF vs PO 2026 + Locize Gettext + ARB/Flutter docs |
| Capability reference → Locale data | CLDR + ICU + IANA registry + IATE + UNTERM + MultiTerm |
| Capability reference → Locale-specific concerns | CLDR plural rules + Intl.* documentation |
| TMS selection matrix | better-i18n + intlpull + Lokalise/Crowdin/Phrase positioning |
| i18n library selection matrix | Definitive Guide 2026 + paraglide-js benchmarks + next-intl design principles |
| ICU MessageFormat catalog | Phrase ICU MessageFormat guide + FormatJS docs |
| CLDR plural rules reference | CLDR plural rules charts + react-i18next ICU docs |
| BCP 47 tag examples | IANA registry + CLDR picking-the-right-language-code |
| hreflang correctness checklist | Google managing multi-regional sites + better-i18n hreflang guide |
| RTL CSS migration playbook | Evil Martians 600M RTL + Placeholdertext RTL guide + MDN CSS Logical Properties |
| CJK font subsetting playbook | Noto CJK GitHub + font-converters subsetting guide + symbolfyi CJK typography |
| Pseudo-localization recipe | pseudo-l10n npm + l10n.dev pseudo-localization help + Crowdin distribution docs |
| Translation memory hygiene playbook | memoQ TMS + Okapi Framework + aiproductivity TM leverage guide |
| MQM 2.0 scorecard | themqm.org + TAUS DQF + Lilt MQM essays |
| Subtitle CPS reference | Subtitle Edit GitHub + Subly docs + EBU broadcast standards |
| Source content translatability rubric | SimpleLocalize i18n guide + Vale docs + composition synthesis |
| Locale routing patterns | better-i18n hreflang guide + Google multi-regional + Next.js / Astro / Docusaurus / MkDocs i18n docs |
| SOTA tool reference (June 2026) | All sources cited in `reference/SOTA_USE_CASES.md` |
| SOTA execution playbook table | Synthesis from `reference/SOTA_USE_CASES.md` summary table |
| Antipattern catalog | Synthesis from RTL guides + ICU MessageFormat docs + Google hreflang errors + Noto CJK regional docs |
| Reference patterns | Synthesis from Crowdin GitHub Action + next-intl docs + paraglide-js Svelte + FormatJS extraction + MJML + Playwright |
| Closing rules | Synthesis restating the three convictions |

---

## Notes on "authored from synthesis"

The v1 pass operated as a SOTA mapping build (not a verbatim-upstream-agent build). All sections labeled "Synthesis" above derive from the cited primary sources in `reference/SOTA_USE_CASES.md`; the framing and ordering are composed locally rather than lifted from a single upstream agent.

These synthesized sections are operational glue and aggregations — not domain claims. Every domain claim (a tool name, a CLDR rule, a hreflang requirement, an MQM error category, a CJK subset character form) traces to one of the cited primary sources.

---

## How to update this agent

If you want to refresh content from upstream:

1. Pull updated SOTA tool documentation from the URLs in `agent.yaml → sources` and `reference/SOTA_USE_CASES.md`.
2. Diff against the previous versions to see what changed.
3. Update the corresponding sections of `soul.md`, `role.md`, and `reference/SOTA_USE_CASES.md`.
4. If a new SOTA tool emerged (e.g., new TMS, new MT engine), add it to `agent.yaml` `enabled_skills` and `mcp_servers` if applicable, then write a new bundled skill pack via Round 2 runtime build.
5. Re-run `python verify.py l10n` to confirm structure intact.
6. Re-build: `python build.py l10n` produces a fresh `.craftbot`.

The SOTA in this domain changes monthly. Refresh trigger every 60 days at minimum:
- Crowdin AI features + AI translation engine catalog
- Phrase Strings GA + Phrase TMS feature parity
- Lokalise OTA changes
- paraglide-js compiler maturity + new framework adapters
- ICU MessageFormat 2.0 standardization progress
- DeepL / ModernMT / Lilt model upgrades
- LSP-side adaptive MT capabilities

---

## SOTA sources (June 2026)

The `role.md → SOTA tool reference (June 2026)` section and the bundled SOTA skill packs trace to these primary sources. Each row pairs the tool with the canonical URL the agent consulted.

| Tool / framework | Source | Used in |
|---|---|---|
| Crowdin CLI | https://github.com/crowdin/crowdin-cli | `skills/tms-setup-crowdin-lokalise-phrase/SKILL.md` |
| Crowdin GitHub Action | https://github.com/crowdin/github-action | `skills/tms-setup-crowdin-lokalise-phrase/SKILL.md` |
| Crowdin In-Context | https://support.crowdin.com/in-context-localization/ | `skills/in-context-editor-setup/SKILL.md` |
| Crowdin OTA SDK | https://github.com/crowdin/react-native-sdk | `skills/tms-setup-crowdin-lokalise-phrase/SKILL.md` |
| Lokalise CLI 2 | https://github.com/lokalise/lokalise-cli-2-go | `skills/tms-setup-crowdin-lokalise-phrase/SKILL.md` |
| Phrase | https://phrase.com/ | `skills/tms-setup-crowdin-lokalise-phrase/SKILL.md` |
| TMS comparison (Crowdin vs Lokalise vs Phrase 2026) | https://intlpull.com/blog/lokalise-vs-phrase-vs-crowdin-2026 | `reference/SOTA_USE_CASES.md` |
| TMS landscape 2026 | https://better-i18n.com/en/i18n/best-tms/ | `reference/SOTA_USE_CASES.md` |
| memoQ TMS | https://www.memoq.com/product/memoq-tms/ | `skills/cat-tool-memoq-trados-phrase/SKILL.md` |
| memoQ AGT (adaptive MT) | https://www.memoq.com/product/memoq-agt/ | `skills/cat-tool-memoq-trados-phrase/SKILL.md` |
| Trados Studio / MultiTerm | https://www.trados.com/product/multiterm/ | `skills/glossary-termbase-multiterm/SKILL.md` |
| DeepL API | https://www.deepl.com/docs-api | `skills/ai-mt-deepl-pro-post-editing/SKILL.md` |
| DeepL vs Google Translate vs Amazon vs ModernMT 2026 | https://www.techno-pulse.com/2026/04/best-ai-translation-tools-in-2026-deepl.html | `skills/ai-mt-deepl-pro-post-editing/SKILL.md` |
| ModernMT | https://www.modernmt.com/api/ | `skills/ai-mt-deepl-pro-post-editing/SKILL.md` |
| Lilt | https://lilt.com/ | `skills/ai-mt-deepl-pro-post-editing/SKILL.md` |
| Lilt adaptive MT vs PEMT | https://lilt.com/blog/ai-translation-automation-how-enterprise-translation-systems-work | `skills/ai-mt-deepl-pro-post-editing/SKILL.md` |
| Unbabel | https://lilt.com/vs/unbabel | `skills/lsp-vendor-management/SKILL.md` |
| IATE EU terminology | https://iate.europa.eu/ | `skills/glossary-termbase-multiterm/SKILL.md` |
| Xbench | https://docs.xbench.net/ | `skills/locale-qa-linguistic-functional/SKILL.md` |
| Okapi Framework | https://okapiframework.org/ | `skills/locale-qa-linguistic-functional/SKILL.md` |
| CLDR | https://cldr.unicode.org/ | `skills/gender-name-address-currency-localization/SKILL.md` |
| ICU MessageFormat (Phrase guide) | https://phrase.com/blog/posts/guide-to-the-icu-message-format/ | `skills/icu-messageformat-pluralization/SKILL.md` |
| FormatJS | https://formatjs.io/ | `skills/icu-messageformat-pluralization/SKILL.md` |
| react-i18next | https://www.i18next.com/ | `skills/in-app-message-i18next-react-intl/SKILL.md` |
| react-intl | https://formatjs.io/docs/react-intl/ | `skills/in-app-message-i18next-react-intl/SKILL.md` |
| next-intl | https://next-intl.dev/ | `skills/in-app-message-i18next-react-intl/SKILL.md` |
| paraglide-js | https://github.com/opral/paraglide-js | `skills/in-app-message-i18next-react-intl/SKILL.md` |
| Definitive Guide to i18n Libraries for Next.js / React 2026 | https://gundogmuseray.medium.com/the-definitive-guide-to-i18n-libraries-for-next-js-react-in-2026-8102c7f68a77 | `skills/in-app-message-i18next-react-intl/SKILL.md` |
| pseudo-l10n npm | https://www.npmjs.com/package/pseudo-l10n | `skills/pseudo-localization/SKILL.md` |
| Pseudo-localization for i18n testing | https://dev.to/anton_antonov/pseudo-localization-for-automated-i18n-testing-31 | `skills/pseudo-localization/SKILL.md` |
| Pseudo-localization (l10n.dev) | https://l10n.dev/help/pseudo-localization | `skills/pseudo-localization/SKILL.md` |
| Evil Martians — 600M write RTL | https://evilmartians.com/chronicles/600-million-people-write-right-to-left-2-fixes-your-app-needs | `skills/rtl-cjk-layout-testing/SKILL.md` |
| Complete Guide to RTL Layout Testing | https://placeholdertext.org/blog/the-complete-guide-to-rtl-right-to-left-layout-testing-arabic-hebrew-more/ | `skills/rtl-cjk-layout-testing/SKILL.md` |
| MDN — direction property | https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/direction | `skills/rtl-cjk-layout-testing/SKILL.md` |
| Noto CJK GitHub | https://github.com/notofonts/noto-cjk | `skills/font-selection-cjk-rtl/SKILL.md` |
| CJK font optimization guide | https://font-converters.com/languages/cjk-font-optimization | `skills/font-selection-cjk-rtl/SKILL.md` |
| Font subsetting by language | https://font-converters.com/guides/font-subsetting-by-language | `skills/font-selection-cjk-rtl/SKILL.md` |
| CJK Web Typography | https://symbolfyi.com/guides/cjk-web-typography/ | `skills/font-selection-cjk-rtl/SKILL.md` |
| glyphhanger | https://github.com/zachleat/glyphhanger | `skills/font-selection-cjk-rtl/SKILL.md` |
| i18n SEO + hreflang guide | https://better-i18n.com/en/blog/i18n-seo-hreflang-locale-urls-guide/ | `skills/locale-routing-subdomain-subdirectory/SKILL.md` |
| Google managing multi-regional sites | https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites | `skills/locale-routing-subdomain-subdirectory/SKILL.md` |
| Next.js i18n | https://nextjs.org/docs/pages/guides/internationalization | `skills/locale-routing-subdomain-subdirectory/SKILL.md` |
| Internationalization Testing (BrowserStack) | https://www.browserstack.com/guide/internationalization-testing-of-websites-and-apps | `skills/locale-qa-linguistic-functional/SKILL.md` |
| SimpleLocalize i18n complete guide | https://simplelocalize.io/blog/posts/internationalization-guide-software-localization/ | `skills/source-content-translatability-review/SKILL.md` |
| Subtitle Edit | https://github.com/SubtitleEdit/subtitleedit | `skills/subtitle-audio-video-localization/SKILL.md` |
| Subly subtitle translator | https://www.getsubly.com/features/subtitle-translator | `skills/subtitle-audio-video-localization/SKILL.md` |
| Whisper (OpenAI) | https://github.com/openai/whisper | `skills/subtitle-audio-video-localization/SKILL.md` |
| Best free subtitle editors 2026 | https://intlpull.com/blog/best-free-subtitle-editors-2026 | `skills/subtitle-audio-video-localization/SKILL.md` |
| MQM framework | https://themqm.org/ | `skills/translator-quality-scoring/SKILL.md` |
| TAUS DQF | https://www.taus.net/qe-platform/dynamic-quality-framework | `skills/translator-quality-scoring/SKILL.md` |
| IANA Language Subtag Registry | https://www.iana.org/assignments/language-subtag-registry | `skills/bcp-47-language-tags/SKILL.md` |
| CLDR picking the right language code | https://cldr.unicode.org/index/cldr-spec/picking-the-right-language-code | `skills/bcp-47-language-tags/SKILL.md` |
| ICU Transliterator (general transforms) | https://unicode-org.github.io/icu/userguide/transforms/general/ | `skills/transliteration-romanization/SKILL.md` |
| transliteration npm | https://github.com/dzcpy/transliteration | `skills/transliteration-romanization/SKILL.md` |
| MJML | https://mjml.io/ | `skills/email-localization-multi-locale/SKILL.md` |
| react-email | https://react.email/ | `skills/email-localization-multi-locale/SKILL.md` |
| Vale | https://vale.sh/ | `skills/source-content-translatability-review/SKILL.md` |
| memoQ TM leverage / AGT comparison | https://www.translatedright.com/blog/cat-tool-comparison-trados-vs-memoq-vs-phrase-vs-smartcat/ | `skills/cat-tool-memoq-trados-phrase/SKILL.md` |

These sources informed the `SOTA tool reference (June 2026)` section in `role.md`, the per-use-case mapping in `reference/SOTA_USE_CASES.md`, and the bundled SOTA skill pack names. The skill pack `SKILL.md` contents are created in Round 2 (runtime build).
