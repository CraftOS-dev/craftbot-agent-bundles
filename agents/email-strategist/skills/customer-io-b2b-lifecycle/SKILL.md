<!--
Source: https://customer.io/docs/api/
Event-driven B2B / product-led lifecycle. Companion to Klaviyo (e-com).
Deeper than marketing-agent's coverage: liquid templating, multi-workspace,
Data Pipelines for activation events, smart send time, broadcasts vs campaigns.
-->
# Customer.io B2B Lifecycle — SKILL

Event-driven B2B + product-led lifecycle: campaigns triggered by activation events from your product warehouse (PostHog / Mixpanel / Segment), transactional sends, broadcasts, and smart send time. Customer.io is the SOTA when "user did X in product, send Y" is the spine of your nurture.

## When to use

- "Trigger onboarding sequence when user invites first teammate"
- "Send dunning when Stripe `invoice.payment_failed` fires"
- "Broadcast monthly product changelog to active workspace owners"
- "Move profiles between segments based on Mixpanel activation events"
- "Build B2B trial-to-paid sequence keyed to feature-adoption milestones"
- "Send transactional + marketing on different message streams from one ESP"

Do **not** use for: pure e-commerce / DTC lifecycle (use Klaviyo skill); creator-economy newsletter (Beehiiv skill); transactional-only with React Email (Resend/Postmark skill).

## Setup

```bash
# Customer.io has three APIs:
#   Track API   — events / people / devices (write)
#   App API     — campaigns / segments / broadcasts / transactional (admin)
#   Data Pipelines — Segment-style CDP integration (Sources / Destinations)

# No first-party MCP yet (June 2026); call REST directly via cli-anything.
```

Auth:

```bash
export CIO_SITE_ID="<your_site_id>"                 # https://fly.customer.io/settings/api_credentials
export CIO_TRACK_API_KEY="<basic_auth_password>"
export CIO_APP_API_KEY="Bearer <your_app_api_key>"  # different scope from Track API
export CIO_REGION="us"                              # or "eu" — region-pinned URLs
```

Region-pinned base URLs (CRITICAL — wrong region returns 401):
- US: `https://track.customer.io/api/v1/`, `https://api.customer.io/v1/`
- EU: `https://track-eu.customer.io/api/v1/`, `https://api-eu.customer.io/v1/`

## Common recipes

### Recipe 1: Identify person + attributes

```bash
curl -X PUT "https://track.customer.io/api/v1/customers/$USER_ID" \
  -u "$CIO_SITE_ID:$CIO_TRACK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "created_at": 1717948800,
    "plan": "pro",
    "company_id": "comp_42",
    "lifecycle_stage": "trial",
    "trial_ends_at": 1718553600
  }'
```

### Recipe 2: Track activation event (triggers onboarding campaign)

```bash
curl -X POST "https://track.customer.io/api/v1/customers/$USER_ID/events" \
  -u "$CIO_SITE_ID:$CIO_TRACK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "team_member_invited",
    "data": {
      "team_id": "team_42",
      "invitee_count": 1,
      "plan": "pro"
    }
  }'
```

### Recipe 3: Build event-triggered onboarding campaign (App API)

```bash
curl -X POST "https://api.customer.io/v1/campaigns" \
  -H "Authorization: $CIO_APP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Onboarding — Trial",
    "type": "triggered",
    "trigger": {
      "type": "event",
      "event_name": "user_signed_up",
      "filter": {"and": [
        {"event": {"data.plan": {"eq": "trial"}}}
      ]}
    },
    "actions": [
      {"type":"email","delay_seconds":0,
       "template_id":"<welcome>","subject":"Welcome, {{customer.first_name}}"},
      {"type":"branch",
       "condition":{"customer":{"feature_first_used":{"exists":true}}},
       "true_actions":[{"type":"exit"}],
       "false_actions":[
         {"type":"email","delay_seconds":172800,
          "template_id":"<nudge1>","subject":"Need help getting started?"}
       ]}
    ],
    "exit_conditions":["plan != trial","unsubscribed"]
  }'
```

### Recipe 4: Liquid templating with conditional content

Customer.io uses Liquid for templates. Powerful conditional logic:

```liquid
<!-- email body -->
Hi {{ customer.first_name | default: "there" }},

{% if customer.plan == "trial" %}
Your trial ends in {{ customer.trial_days_left }} days.
{% elsif customer.plan == "pro" %}
You are on the Pro plan — here is your March usage:
- {{ customer.api_calls_this_month | number_with_delimiter }} API calls
- {{ customer.seats_used }}/{{ customer.seat_limit }} seats
{% endif %}

{% if customer.last_login_at < "now" | date: "%s" | minus: 604800 %}
We noticed you haven't logged in for a week.
{% endif %}
```

### Recipe 5: Transactional message stream (separate from marketing)

Customer.io has two message-types: **Transactional** (no consent required, no unsubscribe, high deliverability priority) and **Marketing** (consented, unsubscribe required, queued).

```bash
# Send transactional via API
curl -X POST "https://api.customer.io/v1/send/email" \
  -H "Authorization: $CIO_APP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "transactional_message_id": "<tx-msg-id>",
    "to": "user@example.com",
    "identifiers": {"id":"user_42"},
    "message_data": {
      "order_id": "ord_91",
      "items": [{"sku":"abc","name":"Widget","qty":1}]
    }
  }'
```

### Recipe 6: Broadcast — one-time to a segment

For non-recurring sends (product launch, newsletter):

```bash
curl -X POST "https://api.customer.io/v1/broadcasts" \
  -H "Authorization: $CIO_APP_API_KEY" \
  -d '{
    "name":"April product launch",
    "segment_id":"<active-workspace-owners>",
    "actions":[{"type":"email","template_id":"<launch-template>","subject":"New: AI Composer"}],
    "send_at": 1719417600
  }'
```

