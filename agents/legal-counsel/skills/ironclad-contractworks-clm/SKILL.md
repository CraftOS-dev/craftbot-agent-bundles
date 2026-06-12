---
name: ironclad-contractworks-clm
description: Contract Lifecycle Management (CLM) platform workflows — Ironclad (enterprise), ContractWorks (mid-market), Lexion (acquired by DocuSign), Evisort, LinkSquares, Concord, PandaDoc. AI clause extraction + repository + workflow automation + e-signature integration (DocuSign / Adobe Sign / Dropbox Sign). Use when integrating contract review output into the user's CLM. Output is an integration plan + memo with the consult-an-attorney disclaimer.
---

# Ironclad / ContractWorks / Lexion CLM — Integration Workflows

The agent doesn't "drive" the CLM but designs the integration workflow so contract-review output flows in cleanly.

## When to use

User says:

- "Set up Ironclad / ContractWorks / Lexion / Evisort / LinkSquares / Concord"
- "CLM workflow for our [contract type]"
- "AI clause extraction"
- "Contract repository"
- "Integrate DocuSign with [CLM]"
- "Workflow automation for contract approvals"
- "Migration from email-based contracts to CLM"

Companion skills:
- `contract-review-msa-nda-employment` — review feeds into CLM.
- `robin-spellbook-harvey-ai-contract-review` — AI redlines into CLM.

## Setup

```bash
# Ironclad — enterprise CLM
# https://ironcladapp.com/
# Quote-based; typically $20k-200k/year

# ContractWorks (by Onit) — mid-market
# https://www.contractworks.com/

# Lexion — acquired by DocuSign 2024
# https://www.lexion.ai/

# Evisort — AI-first CLM
# https://www.evisort.com/

# LinkSquares — AI CLM
# https://linksquares.com/

# Concord — easier startup CLM
# https://www.concord.app/

# PandaDoc — SMB-friendly
# https://www.pandadoc.com/

# DocuSign — e-signature SOTA
pip install docusign-esign
# or
npm install docusign-esign

# Adobe Sign
# https://developer.adobe.com/document-services/apis/sign/

# Dropbox Sign (formerly HelloSign)
# https://developers.hellosign.com/
pip install hellosign-python-sdk
```

Auth / API keys:
- `IRONCLAD_API_KEY` — Ironclad API (enterprise tier).
- `CONTRACTWORKS_API_KEY` — ContractWorks.
- `DOCUSIGN_*` — OAuth client ID / secret / user GUID / private key.
- `ADOBE_SIGN_*` — OAuth.
- `HELLOSIGN_API_KEY` — Dropbox Sign.

## Common recipes

### Recipe 1: Pick the right CLM
| CLM | Tier | Best for | Pricing (approx 2026) |
|---|---|---|---|
| Ironclad | Enterprise | Big-Law / Fortune 500 / sophisticated legal ops | $20k-200k+/year |
| Evisort | Enterprise | AI-heavy clause extraction | $20k-100k/year |
| LinkSquares | Mid/Enterprise | Self-service legal team | $15k-60k/year |
| ContractWorks | Mid-market | Single-product simplicity | $7k-30k/year |
| Lexion (DocuSign) | Mid-market | DocuSign-integrated workflow | $10k-30k/year |
| Concord | Startup/SMB | Lighter touch | $3k-15k/year |
| PandaDoc | SMB | Sales contracts + proposals | $1.2k-15k/year |
| Spotdraft | Startup | New entrant; AI-first | Quote |
| Juro | Mid-market | Browser-native | $10k-30k/year |

Decision factors:
- Volume of contracts (50/year = light tier; 500+ = mid/enterprise)
- Legal team headcount (solo = light; 5+ = enterprise)
- Existing tech stack (Salesforce / HubSpot / DocuSign integration?)
- Budget
- AI requirements

