---
name: ai-doc-extraction-hyperscience-rossum-textract
description: Intelligent Document Processing (IDP) for high-volume mixed-format docs — Hyperscience (enterprise + handwriting), Rossum (invoice-to-ERP), AWS Textract (FORMS + TABLES + QUERIES), Azure Document Intelligence (prebuilt invoice / receipt / ID / tax / contract models), Google Document AI (200+ processors). Extract structured fields + tables + queries with confidence scores; route low-confidence for review. Use when the user says "extract fields from invoices", "parse contracts at scale", "Textract / Azure DI / Document AI", "IDP platform", "AI document extraction", "doc understanding".
---

# AI doc extraction (IDP) — Hyperscience / Rossum / Textract / Azure DI / Document AI

This skill handles high-volume structured + semi-structured extraction. For receipts/invoices specifically, see `receipt-invoice-extraction-veryfi-mindee`. For paper-OCR, see `ocr-paper-doc-extraction`.

## When to use

User says:

- "Extract fields from this batch of invoices / contracts / forms"
- "AWS Textract / Azure Document Intelligence / Google Document AI"
- "Hyperscience / Rossum / Klippa / Nanonets"
- "Parse this PDF into JSON"
- "Doc understanding / IDP"
- "Question-answer extraction from doc"
- "Form fields + tables + queries"
- "Custom-trained extractor"

Companion skills:
- `receipt-invoice-extraction-veryfi-mindee` — receipt-specialized engines.
- `ocr-paper-doc-extraction` — pure OCR (no structured extraction).
- `ai-summarization-clause-extraction` — long-form contract clause extraction.

## Setup

```bash
# AWS Textract — AWS shops
aws configure                   # provide creds
# IAM permissions: textract:AnalyzeDocument, textract:StartDocumentAnalysis, s3:GetObject

# Azure Document Intelligence (formerly Form Recognizer)
# https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/
export AZURE_DI_ENDPOINT="https://<resource>.cognitiveservices.azure.com"
export AZURE_DI_KEY="..."
pip install azure-ai-documentintelligence

# Google Document AI
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/sa.json"
pip install google-cloud-documentai
# Enable Document AI API in GCP project

# Hyperscience — enterprise quote-based
# https://hyperscience.ai/
export HYPERSCIENCE_API_TOKEN="..."

# Rossum — invoice-specialized
# https://rossum.ai/  (REST + webhooks)
export ROSSUM_TOKEN="..."
```

Auth / API keys:
- AWS: standard AWS creds (env / config / role).
- Azure DI: `Ocp-Apim-Subscription-Key` header.
- Google: GOOGLE_APPLICATION_CREDENTIALS env → service account.
- Hyperscience: bearer token.
- Rossum: token via `/auth/login` (username + password).

## Common recipes

### Recipe 1: Pick the engine

| Engine | Best for | Pricing model | Custom training |
|---|---|---|---|
| AWS Textract | AWS shops; mixed forms + tables + queries | Per-page | Limited (Adapter for QUERIES) |
| Azure Document Intelligence | Microsoft shops; broad prebuilt models | Per-page | Custom Neural / Composed |
| Google Document AI | GCP shops; 200+ prebuilt processors; custom via Vertex AI | Per-page | Yes, via Workbench |
| Hyperscience | Enterprise high-volume + handwriting + mixed | Quote-based | Strong custom + active learning |
| Rossum | Invoice-to-ERP specialized | Per-document | Strong on invoices |
| Klippa | Receipts + ID + KYC | Per-document | Yes |
| Mindee | Invoices + receipts + IDs, fast dev | Per-call | Custom API |
| Nanonets | Vertical-specific custom extractors | Per-page + training | Strong custom |

### Recipe 2: AWS Textract — FORMS + TABLES + QUERIES

```bash
# QUERIES feature lets you ask specific Qs of the doc — no custom training needed
aws textract analyze-document \
  --document '{"S3Object":{"Bucket":"contracts","Name":"msa-acme.pdf"}}' \
  --feature-types '["FORMS", "TABLES", "QUERIES"]' \
  --queries-config '{
    "Queries":[
      {"Text":"What is the effective date?","Alias":"effective_date"},
      {"Text":"What is the term length in months?","Alias":"term_months"},
      {"Text":"What is the governing law jurisdiction?","Alias":"governing_law"},
      {"Text":"What is the limitation of liability cap?","Alias":"liability_cap"},
      {"Text":"Who are the parties to this agreement?","Alias":"parties"},
      {"Text":"What is the annual fee?","Alias":"annual_fee"}
    ]
  }' > extracted.json
```

