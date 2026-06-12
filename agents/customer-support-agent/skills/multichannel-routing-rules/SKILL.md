<!--
Source: https://dev.frontapp.com/reference + Zendesk Triggers + Intercom assignment rules
-->
# Multichannel Routing Rules — SKILL

YAML-driven rule engine: `(channel, tier, topic) → (owner, SLA tier, Slack ping)`. Deterministic — same input always produces the same routing. Operates over Zendesk Triggers, Intercom Assignment Rules, Front Rules, HelpScout Workflows, and Slack/Discord routing in parallel.

## When to use

- **New ticket / conversation arrives** — apply routing to assign owner + set SLA + ping.
- **Recipient has 2+ channels** (email + chat + SMS + Discord + voice) — unification matters.
- **VIP / Enterprise needs faster SLA** — tier-based override.
- **Cross-platform rule parity** — same rule expressed in Zendesk + Intercom + Front for shops that run multiple.
- **Codify routing as YAML** for git-tracked changes (not click-ops only).

Trigger phrases: "set up routing rule", "auto-assign new tickets", "route enterprise to dedicated team", "channel routing", "SLA tier rule".

## Setup

```bash
# Most rule engines live inside the ESP. The agent operates them via API.
# Plus a local YAML rule file as the source of truth.
mkdir -p .routing
touch .routing/rules.yaml
```

Auth + env: inherits from `intercom-fin-ai-mcp`, `zendesk-mcp-ops`, `front-multichannel-inbox`, `helpscout-mcp`, `slack-mcp`, `discord-mcp-full`.

Workspace prerequisites:
- Tag schema canonical: `topic-*`, `tier-*`, `channel-*`, `urgency-*`, `language-*`.
- Per-platform group / team / inbox IDs cached locally (`.zendesk-groups.json`, `.intercom-teams.json`, etc.).

## Common recipes

### Recipe 1: Define rules in YAML

```yaml
# .routing/rules.yaml
- rule_id: ent_billing_email
  priority: 100
  when:
    channel: email
    customer.tier: enterprise
    topic: billing
  then:
    assign_team: enterprise_billing
    sla_first_response_minutes: 60
    sla_resolution_minutes: 240
    slack_ping: '#cse-enterprise'
    notify_csm: true

- rule_id: free_bug_chat
  priority: 50
  when:
    channel: chat
    customer.tier: free
    topic: bug
  then:
    assign_team: tier1_support
    sla_first_response_minutes: 1440   # 24h
    sla_resolution_minutes: 4320       # 72h
    require_bug_normalization: true

- rule_id: critical_all_tiers
  priority: 999  # always wins
  when:
    urgency: critical
  then:
    assign_team: oncall
    sla_first_response_minutes: 30
    slack_ping: '#sla-breach'
    pagerduty_incident: true
```

Single source of truth; mirrored to each platform via Recipes 2-5.

### Recipe 2: Express as Zendesk Triggers

```bash
# Translate rule → trigger
curl -sS -X POST "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/triggers.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "trigger":{
      "title":"[rule] ent_billing_email",
      "active":true,
      "conditions":{
        "all":[
          {"field":"status","operator":"is","value":"new"},
          {"field":"via","operator":"is","value":"email"},
          {"field":"organization_id","operator":"is","value":"$ENT_ORG_TAG"},
          {"field":"custom_fields_$CF_TOPIC","operator":"is","value":"billing"}
        ]
      },
      "actions":[
        {"field":"group_id","value":$ENT_BILLING_GROUP_ID},
        {"field":"notification_target","value":["$SLACK_TARGET","Enterprise billing routing"]}
      ]
    }
  }'
```

### Recipe 3: Express as Intercom Assignment Rules

```bash
# Intercom uses workspace-level rule sets, set via UI.
# But you can drive evaluation per-conversation:
curl -sS -X POST "https://api.intercom.io/conversations/$CONV_ID/run_assignment_rules" \
  -H "Authorization: Bearer $INTERCOM_TOKEN" -H "Intercom-Version: 2.13"
```

Or manually assign with the rule's `then.assign_team`:

```bash
curl -sS -X POST "https://api.intercom.io/conversations/$CONV_ID/parts" \
  -H "Authorization: Bearer $INTERCOM_TOKEN" -H "Intercom-Version: 2.13" \
  -d '{"message_type":"assignment","type":"admin","admin_id":"'$ADMIN_ID'","assignee_id":"'$ENT_BILLING_TEAM_ID'","body":"Routed by rule ent_billing_email."}'
```

