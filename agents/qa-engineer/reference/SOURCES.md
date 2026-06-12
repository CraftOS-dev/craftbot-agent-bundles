# QA / Test Engineer — Source Attribution

This file maps every section of `soul.md` and `role.md` back to the research source(s) it was derived from. It is part of the bundle but is **not** loaded into the agent's context — it exists for human verification and future updates.

Unlike `senior-python-engineer` (which downloaded verbatim agent definitions from wshobson/agents and VoltAgent before composition), the qa-engineer v1 build pass derived its content from 2026 web research (URLs below) rather than upstream agent definitions. Round-2 hardening should download 4-6 reference agents (test-automator, qa-engineer, debugger from wshobson/agents and VoltAgent) into `reference/agents/` for traceability tightening.

---

## soul.md → source map

| Section in soul.md | Source(s) |
|---|---|
| Title + persona intro (action-verb-first) | Composed from `reference/SOTA_USE_CASES.md` SOTA tooling per use case; ISO 29119 + DORA framing |
| Purpose | `reference/SOTA_USE_CASES.md` summary + DORA research framing |
| Execution stack | `reference/SOTA_USE_CASES.md` (each bullet maps to a SOTA tool research row) |
| When invoked — new feature | ISO 29119-3 plan template + HTSM risk model |
| When invoked — regression curation | Martin Fowler Test Pyramid + Kent C. Dodds Testing Trophy |
| When invoked — bug verification | DORA "name-the-test-that-would-have-caught-it" pattern |
| When invoked — flaky test triage | TestDino flaky test taxonomy (timing 70% / DOM 28% / network 2%) |
| When invoked — performance test | k6 docs + Locust docs (threshold-driven) |
| When invoked — accessibility audit | axe-core docs + WCAG 2.2 quick reference + pa11y |
| When invoked — release readiness call | DORA + Thoughtworks release readiness checklist |
| Core operating rules | Composed from research; DORA shift-left + flaky-test discipline + accessibility legal floor |
| Test pyramid / trophy decision table | Fowler Pyramid + Dodds Trophy + Thoughtworks Radar 2026 |
| Antipatterns to flag on sight | Composed from research; Playwright web-first assertions docs + testcontainers docs + mutation testing rationale |
| Quality KPIs | DORA research + Fowler Quality Metrics |
| Communication style | Composed from synthesis; not a domain claim — operational glue |
| Output format | Composed from synthesis; ISO 29119 doc structure |
| When to push back | Composed from research; accessibility legal floor + flaky-test discipline + DORA gating |
| When to defer | Sibling agents in `agent_bundle/agents/` (verified at write time) |
| On first conversation (PROACTIVE init) | `agent_bundle/METHODOLOGY.md` standard footer + role-specific routine questions |
| Closing rule | Restates load-bearing convictions from intro |

---

## role.md → source map

