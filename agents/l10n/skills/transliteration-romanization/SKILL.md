---
name: transliteration-romanization
description: ICU Transliterator (Any-Latin, Cyrillic-Latin, Han-Latin/Names), CLDR romanization tables (Pinyin, Romaji, RR Korean). PyICU, ICU4C, Polyglot.js, transliteration npm. Use when the user asks "romanize", "transliterate", "Pinyin", "URL slug for Chinese/Russian/Arabic", "ASCII fallback", or "name search across scripts".
---

# Transliteration & Romanization

ICU Transliterator handles 100+ script pairs (`Any-Latin`, `Cyrillic-Latin`, `Han-Latin`, `Han-Latin/Names`, `Arabic-Latin`, `Hebrew-Latin`, `Greek-Latin`). CLDR ships canonical romanization tables (Pinyin for Mandarin, Hepburn for Japanese, RR for Korean).

Use for: URL slugs, search (Müller ↔ Mueller), accessibility (screen-reader ASCII fallback), name matching across scripts, sortable indexes, ASCII-only environments.

**Romanization is lossy.** Multiple source forms collapse to one Latin form (`亅` and `丿` both become `j` / `pie`); reverse is undefined. Never persist romanized-only versions of names or IDs.

## When to use

- User uploads names in mixed scripts and search must match across.
- URL slug generation for content with Chinese, Cyrillic, Arabic, Greek titles.
- Sortable display of mixed-script lists (collation by Latin form).
- Building ASCII keyboard input for non-Latin languages.
- Pinyin / Furigana annotation generation for learners.
- IATA-style passport-name romanization for travel / KYC.

Trigger phrases: "transliterate", "romanize", "Pinyin", "Romaji", "Hangul romanization", "ICU Transliterator", "slug", "ASCII fallback", "Wade-Giles vs Pinyin", "Hepburn".

## Setup

```bash
# Python — PyICU (binds ICU4C)
pip install PyICU
# Ubuntu: sudo apt-get install libicu-dev pkg-config
# macOS:  brew install icu4c && export PATH="/opt/homebrew/opt/icu4c/bin:$PATH"

# Node — ICU bindings
npm i full-icu                              # ensure Node has full ICU data
npm i icu4x                                 # ICU4X Rust bindings (newer, smaller)
npm i transliteration                       # pure-JS, ASCII slugs only
npm i unidecode                             # python lib has node port; ASCII conversion

# Java
# Maven: com.ibm.icu:icu4j:75.1

# CLI
# uconv — ICU command-line, included with libicu
uconv -x "Any-Latin; Latin-ASCII" -i input.txt -o out.txt

# Polyglot.js for browser
npm i polyglot                              # different from i18n's Polyglot — script polyglot
```

Auth/env: none required.

## ICU Transliterator IDs (memorize)

| ID | Direction | Use |
|---|---|---|
| `Any-Latin` | any script → Latin | One-size-fits-most catch-all |
| `Latin-ASCII` | Latin extended → basic ASCII | Drop diacritics (`é → e`) |
| `Han-Latin` | Chinese Hanzi → Pinyin (no tones) | CLDR default |
| `Han-Latin/Names` | Chinese names → Pinyin | Name-specific variants |
| `Han-Spacedlatin` | Chinese → Pinyin with spaces | Per-syllable |
| `Cyrillic-Latin` | Russian / Bulgarian / Serbian → Latin | BGN/PCGN romanization |
| `Greek-Latin` | Greek → Latin | UN-style romanization |
| `Hebrew-Latin` | Hebrew → Latin | UN-style |
| `Arabic-Latin` | Arabic → Latin | UN-style; lossy |
| `Hiragana-Latin` | ひらがな → Romaji | Hepburn |
| `Katakana-Latin` | カタカナ → Romaji | Hepburn |
| `Hangul-Latin` | 한글 → RR | Revised Romanization (KR national standard 2000) |
| `Devanagari-Latin` | Devanagari → Latin | ISO 15919 |
| `Thai-Latin` | Thai → Latin | RTGS |

Compose with `;`: `"Any-Latin; Latin-ASCII; Lower"` → script → strip diacritics → lowercase.

## Common recipes

### Recipe 1: Python — basic any-script to Latin

```python
from icu import Transliterator

t = Transliterator.createInstance("Any-Latin")
t.transliterate("北京")        # 'běi jīng'
t.transliterate("Москва")      # 'Moskva'
t.transliterate("القاهرة")     # 'alqạhrẗ'
t.transliterate("東京")        # 'dōng jīng' (Chinese reading; use Japanese-specific for Japanese)
```

