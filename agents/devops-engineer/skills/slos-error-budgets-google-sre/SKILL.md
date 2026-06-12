<!--
Source: https://sre.google/workbook/implementing-slos/ · https://sloth.dev/ · https://github.com/pyrra-dev/pyrra
Authored: June 2026 for the devops-engineer agent bundle.
-->

# SLOs + Error Budgets (Google SRE)

Define service-level objectives (SLOs), generate Prometheus recording +
alerting rules via **Sloth** or **Pyrra**, set up multi-window
multi-burn-rate alerts, and use error budgets to govern release pace.
Follows the Google SRE Workbook framework.

## When to use

- New service — define SLOs before turning on alerts.
- Existing service with flaky alerts ("we get paged for noise") — switch to
  budget-based alerting.
- "Should we ship feature X this week?" — answer via error budget burn rate.
- Quarterly SLO review (too tight = constant pages; too loose = no signal).

Skip when: service has <100 req/day (statistical SLOs are noisy); the system
is an experiment or alpha (no SLO commitment).

## Setup

```bash
brew install slok/repo/sloth                                  # Sloth (SLO generator)
# OR via Docker
docker pull ghcr.io/slok/sloth:v0.11.0

# Pyrra (K8s-native SLO operator)
kubectl apply -f https://github.com/pyrra-dev/pyrra/releases/latest/download/manifests.yaml

# Nobl9 — managed alternative (paid)
brew install nobl9/tools/sloctl
sloctl config add-context prod
```

No API key needed for Sloth/Pyrra; both run against Prometheus + AlertManager.

## Common recipes

### Recipe 1 — Define an SLI (the measurable signal)

The SLI must be from the **user's** perspective. For an HTTP API:

- **Availability**: successful_requests / total_requests
- **Latency**: requests_with_duration_below_threshold / total_requests
- **Quality**: requests_returning_correct_data / total_requests
- **Throughput**: sustained_requests_per_second

Avoid "CPU is below 80%" — that's not what users feel.

### Recipe 2 — Sloth spec (single SLO)

```yaml
# slos/api.yaml
version: prometheus/v1
service: api
labels:
  team: platform
slos:
  - name: requests-availability
    objective: 99.9       # over 30d (default time window)
    description: "99.9% of requests succeed (non-5xx)"
    sli:
      events:
        error_query: |
          sum(rate(http_requests_total{service="api",status=~"5.."}[{{.window}}]))
        total_query: |
          sum(rate(http_requests_total{service="api"}[{{.window}}]))
    alerting:
      name: ApiHighErrorRate
      labels: { team: platform }
      annotations:
        summary: "API error rate burning SLO budget"
        runbook_url: "https://github.com/myorg/runbooks/api/availability.md"
      page_alert:
        labels: { severity: critical }
      ticket_alert:
        labels: { severity: warning }
```

```bash
sloth generate -i slos/api.yaml -o prometheus-rules/api.yaml
sloth validate -i slos/api.yaml
kubectl apply -f prometheus-rules/api.yaml -n monitoring
```

Sloth emits **recording rules** for SLI + budget + burn rate, plus
**alerting rules** for multi-window multi-burn-rate.

### Recipe 3 — Multi-window multi-burn-rate (the Google pattern)

| Burn rate | Long window | Short window | Page/Ticket |
|---|---|---|---|
| 14.4× | 1h | 5m | Page |
| 6× | 6h | 30m | Page |
| 3× | 24h | 2h | Ticket |
| 1× | 72h | 6h | Ticket |

A page fires only when BOTH the long and short windows confirm — kills
false positives from blips. Sloth/Pyrra generate this automatically.

Math: burn rate = (actual_error_rate / (1 - SLO)) — i.e. how many "SLOs
worth" of budget is consumed per hour. At 14.4×, you burn 30 days of budget
in ~2 hours.

### Recipe 4 — Latency SLI (histogram_quantile)

```yaml
slos:
  - name: requests-latency-p99
    objective: 99
    description: "99% of requests under 200ms"
    sli:
      events:
        error_query: |
          sum(rate(http_request_duration_seconds_bucket{service="api",le="0.2"}[{{.window}}]))
        total_query: |
          sum(rate(http_request_duration_seconds_count{service="api"}[{{.window}}]))
        # NOTE: error_query is "good events" here; Sloth handles the inversion
```

