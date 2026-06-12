<!--
Source: https://developers.hubspot.com/docs/api/crm/contacts
HubSpot remote MCP (mcp.hubspot.com) went GA April 2026 with OAuth 2.1 + PKCE.
Managed OAuth proxy at gateway.maton.ai/hubspot/ wraps the same endpoints with no per-tenant OAuth dance.
-->
# HubSpot Sales MCP — SKILL

HubSpot is the default CRM for SMB and mid-market sales motions. This skill covers the CRM half of HubSpot: contacts, companies, deals, line items, owners, pipelines, lists, properties, tasks, engagements, workflows, sequences. Use the managed-OAuth proxy at `gateway.maton.ai/hubspot/` for production; fall back to direct `api.hubapi.com` only when the gateway is unavailable.

## When to use

- **Any CRM read or write** against a HubSpot portal — contacts, deals, companies, engagements, tasks, properties.
- **Pipeline review / forecast** queries — list open deals filtered by stage, owner, close date.
- **Lead scoring / lifecycle stage updates** triggered by signal data (intent, product usage, reply).
- **Enrolling a contact in a HubSpot Sequence** (Sales Hub) — the outbound-cadence side, distinct from Marketing Workflows.
- **Trigger phrases**: "update the deal", "move opp to negotiation", "pull pipeline for AE X", "enroll these 30 contacts in sequence Y", "create a follow-up task", "what's our coverage ratio".

Do NOT use this skill when: the user is doing **marketing automation** (workflows, landing pages, forms — defer to `marketing-agent` / `hubspot-crm-marketing-mcp` skill); the customer is **Salesforce-first** (use `salesforce-api` default skill); the task is **call analysis** (use `gong-chorus-call-intelligence`).

## Setup

```bash
# Managed OAuth via Maton api-gateway (preferred — no portal-by-portal OAuth)
export MATON_API_KEY="<maton-key-from-gateway.maton.ai>"
export HUBSPOT_PORTAL_ID="<portal-id-shown-in-hubspot-settings>"

# Direct HubSpot Private App fallback
# Settings → Integrations → Private Apps → Create → grant scopes → copy token
export HUBSPOT_PRIVATE_APP_TOKEN="pat-na1-..."
```

Auth requirements:
- `MATON_API_KEY` — from your Maton workspace, free tier permits 1k req/day, paid tiers higher.
- `HUBSPOT_PRIVATE_APP_TOKEN` — Private App token, free if you own the portal. Scopes required: `crm.objects.contacts.read/write`, `crm.objects.companies.read/write`, `crm.objects.deals.read/write`, `crm.lists.read/write`, `crm.schemas.deals.read`, `crm.objects.owners.read`, `sales-email-read`, `automation` (for sequences + workflows), `tickets` (optional).
- Direct API hit limit: 100 req / 10 s per token (Pro), 250k req/day (Pro), 500k/day (Enterprise).

## Common recipes

### Recipe 1: List open deals for one AE this quarter

```bash
curl -X POST "https://gateway.maton.ai/hubspot/crm/v3/objects/deals/search" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "filterGroups":[{"filters":[
      {"propertyName":"hubspot_owner_id","operator":"EQ","value":"<owner-id>"},
      {"propertyName":"dealstage","operator":"NOT_IN","values":["closedwon","closedlost"]},
      {"propertyName":"closedate","operator":"BETWEEN","value":"2026-04-01","highValue":"2026-06-30"}
    ]}],
    "properties":["dealname","amount","dealstage","closedate","hs_deal_stage_probability"],
    "limit":100
  }'
```

### Recipe 2: Update MEDDIC custom fields on a deal

```bash
curl -X PATCH "https://gateway.maton.ai/hubspot/crm/v3/objects/deals/<deal-id>" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "properties":{
      "meddic_metrics":"Reduce CAC 20% in 6 months",
      "meddic_economic_buyer":"VP Sales — Sarah Lee",
      "meddic_decision_criteria":"SOC 2; ROI > 3x; UX < 30d onboarding",
      "meddic_decision_process":"Demo → security → procurement → exec sign",
      "meddic_identify_pain":"Outbound 3% reply rate; lost $1.2M last year",
      "meddic_champion":"AE Director — Jaime Cruz (confirmed advocacy 2026-06-04)",
      "meddic_score":"15"
    }
  }'
```

### Recipe 3: Bulk update lead score from signal data

