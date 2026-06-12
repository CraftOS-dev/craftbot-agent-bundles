<!--
MCPs: mistral-ocr-mcp, gemini-ocr-mcp (both enabled in agent.yaml)
References: https://docs.mistral.ai/capabilities/document/
            https://ai.google.dev/gemini-api/docs/document-processing
-->

# OCR for scanned / image-only academic papers

Many older academic papers, government PDFs, and foreign-language documents are image-only PDFs without an embedded text layer. Standard text extraction fails. Mistral OCR and Gemini OCR are the SOTA for academic / structured-document OCR with table + equation extraction.

## When to use this skill

- Academic PDFs that return empty text on `pdftotext`
- Older journals (pre-2000) with scanned pages
- Government / regulatory PDFs (FDA submissions, EU documents)
- Foreign-language PDFs (use OCR → DeepL translate pipeline)
- Documents with tables / figures that need structured extraction
- Handwritten notes / charts in image PDFs
- Patent PDFs with image-only claim sections

## When NOT to use

- For text-extractable PDFs → `pdftotext` or `pdfplumber` is faster and cheaper
- For native-digital PDFs → check first whether OCR is even needed
- For full-text scientific search → use Unpaywall + Europe PMC (open access often already extracted)

## Setup

Both MCPs already in `agent.yaml`. API keys provided by user:

```bash
export MISTRAL_API_KEY="..."
export GEMINI_API_KEY="..."
```

## When to choose which engine

| Need | Engine | Why |
|---|---|---|
| Tables (preserve structure) | **Mistral OCR** | Mistral's structured table output is the SOTA |
| Math equations (LaTeX) | **Mistral OCR** | Tuned for STEM |
| Multilingual including low-resource | **Gemini OCR** | Broader language coverage |
| Handwriting | **Gemini OCR** | Generally better on cursive / handwritten |
| Very long documents (100+ pages) | **Gemini** (1M-context) | Single-pass long-document handling |
| Privacy-sensitive | **Mistral** (EU-hosted) | Data residency |
| Cost-optimized | **Mistral OCR** | Lower per-page cost |

When uncertain, run both and compare; defer to the result with cleaner table / equation rendering.

## Common recipes

### Recipe 1 — Mistral OCR for academic paper

```python
from mistralai import Mistral

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
result = client.ocr.process(
    document={"type":"document_url","document_url":"https://example.com/paper.pdf"},
    include_image_base64=False,
)

for page in result.pages:
    print(f"--- Page {page.index} ---")
    print(page.markdown)         # markdown-formatted text with table preservation
```

Output is markdown with table structure preserved (`|...|...|` format). Equations get rendered as LaTeX inline.

### Recipe 2 — Mistral OCR for local PDF

```python
import base64
with open("paper.pdf", "rb") as f:
    pdf_b64 = base64.b64encode(f.read()).decode()

result = client.ocr.process(
    document={"type":"document_url", "document_url": f"data:application/pdf;base64,{pdf_b64}"},
)
```

### Recipe 3 — Gemini OCR for image-PDF

```python
import google.generativeai as genai
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-2.5-pro")

# Upload PDF as inline data
import pathlib
pdf_data = pathlib.Path("paper.pdf").read_bytes()

response = model.generate_content([
    {"mime_type": "application/pdf", "data": pdf_data},
    "Extract all text from this document, preserving tables in markdown format and equations in LaTeX.",
])
print(response.text)
```

### Recipe 4 — OCR + translate pipeline (foreign-language paper)

```python
# 1. OCR with Mistral or Gemini
result = client.ocr.process(document={"type":"document_url","document_url":"https://example.com/chinese-paper.pdf"})

# 2. Translate via deepl-mcp
# DeepL supports document-level translation preserving structure
import deepl  # or call deepl-mcp
translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
translated = translator.translate_text(result.pages[0].markdown, target_lang="EN-US").text

# 3. Now Claude can analyze the translated content
```

