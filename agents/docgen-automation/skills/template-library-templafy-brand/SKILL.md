---
name: template-library-templafy-brand
description: Build and govern an enterprise template library across Word / PowerPoint / Excel / Outlook with brand-asset injection and consistency lint. Templafy is the enterprise tool; for SMB / FOSS, layer python-docx + python-pptx + docxtemplater + Vale + Brandfolder asset reference. Use when the user says "templafy", "brand templates", "template library", "brand consistency", "logo / color / font enforcement", "Word/PPT/Excel templates", "Brandfolder / Frontify".
---

# Template library + brand consistency — Templafy / docx / pptx / Vale

This skill ships the enterprise + SMB versions of "branded template at the point of authoring." For per-doc template authoring (legal MSA, NDA), use `contract-template-authoring-msa-nda`. For batch generation, use `bulk-document-gen-csv`. For multilingual variants, use `multilingual-template-generation`.

## When to use

User says:

- "Centralize our Word / PowerPoint / Excel templates"
- "Templafy / Brandfolder / Frontify"
- "Inject the logo / brand colors / fonts automatically"
- "Brand-compliance lint on docs"
- "Auto-update templates on rebrand"
- "Version control on the template library"
- "Stop reps using off-brand decks"

Companion skills:
- `contract-template-authoring-msa-nda` — single-doc legal templates.
- `bulk-document-gen-csv` — batch CSV → docs.
- `multilingual-template-generation` — locale-specific template variants.
- `document-accessibility-pdf-ua` — tagged PDF + accessibility on export.

## Setup

```bash
# Templafy (enterprise — Office 365 + REST API + add-in)
# No SDK install needed; admin-driven setup at https://www.templafy.com/
# Required env: TEMPLAFY_TENANT, TEMPLAFY_CLIENT_ID, TEMPLAFY_CLIENT_SECRET

# python-docx (FOSS — Word manipulation)
pip install python-docx

# python-pptx (FOSS — PowerPoint manipulation)
pip install python-pptx

# docxtemplater (Node — Jinja-style Word templating)
npm install docxtemplater pizzip
# Modules:
npm install docxtemplater-image-module-free docxtemplater-html-module

# python-docx-template (docxtpl) — Python equivalent
pip install docxtpl

# Vale (FOSS — brand voice lint)
brew install vale
# or download: https://github.com/errata-ai/vale/releases

# Brandfolder API (FOSS access tier)
# Required env: BRANDFOLDER_API_KEY
```

## Common recipes

### Recipe 1: Decide tier — Templafy vs FOSS

| Tier | Tools | Best for | Cost (approx 2026) |
|---|---|---|---|
| Enterprise | Templafy + Brandfolder + Acrolinx | 500+ employees, multi-brand | $30-60/user/mo + brand-asset tier |
| Mid-market | Templafy alone OR docxtemplater + Frontify | 50-500 employees | $20-30/user/mo |
| SMB / startup | python-docx + python-pptx + Vale + Git template repo | <50 employees | Free + dev time |

Default for v1 deployments: ship FOSS stack first; recommend Templafy if user has 200+ seats or multi-brand needs.

### Recipe 2: Template repo layout (Git-backed, source-of-truth)

```text
templates/
├── README.md                  # contributor + lint rules
├── .vale.ini                  # brand voice lint config
├── brand.yaml                 # logo path, hex colors, font family, tagline
├── word/
│   ├── msa.docx
│   ├── nda.docx
│   ├── sow.docx
│   └── _styles.docx           # source for shared Word styles
├── powerpoint/
│   ├── client-pitch.pptx
│   └── _theme.thmx            # PowerPoint theme file
├── excel/
│   ├── proposal-pricing.xlsx
│   └── account-plan.xlsx
├── outlook/                   # email signatures (.htm)
│   └── signature.htm
└── tests/
    └── lint_brand.py          # runs in CI
```

Tag releases (`v3.1.0`) on the repo; CI runs `lint_brand.py` + Vale + visual diff on every PR.

### Recipe 3: brand.yaml (single-source-of-truth for tokens)

```yaml
brand:
  name: Widget Co
  logo:
    primary_path: assets/widgetco-mark.svg
    secondary_path: assets/widgetco-wordmark.svg
  colors:
    primary: "#1A73E8"
    secondary: "#FBBC05"
    text: "#202124"
    background: "#FFFFFF"
  typography:
    heading: "Inter"
    body: "Inter"
    monospace: "JetBrains Mono"
  voice:
    tone: "confident, helpful, plain-English"
    forbidden:
      - "synergize"
      - "leverage"      # use "use"
      - "actionable insights"
```

