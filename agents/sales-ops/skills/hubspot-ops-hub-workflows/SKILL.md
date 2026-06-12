<!--
Source: https://developers.hubspot.com/docs/api/automation/workflows + https://developers.hubspot.com/docs/api/crm/properties
HubSpot Operations Hub — workflows, custom-coded actions, data sync, custom objects (June 2026 SOTA).
-->
# HubSpot Operations Hub — Workflows + Custom-Coded Actions + Data Sync — SKILL

HubSpot Operations Hub Pro/Enterprise admin: programmable Node.js custom-coded actions, workflow extensions, data sync (formerly PieSync), data quality automations (format fix, dedup recommendations), webhooks, custom objects + properties. Workflow JSON via the Automation v4 API.

## When to use

- **Build a HubSpot workflow** — stage-criteria gate, deal routing, contact enrichment trigger.
- **Custom-coded action** — Node.js logic mid-workflow (call external API, transform data).
- **Data sync mapping** — bidirectional sync between HubSpot + Salesforce / NetSuite / other.
- **Custom object** — schema beyond Contact/Company/Deal/Ticket.
- **Property creation** — custom field on standard or custom object.
- **Trigger phrases**: "build a HubSpot workflow", "custom-coded action", "data sync mapping", "HubSpot custom object", "enrich contact in workflow", "stage-criteria HubSpot".

Do NOT use this skill for: **Salesforce admin** (use `salesforce-admin-custom-fields-flows`); **enrichment vendor calls** (use `data-enrichment-zoominfo-apollo-clay`); **deduplication** (use `duplicate-mgmt-leandata-dedupe`); **HubSpot Marketing Hub workflows** (these are simpler; this skill is Operations Hub Pro/Enterprise).

## Setup

```bash
# Auth — Private App access token (Pro/Enterprise)
# In HubSpot: Settings → Integrations → Private Apps → Create
# Scopes needed: automation, crm.objects.contacts, crm.schemas.custom, crm.objects.custom

export HUBSPOT_PRIVATE_APP_TOKEN="<pat-xxx>"
export MATON_API_KEY="<key>"   # if using api-gateway proxy

# Test auth
curl "https://api.hubapi.com/crm/v3/objects/contacts?limit=1" \
  -H "Authorization: Bearer $HUBSPOT_PRIVATE_APP_TOKEN"
```

Required:
- HubSpot Sales Hub Pro/Enterprise OR Operations Hub Pro/Enterprise (for custom-coded actions + data sync)
- Operations Hub for: data sync, data quality automations, workflow extensions, snowflake/bigquery sync
- Marketing Hub Pro for: workflows on Contact + Company only (subset)

## Common recipes

### Recipe 1: Create a workflow via Automation v4 API

```bash
curl -X POST "https://api.hubapi.com/automation/v4/flows" \
  -H "Authorization: Bearer $HUBSPOT_PRIVATE_APP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Discovery to Evaluation - Champion Required",
    "type": "CONTACT_FLOW",
    "isEnabled": false,
    "objectTypeId": "0-1",
    "enrollmentCriteria": {
      "shouldReEnroll": false,
      "listFilterBranch": {
        "filterBranchType": "OR",
        "filterBranches": [{
          "filterBranchType": "AND",
          "filters": [{
            "filterType": "PROPERTY",
            "operator": {"operationType": "PROPERTY_UPDATED"},
            "property": "lifecyclestage",
            "value": "opportunity"
          }]
        }]
      }
    },
    "actions": []
  }'
```

### Recipe 2: Workflow with stage-criteria branching

