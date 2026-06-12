<!--
Source: https://developer.calendly.com/api-docs/ + https://cal.com/docs/api-reference + https://oncehub.com/api
Comparison: https://www.calendly.com/blog/calendly-vs-cal-com-vs-savvycal-2026
-->
# Scheduling Links — Calendly / Cal.com / OnceHub — SKILL

Publish scheduling links that filter noise, route to the right calendar, and respect protected blocks. Calendly owns mind-share + paid-tier workflows; Cal.com is open-source + self-hostable + dev-friendly; OnceHub does enterprise round-robin + complex routing. SavvyCal is the overlay alternative.

## When to use this skill

- **"Send a Calendly link" / "give me a scheduling link"** — direct request for a publishable link.
- **"Route external meetings"** — different question paths → different calendars (sales vs support vs exec).
- **"Set up event types"** — intro 15min, standard 30min, deep 1h, group event.
- **"Round-robin scheduling"** — 2-3 people share a calendar surface (OnceHub or Cal.com Teams).
- **Onboarding a personal-EA workflow** — link defaults to set up once.

**Do NOT use this skill when:**
- Calendar protection / focus defense — see `calendar-protection-motion-reclaim-sunsama`.
- One-off calendar event creation — call `google-calendar-mcp` directly.
- Internal team meeting where attendees are pre-known — direct invite via `google-calendar-mcp`.

## Pick the right platform

| User profile | Recommendation | Why |
|---|---|---|
| Solo / small team, needs SaaS, broadest integrations | **Calendly** | Largest ecosystem, deep workflows on paid tier |
| Self-host, dev-friendly, routing forms, open-source | **Cal.com** | OSS + Docker-deployable + advanced routing |
| Enterprise round-robin, complex multi-step routing, lead-gen | **OnceHub** | Mature routing + CRM integration |
| Overlay-style scheduling (reduce email back-and-forth) | **SavvyCal** | Drop the user's available slots into the email |

## Setup

### Calendly (REST API)

```bash
# Generate Personal Access Token: https://calendly.com/integrations/api_webhooks
export CALENDLY_TOKEN="<pat>"

# Smoke test
curl -s https://api.calendly.com/users/me \
  -H "Authorization: Bearer $CALENDLY_TOKEN"
```

Docs: https://developer.calendly.com/api-docs/

### Cal.com (cloud OR self-host)

Cloud:
```bash
# Generate API key: https://app.cal.com/settings/developer/api-keys
export CALCOM_API_KEY="cal_live_..."
curl -s 'https://api.cal.com/v2/me' \
  -H "Authorization: Bearer $CALCOM_API_KEY" \
  -H "cal-api-version: 2024-08-13"
```

Self-host:
```bash
git clone https://github.com/calcom/cal.com
cd cal.com && docker compose up -d
# Then bind your own domain + Google OAuth keys
```

Docs: https://cal.com/docs

### OnceHub (REST API — paid tier)

```bash
# API key from: https://app.oncehub.com/settings/integrations/api
export ONCEHUB_API_KEY="<key>"
curl -s 'https://api.oncehub.com/v2/users' \
  -H "API-Key: $ONCEHUB_API_KEY"
```

Docs: https://oncehub.com/api

## Common recipes

### Recipe 1: List Calendly event types

```bash
USER_URI=$(curl -s https://api.calendly.com/users/me \
  -H "Authorization: Bearer $CALENDLY_TOKEN" | jq -r '.resource.uri')

curl -s "https://api.calendly.com/event_types?user=$USER_URI" \
  -H "Authorization: Bearer $CALENDLY_TOKEN" \
  | jq '.collection[] | {name, slug, duration, scheduling_url}'
```

### Recipe 2: Create a single-use Calendly scheduling link

For sensitive prospects — link expires after 1 use.

```bash
EVENT_TYPE_URI="https://api.calendly.com/event_types/<uuid>"

curl -X POST https://api.calendly.com/scheduling_links \
  -H "Authorization: Bearer $CALENDLY_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"max_event_count\": 1,
    \"owner\": \"$EVENT_TYPE_URI\",
    \"owner_type\": \"EventType\"
  }"
```