| Section in role.md | Source(s) |
|---|---|
| Capability reference — E2E frameworks | Playwright vs Cypress 2026 research (sources below) |
| Capability reference — Unit / integration | pytest docs + vitest docs + jest docs |
| Capability reference — API testing | Bruno docs + Postman/Newman docs + Insomnia |
| Capability reference — Contract testing | Pact docs |
| Capability reference — Performance / load | k6 vs Locust vs Artillery vs Gatling 2026 research |
| Capability reference — Security / DAST / SAST | OWASP ZAP vs Burp 2026 research + Snyk + Semgrep docs |
| Capability reference — Accessibility | axe-core + pa11y + Lighthouse 2026 research + WCAG 2.2 quick reference |
| Capability reference — Visual regression | Percy vs Chromatic vs Applitools 2026 research + Playwright snapshots docs |
| Capability reference — Cross-browser cloud | BrowserStack vs Sauce Labs vs LambdaTest/TestMu 2026 research |
| Capability reference — Mobile | Maestro vs Appium vs Detox 2026 research |
| Capability reference — Test management | TestRail vs Zephyr vs Xray vs Qase vs TestMo 2026 research |
| Capability reference — AI test maintenance | Mabl / Testim / Functionize / Katalon 2026 research |
| Capability reference — Mutation testing | Stryker / mutmut / Pitest 2026 research + Thoughtworks Radar |
| Capability reference — Code quality gates | SonarQube + CodeClimate 2026 research |
| Capability reference — Test data | Faker docs + Mockaroo + Tonic.ai 2026 research |
| Capability reference — Reporting | Allure + ReportPortal + Playwright HTML docs |
| Test plan template (ISO 29119-3 + HTSM) | ISO/IEC/IEEE 29119-3 + Bach Heuristic Test Strategy Model |
| BDD authoring playbook | Cucumber BDD docs + pytest-bdd docs |
| Accessibility audit playbook | axe-core + pa11y + WCAG 2.2 + manual screen-reader patterns |
| Performance test playbook | k6 docs (threshold-driven) + Locust docs |
| Contract testing playbook | Pact docs + can-i-deploy pattern |
| Flaky test triage playbook | TestDino flaky test taxonomy + Microsoft 2-week pattern + FlakyGuard AI healing |
| Defect triage matrix | Atlassian Jira bug-tracking + S × P industry pattern |
| Release readiness checklist | DORA + Thoughtworks release readiness |
| Antipattern catalog (5 BAD/GOOD pairs) | Composed from research; Playwright web-first docs + testcontainers + mutation-testing rationale |
| SOTA tool reference (per-tool) | Each H3 references the SOTA tool research row in `reference/SOTA_USE_CASES.md` |
| SOTA execution playbook table | Compiled from `reference/SOTA_USE_CASES.md` use-case → first-stop skill pack mapping |
| Bug verification comment template | DORA "name-the-test" pattern |
| Release-readiness memo template | DORA binary gates + Thoughtworks pattern |
| Weekly KPI digest template | DORA four metrics + Fowler Quality Metrics |

---

## Notes on "authored from synthesis"

A handful of sections in soul.md and role.md were composed locally rather than lifted verbatim:

- **Communication style, Output format, When to push back / defer** — operational glue between research-backed sections. Not domain claims.
- **Quality KPIs targets** (escape rate < 5%, MTTR < 24h, flakiness < 2%) — synthesized from DORA + Fowler Quality Metrics + industry-standard SLOs. Each target individually defensible from cited sources; the consolidated table is original synthesis.
- **Antipattern catalog code examples** — composed from research patterns; not lifted from a single canonical source. Each BAD/GOOD pair illustrates a research-cited principle.
- **Output templates (bug verification, release-readiness, weekly KPI)** — composed from DORA + Thoughtworks patterns; original wording.

The PROACTIVE.md self-init footer is a CraftBot-specific design decision documented in `agent_bundle/METHODOLOGY.md` and is the same mechanic across all agents (only the 2-3 role-specific questions change).

---

## SOTA tool sources (June 2026)

> Per-tool source table for the 2026 SOTA QA stack. Every tool listed here is referenced from role.md under `## SOTA tool reference (June 2026)` and from agent.yaml `sources:`.

### E2E frameworks

| Tool | Source | Skill pack |
|---|---|---|
| Playwright | https://playwright.dev/docs | `regression-suite-curation-smoke-critical` + default `playwright-mcp` |
| Cypress | https://docs.cypress.io | role.md capability reference |
| Playwright vs Cypress 2026 | https://getautonoma.com/blog/playwright-vs-cypress · https://reintech.io/blog/playwright-vs-cypress-2026-e2e-testing-comparison · https://tech-insider.org/cypress-vs-playwright-2026/ | role.md capability reference |
| Puppeteer | https://pptr.dev/ | role.md capability reference |
| WebdriverIO | https://webdriver.io/ | `mobile-testing-real-devices-emulators` + role.md |
| Selenium | https://www.selenium.dev/ | role.md capability reference |

### Unit / integration

