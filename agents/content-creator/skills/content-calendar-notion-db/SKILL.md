# Content Calendar — Notion Editorial DB + Buffer Cascade

> Maintain a single-source-of-truth editorial calendar in Notion (parent tentpole + child derivative rows) with Buffer scheduling.

## When to use

Trigger on: "set up my content calendar", "Notion editorial DB", "what should I publish next week", "schedule the week's content", "editorial parent-child DB", "Buffer cascade", "content backlog". This skill owns: Notion DB schema, parent/child row maintenance, week-ahead planning queries, Buffer schedule cascade. For series-level arc planning see `content-series-multi-format-arcs`. For repurposing pipelines see `repurposing-pipeline-1-to-10`.

## Setup

```bash
# Notion MCP
npx -y @notionhq/mcp-server@latest

# Verify access
curl -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  "https://api.notion.com/v1/users/me"

# Buffer MCP for cross-platform schedule
npx -y @buffer/mcp-server@latest
```

Auth env vars:
- `NOTION_API_KEY` — Notion internal integration token.
- `NOTION_EDITORIAL_DB` — editorial DB ID.
- `NOTION_SERIES_DB` — series DB ID (parent of tentpoles).
- `BUFFER_ACCESS_TOKEN` — Buffer personal access token.

## Common recipes

### Recipe 1: Editorial DB schema (single canonical structure)

```yaml
Editorial DB (combined parent tentpole + child derivative):
  properties:
    # Common to both parent + child
    Title: { type: title }
    Status: { type: select, options: [Backlog, Drafting, Review, Scheduled, Published, Repurposing, Archived] }
    Format: { type: select, options: [Newsletter issue, Podcast episode, YouTube long, YouTube short, Reels, TikTok, LinkedIn carousel, LinkedIn long-form, X thread, Threads, Bluesky, Blog post, Audiogram, Quote graphic, Infographic, Lead magnet, Brand partnership] }
    Channel: { type: select, options: [Newsletter, Podcast feed, YouTube, LinkedIn, X / Twitter, Threads, Bluesky, Mastodon, Instagram, TikTok, Facebook, Pinterest, Reddit, Owned blog] }
    Author: { type: people }
    Editor: { type: people }
    Owner: { type: people }
    Schedule date: { type: date }
    Published date: { type: date }
    Primary URL: { type: url }
    KPI target: { type: rich_text }
    KPI actual: { type: number }
    Tags: { type: multi_select }
    Notes: { type: rich_text }

    # Parent (tentpole) specific
    Series: { type: relation, related_db: Series DB }
    Tentpole publish date: { type: date }

    # Child (derivative) specific
    Tentpole: { type: relation, related_db: self }  # self-relation
    Derivative type: { type: select }  # e.g. "Audio→text" or "Long→short video"
```

Create rows via MCP:

```bash
npx @notionhq/mcp create_page \
  --database_id "$NOTION_EDITORIAL_DB" \
  --properties '{
    "Title":{"title":[{"text":{"content":"Ep 42 - newsletter writeup"}}]},
    "Status":{"select":{"name":"Drafting"}},
    "Format":{"select":{"name":"Newsletter issue"}},
    "Channel":{"select":{"name":"Newsletter"}},
    "Tentpole":{"relation":[{"id":"'"$TENTPOLE_ROW_ID"'"}]},
    "Schedule date":{"date":{"start":"2026-06-17"}}
  }'
```

### Recipe 2: Week-ahead query

```bash
# Filter all rows scheduled in next 7 days, sorted by date
npx @notionhq/mcp query_database \
  --database_id "$NOTION_EDITORIAL_DB" \
  --filter '{
    "and":[
      {"property":"Schedule date","date":{"next_week":{}}},
      {"property":"Status","select":{"does_not_equal":"Published"}}
    ]
  }' \
  --sorts '[{"property":"Schedule date","direction":"ascending"}]'
```

### Recipe 3: Backlog grooming (weekly)

```bash
# Pull "Backlog" status with no schedule date
npx @notionhq/mcp query_database \
  --database_id "$NOTION_EDITORIAL_DB" \
  --filter '{
    "and":[
      {"property":"Status","select":{"equals":"Backlog"}},
      {"property":"Schedule date","date":{"is_empty":true}}
    ]
  }'

# Rank by recency + relevance; promote top N to "Drafting" or "Scheduled"
```

### Recipe 4: Scheduled-this-week dashboard

```markdown
# This Week (Mon 2026-06-16 → Sun 2026-06-22)

## Tentpoles
| Date | Format | Title | Status |
|---|---|---|---|
| Tue 6am | Newsletter issue | Issue 042 | Scheduled |
| Wed 9am | Podcast episode | Ep 042: Tuesday-6am | Scheduled |
| Fri 10am | YouTube long | "Why MPP broke email" | Drafting |

## Derivatives queued
| Date | Format | Channel | Status |
|---|---|---|---|
| Tue 8pm | LinkedIn carousel | LinkedIn | Scheduled |
| Wed 10am | X thread | X cascade | Scheduled |
| Wed 6pm | Audiogram | IG + LinkedIn | Headliner auto |
| Thu 9am | Reels clip 1 | IG / TikTok / Shorts | Scheduled |
| Thu 6pm | Quote graphic 1 | IG / LinkedIn | Scheduled |
| Fri 9am | Reels clip 2 | IG / TikTok / Shorts | Scheduled |
```