Returns a unique URL that auto-expires after 1 booking.

### Recipe 3: List upcoming Calendly bookings

```bash
USER_URI=$(curl -s https://api.calendly.com/users/me \
  -H "Authorization: Bearer $CALENDLY_TOKEN" | jq -r '.resource.uri')

curl -s "https://api.calendly.com/scheduled_events?user=$USER_URI&status=active&min_start_time=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  -H "Authorization: Bearer $CALENDLY_TOKEN" \
  | jq '.collection[] | {name, start_time, end_time, invitees_uri}'
```

### Recipe 4: Cancel a Calendly booking

```bash
EVENT_UUID="<scheduled-event-uuid>"
curl -X POST "https://api.calendly.com/scheduled_events/$EVENT_UUID/cancellation" \
  -H "Authorization: Bearer $CALENDLY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reason":"User requested cancellation"}'
```

### Recipe 5: Create Cal.com event type via REST

```bash
curl -X POST https://api.cal.com/v2/event-types \
  -H "Authorization: Bearer $CALCOM_API_KEY" \
  -H "cal-api-version: 2024-06-14" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Working Session",
    "slug": "working-session",
    "lengthInMinutes": 30,
    "locations": [{"type": "integration", "integration": "google-meet"}],
    "bookingFields": [
      {"name":"name","type":"name","required":true},
      {"name":"email","type":"email","required":true},
      {"name":"agenda","type":"text","label":"What's the agenda?","required":true}
    ],
    "minimumBookingNotice": 1440,
    "beforeEventBuffer": 15,
    "afterEventBuffer": 15
  }'
```

### Recipe 6: Cal.com routing form (advanced routing by question)

Routing forms exist via the GUI in Cal.com self-host; via API:

```bash
curl -X POST https://api.cal.com/v2/routing-forms \
  -H "Authorization: Bearer $CALCOM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sales vs Support Router",
    "fields": [
      {"id":"q1","label":"Are you an existing customer?","type":"select","options":["Yes","No"]}
    ],
    "routes": [
      {"if":{"q1":"Yes"},"redirectTo":"https://cal.com/me/support-30min"},
      {"if":{"q1":"No"},"redirectTo":"https://cal.com/me/sales-30min"}
    ]
  }'
```

### Recipe 7: OnceHub round-robin booking page

```bash
curl -X POST https://api.oncehub.com/v2/booking_pages \
  -H "API-Key: $ONCEHUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sales — Round Robin",
    "type": "round_robin",
    "users": ["user-id-1","user-id-2","user-id-3"],
    "assignment_strategy": "first_available"
  }'
```

### Recipe 8: Calendly webhook for new bookings → Notion

```bash
# Subscribe to events
curl -X POST https://api.calendly.com/webhook_subscriptions \
  -H "Authorization: Bearer $CALENDLY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://n8n.example.com/webhook/calendly",
    "events": ["invitee.created","invitee.canceled"],
    "organization": "https://api.calendly.com/organizations/<uuid>",
    "scope": "user"
  }'
```

Then `n8n-workflow-automation` receives the webhook + writes to `notion-mcp`.

### Recipe 9: Test a link by booking against yourself

```bash
# Open the scheduling URL in browser (via playwright-mcp or open)
open "https://calendly.com/<user>/intro-coffee"
# Pick a slot; verify confirmation email + calendar block in google-calendar-mcp.
```

### Recipe 10: Bulk-create the standard event-type matrix

For new user onboarding — standard PA matrix:

```python
import requests, os

TYPES = [
    {"slug":"intro-15min", "title":"Intro Coffee","lengthInMinutes":15,
     "minimumBookingNotice":1440,"beforeEventBuffer":5,"afterEventBuffer":10},
    {"slug":"working-30min","title":"Working Session","lengthInMinutes":30,
     "minimumBookingNotice":1440,"beforeEventBuffer":15,"afterEventBuffer":15},
    {"slug":"deep-1h",      "title":"Deep Conversation","lengthInMinutes":60,
     "minimumBookingNotice":2880,"beforeEventBuffer":30,"afterEventBuffer":30},
]

for t in TYPES:
    r = requests.post("https://api.cal.com/v2/event-types",
        headers={"Authorization":f"Bearer {os.environ['CALCOM_API_KEY']}",
                 "cal-api-version":"2024-06-14"}, json=t)
    print(t['slug'], r.status_code)
```

