---
name: ai-mt-deepl-pro-post-editing
description: AI machine translation + post-editing workflows. DeepL Pro (European leader), Google Translate (breadth), Amazon Translate (cheap), ModernMT (adaptive), Lilt (adaptive+human). Document API, glossaries, formality control. Use when the user asks "translate this with DeepL", "compare MT engines", "set up post-editing".
---

# AI / MT Post-Editing — DeepL Pro / Google / Amazon / ModernMT / Lilt

DeepL leads quality on European pairs (top in 65% per Intento benchmark). Google leads breadth (249+ languages). Amazon is cheapest ($15/M chars). ModernMT learns from corrections in real time. Lilt bundles adaptive MT + human reviewer.

Post-Editing Machine Translation (PEMT) is being replaced by adaptive MT — 71% of linguists prefer adaptive over static PEMT in 2026.

## When to use

- Bulk translate UI strings, docs, support content.
- Set up adaptive learning loop (translator edits → engine retrains).
- Compare MT engines for cost / quality on user's language pairs.
- Preserve formatting in document translation (DOCX, PDF, HTML, MD).
- Enforce glossary on MT output.

Trigger phrases: "DeepL", "translate this catalog", "MT engine", "post-editing", "PEMT", "adaptive MT", "ModernMT", "Lilt", "Document API".

## Setup

```bash
# DeepL — via MCP (preferred) or REST
# MCP: see app/config/mcp_config.json → deepl-mcp

# DeepL REST
curl -X POST 'https://api.deepl.com/v2/translate' \
  -H "Authorization: DeepL-Auth-Key $DEEPL_API_KEY" \
  -d 'text=Hello&target_lang=DE'

# Google Cloud Translation
pipx install google-cloud-translate

# Amazon Translate (via AWS CLI)
pipx install awscli
aws translate translate-text --source-language-code en --target-language-code de --text "Hello"

# ModernMT
# REST — no SDK install needed
# pip install modernmt-python  # community SDK

# Lilt — enterprise REST API
# No SDK; use curl
```

Auth/env:
- `DEEPL_API_KEY` — `https://www.deepl.com/account` (Free 500k chars/mo; Pro from €5.49/mo)
- `GOOGLE_APPLICATION_CREDENTIALS` — service account JSON path
- AWS creds via `~/.aws/credentials`
- `MODERNMT_API_KEY` — `https://www.modernmt.com/`
- `LILT_API_KEY` — enterprise contract

## Engine comparison (2026)

| Engine | Quality (EU pairs) | Languages | Price (per 1M chars) | Adaptive | Document API |
|---|---|---|---|---|---|
| DeepL Pro | Top in 65% | 100+ | $20-25 | No | Yes (DOCX/PDF/HTML/PPTX) |
| Google Translate | Strong | 249+ | $20 (≤500k free) | No | Yes |
| Amazon Translate | Decent | 80+ | $15 | Custom-trained | Yes |
| Azure Translator | Strong | 130+ | $10 | Custom-trained | Yes |
| ModernMT | Strong + adaptive | 200+ | $10-40 | Yes (real-time) | Limited |
| Lilt | Strong + adaptive | 60+ | Enterprise | Yes + human | Limited |
| memoQ AGT | Best with TM/TB | 50+ | Bundled | Yes (LLM) | Via memoQ |

## Common recipes

### Recipe 1: DeepL REST — single string

```bash
curl -X POST 'https://api.deepl.com/v2/translate' \
  -H "Authorization: DeepL-Auth-Key $DEEPL_API_KEY" \
  -d 'text=Save your work before closing.' \
  -d 'target_lang=DE' \
  -d 'formality=more' \
  -d 'preserve_formatting=1' \
  -d 'tag_handling=html'
```

Returns:
```json
{"translations":[{"detected_source_language":"EN","text":"Speichern Sie Ihre Arbeit, bevor Sie sie schließen."}]}
```

### Recipe 2: DeepL with glossary

