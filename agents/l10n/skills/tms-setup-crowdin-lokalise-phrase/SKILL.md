---
name: tms-setup-crowdin-lokalise-phrase
description: Stand up a Translation Management System (Crowdin, Lokalise, or Phrase) end-to-end — CLI install, project bootstrap, source upload, GitHub Action sync, OTA delivery. Use when the user asks "set up Crowdin / Lokalise / Phrase" or needs a TMS picked for their team profile.
---

# TMS Setup — Crowdin / Lokalise / Phrase

Three SOTA TMS platforms cover 90% of 2026 production needs: **Crowdin** (dev / OSS default), **Lokalise** (mobile-first), **Phrase** (enterprise + CAT). All expose CLI + REST API + GitHub Action.

## When to use

- The user is starting fresh and needs a TMS picked.
- The user has a TMS account but needs CI sync wired (GitHub Action).
- The user is migrating between TMS platforms.
- The user wants Over-The-Air (OTA) string delivery for mobile / RN.

Trigger phrases: "set up Crowdin", "wire Lokalise GitHub Action", "Phrase Strings vs Phrase TMS", "OTA strings to iOS", "migrate from Crowdin to Phrase", "which TMS for my team".

## Setup

### Pick the right TMS first

| Team profile | Recommend | Why |
|---|---|---|
| Dev team, OSS, mostly UI strings | Crowdin | Free for OSS, AI translation bundled, best Git integration |
| Mobile-first (iOS + Android + RN) | Lokalise | OTA SDK + Figma plugin + screenshot context |
| Enterprise (SOC 2, LSP-managed, mixed content) | Phrase | Phrase Strings + Phrase TMS combined; audit logs; vendor routing |
| Self-hosted / data sovereignty | Weblate (out of this pack) | OSS, runs on own hardware |

### Install CLIs

```bash
# Crowdin
npm i -g @crowdin/cli
crowdin --version

# Lokalise (CLI v2 — Go binary)
npm i -g @lokalise/cli-2
lokalise2 --version
# Or via brew on macOS: brew tap lokalise/cli-2 && brew install lokalise2

# Phrase
npm i -g @phrase/cli
phrase --version
```

### Auth / env vars

- `CROWDIN_PROJECT_ID` + `CROWDIN_PERSONAL_TOKEN` — from `https://crowdin.com/profile/api-tokens`
- `LOKALISE_API_TOKEN` — from `https://app.lokalise.com/profile#apitokens`
- `PHRASE_TOKEN` — from `https://app.phrase.com/settings/oauth_access_tokens`

Free tiers: Crowdin free for OSS (unlimited); Lokalise free trial (14 days); Phrase free trial.

## Common recipes

### Recipe 1: Crowdin — bootstrap a new project

```bash
crowdin init                            # interactive — creates crowdin.yml
# Or write crowdin.yml manually:
cat > crowdin.yml <<'EOF'
project_id_env: CROWDIN_PROJECT_ID
api_token_env: CROWDIN_PERSONAL_TOKEN
preserve_hierarchy: true
files:
  - source: locales/en.json
    translation: locales/%two_letters_code%.json
EOF

crowdin upload sources                  # push en.json to Crowdin
crowdin upload translations -l de       # push existing de.json to TM
crowdin download                        # pull all translated locales
crowdin status                          # see per-locale completion %
```

### Recipe 2: Crowdin GitHub Action (PR-based locale sync)

```yaml
# .github/workflows/crowdin.yml
name: Crowdin Sync
on:
  push:
    branches: [main]
    paths: ['locales/en.json']
  schedule:
    - cron: '0 0 * * *'
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: crowdin/github-action@v2
        with:
          upload_sources: true
          upload_translations: false
          download_translations: true
          localization_branch_name: l10n_main
          create_pull_request: true
          pull_request_title: 'i18n: locale updates from Crowdin'
          pull_request_labels: 'i18n,crowdin'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          CROWDIN_PROJECT_ID: ${{ secrets.CROWDIN_PROJECT_ID }}
          CROWDIN_PERSONAL_TOKEN: ${{ secrets.CROWDIN_PERSONAL_TOKEN }}
```

