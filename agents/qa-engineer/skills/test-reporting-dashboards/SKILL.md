<!--
Source: https://allurereport.org/ · https://reportportal.io/ · https://playwright.dev/docs/test-reporters · https://docs.pytest.org/en/stable/how-to/output.html
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Test Reporting + Dashboards — Allure + ReportPortal + Playwright HTML

The 2026 reporting stack: **Allure Report** (rich HTML, Jira + Trello + Slack
integration, multi-language) for canonical dashboards; **ReportPortal**
(OSS, AI-driven defect categorization) for unified cross-CI rollup;
**Playwright HTML reporter** + trace viewer for per-run drill-down;
**Grafana** for k6 / perf trends. Hosted on GitHub Pages, S3, or self-host.

## When to use

- Stakeholders want a "what's the test status?" link they can bookmark
- Test failures need historical context (was this test always flaky?)
- Multiple test frameworks need unified rollup
- Release readiness needs evidence dashboard
- Trigger phrases: "test report", "dashboard", "Allure", "ReportPortal",
  "Playwright report", "JUnit XML", "trace viewer", "publish report"

## Setup

```bash
# Allure
brew install allure
# Or
npm i -g allure-commandline
uvx --from allure-pytest pytest --alluredir=allure-results
npm i -D allure-playwright

# ReportPortal — Docker
docker compose -f https://github.com/reportportal/reportportal/raw/master/docker-compose.yml up -d

# Playwright HTML — built-in
# pytest-html
uv add --dev pytest-html
```

Auth: ReportPortal needs token (`RP_TOKEN`); Allure self-hosted no auth.

## Common recipes

### Recipe 1 — Playwright HTML reporter + trace viewer

```ts
// playwright.config.ts
export default defineConfig({
  reporter: [
    ["list"],
    ["html", { open: "never", outputFolder: "playwright-report" }],
    ["json", { outputFile: "results.json" }],
    ["junit", { outputFile: "junit.xml" }],
    ["github"],
  ],
  use: {
    trace: "on-first-retry",   // capture trace when retry kicks in
    screenshot: "only-on-failure",
    video: "retain-on-failure",
  },
});
```

```bash
npx playwright test
npx playwright show-report   # browser opens HTML report
npx playwright show-trace test-results/.../trace.zip
```

### Recipe 2 — Allure for pytest

```bash
uvx pytest --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
```

```python
# Decorate tests with Allure metadata
import allure

@allure.epic("Auth")
@allure.feature("Login")
@allure.story("Happy path")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("smoke", "regression")
def test_login_happy(client, alice):
    with allure.step("POST /login"):
        r = client.post("/login", json=alice)
    with allure.step("Assert 200"):
        assert r.status_code == 200
    allure.attach(r.text, name="response", attachment_type=allure.attachment_type.JSON)
```

### Recipe 3 — Allure for Playwright

```ts
// playwright.config.ts
reporter: [["allure-playwright", { detail: true, outputFolder: "allure-results" }]],
```

```ts
import { test, expect } from "@playwright/test";
import { allure } from "allure-playwright";

test("login happy path", async ({ page }) => {
  allure.epic("Auth");
  allure.feature("Login");
  allure.severity("critical");
  allure.tag("smoke");

  await allure.step("navigate to /login", async () => await page.goto("/login"));
  await allure.step("fill credentials", async () => {
    await page.getByLabel("Email").fill("alice@example.com");
    await page.getByLabel("Password").fill("Test1234!");
  });
  await allure.step("submit", async () => await page.getByRole("button", { name: "Sign in" }).click());
  await expect(page).toHaveURL("/dashboard");
});
```

### Recipe 4 — Publish Allure to GitHub Pages

```yaml
# .github/workflows/allure.yml
on: { workflow_run: { workflows: ["E2E"], types: [completed] } }

jobs:
  publish:
    runs-on: ubuntu-latest
    if: github.event.workflow_run.conclusion == 'success'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: allure-results
          github-token: ${{ secrets.GITHUB_TOKEN }}
          run-id: ${{ github.event.workflow_run.id }}
      - uses: actions/checkout@v4
        with: { ref: gh-pages, path: gh-pages }
      - uses: simple-elf/allure-report-action@master
        with:
          allure_results: allure-results
          allure_history: gh-pages/allure-history
          gh_pages: gh-pages
      - uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_branch: gh-pages
          publish_dir: gh-pages/allure-history
```

Dashboard at: `https://<org>.github.io/<repo>/`.

### Recipe 5 — ReportPortal Docker Compose

```yaml
# docker-compose.rp.yml
services:
  reportportal:
    image: reportportal/service-api:5.13.0
    environment:
      RP_DB_HOST: postgres
      RP_DB_USER: rpuser
      RP_DB_PASS: rppass
    ports: ["8080:8080"]
  ui:
    image: reportportal/service-ui:5.13.0
    ports: ["8081:8080"]
  postgres:
    image: postgres:16
```

```bash
docker compose -f docker-compose.rp.yml up -d
# Open http://localhost:8081  default admin/erebus
```

### Recipe 6 — pytest → ReportPortal

```bash
uv add --dev pytest-reportportal
```

```ini
# pytest.ini
[pytest]
rp_uuid = $RP_TOKEN
rp_endpoint = https://reportportal.example.com
rp_project = my-project
rp_launch = sprint-42
```

```bash
uvx pytest --reportportal
```

### Recipe 7 — Slack notification on failure