### Recipe 2: Ironclad workflow
```text
1. Sign up + onboarding (1-2 weeks typical).
2. Configure workflows:
   - Each contract type (MSA, NDA, vendor, etc.) → workflow with required fields + approvers
3. Build clause library (Ironclad's "Clause Library"):
   - Approved fallback clauses
   - Industry-standard alternatives
4. Set up integrations:
   - Salesforce (CRM) — auto-create contract from opportunity
   - DocuSign (e-sign) — Ironclad → DocuSign envelope
   - Slack — approval notifications
5. Configure AI clause discovery on uploaded contracts.
6. Workflow live; sales kicks off contract from Salesforce; legal approves; signature via DocuSign; repository in Ironclad.
```

### Recipe 3: Ironclad API — programmatic record creation
```python
import requests, os

API = "https://api.ironcladapp.com/public/api/v1"
key = os.environ["IRONCLAD_API_KEY"]
headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

# Create record (contract)
resp = requests.post(
    f"{API}/records",
    headers=headers,
    json={
        "type": "msa",
        "name": "Acme Corp MSA",
        "metadata": {
            "counterparty": "Acme Corp",
            "value": 50000,
            "term": "12 months"
        },
        "attachments": [{"url": "https://yourstore/contract.pdf"}]
    }
)
print(resp.json())
```

### Recipe 4: DocuSign envelope creation (Python)
```python
import docusign_esign as ds
from docusign_esign import ApiClient, EnvelopesApi
import os, base64

api_client = ApiClient()
api_client.host = "https://demo.docusign.net/restapi"  # use demo for sandbox; production for live
api_client.set_default_header("Authorization", f"Bearer {os.environ['DOCUSIGN_ACCESS_TOKEN']}")

envelope_api = EnvelopesApi(api_client)
account_id = os.environ["DOCUSIGN_ACCOUNT_ID"]

# Read contract PDF
with open("contract.pdf", "rb") as f:
    document_base64 = base64.b64encode(f.read()).decode("utf-8")

envelope = ds.EnvelopeDefinition(
    email_subject="Please sign: Acme Corp MSA",
    documents=[
        ds.Document(
            document_base64=document_base64,
            name="MSA",
            file_extension="pdf",
            document_id="1"
        )
    ],
    recipients=ds.Recipients(
        signers=[
            ds.Signer(
                email="signer@acme.com",
                name="Jane Doe",
                recipient_id="1",
                routing_order="1",
                tabs=ds.Tabs(
                    sign_here_tabs=[
                        ds.SignHere(
                            document_id="1",
                            page_number="10",
                            x_position="100",
                            y_position="200"
                        )
                    ]
                )
            )
        ]
    ),
    status="sent"
)

result = envelope_api.create_envelope(account_id, envelope_definition=envelope)
print(result.envelope_id)
```

### Recipe 5: Adobe Sign envelope (alternative)
```python
import requests, os

# OAuth — get access token
# https://developer.adobe.com/document-services/docs/apis/#tag/sign

token = os.environ["ADOBE_SIGN_TOKEN"]
api = "https://api.na2.adobesign.com/api/rest/v6"
headers = {"Authorization": f"Bearer {token}"}

# Upload document
with open("contract.pdf", "rb") as f:
    upload = requests.post(
        f"{api}/transientDocuments",
        headers=headers,
        files={"File": f}
    )
doc_id = upload.json()["transientDocumentId"]

# Create agreement
agreement = requests.post(
    f"{api}/agreements",
    headers={**headers, "Content-Type": "application/json"},
    json={
        "fileInfos": [{"transientDocumentId": doc_id}],
        "name": "Acme MSA",
        "participantSetsInfo": [
            {
                "memberInfos": [{"email": "signer@acme.com"}],
                "order": 1,
                "role": "SIGNER"
            }
        ],
        "signatureType": "ESIGN",
        "state": "IN_PROCESS"
    }
)
print(agreement.json())
```

### Recipe 6: ContractWorks workflow
```text
Lighter than Ironclad:
1. Sign up + initial repository upload (drag-and-drop).
2. OCR + auto-tagging of existing contracts.
3. Smart Tags for date / value / counterparty extraction.
4. Renewal alerts.
5. E-sign integration (DocuSign / Adobe Sign / built-in).
6. Templates for MSA / NDA / SOW.
7. Permission management — view by role.
```