### Recipe 4: Express as Front Rules

Front Rules are admin-only (set in UI). Programmatic: tag conversations to fire pre-configured Front Rules.

```bash
curl -sS -X POST "https://api2.frontapp.com/conversations/$CONV_ID/tags" \
  -H "Authorization: Bearer $FRONT_TOKEN" \
  -d '{"tag_ids":["tag_route_ent_billing"]}'
```

Pre-configured Front Rule listens on `tag added: tag_route_ent_billing` and assigns to team.

### Recipe 5: Webhook-driven evaluation (preferred — vendor-agnostic)

```python
# On conversation.created webhook from ANY platform, evaluate locally:
import yaml, requests

with open('.routing/rules.yaml') as f:
    RULES = sorted(yaml.safe_load(f), key=lambda r: -r['priority'])

def evaluate(conv):
    """conv: dict with channel, customer_tier, topic, urgency, language, etc."""
    for rule in RULES:
        if all(_match(conv, k, v) for k, v in rule['when'].items()):
            return rule
    return None

def _match(conv, key, want):
    actual = _dotget(conv, key)
    if isinstance(want, list): return actual in want
    return actual == want

# Apply
rule = evaluate(conv)
if rule:
    _assign(conv['platform'], conv['id'], rule['then']['assign_team'])
    _set_sla(conv['platform'], conv['id'], rule['then']['sla_first_response_minutes'])
    if 'slack_ping' in rule['then']:
        slack_post(rule['then']['slack_ping'], f"Routed {conv['id']} by {rule['rule_id']}")
```

Cleanest mental model: rules live in code, platforms execute the side effects.

### Recipe 6: Determine channel from inbound payload

```python
def channel_of(webhook):
    if 'discord' in webhook['source']: return 'discord'
    if 'slack' in webhook['source']:   return 'slack'
    if webhook.get('via') == 'phone':  return 'voice'
    if webhook.get('source', {}).get('type') == 'email': return 'email'
    if webhook.get('source', {}).get('type') == 'chat':  return 'chat'
    return 'other'
```

### Recipe 7: Look up customer tier (HubSpot)

```bash
curl -sS "https://api.hubapi.com/crm/v3/objects/companies/search" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"filterGroups":[{"filters":[{"propertyName":"domain","operator":"EQ","value":"acme.com"}]}],"properties":["tier","mrr","csm_owner"]}' \
  | jq '.results[0].properties.tier'
```

Cache results — tier rarely changes.

### Recipe 8: Apply SLA via Zendesk

Zendesk SLA Policies are admin-configured (UI). The agent's role: set ticket fields that the policy matches on:

```bash
curl -sS -X PUT "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/tickets/$TICKET_ID.json" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
  -d '{"ticket":{"priority":"urgent","custom_fields":[{"id":'$CF_TIER',"value":"enterprise"}]}}'
```

The matching SLA Policy auto-applies.

### Recipe 9: Slack ping with rich context

```bash
mcp tool slack.chat_postMessage \
  --channel '#cse-enterprise' \
  --blocks '[
    {"type":"section","text":{"type":"mrkdwn","text":"*Enterprise billing ticket* INT-12345\nCustomer: <https://app.intercom.com/...|Acme Corp> ($120k ARR)"}},
    {"type":"section","fields":[
      {"type":"mrkdwn","text":"*Tier:* enterprise"},
      {"type":"mrkdwn","text":"*Urgency:* high"},
      {"type":"mrkdwn","text":"*Topic:* billing"},
      {"type":"mrkdwn","text":"*SLA:* 60min first response"}
    ]},
    {"type":"actions","elements":[
      {"type":"button","text":{"type":"plain_text","text":"Open ticket"},"url":"https://app.intercom.com/..."}
    ]}
  ]'
```

### Recipe 10: PagerDuty incident on critical-tier

```bash
curl -sS -X POST "https://api.pagerduty.com/incidents" \
  -H "Authorization: Token token=$PAGERDUTY_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.pagerduty+json;version=2" \
  -d "{
    \"incident\":{
      \"type\":\"incident\",
      \"title\":\"[Support] Critical ticket INT-12345 — Enterprise billing outage\",
      \"service\":{\"id\":\"$PD_SERVICE_ID\",\"type\":\"service_reference\"},
      \"urgency\":\"high\",
      \"body\":{\"type\":\"incident_body\",\"details\":\"Customer Acme Corp, $120k ARR, billing system inaccessible.\"}
    }
  }"
```

