<!--
Sources:
- Whova API: https://whova.com/api
- Brella docs: https://brella.io
- Bizzabo Klik: https://www.bizzabo.com/klik
- EventMobi API: https://www.eventmobi.com
- Hubilo API: https://hubilo.com
- Swapcard developer docs: https://developers.swapcard.com
- vFairs platform: https://www.vfairs.com
-->
# Event App (Whova / Brella / Bizzabo / EventMobi) — SKILL

End-to-end event app setup: platform selection → branding → attendee import → agenda sync → speaker import → sponsor configuration → community board + Q&A + matchmaking → push notifications + day-of comms. The event app is the attendee's PRIMARY interface during the event — outranks the website, the printed agenda, and signage. Choose by audience size + budget + matchmaking importance.

## When to use this skill

- New conference / summit / hybrid event needing dedicated mobile app
- Replacing a paper agenda with digital (cost + sustainability win)
- Event needing in-app Q&A + community board + matchmaking
- Multi-day event where attendees navigate parallel tracks
- Trade-show with sponsor booth crawl + lead capture
- Virtual / hybrid event where in-app networking matters

**Do NOT use this skill when:**
- <50 attendee workshop (paper agenda + Slack channel is fine)
- Single-keynote webinar (use webinar platform native chat)
- Single-track summit <100 attendees (Notion DB share is adequate)
- B2C festival (different platform tier — Eventbrite / Aloompa)

## Setup

### Platform decision matrix

| Need | First-stop | Notes |
|---|---|---|
| Attendees <500 + budget <$5K | Whova | Affordable + mobile-first + community board |
| Attendees 500-5000 + branding fidelity | Bizzabo (with Klik SmartBadge) | Modern + mobile-first + lead capture NFC |
| Matchmaking is primary value | Brella | AI interest-based 1:1 meetings |
| Branded fully-custom app | EventMobi | Branded mid-market alternative |
| Virtual / hybrid heavy | RingCentral Events (Hopin) or Hubilo | Virtual-native + hybrid |
| Trade-show + B2B matchmaking | Swapcard | Combined experience + content + matchmaking |
| Trade-show / virtual expo | vFairs | Virtual booth + trade-show focus |
| Enterprise + Cvent ecosystem | Cvent Attendee Hub | Full integration with reg + sponsorship |

### Tools

- `cli-anything` for platform REST API (event creation + attendee import + agenda sync)
- `notion-mcp` for content source of truth (sync from Notion → app)
- `gmail-mcp` for attendee onboarding emails
- `figma-mcp` / `canva-mcp` for branded asset prep (splash screen, banners, theme colors)
- `slack-mcp` for day-of app issue triage

### Whova API

```bash
export WHOVA_TOKEN="<api-key>"     # Settings > API
# Base: https://whova.com/api/v1/
```

### Brella API

```bash
export BRELLA_TOKEN="<api-key>"
# Base: https://api.brella.io/v1/
```

### Bizzabo Open API

```bash
export BIZZABO_TOKEN="<personal-access-token>"
# Base: https://api.bizzabo.com/v1/
```

### EventMobi API

```bash
export EVENTMOBI_TOKEN="<api-key>"
# Base: https://api.eventmobi.com/v1/
```

## Common recipes

### Recipe 1: Whova event creation + branding

```bash
# Create event
curl -X POST https://whova.com/api/v1/events \
  -H "Authorization: Bearer $WHOVA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "DevConf 2027",
    "shortName": "devconf-2027",
    "startDate": "2027-09-15T08:00:00-05:00",
    "endDate": "2027-09-17T18:00:00-05:00",
    "timezone": "America/Chicago",
    "location": {
      "name": "Hilton Chicago",
      "address": "720 S Michigan Ave, Chicago, IL 60605",
      "lat": 41.8694,
      "lng": -87.6249
    },
    "description": "Mid-tier dev conference for 600 senior IC + manager attendees.",
    "branding": {
      "primaryColor": "#0066CC",
      "secondaryColor": "#FFD700",
      "logoUrl": "https://devconf.io/logo.svg",
      "splashScreenUrl": "https://devconf.io/app-splash.png"
    }
  }'
```

### Recipe 2: Bulk attendee import (Whova)

```bash
# Whova accepts CSV via API
curl -X POST https://whova.com/api/v1/events/$EVENT_ID/attendees/import \
  -H "Authorization: Bearer $WHOVA_TOKEN" \
  -F "file=@attendees.csv" \
  -F "options={\"sendInviteEmail\": true, \"skipDuplicates\": true}"
```

CSV format:
```csv
email,first_name,last_name,company,title,role,tags
alex@acme.com,Alex,Smith,Acme,Senior Engineer,attendee,"ai,infra"
sarah@linear.com,Sarah,Khan,Linear,Principal Engineer,speaker,"keynote,ai"
```

### Recipe 3: Agenda sync from Notion to Whova