### Recipe 5: Parent + child auto-create on tentpole intake

```python
# When new tentpole row is created, auto-spawn child derivative rows
def spawn_derivatives(tentpole_row_id, tentpole_format):
    DERIVATIVE_MAP = {
        'Newsletter issue': ['LinkedIn carousel', 'X thread', 'LinkedIn long-form', 'Blog post', 'Audio version', 'Quote graphic', 'Quote graphic', 'IG carousel'],
        'Podcast episode': ['Show notes', 'Audiogram', 'Reels clip 1', 'Reels clip 2', 'X thread', 'LinkedIn carousel', 'Blog post', 'Newsletter writeup', 'Quote graphic', 'YouTube full video', 'YouTube short'],
        'YouTube long': ['YouTube Shorts 1', 'YouTube Shorts 2', 'YouTube Shorts 3', 'Reels', 'TikTok', 'LinkedIn video', 'X thread', 'Newsletter issue', 'Blog post', 'Audiogram', 'Quote graphic'],
    }

    for fmt in DERIVATIVE_MAP.get(tentpole_format, []):
        notion_create_page(
            database_id=NOTION_EDITORIAL_DB,
            properties={
                'Title': {'title':[{'text':{'content':f"<tentpole title> - {fmt}"}}]},
                'Tentpole': {'relation':[{'id': tentpole_row_id}]},
                'Format': {'select':{'name': fmt}},
                'Status': {'select':{'name':'Backlog'}},
            }
        )
```

### Recipe 6: Buffer cascade integration

```bash
# When derivative row Status → "Scheduled", push to Buffer
DERIVATIVE_ROW_ID="<row_id>"
DERIVATIVE=$(npx @notionhq/mcp retrieve_page --page_id $DERIVATIVE_ROW_ID)

CONTENT=$(echo $DERIVATIVE | jq -r '.properties.Notes.rich_text[0].plain_text')
CHANNEL=$(echo $DERIVATIVE | jq -r '.properties.Channel.select.name')
SCHED_DATE=$(echo $DERIVATIVE | jq -r '.properties["Schedule date"].date.start')

npx @buffer/mcp-server create_post \
  --platform "$CHANNEL" \
  --content "$CONTENT" \
  --scheduled-at "$SCHED_DATE"
```

### Recipe 7: Status transitions

```yaml
# Allowed status flow:
Backlog → Drafting → Review → Scheduled → Published → Repurposing → Archived

# Auto-actions per transition:
Drafting → Review:
  - Notify editor via Notion mention
  - Run Vale slop scrub on draft markdown

Review → Scheduled:
  - Cross-check publish date against series cadence
  - Verify channel + UTM tags configured

Scheduled → Published:
  - Set Published date = today
  - Trigger Recipe 5: spawn derivative rows (if not yet)
  - Push to Buffer / Typefully / channel-native publisher

Published → Repurposing:
  - Trigger repurposing-pipeline-1-to-10 chain
  - 24h cooldown before re-promo

Repurposing → Archived:
  - 90 days post-publish
  - Move out of active editorial views
```

### Recipe 8: Notion DB views

```markdown
## Recommended views

1. **This Week** — calendar view filtered to Schedule date this/next week
2. **Backlog** — gallery view of unschedu rows, sorted by relevance
3. **Drafting** — list view of currently-being-written rows
4. **Per-channel** — Kanban grouped by Channel
5. **Per-series** — Kanban grouped by Series
6. **Owner** — table grouped by Owner / Author
7. **Analytics** — table sorted by KPI actual desc (post-publish performance roll-up)
```

### Recipe 9: Anti-drift maintenance (monthly clean-up)

```python
# Once per month, surface drift and clean up
def calendar_drift_audit():
    stale_drafting = notion_query(NOTION_EDITORIAL_DB, filter={
        'Status': {'select': {'equals': 'Drafting'}},
        'last_edited_time': {'before': 'now() - 14 days'}
    })

    orphan_derivatives = notion_query(NOTION_EDITORIAL_DB, filter={
        'Tentpole': {'relation': {'is_empty': True}},
        'Format': {'select': {'is_not_empty': True}}
    })

    print(f"Stale 'Drafting' (>14d no edit): {len(stale_drafting)}")
    print(f"Orphan derivatives (no Tentpole link): {len(orphan_derivatives)}")
    # Archive stale, link orphans, or alert owner
```

### Recipe 10: Sync to Google Calendar

```bash
# Notion Calendar integration in Notion dashboard;
# OR via API: query upcoming scheduled rows and create Google Calendar events

UPCOMING=$(npx @notionhq/mcp query_database --database_id $NOTION_EDITORIAL_DB \
  --filter '{"property":"Status","select":{"equals":"Scheduled"}}')

for ROW in $(echo $UPCOMING | jq -r '.results[]|.id'); do
  # Create gcal event via Google Calendar API
  # ...
done
```

