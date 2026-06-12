---
name: proposal-automation-pandadoc-proposify-qwilr
description: Automate sales proposal / SOW / quote generation via PandaDoc, Proposify, Qwilr, Better Proposals, GetAccept. CRM-triggered (HubSpot / Salesforce) doc creation with merge fields, content library blocks, dynamic pricing tables, embedded e-sign, and view analytics. Use when the user says "generate proposal from deal", "PandaDoc API", "Proposify integration", "Qwilr interactive proposal", "proposal template", "send SOW for signature".
---

# Proposal automation — PandaDoc / Proposify / Qwilr

This skill builds and triggers proposal documents through dedicated proposal platforms. Embedded e-sign is part of the package; CPQ logic and binding pricing decisions defer to `sales-ops` and `finance-controller`.

## When to use

User says:

- "Generate a proposal from this HubSpot deal / Salesforce opportunity"
- "PandaDoc / Proposify / Qwilr API"
- "Send the SOW for signature"
- "Interactive web proposal"
- "Embed pricing table in proposal"
- "Proposal analytics — who viewed, time-to-sign"
- "Content library blocks for proposal"

Companion skills:
- `dynamic-pricing-variable-insertion` — pricing-table payload construction.
- `e-signature-docusign-adobe-sign-pandadoc` — escalate to standalone e-sign when proposal platform isn't enough.
- `hubspot-doc-gen` / `salesforce-conga-composer` — CRM-side triggers.
- `document-analytics-time-to-sign` — funnel + view-time analytics.

## Setup

```bash
# PandaDoc — broadest 2026 default
# https://developers.pandadoc.com/reference/about
# Free dev sandbox; paid Business / Enterprise plans for production
pip install pandadoc-client     # optional Python SDK
# Or curl directly:
export PANDADOC_API_KEY="api_key_xxx"   # from PandaDoc → Settings → API + Integrations

# Proposify
# https://help.proposify.com/en/articles/5398128-api-getting-started
export PROPOSIFY_API_KEY="..."

# Qwilr
# https://qwilr.com/
export QWILR_API_KEY="..."

# GetAccept
# https://app.getaccept.com/api/  (REST)
export GETACCEPT_API_KEY="..."
```

Auth / API keys:
- `PANDADOC_API_KEY` — API key from PandaDoc Settings (Business plan+). Header: `Authorization: API-Key <key>`.
- `PROPOSIFY_API_KEY` — from Proposify Settings → API.
- `QWILR_API_KEY` — from Qwilr Settings → Integrations.
- OAuth alternative on PandaDoc available for multi-tenant SaaS use.

## Common recipes

### Recipe 1: Pick the platform

| Platform | Best for | Pricing (approx 2026) | API surface |
|---|---|---|---|
| PandaDoc | broadest CRM integrations, mature API | $19-65/user/mo | Full REST + webhooks + content library |
| Proposify | proposal-focused, simpler UI | $29-65/user/mo | REST API + Zapier |
| Qwilr | interactive web pages (not PDF-first) | $35-79/user/mo | REST API |
| Better Proposals | template marketplace, design-first | $19-49/user/mo | REST API |
| GetAccept | engagement + signing in one flow | quote | REST API + video proposal |
| Bonsai | freelancers + small studios | $25/mo | Limited API |

### Recipe 2: PandaDoc — create document from template

```bash
curl -X POST https://api.pandadoc.com/public/v1/documents \
  -H "Authorization: API-Key $PANDADOC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Proposal - Acme Corp - WidgetCloud Pro",
    "template_uuid": "tmpl_abc123",
    "recipients": [
      {"email": "buyer@acme.com", "first_name": "Jane", "last_name": "Smith", "role": "Customer"},
      {"email": "rep@widgetco.com", "first_name": "John", "last_name": "Doe", "role": "Sender"}
    ],
    "tokens": [
      {"name": "Customer.Name", "value": "Acme Corp"},
      {"name": "Deal.Amount", "value": "$120,000"},
      {"name": "Deal.StartDate", "value": "2026-07-01"}
    ],
    "pricing_tables": [{
      "name": "Pricing Table 1",
      "data_merge": false,
      "options": {"currency": "USD"},
      "sections": [{
        "title": "Subscription",
        "default": true,
        "rows": [
          {"options": {"qty": 50, "price": 200}, "data": {"name": "WidgetCloud Pro — per seat"}},
          {"options": {"qty": 1, "price": 5000}, "data": {"name": "Onboarding (one-time)"}}
        ]
      }]
    }],
    "metadata": {"deal_id": "hubspot_deal_55512"},
    "tags": ["proposal", "q2-2026"]
  }'
# Response: { "id": "doc_xyz", "status": "document.draft", ... }
```

