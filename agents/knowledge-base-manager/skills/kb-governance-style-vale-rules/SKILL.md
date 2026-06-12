---
name: kb-governance-style-vale-rules
description: KB governance — Vale prose linting (Diataxis + Microsoft + brand-voice styles), markdownlint-cli2 for structure, alex for inclusive language, last-verified stamps, single-source-of-truth enforcement. Use when style is inconsistent, drift across writers, or auditing brand voice.
---

# KB governance — Vale rules, markdownlint, alex, last-verified

## When to use

User says "enforce style", "lint our docs", "inclusive language check", "brand voice consistency", "no duplicate content", "last verified stamp", "doc quality gate". Reach BEFORE merging large content batches and AS PART OF CI for every PR.

## Setup

```bash
# Vale (prose lint)
brew install vale            # macOS
choco install vale           # Windows
# or download release binary from https://github.com/errata-ai/vale/releases

# Markdownlint (structure)
npm i -g markdownlint-cli2

# alex (inclusive language)
npm i -g alex

# Simhash (duplicate detection) for SSOT
pip install simhash datasketch

# Initialize Vale config
vale ls-config        # shows where it's looking
vale sync             # download configured styles
```

Auth / API key requirements: none (all FOSS).

## Common recipes

### Recipe 1: Bootstrap Vale config

```ini
# .vale.ini
StylesPath = .vale/styles
MinAlertLevel = suggestion

Vocab = Brand

Packages = Microsoft, Google, write-good, alex

[*.{md,mdx}]
BasedOnStyles = Vale, Microsoft, Google, write-good, alex, Diataxis, Brand
```

```bash
# Download the style packs
vale sync
```

### Recipe 2: Custom Diataxis style pack

```yaml
# .vale/styles/Diataxis/MixedTier.yml
extends: existence
message: "Diataxis: this looks like a Reference section inside a Tutorial. Split it."
level: warning
scope: heading
ignorecase: true
tokens:
  - 'Reference|API endpoints|All options|Complete list'
```

```yaml
# .vale/styles/Diataxis/TutorialVerbs.yml
extends: existence
message: "Tutorial articles should use guided verbs (Let's, We'll, In this tutorial...)."
level: suggestion
scope: paragraph
tokens:
  - "\\bIn this tutorial\\b|\\bLet's\\b|\\bWe'll\\b"
action: { name: "remove" }
```

### Recipe 3: Brand voice vocab

```bash
mkdir -p .vale/styles/Vocab/Brand
cat > .vale/styles/Vocab/Brand/accept.txt <<'EOF'
Acme
ACME
SaaS
SaaS-native
webhook
OAuth
OpenID
EOF
cat > .vale/styles/Vocab/Brand/reject.txt <<'EOF'
[Bb]lacklist
[Ww]hitelist
[Mm]aster (?!key)
[Ss]lave
EOF
```

### Recipe 4: Run Vale on docs

```bash
vale --output=line docs/                   # human
vale --output=JSON docs/ > vale.json       # machine
vale --output=JSON docs/ | jq -r '.[] | "\(.Line):\(.Severity) \(.Message)"'
```

### Recipe 5: markdownlint-cli2 for structure

```yaml
# .markdownlint-cli2.yaml
config:
  default: true
  MD013: false           # disable line-length (prose docs)
  MD024: { siblings_only: true }   # allow same heading in different sections
  MD041: false           # first line need not be h1 (frontmatter)
  MD033:                 # allow inline HTML for callouts
    allowed_elements: [details, summary, kbd, sup, sub, mark]
globs:
  - "docs/**/*.md"
ignores:
  - "docs/_archived/**"
```

```bash
markdownlint-cli2 "docs/**/*.md"
markdownlint-cli2-fix "docs/**/*.md"   # auto-fix
```

### Recipe 6: alex inclusive language

```bash
npx alex docs/ --quiet
# or per-file
npx alex docs/how-to/authentication/sso-okta.md
```

```yaml
# .alexrc
profile: writing
allow:
  - "host"            # we mean DNS host, not the gender-coded sense
  - "abort"           # technical: process termination
```

### Recipe 7: Single source of truth — duplicate detection

