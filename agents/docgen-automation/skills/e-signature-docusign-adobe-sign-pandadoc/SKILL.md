---
name: e-signature-docusign-adobe-sign-pandadoc
description: Build e-signature pipelines on DocuSign eSignature REST API (dominant 2026 platform), Adobe Sign / Acrobat Sign (Adobe ecosystem), Dropbox Sign / HelloSign (SMB), PandaDoc, SignNow. Envelope creation, recipient routing, signature tabs, webhook (Connect) listeners, certificate of completion archival. Use when the user says "send for signature", "DocuSign envelope", "Adobe Sign / Acrobat Sign", "Dropbox Sign / HelloSign", "e-sign API", "signature workflow".
---

# E-signature pipeline — DocuSign / Adobe Sign / Dropbox Sign / PandaDoc

This skill ships the e-sign mechanics. Legal effect + compliance is `e-sign-compliance-ueta-esign-eidas`'s territory; this skill handles the API + envelope.

## When to use

User says:

- "Send for signature"
- "DocuSign envelope / API"
- "Adobe Sign / Acrobat Sign"
- "Dropbox Sign / HelloSign"
- "SignNow / SignWell / Concord Sign"
- "Embedded e-sign in proposal"
- "Multi-signer routing order"
- "Signature tabs / anchor strings"
- "Notarize.com / Proof.com" (RON section)

Companion skills:
- `e-sign-compliance-ueta-esign-eidas` — legal effect + tier selection (SES / AES / QES).
- `audit-trail-e-sign-versioning` — Certificate of Completion archival + hashing.
- `document-analytics-time-to-sign` — funnel + view-time analytics.
- `clm-ironclad-contractworks-integration` — push signed copy to CLM.

## Setup

```bash
# DocuSign — dominant 2026 platform
pip install docusign-esign
# or Node:
npm install docusign-esign

# Adobe Sign (Acrobat Sign)
# https://developer.adobe.com/document-services/apis/sign-api/
# REST API; OAuth 2.0
# pip install pyadobesign      # community SDK

# Dropbox Sign (formerly HelloSign)
pip install hellosign-python-sdk

# PandaDoc (proposal-style e-sign)
# See proposal-automation-pandadoc-proposify-qwilr

# SignNow
# https://docs.signnow.com/docs/signnow/welcome
pip install signnow-python-sdk

# Notarize / Proof (RON)
# https://www.proof.com/  (REST API on enterprise tier)
```

Auth / API keys:
- DocuSign: `DOCUSIGN_INTEGRATION_KEY` + `DOCUSIGN_USER_ID` + `DOCUSIGN_ACCOUNT_ID` + RSA private key for JWT (recommended) OR OAuth 2.0 access token.
- Adobe Sign: OAuth — `ADOBE_SIGN_CLIENT_ID`, `ADOBE_SIGN_CLIENT_SECRET`, `ADOBE_SIGN_REFRESH_TOKEN`; bearer access token.
- Dropbox Sign: `HELLOSIGN_API_KEY` — basic API key.
- PandaDoc: `PANDADOC_API_KEY` — header `Authorization: API-Key <key>`.
- SignNow: OAuth 2.0 — `SIGNNOW_CLIENT_ID`, `SIGNNOW_CLIENT_SECRET`, `SIGNNOW_USERNAME`, `SIGNNOW_PASSWORD`.

## Common recipes

### Recipe 1: Pick the platform

| Platform | Best for | Pricing (approx 2026) | API maturity |
|---|---|---|---|
| DocuSign | broadest enterprise + integrations | $10-65/user/mo+ | Mature REST + JWT + Connect webhooks |
| Adobe Sign | Adobe Creative Cloud users; PDF-heavy | $14.99-23.99/user/mo | OAuth + REST |
| Dropbox Sign | SMB simplicity, cheaper | $20-30/user/mo | REST + webhooks |
| PandaDoc | proposal + e-sign combined | $19-65/user/mo | REST + webhooks |
| SignNow | mid-market cost-conscious | $8-15/user/mo | REST |
| SignWell | very SMB | $10/user/mo | REST |
| OneSpan | banking + insurance, QES | enterprise quote | REST + SDK |
| Conga Sign | Salesforce-native | bundled | REST |

### Recipe 2: DocuSign — JWT auth (unattended)

