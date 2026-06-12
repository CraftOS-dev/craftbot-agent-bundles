<!--
Source: https://www.wired.com/story/best-travel-planning-apps + https://www.tripit.com + https://www.viator.com/partners/
-->
# Vacation Planning End-to-End — SKILL

Plan a multi-day vacation in 1-3 sessions. Intake → research → day-by-day itinerary → book in order (flights first, then hotels, then activities, then restaurants, then transit) → calendar holds → TripIt aggregation → vacation brief deliverable. Multi-step over multiple working sessions; supports two-way doors for cheap iterations.

## When to use this skill

- **"Plan our trip to X"** — direct trigger.
- **"Book us a vacation"** — broader scope.
- **"Itinerary for Tokyo / Italy / NZ"** — destination-specific.
- **"Family trip" / "couples trip" / "solo adventure"** — varies by party.
- **Pre-trip vacation brief generation** — paper output.

**Do NOT use this skill when:**
- Just flight + hotel for a business trip — see `travel-booking-tripit-hopper-kayak`.
- Restaurant reservations alone — see `restaurant-reservations-opentable-resy-tock`.
- Doctor appointment in travel city — out of scope.

## Setup

### Required MCPs (in agent.yaml)

- `google-flights-mcp`, `amadeus-hotels-mcp`, `booking-mcp`, `agoda-api-mcp` — flights + hotels
- `google-maps-mcp` — transit + drive time
- `firecrawl-mcp` — destination research
- `notion-mcp` — vacation brief deliverable
- `google-calendar-mcp` — holds
- `gmail-mcp` — confirmations + ground transport
- `openweathermap-mcp` — destination weather

### Optional services

- TripIt (see `travel-booking-tripit-hopper-kayak` for setup)
- Viator / Klook / GetYourGuide — activity API access
- Rome2Rio — transit options
- Sherpa — visa requirements

```bash
# Viator partner: https://www.viator.com/partners/
# Klook partner: https://www.klook.com/affiliate/
# Rome2Rio API: https://api.rome2rio.com/
# Sherpa visas: https://www.sherpa.com/
```

## Common recipes

### Recipe 1: Intake brief

```markdown
**Vacation Intake**
- Destination(s): [list, in order]
- Dates: [start - end, flex window]
- Party: [adults + kids + ages]
- Budget total: [$amount, currency]
- Travel style: [luxury / boutique / mid-tier / budget / adventure / family / cultural]
- Must-do: [3-5 items]
- Hard no: [3-5 items]
- Dietary / accessibility / allergies: [...]
- Loyalty programs: [carriers, hotels]
- Visa / passport status: [verify]
```

### Recipe 2: Destination research

```bash
# Pull from authoritative sources
SOURCES=(
  "https://www.nytimes.com/wirecutter/reviews/best-tokyo-restaurants"
  "https://www.lonelyplanet.com/japan/tokyo/things-to-do"
  "https://eater.com/maps/best-restaurants-tokyo"
  "https://www.timeout.com/tokyo"
)

for url in "${SOURCES[@]}"; do
  mcp tool firecrawl.scrape --url "$url" --format markdown >> tokyo_research.md
done
```

### Recipe 3: Build day-by-day skeleton

```markdown
# Tokyo — Jul 15-22 (8 days)

## Day 1 — Jul 15 (arrival)
- 06:00 SFO → NRT (ANA)
- 16:00 arrive NRT
- 18:00 check in hotel Shinjuku
- 19:30 dinner: light izakaya (Toritama Roppongi)

## Day 2 — Jul 16 (Tokyo highlights)
- 09:00 Tsukiji + breakfast
- 11:00 Sensoji + Asakusa walk
- 13:00 lunch: tonkatsu Maisen
- 14:30 Ueno Park + museum
- 18:00 rest at hotel
- 19:30 dinner: Sushi Saito (concierge book)

## Day 3 — Jul 17 (Hakone day trip)
- 07:30 train to Hakone
- 11:00 ryokan checkin
- ...
```

One anchor activity per day; meals; transit between; afternoon rest; one "wing-it" slot.

### Recipe 4: Flight search

```bash
mcp tool google-flights.search \
  --origin SFO --destination NRT \
  --departure-date 2026-07-15 \
  --return-date 2026-07-22 \
  --adults 2 --cabin economy

# Cross-check via Amadeus for inventory + Hopper for predict
```

(See `travel-booking-tripit-hopper-kayak` for full flight recipes.)

