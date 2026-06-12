<!--
Source: https://dora.dev/research/ · https://www.thoughtworks.com/insights/articles/release-readiness-checklist
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Release Readiness Checklists — DORA Gate + Branch Protection

A binary go/no-go checklist enforced by CI status checks and branch
protection. Every gate is automated where possible; manual ones have a
named owner. Aligned with DORA elite-team practices (change-failure < 5%,
restore time < 1h). Output: GO / GO-WITH-MITIGATION / HOLD memo.

## When to use

- Pre-deploy: is this release safe to ship?
- Hotfix: is this patch safe to deploy in 2 hours?
- Quarterly release: is the cumulative change safe?
- Audit: prove the release gate was checked
- Trigger phrases: "release readiness", "go/no-go", "release gate",
  "ship check", "DORA gate", "branch protection", "deployment criteria"

## Setup

```bash
# GitHub branch protection CLI
gh auth login

# Notion / Confluence for release memo
# Sentry / Datadog for canary monitoring
```

Auth: GitHub Admin scope for branch protection; Sentry / Datadog tokens for
SLO checks.

## Common recipes

### Recipe 1 — Master release-readiness checklist

```markdown
# Release Readiness — <version> — <date>

## Gates (all must be green)
- [ ] Smoke suite green — last 24h
- [ ] Critical-path green — last 24h
- [ ] Extended regression green — last 7 days (nightly)
- [ ] Accessibility gate green — 0 WCAG 2.2 AA violations on changed pages
- [ ] Performance budget hit — p99 within budget; no regression > 10%
- [ ] Security gate green — 0 ZAP high; 0 critical CVEs in deps; 0 leaked secrets
- [ ] Contract gate green — `pact-broker can-i-deploy` all consumers
- [ ] Mutation score above floor — > 60% on changed files
- [ ] 0 open P0 defects
- [ ] 0 open P1 defects without product-owner waiver
- [ ] Canary 24h clean — error rate / latency / saturation within baseline
- [ ] Rollback plan documented — runbook + named owner
- [ ] Feature flag default-off if risk > medium
- [ ] Observability ready — dashboards / alerts / on-call rotation

## Verdict
- GO  /  GO-WITH-MITIGATION  /  HOLD

Signed: qa-engineer — <date>
```

### Recipe 2 — Branch protection setup

```bash
# Require all CI gates to pass before merge
gh api -X PUT /repos/$ORG/$REPO/branches/main/protection \
  -F required_status_checks.strict=true \
  -f 'required_status_checks.contexts[]=smoke' \
  -f 'required_status_checks.contexts[]=critical-path' \
  -f 'required_status_checks.contexts[]=a11y' \
  -f 'required_status_checks.contexts[]=security' \
  -f 'required_status_checks.contexts[]=contracts' \
  -F required_pull_request_reviews.required_approving_review_count=2 \
  -F enforce_admins=true \
  -F restrictions=null
```

### Recipe 3 — Release-readiness CI workflow

```yaml
# .github/workflows/release-gate.yml
on:
  workflow_dispatch:
  push: { tags: ['v*'] }

jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Smoke
        run: npx playwright test --project=smoke
      - name: A11y
        run: npx pa11y-ci
      - name: Perf
        run: k6 run --quiet perf/load.js
      - name: Security — deps
        run: |
          uvx pip-audit --strict
          osv-scanner -r .
      - name: Security — DAST
        uses: zaproxy/action-baseline@v0.13.0
        with: { target: 'https://staging.example.com' }
      - name: Contract gate
        run: |
          pact-broker can-i-deploy \
            --pacticipant=WebApp --version=$GITHUB_SHA \
            --to-environment=production \
            --broker-base-url=${{ secrets.PACT_BROKER_BASE_URL }}
      - name: Mutation score
        run: uvx mutmut run && uvx mutmut junitxml > mutmut.xml
      - name: Defects
        run: |
          OPEN=$(gh issue list --label=P0 --label=P1 --state=open --json number | jq length)
          if [ "$OPEN" -gt 0 ]; then echo "Open P0/P1: $OPEN"; exit 1; fi
```

### Recipe 4 — Release-memo template

