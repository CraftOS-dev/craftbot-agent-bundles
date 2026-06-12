---
name: hubspot-doc-gen
description: Generate proposals, quotes, and contracts from HubSpot deal data — HubSpot Quotes (native CPQ-lite for SMB), PandaDoc + HubSpot integration (richer proposals), DocuSign-embedded-in-HubSpot (legacy enterprise), DocSpring custom PDF rendering. Trigger on deal stage change via HubSpot Workflows + webhook → REST. Use when the user says "HubSpot Quote", "HubSpot Deal → proposal", "PandaDoc HubSpot integration", "HubSpot workflow doc gen".
---

# HubSpot-to-doc generation — Quotes / PandaDoc / DocuSign / DocSpring

This skill ships HubSpot-centric doc generation. The dominant 2026 stack: HubSpot Quotes for native SMB; PandaDoc + HubSpot for richer/enterprise; custom DocSpring/HTML for unique formats.

## When to use

User says:

- "Generate a quote from this HubSpot deal"
- "HubSpot Quote / HubSpot Quotes API"
- "PandaDoc integration with HubSpot"
- "HubSpot Workflow → doc gen → e-sign"
- "DocSpring HubSpot integration"
- "Embed signed PDF onto the HubSpot deal record"

Companion skills:
- `proposal-automation-pandadoc-proposify-qwilr` — PandaDoc deep dive.
- `e-signature-docusign-adobe-sign-pandadoc` — sign step after generation.
- `dynamic-pricing-variable-insertion` — line-item + pricing logic.
- `bulk-document-gen-csv` — batch HubSpot-driven runs.

## Setup

```bash
# HubSpot CRM API v3
# Required env: HUBSPOT_ACCESS_TOKEN (private app token) OR OAuth refresh
# Base: https://api.hubapi.com
# Docs: https://developers.hubspot.com/docs/api/overview

# Optional: HubSpot Quotes API
# Same auth; endpoints under /crm/v3/objects/quotes

# PandaDoc REST (recommended doc backend for HubSpot)
# Required env: PANDADOC_API_KEY

# DocSpring (custom PDF generation)
# Required env: DOCSPRING_API_TOKEN

# Optional: DocuSign for embedded signing in HubSpot
# Required env: DOCUSIGN_INTEGRATION_KEY, DOCUSIGN_USER_ID, DOCUSIGN_ACCOUNT_ID

pip install requests
```

## Common recipes

### Recipe 1: Pick the doc backend

| Backend | Best for | Pricing tier (approx 2026) | Strengths |
|---|---|---|---|
| HubSpot Quotes (native) | SMB; HubSpot Sales Hub Pro+ | Bundled | Zero-integration; data lives in HubSpot |
| PandaDoc + HubSpot | Mid-market; richer proposals | $19-65/user/mo | Templates, pricing tables, e-sign in one |
| DocuSign Gen + HubSpot | DocuSign-native shops | DocuSign+Gen tier | Strong CLM downstream |
| DocSpring + HubSpot | Custom-formatted PDFs | $50-300/mo | Pure PDF render — bring your own UI |
| Proposify / Qwilr + HubSpot | Design-led proposals | $25-49/user/mo | Beautiful proposal UX |

Default for SMB: HubSpot Quotes. Default for mid-market: PandaDoc + HubSpot.

### Recipe 2: HubSpot — fetch a deal + associated objects

```bash
# Get deal + properties + line items + primary contact + company
curl "https://api.hubapi.com/crm/v3/objects/deals/$DEAL_ID?associations=line_items,contacts,companies&properties=dealname,amount,closedate,pipeline,dealstage" \
  -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN"
```

Iterate associations to pull line item details:

```bash
for LI in $(jq -r '.associations.line_items.results[].id'); do
  curl "https://api.hubapi.com/crm/v3/objects/line_items/$LI?properties=name,quantity,price,hs_total_discount" \
    -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN"
done
```

