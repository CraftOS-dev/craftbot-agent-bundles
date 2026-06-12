<!--
Sources: https://blog.tooljet.com/appsmith-vs-budibase-vs-tooljet/
         https://www.openhelm.ai/blog/retool-vs-budibase-vs-appsmith-internal-ai-tools
         https://openalternative.co/alternatives/retool
ToolJet = "best Retool OSS alt 2026" — AI-native, Python.
Budibase = no-code + auto CRUD.
Retool = polished + expensive.
-->
# Internal Tools — Retool / ToolJet / Budibase — SKILL

Build internal CRUD tools, dashboards, approval queues, customer-support consoles, ops cockpits. Recommends per-stage: Retool for engineering teams with budget; ToolJet (open-source, AI-native, Python) for the 2026 OSS sweet spot; Budibase for fastest no-code CRUD + built-in DB; Appsmith for JS-heavy code-first OSS.

## When to use

- User wants a **CRUD admin panel** over Postgres / MySQL / Mongo / Snowflake / REST.
- A team needs an **approval queue, refund console, customer-service tool, ops dashboard**.
- Self-host vs hosted decision.
- Trigger phrases: "internal tool", "admin panel", "dashboard", "ops cockpit", "refund tool", "support console", "no-code tool", "Retool", "ToolJet", "Budibase", "Appsmith".

## Setup

```bash
# Retool — cloud-hosted (paid) or self-host (Enterprise)
export RETOOL_API_TOKEN="xxx"           # https://docs.retool.com
npm i -g @retool/cli                    # https://www.npmjs.com/package/@retool/cli
retool login

# ToolJet — open source, self-host
docker run -d \
  --name tooljet \
  -p 80:80 \
  -e SECRET_KEY_BASE="<gen>" \
  -e PG_HOST=db -e PG_DB=tooljet_prod -e PG_USER=postgres -e PG_PASS=postgres \
  tooljet/tooljet-ce:latest
# https://docs.tooljet.com/docs/setup/docker

# Budibase — open source, self-host (Docker single binary)
docker run -d --name budibase -p 10000:80 \
  -v bb_data:/data budibase/budibase:latest
# https://docs.budibase.com/docs/self-host-with-docker

# Appsmith — open source, self-host
curl -L "https://raw.githubusercontent.com/appsmithorg/appsmith/release/deploy/docker/docker-compose.yml" -o docker-compose.yml
docker compose up -d
# https://docs.appsmith.com/
```

## Common recipes

### Recipe 1: Retool CLI — create a new app
```bash
retool create-app --name "Refund Console" --template blank
retool import --file refund_console.json
retool deploy --app refund-console --env production
```

### Recipe 2: ToolJet — connect Postgres + auto-generate CRUD
```yaml
# ToolJet datasource config
datasources:
  - kind: postgres
    name: prod_db
    options:
      host: db.example.com
      port: 5432
      database: prod
      username: tooljet_readonly
      password: ${TOOLJET_DB_PASS}
      ssl_enabled: true
# Then in builder: query.runs(prod_db, "SELECT * FROM customers WHERE id = {{textinput1.value}}")
```

### Recipe 3: Budibase — auto-generated CRUD from table
```bash
# Via Budibase API — pin a screen to a table
curl -X POST "http://localhost:10000/api/applications/<app>/screens" \
  -H "x-budibase-api-key: $BUDIBASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Customers","table":"customers","template":"crud_grid"}'
```

### Recipe 4: Retool component template (refund approval)
```json
{
  "name": "Refund Console",
  "components": [
    {"type":"Input","id":"orderId","label":"Order ID"},
    {"type":"Button","id":"lookup","label":"Look up","onClick":"queries.getOrder.run()"},
    {"type":"Table","id":"orderTable","data":"{{queries.getOrder.data}}"},
    {"type":"Input","id":"refundAmount","label":"Refund $","type":"number"},
    {"type":"Select","id":"reason","options":["Defective","Wrong item","Customer changed mind","Other"]},
    {"type":"Textarea","id":"notes","label":"Internal notes"},
    {"type":"Button","id":"submit","label":"Submit refund","onClick":"queries.refundOrder.run()","confirmation":{"text":"Approve $<<{{refundAmount.value}}>>?"}}
  ],
  "queries": [
    {"name":"getOrder","resource":"prod_db","sql":"SELECT * FROM orders WHERE id = {{orderId.value}}"},
    {"name":"refundOrder","resource":"stripe_api","method":"POST","url":"/v1/refunds","body":{"charge":"{{orderTable.selectedRow.charge_id}}","amount":"{{refundAmount.value*100}}"}}
  ]
}
```

### Recipe 5: Role-based access control (RBAC) per tool
```yaml
# ToolJet group permissions
groups:
  - name: support-tier1
    apps: ['refund-console']
    actions: [view, run_queries]
    data_query_restrictions:
      - "refund_amount <= 50"
  - name: support-lead
    apps: ['refund-console', 'cancellation-console']
    actions: [view, run_queries, approve]
    data_query_restrictions: []
  - name: admin
    apps: ['*']
    actions: ['*']
```

### Recipe 6: Audit trail wrapping
```python
# Retool Query: log every refund to audit_log table BEFORE executing
# In refundOrder query, set: transformer
def beforeRun(orderId, refundAmount, user):
    # POST to audit endpoint
    requests.post('https://api.internal/audit',
        json={
          'actor': user['email'],
          'action': 'refund',
          'target_id': orderId,
          'amount': refundAmount,
          'tool': 'retool:refund-console',
          'ts': datetime.utcnow().isoformat(),
        })
```

