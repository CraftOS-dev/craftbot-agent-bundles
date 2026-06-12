<!--
Source: https://discord.com/developers/docs + https://api.slack.com + https://www.reddit.com/dev/api
-->
# Slack / Discord Community Support — SKILL

Discord server #support + Slack internal triage + Reddit subreddit monitoring + Discourse forum scrape. Daily / hourly cron polling. Patterns for inline reply, opening private DMs / tickets for confidential issues, VIP role tagging, and crisis-comment detection.

## When to use

- **Recipient runs a Discord community server** with #support / #bugs / #help channels.
- **Recipient has a subreddit** (own or competitor) with regular volume.
- **Slack internal triage** — `#cse-on-call` notifications, on-call ping, customer-Slack-Connect.
- **External forums (Discourse / private community platforms)** — Firecrawl-based polling.
- **Crisis comment detection** — viral-negative thread requires escalation within 1h.

Trigger phrases: "monitor our Discord", "subreddit check", "Slack internal triage", "community support", "Reddit mentions".

## Setup

```bash
# Discord MCPs (already in agent.yaml)
mcp tool discord.list_messages --channel_id $CHANNEL_ID --limit 50

# Slack MCP (already in agent.yaml)
mcp tool slack.conversations_list

# Reddit MCP (already in agent.yaml)
mcp tool reddit.search_subreddit --subreddit yourproduct

# Firecrawl MCP (already in agent.yaml)
mcp tool firecrawl.scrape --url https://community.brand.com
```

Auth + env:
- `DISCORD_BOT_TOKEN` — at https://discord.com/developers/applications > Bot > Token. Bot must be added to the server with `Read Messages`, `Send Messages`, `Manage Threads` scopes.
- `SLACK_BOT_TOKEN` — at https://api.slack.com/apps > OAuth & Permissions. Scopes: `channels:read`, `chat:write`, `groups:read`, `im:write`.
- `REDDIT_CLIENT_ID` + `REDDIT_CLIENT_SECRET` — at https://www.reddit.com/prefs/apps. Script-type app for read-only.
- `FIRECRAWL_API_KEY` — at https://firecrawl.dev. Paid for high-volume scrape.

Workspace prerequisites:
- Discord channels: `#support`, `#bugs`, `#help-and-questions`, `#announcements`. Bug-triage role created.
- Slack channels: `#cse-on-call`, `#cse-enterprise`, `#sla-breach`.
- Reddit subreddit monitored (own + 1-2 competitor).

## Common recipes

### Recipe 1: Poll Discord support channel for unanswered questions

```bash
mcp tool discord.list_messages \
  --channel_id $SUPPORT_CHANNEL_ID \
  --limit 50 \
  --after $LAST_SEEN_TIMESTAMP
```

Filter messages where `reactions[]` is empty and no thread exists → likely unanswered. For each, evaluate via Claude: "Is this a question that needs an answer? If yes, draft a response."

### Recipe 2: Reply inline in Discord

```bash
mcp tool discord.send_message \
  --channel_id $SUPPORT_CHANNEL_ID \
  --message_reference $MESSAGE_ID \
  --content "Hey @user — clearing browser cookies usually fixes this. Here are the steps: ..."
```

Use `message_reference` so the reply threads correctly under the original.

### Recipe 3: Open a thread for a confirmed bug

```bash
# Create a thread off the original message
mcp tool discord.create_thread \
  --channel_id $SUPPORT_CHANNEL_ID \
  --message_id $ORIGINAL_MSG_ID \
  --name "Bug: checkout 422" \
  --auto_archive_duration 1440
```

Then post the bug normalization template inside the thread; tag `@bug-triage` role.

### Recipe 4: DM the user to escalate to private ticket

```bash
# Open a DM channel with the user
DM=$(mcp tool discord.create_dm --user_id $USER_ID | jq -r '.id')

# Send DM
mcp tool discord.send_message --channel_id $DM \
  --content "Hi! I'm following up on your post in #support. Can you share your account email so we can pull up your details privately? I'll create a support ticket and we can continue there."
```

Use for cases that may expose PII / account specifics.

### Recipe 5: VIP role detection (CRM-synced)

```bash
# Use Discord roles synced from CRM (via discord-mcp-full or a sync bot)
MEMBER=$(mcp tool discord.get_member --guild_id $GUILD_ID --user_id $USER_ID)
ROLES=$(echo "$MEMBER" | jq -r '.roles[]')

if [[ "$ROLES" == *"enterprise"* ]]; then
  # Escalate immediately
  mcp tool slack.chat_postMessage --channel '#cse-enterprise' \
    --text "Enterprise customer @user posted in Discord #support: <message_url>"
fi
```

### Recipe 6: Search subreddit for product mentions

```bash
mcp tool reddit.search_subreddit \
  --subreddit yourproduct \
  --sort new \
  --time_filter day \
  --limit 50
```

Or for cross-subreddit mentions:

```bash
mcp tool reddit.search_all \
  --query "yourproduct" \
  --sort new \
  --time_filter day \
  --limit 50
```

### Recipe 7: Detect crisis comments (Reddit thread going viral)

```bash
# Threshold: > 100 comments OR > 500 upvotes in <24h with negative title
mcp tool reddit.search_subreddit --subreddit yourproduct --sort hot --limit 25 | \
  jq '.[] | select(.score > 500 and (.created_utc | tonumber) > (now - 86400)) | {title, url, score, num_comments}'
```

For each result, classify sentiment via Claude. Sentiment < 30 + score > 500 → escalate to lead within 1h.

### Recipe 8: Reply to a Reddit comment (use sparingly)

