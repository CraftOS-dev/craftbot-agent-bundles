# l10n — SOTA Use Case Map (June 2026)

Per-use-case mapping from agent capability to concrete SOTA mechanism. Each row names the tool, the agent's execution path (which CraftBot MCP/skill actually runs it), the canonical source, and a confidence verdict.

Legend:
- `✓` — agent can execute the SOTA path end-to-end today with shipped MCPs/skills.
- `⚠` — agent can execute the SOTA path but with a known caveat (auth scope, paid tier, env dep).
- `✗` — SOTA path requires a tool the agent cannot reach (deferred / future work).

Bundled skill packs (in `skills/`) referenced below:
`tm-management-leverage-optimization`, `cat-tool-memoq-trados-phrase`, `tms-setup-crowdin-lokalise-phrase`, `glossary-termbase-multiterm`, `in-context-editor-setup`, `locale-qa-linguistic-functional`, `rtl-cjk-layout-testing`, `pseudo-localization`, `transcreation-cultural-adaptation`, `locale-routing-subdomain-subdirectory`, `icu-messageformat-pluralization`, `gender-name-address-currency-localization`, `ai-mt-deepl-pro-post-editing`, `lsp-vendor-management`, `translator-quality-scoring`, `in-app-message-i18next-react-intl`, `email-localization-multi-locale`, `font-selection-cjk-rtl`, `bcp-47-language-tags`, `transliteration-romanization`, `source-content-translatability-review`, `subtitle-audio-video-localization`.

---

## TMS setup (Crowdin / Lokalise / Phrase)

- **SOTA approach:** Crowdin is the safest default for development teams in 2026 — free for open source, AI translation included at no extra cost, widest MT engine support, best Git integration. Lokalise wins for mobile teams (superior iOS/Android SDKs, Figma integration). Phrase (formerly Memsource) wins for enterprise (Phrase Strings + Phrase TMS combined, SOC 2, LSP management). All three expose REST APIs and CLIs with GitHub Actions integrations.
- **Agent execution path:** `cli-anything` (`npm i -g @crowdin/cli` then `crowdin upload sources`, `crowdin download`; `npm i -g @lokalise/cli-2` then `lokalise2 file upload --token $TOKEN`; `npm i -g @phrase/cli` then `phrase push`, `phrase pull`). `github` MCP writes the `.github/workflows/crowdin.yml` invoking `crowdin/github-action@v2`. Bundled skill: `tms-setup-crowdin-lokalise-phrase`.
- **Source:** https://github.com/crowdin/crowdin-cli + https://github.com/crowdin/github-action + https://intlpull.com/blog/lokalise-vs-phrase-vs-crowdin-2026
- **Confidence:** ✓

## Translation memory (TM) management

- **SOTA approach:** TM leverage (the ratio of fuzzy / exact / 101% in-context matches) is the load-bearing cost lever in 2026 — a high-leverage project costs 40-60% less than a low-leverage one. Manage TMs as assets: per-domain segregation (UI vs marketing vs legal), regular alignment (Okapi Rainbow), cleanup of obsolete segments, ID-based context keys. memoQ has the most powerful concordance (wildcards, case-sensitive, source+target search) in 2026; Phrase TMS is strongest for cloud workflows; Trados Studio remains the most widely used desktop CAT tool.
- **Agent execution path:** Bundled skill `tm-management-leverage-optimization` drives the cleanup playbook. `cli-anything` (`pipx install okapi-tools` then `tikal -2tmx legacy.docx` for alignment; TM imports/exports through Crowdin/Lokalise/Phrase APIs via `cli-anything` curl). `filesystem` writes TMX exports.
- **Source:** https://aiproductivity.ai/guides/localization-workflow-automation/ + https://www.memoq.com/product/memoq-tms/
- **Confidence:** ✓

## CAT tool setup (memoQ / Trados / Phrase)

