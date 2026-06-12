---
name: tm-management-leverage-optimization
description: Translation Memory (TM) hygiene playbook — per-domain split, leverage analysis, Okapi alignment, obsolete pruning. Use when the user asks about TM leverage, "audit our TM", "align legacy docs into TM", or wants to lower translation cost via better TM reuse.
---

# Translation Memory Management & Leverage Optimization

Translation memory is the load-bearing cost lever. A high-leverage project (≥40% fuzzy/exact matches) costs 40-60% less than a low-leverage one. Treat TMs like code: per-domain, version-controlled, regularly pruned.

## When to use

- "We're spending too much on translation" → run leverage analysis.
- "Migrate our old translated docs into the TM" → Okapi Rainbow / Tikal alignment.
- "We have one giant TM for the whole company" → per-domain split.
- "TM is full of garbage from 2018" → obsolete prune.
- "Switching TMS — bring our TM with us" → TMX export/import.

Trigger phrases: "TM leverage", "TM hygiene", "alignment", "TMX", "concordance audit", "translation cost down".

## Setup

```bash
# Okapi Tools (CLI-friendly TM operations)
pipx install okapi-tools
tikal --help

# Or full Okapi Rainbow (Java GUI for batch operations)
# Download: https://okapiframework.org/wiki/index.php?title=Downloads

# TMX inspection / scripting
pipx install translate-toolkit       # provides `tmx2po`, `po2tmx`, etc.
pip install lxml                     # for direct TMX parsing
```

Auth/env: none required (TMS API tokens covered by `tms-setup-crowdin-lokalise-phrase`).

## TM leverage categories (memorize these)

| Match level | Translator effort | Cost factor |
|---|---|---|
| **101% in-context** | Review only — segment + surrounding context match | 0.1× |
| **100% exact** | Verify context | 0.2× |
| **95-99% fuzzy** | Minor edit | 0.4× |
| **75-94% fuzzy** | Substantial edit | 0.6× |
| **50-74% partial** | Reference only | 0.9× |
| **New segment** | Full translation | 1.0× |

Target: ≥40% leverage on rolling 6-month average per project.

## Common recipes

### Recipe 1: Per-domain TM split (the single most impactful change)

**Never** merge UI / marketing / docs / legal TMs. "Save" as a UI button verb is not a 100% match for "Save 20%" marketing copy.

```
tm-ui.tmx          UI strings — short, technical, frequent updates
tm-marketing.tmx   Marketing copy, CTAs — rare reuse, transcreation territory
tm-docs.tmx        Documentation — verbose, technical
tm-legal.tmx       ToS / privacy / compliance — high formality, low change
tm-email.tmx       Transactional + lifecycle email templates
tm-support.tmx     Help center / chatbot — conversational
```

Set per-TMS:
```bash
# Crowdin — assign each source file a TM
crowdin tm list
crowdin tm add --name tm-ui

# Phrase
phrase translation_memories create --name tm-ui --source-locale-id <id> --target-locale-id <id>

# Lokalise — TMs are project-scoped; create one project per domain or use tag-based TM
```

### Recipe 2: Align legacy bilingual docs into TMX

```bash
# Tikal alignment from two parallel files
tikal -2tmx legacy-source.docx legacy-target.docx \
  -sl en -tl de \
  -o legacy-aligned.tmx

# For HTML docs
tikal -2tmx legacy-source.html legacy-target.html \
  -sl en -tl fr \
  -o html-aligned.tmx

# Inspect the TMX
xmllint --xpath 'count(//tu)' legacy-aligned.tmx     # segment count
```

### Recipe 3: Leverage analysis on a new batch

```bash
# Estimate translation cost before sending to LSP
# Crowdin reports leverage on each upload:
crowdin pre-translate --languages de,fr,ja --method tm --auto-approve-imported \
  --apply-untranslated-strings-only
crowdin status --json | jq '.[] | { lang: .languageId, leverage: .translationProgress }'
```

