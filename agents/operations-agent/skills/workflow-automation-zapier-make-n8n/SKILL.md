<!--
Sources: https://medium.com/@automation.labs/zapier-vs-make-vs-n8n-in-2026-where-ai-agents-actually-fit-1edbbeff85f3
         https://blog.n8n.io/best-ai-workflow-automation-tools/
         https://hatchworks.com/blog/ai-agents/n8n-vs-zapier/
n8n 2.0 (Jan 2026) — native LangChain + 70+ AI nodes; self-host = no execution limits.
Zapier 8,000+ apps; Make 3,000+; Pipedream developer-friendly.
-->
# Workflow Automation — Zapier / Make / n8n — SKILL

Build workflow automations: triggers → conditions → actions across SaaS apps. Default to **n8n self-host** for high-volume / AI-heavy / sensitive-data flows (80-90% cheaper at scale, native LangChain in n8n 2.0 Jan 2026). Use **Zapier** for breadth (8,000+ apps; non-engineer authoring). Use **Make.com** for visual scenario builds + Maia AI assistant. Pipedream for developer-friendly code+UI.

## When to use

- Need to glue 2+ SaaS apps with conditional logic.
- Need an AI agent step (n8n 2.0 LangChain).
- Recurring task on schedule.
- Webhook → multi-step fan-out.
- Trigger phrases: "Zap", "automation", "trigger when", "workflow", "n8n", "make.com scenario", "Pipedream".

## Setup

```bash
# n8n self-host (Docker)
docker volume create n8n_data
docker run -d --name n8n \
  -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD="<gen>" \
  -e N8N_HOST="n8n.example.com" \
  -e N8N_PROTOCOL=https \
  -e N8N_ENCRYPTION_KEY="<gen>" \
  -e DB_TYPE=postgresdb -e DB_POSTGRESDB_HOST=db -e DB_POSTGRESDB_DATABASE=n8n -e DB_POSTGRESDB_USER=n8n -e DB_POSTGRESDB_PASSWORD="<gen>" \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n:latest
# https://docs.n8n.io/hosting/

# Zapier
export ZAPIER_TOKEN="xxx"     # https://developer.zapier.com/
# Webhook-based; no daemon needed

# Make.com
export MAKE_TOKEN="xxx"       # https://www.make.com/en/api-documentation

# Pipedream
npm i -g @pipedream/cli
pd login
```

## Common recipes

### Recipe 1: n8n workflow JSON — Slack reminder when Notion task overdue
```json
{
  "name": "Overdue task → Slack",
  "nodes": [
    {
      "name": "Schedule",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {"rule":{"interval":[{"field":"hours","hoursInterval":1}]}}
    },
    {
      "name": "Query Notion",
      "type": "n8n-nodes-base.notion",
      "parameters": {
        "resource":"databasePage",
        "operation":"getAll",
        "databaseId":"<task-db>",
        "filters":{"property":"Due","date":{"before":"={{$now.toISO()}}"}}
      }
    },
    {
      "name": "Filter unfinished",
      "type": "n8n-nodes-base.filter",
      "parameters": {"conditions":{"string":[{"value1":"={{ $json.properties.Status.select.name }}","operation":"notEqual","value2":"Done"}]}}
    },
    {
      "name": "Post Slack",
      "type": "n8n-nodes-base.slack",
      "parameters": {
        "channel":"#ops-overdue",
        "text":"Overdue: {{ $json.properties.Name.title[0].plain_text }} (owner: {{ $json.properties.Owner.people[0].name }})"
      }
    }
  ],
  "connections": {
    "Schedule":{"main":[[{"node":"Query Notion","type":"main","index":0}]]},
    "Query Notion":{"main":[[{"node":"Filter unfinished","type":"main","index":0}]]},
    "Filter unfinished":{"main":[[{"node":"Post Slack","type":"main","index":0}]]}
  }
}
```

### Recipe 2: Import workflow JSON via n8n CLI
```bash
docker exec -it n8n n8n import:workflow --input=/data/overdue-task-slack.json
docker exec -it n8n n8n update:workflow --id=<id> --active=true
```

### Recipe 3: n8n 2.0 LangChain agent node
```json
{
  "name": "Triage incoming support emails",
  "nodes": [
    {"name":"Webhook","type":"n8n-nodes-base.webhook","parameters":{"path":"support-inbound"}},
    {
      "name":"Agent",
      "type":"@n8n/n8n-nodes-langchain.agent",
      "parameters":{
        "model":"claude-sonnet-4-5",
        "systemMessage":"You are a triage assistant. Classify into [billing, technical, sales, spam] and extract customer email + summary.",
        "tools":["calculator","searchHubspot","postLinear"]
      }
    },
    {"name":"Route by class","type":"n8n-nodes-base.switch","parameters":{"value1":"={{$json.classification}}","rules":[{"value2":"billing","output":0},{"value2":"technical","output":1},{"value2":"sales","output":2},{"value2":"spam","output":3}]}}
  ]
}
```