```python
# scripts/dedup-check.py
import pathlib
from simhash import Simhash

articles = {}
for p in pathlib.Path('docs').rglob('*.md'):
    if '_archived' in p.parts:
        continue
    text = p.read_text(encoding='utf-8')
    articles[p] = Simhash(text.split())

dups = []
items = list(articles.items())
for i, (a, ha) in enumerate(items):
    for b, hb in items[i+1:]:
        d = ha.distance(hb)
        if d < 12:   # ~80% similar
            dups.append((a, b, 1 - d/64))

for a, b, sim in sorted(dups, key=lambda x: -x[2]):
    print(f"{sim:.0%}\t{a}\t<->\t{b}")
```

### Recipe 8: Last-verified stamp enforcement

```yaml
# .vale/styles/Brand/LastVerified.yml
extends: script
message: "Article missing 'last_verified' frontmatter, or stamp is >90 days old."
level: warning
script: |
  text := import("text")
  result := []
  if !text.re_match(`(?m)^last_verified:\s+\d{4}-\d{2}-\d{2}`, scope) {
    result = append(result, { begin: 0, end: 1 })
  }
  result
```

### Recipe 9: Frontmatter completeness check

```bash
# Fail PR if missing required frontmatter
for f in $(git diff --name-only origin/main...HEAD -- 'docs/**/*.md'); do
  for key in title slug status owner last_verified; do
    grep -q "^${key}:" "$f" || { echo "::error file=$f::missing $key"; exit 1; }
  done
done
```

### Recipe 10: CI gate (GitHub Actions)

```yaml
# .github/workflows/docs-lint.yml
name: KB lint
on: [pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: errata-ai/vale-action@reviewdog
        with:
          files: docs/
          reporter: github-pr-review
      - run: npm i -g markdownlint-cli2 alex
      - run: markdownlint-cli2 "docs/**/*.md"
      - run: npx alex docs/ --quiet
      - run: pip install simhash && python scripts/dedup-check.py
```

### Recipe 11: Pre-commit hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/errata-ai/vale
    rev: v3.4.2
    hooks:
      - id: vale
        args: [--output=line, docs/]
  - repo: https://github.com/DavidAnson/markdownlint-cli2
    rev: v0.13.0
    hooks:
      - id: markdownlint-cli2
        files: docs/.*\.md$
```

## Examples

### Example 1: Stand up docs-lint CI

**Goal:** Every PR touching `docs/` runs Vale + markdownlint + alex.

**Steps:**
1. Install Vale + create `.vale.ini` (Recipe 1).
2. Add Microsoft + Google + write-good + alex styles via `vale sync`.
3. Author Diataxis style pack (Recipe 2).
4. Add markdownlint config (Recipe 5).
5. Add alex config (Recipe 6).
6. Wire CI job (Recipe 10).
7. Pre-commit hook for fast local feedback (Recipe 11).

**Result:** Style violations caught before merge.

### Example 2: Duplicate-content sweep

**Goal:** 240 articles; ~12% suspected duplicates.

**Steps:**
1. Run `python scripts/dedup-check.py` (Recipe 7).
2. Review pairs with similarity >85%.
3. Pick canonical; redirect the other; archive.
4. Push to `redirects.json`.

**Result:** ~25 articles consolidated; navigation cleaner; SEO improved (canonical signal).

## Edge cases / gotchas

- **Vale style packs version-drift** — pin via `Packages = Microsoft@v0.10.0` once you ship CI.
- **alex false positives** — "abort", "host", "sanity check" trip it in technical docs. Use `.alexrc` allow list.
- **markdownlint MD013 line-length** — disable for prose docs; enforce for code blocks via `MD046`.
- **Simhash on small files** — articles <500 words can falsely group; threshold tuning needed.
- **Vale on MDX** — `*.mdx` works but JSX expressions can confuse tokenizer. Use `[*.{md,mdx}]` and accept noise.
- **Frontmatter check on Windows** — `grep` syntax differs; prefer Python for cross-platform.
- **Pre-commit on huge repos** — full-repo Vale is slow; scope to `git diff --name-only`.
- **CI failures crashing reviewer flow** — start `level: suggestion`, escalate to `warning` after 2 weeks of fixing.
- **Vocab files case-sensitive** — `accept.txt` is literal match unless regex'd.

## Sources

- Vale: https://vale.sh/
- Vale Diataxis-friendly style: https://vale.sh/docs/topics/styles/
- Vale Microsoft Style Guide pack: https://github.com/errata-ai/Microsoft
- markdownlint-cli2: https://github.com/DavidAnson/markdownlint-cli2
- alex: https://alexjs.com/
- Simhash: https://pypi.org/project/simhash/
- vale-action (CI): https://github.com/errata-ai/vale-action
- pre-commit: https://pre-commit.com/
