<!--
Sources:
- Cvent Passkey Hotel Solutions: https://www.cvent.com/en/hospitality-cloud/passkey
- Marriott Group Bookings API: https://developer.marriott.com/
- Hilton Group Bookings: https://www.hilton.com/en/hilton-honors/group-travel/
- Hyatt Group: https://www.hyatt.com/en-US/group-bookings
-->
# Room Block + Hotel Partnerships — SKILL

Room blocks are a contractual minefield: attrition charges can hit $50K+ if pickup is low. This skill manages the full lifecycle — sizing, sub-blocks per attendee tier, pickup tracking, attrition risk monitoring, and overflow handling.

## When to use this skill

- Event has overnight attendees needing accommodation
- Speaker / VIP / sponsor blocks need separate sub-blocks at different rates
- Tracking pickup % vs attrition target (weekly cadence)
- Overflow / spillover planning (pickup exceeds block — add rooms vs overflow hotel)
- Multi-property block (downtown + airport hotels for large conferences)

**Do NOT use this skill when:**
- Day-event with no overnight attendees → skip room block entirely
- Venue includes guest rooms in package (hotels with built-in rooms) → still right-size sub-blocks
- Recipient has corporate travel program negotiating directly → coordinate, don't override

## Setup

### Cvent Passkey

```bash
# Cvent enterprise tier required
export CVENT_PASSKEY_API_KEY="<key>"

# Base endpoint
# https://api.passkey.com/v1/
```

### Direct hotel chain APIs (alternative)

```bash
# Marriott
export MARRIOTT_API_KEY="<key>"  # Developer portal: developer.marriott.com
# Hilton
export HILTON_API_KEY="<key>"
# Hyatt
export HYATT_API_KEY="<key>"
```

### Notion DB for tracking

```bash
mcp tool notion.create_database --name "room-block-tracker" --properties '{
  "Hotel": "title",
  "Block Type": "select:VIP|Speaker|Sponsor|General|Overflow",
  "Contracted Rooms": "number",
  "Rate": "number",
  "Pickup %": "number",
  "Cutoff Date": "date",
  "Attrition Threshold": "number",
  "Status": "select:Open|Cutoff|Attrition Risk|Closed"
}'
```

## Common recipes

### Recipe 1: Right-size the room block

Rule of thumb (per attendee type):

