---
name: content-lifecycle-draft-review-publish-archive
description: Content lifecycle — 5-state workflow (Draft → In Review → Published → Stale → Archived) automated in Notion (Status + DB automation), Confluence (Page Approvals), Document360 (Workflows), and git (GitHub Actions stale-bot). Use when articles go stale, publish gate is missing, or status is invisible.
---

# Content lifecycle — Draft → Review → Publish → Stale → Archive

## When to use

User says "articles go stale", "no publish gate", "we need approval workflow", "Slack me when an article is stale", "set up a docs status column", "what's draft vs published". Reach BEFORE building review cadence (this skill defines the states; cadence skill schedules the checks).

Defer multi-system approval (Jira tickets → KB status) to `operations-agent`.

## Setup

```bash
# Notion: enable Database automation in workspace settings
# Confluence: install Page Approvals app from Atlassian Marketplace
# Document360: built-in (paid; Pro tier+)
# Git-backed: GitHub stale Action
npm i -g @notionhq/client
pipx install notion-py
```

Auth / API key requirements:
- `NOTION_TOKEN` — Notion integration token; share the DB with the integration
- `CONFLUENCE_USER` + `CONFLUENCE_API_TOKEN` — atlassian.com → API tokens
- `DOCUMENT360_API_TOKEN` — Document360 settings → API tokens
- `GITHUB_TOKEN` — repo scope for Actions

## Common recipes

### Recipe 1: Notion — add Status property + automation

```bash
# Add Status property (single-select)
curl -X PATCH "https://api.notion.com/v1/databases/$DB_ID" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "Status": {
        "status": {
          "options": [
            {"name":"Draft","color":"gray"},
            {"name":"In Review","color":"yellow"},
            {"name":"Published","color":"green"},
            {"name":"Stale","color":"orange"},
            {"name":"Archived","color":"red"}
          ]
        }
      },
      "Last Verified": {"date": {}},
      "Owner": {"people": {}}
    }
  }'
```

Then in Notion UI: Database → Automations → "When Status = Stale, send Slack message to Owner".

### Recipe 2: Notion — transition Draft → In Review

```bash
curl -X PATCH "https://api.notion.com/v1/pages/$PAGE_ID" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"properties":{"Status":{"status":{"name":"In Review"}}}}'
```

### Recipe 3: Notion — stamp Last Verified on publish

```bash
curl -X PATCH "https://api.notion.com/v1/pages/$PAGE_ID" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "{
    \"properties\":{
      \"Status\":{\"status\":{\"name\":\"Published\"}},
      \"Last Verified\":{\"date\":{\"start\":\"$(date -u +%F)\"}}
    }
  }"
```

### Recipe 4: Confluence — set Page Property for status

```bash
# Add page property
curl -X POST "https://${SITE}.atlassian.net/wiki/rest/api/content/${PAGE_ID}/property" \
  -u "$CONFLUENCE_USER:$CONFLUENCE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key":"kb-status","value":{"status":"Published","last_verified":"2026-06-09","owner":"alice@example.com"}}'

# Update existing
curl -X PUT "https://${SITE}.atlassian.net/wiki/rest/api/content/${PAGE_ID}/property/kb-status" \
  -u "$CONFLUENCE_USER:$CONFLUENCE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"value":{"status":"Stale"},"version":{"number":2}}'
```

### Recipe 5: Confluence — Page Approvals trigger

Approvals app exposes REST. To request approval:

```bash
curl -X POST "https://${SITE}.atlassian.net/wiki/rest/approvals-api/approval" \
  -u "$CONFLUENCE_USER:$CONFLUENCE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"contentId":"'$PAGE_ID'","approvers":["account-id-of-sme"]}'
```

### Recipe 6: Document360 — set workflow stage

```bash
# Document360 v2 API — categories + articles
curl -X PUT "https://apihub.document360.io/v2/Articles/$ARTICLE_ID" \
  -H "api_token: $DOCUMENT360_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"workflow_status":"Published","language_code":"en"}'
```

### Recipe 7: GitBook — content versioning + page state

```bash
# GitBook API v1 — promote from change request to published
curl -X POST "https://api.gitbook.com/v1/spaces/$SPACE_ID/change-requests/$CR_ID/merge" \
  -H "Authorization: Bearer $GITBOOK_TOKEN"
```

### Recipe 8: Git-backed — frontmatter status

```yaml
---
title: SSO with Okta
slug: how-to/authentication/sso-okta
status: published        # draft | in-review | published | stale | archived
owner: alice@example.com
last_verified: 2026-06-09
diataxis: how-to
tags: [enterprise, auth]
---
```