Or compute manually:
```python
# pip install lxml
from lxml import etree

tm = etree.parse('tm-ui.tmx')
tus = tm.xpath('//tu')
print(f"TM contains {len(tus)} translation units")

# New segments in source.json — count how many have a TM match
import json
sources = json.load(open('locales/en.json'))
new_segments = [k for k, v in sources.items() if v not in [tu.findtext('.//seg') for tu in tus]]
print(f"{len(new_segments)} segments lack TM match (= full cost)")
```

### Recipe 4: Obsolete prune (≥24 months unused)

```bash
# Phrase TMS API
curl -X DELETE 'https://api.phrase.com/v2/projects/<PID>/translations?q=updated_before:2024-06-11' \
  -H "Authorization: token $PHRASE_TOKEN"

# Crowdin — bulk delete by query
curl -X POST 'https://api.crowdin.com/api/v2/tms/<TM_ID>/segments/search' \
  -H "Authorization: Bearer $CROWDIN_PERSONAL_TOKEN" \
  -d '{"query":"updatedAfter<2024-06-11","limit":500}'
```

### Recipe 5: TMX export/import for TMS migration

```bash
# Export from Crowdin
crowdin tm download --id <TM_ID> --format tmx -o tm-ui.tmx

# Export from Phrase
phrase translation_memories export --id <TM_ID> --format tmx > tm-ui.tmx

# Import to Lokalise (TM merge)
lokalise2 translation-memory import \
  --token "$LOKALISE_API_TOKEN" --team-id <TEAM_ID> \
  --file=tm-ui.tmx --source-lang=en --target-lang=de
```

### Recipe 6: Concordance audit (find inconsistencies)

memoQ / Phrase / Trados all support wildcard concordance:

```
*Save*                    Finds any segment containing "Save"
"Save" (case-sensitive)   Brand-term consistency audit
src:checkout tgt:Kasse    Term-pair audit (source-side AND target-side)
```

CLI alternative — search TMX directly:
```bash
xmllint --xpath '//tu[seg[contains(., "Save")]]' tm-ui.tmx | head -100
```

### Recipe 7: Deduplicate TMX

```bash
# Strip exact duplicates (same source + same target)
python -c "
import lxml.etree as ET
tree = ET.parse('tm-ui.tmx')
tus = tree.xpath('//tu')
seen = set()
for tu in tus:
    segs = tuple(s.text for s in tu.xpath('.//seg'))
    if segs in seen:
        tu.getparent().remove(tu)
    seen.add(segs)
tree.write('tm-ui-dedup.tmx', xml_declaration=True, encoding='UTF-8')
"
```

### Recipe 8: Merge TMs cautiously

```bash
# Only merge within same domain (never UI + marketing)
# Use Okapi Rainbow GUI OR script:
python -c "
from translate.tools import tmxmerge
# Merge tm-ui-2024.tmx into tm-ui-master.tmx
"
# Or simply concatenate <tu> elements:
xmllint --xpath '//tu' tm-ui-2024.tmx > segs.xml
# Wrap and inject into master
```

### Recipe 9: TM leverage delta report (CI gate)

```python
# Run before each release — alert if leverage dropped > 5%
import json, subprocess
status = json.loads(subprocess.check_output(['crowdin', 'status', '--json']))
for locale in status:
    leverage = locale.get('translationProgress', 0)
    if leverage < 35:
        print(f"::warning::Locale {locale['languageId']} leverage {leverage}% < 35% target")
```

### Recipe 10: Per-segment context keys (raise leverage)

Add ID + context to every segment so the TM matches on context, not just source text:

```json
{
  "checkout.button.save": {
    "string": "Save",
    "context": "Checkout — save shipping address button (verb, imperative)"
  },
  "promo.banner.save20": {
    "string": "Save 20%",
    "context": "Marketing banner — discount headline (verb, exclamation)"
  }
}
```

