<!--
Source: https://docs.honeycomb.io/ · https://docs.datadoghq.com/ · https://grafana.com/docs/grafana-cloud/
Authored: June 2026 for the devops-engineer agent bundle.
-->

# Honeycomb / Datadog / Grafana Cloud — Backend Recipes

Backend-specific configuration for OTLP-shipping observability. Same OTel
instrumentation (see `opentelemetry-instrumentation`); this skill covers
exporter config, API tokens, dashboard authoring, query languages, and
choosing between **Honeycomb** (wide-events, best traces UX), **Datadog**
(full APM/RUM/logs/synthetics — enterprise standard), and **Grafana Cloud**
(managed Mimir+Tempo+Loki+Pyroscope — best for open-source consistency).

## When to use

- "Where do I ship my OTel data?" — pick a backend.
- Dashboard authoring (Datadog dashboards, Grafana dashboards-as-code).
- Setting up custom queries / derived columns / SLO trackers in a backend.
- Cost-optimizing telemetry (Datadog billing surprises, Honeycomb event
  ingestion quotas).
- Migrating from one backend to another (OTel makes this easy).

Skip when: self-hosted everything (use
`prometheus-grafana-loki-tempo-self-hosted`); SDK-level instrumentation
problems (use `opentelemetry-instrumentation`).

## Setup

```bash
# CLI tools
brew install honeycombio/tap/honeyvent          # local event sender (debug)
brew install datadog/tools/datadog-ci           # CI integration
brew install grafana/grafana/grafana-cli        # OSS Grafana
brew install grafana/grafana/grizzly             # Grafana dashboards-as-code

# API keys (each backend's web console)
export HONEYCOMB_API_KEY="hcaek_..."
export DD_API_KEY="..."           # Datadog
export DD_APP_KEY="..."           # Datadog app key (UI ops)
export GRAFANA_CLOUD_API_KEY="glc_..."
```

Pricing snapshot (2026):
- Honeycomb: free tier 20M events/mo; Pro $130/mo; Enterprise custom.
- Datadog: $15/host/mo APM + $0.10/M log events; metrics extra.
- Grafana Cloud: free 10k series, 50 GB logs, 50 GB traces; Pro $19/user/mo.

## Common recipes

### Recipe 1 — Honeycomb via OTel Collector

```yaml
# Collector exporter
exporters:
  otlp/honeycomb-traces:
    endpoint: api.honeycomb.io:443
    headers:
      x-honeycomb-team: ${env:HONEYCOMB_API_KEY}
  otlp/honeycomb-metrics:
    endpoint: api.honeycomb.io:443
    headers:
      x-honeycomb-team: ${env:HONEYCOMB_API_KEY}
      x-honeycomb-dataset: metrics

service:
  pipelines:
    traces:  { receivers: [otlp], processors: [batch], exporters: [otlp/honeycomb-traces] }
    metrics: { receivers: [otlp], processors: [batch], exporters: [otlp/honeycomb-metrics] }
```

Dataset is the namespace; traces auto-use `service.name`, metrics need
explicit `x-honeycomb-dataset` header.

### Recipe 2 — Datadog via OTel Collector

```yaml
exporters:
  datadog:
    api:
      site: datadoghq.com           # or datadoghq.eu, us3, us5, ap1
      key: ${env:DD_API_KEY}
    metrics:
      resource_attributes_as_tags: true
    traces:
      span_name_as_resource_name: true

service:
  pipelines:
    traces:  { receivers: [otlp], processors: [batch, resource], exporters: [datadog] }
    metrics: { receivers: [otlp], processors: [batch, resource], exporters: [datadog] }
    logs:    { receivers: [otlp], processors: [batch], exporters: [datadog] }
```

Note: Datadog Agent (`datadog-agent`) is the alternative for infrastructure
metrics + system checks; Collector covers app telemetry. Many teams run
both.

### Recipe 3 — Grafana Cloud (Mimir + Tempo + Loki + Pyroscope)

```yaml
exporters:
  otlphttp/grafana:
    endpoint: https://otlp-gateway-prod-us-east-0.grafana.net/otlp
    auth: { authenticator: basicauth/grafana }

extensions:
  basicauth/grafana:
    client_auth:
      username: "${env:GRAFANA_CLOUD_INSTANCE_ID}"
      password: "${env:GRAFANA_CLOUD_API_KEY}"

service:
  extensions: [basicauth/grafana]
  pipelines:
    traces:  { receivers: [otlp], processors: [batch], exporters: [otlphttp/grafana] }
    metrics: { receivers: [otlp], processors: [batch], exporters: [otlphttp/grafana] }
    logs:    { receivers: [otlp], processors: [batch], exporters: [otlphttp/grafana] }
```

