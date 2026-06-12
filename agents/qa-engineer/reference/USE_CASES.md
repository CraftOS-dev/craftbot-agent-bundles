# QA / Test Engineer — Use Cases

**Tier:** specialized · **Category:** engineering
**Core job:** Own the test strategy, suite, infrastructure, and cross-cutting quality concerns layer (accessibility, performance, security, contracts, visual, mobile, flaky-test discipline, release-readiness gates, quality KPIs) for the 2026 stack.

Ships with the SOTA QA stack (Playwright + axe-core + k6 + Bruno + Pact + OWASP ZAP + Stryker/mutmut + Allure) — executes end-to-end, not just directs. Defers app-code unit tests to `senior-python-engineer`, component tests to `frontend-engineer`, CI runner infra to `devops-engineer`, acceptance criteria authoring to `product-manager`, compliance-level security audits to `compliance-agent`.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes today via SOTA tools, and where the honest gaps are.

---

## What this agent is supposed to do

### Test strategy and planning
- Author risk-based test plans (ISO 29119-3 + Heuristic Test Strategy Model)
- Govern test pyramid / trophy ratio per codebase context (AI-first vs handwritten)
- Curate regression suites in three tiers (smoke / critical-path / extended)
- Pick automation layer per use case (unit vs integration vs E2E vs contract vs manual)
- Define entry / exit criteria + pass/fail gates

### Test authoring
- Write Gherkin BDD scenarios (Cucumber.js / pytest-bdd / Playwright-bdd)
- Write Playwright E2E tests (Chromium / Firefox / WebKit)
- Write integration tests against testcontainers backends (Postgres / Redis / Kafka)
- Write API tests in Bruno / Postman / Newman collections
- Write k6 / Locust / Artillery load test scripts
- Write Pact consumer-driven contract tests
- Write OWASP ZAP automation scripts (baseline + full scan)
- Write mobile E2E flows (Maestro / Detox / Appium + WebdriverIO)

### Manual / exploratory testing
- Run session-based exploratory testing (Bach/Bolton SBTM charters, 60-90 min)
- Coordinate UAT scenarios authored by PM/PO; capture sign-off evidence
- Manual accessibility passes (NVDA / JAWS / VoiceOver / keyboard nav / zoom 200%)
- Bug bashes and regression sweeps

### Cross-cutting quality concerns
- **Accessibility** — axe-core + pa11y + Lighthouse CI gates for WCAG 2.2 AA; manual screen-reader passes
- **Performance** — k6 / Locust / Artillery; declarative thresholds; Grafana dashboards
- **Security** — OWASP ZAP DAST + Snyk/pip-audit/osv-scanner dep CVE + gitleaks/trufflehog secrets
- **Contract** — Pact + Pact Broker + `can-i-deploy` release gate; bi-directional with OpenAPI
- **Visual regression** — Playwright native `toHaveScreenshot` free; Applitools / Chromatic / Percy when paid
- **Cross-browser** — Playwright Chromium/Firefox/WebKit free; BrowserStack / Sauce Labs / TestMu AI for the long tail
- **Mobile** — Maestro greenfield; Detox React Native; Appium + WebdriverIO cross-platform

### Test infrastructure
- Wire tests into CI (GitHub Actions / CircleCI / GitLab CI) — matrix + sharding
- Manage ephemeral test environments (Docker Compose / Testcontainers / K8s namespace-per-PR / Neon DB branching)
- Generate synthetic test data (Faker / Mockaroo / Tonic.ai) — GDPR-safe by construction
- Set up test reporting dashboards (Allure / ReportPortal / Playwright HTML / Grafana k6)

### Operational quality discipline
- Triage defects (Severity S1-S4 × Priority P0-P3 matrix; SLA per quadrant)
- Verify bug fixes; write the regression test that would have caught it
- Manage flaky tests (detect → quarantine → root-cause → 2-week fix-or-remove)
- Run mutation testing (Stryker / mutmut / Pitest) — verify the suite catches bugs
- Enforce code quality gates (SonarQube / CodeClimate; PR status checks)
- Make release-readiness go/no-go calls; sign off with evidence
- Coordinate QA-Dev shift-left (3-amigo / story refinement / TDD-BDD in PR)
- Track + report quality KPIs (escape rate, MTTR, flakiness, DORA change-failure rate)

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case from the section above appears here as a row.

