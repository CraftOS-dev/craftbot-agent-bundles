---
name: locale-qa-linguistic-functional
description: Locale-specific QA — linguistic (Xbench, Okapi Checkmate, Vale) and functional (Playwright screenshot diff). Use when the user asks "QA our translations", "check for terminology mismatches", "automated locale gate in CI", or "find layout regressions per locale".
---

# Locale QA — Linguistic + Functional

Two layers run against every locale release: **linguistic** (Xbench / Checkmate / Vale = terminology, segments, tags, prose) and **functional** (Playwright screenshot diff = layout, overflow, truncation). Run both as CI gates before publish.

## When to use

- A locale batch came back from LSP — run linguistic QA before merging.
- Layout regressed in DE / JA / AR — Playwright screenshot diff catches it.
- Terminology drift across translators — Xbench / Checkmate flags mismatches.
- Prose style issues in source-language strings — Vale linter.
- Want a CI gate so bad locales never reach production.

Trigger phrases: "QA translations", "Xbench", "Checkmate", "screenshot diff", "locale regression", "terminology check", "linguistic QA".

## Setup

```bash
# Xbench (Windows GUI — ApSIC; free for individuals)
# Download: https://www.xbench.net/index.php/download

# Okapi Checkmate (cross-platform — Java GUI + CLI)
pipx install okapi-tools
tikal -lc input.xlf -o qa-report.html         # batch QA

# Vale (prose linter)
brew install vale
# OR: curl -fsSL https://github.com/errata-ai/vale/releases/latest/download/vale_macos.tar.gz | tar xz

# Playwright
npm i -D @playwright/test
npx playwright install
```

Auth/env: none for QA tools themselves. Playwright tests need access to staging URLs.

## Common recipes

### Recipe 1: Xbench — terminology + segment QA on bilingual XLIFF

GUI workflow:
```
1. File → New Project → name "release-2026-Q3"
2. Add Files → Bilingual XLIFF → drop *.sdlxliff / *.mqxliff / *.xliff
3. Add Glossary → load brand.tbx
4. Add Checklist → terminology, untranslated, double spaces, brackets
5. Run QA → export HTML report
```

CLI bridge (when Xbench Enterprise installed):
```bash
xbench.exe -p release-2026-Q3.xbp -r qa-report.html -checklists "terminology,segments,format"
```

### Recipe 2: Okapi Checkmate (Tikal CLI) — cross-platform QA

```bash
# Single XLIFF
tikal -lc translated.xlf -tb brand.tbx -o qa-report.html

# Batch directory
for f in locales/*.xlf; do
  tikal -lc "$f" -tb brand.tbx -o "qa-reports/$(basename $f .xlf).html"
done

# JSON output for CI parsing
tikal -lc translated.xlf -of json -o qa.json
jq '[.issues[] | select(.severity == "error")] | length' qa.json
```

### Recipe 3: Vale custom L10n style pack

```yaml
# .vale.ini
StylesPath = .vale/styles
MinAlertLevel = warning
Vocab = L10n

[*.md]
BasedOnStyles = L10n
```

```yaml
# .vale/styles/L10n/Idioms.yml
extends: existence
message: "'%s' is an idiom — will not translate cleanly."
level: error
ignorecase: true
tokens:
  - hit it out of the park
  - low-hanging fruit
  - circle back
  - boil the ocean
  - touch base
  - move the needle
  - drink the kool-aid
  - in the weeds
  - on the same page
```

```bash
vale --output=JSON docs/ > vale-report.json
jq '[.[] | .[] | select(.Severity == "error")] | length' vale-report.json
```

### Recipe 4: Playwright screenshot diff across locales

