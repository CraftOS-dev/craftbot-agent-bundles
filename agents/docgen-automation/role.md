# Document Automation — deep reference

This appends to `AGENT.md`. It is **not** in the agent's default context. Grep it when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Contract template authoring playbook", "Proposal automation playbook", "RFP response playbook", "E-signature pipeline playbook", "E-sign compliance checklist", "IDP / doc extraction playbook", "Bulk doc gen playbook", "Smart form deployment playbook", "Redaction playbook", "PDF/UA accessibility checklist", "Multilingual templating playbook", "CLM integration playbook", "Salesforce Conga Composer", "HubSpot doc gen", "Audit trail recipe", "Antipattern catalog", "Reference templates", "SOTA tool reference".

For provenance of any section, see `SOURCES.md` in this bundle and `reference/SOTA_USE_CASES.md`.

---

## Capability reference

Factual lists banished from `soul.md` (they don't drive turn-by-turn decisions but the agent grep-loads them on demand).

### Document types in scope

- **Contracts:** MSA, NDA (mutual / unilateral / multi-party), employment agreement, independent contractor agreement, vendor / SaaS subscription, customer T&C, AUP, DPA, BAA, SLA, license agreement, reseller / channel partner, JV agreement, asset purchase / stock purchase
- **Proposals:** sales proposal, statement of work (SOW), service quote, project proposal, RFP response, RFQ response, grant proposal, partnership proposal
- **RFP / questionnaires:** RFP, RFI, RFQ, security questionnaire (CAIQ / SIG / SIG-Lite), DDQ (due diligence questionnaire), vendor security assessment
- **Customer-facing forms:** intake form, onboarding form, application form, signup form, registration form, NPS / CSAT survey
- **Internal forms:** expense report, time-off request, equipment request, vendor request, contractor onboarding, employee onboarding
- **Operational docs:** invoice, receipt, purchase order, packing slip, shipping label, delivery confirmation
- **Compliance docs:** privacy policy, cookie policy, terms of service, ToS update notice, DSAR request response, breach notification
- **Marketing / sales collateral:** one-pager, case study, white paper, brochure, sales deck (PPTX)
- **HR docs:** offer letter, employment contract, NDA, IP assignment, separation agreement, severance agreement, reference letter

### Doc-automation platforms in scope

- **Template authoring:** Documate, HotDocs, NetDocuments, Templafy, Docassemble (FOSS), Conga Document Generation, DocuSign Gen, PandaDoc Builder, DocSpring, PDFmonkey, Anvil
- **Proposal:** PandaDoc, Proposify, Qwilr, Better Proposals, GetAccept, Bonsai, HelloBonsai
- **RFP response:** Loopio, Responsive (RFPIO), Qvidian, Ombud, Arphie
- **CLM:** Ironclad, ContractWorks, Lexion (DocuSign), Concord, LinkSquares, Evisort, Agiloft, Conga Contracts, SirionLabs
- **E-signature:** DocuSign, Adobe Sign (Acrobat Sign), Dropbox Sign (HelloSign), SignNow, eversign, SignWell, RightSignature, Conga Sign, OneSpan, OpenSignature
- **IDP / AI extraction:** Hyperscience, Rossum, Klippa, AWS Textract, Azure Document Intelligence, Google Document AI, Veryfi, Mindee, Nanonets, AbbyyFR
- **PDF tools:** Adobe Acrobat Pro DC, Foxit, PDFTron / Apryse, PDF.co API, pdf-lib (JS), jsPDF, ReportLab (Python), WeasyPrint, Prince
- **Smart forms:** Jotform, Formstack, Typeform, Tally, Cognito Forms, Microsoft Forms, Google Forms

### Template libraries to start from

- **Common Paper** — NDA, Cloud Service, DPA, AUP, MSA (standardized + open)
- **Bonterms** — Cloud Terms, AUP, DPA, SLA modules (open)
- **YC Documents** — SAFE (post-money default), MFN side letter, pro-rata side letter, advisor agreement
- **Cooley GO** — equity comp, founders stock, contractor, consulting, employment, IP assignment
- **Stripe Atlas** — incorporation-bundle templates
- **Clerky** — cap-table + equity + fundraising templates
- **NVCA** — Series A canonical docs (term sheet, stock purchase agreement, IRA, voting agreement, ROFR / co-sale agreement)
- **Adobe Sign sample templates** — basic e-sign templates
- **DocuSign Standards Based Signatures** — EU eIDAS QES samples
- **HHS HIPAA Sample BAA** — HIPAA business associate agreement
- **EU Commission SCC 2021/914** — cross-border data transfer module set
- **AICPA TSP 100** — SOC 2 trust services criteria

### Compliance regimes for e-signature

- **US federal:** ESIGN Act (15 USC §7001-7031), UETA (47 states + DC adopted)
- **US state:** state e-signature statutes (NY ESRA, IL Electronic Commerce Security Act, etc.)
- **EU:** eIDAS Regulation (910/2014) + eIDAS 2.0 (2024) — Simple / Advanced / Qualified Electronic Signature tiers + EUDI Wallet
- **UK:** Electronic Communications Act 2000 + UK eIDAS (post-Brexit)
- **Industry-specific:** 21 CFR Part 11 (FDA / pharma), HIPAA (electronic PHI signatures), DoD CMMC, FedRAMP / FISMA e-sign
- **Remote Online Notarization (RON):** 40+ US states adopted (variants of MBA model / RULONA); requires ID verification + KBA + audio/video session

### Pricing model in scope (for dynamic proposal generation)

- Per-seat (named user, concurrent user)
- Per-usage (API calls, GB stored, transactions)
- Tiered (Free / Pro / Enterprise with feature gates)
- Volume / bracket pricing (per-unit cost decreases at thresholds)
- Bundle / package pricing
- One-time + recurring split (setup fee + monthly)
- Subscription + overage (committed minimum + per-unit overage)
- Outcome-based (% of saved spend, % of incremental revenue)

---

## Contract template authoring playbook

1. **Confirm doc type + base template + jurisdiction + side.** MSA / NDA / employment / vendor? Bonterms / Common Paper / YC / org's own template? US state / EU country / UK / Canada? Customer-side or supplier-side?
2. **Identify variable fields + conditional branches.** List every placeholder (party name, address, effective date, fees, term, governing law). List every conditional clause that fires based on a variable (jurisdiction → CA non-compete carve-out; deal size → cap on liability; product mix → SOC 2 addendum; customer tier → premium SLA).
3. **Choose authoring engine:**
   - **Documate / HotDocs** — best for interview-driven authoring + legal industry standard. Web app + REST API.
   - **Docassemble (FOSS)** — best when you need full Python extensibility + self-hosting.
   - **Templafy** — best when brand consistency is the headline requirement + Office-native.
   - **docxtemplater (Node) / python-docx-template (Python)** — best when no SaaS budget; embeds placeholders + loops in Word docs.
   - **Jinja2 + WeasyPrint / Pandoc** — best when HTML-source is preferred; renders pixel-perfect PDF.
4. **Author the master template.** Use clear placeholder syntax (`{{customer.name}}` mustache-style is the de facto standard). Conditional blocks use `{% if customer.is_enterprise %}...{% endif %}`. Loops over child records: `{% for line in line_items %}...{% endfor %}`.
5. **Version-control in `github`.** Initial commit at `v0.1.0`; tag every change. PR review for clause edits. Lint with Vale + brand-voice config.
6. **Sample-render.** Render 2-3 samples hitting different conditional branches. Verify output by hand.
7. **Document the merge field schema.** A `template_schema.yaml` or `template_schema.json` listing every required + optional field + type. Downstream callers (CRM, form, CSV import) honor the schema.
8. **Hand off to `legal-counsel` for binding-language review.** Always.

### Concrete: Bonterms-based Cloud Terms with conditional SOC 2 addendum

```docx
[Title: Cloud Services Agreement]

This Cloud Services Agreement (the "Agreement") is entered into as of {{effective_date|format("MMMM D, YYYY")}}
by and between {{customer.name}}, a {{customer.entity_state}} {{customer.entity_type}}
("Customer"), and {{vendor.name}}, a {{vendor.entity_state}} corporation ("Vendor").

1. SERVICES
   Vendor will provide Customer with access to the {{product.name}} cloud service
   (the "Service") as described in the Order Form attached as Exhibit A.

{% if customer.requires_soc2 %}
2. SECURITY ADDENDUM
   This Agreement incorporates the SOC 2 Security Addendum attached as Exhibit B,
   which sets forth Vendor's security obligations under AICPA Trust Services
   Criteria.
{% endif %}

...

{% if customer.jurisdiction == "California" %}
Governing law: This Agreement shall be governed by the laws of the State of
California, without regard to its conflict of laws principles.
{% elif customer.jurisdiction == "Delaware" %}
Governing law: This Agreement shall be governed by the laws of the State of
Delaware, without regard to its conflict of laws principles.
{% else %}
Governing law: This Agreement shall be governed by the laws of {{customer.jurisdiction}},
without regard to its conflict of laws principles.
{% endif %}
```

Versioned in Git at `templates/cloud-terms/v2.4.0.docx`. Rendered via:

```bash
# Python — python-docx-template
pip install docxtpl
python -c "
from docxtpl import DocxTemplate
tpl = DocxTemplate('templates/cloud-terms/v2.4.0.docx')
tpl.render({
  'effective_date': '2026-06-15',
  'customer': {'name': 'Acme Corp', 'entity_state': 'Delaware', 'entity_type': 'C-corp',
               'requires_soc2': True, 'jurisdiction': 'California'},
  'vendor': {'name': 'WidgetCo Inc', 'entity_state': 'Delaware'},
  'product': {'name': 'WidgetCloud Pro'}
})
tpl.save('out/acme-cloud-terms-2026-06-15.docx')
"
```

---

## Proposal automation playbook

1. **Confirm platform.** PandaDoc (broadest 2026 default), Proposify (proposal-focused), Qwilr (interactive web), Better Proposals, GetAccept. For Salesforce-native shops: Conga Composer.
2. **Confirm CRM source.** HubSpot deal record / Salesforce opportunity / standalone. Trigger: deal stage change or manual rep "Generate Proposal" button.
3. **Build content library.** Reusable blocks: company overview, product overview (per SKU), pricing rate card, terms snippets, signature block. Tag for conditional inclusion.
4. **Build the master template.** PandaDoc Builder / Proposify editor. Bind merge fields (`[Contact.FirstName]`, `[Deal.Amount]`). Embed dynamic pricing tables.
5. **Wire CRM trigger.** PandaDoc has native HubSpot + Salesforce integrations; for custom CRMs use webhook → POST `/v3/documents`. Salesforce: Conga Composer URL button.
6. **Embed e-sign.** PandaDoc / Proposify / Qwilr include e-sign natively. For separate DocuSign / Adobe Sign: chain proposal completion → e-sign envelope creation.
7. **Configure analytics.** Time-to-sign, drop-off per section, view duration. PandaDoc has native; pipe events to `posthog-mcp` / `mixpanel-mcp` via webhook for custom dashboards.
8. **Test against one real deal.** Render → counterparty view → sign → archive. Verify the full pipeline.

### Concrete: PandaDoc REST creation

```bash
# Create a document from a template + CRM data
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
      {"name": "Deal.Amount", "value": "$120,000"}
    ],
    "pricing_tables": [{
      "name": "Pricing Table",
      "data_merge": false,
      "options": {"currency": "USD"},
      "sections": [{
        "title": "Subscription",
        "rows": [
          {"options": {"qty": 50, "price": 200}, "data": {"name": "WidgetCloud Pro - per seat"}}
        ]
      }]
    }]
  }'
# Response includes document.id — use to send via /documents/{id}/send
```

---

## RFP response playbook

1. **Confirm RFP format + delivery.** Word / Excel / PDF / portal-only (e.g., RFP360). Submission deadline + Q&A window.
2. **Extract questions.** Structured Word/Excel → parse via `python-docx` / `openpyxl`. Scanned PDF → `gemini-ocr-mcp` / `mistral-ocr-mcp`. Portal-only → `playwright-mcp` scrape.
3. **Match to answer library.** Loopio / Responsive (RFPIO) auto-match incoming questions to canonical answers; confidence score per match. CSV-based fallback: Python `sentence-transformers` + cosine similarity.
4. **Route low-confidence matches for SME review.** Confidence < 0.7 → flag for SME; `slack-mcp` notifies subject-matter expert.
5. **Assemble final response.** Populate doc with auto-matched + SME-reviewed answers. Preserve formatting (header / footer / page numbers).
6. **Lint for brand voice.** Vale config + brand-voice rules; ensure consistency across answers from different SMEs.
7. **Sign-off + submit.** Final review by sales / pre-sales lead. Submit via portal (Playwright) or email (`gmail-mcp` / `outlook-mcp`).
8. **Update answer library.** Mark answers reused; add SME-edited variants to canonical library for next time.

### Concrete: Responsive (RFPIO) API auto-fill

```bash
# Submit an RFP for auto-fill
curl -X POST https://api.responsive.io/v1/projects \
  -H "Authorization: Bearer $RESPONSIVE_TOKEN" \
  -F "file=@input_rfp.xlsx" \
  -F "name=Acme Corp RFP 2026-Q2" \
  -F "auto_fill=true" \
  -F "confidence_threshold=0.7"
# Returns project_id; poll for completion
curl https://api.responsive.io/v1/projects/$PROJECT_ID/status \
  -H "Authorization: Bearer $RESPONSIVE_TOKEN"
# Download populated response
curl https://api.responsive.io/v1/projects/$PROJECT_ID/export \
  -H "Authorization: Bearer $RESPONSIVE_TOKEN" \
  -o output_response.xlsx
```

---

## E-signature pipeline playbook

1. **Confirm platform + auth.** DocuSign (default), Adobe Sign, Dropbox Sign, PandaDoc, SignNow. JWT for unattended; OAuth for end-user.
2. **Pick envelope strategy.** Template-based (canonical templates with named recipient roles) vs ad-hoc (PDF + tagged signature fields). Template is preferred for repeated workflows.
3. **Build envelope.** Documents + recipients + signature/initial/date/text tabs + routing order + email subject/body. Set reminders (3-day + 7-day) + expiration (30-day default).
4. **Configure webhook (Connect).** DocuSign Connect → URL endpoint that receives envelope events (sent, delivered, completed, declined, voided). Use to trigger archive flow.
5. **Send envelope.** POST `/restapi/v2.1/accounts/{acctId}/envelopes` with `status=sent`. Returns envelope ID + URI.
6. **On completion webhook:**
   - Download completed PDF: `GET /envelopes/{envelopeId}/documents/combined`
   - Download Certificate of Completion: `GET /envelopes/{envelopeId}/documents/certificate`
   - Archive both in `google-drive-mcp` / `aws-s3-mcp` / Notion
7. **OpenTimestamps (optional but recommended for high-stakes).** Hash the completed PDF + cert; submit to `ots stamp`; archive proof for evidentiary value.

### Concrete: DocuSign envelope creation (JWT)

```python
# pip install docusign-esign
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Document, Signer, SignHere, Tabs, Recipients
import base64

# JWT auth (unattended)
api_client = ApiClient()
api_client.host = "https://demo.docusign.net/restapi"  # or account.docusign.net
api_client.set_oauth_host_name("account-d.docusign.com")
token = api_client.request_jwt_user_token(
    client_id=INTEGRATION_KEY,
    user_id=USER_ID,
    oauth_host_name="account-d.docusign.com",
    private_key_bytes=open("private.key", "rb").read(),
    expires_in=3600,
    scopes=["signature", "impersonation"]
)
api_client.set_default_header("Authorization", f"Bearer {token.access_token}")

# Build envelope
with open("contract.pdf", "rb") as f:
    pdf_bytes = base64.b64encode(f.read()).decode("ascii")

envelope_def = EnvelopeDefinition(
    email_subject="Please sign: Cloud Services Agreement",
    documents=[Document(document_base64=pdf_bytes, name="Contract", file_extension="pdf", document_id="1")],
    recipients=Recipients(signers=[
        Signer(
            email="buyer@acme.com", name="Jane Smith", recipient_id="1", routing_order="1",
            tabs=Tabs(sign_here_tabs=[SignHere(anchor_string="/sn1/", anchor_y_offset="10", anchor_units="pixels")])
        )
    ]),
    status="sent"
)

envelopes_api = EnvelopesApi(api_client)
result = envelopes_api.create_envelope(account_id=ACCOUNT_ID, envelope_definition=envelope_def)
print(f"Envelope sent: {result.envelope_id}")
```

---

## E-sign compliance checklist

### US (ESIGN Act + UETA)

- [ ] Consumer consent to electronic records — separately captured, with consent to do business electronically
- [ ] Intent to sign — captured via "I agree" / signature ceremony
- [ ] Association of signature with record — envelope tags ties signer to specific document
- [ ] Record retention — signed record + audit trail preserved + retrievable
- [ ] Attribution — auth method documented (email + access code, SMS, KBA, ID verification)
- [ ] State-specific carve-outs (real estate, wills, trusts, certain UCC) — check state law before relying on e-sign

### EU (eIDAS Regulation 910/2014 + eIDAS 2.0)

- [ ] Choose signature tier appropriate to risk:
  - **Simple Electronic Signature (SES)** — broad applicability; lowest assurance (e.g., typed name, scanned signature)
  - **Advanced Electronic Signature (AES)** — uniquely linked + capable of identifying signer + signer control + linked to data
  - **Qualified Electronic Signature (QES)** — AES + Qualified Certificate from EU Trust List provider + Qualified Signature Creation Device
- [ ] For QES: use EU Trust List provider (e.g., Adobe Sign Trust Services, DocuSign EU Advanced/Qualified)
- [ ] eIDAS 2.0 EUDI Wallet — for cross-border identity (rolling out 2024-2026)
- [ ] Article 25 — court must not deny legal effect solely because signature is electronic
- [ ] Sector-specific: GDPR Art. 7 for consent; eDelivery for cross-border delivery

### Industry overlays

- [ ] **21 CFR Part 11 (FDA / pharma):** validated systems + audit trails + electronic signatures with secured links to records
- [ ] **HIPAA:** encrypted transmission + access controls + audit logs for PHI-related signatures
- [ ] **CMMC / FedRAMP:** signature platforms certified to required level
- [ ] **Real estate (US):** state law varies — many states require RON for notarized transactions

### Remote Online Notarization (RON)

- [ ] State adoption (40+ states + DC as of 2026; RULONA or MBA model)
- [ ] Notary credential — commissioned in the state where notary is physically located
- [ ] ID verification (KBA + government-issued ID)
- [ ] Audio/video recording — preserved per statute (typically 5-10 years)
- [ ] Tamper-evident technology with audit trail

---

## IDP / doc extraction playbook

1. **Confirm input + target.** Single doc / batch / streaming? Structured form / semi-structured invoice / unstructured contract / scanned receipt?
2. **Pick engine:**
   - **AWS Textract** — AWS shops; FORMS + TABLES + QUERIES API (ask specific Qs of doc).
   - **Azure Document Intelligence** — Microsoft shops; prebuilt models (invoice, receipt, ID, tax W-2 / 1099, contract, layout).
   - **Google Document AI** — GCP shops; 200+ prebuilt processors; custom training via Vertex AI.
   - **Hyperscience** — high-volume mixed-format + handwriting; enterprise.
   - **Rossum** — invoice-to-ERP specialized.
   - **Veryfi** — receipts + W-2 / 1099 / bills; sub-second.
   - **Mindee** — invoices + receipts + IDs (SDK + cloud); fastest dev experience.
   - **Klippa** — receipts + ID + KYC.
   - **Nanonets** — custom-trained vertical extractors.
   - **Gemini OCR / Mistral OCR / GPT-4 Vision** — best for free-form / layout-aware extraction at single-doc scale (MCP available).
3. **Run extraction.** API call with file → JSON result with field names + values + confidence + bounding boxes.
4. **Validate output.** Required fields present? Types correct? Values within range? Low-confidence rows flagged.
5. **Post-process.** Currency normalization; date format normalization; entity matching (vendor lookup); duplicate detection.
6. **Export.** Structured JSON → ERP / accounting / CRM. Confidence histogram for QA.

### Concrete: AWS Textract QUERIES API for contract extraction

```bash
aws textract analyze-document \
  --document '{"S3Object":{"Bucket":"contracts","Name":"msa-2026-06.pdf"}}' \
  --feature-types '["FORMS", "TABLES", "QUERIES"]' \
  --queries-config '{
    "Queries":[
      {"Text":"What is the effective date?","Alias":"effective_date"},
      {"Text":"What is the term length in months?","Alias":"term_months"},
      {"Text":"What is the governing law jurisdiction?","Alias":"governing_law"},
      {"Text":"What is the limitation of liability cap?","Alias":"liability_cap"},
      {"Text":"Who are the parties?","Alias":"parties"}
    ]
  }' > extracted.json
# Parse Block array; filter QUERY_RESULT children of each QUERY
```

### Concrete: Azure Document Intelligence — prebuilt invoice model

```bash
curl -X POST "https://${AZURE_DI_ENDPOINT}/documentintelligence/documentModels/prebuilt-invoice:analyze?api-version=2024-07-31-preview" \
  -H "Ocp-Apim-Subscription-Key: ${AZURE_DI_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"urlSource":"https://example.com/invoice.pdf"}'
# Poll the operation-location URL for result
```

---

## Bulk doc gen playbook

1. **Confirm template + data + output.** Template version + CSV / Google Sheets / SQL source + PDF / docx / signed envelope output + delivery (S3 signed URL / email / portal).
2. **Validate CSV.** Required columns present; types match schema; line count reconciled; no SQL-injection-ish characters in fields used in shell commands.
3. **Pick pipeline scale:**
   - **< 100 docs:** loop in Python with docxtpl + WeasyPrint, render sequentially. Done in seconds.
   - **100-1000 docs:** parallel render via `concurrent.futures` or `asyncio` + WeasyPrint; or batch POST to DocSpring / PDFmonkey.
   - **1000-10k docs:** worker queue (Celery / BullMQ / Sidekiq) + S3 storage; render workers scale horizontally.
   - **10k+ docs:** managed service (DocSpring, PDFmonkey, Documate batch) or Lambda + S3 fan-out.
4. **Render + store.** Each doc → S3 with signed URL or Drive folder. Track per-row outcome.
5. **Ship manifest.** `manifest.csv` columns: `input_row_id`, `output_url`, `status`, `envelope_id`, `error_message`. This is the audit deliverable.

### Concrete: Python bulk render with docxtpl + WeasyPrint

```python
# pip install docxtpl weasyprint pandas boto3
import pandas as pd
from docxtpl import DocxTemplate
import subprocess
import boto3
import os

s3 = boto3.client("s3")
manifest = []

df = pd.read_csv("input/customers.csv")
tpl_path = "templates/renewal-letter-v2.1.0.docx"

for _, row in df.iterrows():
    out_docx = f"out/renewal-{row['customer_id']}.docx"
    out_pdf = f"out/renewal-{row['customer_id']}.pdf"
    s3_key = f"renewals/2026-q2/{row['customer_id']}.pdf"

    try:
        tpl = DocxTemplate(tpl_path)
        tpl.render(row.to_dict())
        tpl.save(out_docx)

        # Convert docx → PDF via LibreOffice headless
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf",
                        "--outdir", "out", out_docx], check=True)

        s3.upload_file(out_pdf, "docs-bucket", s3_key)
        url = s3.generate_presigned_url("get_object",
              Params={"Bucket": "docs-bucket", "Key": s3_key}, ExpiresIn=86400)
        manifest.append({"customer_id": row["customer_id"], "status": "ok", "url": url, "error": ""})
    except Exception as e:
        manifest.append({"customer_id": row["customer_id"], "status": "error", "url": "", "error": str(e)})

pd.DataFrame(manifest).to_csv("out/manifest.csv", index=False)
print(f"Bulk run complete: {sum(1 for m in manifest if m['status']=='ok')}/{len(manifest)} succeeded")
```

---

## Smart form deployment playbook

1. **Confirm platform.** Jotform (broad + conditional logic + e-sign), Formstack (HIPAA-eligible, enterprise), Typeform (conversational UX), Tally (free + Notion-style), Cognito Forms (advanced rules).
2. **Build form schema.** Fields + types + validation + conditional show/hide rules + multi-page flow.
3. **Configure submission webhook.** Webhook URL → POST endpoint receives form data; trigger downstream action (PandaDoc doc gen, DocuSign envelope, HubSpot deal creation).
4. **Wire downstream.** Webhook handler builds payload + calls PandaDoc / DocSpring / DocuSign / HubSpot API.
5. **Test end-to-end via `playwright-mcp`.** Script fills form → submits → asserts webhook delivered → asserts doc rendered → asserts envelope sent (if applicable).
6. **Deploy.** Publish form URL. For embedded: provide HTML snippet.

### Concrete: Jotform → DocSpring template render via webhook

```python
# webhook receiver (FastAPI)
from fastapi import FastAPI, Request
import httpx
app = FastAPI()

@app.post("/webhook/jotform-onboarding")
async def jotform_webhook(req: Request):
    submission = await req.json()
    # Map Jotform fields to template schema
    payload = {
        "data": {
            "customer_name": submission["q3_customerName"],
            "customer_email": submission["q4_customerEmail"],
            "effective_date": submission["q5_effectiveDate"],
            "annual_fee": submission["q6_annualFee"],
        }
    }
    # Submit to DocSpring → returns PDF URL
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"https://api.docspring.com/api/v1/templates/{TPL_ID}/submissions",
            json=payload,
            headers={"Authorization": f"Bearer {DOCSPRING_TOKEN}"}
        )
    submission_id = r.json()["submission"]["id"]
    return {"status": "ok", "submission_id": submission_id}
```

---

## Redaction playbook

1. **Confirm scope.** PII categories (PERSON, EMAIL_ADDRESS, US_SSN, US_BANK_NUMBER, CREDIT_CARD, PHONE_NUMBER, IP_ADDRESS, DATE_TIME, LOCATION) + custom regex patterns + bound vs unbound.
2. **Choose engine:**
   - **Microsoft Presidio** — open-source, fast, customizable + Python SDK; default for code-driven redaction.
   - **AWS Comprehend Detect PII** / **Comprehend Medical Detect PHI** — AWS-native; broad language support.
   - **Google DLP** — GCP-native; deep template + custom infoType library.
   - **Adobe Acrobat Pro Redaction tool** — manual one-off; metadata cleansing built in.
3. **Run detection + redaction.** Replace detected spans with `<REDACTED-PERSON>` or solid black bars in PDF.
4. **Strip metadata.** PDF: `pdfcpu` / `qpdf --linearize --object-streams=preserve --decrypt= ...` to strip XMP / DocInfo. Word: clear document properties + comments + tracked changes.
5. **Re-scan to verify.** Run the same engine again on the redacted output; assert zero detections.
6. **Manual review on high-stakes docs.** Eyeball + spot-check before delivery.

### Concrete: Presidio redaction

```python
# pip install presidio-analyzer presidio-anonymizer
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

text = open("input/contract.txt").read()
results = analyzer.analyze(text=text, entities=["PERSON","EMAIL_ADDRESS","US_SSN","PHONE_NUMBER","CREDIT_CARD","LOCATION"], language="en")
redacted = anonymizer.anonymize(text=text, analyzer_results=results,
    operators={"DEFAULT": OperatorConfig("replace", {"new_value": "<REDACTED>"})})

with open("out/contract-redacted.txt","w") as f:
    f.write(redacted.text)

# Re-scan to verify
results_check = analyzer.analyze(text=redacted.text, entities=["PERSON","EMAIL_ADDRESS","US_SSN","PHONE_NUMBER","CREDIT_CARD","LOCATION"], language="en")
assert len(results_check) == 0, f"Redaction incomplete: {len(results_check)} remaining detections"
```

---

## PDF/UA accessibility checklist

PDF/UA (ISO 14289) + WCAG 2.2 AA conformance:

- [ ] Tagged PDF — every visible content element has a tag (paragraph, heading, list, table, figure)
- [ ] Reading order correct — tags follow logical reading sequence (not visual layout if different)
- [ ] Headings hierarchical — H1 → H2 → H3 with no skipped levels
- [ ] Alternative text on every figure / image (alt-empty for decorative)
- [ ] Table headers tagged as `<TH>` with `Scope` attribute (Row / Column)
- [ ] Language metadata set — document-level + per-span where mixed
- [ ] Color contrast ≥ 4.5:1 for body text (WCAG 2.2 AA)
- [ ] No flashing content (PDF/UA-1 doesn't allow)
- [ ] Tab order matches reading order
- [ ] Bookmarks present for documents > 9 pages
- [ ] Form fields have accessible names + tooltips
- [ ] Document title set in metadata (not just filename)
- [ ] Encryption preserves accessibility (don't restrict accessibility-mode PDFs)

### Validation

```bash
# veraPDF — PDF/UA-1 conformance check
verapdf --flavour ua1 --format json input/contract.pdf > validation.json
# Returns { "isCompliant": true/false, "validationResults": [...] }

# Adobe Acrobat Pro accessibility check
# (interactive only; no CLI)

# Pa11y for HTML source
pa11y --standard WCAG2AA https://example.com/doc.html
```

---

## Multilingual templating playbook

1. **Confirm langs + scope.** EN + DE + FR + ES + IT? + Asian (JA, ZH, KO)? Per-language template variants or unified template with translation pass?
2. **For boilerplate-heavy contracts:** maintain `template.en.docx`, `template.de.docx`, `template.fr.docx` — each separately reviewed by counsel in the target jurisdiction. Only the bespoke fields (party name, fee) are merged. Don't translate stable boilerplate every render.
3. **For proposals + marketing collateral:** single source + DeepL translation pass. `tag_handling=html` for HTML; `tag_handling=xml` for XLIFF.
4. **Translation memory:** Lokalise / Crowdin for repeat translations to maintain consistency across docs.
5. **Locale formatting:** dates (DD/MM/YYYY vs MM/DD/YYYY), currency (€1.234,56 vs $1,234.56), addresses, number formatting. Use ICU locale data or `babel` Python lib.
6. **RTL languages:** Arabic, Hebrew — verify template engine supports RTL + bidi text. Word docx handles natively; HTML+CSS needs `dir="rtl"`.

### Concrete: DeepL translation with formatting preservation

```bash
curl -X POST https://api-free.deepl.com/v2/translate \
  -H "Authorization: DeepL-Auth-Key $DEEPL_KEY" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=<p>The customer agrees to the <strong>terms of service</strong>.</p>" \
  -d "target_lang=DE" \
  -d "tag_handling=html" \
  -d "formality=more"
# Response: {"translations":[{"detected_source_language":"EN","text":"<p>Der Kunde stimmt den <strong>Nutzungsbedingungen</strong> zu.</p>"}]}
```

---

## CLM integration playbook

1. **Confirm recipient's CLM.** Ironclad / ContractWorks / Lexion / Concord / LinkSquares / Evisort / Conga Contracts / Agiloft / SirionLabs. If none, recommend ContractWorks for SMB or Ironclad for mid-market+.
2. **Authenticate.** Most use API tokens or OAuth. Ironclad: API key; LinkSquares: API key; ContractWorks: API key + workspace ID.
3. **Choose workflow:**
   - **Pre-execution:** rendered template → CLM staging → review/approval workflow → e-sign envelope creation.
   - **Post-execution:** signed PDF → CLM repository (with extracted metadata via the CLM's AI extractor).
4. **Wire integration:**
   - Render template → upload to CLM (`POST /workflows/{id}/launches` for Ironclad).
   - Approval workflow inside CLM (legal review → finance review → counterparty send).
   - On approval, trigger e-sign envelope.
5. **Extract clauses post-execution.** LinkSquares / Evisort auto-extract clauses; export to data warehouse for analysis.

### Concrete: Ironclad workflow launch

```bash
curl -X POST https://ironcladapp.com/public/api/v1/workflows \
  -H "Authorization: Bearer $IRONCLAD_TOKEN" \
  -H "Content-Type: multipart/form-data" \
  -F 'workflowTemplateId=wftpl_abc123' \
  -F 'attributes={
    "counterpartyName": "Acme Corp",
    "effectiveDate": "2026-06-15",
    "contractValue": 120000,
    "currency": "USD",
    "governingLaw": "Delaware"
  }' \
  -F 'attachments[]=@templates/msa-acme.pdf'
# Returns workflow_id; track status via /workflows/{workflow_id}
```

---

## Salesforce Conga Composer

1. **Confirm Conga license + Salesforce org.** Conga Composer is the dominant Salesforce-native doc-gen tool.
2. **Build Conga template.** Word / Excel / PPT / PDF source with `{{Account.Name}}`, `{{Opportunity.Amount}}`-style merge fields + conditional sections.
3. **Composer button URL.** Configure Salesforce custom button with Composer URL. User clicks → Composer reads record → renders → optionally signs.
4. **Composer URL structure:**
   ```
   https://composer.congamerge.com/Composer8/index.html?sessionId={!API.Session_ID}
   &serverUrl={!API.Partner_Server_URL_280}
   &id={!Opportunity.Id}
   &templateId=a01XXXXXXXXXXXX
   &OFN=Proposal-{!Opportunity.Name}
   &DefaultPDF=1
   &EmailToId={!Opportunity.Owner.Id}
   &DS7=8   <-- DocuSign for Salesforce e-sign
   ```
5. **For non-Conga shops:** Salesforce Apex callout → PandaDoc / DocSpring / DocuSign Gen.

---

## HubSpot doc gen

1. **Confirm HubSpot tier.** Sales Hub Starter+ for Quotes; Marketplace integrations for PandaDoc / Proposify / DocuSign embedded in deal record.
2. **HubSpot Quotes (native):** simplest; create quote on deal → publish → e-sign via integrated DocuSign / HubSpot eSignatures.
3. **PandaDoc + HubSpot:** Marketplace integration; trigger PandaDoc on deal stage change. Best for richer proposals.
4. **Webhook approach:** HubSpot Workflow → webhook → custom doc gen endpoint → POST result back to deal record.

### Concrete: HubSpot Quotes API

```bash
curl -X POST https://api.hubapi.com/crm/v3/objects/quotes \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "hs_title": "WidgetCloud Pro Proposal - Acme Corp",
      "hs_expiration_date": "2026-07-15T00:00:00Z",
      "hs_status": "DRAFT",
      "hs_terms": "Net 30",
      "hs_currency": "USD"
    },
    "associations": [
      {"to": {"id": "$DEAL_ID"}, "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 64}]}
    ]
  }'
```

---

## Audit trail recipe

```python
# After DocuSign envelope completion webhook fires
import docusign_esign as dse
import boto3
import hashlib
import subprocess

api_client = setup_jwt_client()  # see e-sign pipeline
envelopes_api = dse.EnvelopesApi(api_client)

# 1. Download combined PDF (all signed docs)
pdf_path = "archive/envelopes/{envelope_id}/combined.pdf".format(envelope_id=envelope_id)
combined_pdf = envelopes_api.get_document(ACCOUNT_ID, "combined", envelope_id)
with open(pdf_path, "wb") as f: f.write(combined_pdf)

# 2. Download Certificate of Completion
cert_path = "archive/envelopes/{envelope_id}/certificate.pdf".format(envelope_id=envelope_id)
cert_pdf = envelopes_api.get_document(ACCOUNT_ID, "certificate", envelope_id)
with open(cert_path, "wb") as f: f.write(cert_pdf)

# 3. Hash both for evidentiary chain
combined_sha = hashlib.sha256(open(pdf_path,"rb").read()).hexdigest()
cert_sha     = hashlib.sha256(open(cert_path,"rb").read()).hexdigest()

# 4. OpenTimestamps proof (free + decentralized)
subprocess.run(["ots", "stamp", pdf_path], check=True)
subprocess.run(["ots", "stamp", cert_path], check=True)

# 5. Upload to S3 + record metadata
s3 = boto3.client("s3")
s3.upload_file(pdf_path, "contracts-archive", f"envelopes/{envelope_id}/combined.pdf")
s3.upload_file(cert_path, "contracts-archive", f"envelopes/{envelope_id}/certificate.pdf")
s3.upload_file(f"{pdf_path}.ots", "contracts-archive", f"envelopes/{envelope_id}/combined.pdf.ots")

# 6. Notion audit log row
# notion-mcp: append row with envelope_id, signers, completion_ts, combined_sha, cert_sha, s3_uris
```

---

## Antipattern catalog

### Antipattern 1: Find-and-replace at scale

**BAD:** 47 personalized renewal letters generated via `sed -i "s/\{customer\}/$NAME/g" template.docx`.
**Why bad:** Breaks on names with special chars; misses fields; produces inconsistent output. No conditional logic, no audit trail, no error log.
**GOOD:** Conditional template with docxtemplater / python-docx-template; CSV input; manifest.csv output; error-row logging.

### Antipattern 2: Unsigned binding-language drafts at scale

**BAD:** Bulk-send 10k contract drafts to customers with auto-generated indemnity clauses, no legal review.
**Why bad:** Unreviewed binding language exposes the org to enforceability + UPL risk; one bad clause replicates 10k times.
**GOOD:** Template authored from Bonterms / Common Paper base; reviewed by `legal-counsel`; tagged at `v3.2.0`; bulk-send sends from the versioned template only.

### Antipattern 3: E-sign without audit certificate archive

**BAD:** Send DocuSign envelope; download signed PDF only on completion; throw away the Certificate of Completion.
**Why bad:** The Certificate is the evidentiary chain (timestamps + IP + auth method + signer identity). Without it, the signature is uncorroborated in dispute.
**GOOD:** On completion webhook, download both `/documents/combined` AND `/documents/certificate`; archive together; hash + OpenTimestamps for high-stakes.

### Antipattern 4: Redaction without re-scan

**BAD:** Replace PII spans with black bars; deliver redacted PDF.
**Why bad:** Metadata (XMP / DocInfo) still has author + edit history; form fields may not be redacted; image-based text untouched. Single-pass leaks.
**GOOD:** Strip metadata via `pdfcpu` / `qpdf` / Acrobat; re-scan via Presidio / Comprehend / DLP; assert zero remaining detections; manual eyeball on high-stakes.

### Antipattern 5: PDF/UA "tagged" claim without veraPDF validation

**BAD:** Mark a PDF as "accessible" because the source Word doc had heading styles.
**Why bad:** Tagging at export can fail; reading order may be wrong; alt text may be missing; tables may not have headers. Untested.
**GOOD:** Run `verapdf --flavour ua1`; fix every failure; re-validate; ship the validation report alongside the PDF.

### Antipattern 6: Smart form deployed without end-to-end test

**BAD:** Build Jotform → webhook → PandaDoc pipeline; publish form; tell users to fill it in.
**Why bad:** Webhook config drift, field name mismatches, PandaDoc template version mismatch — all silent failures. Submissions vanish.
**GOOD:** Playwright script fills form → asserts webhook delivered → asserts doc rendered → asserts envelope sent. Re-run on every template version bump.

### Antipattern 7: Bulk doc gen without manifest

**BAD:** Render 5,000 personalized PDFs → upload to S3 → email user the bucket prefix.
**Why bad:** No way to verify all rows rendered; no error log; failed rows silently dropped; no input→output mapping.
**GOOD:** `manifest.csv` with one row per input including `output_url`, `status` (ok/error), `error_message`, `envelope_id` if applicable. Ship alongside the bucket.

### Antipattern 8: Salesforce Conga Composer URL committed with sessionId

**BAD:** Hard-coded Composer URL in the Salesforce button with embedded sessionId.
**Why bad:** sessionId is per-user + per-session; URL fails for everyone else. Also a security smell.
**GOOD:** Use `{!API.Session_ID}` + `{!API.Partner_Server_URL_280}` merge fields; Composer reads them at click time per user.

### Antipattern 9: DocuSign tabs by absolute coordinates on a versioned template

**BAD:** Sign field at `xPosition=372, yPosition=648` on every send.
**Why bad:** Template version bump shifts layout; signature lands in the wrong place.
**GOOD:** Anchor tabs (`anchorString="/sn1/"` with explicit anchor text in template); resilient to layout changes.

### Antipattern 10: Translate stable contract boilerplate fresh on every render

**BAD:** Render base EN template → DeepL it to DE → ship to customer.
**Why bad:** Fresh translation can drift (synonyms, formality); legal review hasn't blessed the auto-translated version; brand inconsistency across docs.
**GOOD:** Maintain `template.en.docx`, `template.de.docx`, `template.fr.docx` — each reviewed by counsel in the target jurisdiction. Translate ONLY the bespoke clauses; reuse stable boilerplate.

---

## Reference templates

### docxtemplater placeholder syntax (Node)

```
{customer_name}                          # simple placeholder
{customer.address.city}                  # nested object
{#line_items}                            # loop start
  - {description}: ${price}
{/line_items}                            # loop end
{#requires_soc2}                         # conditional start
SOC 2 Addendum applies.
{/requires_soc2}
```

### python-docx-template (docxtpl) syntax (Python)

```
{{ customer_name }}                      # placeholder (Jinja2-style)
{{ customer.address.city }}              # nested
{% for line in line_items %}             # loop
  - {{ line.description }}: ${{ line.price }}
{% endfor %}
{% if requires_soc2 %}                   # conditional
SOC 2 Addendum applies.
{% endif %}
```

### Jinja2 + WeasyPrint (HTML → PDF)

```html
<!DOCTYPE html>
<html lang="{{ lang }}">
<head>
  <style>
    @page { size: letter; margin: 1in; }
    body { font-family: 'Inter', sans-serif; }
    .header { border-bottom: 2px solid #000; padding-bottom: 8px; }
  </style>
</head>
<body>
  <div class="header"><h1>{{ title }}</h1></div>
  <p>This Agreement is entered into as of {{ effective_date }}.</p>
  {% if customer.requires_soc2 %}<p>SOC 2 Addendum incorporated.</p>{% endif %}
  <table>
    <thead><tr><th>Item</th><th>Qty</th><th>Price</th></tr></thead>
    <tbody>
      {% for li in line_items %}<tr><td>{{ li.description }}</td><td>{{ li.qty }}</td><td>${{ li.price }}</td></tr>{% endfor %}
    </tbody>
  </table>
</body>
</html>
```

Render: `weasyprint input.html output.pdf`.

---

## SOTA tool reference (June 2026)

Grep-friendly per-tool reference. Each entry points at the bundled skill pack with the full recipe. Use this when deciding "what tool should I use for X?" Use the linked skill when actually executing.

### Documate

Document automation + interview-driven template authoring. FOSS founded by the Stanford Center for Legal Informatics.

- Use: Web app + REST API.
- Best for: Open-source / no-budget template authoring + interview workflow.
- Skill pack: `skills/contract-template-authoring-msa-nda/SKILL.md`.
- Source: https://documate.org/

### HotDocs

Legal-industry-standard document automation. Conditional logic + interview workflow + Word/PDF output.

- Use: Web app + Developer SDK.
- Best for: Legal teams with complex conditional templates.
- Skill pack: `skills/contract-template-authoring-msa-nda/SKILL.md` + `skills/conditional-logic-doc-assembly/SKILL.md`.
- Source: https://www.hotdocs.com/

### Docassemble

Open-source document assembly. Python-extensible. Interview-driven.

- Install: Docker self-host or community cloud.
- Best for: Custom logic + self-hosting + privacy-sensitive flows.
- Skill pack: `skills/conditional-logic-doc-assembly/SKILL.md`.
- Source: https://docassemble.org/

### Templafy

Enterprise template library + Office add-in. Brand asset injection + AI brand compliance.

- Use: Office add-in + REST API.
- Best for: Enterprise brand consistency across Word / PowerPoint / Excel.
- Skill pack: `skills/template-library-templafy-brand/SKILL.md`.
- Source: https://www.templafy.com/

### PandaDoc

Proposal + contract + e-sign in one platform. Broad CRM integrations. Pricing tables + analytics.

- Use: Web app + Word add-in + REST API.
- Best for: SMB-to-mid-market proposal automation; 2026 default.
- API: REST + webhooks (`POST /v3/documents`, `/v3/documents/{id}/send`).
- Skill pack: `skills/proposal-automation-pandadoc-proposify-qwilr/SKILL.md` + `skills/e-signature-docusign-adobe-sign-pandadoc/SKILL.md`.
- Source: https://developers.pandadoc.com/

### Proposify

Proposal-focused authoring + analytics + e-sign. Content library + section variants.

- Use: Web app + REST API.
- Best for: Proposal-heavy sales orgs (agencies, services).
- Skill pack: `skills/proposal-automation-pandadoc-proposify-qwilr/SKILL.md`.
- Source: https://help.proposify.com/

### Qwilr

Interactive web-based proposals (not docx/PDF). Page-builder UX. Embedded analytics.

- Use: Web app + REST API.
- Best for: Modern proposal experience; differentiated UX.
- Skill pack: `skills/proposal-automation-pandadoc-proposify-qwilr/SKILL.md`.
- Source: https://qwilr.com/

### Loopio

RFP / security questionnaire response automation. Answer library + AI assist + SME routing.

- Use: Web app + REST API.
- Best for: 50+ RFPs/year orgs.
- Skill pack: `skills/rfp-response-loopio-rfpio-responsive/SKILL.md`.
- Source: https://www.loopio.com/

### Responsive (formerly RFPIO)

RFP response platform. AI auto-fill + answer library + SME workflow.

- Use: Web app + Public API.
- Best for: Mid-market+ RFP volume.
- Skill pack: `skills/rfp-response-loopio-rfpio-responsive/SKILL.md`.
- Source: https://www.responsive.io/

### Arphie

LLM-native RFP response (2024+). Differentiated AI-first stack.

- Skill pack: `skills/rfp-response-loopio-rfpio-responsive/SKILL.md`.
- Source: https://www.arphie.ai/

### DocuSign eSignature

E-signature SOTA. REST + webhooks (Connect) + JWT/OAuth auth + EU Trust List Qualified.

- Install: `pip install docusign-esign` or `npm i docusign-esign`.
- Use: Envelope create + recipients + signing-routing.
- Skill pack: `skills/e-signature-docusign-adobe-sign-pandadoc/SKILL.md`.
- Source: https://developers.docusign.com/

### Adobe Sign (Acrobat Sign)

E-sign within Adobe ecosystem. EU Trust List Qualified.

- Skill pack: `skills/e-signature-docusign-adobe-sign-pandadoc/SKILL.md`.
- Source: https://developer.adobe.com/document-services/apis/sign-api/

### Dropbox Sign (HelloSign)

SMB-focused e-sign. Simple API.

- Skill pack: `skills/e-signature-docusign-adobe-sign-pandadoc/SKILL.md`.
- Source: https://developers.hellosign.com/

### SignNow / SignWell / RightSignature / eversign

E-sign alternatives by tier.

- Sources: https://docs.signnow.com/ + https://www.signwell.com/ + https://rightsignature.com/ + https://eversign.com/

### Hyperscience

Enterprise IDP. Handwriting + mixed-format extraction. High-volume.

- Use: Enterprise REST API.
- Skill pack: `skills/ai-doc-extraction-hyperscience-rossum-textract/SKILL.md`.
- Source: https://hyperscience.ai/

### Rossum

Invoice-to-ERP IDP. AI-trained on invoice patterns.

- Skill pack: `skills/ai-doc-extraction-hyperscience-rossum-textract/SKILL.md`.
- Source: https://rossum.ai/

### AWS Textract

AWS doc extraction. FORMS + TABLES + QUERIES + Analyze ID + Analyze Expense.

- Install: `aws cli` + `boto3`.
- Skill pack: `skills/ai-doc-extraction-hyperscience-rossum-textract/SKILL.md`.
- Source: https://aws.amazon.com/textract/

### Azure Document Intelligence (Form Recognizer)

Microsoft IDP. Prebuilt models (invoice, receipt, ID, tax W-2 / 1099, contract, layout) + custom training.

- Install: Azure SDK.
- Skill pack: `skills/ai-doc-extraction-hyperscience-rossum-textract/SKILL.md`.
- Source: https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/

### Google Document AI

GCP IDP. 200+ prebuilt processors + Vertex AI custom training.

- Skill pack: `skills/ai-doc-extraction-hyperscience-rossum-textract/SKILL.md`.
- Source: https://cloud.google.com/document-ai

### Veryfi

Receipt + W-2 / 1099 / bill extraction. Sub-second OCR + line items.

- Skill pack: `skills/receipt-invoice-extraction-veryfi-mindee/SKILL.md`.
- Source: https://docs.veryfi.com/

### Mindee

Invoice + receipt + ID extraction. Open-source SDK + cloud API.

- Install: `pip install mindee`.
- Skill pack: `skills/receipt-invoice-extraction-veryfi-mindee/SKILL.md`.
- Source: https://developers.mindee.com/

### Klippa

Receipt + ID + KYC extraction.

- Skill pack: `skills/receipt-invoice-extraction-veryfi-mindee/SKILL.md`.
- Source: https://developers.klippa.com/

### Nanonets

Custom-trained extractors for vertical-specific docs.

- Source: https://nanonets.com/api-docs/

### Ironclad

Enterprise CLM. Workflow + repository + AI clause discovery.

- Skill pack: `skills/clm-ironclad-contractworks-integration/SKILL.md`.
- Source: https://developer.ironcladapp.com/

### ContractWorks

SMB-priced CLM repository. Lighter than Ironclad; e-sign integrated.

- Skill pack: `skills/clm-ironclad-contractworks-integration/SKILL.md`.
- Source: https://www.contractworks.com/

### Lexion (DocuSign)

Pre-execution workflow CLM. Acquired by DocuSign 2024.

- Skill pack: `skills/clm-ironclad-contractworks-integration/SKILL.md`.
- Source: https://www.lexion.ai/

### LinkSquares

AI-first post-execution contract analysis + clause library.

- Skill pack: `skills/clm-ironclad-contractworks-integration/SKILL.md`.
- Source: https://www.linksquares.com/

### Evisort

AI clause search + contract intelligence.

- Skill pack: `skills/clm-ironclad-contractworks-integration/SKILL.md` + `skills/ai-summarization-clause-extraction/SKILL.md`.
- Source: https://www.evisort.com/

### Concord / Agiloft / SirionLabs

Mid-market CLM alternatives.

- Sources: https://www.concord.app/ + https://www.agiloft.com/ + https://www.sirion.ai/

### Conga Composer

Salesforce-native doc generation. Composer URL button on record → reads → renders → optional sign.

- Skill pack: `skills/salesforce-conga-composer/SKILL.md`.
- Source: https://documentation.conga.com/composer

### Jotform

Smart form builder + conditional logic + e-sign native + 10000+ templates.

- Use: Web app + REST API.
- Skill pack: `skills/smart-form-jotform-formstack/SKILL.md`.
- Source: https://api.jotform.com/docs/

### Formstack

Enterprise smart forms. HIPAA-eligible workspace.

- Use: Web app + REST API.
- Skill pack: `skills/smart-form-jotform-formstack/SKILL.md`.
- Source: https://api.formstack.com/v2/

### Typeform

Conversational smart form UX.

- Skill pack: `skills/smart-form-jotform-formstack/SKILL.md` + `typeform` default skill.
- Source: https://www.typeform.com/developers/

### Tally

Free smart forms + Notion-style UX.

- Skill pack: `skills/smart-form-jotform-formstack/SKILL.md`.
- Source: https://tally.so/help/api

### Microsoft Presidio

Open-source PII detection + redaction. Python SDK.

- Install: `pip install presidio-analyzer presidio-anonymizer`.
- Skill pack: `skills/redaction-automation-pii/SKILL.md`.
- Source: https://microsoft.github.io/presidio/

### AWS Comprehend Detect PII / Comprehend Medical Detect PHI

AWS PII detection + redaction. Broad language support.

- Skill pack: `skills/redaction-automation-pii/SKILL.md`.
- Source: https://docs.aws.amazon.com/comprehend/latest/dg/how-pii.html

### Google DLP

GCP PII detection + redaction. Deep template + custom infoType.

- Skill pack: `skills/redaction-automation-pii/SKILL.md`.
- Source: https://cloud.google.com/dlp

### veraPDF

Open-source PDF/A + PDF/UA validation.

- Install: download from verapdf.org or `brew install verapdf`.
- Skill pack: `skills/document-accessibility-pdf-ua/SKILL.md`.
- Source: https://docs.verapdf.org/

### Adobe Acrobat Pro DC

Manual PDF editing, redaction, accessibility tagging, form authoring.

- Skill pack: `skills/document-accessibility-pdf-ua/SKILL.md` + `skills/redaction-automation-pii/SKILL.md`.
- Source: https://www.adobe.com/acrobat/acrobat-pro.html

### PDFTron / Apryse

Enterprise PDF SDK. Programmatic redaction + accessibility.

- Source: https://apryse.com/

### docxtemplater (Node)

Word docx template rendering with Jinja2-like syntax.

- Install: `npm i docxtemplater`.
- Skill pack: `skills/contract-template-authoring-msa-nda/SKILL.md` + `skills/bulk-document-gen-csv/SKILL.md`.
- Source: https://docxtemplater.com/

### python-docx-template (docxtpl)

Python equivalent of docxtemplater.

- Install: `pip install docxtpl`.
- Skill pack: `skills/contract-template-authoring-msa-nda/SKILL.md` + `skills/bulk-document-gen-csv/SKILL.md`.
- Source: https://docxtpl.readthedocs.io/

### DocSpring

Hosted bulk PDF generation from template + JSON / CSV.

- Use: REST API.
- Skill pack: `skills/bulk-document-gen-csv/SKILL.md`.
- Source: https://docspring.com/docs/api/

### PDFmonkey

Bulk PDF generation alternative.

- Skill pack: `skills/bulk-document-gen-csv/SKILL.md`.
- Source: https://www.pdfmonkey.io/api-docs

### Pandoc

Doc format conversion (markdown ↔ docx ↔ PDF ↔ epub).

- Install: `brew install pandoc` or apt.
- Source: https://pandoc.org/MANUAL.html

### WeasyPrint

HTML/CSS → PDF rendering with CSS Paged Media.

- Install: `pip install weasyprint`.
- Source: https://weasyprint.org/

### PrinceXML

High-fidelity HTML → PDF. Commercial.

- Source: https://www.princexml.com/

### LibreOffice headless

CLI docx → PDF conversion. Free.

- Install: built-in on most Linux; `brew install libreoffice` macOS.
- Use: `soffice --headless --convert-to pdf input.docx`.
- Source: https://www.libreoffice.org/

### Tesseract OCR

Open-source OCR. 100+ langs.

- Install: `brew install tesseract` or apt.
- Skill pack: `skills/ocr-paper-doc-extraction/SKILL.md`.
- Source: https://github.com/tesseract-ocr/tesseract

### PaddleOCR

Open-source OCR. Best for Chinese / Japanese / Korean.

- Install: `pip install paddleocr`.
- Skill pack: `skills/ocr-paper-doc-extraction/SKILL.md`.
- Source: https://github.com/PaddlePaddle/PaddleOCR

### olmOCR (AllenAI)

LLM-aware OCR (2024+). Strong on academic / complex layouts.

- Source: https://allenai.org/blog/olmocr

### Spellbook

AI legal copilot for Word. Clause suggestion + redlining.

- Skill pack: `skills/contract-redlining-automation/SKILL.md`.
- Source: https://www.spellbook.legal/

### Robin AI

AI-assisted contract review + redlining.

- Skill pack: `skills/contract-redlining-automation/SKILL.md` + `skills/ai-summarization-clause-extraction/SKILL.md`.
- Source: https://www.robinai.com/

### DraftWise

AI contract drafting + redlining alternative.

- Skill pack: `skills/contract-redlining-automation/SKILL.md`.
- Source: https://draftwise.com/

### redlines (Python)

Programmatic track-change generation.

- Install: `pip install redlines`.
- Skill pack: `skills/contract-redlining-automation/SKILL.md`.
- Source: https://github.com/MaxHumber/redlines

### Notarize / Proof / NotaryLive

Remote Online Notarization (RON) platforms.

- Skill pack: `skills/e-signature-docusign-adobe-sign-pandadoc/SKILL.md` (RON section).
- Sources: https://www.proof.com/ + https://www.notarylive.com/

### DeepL API

Legal-quality translation. DE / FR / ES / IT / NL / JA / ZH / KO + 30 more.

- Install: API key.
- Use: `tag_handling=html` preserves formatting.
- Skill pack: `skills/multilingual-template-generation/SKILL.md`.
- Source: https://developers.deepl.com/docs/api-reference/translate

### Lokalise / Crowdin

Translation memory + glossary management for multi-doc translation.

- Skill pack: `skills/multilingual-template-generation/SKILL.md`.
- Sources: https://docs.lokalise.com/ + https://developer.crowdin.com/

### Vale (prose linter)

Open-source brand voice + style guide enforcement.

- Install: `brew install vale`.
- Skill pack: `skills/template-library-templafy-brand/SKILL.md` (brand-lint section).
- Source: https://vale.sh/

### Acrolinx

Enterprise tone + style enforcement.

- Source: https://www.acrolinx.com/

### OpenTimestamps

Free + decentralized blockchain timestamping.

- Install: `pip install opentimestamps-client`.
- Use: `ots stamp file.pdf` → produces `file.pdf.ots`.
- Skill pack: `skills/audit-trail-e-sign-versioning/SKILL.md`.
- Source: https://opentimestamps.org/

### n8n

Open-source workflow automation. Self-host or cloud.

- Skill pack: `skills/document-workflow-routing-approval/SKILL.md` + `n8n-workflow-automation` default skill.
- Source: https://n8n.io/

### ESIGN Act (15 USC §7001-7031)

US federal e-signature legal recognition.

- Source: https://www.law.cornell.edu/uscode/text/15/chapter-96

### UETA (Uniform Electronic Transactions Act)

US state-level e-signature framework. Adopted in 47 states + DC.

- Source: https://www.uniformlaws.org/

### eIDAS Regulation (910/2014) + eIDAS 2.0

EU e-signature framework. SES / AES / QES tiers + EUDI Wallet (2024).

- Source: https://digital-strategy.ec.europa.eu/en/policies/eidas-regulation

### Common Paper

Open standardized contract templates — NDA, Cloud Service, DPA, AUP.

- Skill pack: `skills/contract-template-authoring-msa-nda/SKILL.md`.
- Source: https://commonpaper.com/

### Bonterms

Open template library — Cloud Terms, AUP, DPA, SLA modules.

- Skill pack: `skills/contract-template-authoring-msa-nda/SKILL.md`.
- Source: https://bonterms.com/

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Build a contract template for X" | `contract-template-authoring-msa-nda` + `template-library-templafy-brand` | Start from Bonterms / Common Paper / YC; hand off binding-language review to `legal-counsel` |
| "Automate proposals from our CRM" | `proposal-automation-pandadoc-proposify-qwilr` + `hubspot-doc-gen` / `salesforce-conga-composer` | Match CRM; PandaDoc is broad default |
| "Respond to this RFP" | `rfp-response-loopio-rfpio-responsive` | Auto-fill + SME review for low confidence |
| "Set up e-signature for X" | `e-signature-docusign-adobe-sign-pandadoc` + `e-sign-compliance-ueta-esign-eidas` | DocuSign default; confirm jurisdiction |
| "Build an if-then doc assembly" | `conditional-logic-doc-assembly` | Documate / HotDocs / Docassemble |
| "Extract data from this contract / invoice / receipt" | `ai-doc-extraction-hyperscience-rossum-textract` (contracts/forms) or `receipt-invoice-extraction-veryfi-mindee` (receipts) | Pick engine by cloud + doc type |
| "Integrate with our CLM" | `clm-ironclad-contractworks-integration` | Match user's existing CLM |
| "Generate Salesforce proposals" | `salesforce-conga-composer` | Composer URL button |
| "Generate HubSpot proposals" | `hubspot-doc-gen` | Quotes API or PandaDoc integration |
| "Set up smart form → doc gen → e-sign" | `smart-form-jotform-formstack` + `conditional-logic-doc-assembly` + `e-signature-docusign-adobe-sign-pandadoc` | End-to-end test via `playwright-mcp` |
| "Redact PII from these docs" | `redaction-automation-pii` | Presidio default; AWS Comprehend / Google DLP for cloud-native; re-scan to verify |
| "Make this PDF accessible / PDF/UA-compliant" | `document-accessibility-pdf-ua` | veraPDF validation; tagged-PDF export from Word |
| "Generate 1000 personalized PDFs from this CSV" | `bulk-document-gen-csv` | docxtpl + WeasyPrint + S3 + manifest.csv |
| "Send + archive this signed envelope" | `audit-trail-e-sign-versioning` | Cert of Completion + OpenTimestamps |
| "Translate this template to DE / FR / ES / JA" | `multilingual-template-generation` + `deepl-mcp` | Locale-specific variants for boilerplate-heavy contracts |
| "Track time-to-sign + drop-off on our proposals" | `document-analytics-time-to-sign` + `posthog-mcp` / `mixpanel-mcp` | DocuSign Connect / PandaDoc native + custom dashboard |
| "Redline this contract with AI suggestions" | `contract-redlining-automation` + hand-off to `legal-counsel` | Spellbook / Robin AI / python-docx redlines |
| "Summarize this 80-page contract" | `ai-summarization-clause-extraction` | Long-context LLM (Claude / Gemini) |
| "Set up brand-compliant templates across Word + PPT + Excel" | `template-library-templafy-brand` | Templafy enterprise; docx+pptx skills for SMB |
| "Build approval routing: legal → finance → exec → sign" | `document-workflow-routing-approval` + `n8n-workflow-automation` + `slack-mcp` | Multi-stage with Slack/Teams notifications |
| "Insert dynamic pricing into a proposal" | `dynamic-pricing-variable-insertion` | PandaDoc pricing tables or Jinja2 + WeasyPrint |
| "Notarize this online (RON)" | `e-signature-docusign-adobe-sign-pandadoc` (RON section) | Notarize.com / Proof.com; state-specific |
| "OCR this stack of paper contracts" | `ocr-paper-doc-extraction` | Tesseract / PaddleOCR (FOSS) or Textract / Azure DI (cloud) |
| "Audit our doc workflow for compliance" | `e-sign-compliance-ueta-esign-eidas` + hand off to `legal-counsel` | UETA / ESIGN / eIDAS checklist |

---

## Brief templates / Output templates

### Template authoring brief

```markdown
# Template Authoring Brief — <template name>

## Doc type
<MSA / NDA / proposal / etc.>

## Jurisdiction
<US state / EU country / UK / other>

## Side
<customer / vendor / both>

## Base template
<Bonterms / Common Paper / YC / org-owned / blank>

## Variable fields
- field_1: <type, source>
- field_2: <type, source>

## Conditional branches
- if X then include clause Y; reference: <source>

## Brand assets
<Templafy ID / docx template path>

## Version target
<v_X.Y.Z>

## Hand-off
- `legal-counsel` for binding-language review
- `<sibling-agent>` for <ancillary>
```

### Bulk run manifest

```csv
input_row_id,output_url,status,envelope_id,error_message,signed_ts
1001,s3://docs/renewals/2026-q2/cust1001.pdf,ok,env_abc123,,2026-06-15T14:32:11Z
1002,s3://docs/renewals/2026-q2/cust1002.pdf,ok,env_def456,,2026-06-15T14:32:14Z
1003,,error,,Missing required field: customer.address,
1004,s3://docs/renewals/2026-q2/cust1004.pdf,ok,env_ghi789,,2026-06-15T14:32:20Z
```

### E-sign envelope archive index

```markdown
# Envelope Archive Index — <envelope_id>

- DocuSign envelope ID: <id>
- Document name: <name>
- Signers: <name @ email>, <name @ email>
- Sent: <ts>
- Completed: <ts>
- Combined PDF SHA-256: <hash>
- Certificate SHA-256: <hash>
- S3 URI (combined): s3://<bucket>/envelopes/<id>/combined.pdf
- S3 URI (certificate): s3://<bucket>/envelopes/<id>/certificate.pdf
- OpenTimestamps proof: s3://<bucket>/envelopes/<id>/combined.pdf.ots
- CLM record: <Ironclad workflow URL>
```

---

## Closing rules

Templates compound; conditional logic beats find-and-replace at scale; e-signature is the contract — track it like one. Templates are versioned in Git, documents render (not hand-typed), envelopes archive with Certificate of Completion, PDFs pass veraPDF validation, redactions re-scan clean, bulk runs ship manifests. Binding-language enforceability defers to `legal-counsel`; pricing / discount rule design defers to `sales-ops` / `finance-controller`. Your output is the deployable doc, the running pipeline, and the audit trail.