### Recipe 4: Zapier — webhook to multi-action zap
```bash
# Trigger a webhook-style Zap via REST
curl -X POST "https://hooks.zapier.com/hooks/catch/<account>/<zap>/" \
  -H "Content-Type: application/json" \
  -d '{
    "event":"deal_closed_won",
    "deal_amount_USD":45000,
    "customer_email":"alex@example.com",
    "owner":"sales-rep@co.com"
  }'
# Zap fans out: Slack #revenue post, HubSpot deal stage update, Notion CRM row, Gusto commission row
```

### Recipe 5: Make.com scenario blueprint
```json
{
  "name": "New-hire fanout",
  "scenario": {
    "trigger": {"app":"Rippling","event":"employee.hired"},
    "modules": [
      {"app":"GoogleWorkspace","action":"createUser","fields":{"email":"{{trigger.work_email}}","firstName":"{{trigger.first_name}}","lastName":"{{trigger.last_name}}"}},
      {"app":"Slack","action":"inviteUser","channel":"#welcome"},
      {"app":"GitHub","action":"inviteOrgMember","org":"acme","team":"engineering"},
      {"app":"Notion","action":"addPageToDatabase","db_id":"<onboarding>","props":{"Name":"{{trigger.full_name}}","Start":"{{trigger.start_date}}"}},
      {"app":"Linear","action":"createIssue","team":"ops","title":"Order laptop for {{trigger.full_name}}"}
    ]
  }
}
```

### Recipe 6: Pipedream component (code-first webhook)
```javascript
// File: components/new_hire_fanout.js
export default {
  key: "new_hire_fanout",
  version: "0.0.1",
  type: "source",
  props: {
    rippling: {type:"app",app:"rippling"},
    slack: {type:"app",app:"slack"},
  },
  async run({event}) {
    const employee = event.body;
    await this.slack.postMessage({
      channel:"#welcome",
      text:`Welcome ${employee.full_name} — starting ${employee.start_date}`
    });
  }
}
```

### Recipe 7: n8n cron at 09:00 daily — KPI digest
```json
{
  "name":"Daily KPI digest 09:00",
  "nodes":[
    {"name":"Cron","type":"n8n-nodes-base.scheduleTrigger","parameters":{"rule":{"cronExpression":"0 9 * * 1-5"}}},
    {"name":"Get Stripe MRR","type":"n8n-nodes-base.httpRequest","parameters":{"url":"https://api.stripe.com/v1/billing/...","authentication":"genericCredentialType"}},
    {"name":"Get HubSpot pipeline","type":"n8n-nodes-base.httpRequest","parameters":{"url":"https://api.hubapi.com/crm/v3/objects/deals?filterGroups=..."}},
    {"name":"Format","type":"n8n-nodes-base.code","parameters":{"jsCode":"return [{json:{summary: `MRR ${$json.mrr}; pipe ${$json.pipe}`}}];"}},
    {"name":"Slack post","type":"n8n-nodes-base.slack","parameters":{"channel":"#kpi-daily","text":"={{$json.summary}}"}}
  ]
}
```

### Recipe 8: Error handling — n8n error workflow
```json
{
  "name":"Global error handler",
  "nodes":[
    {"name":"Error trigger","type":"n8n-nodes-base.errorTrigger","parameters":{}},
    {"name":"Format error","type":"n8n-nodes-base.code","parameters":{"jsCode":"return [{json:{wfName: $json.workflow.name, err: $json.execution.error.message, time: $json.execution.startedAt}}];"}},
    {"name":"Slack alert","type":"n8n-nodes-base.slack","parameters":{"channel":"#automation-errors","text":":rotating_light: {{$json.wfName}} failed: {{$json.err}}"}}
  ]
}
```

### Recipe 9: Stage-based platform selection
```yaml
choose:
  non_engineer_authoring:
    primary: Zapier
    why: 8000+ apps; AI agents; simplest UX
  visual_builder_complex_branching:
    primary: Make.com
    why: Maia AI assistant + visual canvas + cheap per ops
  developer_team_high_volume_AI:
    primary: n8n self-host
    why: No execution caps; 80-90% cheaper at scale; native LangChain
  developer_code_first:
    primary: Pipedream
    why: JS components + free tier
  enterprise_data_pipeline:
    primary: Workato or Tray.io
    why: Enterprise SSO, governance, data-flow oriented
  personal_macOS_iOS:
    primary: Apple Shortcuts
    why: Free + cross-device
```

