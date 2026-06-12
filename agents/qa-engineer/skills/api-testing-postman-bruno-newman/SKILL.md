<!--
Source: https://docs.usebruno.com/ · https://learning.postman.com/docs/running-collections/using-newman-cli/ · https://docs.insomnia.rest/
Authored: June 2026 for the qa-engineer agent bundle.
-->

# API Testing — Bruno + Postman + Newman + Insomnia

The 2026 API-test stack: **Bruno** (open-source, Git-native `.bru` files,
zero-telemetry) is the default for new repos; **Postman + Newman** remain
enterprise standard for workspaces / mock servers; **Insomnia** for
GraphQL-heavy. CI runs via `bru run` / `newman run` / `inso run`.

## When to use

- New service / endpoint, want a versioned smoke + regression API suite
- Postman collection inherited from another team needs CI integration
- GraphQL endpoint with complex queries / mutations
- Auth-flow chain (login → use token → logout) needs assertion
- Trigger phrases: "API test", "Bruno", "Postman", "Newman", "Insomnia",
  "collection", "REST test", "GraphQL test"

Do NOT use for: contract testing (use Pact); load testing (use k6);
unit-level assertion on API handlers (use pytest/vitest directly).

## Setup

```bash
# Bruno (default 2026)
npm i -g @usebruno/cli         # CLI
# Or download desktop app from https://www.usebruno.com/downloads

# Postman + Newman
npm i -g newman newman-reporter-htmlextra

# Insomnia
npm i -g inso

# Optional: Inquisitive HTTPie / curl wrappers
brew install httpie
```

Auth / API keys: per-environment env vars (`POSTMAN_API_KEY` for Postman Cloud
collections; otherwise none).

## Common recipes

### Recipe 1 — Bruno `.bru` request

```
# collection/orders/create_order.bru
meta {
  name: Create order
  type: http
  seq: 1
}

post {
  url: {{baseUrl}}/api/v1/orders
  body: json
  auth: bearer
}

auth:bearer {
  token: {{authToken}}
}

body:json {
  {
    "product_id": 42,
    "qty": 1
  }
}

assert {
  res.status: eq 201
  res.body.id: isNumber
  res.body.total: eq 9.99
  res.responseTime: lt 500
}

tests {
  test("returns Location header", function() {
    expect(res.getHeader("Location")).to.match(/\/orders\/\d+/);
  });
}
```

### Recipe 2 — Bruno environments

```
# collection/environments/staging.bru
vars {
  baseUrl: https://staging.api.example.com
  authToken: {{process.env.STAGING_TOKEN}}
}
```

```bash
bru run collection/ --env staging --reporter-html report.html
bru run collection/orders/ --env production --output junit.xml --format junit
```

### Recipe 3 — Bruno scripting

```
# pre-request: capture token
script:pre-request {
  const r = await bru.runRequest("auth/login");
  bru.setVar("authToken", r.body.token);
}

# post-response: chain a follow-up
script:post-response {
  bru.setVar("orderId", res.body.id);
}
```

### Recipe 4 — Postman collection + Newman run

```bash
# Run collection.json with env.json
newman run collection.json -e env.json \
  --reporters cli,htmlextra,junit \
  --reporter-htmlextra-export report.html \
  --reporter-junit-export junit.xml \
  --bail            # fail fast on first failure
```

### Recipe 5 — Postman test scripts (Chai-style)

```js
// Tests tab in Postman request
pm.test("Status code is 201", () => pm.response.to.have.status(201));
pm.test("Response under 500ms", () => pm.expect(pm.response.responseTime).to.be.below(500));

const json = pm.response.json();
pm.test("Has order id", () => pm.expect(json.id).to.be.a('number'));
pm.test("Total is 9.99", () => pm.expect(json.total).to.eql(9.99));

pm.collectionVariables.set("orderId", json.id);
```

### Recipe 6 — Insomnia request collection

```yaml
# collection.inso.yaml — Inso v2 format
type: collection.insomnia.rest/5.0
name: Orders API
requests:
  - name: Create order
    method: POST
    url: "{{ baseUrl }}/api/v1/orders"
    headers:
      Authorization: "Bearer {{ authToken }}"
      Content-Type: application/json
    body:
      mimeType: application/json
      text: '{"product_id": 42, "qty": 1}'
    tests:
      - name: status 201
        type: assertResponseStatus
        value: 201
```

```bash
inso run test "Orders API" --env staging --reporter junit > junit.xml
```

### Recipe 7 — GraphQL with Bruno

```
# collection/graphql/get_orders.bru
post {
  url: {{baseUrl}}/graphql
  body: graphql
}

body:graphql {
  query GetOrders($status: String!) {
    orders(status: $status) {
      id
      total
      status
    }
  }
}

body:graphql:vars {
  { "status": "pending" }
}

assert {
  res.status: eq 200
  res.body.data.orders: isArray
  res.body.errors: isUndefined
}
```

### Recipe 8 — Newman in CI (GitHub Actions)

