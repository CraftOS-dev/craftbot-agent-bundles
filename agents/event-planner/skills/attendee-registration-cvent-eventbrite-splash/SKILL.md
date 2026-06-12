<!--
Sources:
- Cvent Event Management API: https://developers.cvent.com/
- Bizzabo Open API: https://developers.bizzabo.com/
- Splash REST API: https://api-docs.splashthat.com/
- Eventbrite API: https://www.eventbrite.com/platform/api
- RingCentral Events Developer (Hopin): https://hopin.com/developers
-->
# Attendee Registration (Cvent / Eventbrite / Splash / Bizzabo / Hopin) — SKILL

Pick the right platform → configure registration form → integrate payment + email confirmation → track funnel + drop-off → handoff to event app. Platform choice is irreversible mid-cycle, so the decision matrix matters.

## When to use this skill

- Standing up registration for a new event
- Migrating from one platform to another (free → paid, basic → enterprise)
- Adding paid registration tier (early bird / regular / late / VIP)
- Group / corporate registration codes
- Multi-event series (recurring conferences with attendee history)
- Reg-page funnel optimization (drop-off > 30%)

**Do NOT use this skill when:**
- Attendees are pre-registered via CRM (corporate internal events) → use `notion-mcp` directly
- Event is invite-only with hard whitelist → use `gmail-mcp` for invites + accept tracking
- Pure virtual webinar with single broadcast → use `live-streaming-restream-obs-streamyard`

## Setup

### Platform decision matrix

| Platform | Best for | Pricing | API tier |
|---|---|---|---|
| **Cvent** | Enterprise complex (full RFP + reg + agenda + sponsors + sessions) | $10K+/yr | Full |
| **Bizzabo / Klik** | Mid-market, mobile-first, NFC badges | $5K-$15K/yr | Full |
| **Splash** | Brand-led marketing events | $3K-$10K/yr | Mid |
| **Eventbrite** | Consumer / high-volume / paid public | Free + transaction fees | Full |
| **RingCentral Events (Hopin)** | Virtual / hybrid | $5K-$15K/yr | Full |
| **Whova** | Mobile-first community events | $1K-$5K/yr | Mid |
| **Lu.ma** | Small recurring meetups | Free / low | Mid |

### Auth

```bash
# Cvent
export CVENT_API_TOKEN="<oauth-token>"

# Bizzabo
export BIZZABO_TOKEN="<pat>"

# Splash
export SPLASH_API_KEY="<api-key>"

# Eventbrite
export EVENTBRITE_TOKEN="<oauth-token>"

# RingCentral Events (Hopin)
export HOPIN_TOKEN="<api-key>"
```

## Common recipes

### Recipe 1: Cvent — create event + registration

```bash
# 1. Create event
curl -X POST https://api-platform.cvent.com/v1/events \
  -H "Authorization: Bearer $CVENT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Q3 Customer Summit 2026",
    "code": "QCS26",
    "startDate": "2026-09-15T08:00:00Z",
    "endDate": "2026-09-17T18:00:00Z",
    "venueId": "<venue-id>",
    "registrationType": "tiered",
    "capacity": 500
  }'

# 2. Create registration types (tiers)
curl -X POST https://api-platform.cvent.com/v1/events/$EVENT_ID/registrationTypes \
  -d '{
    "name": "Early Bird",
    "fee": 599,
    "capacity": 200,
    "availableFrom": "2026-05-01T00:00:00Z",
    "availableTo": "2026-07-15T23:59:59Z"
  }'
curl -X POST ... -d '{"name": "Regular", "fee": 799, ...}'
curl -X POST ... -d '{"name": "VIP", "fee": 1499, ...}'

# 3. Create custom registration fields (dietary, company, role, etc)
curl -X POST https://api-platform.cvent.com/v1/events/$EVENT_ID/customFields \
  -d '{
    "name": "dietary_requirement",
    "type": "multi_select",
    "options": ["Standard","Vegan","GF","Halal","Kosher","Other"],
    "required": true
  }'

# 4. Get registration page URL
curl -X GET https://api-platform.cvent.com/v1/events/$EVENT_ID/registrationPage
# Returns the public reg URL
```

### Recipe 2: Bizzabo — create event + reg via Klik