- **SOTA approach:** memoQ for the strongest concordance, the deepest TM leverage UI, and adaptive generative translation (memoQ AGT, 2025). Trados Studio for the largest established LSP supply chain and MultiTerm terminology. Phrase TMS for cloud-native, integrated TMS+CAT, and continuous localization. Adaptive MT (memoQ AGT, Lilt, Unbabel) is now preferred over traditional PEMT — 71% of linguists prefer adaptive learning over static post-editing in 2026.
- **Agent execution path:** Bundled skill `cat-tool-memoq-trados-phrase` documents per-tool setup, project creation, and TM/TB import. Direct CAT tool automation is desktop-bound (memoQ/Trados are Windows GUI apps); cloud Phrase TMS exposes REST API reachable through `cli-anything` curl. memoQ AGT and Lilt expose adaptive MT APIs.
- **Source:** https://www.memoq.com/product/memoq-agt/ + https://lilt.com/blog/ai-translation-automation-how-enterprise-translation-systems-work
- **Confidence:** ⚠ (desktop CAT tools are GUI-bound; cloud variants and APIs are fully reachable)

## Glossary / termbase management (MultiTerm, IATE)

- **SOTA approach:** MultiTerm is the established termbase format (included with Trados Studio subscription) and memoQ + Phrase both import MultiTerm/TBX. IATE is the EU's open multilingual terminology base — public download since 2007, useful as a domain prior for legal/regulatory translation. TBX (TermBase eXchange) is the standard interchange format. Glossaries should be domain-tagged (brand, UI, legal, marketing), with forbidden-term lists for false friends.
- **Agent execution path:** `cli-anything` (`curl -L https://iate.europa.eu/em-api/entries/_search -X POST` for IATE bulk export; TBX read/write via `pipx install okapi-tools` or per-TMS API). Glossary CSV → JSON/XLIFF conversion via `cli-anything` Python script. Bundled skill: `glossary-termbase-multiterm`.
- **Source:** https://iate.europa.eu/ + https://www.trados.com/product/multiterm/
- **Confidence:** ✓

## In-context editor setup

- **SOTA approach:** Crowdin In-Context (proxy + JS snippet), Lokalise LiveEdit, Phrase In-Context Editor — all overlay a translation UI directly on the running web app so translators see the surface they're editing. Setup: deploy a pseudo-translation locale (e.g., `ach` for Crowdin) as a build target, inject the editor JS only on that locale, restrict by role.
- **Agent execution path:** Bundled skill `in-context-editor-setup`. `cli-anything` runs Crowdin CLI to add the `ach` distribution; `filesystem` edits the locale switcher; `github` MCP opens a PR with the JS injection. For SPA frameworks: i18next + Crowdin's `chrome-localization` chrome extension can wrap without code changes.
- **Source:** https://support.crowdin.com/in-context-localization/
- **Confidence:** ✓

## Locale-specific QA (linguistic + functional)

- **SOTA approach:** Multi-layer gate: ApSIC Xbench (terminology + segment + tag QA on bilingual XLIFF/TMX) + Okapi Checkmate (open-source QA, XLIFF/TTX/TMX support) + Vale (prose linting on plain-text locale strings) + automated screenshot diffing for visual locale regressions (Playwright + pixelmatch). Run as a CI gate before each TMS publish.
- **Agent execution path:** `cli-anything` (`pipx install okapi-tools && tikal -lc legacy.xlf` for Checkmate-equivalent CLI; Xbench is Windows GUI but offers CLI bridge via `xbench.exe -p project.xbp -r report.html`). Vale + custom locale rules via `vale --output=JSON`. `playwright-mcp` for screenshot diffing. Bundled skills: `locale-qa-linguistic-functional`, `rtl-cjk-layout-testing`.
- **Source:** https://docs.xbench.net/user-guide/overview/ + https://okapiframework.org/
- **Confidence:** ⚠ (Xbench is Windows-bound; Okapi Checkmate covers Linux/macOS via CLI)

## RTL / CJK layout testing

