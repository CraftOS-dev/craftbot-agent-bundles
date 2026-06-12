---
name: gender-name-address-currency-localization
description: Per-locale conventions — name order, address format, currency, date/time/number formatting via Intl.* APIs + CLDR data. Use when the user asks "format date for ja-JP", "address fields for DE", "currency JPY no decimals", "name order ja vs en".
---

# Gender, Name, Address, Currency Localization

`Intl.*` browser APIs + CLDR drive correct per-locale formatting. Don't hand-roll. CLDR data ships with browsers + Node 22+; covers dates, numbers, currency, plural rules, name order, list formatting, relative time, segmentation.

## When to use

- The user is rendering dates, numbers, currency, percentages.
- Building address forms that adapt per locale.
- Implementing user-facing name fields (single field vs given/family).
- Handling pluralized relative time ("3 minutes ago", "in 2 hours").
- Sort/collation operations on user-visible lists.

Trigger phrases: "format date", "format currency", "address fields", "name order", "Intl", "CLDR", "collation", "RelativeTimeFormat".

## Setup

```bash
# Browser-native — no install (Node 22+ ships full CLDR)

# Polyfills for older targets
npm i @formatjs/intl-numberformat
npm i @formatjs/intl-datetimeformat
npm i @formatjs/intl-relativetimeformat
npm i @formatjs/intl-listformat
npm i @formatjs/intl-pluralrules
npm i @formatjs/intl-locale

# Address — country form data
npm i i18n-postal-address
npm i libpostal           # heavyweight parser

# Country/region data
npm i countries-list
npm i @cospired/i18n-iso-languages
```

Auth/env: none required.

## Common recipes

### Recipe 1: Intl.DateTimeFormat

```ts
const date = new Date('2026-04-03T15:45:00');

new Intl.DateTimeFormat('en-US', { dateStyle: 'long' }).format(date);
// "April 3, 2026"

new Intl.DateTimeFormat('en-GB', { dateStyle: 'long' }).format(date);
// "3 April 2026"

new Intl.DateTimeFormat('ja-JP', { dateStyle: 'long' }).format(date);
// "2026年4月3日"

new Intl.DateTimeFormat('ar', { dateStyle: 'long' }).format(date);
// "٣ أبريل ٢٠٢٦"

new Intl.DateTimeFormat('zh-Hans-CN', { dateStyle: 'full', timeStyle: 'short' }).format(date);
// "2026年4月3日星期五 15:45"
```

Styles: `full`, `long`, `medium`, `short` for date + time independently.

### Recipe 2: Intl.NumberFormat — currency

```ts
new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(1234.56);
// "1.234,56 €"

new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(1234.56);
// "$1,234.56"

new Intl.NumberFormat('ja-JP', { style: 'currency', currency: 'JPY' }).format(1234);
// "¥1,234"  ← no decimals (CLDR knows JPY/KRW/VND)

new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(123456.78);
// "₹1,23,456.78"  ← Indian grouping (lakh + crore)

new Intl.NumberFormat('ar', { style: 'currency', currency: 'AED' }).format(1234.56);
// "‏١٬٢٣٤٫٥٦ د.إ."  ← Arabic-Indic digits
```

### Recipe 3: Compact / scientific number

```ts
new Intl.NumberFormat('en-US', { notation: 'compact' }).format(1234567);
// "1.2M"

new Intl.NumberFormat('de-DE', { notation: 'compact' }).format(1234567);
// "1,2 Mio."

new Intl.NumberFormat('ja-JP', { notation: 'compact' }).format(12345);
// "1.2万"

new Intl.NumberFormat('en-US', { notation: 'scientific' }).format(1234.56);
// "1.235E3"
```

### Recipe 4: Intl.RelativeTimeFormat

```ts
const rtf = new Intl.RelativeTimeFormat('en-US', { numeric: 'auto' });
rtf.format(-1, 'day');     // "yesterday"
rtf.format(0, 'day');      // "today"
rtf.format(2, 'day');      // "in 2 days"
rtf.format(-3, 'month');   // "3 months ago"

new Intl.RelativeTimeFormat('ja-JP', { numeric: 'auto' }).format(-1, 'day');
// "昨日"

new Intl.RelativeTimeFormat('ar', { numeric: 'auto' }).format(-3, 'minute');
// "قبل ٣ دقائق"
```

### Recipe 5: Intl.ListFormat

```ts
new Intl.ListFormat('en-US', { style: 'long', type: 'conjunction' }).format(['Alice', 'Bob', 'Carol']);
// "Alice, Bob, and Carol"

new Intl.ListFormat('de-DE').format(['Alice', 'Bob', 'Carol']);
// "Alice, Bob und Carol"

new Intl.ListFormat('ja-JP').format(['アリス', 'ボブ', 'キャロル']);
// "アリス、ボブ、およびキャロル"

new Intl.ListFormat('ar').format(['أ', 'ب', 'ج']);
// "أ، وب، وج"
```

### Recipe 6: Intl.PluralRules

