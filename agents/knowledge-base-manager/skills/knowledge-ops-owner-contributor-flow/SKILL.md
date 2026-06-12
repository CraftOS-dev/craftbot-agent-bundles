---
name: knowledge-ops-owner-contributor-flow
description: KB knowledge-ops — RACI matrix per content area, named owner per article/section, contributor leaderboard, owner pings via Slack. Use when ownership is fuzzy, contributors don't know what to write, or accountability is missing.
---

# Knowledge ops — owner / contributor flow

## When to use

User says "who owns this doc?", "set up RACI for docs", "build contributor leaderboard", "ping owner on stale", "CODEOWNERS for docs", "Notion db for doc owners". Reach BEFORE content-review-cadence (owners must exist before pings have a recipient).

## Setup

```bash
# Notion (RACI database) — already covered via notion-mcp
# Slab Team Owner — set in workspace settings UI
# Git: CODEOWNERS or OWNERS.md
# Quick install:
brew install gh
gh auth login
```

Auth / API key requirements:
- `NOTION_TOKEN` — for RACI database
- `SLACK_BOT_TOKEN` — `chat:write` scope for owner pings
- `GITHUB_TOKEN` — for CODEOWNERS automation

## Common recipes

### Recipe 1: Create RACI Notion database

```bash
curl -X POST "https://api.notion.com/v1/databases" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent":{"page_id":"'"$PARENT_PAGE"'"},
    "title":[{"text":{"content":"KB RACI"}}],
    "properties":{
      "Content area":{"title":{}},
      "Responsible":{"people":{}},
      "Accountable":{"people":{}},
      "Consulted":{"people":{}},
      "Informed":{"people":{}},
      "Article count":{"number":{"format":"number"}},
      "Last reviewed":{"date":{}},
      "Slack channel":{"rich_text":{}}
    }
  }'
```

### Recipe 2: Upsert content-area RACI row

```bash
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent":{"database_id":"'$DB_ID'"},
    "properties":{
      "Content area":{"title":[{"text":{"content":"Authentication / SSO"}}]},
      "Responsible":{"people":[{"id":"alice-user-id"}]},
      "Accountable":{"people":[{"id":"eng-mgr-user-id"}]},
      "Consulted":{"people":[{"id":"security-team-id"}]},
      "Slack channel":{"rich_text":[{"text":{"content":"#docs-auth"}}]}
    }
  }'
```

### Recipe 3: Git CODEOWNERS for docs

```bash
# .github/CODEOWNERS
cat > .github/CODEOWNERS <<'EOF'
# Knowledge base ownership
docs/how-to/authentication/ @alice @security-team
docs/how-to/webhooks/       @bob
docs/how-to/billing/        @carol @finance-team
docs/reference/api/         @api-team
docs/concept/               @architects
EOF

git add .github/CODEOWNERS
git commit -m "docs: add CODEOWNERS for KB sections"
```

### Recipe 4: Alternative OWNERS.md per directory

```bash
# docs/how-to/authentication/OWNERS.md
cat > docs/how-to/authentication/OWNERS.md <<'EOF'
# Owners — Authentication
- **Owner:** Alice Chen (@alice on Slack, alice@example.com)
- **Reviewers:** @security-team
- **Backup:** Bob Singh (@bob)
- **Domain SME:** @cto

Touch this folder = ping owner via PR review request.
EOF
```

### Recipe 5: Slab Team Owner (workspace setting)

In Slab UI: Settings → Teams → Create Team → Add Members → Assign Team Owner per top-level area.

```bash
# Slab REST API
curl -X POST "https://api.slab.com/v1/graphql" \
  -H "Authorization: $SLAB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"mutation{addUserToTeam(teamId:\"team-uuid\", userId:\"user-uuid\", role:OWNER){id}}"}'
```

### Recipe 6: Slack owner-ping for stale article

```bash
OWNER_USER_ID=$(jq -r --arg email "alice@example.com" \
  '.members[] | select(.profile.email==$email).id' < slack-users.json)

curl -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"channel\":\"$OWNER_USER_ID\",
    \"text\":\"Stale KB article needs your eyes: docs/how-to/sso-okta.md (last verified 184d ago). Review: https://docs.example.com/how-to/sso-okta\"
  }"
```

