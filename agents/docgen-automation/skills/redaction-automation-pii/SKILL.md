---
name: redaction-automation-pii
description: Detect + redact PII / PHI in documents — Microsoft Presidio (open-source NER + anonymizer), AWS Comprehend Detect-PII, Comprehend Medical Detect-PHI, Google DLP, Adobe Acrobat Pro redaction, Foxit, PDFTron / Apryse. Strip metadata (qpdf, exiftool), redact in-place (mutool), regex backstop. Use when the user says "redact PII", "anonymize", "strip PHI", "Presidio", "AWS Comprehend PII", "Google DLP", "redact PDF", "remove SSN / credit card / phone".
---

# Redaction automation — Presidio / AWS Comprehend / Google DLP / PDF tools

This skill ships PII/PHI detection + true redaction. Do NOT use cosmetic black-box overlays — they leak via copy-paste, OCR, and PDF text streams. True redaction removes the underlying text.

## When to use

User says:

- "Redact PII / PHI / personal data"
- "Anonymize this dataset / document"
- "Strip SSNs / credit cards / passport numbers"
- "Microsoft Presidio / AWS Comprehend / Google DLP"
- "GDPR Article 17 erasure / right to be forgotten"
- "HIPAA Safe Harbor de-identification"
- "Replace names with placeholders for ML training data"
- "PDF redaction"

Companion skills:
- `ai-doc-extraction-hyperscience-rossum-textract` — extract THEN redact pipeline.
- `document-accessibility-pdf-ua` — re-tag PDF after redaction.
- `audit-trail-e-sign-versioning` — preserve pre-redaction version under access control.
- `bulk-document-gen-csv` — batch redaction over many files.

## Setup

```bash
# Microsoft Presidio (open-source) — primary
pip install presidio-analyzer presidio-anonymizer
python -m spacy download en_core_web_lg
# For multi-lang:
python -m spacy download de_core_news_lg
# Or Stanza/transformers models

# AWS Comprehend (PII) + Comprehend Medical (PHI)
pip install boto3
# Required env: AWS credentials

# Google Cloud DLP
pip install google-cloud-dlp
# Required env: GOOGLE_APPLICATION_CREDENTIALS

# Azure AI Language PII recognition
pip install azure-ai-textanalytics

# PDF tools
brew install qpdf mupdf-tools exiftool poppler
# qpdf: linearize / metadata strip
# mutool (mupdf): content removal
# exiftool: EXIF / XMP scrub
# poppler: pdftotext for verification

# Adobe Acrobat Pro DC (UI / paid)
# Foxit PhantomPDF (UI / paid)
# Apryse / PDFTron SDK (paid programmatic)
```

## Common recipes

### Recipe 1: Pick the engine

| Engine | Best for | Notes |
|---|---|---|
| Microsoft Presidio | OSS + Python pipeline | NER (spaCy/Stanza) + 30+ recognizers + analyzer/anonymizer split |
| AWS Comprehend Detect-PII | AWS-native, broad languages | Real-time + async batch |
| AWS Comprehend Medical Detect-PHI | Healthcare / HIPAA | PHI categories + HIPAA-eligible |
| Google DLP | GCP-native + best-in-class catalog | 150+ infoTypes + custom; tokenization options |
| Azure AI Language PII | Azure-native | Decent quality; tight Azure integration |
| Regex + manual rules | Last-mile + low-tech | Always layer on top — never alone |

Default for self-hosted / FOSS: Presidio. For cloud-native: pick by cloud provider. For PHI/HIPAA: AWS Comprehend Medical or HIPAA-eligible Google DLP.

### Recipe 2: Presidio — analyze + anonymize text

```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

text = "John Doe lives at 123 Main St, SSN 123-45-6789, email john@acme.com, phone +1-555-0100."

# Detect
results = analyzer.analyze(
    text=text,
    entities=["PERSON","LOCATION","US_SSN","EMAIL_ADDRESS","PHONE_NUMBER","CREDIT_CARD","IBAN_CODE","IP_ADDRESS","DATE_TIME","MEDICAL_LICENSE"],
    language="en"
)
# Anonymize
out = anonymizer.anonymize(
    text=text,
    analyzer_results=results,
    operators={
        "PERSON": OperatorConfig("replace", {"new_value": "<PERSON>"}),
        "US_SSN": OperatorConfig("mask", {"masking_char":"X","chars_to_mask":11,"from_end":False}),
        "EMAIL_ADDRESS": OperatorConfig("hash", {"hash_type":"sha256"}),
        "DEFAULT": OperatorConfig("replace", {"new_value": "<REDACTED>"})
    }
)
print(out.text)
```

