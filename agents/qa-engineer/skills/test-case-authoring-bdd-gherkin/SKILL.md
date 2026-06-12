<!--
Source: https://cucumber.io/docs/bdd/ · https://pytest-bdd.readthedocs.io/ · https://github.com/pavelzw/playwright-bdd
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Test Case Authoring — BDD / Gherkin

Behavior-driven development with Gherkin (Given/When/Then) makes tests
readable by PMs, devs, and QA. The 2026 stack: **Cucumber** for Node/Java,
**pytest-bdd** for Python, **playwright-bdd** when the suite is already
Playwright. Declarative steps, reusable step libraries, and `Scenario Outline`
for parameterization are the rails.

## When to use

- Feature has business-readable acceptance criteria the PM/PO will review
- You want non-engineers to author / review test specs
- Test cases need to live in a test-management tool (Qase / Xray / TestRail
  imports Gherkin)
- 3-amigo refinement produces concrete examples worth capturing
- Trigger phrases: "Gherkin", "BDD", "Cucumber", "feature file", "step
  definition", "scenario outline", "acceptance test"

Do NOT use for: pure unit tests; throwaway debugging tests; performance /
load tests (k6 thresholds beat Gherkin).

## Setup

```bash
# Node.js (Cucumber.js)
npm i -D @cucumber/cucumber

# Python (pytest-bdd)
uv add --dev pytest-bdd

# Playwright + BDD
npm i -D playwright-bdd @playwright/test

# Java (Cucumber JVM)
# In pom.xml:
#   io.cucumber:cucumber-java:7.20.1
#   io.cucumber:cucumber-junit-platform-engine:7.20.1
```

Auth / API key requirements: none.

## Common recipes

### Recipe 1 — Feature file skeleton

```gherkin
# features/password_reset.feature
Feature: Password reset
  As a registered user who forgot their password
  I want to receive a reset link via email
  So that I can regain access without contacting support

  Background:
    Given a registered user with email "alice@example.com"

  Scenario: Reset link sent for a known email
    When I request a password reset for "alice@example.com"
    Then a reset email is sent to "alice@example.com"
    And the email contains a valid reset token

  Scenario: No leak for an unknown email
    When I request a password reset for "unknown@example.com"
    Then the response message is "If the email exists, a reset link was sent"
    And no email is sent

  Scenario Outline: Invalid input rejected
    When I request a password reset for "<email>"
    Then the response status is 400
    Examples:
      | email           |
      |                 |
      | not-an-email    |
      | @nodomain.com   |
```

### Recipe 2 — pytest-bdd step definitions (Python)

```python
# tests/step_defs/test_password_reset.py
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("../features/password_reset.feature")

@given(parsers.parse('a registered user with email "{email}"'))
def register_user(db, email):
    db.users.insert_one({"email": email, "password_hash": "..."})

@when(parsers.parse('I request a password reset for "{email}"'))
def request_reset(client, email, scenario_ctx):
    scenario_ctx["response"] = client.post(
        "/auth/password-reset", json={"email": email}
    )

@then(parsers.parse('a reset email is sent to "{email}"'))
def email_sent(mailbox, email):
    assert any(m["to"] == email for m in mailbox.sent)

@then(parsers.parse('the response status is {status:d}'))
def response_status(scenario_ctx, status):
    assert scenario_ctx["response"].status_code == status
```

Run: `uvx pytest tests/step_defs/ -v`.

### Recipe 3 — Cucumber.js step defs (TypeScript)

```ts
// features/step_definitions/password_reset.steps.ts
import { Given, When, Then, Before } from "@cucumber/cucumber";
import { strict as assert } from "node:assert";
import { ApiClient } from "../support/api";

let client: ApiClient;
let response: Response;

Before(async () => { client = new ApiClient(); });

Given(/^a registered user with email "([^"]+)"$/, async (email) => {
  await client.createUser({ email, password: "seed" });
});

When(/^I request a password reset for "([^"]+)"$/, async (email) => {
  response = await client.post("/auth/password-reset", { email });
});

Then(/^the response status is (\d+)$/, (status: string) => {
  assert.equal(response.status, Number(status));
});
```

```json
// cucumber.json
{
  "default": {
    "paths": ["features/**/*.feature"],
    "require": ["features/step_definitions/*.ts"],
    "requireModule": ["ts-node/register"],
    "format": ["@cucumber/pretty-formatter", "html:reports/cucumber.html"]
  }
}
```

Run: `npx cucumber-js`.

### Recipe 4 — playwright-bdd (best DX for E2E)

```ts
// playwright.config.ts
import { defineConfig } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

const testDir = defineBddConfig({
  features: ["features/**/*.feature"],
  steps: ["features/steps/*.ts"],
});

export default defineConfig({ testDir });
```

```ts
// features/steps/login.ts
import { createBdd } from "playwright-bdd";
const { Given, When, Then } = createBdd();

Given("a user on the login page", async ({ page }) => {
  await page.goto("/login");
});

When("they sign in with {string} and {string}", async ({ page }, email, pw) => {
  await page.getByLabel("Email").fill(email);
  await page.getByLabel("Password").fill(pw);
  await page.getByRole("button", { name: "Sign in" }).click();
});

Then("they land on the dashboard", async ({ page }) => {
  await page.waitForURL("/dashboard");
});
```

```bash
npx bddgen && npx playwright test
```

### Recipe 5 — Reusable step library

