<!--
Source: https://developers.linear.app/docs + Sentry MCP + role.md bug-normalization template
-->
# Bug Report Normalization → Linear — SKILL

Free-form support ticket → structured Linear (or Jira) issue. Includes: bug-template extraction, Sentry crash matching, customer-impact quantification, environment fingerprinting, workaround capture. Output is an engineering-actionable issue that doesn't bounce back.

## When to use

- **Confirmed reproducible bug** in a support ticket needing engineering action.
- **Customer-tier-driven auto-escalation** — Enterprise tier auto-escalates any bug.
- **Multiple ticket reports of the same fingerprint** → consolidate into one Linear issue with `source_ticket_count`.
- **Sentry-known crash + customer report** — link them.
- **Post-incident bug** — separate from incident itself (incident comms in `incident-customer-comms-statuspage`).

This skill is the *normalization* step. The downstream Linear-creation lives in `escalation-linear-jira-engineering`.

Trigger phrases: "normalize this bug", "create Linear issue from ticket", "match this to Sentry", "bug template", "engineering escalation".

## Setup

```bash
# Linear + Sentry MCPs (already in agent.yaml)
mcp tool linear.create_issue --help
mcp tool sentry.search_issues --help
```

Auth + env: inherits `LINEAR_API_KEY`, `SENTRY_TOKEN` from sibling skills.

Workspace prerequisites:
- Linear labels: `support-escalated`, `bug`, `tier-*`, `severity-*`, `area-*`.
- Sentry projects + organization slug mapped.
- Customer-tier lookup (HubSpot / CRM).

## Common recipes

### Recipe 1: Extract structured bug fields from a free-form ticket

```python
# cli-anything python — feed ticket transcript to Claude with structured-output prompt
PROMPT = """You are a senior support engineer. Read this ticket transcript and extract structured bug fields. If a field cannot be determined, return null.

OUTPUT STRICT JSON only matching this schema:
{
  "title": "Short user-visible description, <=80 chars",
  "expected": "What customer expected, 1-2 sentences",
  "actual": "What actually happened, 1-2 sentences",
  "steps_to_repro": ["step 1", "step 2", ...],
  "environment": {
    "browser": "...",
    "os": "...",
    "app_version": "...",
    "region": "..."
  },
  "frequency": "first_report|cluster|persistent",
  "impact": "cosmetic|workflow_inconvenience|workflow_blocked|data_loss|security",
  "workaround_known": "...|null",
  "search_terms": ["term1", "term2"]  // for Sentry search
}

Transcript:
"""
```

Returns a structured JSON object suitable for downstream Sentry search + Linear create.

### Recipe 2: Look up customer tier + ARR

```bash
EMAIL=$(jq -r '.customer.email' < ticket.json)

curl -sS "https://api.hubapi.com/crm/v3/objects/contacts/search" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"filterGroups\":[{\"filters\":[{\"propertyName\":\"email\",\"operator\":\"EQ\",\"value\":\"$EMAIL\"}]}],\"properties\":[\"tier\",\"company_arr\",\"csm_owner\"]}" \
  | jq '.results[0].properties'
```

Drives `severity × tier → priority` mapping in the engineering escalation skill.

### Recipe 3: Sentry search for matching crash

```bash
# Build query from search_terms
QUERY=$(jq -r '.search_terms | join(" ")' < bug-fields.json)

curl -sS "https://sentry.io/api/0/projects/$ORG/$PROJECT/issues/?query=$QUERY&statsPeriod=30d" \
  -H "Authorization: Bearer $SENTRY_TOKEN" \
  | jq '.[] | {id, title, count, userCount, firstSeen, lastSeen, permalink, fingerprint: .metadata.value}'
```

Pick highest `userCount` match; that's the most relevant Sentry issue. If none match → search broader (`statsPeriod=90d`, drop a term).

### Recipe 4: Search for prior matching support tickets (dedup)

