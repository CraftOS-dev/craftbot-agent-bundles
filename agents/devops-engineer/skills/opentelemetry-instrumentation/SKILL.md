<!--
Source: https://opentelemetry.io/docs/ · https://opentelemetry.io/docs/specs/otel/ · https://opentelemetry.io/docs/collector/
Authored: June 2026 for the devops-engineer agent bundle.
-->

# OpenTelemetry Instrumentation + Collector

The 2026 vendor-neutral standard for traces, metrics, and logs. Author OTel
Collector configs, deploy via Helm/Operator, choose sampling strategies,
enforce semantic conventions, and wire auto-instrumentation for Python /
Go / Node / Java / .NET. Cross-cuts the observability skill packs — this
focuses on the SDK + Collector layer; backend-specific recipes live in
`honeycomb-datadog-observability` and `prometheus-grafana-loki-tempo-self-hosted`.

## When to use

- New service — add traces/metrics from day 1.
- Existing service with poor visibility ("we can't tell where time is spent").
- Multi-backend observability (ship to Honeycomb AND Prometheus).
- Tail-based sampling (sample by trace properties, not random).
- Replacing legacy Jaeger / Zipkin instrumentation.

Skip when: workload is so short-lived that OTel startup overhead matters
(CLIs, lambdas under 50ms cold start — use simpler metric emission); or
backend specifically requires its proprietary SDK (rare).

## Setup

```bash
# Collector binary (local testing)
brew install opentelemetry-collector

# In-cluster Collector (Helm)
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts
helm upgrade --install otel-collector open-telemetry/opentelemetry-collector \
  -n observability --create-namespace \
  --set mode=deployment \
  --values otel-values.yaml

# OTel Operator (auto-instrumentation injection)
helm upgrade --install opentelemetry-operator open-telemetry/opentelemetry-operator \
  -n opentelemetry-operator-system --create-namespace \
  --set "manager.collectorImage.repository=otel/opentelemetry-collector-contrib"
```

OTLP endpoint: gRPC `4317` or HTTP `4318` — both supported.

## Common recipes

### Recipe 1 — Collector config (universal sink)

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc: { endpoint: 0.0.0.0:4317 }
      http: { endpoint: 0.0.0.0:4318 }
  prometheus:
    config:
      scrape_configs:
        - job_name: 'k8s-pods'
          kubernetes_sd_configs: [{ role: pod }]
          relabel_configs:
            - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
              action: keep
              regex: true

processors:
  batch:
    timeout: 10s
    send_batch_size: 1024
  memory_limiter:
    check_interval: 5s
    limit_percentage: 80
    spike_limit_percentage: 25
  resource:
    attributes:
      - { key: deployment.environment, value: prod, action: upsert }
      - { key: k8s.cluster.name, value: prod-us-east-1, action: insert }
  k8sattributes:
    auth_type: serviceAccount
    extract:
      metadata: [k8s.pod.name, k8s.namespace.name, k8s.node.name]
  tail_sampling:
    decision_wait: 10s
    policies:
      - name: errors
        type: status_code
        status_code: { status_codes: [ERROR] }
      - name: slow
        type: latency
        latency: { threshold_ms: 1000 }
      - name: probabilistic
        type: probabilistic
        probabilistic: { sampling_percentage: 10 }

exporters:
  otlp/honeycomb:
    endpoint: api.honeycomb.io:443
    headers: { x-honeycomb-team: ${env:HONEYCOMB_API_KEY} }
  prometheus:
    endpoint: 0.0.0.0:8889
  loki:
    endpoint: http://loki.observability:3100/loki/api/v1/push
    tls: { insecure: true }
  debug:
    verbosity: detailed

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, k8sattributes, resource, tail_sampling, batch]
      exporters: [otlp/honeycomb]
    metrics:
      receivers: [otlp, prometheus]
      processors: [memory_limiter, resource, batch]
      exporters: [prometheus]
    logs:
      receivers: [otlp]
      processors: [memory_limiter, k8sattributes, resource, batch]
      exporters: [loki]
```

```bash
otelcol-contrib --config=otel-collector-config.yaml
```

### Recipe 2 — Deploy Collector via Operator (CRD)

```yaml
apiVersion: opentelemetry.io/v1beta1
kind: OpenTelemetryCollector
metadata: { name: gateway, namespace: observability }
spec:
  mode: deployment
  replicas: 3
  image: otel/opentelemetry-collector-contrib:0.108.0
  config: |
    # paste config from Recipe 1
  resources:
    requests: { cpu: 100m, memory: 256Mi }
    limits:   { cpu: 1000m, memory: 1Gi }