Pattern: `rate(*_bucket{le="THRESHOLD"})` counts requests faster than the
threshold; divide by total. SLI = "fraction fast enough".

### Recipe 5 — Pyrra (K8s-native SLO CRD)

```yaml
apiVersion: pyrra.dev/v1alpha1
kind: ServiceLevelObjective
metadata: { name: api-availability, namespace: prod }
spec:
  target: "99.9"
  window: 28d
  description: "99.9% of API requests succeed"
  indicator:
    ratio:
      errors:
        metric: http_requests_total{service="api",status=~"5.."}
      total:
        metric: http_requests_total{service="api"}
  alerting:
    name: ApiAvailability
    labels: { team: platform }
```

```bash
kubectl apply -f api-slo.yaml
kubectl get servicelevelobjective -n prod
# Pyrra reconciles → PrometheusRules created automatically
```

Pyrra has a UI: `kubectl port-forward -n pyrra svc/pyrra-api-frontend 9099:9099`.

### Recipe 6 — Recording rules (efficient SLI)

Without recording rules, every alert evaluation re-runs the SLI query. With
them, the SLI is cached. Sloth/Pyrra generate these.

```yaml
groups:
  - name: api.slos
    rules:
      - record: slo:sli_error:rate5m
        expr: |
          sum(rate(http_requests_total{service="api",status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total{service="api"}[5m]))
        labels: { service: api, slo: requests-availability }
      - record: slo:error_budget:remaining
        expr: |
          1 - (slo:sli_error:rate30d / 0.001)    # 0.001 = (1 - 0.999) for 99.9%
        labels: { service: api, slo: requests-availability }
```

### Recipe 7 — Error budget policy (markdown sibling to code)

```markdown
# Error Budget Policy — api service

**SLO:** 99.9% availability over rolling 30 days
**Budget:** 0.1% × 30d = ~43 minutes of downtime per month

## Policy

- **Budget > 50% remaining (healthy):** Ship features at normal pace.
- **Budget 20-50% remaining (watch):** Slow risky changes; add canaries.
- **Budget 0-20% remaining (depleted):** Freeze non-essential feature
  releases. Only reliability work + critical bug fixes.
- **Budget exhausted (negative):** Full release freeze. Postmortem
  required. SLO breach reported to leadership.

## Review

- Quarterly SLO review on the second Tuesday.
- Targets that page rarely → too generous; tighten.
- Targets that page constantly → too aggressive; loosen or change SLI.
```

### Recipe 8 — Alert annotations

```yaml
alerting:
  page_alert:
    annotations:
      summary: "API burning error budget at {{ .Labels.burn_rate }}x rate"
      description: |
        Service {{ .Labels.service }} is consuming error budget at
        {{ .Labels.burn_rate }}× the sustainable rate (target {{ .Labels.objective }}%).
      runbook_url: "https://github.com/myorg/runbooks/api/{{ .Labels.slo }}.md"
      dashboard_url: "https://grafana.myorg.com/d/api-slo"
```

`runbook_url` is mandatory — paging without a runbook is paging into the void.

### Recipe 9 — Grafana SLO dashboard

```promql
# Current 30d budget remaining
slo:error_budget:remaining{service="api", slo="requests-availability"}

# Burn rate over time
slo:sli_error:rate1h / 0.001

# Time-to-exhaustion at current burn
((1 - slo:sli_error:rate30d / 0.001) * 30 * 24) / (slo:sli_error:rate1h / 0.001)
```

Grafana dashboard JSON example: https://grafana.com/grafana/dashboards/14348

### Recipe 10 — Test the alert (fault injection)

```bash
# Inject errors via a feature flag or canary
kubectl set env deployment/api -n prod ERROR_INJECT_RATE=0.1

# Watch
kubectl logs -n monitoring -l app=alertmanager -f
# Expect 14.4× page after ~5min
```

Restore: `kubectl set env deployment/api ERROR_INJECT_RATE=0 -n prod`.

### Recipe 11 — Validate Sloth spec in CI

```yaml
# .github/workflows/slos.yml
- name: Validate SLO specs
  run: |
    for f in slos/*.yaml; do
      docker run --rm -v $PWD:/work -w /work ghcr.io/slok/sloth:v0.11.0 validate -i $f
    done
- name: Generate PrometheusRules
  run: docker run --rm -v $PWD:/work -w /work ghcr.io/slok/sloth:v0.11.0 generate -i slos/ -o prometheus-rules/
- name: Confirm rules differ
  run: git diff --exit-code prometheus-rules/
```

