<!--
Source: https://sre.google/sre-book/managing-incidents/ · https://developer.pagerduty.com/api-reference/ · https://incident.io/changelog
Authored: June 2026 for the devops-engineer agent bundle.
-->

# PagerDuty / Opsgenie / Incident.io / Rootly — Incident Response

Paging + war-room coordination + post-incident review. **PagerDuty**
(enterprise default), **Opsgenie** (Atlassian), **Incident.io** (modern
combined IRM + on-call), **Rootly** (modern IRM), **FireHydrant** (modern
IRM), **Grafana OnCall** (OSS free). Sets the rotation, fires the page,
opens the war-room, drives the timeline, and produces the blameless PIR.

## When to use

- A SEV1/SEV2 page just fired — drive the response.
- Setting up on-call rotation for a new service.
- Wiring alerts → paging provider (Alertmanager webhook, etc.).
- Authoring a runbook (linked from alert annotations).
- Drafting a post-incident review.

Skip when: incident is SEV3 (file a ticket, no page); team is one person
(use Grafana OnCall free).

## Setup

```bash
# CLIs
brew install pagerduty/tap/pd-cli              # PagerDuty
brew install opsgenie/opsgenie-cli/opsgenie-cli # Opsgenie
npm install -g @incident.io/cli                # Incident.io
brew install rootly/tools/rootly               # Rootly

# Auth
export PD_API_KEY="..."        # PagerDuty REST API key
export OPSGENIE_API_KEY="..."
export INCIDENT_IO_API_KEY="inc_..."
export ROOTLY_API_KEY="..."

# Grafana OnCall (OSS, self-hosted)
helm repo add grafana https://grafana.github.io/helm-charts
helm upgrade --install oncall grafana/oncall -n oncall --create-namespace
```

Pricing (2026):
- PagerDuty: $21/user/mo (Professional); higher for Business.
- Opsgenie: $9/user/mo (Standard).
- Incident.io: $29/user/mo (combined IRM + on-call).
- Rootly: from $24/user/mo.
- FireHydrant: from $25/user/mo.
- Grafana OnCall: free, self-hosted (or Grafana Cloud Pro).

## Common recipes

### Recipe 1 — Severity matrix

```markdown
| Level | Definition | Response | Comms |
|---|---|---|---|
| SEV1 | User-facing outage; revenue/SLA impact | Page now. Mitigate first. War-room. | Status page + customer email |
| SEV2 | Degraded service for >10 min | Page during biz hours. | Internal Slack + status page if customer-visible |
| SEV3 | Internal-only issue; no user impact | File ticket. Schedule fix. | Internal Slack |
```

### Recipe 2 — SEV1 flow (60-second mitigation default)

1. **Acknowledge page** within 5 min. Slack: `@here ack — investigating`.
2. **Open war-room.** `incident-io declare` or `rootly declare` opens
   the channel + timeline. Pull in on-call SRE, service owner, recent deployer.
3. **Mitigate first.** Default ladder:
   - `argocd app rollback <app>` (60s)
   - `kubectl rollout undo deployment <name>` (30s)
   - Feature flag off
   - `kubectl scale deployment <name> --replicas=0` (runaway pods)
   - DNS cutover to fallback
4. **Confirm mitigation.** Watch SLI graph. Error rate drops, latency
   recovers? Good. Re-page the channel; downgrade severity.
5. **Diagnose** — only after mitigation. Pull:
   - Last 5 deploys (`gh run list --limit 5`, `argocd app history`)
   - Sentry errors (filtered to service + 30min window)
   - Tail logs (`kubectl logs --tail=200 -l app=<svc>`)
   - Honeycomb/Datadog traces around incident start
6. **Status page** update for SEV1 — `statuspage` CLI or auto-sync.
7. **Resolve** when SLI back in budget AND root cause hypothesized.

### Recipe 3 — Alertmanager → PagerDuty