### Recipe 9: GitHub Actions stale-bot for git-backed KB

```yaml
# .github/workflows/stale-content.yml
name: Stale KB content
on:
  schedule:
    - cron: '0 9 * * 1'
  workflow_dispatch:

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - name: Find stale pages
        run: |
          THRESHOLD=180
          NOW=$(date -u +%s)
          find docs -name '*.md' -print0 | while IFS= read -r -d '' f; do
            ts=$(git log -1 --format=%ct -- "$f")
            age=$(( (NOW - ts) / 86400 ))
            if [ "$age" -gt "$THRESHOLD" ]; then
              echo "$f|$age" >> stale.txt
            fi
          done
      - name: Update frontmatter status
        run: |
          if [ -s stale.txt ]; then
            while IFS='|' read -r f age; do
              python -c "import re,sys;f=open('$f').read();new=re.sub(r'^status: published$','status: stale',f,count=1,flags=re.M);open('$f','w').write(new)"
            done < stale.txt
            git config user.email "bot@example.com"
            git config user.name "stale-bot"
            git add -A && git commit -m "chore(docs): mark $(wc -l<stale.txt) pages stale" && git push
          fi
      - name: Slack ping owners
        run: |
          [ -s stale.txt ] && curl -X POST "$SLACK_WEBHOOK" \
            -H 'Content-Type: application/json' \
            -d "{\"text\":\"Stale KB pages this week:\\n$(awk -F'|' '{printf "%s (%sd)\\n",$1,$2}' stale.txt)\"}"
```

### Recipe 10: Archive without delete

```bash
# Notion: move to "Archive" sub-page; uncheck "Show in nav" property
curl -X PATCH "https://api.notion.com/v1/pages/$PAGE_ID" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -d '{"properties":{"Status":{"status":{"name":"Archived"}},"Show in nav":{"checkbox":false}}}'

# Git: move to _archived/, add banner, keep in search index
git mv docs/how-to/legacy-sso.md docs/_archived/how-to/legacy-sso.md
```

## Examples

### Example 1: Implement 5-state lifecycle in Notion KB

**Goal:** 240 articles; no consistent state; owners unaware of staleness.

**Steps:**
1. Add Status + Last Verified + Owner properties (Recipe 1).
2. Bulk-set existing articles to "Published" via Notion API.
3. Add automation: Status=Stale → Slack DM to Owner.
4. Add automation: Last Verified > 90d → set Status=Stale.
5. Quarterly: filter Status=Stale; route owner queue.

**Result:** Every article has named owner + state; stale → owner ping within 1 day.

### Example 2: Git-backed Docusaurus KB lifecycle

**Goal:** PRs ship as Draft; require SME approval before Published.

**Steps:**
1. Add `status: draft` to all new article frontmatter (PR template).
2. CODEOWNERS routes review by content area.
3. Pre-publish CI gate: `grep -r '^status: draft' docs/` fails build for landed-but-draft articles.
4. Merge sets status=published via PR template checkbox + GitHub Action.
5. Cron (Recipe 9) flips stale pages monthly.

**Result:** No publish gate skipping; named owner on every PR.

## Edge cases / gotchas

- **Notion DB automations need Workspace owner** to set up; free plan limited to 100 automation runs/mo.
- **Confluence Page Approvals = paid Marketplace app** (~$5/user/mo from AppFox or similar).
- **Document360 workflows = Pro tier+** (~$149/mo).
- **GitHub Actions cron not exact** — "0 9 * * 1" can fire 0-30 min late under load. Don't depend on exact time.
- **Don't delete archives** — old support tickets reference them; SEO inbound dies. Keep with banner for 12mo minimum.
- **Status property race condition** — when 2 editors land changes simultaneously, last write wins. Use Confluence Page Approvals for higher-stakes content.
- **Last Verified vs Last Modified** — auto-modified by any edit (typo fix); Last Verified is a deliberate SME stamp. Don't conflate.
- **Stale-bot false positives** — articles that are accurate and intentionally evergreen still need an owner ping to re-verify. Don't auto-archive without human review.
- **Frontmatter drift** — enforce with `vale` rule "every article must have status + owner + last_verified."

## Sources

- Notion DB automations: https://www.notion.com/help/database-automations
- Notion API status property: https://developers.notion.com/reference/property-object#status
- Confluence Page Properties: https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page-properties/
- Confluence Page Approvals: https://www.atlassian.com/software/confluence/apps/page-approvals
- Document360 workflows: https://docs.document360.com/docs/workflows
- GitBook content API: https://developer.gitbook.com/
- GitHub Actions stale: https://github.com/actions/stale