```python
import requests, os

token = os.environ["HUBSPOT_PRIVATE_APP_TOKEN"]
payload = {
    "name": "Evaluation Gate — Champion + Pain Required",
    "type": "DEAL_FLOW",
    "isEnabled": True,
    "objectTypeId": "0-3",
    "enrollmentCriteria": {
        "shouldReEnroll": True,
        "listFilterBranch": {
            "filterBranchType": "AND",
            "filters": [{
                "filterType": "PROPERTY",
                "operator": {"operationType": "PROPERTY_UPDATED",
                             "valueProperty": "dealstage",
                             "expectedValue": "evaluation"},
                "property": "dealstage"
            }]
        }
    },
    "actions": [{
        "actionId": "1",
        "type": "IF_BRANCH",
        "filterBranch": {
            "filterBranchType": "OR",
            "filters": [
                {"filterType": "PROPERTY", "property": "champion_name",
                 "operator": {"operationType": "IS_EMPTY"}},
                {"filterType": "PROPERTY", "property": "identified_pain",
                 "operator": {"operationType": "IS_EMPTY"}}
            ]
        },
        "connection": {
            "matchedAction": "2",
            "nonMatchedAction": "3"
        }
    }, {
        "actionId": "2",
        "type": "SET_PROPERTY",
        "fields": {"propertyName": "deal_stage_blocked", "value": "true"}
    }, {
        "actionId": "3",
        "type": "SET_PROPERTY",
        "fields": {"propertyName": "deal_stage_blocked", "value": "false"}
    }]
}

r = requests.post("https://api.hubapi.com/automation/v4/flows",
                  headers={"Authorization": f"Bearer {token}",
                           "Content-Type": "application/json"},
                  json=payload)
print(r.status_code, r.json())
```

### Recipe 3: Custom-coded action (Node.js — enrichment in workflow)

In HubSpot UI: Workflow → Add action → Custom code → Node.js 18 → paste:

```javascript
// Operations Hub custom-coded action
const axios = require('axios');

exports.main = async (event, callback) => {
  const { domain, contactId } = event.inputFields;

  if (!domain) {
    return callback({ outputFields: { enriched: 'false' } });
  }

  // Hit Apollo via api-gateway
  try {
    const r = await axios.get(
      `https://gateway.maton.ai/apollo/api/v1/organizations/enrich?domain=${domain}`,
      { headers: { 'Authorization': `Bearer ${process.env.MATON_KEY}` } }
    );
    const d = r.data.organization || {};
    callback({
      outputFields: {
        enriched: 'true',
        industry: d.industry || '',
        employee_count: String(d.estimated_num_employees || ''),
        tech_stack: (d.technologies || []).join(',').slice(0, 1000)
      }
    });
  } catch (e) {
    callback({ outputFields: { enriched: 'false', error: e.message.slice(0,200) } });
  }
};
```

Required: define `inputFields` (domain, contactId) and `outputFields` (enriched, industry, employee_count, tech_stack) in the action config UI. Secret `MATON_KEY` via Workflows → Secrets.

### Recipe 4: Create a custom property

```bash
curl -X POST "https://api.hubapi.com/crm/v3/properties/deals" \
  -H "Authorization: Bearer $HUBSPOT_PRIVATE_APP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "champion_name",
    "label": "Champion Name",
    "type": "string",
    "fieldType": "text",
    "groupName": "dealinformation",
    "description": "Internal advocate inside the prospect org",
    "formField": false,
    "displayOrder": 5
  }'
```

### Recipe 5: Create a custom object schema

```bash
curl -X POST "https://api.hubapi.com/crm/v3/schemas" \
  -H "Authorization: Bearer $HUBSPOT_PRIVATE_APP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "champion",
    "labels": {"singular": "Champion", "plural": "Champions"},
    "primaryDisplayProperty": "name",
    "requiredProperties": ["name", "deal_id"],
    "properties": [
      {"name": "name", "label": "Name", "type": "string", "fieldType": "text"},
      {"name": "deal_id", "label": "Deal ID", "type": "string", "fieldType": "text"},
      {"name": "advocacy_score", "label": "Advocacy Score", "type": "number", "fieldType": "number"}
    ],
    "associatedObjects": ["DEAL", "CONTACT"]
  }'
```

### Recipe 6: Data sync mapping (Salesforce → HubSpot)

In HubSpot: Settings → Integrations → Data sync → Salesforce → New sync (UI-led, but API exists):

```bash
# List existing sync settings
curl "https://api.hubapi.com/crm/v3/data-sync/sync-settings" \
  -H "Authorization: Bearer $HUBSPOT_PRIVATE_APP_TOKEN"