One endpoint for all three signals — Grafana Cloud routes internally.

### Recipe 4 — Honeycomb Trigger (alerting)

```yaml
# Triggers are managed in UI; declarative via Terraform provider:
resource "honeycombio_trigger" "high_latency" {
  name        = "api p95 latency > 500ms"
  dataset     = "api"
  description = "API p95 latency exceeded SLO"
  disabled    = false
  query_id    = honeycombio_query.p95_latency.id
  frequency   = 60       # check every 60s
  threshold {
    op = ">"
    value = 0.5           # 500ms in seconds
  }
  recipient { type = "slack", target = "#alerts-api" }
  recipient { type = "pagerduty", target = "PD_SERVICE_KEY" }
}
```

### Recipe 5 — Datadog monitor (Terraform)

```hcl
resource "datadog_monitor" "high_error_rate" {
  name    = "[API] 5xx error rate > 1%"
  type    = "metric alert"
  message = <<EOT
{{#is_alert}}
API error rate exceeded SLO. See runbook: https://github.com/myorg/runbooks/api/high-errors.md
{{/is_alert}}
@pagerduty-API
EOT
  query = "sum(last_5m):sum:trace.http.request.errors{service:api,env:prod}.as_count() / sum:trace.http.request.hits{service:api,env:prod}.as_count() > 0.01"
  monitor_thresholds {
    critical = 0.01
    warning  = 0.005
  }
  notify_no_data    = false
  renotify_interval = 60
  tags              = ["service:api", "team:platform"]
}
```

### Recipe 6 — Grafana dashboard-as-code (Grizzly)

```yaml
# grafana/dashboards/api.dashboard.yaml
apiVersion: grizzly.grafana.com/v1alpha1
kind: Dashboard
metadata: { name: api-overview }
spec:
  uid: api-overview
  title: API Overview
  refresh: 30s
  time: { from: now-6h, to: now }
  panels:
    - title: Request rate
      type: timeseries
      targets:
        - expr: sum(rate(http_requests_total{service="api"}[1m])) by (status_class)
          datasource: { type: prometheus, uid: prom }
```

```bash
grr apply grafana/dashboards/api.dashboard.yaml
grr diff grafana/dashboards/
grr pull -d grafana/dashboards/                 # snapshot current state
```

### Recipe 7 — Datadog dashboard JSON-as-code

```bash
datadog-ci dashboards push grafana/dashboards/*.json
datadog-ci dashboards pull --id abc-123 --destination .
```

```json
{
  "title": "API Overview",
  "widgets": [
    {
      "definition": {
        "type": "timeseries",
        "title": "Error rate",
        "requests": [
          {
            "q": "sum:trace.http.request.errors{service:api,env:prod}.as_count() / sum:trace.http.request.hits{service:api,env:prod}.as_count()",
            "display_type": "line"
          }
        ]
      }
    }
  ],
  "layout_type": "ordered"
}
```

### Recipe 8 — Honeycomb query (HoneyQL via API)

```bash
curl -X POST "https://api.honeycomb.io/1/queries/api" \
  -H "X-Honeycomb-Team: ${HONEYCOMB_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "calculations": [
      {"op": "HEATMAP", "column": "duration_ms"},
      {"op": "P95", "column": "duration_ms"}
    ],
    "filters": [{"column": "service.name", "op": "=", "value": "api"}],
    "breakdowns": ["http.target"],
    "time_range": 3600
  }'
```

UI is the primary surface; API for automation.

### Recipe 9 — Cost optimization (key strategies)

**Honeycomb**: events are billed; sample at the Collector via
`tail_sampling` (keep all errors + slow + 10% of healthy). Each span = 1
event.

**Datadog**: hosts are billed at $15/mo each for APM; log retention is
volume-based. Cut by:
- Setting `tag_cardinality_limit` on custom metrics (each tag combo = a
  metric = $$$).
- Use log indexes with retention tuning (`info` = 3d, `error` = 30d).
- `datadog-ci tag` to limit custom-metric tags.

**Grafana Cloud**: active series + log GB + trace GB. Cut active series via
`metric_relabel_configs` dropping unused labels.

### Recipe 10 — Honeycomb dataset/environment isolation

```yaml
# Per-env headers
exporters:
  otlp/honeycomb-prod:
    endpoint: api.honeycomb.io:443
    headers: { x-honeycomb-team: ${env:HC_KEY_PROD} }
  otlp/honeycomb-staging:
    endpoint: api.honeycomb.io:443
    headers: { x-honeycomb-team: ${env:HC_KEY_STAGING} }
```

