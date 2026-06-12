---
name: cat-tool-memoq-trados-phrase
description: CAT tool setup — memoQ (desktop + AGT adaptive MT), Trados Studio (largest LSP supply chain), Phrase TMS (cloud-native). Use when the user asks "set up memoQ project", "Trados package", "adaptive MT in CAT", or wants CAT tool selection guidance.
---

# CAT Tool Setup — memoQ / Trados / Phrase TMS

CAT tools sit between the TMS and the translator. **memoQ** has the deepest TM concordance + memoQ AGT (adaptive generative translation, 2025+). **Trados Studio** has the widest LSP supply chain. **Phrase TMS** is cloud-native + integrates with Phrase Strings.

Adaptive MT (memoQ AGT, Lilt, Unbabel) is replacing static PEMT in 2026 — 71% of linguists prefer adaptive over traditional post-editing.

## When to use

- The user is creating a translator-facing CAT project.
- The user needs to export a Trados "package" for an LSP.
- The user wants adaptive MT (AGT, Lilt) enabled in CAT.
- The user is choosing between desktop CAT (memoQ/Trados) and cloud CAT (Phrase TMS).
- The user has Trados / memoQ files (`.sdlxliff`, `.mqxlz`, `.mqxliff`) to inspect.

Trigger phrases: "memoQ project", "Trados package", "AGT", "adaptive MT", "sdlxliff", "mqxliff", "Phrase TMS", "CAT tool".

## Setup

### memoQ

- **memoQ Desktop** (Windows) — most powerful UI; required for offline work. Trial: 30 days.
- **memoQ Cloud** — paid cloud variant; same engine, browser-accessible.
- **memoQ Server** — on-prem (enterprise).

Install Desktop: download from `https://www.memoq.com/downloads`. Activate with license server URL.

### Trados Studio

- **Trados Studio** (Windows desktop) — subscription includes MultiTerm.
- **Trados Live** — cloud variant.
- **Trados Team / Enterprise** — server.

Install: `https://www.trados.com/products/trados-studio/`. Per-seat licensing.

### Phrase TMS (cloud, formerly Memsource)

- Browser-based — no install. Sign up at `https://phrase.com/`.
- CLI for project management: included with `@phrase/cli` package (covered in `tms-setup-crowdin-lokalise-phrase` skill).

## Common recipes

### Recipe 1: memoQ — create a project (Desktop GUI)

```
File → New Project → Wizard

1. Project name, source language, target languages (multiselect)
2. Translation Memories: attach existing tm-ui.tmx (read-only for reference) + tm-ui-current.tmx (writable)
3. Termbases: attach termbase-brand.mtbx + termbase-product.mtbx
4. MT Settings: select engine (DeepL Pro / Google / AGT) — see Recipe 3
5. Import documents: drag XLIFF / DOCX / IDML / HTML in
6. Assign translators per locale → Send delivery email
```

CLI equivalent (memoQ Server REST API):
```bash
curl -X POST 'https://memoq.example.com/memoQServices/Resources/Projects/Create' \
  -H "Authorization: Bearer $MEMOQ_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "release-2026-Q3",
    "sourceLanguageCode": "en-US",
    "targetLanguageCodes": ["de-DE", "fr-FR", "ja-JP"]
  }'
```

### Recipe 2: memoQ AGT — adaptive generative translation

memoQ AGT (2025+) is an LLM-based adaptive engine that learns from the project's TM + termbase. Enable in Project Settings:

```
Project home → Settings → Machine Translation → Add:
  Provider: memoQ AGT
  Domain: select "Custom — fine-tune with current TM + TB"
  Glossary enforcement: ON
  Style guide: paste brand voice
```

Use during translation: AGT suggestions appear in the Translation Results panel, ranked above static MT.

### Recipe 3: memoQ + DeepL / Google MT integration

```
Settings → Machine Translation → New plugin:
  Engine: DeepL Pro
  API Key: <DEEPL_API_KEY>
  Formality: prefer formal (DE/ES/JA support)
  Glossary ID: <from DeepL glossary endpoint>

Result: confirm 100% TM match first, then AGT, then DeepL Pro, then Google as fallback.
```

