---
name: bulk-document-gen-csv
description: Generate 1000s of personalized documents from CSV / JSON / DB rows using DocSpring (hosted batch PDF), PDFmonkey (alt hosted), docxtemplater / python-docx-template + WeasyPrint / LibreOffice (FOSS pipeline). Worker queue (Celery / BullMQ / Sidekiq) + S3 upload + signed URL delivery. Use when the user says "bulk document generation", "mail merge at scale", "10000 PDFs from CSV", "DocSpring", "PDFmonkey", "personalized renewal letters", "batch render".
---

# Bulk document generation — DocSpring / PDFmonkey / docxtemplater / Jinja+WeasyPrint

This skill ships the "1 template + N rows = N documents" pipeline. Hosted services (DocSpring / PDFmonkey) for managed; FOSS stack (docxtpl + WeasyPrint + queue) for self-host.

## When to use

User says:

- "Generate 5,000 renewal letters from this CSV"
- "Bulk mail merge"
- "DocSpring / PDFmonkey"
- "Customer-specific PDF per row"
- "Annual statement mailing"
- "Tax-letter / W-2 / 1099 batch printing"
- "Generate per-recipient certificates"

Companion skills:
- `template-library-templafy-brand` — source of the template.
- `dynamic-pricing-variable-insertion` — per-row pricing logic.
- `e-signature-docusign-adobe-sign-pandadoc` — batch send for sign (DocuSign Bulk Send).
- `audit-trail-e-sign-versioning` — manifest of every output.

## Setup

```bash
# DocSpring (hosted PDF batch)
# Required env: DOCSPRING_API_TOKEN
# https://docspring.com/docs/api/

# PDFmonkey (alternative)
# Required env: PDFMONKEY_API_KEY
# https://www.pdfmonkey.io/api-docs

# Anvil PDF (PDF fill via API)
# Required env: ANVIL_API_KEY

# FOSS stack
pip install docxtpl python-docx jinja2 weasyprint pandas tqdm
# or Node:
npm install docxtemplater pizzip handlebars puppeteer

# Worker queue
pip install celery redis      # or rq
# or Node:
npm install bullmq ioredis

# Storage
pip install boto3              # S3
# or:
# google-drive-mcp / aws-s3-mcp
```

## Common recipes

### Recipe 1: Pick the stack

| Stack | Best for | Pricing (approx 2026) |
|---|---|---|
| DocSpring | 100-100K docs/month; hosted | $0.005-0.02/doc |
| PDFmonkey | Similar; cheaper for low vol | $19-99/mo + per-doc |
| Anvil | PDF-form-filling specifically | $89-499/mo |
| Documate batch | Legal-heavy templates | Quote |
| FOSS (docxtpl + WeasyPrint + S3) | Cost-sensitive; full control | Free + dev time |
| DocuSign Bulk Send | Bulk send for sign (not gen) | DocuSign tier |
| Carbone.io | Open-source render engine | Free / hosted tier |
| Stamper.io | Hosted PDF templating | $29-99/mo |

Default for ad-hoc < 10K: FOSS stack. For 10K-100K + SLA: DocSpring. For PDF form filling: Anvil.

### Recipe 2: docxtpl — render N docs from a CSV

```python
import pandas as pd
from docxtpl import DocxTemplate
from pathlib import Path
from tqdm import tqdm

template_path = "templates/renewal-letter.docx"
df = pd.read_csv("input/renewals.csv")        # has columns: customer_id, name, address, plan, due_date, amount
output_dir = Path("dist/renewals/")
output_dir.mkdir(parents=True, exist_ok=True)

for _, row in tqdm(df.iterrows(), total=len(df)):
    doc = DocxTemplate(template_path)
    doc.render(row.to_dict())
    safe_id = str(row["customer_id"]).replace("/", "_")
    doc.save(output_dir / f"renewal-{safe_id}.docx")
```

Template `renewal-letter.docx` contains tokens: `{{ name }}`, `{{ address }}`, `{{ plan }}`, conditional `{% if amount > 100 %}...{% endif %}`.

### Recipe 3: docx → PDF batch (LibreOffice headless)