### Recipe 5: Hotel search per neighborhood

```bash
# Tokyo example: Shinjuku for first 3 nights, Hakone ryokan for night 4, Shinjuku final nights
mcp tool booking.search \
  --city "Tokyo Shinjuku" \
  --checkin "2026-07-15" --checkout "2026-07-18" \
  --adults 2 --free-cancellation true --min-rating 4
```

### Recipe 6: Activity booking (Viator / Klook)

```bash
# Search Viator API for activities
curl -s "https://api.viator.com/partner/products/search?destId=687" \
  -H "exp-api-key: $VIATOR_API_KEY" \
  -H "Accept: application/json"
```

Surface 5 candidates; user picks 2-3 to book.

### Recipe 7: Restaurant reservations for each night

See `restaurant-reservations-opentable-resy-tock` for full flow. Pattern:

```bash
# Per restaurant deep-link
echo "https://www.exploretock.com/sushi-saito"
echo "https://resy.com/cities/ny/don-angie?date=2026-07-15&seats=2"
```

### Recipe 8: Transit via Google Maps

```bash
mcp tool google-maps.directions \
  --origin "Shinjuku, Tokyo" \
  --destination "Tsukiji, Tokyo" \
  --mode transit \
  --departure-time "2026-07-16T09:00:00+09:00"
```

For multi-leg: walk + train + walk.

### Recipe 9: Weather forecast

```bash
mcp tool openweathermap.forecast \
  --location "Tokyo,JP" \
  --start "2026-07-15" \
  --end "2026-07-22"
```

Pack accordingly; rainy → buy umbrella on arrival; hot → light layers.

### Recipe 10: Visa / passport check

```bash
# Pull from Sherpa or US State Dept
mcp tool firecrawl.scrape \
  --url "https://travel.state.gov/content/travel/en/international-travel/International-Travel-Country-Information-Pages/Japan.html"
```

Surface: visa-free duration, passport validity required (6 months min for most countries).

### Recipe 11: Insurance check

```bash
# Surface common providers
echo "Travel insurance options:
- Allianz: https://www.allianztravelinsurance.com/
- Faye: https://www.withfaye.com/
- World Nomads: https://www.worldnomads.com/
- SafetyWing: https://safetywing.com/"
```

### Recipe 12: TripIt aggregation

Forward all confirmation emails to `plans@tripit.com`:

```bash
mcp tool gmail.forward --to "plans@tripit.com" \
  --message-id "<flight-confirm-msg-id>"
# Repeat for hotel, activities, restaurant confirmations.
```

### Recipe 13: Calendar holds for whole trip

```python
# For each major event:
calendar_events = [
    ("Depart SFO — ANA 7", "2026-07-15T03:00-07:00", "2026-07-15T06:00-07:00"),
    ("Flight SFO -> NRT", "2026-07-15T06:00-07:00", "2026-07-16T10:30+09:00"),
    ("Hotel Shinjuku checkin", "2026-07-16T15:00+09:00", "2026-07-16T18:00+09:00"),
    ("Sushi Saito 7pm reservation", "2026-07-16T19:00+09:00", "2026-07-16T22:00+09:00"),
    # ... per day
    ("Hotel checkout", "2026-07-22T11:00+09:00", "2026-07-22T11:30+09:00"),
    ("Flight NRT -> SFO", "2026-07-22T17:00+09:00", "2026-07-22T11:30-07:00"),
]
for ev in calendar_events:
    google_calendar.create_event(...)
```

### Recipe 14: Vacation brief deliverable

Output to `notion-mcp` or `docx`. Sections: cover (dates + party + budget), pre-trip (flight + hotel + insurance + visa confirmations), per-day H2 (anchor + meals + transit + buffer + wing-it), booking summary table, packing seed (per-day-count + weather + adapter + cash), emergency contacts, loyalty status reminders. Full template in `role.md` "Vacation brief template" section.

### Recipe 15: Pre-trip checklist (T-1 day)

See `travel-booking-tripit-hopper-kayak` Recipe 11. Add vacation-specifics:
- Restaurant reservations confirmed in TripIt
- Activities tickets in Apple Wallet
- Local SIM / Pocket Wi-Fi booked
- Cash exchanged or ATM card with no foreign fee

## Examples

### Example 1: Tokyo for a couple (7 nights)

**Goal:** First Tokyo trip; couple; mid-luxury; cultural + food focused.