```python
# Pull from notion-mcp source of truth
sessions = notion.query_db(database='devconf-2027-agenda')

for s in sessions:
    payload = {
        'name': s['title'],
        'description': s['abstract'],
        'startTime': s['start_iso'],
        'endTime': s['end_iso'],
        'location': s['room'],
        'track': s['track'],
        'speakers': [{'id': spk_id, 'role': 'speaker'} for spk_id in s['speakers']],
        'tags': s['tags']
    }
    requests.post(
        f"https://whova.com/api/v1/events/{EVENT_ID}/sessions",
        headers={'Authorization': f'Bearer {WHOVA_TOKEN}'},
        json=payload
    )
```

### Recipe 4: Speaker bulk import

```bash
curl -X POST https://whova.com/api/v1/events/$EVENT_ID/speakers/bulk \
  -H "Authorization: Bearer $WHOVA_TOKEN" \
  -F "file=@speakers.csv"
```

CSV:
```csv
email,name,company,title,bio,photo_url,linkedin,twitter
sarah@linear.com,Sarah Khan,Linear,Principal Engineer,"8 years scaling LLM systems.",https://...,linkedin.com/sarahkhan,@sarahkhan
```

### Recipe 5: Sponsor configuration

```bash
# Per sponsor, create sponsor profile + booth metadata
curl -X POST https://whova.com/api/v1/events/$EVENT_ID/sponsors \
  -H "Authorization: Bearer $WHOVA_TOKEN" \
  -d '{
    "name": "Linear",
    "tier": "Platinum",
    "logoUrl": "https://...",
    "description": "Linear is the modern engineering project management.",
    "website": "https://linear.app",
    "boothNumber": "1",
    "boothLocation": "Lobby Premium",
    "contactEmail": "events@linear.app",
    "documents": [
      {"name": "Product Brief", "url": "https://..."}
    ],
    "videos": [
      {"name": "Demo", "url": "https://youtube.com/..."}
    ],
    "leadCapture": true,
    "leadCaptureSettings": {
      "scanner": "klik_smartbadge",
      "syncToHubspot": true
    }
  }'
```

### Recipe 6: Brella matchmaking + interest taxonomy

```bash
# Set interest taxonomy
curl -X POST https://api.brella.io/v1/events/$EVENT_ID/interests \
  -H "Authorization: Bearer $BRELLA_TOKEN" \
  -d '{
    "interests": [
      {"name": "AI/ML Engineering", "category": "Technical"},
      {"name": "LLM Production", "category": "Technical"},
      {"name": "Infrastructure", "category": "Technical"},
      {"name": "Hiring", "category": "Business"},
      {"name": "Recruiting", "category": "Business"},
      {"name": "Co-Founder Search", "category": "Business"}
    ]
  }'

# Onboard attendees (they pick 3-7 interests at signup)
# Brella matches algorithmically; attendees book 1:1 meetings
```

### Recipe 7: Community board (Whova)

```bash
# Create topics for community discussion
curl -X POST https://whova.com/api/v1/events/$EVENT_ID/community/topics \
  -d '{
    "topics": [
      {"name": "Meet other Chicago-area folks", "description": "Find locals"},
      {"name": "LLM Production War Stories", "description": "Share what's broken"},
      {"name": "Hiring + Recruiting", "description": "Posting jobs welcome"},
      {"name": "Lost & Found", "description": "Day-of help"}
    ]
  }'
```

### Recipe 8: Push notifications (day-of)

```bash
# Day-of cadence:
# 7:30am — "Doors open at 8am. Check in at the lobby."
# 8:55am — "Keynote starts at 9am. Find your seat."
# 10:25am — "Coffee break at 10:30. Sponsored by Datadog at booth #14."
# 12:25pm — "Lunch in the atrium. Vegan / GF / Halal stations marked."

curl -X POST https://whova.com/api/v1/events/$EVENT_ID/notifications \
  -d '{
    "title": "Doors open at 8am",
    "body": "Welcome to DevConf 2027! Check in at the lobby. Coffee is on us at sponsor station 14.",
    "sendAt": "2027-09-15T07:30:00-05:00",
    "audience": "all",
    "deepLink": "/agenda"
  }'
```

### Recipe 9: Bizzabo Klik SmartBadge NFC lead capture sync

```bash
# Klik SmartBadge syncs lead scans directly to sponsor CRM
curl -X POST https://api.bizzabo.com/v1/events/$EVENT_ID/lead-capture/configure \
  -H "Authorization: Bearer $BIZZABO_TOKEN" \
  -d '{
    "sponsorId": "acme_corp",
    "crmIntegration": "hubspot",
    "hubspotPortalId": "12345678",
    "hubspotApiKey": "secret-token-here",
    "leadSource": "DevConf 2027",
    "pipeline": "Conference Pipeline",
    "stage": "Marketing Qualified Lead"
  }'
```

### Recipe 10: EventMobi branded app

EventMobi is the best path for branded apps (full custom theme matching brand system).