### Recipe 11: KPI roll-up post-publish

```python
# 7 days after Published, populate KPI actual
from datetime import datetime, timedelta

newly_published = notion_query(NOTION_EDITORIAL_DB, filter={
    'Status': {'select': {'equals':'Published'}},
    'Published date': {'date': {'on_or_after': (datetime.now() - timedelta(days=7)).isoformat(),
                                'on_or_before': (datetime.now() - timedelta(days=6)).isoformat()}},
    'KPI actual': {'number': {'is_empty': True}},
})

for row in newly_published:
    fmt = row['properties']['Format']['select']['name']
    kpi = fetch_kpi_per_format(fmt, row['properties']['Primary URL']['url'])
    notion_update(row['id'], {'KPI actual': {'number': kpi}})
```

### Recipe 12: Repurposing status loop

```bash
# Periodically scan "Repurposing" status; for each, ensure derivative rows exist + scheduled
REPURP=$(npx @notionhq/mcp query_database --database_id $NOTION_EDITORIAL_DB \
  --filter '{"property":"Status","select":{"equals":"Repurposing"}}')

for TENT in $(echo $REPURP | jq -r '.results[]|.id'); do
  CHILDREN=$(npx @notionhq/mcp query_database --database_id $NOTION_EDITORIAL_DB \
    --filter '{"property":"Tentpole","relation":{"contains":"'"$TENT"'"}}')
  COUNT=$(echo $CHILDREN | jq '.results|length')
  if [ "$COUNT" -lt 8 ]; then
    echo "Tentpole $TENT has only $COUNT derivatives; needs more queued"
  fi
done
```

## Examples

### Example 1: Weekly Monday planning ritual

**Goal:** Every Monday, set the week's editorial calendar.

**Steps:**
1. Recipe 2: query upcoming-week scheduled rows.
2. Recipe 3: groom backlog → schedule 2-3 more rows if needed.
3. Recipe 4: assemble dashboard view of the week.
4. Send dashboard to team Slack / email.
5. Confirm Buffer schedules are in (Recipe 6).

**Result:** Team aligned on week's editorial plan in <30 min.

### Example 2: New tentpole intake

**Goal:** Add a new podcast episode to the calendar with all 10 derivatives queued.

**Steps:**
1. Create new row in Editorial DB with Format=Podcast episode, Status=Backlog.
2. Recipe 5: auto-spawn 10 child derivative rows.
3. Editor reviews + sets KPI target + tentpole publish date.
4. Status → Drafting → Review → Scheduled.
5. Recipe 6: Buffer schedules each derivative on publish.

**Result:** Full 1-to-10 pipeline tracked in single DB.

### Example 3: Monthly drift audit

**Goal:** Clean up stale rows before they pile up.

**Steps:**
1. Recipe 9: query stale Drafting + orphan derivatives.
2. For each stale row: ping owner / archive if irrelevant.
3. For each orphan: link to correct tentpole or archive.
4. Recipe 11: backfill KPI actual for newly-published rows.

**Result:** Clean DB; no stale rows lingering.

## Edge cases / gotchas

- **Notion DB relations can ORPHAN** when a parent row is deleted. Use rollups + the orphan audit (Recipe 9) to catch.
- **Notion DB query rate limit = 3 req/s** average. Bulk operations need delay.
- **Self-relation (Tentpole linking to another row in the same DB)** is supported but UX shows both sides; can confuse editors. Document the relationship direction.
- **Don't over-tag** — Format + Channel are mandatory; Tags should be 1-2 per row max.
- **Single source of truth** — don't duplicate the editorial DB across team Slack / Trello / spreadsheet. Stale duplicates kill trust in the canonical DB.
- **Notion's date-filter syntax** uses different keys (`equals`, `before`, `next_week`, etc.). Reference the API docs.
- **Schedule dates in UTC** to avoid timezone drift across team members.
- **Buffer schedules are per-platform** — don't assume one Notion row → one Buffer post unless Channel = single platform.
- **Status transitions should be enforced via workflow** — don't let "Backlog" jump directly to "Published" without intermediate states.
- **Backlog should never exceed 50 rows** — anything bigger is a wish list, not a backlog. Archive aggressively.
- **KPI target should be set BEFORE Published**, not retroactively. Otherwise it's vanity.
- **Don't reuse Notion DB across multiple agents** — content-creator's editorial DB ≠ marketing-agent's campaign DB. Keep separate.
- **Notion calendar views break with >500 dated rows** in a view — filter aggressively.
- **Export the DB monthly** as CSV backup; Notion downtime + accidental deletion happens.

## Sources

- [Notion editorial calendar template](https://www.notion.com/templates/editorial-calendar)
- [Notion AI content calendar with Claude](https://espressio.ai/blog/claude-notion-content-calendar)
- [Notion API docs](https://developers.notion.com/)
- [Buffer GraphQL + MCP](https://mcpmarket.com/server/buffer)
- [Notion MCP](https://github.com/makenotion/notion-mcp-server)
