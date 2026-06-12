# qa-engineer — SOTA Use Cases (June 2026)

This document maps every documented QA / test-engineering use case to a concrete SOTA execution mechanism. Every use case has a named tool, an exact agent-level execution path, a source URL, and a confidence rating.

Defer to the parent `senior-python-engineer` agent for app-code unit tests written in the same edit as the feature; this agent owns the *test strategy*, *suite*, *infrastructure*, and *cross-cutting quality concerns* layer.

---

## 1. Test plan authoring (objectives, scope, risks, exit criteria)

- **SOTA approach:** ISO/IEC/IEEE 29119-3 test-plan template adapted with risk-based testing (Heuristic Test Strategy Model / RBT matrix) + Living-doc test plan in Markdown under `docs/test-plans/` (PMBOK-style) reviewed in PRs alongside the feature.
- **Agent execution path:** `filesystem` MCP writes `docs/test-plans/<feature>.md` + `notion-mcp` for stakeholder sign-off; bundled skill `test-plan-authoring-pmbok-iso`.
- **Source:** https://www.iso.org/standard/79428.html (29119-3); https://www.satisfice.com/download/heuristic-test-strategy-model
- **Confidence:** ✓ Fully executable

## 2. Test case authoring (BDD/Gherkin + manual + automated)

- **SOTA approach:** Gherkin scenarios in `features/*.feature` consumed by Cucumber.js / pytest-bdd / Cypress-cucumber / Playwright-bdd; Given/When/Then with declarative steps; reused in test-management tools (Qase / TestRail).
- **Agent execution path:** `cli-anything` + `npx @cucumber/cucumber` or `uvx pytest-bdd`; `filesystem` writes features + step defs; bundled skill `test-case-authoring-bdd-gherkin`.
- **Source:** https://cucumber.io/docs/bdd/ · https://pytest-bdd.readthedocs.io/
- **Confidence:** ✓ Fully executable

## 3. Exploratory testing (session-based, charters, time-boxed)

- **SOTA approach:** Session-Based Test Management (Bach/Bolton) — 60-90 min charters; notes captured live; `xrayCharters` heuristics; modern tooling: Rapid Reporter, BugMagnet, mind-maps in Excalidraw/draw.io.
- **Agent execution path:** `filesystem` writes charter + session-sheet templates; `drawio-mcp` for risk maps; bundled skill `exploratory-testing-charters-session-based`.
- **Source:** https://www.satisfice.com/download/session-based-test-management · https://www.ministryoftesting.com/dojo/lessons/exploratory-testing
- **Confidence:** ✓ Fully executable

## 4. Regression suite curation (smoke + critical path + extended regression)

- **SOTA approach:** Three-tier regression — smoke (< 5 min, blocks deploy), critical-path (< 30 min, post-merge), extended regression (nightly). Tag tests with pytest markers / Playwright projects / Cypress tags.
- **Agent execution path:** `cli-anything` (`uvx pytest -m smoke`, `npx playwright test --project=smoke`); `filesystem` writes `pytest.ini` + `playwright.config.ts` projects; bundled skill `regression-suite-curation-smoke-critical`.
- **Source:** https://martinfowler.com/articles/practical-test-pyramid.html · https://playwright.dev/docs/test-projects
- **Confidence:** ✓ Fully executable

## 5. Manual QA workflows for new features

- **SOTA approach:** Acceptance-criteria-driven checklists tied to user-story DoD (Definition of Done); evidence captured via Loom/screen recordings + screenshots; Jira/Linear tickets updated with QA-PASS/QA-FAIL labels.
- **Agent execution path:** `filesystem` writes manual test scripts; `jira-mcp` / `linear-mcp` updates ticket status; bundled skill cross-refs `exploratory-testing-charters-session-based`.
- **Source:** https://www.scrumguides.org/scrum-guide.html · https://www.atlassian.com/agile/project-management/definition-of-done
- **Confidence:** ✓ Fully executable

## 6. Accessibility testing (WCAG 2.2 AA, screen reader, keyboard nav, color contrast)

