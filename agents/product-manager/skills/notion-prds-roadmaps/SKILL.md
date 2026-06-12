<!--
Source: https://developers.notion.com/docs/mcp
Notion MCP remote, GA late 2025
ChatPRD rubric: https://www.chatprd.ai
-->
# Notion PRDs + Roadmaps — SKILL

Notion is the narrative home for PRDs, research repos, roadmap docs, strategy docs, and stakeholder updates. This pack covers template-driven page creation, embedded Linear/Figma blocks, and programmatic PRD review against the ChatPRD/Kraftful-style rubric.

## When to use

- Drafting PRDs (1-pager + full template) into a Notion database.
- Building a roadmap doc that embeds Linear projects + initiatives.
- Running the PRD review rubric against an existing Notion PRD.
- Setting up the research repository (Notion DB of interview synthesis entries).
- Publishing the weekly/monthly stakeholder update to a Notion archive page.
- Writing the annual strategy doc (Rumelt kernel + 7 Powers).

Trigger phrases: "write a PRD for X", "draft the roadmap doc", "review this PRD", "set up a research repo", "publish the weekly update", "write our annual strategy".

## Setup

```bash
# Notion remote MCP — preferred, GA
# Install via CraftBot MCP catalog OR connect via Notion's hosted MCP endpoint.
# Standalone fallback uses Notion REST API directly:
curl -fsSL "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"
```

Auth:
- `NOTION_API_KEY` — internal integration token from https://www.notion.so/my-integrations. Free.
- Share the target databases with the integration before any writes.

MCP tools available (`notion-mcp`):
- `create_page` (parent: page or database)
- `update_page` (properties + content blocks)
- `append_block_children` (add to existing page)
- `query_database` (filter + sort)
- `retrieve_page` / `retrieve_database`
- `create_database` / `update_database_schema`

## Common recipes

### Recipe 1: Create a 1-pager PRD in the PRD database

```bash
mcp tool notion.create_page \
  --parent '{"database_id":"<prd-db-id>"}' \
  --properties '{
    "Name":{"title":[{"text":{"content":"Onboarding revamp — 1-pager"}}]},
    "Status":{"select":{"name":"Draft"}},
    "Author":{"people":[{"id":"<user-id>"}]},
    "Linear Project":{"url":"https://linear.app/team/project/onboarding-revamp"}
  }' \
  --children '[
    {"object":"block","type":"heading_1","heading_1":{"rich_text":[{"text":{"content":"Problem"}}]}},
    {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"text":{"content":"Solo founders abandon onboarding before reaching first value (35% D7 retention; 8 of 11 interview signal)."}}]}},
    {"object":"block","type":"heading_1","heading_1":{"rich_text":[{"text":{"content":"Hypothesis"}}]}},
    {"object":"block","type":"paragraph","paragraph":{"rich_text":[{"text":{"content":"If we add a 3-step in-product checklist, then D7 retention will rise from 35% → 42% by Q3 because friction in time-to-first-value is the documented blocker."}}]}}
  ]'
```

### Recipe 2: Run the PRD review rubric programmatically

```python
# Reads an existing PRD; checks 11 rubric items; returns gap list.
import requests
import re

NOTION = "https://api.notion.com/v1"
H = {"Authorization": f"Bearer {NOTION_API_KEY}", "Notion-Version": "2022-06-28"}

def get_page_text(page_id):
    blocks = requests.get(f"{NOTION}/blocks/{page_id}/children?page_size=100", headers=H).json()["results"]
    out = []
    for b in blocks:
        t = b.get("type")
        if t and b[t].get("rich_text"):
            out.append("".join(rt["plain_text"] for rt in b[t]["rich_text"]))
    return "\n".join(out)

def review(text):
    gaps = []
    if not re.search(r"problem", text, re.I): gaps.append("Missing Problem section")
    if not re.search(r"hypothesis|if .* then", text, re.I): gaps.append("Missing testable hypothesis")
    if not re.search(r"\d+%|\d+x", text): gaps.append("No quantitative success criteria")
    if not re.search(r"non[- ]goal", text, re.I): gaps.append("No explicit non-goals")
    if not re.search(r"primary user|target user", text, re.I): gaps.append("No named primary user")
    if not re.search(r"open question", text, re.I): gaps.append("No open questions listed")
    if not re.search(r"risk", text, re.I): gaps.append("No risks section")
    if re.search(r"\b(improve|optimize|leverage|enhance|streamline)\b", text, re.I):
        gaps.append("Vague verbs detected — replace with concrete action")
    if not re.search(r"event|tracking|analytics", text, re.I): gaps.append("No tracking spec")
    if not re.search(r"figma|design", text, re.I): gaps.append("No design dependency")
    return gaps

gaps = review(get_page_text("<prd-page-id>"))
print(gaps)
```

