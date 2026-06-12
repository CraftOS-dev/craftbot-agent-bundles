---
name: icu-messageformat-pluralization
description: ICU MessageFormat — plurals, gender, select, nested, dates/numbers/currency. CLDR plural rules per language. FormatJS CLI for lint + extract + compile. Use when the user asks "add plurals", "gender-aware strings", "ICU plural rules", or "fix CLDR categories".
---

# ICU MessageFormat & Pluralization

ICU MessageFormat 1 (current 2026 standard) handles plurals, gender, select, dates/numbers/currency — without if/else logic in components. CLDR plural rules cover all 30+ plural categories (Arabic 6, Russian/Polish 4, English 2, CJK 1).

MessageFormat 2.0 is approaching standardization in 2026; plan for migration but ship MF1 today.

## When to use

- The user is adding count-based UI (`# items`, `# results`, `5 minutes ago`).
- The user needs gender-aware strings (`he uploaded` / `she uploaded` / `they uploaded`).
- The user is integrating dates, numbers, currency, percentages in messages.
- The user has translators reporting "missing plural form" warnings.
- The user is choosing between if/else in code vs ICU in messages.

Trigger phrases: "ICU", "MessageFormat", "plurals", "CLDR plurals", "gender select", "FormatJS", "intl-messageformat", "MF2".

## Setup

```bash
# FormatJS CLI (lint + extract + compile)
npm i -g @formatjs/cli

# Runtime (any of these)
npm i intl-messageformat               # standalone
npm i react-intl                       # React + FormatJS
npm i i18next i18next-icu              # i18next + ICU
npm i next-intl                        # Next.js (uses intl-messageformat under hood)

# Browser/Node 22+ have Intl.* APIs that ICU uses
```

Auth/env: none required.

## CLDR plural categories (memorize)

| Language | Categories | Notes |
|---|---|---|
| English, German, Dutch | one, other | 1 vs 2+ |
| Spanish, Italian, Portuguese | one, many, other | 1 / 1M+ / 2-999K |
| French | one, many, other | 0,1 / 1M+ / 2+ |
| Russian, Polish, Ukrainian, Croatian | one, few, many, other | 1,21,31 / 2-4,22-24 / 0,5-20 |
| Arabic | zero, one, two, few, many, other | 0 / 1 / 2 / 3-10 / 11-99 / 100+ |
| Hebrew | one, two, many, other | 1 / 2 / 10,20,... / other |
| Japanese, Chinese, Korean, Thai, Vietnamese | other | all numbers |
| Welsh | zero, one, two, few, many, other | 0 / 1 / 2 / 3 / 6 / other |

**Always provide `other`** — it's the universal fallback.

## Common recipes

### Recipe 1: Basic plural

```
{count, plural,
  =0 {No items}
  one {# item}
  other {# items}
}
```

`=0`, `=1`, `=N` match exact values (before category rules). `one`, `other` match CLDR category. `#` substitutes the count.

### Recipe 2: Arabic 6-form plural

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

All 6 categories required for translator UX. Translators get explicit warnings if any is missing.

### Recipe 3: Gender select

```
{gender, select,
  male {He uploaded a photo.}
  female {She uploaded a photo.}
  other {They uploaded a photo.}
}
```

`select` is exact-match (not CLDR rules). Always include `other` as fallback.

### Recipe 4: Nested plural + gender

```
{numPhotos, plural,
  =0 {{gender, select,
       female {She has no photos.}
       male {He has no photos.}
       other {They have no photos.}}}
  =1 {{gender, select,
       female {She has 1 photo.}
       male {He has 1 photo.}
       other {They have 1 photo.}}}
  other {{gender, select,
          female {She has # photos.}
          male {He has # photos.}
          other {They have # photos.}}}
}
```

### Recipe 5: Date / time / number / currency

```
You have {count, number} items as of {date, date, long} ({date, time, short}).
Total: {amount, number, ::currency/EUR}
Discount: {pct, number, percent}
```

Skeleton syntax (ICU 1.5+):
```
{amount, number, ::currency/EUR .00}            EUR with 2 decimals
{date, date, ::yMMMd}                            "Apr 3, 2026"
{date, date, ::yMMMMEEEEd}                       "Saturday, April 3, 2026"
```

### Recipe 6: react-intl extraction (FormatJS)