Output: `<PERSON> lives at <REDACTED>, SSN XXXXXXXXXXX, email ab12..., phone <REDACTED>.`

### Recipe 3: Presidio — add custom recognizer (company-specific IDs)

```python
from presidio_analyzer import PatternRecognizer, Pattern

employee_id = PatternRecognizer(
    supported_entity="EMPLOYEE_ID",
    name="EmployeeIDRecognizer",
    patterns=[Pattern(name="emp_id", regex=r"EMP-\d{6}", score=0.95)],
    context=["employee","staff","worker"]
)
analyzer.registry.add_recognizer(employee_id)
```

### Recipe 4: AWS Comprehend — detect PII

```python
import boto3
client = boto3.client("comprehend", region_name="us-east-1")
res = client.detect_pii_entities(Text=text, LanguageCode="en")
for e in res["Entities"]:
    print(e["Type"], text[e["BeginOffset"]:e["EndOffset"]], e["Score"])
```

Categories: NAME, ADDRESS, PHONE, EMAIL, AGE, USERNAME, PASSWORD, URL, BANK_ACCOUNT_NUMBER, BANK_ROUTING, CREDIT_DEBIT_NUMBER, CREDIT_DEBIT_CVV, CREDIT_DEBIT_EXPIRY, PIN, IP_ADDRESS, MAC_ADDRESS, SSN, PASSPORT_NUMBER, DRIVER_ID, DATE_TIME, US_INDIVIDUAL_TAX_IDENTIFICATION_NUMBER, ALL.

### Recipe 5: AWS Comprehend Medical — detect PHI

```python
client = boto3.client("comprehendmedical", region_name="us-east-1")
phi = client.detect_phi(Text=clinical_note)
for e in phi["Entities"]:
    print(e["Category"], e["Type"], e["Text"], e["Score"])
```

PHI categories include: NAME, ADDRESS, AGE, EMAIL, PHONE_OR_FAX, IDENTIFIER, PROFESSION, DATE, URL.

### Recipe 6: Google DLP — inspect + de-identify

```python
from google.cloud import dlp_v2
dlp = dlp_v2.DlpServiceClient()
parent = f"projects/{PROJECT_ID}/locations/global"
res = dlp.deidentify_content(request={
    "parent": parent,
    "inspect_config": {
        "info_types": [{"name":"PERSON_NAME"},{"name":"EMAIL_ADDRESS"},{"name":"US_SOCIAL_SECURITY_NUMBER"},{"name":"CREDIT_CARD_NUMBER"}]
    },
    "deidentify_config": {
        "info_type_transformations": {
            "transformations": [{
                "primitive_transformation": {"replace_with_info_type_config": {}}
            }]
        }
    },
    "item": {"value": text}
})
print(res.item.value)
```

DLP also supports format-preserving encryption + tokenization (`crypto_replace_ffx_fpe_config`).

### Recipe 7: PDF — true content removal with mutool

```bash
# Convert PDF → text, redact, convert back is BAD (loses layout).
# Better: identify redact regions, then use mutool to remove.

# 1) OCR / text extract to find coordinates
pdftotext -bbox-layout input.pdf -    # bounding boxes per word
# Parse for PII spans; map to PDF coordinates

# 2) Apply redaction via mutool (page,bbox)
mutool clean -d input.pdf output.pdf
# More invasive: use Apryse SDK or pdfcpu for in-place redaction

# 3) Sanitize metadata + linearize
qpdf --linearize --object-streams=generate output.pdf final.pdf
exiftool -all:all= -overwrite_original final.pdf
```

Cosmetic black-box overlays (Foxit "Mark for redaction" without Apply) DO NOT remove text. Always Apply.

### Recipe 8: PDF redaction via Apryse SDK (programmatic, true redaction)

