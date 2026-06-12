---
name: expert-finder-who-knows-x
description: "Who-knows-X" — Stack Overflow for Teams reputation, Slack channel-history mining, Notion expertise DB, git author analysis on docs/code, Glean / Lattice expert finder. Use when employees keep asking the same question and the answer lives in one head, not in a wiki.
---

# Expert finder — who knows about X internally?

## When to use

Reach for this skill when the user says: "who knows about X?", "expert finder", "find the SME", "who edited this article", "who answered this in Slack", "knowledge map", "expertise database", "Glean", "Stack Overflow for Teams reputation", or "we keep DMing the same 3 people". Use this skill to operationalize tacit-knowledge discovery in addition to (not instead of) writing the answer down. If a question repeats >3×, the expert lookup is a stopgap — the real fix is a KB article in `knowledge-ops-owner-contributor-flow`.

## Setup

```bash
# Notion (default DB for expertise)
# No install — use notion-mcp; see knowledge-base-manager bundle

# Slack channel history
npm i -g @slack/web-api    # or use slack-mcp

# Stack Overflow for Teams
# REST API; no client needed
# pipx install requests-cache  (handy for repeat queries)

# git author analysis (built-in)
git --version

# Glean / Lattice (paid; no install — REST API)
```

Auth / env vars:
- `NOTION_API_TOKEN` — for expertise DB. Free.
- `SLACK_BOT_TOKEN` — `xoxb-...` from app → OAuth & Permissions. Needs `channels:history`, `users:read`, `search:read`. Free.
- `STACK_OVERFLOW_TEAMS_PAT` — Stack Overflow for Teams API personal access token. Paid (Business tier+).
- `GLEAN_API_KEY` — Glean Indexing/Search API. Paid.
- `GH_TOKEN` — for git author analysis via GitHub API if going beyond local git.

## Common recipes

### Recipe 1: Notion expertise DB schema

```python
# DB columns
- Person (relation → People DB)
- Areas (multi-select: SSO, Webhooks, Billing, Mobile, etc.)
- Depth (select: Expert / Familiar / Curious / Owner)
- Last verified (date)
- Source (multi-select: Self-declared / Manager-confirmed / Slack-history / Git-history)
- Out-of-office (date)
- Slack handle (string)
- Email (email)
- Page link (URL — anchor in Notion)
```

```bash
# Query: "who knows SSO?"
curl -X POST "https://api.notion.com/v1/databases/$EXPERT_DB_ID/query" \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H 'Notion-Version: 2022-06-28' \
  -d '{
    "filter": {
      "and": [
        {"property":"Areas","multi_select":{"contains":"SSO"}},
        {"property":"Depth","select":{"does_not_equal":"Curious"}}
      ]
    },
    "sorts": [{"property":"Depth","direction":"ascending"}]
  }' | jq '.results[].properties.Person.title[0].plain_text'
```

### Recipe 2: Mine Slack channel history for "who answered this"

```bash
# Find Slack messages matching "SSO Okta" with replies count → top responder
curl -X POST 'https://slack.com/api/search.messages' \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -d "query=sso okta in:#help-eng has:reply" \
  -d "count=100" \
  -d "sort=score" \
  | jq -r '.messages.matches[] | "\(.user)\t\(.text|.[:80])"'

# Aggregate top responders
curl -X POST 'https://slack.com/api/search.messages' \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -d "query=sso okta in:#help-eng" \
  | jq -r '.messages.matches[].user' \
  | sort | uniq -c | sort -rn | head -5
```

The top-5 list by response count = de-facto SMEs for that topic.

### Recipe 3: Slack `channels:history` for thread depth

```bash
# Pull full channel history of #ask-sre for last 90d → cluster by topic
SINCE=$(date -d '90 days ago' +%s)
curl -X GET "https://slack.com/api/conversations.history?channel=$CHANNEL_ID&oldest=$SINCE&limit=1000" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  > history.json

# Top responders by thread participation
jq -r '.messages[] | select(.reply_count>0) | .latest_reply' history.json | \
  xargs -I{} curl -s "https://slack.com/api/conversations.replies?channel=$CHANNEL_ID&ts={}" \
    -H "Authorization: Bearer $SLACK_BOT_TOKEN" | \
  jq -r '.messages[].user' | sort | uniq -c | sort -rn | head -10
```

### Recipe 4: Git author analysis — "who edited articles about X"

```bash
# Top authors on docs about "webhook"
git log --pretty=format:'%an|%ae' -- 'docs/**/*webhook*' | sort | uniq -c | sort -rn | head -5

# Top authors on a specific code area
git log --pretty=format:'%an' -- 'src/services/sso/**' | sort | uniq -c | sort -rn | head -5

# Recent authors (last 90d) — current expertise vs historical
git log --since='90 days ago' --pretty=format:'%an' -- 'docs/**/*sso*' | sort | uniq -c | sort -rn
```

