<!--
Sources: https://www.productboard.com/integrations/ + https://canny.io/ + https://www.featurebase.app/ + https://linear.app/docs + https://developers.notion.com/
-->
# Community Feedback Loop → Product — SKILL

Closed-loop pipeline from community feedback channel(s) → cluster → top-N per week → product portal (Productboard / Canny / Featurebase / Linear) → product team review → reverse-sync status updates back to community ("shipped" reaction; "in progress" status; "won't fix" with rationale). Public roadmap for transparency.

## When to use

- Setting up the community → product feedback pipeline for the first time.
- Existing #feedback channel but nothing actionable downstream.
- Community asking "what happens to my feedback?" — need to ship the reverse-sync.
- Quarterly feedback-loop audit (top-N requested vs delivered).
- Migration from manual triage to clustered + scored automation.
- Tier-1 feature feedback prioritization with member-count weighting.
- Beta-program feedback structured intake.
- Cross-link to `community-led-plg-motion` (PLG-driven feedback as activation signal).

Trigger phrases: "feedback loop", "feature request", "community feedback", "Productboard", "Canny", "Featurebase", "Linear feedback", "reverse sync", "feature voting", "public roadmap", "feedback portal".

## Setup

```bash
# Productboard
export PRODUCTBOARD_TOKEN=$(op item get productboard --fields token)
curl -H "Authorization: Bearer $PRODUCTBOARD_TOKEN" \
  -H "X-Version: 1" \
  https://api.productboard.com/notes

# Canny
export CANNY_API_KEY=$(op item get canny --fields api_key)
curl -X POST https://canny.io/api/v1/posts/create \
  -H "Content-Type: application/json" \
  -d "{\"apiKey\":\"$CANNY_API_KEY\",\"authorID\":\"USER_ID\",\"boardID\":\"BOARD\",\"title\":\"Better search\",\"details\":\"From community: ...\"}"

# Featurebase
curl -H "Authorization: Bearer $FEATUREBASE_TOKEN" \
  https://app.featurebase.app/api/v1/posts

# Linear (already via linear-mcp)
mcp tool linear-mcp.create_issue \
  --team_id $LINEAR_TEAM \
  --title "Feature: Better search" \
  --description "Community ask. See community thread links below." \
  --labels community-source,product-feedback
```

Auth + env:
- `PRODUCTBOARD_TOKEN` — Productboard → Settings → Integrations → Public API.
- `CANNY_API_KEY` — canny.io → Settings → API. Free tier supports 1 board.
- `FEATUREBASE_TOKEN` — featurebase.app → Settings → API.
- `LINEAR_API_KEY` — Linear → Settings → API → Personal API key.
- `NOTION_TOKEN` — for public roadmap mirror.
- `DISCORD_BOT_TOKEN` + `SLACK_BOT_TOKEN` — for in-community reverse-sync posts.

Workspace prerequisites:
- Community channels: `#feedback` (Discord), `#product-feedback` (Slack), `feedback` tag (Circle/Discourse).
- Tags: `product-feedback`, `bug`, `feature-request`, `pricing-feedback`.
- Labels in destination portal: `community-source`, `member-count:N`, `tier:champion`.
- Public roadmap URL (Notion / Productboard portal / Canny board).
- "Status" reactions in community: ✅ shipped, 🔧 in-progress, 🤔 considering, ❌ wont-fix.

## Common recipes

### Recipe 1: Portal selection matrix

| Profile | Tool | Why |
|---|---|---|
| Engineering-led, want issue-tracker-native | Linear | Best dev workflow; public roadmap option |
| PM-led, formal prioritization | Productboard | Best taxonomy + roadmap + voting |
| Public + community-voted | Canny | Best UI for public voting + status |
| Lightweight + cheap | Featurebase | Cheaper Canny alt, public boards |
| Free / no portal | Notion + Discord thread voting | Manual but $0 |

Default: Linear if engineering-led; Productboard for B2B PM; Canny for public-facing.

### Recipe 2: Weekly feedback channel sweep (Discord)