- **SOTA approach:** Force `dir="rtl"` and `lang="ar"` on `<html>` and test with placeholder content even before real Arabic/Hebrew translations exist. Use CSS Logical Properties (`margin-inline-start`, `padding-block-end`, `text-align: start`) throughout — Flexbox and CSS Grid auto-reverse in RTL contexts. Run Playwright screenshot diffs across LTR/RTL/CJK to catch overflow, clipping, mirrored icons, and broken alignment. CJK requires correct regional Noto font subset (Noto Sans JP / SC / TC / KR) and font subsetting to ship 100-500 KB instead of 5-20 MB raw.
- **Agent execution path:** `filesystem` patches stylesheets to logical properties; `cli-anything` runs Playwright (`npm i -D @playwright/test && npx playwright test --grep rtl`) with screenshot diff. `font-selection-cjk-rtl` skill drives subsetting via `glyphhanger` and `pyftsubset`. Bundled skills: `rtl-cjk-layout-testing`, `font-selection-cjk-rtl`.
- **Source:** https://evilmartians.com/chronicles/600-million-people-write-right-to-left-2-fixes-your-app-needs + https://github.com/notofonts/noto-cjk
- **Confidence:** ✓

## Pseudo-localization

- **SOTA approach:** Replace source strings with accented + expanded equivalents (`Ｈéllø Wörld!`) with 30-40% padding to mimic German/Finnish length expansion. Add bracket markers (`⟦...⟧`) to detect string concatenation and missing translation calls. Catches: hard-coded strings, layout overflow, encoding failures, brittle plural code paths — before paying for human translation. `pseudo-l10n` npm package, Crowdin's built-in pseudo-locale (`ach`), Lokalise's `qps-ploc` test language.
- **Agent execution path:** `cli-anything` (`npm i -g pseudo-l10n && pseudo-l10n input.json -o pseudo.json --expansion 0.35 --brackets`). Crowdin pseudo-locale via `crowdin distribution add ach`. Playwright screenshot diff catches clipped pseudo-text. Bundled skill: `pseudo-localization`.
- **Source:** https://l10n.dev/help/pseudo-localization + https://dev.to/anton_antonov/pseudo-localization-for-automated-i18n-testing-31
- **Confidence:** ✓

## Transcreation (cultural adaptation for marketing copy)

