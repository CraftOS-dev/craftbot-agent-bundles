# Localization (L10n) — deep reference

This appends to `AGENT.md`. It is **not** in the agent's default context. Grep it when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "TMS selection matrix", "i18n library selection matrix", "ICU MessageFormat catalog", "CLDR plural rules reference", "BCP 47 tag examples", "hreflang correctness checklist", "RTL CSS migration playbook", "CJK font subsetting playbook", "Pseudo-localization recipe", "Translation memory hygiene playbook", "MQM 2.0 scorecard", "Subtitle CPS reference", "SOTA tool reference", "Source content translatability rubric", "Locale routing patterns".

For provenance of any section, see `SOURCES.md` in this bundle.

---

## Capability reference

Factual reference — tools, frameworks, locale data. SOUL.md does not carry these (they don't drive turn-by-turn decisions); grep here when the user asks "what should I use for X?"

### Supported TMS platforms

- **Crowdin** — free for OSS, AI translation bundled, best Git integration, widest MT engine support; safest default for dev teams
- **Lokalise** — superior iOS/Android SDKs, Figma plugin, screenshot context; best for mobile teams
- **Phrase** (formerly Memsource) — combined TMS (Phrase Strings) + CAT (Phrase TMS); SOC 2, audit logs, LSP routing; best for enterprise
- **Smartling** — enterprise-scale automation + integrations; high price floor
- **Transifex** — software-focused (UI/web/mobile), Git-integrated, continuous localization
- **Weblate** — open-source self-hosted; full data control; used by 1150+ OSS projects
- **POEditor** — lightweight, free for OSS, 1000-string free tier for SMB
- **Smartcat** — collaborative TMS + translator marketplace combined
- **GlobalLink (RWS)** — enterprise legacy, Trados ecosystem
- **Wordbee** — translation agencies + LSP-side workflow

### Supported CAT tools

- **memoQ** — most powerful concordance (wildcards, case-sensitive, source+target); memoQ AGT adaptive generative translation (2025+)
- **Trados Studio** — widest LSP supply chain; MultiTerm included on subscription
- **Phrase TMS** — cloud-native, integrated with Phrase Strings; continuous localization
- **MateCat** — free, browser-based CAT; community + commercial editions
- **OmegaT** — open-source desktop CAT; SUbtle TM features
- **Wordfast** — long-established commercial CAT
- **Smartcat (CAT mode)** — browser CAT inside the marketplace platform

### Translation engines (MT)

- **DeepL Pro / Pro API** — highest quality for European pairs (top in 65% per Intento); 100+ languages 2026
- **DeepL Document API** — preserves formatting; whole-document translate
- **Google Translate API** — 249+ languages, breadth winner; free 500K chars/month
- **Amazon Translate** — cheapest ($15/M chars); AWS integration
- **Azure Translator** — Microsoft ecosystem, custom training
- **ModernMT** — adaptive learning, $10/M standard / $40/M premium; teaches on translator corrections
- **Lilt** — adaptive NMT + human reviewer integrated workflow
- **Unbabel** — AI + human editor combined
- **memoQ AGT** — LLM-based, domain-adapted from existing TM/TB
- **OpenAI / Anthropic / Azure AI** — via Crowdin, Phrase, Lokalise AI integrations

### LSPs (Language Service Providers)

- **TransPerfect** — global enterprise scale
- **RWS** — Trados parent, enterprise legacy
- **Welocalize** — gaming, life sciences, enterprise
- **Acclaro** — marketing transcreation focus
- **Andovar** — Asian markets specialization
- **Smartcat marketplace** — direct translator hire, lightweight contract
- **Lilt** — tech + adaptive MT bundled with human review
- **Unbabel** — AI + human, support-content focus

### i18n libraries (web / app)

- **i18next + react-i18next** — largest ecosystem (3.5M+ weekly DLs); plugin-rich; default for non-Next.js React
- **react-intl (FormatJS)** — strict ICU MessageFormat compliance; smallest bundle; built on `Intl.*`
- **next-intl** — Next.js App Router + server rendering native; ICU-based; subdirectory routing built-in
- **paraglide-js (inlang)** — compiler-based, type-safe, 47 KB vs 205 KB i18next (70% reduction); `LocalizedString` branded type
- **LinguiJS** — macro-based; ICU support; mid-size bundle
- **vue-i18n** — Vue framework standard; v9 supports ICU
- **vue-i18n-next** — Vue 3 specific
- **Angular i18n (i18n + $localize)** — Angular framework standard; ICU support
- **svelte-i18n / paraglide-js Svelte** — Svelte options
- **Astro i18n + paraglide-js** — Astro Islands
- **Flutter intl / easy_localization** — Flutter mobile
- **react-native-localize** — RN locale detection
- **iOS Foundation Localizable.strings + .stringsdict** — iOS native (with `String Catalogs` from iOS 17+)
- **Android XML strings + plurals** — Android native (with App Bundle locale split)

### File format catalog

- **JSON** — flat or nested key/value; default for i18next, vue-i18n; simple but no plural metadata
- **XLIFF 1.2 / 2.0 / 2.1** — XML-based, segment-level metadata; LSP/CAT exchange standard
- **PO / POT** — Gettext; widely supported, plural rules built in
- **YAML** — Rails / static-site default; human-readable
- **ARB** — Flutter; ICU MessageFormat native
- **Stringsdict / .strings** — iOS native
- **Android XML** — Android native
- **TMX** — Translation Memory eXchange; TM interchange
- **TBX** — TermBase eXchange; glossary interchange
- **SRT / VTT / ASS** — subtitle formats

### Locale data sources

- **CLDR (Unicode Common Locale Data Repository)** — canonical locale data: plurals, date/time/number/currency, name order, address format, collation, romanization
- **ICU (International Components for Unicode)** — implementation of CLDR + transliteration + bidi
- **IANA Language Subtag Registry** — BCP 47 / RFC 5646 source of truth
- **IATE (Interactive Terminology for Europe)** — EU multilingual termbase, bulk-downloadable
- **UNTERM** — UN terminology database
- **TermBank (Tilde)** — commercial termbase aggregator
- **MultiTerm** — Trados termbase format (included on Trados subscription)

### Locale-specific concerns

- **Plural categories** — Arabic 6 (zero/one/two/few/many/other); Russian/Polish 4; English/German 2; Japanese/Chinese/Korean 1 (other only)
- **Gender** — many languages have grammatical gender on nouns/adjectives/verbs not just pronouns (DE, FR, ES, IT, RU, AR)
- **Name order** — Eastern Asian (CJK, HU) family-given; Western given-family; Hispanic with two surnames; Arabic patronymic chain
- **Address format** — DE: `Straße Nr. / PLZ Stadt`; JP: postal-prefecture-city-street; UK: street, city, postcode; US: street + city, state ZIP
- **Currency** — JPY/KRW/VND no decimals; CHF inverted thousands; EUR per-locale grouping
- **Date format** — ISO 8601 storage, `Intl.DateTimeFormat` for rendering; never hand-roll
- **Number format** — Arabic-Indic digits in Arabic; full-width vs half-width in CJK; `Intl.NumberFormat`
- **Text direction** — RTL (ar, he, ur, fa, ps); LTR everything else; bidi-isolate for mixed content

---

## TMS selection matrix

| Team profile | Recommend | Rationale |
|---|---|---|
| Dev team, OSS, mostly UI strings | **Crowdin** | Free for OSS, AI bundled, best Git integration, GitHub Action mature |
| Mobile-first (iOS + Android + RN) | **Lokalise** | OTA SDK + Figma plugin + screenshot context |
| Enterprise (SOC 2, LSP-managed, mixed content) | **Phrase** | Phrase Strings + Phrase TMS combined; audit logs; vendor routing |
| Massive scale (Fortune 500, multi-product) | **Smartling** | Automation depth + global enterprise support |
| Self-hosted / data-sovereignty | **Weblate** | OSS, runs on own hardware; 1150+ OSS users |
| SMB / lightweight | **POEditor** | Free tier, simple UX, OSS unlimited |
| Translator marketplace combined | **Smartcat** | Direct translator hire + CAT integrated |
| Existing Trados ecosystem | **GlobalLink (RWS)** | Trados-native, LSP supply pre-integrated |

---

## i18n library selection matrix

| Stack | Recommend | Rationale |
|---|---|---|
| Next.js App Router | **next-intl** | Server rendering + route-based locales native |
| React (Vite / CRA / generic) | **react-intl** (ICU strict) or **react-i18next** (ecosystem) | Pick by ICU strictness need |
| React + bundle-size critical | **paraglide-js** | 47 KB vs 205 KB i18next (70% reduction) |
| Vue 3 | **vue-i18n** v9 | Framework standard; ICU support |
| Svelte / SvelteKit | **paraglide-js** | Type-safe, compiler-based, Svelte-native |
| Astro | **paraglide-js** + Astro i18n | Islands-friendly, type-safe |
| Angular | **Angular i18n + $localize** | Framework standard |
| Flutter | **Flutter intl + intl_translation** | ARB + ICU native |
| iOS native | **String Catalogs** (iOS 17+) or **Localizable.strings + .stringsdict** | Apple native |
| Android native | **App Bundle XML strings + plurals.xml** | Google native |
| React Native | **i18next + react-native-localize** + Crowdin RN SDK (OTA) | OTA + RN ecosystem |

---

## ICU MessageFormat catalog

### Basic syntax

```
Hello, {name}!
```

### Plural (CLDR categories: zero / one / two / few / many / other)

```
{count, plural,
  =0 {No items}
  one {# item}
  other {# items}
}
```

Arabic example (uses zero/one/two/few/many/other):

```
{count, plural,
  zero {لا توجد عناصر}
  one {عنصر واحد}
  two {عنصران}
  few {# عناصر}
  many {# عنصرًا}
  other {# عنصر}
}
```

### Gender / select

```
{gender, select,
  male {He uploaded a photo.}
  female {She uploaded a photo.}
  other {They uploaded a photo.}
}
```

### Date / time / number / currency

```
You have {count, number} items as of {date, date, long} ({date, time, short}).
Total: {amount, number, ::currency/EUR}
```

### Nested

```
{numPhotos, plural,
  =0 {{gender, select, female {She has no photos.} male {He has no photos.} other {They have no photos.}}}
  =1 {{gender, select, female {She has 1 photo.} male {He has 1 photo.} other {They have 1 photo.}}}
  other {{gender, select, female {She has # photos.} male {He has # photos.} other {They have # photos.}}}
}
```

### Validation

```bash
npm i -g @formatjs/cli
formatjs lint 'lang/**/*.json'
formatjs extract 'src/**/*.{ts,tsx}' --out-file lang/en.json --id-interpolation-pattern '[sha512:contenthash:base64:6]'
formatjs compile lang/en.json --ast --out-file lang/compiled/en.json
```

---

## CLDR plural rules reference

| Language | Categories | Example range |
|---|---|---|
| English, German, Dutch, Swedish, Norwegian | one, other | 1 / 0,2,3,...|
| Spanish, Italian, Portuguese | one, many, other | 1 / 0,1M+ / 2,3,... |
| French | one, many, other | 0,1 / 0,1M+ / 2,3,... |
| Russian, Polish, Ukrainian, Croatian | one, few, many, other | 1,21,31,... / 2,3,4,22,... / 0,5-20,... |
| Arabic | zero, one, two, few, many, other | 0 / 1 / 2 / 3-10 / 11-99 / 100+ |
| Hebrew | one, two, many, other | 1 / 2 / 10,20,... / others |
| Japanese, Chinese, Korean, Vietnamese, Thai, Indonesian, Malay | other | all numbers |
| Welsh | zero, one, two, few, many, other | 0 / 1 / 2 / 3 / 6 / others |

Always provide `other` (fallback). For languages with one category (CJK), only `other` is needed but always supply it explicitly.

---

## BCP 47 tag examples

| Tag | Use | Notes |
|---|---|---|
| `en` | English (unspecified region) | Use only when region doesn't matter |
| `en-US` | US English | Default for US audience |
| `en-GB` | British English | Spellings (colour, organise), date format DD/MM/YYYY |
| `en-AU` | Australian English | Local conventions |
| `zh-Hans-CN` | Simplified Chinese, China | Use explicit `Hans` script |
| `zh-Hant-TW` | Traditional Chinese, Taiwan | Use explicit `Hant` script |
| `zh-Hant-HK` | Traditional Chinese, Hong Kong | Different vocabulary from TW |
| `pt-BR` | Brazilian Portuguese | Distinct from European |
| `pt-PT` | European Portuguese | |
| `es-ES` | European Spanish | Distinct from LATAM |
| `es-MX` | Mexican Spanish | LATAM Spanish reference |
| `es-419` | LATAM Spanish (UN region code) | Pan-LATAM fallback |
| `sr-Latn-RS` | Serbian, Latin script, Serbia | Script disambiguation |
| `sr-Cyrl-RS` | Serbian, Cyrillic script, Serbia | |
| `ar-EG` | Egyptian Arabic | MSA-EG hybrid |
| `ar-SA` | Saudi Arabic | More formal MSA |
| `ja` | Japanese | One region (Japan); region tag rarely needed |
| `ko` | Korean | Two scripts but one is dominant |
| `de-DE` | Standard German, Germany | |
| `de-AT` | Austrian German | Vocabulary differences |
| `de-CH` | Swiss German | No ß; numeric punctuation differences |
| `nb-NO` | Norwegian Bokmål | Distinct from Nynorsk |
| `fil-PH` | Filipino, Philippines | Tag `fil` not `tl` (Tagalog is the language; Filipino is the official) |

Validate with `Intl.getCanonicalLocales(['zh-Hans'])` — should return `['zh-Hans']`.

---

## hreflang correctness checklist

For every multi-locale page:

- [ ] Self-referencing tag present (e.g., page in `/de/` includes `<link rel="alternate" hreflang="de" href="/de/path">`)
- [ ] Symmetric — every page in the cluster lists every other page in the cluster
- [ ] Valid BCP 47 tags (ISO 639-1 language + optional ISO 3166-1 region)
- [ ] `x-default` present (fallback for unmatched locales)
- [ ] No mixing language-only (`en`) with language-region (`en-US`) in the same cluster
- [ ] Absolute URLs (Google requires fully-qualified)
- [ ] Returned in HTTP `Link` header OR `<head>` `<link>` OR XML sitemap (not multiple)
- [ ] Pages return 200, not redirect

### Example

```html
<head>
  <link rel="alternate" hreflang="en" href="https://example.com/" />
  <link rel="alternate" hreflang="de" href="https://example.com/de/" />
  <link rel="alternate" hreflang="fr" href="https://example.com/fr/" />
  <link rel="alternate" hreflang="ja" href="https://example.com/ja/" />
  <link rel="alternate" hreflang="ar" href="https://example.com/ar/" />
  <link rel="alternate" hreflang="x-default" href="https://example.com/" />
</head>
```

---

## RTL CSS migration playbook

### Audit step

```bash
# Find all directional CSS
grep -rE 'margin-(left|right)|padding-(left|right)|text-align:\s*(left|right)|float:\s*(left|right)|(border|left|right):\s+' src/
```

### Migration map

| Old (directional) | New (logical) |
|---|---|
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `padding-left` | `padding-inline-start` |
| `padding-right` | `padding-inline-end` |
| `text-align: left` | `text-align: start` |
| `text-align: right` | `text-align: end` |
| `border-left` | `border-inline-start` |
| `border-right` | `border-inline-end` |
| `left: 0` | `inset-inline-start: 0` |
| `right: 0` | `inset-inline-end: 0` |
| `float: left` | `float: inline-start` |
| `margin: 0 8px 0 16px` | `margin-block: 0; margin-inline: 16px 8px` |

### HTML root setup

```html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
  <head>...</head>
  <body>...</body>
</html>
```

### Direction check (not locale check)

```js
const isRTL = document.dir === 'rtl';
// NOT: const isRTL = locale === 'ar' || locale === 'he';
```

### Icons that need flipping in RTL

- Chevrons / arrows (`›` → `‹` in RTL)
- Back/forward navigation icons
- Slider direction indicators
- Reply / forward email icons

### Icons that should NOT flip

- Logos
- Brand marks
- Mathematical operators (numbers always LTR even in RTL text — Unicode BiDi algorithm handles)
- Media playback controls (play / pause / volume — universally LTR convention)
- Phone / email / location icons (no directional meaning)

### CSS for icon flipping

```css
[dir="rtl"] .chevron-right {
  transform: scaleX(-1);
}
```

---

## CJK font subsetting playbook

### Why subset

Unoptimized CJK fonts are 5-20 MB. After subset: 100-500 KB. Critical for mobile + slow networks.

### Regional variants (NOT interchangeable)

- **Noto Sans SC** — Simplified Chinese, China
- **Noto Sans TC** — Traditional Chinese, Taiwan
- **Noto Sans HK** — Traditional Chinese, Hong Kong (different from TW)
- **Noto Sans JP** — Japanese (kanji forms differ from Chinese)
- **Noto Sans KR** — Korean (Hangul + Hanja)

### Subset by used characters

```bash
# glyphhanger (recommended for web)
npm install -g glyphhanger
glyphhanger --subset=NotoSansJP.ttf --formats=woff2 --output=public/fonts/ \
  --whitelist-ranges=U+3040-309F,U+30A0-30FF,U+4E00-9FFF,U+FF00-FFEF

# pyftsubset (Python, more control)
pip install fonttools brotli
pyftsubset NotoSansSC.otf \
  --text-file=corpus.txt \
  --output-file=NotoSansSC.woff2 \
  --flavor=woff2 \
  --layout-features='*' \
  --no-hinting
```

### CSS

```css
@font-face {
  font-family: 'Noto Sans SC';
  src: url('/fonts/NotoSansSC.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
  unicode-range: U+4E00-9FFF, U+3000-303F, U+FF00-FFEF;
}

:lang(zh-Hans), [lang|="zh-Hans"] {
  font-family: 'Noto Sans SC', sans-serif;
}
```

### Google Fonts (auto-subset)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap" rel="stylesheet">
```

Google Fonts serves character-level subsets based on page content — appropriate for product pages, not advisable when offline support is needed.

### Per-script Noto + Arabic

- Arabic: Noto Sans Arabic + `font-feature-settings: "init", "medi", "fina"` for contextual forms
- Hebrew: Noto Sans Hebrew
- Thai: Noto Sans Thai (no spaces — line-break behavior differs)
- Devanagari: Noto Sans Devanagari (combining marks)

---

## Pseudo-localization recipe

### Generate pseudo-locale catalog

```bash
# pseudo-l10n npm package
npm install -g pseudo-l10n
pseudo-l10n input.json -o pseudo.json --expansion 0.35 --brackets

# Output: { "hello": "⟦Ħéllø⟧" } → expanded, accented, bracket-marked
```

### Crowdin pseudo-locale (`ach` distribution)

```bash
npm install -g @crowdin/cli
crowdin distribution add --name ach --target-language ach
# Pseudo strings auto-generated and served via OTA
```

### Lokalise `qps-ploc` test language

```bash
lokalise2 file upload --token $TOKEN --project-id $PID \
  --file=en.json --lang-iso=qps-ploc --replace-modified
```

### Run Playwright diff against pseudo

```js
// playwright.config.ts
projects: [
  { name: 'baseline', use: { locale: 'en-US' } },
  { name: 'pseudo', use: { locale: 'ach' } },
  { name: 'rtl', use: { locale: 'ar' } },
  { name: 'cjk-jp', use: { locale: 'ja' } },
  { name: 'cjk-cn', use: { locale: 'zh-Hans-CN' } },
]

// test
test('pseudo-locale no overflow', async ({ page }) => {
  await page.goto('/checkout');
  await expect(page).toHaveScreenshot('checkout-pseudo.png', { maxDiffPixelRatio: 0.02 });
});
```

### What pseudo catches

- Hard-coded strings (don't get accented → visible as plain English)
- Layout overflow (German/Finnish are 30%+ longer than English; pseudo simulates)
- String concatenation (split brackets reveal it)
- Missing translation calls (untranslated strings render as plain English)
- Encoding failures (special chars break encoding)
- Brittle plural code paths (pseudo can target plural categories)

---

## Translation memory hygiene playbook

### Leverage analysis

```
TM Leverage Categories:
- 101% in-context match  → near-zero translator cost (review only)
- 100% exact match       → low cost (verify context)
- 95-99% fuzzy match    → medium cost (edit)
- 75-94% fuzzy match    → high cost (edit substantially)
- 50-74% partial match  → reference only
- New segment           → full cost
```

Target: per-domain TM with ≥40% leverage on rolling 6-month average.

### Per-domain split

- `tm-ui.tmx` — interface strings (short, technical, frequent updates)
- `tm-marketing.tmx` — copy, headlines, CTAs (rare reuse; transcreation)
- `tm-docs.tmx` — documentation (verbose, technical)
- `tm-legal.tmx` — ToS, privacy, compliance (high formality, low change)
- `tm-email.tmx` — transactional + lifecycle templates

**Never merge across domains.** UI string "Save" should not appear as a 100% match for marketing CTA "Save 20%".

### Alignment (legacy doc → TMX)

```bash
# Okapi Rainbow (CLI: Tikal)
pipx install okapi-tools
tikal -2tmx legacy-source.docx legacy-target.docx \
  -sl en -tl de \
  -o legacy-aligned.tmx
```

### Obsolete prune

```sql
-- Pseudo-SQL for TMS API
DELETE FROM tm_segments
WHERE last_used < NOW() - INTERVAL '24 months'
  AND match_count = 0
  AND project_id IN (deprecated_projects);
```

### Concordance search

memoQ + Phrase TMS + Trados all support wildcard concordance:
- `*Save*` finds any segment containing "Save"
- Case-sensitive flag for brand terms
- Source + target search for term consistency audits

---

## MQM 2.0 scorecard

### Error categories

- **Accuracy** — Mistranslation, Omission, Addition, Untranslated, Do-not-translate violation
- **Fluency** — Grammar, Spelling, Punctuation, Register, Style, Inconsistency
- **Terminology** — Wrong term, Inconsistent term, Forbidden term
- **Locale convention** — Number format, Date format, Currency format, Address format, Name order
- **Style** — Awkwardness, Unclear reference, Inconsistency
- **Design** — Length, Truncation, Whitespace
- **Veracity** — Brand voice deviation (custom for marketing)

### Severity weights

| Severity | Weight | Definition |
|---|---|---|
| Critical | 10 | Renders content unusable / brand-damaging / legal risk |
| Major | 5 | Significantly impedes comprehension or task |
| Minor | 1 | Noticeable but doesn't impede |
| Neutral | 0 | Stylistic preference, no clear error |

### Per-1000-word error rate

```
Score = (sum of severity weights × penalty_factor) / (translated_words / 1000)

Target thresholds:
- Premium (legal, marketing, brand): ≤ 5 points / 1000 words
- Standard (UI, support, docs): ≤ 15 points / 1000 words
- Functional (internal, dev tooling): ≤ 30 points / 1000 words
```

### Scorecard CSV

```csv
translator,domain,locale,word_count,critical,major,minor,score
alice,ui,de-DE,2400,0,3,8,9.6
bob,marketing,fr-FR,1800,1,2,4,12.2
carol,legal,ja-JP,3200,0,0,2,0.6
```

### Aggregation

```python
import pandas as pd
df = pd.read_csv('mqm_scores.csv')
trend = df.groupby(['translator', 'domain']).agg(
    avg_score=('score', 'mean'),
    word_count_total=('word_count', 'sum'),
    sample_count=('locale', 'count')
).sort_values('avg_score')
```

---

## Subtitle CPS reference

Reading-speed band per script (target range for native speakers):

| Script / language family | Target CPS | Notes |
|---|---|---|
| European (Latin) | 17 (15-21) | Default; en/de/fr/es/it/pt at this band |
| Cyrillic (ru/uk) | 17-19 | Slightly higher tolerance |
| Arabic / Hebrew | 16-18 | RTL display; sub timing same |
| Japanese | 4-7 characters/sec (kanji+kana) | Effectively 13-15 CPS — denser per char |
| Chinese (CN / TW) | 5-7 chars/sec | Similar to Japanese |
| Korean | 6-8 chars/sec | Hangul reads faster than kanji |
| Thai | 14-16 CPS | No spaces; line-break care |

Line constraints:
- Max 2 lines per cue
- European: ≤ 42 chars per line
- CJK: ≤ 16 chars per line (Japanese broadcast standard)
- Min duration: ≥ 1 second per cue
- Max duration: ≤ 7 seconds per cue

### Workflow

```bash
# 1. Extract audio
ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 audio.wav

# 2. Transcribe with Whisper
pip install -U openai-whisper
whisper audio.wav --model large-v3 --output_format srt --output_dir subs/

# 3. Translate SRT per locale
# Subly / DeepL Pro / Google Translate
# preserve timing, re-validate CPS

# 4. Validate CPS
pip install srt-tools
python -c "
import srt, sys
subs = list(srt.parse(open(sys.argv[1]).read()))
for sub in subs:
    duration = (sub.end - sub.start).total_seconds()
    cps = len(sub.content) / duration if duration > 0 else 0
    if cps > 21 or cps < 5:
        print(f'CPS violation: {sub.index} = {cps:.1f}')
" subs/output.srt
```

---

## Source content translatability rubric

### Pre-translation checklist (run on source before translation)

- [ ] No idioms (`hit it out of the park`, `low-hanging fruit`)
- [ ] No ambiguous pronouns (`it`, `they` with multiple antecedents)
- [ ] No gendered nouns without explicit context (`the doctor → he/she`)
- [ ] No hardcoded units (mph, °F, feet, gallons — use locale-aware rendering)
- [ ] No string concatenation (`"You have " + count + " items"` → use ICU)
- [ ] No embedded HTML/markup in strings (separate structure from text)
- [ ] No ambiguous date formats (`03/04/25` → ISO `2025-04-03`)
- [ ] No cultural references (sports, holidays, food specific to one market)
- [ ] No abbreviations without expansion (`OOO` → `out of office`)
- [ ] No metaphors that don't translate (`circle back`, `boil the ocean`)

### Cost projection

Each issue costs:
- Concat string: +1 translator pass (split, re-stitch) = +15% time
- Idiom: requires transcreation (3x word-rate) = +200% cost on that string
- Ambiguous pronoun: requires translator query = +1 round trip
- Hardcoded unit: requires per-locale rewrite = +1 dev round trip

Cumulative: bad source → +20-40% total cost.

### Vale custom L10n style pack

```yaml
# .vale/styles/L10n/Idioms.yml
extends: existence
message: "'%s' is an idiom — replace for translatability."
ignorecase: true
tokens:
  - hit it out of the park
  - low-hanging fruit
  - circle back
  - boil the ocean
  - touch base
  - move the needle
  - drink the kool-aid
```

---

## Locale routing patterns

### Subdirectory (recommended default)

```
example.com/         → en (or x-default)
example.com/de/      → de
example.com/fr/      → fr
example.com/ja/      → ja
example.com/ar/      → ar
```

Pro: consolidates link equity, simpler to maintain, single domain
Con: server-side routing required

### Subdomain

```
example.com          → en
de.example.com       → de
fr.example.com       → fr
```

Pro: independent infrastructure per locale
Con: link equity split, more DNS work, weaker geo-signal

### ccTLD

```
example.com          → en (US implied)
example.de           → de
example.fr           → fr
example.co.jp        → ja
```

Pro: strongest geo-signal
Con: multiple domains, multiple registrations, complex ops

### Query parameter (not recommended for primary routing)

```
example.com?lang=de
```

Pro: simplest
Con: Google does not recognize as separate locale URL; bad for SEO

### Framework-native subdirectory recipes

**Next.js (App Router)**:
```bash
npm i next-intl
# app/[locale]/layout.tsx
# i18n config in middleware.ts
```

**Astro Starlight**:
```bash
npm create astro@latest -- --template starlight
# locales in astro.config.mjs
```

**Docusaurus**:
```bash
npx create-docusaurus@latest my-site classic
# i18n.locales in docusaurus.config.js
```

**MkDocs Material**:
```bash
uv add mkdocs-material mkdocs-static-i18n
# plugins.i18n in mkdocs.yml
```

---

## SOTA tool reference (June 2026)

> One H3 per tool. Each subsection points to its bundled skill pack (Round 2 creates the `SKILL.md`) + brief usage note + canonical source.

### Crowdin

**Use for:** TMS for dev teams + OSS projects; default first choice.
**Skill pack:** [`tms-setup-crowdin-lokalise-phrase`](skills/tms-setup-crowdin-lokalise-phrase/SKILL.md)
**Install:** `npm i -g @crowdin/cli`
**Quick recipe:**
```bash
crowdin init                           # create crowdin.yml
crowdin upload sources                 # push source catalogs
crowdin upload translations            # push existing translations to TM
crowdin download                       # pull translated files
# GitHub Action: crowdin/github-action@v2
```
**Source:** https://github.com/crowdin/crowdin-cli

### Lokalise

**Use for:** TMS for mobile-first teams; Figma integration; OTA SDKs (RN/iOS/Android).
**Skill pack:** [`tms-setup-crowdin-lokalise-phrase`](skills/tms-setup-crowdin-lokalise-phrase/SKILL.md)
**Install:** `npm i -g @lokalise/cli-2`
**Quick recipe:**
```bash
lokalise2 file upload --token $TOKEN --project-id $PID --file=en.json --lang-iso=en
lokalise2 file download --token $TOKEN --project-id $PID --format=json --bundle-structure='%LANG_ISO%.json'
```
**Source:** https://github.com/lokalise/lokalise-cli-2-go

### Phrase (Strings + TMS)

**Use for:** Enterprise — combined TMS + CAT, SOC 2, LSP routing.
**Skill pack:** [`tms-setup-crowdin-lokalise-phrase`](skills/tms-setup-crowdin-lokalise-phrase/SKILL.md)
**Install:** `npm i -g @phrase/cli`
**Quick recipe:**
```bash
phrase init                            # create .phrase.yml
phrase push                            # upload sources
phrase pull                            # download translations
```
**Source:** https://phrase.com/

### memoQ + memoQ AGT

**Use for:** CAT tool with deepest TM leverage UI; adaptive generative translation (2025+).
**Skill pack:** [`cat-tool-memoq-trados-phrase`](skills/cat-tool-memoq-trados-phrase/SKILL.md)
**Install:** memoQ Desktop (Windows GUI) or memoQ Cloud
**Quick recipe:**
- Create project → import TMs + TBs → enable AGT → set MT engine (DeepL/Google/AGT) → assign translator
**Source:** https://www.memoq.com/product/memoq-agt/

### Trados Studio + MultiTerm

**Use for:** Largest LSP supply chain; established CAT; MultiTerm termbase format.
**Skill pack:** [`cat-tool-memoq-trados-phrase`](skills/cat-tool-memoq-trados-phrase/SKILL.md)
**Install:** Trados Studio Desktop (Windows) or Trados Live (cloud)
**Source:** https://www.trados.com/

### DeepL Pro API

**Use for:** Highest-quality MT for European pairs; Document API preserves formatting.
**Skill pack:** [`ai-mt-deepl-pro-post-editing`](skills/ai-mt-deepl-pro-post-editing/SKILL.md)
**MCP:** `deepl-mcp`
**Install:** API key from deepl.com/pro
**Quick recipe:**
```bash
curl -X POST 'https://api.deepl.com/v2/translate' \
  -H "Authorization: DeepL-Auth-Key $DEEPL_API_KEY" \
  -d "text=Hello world&target_lang=DE&formality=more"
```
**Source:** https://www.deepl.com/docs-api

### ModernMT

**Use for:** Adaptive MT — learns from translator corrections in real time.
**Skill pack:** [`ai-mt-deepl-pro-post-editing`](skills/ai-mt-deepl-pro-post-editing/SKILL.md)
**Install:** API key from modernmt.com
**Source:** https://www.modernmt.com/api/

### Lilt

**Use for:** Adaptive NMT + human reviewer in one workflow.
**Skill pack:** [`ai-mt-deepl-pro-post-editing`](skills/ai-mt-deepl-pro-post-editing/SKILL.md)
**Install:** Lilt enterprise API key
**Source:** https://lilt.com/

### IATE (terminology)

**Use for:** EU multilingual termbase — public, bulk-downloadable; ideal prior for legal/regulatory.
**Skill pack:** [`glossary-termbase-multiterm`](skills/glossary-termbase-multiterm/SKILL.md)
**Quick recipe:**
```bash
# Bulk download — https://iate.europa.eu/download-iate
curl -L https://iate.europa.eu/em-api/entries/_search -X POST -H 'Content-Type: application/json' \
  -d '{"query": "data protection", "source": {"languages": ["en"]}, "targets": {"languages": ["de","fr","es"]}}'
```
**Source:** https://iate.europa.eu/

### MultiTerm (Trados)

**Use for:** Termbase format included with Trados subscription; memoQ + Phrase import.
**Skill pack:** [`glossary-termbase-multiterm`](skills/glossary-termbase-multiterm/SKILL.md)
**Source:** https://www.trados.com/product/multiterm/

### CLDR + ICU

**Use for:** Authoritative locale data — plurals, formats, name order, address, transliteration.
**Skill pack:** [`gender-name-address-currency-localization`](skills/gender-name-address-currency-localization/SKILL.md)
**Install:** Browser-native (`Intl.*`) or `pip install PyICU` for transliteration
**Quick recipe:**
```js
new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(1234.56);
// → "1.234,56 €"

new Intl.DateTimeFormat('ja-JP', { dateStyle: 'long' }).format(new Date());
// → "2026年6月11日"
```
**Source:** https://cldr.unicode.org/

### i18next + react-i18next

**Use for:** Largest React i18n ecosystem; plugin-rich; ICU via `i18next-icu`.
**Skill pack:** [`in-app-message-i18next-react-intl`](skills/in-app-message-i18next-react-intl/SKILL.md)
**Install:** `npm i i18next react-i18next i18next-icu i18next-browser-languagedetector`
**Source:** https://www.i18next.com/

### react-intl (FormatJS)

**Use for:** Strict ICU MessageFormat; smallest bundle; built on `Intl.*`.
**Skill pack:** [`in-app-message-i18next-react-intl`](skills/in-app-message-i18next-react-intl/SKILL.md)
**Install:** `npm i react-intl @formatjs/cli`
**Quick recipe:**
```bash
formatjs extract 'src/**/*.{ts,tsx}' --out-file lang/en.json \
  --id-interpolation-pattern '[sha512:contenthash:base64:6]'
formatjs compile lang/en.json --ast --out-file lang/compiled/en.json
```
**Source:** https://formatjs.io/

### next-intl

**Use for:** Next.js App Router + server rendering; route-based locales.
**Skill pack:** [`in-app-message-i18next-react-intl`](skills/in-app-message-i18next-react-intl/SKILL.md)
**Install:** `npm i next-intl`
**Source:** https://next-intl.dev/

### paraglide-js (inlang)

**Use for:** Compiler-based, type-safe i18n; 70% bundle reduction; `LocalizedString` branded type.
**Skill pack:** [`in-app-message-i18next-react-intl`](skills/in-app-message-i18next-react-intl/SKILL.md)
**Install:** `npm i -D @inlang/paraglide-js`
**Quick recipe:**
```bash
npx @inlang/paraglide-js@latest init        # scaffold project.inlang
npx @inlang/paraglide-js@latest compile     # → src/paraglide/messages/
```
**Source:** https://github.com/opral/paraglide-js

### pseudo-l10n

**Use for:** Generate pseudo-locale catalogs to catch i18n bugs pre-translation.
**Skill pack:** [`pseudo-localization`](skills/pseudo-localization/SKILL.md)
**Install:** `npm i -g pseudo-l10n`
**Source:** https://www.npmjs.com/package/pseudo-l10n

### Playwright (for RTL + CJK + pseudo)

**Use for:** Screenshot-diff testing across locales, directions, scripts.
**Skill pack:** [`rtl-cjk-layout-testing`](skills/rtl-cjk-layout-testing/SKILL.md) + [`pseudo-localization`](skills/pseudo-localization/SKILL.md)
**MCP:** `playwright-mcp`
**Source:** https://playwright.dev/

### Vale + L10n style pack

**Use for:** Source content translatability review; locale-specific style enforcement.
**Skill pack:** [`source-content-translatability-review`](skills/source-content-translatability-review/SKILL.md) + [`locale-qa-linguistic-functional`](skills/locale-qa-linguistic-functional/SKILL.md)
**Install:** `cli-anything` + `brew install vale` (or release tarball)
**Source:** https://vale.sh/

### Xbench (ApSIC)

**Use for:** Terminology + segment + tag QA on bilingual XLIFF/TMX.
**Skill pack:** [`locale-qa-linguistic-functional`](skills/locale-qa-linguistic-functional/SKILL.md)
**Install:** Windows desktop (free for individuals)
**Source:** https://docs.xbench.net/

### Okapi Framework (Checkmate + Tikal)

**Use for:** Cross-platform alternative to Xbench; alignment + TM export.
**Skill pack:** [`locale-qa-linguistic-functional`](skills/locale-qa-linguistic-functional/SKILL.md) + [`tm-management-leverage-optimization`](skills/tm-management-leverage-optimization/SKILL.md)
**Install:** `pipx install okapi-tools` or Rainbow desktop (Java)
**Source:** https://okapiframework.org/

### Noto Sans CJK + Arabic

**Use for:** CJK + RTL web fonts; Unicode 16.0 aligned (2024+).
**Skill pack:** [`font-selection-cjk-rtl`](skills/font-selection-cjk-rtl/SKILL.md)
**Source:** https://github.com/notofonts/noto-cjk

### Whisper (OpenAI)

**Use for:** Audio → SRT transcription before subtitle translation; large-v3 model.
**Skill pack:** [`subtitle-audio-video-localization`](skills/subtitle-audio-video-localization/SKILL.md)
**Install:** `pip install -U openai-whisper`
**Source:** https://github.com/openai/whisper

### Subtitle Edit

**Use for:** Open-source subtitle editor, 200+ formats, Whisper integration.
**Skill pack:** [`subtitle-audio-video-localization`](skills/subtitle-audio-video-localization/SKILL.md)
**Source:** https://github.com/SubtitleEdit/subtitleedit

### Subly

**Use for:** AI subtitle translation, 255 languages, timing preservation.
**Skill pack:** [`subtitle-audio-video-localization`](skills/subtitle-audio-video-localization/SKILL.md)
**Source:** https://www.getsubly.com/features/subtitle-translator

### MQM 2.0 framework

**Use for:** Translator quality scoring; error taxonomy + severity weights.
**Skill pack:** [`translator-quality-scoring`](skills/translator-quality-scoring/SKILL.md)
**Source:** https://themqm.org/

### glyphhanger + pyftsubset

**Use for:** CJK + Arabic font subsetting; 5-20 MB → 100-500 KB.
**Skill pack:** [`font-selection-cjk-rtl`](skills/font-selection-cjk-rtl/SKILL.md)
**Install:** `npm i -g glyphhanger` + `pip install fonttools brotli`
**Source:** https://github.com/zachleat/glyphhanger

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Set up Crowdin / Lokalise / Phrase" | `tms-setup-crowdin-lokalise-phrase` | Pair with `github` MCP for the Action workflow |
| "Add German / Japanese / Arabic to my app" | `in-app-message-i18next-react-intl` + `tms-setup-crowdin-lokalise-phrase` | Pseudo + RTL/CJK gates before publish |
| "Translate this catalog" | `ai-mt-deepl-pro-post-editing` + `deepl-mcp` | TM + termbase enforcement pre-publish |
| "Set up i18n in my React/Next.js/Astro app" | `in-app-message-i18next-react-intl` | Match library to framework |
| "Add plurals / gender / select" | `icu-messageformat-pluralization` | ICU MessageFormat 1; CLDR rules |
| "Test our RTL layout" | `rtl-cjk-layout-testing` + `playwright-mcp` | CSS Logical Properties first, screenshot diff |
| "Test our CJK layout" | `rtl-cjk-layout-testing` + `font-selection-cjk-rtl` | Regional Noto subset + Playwright diff |
| "Pseudo-localize" | `pseudo-localization` + `playwright-mcp` | Catches 80% of i18n bugs pre-translation |
| "Audit our translation memory" | `tm-management-leverage-optimization` | Per-domain split + leverage delta report |
| "Manage our glossary / termbase" | `glossary-termbase-multiterm` | TBX + MultiTerm + IATE prior |
| "Build a termbase from IATE" | `glossary-termbase-multiterm` | Bulk download + per-domain filter |
| "Score our translators" | `translator-quality-scoring` | MQM 2.0; per-translator + per-domain trend |
| "Localize email templates" | `email-localization-multi-locale` | MJML / react-email + ICU |
| "Translate subtitles" | `subtitle-audio-video-localization` | Whisper STT + Subly/DeepL + CPS check |
| "Set up locale routing" | `locale-routing-subdomain-subdirectory` | Subdirectory + hreflang + framework config |
| "Add hreflang" | `locale-routing-subdomain-subdirectory` | Defer deep strategy to `seo-specialist` |
| "Set BCP 47 tag" | `bcp-47-language-tags` | Validate with `Intl.getCanonicalLocales()` |
| "Transliterate / romanize" | `transliteration-romanization` | ICU Transliterator |
| "Review source for translatability" | `source-content-translatability-review` | Vale L10n pack; rewrite or hand-off to writer |
| "Set up in-context editing" | `in-context-editor-setup` | Crowdin `ach` distribution + JS snippet |
| "Set up CAT tool" | `cat-tool-memoq-trados-phrase` | memoQ / Trados / Phrase TMS |
| "Manage LSP vendor" | `lsp-vendor-management` | RFP + MQM scorecard + per-locale rate sheet |
| "Transcreate marketing copy" | `transcreation-cultural-adaptation` | Defer final creative to `marketing-agent` |

---

## Antipattern catalog

### Antipattern 1: Locale-specific RTL check

**BAD:**
```js
const isRTL = locale === 'ar' || locale === 'he';
```
**Why it's bad:** Misses Urdu, Farsi, Pashto, Yiddish. New RTL locale added → silent bug.

**GOOD:**
```js
const isRTL = document.dir === 'rtl';
// OR using Intl Locale API:
const isRTL = new Intl.Locale(locale).textInfo.direction === 'rtl';
```
**Why it's better:** Direction is a property of the script + locale; CLDR knows.

### Antipattern 2: String concatenation across plural

**BAD:**
```jsx
<span>{count} {count === 1 ? 'item' : 'items'}</span>
```
**Why it's bad:** Doesn't translate to Arabic (6 plural forms), Russian (4), Polish (4). Plural-rule logic in component.

**GOOD:**
```jsx
import { FormattedMessage } from 'react-intl';

<FormattedMessage
  id="cart.items"
  defaultMessage="{count, plural, =0 {No items} one {# item} other {# items}}"
  values={{ count }}
/>
```
**Why it's better:** ICU handles CLDR plural rules per locale. Translators write per-language forms.

### Antipattern 3: BCP 47 tag without script

**BAD:**
```js
const locale = 'zh-CN';
new Intl.NumberFormat(locale).format(1234.56);
```
**Why it's bad:** `zh-CN` is ambiguous (could be Simplified or Traditional). `Intl.getCanonicalLocales(['zh-CN'])` returns `['zh-CN']` but downstream tooling may infer differently.

**GOOD:**
```js
const locale = 'zh-Hans-CN';     // Simplified, China
const locale2 = 'zh-Hant-TW';    // Traditional, Taiwan
```
**Why it's better:** Explicit script avoids ambiguity. CLDR/ICU all canonicalize.

### Antipattern 4: hreflang without x-default

**BAD:**
```html
<link rel="alternate" hreflang="en-US" href="https://example.com/" />
<link rel="alternate" hreflang="de-DE" href="https://example.com/de/" />
```
**Why it's bad:** Missing `x-default`; missing self-references; missing other locales in cluster. Google may ignore entire cluster.

**GOOD:**
```html
<link rel="alternate" hreflang="en" href="https://example.com/" />
<link rel="alternate" hreflang="de" href="https://example.com/de/" />
<link rel="alternate" hreflang="fr" href="https://example.com/fr/" />
<link rel="alternate" hreflang="ja" href="https://example.com/ja/" />
<link rel="alternate" hreflang="ar" href="https://example.com/ar/" />
<link rel="alternate" hreflang="x-default" href="https://example.com/" />
```
**Why it's better:** Self-ref + symmetric + `x-default`. 60%+ of multilingual sites get this wrong per Google; this is the fix.

### Antipattern 5: Cross-domain TM merge

**BAD:** Single `tm.tmx` for UI, marketing, docs, legal combined.
**Why it's bad:** "Save" as UI button = imperative verb. "Save 20% today" = marketing copy. Mixed leverage poisons both — UI translator sees a marketing match and uses it; reader gets weird tone.

**GOOD:** Per-domain TMs:
- `tm-ui.tmx`
- `tm-marketing.tmx`
- `tm-docs.tmx`
- `tm-legal.tmx`

**Why it's better:** Leverage stays per-domain accurate. Translators get domain-appropriate suggestions.

### Antipattern 6: `margin-left` in 2026

**BAD:**
```css
.sidebar { margin-left: 16px; padding-right: 8px; }
```
**Why it's bad:** Broken in Arabic / Hebrew / Urdu / Farsi.

**GOOD:**
```css
.sidebar { margin-inline-start: 16px; padding-inline-end: 8px; }
```
**Why it's better:** Auto-flips in `dir="rtl"`. No JS direction check needed.

### Antipattern 7: Hardcoded date format

**BAD:**
```js
const dateStr = `${day}/${month}/${year}`;
```
**Why it's bad:** Doesn't match locale conventions. `03/04/25` ambiguous (April 3 vs March 4 vs March 25).

**GOOD:**
```js
new Intl.DateTimeFormat(locale, { dateStyle: 'long' }).format(date);
// → "3 April 2025" (en-GB), "4 March 2025" (en-US), "2025年4月3日" (ja-JP)
```
**Why it's better:** CLDR handles per-locale conventions automatically.

### Antipattern 8: Single Noto Sans CJK for all CJK

**BAD:**
```css
font-family: 'Noto Sans CJK', sans-serif;
```
**Why it's bad:** Kanji/Hanzi forms differ between SC, TC, JP, KR. Wrong subset → visible character variant.

**GOOD:**
```css
:lang(zh-Hans) { font-family: 'Noto Sans SC', sans-serif; }
:lang(zh-Hant) { font-family: 'Noto Sans TC', sans-serif; }
:lang(ja)      { font-family: 'Noto Sans JP', sans-serif; }
:lang(ko)      { font-family: 'Noto Sans KR', sans-serif; }
```
**Why it's better:** Regional character forms render correctly. Also enables per-subset font loading.

---

## Reference patterns

### Pattern: Crowdin GitHub Action workflow

```yaml
name: Crowdin Sync

on:
  push:
    branches: [main]
    paths: ['locales/en.json']
  schedule:
    - cron: '0 0 * * *'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Crowdin push + pull
        uses: crowdin/github-action@v2
        with:
          upload_sources: true
          upload_translations: false
          download_translations: true
          localization_branch_name: l10n_main
          create_pull_request: true
          pull_request_title: 'i18n: locale updates from Crowdin'
          pull_request_labels: 'i18n,crowdin'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          CROWDIN_PROJECT_ID: ${{ secrets.CROWDIN_PROJECT_ID }}
          CROWDIN_PERSONAL_TOKEN: ${{ secrets.CROWDIN_PERSONAL_TOKEN }}
```

### Pattern: next-intl App Router setup

```ts
// i18n/routing.ts
import { defineRouting } from 'next-intl/routing';
import { createNavigation } from 'next-intl/navigation';

export const routing = defineRouting({
  locales: ['en', 'de', 'fr', 'ja', 'ar', 'zh-Hans-CN'],
  defaultLocale: 'en',
  localePrefix: 'as-needed',  // /de/page, but /page for en
});

export const { Link, redirect, usePathname, useRouter } = createNavigation(routing);

// middleware.ts
import createMiddleware from 'next-intl/middleware';
import { routing } from './i18n/routing';

export default createMiddleware(routing);

export const config = {
  matcher: ['/((?!api|_next|.*\\..*).*)'],
};

// app/[locale]/layout.tsx
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';

export default async function LocaleLayout({ children, params }) {
  const messages = await getMessages();
  return (
    <html lang={params.locale} dir={params.locale === 'ar' ? 'rtl' : 'ltr'}>
      <body>
        <NextIntlClientProvider messages={messages}>
          {children}
        </NextIntlClientProvider>
      </body>
    </html>
  );
}
```

### Pattern: paraglide-js Svelte setup

```bash
npx @inlang/paraglide-js@latest init --languageTags en,de,fr,ja,ar
# → creates project.inlang/settings.json
#   creates messages/en.json, messages/de.json, ...
#   adds compile step to package.json

# Use in code:
import * as m from '$lib/paraglide/messages.js';
import { setLanguageTag } from '$lib/paraglide/runtime.js';

setLanguageTag('de');
m.hello_world({ name: 'Welt' });  // type-checked function call
```

### Pattern: ICU MessageFormat with FormatJS extraction

```bash
# 1. Annotate messages in code
# src/Components/Cart.tsx
import { FormattedMessage } from 'react-intl';

<FormattedMessage
  id="cart.itemCount"
  defaultMessage="{count, plural, =0 {No items} one {# item} other {# items}}"
  values={{ count }}
/>

# 2. Extract to JSON
formatjs extract 'src/**/*.{ts,tsx}' --out-file lang/en.json \
  --id-interpolation-pattern '[sha512:contenthash:base64:6]'

# 3. Lint for ICU correctness
formatjs lint 'lang/**/*.json'

# 4. Compile to AST (optional, faster runtime)
formatjs compile lang/en.json --ast --out-file lang/compiled/en.json
```

### Pattern: Playwright RTL + pseudo + CJK test grid

```ts
// tests/i18n-grid.spec.ts
import { test, expect } from '@playwright/test';

const locales = [
  { code: 'en-US', dir: 'ltr', label: 'baseline' },
  { code: 'ach',   dir: 'ltr', label: 'pseudo' },
  { code: 'ar',    dir: 'rtl', label: 'rtl-arabic' },
  { code: 'he',    dir: 'rtl', label: 'rtl-hebrew' },
  { code: 'ja',    dir: 'ltr', label: 'cjk-japanese' },
  { code: 'zh-Hans-CN', dir: 'ltr', label: 'cjk-simplified' },
  { code: 'zh-Hant-TW', dir: 'ltr', label: 'cjk-traditional' },
];

const pages = ['/', '/checkout', '/settings', '/profile'];

for (const loc of locales) {
  for (const pg of pages) {
    test(`${loc.label} ${pg}`, async ({ page, browserName }) => {
      await page.goto(`/${loc.code}${pg}`);
      const html = page.locator('html');
      await expect(html).toHaveAttribute('dir', loc.dir);
      await expect(html).toHaveAttribute('lang', loc.code);
      await expect(page).toHaveScreenshot(`${loc.label}-${pg.replace('/', '-')}.png`, {
        maxDiffPixelRatio: 0.02,
        fullPage: true,
      });
    });
  }
}
```

### Pattern: MJML email template per-locale

```mjml
<mjml dir="{{dir}}" lang="{{lang}}">
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Noto Sans', sans-serif" />
    </mj-attributes>
    <mj-style>
      [dir="rtl"] { text-align: right; }
    </mj-style>
    <mj-preview>{{preheader}}</mj-preview>
  </mj-head>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text>{{greeting}}, {{name}}!</mj-text>
        <mj-text>{{body}}</mj-text>
        <mj-button href="{{cta_url}}" align="{{cta_align}}">{{cta_text}}</mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

Build per locale:

```bash
# Render per-locale
for locale in en de fr ja ar; do
  npx mjml templates/welcome.mjml -o dist/welcome-$locale.html \
    --config.fileExt=.mjml \
    --juice.removeStyleTags=true
done
```

---

## Closing rules

Translation memory is asset, not commodity — manage like code. Layout is half the localization — RTL and CJK break designs that "translate" cleanly. Transcreation > translation for marketing copy. When in doubt, run the pseudo-locale gate first.

For provenance of any section above, see `SOURCES.md`. For the per-use-case SOTA mapping that drove `agent.yaml`, see `reference/SOTA_USE_CASES.md`.
