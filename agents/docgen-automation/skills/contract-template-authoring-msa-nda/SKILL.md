---
name: contract-template-authoring-msa-nda
description: Author reusable, conditional-logic contract templates (MSA, NDA, employment, vendor, customer T&C, DPA, AUP, BAA, SLA) anchored to Bonterms / Common Paper / YC / NVCA canonical templates. Variable fields + conditional clauses + version control + binding-language hand-off to legal-counsel. Use when the user says "draft an MSA template", "build NDA template", "build employment offer letter template", "set up contract template library", "version our SaaS T&C".
---

# Contract template authoring (MSA / NDA / employment / vendor / T&C)

This skill builds **the source template** — the master, conditional-logic-bearing artifact a doc-gen engine renders from. It does NOT produce binding contract language; for that, hand off to the `legal-counsel` sibling agent.

## When to use

User says:

- "Author an MSA / NDA / employment / vendor / customer T&C / DPA / AUP / BAA / SLA template"
- "Build a template library for [contract type]"
- "Anchor our [contract type] to Bonterms / Common Paper / YC SAFE / NVCA"
- "Version control on legal templates"
- "Add a conditional [SOC 2 addendum / CA non-compete carve-out / HIPAA BAA] to the MSA"
- "Modular clause library"

Companion skills:
- `conditional-logic-doc-assembly` — execution engine (Documate / HotDocs / Docassemble) for rendering this template.
- `template-library-templafy-brand` — brand consistency + asset injection layer.
- `contract-redlining-automation` — track-change generation against this template.
- `clm-ironclad-contractworks-integration` — push rendered output to a CLM repository.

## Setup

```bash
# Author with code (Python / Node) — no SaaS required, free
pip install docxtpl python-docx jinja2     # Python docx templating
npm install -g docxtemplater                # Node docx templating
brew install pandoc                          # markdown ↔ docx ↔ pdf
pip install weasyprint                       # HTML → PDF

# Anchor templates — pull canonical sources
curl -fsSL https://commonpaper.com/standards/ -o sources/common-paper-index.html
curl -fsSL https://bonterms.com/ -o sources/bonterms-index.html
# Bonterms + Common Paper templates are downloadable docx — clone to source-of-truth repo

# SaaS authoring (commercial)
# Documate: https://documate.org/  (FOSS / hosted tier)
# HotDocs:  https://www.hotdocs.com/  (legal industry standard, paid)
# Templafy: https://www.templafy.com/  (brand + Office-native, enterprise)
```

Auth / API keys:
- `HOTDOCS_*` — HotDocs Cloud Services tenant + OAuth client id/secret if using SaaS authoring.
- `TEMPLAFY_*` — Templafy tenant + API token for upload.
- `GITHUB_TOKEN` — required to version templates in a private repo via `github` MCP.

## Common recipes

### Recipe 1: Pick the authoring engine

| Engine | Best for | License | Trigger |
|---|---|---|---|
| python-docx-template (docxtpl) | code-first orgs; CI render | OSS | "render via Python", "no SaaS budget" |
| docxtemplater (Node) | code-first JS orgs | OSS | "render via Node" |
| Jinja2 + WeasyPrint | HTML source → pixel-perfect PDF | OSS | "high-fidelity PDF", "CSS Paged Media" |
| Documate | interview-driven legal authoring | FOSS / hosted | "self-serve interview flow" |
| HotDocs | legal-industry-standard conditional logic | Paid | "Big Law standard", "existing HotDocs shop" |
| Docassemble | Python-extensible interview engine | OSS | "self-host", "custom Python rules" |
| Templafy | Office-native + brand injection | Enterprise | "Word/PPT-first org", "brand-critical" |

### Recipe 2: Pull a canonical base template

