<!--
Source: https://buffer.com/developers/api
Buffer MCP: https://buffer.com/resources/best-social-media-apis/
Sprout Social: https://sproutsocial.com/insights/social-media-scheduling-tools/
Agorapulse Inbox Assistant: https://www.agorapulse.com/
-->
# Community Engagement — Comments + DMs at Scale — SKILL

Reply to comments and DMs across LinkedIn, X, IG, TikTok, Threads, Bluesky in one inbox via Buffer MCP `getEngagements` / `respondToEngagement`. Falls through to Sprout Social (enterprise) or Agorapulse Inbox Assistant (SMB) for collision detection and rule-routing when those licenses exist. Hand off complaints to `social-customer-service-handoff` and crises to `social-crisis-comms`.

## When to use this skill

- **Daily inbox sweep** across 4+ connected channels — Buffer's MCP returns a unified engagement queue.
- **SLA-driven triage** — urgent (15 min) / question (4 hr) / praise (24 hr) per role.md SLA matrix.
- **Recurring-pattern surfacing** — 3+ identical complaints in 7 days flag product team via `slack-mcp`.
- **Team coordination** — multi-admin reply queue with collision detection (Sprout / Agorapulse).

**Do NOT use this skill when:**
- A complaint needs resolution beyond acknowledgment — escalate via `social-customer-service-handoff`.
- A negative-mention velocity spike triggers crisis flag — escalate via `social-crisis-comms`.
- Publishing (not engaging) — use the Buffer publishing skill or native platform MCPs.

## Setup

### Buffer MCP install

```bash
npx -y @buffer/mcp-server@latest
export BUFFER_ACCESS_TOKEN="<pat>"
export BUFFER_ORGANIZATION_ID="<org-uuid>"  # team plans only
```

PAT generated at https://publish.buffer.com/account/apps.

### Sprout Social (enterprise) auth

```bash
# Sprout API requires OAuth 2.0 + paid customer ID
export SPROUT_API_KEY="<key>"
export SPROUT_CUSTOMER_ID="<id>"
# Endpoint: https://api.sproutsocial.com/v1/<customer>/messages
```

### Agorapulse Inbox Assistant (SMB)

```bash
export AGORAPULSE_API_KEY="<key>"
# Endpoint: https://api.agorapulse.com/api/v2/conversations
```

### Channel mapping

Run once to map channel IDs:

```bash
mcp tool buffer.list_channels
# Persist mapping in .buffer-channels.json (see buffer-cross-platform-publishing skill)
```

### Triage Notion DB

Required columns: `engagement_id / channel / author_handle / type (urgent/question/praise/complaint/spam/DM/tag) / sentiment / received_at / sla_due / status (open/replied/escalated/closed) / assignee / reply_text`.

## Common recipes

### Recipe 1: Daily 9am sweep — pull yesterday's engagements

```bash
# Pull comments + DMs + mentions per channel since last run
mcp tool buffer.get_engagements \
  --channels '["linkedin_company","twitter","instagram","tiktok","threads","bluesky"]' \
  --since "$(date -u -d 'yesterday 9:00' +%Y-%m-%dT%H:%M:%SZ)" \
  --types '["comment","dm","mention","tag"]'
```

Returns array: `{id, channelId, type, authorHandle, text, mediaUrl, createdAt, sentiment, parentPostId}`.

### Recipe 2: Triage classifier (regex + sentiment)

```python
import re
URGENT_PATTERNS = [
    r'\b(broken|refund|scam|stole|illegal|sue|lawyer|press)\b',
    r'@(?:ceo|founder|head[_\-]of)',
    r'\b(crisis|emergency|down|outage)\b',
]
QUESTION_PATTERNS = [r'\?$', r'^(how|why|when|where|what|can|does|do|is|are)\b']
COMPLAINT_PATTERNS = [r'\b(disappoint|terrible|worst|hate|garbage|trash)\b']
SPAM_PATTERNS = [r'\bclick (here|link)\b', r'bit\.ly/\w+', r'\b(dm me|check bio)\b.*\b(crypto|investment)\b']

def classify(text, sentiment_score):
    t = text.lower()
    if any(re.search(p, t) for p in SPAM_PATTERNS): return 'spam'
    if any(re.search(p, t) for p in URGENT_PATTERNS): return 'urgent'
    if any(re.search(p, t) for p in COMPLAINT_PATTERNS) and sentiment_score < -0.3: return 'complaint'
    if any(re.search(p, t) for p in QUESTION_PATTERNS): return 'question'
    if sentiment_score > 0.3: return 'praise'
    return 'neutral'
```

### Recipe 3: Reply via Buffer MCP

```bash
mcp tool buffer.respond_to_engagement \
  --id "<engagement_id>" \
  --text "@authorhandle Thanks for the heads up — DMing you now to get this fixed."
```

GraphQL equivalent:

```graphql
mutation Respond {
  respondToEngagement(input: {
    id: "eng_abc123"
    text: "Reply text"
  }) {
    id status sentAt
  }
}
```

### Recipe 4: Auto-tag + auto-assign (Agorapulse pattern via cli-anything)

```bash
# Auto-assign "complaint" type to support queue assignee
curl -X PATCH "https://api.agorapulse.com/api/v2/conversations/$ID" \
  -H "Authorization: Bearer $AGORAPULSE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"assignee_id": "user_support_lead", "labels": ["complaint","sla_4h"]}'
```

### Recipe 5: SLA breach watchdog