### Recipe 3: Quarterly roadmap doc with embedded Linear

```bash
mcp tool notion.create_page \
  --parent '{"page_id":"<workspace-root>"}' \
  --properties '{"title":[{"text":{"content":"Q3 2026 Roadmap"}}]}' \
  --children '[
    {"type":"callout","callout":{"rich_text":[{"text":{"content":"This is a hypothesis, not a contract. NOW is committed. NEXT is best-current-bet. LATER is intent only."}}],"icon":{"emoji":"🎯"}}},
    {"type":"heading_2","heading_2":{"rich_text":[{"text":{"content":"OKR alignment"}}]}},
    {"type":"bulleted_list_item","bulleted_list_item":{"rich_text":[{"text":{"content":"O1: D7 retention 35% → 42% — addressed by onboarding revamp + in-product checklist"}}]}},
    {"type":"heading_2","heading_2":{"rich_text":[{"text":{"content":"NOW (committed)"}}]}},
    {"type":"embed","embed":{"url":"https://linear.app/team/initiative/q3-activation-revamp"}}
  ]'
```

### Recipe 4: Set up the research repository database

```bash
mcp tool notion.create_database \
  --parent '{"page_id":"<research-page>"}' \
  --title '[{"text":{"content":"Research Repository"}}]' \
  --properties '{
    "Topic":{"title":{}},
    "Date":{"date":{}},
    "Method":{"select":{"options":[{"name":"Interview"},{"name":"Survey"},{"name":"Analytics"},{"name":"Support"},{"name":"Sales calls"}]}},
    "Sample size":{"number":{"format":"number"}},
    "Themes":{"multi_select":{}},
    "Linked PRDs":{"relation":{"database_id":"<prd-db>"}},
    "Dovetail link":{"url":{}}
  }'
```

### Recipe 5: Append a weekly update to the archive

```bash
mcp tool notion.append_block_children \
  --block_id "<weekly-update-archive-page>" \
  --children '[
    {"type":"heading_2","heading_2":{"rich_text":[{"text":{"content":"Week of 2026-06-09"}}]}},
    {"type":"heading_3","heading_3":{"rich_text":[{"text":{"content":"Wins"}}]}},
    {"type":"bulleted_list_item","bulleted_list_item":{"rich_text":[{"text":{"content":"D7 retention 35% → 38% (Amplitude funnel; onboarding revamp shipped Mon)"}}]}},
    {"type":"heading_3","heading_3":{"rich_text":[{"text":{"content":"Lowlights"}}]}},
    {"type":"bulleted_list_item","bulleted_list_item":{"rich_text":[{"text":{"content":"Notif center slipped 1 week — API rate-limit; new ETA 2026-06-22"}}]}}
  ]'
```

### Recipe 6: Strategy doc (Rumelt kernel)