```bash
curl -X POST https://api.eventmobi.com/v1/events \
  -d '{
    "name": "Acme Summit 2027",
    "branding": {
      "appIcon": "...",
      "splashScreen": "...",
      "primaryColor": "#FF0000",
      "fontFamily": "InterDisplay",
      "customCSS": "...",
      "tabBarIcons": {"agenda": "...", "speakers": "...", "sponsors": "..."}
    },
    "customFields": [
      {"key": "attendee_tier", "values": ["GA", "VIP", "Speaker"]}
    ]
  }'
```

## Examples

### Example A: 600-attendee Whova event setup (8 weeks pre-event)

```bash
# 1. Create event (Week -8)
# 2. Set branding (Week -8)
# 3. Import speakers (Week -7, after CFP closes)
# 4. Build agenda from CFP accepts (Week -7)
# 5. Open community board (Week -6)
# 6. Open attendee registration sync (Week -4, ongoing daily sync)
# 7. Configure sponsors (Week -2, after contracts close)
# 8. Schedule push notifications (Week -1)
# 9. Final mobile QA on iPhone + Android (Week -1)
# 10. Soft launch: attendee email with app link (Week -1)
```

### Example B: Hybrid event using Bizzabo (in-room app + virtual portal)

```bash
# Bizzabo handles both physical app + virtual viewing portal in one platform
# Configure:
# - In-room attendees access via mobile app
# - Virtual attendees access via web portal (same data)
# - Q&A unified across both audiences (Slido embedded)
# - Networking matchmaking works across both
```

### Example C: Brella matchmaking-first event (trade show)

```bash
# Brella's strength is 1:1 meeting density
# Configuration:
# - Interest taxonomy: 30-50 specific categories
# - Pre-event: attendees onboard, pick 5-10 interests
# - Brella suggests 10-20 matches per attendee
# - Attendees book meetings (15-30 min slots)
# - Pre-event nudge cadence: 14 days, 7 days, 3 days, 1 day
# - Day-of: app shows next meeting + location countdown
```

## Edge cases

### App rejected from App Store / Play Store
Apple / Google have approval delays (3-7 days). Some platforms (Whova, EventMobi) batch-publish under their corporate developer accounts so individual events don't need approval. Confirm with platform sales.

### Attendees who refuse to install
Always offer a web app fallback. Most platforms (Whova, Bizzabo) auto-generate a `web.<platform>.com/<event-slug>` URL. Print on signage as backup.

### Sponsor logo wrong resolution
Lead capture booth banners may render sponsor logos pixelated if uploaded at low DPI. Mandate vector (SVG / PDF) at contract signing.

### Push notification timing
Push notifications fire by device timezone, NOT event timezone. For multi-timezone hybrid events, schedule notifications per attendee timezone OR use "event-time" mode in Whova/EventMobi.

### Brella attendees not opting into matchmaking
Default opt-out kills value. Use opt-in during registration with clear value-prop ("get 5 1:1 meetings auto-matched"). Push reminder if attendee hasn't onboarded by 14 days out.

### Community board moderation
Open community boards attract spam + recruiter overflow. Designate 2-3 community moderators with auto-flag rules (block "free trial" / "DM me" patterns).

### Day-of app crash
Have venue wifi handle 1.5x peak load (everyone refreshes when app crashes). Ops keeps backup paper agenda for 50+ attendees in case app fails 30+ min.

### Q&A integration with Slido / Pigeonhole
Whova has native Q&A but most enterprise events use Slido for moderation. Configure deep-link in Whova to Slido session URL per session.

### Lead capture privacy compliance
GDPR/CCPA: capture explicit consent at scan ("share my info with this sponsor?" YES/NO). Default to NO. Some Klik / Whova configs default to YES — verify and override.

### Multi-language event apps
DeepL via `deepl-mcp` translates agenda content; manually QA before publishing. Some platforms (EventMobi) support multi-language natively.

### App link in event emails
Use deep links (e.g., `whova://event/<slug>`) that open the app if installed OR fallback to web. Test on iOS + Android pre-launch.

### Speaker bio sync conflict
If a speaker updates their bio in Sessionize but the app already has the old version, set up daily sync job from CFP → app to avoid drift.

### Attendee directory privacy
Allow attendees to opt-out of being listed in attendee directory. Default to OPT-IN. Document at registration.

### Sponsor lead handoff timing
Day-of leads must sync to sponsor CRM in real-time for opportunity tracking. If sync is daily-batch, sponsors complain. Verify Klik / Bizzabo settings.

## Sources

- **Whova API**: https://whova.com/api
- **Brella docs**: https://brella.io
- **Bizzabo Klik**: https://www.bizzabo.com/klik
- **Bizzabo Open API**: https://developers.bizzabo.com
- **EventMobi**: https://www.eventmobi.com
- **Swapcard developer**: https://developers.swapcard.com
- **Hubilo**: https://hubilo.com
- **vFairs**: https://www.vfairs.com
- **Cvent Attendee Hub**: https://www.cvent.com/en/event-marketing-management/attendee-hub
