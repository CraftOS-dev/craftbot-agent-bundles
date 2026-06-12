---
name: bcp-47-language-tags
description: BCP 47 / RFC 5646 language tag selection — language-Script-Region-Variant. CLDR locale registry, IANA subtag registry, Intl.getCanonicalLocales validation. Use when the user asks "what locale code", "zh-CN vs zh-Hans-CN", "BCP 47", "locale tag", "language code", or builds a language picker.
---

# BCP 47 Language Tags

BCP 47 (RFC 5646) is the standard for locale identifiers everywhere — `Accept-Language`, `lang=` attribute, `hreflang`, `Intl.*` APIs, Crowdin/Lokalise/Phrase project codes, iOS/Android locale folders. Get the tag wrong and the entire locale's CLDR data falls back to a wrong default.

Form: `language[-Script][-Region][-Variant][-Extension][-PrivateUse]`. Always use canonical (lowercase language, Titlecase script, UPPERCASE region).

## When to use

- Picking the tag for a new locale (especially Chinese, Serbian, Portuguese, Spanish).
- Resolving "the German team says `de-DE` but Crowdin shows `de`" ambiguity.
- Validating user-submitted locale codes before saving.
- Setting `<html lang="...">`, `hreflang`, or `Accept-Language` fallback chains.
- Mapping legacy / vendor tags (e.g., `iw` → `he`, `zh-CN` → `zh-Hans-CN`).
- Translating an OS locale string (`pt_BR.UTF-8`) into a web BCP 47 tag (`pt-BR`).

Trigger phrases: "BCP 47", "RFC 5646", "language tag", "locale code", "zh-Hans", "zh-Hant", "pt-BR vs pt-PT", "language subtag registry", "getCanonicalLocales".

## Setup

```bash
# No install needed for browser / Node 18+
node -e "console.log(Intl.getCanonicalLocales(['zh-Hans']))"
# → [ 'zh-Hans' ]

# IANA Language Subtag Registry (authoritative)
curl -sL https://www.iana.org/assignments/language-subtag-registry > registry.txt
wc -l registry.txt   # ~10000 entries; one block per subtag

# CLDR locale list
curl -sL https://raw.githubusercontent.com/unicode-org/cldr-json/main/cldr-json/cldr-core/availableLocales.json > cldr-locales.json
```

Auth/env: none required.

## Tag structure

| Segment | Source | Example | Case |
|---|---|---|---|
| Language | ISO 639-1 (2-letter) or ISO 639-3 (3-letter) | `en`, `zh`, `cmn`, `yue` | lowercase |
| Script | ISO 15924 (4-letter) | `Hans`, `Hant`, `Latn`, `Cyrl`, `Arab` | Titlecase |
| Region | ISO 3166-1 alpha-2 OR UN M.49 (3-digit) | `US`, `CN`, `419` (LATAM) | UPPERCASE |
| Variant | Registered variant | `valencia`, `tarask`, `1996` | lowercase |
| Extension | `u-` (Unicode), `t-` (transform) | `u-ca-buddhist`, `u-nu-arab` | lowercase |
| Private use | `x-` prefix | `x-internal`, `x-test` | lowercase |

## Canonical tags (memorize)