```

Field mapping pattern (one-way Salesforce-master):
- Source: Salesforce.Account
- Target: HubSpot.Company
- Map: Name → name, BillingCountry → country, NumberOfEmployees → numberofemployees
- Conflict: "source-wins" (Salesforce master), "target-overwrites-empty" (fill blanks only)

### Recipe 7: Workflow webhook trigger (external system → HubSpot)

```bash
# Get the webhook URL for a workflow
# In HubSpot UI: Workflow → Trigger → Webhook (Ops Hub Pro+)
# URL format: https://api.hubapi.com/automation/v4/webhook-triggers/<flowId>/<token>

curl -X POST "https://api.hubapi.com/automation/v4/webhook-triggers/<flowId>/<token>" \
  -H "Content-Type: application/json" \
  -d '{"contact_email": "user@co.com", "trigger_event": "demo_completed"}'
```

### Recipe 8: Bulk property update

```python
import requests, os

token = os.environ["HUBSPOT_PRIVATE_APP_TOKEN"]
# Up to 100 records per batch
inputs = [
    {"id": "12345", "properties": {"lifecyclestage": "opportunity"}},
    {"id": "12346", "properties": {"lifecyclestage": "opportunity"}}
]
r = requests.post(
    "https://api.hubapi.com/crm/v3/objects/contacts/batch/update",
    headers={"Authorization": f"Bearer {token}",
             "Content-Type": "application/json"},
    json={"inputs": inputs}
)
print(r.status_code, r.json())
```

### Recipe 9: Find workflow by name (for editing)

```bash
curl "https://api.hubapi.com/automation/v4/flows?limit=100" \
  -H "Authorization: Bearer $HUBSPOT_PRIVATE_APP_TOKEN" \
  | jq '.results[] | select(.name | contains("Evaluation Gate"))'
```

### Recipe 10: Disable/enable workflow (rollback safety)

```bash
# Get
curl "https://api.hubapi.com/automation/v4/flows/<flowId>" \
  -H "Authorization: Bearer $HUBSPOT_PRIVATE_APP_TOKEN"

# Patch to disable
curl -X PATCH "https://api.hubapi.com/automation/v4/flows/<flowId>" \
  -H "Authorization: Bearer $HUBSPOT_PRIVATE_APP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"isEnabled": false}'
```

### Recipe 11: Property dependency tracking (before deletion)

```bash
# Find workflows referencing a property
curl "https://api.hubapi.com/automation/v4/flows?limit=100" \
  -H "Authorization: Bearer $HUBSPOT_PRIVATE_APP_TOKEN" \
  | jq '.results[] | select(.actions[] | tostring | contains("champion_name"))'

# Find reports — there's no list-reports API; use UI search OR
# Find pipeline stages using property as criteria
curl "https://api.hubapi.com/crm/v3/pipelines/deals" \
  -H "Authorization: Bearer $HUBSPOT_PRIVATE_APP_TOKEN"
```

### Recipe 12: Data quality automation (format fix)

In HubSpot UI: Operations Hub → Data Quality → Automations:
- "Format US phone numbers" → standardize to (xxx) xxx-xxxx
- "Capitalize first names" → "alice" → "Alice"
- "Trim whitespace on company names"

API listing:
```bash
curl "https://api.hubapi.com/crm/v3/automations" \
  -H "Authorization: Bearer $HUBSPOT_PRIVATE_APP_TOKEN"
