---
name: conditional-logic-doc-assembly
description: Execute conditional doc assembly via Documate (FOSS / hosted), HotDocs (legal-industry standard), and Docassemble (Python-extensible OSS) interview engines. If-then clause insertion driven by interview answers — jurisdiction-specific clauses, product-mix appendices, customer-tier SLA, regulatory overlays (HIPAA BAA, GDPR DPA). Use when the user says "interview-driven doc gen", "Documate / HotDocs / Docassemble", "if-then clause logic", "doc assembly engine", "self-serve doc builder".
---

# Conditional logic doc assembly — Documate / HotDocs / Docassemble

This skill executes the rendering engine. The source templates come from `contract-template-authoring-msa-nda` or `template-library-templafy-brand`; this skill turns the interview answers into a finished doc.

## When to use

User says:

- "Documate / HotDocs / Docassemble"
- "Interview-driven document"
- "If-then clause logic"
- "Conditional sections in template"
- "Doc assembly engine"
- "Self-serve doc builder for [contract / form]"
- "Jurisdiction-specific clauses"
- "Customer-tier SLA terms"

Companion skills:
- `contract-template-authoring-msa-nda` — authors the conditional template.
- `smart-form-jotform-formstack` — alternative front-end for collecting interview data.
- `bulk-document-gen-csv` — for batch (non-interview) rendering of the same conditional template.

## Setup

```bash
# Docassemble (FOSS) — Python-extensible interview engine
docker pull jhpyle/docassemble
docker run -d -p 80:80 --name docassemble jhpyle/docassemble
# https://docassemble.org/  — full self-host

# Documate — hosted SaaS or self-host (FOSS core)
# https://documate.org/
# REST API on hosted tier

# HotDocs — legal industry standard (paid)
# https://www.hotdocs.com/
# HotDocs Cloud Services (HDCS) REST API

# python-docx-template — code-first conditional rendering
pip install docxtpl jinja2

# Jinja2 + WeasyPrint for HTML source
pip install jinja2 weasyprint
```

Auth / API keys:
- `HOTDOCS_CLIENT_ID` + `HOTDOCS_CLIENT_SECRET` — HotDocs Cloud Services OAuth.
- `DOCUMATE_API_KEY` — Documate hosted tenant token.
- Docassemble — username/password admin auth; API tokens issued per user.

## Common recipes

### Recipe 1: Pick the engine

| Engine | Best for | License | Trigger |
|---|---|---|---|
| Docassemble | self-host, full Python rules | OSS (MIT) | "self-host", "custom Python logic", "no per-user fees" |
| Documate | hosted, lawyer-friendly UI | FOSS / hosted | "lawyer-built interviews", "FOSS-with-cloud option" |
| HotDocs | enterprise legal | Paid | "Big Law shop", "existing HotDocs investment" |
| python-docx-template | code-first dev orgs | OSS | "render in CI", "no interview UI" |
| Jinja2 + WeasyPrint | HTML source → PDF | OSS | "pixel-perfect PDF", "marketing-collateral-style render" |

### Recipe 2: Docassemble — write an interview YAML

```yaml
# interviews/msa.yml
metadata:
  title: SaaS MSA Builder
  short title: MSA
---
mandatory: True
question: |
  Welcome to the SaaS MSA Builder.
  This interview produces a draft MSA for review by your counsel.
subquestion: |
  This is NOT legal advice. Output requires attorney review before execution.
field: confirmed
---
mandatory: True
question: Customer information
fields:
  - Customer legal name: customer_name
  - Customer state of incorporation: customer_state
    code: |
      [{'value': s, 'label': s} for s in ['Delaware', 'California', 'New York', 'Other']]
  - Customer entity type: customer_entity
    choices: [C-corp, LLC, S-corp, LP, Other]
  - Annual fee (USD): annual_fee
    datatype: currency
  - Requires SOC 2 addendum: requires_soc2
    datatype: yesno
  - Requires HIPAA BAA: requires_baa
    datatype: yesno
---
mandatory: True
question: Final review
subquestion: |
  Generating MSA for ${customer_name}.
field: ready
---
mandatory: True
attachment:
  name: MSA-${customer_name}
  filename: msa-${customer_name|lower|replace(' ', '-')}
  docx template file: templates/msa-v2.4.0.docx
```

