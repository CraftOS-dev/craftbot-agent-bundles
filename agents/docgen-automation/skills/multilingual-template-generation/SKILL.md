---
name: multilingual-template-generation
description: Translate and localize contract / proposal / form templates — DeepL (legal-quality, 30+ langs), Lokalise + Crowdin (translation memory + glossary), Google / Microsoft Translator (breadth). Maintain locale-specific variants for boilerplate-heavy contracts; only translate bespoke clauses. Preserve docx / HTML formatting via `tag_handling`. Use when the user says "translate this contract", "DeepL", "Lokalise", "Crowdin", "localize template", "multi-language proposal", "DE / FR / ES / JA / ZH variants".
---

# Multilingual template generation — DeepL + Lokalise / Crowdin + locale variants

This skill ships the translation pipeline. Strategy: maintain locale-specific master variants for high-stakes boilerplate; auto-translate only the bespoke per-deal clauses.

## When to use

User says:

- "Translate this template to DE / FR / ES / JA / ZH"
- "DeepL API"
- "Lokalise / Crowdin translation memory"
- "Localize the proposal for the German market"
- "Multi-language NDA"
- "Preserve Word / HTML formatting in translation"

Companion skills:
- `template-library-templafy-brand` — locale-specific template variants in the library.
- `contract-template-authoring-msa-nda` — source of master template per locale.
- `document-accessibility-pdf-ua` — language tags on PDF.
- `l10n` adjacent sibling agent — complex multilingual workflows.

## Setup

```bash
# DeepL (legal-quality)
pip install deepl
# Required env: DEEPL_API_KEY
# Free tier: 500K chars/mo. Paid Pro: $5+/mo
# Or use deepl-mcp MCP

# Google Translate (breadth)
pip install google-cloud-translate
# Required env: GOOGLE_APPLICATION_CREDENTIALS

# Microsoft Translator (Azure)
pip install azure-ai-translation-text
# Required env: AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION

# Lokalise REST
# Required env: LOKALISE_API_TOKEN, LOKALISE_PROJECT_ID

# Crowdin REST
# Required env: CROWDIN_API_TOKEN

# Helpers
pip install python-docx lxml beautifulsoup4
```

## Common recipes

### Recipe 1: Pick the engine + workflow

| Engine / tool | Best for | Notes |
|---|---|---|
| DeepL | Legal / formal content; EU langs | Highest quality DE / FR / ES / IT / NL / PL / JA / ZH / KO |
| Google Translate | Breadth (130+ langs) | Less polished but covers long tail |
| Microsoft Translator | Microsoft shops | Strong CJK; Azure-resident |
| Amazon Translate | AWS-resident | Solid English ↔ major langs |
| Lokalise | Translation memory + glossary; team workflow | Per-string + per-key management |
| Crowdin | Localization platform for product strings | Bigger free tier |
| Smartling | Enterprise translation memory | Premium pricing |
| Phrase (formerly PhraseApp) | Devops + i18n | Strong CLI |
| Human translation marketplace | Final legal review | Use after machine pass |

Default: DeepL for legal/proposal translation. Layer Lokalise/Crowdin for translation memory across many documents.

### Recipe 2: DeepL — translate a paragraph (Python SDK)

```python
import deepl

translator = deepl.Translator(os.environ["DEEPL_API_KEY"])
text = "This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware."

result = translator.translate_text(text, target_lang="DE", formality="more")
print(result.text)
# → "Dieser Vertrag unterliegt den Gesetzen des Bundesstaates Delaware und wird nach diesen ausgelegt."
```

Common target_lang codes: `DE`, `FR`, `ES`, `IT`, `NL`, `PL`, `PT-BR`, `PT-PT`, `JA`, `ZH` (simplified), `KO`. Formality: `default` / `more` / `less` (where supported).

### Recipe 3: DeepL — translate Word docx preserving formatting

```python
result = translator.translate_document(
    "templates/msa-en.docx",
    "translated/msa-de.docx",
    target_lang="DE",
    formality="more"
)
```

DeepL's document translation preserves runs, styles, headers/footers, tables. Counts toward character quota.

### Recipe 4: DeepL — translate HTML with tag preservation

```python
html = "<p>By signing below, <strong>Customer</strong> agrees to the terms.</p>"
result = translator.translate_text(html, target_lang="FR", tag_handling="html")
print(result.text)
# → "<p>En signant ci-dessous, <strong>le Client</strong> accepte les conditions.</p>"
```

Use `tag_handling="xml"` for XML; `tag_handling="html"` for HTML. Default treats as plain text (tags get translated → broken HTML).

### Recipe 5: DeepL — preserve glossary terms

```python
# Create glossary
glossary = translator.create_glossary(
    name="WidgetCo EN-DE",
    source_lang="EN",
    target_lang="DE",
    entries={
        "WidgetCo": "WidgetCo",                  # do not translate brand
        "Premium Plan": "Premium-Plan",
        "Service Level Agreement": "Servicevereinbarung"
    }
)
result = translator.translate_text(text, target_lang="DE", glossary=glossary)
```

