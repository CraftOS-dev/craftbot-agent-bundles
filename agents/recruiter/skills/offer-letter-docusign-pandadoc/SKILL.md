<!--
Sources: https://developers.docusign.com/docs/esign-rest-api/
         https://developers.pandadoc.com/reference/about
         https://www.greenhouse.io/integrations/docusign
2026 landscape: DocuSign = market leader (1M+ customers, eSign + CLM); PandaDoc = modern API-first
challenger, template flexibility, free-tier eSign; HelloSign/Dropbox Sign = developer-friendly third
option. Offer-letter automation pattern: ATS event → DocuSign template merge → e-sign → webhook →
ATS attachment. Binding wording always deferred to legal-counsel.
-->
# Offer Letter — DocuSign / PandaDoc — SKILL

Generate, send, track, and archive offer letters via DocuSign or PandaDoc with ATS merge fields, e-signature, reminder cadence, and signed-PDF archive back to Greenhouse / Ashby / Lever. Covers REST template management, envelope creation, webhook handling for signed events, and the offer-acceptance-window tracking loop.

## When to use

- User has a verbal yes from the candidate and needs a binding offer letter generated + e-signed in <1 hour.
- Setting up offer-letter templates per geo (US FTE / US contractor / EMEA / APAC) with merge fields populated from ATS data.
- Building auto-reminder cadence (T+2, T+4, T+6 days) before offer expiration.
- Closing the loop: signed PDF auto-attached to candidate record in Greenhouse / Ashby / Lever.
- Trigger phrases: "draft offer", "send offer", "offer letter template", "e-sign", "DocuSign envelope", "PandaDoc document", "offer not signed yet".
- Defer binding wording (at-will, non-compete, IP assignment, FCRA, equity grant) to `legal-counsel`.

## Setup

```bash
# DocuSign (sandbox + prod)
export DOCUSIGN_ACCOUNT_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export DOCUSIGN_BASE_PATH="https://demo.docusign.net/restapi"   # demo
# export DOCUSIGN_BASE_PATH="https://na2.docusign.net/restapi"  # prod region
export DOCUSIGN_ACCESS_TOKEN="<bearer_from_jwt_grant>"          # JWT grant flow

# PandaDoc
export PANDADOC_API_KEY="<api-or-Bearer>"                       # https://app.pandadoc.com/a/#/settings/api

# Greenhouse for attachment back-link
export GREENHOUSE_API_KEY="harvest_xxx"
export GH_USER_ID="123456"
```

Auth model:
- **DocuSign:** JWT grant flow (server-to-server). Generate RSA keypair, upload public key to integration key, request access token from `oauth/token` with assertion. Tokens expire in 1 hour — refresh proactively.
- **PandaDoc:** Static API key (legacy) or OAuth2 (org installs). Pass as `Authorization: API-Key <key>` (legacy) or `Bearer <token>`.
- **HelloSign / Dropbox Sign:** Static API key, basic-auth pattern (`-u "$KEY:"`).

## Common recipes

### Recipe 1: List DocuSign templates
```bash
curl -s -H "Authorization: Bearer $DOCUSIGN_ACCESS_TOKEN" \
  "$DOCUSIGN_BASE_PATH/v2.1/accounts/$DOCUSIGN_ACCOUNT_ID/templates" \
  | jq '.envelopeTemplates[] | {templateId, name, lastModified}'
```
Use the returned `templateId` for envelope creation.

### Recipe 2: Send offer letter from DocuSign template
```bash
curl -s -X POST -H "Authorization: Bearer $DOCUSIGN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "$DOCUSIGN_BASE_PATH/v2.1/accounts/$DOCUSIGN_ACCOUNT_ID/envelopes" \
  -d '{
    "templateId": "<template_id>",
    "templateRoles": [{
      "email": "jane@example.com",
      "name": "Jane Doe",
      "roleName": "Candidate",
      "tabs": {
        "textTabs": [
          {"tabLabel": "base_salary", "value": "185000"},
          {"tabLabel": "start_date", "value": "2026-07-15"},
          {"tabLabel": "title", "value": "Senior Backend Engineer"},
          {"tabLabel": "equity_shares", "value": "12000"}
        ]
      }
    }],
    "status": "sent",
    "emailSubject": "Offer from Acme — please review and sign",
    "notification": {
      "reminders": {"reminderEnabled": "true", "reminderDelay": "2", "reminderFrequency": "2"},
      "expirations": {"expireEnabled": "true", "expireAfter": "7", "expireWarn": "2"}
    }
  }'
```
Merge fields populate via `tabLabel`. Built-in `reminders` + `expirations` replace your custom cadence.

