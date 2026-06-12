<!--
Named-flow templates + throttling + exit conditions.
Welcome / Browse / Cart / Post-purchase / Win-back / Sunset / Nurture.
-->
# Klaviyo / Customer.io Flow Design Patterns — SKILL

Named-flow templates with documented structure: welcome (4-5 / 14d), browse abandonment (2 / 48h), cart abandonment (3 / 72h), post-purchase (3-5 / 60d), win-back (2-3 / 14-21d), sunset (1 / suppress), B2B onboarding (event-triggered). Each pattern includes throttling, exit conditions, smart send time, metric targets.

## When to use

- "Design our welcome flow"
- "Build cart abandonment sequence"
- "Standard post-purchase template"
- "B2B trial-to-paid sequence"
- "Reactivation sequence — what's standard"
- "Audit our existing flow against best practices"

## Setup

No new tools — uses Klaviyo MCP / Customer.io API.

## Common recipes

### Recipe 1: Welcome flow template (e-com, 4 emails, 14 days)

```json
{
  "name": "Welcome — EN",
  "trigger": {"type": "list_subscribed", "list_id": "<newsletter>"},
  "audience_filter": {"language": "en", "consent": "subscribed"},
  "steps": [
    {"type": "email", "delay_seconds": 0,
     "template_id": "<welcome-1-intro>",
     "subject": "Welcome — here is what to expect",
     "smart_send_time": true},
    {"type": "email", "delay_seconds": 259200,
     "template_id": "<welcome-2-brand-story>",
     "subject": "Why we built Brand"},
    {"type": "conditional_split",
     "condition": "Has placed order? Has clicked any email?",
     "yes_branch": "engaged_path",
     "no_branch": "nudge_path"},
    {"id": "nudge_path", "type": "email", "delay_seconds": 604800,
     "template_id": "<welcome-3-popular>",
     "subject": "Our most-loved products"},
    {"id": "engaged_path", "type": "email", "delay_seconds": 604800,
     "template_id": "<welcome-3-personalized>",
     "subject": "Based on what you liked"},
    {"type": "email", "delay_seconds": 604800,
     "template_id": "<welcome-4-offer>",
     "subject": "A welcome gift: 10% off your first order"}
  ],
  "exit_conditions": ["Placed Order", "Unsubscribed", "Bounced (hard)", "Spam Complained"],
  "throttle": {"max_emails_per_recipient_per_day": 1}
}
```

Metric targets:
- CTR > 5% (welcome high-intent)
- Conversion rate > 1% (driving to first order)
- Unsubscribe rate < 1%
- Complaint rate < 0.05%

### Recipe 2: Browse abandonment (2 emails, 48 hours)

```bash
curl -X POST "https://a.klaviyo.com/api/flows" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"flow","attributes":{
    "name":"Browse Abandonment — EN",
    "trigger":{"type":"metric","metric_name":"Viewed Product"},
    "filters":[
      {"type":"profile-property","property":"language","equals":"en"},
      {"type":"not","filter":{"type":"metric","name":"Placed Order","since":"now-72h"}},
      {"type":"not","filter":{"type":"metric","name":"Started Checkout","since":"now-72h"}}
    ],
    "steps":[
      {"type":"email","delay_seconds":3600,
       "template_id":"<browse-1>",
       "subject_variants":[{"text":"Still thinking about {{ event.product_name }}?"}]},
      {"type":"email","delay_seconds":86400,
       "template_id":"<browse-2-related>",
       "subject_variants":[{"text":"You might also like..."}]}
    ],
    "exit_conditions":["Placed Order","Unsubscribed"]
  }}}'
```

### Recipe 3: Cart abandonment (3 emails, 72 hours)