```python
# pip install docusign-esign cryptography
from docusign_esign import ApiClient

api_client = ApiClient()
api_client.set_oauth_host_name("account.docusign.com")     # production
# or "account-d.docusign.com" for sandbox

token = api_client.request_jwt_user_token(
    client_id=os.environ["DOCUSIGN_INTEGRATION_KEY"],
    user_id=os.environ["DOCUSIGN_USER_ID"],
    oauth_host_name="account.docusign.com",
    private_key_bytes=open("private.key", "rb").read(),
    expires_in=3600,
    scopes=["signature", "impersonation"]
)
api_client.set_default_header("Authorization", f"Bearer {token.access_token}")
api_client.host = "https://na3.docusign.net/restapi"   # base URI from user-info call
```

One-time consent (per integration key + user pair) at:
`https://account.docusign.com/oauth/auth?response_type=code&scope=signature%20impersonation&client_id=<integration_key>&redirect_uri=<your_uri>`

### Recipe 3: DocuSign — create + send envelope (Python)

```python
from docusign_esign import (
    EnvelopesApi, EnvelopeDefinition, Document, Signer, SignHere, DateSigned,
    Text, Tabs, Recipients
)
import base64

with open("contract.pdf", "rb") as f:
    pdf_b64 = base64.b64encode(f.read()).decode("ascii")

envelope_def = EnvelopeDefinition(
    email_subject="Please sign: Cloud Services Agreement",
    email_blurb="See attached MSA. Sign at the marked tabs.",
    documents=[Document(
        document_base64=pdf_b64,
        name="MSA",
        file_extension="pdf",
        document_id="1"
    )],
    recipients=Recipients(signers=[
        Signer(
            email="buyer@acme.com",
            name="Jane Smith",
            recipient_id="1",
            routing_order="1",
            tabs=Tabs(
                sign_here_tabs=[SignHere(
                    anchor_string="/sn1/",
                    anchor_y_offset="10",
                    anchor_units="pixels",
                    anchor_x_offset="20"
                )],
                date_signed_tabs=[DateSigned(anchor_string="/ds1/", anchor_y_offset="10", anchor_units="pixels")],
                text_tabs=[Text(
                    anchor_string="/title1/", anchor_y_offset="10",
                    label="Title", required=True, width="120"
                )]
            )
        )
    ]),
    status="sent"     # "created" for draft; "sent" to send immediately
)

envelopes_api = EnvelopesApi(api_client)
result = envelopes_api.create_envelope(
    account_id=os.environ["DOCUSIGN_ACCOUNT_ID"],
    envelope_definition=envelope_def
)
print(f"Envelope: {result.envelope_id}")
```

### Recipe 4: DocuSign — anchor strings vs absolute positioning

```text
Anchor strings (preferred): place the literal string "/sn1/" in the PDF (white text on white bg so invisible).
At envelope create time, DocuSign finds every occurrence and places a tab anchored to it.
Pros: template invariant to page reflow.

Absolute positioning: SignHere(document_id="1", page_number="10", x_position="100", y_position="200")
Pros: deterministic placement when PDF layout is fixed.
Cons: breaks if pagination shifts.
```

### Recipe 5: DocuSign — sequential vs parallel routing

```python
# Sequential — recipient 1 signs first, then recipient 2
signers=[
    Signer(email="signer1@acme.com", routing_order="1", recipient_id="1", ...),
    Signer(email="signer2@acme.com", routing_order="2", recipient_id="2", ...)
]
# Parallel — both can sign in any order
signers=[
    Signer(email="signer1@acme.com", routing_order="1", recipient_id="1", ...),
    Signer(email="signer2@acme.com", routing_order="1", recipient_id="2", ...)
]
```

### Recipe 6: DocuSign — Connect webhook listener (envelope events)

```python
# FastAPI receiver
from fastapi import FastAPI, Request
import xmltodict

app = FastAPI()

@app.post("/webhook/docusign-connect")
async def connect(req: Request):
    body = await req.body()
    # Connect can deliver XML or JSON depending on config
    data = xmltodict.parse(body)
    envelope = data["DocuSignEnvelopeInformation"]["EnvelopeStatus"]
    status = envelope["Status"]
    if status == "Completed":
        envelope_id = envelope["EnvelopeID"]
        # Download combined doc + Certificate of Completion → see audit-trail-e-sign-versioning
    return {"ok": True}
```

Configure Connect in DocuSign Admin → Connect → Add Configuration → URL + events (Sent, Delivered, Completed, Declined, Voided).