### Recipe 3: HubSpot Quotes — create a native quote (Quotes API)

```bash
curl -X POST https://api.hubapi.com/crm/v3/objects/quotes \
  -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "hs_title": "Acme Corp - Q2 2026",
      "hs_expiration_date": "2026-07-15",
      "hs_currency": "USD",
      "hs_payment_enabled": "true",
      "hs_esign_enabled": "true",
      "hs_terms": "Net 30. Subject to MSA.",
      "hs_proposal_template": "PROPOSAL_TEMPLATE_ID"
    },
    "associations": [
      { "to": {"id": "DEAL_ID"}, "types": [{"associationCategory":"HUBSPOT_DEFINED","associationTypeId":64}] }
    ]
  }'
```

Then associate line items by similar POST to `/crm/v3/objects/quotes/$QUOTE_ID/associations/line_items/$LI_ID/quote_to_line_item`.

### Recipe 4: HubSpot Quotes — set delivery + send

```bash
# Mark quote as Approved → URL becomes public
curl -X PATCH https://api.hubapi.com/crm/v3/objects/quotes/$QUOTE_ID \
  -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"properties":{"hs_status":"APPROVED"}}'

# Get the public URL
curl "https://api.hubapi.com/crm/v3/objects/quotes/$QUOTE_ID?properties=hs_public_url_key" \
  -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" | jq -r '.properties.hs_public_url_key'
# → https://app.hubspot.com/documents/.../<public_key>
```

### Recipe 5: PandaDoc — create document from HubSpot deal (recommended)

```python
import requests

# 1) Fetch deal
deal = requests.get(
    f"https://api.hubapi.com/crm/v3/objects/deals/{DEAL_ID}?associations=line_items,contacts",
    headers={"Authorization": f"Bearer {HUBSPOT_TOKEN}"}
).json()

# 2) Create PandaDoc from template (pre-built in PandaDoc UI)
pdoc = requests.post(
    "https://api.pandadoc.com/public/v1/documents",
    headers={"Authorization": f"API-Key {PANDADOC_KEY}"},
    json={
        "name": f"Proposal - {deal['properties']['dealname']}",
        "template_uuid": PANDADOC_TEMPLATE_UUID,
        "recipients": [{
            "email": primary_contact_email,
            "first_name": primary_contact_first,
            "last_name": primary_contact_last,
            "role": "client"
        }],
        "tokens": [
            {"name": "deal.name", "value": deal["properties"]["dealname"]},
            {"name": "deal.amount", "value": deal["properties"]["amount"]},
            {"name": "deal.close_date", "value": deal["properties"]["closedate"]},
        ],
        "pricing_tables": [{
            "name": "Pricing",
            "sections": [{
                "title": "Subscription",
                "rows": [
                    {"options": {}, "data": {
                        "name": li["properties"]["name"],
                        "qty": li["properties"]["quantity"],
                        "price": li["properties"]["price"]
                    }}
                    for li in line_items
                ]
            }]
        }],
        "metadata": {"hubspot_deal_id": DEAL_ID}
    }
).json()
```

### Recipe 6: PandaDoc — send + capture document URL

```python
doc_id = pdoc["id"]
# Wait for processing
while requests.get(f"https://api.pandadoc.com/public/v1/documents/{doc_id}",
                   headers={"Authorization": f"API-Key {PANDADOC_KEY}"}).json()["status"] == "document.uploaded":
    time.sleep(2)
# Send
requests.post(
    f"https://api.pandadoc.com/public/v1/documents/{doc_id}/send",
    headers={"Authorization": f"API-Key {PANDADOC_KEY}"},
    json={"message": "Please review and sign.", "silent": False}
)
```

### Recipe 7: PandaDoc webhook → write back to HubSpot deal