```

```bash
kubectl apply -f otel-collector.yaml
kubectl get opentelemetrycollector -n observability
```

### Recipe 3 — Auto-instrumentation via Operator

```yaml
apiVersion: opentelemetry.io/v1alpha1
kind: Instrumentation
metadata: { name: default, namespace: observability }
spec:
  exporter:
    endpoint: http://gateway-collector.observability:4318
  propagators: [tracecontext, baggage, b3]
  sampler:
    type: parentbased_traceidratio
    argument: "0.1"
  python:
    env:
      - { name: OTEL_LOGS_EXPORTER, value: otlp }
  go: {}
  nodejs: {}
  java: {}
  dotnet: {}
```

```yaml
# Annotate the Deployment to opt in
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  annotations:
    instrumentation.opentelemetry.io/inject-python: "observability/default"
spec: {...}
```

Operator injects an init container that copies the SDK + sets env vars.
Zero code changes.

### Recipe 4 — Python SDK (manual setup)

```python
# src/otel.py
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource

def setup(service_name: str, env: str, endpoint: str) -> None:
    resource = Resource.create({
        "service.name": service_name,
        "service.version": "1.27.3",
        "deployment.environment": env,
    })
    # Traces
    tp = TracerProvider(resource=resource)
    tp.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
    trace.set_tracer_provider(tp)
    # Metrics
    reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=endpoint))
    metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[reader]))
```

### Recipe 5 — Env-var-only (12-factor)

```bash
export OTEL_SERVICE_NAME=api
export OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector.observability:4318
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
export OTEL_RESOURCE_ATTRIBUTES="deployment.environment=prod,service.version=1.27.3"
export OTEL_TRACES_SAMPLER=parentbased_traceidratio
export OTEL_TRACES_SAMPLER_ARG=0.1
export OTEL_LOG_LEVEL=info
```

SDK respects these without code changes — universal across languages.

### Recipe 6 — Semantic conventions for HTTP server

```python
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

@app.middleware("http")
async def middleware(request, call_next):
    with tracer.start_as_current_span(f"{request.method} {request.url.path}") as span:
        # https://opentelemetry.io/docs/specs/semconv/http/http-spans/
        span.set_attribute("http.request.method", request.method)
        span.set_attribute("url.path", request.url.path)
        span.set_attribute("server.address", request.url.hostname or "")
        span.set_attribute("user_agent.original", request.headers.get("user-agent", ""))
        response = await call_next(request)
        span.set_attribute("http.response.status_code", response.status_code)
        if response.status_code >= 500:
            span.set_status(trace.Status(trace.StatusCode.ERROR))
        return response
```

Stick to documented attribute names — backends auto-extract dashboards
when you do.

### Recipe 7 — Sampling strategies

| Strategy | When |
|---|---|
| `parentbased_always_on` | dev; debug a specific flow end-to-end |
| `parentbased_traceidratio` (0.1) | prod default; 10% sample |
| `tail_sampling` (Collector) | keep all errors + slow traces, sample rest |

Tail-based sampling in the Collector (Recipe 1) is preferred for prod —
the SDK samples nothing; Collector decides after seeing the whole trace.

### Recipe 8 — Verify the pipeline (debug exporter)

```yaml
service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [debug]
```

```bash
otelcol-contrib --config=debug.yaml
# Send a test span
curl -X POST http://localhost:4318/v1/traces -H "Content-Type: application/json" \
  -d '{"resourceSpans":[{"resource":{"attributes":[{"key":"service.name","value":{"stringValue":"test"}}]},"scopeSpans":[{"spans":[{"name":"test","kind":1,"traceId":"abcd1234abcd1234abcd1234abcd1234","spanId":"abcd1234abcd1234"}]}]}]}'
# Check stdout for the parsed span
```

### Recipe 9 — Cross-service trace propagation

```python
# Service A (client)
from opentelemetry.instrumentation.requests import RequestsInstrumentor
RequestsInstrumentor().instrument()
# All outbound requests carry `traceparent` + `tracestate` headers

# Service B (server)
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
FastAPIInstrumentor.instrument_app(app)
# Reads incoming headers; continues the trace
```

Works across languages — the `W3C TraceContext` spec is universal.

### Recipe 10 — Log correlation (trace_id in logs)

```python
import logging
from opentelemetry.instrumentation.logging import LoggingInstrumentor

