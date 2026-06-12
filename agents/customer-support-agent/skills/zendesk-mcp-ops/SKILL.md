<!--
Source: https://developer.zendesk.com/api-reference/
Zendesk Intelligent Triage: https://support.zendesk.com/hc/en-us/articles/4964463770650-About-intelligent-triage
-->
# Zendesk MCP Ops — SKILL

Zendesk Support is the incumbent ticketing platform with Advanced AI bolt-on (Intelligent Triage + Sentiment + Smart Assist). This skill covers the full ticket lifecycle: list / create / update / search tickets, manage macros, push triggers / automations, read SLA policies, and emit breach alerts.

## When to use

- **Recipient runs Zendesk Support** — even if they have Advanced AI, the underlying operations go through the REST API surface this skill wraps.
- **Triage incoming tickets** — Intelligent Triage classifies; this skill applies the resulting tag / group / SLA / assignee.
- **Macro lifecycle** — list, version, lint, push, sunset canned replies.
- **SLA policies + breach detection** — read policies, query breached tickets, fire `slack-mcp` alerts.
- **Trigger / automation authoring** — codify routing rules as triggers (event-driven) and automations (time-based).

Trigger phrases: "triage Zendesk tickets", "draft a Zendesk macro", "check SLA breaches", "create Zendesk trigger", "Zendesk sentiment report".

## Setup

```bash
# Zendesk does NOT have a vendor-published MCP yet (2026-06). Use cli-anything + curl,
# or a community MCP wrapper if installed in CraftBot.
curl -sS https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/users/me.json \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" | jq .
```

Auth + env:
- `ZENDESK_SUBDOMAIN` — `<subdomain>.zendesk.com` value.
- `ZENDESK_EMAIL` — admin user email.
- `ZENDESK_API_TOKEN` — generate at `Admin Center > Apps & integrations > APIs > Zendesk API > Add API token`. Auth uses email/token via basic auth (`$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN`).
- Advanced AI add-on required for Intelligent Triage features (paid, $50/agent/mo).

Workspace prerequisites:
- Intelligent Triage enabled at `Admin Center > Tools > AI > Intelligent triage`. Training takes 1-2 weeks on historical data.
- SLA Policies configured at `Admin Center > Objects and rules > Business rules > Service level agreements`.
- Default group / brand IDs cached locally (groups change rarely; cache hits avoid extra calls).

## Common recipes

### Recipe 1: List unassigned open tickets

```bash
curl -sS "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/search.json?query=type:ticket+status:open+assignee:none" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" | jq '.results[] | {id, subject, created_at, requester_id, tags}'
```

`search.json` returns up to 100 per page; honor `next_page`. For high-volume orgs use the Incremental Tickets Export instead.

### Recipe 2: Read full ticket including comments

```bash
curl -sS "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/tickets/$TICKET_ID.json?include=comments,users,groups" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" | jq .
```

`include=comments` pulls the conversation transcript inline. Public + private comments returned; filter on `public: true` for customer-facing only.

### Recipe 3: Update ticket (set status, group, tags, assignee)

```bash
curl -sS -X PUT "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/tickets/$TICKET_ID.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ticket":{
      "status":"open",
      "group_id":$ENTERPRISE_BILLING_GROUP_ID,
      "assignee_id":$AGENT_ID,
      "priority":"high",
      "tags":["topic-billing","tier-enterprise","sentiment-frustrated","triage-done"],
      "custom_fields":[{"id":$CF_TOPIC_ID,"value":"billing"}],
      "comment":{"body":"Internal: routed to enterprise billing. Customer ARR=$120k.","public":false}
    }
  }'
```

`public: false` is an internal note. Always tag — untagged tickets are noise. Use `additive_tags` instead of `tags` when you want to add without overwriting.

### Recipe 4: Apply an existing macro