| Use case | SOTA mechanism | Path |
|---|---|---|
| Test plan authoring | ISO 29119-3 + HTSM risk model | `filesystem` + bundled `test-plan-authoring-pmbok-iso` |
| Test pyramid / trophy governance | Trophy ratio (AI-first) / Pyramid (handwritten) | `filesystem` + bundled `test-pyramid-governance` |
| Regression suite curation | Playwright projects + pytest markers — smoke/critical/extended | `cli-anything` + bundled `regression-suite-curation-smoke-critical` |
| BDD test authoring | Cucumber.js / pytest-bdd / Playwright-bdd | `cli-anything` + bundled `test-case-authoring-bdd-gherkin` |
| E2E browser tests | Playwright (Chromium / Firefox / WebKit native) | `playwright-mcp` + bundled `regression-suite-curation-smoke-critical` |
| Integration tests | testcontainers (real Postgres / Redis / Kafka) | `cli-anything` + parent's `testcontainers-integration-testing` skill |
| API testing | Bruno (Git-native) + Postman + Newman | `cli-anything` + bundled `api-testing-postman-bruno-newman` |
| Performance / load | k6 (JS default) + Locust (Py) + Artillery (Node) | `cli-anything` + bundled `performance-testing-k6-locust-artillery` |
| Contract testing | Pact + Pact Broker (OSS) / PactFlow + `can-i-deploy` | `cli-anything` + bundled `contract-testing-pact` |
| Security / DAST | OWASP ZAP (CI default) + Burp Pro (manual) + SARIF | `cli-anything` + `github` (SARIF upload) + bundled `security-testing-owasp-zap-burp` |
| Dependency CVE | Snyk / pip-audit / osv-scanner | `cli-anything` + bundled `security-testing-owasp-zap-burp` |
| Mobile E2E | Maestro (greenfield) / Detox (RN) / Appium + WebdriverIO | `cli-anything` + bundled `mobile-testing-real-devices-emulators` |
| Cross-browser coverage | Playwright native (free) + BrowserStack / Sauce / TestMu (cloud) | `playwright-mcp` + bundled `cross-browser-browserstack-saucelabs-lambdatest` |
| Visual regression | Playwright `toHaveScreenshot` (free) + Applitools / Chromatic / Percy (paid) | `cli-anything` + bundled `visual-regression-percy-chromatic-applitools` |
| Accessibility (WCAG 2.2 AA) | axe-core + pa11y + Lighthouse + manual NVDA / VoiceOver | `cli-anything` + `playwright-mcp` + bundled `accessibility-testing-wcag-22-aa-axe` |
| Exploratory testing | Bach/Bolton SBTM charters; mind-maps in draw.io / Excalidraw | `filesystem` + bundled `exploratory-testing-charters-session-based` |
| UAT coordination | Acceptance-criteria scenarios + Loom + Notion sign-off | `notion-mcp` + bundled `uat-coordination` |
| Test data management | Faker / Mockaroo / Tonic.ai — GDPR-safe synthetic | `cli-anything` + bundled `test-data-management-synthetic` |
| Test environments | Docker Compose / Testcontainers / K8s namespace-per-PR / Neon branching | `cli-anything` + `kubernetes-mcp` + `postgresql-mcp` |
| Defect triage | Severity × Priority matrix + SLA per quadrant | `jira-mcp` / `linear-mcp` + bundled `defect-triage-severity-priority` |
| Bug verification + closure | Reproduce + verify + name-the-test (DORA pattern) | `cli-anything` + `jira-mcp` / `linear-mcp` + `sentry-mcp` |
| Flaky test management | Detect / quarantine / root-cause / 2-week deadline | `cli-anything` + `github-api` (quarantine PRs) + bundled `flaky-test-quarantine-root-cause` |
| Mutation testing | Stryker (JS/.NET) + mutmut (Py) + Pitest (JVM) | `cli-anything` + bundled `mutation-testing-stryker-mutmut` |
| Code quality gates | SonarQube / SonarCloud + CodeClimate PR status checks | `cli-anything` + `github-api` + bundled `quality-kpis-escape-rate-mttr` |
| CI/CD test integration | GH Actions matrix + Playwright sharding + pytest-xdist | `github-api` + `cli-anything` + bundled `ci-cd-test-integration-parallelization` |
| Test reporting / dashboards | Allure + ReportPortal + Playwright HTML + Grafana k6 | `cli-anything` + bundled `test-reporting-dashboards` |
| Smoke test automation | Playwright `--project=smoke` / pytest `-m smoke`, < 5 min | `cli-anything` + `slack-mcp` (failure alerts) |
| Release readiness call | DORA binary gates + GH branch protection | `github-api` + `filesystem` + bundled `release-readiness-checklists` |
| QA-Dev shift-left | 3-amigo + TDD/BDD in PR + retro KPI review | `notion-mcp` + `jira-mcp` + bundled `qa-dev-shift-left` |
| Quality KPIs | Escape rate < 5% + MTTR P0 < 24h + flakiness < 2% + DORA | `cli-anything` + `posthog-mcp` + `slack-mcp` + bundled `quality-kpis-escape-rate-mttr` |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Contract testing — hosted Pact Broker | ⚠ | PactFlow is paid for org-scale; OSS Pact Broker (Docker image) is free and ships immediately. Agent defaults to OSS until recipient sets `PACTFLOW_*` env vars. |
| Cross-browser cloud grid | ⚠ | BrowserStack ($50-75k/yr at 100 parallel) / Sauce Labs ($80-120k/yr) / TestMu AI cheaper. Free fallback: local Playwright Chromium + Firefox + WebKit covers 80%+ of regressions. Agent uses cloud only when `BROWSERSTACK_KEY` / `SAUCE_USERNAME` set. |
| Code quality cloud gates | ⚠ | SonarCloud free for OSS, paid for private repos; SonarQube Community self-host free. Agent defaults to self-host or OSS path until recipient provides SonarCloud token. |
| Real-device mobile cloud | ⚠ | BrowserStack App Live / Sauce Real Device paywalled (recipient owns key). Free fallback: iOS Simulator / Android Emulator + Maestro local. |
| Visual regression Visual AI | ⚠ | Applitools / Chromatic / Percy paywalled. Free fallback: Playwright native `toHaveScreenshot` baseline-in-Git. |
| AI test maintenance SaaS | ⚠ | Mabl / Testim / Functionize paywalled. Free fallback: well-curated Playwright suite + `flaky-test-quarantine-root-cause` discipline + pytest-rerunfailures. |
| Compliance audit (SOC 2, ISO 27001, PCI-DSS evidence) | ✗ | Out of scope — defer to `compliance-agent`. QA does DAST + SAST + dep scanning; compliance owns the audit trail. |