```bash
# Convert all .docx in dist/renewals/ to PDF
soffice --headless --convert-to pdf --outdir dist/renewals/pdf/ dist/renewals/*.docx

# Parallelize with GNU parallel for speed:
ls dist/renewals/*.docx | parallel -j 8 soffice --headless --convert-to pdf --outdir dist/renewals/pdf/ {}
```

### Recipe 4: Jinja2 + WeasyPrint (HTML → PDF) batch

```python
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

env = Environment(loader=FileSystemLoader("templates"))
tmpl = env.get_template("renewal.html")

df = pd.read_csv("input/renewals.csv")
for _, row in df.iterrows():
    html_str = tmpl.render(row.to_dict())
    HTML(string=html_str).write_pdf(f"dist/renewals/{row['customer_id']}.pdf")
```

WeasyPrint advantages: CSS Paged Media (cover page, headers, footers, page-breaks).

### Recipe 5: DocSpring — batch submission

```python
import requests
df = pd.read_csv("renewals.csv")
batch = requests.post(
    f"https://api.docspring.com/api/v1/templates/{TEMPLATE_ID}/submissions/batch",
    auth=(DOCSPRING_TOKEN, ""),
    json={
        "data_requests": [row.to_dict() for _, row in df.iterrows()],
        "test": False,
        "data_requests_test_mode": False
    }
)
batch_id = batch.json()["id"]
# Poll status
while requests.get(f"https://api.docspring.com/api/v1/batch_submissions/{batch_id}",
                   auth=(DOCSPRING_TOKEN, "")).json()["state"] != "processed":
    time.sleep(5)
# Download
for sub in requests.get(f"https://api.docspring.com/api/v1/batch_submissions/{batch_id}/submissions",
                        auth=(DOCSPRING_TOKEN, "")).json():
    download(sub["download_url"], f"dist/{sub['data_requests'][0]['customer_id']}.pdf")
```

DocSpring caps batch size at ~1000 per request; chunk for larger.

### Recipe 6: PDFmonkey — generate per-row

```bash
curl -X POST https://api.pdfmonkey.io/api/v1/documents \
  -H "Authorization: Bearer $PDFMONKEY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "document": {
      "document_template_id": "tmpl_...",
      "status": "pending",
      "payload": "{\"customer_id\":\"C001\",\"name\":\"Acme\",\"amount\":2400}",
      "meta": "{\"_filename\":\"renewal-C001.pdf\"}"
    }
  }'
```

PDFmonkey is async; receive via webhook or poll.

### Recipe 7: Celery worker queue for FOSS pipeline

```python
# tasks.py
from celery import Celery
from docxtpl import DocxTemplate
import boto3

app = Celery("docs", broker="redis://localhost:6379/0")
s3 = boto3.client("s3")

@app.task(bind=True, max_retries=3)
def render_one(self, row, batch_id):
    try:
        doc = DocxTemplate("templates/renewal-letter.docx")
        doc.render(row)
        out = f"/tmp/{row['customer_id']}.docx"
        doc.save(out)
        # Convert via LibreOffice
        subprocess.run(["soffice","--headless","--convert-to","pdf","--outdir","/tmp",out], check=True)
        # Upload to S3
        s3.upload_file(f"/tmp/{row['customer_id']}.pdf",
                       "doc-output",
                       f"batches/{batch_id}/{row['customer_id']}.pdf")
        return {"customer_id": row["customer_id"], "status": "ok"}
    except Exception as e:
        self.retry(countdown=60, exc=e)

# Dispatcher
def dispatch_batch(df, batch_id):
    for _, row in df.iterrows():
        render_one.delay(row.to_dict(), batch_id)
```

Run `celery -A tasks worker --concurrency=8` then call `dispatch_batch(df, batch_id)`.

### Recipe 8: Manifest + per-row status tracking

```python
# Generate manifest with output URL per row
manifest = []
for _, row in df.iterrows():
    try:
        # render + upload
        s3_uri = f"s3://doc-output/batches/{batch_id}/{row['customer_id']}.pdf"
        url = generate_signed_url(s3_uri, expires=86400*7)    # 7-day signed
        manifest.append({"customer_id": row["customer_id"], "status":"ok",
                         "s3_uri": s3_uri, "signed_url": url, "rendered_at": utcnow()})
    except Exception as e:
        manifest.append({"customer_id": row["customer_id"], "status":"error",
                         "error": str(e), "rendered_at": utcnow()})
pd.DataFrame(manifest).to_csv(f"dist/{batch_id}/manifest.csv", index=False)
```