```ts
const pr = new Intl.PluralRules('en-US');
pr.select(0);    // "other"
pr.select(1);    // "one"
pr.select(2);    // "other"

new Intl.PluralRules('ar').select(2);    // "two"
new Intl.PluralRules('ru').select(2);    // "few"
new Intl.PluralRules('ja').select(5);    // "other"
```

Use to drive plural keys without ICU MessageFormat:
```ts
const cat = new Intl.PluralRules(locale).select(count);
const key = `items.${cat}`;  // "items.one", "items.other"
```

### Recipe 7: Intl.Collator (locale-aware sort)

```ts
const items = ['Zürich', 'Zurich', 'Adams', 'Müller', 'Mueller'];

[...items].sort(new Intl.Collator('de-DE').compare);
// ['Adams', 'Mueller', 'Müller', 'Zurich', 'Zürich']

[...items].sort(new Intl.Collator('sv-SE').compare);
// ['Adams', 'Mueller', 'Müller', 'Zurich', 'Zürich']   ← Swedish treats Ü differently

new Intl.Collator('en', { sensitivity: 'base' }).compare('Müller', 'Muller');
// 0  ← ignores accents
```

### Recipe 8: Intl.Segmenter (CJK word segmentation)

```ts
const segmenter = new Intl.Segmenter('ja-JP', { granularity: 'word' });
const segs = [...segmenter.segment('東京の天気')];
// [{ segment: '東京', ...}, { segment: 'の', ...}, { segment: '天気', ...}]
```

Crucial for Japanese / Chinese / Thai (no spaces) where text breaking can't use whitespace.

### Recipe 9: Name order per locale

```ts
const NAME_ORDER = {
  // Family-given (Eastern Asian, Hungarian)
  'ja': 'family-given',
  'ko': 'family-given',
  'zh-Hans': 'family-given',
  'zh-Hant': 'family-given',
  'hu': 'family-given',
  'vi': 'family-given',
  // Given-family (default Western)
  'default': 'given-family',
};

function formatName(given, family, locale) {
  const order = NAME_ORDER[locale.split('-')[0]] || NAME_ORDER.default;
  return order === 'family-given'
    ? `${family}${family && given ? ' ' : ''}${given}`
    : `${given}${given && family ? ' ' : ''}${family}`;
}

// Japanese: 山田 太郎 (Yamada Taro)
// English: Alice Smith
```

ICU offers `Intl.DisplayNames` for name fields, but locale-correct name order is not yet in Intl. Use rule above.

### Recipe 10: Address fields per locale

Don't render `street\ncity, state ZIP` for everyone. Different countries have different field orders + names.

```ts
const ADDRESS_FORMATS = {
  US: ['street1', 'street2', 'city', 'state', 'zip'],          // street, city, state ZIP
  DE: ['street', 'zip city'],                                   // Strasse Nr. / PLZ Stadt
  JP: ['zip', 'prefecture', 'city', 'street'],                  // postal → prefecture → city → street
  UK: ['street1', 'street2', 'city', 'postcode'],
  CN: ['province', 'city', 'district', 'street'],
  IN: ['street1', 'street2', 'city', 'state', 'pin'],
  BR: ['street', 'number', 'neighborhood', 'city', 'state', 'cep'],
  AR: ['street', 'city', 'province', 'postal'],
};
```

Use `i18n-postal-address` library for canonical format strings.

### Recipe 11: Postal code validation per country

```ts
import postcodeValidator from 'postcode-validator';

postcodeValidator.validate('10115', 'DE');       // true (Berlin)
postcodeValidator.validate('100-0001', 'JP');    // true
postcodeValidator.validate('SW1A 1AA', 'GB');    // true
postcodeValidator.validate('1234', 'US');        // false (US ZIP needs 5 digits)
```

### Recipe 12: Phone number per locale

```bash
npm i libphonenumber-js
```

```ts
import { parsePhoneNumber } from 'libphonenumber-js';

const p = parsePhoneNumber('+4915155555555');
p.country;                  // 'DE'
p.formatInternational();    // "+49 1515 555 5555"
p.formatNational();         // "01515 5555555"
```

### Recipe 13: Currency code list (CLDR)

```ts
// Get display name for currency in locale
new Intl.DisplayNames('en-US', { type: 'currency' }).of('JPY');
// "Japanese Yen"

new Intl.DisplayNames('ja-JP', { type: 'currency' }).of('USD');
// "米ドル"
```

### Recipe 14: Language / region display name

```ts
new Intl.DisplayNames('en-US', { type: 'language' }).of('ja');
// "Japanese"

new Intl.DisplayNames('de-DE', { type: 'region' }).of('JP');
// "Japan"

new Intl.DisplayNames('zh-Hans-CN', { type: 'language' }).of('en');
// "英语"
```

### Recipe 15: Measurement unit

```ts
new Intl.NumberFormat('en-US', { style: 'unit', unit: 'kilometer' }).format(5);
// "5 km"

new Intl.NumberFormat('en-US', { style: 'unit', unit: 'celsius', unitDisplay: 'long' }).format(20);
// "20 degrees Celsius"

new Intl.NumberFormat('en-US', { style: 'unit', unit: 'fahrenheit' }).format(68);
// "68°F"
```

