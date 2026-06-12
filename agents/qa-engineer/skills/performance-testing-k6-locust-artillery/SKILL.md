<!--
Source: https://k6.io/docs/ · https://docs.locust.io/ · https://www.artillery.io/docs · https://gatling.io/docs/
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Performance Testing — k6 + Locust + Artillery

The 2026 performance toolchain: **k6** (Grafana, JS scripts, declarative
`thresholds`) is the default; **Locust** for Python shops with live web UI;
**Artillery** for Node.js with plugin ecosystem. Gatling for JVM peak
performance. CI integration centers on threshold-based fail-on-breach with
Grafana Cloud k6 or Prometheus for distributed runs.

## When to use

- New endpoint, want to know p99 latency under load
- Existing endpoint slow in prod — confirm + repro
- Pre-launch performance budget verification
- Load capacity planning (X RPS, Y concurrent users)
- Stress test before Black Friday / launch
- Trigger phrases: "load test", "k6", "Locust", "Artillery", "p99", "p95",
  "RPS", "concurrent users", "performance test", "stress test"

Do NOT use for: micro-benchmarks (use `pytest-benchmark` / `tinybench`);
single-request latency (use `curl -w`).

## Setup

```bash
# k6 — Mac / Linux
brew install k6
# Or via Docker
docker pull grafana/k6:latest

# Locust — Python
uvx locust --version
uv add --dev locust

# Artillery — Node
npm i -g artillery@latest

# Gatling — JVM
# Use sbt/maven plugin or standalone bundle from gatling.io
```

Auth: none locally. Grafana Cloud k6 / SaaS: `K6_CLOUD_TOKEN`.

## Common recipes

### Recipe 1 — k6 baseline load script

```js
// load.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },    // warm-up
    { duration: '2m',  target: 200 },   // ramp
    { duration: '5m',  target: 200 },   // steady
    { duration: '30s', target: 0 },     // ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<400', 'p(99)<800'],
    http_req_failed:   ['rate<0.01'],
    checks:            ['rate>0.99'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/users/me', {
    headers: { Authorization: `Bearer ${__ENV.TOKEN}` },
  });
  check(res, {
    'status 200': r => r.status === 200,
    'has user.id': r => JSON.parse(r.body).id !== undefined,
  });
  sleep(1);
}
```

```bash
k6 run --env TOKEN=$E2E_TOKEN load.js
k6 run --out json=results.json load.js
docker run --rm -v $PWD:/scripts grafana/k6 run /scripts/load.js
```

### Recipe 2 — k6 thresholds = CI gate

```js
export const options = {
  thresholds: {
    'http_req_duration{name:checkout}': ['p(99)<600'],   // tagged subset
    'http_req_failed':                  ['rate<0.005'],
    'iteration_duration':               ['p(95)<2000'],
  },
};
```

k6 exits non-zero on threshold breach — wire to CI to fail the build.

### Recipe 3 — Locust Python load test

```python
# locustfile.py
from locust import HttpUser, task, between, events

class APIUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://api.example.com"

    def on_start(self):
        r = self.client.post("/auth/login", json={
            "email": "loadtest@example.com",
            "password": "Test1234!",
        })
        self.token = r.json()["token"]
        self.client.headers["Authorization"] = f"Bearer {self.token}"

    @task(3)
    def get_user(self):
        with self.client.get("/users/me", catch_response=True) as r:
            if r.elapsed.total_seconds() > 0.8:
                r.failure("p99 budget exceeded")

    @task(1)
    def post_order(self):
        self.client.post("/orders", json={"product_id": 42, "qty": 1})

@events.test_stop.add_listener
def on_stop(environment, **kw):
    p99 = environment.stats.total.get_response_time_percentile(0.99)
    if p99 > 800:
        environment.process_exit_code = 1
```

```bash
uvx locust -f locustfile.py --host=https://api.example.com
uvx locust -f locustfile.py --headless -u 200 -r 20 -t 5m \
  --csv=results --html=report.html
```