### Recipe 7: AI clause extraction (Evisort / LinkSquares / Lexion / Ironclad AI)
```text
Workflows:
1. Upload contract corpus.
2. AI extracts:
   - Effective date
   - Term + auto-renewal
   - Termination notice
   - Liability cap
   - Indemnity scope
   - IP ownership
   - Governing law
   - Payment terms
3. Build dashboards:
   - "All vendor contracts with auto-renewal in next 90 days"
   - "All MSAs with liability cap under $1M"
   - "All contracts with CA governing law"
4. Trigger workflows on extracted data (e.g., auto-renew alert).
```

### Recipe 8: Integration with sales — Salesforce → CLM
```text
Common workflow:
1. Sales closes opportunity in Salesforce.
2. Trigger CLM workflow (Ironclad / LinkSquares / etc.):
   - Auto-populate contract from template
   - Counterparty data from Salesforce
   - Pricing from Salesforce
3. Legal reviews + redlines in CLM.
4. Approval routing (Slack notifications).
5. Send to counterparty for signature via DocuSign.
6. Signed copy back in CLM repository.
7. Salesforce updated with execution date + contract reference.
```

### Recipe 9: Integration with contract-review output
```text
Manual review workflow:
1. Contract uploaded to CLM (manual or auto from Salesforce).
2. Legal reviews using `contract-review-msa-nda-employment` skill.
3. Memo + redline produced.
4. Upload memo as attachment to CLM record.
5. Redline routed to counterparty.
6. Iteration + finalization.
7. Signature via DocuSign.
8. Repository updated.

AI-assisted workflow (`robin-spellbook-harvey-ai-contract-review`):
1. CLM kicks off review.
2. Robin AI / Spellbook produces first-pass redline.
3. Legal reviews AI output.
4. Modified redline back to CLM.
5. Standard workflow continues.
```

### Recipe 10: Migration from email-based to CLM
```text
Migration steps:
1. Inventory existing contracts (Google Drive / Dropbox / SharePoint / email attachments).
2. Pick CLM (Recipe 1).
3. Bulk upload contracts → OCR + auto-tagging.
4. Manually verify key contracts.
5. Tag by counterparty / type / value / status.
6. Set up workflows for NEW contracts.
7. Train team on new process.
8. Sunset email workflow over 30-60 days.
```

### Recipe 11: Renewal management
```text
Critical: most CLMs track auto-renewal + non-renewal deadlines.

For each contract:
- Effective date
- Initial term
- Auto-renewal: yes/no
- Renewal length
- Non-renewal notice period
- Notification trigger: notice period + buffer (e.g., 30 days before deadline)

Set up alerts to legal/CFO/contract owner.
Missed deadlines = forced renewals at sometimes worse terms.
```

### Recipe 12: E-sign comparison
| Platform | Strength | Tier |
|---|---|---|
| DocuSign | Most-used; broad integrations; mature API | Enterprise / SMB |
| Adobe Sign | PDF integration; Adobe Creative Cloud users | Enterprise |
| Dropbox Sign | Simple; cheaper | SMB |
| PandaDoc | Built-in CLM | SMB |
| HelloSign (= Dropbox Sign now) | Same as Dropbox Sign | SMB |
| Concord | Built-in to Concord CLM | SMB |

For most users: DocuSign default; Dropbox Sign cheaper alternative.

## Examples

### Example 1: Startup migrating from Gmail/Dropbox to Concord
**Goal:** Get all contracts in one repository with renewal tracking.
**Steps:**
1. Recipe 10 migration.
2. Sign up for Concord (~$10/user/mo).
3. Bulk upload 50 existing contracts.
4. OCR + tag (Recipe 7).
5. Set up renewal alerts.
6. Integrate DocuSign (Recipe 4).
7. Establish new-contract workflow.
8. Train team.

**Result:** Centralized contract management + renewal awareness.