```tsx
// src/components/Cart.tsx
import { FormattedMessage } from 'react-intl';

<FormattedMessage
  id="cart.itemCount"
  defaultMessage="{count, plural, =0 {No items} one {# item} other {# items}}"
  values={{ count }}
/>

<FormattedMessage
  id="cart.userPhotos"
  defaultMessage="{count, plural, =0 {{gender, select, female {She has no photos.} male {He has no photos.} other {They have no photos.}}} other {{gender, select, female {She has # photos.} male {He has # photos.} other {They have # photos.}}}}"
  values={{ count, gender }}
/>
```

Extract:
```bash
formatjs extract 'src/**/*.{ts,tsx}' --out-file lang/en.json \
  --id-interpolation-pattern '[sha512:contenthash:base64:6]'
```

### Recipe 7: Lint catalogs for ICU correctness

```bash
formatjs lint 'lang/**/*.json'

# Catches:
# - Missing `other` fallback
# - Unbalanced braces
# - Missing CLDR categories per locale (e.g., `zero` missing in Arabic plural)
# - Unknown skeleton patterns
```

### Recipe 8: Compile to AST (faster runtime)

```bash
formatjs compile lang/en.json --ast --out-file lang/compiled/en.json
```

AST is pre-parsed; runtime skips parse step. Useful for high-RPS pages.

### Recipe 9: i18next + ICU

```bash
npm i i18next i18next-icu intl-messageformat
```

```ts
import i18next from 'i18next';
import ICU from 'i18next-icu';

i18next.use(ICU).init({
  lng: 'de',
  resources: {
    de: {
      translation: {
        'cart.items': '{count, plural, one {# Artikel} other {# Artikel}}',
      },
    },
  },
});

i18next.t('cart.items', { count: 3 });   // "3 Artikel"
```

### Recipe 10: Standalone intl-messageformat

```ts
import IntlMessageFormat from 'intl-messageformat';

const msg = new IntlMessageFormat(
  '{count, plural, one {# item} other {# items}}',
  'en'
);
msg.format({ count: 3 });   // "3 items"
```

### Recipe 11: Paraglide-js + ICU

```bash
npx @inlang/paraglide-js@latest init
npm i @inlang/paraglide-js-adapter-message-format
```

```ts
// messages/en.json
{
  "cart_items": "{count, plural, one {# item} other {# items}}"
}

// Use compiled:
import * as m from '$lib/paraglide/messages';
m.cart_items({ count: 3 });   // type-checked!
```

### Recipe 12: next-intl + ICU (native)

```ts
// messages/en.json
{
  "Cart": {
    "items": "{count, plural, =0 {No items} one {# item} other {# items}}"
  }
}

// component.tsx
import { useTranslations } from 'next-intl';
const t = useTranslations('Cart');
t('items', { count: 3 });
```

### Recipe 13: Skeleton number formats (ICU 1.5+)

```
{n, number, ::currency/USD}                     $1,234.56
{n, number, ::currency/JPY}                     ¥1,235        (no decimals — CLDR auto)
{n, number, ::compact-short}                    1.2K, 3.5M
{n, number, ::scientific}                       1.234E3
{n, number, ::percent .00}                      12.34%
{n, number, ::measure-unit/length-meter}        1,234 m
{n, number, ::measure-unit/length-meter unit-width-narrow}  1,234m
```

### Recipe 14: Skeleton date formats

```
{d, date, ::yMd}              4/3/2026
{d, date, ::yMMMMd}           April 3, 2026
{d, date, ::yMMMMEEEEd}       Saturday, April 3, 2026
{d, date, ::hms}              3:45:32 PM
{d, date, ::EEEEMMMdjmm}      Sat, Apr 3, 3:45 PM
```

### Recipe 15: Validate against CLDR rules per locale

```ts
// Build-time check — does locale 'ar' file have all 6 plural categories?
import { PluralRules } from 'intl-pluralrules';
const arRules = new Intl.PluralRules('ar');
const REQUIRED = ['zero', 'one', 'two', 'few', 'many', 'other'];
const present = new Set();
for (let n = 0; n < 200; n++) {
  present.add(arRules.select(n));
}
const missing = REQUIRED.filter(c => !present.has(c));
console.log({ missing });   // should be []
```

### Recipe 16: MessageFormat 2.0 preview

```
.match {$count :number}
0  {{No items}}
one {{One item}}
*  {{{$count} items}}
```

MF2 is a structural rewrite — more readable, better tool support. ICU 75+ has MF2 parser. Plan migration when MF2 ships in stable Intl.MessageFormat (likely 2026-2027).

## Examples

### Example 1: Add cart-count plural to a SaaS app

**Goal:** Display "5 items in cart" with correct plural in 6 locales (incl. AR + RU).

