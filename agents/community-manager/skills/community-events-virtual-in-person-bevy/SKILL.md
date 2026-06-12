<!--
Sources: https://bevy.com/ + https://lu.ma/ + https://www.goldcast.io/ + https://welcome.com/ + https://www.eventbrite.com/ + https://docs.zoom.us/
-->
# Community Events (Virtual + In-Person + Bevy) — SKILL

Event-type decision matrix: intimate / hybrid / large-scale virtual / in-person regional / chapter-based. Bevy (chapter SOTA), Lu.ma (casual creator), Hopin/RingCentral (hybrid), Goldcast/Welcome (B2B virtual), Zoom/Riverside (streaming), Eventbrite (ticketing). Post-event: attendee → Common Room sync + thank-you cascade.

## When to use

- New community needs first IRL or virtual event.
- Scaling to chapter-based program (Atlassian / Salesforce / Notion model).
- Quarterly town hall / member summit planning.
- AMA, virtual conference, hackathon, or in-person meetup.
- Re-engaging dormant members via event-driven content.
- Pre-launch events for product / book / course.
- Attendee data flow into community CRM (HubSpot / Common Room).

Trigger phrases: "community event", "meetup", "AMA event", "town hall event", "Bevy chapter", "Lu.ma", "Goldcast", "virtual conference", "in-person meetup", "Eventbrite".

## Setup

```bash
# Bevy (chapter-based) — REST API
curl -H "Authorization: Bearer $BEVY_TOKEN" \
  https://api.bevy.com/v1/chapters

# Lu.ma — REST API
curl -H "x-luma-api-key: $LUMA_KEY" \
  https://api.lu.ma/public/v1/event/create \
  -d '{"name":"Town Hall","start_at":"2026-07-15T18:00:00Z"}'

# Eventbrite
curl -H "Authorization: Bearer $EVENTBRITE_OAUTH" \
  https://www.eventbriteapi.com/v3/organizations/$ORG/events/

# Zoom-mcp for webinars
mcp tool zoom.create_webinar --topic "AMA" --start_time "2026-07-15T18:00:00Z" --duration 60

# Goldcast (B2B virtual)
curl -H "Authorization: $GOLDCAST_TOKEN" \
  https://api.goldcast.io/v1/events
```

Auth + env:
- `BEVY_TOKEN` — paid enterprise.
- `LUMA_KEY` — free + paid tiers.
- `EVENTBRITE_OAUTH` — Eventbrite OAuth.
- `ZOOM_OAUTH_TOKEN` — Zoom OAuth.
- `GOLDCAST_TOKEN` — Goldcast API.
- `RIVERSIDE_API_KEY` — Riverside for streaming-style.

Workspace prerequisites:
- Notion DB `Events` (cols: name, type, date, host, attendees, recording, post-event).
- Calendar (Google) for event registration sync.

## Common recipes

### Recipe 1: Event-type decision matrix

| Event type | Best platform | Cost | Audience | Cadence |
|---|---|---|---|---|
| Intimate AMA (10-50) | Zoom + Discord Stage | $0 | Top members | Monthly |
| Town hall (100-500) | Zoom Webinars + Restream | $50-300 | All members | Quarterly |
| Hybrid conference (500-2k) | Goldcast / Welcome / RingCentral Events | $1k-10k | Strategic | Annual |
| In-person meetup (10-100) | Lu.ma + Meetup.com | $0-200 | Regional | Quarterly |
| Chapter-based community | Bevy | enterprise | Distributed | Ongoing |
| Hackathon (200-2k virtual) | Devpost + Discord | $500-5k | Devs | Annual |
| Workshop / training (20-100) | Zoom + Notion | $50-200 | Learners | Monthly |
| Virtual booth at industry conf | n/a, partner with org | $1k-50k | New audience | Per conf |

### Recipe 2: Bevy chapter event creation