### Recipe 4: Trados Studio — open an `.sdlxliff` file

```
File → Open → Translate Single Document → select .sdlxliff
# OR open a Trados Package (.sdlppx)
File → Open → Open Package → .sdlppx
```

Trados package contains: source XLIFF + reference TMs + termbases + project settings. Translator returns a `.sdlrpx` return package.

CLI inspect (no Trados install needed):
```bash
# SDLXLIFF is XML — inspect with xmllint
xmllint --xpath '//trans-unit[@id="42"]' file.sdlxliff
xmllint --xpath 'count(//trans-unit[not(target/text())])' file.sdlxliff   # untranslated count
```

### Recipe 5: Trados — export bilingual review file (Word)

For non-CAT reviewers (lawyers, in-market reviewers without Trados):

```
Batch Tasks → Export for Bilingual Review → DOCX
# Translator edits in Word, returns DOCX
Batch Tasks → Update from Bilingual Review → DOCX
```

### Recipe 6: Phrase TMS — create project via REST

```bash
curl -X POST 'https://cloud.memsource.com/web/api2/v1/projects' \
  -H "Authorization: ApiToken $PHRASE_TMS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "release-2026-Q3",
    "sourceLang": "en",
    "targetLangs": ["de", "fr", "ja-jp"],
    "machineTranslateSettings": {
      "machineTranslateSettingsUid": "<settings-uid>"
    }
  }'
```

### Recipe 7: Phrase TMS — upload job + assign translator

```bash
# Upload source file as job
curl -X POST 'https://cloud.memsource.com/web/api2/v1/projects/<PID>/jobs' \
  -H "Authorization: ApiToken $PHRASE_TMS_TOKEN" \
  -F 'memsource={"targetLangs":["de"]}' \
  -F 'file=@locales/en.json'

# Assign to translator
curl -X PATCH 'https://cloud.memsource.com/web/api2/v1/projects/<PID>/jobs/<JID>' \
  -H "Authorization: ApiToken $PHRASE_TMS_TOKEN" \
  -d '{"providers":[{"id":"<translator-uid>","type":"USER"}]}'
```

### Recipe 8: Concordance search (memoQ wildcards)

Most powerful concordance in 2026:
```
*Save*                     contains "Save"
"Save"                     exact match
src:checkout tgt:Kasse     source+target pair
^Save                      starts with "Save"
Save$                      ends with "Save"
```

### Recipe 9: Lilt adaptive MT integration

Lilt's API can plug into memoQ, Phrase, or run standalone:

```bash
curl -X POST 'https://api.lilt.com/v2/translate' \
  -H "Authorization: Basic $(echo -n :$LILT_API_KEY | base64)" \
  -d '{
    "source": "Save your work.",
    "memory_id": "<MEM_ID>",
    "source_lang": "en",
    "target_lang": "de"
  }'
```

Adaptive loop: translator edits → POST back to `/v2/memories/<id>/feedback` → Lilt updates the model for next segment in the same project.

### Recipe 10: Inspect `.mqxliff` file (memoQ XLIFF)

```bash
# Same as XLIFF — but memoQ-specific extensions in mq: namespace
xmllint --xpath 'count(//trans-unit[@mq:status="Confirmed"])' file.mqxliff
xmllint --xpath '//trans-unit[mq:status="ProofreadConfirmed"]' file.mqxliff | head -50
```

### Recipe 11: Cloud CAT comparison vector

```
Phrase TMS  → strongest API, native cloud, ICU support, REST first
memoQ Cloud → desktop feature parity in browser, AGT included
Trados Live → familiar UI for Trados translators, MultiTerm cloud
matecat     → free, browser, no install
Smartcat    → CAT + marketplace combined
```

## Examples

### Example 1: Stand up a memoQ AGT-powered project for a new SaaS launch

**Goal:** Translate 200k words of release content into 8 languages with adaptive MT keeping per-locale consistency.