```markdown
# Release Memo — <version> — <date>

## Verdict
GO / GO-WITH-MITIGATION / HOLD

## Summary
<2-3 sentences on what's shipping and major risks>

## Gates
| Gate | Status | Link |
|---|---|---|
| Smoke | ✓ | <CI run> |
| Critical | ✓ | <CI run> |
| A11y | ✓ | <pa11y report> |
| Perf | ✓ | <k6 dashboard> |
| Security | ✓ | <SARIF link> |
| Contracts | ✓ | <Pact Broker> |
| Mutation | ✓ 67% | <mutmut report> |
| Defects | ✓ 0 P0/P1 | <Jira filter> |
| Canary | pending — 24h watch | <Sentry, Grafana> |

## Mitigations (if GO-WITH-MITIGATION)
- <risk> — feature flag <name> default-off; rollout 10/50/100% over 3 days
- <risk> — on-call <name> for first 48h post-deploy

## Holds (if HOLD)
- <gate> — <issue> — owner: <name> — ETA: <date>

## Rollback plan
- Trigger: error rate > 2% for 5 min OR p99 > 1500ms for 10 min
- Owner: <SRE name>
- Steps: <runbook link>
- Rollback time target: < 10 min

## Approvers
- QA: <signature>
- EM: <signature>
- PM: <signature>
- SRE on-call: <signature>
```

### Recipe 5 — Canary check workflow

```yaml
# .github/workflows/canary.yml
on: { workflow_dispatch: { inputs: { version: { type: string } } } }
jobs:
  canary:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy 5% canary
        run: kubectl apply -f canary.yaml
      - name: Wait 30 min
        run: sleep 1800
      - name: Check error rate (Sentry)
        run: |
          ERRORS=$(curl -H "Authorization: Bearer $SENTRY_TOKEN" \
            "https://sentry.io/api/0/organizations/$ORG/events-stats/?project=app&query=release:${{ inputs.version }}&interval=1m" \
            | jq '.data[] | .[1]' | jq -s 'add')
          if [ "$ERRORS" -gt 10 ]; then exit 1; fi
      - name: Check p99 (Grafana)
        run: |
          P99=$(curl -H "Authorization: Bearer $GRAFANA_TOKEN" \
            "https://grafana.example.com/api/datasources/proxy/1/api/v1/query?query=histogram_quantile(0.99,...)" \
            | jq '.data.result[0].value[1] | tonumber')
          if (( $(echo "$P99 > 800" | bc -l) )); then exit 1; fi
      - name: Promote to 100%
        run: kubectl apply -f production.yaml
```

### Recipe 6 — Pre-deploy hold conditions

```markdown
## HOLD if any of these
- Any open P0 defect
- > 1 open P1 defect without waiver
- ZAP high-severity alert unresolved
- pact-broker can-i-deploy returns non-zero
- Mutation score regressed > 5% from last release
- Performance p99 regressed > 10% on critical endpoint
- Critical-path or smoke red in last 24h
- > 5% of CI runs flaky in last 24h
- Migration without rollback path
- Feature flag missing for risk-> medium changes
```

### Recipe 7 — GO-WITH-MITIGATION rules

```markdown
## When MITIGATION is acceptable
- S2 defect in non-critical area + feature flag default-off
- S3 defect with workaround documented in release notes
- Performance regression < 10% with monitoring + on-call standing by
- Known a11y rule on non-changed pages, with backlog ticket

## When NEVER mitigated (always HOLD)
- Data-loss risk
- Authn / authz bypass
- PII leak risk
- Compliance regression (SOC 2, PCI, HIPAA, GDPR)
```

### Recipe 8 — Automated PR template

```markdown
<!-- .github/PULL_REQUEST_TEMPLATE.md -->
## Release impact
- [ ] No customer-facing impact
- [ ] Behind feature flag — default off
- [ ] Migration included; rollback tested
- [ ] Touches critical path (auth / billing / checkout) — extra review

## Tests
- [ ] Unit added/updated
- [ ] Integration added/updated
- [ ] E2E added/updated (Playwright)
- [ ] A11y verified (if UI)
- [ ] Visual diff approved (if UI)

## Gates checked
- [ ] CI green
- [ ] Mutation score not regressed
- [ ] Coverage delta < -1%

## Sign-off
- [ ] QA: <name>
- [ ] EM: <name>
- [ ] PM acknowledged (if customer-facing)
```

