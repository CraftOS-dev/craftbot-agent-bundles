<!--
Sources:
git-cliff — https://git-cliff.org
Conventional commits — https://www.conventionalcommits.org
Linear cycle reports — https://linear.app/docs/cycles
-->
# Release Notes + Changelog Automation — SKILL

git-cliff converts conventional commits to a structured changelog; Linear cycle reports give the product-facing release notes. This pack chains both, publishes to a Notion changelog DB, and broadcasts via Gmail + Slack.

## When to use

- Generating the engineering changelog from git history at end of cycle.
- Writing customer-facing release notes from completed Linear issues.
- Publishing to a versioned Notion changelog database.
- Broadcasting "what shipped this week/month" via email + Slack.
- Aggregating cycle-over-cycle improvements for the quarterly review.

Trigger phrases: "generate release notes", "what shipped this cycle", "publish the changelog", "monthly release email", "cut a release".

## Setup

```bash
# git-cliff — Rust binary; install via cargo OR pre-built release
cargo install git-cliff
# OR (macOS)
brew install git-cliff
# OR (npm)
npx -y git-cliff@latest --help
```

Auth (no auth for git-cliff itself; uses local git):
- Linear API: `LINEAR_API_KEY` — see `linear-product-management` skill.
- Gmail/Slack: covered by their MCPs.
- Notion: `NOTION_API_KEY` — see `notion-prds-roadmaps`.

## Common recipes

### Recipe 1: Bootstrap git-cliff config

```bash
git cliff --init
# Writes cliff.toml with conventional-commits parsing
```

Default `cliff.toml`:

```toml
[changelog]
header = """
# Changelog
"""
body = """
{% for group, commits in commits | group_by(attribute="group") %}
### {{ group | upper_first }}
{% for commit in commits %}
- {{ commit.message | upper_first }}\
  {% if commit.scope %}({{ commit.scope }}){% endif %}\
   ([{{ commit.id | truncate(length=7, end="") }}])
{% endfor %}
{% endfor %}
"""

[git]
conventional_commits = true
filter_unconventional = true
commit_parsers = [
  { message = "^feat", group = "Features" },
  { message = "^fix", group = "Bug Fixes" },
  { message = "^perf", group = "Performance" },
  { message = "^refactor", group = "Refactoring" },
  { message = "^docs", group = "Documentation" },
  { message = "^chore", skip = true },
]
```

### Recipe 2: Generate the engineering changelog

```bash
# Last tag → HEAD
git cliff --latest --output CHANGELOG-eng.md

# Specific range
git cliff v2.3.0..v2.4.0 --output CHANGELOG-v2.4.0.md

# Tag-and-changelog in one shot
git cliff --tag v2.4.0 --output CHANGELOG.md
git tag v2.4.0
```

### Recipe 3: Pull product-facing notes from Linear

```bash
# All issues completed in cycle 27 (which becomes the user-facing release notes)
mcp tool linear.list_issues \
  --filter '{"cycle":{"id":{"eq":"<cycle-27-id>"}},"state":{"type":{"eq":"completed"}}}' \
  --first 100 \
| jq -r '.nodes[] | "- **\(.title)** — \(.description | split("\n")[0] // "Shipped")\n  - Issue: \(.url)"' \
> release-product.md
```

### Recipe 4: Merge eng + product notes into a single release post

```bash
cat > release-2026-06-09.md <<'EOF'
# Release — week of 2026-06-09

## What's new for you
EOF
cat release-product.md >> release-2026-06-09.md

cat >> release-2026-06-09.md <<'EOF'

---

## For engineers (technical changelog)
EOF
cat CHANGELOG-eng.md >> release-2026-06-09.md
```

### Recipe 5: Publish to Notion changelog database

```bash
mcp tool notion.create_page \
  --parent '{"database_id":"<changelog-db>"}' \
  --properties '{
    "Version":{"title":[{"text":{"content":"Release 2026-06-09"}}]},
    "Date":{"date":{"start":"2026-06-09"}},
    "Cycle":{"select":{"name":"Cycle 27"}},
    "Type":{"multi_select":[{"name":"Feature"},{"name":"Fix"}]}
  }' \
  --children '[
    ... (parse release-2026-06-09.md into blocks)
  ]'
```

### Recipe 6: Email broadcast via Gmail

```bash
mcp tool gmail.send \
  --to "customers@your-list.com" \
  --bcc "<customer-list>" \
  --subject "What's new — week of June 9" \
  --body "$(cat release-product.md)"
```

### Recipe 7: Slack broadcast

```bash
mcp tool slack.post \
  --channel "#product-updates" \
  --text "📦 Release shipped — cycle 27. See: https://www.notion.so/changelog/release-2026-06-09"
```

