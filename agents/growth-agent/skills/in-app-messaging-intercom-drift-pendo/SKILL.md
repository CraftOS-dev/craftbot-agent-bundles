<!--
Source: Intercom + Fin AI 2026 + Customer.io vs Braze 2026 comparison + clonepartner Intercom vs Drift decision matrix
-->
# In-App Messaging — Intercom / Customer.io / Pendo / 1mind SKILL

> Tool selection + event-triggered message design for PLG in-app messaging. Drift sunset March 2026; 1mind is the successor for Drift refugees. Intercom Fin AI auto-resolves 50-70% of inbound (2026).

## When to use

Trigger phrases:
- "Set up in-app messaging"
- "Trigger message when user does X"
- "Intercom vs Customer.io vs Pendo"
- "Drift sunset what next?" (use 1mind)
- "Upgrade prompt design"
- "Customer support chat" (pair Fin AI with Intercom)

Pair: `free-to-paid-upgrade-prompts`, `win-back-campaigns`, `behavioral-cohort-design` (audience), `onboarding-userpilot-appcues-chameleon` (parallel tour delivery).

## Setup

```bash
export INTERCOM_TOKEN="dG9rOi..."
export CUSTOMERIO_API_KEY="cio_..."
export CUSTOMERIO_SITE_ID="..."
export PENDO_INTEGRATION_KEY="pdo_..."
export ONEMIND_API_KEY="1m_..."
```

Required event taxonomy (Object-Action past-tense) — same shape across tools.

## Tool decision matrix (June 2026)

| Tool | Product tours | In-app chat | AI agent (auto-resolve) | Event-trigger logic | Best for |
|---|---|---|---|---|---|
| **Intercom** | Best-in-class | ✓ | **Fin AI** (50-70% auto-resolve, 2026) | Good | PLG + B2B SaaS; want everything in one |
| **Customer.io** | ✗ (use w/ Pendo or Userpilot) | ✓ (Customer.io Chat 2026) | Limited | **Best-in-class** | Logic-heavy event-triggered journeys |
| **Pendo Resource Center** | ✓ | ✗ | ✗ | Basic | Pendo customer; want guides + RC unified |
| **Userpilot** | ✓ | ✗ | ✗ | Basic | Userpilot customer; native to onboarding |
| **1mind** (Drift successor, March 2026) | ✓ | ✓ | ✓ | Good | Drift refugees; AI-conversational-first |
| **Crisp** | ✓ | ✓ | Basic | Basic | Bootstrapped / SMB |
| **HubSpot Chat** | Limited | ✓ | HubSpot AI | Linked to HubSpot CRM | HubSpot-native orgs |

Pricing (2026):
- Intercom: $29 starter; escalates fast — typical PLG team $2-15K/mo at scale; Fin AI = $0.99 per resolved conversation
- Customer.io: $150-1500/mo; usage-based above 5K profiles
- 1mind: ~$1500/mo starter; AI-conversational-first pricing
- Pendo Resource Center: bundled w/ Pendo
- Crisp: free starter; $25-95/mo paid

## Common recipes

### Recipe 1: Intercom — trigger message via cohort event

```bash
# Create cohort in PostHog → sync to Intercom via Hightouch (Recipe in reverse-etl skill)
# Or directly tag user when event fires:

curl -X POST "https://api.intercom.io/contacts/$CONTACT_ID/tags" \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"id": "approaching_usage_limit"}'

# Intercom Series triggered on tag: "approaching_usage_limit"
# Message sent: "You're at 87% of your free tier. Upgrade for unlimited."
```

### Recipe 2: Intercom — Series via API (event-triggered campaign)

```bash
curl -X POST "https://api.intercom.io/messages" \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message_type": "inapp",
    "subject": "Ready to unlock unlimited?",
    "body": "<p>You hit 90% of your free tier today.</p>",
    "template": "plain",
    "from": {"type": "admin", "id": "12345"},
    "to": {"type": "user", "id": "USER_ID"}
  }'
```