```bash
# Preview the macro effect against this ticket (does NOT apply)
curl -sS "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/tickets/$TICKET_ID/macros/$MACRO_ID/apply.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" | jq '.result'

# Then PUT the resulting ticket payload back
curl -sS -X PUT "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/tickets/$TICKET_ID.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
  -d @macro-result.json
```

This 2-step apply gives the agent a chance to lint the comment via Vale before customer-facing.

### Recipe 5: Create a new macro

```bash
curl -sS -X POST "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/macros.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "macro":{
      "title":"[topic-billing] [tier-enterprise] Plan downgrade walkthrough",
      "description":"Cluster of 18 tickets in last 30d on plan downgrade flow.",
      "active":true,
      "restriction":{"type":"Group","id":$ENTERPRISE_BILLING_GROUP_ID},
      "actions":[
        {"field":"comment_value","value":"Here is the exact steps to downgrade your plan..."},
        {"field":"current_tags","value":"macro-applied topic-billing"},
        {"field":"status","value":"pending"}
      ]
    }
  }'
```

`restriction` keeps the macro out of agents' libraries unless they're in the right group — prevents misuse.

### Recipe 6: List SLA policies

```bash
curl -sS "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/slas/policies.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" | jq '.sla_policies[] | {id, title, position, filter, policy_metrics}'
```

Returns policy ID + filter rules + minutes-per-priority. Use IDs in Recipe 7's breach query.

### Recipe 7: Find SLA-breached tickets

```bash
curl -sS "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/search.json?query=type:ticket+status<solved+breached:true" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" | jq '.results[] | {id, subject, priority, status, sla_breached_at: .metric_events}'
```

`breached:true` is a real search operator. For richer breach context, query `/incremental/ticket_metric_events.json?include=metric_set`.

### Recipe 8: Create a trigger (event-based routing rule)

```bash
curl -sS -X POST "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/triggers.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "trigger":{
      "title":"[Route] Enterprise + Billing -> enterprise-billing group",
      "active":true,
      "conditions":{
        "all":[
          {"field":"status","operator":"is","value":"new"},
          {"field":"organization_id","operator":"is","value":"$ENT_ORG_TAG"},
          {"field":"custom_fields_$CF_TOPIC_ID","operator":"is","value":"billing"}
        ]
      },
      "actions":[
        {"field":"group_id","value":$ENTERPRISE_BILLING_GROUP_ID},
        {"field":"priority","value":"high"},
        {"field":"notification_target","value":["$SLACK_TARGET_ID","Routing enterprise billing ticket"]}
      ]
    }
  }'
```

Triggers fire on ticket create/update events. Use `notification_target` to ping Slack via Zendesk's HTTP target.

### Recipe 9: Read Intelligent Triage classification

```bash
curl -sS "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/tickets/$TICKET_ID.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" | jq '.ticket.fields[] | select(.id == "intent" or .id == "language" or .id == "sentiment") '
```

Intelligent Triage writes `intent`, `language`, `sentiment` as custom ticket fields. Read them post-creation; use them in triggers / automation conditions.

### Recipe 10: Bulk-update tickets (mark stale conversations)

```bash
curl -sS -X PUT "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/tickets/update_many.json?ids=$ID1,$ID2,$ID3" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ticket":{"status":"solved","comment":{"body":"Auto-close after 14d no response. Reply to reopen.","public":true}}}'
```

Up to 100 ticket IDs per request. Returns a job ID; poll `/job_statuses/$id.json` for completion.

### Recipe 11: Export tickets for clustering / macro mining

```bash
# Cursor-based incremental export (recommended for >1000 tickets)
curl -sS "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/incremental/tickets/cursor.json?start_time=1748390400" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" | jq '.tickets[] | {id, subject, description, tags}'
```

Feed into embedding-based clustering pipeline. The `start_time` is a Unix timestamp.

### Recipe 12: Read group + brand mappings (one-time cache)

