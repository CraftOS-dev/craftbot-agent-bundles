---
name: pseudo-localization
description: Pseudo-locale generation (accented + expanded source strings + bracket markers) for catching i18n bugs before paying for translation. pseudo-l10n npm + Crowdin ach + Lokalise qps-ploc + Playwright diff. Use when the user asks "pseudo-localize", "i18n smoke test", "catch hardcoded strings", "find layout overflow".
---

# Pseudo-Localization

Replace source strings with accented + expanded variants (`Ｈéllø Wörld!` → `⟦Ħéllø Wörld!⟧`) with 30-40% length padding. Catches **80%** of i18n bugs before a single translator is paid: hard-coded strings, layout overflow, concatenation, missing translation calls, encoding failures.

## When to use

- Starting i18n on an existing app — pseudo first, translate later.
- After any major refactor — pseudo catches re-introduced hardcoded strings.
- Before LSP handoff — pseudo round-trip verifies the catalog pipeline works.
- Reports of overflow in DE / FI / RU — pseudo simulates 30-40% expansion universally.

Trigger phrases: "pseudo-localize", "pseudoloc", "i18n smoke test", "hardcoded string check", "qps-ploc", "ach locale", "layout overflow test".

## Setup

```bash
# Local generation
npm i -g pseudo-l10n
pseudo-l10n --help

# Alternative — pseudoloc (Microsoft-derived)
npm i -g pseudoloc

# Python alternative
pip install pseudoloc

# Crowdin pseudo-locale — built in (ach distribution)
npm i -g @crowdin/cli

# Lokalise pseudo — qps-ploc test language
npm i -g @lokalise/cli-2
```

Auth/env: TMS tokens covered by `tms-setup-crowdin-lokalise-phrase`.

## Pseudo character mapping

```
a → å, b → ḅ, c → ċ, d → ḋ, e → é, f → ḟ, g → ġ, h → ḣ, i → í, ...
Brackets: ⟦ ... ⟧ to detect concatenation + missing translate calls
Padding: 30-40% extra length to simulate German/Finnish expansion
```

## Common recipes

### Recipe 1: Generate pseudo-locale catalog locally

```bash
pseudo-l10n input.json -o pseudo.json --expansion 0.35 --brackets

# Example transform:
# { "hello": "Hello, world!" } → { "hello": "⟦Ħéllø, ẅörlḋ! one two⟧" }
```

Options:
```
--expansion 0.35      30-40% length padding (DE/FI mimic)
--brackets            wrap with ⟦...⟧ (catches concat)
--accents             add diacritics (catches encoding bugs)
--rtl                 wrap with U+202E + U+202C (RTL simulation)
```

### Recipe 2: Programmatic pseudo (build-time)

```ts
// scripts/build-pseudo.ts
import fs from 'fs';
import { pseudoMap } from 'pseudo-l10n/lib/maps';

const en = JSON.parse(fs.readFileSync('locales/en.json', 'utf8'));

function pseudoize(s: string): string {
  const accented = s.split('').map(c => pseudoMap[c] || c).join('');
  // 35% expansion via filler
  const pad = '_'.repeat(Math.ceil(accented.length * 0.35));
  return `⟦${accented}${pad}⟧`;
}

function walk(obj: any): any {
  if (typeof obj === 'string') return pseudoize(obj);
  if (Array.isArray(obj)) return obj.map(walk);
  if (typeof obj === 'object' && obj !== null) {
    return Object.fromEntries(Object.entries(obj).map(([k, v]) => [k, walk(v)]));
  }
  return obj;
}

fs.writeFileSync('locales/ach.json', JSON.stringify(walk(en), null, 2));
```

### Recipe 3: Preserve ICU placeholders + HTML tags

ICU vars like `{count}` and HTML tags `<b>...</b>` must NOT be pseudo-ized:

```ts
function pseudoizeWithIcu(s: string): string {
  // Match {var}, {count, plural, ...}, <tag>, </tag>
  const segments = s.split(/(\{[^}]+\}|<\/?[^>]+>)/g);
  return '⟦' + segments.map((seg, i) =>
    i % 2 === 0 ? accentize(seg) : seg     // odd = placeholder, leave alone
  ).join('') + '⟧';
}
```

### Recipe 4: Crowdin pseudo via `ach` distribution

```bash
# Add `ach` (Acholi) as pseudo-target — Crowdin auto-pseudoizes
crowdin distribution add --name pseudo --target-language ach

# Get distribution hash
crowdin distribution list

# Use in app — pseudo strings stream from Crowdin OTA
```

