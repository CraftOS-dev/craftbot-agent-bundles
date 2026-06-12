<!--
Sources:
- Cvent Supplier Network: https://www.cvent.com/en/event-marketing-management/venue-sourcing-software
- Cvent Developer Portal: https://developers.cvent.com/
- Bizzabo Venue Concierge: https://www.bizzabo.com
- Splash Venue Directory: https://splashthat.com
-->
# Venue Sourcing (Cvent / Splash / Bizzabo) — SKILL

Programmatic venue sourcing across the SOTA hospitality marketplaces. Cvent Supplier Network is the default for any event >100 attendees with overnight room blocks (300K+ venues globally). Bizzabo Venue Concierge is included in the Bizzabo subscription for mid-market. Splash has a free brand-led venue directory for marketing events.

## When to use this skill

- New venue search for a confirmed format (in-person or hybrid)
- Comparing 3-5 venue proposals on F&B / room block / AV / accessibility / total cost
- Re-sourcing when an existing venue falls through (force majeure, lost negotiation)
- Multi-city roadshow venue scout (same format, different cities)
- Venue-history audit for repeat events (was last year's venue the best option?)

**Do NOT use this skill when:**
- Format isn't locked yet → run `event-format-selection-in-person-virtual-hybrid` first
- Venue is already signed → run `venue-contract-negotiation` for redline
- Recipient has a strong venue preference already → confirm dates + book directly

## Setup

### Cvent Supplier Network API

```bash
# Cvent paid account required. OAuth client credentials flow.
export CVENT_CLIENT_ID="<client-id>"
export CVENT_CLIENT_SECRET="<client-secret>"

# Get bearer token
export CVENT_API_TOKEN=$(curl -s -X POST \
  https://api-platform.cvent.com/v1/oauth2/token \
  -u "$CVENT_CLIENT_ID:$CVENT_CLIENT_SECRET" \
  -d "grant_type=client_credentials" | jq -r .access_token)
```

Endpoint base: `https://api-platform.cvent.com/v1/`

### Bizzabo Open API

```bash
export BIZZABO_TOKEN="<personal-access-token>"  # from Bizzabo > Settings > API
# Base: https://api.bizzabo.com/v1/
```

### Splash REST API

```bash
export SPLASH_API_KEY="<api-key>"  # from Splash > Settings > Integrations > API
# Base: https://api.splashthat.com/v1/
```

### Free fallback (no paid platform)

```bash
# Use brave-search + firecrawl-mcp for venue website scraping
mcp tool brave-search.search --q "<city> conference venue 500 capacity AV"
mcp tool firecrawl.scrape --url "<venue-url>" --formats "markdown,extract"
```

## Common recipes

### Recipe 1: Cvent Supplier Network venue search

```bash
curl -X POST https://api-platform.cvent.com/v1/venues/search \
  -H "Authorization: Bearer $CVENT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "destination": {"city": "Chicago", "state": "IL", "country": "US"},
    "eventDate": {"start": "2026-09-15", "end": "2026-09-17"},
    "meetingRooms": [{"capacity": 500, "setup": "theater"}],
    "guestRooms": {"peakNight": 350},
    "amenities": ["wifi","av_inhouse","accessible","parking"],
    "accessibility": ["wheelchair","listening_device"]
  }'
```

Response: paginated list of venues with capacity, room rates, F&B minimum, AV tier, contact.

### Recipe 2: Create RFP (Request for Proposal) to multiple venues

```bash
curl -X POST https://api-platform.cvent.com/v1/rfps \
  -H "Authorization: Bearer $CVENT_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "eventName": "Q3 Customer Summit 2026",
    "venueIds": ["venue_id_1","venue_id_2","venue_id_3","venue_id_4","venue_id_5"],
    "eventDateRange": {"start": "2026-09-15", "end": "2026-09-17"},
    "attendeeCount": 350,
    "guestRoomBlock": {"peakNight": 200, "checkIn": "2026-09-14", "checkOut": "2026-09-18"},
    "meetingSpace": [
      {"name": "General Session", "capacity": 350, "setup": "theater", "av": "full"},
      {"name": "Breakout A", "capacity": 100, "setup": "classroom"},
      {"name": "Breakout B", "capacity": 100, "setup": "classroom"},
      {"name": "Breakout C", "capacity": 100, "setup": "classroom"},
      {"name": "Networking Reception", "capacity": 350, "setup": "cocktail"}
    ],
    "fbMinimum": 75000,
    "responseDueDate": "2026-06-25",
    "decisionDate": "2026-07-15"
  }'
```

### Recipe 3: Compare proposals (Notion DB output)

```python
# Pseudo via cli-anything python
proposals = cvent.get_proposals(rfp_id)
comparison = []
for p in proposals:
    comparison.append({
        'Venue': p['venueName'],
        'Total Cost': p['totalEstimatedCost'],
        'F&B Min': p['fbMinimum'],
        'Room Rate': p['guestRoomRate'],
        'AV Tier': p['avPackage'],
        'Outside AV Allowed': p['outsideAvAllowed'],
        'Accessibility': p['accessibilityScore'],
        'Wifi Capacity': p['wifiBandwidth'],
        'Parking': p['parkingSpots'],
        'Walkable Hotels': p['nearbyHotels'],
        'Concession Notes': p['concessions'],  # what venue is willing to comp
        'Force Majeure Language': p['forceMejeureClause'],
    })

mcp_tool('notion.create_database_row', database='venue-comparison-db', properties=comparison)
```

### Recipe 4: Bizzabo Venue Concierge (mid-market)

```bash
curl -X POST https://api.bizzabo.com/v1/venue-search \
  -H "Authorization: Bearer $BIZZABO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Austin",
    "capacity": 200,
    "date": "2026-10-12",
    "type": ["hotel","conference_center","unique_venue"]
  }'
```

### Recipe 5: Splash venue directory (marketing-led events)

```bash
curl -X GET "https://api.splashthat.com/v1/venues?city=NYC&capacity=150&category=brand_venue" \
  -H "Authorization: Bearer $SPLASH_API_KEY"
```

### Recipe 6: Free fallback — manual search

When recipient has no Cvent/Bizzabo/Splash subscription:

```bash
# 1. Discover venues
mcp tool brave-search.search --q "Boston conference venue 300 capacity AV included"

# 2. Scrape websites for specs
for url in $(mcp_tool brave-search top_results); do
  mcp tool firecrawl.scrape --url "$url" --extract-schema '{
    "name": "string",
    "capacity": "number",
    "rooms": "array",
    "av": "string",
    "fb_minimum": "string",
    "contact_email": "string"
  }'
done

# 3. RFP via gmail-mcp
mcp tool gmail.send_email \
  --to "$(extract contact_email)" \
  --subject "RFP — [Event Name] — 300 attendees — Q4 2026" \
  --body "$(cat rfp_template.md)"
```

### Recipe 7: Venue history check (repeat events)

```sql
-- postgresql-mcp: venue performance history
SELECT v.name, v.city, v.last_used, v.avg_nps, v.av_complaints, v.fb_complaints, v.would_rebook
FROM venue_history v
WHERE v.city = 'Chicago' AND v.capacity_max >= 350
ORDER BY v.avg_nps DESC, v.last_used DESC;
```

## Examples

### Example A: 500-attendee in-person conference, Chicago, March 2027

```bash
# 1. Search
curl -X POST https://api-platform.cvent.com/v1/venues/search \
  -H "Authorization: Bearer $CVENT_API_TOKEN" \
  -d '{
    "destination": {"city":"Chicago","state":"IL"},
    "eventDate": {"start":"2027-03-10","end":"2027-03-12"},
    "meetingRooms": [{"capacity":500}],
    "guestRooms": {"peakNight":300}
  }'

# 2. Top 5 results → RFP to all
for venue_id in $(top_5_results); do
  curl -X POST https://api-platform.cvent.com/v1/rfps -d "{\"venueIds\":[\"$venue_id\"],...}"
done

# 3. Track proposals in Notion
# 4. Hand off final 3 to user for site visit + final selection
```

### Example B: Multi-city roadshow (4 cities, 200 attendees each)

Run same search per city; compile per-city comparison; standardize spec across cities for sponsor consistency.

```python
cities = ['Austin', 'Boston', 'San Francisco', 'New York']
for city in cities:
    proposals = cvent.search(city=city, capacity=200, dates=tour_dates[city])
    notion.create_db(f'roadshow-{city}-venues', proposals[:5])
```

### Example C: Unique / non-traditional venue (gala, popup)

Cvent has limited coverage for non-hotel venues. Use Splash's venue directory + firecrawl for boutique venues.

```bash
mcp tool brave-search.search --q "NYC industrial loft venue 200 capacity gala 2027"
# + Peerspace.com, Eventup, Splacer for unique venues
mcp tool firecrawl.scrape --url "https://peerspace.com/venues/<id>"
```

## Edge cases

### F&B minimum mismatch
If venue's F&B minimum is >70% of your projected F&B spend, flag for `venue-contract-negotiation`. Negotiate down OR find a venue without F&B minimum mandate.

### Room block attrition risk
If your room block exceeds 60% of expected attendees, you risk attrition charges. Right-size to 40-50% of attendee count + add sub-blocks per tier (speaker / VIP / general). See `room-block-hotel-partnerships`.

### In-house AV monopoly
Many hotels mandate in-house AV at 2-3x market rate. Flag immediately for `venue-contract-negotiation`. Outside-vendor allowance must be in writing.

### Accessibility unconfirmed
Cvent's "accessibility tier" is venue self-reported. Always verify via site visit OR explicit checklist email to venue accessibility coordinator. See `accessibility-ada-captioning-interpretation` for the audit.

### Walkability + transit
Attendee perception of venue quality is influenced by walkable food/coffee within 5-min walk + transit access. Score venues on walkability using `brave-search` for nearby amenities.

### Last-minute sourcing (<60 days out)
Cvent RFP cycle is typically 2-3 weeks. For tight timelines, call venue sales directly. Bypass RFP; use `gmail-mcp` with direct contact + 48-hour response request.

### Sustainability requirement
For events with sustainability mandate, filter for LEED-certified or B Corp venues. Add `sustainabilityCertification` to search filter (Cvent supports this).

### International venues
Cvent Supplier Network is strong in US/EU/UK; weaker in APAC/LATAM. For Asia, use Asia Conference Solutions or local DMC (Destination Management Company).

### Hybrid format venue requirements
For hybrid, venue must have: ≥500Mbps wired uplink, capacity for camera + audio capture, ideally green-screen-friendly walls. Add to search criteria explicitly.

### Site visit decision
For venues >$50K total cost OR >300 attendees, in-person site visit is mandatory before contract signature. Schedule via `google-calendar-mcp`.

## Sources

- **Cvent Supplier Network**: https://www.cvent.com/en/event-marketing-management/venue-sourcing-software
- **Cvent Developer Portal**: https://developers.cvent.com/
- **Bizzabo Venue Concierge**: https://www.bizzabo.com/blog/venue-concierge
- **Splash Venue Directory**: https://splashthat.com/venues
- **MPI Venue Sourcing Best Practices**: https://www.mpi.org/education/venue-sourcing
- **Peerspace (unique venues)**: https://peerspace.com
