# QA / Test Engineer — deep reference

This section appends to `AGENT.md`. It is **not** in the agent's default context. Grep it when the SOUL.md summary isn't enough.

Searchable headings: "Capability reference", "Test plan template", "BDD authoring playbook", "Antipattern catalog", "Accessibility audit playbook", "Performance test playbook", "Contract testing playbook", "Flaky test triage playbook", "Defect triage matrix", "Release readiness checklist", "SOTA tool reference (June 2026)".

For provenance of any section, see `SOURCES.md` in this bundle.

---

## Capability reference

Pure factual reference — what tools, frameworks, and patterns exist in the QA ecosystem. SOUL.md does not carry these (they don't drive turn-by-turn decisions); grep here when the user asks "what should I use for X?"

### E2E frameworks (browser)

- **Playwright** — default 2026 choice. Chromium / Firefox / WebKit bundled. Free parallel sharding. Multi-language (TS / JS / Python / Java / .NET). Auto-waiting. Microsoft-backed. 33M weekly npm downloads (vs Cypress 6.5M).
- **Cypress** — best interactive DX / time-travel debugger. Chrome-only by default. Paid parallelism. Component testing native.
- **Selenium** — legacy; only for codebases where it's already in place. Replaced by Playwright/Cypress for new work.
- **Puppeteer** — Chrome DevTools Protocol direct; useful when Playwright's abstraction is unwanted. Same author team migrated to Playwright.
- **WebdriverIO** — popular Appium pair; standards-based; cross-platform.
- **TestCafe** — proxy-based; no browser driver; works without admin. Niche.

### Unit / integration frameworks

- **Python** — `pytest` 9.x default; `pytest-asyncio` for async; `pytest-bdd` for Gherkin; `pytest-xdist` for parallel; `pytest-rerunfailures` for retries; `pytest-mock` for fixtures; `hypothesis` for property-based; `freezegun` for time mocking; `testcontainers` for real DB/Redis/Kafka.
- **JS/TS** — `vitest` (Vite-native, default 2026) > `jest` (legacy, slower) > `mocha` (assertion-library agnostic). `@testing-library/react` for component; `supertest` for API; `msw` for HTTP mocking.
- **Java** — JUnit 5 default; AssertJ for fluent assertions; Mockito for mocks; Rest Assured for API.
- **.NET** — xUnit / NUnit / MSTest; Moq for mocks.
- **Ruby** — RSpec dominant.

### API testing

- **Bruno** — 2026 default for new repos. OSS. Git-native `.bru` files. `bru` CLI. No telemetry.
- **Postman** — enterprise standard. Workspaces, mock servers, monitors. Newman CLI for CI.
- **Insomnia** — middle ground. Native GraphQL. Kong-owned (some pricing changes since acquisition).
- **REST Assured** — Java BDD-style API assertions.
- **Karate** — Java; combines Gherkin + API + perf + UI.
- **httpie / curl** — ad-hoc one-offs via `cli-anything`.
- **HTTP mocking** — `msw` (Mock Service Worker), `WireMock`, `Mountebank`, `Mirage JS`, `nock` (Node), `vcrpy` / `respx` / `pytest-httpx` (Python).

### Contract testing

- **Pact** — consumer-driven. Brokers: Pact Broker (OSS Docker) or PactFlow (hosted, paid).
- **Spring Cloud Contract** — JVM ecosystem; producer-driven.
- **Bi-directional Pact** — works with existing OpenAPI specs; easier adoption for spec-first teams.
- **OpenAPI / AsyncAPI validators** — `prism` (CLI), `dredd`, `apisprout` for spec compliance.

### Performance / load

- **k6** — 2026 default. Go runtime; JS scripts. Declarative `thresholds`. Grafana Cloud k6. Strong CI fail-on-breach.
- **Locust** — Python; live web UI. Choice for Python shops.
- **Artillery** — Node.js. Plugin ecosystem.
- **Gatling** — JVM, Scala DSL. Best perf-per-VU.
- **JMeter** — legacy; XML GUI; only when already in place.
- **Bombardier** — Go binary; HTTP smoke perf.
- **wrk / wrk2** — minimalist HTTP load.

### Security / DAST / SAST

- **OWASP ZAP** — free DAST; official GitHub Actions; SARIF output. Default for CI.
- **Burp Suite Pro** — manual pentest; Burp Enterprise DAST in CI (paid).
- **Snyk** — dep CVE + IaC + container; SaaS.
- **Semgrep** — SAST; community rulesets; `--config=auto`.
- **CodeQL** — GitHub's SAST; deep dataflow.
- **Trivy / Grype** — container + dep CVE scanners.
- **`pip-audit`** (Python) / **`npm audit`** (Node) / **`osv-scanner`** (Google multi-eco).
- **`gitleaks`** / **`trufflehog`** — secrets detection.
- **Pynt** / **42Crunch** — API security testing.

### Accessibility

- **axe-core (Deque)** — gold standard rule engine. ~57% automated WCAG detection. Embedded in Lighthouse a11y, Pa11y, axe DevTools browser extension.
- **pa11y** — CLI + Pa11y CI for CI pipelines. axe-core + HTML CodeSniffer.
- **Lighthouse** — Google; subset of axe-core + perf + SEO + PWA. CI via `lighthouse --only=accessibility`.
- **Accessibility Insights for Web** — Microsoft; FastPass + Assessment workflows.
- **WAVE** — WebAIM; browser extension + API.
- **Stark** — design-system a11y in Figma/Sketch/XD/Adobe.
- **Tenon** — paid; broader rule set than axe.
- **Screen readers** (manual) — NVDA (Windows free), JAWS (Windows paid), VoiceOver (macOS/iOS), TalkBack (Android), Narrator (Windows).
- **WCAG levels** — 2.0 → 2.1 → 2.2 (current 2026 floor for new builds); 3.0 working draft.

### Visual regression

- **Playwright native** — `expect(page).toHaveScreenshot()` + `--update-snapshots`. Free; baseline in Git.
- **Applitools Eyes** — perceptual Visual AI; longest head start; enterprise.
- **Chromatic** — Storybook-first; component-level; review UI.
- **Percy (BrowserStack)** — pixel + AI Visual Review Agent (2026); BrowserStack-bundled.
- **Reflect** — full-flow visual + interaction.
- **BackstopJS** — OSS Puppeteer-based.

### Cross-browser cloud

- **BrowserStack** — 30k+ devices/browsers; published pricing tiers; large real-device farm.
- **Sauce Labs** — deeper analytics (Sauce Insights); enterprise compliance at lower tiers; better mobile SDK.
- **TestMu AI (LambdaTest rebrand 2026)** — cheaper + KaneAI for AI-assisted authoring.
- **CrossBrowserTesting (Smartbear)** — niche.
- **Headspin** — real-device mobile + perf.

### Mobile

- **Maestro** — YAML; fastest setup (10-15 min); iOS + Android + RN + Flutter + web. Greenfield default.
- **Detox** — React Native; grey-box; <2% flakiness; testID-based.
- **Appium** — cross-platform/cross-language; deepest ecosystem; 15-20% flakiness baseline.
- **WebdriverIO + Appium** — JS/TS Appium of choice; better DX.
- **XCUITest** — native iOS.
- **Espresso** — native Android.
- **Earl Grey** — Google's iOS UI testing.
- **EarlGrey 2** — XCUITest + EarlGrey.
- **BrowserStack App Live / Sauce Real Device** — real-device cloud.

### Test management

- **TestRail** — web-based; widely adopted; aging UI.
- **Qase** — cloud-based; transparent pricing; AI features.
- **Zephyr Scale / Squad / Enterprise** — Jira-native add-ons.
- **Xray** — Jira-native; deepest Jira integration.
- **TestMo** — cloud; manual + exploratory + automated unified.
- **QMetry** — Jira / Confluence ecosystem.
- **TestLink** — OSS legacy.
- **PractiTest** — risk-based test management.

### AI test maintenance / authoring

- **Mabl** — agentic; self-healing; AI since 2017.
- **Testim (Tricentis)** — AI stability features for web/cloud-native.
- **Functionize** — NLP test authoring; adaptive learning.
- **Reflect** — record + AI maintenance.
- **Testsigma** — NLP authoring; cross-platform.
- **Katalon Studio** — web/mobile/desktop/API unified.
- **QA Wolf** — outsourced + tool combo.

### Mutation testing

- **Stryker** — JS/TS, .NET, Scala. Thoughtworks Radar 2026 Trial. AI-pruned mutants (~30% noise reduction).
- **mutmut** — Python; 88.5% detection; 1200 mutants/min.
- **Pitest** — Java/JVM; configurable; rich mutators.
- **MutPy** — Python; superseded by mutmut.
- **cargo-mutants** — Rust.

### Code quality gates

- **SonarQube** (self-host) / **SonarCloud** (SaaS) — coverage + duplication + complexity + security + AI code assurance gate. PR status check.
- **CodeClimate** — maintainability score + tech debt.
- **DeepSource** — multi-language SAST + tech debt.
- **Codacy** — SaaS static analysis.
- **GitGuardian** — secrets + IaC.

### Test data

- **Faker.js / Faker (Python) / Faker (Ruby)** — column-level synthetic generation.
- **Mockaroo** — schema-based rule-driven mock.
- **Tonic.ai** — production-like masked synthetic; enterprise.
- **GenRocket** — model-driven test data factory.
- **Synth** — declarative data generator (Rust).
- **MakeFake** — rapid mock data.

### Reporting / dashboards

- **Allure Report** — HTML; Jira integration; multi-language.
- **ReportPortal** — AI-driven aggregation; OSS.
- **Playwright HTML reporter** — bundled; trace viewer.
- **pytest-html** — single-file HTML.
- **Currents** — Cypress/Playwright analytics SaaS.
- **Foresight** — CI insights + test analytics.
- **Datadog CI Visibility** — CI + tests unified.

---

## Test plan template (ISO 29119-3 + HTSM lite)

```markdown
# Test Plan — <Feature>

## 1. Identifier
- Plan ID: TP-<feature-slug>-vN
- Sprint: <NN>
- Owner: <name>

## 2. Scope
- In scope: <bulleted features>
- Out of scope: <bulleted exclusions>

## 3. Risk model (HTSM-lite)
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| <risk> | H/M/L | H/M/L | <action> |

## 4. Test approach
- Tiering: smoke / critical / extended / quarantine
- Trophy ratio target: 25% static / 15% unit / 40% integration / 15% E2E / 5% manual
- Frameworks: <Playwright / pytest / k6 / axe-core / Pact>
- Test data: <synthetic / fixtures>

## 5. Pass/fail criteria
- All smoke green (< 5 min)
- All critical-path green (< 30 min)
- a11y gate: 0 WCAG 2.2 AA violations
- perf gate: p99 < <budget>
- Security gate: 0 high-severity ZAP alerts
- 0 open P0/P1 defects
- Mutation score > 60%

## 6. Entry / exit criteria
- Entry: feature merged to staging, deploy green.
- Exit: all pass criteria met OR product-owner override documented.

## 7. Reporting
- Allure / Playwright HTML linked in PR
- Slack digest end-of-sprint
- Notion KPI page updated
```

---

## BDD authoring playbook

### Gherkin scenario shape

```gherkin
Feature: User can reset their password
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
    Then the response is generic "If the email exists, a reset link was sent"
    And no email is sent

  Scenario Outline: Invalid input rejected
    When I request a password reset for "<email>"
    Then the response status is 400
    Examples:
      | email |
      | "" |
      | "not-an-email" |
      | "@nodomain.com" |
```

### Step definition (pytest-bdd)

```python
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("features/password_reset.feature")

@given(parsers.parse('a registered user with email "{email}"'))
def register_user(db, email):
    db.users.insert({"email": email, "password_hash": "..."})

@when(parsers.parse('I request a password reset for "{email}"'))
def request_reset(client, email):
    return client.post("/auth/password-reset", json={"email": email})
```

### Rules

- Declarative steps, not imperative. "When I submit the form" beats "When I click `#submit`".
- One scenario = one behavior. No "And then I also..."
- Background for setup shared across scenarios.
- `Scenario Outline` for parameterized cases.
- Step defs reusable across feature files.

---

## Accessibility audit playbook

### Phase 1 — automated baseline

```bash
# axe-core CLI
npx @axe-core/cli https://staging.example.com/page --tags=wcag22aa --exit

# pa11y CI
npx pa11y-ci --sitemap https://staging.example.com/sitemap.xml

# Lighthouse a11y only
npx lighthouse https://staging.example.com/page --only-categories=accessibility \
  --output=html --output-path=./lighthouse-a11y.html

# Playwright + axe-core
import { test, expect } from '@playwright/test';
import { AxeBuilder } from '@axe-core/playwright';

test('homepage has no a11y violations', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).withTags(['wcag22aa']).analyze();
  expect(results.violations).toEqual([]);
});
```

### Phase 2 — manual pass

Automated tools catch ~30-57%. The remaining 40-70% requires manual:

- **Keyboard navigation** — Tab through every interactive element. No traps. Focus visible.
- **Screen reader** — NVDA + Chrome (Windows free); VoiceOver + Safari (macOS). Verify reading order, ARIA labels, live regions.
- **Color contrast** — automated catches static; manual catches dynamic (e.g., hover/focus states the tool didn't reach).
- **Zoom 200%** — content reflows; no horizontal scroll; no truncation.
- **Reduced motion** — prefers-reduced-motion CSS respected.
- **Form errors** — announced by screen reader; programmatically associated.

### Phase 3 — CI gate

```yaml
# .github/workflows/a11y.yml
on: [pull_request]
jobs:
  axe:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test --project=a11y
      - if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: axe-violations
          path: test-results/
```

---

## Performance test playbook

### Step 1 — ask budget

- **p50, p99 latency** under what load?
- **Throughput** target (req/s)?
- **Error rate** ceiling (typically < 1%)?
- **Resource budget** (CPU / memory / cost)?

If they don't know, that's the answer — measure baseline first.

### Step 2 — k6 script

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },   // warm-up
    { duration: '2m', target: 200 },   // ramp
    { duration: '5m', target: 200 },   // steady
    { duration: '30s', target: 0 },    // ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(99)<800', 'p(95)<400'],
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/users/me', {
    headers: { Authorization: `Bearer ${__ENV.TOKEN}` },
  });
  check(res, {
    'status 200': r => r.status === 200,
    'body has user': r => JSON.parse(r.body).id !== undefined,
  });
  sleep(1);
}
```

### Step 3 — locust alternative (Python shops)

```python
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def get_user(self):
        with self.client.get("/users/me", catch_response=True) as r:
            if r.elapsed.total_seconds() > 0.8:
                r.failure("p99 budget exceeded")

    @task(1)
    def post_order(self):
        self.client.post("/orders", json={"product_id": 42, "qty": 1})
