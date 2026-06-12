---
name: receipt-invoice-extraction-veryfi-mindee
description: Extract structured data from receipts, invoices, bills, W-2 / 1099, and KYC IDs using specialized OCR providers — Veryfi (sub-second receipts + tax forms), Mindee (open-source SDK + cloud invoices/receipts/IDs), Klippa (receipt + ID + KYC), Nanonets (custom-trained). Use when the user says "extract receipt data", "parse invoice", "OCR a bill", "Veryfi", "Mindee", "Klippa", "Nanonets", "line-item extraction", "vendor + total + tax + line items".
---

# Receipt / invoice / bill extraction — Veryfi, Mindee, Klippa, Nanonets

This skill ships the specialized receipt/invoice extraction stack. For mixed-format enterprise IDP (handwriting, contracts, structured forms at scale), use `ai-doc-extraction-hyperscience-rossum-textract`. For paper-only OCR with no structure, use `ocr-paper-doc-extraction`.

## When to use

User says:

- "Extract data from this receipt / invoice / bill"
- "Veryfi / Mindee / Klippa / Nanonets API"
- "Parse a W-2 / 1099 / paystub"
- "Pull vendor + total + tax + date + line items into JSON"
- "Push invoices into QuickBooks / Xero / NetSuite / SAP"
- "KYC ID extraction" (passport / driver's license / national ID)
- "Reimbursement scan-and-submit"

Companion skills:
- `ai-doc-extraction-hyperscience-rossum-textract` — for non-receipt structured docs (contracts, claims, statements) and very high volume.
- `ocr-paper-doc-extraction` — fallback when no specialized model exists.
- `bulk-document-gen-csv` — output side for batch extracted-then-rendered flows.

## Setup

```bash
# Veryfi (best for receipts + W-2 / 1099 / bills; US-centric)
pip install veryfi
# Required env: VERYFI_CLIENT_ID, VERYFI_CLIENT_SECRET, VERYFI_USERNAME, VERYFI_API_KEY

# Mindee (broad invoice/receipt/ID; EU + US; open-source SDK)
pip install mindee
# Required env: MINDEE_API_KEY

# Klippa (receipts + IDs + KYC; EU-heavy)
# REST API — no official Python SDK
# Required env: KLIPPA_API_KEY

# Nanonets (custom-trained extractors per workflow)
pip install requests        # REST API
# Required env: NANONETS_API_KEY + a trained MODEL_ID
```

Sign-up URLs:
- Veryfi: https://app.veryfi.com/signup/api/
- Mindee: https://platform.mindee.com/signup
- Klippa: https://www.klippa.com/en/docguard/
- Nanonets: https://app.nanonets.com/

## Common recipes

### Recipe 1: Pick the provider

| Provider | Best for | Pricing (approx 2026) | Strengths | Watch out |
|---|---|---|---|---|
| Veryfi | US receipts + W-2 / 1099 / paystubs | $0.08-0.15 per doc | Sub-second; great on crumpled receipts | Less optimized for EU invoices |
| Mindee | International invoices + receipts + IDs | $0.10-0.20 per doc | Open-source SDK; broad doc catalog | Custom models extra |
| Klippa | EU receipts + KYC IDs | Quote-based | Strong on EU VAT structures + ID docs | Less US coverage |
| Nanonets | Anything custom-trained | $0.10-0.30 per doc | Train on your own templates in hours | Setup time for training |

Pick: receipts/US tax → Veryfi; broad invoice/ID → Mindee; EU VAT → Klippa; bespoke template → Nanonets.

### Recipe 2: Veryfi — process a receipt (Python SDK)

```python
from veryfi import Client

veryfi = Client(
    client_id=os.environ["VERYFI_CLIENT_ID"],
    client_secret=os.environ["VERYFI_CLIENT_SECRET"],
    username=os.environ["VERYFI_USERNAME"],
    api_key=os.environ["VERYFI_API_KEY"],
)

doc = veryfi.process_document("receipt.jpg")
print(doc["vendor"]["name"], doc["total"], doc["currency_code"])
for li in doc["line_items"]:
    print(li["description"], li["total"])
```

Veryfi returns: `vendor`, `total`, `subtotal`, `tax`, `tip`, `discount`, `currency_code`, `date`, `payment` (card brand + last 4), and a `line_items[]` array.

### Recipe 3: Veryfi — process a W-2 form

```python
doc = veryfi.process_w2_document("w2_2024.pdf")
print(doc["employer_ein"], doc["wages"], doc["federal_tax_withheld"])
```

W-2 endpoint returns boxes 1-20 plus state-section detail. Same shape on 1099-NEC and 1099-MISC.

### Recipe 4: Mindee — invoice OCR (Python SDK)

```python
from mindee import Client, product

mindee_client = Client(api_key=os.environ["MINDEE_API_KEY"])
input_doc = mindee_client.source_from_path("invoice.pdf")

result = mindee_client.parse(product.InvoiceV4, input_doc)
inv = result.document.inference.prediction

print("Supplier:", inv.supplier_name.value)
print("Total:", inv.total_amount.value, inv.locale.currency)
print("Date:", inv.date.value, "Due:", inv.due_date.value)
for li in inv.line_items:
    print(li.description, li.quantity, li.unit_price, li.total_amount)
```

Mindee product catalog: `InvoiceV4`, `ReceiptV5`, `PassportV1`, `EuDriverLicenseV1`, `UsDriverLicenseV1`, `IdCardFrV2`, `BillOfLadingV1`. Plus custom builders.

### Recipe 5: Mindee — receipt OCR

```python
from mindee import Client, product
r = mindee_client.parse(product.ReceiptV5, mindee_client.source_from_path("starbucks.jpg"))
print(r.document.inference.prediction.supplier_name.value)
print(r.document.inference.prediction.total_amount.value)
```

### Recipe 6: Mindee — async queue + parse (for batches)

```python
# Best for >10 docs/min — submit to queue, poll for result
job = mindee_client.enqueue(product.InvoiceV4, input_doc)
result = mindee_client.parse_queued(product.InvoiceV4, job.job.id)
while result.job.status != "completed":
    time.sleep(2)
    result = mindee_client.parse_queued(product.InvoiceV4, job.job.id)
print(result.document.inference.prediction.total_amount.value)
```

### Recipe 7: Klippa — financial doc parser (curl)

```bash
curl -X POST https://custom-ocr.klippa.com/api/v1/parseDocument/financial_full \
  -H "X-Auth-Key: $KLIPPA_API_KEY" \
  -F "document=@invoice.pdf" \
  -F "pdf_text_extraction=fast"
```

Returns vendor, customer, lines, VAT breakdown (per rate), payment terms, IBAN, BIC, invoice + due date.

### Recipe 8: Klippa — ID / passport extraction (KYC)

```bash
curl -X POST https://custom-ocr.klippa.com/api/v1/parseDocument/identity_full \
  -H "X-Auth-Key: $KLIPPA_API_KEY" \
  -F "document=@passport.jpg" \
  -F "country_check=true"
```

Returns name, DOB, document number, MRZ check, country, expiration. Plus liveness + face-match endpoint at `/parseDocument/identity_face_match/`.

### Recipe 9: Nanonets — extract with a trained model

```bash
curl https://app.nanonets.com/api/v2/OCR/Model/$MODEL_ID/LabelFile/ \
  -X POST \
  -u $NANONETS_API_KEY: \
  -F "file=@waybill.pdf"
```

Returns the fields you trained the model on (e.g., shipper, consignee, weight, container_no), each with a confidence score.

### Recipe 10: Push extracted invoices to QuickBooks Online

```python
# After Veryfi/Mindee returns the invoice
import requests

invoice = veryfi.process_document("invoice.pdf")
qbo_body = {
    "Line": [{
        "DetailType": "AccountBasedExpenseLineDetail",
        "Amount": invoice["total"],
        "AccountBasedExpenseLineDetail": {
            "AccountRef": {"value": "7"}    # COGS / OPEX
        }
    }],
    "VendorRef": {"value": qbo_vendor_id_for(invoice["vendor"]["name"])},
    "TxnDate": invoice["date"]
}
requests.post(
    f"https://quickbooks.api.intuit.com/v3/company/{REALM_ID}/bill",
    headers={"Authorization": f"Bearer {QBO_TOKEN}"},
    json=qbo_body,
)
```

### Recipe 11: Confidence-based human review gate

```python
LOW_CONF = 0.85
doc = veryfi.process_document("receipt.jpg")
fields_to_review = []
for key in ("total", "tax", "vendor"):
    if doc.get(f"{key}_confidence", 1.0) < LOW_CONF:
        fields_to_review.append(key)
if fields_to_review:
    # Route to human queue (Slack / Linear / Jira)
    notify_review_queue(doc["id"], fields_to_review)
```

Mindee + Klippa + Nanonets return per-field confidence. Always gate auto-posting on confidence.

## Examples

### Example 1: Reimbursement intake — Slack DM to GL coding

**Goal:** Employee DMs receipts to a Slack bot → extract → post to NetSuite as expense report line.
**Steps:**
1. `slack-mcp` listens for `app_mention` with image attachments.
2. Recipe 2 — Veryfi processes the image.
3. Map vendor → GL account via lookup table.
4. POST to NetSuite `ExpenseReportLine` REST endpoint.
5. Recipe 11 — flag low-confidence for FP&A review.

**Result:** Sub-minute reimbursement intake, accountant only touches the flagged items.

### Example 2: AP invoice automation — email to ERP

**Goal:** Vendor emails PDF invoice to `ap@widgetco.com` → extract → match to PO → push to ERP.
**Steps:**
1. `gmail-mcp` polls AP inbox, downloads attachments.
2. Recipe 4 — Mindee parses each invoice.
3. Match invoice.PO# against open POs (ERP query).
4. If match + confidence ≥ 0.92, auto-post bill to ERP. Else, queue for AP clerk.
5. Send acknowledgment + reference number to vendor.

**Result:** 70-90% touchless AP processing.

### Example 3: KYC onboarding — Klippa for ID verification

**Goal:** New customer uploads passport → verify document authenticity + extract → store in CRM.
**Steps:**
1. Customer uploads passport via Jotform (see `smart-form-jotform-formstack`).
2. Recipe 8 — Klippa parses, validates MRZ, runs country check.
3. If `face_match_score ≥ 0.9` and `mrz_valid == true`, mark KYC passed.
4. Push to HubSpot custom property; `redaction-automation-pii` strips ID from any logs.

**Result:** Compliant KYC intake with auditable chain of evidence.

## Edge cases / gotchas

- **Receipt vs invoice schema differs.** Receipts use `ReceiptV5`, invoices use `InvoiceV4`. Don't send a receipt to an invoice parser; both libs error or return junk.
- **Currency detection is locale-sensitive.** Mindee uses ISO-4217; Veryfi defaults to USD on ambiguity. Always validate `currency_code` against expected list.
- **Crumpled / phone-shot receipts.** Veryfi handles these best. For Mindee, ensure ≥150 dpi and de-skew before sending.
- **Multi-page PDFs.** Some endpoints process only page 1 unless `pages` param is set. Send each page separately or use the `analyze_pages` query parameter.
- **PII in receipts (cards, IDs).** All providers can be configured to redact card numbers from response; enable on each request. Never log full PAN/CVV.
- **Webhook delivery.** Veryfi + Mindee + Klippa all support webhook callbacks for async processing. Configure timeout retry logic.
- **Model drift.** Built-in models change quarterly; re-test critical flows monthly on a 100-doc golden set.
- **HIPAA / regulated data.** Not all providers have HIPAA BAA. Verify before sending any covered data (Veryfi offers BAA on enterprise plan).
- **Custom training (Nanonets).** Needs 50-200 labeled samples per template. Cross-validate before going live.
- **Language coverage.** Veryfi: EN best; Mindee: 60+ languages; Klippa: EU langs strong; Nanonets: trained per language.
- **Tax / VAT line correctness.** EU VAT receipts often have multiple VAT rates (e.g., 6% + 21%). Klippa handles per-rate breakdown; Mindee returns totals only by default.
- **Date format ambiguity.** US (MM/DD/YYYY) vs EU (DD/MM/YYYY) — always check `date_format` from the locale field or coerce server-side.
- **Cost.** Per-page billing applies; multi-page invoices cost more. Pre-split into per-invoice PDFs.

## Sources

- [Veryfi API docs](https://docs.veryfi.com/) — receipts + tax forms.
- [Veryfi Python SDK](https://github.com/veryfi/veryfi-python) — official SDK.
- [Mindee Developer Docs](https://developers.mindee.com/) — product catalog + custom builders.
- [Mindee Python SDK](https://github.com/mindee/mindee-api-python) — open-source SDK.
- [Klippa DocHorizon API](https://www.klippa.com/en/api/dochorizon/) — financial + identity parsers.
- [Nanonets API](https://nanonets.com/api-docs/) — custom-trained models.
- [QuickBooks Online API — Bill](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/bill) — for AP pipeline integration.
- [NetSuite Expense Reports REST](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_158156965962.html) — for reimbursement pipeline integration.
- Sister skills: `ai-doc-extraction-hyperscience-rossum-textract`, `ocr-paper-doc-extraction`, `bulk-document-gen-csv`.