```json
{
  "name": "Cart Abandonment — EN",
  "trigger": {"type": "metric", "metric_name": "Started Checkout"},
  "filters": [
    {"language": "en"},
    {"not": {"Placed Order since trigger": true}}
  ],
  "steps": [
    {"type": "email", "delay_seconds": 3600,
     "template_id": "<cart-1-reminder>",
     "subject": "You forgot something",
     "content": "Hi {{ first_name }}, your cart is waiting. {{ cart.item_count }} items, ${{ cart.total }}."},
    {"type": "conditional_split",
     "condition": "Predicted churn risk = high?",
     "yes_branch": "vip_discount",
     "no_branch": "regular_discount"},
    {"id": "regular_discount", "type": "email", "delay_seconds": 86400,
     "template_id": "<cart-2-10pct>",
     "subject": "Save 10% on your order"},
    {"id": "vip_discount", "type": "email", "delay_seconds": 86400,
     "template_id": "<cart-2-15pct>",
     "subject": "We saved you 15%"},
    {"type": "email", "delay_seconds": 172800,
     "template_id": "<cart-3-scarcity>",
     "subject": "Last chance — your cart expires soon"}
  ],
  "exit_conditions": ["Placed Order", "Unsubscribed"]
}
```

### Recipe 4: Post-purchase (5 emails, 60 days)

```json
{
  "name": "Post-Purchase — Physical Goods",
  "trigger": {"type": "metric", "metric_name": "Placed Order"},
  "steps": [
    {"type": "email", "delay_seconds": 0,
     "template_id": "<thank-you>",
     "subject": "Thanks for your order, {{ first_name }}!"},
    {"type": "email", "delay_seconds": 86400,
     "template_id": "<shipping-update>",
     "subject": "Your order is on its way"},
    {"type": "wait_for_event", "event": "Order Delivered", "timeout_days": 14},
    {"type": "email", "delay_seconds": 604800,
     "template_id": "<usage-tips>",
     "subject": "Get the most out of {{ product_category }}"},
    {"type": "email", "delay_seconds": 1209600,
     "template_id": "<review-request>",
     "subject": "How is your {{ product_name }}? Share a review"},
    {"type": "conditional_split",
     "condition": "Product category = consumable?",
     "yes_branch": "replenish",
     "no_branch": "upsell"},
    {"id": "replenish", "type": "email", "delay_seconds": 3024000,
     "template_id": "<replenishment>",
     "subject": "Time to restock?"},
    {"id": "upsell", "type": "email", "delay_seconds": 3024000,
     "template_id": "<upsell>",
     "subject": "Complete your collection"}
  ]
}
```

### Recipe 5: Win-back (3 emails, 21 days)

```json
{
  "name": "Win-back — At-risk (RFM)",
  "trigger": {"type": "segment_entered", "segment_id": "<at-risk-segment>"},
  "trigger_segment_definition": "Engaged-30d declined to dormant; has prior order",
  "steps": [
    {"type": "email", "delay_seconds": 0,
     "template_id": "<winback-1-miss-you>",
     "subject": "We miss you"},
    {"type": "conditional_split",
     "condition": "Clicked since step 1?",
     "yes_branch": "exit",
     "no_branch": "continue"},
    {"type": "email", "delay_seconds": 604800,
     "template_id": "<winback-2-offer>",
     "subject": "Come back with 20% off"},
    {"type": "conditional_split",
     "condition": "Clicked since step 2?",
     "yes_branch": "exit",
     "no_branch": "continue"},
    {"type": "email", "delay_seconds": 1209600,
     "template_id": "<winback-3-final>",
     "subject": "Last chance — should we stop emailing?"},
    {"type": "action", "delay_seconds": 604800,
     "action": "suppress",
     "reason": "No win-back engagement after 3 emails"}
  ],
  "exit_conditions": ["Clicked Email", "Placed Order", "Unsubscribed"]
}
```

### Recipe 6: B2B onboarding (event-triggered, Customer.io)