```bash
# Intercom
curl -sS -X POST "https://api.intercom.io/conversations/search" \
  -H "Authorization: Bearer $INTERCOM_TOKEN" -H "Intercom-Version: 2.13" \
  -d "{\"query\":{\"operator\":\"AND\",\"value\":[
    {\"field\":\"source.body\",\"operator\":\"~\",\"value\":\"$SEARCH_TERMS\"},
    {\"field\":\"created_at\",\"operator\":\">\",\"value\":$(date -u -d '30 days ago' +%s)}
  ]}}" | jq '.total_count, [.conversations[].id]'

# Zendesk
curl -sS "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/search.json?query=type:ticket+\"$SEARCH_TERMS\"+created>30days" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" | jq '.count, [.results[].id]'
```

If you find N>=5 matching tickets, this is a cluster, not a single report.

### Recipe 5: Fill the bug normalization template

```python
def render_template(fields, customer, sentry, prior_tickets, source_ticket):
    return f"""# Bug Report — {fields['title']}

## Customer
- Name: {customer['name']}
- Email: {customer['email']}
- Tier: {customer['tier']}
- ARR: ${customer['arr']:,}
- Workspace ID: {customer.get('workspace_id', 'N/A')}
- Source ticket: {source_ticket['url']}

## What they expected
{fields['expected']}

## What actually happened
{fields['actual']}

## Steps to reproduce
{chr(10).join(f"{i+1}. {s}" for i, s in enumerate(fields['steps_to_repro']))}

## Environment
- Browser: {fields['environment'].get('browser', 'N/A')}
- OS: {fields['environment'].get('os', 'N/A')}
- App version: {fields['environment'].get('app_version', 'N/A')}
- Region/locale: {fields['environment'].get('region', 'N/A')}

## Frequency
- [{'x' if fields['frequency']=='first_report' else ' '}] First report
- [{'x' if fields['frequency']=='cluster' else ' '}] Cluster ({len(prior_tickets)} reports in last 30d)
- [{'x' if fields['frequency']=='persistent' else ' '}] Persistent / ongoing

## Customer impact
- [{'x' if fields['impact']=='cosmetic' else ' '}] Cosmetic / annoyance only
- [{'x' if fields['impact']=='workflow_inconvenience' else ' '}] Workflow inconvenience
- [{'x' if fields['impact']=='workflow_blocked' else ' '}] Workflow blocked
- [{'x' if fields['impact']=='data_loss' else ' '}] Data loss / corruption
- [{'x' if fields['impact']=='security' else ' '}] Security implication

## Dollar impact
- Customer ARR: ${customer['arr']:,}
- Number of users affected (Sentry): {sentry.get('userCount', 'N/A') if sentry else 'no Sentry match'}

## Sentry match
{f"- {sentry['permalink']}" if sentry else "- No matching Sentry issue (searched 30d)"}
{f"- Fingerprint: {sentry['fingerprint']}" if sentry else ""}
{f"- First seen: {sentry['firstSeen']}" if sentry else ""}

## Prior tickets ({len(prior_tickets)})
{chr(10).join(f"- {t}" for t in prior_tickets[:10])}

## Workaround offered
{fields['workaround_known'] or 'None identified yet'}
"""
```

### Recipe 6: Compute severity × tier → priority

```python
def priority(severity, tier):
    PRIORITY_MAP = {
        ('crit',  'enterprise'): 1, ('crit',  'growth'):     1,
        ('crit',  'starter'):    2, ('crit',  'free'):       2,
        ('high',  'enterprise'): 2, ('high',  'growth'):     2,
        ('high',  'starter'):    3, ('high',  'free'):       3,
        ('med',   'enterprise'): 2, ('med',   'growth'):     3,
        ('med',   'starter'):    3, ('med',   'free'):       4,
        ('low',   'enterprise'): 3, ('low',   'growth'):     4,
        ('low',   'starter'):    4, ('low',   'free'):       4,
    }
    return PRIORITY_MAP.get((severity, tier), 4)
```

### Recipe 7: Create Linear issue (combined)

