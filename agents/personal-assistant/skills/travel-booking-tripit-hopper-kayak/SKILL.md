<!--
Source: https://tripit.github.io/api/ + https://www.kayak.com/labs + https://developers.amadeus.com/
Comparison: https://www.nerdwallet.com/article/travel/best-flight-search-engines
-->
# Travel Booking — TripIt / Hopper / KAYAK — SKILL

Book flight + hotel + car with auto-itinerary aggregation, predictive pricing, and TripIt parsing. TripIt is the master itinerary; Hopper predicts the best buy moment; KAYAK + Google Flights + Amadeus run the actual search; Booking.com / Amadeus handle hotels.

## When to use this skill

- **"Book a flight to X" / "find me a hotel" / "rent a car"** — any single travel-booking request.
- **"Plan a business trip"** — flight + hotel + ground + reminders + calendar holds.
- **"Aggregate my itineraries"** — pull existing TripIt trips, refresh confirmations.
- **"Track flight price"** — Hopper predict + watch.
- **Pre-departure checklist** — T-1 day verification.

**Do NOT use this skill when:**
- Multi-day vacation planning end-to-end with activities + restaurants — see `vacation-planning-end-to-end`.
- Restaurant reservations on-trip — see `restaurant-reservations-opentable-resy-tock`.
- Filing expense reports post-trip — see `expense-tracking-expensify-ramp-brex`.

## Pick the right tool

| Need | Tool | Why |
|---|---|---|
| Auto-aggregate itineraries from email | **TripIt Pro** | Parses confirmation emails; flight tracker; Pro Plan ($49/yr) |
| Predict cheap-flight-now-vs-wait | **Hopper** | Proprietary ML; mobile-only; no public API |
| Broadest flight metasearch + price graph | **Google Flights** | Free; flexible-dates; price tracking |
| Filter-heavy flight search | **KAYAK** | Mature filters; bag fees; alarms |
| GDS / developer access (full inventory) | **Amadeus / Sabre** | Enterprise dev; full API |
| Hotel breadth + free-cancel rate | **Booking.com** | Largest network; flexible terms |
| Points redemption | **Amex Travel / Chase Travel / Capital One Travel** | Cardholder portals |

## Setup

### TripIt (OAuth-protected REST)

```bash
# Sign up free account + Pro ($49/yr) for auto-import
# TripIt API uses OAuth 1.0a (legacy):
# https://tripit.github.io/api/doc/v2/authentication.html

export TRIPIT_API_KEY="<consumer-key>"
export TRIPIT_API_SECRET="<consumer-secret>"
# OAuth dance via cli-anything or use email-forwarding fallback
```

**Easiest TripIt path**: Forward confirmation emails to `plans@tripit.com` from the registered address.

### Hopper

Hopper is mobile-only. No public API. Agent recommends user install + surfaces deep-links via universal URL scheme: `https://hopper.com/flights/<origin>-<dest>?date=<>`.

### Google Flights (via `google-flights-mcp`)

```bash
# Already wired in mcp_servers in agent.yaml
# Smoke:
mcp tool google-flights.search --origin SFO --destination NRT --departure-date 2026-07-15
```

### KAYAK

KAYAK Labs API is partner-only. Agent uses `firecrawl-mcp` for KAYAK price reads, or wraps via `playwright-mcp`.

### Amadeus (full GDS)

```bash
# Self-service at https://developers.amadeus.com/
export AMADEUS_CLIENT_ID="<id>"
export AMADEUS_CLIENT_SECRET="<secret>"

# Get token (90 min)
curl -s https://test.api.amadeus.com/v1/security/oauth2/token \
  -d "grant_type=client_credentials&client_id=$AMADEUS_CLIENT_ID&client_secret=$AMADEUS_CLIENT_SECRET" \
  | jq -r .access_token
```

### Booking.com (via `booking-mcp`) + Agoda (via `agoda-api-mcp`)

Both wired in `mcp_servers`. Recipient adds keys.

## Common recipes

### Recipe 1: Flight search via Google Flights

```bash
mcp tool google-flights.search \
  --origin SFO --destination NRT \
  --departure-date 2026-07-15 \
  --return-date 2026-07-29 \
  --adults 1 --cabin business
```

Returns 5-10 fare options. Optimize for: total travel time + reasonable connections (90min min) + airline loyalty match.

### Recipe 2: Amadeus flight offers + booking