### Recipe 7: DocuSign — download completed PDF + cert

```python
# After Completed event
envelopes_api = EnvelopesApi(api_client)
combined = envelopes_api.get_document(
    account_id=ACCT, envelope_id=env_id, document_id="combined"
)
with open(f"archive/{env_id}/combined.pdf", "wb") as f:
    f.write(combined)
cert = envelopes_api.get_document(
    account_id=ACCT, envelope_id=env_id, document_id="certificate"
)
with open(f"archive/{env_id}/certificate.pdf", "wb") as f:
    f.write(cert)
```

### Recipe 8: Adobe Sign — create agreement

```python
import requests

token = os.environ["ADOBE_SIGN_TOKEN"]
api = "https://api.na2.adobesign.com/api/rest/v6"

# 1) Upload transient document
with open("contract.pdf", "rb") as f:
    up = requests.post(
        f"{api}/transientDocuments",
        headers={"Authorization": f"Bearer {token}"},
        files={"File": f}
    )
doc_id = up.json()["transientDocumentId"]

# 2) Create agreement
agreement = requests.post(
    f"{api}/agreements",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={
        "fileInfos": [{"transientDocumentId": doc_id}],
        "name": "Acme MSA",
        "participantSetsInfo": [{
            "memberInfos": [{"email": "signer@acme.com"}],
            "order": 1,
            "role": "SIGNER"
        }],
        "signatureType": "ESIGN",
        "state": "IN_PROCESS"
    }
)
print(agreement.json()["id"])
```

### Recipe 9: Dropbox Sign — create signature request

```python
from hellosign_sdk import HSClient
client = HSClient(api_key=os.environ["HELLOSIGN_API_KEY"])

req = client.send_signature_request(
    test_mode=False,
    title="Acme MSA",
    subject="Please sign the Acme MSA",
    message="Sign at the marked locations.",
    signers=[{"email_address": "buyer@acme.com", "name": "Jane Smith"}],
    files=["contract.pdf"]
)
print(req.signature_request_id)
```

### Recipe 10: SignNow — invite signer

```bash
curl -X POST https://api.signnow.com/document/$DOC_ID/invite \
  -H "Authorization: Bearer $SIGNNOW_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to": [{"email": "buyer@acme.com", "role_id": "..."}],
    "from": "rep@widgetco.com",
    "subject": "Please sign"
  }'
```

### Recipe 11: Embedded signing — sign inside your app

```python
# DocuSign — create a recipient view URL the user redirects to
from docusign_esign import RecipientViewRequest
view = RecipientViewRequest(
    return_url="https://your-app/signing-complete",
    authentication_method="email",
    email="buyer@acme.com",
    user_name="Jane Smith",
    client_user_id="<your_uid_for_this_user>",   # MUST match signer's client_user_id
    recipient_id="1"
)
result = envelopes_api.create_recipient_view(
    account_id=ACCT, envelope_id=env_id, recipient_view_request=view
)
# Redirect the user to result.url
```

### Recipe 12: RON via Notarize / Proof.com

```bash
# Proof.com (formerly Notarize.com) — create a notary transaction
curl -X POST https://api.proof.com/v1/transactions \
  -H "X-API-KEY: $PROOF_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_name": "Deed - Acme - 2026-06-15",
    "documents": [{"resource": "<base64-pdf>"}],
    "signers": [{
      "first_name": "Jane", "last_name": "Smith",
      "email": "jane@acme.com",
      "signing_requirement": "notarization"
    }],
    "personally_known": false
  }'
# Signer joins live audio/video session with a commissioned notary; output: notarized + e-sealed PDF
```

### Recipe 13: Reminders + expiration

```python
# DocuSign envelope notification settings
from docusign_esign import EnvelopeNotificationRequest, Reminders, Expirations
notification = EnvelopeNotificationRequest(
    reminders=Reminders(reminder_enabled="true", reminder_delay="3", reminder_frequency="3"),
    expirations=Expirations(expire_enabled="true", expire_after="30", expire_warn="5")
)
envelopes_api.update_notification_settings(
    account_id=ACCT, envelope_id=env_id, envelope_notification_request=notification
)
```

## Examples

### Example 1: One-signer DocuSign MSA from contract pipeline

