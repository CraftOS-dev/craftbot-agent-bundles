<!--
Source: https://opentelemetry.io/docs/languages/python/ · https://github.com/open-telemetry/opentelemetry-python
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# OpenTelemetry Python — Tracing, Metrics, Logs

OpenTelemetry (OTel) is the 2026 vendor-neutral standard for observability:
distributed tracing, metrics, and logs in one SDK that emits to any backend
(Honeycomb, Datadog, Sentry, Grafana, New Relic, Splunk, Elastic, AWS X-Ray).

This is the SOTA way to instrument Python services. Avoid vendor-specific
SDKs unless OpenTelemetry doesn't cover the feature.

## When to use this skill

- New service — add tracing/metrics from day 1
- Existing service with poor visibility — instrument
- "Where did this slow request spend time?" investigations
- Connecting traces across service boundaries (FastAPI calling another)
- SLO/SLI tracking
- Sentry-style error capture + breadcrumbs in production

Do NOT add OpenTelemetry when: process is short-lived (CLIs, one-off
scripts); structured logs alone suffice; latency budget is sub-millisecond
and instrumentation overhead matters.

## Setup

```bash
# Distribution package (recommended) — bundles common instrumentations
uv add opentelemetry-distro opentelemetry-exporter-otlp

# Auto-instrument popular libraries
uvx opentelemetry-bootstrap -a install
```

`opentelemetry-bootstrap -a install` detects installed packages (FastAPI,
SQLAlchemy, httpx, asyncpg, redis, etc.) and installs matching
instrumentation packages.

## Common recipes

### Recipe 1 — Zero-code auto-instrumentation

```bash
opentelemetry-instrument \
    --service_name my-app \
    --exporter_otlp_endpoint http://otel-collector:4317 \
    uv run uvicorn main:app
```

`opentelemetry-instrument` wraps any Python command. It injects spans for
every supported library — FastAPI requests, SQLAlchemy queries, httpx
calls, asyncpg queries, redis ops — automatically. Zero code changes.

### Recipe 2 — Code-based setup (explicit)

```python
# src/my_app/otel.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

def setup_otel(service_name: str, otlp_endpoint: str) -> None:
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endpoint))
    )
    trace.set_tracer_provider(provider)
```

Call once at app startup.

### Recipe 3 — Manual spans for business logic

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

async def process_order(order_id: int) -> None:
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        with tracer.start_as_current_span("validate"):
            await validate(order_id)
        with tracer.start_as_current_span("charge"):
            await charge(order_id)
        with tracer.start_as_current_span("notify"):
            await notify(order_id)
```

Show up as nested spans in the trace UI. Add domain-meaningful names — not
"step 1", "step 2".

### Recipe 4 — Metrics (counters, histograms, gauges)

```python
from opentelemetry import metrics

meter = metrics.get_meter(__name__)

request_count = meter.create_counter(
    "http.requests",
    unit="1",
    description="Total HTTP requests",
)
request_latency = meter.create_histogram(
    "http.request.duration",
    unit="ms",
    description="HTTP request latency",
)

