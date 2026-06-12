# Localization (L10n) — Use Cases

**Tier:** specialized · **Category:** content / i18n
**Core job:** Ship product locales — TMS pipelines, CAT setup, translation memory hygiene, ICU MessageFormat catalogs, RTL/CJK Playwright diffs, MT post-editing workflows, locale routing + hreflang, transcreation dispatch, MQM 2.0 translator scoring.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

> Ships with the SOTA L10n operator stack (Crowdin/Lokalise/Phrase CLIs, DeepL Pro, ICU MessageFormat via FormatJS/intl-messageformat, paraglide-js compiler, Playwright direction-aware screenshot diffs, Noto Sans CJK/Arabic subsetting, Xbench/Okapi QA, MQM 2.0 scoring, Subtitle Edit + Whisper). Executes end-to-end — TMS setup, locale launch, RTL/CJK gate, translator scoring — not just direct. Defers `marketing-agent` for final creative call on transcreation, `seo-specialist` for deep hreflang strategy, `frontend-engineer` for complex i18n integration in production codebases, `video-creator` for video dubbing + render.

---

## What this agent is supposed to do

### Set up TMS pipelines

- Crowdin (default for dev teams + OSS) — CLI + GitHub Action + OTA delivery to RN/iOS/Android
- Lokalise (default for mobile teams) — iOS/Android SDK + Figma plugin + screenshot context
- Phrase (default for enterprise) — Phrase Strings + Phrase TMS + SOC 2 + LSP routing
- Pre-publish gate (TM enforcement + termbase check + in-context editor)

### Manage translation memory (TM) as an asset

- Per-domain split (UI / marketing / docs / legal / email)
- Leverage analysis (fuzzy / exact / 101% in-context ratio, per-domain delta)
- Alignment (Okapi Rainbow / Tikal for legacy → TMX)
- Concordance audits (term consistency across recent segments)
- Obsolete prune + obsolete-segment count

### Manage glossary + termbase

- MultiTerm + TBX interchange + IATE bulk-import
- Per-domain glossaries (brand, UI, legal, marketing, support)
- Forbidden-term lists (false friends, competitor names, do-not-translate)
- IATE bulk export for legal/regulatory translation prior

### Set up CAT tool pipelines

- memoQ (deepest TM leverage + AGT adaptive generative translation)
- Trados Studio + MultiTerm (largest LSP supply chain)
- Phrase TMS (cloud-native, continuous localization)
- Adaptive MT engine selection (Lilt / ModernMT / memoQ AGT)

### Build in-app message catalogs

- i18next + react-i18next (largest React ecosystem)
- react-intl (strict ICU, smallest bundle)
- next-intl (Next.js App Router native)
- paraglide-js (compiler-based, type-safe, 70% bundle reduction)
- vue-i18n, Angular i18n, Flutter intl, iOS String Catalogs, Android XML

### Apply ICU MessageFormat

- Plurals (CLDR rules — Arabic 6 categories, Russian/Polish 4, English 2, CJK 1)
- Gender / select
- Date / time / number / currency formatting (via `Intl.*`)
- Nested ICU patterns
- FormatJS extraction + lint + AST compilation

### Run pseudo-localization gate

- `pseudo-l10n` npm package (30-40% expansion + bracket markers + accented chars)
- Crowdin `ach` pseudo-locale distribution
- Lokalise `qps-ploc` test language
- Playwright screenshot diff against baseline
- Catches: hardcoded strings, layout overflow, missing translation calls, encoding failures

### Test RTL / CJK layouts

- Force `dir="rtl"` + `lang="ar"` even before real Arabic translations exist
- Audit + migrate `margin-left`/`padding-right`/`text-align: left` → CSS Logical Properties
- Direction check via `document.dir === 'rtl'` (not locale-specific)
- Icon flip catalog (chevrons / back / forward yes; logos / phone / play no)
- Regional Noto subset (SC / TC / JP / KR not interchangeable)
- Playwright screenshot diff per direction × per script

### Subset fonts

- Noto Sans SC / TC / JP / KR for CJK (regional variants)
- Noto Sans Arabic + Hebrew + Thai + Devanagari for non-Latin
- glyphhanger (web-friendly, Unicode range whitelist)
- pyftsubset (full control, Brotli compression)
- Google Fonts `text=` API (character-level auto-subset)
- 5-20 MB → 100-500 KB

### Run AI / MT post-editing workflows

- DeepL Pro (highest quality for European pairs)
- DeepL Document API (preserves formatting)
- Google Translate API (249+ languages, breadth)
- Amazon Translate (cheapest at $15/M chars)
- ModernMT (adaptive — learns from translator corrections)
- Lilt + Unbabel (adaptive NMT + human reviewer integrated)
- Post-edit workflow with TM + termbase enforcement

