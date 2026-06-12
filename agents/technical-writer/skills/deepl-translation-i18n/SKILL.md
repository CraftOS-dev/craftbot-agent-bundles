---
name: deepl-translation-i18n
description: i18n docs workflow — DeepL API for high-quality machine translation, Crowdin / Lokalise for translator review, per-generator locale routing. Use when shipping multi-language docs.
---

# DeepL + Crowdin / Lokalise — Docs i18n

DeepL is the 2026 SOTA for machine translation quality (still outperforms Google Translate and GPT-class general translation on most language pairs for technical content). Pair with Crowdin or Lokalise when human translators need to review/edit the output.

## When to use this skill

- Translate existing docs into one or more new languages.
- Maintain parity between en docs and translated versions as docs evolve.
- Stand up a translator review workflow.

## Setup

### DeepL via deepl-mcp

```json
// .mcp.json
{
  "mcpServers": {
    "deepl": {
      "command": "npx",
      "args": ["-y", "deepl-mcp"],
      "env": {
        "DEEPL_API_KEY": "<api key from https://www.deepl.com/account>"
      }
    }
  }
}
```

The MCP exposes `translate(text, target_lang, source_lang?)` and batched variants.

### DeepL via REST (fallback)

```bash
curl -X POST 'https://api-free.deepl.com/v2/translate' \
  -H "Authorization: DeepL-Auth-Key $DEEPL_API_KEY" \
  -d 'text=Hello world' \
  -d 'target_lang=FR' \
  -d 'preserve_formatting=1' \
  -d 'tag_handling=html'
```

### Crowdin

```bash
npm i -g @crowdin/cli
echo "
project_id: 'xxxx'
api_token_env: CROWDIN_API_TOKEN

preserve_hierarchy: true

files:
  - source:      docs/**/*.md
    translation: docs/i18n/%locale%/%original_path%/%file_name%.%file_extension%
" > crowdin.yml

# upload sources
crowdin upload sources

# download translations
crowdin download
```

### Lokalise

```bash
npm i -g @lokalise/cli-2
lokalise2 file upload --token "$LOKALISE_TOKEN" --project-id xxxx \
  --file docs/quickstart.md --lang-iso en
lokalise2 file download --token "$LOKALISE_TOKEN" --project-id xxxx \
  --format markdown --unzip-to ./
```

## Common recipes

### Recipe 1: First-time translate a docs tree

```bash
# Source tree: docs/en/**
# Target: docs/i18n/fr/**, docs/i18n/de/**

for src in $(find docs/en -name "*.md"); do
  rel=${src#docs/en/}
  for lang in FR DE ES; do
    out="docs/i18n/${lang,,}/${rel}"
    mkdir -p "$(dirname "$out")"
    # via DeepL REST
    curl -sX POST 'https://api-free.deepl.com/v2/translate' \
      -H "Authorization: DeepL-Auth-Key $DEEPL_API_KEY" \
      --data-urlencode "text@${src}" \
      -d "target_lang=${lang}" \
      -d 'tag_handling=markdown' \
      -d 'preserve_formatting=1' \
      | jq -r '.translations[0].text' > "$out"
  done
done
```

For agent runs, prefer the `deepl-mcp` `translate` tool with `tag_handling: "markdown"`.

### Recipe 2: Keep translations in sync as en docs evolve

Use Crowdin's "Translation Memory" feature:

```bash
crowdin upload sources          # uploads en sources
# Crowdin auto-suggests TM matches for unchanged content
crowdin download                # pulls fresh translations
```

Or, with DeepL only, diff en files and re-translate changed paragraphs:

```bash
git diff --name-only HEAD~1 HEAD -- 'docs/en/**/*.md' | xargs -I{} bash translate.sh {}
```

### Recipe 3: Glossary enforcement

Both DeepL and Crowdin support glossaries:

DeepL glossary:

```bash
curl -X POST 'https://api-free.deepl.com/v2/glossaries' \
  -H "Authorization: DeepL-Auth-Key $DEEPL_API_KEY" \
  -d 'name=acme-en-fr' \
  -d 'source_lang=EN' \
  -d 'target_lang=FR' \
  -d 'entries_format=csv' \
  --data-urlencode 'entries=API,API
SDK,SDK
endpoint,point de terminaison'
```

Then pass `glossary_id` on each translate call.

### Recipe 4: Locale routing per docs generator

| Generator | i18n config |
|---|---|
| **Docusaurus** | `i18n: { defaultLocale: 'en', locales: ['en','fr','de'] }`; files in `i18n/<locale>/docusaurus-plugin-content-docs/current/` |
| **VitePress** | `locales: { root: { lang: 'en' }, fr: { lang: 'fr', link: '/fr/' } }`; files in `fr/**/*.md` |
| **Starlight** | `locales: { en: { label: 'English' }, fr: { label: 'Français' } }`; files in `src/content/docs/<locale>/**` |
| **MkDocs Material** | `i18n` plugin: language suffix `index.fr.md` OR per-language directory |
| **Mintlify** | `"locales": ["en","fr","de"]` in docs.json, translated files in `<locale>/` |

### Recipe 5: GitHub Actions sync workflow

```yaml
# .github/workflows/i18n-sync.yml
name: i18n sync
on:
  push:
    branches: [main]
    paths: ['docs/en/**']
  schedule:
    - cron: '0 6 * * 1'
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: crowdin/github-action@v2
        with:
          upload_sources: true
          download_translations: true
          create_pull_request: true
          pull_request_title: 'i18n: sync from Crowdin'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          CROWDIN_PROJECT_ID: ${{ secrets.CROWDIN_PROJECT_ID }}
          CROWDIN_PERSONAL_TOKEN: ${{ secrets.CROWDIN_TOKEN }}
```

## Quality patterns

- **Always set `tag_handling=markdown`** with DeepL so backticks, code fences, and links survive.
- **Provide glossaries** for product names, technical terms, brand voice phrases.
- **Reuse Translation Memory** — Crowdin/Lokalise pay back the setup cost from translation 2 onward.
- **Mark untranslatable spans** with `<x-trans:no>...</x-trans:no>` (Crowdin) or `<x>...</x>` (Lokalise).
- **Right-to-left languages (Arabic, Hebrew):** verify your CSS supports `dir="rtl"`.
- **Never machine-translate the legal pages** (Terms, Privacy) — flag for human review.

## What the agent flags to the user

- **DeepL API key required:** free tier covers 500k chars/month; paid tier scales.
- **Translation pricing:** DeepL Pro is per character; Crowdin / Lokalise are per-translator-seat (paid) but offer OSS free tiers.
- **Translator review needed for marketing copy:** machine translation suffices for technical content; not for brand voice.
- **Locale parity tracking:** the agent reports en-translations-drift (how many words in en have no translated counterpart).

## Edge cases

- **Code samples in docs:** wrap in fenced blocks; DeepL preserves them with `tag_handling=markdown`.
- **MDX components:** strip JSX before translating, re-attach after. Crowdin does this with the MDX plugin.
- **Right-to-left languages:** test the rendered site in RTL mode; Starlight + Docusaurus support `direction: rtl`.
- **CJK languages:** verify font fallbacks in the docs theme.
- **Per-page translation status:** Docusaurus + Crowdin show a translation badge per page.

## Sources

- DeepL API docs: https://developers.deepl.com/
- deepl-mcp: https://github.com/DeepLcom/deepl-mcp-server (or community equivalent)
- Crowdin docs: https://developer.crowdin.com/
- Crowdin GitHub Action: https://github.com/crowdin/github-action
- Lokalise CLI: https://github.com/lokalise/lokalise-cli-2-go