```bash
# Upload + run via Docassemble admin UI or API:
curl -X POST "$DA_URL/api/secrets" \
  -H "X-API-Key: $DA_TOKEN" \
  -d "github_user_token=..."   # for git-backed playgrounds

curl -X POST "$DA_URL/api/session/new?i=docassemble.demo:msa.yml" \
  -H "X-API-Key: $DA_TOKEN"
# Returns session id; subsequent calls walk the interview
```

### Recipe 3: Docassemble — embed Python rules

```yaml
# interviews/employment.yml
---
code: |
  if state == 'California':
    has_non_compete = False
    non_compete_clause = ""
  elif state == 'Massachusetts':
    has_non_compete = True
    non_compete_clause = (
      "12-month non-compete with mandatory garden-leave payment per "
      "M.G.L. c. 149, § 24L."
    )
  else:
    has_non_compete = True
    non_compete_clause = "12-month non-compete in the U.S."
---
```

### Recipe 4: HotDocs — author template + invoke via HDCS

```html
<!-- HotDocs template authored in HotDocs Author (Windows) -->
<!-- Variables: «CUSTOMER NAME», «EFFECTIVE DATE», «JURISDICTION» -->
<!-- Conditional: «IF JURISDICTION = "CA"»...«END IF» -->

<!-- Invoke render via HotDocs Cloud Services -->
```

```bash
# HotDocs Cloud Services REST — assemble document
curl -X POST "https://cloud.hotdocs.com/hdcs/files/<template-package-id>/assemble" \
  -H "Authorization: HMAC-SHA1 $HOTDOCS_HMAC" \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0"?>
  <AnswerSet>
    <Answer name="CUSTOMER NAME"><TextValue>Acme Corp</TextValue></Answer>
    <Answer name="EFFECTIVE DATE"><DateValue>2026-06-15</DateValue></Answer>
    <Answer name="JURISDICTION"><TextValue>CA</TextValue></Answer>
  </AnswerSet>'
# Returns assembled docx
```

### Recipe 5: Documate — render via REST

```bash
# Documate hosted API
curl -X POST "https://app.documate.org/api/v1/templates/<template_id>/render" \
  -H "Authorization: Bearer $DOCUMATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "answers": {
      "customer_name": "Acme Corp",
      "effective_date": "2026-06-15",
      "jurisdiction": "California",
      "annual_fee": 120000,
      "requires_soc2": true
    },
    "output_format": "docx"
  }' \
  -o output.docx
```

### Recipe 6: docxtpl — code-first conditional render

```python
# pip install docxtpl
from docxtpl import DocxTemplate

tpl = DocxTemplate("templates/msa-v2.4.0.docx")
ctx = {
    "customer": {
        "name": "Acme Corp",
        "entity_state": "Delaware",
        "entity_type": "C-corp",
        "jurisdiction": "California",
        "requires_soc2": True,
        "requires_baa": False,
    },
    "vendor": {"name": "WidgetCo Inc", "entity_state": "Delaware"},
    "effective_date": "2026-06-15",
    "annual_fee": 120000,
}
tpl.render(ctx)
tpl.save("out/msa-acme-2026-06-15.docx")
```

In the template, conditional clauses use Jinja2:
```
{%p if customer.requires_soc2 %}
2. SECURITY ADDENDUM
   This Agreement incorporates the SOC 2 Security Addendum (Exhibit B).
{%p endif %}

{% if customer.jurisdiction == "California" %}
Governing law: California.
{% elif customer.jurisdiction == "Delaware" %}
Governing law: Delaware.
{% else %}
Governing law: {{customer.jurisdiction}}.
{% endif %}
```