```

### Step 4 — CI integration

```yaml
- name: Run k6 load test
  run: |
    docker run --rm -v $PWD:/scripts grafana/k6 run /scripts/load.js \
      --out json=results.json
- name: Upload k6 results
  uses: actions/upload-artifact@v4
  with: { name: k6-results, path: results.json }
```

Fail the build on threshold breach (k6 returns non-zero exit code).

---

## Contract testing playbook (Pact)

### Consumer side (JS/TS)

```javascript
import { PactV3, MatchersV3 } from '@pact-foundation/pact';
const { like, eachLike, integer, string } = MatchersV3;

const provider = new PactV3({ consumer: 'WebApp', provider: 'OrdersAPI' });

test('GET /orders returns list', async () => {
  await provider
    .uponReceiving('a request for orders')
    .withRequest({ method: 'GET', path: '/orders' })
    .willRespondWith({
      status: 200,
      body: eachLike({ id: integer(1), total: like(99.99), status: string('pending') }),
    });

  await provider.executeTest(async (mockServer) => {
    const orders = await fetchOrders(mockServer.url);
    expect(orders).toHaveLength(1);
  });
});
```

### Publish + verify

```bash
# Consumer publishes pact to broker
pact-broker publish ./pacts \
  --consumer-app-version=$GIT_SHA \
  --broker-base-url=$PACT_BROKER_URL