### Recipe 7: Contributor leaderboard from git log

```bash
# Top contributors to docs/ in last 90 days
git log --since="90 days ago" --pretty=format:"%an" -- docs/ \
  | sort | uniq -c | sort -rn | head -10
```

### Recipe 8: Auto-update RACI row on each commit

```yaml
# .github/workflows/raci-sync.yml
on:
  push:
    paths: ['docs/**']
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          # parse changed docs paths → find owner from CODEOWNERS → push to Notion
          git diff --name-only HEAD~1 -- docs/ | python sync-raci.py
        env:
          NOTION_TOKEN: ${{ secrets.NOTION_TOKEN }}
```

### Recipe 9: Monthly leaderboard post

```bash
LEADERS=$(git log --since="30 days ago" --pretty=format:"%an" -- docs/ \
  | sort | uniq -c | sort -rn | head -5 \
  | awk '{printf "%s. %s — %d commits\\n", NR, $2, $1}')

curl -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -d "{\"channel\":\"#docs\", \"text\":\"📚 KB Contributor Leaderboard — June 2026\\n$LEADERS\"}"
```

### Recipe 10: Query "who owns this path?"

```bash
# Check CODEOWNERS for a path
gh api repos/$ORG/$REPO/codeowners/errors

# Or parse locally
git ls-files docs/how-to/authentication/sso-okta.md \
  | xargs python -c "
import sys, re, pathlib
co = pathlib.Path('.github/CODEOWNERS').read_text()
for line in co.splitlines():
    if not line.strip() or line.startswith('#'): continue
    pat, *owners = line.split()
    if any(p in sys.argv[1] for p in [pat.lstrip('/')]):
        print(' '.join(owners))
"
```

## Examples

### Example 1: Bootstrap RACI for 50-section internal wiki

**Goal:** No owners; nobody knows who to ask.

**Steps:**
1. Create RACI Notion database (Recipe 1).
2. Workshop 1-hr session: 50 sections → assign Owner / Approver / Consulted.
3. Bulk upsert via Notion API (Recipe 2).
4. Mirror in `OWNERS.md` per directory (Recipe 4).
5. Set up monthly owner-ping cadence (Recipe 6).

**Result:** Every section has a named owner; staleness pings land in the right inbox.

### Example 2: Git-backed CODEOWNERS + leaderboard

**Goal:** Reward contributors; surface ownership in PR review.

**Steps:**
1. Write CODEOWNERS for `docs/**` (Recipe 3).
2. Enable required code-owner review in GitHub branch protection.
3. Monthly cron → post leaderboard to #docs (Recipes 7, 9).
4. Top 3 contributors get $25 swag credit (out-of-skill).

**Result:** PRs auto-request the right reviewer; contributors see recognition.

## Edge cases / gotchas

- **CODEOWNERS pattern precedence** — last match wins, not first. Lint with `gh api repos/.../codeowners/errors`.
- **Notion people property** requires invited user IDs — external SMEs need workspace access first.
- **Slab Team Owner** is workspace-level; individual articles inherit. Override per-page is paid Slab Premium only.
- **Owner attrition** — leavers leave orphan articles. Monthly job: cross-reference Slack/HR with RACI; flag orphans.
- **Approver vs Owner** — keep separate. Owner does the work; Approver gates the PR.
- **Avoid teams-as-owners on CODEOWNERS** unless team has Issues notifications enabled (else ping goes to /dev/null).
- **Don't over-shard ownership** — 1 owner per section beats 5 reviewers per article (no clear accountability).
- **Stale RACI** — RACI itself goes stale. Quarterly review.

## Sources

- RACI matrix guide (Atlassian): https://www.atlassian.com/work-management/project-management/raci-chart
- CODEOWNERS: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- Notion DB API: https://developers.notion.com/reference/post-database-query
- Slab Teams: https://slab.com/help/teams
- Slack chat.postMessage: https://api.slack.com/methods/chat.postMessage
- Slab API: https://docs.slab.com/developers