### Recipe 4: python-docx — inject brand colors + heading style

```python
from docx import Document
from docx.shared import RGBColor, Pt

doc = Document("templates/word/msa.docx")

# Update Heading 1 style to brand primary color
styles = doc.styles
h1 = styles["Heading 1"]
h1.font.color.rgb = RGBColor.from_string("1A73E8")
h1.font.name = "Inter"
h1.font.size = Pt(20)

# Insert brand logo in header
header = doc.sections[0].header.paragraphs[0]
run = header.add_run()
run.add_picture("assets/widgetco-mark.svg", width=Pt(120))

doc.save("dist/msa-branded.docx")
```

### Recipe 5: docxtemplater — token replacement (Node)

```javascript
const PizZip = require("pizzip");
const Docxtemplater = require("docxtemplater");
const fs = require("fs");

const content = fs.readFileSync("templates/word/msa.docx", "binary");
const zip = new PizZip(content);
const doc = new Docxtemplater(zip, { paragraphLoop: true, linebreaks: true });

doc.render({
  customer_name: "Acme Corp",
  customer_state: "Delaware",
  msa_date: "2026-06-15",
  fees_total: "$240,000",
  is_enterprise: true,        // gates a conditional clause
});

fs.writeFileSync("dist/msa-acme.docx", doc.getZip().generate({ type: "nodebuffer" }));
```

Inside the docx, use `{customer_name}`, `{#is_enterprise}...{/is_enterprise}` conditional blocks.

### Recipe 6: python-pptx — apply brand theme to a deck

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

prs = Presentation("templates/powerpoint/client-pitch.pptx")

for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    run.font.name = "Inter"
                    if "Heading" in (shape.name or ""):
                        run.font.color.rgb = RGBColor(0x1A, 0x73, 0xE8)

# Inject logo on every slide master
master = prs.slide_masters[0]
master.shapes.add_picture("assets/widgetco-mark.svg",
                          Inches(0.3), Inches(0.3), width=Inches(1.2))

prs.save("dist/pitch-rebranded.pptx")
```

### Recipe 7: Templafy — upload a template via REST

```bash
curl -X POST https://$TENANT.templafy.com/api/v2/templates \
  -H "Authorization: Bearer $TEMPLAFY_TOKEN" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@msa.docx" \
  -F "name=MSA — Customer" \
  -F "category=contracts/msa" \
  -F "tags=msa,contract,customer"
```

Templafy then surfaces this template inside Word/PPT via the Office add-in.

### Recipe 8: Templafy — fetch brand assets at render time

```bash
curl https://$TENANT.templafy.com/api/v2/library/assets?type=logo \
  -H "Authorization: Bearer $TEMPLAFY_TOKEN"
```

Returns CDN URLs for logos / images / banners. Use these in `{%img logo_primary %}` tags inside the template.

### Recipe 9: Brand voice lint with Vale

Create `.vale.ini`:

```ini
StylesPath = styles
MinAlertLevel = suggestion
Vocab = WidgetCo

[*.{md,html,docx}]
BasedOnStyles = WidgetCo
```

Create `styles/WidgetCo/Forbidden.yml`:

```yaml
extends: existence
message: "Avoid '%s' (per brand voice guide)"
ignorecase: true
level: error
tokens:
  - synergize
  - leverage
  - actionable insights
  - circle back