```

## Examples

### Example 1: Evaluation-stage gate with champion enforcement

**Goal:** Block deals advancing to "Evaluation" stage unless Champion + Pain fields populated.

**Steps:**
1. Create `champion_name` and `identified_pain` properties (Recipe 4).
2. Create workflow JSON (Recipe 2) — enrolls deals on dealstage update → branches on empty fields → sets `deal_stage_blocked` flag.
3. Test by manually advancing a sandbox deal without champion → confirm flag fires.
4. Add a Salesforce-style "blocked" task assigned to AE in workflow continuation.
5. Enable workflow via Recipe 10.

**Result:** Same enforcement as Salesforce validation rule, applied in HubSpot.

### Example 2: Daily Apollo enrichment in workflow

**Goal:** On new contact creation, enrich with Apollo data (industry, employee count, tech stack).

**Steps:**
1. Create properties: `industry`, `employee_count`, `tech_stack` (Recipe 4).
2. Add MATON_KEY to Workflows → Secrets.
3. Create workflow: trigger "Contact created" → custom-coded action (Recipe 3) with input field `domain` from contact's email domain → write output to properties.
4. Test with 5 manual contacts before enabling broadly.

**Result:** Every new contact auto-enriched at creation; reduces SDR research time.

### Example 3: Salesforce → HubSpot company sync

**Goal:** Maintain consistent company data between Salesforce (system of record) and HubSpot (marketing automation surface).

**Steps:**
1. In HubSpot Settings → Integrations → Connect Salesforce.
2. Configure Data sync mapping (Recipe 6) with Salesforce-wins conflict resolution.
3. For each Salesforce field that should sync: define source → target mapping.
4. Validate with 10 sample accounts; check sync log for errors.
5. Enable full sync; monitor weekly.

**Result:** Marketing nurtures contacts on consistent company attributes; no manual reconciliation.

## Edge cases / gotchas

- **Operations Hub Pro vs Enterprise** — Pro gets custom-coded actions; Enterprise adds data sets + advanced data quality automations. Pricing matters for the right capability.
- **Custom-coded action runtime limits** — 20-second execution timeout, 10MB memory. Long-running external API calls fail silently if they exceed.
- **Webhook retries** — workflow webhooks retry 3 times with exponential backoff. Idempotent handlers required.
- **Data sync conflict modes** — "Most recent" mode can cause silent overwrites of correct values. Prefer explicit "source-wins" with clear directionality.
- **Property name immutability** — once created, you cannot rename a property's `name`. Only `label`. Plan naming conventions upfront.
- **Workflow enrollment volume limits** — Pro: 25K/day. Enterprise: unlimited. Bulk imports can exhaust the limit.
- **Custom objects can't have associations to all object types** — check `associatedObjects` in API; some combinations require Enterprise.
- **Workflow API JSON is fragile** — small structural changes (filterBranch nesting) cause 400 errors with cryptic messages. Use the UI to build first, then export structure.
- **Re-enrollment trap** — `shouldReEnroll: true` re-runs the workflow on every property update, can cause infinite loops if action also updates that property. Add filter `dealstage IS_KNOWN` to suppress.
- **Pipeline stage IDs are slugified labels, not stable IDs** — `evaluation` not `db-uuid`. Rename a stage → workflow breaks.
- **Marketing Hub workflows can't trigger on Deal updates** — that's an Ops Hub or Sales Hub Pro+ feature.
- **Secrets in custom-coded actions are workflow-scoped** — created via Workflows → Manage actions → Secrets. Not API-managed.
- **API rate limits** — 100 req/10s per portal (Pro), 150 (Enterprise). Bulk batch endpoints help.
- **Custom object property edit lag** — schema changes take up to 60s to propagate. Don't test immediately.
- **Sandboxing** — HubSpot Enterprise gets sandbox portals. Pro doesn't; test workflows in `isEnabled: false` mode with single test contact.
- **OAuth vs Private App** — Private App tokens don't expire; OAuth refresh tokens do. Production: Private App.

## Sources

- [HubSpot Automation v4 API (Workflows)](https://developers.hubspot.com/docs/api/automation/workflows)
- [HubSpot Custom Code Workflow Actions](https://developers.hubspot.com/docs/api/automation/custom-code-actions)
- [HubSpot CRM Properties API](https://developers.hubspot.com/docs/api/crm/properties)
- [HubSpot Custom Objects API](https://developers.hubspot.com/docs/api/crm/crm-custom-objects)
- [HubSpot Data Sync](https://developers.hubspot.com/docs/api/crm/data-sync)
- [HubSpot Private Apps](https://developers.hubspot.com/docs/api/private-apps)
- [Operations Hub Pricing + Features](https://www.hubspot.com/products/operations)
- [HubSpot API Rate Limits](https://developers.hubspot.com/docs/api/usage-details)