### Recipe 3: Crowdin OTA — React Native

```bash
npm i @crowdin/ota-client
# Generate OTA distribution
crowdin distribution add --name production --target-language all
# Get hash → app config
```

```ts
import OtaClient from '@crowdin/ota-client';
const client = new OtaClient('your-distribution-hash');
const strings = await client.getStringsByLocale('de');
```

### Recipe 4: Lokalise — upload + download

```bash
# Upload source
lokalise2 file upload \
  --token "$LOKALISE_API_TOKEN" --project-id $LOKALISE_PROJECT_ID \
  --file=locales/en.json --lang-iso=en --replace-modified

# Download all locales
lokalise2 file download \
  --token "$LOKALISE_API_TOKEN" --project-id $LOKALISE_PROJECT_ID \
  --format=json --bundle-structure='%LANG_ISO%.json' \
  --unzip-to=./locales/

# Check project keys count
lokalise2 key list --token "$LOKALISE_API_TOKEN" --project-id $LOKALISE_PROJECT_ID --limit 5000
```

### Recipe 5: Lokalise GitHub Action

```yaml
# .github/workflows/lokalise.yml
name: Lokalise Sync
on:
  push:
    branches: [main]
    paths: ['locales/en.json']
jobs:
  push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: lokalise/lokalise-push-action@v3
        with:
          api_token: ${{ secrets.LOKALISE_API_TOKEN }}
          project_id: ${{ secrets.LOKALISE_PROJECT_ID }}
          translations_path: |
            locales
          file_format: json
          base_lang: en
```

### Recipe 6: Lokalise OTA SDK (iOS / Android / RN)

```ts
// React Native
import { LokaliseRN } from '@lokalise/react-native-ota-sdk';
LokaliseRN.init('<sdk-token>', '<project-id>');
await LokaliseRN.updateTranslations();
```

```swift
// iOS
import LokaliseSDK
Lokalise.shared.setProjectID("<project-id>", token: "<sdk-token>")
Lokalise.shared.updateTranslations { _, _ in }
```

### Recipe 7: Phrase Strings — init + push/pull

```bash
phrase init                             # interactive — creates .phrase.yml
# Manual config:
cat > .phrase.yml <<'EOF'
phrase:
  access_token: <PHRASE_TOKEN>
  project_id: <PROJECT_ID>
  file_format: json
  push:
    sources:
      - file: locales/en.json
        params:
          locale_id: <EN_LOCALE_ID>
          tags: ui
  pull:
    targets:
      - file: locales/<locale_name>.json
EOF

phrase push                             # upload sources
phrase pull                             # download all locales
phrase locales list                     # check locale IDs
```

### Recipe 8: Phrase GitHub Action

```yaml
# .github/workflows/phrase.yml
name: Phrase Sync
on:
  push:
    branches: [main]
jobs:
  sync:
    runs-on: ubuntu-latest
    container: ghcr.io/phrase/phrase-cli:latest
    steps:
      - uses: actions/checkout@v4
      - run: phrase push
      - run: phrase pull
        env:
          PHRASE_ACCESS_TOKEN: ${{ secrets.PHRASE_TOKEN }}
```

### Recipe 9: Cross-platform — convert JSON ↔ XLIFF for LSP handoff

```bash
# All three TMS export XLIFF
crowdin download translations --export-only-approved --format xliff
lokalise2 file download --token "$LOKALISE_API_TOKEN" --project-id $PID --format=xliff
phrase pull --target='locales/<locale_name>.xliff'

# Convert back to JSON locally
pipx install okapi-tools
tikal -2json input.xlf
```

### Recipe 10: Quick TMS health check (CI gate)

```bash
# Crowdin — fail PR if translation < 80% per locale
crowdin status --json | jq -e '
  .[] | select(.translationProgress < 80) |
  "Locale \(.languageId) is \(.translationProgress)% translated"' && exit 1 || exit 0
```

## Examples

### Example 1: Bootstrap Crowdin for an OSS React app from scratch

**Goal:** Take a fresh React app with one `locales/en.json`, get translations for de/fr/ja/ar flowing via PR.

