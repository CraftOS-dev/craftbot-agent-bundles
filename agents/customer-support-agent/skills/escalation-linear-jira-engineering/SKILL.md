<!--
Source: https://developers.linear.app/docs and https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/
-->
# Escalation: Linear / Jira Engineering — SKILL

Structured bug normalization → engineering issue. Linear MCP for modern shops; Jira MCP for Atlassian shops; GitHub Issues for OSS / dev-tools. Customer-tier label preserves business context. Bidirectional sync writes engineering status back as ticket internal note.

## When to use

- **Escalating a confirmed bug** (reproducible, customer-impactful) to engineering.
- **Feature requests with cluster ≥ 5 mentions** in 30d → product backlog.
- **Customer-tier-driven escalation** (Enterprise auto-escalates for any bug).
- **P0 / P1 incident escalation** — emergency Linear/Jira issue tied to PagerDuty.
- **Bidirectional sync** — engineering state changes → ticket internal note.

Trigger phrases: "escalate this to engineering", "open a Linear issue from this ticket", "create Jira bug", "engineering handoff", "support escalation".

## Setup

```bash
# Linear MCP (already in agent.yaml)
mcp tool linear.list_teams

# Jira MCP (already in agent.yaml)
mcp tool jira.list_projects

# Or direct API (always works)
curl -sS https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ viewer { id name } }"}'
```

Auth + env:
- **Linear**: `LINEAR_API_KEY` at `Settings > API > Personal API keys`. No "Bearer" prefix in the Authorization header — just the raw key.
- **Jira**: `JIRA_BASE_URL` (e.g., `https://yourorg.atlassian.net`), `JIRA_EMAIL`, `JIRA_API_TOKEN` (at `id.atlassian.com/manage-profile/security/api-tokens`). Basic auth with `email:token`.
- **GitHub**: `GITHUB_TOKEN` (PAT or fine-grained); used for OSS projects.

Workspace prerequisites:
- Linear: a team and a labels schema (`support-escalated`, `bug`, `tier-{enterprise,growth,starter,free}`, `severity-{crit,high,med,low}`).
- Jira: a project and an issue type for `Bug` and `Story`. Customer-impact custom field.

## Common recipes

### Recipe 1: Linear — create issue with structured bug normalization

```graphql
mutation EscalateBug {
  issueCreate(input: {
    teamId: "TEAM_ENG"
    title: "[BUG] Checkout 422 on plan downgrade — affects Enterprise"
    description: """
## Customer
- Name: Jane Doe
- Email: jane@example.com
- Tier: Enterprise
- ARR: $120k
- Workspace ID: ws_abc

## Steps to repro
1. Log in as Enterprise admin
2. Navigate to Settings > Billing > Change Plan
3. Select downgrade to Growth
4. Click Confirm

## Expected
Plan downgrades successfully.

## Actual
HTTP 422 with error code BILL_PLAN_INVALID.

## Sentry match
https://sentry.io/issues/123456 — fingerprint a1b2c3, first seen 2026-06-08, 47 affected users

## Source tickets
- INT-9876 (this one)
- INT-9823 (prior week, same fingerprint)
"""
    labelIds: ["lbl_support_escalated", "lbl_bug", "lbl_tier_enterprise", "lbl_severity_high"]
    priority: 2  # Urgent=1, High=2, Medium=3, Low=4
    stateId: "state_backlog"
  }) {
    issue { id identifier url title }
    success
  }
}
```

```bash
curl -sS https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d @escalate-bug-mutation.json
```

`labelIds` requires you to first fetch label IDs from `team(id).labels`.

### Recipe 2: Linear — list team labels (one-time cache)

```graphql
query TeamLabels {
  team(id: "TEAM_ENG") {
    labels(first: 100) {
      nodes { id name color }
    }
  }
}
```

Cache the name → id mapping in `.linear-labels.json`.

### Recipe 3: Linear — back-link ticket via attachment / external reference

```graphql
mutation AttachExternalTicket {
  attachmentLinkURL(
    issueId: "iss_abc"
    url: "https://yourorg.zendesk.com/agent/tickets/12345"
    title: "Zendesk #12345 — original ticket"
  ) {
    attachment { id url }
    success
  }
}
```

Surfaces the ticket link inside Linear; engineering can jump back to context.

### Recipe 4: Linear — list issues to write status back to ticket (reverse-sync)