Manifest CSV columns: `customer_id, status, s3_uri, signed_url, error, rendered_at`.

### Recipe 9: Email delivery loop (with `gmail-mcp` or SendGrid)

```python
import sendgrid
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64

sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
for row in df.to_dict("records"):
    with open(f"dist/{row['customer_id']}.pdf", "rb") as f:
        pdf_b64 = base64.b64encode(f.read()).decode()
    msg = Mail(
        from_email="renewals@widgetco.com",
        to_emails=row["email"],
        subject=f"Your {row['plan']} renewal — {row['due_date']}",
        html_content=f"Hi {row['name']},<br>Attached renewal letter."
    )
    msg.add_attachment(Attachment(FileContent(pdf_b64),
                                  FileName(f"renewal-{row['customer_id']}.pdf"),
                                  FileType("application/pdf"),
                                  Disposition("attachment")))
    sg.send(msg)
```

### Recipe 10: DocuSign Bulk Send (one envelope, many recipients)

```python
# Different from doc-gen; one signed template sent to N recipients
from docusign_esign import BulkSendApi, BulkSendingList
bulk_api = BulkSendApi(api_client)

bulk_list = BulkSendingList(name="Renewals Q2", bulk_copies=[
    {"recipients":[{"name":r["name"],"email":r["email"],"roleName":"signer"}]}
    for r in df.to_dict("records")
])
created = bulk_api.create_bulk_send_list(account_id=ACCT, bulk_sending_list=bulk_list)
bulk_api.send(account_id=ACCT, envelope_id=template_env_id, bulk_send_list_id=created.list_id)
```

DocuSign Bulk Send caps at 1K recipients per list by default; quotas tier-dependent.

### Recipe 11: Idempotency + resumability

```python
# Track per-row state in Postgres / SQLite so re-runs skip done rows
import sqlite3
conn = sqlite3.connect("batch_state.db")
conn.execute("CREATE TABLE IF NOT EXISTS rendered (batch_id TEXT, customer_id TEXT PRIMARY KEY, status TEXT, ts INTEGER)")
def already_done(batch_id, cid):
    return conn.execute("SELECT 1 FROM rendered WHERE batch_id=? AND customer_id=? AND status='ok'",
                        (batch_id, cid)).fetchone() is not None

for row in df.to_dict("records"):
    if already_done(batch_id, row["customer_id"]):
        continue
    render_one(row)
    conn.execute("INSERT OR REPLACE INTO rendered VALUES (?,?,?,?)",
                 (batch_id, row["customer_id"], "ok", int(time.time())))
    conn.commit()
```

### Recipe 12: Validation pass — dry run + spot check

```python
# 1) Render first 5 rows; visually verify
df.head(5).apply(lambda r: render_one(r.to_dict(), "DRYRUN"), axis=1)
# 2) Manifest spot check — sample 10% via random.sample
import random
sample = random.sample(manifest, max(10, len(manifest)//10))
for s in sample:
    assert os.path.getsize(local_path(s["s3_uri"])) > 1024     # not empty
```

## Examples

### Example 1: Q2 customer renewal letters (5K)

**Goal:** Email 5,000 personalized renewal letters with line items.
**Steps:**
1. Pull CSV from CRM (HubSpot / Salesforce).
2. Recipe 2 — docxtpl render.
3. Recipe 3 — LibreOffice → PDF.
4. Recipe 7 — Celery queue across 8 workers.
5. Recipe 9 — SendGrid bulk email.
6. Recipe 8 — manifest CSV.

**Result:** Q2 renewals out in 30 minutes.

### Example 2: 1099-NEC year-end mailing (DocSpring)

**Goal:** 800 1099-NEC PDFs for IRS filing season.
**Steps:**
1. Pull payee data from QuickBooks / NetSuite.
2. Recipe 5 — DocSpring batch with IRS-form-aligned template.
3. Recipe 10 — DocuSign Bulk Send for e-sign / acknowledgment.
4. Postmark / SendGrid attaches + mails certified PDFs.