| Attendee type | Room block % of attendee count |
|---|---|
| Local attendees (same city) | 0% (don't block) |
| Regional (drive distance) | 15-25% |
| Out-of-region | 70-85% |
| Speakers + VIPs | 100% of speaker count + 50% buffer |
| Sponsors | 1 room per booth × tier multiplier |

```python
# Calculation example
total_attendees = 500
local_pct = 0.15
regional_pct = 0.30
out_of_region_pct = 0.55

block_size = (
    (total_attendees * local_pct * 0)  # locals don't need rooms
    + (total_attendees * regional_pct * 0.20)
    + (total_attendees * out_of_region_pct * 0.80)
) + speaker_count + (sponsor_count * 1.5)

# 500 * 0.15 * 0 + 500 * 0.30 * 0.20 + 500 * 0.55 * 0.80 + 25 + 30
# = 0 + 30 + 220 + 25 + 30 = 305 rooms
```

### Recipe 2: Sub-block setup (speaker / VIP / sponsor / general)

```bash
# Cvent Passkey: create sub-blocks
curl -X POST https://api.passkey.com/v1/blocks \
  -H "Authorization: Bearer $CVENT_PASSKEY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "eventId": "evt_xyz",
    "subBlocks": [
      {
        "name": "Speakers",
        "rooms": 30,
        "checkIn": "2026-09-14",
        "checkOut": "2026-09-18",
        "rate": 0,             // comped
        "billingMethod": "master_account",
        "bookingCodes": ["SPK2026"]
      },
      {
        "name": "VIP",
        "rooms": 20,
        "rate": 199,
        "billingMethod": "self_pay",
        "bookingCodes": ["VIP2026"]
      },
      {
        "name": "Sponsor",
        "rooms": 50,
        "rate": 229,
        "billingMethod": "self_pay",
        "bookingCodes": ["SPONSOR2026"]
      },
      {
        "name": "General",
        "rooms": 200,
        "rate": 259,
        "billingMethod": "self_pay",
        "bookingCodes": ["EVENT2026"]
      }
    ]
  }'
```

### Recipe 3: Attendee booking link / call-in

Cvent Passkey generates a unique booking link per sub-block:

```bash
curl -X GET https://api.passkey.com/v1/blocks/$BLOCK_ID/booking-link \
  -H "Authorization: Bearer $CVENT_PASSKEY_API_KEY"

# Response: https://book.passkey.com/event/<event-code>/owner/<id>
```

Embed in registration confirmation email (via `gmail-mcp` template).

### Recipe 4: Pickup tracking (weekly)

```bash
# Pull pickup data
curl -X GET https://api.passkey.com/v1/blocks/$BLOCK_ID/pickup \
  -H "Authorization: Bearer $CVENT_PASSKEY_API_KEY"

# Response:
# {
#   "contracted": 200,
#   "picked_up": 145,
#   "pickup_pct": 0.725,
#   "days_to_cutoff": 30,
#   "attrition_risk": "medium"
# }
```

Insert to `postgresql-mcp` warehouse + alert via `slack-mcp`:

```sql
INSERT INTO room_block_history (event_id, block_id, contracted, picked_up, pct, snapshot_date)
VALUES (...);
```

Alert thresholds:
- Pickup < 50% with 60 days to event → high risk → marketing push
- Pickup < 70% with 30 days to event → medium risk → email reminder
- Pickup < 80% at cutoff → confirm attrition penalty calculation

### Recipe 5: Attrition risk mitigation

When pickup is tracking low (60 days out):

```python
# Trigger:
if pickup_pct < 0.7 and days_to_event < 60:
    # 1. Email registered attendees who haven't booked
    unbooked = registrations.filter(hotel_booked=False)
    for attendee in unbooked:
        gmail.send_email(
            to=attendee.email,
            template='room_block_reminder',
            data={'name': attendee.name, 'booking_url': passkey_url, 'rate': 259}
        )
    # 2. Social push via marketing-agent
    # 3. Negotiate block reduction with hotel (often allowed pre-cutoff)
    # 4. Update slack-mcp ops channel
    slack.send(channel='event-ops', text=f'Room block at {pickup_pct*100:.0f}% — risk medium. Email push triggered.')
```

### Recipe 6: Block reduction (pre-cutoff)

Most hotels allow block reduction up to 30 days out without penalty. Use it:

```bash
mcp tool gmail.send_email \
  --to "$HOTEL_GROUPS_REP" \
  --subject "Block Reduction Request — Event ABC — 30 days out" \
  --body "Hi <rep>, We're tracking at 72% pickup. Per our contract, we'd like to reduce the block from 200 to 180 rooms to avoid attrition exposure. Please confirm written acknowledgment."
```

### Recipe 7: Overflow handling

When pickup exceeds block (good problem!):

```bash
# Option 1: Add rooms to primary block (if hotel has availability)
curl -X PATCH https://api.passkey.com/v1/blocks/$BLOCK_ID \
  -d '{"contractedRooms": 230}'

# Option 2: Add overflow hotel
# Source via Cvent Supplier Network (venue-sourcing skill)
# Set up secondary block; route attendees via "primary full" email
```

### Recipe 8: Direct hotel API (no Cvent Passkey)

For Marriott:

```bash
curl -X POST https://api.marriott.com/v1/group-bookings \
  -H "Authorization: Bearer $MARRIOTT_API_KEY" \
  -d '{
    "propertyId": "<property-id>",
    "groupName": "Event ABC 2026",
    "checkIn": "2026-09-14",
    "checkOut": "2026-09-18",
    "rooms": [
      {"type": "standard_king", "count": 100, "rate": 259},
      {"type": "double_queen", "count": 100, "rate": 259}
    ],
    "cutoffDate": "2026-08-14",
    "billingMethod": "self_pay"
  }'
```

## Examples

### Example A: 500-attendee tech conference, 3-night

Block sizing:
- 200 rooms general
- 30 rooms speaker (master account; comped)
- 20 rooms VIP (discounted; self-pay)
- 30 rooms sponsor (separate booking code per sponsor for attribution)

Tracking cadence:
- Weekly Slack digest
- Daily alert if pickup < 60% within 45 days
- Pre-cutoff reduction at 65% pickup → 180 rooms (saves $X in potential attrition)

### Example B: Multi-property block (downtown + airport)

```yaml
primary_hotel:
  property: Marriott Marquis Chicago
  rooms: 250
  rate: 299
  walkable: true
overflow_hotel:
  property: Hilton Garden Inn O'Hare
  rooms: 50
  rate: 189
  walkable: false  # shuttle required
  shuttle: 30min loop, 6am-11pm
```

Communicate clearly: primary fills first, overflow only when primary full.

### Example C: Customer summit (small, exec-focused)

50-attendee summit at boutique hotel:
- 50 rooms 1-night
- All comped (recipient-paid)
- Master account billing
- VIP arrival check-in (dedicated registration desk in hotel lobby)

No attrition risk (recipient pays regardless of attendance), but still track no-shows for budget reconciliation.

## Edge cases

### Pickup tracking lag
Hotels often update pickup data weekly, not daily. For events <30 days out, request manual pickup count via direct contact. Update Notion DB manually.

### Government attendees + per diem caps
Federal attendees can't exceed GSA per diem rates. Negotiate a sub-block at per diem rate (varies by city; lookup at gsa.gov).

### Currency for international attendees
Block rate in venue's local currency; communicate USD equivalent in registration. Note exchange rate disclosure: "Rates approximate; final charges in venue currency."

### Pet-friendly / accessibility room demand
Some attendees require pet-friendly OR mobility-accessible rooms. Add sub-block per requirement OR confirm hotel's general inventory includes adequate accessible rooms.

### Sponsor exclusivity
If sponsor commits to "host hotel" exclusivity, block must be at sponsor's specified property. Build sponsor approval into venue sourcing.

### Cutoff date confusion
Attendees often expect block availability up to event day. Communicate cutoff date in EVERY registration email + 14-day reminder + 7-day reminder.

### Late arrival / early departure
Block standard nights are check-in event day -1 + check-out event day +1. For pre/post tours or extended stays, negotiate "shoulder dates" rates within the block.

### Block sold out before cutoff
Means block was undersized — good problem. Add rooms (Recipe 7) OR direct attendees to alternate hotels with discount code. Update registration page with alert.

### Cancellation policy on individual reservations
Default hotel policy is 24-48 hour cancellation. For larger events, push for 7-day cancellation (better attendee experience; harder negotiation).

## Sources

- **Cvent Passkey**: https://www.cvent.com/en/hospitality-cloud/passkey
- **Marriott Developer Portal**: https://developer.marriott.com/
- **Hilton Group Travel**: https://www.hilton.com/en/hilton-honors/group-travel/
- **Hyatt Group**: https://www.hyatt.com/en-US/group-bookings
- **MPI Room Block Best Practices**: https://www.mpi.org/education/room-block-management
- **GSA Per Diem Rates** (federal): https://www.gsa.gov/travel/plan-book/per-diem-rates