App side:
```ts
import OtaClient from '@crowdin/ota-client';
const client = new OtaClient('<DIST_HASH>');
if (locale === 'ach') {
  const strings = await client.getStringsByLocale('ach');
  // Crowdin returns pre-pseudoized strings
}
```

### Recipe 5: Lokalise pseudo via `qps-ploc`

```bash
# Upload en source → Lokalise auto-creates qps-ploc test language
lokalise2 file upload \
  --token $LOKALISE_API_TOKEN --project-id $PID \
  --file=en.json --lang-iso=en

# In Lokalise project settings → Languages → enable qps-ploc as test target
# Lokalise auto-generates pseudo entries

lokalise2 file download \
  --token $LOKALISE_API_TOKEN --project-id $PID \
  --filter-langs=qps-ploc --format=json
```

### Recipe 6: Phrase pseudo via custom locale

```bash
# Add custom locale 'pseudo' to project
curl -X POST "https://api.phrase.com/v2/projects/<PID>/locales" \
  -H "Authorization: token $PHRASE_TOKEN" \
  -d '{"locale":{"name":"pseudo","code":"pseudo"}}'

# Phrase auto-applies pseudoization rules to this locale
```

### Recipe 7: Playwright pseudo screenshot diff

```ts
// tests/pseudo.spec.ts
import { test, expect } from '@playwright/test';

test('pseudo locale — no overflow on key pages', async ({ page }) => {
  const PAGES = ['/', '/checkout', '/settings', '/profile'];
  for (const pg of PAGES) {
    await page.goto(`http://staging.app.com/ach${pg}`);
    // Verify brackets present in DOM (catches missing translate calls)
    const hasBrackets = await page.evaluate(() => document.body.innerText.includes('⟦'));
    expect(hasBrackets).toBe(true);

    await expect(page).toHaveScreenshot(`pseudo${pg.replace('/', '-')}.png`, {
      maxDiffPixelRatio: 0.02, fullPage: true,
    });
  }
});

test('no untranslated English in pseudo build', async ({ page }) => {
  await page.goto('http://staging.app.com/ach/');
  // Common English words shouldn't appear in pseudo (would indicate hardcoded)
  const englishOnly = await page.evaluate(() => {
    const text = document.body.innerText;
    return text.match(/\b(checkout|settings|profile|save|cancel|submit)\b/gi) || [];
  });
  expect(englishOnly.length).toBeLessThan(3);  // small tolerance for unavoidable English
});
```

### Recipe 8: Locale switcher with pseudo option (dev mode only)

```tsx
// LocaleSwitcher.tsx
const LOCALES = process.env.NODE_ENV === 'production'
  ? ['en', 'de', 'fr', 'ja', 'ar']
  : ['en', 'de', 'fr', 'ja', 'ar', 'ach'];   // pseudo only in dev/staging

return (
  <select onChange={e => setLocale(e.target.value)}>
    {LOCALES.map(l => (
      <option key={l} value={l}>{l === 'ach' ? '⟦Pseudo⟧' : labels[l]}</option>
    ))}
  </select>
);
```

### Recipe 9: Watch script — regenerate pseudo on en.json change

```bash
# Auto-rebuild pseudo on source change
npm i -D chokidar-cli
npx chokidar 'locales/en.json' -c 'pseudo-l10n locales/en.json -o locales/ach.json --expansion 0.35 --brackets'
```

### Recipe 10: CI gate — pseudo must build cleanly

```yaml
# .github/workflows/pseudo.yml
name: Pseudo i18n Smoke Test
on: pull_request
jobs:
  pseudo:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm i -g pseudo-l10n
      - run: pseudo-l10n locales/en.json -o locales/ach.json --expansion 0.35 --brackets
      - run: npm run build
      - run: npx playwright test pseudo.spec.ts