## Examples

### Example 1: New executive — standard event-type matrix

**Goal:** Set up Intro / Working / Deep + family-block respect.

**Steps:**
1. Verify protected blocks live (Recipe 8 in `calendar-protection-motion-reclaim-sunsama`).
2. Run Recipe 10 to create 3 event types.
3. For each, verify `minimumBookingNotice` matches user's prep need.
4. Publish the user's main link page (Calendly: `calendly.com/<user>`; Cal.com: `cal.com/<user>`).
5. Test via Recipe 9.

**Result:** Publishable link page with 3 right-sized event types.

### Example 2: Single-use sensitive prospect

**Goal:** Send a one-time link to a prospect that auto-expires.

**Steps:**
1. Recipe 2 — create single-use scheduling link off the "Deep 1h" event type.
2. Send the URL via `gmail-mcp` with a personalized intro.
3. After booking arrives via webhook (Recipe 8), log to `notion-mcp` prospect DB.

**Result:** Link expires after 1 use; lead-gen flow tracked.

### Example 3: Cal.com routing form for inbound

**Goal:** Inbound traffic to a single landing page; route by question.

**Steps:**
1. Recipe 6 — create routing form with 2 routes (existing customer vs prospect).
2. Embed the form URL on landing page.
3. Customers route to 15-min support; prospects route to 30-min sales.
4. Each route lands on a different team-member's calendar via round-robin.

**Result:** Single inbound URL with intelligent routing.

## Edge cases / gotchas

- **Calendly free tier**: 1 event type only, no automated single-use links, no routing. Pro ($12/mo) for routing + multi-type. Source: https://calendly.com/pricing
- **Cal.com self-host requires PostgreSQL + Redis**: not trivial; recommend Docker Compose path. Production needs SMTP for confirmation emails. Source: https://cal.com/docs/self-hosting
- **OAuth + Google Workspace admin**: Both Calendly and Cal.com need full GCal scope. If admin restricts, OAuth fails — escalate to IT.
- **Timezone handling on links**: All three platforms auto-detect invitee TZ. But for the host, double-check working hours match local TZ — flying east/west breaks defaults.
- **Buffer + booking conflict**: Setting buffer=30min after a 1h event means a 30min meeting at 11am blocks 10:30-12:00. Visualize before launching.
- **Cal.com routing form rate**: Embedded forms tracked via JS — heavy on slow networks. Use plain redirect when possible.
- **OnceHub price tier**: OnceHub free tier = no API. Paid Growth tier ($15/user/mo) required. Source: https://oncehub.com/pricing
- **Webhook signature verification**: Always verify Calendly webhook signature (`Calendly-Webhook-Signature` header) before processing — replay attacks possible.
- **Single-use link race condition**: If 2 people open the same single-use link, both can book before max-event-count enforces. Calendly closes only after the first confirmation lands. Workaround: very-short expiration window.
- **Cancellation policy enforcement**: All three respect cancellation lead times but don't auto-charge no-show fees. Stripe integration via `stripe-mcp` for that.
- **Calendar feed lag**: Calendly + Cal.com refresh source calendar every 5 min. Real-time conflicts may slip through if a meeting was just added.
- **SavvyCal positioning**: SavvyCal is overlay-only (drop slots into email). Different UX. Recommend only if user complains "Calendly back-and-forth is too much."

## Sources

- [Calendly API docs](https://developer.calendly.com/api-docs/)
- [Cal.com API reference](https://cal.com/docs/api-reference)
- [Cal.com self-host guide](https://cal.com/docs/self-hosting)
- [OnceHub API](https://oncehub.com/api)
- [Calendly vs Cal.com vs SavvyCal 2026](https://www.calendly.com/blog/calendly-vs-cal-com-vs-savvycal-2026)
- [SavvyCal docs](https://savvycal.com/help/api)