```python
# PandaDoc fires document_state_changed events
@app.post("/webhooks/pandadoc")
async def pdoc_webhook(payload: dict):
    if payload["event"] == "document_state_changed" and payload["data"]["status"] == "document.completed":
        deal_id = payload["data"]["metadata"]["hubspot_deal_id"]
        # Move HubSpot deal to "Closed Won"
        requests.patch(
            f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}",
            headers={"Authorization": f"Bearer {HUBSPOT_TOKEN}"},
            json={"properties": {"dealstage": "closedwon"}}
        )
        # Attach signed PDF as a note + file
        pdf_url = payload["data"]["pdf_url"]
        # Recipe 8 — attach
```

### Recipe 8: Attach a file to a HubSpot deal

```bash
# Upload file
FILE_ID=$(curl -X POST https://api.hubapi.com/files/v3/files \
  -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -F "file=@signed-proposal.pdf" \
  -F "folderPath=/Signed Proposals" \
  -F 'options={"access":"PRIVATE"}' \
  | jq -r '.id')

# Attach to deal via note
curl -X POST https://api.hubapi.com/crm/v3/objects/notes \
  -H "Authorization: Bearer $HUBSPOT_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"properties\": {
      \"hs_note_body\": \"Signed proposal attached.\",
      \"hs_attachment_ids\": \"$FILE_ID\",
      \"hs_timestamp\": $(date +%s)000
    },
    \"associations\": [{\"to\":{\"id\":\"$DEAL_ID\"},\"types\":[{\"associationCategory\":\"HUBSPOT_DEFINED\",\"associationTypeId\":214}]}]
  }"
```

### Recipe 9: HubSpot Workflow → webhook trigger

In HubSpot → Workflows → Create:
1. Trigger: Deal stage = "Proposal Sent" (custom stage).
2. Action: Send webhook to `https://your-app/webhooks/hubspot-proposal`.
3. Payload includes deal ID + contact ID.
4. Your endpoint runs Recipe 5 to create the PandaDoc proposal.

### Recipe 10: DocSpring — render HTML template + HubSpot data → PDF

```bash
# DocSpring expects a pre-uploaded template with form-field tokens
curl -X POST https://api.docspring.com/api/v1/templates/$TEMPLATE_ID/submissions \
  -u $DOCSPRING_API_TOKEN: \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "customer_name": "Acme Corp",
      "deal_amount": 240000,
      "term_months": 36
    },
    "test": false
  }'
# Response includes download_url for the rendered PDF
```

### Recipe 11: DocuSign send + embed signed PDF on HubSpot deal

```python
# After Recipe 5/6 OR direct DocuSign send
# DocuSign Connect webhook fires on Completed
# Pull cert + combined PDF (see e-signature-docusign-adobe-sign-pandadoc)
# Then Recipe 8 — attach to HubSpot deal
```

### Recipe 12: Bulk proposal regeneration (e.g., quarterly rebrand)

```python
# Re-render all OPEN proposals after brand update
deals = requests.get(
    "https://api.hubapi.com/crm/v3/objects/deals?properties=dealname,amount&associations=line_items",
    headers={"Authorization": f"Bearer {HUBSPOT_TOKEN}"}
).json()
for d in deals["results"]:
    if d["properties"]["dealstage"] in ("appointmentscheduled", "qualifiedtobuy", "presentationscheduled"):
        # Recipe 5 — re-create PandaDoc with new template version
        ...
```

## Examples

### Example 1: SMB native — HubSpot Quotes only

**Goal:** 15-rep SaaS shop ships quotes natively, no extra tools.
**Steps:**
1. Build a Proposal Template in HubSpot UI (Settings → Quotes).
2. Add custom Quote properties (currency, terms).
3. Reps create Quote from Deal → publish → public URL.
4. Buyer signs + pays (HubSpot Payments).
5. Quote object stores artifact + status.

**Result:** Zero-cost doc gen for HubSpot-resident teams.

### Example 2: Mid-market — PandaDoc + HubSpot + DocuSign hand-off

