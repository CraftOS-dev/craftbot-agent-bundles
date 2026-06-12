---
name: rtl-cjk-layout-testing
description: RTL (Arabic/Hebrew/Urdu/Farsi) + CJK (Japanese/Chinese/Korean) layout testing. CSS Logical Properties + dir="rtl" + Playwright screenshot diff. Use when the user asks "test RTL", "Arabic layout broken", "CJK font fallback", or wants a multi-locale layout regression gate.
---

# RTL + CJK Layout Testing

RTL covers ~600M users (Arabic 422M + Hebrew 9M + Urdu 230M + Farsi 110M + Pashto 60M). CJK covers 1.5B+. Both break LTR-only layouts. The fix is structural (CSS Logical Properties + `dir="rtl"`) + verified (Playwright screenshot diff).

## When to use

- Adding Arabic / Hebrew / Urdu / Farsi to the app.
- Adding Japanese / Chinese / Korean and seeing font-fallback boxes.
- Migrating legacy CSS (`margin-left`/`padding-right`) to logical properties.
- Want a CI gate that prevents RTL/CJK regressions on every PR.
- Reports of broken icons / mirrored UI in RTL.

Trigger phrases: "RTL", "right to left", "Arabic layout", "Hebrew", "CJK", "Japanese font", "Chinese font", "logical properties", "dir=rtl".

## Setup

```bash
# Playwright for visual regression
npm i -D @playwright/test
npx playwright install

# CJK fonts on Linux CI runners (Ubuntu base)
sudo apt-get install -y fonts-noto-cjk fonts-noto-color-emoji fonts-noto-cjk-extra fonts-noto

# Arabic / Hebrew fonts
sudo apt-get install -y fonts-noto-arabic fonts-noto-hebrew

# stylelint for logical property enforcement
npm i -D stylelint stylelint-config-standard stylelint-use-logical
```

Auth/env: none required.

## RTL CSS migration map (cheat sheet)

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

## Common recipes

### Recipe 1: HTML root setup

```html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
  <head>...</head>
  <body>...</body>
</html>
```

For dynamic locale switching:
```ts
// Next.js
import { useLocale } from 'next-intl';
const locale = useLocale();
const dir = ['ar', 'he', 'ur', 'fa', 'ps', 'yi'].includes(locale) ? 'rtl' : 'ltr';
return <html lang={locale} dir={dir}>...</html>;
```

Better — use Intl.Locale (CLDR-aware, future RTL locales automatic):
```ts
const dir = new Intl.Locale(locale).textInfo?.direction ?? 'ltr';
```

### Recipe 2: Direction check (not locale check)

**BAD:**
```js
const isRTL = locale === 'ar' || locale === 'he';
```

**GOOD:**
```js
const isRTL = document.dir === 'rtl';
// OR
const isRTL = new Intl.Locale(locale).textInfo?.direction === 'rtl';
```

Why: misses Urdu, Farsi, Pashto, Yiddish.

### Recipe 3: Logical properties stylelint rule

```json
// .stylelintrc.json
{
  "extends": ["stylelint-config-standard"],
  "plugins": ["stylelint-use-logical"],
  "rules": {
    "csstools/use-logical": [
      "always",
      { "except": ["transform"] }
    ]
  }
}
```

```bash
npx stylelint 'src/**/*.css'
# Auto-fix where possible
npx stylelint 'src/**/*.css' --fix
```

### Recipe 4: Audit existing CSS for directional properties

```bash
grep -rE 'margin-(left|right):|padding-(left|right):|text-align:\s*(left|right)|float:\s*(left|right)|border-(left|right):' src/ \
  --include='*.css' --include='*.scss' --include='*.tsx' --include='*.jsx'

# Count by file
grep -rcE 'margin-(left|right):' src/ --include='*.css' | sort -t: -k2 -nr | head -20
```

### Recipe 5: Icon flipping for RTL

Icons that flip (chevrons, arrows, navigation):
```css
[dir="rtl"] .chevron-right,
[dir="rtl"] .arrow-back,
[dir="rtl"] .reply-icon {
  transform: scaleX(-1);
}
```

Icons that **don't** flip (logos, play/pause, phone, location, numbers):
```css
/* Default — no transform; logos/brand never flip */
.logo, .brand-mark { /* no flip */ }
```

### Recipe 6: Playwright RTL + CJK + pseudo grid