| Tool | Source | Skill pack |
|---|---|---|
| pytest | https://docs.pytest.org/ | parent's `python-testing-patterns` |
| pytest-bdd | https://pytest-bdd.readthedocs.io/ | `test-case-authoring-bdd-gherkin` |
| Vitest | https://vitest.dev/ | role.md capability reference |
| Jest | https://jestjs.io/ | role.md capability reference |
| testcontainers | https://testcontainers.com/ | parent's `testcontainers-integration-testing` |
| Hypothesis | https://hypothesis.readthedocs.io/ | parent's `hypothesis-property-based` |
| pytest-xdist | https://pytest-xdist.readthedocs.io/ | `ci-cd-test-integration-parallelization` |
| pytest-rerunfailures | https://github.com/pytest-dev/pytest-rerunfailures | `flaky-test-quarantine-root-cause` |

### API testing

| Tool | Source | Skill pack |
|---|---|---|
| Bruno | https://docs.usebruno.com/ · https://github.com/usebruno/bruno | `api-testing-postman-bruno-newman` |
| Postman / Newman | https://learning.postman.com/docs/running-collections/using-newman-cli/running-collections-on-the-command-line/ | `api-testing-postman-bruno-newman` |
| Insomnia | https://docs.insomnia.rest/ | `api-testing-postman-bruno-newman` |
| Postman vs Bruno vs Insomnia 2026 | https://growai.in/postman-vs-bruno-vs-insomnia-api-testing-2026/ · https://www.openhelm.ai/blog/postman-vs-insomnia-vs-bruno-api-testing | role.md capability reference |
| msw (Mock Service Worker) | https://mswjs.io/ | role.md capability reference |
| WireMock | https://wiremock.org/ | role.md capability reference |
| Mountebank | http://www.mbtest.org/ | role.md capability reference |

### Contract testing

| Tool | Source | Skill pack |
|---|---|---|
| Pact | https://docs.pact.io/ | `contract-testing-pact` |
| PactFlow | https://pactflow.io/ | `contract-testing-pact` |
| Pact 2026 microservices guide | https://totalshiftleft.ai/blog/contract-testing-for-microservices · https://www.sqaexperts.com/consumerdriven-contract-testing-with-pact-microservices-qa-guide-for-2026 · https://qaskills.sh/blog/pact-contract-testing-complete-guide-2026 | role.md capability reference |
| Spring Cloud Contract | https://spring.io/projects/spring-cloud-contract | role.md capability reference |
| `can-i-deploy` | https://docs.pact.io/pact_broker/can_i_deploy | `contract-testing-pact` |

### Performance / load

| Tool | Source | Skill pack |
|---|---|---|
| k6 | https://k6.io/docs/ · https://github.com/grafana/k6 | `performance-testing-k6-locust-artillery` |
| Locust | https://docs.locust.io/ | `performance-testing-k6-locust-artillery` |
| Artillery | https://www.artillery.io/docs | `performance-testing-k6-locust-artillery` |
| Gatling | https://gatling.io/docs/ | `performance-testing-k6-locust-artillery` |
| JMeter | https://jmeter.apache.org/ | role.md capability reference |
| k6 vs Locust vs Artillery vs Gatling 2026 | https://www.vervali.com/blog/best-load-testing-tools-in-2026-definitive-guide-to-jmeter-gatling-k6-loadrunner-locust-blazemeter-neoload-artillery-and-more/ · https://thesoftwarescout.com/best-load-testing-tools-2026-k6-vs-locust-vs-jmeter-vs-artillery-compared/ | role.md capability reference |

### Security