**Steps:**
1. Open memoQ Desktop → New Project (Recipe 1).
2. Attach `tm-ui-master.tmx` (write-protected reference) + create new `tm-ui-2026Q3.tmx` (writable).
3. Attach `termbase-brand.mtbx` (forbidden + preferred terms) + `termbase-product.mtbx`.
4. MT settings: AGT primary + DeepL Pro secondary (Recipes 2-3).
5. Import all `.json` (locale catalogs) + `.xliff` (from Phrase TMS) sources.
6. Pre-translate: TM ≥75% applied automatically + AGT suggestions for ≤74% segments.
7. Assign per-locale translator. Translator gets pre-leveraged file, reviews AGT suggestions live.
8. Deliver: export approved segments back to `.json`; re-import into Phrase TMS as 100% match.

**Result:** ~70% reduction in raw translation hours vs. static MT post-editing.

### Example 2: Run Trados package from an LSP through review

**Goal:** A vendor returned a `release-2026.sdlrpx` package; need to import, QA, deliver final.

**Steps:**
1. Open Trados Studio → File → Open → Open Return Package → `release-2026.sdlrpx`.
2. Batch Tasks → Verify Files → Trados QA Checker — flags missing tags, terminology violations.
3. Run Xbench QA in parallel (see `locale-qa-linguistic-functional` skill) for terminology mismatches.
4. Review flagged segments in Editor; accept or reject.
5. Batch Tasks → Generate Target Translations → final `.json` per locale.
6. Update reference TM: Batch Tasks → Update Main Translation Memories.

**Result:** Final locale files ready for production; TM grown by ~12k new segments.

## Edge cases / gotchas

- **memoQ Desktop = Windows-only** — no native macOS/Linux. Workaround: memoQ Cloud or VM.
- **Trados file format proliferation** — `.sdlxliff` (file), `.sdlppx` (project package out), `.sdlrpx` (return package), `.sdltm` (TM binary), `.sdltb` (termbase binary). Binary formats only readable in Trados; use `tikal` to convert to TMX/XLIFF.
- **memoQ vs Trados TM portability** — both export TMX, but inline tag formats differ. Always export via the source tool, then re-import via the target tool's TMX importer (not direct binary copy).
- **AGT requires memoQ 2025+ Server tier** — desktop AGT requires connecting to a paid AGT server endpoint. Confirm tier before promising AGT to user.
- **CAT pricing** — memoQ Translator Pro ~€770/year; Trados Studio Professional ~€2,895 one-time; Phrase TMS starts $200/mo. Inform the user when CAT is required.
- **Translator onboarding** — sending a Trados package to a memoQ-only translator wastes a round-trip. Use the universal XLIFF 2.0 path or ask translator's CAT in advance.
- **Inline tags lost on round-trip** — XLIFF `<ph>`/`<g>` tags must round-trip; some MT engines strip them. Use memoQ "tag protection" or Trados "tag verification" before delivery.
- **Termbase format conversion** — MultiTerm `.sdltb` (Trados) ≠ memoQ `.mtbx`. Convert via TBX (TermBase eXchange) — covered in `glossary-termbase-multiterm` skill.
- **AGT does not equal LLM general translation** — AGT is fine-tuned on the project's TM + termbase. Quality drops outside the trained domain.
- **Lilt API requires enterprise contract** — not self-serve. Smaller orgs use Lilt via Phrase TMS connector or stay with DeepL + memoQ AGT.
- **Phrase TMS rate limits** — 10 req/sec on enterprise; bulk job upload requires `/projects/<id>/jobs/bulk` endpoint.

## Sources

- memoQ AGT: https://www.memoq.com/product/memoq-agt/
- memoQ TMS: https://www.memoq.com/product/memoq-tms/
- Trados Studio: https://www.trados.com/products/trados-studio/
- Phrase TMS API: https://cloud.memsource.com/web/docs/api
- Lilt API: https://lilt.com/docs
- Lilt adaptive MT: https://lilt.com/blog/ai-translation-automation-how-enterprise-translation-systems-work
- Adaptive MT vs PEMT: https://labs.lilt.com/free-the-translators-how-adaptive-mt-turns-post-editing-janitors-into-cultural-consultants
- CAT tool comparison: https://intlpull.com/blog/top-10-localization-tools-tms-comparison-2026