```bash
mcp tool reddit.submit_reply \
  --parent_id "t1_$COMMENT_ID" \
  --text "Hi — that error is a known issue we're fixing. Workaround: <steps>. If you want personalized help, send us a message at <support@brand.com>."
```

Public replies require Trust-and-Safety lens (per `role.md` antipattern catalog). For complex issues, DM to migrate to a private support ticket.

### Recipe 9: Slack internal — notify on-call

```bash
mcp tool slack.chat_postMessage \
  --channel '#cse-on-call' \
  --text "Discord #support has an unanswered question (15min): <message_url>. Customer tier: enterprise."
```

15-minute SLA on Discord enterprise mentions is reasonable; tune per recipient.

### Recipe 10: Slack Connect customer channel polling

```bash
# Slack Connect channels are external to your workspace but accessible if you're added
mcp tool slack.conversations_history \
  --channel $SLACK_CONNECT_CHANNEL_ID \
  --limit 100 \
  --oldest $LAST_SEEN_TS
```

For each message in a Slack Connect channel, treat as a support inbound. Open Intercom / Zendesk ticket if it's a question / bug.

### Recipe 11: Firecrawl Discourse forum scrape

```bash
mcp tool firecrawl.scrape \
  --url "https://forum.brand.com/c/support" \
  --formats markdown \
  --only_main_content true
```

Daily cron; diff against yesterday to find new threads. For each new thread, classify and route.

### Recipe 12: Cross-channel deduplication

```python
# Same customer posting on Discord AND Reddit AND Slack Connect
import hashlib

def fingerprint(text):
    """Normalize + hash the first 200 chars of a post."""
    return hashlib.sha256(text.lower().strip()[:200].encode()).hexdigest()

# Maintain a dedup table
seen = {}  # fingerprint -> (platform, url, first_seen_at)
def is_dup(text, platform, url):
    fp = fingerprint(text)
    if fp in seen:
        return seen[fp]  # tuple of original
    seen[fp] = (platform, url, time.time())
    return None
```

When a duplicate appears across platforms, link them via internal note rather than re-replying.

## Examples

### Example 1: Hourly Discord poll → ticket pipeline

**Goal:** Every hour, Discord #support is checked; unanswered questions become tickets.

**Steps:**
1. Cron every 60min: Recipe 1 (list new messages since last seen).
2. For each: classify via Claude — `question` | `bug` | `feature_request` | `casual`.
3. `bug` → Recipe 3 (create thread + bug normalization).
4. `question` → Recipe 2 (reply inline) if Kapa confidence ≥ 0.7; else open ticket via Recipe 4 (DM-to-ticket).
5. `feature_request` → Productboard / Linear feature-request log.
6. `casual` → ignore.
7. Update `.last_seen_discord_timestamp`.

**Result:** Discord support coverage zero-latency.

### Example 2: Daily Reddit subreddit sweep

**Goal:** Catch viral negative threads early; respond on the polite ones.

**Steps:**
1. Cron daily 09:00: Recipe 6 (search /r/yourproduct, last 24h).
2. For each post: classify sentiment.
3. Posts with sentiment < 30 AND score > 100: Recipe 7 (crisis check); escalate to lead via Slack.
4. Posts with sentiment ≥ 30 AND has answerable question: Recipe 8 (reply with workaround).
5. Posts mentioning competitor name: tag for marketing-agent review.

**Result:** Reddit isn't a black hole; crisis caught within 24h.

## Edge cases / gotchas

- **Discord rate limits** — 50 req / sec global, with sub-limits per endpoint. `send_message` has burst protection; pause 500ms between messages.
- **Bot permissions** — must add the bot to each channel explicitly (or use `Manage Server` to default). New channels won't auto-include it.
- **Slack rate limits** — Tier 3 (`chat.postMessage`): 50 req/min. Tier 1: 1 req/sec. Honor `Retry-After`.
- **Reddit OAuth** — script-type app for read-only; web app for posting (requires user OAuth). Bot replies trigger Reddit's anti-spam if too frequent.
- **Reddit unwritten rules** — communities ban "corporate replies" that feel performative. Read the subreddit's rules; lean on transparency / specific workarounds rather than CSAT-pitch.
- **Discord mention performance** — `@everyone` and `@here` mass-pings are catastrophic. Never use programmatically. Role pings (`@bug-triage`) are fine.
- **Slack Connect message attribution** — internal messages in Connect channels are visible to the external org. Don't post sensitive internal notes there; use threads in your own workspace.
- **Firecrawl daily scrape may break on rerendered SPAs** — Discourse mostly fine; some forums are JavaScript-heavy. Try `--actions [wait,5000]`.
- **Cross-channel customer-identity matching** — Discord username ≠ Reddit username ≠ email. Maintain a manual mapping table for VIPs.
- **Crisis detection false positives** — a high-upvote thread isn't always negative. Always classify sentiment, not just engagement.
- **Reddit subreddit shadow-bans** — if your bot account's replies suddenly disappear, you've been shadow-banned. Use a non-bot account moderated by a human.
- **Don't engage trolls** — antipattern from `role.md`. Detect, log, internal escalate; don't reply.

## Sources

- [Discord Developer Docs](https://discord.com/developers/docs/intro)
- [Discord create message API](https://discord.com/developers/docs/resources/channel#create-message)
- [Slack chat.postMessage](https://api.slack.com/methods/chat.postMessage)
- [Slack conversations.history](https://api.slack.com/methods/conversations.history)
- [Reddit API rules](https://www.reddit.com/dev/api)
- [Firecrawl scrape API](https://docs.firecrawl.dev/api-reference/endpoint/scrape)