### Example 2: Enterprise SaaS using Ironclad + Salesforce
**Goal:** Auto-generate vendor MSA from Salesforce opportunity.
**Steps:**
1. Recipe 2 + 8 set up Ironclad + Salesforce integration.
2. Build MSA template in Ironclad.
3. Configure workflow: opportunity close → auto-create MSA → legal review → DocuSign send.
4. AI clause extraction on signed contracts (Recipe 7).
5. Renewal dashboard (Recipe 11).
6. Add disclaimer in default ToS / Order Form references.

**Result:** Automated contract creation from sales pipeline.

### Example 3: Integrating contract-review skill into Lexion
**Goal:** Use AI review output in DocuSign-integrated CLM.
**Steps:**
1. Contract intake via Lexion.
2. Run `contract-review-msa-nda-employment` Recipe 2-5 outside Lexion.
3. Upload redline + memo as Lexion attachments.
4. Mark Lexion workflow state to "Negotiation."
5. Lexion → DocuSign for signature.

**Result:** AI-assisted review integrated with CLM workflow.

## Edge cases / gotchas

- **CLM ≠ source of truth for legal interpretation.** CLM holds metadata + records; legal interpretation still requires reading the actual document.
- **AI clause extraction errors.** AI may misclassify "12 months" as effective date vs term. Always spot-check.
- **API rate limits.** Ironclad / Evisort / LinkSquares all have rate caps; batch operations need pagination.
- **E-sign legal validity.** ESIGN Act (2000) + UETA (state-level) + eIDAS (EU) make e-signatures valid for most documents. Exceptions: wills, divorce, court documents.
- **EU-specific e-sign types.** eIDAS distinguishes SES (Simple) / AdES (Advanced) / QES (Qualified). For high-stakes documents (notarized), QES required.
- **DocuSign + Dropbox Sign + Adobe Sign each track audit trails.** Don't manually amend signed PDF; re-execute via the platform.
- **CLM data sovereignty.** EU customers may require EU-hosted CLM. Verify data residency.
- **Vendor lock-in.** Migrating from one CLM to another can be painful; metadata schema differs. Test export/import before committing.
- **API auth complexity.** DocuSign JWT vs OAuth flows; Ironclad token rotation; etc. Plan for token-refresh logic.
- **Cost surprises.** CLM tiers can balloon at >100 user / >1000 contracts thresholds. Negotiate annually.
- **Salesforce integration scope.** Different CLMs offer different Salesforce object-level integrations; verify pre-purchase.
- **Repository search limits.** Free-text search in some CLMs is poor; AI-search via Evisort / LinkSquares stronger.
- **Workflow rigidity.** Highly customized workflows may break on CLM upgrades. Document customizations.

> Warning: **This is informational guidance from an AI agent. Always consult a licensed attorney before relying on CLM-generated workflows or e-signature processes for binding legal documents.**

## Sources

- [Ironclad](https://ironcladapp.com/) — enterprise CLM.
- [Ironclad API](https://developer.ironcladapp.com/) — REST API docs.
- [ContractWorks](https://www.contractworks.com/) — mid-market CLM.
- [Lexion (DocuSign)](https://www.lexion.ai/) — DocuSign-acquired CLM.
- [Evisort](https://www.evisort.com/) — AI-first CLM.
- [LinkSquares](https://linksquares.com/) — AI CLM.
- [Concord](https://www.concord.app/) — startup CLM.
- [PandaDoc](https://www.pandadoc.com/) — SMB contracts.
- [Juro](https://juro.com/) — browser-native CLM.
- [Spotdraft](https://spotdraft.com/) — new AI-first CLM.
- [DocuSign Developer](https://developers.docusign.com/) — e-sign API.
- [Adobe Sign Developer](https://developer.adobe.com/document-services/apis/sign/) — alt e-sign.
- [Dropbox Sign Developer (HelloSign)](https://developers.hellosign.com/) — alt e-sign.
- [ESIGN Act](https://www.law.cornell.edu/uscode/text/15/chapter-96) — US e-signature law.
- [eIDAS Regulation](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv:OJ.L_.2014.257.01.0073.01.ENG) — EU e-signature framework.
- Sister skills: `contract-review-msa-nda-employment`, `robin-spellbook-harvey-ai-contract-review`.