```bash
curl -sS "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/groups.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" | jq '.groups[] | {id, name}' > .zendesk-groups.json

curl -sS "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/brands.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" | jq '.brands[] | {id, name, subdomain}' > .zendesk-brands.json
```

Store and re-use; group / brand IDs rarely change.

## Examples

### Example 1: Daily SLA breach digest

**Goal:** Email support lead each morning with last-24h breaches by tier.

**Steps:**
1. Query `/search.json?query=type:ticket+breached:true+created>24h` for breached IDs.
2. For each, pull tier tag + topic tag + first-response timestamp via `/tickets/$id.json`.
3. Aggregate by tier; format the weekly-SLA-report template from `role.md`.
4. `gmail-mcp send_email` to `support-lead@brand.com`.

**Result:** Lead sees breach trend by tier + top breach reasons in 5 lines.

### Example 2: Mine 90 days of tickets → propose 5 new macros

**Goal:** Reduce macro library drift by surfacing emerging clusters.

**Steps:**
1. Incremental export of last 90 days via `/incremental/tickets/cursor.json`.
2. Embed subjects + descriptions (`cli-anything` python with `openai` ada / Voyage).
3. HDBSCAN cluster; filter clusters ≥ 5 tickets, no existing macro.
4. For each cluster, Claude drafts a macro per the macro template (Vale-linted).
5. Open a Notion review page with the 5 drafts + cluster sample IDs.
6. On approval, `POST /macros.json` for each.

**Result:** 5 new macros covering ~50 tickets/month worth of repeat work.

## Edge cases / gotchas

- **Rate limits depend on plan** — Suite Professional: 700 rpm; Enterprise: 2500 rpm. Honor `Retry-After` header on 429. Bulk exports use the cursor endpoint, not search.
- **Search.json has a 1000-result cap** — even with `next_page`. For >1000 results use the Incremental Export API.
- **Tags overwrite by default** — `tags` field on PUT replaces; use `additive_tags` to add, `remove_tags` to remove. Easy to nuke triage tags accidentally.
- **Macros and Triggers run as the ticket requester unless `assignee` is set** — surprises when a macro changes status to "pending" but the assignee is null → ticket becomes unassigned.
- **Intelligent Triage costs $50/agent/mo** — Advanced AI add-on. Without it, `intent` / `sentiment` ticket fields don't auto-populate. Mention this requirement when reading triage output.
- **Custom field IDs vary by tenant** — never hardcode the `$CF_TOPIC_ID`. Cache from `/ticket_fields.json` per workspace.
- **Sandbox vs production** — `*.zendesk.com` URLs are case-sensitive; sandbox lives at `<subdomain>1.zendesk.com` typically. Verify base URL before any PUT.
- **API token auth uses `email/token` syntax** — easy to forget the literal `/token` separator. `curl -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN"`.
- **Public vs private comments** — `public: true` ships to the customer. Default is `true` on `/tickets.json` ticket create. Always set explicitly to avoid leaking internal notes.
- **SLA policies are evaluated in `position` order** — the first matching policy wins. Reorder rather than duplicate.

## Sources

- [Zendesk Developer Docs (API reference)](https://developer.zendesk.com/api-reference/)
- [Zendesk SLA Policies API](https://developer.zendesk.com/api-reference/ticketing/business-rules/sla_policies/)
- [Intelligent triage overview](https://support.zendesk.com/hc/en-us/articles/4964463770650-About-intelligent-triage)
- [Using intelligent triage for escalations](https://support.zendesk.com/hc/en-us/articles/6353620565530-Using-intelligent-triage-to-identify-and-act-on-ticket-escalations)
- [Zendesk Advanced AI pricing analysis 2026 (Twig)](https://www.twig.so/blog/zendesk-advanced-ai)
- [Zendesk Intelligent Triage 2026 guide (eesel)](https://www.eesel.ai/blog/zendesk-intelligent-triage)