ICU-aware TMS (Crowdin, Lokalise, Phrase) all use the `description` / `context` field for in-context matching, which becomes the **101% match** rather than 100%.

## Examples

### Example 1: Cut translation spend 40% on a 50k-string SaaS

**Goal:** Drop quarterly LSP invoice from $40k to $24k.

**Steps:**
1. Audit current TM: `crowdin tm list` → one giant TM, no domain split.
2. Export full TMX, segment by file path (Recipe 5).
3. Re-import as four TMs: `tm-ui`, `tm-marketing`, `tm-docs`, `tm-legal`.
4. Configure each source file to map to its domain TM in `crowdin.yml`.
5. Run pre-translate (Recipe 3) — leverage report shows 38% → 51% improvement on UI batch.
6. LSP next quarter quotes 38% cheaper (per-word base × leverage discount).
7. Commit TM exports to a private repo as backup.

**Result:** Annual savings ~$60k; faster turnaround; consistency in UI terminology.

### Example 2: Migrate 200 legacy PDF/DOCX translations into TM

**Goal:** Recover sunk translation cost from 2019-2022 archive into modern TM.

**Steps:**
1. Pair each source PDF with its translated counterpart.
2. Convert PDFs to text with `pdftotext` (or use `pdf` skill).
3. Run `tikal -2tmx` per pair (Recipe 2) → 200 small TMX files.
4. Merge into `tm-docs-legacy.tmx` (Recipe 8).
5. Manual QA sample: open 100 random TUs in memoQ, verify alignment quality.
6. Import to active TMS as separate "legacy" TM with lower priority.
7. New translations: TMS shows legacy 95% fuzzy matches → translators edit, not retranslate.

**Result:** ~12k segments recovered; first quarter saves ~18% on docs translation.

## Edge cases / gotchas

- **TMX 1.4 vs 2.0** — most CAT tools still default to 1.4. Use 1.4 for interchange unless TMS explicitly supports 2.0.
- **Cross-domain bleed** — single TM for UI + marketing kills both: translator picks wrong match. Always split.
- **Stale TM in long-running projects** — segments untouched > 24 months are often outdated; prune (Recipe 4). Keep history in git, not the live TM.
- **Inline tag preservation** — XLIFF inline tags (`<g>`, `<x>`, `<ph>`) must round-trip; broken tags = invalid TM unit. Use Okapi to normalize.
- **TM with embedded HTML** — strip in source before storing, re-inject on render. Otherwise leverage drops to 0% on any HTML diff.
- **Locale variants split** — `de-DE` and `de-AT` are different TM targets; never collapse. Keep separate or run alignment.
- **Case sensitivity** — "Save" vs "save" are different segments in strict TM; normalize source if intentional.
- **Concordance privacy** — TM segments may contain PII (customer names in support transcripts). Strip before storing.
- **Right-to-left round-trip** — bidi controls (`‫`, `‬`) can be lost on TMX export; verify Arabic / Hebrew TUs round-trip.
- **Auto-translate ≠ TM** — Crowdin's "auto-translation" via MT writes to TM; mark MT segments as `confirmed: false` so they don't count as leverage until reviewed.
- **TM ownership** — translators may have IP claims on TM segments under EU contractor law. Add TM ownership clause to contractor agreement.

## Sources

- Okapi Framework: https://okapiframework.org/
- Tikal CLI guide: https://okapiframework.org/wiki/index.php?title=Tikal
- TMX 1.4 spec: https://www.gala-global.org/lisa-oscar-standards
- Translate Toolkit: https://translate-toolkit.readthedocs.io/
- Crowdin TM API: https://developer.crowdin.com/api/v2/#tag/Translation-Memory
- Phrase TM API: https://developers.phrase.com/api/#translation-memories
- TM ROI calculator (Smartling): https://www.smartling.com/resources/blog/translation-memory-roi/
- memoQ TMS overview: https://www.memoq.com/product/memoq-tms/
- l10n workflow automation: https://aiproductivity.ai/guides/localization-workflow-automation/
