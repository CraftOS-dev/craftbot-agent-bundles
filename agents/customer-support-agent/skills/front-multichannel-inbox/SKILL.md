<!--
Source: https://dev.frontapp.com/reference/introduction
Front Smart Summarize + Task conversations: https://community.front.com/api-news-updates-40
-->
# Front Multichannel Inbox — SKILL

Front is the SOTA shared-inbox platform that unifies email + chat + SMS + WhatsApp + Twitter / X DMs + Front Chat into one collaborative inbox with rules, templates, and Smart Summarize. Use this skill any time the recipient runs on Front and the agent needs to read, route, summarize, reply, or template inside Front.

## When to use

- **Recipient operates on Front** (most common for shared-inbox shops, 5-200 agents).
- **Unified multichannel triage** — Front already normalizes channels; the agent just routes on the unified `conversation` object.
- **Templates (Front's macro equivalent)** — author, version, push canned replies.
- **Smart Summarize for handoffs** — auto-summary on long threads.
- **Inbox rules + assign workflows** — codify routing as Front Rules.
- **Task conversations** (2026) — convert a thread into a tracked task with description field.

Trigger phrases: "triage Front conversations", "summarize this Front thread", "create a Front template", "assign Front conversation", "Front routing rule".

## Setup

```bash
# Front exposes a REST API at api2.frontapp.com (Core API). No vendor MCP yet (2026-06).
# Use cli-anything + curl or one of the community MCPs (e.g., @frontapp/community-mcp).
curl -sS https://api2.frontapp.com/me \
  -H "Authorization: Bearer $FRONT_TOKEN" \
  -H "Accept: application/json" | jq .
```

Auth + env:
- `FRONT_TOKEN` — API token at `Settings > Developers > API Tokens`. Tokens carry the scope of the user who created them; create a dedicated "automation" user with admin role for cross-inbox access.
- Webhook signing secret (`FRONT_WEBHOOK_SECRET`) if you wire `conversation.created` to Front's webhook delivery.

Workspace prerequisites:
- One or more inboxes connected (email, chat, channel APIs).
- Tags created up-front at `Settings > Tags` — programmatic tag-create requires admin scope and is rate-limited.

## Common recipes

### Recipe 1: List open conversations needing assignment

```bash
curl -sS "https://api2.frontapp.com/conversations?q[statuses][]=open&q[statuses][]=unassigned" \
  -H "Authorization: Bearer $FRONT_TOKEN" | jq '._results[] | {id, subject, status, created_at, recipient: .recipient.handle}'
```

Front uses `_results` (note the underscore) for the items array and `_pagination.next` for paging. Track `next` cursor token.

### Recipe 2: Read full conversation (including messages)

```bash
# Conversation metadata
curl -sS "https://api2.frontapp.com/conversations/$CONV_ID" \
  -H "Authorization: Bearer $FRONT_TOKEN" | jq .

# Conversation messages
curl -sS "https://api2.frontapp.com/conversations/$CONV_ID/messages" \
  -H "Authorization: Bearer $FRONT_TOKEN" | jq '._results[] | {id, type, body, created_at, author: .author.username}'

# Conversation comments (internal-only)
curl -sS "https://api2.frontapp.com/conversations/$CONV_ID/comments" \
  -H "Authorization: Bearer $FRONT_TOKEN" | jq '._results[]'
```

Three endpoints — separated because Front distinguishes customer-visible messages from agent-only comments.

### Recipe 3: Assign conversation to a teammate or team

```bash
curl -sS -X PATCH "https://api2.frontapp.com/conversations/$CONV_ID/assignee" \
  -H "Authorization: Bearer $FRONT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"assignee_id":"$TEAMMATE_ID"}'
```

To unassign, pass `{"assignee_id": null}`. For team assignment via inbox routing, use Rules (Recipe 9) instead.

### Recipe 4: Reply to the customer

```bash
curl -sS -X POST "https://api2.frontapp.com/conversations/$CONV_ID/messages" \
  -H "Authorization: Bearer $FRONT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "body":"<p>Here is the workaround...</p>",
    "text":"Here is the workaround...",
    "channel_id":"$EMAIL_CHANNEL_ID",
    "options":{"archive":false,"tags":["macro-applied","topic-billing"]}
  }'
```

`channel_id` is the outbound channel (email / chat / etc.). The same conversation can have multiple inbound channels but a reply must be on one outbound channel.

### Recipe 5: Post internal comment

```bash
curl -sS -X POST "https://api2.frontapp.com/conversations/$CONV_ID/comments" \
  -H "Authorization: Bearer $FRONT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"body":"@billing-team — customer is Enterprise tier, $200k ARR, frustrated.","author_id":"$AUTHOR_ID"}'
```

`@mention` syntax pings teammates in their Front inbox. Internal comments do NOT ship to customer.

### Recipe 6: Apply tag(s)

```bash
curl -sS -X POST "https://api2.frontapp.com/conversations/$CONV_ID/tags" \
  -H "Authorization: Bearer $FRONT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tag_ids":["tag_topic_billing","tag_tier_enterprise","tag_sentiment_frustrated"]}'
```

Tags here use IDs. Cache the name→id mapping from `GET /tags`.

### Recipe 7: Use Smart Summarize on a long thread

Smart Summarize is a Front AI feature surfaced in the UI; the API exposes it via:

```bash
curl -sS "https://api2.frontapp.com/conversations/$CONV_ID/ai/summary" \
  -H "Authorization: Bearer $FRONT_TOKEN" | jq '.summary, .key_topics, .customer_mood'
```

Returns a 2-3 sentence summary plus extracted topics. Use on handoffs to engineering or CSM. (Front AI add-on required for this endpoint.)

### Recipe 8: Create a template (Front's macro equivalent)

```bash
curl -sS -X POST "https://api2.frontapp.com/templates" \
  -H "Authorization: Bearer $FRONT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"[topic-billing] Plan downgrade walkthrough",
    "subject":"Re: Downgrading your plan",
    "body":"<p>Hi {{first_name}},</p><p>Here are the exact steps...</p>",
    "inbox_id":"$BILLING_INBOX_ID"
  }'
```

`inbox_id` scopes the template to one inbox (recommended). Use `{{first_name}}` / `{{last_name}}` mustache for personalization — Front resolves at send time.

### Recipe 9: Create a routing rule

Front Rules are admin-only and authored via the Settings UI. To list rules via API:

```bash
curl -sS "https://api2.frontapp.com/inboxes/$INBOX_ID/rules" \
  -H "Authorization: Bearer $FRONT_TOKEN" | jq '._results[]'
```

For programmatic rule creation, use the Rules API beta (request access via Front support).

### Recipe 10: Create a Task conversation (2026 feature)

```bash
curl -sS -X POST "https://api2.frontapp.com/conversations" \
  -H "Authorization: Bearer $FRONT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type":"task",
    "subject":"Follow up — refund disputed by customer",
    "description":"Customer disputes the refund timing. Need to confirm with finance by EOD Friday.",
    "inbox_id":"$BILLING_INBOX_ID",
    "assignee_id":"$AGENT_ID",
    "tags":["task-followup","topic-billing"]
  }'
```

`type: "task"` distinguishes from `email` / `chat`. Tasks carry a dedicated `description` field for context — use for action items born inside a thread.

### Recipe 11: Archive / reopen conversations

```bash
# Archive
curl -sS -X PATCH "https://api2.frontapp.com/conversations/$CONV_ID" \
  -H "Authorization: Bearer $FRONT_TOKEN" \
  -d '{"status":"archived"}'

# Reopen
curl -sS -X PATCH "https://api2.frontapp.com/conversations/$CONV_ID" \
  -H "Authorization: Bearer $FRONT_TOKEN" \
  -d '{"status":"open"}'

# Delete (permanent, 2026 feature)
curl -sS -X DELETE "https://api2.frontapp.com/conversations/$CONV_ID" \
  -H "Authorization: Bearer $FRONT_TOKEN"
```

`status: archived` is recoverable; `DELETE` is permanent (audit log retained).

### Recipe 12: Webhook on `conversation.created`

```bash
curl -sS -X POST "https://api2.frontapp.com/applications/$APP_ID/webhooks" \
  -H "Authorization: Bearer $FRONT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url":"https://your-agent.example.com/webhooks/front",
    "events":["conversation.created","comment.created","conversation.tagged"]
  }'
```

Verify webhook signature using `FRONT_WEBHOOK_SECRET` and the `X-Front-Signature` header (HMAC-SHA1).

## Examples

### Example 1: Morning triage of overnight Front inbox

**Goal:** Triage every overnight conversation: classify, tag, route, summarize.

**Steps:**
1. List open + unassigned: `GET /conversations?q[statuses][]=open&q[statuses][]=unassigned`.
2. For each conv: fetch messages, classify topic/urgency/sentiment via Claude, post internal comment with classification.
3. Add tags (`POST /conversations/$id/tags`).
4. Assign teammate or team (`PATCH /conversations/$id/assignee`).
5. If thread >5 messages, call `/ai/summary` and pin summary as a comment.

**Result:** Every conv triaged before standup; agents start the day with prioritized queues.

### Example 2: Productize a template from a winning ticket

**Goal:** A teammate wrote a great reply; turn it into a reusable template.

**Steps:**
1. Read source message: `GET /conversations/$id/messages` and copy the body.
2. Generalize: replace customer-specific details with `{{first_name}}` etc.
3. Vale lint against `styles/Brand/Voice.yml`.
4. `POST /templates` with the cleaned body.
5. Notion DB entry pointing to template id for cross-platform parity.

**Result:** New template live in Front; sister-platform versions (Zendesk macro, Intercom article) can be auto-derived.

## Edge cases / gotchas

- **`_results` not `results`** — Front prefixes all list-response keys with underscore. Easy bug if you copy a Stripe / GitHub paging pattern.
- **Rate limits** — Core API: 50 req/sec per token globally; 600 req/min for write ops. Honor `X-Rate-Limit-Remaining` header.
- **Inbox vs Channel vs Team** — common confusion. Inbox = collection. Channel = the connection to email / chat / etc. Team = group of teammates. Templates scope to inboxes; assignments scope to teammates; rules scope to inboxes.
- **Tag IDs are not human-readable** — `tag_abc123` style. Always cache name→id and validate before publishing rules that depend on tags.
- **Smart Summarize requires Front AI add-on** — without it, `/ai/summary` returns 402. Fallback: send transcript to Claude with the summary template.
- **Task conversations are 2026-only** — older Front installs (pre-April 2026) don't support `type: "task"`. Check workspace version at `GET /me` → `account.features`.
- **Deleting a conversation is permanent and audited** — never call DELETE without explicit user approval. Use archive instead.
- **Custom fields are per-inbox** — define on the inbox at `Settings > Inbox > Custom Fields`. The API requires the field's UUID, not its label.
- **Outbound channel_id required for replies** — easy 422 if you omit it on a multi-channel conv.
- **Webhook signature uses HMAC-SHA1, not SHA256** — common foot-gun. Use SHA1 base64 of body with `FRONT_WEBHOOK_SECRET`.

## Sources

- [Front Core API introduction](https://dev.frontapp.com/reference/introduction)
- [Front Conversations endpoint](https://dev.frontapp.com/reference/conversations)
- [Front Messages endpoint](https://dev.frontapp.com/reference/messages)
- [Front API news & updates (community)](https://community.front.com/api-news-updates-40)
- [Front overview + use cases](https://help.front.com/en/articles/2482)
- [Front 2026 review + alternatives (eesel)](https://www.eesel.ai/blog/front-review)
