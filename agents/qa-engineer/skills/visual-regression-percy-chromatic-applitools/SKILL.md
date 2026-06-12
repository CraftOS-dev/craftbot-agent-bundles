<!--
Source: https://playwright.dev/docs/test-snapshots · https://applitools.com/ · https://www.chromatic.com/ · https://percy.io/
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Visual Regression — Playwright + Applitools + Chromatic + Percy

The 2026 visual stack: **Playwright native** `toHaveScreenshot()` for free
local coverage; **Applitools Eyes** (perceptual Visual AI) for enterprise;
**Chromatic** for Storybook-first component teams; **Percy** for BrowserStack-
bundled. Choose by team workflow + budget.

## When to use

- Pixel-precise UI regressions matter (design system, marketing site)
- Storybook component review needs cross-team sign-off
- Cross-browser visual diff (Safari renders text different from Chrome)
- Catching CSS regressions a unit test can't (specificity, cascade collapse)
- Trigger phrases: "visual regression", "screenshot", "pixel diff",
  "Percy", "Chromatic", "Applitools", "Eyes", "design QA"

## Setup

```bash
# Playwright native (free)
npm i -D @playwright/test

# Applitools Eyes (Playwright)
npm i -D @applitools/eyes-playwright

# Chromatic (Storybook)
npm i -D chromatic
# Storybook already installed

# Percy (BrowserStack)
npm i -D @percy/cli @percy/playwright
```

Auth:
- `APPLITOOLS_API_KEY` — Applitools account
- `CHROMATIC_PROJECT_TOKEN` — Chromatic project token
- `PERCY_TOKEN` — Percy / BrowserStack key
- Playwright native: none

## Common recipes

### Recipe 1 — Playwright `toHaveScreenshot` (free, native)

```ts
import { test, expect } from "@playwright/test";

test("homepage matches baseline", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveScreenshot("home.png");
});

test("button states", async ({ page }) => {
  await page.goto("/components/button");
  const button = page.getByRole("button", { name: "Submit" });
  await expect(button).toHaveScreenshot("button-default.png");
  await button.hover();
  await expect(button).toHaveScreenshot("button-hover.png", { maxDiffPixels: 100 });
});
```

```bash
# First run — generates baseline
npx playwright test --update-snapshots
# Subsequent runs — compares to baseline
npx playwright test
```

### Recipe 2 — Playwright config — visual project

```ts
// playwright.config.ts
export default defineConfig({
  projects: [
    {
      name: "visual",
      testMatch: /.*\.visual\.spec\.ts/,
      use: { ...devices["Desktop Chrome"] },
      expect: {
        toHaveScreenshot: {
          maxDiffPixels: 100,
          threshold: 0.2,
          animations: "disabled",
          caret: "hide",
        },
      },
    },
  ],
});
```

### Recipe 3 — Applitools Eyes (Visual AI)

```ts
// tests/visual/applitools.spec.ts
import { test } from "@playwright/test";
import { Eyes, ClassicRunner, Target, MatchLevel } from "@applitools/eyes-playwright";

test("homepage", async ({ page }) => {
  const eyes = new Eyes(new ClassicRunner());
  await eyes.open(page, "MyApp", "Homepage", { width: 1280, height: 720 });
  try {
    await page.goto("/");
    await eyes.check("Hero", Target.window().fully().matchLevel(MatchLevel.Strict));
    await page.click("text=Pricing");
    await eyes.check("Pricing", Target.window().fully());
  } finally {
    await eyes.closeAsync();
  }
});
```

```bash
APPLITOOLS_API_KEY=... npx playwright test tests/visual/applitools.spec.ts
```

Applitools dashboard — review diffs, approve via UI; baselines auto-track.

### Recipe 4 — Chromatic (Storybook)

```bash
npx chromatic --project-token=$CHROMATIC_PROJECT_TOKEN
# Or for CI
npx chromatic --project-token=$CHROMATIC_PROJECT_TOKEN \
  --exit-zero-on-changes \
  --only-changed
```

```js
// .storybook/main.ts — Chromatic params
export default {
  stories: ["../src/**/*.stories.@(ts|tsx)"],
  addons: ["@storybook/addon-essentials"],
  features: {
    interactionsDebugger: true,
  },
};

// per-story
export const Primary = {
  parameters: {
    chromatic: { viewports: [320, 768, 1200], pauseAnimationAtEnd: true },
  },
};
```

### Recipe 5 — Percy (BrowserStack)

```ts
// tests/visual/percy.spec.ts
import { test } from "@playwright/test";
import percySnapshot from "@percy/playwright";

test("captures homepage", async ({ page }) => {
  await page.goto("/");
  await percySnapshot(page, "Homepage", {
    widths: [375, 768, 1280],
    minHeight: 1024,
  });
});
```

```bash
PERCY_TOKEN=... npx percy exec -- npx playwright test
```

### Recipe 6 — Handling dynamic content (mask / wait)

```ts
// Playwright native — mask dynamic regions
await expect(page).toHaveScreenshot("home.png", {
  mask: [
    page.locator(".timestamp"),
    page.locator(".user-avatar"),
    page.locator("[data-testid=loading-skeleton]"),
  ],
  fullPage: true,
});

// Wait for content
await page.waitForLoadState("networkidle");
await expect(page.getByText("Welcome")).toBeVisible();
await expect(page).toHaveScreenshot();
```

### Recipe 7 — Cross-browser visual diff