### Recipe 3: PandaDoc — send for signature

```bash
# After document.uploaded webhook (POST /documents enqueues async draft creation)
curl -X POST "https://api.pandadoc.com/public/v1/documents/$DOC_ID/send" \
  -H "Authorization: API-Key $PANDADOC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Proposal for Acme Corp — please review",
    "message": "Hi Jane,\n\nAttached is the WidgetCloud Pro proposal we discussed. Sign in-line when ready.\n\nJohn",
    "silent": false
  }'
```

### Recipe 4: PandaDoc — webhook listener (completion + view events)

```python
# FastAPI receiver
from fastapi import FastAPI, Request, Header, HTTPException
import hmac, hashlib

app = FastAPI()
PANDADOC_SIGNATURE_KEY = "..."   # from PandaDoc → Settings → Webhooks → signing key

@app.post("/webhook/pandadoc")
async def pandadoc_webhook(req: Request, signature: str = Header(None, alias="X-Pandadoc-Signature")):
    body = await req.body()
    expected = hmac.new(PANDADOC_SIGNATURE_KEY.encode(), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise HTTPException(403)
    events = await req.json()
    for ev in events:
        if ev["event"] == "document_state_changed" and ev["data"]["status"] == "document.completed":
            # Download + archive
            ...
    return {"ok": True}
```

### Recipe 5: PandaDoc — content library block

```bash
# Reusable "Company Overview" block for any proposal
curl -X POST https://api.pandadoc.com/public/v1/content-library-items \
  -H "Authorization: API-Key $PANDADOC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Company Overview — WidgetCo",
    "blocks": [
      {"type": "text", "content": "WidgetCo is a cloud platform serving 5,000+ customers..."}
    ]
  }'
# Use the returned content_library_item_uuid in subsequent documents
```

### Recipe 6: Proposify — create proposal via API

```bash
curl -X POST https://api.proposify.com/v2/proposals \
  -H "Authorization: Bearer $PROPOSIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Acme Corp — WidgetCloud Pro Proposal",
    "template_id": 12345,
    "client_id": 67890,
    "fields": {
      "{{customer_name}}": "Acme Corp",
      "{{annual_fee}}": "$120,000"
    }
  }'
```

### Recipe 7: Qwilr — create interactive page

```bash
curl -X POST https://api.qwilr.com/v1/pages \
  -H "Authorization: Bearer $QWILR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Acme — WidgetCloud Pro",
    "templateId": "tpl_abc",
    "merge": {
      "customer.name": "Acme Corp",
      "deal.amount": 120000
    }
  }'
# Returns a public URL; embed in CRM, send via email
```

### Recipe 8: Trigger from HubSpot deal stage change

```python
# HubSpot Workflow → webhook POST → this handler
from fastapi import FastAPI, Request
import httpx
app = FastAPI()

@app.post("/webhook/hubspot-deal-stage")
async def on_deal_stage(req: Request):
    payload = await req.json()
    if payload["properties"]["dealstage"]["value"] != "proposal_sent":
        return {"skip": True}
    deal_id = payload["objectId"]
    # Fetch deal + line items + contacts (HubSpot CRM v3)
    headers = {"Authorization": f"Bearer {HUBSPOT_TOKEN}"}
    async with httpx.AsyncClient() as c:
        deal = (await c.get(f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}?associations=contacts,line_items", headers=headers)).json()
        # Build PandaDoc payload from deal
        await c.post("https://api.pandadoc.com/public/v1/documents",
                     headers={"Authorization": f"API-Key {PANDADOC_API_KEY}"},
                     json=build_pandadoc_payload(deal))
    return {"ok": True}
```

### Recipe 9: PandaDoc — embed CRM merge fields

PandaDoc supports CRM-tokenized fields (`[Contact.FirstName]`, `[Deal.Amount]`, `[Company.Name]`) when integration is connected to HubSpot / Salesforce / Pipedrive natively. In API mode, `tokens` array replaces them at create time.

### Recipe 10: PandaDoc analytics — view duration per section

```bash
# Get document details + view-time
curl "https://api.pandadoc.com/public/v1/documents/$DOC_ID/details" \
  -H "Authorization: API-Key $PANDADOC_API_KEY"
# Response includes recipients[].last_view_date, recipients[].read_duration_seconds
```

Pipe to `posthog-mcp` for funnel dashboards (sent → opened → read 30s+ → signed).

### Recipe 11: Document approval workflow (PandaDoc native)

```bash
# Add approver before recipients sign
curl -X POST "https://api.pandadoc.com/public/v1/documents/$DOC_ID/approvers" \
  -H "Authorization: API-Key $PANDADOC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "approvers": [
      {"email": "legal@widgetco.com", "id": "user_uuid_legal"},
      {"email": "cfo@widgetco.com", "id": "user_uuid_finance"}
    ]
  }'
```