```bash
# Create glossary
curl -X POST 'https://api.deepl.com/v2/glossaries' \
  -H "Authorization: DeepL-Auth-Key $DEEPL_API_KEY" \
  -d 'name=brand-en-de' \
  -d 'source_lang=EN' \
  -d 'target_lang=DE' \
  -d 'entries_format=csv' \
  --data-urlencode 'entries=API,API
SDK,SDK
endpoint,Endpunkt'
# → returns {"glossary_id": "abc123..."}

# Use on translate
curl -X POST 'https://api.deepl.com/v2/translate' \
  -H "Authorization: DeepL-Auth-Key $DEEPL_API_KEY" \
  -d 'text=Connect to the API endpoint.' \
  -d 'target_lang=DE' \
  -d 'glossary_id=abc123...'
```

### Recipe 3: DeepL Document API (DOCX, PDF, HTML)

```bash
# Upload document
RESPONSE=$(curl -X POST 'https://api.deepl.com/v2/document' \
  -H "Authorization: DeepL-Auth-Key $DEEPL_API_KEY" \
  -F 'file=@whitepaper.docx' \
  -F 'target_lang=DE' \
  -F 'formality=more')
DOC_ID=$(echo $RESPONSE | jq -r '.document_id')
DOC_KEY=$(echo $RESPONSE | jq -r '.document_key')

# Poll status
curl "https://api.deepl.com/v2/document/$DOC_ID" \
  -H "Authorization: DeepL-Auth-Key $DEEPL_API_KEY" \
  -d "document_key=$DOC_KEY"

# Download when status = "done"
curl -X POST "https://api.deepl.com/v2/document/$DOC_ID/result" \
  -H "Authorization: DeepL-Auth-Key $DEEPL_API_KEY" \
  -d "document_key=$DOC_KEY" \
  -o whitepaper-de.docx
```

Document API preserves all formatting — fonts, images, tables, paragraph styles.

### Recipe 4: DeepL via MCP

```ts
// MCP tool: deepl-mcp exposes `translate`, `translate_document`, `glossary_*`
// Call from agent:
await tools.deepl.translate({
  text: 'Save your work.',
  target_lang: 'DE',
  formality: 'more',
  tag_handling: 'html',
  glossary_id: 'abc123...'
});
```

### Recipe 5: Google Translate v3 — batch

```bash
gcloud auth application-default login

curl -X POST "https://translation.googleapis.com/v3/projects/$PROJECT/locations/global:translateText" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "sourceLanguageCode": "en",
    "targetLanguageCode": "de",
    "contents": ["Hello", "World", "Save your work"]
  }'
```

### Recipe 6: Amazon Translate — batch via S3

```bash
aws translate start-text-translation-job \
  --job-name release-2026Q3 \
  --source-language-code en \
  --target-language-codes de fr ja \
  --input-data-config S3Uri=s3://bucket/sources/,ContentType=text/plain \
  --output-data-config S3Uri=s3://bucket/output/ \
  --data-access-role-arn arn:aws:iam::123:role/translate

aws translate describe-text-translation-job --job-id <JOB_ID>
```

### Recipe 7: ModernMT — adaptive translation

```bash
# Translate (uses learned corrections)
curl 'https://api.modernmt.com/translate' \
  -H "MMT-ApiKey: $MODERNMT_API_KEY" \
  -d 'source=en' \
  -d 'target=de' \
  -d 'q=Save your work' \
  -d 'priority=normal'

# Feedback — train the engine
curl -X PUT 'https://api.modernmt.com/memories/<MEM_ID>/content' \
  -H "MMT-ApiKey: $MODERNMT_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "source": "en",
    "target": "de",
    "sentence": "Save your work",
    "translation": "Speichern Sie Ihre Arbeit"
  }'
# Next translation gets the correction
```

### Recipe 8: Lilt adaptive translation

```bash
curl -X POST 'https://api.lilt.com/v2/translate' \
  -H "Authorization: Basic $(echo -n :$LILT_API_KEY | base64)" \
  -H 'Content-Type: application/json' \
  -d '{
    "source": "Save your work before closing.",
    "source_lang": "en",
    "target_lang": "de",
    "memory_id": <MEMORY_ID>
  }'

# Submit corrected translation back to memory
curl -X POST "https://api.lilt.com/v2/memories/<MEM_ID>/segments" \
  -H "Authorization: Basic $(echo -n :$LILT_API_KEY | base64)" \
  -d '{
    "source": "Save your work before closing.",
    "target": "Speichern Sie Ihre Arbeit, bevor Sie schließen."
  }'
```

### Recipe 9: PEMT (Post-Editing MT) workflow

