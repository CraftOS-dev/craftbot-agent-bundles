---
name: document-accessibility-pdf-ua
description: Build and validate accessible PDFs — PDF/UA (ISO 14289), tagged PDF, WCAG 2.2 AA — using veraPDF (FOSS validator), PAC 2024 (free GUI), Adobe Acrobat Pro DC accessibility checker, axe / pa11y for HTML; conversion via Word styles → Tagged PDF, Pandoc, LibreOffice. Use when the user says "PDF/UA", "tagged PDF", "accessible PDF", "WCAG 2.2", "screen-reader friendly", "veraPDF", "508 compliance".
---

# Document accessibility — PDF/UA + tagged PDF + WCAG 2.2

This skill ships PDF + Office accessibility validation + remediation. The 2026 baseline is PDF/UA (ISO 14289) for PDF; WCAG 2.2 AA for HTML; Section 508 for US federal procurement.

## When to use

User says:

- "Make this PDF accessible / PDF/UA-compliant"
- "Tagged PDF for screen readers"
- "WCAG 2.2 AA / Section 508 / EAA 2025 compliance"
- "veraPDF / PAC 2024"
- "Add alt text to images in this doc"
- "Convert Word → accessible PDF"
- "Reading order is wrong"

Companion skills:
- `redaction-automation-pii` — re-tag after redaction.
- `multilingual-template-generation` — accessibility + language markers.
- `bulk-document-gen-csv` — accessibility at batch render time.
- `template-library-templafy-brand` — bake accessibility into the master template.

## Setup

```bash
# veraPDF (FOSS PDF/A + PDF/UA validator)
# Download installer from https://verapdf.org/software/
# Or install via Homebrew:
brew install verapdf
# Or run via Docker:
docker run --rm -v $(pwd):/data verapdf/verapdf-rest

# PAC 2024 (free GUI Windows; Java CLI Mac/Linux)
# https://pac.pdf-accessibility.org/

# Adobe Acrobat Pro DC — built-in accessibility checker (paid)

# axe-core / pa11y for HTML
npm install -g pa11y axe-cli

# Pandoc (for tagged PDF via LaTeX)
brew install pandoc

# LibreOffice headless (for tagged PDF from docx)
brew install --cask libreoffice

# Python tools
pip install pdfa-validator   # alternative validator
pip install pikepdf          # programmatic PDF edit
pip install python-docx      # add alt text + heading styles
```

## Common recipes

### Recipe 1: Standards quick map

| Standard | Scope | Key rules |
|---|---|---|
| PDF/UA (ISO 14289-1) | PDF documents | Tagged tree, reading order, alt text, language, no scanned text-as-image |
| WCAG 2.2 AA | Web + HTML docs | 4 principles (POUR), 50 criteria |
| Section 508 | US fed procurement | Adopts WCAG 2.0 AA + PDF/UA |
| EAA 2025 | EU products + services from June 2025 | Reference WCAG 2.1 / EN 301 549 |
| EN 301 549 | EU accessibility for ICT | Industry baseline ≈ WCAG 2.1 |
| ATAG 2.0 | Authoring tools | Tools themselves accessible |

### Recipe 2: veraPDF — validate PDF/UA-1

```bash
# Linux/Mac CLI
verapdf --flavour ua1 input.pdf
# Returns 0 if conformant; prints rule violations otherwise

# Batch + machine-readable
verapdf --flavour ua1 --format xml input.pdf > report.xml
verapdf --flavour ua1 --format json batch_dir/ > batch-report.json
```

### Recipe 3: veraPDF — PDF/A validation (long-term archival)

```bash
# PDF/A-2b is the practical baseline (allows JPEG2000 etc.)
verapdf --flavour 2b input.pdf
```

PDF/A often required alongside PDF/UA for archival accessibility (e.g., government deposits).

### Recipe 4: PAC 2024 (PDF Accessibility Checker)

```bash
# Windows: pac2024.exe input.pdf
# Mac/Linux: java -jar PAC-2024.jar input.pdf
# Outputs: HTML report with rule-by-rule pass/fail
```

