---
name: ocr-paper-doc-extraction
description: OCR paper documents using cloud (AWS Textract, Azure Document Intelligence, Google Document AI, Gemini OCR, Mistral OCR), open-source (Tesseract, PaddleOCR, Surya, olmOCR, GOT-OCR2.0), or LLM-aware. Pick by document type, language, fidelity needed. Use when the user says "OCR this scan", "extract text from paper", "Tesseract", "PaddleOCR", "olmOCR", "Gemini OCR", "Mistral OCR", "scanned PDF to text".
---

# OCR for paper documents — Tesseract / PaddleOCR / cloud / LLM-aware

This skill ships the OCR engine selection + pipeline. For structured receipts/invoices, prefer `receipt-invoice-extraction-veryfi-mindee`. For structured contracts/forms at scale, prefer `ai-doc-extraction-hyperscience-rossum-textract`. This skill is for everything else — pure scan-to-text.

## When to use

User says:

- "OCR this stack of paper contracts / books / archives"
- "Extract text from scanned PDFs"
- "Tesseract / PaddleOCR"
- "Gemini OCR / Mistral OCR"
- "olmOCR / GOT-OCR2.0"
- "Asian language (CJK) OCR"
- "Handwriting recognition"
- "Searchable PDF from scan"

Companion skills:
- `ai-doc-extraction-hyperscience-rossum-textract` — structured extraction (forms, contracts).
- `receipt-invoice-extraction-veryfi-mindee` — receipts + invoices.
- `redaction-automation-pii` — redact in OCR'd output.
- `document-accessibility-pdf-ua` — produce tagged + accessible PDF.

## Setup

```bash
# Tesseract (open-source baseline)
brew install tesseract               # mac
apt install tesseract-ocr            # ubuntu
# Languages: tesseract --list-langs ; add more via tesseract-ocr-eng / -fra / -jpn etc.

# PaddleOCR (best for CJK)
pip install paddlepaddle paddleocr

# EasyOCR (PyTorch-based; 80+ languages)
pip install easyocr

# Surya OCR (best detector + layout in 2025)
pip install surya-ocr

# Tesserocr (Python wrapper for Tesseract)
pip install tesserocr

# olmOCR (LLM-aware OCR — AllenAI; strong on academic PDFs)
pip install olmocr               # or via Docker

# Cloud OCR (use MCPs)
# gemini-ocr-mcp, mistral-ocr-mcp, openai-ocr-mcp, easyocr-mcp
# AWS Textract via boto3
pip install boto3
# Azure Document Intelligence
pip install azure-ai-formrecognizer
# Google Document AI
pip install google-cloud-documentai

# Pre-processing
pip install pillow opencv-python pdf2image
brew install poppler             # pdf2image dependency
```

## Common recipes

### Recipe 1: Pick the OCR engine

| Engine | Best for | Speed | Quality | Cost |
|---|---|---|---|---|
| Tesseract | English baseline + 100+ langs | Fast | OK | Free |
| PaddleOCR | CJK + multi-lang detection | Medium | High | Free |
| EasyOCR | Quick prototypes 80+ langs | Medium | OK | Free |
| Surya OCR | Layout-aware + 90+ langs | Medium | High | Free |
| olmOCR | Academic + structured + complex layouts | Slower | Very high | Free (LLM cost) |
| GOT-OCR2.0 | Formula + table | Slower | Very high | Free |
| Gemini 2.0 OCR (via MCP) | Mixed-content; multimodal | Medium | Very high | API cost |
| Mistral OCR (Pixtral) | Structured docs | Medium | High | API cost |
| AWS Textract | AWS-resident, forms/tables/queries | Fast | Very high | $1.50/1000 pages |
| Azure Document Intelligence | Azure-resident + prebuilt models | Fast | Very high | $1.50/1000 pages |
| Google Document AI | GCP-resident + 200+ processors | Fast | Very high | $1.50/1000 pages |

Default: Tesseract for English ad-hoc; PaddleOCR for CJK; Gemini OCR via MCP for layout-rich PDFs.

### Recipe 2: Tesseract — basic CLI

```bash
# Single image
tesseract scan.png output -l eng
# (writes output.txt)

# PDF → multipage text
tesseract scan.pdf output -l eng pdf       # output.pdf (searchable)
tesseract scan.pdf output -l eng txt

# Multi-language
tesseract scan.png output -l eng+fra+deu

# Tune for layout
tesseract scan.png output --psm 6          # assume uniform block of text
tesseract scan.png output --psm 11         # sparse text
```

PSM modes: 1=auto, 3=full auto (default), 4=single column, 6=block, 11=sparse, 13=raw line.

### Recipe 3: Tesseract — Python wrapper with image preprocessing