# Provider verifies
pact-provider-verifier --provider-base-url=https://staging-orders \
  --pact-broker-url=$PACT_BROKER_URL \
  --provider OrdersAPI

# Pre-deploy gate
pact-broker can-i-deploy --pacticipant WebApp \
  --version $GIT_SHA --to-environment production
```

### Rules

- Pacts express interactions, not specs. Use OpenAPI for specs; bi-directional Pact bridges them.
- `can-i-deploy` is a CI gate, not advice.
- Keep provider states minimal — large state machines fight you.
- Run provider verification in the provider's CI, not a shared env.
- Version your APIs explicitly (path, header, content negotiation).

---

## Flaky test triage playbook

### Step 1 — detect

```bash
# pytest — collect history
pytest --json-report --json-report-file=report.json
# Run 10x: those failing 1-9 times = flaky
for i in {1..10}; do pytest --json-report --json-report-file=run-$i.json; done

# Playwright — built-in flaky detection
npx playwright test --reporter=json --retries=2
# Tests retried but ultimately passed appear as `flaky` in report.json

# GitHub Actions — flaky test action
- uses: ksuderman/flaky-test-detector@v1
```

### Step 2 — quarantine

```python
# pytest — quarantine
@pytest.mark.flaky(reruns=2, reruns_delay=1)
@pytest.mark.quarantine  # custom marker, excluded from blocking gate
def test_known_flaky_payment_flow():
    ...