| Tag | Use | Notes |
|---|---|---|
| `en` | English (unspecified region) | Use only when region irrelevant; otherwise pick `en-US` / `en-GB` |
| `en-US` | US English | Default for US audience; m/d/y dates, USD |
| `en-GB` | British English | colour/organise, d/m/y, GBP |
| `en-AU` | Australian English | local conventions |
| `en-CA` | Canadian English | metric + d/m/y; co-exists with `fr-CA` |
| `en-IN` | Indian English | INR `Intl` lakh/crore grouping |
| `zh-Hans-CN` | Simplified Chinese, China | ALWAYS include `Hans` script |
| `zh-Hant-TW` | Traditional Chinese, Taiwan | Different from HK |
| `zh-Hant-HK` | Traditional Chinese, Hong Kong | Different glyphs + vocab from TW |
| `zh-Hans-SG` | Simplified Chinese, Singapore | Singapore-specific |
| `pt-BR` | Brazilian Portuguese | Distinct from European |
| `pt-PT` | European Portuguese | |
| `es-ES` | European Spanish | Use ud., vosotros |
| `es-MX` | Mexican Spanish | LATAM reference |
| `es-419` | LATAM Spanish (UN M.49 region) | Pan-LATAM fallback |
| `es-US` | US Spanish | US-specific tag |
| `sr-Latn-RS` | Serbian, Latin script | Script-mandatory |
| `sr-Cyrl-RS` | Serbian, Cyrillic script | |
| `ar-EG` | Egyptian Arabic | MSA-EG hybrid |
| `ar-SA` | Saudi Arabic | More formal MSA |
| `ar` | Modern Standard Arabic | Pan-Arab fallback |
| `ja` | Japanese | One region (JP); skip `-JP` |
| `ko` | Korean | One region (KR) |
| `de-DE` | Standard German | |
| `de-AT` | Austrian German | Vocabulary differences |
| `de-CH` | Swiss German | No ß; numeric punctuation differs |
| `nb-NO` | Norwegian Bokmål | NOT `no` — `no` is macro tag |
| `nn-NO` | Norwegian Nynorsk | |
| `fil-PH` | Filipino, Philippines | `fil` not `tl` (Tagalog) |
| `iw` → `he` | Hebrew (legacy → current) | Map `iw` to `he` on input |
| `in` → `id` | Indonesian (legacy → current) | Map `in` to `id` |
| `ji` → `yi` | Yiddish | Map `ji` to `yi` |

## Common recipes

### Recipe 1: Validate a tag

```js
// Browser / Node
function isValidBCP47(tag) {
  try {
    return Intl.getCanonicalLocales([tag])[0] === tag.toString();
  } catch {
    return false;
  }
}

isValidBCP47('zh-Hans-CN');  // true
isValidBCP47('zh_CN');       // false — underscore not allowed
isValidBCP47('xx-YY');       // true (syntactically valid) — does not check CLDR coverage
```

### Recipe 2: Canonicalize a tag

```js
Intl.getCanonicalLocales(['EN-us']);        // ['en-US']
Intl.getCanonicalLocales(['ZH-hans-cn']);   // ['zh-Hans-CN']
Intl.getCanonicalLocales(['iw']);           // ['he'] — legacy mapping
Intl.getCanonicalLocales(['cmn-Hans-CN']);  // ['cmn-Hans-CN'] — preserves 3-letter
```

### Recipe 3: Parse / build with Intl.Locale

```js
const loc = new Intl.Locale('zh-Hant-HK');
loc.language;   // 'zh'
loc.script;     // 'Hant'
loc.region;     // 'HK'
loc.baseName;   // 'zh-Hant-HK'

// Build
const built = new Intl.Locale('zh', { script: 'Hans', region: 'CN' });
built.toString();   // 'zh-Hans-CN'

// Get text direction (no manual list)
new Intl.Locale('ar').textInfo.direction;        // 'rtl'
new Intl.Locale('he').textInfo.direction;        // 'rtl'
new Intl.Locale('zh-Hans-CN').textInfo.direction; // 'ltr'
```

### Recipe 4: Map legacy OS / vendor locales

```js
const LEGACY = {
  // POSIX → BCP 47
  'en_US.UTF-8': 'en-US',
  'pt_BR.UTF-8': 'pt-BR',
  'zh_CN.UTF-8': 'zh-Hans-CN',
  'zh_TW.UTF-8': 'zh-Hant-TW',
  // Legacy ISO 639-1
  'iw':    'he',
  'in':    'id',
  'ji':    'yi',
  'jw':    'jv',
  // Ambiguous Chinese
  'zh-CN': 'zh-Hans-CN',
  'zh-TW': 'zh-Hant-TW',
  'zh-HK': 'zh-Hant-HK',
  'zh-SG': 'zh-Hans-SG',
};
function normalize(input) {
  const cleaned = input.replace(/_/g, '-').split('.')[0];
  return LEGACY[cleaned] || Intl.getCanonicalLocales([cleaned])[0];
}
```