### Recipe 8: Filter Linear by "release-worthy" label only

Not every completed issue is customer-facing. Use a label:

```bash
# Set up team convention: `release-worthy` label on issues that go in customer-facing notes
mcp tool linear.list_issues \
  --filter '{
    "cycle":{"id":{"eq":"<cycle-27-id>"}},
    "state":{"type":{"eq":"completed"}},
    "labels":{"name":{"eq":"release-worthy"}}
  }'
```

### Recipe 9: Conventional commit lint (pre-commit hook)

```bash
# Reject non-conventional commits via commitlint
npm i -g @commitlint/cli @commitlint/config-conventional

# .commitlintrc.json
echo '{"extends":["@commitlint/config-conventional"]}' > .commitlintrc.json

# .husky/commit-msg
npx husky add .husky/commit-msg 'npx commitlint --edit "$1"'
```

This ensures git-cliff always has clean conventional commits to parse.

### Recipe 10: Quarterly digest

```bash
# Roll up the last 3 cycles into a single quarterly release email
CYCLE_IDS=$(mcp tool linear.list_cycles --teamKey "PROD" --first 3 | jq -r '.nodes[].id' | tr '\n' ',')

mcp tool linear.list_issues \
  --filter "{\"cycle\":{\"id\":{\"in\":[\"${CYCLE_IDS%,}\"]}},\"state\":{\"type\":{\"eq\":\"completed\"}},\"labels\":{\"name\":{\"eq\":\"release-worthy\"}}}" \
  --first 200 \
| jq -r '
  .nodes
  | group_by(.labels.nodes[]? | select(.name | startswith("theme-")).name)
  | .[]
  | "## \(.[0].labels.nodes[]? | select(.name | startswith("theme-")).name | sub("theme-";""))\n\(map("- \(.title)") | join("\n"))"
'
```

## Examples

### Example 1: End-of-cycle release flow
**Goal:** Cycle 27 ended; publish the release.

**Steps:**
1. Engineering: tag the release (`git tag v2.4.0 && git push --tags`).
2. Run `git cliff --tag v2.4.0` (Recipe 2) for engineering changelog.
3. Pull product-facing notes from Linear (Recipe 3).
4. Merge into release post (Recipe 4).
5. Publish to Notion changelog DB (Recipe 5).
6. Email customer list (Recipe 6).
7. Slack #product-updates (Recipe 7).

**Result:** Versioned changelog in git + Notion + customer comms in one shot.

### Example 2: Quarterly product newsletter
**Goal:** Roll up Q3 shipping into a single customer email.

**Steps:**
1. Pull last 6 cycles' release-worthy issues (Recipe 10).
2. Group by theme labels (e.g., `theme-onboarding`, `theme-analytics`).
3. Format as a 1-2 paragraph "what we shipped this quarter."
4. Distribute via Gmail batch + post to Notion blog DB.

**Result:** Customers see momentum; sales gets enablement material.

## Edge cases / gotchas

- **Conventional commits required.** If the team doesn't follow `feat:` / `fix:` / `perf:`, git-cliff produces a noisy or empty changelog. Recipe 9 enforces.
- **First-release problem.** `git cliff --latest` needs at least one prior tag. For initial release: `git cliff --unreleased`.
- **Linear states != "release-worthy".** Plenty of completed issues are internal. Use a label (Recipe 8) to filter.
- **Multi-team Linear.** If multiple teams share a cycle, filter by `team` in `list_issues`.
- **Notion blocks > 2000 chars.** Long release notes need block splitting; use `markdown-converter` skill to chunk.
- **Email deliverability.** Bulk customer email via Gmail rate-limits at ~500/day. Use Klaviyo for >1k recipients (defer to `marketing-agent`).
- **Versioning convention.** SemVer (v2.4.0) vs CalVer (2026.06.09) vs cycle-numbered (cycle-27). Pick once; stick.
- **Don't mix internal + external in one email.** Engineering changelog has refactors/internal tooling that confuse customers. Keep separate.
- **Conventional commit scopes.** Use `feat(onboarding): ...` to give git-cliff grouping; otherwise everything lumps under "Features."
- **Breaking changes.** Conventional commits flag breaking changes with `!` (e.g., `feat!: rename API`). Surface these prominently in release notes.

## Sources

- [git-cliff docs](https://git-cliff.org)
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0)
- [Semantic Versioning](https://semver.org)
- [commitlint](https://commitlint.js.org)
- [Linear cycle reports](https://linear.app/docs/cycles)
- [Notion changelog DB pattern (Lenny)](https://www.lennysnewsletter.com/p/changelog-best-practices)
- [Husky pre-commit hooks](https://typicode.github.io/husky)