# pytest.ini
[pytest]
markers =
    quarantine: flaky tests; not run in PR gate

# Run gate without quarantined:
pytest -m "not quarantine"
```

```typescript
// Playwright — quarantine via project
// playwright.config.ts
projects: [
  { name: 'main', testIgnore: /.*\.quarantine\.spec\.ts/ },
  { name: 'quarantine', testMatch: /.*\.quarantine\.spec\.ts/, retries: 3 },
],
```

### Step 3 — root cause categorize

| Category | % | Common cause | Fix |
|---|---|---|---|
| Timing | ~70% | Race / waitForTimeout / animation | Web-first assertions; `expect(...).toPass()`; explicit waits |
| DOM / selector | ~28% | Brittle CSS / nth-child | Use `getByRole` / `getByTestId`; avoid index selectors |
| Network / data | ~2% | Real API rate limit / shared DB | Mock with `msw` / `respx`; testcontainers; per-test cleanup |

### Step 4 — fix or remove (2-week deadline)

- Quarantine ticket: owner, deadline = today + 14 days, RCA category.
- After 14 days unfixed: remove the test. A flaky test that nobody fixes is worse than no test.

---

## Defect triage matrix

| Severity \ Priority | P0 (ship-blocker) | P1 (next release) | P2 (backlog) | P3 (nice-to-have) |
|---|---|---|---|---|
| **S1 (crash / data loss)** | Hotfix within 24h | Fix in current sprint | — | — |
| **S2 (major broken)** | Fix in current sprint | Fix in next sprint | Backlog | — |
| **S3 (minor)** | — | Fix in next sprint | Backlog | Tech debt |
| **S4 (cosmetic)** | — | — | Backlog | Tech debt / won't fix |

- **Severity** = engineering impact. Determined by QA + dev.
- **Priority** = business urgency. Determined by PM/PO.
- A high-severity / low-priority bug is possible (corner case affecting 0.1% of users that crashes their browser — S1/P2).

---

## Release readiness checklist

Pre-deploy binary gates. Each must be green.

- [ ] **Smoke suite green** — last 24h
- [ ] **Critical-path suite green** — last 24h
- [ ] **Extended regression green** — last 7 days (nightly cadence)
- [ ] **Accessibility gate green** — 0 WCAG 2.2 AA violations on changed pages
- [ ] **Performance budget hit** — p99 within budget; no regression > 10% vs last release
- [ ] **Security gate green** — 0 ZAP high-severity; 0 critical CVEs in deps; 0 leaked secrets
- [ ] **Contract gate green** — `pact-broker can-i-deploy` for all consumers
- [ ] **Mutation score above floor** — > 60% on changed files
- [ ] **0 open P0 defects** — verified in Jira/Linear
- [ ] **0 open P1 defects** without product-owner waiver
- [ ] **Canary 24h clean** — error rate / latency / saturation within baseline
- [ ] **Rollback plan documented** — runbook + responsible owner
- [ ] **Feature flag default-off** if risk > medium
- [ ] **Observability ready** — dashboards / alerts / on-call rotation in place

Any red item → hold or go-with-mitigation. Surface in PR description / Notion release doc.

---

## Antipattern catalog

### Sleep-driven E2E

**BAD:**
```javascript
await page.click('#submit');
await page.waitForTimeout(5000);
expect(await page.locator('.message').textContent()).toBe('Success');
```
**Why it's bad:** Timing-dependent. Flaky on slow CI; wastes time on fast CI. Tells you nothing about the real wait condition.

**GOOD:**
```javascript
await page.click('#submit');
await expect(page.locator('.message')).toHaveText('Success');
```
**Why it's better:** Playwright's `toHaveText` auto-retries with a sane timeout. No magic number. Test reads as intent.

### Shared mutable state across tests

**BAD:**
```python
# tests/test_users.py
def test_create_user(db):
    db.users.insert({"email": "alice@example.com"})  # leaks into next test