```bash
# Create event in a chapter
curl -X POST -H "Authorization: Bearer $BEVY_TOKEN" \
  https://api.bevy.com/v1/chapters/$CHAPTER_ID/events \
  -d '{
    "title": "Atlanta Community Meetup",
    "starts_at": "2026-07-20T18:00:00Z",
    "ends_at": "2026-07-20T20:00:00Z",
    "location_name": "Ponce City Market",
    "city": "Atlanta",
    "capacity": 50,
    "description": "Monthly meetup..."
  }'
```

### Recipe 3: Lu.ma casual event

```bash
curl -X POST -H "x-luma-api-key: $LUMA_KEY" -H "Content-Type: application/json" \
  https://api.lu.ma/public/v1/event/create \
  -d '{
    "name": "Q3 Community AMA",
    "start_at": "2026-07-15T18:00:00Z",
    "end_at": "2026-07-15T19:00:00Z",
    "description": "Founder + community Q&A. Bring questions.",
    "approval_required": false,
    "visibility": "public"
  }'

# Returns event_id + RSVP url
```

### Recipe 4: Eventbrite for paid event

```bash
curl -X POST -H "Authorization: Bearer $EVENTBRITE_OAUTH" \
  https://www.eventbriteapi.com/v3/organizations/$ORG/events/ \
  -d '{
    "event": {
      "name": {"html": "Member Summit 2026"},
      "start": {"timezone": "America/New_York", "utc": "2026-09-15T13:00:00Z"},
      "end": {"timezone": "America/New_York", "utc": "2026-09-15T22:00:00Z"},
      "currency": "USD"
    }
  }'

# Create ticket class
curl -X POST -H "Authorization: Bearer $EVENTBRITE_OAUTH" \
  https://www.eventbriteapi.com/v3/events/$EVENT_ID/ticket_classes/ \
  -d '{"ticket_class":{"name":"Member","cost":"USD,5000","quantity_total":200}}'
```

### Recipe 5: Zoom webinar with auto-recording

```bash
mcp tool zoom.create_webinar \
  --topic "Q3 Town Hall" \
  --start_time "2026-07-15T18:00:00Z" \
  --duration 60 \
  --settings '{
    "auto_recording": "cloud",
    "registration_type": 1,
    "approval_type": 0,
    "panelists_invitation_email_notification": true
  }'
```

### Recipe 6: Goldcast B2B virtual event

```bash
curl -X POST -H "Authorization: $GOLDCAST_TOKEN" \
  https://api.goldcast.io/v1/events \
  -d '{
    "name": "Customer Conference",
    "start_time": "2026-09-10T14:00:00Z",
    "duration_minutes": 240,
    "registration_form": {...}
  }'
```

### Recipe 7: Pre-event 7-day reminder cascade

```python
# D-7, D-3, D-1, D-0 (1h before)
SCHEDULE = [(-7, "save-the-date"), (-3, "agenda preview"), (-1, "tomorrow"), (-0.04, "1h reminder")]

for days_before, key in SCHEDULE:
    when = event_start - timedelta(days=abs(days_before))
    for attendee in registered_attendees:
        if attendee.opt_in_reminders:
            schedule_email(attendee.email, template=key, send_at=when)
            if attendee.in_discord:
                schedule_discord_dm(attendee.discord_id, template=key, send_at=when)
```

### Recipe 8: Post-event attendee → Common Room sync

```bash
# Pull attendee list from event platform
ATTENDEES=$(curl -H "..." https://api.lu.ma/public/v1/event/$EVENT_ID/guests | jq '.guests[]')

# Push to Common Room as a tagged segment
echo "$ATTENDEES" | jq -c '.' | while read attendee; do
  EMAIL=$(echo "$attendee" | jq -r .email)
  curl -X POST -H "Authorization: Bearer $COMMON_ROOM_TOKEN" \
    https://app.commonroom.io/api/v1/members/$EMAIL/tags \
    -d '{"tag": "attended-q3-town-hall-2026"}'
done
```

### Recipe 9: Thank-you cascade + recording share (D+1)