```

### Recipe 11: Pseudo for non-Latin scripts (catches CJK font issues)

```ts
// Pseudo for testing CJK font + width
function pseudoCjk(s: string): string {
  // Substitute Latin with CJK-width fillers
  return s.replace(/[a-zA-Z]/g, '○');  // Each Latin char → full-width circle
}
```

### Recipe 12: Test plural code paths via pseudo

ICU plural categories: zero/one/two/few/many/other. Pseudo should generate per-category strings:
```json
{
  "cart.items": "⟦{count, plural, =0 {Ņ̃ ḯṫéṁś___} one {# ḯṫéṁ____} other {# ḯṫéṁś____}}⟧"
}
```

Test with various counts: 0, 1, 2, 5, 21, 100.

## Examples

### Example 1: Pre-translation pseudo audit on a 500-key catalog

**Goal:** Find all hardcoded strings + layout overflow before paying $5k for DE translation.

**Steps:**
1. Generate pseudo: `pseudo-l10n locales/en.json -o locales/ach.json --expansion 0.35 --brackets`.
2. Add `ach` to locale switcher (dev only, Recipe 8).
3. Build app, run staging: `staging.app.com/ach/`.
4. Walk the app — any plain English (no brackets, no accents) is hardcoded.
5. Fix each hardcoded string (move to `en.json`, regenerate pseudo).
6. Take Playwright screenshots (Recipe 7) — overflow shows in pseudo.
7. Fix CSS: longer label widths, flexible containers.
8. Hand off `en.json` to LSP only after pseudo is clean.

**Result:** 80% of i18n bugs caught for free; LSP receives clean source; downstream cost down 20-40%.

### Example 2: Continuous pseudo gate via CI

**Goal:** Every PR is pseudo-validated; regressions can't merge.

**Steps:**
1. Add CI workflow (Recipe 10) — runs on every PR.
2. PR introduces `<button>Submit</button>` (hardcoded English) instead of `{t('button.submit')}`.
3. Pseudo gen runs → `ach.json` doesn't contain "Submit" → Playwright DOM check (Recipe 7) finds "Submit" without brackets.
4. CI fails with "Hardcoded English string detected in /checkout".
5. Developer fixes — uses `t()` call. CI passes.

**Result:** Hardcoded strings never reach main.

## Edge cases / gotchas

- **ICU placeholders MUST be preserved** — `{count}` and `<b>` tags get accented otherwise. Use Recipe 3 pattern.
- **Plural keys** — pseudo with plurals breaks if ICU rules are stripped. Either preserve ICU syntax OR pseudoize each plural branch separately.
- **`ach` (Acholi) is a real language** — Crowdin reuses it as pseudo by convention; not a real Acholi translation. Don't confuse users.
- **`qps-ploc` is a Microsoft convention** — "pseudo Latin" tag; some BCP 47 validators flag as invalid. It's a private-use tag and works in Lokalise.
- **`x-pseudo` / `xx-Hant` private tags** — alternative pseudo tags; may break framework locale validation. Stick with `ach` or `qps-ploc`.
- **Pseudo expansion ≠ all locales** — Vietnamese/Polish can be 20-30% longer; German 30-50%; Finnish 40-50%. 35% is a reasonable median.
- **Bracket marker rendering** — `⟦⟧` chars require font with U+27E6 / U+27E7 support; falls back to boxes on some Linux systems. Verify font stack.
- **RTL pseudo** — wrapping in U+202E / U+202C simulates RTL but doesn't catch real bidi issues. Use real Arabic for RTL testing (see `rtl-cjk-layout-testing`).
- **Don't ship pseudo to production** — gate behind feature flag or environment check (Recipe 8). Otherwise users see gibberish.
- **Search engines index pseudo URLs** — block via `robots.txt`: `Disallow: /ach/`.
- **Long pseudo strings break tests** — if test asserts exact text, pseudo breaks it. Use placeholder-aware assertions: `expect(button).toContainText(t('submit'))`.
- **MT pre-translate skips pseudo** — Crowdin/Lokalise won't run MT against `ach`/`qps-ploc` by default; pseudo is generated server-side, not translated.
- **Pseudo doesn't catch wrong-locale data** — date/number/currency formatting bugs (e.g., DE always commas) need real-locale testing.

## Sources

- pseudo-l10n: https://www.npmjs.com/package/pseudo-l10n
- pseudoloc: https://www.npmjs.com/package/pseudoloc
- pseudo-localization for automated i18n testing: https://dev.to/anton_antonov/pseudo-localization-for-automated-i18n-testing-31
- l10n.dev pseudo guide: https://l10n.dev/help/pseudo-localization
- Crowdin pseudo-localization: https://support.crowdin.com/pseudo-localization/
- Lokalise placeholder language: https://docs.lokalise.com/en/articles/1626608-placeholder-language
- Microsoft pseudo (qps-ploc): https://learn.microsoft.com/en-us/globalization/methodology/pseudo-localization
- ICU MessageFormat: https://formatjs.io/docs/icu-syntax