- **SOTA approach:** axe-core (Deque, ~57% WCAG-issue detection automated) + Lighthouse a11y + pa11y for CI gates; complement with manual NVDA/JAWS/VoiceOver passes for the ~40% automation cannot catch (reading order, keyboard traps, contextual clarity). WCAG 2.2 AA the current default; WCAG 3.0 tracking.
- **Agent execution path:** `cli-anything` (`npx @axe-core/cli`, `npx pa11y-ci`, `npx lighthouse --only=accessibility`); `playwright-mcp` for `@axe-core/playwright`; bundled skill `accessibility-testing-wcag-22-aa-axe`.
- **Source:** https://www.deque.com/axe/axe-core/ · https://pa11y.org/ · https://www.w3.org/WAI/WCAG22/quickref/
- **Confidence:** ✓ Fully executable

## 7. Performance testing (k6 + Locust + Artillery for load)

- **SOTA approach:** k6 (Grafana, Go runtime, JS scripts) as the 2026 default for JS/TS teams; Locust (Python) for Python teams; Gatling for JVM. k6 has the strongest CI integration (declarative `thresholds`, fails build on breach), Grafana Cloud k6 for distributed runs.
- **Agent execution path:** `cli-anything` (`brew install k6 && k6 run script.js`, `uvx locust -f locustfile.py`); bundled skill `performance-testing-k6-locust-artillery`.
- **Source:** https://k6.io/docs/ · https://docs.locust.io/ · https://www.artillery.io/docs
- **Confidence:** ✓ Fully executable

## 8. API testing (Postman/Bruno/Newman collections)

- **SOTA approach:** Bruno (open-source, Git-native `.bru` files, free forever) is the 2026 default for new repos; Postman still dominant for enterprises with workspaces/mock servers/Newman CI; Insomnia for GraphQL-heavy. Run in CI via `bru run` / `newman run` / `inso run`.
- **Agent execution path:** `cli-anything` (`npm i -g @usebruno/cli && bru run`, `npx newman run`); `filesystem` writes collections; bundled skill `api-testing-postman-bruno-newman`.
- **Source:** https://docs.usebruno.com/ · https://learning.postman.com/docs/running-collections/using-newman-cli/running-collections-on-the-command-line/
- **Confidence:** ✓ Fully executable

## 9. Contract testing (Pact, bi-directional, can-i-deploy)

- **SOTA approach:** Consumer-driven Pact contracts + Pact Broker (PactFlow hosted or self-hosted) as source of truth + `pact-broker can-i-deploy` gate before prod; bi-directional contracts when OpenAPI spec exists.
- **Agent execution path:** `cli-anything` (`npm i @pact-foundation/pact && pact-broker publish`, `pact-broker can-i-deploy`); bundled skill `contract-testing-pact`.
- **Source:** https://docs.pact.io/ · https://pactflow.io/
- **Confidence:** ⚠ PactFlow paid for org-scale; OSS Pact Broker free fallback works immediately

## 10. Security testing (OWASP ZAP, Burp Suite, dependency scanning)

- **SOTA approach:** OWASP ZAP for CI/CD DAST (free, Apache 2.0, official GitHub Actions `zaproxy/action-baseline` + `action-full-scan`, SARIF output) — clear winner for automation; Burp Suite Pro for manual pentest engagements. Pair with dep CVE scanning (`pip-audit`, `osv-scanner`, `npm audit`, Snyk).
- **Agent execution path:** `cli-anything` (`docker run zaproxy/zap-stable zap-baseline.py -t <url>`); `github-api` MCP publishes SARIF to GitHub code scanning; bundled skill `security-testing-owasp-zap-burp`.
- **Source:** https://www.zaproxy.org/ · https://portswigger.net/burp · https://github.com/zaproxy/action-baseline
- **Confidence:** ✓ Fully executable (Burp Pro license = recipient-paywalled, ZAP free fallback)

## 11. UAT coordination