```bash
curl -X POST https://api.bizzabo.com/v1/events \
  -H "Authorization: Bearer $BIZZABO_TOKEN" \
  -d '{
    "name": "Summit 2026",
    "startDate": "2026-09-15",
    "endDate": "2026-09-17",
    "registrationOpen": true,
    "klikEnabled": true,    // enables NFC SmartBadge
    "leadCaptureMode": "automatic"
  }'

# Add registration questions
curl -X POST https://api.bizzabo.com/v1/events/$EVENT_ID/questions \
  -d '{"text": "Dietary requirements", "type": "multi_select", "options": [...]}'
```

### Recipe 3: Splash — brand-led registration

```bash
# Create event with brand kit
curl -X POST https://api.splashthat.com/v1/events \
  -H "Authorization: Bearer $SPLASH_API_KEY" \
  -d '{
    "title": "Brand Launch Party",
    "description": "...",
    "date": "2026-08-20",
    "venue_name": "...",
    "brand_kit_id": "<bk-id>",
    "ticketing_enabled": true
  }'

# Upload custom CSS for branded look
curl -X PUT https://api.splashthat.com/v1/events/$EVENT_ID/theme \
  -d '{"css": "<branded-css>"}'

# Get RSVP / ticketing URL
curl -X GET https://api.splashthat.com/v1/events/$EVENT_ID
```

### Recipe 4: Eventbrite — consumer ticketing

```bash
# Create event
curl -X POST https://www.eventbriteapi.com/v3/events/ \
  -H "Authorization: Bearer $EVENTBRITE_TOKEN" \
  -d '{
    "event": {
      "name": {"html": "Public Conference 2026"},
      "start": {"utc": "2026-09-15T13:00:00Z", "timezone": "America/Chicago"},
      "end": {"utc": "2026-09-17T22:00:00Z", "timezone": "America/Chicago"},
      "currency": "USD",
      "online_event": false,
      "venue_id": "<venue-id>"
    }
  }'

# Create ticket classes
curl -X POST https://www.eventbriteapi.com/v3/events/$EVENT_ID/ticket_classes/ \
  -d '{
    "ticket_class": {
      "name": "General Admission",
      "cost": "USD,99,00",
      "quantity_total": 500
    }
  }'

# Publish
curl -X POST https://www.eventbriteapi.com/v3/events/$EVENT_ID/publish/
```

### Recipe 5: RingCentral Events (Hopin) — virtual / hybrid

```bash
# Create event
curl -X POST https://hopin.com/api/v1/events \
  -H "Authorization: Bearer $HOPIN_TOKEN" \
  -d '{
    "name": "Virtual Conference 2026",
    "start": "2026-09-15T14:00:00Z",
    "end": "2026-09-17T22:00:00Z",
    "ticket_types": [
      {"name": "Free", "price": 0, "quantity": 1000},
      {"name": "Premium", "price": 99, "quantity": 200}
    ],
    "stage_count": 3,
    "networking_enabled": true,
    "expo_enabled": true  // sponsor booths
  }'
```

### Recipe 6: Custom registration fields (best practices)

Standard fields to ALWAYS include:

```yaml
required_fields:
  - first_name
  - last_name
  - email (validated)
  - company
  - job_title

recommended_fields:
  - phone (for day-of contact)
  - linkedin_url (for networking)
  - dietary_requirement (multi-select)
  - food_allergies (free-text)
  - accessibility_accommodations (free-text)
  - interests (multi-select; drives matchmaking — see virtual-networking-brella-swapcard)
  - questions_for_speakers (free-text)
  - referral_source (drop-down: paid social, email, organic, peer, etc.)
  - photo_consent (checkbox)
  - terms_accepted (checkbox)
  - emergency_contact_name + phone (for VIP / multi-day events)
```

### Recipe 7: Group / corporate registration code

```bash
# Cvent: create promo / discount code
curl -X POST https://api-platform.cvent.com/v1/events/$EVENT_ID/discountCodes \
  -d '{
    "code": "TEAMABC10",
    "type": "percentage",
    "value": 10,
    "maxUses": 50,
    "appliesToTier": ["Early Bird", "Regular"]
  }'

# Eventbrite: same pattern
curl -X POST https://www.eventbriteapi.com/v3/events/$EVENT_ID/discounts/ \
  -d '{"discount": {"code": "TEAMABC10", "type": "code", "percent_off": "10"}}'
```

### Recipe 8: Confirmation email customization

Replace platform's default confirmation with branded version:

```bash
mcp tool gmail.send_email \
  --to "$attendee_email" \
  --subject "You're in! [Event Name] Sept 15-17, 2026" \
  --body "$(envsubst < confirmation_template.html)" \
  --attachments "calendar_invite.ics,event_pdf_guide.pdf"
```

