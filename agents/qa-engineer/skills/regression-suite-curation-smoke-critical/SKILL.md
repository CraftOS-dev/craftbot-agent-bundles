<!--
Source: https://martinfowler.com/articles/practical-test-pyramid.html · https://playwright.dev/docs/test-projects · https://docs.pytest.org/en/stable/how-to/mark.html
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Regression Suite Curation — Smoke + Critical + Extended

A healthy regression suite is **tiered**: smoke (<5 min, blocks deploy) →
critical-path (<30 min, post-merge) → extended (nightly). Tagging via
Playwright projects / pytest markers / Cypress tags / Selenium suites keeps
the right tests running at the right cadence.

## When to use

- New repo or repo with one big "tests" folder
- CI feedback is too slow (>10 min on PR)
- Tests are running in PR that don't need to
- Adding a new feature — need to decide its suite tier
- Trigger phrases: "smoke tests", "critical path", "regression suite",
  "suite tiers", "test markers", "test projects", "tag tests"

## Setup

```bash
# Playwright
npm i -D @playwright/test

# pytest
uv add --dev pytest pytest-xdist pytest-html

# Cypress (legacy)
npm i -D cypress @cypress/grep

# Selenium / TestNG (legacy)
# Annotate groups in TestNG XML
```

Auth: none.

## Common recipes

### Recipe 1 — Playwright projects = tiers

```ts
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  projects: [
    {
      name: "smoke",
      testMatch: /.*\.smoke\.spec\.ts/,
      use: { ...devices["Desktop Chrome"] },
      timeout: 30_000,
    },
    {
      name: "critical",
      testMatch: /.*\.(smoke|critical)\.spec\.ts/,
      use: { ...devices["Desktop Chrome"] },
      timeout: 60_000,
    },
    {
      name: "extended",
      testMatch: /.*\.spec\.ts/,
      use: { ...devices["Desktop Chrome"] },
      timeout: 120_000,
    },
  ],
});
```

Run: `npx playwright test --project=smoke`. Smoke suite < 5 min.

### Recipe 2 — pytest markers = tiers

```ini
# pyproject.toml
[tool.pytest.ini_options]
markers = [
    "smoke: < 5 min subset; blocks deploy",
    "critical: < 30 min critical-path; post-merge",
    "extended: full regression; nightly",
    "quarantine: known-flaky; excluded from gate",
]
addopts = "-m 'not quarantine' --strict-markers"
```

```python
# tests/auth/test_login.py
import pytest

@pytest.mark.smoke
def test_login_happy_path(client, alice):
    assert client.post("/login", json=alice).status_code == 200

@pytest.mark.critical
def test_login_lockout_after_5_failures(client, alice):
    for _ in range(5):
        client.post("/login", json={"email": alice.email, "password": "wrong"})
    assert client.post("/login", json=alice).status_code == 423

@pytest.mark.extended
def test_login_with_100_concurrent_users(client):
    ...
```

Run: `uvx pytest -m smoke`, `uvx pytest -m "smoke or critical"`.

### Recipe 3 — Cypress @cypress/grep tags

```ts
// cypress.config.ts
import { defineConfig } from "cypress";
import grep from "@cypress/grep/src/plugin";

export default defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      grep(config);
      return config;
    },
  },
});

// tests/login.cy.ts
it("login happy path", { tags: ["@smoke"] }, () => { ... });
it("password reset", { tags: ["@critical"] }, () => { ... });
```

```bash
npx cypress run --env grepTags=@smoke
```

### Recipe 4 — Selenium / TestNG groups

```xml
<!-- testng.xml -->
<suite name="Smoke">
  <test name="smoke">
    <groups><run><include name="smoke"/></run></groups>
    <classes><class name="com.app.tests.LoginTests"/></classes>
  </test>
</suite>
```

```java
@Test(groups = {"smoke", "critical"})
public void loginHappyPath() { ... }
```

```bash
mvn test -DsuiteXmlFile=testng-smoke.xml
```

### Recipe 5 — Tiering decision rules

| Tier | Criteria | Time budget | Trigger |
|------|---------|-------------|---------|
| Smoke | Top revenue / data-loss / auth flows | < 5 min | every PR |
| Critical | All major user journeys + integrations | < 30 min | post-merge to main |
| Extended | Edge cases, low-traffic flows, all browsers | unlimited | nightly |
| Quarantine | Flaky pending RCA | n/a | not in gate |

Rule of thumb: 3-10 smoke tests, 30-100 critical, hundreds extended.

### Recipe 6 — CI workflow split by tier

```yaml
# .github/workflows/ci.yml
on:
  pull_request:
  push: { branches: [main] }
  schedule: [{ cron: "0 3 * * *" }]   # nightly extended

jobs:
  smoke:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - run: npx playwright install --with-deps chromium
      - run: npx playwright test --project=smoke
  critical:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    timeout-minutes: 35
    steps:
      - uses: actions/checkout@v4
      - run: npx playwright install --with-deps
      - run: npx playwright test --project=critical
  extended:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    timeout-minutes: 180
    strategy: { matrix: { shard: [1,2,3,4] } }
    steps:
      - uses: actions/checkout@v4
      - run: npx playwright test --project=extended --shard=${{ matrix.shard }}/4
```

