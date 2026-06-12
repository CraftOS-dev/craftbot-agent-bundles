<!--
Source: https://developer.helpscout.com/mailbox-api/
HelpScout Mailbox API 2.0 reference (2026).
-->
# HelpScout MCP — SKILL

HelpScout (Mailbox API 2.0) is the canonical small-team email + chat platform. Use this skill when the recipient runs HelpScout: list / read / update conversations, manage Saved Replies (HelpScout's macro equivalent), create threads, apply tags + workflows.

## When to use

- **Recipient operates on HelpScout** — common for 1-50 agent teams, customer-support shops that started small.
- **Conversation lifecycle** — read, reply, snooze, close.
- **Saved Replies** (macros) — list / create / update; tied to a Mailbox, not workspace.
- **Threading** — append customer / agent / note threads.
- **Tag-driven routing** — apply tags from triage; configure HelpScout Workflows.
- **Reports** — pull happiness ratings, conversation volumes.

Trigger phrases: "HelpScout ticket triage", "create a saved reply", "HelpScout workflow", "reply to HelpScout conversation".

## Setup

```bash
# HelpScout uses OAuth2 client_credentials for server apps.
# Exchange app_id/secret for a 2h access token:
curl -sS -X POST https://api.helpscout.net/v2/oauth2/token \
  -d grant_type=client_credentials \
  -d client_id=$HELPSCOUT_APP_ID \
  -d client_secret=$HELPSCOUT_APP_SECRET | jq -r '.access_token'
```

Auth + env:
- `HELPSCOUT_APP_ID` and `HELPSCOUT_APP_SECRET` — create at `Your Profile > My Apps > Create My App`.
- `HELPSCOUT_TOKEN` — short-lived (2h) access token from the call above; cache & refresh.
- All requests need `Authorization: Bearer $HELPSCOUT_TOKEN`.

Workspace prerequisites:
- Mailbox(es) configured (`Manage > Mailboxes`); each has its own saved-reply library.
- Tags pre-created if you want stable IDs (auto-create works but pollutes namespace).

## Common recipes

### Recipe 1: List open conversations needing assignment

```bash
curl -sS "https://api.helpscout.net/v2/conversations?status=active&assigned=false&mailbox=$MAILBOX_ID" \
  -H "Authorization: Bearer $HELPSCOUT_TOKEN" \
  -H "Accept: application/json" | jq '._embedded.conversations[] | {id, subject, status, createdAt, customer: .primaryCustomer.email}'
```

HelpScout uses HAL: collection lives under `_embedded.conversations`; paging via `_links.next.href`.

### Recipe 2: Get one conversation with full thread history

```bash
curl -sS "https://api.helpscout.net/v2/conversations/$CONV_ID?embed=threads" \
  -H "Authorization: Bearer $HELPSCOUT_TOKEN" | jq '.'
```

`embed=threads` pulls all threads inline (customer messages, agent replies, internal notes, status changes).

### Recipe 3: Update conversation (assign, change status, change mailbox)

```bash
# Reassign
curl -sS -X PATCH "https://api.helpscout.net/v2/conversations/$CONV_ID" \
  -H "Authorization: Bearer $HELPSCOUT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"op":"replace","path":"/assignTo","value":$USER_ID}'

# Change status (active|pending|closed|spam)
curl -sS -X PATCH "https://api.helpscout.net/v2/conversations/$CONV_ID" \
  -H "Authorization: Bearer $HELPSCOUT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"op":"replace","path":"/status","value":"pending"}'

# Move mailbox
curl -sS -X PATCH "https://api.helpscout.net/v2/conversations/$CONV_ID" \
  -H "Authorization: Bearer $HELPSCOUT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"op":"replace","path":"/mailboxId","value":$NEW_MAILBOX_ID}'
```

HelpScout uses JSON Patch syntax for updates. One operation per call.

### Recipe 4: Reply to customer (creates a customer-thread)

```bash
curl -sS -X POST "https://api.helpscout.net/v2/conversations/$CONV_ID/reply" \
  -H "Authorization: Bearer $HELPSCOUT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text":"Here is the workaround steps...",
    "user":'$USER_ID',
    "customer":{"email":"user@example.com"}
  }'
```

`user` is the agent sending the reply. `customer` identifies the recipient.

### Recipe 5: Add an internal note

```bash
curl -sS -X POST "https://api.helpscout.net/v2/conversations/$CONV_ID/notes" \
  -H "Authorization: Bearer $HELPSCOUT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"Customer is Enterprise tier, $120k ARR. Frustrated about billing migration.","user":'$USER_ID'}'
```

Notes never reach the customer; ideal for triage evidence chain.

### Recipe 6: Apply tags

```bash
curl -sS -X PUT "https://api.helpscout.net/v2/conversations/$CONV_ID/tags" \
  -H "Authorization: Bearer $HELPSCOUT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tags":["topic-billing","tier-enterprise","sentiment-frustrated","triage-done"]}'
```

Tags here use names (HelpScout creates IDs server-side). PUT *replaces* the tag set — use Get + merge if additive.

### Recipe 7: List saved replies for a mailbox

```bash
curl -sS "https://api.helpscout.net/v2/mailboxes/$MAILBOX_ID/saved-replies" \
  -H "Authorization: Bearer $HELPSCOUT_TOKEN" | jq '._embedded["saved-replies"][] | {id, name, category}'
```

Saved replies are mailbox-scoped, not workspace-wide.

### Recipe 8: Create a saved reply

```bash
curl -sS -X POST "https://api.helpscout.net/v2/mailboxes/$MAILBOX_ID/saved-replies" \
  -H "Authorization: Bearer $HELPSCOUT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"[topic-billing] Plan downgrade walkthrough",
    "subject":"Re: Plan downgrade",
    "text":"Hi %customer.firstName%,\n\nHere are the exact steps to downgrade...",
    "category":"Billing"
  }'
```

Variables use `%customer.firstName%` syntax (NOT mustache). Test render before pushing.

### Recipe 9: Update a saved reply

```bash
curl -sS -X PUT "https://api.helpscout.net/v2/mailboxes/$MAILBOX_ID/saved-replies/$REPLY_ID" \
  -H "Authorization: Bearer $HELPSCOUT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"[topic-billing] Plan downgrade walkthrough",
    "text":"Updated text..."
  }'
```

Full PUT — required fields must all be present.

### Recipe 10: Create a brand-new conversation (e.g., from a webhook)

```bash
curl -sS -X POST "https://api.helpscout.net/v2/conversations" \
  -H "Authorization: Bearer $HELPSCOUT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "subject":"Critical error in checkout flow",
    "customer":{"email":"user@example.com"},
    "mailboxId":'$MAILBOX_ID',
    "type":"email",
    "status":"active",
    "threads":[{
      "type":"customer",
      "customer":{"email":"user@example.com"},
      "text":"Original error report from product webhook..."
    }],
    "tags":["auto-created","error-critical"]
  }'
```

Used for product-event-driven ticket creation.

### Recipe 11: Snooze a conversation

```bash
curl -sS -X PATCH "https://api.helpscout.net/v2/conversations/$CONV_ID" \
  -H "Authorization: Bearer $HELPSCOUT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"op":"replace","path":"/snoozeUntil","value":"2026-06-15T09:00:00Z"}'
```

Snooze surfaces the conversation back to the queue at `snoozeUntil`.

### Recipe 12: Pull weekly happiness report

```bash
curl -sS "https://api.helpscout.net/v2/reports/happiness?start=2026-06-01T00:00:00Z&end=2026-06-08T00:00:00Z&mailboxes=$MAILBOX_ID" \
  -H "Authorization: Bearer $HELPSCOUT_TOKEN" | jq '.companyOverall'
```

HelpScout's built-in CSAT-style rating (Great / Okay / Not Good). Feed into weekly digest.

## Examples

### Example 1: Triage + saved-reply mining loop

**Goal:** Triage today's unworked conversations and identify 1-2 saved-reply candidates.

**Steps:**
1. List unassigned active conversations.
2. For each: pull threads (Recipe 2), classify topic/urgency/sentiment via Claude.
3. Tag (Recipe 6), assign (Recipe 3), drop internal note with classification (Recipe 5).
4. At end of week: export conversations of last 30 days, embed bodies, cluster. Top clusters without a saved reply → propose new saved replies in Notion review doc.

**Result:** Cleaner queue; library grows from real ticket patterns.

### Example 2: Auto-resolve "where do I download my invoice" cluster

**Goal:** A common ticket cluster has a single answer. Auto-reply + close.

**Steps:**
1. Workflow set in HelpScout UI: tag `topic-invoice-download` triggers apply-saved-reply.
2. Agent skill detects the cluster via classification, applies tag (Recipe 6).
3. HelpScout workflow auto-applies the saved reply with the invoice-download steps.
4. Agent verifies on the conversation (Recipe 2) and sets status to `pending` (Recipe 3) — wait 7d, auto-close.

**Result:** 30+ tickets/week auto-resolved without agent involvement.

## Edge cases / gotchas

- **OAuth access tokens last 2 hours** — cache aggressively or you'll burn rate limits doing token exchanges. Refresh ~ten minutes before expiry.
- **Rate limits** — 200 req / minute per account by default. Burst protection on writes (60 req / 10s). Honor `X-RateLimit-Remaining`.
- **JSON Patch only on conversation PATCH** — not standard JSON. `{ "op": "replace", "path": "/...", "value": "..." }`. Easy to get wrong.
- **Saved replies are mailbox-scoped** — moving a conversation to a new mailbox means saved replies from the old mailbox don't apply. Maintain cross-mailbox parity via Notion source of truth.
- **Variables use `%customer.firstName%` syntax** — NOT mustache, NOT Liquid. Different from Plain / Front / Intercom.
- **Tags PUT replaces** — to add a tag, GET existing tags first then PUT the merged list. Or use a Workflow to apply tag conditionally.
- **Customer matching** — replies require either an `email` or a HelpScout `customerId`. Email auto-creates a customer if not found; can cause duplicates if email casing varies. Normalize lowercase before sending.
- **HelpScout AI Assist** — paid 2026 add-on that auto-summarizes and drafts replies. Not exposed via REST API; UI-only feature for now.
- **HAL `_embedded` and `_links`** — many integrations break expecting plain `data` / `pagination`. Use HAL-aware libs or jq carefully.
- **No GraphQL** — only REST. SDK officially in PHP + Ruby; community Python/JS libs exist.

## Sources

- [HelpScout Mailbox API 2.0](https://developer.helpscout.com/mailbox-api/)
- [List Saved Replies](https://developer.helpscout.com/mailbox-api/endpoints/inboxes/saved_Replies/saved-replies-list/)
- [Get Conversation](https://developer.helpscout.com/mailbox-api/endpoints/conversations/get/)
- [Update Conversation (JSON Patch)](https://developer.helpscout.com/mailbox-api/endpoints/conversations/update/)
- [Create Reply Thread](https://developer.helpscout.com/mailbox-api/endpoints/conversations/threads/reply/)
- [Email Report endpoint](https://developer.helpscout.com/mailbox-api/endpoints/reports/email/)