### Recipe 2: Compose pipelines (ICU rule syntax)

```python
from icu import Transliterator

# Full pipeline: any script → Latin → ASCII → lowercase
slug = Transliterator.createInstance("Any-Latin; Latin-ASCII; Lower; [:Punctuation:] Remove")
slug.transliterate("北京欢迎你! 2026")
# → 'bei jing huan ying ni 2026'

slug.transliterate("Crème Brûlée")
# → 'creme brulee'

slug.transliterate("Здравствуй, мир!")
# → 'zdravstvuj mir'
```

### Recipe 3: ICU4C / uconv CLI

```bash
# Single transform
echo "東京タワー" | uconv -x "Any-Latin"
# → dōng jīng tawā

# Pipeline
echo "Crème Brûlée 北京" | uconv -x "Any-Latin; Latin-ASCII; Lower"
# → creme brulee bei jing

# Batch convert file
uconv -x "Any-Latin; Latin-ASCII" -i ru_names.txt -o ru_names_ascii.txt
```

### Recipe 4: Node — ICU4X / full-icu

```js
// Node 22+ with full-icu
const tx = new Intl.Collator('en', { sensitivity: 'base' });
// ↑ Collator handles diacritic-insensitive matching (Müller == Muller)

// For actual transliteration, use a binding:
import { Transliterator } from 'icu4x';
const t = Transliterator.create('Any-Latin');
t.transliterate('北京');   // 'běi jīng'
```

### Recipe 5: Node — transliteration npm (ASCII slugs)

```js
import { slugify, transliterate } from 'transliteration';

transliterate('北京欢迎你');      // 'Bei Jing Huan Ying Ni '
transliterate('Crème Brûlée');    // 'Creme Brulee'
transliterate('Здравствуй');      // 'Zdravstvuy'

slugify('北京欢迎你 2026');       // 'bei-jing-huan-ying-ni-2026'
slugify('Crème Brûlée Café');     // 'creme-brulee-cafe'
slugify('日本語', { trim: true }); // 'ri-ben-yu'
```

Pure-JS, no ICU dep, ~50KB. Lower quality than ICU (no Han-Names specialty, less Pinyin accuracy).

### Recipe 6: Polyglot.js (browser-side transliteration)

```js
// CDN
<script type="module">
import { Transliterator } from 'https://unpkg.com/polyglot-js/dist/polyglot.mjs';

const t = await Transliterator.create('Any-Latin');
console.log(t.transliterate('日本語'));   // 'rì běn yǔ'
</script>
```

WASM-based; uses ICU4X data; ~400KB total. Good when server-side ICU not viable.

### Recipe 7: URL slug for CMS content

```python
from icu import Transliterator
import re

slug_xlit = Transliterator.createInstance(
  "Any-Latin; Latin-ASCII; Lower; [^[:Alphanumeric:][:Whitespace:]] Remove"
)

def slugify(text, max_len=80):
    s = slug_xlit.transliterate(text).strip()
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s[:max_len]

slugify("北京欢迎你！2026年的春天")    # 'bei-jing-huan-ying-ni-2026-nian-de-chun-tian'
slugify("Здравствуй мир")              # 'zdravstvuj-mir'
slugify("Café René - L'Été")           # 'cafe-rene-lete'
```

### Recipe 8: Han-Latin/Names — Chinese name accuracy

```python
from icu import Transliterator

# Generic Han transliterator picks most common reading
generic = Transliterator.createInstance("Han-Latin")
generic.transliterate("王小明")    # 'wáng xiǎo míng'

# Names-specialized — different default reading for common name characters
names = Transliterator.createInstance("Han-Latin/Names")
names.transliterate("曾国藩")      # 'zēng guó fán'  (NOT 'céng' for 曾 in name context)
```

Han characters often have multiple readings (多音字); `/Names` variant prefers name readings.

### Recipe 9: Japanese name romanization (Hepburn vs Kunrei-shiki)

```python
from icu import Transliterator

# ICU default = Hepburn-ish
t = Transliterator.createInstance("Hiragana-Latin")
t.transliterate("ふじさん")        # 'fujisan'

# Katakana
t2 = Transliterator.createInstance("Katakana-Latin")
t2.transliterate("トウキョウ")     # 'toukyou' (or 'tōkyō' with macrons)

# For Kanji → Romaji you need MeCab or kakasi (Japanese-specific morphological)
# ICU's Any-Latin treats Kanji as Chinese → wrong reading
# Use: pip install pykakasi
import pykakasi
kks = pykakasi.kakasi()
result = kks.convert("東京")
print(result[0]['hepburn'])     # 'toukyou'
```