```graphql
query EscalatedIssues {
  issues(
    filter: { labels: { name: { eq: "support-escalated" } }, completedAt: { null: false } }
    first: 25
  ) {
    nodes {
      id
      identifier
      title
      state { name }
      completedAt
      attachments { nodes { url } }
    }
  }
}
```

Filter on `state.name = "Done"` to find newly-resolved escalations; post status update back to the original ticket.

### Recipe 5: Jira — create bug

```bash
curl -sS -X POST "$JIRA_BASE_URL/rest/api/3/issue" \
  -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fields":{
      "project":{"key":"ENG"},
      "summary":"[BUG] Checkout 422 on plan downgrade — affects Enterprise",
      "issuetype":{"name":"Bug"},
      "priority":{"name":"High"},
      "labels":["support-escalated","tier-enterprise","severity-high"],
      "description":{
        "type":"doc",
        "version":1,
        "content":[{"type":"paragraph","content":[{"type":"text","text":"## Customer..."}]}]
      },
      "customfield_10050":"Zendesk #12345"
    }
  }' | jq '.key, .self'
```

Note: Jira Cloud REST v3 uses Atlassian Document Format (ADF) for rich text. ADF is verbose but full-fidelity.

### Recipe 6: Jira — transition issue (e.g., to "In Progress")

```bash
# Find available transitions
curl -sS "$JIRA_BASE_URL/rest/api/3/issue/ENG-123/transitions" \
  -u "$JIRA_EMAIL:$JIRA_API_TOKEN" | jq '.transitions[] | {id, name}'

# Apply transition
curl -sS -X POST "$JIRA_BASE_URL/rest/api/3/issue/ENG-123/transitions" \
  -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"transition":{"id":"31"}}'
```

Transition IDs differ per workflow scheme; always list first.

### Recipe 7: Jira — add a remote link (back to support ticket)

```bash
curl -sS -X POST "$JIRA_BASE_URL/rest/api/3/issue/ENG-123/remotelink" \
  -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "object":{
      "url":"https://yourorg.zendesk.com/agent/tickets/12345",
      "title":"Zendesk #12345 — original ticket"
    }
  }'
```

### Recipe 8: Jira — JQL search for escalated bugs

```bash
curl -sS "$JIRA_BASE_URL/rest/api/3/search?jql=labels=support-escalated+AND+resolution=Unresolved+ORDER+BY+priority+DESC" \
  -u "$JIRA_EMAIL:$JIRA_API_TOKEN" | jq '.issues[] | {key, summary, status: .fields.status.name, priority: .fields.priority.name}'
```

### Recipe 9: GitHub Issues — open issue (OSS shops)

```bash
gh issue create \
  --repo brand/app \
  --title "[BUG] Checkout 422 on plan downgrade — affects Enterprise" \
  --body "$(cat bug-normalization.md)" \
  --label "support-escalated,bug,tier-enterprise,severity-high"
```

Or via REST:

```bash
curl -sS -X POST "https://api.github.com/repos/brand/app/issues" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{
    "title":"[BUG] Checkout 422 on plan downgrade",
    "body":"...",
    "labels":["support-escalated","bug","tier-enterprise","severity-high"]
  }'
```

### Recipe 10: Push status back to ticket on resolve

```bash
# When Linear issue moves to "Done":
# 1. Read attachment URLs from issue (Recipe 4)
# 2. For each ticket-platform URL, post an internal note

# Intercom internal note
curl -sS -X POST "https://api.intercom.io/conversations/$CONV_ID/parts" \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H "Intercom-Version: 2.13" \
  -d '{"message_type":"note","type":"admin","admin_id":"'$ADMIN_ID'","body":"Engineering shipped the fix in ENG-1234 (version 4.12.3). Please verify and let the customer know if the issue persists."}'

# Zendesk
curl -sS -X PUT "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/tickets/$TICKET_ID.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
  -d '{"ticket":{"comment":{"body":"Engineering shipped the fix in ENG-1234.","public":false}}}'
```

### Recipe 11: Pre-escalation Sentry match

```bash
# sentry-mcp search by ticket keywords
mcp tool sentry.search_issues \
  --project_slug app-prod \
  --query "BILL_PLAN_INVALID checkout 422" \
  --limit 5

# Or REST
curl -sS "https://sentry.io/api/0/projects/$ORG/$PROJECT/issues/?query=BILL_PLAN_INVALID+checkout+422" \
  -H "Authorization: Bearer $SENTRY_TOKEN" | jq '.[] | {id, title, count, userCount, firstSeen, permalink}'
```