### Recipe 4 — Artillery scenario YAML

```yaml
# scenario.yml
config:
  target: https://api.example.com
  phases:
    - duration: 60
      arrivalRate: 5
      rampTo: 50
      name: warm-up
    - duration: 300
      arrivalRate: 50
      name: steady
  ensure:
    p99: 800
    maxErrorRate: 1
  plugins:
    expect: {}
    metrics-by-endpoint: {}

scenarios:
  - name: browse-and-buy
    flow:
      - get:
          url: /products
          expect:
            - statusCode: 200
            - hasHeader: content-type
      - think: 2
      - post:
          url: /orders
          json: { product_id: 42, qty: 1 }
          expect:
            - statusCode: 201
```

```bash
artillery run scenario.yml --output report.json
artillery report report.json -o report.html
```

### Recipe 5 — Spike / stress / soak templates

```js
// spike.js — sudden load surge
export const options = {
  stages: [
    { duration: '10s', target: 100 },
    { duration: '1m',  target: 100 },
    { duration: '10s', target: 1400 },  // SPIKE
    { duration: '3m',  target: 1400 },
    { duration: '10s', target: 100 },
    { duration: '3m',  target: 100 },
    { duration: '10s', target: 0 },
  ],
};

// soak.js — sustained load
export const options = {
  stages: [
    { duration: '5m',  target: 400 },
    { duration: '4h',  target: 400 },     // soak
    { duration: '5m',  target: 0 },
  ],
};

// stress.js — find breakpoint
export const options = {
  stages: [
    { duration: '2m',  target: 100 },
    { duration: '5m',  target: 100 },
    { duration: '2m',  target: 200 },
    { duration: '5m',  target: 200 },
    { duration: '2m',  target: 300 },
    { duration: '5m',  target: 300 },
    { duration: '10s', target: 0 },
  ],
};
```

### Recipe 6 — CI integration (k6)

```yaml
# .github/workflows/perf.yml
on:
  pull_request: { paths: ['perf/**', 'api/**'] }
  schedule: [{ cron: '0 4 * * *' }]    # nightly

jobs:
  k6:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - name: Run k6
        uses: grafana/k6-action@v0.3.1
        with:
          filename: perf/load.js
          flags: --out json=results.json
      - uses: actions/upload-artifact@v4
        with: { name: k6-results, path: results.json }
```

### Recipe 7 — Distributed run via Grafana Cloud k6

```bash
k6 cloud login --token $K6_CLOUD_TOKEN
k6 cloud run load.js
# Or upload script + run from dashboard
```

For free open-source distributed: k6-operator on K8s.

### Recipe 8 — Browser-based perf (k6 browser module)

```js
import { browser } from 'k6/experimental/browser';
import { check } from 'k6';

export const options = {
  scenarios: {
    browser: {
      executor: 'shared-iterations',
      options: { browser: { type: 'chromium' } },
    },
  },
};

export default async function () {
  const page = browser.newPage();
  await page.goto('https://app.example.com');
  await page.locator('input[name=email]').type('user@example.com');
  await page.locator('input[name=password]').type('Test1234!');
  await Promise.all([page.locator('button[type=submit]').click(), page.waitForNavigation()]);
  check(page, { 'logged in': p => p.url().includes('/dashboard') });
  page.close();
}
```

### Recipe 9 — Reading the numbers

```
checks.....................: 99.98% ✓ 5996  ✗ 1
data_received..............: 12 MB  200 kB/s
http_req_blocked...........: avg=2.5ms  p(95)=12ms
http_req_connecting........: avg=1.2ms  p(95)=6ms
http_req_duration..........: avg=145ms  p(95)=380ms  p(99)=720ms
  { expected_response:true }.: avg=144ms  p(95)=378ms  p(99)=718ms
http_req_failed............: 0.02% ✓ 1     ✗ 5996
http_req_receiving.........: avg=0.5ms  p(95)=2ms
http_req_sending...........: avg=0.1ms  p(95)=0.3ms
http_req_waiting...........: avg=144ms  p(95)=378ms  p(99)=720ms
```

