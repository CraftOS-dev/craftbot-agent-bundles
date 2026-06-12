---
name: employee-facing-internal-wiki-notion-slab
description: Internal wiki — Notion teamspaces (native MCP), Slab Team Owner, Tettra Slack-native, Guru "Card of the Day", Confluence Spaces, GitBook for dev-leaning teams. SSO + SCIM, expert finder, "Spring Clean" sprints. Use when standing up or scaling internal docs.
---

# Internal wiki — Notion / Slab / Tettra / Guru / Confluence / GitBook

## When to use

User says "internal wiki", "company handbook", "engineering runbook hub", "Slack-native KB", "Notion teamspaces", "Slab vs Tettra vs Guru", "Confluence spaces". Reach AFTER ownership decisions (knowledge-ops skill) and BEFORE wiring expert-finder.

## Setup

```bash
# Notion (native MCP)
# Already wired via notion-mcp

# Slab
# REST: https://api.slab.com — GraphQL endpoint
export SLAB_API_KEY=...

# Tettra
# REST: https://app.tettra.co/api
export TETTRA_API_KEY=...

# Guru
# REST: https://api.getguru.com/api/v1
export GURU_USER=...
export GURU_TOKEN=...

# Confluence
export CONFLUENCE_USER=...
export CONFLUENCE_API_TOKEN=...

# GitBook
export GITBOOK_TOKEN=...

# Slab CLI not official; use curl
npm i -g @slack/web-api  # for surfacing into Slack
```

Auth / API key requirements:
- Notion via MCP token (already wired)
- Slab GraphQL: API key from Settings → API
- Tettra: API key from settings
- Guru: user+token Basic auth
- Confluence Atlassian API token
- Slack: bot token for surfacing

## Common recipes

### Recipe 1: Notion teamspace bootstrap

```bash
# Create top-level teamspace page
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent":{"workspace":true},
    "properties":{"title":[{"text":{"content":"Engineering"}}]},
    "children":[
      {"type":"heading_1","heading_1":{"rich_text":[{"text":{"content":"Engineering wiki"}}]}},
      {"type":"divider","divider":{}}
    ]
  }'
```

### Recipe 2: Slab post creation

```bash
curl -X POST "https://api.slab.com/v1/graphql" \
  -H "Authorization: $SLAB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query":"mutation($input:CreatePostInput!){createPost(input:$input){id}}",
    "variables":{"input":{
      "title":"Engineering onboarding",
      "content":"# Welcome\n\nFirst steps...",
      "format":"MARKDOWN",
      "topicIds":["topic-eng"]
    }}
  }'
```

### Recipe 3: Slab Team assignment

```bash
curl -X POST "https://api.slab.com/v1/graphql" \
  -H "Authorization: $SLAB_API_KEY" \
  -d '{"query":"mutation{addUserToTeam(teamId:\"team-eng\", userId:\"user-alice\", role:OWNER){id}}"}'
```

### Recipe 4: Tettra page create

```bash
curl -X POST "https://app.tettra.co/api/v1/pages" \
  -H "Authorization: Bearer $TETTRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Engineering runbook: incident response",
    "content":"# Incident response\n\n1. ...",
    "category_id":12,
    "subcategory_id":34,
    "published": true
  }'
```

### Recipe 5: Guru card create

```bash
curl -X POST "https://api.getguru.com/api/v1/cards" \
  -u "${GURU_USER}:${GURU_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "preferredPhrase":"Reset SSO config",
    "content":"<p>Steps...</p>",
    "collection":{"id":"col_engineering"},
    "boards":[{"id":"board_runbooks"}],
    "shareStatus":"TEAM",
    "verifiers":[{"user":{"email":"alice@example.com"}}]
  }'
```

### Recipe 6: Guru "Card of the Day" Slack integration

In Guru: Settings → Integrations → Slack → Connect; enable "Daily Card" to Slack channel.

```bash
# Confirm via API
curl -u "${GURU_USER}:${GURU_TOKEN}" "https://api.getguru.com/api/v1/integrations/slack"
```

### Recipe 7: Confluence Space + page create

```bash
# Create space
curl -X POST "https://${SITE}.atlassian.net/wiki/rest/api/space" \
  -u "$CONFLUENCE_USER:$CONFLUENCE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"key":"ENG","name":"Engineering","description":{"plain":{"value":"Engineering wiki","representation":"plain"}}}'

# Create page
curl -X POST "https://${SITE}.atlassian.net/wiki/rest/api/content" \
  -u "$CONFLUENCE_USER:$CONFLUENCE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type":"page",
    "title":"Onboarding",
    "space":{"key":"ENG"},
    "body":{"storage":{"value":"<h1>Welcome</h1>","representation":"storage"}}
  }'
```

### Recipe 8: GitBook space + page

```bash
# Create change request
curl -X POST "https://api.gitbook.com/v1/spaces/$SPACE_ID/change-requests" \
  -H "Authorization: Bearer $GITBOOK_TOKEN" \
  -d '{"title":"Add onboarding page"}'

# Add page via change request
curl -X POST "https://api.gitbook.com/v1/spaces/$SPACE_ID/content/page" \
  -H "Authorization: Bearer $GITBOOK_TOKEN" \
  -d '{"page":{"title":"Onboarding","kind":"document"}}'
```

