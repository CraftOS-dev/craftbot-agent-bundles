<!--
Source: https://www.iso.org/standard/79428.html · https://www.satisfice.com/download/heuristic-test-strategy-model
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Test Plan Authoring — ISO 29119-3 + HTSM

The 2026 SOTA test plan is a Markdown living-doc committed to the repo
(`docs/test-plans/<feature>.md`) under PR review, structured per **ISO/IEC/IEEE
29119-3** (test documentation) and risk-modeled with the **Heuristic Test
Strategy Model** (Bach). PMBOK-style sections for stakeholder readability;
binary entry/exit criteria for CI gating.

## When to use

- A new feature, epic, or release needs a written test strategy
- A regulated audit (SOC 2 / ISO / FDA / FedRAMP) demands documented test
  evidence
- Cross-team coordination needed (PM, dev, QA, infra all signing off)
- Trigger phrases: "write a test plan", "test strategy for X", "release plan",
  "ISO 29119", "audit evidence", "test approach document"

Do NOT use for: a single bug fix (inline regression test is enough); a spike
or throwaway prototype.

## Setup

```bash
# No tooling required — Markdown + Git.
# Optional: lint plans with vale or markdownlint
brew install vale
npm i -g markdownlint-cli2
```

Auth / API key requirements: none. Notion sign-off requires `notion-mcp`.

## Common recipes

### Recipe 1 — ISO 29119-3 plan skeleton

Save as `docs/test-plans/<feature>.md`:

```markdown
# Test Plan — <Feature> — TP-<slug>-v<N>

## 1. Identification
- Plan ID: TP-<slug>-v1
- Sprint: <NN>  Release: <vX.Y>
- Owner: <name>  Reviewers: <PM, EM, SRE>
- Date: <YYYY-MM-DD>

## 2. Scope
- In scope: <bulleted features>
- Out of scope: <explicit exclusions>
- Assumptions: <env, data, dependencies>

## 3. Risk model (HTSM-lite)
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Payment double-charge | M | H | Idempotency key + replay test |
| Auth bypass | L | H | OWASP ZAP scan + manual auth review |
| Data loss on rollback | M | H | Migration dry-run + restore drill |

## 4. Test approach
- Tiering: smoke (<5min) / critical (<30min) / extended (nightly)
- Trophy ratio target: 25% static / 15% unit / 40% integration / 15% E2E / 5% manual
- Frameworks: Playwright + pytest + k6 + axe-core + Pact
- Test data: synthetic via Faker; masked snapshot for PII fields

## 5. Pass/fail criteria
- All smoke green
- Critical-path green
- 0 WCAG 2.2 AA violations on changed pages
- p99 < <ms> at <X> RPS
- 0 ZAP high-severity alerts
- Mutation score > 60% on changed files
- 0 open P0/P1 defects

## 6. Entry / exit criteria
- Entry: feature merged to staging; smoke green; canary 1h clean
- Exit: all pass criteria met OR product-owner override with mitigation

## 7. Schedule
- Test design: <date>
- Test execution: <date range>
- Sign-off target: <date>

## 8. Resources
- Owner: <QA>  Devs: <list>  PM: <name>
- Environments: staging-pr-<NN>; ephemeral DB via Neon branch
- Tooling: Playwright, k6, ZAP, Pact

## 9. Communication
- Slack: #qa-<feature>  Notion: <link>
- Daily status: by 17:00 UTC; final report: <date>
```

### Recipe 2 — HTSM risk-table generator (heuristic checklist)

Walk every dimension of the **Project / Quality Criteria / Product Elements / Test
Techniques** quadrants, score each risk on Likelihood (L/M/H) × Impact (L/M/H):

```markdown
| Quadrant | Risk source | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| Product elements — Structure | Schema migration breaks reads | M | H | Migration dry-run + rollback drill |
| Product elements — Function | New API endpoint mis-validates input | M | M | Property-based test with Hypothesis |
| Quality — Capability | Feature missing for power users | L | M | UAT scenario coverage |
| Quality — Security | New endpoint lacks authz check | M | H | ZAP + manual OWASP ASVS review |
| Quality — Performance | Query plan regression | M | H | k6 thresholds + EXPLAIN diff |
| Quality — Compatibility | iOS Safari WebKit bug | L | M | Playwright WebKit project + BrowserStack iOS |
| Quality — Reliability | Race on concurrent writes | M | H | Stateful Hypothesis test |
| Project — Schedule | Late spec freeze | H | M | 3-amigo refinement; testable acceptance |
| Project — People | Single owner | M | M | Pair on author + reviewer |
```

### Recipe 3 — Pre-PR test-plan PR template

```markdown
# .github/PULL_REQUEST_TEMPLATE/test_plan.md
## Test plan link
- [ ] `docs/test-plans/<feature>.md` updated this PR

## Risk review
- [ ] HTSM table reviewed in 3-amigo
- [ ] Pass/fail criteria CI-enforceable
- [ ] Entry/exit dates set

## Sign-off
- [ ] PM acknowledged scope
- [ ] EM acknowledged risk
- [ ] QA owner assigned
```

### Recipe 4 — markdownlint plan-style enforcement

```yaml
# .markdownlint-cli2.yaml
config:
  default: true
  MD013: false       # line length OK
  MD024: false       # allow duplicate headings (multiple "Scope" per release)
  MD033:             # allow inline HTML for tables
    allowed_elements: ["br", "kbd"]
globs:
  - "docs/test-plans/**/*.md"
```

```bash
npx markdownlint-cli2 "docs/test-plans/**/*.md"
```