### Recipe 3: Intercom Fin AI — configure auto-resolve

```bash
# Configure Fin AI on knowledge sources (Help Center + docs URL)
curl -X POST "https://api.intercom.io/ai/agent/sources" \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -d '{
    "type": "external_pages",
    "url": "https://help.yourdomain.com",
    "language": "en"
  }'

# Set escalation rules
curl -X PUT "https://api.intercom.io/ai/agent/settings" \
  -H "Authorization: Bearer $INTERCOM_TOKEN" \
  -d '{
    "escalate_to_human": ["billing", "refund", "complaint"],
    "confidence_threshold": 0.8
  }'
```

Fin AI claim (Intercom Apr 2026): 50-70% of inbound auto-resolved. Cost: $0.99 per resolved conv. Calc ROI: if avg agent time = 8 min × $40/hr fully loaded = $5.33 saved per resolve.

### Recipe 4: Customer.io — event-triggered campaign

```bash
# Create campaign triggered by behavioral cohort entry
curl -X POST "https://api.customer.io/v1/campaigns" \
  -H "Authorization: Bearer $CUSTOMERIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Upgrade prompt - approaching limit",
    "trigger": {
      "type": "event",
      "event_name": "Limit Approached",
      "filters": {"usage_pct": {"gte": 80}}
    },
    "actions": [
      {"type": "email", "template_id": "tpl_upgrade_offer"},
      {"type": "in_app", "template_id": "tpl_upgrade_modal"}
    ],
    "exit_criteria": "User Subscribed OR 14 days elapsed"
  }'
```

### Recipe 5: Customer.io — segment-driven messaging

```bash
curl -X POST "https://api.customer.io/v1/segments" \
  -H "Authorization: Bearer $CUSTOMERIO_API_KEY" \
  -d '{
    "name": "Dormant 30+ days",
    "conditions": {
      "and": [
        {"event_count": {"event": "session_started", "operator": "lt", "value": 1, "window_days": 30}},
        {"attribute": {"name": "plan_tier", "operator": "eq", "value": "paid"}}
      ]
    }
  }'
```

### Recipe 6: Pendo Resource Center — config

Pendo Resource Center = persistent help widget with announcement / guide / search.

```bash
curl -X POST "https://app.pendo.io/api/v1/resourcecenter" \
  -H "x-pendo-integration-key: $PENDO_INTEGRATION_KEY" \
  -d '{
    "modules": ["announcements", "onboarding", "search", "feedback"],
    "audience": "all_users",
    "branding": {"color": "#FF6B35", "icon": "lightbulb"}
  }'
```

### Recipe 7: 1mind — Drift refugees, set up conversational AI

```bash
# 1mind = March 2026 Drift successor; AI-conversational-first
curl -X POST "https://api.1mind.com/v1/playbooks" \
  -H "Authorization: Bearer $ONEMIND_API_KEY" \
  -d '{
    "name": "Lead qualifier",
    "trigger": "first_visit_pricing_page",
    "ai_persona": "qualifier_assistant",
    "qualifying_questions": [
      "What problem brings you here today?",
      "Team size?",
      "Currently using a competitor?"
    ],
    "handoff": {"to": "sales", "criteria": "team_size > 50"}
  }'
```

### Recipe 8: Message-type → tool map (when to send what)

| Message type | Best tool | Why |
|---|---|---|
| Welcome on first session | Userpilot / Appcues / Pendo | Tied to onboarding tour |
| Feature discovery (post-aha) | Intercom / Userpilot | Contextual to behavior |
| Upgrade prompt (PQL-trigger) | Customer.io / Intercom | Event-trigger reliable |
| Win-back (dormant 30+) | Customer.io / Klaviyo | Logic-heavy sequencing |
| Support chat | Intercom + Fin AI | Auto-resolve + handoff |
| Pre-sales lead qual | 1mind / HubSpot Chat | Conversational AI |
| Announcement / changelog | Pendo Resource Center | Persistent + searchable |