Pair with `OWNERS.md`-style CODEOWNERS for the source-of-truth on official ownership.

### Recipe 5: Stack Overflow for Teams — top users per tag

```bash
# Top users with reputation > 500 on tag "sso"
curl -s "https://your-team.stackenterprise.co/api/v3/users/by-reputation?tags=sso&limit=10" \
  -H "X-API-Access-Token: $STACK_OVERFLOW_TEAMS_PAT" \
  | jq '.items[] | {name, reputation, tag_score: .tags[]|select(.tag_name=="sso")|.score}'

# Recent answer activity
curl -s "https://your-team.stackenterprise.co/api/v3/questions?tags=sso&order=activity&limit=20" \
  -H "X-API-Access-Token: $STACK_OVERFLOW_TEAMS_PAT" \
  | jq '.items[] | {title, answer_count, owner: .owner.name, accepted: .accepted_answer_id}'
```

### Recipe 6: Glean Search API — query for SMEs

```bash
# Glean Indexing API to surface "experts on SSO"
curl -X POST 'https://your-org.glean.com/rest/api/v1/search' \
  -H "Authorization: Bearer $GLEAN_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "SSO Okta SAML",
    "requestOptions": {
      "facetFilters": [{"fieldName":"category","values":["expert"]}]
    },
    "pageSize": 10
  }' | jq '.results[] | {title, snippet, person: .person.name}'
```

Glean cross-indexes Notion + Slack + Confluence + git + Drive — the broadest signal.

### Recipe 7: Render a unified expert card

```bash
#!/usr/bin/env bash
# expert-card.sh — given a topic, render unified card from Notion + git + Slack
TOPIC=$1

NOTION=$(curl -s -X POST "https://api.notion.com/v1/databases/$EXPERT_DB_ID/query" \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H 'Notion-Version: 2022-06-28' \
  -d "{\"filter\":{\"property\":\"Areas\",\"multi_select\":{\"contains\":\"$TOPIC\"}}}" \
  | jq -r '.results[]|.properties.Person.title[0].plain_text')

GIT=$(git log --pretty=format:'%an' -- "docs/**/*${TOPIC}*" "src/**/*${TOPIC}*" 2>/dev/null | sort | uniq -c | sort -rn | head -3 | awk '{print $2 " " $3}')

SLACK=$(curl -s -X POST 'https://slack.com/api/search.messages' \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -d "query=$TOPIC has:reply" | \
  jq -r '.messages.matches[].user' | sort | uniq -c | sort -rn | head -3 | awk '{print $2}')

cat <<EOF
# Expert card: $TOPIC

## Notion (self-declared)
$NOTION

## Git (last touched docs/code)
$GIT

## Slack (top responders in last 90d)
$SLACK
EOF
```

### Recipe 8: Out-of-office redirect (don't ping vacationing experts)

```bash
# Filter out OOO before pinging
candidates=$(curl -s -X POST "https://api.notion.com/v1/databases/$EXPERT_DB_ID/query" \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H 'Notion-Version: 2022-06-28' \
  -d '{"filter":{"and":[
    {"property":"Areas","multi_select":{"contains":"SSO"}},
    {"or":[
      {"property":"Out-of-office","date":{"is_empty":true}},
      {"property":"Out-of-office","date":{"before":"'$(date --iso-8601)'"}}
    ]}
  ]}}' | jq -r '.results[]|.properties.Slack.rich_text[0].plain_text')
```

### Recipe 9: Auto-update Notion DB from git authorship monthly

```yaml
# .github/workflows/refresh-expert-db.yml
on:
  schedule: [{ cron: '0 9 1 * *' }]   # 1st of each month
jobs:
  refresh:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - name: Compute per-topic top authors
        run: |
          for topic in sso webhooks billing api-keys; do
            top=$(git log --since='90 days ago' --pretty=format:'%ae' -- "docs/**/*${topic}*" "src/**/*${topic}*" | sort | uniq -c | sort -rn | head -3 | awk '{print $2}')
            for email in $top; do
              curl -X POST 'https://api.notion.com/v1/pages' \
                -H "Authorization: Bearer ${{ secrets.NOTION_API_TOKEN }}" \
                -H 'Notion-Version: 2022-06-28' \
                -d "{
                  \"parent\":{\"database_id\":\"${{ secrets.EXPERT_DB_ID }}\"},
                  \"properties\":{
                    \"Email\":{\"email\":\"$email\"},
                    \"Areas\":{\"multi_select\":[{\"name\":\"$topic\"}]},
                    \"Source\":{\"multi_select\":[{\"name\":\"Git-history\"}]},
                    \"Last verified\":{\"date\":{\"start\":\"$(date --iso-8601)\"}}
                  }
                }"
            done
          done
```

### Recipe 10: Slack bot "/who-knows" slash command

