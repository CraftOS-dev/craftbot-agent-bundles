<!--
Source: https://playwright.dev/docs/best-practices · https://playwright.dev/docs/trace-viewer
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# Playwright — E2E stability

Playwright 1.50+ is the SOTA E2E test runner. Web-first assertions auto-wait
(no `waitForTimeout`!), locators beat selectors, fixtures isolate state, traces
debug failures, sharding parallelizes CI. This skill encodes the stability
patterns that separate flaky suites from green ones.

## When to use

- Authoring E2E tests for a new feature
- A test is flaky and you can't figure out why
- Setting up Playwright in a new project
- Migrating from Cypress / Selenium / WebdriverIO
- Trigger phrases: "E2E", "Playwright", "flaky test", "auto-waiting",
  "trace viewer", "fixture", "codegen", "sharding", "page object"

## Setup

```bash
pnpm add -D @playwright/test
pnpm dlx playwright install                 # downloads Chromium/Firefox/WebKit
pnpm dlx playwright install --with-deps     # also installs OS deps (Linux)

# Optional add-ons
pnpm add -D @axe-core/playwright            # a11y in E2E
pnpm add -D playwright-test-coverage        # JS coverage in E2E
```

Verify: `pnpm exec playwright --version` → 1.50+.

No API keys (for cloud parallelization see Microsoft Playwright Testing).

## Common recipes

### Recipe 1 — `playwright.config.ts` baseline

```ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  timeout: 30_000,                              // per test
  expect: { timeout: 5_000 },                   // per assertion
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 4 : undefined,
  reporter: process.env.CI ? [["github"], ["html"]] : "list",
  use: {
    baseURL: process.env.E2E_BASE_URL ?? "http://localhost:3000",
    trace: "on-first-retry",                    // capture trace when a test fails
    screenshot: "only-on-failure",
    video: "retain-on-failure",
    actionTimeout: 10_000,
    navigationTimeout: 30_000,
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    { name: "webkit", use: { ...devices["Desktop Safari"] } },
    { name: "mobile", use: { ...devices["Pixel 7"] } },
  ],
  webServer: {
    command: "pnpm dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
});
```

### Recipe 2 — Web-first locators (never `getByText` directly in props)

```ts
import { test, expect } from "@playwright/test";

test("submits the form", async ({ page }) => {
  await page.goto("/signup");

  // ROLE — preferred, matches accessibility tree
  await page.getByRole("textbox", { name: "Email" }).fill("user@example.com");
  await page.getByRole("textbox", { name: "Password" }).fill("hunter2!");
  await page.getByRole("checkbox", { name: "I agree" }).check();
  await page.getByRole("button", { name: "Sign up" }).click();

  // LABEL — for inputs
  await page.getByLabel("Full name").fill("Ada Lovelace");

  // TEXT — for visible content
  await expect(page.getByText("Welcome, Ada")).toBeVisible();

  // TEST ID — last resort, when role/label unavailable
  await page.getByTestId("payment-method").click();
});
```

Locator priority: `getByRole` > `getByLabel` > `getByPlaceholder` > `getByText`
> `getByTestId` > CSS selectors.

### Recipe 3 — Web-first assertions (auto-wait)

```ts
// BAD — manual sleep, brittle
await page.click("button.submit");
await page.waitForTimeout(2000);
expect(await page.locator(".success").isVisible()).toBe(true);

// GOOD — auto-waits up to timeout
await page.getByRole("button", { name: "Submit" }).click();
await expect(page.getByText("Order placed")).toBeVisible();
await expect(page.getByText("Order placed")).toHaveText(/^Order placed/);
await expect(page).toHaveURL(/\/orders\//);
await expect(page).toHaveTitle(/Order confirmed/);
```

`expect(locator).toBeVisible()` polls until visible or timeout — no manual waits.

### Recipe 4 — Fixtures for isolated state

```ts
// tests/fixtures.ts
import { test as base } from "@playwright/test";

type Fixtures = {
  authedPage: import("@playwright/test").Page;
  testUser: { email: string; password: string };
};

export const test = base.extend<Fixtures>({
  testUser: async ({}, use) => {
    const user = { email: `test+${Date.now()}@example.com`, password: "pass1234!" };
    await api.createUser(user);
    await use(user);
    await api.deleteUser(user.email);
  },
  authedPage: async ({ page, testUser }, use) => {
    await page.goto("/login");
    await page.getByLabel("Email").fill(testUser.email);
    await page.getByLabel("Password").fill(testUser.password);
    await page.getByRole("button", { name: "Log in" }).click();
    await expect(page).toHaveURL("/");
    await use(page);
  },
});

export { expect } from "@playwright/test";
```

```ts
import { test, expect } from "./fixtures";
test("logged-in user sees dashboard", async ({ authedPage }) => {
  await expect(authedPage.getByRole("heading", { name: "Dashboard" })).toBeVisible();
});
```

### Recipe 5 — Storage state (skip login per test)

```ts
// global-setup.ts
import { chromium } from "@playwright/test";

async function globalSetup() {
  const browser = await chromium.launch();
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  await page.goto("http://localhost:3000/login");
  await page.getByLabel("Email").fill(process.env.SEED_EMAIL!);
  await page.getByLabel("Password").fill(process.env.SEED_PASSWORD!);
  await page.getByRole("button", { name: "Log in" }).click();
  await ctx.storageState({ path: ".auth/user.json" });
  await browser.close();
}
export default globalSetup;
```

```ts
// playwright.config.ts
export default defineConfig({
  globalSetup: "./global-setup.ts",
  use: { storageState: ".auth/user.json" },
});
```