```python
# Pull last 7 days of #feedback posts
import datetime
from discord_full import client

since = datetime.datetime.utcnow() - datetime.timedelta(days=7)
msgs = client.list_messages(channel_id=FEEDBACK_CH, after=since)

posts = [{
    "id": m["id"],
    "author_id": m["author"]["id"],
    "author_name": m["author"]["username"],
    "text": m["content"],
    "url": f"https://discord.com/channels/{GUILD}/{FEEDBACK_CH}/{m['id']}",
    "reactions": sum(r["count"] for r in m.get("reactions", [])),
    "replies": m.get("thread", {}).get("message_count", 0),
} for m in msgs if "[bot]" not in m["content"]]
```

Same shape for Slack via `slack-mcp.conversations_history` and Discourse via `cli-anything` curl `/c/feedback.json`.

### Recipe 3: Cluster via embeddings

```python
# Use Voyage AI or OpenAI embeddings
import voyageai, numpy as np
vc = voyageai.Client()

embeddings = vc.embed([p["text"] for p in posts], model="voyage-3").embeddings
embeddings = np.array(embeddings)

# DBSCAN clustering
from sklearn.cluster import DBSCAN
clusters = DBSCAN(eps=0.35, min_samples=2, metric="cosine").fit(embeddings)
labels = clusters.labels_

# Group posts
from collections import defaultdict
clustered = defaultdict(list)
for p, lbl in zip(posts, labels):
    clustered[int(lbl)].append(p)

# Sort by demand score: replies + reactions + unique authors
def demand_score(group):
    return sum(p["reactions"] + p["replies"] for p in group) + len({p["author_id"] for p in group})

top_clusters = sorted(
    [g for lbl, g in clustered.items() if lbl != -1],
    key=demand_score,
    reverse=True,
)[:10]
```

### Recipe 4: Cluster → summary via Claude

```python
import anthropic, json
client = anthropic.Anthropic()

def summarize_cluster(posts: list[dict]) -> dict:
    excerpts = "\n---\n".join([f"<@{p['author_name']}>: {p['text']}" for p in posts[:20]])
    resp = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=400,
        system="""You synthesize community feedback clusters into product-ticket-ready briefs.

Output JSON only:
{
  "title": "10-word feature title",
  "summary": "2-3 sentence description",
  "user_problem": "what pain point this addresses",
  "ask_count": "number of distinct asks",
  "tier": "P0|P1|P2",
  "category": "feature|bug|UX|pricing|integration|docs",
  "tags": ["..."]
}""",
        messages=[{"role": "user", "content": excerpts}],
    )
    return json.loads(resp.content[0].text)
```

### Recipe 5: Push to Productboard

```python
for cluster in top_clusters:
    summary = summarize_cluster(cluster)
    member_urls = [p["url"] for p in cluster]

    requests.post(
        "https://api.productboard.com/notes",
        headers={
            "Authorization": f"Bearer {PRODUCTBOARD_TOKEN}",
            "X-Version": "1",
        },
        json={
            "title": summary["title"],
            "content": (
                f"{summary['summary']}\n\n"
                f"**User problem:** {summary['user_problem']}\n"
                f"**Source:** Community ({len(cluster)} posts, "
                f"{len({p['author_id'] for p in cluster})} distinct authors)\n\n"
                f"**Threads:**\n" + "\n".join(member_urls)
            ),
            "tags": ["community-source"] + summary["tags"],
            "source": {"origin": "community", "record_id": cluster[0]["id"]},
            "company": {"domain": "community.brand.com"},
            "user": {"email": "community-bot@brand.com"},
        },
    )
```

### Recipe 6: Push to Linear (engineering-led)

```bash
# Each cluster becomes a Linear issue
mcp tool linear-mcp.create_issue \
  --team_id "$LINEAR_TEAM" \
  --title "$SUMMARY_TITLE" \
  --description "$SUMMARY_TEXT

Member count: $N_DISTINCT_AUTHORS
Total posts: $N_POSTS
Threads:
$THREAD_LINKS

cluster-id: $CLUSTER_ID" \
  --labels community-source,product-feedback,tier-$TIER \
  --priority $PRIORITY
```

Linear's `community-source` label + custom field `member_count` enables PM prioritization by demand.

### Recipe 7: Push to Canny (public voting)

