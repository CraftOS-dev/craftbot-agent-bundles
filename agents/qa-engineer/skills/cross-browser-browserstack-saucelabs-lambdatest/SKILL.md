<!--
Source: https://playwright.dev/docs/browsers · https://www.browserstack.com/automate · https://saucelabs.com/products/automated-testing · https://www.lambdatest.com/
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Cross-Browser Testing — Playwright + BrowserStack + Sauce Labs + LambdaTest

The 2026 strategy: **Playwright native** (Chromium / Firefox / WebKit)
covers 80%+ of regressions for free. Cloud grids (**BrowserStack**, **Sauce
Labs**, **LambdaTest / TestMu**) cover the long tail: older browsers, real
mobile devices, regional networks. Pick the grid based on device coverage
vs cost.

## When to use

- Need Safari coverage (WebKit) and team is Windows/Linux-only
- Customer-reported bug on IE 11 / Edge legacy / specific Android version
- Pre-launch verification on iOS Safari / Samsung Internet
- Geo-distributed testing (e.g., Japanese network, Brazilian device)
- Trigger phrases: "cross-browser", "Safari", "Firefox", "WebKit",
  "BrowserStack", "Sauce Labs", "LambdaTest", "TestMu", "real device"

## Setup

```bash
# Playwright (free local cross-browser)
npm i -D @playwright/test
npx playwright install --with-deps   # downloads Chromium + Firefox + WebKit

# BrowserStack
npm i -D browserstack-node-sdk @playwright/test
# Sauce Labs
npm i -D @saucelabs/playwright-runner
# LambdaTest
# Use playwright-tunnel or direct WebSocket WS endpoint
```

Auth:
- `BROWSERSTACK_USERNAME`, `BROWSERSTACK_ACCESS_KEY`
- `SAUCE_USERNAME`, `SAUCE_ACCESS_KEY`
- `LT_USERNAME`, `LT_ACCESS_KEY`

## Common recipes

### Recipe 1 — Playwright local cross-browser

```ts
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox",  use: { ...devices["Desktop Firefox"] } },
    { name: "webkit",   use: { ...devices["Desktop Safari"] } },
    { name: "mobile-chrome", use: { ...devices["Pixel 7"] } },
    { name: "mobile-safari", use: { ...devices["iPhone 14"] } },
  ],
});
```

```bash
npx playwright test                    # all projects
npx playwright test --project=webkit   # WebKit only
```

### Recipe 2 — BrowserStack Playwright SDK

```ts
// browserstack.yml
userName: ${BROWSERSTACK_USERNAME}
accessKey: ${BROWSERSTACK_ACCESS_KEY}
buildName: PW Sample Build
platforms:
  - os: OS X
    osVersion: Sequoia
    browserName: playwright-webkit
  - os: Windows
    osVersion: 11
    browserName: playwright-firefox
  - deviceName: Samsung Galaxy S24
    osVersion: 14.0
    browserName: chrome
parallelsPerPlatform: 1
debug: true
networkLogs: true
consoleLogs: errors
```

```bash
# Wrap CLI with BrowserStack SDK
npx browserstack-node-sdk playwright test
# Or via env var
BROWSERSTACK=true npx playwright test
```

### Recipe 3 — Sauce Labs Playwright

```ts
// saucectl.yml
apiVersion: v1alpha
kind: playwright
sauce:
  region: us-west-1
  concurrency: 5
  metadata:
    name: PW E2E
playwright:
  version: 1.50.1
suites:
  - name: chrome-mac
    platformName: "macOS 14"
    params:
      browserName: chromium
    testMatch: ["**/*.spec.ts"]
  - name: webkit
    platformName: "macOS 14"
    params:
      browserName: webkit
    testMatch: ["**/*.spec.ts"]
```

```bash
npx saucectl run
```

### Recipe 4 — LambdaTest connection (TestMu)

