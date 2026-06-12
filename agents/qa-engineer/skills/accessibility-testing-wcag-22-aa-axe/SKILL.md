<!--
Source: https://www.deque.com/axe/axe-core/ · https://pa11y.org/ · https://www.w3.org/WAI/WCAG22/quickref/
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Accessibility Testing — WCAG 2.2 AA (axe-core + pa11y + Lighthouse + manual)

The 2026 QA-side a11y toolchain is layered: **axe-core** (~57% automated WCAG
detection) embedded via `@axe-core/playwright` in E2E + **pa11y-ci** for
sitemap sweeps + **Lighthouse CI** for budgets + **manual** NVDA/JAWS/
VoiceOver passes for the 43% automation can't catch. The QA owns the suite,
the gate, and the manual playbook; the frontend agent owns component-level
a11y.

## When to use

- Accessibility audit before launch or regulated release
- Setting up a11y CI gate for the first time
- Manual screen-reader / keyboard verification for a critical flow
- WCAG 2.2 AA compliance evidence for procurement / VPAT
- Trigger phrases: "a11y", "accessibility", "WCAG", "axe", "pa11y",
  "Lighthouse", "screen reader", "VPAT", "ACCR"

## Setup

```bash
# CLI
npm i -g @axe-core/cli pa11y pa11y-ci lighthouse @lhci/cli

# Playwright integration
npm i -D @axe-core/playwright

# pytest (Python E2E)
uv add --dev axe-playwright-python pytest-playwright

# Cypress (legacy)
npm i -D cypress-axe
```

Auth: none. Lighthouse CI server token only if uploading reports.

## Common recipes

### Recipe 1 — axe-core CLI baseline

```bash
npx @axe-core/cli https://staging.example.com \
  --tags=wcag2a,wcag2aa,wcag21aa,wcag22aa \
  --exit --save axe-results.json
```

`--exit` returns non-zero on violation; safe for CI.

### Recipe 2 — Playwright + AxeBuilder

```ts
// tests/a11y/pages.a11y.spec.ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const pages = ["/", "/login", "/pricing", "/blog", "/contact"];

for (const path of pages) {
  test(`${path} — WCAG 2.2 AA clean`, async ({ page }) => {
    await page.goto(path);
    await page.waitForLoadState("networkidle");
    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
      .disableRules(["region"])    // skip until landmark refactor PR-1284
      .analyze();

    test.info().annotations.push({
      type: "violations",
      description: JSON.stringify(results.violations, null, 2),
    });
    expect(results.violations).toEqual([]);
  });
}
```

### Recipe 3 — pa11y-ci with sitemap

```json
// .pa11yci.json
{
  "defaults": {
    "standard": "WCAG2AA",
    "timeout": 30000,
    "wait": 500,
    "chromeLaunchConfig": { "args": ["--no-sandbox"] }
  },
  "urls": [
    { "url": "http://localhost:3000/", "actions": [] },
    { "url": "http://localhost:3000/dashboard",
      "actions": ["set field #email to user@example.com",
                  "set field #password to Test1234!",
                  "click element button[type=submit]",
                  "wait for path to be /dashboard"] }
  ]
}
```

```bash
npx pa11y-ci --sitemap https://staging.example.com/sitemap.xml
npx pa11y-ci  # uses .pa11yci.json
```

### Recipe 4 — Lighthouse CI a11y budget

```js
// lighthouserc.cjs
module.exports = {
  ci: {
    collect: {
      url: ["http://localhost:3000/", "http://localhost:3000/blog"],
      numberOfRuns: 3,
      startServerCommand: "npm start",
    },
    assert: {
      assertions: {
        "categories:accessibility": ["error", { minScore: 0.95 }],
        "audits:color-contrast": "error",
        "audits:image-alt": "error",
        "audits:button-name": "error",
        "audits:label": "error",
      },
    },
    upload: { target: "temporary-public-storage" },
  },
};
```

```bash
npx lhci autorun
```

### Recipe 5 — Python E2E (axe-playwright-python)

```python
# tests/test_a11y.py
import pytest
from playwright.sync_api import Page
from axe_playwright_python.sync_playwright import Axe

@pytest.fixture
def axe():
    return Axe()

@pytest.mark.parametrize("path", ["/", "/login", "/dashboard"])
def test_wcag_22_aa(page: Page, axe: Axe, path: str):
    page.goto(f"http://localhost:3000{path}")
    page.wait_for_load_state("networkidle")
    results = axe.run(page, options={"runOnly": ["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"]})
    assert results.violations_count == 0, results.generate_report()
```

### Recipe 6 — Authenticated flow scan

