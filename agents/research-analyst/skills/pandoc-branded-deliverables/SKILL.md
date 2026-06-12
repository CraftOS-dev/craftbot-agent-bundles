<!--
Source: https://pandoc.org/MANUAL.html
Reference docs: https://pandoc.org/MANUAL.html#options-affecting-specific-writers
-->

# Pandoc — markdown to branded DOCX / PDF / PPTX

Pandoc is the universal document converter. With `--reference-doc=template.docx` it produces branded Word output that matches the user's corporate template. Same pattern works for PPTX. This is the recommended last step for any research deliverable.

## When to use this skill

- Converting a markdown research report to a branded Word document
- Producing branded PowerPoint from markdown content
- Generating PDF with consistent typography (via xelatex or wkhtmltopdf)
- Bulk export of the same report to multiple formats (md → docx + pdf + html)
- Maintaining a single source of truth (markdown) while producing format-specific deliverables

## When NOT to use

- For one-off ad-hoc PDF of a single chart → use the chart library's direct export
- For interactive HTML reports → keep as Plotly HTML, don't flatten to PDF
- For very-design-heavy outputs (magazine layouts) → use InDesign, not Pandoc

## Setup

```bash
# Pandoc
choco install pandoc          # Windows
brew install pandoc           # macOS
apt install pandoc            # Linux

# PDF engines (one is enough)
choco install miktex          # or basictex on macOS
# Or wkhtmltopdf for HTML→PDF rendering
choco install wkhtmltopdf

# Verify
pandoc --version
```

## Common recipes

### Recipe 1 — Markdown → branded DOCX

```bash
# 1. Get / build a template
pandoc -o template.docx --print-default-data-file reference.docx
# Open template.docx in Word, modify styles (Title, Heading 1, Heading 2, Body Text), save.

# 2. Convert with the template applied
pandoc report.md \
  -o report.docx \
  --reference-doc=template.docx \
  --toc --toc-depth=2 \
  --number-sections \
  --highlight-style=tango
```

Brand styling lives in the template's Style definitions, NOT in the markdown. This separates content from design.

### Recipe 2 — Markdown → branded PPTX

```bash
# Template
pandoc -o template.pptx --print-default-data-file reference.pptx
# Modify slide-master in PowerPoint, save.

# Convert (each "# Heading" becomes a slide title; each "## Heading" becomes content)
pandoc deck.md \
  -o deck.pptx \
  --reference-doc=template.pptx \
  -t pptx
```

For complex slide layouts (multi-column, custom positions), `python-pptx` may be a better fit than Pandoc.

### Recipe 3 — Markdown → PDF

```bash
# Via LaTeX (best typography)
pandoc report.md -o report.pdf \
  --pdf-engine=xelatex \
  --variable=geometry:margin=1in \
  --variable=mainfont:"Source Serif Pro" \
  --variable=monofont:"JetBrains Mono" \
  --highlight-style=tango \
  --toc --toc-depth=2 \
  --number-sections

# Via wkhtmltopdf (HTML-based; simpler templates)
pandoc report.md -o report.pdf \
  --pdf-engine=wkhtmltopdf \
  --css=brand.css
```

### Recipe 4 — Multi-format export from one source

```bash
SOURCE=report.md
BASE=report
pandoc "$SOURCE" -o "$BASE.docx" --reference-doc=template.docx --toc
pandoc "$SOURCE" -o "$BASE.pdf"  --pdf-engine=xelatex --toc
pandoc "$SOURCE" -o "$BASE.html" --standalone --css=brand.css --toc
# All from a single markdown source.
```

### Recipe 5 — Embedding charts

In markdown:

```markdown
## Cohort retention

![Cohort retention curve, Jan-Mar 2025 cohorts](cohort_retention.png){width=6in}
*Figure 1: Cohort retention by signup month. Mar cohort retains 26% at Week 8, up from 21% for Jan cohort — improvement consistent with the v3.2 release.*
```

Pandoc respects the `{width=...}` extension for sizing. The italic caption immediately after the image renders as the figure caption.

### Recipe 6 — YAML front-matter for metadata

```markdown
---
title: "Market Sizing — LFP Battery Storage 2025-2030"
subtitle: "Q2 2026 Research Brief"
author: "Research Analyst"
date: "2026-06-09"
abstract: |
  This brief sizes the LFP battery stationary-storage market...
keywords: [battery, energy storage, LFP, market sizing]
---

# Executive summary
...
```