```bash
# Batch up to 100 contacts in one call
curl -X POST "https://gateway.maton.ai/hubspot/crm/v3/objects/contacts/batch/update" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs":[
      {"id":"<contact-id-1>","properties":{"lead_score":"72","last_intent_signal":"pricing-page-visit"}},
      {"id":"<contact-id-2>","properties":{"lead_score":"55","last_intent_signal":"changelog-view"}}
    ]
  }'
```

### Recipe 4: Create a follow-up task on a deal

```bash
curl -X POST "https://gateway.maton.ai/hubspot/crm/v3/objects/tasks" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "properties":{
      "hs_task_subject":"Champion silent 8d — send 1-pager + ROI calc",
      "hs_task_body":"NBA: Send ROI calculator + case study link, then book a 15-min sync.",
      "hs_timestamp":"2026-06-12T16:00:00Z",
      "hubspot_owner_id":"<owner-id>",
      "hs_task_priority":"HIGH",
      "hs_task_type":"TODO"
    },
    "associations":[{"to":{"id":"<deal-id>"},"types":[{"associationCategory":"HUBSPOT_DEFINED","associationTypeId":216}]}]
  }'
```

### Recipe 5: Enroll a contact in a Sales Hub Sequence

```bash
# Sequence IDs: GET /automation/v3/sequences
curl -X POST "https://gateway.maton.ai/hubspot/automation/v3/sequences/<sequence-id>/enrollments" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contactId":"<contact-id>",
    "senderEmail":"ae@brand.com",
    "startDate":"2026-06-10T09:00:00Z",
    "sequenceProperties":{"firstName":"Sam","companyName":"Acme"}
  }'
```

### Recipe 6: Move a deal to a new stage with an activity note

```bash
# Step 1: Patch stage
curl -X PATCH "https://gateway.maton.ai/hubspot/crm/v3/objects/deals/<deal-id>" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{"properties":{"dealstage":"presentationscheduled","hs_deal_stage_probability":"0.4"}}'

# Step 2: Log engagement note
curl -X POST "https://gateway.maton.ai/hubspot/crm/v3/objects/notes" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "properties":{"hs_note_body":"Stage moved after demo confirmed for 2026-06-15. EB attending.","hs_timestamp":"'$(date -u +%s%3N)'"},
    "associations":[{"to":{"id":"<deal-id>"},"types":[{"associationCategory":"HUBSPOT_DEFINED","associationTypeId":214}]}]
  }'
```

### Recipe 7: Dynamic list of stalled deals (age-in-stage > 30 days)

```bash
curl -X POST "https://gateway.maton.ai/hubspot/crm/v3/lists" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"Stalled — In Stage > 30d",
    "objectTypeId":"0-3",
    "processingType":"DYNAMIC",
    "filterBranch":{"filterBranchType":"AND","filters":[
      {"property":"hs_time_in_dealstage","operator":"GREATER_THAN","value":2592000000},
      {"property":"hs_is_closed","operator":"EQ","value":false}
    ]}
  }'
```

### Recipe 8: Pull last-activity-date per contact (for stale outreach detection)

```bash
curl -X POST "https://gateway.maton.ai/hubspot/crm/v3/objects/contacts/search" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "filterGroups":[{"filters":[{"propertyName":"notes_last_contacted","operator":"LT","value":"'$(date -u -d "14 days ago" +%s%3N)'"}]}],
    "properties":["email","firstname","notes_last_contacted","hs_lead_status"],
    "limit":100
  }'
```

### Recipe 9: Round-robin assign newly-created MQLs

```bash
# After form submit (MQL signal), call assignment workflow OR direct PATCH
curl -X PATCH "https://gateway.maton.ai/hubspot/crm/v3/objects/contacts/<contact-id>" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{"properties":{"hubspot_owner_id":"<rr-selected-owner-id>","hs_lead_status":"NEW","lifecyclestage":"marketingqualifiedlead"}}'
```

Owner pool query: `GET /crm/v3/owners?archived=false&limit=100`. Round-robin index stored in `postgresql-mcp` or a Notion key-value page.

### Recipe 10: Append SDR handoff package to deal

