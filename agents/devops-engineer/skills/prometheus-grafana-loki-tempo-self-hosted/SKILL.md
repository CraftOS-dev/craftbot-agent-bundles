<!--
Source: https://github.com/prometheus-operator/kube-prometheus · https://grafana.com/oss/ · https://vector.dev/
Authored: June 2026 for the devops-engineer agent bundle.
-->

# Self-Hosted Observability: Prometheus + Grafana + Loki + Tempo + Mimir + Vector

The 2026 open-source observability stack: **kube-prometheus-stack** (CNCF
Prometheus + Grafana + Alertmanager), **Loki** (logs), **Tempo** (traces),
**Mimir** (HA long-term Prometheus-compatible metrics), **Pyroscope**
(continuous profiling), **Vector** (Rust log/metric router replacing
Fluentd/Fluent Bit). All glued via Grafana for unified UX. Best when an
org needs full control over telemetry data + zero vendor lock-in.

## When to use

- "We can't ship telemetry to a SaaS for compliance/cost reasons."
- Multi-cluster fleet (5+ K8s clusters) — Mimir for centralized metrics.
- Petabyte-scale logs — Loki's object-store backend > Elasticsearch.
- Distributed tracing without a paid backend.
- Migrating off ELK / Splunk / Datadog for cost.

Skip when: small team (use Grafana Cloud free tier or Honeycomb); compliance
allows SaaS (use `honeycomb-datadog-observability` — lower ops load).

## Setup

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add vector https://helm.vector.dev
helm repo update

# Core stack
helm upgrade --install kps prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace -f kps-values.yaml --version 65.x

# Logs
helm upgrade --install loki grafana/loki -n logging --create-namespace -f loki-values.yaml

# Traces
helm upgrade --install tempo grafana/tempo-distributed -n tracing --create-namespace -f tempo-values.yaml

# Long-term metrics
helm upgrade --install mimir grafana/mimir-distributed -n metrics --create-namespace -f mimir-values.yaml

# Profiling
helm upgrade --install pyroscope grafana/pyroscope -n profiling --create-namespace

# Log router
helm upgrade --install vector vector/vector -n logging -f vector-values.yaml \
  --set role=Agent
```

Hardware floor: 3-node K8s cluster, 16 CPU / 32 GB RAM total for Loki+Tempo
+Mimir+Pyroscope minimums.

## Common recipes

### Recipe 1 — kube-prometheus-stack values

```yaml
# kps-values.yaml
prometheus:
  prometheusSpec:
    retention: 24h                   # short — Mimir does long-term
    replicas: 2
    storageSpec:
      volumeClaimTemplate:
        spec: { storageClassName: gp3, resources: { requests: { storage: 100Gi } } }
    serviceMonitorSelectorNilUsesHelmValues: false
    podMonitorSelectorNilUsesHelmValues: false
    remoteWrite:
      - url: http://mimir-distributor.metrics:8080/api/v1/push
        headers: { X-Scope-OrgID: prod }

grafana:
  adminPassword: "<from-secret>"
  persistence: { enabled: true, size: 10Gi }
  defaultDashboardsTimezone: utc
  sidecar:
    datasources: { enabled: true, label: grafana_datasource }
    dashboards:  { enabled: true, label: grafana_dashboard }

alertmanager:
  alertmanagerSpec:
    replicas: 2
    storage:
      volumeClaimTemplate:
        spec: { storageClassName: gp3, resources: { requests: { storage: 10Gi } } }
    config:
      route:
        receiver: slack-default
        group_by: [alertname, cluster, service]
        routes:
          - matchers: [severity = "critical"]
            receiver: pagerduty-prod
      receivers:
        - name: slack-default
          slack_configs:
            - api_url: ${SLACK_WEBHOOK}
              channel: '#alerts'
              text: '{{ template "slack.default.text" . }}'
        - name: pagerduty-prod
          pagerduty_configs:
            - service_key: ${PAGERDUTY_KEY}
              description: '{{ .CommonAnnotations.summary }}'
```

### Recipe 2 — ServiceMonitor (Prometheus auto-discovery)

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: api
  namespace: prod
  labels: { release: kps }    # kps's Prometheus selects on this label
spec:
  selector: { matchLabels: { app.kubernetes.io/name: api } }
  endpoints:
    - port: metrics
      path: /metrics
      interval: 30s
      relabelings:
        - sourceLabels: [__meta_kubernetes_pod_node_name]
          targetLabel: node
```

`release: kps` matches the Helm release name; Prometheus picks up
ServiceMonitors with that label.

