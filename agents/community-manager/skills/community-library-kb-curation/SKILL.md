<!--
Sources: https://www.notion.com/help + https://slab.com/ + https://tettra.com/ + https://stackoverflowteams.com/ + https://meta.discourse.org/ + https://lychee.cli.rs/ + https://github.com/wilsonzlin/crawley
-->
# Community Library + KB Curation — SKILL

Community-side knowledge base curation: Notion / Slab / Tettra / Stack Overflow for Teams / Outline / Confluence for source-of-truth; community-side curation via pinned messages, FAQ channels, Discord forum channels, Discourse FAQ category. Drift detection: zero-result searches, unanswered top topics, stale pinned content. Cross-link from KB to community for "still stuck?" path. Weekly drift report + auto-draft new KB entries with member-question citations.

## When to use

- New KB build for a growing community.
- Existing KB lacking discoverability / weekly drift.
- Migration from one KB SaaS to another.
- Zero-result search analytics surfacing unmet info needs.
- Pinned-message overflow on Discord / Slack — needs canonicalization.
- Discourse FAQ category SEO grooming.
- Auto-drafting KB articles from top community Q&A threads.
- Dead-link sweep + reorganize after a major release / rename.
- Tie KB articles to support ticket deflection metrics (cross-link `community-roi-retention-expansion-advocacy` Recipe 5).

Trigger phrases: "community KB", "knowledge base", "FAQ channel", "Notion KB", "Slab", "Tettra", "drift report", "zero-result search", "pinned messages", "Discourse FAQ", "auto-draft KB", "documentation drift", "Lychee", "dead-link sweep".

## Setup

```bash
# Notion API for KB DB
mcp tool notion-mcp.databases_query --database_id $KB_DB_ID \
  --filter '{"property":"Last reviewed","date":{"before":"'$(date -d '90 days ago' -I)'"}}'

# Slab API
curl -H "Authorization: Bearer $SLAB_TOKEN" https://api.slab.com/topics

# Tettra
curl -H "Authorization: Bearer $TETTRA_TOKEN" https://api.tettra.com/v1/pages

# Stack Overflow for Teams
curl -H "X-API-Access-Token: $SO_TEAMS_TOKEN" \
  "https://YOUR-INSTANCE.stackenterprise.co/api/2.3/questions?site=stackoverflow&team=brand"

# Discourse FAQ category
curl -H "Api-Key: $DISCOURSE_API_KEY" -H "Api-Username: system" \
  "https://forum.brand.com/c/faq/15.json"

# Discord pinned + threads in forum channels
mcp tool discord-mcp-full.list_pinned_messages --channel_id $CHANNEL_ID
mcp tool discord-mcp-full.list_active_threads --guild_id $GUILD_ID

# Lychee dead-link sweep
uvx lychee --max-concurrency 10 \
  --exclude-path '*.test.md' \
  --base-url https://kb.brand.com \
  https://kb.brand.com/sitemap.xml > lychee-report.json

# Sitemap / crawler
uvx crawley https://kb.brand.com --max-depth 4 --json > urls.json
```

Auth + env:
- `NOTION_TOKEN` — Notion integration in workspace.
- `SLAB_TOKEN` — Slab → Profile → API.
- `TETTRA_TOKEN` — Tettra → Admin → API.
- `SO_TEAMS_TOKEN` — Stack Overflow → Account → API Access Tokens.
- `DISCOURSE_API_KEY` + `DISCOURSE_API_USERNAME` — Discourse admin.
- `DISCORD_BOT_TOKEN` — for pinned + forum channel queries.
- `LYCHEE` — `uvx lychee` runs ad hoc; no token.

Workspace prerequisites:
- KB SoT (Notion / Slab / etc.) with `Last reviewed`, `Owner`, `Topic` properties.
- Sitemap or article registry for crawl.
- Community search-zero-result logs.
- Slack `#kb-drift` channel for weekly report.
- Notion DB `Community KB Drift Report` for archive.

## Common recipes

### Recipe 1: KB tool selection matrix

| Profile | Tool | Why |
|---|---|---|
| Modern SoT + community embed | Notion | Flexible blocks; great public sharing |
| KB SaaS focused | Slab or Tettra | Built for KB; better search; SaaS managed |
| Technical Q&A | Stack Overflow for Teams | Vote-based, upvote sort, SEO-friendly internal |
| Self-hosted FOSS | Outline | Markdown + Postgres; full control |
| Enterprise (regulated) | Confluence | Mature; access controls; compliance |
| Public + community-as-SEO | Discourse FAQ | Same forum already hosts community |
| Dev docs site | Mintlify / Docusaurus | Code-block + version control |