Glossaries persist; reference by ID in future calls.

### Recipe 6: Locale-variant strategy for contracts

```text
templates/
└── contracts/
    ├── msa-en-US.docx                # master for US
    ├── msa-en-GB.docx                # UK variant (e.g., "endeavour" not "endeavor")
    ├── msa-de-DE.docx                # Germany — locally-reviewed by counsel
    ├── msa-fr-FR.docx                # France — locally-reviewed
    ├── msa-ja-JP.docx                # Japan — locally-reviewed
    └── _bespoke_clauses_locale/
        ├── exhibit-a.docx            # per-deal exhibits; auto-translate OK
        └── exhibit-b.docx
```

Master boilerplate (LoL, governing law, IP) gets local counsel review once + cached.
Per-deal exhibits (line items, fees) get machine-translated per deal.

### Recipe 7: Per-locale legal nuance map

```python
LOCALE_RULES = {
    "de-DE": {
        "governing_law_default": "Gesetze der Bundesrepublik Deutschland",
        "venue_default": "Gerichtsstand München",
        "currency": "EUR",
        "date_format": "DD.MM.YYYY",
        "warranty_disclaimer_style": "stricter_due_to_BGB",
        "data_protection": "GDPR + BDSG"
    },
    "fr-FR": {
        "governing_law_default": "lois françaises",
        "venue_default": "Tribunaux de Paris",
        "currency": "EUR",
        "language_required": "FR mandatory under Toubon law for B2C contracts",
    },
    "ja-JP": {
        "currency": "JPY",
        "date_format": "YYYY-MM-DD",
        "seal_required_for_signing": True,    # hanko culture
    }
}
```

Hand off to `legal-counsel` for each new locale — bespoke counsel review beats machine translation for binding terms.

### Recipe 8: Lokalise — push + pull translations

```bash
# Push source keys
curl -X POST https://api.lokalise.com/api2/projects/$PROJECT_ID/keys \
  -H "X-Api-Token: $LOKALISE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "keys": [
      {"key_name":"msa.lol.cap","platforms":["other"],
       "translations":[{"language_iso":"en","translation":"Vendor liability cap: 12 months fees paid."}]}
    ]
  }'

# Pull translated keys
curl https://api.lokalise.com/api2/projects/$PROJECT_ID/files/download \
  -H "X-Api-Token: $LOKALISE_API_TOKEN" \
  -d 'format=json&original_filenames=false'
```

Lokalise also exposes machine pre-translation + human review workflows.

### Recipe 9: Crowdin — string-by-string upload

```bash
# Upload a source file
curl -X POST https://api.crowdin.com/api/v2/projects/$PROJECT_ID/files \
  -H "Authorization: Bearer $CROWDIN_API_TOKEN" \
  -F "file=@en-strings.json" \
  -F "name=msa-strings.json"
```

Crowdin supports machine pre-translation + human review.

### Recipe 10: docx + glossary + locale variant pipeline

```python
def localize_doc(src_path, target_lang, glossary_id, output_dir):
    translator = deepl.Translator(os.environ["DEEPL_API_KEY"])
    out_path = f"{output_dir}/{Path(src_path).stem}-{target_lang.lower()}.docx"
    translator.translate_document(
        src_path,
        out_path,
        target_lang=target_lang,
        formality="more",
        glossary=glossary_id
    )
    return out_path

# Bulk localize all bespoke exhibits
for lang in ("DE", "FR", "ES", "JA"):
    for exhibit in Path("templates/contracts/_bespoke_clauses_locale/").glob("*.docx"):
        localize_doc(str(exhibit), lang, glossary_id=GLOSSARIES[lang], output_dir=f"dist/{lang}")
```

### Recipe 11: Quality assurance — back-translation spot check

```python
de = translator.translate_text("This Agreement is governed by Delaware law.", target_lang="DE")
en_back = translator.translate_text(de.text, target_lang="EN-US")
print(en_back.text)
# Sanity-check: should match original meaning.
```

Use sparingly; back-translation isn't a perfect quality signal but flags egregious shifts.

### Recipe 12: Currency + date format per locale

```python
import babel.numbers, babel.dates
from datetime import datetime
amount, due = 24000, datetime(2026, 6, 15)
for loc in ("en_US","de_DE","fr_FR","ja_JP"):
    print(loc, babel.numbers.format_currency(amount, "USD", locale=loc))
    print(loc, babel.dates.format_date(due, format="long", locale=loc))
```

Localize numbers + dates separately from text translation.

### Recipe 13: Tagging language at PDF level

```python
import pikepdf
pdf = pikepdf.open("msa-de.pdf", allow_overwriting_input=True)
pdf.Root.Lang = pikepdf.String("de-DE")
pdf.save("msa-de-tagged.pdf")
```

Required for PDF/UA + screen readers per language (`document-accessibility-pdf-ua`).

### Recipe 14: Mixed-language docs (bilingual contracts)