### Recipe 5: Language picker UI

```js
const SUPPORTED = [
  { tag: 'en',          name: 'English' },
  { tag: 'de-DE',       name: 'Deutsch (Deutschland)' },
  { tag: 'fr-FR',       name: 'Français (France)' },
  { tag: 'fr-CA',       name: 'Français (Canada)' },
  { tag: 'pt-BR',       name: 'Português (Brasil)' },
  { tag: 'pt-PT',       name: 'Português (Portugal)' },
  { tag: 'es-ES',       name: 'Español (España)' },
  { tag: 'es-419',      name: 'Español (Latinoamérica)' },
  { tag: 'zh-Hans-CN',  name: '简体中文 (中国)' },
  { tag: 'zh-Hant-TW',  name: '繁體中文 (台灣)' },
  { tag: 'zh-Hant-HK',  name: '繁體中文 (香港)' },
  { tag: 'ja',          name: '日本語' },
  { tag: 'ko',          name: '한국어' },
  { tag: 'ar-EG',       name: 'العربية (مصر)' },
  { tag: 'ar-SA',       name: 'العربية (السعودية)' },
  { tag: 'he',          name: 'עברית' },
];

// Show endonym (Intl.DisplayNames if you don't want to maintain manually)
const dn = new Intl.DisplayNames(['en'], { type: 'language' });
dn.of('zh-Hans-CN');    // "Chinese (Simplified, China)"

const dnLocal = (tag) => new Intl.DisplayNames([tag], { type: 'language' }).of(tag);
dnLocal('ja');          // "日本語"
```

### Recipe 6: Accept-Language negotiation

```js
function pickLocale(acceptLanguage, supported) {
  const requested = acceptLanguage
    .split(',')
    .map(s => {
      const [tag, q] = s.trim().split(';q=');
      return { tag: Intl.getCanonicalLocales([tag])[0], q: parseFloat(q) || 1.0 };
    })
    .sort((a, b) => b.q - a.q);

  for (const req of requested) {
    // Exact match
    if (supported.includes(req.tag)) return req.tag;
    // Language match (en-US → en if en supported)
    const lang = new Intl.Locale(req.tag).language;
    const langMatch = supported.find(s => new Intl.Locale(s).language === lang);
    if (langMatch) return langMatch;
  }
  return supported[0];   // x-default fallback
}

pickLocale('zh-CN,zh;q=0.9,en;q=0.8',
  ['zh-Hans-CN', 'zh-Hant-TW', 'en']);   // 'zh-Hans-CN'
```

### Recipe 7: Fallback chain (Intl.Locale.maximize / minimize)

```js
new Intl.Locale('en').maximize().toString();        // 'en-Latn-US'
new Intl.Locale('zh').maximize().toString();        // 'zh-Hans-CN'
new Intl.Locale('zh-Hant').maximize().toString();   // 'zh-Hant-TW'
new Intl.Locale('zh-Hans-CN').minimize().toString();// 'zh'
```

Use `maximize()` to expand a bare language tag to its CLDR-implied default region/script.

### Recipe 8: Lookup against IANA Subtag Registry

```bash
# Download once
curl -sL https://www.iana.org/assignments/language-subtag-registry > registry.txt

# Find a language subtag
awk 'BEGIN{RS="%%\n"} /Type: language/ && /Subtag: yue/' registry.txt
# Subtag: yue
# Description: Yue Chinese
# Description: Cantonese
# Added: 2009-07-29

# Find script subtags
awk 'BEGIN{RS="%%\n"} /Type: script/' registry.txt | grep -A1 'Subtag: '
```

### Recipe 9: Crowdin / Lokalise / Phrase tag conventions