Default: Notion for modern; Discourse FAQ if Discourse already running.

### Recipe 2: Notion KB structure

```yaml
# Notion DB schema
KB Articles:
  properties:
    Title: title
    URL slug: text
    Topic: multi-select [Onboarding, Billing, Integrations, Roadmap, Troubleshooting, ...]
    Owner: person
    Status: select [Draft, Published, Archived, Stale]
    Last reviewed: date
    Next review due: date  # formula: Last reviewed + 90d
    Source threads: relation → Community Threads DB
    Linked KB: relation → KB Articles (self)
    Views (30d): number
    Helpful votes: number
    Last edited: created_time
```

### Recipe 3: Weekly drift report

```python
# Run every Friday; surface drift signals
import datetime, requests

today = datetime.date.today()

# Stale articles (not reviewed in 90+ days)
stale = notion.databases_query(
    database_id=KB_DB_ID,
    filter={
        "and": [
            {"property": "Status", "select": {"equals": "Published"}},
            {"property": "Last reviewed", "date": {"before": (today - datetime.timedelta(days=90)).isoformat()}}
        ]
    }
)["results"]

# Articles with declining views
declining = notion.databases_query(
    database_id=KB_DB_ID,
    filter={"property": "Views (30d)", "number": {"less_than": 5}}
)["results"]

# Zero-result searches (last 7 days)
zero_results = postgres.query("""
SELECT query, COUNT(*) AS cnt
FROM search_logs
WHERE results_count = 0 AND ts > now() - interval '7 days'
GROUP BY 1 ORDER BY 2 DESC LIMIT 20;
""")

# Unanswered top community threads
unanswered = discord_full.list_active_threads(guild_id=GUILD)
unanswered = [t for t in unanswered if t["message_count"] < 3 and t["age_days"] > 3]

# Post drift report
slack_mcp.chat_postMessage(
    channel="#kb-drift",
    text=f"""*Weekly KB drift — {today}*

:warning: {len(stale)} articles overdue for review
:chart_with_downwards_trend: {len(declining)} articles with <5 views in 30d
:mag: Top zero-result searches: {", ".join(r['query'] for r in zero_results[:5])}
:question: {len(unanswered)} unanswered community threads aged >3d

See: {KB_DB_PUBLIC_URL}?filter=stale-this-week
""",
)
```

### Recipe 4: Auto-draft KB from community Q&A

```python
import anthropic
client = anthropic.Anthropic()

# Pull resolved community threads in last 7 days
threads = discord_full.list_threads_resolved(guild_id=GUILD, days_back=7)

for t in threads:
    msgs = discord_full.list_messages(channel_id=t["id"])
    question = msgs[0]["content"]
    answers = "\n".join(m["content"] for m in msgs[1:])

    resp = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1500,
        system="""You synthesize a community Q&A thread into a publishable KB article.

Output JSON:
{
  "title": "How to … (action verb)",
  "topic": "Onboarding|Billing|Integrations|Roadmap|Troubleshooting|Other",
  "summary": "2-sentence summary",
  "body": "Markdown body. Sections: Problem / Steps / Why this works / Related",
  "tags": ["tag1","tag2"],
  "source_thread_url": "the Discord thread URL"
}

Style: technical writing voice, no fluff, code blocks where applicable.""",
        messages=[{
            "role": "user",
            "content": f"Question: {question}\n\nAnswers (multiple voices):\n{answers}"
        }],
    )
    draft = json.loads(resp.content[0].text)

    # Create Notion KB page in Draft state
    notion.pages_create(
        parent={"database_id": KB_DB_ID},
        properties={
            "Title": {"title": [{"text": {"content": draft["title"]}}]},
            "Topic": {"multi_select": [{"name": draft["topic"]}]},
            "Status": {"select": {"name": "Draft"}},
            "Owner": {"people": [{"id": KB_AUTO_DRAFT_USER}]},
            "Last reviewed": {"date": {"start": str(today)}},
        },
        children=markdown_to_notion_blocks(draft["body"] + f"\n\n---\nSource: {t['url']}"),
    )
```

Notion DB receives drafts; KB owner reviews + publishes weekly batch.

### Recipe 5: Dead-link sweep via Lychee