```bash
# Common Paper standardized templates (NDA, Cloud Service, DPA, AUP, MSA)
mkdir -p sources/common-paper
curl -fsSL "https://commonpaper.com/standards/cloud-service-agreement/" -o sources/common-paper/csa.html
# Common Paper publishes docx; manually download the latest revision

# Bonterms modules (Cloud Terms, AUP, DPA, SLA)
mkdir -p sources/bonterms
# Bonterms publishes docx + linked dictionary; download each module separately

# YC SAFE (post-money default) + advisor agreement
curl -fsSL "https://www.ycombinator.com/documents" -o sources/yc-index.html

# NVCA Series A canonical docs
curl -fsSL "https://nvca.org/resources/model-legal-documents/" -o sources/nvca-index.html
```

### Recipe 3: Define the merge-field schema

```yaml
# template_schema.yaml — single source of truth for every field downstream callers must supply
template: msa-saas-customer-side
version: 2.4.0
fields:
  effective_date:
    type: date
    required: true
    format: "YYYY-MM-DD"
  customer:
    name: { type: string, required: true }
    entity_state: { type: string, required: true }
    entity_type: { type: enum, values: [C-corp, LLC, LP, S-corp, GmbH, Ltd], required: true }
    jurisdiction: { type: string, required: true }
    requires_soc2: { type: bool, default: false }
    requires_baa: { type: bool, default: false }
    requires_dpa: { type: bool, default: false }
  vendor:
    name: { type: string, required: true }
    entity_state: { type: string, required: true }
  product:
    name: { type: string, required: true }
    sku: { type: string, required: true }
  fees:
    annual_fee: { type: currency, required: true }
    currency: { type: string, default: USD }
    payment_terms: { type: enum, values: [Net 30, Net 45, Net 60], default: "Net 30" }
  term:
    initial_months: { type: int, default: 12 }
    auto_renew: { type: bool, default: true }
    non_renewal_notice_days: { type: int, default: 60 }
  liability:
    cap_multiplier: { type: float, default: 1.0 }
```

### Recipe 4: Author the conditional template (docxtpl)

```bash
# templates/msa/v2.4.0.docx — opened in Word with placeholders + Jinja2 blocks
# Inline syntax:
#   {{customer.name}}                           — merge field
#   {{effective_date|format("MMMM D, YYYY")}}   — Jinja2 filter
#   {%p if customer.requires_soc2 %}            — conditional paragraph
#   {%tr if line.included %}                    — conditional table row
#   {% for line in line_items %} ... {%endfor%} — loop over child records
```

### Recipe 5: Render against test data

```python
# pip install docxtpl
from docxtpl import DocxTemplate
import yaml

tpl = DocxTemplate("templates/msa/v2.4.0.docx")
with open("test/fixtures/acme.yaml") as f:
    ctx = yaml.safe_load(f)
tpl.render(ctx)
tpl.save(f"out/msa-{ctx['customer']['name'].lower().replace(' ','-')}-{ctx['effective_date']}.docx")
```

### Recipe 6: Convert rendered docx → PDF

```bash
# LibreOffice headless (free, server-friendly)
soffice --headless --convert-to pdf:writer_pdf_Export \
        --outdir out out/msa-acme-2026-06-15.docx

# Pandoc (markdown / docx → PDF via WeasyPrint engine)
pandoc out/msa-acme-2026-06-15.docx -o out/msa-acme.pdf --pdf-engine=weasyprint
```

### Recipe 7: Version control with semantic versioning

```bash
# Treat templates like code
git init templates/
git add templates/msa/v2.4.0.docx template_schema.yaml
git commit -m "msa: v2.4.0 — add SOC 2 addendum conditional + CA non-compete carve-out"
git tag -a v2.4.0 -m "MSA SaaS customer-side template v2.4.0"
git push origin main --tags

# PR-only changes — require legal-counsel review on clause edits
# Lint with Vale before merge:
vale --config .vale.ini templates/msa/v2.4.0.docx
```

### Recipe 8: HTML / Jinja2 source for pixel-perfect PDF

