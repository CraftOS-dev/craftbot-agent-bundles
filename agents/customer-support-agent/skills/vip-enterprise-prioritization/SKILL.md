<!--
Source: HubSpot custom properties + Zendesk Routing + Intercom Customer Tier
-->
# VIP / Enterprise Prioritization — SKILL

CRM tier (HubSpot / Salesforce) → platform routing rule + tighter SLA tier + dedicated channel ping. Read tier on `conversation.created`; override default routing if `tier=enterprise`. Includes deterministic SLA escalation, ARR-aware Slack pings, and Slack Connect / dedicated channel patterns.

## When to use

- **Enterprise / VIP conversation arrives** — bypass default queue, ping dedicated team.
- **ARR-based escalation** — > $X ARR triggers enterprise tier even if CRM lags.
- **Slack Connect channel customers** — separate routing pattern (they're already in your workspace).
- **Customer Success Manager (CSM) notification** — VIP CSMs get pinged on any ticket from their book.
- **SLA tier override** — enterprise on chat gets the email-tier SLA (faster).

Complements `multichannel-routing-rules` — that skill defines the YAML; this skill handles the VIP lookup + override patterns.

Trigger phrases: "VIP routing", "enterprise prioritization", "Slack Connect customer", "CSM ping", "enterprise SLA".

## Setup

```bash
# Inherits HubSpot + Slack + ESP credentials from sibling skills
# Optional: Salesforce
curl -sS "https://$SF_INSTANCE.my.salesforce.com/services/data/v56.0/sobjects/Account/$ACC_ID" \
  -H "Authorization: Bearer $SF_TOKEN"
```

Auth + env: inherits `HUBSPOT_TOKEN`, `SF_TOKEN` (if Salesforce), `SLACK_BOT_TOKEN`, ESP creds.

Workspace prerequisites:
- CRM has a stable `tier` field on companies/accounts.
- CRM has `csm_owner` field linking to the named CSM.
- Dedicated Slack channels: `#cse-enterprise`, `#cse-growth`, `#cse-on-call`.
- ESP teams: `enterprise_support`, `enterprise_billing`, `tier1`.

## Common recipes

### Recipe 1: Look up customer tier by email (HubSpot)

```bash
EMAIL="user@acme.com"

curl -sS "https://api.hubapi.com/crm/v3/objects/contacts/search" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"filterGroups\":[{\"filters\":[{\"propertyName\":\"email\",\"operator\":\"EQ\",\"value\":\"$EMAIL\"}]}],
    \"properties\":[\"associatedcompanyid\",\"tier\",\"csm_owner\"],
    \"limit\":1
  }" | jq '.results[0].properties'
```

Cache `email → {tier, csm_owner}` for 1h to reduce HubSpot API hits.

### Recipe 2: Look up by company domain (broader match)

```bash
DOMAIN=$(echo "$EMAIL" | awk -F@ '{print $2}')

curl -sS "https://api.hubapi.com/crm/v3/objects/companies/search" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"filterGroups\":[{\"filters\":[{\"propertyName\":\"domain\",\"operator\":\"EQ\",\"value\":\"$DOMAIN\"}]}],
    \"properties\":[\"tier\",\"annualrevenue\",\"csm_owner\",\"slack_connect_channel\"],
    \"limit\":1
  }" | jq '.results[0].properties'
```

Catches @newhire@acme.com when their contact record doesn't exist yet.

### Recipe 3: ARR-based fallback tier

```python
def effective_tier(crm_tier, arr):
    """If CRM tier is missing/stale, infer from ARR."""
    if crm_tier in ('enterprise', 'growth', 'starter', 'free'):
        return crm_tier
    if arr is None: return 'unknown'
    if arr >= 100000: return 'enterprise'
    if arr >= 25000:  return 'growth'
    if arr >= 1000:   return 'starter'
    return 'free'
```

Apply on every routing call. ARR cutoffs are per-recipient.

### Recipe 4: Salesforce lookup (alternative CRM)

```bash
curl -sS "https://$SF_INSTANCE.my.salesforce.com/services/data/v56.0/query?q=$(echo "SELECT Tier__c, AnnualRevenue, CSM_Owner__c FROM Account WHERE Domain__c = 'acme.com' LIMIT 1" | jq -sRr @uri)" \
  -H "Authorization: Bearer $SF_TOKEN" | jq '.records[0]'
```

### Recipe 5: Apply enterprise override on Zendesk ticket

```bash
TIER=$(lookup_tier "$EMAIL")
if [ "$TIER" = "enterprise" ]; then
  curl -sS -X PUT "https://$ZENDESK_SUBDOMAIN.zendesk.com/api/v2/tickets/$TICKET_ID.json" \
    -u "$ZENDESK_EMAIL/token:$ZENDESK_API_TOKEN" \
    -d '{
      "ticket":{
        "group_id":'$ENT_SUPPORT_GROUP_ID',
        "priority":"high",
        "custom_fields":[{"id":'$CF_TIER_ID',"value":"enterprise"}],
        "tags":["tier-enterprise","vip-routed"]
      }
    }'
fi
```

Setting `tier-enterprise` tag also fires Zendesk SLA Policy that targets that tag.

### Recipe 6: Slack ping with rich context (enterprise)

```bash
ARR=$(jq -r '.annualrevenue' < customer.json)
CSM=$(jq -r '.csm_owner' < customer.json)

mcp tool slack.chat_postMessage \
  --channel '#cse-enterprise' \
  --blocks '[
    {"type":"section","text":{"type":"mrkdwn","text":"*Enterprise ticket* <https://app.intercom.com/...|Acme Corp> ($'"$ARR"' ARR)\nCSM: <@'"$CSM"'>"}},
    {"type":"section","fields":[
      {"type":"mrkdwn","text":"*Topic:* billing"},
      {"type":"mrkdwn","text":"*Urgency:* high"},
      {"type":"mrkdwn","text":"*SLA:* 60min first response"},
      {"type":"mrkdwn","text":"*Channel:* email"}
    ]},
    {"type":"actions","elements":[
      {"type":"button","text":{"type":"plain_text","text":"Open ticket"},"url":"https://app.intercom.com/..."},
      {"type":"button","text":{"type":"plain_text","text":"Acknowledge"},"value":"ack_'"$TICKET_ID"'"}
    ]}
  ]'
```

`<@$CSM>` pings the CSM in Slack. ARR visible immediately.

### Recipe 7: Slack Connect routing pattern

If the customer has a Slack Connect channel:

```bash
SLACK_CONNECT_CH=$(echo "$CUSTOMER" | jq -r '.slack_connect_channel')

# Post the ticket in their Slack Connect channel for transparency
mcp tool slack.chat_postMessage \
  --channel "$SLACK_CONNECT_CH" \
  --text "Hi! We received your support request via email. I'm $AGENT_NAME — happy to continue here or stick with email. https://app.intercom.com/..."
```

VIP customers often prefer Slack Connect; offering both is appreciated.

### Recipe 8: SLA tier table

```yaml
# Override defaults from role.md per-customer
sla_overrides:
  enterprise:
    first_response_min: 60
    resolution_min: 240
    weekend_coverage: true
  growth:
    first_response_min: 240
    resolution_min: 1440
  starter:
    first_response_min: 480
    resolution_min: 2880
  free:
    first_response_min: 1440
    resolution_min: 4320

# Critical urgency overrides ALL tiers to 30min first response
critical_override_min: 30
```

### Recipe 9: CSM dashboard query

```sql
-- Per-CSM ticket volume + SLA hit rate
SELECT
  c.csm_owner,
  COUNT(*) AS tickets_30d,
  ROUND(100.0 * SUM(CASE WHEN t.first_response_breached THEN 0 ELSE 1 END) / COUNT(*), 1) AS frt_sla_pct,
  ROUND(AVG(t.first_response_minutes), 1) AS avg_frt_min
FROM support.tickets t
JOIN crm.customers c ON t.email = c.email
WHERE c.tier = 'enterprise'
  AND t.created_at >= NOW() - INTERVAL '30 days'
GROUP BY c.csm_owner
ORDER BY frt_sla_pct ASC;  -- worst-performing first
```

Surfaces overloaded CSMs.

### Recipe 10: Pre-emptive CSM notification on tier upgrade

```bash
# When CRM tier changes from growth → enterprise:
curl -sS -X POST "https://api.hubapi.com/automation/v3/workflows/$WORKFLOW_ID/enrollments/contact/$CONTACT_ID" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN"
# HubSpot workflow notifies CSM + sends welcome to enterprise tier
```

Doesn't impact ticket triage but improves CSM continuity.

### Recipe 11: Detect new-from-target-account (no contact yet)

```bash
# Email user@acme.com arrives but no HubSpot contact exists
# Check if @acme.com is a known company
DOMAIN=$(echo "$EMAIL" | awk -F@ '{print $2}')

COMPANY=$(curl -sS "https://api.hubapi.com/crm/v3/objects/companies/search" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -d "{\"filterGroups\":[{\"filters\":[{\"propertyName\":\"domain\",\"operator\":\"EQ\",\"value\":\"$DOMAIN\"}]}],\"properties\":[\"tier\"]}" \
  | jq -r '.results[0].properties.tier // empty')

if [ "$COMPANY" = "enterprise" ]; then
  # New employee at an enterprise account — auto-create contact + assign tier
  curl -sS -X POST "https://api.hubapi.com/crm/v3/objects/contacts" \
    -H "Authorization: Bearer $HUBSPOT_TOKEN" \
    -d "{\"properties\":{\"email\":\"$EMAIL\",\"tier\":\"enterprise\"}}"
fi
```

Catches new-employee tickets without manual CRM sync.

### Recipe 12: VIP escalation on customer tier change in conversation

```bash
# Sometimes a Growth-tier conversation reveals the customer just upgraded
# Watch for keywords "we just signed", "upgrading", etc.
# When detected, prompt agent to verify tier:

mcp tool slack.chat_postMessage \
  --channel '#cse-on-call' \
  --text "Conversation $TICKET_ID mentions an upgrade. Confirm tier with sales — may need re-routing."
```

## Examples

### Example 1: Enterprise email arrives, full enterprise pipeline

**Goal:** New email from `jane@acme.com`; route to enterprise + ping CSM.

**Steps:**
1. Webhook `conversation.created` from Intercom.
2. Recipe 1 — lookup tier=enterprise, csm_owner=@john.
3. Recipe 5 (adapt for Intercom) — assign to enterprise team.
4. Recipe 6 — Slack ping in `#cse-enterprise` with ARR + CSM mention.
5. If customer has Slack Connect: Recipe 7 — cross-post in their channel.
6. SLA enforced via tier-tag + Zendesk SLA Policy (Recipe 8).

**Result:** Enterprise customer sees tight first-response; CSM is in the loop.

### Example 2: Slack Connect customer raises a question

**Goal:** Customer posts in shared Slack Connect channel — treat as ticket.

**Steps:**
1. `slack-mcp message.created` webhook fires for `$SLACK_CONNECT_CH`.
2. Look up channel → customer mapping (cache, or `customers.slack_connect_channel = ch_id`).
3. Auto-create Intercom conversation with channel=`slack_connect`.
4. Tier=enterprise (known from CRM); apply Recipe 5 + 6 routing.
5. CSM (or assigned agent) replies in Slack Connect channel directly; agent mirrors reply back to Intercom for record.

**Result:** Conversation lives in Slack Connect (customer's preference); record preserved in ticketing system.

## Edge cases / gotchas

- **Multi-tier accounts** — same customer can have multiple personas (e.g., Acme Corp has 50 users; CEO is enterprise-tier, IT-admin is growth-tier). Use the company-level tier, not contact-level.
- **HubSpot tier property may be stale** — if Sales hasn't updated post-renewal, the CRM lies. Fall back to ARR (Recipe 3).
- **Domain-based lookup limitations** — generic emails (gmail.com, @example.com) can't be matched on domain. Require email match.
- **CSM ping fatigue** — pinging CSM on every ticket erodes signal. Throttle to one-ping-per-day-per-CSM-per-customer.
- **Slack Connect customers expect Slack-native replies** — ESP-mediated replies feel impersonal. Where possible, reply in Slack Connect directly and sync back to ESP.
- **Tier override loops** — VIP customer with critical urgency: SLA from `critical_override_min` should win, not tier SLA. Configure rule priority correctly.
- **Sales-flagged "VIP prospect"** — pre-customer tier; HubSpot may have a `lifecycle_stage=opportunity` with `vip_flag=true`. Treat as enterprise-tier for support purposes during evaluation.
- **CSM offline / vacation** — Slack-mention an unresponsive person creates frustration. Use `slack-mcp users.getPresence` to detect; fall back to CSM's backup or team channel.
- **Cross-tier collision in Slack Connect** — your `#enterprise` Slack Connect with Acme has multiple Acme users; some are tier-mapped, some aren't. Apply company tier across all participants.
- **Don't over-prioritize one VIP at others' expense** — if 5 enterprise customers all hit critical at the same time, you still need a queue policy.
- **Track tier history** — `tier_at_ticket_create` is more useful than `tier_now` for SLA-hit rate analysis (tier may have changed mid-resolution).
- **CRM API rate limits** — HubSpot free: 100 req/10s. Burst-cache email→tier lookups.

## Sources

- [HubSpot Contacts Search API](https://developers.hubspot.com/docs/api/crm/contacts)
- [HubSpot Companies Search API](https://developers.hubspot.com/docs/api/crm/companies)
- [Salesforce REST Query API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/dome_query.htm)
- [Zendesk SLA Policies API](https://developer.zendesk.com/api-reference/ticketing/business-rules/sla_policies/)
- [Slack Connect (channel docs)](https://slack.com/help/articles/360037246403-Make-channels-shared-with-other-companies)
- [VIP / Enterprise routing playbook (role.md)](../../role.md)