### Recipe 5 — `vale` prose lint with QA dictionary

```ini
# .vale.ini
StylesPath = .vale
MinAlertLevel = suggestion
[*.md]
BasedOnStyles = QA
```

```bash
vale docs/test-plans/
```

Add to `.vale/QA/Approved.yml`:
```yaml
extends: existence
message: "Prefer 'pass criteria' over 'acceptance criteria' in test plans."
level: warning
tokens:
  - acceptance criteria
```

### Recipe 6 — Embed plan in Notion via mcp__notion-mcp

```python
# Pseudo (use the agent's notion-mcp tool):
# Page: "Test Plans / <feature>"
# Body: paste rendered Markdown
# Properties:
#   Status: Draft | In Review | Approved | Executing | Done
#   Owner: <person>
#   Risk Score: sum(L*I) per HTSM
```

### Recipe 7 — Entry/exit CI gate (GitHub Actions)

```yaml
# .github/workflows/release-gate.yml
on: [pull_request]
jobs:
  release-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Verify test plan exists
        run: |
          FEATURE=$(gh pr view ${{ github.event.pull_request.number }} \
            --json labels --jq '.labels[] | select(.name|startswith("feature/")) | .name | sub("^feature/";"")')
          test -f "docs/test-plans/${FEATURE}.md" || \
            (echo "Missing docs/test-plans/${FEATURE}.md"; exit 1)
      - name: Check pass/fail criteria block
        run: grep -q "Pass/fail criteria" "docs/test-plans/${FEATURE}.md"
```

### Recipe 8 — Trace acceptance criteria → test ID

```markdown
## Acceptance criteria → test mapping
| AC ID | Acceptance criterion | Test ID | Status |
|---|---|---|---|
| AC-1 | User can sign up with valid email | tests/auth/signup.spec.ts::valid_email | green |
| AC-2 | Duplicate email returns 409 | tests/auth/signup.spec.ts::duplicate_email | green |
| AC-3 | Password < 12 chars rejected | tests/auth/signup.spec.ts::weak_password | red |
```

Stops "what AC covers what test" debate at sign-off.

### Recipe 9 — Reuse plan template via `cookiecutter`

```bash
uvx cookiecutter gh:org/qa-test-plan-template \
  --no-input feature_slug=payments-v2 owner="QA Eng" sprint=42
```

Drops a populated plan in one command.

### Recipe 10 — Per-release plan rollup

`docs/test-plans/_index.md`:

```markdown
| Release | Plan | Verdict | Defects escaped | Notes |
|---|---|---|---|---|
| v1.42 | [payments-v2](payments-v2.md) | GO | 0 | Canary clean |
| v1.41 | [auth-refresh](auth-refresh.md) | GO-WITH-MITIGATION | 1 P2 | Feature flag rollout |
| v1.40 | [search-rerank](search-rerank.md) | HOLD | 1 P0 | Rolled back; replan v1.40.1 |
```

## Examples

### Example 1: Greenfield feature — author + ship

**Goal:** Ship a new "two-factor auth" feature with audit-grade docs.

1. Fork `docs/test-plans/_template.md` → `two-factor-auth.md`.
2. Fill HTSM table — at least one risk per quadrant.
3. Open PR with `test-plan` label; assign EM + PM reviewers.
4. After approval, link plan in feature epic; QA executes per Schedule.
5. At exit, attach release-readiness memo + Allure report to the plan.

**Result:** PR-trail, sign-off, evidence, all in Git history.

### Example 2: Regulated audit — SOC 2 evidence

**Goal:** Auditor asks "show me your test plan for change <SHA>".

1. `git log --grep "TP-" -- docs/test-plans/` lists every plan.
2. Each plan committed alongside the feature PR — same SHA.
3. Plan includes risk model, pass/fail criteria, sign-off line.
4. Export via `pandoc docs/test-plans/<feat>.md -o evidence.pdf`.

**Result:** Auditor closes the control without further questions.

## Edge cases / gotchas

- **Plan rot** — out-of-date plans are worse than none. Tie plan updates to
  feature PRs via PR template checklist.
- **Over-engineering** — 1-page plans are normal for small features. ISO 29119
  is a checklist, not a word-count target.
- **Risk theater** — every plan listing "data loss" as M/H is noise. Score
  honestly; let HTSM drive coverage budget.
- **Acceptance criteria drift** — when PM rewrites ACs mid-sprint, update the
  AC→test mapping table the same day.
- **Sign-off as ceremony** — require named reviewers on the PR, not "team
  approved" emoji reactions in Slack.
- **Plans without entry/exit criteria** — these are essays, not plans. Refuse
  to merge without binary criteria.
- **Confusing severity vs priority in pass criteria** — "0 P0/P1 open" is the
  release-blocker; "0 S1/S2" is the engineering-debt rule.
- **PMBOK overload** — ignore stakeholder communication matrices for internal
  features; keep them for enterprise/regulated.

## Sources

- [ISO/IEC/IEEE 29119-3 — Test documentation](https://www.iso.org/standard/79428.html)
- [Heuristic Test Strategy Model — James Bach](https://www.satisfice.com/download/heuristic-test-strategy-model)
- [Risk-based testing — Hans Schaefer](https://www.testingreferences.com/risk-based-testing.php)
- [PMBOK 7 — quality management chapter](https://www.pmi.org/standards/pmbok)
- [Ministry of Testing — test plan templates](https://www.ministryoftesting.com/dojo/lessons/test-planning)
- [Atlassian — Definition of Done](https://www.atlassian.com/agile/project-management/definition-of-done)
