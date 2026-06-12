<!--
Source: https://developers.notion.com/reference/intro
Lychee link checker: https://lychee.cli.rs/
-->
# Notion Knowledge Base Management — SKILL

Notion is the editorial source-of-truth for the support KB / FAQ / runbook library. This skill covers KB hygiene: drift detection (articles unreviewed in 90d), dead-link sweep (Lychee), zero-result cross-reference, KB article authoring, and bidirectional sync with platform Help Center (Intercom Articles / Zendesk Guide).

## When to use

- **Weekly KB hygiene** — find stale articles, dead links, orphaned pages.
- **Authoring new KB articles** from ticket-cluster signals (with the technical-writer agent).
- **FAQ DB management** — add new FAQ entries, mark resolved, track view counts.
- **Macro / saved-reply source of truth** — Notion DB drives cross-platform parity (Zendesk macros, Intercom articles, Front templates, HelpScout saved replies, Plain snippets).
- **Drift report** — articles with `last_reviewed < 90d ago` flagged.

Trigger phrases: "audit our KB", "find dead links", "create FAQ entry", "stale Notion docs", "KB drift report".

## Setup

```bash
# Notion MCP already on the recipient's install (notion-mcp).
# Direct API also works:
curl -sS "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28"
```

Auth + env:
- `NOTION_TOKEN` — integration token at https://www.notion.so/my-integrations. Internal integration recommended; share specific databases / pages with it.
- `NOTION_VERSION` — pin to `2022-06-28` (still stable in 2026).
- `KB_DB_ID` — the database ID for the KB collection. Find in URL: `notion.so/<workspace>/<db-id>?v=...`.

Tool prerequisites:
- Lychee (link checker) — `cargo install lychee` or `uvx --from lychee-rs lychee`. Free, fast.
- KB schema: each article page has properties `Title`, `Status` (Draft / Published / Archived), `Last Reviewed` (date), `Owner` (person), `Source Tickets` (multi-select / text), `Linked Macro IDs` (text), `View Count Last 30d` (number).

## Common recipes

### Recipe 1: Query KB DB for stale articles (>90d since review)

```bash
# Via notion-mcp
mcp tool notion.query_database \
  --database_id $KB_DB_ID \
  --filter '{"and":[
    {"property":"Status","status":{"equals":"Published"}},
    {"property":"Last Reviewed","date":{"before":"2026-03-09"}}
  ]}'

# Direct API
curl -sS -X POST "https://api.notion.com/v1/databases/$KB_DB_ID/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "filter":{
      "and":[
        {"property":"Status","status":{"equals":"Published"}},
        {"property":"Last Reviewed","date":{"before":"2026-03-09"}}
      ]
    },
    "sorts":[{"property":"Last Reviewed","direction":"ascending"}]
  }' | jq '.results[] | {id, title: .properties.Title.title[0].plain_text, last_reviewed: .properties["Last Reviewed"].date.start}'
```

Compute the cutoff date (today - 90d) dynamically.

### Recipe 2: Update article (mark reviewed)

```bash
curl -sS -X PATCH "https://api.notion.com/v1/pages/$PAGE_ID" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "properties":{
      "Last Reviewed":{"date":{"start":"2026-06-09"}},
      "Reviewed By":{"people":[{"id":"$USER_ID"}]}
    }
  }'
```

### Recipe 3: Create a new KB article from a ticket cluster

```bash
curl -sS -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent":{"database_id":"'$KB_DB_ID'"},
    "properties":{
      "Title":{"title":[{"text":{"content":"How to rotate your API key"}}]},
      "Status":{"status":{"name":"Draft"}},
      "Last Reviewed":{"date":{"start":"2026-06-09"}},
      "Source Tickets":{"rich_text":[{"text":{"content":"INT-1234, ZEN-5678, INT-9012"}}]}
    },
    "children":[
      {"object":"block","type":"heading_2","heading_2":{"rich_text":[{"text":{"content":"Quick answer (TL;DR)"}}]}},
      {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"text":{"content":"Go to Settings → API Keys → Rotate. The old key remains valid for 24h."}}]}}
    ]
  }'
```

Author per the KB article template in `role.md`. Use the technical-writer agent (`/agents technical-writer`) for richer prose.

### Recipe 4: Lychee link sweep across KB

