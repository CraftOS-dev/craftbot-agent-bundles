---
name: font-selection-cjk-rtl
description: Font selection + subsetting for CJK (Noto Sans SC/TC/JP/KR) and RTL (Noto Sans Arabic/Hebrew). glyphhanger + pyftsubset, font-display, unicode-range, contextual forms. Use when the user asks "CJK font", "Arabic font", "subset font", "font tofu", or fonts are 5-20MB.
---

# Font Selection & Subsetting — CJK + RTL

Unoptimized CJK fonts are 5-20 MB; after subsetting 100-500 KB. Critical for mobile + slow networks. **Regional Noto variants are NOT interchangeable** — kanji forms differ between SC/TC/JP/KR even when codepoints overlap.

Arabic needs `font-feature-settings: "init", "medi", "fina"` for contextual letter forms. Hebrew + Thai + Devanagari have script-specific requirements.

## When to use

- Adding CJK locale (ZH/JA/KO) and shipping fonts.
- Adding Arabic / Hebrew / Thai / Devanagari.
- Reports of tofu boxes (□) in production.
- Font payload > 1MB and needs to shrink.
- Mixed-script content rendering issues.

Trigger phrases: "CJK font", "Noto Sans", "Arabic font", "Hebrew font", "font subset", "glyphhanger", "tofu", "font tofu", "kanji forms".

## Setup

```bash
# glyphhanger (web subsetting)
npm i -g glyphhanger

# pyftsubset (fontTools — more control)
pip install fonttools brotli

# Noto fonts — download from
# https://github.com/notofonts/noto-cjk/releases
# https://fonts.google.com/noto/specimen/Noto+Sans+Arabic

# Font format converters
npm i -g ttf2woff2
brew install woff2                       # OR pip install fonttools
```

Auth/env: none required.

## Regional Noto variants (memorize)

| Variant | Use for | Notes |
|---|---|---|
| Noto Sans SC | Simplified Chinese (CN, SG) | China standard |
| Noto Sans TC | Traditional Chinese (TW) | Taiwan kanji forms |
| Noto Sans HK | Traditional Chinese (HK) | Hong Kong-specific glyphs |
| Noto Sans JP | Japanese | Kanji forms differ from Chinese |
| Noto Sans KR | Korean | Hangul + Hanja |
| Noto Sans Arabic | Arabic, Persian, Urdu, Pashto | Contextual forms |
| Noto Sans Hebrew | Hebrew, Yiddish | RTL |
| Noto Sans Thai | Thai | No spaces; word breaking |
| Noto Sans Devanagari | Hindi, Marathi, Sanskrit | Combining marks |
| Noto Color Emoji | Emoji | Multi-script |

**Never use "Noto Sans CJK" combined** — 16MB unsubsetted; renders Chinese kanji in wrong forms for JP context.

## Common recipes

### Recipe 1: glyphhanger subsetting from page corpus

```bash
# Crawl your site, capture used characters → subset font
glyphhanger https://example.com --subset=NotoSansJP.ttf \
  --formats=woff2 --output=public/fonts/

# Or whitelist Unicode ranges
glyphhanger --subset=NotoSansJP.ttf --formats=woff2 \
  --output=public/fonts/ \
  --whitelist-ranges=U+3040-309F,U+30A0-30FF,U+4E00-9FFF,U+FF00-FFEF
# U+3040-309F: Hiragana
# U+30A0-30FF: Katakana
# U+4E00-9FFF: CJK Unified Ideographs
# U+FF00-FFEF: Halfwidth/Fullwidth
```

### Recipe 2: pyftsubset — fine control

```bash
# Subset from text corpus
pyftsubset NotoSansSC.otf \
  --text-file=corpus.txt \
  --output-file=NotoSansSC.woff2 \
  --flavor=woff2 \
  --layout-features='*' \
  --no-hinting

# Subset by Unicode range
pyftsubset NotoSansArabic.ttf \
  --unicodes='U+0600-06FF,U+0750-077F,U+FB50-FDFF,U+FE70-FEFF' \
  --output-file=NotoSansArabic-subset.woff2 \
  --flavor=woff2 \
  --layout-features='init,medi,fina,isol,rlig,calt'
```