```python
# Side-by-side EN | DE table layout via python-docx
from docx import Document
from docx.shared import Inches
doc = Document()
table = doc.add_table(rows=1, cols=2)
table.rows[0].cells[0].text = en_clause
table.rows[0].cells[1].text = de_clause
doc.save("msa-bilingual.docx")
```

Common in international M&A + cross-border financing.

## Examples

### Example 1: German distributor agreement — locally-reviewed master + per-deal exhibits

**Goal:** Sales to German distributors; legal-quality DE contract.
**Steps:**
1. Recipe 6 — `msa-de-DE.docx` master one-time-reviewed by German counsel.
2. Per deal: Recipe 10 translates bespoke Exhibit A (line items) via DeepL + glossary.
3. Recipe 12 — currency/date localized.
4. Recipe 13 — Lang tag on PDF.
5. `legal-counsel` (DE) approves once per master version.

**Result:** Compliant German contracts without per-deal legal review.

### Example 2: JP / KR / ZH market entry — three-locale set

**Goal:** Same SaaS product enters 3 Asian markets.
**Steps:**
1. Recipe 5 — per-locale glossary with brand + product names.
2. Recipe 6 — three master MSAs; Japan with hanko notes (Recipe 7).
3. Recipe 11 — back-translation spot check on critical clauses.
4. Local counsel review each → finalize.

**Result:** Tri-locale go-to-market with culturally appropriate contracts.

### Example 3: Marketing collateral batch translate via Lokalise

**Goal:** 30 product brochures into 8 languages.
**Steps:**
1. Recipe 9 — upload to Lokalise as source.
2. Lokalise machine pre-translate via DeepL.
3. In-country reviewers polish in Lokalise UI.
4. Pull via Recipe 8 → render via `bulk-document-gen-csv`.

**Result:** 240 localized brochures from 30 source files.

## Edge cases / gotchas

- **Machine translation is NOT a substitute for legal review.** Always hand binding contract translation off to local counsel before signing.
- **Toubon Law (France).** B2C contracts in France must be in French. EN-only invalidates the contract.
- **EU Consumer Rights Directive.** Local language consumer contracts often required.
- **CJK character expansion.** Translated text length can change ±30%; design layouts to flex.
- **RTL languages (Arabic, Hebrew).** Word + WeasyPrint support RTL — set para alignment + bidi direction.
- **Numeral systems.** Arabic uses Eastern Arabic numerals by default; Japanese may use full-width.
- **Date order varies by locale.** ISO-8601 internally; format at render only.
- **Hanko / chop / seal in JP / CN / KR / TW.** Physical seal required for legal effect in some contexts — discuss with local counsel.
- **DeepL quota.** Free tier 500K chars/mo; Pro tier billed per character. Watch usage on doc-mode (whole file counts).
- **DeepL `formality`.** Available for DE / FR / ES / IT / NL / PL / PT / RU; not for EN / JA / ZH / KO.
- **Glossary entries are case-sensitive.** "WidgetCo" ≠ "widgetco" in match.
- **HTML tag preservation.** `tag_handling="html"` recommended; failing to set this breaks structured docs.
- **docx tracked changes.** DeepL document mode strips tracked changes; finalize before translating.
- **Embedded images with text.** Not translated by any engine; replace at source.
- **OCR'd PDFs.** Translate poorly; re-author from text source if possible.
- **Variable substitution (Jinja `{{ }}`).** Translator may break tokens; pre-process to placeholders + restore post.
- **Right-to-left mixing with LTR (e.g., AR + EN brand).** Unicode bidi controls + careful design.
- **Numeric format (decimal/thousand separator) in pricing tables.** Use Babel (Recipe 12), never f-strings.
- **Compliance docs (e.g., GDPR privacy policy).** Multi-jurisdiction nuance; defer to `compliance-agent` / `legal-counsel` sibling.

## Sources

- [DeepL Translate API](https://developers.deepl.com/docs/api-reference/translate) — REST + SDK + glossary + document.
- [DeepL Python SDK](https://github.com/DeepLcom/deepl-python) — official.
- [Google Cloud Translate](https://cloud.google.com/translate/docs) — Translation API v3.
- [Microsoft Azure AI Translator](https://learn.microsoft.com/en-us/azure/ai-services/translator/) — Azure-native.
- [Amazon Translate](https://docs.aws.amazon.com/translate/) — AWS-native.
- [Lokalise API](https://developers.lokalise.com/reference/lokalise-rest-api) — keys + files + projects.
- [Crowdin API](https://developer.crowdin.com/api/v2/) — file + string + machine translation.
- [Smartling docs](https://help.smartling.com/) — enterprise alt.
- [Phrase docs](https://developers.phrase.com/) — i18n CLI + API.
- [Babel](https://babel.pocoo.org/en/latest/) — locale-aware number + date formatting.
- [pikepdf — Lang tag](https://pikepdf.readthedocs.io/) — PDF language metadata.
- Sister skills: `template-library-templafy-brand`, `contract-template-authoring-msa-nda`, `document-accessibility-pdf-ua`, `l10n` (sibling agent).