| Tool | Source | Skill pack |
|---|---|---|
| OWASP ZAP | https://www.zaproxy.org/ | `security-testing-owasp-zap-burp` |
| ZAP GitHub Actions | https://github.com/zaproxy/action-baseline · https://github.com/zaproxy/action-full-scan | `security-testing-owasp-zap-burp` |
| Burp Suite | https://portswigger.net/burp | `security-testing-owasp-zap-burp` |
| OWASP ZAP vs Burp Suite 2026 | https://appsecsanta.com/dast-tools/burp-suite-vs-zap · https://bughuntertools.com/articles/owasp-zap-vs-burp-suite-2026/ · https://mintqa.com/blogs/burp-suite-vs-owasp-zap-in-ci-cd-a-real-startups-devsecops-case-study/ | role.md capability reference |
| Snyk | https://snyk.io/ | `security-testing-owasp-zap-burp` |
| pip-audit | https://pypi.org/project/pip-audit/ | `security-testing-owasp-zap-burp` |
| osv-scanner | https://google.github.io/osv-scanner/ | `security-testing-owasp-zap-burp` |
| Semgrep | https://semgrep.dev/ | role.md capability reference |
| CodeQL | https://codeql.github.com/ | role.md capability reference + default `codeql` skill |
| Trivy | https://trivy.dev/ | role.md capability reference |
| Grype | https://github.com/anchore/grype | role.md capability reference |

### Accessibility

| Tool | Source | Skill pack |
|---|---|---|
| axe-core | https://www.deque.com/axe/axe-core/ · https://github.com/dequelabs/axe-core | `accessibility-testing-wcag-22-aa-axe` |
| @axe-core/playwright | https://github.com/dequelabs/axe-core-npm/tree/develop/packages/playwright | `accessibility-testing-wcag-22-aa-axe` |
| pa11y | https://pa11y.org/ · https://github.com/pa11y/pa11y-ci | `accessibility-testing-wcag-22-aa-axe` |
| Lighthouse | https://developer.chrome.com/docs/lighthouse/ | `accessibility-testing-wcag-22-aa-axe` |
| WCAG 2.2 quick reference | https://www.w3.org/WAI/WCAG22/quickref/ | `accessibility-testing-wcag-22-aa-axe` |
| Accessibility automation 2026 | https://www.accesify.io/blog/accessibility-testing-automation-axe-pa11y-lighthouse-ci/ · https://crosscheck.cloud/blogs/best-accessibility-testing-tools-wcag/ · https://crosscheck.cloud/blogs/axe-vs-wave-vs-pa11y-accessibility-testing/ | role.md capability reference |
| NVDA / JAWS / VoiceOver | https://www.nvaccess.org/ · https://www.freedomscientific.com/products/software/jaws/ · https://www.apple.com/accessibility/vision/ | role.md capability reference |

### Visual regression

| Tool | Source | Skill pack |
|---|---|---|
| Playwright snapshots | https://playwright.dev/docs/test-snapshots | `visual-regression-percy-chromatic-applitools` |
| Applitools Eyes | https://applitools.com/ | `visual-regression-percy-chromatic-applitools` |
| Chromatic | https://www.chromatic.com/ | `visual-regression-percy-chromatic-applitools` |
| Percy | https://percy.io/ | `visual-regression-percy-chromatic-applitools` |
| Visual regression 2026 | https://bug0.com/knowledge-base/visual-regression-testing-tools · https://crosscheck.cloud/blogs/percy-vs-applitools-vs-chromatic-visual-regression-testing/ · https://saucelabs.com/resources/blog/comparing-the-20-best-visual-testing-tools-of-2026 | role.md capability reference |
| BackstopJS | https://github.com/garris/BackstopJS | role.md capability reference |

### Cross-browser cloud

| Tool | Source | Skill pack |
|---|---|---|
| BrowserStack Automate | https://www.browserstack.com/automate | `cross-browser-browserstack-saucelabs-lambdatest` |
| Sauce Labs | https://saucelabs.com/products/automated-testing | `cross-browser-browserstack-saucelabs-lambdatest` |
| TestMu AI (LambdaTest rebrand 2026) | https://www.lambdatest.com/ | `cross-browser-browserstack-saucelabs-lambdatest` |
| Cross-browser 2026 comparison | https://saucelabs.com/resources/blog/a-comprehensive-best-cross-browser-testing-tools-comparison · https://getautonoma.com/blog/browserstack-vs-saucelabs-2026 · https://outstaff-osmium.com/blog/browserstack-vs-lambdatest-comparison | role.md capability reference |

### Mobile