```

Run: `vale templates/` → CI fails PR if forbidden tokens found.

### Recipe 10: GitHub Actions workflow for template repo CI

```yaml
name: Template Repo CI
on: pull_request
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: errata-ai/vale-action@reviewdog
        with: { files: "templates/" }
      - run: pip install python-docx
      - run: python tests/lint_brand.py
      - name: Visual diff via LibreOffice → PNG
        run: |
          soffice --headless --convert-to png templates/word/*.docx
          # diff against last release PNGs via imagemagick compare
```

### Recipe 11: Brandfolder — fetch the latest logo at template build

```bash
curl https://api.brandfolder.com/v4/brandfolders/$BF_ID/assets?include=attachments \
  -H "Authorization: Bearer $BRANDFOLDER_API_KEY"
```

Pull the asset by name/tag, cache locally, embed into the template.

### Recipe 12: Auto-rebrand on color change (mass update)

```python
# When brand.yaml changes, re-render every template with new tokens
import yaml, subprocess
from docx import Document
from docx.shared import RGBColor

brand = yaml.safe_load(open("brand.yaml"))
for tmpl in Path("templates/word").glob("*.docx"):
    doc = Document(tmpl)
    for style_name in ("Heading 1", "Heading 2"):
        doc.styles[style_name].font.color.rgb = (
            RGBColor.from_string(brand["brand"]["colors"]["primary"].lstrip("#"))
        )
    doc.save(f"dist/rebranded/{tmpl.name}")
subprocess.run(["git", "add", "dist/rebranded/"])
```

## Examples

### Example 1: SMB rebrand sprint — Git + python-docx, no Templafy

**Goal:** 20-person startup with 30 Word/PPT templates needs a global rebrand in 2 days.
**Steps:**
1. Create repo `templates/` with layout from Recipe 2.
2. Author `brand.yaml` (Recipe 3) with new tokens.
3. Run Recipe 12 batch script.
4. Open 3-5 representative templates for visual QA.
5. Tag `v2.0.0`, ship; reps re-download from repo.

**Result:** Full rebrand in days for $0 software cost.

### Example 2: Enterprise — Templafy + Brandfolder

**Goal:** 1500-employee org keeps decks on-brand without policing every rep.
**Steps:**
1. Brandfolder holds master assets (Recipe 11).
2. Templafy templates reference Brandfolder asset IDs (Recipe 7, 8).
3. PowerPoint Templafy add-in injects brand on every new file.
4. PR workflow (Recipe 10) reviews template changes before publish.

**Result:** Every new doc is on-brand by default; no manual policing.

### Example 3: Brand voice lint in PR review

**Goal:** Marketing copy in templates auto-checked for tone before merge.
**Steps:**
1. Vale config from Recipe 9.
2. GitHub Action runs on PR (Recipe 10).
3. Reviewdog posts inline PR comments for each violation.

**Result:** Forbidden jargon never reaches the published template library.

## Edge cases / gotchas

- **Word style precedence.** Direct character formatting overrides paragraph style — when re-skinning, also strip direct formatting (`run.font.color = None`) or styles won't apply.
- **PowerPoint theme.thmx is fragile.** Rebuilding decks via python-pptx loses the theme. Better: apply the .thmx in PowerPoint manually, then ship the .pptx with theme baked in.
- **Office 365 Cloud Policy.** Templafy works best when admin sets the corporate template gallery via Cloud Policy; otherwise reps can ignore it.
- **Vale only sees text content.** Pure-image marketing slides bypass Vale; pair with image-OCR check for those.
- **SVG logos in Word.** Word 2016+ supports SVG natively; older versions need PNG fallback. Always ship both.
- **Outlook signature deployment.** Email signatures need either a deployment tool (Templafy Email Signatures, Exclaimer, CodeTwo) or GPO push — manual install never sticks.
- **Multi-brand orgs (M&A).** Each acquired entity may need its own template gallery; Templafy supports this via "Spaces" — design the structure up front.
- **Locale-specific templates.** Don't keep one template with switched text — `multilingual-template-generation` ships proper locale variants.
- **Brand asset CDN URLs expire.** Cache locally during template build; don't bake CDN URLs that expire into committed templates.
- **Git LFS for large assets.** PSDs, .ai, large .ppt with embedded media — use Git LFS.
- **Conflicting style sources.** Templafy's brand may conflict with org's Group Policy or with a vendor template the rep pasted in. Lint catches this.
- **Embedded fonts in PDF export.** Word's "Embed fonts in the file" preserves brand fonts in PDFs; without it, recipient sees fallback.
- **Acrolinx vs Vale.** Acrolinx is enterprise + ML; Vale is rule-based + free. Vale handles 80% of orgs.

## Sources

- [Templafy product](https://www.templafy.com/) + [REST API](https://api.templafy.com/) — enterprise template library.
- [python-docx](https://python-docx.readthedocs.io/) — Word manipulation in Python.
- [python-pptx](https://python-pptx.readthedocs.io/) — PowerPoint manipulation.
- [docxtemplater](https://docxtemplater.com/) — Jinja-style Word templating in Node.
- [docxtpl](https://docxtpl.readthedocs.io/) — Jinja-style in Python.
- [Vale](https://vale.sh/) — open-source prose linter.
- [Vale Action for GitHub](https://github.com/errata-ai/vale-action) — CI integration.
- [Brandfolder API](https://developers.brandfolder.com/) — brand asset library.
- [Frontify](https://www.frontify.com/) — brand guideline + asset platform.
- [Acrolinx](https://www.acrolinx.com/) — enterprise tone + brand voice.
- Sister skills: `contract-template-authoring-msa-nda`, `bulk-document-gen-csv`, `multilingual-template-generation`.
