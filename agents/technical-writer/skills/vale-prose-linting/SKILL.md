---
name: vale-prose-linting
description: Prose linting with Vale — de facto SOTA for docs-as-code style enforcement. Google + Microsoft + write-good style packs, custom YAML rules, JSON output for CI, organization-specific style packs. Use when enforcing voice / terminology / style across docs.
---

# Vale — Prose Linting

Vale is the standard prose linter for technical documentation. It applies configurable style packs (Google, Microsoft, RedHat, write-good) and custom YAML rules to markdown, MDX, AsciiDoc, reStructuredText, and HTML.

## When to use this skill

- Enforce a style guide across docs (Microsoft Style Guide, Google Developer Documentation Style, etc).
- Maintain terminology consistency (one canonical term per concept).
- Block insensitive or unclear language at PR time.
- Enforce Diátaxis section vocabulary (e.g., no "you'll learn" in reference pages).

## Setup

### Install

```bash
# Linux / macOS
brew install vale
# or release binary
curl -fsSL https://github.com/errata-ai/vale/releases/latest/download/vale_3.x.x_Linux_64-bit.tar.gz | tar xz
sudo mv vale /usr/local/bin/
vale --version
```

### Initialize

```bash
vale ls-config           # show effective config (none yet)
```

Create `.vale.ini` at repo root:

```ini
StylesPath = .vale/styles
MinAlertLevel = suggestion

# Vocabularies — accept project-specific terms not in any style pack
Vocab = MyProject

# Packages to fetch
Packages = Google, Microsoft, write-good, proselint, alex

[*.{md,mdx}]
BasedOnStyles = Vale, Google, write-good
Google.We = error           # error on "we"/"our"
Google.Headings = warning
Microsoft.We = error
write-good.Passive = warning
write-good.TooWordy = warning
write-good.Cliches = warning
alex.ProfanityLikely = error
```

Create vocabulary:

```bash
mkdir -p .vale/styles/config/vocabularies/MyProject/
cat > .vale/styles/config/vocabularies/MyProject/accept.txt <<'EOF'
Anthropic
CraftBot
Mintlify
OAuth
PostgreSQL
TypeScript
EOF
```

Sync style packs:

```bash
vale sync
```

This downloads `Google`, `Microsoft`, `write-good`, `proselint`, and `alex` into `.vale/styles/`. Commit `.vale.ini` and the vocabularies; gitignore `.vale/styles/` (re-fetched via `vale sync`).

## Common recipes

### Recipe 1: One-shot lint

```bash
vale docs/
vale README.md
```

### Recipe 2: JSON output for CI

```bash
vale --output=JSON docs/ > vale-report.json
# Severity counts:
jq '[.[] | .[] | .Severity] | group_by(.) | map({key: .[0], count: length}) | from_entries' vale-report.json
```

### Recipe 3: GitHub Actions integration

```yaml
# .github/workflows/vale.yml
name: Prose
on:
  pull_request:
    paths: ['docs/**', '**/*.md']
jobs:
  vale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: errata-ai/vale-action@reviewdog
        with:
          fail_on_error: true
          reporter: github-pr-review
          filter_mode: added       # only flag new prose
          token: ${{ secrets.GITHUB_TOKEN }}
```

This posts annotations inline on the PR diff.

### Recipe 4: Custom rule — banned terms

`.vale/styles/MyProject/Terms.yml`:

```yaml
extends: substitution
message: 'Use "%s" instead of "%s"'
level: error
ignorecase: true
swap:
  blacklist: blocklist
  whitelist: allowlist
  master: main
  slave: replica
  click here: '<link text describing the destination>'
```

### Recipe 5: Custom rule — Diátaxis section vocabulary

`.vale/styles/Diataxis/TutorialOnly.yml`:

```yaml
extends: existence
message: 'Tutorial sections must use "you" — found instructional voice issue near "%s"'
level: warning
scope:
  - heading.h1
nonword: true
tokens:
  - 'How to'        # how-to-style headings belong in how-to/
```

Activate per-folder via `[docs/tutorials/*.md]` block in `.vale.ini` with `BasedOnStyles = Vale, Diataxis`.

### Recipe 6: Org-specific style pack

Layout:

```
.vale/styles/Acme/
├── meta.json
├── README.md
├── Acceptance.yml       # accept terminology
├── ActiveVoice.yml      # require active voice
├── ProductNames.yml     # canonical product names
└── Substitutions.yml
```

`meta.json`:

```json
{
  "name": "Acme",
  "vale_version": ">=3.0.0",
  "feed": "https://acme.com/vale-rules/feed.json",
  "description": "Acme Inc internal style"
}
```

Distribute via internal Pages site or git submodule. Add to `.vale.ini`:

```ini
Packages = Google, Microsoft, https://acme.com/vale-rules/Acme.zip
```

### Recipe 7: Selective enforcement

```ini
[docs/reference/**/*.md]
BasedOnStyles = Vale, Google
Google.Headings = error

[docs/tutorials/**/*.md]
BasedOnStyles = Vale, Google
Google.Headings = warning      # tutorial headings can be casual

[docs/explanation/**/*.md]
BasedOnStyles = Vale, Google
write-good.Passive = error     # explanation must be active voice
```

### Recipe 8: Vale Server (live IDE integration)

```bash
# install vale-vscode
code --install-extension errata-ai.vale-server
# add to .vscode/settings.json
{
  "vale.valeCLI.path": "/usr/local/bin/vale",
  "vale.valeCLI.config": "${workspaceFolder}/.vale.ini"
}
```

Editors get squiggly lines on style issues in real time.

## Recommended style pack stack

For 80%+ docs projects:

```ini
Packages = Google, write-good, proselint, alex
BasedOnStyles = Vale, Google, write-good
```

- **Google** — modern, developer-focused, widely accepted as the SOTA tech-writing style.
- **Microsoft** — slightly more formal; choose Google OR Microsoft, not both (they conflict).
- **write-good** — passive voice, weasel words, lexical illusions.
- **proselint** — Strunk & White rigor; calibrate severity to `suggestion`.
- **alex** — gender / race / age / religion sensitivity.

## Edge cases

- **MDX (Mintlify / Docusaurus):** Vale parses MDX via the `--filter=md` flag or `.vale.ini` `[*.mdx]` block. Custom JSX components are skipped automatically.
- **Code fences:** Vale skips fenced code by default.
- **Frontmatter:** Vale's `--ignore-syntax` flag skips YAML/TOML frontmatter.
- **Performance on huge repos:** use `--minAlertLevel error` in CI; reserve `warning`/`suggestion` for local dev.
- **False positives on technical terms:** add them to `MyProject/accept.txt` (case-sensitive).
- **Style pack conflicts:** Google and Microsoft are mutually exclusive in many rules. Pick one as the source of truth.

## Sources

- Vale: https://vale.sh/
- Vale GitHub: https://github.com/errata-ai/vale
- Google style pack: https://github.com/errata-ai/Google
- Microsoft style pack: https://github.com/errata-ai/Microsoft
- write-good: https://github.com/errata-ai/write-good
- proselint: https://github.com/errata-ai/proselint
- alex: https://github.com/errata-ai/alex