```bash
AMADEUS_TOKEN=$(curl -s https://test.api.amadeus.com/v1/security/oauth2/token \
  -d "grant_type=client_credentials&client_id=$AMADEUS_CLIENT_ID&client_secret=$AMADEUS_CLIENT_SECRET" \
  | jq -r .access_token)

# Search
curl -s 'https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=SFO&destinationLocationCode=NRT&departureDate=2026-07-15&adults=1&max=5' \
  -H "Authorization: Bearer $AMADEUS_TOKEN"
```

For production booking, requires Amadeus Production account ($) + airline distribution agreements.

### Recipe 3: Hotel search via Amadeus

```bash
curl -s 'https://test.api.amadeus.com/v3/shopping/hotel-offers?cityCode=NYC&checkInDate=2026-07-15&checkOutDate=2026-07-18&adults=1' \
  -H "Authorization: Bearer $AMADEUS_TOKEN"
```

### Recipe 4: Hotel search via Booking.com MCP

```bash
mcp tool booking.search \
  --city "Tokyo" \
  --checkin "2026-07-15" \
  --checkout "2026-07-18" \
  --adults 2 \
  --sort price_low \
  --free-cancellation true \
  --min-rating 4
```

### Recipe 5: TripIt — list upcoming trips

```bash
# OAuth-signed GET (sketch — actual signing via cli-anything python script)
curl -s 'https://api.tripit.com/v1/list/trip/past/false/page_num/1/page_size/25/format/json' \
  -H "Authorization: OAuth oauth_consumer_key=$TRIPIT_API_KEY,..."
```

### Recipe 6: TripIt — manual add reservation (no email parse)

```bash
curl -X POST 'https://api.tripit.com/v1/create' \
  -H "Authorization: OAuth ..." \
  --data-urlencode 'json={
    "Trip": {"display_name":"Tokyo July 2026","start_date":"2026-07-15","end_date":"2026-07-21"},
    "AirObject": {"start_date_time":{"date":"2026-07-15","time":"06:00:00","timezone":"America/Los_Angeles"},
                  "Segment":[{"start_airport_code":"SFO","end_airport_code":"NRT","marketing_airline":"ANA","marketing_flight_number":"7"}]}
  }'
```

### Recipe 7: TripIt — forward parse fallback

If API auth too heavy: forward the original confirmation email to `plans@tripit.com`. TripIt auto-parses 100+ vendors (see role.md TripIt parse rules section for full list).

```bash
# Via gmail-mcp
mcp tool gmail.forward \
  --to "plans@tripit.com" \
  --from "<user@gmail.com>" \
  --message-id "<confirmation-msg-id>"
```

### Recipe 8: Create calendar holds for trip

After booking, create 5 standard holds via `google-calendar-mcp`:

```bash
# Departure airport arrival
mcp tool google-calendar.create_event \
  --summary "Depart SFO — ANA 7" \
  --start "2026-07-15T03:00:00-07:00" \
  --end   "2026-07-15T06:00:00-07:00" \
  --description "Confirmation: ABCXYZ; Seat: 12A"

# In-flight (block)
mcp tool google-calendar.create_event \
  --summary "Flight SFO -> NRT" \
  --start "2026-07-15T06:00:00-07:00" \
  --end   "2026-07-16T10:30:00+09:00" \
  --transparency opaque

# Hotel checkin / checkout
# Online checkin reminder 24h before
# Return travel mirror
```

### Recipe 9: Flight tracking

If user has TripIt Pro, `pro/flight_status` provides real-time + delay alerts. Fallback: FlightAware API.

```bash
# FlightAware (paid)
export FLIGHTAWARE_KEY="<key>"
curl -s "https://aeroapi.flightaware.com/aeroapi/flights/UA123" \
  -H "x-apikey: $FLIGHTAWARE_KEY"
```

### Recipe 10: Hopper deep-link

```bash
# Surface link for user to complete in mobile
echo "https://hopper.com/flights/SFO-NRT?date=2026-07-15&returnDate=2026-07-29"
```

### Recipe 11: Pre-departure checklist (T-1 day)

```markdown
- [ ] Online check-in (T-24h trigger)
- [ ] Boarding pass to Apple/Google Wallet
- [ ] TSA PreCheck / Global Entry on ticket
- [ ] Seat selected
- [ ] Hotel confirmation in TripIt
- [ ] Ground transport booked
- [ ] Calendar holds active
- [ ] Out-of-office set in gmail-mcp
- [ ] Power adapter / cables
- [ ] Passport in date (intl) + visa if needed
- [ ] Bag tags w/ destination address
```