```python
# Flask app (deployed on Cloudflare Workers / Render / Fly)
from flask import Flask, request, jsonify
import os, requests
app = Flask(__name__)

@app.post('/who-knows')
def who_knows():
    topic = request.form['text'].strip()
    # Query Notion expert DB
    r = requests.post(
        f"https://api.notion.com/v1/databases/{os.environ['EXPERT_DB_ID']}/query",
        headers={'Authorization': f"Bearer {os.environ['NOTION_API_TOKEN']}", 'Notion-Version': '2022-06-28'},
        json={'filter':{'property':'Areas','multi_select':{'contains': topic}}})
    people = [p['properties']['Person']['title'][0]['plain_text'] for p in r.json()['results']]
    return jsonify({'response_type':'ephemeral', 'text': f"*Experts on {topic}:*\n- " + "\n- ".join(people)})
```

Register in Slack → Apps → Slash commands → `/who-knows`.

## Examples

### Example 1: Stand up expertise DB + Slack bot in a day

**Goal:** Engineers stop DMing the same 3 people; SREs query a slash command.

**Steps:**
1. Build Notion expert DB (Recipe 1).
2. Self-declaration form: ask 30 ICs to list 2-3 topics they're "Expert" or "Familiar" in.
3. Manager-confirmation pass: managers verify the self-declarations.
4. Deploy Slack `/who-knows` (Recipe 10).
5. Tell the team in #all.
6. Auto-augment monthly from git history (Recipe 9).

**Result:** Cycle time for "who would know this?" drops from minutes to seconds.

### Example 2: Surface tacit knowledge from Slack history

**Goal:** Find the unwritten SSO knowledge living in #help-eng.

**Steps:**
1. Identify high-signal channels: `#help-eng`, `#ask-sre`, `#support`.
2. Pull 90d history per channel (Recipe 3).
3. Aggregate top responders per recurring topic.
4. Approach top-3 responders: "Will you write the canonical KB article?"
5. Add them to Notion expert DB with Source = "Slack-history".

**Result:** Tacit knowledge gets a path to becoming wiki content.

### Example 3: Glean cross-source expert lookup

**Goal:** "Who knows about our payments integration with Stripe?" — search across Slack + Notion + git + Drive.

**Steps:**
1. Ensure Glean is indexing all four sources (Glean Admin → Sources).
2. Query the Search API (Recipe 6) with relevant terms.
3. Glean returns ranked candidates with confidence scores.
4. Cross-check with Notion DB; auto-add if Glean confidence > 0.8.

**Result:** Single-query lookup across every tacit-knowledge store in the org.

## Edge cases / gotchas

- **Self-declaration bias** — people under-rate their expertise. Manager-confirmation pass is non-optional.
- **Last-verified rot** — like KB articles, expertise rots. Auto-prompt re-verification every 6 months via Notion automation.
- **Slack `search.messages` rate limits** — Tier 2 (20+ req/min). Batch queries; cache results.
- **Stack Overflow Teams is paid + slow API** — Business tier minimum. Rate limit 300 req/30s.
- **Glean is enterprise-priced** — $10-30/user/month; only justifiable at scale. Use Notion DB + Slack search for SMB.
- **Don't expose to all** — restrict queries to authenticated employees; Slack bot returns ephemeral (Recipe 10).
- **Promote experts → burn them out** — if anyone is pinged >5×/week, push to write the article (`knowledge-ops-owner-contributor-flow`).
- **CODEOWNERS ≠ topic expertise** — CODEOWNERS is responsibility, not knowledge. Two separate signals.
- **Git author noise** — drive-by typo fixes show up as "authorship". Filter with weighted metric (lines × author count).
- **OOO data needs to come from HRIS** — pull from BambooHR / Workday; sync into Notion DB via webhook.
- **Don't index private DMs** — Slack scope: `channels:history` + `groups:history` only; not `im:history`.
- **Topic taxonomy drift** — "SSO" vs "single sign-on" under-counts. Use synonyms (mirror `algolia-typesense-search-optimization`).
- **Glean Search API cold queries** — cache results in your `/who-knows` bot to beat Slack 3s timeout.
- **Don't substitute for written docs** — every "/who-knows X" hit >3× should generate a KB ticket.

## Sources

- [Stack Overflow for Teams API](https://stackoverflowteams.com/api/v3/)
- [Stack Overflow Teams reputation explained](https://stackoverflowteams.help/en/articles/4577200-reputation)
- [Slack `search.messages` API](https://api.slack.com/methods/search.messages)
- [Slack `conversations.history` API](https://api.slack.com/methods/conversations.history)
- [Slack slash command guide](https://api.slack.com/interactivity/slash-commands)
- [Notion databases API](https://developers.notion.com/reference/post-database-query)
- [Glean Search API](https://developers.glean.com/docs/client_api/search_api/)
- [Glean Expert Finder](https://www.glean.com/product/expert-finder)
- [GitHub CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [Tacit knowledge — Polanyi](https://en.wikipedia.org/wiki/Tacit_knowledge)
- [Knowledge graph mining via Slack — Glean case study](https://www.glean.com/blog/)