```ts
// tests/i18n-grid.spec.ts
import { test, expect } from '@playwright/test';

const LOCALES = [
  { code: 'en-US', dir: 'ltr' },
  { code: 'de-DE', dir: 'ltr' },         // German — 30%+ longer than English
  { code: 'fi-FI', dir: 'ltr' },         // Finnish — even longer
  { code: 'ja-JP', dir: 'ltr' },         // Japanese — vertical density, font fallback
  { code: 'ar',    dir: 'rtl' },         // RTL — full layout flip
  { code: 'he-IL', dir: 'rtl' },
  { code: 'zh-Hans-CN', dir: 'ltr' },
  { code: 'ach',   dir: 'ltr' },         // pseudo — 30-40% expansion
];

const PAGES = ['/', '/checkout', '/settings', '/profile'];

for (const loc of LOCALES) {
  for (const pg of PAGES) {
    test(`${loc.code} ${pg}`, async ({ page }) => {
      await page.goto(`http://staging.app.com/${loc.code}${pg}`);
      const html = page.locator('html');
      await expect(html).toHaveAttribute('dir', loc.dir);
      await expect(html).toHaveAttribute('lang', loc.code);
      await expect(page).toHaveScreenshot(`${loc.code}-${pg.replace('/', '-') || 'home'}.png`, {
        maxDiffPixelRatio: 0.02,
        fullPage: true,
      });
    });
  }
}
```

```bash
# Run; update baselines on first run
npx playwright test --update-snapshots i18n-grid

# Subsequent runs detect regressions
npx playwright test i18n-grid
```

### Recipe 5: Tag balance check on XLIFF

```bash
# Inline tags ({var}, <strong>, <link>) must round-trip from source to target
python -c "
import lxml.etree as ET
import re
tree = ET.parse('translated.xlf')
issues = []
for tu in tree.xpath('//trans-unit'):
    source_tags = re.findall(r'\{[a-zA-Z_]+\}|<[^>]+>', tu.findtext('source') or '')
    target_tags = re.findall(r'\{[a-zA-Z_]+\}|<[^>]+>', tu.findtext('target') or '')
    if sorted(source_tags) != sorted(target_tags):
        issues.append({'id': tu.get('id'), 'src': source_tags, 'tgt': target_tags})
print(f'Tag mismatch in {len(issues)} segments')
"
```

### Recipe 6: ICU MessageFormat syntax lint

```bash
npm i -g @formatjs/cli
formatjs lint 'locales/**/*.json'        # validates ICU plural/select syntax

# Errors look like:
# [ERROR] locales/de.json: Plural rule "many" missing for 'cart.items'
```

### Recipe 7: Untranslated string detection

```bash
# Compare en.json (source) → de.json (target). If de value == en value, it's untranslated.
python -c "
import json
en = json.load(open('locales/en.json'))
de = json.load(open('locales/de.json'))
unchanged = [k for k, v in en.items() if de.get(k) == v]
print(f'{len(unchanged)} potentially untranslated keys in de.json')
"
```

### Recipe 8: Forbidden term detection (DNT enforcement)

```bash
# Brand terms that must never appear translated
DNT_TERMS=("API" "SDK" "CraftBot")
for term in "${DNT_TERMS[@]}"; do
  if jq -r 'to_entries | .[] | .value' locales/de.json | grep -qE "(API ?Schnittstelle|Software-Entwicklungs-Kit|Bastel-Bot)"; then
    echo "FORBIDDEN: $term was translated in de.json"
    exit 1
  fi
