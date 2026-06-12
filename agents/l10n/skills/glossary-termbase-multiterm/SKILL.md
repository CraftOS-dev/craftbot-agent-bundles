---
name: glossary-termbase-multiterm
description: Termbase + glossary management — MultiTerm (Trados), TBX interchange, IATE bulk import, per-domain glossaries with forbidden terms. Use when the user asks "manage our glossary", "import IATE", "termbase for legal", or needs term-consistency enforcement across translators.
---

# Glossary & Termbase Management (MultiTerm + TBX + IATE)

Terminology consistency is the second-largest quality lever after TM. A wrong brand term ("login" vs "sign in"), a missed forbidden term, or a switched legal-domain term ("consumer" vs "customer") shows up as obvious quality failure. Termbases are owned across all translators; glossaries are project-scoped.

## When to use

- The user is starting a new product → seed a brand termbase.
- The user is shipping legal/regulatory → seed from IATE (EU termbase).
- The user wants forbidden-term enforcement (e.g., never translate "API", "SDK").
- The user has Trados `.sdltb` files and wants to use them in memoQ/Phrase.
- The user has a CSV glossary that needs to become TBX.

Trigger phrases: "termbase", "glossary", "MultiTerm", "TBX", "IATE", "forbidden term", "DNT" (do not translate), "term consistency".

## Setup

```bash
# Okapi tools for TBX read/write
pipx install okapi-tools                 # provides tikal

# TBX validation
pip install lxml

# IATE API — no install (REST)

# tbx-tools (community, for conversions)
npm i -g tbx-validator
```

Auth/env: TMS API tokens (Crowdin / Lokalise / Phrase) covered by `tms-setup-crowdin-lokalise-phrase`.

## Termbase taxonomy (always split these)

```
termbase-brand.tbx       Brand voice + product names (DNT list)
termbase-product.tbx     UI labels, error messages, settings names
termbase-legal.tbx       Regulatory / legal — high formality
termbase-marketing.tbx   Transcreatable terms — flexible
termbase-domain.tbx      Industry-specific (medical, finance, gaming)
termbase-forbidden.tbx   False friends, deprecated terms, banned phrases
```

Each entry needs: `term`, `language`, `domain`, `definition`, `status` (preferred / admitted / forbidden), `partOfSpeech`, `context`.

## Common recipes

### Recipe 1: Bootstrap a brand termbase from CSV

```bash
# CSV format: term_en,term_de,term_fr,term_ja,context,part_of_speech,status
# Example row: dashboard,Übersicht,tableau de bord,ダッシュボード,Main app landing,noun,preferred

# Convert CSV → TBX with Tikal
tikal -2tbx brand.csv -o brand.tbx -sl en -tl de,fr,ja

# Or use Python (when csv format is custom)
python -c "
import csv
from lxml import etree

E = etree.Element
root = E('martif', type='TBX', attrib={'{http://www.w3.org/XML/1998/namespace}lang': 'en'})
body = etree.SubElement(etree.SubElement(root, 'text'), 'body')
with open('brand.csv') as f:
    for row in csv.DictReader(f):
        entry = etree.SubElement(body, 'termEntry')
        for lang in ['en', 'de', 'fr', 'ja']:
            lang_set = etree.SubElement(entry, 'langSet', attrib={'{http://www.w3.org/XML/1998/namespace}lang': lang})
            tig = etree.SubElement(lang_set, 'tig')
            term = etree.SubElement(tig, 'term')
            term.text = row[f'term_{lang}']
etree.ElementTree(root).write('brand.tbx', xml_declaration=True, encoding='UTF-8', pretty_print=True)
"
```

### Recipe 2: Import IATE for legal/regulatory translation

IATE (Interactive Terminology for Europe) is the EU's open multilingual termbase — 8M+ terms, 24 languages.

```bash
# Bulk export — manual download from https://iate.europa.eu/download-iate
# (CSV / TBX-Basic / RDF formats)

# Query by API for specific terms
curl -X POST 'https://iate.europa.eu/em-api/entries/_search' \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "data protection",
    "source": {"languages": ["en"]},
    "targets": {"languages": ["de", "fr", "es", "it"]},
    "limit": 100
  }'

# Filter by domain (legal = 1206; finance = 2406; environment = 5206)
curl -X POST 'https://iate.europa.eu/em-api/entries/_search' \
  -H 'Content-Type: application/json' \
  -d '{
    "domain": "1206",
    "source": {"languages": ["en"]},
    "targets": {"languages": ["de"]}
  }'
```