### Recipe 3: Generate corpus from i18n catalog

```bash
# Extract all characters used in translated content
cat locales/*.json | python -c "
import sys, json
chars = set()
for line in sys.stdin:
    try:
        data = json.loads(line)
    except: continue
    def walk(o):
        if isinstance(o, str): chars.update(o)
        elif isinstance(o, dict): [walk(v) for v in o.values()]
        elif isinstance(o, list): [walk(v) for v in o]
    walk(data)
print(''.join(sorted(chars)))
" > corpus.txt

pyftsubset NotoSansJP.otf --text-file=corpus.txt --output-file=fonts/NotoSansJP.woff2 --flavor=woff2
```

### Recipe 4: Per-locale font loading via CSS

```css
/* SC */
@font-face {
  font-family: 'Noto Sans';
  src: url('/fonts/NotoSansSC.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
  unicode-range: U+4E00-9FFF, U+3000-303F, U+FF00-FFEF;
}

/* JP — different file, different glyphs */
@font-face {
  font-family: 'Noto Sans';
  src: url('/fonts/NotoSansJP.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
  unicode-range: U+3040-309F, U+30A0-30FF, U+4E00-9FFF;
}

/* KR */
@font-face {
  font-family: 'Noto Sans';
  src: url('/fonts/NotoSansKR.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
  unicode-range: U+AC00-D7AF, U+1100-11FF, U+3130-318F;
}

/* Arabic */
@font-face {
  font-family: 'Noto Sans Arabic';
  src: url('/fonts/NotoSansArabic.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
  unicode-range: U+0600-06FF, U+0750-077F, U+FB50-FDFF, U+FE70-FEFF;
}
```

### Recipe 5: Locale-scoped font assignment

```css
:lang(zh-Hans), [lang|="zh-Hans"] {
  font-family: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}
:lang(zh-Hant), [lang|="zh-Hant"] {
  font-family: 'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', sans-serif;
}
:lang(ja), [lang|="ja"] {
  font-family: 'Noto Sans JP', 'Hiragino Sans', 'Yu Gothic', 'Meiryo', sans-serif;
}
:lang(ko), [lang|="ko"] {
  font-family: 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
}
:lang(ar), :lang(fa), :lang(ur) {
  font-family: 'Noto Sans Arabic', 'Geeza Pro', 'Tahoma', sans-serif;
  font-feature-settings: 'init', 'medi', 'fina', 'isol';
}
:lang(he), :lang(yi) {
  font-family: 'Noto Sans Hebrew', 'David', 'Arial Hebrew', sans-serif;
}
:lang(th) {
  font-family: 'Noto Sans Thai', 'Tahoma', sans-serif;
  word-break: break-all;             /* Thai has no spaces */
  line-break: strict;
}
```

### Recipe 6: Google Fonts auto-subset

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&family=Noto+Sans+SC:wght@400;700&family=Noto+Sans+Arabic:wght@400;700&display=swap" rel="stylesheet">
```

Google Fonts auto-subsets per page content — good for marketing pages, worse for offline / unpredictable corpus.

### Recipe 7: Per-weight subsetting

```bash
# Subset each weight separately (4-weight × 3 scripts = 12 files)
for weight in 300 400 500 700; do
  pyftsubset NotoSansJP-w$weight.otf \
    --text-file=corpus.txt \
    --output-file=fonts/NotoSansJP-$weight.woff2 \
    --flavor=woff2
done
```

```css
@font-face {
  font-family: 'Noto Sans JP';
  src: url('/fonts/NotoSansJP-400.woff2') format('woff2');
  font-weight: 400;
}
@font-face {
  font-family: 'Noto Sans JP';
  src: url('/fonts/NotoSansJP-700.woff2') format('woff2');
  font-weight: 700;
}
```

### Recipe 8: Variable font subsetting

```bash
# Single variable font file replaces multiple weights
pyftsubset NotoSansJP-VF.ttf \
  --text-file=corpus.txt \
  --output-file=fonts/NotoSansJP-VF.woff2 \
  --flavor=woff2 \
  --layout-features='*' \
  --no-hinting