### Recipe 7 — Smoke test patterns (the only 5 you really need)

```ts
// tests/login.smoke.spec.ts
test("happy login", async ({ page }) => { /* < 30s */ });

// tests/checkout.smoke.spec.ts
test("checkout one item", async ({ page }) => { /* < 60s */ });

// tests/api-health.smoke.spec.ts
test("api /health returns 200", async ({ request }) => {
  expect((await request.get("/health")).status()).toBe(200);
});

// tests/dashboard.smoke.spec.ts
test("dashboard loads for authed user", async ({ authedPage }) => { /* < 30s */ });

// tests/db.smoke.spec.ts
test("db ping", async () => { /* < 5s */ });
```

If smoke takes longer than 5 min, you're testing too much.

### Recipe 8 — Critical-path coverage matrix

```markdown
| Journey | Test ID | Tier |
|---|---|---|
| Sign up + verify email | tests/auth/signup.critical.spec.ts | critical |
| Log in + 2FA | tests/auth/login.critical.spec.ts | critical |
| Browse → cart → checkout → receipt | tests/checkout/full.critical.spec.ts | critical |
| Admin invites user | tests/admin/invite.critical.spec.ts | critical |
| Subscription upgrade | tests/billing/upgrade.critical.spec.ts | critical |
```

Make it a living doc in the repo; update when journeys change.

### Recipe 9 — Move a test between tiers

```bash
# rename or update tag
git mv tests/auth/lockout.extended.spec.ts tests/auth/lockout.critical.spec.ts

# pytest — change marker
sed -i 's/@pytest.mark.extended/@pytest.mark.critical/' tests/auth/test_lockout.py
```

Reasoning required in PR description ("escape rate showed N% of post-deploy
defects in auth lockout; promoting").

### Recipe 10 — Suite-size SLOs in CI

```yaml
- name: Suite size SLO
  run: |
    SMOKE=$(npx playwright test --project=smoke --list | wc -l)
    if [ "$SMOKE" -gt 12 ]; then
      echo "Smoke suite has $SMOKE tests; budget is 10"
      exit 1
    fi
```

Hard cap prevents smoke creep.

## Examples

### Example 1: Greenfield repo — set tiers from day 1

**Goal:** New project, 0 tests, want healthy suite structure.

1. Create `playwright.config.ts` with smoke/critical/extended projects
   (Recipe 1).
2. Write `tests/smoke/` with 3 happy-path tests; add to CI.
3. Add `tests/critical/` empty; gate on green smoke.
4. Add nightly extended workflow (Recipe 6).
5. Document tier rules in `docs/testing/SUITE_TIERS.md`.

### Example 2: Triage a slow CI — drop tests to critical

**Goal:** PR CI takes 25 min; need < 10 min.

1. `npx playwright test --project=smoke --reporter=line` — measure runtime per
   test.
2. Identify tests > 30s. For each: does it test a smoke-tier journey?
3. Move non-smoke tests to critical: rename `.smoke.spec.ts` → `.critical.spec.ts`.
4. Update CI to run only smoke on PR; critical on main merge.
5. Verify total smoke runtime < 5 min in next CI run.

## Edge cases / gotchas

- **Smoke creep** — every team wants their feature in smoke. Hard cap (5
  min / 10 tests) prevents this.
- **Tier inflation** — promoting "critical" tests to "smoke" because they
  "feel important". Require escape-rate or DORA-failure evidence.
- **Untagged tests** — fall through to slowest tier or get skipped entirely.
  Use `--strict-markers` (pytest) or `--forbid-untagged` (custom CI step).
- **One-tier-only suites** — all tests are "extended" so nothing blocks PR.
  Defeats the point — designate smoke explicitly.
- **Tests that don't fit a tier** — e2e visual diffs are not smoke (slow).
  Use a separate tier (visual / a11y / perf) with their own cadence.
- **Quarantine forever** — quarantined tests must have a 2-week deadline
  (see `flaky-test-quarantine-root-cause` skill).
- **Cypress / Selenium projects** — if migrating from these to Playwright,
  port tier-by-tier (smoke first), keep both running during migration.
- **Tier and parallelism interact** — smoke can run un-sharded (fast); extended
  must shard (long runtime).
- **Don't tag by file path alone** — markers / tags are searchable; folder
  organization rots.
- **Suite duration drifts** — track per-PR runtime; alert when smoke > 5 min.

## Sources

- [Practical Test Pyramid — Martin Fowler](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Playwright projects](https://playwright.dev/docs/test-projects)
- [pytest markers](https://docs.pytest.org/en/stable/how-to/mark.html)
- [@cypress/grep](https://github.com/cypress-io/cypress/tree/develop/npm/grep)
- [TestNG groups](https://testng.org/groups/)
- [Google Testing Blog — flaky-and-fast suites](https://testing.googleblog.com/)
- [The Testing Trophy — Kent C. Dodds](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