```yaml
# .github/workflows/api-tests.yml
on: [pull_request]
jobs:
  newman:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm i -g newman newman-reporter-htmlextra
      - name: Run API tests
        env:
          STAGING_TOKEN: ${{ secrets.STAGING_TOKEN }}
        run: |
          newman run postman/collection.json -e postman/staging.json \
            --reporters cli,htmlextra,junit \
            --reporter-htmlextra-export report.html \
            --reporter-junit-export junit.xml
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: api-test-report, path: report.html }
      - uses: dorny/test-reporter@v1
        if: always()
        with:
          name: API Tests
          path: junit.xml
          reporter: java-junit
```

### Recipe 9 — Bruno in CI

```yaml
- name: Bruno CLI install
  run: npm i -g @usebruno/cli
- name: Run Bruno collection
  env:
    STAGING_TOKEN: ${{ secrets.STAGING_TOKEN }}
  run: |
    bru run collection/ --env staging \
      --format junit --output bruno-junit.xml \
      --reporter-html bruno-report.html
- uses: actions/upload-artifact@v4
  with: { name: bruno-report, path: bruno-report.html }
```

### Recipe 10 — Chain auth → test pattern

```
# collection/auth/login.bru — seq: 0 (runs first)
post {
  url: {{baseUrl}}/auth/login
}
body:json { { "email": "{{user}}", "password": "{{pass}}" } }
script:post-response { bru.setVar("authToken", res.body.token); }

# collection/orders/get_orders.bru — seq: 1
get { url: {{baseUrl}}/api/v1/orders }
auth:bearer { token: {{authToken}} }
```

`bru run collection/` runs sequentially per `seq:` and chains the token.

### Recipe 11 — Schema validation (response shape)

```
# Bruno
assert {
  res.body: matches schema {
    "type": "object",
    "required": ["id", "total"],
    "properties": {
      "id": { "type": "number" },
      "total": { "type": "number", "minimum": 0 }
    }
  }
}
```

```js
// Postman
const schema = { /* JSON Schema */ };
pm.test("Schema valid", () => pm.response.to.have.jsonSchema(schema));
```

### Recipe 12 — Data-driven runs (CSV iterations)

```bash
# Newman with CSV
newman run collection.json -e env.json -d testdata.csv --iteration-count 50

# Bruno
bru run collection/test_with_data.bru --env staging --csv testdata.csv
```

`testdata.csv`:
```csv
email,password,expectedStatus
alice@example.com,Test1234!,200
bob@example.com,wrong,401
```

## Examples

### Example 1: Bootstrap API tests in new repo

**Goal:** API has 10 endpoints; want CI gate within 1 day.

1. `mkdir api-tests && cd api-tests && bru init`
2. Add `environments/staging.bru` with `baseUrl` + token via env var.
3. Add `auth/login.bru` → captures token.
4. For each endpoint, write `.bru` with assertions (Recipe 1).
5. Wire Bruno into CI (Recipe 9).
6. Commit + open PR.

### Example 2: Migrate Postman → Bruno

**Goal:** Move existing Postman team off Postman Cloud (telemetry concern).

1. Export Postman collection v2.1 + environment JSON.
2. `bru import postman collection.json --output bruno-collection/`
3. Verify Bruno scripting equivalents (`pm.test()` → Bruno `tests {}`).
4. Add to Git; CI now uses `bru run`.
5. Sunset Postman workspace after 1 sprint of dual-run.

## Edge cases / gotchas

- **Secrets in `.bru` / Postman exports** — never commit raw tokens. Use
  `{{process.env.X}}` (Bruno) / `{{X}}` resolved from env file.
- **Newman + Postman version mismatch** — keep Newman within one minor
  version of Postman app to avoid feature breakage.
- **Postman Cloud telemetry** — Bruno wins for privacy-sensitive shops;
  Postman has telemetry opt-out but data still uploaded to Postman API
  by default.
- **Postman Pre-request `setTimeout`** is sandboxed — use `setTimeout` in
  combination with `pm.sendRequest` not `setImmediate`.
- **GraphQL errors return 200** — assert `res.body.errors === undefined`,
  not just status.
- **File uploads** — Bruno uses `body: multipart-form`; Postman uses
  form-data. Both need a file path that exists in CI.
- **Chained requests outside collection order** — Bruno respects `seq:`
  in folder; Newman respects array order in JSON.
- **Long-running async APIs** — poll with `bru.runRequest()` in script
  with retry; or use `pm.test.async`.
- **Insomnia v8 vs v9** — v9 introduces breaking changes to plugins. Pin
  `inso` version in CI.
- **HAR import** — Bruno + Postman can import HAR captures for replay; useful
  for reproducing browser-generated requests.
- **Mock servers** — Postman has built-in mock; Bruno relies on external
  (msw, WireMock). Mockoon is a good companion.

## Sources

- [Bruno docs](https://docs.usebruno.com/)
- [Bruno CLI](https://docs.usebruno.com/bru-cli/overview)
- [Postman docs](https://learning.postman.com/docs/)
- [Newman CLI](https://learning.postman.com/docs/running-collections/using-newman-cli/running-collections-on-the-command-line/)
- [newman-reporter-htmlextra](https://github.com/DannyDainton/newman-reporter-htmlextra)
- [Insomnia docs](https://docs.insomnia.rest/)
- [Inso CLI](https://docs.insomnia.rest/inso-cli/introduction)
- [GraphQL testing best practices](https://graphql.org/learn/best-practices/)
- [Mockoon mock servers](https://mockoon.com/)