```python
import cv2
import pytesseract
from PIL import Image

def preprocess(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Deskew
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45: angle = -(90 + angle)
    else: angle = -angle
    (h,w) = gray.shape
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
    rotated = cv2.warpAffine(gray, M, (w,h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    # Binarize
    _, thresh = cv2.threshold(rotated, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

clean = preprocess("noisy_scan.png")
text = pytesseract.image_to_string(clean, lang="eng", config="--psm 6")
```

### Recipe 4: PaddleOCR — Chinese / Japanese / Korean

```python
from paddleocr import PaddleOCR

# Initialize once (downloads models)
ocr = PaddleOCR(use_angle_cls=True, lang="ch")    # Chinese; lang options: en, japan, korean, etc.

result = ocr.ocr("invoice_zh.png", cls=True)
for line in result[0]:
    bbox, (text, confidence) = line
    print(text, confidence)
```

### Recipe 5: EasyOCR — quick 80+ language

```python
import easyocr
reader = easyocr.Reader(["en","de","fr"])
result = reader.readtext("multilang.png", detail=1)  # detail=1 returns bbox + conf
for bbox, text, conf in result:
    print(text, conf)
```

### Recipe 6: Surya OCR — layout-aware

```python
from surya.ocr import run_ocr
from surya.model.detection.model import load_model as load_det, load_processor as load_det_p
from surya.model.recognition.model import load_model as load_rec, load_processor as load_rec_p
from PIL import Image

det_model = load_det()
det_processor = load_det_p()
rec_model = load_rec()
rec_processor = load_rec_p()

image = Image.open("scan.png")
predictions = run_ocr([image], [["en"]], det_model, det_processor, rec_model, rec_processor)
for p in predictions[0].text_lines:
    print(p.text)
```

### Recipe 7: olmOCR — high-fidelity LLM-aware

```bash
# Self-hosted via Docker / direct
pip install olmocr
olmocr ocr --input scans/ --output extracted/ --model olmocr-7b
# Produces structured JSON with text + layout + metadata per page
```

Best for academic articles, complex multi-column layouts, math/tables.

### Recipe 8: AWS Textract — sync detect_document_text

```python
import boto3
textract = boto3.client("textract", region_name="us-east-1")
with open("scan.png","rb") as f:
    bytes_data = f.read()
res = textract.detect_document_text(Document={"Bytes": bytes_data})
for block in res["Blocks"]:
    if block["BlockType"] == "LINE":
        print(block["Text"], block["Confidence"])
```

For PDFs >5MB or multi-page: use `start_document_text_detection` + S3 + polling.

### Recipe 9: Azure Document Intelligence — read model

```python
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

client = DocumentAnalysisClient(endpoint=AZURE_ENDPOINT, credential=AzureKeyCredential(AZURE_KEY))
with open("scan.pdf","rb") as f:
    poller = client.begin_analyze_document("prebuilt-read", f)
result = poller.result()
for page in result.pages:
    for line in page.lines:
        print(line.content)
```

### Recipe 10: Google Document AI — OCR processor

```python
from google.cloud import documentai_v1
client = documentai_v1.DocumentProcessorServiceClient()
name = client.processor_path(PROJECT, LOCATION, OCR_PROCESSOR_ID)
with open("scan.pdf","rb") as f:
    request = documentai_v1.ProcessRequest(name=name,
        raw_document=documentai_v1.RawDocument(content=f.read(), mime_type="application/pdf"))
result = client.process_document(request=request)
print(result.document.text)
```

### Recipe 11: Searchable PDF (text layer over original image)

```bash
# Tesseract PDF mode = best free way
tesseract input.png output -l eng pdf
# OR ocrmypdf wrapper (handles multi-page PDFs end-to-end)
pip install ocrmypdf
ocrmypdf input.pdf output.pdf --language eng --rotate-pages --deskew --clean
```

`ocrmypdf` is the production-ready CLI: takes scanned PDF, returns searchable PDF + cleans + deskews.

### Recipe 12: Handwriting OCR

```python
# AWS Textract supports handwriting natively
res = textract.analyze_document(Document={"Bytes": handwriting_bytes}, FeatureTypes=["FORMS"])
for b in res["Blocks"]:
    if b.get("TextType") == "HANDWRITING":
        print(b["Text"], b["Confidence"])

# Azure also supports; for Gemini-OCR pass with prompt "Transcribe the handwritten text"
```

### Recipe 13: PDF → images → OCR pipeline

```python
from pdf2image import convert_from_path
images = convert_from_path("scan.pdf", dpi=300)
all_text = ""
for i, img in enumerate(images):
    img.save(f"/tmp/page-{i}.png")
    text = pytesseract.image_to_string(img, lang="eng")
    all_text += f"\n--- Page {i+1} ---\n{text}"
```

300 DPI is the OCR sweet spot. Higher costs more without quality gain on body text.

### Recipe 14: Confidence-based human review

```python
LOW_CONF = 0.85
res = textract.analyze_document(...)
unsure = [b["Text"] for b in res["Blocks"] if b["BlockType"]=="LINE" and b["Confidence"]/100 < LOW_CONF]
if unsure:
    notify_review_queue(doc_id, unsure)
```