Parse:
```python
import json
data = json.load(open("extracted.json"))
queries = {}
query_id_to_alias = {}
for b in data["Blocks"]:
    if b["BlockType"] == "QUERY":
        query_id_to_alias[b["Id"]] = b["Query"]["Alias"]
    if b["BlockType"] == "QUERY_RESULT":
        # Find parent QUERY via Relationships
        ...
```

### Recipe 3: AWS Textract — async for multi-page PDFs

```python
import boto3
client = boto3.client("textract")
start = client.start_document_analysis(
    DocumentLocation={"S3Object": {"Bucket": "contracts", "Name": "long-msa.pdf"}},
    FeatureTypes=["FORMS", "TABLES"],
    NotificationChannel={
        "SNSTopicArn": "arn:aws:sns:us-east-1:123:textract-completion",
        "RoleArn": "arn:aws:iam::123:role/TextractServiceRole"
    }
)
job_id = start["JobId"]
# SNS notifies when ready; poll meanwhile:
resp = client.get_document_analysis(JobId=job_id)
while resp["JobStatus"] == "IN_PROGRESS":
    time.sleep(5)
    resp = client.get_document_analysis(JobId=job_id)
```

### Recipe 4: Azure Document Intelligence — prebuilt invoice model

```bash
curl -X POST "${AZURE_DI_ENDPOINT}/documentintelligence/documentModels/prebuilt-invoice:analyze?api-version=2024-11-30" \
  -H "Ocp-Apim-Subscription-Key: ${AZURE_DI_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"urlSource":"https://example.com/invoice.pdf"}'
# Returns 202 + Operation-Location header

# Poll
curl "${AZURE_DI_ENDPOINT}/documentintelligence/documentModels/prebuilt-invoice/analyzeResults/${OP_ID}?api-version=2024-11-30" \
  -H "Ocp-Apim-Subscription-Key: ${AZURE_DI_KEY}"
```

### Recipe 5: Azure DI — available prebuilt models (2026)

```text
prebuilt-invoice           — invoices
prebuilt-receipt           — receipts
prebuilt-idDocument        — passports, driver's licenses, ID cards
prebuilt-tax.us.w2         — US W-2 forms
prebuilt-tax.us.1098       — US Form 1098 (mortgage interest)
prebuilt-tax.us.1099       — 1099-NEC, 1099-MISC, 1099-DIV
prebuilt-tax.us.1040       — Form 1040
prebuilt-contract          — contract layout extraction
prebuilt-businessCard      — business cards
prebuilt-healthInsuranceCard.us — US health insurance cards
prebuilt-marriageCertificate.us — US marriage certificates
prebuilt-mortgage.us.1003  — Uniform Residential Loan App
prebuilt-mortgage.us.1008  — Underwriting Transmittal Summary
prebuilt-mortgage.us.closingDisclosure — TILA-RESPA Closing Disclosure
prebuilt-bankStatement.us  — US bank statements
prebuilt-paystub.us        — US paystubs
prebuilt-creditCard        — credit card statements
prebuilt-layout            — general layout (text + tables + bounding)
prebuilt-read              — plain OCR
```

### Recipe 6: Azure DI — Python SDK

```python
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

client = DocumentIntelligenceClient(
    endpoint=os.environ["AZURE_DI_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_DI_KEY"])
)
with open("invoice.pdf", "rb") as f:
    poller = client.begin_analyze_document(
        "prebuilt-invoice",
        analyze_request=f,
        content_type="application/octet-stream"
    )
result = poller.result()
for doc in result.documents:
    fields = doc.fields
    print({
        "vendor": fields.get("VendorName").value_string if fields.get("VendorName") else None,
        "total": fields.get("InvoiceTotal").value_currency.amount if fields.get("InvoiceTotal") else None,
        "invoice_date": fields.get("InvoiceDate").value_date.isoformat() if fields.get("InvoiceDate") else None,
        "confidence": doc.confidence
    })
```

### Recipe 7: Google Document AI — invoke a processor