Template should include:
- Calendar invite (`.ics` file)
- Hotel booking link (from `room-block-hotel-partnerships`)
- What to expect (agenda preview)
- Pre-event tasks (download event app, complete profile, etc.)
- Day-of contact info

### Recipe 9: Funnel tracking via PostHog

```python
# Embed PostHog on reg page
# In page header:
# posthog.init('<api-key>', { api_host: 'https://app.posthog.com' });

# Track key events:
# - registration_page_viewed
# - registration_form_started
# - registration_payment_started
# - registration_completed

# HogQL query for funnel:
"""
SELECT step_count, conversion_rate
FROM funnel(
  events = ['page_viewed', 'form_started', 'payment_started', 'completed']
  filter = event_id = '<event-id>'
  window = 7 day
)
"""
```

Drop-off > 30% at any step → optimize. Common fixes: reduce required fields, single-page form, social signup, embedded checkout.

### Recipe 10: Real-time check-in tracking (day-of)

```python
# Poll every 60 seconds for check-in queue depth
import time
while event_in_progress:
    metrics = cvent.get_event_metrics(EVENT_ID)
    if metrics['check_in_queue_depth'] > 50 OR metrics['avg_wait_time_seconds'] > 300:
        slack.send_message(
            channel='event-ops',
            text=f':rotating_light: Check-in queue depth: {metrics["check_in_queue_depth"]}, '
                 f'wait: {metrics["avg_wait_time_seconds"]/60:.1f}min'
        )
    time.sleep(60)
```

## Examples

### Example A: Mid-market conference, paid tickets, Cvent

- Cvent Event Management for full reg + check-in
- 3 tiers: Early Bird $599 / Regular $799 / VIP $1499
- Stripe payment integration via Cvent
- Confirmation email + 7-day reminder + 1-day reminder
- Day-of check-in via Cvent OnArrival kiosks

### Example B: Free consumer conference, Eventbrite

- Eventbrite for free registration + paid VIP tier
- Branded reg page (with logo + custom CSS)
- Multiple ticket types (general $0, premium $99)
- Wait-list automatically engaged when capacity reached
- Refund policy: 7-day before event, 50% refund

### Example C: Customer-only summit, invite-only, Notion + manual

- Notion DB of invited customers (synced from CRM)
- Email invite via `gmail-mcp` with unique RSVP token
- RSVP tracked in Notion (open/accepted/declined)
- No public reg page; recipient-pays for all attendance
- VIP arrival check-in (dedicated lobby station; no kiosk)

## Edge cases

### Refund policy
Define before launch: 30-day before = full refund, 7-day = 50%, <7-day = no refund. Apply per platform's refund engine.

### Capacity overflow
Wait-list automatically; promote when cancellation occurs. Communicate cap clearly on reg page to avoid frustration.

### Attendee privacy / GDPR
Reg form must include privacy policy + consent for marketing emails (separate from event comms). Comply with GDPR / CCPA for data residency.

### Duplicate registration
Use email as unique identifier. Detect duplicate; merge OR flag for manual review.

### Payment failures
Retry payment 24 hours later; if still fails, hold reg in "Payment Pending" state for 72 hours then cancel.

### Group registration (corporate)
"Pay-once-for-N" via discount codes OR purchase order. Cvent has "Group" feature with single payment + multiple attendees.

### Tax handling (international, paid)
Different tax rules: US sales tax by state, EU VAT by country, etc. Stripe handles most; verify per platform.

### Multi-currency
For international events, allow USD + local currency. Stripe handles conversion. Display "Approximate USD" on reg page.

### Late registration (door price)
Differential pricing: day-of $999 vs early bird $599. Communicate cutoff dates clearly.

### Sponsor passes (free for sponsor team)
Allocate N free codes per sponsor tier. Sponsor distributes codes to their team. Tracking handled via discount code's "Allocated to" metadata.

## Sources

- **Cvent Developer Portal**: https://developers.cvent.com/
- **Bizzabo Open API**: https://developers.bizzabo.com/
- **Splash REST API**: https://api-docs.splashthat.com/
- **Eventbrite Platform**: https://www.eventbrite.com/platform/api
- **RingCentral Events Developer**: https://hopin.com/developers
- **Whova API**: https://whova.com/api
- **Cvent OnArrival Check-In**: https://www.cvent.com/en/event-marketing-management/on-arrival-event-check-in-software