- **SOTA approach:** Acceptance-criteria-driven UAT plan in test-management tool (TestRail/Qase/Xray); Loom walkthroughs for async stakeholders; UAT scenarios written by PM/PO + reviewed by QA; sign-off captured in Notion/Confluence.
- **Agent execution path:** `notion-mcp` writes UAT scenarios + sign-off doc; `filesystem` writes per-scenario evidence; bundled skill `uat-coordination`.
- **Source:** https://www.atlassian.com/agile/project-management/user-acceptance-testing
- **Confidence:** ✓ Fully executable

## 12. Test data management (synthetic vs production-like, GDPR-safe)

- **SOTA approach:** Synthetic-first via Faker.js / Mockaroo / GenRocket / Tonic.ai — privacy-safe by construction (no PII); production-like via masked snapshots (Tonic Structural, DBmask) when realistic-distribution is required. Store fixtures in Git alongside test code.
- **Agent execution path:** `cli-anything` (`uvx --from faker faker ...`, `npm i @faker-js/faker`); `filesystem` writes fixtures; bundled skill `test-data-management-synthetic`.
- **Source:** https://faker.readthedocs.io/ · https://fakerjs.dev/ · https://mockaroo.com/ · https://www.tonic.ai/
- **Confidence:** ✓ Fully executable

## 13. Defect triage + prioritization (severity vs priority)

- **SOTA approach:** Severity (S1-S4 — engineering impact) × Priority (P0-P3 — business urgency) matrix; SLA per quadrant; weekly bug-bash + triage; auto-tagging via Jira/Linear workflows.
- **Agent execution path:** `jira-mcp` / `linear-mcp` queries + updates issues with severity/priority labels; `filesystem` writes triage notes; bundled skill `defect-triage-severity-priority`.
- **Source:** https://www.atlassian.com/agile/tutorials/bug-tracking-with-jira
- **Confidence:** ✓ Fully executable

## 14. Bug verification + closure

- **SOTA approach:** Reproduce → verify fix on the fix PR + a canary deploy → close ticket with evidence (screenshots, video) → add regression test to prevent recurrence (the "name-the-test-that-would-have-caught-it" loop). Standard for elite DORA teams.
- **Agent execution path:** `cli-anything` (`gh pr checkout <fix-pr>`, run repro steps); `jira-mcp` updates closure; `filesystem` writes regression test; bundled skill cross-refs `qa-dev-shift-left`.
- **Source:** https://dora.dev/research/ · https://martinfowler.com/articles/microservice-testing/
- **Confidence:** ✓ Fully executable

## 15. Test environment management (staging hygiene, fixtures, seed data)

- **SOTA approach:** Containerized envs (Docker Compose / Testcontainers / Kubernetes namespace-per-PR); seeded fixtures rebuilt on each run; data hygiene scripts; preview environments via Vercel / Render / Coolify; Ephemeral DBs via Neon branching.
- **Agent execution path:** `cli-anything` (`docker compose up -d`, `uvx testcontainers`, `kubectl apply -f manifests/`); `kubernetes-mcp` if cluster ops; bundled skill cross-refs `ci-cd-test-integration-parallelization`.
- **Source:** https://testcontainers.com/ · https://docs.docker.com/compose/ · https://neon.tech/docs/guides/branching-test-queries
- **Confidence:** ✓ Fully executable

## 16. Cross-browser testing strategy (BrowserStack/Sauce/LambdaTest/TestMu)

- **SOTA approach:** Playwright native cross-browser (Chromium + Firefox + WebKit) free for most coverage; cloud grids (BrowserStack 30k+ devices, Sauce Labs deeper analytics, TestMu AI cost-effective alternative with KaneAI assist) for the long-tail real devices / older OS versions.
- **Agent execution path:** `cli-anything` (`npx playwright test --project=chromium,firefox,webkit`); `playwright-mcp` orchestrates; remote grid via BrowserStack/Sauce REST API (recipient owns key); bundled skill `cross-browser-browserstack-saucelabs-lambdatest`.
- **Source:** https://playwright.dev/docs/browsers · https://www.browserstack.com/automate · https://saucelabs.com/products/automated-testing
- **Confidence:** ⚠ Cloud grids require paid keys (recipient-owned); free local Playwright cross-browser covers 80%+