```html
<!-- templates/msa/v2.4.0.html -->
<!DOCTYPE html>
<html>
<head>
  <style>
    @page { size: letter; margin: 1in; }
    h1 { font-family: 'Helvetica'; }
  </style>
</head>
<body>
  <h1>Master Services Agreement</h1>
  <p>Effective: {{ effective_date.strftime('%B %d, %Y') }}</p>
  <p>Between <strong>{{ customer.name }}</strong>, a {{ customer.entity_state }}
     {{ customer.entity_type }}, and <strong>{{ vendor.name }}</strong>.</p>

  {% if customer.requires_soc2 %}
  <h2>Security Addendum</h2>
  <p>Vendor maintains SOC 2 Type II certification per AICPA TSP 100.</p>
  {% endif %}

  {% if customer.jurisdiction == "California" %}
  <p>Governing law: State of California.</p>
  {% elif customer.jurisdiction == "Delaware" %}
  <p>Governing law: State of Delaware.</p>
  {% else %}
  <p>Governing law: {{ customer.jurisdiction }}.</p>
  {% endif %}
</body>
</html>
```

```bash
# Render via WeasyPrint
python -c "
from jinja2 import Template
from weasyprint import HTML
ctx = {...}
html = Template(open('templates/msa/v2.4.0.html').read()).render(**ctx)
HTML(string=html).write_pdf('out/msa-acme.pdf')
"
```

### Recipe 9: Document the binding-language hand-off

Every template MUST carry a `LEGAL_REVIEW.md` next to it:

```markdown
# templates/msa/v2.4.0/LEGAL_REVIEW.md
- Base: Bonterms Cloud Terms v2.1.0 (2025-09)
- Diff vs base: added §4.3 SOC 2 addendum (conditional on `customer.requires_soc2`)
- Reviewer: Outside counsel — review date 2026-05-12
- Jurisdictions covered: US (CA, DE, NY); EU (not yet — DPA exhibit pending)
- Open issues: None
- Next review trigger: any §6 (indemnity) or §10 (LoL) edit
```

### Recipe 10: Clause library pattern (modular snippets)

```text
templates/
├── msa/
│   └── v2.4.0.docx
├── clauses/
│   ├── governing-law/
│   │   ├── ca.md           # California carve-outs
│   │   ├── de.md           # Delaware default
│   │   └── ny.md
│   ├── indemnity/
│   │   ├── mutual.md
│   │   └── one-way-vendor.md
│   └── liability-cap/
│       ├── 1x-fees.md
│       ├── 2x-fees.md
│       └── unlimited-gross-negligence-only.md
```

Template uses `{% include "clauses/governing-law/" + customer.jurisdiction_slug + ".md" %}`.

### Recipe 11: Brand lint with Vale

```ini
# .vale.ini
StylesPath = .vale/styles
MinAlertLevel = warning
[*.{md,docx}]
BasedOnStyles = Vale, Brand
```

Brand-voice rules in `.vale/styles/Brand/` enforce: no jargon, sentence case headings, oxford comma, no "very/really/just", first-person plural ("we") not third-person ("the Company"). Run on every PR via `github` MCP.

## Examples

### Example 1: SaaS MSA from Bonterms base, with conditional SOC 2 + CA carve-out

**Goal:** Author a customer-side SaaS MSA reusable across 200+ deals/year with two conditional branches.
**Steps:**
1. Recipe 2 — pull Bonterms Cloud Terms docx into `sources/bonterms/cloud-terms-v2.1.0.docx`.
2. Open in Word, save as `templates/msa/v0.1.0.docx`.
3. Add merge fields per Recipe 3 schema; conditionals per Recipe 4.
4. Render against fixture (Recipe 5); verify both branches in two test passes.
5. Convert to PDF (Recipe 6); spot-check formatting.
6. Commit + tag v0.1.0 (Recipe 7).
7. Send to `legal-counsel` for clause review.
8. Iterate based on counsel comments → v1.0.0 release.

**Result:** Versioned template + `LEGAL_REVIEW.md` + render harness.

### Example 2: Multi-party mutual NDA from Common Paper base

**Goal:** Standardize cross-party NDAs without re-drafting every time.
**Steps:**
1. Pull Common Paper Mutual NDA template.
2. Identify variables: party_a, party_b, optional party_c, purpose, term_months, residual_clause_yn.
3. Define schema; author docxtpl version supporting `{% for party in parties %}` loop.
4. Test: 2-party vs 3-party renders.
5. Hand to `legal-counsel` for sign-off.