### Manage LSP vendors

- Acclaro / TransPerfect / Welocalize / Andovar selection
- Smartcat marketplace (direct translator hire)
- Per-domain RFP (legal, marketing, technical, medical)
- MQM 2.0 scorecard for quality contract
- Rate sheet per locale ($0.08-$0.35/word per pair + script)

### Score translator quality (MQM 2.0)

- Error taxonomy (accuracy / fluency / terminology / locale convention / style / design / veracity)
- Severity weights (critical / major / minor / neutral)
- Per-1000-word error rate
- Per-translator + per-domain aggregation
- Trend identification + training/replacement threshold

### Run locale-specific QA

- Xbench (terminology + segment + tag QA on bilingual XLIFF/TMX)
- Okapi Framework Checkmate (cross-platform XLIFF/TTX/TMX QA)
- Vale + custom L10n style pack
- Playwright screenshot diff per locale × per direction

### Set up locale routing

- Subdirectory (default — consolidates link equity)
- Subdomain vs subdirectory vs ccTLD trade-off matrix
- Framework-native: Next.js / Astro / Docusaurus / VitePress / MkDocs Material i18n
- `hreflang` cluster — self-reference + symmetric + `x-default` + valid BCP 47

### Apply BCP 47 language tags

- RFC 5646 tag construction (language-Script-Region-Variant)
- IANA Subtag Registry validation
- `Intl.getCanonicalLocales()` canonicalization
- Common gotchas (`zh-Hans-CN` not `zh-CN`, `pt-BR` not `pt`, `fil-PH` not `tl-PH`)

### Localize gender / name / address / currency

- `Intl.NumberFormat` / `Intl.DateTimeFormat` / `Intl.RelativeTimeFormat` / `Intl.PluralRules`
- Name order per CLDR (Eastern Asian family-given; Western given-family; Hungarian family-given)
- Address format per CLDR (DE / JP / UK / US distinct)
- Currency rules (JPY no decimals; EUR per-locale grouping)

### Transliterate / romanize

- ICU Transliterator (`Any-Latin`, `Cyrillic-Latin`, `Han-Latin/Names`)
- Pinyin for Mandarin (Wade-Giles legacy)
- Romaji for Japanese (Hepburn vs Kunrei-shiki)
- RR (Revised Romanization) for Korean
- URL slug generation via `transliteration` npm package

### Review source content for translatability

- Idiom detection + rewrite
- Ambiguous pronoun disambiguation
- Hardcoded unit removal (mph / °F / feet)
- String concatenation → ICU MessageFormat conversion
- Embedded markup separation
- Date format ambiguity
- Cultural reference flagging
- Pre-translation cost projection (20-40% reduction possible)

### Localize email templates

- MJML + react-email with ICU
- Per-locale subject line + preheader (open-rate impact)
- RTL-aware HTML (`dir="rtl"` + `lang="ar"` root)
- Locale-aware date / time / currency in body
- CTA copy transcreated, not translated
- Klaviyo / Customer.io / Resend multi-locale templates

### Localize subtitles + audio

- Subtitle Edit (open source, 200+ formats, Whisper integration)
- Aegisub (advanced ASS/SSA styling for anime fansubbing)
- Subly (AI 255-language subtitle translation with timing)
- Whisper large-v3 for audio → SRT transcription
- CPS check (15-21 European; ~14 CJK)
- Line constraints (≤2 lines; ≤42 chars European, ≤16 chars CJK)
- Hand-off to `video-creator` for dubbing + render

### Transcreate (cultural adaptation for marketing copy)