### Recipe 3: Check DocuSign envelope status
```bash
curl -s -H "Authorization: Bearer $DOCUSIGN_ACCESS_TOKEN" \
  "$DOCUSIGN_BASE_PATH/v2.1/accounts/$DOCUSIGN_ACCOUNT_ID/envelopes/<envelope_id>" \
  | jq '{status, sentDateTime, completedDateTime, recipients}'
```
Statuses: `created`, `sent`, `delivered` (opened), `signed`, `completed`, `declined`, `voided`.

### Recipe 4: Download signed PDF from DocuSign
```bash
curl -s -H "Authorization: Bearer $DOCUSIGN_ACCESS_TOKEN" \
  -H "Accept: application/pdf" \
  "$DOCUSIGN_BASE_PATH/v2.1/accounts/$DOCUSIGN_ACCOUNT_ID/envelopes/<envelope_id>/documents/combined" \
  -o offer_signed.pdf
```

### Recipe 5: Register DocuSign Connect webhook (envelope events)
```bash
curl -s -X POST -H "Authorization: Bearer $DOCUSIGN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "$DOCUSIGN_BASE_PATH/v2.1/accounts/$DOCUSIGN_ACCOUNT_ID/connect" \
  -d '{
    "name": "Recruiter offer-signed → ATS",
    "urlToPublishTo": "https://hooks.example.com/docusign/signed",
    "envelopeEvents": ["completed", "declined", "voided"],
    "includeDocuments": true,
    "requireAcknowledgment": true,
    "signMessageWithX509Cert": false
  }'
```
DocuSign retries failed deliveries for 24h with backoff. Idempotent handler required.

### Recipe 6: PandaDoc — create document from template
```bash
curl -s -X POST -H "Authorization: API-Key $PANDADOC_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.pandadoc.com/public/v1/documents" \
  -d '{
    "name": "Offer Letter — Jane Doe — Senior Backend",
    "template_uuid": "<template_uuid>",
    "recipients": [
      {"email": "jane@example.com", "first_name": "Jane", "last_name": "Doe", "role": "Candidate", "signing_order": 1}
    ],
    "tokens": [
      {"name": "base_salary", "value": "$185,000"},
      {"name": "title", "value": "Senior Backend Engineer"},
      {"name": "start_date", "value": "July 15, 2026"},
      {"name": "equity_shares", "value": "12,000"}
    ],
    "pricing_tables": [],
    "metadata": {"ats_candidate_id": "<gh_candidate_id>"}
  }'
```
Returns `id` (document UUID). Document starts in `document.draft`.

### Recipe 7: PandaDoc — send document for signature
```bash
curl -s -X POST -H "Authorization: API-Key $PANDADOC_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.pandadoc.com/public/v1/documents/<document_id>/send" \
  -d '{
    "message": "Hi Jane, attached is your offer from Acme. Please review, sign, and reach out with any questions.",
    "subject": "Offer from Acme — please review and sign",
    "silent": false
  }'
```

### Recipe 8: PandaDoc — webhook subscription
```bash
curl -s -X POST -H "Authorization: API-Key $PANDADOC_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.pandadoc.com/public/v1/webhook-subscriptions" \
  -d '{
    "name": "Offer signed → ATS attachment",
    "url": "https://hooks.example.com/pandadoc/signed",
    "active": true,
    "triggers": ["document_state_changed", "document_completed"],
    "payload": ["documents", "recipients"]
  }'
```

### Recipe 9: Attach signed PDF back to Greenhouse candidate
```bash
curl -s -X POST -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -F "filename=offer_signed.pdf" \
  -F "type=offer_letter" \
  -F "content=@./offer_signed.pdf" \
  "https://harvest.greenhouse.io/v1/candidates/<candidate_id>/attachments"
```
`type` values: `offer_letter`, `resume`, `cover_letter`, `take_home_test`, `other`. Use `offer_letter` so it surfaces in the offer tab.

### Recipe 10: Attach signed PDF to Ashby
```bash
curl -s -X POST -u "$ASHBY_API_KEY:" \
  -F "applicationId=<app_id>" \
  -F "file=@./offer_signed.pdf" \
  "https://api.ashbyhq.com/file.upload"
# Then link via application.addNote with the returned fileHandle
```

### Recipe 11: Void / cancel an outstanding DocuSign envelope
```bash
curl -s -X PUT -H "Authorization: Bearer $DOCUSIGN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "$DOCUSIGN_BASE_PATH/v2.1/accounts/$DOCUSIGN_ACCOUNT_ID/envelopes/<envelope_id>" \
  -d '{"status": "voided", "voidedReason": "Candidate withdrew — voided per recruiter"}'
```

### Recipe 12: Resend a stalled envelope (DocuSign)
```bash
curl -s -X PUT -H "Authorization: Bearer $DOCUSIGN_ACCESS_TOKEN" \
  "$DOCUSIGN_BASE_PATH/v2.1/accounts/$DOCUSIGN_ACCOUNT_ID/envelopes/<envelope_id>/recipients?resend_envelope=true" \
  -d '{"signers":[{"recipientId":"1","email":"jane@example.com","name":"Jane Doe"}]}'
```

