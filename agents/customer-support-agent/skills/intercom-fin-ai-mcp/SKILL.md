<!--
Source: https://developers.intercom.com/docs/references/rest-api/api.intercom.io/
Intercom Fin AI (GA Mar 2026): https://www.intercom.com/help/en/articles/9442290-fin-ai-operator
-->
# Intercom Fin AI MCP — SKILL

Intercom Fin AI Operator (GA March 2026) is the SOTA for AI-first support inboxes: triage, auto-reply, conversation summary, macro management, and Resolution Score gating in one platform. Use this skill any time the recipient runs on Intercom and the agent needs to read, classify, reply to, or escalate a conversation.

## When to use

- **Triage inbound Intercom conversations** — classify topic / urgency / sentiment in one API pass and apply assignment rules.
- **Auto-draft / auto-send replies** through Fin's Resolution Score gating (default threshold 0.7; below threshold escalates to human).
- **Summarize a conversation for handoff** (engineering / CSM / lead) via Fin's built-in summarizer.
- **Manage macros / canned replies** programmatically (export, lint, push, version).
- **Pull deflection + Fin resolution metrics** for weekly support digests.

Trigger phrases: "triage Intercom tickets", "draft Intercom macros", "summarize this Intercom conversation", "Fin auto-reply", "Fin resolution score".

## Setup

```bash
# Intercom MCP server (community / vendor — pick whichever is installed in CraftBot)
npx -y @intercom/mcp-server@latest
# OR call REST directly via cli-anything (always works)
curl -sS https://api.intercom.io/me -H "Authorization: Bearer $INTERCOM_TOKEN" | jq .
```

Auth + env:
- `INTERCOM_TOKEN` — Personal Access Token; create at `Settings > Integrations > Developer Hub > New app > Authentication > Access tokens`. App-scoped tokens are preferred over PATs in production.
- `INTERCOM_API_VERSION` — pin to `2.13` (current as of 2026-06) via header `Intercom-Version: 2.13`.
- Fin must be enabled per workspace (Settings > Operator > Fin AI Agent), with a configured knowledge source.

Workspace prerequisites:
- Knowledge sources connected (Help Center, public URL, uploaded docs). Without these, Fin's Resolution Score will always be low.
- A "Fin escalation team" assigned for below-threshold handoffs.

## Common recipes

### Recipe 1: List open conversations needing triage

```bash
curl -sS https://api.intercom.io/conversations/search \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H "Intercom-Version: 2.13" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "operator": "AND",
      "value": [
        {"field": "state",  "operator": "=", "value": "open"},
        {"field": "ai_agent_participated", "operator": "=", "value": false}
      ]
    },
    "pagination": {"per_page": 50}
  }' | jq '.conversations[] | {id, subject: .source.subject, created: .created_at}'
```

Returns all unworked conversations Fin hasn't touched. Feed each id into the triage pipeline.

### Recipe 2: Read full conversation transcript

```bash
curl -sS https://api.intercom.io/conversations/$CONV_ID \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H "Intercom-Version: 2.13" \
  -H "Content-Type: application/json" \
  -G --data-urlencode "display_as=plaintext" | jq '.'
```

`display_as=plaintext` strips Intercom rich text so Claude / Loris can score sentiment cleanly.

### Recipe 3: Apply assignment rules (route via Intercom's built-in router)

```bash
curl -sS -X POST https://api.intercom.io/conversations/$CONV_ID/run_assignment_rules \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H "Intercom-Version: 2.13"
```

Honors the workspace's rule set (channel / tier / topic → owner). Idempotent — safe to re-run after tagging.

### Recipe 4: Assign to admin or team manually

```bash
curl -sS -X POST https://api.intercom.io/conversations/$CONV_ID/parts \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H "Intercom-Version: 2.13" \
  -H "Content-Type: application/json" \
  -d '{
    "message_type":"assignment",
    "type":"admin",
    "admin_id":"$ADMIN_ID",
    "assignee_id":"$TEAM_ID",
    "body":"Assigning to enterprise billing — customer tier=enterprise, topic=billing."
  }'
```

`assignee_id` can be a team id (route to queue) or admin id (route to specific person).

### Recipe 5: Reply to customer