ICU does NOT do Kanji → Japanese Romaji; it treats CJK Unified Ideographs as Chinese. Use pykakasi or MeCab for Japanese.

### Recipe 10: Korean Revised Romanization

```python
from icu import Transliterator

t = Transliterator.createInstance("Hangul-Latin")
t.transliterate("서울")            # 'seoul'
t.transliterate("부산")            # 'busan'
t.transliterate("김치")            # 'gimchi' (RR; would be 'kimchi' in McCune-Reischauer)
```

ICU uses Revised Romanization (Korean MOE 2000 standard). For McCune-Reischauer (academic), use `Hangul-Latin/MR` if available, else manual mapping.

### Recipe 11: Search across scripts (Müller / Mueller / Muller)

```js
// Build normalized search index
function normalizeForSearch(str) {
  return str
    .normalize('NFKD')
    .replace(/[̀-ͯ]/g, '')      // strip combining diacritics
    .replace(/ß/g, 'ss')                   // German ess-tsett
    .replace(/ä/gi, 'ae')                  // umlaut → digraph (German convention)
    .replace(/ö/gi, 'oe')
    .replace(/ü/gi, 'ue')
    .toLowerCase();
}

normalizeForSearch('Müller');     // 'mueller'
normalizeForSearch('Mueller');    // 'mueller'
normalizeForSearch('Muller');     // 'muller'   ← different; explicit
// All-in-one with ICU:
//   Transliterator "Any-Latin; Latin-ASCII; de-ASCII"
//   or composite "NFKD; [:Nonspacing Mark:] Remove; NFC; Lower"
```

### Recipe 12: Passport-name romanization (ICAO 9303)

```python
# ICAO 9303 = travel-doc standard. ICU has no MRZ rules; combine per origin:
# CN: Pinyin no tones | RU: GOST R 52535.1 | KR: RR + surname overrides (Lee/Park/Kim) | JP: Hepburn
PASSPORT_RULES = {
  'CN': Transliterator.createInstance("Han-Latin/Names; Latin-ASCII; Upper"),
  'RU': Transliterator.createInstance("Cyrillic-Latin/BGN; Latin-ASCII; Upper"),
  'JP': lambda s: pykakasi.kakasi().convert(s)[0]['hepburn'].upper(),
  'KR': Transliterator.createInstance("Hangul-Latin; Latin-ASCII; Upper"),
}
```

### Recipe 13: Furigana / Pinyin annotation for learners

```python
import pykakasi; from pypinyin import pinyin, Style
pykakasi.kakasi().convert("東京駅")        # → [{orig:東京,hira:とうきょう,hepburn:toukyou},...]
pinyin('中文', style=Style.TONE)           # [['zhōng'], ['wén']]
pinyin('中文', style=Style.NORMAL)         # [['zhong'], ['wen']]
```

### Recipe 14: ICU rule-set inline (custom transliterator)

```python
from icu import Transliterator
rules = "ß > ss; ä > ae; ö > oe; ü > ue; Ä > Ae; Ö > Oe; Ü > Ue;"
t = Transliterator.createFromRules("de_ASCII", rules)
t.transliterate("Müßiggang")    # 'Muessiggang'
```

### Recipe 15: Reverse + batch normalize

```python
# Reverse (Latin → script) is lossy; use only for search candidate generation.
Transliterator.createInstance("Latin-Cyrillic").transliterate("Moskva")  # 'Москва'

# Batch normalize a CSV column → ASCII slug column
import csv, sys
t = Transliterator.createInstance('Any-Latin; Latin-ASCII; Lower')
for row in csv.reader(open(sys.argv[1])):
    print(','.join(row + [t.transliterate(row[1])]))
```

## Examples

### Example 1: URL slugs for a multilingual CMS

**Goal:** Editors publish posts in EN, ZH, RU, AR; slug column must be ASCII and SEO-safe.