```yaml
# alertmanager-config.yaml
route:
  receiver: slack-default
  group_by: [alertname, cluster, service]
  routes:
    - matchers: [severity="critical"]
      receiver: pagerduty-prod
      continue: true
    - matchers: [severity="warning"]
      receiver: slack-alerts

receivers:
  - name: pagerduty-prod
    pagerduty_configs:
      - service_key: ${PAGERDUTY_INTEGRATION_KEY}
        description: '{{ .CommonAnnotations.summary }}'
        details:
          runbook: '{{ .CommonAnnotations.runbook_url }}'
          dashboard: '{{ .CommonAnnotations.dashboard }}'
          labels: '{{ .CommonLabels }}'
```

PagerDuty Integration Key from Service → Integrations → Prometheus.

### Recipe 4 — PagerDuty REST API (create incident from script)

```bash
curl -X POST https://api.pagerduty.com/incidents \
  -H "Authorization: Token token=${PD_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.pagerduty+json;version=2" \
  -H "From: ops@myorg.com" \
  -d '{
    "incident": {
      "type": "incident",
      "title": "API 5xx spike",
      "service": { "id": "PSERVICE", "type": "service_reference" },
      "urgency": "high",
      "body": { "type": "incident_body", "details": "Error rate at 8%. Runbook: ..." }
    }
  }'
```

### Recipe 5 — Incident.io declarative (Terraform)

```hcl
resource "incident_io_workflow" "auto_page_sev1" {
  name      = "Auto-page on SEV1"
  trigger   = "incident.created"
  condition_groups = [{
    conditions = [{
      subject  = "incident.severity"
      operation = "is"
      param_bindings = [{ value = "SEV1" }]
    }]
  }]
  expressions = []
  steps = [{
    name = "page_oncall"
    param_bindings = [
      { array_value = [{ literal = "ESCALATION_LEVEL_1" }] }
    ]
  }]
}
```

### Recipe 6 — Opsgenie team escalation

```yaml
# Opsgenie escalation policy
name: api-escalation
rules:
  - delay: 0min
    notify: { type: user, username: oncall-primary@myorg.com }
  - delay: 5min
    notify: { type: user, username: oncall-secondary@myorg.com }
  - delay: 15min
    notify: { type: team, name: platform-team }
  - delay: 30min
    notify: { type: schedule, name: vp-eng-escalation }
```

```bash
opsgenie-cli createEscalation --name api-escalation --rules @rules.json
```

### Recipe 7 — Grafana OnCall (OSS) routing

```yaml
# integration: prometheus-alertmanager
# escalation_chain
escalation_chain:
  name: critical-escalation
  steps:
    - type: notify_persons
      persons: [oncall-primary]
    - type: wait
      duration: 5m
    - type: notify_persons
      persons: [oncall-secondary]
    - type: wait
      duration: 10m
    - type: notify_team
      team: platform
```

Bot users in Slack/MS Teams handle the actual paging via push notification.

### Recipe 8 — Runbook template (linked from alert)

```markdown
# Runbook: api — high error rate

## Severity
SEV1 if rate > 5% sustained 2m; SEV2 if rate > 1% sustained 10m.

## Impact
~`<%>`% of requests failing 5xx. Customer dashboards may be empty.

## Symptoms
- Alert `ApiHighErrorRate` firing
- Sentry issue volume spike
- Grafana `api-overview` panel red

## Diagnose
1. `kubectl logs --tail=200 -l app=api -n prod | grep -i error`
2. `argocd app history api` — recent deploys (last 30 min)
3. Sentry: filter by service:api, last 1h
4. Honeycomb: `service.name = api AND http.status_code >= 500`
5. Check upstream: DB status, third-party API status pages

## Mitigate
Choose first that applies:
- `argocd app rollback api` (60s)
- `kubectl rollout undo deployment api -n prod` (30s)
- Feature flag off: `curl -X PATCH https://app.launchdarkly.com/api/v2/flags/...`
- Scale up replicas if resource-pressure: `kubectl scale deploy api --replicas=10 -n prod`