done
```

### Recipe 9: CI gate — combined QA

```yaml
# .github/workflows/locale-qa.yml
name: Locale QA
on: pull_request
jobs:
  qa:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm i
      - name: ICU lint
        run: npx formatjs lint 'locales/**/*.json'
      - name: Vale prose
        uses: errata-ai/vale-action@v2
        with:
          files: locales/
      - name: Okapi Checkmate
        run: |
          pipx install okapi-tools
          for f in locales/*.xlf; do tikal -lc "$f" -of json -o "$f.qa.json"; done
          jq -s '[.[].issues[] | select(.severity == "error")] | length' locales/*.qa.json | tee /tmp/err
          [ "$(cat /tmp/err)" -eq 0 ]
      - name: Playwright screenshot
        run: npx playwright test --reporter=github i18n-grid
```

### Recipe 10: Per-locale QA dashboard

Aggregate per-translator + per-locale + per-domain scores:
```bash
# Crowdin QA report API
curl -L "https://api.crowdin.com/api/v2/projects/<PID>/reports" \
  -H "Authorization: Bearer $CROWDIN_PERSONAL_TOKEN" \
  -X POST -d '{"name":"top-members","schema":{"unit":"strings","languageId":"de"}}'
```

### Recipe 11: Length / truncation check

```bash
# DE > 130% of EN source length — likely overflows UI
python -c "
import json
en = json.load(open('locales/en.json'))
de = json.load(open('locales/de.json'))
for k, en_val in en.items():
    de_val = de.get(k, '')
    if de_val and len(de_val) > len(en_val) * 1.4:
        print(f'{k}: en={len(en_val)} de={len(de_val)} (+{int((len(de_val)/len(en_val)-1)*100)}%)')
"
```

### Recipe 12: A11y check on translated content

```bash
# axe-core under Playwright per locale
npm i -D @axe-core/playwright
```

```ts
import AxeBuilder from '@axe-core/playwright';

test('a11y per locale', async ({ page }) => {
  for (const locale of ['en-US', 'de-DE', 'ar', 'ja-JP']) {
    await page.goto(`/${locale}/`);
    const results = await new AxeBuilder({ page }).analyze();
    expect(results.violations).toEqual([]);
  }
});
```

## Examples

### Example 1: CI gate catches a forbidden-term violation before merge

**Goal:** Prevent vendor from translating "API" as "Schnittstelle" in DE strings.

**Steps:**
1. Vendor delivers `de.json` via Crowdin PR.
2. GitHub Action triggers (Recipe 9): ICU lint → Vale → Checkmate → Playwright.
3. Recipe 8's forbidden-term check finds "Schnittstelle" in error message string.
4. CI fails PR; reviewer comments; vendor fixes; re-runs.

**Result:** Bad term never reaches production; vendor learns the constraint.

### Example 2: Find Arabic layout regression after CSS refactor

**Goal:** Recent CSS change broke RTL alignment; need to find the page.

**Steps:**
1. Capture baseline screenshots before refactor: `npx playwright test --update-snapshots i18n-grid`.
2. After refactor, run: `npx playwright test i18n-grid`.
3. Playwright HTML report shows pixel diffs per page × locale.
4. Open the `ar` columns → identify `/checkout` regressed (sidebar misaligned).
5. Inspect element, see lingering `margin-left: 16px` in new code.
6. Fix to `margin-inline-start: 16px`; rerun; passes.

**Result:** Layout regression caught pre-deploy; CSS Logical Properties pattern reinforced.

## Edge cases / gotchas

- **Xbench is Windows-only** — for macOS/Linux teams, use Okapi Checkmate; covers 90% of the same checks.
- **Xbench Enterprise CLI is paid** — free version is GUI-only. Use Okapi Tikal for CLI in CI.
- **Playwright snapshot fonts vary by OS** — use a single Linux runner for baseline + diff; or use `playwright/test:focal` Docker image; otherwise rendering differs.
- **CJK fonts in Linux runners** — `apt-get install -y fonts-noto-cjk` before Playwright run, otherwise tofu boxes.
- **Pseudo-locale Playwright run** — `ach` includes bracket markers `⟦...⟧`; baseline screenshot accordingly.
- **Vale + locale strings** — Vale designed for prose; on JSON locale strings, use `jq` to extract values + pipe to Vale: `jq -r 'to_entries | .[] | .value' en.json | vale --in=text`.
- **Tag mismatch false positives** — when locale wraps a phrase differently. Use semantic tag comparison (count by name, not by position).
- **`maxDiffPixelRatio: 0.02`** — 2% pixel tolerance is forgiving for anti-aliasing; lower to 0.005 for strict.
- **Screenshot grid scale** — 5 locales × 10 pages × 3 viewports = 150 screenshots. Limit grid to critical pages; expand opportunistically.
- **Untranslated detection false positives** — proper nouns ("Berlin", "Tokyo") legitimately untranslated. Mark with `do_not_translate` flag in TMS; QA pre-allows them.
- **ICU lint cost** — `formatjs lint` on large catalogs (50k+ keys) takes minutes; cache or split by file.

## Sources

- Xbench: https://docs.xbench.net/user-guide/overview/
- Xbench checklists: https://docs.xbench.net/user-guide/check-types/
- Okapi Framework: https://okapiframework.org/
- Tikal CLI: https://okapiframework.org/wiki/index.php?title=Tikal
- Checkmate: https://okapiframework.org/wiki/index.php?title=CheckMate
- Vale prose linter: https://vale.sh/
- Vale GitHub Action: https://github.com/errata-ai/vale-action
- FormatJS CLI: https://formatjs.io/docs/tooling/cli
- Playwright screenshots: https://playwright.dev/docs/test-snapshots
- BrowserStack i18n testing: https://www.browserstack.com/guide/internationalization-testing-of-websites-and-apps
- axe-core Playwright: https://github.com/dequelabs/axe-core-npm