| Tool | Source | Skill pack |
|---|---|---|
| Maestro | https://maestro.dev/docs · https://github.com/mobile-dev-inc/maestro | `mobile-testing-real-devices-emulators` |
| Detox | https://wix.github.io/Detox/ · https://github.com/wix/Detox | `mobile-testing-real-devices-emulators` |
| Appium | https://appium.io/ | `mobile-testing-real-devices-emulators` |
| WebdriverIO + Appium | https://webdriver.io/docs/appium-service | `mobile-testing-real-devices-emulators` |
| XCUITest | https://developer.apple.com/documentation/xctest | role.md capability reference |
| Espresso | https://developer.android.com/training/testing/espresso | role.md capability reference |
| Mobile testing 2026 | https://maestro.dev/insights/best-mobile-app-testing-frameworks · https://www.drizz.dev/post/detox-vs-appium-vs-maestro-which-mobile-testing-framework-in-2026 · https://codersera.com/blog/maestro-vs-appium-vs-detox-2026/ | role.md capability reference |

### Test management

| Tool | Source | Skill pack |
|---|---|---|
| TestRail | https://www.testrail.com/ | role.md capability reference |
| Qase | https://qase.io/ | role.md capability reference |
| Zephyr Scale/Squad/Enterprise | https://smartbear.com/test-management/zephyr/ | role.md capability reference |
| Xray | https://www.getxray.app/ | role.md capability reference |
| TestMo | https://www.testmo.com/ | role.md capability reference |
| Test management 2026 | https://www.testrail.com/blog/popular-test-management-tools/ · https://www.qase.io/blog/best-test-management-tools/ · https://katalon.com/resources-center/blog/testrail-alternatives | role.md capability reference |

### AI test maintenance

| Tool | Source | Skill pack |
|---|---|---|
| Mabl | https://www.mabl.com/ | role.md capability reference |
| Testim (Tricentis) | https://www.testim.io/ | role.md capability reference |
| Functionize | https://www.functionize.com/ | role.md capability reference |
| Katalon | https://katalon.com/ | role.md capability reference |
| Reflect | https://reflect.run/ | role.md capability reference |
| AI testing 2026 | https://www.shiplight.ai/blog/best-ai-testing-tools-2026 · https://testcollab.com/blog/ai-testing-tools · https://getautonoma.com/blog/ai-testing-platform-comparison | role.md capability reference |

### Mutation testing

| Tool | Source | Skill pack |
|---|---|---|
| Stryker | https://stryker-mutator.io/ · https://github.com/stryker-mutator/stryker-js | `mutation-testing-stryker-mutmut` |
| mutmut | https://github.com/boxed/mutmut | `mutation-testing-stryker-mutmut` |
| Pitest | https://pitest.org/ | `mutation-testing-stryker-mutmut` |
| Mutation testing 2026 | https://oneuptime.com/blog/post/2026-01-24-mutation-testing/view · https://johal.in/mutation-testing-with-stryker-net-and-python-coverage-2026/ | role.md capability reference |

### Code quality gates

| Tool | Source | Skill pack |
|---|---|---|
| SonarQube | https://docs.sonarsource.com/sonarqube-server/ | `quality-kpis-escape-rate-mttr` |
| SonarCloud | https://docs.sonarsource.com/sonarqube-cloud/ | `quality-kpis-escape-rate-mttr` |
| CodeClimate | https://codeclimate.com/quality | `quality-kpis-escape-rate-mttr` |
| SonarQube quality gates docs | https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-quality-gates/introduction-to-quality-gates | `quality-kpis-escape-rate-mttr` |
| SonarQube AI code assurance | https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/ai-code-assurance/quality-gates-for-ai-code | role.md capability reference |

### Test data

| Tool | Source | Skill pack |
|---|---|---|
| Faker (Python) | https://faker.readthedocs.io/ | `test-data-management-synthetic` |
| Faker.js | https://fakerjs.dev/ | `test-data-management-synthetic` |
| Mockaroo | https://mockaroo.com/ | `test-data-management-synthetic` |
| Tonic.ai | https://www.tonic.ai/ · https://www.tonic.ai/blog/synthetic-data-generation-tools | `test-data-management-synthetic` |
| GenRocket | https://www.genrocket.com/ | role.md capability reference |
| Synthetic vs production data 2026 | https://totalshiftleft.ai/blog/synthetic-test-data-vs-production-data · https://totalshiftleft.ai/blog/test-data-management-modern-applications | role.md capability reference |