## Recover
- Watch Grafana SLI panel; should return to budget within 10 min
- `curl https://api.myorg.com/health` 200

## Escalate
- Primary: @sre-oncall
- Backup: @sre-secondary
- Service owner: #platform-eng Slack
- SEV1 only: VP Eng @vp-eng
```

### Recipe 9 — Status page (Statuspage / Better Stack)

```bash
# Atlassian Statuspage
curl -X POST https://api.statuspage.io/v1/pages/$PAGE_ID/incidents \
  -H "Authorization: OAuth $SP_TOKEN" \
  -d 'incident[name]=API Degraded&incident[status]=investigating&incident[impact]=major&incident[body]=We are investigating elevated error rates on the API.'

# Better Stack Status Page
curl -X POST https://uptime.betterstack.com/api/v2/status-pages/$PAGE_ID/status-updates \
  -H "Authorization: Bearer $BS_TOKEN" \
  -d '{"data":{"attributes":{"title":"API Degraded","body":"...","status":"investigating"}}}'
```

### Recipe 10 — Post-incident review (blameless PIR template)

```markdown
# Incident: API 5xx spike — 2026-06-09

**Severity:** SEV1
**Started:**   2026-06-09 14:23 UTC
**Detected:**  2026-06-09 14:25 UTC (TTD: 2 min)
**Mitigated:** 2026-06-09 14:31 UTC (TTM: 8 min)
**Resolved:**  2026-06-09 15:47 UTC (TTR: 1h 24m)
**Author:**    @on-call (Jane Doe)
**Customer impact:** ~12,000 requests failed during 8-minute window. ~3% of daily volume.

## Summary
A deploy at 14:20 UTC introduced a null-pointer regression in the orders endpoint, causing 5xx on ~30% of orders requests. Detected via burn-rate alert at 14:25; mitigated by `argocd app rollback` to v1.27.2 at 14:31. Root cause: missing null-check in PR #4521.