| TMS | Format | Example |
|---|---|---|
| Crowdin | BCP 47 | `zh-CN` (legacy) or `zh-Hans-CN` (configurable) |
| Lokalise | BCP 47 with underscore option | `zh_Hans_CN` or `zh-Hans-CN` |
| Phrase Strings | BCP 47 | `zh-Hans-CN` |
| GitHub i18n | BCP 47 | `zh-Hans-CN` |
| iOS `.lproj` | ISO/POSIX | `zh-Hans.lproj`, `pt-BR.lproj` |
| Android `res/values-` | POSIX-ish | `values-zh-rCN`, `values-pt-rBR` (note `r` prefix) |
| Gettext `.po` | POSIX | `pt_BR`, `zh_CN` |

```bash
# Normalize all to BCP 47 before submitting to TMS
node -e "console.log(Intl.getCanonicalLocales(['pt_BR', 'zh_CN', 'fr_CA']))"
# → [ 'pt-BR', 'zh-CN', 'fr-CA' ]
# Then manually expand zh-CN → zh-Hans-CN for unambiguity
```

### Recipe 10: Android / iOS conversion

```js
// BCP 47 → Android values-XX folder
function bcp47ToAndroid(tag) {
  const loc = new Intl.Locale(tag);
  let folder = loc.language;
  if (loc.script) folder += `-${loc.script.slice(0,1)}${loc.script.slice(1).toLowerCase()}`;
  if (loc.region) folder += `-r${loc.region}`;
  return folder;
}
bcp47ToAndroid('zh-Hans-CN');   // 'zh-Hans-rCN'
bcp47ToAndroid('pt-BR');         // 'pt-rBR'

// iOS uses BCP 47 lproj names directly since iOS 9
function bcp47ToIOS(tag) {
  return tag.replace(/-/g, '-');   // 'zh-Hans' becomes 'zh-Hans.lproj'
}
```

### Recipe 11: Extension subtags (calendar, numbering)

```
en-US-u-ca-buddhist      Buddhist calendar
ar-SA-u-nu-arab          Arabic-Indic digits
th-TH-u-ca-buddhist-nu-thai   Thai calendar + Thai digits
ja-JP-u-ca-japanese      Japanese imperial calendar
```

```js
new Intl.DateTimeFormat('th-TH-u-ca-buddhist', { dateStyle: 'long' }).format(new Date());
// → "11 มิถุนายน พ.ศ. 2569"  (Thai Buddhist year)
```

### Recipe 12: Private-use tags for test / internal

```
x-internal              Internal test locale
en-x-pseudo             Pseudo-localized English
qps-Latn-ploc           Microsoft's pseudo-locale (qps = reserved test range)
ach                     Crowdin's pseudo-locale (Acholi, repurposed)
```

`qps-*` (qaa-qtz) range is reserved by ISO for private use.

## Examples

### Example 1: Convert customer locale list to canonical BCP 47

**Goal:** Marketing team supplies `[en_US, pt_BR, zh_CN, zh_TW, ar, he, fr-CA, in]` — normalize for Crowdin.

**Steps:**
1. Run each through Recipe 4 normalize: `iw → he`, `in → id`, `zh_CN → zh-Hans-CN`, `zh_TW → zh-Hant-TW`.
2. Run `Intl.getCanonicalLocales()` on result for syntactic validation.
3. Filter against `Intl.DisplayNames([...]).of(tag)` returning a non-empty string — confirms CLDR coverage.
4. Output: `['en-US', 'pt-BR', 'zh-Hans-CN', 'zh-Hant-TW', 'ar', 'he', 'fr-CA', 'id']`.
5. Push to Crowdin via `crowdin.yml` `languages_mapping`.

**Result:** All locales canonical; no downstream ambiguity in TMS or rendering.

### Example 2: Choose between `zh-CN` and `zh-Hans-CN`

**Goal:** New product launching in mainland China; engineering wrote `zh-CN`, design lead asks if that's right.

