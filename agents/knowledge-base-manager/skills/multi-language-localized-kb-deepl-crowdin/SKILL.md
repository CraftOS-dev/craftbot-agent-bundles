---
name: multi-language-localized-kb-deepl-crowdin
description: Multi-language KB — DeepL Pro (tag_handling=markdown), Crowdin/Lokalise translation memory + glossary, locale routing (Docusaurus i18n, Starlight locales, MkDocs Material i18n). FOSS fallback Argos Translate. Use when shipping KB in multiple languages.
---

# Multi-language KB — DeepL + Crowdin + Lokalise + Argos

## When to use

User says "translate KB", "i18n docs", "DeepL", "Crowdin", "Lokalise", "ship docs in German/Japanese". Reach AFTER source-of-truth locale is fixed and BEFORE shipping any new content (translation queue must be wired upfront).

## Setup

```bash
# DeepL Pro API
pip install deepl
export DEEPL_API_KEY=...    # https://www.deepl.com/account/summary

# Crowdin CLI
npm i -g @crowdin/cli
crowdin --version

# Lokalise CLI
brew install lokalise2     # macOS
# or
curl -sf https://raw.githubusercontent.com/lokalise/lokalise-cli-2-go/master/install.sh | sh

# Argos Translate (FOSS, local)
pip install argostranslate
# Download language pack
argospm install translate-en_de
```

Auth / API key requirements:
- `DEEPL_API_KEY` — Free tier 500k chars/mo, Pro unlimited
- `CROWDIN_PROJECT_ID` + `CROWDIN_TOKEN`
- `LOKALISE_PROJECT_ID` + `LOKALISE_TOKEN`

## Common recipes

### Recipe 1: DeepL translate single markdown file

```python
import deepl, pathlib, os
translator = deepl.Translator(os.environ['DEEPL_API_KEY'])
src = pathlib.Path('docs/how-to/sso-okta.md')
text = src.read_text()
result = translator.translate_text(
    text,
    source_lang="EN",
    target_lang="DE",
    tag_handling="markdown",   # KEY: preserves md structure
    preserve_formatting=True,
)
pathlib.Path('docs/de/how-to/sso-okta.md').write_text(result.text)
```

### Recipe 2: DeepL with glossary

```python
# Create glossary first
glossary = translator.create_glossary(
    "Acme EN-DE", source_lang="EN", target_lang="DE",
    entries={"webhook":"Webhook","SSO":"SSO","API key":"API-Schlüssel"}
)

result = translator.translate_text(
    text, source_lang="EN", target_lang="DE",
    tag_handling="markdown",
    glossary=glossary,
)
```

### Recipe 3: DeepL formality control

```python
# Per-locale formality
# DE/JA support formality
result = translator.translate_text(
    text, source_lang="EN", target_lang="DE",
    formality="less",   # informal — useful for docs voice
    tag_handling="markdown",
)
```

### Recipe 4: Crowdin — bootstrap project + upload sources

```yaml
# crowdin.yml
project_id: '$CROWDIN_PROJECT_ID'
api_token: '$CROWDIN_TOKEN'
preserve_hierarchy: true
files:
  - source: '/docs/**/*.md'
    translation: '/docs/%two_letters_code%/**/%original_file_name%'
    ignore: ['**/_archived/**']
```

```bash
crowdin init       # creates crowdin.yml interactively
crowdin upload sources
crowdin upload translations   # initial bootstrap
```

### Recipe 5: Crowdin — download translations

```bash
crowdin download
# or per-locale
crowdin download -l de
```

### Recipe 6: Crowdin — pre-translate via DeepL MT engine

```bash
# Configure MT engine in Crowdin UI: Project → MT Engines → DeepL
# Then via API:
curl -X POST "https://api.crowdin.com/api/v2/projects/${CROWDIN_PROJECT_ID}/pre-translations" \
  -H "Authorization: Bearer $CROWDIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"languageIds":["de","ja","fr"],"fileIds":[123,456],"method":"mt","engineId":42}'
```

### Recipe 7: Lokalise — push/pull

```bash
# Upload sources
lokalise2 file upload \
  --token "$LOKALISE_TOKEN" --project-id "$LOKALISE_PROJECT_ID" \
  --file "docs/**/*.md" --lang-iso en \
  --replace-modified

# Download translations
lokalise2 file download \
  --token "$LOKALISE_TOKEN" --project-id "$LOKALISE_PROJECT_ID" \
  --format md --bundle-structure "docs/%LANG_ISO%/%FILENAME%"
```

### Recipe 8: Argos Translate (FOSS local)

```python
import argostranslate.translate
text = open('docs/how-to/sso-okta.md').read()
translated = argostranslate.translate.translate(text, "en", "de")
open('docs/de/how-to/sso-okta.md','w').write(translated)
```

### Recipe 9: Docusaurus i18n config