Pandoc pulls these into the cover page (DOCX) or LaTeX `\maketitle` (PDF).

### Recipe 7 — Cross-references with pandoc-crossref

For numbered figure / table / equation references:

```bash
pip install pandoc-crossref     # or via pandoc filters
pandoc report.md -o report.pdf --filter pandoc-crossref --citeproc
```

Then in markdown:

```markdown
The cohort retention curve in @fig:retention shows improvement...

![Cohort retention](retention.png){#fig:retention width=6in}
```

### Recipe 8 — Citations with bibtex

```bash
# bibliography.bib in BibTeX format
pandoc report.md -o report.pdf \
  --citeproc \
  --bibliography=bibliography.bib \
  --csl=chicago-author-date.csl
```

In markdown:

```markdown
Recent meta-analysis confirms cardiovascular benefit [@smith2024glp1].
```

Pandoc resolves `@smith2024glp1` from the .bib file and formats per the CSL style.

### Recipe 9 — Tables

```markdown
| Metric | Q1 2026 | Q2 2026 | YoY |
|---:|---:|---:|---:|
| Revenue | $12.4M | $15.7M | +27% |
| Gross margin | 62% | 68% | +6pp |
| ARR | $54M | $68M | +26% |
```

For complex tables (merged cells, custom widths), use Pandoc's grid table syntax or generate via pandas `df.to_markdown(tablefmt="grid")`.

## Template customization deep-dive

The reference docx is just a docx with one paragraph per built-in style. Pandoc maps markdown elements to styles by name:

| Markdown | Word style |
|---|---|
| `# H1` | `Heading 1` |
| `## H2` | `Heading 2` |
| Plain paragraph | `Body Text` or `Normal` |
| Code block | `Source Code` |
| Inline code | `Verbatim Char` |
| Blockquote | `Block Quote` |
| Caption (italic after image) | `Image Caption` |
| List item | `List Paragraph` |

To rebrand: open template.docx in Word → Modify each style (font, color, spacing) → save. No other changes needed.

For the same brand across deliverables, version-control `template.docx` alongside the markdown source.

## Edge cases

- **Image paths:** must be relative to the markdown file's directory, or use absolute paths.
- **Heading levels in Word:** if you want Heading 3 to use the docx Heading 3 style, the markdown must have `### H3`. Skipping levels breaks the style mapping.
- **PPTX content overflow:** Pandoc PPTX is finicky about content per slide. If content overflows, split into multiple slides (more `##` headings) rather than fighting the template.
- **Pandoc version:** features like `pandoc-crossref` require Pandoc ≥ 3.0. Check `pandoc --version`.
- **xelatex on Windows:** MikTeX downloads packages on first use; pre-warm by running `pandoc --pdf-engine=xelatex` once.
- **Code-block syntax highlighting in DOCX:** set `--highlight-style=tango` or another built-in style. List: `pandoc --list-highlight-styles`.
- **Mixed RTL / LTR text:** use `--variable=mainfontoptions:'Script=Default'` for Arabic / Hebrew; specify language: `lang=ar` in YAML front-matter.
- **Embedded HTML:** Pandoc preserves raw HTML in HTML output but drops it in DOCX/PDF. For HTML-only features (interactive charts), use `target=html` blocks.

## Deliverable template reference (from role.md)

The role.md "Report templates" section defines the structure. Implement each as markdown then `pandoc` to the target format:

- Executive briefing (1 page) → `pandoc brief.md -o brief.docx --reference-doc=brief-template.docx`
- Research report (long-form) → `pandoc report.md -o report.docx --toc --reference-doc=report-template.docx`
- Trend report → same as above with trend-template.docx
- Competitive intelligence report → CI-template.docx
- Market analysis → market-template.docx
- Scientific synthesis → scientific-template.docx (use `--citeproc` + .bib)

Maintain one branded template per deliverable type.

## Sources

- Pandoc manual: https://pandoc.org/MANUAL.html
- Reference doc usage: https://pandoc.org/MANUAL.html#option--reference-doc
- pandoc-crossref: https://lierdakil.github.io/pandoc-crossref/
- CSL style repository: https://citationstyles.org/
- role.md → "Report templates" (this bundle)

## Related skills

- `docx`, `pdf`, `pptx`, `xlsx` (defaults) — primitives Pandoc orchestrates
- `data-storytelling-plotly-altair` — produces the charts Pandoc embeds
- `git-commit` (default) — version-control the markdown source