**Steps:**
1. Define in `en.json`: `{count, plural, =0 {Cart is empty} one {# item in cart} other {# items in cart}}`.
2. Push to Crowdin. Translators see ICU editor with per-locale plural categories.
3. AR translator fills `zero/one/two/few/many/other`. RU fills `one/few/many/other`.
4. Pull: `crowdin download`.
5. Lint: `formatjs lint 'lang/**/*.json'` → confirms each locale has required categories.
6. Compile: `formatjs compile lang/de.json --ast --out-file lang/compiled/de.json`.
7. Test:
   - `t({count: 0})` → "Cart is empty" (en); "سلة التسوق فارغة" (ar)
   - `t({count: 5})` → "5 items in cart" (en); "5 عناصر في سلة التسوق" (ar)

**Result:** All locales render grammatically correct counts; translators no longer file "plural form" bugs.

### Example 2: Gender + count nested for activity feed

**Goal:** "Alice uploaded 3 photos" with gender + count in 6 locales.

**Steps:**
1. Define nested message (Recipe 4) in `en.json`.
2. Source-side: `<FormattedMessage id="feed.photos" values={{ name, gender, count }} />`.
3. Crowdin opens nested ICU editor — translators see each combination.
4. Verify each locale handles gender + count combination correctly.
5. Test edge cases: gender unknown (`other`), count 0, count 1, count 10, count 100.

**Result:** Activity feed reads naturally in every locale; "they have 1 photos" bug eliminated.

## Edge cases / gotchas

- **`=0` vs `zero`** — `=0` is exact match (en `=0` "No items"). `zero` is CLDR category (Arabic uses for count=0, Welsh uses too). Use `=0` for special-case copy, `zero` for grammatical category.
- **`other` always required** — even Japanese (1 category) needs `other`. Tools fail without it.
- **`#` in literal text** — escape with `'#'` if you need literal hash sign.
- **Single quotes** — `'` escapes ICU syntax: `It's` must be `It''s` or use straight apostrophe `It's`.
- **Curly braces in literal** — escape with `'{'` and `'}'`.
- **MessageFormat 1 vs 2** — MF1 ships today; MF2 is preview. Don't ship MF2 to production unless explicitly experimenting.
- **HTML inside ICU** — possible but discouraged; use rich-text formatting via `<FormattedMessage>` chunks instead:
  ```tsx
  <FormattedMessage
    id="welcome"
    defaultMessage="Hello <b>{name}</b>"
    values={{ name: 'Alice', b: chunks => <b>{chunks}</b> }}
  />
  ```
- **CLDR data version** — Node 22 ships CLDR 45; Node 20 ships 44. New locale variants (e.g., 2024 additions) may need polyfill on older Node.
- **Plural number type** — ICU rules differ for cardinal (1 item, 2 items) vs ordinal (1st, 2nd). Use `plural` for cardinal, `selectordinal` for ordinal.
- **Decimal plurals** — `1.5` falls into `other` in English; AR/RU may treat as `few` or `many`. Test fractional counts.
- **Empty placeholder** — `{name}` with `name=""` renders empty space, not removed. Use conditional logic.
- **Performance** — uncompiled MF parsed on every render. Use `formatjs compile` for high-traffic pages.
- **Forbidden in some TMS UIs** — Lokalise's plural editor doesn't show ICU directly by default; switch to "ICU mode" in project settings.
- **Combining `select` + `plural`** — `select` first (outer), `plural` inner (Recipe 4); reversing causes most translators confusion.

## Sources

- ICU MessageFormat (FormatJS): https://formatjs.io/docs/icu-syntax
- intl-messageformat: https://www.npmjs.com/package/intl-messageformat
- ICU MessageFormat guide (Phrase): https://phrase.com/blog/posts/guide-to-the-icu-message-format/
- CLDR plural rules: https://cldr.unicode.org/index/cldr-spec/plural-rules
- CLDR plural categories: https://www.unicode.org/cldr/charts/47/supplemental/language_plural_rules.html
- FormatJS CLI: https://formatjs.io/docs/tooling/cli
- i18next-icu: https://github.com/i18next/i18next-icu
- next-intl ICU: https://next-intl.dev/docs/usage/messages
- Paraglide-js + MessageFormat: https://github.com/opral/paraglide-js
- MessageFormat 2.0 spec: https://github.com/unicode-org/message-format-wg
- ICU number skeletons: https://github.com/unicode-org/icu/blob/main/docs/userguide/format_parse/numbers/skeletons.md