## Examples

### Example 1: Domestic 3-day business trip

**Goal:** SFO → JFK Jul 15-17, 1 night Marriott Manhattan, no car.

**Steps:**
1. Flight: Recipe 1 (Google Flights) — find 3 options; recommend AA 1234 (UA Plus status, business class, 6h direct).
2. User confirms; book via airline.com (deep-link).
3. Hotel: Recipe 4 (Booking) — Marriott Marquis, breakfast, free cancel.
4. Recipe 7 — forward both confirmations to `plans@tripit.com`.
5. Recipe 8 — create 5 calendar holds + 24h check-in reminder.
6. Recipe 11 — surface pre-dep checklist.
7. Schedule `expense-tracking-expensify-ramp-brex` skill post-trip.

**Result:** Booked flight + hotel + 5 calendar holds + reminder + checklist.

### Example 2: International + points redemption

**Goal:** SFO → NRT, business class, redeem 80k Amex points via Pay-With-Points.

**Steps:**
1. Recipe 1: find cash fare ($3.5k business).
2. Surface Amex Pay-With-Points deep-link (no API): `https://travel.americanexpress.com/flights?from=SFO&to=NRT&date=2026-07-15`.
3. User books via Amex portal.
4. Forward confirmation to TripIt (Recipe 7).
5. International additions: passport-date check; visa exempt or required? (Japan: visa-free for US 90 days); travel insurance check.

**Result:** Points-redeemed booking + TripIt aggregation + international prep.

### Example 3: Track price + alert on drop

**Goal:** Flexible Sep travel; want to buy when fare drops $200.

**Steps:**
1. Recipe 1: baseline fare $850 SFO-LHR Sep 12-22.
2. Set up Google Flights price-tracking (within `google-flights-mcp`).
3. Recommend Hopper install (Recipe 10 deep-link).
4. Schedule weekly check via `n8n-workflow-automation`.
5. On drop > $200, agent emails user via `gmail-mcp`.

**Result:** Multi-source price watch + alert workflow.

## Edge cases / gotchas

- **TripIt OAuth 1.0a**: Legacy. Use email-forward fallback (Recipe 7) unless full integration needed.
- **TripIt Pro vs Free**: Free shows trips you forward. Pro ($49/yr) auto-parses inbox + adds flight status + airport reqs. Source: https://www.tripit.com/pro
- **Amadeus test vs production**: `test.api.amadeus.com` returns sample data (not real inventory). Production requires applications + revenue agreements with airlines.
- **Hopper has no API**: All recipes are deep-link only. Don't promise automated Hopper bookings.
- **Google Flights MCP doesn't book**: It's search-only; final booking is user-completion via airline site.
- **KAYAK Labs**: Real-time API requires partner agreement. Use `firecrawl-mcp` for read-only KAYAK queries.
- **Booking.com cancellation policy**: Verify `free-cancellation` flag is honored at the rate level (some "Free Cancellation" rates have a deadline). Check `is_genius_deal` and `cancellation_deadline` in response.
- **Time zone in TripIt manual add**: ALWAYS include `timezone` field (e.g., `America/Los_Angeles`). Without it, TripIt may pick wrong + display arrival mis-aligned.
- **OAuth scope on Gmail forward**: `gmail-mcp` needs `gmail.compose` scope to forward; verify before recipe 7.
- **Calendar TZ**: When booking international, `google-calendar-mcp` `start_time_zone` and `end_time_zone` must match origin/dest TZs respectively. See antipattern 3 in role.md.
- **Loyalty number on ticket**: Verify loyalty number was added at booking — adding after-the-fact via airline app is OK but not always automatic.
- **Travel insurance**: For international > $1k cost, recommend separate review. `cli-anything` + Allianz / Faye / SafetyWing APIs available.
- **Hopper free trial**: Hopper itself is free; some predictive features require account creation.
- **Booking.com payment**: Some rates "Reserve Now Pay Later" — verify before user thinks it's locked.

## Sources

- [TripIt API docs](https://tripit.github.io/api/)
- [TripIt Pro](https://www.tripit.com/pro)
- [Amadeus Self-Service](https://developers.amadeus.com/)
- [Google Flights help](https://support.google.com/travel/answer/9039220)
- [KAYAK Labs](https://www.kayak.com/labs)
- [Booking.com Demand API](https://developers.booking.com/)
- [Best flight search engines 2026](https://www.nerdwallet.com/article/travel/best-flight-search-engines)
- [Hopper](https://www.hopper.com/)