### Recipe 7: SSO setup (Retool)
```bash
# Configure SAML SSO via Okta
retool sso configure \
  --type saml \
  --idp-metadata-url https://<org>.okta.com/app/<id>/sso/saml/metadata \
  --group-attribute groups
# Group mapping: Okta group "Retool-Support" → Retool group "support-tier1"
```

### Recipe 8: ToolJet AI integration (2026)
```javascript
// ToolJet 3.x supports first-class AI nodes for prompt-driven steps
queries.summarizeOrder = {
  kind: "anthropic",
  options: {
    model: "claude-sonnet-4-5",
    prompt: "Summarize this order in 2 lines for the support agent: {{orderTable.selectedRow}}",
    max_tokens: 200
  }
}
```

### Recipe 9: Budibase — embeddable internal portal
```bash
# Generate a signed embed URL for a partner-facing dashboard
curl -X POST "http://localhost:10000/api/applications/<app>/embed" \
  -H "x-budibase-api-key: $BUDIBASE_API_KEY" \
  -d '{"context":{"customerId":"123"},"ttl_seconds":3600}'
```

### Recipe 10: Stage-by-stage tool selection
```yaml
choose:
  pre_pmf_under_25_users:
    primary: Budibase  # fastest, free, no eng required
    alt: ToolJet
  growth_25_to_100_users_eng_team:
    primary: ToolJet self-host  # AI nodes + Python + no per-user fees
    alt: Retool (if budget) or Appsmith (if pure JS shop)
  scale_100plus_users_need_polish:
    primary: Retool
    alt: ToolJet Cloud
  airtable_first_no_eng:
    primary: Softr or Stacker (Airtable wrappers)
    alt: Glide
```

### Recipe 11: Component library starter pack
```json
{
  "patterns": {
    "approval_queue": ["Table","ApproveButton","RejectButton","NotesInput","AuditLog"],
    "customer_support_console": ["SearchBar","CustomerCard","OrderTable","NotesInput","SendEmailButton"],
    "ops_dashboard": ["KPICards","TimeSeriesChart","TopNTable","FilterDateRange"],
    "data_entry": ["Form","ValidationRules","SubmitButton","SuccessToast"],
    "lookup_and_action": ["Input","LookupButton","ResultPanel","ActionButton"]
  }
}
```

## Examples

### Example 1: Refund console for 5-person support team
**Goal:** Stop writing manual Stripe refunds.
**Steps:**
1. Recipe 7: configure SSO on Retool.
2. Recipe 4 + Stripe API resource: build console.
3. Recipe 5: support-tier1 capped at $50; support-lead unlimited.
4. Recipe 6: audit log to internal endpoint.
5. Roll out behind feature flag.

**Result:** Support handles refunds in 30s vs 5min; auditable; capped by policy.

### Example 2: Customer-support cockpit
**Goal:** One pane joining 4 systems.
**Steps:**
1. Pick ToolJet self-host (Recipe 0).
2. Recipe 2: connect Postgres (customers).
3. Add Intercom REST resource + Stripe API + Sentry REST.
4. Recipe 11 customer_support_console pattern.
5. Recipe 8: AI summarization node for ticket triage.

**Result:** Support sees customer, last order, recent errors, last 5 conversations in one screen.

### Example 3: Ops dashboard for headcount + spend
**Goal:** Live KPI dashboard for founder.
**Steps:**
1. Budibase or Retool — pick Budibase if no eng cycles.
2. Connect Rippling + Ramp + xero.
3. Recipe 11 ops_dashboard pattern: KPI cards + TS chart + top vendors.
4. Embed in Notion via iframe (Recipe 9).

**Result:** Founder bookmarks one URL; ops never sends weekly spreadsheets again.

## Edge cases / gotchas

- **Retool per-user pricing.** $10-50/user/mo escalates fast on a support team of 30. ToolJet OSS or Budibase = $0 per user. Cost crossover ~ 20 users.
- **Self-host operational burden.** Docker, Postgres, backups, TLS, updates — eats 0.1-0.2 FTE if no one owns it. Cloud avoids this.
- **Pumping production writes.** Direct INSERT/UPDATE from an internal tool to prod DB = footgun. Always wrap through a service / API; do not give DB write creds to a UI builder.
- **Audit log gaps.** Default builders don't audit. Recipe 6 must be wired or you can't answer "who refunded X?"
- **PII in tool screens.** SOC 2 / HIPAA / PCI scope can extend into the internal tool. Mask SSN, last-4 card, full DOB unless role-required. Use role-based field-level controls (ToolJet column-masking; Retool transformer pre-redact).
- **RBAC scope creep.** "Admin" tends to widen over months. Quarterly review of who's in `admin` group; revoke aggressively.
- **AI node cost.** ToolJet/Retool AI nodes call vendor models per invocation; budget unpredictable. Cap with rate-limit + per-user daily caps.
- **Postgres read replica.** Always point internal tools at a replica, not primary. Heavy queries from a UI can lock production.
- **Embedded portal (Recipe 9) auth.** Signed embed tokens are not OAuth scopes; don't expose customer-tenant data without strict tenant filter in every query.
- **Retool Cloud + EU data.** Retool EU residency = paid Enterprise feature. For EU customer data, self-host or use ToolJet EU.

## Sources

- ToolJet Blog — Appsmith vs Budibase vs ToolJet 2026: https://blog.tooljet.com/appsmith-vs-budibase-vs-tooljet/
- OpenHelm — Retool vs Budibase vs Appsmith 2026: https://www.openhelm.ai/blog/retool-vs-budibase-vs-appsmith-internal-ai-tools
- OpenAlternative — Retool OSS Alternatives 2026: https://openalternative.co/alternatives/retool
- Retool docs: https://docs.retool.com/
- ToolJet docs: https://docs.tooljet.com/
- Budibase docs: https://docs.budibase.com/
- Appsmith docs: https://docs.appsmith.com/