**Goal:** After `contract-template-authoring-msa-nda` renders MSA pdf, send for signature.
**Steps:**
1. Render docx → PDF (LibreOffice headless).
2. Recipe 2 — JWT auth.
3. Recipe 3 — envelope with anchor-string tabs.
4. Recipe 13 — 3-day reminders, 30-day expiration.
5. Recipe 6 — Connect webhook handler.
6. On Completed: Recipe 7 — download PDF + cert; archive via `audit-trail-e-sign-versioning`.

**Result:** Fully automated send-and-archive flow.

### Example 2: Multi-signer Adobe Sign agreement with parallel signing

**Goal:** Both buyer + seller sign simultaneously.
**Steps:**
1. Recipe 8 — create agreement with two members in `participantSetsInfo[0]` (same order).
2. Adobe Sign sends to both; either order accepted.
3. Webhook on completion.

**Result:** Faster turnaround on bilateral signing.

### Example 3: Embedded e-sign for SaaS onboarding

**Goal:** Customer signs the SaaS T&C inside your web app, not via email.
**Steps:**
1. Recipe 3 — create envelope with `client_user_id` on the signer.
2. Recipe 11 — generate recipient view URL.
3. Redirect customer to URL; on return, mark onboarding complete.

**Result:** Embedded signing UX inside SaaS onboarding.

## Edge cases / gotchas

- **DocuSign JWT requires one-time user consent.** First call returns 401 with a consent URL; user must approve once per `integration_key + user_id` pair.
- **Anchor strings are case-sensitive + must be invisible.** Use the same font color as the page background (white-on-white). Use unique strings (`/sn1/`, `/sn2/`) per tab.
- **DocuSign sandbox vs production.** `demo.docusign.net` (sandbox) vs `na3.docusign.net` / `eu.docusign.net` / etc. (production). Base URI returned by user-info endpoint; don't hardcode.
- **client_user_id is opaque but mandatory for embedded signing.** Use a stable user identifier; missing it → "Signing access required" error.
- **Connect webhook signing.** DocuSign Connect can sign with HMAC-SHA256; enable + validate the signature header.
- **Re-sends and reminders.** Multiple `POST /envelopes/{id}/recipients` resends; DocuSign rate-limits to a few per hour per recipient.
- **Adobe Sign URL region.** `na1`, `na2`, `na3`, `eu1`, `jp1` — get the correct base URL from `/baseUris` for your account.
- **Dropbox Sign templates.** Templates have role names; signers must reference roles, not raw emails.
- **eIDAS QES on DocuSign + Adobe Sign.** Enable EU Advanced/Qualified add-ons; signature ceremony uses Qualified Signature Creation Device. See `e-sign-compliance-ueta-esign-eidas`.
- **Reusable templates require approval.** DocuSign templates need account-level enable; some shops lock down template editing.
- **Bulk send.** DocuSign Bulk Send sends one envelope to many recipients (each gets a copy); confused with multi-signer — these are different.
- **PDF page count limit.** DocuSign: 25 MB per envelope, 1000 pages; Adobe Sign similar. Compress before upload.
- **Webhook idempotency.** DocuSign Connect retries; deduplicate by `envelope_id + status` pair.
- **RON jurisdictional limits.** Notarize/Proof only legal in states that have adopted RON statutes (40+ as of 2026). For others: hand off to in-person notary.
- **Sandbox certs are not legally binding.** Don't archive sandbox envelopes as production audit trail.

## Sources

- [DocuSign eSignature REST API](https://developers.docusign.com/docs/esign-rest-api/) — full reference.
- [DocuSign Connect](https://developers.docusign.com/platform/webhooks/connect/) — webhook configuration.
- [DocuSign JWT Grant](https://developers.docusign.com/platform/auth/jwt/) — unattended auth.
- [Adobe Sign Developer](https://developer.adobe.com/document-services/apis/sign-api/) — REST API.
- [Dropbox Sign (HelloSign) Developer](https://developers.hellosign.com/) — REST + SDKs.
- [SignNow API](https://docs.signnow.com/docs/signnow/welcome) — REST.
- [PandaDoc Developer](https://developers.pandadoc.com/reference/about) — proposal + e-sign.
- [Proof.com (formerly Notarize)](https://www.proof.com/) — RON.
- Sister skills: `e-sign-compliance-ueta-esign-eidas`, `audit-trail-e-sign-versioning`, `document-analytics-time-to-sign`, `clm-ironclad-contractworks-integration`.
