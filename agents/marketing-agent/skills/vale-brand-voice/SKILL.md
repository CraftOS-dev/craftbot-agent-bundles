<!--
Source: https://vale.sh/
Vale linter — Go binary, custom YAML rules
-->
# Vale Brand Voice — SKILL

Vale is the SOTA prose linter for technical writing. Custom YAML rules in `styles/Brand/` enforce the marketing-agent's AI-slop catch list ("leverage" → "use", "utilize" → "use", "in today's fast-paced world" → [strip], banned openers, sycophancy hits, stock transitions). Runs in CI on every PR.

## When to use this skill

- **Brand voice enforcement** across all written content (blog, email, social, decks).
- **AI-slop strip** before publishing AI-drafted content (see role.md catch list).
- **CI integration** to block PRs that introduce slop.
- **Multi-brand voice** — separate `styles/<Brand>/` per client / property.
- **Consistency audits** across existing content corpus.

**Do NOT use this skill when:**
- **Grammar / spelling only** — use LanguageTool or write-good.
- **SEO content scoring** — use Surfer SEO / Clearscope.
- **Translation quality** — use DeepL (`deepl-mcp`).

## Setup

### Install (cli-anything via uvx)

```bash
# Modern: uvx Vale wrapper (cross-platform)
uvx vale --version

# Or direct binary (Go, single executable)
brew install vale          # macOS
choco install vale         # Windows
sudo snap install vale     # Linux
```

### Project structure

```
.
├── .vale.ini                    # config (formats, packages, styles paths)
├── styles/
│   ├── Brand/                   # custom brand voice
│   │   ├── AISlop.yml          # AI-slop banned phrases
│   │   ├── BannedOpeners.yml   # opening phrase blocklist
│   │   ├── Sycophancy.yml      # "Great question!" etc.
│   │   ├── CorporateJargon.yml # leverage/utilize/synergize
│   │   ├── StockTransitions.yml # moreover/furthermore overuse
│   │   ├── StyleProblems.yml   # em-dash count, passive voice chains
│   │   └── vocab.txt           # accepted brand terms
│   └── Google/                  # pre-built Google style (via Vale Package Manager)
└── content/
    ├── blog/
    ├── email/
    └── social/
```

### `.vale.ini`

```ini
StylesPath = styles

# Globally accepted vocab (whitelist)
Vocab = Brand

# Minimum severity to trigger
MinAlertLevel = suggestion

# File formats
[*.{md,html,txt}]
BasedOnStyles = Brand, Google

# Markdown-specific: skip code blocks, URLs, file paths
[*.md]
BlockIgnores = (?s)^```.*?```
TokenIgnores = (\b[A-Z]+\b)
```

## Common recipes

### Recipe 1: Run on a single file

```bash
uvx vale content/blog/post.md
# Output: line/col + rule violated + suggestion
```

### Recipe 2: Run on a directory + JSON output (for CI / parsing)

```bash
uvx vale --config=.vale.ini --output=JSON content/blog/ > vale-report.json

# Pretty
jq '.[] | {file: keys[0], errors: map(.Severity == "error") | length, warnings: map(.Severity == "warning") | length}' vale-report.json
```

### Recipe 3: Fail CI on errors

```bash
# Exit non-zero on any errors
uvx vale --minAlertLevel=error content/
echo "Exit: $?"
```

### Recipe 4: Custom rule — banned phrases (existence check)

`styles/Brand/AISlop.yml`:

```yaml
extends: existence
message: "AI slop: '%s' is on the banned list. Cut or rewrite."
level: error
ignorecase: true
tokens:
  - "in today's fast-paced world"
  - "in a world where"
  - "it's no secret that"
  - "look no further than"
  - "without a doubt"
  - "delve into"
  - "embark on a journey"
  - "navigate the complexities"
  - "unlock the power of"
  - "reshape the landscape"
  - "the future is bright"
  - "at the forefront"
  - "level up"
  - "the bottom line is"
  - "in conclusion"
  - "first and foremost"
```

### Recipe 5: Substitution rule — corporate jargon → plain English

`styles/Brand/CorporateJargon.yml`:

```yaml
extends: substitution
message: "Corporate jargon: replace '%s' with '%s'."
level: warning
ignorecase: true
swap:
  leverage: use
  utilize: use
  synergize: cut
  "synergize with": "work with"
  "best-in-class": (cut or be specific)
  "game-changing": (cut or specify the change)
  "cutting-edge": (cut or describe specifics)
  "robust": strong
  "seamless": smooth
  "world-class": (cut)
  "industry-leading": (back with proof or cut)
  "revolutionary": (cut)
  "next-generation": (cut or describe)
  "comprehensive": (be specific)
  "innovative": (describe the innovation)
```

### Recipe 6: Sycophancy + hedging

`styles/Brand/Sycophancy.yml`:

```yaml
extends: existence
message: "Sycophancy: '%s' adds nothing. Cut."
level: error
ignorecase: true
tokens:
  - "great question"
  - "absolutely"
  - "certainly"
  - "happy to help"
  - "i'd love to"
  - "i'm thrilled"
  - "fantastic"
  - "amazing"
  - "wonderful"
```