Login runs once; every test starts already authenticated.

### Recipe 6 — Mock network with `page.route`

```ts
test("shows empty state when API returns []", async ({ page }) => {
  await page.route("**/api/posts", (route) =>
    route.fulfill({ status: 200, body: "[]" }),
  );
  await page.goto("/blog");
  await expect(page.getByText("No posts yet")).toBeVisible();
});
```

### Recipe 7 — A11y check inline with E2E

```ts
import AxeBuilder from "@axe-core/playwright";

test("home is a11y-clean", async ({ page }) => {
  await page.goto("/");
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa"])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

### Recipe 8 — Codegen (record + replay)

```bash
pnpm exec playwright codegen http://localhost:3000
# Click through the app; Playwright generates test code
# Copy/paste the generated script into a .spec.ts file
```

### Recipe 9 — Trace Viewer (debug failures)

```bash
# Locally after a failed run
pnpm exec playwright show-trace test-results/example-failed/trace.zip

# Or view the HTML report
pnpm exec playwright show-report
```

Trace Viewer shows: every action, every locator query, network log, console
log, snapshots before/after. Trace = the single best feature.

### Recipe 10 — Sharding in CI

```yaml
# .github/workflows/e2e.yml
jobs:
  e2e:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: pnpm install
      - run: pnpm exec playwright install --with-deps chromium
      - run: pnpm exec playwright test --shard=${{ matrix.shard }}/4
```

4 parallel shards = 4x faster CI.

### Recipe 11 — Page Object Model (optional, for complex flows)

```ts
// tests/poms/LoginPage.ts
import type { Page } from "@playwright/test";

export class LoginPage {
  constructor(private page: Page) {}
  async goto() { await this.page.goto("/login"); }
  async fill(email: string, password: string) {
    await this.page.getByLabel("Email").fill(email);
    await this.page.getByLabel("Password").fill(password);
  }
  async submit() { await this.page.getByRole("button", { name: "Log in" }).click(); }
}
```

Use sparingly — heavy POMs become maintenance burdens. Prefer fixtures.

### Recipe 12 — Component testing mode

```bash
pnpm dlx playwright install
pnpm dlx playwright init-component-test
```

```tsx
// tests/components/Button.spec.tsx
import { test, expect } from "@playwright/experimental-ct-react";
import { Button } from "@/components/Button";

test("renders and clicks", async ({ mount }) => {
  let clicked = false;
  const component = await mount(<Button onClick={() => clicked = true}>Click</Button>);
  await component.click();
  expect(clicked).toBe(true);
});
```

For most apps, Vitest browser mode is the better choice for components and
Playwright stays for E2E.

## Examples

### Example 1: Set up a green Playwright suite from scratch

```bash
pnpm add -D @playwright/test
pnpm dlx playwright install --with-deps
# Edit playwright.config.ts (use Recipe 1)
mkdir tests
# Write one happy-path test (Recipe 2)
pnpm exec playwright test
pnpm exec playwright show-report
```

### Example 2: Debug a flaky test

1. Run with `--repeat-each=5` — does it flake locally?
2. Add `trace: "on"` to the test → `pnpm exec playwright test --headed`
3. Open trace: `pnpm exec playwright show-trace test-results/.../trace.zip`
4. Look for: race conditions (assertion fires before request resolved),
   timing-dependent visibility, animation interfering with click
5. Fix with web-first assertion (`toBeVisible`) or stable locator
   (`getByRole`) — never with `waitForTimeout`

## Edge cases / gotchas

- **`waitForTimeout` is banned** in healthy suites — use `expect.toBeVisible()`
  or `waitForRequest` / `waitForLoadState`.
- **`networkidle`** is unreliable for SPAs — there's always something polling.
  Prefer `domcontentloaded` + assertion on visible content.
- **Multiple matches** — `getByRole("button")` may match many. Add `name:` or
  scope with `.first()` / `.nth(0)`.
- **iframes** — `page.frameLocator("iframe[name=stripe]").getByPlaceholder("Card number")`.
- **Shadow DOM** — Playwright pierces shadow roots automatically via locators.
- **Downloads** — `const [download] = await Promise.all([page.waitForEvent("download"),
  page.click("a.export")]); await download.saveAs("./tmp.csv");`
- **File uploads** — `await page.setInputFiles("input[type=file]", "./fixture.png");`
- **Authentication state expires** — set `storageState` expiry checks; re-run
  `globalSetup` daily.
- **Visual diffs** — Playwright has built-in `toHaveScreenshot()` but Chromatic
  is more powerful for design systems.
- **CI vs local** — CI uses headless + slower CPU. Test with
  `--workers=1 --headed=false` locally to mimic.
- **Test ordering** — Playwright doesn't guarantee order across files. Make
  every test independent.
- **`page.pause()`** drops into interactive debugger — set in code, run with
  `--headed`. Don't commit.

## Sources

- [Playwright docs](https://playwright.dev/)
- [Best practices](https://playwright.dev/docs/best-practices)
- [Trace Viewer](https://playwright.dev/docs/trace-viewer)
- [Locators guide](https://playwright.dev/docs/locators)
- [Fixtures guide](https://playwright.dev/docs/test-fixtures)
- [Sharding](https://playwright.dev/docs/test-sharding)
- [Microsoft Playwright Testing](https://learn.microsoft.com/en-us/azure/playwright-testing/) — cloud parallel runs
- [Stefan Judis — Playwright deep dives (2025)](https://www.stefanjudis.com/) — weekly tips
- [Playwright YouTube — official channel](https://www.youtube.com/@Playwrightdev)