```python
# Email
gmail.send(
  to=attendee.email,
  subject=f"Thanks for joining {event.name}",
  body=f"""
Hi {attendee.name},

Thank you for joining {event.name} yesterday. Here's the recording: {recording_url}

Key resources:
- Slides: {slides_url}
- Q&A digest: {qa_digest_url}
- Next event: {next_event_url}

— $HOST
"""
)

# Discord post
discord_full.send_message(
  channel_id=ANNOUNCE_CH,
  content=f"🎬 Recording of yesterday's {event.name}: {recording_url}\n\nKey moments: {timestamps}"
)
```

### Recipe 10: Chapter lead onboarding (Bevy)

```bash
# Invite new chapter lead via Bevy
curl -X POST -H "Authorization: Bearer $BEVY_TOKEN" \
  https://api.bevy.com/v1/chapters/$CHAPTER_ID/leads \
  -d '{"email":"lead@city.com","role":"organizer"}'

# Send onboarding email
gmail.send(
  to="lead@city.com",
  subject="Welcome — Atlanta chapter lead",
  body=onboarding_template
)
```

## Examples

### Example 1: Monthly Lu.ma AMA series

**Goal:** 12 AMAs/year via Lu.ma; 50-100 attendees each.

**Steps:**
1. Create event in Lu.ma (Recipe 3).
2. Post Lu.ma RSVP link in Discord + Slack + newsletter.
3. 7-day reminder cascade (Recipe 7).
4. Day-of: post Zoom link + Discord Stage option.
5. Post-event: Common Room tag + recording + Q&A digest (Recipes 8, 9).

**Result:** Avg 78 attendees; 8 hit 100+. 3 attendees per AMA → Champion tier.

### Example 2: Bevy chapter program for B2B SaaS

**Goal:** Launch chapter program with 10 cities Year 1.

**Steps:**
1. Recipe 1 → Bevy is right tool (enterprise chapter).
2. Chapter lead recruitment via Common Room champion list.
3. Bevy API event creation per chapter (Recipe 2).
4. Chapter lead onboarding (Recipe 10).
5. Quarterly: chapter-lead sync via Zoom.
6. Post-event attendee → HubSpot + Common Room sync (Recipe 8).

**Result:** Year 1: 10 cities × 4 events = 40 events; 2.4k attendees; 180 SQLs.

## Edge cases / gotchas

- **Bevy is expensive** — only worth it at 5+ chapters; for 1-2 cities use Lu.ma + Meetup.
- **Lu.ma's email deliverability** — some corporate spam filters block; share calendar invite as backup.
- **Eventbrite fees** — 3.7% + $1.79 per paid ticket; eat into low-cost events.
- **Zoom webinar capacity** — base 500 attendees; bigger needs add-on; check before promoting.
- **Timezone confusion** — always state event time in 2+ timezones; auto-detect from email IP.
- **Hybrid event = double work** — physical + virtual need separate hosts. Don't underestimate.
- **In-person attendance forecast** — 50% RSVP show-rate is typical; over-invite or under-cater.
- **Recording consent** — pre-event "this will be recorded" notice; mute non-consent attendees.
- **Post-event drop-off** — D+1 thank-you cascade must fire same-day or attendance feels cold.
- **Speaker no-show** — always have backup content; never run an event with single point of failure.
- **Chapter-lead burnout** — annual stipend or swag + clear off-ramp; turnover is 30%/yr typical.
- **Common Room sync delay** — give attendees 7 days to "appear" before tagging in case of identity mismatch.
- **GDPR for events** — attendee data sharing requires opt-in; default privacy settings should be conservative.

## Sources

- [Bevy](https://bevy.com/)
- [Bevy community-led events](https://bevy.com/products/community-led-events-platform)
- [Lu.ma API](https://lu.ma/api)
- [Eventbrite API](https://www.eventbrite.com/platform/api)
- [Zoom Webinars API](https://docs.zoom.us/docs/api/webinars/)
- [Goldcast](https://www.goldcast.io/)
- [Welcome](https://welcome.com/)
- [Meetup API](https://www.meetup.com/api/)