## Timeline (UTC)
- 14:20 — Deploy of v1.27.3 (PR #4521)
- 14:23 — First 5xx error in Sentry; SLI burn begins
- 14:25 — `ApiHighErrorRate` page fires (14.4× burn rate / 5min window)
- 14:26 — On-call acks; war-room opened
- 14:28 — `argocd app history api` shows v1.27.3 deploy at 14:20
- 14:31 — `argocd app rollback api 41` (to v1.27.2); pods recreating
- 14:34 — Error rate returns to baseline
- 14:40 — SLI panel green for 10min; incident downgraded to SEV2 (root cause unconfirmed)
- 15:47 — Postmortem PR opened; ROOT CAUSE confirmed; incident closed

## Root cause
PR #4521 added optional `discount` field; downstream serialization assumed non-null. Test coverage missed the empty-discount case.

## Contributing factors
- No null-check in `OrderResponse.from_dict`.
- Test fixture always had a discount.
- Canary stage skipped (deploy was urgent for the discount campaign).

## What went well
- Burn-rate alert fired within 2 min — TTD < 5 min goal.
- `argocd app rollback` worked first try — TTM < 10 min goal.
- War-room had service owner + deployer within 4 min.

## What went poorly
- Canary stage was bypassed via `--no-prompt`. Operator error, not tooling.
- The Sentry rule for new errors only triggers after 50 events; we should drop to 10 for new releases.

## Lessons learned
- Treat "urgent" deploys with MORE rigor, not less.
- Sentry alert thresholds should scale with traffic; static thresholds miss low-volume regressions.
- The runbook said "rollback to N-1"; on-call did this; runbook worked.

## Action items
| Owner | Action | Due | GitHub issue |
|---|---|---|---|
| @jane | Add null-check + test for `OrderResponse.from_dict` | 2026-06-10 | #4530 (incident-followup) |
| @platform | Lower Sentry first-seen alert threshold to 10 events for new releases | 2026-06-13 | #4531 |
| @sre  | Add `cannot-skip-canary` policy on prod ArgoCD app | 2026-06-12 | #4532 |
```

### Recipe 11 — PagerDuty CLI

```bash
pd ack 12345           # ack an incident
pd resolve 12345       # resolve
pd snooze 12345 1h     # snooze
pd schedule list       # see rotations
pd incident list --status=triggered
```

### Recipe 12 — Incident.io CLI

```bash
incident incidents create --severity SEV1 --name "API 5xx spike"
incident incidents update <id> --severity SEV2
incident incidents resolve <id>
incident postmortems generate <id>      # AI-drafted PIR (paid feature)
```

## Examples

### Example 1 — Add new service to PagerDuty rotation

**Goal:** `api` service paged via PagerDuty, escalating after 5 min.

1. PagerDuty UI → Configuration → Services → New Service: name `api`,
   integration `Prometheus`.
2. Copy integration key.
3. Add to Alertmanager config (Recipe 3).
4. Create Escalation Policy: oncall-primary → oncall-secondary (5min) →
   team (15min).
5. Set Service's Escalation Policy.
6. Test: `amtool alert add ApiHighErrorRate severity=critical service=api`.
7. Page should fire within 60s.

**Result:** Page → ack → escalate flow works end-to-end.

### Example 2 — Migrate from PagerDuty to Incident.io

**Goal:** Combined IRM + on-call in one tool.

1. Export PagerDuty rotation: `pd schedule list --json > pd-schedules.json`.
2. `incident schedules create --from-pagerduty pd-schedules.json`.
3. Update Alertmanager: replace `pagerduty_configs` → `webhook_configs`
   pointing at Incident.io.
4. Run both in parallel for 1 cycle; cut PagerDuty after 2 weeks.

**Result:** One vendor handles paging + IRM + war-rooms + PIR.

## Edge cases / gotchas

- **Don't page on raw errors** — page on burn rate (`slos-error-budgets-google-sre`).
  Raw threshold alerts are 80% false positives.
- **Pagers go off at 3 AM**; ensure every alert has `runbook_url` and a
  human-readable `summary`.
- **Acknowledge is not resolve.** Ack stops re-paging; resolve closes the
  incident. Mixing them up = unclosed incidents pile up.
- **Slack war-room timezone**: incident.io / Rootly default to UTC in
  timeline; configure user TZ for display.
- **Rotation handoff**: schedule overlaps of 30 min between primary and
  secondary; never hard cuts.
- **Manual page** during a SEV1: never solo. Always escalate to a peer
  within 15 min for cognitive backup.
- **Status page audience**: customers see public; team sees internal.
  Statuspage Subscribers vs Audience controls; misuse = leaks of in-progress
  diagnosis.
- **Mitigate before diagnose**: SEV1 = revert first, root-cause later.
  The PIR catches the diagnostic gap.
- **Burnout**: on-call rotations > 1 week without breaks = attrition. SRE
  norm: 1 week on, 5+ weeks off, plus comp.
- **TTM > TTD**: if mitigation > detection consistently, the runbook is
  wrong or missing. Quarterly review.

## Sources

- https://sre.google/sre-book/managing-incidents/ — Google SRE incident mgmt
- https://sre.google/sre-book/postmortem-culture/ — blameless PIR
- https://response.pagerduty.com/ — PagerDuty incident response guide
- https://developer.pagerduty.com/api-reference/ — PagerDuty API
- https://incident.io/guide/ — Incident.io guide
- https://incident.io/blog/postmortem-template — Incident.io PIR template
- https://docs.opsgenie.com/ — Opsgenie docs
- https://rootly.com/blog/ — Rootly blog (modern IR)
- https://grafana.com/products/oncall/ — Grafana OnCall (OSS)
- https://www.usenix.org/conference/srecon23americas — recent SREcon talks
- https://howie.ai/ — LLM-assisted PIR drafter