## 17. Mobile testing strategy (real devices vs emulators)

- **SOTA approach:** Maestro (YAML, fastest setup, 10-15 min time-to-first-test) for greenfield; Detox for pure React Native (lowest flakiness <2% via grey-box); Appium + WebdriverIO for cross-platform/cross-language depth. BrowserStack App / Sauce Real Device Cloud for real-device coverage.
- **Agent execution path:** `cli-anything` (`maestro test flow.yaml`, `detox test`, `npx wdio run wdio.conf.js`); bundled skill `mobile-testing-real-devices-emulators`.
- **Source:** https://maestro.dev/docs · https://wix.github.io/Detox/ · https://appium.io/
- **Confidence:** ✓ Fully executable (real-device cloud paywalled, emulator path free)

## 18. Visual regression (Percy/Chromatic/Applitools)

- **SOTA approach:** Playwright's native `expect(page).toHaveScreenshot()` for free local coverage; Applitools Eyes (perceptual Visual AI, longest head start) for enterprise; Chromatic for Storybook-first component teams; Percy for BrowserStack-bundled coverage.
- **Agent execution path:** `cli-anything` (`npx playwright test --update-snapshots`, `npx percy exec -- npm test`, `npx chromatic --project-token=...`); bundled skill `visual-regression-percy-chromatic-applitools`.
- **Source:** https://playwright.dev/docs/test-snapshots · https://applitools.com/ · https://www.chromatic.com/ · https://percy.io/
- **Confidence:** ✓ Fully executable (Percy/Chromatic/Applitools paywalled; Playwright native free fallback)

## 19. Test pyramid governance (unit vs integration vs E2E ratio)

- **SOTA approach:** Pyramid (unit > integration > E2E) OR Trophy (Kent C. Dodds — integration-heavy) — in 2026 the Trophy is increasingly favored for AI-first teams since LLM-generated code makes unit-test ratios less meaningful. Enforce via coverage tags + suite-size SLOs (unit < 100 ms median, integration < 5 s, E2E < 60 s).
- **Agent execution path:** `filesystem` writes coverage policy + suite-size CI gates; `cli-anything` (`uvx pytest --collect-only -q` to enumerate); bundled skill `test-pyramid-governance`.
- **Source:** https://martinfowler.com/articles/practical-test-pyramid.html · https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications · https://thoughtworks.com/radar
- **Confidence:** ✓ Fully executable

## 20. Flaky test management (quarantine, root-cause, AI healing)