**Steps:**
1. Recipe 1: intake (party, budget $5.5k, dates Jul 15-22, must-do: Sushi Saito, Hakone day trip).
2. Recipe 2: research (Wirecutter, Eater Tokyo, Lonely Planet).
3. Recipe 3: build skeleton.
4. Recipe 4: flights — ANA 7/8 with Star Alliance Gold.
5. Recipe 5: hotels — Park Hyatt Shinjuku 6 nights + Hakone Yutaka ryokan 1 night.
6. Recipe 7: restaurants per night (Sushi Saito via concierge call; rest via Recipe 1+2).
7. Recipe 6: 2 activities (Tsukiji food tour; Hakone day trip with private guide).
8. Recipe 8: transit per leg.
9. Recipe 9: weather (rainy season; pack umbrella).
10. Recipe 10: visa (none).
11. Recipe 12: forward all confirms to TripIt.
12. Recipe 13: 50+ calendar holds.
13. Recipe 14: full vacation brief.

**Result:** Tokyo trip end-to-end in 2 working sessions; deliverable for user to bring on phone.

### Example 2: Family Italy (12 days)

**Goal:** Family of 4 + grandparent; ages 8-72; Sep dates.

**Steps:**
1. Recipe 1: intake (party = 4 + 1; budget $15k; styles vary).
2. Multi-destination: Rome → Florence → Cinque Terre → Venice.
3. Recipe 4: open-jaw flights (FCO in, VCE out).
4. Recipe 5: family-friendly hotels per city + grandparent accessibility consideration.
5. Recipe 6: family activities (Roman Forum tour, cooking class, gondola).
6. Recipe 7: family-friendly restaurants per night.
7. Recipe 14: detailed brief with per-person packing.

**Result:** Multi-gen trip with all needs balanced.

### Example 3: Adventure solo NZ (14 days)

**Goal:** Solo backpacker; budget $4k; activity-focused.

**Steps:**
1. Recipe 1: intake (solo, $4k, must-do: Routeburn Track + Glow Worm Cave).
2. Recipe 2: research budget hostels + DOC huts.
3. Recipe 6: hut bookings (limited; book ASAP).
4. Recipe 4: cheapest flights (LATAM via Auckland).
5. Lighter hotel/hostel mix.
6. Recipe 14: minimalist brief.

**Result:** Adventure-style budget trip locked.

## Edge cases / gotchas

- **Booking order**: Flights first (constrain everything) → hotels by neighborhood → activities → restaurants. Two-way doors (free-cancellation) first; non-refundable later.
- **Lead times**: Popular restaurants 2-4 weeks; visas up to 4-8 weeks (China); passport 6+ month validity required for entry.
- **Flight + activity timing conflict**: Don't book 7am activity day-after red-eye landing.
- **Weather windows**: Rainy/monsoon season changes the plan. Recipe 9 first.
- **Time zone**: All calendar holds in destination TZ; departure / arrival flights in TZ at each end.
- **Local SIM + cash**: Buy SIM at airport or pre-order (Airalo eSIM); cash matters more than card in Japan / parts of Italy.
- **Lounge access**: Star Alliance Gold / Priority Pass / Amex Platinum. Surface available.
- **Activity duration vs day**: 1 anchor per day; over-stuffing = bad. Build in 1h+ buffer.
- **Travel days lose time**: Arrival = half day; departure = half day. Don't over-plan.
- **Pacing**: Family pace ≠ couple pace; kids need rest + snack stops. Solo female travelers — surface safety in some destinations.
- **Insurance pre-departure only**: Some won't cover after.
- **Currency risk + cancellation domino**: Book 2 months out for hotel; FX may move 5-10%; cancel flight, hotels may cascade — review penalty chain.
- **Wallet readiness**: Boarding pass + visa + travel insurance in Apple Wallet / Google Wallet pre-trip.

## Sources

- [WIRED best travel planning apps](https://www.wired.com/story/best-travel-planning-apps)
- [TripIt](https://www.tripit.com)
- [Wanderlog](https://wanderlog.com/)
- [Roadtrippers](https://roadtrippers.com/)
- [Viator Partners](https://www.viator.com/partners/)
- [Klook Affiliate](https://www.klook.com/affiliate/)
- [Rome2Rio API](https://www.rome2rio.com/documentation/)
- [Sherpa visa](https://www.sherpa.com/)
- [US State Dept](https://travel.state.gov/)
- [Lonely Planet](https://www.lonelyplanet.com/)