**Result:** Annual filings batch-processed; manifest archived.

### Example 3: Onboarding kit for 200 new hires (folder-per-recipient)

**Goal:** New hire gets offer letter + handbook + 83(b) election (where applicable) + I-9.
**Steps:**
1. CSV per hire: name, start_date, salary, equity_grant.
2. Recipe 2 — render 4 docs per row.
3. Bundle as ZIP per hire via Recipe 7 worker.
4. Upload ZIPs to S3 + signed URL.
5. `gmail-mcp` emails the link to candidate manager.

**Result:** No-touch onboarding kit per new hire.

## Edge cases / gotchas

- **LibreOffice headless concurrency.** Multiple `soffice` instances clash on same `$HOME/.config/libreoffice`. Use `-env:UserInstallation=file:///tmp/lo-$RANDOM` per worker.
- **Filename collisions.** Use unique row IDs not customer names. Slugify path-safe.
- **CSV encoding.** UTF-8 vs UTF-16 vs CP1252 — read with explicit encoding; mojibake silently corrupts names.
- **CRLF vs LF in CSV.** Pandas handles; lower-level parsers may not.
- **Large CSV memory.** Use `pandas.read_csv(chunksize=...)` for >1GB files; never load entirely.
- **Date / currency formatting per row's locale.** Use Babel / Intl.NumberFormat; never f-string monetary values.
- **Empty / NaN values explode templates.** Pre-clean: `df = df.fillna({"middle_name":"","amount":0})`.
- **Conditional logic edge.** Jinja2 raw `{% if amount > 100 %}` fails on string amounts; coerce types early.
- **Template versioning.** Pin template version in batch metadata; reproducibility matters.
- **Throttling on hosted APIs.** DocSpring 100 req/min; PDFmonkey 60 req/min — chunk + backoff.
- **S3 throttles per prefix.** Spread across multiple prefixes (sharding).
- **Bulk email deliverability.** SendGrid / Postmark dedicated IP + DKIM + SPF + warmup, else inbox provider drops.
- **Per-row PII handling.** Encrypt at rest; signed URL TTL appropriate to use; never log raw row.
- **Audit retention.** Manifest + S3 versioning + Object Lock for compliance.
- **Rollback.** If 100 out of 5K send wrong, batch-revoke signed URLs (rotate S3 prefix) + re-send corrected.
- **Disk full mid-batch.** Use ephemeral worker scratch; upload+delete; never keep 5K PDFs locally.
- **Idempotency keys per row.** Postmark / SendGrid: use customer_id as IDK; prevent duplicate email on retry.
- **Test in sandbox / staging.** Bulk email is hard to undo; always start with 5-row sanity test.

## Sources

- [DocSpring API docs](https://docspring.com/docs/api/) — batch submissions + templates.
- [PDFmonkey API](https://www.pdfmonkey.io/api-docs) — async PDF generation.
- [Anvil PDF docs](https://www.useanvil.com/docs/api/) — PDF form filling.
- [Carbone.io](https://carbone.io/api-reference.html) — open-source render engine.
- [docxtpl](https://docxtpl.readthedocs.io/) — Word templating with Jinja syntax.
- [docxtemplater](https://docxtemplater.com/) — Node equivalent.
- [WeasyPrint](https://doc.courtbouillon.org/weasyprint/) — HTML to PDF with CSS Paged Media.
- [Celery + Redis](https://docs.celeryq.dev/) — worker queue.
- [BullMQ + Redis](https://docs.bullmq.io/) — Node worker queue.
- [DocuSign Bulk Send](https://developers.docusign.com/docs/esign-rest-api/how-to/send-bulk-envelopes/) — bulk send for signature.
- [SendGrid v3 API](https://docs.sendgrid.com/api-reference/mail-send/mail-send) — bulk email.
- [Postmark API](https://postmarkapp.com/developer) — transactional email.
- [AWS S3 Multipart + Presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html) — bulk storage.
- Sister skills: `template-library-templafy-brand`, `dynamic-pricing-variable-insertion`, `e-signature-docusign-adobe-sign-pandadoc`, `audit-trail-e-sign-versioning`.