```bash
# Run weekly via cli-anything cron
uvx --from lychee-rs lychee \
  --max-concurrency 10 \
  --timeout 20 \
  --format json \
  --output kb-link-report.json \
  https://kb.brand.com/

# Filter failures
jq '.fail_map | to_entries[] | {url: .key, errors: .value[].status}' kb-link-report.json
```

Lychee respects `robots.txt`, follows redirects, supports auth headers. For internal Notion-published KBs, point at `https://<your-domain>.notion.site/...`.

### Recipe 5: Cross-reference Kapa zero-result queries with KB

```bash
# 1. Pull top zero-result queries from Kapa
ZERO=$(curl -sS "https://api.kapa.ai/analytics/v1/projects/$KAPA_PROJECT_ID/queries/unanswered?period=30d&limit=20" \
  -H "X-API-Key: $KAPA_API_KEY" | jq -r '.queries[].query')

# 2. For each, search Notion KB
echo "$ZERO" | while read query; do
  echo "Query: $query"
  curl -sS -X POST "https://api.notion.com/v1/search" \
    -H "Authorization: Bearer $NOTION_TOKEN" \
    -H "Notion-Version: 2022-06-28" \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"$query\",\"filter\":{\"property\":\"object\",\"value\":\"page\"}}" \
    | jq '.results | length'
done
```

If a zero-result query returns 0 Notion matches → content gap (draft a new article).

### Recipe 6: Bulk-archive deprecated articles

```bash
# List candidates first (Status=Archived but not yet trashed)
curl -sS -X POST "https://api.notion.com/v1/databases/$KB_DB_ID/query" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -d '{"filter":{"property":"Status","status":{"equals":"Archived"}}}' \
  | jq -r '.results[].id' | while read id; do
    curl -sS -X PATCH "https://api.notion.com/v1/pages/$id" \
      -H "Authorization: Bearer $NOTION_TOKEN" \
      -H "Notion-Version: 2022-06-28" \
      -d '{"archived":true}'  # Notion's trash flag
  done
```

`archived: true` moves to Notion trash (30-day recovery window).

### Recipe 7: Sync Notion KB → Intercom Help Center

```python
# Pseudocode via cli-anything python
import notion_client, requests, os

n = notion_client.Client(auth=os.environ['NOTION_TOKEN'])
pages = n.databases.query(database_id=os.environ['KB_DB_ID'], filter={
    'property': 'Status', 'status': {'equals': 'Published'}
})['results']

for p in pages:
    title = p['properties']['Title']['title'][0]['plain_text']
    body = render_blocks_to_html(n.blocks.children.list(block_id=p['id'])['results'])
    intercom_id = p['properties'].get('Intercom Article ID', {}).get('rich_text', [])
    if intercom_id:
        url = f"https://api.intercom.io/articles/{intercom_id[0]['plain_text']}"
        method = 'PUT'
    else:
        url = "https://api.intercom.io/articles"
        method = 'POST'
    requests.request(method, url, headers={
        'Authorization': f"Bearer {os.environ['INTERCOM_TOKEN']}",
        'Intercom-Version': '2.13'
    }, json={'title': title, 'body': body, 'author_id': os.environ['ADMIN_ID'], 'state': 'published'})
```

Notion is source of truth; Intercom is the published surface.

### Recipe 8: Add to "Source Tickets" property when reusing pattern

```bash
# Fetch current value, append new ticket id, PATCH
CURRENT=$(curl -sS https://api.notion.com/v1/pages/$PAGE_ID \
  -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" \
  | jq -r '.properties["Source Tickets"].rich_text[0].plain_text // ""')
NEW="$CURRENT, INT-9999"

curl -sS -X PATCH "https://api.notion.com/v1/pages/$PAGE_ID" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -d "{\"properties\":{\"Source Tickets\":{\"rich_text\":[{\"text\":{\"content\":\"$NEW\"}}]}}}"
```

Demonstrates KB-article ↔ ticket back-reference. Useful for showing engineering "this article reflects N customer reports."

### Recipe 9: Drift report → weekly digest

```bash
# 1. Query stale articles (Recipe 1)
# 2. Aggregate by Owner
# 3. Format markdown summary
# 4. Email via gmail-mcp to support-lead + each owner
```

Report includes: title, last_reviewed, owner, view_count_30d. Owners self-serve.