### Recipe 3 — PrometheusRule for alerts

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata: { name: api-slo, namespace: prod, labels: { release: kps } }
spec:
  groups:
    - name: api.rules
      interval: 30s
      rules:
        - alert: ApiHighErrorRate
          expr: |
            sum(rate(http_requests_total{service="api",status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total{service="api"}[5m]))
            > 0.05
          for: 2m
          labels: { severity: critical, service: api }
          annotations:
            summary: "5xx error rate > 5% on api"
            description: "{{ $value | humanizePercentage }} of requests are 5xx"
            runbook_url: "https://github.com/myorg/runbooks/api/high-error-rate.md"
```

### Recipe 4 — Loki values (S3 backend)

```yaml
# loki-values.yaml
loki:
  auth_enabled: false
  schemaConfig:
    configs:
      - from: "2024-01-01"
        store: tsdb
        object_store: s3
        schema: v13
        index: { prefix: index_, period: 24h }
  storage:
    type: s3
    s3:
      region: us-east-1
      bucketnames: myorg-loki
  limits_config:
    retention_period: 720h           # 30d
    max_query_lookback: 720h

write:    { replicas: 3, persistence: { size: 50Gi } }
read:     { replicas: 3 }
backend:  { replicas: 3, persistence: { size: 50Gi } }
gateway:  { enabled: true, replicas: 2 }
```

### Recipe 5 — Vector agent (ship logs to Loki)

```yaml
# vector-values.yaml — DaemonSet mode
role: Agent
customConfig:
  sources:
    k8s_logs:
      type: kubernetes_logs
      glob_minimum_cooldown_ms: 500
  transforms:
    add_meta:
      type: remap
      inputs: [k8s_logs]
      source: |
        .cluster = "prod-us-east-1"
        .level = .kubernetes_labels."app.kubernetes.io/level" || "info"
  sinks:
    loki:
      type: loki
      inputs: [add_meta]
      endpoint: http://loki-gateway.logging:80
      labels:
        service: '{{ kubernetes_labels."app.kubernetes.io/name" }}'
        namespace: '{{ kubernetes.pod_namespace }}'
        cluster: '{{ cluster }}'
      encoding: { codec: json }
```

```bash
vector validate --config vector.yaml
vector --config vector.yaml --watch-config
```

### Recipe 6 — Tempo (traces via OTLP)

```yaml
# tempo-values.yaml
traces:
  otlp:
    grpc: { enabled: true }
    http: { enabled: true }
storage:
  trace:
    backend: s3
    s3:
      bucket: myorg-tempo
      endpoint: s3.amazonaws.com
      region: us-east-1
distributor: { replicas: 3 }
ingester:    { replicas: 3, persistence: { size: 50Gi } }
querier:     { replicas: 2 }
queryFrontend: { replicas: 2 }
compactor:   { replicas: 1 }
```

### Recipe 7 — Mimir (long-term metrics)

```yaml
# mimir-values.yaml
mimir:
  structuredConfig:
    common:
      storage:
        backend: s3
        s3:
          bucket_name: myorg-mimir
          region: us-east-1
    blocks_storage:
      tsdb: { dir: /data/tsdb }
    multitenancy_enabled: true
    limits:
      max_global_series_per_user: 1500000
      ingestion_rate: 25000
distributor: { replicas: 3 }
ingester:    { replicas: 3, persistentVolume: { size: 50Gi } }
querier:     { replicas: 2 }
query_frontend: { replicas: 2 }
store_gateway: { replicas: 2 }
compactor:   { replicas: 1 }
```

Prometheus `remote_write` (Recipe 1) ships to Mimir → long-term retention
(30d+) without local disk pressure.

### Recipe 8 — Grafana datasource provisioning

```yaml
# k8s ConfigMap with label `grafana_datasource: "1"`
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-datasources
  namespace: monitoring
  labels: { grafana_datasource: "1" }
data:
  datasources.yaml: |
    apiVersion: 1
    datasources:
      - name: Prometheus
        type: prometheus
        url: http://kps-kube-prometheus-stack-prometheus.monitoring:9090
        isDefault: true
      - name: Mimir
        type: prometheus
        url: http://mimir-query-frontend.metrics:8080/prometheus
        jsonData: { httpHeaderName1: 'X-Scope-OrgID' }
        secureJsonData: { httpHeaderValue1: 'prod' }
      - name: Loki
        type: loki
        url: http://loki-gateway.logging:80
      - name: Tempo
        type: tempo
        url: http://tempo-query-frontend.tracing:3100
        jsonData:
          tracesToLogsV2:
            datasourceUid: loki
            spanStartTimeShift: '-1m'
            spanEndTimeShift: '1m'
```

### Recipe 9 — Cross-correlation (Logs ↔ Traces ↔ Metrics)

In Grafana:
- Loki panel → click `trace_id` field → Tempo opens that trace.
- Tempo span → "Logs for this span" → Loki query by trace_id.
- Prometheus panel → Exemplars enabled → click data point → Tempo trace.

Requires: log lines embed `trace_id` (OTel Logging Instrumentor); Prometheus
remote_write supports exemplars (kps Prometheus ≥ v2.40).

### Recipe 10 — Pyroscope (continuous profiling)

```bash
helm upgrade --install pyroscope grafana/pyroscope -n profiling --create-namespace
```

Python app:

```python
import pyroscope
pyroscope.configure(
    application_name="api",
    server_address="http://pyroscope.profiling:4040",
    tags={"env": "prod"},
)
```

Go app: `-pyroscope.server.address=http://pyroscope.profiling:4040`. View
in Grafana → Explore → Pyroscope.

### Recipe 11 — Querying

```promql
# PromQL — request rate
sum(rate(http_requests_total{service="api"}[5m])) by (status_class)

# LogQL — error logs in last hour
{service="api", level="error"} |= "panic" | json | line_format "{{.msg}}"

# TraceQL (Tempo) — slow API traces
{ service.name = "api" && span.http.status_code = 500 } | duration > 500ms
```

### Recipe 12 — Backup + restore

```bash
# Velero handles K8s state. Object storage (S3) is the truth for Loki/Tempo/Mimir.
aws s3 sync s3://myorg-loki-prod s3://myorg-loki-dr-eu-west-1
aws s3 sync s3://myorg-mimir-prod s3://myorg-mimir-dr-eu-west-1
aws s3 sync s3://myorg-tempo-prod s3://myorg-tempo-dr-eu-west-1
```

## Examples

### Example 1 — Greenfield self-host: bootstrap full stack on EKS

**Goal:** Cluster has zero observability; need full stack in <2h.

1. Provision S3 buckets via OpenTofu (Mimir, Loki, Tempo bucket each).
2. `helm install kps prometheus-community/kube-prometheus-stack` (Recipe 1).
3. `helm install loki/tempo/mimir/vector/pyroscope` (Recipes 4-7).
4. Provision Grafana datasources (Recipe 8).
5. Add `ServiceMonitor` for `api` (Recipe 2); confirm metrics in Grafana.
6. Add OTel Collector → Tempo (Recipe 6); confirm traces in Grafana.
7. Vector picks up pod logs → Loki (Recipe 5); confirm `{service="api"}` query.

**Result:** Unified Grafana with metrics + logs + traces + profiles.

### Example 2 — Migrate from Datadog to self-hosted

**Goal:** Cut $20k/mo Datadog bill.

1. Stand up self-hosted stack on cheaper EKS (`m6i.xlarge` × 3).
2. Dual-write phase: Collector exports to BOTH Datadog and OTLP/Tempo.
3. Author all Datadog dashboards in Grafana (Grizzly diff).
4. Mirror alerts: Datadog monitors → PrometheusRule (Recipe 3).
5. 2-week parity check; cut Datadog exporter from Collector.
6. Cancel Datadog plan.

**Result:** ~$3k/mo infra cost; same signals.

## Edge cases / gotchas

- **Prometheus cardinality**: every unique label combination = 1 series.
  10k pods × 50 metrics × 5 labels = millions of series → Prometheus OOMs.
  Use `metric_relabel_configs` to drop unused labels.
- **Loki labels are NOT for high-cardinality** (user_id, trace_id) — those
  go in the log line + JSON parse via LogQL. Loki keeps a small fixed
  number of label values per stream.
- **Tempo doesn't index span attributes by default.** Use `TraceQL` for
  trace search; or enable Tempo's metrics-generator for span-derived metrics.
- **Mimir multi-tenancy via `X-Scope-OrgID`**: every write + query must
  carry the header. `multitenancy_enabled: false` for single-tenant.
- **kps Grafana defaults to ephemeral storage**; set `persistence.enabled:
  true` or lose dashboards on restart.
- **Vector vs Fluent Bit**: Vector is Rust, lower memory, modern config —
  prefer for new deployments. Fluent Bit still wins on plugin count for
  niche sources.
- **Object storage retries**: S3 throttling at high write rates. Mimir/Loki
  have built-in retries; tune `concurrency` and `flush_op_timeout`.
- **AlertManager dedup window**: by default `group_wait: 30s`, `group_interval:
  5m`. Tune for noisy alerts.
- **PrometheusRule `interval`** must be ≥ Prometheus `scrape_interval`.
- **`remoteWrite` to Mimir** doubles Prometheus memory usage (in-flight
  shards). Plan capacity.
- **Tempo storage explosions**: tail-sample at the Collector level
  (`tail_sampling` processor) — otherwise every span is stored.

## Sources

- https://github.com/prometheus-operator/kube-prometheus — kube-prometheus-stack
- https://prometheus.io/docs/prometheus/latest/configuration/configuration/ — Prometheus config
- https://grafana.com/docs/loki/latest/ — Loki docs
- https://grafana.com/docs/tempo/latest/ — Tempo docs
- https://grafana.com/docs/mimir/latest/ — Mimir docs
- https://grafana.com/docs/pyroscope/latest/ — Pyroscope docs
- https://vector.dev/docs/ — Vector docs
- https://grafana.com/docs/grafana/latest/dashboards/ — Grafana dashboards
- https://prometheus.io/docs/practices/naming/ — Prometheus naming conventions
- https://grafana.com/blog/2023/04/19/how-grafana-cloud-uses-grafana-mimir-for-its-billion-active-series-monitoring/ — Mimir at scale