`From` header must be a valid PD user email.

### Recipe 11: Rule audit — list active rules per platform

```bash
# Zendesk
curl -sS "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/triggers.json?active=true" \
  -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" | jq '.triggers[] | {id, title, position}'

# Front
curl -sS "https://api2.frontapp.com/inboxes/$INBOX_ID/rules" \
  -H "Authorization: Bearer $FRONT_TOKEN" | jq '._results[]'
```

Compare against `.routing/rules.yaml` weekly. Out-of-sync = drift.

### Recipe 12: Replay (simulate routing on historical tickets)

```python
# Useful for validating rule changes pre-prod
for ticket_id in last_30_days_tickets:
    conv = fetch(ticket_id)
    rule = evaluate(conv)
    actual_owner = conv['assignee']
    if rule and rule['then']['assign_team'] != actual_owner:
        print(f"MISMATCH {ticket_id}: rule={rule['rule_id']}, actual={actual_owner}")
```

Run before deploying a rule change to catch unintended re-routes.

## Examples

### Example 1: Roll out a new rule across Zendesk + Intercom

**Goal:** Ship `ent_billing_email` rule consistently.

**Steps:**
1. Edit `.routing/rules.yaml`, add the rule.
2. Run replay (Recipe 12) on last 30d — confirm no surprise mismatches.
3. Create Zendesk Trigger (Recipe 2).
4. Configure Intercom assignment rule in UI (Intercom has no rule-create API; UI-only).
5. Verify with `mcp tool intercom.run_assignment_rules` against a sample new conv.
6. Commit `.routing/rules.yaml` to git.

**Result:** Rule live across platforms; change is git-tracked.

### Example 2: Critical incident routing test

**Goal:** Confirm critical-urgency tickets actually reach on-call within 30min.

**Steps:**
1. Trigger a test conversation with `urgency=critical`.
2. Confirm Recipe 5 webhook evaluator hits `critical_all_tiers` rule (priority 999).
3. Confirm Slack ping arrives in `#sla-breach` within 60s.
4. Confirm PagerDuty incident created (Recipe 10).
5. Confirm assignee is the on-call engineer (rotation read via PD).
6. Document outcome in runbook.

**Result:** Critical-path routing tested end-to-end.

## Edge cases / gotchas

- **Priority ties** — two rules at the same priority match the same conv. Pick the one with the most-specific `when` clause OR add `tiebreak: rule_id` as a deterministic ordering.
- **Tag races** — applying a tag triggers a Front Rule which applies another tag which triggers another rule. Test for loops.
- **Intercom rule create has no API** — UI-only configuration (June 2026). For programmatic rules, evaluate locally (Recipe 5) and apply via assignment API.
- **Custom field IDs vary per tenant** — never hardcode `$CF_TOPIC_ID`. Cache per-workspace.
- **SLA Policies in Zendesk evaluate by position, not match-specificity** — first match wins. Reorder via API: `PUT /api/v2/slas/policies/reorder.json`.
- **Holiday / weekend coverage** — base SLA policies don't auto-skip non-business hours unless configured. For 24/7 enterprise tier, set `business_hours: false` on the policy.
- **PagerDuty `From` header** — must be a valid PD user email, or 400. Use a service-account user dedicated to the agent.
- **VIP override loops** — VIP enterprise tier should hit Recipe 999 rule; ensure no lower-priority rule re-routes them.
- **YAML schema drift** — when adding a new field (e.g., `language`), older webhook payloads may not have it. Default to None gracefully.
- **Cross-platform drift** — Zendesk Trigger and Intercom Rule expressing the same business rule diverge over time. Quarterly audit (Recipe 11).
- **Test rules in staging first** — replay (Recipe 12) catches some misses but not all. Use a staging workspace for trigger changes.

## Sources

- [Zendesk Triggers API](https://developer.zendesk.com/api-reference/ticketing/business-rules/triggers/)
- [Zendesk SLA Policies API](https://developer.zendesk.com/api-reference/ticketing/business-rules/sla_policies/)
- [Intercom run assignment rules](https://developers.intercom.com/docs/references/rest-api/api.intercom.io/conversations/runassignmentrules)
- [Front Rules + Tags](https://dev.frontapp.com/reference/tags)
- [PagerDuty Incidents API](https://developer.pagerduty.com/api-reference/9d0b4b12e36f9-create-an-incident)
- [Slack chat.postMessage with blocks](https://api.slack.com/methods/chat.postMessage)