```ts
// tests/i18n-layout.spec.ts
import { test, expect } from '@playwright/test';

const LOCALES = [
  { code: 'en-US', dir: 'ltr', label: 'baseline' },
  { code: 'ach',   dir: 'ltr', label: 'pseudo' },
  { code: 'ar',    dir: 'rtl', label: 'rtl-arabic' },
  { code: 'he',    dir: 'rtl', label: 'rtl-hebrew' },
  { code: 'ja',    dir: 'ltr', label: 'cjk-japanese' },
  { code: 'zh-Hans-CN', dir: 'ltr', label: 'cjk-simplified' },
  { code: 'zh-Hant-TW', dir: 'ltr', label: 'cjk-traditional' },
  { code: 'ko',    dir: 'ltr', label: 'cjk-korean' },
];

const PAGES = ['/', '/checkout', '/settings', '/profile'];

for (const loc of LOCALES) {
  for (const pg of PAGES) {
    test(`${loc.label} ${pg}`, async ({ page }) => {
      await page.goto(`http://staging.app.com/${loc.code}${pg}`);
      const html = page.locator('html');
      await expect(html).toHaveAttribute('dir', loc.dir);
      await expect(page).toHaveScreenshot(`${loc.label}-${pg.replace('/', '-') || 'home'}.png`, {
        maxDiffPixelRatio: 0.02,
        fullPage: true,
      });
    });
  }
}
```

### Recipe 7: CJK font fallback chain

```css
/* Regional Noto subsets — character forms differ between SC/TC/JP/KR */
:lang(zh-Hans), [lang|="zh-Hans"] {
  font-family: 'Noto Sans SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
}
:lang(zh-Hant), [lang|="zh-Hant"] {
  font-family: 'Noto Sans TC', 'PingFang TC', 'Microsoft JhengHei', sans-serif;
}
:lang(ja), [lang|="ja"] {
  font-family: 'Noto Sans JP', 'Hiragino Sans', 'Yu Gothic', sans-serif;
}
:lang(ko), [lang|="ko"] {
  font-family: 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;
}
```

### Recipe 8: Arabic contextual forms

```css
:lang(ar), :lang(fa), :lang(ur) {
  font-family: 'Noto Sans Arabic', 'Geeza Pro', 'Tahoma', sans-serif;
  font-feature-settings: 'init', 'medi', 'fina', 'isol';   /* initial/medial/final/isolated */
}
```

### Recipe 9: Bidi isolation for mixed-direction content

```html
<!-- Wrap LTR content inside RTL paragraph -->
<p>السعر هو <bdi>$123.45</bdi> في اليوم.</p>

<!-- Or via CSS for dynamic content -->
.user-name { unicode-bidi: isolate; }
.code-snippet { unicode-bidi: isolate; direction: ltr; }
```

### Recipe 10: Numeric input direction

Arabic-Indic digits (`٠١٢٣٤٥٦٧٨٩`) vs Latin (`0123456789`):
```html
<!-- Force Latin digits in form inputs (broader UX, common pattern) -->
<input type="tel" lang="en" />

<!-- Or let CLDR handle -->
<input dir="auto" />
```

### Recipe 11: Form field alignment RTL

```css
.form-input {
  text-align: start;            /* not 'left' */
  padding-inline-start: 1rem;   /* not padding-left */
  padding-inline-end: 0.5rem;
}
.form-icon {
  inset-inline-start: 0.75rem;  /* not 'left: 0.75rem' */
}
```

### Recipe 12: Tabular numbers (always LTR)

```css
.price, .stat, .table-number {
  font-feature-settings: 'tnum';   /* tabular numbers */
  unicode-bidi: isolate;
  direction: ltr;                  /* lock LTR for numbers */
}
```

### Recipe 13: CJK line breaks

```css
/* Chinese has no spaces — let browser break anywhere */
:lang(zh-Hans), :lang(zh-Hant) {
  word-break: break-all;
  line-break: strict;            /* CJK punctuation correctness */
}

/* Japanese — kinsoku shori (punctuation rule) */
:lang(ja) {
  line-break: strict;
  word-break: keep-all;
}
```

### Recipe 14: CSS Grid + Flexbox auto-reverse

Flexbox `flex-direction: row` auto-reverses in `dir="rtl"`. Verify nothing overrides:
```css
/* GOOD — auto-reverses */
.nav { display: flex; flex-direction: row; }

