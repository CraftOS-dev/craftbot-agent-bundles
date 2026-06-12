<!--
Source: https://testdino.com/blog/flaky-tests · https://trunk.io/flaky-tests · https://www.functionize.com/blog/the-flaky-test-problem-root-cause-and-how-ai-solves-it
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Flaky Test Management — Detect → Quarantine → Root-Cause → 2-Week Fix

The 2026 SOTA for flake: **detect** via repeat runs / CI history;
**quarantine** to a non-blocking suite; **root-cause** with the 70% timing /
28% DOM / 2% network taxonomy; **heal or remove** in 2 weeks (Microsoft
pattern). AI-assisted: FlakyGuard (47.6% auto-fixes), Trunk.io flaky detection,
Mergify auto-retry orchestration.

## When to use

- A test passes locally, fails on CI
- "Re-run the build" is becoming common
- CI green != reality green
- A suite needs flake metrics for governance
- Trigger phrases: "flaky", "flake", "intermittent", "passes locally",
  "quarantine", "rerun", "race condition", "timing-dependent"

## Setup

```bash
# pytest retries + report
uv add --dev pytest-rerunfailures pytest-randomly pytest-json-report

# Playwright retries
# Built-in: retries: 2 in config

# Trunk.io flaky test
# https://trunk.io/products/flaky-tests — SaaS

# CI flaky detector action
# https://github.com/marketplace/actions/test-flakiness-detector
```

Auth: GitHub App / Trunk.io token if using SaaS.

## Common recipes

### Recipe 1 — Detect flakes via repeat runs

```bash
# pytest — run 10x, report which tests failed sometimes
for i in {1..10}; do
  uvx pytest --json-report --json-report-file=run-$i.json -p no:randomly || true
done

# Aggregate
python scripts/find_flakes.py run-*.json
```

```python
# scripts/find_flakes.py
import json, sys, collections
runs = [json.load(open(p)) for p in sys.argv[1:]]
results = collections.defaultdict(list)
for run in runs:
    for t in run["tests"]:
        results[t["nodeid"]].append(t["outcome"])
for nodeid, outcomes in results.items():
    fails = sum(1 for o in outcomes if o == "failed")
    if 0 < fails < len(outcomes):
        print(f"FLAKY ({fails}/{len(outcomes)}): {nodeid}")
```

### Recipe 2 — Playwright built-in flake detection

```ts
// playwright.config.ts
export default defineConfig({
  retries: process.env.CI ? 2 : 0,
  reporter: [
    ["list"],
    ["json", { outputFile: "playwright-report.json" }],
    ["github"],
  ],
});
```

After CI run:
```bash
# Tests retried but ultimately passed appear as `flaky` in the JSON
jq '.suites[].suites[].specs[] | select(.tests[].results[].status == "flaky")' \
  playwright-report.json
```

### Recipe 3 — Quarantine via marker (pytest)

```python
# tests/payments/test_double_submit.py
@pytest.mark.flaky(reruns=2, reruns_delay=1)
@pytest.mark.quarantine  # excluded from blocking gate
def test_known_flaky_double_submit():
    ...
```

```ini
# pyproject.toml
[tool.pytest.ini_options]
markers = [
  "quarantine: tracked flakes; not in PR gate",
]
addopts = "-m 'not quarantine' --strict-markers"
```

```bash
uvx pytest                           # excludes quarantine
uvx pytest -m quarantine             # only quarantine — track separately
```

### Recipe 4 — Quarantine via Playwright project

```ts
// playwright.config.ts
projects: [
  { name: "main",       testIgnore: /.*\.quarantine\.spec\.ts/ },
  { name: "quarantine", testMatch: /.*\.quarantine\.spec\.ts/, retries: 3 },
],
```

```bash
npx playwright test --project=main         # PR gate
npx playwright test --project=quarantine   # tracked separately
```

### Recipe 5 — Root-cause taxonomy