```javascript
// docusaurus.config.js
module.exports = {
  i18n: {
    defaultLocale: 'en',
    locales: ['en','de','ja','fr'],
    localeConfigs: {
      de: { label: 'Deutsch', direction: 'ltr', htmlLang: 'de-DE' },
      ja: { label: '日本語', direction: 'ltr', htmlLang: 'ja-JP' },
    },
  },
};
```

```bash
# Generate per-locale folders
npm run write-translations -- --locale de
```

### Recipe 10: Starlight locales

```javascript
// astro.config.mjs
import starlight from '@astrojs/starlight';
export default defineConfig({
  integrations: [starlight({
    defaultLocale: 'en',
    locales: {
      en: { label: 'English' },
      de: { label: 'Deutsch' },
      ja: { label: '日本語' },
    },
  })],
});
```

Folder layout: `src/content/docs/en/...`, `src/content/docs/de/...`.

### Recipe 11: MkDocs Material i18n plugin

```yaml
plugins:
  - i18n:
      docs_structure: folder
      languages:
        - locale: en
          default: true
          name: English
        - locale: de
          name: Deutsch
        - locale: ja
          name: 日本語
```

### Recipe 12: CI gate — block release if locale missing >5% of source

```yaml
# .github/workflows/i18n-coverage.yml
on: [pull_request]
jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          for loc in de ja fr; do
            SRC=$(find docs/en -name '*.md' | wc -l)
            TGT=$(find docs/$loc -name '*.md' | wc -l)
            COV=$((TGT*100/SRC))
            echo "$loc coverage: $COV%"
            [ "$COV" -lt 95 ] && { echo "::error::$loc below 95%"; exit 1; }
          done
```

### Recipe 13: Triggered translation on PR merge

```yaml
# .github/workflows/translate-on-merge.yml
on:
  push:
    branches: [main]
    paths: ['docs/en/**']
jobs:
  translate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install deepl
      - run: |
          for f in $(git diff --name-only HEAD~1 -- docs/en/); do
            python scripts/translate.py "$f" de ja fr
          done
      - run: |
          git add docs/de/ docs/ja/ docs/fr/
          git diff --staged --quiet || git commit -m "i18n: auto-translate"
          git push
```

## Examples

### Example 1: Launch German + Japanese docs

**Goal:** 200 EN articles → bilingual.

**Steps:**
1. Lock EN as source-of-truth.
2. Crowdin bootstrap (Recipe 4); upload sources.
3. DeepL pre-translation (Recipe 6).
4. Glossary per locale (Recipe 2).
5. Crowdin assigns native SME reviewers; PRs reviewed in-tool.
6. Download approved translations (Recipe 5).
7. Docusaurus i18n (Recipe 9); deploy.
8. CI gate at 95% (Recipe 12).

**Result:** Bilingual docs site within 6-8 weeks.

### Example 2: Self-host Argos for low-budget

**Goal:** No paid translation; ship "rough" locales with caveat banner.

**Steps:**
1. Install Argos + en→de + en→ja language packs.
2. Loop over `docs/en/**`, translate to `docs/{de,ja}/**` (Recipe 8).
3. Add banner: "Machine-translated; PRs welcome to improve."

**Result:** $0; lower quality but accessible.

## Edge cases / gotchas

- **DeepL tag_handling=markdown** is essential — without it, `**bold**` becomes `* * fett * *`.
- **DeepL char-count includes markdown formatting** — budget 1.3× source size for billing.
- **DeepL supports limited locales** — no Arabic / Hebrew yet. Use Crowdin's other MT engines for those.
- **Crowdin TM warms up slowly** — first 1000 strings have low TM hit rate; expect cost spike at start.
- **Translation memory leaks scope** — TM auto-suggests across projects. Use separate Crowdin projects per product line.
- **Per-locale slug rewriting** — if your slugs are English, translated nav looks odd. Some teams keep EN slugs.
- **Right-to-left** (ar/he) requires `direction: rtl` and tested layout.
- **MkDocs i18n plugin** is community; pin version.
- **Lokalise free tier** is limited; for >250 strings you need paid.
- **Argos quality lags DeepL** noticeably. Use for "good enough" not "production".
- **JA formality** — DeepL supports formal/informal but not full keigo levels.

## Sources

- DeepL API: https://developers.deepl.com/
- DeepL markdown handling: https://developers.deepl.com/docs/xml-and-html-handling/markdown
- DeepL glossary: https://developers.deepl.com/docs/api-reference/glossaries
- Crowdin API: https://developer.crowdin.com/
- Crowdin CLI: https://crowdin.github.io/crowdin-cli/
- Lokalise: https://docs.lokalise.com/
- Argos Translate: https://github.com/argosopentech/argos-translate
- Docusaurus i18n: https://docusaurus.io/docs/i18n/introduction
- Starlight i18n: https://starlight.astro.build/guides/i18n/
- MkDocs Material i18n: https://squidfunk.github.io/mkdocs-material/setup/changing-the-language/