### Recipe 7: Audit trail — which branches fired

```python
# Capture branch decisions for audit
import json
branches_fired = {
    "soc2_addendum": ctx["customer"]["requires_soc2"],
    "baa_addendum": ctx["customer"]["requires_baa"],
    "jurisdiction_clause": ctx["customer"]["jurisdiction"],
    "non_compete_carve_out": ctx["customer"]["jurisdiction"] == "California",
}
with open("out/msa-acme-audit.json", "w") as f:
    json.dump({"template_version": "v2.4.0", "branches": branches_fired, "rendered_at": "2026-06-15T10:00:00Z"}, f, indent=2)
```

### Recipe 8: Test matrix — every branch combination

```python
# Generate all combinations of bool flags + jurisdictions
import itertools
flags = ["requires_soc2", "requires_baa", "requires_dpa"]
jurisdictions = ["California", "Delaware", "New York", "EU"]
for combo in itertools.product([True, False], repeat=len(flags)):
    for j in jurisdictions:
        ctx = base_ctx.copy()
        for k, v in zip(flags, combo):
            ctx["customer"][k] = v
        ctx["customer"]["jurisdiction"] = j
        tpl = DocxTemplate("templates/msa-v2.4.0.docx")
        tpl.render(ctx)
        suffix = "-".join(f"{k}={v}" for k, v in zip(flags, combo)) + f"-{j}"
        tpl.save(f"out/test/msa-{suffix}.docx")
```

### Recipe 9: Smart-form trigger → docassemble interview

```python
# Jotform/Typeform webhook → start a docassemble session pre-populated with form data
import httpx
async def on_form_submit(submission):
    # Map form fields to interview variables
    answers = {
        "customer_name": submission["q3_name"],
        "customer_state": submission["q5_state"],
        "annual_fee": submission["q7_fee"],
    }
    async with httpx.AsyncClient() as c:
        r = await c.post(f"{DA_URL}/api/session/new",
                         params={"i": "docassemble.demo:msa.yml"},
                         json={"variables": answers},
                         headers={"X-API-Key": DA_TOKEN})
    return r.json()["session"]
```

### Recipe 10: Docassemble — generate multiple outputs from one interview

```yaml
# Docassemble supports multi-format attachment
attachment:
  name: MSA Bundle
  variable name: docs
  attachments:
    - name: MSA
      filename: msa
      docx template file: templates/msa.docx
      valid formats: [docx, pdf]
    - name: Order Form
      filename: order-form
      docx template file: templates/order-form.docx
      valid formats: [docx, pdf]
    - name: SOC 2 Addendum
      filename: soc2-addendum
      docx template file: templates/soc2-addendum.docx
      valid formats: [docx, pdf]
      condition: requires_soc2
```

### Recipe 11: Versioning the interview + template together

```text
interviews/
├── msa/
│   ├── v2.4.0/
│   │   ├── interview.yml
│   │   ├── template.docx
│   │   └── CHANGELOG.md
│   └── v2.5.0/
│       └── ...
```

Each version is independently runnable; CRM points at `latest` or pinned version.

## Examples

### Example 1: Lawyer-built MSA interview via Docassemble

**Goal:** In-house counsel maintains a self-serve MSA interview for sales reps.
**Steps:**
1. Recipe 2 — author interview.yml.
2. Recipe 3 — embed Python rules for state-specific clauses.
3. Upload to Docassemble server (Docker self-host).
4. Author + version template (`contract-template-authoring-msa-nda`).
5. Recipe 8 — generate test matrix; counsel reviews each branch.
6. Recipe 10 — bundle MSA + Order Form + SOC 2 Addendum.
7. Deploy URL to reps; rep walks interview → downloads docx bundle → routes to e-sign.