def test_login_alice(db):
    user = db.users.find_one({"email": "alice@example.com"})  # depends on order
```
**Why it's bad:** Hidden coupling. Reorder = breaks. Parallel = breaks.

**GOOD:**
```python
@pytest.fixture
def alice(db):
    user = db.users.insert({"email": "alice@example.com"})
    yield user
    db.users.delete(user.id)

def test_login_alice(client, alice):
    response = client.post("/login", json={"email": alice.email})
    assert response.status_code == 200
```

### Mocking the system under test

**BAD:**
```javascript
test('user service creates user', () => {
  const userService = new UserService();
  jest.spyOn(userService, 'createUser').mockResolvedValue({ id: 42 });
  expect(userService.createUser({...})).resolves.toEqual({ id: 42 });
});
```
**Why it's bad:** Verifies the mock, not the system. Useless signal.

**GOOD:**
```javascript
test('user service creates user', async () => {
  // testcontainers Postgres
  await using container = await new PostgreSqlContainer().start();
  const userService = new UserService(container.getConnectionUri());
  const user = await userService.createUser({ email: 'alice@example.com' });
  expect(user.id).toBeDefined();
});
```

### Auto-approved snapshots

**BAD:**
```bash
# CI runs: npx playwright test --update-snapshots
git add . && git commit -m "fix tests"
```
**Why it's bad:** Snapshots are documentation of expected output. Auto-approve = no review = no signal.

**GOOD:**
- Snapshots updated only via explicit PR with human review.
- CI fails on snapshot mismatch; developer regenerates locally + commits.

### Coverage as the only quality signal

**BAD:**
```python
def test_user_service():
    service.create_user(valid_data)  # 100% coverage; never asserts anything
```
**Why it's bad:** Coverage tells you the code ran. Says nothing about correctness. Mutation testing exposes this.

**GOOD:** Track mutation score alongside coverage. A 100% covered file with 20% mutation score is poorly tested.

### E2E for what unit could cover

**BAD:** Playwright test that exercises a date-formatting utility.
**Why it's bad:** 5s vs 5ms. Same signal. Slow CI.
**GOOD:** Unit test for the utility. E2E reserved for cross-system flows.

---

## SOTA tool reference (June 2026)

Grep-friendly per-tool reference. Each tool gets 10-30 lines naming the verb, source, canonical commands, and the bundled skill pack.

### Playwright — E2E framework (default 2026)

**Use for:** any browser-based E2E test. Cross-browser (Chromium / Firefox / WebKit). Visual regression via `toHaveScreenshot`. Cross-platform mobile via emulation.
**Skill pack:** `regression-suite-curation-smoke-critical` + default `playwright-mcp`
**Install:** `npm i -D @playwright/test && npx playwright install`
**Quick recipe:**
```bash
npx playwright test --project=chromium --grep=@smoke
npx playwright test --shard=1/4
npx playwright show-report
```
**Source:** https://playwright.dev/docs

### axe-core — accessibility rule engine

**Use for:** WCAG 2.0 / 2.1 / 2.2 A/AA/AAA automated checks.
**Skill pack:** `accessibility-testing-wcag-22-aa-axe`
**Install:** `npm i -D @axe-core/playwright @axe-core/cli`
**Quick recipe:**
```bash
npx @axe-core/cli https://staging.example.com --tags=wcag22aa --exit
# In Playwright test:
const results = await new AxeBuilder({ page }).withTags(['wcag22aa']).analyze();
```
**Source:** https://www.deque.com/axe/axe-core/

### pa11y / pa11y-ci — accessibility CI

**Use for:** sitemap-driven CI a11y gates.
**Skill pack:** `accessibility-testing-wcag-22-aa-axe`
**Install:** `npm i -D pa11y-ci`
**Quick recipe:**
```bash
npx pa11y-ci --sitemap https://staging.example.com/sitemap.xml
# .pa11yci config: threshold, ignore rules, viewport
```
**Source:** https://pa11y.org/

### Lighthouse — a11y / perf / SEO audit

**Use for:** PageSpeed + a11y subset + best practices. Embedded in Chrome DevTools.
**Skill pack:** `accessibility-testing-wcag-22-aa-axe`
**Install:** `npm i -D lighthouse`
**Quick recipe:**
```bash
npx lighthouse https://staging.example.com --only-categories=accessibility \
  --output=html --output-path=./lighthouse-a11y.html