### Recipe 10: Cost math (n8n vs Zapier)
```python
# Crossover analysis
zapier_pro_tasks_per_mo = 2000      # Pro tier
zapier_pro_cost_USD = 49

zapier_team_tasks_per_mo = 50000
zapier_team_cost_USD = 399

n8n_self_host_cost_USD = 50         # VPS + Postgres + ops time ~ $50/mo
n8n_executions_per_mo = "unlimited"

def crossover(monthly_tasks):
    if monthly_tasks < 750:
        return "Zapier Starter ($19.99)"
    if monthly_tasks < 2000:
        return "Zapier Pro ($49)"
    if monthly_tasks < 10000:
        return "Make Core ($29) or n8n self-host ($50)"
    return "n8n self-host — Zapier would be $200-2000+/mo at this volume"
# >2k tasks/mo → n8n usually wins on cost.
```

### Recipe 11: n8n queue mode for scale
```bash
# Worker-based execution for high-throughput
docker run -d --name n8n-main -e EXECUTIONS_MODE=queue -e QUEUE_BULL_REDIS_HOST=redis ... n8nio/n8n
docker run -d --name n8n-worker-1 -e EXECUTIONS_MODE=queue -e QUEUE_BULL_REDIS_HOST=redis ... n8nio/n8n worker
docker run -d --name n8n-worker-2 ... n8nio/n8n worker
# Scales horizontally; main process dedicated to UI + webhook receive
```

## Examples

### Example 1: Hire fanout
**Goal:** New-hire row in HRIS → 7 downstream provisioning steps.
**Steps:**
1. Recipe 5 if Make/Zapier shop; Recipe 1 + Recipe 2 if n8n shop.
2. Trigger: Rippling employee.hired webhook.
3. Branches: Google Workspace, Slack, GitHub, Notion, Linear, Recipe 7 ops calendar event, Recipe 8 error handler.
4. Recipe 11 if processing > 100 hires/mo.

**Result:** Day-1 systems provisioned automatically; ops audits in #ops-fanout channel.

### Example 2: Daily KPI digest
**Goal:** 09:00 Mon-Fri Slack post with MRR + pipeline + tickets.
**Steps:**
1. Recipe 7 n8n cron workflow.
2. Stripe + HubSpot + Linear HTTP nodes.
3. Format → Slack `#kpi-daily`.

**Result:** Founder reads one message; no manual digest building.

### Example 3: AI-powered support triage (n8n 2.0)
**Goal:** Reduce manual triage on inbound.
**Steps:**
1. Recipe 3 LangChain agent node.
2. Classify; route to billing / tech / sales queues in Linear.
3. Recipe 8 catches errors to #automation-errors.

**Result:** ~70% of inbound auto-routed; humans review only flagged.

## Edge cases / gotchas

- **n8n self-host backups.** Postgres backup MANDATORY; lost workflows = lost work. Daily pg_dump → S3.
- **Zapier task billing.** "Task" = 1 successful action; filters that exit do NOT count. But polling triggers consume tasks even with no new data; switch to webhooks.
- **Make.com "operations" semantic.** Each module run = 1 op; iterators are op-heavy. Optimize by aggregating before iterators.
- **Pipedream cold starts.** Free tier components cold-start ~ 500ms; OK for human-triggered but bad for low-latency webhooks.
- **n8n encryption key loss.** If `N8N_ENCRYPTION_KEY` is lost, all stored credentials become unreadable. Back up to a password manager.
- **OAuth token expiry.** Many app integrations require periodic re-auth; build a re-auth alert in Recipe 8 error workflow.
- **Webhook DDoS.** Public webhooks should validate a shared secret (HMAC) in node-1; otherwise public endpoint = DOS target.
- **LangChain node tool selection.** Recipe 3 — give the agent only the minimum tools it needs. Over-tooling = hallucinations + costs.
- **Rate-limit per app.** HubSpot 100 req/10s, Slack 1 req/s per channel for posts, Notion 3 req/s. Chunk + sleep on bulk.
- **Data residency on hosted (Zapier/Make).** EU PII in a US-hosted Zap = GDPR transfer obligation. For EU-only flows, self-host n8n in EU region. **Defer to `legal-counsel` for binding GDPR transfer assessment.**
- **Production vs sandbox.** Build in a separate sandbox instance; promote workflow JSON to prod via Recipe 2 import. Don't edit prod live.

## Sources

- Automation Labs — Zapier vs Make vs n8n 2026: https://medium.com/@automation.labs/zapier-vs-make-vs-n8n-in-2026-where-ai-agents-actually-fit-1edbbeff85f3
- n8n blog — Best AI Workflow Tools 2026: https://blog.n8n.io/best-ai-workflow-automation-tools/
- HatchWorks — n8n vs Zapier 2026: https://hatchworks.com/blog/ai-agents/n8n-vs-zapier/
- n8n docs: https://docs.n8n.io/
- Zapier developer platform: https://platform.zapier.com/
- Make.com developer: https://www.make.com/en/api-documentation
- Pipedream docs: https://pipedream.com/docs/
- LangChain (n8n integration): https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/