```python
from google.cloud import documentai_v1 as documentai

client = documentai.DocumentProcessorServiceClient()
name = f"projects/{PROJECT_ID}/locations/us/processors/{PROCESSOR_ID}"

with open("invoice.pdf", "rb") as f:
    raw_document = documentai.RawDocument(content=f.read(), mime_type="application/pdf")
request = documentai.ProcessRequest(name=name, raw_document=raw_document)
result = client.process_document(request=request)
doc = result.document

# Entities
for ent in doc.entities:
    print(ent.type_, ent.mention_text, ent.confidence)
```

### Recipe 8: Google Document AI — popular prebuilt processors

```text
INVOICE_PROCESSOR             — invoices
EXPENSE_PROCESSOR             — expense receipts
US_DRIVER_LICENSE_PROCESSOR
US_PASSPORT_PROCESSOR
US_W2_PROCESSOR
US_W9_PROCESSOR
US_1040_PROCESSOR
CONTRACT_PROCESSOR            — contracts
FORM_PARSER_PROCESSOR         — general forms
OCR_PROCESSOR                 — plain OCR
LAYOUT_PARSER                 — general layout
US_BANK_STATEMENT_PROCESSOR
US_PAYSTUB_PROCESSOR
US_UTILITY_BILL_PROCESSOR
US_MORTGAGE_DOCUMENTS_PARSER
```

### Recipe 9: Hyperscience — submit + retrieve

```bash
# Hyperscience expects a multipart upload to a configured Flow
curl -X POST "https://${HYPERSCIENCE_HOST}/api/v5/submissions" \
  -H "Authorization: Token $HYPERSCIENCE_API_TOKEN" \
  -F "files[]=@input.pdf" \
  -F "external_id=acme-2026-q2-batch-001"

# Returns submission_id; poll for state=complete
curl "https://${HYPERSCIENCE_HOST}/api/v5/submissions/${SUB_ID}" \
  -H "Authorization: Token $HYPERSCIENCE_API_TOKEN"

# Get extracted data
curl "https://${HYPERSCIENCE_HOST}/api/v5/submissions/${SUB_ID}/transcription/json" \
  -H "Authorization: Token $HYPERSCIENCE_API_TOKEN"
```

### Recipe 10: Rossum — submit invoice + fetch

```bash
# Auth
curl -X POST https://api.elis.rossum.ai/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"...","password":"..."}'
# Returns { "key": "..." }

# Upload to a queue
curl -X POST "https://api.elis.rossum.ai/v1/queues/${QUEUE_ID}/upload" \
  -H "Authorization: token $ROSSUM_TOKEN" \
  -F content=@invoice.pdf

# Poll annotations for the queue
curl "https://api.elis.rossum.ai/v1/annotations?queue=${QUEUE_ID}&status=to_review" \
  -H "Authorization: token $ROSSUM_TOKEN"
```

### Recipe 11: Confidence-driven review routing

```python
import json
results = json.load(open("extracted.json"))
to_review = []
for field in results["fields"]:
    if field["confidence"] < 0.85:
        to_review.append(field)

# Send to Slack for SME review
if to_review:
    post_slack(f"{len(to_review)} fields need review", to_review)
```

### Recipe 12: Custom training (Azure DI Custom Neural)

```bash
# 1) Upload training docs + labels to Blob Storage
az storage blob upload-batch -d training-data -s ./labeled-docs/

# 2) Train a custom model
curl -X POST "${AZURE_DI_ENDPOINT}/documentintelligence/documentModels:build?api-version=2024-11-30" \
  -H "Ocp-Apim-Subscription-Key: ${AZURE_DI_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "modelId": "custom-vendor-form-v1",
    "buildMode": "neural",
    "azureBlobSource": {
      "containerUrl": "https://<account>.blob.core.windows.net/training-data?<SAS>"
    }
  }'

# 3) Use custom model
curl -X POST "${AZURE_DI_ENDPOINT}/documentintelligence/documentModels/custom-vendor-form-v1:analyze?api-version=2024-11-30" \
  -H "Ocp-Apim-Subscription-Key: ${AZURE_DI_KEY}" \
  -d '{"urlSource":"https://example.com/vendor-form.pdf"}'
```

### Recipe 13: Validate output schema

```python
import jsonschema
schema = {
    "type": "object",
    "required": ["vendor", "total", "invoice_date"],
    "properties": {
        "vendor": {"type": "string", "minLength": 1},
        "total": {"type": "number", "minimum": 0},
        "invoice_date": {"type": "string", "format": "date"}
    }
}
jsonschema.validate(extracted, schema)
```

## Examples

### Example 1: Batch contract extraction with AWS Textract QUERIES