`styles/Brand/Hedging.yml`:

```yaml
extends: occurrence
message: "Hedging overload. '%s' appears too often."
level: warning
ignorecase: true
max: 3
scope: paragraph
tokens:
  - "may"
  - "might"
  - "could"
  - "perhaps"
  - "possibly"
  - "potentially"
```

### Recipe 7: Em-dash count limit

`styles/Brand/StyleProblems.yml`:

```yaml
extends: occurrence
message: "Too many em-dashes in one paragraph (max 1)."
level: warning
max: 1
scope: paragraph
tokens:
  - "—"
```

### Recipe 8: Auto-fix safe substitutions

```bash
uvx vale --fix content/blog/post.md
```

Only `substitution` rules with non-parenthetical swaps auto-fix.

### Recipe 9: Multi-brand support

```ini
# .vale.ini
StylesPath = styles

[content/clientA/**]
BasedOnStyles = Brand, ClientA

[content/clientB/**]
BasedOnStyles = Brand, ClientB
```

`styles/ClientA/` and `styles/ClientB/` can override severities or add brand-specific terms.

## Examples — CI integration (GitHub Actions)

```yaml
# .github/workflows/vale.yml
name: Vale lint
on:
  pull_request:
    paths:
      - 'content/**'
      - 'styles/**'
      - '.vale.ini'

jobs:
  vale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: errata-ai/vale-action@reviewdog
        with:
          version: 3.4.2
          files: content/
          fail_on_error: true
          token: ${{ secrets.GITHUB_TOKEN }}
          reporter: github-pr-review
```

This:
- Runs Vale on every PR touching `content/`
- Posts inline review comments
- Blocks merge on errors

## Examples — full AI-slop catch ruleset (`styles/Brand/`)

The agent ships these files as bundle defaults; clients override:

```
styles/Brand/
├── AISlop.yml           — banned openers, AI patterns (24 phrases)
├── BannedOpeners.yml    — "In today's fast-paced..." etc.
├── CorporateJargon.yml  — leverage → use (40 swaps)
├── Sycophancy.yml       — "Great question" → cut (15 phrases)
├── StockTransitions.yml — moreover/furthermore overuse limit
├── Hedging.yml          — may/might/could max 3 per paragraph
├── PassiveVoice.yml     — passive ratio > 25% warning
├── EmDash.yml           — max 1 per paragraph
├── ReadingLevel.yml     — Flesch-Kincaid grade target
├── LongSentence.yml     — > 35 words = error
├── DoubleSpace.yml      — error
├── ExclamationMark.yml  — > 1 per paragraph = warning
└── vocab.txt            — accepted brand terms (don't flag as misspellings)
```

`vocab.txt` example:

```
yourbrand
ProductName
TeamName
JargonWeUse
APITerms
```

## Edge cases

### Code blocks + URLs
Vale's `BlockIgnores` skips fenced code blocks. URLs need `TokenIgnores`:

```ini
TokenIgnores = (https?://\S+)
```

### False positives on names
Add to `vocab.txt`. Vale uses case-sensitive matching by default; use `ignorecase: true` in rules to be lenient.

### Severity levels
- `suggestion` — informational, doesn't block CI
- `warning` — yellow flag
- `error` — fails CI with `--minAlertLevel=error`

Use `error` only for non-negotiable rules (AI slop, sycophancy). Use `warning` for style preferences.

### Performance
Vale processes ~1000 files/sec. CI runtime negligible.

### Pre-existing content
First-time rollout: expect 1000s of violations. Auto-fix what's safe, manually review the rest over 2-3 weeks. Or grandfather existing content via `.valeignore`:

```
content/legacy/**
content/old-blog/**
```

### Brand voice vs author voice
Vale enforces house rules — not author style. Guest writers / executives may have signature phrases; whitelist via vocab or `[scope:exclude]` directives.

### Multi-language
Vale supports English best. For BG/FR/DE content, use language-specific styles via `BasedOnStyles` per file. Or run only AISlop rules cross-language.

### Rule debugging
```bash
uvx vale ls-config              # show effective config
uvx vale --no-exit content/    # don't exit on errors, just report
```

### Updating from a community style
```bash
# Sync with Google style guide
uvx vale sync
```

`.vale.ini`:
```ini
Packages = Google, write-good
```

### Substitution suggestions
The `(parenthetical)` swap target in YAML is a human-readable hint shown to the author — Vale won't auto-substitute. Use for "use judgment" cases.

## Sources

- **Vale docs**: https://vale.sh/docs/
- **Vale styles registry**: https://vale.sh/explorer/
- **GitHub Action**: https://github.com/errata-ai/vale-action
- **Existence rule type**: https://vale.sh/docs/topics/styles/#existence
- **Substitution rule**: https://vale.sh/docs/topics/styles/#substitution
- **Occurrence rule**: https://vale.sh/docs/topics/styles/#occurrence