```ts
test("authed dashboard a11y", async ({ page, context }) => {
  await context.storageState({ path: ".auth/user.json" });
  await page.goto("/dashboard");
  const results = await new AxeBuilder({ page })
    .include("#main")             // scope to app-owned content
    .exclude("iframe[name=intercom]")  // exclude third-party
    .withTags(["wcag22aa"])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

### Recipe 7 — Manual keyboard playbook

For every page, manually verify:

```markdown
## Keyboard pass — <page>
- [ ] Tab order visits every interactive element in visible order
- [ ] No focus trap (can Tab out of every modal, menu, dialog)
- [ ] Focus indicator visible on every focused element
- [ ] Esc closes dialogs, menus, popovers
- [ ] Arrow keys navigate menus, lists, tabs, comboboxes
- [ ] Space activates buttons / checkboxes / toggles
- [ ] Enter submits forms / activates links
- [ ] Skip-to-main link reaches main content
- [ ] No `tabindex > 0`
```

### Recipe 8 — Screen reader pass

```markdown
## NVDA (Win) — primary flow
- [ ] Page title announced on load
- [ ] Heading hierarchy read (h1 → h2 → h3)
- [ ] Landmarks ("main", "nav", "complementary") announced
- [ ] Form labels read with inputs
- [ ] Error messages read on submit
- [ ] Live regions announced (cart updated, save success)
- [ ] Images: alt read, decorative skipped
- [ ] Modals: title + description announced on open

## VoiceOver (mac) — same checklist
## TalkBack (Android) + VoiceOver iOS — mobile flows
```

### Recipe 9 — Color contrast spot-check

```bash
# Programmatic via axe-core color-contrast rule (already runs)
# Manual:
# https://webaim.org/resources/contrastchecker/
# Targets:
#   4.5:1 — normal text
#   3:1 — large text (>= 18pt or >= 14pt bold), UI components, graphics
```

### Recipe 10 — Zoom + reflow test

```bash
# Manual:
# 1. Open Chrome at 100%; visit page
# 2. Press Ctrl+ to 200% zoom; verify:
#    - no horizontal scroll
#    - no truncation
#    - no overlapping content
#    - all interactives still reachable
# 3. Same at 400% via WCAG 2.2 reflow requirement
```

### Recipe 11 — CI gate workflow

```yaml
# .github/workflows/a11y.yml
on: [pull_request]
jobs:
  axe:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npx playwright test --project=a11y
      - if: failure()
        uses: actions/upload-artifact@v4
        with: { name: a11y-results, path: test-results/ }
  pa11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run build && npm start &
      - run: npx wait-on http://localhost:3000
      - run: npx pa11y-ci
```

### Recipe 12 — VPAT / ACCR evidence export

```bash
# axe-core JSON → markdown via custom script
node scripts/axe-to-vpat.js axe-results.json > vpat-evidence.md

# Pa11y → markdown report
npx pa11y-ci --reporter json > pa11y.json
node scripts/pa11y-to-vpat.js pa11y.json >> vpat-evidence.md
```

## Examples

### Example 1: Stand up CI a11y gate from scratch

**Goal:** Block merge on WCAG 2.2 AA violations.

1. Add `@axe-core/playwright` (Recipe 2). Cover 5-10 critical pages.
2. Add Lighthouse CI accessibility minScore 0.95 (Recipe 4).
3. Wire workflow `a11y.yml` to PR (Recipe 11).
4. First run will fail with existing violations — fix or `disableRules`
   with a tracked issue.
5. Add monthly manual NVDA pass to release checklist.

### Example 2: Single-flow audit + manual evidence

**Goal:** Audit checkout flow for VPAT documentation.

1. Run automated: axe on each step page; export results.
2. Manual keyboard pass — note tab order + traps.
3. NVDA + Chrome pass — note reading order + announcements.
4. Zoom 200% — note layout intact.
5. Compile evidence per Recipe 12; deliver VPAT.

## Edge cases / gotchas

- **Automated catches ~57%** — never claim WCAG compliance from axe alone.
- **`network-idle` flakes** — SPAs often have ongoing polling. Use explicit
  `waitForSelector` for known stable content.
- **Third-party iframes** — exclude with `AxeBuilder.exclude()` rather than
  fail. Track separately ("intercom not WCAG 2.2 AA").
- **Color contrast on hover/focus** — axe doesn't navigate into hover states.
  Use Playwright hover + re-scan or manual.
- **Live regions overuse** — `aria-live="assertive"` fires every change.
  Test with screen reader, not just axe.
- **`role="img"` on decorative SVGs** — axe doesn't flag, but screen readers
  do read. Use `aria-hidden="true"` on truly decorative.
- **Lighthouse a11y score = subset of axe** — 0.95 score does NOT mean axe-clean.
  Run both.
- **WCAG 2.2 new criteria** — focus appearance (2.4.11), target size 24px
  (2.5.8), dragging movements (2.5.7). Existing suites miss these.
- **Mobile viewport scan** — axe doesn't auto-set mobile viewport. Configure
  Playwright `devices['iPhone 14']` for mobile a11y.
- **AT testing in CI** — no production-grade NVDA-in-CI exists. Manual pass
  per release.
- **PDF / SVG content** — out of scope for axe. Use Adobe Acrobat Pro a11y
  checker or pac3 for PDFs.

## Sources

- [axe-core rules](https://dequeuniversity.com/rules/axe/)
- [@axe-core/playwright](https://github.com/dequelabs/axe-core-npm/tree/develop/packages/playwright)
- [pa11y docs](https://pa11y.org/)
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- [WCAG 2.2 quick reference](https://www.w3.org/WAI/WCAG22/quickref/)
- [WCAG 2.2 what's new](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)
- [WebAIM contrast checker](https://webaim.org/resources/contrastchecker/)
- [Deque University](https://dequeuniversity.com/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [Accessibility Insights for Web](https://accessibilityinsights.io/)