```ts
// playwright-lt.config.ts
import { chromium } from "@playwright/test";

const lt = `wss://cdp.lambdatest.com/playwright?capabilities=${encodeURIComponent(JSON.stringify({
  browserName: "Chrome",
  browserVersion: "latest",
  "LT:Options": {
    platform: "Windows 11",
    build: "PW LT Run",
    name: "Smoke",
    user: process.env.LT_USERNAME,
    accessKey: process.env.LT_ACCESS_KEY,
    network: true,
    video: true,
    console: true,
  },
}))}`;

(async () => {
  const browser = await chromium.connect({ wsEndpoint: lt });
  // ... run tests
})();
```

### Recipe 5 — Selective cloud run (matrix CI)

```yaml
# .github/workflows/cross-browser.yml
on:
  workflow_dispatch:
  schedule: [{ cron: '0 6 * * 1' }]  # weekly nightly

jobs:
  local-pw:
    runs-on: ubuntu-latest
    strategy: { matrix: { project: [chromium, firefox, webkit] } }
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx playwright install --with-deps ${{ matrix.project }}
      - run: npx playwright test --project=${{ matrix.project }}

  cloud-bs:
    if: github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - env:
          BROWSERSTACK_USERNAME: ${{ secrets.BROWSERSTACK_USERNAME }}
          BROWSERSTACK_ACCESS_KEY: ${{ secrets.BROWSERSTACK_ACCESS_KEY }}
        run: npx browserstack-node-sdk playwright test
```

### Recipe 6 — Real-device mobile (BrowserStack App Live)

```ts
// playwright-bs-mobile.config.ts
import { devices, defineConfig } from "@playwright/test";

export default defineConfig({
  projects: [
    { name: "Samsung Galaxy S24 Real",
      use: { ...devices["Galaxy S24"], baseURL: "https://staging.example.com" } },
    { name: "iPhone 15 Pro Real",
      use: { ...devices["iPhone 15 Pro"] } },
  ],
});
```

BrowserStack streams real device; bandwidth-sensitive. Charge per minute.

### Recipe 7 — Local tunneling (BrowserStack Local / Sauce Connect)

```bash
# BrowserStack Local — test against staging-internal URL
npx browserstack-local --key $BROWSERSTACK_ACCESS_KEY

# Sauce Connect Proxy
sc -u $SAUCE_USERNAME -k $SAUCE_ACCESS_KEY --tunnel-identifier ci-tunnel
```

Use when staging is behind VPN / firewall.

### Recipe 8 — Browser matrix decision

```markdown
| Browser | Local Playwright | Cloud | Real device |
|---|---|---|---|
| Chromium / Edge Chromium | ✓ | ✓ | n/a |
| Firefox | ✓ | ✓ | n/a |
| Safari (macOS WebKit) | ✓ (Linux/Win OK) | ✓ | n/a |
| Safari iOS | ✗ | ✓ (via cloud) | preferred for real-touch |
| Samsung Internet | ✗ | ✓ | preferred |
| Edge legacy (pre-2020) | ✗ | ✓ | n/a |
| IE 11 | ✗ | ✓ (BS, Sauce — sunset) | n/a |
```

Use cloud only for the rows you can't cover locally.

### Recipe 9 — Cost guardrails

```markdown
## Cost guardrails
- Smoke: chromium local only (free)
- Critical-path: chromium + firefox + webkit local (free)
- Nightly extended: full local matrix (free)
- Weekly cloud: top 5 cloud devices (paid, ~$5-50/run)
- Pre-launch: 20-device cloud matrix (paid, ~$50-300)
```

### Recipe 10 — Visual diff cross-browser (Playwright native)

```ts
test("renders the same on all browsers", async ({ page }) => {
  await page.goto("/");
  await expect(page).toHaveScreenshot("home.png", { maxDiffPixels: 100 });
});
```

```bash
npx playwright test --project=chromium --update-snapshots
# Then run on firefox + webkit — diffs flagged
```

### Recipe 11 — Network throttling (cloud)