### Recipe 16: Calendar / non-Gregorian

```ts
new Intl.DateTimeFormat('ja-JP-u-ca-japanese', { era: 'long' }).format(new Date());
// "令和8年6月11日"  ← Japanese era

new Intl.DateTimeFormat('th-TH-u-ca-buddhist').format(new Date());
// Thai Buddhist calendar

new Intl.DateTimeFormat('ar-SA-u-ca-islamic').format(new Date());
// Islamic Hijri calendar
```

### Recipe 17: Number system override

```ts
new Intl.NumberFormat('ar', { numberingSystem: 'arab' }).format(123);
// "١٢٣"

new Intl.NumberFormat('ar', { numberingSystem: 'latn' }).format(123);
// "123"  ← force Latin digits
```

## Examples

### Example 1: Build a locale-aware checkout summary

**Goal:** Render "$1,234.56 USD on Apr 3, 2026" with correct format per locale.

**Steps:**
1. Determine locale + currency: `const locale = 'de-DE'; const currency = 'EUR';`
2. Currency: `new Intl.NumberFormat(locale, { style: 'currency', currency }).format(amount)` → "1.234,56 €"
3. Date: `new Intl.DateTimeFormat(locale, { dateStyle: 'long' }).format(date)` → "3. April 2026"
4. Combine via ICU MessageFormat:
   ```
   {amount, number, ::currency/EUR} on {date, date, ::yMMMd}
   ```
5. Test ja-JP with JPY — confirm no decimals; AR with AED — confirm Arabic-Indic digits.

**Result:** Checkout summary reads naturally in every locale.

### Example 2: Address form that adapts to country

**Goal:** Address form fields rearrange based on selected country.

**Steps:**
1. Country dropdown triggers form re-render.
2. Look up `ADDRESS_FORMATS[country]` (Recipe 10) → array of field IDs in order.
3. Render fields with locale-appropriate labels: "ZIP" (US) vs "PLZ" (DE) vs "郵便番号" (JP).
4. Validate postal code per country (Recipe 11).
5. Display formatted address on review screen — JP shows postal first, US shows postal last.

**Result:** Local users see familiar address forms; data validates correctly per country.

## Edge cases / gotchas

- **`Intl` is part of ECMAScript spec, not a polyfill needed in modern browsers** — but data sizes vary. Chrome ships full CLDR; older Node may not.
- **`numeric: 'auto'` vs `'always'`** — `auto` returns "yesterday" / "today"; `always` returns "1 day ago" / "0 days ago". Pick per UI.
- **`zh-CN` defaults to `zh-Hans-CN`** — explicit script (`zh-Hans-CN`, `zh-Hant-TW`) preferred.
- **Currency `JPY` rendering** — CLDR knows JPY has no minor units. Don't pass `minimumFractionDigits: 2` (overrides correct behavior).
- **Indian number grouping (`en-IN`)** — uses lakh (1,00,000) and crore (1,00,00,000), not 1,000,000. Auto-handled by Intl when locale is `en-IN`.
- **`en-US` collation ≠ alphabetical** — case-insensitive by default. Override with `sensitivity: 'variant'` for strict.
- **Japanese calendar era** — must include `-u-ca-japanese` extension; new era from 2019 (Reiwa) requires CLDR ≥ 35.
- **Arabic numbers in form inputs** — even if display uses Arabic-Indic digits, accept both: `String(input).replace(/[٠-٩]/g, d => String.fromCharCode(d.charCodeAt(0) - 1632))`.
- **Locale fallback chain** — `Intl.DateTimeFormat('xx-YY')` falls back to `xx` then default. `Intl.DateTimeFormat.supportedLocalesOf()` checks.
- **Address format != phone format != postal code format** — three separate libraries; don't conflate.
- **Hungarian name order** — `hu` uses family-given (like CJK). Easy to miss.
- **Name parsing single-field** — `John Smith Jr.` has 3 parts; `de la Cruz` has 3 words but is one surname. Don't split blindly.
- **CLDR data freshness** — Node updates CLDR lag months behind official. Critical for new currency rollouts (BRL revaluation, etc.).
- **Spelling for currency in title case** — `Intl.NumberFormat(..., { currencyDisplay: 'name' })` returns "US dollars" not "US Dollars"; capitalize in UI if needed.
- **`Intl.Locale.textInfo.direction`** — Safari < 17 lacks; use direction lookup table fallback.

## Sources

- MDN Intl: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl
- Intl.DateTimeFormat: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat
- Intl.NumberFormat: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat
- Intl.RelativeTimeFormat: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/RelativeTimeFormat
- Intl.PluralRules: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/PluralRules
- Intl.ListFormat: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/ListFormat
- Intl.Segmenter: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/Segmenter
- Intl.DisplayNames: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DisplayNames
- CLDR: https://cldr.unicode.org/
- FormatJS polyfills: https://formatjs.io/docs/polyfills/
- libphonenumber-js: https://www.npmjs.com/package/libphonenumber-js
- postcode-validator: https://www.npmjs.com/package/postcode-validator
- i18n-postal-address: https://www.npmjs.com/package/i18n-postal-address