Always attempt a Sentry match BEFORE opening the Linear issue. Pre-attached crash context gets faster engineering action.

### Recipe 12: Priority mapping (severity × tier → priority)

```python
# Default mapping; tune per recipient
PRIORITY = {
    ('crit',  'enterprise'): 1,  # Urgent
    ('crit',  'growth'):     1,
    ('crit',  'starter'):    2,
    ('crit',  'free'):       2,
    ('high',  'enterprise'): 2,
    ('high',  'growth'):     2,
    ('high',  'starter'):    3,  # Medium
    ('high',  'free'):       3,
    ('med',   'enterprise'): 2,
    ('med',   'growth'):     3,
    ('med',   'starter'):    3,
    ('med',   'free'):       4,
    ('low',   '*'):          4,
}
```

Apply this mapping before populating `priority` on the Linear / Jira create.

## Examples

### Example 1: Full escalation pipeline

**Goal:** Customer reports a reproducible bug; full pipeline runs.

**Steps:**
1. Read transcript + attachments from Zendesk / Intercom.
2. Run `sentry-mcp search_issues` for keyword match (Recipe 11).
3. Fill bug normalization template from `role.md`.
4. `linear-mcp create_issue` with structured description, labels, priority (Recipes 1 + 12).
5. `attachmentLinkURL` to back-link the ticket (Recipe 3).
6. Internal note on the ticket: "Logged as ENG-1234; no ETA yet."
7. Customer-facing reply: workaround + tracking commitment (no fake ETA).

**Result:** Engineering has actionable issue; customer has workaround + transparency.

### Example 2: Atlassian shop with Jira + Slack escalation

**Goal:** Recipient uses Jira; ticket escalation also pings on-call Slack.

**Steps:**
1. Bug normalization (Recipe 5 with ADF body).
2. `slack-mcp chat_postMessage` to `#eng-on-call` with the Jira issue link + customer impact summary.
3. `remotelink` (Recipe 7) back to the source Zendesk ticket.
4. When Jira issue transitions to Done (poll Recipe 8 daily), push back internal note (Recipe 10).

**Result:** Atlassian-native flow; Slack visibility for on-call.

## Edge cases / gotchas

- **Linear auth header has NO `Bearer` prefix** — just the raw key. Common 401 cause.
- **Linear labels are scoped to the team** — you can't apply a label from team A to an issue in team B. List labels per-team.
- **Jira ADF is verbose** — for plain text, use `{"type":"paragraph","content":[{"type":"text","text":"..."}]}`. For Markdown sources, use the `marked` library to convert before posting.
- **Jira priority field requires the exact priority name** — `"High"` not `"high"`. Names are workspace-specific.
- **Jira issue type names are workspace-specific** — `"Bug"`, `"Story"`, `"Task"` are common defaults; verify per project.
- **GraphQL vs REST** — Linear is GraphQL-only; Jira is REST. The mental model is different (mutations vs PATCH endpoints).
- **Linear priority is INT** — 1=Urgent, 2=High, 3=Medium, 4=Low. Easy to invert if you assume bigger=higher.
- **Reverse sync is async** — when engineering closes an issue, the ticket-side post-back can lag. Use a cron + idempotent posting (check if "Engineering shipped" note exists before re-posting).
- **Rate limits**: Linear: 1500 req / hour; Jira: 10 req / sec sustained, burst 100; GitHub: 5000 / hour authenticated.
- **Customer PII in description** — sanitize email / phone before posting to engineering tools (some engineering teams don't have a data-access privilege model).
- **Don't escalate to engineering without a workaround attempt first** — the antipattern from `role.md`. Engineering pushes back if you haven't tried known fixes.

## Sources

- [Linear API + GraphQL docs](https://developers.linear.app/docs)
- [Linear webhooks](https://developers.linear.app/docs/graphql/webhooks)
- [Atlassian Jira Cloud REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [Atlassian Document Format (ADF) reference](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/)
- [Sentry Issue Search API](https://docs.sentry.io/api/events/list-a-projects-issues/)
- [GitHub Issues REST API](https://docs.github.com/en/rest/issues/issues)
