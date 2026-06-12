<!--
Source: https://docs.pact.io/ · https://pactflow.io/ · https://docs.pact.io/pact_broker/can_i_deploy
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Contract Testing — Pact + Pact Broker + can-i-deploy

Consumer-driven Pact contracts let teams ship microservices independently
without integration-test gridlock. The 2026 setup: **Pact** SDK (Node /
Python / JVM / .NET / Go) + **Pact Broker** (OSS Docker) or **PactFlow**
(hosted) + **`can-i-deploy`** as the binary release gate. Bi-directional Pact
bridges OpenAPI specs for spec-first teams.

## When to use

- Microservices: consumer + provider in separate repos / pipelines
- Eliminate end-to-end-test sync between teams
- Pre-deploy gate: "is it safe to ship to prod?"
- Spec-first team wants to compare provider response against OpenAPI
- Trigger phrases: "Pact", "contract test", "consumer-driven contract",
  "can-i-deploy", "Pact Broker", "PactFlow", "bi-directional contract"

Do NOT use for: external third-party APIs (you don't control the provider);
single-service apps (no consumer/provider split).

## Setup

```bash
# JS/TS — pact-foundation
npm i -D @pact-foundation/pact

# Python
uv add --dev pact-python

# JVM — Maven
# io.pact:pact-jvm-consumer-junit5:4.6.x

# .NET
dotnet add package PactNet

# Pact Broker (OSS, free)
docker run --name pact-broker -d -p 9292:9292 \
  -e PACT_BROKER_DATABASE_URL=postgres://... \
  pactfoundation/pact-broker:latest

# PactFlow (hosted)
# https://pactflow.io — sign up, get API token
```

Auth: `PACT_BROKER_BASE_URL`, `PACT_BROKER_TOKEN` (or `PACT_BROKER_USERNAME`
+ `PACT_BROKER_PASSWORD`).

## Common recipes

### Recipe 1 — Consumer test (JS/TS)

```js
// consumer/orders.consumer.pact.test.js
const { PactV4, MatchersV3 } = require('@pact-foundation/pact');
const { like, eachLike, integer, string, regex } = MatchersV3;
const { getOrders } = require('../src/api/orders');

const provider = new PactV4({
  consumer: 'WebApp',
  provider: 'OrdersAPI',
  dir: './pacts',
  logLevel: 'warn',
});

test('GET /orders returns a list', async () => {
  await provider
    .addInteraction()
    .given('user has 2 orders')
    .uponReceiving('a request for orders')
    .withRequest('GET', '/orders', (b) => {
      b.headers({ Accept: 'application/json' });
      b.query({ status: 'pending' });
    })
    .willRespondWith(200, (b) => {
      b.jsonBody(eachLike({
        id: integer(1),
        total: like(99.99),
        status: regex('pending|shipped|delivered', 'pending'),
      }));
    })
    .executeTest(async (mockServer) => {
      const orders = await getOrders(mockServer.url, 'pending');
      expect(orders).toHaveLength(1);
      expect(orders[0]).toHaveProperty('id');
    });
});
```

```bash
npx jest consumer/orders.consumer.pact.test.js
# Generates ./pacts/WebApp-OrdersAPI.json
```

### Recipe 2 — Consumer test (Python)

```python
# consumer/test_orders_consumer.py
import pytest
from pact import Consumer, Provider, Like, EachLike, Term
from src.api.orders import get_orders

pact = Consumer("WebApp").has_pact_with(
    Provider("OrdersAPI"),
    pact_dir="./pacts",
    log_dir="./logs/pact",
)

@pytest.fixture(scope="session", autouse=True)
def setup_pact():
    pact.start_service()
    yield
    pact.stop_service()

def test_get_orders():
    expected = {
        "id": 1,
        "total": 99.99,
        "status": Term(r"pending|shipped|delivered", "pending"),
    }
    pact.given("user has 2 orders") \
        .upon_receiving("a request for orders") \
        .with_request("GET", "/orders", query={"status": "pending"}) \
        .will_respond_with(200, body=EachLike(expected))

    with pact:
        result = get_orders(pact.uri, "pending")
        assert len(result) >= 1
```

### Recipe 3 — Publish pact to broker

```bash
# JS
npx @pact-foundation/pact-broker publish ./pacts \
  --consumer-app-version=$GIT_SHA \
  --branch=$GIT_BRANCH \
  --broker-base-url=$PACT_BROKER_BASE_URL \
  --broker-token=$PACT_BROKER_TOKEN

# Python
pact-broker publish ./pacts \
  --consumer-app-version=$GIT_SHA \
  --broker-base-url=$PACT_BROKER_BASE_URL \
  --broker-token=$PACT_BROKER_TOKEN
```

### Recipe 4 — Provider verification

```js
// provider/verify.pact.js
const { Verifier } = require('@pact-foundation/pact');

new Verifier({
  providerBaseUrl: process.env.PROVIDER_URL,        // https://staging-orders
  provider: 'OrdersAPI',
  providerVersion: process.env.GIT_SHA,
  providerVersionBranch: process.env.GIT_BRANCH,
  pactBrokerUrl: process.env.PACT_BROKER_BASE_URL,
  pactBrokerToken: process.env.PACT_BROKER_TOKEN,
  consumerVersionSelectors: [
    { mainBranch: true },
    { deployedOrReleased: true },
  ],
  publishVerificationResult: process.env.CI === 'true',
  stateHandlers: {
    'user has 2 orders': () => seedOrders(2),
    'no orders exist':   () => clearOrders(),
  },
}).verifyProvider();
```

```bash
node provider/verify.pact.js
```

### Recipe 5 — `can-i-deploy` release gate

```bash
# Consumer side — before deploying
pact-broker can-i-deploy \
  --pacticipant=WebApp \
  --version=$GIT_SHA \
  --to-environment=production \
  --broker-base-url=$PACT_BROKER_BASE_URL

# Provider side
pact-broker can-i-deploy \
  --pacticipant=OrdersAPI \
  --version=$GIT_SHA \
  --to-environment=production
```

Exit code 0 = safe to deploy. Exit code 1 = held.

### Recipe 6 — Record deployment

```bash
pact-broker record-deployment \
  --pacticipant=WebApp \
  --version=$GIT_SHA \
  --environment=production
```

### Recipe 7 — CI workflow (consumer)

```yaml
# .github/workflows/consumer.yml
jobs:
  consumer-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - name: Run consumer pact tests
        run: npx jest --testPathPattern=consumer/
      - name: Publish pact
        if: github.ref == 'refs/heads/main'
        run: |
          npx pact-broker publish ./pacts \
            --consumer-app-version=$GITHUB_SHA \
            --branch=${GITHUB_REF_NAME} \
            --broker-base-url=${{ secrets.PACT_BROKER_BASE_URL }} \
            --broker-token=${{ secrets.PACT_BROKER_TOKEN }}
      - name: Can I deploy?
        if: github.ref == 'refs/heads/main'
        run: |
          npx pact-broker can-i-deploy \
            --pacticipant=WebApp --version=$GITHUB_SHA \
            --to-environment=production \
            --broker-base-url=${{ secrets.PACT_BROKER_BASE_URL }} \
            --broker-token=${{ secrets.PACT_BROKER_TOKEN }}
```

### Recipe 8 — CI workflow (provider)

```yaml
jobs:
  pact-verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - name: Start provider locally
        run: npm run start:test &
      - run: npx wait-on http://localhost:3001
      - name: Verify pacts
        env:
          PROVIDER_URL: http://localhost:3001
          GIT_SHA: ${{ github.sha }}
          GIT_BRANCH: ${{ github.ref_name }}
          PACT_BROKER_BASE_URL: ${{ secrets.PACT_BROKER_BASE_URL }}
          PACT_BROKER_TOKEN: ${{ secrets.PACT_BROKER_TOKEN }}
        run: node provider/verify.pact.js
```

### Recipe 9 — Bi-directional contract (OpenAPI-based)

```bash
# Provider publishes OpenAPI + verification results
pactflow publish-provider-contract openapi.yaml \
  --provider=OrdersAPI \
  --provider-app-version=$GIT_SHA \
  --branch=main \
  --content-type application/yaml \
  --verification-success \
  --verification-results=openapi-test-results.json
```

### Recipe 10 — Pact Broker self-host (docker-compose)

```yaml
# docker-compose.pact.yml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: pact
      POSTGRES_USER: pact
      POSTGRES_PASSWORD: pact
  pact-broker:
    image: pactfoundation/pact-broker:latest
    ports: ["9292:9292"]
    depends_on: [postgres]
    environment:
      PACT_BROKER_DATABASE_URL: postgres://pact:pact@postgres/pact
      PACT_BROKER_BASIC_AUTH_USERNAME: admin
      PACT_BROKER_BASIC_AUTH_PASSWORD: admin
```

```bash
docker compose -f docker-compose.pact.yml up -d
# Visit http://localhost:9292
```

### Recipe 11 — Matrix view + tagging strategy

- Tag consumer versions with branch + environment: `git-feature-x`, `prod`,
  `staging`.
- Provider verification selectors pull latest of each.
- Matrix shows which consumer↔provider versions are compatible.

```bash
pact-broker create-version-tag --pacticipant=WebApp --version=$GIT_SHA --tag=prod
```

### Recipe 12 — Webhooks (auto-trigger provider verify)

```yaml
# Pact Broker webhook config — fires on new consumer pact
events:
  - name: contract_content_changed
request:
  method: POST
  url: https://api.github.com/repos/org/orders-api/dispatches
  headers:
    Authorization: Bearer ${user.GITHUB_TOKEN}
  body: |
    { "event_type": "pact-changed",
      "client_payload": { "consumer": "${pactbroker.consumerName}" } }
```

## Examples

### Example 1: New consumer + new provider

**Goal:** Set up first contract between `WebApp` and `OrdersAPI`.

1. WebApp team: write consumer test (Recipe 1); publish pact to broker.
2. OrdersAPI team: write verification (Recipe 4); run on every PR + main.
3. Wire `can-i-deploy` into both deploys (Recipe 5).
4. Add webhook for auto-verify on contract change (Recipe 12).
5. After 1 sprint: kill cross-service E2E tests that contract now covers.

### Example 2: Onboard 5th consumer to existing provider

**Goal:** New mobile app consumes `OrdersAPI`; need contract assurance.

1. Mobile team writes consumer test in their repo; publishes
   `MobileApp-OrdersAPI.json` pact.
2. OrdersAPI provider verification (Recipe 4) picks it up via
   `consumerVersionSelectors: [{ mainBranch: true }]`.
3. If verification fails: provider team adds state handler OR mobile team
   loosens matchers; iterate.
4. Once green, mobile deploys with `can-i-deploy --to-environment=production`.

## Edge cases / gotchas

- **Pacts are NOT specs** — Pact captures interactions you have, not all
  possible. For full spec coverage use OpenAPI + bi-directional Pact.
- **Provider states are state machines** — keep small. 30 states for one
  endpoint is a smell.
- **Strict matchers vs `like()`** — too strict, brittle to legit changes;
  too loose, misses contract drift. Default `like()` for values, `regex` for
  formats.
- **Order matters** — Pact won't enforce field order in JSON, but does enforce
  presence + type.
- **Consumer pacts have a SHA in the filename** — commit pacts/ to consumer
  repo or upload to broker; don't depend on the runtime-generated copy.
- **`can-i-deploy` returns success on missing data** — set `--retry-while-unknown`
  to wait for in-flight verifications.
- **Provider verifies many consumer versions** — slow if there are dozens.
  Use `consumerVersionSelectors: [{ deployedOrReleased: true }]` to bound it.
- **Pact JVM vs Pact Ruby (CLI)** — same broker; spec versions differ. Pact
  V4 is the 2026 default; older JVM defaults to V3.
- **Bi-directional Pact** — requires PactFlow (paid) or pact-broker with
  bi-directional plugin (OSS in 2026).
- **Don't pact-test third-party APIs** — they won't run your verification.
  Use schemathesis / dredd / record-replay instead.
- **Webhooks need broker auth** — guard with token; otherwise anyone can
  trigger your provider CI.
- **Pact files in Git churn noisily** — auto-generated. Either commit
  deliberately on milestone or publish to broker and gitignore.

## Sources

- [Pact docs](https://docs.pact.io/)
- [Pact specification](https://github.com/pact-foundation/pact-specification)
- [PactFlow](https://pactflow.io/)
- [Pact Broker (OSS) Docker](https://github.com/pact-foundation/pact_broker-docker)
- [can-i-deploy](https://docs.pact.io/pact_broker/can_i_deploy)
- [@pact-foundation/pact (JS)](https://github.com/pact-foundation/pact-js)
- [pact-python](https://github.com/pact-foundation/pact-python)
- [Bi-directional contracts](https://docs.pactflow.io/docs/bi-directional-contract-testing/)
- [Pact best practices](https://docs.pact.io/getting_started/best_practices)
- [Consumer-driven contracts (Fowler)](https://martinfowler.com/articles/consumerDrivenContracts.html)