# Slightly larger single file vs many static files
```

```css
@font-face {
  font-family: 'Noto Sans JP';
  src: url('/fonts/NotoSansJP-VF.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap;
}
```

### Recipe 9: Arabic contextual forms verification

```html
<!-- Test all positions render correctly -->
<p lang="ar">
  مرحبا بالعالم
</p>
<!-- م = isolated (no preceding letter)
     ر = medial
     ح = medial
     ب = medial
     ا = isolated (after non-joining)
     ل = initial
     ع = medial
     ا = medial
     ل = medial
     م = final -->
```

Without `font-feature-settings: "init", "medi", "fina", "isol"`, Arabic renders disconnected.

### Recipe 10: Font payload measurement

```bash
# Before/after sizes
du -h NotoSansJP-Regular.otf            # 16M  (full)
du -h fonts/NotoSansJP.woff2             # 380K (subsetted to 5k chars)
du -h fonts/NotoSansArabic.woff2         # 45K  (Arabic basic + extended)
```

### Recipe 11: Font tofu detection

```ts
// Catch tofu boxes in dev
const testGlyph = document.createElement('span');
testGlyph.style.fontFamily = 'Noto Sans JP, monospace';
testGlyph.innerText = '東京';
testGlyph.style.position = 'absolute';
testGlyph.style.visibility = 'hidden';
document.body.appendChild(testGlyph);

const width = testGlyph.offsetWidth;
testGlyph.style.fontFamily = 'monospace';   // fallback
const fallbackWidth = testGlyph.offsetWidth;
const hasTofu = width === fallbackWidth;    // no special font matched
console.log({ hasTofu });
testGlyph.remove();
```

### Recipe 12: preload critical fonts

```html
<link rel="preload" href="/fonts/NotoSansJP.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/NotoSansArabic.woff2" as="font" type="font/woff2" crossorigin>
```

Only preload fonts needed above-the-fold; preloading unused fonts hurts.

### Recipe 13: System font stack (no web font)

```css
/* If product is OK with system fallback, no web font payload */
:lang(zh-Hans) { font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; }
:lang(zh-Hant) { font-family: 'PingFang TC', 'Microsoft JhengHei', sans-serif; }
:lang(ja) { font-family: 'Hiragino Sans', 'Meiryo', 'Yu Gothic', sans-serif; }
:lang(ko) { font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif; }
:lang(ar) { font-family: 'Geeza Pro', 'Segoe UI', 'Tahoma', sans-serif; }
```

Trade-off: zero font download, but rendering varies per OS.

### Recipe 14: CJK punctuation handling

```css
:lang(ja), :lang(zh-Hans), :lang(zh-Hant) {
  /* Use IVS variation selectors to disambiguate Han characters */
  font-variant-east-asian: jis90 proportional-width;
  text-spacing: trim-start trim-end;     /* CSS Text Module Level 4 */
}
```

### Recipe 15: Vertical CJK writing (rare but supported)

```css
.book-title {
  writing-mode: vertical-rl;          /* right-to-left vertical (JP/ZH-trad) */
  text-orientation: upright;          /* keeps Latin chars vertical */
}
```

### Recipe 16: Font display strategies

```css
@font-face {
  src: url(...);
  font-display: swap;     /* show fallback immediately, swap when font loads */
  /* OR */
  font-display: optional; /* show fallback; skip font if not loaded in 100ms */
  /* OR */
  font-display: fallback; /* brief swap window then fallback */
}
```

For CJK heavy: `swap` causes layout shift; `optional` skips slow loads; pick based on UX priority.

## Examples

### Example 1: Add Japanese support, ship < 500KB fonts

**Goal:** Add JA locale to existing app; CJK font payload must be < 500KB.

**Steps:**
1. Build corpus from translated `ja.json` (Recipe 3) → unique character set ~5000 chars.
2. Download Noto Sans JP from notofonts/noto-cjk.
3. Subset weights 400 + 700 via pyftsubset (Recipes 2, 7) → ~180KB total.
4. Add `@font-face` per weight (Recipe 4) with `unicode-range`.
5. Add `:lang(ja)` selector (Recipe 5).
6. Add preload for above-the-fold weight (Recipe 12).
7. Test: open `/ja/` page, verify no tofu (Recipe 11), Lighthouse confirms font payload.

**Result:** JA locale renders with native-quality fonts; 180KB payload (vs 16MB unsubsetted).

### Example 2: Diagnose Arabic letters appearing disconnected

**Goal:** Arabic words render as separate letters (مرحبا → م ر ح ب ا), not connected.

**Steps:**
1. Inspect element — confirms `font-family: 'Noto Sans Arabic'` applied.
2. Check `font-feature-settings` — missing.
3. Add: `font-feature-settings: 'init', 'medi', 'fina', 'isol', 'rlig', 'calt';` (Recipe 9).
4. Verify in browser — letters connect.
5. Subset font with full layout features: `pyftsubset ... --layout-features='*'`.

**Result:** Arabic renders with proper letter connections.

## Edge cases / gotchas

- **"Noto Sans CJK" single file = 16MB** — split into SC/TC/JP/KR + subset; don't ship monolithic.
- **Kanji form variance** — `直` looks different in SC vs JP vs TC; same codepoint, different glyph. Using wrong Noto subset = wrong glyph.
- **Hong Kong is its own subset** — Noto Sans HK ≠ Noto Sans TC; HK has 4500+ unique characters.
- **`unicode-range` browser support** — modern browsers download only the matching range. Older browsers download all `@font-face` definitions.
- **`font-display: swap` causes layout shift** — CJK in particular shifts visibly. Track CLS metric.
- **CJK fonts in Linux CI (Playwright)** — `apt-get install -y fonts-noto-cjk` else tofu in screenshots.
- **`pyftsubset --layout-features='*'`** — preserves OpenType features (ligatures, contextual alternates). Without, Arabic + Devanagari break.
- **Arabic combining marks** — diacritics (`َ ِ ُ`) need full Unicode range; subsetting with character list may drop them.
- **Devanagari + Indic conjuncts** — `kṣ` (क्ष) needs OpenType GSUB rules; preserve all layout features.
- **Variable fonts axis support** — Noto VF supports weight axis; subsetting drops axes if not specified. Use `--axes='wght=100:900'`.
- **WOFF1 vs WOFF2** — WOFF2 ~30% smaller; supported by all browsers since 2018. Don't ship WOFF1 unless IE11 required.
- **Font subset doesn't cover symbols + emoji** — keep Noto Color Emoji separate; CJK + emoji in one element needs both fonts in family stack.
- **Google Fonts page cache** — same URL same character set; page change triggers new download.
- **Self-host vs Google Fonts** — Google CDN faster globally but GDPR concern (IP transmitted to Google). Self-host for EU compliance.
- **Per-page corpus subset bloat** — if every page has unique chars, lots of subsets. Use Google Fonts dynamic subsetting OR union corpus across high-traffic pages.
- **Font fingerprinting** — privacy concern; some browsers (Tor) block font enumeration.

## Sources

- Noto CJK: https://github.com/notofonts/noto-cjk
- Noto Fonts (all scripts): https://fonts.google.com/noto
- Google Fonts: https://fonts.google.com/
- glyphhanger: https://github.com/zachleat/glyphhanger
- pyftsubset (fontTools): https://fonttools.readthedocs.io/en/latest/subset/
- CJK font optimization: https://font-converters.com/languages/cjk-font-optimization
- font-display: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/font-display
- unicode-range: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/unicode-range
- Arabic typography: https://www.smashingmagazine.com/2024/02/arabic-typography/
- CSS Text Module Level 4: https://www.w3.org/TR/css-text-4/
- Variable fonts: https://web.dev/variable-fonts/
- font subsetting by language: https://font-converters.com/guides/font-subsetting-by-language