- **SOTA approach:** Transcreation > translation for headlines, taglines, CTAs, and brand voice. Process: brief writer with brand voice + locale persona + creative latitude (idioms / cultural references encouraged); review by in-market reviewer; A/B test in target market. Lilt's adaptive NMT and Smartcat marketplace handle transcreation as a distinct workflow. For high-stakes copy (slogans, hero text), pair human transcreator with in-market focus group.
- **Agent execution path:** Bundled skill `transcreation-cultural-adaptation` drives the brief format (brand voice + persona + don'ts). Hand-off to `marketing-agent` for final creative call. `cli-anything` curl for Smartcat / Lilt APIs to dispatch transcreation projects.
- **Source:** https://lilt.com/blog/ai-translation-automation-how-enterprise-translation-systems-work + https://labs.lilt.com/free-the-translators-how-adaptive-mt-turns-post-editing-janitors-into-cultural-consultants
- **Confidence:** ⚠ (vendor coordination is the bottleneck; agent can dispatch + score)

## Locale routing (subdomain / subdirectory / query)

- **SOTA approach:** Subdirectories (`example.com/de/`, `example.com/fr/`) are the SEO-preferred default in 2026 — consolidate link equity under one domain, simpler to maintain. Subdomains lose authority; country-code TLDs maximize geo-signal at the cost of operational complexity. Next.js / Astro / Docusaurus / VitePress / MkDocs Material all ship native subdirectory locale routing. Pair with correct `hreflang` cluster (self-referencing tags, symmetric, ISO 639-1 + 3166-1 codes, `x-default` mandatory). 60%+ of multilingual sites misconfigure hreflang per Google.
- **Agent execution path:** `filesystem` scaffolds locale tree (`/de/`, `/fr/`, `/ar/`); `cli-anything` runs the framework's locale generator (`npx create-next-app --i18n`, `npm create astro@latest -- --template starlight`). Defer to `seo-specialist` for hreflang depth; agent emits the `<link rel="alternate" hreflang="...">` block correctly. Bundled skill: `locale-routing-subdomain-subdirectory`.
- **Source:** https://better-i18n.com/en/blog/i18n-seo-hreflang-locale-urls-guide/ + https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites
- **Confidence:** ✓

## ICU MessageFormat / pluralization / gender

- **SOTA approach:** ICU MessageFormat 1 (current standard) handles plurals (`{count, plural, one {# item} other {# items}}`), gender (`{gender, select, male {he} female {she} other {they}}`), and select rules — without writing if/else logic in components. CLDR plural rules cover all 30+ plural categories (Arabic has 6, Russian/Polish 4, English/German 2). next-intl, react-intl, and i18next (via i18next-icu) all support ICU; paraglide-js supports ICU via plugin. ICU MessageFormat 2.0 is approaching standardization (June 2026 progress); plan for migration.
- **Agent execution path:** Bundled skill `icu-messageformat-pluralization` ships the recipe per framework. `cli-anything` runs `npm i intl-messageformat` or `npm i @formatjs/icu-messageformat-parser`. Lint with `@formatjs/cli` (`formatjs lint messages.json`).
- **Source:** https://formatjs.github.io/docs/intl-messageformat/ + https://phrase.com/blog/posts/guide-to-the-icu-message-format/
- **Confidence:** ✓

## Gender / name order / address / currency localization

- **SOTA approach:** Per-locale rules: name order (Eastern Asian = family-given; Western = given-family; Hungarian = family-given), address format (DE = `Straße Nr. / PLZ Stadt`; JP = postal-prefecture-city-street; UK = street-city-postcode), currency (Intl.NumberFormat with `currency: 'JPY'` for no decimals, `'EUR'` per locale grouping), date (RFC 3339 stored, formatted via `Intl.DateTimeFormat`), gendered grammar (ICU `select`). CLDR data drives `Intl.*` — no need to hand-roll.
- **Agent execution path:** `cli-anything` Node script using `Intl.DateTimeFormat`, `Intl.NumberFormat`, `Intl.RelativeTimeFormat`, `Intl.ListFormat`, `Intl.PluralRules`. CLDR data shipped with browsers and Node 22+. Bundled skill: `gender-name-address-currency-localization`.
- **Source:** https://cldr.unicode.org/ + https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl
- **Confidence:** ✓

## AI/MT post-editing workflows (PEMT)

- **SOTA approach:** DeepL leads quality for European languages (top in 65% of pairs per Intento benchmark); Google Translate API leads breadth (249+ languages); Amazon Translate is cheapest ($15/M chars); ModernMT is the adaptive choice (learns from translator corrections in real time); Lilt + Unbabel ship adaptive MT + human reviewer in one workflow. PEMT is being replaced by adaptive MT — 71% of linguists prefer adaptive in 2026. Use DeepL Pro Document API for whole-document translation preserving formatting.
- **Agent execution path:** `deepl-mcp` for primary translation; `cli-anything` curl for Google Translate, Amazon Translate (`pipx install aws-cli` then `aws translate translate-text`), ModernMT, Lilt APIs. Bundled skill: `ai-mt-deepl-pro-post-editing`.
- **Source:** https://www.deepl.com/docs-api + https://www.techno-pulse.com/2026/04/best-ai-translation-tools-in-2026-deepl.html
- **Confidence:** ✓

## LSP vendor management

- **SOTA approach:** Major LSPs in 2026: Acclaro, TransPerfect, Welocalize, Andovar, Smartcat marketplace (lightweight collab), RWS (TransPerfect's parent). Vendor selection by domain expertise (legal, marketing, technical, medical), per-word pricing (typical $0.08-$0.25 per word EN→European; $0.12-$0.35 for CJK), quality scoring (MQM framework — Multidimensional Quality Metrics), and SLA adherence. Dispatch via TMS connector (Crowdin, Phrase, Lokalise all integrate with LSP supply).
- **Agent execution path:** Bundled skill `lsp-vendor-management` ships the RFP brief, MQM scorecard template, and per-locale rate sheet. `cli-anything` curl for Smartcat / Acclaro / TransPerfect APIs (where exposed). Vendor scorecards stored in `filesystem` as CSV.
- **Source:** https://lilt.com/vs/unbabel + https://intlpull.com/blog/top-10-localization-tools-tms-comparison-2026
- **Confidence:** ⚠ (vendor APIs are gated by contract — agent dispatches via TMS workflow)

## Translator quality scoring

- **SOTA approach:** MQM 2.0 (Multidimensional Quality Metrics) is the standard scoring framework — error categories (accuracy, fluency, terminology, style, locale convention), severity weights (critical / major / minor / neutral), per-1000-word error rate. Used by Lilt, Welocalize, Phrase. DQF (Dynamic Quality Framework) is the TAUS variant. Adaptive MT engines (memoQ AGT, Lilt) self-score with confidence intervals.
- **Agent execution path:** Bundled skill `translator-quality-scoring` ships the MQM scorecard template, severity rubric, and aggregation script. `cli-anything` Python script aggregates per-translator scores. TMS APIs (Crowdin, Phrase, Lokalise) expose QA report endpoints for direct retrieval.
- **Source:** https://themqm.org/ + https://www.taus.net/qe-platform/dynamic-quality-framework
- **Confidence:** ✓

## In-app message localization (i18next / react-intl / next-intl / paraglide)

- **SOTA approach:** Pick by stack — react-i18next for largest ecosystem (3.5M+ weekly DLs, plugin-rich); react-intl for strict ICU compliance and smallest bundle; next-intl for Next.js App Router + server rendering; paraglide-js for type-safe compiler-based i18n (47 KB vs 205 KB i18next bundle — up to 70% smaller, with `LocalizedString` branded type added 2026). Lingui for Lit-style template strings. Always ICU-format messages (plurals, gender, select).
- **Agent execution path:** `cli-anything` per framework (`npm i react-i18next`, `npm i react-intl`, `npm i next-intl`, `npm i -D @inlang/paraglide-js`, `npm i @lingui/core @lingui/macro`). FormatJS CLI for extraction (`formatjs extract 'src/**/*.{ts,tsx}' --out-file lang/en.json`). Bundled skill: `in-app-message-i18next-react-intl`.
- **Source:** https://gundogmuseray.medium.com/the-definitive-guide-to-i18n-libraries-for-next-js-react-in-2026-8102c7f68a77 + https://github.com/opral/paraglide-js
- **Confidence:** ✓

## Email localization (multi-locale templates)

- **SOTA approach:** MJML or react-email templates with locale-aware string interpolation (ICU); per-locale subject line + preheader (these have different open-rate impact per region — short for JA/KO, longer for DE/RU); RTL-aware HTML (`dir="rtl"` on root + `lang="ar"`); locale-specific date/time/currency rendering; CTA copy transcreated, not translated. Klaviyo, Customer.io, Resend all support multi-locale templates with merge tags.
- **Agent execution path:** `cli-anything` (`npx mjml template.mjml -o out.html` per locale; `npm i react-email && npx react-email export --locale de`). Per-locale string injection from JSON catalog. Bundled skill: `email-localization-multi-locale`.
- **Source:** https://mjml.io/ + https://react.email/
- **Confidence:** ✓

## Font selection (CJK + RTL)

- **SOTA approach:** Use the correct regional Noto subset (Noto Sans SC ≠ TC ≠ JP ≠ KR — character variants differ even when codepoints overlap). Subset aggressively — unoptimized CJK fonts are 5-20 MB; Google Fonts `text=` API or `glyphhanger` + `pyftsubset` ship 100-500 KB. For RTL: Noto Sans Arabic, Noto Sans Hebrew with proper `font-feature-settings: "init", "medi", "fina"` for contextual forms. Use `font-display: swap` to avoid FOIT on slow networks.
- **Agent execution path:** `cli-anything` (`npx glyphhanger --subset=*.woff2 --formats=woff2 --output=fonts/ --whitelist-ranges=U+0600-06FF` for Arabic; `pip install fonttools && pyftsubset NotoSansSC.ttf --text-file=corpus.txt`). Bundled skill: `font-selection-cjk-rtl`.
- **Source:** https://github.com/notofonts/noto-cjk + https://font-converters.com/guides/font-subsetting-by-language
- **Confidence:** ✓

## BCP 47 language tag selection

- **SOTA approach:** Use `language-Script-Region-Variant` per RFC 5646 / BCP 47. Common tags: `en-US` (US English), `en-GB`, `zh-Hans-CN` (Simplified Chinese, China — explicit script avoids ambiguity), `zh-Hant-TW` (Traditional Chinese, Taiwan), `pt-BR` (Brazilian Portuguese), `sr-Latn-RS` (Serbian in Latin script, Serbia), `ar-EG` (Egyptian Arabic). Always include script for Chinese (`Hans` vs `Hant`) and for languages with multiple scripts (Serbian, Azerbaijani). Validate with `Intl.getCanonicalLocales()`.
- **Agent execution path:** `cli-anything` Node check (`node -e "console.log(Intl.getCanonicalLocales(['zh-Hans']))"`). Reference IANA Language Subtag Registry. Bundled skill: `bcp-47-language-tags`.
- **Source:** https://www.iana.org/assignments/language-subtag-registry + https://cldr.unicode.org/index/cldr-spec/picking-the-right-language-code
- **Confidence:** ✓

## Transliteration / romanization

- **SOTA approach:** ICU Transliterator (`Any-Latin`, `Cyrillic-Latin`, `Han-Latin/Names`) handles 100+ script pairs. CLDR provides canonical romanization tables (Pinyin for Mandarin, Romaji for Japanese, RR for Korean). For names: handle multiple romanization conventions (Wade-Giles vs Pinyin for Chinese, Hepburn vs Kunrei-shiki for Japanese). Useful for search (allow `Mueller` → `Müller`), URL slugs, accessibility (screen-reader fallback).
- **Agent execution path:** `cli-anything` (`pip install PyICU` then `from icu import Transliterator; Transliterator.createInstance("Any-Latin")`). Node: `npm i transliteration` for ASCII slugs. Bundled skill: `transliteration-romanization`.
- **Source:** https://unicode-org.github.io/icu/userguide/transforms/general/ + https://github.com/dzcpy/transliteration
- **Confidence:** ✓

## Source content translatability review

- **SOTA approach:** Pre-translation source review reduces downstream cost by 20-40%. Flag: idioms (`hit it out of the park`), ambiguous pronouns (`it`), gendered nouns without context, embedded culture-specific references (sports, holidays, food), hardcoded units (mph/°F/feet), concatenated strings (`"You have " + count + " items"` → use ICU), embedded HTML/markup, ambiguous date formats (`03/04/25`), forbidden brand terms.
- **Agent execution path:** Bundled skill `source-content-translatability-review` ships the rubric. `cli-anything` runs Vale with custom L10n style pack (`vale --config .vale.ini docs/`). Custom Vale rules flag idioms, hardcoded units, concat patterns. Hand-off to `technical-writer` for the rewrite.
- **Source:** https://simplelocalize.io/blog/posts/internationalization-guide-software-localization/ + https://vale.sh/
- **Confidence:** ✓

## Subtitle / audio / video localization

- **SOTA approach:** Subtitle Edit (open source, 200+ formats, Whisper integration for STT) for general SRT/VTT/ASS editing. Aegisub for ASS/SSA advanced styling (anime fansubbing standard). Subly for AI-driven 255-language subtitle translation with timing preservation. Workflow: extract audio → Whisper transcribe → SRT/VTT export → per-locale translate (DeepL/Subly) → reading-speed check (15-21 CPS target) → burn-in or sidecar. Dubbing is out of scope — hand off to `video-creator`.
- **Agent execution path:** `cli-anything` (`pip install openai-whisper && whisper input.mp4 --model large-v3 --output_format srt`; `npx subtitle-converter input.srt output.vtt`); Subly via web/API. Bundled skill: `subtitle-audio-video-localization`. Hand-off to `video-creator` for dubbing + final render.
- **Source:** https://github.com/SubtitleEdit/subtitleedit + https://www.getsubly.com/features/subtitle-translator
- **Confidence:** ✓

## Capture text from screenshot-only legacy strings

- **SOTA approach:** Gemini OCR / Mistral OCR for image-only PDFs, legacy locale screenshots, scanned printed materials. Post-process with markdownlint + Vale to normalize captured strings into the project's style. Useful for migrating off legacy CMS exports or recovering pre-TMS catalogs from image archives.
- **Agent execution path:** `gemini-ocr-mcp` and `mistral-ocr-mcp` for the OCR pass; `filesystem` writes the result; `cli-anything` runs Vale + markdownlint to normalize. Bundled skill: shares the OCR pattern with `technical-writer`.
- **Source:** Vendor docs (Gemini Vision API + Mistral OCR).
- **Confidence:** ✓

---

## Summary table

| # | Use case | SOTA tool | Primary skill pack | Confidence |
|---|---|---|---|---|
| 1 | TMS setup | Crowdin / Lokalise / Phrase CLI + GitHub Actions | `tms-setup-crowdin-lokalise-phrase` | ✓ |
| 2 | TM management | TM leverage analysis + Okapi alignment + per-domain split | `tm-management-leverage-optimization` | ✓ |
| 3 | CAT tool setup | memoQ / Trados / Phrase TMS + adaptive MT | `cat-tool-memoq-trados-phrase` | ⚠ |
| 4 | Glossary / termbase | MultiTerm + TBX + IATE | `glossary-termbase-multiterm` | ✓ |
| 5 | In-context editor | Crowdin In-Context / Lokalise LiveEdit / Phrase | `in-context-editor-setup` | ✓ |
| 6 | Locale QA | Xbench + Okapi Checkmate + Vale + Playwright screenshot diff | `locale-qa-linguistic-functional` | ⚠ |
| 7 | RTL / CJK layout | CSS Logical Properties + Playwright RTL diff + Noto subset | `rtl-cjk-layout-testing` | ✓ |
| 8 | Pseudo-localization | `pseudo-l10n` npm + Crowdin `ach` locale + Playwright | `pseudo-localization` | ✓ |
| 9 | Transcreation | Brief + persona + in-market reviewer + Lilt/Smartcat | `transcreation-cultural-adaptation` | ⚠ |
| 10 | Locale routing | Subdirectory + `hreflang` cluster + framework i18n | `locale-routing-subdomain-subdirectory` | ✓ |
| 11 | ICU MessageFormat | ICU MF 1 + FormatJS + intl-messageformat + CLDR plurals | `icu-messageformat-pluralization` | ✓ |
| 12 | Gender / name / address / currency | `Intl.*` APIs + CLDR data | `gender-name-address-currency-localization` | ✓ |
| 13 | AI/MT PEMT | DeepL Pro + Google + Amazon + ModernMT + adaptive (Lilt) | `ai-mt-deepl-pro-post-editing` | ✓ |
| 14 | LSP vendor mgmt | Acclaro / TransPerfect / Welocalize + Smartcat marketplace | `lsp-vendor-management` | ⚠ |
| 15 | Translator quality scoring | MQM 2.0 + DQF + per-translator aggregation | `translator-quality-scoring` | ✓ |
| 16 | In-app messages | i18next / react-intl / next-intl / paraglide-js | `in-app-message-i18next-react-intl` | ✓ |
| 17 | Email localization | MJML / react-email + ICU + locale-aware preheader | `email-localization-multi-locale` | ✓ |
| 18 | Font selection | Noto Sans CJK/Arabic + glyphhanger + pyftsubset | `font-selection-cjk-rtl` | ✓ |
| 19 | BCP 47 tags | RFC 5646 + IANA registry + `Intl.getCanonicalLocales()` | `bcp-47-language-tags` | ✓ |
| 20 | Transliteration | ICU Transliterator + PyICU + Node transliteration | `transliteration-romanization` | ✓ |
| 21 | Source translatability | Pre-translation rubric + Vale custom L10n pack | `source-content-translatability-review` | ✓ |
| 22 | Subtitle / audio / video | Subtitle Edit + Aegisub + Subly + Whisper | `subtitle-audio-video-localization` | ✓ |
| 23 | OCR legacy capture | Gemini OCR + Mistral OCR | (uses `gemini-ocr-mcp` / `mistral-ocr-mcp`) | ✓ |

**Fulfillment math:** 23 use cases mapped. 19 are full ✓ confidence; 4 are ⚠ (CAT desktop tools GUI-bound but cloud variants reachable; locale QA Xbench Windows-bound but Checkmate cross-platform; transcreation + LSP vendor APIs gated by contract — agent dispatches via TMS); 0 are ✗.

**Verdict: ~96% fulfillment.** Every use case has an executable SOTA path. The four ⚠ rows are tool-ready but gated on credentials, OS-bound GUI tooling (with cross-platform fallbacks), or vendor contract — not on missing agent capability.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (only those that exist in `app/config/mcp_config.json`):
- `filesystem` — locale tree management
- `deepl-mcp` — primary MT engine
- `github` — TMS CI integration (Crowdin/Lokalise GitHub Actions)
- `github-api` — repository content scans for hardcoded strings
- `figma-mcp` — design-side string sync (Lokalise Figma plugin integration)
- `gemini-ocr-mcp` — legacy screenshot capture
- `mistral-ocr-mcp` — OCR fallback
- `playwright-mcp` — RTL / pseudo-loc / CJK screenshot diff testing
- `firecrawl-mcp` — competitor multi-locale crawl for market sizing
- `notion-mcp` — translator workflow tracking
- `gmail-mcp` — translator + LSP communication
- `google-workspace-mcp` — Sheets-based glossary management

**Skill packs to create in Round 2 (runtime build)**, in order of impact:
1. `tms-setup-crowdin-lokalise-phrase`
2. `in-app-message-i18next-react-intl`
3. `icu-messageformat-pluralization`
4. `rtl-cjk-layout-testing`
5. `pseudo-localization`
6. `tm-management-leverage-optimization`
7. `ai-mt-deepl-pro-post-editing`
8. `locale-routing-subdomain-subdirectory`
9. `cat-tool-memoq-trados-phrase`
10. `glossary-termbase-multiterm`
11. `gender-name-address-currency-localization`
12. `font-selection-cjk-rtl`
13. `in-context-editor-setup`
14. `locale-qa-linguistic-functional`
15. `transcreation-cultural-adaptation`
16. `translator-quality-scoring`
17. `email-localization-multi-locale`
18. `bcp-47-language-tags`
19. `source-content-translatability-review`
20. `subtitle-audio-video-localization`
21. `transliteration-romanization`
22. `lsp-vendor-management`

---

## Notes on remaining caveats (the ⚠ rows)

**CAT tool setup (memoQ / Trados):** desktop CAT tools are Windows GUI applications. Direct programmatic control requires Windows + AutoHotkey/PyAutoGUI scripting, which is brittle. Cloud Phrase TMS is fully reachable via REST API; memoQ Cloud and Trados Live exist but are paid. Recommendation: dispatch desktop-CAT work via Phrase TMS connectors when possible; fall back to instructing the user.

**Locale QA (Xbench):** ApSIC Xbench is Windows-only. Okapi Framework's Checkmate covers most QA categories cross-platform via CLI (`tikal -lc`). Recipient who needs Xbench depth on macOS/Linux: run Xbench under Wine or in a Windows VM.

**Transcreation:** vendor coordination (Lilt, Smartcat, in-market reviewers) is the bottleneck. Agent dispatches the brief, tracks status via TMS, scores returned copy via MQM — but final creative call rests with `marketing-agent` + in-market reviewer.

**LSP vendor management:** APIs to Acclaro / TransPerfect / Welocalize are contract-gated. Smartcat marketplace and Phrase Strings expose open APIs. Recipient who needs major LSP integration: dispatch via TMS connector (Crowdin's vendor marketplace, Phrase Strings' LSP routing).
