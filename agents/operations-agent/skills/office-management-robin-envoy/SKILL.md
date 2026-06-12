<!--
Sources: https://archieapp.co/blog/envoy-vs-robin/
         https://robinpowered.com/
Robin = 2026 Gartner Magic Quadrant Leader for Workplace Experience.
Envoy = visitor management leader.
-->
# Office Management — Robin / Envoy — SKILL

Hybrid office coordination: desk booking, room booking, visitor management, delivery management, space analytics, neighborhood / team-day scheduling. Robin is the 2026 Gartner MQ Leader for Workplace Experience Applications (AI-powered workplace ops); Envoy is the visitor-management leader; Tactic / Skedda / Eden Workplace as alts.

## When to use

- Hybrid policy (1-3 anchor days/wk) needs coordination.
- Visitor / delivery management for office.
- Desk + room booking with team-day clustering.
- Space utilization analytics for lease decisions.
- Trigger phrases: "desk booking", "room booking", "visitor", "hot desk", "anchor day", "team day", "Robin", "Envoy", "Tactic", "Skedda", "Eden Workplace", "space analytics".

## Setup

```bash
export ROBIN_TOKEN="xxx"           # https://api.robinpowered.com — Pro+ tier
export ENVOY_TOKEN="xxx"           # https://docs.envoy.com — paid
export TACTIC_TOKEN="xxx"          # https://gettactic.com
export SKEDDA_TOKEN="xxx"          # https://skedda.com
```

## Common recipes

### Recipe 1: Tool selection
```yaml
choose:
  hybrid_desk_room_booking_AI_workplace_ops:
    primary: Robin
    why: 2026 Gartner MQ Leader; AI-powered; deepest desk + room + neighborhood + analytics
  visitor_first_office:
    primary: Envoy
    why: Visitor management leader; delivery; compliance / SLA
  cost_conscious_desk_only:
    primary: Skedda
    why: Simpler scheduling; cheaper per-resource
  team_day_clustering:
    primary: Tactic
    why: Anchor-day + team coordination focused
  small_team_no_separate_tool:
    primary: Google Calendar resource bookings
    why: Free; works for < 30 desks; no analytics
```

### Recipe 2: Robin — book a desk
```bash
curl -s -X POST "https://api.robinpowered.com/v1/desks/<desk_id>/reservations" \
  -H "Authorization: Access-Token $ROBIN_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "start":{"date_time":"2026-07-08T09:00:00","time_zone":"America/New_York"},
    "end":{"date_time":"2026-07-08T18:00:00","time_zone":"America/New_York"},
    "reservee":{"email":"avery@co.com"}
  }'
```

### Recipe 3: Robin — find available desks
```bash
curl -s "https://api.robinpowered.com/v1/locations/<loc>/desks/availability?start=2026-07-08T09:00:00&end=2026-07-08T18:00:00" \
  -H "Authorization: Access-Token $ROBIN_TOKEN" \
  | jq '[.data[] | select(.is_available) | {id, name, neighborhood, amenities}]'
```

### Recipe 4: Envoy — pre-register visitor
```bash
curl -s -X POST "https://api.envoy.com/v1/invites" \
  -H "Authorization: Bearer $ENVOY_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "visitor":{"name":"Jules K","email":"jules@example.com","company":"Customer Co"},
    "host_id":"<user>",
    "expected_arrival":"2026-07-10T14:00:00",
    "location_id":"<loc>",
    "agreement_to_sign":"NDA-v3"
  }'
```

### Recipe 5: Anchor-day policy enforcement (Robin)
```yaml
anchor_day_policy:
  engineering_team:
    days: [Tuesday, Wednesday]
    min_office_days_per_week: 2
    enforcement: soft  # remind, not block
  sales_team:
    days: [Monday, Thursday]
    min_office_days_per_week: 2
  ops_people_team:
    days: [Wednesday]
    min_office_days_per_week: 1
  all_company_day:
    day: Wednesday
    enforcement: hard
```

### Recipe 6: Room booking with capacity + amenities
```bash
curl -s "https://api.robinpowered.com/v1/spaces?capacity_min=8&amenities=zoom_room,whiteboard" \
  -H "Authorization: Access-Token $ROBIN_TOKEN" \
  | jq '[.data[] | {id, name, capacity, amenities}]'

# Book
curl -s -X POST "https://api.robinpowered.com/v1/events" \
  -H "Authorization: Access-Token $ROBIN_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "title":"Quarterly Ops Review",
    "start":{"date_time":"2026-07-15T14:00:00","time_zone":"America/New_York"},
    "end":{"date_time":"2026-07-15T15:30:00","time_zone":"America/New_York"},
    "space_id":"<conf-room>",
    "creator_email":"alex@co.com"
  }'
```