PR fails if generated rules are out of sync with the spec.

### Recipe 12 — Nobl9 (managed alternative)

```yaml
# slo-api.yaml — Nobl9 declarative
apiVersion: n9/v1alpha
kind: SLO
metadata: { name: api-availability, project: production }
spec:
  service: api
  budgetingMethod: Occurrences
  objectives:
    - target: 0.999
      timeSliceWindow: 30d
  indicator:
    metricSource: { name: prometheus, kind: Agent }
    rawMetric:
      query: "sum(rate(http_requests_total{service='api',status!~'5..'}[1m])) / sum(rate(http_requests_total{service='api'}[1m]))"
```

```bash
sloctl apply -f slo-api.yaml
sloctl get slos
```

## Examples

### Example 1 — First SLO for new API service

**Goal:** Define + ship "99.9% availability over 30d" SLO.

1. Confirm metric exists: `http_requests_total{service="api",status="..."}`.
2. Author Sloth spec (Recipe 2).
3. `sloth generate -i api.yaml -o rules.yaml`.
4. `kubectl apply -f rules.yaml -n monitoring`.
5. Sanity check Prometheus:
   `slo:sli_error:rate5m{service="api"}` should evaluate.
6. Author runbook at `runbooks/api/availability.md`.
7. Commit + PR; review with on-call.

**Result:** Multi-burn-rate alerts live; runbook linked from each alert.

### Example 2 — Convert latency thresholds to a real SLO

**Goal:** Replace `latency > 1s` alert (noisy) with budget-based one.

1. Identify percentile: "99% of requests under 200ms over 7d".
2. Confirm histogram exists: `http_request_duration_seconds_bucket{le="0.2"}`.
3. Sloth spec (Recipe 4) — latency SLO with `objective: 99`, `time_window: 7d`.
4. Generate + apply rules.
5. Compare alert volume in Alertmanager over 1 week: expect 80%+ noise drop.

**Result:** Pages only when budget is at sustained risk.

## Edge cases / gotchas

- **SLI must be from the user's perspective.** "CPU at 80%" isn't an SLI;
  "requests served successfully" is.
- **Burn rate denominator is (1 - SLO), not error rate.** A 99.9% SLO and
  a 99% SLO have very different burn rates for the same error rate.
- **Rolling windows** (30d) require Prometheus retention ≥ window. If
  Prometheus retains 14d locally, use Mimir/Thanos remote_write.
- **SLI of zero traffic = undefined.** `total_query` returning 0 makes the
  SLI ratio NaN. Sloth handles via `slo:sli_error:absent`; verify.
- **Multi-instance services**: sum across all instances in the SLI. Don't
  per-instance SLO unless each is independently user-facing.
- **`for: 0s` on burn-rate alerts is fine** — the multi-window check IS the
  debounce.
- **Don't alert on SLO directly** — alert on burn rate. Direct SLO alerts
  fire once the budget is already spent.
- **Outages from upstream (cloud provider, DNS) burn budget too.** SLO
  policy must account for "shared fate" — Google SRE recommends a separate
  "vendor incident" tag rather than counting against budget.
- **Synthetic monitors** (uptime probes) give independent SLI signal but
  cost extra; useful as a redundancy SLI.
- **Pyrra's PrometheusRules are owned by the operator** — manual
  `kubectl edit` is overwritten.
- **Quarterly SLO review meeting** is the most important governance ritual.
  SLOs nobody talks about become decoration.

## Sources

- https://sre.google/workbook/implementing-slos/ — Google SRE Workbook chapter
- https://sre.google/workbook/alerting-on-slos/ — multi-burn-rate alerting
- https://sloth.dev/ — Sloth
- https://github.com/slok/sloth — Sloth source
- https://github.com/pyrra-dev/pyrra — Pyrra (K8s SLO operator)
- https://www.nobl9.com/ — Nobl9 (managed)
- https://grafana.com/grafana/dashboards/14348 — Sloth Grafana dashboard
- https://prometheus.io/docs/practices/alerting/ — Prometheus alerting practices
- https://www.usenix.org/conference/srecon19asia/presentation/jackson — SLO burn rate talk