@app.middleware("http")
async def middleware(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    request_count.add(1, {"method": request.method, "status": response.status_code})
    request_latency.record(elapsed_ms, {"method": request.method})
    return response
```

### Recipe 5 — Log correlation

```python
import logging
from opentelemetry.instrumentation.logging import LoggingInstrumentor

LoggingInstrumentor().instrument(set_logging_format=True)
# Now every log message includes trace_id + span_id
```

In your backend (Honeycomb / Datadog / etc.), filter logs by trace_id to
get logs for a specific trace. Massive uplift for debugging.

### Recipe 6 — Exception capture

```python
from opentelemetry import trace

try:
    risky()
except Exception as e:
    span = trace.get_current_span()
    span.record_exception(e)
    span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
    raise
```

The trace UI shows exceptions inline on the span; backends like Sentry/
Honeycomb correlate them with the full trace.

### Recipe 7 — FastAPI + OTel

```python
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()
FastAPIInstrumentor.instrument_app(app)
```

Auto-creates a span per request, with HTTP method, path, status code,
duration as attributes.

### Recipe 8 — SQLAlchemy + OTel

```python
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

SQLAlchemyInstrumentor().instrument(engine=engine)
```

Every query becomes a span. Combined with HTTP traces: you can see exactly
which queries each request fired and how long they took.

### Recipe 9 — Configure via env vars (12-factor)

```bash
export OTEL_SERVICE_NAME=my-app
export OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
export OTEL_RESOURCE_ATTRIBUTES="deployment.environment=prod,version=1.2.3"
export OTEL_TRACES_SAMPLER=traceidratio
export OTEL_TRACES_SAMPLER_ARG=0.1                  # sample 10%
```

OpenTelemetry SDK reads these without code changes. Standard env vars across
all OTel SDKs (Python, Go, Java, JS, etc.).

### Recipe 10 — Sentry SDK on top

```python
import sentry_sdk
from sentry_sdk.integrations.opentelemetry import SentrySpanProcessor

sentry_sdk.init(dsn=settings.sentry_dsn, traces_sample_rate=1.0)

# OR fully OTel-based: configure OTel to export to Sentry
```

Sentry has a first-class OTel integration. You get Sentry-style error
grouping + suggested fixes plus full distributed traces.

## Backend choice

| Backend | When to choose |
|---|---|
| **Honeycomb** | best-in-class trace UX; freemium tier; great for distributed systems |
| **Datadog APM** | enterprise standard; rich metrics correlation; paid |
| **Sentry Performance** | best for error-correlated traces; familiar to most devs |
| **Grafana Tempo + Loki + Prometheus** | self-hosted; open source; most flexible |
| **New Relic / Dynatrace / AppDynamics** | mature, enterprise |
| **AWS X-Ray** | AWS-native; if already in AWS |
| **Jaeger** | open source; older; simpler ops |

All accept OTLP. The choice doesn't constrain instrumentation — that's the
point of OpenTelemetry.

## Common gotchas

- **Async + threading mix**: spans use Python's `contextvars`; should work
  out of the box for asyncio, but `loop.run_in_executor` may not propagate
  context. Use `contextvars.copy_context()` if you see missing parent spans.
- **Sampling**: 100% sampling on a high-throughput service crushes the
  backend. Start at 10% (`OTEL_TRACES_SAMPLER_ARG=0.1`) and tune.
- **PII in attributes**: don't put user emails / PII in span attributes
  unless your backend supports field-level scrubbing.
- **Span attributes vs events**: short-lived state → events
  (`span.add_event(...)`); long-lived state → attributes.
- **Trace ID propagation across boundaries**: HTTP headers
  (`traceparent`, `tracestate`) — auto-injected by instrumented HTTP
  clients. Kafka headers similar.
- **Cardinality explosion**: don't put user IDs / order IDs as metric
  labels — instead, use traces with those IDs as span attributes.
- **CLI tools / batch jobs**: OTel works but use `SimpleSpanProcessor`
  (synchronous) instead of `BatchSpanProcessor` (async) so spans flush
  before exit.

## Continuous profiling (separate concern)

OpenTelemetry covers traces/metrics/logs. For continuous CPU/memory profiling
in production:

| Tool | Notes |
|---|---|
| Sentry Profiling | natively integrates with traces; correlates exception + flamegraph |
| Pyroscope | open source; great UI; py-spy under the hood |
| Datadog Continuous Profiler | bundled with Datadog APM |

These complement OTel — not replacements.

## Sources

- https://opentelemetry.io/docs/languages/python/ — Python SDK docs
- https://github.com/open-telemetry/opentelemetry-python — source
- https://github.com/open-telemetry/opentelemetry-python-contrib — contrib (auto-instrumentation)
- https://opentelemetry.io/docs/specs/otel/ — OTel spec
- https://docs.honeycomb.io/getting-data-in/opentelemetry/python/ — Honeycomb integration
- https://docs.datadoghq.com/tracing/setup_overview/open_standards/python/ — Datadog OTel
- https://docs.sentry.io/platforms/python/integrations/opentelemetry/ — Sentry OTel