### Recipe 5 — Table extraction quality check

After OCR, validate tables visually:

```python
# Mistral OCR returns markdown tables. Convert to pandas for sanity check:
import io, pandas as pd
md_table = page.markdown.split("|---|")[1].split("\n\n")[0]
df = pd.read_csv(io.StringIO(md_table), sep="|").drop(columns=[c for c in [...] if c==""])
print(df.head())
# If columns mis-aligned, re-run with Gemini or manually fix
```

### Recipe 6 — Cost-aware batch OCR

For a corpus of N papers, batch + cache:

```python
# Compute content hash; skip if cached
import hashlib, json, pathlib
cache_dir = pathlib.Path("./ocr_cache")
cache_dir.mkdir(exist_ok=True)

def ocr_cached(pdf_path):
    h = hashlib.sha256(pathlib.Path(pdf_path).read_bytes()).hexdigest()[:16]
    cache_file = cache_dir / f"{h}.json"
    if cache_file.exists():
        return json.loads(cache_file.read_text())
    result = mistral_ocr(pdf_path)
    cache_file.write_text(json.dumps(result))
    return result
```

### Recipe 7 — Equation extraction

For STEM papers:

```python
# Mistral OCR returns LaTeX for math
# Verify with KaTeX/MathJax before embedding in the deliverable
# Some equations need manual cleanup (cross-references, equation numbers)
```

### Recipe 8 — Multi-page chart / figure extraction

Mistral OCR returns figure-image locations as bounding boxes:

```python
result = client.ocr.process(
    document={"type":"document_url","document_url":URL},
    include_image_base64=True,
)
for page in result.pages:
    for img in page.images:
        # img.id, img.top_left_x, img.top_left_y, img.bottom_right_x, img.bottom_right_y
        # img.image_base64
        save_image(img.image_base64, f"figure_p{page.index}_{img.id}.png")
```

Useful when you need the figure separately for citation in the deliverable.

## Edge cases

- **Multi-column layouts:** OCR engines sometimes mis-order columns (reading across instead of down). Test on the first page; if wrong, force single-column processing or post-process by x-coordinate sorting.
- **Footnotes / endnotes:** typically interleaved with main text. Mistral preserves them in-line; you may want to extract separately by font-size signal.
- **Watermarked PDFs:** "DRAFT" / "CONFIDENTIAL" watermarks confuse OCR — they get included as text. Pre-process with a watermark filter or instruct the OCR model to ignore.
- **Equation numbering:** equation references like `(3.14)` sometimes get extracted as text "3.14". Use post-processing regex to normalize.
- **PDF corruption:** if the PDF is malformed, convert to images first (`pdftoppm input.pdf page -png -r 300`) and OCR the images.
- **Cost vs accuracy:** Gemini at higher resolution costs more but extracts handwriting better. Use Gemini for archival / handwritten; Mistral for typeset.
- **Hallucination on low-quality images:** very low-res scans (~150 dpi or worse) can cause OCR to hallucinate plausible-but-wrong text. Cross-check load-bearing numbers against the original image.
- **Tables that span pages:** preserve the page boundary in your extraction so the join logic can stitch.

## Sources

- Mistral OCR: https://docs.mistral.ai/capabilities/document/
- Gemini document understanding: https://ai.google.dev/gemini-api/docs/document-processing
- DeepL document translation: https://developers.deepl.com/docs/api-reference/document
- (Fallback) Tesseract: https://github.com/tesseract-ocr/tesseract (open-source; lower accuracy on academic content)
- (Fallback) AWS Textract: https://aws.amazon.com/textract/ (commercial)

## Related skills

- `paper-search-mcp` — finds the PDFs; this skill extracts when text layer absent
- `semantic-scholar-openalex` — DOI / paper metadata lookup
- `pandoc-branded-deliverables` — markdown extracted text → branded report