```
**Source:** https://developer.chrome.com/docs/lighthouse/

### k6 — load testing (default 2026)

**Use for:** HTTP / WebSocket / gRPC load tests with declarative thresholds.
**Skill pack:** `performance-testing-k6-locust-artillery`
**Install:** `brew install k6` or `docker run grafana/k6`
**Quick recipe:**
```bash
k6 run script.js
k6 run --out json=results.json script.js
k6 cloud script.js   # Grafana Cloud k6
```
**Source:** https://k6.io/docs/

### Locust — Python load testing

**Use for:** Python-shop performance testing; live web UI.
**Skill pack:** `performance-testing-k6-locust-artillery`
**Install:** `uv add --dev locust` or `uvx locust`
**Quick recipe:**
```bash
uvx locust -f locustfile.py --host=https://api.example.com
uvx locust -f locustfile.py --headless -u 100 -r 10 -t 5m
```
**Source:** https://docs.locust.io/

### Artillery — Node.js load testing

**Use for:** Node-shop perf testing with plugin ecosystem.
**Skill pack:** `performance-testing-k6-locust-artillery`
**Install:** `npm i -g artillery`
**Quick recipe:**
```bash
artillery run scenario.yml
artillery quick --count 50 --num 10 https://api.example.com
```
**Source:** https://www.artillery.io/docs

### Bruno — Git-native API client (default 2026)

**Use for:** REST / GraphQL collections committed in Git.
**Skill pack:** `api-testing-postman-bruno-newman`
**Install:** `npm i -g @usebruno/cli`
**Quick recipe:**
```bash
bru run --env production
bru run collection/ --reporter-json results.json
```
**Source:** https://docs.usebruno.com/

### Postman + Newman — enterprise API testing

**Use for:** Postman collections in CI; mock servers; monitors.
**Skill pack:** `api-testing-postman-bruno-newman`
**Install:** `npm i -g newman`
**Quick recipe:**
```bash
newman run collection.json -e env.json --reporters cli,html
```
**Source:** https://learning.postman.com/docs/

### Pact — consumer-driven contracts

**Use for:** verifying provider/consumer agree on API shape.
**Skill pack:** `contract-testing-pact`
**Install:** `npm i -D @pact-foundation/pact @pact-foundation/pact-node`
**Quick recipe:**
```bash
pact-broker publish ./pacts --consumer-app-version=$GIT_SHA --broker-base-url=$PACT_BROKER_URL
pact-broker can-i-deploy --pacticipant WebApp --version $GIT_SHA --to-environment production
```
**Source:** https://docs.pact.io/

### OWASP ZAP — DAST in CI

**Use for:** automated DAST against staging URL; SARIF output for GitHub code scanning.
**Skill pack:** `security-testing-owasp-zap-burp`
**Install:** `docker pull zaproxy/zap-stable`
**Quick recipe:**
```bash
docker run -t zaproxy/zap-stable zap-baseline.py -t https://staging.example.com
# GitHub Action:
- uses: zaproxy/action-baseline@v0.12.0
  with: { target: 'https://staging.example.com' }