### Recipe 3: MultiTerm `.sdltb` → portable TBX

```bash
# In Trados Studio:
# MultiTerm → File → Export → MultiTerm 5/XML → save as .tbx

# Or via SDL MultiTerm Convert (separate utility):
# C:\Program Files (x86)\SDL\SDL MultiTerm\MultiTerm Convert\
# Choose: MultiTerm Termbase → XML (TBX)

# Validate the export
tbx-validator brand.tbx
xmllint --noout --schema https://www.tbxinfo.net/tbx-default.xsd brand.tbx
```

### Recipe 4: Upload termbase to TMS

```bash
# Crowdin glossary upload
curl -X POST "https://api.crowdin.com/api/v2/glossaries" \
  -H "Authorization: Bearer $CROWDIN_PERSONAL_TOKEN" \
  -F 'file=@brand.tbx' \
  -F 'name=brand-terms' \
  -F 'format=tbx'

# Lokalise glossary
lokalise2 glossary-term create \
  --token "$LOKALISE_API_TOKEN" --project-id $PID \
  --terms-file=brand-terms.csv

# Phrase termbase
curl -X POST "https://api.phrase.com/v2/term_bases" \
  -H "Authorization: token $PHRASE_TOKEN" \
  -F 'term_base[file]=@brand.tbx' \
  -F 'term_base[name]=brand-terms'
```

### Recipe 5: Forbidden term list (DNT — Do Not Translate)

```tbx
<termEntry id="dnt-001">
  <descrip type="subjectField">product</descrip>
  <langSet xml:lang="en">
    <tig>
      <term>API</term>
      <termNote type="termType">acronym</termNote>
      <descrip type="status">forbidden_translation</descrip>
    </tig>
  </langSet>
  <langSet xml:lang="de">
    <tig>
      <term>API</term>  <!-- same, DNT -->
      <descrip type="status">do_not_translate</descrip>
    </tig>
  </langSet>
</termEntry>
```

In Trados/memoQ/Phrase: set the term entry's status to **forbidden_translation** or attach a `do_not_translate` attribute. CAT QA flags translators who localize the DNT term.

### Recipe 6: Per-domain glossary split

```bash
# Tag CSV → TBX with domain attribute
python -c "
import csv
from lxml import etree
for domain in ['brand', 'product', 'legal', 'marketing']:
    # Read brand-master.csv, filter by domain column, write brand-<domain>.tbx
    pass
"

# Or store domain in TBX entry:
# <termEntry id='t1'><descrip type='subjectField'>legal</descrip>...
```

### Recipe 7: TBX → JSON for in-app glossary tooltips

```python
from lxml import etree
import json

tree = etree.parse('brand.tbx')
out = {}
for entry in tree.xpath('//termEntry'):
    en = entry.xpath('./langSet[@xml:lang="en"]/tig/term/text()',
                     namespaces={'xml': 'http://www.w3.org/XML/1998/namespace'})
    de = entry.xpath('./langSet[@xml:lang="de"]/tig/term/text()',
                     namespaces={'xml': 'http://www.w3.org/XML/1998/namespace'})
    if en and de:
        out[en[0]] = {'de': de[0]}
print(json.dumps(out, ensure_ascii=False, indent=2))
```

### Recipe 8: Run termbase QA against translated XLIFF

```bash
# Xbench (Windows GUI) — load termbase, run QA, export HTML report
xbench.exe -p qa-project.xbp -r terminology-report.html

# Okapi Checkmate (cross-platform) — terminology check
tikal -lc translated.xlf -tb brand.tbx -o qa-report.html

# Crowdin terminology QA — built into Crowdin QA settings:
# Project → Settings → QA → Inconsistent Glossary Terms → ON
```

### Recipe 9: Inline term highlight in TMS UI

```bash
# Crowdin highlights known terms in the editor automatically — just upload.
# Phrase: enable "Terminology" QA check in project settings.
# Lokalise: install the "Glossary" plugin in project settings.
```

### Recipe 10: Build a forbidden term list from Vale prose linter

```yaml
# .vale/styles/L10n/ForbiddenTerms.yml — for source content
extends: existence
message: "Forbidden term '%s' — use the preferred alternative."
level: error
tokens:
  - whitelist          # use "allowlist"
  - blacklist          # use "blocklist"
  - master/slave       # use "primary/replica"
  - dummy text         # use "placeholder text"
  - sanity check       # use "validity check"
```

### Recipe 11: Termbase sync — TMS ↔ git