```python
# Apryse / PDFTron — paid SDK; reliable
import PDFTron
doc = PDFTron.PDFDoc("input.pdf")
redactions = []
# Find SSN pattern
for page_n in range(doc.GetPageCount()):
    text = doc.GetPage(page_n+1).GetTextExtractor()
    for ssn_match in find_ssns(text):
        redactions.append(PDFTron.Redaction(page_n+1, ssn_match.bbox, "[SSN REDACTED]"))
PDFTron.Redactor.Redact(doc, redactions)
doc.Save("output.pdf", PDFTron.SDFDoc.e_linearized)
```

### Recipe 9: Word docx — find-and-replace via python-docx

```python
from docx import Document
import re

PATTERNS = {
    r"\b\d{3}-\d{2}-\d{4}\b": "[SSN REDACTED]",      # SSN
    r"\b(?:\d[ -]*?){13,19}\b": "[CC REDACTED]",      # Credit card
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b": "[EMAIL REDACTED]"
}
doc = Document("input.docx")
for para in doc.paragraphs:
    for pat, repl in PATTERNS.items():
        for run in para.runs:
            run.text = re.sub(pat, repl, run.text)
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                for pat, repl in PATTERNS.items():
                    for run in para.runs:
                        run.text = re.sub(pat, repl, run.text)
doc.save("output.docx")
```

This is regex-only; layer Presidio (Recipe 2) for NER-driven (names, addresses).

### Recipe 10: Metadata scrub (defang docs before sharing)

```bash
# PDF — strip EXIF/XMP/Producer/Creator
exiftool -all:all= -overwrite_original input.pdf

# Word — clean Properties
python -c "
from docx import Document
d = Document('input.docx')
d.core_properties.author = ''
d.core_properties.last_modified_by = ''
d.core_properties.comments = ''
d.core_properties.title = ''
d.core_properties.subject = ''
d.save('cleaned.docx')
"

# Image — strip GPS / camera
exiftool -all:all= -overwrite_original input.jpg
```

### Recipe 11: HIPAA Safe Harbor (18 identifiers) verification

```python
SAFE_HARBOR_IDENTIFIERS = [
    "NAME","GEOGRAPHY_SUB_STATE","DATE_BIRTH","PHONE","FAX","EMAIL",
    "SSN","MEDICAL_RECORD_NUMBER","HEALTH_PLAN_BENEFICIARY","ACCOUNT_NUMBER",
    "CERTIFICATE_LICENSE","VEHICLE_ID","DEVICE_ID","URL","IP_ADDRESS",
    "BIOMETRIC","FACIAL_PHOTO","OTHER_UNIQUE_ID"
]
# Run Recipe 5 (Comprehend Medical) — if ANY of the 18 remain → fail audit.
```

### Recipe 12: Pseudonymization (reversible tokenization for ML training)

```python
# Format-preserving encryption (FPE) — replace SSN with synthetic SSN
from google.cloud import dlp_v2
dlp = dlp_v2.DlpServiceClient()
res = dlp.deidentify_content(request={
    "parent": f"projects/{PROJECT_ID}/locations/global",
    "deidentify_config": {
        "info_type_transformations": {
            "transformations":[{
                "primitive_transformation":{
                    "crypto_replace_ffx_fpe_config":{
                        "crypto_key":{"kms_wrapped":{"crypto_key_name": KMS_KEY, "wrapped_key": WRAPPED_KEY}},
                        "common_alphabet":"NUMERIC"
                    }
                }
            }]
        }
    },
    "item": {"value":"SSN: 123-45-6789"}
})
# Output retains format; can be reversed with the same key
```

### Recipe 13: Verification pass (re-scan after redaction)

```python
# After redaction, re-run analyzer — fail if anything remains
results = analyzer.analyze(text=redacted_text, language="en")
if results:
    raise RuntimeError(f"Redaction failed: {[r.entity_type for r in results]}")
```

Always verify; never trust the redactor blindly.

## Examples

### Example 1: HIPAA Safe Harbor de-identification of clinical notes

**Goal:** Convert 10K clinical notes into HIPAA-de-identified dataset for analytics.
**Steps:**
1. Recipe 5 — AWS Comprehend Medical batches.
2. For each detected PHI, replace via Recipe 6 deidentify_content.
3. Recipe 11 — verify 18 identifiers gone.
4. Recipe 13 — re-scan as audit.

**Result:** Compliant dataset; auditable.

### Example 2: Contract redaction before counterparty share

