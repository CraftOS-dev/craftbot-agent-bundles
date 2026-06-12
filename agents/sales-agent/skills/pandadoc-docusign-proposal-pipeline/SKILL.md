<!--
Source: https://developers.pandadoc.com/ + https://developers.docusign.com/docs/esign-rest-api/
Proposal + e-sign workflow (June 2026 SOTA).
-->
# PandaDoc + DocuSign Proposal Pipeline — SKILL

Generate proposals from templates with CRM-merge tokens, send for e-sign, track view + sign analytics back to CRM. **PandaDoc** is proposal-native (template builder + e-sign in one); **DocuSign** is best when you already have a proposal source (PowerPoint, Google Doc, generated PDF) and just need enterprise-grade e-sign. **Qwilr** and **Proposify** are valid alternatives — covered briefly at the end.

## When to use

- **Generate a proposal from a CRM record** — pull deal data, populate template tokens, send to buyer.
- **E-sign a contract or MSA** — DocuSign for enterprise, PandaDoc for SMB.
- **Track proposal engagement** — who opened the doc, who viewed which page, who signed first.
- **Multi-signer routing** — sequential or parallel routing across champion / EB / legal.
- **Trigger phrases**: "send proposal to X", "draft a quote for deal Y", "e-sign this", "proposal status", "who signed", "send for redlines".