Each env gets its own API key bound to its environment.

### Recipe 11 — Datadog APM live tail / search

```bash
datadog-ci trace-flame search --service api --env prod --tag "http.status_code:5xx" --duration 1h
# Or web: app.datadoghq.com → APM → Traces → query "service:api status:error"
```

### Recipe 12 — Migration: Datadog → Honeycomb (via Collector)

```yaml
# Dual-write phase
exporters:
  datadog:    { api: { key: ${DD_API_KEY} } }
  otlp/honeycomb: { endpoint: api.honeycomb.io:443, headers: { x-honeycomb-team: ${HC_KEY} } }

service:
  pipelines:
    traces: { receivers: [otlp], exporters: [datadog, otlp/honeycomb] }
```

Run dual-write for 2 weeks; build parity dashboards in Honeycomb; cut
Datadog exporter.

## Examples

### Example 1 — Wire new service to Honeycomb in <30 minutes

**Goal:** API service emitting OTLP → Honeycomb traces + metrics dataset.

1. Sign up at https://ui.honeycomb.io; get API key.
2. Add Collector exporter (Recipe 1).
3. Deploy app with `OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318`.
4. Open Honeycomb UI → Datasets → see `api` populated.
5. Build BubbleUp query: filter `status_code = 500` → see which endpoints + when.

**Result:** Traces visible, cost ~$0 on free tier.

### Example 2 — Datadog dashboards-as-code in CI

**Goal:** Every PR that changes `dashboards/*.json` updates the Datadog dashboard.

1. Author dashboard JSON (Recipe 7).
2. CI step:

   ```yaml
   - run: |
       export DATADOG_API_KEY=${{ secrets.DD_API_KEY }}
       export DATADOG_APP_KEY=${{ secrets.DD_APP_KEY }}
       datadog-ci dashboards push dashboards/*.json
   ```

3. Merge PR → Datadog UI shows updated dashboard.

**Result:** Dashboard drift eliminated; PR review on UI changes.

## Edge cases / gotchas

- **Honeycomb event = 1 span = 1 metric data point.** A trace with 50 spans
  costs 50 events. Tail-sampling at Collector is the cost knob.
- **Datadog `unifiedServiceTagging`**: set `service`, `env`, `version` as
  span attributes — Datadog UI relies on these for navigation. Set via
  `OTEL_RESOURCE_ATTRIBUTES`.
- **Datadog custom metrics cardinality**: $5/100 custom metrics per host.
  Tag explosions = surprise bills. Set `tag_cardinality_limit: 5000` on the
  Agent.
- **Grafana Cloud free tier limits**: 14-day retention for metrics, 14d for
  logs, 13 months for traces. Upgrade for longer.
- **Honeycomb sampling key**: trace_id-based — every span in a sampled trace
  is kept or dropped together. Configure in Collector `probabilistic`
  sampler with consistent hash.
- **Datadog log index quotas**: default 30 GB/day, then dropped. Set
  exclusion filters for high-volume noise (health checks, etc.).
- **OTLP/HTTP through corp proxies**: many corp proxies break HTTP/2; HTTP/1.1
  fallback via `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf` and use
  `otlphttp` exporter, not `otlp` (gRPC) in the Collector.
- **Datadog APM service catalog**: requires `dd.service` tag — set
  `service.name` resource attribute and DD Collector exporter maps it.
- **Honeycomb's BubbleUp**: works best with high-cardinality span
  attributes — emit lots of dims (user_id, plan, region) without fear; it's
  what the wide-events model is built for.
- **Grafana Cloud's Mimir labels are still Prometheus-flavored** — high
  cardinality bites. Same rules as self-hosted Prometheus.

## Sources

- https://docs.honeycomb.io/getting-data-in/opentelemetry/ — Honeycomb OTel
- https://docs.honeycomb.io/working-with-your-data/queries/ — HoneyQL
- https://docs.datadoghq.com/opentelemetry/ — Datadog OTel
- https://docs.datadoghq.com/agent/ — Datadog Agent
- https://docs.datadoghq.com/dashboards/ — Datadog dashboards
- https://grafana.com/docs/grafana-cloud/send-data/otlp/ — Grafana Cloud OTLP
- https://grafana.com/docs/grafana-cloud/cost-management-and-billing/ — Grafana billing
- https://github.com/grafana/grizzly — Grizzly (dashboards-as-code)
- https://github.com/DataDog/datadog-ci — datadog-ci CLI
- https://www.honeycomb.io/blog/honeycomb-vs-datadog — comparison post (2025)