```bash
# Export termbase nightly → commit to repo
curl -L "https://api.crowdin.com/api/v2/glossaries/<GID>/exports" \
  -H "Authorization: Bearer $CROWDIN_PERSONAL_TOKEN" \
  -X POST -d '{"format":"tbx"}' | jq -r '.data.url' > url.txt
curl "$(cat url.txt)" -o termbases/brand-$(date +%Y%m%d).tbx
git add termbases/ && git commit -m "termbase: nightly snapshot"
```

## Examples

### Example 1: Seed a 500-term brand termbase for a new product launch

**Goal:** Lock down product naming + UI verbs across 6 locales before any translation starts.

**Steps:**
1. Marketing + product write the canonical EN term list with definitions (CSV in Google Sheets).
2. Export CSV → run Recipe 1 to build `brand-2026-launch.tbx`.
3. Send TBX to LSP for initial multilingual seeding (LSP returns 6-lang TBX).
4. QA: open TBX in memoQ, spot-check 50 entries with in-market reviewers.
5. Upload to Crowdin via Recipe 4 — Crowdin highlights brand terms in translator UI.
6. Run Recipe 8 against the first translated batch — fix any flagged inconsistencies.
7. Commit TBX to repo (Recipe 11) for version history.

**Result:** Brand terminology consistent from day 1; LSPs reference it on every new project.

### Example 2: Pull EU legal terminology for GDPR docs

**Goal:** Translate a privacy policy with regulator-aligned vocabulary in DE / FR / ES / IT.

**Steps:**
1. Identify key legal terms in source: data subject, controller, processor, legitimate interest, etc.
2. For each, query IATE (Recipe 2) — capture the official EU-aligned translation per locale.
3. Build `legal-gdpr.tbx` from results (Recipe 1).
4. Upload to TMS (Recipe 4) with priority over generic terms.
5. Translator sees IATE-aligned terms surfaced as 101% matches in CAT.
6. Final QA: terminology check (Recipe 8) confirms regulator term used everywhere.

**Result:** Legal-grade terminology consistency; less rework with in-market legal reviewers.

## Edge cases / gotchas

- **TBX dialect proliferation** — TBX-Basic, TBX-Default, TBX-V3 (ISO 30042:2019). Trados outputs TBX-Default; tools differ in what they accept. Use TBX-Basic for cross-tool exchange.
- **MultiTerm convert utility is separate** — not bundled with Trados Studio installer; download separately from RWS portal.
- **IATE bulk download is huge** (~3GB compressed). Filter to your domain + languages before importing.
- **DNT terms still need a "translation"** — TBX entry must have a `<term>` in the target `<langSet>` (same string). Empty target = some QA tools mark as missing.
- **Term variants** — "sign in / sign-in / signin" are three terms. Use TBX `<termNote type="variants">` to link.
- **Forbidden in source, allowed in target** — e.g., source uses "whitelist" historically; target uses "allowlist". Mark source-side as forbidden + provide preferred → rewrite source, then translate.
- **Domain code numbers (IATE)** — use IATE domain code list: legal=1206, finance=2406, IT=3231, medical=2841. Otherwise queries return cross-domain noise.
- **Termbase size limits** — Crowdin glossary tier-capped; Lokalise unlimited; Phrase enterprise unlimited. Split large termbases by domain.
- **Multi-script terms** — Japanese has hiragana + katakana + kanji variants of same term; Chinese has SC + TC. TBX `<langSet xml:lang="ja">` should contain all variants as separate `<tig>` blocks.
- **Acronyms vs full forms** — "API" vs "Application Programming Interface". Mark with `<termNote type="termType">acronym</termNote>` + link via `<termEntry>` cross-reference.
- **Termbase ownership in vendor contracts** — clarify who owns the termbase output. Default: client owns; vendor edits.

## Sources

- IATE: https://iate.europa.eu/
- IATE Search API: https://iate.europa.eu/em-api/
- MultiTerm: https://www.trados.com/product/multiterm/
- TBX (TermBase eXchange) Standard: https://www.tbxinfo.net/
- ISO 30042:2019 (TBX): https://www.iso.org/standard/62510.html
- TBX Basic specification: https://www.tbxinfo.net/tbx-default/
- Okapi TBX support: https://okapiframework.org/wiki/index.php?title=TBX_Filter
- Crowdin glossary docs: https://support.crowdin.com/glossary/
- Phrase term base docs: https://support.phrase.com/hc/en-us/articles/5784103586460
- UNTERM: https://unterm.un.org/