```bash
curl -sS -X POST https://api.intercom.io/conversations/$CONV_ID/reply \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H "Intercom-Version: 2.13" \
  -H "Content-Type: application/json" \
  -d '{
    "message_type":"comment",
    "type":"admin",
    "admin_id":"$ADMIN_ID",
    "body":"<p>Here is what triggers the error and the workaround...</p>"
  }'
```

`message_type: "note"` posts an internal-only note (preserves evidence chain without customer-facing exposure).

### Recipe 6: Tag for product signal

```bash
curl -sS -X POST https://api.intercom.io/conversations/$CONV_ID/tags \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H "Intercom-Version: 2.13" \
  -H "Content-Type: application/json" \
  -d '{"id":"$TAG_ID","admin_id":"$ADMIN_ID"}'
```

Tag schema (recommended): `topic-<auth|billing|bug|how-to|feature|abuse>`, `urgency-<crit|high|normal|low>`, `sentiment-<frustrated|confused|neutral|satisfied>`, `tier-<enterprise|growth|starter|free>`. Untagged tickets are noise.

### Recipe 7: Generate conversation summary (Fin / built-in)

```bash
# As of v2.13, summaries auto-attach on Fin-touched conversations under .ai_agent.source.summary.
# Read it back:
curl -sS https://api.intercom.io/conversations/$CONV_ID \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H "Intercom-Version: 2.13" | jq '.ai_agent.source.summary, .ai_agent.resolution_state, .ai_agent.last_answer_type'
```

For non-Fin conversations, feed the transcript to Claude with the structured-summary template from `role.md`.

### Recipe 8: Create a macro (canned reply)

```bash
# REST API — Macros are managed via the Help Center / Inbox UI as of 2026-06.
# Programmatic surface uses the Saved Replies endpoint:
curl -sS -X POST https://api.intercom.io/articles \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H "Intercom-Version: 2.13" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Login loop after SSO migration",
    "description":"Macro: walks user through clearing cookies + re-auth.",
    "body":"<p>Clear cookies for app.brand.com, then re-auth via your SSO provider...</p>",
    "author_id":"$ADMIN_ID",
    "state":"published",
    "parent_id":"$COLLECTION_ID",
    "parent_type":"collection"
  }'
```

Note: Fin AI uses Help Center Articles + Knowledge Sources, NOT macros, as its answer corpus. Macros power *Copilot* (the agent-side assistant), not Fin. Update both surfaces when shipping a new canned reply.

### Recipe 9: Configure Fin Resolution Score threshold

Fin's auto-reply gate uses Resolution Score (0-1). Default cutoff 0.7. Adjust per workspace at `Settings > Fin AI Agent > Confidence threshold`. Via API (Operator API, preview):

```bash
curl -sS -X PATCH https://api.intercom.io/ai/operator/settings \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H "Intercom-Version: 2.13" \
  -H "Content-Type: application/json" \
  -d '{"resolution_score_threshold": 0.75}'
```

Raise threshold = fewer auto-replies, higher accuracy. Lower = more deflection, more risk of bad answer.

### Recipe 10: Pull Fin deflection metrics

```bash
curl -sS https://api.intercom.io/ai/reports/deflection \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H "Intercom-Version: 2.13" \
  -G --data-urlencode "starting_after=2026-05-09" \
       --data-urlencode "ending_before=2026-06-09" | jq '.metrics'
```

Returns `total_conversations`, `fin_resolved`, `human_escalated`, `resolution_rate`, `csat_avg`. Feed into weekly digest.

### Recipe 11: Search for matching past conversations (dedup / cluster)

```bash
curl -sS -X POST https://api.intercom.io/conversations/search \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H "Intercom-Version: 2.13" \
  -H "Content-Type: application/json" \
  -d '{
    "query":{"operator":"AND","value":[
      {"field":"source.body","operator":"~","value":"redis timeout"},
      {"field":"created_at","operator":">","value":1748390400}
    ]}
  }' | jq '.total_count, .conversations[].id'
```

Use this to detect bug clusters before opening a new Linear escalation.

### Recipe 12: Bulk close stale conversations

```bash
for id in $(curl -sS https://api.intercom.io/conversations/search ... | jq -r '.conversations[].id'); do
  curl -sS -X POST https://api.intercom.io/conversations/$id/parts \
    -H "Authorization: Bearer $INTERCOM_TOKEN" \
    -H "Intercom-Version: 2.13" \
    -d '{"message_type":"close","type":"admin","admin_id":"'$ADMIN_ID'","body":"Auto-close: no response in 14 days."}'
done
```