/* BAD — forces direction regardless of dir */
.nav { display: flex; flex-direction: row-reverse; }
```

Grid `grid-template-columns` also auto-flips column order.

### Recipe 15: Custom property direction-aware

```css
:root {
  --gap-start: 16px;
  --gap-end: 8px;
}
.card {
  margin-inline: var(--gap-start) var(--gap-end);  /* applies start/end correctly */
}
```

## Examples

### Example 1: Migrate a CSS module from directional to logical properties

**Goal:** `Sidebar.module.css` uses `margin-left` / `padding-right`; need RTL-correct version.

**Steps:**
1. Audit: `grep -E 'margin-(left|right):|padding-(left|right):' src/components/Sidebar/Sidebar.module.css`.
2. Replace per the migration map table (Recipe 3 mapping).
3. Add stylelint rule (Recipe 3) — fails CI on future regressions.
4. Add Arabic test page to staging.
5. Add Playwright snapshot for `ar` Sidebar route (Recipe 6).
6. Visual diff confirms layout flips correctly; commit + open PR.

**Result:** Sidebar renders correctly LTR + RTL with zero JS direction checks.

### Example 2: Catch CJK font fallback boxes in CI

**Goal:** `/ja/` page shows tofu boxes (□) on Linux CI but not local Mac.

**Steps:**
1. Install Noto CJK on CI runner: `sudo apt-get install -y fonts-noto-cjk fonts-noto-cjk-extra`.
2. Add Japanese page to Playwright grid (Recipe 6).
3. Baseline screenshot now renders Japanese glyphs.
4. Future CSS regression that removes the font fallback chain → Playwright diff catches it.

**Result:** Font fallback regressions visible pre-merge.

### Example 3: Add Hebrew without breaking Arabic

**Goal:** Already have Arabic working; adding Hebrew.

**Steps:**
1. Add Hebrew to locale list: `['en', 'de', 'ar', 'he', 'ja']`.
2. Update RTL detection (Recipe 2) — `Intl.Locale.textInfo.direction` auto-handles.
3. Add Hebrew page set to Playwright grid (Recipe 6).
4. Update font stack (Recipe 8) — add Hebrew Noto: `font-family: 'Noto Sans Hebrew', sans-serif;` for `:lang(he)`.
5. Test mixed-Hebrew-LTR content (URLs, codes) wraps with `<bdi>` (Recipe 9).
6. Visual diff against baseline.

**Result:** Hebrew works alongside Arabic with no special-casing.

## Edge cases / gotchas

- **`flex-direction: row-reverse` overrides RTL** — don't force; let browser auto-flip on `dir="rtl"`.
- **CSS animations don't auto-flip** — `keyframes` with `translateX(100px)` moves left in RTL when you wanted right. Use `inset-inline-start` for positioning animations.
- **`position: fixed` toasts in RTL** — `right: 16px` becomes left side in RTL because viewport flips. Use `inset-inline-end: 16px` so toast stays on the trailing edge.
- **Mirrored emoji / icons by accident** — `transform: scaleX(-1)` flips children too; isolate to specific icon.
- **CJK punctuation width** — `、。「」` are full-width; mixing with half-width Latin needs `text-spacing`.
- **iOS Safari `dir` re-render bug** — switching `dir` at runtime sometimes doesn't repaint child layout. Force reflow: `document.body.offsetHeight`.
- **Inputs `dir="auto"` works for free** — but breaks `text-align` if you override. Test both.
- **`unicode-bidi: isolate` vs `bidi-override`** — isolate (correct, preserves bidi algorithm). Override (broken, forces direction regardless of content).
- **CKEditor / Slate.js RTL** — rich-text editors need explicit `dir` per block; not always auto.
- **Font subset must cover all CJK regional variants** — single "Noto Sans CJK" file is ~16MB. Use regional subsets (SC/TC/JP/KR) per locale — see `font-selection-cjk-rtl` skill.
- **Right-aligned form labels in RTL** — labels naturally float to trailing edge when using `text-align: start`. Don't override.
- **Pre-existing `[dir="ltr"]` overrides** — sometimes inherited from parent component library. Test components in isolation with `dir="rtl"` wrapper.

## Sources

- 600M people write RTL (Evil Martians): https://evilmartians.com/chronicles/600-million-people-write-right-to-left-2-fixes-your-app-needs
- RTL layout testing guide: https://placeholdertext.org/blog/the-complete-guide-to-rtl-right-to-left-layout-testing-arabic-hebrew-more/
- CSS Logical Properties (MDN): https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Logical_Properties_and_Values
- stylelint-use-logical: https://github.com/csstools/postcss-plugins/tree/main/plugins/stylelint-use-logical
- Intl.Locale.textInfo: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Locale/textInfo
- Unicode BiDi algorithm: https://www.unicode.org/reports/tr9/
- Noto CJK: https://github.com/notofonts/noto-cjk
- Noto Arabic: https://fonts.google.com/noto/specimen/Noto+Sans+Arabic
- Playwright snapshots: https://playwright.dev/docs/test-snapshots
- CSS Grid in RTL: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_grid_layout