**Steps:**
1. `npm i -g @crowdin/cli`
2. Create the Crowdin project at `crowdin.com/projects/create`; collect `PROJECT_ID` + create personal token.
3. `crowdin init` → answer prompts, choose JSON format, set `locales/en.json` as source.
4. `crowdin upload sources` → confirm en.json appears in Crowdin web UI.
5. Add target languages in Crowdin UI: de, fr, ja, ar.
6. Drop the GitHub Action in `.github/workflows/crowdin.yml` (Recipe 2).
7. Add `CROWDIN_PROJECT_ID` and `CROWDIN_PERSONAL_TOKEN` to repo secrets.
8. Translate first batch with Crowdin AI (free for OSS) or invite translators.
9. Wait for the bot PR titled "i18n: locale updates from Crowdin" — review + merge.

**Result:** `locales/de.json`, `locales/fr.json`, `locales/ja.json`, `locales/ar.json` land in repo; nightly cron keeps them in sync.

### Example 2: Mobile-first team picks Lokalise for OTA delivery

**Goal:** iOS + Android + React Native ship strings without app-store resubmits.

**Steps:**
1. Create Lokalise project with three platforms (iOS / Android / RN).
2. Upload `Localizable.strings`, `strings.xml`, `en.json` via `lokalise2 file upload` (Recipe 4).
3. Generate OTA SDK token in Lokalise project settings.
4. Wire OTA SDK in each app (Recipe 6).
5. Add `lokalise-push-action` in CI (Recipe 5) for source-of-truth push.
6. Translators edit in Lokalise web UI; updates ship to apps via OTA without redeploy.

**Result:** String updates appear in production apps within seconds; no Apple/Google review cycle.

## Edge cases / gotchas

- **Crowdin free OSS tier** — requires GitHub repo to be public; verify via Crowdin's OSS verification form. Paid tier required for private repos.
- **Lokalise CLI v1 deprecated** — old `lokalise` (v1, Node) is dead; always use `lokalise2` (Go binary, v2).
- **Phrase Strings vs Phrase TMS** — Strings is the lightweight key/value TMS; TMS (formerly Memsource) is the enterprise CAT. They share a portal but have separate CLIs and pricing.
- **GitHub Action token scope** — Crowdin/Lokalise/Phrase actions all need a `GITHUB_TOKEN` with `contents: write` and `pull-requests: write` on PR-creating workflows. Add to `permissions:` block.
- **OTA delivery has a CDN propagation delay** — Crowdin OTA hashes are cached up to 5 minutes; Lokalise OTA propagates within ~30s.
- **JSON nesting vs flat** — Crowdin and Lokalise both handle nested JSON, but ICU pluralization keys must use dot notation (`cart.items.{count, plural, ...}`), not nested objects. Configure via `escape_quotes` flag.
- **Rate limits** — Crowdin API: 60 req/min/token. Lokalise: 6 req/sec. Phrase: 10 req/sec on starter, higher on enterprise.
- **Source file size** — Lokalise free tier capped at 1000 keys; Phrase free at 1500; Crowdin OSS unlimited.
- **Pseudo-locale support** — Crowdin uses `ach`; Lokalise uses `qps-ploc`; Phrase uses custom locales — each TMS has different conventions (see `pseudo-localization` skill).
- **Approval workflow** — `--export-only-approved` (Crowdin) and `--filter-data='translated'` (Lokalise) prevent shipping unreviewed strings.

## Sources

- Crowdin CLI: https://github.com/crowdin/crowdin-cli
- Crowdin GitHub Action: https://github.com/crowdin/github-action
- Lokalise CLI v2: https://github.com/lokalise/lokalise-cli-2-go
- Lokalise Push Action: https://github.com/lokalise/lokalise-push-action
- Phrase CLI: https://github.com/phrase/phrase-cli
- Phrase docs: https://support.phrase.com/hc/en-us
- Comparison: https://intlpull.com/blog/lokalise-vs-phrase-vs-crowdin-2026
- TMS market 2026: https://better-i18n.com/en/i18n/best-tms/