### Flaky test management

| Tool | Source | Skill pack |
|---|---|---|
| Trunk.io flaky tests | https://trunk.io/flaky-tests | `flaky-test-quarantine-root-cause` |
| Mergify flaky management | https://articles.mergify.com/how-to-get-rid-of-flaky-tests-lethal-tools/ | `flaky-test-quarantine-root-cause` |
| TestDino flaky guide | https://testdino.com/blog/flaky-tests · https://testdino.com/blog/flaky-test-benchmark · https://testdino.com/blog/flaky-test-detection-tools | `flaky-test-quarantine-root-cause` |
| Functionize AI flaky | https://www.functionize.com/blog/the-flaky-test-problem-root-cause-and-how-ai-solves-it | role.md capability reference |
| Harness flaky tests | https://www.harness.io/blog/flaky-tests-the-quiet-killer-of-productivity-in-your-ci-pipeline | role.md capability reference |

### CI integration

| Tool | Source | Skill pack |
|---|---|---|
| GitHub Actions matrix | https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs | `ci-cd-test-integration-parallelization` |
| Playwright sharding | https://playwright.dev/docs/test-sharding | `ci-cd-test-integration-parallelization` |
| pytest-xdist | https://pytest-xdist.readthedocs.io/ | `ci-cd-test-integration-parallelization` |
| Playwright retries | https://playwright.dev/docs/test-retries | `flaky-test-quarantine-root-cause` |

### Reporting

| Tool | Source | Skill pack |
|---|---|---|
| Allure Report | https://allurereport.org/ | `test-reporting-dashboards` |
| ReportPortal | https://reportportal.io/ | `test-reporting-dashboards` |
| Playwright HTML reporter | https://playwright.dev/docs/test-reporters | `test-reporting-dashboards` |
| pytest-html | https://pytest-html.readthedocs.io/ | `test-reporting-dashboards` |
| Currents | https://currents.dev/ | role.md capability reference |

### Methodology / strategy

| Source | URL | Used for |
|---|---|---|
| ISO/IEC/IEEE 29119-3 | https://www.iso.org/standard/79428.html | Test plan template |
| Heuristic Test Strategy Model (Bach) | https://www.satisfice.com/download/heuristic-test-strategy-model | Risk-based test plan |
| Session-Based Test Management (Bach/Bolton) | https://www.satisfice.com/download/session-based-test-management | Exploratory testing |
| Practical Test Pyramid (Fowler) | https://martinfowler.com/articles/practical-test-pyramid.html | Pyramid governance |
| Testing Trophy (Kent C. Dodds) | https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications | Trophy ratio |
| Test pyramid 2026 | https://testomat.io/blog/testing-pyramid-role-in-modern-software-testing-strategies/ · https://qalified.com/blog/test-pyramid-for-engineering-teams/ · https://getautonoma.com/blog/test-automation-strategy-ai-teams | role.md capability reference |
| Cucumber BDD docs | https://cucumber.io/docs/bdd/ | BDD authoring |
| 3-amigo collaboration | https://www.atlassian.com/agile/software-development/3-amigos | Shift-left |
| Shift-left testing 2026 | https://contextqa.com/blog/shift-left-testing-strategy/ | Shift-left rules |
| Definition of Done | https://www.atlassian.com/agile/project-management/definition-of-done | UAT criteria |
| Atlassian bug tracking with Jira | https://www.atlassian.com/agile/tutorials/bug-tracking-with-jira | Defect triage matrix |
| DORA research | https://dora.dev/research/ | Quality KPIs + release readiness + shift-left |
| Microservice testing (Fowler) | https://martinfowler.com/articles/microservice-testing/ | Bug verification + contract testing |
| Quality Metrics (Fowler) | https://martinfowler.com/articles/qualityMetrics.html | Quality KPI definitions |
| Thoughtworks Technology Radar | https://thoughtworks.com/radar | Mutation testing Trial ring + Trophy framing |