### Recipe 7: Space analytics — utilization heatmap
```python
# Pull desk reservations past 30 days → utilization heatmap
import requests, os, pandas as pd
r = requests.get('https://api.robinpowered.com/v1/locations/<loc>/desks/reservations?from=2026-06-01&to=2026-06-30',
    headers={'Authorization': f"Access-Token {os.environ['ROBIN_TOKEN']}"}).json()
df = pd.DataFrame(r['data'])
df['date'] = pd.to_datetime(df['start']['date_time']).dt.date
util = df.groupby(['date','desk_id']).size().reset_index(name='reservations')
# Pivot day-of-week × desk → heatmap
print(util.pivot_table(index='desk_id', columns='date', values='reservations'))
```

### Recipe 8: Visitor sign-in compliance flow
```yaml
envoy_visitor_flow:
  steps:
    - capture: [full_name, email, company, phone, photo]
    - agreements: [NDA-v3, Visitor-Health-Attestation]
    - notify_host: slack + email + sms
    - badge_print: yes
    - check_out: required_at_exit
  data_retention_days: 90    # GDPR / CCPA minimization
  evacuation_export: live    # for fire drill / emergency
```

### Recipe 9: Delivery management
```bash
# Envoy Deliveries — auto-OCR package label, notify recipient
curl -s -X POST "https://api.envoy.com/v1/deliveries" \
  -H "Authorization: Bearer $ENVOY_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "carrier":"UPS",
    "tracking_number":"1Z...",
    "recipient_search_term":"avery",
    "location_id":"<loc>"
  }'
```

### Recipe 10: Neighborhood / team-zone setup (Robin)
```yaml
neighborhood:
  - name: "Engineering East"
    floor: 4
    capacity: 24
    teams: [platform, infra]
    amenities: [standing_desks, monitors, whiteboards]
  - name: "Sales Bullpen"
    floor: 4
    capacity: 16
    teams: [sales, sales_engineering]
    amenities: [phone_booths, monitors]
  - name: "Quiet Library"
    floor: 5
    capacity: 8
    teams: any
    amenities: [silence_zone, no_calls]
```

### Recipe 11: Weekly anchor-day digest (Slack)
```bash
# Monday 09:00 — post who's in office today + this week
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "channel":"#nyc-office",
    "text":"This week in office (NYC HQ):\nMon: 12 desks, Eng anchor (Tue), Sales anchor (Mon, Thu).\nTue: 24 desks, Eng anchor.\nWed: 32 desks, ALL COMPANY DAY.\nThu: 18 desks, Sales anchor.\nFri: 8 desks.\n"
  }'
```

## Examples

### Example 1: Stand up Robin for 60-person hybrid HQ
**Goal:** Desk + room booking + anchor-day enforcement.
**Steps:**
1. Recipe 10: define neighborhoods / floors.
2. Import desk inventory from CAD/Floorplan.
3. Recipe 5: anchor-day policies per team.
4. Recipe 11: weekly digest.
5. Recipe 7: month-1 utilization report → lease-decision input.

**Result:** Booked desks, no double-bookings, data-driven space decisions.

### Example 2: Visitor flow + delivery for product launch event
**Goal:** 80 visitors checked in cleanly.
**Steps:**
1. Recipe 4: bulk pre-register from event RSVP list.
2. NDA on arrival via Recipe 8.
3. Recipe 9 for swag deliveries.
4. Evacuation export ready in case.

**Result:** Smooth event, compliant, badge-tracked.

## Edge cases / gotchas

- **Anchor-day "soft" enforcement.** Recipe 5 — calling out absentees publicly fractures team trust. Use soft nudges + manager 1:1s.
- **Visitor PII retention.** GDPR / CCPA — 90 days is typical retention; longer requires justification. Recipe 8 `data_retention_days`.
- **Photo capture for visitors.** EU requires lawful basis + signage at entry. **Defer to `legal-counsel` for binding GDPR Article 13 compliance.**
- **Robin/Envoy SSO.** Both support SAML SCIM via Okta/JumpCloud/WorkOS; mandatory for compliance.
- **Multi-location overlap.** People-on-rotation between SF + NYC create reservation overlaps; allow concurrent reservations per email but flag for clarity.
- **Lease-decision data integrity.** Don't make a lease cut on 30-day data; need 90 days of stable post-policy data.
- **Desk hoarding.** Auto-release un-checked-in desks after 60-90 min; Robin has this; tune to local norms.
- **Calendar integration sync lag.** Robin → Google/Outlook can lag 1-5 min; team-day digest must pull at the morning side.
- **Envoy NDA legal weight.** Visitor NDA via Envoy ≠ MSA-grade NDA for partners. For board / sensitive partners, use DocuSign / Adobe Sign + counsel-reviewed form.
- **Fire-drill / evacuation list.** Live export must be < 5 min stale; verify by testing monthly.
- **Defer to `legal-counsel` for binding visitor agreements, NDA enforceability, and worker monitoring (badge swipe data) under EU/state employee-monitoring law.**

## Sources

- Archie — Envoy vs Robin 2026: https://archieapp.co/blog/envoy-vs-robin/
- Robin: https://robinpowered.com/
- Envoy: https://envoy.com/
- Robin API docs: https://docs.robinpowered.com/
- Envoy API: https://docs.envoy.com/
- Tactic: https://gettactic.com/
- Skedda: https://www.skedda.com/
- Eden Workplace: https://www.edenworkplace.com/