## Examples

### Example 1: Sales Hub triggers PandaDoc on deal stage change

**Goal:** Rep clicks "Generate Proposal" in HubSpot → PandaDoc proposal created with deal data → emailed for signature.
**Steps:**
1. HubSpot Workflow: deal stage = "Proposal Sent" → webhook to internal endpoint.
2. Endpoint Recipe 8 — fetch deal + line items.
3. Map to PandaDoc payload (Recipe 2) using a deal-type → template_uuid lookup.
4. POST `/documents` → wait for `document.uploaded` webhook.
5. POST `/documents/{id}/send` (Recipe 3) with subject/message from rep.
6. Webhook listener Recipe 4 archives signed PDF + posts to Slack channel.

**Result:** One-click proposal from deal record to signed PDF.

### Example 2: Qwilr interactive proposal for enterprise sale

**Goal:** Send a fully interactive web proposal with embedded video, ROI calculator, and "select your plan" widget.
**Steps:**
1. Author Qwilr template with ROI block + plan selector.
2. Recipe 7 — POST `/pages` with merge data.
3. Email rep the Qwilr URL; rep forwards.
4. Buyer interacts → Qwilr captures section-by-section engagement.
5. Buyer clicks "Accept" → Qwilr e-sign or hand-off to DocuSign for contract.

**Result:** Interactive proposal with full engagement analytics.

### Example 3: Proposify multi-stakeholder approval flow

**Goal:** Each $50k+ proposal must be approved by legal + finance before client sees it.
**Steps:**
1. Recipe 6 — create proposal as draft.
2. Internal approval routing (Recipe 11 PandaDoc analog in Proposify Settings).
3. On both approvals, Proposify auto-sends to client.
4. Track signature via webhook → posthog funnel.

**Result:** Compliance-gated proposal flow.

## Edge cases / gotchas

- **PandaDoc draft creation is async.** `POST /documents` returns `document.draft` immediately but document isn't ready until `document.uploaded` webhook fires. Don't `/send` until ready.
- **Rate limits.** PandaDoc: 100 req/min on Business; 1000 req/min on Enterprise. Implement exponential backoff.
- **Pricing-table cents vs dollars.** `price` field is float in dollars (200.00 = $200). Don't pass cents (20000 → renders as $20,000).
- **Token vs merge-field naming.** PandaDoc tokens look like `Customer.Name` not `[Customer.Name]` in the API payload (brackets only in the template).
- **CRM token-mapping during native integration.** When PandaDoc-HubSpot is connected, tokens auto-populate; in API mode, you supply tokens — don't double-populate.
- **Webhook replay required.** PandaDoc webhooks fire at-least-once; deduplicate by `event_id`. Sign verification mandatory.
- **Qwilr quote acceptance is not e-sign.** Qwilr "Accept" is a click-to-accept gesture (still ESIGN/UETA-compliant for most commercial use) but high-stakes contracts should round-trip via DocuSign for the audit certificate.
- **Branding overrides.** Templafy + PandaDoc both inject brand assets; if both engaged, deduplicate to avoid double-stamped logos. See `template-library-templafy-brand`.
- **API key rotation.** No native key rotation alerts; build your own. Rotate quarterly.
- **PandaDoc OAuth vs API key.** OAuth required for multi-tenant; API key for single-account. Don't mix.
- **Proposify content library is per-workspace.** Template ID 12345 in workspace A ≠ template 12345 in workspace B; confirm `workspace_id` on every call.
- **Currency mismatch.** PandaDoc pricing tables default USD; pass `options.currency` for non-USD; multi-currency proposals require multi-table workaround.

## Sources

- [PandaDoc Developer Docs](https://developers.pandadoc.com/reference/about) — REST API + webhooks.
- [PandaDoc Pricing Tables](https://support.pandadoc.com/hc/en-us/articles/360011434953) — pricing payload schema.
- [Proposify API](https://help.proposify.com/en/articles/5398128-api-getting-started) — REST API.
- [Qwilr](https://qwilr.com/) — interactive web proposals.
- [Better Proposals](https://betterproposals.io/) — template-rich proposals.
- [GetAccept](https://www.getaccept.com/) — engagement-driven proposals.
- [HubSpot Developer Workflows](https://developers.hubspot.com/docs/api/automation/workflows) — CRM trigger source.
- Sister skills: `dynamic-pricing-variable-insertion`, `e-signature-docusign-adobe-sign-pandadoc`, `hubspot-doc-gen`, `salesforce-conga-composer`, `document-analytics-time-to-sign`.
