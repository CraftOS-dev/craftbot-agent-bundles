---
name: content-audit-stale-inaccurate-redundant
description: Three-axis content audit — Stale (last-modified + last-verified), Inaccurate (Lychee link-check + pytest-markdown-docs code-fence + version mismatch), Redundant (simhash/MinHash text similarity). Outputs per-owner action list. Use when CFO/CS asks "is our KB still accurate?"
---

# Content audit — stale, inaccurate, redundant

## When to use

User says "audit our KB", "find stale articles", "broken links", "outdated code samples", "duplicate articles", "merge candidates". Reach BEFORE big restructures and AS recurring quarterly job.

## Setup

```bash
# Lychee link checker (Rust binary, very fast)
brew install lychee
# or
cargo install lychee
# Docker:
docker run --rm -v $(pwd):/data lycheeverse/lychee /data/docs

# pytest-markdown-docs (Modal Labs)
pipx install uv
uv add --dev pytest pytest-markdown-docs

# Simhash for dedup
pip install simhash datasketch

# Frontmatter parsing
pipx install python-frontmatter
```

Auth / API key requirements:
- Optional: `GITHUB_TOKEN` for Lychee to check rate-limited GitHub links
- Optional: site auth headers via `lychee --header "Cookie:..."` for SSO-gated KBs

## Common recipes

### Recipe 1: Stale audit — last-modified > 180d

```bash
NOW=$(date -u +%s)
THRESHOLD=180

find docs -name '*.md' -not -path 'docs/_archived/*' -print0 \
| while IFS= read -r -d '' f; do
  ts=$(git log -1 --format=%ct -- "$f" 2>/dev/null)
  [ -z "$ts" ] && continue
  age=$(( (NOW - ts) / 86400 ))
  if [ "$age" -gt "$THRESHOLD" ]; then
    printf "%s\t%d\n" "$f" "$age"
  fi
done | sort -t$'\t' -k2 -rn > stale-by-modified.tsv
```

### Recipe 2: Stale audit — last-verified > 90d in frontmatter

```python
# scripts/check-verified.py
import pathlib, datetime, frontmatter
THRESHOLD = 90
now = datetime.date.today()
for p in pathlib.Path('docs').rglob('*.md'):
    if '_archived' in p.parts: continue
    post = frontmatter.load(p)
    lv = post.get('last_verified')
    if not lv:
        print(f"{p}\tMISSING last_verified")
        continue
    lv_date = lv if isinstance(lv, datetime.date) else datetime.date.fromisoformat(str(lv))
    age = (now - lv_date).days
    if age > THRESHOLD:
        print(f"{p}\t{age}d since verified")
```

### Recipe 3: Inaccurate — Lychee link check

```bash
# Fast scan with JSON output
lychee --format json --output report.json \
       --max-concurrency 16 \
       --accept 200,206,403 \
       --exclude-mail \
       --no-progress \
       docs/

# Pull failed
jq -r '.fail_map | to_entries[] | .key as $k | .value[] | "\(.url)\t\($k)\t\(.status)"' report.json \
  > broken-links.tsv
```

### Recipe 4: Inaccurate — pytest-markdown-docs

```bash
# Test every Python code-fence in docs/
uvx pytest --markdown-docs docs/ -v --tb=short > pytest-docs.log

# Or: subset to a single file/folder
uvx pytest --markdown-docs docs/how-to/webhooks/
```

Add fence directive to skip:

````markdown
```python notest
# this won't execute under pytest-markdown-docs
print("example only")
```
````

### Recipe 5: Inaccurate — version mismatch

```python
# scripts/version-check.py
import frontmatter, pathlib, json
CURRENT = "2.4.0"  # current product version
for p in pathlib.Path('docs').rglob('*.md'):
    post = frontmatter.load(p)
    declared = post.get('version')
    if declared and declared != CURRENT:
        print(f"{p}\tdeclared={declared}\tcurrent={CURRENT}")
```

### Recipe 6: Redundant — simhash dedup

```python
# scripts/dedup.py
import pathlib
from simhash import Simhash

articles = {}
for p in pathlib.Path('docs').rglob('*.md'):
    if '_archived' in p.parts: continue
    text = p.read_text(encoding='utf-8').lower()
    # normalize: drop frontmatter + headings
    body = '\n'.join(l for l in text.split('\n') if not l.startswith(('---','#')))
    articles[p] = Simhash(body.split())

pairs = []
items = list(articles.items())
for i, (a, ha) in enumerate(items):
    for b, hb in items[i+1:]:
        d = ha.distance(hb)
        if d < 12:  # ~80% sim
            pairs.append((a, b, 1 - d/64))

for a, b, sim in sorted(pairs, key=lambda x: -x[2])[:30]:
    print(f"{sim:.0%}\t{a}\t<->\t{b}")
```

### Recipe 7: Redundant — MinHash (LSH at scale)