**Verdict (June 2026): ~95% fulfillment.** Every QA workflow has a named SOTA tool and an exact execution mechanism. The ⚠ rows are paywalled-on-recipient SaaS — the agent ships with the OSS / free fallback that runs immediately without paying. The single ✗ row (compliance audits) is correctly out of scope and hands off to `compliance-agent`.

---

## When to use this agent

- "Write a test plan for our checkout redesign"
- "Set up Playwright E2E tests for our app — Chrome, Firefox, Safari"
- "Add accessibility testing to our CI — WCAG 2.2 AA"
- "Load-test the orders API to find the breaking point"
- "Set up contract testing between our web app and the orders service"
- "Run a security scan against staging and upload the SARIF to GitHub"
- "Why are these 12 tests flaky? Quarantine them and find the root cause"
- "Audit our test pyramid — are we over-investing in E2E?"
- "Generate synthetic test data for our user fixtures"
- "Is this release ready to ship? Run the checklist"
- "Triage these 30 bugs — which are P0 / P1?"
- "Write a Stryker mutation test config for our JS codebase"
- "Set up Allure reporting and publish to GitHub Pages"
- "How do we cut our CI test time from 45 min to 10 min?"

---

## When NOT to use this agent

- App-code unit tests written in the same edit as the feature → `senior-python-engineer` (parent) or `frontend-engineer` (TS/React). QA owns the suite-level governance; per-feature unit tests live with the feature code.
- Component-level testing architecture (Storybook + React Testing Library + Chromatic visual) → `frontend-engineer`.
- CI runner / cluster infra (self-hosted GH Actions runners, K8s test cluster provisioning, build cache strategy) → `devops-engineer`. QA owns the test stage definitions inside CI; DevOps owns the runner.
- Acceptance criteria authoring + Definition of Done → `product-manager`. QA writes tests against the criteria; PM writes the criteria.
- Compliance-level security audits (SOC 2 evidence, ISO 27001 controls, PCI-DSS attestation) → `compliance-agent`. QA does DAST/SAST/dep-CVE in CI; compliance owns the audit trail.
- UAT facilitation with execs / customers → `product-manager` or `customer-success`. QA writes UAT scenarios and coordinates QA-side sign-off; PM owns stakeholder facilitation.
- Non-engineering tasks (marketing copy, sales decks, etc.) — out of scope; refuse politely.