```bash
# Custom properties prefilled by the SDR
curl -X POST "https://gateway.maton.ai/hubspot/crm/v3/objects/deals" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "properties":{
      "dealname":"Acme — Outbound Q3",
      "pipeline":"default",
      "dealstage":"qualifiedtobuy",
      "amount":"45000",
      "closedate":"2026-09-30",
      "hubspot_owner_id":"<ae-owner-id>",
      "sdr_notes":"4 touches before reply. Pain: outbound 2% reply. Champion candidate: Marketing Ops Mgr.",
      "bant_budget":"$40-60K confirmed",
      "bant_authority":"VP Sales (Sarah Lee)",
      "bant_need":"Reduce CAC + reply rate",
      "bant_timeline":"Q4 close",
      "next_step":"Discovery call 2026-06-12 14:00 UTC"
    }
  }'
```

## Examples

### Example 1: Weekly pipeline review (end-to-end)

**Goal:** Pull all open deals for an AE, flag slip-risk + stalled, deliver a Notion summary + Slack ping.

**Steps:**
1. `POST /crm/v3/objects/deals/search` filtered by `hubspot_owner_id` + open stage (Recipe 1).
2. Compute age-in-stage from `hs_time_in_dealstage`; flag deals > 1.5x median for stage.
3. Compute coverage ratio: sum of `amount` ÷ quota; flag if < 3x.
4. Render Markdown table → push to Notion via `notion-mcp`; Slack ping the AE via `slack-mcp` with the top-5 slip-risk deals.

**Result:** Notion doc with pipeline + stalled + slip-risk tables; Slack DM with top-5 NBAs.

### Example 2: Auto-create a follow-up task when MEDDIC score drops

**Goal:** When a deal's MEDDIC score recomputes below 14 (Commit threshold), create a "close criteria gaps" task on the AE.

**Steps:**
1. Nightly cron pulls open deals (Recipe 1) + `meddic_score` property.
2. For each deal with score < 14 AND probability >= 0.6, create a task (Recipe 4) titled "MEDDIC gap: <lowest-scoring-field>".
3. Push a Slack DM to owner via `slack-mcp`.

**Result:** AE gets a daily, prioritized list of which MEDDIC fields to chase on which deal.

## Edge cases / gotchas

- **Custom property API names** are *not* the same as labels — the API uses `snake_case` internal name. Query `GET /crm/v3/properties/deals` once and cache the label→name map; otherwise PATCH calls silently no-op.
- **Sequence enrollment requires a connected mailbox**. The `senderEmail` must be a user who has linked their inbox (Gmail / Outlook) in HubSpot UI; otherwise you'll get `400 INVALID_SENDER`.
- **Rate limit 100 req/10s** is per OAuth app, not per portal — sharing a Maton key across many writes can throttle. Use the batch endpoints (`/batch/update` accepts 100 records/call) for any bulk loop.
- **`hs_deal_stage_probability` is not auto-computed** when you PATCH `dealstage`; you must set it explicitly or it stays at the prior value, breaking forecast roll-ups.
- **Hub tier gates**: Sequences require **Sales Hub Pro+** ($90/seat/mo); workflows require **Marketing Hub Pro+** OR **Sales Hub Enterprise**; predictive scoring requires **Enterprise** ($150/seat/mo).
- **Free Private App tokens never expire** but are tied to a single portal — for multi-tenant agencies, use the gateway OAuth path instead.
- **`closedate` is a date, not a datetime** — pass `YYYY-MM-DD` only. Timestamps with `T00:00:00` work but timezone-shift unpredictably; HubSpot stores in UTC midnight.
- **Associations are typed** — the `associationTypeId` (e.g., 216 for task→deal) must match the schema. Pull from `/crm/v4/associations/<from>/<to>/labels` once.
- **Search API caps at 10,000 results** with `after` pagination. For larger pulls use `/crm/v3/objects/<type>?paginate` (cursor-based) and accept that filters aren't supported the same way.

## Sources

- HubSpot CRM API reference: https://developers.hubspot.com/docs/api/crm/contacts
- HubSpot Deals API: https://developers.hubspot.com/docs/api/crm/deals
- HubSpot Sequences API (Sales Hub): https://developers.hubspot.com/docs/api/automation/sequences
- HubSpot Lists API v3 (June 2025 GA): https://developers.hubspot.com/docs/api/crm/lists
- HubSpot rate limits + tier matrix: https://developers.hubspot.com/docs/api/usage-details
- HubSpot remote MCP (`mcp.hubspot.com`) GA notes April 2026: https://developers.hubspot.com/mcp