**Goal:** Extract effective date, term, governing law, LoL from 1000 contracts in S3.
**Steps:**
1. List PDFs in `s3://contracts/incoming/`.
2. Recipe 3 — `start_document_analysis` per file.
3. Use Textract QUERIES (Recipe 2) for the 6 target fields.
4. Recipe 11 — low-confidence routing to Slack.
5. Store results in DynamoDB / Postgres + push to CLM via `clm-ironclad-contractworks-integration`.

**Result:** Structured contract metadata at scale.

### Example 2: Azure DI invoice → ERP integration

**Goal:** Vendor sends 100 invoices/day; auto-extract + post to NetSuite.
**Steps:**
1. SFTP / S3 ingest.
2. Recipe 6 — Azure DI `prebuilt-invoice` model.
3. Validate via Recipe 13.
4. Map to NetSuite Vendor Bill format.
5. Recipe 11 — low-conf (<0.85) → AP team Slack queue.
6. Post via NetSuite REST API on approval.

**Result:** 80%+ touchless invoice processing.

### Example 3: Hyperscience handwritten form digitization

**Goal:** 10k handwritten medical intake forms → structured patient records.
**Steps:**
1. Recipe 9 — Hyperscience flow configured for handwriting.
2. Active learning — flagged docs go to keyer; model retrains weekly.
3. Output to HL7 FHIR (Patient resource).
4. HIPAA-eligible storage in S3 with envelope encryption.

**Result:** Handwriting → structured at production scale.

## Edge cases / gotchas

- **Textract async vs sync.** Sync (`analyze_document`) for single-page PDFs ≤ 10 MB; async (`start_document_analysis`) for multi-page or larger. Hitting sync with multi-page → silent first-page-only result.
- **Textract QUERIES limit.** Up to 15 queries per call. Hit the limit → multiple calls + reconcile.
- **Azure DI page count limits.** Free tier 2-page max; standard 2000 pages per model call. Split larger PDFs.
- **Azure DI prebuilt invoice locale.** Some fields (US-specific) on `prebuilt-invoice` may miss non-US invoices; use `prebuilt-invoice` with `locale=en-GB` etc.
- **Google Document AI quotas.** Default 600 requests/minute; can raise.
- **Service-account permissions.** Google needs `documentai.processors.processDocument` + `storage.objects.get`.
- **Hyperscience handwriting accuracy varies.** Train on representative samples; bad samples → poor active learning.
- **Rossum is invoice-centric.** Don't try to extract contract clauses with Rossum.
- **Confidence scores aren't probabilities.** They're heuristic; calibrate threshold per engine + doc type.
- **PII in extraction.** Logs may contain extracted PII; configure retention; comply with HIPAA / GDPR.
- **Custom training data requires labels.** 50-200 labeled docs minimum for Azure Custom Neural; 5-10 per field for Document AI custom.
- **OCR quality affects extraction.** Bad scans → bad extraction. Preprocess (deskew, denoise) before submit.
- **Engines drift.** Test fixtures periodically; engines retrain + accuracy can shift.
- **Cost surprise.** Per-page pricing on AWS ($1.50 / 1k pages for FORMS); 1 contract = 10 pages = $0.015; 1M docs = $15k.
- **Cross-region data residency.** GDPR — use EU-region endpoints; pin region in client.
- **Multi-language.** Most engines support 70+ langs but accuracy varies; Hyperscience strongest on multi-script.
- **Tables vs forms vs queries.** Cross-cutting — invoice line items often missed by FORMS feature but captured by TABLES.

## Sources

- [AWS Textract](https://aws.amazon.com/textract/) — overview.
- [AWS Textract Docs](https://docs.aws.amazon.com/textract/latest/dg/) — full reference.
- [Azure Document Intelligence](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/) — formerly Form Recognizer.
- [Azure DI Prebuilt models](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/overview) — list.
- [Google Document AI](https://cloud.google.com/document-ai) — overview.
- [Google Document AI Processors](https://cloud.google.com/document-ai/docs/processors-list) — full list.
- [Hyperscience](https://hyperscience.ai/) — IDP.
- [Rossum](https://rossum.ai/) — invoice-to-ERP.
- [Klippa](https://www.klippa.com/) — receipts + ID + KYC.
- [Nanonets](https://nanonets.com/) — custom-trained extractors.
- Sister skills: `receipt-invoice-extraction-veryfi-mindee`, `ocr-paper-doc-extraction`, `ai-summarization-clause-extraction`.