```markdown
| Category | % | Common cause | Fix |
|---|---|---|---|
| Timing | ~70% | Race / waitForTimeout / animation | Web-first assertions; `expect(...).toPass()`; explicit waits |
| DOM / selector | ~28% | Brittle CSS / nth-child | `getByRole` / `getByTestId`; avoid index selectors |
| Network / data | ~2% | Real API rate limit / shared DB | `msw` / `respx`; testcontainers; per-test cleanup |
```

### Recipe 6 — Fix timing flake (anti-pattern → fix)

```ts
// BAD
await page.click("button.submit");
await page.waitForTimeout(2000);
expect(await page.locator(".message").textContent()).toBe("Success");

// GOOD
await page.getByRole("button", { name: "Submit" }).click();
await expect(page.locator(".message")).toHaveText("Success");
```

### Recipe 7 — Fix DOM-selector flake

```ts
// BAD — index selector breaks on reorder
await page.locator("ul > li:nth-child(3) > button").click();

// GOOD — role + name
await page.getByRole("listitem").filter({ hasText: "Premium" })
  .getByRole("button", { name: "Subscribe" }).click();
```

### Recipe 8 — Fix data flake (shared state)

```python
# BAD — depends on test order
def test_create(db):
    db.users.insert({"email": "alice@example.com"})

def test_login(db):  # assumes alice exists
    assert db.users.find_one(email="alice@example.com")

# GOOD — fixture
@pytest.fixture
def alice(db):
    u = db.users.insert({"email": "alice@example.com"})
    yield u
    db.users.delete(u.id)

def test_login(client, alice):
    assert client.post("/login", json=alice).status_code == 200
```

### Recipe 9 — Quarantine ticket template

```markdown
# Flaky test ticket

**Test:** `tests/payments/test_double_submit.py::test_double_submit`
**Quarantined:** 2026-06-09
**Owner:** @alice
**Fix-by:** 2026-06-23  (2-week SLA)
**Category:** Timing
**Suspected cause:** Race between Stripe webhook and DB write
**Repro rate:** 4/10 on CI; 0/10 local

## Triage notes
- [x] Repro'd locally with `--repeat-each=10`
- [ ] Traced with Playwright trace viewer
- [ ] Patched with retry assertion
- [ ] Removed from quarantine

## Decision after deadline
- [ ] FIX (PR link)
- [ ] DELETE (test no longer reflects shipped behavior)
```

### Recipe 10 — pytest-randomly to surface order-dependent flakes

```bash
uv add --dev pytest-randomly
uvx pytest -p randomly --randomly-seed=42
```

Random order surfaces order-dependent tests immediately.

### Recipe 11 — CI flaky detection workflow

```yaml
# .github/workflows/flaky-detector.yml
on: { schedule: [{ cron: '0 3 * * *' }] }   # nightly
jobs:
  detect:
    runs-on: ubuntu-latest
    strategy: { matrix: { run: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] } }
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npx playwright install --with-deps
      - run: npx playwright test --reporter=json --output=report-${{ matrix.run }}.json
      - uses: actions/upload-artifact@v4
        with: { name: nightly-flake-runs, path: report-*.json }

  aggregate:
    needs: detect
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with: { name: nightly-flake-runs }
      - run: node scripts/aggregate-flakes.js report-*.json > flakes.md
      - uses: actions/upload-artifact@v4
        with: { name: nightly-flake-report, path: flakes.md }
```

### Recipe 12 — Auto-create quarantine issues

```yaml
# .github/workflows/auto-quarantine.yml
- name: Open issue for new flake
  uses: actions/github-script@v7
  with:
    script: |
      const flakes = require('./flakes.json');
      for (const t of flakes) {
        await github.rest.issues.create({
          ...context.repo,
          title: `[flake] ${t.name} (${t.failureRate}%)`,
          body: `## Failure rate: ${t.failureRate}%\n\nQuarantine in 2 weeks if not fixed.`,
          labels: ['flake', 'quarantine'],
        });
      }