```bash
# Crawl KB + flag dead links
uvx lychee \
  --max-concurrency 16 \
  --timeout 20 \
  --accept 200,206,302 \
  --base-url https://kb.brand.com \
  --output lychee.json \
  --format json \
  https://kb.brand.com/sitemap.xml

# Filter to dead links only
jq '.fail[] | {url:.url, status:.status.code, source:.source}' lychee.json > dead-links.json

# Open Linear issue per cluster
jq -r '.url' dead-links.json | sort -u | while read url; do
  mcp tool linear-mcp.create_issue \
    --team_id $KB_TEAM \
    --title "Fix dead link: $url" \
    --labels kb-drift,dead-link \
    --priority "Medium"
done
```

### Recipe 6: Zero-result search → KB authoring queue

```python
# Postgres search_logs table: each search w/ query + results_count
top_zero = postgres.query("""
SELECT query, COUNT(*) AS searches, COUNT(DISTINCT searcher_id) AS searchers
FROM search_logs
WHERE results_count = 0 AND ts > now() - interval '30 days'
GROUP BY 1
ORDER BY searches DESC
LIMIT 25;
""")

# For each, ask Claude: is this an authoring need? What's the article shape?
for row in top_zero:
    if row["searchers"] < 3:
        continue  # noise floor
    resp = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=400,
        system="Given a community search query that returned zero results, draft a 1-line article title + topic + estimated effort to write.",
        messages=[{"role":"user","content":row["query"]}],
    )
    # Create Notion DB row in "Authoring queue" status
    notion.pages_create(
        parent={"database_id": AUTHORING_QUEUE_DB},
        properties={
            "Title": {"title": [{"text": {"content": resp.content[0].text.split('\n')[0]}}]},
            "Source query": {"rich_text": [{"text": {"content": row["query"]}}]},
            "Demand": {"number": row["searches"]},
            "Distinct searchers": {"number": row["searchers"]},
            "Status": {"select": {"name": "Backlog"}},
        }
    )
```

### Recipe 7: Discord forum-channel KB conversion

Discord Forum channels are well-suited as semi-KB:

```bash
# Identify well-resolved threads in #help-forum
mcp tool discord-mcp-full.list_threads \
  --channel_id $HELP_FORUM_CH \
  --is_resolved true

# Pin top-voted resolved threads
mcp tool discord-mcp-full.pin_message \
  --channel_id $THREAD_ID --message_id $TOP_REPLY_ID

# Add canonical tags
mcp tool discord-mcp-full.set_thread_tags \
  --thread_id $THREAD_ID \
  --tag_ids '["resolved","canonical","kb-promoted"]'
```

Then expose via `discord-mcp-full.search_threads` for community.

### Recipe 8: Discourse FAQ category grooming

```bash
# Pull topics + sort by view count
curl -H "Api-Key: $DISCOURSE_API_KEY" -H "Api-Username: system" \
  "https://forum.brand.com/c/faq/15.json?order=views" | \
  jq '.topic_list.topics[] | select(.views > 100) | {id, slug, views, last_posted_at}'

# Move under-viewed FAQ topics to "archive"
for topic_id in $UNDER_VIEWED_IDS; do
  curl -X PUT -H "Api-Key: $DISCOURSE_API_KEY" -H "Api-Username: system" \
    "https://forum.brand.com/t/-/$topic_id.json" \
    -d '{"category_id": 99}'  # archive category
done

# Edit canonical FAQ topics with last-reviewed footer
curl -X PUT -H "Api-Key: $DISCOURSE_API_KEY" -H "Api-Username: system" \
  "https://forum.brand.com/posts/$POST_ID.json" \
  -d '{"post": {"raw": "'$NEW_BODY'", "edit_reason": "Quarterly FAQ review"}}'
```

### Recipe 9: Stack Overflow for Teams Q&A canonicalization

```bash
# Find duplicate Q's
curl -H "X-API-Access-Token: $SO_TEAMS_TOKEN" \
  "https://INSTANCE.stackenterprise.co/api/2.3/questions?team=brand&sort=duplicate"

# Mark dup
curl -X POST -H "X-API-Access-Token: $SO_TEAMS_TOKEN" \
  "https://INSTANCE.stackenterprise.co/api/2.3/questions/$QID/duplicate" \
  -d "original_id=$ORIG_ID"

# Top tags by question volume
curl -H "X-API-Access-Token: $SO_TEAMS_TOKEN" \
  "https://INSTANCE.stackenterprise.co/api/2.3/tags?team=brand&sort=popular"
```

### Recipe 10: Cross-link KB article ↔ community thread