```ts
// playwright.config.ts
projects: [
  { name: "chromium-visual", use: { ...devices["Desktop Chrome"] }, testMatch: /.*\.visual\.spec\.ts/ },
  { name: "firefox-visual",  use: { ...devices["Desktop Firefox"] }, testMatch: /.*\.visual\.spec\.ts/ },
  { name: "webkit-visual",   use: { ...devices["Desktop Safari"] }, testMatch: /.*\.visual\.spec\.ts/ },
],
```

Each browser keeps its own baseline directory:
`tests/visual/__snapshots__/{file}-{project}-{platform}.png`

### Recipe 8 — Approve baseline via PR

```bash
# Local
npx playwright test --update-snapshots
git add -A tests/**/__snapshots__
git commit -m "chore(visual): update baselines for new layout"
```

Never auto-update in CI — humans review diffs.

### Recipe 9 — Suppress flaky elements (animations / cursors)

```ts
// Per test
await expect(page).toHaveScreenshot({ animations: "disabled", caret: "hide" });

// Global in config
expect: {
  toHaveScreenshot: { animations: "disabled", caret: "hide" },
},
```

### Recipe 10 — Component-level visual (Storybook + Chromatic)

```ts
// Button.stories.tsx
export const States: Story = {
  render: () => (
    <div className="space-y-4">
      <Button>Default</Button>
      <Button variant="primary">Primary</Button>
      <Button disabled>Disabled</Button>
    </div>
  ),
  parameters: { chromatic: { delay: 300 } },
};
```

Chromatic captures every story; reviewers compare via web UI.

### Recipe 11 — CI workflow (Playwright native)

```yaml
# .github/workflows/visual.yml
on:
  pull_request: { paths: ['src/**', 'tests/visual/**'] }

jobs:
  visual:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npx playwright test --project=visual
      - if: failure()
        uses: actions/upload-artifact@v4
        with: { name: visual-diffs, path: test-results/ }
```

### Recipe 12 — CI workflow (Chromatic)

```yaml
- name: Run Chromatic
  uses: chromaui/action@latest
  with:
    projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
    exitZeroOnChanges: true
    onlyChanged: true
    autoAcceptChanges: main
```

### Recipe 13 — Approving diffs via Chromatic UI

1. CI fails with "1 change detected".
2. Open Chromatic build URL.
3. Review side-by-side; click "Accept" or "Deny".
4. PR auto-updates status.

### Recipe 14 — Visual diff tooling decision

```markdown
| Need | Tool |
|---|---|
| Free, in-repo, single team | Playwright native |
| Storybook-first, design system review | Chromatic |
| Visual AI (ignores rendering noise), enterprise | Applitools |
| BrowserStack-bundled, mid-market | Percy |
| Open-source / self-host | Reg-cli, BackstopJS, Loki |
```

## Examples

### Example 1: Stand up visual regression cheaply

**Goal:** Catch CSS regressions, $0 budget.

1. Add Playwright `toHaveScreenshot` (Recipe 1) for 5-10 pages.
2. Add visual project (Recipe 2); run on PR.
3. Mask dynamic regions (Recipe 6).
4. CI uploads diffs as artifacts (Recipe 11).
5. Approve baselines via PR (Recipe 8).

### Example 2: Storybook component review with stakeholders

**Goal:** Designer-friendly review for design system PRs.

1. Add Chromatic to Storybook (Recipe 4).
2. CI workflow auto-publishes per PR (Recipe 12).
3. Chromatic auto-comments on PR with build link.
4. Designer approves visual changes in Chromatic web UI (Recipe 13).
5. CI status flips green; merge proceeds.

## Edge cases / gotchas

- **Font rendering differs OS-to-OS** — Linux CI ≠ macOS dev. Pin font set
  or use Docker image with fixed fonts.
- **Animations cause flake** — `animations: "disabled"` or `pauseAnimationAtEnd`
  (Chromatic).
- **Loading skeletons / shimmer** — wait for stable state or mask.
- **Locale / date / time** — fix with frozen time (`page.clock.install`).
- **Auto-update in CI is a banned antipattern** — humans must review diffs.
- **Image sizes blow up Git** — large PNGs in `__snapshots__` bloat repo.
  Use Git LFS for `*.png` over 100KB.
- **`maxDiffPixels` vs `threshold`** — `maxDiffPixels` (absolute count) for
  small components; `threshold` (% per-pixel) for large pages.
- **Chromatic free tier** — 5k snapshots/month for OSS; paid above.
- **Applitools requires baseline approval** — first run uploads but stays
  "Unresolved" until accepted in UI.
- **Percy + BrowserStack pricing** — bundled with BS subscriptions; not
  separable.
- **CDP screenshot vs OS screenshot** — Playwright uses CDP; macOS native
  XCUITest = different DPI. Tests not portable across.
- **Visual diff + a11y** — diffs catch contrast regressions axe missed;
  consider running together.
- **Empty baseline directory in fresh PR** — set `--update-snapshots` only
  on first commit; thereafter PR fails until diff approved.

## Sources

- [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots)
- [Applitools Eyes Playwright](https://applitools.com/docs/topics/sdk-getting-started-pages/sdk-playwright.html)
- [Chromatic docs](https://www.chromatic.com/docs/)
- [Chromatic GitHub Action](https://github.com/chromaui/action)
- [Percy + Playwright](https://docs.percy.io/docs/playwright)
- [BackstopJS (OSS)](https://github.com/garris/BackstopJS)
- [Reg-cli (OSS)](https://github.com/reg-viz/reg-cli)
- [Storybook visual testing](https://storybook.js.org/docs/writing-tests/visual-testing)
- [Visual testing best practices (Smashing Mag)](https://www.smashingmagazine.com/2024/visual-regression-testing-guide/)