### Skill pack inventory (NEW — bundled by this agent)

| Skill pack | Tools covered |
|---|---|
| `test-plan-authoring-pmbok-iso` | ISO 29119-3, HTSM, PMBOK plan structure |
| `test-case-authoring-bdd-gherkin` | Cucumber.js, pytest-bdd, Playwright-bdd, Karate |
| `exploratory-testing-charters-session-based` | Bach/Bolton SBTM, Rapid Reporter, BugMagnet |
| `regression-suite-curation-smoke-critical` | Playwright projects, pytest markers, tagging strategy |
| `accessibility-testing-wcag-22-aa-axe` | axe-core, @axe-core/playwright, pa11y-ci, Lighthouse, NVDA/JAWS/VoiceOver |
| `performance-testing-k6-locust-artillery` | k6, Locust, Artillery, Gatling, JMeter |
| `api-testing-postman-bruno-newman` | Bruno (bru CLI), Postman + Newman, Insomnia + inso |
| `contract-testing-pact` | Pact, Pact Broker, PactFlow, `can-i-deploy`, bi-directional |
| `security-testing-owasp-zap-burp` | OWASP ZAP, Burp, Snyk, pip-audit, osv-scanner, gitleaks |
| `uat-coordination` | Acceptance criteria, Loom evidence, Notion sign-off |
| `test-data-management-synthetic` | Faker, Mockaroo, Tonic.ai, GenRocket |
| `defect-triage-severity-priority` | S1-S4 × P0-P3 matrix, SLA per quadrant |
| `cross-browser-browserstack-saucelabs-lambdatest` | BrowserStack, Sauce Labs, TestMu AI |
| `mobile-testing-real-devices-emulators` | Maestro, Detox, Appium, WebdriverIO |
| `visual-regression-percy-chromatic-applitools` | Playwright native + Applitools + Chromatic + Percy |
| `test-pyramid-governance` | Pyramid vs Trophy, suite-size SLOs |
| `flaky-test-quarantine-root-cause` | Detect / quarantine / heal / 2-week fix-or-remove |
| `ci-cd-test-integration-parallelization` | GH Actions matrix, Playwright sharding, pytest-xdist |
| `test-reporting-dashboards` | Allure, ReportPortal, Playwright HTML |
| `release-readiness-checklists` | DORA binary gates, GH branch protection |
| `mutation-testing-stryker-mutmut` | Stryker, mutmut, Pitest |
| `qa-dev-shift-left` | 3-amigo, TDD/BDD in PR, retro KPI review |
| `quality-kpis-escape-rate-mttr` | Escape rate, MTTR, flakiness, coverage + mutation, DORA |

---

## Refreshing from upstream

When SOTA tools change (new versions, model launches, API changes):

1. Re-run the SOTA web searches that backed `reference/SOTA_USE_CASES.md` for affected use cases.
2. Update the relevant skill pack(s) in `agents/qa-engineer/skills/<name>/SKILL.md`.
3. Update the SOTA sources table above.
4. Update `reference/SOTA_USE_CASES.md` confidence ratings if applicable.
5. Re-run `python verify.py qa-engineer` to confirm structure intact.
6. Re-build: `python build.py qa-engineer` produces a fresh `.craftbot`.

For Round-2 hardening (upstream agent definitions):

1. Download into `reference/agents/`:
   - `wshobson/agents` — `plugins/backend-development/agents/test-automator.md` (verify path)
   - `VoltAgent/awesome-claude-code-subagents` — `04-quality-security/qa-engineer.md` (verify path)
   - `VoltAgent/awesome-claude-code-subagents` — `04-quality-security/test-automator.md`
2. Map each section above to a downloaded reference file path (replace `composed from research` entries with file path).
3. Re-verify provenance with `verify.py`.