### Recipe 9 — DORA metrics + release gate

```markdown
| DORA metric | Elite target | This release |
|---|---|---|
| Lead time for changes | < 1 day | <value> |
| Deploy frequency | multiple/day | <value> |
| Change failure rate | < 5% | <value> |
| Mean time to restore | < 1h | <value> |
```

Hold deploy if change-failure rate trending up > 10% over last 30 days
without explanation.

### Recipe 10 — Notion release page (notion-mcp)

```python
# Pseudo via notion-mcp
# Create page "Releases / <version>" under "Engineering / Release"
# Body: render memo markdown
# Properties:
#   - Verdict: GO | MITIGATION | HOLD
#   - Risk score: int
#   - Deploy date: date
#   - Rollback owner: person
# After release: append post-mortem section if change-failure
```

### Recipe 11 — Rollback drill

```bash
# Once per quarter — practice rollback
kubectl rollout undo deployment/app -n production
# Or via Argo Rollouts
argocd app rollback app-prod
# Measure time-to-restore; aim < 10 min
```

Track drill outcome in Notion; failed drills = release-gate impediment.

### Recipe 12 — Post-release escape tracking

```markdown
## Post-release escape — <version>
| Issue | Severity | Detected | Fix release | Why missed |
|---|---|---|---|---|
| ORD-1284 | S2 | 2026-06-12 | v1.42.1 | Edge case not in regression |
| PMT-9921 | S3 | 2026-06-13 | v1.43 | Workaround documented |
```

Feeds next sprint retro + next release plan's risk table.

## Examples

### Example 1: Release v1.42 — full gate run

**Goal:** Ship v1.42 with audit-grade evidence.

1. Pre-cut: PR opens release branch (Recipe 8).
2. CI runs release-gate workflow (Recipe 3).
3. All gates pass; verdict GO (Recipe 4 memo signed).
4. 5% canary 30 min (Recipe 5) — green; promote to 100%.
5. Memo published to Notion (Recipe 10).
6. 24h post-deploy: no escape; close release.

### Example 2: Hotfix release — abbreviated gate

**Goal:** Fix P0 in 2 hours.

1. Hotfix branch; only smoke + the fix's own test run.
2. Memo notes "GO-WITH-MITIGATION: skipped full regression due to time".
3. SRE on standing by; extra-aggressive canary (15 min at 5%).
4. Post-hoc: full regression on hotfix branch next day.

## Edge cases / gotchas

- **Override culture** — if EM always overrides HOLD verdicts, gate is
  theater. Each override needs documented rationale + retro.
- **Ceremonial sign-off** — checkbox without evidence is theater too. Each
  gate links to its CI run / dashboard.
- **Pre-defined waivers** — "P1 with feature flag is OK" — document policy
  in Recipe 7 so it's not case-by-case.
- **Last-minute hotfix bypass** — emergency process must still produce a
  memo, even short.
- **Long-running canary** — 24h is the default; lower at your own risk.
- **Tagged-release-only workflow** — gate fires only on `v*` push; safe.
  Don't run on every push.
- **Pact `can-i-deploy` flakes** — broker outage causes false negatives.
  Distinguish "unknown" vs "incompatible".
- **Branch protection bypass via admin** — `enforce_admins: true` prevents.
- **Coverage delta noise** — small refactors show -2% just from rename.
  Tolerance band (e.g., > -1% allowed).
- **Mutation regression on legacy code** — set per-file thresholds; don't
  block on file that was never tested.
- **Release notes ≠ release memo** — release notes are customer-facing;
  memo is internal sign-off.

## Sources

- [DORA research](https://dora.dev/research/)
- [Thoughtworks — Release Readiness](https://www.thoughtworks.com/insights/articles/release-readiness-checklist)
- [GitHub branch protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
- [Google SRE — release engineering](https://sre.google/sre-book/release-engineering/)
- [Argo Rollouts](https://argo-rollouts.readthedocs.io/)
- [Atlassian — DoD](https://www.atlassian.com/agile/project-management/definition-of-done)
- [Pact can-i-deploy](https://docs.pact.io/pact_broker/can_i_deploy)
- [Sentry release tracking](https://docs.sentry.io/product/releases/)
- [Datadog deployment tracking](https://docs.datadoghq.com/tracing/services/deployment_tracking/)