**Result:** A single template that handles 2- and 3-party NDAs with one render call.

### Example 3: Employment offer letter with state-by-state clauses

**Goal:** Author an offer letter that auto-adjusts non-compete + at-will + arbitration to the candidate's state.
**Steps:**
1. Start from Cooley GO offer letter template.
2. Build state-clauses library (Recipe 10): CA bans non-compete; MA restricts; TX permits.
3. Schema includes `candidate.state`.
4. Template includes `{% include "clauses/non-compete/" + candidate.state + ".md" %}`.
5. Render for one candidate per region; counsel review.
6. Tag v1.0.0; deploy via HR portal smart form (`smart-form-jotform-formstack`).

**Result:** Single template covering all 50 states without manual edits.

## Edge cases / gotchas

- **Binding language is NOT this skill's deliverable.** This skill produces the source template; clause-level binding language is `legal-counsel`'s responsibility. Always emit the disclaimer + hand off.
- **docx field corruption.** Word smart-typography auto-replaces straight quotes with curly quotes inside Jinja2 tags → render errors. Disable autocorrect; or use the `<<` `>>` delimiters supported by docxtpl.
- **Conditional paragraph syntax mismatch.** `{%if%}` (inline) vs `{%p if %}` (whole paragraph) vs `{%tr if %}` (whole table row) in docxtpl — pick the right one for the surrounding element or you get orphan tags.
- **Bonterms / Common Paper licensing.** Both are CC-licensed; review the license at use time; attribute when redistributing.
- **Multilingual templates.** Don't translate boilerplate at render time. Maintain per-jurisdiction `template.en.docx`, `template.de.docx`. Only merge fields are language-agnostic. See `multilingual-template-generation`.
- **PDF vs docx output mismatch.** Word's PDF export may render differently than LibreOffice's. Standardize on one converter (LibreOffice headless or Pandoc + WeasyPrint) per pipeline.
- **Auto-renewal trap.** If template includes auto-renewal, surface it in the schema + render a renewal alert via CLM. See `clm-ironclad-contractworks-integration` Recipe 11.
- **Version drift across markets.** v2.4.0 US ≠ v2.4.0 EU. Use suffixed tags: `v2.4.0-us`, `v2.4.0-eu`.
- **Embedded images / signatures.** docxtpl handles images via `InlineImage`; SaaS engines (HotDocs / Documate) handle natively. Test image render path early.
- **No tests = silent breakage.** Run render fixtures in CI on every commit. Pin docxtpl version; new releases occasionally change tag parsing.

> **Disclaimer:** This skill builds the source artifact. The agent does not draft binding contract language. Hand off final clause review to `legal-counsel` (with consult-an-attorney disclaimer) before any executed document.

## Sources

- [Documate](https://documate.org/) — FOSS interview-driven authoring.
- [HotDocs](https://www.hotdocs.com/) — legal-industry-standard conditional logic.
- [Docassemble](https://docassemble.org/) — Python-extensible OSS engine.
- [Common Paper](https://commonpaper.com/standards/) — NDA / Cloud Service / DPA / AUP / MSA standardized base.
- [Bonterms](https://bonterms.com/) — Cloud Terms / AUP / DPA / SLA modules.
- [YC Documents](https://www.ycombinator.com/documents) — SAFE + advisor + IP assignment.
- [NVCA Model Legal Documents](https://nvca.org/resources/model-legal-documents/) — Series A canonical.
- [Cooley GO](https://www.cooleygo.com/documents/) — equity comp + employment + IP.
- [python-docx-template (docxtpl)](https://docxtpl.readthedocs.io/) — Python rendering.
- [docxtemplater](https://docxtemplater.com/) — Node rendering.
- [Pandoc Manual](https://pandoc.org/MANUAL.html) — format conversion.
- [WeasyPrint](https://weasyprint.org/) — CSS Paged Media → PDF.
- Sister skills: `conditional-logic-doc-assembly`, `template-library-templafy-brand`, `contract-redlining-automation`.