```bash
mcp tool linear.create_issue \
  --teamId "team_eng" \
  --title "[BUG] Checkout 422 on plan downgrade — affects Enterprise" \
  --description "$(cat bug-normalization.md)" \
  --labelIds '["lbl_support_escalated","lbl_bug","lbl_tier_enterprise","lbl_severity_high"]' \
  --priority 2

# Then attach the source ticket
mcp tool linear.attachmentLinkURL \
  --issueId $ISSUE_ID \
  --url "https://app.intercom.com/inbox/conversations/$CONV_ID" \
  --title "Intercom #$CONV_ID — source ticket"

# And the Sentry issue
mcp tool linear.attachmentLinkURL \
  --issueId $ISSUE_ID \
  --url "https://sentry.io/issues/$SENTRY_ISSUE_ID" \
  --title "Sentry crash #$SENTRY_ISSUE_ID"
```

Two attachments minimum (source ticket + Sentry); more if cluster spans many tickets.

### Recipe 8: Post internal note on the source ticket

```bash
# Intercom
curl -sS -X POST "https://api.intercom.io/conversations/$CONV_ID/parts" \
  -H "Authorization: Bearer $INTERCOM_TOKEN" -H "Intercom-Version: 2.13" \
  -d '{"message_type":"note","type":"admin","admin_id":"'$ADMIN_ID'","body":"Escalated to engineering as ENG-1234. No ETA yet. I will update by EOD Friday whether it'\''s still no-ETA or has a target."}'

# Zendesk
curl -sS -X PUT "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/tickets/$TICKET_ID.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
  -d '{"ticket":{"comment":{"body":"Escalated to engineering as ENG-1234.","public":false}}}'
```

### Recipe 9: Reply to customer (workaround + transparency, no fake ETA)

```bash
# Per role.md antipattern catalog: NO fabricated ETAs, NO performative empathy.
REPLY="Hi $FIRST_NAME,

I reproduced the error you reported (checkout 422 on plan downgrade). Here's the workaround for now:

1. Log out completely
2. Clear cookies for app.brand.com
3. Log back in via SSO
4. Try the downgrade again

I've logged this as a tracked engineering issue (ENG-1234). No ETA from engineering yet; I'll update you by EOD Friday whether they have a target or still no-ETA.

— $AGENT_NAME"

# Send via platform reply (Intercom example)
curl -sS -X POST "https://api.intercom.io/conversations/$CONV_ID/reply" \
  -H "Authorization: Bearer $INTERCOM_TOKEN" -H "Intercom-Version: 2.13" \
  -d "{\"message_type\":\"comment\",\"type\":\"admin\",\"admin_id\":\"$ADMIN_ID\",\"body\":\"$(echo "$REPLY" | sed 's/$/<br>/' | tr -d '\n')\"}"
```

### Recipe 10: Increment source-ticket count on cluster issue

```bash
# When a NEW ticket matches an existing Linear issue
mcp tool linear.attachmentLinkURL \
  --issueId $EXISTING_LINEAR_ISSUE \
  --url "https://app.intercom.com/inbox/conversations/$NEW_CONV_ID" \
  --title "Intercom #$NEW_CONV_ID — additional report ($N total)"

# Update Linear issue description with new total
NEW_DESC=$(mcp tool linear.issue --id $EXISTING_LINEAR_ISSUE | jq -r '.description' | sed "s/Cluster ([0-9]* reports/Cluster ($N reports/")
mcp tool linear.update_issue --id $EXISTING_LINEAR_ISSUE --description "$NEW_DESC"
```

Engineering sees: "this isn't a one-off; it's growing."

### Recipe 11: Sentry tag for support-reported

```bash
# Mark a Sentry issue as customer-reported (helps engineering prioritize)
curl -sS -X PUT "https://sentry.io/api/0/projects/$ORG/$PROJECT/issues/$SENTRY_ISSUE_ID/" \
  -H "Authorization: Bearer $SENTRY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"isBookmarked":true,"tags":["support-reported","tier-enterprise"]}'
```

Bookmarking surfaces to engineering's Sentry dashboard.

### Recipe 12: Sentry comment with source ticket reference