```bash
curl -X POST "https://api.customer.io/v1/campaigns" \
  -H "Authorization: $CIO_APP_API_KEY" \
  -d '{
    "name": "Trial onboarding",
    "type": "triggered",
    "trigger": {"type":"event","event_name":"user_signed_up","filter":{"customer":{"plan":{"eq":"trial"}}}},
    "actions": [
      {"type":"email","delay_seconds":0,"template_id":"<welcome>",
       "subject":"Welcome to Brand, {{customer.first_name}}"},
      {"type":"wait","duration":86400},
      {"type":"branch",
       "condition":{"customer":{"feature_first_used":{"exists":true}}},
       "true":[{"type":"exit"}],
       "false":[
         {"type":"email","template_id":"<nudge-feature>",
          "subject":"Lets get you started — 3 quick steps"}
       ]},
      {"type":"wait","duration":172800},
      {"type":"branch",
       "condition":{"customer":{"team_member_invited":{"exists":true}}},
       "true":[{"type":"email","template_id":"<team-feature>"}],
       "false":[{"type":"email","template_id":"<collab-nudge>"}]},
      {"type":"wait","duration":604800},
      {"type":"email","template_id":"<midway-checkin>",
       "subject":"How is the trial going?"},
      {"type":"branch",
       "condition":{"customer":{"trial_ends_at":{"in_next":"3d"}}},
       "true":[{"type":"email","template_id":"<upgrade-now>","subject":"3 days left — upgrade"}],
       "false":[]}
    ],
    "exit_conditions":[
      {"customer":{"plan":{"in":["pro","enterprise"]}}},
      {"customer":{"unsubscribed":{"eq":true}}}
    ]
  }'
```

### Recipe 7: Throttling rules

Per-flow:

```bash
curl -X PATCH "https://a.klaviyo.com/api/flows/<flow-id>" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"flow","attributes":{
    "throttling":{
      "max_send_rate_per_hour": 5000,
      "max_emails_per_recipient_per_day": 1,
      "max_emails_per_recipient_per_week": 4
    }
  }}}'
```

Global account-level send velocity (for IP warming):

```bash
# Klaviyo sending throttle (Plus/Advanced)
curl -X PUT "https://a.klaviyo.com/api/sending-options" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"sending-options","attributes":{"max_send_rate_per_minute":100}}}'
```

### Recipe 8: Universal exit conditions (always)

Every flow should include:

```json
"exit_conditions": [
  "Placed Order",       // primary goal achieved
  "Unsubscribed",       // explicit user request
  "Bounced (hard)",     // address invalid
  "Spam Complained",    // user marked spam — immediate exit
  "Sunset Tag Added"    // engagement-tier downgrade
]
```

### Recipe 9: Smart send time per step

```bash
# Enable Smart Send Time on each email step (not flow-level)
for STEP_ID in <step-1> <step-2> <step-3>; do
  curl -X PATCH "https://a.klaviyo.com/api/flow-actions/$STEP_ID" \
    -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
    -d '{"data":{"type":"flow-action","attributes":{"smart_send_time":true}}}'
done
```

### Recipe 10: Flow audit checklist

```markdown
# Flow Audit — <flow-name>

## Trigger
- [ ] Trigger event well-defined (specific metric, not "any event")
- [ ] Audience filter present (engagement tier? language? lifecycle stage?)
- [ ] Initial delay calibrated to user expectation

## Steps
- [ ] Each step has clear purpose (don't have filler emails)
- [ ] Subject lines vary in approach (not all 5 emails start with "Hey")
- [ ] CTAs clear and specific (not all "Learn more")
- [ ] Conditional branches reflect user intent (e.g., engaged vs not)

## Exit conditions
- [ ] Primary goal (e.g., purchase, click) exits flow
- [ ] Unsubscribe exits flow
- [ ] Hard bounce exits flow
- [ ] Spam complaint exits flow
- [ ] Engagement-tier downgrade exits flow (sunset)

## Throttling
- [ ] Max emails per recipient per day ≤ 1 (or business-justified > 1)
- [ ] Max emails per recipient per week ≤ 4
- [ ] Global send-rate cap respects warmup state

## Smart Send Time
- [ ] Enabled on individual steps where engagement matters
- [ ] Fallback time set for profiles with insufficient history

## Tracking
- [ ] UTM parameters set
- [ ] Revenue attribution window appropriate (5d default, 14d for high-LTV)
- [ ] Conversion metric defined

## Compliance
- [ ] Marketing consent verified at entry
- [ ] One-click unsubscribe header present
- [ ] Physical address in footer
- [ ] Per-jurisdiction handling (GDPR for EU profiles)
```