```python
# scripts/dedup-lsh.py — for >5000 articles
from datasketch import MinHash, MinHashLSH
import pathlib
lsh = MinHashLSH(threshold=0.8, num_perm=128)
mh_by = {}
for p in pathlib.Path('docs').rglob('*.md'):
    text = p.read_text(encoding='utf-8')
    m = MinHash(num_perm=128)
    for token in text.split():
        m.update(token.encode())
    mh_by[str(p)] = m
    lsh.insert(str(p), m)

seen = set()
for p, m in mh_by.items():
    for cand in lsh.query(m):
        if cand != p and (p, cand) not in seen and (cand, p) not in seen:
            seen.add((p, cand))
            sim = m.jaccard(mh_by[cand])
            print(f"{sim:.0%}\t{p}\t<->\t{cand}")
```

### Recipe 8: Aggregated audit report

```python
# scripts/audit-report.py
from datetime import date
print(f"# KB Audit — {date.today().isoformat()}\n")

print("## Stale (last-modified > 180d)\n")
print("| Article | Days | Owner |\n|---|---|---|")
# read stale-by-modified.tsv, lookup owner from CODEOWNERS, print

print("\n## Inaccurate — broken links\n")
print("| URL | In file | Status |\n|---|---|---|")
# from broken-links.tsv

print("\n## Inaccurate — failing code fences\n")
# from pytest-docs.log

print("\n## Redundant (similarity > 80%)\n")
print("| A | B | Sim | Suggested action |\n|---|---|---|---|")
# from simhash output
```

### Recipe 9: Open GitHub issues for each finding

```bash
while IFS=$'\t' read -r file days; do
  owner=$(python scripts/lookup-owner.py "$file")
  gh issue create \
    --title "Stale KB: $file ($days days)" \
    --body "Owner: $owner. Action: review + re-verify or archive." \
    --label "docs,stale" \
    --assignee "$owner"
done < stale-by-modified.tsv
```

### Recipe 10: CI gate for inaccurate changes

```yaml
# .github/workflows/docs-accuracy.yml
on:
  pull_request:
    paths: ['docs/**']
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: lycheeverse/lychee-action@v1
        with:
          args: --no-progress --format json docs/
          fail: true
      - run: pipx install uv && uv add --dev pytest pytest-markdown-docs
      - run: uvx pytest --markdown-docs docs/
```

### Recipe 11: Quarterly cron + Slack notify

```yaml
# .github/workflows/quarterly-audit.yml
on:
  schedule:
    - cron: '0 6 1 */3 *'   # 1st of every 3rd month
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: bash scripts/run-all-audits.sh > audit.md
      - run: |
          curl -F file=@audit.md \
               -F channels=#docs \
               -F initial_comment="Quarterly KB audit" \
               -H "Authorization: Bearer ${{secrets.SLACK_TOKEN}}" \
               https://slack.com/api/files.upload
```

## Examples

### Example 1: First-time KB audit

**Goal:** Surface what's stale, broken, duplicate.

**Steps:**
1. Run all 3 axes (Recipes 1-2 stale, 3-5 inaccurate, 6-7 redundant).
2. Aggregate (Recipe 8).
3. File owner-assigned issues (Recipe 9).
4. Track owner-side resolution in Notion or GitHub Project.

**Result:** Per-owner action list; ~10-30% of pages typically flagged on first audit.

### Example 2: PR gate for accuracy

**Goal:** Block broken links + failing examples from merging.

**Steps:**
1. Add Recipe 10 CI workflow.
2. Require checks on `main` via branch protection.
3. Allow lint-fix PRs to land without re-running (path-filter).

**Result:** Inaccurate changes can't merge silently.

## Edge cases / gotchas

- **Lychee on rate-limited domains** — GitHub returns 429; configure `--token "$GITHUB_TOKEN"`.
- **Lychee fragment checks** — `--include-fragments` to validate anchors; slower but catches drift.
- **pytest-markdown-docs side effects** — code fences that hit network/credentials need `notest`. Document the convention.
- **Simhash false positives** — common boilerplate (frontmatter, license headers) inflates similarity; strip before hashing.
- **MinHash thresholds** — Jaccard > 0.8 is aggressive; for KB articles 0.6 typically right.
- **Stale ≠ wrong** — evergreen tutorials may not have changed but are still accurate. Owner must verify, not auto-archive.
- **Version frontmatter drift** — multiple maintained versions need per-version trees, not a global `version:`.
- **CODEOWNERS lookup** — last match wins. Lint with `gh api repos/.../codeowners/errors`.
- **Audit-fatigue** — if every quarter flags the same 30%, owners ignore. Track resolution rate; escalate persistently-stale to KB team for archive/merge.
- **Large repos** — full simhash O(n^2); use LSH MinHash above ~3k articles.

## Sources

- Lychee: https://github.com/lycheeverse/lychee
- lychee-action: https://github.com/lycheeverse/lychee-action
- pytest-markdown-docs (Modal): https://github.com/modal-labs/pytest-markdown-docs
- Simhash: https://pypi.org/project/simhash/
- datasketch MinHash LSH: https://ekzhu.com/datasketch/lsh.html
- python-frontmatter: https://python-frontmatter.readthedocs.io/
- GitHub branch protection: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