PAC checks Matterhorn Protocol (PDF/UA's machine + human checks).

### Recipe 5: Word → tagged PDF (preserve structure)

In Word desktop:
1. Use **Heading 1/2/3 styles** for structure (not bold font).
2. Add **alt text** on every image: right-click image → View Alt Text.
3. Set **table headers**: Table Tools → Layout → Repeat Header Rows.
4. Use **lists** via list styles (not manual bullets).
5. Set **document language**: Review → Language.
6. File → Save As → PDF → Options → Check "Document structure tags for accessibility" + "Document properties" + "Bitmap text when fonts may not be embedded".

CLI alternative (Mac/Linux):

```bash
soffice --headless --convert-to "pdf:writer_pdf_Export:SelectPdfVersion=2,UseTaggedPDF=true,ExportNotes=true,IsAddPDFTagsForAccessibility=true" input.docx
```

### Recipe 6: pikepdf — add document metadata + lang

```python
import pikepdf
pdf = pikepdf.open("input.pdf", allow_overwriting_input=True)
# Set top-level Lang
pdf.Root.Lang = pikepdf.String("en-US")
# Set marked = true (so reader treats as tagged)
pdf.Root.MarkInfo = pikepdf.Dictionary(Marked=True)
# Set title for accessibility (overrides "filename.pdf" in screen reader)
with pdf.open_metadata() as m:
    m["dc:title"] = "Acme MSA — 2026-06-15"
    m["dc:language"] = "en-US"
pdf.save("output.pdf")
```

### Recipe 7: pa11y — HTML accessibility audit

```bash
pa11y https://your-app.com/proposals/123 --standard WCAG2AA --reporter cli
pa11y --standard WCAG2AA file:///$(pwd)/proposal.html
```

`pa11y-ci` runs against a list of URLs in CI:

```json
// .pa11yci.json
{
  "defaults": {"standard": "WCAG2AA", "timeout": 30000},
  "urls": ["https://app.com/proposal/sample", "file:///dist/proposal.html"]
}
```

### Recipe 8: axe-core — automated accessibility scan

```bash
# In Node test
npm install -D @axe-core/playwright
```

```javascript
const { test, expect } = require("@playwright/test");
const AxeBuilder = require("@axe-core/playwright").default;

test("proposal page is accessible", async ({ page }) => {
  await page.goto("https://your-app.com/proposal/123");
  const results = await new AxeBuilder({ page }).withTags(["wcag2a","wcag2aa","wcag21aa","wcag22aa"]).analyze();
  expect(results.violations).toEqual([]);
});
```

### Recipe 9: python-docx — bulk add alt text to images

```python
from docx import Document
from docx.oxml.ns import qn

doc = Document("templates/master-msa.docx")
for shape in doc.inline_shapes:
    docPr = shape._inline.find(qn("wp:docPr"))
    if docPr is not None:
        docPr.set("descr", "Widget Co logo")     # alt text
        docPr.set("title", "Logo")
doc.save("templates/master-msa-accessible.docx")
```

### Recipe 10: Manually remediate PDF in Adobe Acrobat Pro

1. Open PDF → Tools → Accessibility → Autotag Document.
2. Open Tags panel → drag tags into correct reading order.
3. Right-click image tags → Properties → Alternate Text.
4. Tools → Accessibility → Reading Order → set table headers per column.
5. Tools → Accessibility → Accessibility Check → fix flagged issues.
6. Save.

Re-validate via Recipe 2.

### Recipe 11: Conversion pipeline — Markdown → Tagged PDF via Pandoc

```bash
# Use Pandoc with LaTeX engine that supports tagging
pandoc input.md \
  --pdf-engine=lualatex \
  --metadata title="Acme MSA" \
  --metadata lang=en-US \
  -V documentclass=article \
  -V pdfmanagement \
  -o output.pdf

# Verify
verapdf --flavour ua1 output.pdf
```

For complex layouts, use `--pdf-engine=tectonic` with `accessibility` package.

### Recipe 12: HTML → Tagged PDF via WeasyPrint

```python
from weasyprint import HTML, CSS
HTML("input.html").write_pdf(
    "output.pdf",
    stylesheets=[CSS(string="@page { size: A4; margin: 1in; }")],
    pdf_variant="pdf/ua-1",         # WeasyPrint 60+ supports PDF/UA
    presentational_hints=True
)
```

Requires WeasyPrint >= 60.

### Recipe 13: CI gate — fail PR if PDFs aren't accessible

```yaml
# .github/workflows/accessibility.yml
name: Accessibility CI
on: [pull_request]
jobs:
  pdf-ua:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install veraPDF
        run: |
          wget https://software.verapdf.org/releases/verapdf-installer.zip
          unzip verapdf-installer.zip
          ./verapdf-greenfield-*/verapdf-install --silent
      - name: Validate all PDFs
        run: |
          for pdf in dist/*.pdf; do
            verapdf --flavour ua1 "$pdf" || exit 1
          done

  html-wcag:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm install -g pa11y-ci
      - run: pa11y-ci --config .pa11yci.json
```

### Recipe 14: Color contrast verification

```python
# WCAG 2.2 requires 4.5:1 for body text, 3:1 for large text
def contrast_ratio(rgb1, rgb2):
    def luminance(rgb):
        r, g, b = [c/255 for c in rgb]
        r = ((r+0.055)/1.055)**2.4 if r > 0.03928 else r/12.92
        g = ((g+0.055)/1.055)**2.4 if g > 0.03928 else g/12.92
        b = ((b+0.055)/1.055)**2.4 if b > 0.03928 else b/12.92
        return 0.2126*r + 0.7152*g + 0.0722*b
    l1, l2 = luminance(rgb1), luminance(rgb2)
    return (max(l1,l2)+0.05) / (min(l1,l2)+0.05)

assert contrast_ratio((26,115,232), (255,255,255)) >= 4.5  # brand primary on white
```

### Recipe 15: Heading-order check

```python
from docx import Document
doc = Document("template.docx")
levels_seen = []
for para in doc.paragraphs:
    style = para.style.name
    if style.startswith("Heading "):
        levels_seen.append(int(style.split()[1]))
# Verify no skipped levels
for i in range(1, len(levels_seen)):
    if levels_seen[i] > levels_seen[i-1] + 1:
        raise ValueError(f"Heading skip: {levels_seen[i-1]} → {levels_seen[i]}")
```

## Examples

### Example 1: Federal RFP response → 508 compliance

**Goal:** Win government RFP requires Section 508 PDF deliverables.
**Steps:**
1. Author in Word using styles + alt text (Recipe 5, 9).
2. Export with tagging (Recipe 5).
3. Recipe 2 — validate PDF/UA via veraPDF.
4. Recipe 10 — fix any failures in Acrobat Pro.
5. Recipe 6 — finalize language metadata.

**Result:** Compliant deliverable; no 508 reject letter.

### Example 2: SaaS proposal HTML viewer — WCAG 2.2 AA

**Goal:** PandaDoc-style web viewer for proposals; auditable for WCAG.
**Steps:**
1. Recipe 8 — axe-core in Playwright suite.
2. Recipe 14 — contrast verification in design tokens.
3. Recipe 7 — pa11y-ci on sample URLs in PR.

**Result:** PRs blocked on accessibility regressions.

### Example 3: Quarterly bulk re-validation of contract archive

**Goal:** 5K-PDF contract repo; verify still PDF/UA after archive migration.
**Steps:**
1. Recipe 2 — batch mode on full repo.
2. Aggregate XML/JSON report.
3. Flag failures for remediation; route via `linear-mcp`.

**Result:** Continuous accessibility health on the archive.

## Edge cases / gotchas

- **Tagged PDF ≠ PDF/UA.** Tagged is a prerequisite; PDF/UA adds structural and semantic rules. veraPDF tests the full set.
- **Autotag in Acrobat is often wrong.** Especially on multi-column or tabular content; review before shipping.
- **Decorative images.** Mark via `<Artifact>` tag, not empty alt text — empty alt = "no description provided" (WCAG fail).
- **Empty header cells in tables.** PDF/UA flags missing header cell text; fix in source.
- **Scanned PDFs are not accessible.** OCR + tagging required first.
- **Adobe Acrobat "save as PDF/A" loses tagging.** Save as PDF first, then run Preflight → PDF/UA preset.
- **Languages mixed in one doc.** Wrap foreign-language spans with `Lang` attribute (Recipe 6 for top-level).
- **List nesting depth.** Some screen readers cap at ~6 levels; flatten or restructure.
- **Footnotes via inline numbers.** Mark with `Note` structure tag, not raw inline text.
- **Decorative borders / dividers.** Tag as Artifact; otherwise screen reader reads "horizontal rule" repeatedly.
- **Form fields need labels.** Each `<TextField>` / `<CheckBox>` needs a `<Label>` parent or `Lbl` adjacent.
- **Brand fonts without good Unicode mapping.** Cause garbled screen reader output; verify ActualText where needed.
- **PDF/A + PDF/UA combined.** Validate both; some rules conflict (transparency etc.). Use PDF/A-2u or PDF/A-3u + PDF/UA pair.
- **Inline math.** MathML preferred; tag with `<Formula>` + alt text fallback.
- **WCAG 2.2 vs 2.1 vs 2.0.** 2.2 added 9 new criteria (June 2023); EU EN 301 549 currently maps 2.1 in most member states.
- **Section 508 refresh (2018).** Still references WCAG 2.0 AA; new federal regs update is in flight as of 2026.
- **WeasyPrint pdf/ua-1 support.** Recent feature; verify version + accept some rule failures still need manual fixes.

## Sources

- [PDF/UA — ISO 14289-1](https://www.pdfa.org/resource/iso-14289/) — standard overview.
- [veraPDF docs](https://docs.verapdf.org/) — PDF/A + PDF/UA validation.
- [PAC 2024](https://pac.pdf-accessibility.org/) — free PDF accessibility checker.
- [Matterhorn Protocol](https://www.pdfa.org/resource/the-matterhorn-protocol-2-0/) — PDF/UA machine + human checks.
- [WCAG 2.2 quickref](https://www.w3.org/WAI/WCAG22/quickref/) — criteria reference.
- [Section 508 standards](https://www.section508.gov/) — US federal procurement.
- [EAA 2025](https://ec.europa.eu/social/main.jsp?catId=1202) — EU Accessibility Act.
- [EN 301 549](https://www.etsi.org/standards#page=1&search=EN%20301%20549) — EU ICT accessibility.
- [Adobe Acrobat Accessibility Guide](https://www.adobe.com/accessibility/pdf/pdf-accessibility-overview.html) — Acrobat-side remediation.
- [pa11y](https://pa11y.org/) — HTML CLI scanner.
- [axe-core](https://github.com/dequelabs/axe-core) — Deque's accessibility engine.
- [pikepdf](https://pikepdf.readthedocs.io/) — Python PDF manipulation.
- [WeasyPrint](https://doc.courtbouillon.org/weasyprint/stable/) — HTML to PDF with PDF/UA support.
- Sister skills: `redaction-automation-pii`, `multilingual-template-generation`, `bulk-document-gen-csv`, `template-library-templafy-brand`.