### Recipe 9: Surface a wiki page in Slack

```bash
curl -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel":"#engineering",
    "text":"📖 New runbook: Incident response — https://wiki.example.com/eng/incident-response",
    "blocks":[
      {"type":"section","text":{"type":"mrkdwn","text":"*New runbook*: <https://wiki.example.com/eng/incident-response|Incident response>"}}
    ]
  }'
```

### Recipe 10: SSO group sync via SCIM

```bash
# Notion SCIM example (Enterprise plan)
curl -X POST "https://api.notion.com/scim/v2/Users" \
  -H "Authorization: Bearer $NOTION_SCIM_TOKEN" \
  -H "Content-Type: application/scim+json" \
  -d '{
    "schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],
    "userName":"alice@example.com",
    "active":true,
    "emails":[{"value":"alice@example.com","primary":true}]
  }'
```

Same SCIM endpoints exist for Confluence, Guru, Slab Enterprise.

### Recipe 11: Quarterly Wiki Spring Clean sprint

```python
# scripts/spring-clean.py
# Pull pages not edited in 365d AND no views in 180d → archive candidates
# Run quarterly; send list to teamspace owners.
import requests, os, datetime
notion_db = os.environ['NOTION_DB_WIKI']
cursor = None
candidates = []
while True:
    r = requests.post(f"https://api.notion.com/v1/databases/{notion_db}/query",
        headers={"Authorization":f"Bearer {os.environ['NOTION_TOKEN']}","Notion-Version":"2022-06-28"},
        json={"start_cursor": cursor} if cursor else {})
    for pg in r.json()['results']:
        edited = datetime.datetime.fromisoformat(pg['last_edited_time'].rstrip('Z'))
        if (datetime.datetime.utcnow() - edited).days > 365:
            candidates.append(pg['url'])
    cursor = r.json().get('next_cursor')
    if not cursor: break
print(f"{len(candidates)} stale page candidates for archive review")
```

### Recipe 12: Slack-native search (Tettra)

In Tettra Slack: `/tettra what is the incident response process?`. Returns ranked pages inline.

## Examples

### Example 1: New startup — bootstrap Notion wiki

**Goal:** Engineering, Product, GTM teamspaces with onboarding flows.

**Steps:**
1. Workspace-level template (Notion built-in Company Wiki).
2. Create teamspaces: Engineering, Product, GTM (Recipe 1).
3. RACI per teamspace (knowledge-ops skill).
4. New-joiner page auto-shared via Notion automation.
5. Slack #wiki channel posts new pages via webhook.

**Result:** Wiki feels owned; new joiners onboard in 1 day.

### Example 2: 500-person co — Confluence + Slab hybrid

**Goal:** Confluence for engineering deep docs; Slab for go-to-market.

**Steps:**
1. Confluence Space per engineering team (Recipe 7).
2. Slab teamspaces per GTM function (Recipe 2).
3. SSO + SCIM across both (Recipe 10).
4. Quarterly Spring Clean (Recipe 11).
5. Slack surfacing on every new top-level page (Recipe 9).

**Result:** Engineers stay in Confluence (Jira proximity); GTM lives in Slab (Slack proximity).

## Edge cases / gotchas

- **Notion Workspace search ≠ teamspace search** — search scope follows your last-clicked teamspace; document the gotcha.
- **Slab "Team Owner"** is platform feature; not per-page ACL. Article-level ownership needs RACI db.
- **Tettra page categories** are flat (2 levels). For deep IA, use Confluence/Notion.
- **Guru cards have "verified by" workflow** — verifier must re-stamp every X days or card shows "unverified". This is great for accuracy; can become nag if over-eager.
- **Confluence Page Approvals = paid Marketplace app**.
- **GitBook git-sync** turns docs-as-code; pairs well with engineering teams; harder for non-technical contributors.
- **SCIM provisioning** is Enterprise plan on Notion/Guru/Slab; budget accordingly.
- **Slack-native KBs go stale faster** — too easy to write, too hard to maintain. Add cadence.
- **Migration between platforms** — see `content-migration-between-platforms` skill.
- **One source of truth per topic** — if a page exists in both Notion and Confluence, owners argue which is canonical. Pick one per content area.

## Sources

- Notion API: https://developers.notion.com/
- Notion SCIM: https://www.notion.com/help/provision-users-and-groups-with-scim
- Slab help (Teams): https://slab.com/help/teams
- Slab API: https://docs.slab.com/developers
- Tettra API: https://help.tettra.com/en/articles/4307317-tettra-api
- Guru API: https://developer.getguru.com/reference/
- Guru Slack integration: https://help.getguru.com/en/articles/4951036-slack-integration
- Confluence REST v2: https://developer.atlassian.com/cloud/confluence/rest/v2/
- GitBook API: https://developer.gitbook.com/
- SCIM 2.0: https://scim.cloud/