```
1. Source segment → MT engine → raw MT
2. Translator opens in CAT (memoQ / Trados / Phrase TMS)
3. Edits raw MT to final translation
4. CAT counts post-edit effort (PED — % of segment changed)
5. Final segment → TM
6. If adaptive MT (ModernMT / Lilt): correction back to engine
```

PED categories:
- 0-10%: light PE (LPE) — minor cleanup
- 10-40%: medium PE (MPE)
- 40-70%: heavy PE (HPE) — substantial rewrite
- 70%+: discard MT, full translate

### Recipe 10: Bulk JSON catalog translation

```bash
# Translate entire en.json → de.json via DeepL
jq -r 'to_entries[] | "\(.key)|\(.value)"' en.json | while IFS='|' read -r key val; do
  translated=$(curl -s -X POST 'https://api.deepl.com/v2/translate' \
    -H "Authorization: DeepL-Auth-Key $DEEPL_API_KEY" \
    --data-urlencode "text=$val" \
    -d 'target_lang=DE' \
    -d 'formality=more' \
    | jq -r '.translations[0].text')
  echo "  \"$key\": \"$translated\","
done > de.json.partial
```

Better — use Crowdin / Phrase / Lokalise's built-in MT pre-translate (handles ICU correctly).

### Recipe 11: TMS-integrated MT pre-translate

```bash
# Crowdin
crowdin pre-translate --languages de,fr,ja --method mt --auto-approve-imported \
  --apply-untranslated-strings-only

# Phrase
phrase pre_translate \
  --target-locale-ids <LOC_ID> --machine-translate-settings-id <MT_ID>

# Lokalise — auto-translate via UI or:
lokalise2 translation upload \
  --token "$LOKALISE_API_TOKEN" --project-id $PID \
  --use-auto-translation --filter-data='untranslated'
```

### Recipe 12: Quality estimation (which MT segments need PE)

DeepL returns confidence; ModernMT scores per segment. Triage by score:
```python
# Pseudocode
for seg in raw_mt:
    if seg.confidence > 0.95:
        seg.status = 'auto-approve'    # ship as-is
    elif seg.confidence > 0.85:
        seg.status = 'spot-review'     # sample 10% review
    else:
        seg.status = 'full-PE'         # translator edits
```

### Recipe 13: Glossary auto-build from TM

```bash
# Extract high-frequency source terms → seed glossary
python -c "
import json, collections
en = json.load(open('locales/en.json'))
words = collections.Counter()
for v in en.values():
    words.update(v.split())
common = [w for w, c in words.most_common(200) if len(w) > 3]
print('\n'.join(common))
" > candidate-terms.txt
# Human review → upload to DeepL glossary
```

### Recipe 14: Formality control (DeepL)

```bash
# DeepL formality params (DE/FR/ES/IT/JA/RU/NL/PT/PL support)
curl ... -d 'formality=more'       # formal (Sie / vous)
curl ... -d 'formality=less'       # informal (du / tu)
curl ... -d 'formality=default'    # MT decides
```

JA: `formality=more` produces です/ます; `less` produces だ/である.

### Recipe 15: Compare engines on user pairs

```bash
# Quick QC: same source → 3 engines → human ranks
SRC="Save your work before closing the application."
for ENG in deepl google amazon; do
  case $ENG in
    deepl) curl -s 'https://api.deepl.com/v2/translate' -H "Authorization: DeepL-Auth-Key $DEEPL_API_KEY" -d "text=$SRC" -d 'target_lang=DE' | jq -r '.translations[0].text' ;;
    google) gcloud translate --target=de --source=en "$SRC" ;;
    amazon) aws translate translate-text --source-language-code en --target-language-code de --text "$SRC" | jq -r '.TranslatedText' ;;
  esac
  echo "  ↑ $ENG"
done
```

## Examples

### Example 1: Translate 5k UI strings into 6 locales with DeepL Pro

**Goal:** Initial bulk MT pre-translation; human reviewers edit afterwards.

**Steps:**
1. Push source `en.json` to Crowdin (or use direct DeepL API).
2. Create DeepL glossary for brand terms (Recipe 2): "API", "SDK", "CraftBot" → DNT.
3. Run Crowdin MT pre-translate (Recipe 11) with DeepL engine + glossary.
4. Set strings to "needs review" status.
5. In-country reviewer opens Crowdin, edits MT to final translation.
6. CI pulls approved translations (Recipe `download --export-only-approved`).
7. Cost: 5000 strings × 50 chars × 6 locales = 1.5M chars × $0.025 = ~$37.50.