**Result:** Reps generate first-draft MSAs in 10 min without paging counsel.

### Example 2: HotDocs migration — modernize legacy templates

**Goal:** Org has 30+ HotDocs templates; want to expose them via API.
**Steps:**
1. Inventory templates in HotDocs Author.
2. Migrate to HotDocs Cloud Services (HDCS) — upload template packages.
3. Recipe 4 — invoke `/assemble` REST endpoint per template.
4. Build a thin orchestration layer that maps internal IDs → HDCS template IDs.
5. Sunset HotDocs Server.

**Result:** Legacy HotDocs templates available via REST.

### Example 3: Code-first conditional render — 200 employment offer letters

**Goal:** HR runs an offer batch for 200 new hires across 12 states.
**Steps:**
1. Use docxtpl + per-state clause library.
2. Recipe 8 — test matrix per state.
3. Bulk render via `bulk-document-gen-csv` (sister skill).
4. Each offer → e-sign envelope (`e-signature-docusign-adobe-sign-pandadoc`).

**Result:** 200 personalized offers shipped in <1 hour.

## Edge cases / gotchas

- **Docassemble Python rules and YAML order matter.** Variables must be defined before use; use `code:` blocks to set derived variables; mandatory blocks fire top-to-bottom.
- **HotDocs HMAC auth.** HDCS uses HMAC-SHA1 signature over request canonical string + timestamp; if clock drifts >5 min, requests fail with 401.
- **docxtpl tag-corruption.** Word smart-typography breaks `{{` / `}}` if autocorrect introduces curly quotes — disable in template author's Word settings, or use `[[` / `]]` delimiters in docxtpl.
- **`{%p if%}` vs `{% if %}` — paragraph vs inline.** Wrong choice leaves orphan paragraph marks.
- **Table-row conditionals require `{%tr if%}`** — `{% if %}` in a table cell leaves blank rows.
- **Loop indices in tables — use `{%tr for %}`** for each iteration to spawn a row.
- **Docassemble GPU/load.** Heavy interviews + many concurrent users → tune the gunicorn worker count.
- **HotDocs templates aren't `.docx`.** Author file is `.cmp` (component file); render output is docx. Don't try to open `.cmp` in Word.
- **Documate is FOSS but the hosted tier costs.** Self-host is free; managed adds team mgmt + storage.
- **Conditional clauses can leave orphan whitespace.** Use `{%-` and `-%}` in Jinja2 to strip whitespace; in docxtpl use `{%p if %}` (paragraph delete).
- **Audit trail is mandatory for legal docs.** Always capture which branches fired (Recipe 7); store next to the rendered doc.
- **No interview UI = code-only renders.** docxtpl + Python is fine for batch; for self-serve, you need Docassemble / Documate / HotDocs front end or a smart-form (`smart-form-jotform-formstack`).
- **Locale formatting.** Docassemble uses Babel for currency / dates; HotDocs has built-in locale; docxtpl needs explicit formatting (`{{ amount|format_currency('USD', 'en_US') }}`).
- **Image insertion via docxtpl.** Use `InlineImage(tpl, "logo.png", width=Mm(40))` — passing a path string renders the path text, not the image.

## Sources

- [Docassemble](https://docassemble.org/) — OSS interview engine.
- [Docassemble docs](https://docassemble.org/docs.html) — full reference.
- [Documate](https://documate.org/) — FOSS-with-cloud doc automation.
- [HotDocs](https://www.hotdocs.com/) — legal-industry standard.
- [HotDocs Cloud Services](https://www.hotdocs.com/products/hotdocs-cloud-services/) — REST API.
- [python-docx-template (docxtpl)](https://docxtpl.readthedocs.io/) — Jinja2-in-docx rendering.
- [Jinja2](https://jinja.palletsprojects.com/) — template syntax.
- Sister skills: `contract-template-authoring-msa-nda`, `smart-form-jotform-formstack`, `bulk-document-gen-csv`.