**Steps:**
1. Run: `Intl.getCanonicalLocales(['zh-CN'])` → `['zh-CN']` — syntactically valid.
2. Run: `new Intl.Locale('zh-CN').maximize().toString()` → `'zh-Hans-CN'` — CLDR fills in `Hans`.
3. But: vendor tooling (TMS, CAT, font config) may not maximize. Risk: Traditional fonts served if region inferred wrong.
4. Decision: use `zh-Hans-CN` explicitly everywhere — leaves no inference to tooling.
5. Update: `crowdin.yml`, `i18n/routing.ts`, `<html lang>`, `Accept-Language` parsing, CDN routing.
6. Add unit test asserting `'zh-CN'` input maps to `'zh-Hans-CN'`.

**Result:** Unambiguous Simplified Chinese; tooling can't pick Traditional Hant glyphs by accident.

## Edge cases / gotchas

- **`zh-CN` is technically valid but ambiguous** — CLDR maximizes to `zh-Hans-CN`, but third-party font configs, OS keyboards, and older browsers may not. Always use `zh-Hans-CN` / `zh-Hant-TW` explicitly.
- **`no` vs `nb` / `nn`** — `no` is a macrolanguage. Use `nb-NO` (Bokmål) or `nn-NO` (Nynorsk) explicitly.
- **`tl` vs `fil`** — Tagalog (`tl`) is a language; Filipino (`fil`) is the official register. Use `fil-PH`.
- **`yue` vs `zh-yue` vs `zh-Hant-HK`** — Cantonese has dedicated `yue`; HK locale is `zh-Hant-HK` for written; spoken Cantonese is `yue-Hant-HK`.
- **Legacy macros `iw` / `in` / `ji`** — IANA marked deprecated; current `he` / `id` / `yi`. Normalize on input.
- **`en-US-POSIX`** — POSIX variant; rare; can break ICU date parsing.
- **Region `419` (LATAM)** — UN M.49 code; valid BCP 47; covers all of Spanish Latin America as one bucket.
- **Casing** — `zh-hans-cn` and `ZH-Hans-CN` are both valid input but not canonical. Always store canonical.
- **Underscores** — `zh_Hans_CN` is POSIX / Java; not BCP 47. Convert to hyphens.
- **`x-default` is not a real BCP 47** — it's a hreflang convention only; do not use as `lang=` attribute.
- **`Intl.DisplayNames` may return undefined** — if locale has no CLDR data, `of()` returns the tag itself or undefined. Always handle.
- **iOS uses `Base.lproj`** for templates, BCP 47 for locales. Don't store `en.lproj` and `en-US.lproj` both — they collide.
- **Android `r` prefix** — `values-pt-rBR` (region prefix `r`). Without `r`, Android treats as new locale.
- **Crowdin custom mappings** — `crowdin.yml` `languages_mapping` overrides Crowdin's default codes for files. Use when stuck with legacy POSIX in code.
- **Right-to-left detection** — never `tag === 'ar' || tag === 'he'`. Use `new Intl.Locale(tag).textInfo.direction === 'rtl'`. Catches `fa`, `ur`, `ps`, `ku`, `yi`.
- **Variant subtags rare in product** — `de-1996` (new orthography), `ca-valencia` (Valencian Catalan), `be-tarask` (Belarusian). Most TMSs don't expose these.

## Sources

- BCP 47 / RFC 5646: https://www.rfc-editor.org/info/bcp47  +  RFC https://www.rfc-editor.org/rfc/rfc5646.html
- IANA Language Subtag Registry: https://www.iana.org/assignments/language-subtag-registry
- CLDR picking codes: https://cldr.unicode.org/index/cldr-spec/picking-the-right-language-code
- CLDR available locales: https://github.com/unicode-org/cldr-json/blob/main/cldr-json/cldr-core/availableLocales.json
- Intl.getCanonicalLocales / Intl.Locale / Intl.DisplayNames: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl
- ISO 639 / 15924 / 3166 / UN M.49: https://www.loc.gov/standards/iso639-2/  https://www.unicode.org/iso15924/  https://www.iso.org/iso-3166-country-codes.html  https://unstats.un.org/unsd/methodology/m49/
- Android locale qualifiers: https://developer.android.com/guide/topics/resources/providing-resources#AlternativeResources
- Apple language and locale IDs: https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPInternational/LanguageandLocaleIDs/LanguageandLocaleIDs.html