```python
# Run every 15 min via cli-anything cron
from datetime import datetime, timezone, timedelta
SLA_BY_TYPE = {'urgent': 15, 'question': 240, 'complaint': 60, 'praise': 1440, 'dm': 240}

for eng in notion.query(triage_db, filter={'status':'open'}):
    elapsed_min = (datetime.now(timezone.utc) - eng['received_at']).total_seconds() / 60
    sla = SLA_BY_TYPE.get(eng['type'], 240)
    if elapsed_min > sla * 0.8:  # 80% of SLA = warn
        slack.post_message('#social-sla', f"SLA risk: {eng['id']} ({eng['type']}) — {int(elapsed_min)} min elapsed")
```

### Recipe 6: Pin top comment via native MCP fallback

Buffer doesn't expose comment-pin. Falls to native MCPs:

```bash
# Instagram pin via insta-business-mcp
mcp tool insta_business.pin_comment --media_id "<media>" --comment_id "<comment>"

# TikTok pin via tiktok-mcp
mcp tool tiktok.pin_comment --video_id "<video>" --comment_id "<comment>"
```

### Recipe 7: Hide / delete spam

```bash
mcp tool buffer.respond_to_engagement --id "<id>" --action hide
# Or native:
mcp tool insta_business.hide_comment --comment_id "<id>"
mcp tool twitter.hide_reply --tweet_id "<id>"
```

### Recipe 8: Recurring-pattern detection (weekly)

```python
# Group by topic + author last 7 days
from collections import Counter
all_engs = notion.query(triage_db, filter={'received_at__gte': now - 7d})
complaint_topics = Counter(e['extracted_topic'] for e in all_engs if e['type']=='complaint')
for topic, n in complaint_topics.most_common(5):
    if n >= 3:
        slack.post_message('#product-feedback',
            f"Recurring complaint: '{topic}' — {n} reports in 7 days. Triage in Notion: <link>")
```

## Examples

### Example A: Daily morning queue → Notion → Slack digest

```yaml
# .github/workflows/social-inbox.yml (or local cron)
schedule:
  - cron: '0 9 * * *'  # 9am daily

jobs:
  sweep:
    steps:
      - pull engagements (Recipe 1)
      - classify (Recipe 2)
      - upsert into Notion triage DB
      - post Slack digest: "Inbox: 23 new (3 urgent / 8 questions / 9 praise / 3 complaints)"
```

### Example B: Mid-day SLA-breach Slack ping

```python
# 12pm + 4pm cron
breaches = [e for e in open_engs() if elapsed(e) > SLA_BY_TYPE[e['type']]]
if breaches:
    slack.post_message('#social-sla',
        f"⚠ {len(breaches)} SLA breaches: " + ", ".join(f"{e['id']} ({e['type']})" for e in breaches[:5]))
```

### Example C: Reply quality template

For praise:

> @{handle} Means a lot — thank you. The {specific-thing-they-mentioned} was something the team really sweated over.

For question:

> @{handle} Great q. {direct-answer-1-line}. More detail here: {link}. DM if you want to dig in.

For complaint:

> @{handle} Sorry that happened — DMing you now to make this right. Could you share your order # / account email?

## Edge cases

### Buffer rate limits
60 req/min per token. For bulk replies use `respondToEngagementBatch` (max 50 per call). Backoff on 429.

### Native-only engagement types
- **Instagram Story replies / mentions** — Buffer surfaces Story mentions but not Story replies; use `insta-business-mcp`.
- **TikTok DMs** — TikTok DMs are still beta in Buffer (June 2026); fall to `tiktok-mcp`.
- **Threads quote-posts** — surface in Buffer mentions feed, but reply must go via Threads-native UI / `threads-mcp` if available.

### Author identity collision
Same handle across platforms is rarely same human. Don't merge across channels unless you've matched them (e.g., linked profile bio).

### Bot replies
Generic "Thanks!" replies are flagged by IG / X spam-classifier. Minimum 2-line substantive reply or genuine 1-line referencing what they said.

### Sentiment-classifier failure on sarcasm
Brand24 2026 sentiment model handles sarcasm; baseline VADER does not. If using local classifier, flag any high-engagement reply with low sentiment confidence for manual review.

### Sprout / Agorapulse collision detection
If two team members start drafting a reply, the tool surfaces a lock. Without those tools, use Notion `assignee` column + a "claim" step.

### Hidden / shadowbanned replies
Algorithms shadowban brand replies that look spammy (linkified, repetitive emoji rows). Vary opening word; don't paste identical replies.

### Multi-language inbox
Spanish / Portuguese / Mandarin DMs to global brands: route by language via `deepl-mcp` detection → assign per-language responder.

### DM consent + privacy
Don't paste DM content publicly. Don't screenshot DMs without consent. GDPR / CCPA apply to DM logs in EU / California — review retention.

### Closed accounts
If author has gone private or deleted, Buffer returns `engagement.author = null`. Mark closed in triage DB; don't reply (would post into the void).

### Quote-reply tactics
On X, quote-replying high-traction posts gets your brand in the thread context — algorithmic boost. Reserve for genuinely-additive replies; spammy quote-replies hurt.

## Sources

- **Buffer Developers (API + MCP)**: https://buffer.com/developers/api
- **Buffer — Best social media APIs 2026**: https://buffer.com/resources/best-social-media-apis/
- **Sprout Social — Scheduling tools 2026**: https://sproutsocial.com/insights/social-media-scheduling-tools/
- **Agorapulse Inbox Assistant**: https://www.agorapulse.com/inbox-assistant/
- **Instagram Graph API (comments + replies)**: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/comment