- `http_req_waiting` = server latency (this is what you tune).
- `http_req_duration` = total, including transport.
- p95 / p99 = tail; mean is misleading.

### Recipe 10 — Threshold patterns

```js
thresholds: {
  // hard fail
  http_req_duration:                ['p(99)<800'],
  http_req_failed:                  ['rate<0.01'],
  // soft warn but still fail run
  'http_req_duration{name:search}': [{ threshold: 'p(95)<300', abortOnFail: true }],
  // SLO checks
  http_reqs:                        ['rate>100'],
  iteration_duration:               ['med<1000'],
}
```

### Recipe 11 — Output to Grafana / Prometheus

```bash
k6 run --out experimental-prometheus-rw=http://prometheus:9090/api/v1/write load.js
# Grafana dashboard: import k6 dashboard ID 19665
```

## Examples

### Example 1: New endpoint perf budget

**Goal:** `POST /api/v1/orders` < 600ms p99 at 200 RPS.

1. Write `load.js` (Recipe 1 + Recipe 2 thresholds).
2. Run on staging: `k6 run --env TOKEN=... load.js`.
3. If breach, profile (DB EXPLAIN, APM trace) then iterate.
4. Once green, add to nightly CI.
5. Track p99 trend in Grafana; alert on regression > 10%.

### Example 2: Pre-launch capacity test

**Goal:** Confirm 5x baseline traffic survives launch.

1. Measure baseline RPS (Grafana / logs).
2. Stress script: ramp to 5x (Recipe 5 stress.js).
3. Observe: at what RPS does p99 break SLO?
4. Identify bottleneck (DB, cache, app pool).
5. Fix or scale; re-run.
6. Soak 4h at 1x launch load (Recipe 5 soak.js) to catch leaks.

## Edge cases / gotchas

- **Testing against prod** — never. Use staging or load-test cluster.
- **Localhost bottleneck** — local k6 caps around 30k RPS due to kernel TCP
  reuse. Use Grafana Cloud or k6-operator for higher.
- **Auth token expiration** — long runs need token refresh in `setup()` or
  per-iteration.
- **Think time = 0** is unrealistic — real users pause; `sleep(1)` minimum.
- **Connection reuse** — k6 reuses by default; if you need fresh conn per
  request set `http.options({ noConnectionReuse: true })`.
- **DNS at scale** — k6 caches DNS; if test load-balancing across IPs, use
  `discardResponseBodies` and IP list.
- **Database in test env smaller than prod** — perf results misleading;
  scale test DB or use perf-prod-clone with masked data.
- **Cold cache vs warm cache** — first iteration is slow; warm-up stage
  before measuring.
- **Logging in load test** — verbose check failures swamp stdout; use
  `--summary-export=summary.json` and inspect afterwards.
- **k6 sleep is blocking** — high think times mean lower throughput; use
  scenarios with `executor: 'constant-arrival-rate'` for fixed RPS.
- **No browser perf in k6 free distributed** — Cloud only.
- **Locust GIL** — high-contention scenarios; use `--processes=N` to fork.

## Sources

- [k6 docs](https://k6.io/docs/)
- [k6 thresholds](https://k6.io/docs/using-k6/thresholds/)
- [k6 GitHub Actions](https://github.com/grafana/k6-action)
- [Grafana Cloud k6](https://grafana.com/products/cloud/k6/)
- [Locust docs](https://docs.locust.io/)
- [Artillery docs](https://www.artillery.io/docs)
- [Gatling docs](https://gatling.io/docs/)
- [Brendan Gregg — USE method](https://www.brendangregg.com/usemethod.html)
- [Google SRE — SLO workbook](https://sre.google/workbook/implementing-slos/)