**Goal:** Better template variety + analytics; existing DocuSign for execution.
**Steps:**
1. Recipe 9 — HubSpot workflow on stage change.
2. Recipe 5 — create PandaDoc with template + tokens.
3. Recipe 6 — send to client.
4. PandaDoc analytics tracked in PandaDoc; final signed PDF re-routed to DocuSign for audit.
5. Recipe 8 — attach signed PDF to deal.

**Result:** Best-of-breed with HubSpot as system of record.

### Example 3: Custom legal contract template → DocSpring

**Goal:** Custom MSA with unique branding; needs precise PDF layout.
**Steps:**
1. Author HTML/CSS for MSA in DocSpring UI.
2. Recipe 10 — render via DocSpring with HubSpot data.
3. Send via DocuSign envelope.
4. Recipe 8 — archive on deal.

**Result:** Pixel-perfect bespoke contracts driven by HubSpot pipeline.

## Edge cases / gotchas

- **HubSpot Quotes is Sales Hub Pro+.** Free + Starter tiers lack the Quotes object — gate the recipe by tier.
- **Private app vs OAuth.** Private apps simpler; OAuth required for marketplace apps. Required scopes: `crm.objects.deals.read`, `crm.objects.quotes.write`, `files`, `e-commerce`.
- **HubSpot Quote public URL token.** `hs_public_url_key` only generated when status = APPROVED; otherwise empty.
- **HubSpot Payments availability.** US/Canada only (as of 2026); EU buyers use Stripe link manually.
- **Line item price book.** Quote line items can be pulled from HubSpot Products library or be ad-hoc. Decide org-wide convention.
- **PandaDoc template tokens vs HubSpot fields.** Token names must match exactly; design a mapping doc.
- **PandaDoc Pricing tables vs Free text.** Pricing tables compute totals server-side; free text doesn't — use pricing tables for anything monetary.
- **Webhook signing.** HubSpot signs webhooks with `X-HubSpot-Signature-v3`; always verify.
- **Webhook retries.** HubSpot retries on 5xx; idempotency keys recommended.
- **PandaDoc HubSpot CRM Card.** PandaDoc ships a CRM Card for HubSpot deals — surface it on the deal record for in-CRM creation.
- **Multi-currency.** Both HubSpot Quotes + PandaDoc support multi-currency; set deal currency early.
- **Decimal precision.** HubSpot stores `amount` as decimal; PandaDoc expects strings for pricing — coerce types.
- **DocSpring templates.** Edit in DocSpring UI; preview mode for QA — production rendering uses the published template version.
- **Owner / Branding on quotes.** HubSpot Quotes inherit org-default branding; per-deal override only via templated content.
- **Quote expiration.** Native quotes default 30 days; PandaDoc default 90 — verify.
- **HubSpot deal close auto-close.** When deal closes via PandaDoc webhook, only the deal closes — sub-items (e.g., recurring revenue) must be set up separately.

## Sources

- [HubSpot CRM API v3](https://developers.hubspot.com/docs/api/crm/understanding-the-crm) — deals, contacts, quotes, files.
- [HubSpot Quotes API](https://developers.hubspot.com/docs/api/crm/quotes) — native quote object.
- [HubSpot Files API](https://developers.hubspot.com/docs/api/files/files) — attach signed PDFs.
- [HubSpot Workflows](https://knowledge.hubspot.com/workflows/) — UI workflow triggers.
- [PandaDoc Developer Docs](https://developers.pandadoc.com/reference/about) — templates + recipients + send.
- [PandaDoc + HubSpot integration](https://www.pandadoc.com/integrations/hubspot/) — official integration page.
- [DocSpring API](https://docspring.com/docs/api/) — custom PDF rendering.
- [DocuSign Gen for HubSpot](https://www.docusign.com/products/hubspot) — DocuSign-native flow.
- Sister skills: `proposal-automation-pandadoc-proposify-qwilr`, `e-signature-docusign-adobe-sign-pandadoc`, `dynamic-pricing-variable-insertion`, `bulk-document-gen-csv`.