```yaml
- name: Slack on failure
  if: failure()
  uses: slackapi/slack-github-action@v1.27.0
  with:
    payload: |
      {
        "text": ":red_circle: Test failure in <${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|${{ github.workflow }}>",
        "blocks": [
          {"type": "section", "text": {"type": "mrkdwn", "text": "*PR:* <${{ github.event.pull_request.html_url }}|#${{ github.event.pull_request.number }}>\n*Branch:* `${{ github.head_ref }}`"}}
        ]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Recipe 8 — k6 + Grafana

```bash
# Output k6 to InfluxDB / Prometheus
k6 run --out experimental-prometheus-rw=http://prometheus:9090/api/v1/write load.js

# Or Grafana Cloud k6
k6 cloud run load.js
```

Grafana dashboard import ID 19665 (k6 official); shows p50/p95/p99 trends.

### Recipe 9 — JUnit XML for GitHub PR comments

```yaml
- uses: dorny/test-reporter@v1
  if: always()
  with:
    name: Playwright Tests
    path: junit.xml
    reporter: java-junit
```

PR gets inline comment summarizing pass/fail per test.

### Recipe 10 — Combined Allure across frameworks

```bash
# pytest results
uvx pytest --alluredir=allure-results-pytest

# Playwright results
npx playwright test    # writes to allure-results-playwright

# Merge
mkdir -p allure-results-merged
cp -r allure-results-pytest/* allure-results-merged/
cp -r allure-results-playwright/* allure-results-merged/
allure generate allure-results-merged -o allure-report --clean
```

Single dashboard for backend + frontend tests.

### Recipe 11 — Allure trend / history

```bash
# To get trend chart, retain history between runs
mkdir -p allure-results
cp -r previous-report/history allure-results/history    # if exists
allure generate allure-results -o allure-report --clean
```

The action `simple-elf/allure-report-action` (Recipe 4) does this automatically.

### Recipe 12 — Embedded artifacts in report

```python
# pytest
import allure
allure.attach.file("screenshot.png", name="screenshot", attachment_type=allure.attachment_type.PNG)
allure.attach(json.dumps(api_response), name="api response", attachment_type=allure.attachment_type.JSON)
```

```ts
// Playwright auto-attaches screenshots/videos/traces on failure
test("foo", async ({ page }, testInfo) => {
  await testInfo.attach("login-state.json", { body: JSON.stringify(state), contentType: "application/json" });
});
```

### Recipe 13 — Reporter selection rubric

```markdown
| Need | Tool |
|---|---|
| Default per-run HTML, traces | Playwright HTML / pytest-html |
| Multi-framework rollup, rich metadata, history | Allure |
| AI-categorization, OSS server, cross-CI | ReportPortal |
| Perf trend | Grafana + k6 / Prometheus |
| PR inline summary | JUnit + dorny/test-reporter |
| Stakeholder dashboard | Allure on GitHub Pages / S3 |
```

## Examples

### Example 1: PR check with HTML report

**Goal:** Reviewer clicks one link, sees what failed.

1. Playwright HTML reporter (Recipe 1) generates per-run.
2. JUnit + dorny/test-reporter (Recipe 9) → PR inline comment.
3. Allure published per main merge (Recipe 4) → permanent dashboard.
4. Slack notification on PR failure (Recipe 7).

### Example 2: Multi-framework dashboard for management

**Goal:** Manager wants one weekly view.

1. Allure for pytest (Recipe 2) + Playwright (Recipe 3) + Cypress (allure-cypress).
2. Merge results (Recipe 10).
3. Publish to GitHub Pages weekly (Recipe 4 + workflow_dispatch).
4. Allure email digest plugin → manager weekly inbox.
5. ReportPortal (Recipe 5) for AI-categorized common failure clusters.

## Edge cases / gotchas

- **HTML reports in Git** — bloat. Publish to GitHub Pages / S3, don't
  commit.
- **Allure JS adapter version mismatch** — `allure-playwright` must align
  with `allure-commandline`. Pin both.
- **Allure history grows unbounded** — prune to last N runs in CI.
- **ReportPortal self-host complexity** — needs Postgres + Elasticsearch +
  RabbitMQ. Use SaaS or hosted offering for small teams.
- **Slack failure noise** — only alert on main / smoke failures; PR
  failures clutter.
- **Trace size** — 5-50MB per test. Use `trace: 'on-first-retry'`, not `on`.
- **Auth-protected dashboards** — GitHub Pages public; protect via Cloudflare
  Access or move to S3+CloudFront with auth.
- **Multi-shard reports duplicated** — merge with `playwright merge-reports`
  or single Allure dir before generate.
- **Allure `severity` mismatch with QA severity** — Allure uses
  blocker/critical/normal/minor/trivial. Map to your S1-S4 in docs.
- **JUnit XML truncation in GitHub Actions** — line cap; very large suites
  silently truncate. Upload artifact instead.
- **Screenshot attachments in Allure** — automatic for Playwright failure;
  for pytest add hook in `conftest.py`.
- **Trends only show after 2+ runs** — first run is baseline.

## Sources

- [Allure Report](https://allurereport.org/)
- [Allure pytest](https://allurereport.org/docs/pytest/)
- [allure-playwright](https://allurereport.org/docs/playwright/)
- [ReportPortal](https://reportportal.io/)
- [ReportPortal Docker](https://github.com/reportportal/reportportal)
- [Playwright reporters](https://playwright.dev/docs/test-reporters)
- [Playwright trace viewer](https://playwright.dev/docs/trace-viewer)
- [pytest-html](https://pytest-html.readthedocs.io/)
- [pytest-reportportal](https://github.com/reportportal/agent-python-pytest)
- [dorny/test-reporter](https://github.com/dorny/test-reporter)
- [simple-elf/allure-report-action](https://github.com/marketplace/actions/allure-report-action)
- [Grafana k6 dashboard 19665](https://grafana.com/grafana/dashboards/19665/)