**Steps:**
1. Pick library — ICU server-side (Python or Node) for quality, `transliteration` npm if no ICU.
2. Pipeline (Recipe 2): `"Any-Latin; Latin-ASCII; Lower; [^[:Alphanumeric:][:Whitespace:]] Remove"`.
3. Wrap with `slugify()` (Recipe 7) — collapse whitespace to `-`, trim to 80 chars.
4. Apply on publish hook (Strapi `beforeCreate`, Sanity `slugify` source).
5. Persist both `title` (original) and `slug` (ASCII). Never display slug to humans.
6. Unit test: `slugify('北京欢迎你')` → `'bei-jing-huan-ying-ni'`; `slugify('Здравствуй мир')` → `'zdravstvuj-mir'`.

**Result:** SEO-friendly Latin URLs; humans see original title; search engines index ASCII paths.

### Example 2: KYC search — `Müller` matches `Mueller` matches `Muller`

**Goal:** Compliance team uploads CSV of sanctioned names; agent search must match across diacritic variants.

**Steps:**
1. Build search-normalized column (Recipe 11) for every row at ingest.
2. On query: normalize the input the same way.
3. Index normalized form in DB (`mueller`).
4. Lookup: `WHERE search_norm = $normalized OR search_norm LIKE $normalized || '%'`.
5. Per language family, customize rules — German uses `ae`/`oe`/`ue`/`ss`; Scandinavian uses `ae`/`oe`; Czech strips diacritics only.
6. Audit: log raw + normalized for explainability.

**Result:** Diacritic-insensitive search; auditable; no false negatives from spelling variants.

## Edge cases / gotchas

- **LOSSY** — `Müller` / `Mueller` both → `mueller`; not reversible. Never use as a unique ID.
- **CJK Unified Ideographs ambiguity** — `直` differs in JP vs ZH; `Any-Latin` defaults to Pinyin. Use script-specific transliterators for JA/KO.
- **Pinyin tones in slugs** — `tóu` not URL-safe; always chain `Latin-ASCII`.
- **Han-Latin vs Han-Latin/Names** — `Names` variant picks name-context readings; use for proper nouns.
- **Hangul + Hanja** — ICU `Hangul-Latin` skips Hanja; pre-process with kakasi/komoran.
- **Arabic short vowels** — written without vowels (مرحبا = `mrhba` not `marhaba`); needs ḥarakāt source for accurate output.
- **Multiple romanization standards** — Pinyin vs Wade-Giles vs Yale (ZH); BGN/PCGN vs ISO 9 vs GOST (RU). Pick one + document.
- **Korean surname conventions** — `이` is RR `i` but passports use `Lee`; `박` → `Park`. Don't apply ICU blindly to legal names.
- **Transliterator cache** — creation has overhead; cache the instance.
- **NFC/NFD normalization** — apply before transliteration so combining marks are consistent.
- **PyICU on Windows** — requires VC++ + ICU headers; fall back to `unidecode` or `uconv` subprocess.
- **Browser bundle size** — ICU4X WASM ~400KB, `transliteration` npm ~50KB, `unidecode-plus` ~100KB.
- **Mixed scripts** — per-codepoint; `Hello 北京` → `hello běi jīng`.
- **Diacritic-only normalization** — `NFKD; [:Nonspacing Mark:] Remove; NFC` keeps script, strips marks.
- **Turkish lowercase** — `Lower` ignores `İ → i` vs `I → ı`; compose with `tr-Lower`.
- **Collator vs transliterate** — `Intl.Collator` with `sensitivity: 'base'` already matches `Müller ≈ Muller` for sort/compare; transliterate only for stored canonical forms.

## Sources

- ICU Transforms guide + data: https://unicode-org.github.io/icu/userguide/transforms/general/
- PyICU: https://gitlab.pyicu.org/main/pyicu  +  ICU4X (Rust/WASM) https://github.com/unicode-org/icu4x
- transliteration npm: https://github.com/dzcpy/transliteration  +  unidecode (Py) https://pypi.org/project/Unidecode/
- pykakasi (JP): https://github.com/miurahr/pykakasi  +  pypinyin (ZH) https://github.com/mozillazg/python-pinyin
- CLDR transliteration: https://cldr.unicode.org/index/cldr-spec/transliteration-guidelines
- Polyglot.js: https://github.com/airbnb/polyglot.js
- BGN/PCGN romanization: https://www.gov.uk/government/publications/romanisation-systems
- Korean Revised Romanization: https://en.wikipedia.org/wiki/Revised_Romanization_of_Korean
- ICAO 9303 (passport MRZ): https://www.icao.int/publications/pages/publication.aspx?docnum=9303
- Hepburn / Pinyin: https://en.wikipedia.org/wiki/Hepburn_romanization  https://www.iso.org/standard/61420.html (ISO 7098)