### Recipe 11: Replenishment flow (consumables only)

Pre-condition: Klaviyo Predictive AI provides `expected_date_of_next_order` per profile.

```json
{
  "name": "Replenishment — predicted next order in 7 days",
  "trigger": {
    "type": "predictive_property_threshold",
    "property": "expected_date_of_next_order",
    "comparison": "within",
    "value": "7d"
  },
  "filter": {
    "product_category": "consumable",
    "purchases_total": ">= 2"
  },
  "steps": [
    {"type": "email", "delay_seconds": 0,
     "template_id": "<replenish-1>",
     "subject": "Time to restock?"}
  ],
  "exit_conditions": ["Placed Order"]
}
```

### Recipe 12: Birthday / anniversary flow

```json
{
  "name": "Birthday — annual recurring",
  "trigger": {
    "type": "date_property",
    "property": "birthday",
    "timing": "annually"
  },
  "steps": [
    {"type": "email", "delay_seconds": 0,
     "template_id": "<birthday>",
     "subject": "Happy birthday, {{ first_name }} — here is a gift"}
  ]
}
```

## Examples

### Example 1: Build complete e-com lifecycle (8 named flows)

**Goal:** new DTC brand needs full lifecycle automation.

**Steps:**

1. Inventory required flows: Welcome, Browse, Cart, Post-purchase, Review, Win-back, Sunset, Birthday.
2. Implement each from named templates (Recipes 1-7, 10-12).
3. Set throttling globally + per-flow (Recipe 7).
4. Enable Smart Send Time on critical steps (Recipe 9).
5. Define metric targets per flow (Recipe 1).
6. Audit using checklist (Recipe 10).
7. After 30 days, pull metrics; iterate the underperformers.

### Example 2: B2B SaaS onboarding flow

**Goal:** trial users → activated → paid.

**Steps:**

1. Identify activation events (feature_first_used, team_invited, etc.) — use posthog-mcp.
2. Build Customer.io campaign (Recipe 6).
3. Branch on which events fired by midway-check.
4. Pre-renewal nudge at trial_ends_at - 3d.
5. Post-trial: branch to onboarding-paid OR win-back.

## Edge cases

- **Don't combine browse + cart triggers in one flow** — too noisy. Separate flows.
- **Welcome flow length** — 4-5 emails feels right. < 3 leaves money on table; > 7 fatigues new subscribers.
- **Smart Send Time + 0s delay** — Klaviyo respects Smart Send Time on first step only after some history; new profiles default to send-now.
- **Exit conditions are evaluated continuously**, not just at delay boundaries. A user who unsubscribes mid-flow exits the next step.
- **Conditional split branches must rejoin or terminate explicitly** — otherwise some profiles never exit.
- **Multi-language flows** — see `multi-language-esp-architecture-icu` skill. Use language as audience filter, not as conditional step.
- **Predictive properties take 30+ days** to populate; new profiles fall through replenishment trigger.
- **Don't run cart + browse simultaneously** — same user, contradictory signals. Cart > Browse priority; browse exits if cart triggers.
- **B2B nurture vs e-com lifecycle** — different timing (days vs hours). B2B can have 2-3 week gaps; e-com cart should be < 72h.

## Sources

- [Klaviyo flow templates](https://help.klaviyo.com/hc/en-us/articles/115002774932)
- [Klaviyo abandoned cart flow](https://help.klaviyo.com/hc/en-us/articles/360001070631)
- [Klaviyo welcome series](https://help.klaviyo.com/hc/en-us/articles/115004317991)
- [Klaviyo post-purchase flow](https://www.klaviyo.com/blog/post-purchase-email-flow)
- [Customer.io campaigns](https://customer.io/docs/journeys/campaigns/)
- [Customer.io triggered campaigns](https://customer.io/docs/journeys/triggered-campaigns/)
- [Smart Send Time (Klaviyo)](https://help.klaviyo.com/hc/en-us/articles/360050287831)
