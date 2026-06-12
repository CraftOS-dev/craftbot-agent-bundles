---
name: pa11y-axe-accessibility-audit
description: WCAG 2.2 AA accessibility audit for docs sites — pa11y-ci + axe-core (deque-labs). 57%+ coverage via axe rules. CI gate patterns and Lighthouse CI as complement. Use whenever auditing or gating a docs PR for accessibility.
---

# pa11y + axe-core Accessibility Audit

`pa11y-ci` is the open-source accessibility test runner; under the hood it uses **axe-core** (Deque) as the rule engine. axe-core delivers ~57% of all detectable WCAG issues automatically — the highest of any FOSS engine in 2026.

For comprehensive coverage, complement with **Lighthouse CI** (Google) which runs accessibility + performance + SEO + best-practices categories.

## When to use this skill

- Audit existing docs for WCAG 2.2 AA compliance.
- CI gate on docs PRs to prevent regressions.
- Generate JSON / HTML accessibility reports for stakeholders.

## Setup

### Install

```bash
npm i -g pa11y pa11y-ci
npm i -g @lhci/cli                    # Lighthouse CI
npm i -g @axe-core/cli                # axe-core CLI standalone
pa11y --version
```

### Project config — `.pa11yci.json`

```json
{
  "defaults": {
    "standard": "WCAG2AA",
    "timeout": 30000,
    "wait": 1000,
    "viewport": { "width": 1280, "height": 800 },
    "chromeLaunchConfig": {
      "args": ["--no-sandbox", "--disable-dev-shm-usage"]
    },
    "runners": ["axe", "htmlcs"],
    "ignore": [
      "color-contrast",                              // example: ignore project-wide
      "WCAG2AA.Principle1.Guideline1_4.1_4_3.G18"    // specific rule
    ],
    "reporter": "json"
  },
  "urls": [
    "http://localhost:3000/",
    "http://localhost:3000/quickstart",
    "http://localhost:3000/api-reference",
    {
      "url": "http://localhost:3000/login",
      "actions": [
        "set field input[name=email] to demo@example.com",
        "set field input[name=password] to demopassword",
        "click element button[type=submit]",
        "wait for path to be /dashboard"
      ]
    }
  ]
}
```

## Common recipes

### Recipe 1: Single-page audit

```bash
pa11y http://localhost:3000/quickstart
```

### Recipe 2: Crawl a sitemap

```bash
pa11y-ci --sitemap https://docs.example.com/sitemap.xml --sitemap-find docs.example.com --sitemap-replace localhost:3000
```

### Recipe 3: Run from config file

```bash
pa11y-ci --config .pa11yci.json
# JSON output
pa11y-ci --config .pa11yci.json --reporter json > a11y-report.json
```

### Recipe 4: axe-core CLI standalone

```bash
axe http://localhost:3000/quickstart --tags wcag2aa,wcag22aa --save axe-report.json
```

axe-core's rule tags:

| Tag | Coverage |
|---|---|
| `wcag2a` | WCAG 2.0 Level A |
| `wcag2aa` | WCAG 2.0 Level AA |
| `wcag21a` / `wcag21aa` | WCAG 2.1 |
| `wcag22a` / `wcag22aa` | WCAG 2.2 |
| `best-practice` | Beyond-WCAG quality rules |
| `experimental` | New rules in beta |

### Recipe 5: GitHub Actions CI gate

```yaml
# .github/workflows/a11y.yml
name: Accessibility
on:
  pull_request:
    paths: ['docs/**']
jobs:
  pa11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm i -g pa11y-ci
      - run: npm ci
      - run: npm run build        # build the docs site
      - run: npx serve dist &     # serve at :3000
      - run: sleep 3
      - run: pa11y-ci --config .pa11yci.json --reporter json > a11y.json
      - if: always()
        uses: actions/upload-artifact@v4
        with: { name: a11y-report, path: a11y.json }
```

### Recipe 6: Lighthouse CI (a11y + perf + SEO)

```yaml
# .lighthouserc.json
{
  "ci": {
    "collect": {
      "url": ["http://localhost:3000/", "http://localhost:3000/quickstart"],
      "startServerCommand": "npx serve dist -p 3000",
      "numberOfRuns": 3
    },
    "assert": {
      "preset": "lighthouse:recommended",
      "assertions": {
        "categories:accessibility": ["error",  { "minScore": 0.95 }],
        "categories:performance":   ["warn",   { "minScore": 0.85 }],
        "categories:best-practices":["error",  { "minScore": 0.90 }],
        "categories:seo":           ["error",  { "minScore": 0.90 }]
      }
    },
    "upload": { "target": "temporary-public-storage" }
  }
}
```

Workflow:

```yaml
- run: npm i -g @lhci/cli
- run: lhci autorun
```

### Recipe 7: pa11y for a single URL with actions (login flow)

```bash
pa11y http://localhost:3000/dashboard \
  --actions "set field input[name=email] to demo@example.com" \
  --actions "set field input[name=password] to demopassword" \
  --actions "click element button[type=submit]" \
  --actions "wait for path to be /dashboard"
```

## Common WCAG 2.2 AA gotchas axe catches

- `color-contrast` — text/background contrast < 4.5:1 (3:1 for large text).
- `image-alt` — missing alt text.
- `label` — form inputs without associated labels.
- `link-name` — empty or non-descriptive link text ("click here").
- `heading-order` — skipped heading levels (h2 → h4).
- `region` — content outside landmarks.
- `aria-allowed-attr` — invalid ARIA on a role.
- `focus-order-semantics` — focus order doesn't match visual order.
- New in WCAG 2.2: `target-size-minimum` (24x24 px tap targets).

## Manual checks axe can't automate

axe-core covers ~57% of WCAG. The remainder require manual review:

- Logical heading hierarchy semantics.
- Visible focus indicator quality.
- Reading order in screen readers.
- Keyboard trap detection.
- Cognitive load / clarity of language.
- Captions and transcripts on media.

Hand these off to a human accessibility reviewer; document the limitation in the audit report.

## Edge cases

- **SPA / hydration timing:** increase `wait` in pa11y config; some routes need 2-3s before axe runs.
- **CSS-only animations triggering rule failures:** disable via `chromeLaunchConfig.args: ["--force-prefers-reduced-motion"]`.
- **Iframe content:** axe doesn't traverse cross-origin iframes; test embedded content separately.
- **Authenticated docs:** use pa11y `--actions` or cookie injection.
- **Dark-mode contrast:** test both light and dark by toggling theme via action.

## Sources

- pa11y: https://github.com/pa11y/pa11y
- pa11y-ci: https://github.com/pa11y/pa11y-ci
- axe-core: https://github.com/dequelabs/axe-core
- Lighthouse CI: https://github.com/GoogleChrome/lighthouse-ci
- WCAG 2.2 AA: https://www.w3.org/WAI/WCAG22/quickref/?levels=aa