```bash
# Each cluster as a Canny post (public, votable)
curl -X POST https://canny.io/api/v1/posts/create \
  -H "Content-Type: application/json" \
  -d "{
    \"apiKey\": \"$CANNY_API_KEY\",
    \"authorID\": \"$CANNY_BOT_USER\",
    \"boardID\": \"$CANNY_BOARD_FEEDBACK\",
    \"title\": \"$SUMMARY_TITLE\",
    \"details\": \"From community: $SUMMARY_TEXT\\n\\nThreads: $THREAD_LINKS\",
    \"customFields\": {\"community_source_count\": $N_AUTHORS}
  }"
```

Then community members can publicly upvote, which feeds public-roadmap demand signal.

### Recipe 8: Reverse-sync — Webhook on status change

Linear webhook → community announce:

```python
@app.post("/webhook/linear")
def linear_webhook(payload):
    if payload["action"] == "update" and payload["data"]["state"]["name"] == "Done":
        issue = payload["data"]
        if "community-source" in [l["name"] for l in issue["labels"]]:
            cluster_id = extract_cluster_id(issue["description"])
            thread_urls = extract_thread_urls(issue["description"])

            # Tag original posters
            for url in thread_urls:
                channel_id, message_id = parse_discord_url(url)
                discord_full.create_message(
                    channel_id=channel_id,
                    content=f":white_check_mark: **Shipped!** This feature you asked for is live. "
                            f"See release notes: {issue['url']}\n"
                            f"Thanks <@{get_author(message_id)}> for the suggestion.",
                    message_reference={"message_id": message_id},
                )

            # Announce in #releases
            discord_full.create_message(
                channel_id=RELEASES_CH,
                content=f":rocket: **{issue['title']}** is live — "
                        f"originally suggested by {len(thread_urls)} community members. {issue['url']}"
            )
```

Productboard / Canny / Featurebase have equivalent webhook events; Linear is leanest.

### Recipe 9: Weekly digest to community

```python
# Friday: post the week's status to community
status = {
    "received_this_week": len(top_clusters),
    "shipped_this_week": linear.issues(label="community-source", state="Done", updated_since="7d ago"),
    "in_progress": linear.issues(label="community-source", state="In Progress"),
    "considering": linear.issues(label="community-source", state="Backlog", priority=">=High"),
}

slack_mcp.chat_postMessage(
    channel="#community-feedback-loop",
    text=f"""*Feedback loop — week of {today}*

:incoming_envelope: {status['received_this_week']} new clusters synthesized from your posts
:rocket: {len(status['shipped_this_week'])} shipped this week:
{newline_join(['• ' + i['title'] + ' ← ' + i['url'] for i in status['shipped_this_week']])}

:hammer_and_wrench: In progress ({len(status['in_progress'])}):
{newline_join(['• ' + i['title'] for i in status['in_progress'][:5]])}

:thinking_face: Considering ({len(status['considering'])}):
{newline_join(['• ' + i['title'] for i in status['considering'][:5]])}

Add feedback in <#feedback> anytime. Roadmap: {ROADMAP_URL}
""",
)
```

### Recipe 10: Notion-mirrored public roadmap

```python
# Mirror Linear → Notion for public-readable roadmap (works when Linear is private)
for issue in linear.issues(label="community-source"):
    notion.pages_update_or_create(
        database_id=ROADMAP_DB_ID,
        external_id=issue["id"],
        properties={
            "Title": {"title": [{"text": {"content": issue["title"]}}]},
            "Status": {"select": {"name": map_linear_to_notion(issue["state"]["name"])}},
            "Description": {"rich_text": [{"text": {"content": issue["description"][:1000]}}]},
            "Demand": {"number": issue.get("member_count", 0)},
            "Last updated": {"date": {"start": issue["updated_at"]}},
        }
    )
```

Share the Notion DB page publicly; embed in community Discourse FAQ or Circle About.

## Examples

### Example 1: Greenfield setup (Discord + Linear)

**Goal:** OSS project, want feedback → Linear → reverse-sync to Discord.