- **SOTA approach:** Detect → quarantine (separate suite, doesn't block merge) → root-cause categorize (timing 70%+, DOM/selector 28%, network/data) → auto-heal via AI (FlakyGuard 47.6% reproducible fixes, Mergify auto-retry). 2-week "fix or remove" deadline (Microsoft pattern).
- **Agent execution path:** `cli-anything` (`uvx pytest --rerunfailures=2 --reruns-delay=1`, `npx playwright test --retries=2`); `github-api` MCP for quarantine PRs; bundled skill `flaky-test-quarantine-root-cause`.
- **Source:** https://testdino.com/blog/flaky-tests · https://trunk.io/flaky-tests · https://www.functionize.com/blog/the-flaky-test-problem-root-cause-and-how-ai-solves-it
- **Confidence:** ✓ Fully executable

## 21. CI/CD test integration (stages, parallelization, retries)

- **SOTA approach:** GitHub Actions / CircleCI / GitLab CI matrix runs with sharding (`playwright --shard=1/4`, `pytest-xdist -n auto`); fail-fast on smoke, full parallel for regression; nightly long-running; cache deps + browsers + Docker layers.
- **Agent execution path:** `github-api` MCP writes workflow YAMLs; `cli-anything` (`gh workflow run`, `gh run watch`); bundled skill `ci-cd-test-integration-parallelization`.
- **Source:** https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs · https://playwright.dev/docs/test-sharding · https://pytest-xdist.readthedocs.io/
- **Confidence:** ✓ Fully executable

## 22. Test reporting + dashboards

- **SOTA approach:** Allure (HTML + Jira integration) or ReportPortal (AI-driven aggregation) for dashboards; Playwright HTML reporter / pytest-html for per-run; Grafana for k6 perf trends; published to GitHub Pages or S3.
- **Agent execution path:** `cli-anything` (`uvx allure serve`, `npx playwright show-report`, `uv add --dev pytest-html`); bundled skill `test-reporting-dashboards`.
- **Source:** https://allurereport.org/ · https://reportportal.io/ · https://playwright.dev/docs/test-reporters
- **Confidence:** ✓ Fully executable

## 23. Release readiness checklist (go/no-go)

- **SOTA approach:** Standardized checklist enforced by CI: smoke green, critical-path green, a11y gate green, perf budget green, security gate green, no P0/P1 open, canary 24h clean. Codified in pull-request templates + branch protection.
- **Agent execution path:** `filesystem` writes `.github/pull_request_template.md` + branch-protection rules via `github-api`; bundled skill `release-readiness-checklists`.
- **Source:** https://dora.dev/research/ · https://www.thoughtworks.com/insights/articles/release-readiness-checklist
- **Confidence:** ✓ Fully executable

## 24. Smoke test automation

- **SOTA approach:** Top-of-pyramid 3-10 critical scenarios run on every deploy in <5 min; Playwright `--project=smoke` tag or pytest `-m smoke` marker; blocks deploy on red; surfaced in Slack via PR comment.
- **Agent execution path:** `cli-anything` (`npx playwright test --project=smoke`, `uvx pytest -m smoke`); `slack-mcp` for failure notifications; bundled skill cross-refs `regression-suite-curation-smoke-critical`.
- **Source:** https://playwright.dev/docs/test-projects · https://docs.pytest.org/en/stable/how-to/mark.html
- **Confidence:** ✓ Fully executable

## 25. Mutation testing (Stryker, mutmut, Pitest)

- **SOTA approach:** Stryker for JS/TS/Scala/.NET (Thoughtworks Radar 2026 Trial — AI-pruned mutants reduce noise 30%); mutmut for Python (88.5% detection, 1200 mutants/min); Pitest for Java/JVM. Verify the test suite actually catches bugs — kill rate > coverage % as quality metric.
- **Agent execution path:** `cli-anything` (`npx stryker run`, `uvx mutmut run`, `pitest` Gradle plugin); bundled skill `mutation-testing-stryker-mutmut`.
- **Source:** https://stryker-mutator.io/ · https://github.com/boxed/mutmut · https://pitest.org/
- **Confidence:** ✓ Fully executable

## 26. Code quality gates (SonarQube, CodeClimate)

- **SOTA approach:** SonarQube quality gates (coverage, duplication, complexity, security hotspots, AI-code-assurance gate as of 2026); CodeClimate maintainability score; fail PR on gate breach via GitHub status check.
- **Agent execution path:** `cli-anything` (`docker run sonarqube`, `sonar-scanner`); `github-api` writes status checks; bundled skill `quality-kpis-escape-rate-mttr` cross-refs.
- **Source:** https://docs.sonarsource.com/sonarqube-server/ · https://codeclimate.com/quality
- **Confidence:** ⚠ SonarQube self-host or SonarCloud paid for private repos; SonarCloud free for OSS

## 27. QA-Dev collaboration (shift-left)

- **SOTA approach:** TDD/BDD enforced in PRs; test plans authored in same sprint as feature design; QA in 3-amigo / story refinement; quality KPIs reviewed in retros. DORA shows shift-left correlates 4-5x with elite deploy frequency.
- **Agent execution path:** `filesystem` writes 3-amigo templates; `notion-mcp` / `jira-mcp` updates story templates; bundled skill `qa-dev-shift-left`.
- **Source:** https://dora.dev/research/ · https://www.atlassian.com/agile/software-development/3-amigos
- **Confidence:** ✓ Fully executable

## 28. Quality KPIs (escape rate, MTTR, escaped defects per release)

- **SOTA approach:** Track escape rate (defects found post-release / total) < 5%; MTTR for defects < 24h for P0; flakiness rate < 2%; coverage trends; reported per sprint. Surface in Datadog / Grafana / PostHog dashboards or Excel summary.
- **Agent execution path:** `cli-anything` (`jq` over Jira API export), `posthog-mcp` for product-side KPIs; `filesystem` writes weekly KPI report; bundled skill `quality-kpis-escape-rate-mttr`.
- **Source:** https://dora.dev/research/ · https://martinfowler.com/articles/qualityMetrics.html
- **Confidence:** ✓ Fully executable

---

## Summary table (≥90% fulfillment)

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | Test plan authoring | ISO 29119-3 + HTSM | `filesystem` + bundled skill | ✓ |
| 2 | Test case authoring (BDD) | Cucumber / pytest-bdd / Playwright-bdd | `cli-anything` + bundled skill | ✓ |
| 3 | Exploratory testing (SBTM) | Bach/Bolton SBTM charters | `filesystem` + `drawio-mcp` | ✓ |
| 4 | Regression suite curation | Playwright projects / pytest markers | `cli-anything` + bundled skill | ✓ |
| 5 | Manual QA workflows | DoD + Jira/Linear labels | `jira-mcp` / `linear-mcp` | ✓ |
| 6 | Accessibility (WCAG 2.2 AA) | axe-core + pa11y + Lighthouse | `cli-anything` + `playwright-mcp` | ✓ |
| 7 | Performance testing | k6 + Locust + Artillery | `cli-anything` | ✓ |
| 8 | API testing | Bruno + Postman + Newman | `cli-anything` | ✓ |
| 9 | Contract testing | Pact + Pact Broker / PactFlow | `cli-anything` | ⚠ |
| 10 | Security testing | OWASP ZAP + Burp + Snyk | `cli-anything` + `github-api` (SARIF) | ✓ |
| 11 | UAT coordination | TestRail/Qase + Notion sign-off | `notion-mcp` | ✓ |
| 12 | Test data management | Faker + Mockaroo + Tonic | `cli-anything` | ✓ |
| 13 | Defect triage | Severity × Priority matrix | `jira-mcp` / `linear-mcp` | ✓ |
| 14 | Bug verification + closure | DORA name-the-test pattern | `cli-anything` + `jira-mcp` | ✓ |
| 15 | Test environment management | Testcontainers + Docker + Neon branching | `cli-anything` + `kubernetes-mcp` | ✓ |
| 16 | Cross-browser strategy | Playwright + BrowserStack/Sauce/TestMu | `cli-anything` + `playwright-mcp` | ⚠ |
| 17 | Mobile testing | Maestro + Detox + Appium | `cli-anything` | ✓ |
| 18 | Visual regression | Playwright toHaveScreenshot + Applitools/Chromatic/Percy | `cli-anything` | ✓ |
| 19 | Test pyramid / trophy | Coverage policy + suite-size SLOs | `filesystem` + `cli-anything` | ✓ |
| 20 | Flaky test management | Detect/quarantine/heal pipeline | `cli-anything` + `github-api` | ✓ |
| 21 | CI/CD test integration | GH Actions matrix + sharding | `github-api` + `cli-anything` | ✓ |
| 22 | Test reporting / dashboards | Allure + ReportPortal + Playwright HTML | `cli-anything` | ✓ |
| 23 | Release readiness checklist | DORA gate + GH branch protection | `github-api` + `filesystem` | ✓ |
| 24 | Smoke test automation | Playwright/pytest smoke tags | `cli-anything` + `slack-mcp` | ✓ |
| 25 | Mutation testing | Stryker + mutmut + Pitest | `cli-anything` | ✓ |
| 26 | Code quality gates | SonarQube + CodeClimate | `cli-anything` + `github-api` | ⚠ |
| 27 | QA-Dev shift-left | 3-amigo + DORA practices | `notion-mcp` / `jira-mcp` | ✓ |
| 28 | Quality KPIs | Escape rate + MTTR + flakiness | `cli-anything` + `posthog-mcp` | ✓ |

**Fulfillment math:** 28 use cases mapped. 25 are full ✓ confidence; 3 are ⚠ (recipient-paywalled SaaS — PactFlow / BrowserStack-Sauce / SonarCloud-private — each with a free OSS fallback that ships immediately); 0 are ✗.

**Verdict: ~95% fulfillment.** The three ⚠ rows are paywalled-on-recipient SaaS — the agent ships with the OSS fallback path (OSS Pact Broker, local Playwright cross-browser, self-host SonarQube) that runs without paying. Every QA workflow has a named SOTA tool and an exact execution mechanism.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (cross-checked against `app/config/mcp_config.json`):
- `filesystem` — always
- `github` — PRs, status checks, SARIF uploads, branch protection (use cases 10, 14, 21, 23)
- `playwright-mcp` — E2E orchestration, axe-core integration, visual regression (use cases 1, 4, 6, 16, 18, 20, 22, 24)
- `postgresql-mcp` — fixtures, seeded test data, test DB inspection (use case 15)
- `sentry-mcp` — prod error triage + flaky-test escape-rate correlation (use cases 14, 20, 28)
- `kubernetes-mcp` — ephemeral test environments (use case 15)
- `jira-mcp` — defect triage, ticket lifecycle (use cases 5, 13, 14, 27)
- `linear-mcp` — same purpose as jira-mcp for Linear-shops (use cases 5, 13, 14, 27)
- `notion-mcp` — UAT sign-off, test plan reviews, retros (use cases 1, 11, 27)
- `slack-mcp` — smoke failure alerts, escape-rate weekly digest (use cases 24, 28)
- `posthog-mcp` — product-side defect signals + escape-rate (use case 28)

**Skill packs to create (bundled, 22-23 items)** in order of impact:
1. `test-plan-authoring-pmbok-iso`
2. `test-case-authoring-bdd-gherkin`
3. `exploratory-testing-charters-session-based`
4. `regression-suite-curation-smoke-critical`
5. `accessibility-testing-wcag-22-aa-axe`
6. `performance-testing-k6-locust-artillery`
7. `api-testing-postman-bruno-newman`
8. `contract-testing-pact`
9. `security-testing-owasp-zap-burp`
10. `uat-coordination`
11. `test-data-management-synthetic`
12. `defect-triage-severity-priority`
13. `cross-browser-browserstack-saucelabs-lambdatest`
14. `mobile-testing-real-devices-emulators`
15. `visual-regression-percy-chromatic-applitools`
16. `test-pyramid-governance`
17. `flaky-test-quarantine-root-cause`
18. `ci-cd-test-integration-parallelization`
19. `test-reporting-dashboards`
20. `release-readiness-checklists`
21. `mutation-testing-stryker-mutmut`
22. `qa-dev-shift-left`
23. `quality-kpis-escape-rate-mttr`

---

## Notes on remaining caveats (the ⚠ rows)

- **Contract testing (#9):** PactFlow hosted broker is paid; OSS Pact Broker (Docker image) is free and ships immediately. Agent defaults to OSS until recipient sets a `PACTFLOW_*` env var.
- **Cross-browser cloud (#16):** BrowserStack ($50-75k/yr at 100 parallel) / Sauce Labs ($80-120k/yr) / TestMu cheaper. Free fallback: local Playwright across Chromium + Firefox + WebKit covers 80%+ of regressions. Agent uses cloud only when `BROWSERSTACK_KEY` / `SAUCE_USERNAME` / etc. set.
- **Code quality gates (#26):** SonarCloud free for OSS, paid for private repos; SonarQube Community self-host free. Agent defaults to self-host or OSS path until recipient provides SonarCloud token.