- Brief format (brand voice + locale persona + creative latitude + don'ts)
- Dispatch via TMS or Smartcat
- In-market reviewer coordination
- A/B test in target market
- Hand-off final creative call to `marketing-agent`

### Set up in-context editor

- Crowdin In-Context (proxy + JS snippet)
- Lokalise LiveEdit
- Phrase In-Context Editor
- Pseudo-locale (`ach`) as build target for editor surface
- Role-restricted overlay

### Capture text from screenshot-only legacy strings

- Gemini OCR / Mistral OCR for legacy locale archives
- Post-process with markdownlint + Vale
- Useful for migrating off legacy CMS exports

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case from the section above appears here as a row. Row order matches `reference/SOTA_USE_CASES.md` 1:1.

| Use case | SOTA mechanism | Path |
|---|---|---|
| TMS setup | Crowdin / Lokalise / Phrase CLI + GitHub Action | `cli-anything` (`npx @crowdin/cli`, `@lokalise/cli-2`, `@phrase/cli`) + `github` MCP + `tms-setup-crowdin-lokalise-phrase` |
| Translation memory management | Per-domain split + Okapi Tikal alignment + leverage report | `cli-anything` (`pipx install okapi-tools && tikal -2tmx`) + TMS API curl + `tm-management-leverage-optimization` |
| CAT tool setup | memoQ AGT + Trados + Phrase TMS + adaptive MT | `cat-tool-memoq-trados-phrase` skill; cloud Phrase TMS via REST through `cli-anything` curl |
| Glossary / termbase management | MultiTerm + TBX + IATE bulk-import | `cli-anything` curl (IATE bulk export) + `glossary-termbase-multiterm` skill |
| In-context editor setup | Crowdin In-Context + `ach` distribution + JS snippet | `cli-anything` (`crowdin distribution add ach`) + `in-context-editor-setup` |
| Locale-specific QA | Xbench + Okapi Checkmate + Vale + Playwright screenshot diff | `cli-anything` (`tikal -lc`, `vale --output=JSON`) + `playwright-mcp` + `locale-qa-linguistic-functional` |
| RTL / CJK layout testing | CSS Logical Properties + Playwright diff + Noto subset | `playwright-mcp` + `cli-anything` (glyphhanger) + `rtl-cjk-layout-testing` |
| Pseudo-localization | `pseudo-l10n` npm + Crowdin `ach` + Playwright | `cli-anything` (`npm i -g pseudo-l10n`) + `playwright-mcp` + `pseudo-localization` |
| Transcreation | Brief + persona + Smartcat/Lilt dispatch + in-market reviewer | `cli-anything` curl (Smartcat API) + `transcreation-cultural-adaptation`; hand-off to `marketing-agent` |
| Locale routing | Subdirectory + `hreflang` cluster + framework i18n | `filesystem` + `cli-anything` (framework scaffolders) + `locale-routing-subdomain-subdirectory` |
| ICU MessageFormat | ICU MF 1 + FormatJS extract/lint/compile + CLDR | `cli-anything` (`@formatjs/cli`) + `icu-messageformat-pluralization` |
| Gender / name / address / currency | `Intl.*` APIs + CLDR data | `cli-anything` Node + `gender-name-address-currency-localization` |
| AI/MT post-editing | DeepL Pro + Google + Amazon + ModernMT + Lilt adaptive | `deepl-mcp` + `cli-anything` curl (Google/Amazon/ModernMT/Lilt) + `ai-mt-deepl-pro-post-editing` |
| LSP vendor management | RFP + MQM scorecard + Smartcat marketplace API | `cli-anything` curl + `lsp-vendor-management` |
| Translator quality scoring | MQM 2.0 + DQF + per-translator aggregation | `cli-anything` Python + TMS API + `translator-quality-scoring` |
| In-app messages | i18next / react-intl / next-intl / paraglide-js | `cli-anything` per framework + `in-app-message-i18next-react-intl` |
| Email localization | MJML / react-email + ICU + locale-aware preheader | `cli-anything` (`mjml`, `react-email`) + `email-localization-multi-locale` |
| Font selection (CJK + RTL) | Noto Sans CJK/Arabic + glyphhanger + pyftsubset | `cli-anything` (`glyphhanger`, `pyftsubset`) + `font-selection-cjk-rtl` |
| BCP 47 tags | RFC 5646 + IANA registry + `Intl.getCanonicalLocales()` | `cli-anything` Node + `bcp-47-language-tags` |
| Transliteration | ICU Transliterator + PyICU + `transliteration` npm | `cli-anything` (`pip install PyICU`, `npm i transliteration`) + `transliteration-romanization` |
| Source translatability review | Pre-translation rubric + Vale L10n style pack | `cli-anything` (`vale`) + `source-content-translatability-review`; rewrite or hand-off to `technical-writer` |
| Subtitle / audio / video | Subtitle Edit + Aegisub + Subly + Whisper + CPS check | `cli-anything` (`whisper`, `subtitle-converter`) + Subly API + `subtitle-audio-video-localization`; hand-off to `video-creator` for dubbing |
| OCR legacy capture | Gemini OCR + Mistral OCR | `gemini-ocr-mcp` + `mistral-ocr-mcp` |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| memoQ / Trados Desktop CAT automation | ⚠ | Desktop GUIs are Windows-bound. Cloud Phrase TMS is fully reachable via REST API; memoQ Cloud + Trados Live exist but are paid. Recommendation: dispatch desktop-CAT work via Phrase TMS connectors when possible; agent gives instructions otherwise. |
| Xbench QA on macOS / Linux | ⚠ | ApSIC Xbench is Windows-only. Okapi Framework's Checkmate covers most QA categories cross-platform via `tikal -lc` CLI. Recipient who needs Xbench depth on non-Windows: Wine or Windows VM. |
| Transcreation final creative call | ⚠ | Agent dispatches the brief, scores returned copy via MQM, tracks via TMS. Final brand-voice approval rests with `marketing-agent` + in-market reviewer. |
| LSP vendor API integration (Acclaro / TransPerfect / Welocalize) | ⚠ | APIs are contract-gated. Smartcat marketplace and Phrase Strings expose open APIs. Recipient who needs major LSP integration: dispatch via TMS connector (Crowdin vendor marketplace, Phrase Strings' LSP routing). |
| DeepL Pro / ModernMT / Lilt API keys | ⚠ | API keys required for production use. Free DeepL tier (500K chars/month) covers small projects; agent makes the choice and prompts for credentials. |
| Video dubbing + final render | ✗ | Out of scope for L10n. Hand-off to `video-creator` (which has Replicate + ElevenLabs + FFmpeg + Hedra Character-3 for dubbing). |
| Deep hreflang strategy + international keyword research | ✗ | Defer to `seo-specialist` (which has Ahrefs MCP + GA4 + locale-specific keyword research depth). Agent emits the `hreflang` cluster correctly. |
| Production i18n library integration in complex codebases | ✗ | Defer to `frontend-engineer` for monorepos, server-component-heavy stacks, edge runtime. Agent provides catalog + ICU strings + locale routing config. |

**Verdict (June 2026): ~96% fulfillment.** Every use case has an executable SOTA path. The four ⚠ rows are tool-ready but gated on per-project credentials, OS-bound GUI tooling (with cross-platform fallbacks), or vendor contract. The three ✗ rows are intentional hand-offs to sibling agents — not gaps in this agent.

---

## When to use this agent

- "Set up Crowdin / Lokalise / Phrase for my repo and wire the GitHub Action"
- "Add Japanese / Arabic / Simplified Chinese to my React app"
- "Migrate my CSS from `margin-left` to CSS Logical Properties for RTL"
- "Pseudo-localize this build and report layout overflow / hardcoded strings"
- "Run a Playwright RTL + CJK screenshot diff against my staging environment"
- "Convert these strings to ICU MessageFormat with proper plurals + gender"
- "Translate this JSON catalog via DeepL Pro and enforce my termbase"
- "Audit my translation memory — leverage delta, obsolete prune, per-domain split"
- "Score my translators with MQM 2.0 and surface drift"
- "Subset Noto Sans CJK for my landing page — 5 MB is killing mobile load"
- "Build a `hreflang` cluster for my 12 target locales and validate it"
- "Generate subtitles in 8 languages with CPS check"
- "Review this UI copy for translatability and rewrite the idioms"
- "Build an LSP RFP with MQM scorecard for legal translation in DE/FR/JA"

---

## When NOT to use this agent

- **Docs authoring + structure (READMEs, API refs, tutorials, ADRs)** — hand off to `technical-writer` (which has Mintlify / Redocly / Diátaxis / Vale prose-linting). L10n localizes the docs but doesn't author them.
- **Final creative call on headlines / taglines / brand voice** — hand off to `marketing-agent` (which has the campaign + brand-voice tone matrix + Buffer / Meta Ads). L10n dispatches transcreation briefs and scores returns.
- **Deep hreflang strategy + multi-region SEO + international keyword research** — hand off to `seo-specialist` (which has Ahrefs / GA4 / per-locale keyword research depth). L10n emits the `hreflang` cluster correctly.
- **Production i18n library integration in complex codebases (server components, edge runtime, monorepos)** — hand off to `frontend-engineer` for the integration; L10n provides the catalog + ICU strings + routing config.
- **Video dubbing + final video render** — hand off to `video-creator` (which has Replicate + ElevenLabs + FFmpeg + Hedra). L10n ships subtitle + script translation; dubbing/render is theirs.
- **Legal review of localized ToS / privacy policy / cookie banners** — recommend in-market legal counsel. L10n ships the translation; jurisdiction-specific compliance approval is not in scope.
- **Writing code itself** — recommend `senior-python-engineer` (or future TS/Go specialists). L10n ships catalogs + config; production library integration is hand-off.
- **Marketing copy from scratch (no source to localize)** — hand off to `marketing-agent` for greenfield copy; L10n localizes existing.