### Recipe 15: Multi-engine fallback

```python
def ocr_with_fallback(img_path):
    # Try Tesseract first (free)
    text = pytesseract.image_to_string(img_path)
    if len(text.strip()) > 100:        # decent
        return ("tesseract", text)
    # Fall back to AWS Textract for low-yield scans
    res = textract.detect_document_text(Document={"Bytes": open(img_path,"rb").read()})
    text = "\n".join(b["Text"] for b in res["Blocks"] if b["BlockType"]=="LINE")
    if text.strip():
        return ("textract", text)
    # Last resort: Gemini OCR via MCP for complex layout
    return ("gemini", gemini_ocr_via_mcp(img_path))
```

## Examples

### Example 1: Searchable archive of 5K historical contracts

**Goal:** Lawyer wants to grep across 1990s paper contracts.
**Steps:**
1. Scan/upload to S3.
2. Recipe 11 — ocrmypdf each PDF → searchable.
3. Index full-text in Postgres / Elasticsearch.
4. UI on top for fuzzy search.

**Result:** Searchable contract archive; full-text grep across decades.

### Example 2: Chinese invoice OCR pipeline

**Goal:** Asia ops scan invoices in zh-CN.
**Steps:**
1. Recipe 4 — PaddleOCR.
2. Post-process layout → JSON lines.
3. Confidence gate + AP queue.

**Result:** Localized invoice ingestion without English-only blind spot.

### Example 3: Academic library — olmOCR for complex layouts

**Goal:** University library digitizes 10K papers with multi-column + formulas.
**Steps:**
1. Recipe 7 — olmOCR batch.
2. Structured JSON output indexed for citation graph.
3. Recipe 11 — produce both searchable PDF + structured.

**Result:** Higher fidelity than Tesseract for academic content.

## Edge cases / gotchas

- **DPI too low.** <200 DPI → Tesseract garbles. Aim 300+; cloud OCRs handle lower but still suffer.
- **Color scans confusing.** Convert to grayscale + binarize before Tesseract.
- **Skew + rotation.** Pre-deskew (Recipe 3). Otherwise lines split mid-character.
- **Multi-column not split.** Use `--psm 1` (Tesseract auto OSD + PSM) or layout-aware Surya / olmOCR.
- **Handwriting on Tesseract.** Poor. Use AWS Textract handwriting or Gemini.
- **CJK on Tesseract.** Works but PaddleOCR > Tesseract for CJK.
- **Math / equations.** Tesseract drops them; use GOT-OCR2.0 or olmOCR for academic.
- **Tables.** Tesseract no structure; use Textract `analyze_document` with `TABLES` feature, Azure DI layout model, or Surya.
- **Rotated text.** Tesseract `--psm 0` does OSD (orientation detection); explicitly rotate first via OpenCV.
- **Memory on big PDFs.** Use Recipe 13 page-by-page; don't load entire PDF as one.
- **Cloud OCR async limits.** AWS Textract sync 5MB / 11 pages; async 500MB / 3K pages.
- **Tesseract OEM mode.** OEM 1 (LSTM) is the modern engine; OEM 3 default; LSTM has way better quality.
- **Image too small.** Upscale 2x via `cv2.resize` before OCR (especially for printed body text from phones).
- **Mixed languages in same page.** Multi-lang tesseract `-l eng+fra` works; PaddleOCR initialize per lang.
- **Encoding output.** Always specify UTF-8 when writing OCR output; defaults vary by OS.
- **Privacy.** Cloud OCR sends content to vendor; for confidential / regulated docs, prefer local Tesseract / PaddleOCR.
- **Cost at scale.** Cloud at $1.50/1K pages × 1M pages = $1.5K. FOSS Tesseract trades compute for $0.

## Sources

- [Tesseract OCR docs](https://github.com/tesseract-ocr/tesseract) — open-source baseline.
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) — CJK-strong.
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) — broad-language Python.
- [Surya OCR](https://github.com/VikParuchuri/surya) — layout-aware.
- [olmOCR (AllenAI)](https://allenai.org/blog/olmocr) — LLM-aware OCR.
- [GOT-OCR2.0](https://github.com/Ucas-HaoranWei/GOT-OCR2.0) — formula + table.
- [AWS Textract](https://aws.amazon.com/textract/) — AWS OCR + forms/tables.
- [Azure Document Intelligence](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/) — Azure OCR.
- [Google Document AI](https://cloud.google.com/document-ai) — GCP OCR.
- [ocrmypdf](https://ocrmypdf.readthedocs.io/) — searchable PDF wrapper.
- [pdf2image](https://github.com/Belval/pdf2image) — PDF → image conversion.
- Sister skills: `ai-doc-extraction-hyperscience-rossum-textract`, `receipt-invoice-extraction-veryfi-mindee`, `redaction-automation-pii`, `document-accessibility-pdf-ua`.