```bash
curl -sS -X POST "https://sentry.io/api/0/issues/$SENTRY_ISSUE_ID/comments/" \
  -H "Authorization: Bearer $SENTRY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"data":{"text":"Customer-reported in [Intercom #12345](https://app.intercom.com/inbox/conversations/12345) — Acme Corp ($120k ARR). Linear: ENG-1234."}}'
```

Bidirectional link Sentry ↔ Linear ↔ source ticket.

## Examples

### Example 1: Single enterprise bug, full pipeline

**Goal:** Customer reports a reproducible bug; full normalization + escalation.

**Steps:**
1. Customer message → Recipe 1 (extract fields).
2. Recipe 2 (lookup tier) — Enterprise, $120k ARR.
3. Recipe 3 (Sentry search) — matched issue 47 users affected.
4. Recipe 4 (prior tickets) — 2 prior reports last 30d.
5. Recipe 5 + 6 (render template + compute priority=2).
6. Recipe 7 (create Linear with attachments).
7. Recipe 8 (internal note on ticket).
8. Recipe 9 (workaround reply to customer).
9. Recipe 11 + 12 (Sentry bookmarking + cross-link).

**Result:** Engineering has a complete, structured issue. Customer has a workaround + transparent commitment.

### Example 2: Cluster detection — 6th report of same bug

**Goal:** Detect a known cluster; don't open a duplicate.

**Steps:**
1. Recipe 1 extracts fields.
2. Recipe 4 searches prior tickets — finds 5 matches with same `topic-checkout-422`.
3. Search Linear: `mcp tool linear.list_issues --label "support-escalated" --query "checkout 422"`.
4. If a Linear issue exists: Recipe 10 (increment + new attachment).
5. Recipe 8 (internal note: "Already tracked as ENG-1234, 6 reports total.").
6. Recipe 9 (workaround reply).

**Result:** No duplicate issues; engineering's cluster count grows visibly.

## Edge cases / gotchas

- **Don't escalate cosmetic issues** — match `impact=cosmetic` → handle via macro / kb-article path; don't burn engineering attention.
- **Don't open Linear without a workaround attempt** — engineering pushes back if you haven't tried known fixes. Always include the workaround field (or explicitly "None known yet").
- **Sentry search is fuzzy** — exact-error-string searches sometimes miss because Sentry truncates. Try shorter queries.
- **Cluster threshold matters** — `>=5 reports in 30d` per `role.md`. Below that, single-report escalations bloat engineering's queue.
- **Customer PII in description** — sanitize email / phone / API keys before posting to Linear (some engineering teams have lower trust boundary).
- **Free-tier customer reporting Critical-severity bug** — still create Linear, but with priority=3, NOT 1. Free-tier bugs don't bypass enterprise's priority queue.
- **Ticket → Linear → Ticket sync is async** — reverse-sync (Linear `Done` → ticket internal note) lags 5-60min depending on poller.
- **Severity classification confidence** — Claude's severity inference (Recipe 1) is often wrong on first pass. Add a human-review gate before Linear-create for non-enterprise tickets.
- **Search terms quality** — generic terms ("error", "broken") return too many Sentry matches. Force at least 2 specific terms in `search_terms`.
- **Don't auto-create Linear from chat** — at minimum, confirm reproduction. Single-mention-in-Discord isn't a confirmed bug.
- **Mind the ticket cluster vs Sentry cluster mismatch** — same UI symptom can have different Sentry fingerprints. Match by error message text + URL path, not just fingerprint.

## Sources

- [Linear API + GraphQL](https://developers.linear.app/docs)
- [Linear attachments + external references](https://developers.linear.app/docs/graphql/working-with-the-graphql-api/issue-attachments)
- [Sentry Issue Search API](https://docs.sentry.io/api/events/list-a-projects-issues/)
- [Sentry update issue](https://docs.sentry.io/api/events/update-an-issue/)
- [Bug normalization template (role.md companion)](../../role.md)
- [Anthropic structured output prompting](https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/increase-output-consistency)