```ts
// BrowserStack network profiles
const capabilities = {
  "bstack:options": { networkProfile: "2g-gprs-good" },
};
```

```ts
// Local Playwright — CDP
const cdp = await page.context().newCDPSession(page);
await cdp.send("Network.emulateNetworkConditions", {
  offline: false,
  downloadThroughput: (1.5 * 1024 * 1024) / 8,
  uploadThroughput: (750 * 1024) / 8,
  latency: 40,
});
```

### Recipe 12 — Geo-distributed (cloud)

```yaml
# Sauce Labs region
sauce:
  region: eu-central-1   # Frankfurt
  # or us-east-4 / ap-southeast-3
```

Tests run physically in region — useful for CDN/Akamai routing tests.

## Examples

### Example 1: Standard project — Playwright local, no cloud

**Goal:** Cover 80% of cross-browser regressions for free.

1. Configure Playwright with chromium + firefox + webkit projects (Recipe 1).
2. CI matrix runs each project in parallel (Recipe 5).
3. Visual diffs across projects (Recipe 10).
4. Cloud only for pre-launch on top devices (Recipe 6).

### Example 2: Enterprise app — full cloud matrix

**Goal:** Old Edge + IE11 + 5 mobile devices for compliance.

1. BrowserStack `browserstack.yml` (Recipe 2) with target matrix.
2. Wrap CI with `browserstack-node-sdk` (Recipe 5 cloud-bs job).
3. BrowserStack Local for staging-internal URL (Recipe 7).
4. Track cost — limit to nightly + manual triggers (Recipe 9).

## Edge cases / gotchas

- **Playwright WebKit ≠ Safari fully** — same engine but missing iOS-specific
  UI / touch / haptics. Use cloud for real iOS Safari.
- **Cloud queueing** — at free tier, runs queue 10-30 min. Pay for parallel
  slots or move to local Playwright.
- **Network bandwidth on cloud** — uploading 100MB artifact per test costs;
  prefer trace-on-failure only.
- **Cookies between local + cloud** — different domains; storageState
  pre-recorded locally may not work on cloud. Re-record per environment.
- **Old browser bug ≠ your bug** — IE 11 dies on `?.` syntax; not a bug in
  your code, an environment limit. Document support floor explicitly.
- **Real-device tests are slow** — 3-5x slower than emulated; budget time.
- **Cloud session limits** — most providers cap session to 90 min; long
  tests need split into shorter runs.
- **LambdaTest TestMu AI** — KaneAI authoring; useful for record-replay but
  outputs may need clean-up.
- **BrowserStack vs Sauce vs LambdaTest pricing** — BrowserStack 30k+
  devices ($50-75k/yr at 100 parallel); Sauce deeper analytics ($80-120k);
  LambdaTest cheaper alternative.
- **Headless mode flakiness** — some sites detect headless (Cloudflare,
  Akamai bot manager). Use `--headed` or stealth plugins for those tests.
- **WebKit on Linux** — Playwright bundles a Linux-friendly WebKit build;
  not 100% identical to Apple WebKit. Cloud iOS Safari for last-mile.

## Sources

- [Playwright browsers](https://playwright.dev/docs/browsers)
- [Playwright devices](https://github.com/microsoft/playwright/blob/main/packages/playwright-core/src/server/deviceDescriptorsSource.json)
- [BrowserStack Automate](https://www.browserstack.com/automate)
- [BrowserStack Playwright SDK](https://www.browserstack.com/docs/automate/playwright)
- [Sauce Labs automated testing](https://saucelabs.com/products/automated-testing)
- [saucectl Playwright](https://docs.saucelabs.com/dev/cli/saucectl/usage/saucectl-playwright/)
- [LambdaTest Playwright](https://www.lambdatest.com/support/docs/playwright-on-cloud/)
- [TestMu AI rebrand](https://www.lambdatest.com/testmuconf-2024)
- [Can I Use](https://caniuse.com/) — feature support matrix
- [WebKit feature status](https://webkit.org/status/)