```
**Source:** https://www.zaproxy.org/ · https://github.com/zaproxy/action-baseline

### Burp Suite — manual pentest

**Use for:** manual pentest engagements; deep inspection; Burp Enterprise for paid CI DAST.
**Skill pack:** `security-testing-owasp-zap-burp`
**Source:** https://portswigger.net/burp

### Snyk / pip-audit / osv-scanner — dep CVE

**Use for:** dep vulnerability scanning in CI.
**Skill pack:** `security-testing-owasp-zap-burp`
**Quick recipe:**
```bash
uvx pip-audit
npx snyk test
osv-scanner -r .
```
**Source:** https://snyk.io/ · https://pypi.org/project/pip-audit/ · https://google.github.io/osv-scanner/

### Faker — synthetic test data

**Use for:** programmatic fake data generation.
**Skill pack:** `test-data-management-synthetic`
**Install (Python):** `uv add --dev faker`
**Install (JS):** `npm i -D @faker-js/faker`
**Quick recipe:**
```python
from faker import Faker
fake = Faker()
user = {"name": fake.name(), "email": fake.email(), "address": fake.address()}
```
**Source:** https://faker.readthedocs.io/ · https://fakerjs.dev/

### Mockaroo — schema-based mock data

**Use for:** realistic dataset generation via web UI or API.
**Skill pack:** `test-data-management-synthetic`
**Source:** https://mockaroo.com/

### Tonic.ai — production-like masked synthetic

**Use for:** statistically representative synthetic data from prod schemas, GDPR-safe.
**Skill pack:** `test-data-management-synthetic`
**Source:** https://www.tonic.ai/

### Stryker — JS/TS/.NET mutation testing

**Use for:** verifying test suite catches injected bugs (kill rate).
**Skill pack:** `mutation-testing-stryker-mutmut`
**Install:** `npx stryker init`
**Quick recipe:**
```bash
npx stryker run
# stryker.conf.js: mutate, testRunner, reporters
```
**Source:** https://stryker-mutator.io/

### mutmut — Python mutation testing

**Use for:** Python suite kill rate; 88.5% detection.
**Skill pack:** `mutation-testing-stryker-mutmut`
**Install:** `uv add --dev mutmut` or `uvx mutmut`
**Quick recipe:**
```bash
uvx mutmut run
uvx mutmut results
uvx mutmut show <id>
```
**Source:** https://github.com/boxed/mutmut

### Pitest — JVM mutation testing

**Use for:** Java/Kotlin/Scala mutation testing.
**Skill pack:** `mutation-testing-stryker-mutmut`
**Source:** https://pitest.org/

### BrowserStack / Sauce Labs / TestMu AI — cross-browser cloud

**Use for:** real-device coverage + older browser versions when local Playwright isn't enough.
**Skill pack:** `cross-browser-browserstack-saucelabs-lambdatest`
**Source:** https://www.browserstack.com/automate · https://saucelabs.com/products/automated-testing

### Maestro — mobile E2E (default 2026)

**Use for:** YAML-driven mobile E2E for iOS / Android / RN / Flutter / web. Fastest setup.
**Skill pack:** `mobile-testing-real-devices-emulators`
**Install:** `curl -Ls https://get.maestro.mobile.dev | bash`
**Quick recipe:**
```bash
maestro test flows/login.yaml
maestro studio  # interactive recorder
```
**Source:** https://maestro.dev/docs

### Detox — React Native E2E

**Use for:** pure React Native; lowest flakiness (<2%) via grey-box sync.
**Skill pack:** `mobile-testing-real-devices-emulators`
**Source:** https://wix.github.io/Detox/

### Appium + WebdriverIO — cross-platform mobile

**Use for:** native + hybrid + cross-language + cross-platform.
**Skill pack:** `mobile-testing-real-devices-emulators`
**Source:** https://appium.io/

### Applitools Eyes — perceptual visual AI

**Use for:** enterprise visual regression with Visual AI engine.
**Skill pack:** `visual-regression-percy-chromatic-applitools`
**Source:** https://applitools.com/

### Chromatic — Storybook-first visual

**Use for:** component-level visual regression for Storybook teams.
**Skill pack:** `visual-regression-percy-chromatic-applitools`
**Quick recipe:**
```bash
npx chromatic --project-token=$CHROMATIC_TOKEN
```
**Source:** https://www.chromatic.com/

### Percy — BrowserStack-integrated visual

**Use for:** mid-market visual regression bundled with BrowserStack.
**Skill pack:** `visual-regression-percy-chromatic-applitools`
**Source:** https://percy.io/

### Allure — multi-language test reporting

**Use for:** rich HTML reports with Jira integration; multi-framework.
**Skill pack:** `test-reporting-dashboards`
**Install:** `uvx allure` or `npm i -D allure-playwright`
**Quick recipe:**
```bash
uvx allure serve allure-results/
```
**Source:** https://allurereport.org/

### ReportPortal — AI test report aggregation

**Use for:** unified test reporting across CI; AI-driven defect categorization.
**Skill pack:** `test-reporting-dashboards`
**Source:** https://reportportal.io/

### SonarQube / SonarCloud — code quality gates

**Use for:** coverage + duplication + complexity + security hotspots as PR gates.
**Skill pack:** `quality-kpis-escape-rate-mttr`
**Quick recipe:**
```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube:lts-community
sonar-scanner -Dsonar.projectKey=myproject -Dsonar.host.url=http://localhost:9000
```
**Source:** https://docs.sonarsource.com/sonarqube-server/

### testcontainers — real backends in tests

**Use for:** real Postgres / Redis / Kafka / Mongo per test.
**Skill pack:** uses parent's `testcontainers-integration-testing` skill
**Source:** https://testcontainers.com/

### pytest-rerunfailures / Playwright `retries` — flake mitigation

**Use for:** quarantined-test reruns while RCA is pending.
**Skill pack:** `flaky-test-quarantine-root-cause`
**Source:** https://github.com/pytest-dev/pytest-rerunfailures · https://playwright.dev/docs/test-retries

### `pact-broker can-i-deploy` — release gate