### Recipe 7: Segment by behavioral cohort

```bash
curl -X POST "https://api.customer.io/v1/segments" \
  -H "Authorization: $CIO_APP_API_KEY" \
  -d '{
    "name": "Power users — last 30d",
    "type": "data-driven",
    "conditions": {
      "and": [
        {"event":{"name":"feature_used","performed":{"count":">=20","within":"30d"}}},
        {"attribute":{"plan":{"in":["pro","enterprise"]}}},
        {"event":{"name":"unsubscribed","performed":{"count":"=0"}}}
      ]
    }
  }'
```

### Recipe 8: Smart Send Time

Customer.io's Send-time optimization analyzes per-recipient open/click history:

```bash
# Enable on campaign action
curl -X PATCH "https://api.customer.io/v1/campaigns/<id>/actions/<action-id>" \
  -H "Authorization: $CIO_APP_API_KEY" \
  -d '{"send_time_optimization": true, "fallback_send_time": "10:00", "fallback_timezone": "customer"}'
```

### Recipe 9: Multi-workspace (B2B reseller pattern)

For agencies / multi-tenant SaaS, one Customer.io workspace per client:

```bash
# Workspace creation requires Customer.io support — list workspaces:
curl "https://api.customer.io/v1/workspaces" -H "Authorization: $CIO_APP_API_KEY"

# Per workspace, separate Site ID + Track API key. Set in env per-job.
```

### Recipe 10: Data Pipelines — Segment-style sources

Customer.io Data Pipelines = embedded CDP. Set up Source from your product app, transformations, and Destinations (warehouse, analytics):

```bash
curl -X POST "https://cdp.customer.io/v1/sources" \
  -H "Authorization: $CIO_APP_API_KEY" \
  -d '{
    "name":"app-prod",
    "type":"http",
    "settings":{"webhookUrl":"https://cdp.customer.io/v1/p/app-prod"}
  }'
```

Then send events:

```bash
curl -X POST "https://cdp.customer.io/v1/p/app-prod" \
  -H "Authorization: Basic $(echo -n $CIO_WRITE_KEY: | base64)" \
  -d '{
    "userId":"user_42",
    "event":"team_member_invited",
    "properties":{"team_id":"team_42"}
  }'
```

## Examples

### Example 1: Trial-to-paid conversion sequence

**Goal:** for SaaS trial users, drive activation → conversion.

**Steps:**

1. Identify user on signup (Recipe 1), set `lifecycle_stage=trial`, `trial_ends_at`.
2. Track activation events as user hits milestones (Recipe 2):
   - `feature_first_used` → triggers value-realization email
   - `team_member_invited` → triggers collaboration nudge
   - `integration_connected` → triggers power-user content
3. Build campaign with conditional branches based on which activation events fired (Recipe 3). Skip nudges if user already activated.
4. At `trial_ends_at - 3d`, trigger upgrade campaign with usage stats (Recipe 4).
5. After trial ends, branch:
   - Converted → onboarding-paid sequence
   - Did not convert → win-back sequence (7d, 14d, 30d cadence)

**Result:** segmentation-aware trial sequence that skips redundant nudges and accelerates conversion.

### Example 2: Stripe dunning via webhook → campaign

**Goal:** when Stripe says payment failed, send escalating dunning.

**Steps:**

1. Stripe webhook → your backend → identify customer in Customer.io with `payment_status=failed`:
   ```bash
   curl -X PUT "https://track.customer.io/api/v1/customers/$USER_ID" \
     -u "$CIO_SITE_ID:$CIO_TRACK_API_KEY" \
     -d '{"payment_status":"failed","last_failure_at":1717948800}'
   ```
2. Track event `payment_failed` (Recipe 2).
3. Campaign triggers off `payment_failed` event with 3-email cadence (1h, 24h, 72h).
4. Exit condition: `payment_status == "succeeded"`.

## Edge cases

- **Region pinning** — US workspace + EU URL = 401. Always confirm region via `Settings → Workspace`.
- **Liquid timezone defaults to UTC** — wrap dates with `| date: "%B %-d, %Y", customer.timezone` to render in customer's local TZ.
- **Track API basic auth + App API bearer** — these are DIFFERENT keys with different scopes. Don't mix.
- **Transactional vs Marketing send classification** — transactional messages **bypass consent and unsubscribe** by design. Misclassifying a marketing message as transactional will get your domain blocked. ESP enforcement caught hundreds of senders in 2024-2025.
- **Segment recompute lag** — data-driven segments recompute on a schedule (every 15-60 min depending on size). Don't trigger flows expecting instant segment membership.
- **Customer.io drops events for unknown users** — if `customers/$ID/events` is called for an ID that hasn't been `PUT` first, the event is silently dropped (unless `accept_unknown_users: true` is on at workspace level).
- **Rate limits** — Track API: 100 req/s per workspace. App API: 60 req/min for write endpoints. Use exponential backoff on 429.
- **Liquid does NOT have full Shopify Liquid filter set** — `where`, `group_by` are absent. Pre-compute in your backend.

## Sources

- [Customer.io API docs](https://customer.io/docs/api/)
- [Track API reference](https://customer.io/docs/api/track/)
- [App API reference](https://customer.io/docs/api/app/)
- [Liquid templating](https://customer.io/docs/journeys/liquid-tag-list/)
- [Send-time optimization](https://customer.io/docs/journeys/send-time-optimization)
- [Data Pipelines](https://customer.io/docs/cdp/sources/)
- [Transactional vs Marketing](https://customer.io/docs/journeys/message-types/)