```bash
mcp tool notion.create_page \
  --parent '{"page_id":"<strategy-folder>"}' \
  --properties '{"title":[{"text":{"content":"Annual Strategy 2026"}}]}' \
  --children '[
    {"type":"heading_1","heading_1":{"rich_text":[{"text":{"content":"Diagnosis"}}]}},
    {"type":"paragraph","paragraph":{"rich_text":[{"text":{"content":"What is happening in the market and inside our product."}}]}},
    {"type":"heading_1","heading_1":{"rich_text":[{"text":{"content":"Guiding policy"}}]}},
    {"type":"paragraph","paragraph":{"rich_text":[{"text":{"content":"Our approach. The angle. The bet."}}]}},
    {"type":"heading_1","heading_1":{"rich_text":[{"text":{"content":"Coherent actions"}}]}},
    {"type":"paragraph","paragraph":{"rich_text":[{"text":{"content":"The specific moves we will make this year."}}]}},
    {"type":"heading_1","heading_1":{"rich_text":[{"text":{"content":"Moat (7 Powers)"}}]}},
    {"type":"paragraph","paragraph":{"rich_text":[{"text":{"content":"Which 1-3 powers we are building and how."}}]}}
  ]'
```

### Recipe 7: Query the PRD DB for "drafts older than 14 days"

```bash
mcp tool notion.query_database \
  --database_id "<prd-db>" \
  --filter '{"and":[
    {"property":"Status","select":{"equals":"Draft"}},
    {"property":"Last edited","date":{"before":"2026-05-26"}}
  ]}' \
  --sorts '[{"property":"Last edited","direction":"ascending"}]'
```

### Recipe 8: Add a Linear-issue linked database to a PRD

```bash
# Notion supports embedded Linear via the Linear-Notion integration.
# Add a linked-DB block pointing at the Linear team's view.
mcp tool notion.append_block_children \
  --block_id "<prd-page-id>" \
  --children '[
    {"type":"link_to_page","link_to_page":{"page_id":"<linear-linked-db-page>"}}
  ]'
```

## Examples

### Example 1: New PRD from intake to review
**Goal:** Convert a discovery brief into a 1-pager PRD and run review.

**Steps:**
1. Read the discovery brief (Notion page in Discovery DB).
2. Generate 1-pager PRD via `create_page` with PRD template (Recipe 1).
3. Run the rubric via Recipe 2; surface gaps as inline comments via `update_page` with annotation blocks.
4. Status: `Draft → Ready for review` once gaps are zero.

**Result:** PRD page in Notion + populated `Status` + linked discovery doc + rubric pass.

### Example 2: Quarterly roadmap kickoff doc
**Goal:** Stand up the Q3 roadmap page that links to Linear initiatives.

**Steps:**
1. Pull active Linear initiatives via `linear-product-management` Recipe 9.
2. Create the roadmap page via Recipe 3 with the now/next/later structure.
3. Embed each Linear initiative URL as a child block.
4. Share with #product-leads via `slack-mcp`.

**Result:** A single Notion page that exec/eng/all-hands all link to.

## Edge cases / gotchas

- **Integration must be invited.** A new integration cannot read/write a database it has not been added to. Each DB needs explicit share.
- **Rich-text length cap.** Blocks max ~2000 characters of rich text; split long paragraphs into multiple blocks.
- **Rate limits.** Notion enforces ~3 requests/sec; bursty bulk writes throttle. Use 350 ms between calls or batch with `append_block_children`.
- **Schema drift.** `properties` writes fail on unknown field names; query the DB schema first if fields are user-defined.
- **API versioning.** Header `Notion-Version: 2022-06-28` is current stable; newer versions exist but not all features are GA.
- **Database vs page parent.** A "page" with `database_id` parent becomes a row; a "page" with `page_id` parent is a regular sub-page. They behave differently for queries.
- **Comments are NOT pages.** Inline comments require the dedicated comments API (`/comments`), not block children.
- **No Markdown import.** Notion does NOT accept Markdown directly — convert via `markdown-converter` skill or compose block-by-block.
- **Public sharing.** Pages created via API are not public by default; sharing must be done manually OR via Notion's site-publishing feature.

## Sources

- [Notion API reference](https://developers.notion.com/reference)
- [Notion MCP overview](https://developers.notion.com/docs/mcp)
- [Block object types](https://developers.notion.com/reference/block)
- [Database queries](https://developers.notion.com/reference/post-database-query)
- [ChatPRD rubric reference](https://www.chatprd.ai)
- [Kraftful PRD coach](https://kraftful.com)
- [Lenny's PRD template guide](https://www.lennysnewsletter.com/p/the-ultimate-guide-to-writing-prds)
