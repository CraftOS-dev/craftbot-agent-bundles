<!--
Source: https://developers.klaviyo.com/en/docs/klaviyo_mcp_server
Klaviyo MCP: official, GA Feb 2026
-->
# Klaviyo Email Lifecycle — SKILL

Klaviyo's official MCP server (`@klaviyo/mcp-server`) implements the e-commerce lifecycle workflow as MCP tools: segments, flows (welcome / nurture / reactivation / win-back / review / referral), campaigns, and the all-important `get_campaign_metrics` for post-Apple-MPP measurement (CTR / CTOR / conversion / revenue).

## When to use this skill

- **E-commerce or DTC brand** with Shopify, BigCommerce, or WooCommerce backend (Klaviyo's strongest integration).
- **Lifecycle automation** — welcome series, browse-abandonment, cart-abandonment, post-purchase, win-back.
- **Segmentation-first email strategy** — Klaviyo's segment engine is best-in-class.
- **Revenue-attributed reporting** — Klaviyo's revenue-per-recipient is the cleanest e-com email metric.
- **Post-MPP measurement** — `get_campaign_metrics` returns clicks, CTR, CTOR, complaint rate, revenue.

**Do NOT use this skill when:**
- **B2B email automation** with deal-stage triggers → use HubSpot remote MCP (see `hubspot-crm-marketing-mcp` skill).
- **Transactional-only** (receipts, password resets) → use Resend MCP.
- **Newsletter-style broadcast with no segmentation** → still allowed, but the agent should push back per the segmentation-over-broadcast rule.

## Setup

### Install

```bash
# Klaviyo official MCP server (Feb 2026 GA)
npx -y @klaviyo/mcp-server@latest
```

### Auth — Private API Key

Generate at https://www.klaviyo.com/account#api-keys-tab:

```bash
export KLAVIYO_API_KEY="pk_<your_key>"
# Optional company name for multi-account
export KLAVIYO_COMPANY="<company-id>"
```

Scopes needed:
- `lists:read`, `lists:write`
- `segments:read`, `segments:write`
- `flows:read`, `flows:write`
- `campaigns:read`, `campaigns:write`
- `events:read`
- `profiles:read`, `profiles:write`
- `templates:read`, `templates:write`
- `metrics:read`

### MCP tools available

- `create_segment` / `list_segments` / `update_segment`
- `create_flow` / `list_flows` / `update_flow_status`
- `create_campaign` / `send_campaign` / `get_campaign_metrics`
- `create_template` / `update_template`
- `list_profiles` / `update_profile` / `bulk_subscribe`
- `track_event` (server-side event)
- `sync_list` (CRM → Klaviyo list sync)

## Common recipes

### Recipe 1: Welcome series (4 emails, 14 days)

```bash
# Step 1 — segment: new subscribers, no orders yet, language=EN
mcp tool klaviyo.create_segment \
  --name "Welcome Series — New EN Subscribers" \
  --definition '{
    "type": "and",
    "conditions": [
      {"type":"is","property":"Email Marketing Consent","value":"Subscribed"},
      {"type":"has not","metric":"Placed Order"},
      {"type":"equals","property":"Language","value":"EN"}
    ]
  }'

# Step 2 — flow: 4 emails, 14 days, exit on order
mcp tool klaviyo.create_flow \
  --name "Welcome Series — EN" \
  --trigger '{"type":"list_added","listId":"<welcome-list-id>"}' \
  --steps '[
    {"type":"email","delay":"0h","templateId":"<welcome-1>","subjectAB":[{"id":"a","text":"Welcome — here is what you get"},{"id":"b","text":"You are in. Let me orient you."}]},
    {"type":"email","delay":"72h","templateId":"<welcome-2>","subjectAB":[{"id":"a","text":"Three tips for your first week"}]},
    {"type":"email","delay":"168h","templateId":"<welcome-3>","subjectAB":[{"id":"a","text":"What our top customers do (and you can too)"}]},
    {"type":"email","delay":"336h","templateId":"<welcome-4>","subjectAB":[{"id":"a","text":"Your offer expires soon"}]}
  ]' \
  --exitConditions '["Placed Order","Unsubscribed","Bounced (hard)","Spam Complained"]'
```

### Recipe 2: Abandoned cart (3 emails, 24h / 24h / 48h)

```bash
mcp tool klaviyo.create_flow \
  --name "Abandoned Cart — EN" \
  --trigger '{"type":"metric","metric":"Started Checkout"}' \
  --filter '{"type":"and","conditions":[{"type":"has not","metric":"Placed Order","since":"trigger"}]}' \
  --steps '[
    {"type":"email","delay":"1h","templateId":"<cart-1>","subjectAB":[{"text":"Did you forget something?"}]},
    {"type":"email","delay":"24h","templateId":"<cart-2>","subjectAB":[{"text":"Save 10% — your cart is waiting"}]},
    {"type":"email","delay":"72h","templateId":"<cart-3>","subjectAB":[{"text":"Last chance on your cart"}]}
  ]' \
  --exitConditions '["Placed Order","Unsubscribed"]'
```

### Recipe 3: Win-back (cool-down → win-back → suppress)

```bash
mcp tool klaviyo.create_segment \
  --name "At-Risk — No engagement 90d" \
  --definition '{
    "type":"and",
    "conditions":[
      {"type":"has not","metric":"Clicked Email","since":"90d"},
      {"type":"has","metric":"Placed Order","since":"365d"}
    ]
  }'

mcp tool klaviyo.create_flow \
  --name "Win-back" \
  --trigger '{"type":"segment_entered","segmentId":"<at-risk-id>"}' \
  --steps '[
    {"type":"email","delay":"0h","templateId":"<winback-1>","subjectAB":[{"text":"We miss you"}]},
    {"type":"email","delay":"168h","templateId":"<winback-2>","subjectAB":[{"text":"Final offer: 20% off"}]},
    {"type":"action","delay":"336h","action":"suppress","reason":"Inactive 90d, no winback engagement"}
  ]' \
  --exitConditions '["Clicked Email","Placed Order","Unsubscribed"]'
```

### Recipe 4: Review request (7-30 days post-order)

```bash
mcp tool klaviyo.create_flow \
  --name "Review Request" \
  --trigger '{"type":"metric","metric":"Fulfilled Order"}' \
  --steps '[
    {"type":"email","delay":"168h","templateId":"<review-1>","subjectAB":[{"text":"How is your <product>?"}]},
    {"type":"email","delay":"504h","templateId":"<review-2>","subjectAB":[{"text":"Quick favor: review?"}]}
  ]' \
  --exitConditions '["Submitted Review","Unsubscribed"]'
```

### Recipe 5: Post-Apple-MPP measurement — `get_campaign_metrics`

This is the CRITICAL function. Open rates are inflated 40-60% by Apple Mail pre-fetch. Use:

```bash
mcp tool klaviyo.get_campaign_metrics \
  --campaignId "<cid>" \
  --metrics '["clicked","ctr","ctor","unsubscribed","unsubscribe_rate","spam_complaint","spam_complaint_rate","revenue","revenue_per_recipient"]'
```

Returns:

```json
{
  "campaign_id": "<cid>",
  "clicked": 312,
  "ctr": 0.0421,             // clicks / sends
  "ctor": 0.1853,            // clicks / opens — engagement among engaged
  "unsubscribed": 4,
  "unsubscribe_rate": 0.00054,
  "spam_complaint": 1,
  "spam_complaint_rate": 0.00013,  // MUST be < 0.0010 (0.10%)
  "revenue": 4231.50,
  "revenue_per_recipient": 0.571
}
```

Alert rules (in agent's monitoring layer):
- `spam_complaint_rate > 0.0010` → immediate flag
- `ctr < 0.01` → flag for re-targeting / subject A/B refresh
- `unsubscribe_rate > 0.005` → flag content / cadence mismatch

### Recipe 6: Segment for B2B-style lead nurture in e-com context

```bash
mcp tool klaviyo.create_segment \
  --name "High-intent prospects — view + cart, no purchase 14d" \
  --definition '{
    "type":"and",
    "conditions":[
      {"type":"has","metric":"Viewed Product","count":">=3","since":"30d"},
      {"type":"has","metric":"Added to Cart","since":"30d"},
      {"type":"has not","metric":"Placed Order","since":"14d"}
    ]
  }'
```

### Recipe 7: CRM-ESP sync from HubSpot list

```bash
# HubSpot exports list → Klaviyo imports
mcp tool klaviyo.sync_list \
  --source "hubspot" \
  --sourceListId "<hubspot-list-id>" \
  --klaviyoListId "<klaviyo-list-id>" \
  --schedule "hourly"
```

### Recipe 8: Multi-language welcome series (with deepl-mcp)

```python
# Per-language Klaviyo template
languages = ['EN','BG','FR']
master_template = 'welcome-1-EN'

for lang in languages:
    if lang == 'EN':
        continue
    translated_html = deepl.translate(template_html, target_lang=lang)
    klaviyo.create_template(name=f'welcome-1-{lang}', html=translated_html)

# Router flow
klaviyo.create_flow(
    name='Welcome (multi-language)',
    trigger={'type':'list_added','listId':'<welcome-list>'},
    steps=[
        {'type':'branch','condition':{'property':'Language','equals':'BG'},'templateId':'welcome-1-BG'},
        {'type':'branch','condition':{'property':'Language','equals':'FR'},'templateId':'welcome-1-FR'},
        {'type':'branch','condition':{'default':True},'templateId':'welcome-1-EN'},
    ],
)
```

## Examples — full lifecycle map

For a typical DTC brand the agent will spin up:

| Sequence | Trigger | # emails | Exit |
|---|---|---|---|
| Welcome | list_added(newsletter) | 4 over 14d | Order / Unsub |
| Browse abandonment | Viewed Product, no order 24h | 2 over 48h | Order / Unsub |
| Cart abandonment | Started Checkout, no order 1h | 3 over 72h | Order / Unsub |
| Post-purchase #1 | Fulfilled Order | 2 over 7d | Order #2 |
| Review request | Fulfilled Order + 7d | 2 over 21d | Submitted Review / Unsub |
| Replenishment | Days since last order > avg cycle | 1 | New order |
| Win-back (at-risk) | No clicks 90d, has prior order | 2 over 14d | Click / Order |
| Sunset / suppress | Inactive 180d + no winback engage | 1 + suppress | n/a |

## Edge cases

### Apple MPP open inflation
Klaviyo's `opened_rate` metric still reports inflated open rate. **Never** use it as primary KPI. The agent treats opens as directional only; CTR / CTOR / revenue are gospel.

### Subject A/B testing
Klaviyo runs A/B on 25% of segment by default, picks winner by `ctr` after 4 hours. Override winner metric to `placed_order` for transactional flows:

```bash
mcp tool klaviyo.create_campaign \
  --abTest '{"variants":[{"subject":"A"},{"subject":"B"}],"winnerMetric":"placed_order","testWindowHours":4}'
```

### Compliance — consent, unsub, footer
- Klaviyo enforces consent (Email Marketing Consent field) — flows do NOT send to non-consented profiles.
- One-click unsubscribe (RFC 8058) auto-included.
- Footer with sender physical address required for CAN-SPAM; Klaviyo enforces in template editor.

### Deliverability — Klaviyo + dedicated IPs
- Default shared IPs sufficient < 100K sends/mo.
- Dedicated IP at $250/mo+ — only if list quality is proven (complaint < 0.05%).
- Warm-up over 4 weeks (Klaviyo provides warm-up flow).

### List hygiene
- Hard bounces auto-suppress.
- Soft bounces suppressed after 5 consecutive.
- Inactive 180d → manual suppress via sunset flow.
- Run quarterly: `list_profiles(filter='last_open_or_click > 365d')` → suppress.

### Revenue attribution
Klaviyo's revenue attribution window default: 5 days after click. For longer sales cycles, set per-flow:

```bash
mcp tool klaviyo.update_flow \
  --id "<flow-id>" \
  --revenueAttributionWindowDays 14
```

## Sources

- **Klaviyo MCP docs**: https://developers.klaviyo.com/en/docs/klaviyo_mcp_server
- **Klaviyo API reference**: https://developers.klaviyo.com/en/reference
- **Apple MPP impact**: https://help.klaviyo.com/hc/en-us/articles/4406874740379
- **Deliverability**: https://help.klaviyo.com/hc/en-us/categories/115001541352-Deliverability