**Steps:**
1. Create `#feedback` Discord channel with description "post asks here; we sync weekly".
2. Pin a message explaining the closed-loop process + emoji legend.
3. Friday cron: sweep (Recipe 2) → cluster (Recipe 3) → summarize (Recipe 4) → push to Linear (Recipe 6) with `community-source` label.
4. Linear webhook deployed → reverse-sync on state change (Recipe 8).
5. Friday digest post (Recipe 9).
6. Notion roadmap mirror (Recipe 10) embedded in `community-roadmap` channel.

**Result:** Community sees "we heard you, here's what's coming". Reply-to-ship median latency: 12 days for P0, 45 days for P1.

### Example 2: B2B SaaS scaling up (Productboard + Canny)

**Goal:** PM-led B2B with 5k community members + 200 enterprise accounts.

**Steps:**
1. Weekly sweep → cluster → push to Productboard via Recipe 5.
2. Productboard "Pulse" widget for sales + CSM to track community demand on accounts.
3. Top-voted Productboard items pushed to Canny for public roadmap visibility.
4. Quarterly customer advisory board reviews top 20 community clusters.
5. Reverse-sync: Productboard "Done" → Slack `#feedback` thread reply tagging original posters.

**Result:** Enterprise sales cycle reference customer asks come through community → tracked → closed loop. NRR for community-active accounts +12% vs baseline.

### Example 3: Audit + close gaps (existing community)

**Goal:** Existing community feedback channel has 1000 posts; nothing has been done. Quarterly audit.

**Steps:**
1. Backfill: cluster all 1000 historical posts (Recipe 3 with looser eps).
2. Score by total reactions × distinct authors.
3. Top 25 clusters → Productboard with priority weighting.
4. Identify shipped-but-not-announced: cross-reference with release notes; backfill reverse-sync (Recipe 8).
5. Post "Feedback audit results" thread acknowledging gaps.
6. Going forward: weekly cadence (Recipe 9).

**Result:** Community trust score (NPS) jumped 18 points after audit + announcement. Top 5 clusters became Q3 roadmap items.

## Edge cases / gotchas

- **Spam / low-quality clusters** — single-post clusters often noise. Require ≥2 distinct authors per cluster to push to portal.
- **Duplicate clusters across weeks** — same ask appears multiple weeks. Match by embedding similarity; merge votes into existing portal item.
- **PII leakage** — community member usernames may include real names. Strip or hash before pushing externally; use community-bot user for portal author.
- **Webhook reliability** — Linear webhooks fail silently. Add weekly reconciliation job to catch missed states.
- **"Won't fix" with no rationale** — kills community trust. Always reverse-sync with at least 1-sentence explanation.
- **Productboard duplicate posts** — Productboard's auto-dedup is overly strict. Use note-source field, not title match.
- **Canny vote inflation** — public Canny boards can be brigaded by single-issue voters. Weight by community-account verification.
- **Linear rate limits** — 1500 req/hr; bulk push of 50+ clusters needs batching.
- **Embedding clustering noise** — DBSCAN's eps is sensitive; tune per dataset. Validate on 10 known asks first.
- **Cross-language clustering fails** — non-English posts cluster separately. Translate via deepl-mcp before clustering.
- **Stale roadmap visibility** — Notion mirror lags Linear. Run hourly, not daily, if PMs ship daily.
- **Sales-driven asks override community-driven** — when CSM/sales push items "from $1M deal", community items get deprioritized. Track ratio of shipped community-source vs sales-source quarterly; rebalance.
- **Bot author confusion** — community bot posting Canny items shows as "Bot" author; alienates voters. Surface original community member name in details field.
- **GDPR right-to-erasure** — member requests deletion → community post deleted → cluster references break. Maintain audit log of cluster-source pointers; allow orphan-cluster mode.
- **Reverse-sync to deleted channels** — community member left, message deleted. Webhook fails silently; log + skip.

## Sources

- [Productboard public API](https://developer.productboard.com/)
- [Productboard community integrations](https://www.productboard.com/integrations/)
- [Canny API docs](https://developers.canny.io/)
- [Featurebase API](https://docs.featurebase.app/api)
- [Linear API docs](https://developers.linear.app/docs)
- [Linear webhooks](https://developers.linear.app/docs/graphql/webhooks)
- [Notion API](https://developers.notion.com/)
- [Voyage AI embeddings](https://docs.voyageai.com/docs/embeddings)
- [Anthropic prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