Honor the antipattern rule from `role.md`: include a concrete reopen path in the body.

## Examples

### Example 1: Full triage pass on the morning queue

**Goal:** Triage all unworked overnight conversations and route them.

**Steps:**
1. List open conversations untouched by Fin:
   ```bash
   curl -sS https://api.intercom.io/conversations/search -H "Authorization: Bearer $INTERCOM_TOKEN" -H "Intercom-Version: 2.13" -d '{"query":{"operator":"AND","value":[{"field":"state","operator":"=","value":"open"},{"field":"ai_agent_participated","operator":"=","value":false}]}}'
   ```
2. For each id: fetch transcript (`/conversations/$id?display_as=plaintext`), classify topic/urgency/sentiment via Claude or Loris, write internal note with classification, apply tags, run `/run_assignment_rules`.
3. For Critical-urgency tickets: also `slack-mcp chat_postMessage` to `#cse-on-call`.

**Result:** Every overnight ticket triaged, tagged, routed; on-call paged for criticals.

### Example 2: Escalate a confirmed bug to Linear

**Goal:** Customer reports reproducible crash; escalate to engineering with full context.

**Steps:**
1. Read transcript + attachments via `/conversations/$id`.
2. Search Sentry for matching fingerprint (`sentry-mcp search_issues query=...`).
3. Fill the bug normalization template from `role.md`.
4. `linear-mcp create_issue` with structured description, customer-tier label, Sentry link.
5. Post internal note on the conversation linking the Linear issue id.
6. Reply to customer: workaround + Linear tracking commitment (no fake ETA).

**Result:** Engineering has actionable issue; customer has workaround + transparent next-update commitment.

## Edge cases / gotchas

- **Macros vs Articles vs Saved Replies** — terminology landmine. Fin pulls from **Articles** in Help Center + **Knowledge Sources**. Copilot (agent-side) pulls from **Macros**. Updating one does not update the other. Maintain a Notion DB as cross-platform source of truth.
- **Rate limits** — REST API: 10,000 req / minute per workspace, but burst protection kicks in at 83 req / 10s. Pace bulk operations or use the `Intercom-RateLimit-Remaining` response header to back off.
- **API version pinning** — never call without `Intercom-Version` header. The default version is the workspace's "stable" pin which can change without warning. Pin `2.13`.
- **Fin Resolution Score is opaque** — Intercom does not return the exact score on most endpoints, only the binary `ai_agent.resolution_state` (`assumed_resolved` | `confirmed_resolved` | `routed_to_team`). Score is visible in the UI / reporting endpoint only.
- **`ai_agent_participated` filter** — recently renamed from `bot_participated`. If you're hitting "field not found", upgrade your `Intercom-Version` header.
- **Conversation parts are append-only** — `POST /conversations/$id/parts` cannot delete a previous reply. Mistakes ship to the customer unless you catch them in a draft workflow.
- **Tag IDs, not tag names** — the API requires tag IDs. List tags once (`GET /tags`) and cache the name→id mapping.
- **Fin doesn't read Macros** — common bug: team writes a macro, expects Fin to auto-reply with it; Fin won't see it. Push to Help Center as an Article instead.
- **Webhook payload truncation** — conversation webhook bodies are truncated at 64KB. For long threads, re-fetch the full conversation via REST.
- **EU vs US data residency** — EU workspaces use `api.eu.intercom.io`. US use `api.intercom.io`. Check `Workspace > Region` before pinning the base URL.

## Sources

- [Intercom REST API reference](https://developers.intercom.com/docs/references/rest-api/api.intercom.io/)
- [Intercom OpenAPI spec on GitHub](https://github.com/intercom/Intercom-OpenAPI)
- [Fin AI Agent explained](https://www.intercom.com/help/en/articles/7120684-fin-ai-agent-explained)
- [Fin AI Operator (GA Mar 2026)](https://www.intercom.com/help/en/articles/9442290-fin-ai-operator)
- [Knowledge sources for Fin](https://www.intercom.com/help/en/articles/9440354-knowledge-sources-to-power-ai-agents-and-self-serve-support)
- [Intercom Fin AI Guide 2026 (myaskai)](https://myaskai.com/blog/intercom-fin-ai-agent-complete-guide-2026)