Do NOT use this skill for: **drafting the proposal *content*** (that's a `docx` / `notion-mcp` task before populating the template); **CPQ configuration** (use DealHub for complex SKU + bundle logic); **invoicing post-sign** (handoff to `stripe-mcp` or `finance-controller`).

## Setup

```bash
# Managed OAuth via Maton
export MATON_API_KEY="<key>"

# Direct fallbacks
export PANDADOC_API_KEY="<key>"      # Settings → API → Personal Access Token
# PandaDoc pricing: $19/seat/mo Essentials, $49 Business, $199 Enterprise
export DOCUSIGN_INTEGRATION_KEY="<key>"
export DOCUSIGN_USER_GUID="<user-guid>"
export DOCUSIGN_ACCOUNT_ID="<account-id>"
export DOCUSIGN_RSA_PRIVATE_KEY_PATH="/path/to/private.key"
# DocuSign pricing: $10/user/mo Personal, $25 Standard, $40 Business Pro, Enterprise-quote
```

DocuSign uses JWT auth (RSA-signed) for service accounts; PandaDoc uses simple API key. PandaDoc has a free sandbox tier; DocuSign developer accounts are free for testing.

## Common recipes

### Recipe 1: PandaDoc — create proposal from template + CRM tokens

```bash
# Step 1: List templates to get the right template ID
curl "https://gateway.maton.ai/pandadoc/public/v1/templates" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq '.results[] | {id, name}'

# Step 2: Create document from template with tokens populated
curl -X POST "https://gateway.maton.ai/pandadoc/public/v1/documents" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"Acme — Proposal Q3-2026",
    "template_uuid":"<template-id>",
    "owner":{"email":"ae@brand.com"},
    "recipients":[
      {"email":"sam@acme.com","first_name":"Sam","last_name":"Lee","role":"signer"},
      {"email":"alex@acme.com","first_name":"Alex","last_name":"Cruz","role":"approver"}
    ],
    "tokens":[
      {"name":"Account.Name","value":"Acme Inc"},
      {"name":"Deal.Amount","value":"$85,000"},
      {"name":"Deal.Term","value":"12 months"},
      {"name":"Deal.StartDate","value":"2026-07-01"},
      {"name":"Champion.FirstName","value":"Sam"},
      {"name":"EB.Title","value":"VP Sales"}
    ],
    "pricing_tables":[
      {"name":"Pricing","data_merge":true,"items":[
        {"qty":25,"name":"Sales Pro seats","price":2400,"description":"$2,400/seat/year"},
        {"qty":1,"name":"Onboarding","price":5000,"description":"One-time"}
      ]}
    ],
    "metadata":{"hubspot_deal_id":"<deal-id>"}
  }'
```

Returns document `id` in `uploaded` status.

### Recipe 2: PandaDoc — send for signature

```bash
curl -X POST "https://gateway.maton.ai/pandadoc/public/v1/documents/<doc-id>/send" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "message":"Hi Sam — proposal for our Q3 engagement. Two questions inline (highlighted). Happy to jump on a call to walk through.",
    "subject":"Brand × Acme — Proposal Q3-2026",
    "silent":false
  }'
```

`silent: false` triggers PandaDoc's email to each recipient with the signing link.

### Recipe 3: PandaDoc — get doc status + engagement

```bash
curl "https://gateway.maton.ai/pandadoc/public/v1/documents/<doc-id>/details" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq '{
    status,
    sent: .date_sent,
    signed: .date_completed,
    recipients: .recipients[] | {email, has_completed, last_view_date, total_views}
  }'
```

Status values: `document.draft`, `document.sent`, `document.viewed`, `document.completed`, `document.declined`.

### Recipe 4: PandaDoc — webhook for status changes

```bash
# Create once per workspace
curl -X POST "https://gateway.maton.ai/pandadoc/public/v1/webhook-subscriptions" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"Proposal status sync",
    "url":"https://your-app.com/webhook/pandadoc",
    "triggers":["document_state_changed","recipient_completed","document_completed"],
    "shared_key":"<secret-for-signature-validation>"
  }'
```

On `document_completed`, your handler should:
1. Patch the linked HubSpot deal: `dealstage = closedwon`, `closedate = now`.
2. Trigger `slack-mcp` post in `#wins` channel.
3. Hand off to `customer-success-agent` for kickoff (future).

### Recipe 5: DocuSign — create envelope from existing PDF

```bash
# Step 1: Get JWT access token (one-time per hour; cache the token)
# Build a JWT signed with your RSA private key — assertion scope: signature impersonation
ACCESS_TOKEN=$(curl -X POST https://account.docusign.com/oauth/token \
  -d "grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion=<your-jwt>" | jq -r '.access_token')

# Step 2: Create envelope with embedded PDF (base64)
PDF_B64=$(base64 -w 0 proposal.pdf)
curl -X POST "https://gateway.maton.ai/docusign/restapi/v2.1/accounts/$DOCUSIGN_ACCOUNT_ID/envelopes" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "emailSubject":"Please sign — Acme MSA",
    "documents":[{
      "documentBase64":"'$PDF_B64'",
      "name":"Acme MSA",
      "fileExtension":"pdf",
      "documentId":"1"
    }],
    "recipients":{
      "signers":[
        {
          "email":"sam@acme.com","name":"Sam Lee","recipientId":"1","routingOrder":"1",
          "tabs":{"signHereTabs":[{"anchorString":"/sig1/","anchorYOffset":"10","documentId":"1"}]}
        },
        {
          "email":"sarah@acme.com","name":"Sarah Lee","recipientId":"2","routingOrder":"2",
          "tabs":{"signHereTabs":[{"anchorString":"/sig2/","anchorYOffset":"10","documentId":"1"}]}
        }
      ]
    },
    "status":"sent"
  }'
```

`routingOrder` controls sequential routing — sig2 isn't shown until sig1 signs.

### Recipe 6: DocuSign — embedded signing (in-app signing UX)

```bash
# Step 1: Create envelope with clientUserId on the signer (not just email)
# Step 2: Generate recipient view URL — buyer signs in your iframe, not via email
curl -X POST "https://gateway.maton.ai/docusign/restapi/v2.1/accounts/$DOCUSIGN_ACCOUNT_ID/envelopes/<envelope-id>/views/recipient" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "userName":"Sam Lee",
    "email":"sam@acme.com",
    "recipientId":"1",
    "clientUserId":"<unique-internal-id>",
    "returnUrl":"https://your-app.com/post-sign"
  }' | jq -r '.url'
```

Use when you want the signing experience inside your app instead of DocuSign's email-link flow.

### Recipe 7: DocuSign — webhook (Connect) for envelope events

```bash
# One-time setup via UI: Settings → Connect → Add Configuration → URL + events
# Events to enable: envelope-sent, envelope-completed, envelope-declined, envelope-voided
```

DocuSign signs the webhook with HMAC; verify on receipt.

### Recipe 8: Bulk send via PandaDoc (proposal-per-prospect)

```bash
# Useful for renewal proposals or volume e-sign
curl -X POST "https://gateway.maton.ai/pandadoc/public/v1/documents/bulk_send" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "template_uuid":"<template-id>",
    "documents":[
      {"name":"Renewal — Acme","recipients":[{"email":"sam@acme.com","role":"signer"}],"tokens":[{"name":"Amount","value":"$30,000"}]},
      {"name":"Renewal — Globex","recipients":[{"email":"pat@globex.io","role":"signer"}],"tokens":[{"name":"Amount","value":"$45,000"}]}
    ]
  }'
```

Up to 50 docs per call.

### Recipe 9: Choose: PandaDoc vs DocuSign decision tree

```yaml
use_pandadoc_when:
  - "Proposal content lives in the template (pricing tables, customizable sections)"
  - "Deal size < $250K (faster to build, lower per-doc cost)"
  - "Sales team wants in-doc engagement analytics"
  - "Need pricing-table arithmetic in the doc"

use_docusign_when:
  - "Enterprise deal > $250K with strict legal review"
  - "Proposal already lives in PowerPoint / Word and goes through legal redlines"
  - "Customer requires DocuSign specifically (common in regulated industries)"
  - "Need advanced routing (sequential, parallel, conditional)"
  - "Compliance: 21 CFR Part 11, HIPAA-ready, FedRAMP needed"

avoid_both_when:
  - "Quote is < $1K and customer signs via simple click — use Stripe Checkout or invoice"
```

### Recipe 10: CRM-token mapping (deal record → proposal)

```yaml
# Map HubSpot deal properties to PandaDoc tokens
hubspot_deal_to_pandadoc_tokens:
  dealname              -> Deal.Name
  amount                -> Deal.Amount
  closedate             -> Deal.CloseDate
  hubspot_owner_id      -> AE.Email   (resolve owner email)
  meddic_economic_buyer -> EB.Title
  meddic_champion       -> Champion.Name
  amount_in_words       -> Deal.AmountInWords (custom computed field)
  primary_contact.email -> Recipient.Email
  primary_contact.firstname -> Recipient.FirstName
```

Compute custom tokens (like "amount in words", "annualized monthly cost") in your pre-send adapter; don't try to make PandaDoc evaluate formulas.

### Recipe 11: Track engagement → trigger NBA

```python
# On webhook event "document_viewed" — fire NBA if specific pages viewed
def on_viewed(payload):
    pages_viewed = payload["data"]["pages"]
    if any(p["page_number"] == 7 for p in pages_viewed):   # pricing page
        # The buyer is on pricing → high-intent signal
        create_hubspot_task({
            "subject":"Buyer viewed pricing page — follow up in 24h",
            "deal_id": payload["metadata"]["hubspot_deal_id"],
        })
    if any(p["page_number"] in (10, 11) for p in pages_viewed):  # legal/MSA pages
        # Buyer reviewing legal → likely close imminent
        slack_dm(deal_owner, "Buyer reviewing legal pages of proposal — Champion likely briefing EB")
```

## Examples

### Example 1: End-to-end proposal send (PandaDoc)

**Goal:** AE clicks "send proposal" on a $85K deal; buyer receives signed-ready proposal within 5 min.

**Steps:**
1. AE clicks the action; agent pulls deal record via `hubspot-sales-mcp` recipe 1.
2. Recipe 10 token map → build token array.
3. Recipe 1 — create PandaDoc document from "Mid-Market Annual" template.
4. Recipe 2 — send to champion + EB with personalized message.
5. Recipe 4 webhook configured ahead of time → fires when buyer views/signs.
6. On sign-complete event: PATCH HubSpot deal to closedwon (Recipe 5 in `hubspot-sales-mcp`); post to `#wins` Slack.

**Result:** AE sees doc sent in 5 min vs 30 min manual; buyer engagement tracked back to CRM automatically.

### Example 2: Enterprise MSA via DocuSign with multi-signer routing

**Goal:** $300K enterprise deal needs MSA signed by champion → legal (theirs) → CFO (theirs), in sequence; then countersigned by our COO.

**Steps:**
1. Legal-approved PDF rendered from Word source (via `docx` + `pdf` default skills).
2. Recipe 5 with 4 signers, `routingOrder: 1, 2, 3, 4`.
3. Anchor tabs (`/sig1/`, `/sig2/`, etc.) embedded in PDF at signature lines.
4. Recipe 7 webhook fires on each `envelope-completed` event → notify next signer's deal owner.
5. On final sign, PATCH HubSpot closedwon + create implementation kickoff task.

**Result:** 4-signer enterprise close handled cleanly with full audit trail.

## Edge cases / gotchas

- **PandaDoc tokens are case-sensitive** — `Deal.Amount` and `deal.amount` are different. Templates fail silently when a token isn't matched (renders the literal `{{Deal.Amount}}` in the doc).
- **PandaDoc free tier (Free eSign) is limited to 5 docs/mo** and no API access. Real use requires Business ($49/seat) minimum.
- **DocuSign JWT auth is fiddly** — need an Integration Key + RSA key pair + admin grant consent the first time. JWT expiry is 1 hour; cache + refresh.
- **DocuSign anchor tabs depend on exact PDF text matching** — if your PDF rendering changes (font, kerning), anchors silently misalign. Always test the final PDF before bulk-sending.
- **Sequential routing in PandaDoc requires the "Workflow" feature** — not in Essentials tier. Either upgrade or use DocuSign.
- **Webhook signature validation matters**: a malicious actor sending fake "completed" events can flip your CRM to closedwon. Verify HMAC on every event.
- **PandaDoc + Salesforce native integration** is more limited than HubSpot's; route through `api-gateway` for parity.
- **Re-sending a sent doc** in PandaDoc creates a *new* version, not a resend. To resend with same URL, use `/documents/<id>/resend`.
- **DocuSign "voided" envelopes count toward your quota** — high-volume teams burn through credits via voids.
- **Buyer side of e-sign is jurisdictional**: some EU buyers require qualified electronic signature (QES) via Adobe Sign + national ID schemes; standard DocuSign/PandaDoc e-sign may not be legally binding for certain contracts in those jurisdictions.
- **Pricing-table calculations**: PandaDoc auto-sums and discounts well; DocuSign + a static PDF requires hand-calculation. For deals with complex SKU bundles + multi-year ramps, prefer PandaDoc or a true CPQ.
- **Legal redlines**: PandaDoc has version-tracking; DocuSign does not natively (use Word's tracked changes externally). For >$100K deals with active legal redlines, DocuSign + Word back-and-forth is the norm.

## Sources

- PandaDoc API docs: https://developers.pandadoc.com/
- PandaDoc Documents API: https://developers.pandadoc.com/reference/documents
- DocuSign eSignature REST API: https://developers.docusign.com/docs/esign-rest-api/
- DocuSign JWT auth flow: https://developers.docusign.com/platform/auth/jwt/jwt-get-token/
- DocuSign Connect webhooks: https://developers.docusign.com/platform/webhooks/
- PandaDoc vs DocuSign vs Qwilr 2026 comparison: https://www.pandadoc.com/blog/pandadoc-vs-docusign/
- Qwilr API: https://help.qwilr.com/article/278-qwilr-api
- Proposify API: https://developer.proposify.com/