### Recipe 10: Tag article with linked-macro IDs (cross-platform parity)

```bash
curl -sS -X PATCH "https://api.notion.com/v1/pages/$PAGE_ID" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "properties":{
      "Linked Macro IDs":{"rich_text":[{"text":{"content":"zendesk:macro_12345 | intercom:article_67890 | front:tpl_abc123 | helpscout:sr_99 | plain:snippet_42"}}]}
    }
  }'
```

When a downstream platform's macro/template is updated, sync back to Notion (Notion stays canonical).

### Recipe 11: Search across the workspace

```bash
curl -sS -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "query":"SSO Okta",
    "filter":{"property":"object","value":"page"},
    "page_size":10
  }' | jq '.results[] | {id, title: .properties.Title.title[0].plain_text}'
```

### Recipe 12: List recently-modified pages (audit feed)

```bash
curl -sS -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "sort":{"direction":"descending","timestamp":"last_edited_time"},
    "page_size":20
  }' | jq '.results[] | {id, title: .properties.Title.title[0].plain_text, last_edited: .last_edited_time}'
```

Sanity-check for unintended edits or unauthorized publishers.

## Examples

### Example 1: Monday morning drift report

**Goal:** Identify stale KB content and dead links; email owners.

**Steps:**
1. Compute cutoff = today - 90d.
2. Run Recipe 1 → list stale articles.
3. Run Recipe 4 → Lychee sweep over kb.brand.com.
4. Aggregate: stale articles + broken-link articles, group by `Owner`.
5. Format markdown digest (using `docx` skill optionally).
6. `gmail-mcp send_email` to each owner with their list + a "mark reviewed" CTA.

**Result:** Each owner sees their 3-7 stale articles each Monday; cleanup is distributed and predictable.

### Example 2: Convert top ticket cluster into KB article + Intercom Article

**Goal:** Ship a new article for the #1 unanswered query.

**Steps:**
1. Pull top zero-result query from Kapa (Recipe 5).
2. Draft KB article per the template in `role.md` (use `/agents technical-writer` for prose pass).
3. `POST /pages` in Notion KB DB (Recipe 3).
4. Render Notion blocks → HTML; POST to Intercom Help Center (Recipe 7).
5. Trigger Kapa re-index of the Help Center source (`POST /sources/$id/reindex`).
6. Update Notion page with the Intercom Article ID for back-reference.

**Result:** New article live + Kapa now answers the previously-unanswered query.

## Edge cases / gotchas

- **Notion API uses cursor pagination** — `has_more` / `next_cursor` on each call. Easy to drop results if you don't loop.
- **Rate limits** — 3 req / sec average per integration token. Burst ok; sustained traffic gets 429. Honor `Retry-After`.
- **Rich text vs title** — Notion's `Title` property is a separate type from `Rich Text`. PATCH the wrong type and you get 400.
- **Blocks API is paginated separately from pages** — `GET /blocks/$id/children` for the body; `GET /pages/$id` for properties only. Easy to think one call gives you everything.
- **`archived: true` is soft-delete** — 30d in trash, then permanent. Don't archive without owner approval.
- **Status property type changed in 2023** — older databases use `select`; newer use `status`. Inspect schema first.
- **Notion search ranks badly** — it's not Elasticsearch. For high-quality search, prefer Kapa's `/search` endpoint over Notion's.
- **Lychee config** — default user-agent gets blocked by some auth-walled sites. Use `--user-agent "Mozilla/5.0..."` and `--cookie-jar` if needed.
- **Integration must be shared with each page/DB** — easy 404 if you forgot to "Share → Add connection" on a new DB.
- **API version pinning** — always pass `Notion-Version`. Default behavior changes silently otherwise.
- **HTML rendering of Notion blocks is non-trivial** — most blocks have edge cases (code blocks, embeds, toggles). Use `notion-to-md` lib if pushing to Markdown-first downstream.

## Sources

- [Notion API introduction](https://developers.notion.com/reference/intro)
- [Notion databases — query](https://developers.notion.com/reference/post-database-query)
- [Notion pages — update](https://developers.notion.com/reference/patch-page)
- [Notion search](https://developers.notion.com/reference/post-search)
- [Lychee link checker](https://lychee.cli.rs/)
- [Lychee GitHub](https://github.com/lycheeverse/lychee)