```python
# tests/step_defs/common.py
from pytest_bdd import given, when, then, parsers

@given(parsers.parse('I am logged in as "{role}"'))
def login_as(client, role):
    user = make_user(role=role)
    client.login(user)

@then(parsers.parse('the response status is {status:d}'))
def status_is(ctx, status):
    assert ctx["response"].status_code == status
```

Then in any feature: `Given I am logged in as "admin"` works across suites.

### Recipe 6 — Scenario tags + selective runs

```gherkin
@smoke @auth
Scenario: Successful login
  Given a registered user
  When they sign in
  Then they land on the dashboard

@regression @slow
Scenario: 100 concurrent logins
  ...
```

Run only smoke: `npx cucumber-js --tags "@smoke"` /
`uvx pytest -m smoke`.

### Recipe 7 — Data tables (Gherkin → step)

```gherkin
Scenario: Bulk-create users
  Given the following users exist:
    | email             | role  |
    | alice@example.com | admin |
    | bob@example.com   | user  |
  When I list users
  Then I see 2 results
```

```python
@given("the following users exist:")
def create_users(db, datatable):
    for row in datatable:
        db.users.insert_one({"email": row["email"], "role": row["role"]})
```

### Recipe 8 — Background = shared setup

```gherkin
Feature: Shopping cart

  Background:
    Given a logged-in customer "alice@example.com"
    And a product "Widget" priced 9.99 USD in stock

  Scenario: Add to cart
    When the customer adds "Widget" to their cart
    Then the cart total is 9.99 USD
```

`Background` runs before every Scenario in the Feature. Keep it short.

### Recipe 9 — Hooks (setup / teardown)

```ts
// Cucumber.js
import { Before, After, BeforeAll, AfterAll } from "@cucumber/cucumber";
BeforeAll(async () => { await testDb.start(); });
AfterAll(async () => { await testDb.stop(); });
Before({ tags: "@auth" }, async function () { await seedAuthFixtures(this); });
After(async function (scenario) {
  if (scenario.result?.status === "FAILED") {
    const screenshot = await this.page.screenshot();
    this.attach(screenshot, "image/png");
  }
});
```

### Recipe 10 — Export Gherkin → test-management

```bash
# Qase
curl -X POST "https://api.qase.io/v1/case/<project>/import/feature" \
  -H "Token: $QASE_TOKEN" -F "file=@features/auth.feature"

# Xray (Jira)
curl -H "Authorization: Bearer $XRAY_TOKEN" \
  -F "file=@features/auth.feature" \
  "https://xray.cloud.getxray.app/api/v2/import/feature"
```

## Examples

### Example 1: New feature — author + automate from 3-amigo

**Goal:** Capture 3-amigo conversation as executable Gherkin.

1. In refinement, write 1-3 concrete examples per AC on whiteboard.
2. Translate to `features/<feature>.feature` with one Scenario per example.
3. Stub step definitions with `pytest --collect-only` or `npx cucumber-js
   --dry-run` to list missing steps.
4. Implement steps; reuse from `common.py` / `common.steps.ts`.
5. PR runs the feature in CI; PM reviews Gherkin readability.

**Result:** Acceptance criteria become executable contract; refinement becomes
test evidence.

### Example 2: Migrate from imperative E2E to BDD

**Goal:** Convert a 50-line Playwright `test()` to a Scenario.

1. Identify the user-visible behavior (one sentence).
2. Write the Scenario with declarative steps — "I sign in", not "I click
   button#submit".
3. Implement step defs that wrap existing helpers — no business logic in
   steps.
4. Delete the original imperative test once the Scenario is green.

## Edge cases / gotchas

- **Imperative steps** — `When I click #submit-btn` is an antipattern. Use
  `When I submit the form`. Step implementations hide the selector.
- **Steps with side effects on each other** — keep steps stateless except
  via the `World` (Cucumber) or fixtures (pytest-bdd).
- **Scenario Outlines with 20+ rows** — split into a Scenario per concept;
  use Outline only for data variation.
- **Feature files in multiple languages** — `# language: fr` directive
  enables localized keywords. Avoid mixing.
- **Step regex collisions** — Cucumber will silently match the first; prefer
  `parsers.parse` or Cucumber expressions over raw regex.
- **Hooks too coarse** — `BeforeAll` that seeds prod-like data slows the
  suite. Use `Before({ tags: "@needs-fixture" })` to scope.
- **One step that does everything** — `When I do the thing` step that calls
  10 helpers becomes opaque. Decompose.
- **BDD for unit tests** — overkill. Gherkin is for cross-team conversation,
  not for asserting a function returns 42.
- **Gherkin in CI report** — render to HTML with Cucumber HTML or pytest-bdd
  `--gherkin-terminal-reporter` for stakeholder visibility.
- **Mixing Gherkin and code in step bodies** — step body should call one
  helper. If your step body has 30 lines, extract.

## Sources

- [Cucumber BDD docs](https://cucumber.io/docs/bdd/)
- [pytest-bdd docs](https://pytest-bdd.readthedocs.io/)
- [playwright-bdd](https://github.com/vitalets/playwright-bdd)
- [Specification by Example — Gojko Adzic](https://gojko.net/books/specification-by-example/)
- [Cucumber best practices](https://cucumber.io/docs/bdd/better-gherkin/)
- [Xray import API](https://docs.getxray.app/display/XRAYCLOUD/Importing+Cucumber+Tests)
- [Qase BDD import](https://help.qase.io/en/articles/5563566-bdd-test-management)