**Goal:** Share a benchmark contract with vendor; strip our internal names + pricing.
**Steps:**
1. Recipe 9 — regex pass for emails / phone.
2. Recipe 2 — Presidio NER for names + locations.
3. Recipe 7 — true PDF redaction (not overlay).
4. Recipe 10 — strip metadata.
5. Recipe 13 — verify.

**Result:** Counterparty sees structure without leaks.

### Example 3: ML training data anonymization (pseudonymize for reversibility)

**Goal:** Anonymize prod customer data for staging ML pipeline; need to map back later.
**Steps:**
1. Recipe 12 — Google DLP FFX FPE pseudonymization.
2. Store the wrapped key in KMS; restrict access to compliance officer.
3. Verify (Recipe 13).

**Result:** Pseudonymized data usable for ML; reversible only by privileged user.

## Edge cases / gotchas

- **Cosmetic black-box overlay ≠ redaction.** Foxit "Mark" vs "Apply" — Mark is overlay only. Always Apply (true content removal).
- **PDF text streams persist on overlay.** Even with overlay, the underlying text stream is selectable; mutool / Apryse remove the content.
- **OCR'd PDFs vs native text PDFs.** OCR'd: text in invisible layer beneath image; redaction must remove both layers.
- **Image-only PDFs.** No text to detect via Presidio; first OCR via `ocr-paper-doc-extraction`, then redact in the text layer + black-fill the image region.
- **Handwriting.** Doesn't get detected by NLP-only; pair with vision models.
- **NER misses + false positives.** Names like "Apple" (product or person?) — context matters. Use entity confidence ≥ 0.85.
- **Long PII spans split by lines.** Multi-line addresses; Presidio's `chunk_size` matters.
- **Non-English PII.** Use `spaCy` non-English models or transformer models; AWS Comprehend supports 12 languages but accuracy varies.
- **Credit card validation.** Luhn-check matched digits to reduce false positives.
- **HIPAA Expert Determination vs Safe Harbor.** Two paths; Safe Harbor = 18 identifiers gone; Expert = stats expert sign-off.
- **GDPR pseudonymization ≠ anonymization.** Pseudonymized data is still personal data under GDPR; anonymization must be irreversible.
- **Logs may capture pre-redaction text.** Audit log pipelines + ML training caches can re-introduce PII. Scan downstream.
- **Reversibility key management.** FFX/FPE keys must be vaulted (KMS / HashiCorp Vault); compromise = re-identification.
- **PDF/UA tags survive redaction.** Re-run accessibility tagging after redaction (`document-accessibility-pdf-ua`).
- **Source documents must be access-controlled.** Even after redaction, keep originals in restricted bucket.
- **Don't redact regulatory-required fields.** Tax IDs on tax forms, names on legal docs — redaction destroys legal validity. Confirm policy.
- **DLP throughput.** AWS Comprehend Real-time: 100 KB per call; for batch use Async start_pii_entities_detection_job.

## Sources

- [Microsoft Presidio docs](https://microsoft.github.io/presidio/) — analyzer + anonymizer + recognizers.
- [Presidio Github](https://github.com/microsoft/presidio) — source + examples.
- [AWS Comprehend Detect-PII](https://docs.aws.amazon.com/comprehend/latest/dg/how-pii.html) — categories + API.
- [AWS Comprehend Medical Detect-PHI](https://docs.aws.amazon.com/comprehend-medical/latest/dev/textanalysis-phi.html) — HIPAA-eligible.
- [Google Cloud DLP](https://cloud.google.com/dlp/docs) — infoTypes + de-identify + FPE.
- [Azure AI Language PII](https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/overview) — Azure equivalent.
- [HHS HIPAA Safe Harbor](https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html) — 18 identifiers.
- [Apryse / PDFTron Redaction SDK](https://apryse.com/products/sdk/redaction) — programmatic true redaction.
- [mutool](https://mupdf.com/docs/manual-mutool-clean.html) — content stream cleaning.
- [qpdf](https://qpdf.readthedocs.io/) — PDF transformation + stripping.
- [exiftool](https://exiftool.org/) — metadata scrub.
- Sister skills: `ai-doc-extraction-hyperscience-rossum-textract`, `document-accessibility-pdf-ua`, `audit-trail-e-sign-versioning`, `bulk-document-gen-csv`.