LoggingInstrumentor().instrument(set_logging_format=True)
# Log lines now include trace_id=... span_id=...
```

In Honeycomb/Datadog/Loki, filter logs by `trace_id` → see all logs for a
single trace.

### Recipe 11 — Collector deployment topologies

| Topology | When |
|---|---|
| **Agent (DaemonSet)** | low-cardinality enrichment + forward to gateway |
| **Gateway (Deployment)** | aggregation, tail sampling, multi-backend fan-out |
| **Agent + Gateway** | most prod stacks — agent handles k8s metadata, gateway does sampling + export |
| **Sidecar** | per-pod (low-volume); rare for new deploys |

```yaml
# Operator with sidecar mode
apiVersion: opentelemetry.io/v1beta1
kind: OpenTelemetryCollector
metadata: { name: api-sidecar }
spec:
  mode: sidecar
  config: |
    receivers: { otlp: { protocols: { grpc: {}, http: {} } } }
    exporters: { otlp: { endpoint: gateway-collector.observability:4317 } }
    service: { pipelines: { traces: { receivers: [otlp], exporters: [otlp] } } }
```

### Recipe 12 — Validate Collector config

```bash
otelcol-contrib --config=otel-collector-config.yaml --dry-run
# OR
otelcol-validator --config=otel-collector-config.yaml
```

## Examples

### Example 1 — Add OTel to a Python FastAPI service from zero

**Goal:** Traces shipped to gateway Collector → Honeycomb.

1. `uv add opentelemetry-distro opentelemetry-exporter-otlp`.
2. `opentelemetry-bootstrap -a install` — auto-installs FastAPI/SQLAlchemy/httpx instrumentation.
3. In `Dockerfile` ENTRYPOINT, wrap:

   ```dockerfile
   ENTRYPOINT ["opentelemetry-instrument", "uvicorn", "main:app", "--host", "0.0.0.0"]
   ```

4. Env vars (Recipe 5) in K8s Deployment.
5. Deploy; `kubectl logs` shows OTel SDK startup; traces appear in Honeycomb.

**Result:** Zero code changes; full HTTP + DB + outbound HTTP traces.

### Example 2 — Migrate Jaeger client → OTel

**Goal:** Drop legacy Jaeger SDK; same Jaeger backend keeps working.

1. Replace Jaeger SDK calls with OTel SDK (Recipe 4).
2. Point Collector `exporters` to `jaeger` (yes, Jaeger backend still
   supported as OTLP receiver in 2.0+).

   ```yaml
   exporters:
     otlp/jaeger:
       endpoint: jaeger-collector.observability:4317
       tls: { insecure: true }
   ```

3. Drop the old Jaeger dep from `requirements.txt`.
4. Verify traces in Jaeger UI.

**Result:** Future backend-portable; Jaeger now optional.

## Edge cases / gotchas

- **`BatchSpanProcessor` is async + buffered.** Short-lived processes lose
  spans at exit. Use `SimpleSpanProcessor` for CLIs or call `tp.shutdown()`
  before exit.
- **Cardinality explosion in metrics**: don't use user IDs / order IDs as
  metric attributes. Use traces with those as span attributes instead.
- **`OTEL_EXPORTER_OTLP_PROTOCOL` defaults to `grpc` in Python**, `http/protobuf`
  in Node. Mismatch with Collector endpoint = silent drops.
- **`OTEL_LOG_LEVEL=debug`** prints exporter stats — invaluable for "why
  aren't traces showing up?"
- **Tail sampling needs the whole trace in one Collector**. With multiple
  gateway replicas, route by `trace_id` (use `loadbalancing` exporter to
  hash to a stable instance).
- **`memory_limiter` must be FIRST in processor pipeline.** Otherwise the
  Collector OOMs before throttling.
- **`k8sattributes` requires RBAC** to read Pod/Namespace metadata. Helm
  chart provisions this; manual installs need to grant `pods:get,list,watch`.
- **`debug` exporter** (formerly `logging`) prints to stdout — never use
  in prod, floods logs.
- **OTLP/HTTP vs OTLP/gRPC**: HTTP is fine through L7 proxies (Cloudflare,
  ALB); gRPC requires L4 or HTTP/2-aware proxy. Default to HTTP for
  cross-network.
- **Resource attributes vs span attributes**: resource attrs apply to all
  spans from the service (service.name, version); span attrs are per-span
  (http.method).
- **OTel Logs API is GA but newer than traces/metrics.** Most backends
  accept OTLP logs (Honeycomb, Datadog, Grafana Loki via OTLP).

## Sources

- https://opentelemetry.io/docs/ — OTel docs root
- https://opentelemetry.io/docs/specs/otel/ — OTel spec
- https://opentelemetry.io/docs/collector/ — Collector docs
- https://opentelemetry.io/docs/collector/configuration/ — Collector config
- https://opentelemetry.io/docs/specs/semconv/ — semantic conventions
- https://github.com/open-telemetry/opentelemetry-operator — OTel Operator (K8s)
- https://github.com/open-telemetry/opentelemetry-collector-contrib — contrib distribution
- https://opentelemetry.io/docs/specs/otel/trace/sdk/#sampling — sampling spec
- https://opentelemetry.io/blog/2024/otel-generally-available/ — Logs API GA