```

### Recipe 13 — Trunk.io flaky-tests SaaS

```bash
# Install GitHub App from Trunk.io
# Uploads test results from CI; Trunk identifies flakes via ML
# Auto-quarantines, opens issues, suggests fixes
```

Free tier covers 1500 monthly runs.

### Recipe 14 — 2-week SLA enforcement

```python
# scripts/enforce_quarantine_sla.py
import sys, datetime, github3
gh = github3.login(token=os.environ["GITHUB_TOKEN"])
repo = gh.repository("org", "repo")
threshold = datetime.datetime.utcnow() - datetime.timedelta(days=14)

for issue in repo.issues(labels="flake,quarantine", state="open"):
    if issue.created_at < threshold:
        print(f"OVERDUE: #{issue.number} — {issue.title}")
        sys.exit(1)
```

After deadline: PR removes the test outright; quarantine without fix = delete.

## Examples

### Example 1: Triage a single new flake

**Goal:** Test "checkout submit" failed 1/5 PR runs this week.

1. Local repro: `npx playwright test --repeat-each=10 checkout.spec.ts`.
2. Trace failed run: `npx playwright show-trace test-results/.../trace.zip`.
3. Identify: assertion on `text=Success` before request response.
4. Fix: `await expect(page.getByText("Success")).toBeVisible()` (Recipe 6).
5. Verify: 10 runs green locally; merge fix.

### Example 2: Backlog of 15 quarantined tests

**Goal:** Bulk action on a sprawling quarantine backlog.

1. Audit: list all quarantined tests + age (Recipe 14).
2. > 14 days: delete (write PR removing test + closing issue).
3. < 14 days: triage per Recipe 5; assign owner.
4. Mid-sprint: enforce SLA via CI step that fails on overdue.
5. Retrospective: which areas have highest flake rate? Architectural fix
   beats whack-a-mole.

## Edge cases / gotchas

- **Rerun != fix** — `retries: 2` masks symptoms. Use only for tests with a
  known root cause being addressed.
- **"It's flaky" without evidence** — require 3 documented failures with
  trace before quarantining.
- **Quarantine forever** — must have a 14-day deadline. After, delete.
- **Hidden coupling** — order-dependent tests pass in `test_a, test_b, test_c`
  but fail in random order. Run with `pytest-randomly` weekly.
- **Auto-retry in CI without flake tracking** — CI looks green; reality is
  bad. Log retries; alert on retry rate > 5%.
- **Network flake on real APIs** — mock with `msw` / `respx` / `WireMock`;
  testcontainers for DB/Redis/Kafka.
- **Browser version drift** — Chrome updates change rendering / timing.
  Pin Playwright `@playwright/test` version + browser channel.
- **Headless vs headed** — some flakes only manifest headless. Default CI
  is headless; test both locally.
- **Test author bias** — author claims "not flaky on my machine". Repro on
  CI-equivalent Docker.
- **Quarantine pile-up** — > 20 quarantined tests = pull on architecture.
  Likely a global flaky source (db cleanup, time, network).
- **Flaky source code** — sometimes the SUT is non-deterministic. Test is
  correct; code is wrong. Fix the code.

## Sources

- [TestDino flaky tests guide](https://testdino.com/blog/flaky-tests)
- [Trunk.io flaky test detection](https://trunk.io/flaky-tests)
- [Microsoft Engineering blog — fighting flake](https://devblogs.microsoft.com/devops/)
- [Google Testing — Flaky Tests at Google](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html)
- [pytest-rerunfailures](https://github.com/pytest-dev/pytest-rerunfailures)
- [pytest-randomly](https://github.com/pytest-dev/pytest-randomly)
- [Playwright test retries](https://playwright.dev/docs/test-retries)
- [Mergify auto-retry](https://docs.mergify.com/)
- [FlakyGuard study](https://arxiv.org/abs/2308.07876)
- [Functionize — flaky test problem](https://www.functionize.com/blog/the-flaky-test-problem-root-cause-and-how-ai-solves-it)