## Examples

### Example 1: End-to-end offer-send via DocuSign + Greenhouse
**Goal:** Verbal yes from Jane → signed offer in Greenhouse within 1h.
**Steps:**
1. Pull merge fields from Greenhouse: `GET /v1/candidates/<id>` → name, email; `GET /v1/offers/<id>` → comp + start date.
2. Resolve template by name (`templates?search_text=US-FTE-Senior-Engineer`).
3. Send envelope (Recipe 2) with merge tabs + 7-day expiration + 2-day reminder.
4. Webhook on `completed` (Recipe 5) → download PDF (Recipe 4) → attach to Greenhouse (Recipe 9) → POST `/v1/applications/<id>/move?stage=hired`.

**Result:** Signed PDF in Greenhouse offer tab, candidate moved to `hired`, hiring manager + ops Slacked. Under 90 sec of human time once template is wired.

### Example 2: PandaDoc with conditional equity-grant block
**Goal:** Single template handles ISO / NSO / RSU based on candidate type (US new hire vs international vs senior exec).
**Steps:**
1. PandaDoc template: add 3 content blocks (ISO, NSO, RSU) with conditional show-rules tied to `equity_type` token.
2. POST document with `tokens: [{name: "equity_type", value: "RSU"}, ...]` (Recipe 6); PandaDoc renders the correct block.
3. Send (Recipe 7).
4. Webhook on `document_completed` → fetch signed PDF: `GET /documents/<id>/download` → attach to ATS (Recipe 9 / 10).

**Result:** One template, no duplication. Legal reviews one canonical document. Switching to "RSU" no longer requires manual letter rewrite.

## Edge cases / gotchas

- **DocuSign JWT token expiry.** Tokens expire after 1h. Build a refresh loop or cache + lazily refresh on 401. Don't paste a bearer into the recruiter's terminal.
- **DocuSign sandbox vs prod base URLs.** `demo.docusign.net` vs `na2|eu|au.docusign.net`. Wrong base path → 404. Get the prod base from `GET /v2.1/accounts/<id>` → `baseUri`.
- **Template merge-field label drift.** If legal renames a `textTab` label in the template, your `tabLabel` payload silently doesn't merge — letter goes out with blank fields. Always test in sandbox after a template edit.
- **PandaDoc token vs role naming.** Recipient `role` must match the template's role exactly (case-sensitive). Mismatched role → 400 "role not found in template".
- **Offer-expiration timezone.** DocuSign envelope expiration is account-tz; convert from candidate's local TZ for offer-deadline wording in the letter.
- **Email deliverability.** Both DocuSign + PandaDoc emails sometimes hit spam (especially Gmail Promotions). Add your domain to candidate-side allowlist mention in the recruiter screen ("you'll get an email from `dse_NA4@docusign.net` or `panda@pandadoc.com`").
- **Webhook idempotency.** DocuSign Connect can deliver the same `completed` event twice on retries. Track by `envelopeId` + idempotency key in your handler.
- **Signature certificate retention.** DocuSign provides a signed certificate of completion (audit trail). Retain it 7+ years (employment-records norm) — download via `/envelopes/<id>/documents/certificate`.
- **Binding wording.** At-will (state-specific), non-compete (banned in CA / OK / ND / MN), IP assignment (CA Labor Code §2870 carve-out), FCRA contingency wording, Section 83(b) timing, mandatory arbitration (CA AB 51, NY UJC §7515 restrictions) → **defer to `legal-counsel`**.
- **Equity grant final terms.** Letter says "subject to Board approval"; Carta / Pulley owns issuance after Board grants. Don't promise vesting in the letter.
- **Rate limits.** DocuSign: ~1000 calls/hour per account (raise via support). PandaDoc: 100/min on most plans. Backoff on 429.
- **Free-tier ceilings.** DocuSign free dev sandbox = unlimited; prod free trial = 30 days. PandaDoc free eSign = unlimited but no templates / API on free tier. HelloSign / Dropbox Sign: 3 docs/month free.

## Sources

- [DocuSign eSignature REST API](https://developers.docusign.com/docs/esign-rest-api/)
- [DocuSign Envelope: Create](https://developers.docusign.com/docs/esign-rest-api/reference/envelopes/envelopes/create/)
- [DocuSign Connect (webhooks)](https://developers.docusign.com/platform/webhooks/connect/)
- [PandaDoc API reference](https://developers.pandadoc.com/reference/about)
- [PandaDoc webhooks](https://developers.pandadoc.com/reference/create-webhook-subscription)
- [Greenhouse `/candidates/{id}/attachments`](https://developers.greenhouse.io/harvest.html#post-add-attachment)
- [Ashby `file.upload`](https://developers.ashbyhq.com/reference/fileupload)
- [DocuSign vs PandaDoc 2026 comparison](https://www.g2.com/compare/docusign-vs-pandadoc)