### Recipe 9: Measure in-app message lift (A/B vs control)

```sql
SELECT
  variant,
  count() AS shown,
  countIf(cta_clicked) AS clicked,
  clicked * 100.0 / shown AS ctr_pct,
  countIf(target_action_completed) AS converted,
  converted * 100.0 / shown AS conv_rate_pct
FROM cohort_with_message_treatment
GROUP BY variant
```

Use GrowthBook to randomize treatment (send vs hold-out 10%).

### Recipe 10: Frequency capping (avoid message fatigue)

```python
# Max 2 in-app messages per user per 7 days
def can_send_message(user, message_id):
    sent_last_7d = count_messages(user, window_days=7)
    if sent_last_7d >= 2:
        return False
    if message_already_sent(user, message_id, window_days=30):
        return False
    return True
```

Track per-user message-fatigue metric; alert if dismissal rate climbs > 20%.

## Examples

### Example 1: B2B SaaS, PLG + paid plan, $5K/mo budget

Stack: Intercom (chat + Fin AI + product tours) + Customer.io (event-triggered email + in-app behavioral journeys).

Trigger map:
- Approach usage limit → Customer.io campaign → in-app + email
- New feature launch → Intercom announcement
- Stuck during onboarding → Fin AI chat surface
- Dormant 30+ days → Customer.io win-back sequence (hand off to `win-back-campaigns`)

### Example 2: Pre-PMF startup, $0 budget

Use Crisp (free) for chat + manual triage.
Use Userpilot Starter ($249/mo) for onboarding tours.
Defer Customer.io until paid plan signals product-market-fit.

### Example 3: Sales-led + PLG hybrid

Intercom for in-app + Fin AI.
1mind for high-intent visitor qualifier on pricing page.
Slack alert via `slack-mcp` to AE when high-fit visitor identified.

## Edge cases / gotchas

- **Intercom pricing surprise** — pricing tiers escalate with MAU + features; budget for 3x your starter tier at scale.
- **Fin AI hallucination risk** — train only on verified Help Center content; review weekly. Escalate ambiguous (refund, billing, complaint) to human.
- **Drift sunset March 2026** — Drift integrations break; migrate to 1mind or Intercom pre-sunset.
- **In-app message fatigue** — > 3 messages/week → dismiss rate spikes 2-3x. Cap aggressively.
- **Tool overlap (onboarding + messaging)** — Userpilot/Pendo do both tours + messages; layering Intercom doubles vendor cost. Pick one for both unless you need Intercom's chat.
- **GDPR — track-and-target** — cookie consent for behavioral targeting; check region defaults.
- **Server-side event timing** — Customer.io triggers on event arrival; client-side network failures cause silent message non-delivery. Use server-side event firing where possible.
- **CRM vs CDP source-of-truth** — Customer.io syncs with HubSpot/Salesforce; ensure user attributes flow one direction or you get conflicts.
- **Cohort sync latency** — PostHog cohort → Intercom tag via Hightouch ~5min-1hr lag; design for non-realtime.
- **Mobile-app in-app messaging** — Intercom + Pendo + Appcues all support, but SDK setup is per-platform; budget engineering time.

## Sources

- Intercom (Fin AI): https://www.intercom.com/ + https://www.intercom.com/fin
- Customer.io vs Braze 2026: https://www.getvero.com/resources/braze-vs-customer-io-which-is-better-in-2026/
- Intercom vs Drift 2026 (1mind successor): https://clonepartner.com/blog/intercom-vs-drift-2026-the-operations-leads-decision-matrix
- Pendo Resource Center: https://www.pendo.io/products/in-app-guidance/
- Customer.io API docs: https://customer.io/docs/api/
- Stackmatix PLG messaging: https://www.stackmatix.com/blog/plg-onboarding-activation
- 1mind (Drift successor, March 2026 launch): https://1mind.com/