```python
# When KB article published, find source threads and tag w/ link
def crosslink_published_article(article):
    sources = article["properties"]["Source threads"]["relation"]
    for s_id in [s["id"] for s in sources]:
        # Reverse: each source thread DB row gets link to article
        notion.pages_update(
            page_id=s_id,
            properties={
                "KB article": {"relation": [{"id": article["id"]}]},
            }
        )
        # Discord: reply in original thread w/ "We wrote this up: <link>"
        thread_url = notion.pages_retrieve(s_id)["properties"]["Discord URL"]["url"]
        channel_id, message_id = parse_discord_url(thread_url)
        discord_full.create_message(
            channel_id=channel_id,
            content=(
                f":books: We turned this thread into a KB article: <{article['url']}>. "
                f"Thanks to everyone who contributed!"
            ),
            message_reference={"message_id": message_id},
        )
```

## Examples

### Example 1: Net-new KB build (Discord-first community)

**Goal:** 3-month-old Discord community wants KB foundation.

**Steps:**
1. Notion KB DB created (Recipe 2).
2. Top 25 community questions identified (Recipe 6 zero-result + Discord top-replied threads).
3. Auto-draft 25 articles (Recipe 4) → reviewed by community lead.
4. Publish; pin links in #help channel.
5. Weekly drift report (Recipe 3).

**Result:** Month 1: 25 articles published. Month 3: 60% of new-member questions answered by KB before asking.

### Example 2: Migrate from Confluence to Notion

**Goal:** Legacy Confluence KB, drifting; team wants Notion.

**Steps:**
1. Export Confluence to HTML + Markdown via `confluence-cli`.
2. Bulk import to Notion KB DB (Recipe 2 schema).
3. Lychee dead-link sweep (Recipe 5) on imported set.
4. Owner assignment per topic.
5. Re-publish + 301 redirects from old URLs.

**Result:** 340 articles migrated; ~15% dead links cleaned; 90-day review cadence set up.

### Example 3: Discourse FAQ refresh (quarterly)

**Goal:** Discourse forum FAQ category drifted; want fresh + searchable.

**Steps:**
1. Pull all FAQ topics by views (Recipe 8).
2. Top 30 → reviewed + last-reviewed footer added.
3. Bottom 50% (under-viewed + > 6 months) → moved to archive category.
4. Cross-link from Discord/Slack pinned messages → top FAQ topics.
5. Run Lychee sweep on FAQ category URLs.

**Result:** Avg FAQ view rate +25% after refresh; clean signal for future drift cycle.

## Edge cases / gotchas

- **Stale pin overflow** — Discord caps pinned messages at 50/channel. Convert old pins to Forum threads + KB.
- **Auto-draft hallucination** — Claude can synthesize wrong fixes from incomplete threads. Always require human review before publish.
- **Discourse FAQ → Google indexing latency** — moving topics changes URLs → SEO transient drop. Use 301 redirects via Discourse Redirect plugin.
- **Owner abandonment** — KB authors leave team; articles orphan. Quarterly owner audit.
- **Notion public-share rate limit** — public KB pages have 60 req/min per source IP. Cache or use Notion API → static site.
- **Cross-platform drift** — KB on Notion, Discourse FAQ, Discord pinned, Slack canvas — same content authored 4x. Pick ONE canonical source; others link to it.
- **Auto-archive aggressive** — under-viewed doesn't always mean stale. Set min view < 5 and age > 6mo + flagging.
- **Lychee timeout floods** — large KB on slow CDN times out. Use `--timeout 60` + retry.
- **Multi-language KB** — KB in EN; community in 5 languages. Drift on each language; track separately or DeepL pipeline.
- **Outdated screenshots** — UI changes; screenshots lag. Tag articles with UI version; auto-flag when product UI bumps.
- **Forum-channel pollution** — Discord Forum used for unmoderated chatter mingles with help. Separate `#help-forum` from `#general-forum`.
- **Search analytics privacy** — search-logs are PII if query contains identifiers. Hash or truncate.

## Sources

- [Notion API reference](https://developers.notion.com/reference/intro)
- [Notion docs as KB best practices](https://www.notion.com/help/category/knowledge-bases)
- [Slab API](https://api.slab.com/docs)
- [Tettra help](https://docs.tettra.co/)
- [Stack Overflow for Teams API](https://api.stackexchange.com/docs)
- [Discourse API](https://docs.discourse.org/)
- [Discourse FAQ category pattern](https://meta.discourse.org/t/getting-started-with-categories/2769)
- [Lychee link checker](https://lychee.cli.rs/)
- [Outline KB](https://www.getoutline.com/)
- [Confluence Cloud REST API](https://developer.atlassian.com/cloud/confluence/rest/v2/)