**Result:** Initial pre-translation in hours, not weeks; PED ~20-30% across locales.

### Example 2: Translate a 50-page DOCX whitepaper preserving formatting

**Goal:** Sales whitepaper in EN → DE/FR/ES with intact formatting (fonts, tables, images).

**Steps:**
1. Upload to DeepL Document API (Recipe 3) per target locale.
2. Poll status — each doc takes 2-10 min.
3. Download translated DOCX.
4. Open in Word → spot-check tables, captions, footers — formatting preserved.
5. Send to in-market reviewer for final edit pass.

**Result:** No manual formatting recovery; reviewer focuses on language, not layout.

### Example 3: Adaptive MT loop with ModernMT for support docs

**Goal:** Support docs translated DE/FR over 6 months; want engine to learn brand voice.

**Steps:**
1. Initial batch translated with ModernMT (Recipe 7).
2. Translator edits final strings in TMS.
3. CI script POSTs corrected segments back to ModernMT memory (Recipe 7 feedback).
4. After 1000 corrections, batch 2 MT quality measurably improves (lower PED).
5. After 5000 corrections, batch 5 MT is near-shippable for low-stakes segments.

**Result:** Per-segment translation effort drops 30-50% over project lifetime.

## Edge cases / gotchas

- **DeepL free tier** — `api-free.deepl.com` (not `api.deepl.com`). 500k chars/month; rate-limited.
- **DeepL `tag_handling`** — `xml` or `html`. Without, inline tags get translated. Always set for HTML/Markdown sources.
- **DeepL `preserve_formatting=1`** — preserves whitespace, capitalization, punctuation; without, MT may "fix" stylistic choices.
- **Glossary lifecycle** — DeepL glossaries are immutable; updates require delete + recreate. Version glossary IDs.
- **Google language code** — uses ISO 639-1 (`de`, not `de-DE`). DeepL uses uppercased (`DE`).
- **Amazon Translate active learning** — `Active Custom Translation` requires parallel corpus upload; setup heavier.
- **ModernMT memory scope** — per-API-key. Sharing memories across users complicates "who edited what".
- **Lilt is enterprise-only** — no self-serve; minimum monthly commitment.
- **Document API quota** — DeepL Pro: 10MB max per doc; 1000-page hard cap. Google: 20MB.
- **PDF translation** — DeepL Document API does PDF → DOCX (not PDF → PDF). Formatting partially preserved.
- **Cost trap on JSON** — `tag_handling=html` on JSON sometimes mangles backslash escapes. Test on a sample.
- **Source detect cost** — `source_lang` auto-detected by DeepL/Google; faster + cheaper to set explicitly.
- **Rate limits** — DeepL Pro: 120 req/sec (paid tier dependent). Google: 6000 char/sec. Burst with care.
- **MT output ≠ translation** — for legal, brand, marketing copy, always have human in the loop.
- **Bilingual context** — adaptive engines need bilingual pairs, not monolingual edits. Don't dump corrections without source.
- **Pre-existing translations** — MT may overwrite hand-translated segments if pre-translate runs over them. Use `--apply-untranslated-strings-only` (Crowdin) or equivalent.

## Sources

- DeepL API docs: https://developers.deepl.com/
- DeepL Document API: https://developers.deepl.com/docs/api-reference/document
- DeepL glossaries: https://developers.deepl.com/docs/api-reference/glossaries
- DeepL formality: https://developers.deepl.com/docs/api-reference/translate
- Google Translate v3: https://cloud.google.com/translate/docs/reference/rest/v3
- Amazon Translate: https://docs.aws.amazon.com/translate/latest/dg/what-is.html
- ModernMT API: https://www.modernmt.com/api/
- Lilt API: https://lilt.com/docs
- Lilt adaptive MT vs PEMT: https://lilt.com/blog/ai-translation-automation-how-enterprise-translation-systems-work
- Best AI translation 2026: https://www.techno-pulse.com/2026/04/best-ai-translation-tools-in-2026-deepl.html
- Intento State of MT 2024: https://inten.to/state-of-machine-translation-2024/