**Use for:** binary go/no-go on contract compatibility before prod deploy.
**Skill pack:** `contract-testing-pact`
**Source:** https://docs.pact.io/pact_broker/can_i_deploy

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Write a test plan for X" | `test-plan-authoring-pmbok-iso` | ISO 29119-3 + HTSM risk model |
| "Add E2E tests for the login flow" | `regression-suite-curation-smoke-critical` + `playwright-mcp` | Playwright default; smoke tier |
| "Test our app for accessibility" | `accessibility-testing-wcag-22-aa-axe` | axe + pa11y + Lighthouse; manual NVDA pass |
| "Load test the API" | `performance-testing-k6-locust-artillery` | k6 default; Locust if Python shop |
| "Set up API testing" | `api-testing-postman-bruno-newman` | Bruno default 2026; Postman if enterprise |
| "Add contract tests between services" | `contract-testing-pact` | Pact + Pact Broker + can-i-deploy gate |
| "Security scan the staging URL" | `security-testing-owasp-zap-burp` | ZAP baseline + SARIF upload |
| "Run UAT for the new feature" | `uat-coordination` | Scenarios from PM/PO; QA facilitates |
| "Generate test data" | `test-data-management-synthetic` | Faker default; Mockaroo for schema |
| "Triage these 20 open bugs" | `defect-triage-severity-priority` | S1-S4 × P0-P3 matrix + SLA |
| "Test on Safari and IE11" | `cross-browser-browserstack-saucelabs-lambdatest` | Playwright WebKit free; cloud for IE11 |
| "Set up mobile E2E" | `mobile-testing-real-devices-emulators` | Maestro greenfield; Detox if RN |
| "Catch visual regressions" | `visual-regression-percy-chromatic-applitools` | Playwright native free; SaaS when needed |
| "Audit our test pyramid ratio" | `test-pyramid-governance` | Trophy default for AI-first; Pyramid for handwritten |
| "Tests are flaky" | `flaky-test-quarantine-root-cause` | Detect → quarantine → 2-week deadline |
| "Add tests to CI" | `ci-cd-test-integration-parallelization` | GH Actions matrix + sharding |
| "Set up test reporting" | `test-reporting-dashboards` | Allure / ReportPortal / Playwright HTML |
| "Is this release ready to ship?" | `release-readiness-checklists` | Binary gates; go/no-go memo |
| "Add smoke tests" | `regression-suite-curation-smoke-critical` | 3-10 critical scenarios, < 5 min |
| "Verify test quality" | `mutation-testing-stryker-mutmut` | Mutation score > coverage % |
| "How do we shift quality left" | `qa-dev-shift-left` | 3-amigo + TDD + retro KPIs |
| "Show me our quality KPIs" | `quality-kpis-escape-rate-mttr` | Escape rate + MTTR + flakiness |
| "Help me explore this new feature manually" | `exploratory-testing-charters-session-based` | SBTM charter + session sheet |
| "Write tests in Gherkin" | `test-case-authoring-bdd-gherkin` | Declarative steps; Background; Outline |

---

## Brief / Output templates

### Bug verification comment template

```markdown
**Bug verified — closed.**

Reproduced: <yes/no, steps if no>
Fix verified on: <PR-link, commit-sha>
Evidence: <screenshot / video / Loom>
Regression test added: <test-file-path, line-range>
Test would have caught it: <yes — `test_X_scenario_outcome` in `tests/regression/`>

If escape (found in prod): post-mortem note → next sprint retro.
```

### Release-readiness memo template

```markdown
# Release Readiness — <version> — <date>

**Verdict:** GO / GO-WITH-MITIGATION / HOLD

## Gates
- [x] Smoke green (link to last run)
- [x] Critical-path green
- [x] Accessibility — 0 WCAG 2.2 AA violations on changed pages
- [x] Performance — p99 within budget (link to k6 dashboard)
- [x] Security — 0 ZAP high; 0 critical CVEs in deps
- [x] Contract — `can-i-deploy` green for all consumers
- [x] Mutation score — > 60% on changed files
- [x] Open defects — 0 P0; 0 P1 without waiver
- [x] Canary 24h clean
- [x] Rollback plan documented

## Mitigations (if GO-WITH-MITIGATION)
- <risk> — feature flag `<name>` default-off; rollout 10% / 50% / 100% over 3 days.

## Holds (if HOLD)
- <gate name> — <what's red> — <owner> — <ETA to green>

Signed: qa-engineer · <date>
```

### Weekly KPI digest template

```markdown
# QA Weekly — Sprint <NN> — <date>

**Escape rate:** <X>% (target < 5%) — <trend ▲▼>
**MTTR P0:** <Xh> (target < 24h) — <trend>
**MTTR P1:** <Xd> (target < 7d) — <trend>
**Flakiness:** <X>% of CI runs (target < 2%) — <trend>
**Coverage:** line <X>% · branch <X>% · mutation <X>%
**Suite duration:** smoke <Xs> · critical <Xm> · extended <Xh>
**DORA change-failure rate:** <X>% (elite < 5%) — <trend>

**Top 3 quality risks this week:**
1. <risk + owner + ETA>
2. ...
3. ...

**Quarantined tests:** <N> (open ticket count); fix-by deadlines this week: <list>
```

---

## Closing rules

Quality is everyone's job — but someone has to drive it. The trophy beats the pyramid in 2026 for AI-first codebases. UAT happens whether you plan it or not — plan it. Ship the green CI run, the SARIF report, the closed bug, and the release-readiness sign-off.
