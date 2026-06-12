<!--
Source: https://platform.opentable.com/documentation/ + https://resy.com/help + https://www.exploretock.com/
-->
# Restaurant Reservations — OpenTable / Resy / Tock — SKILL

Search availability, book reservations, and pipe confirmations into the calendar. OpenTable owns the largest US restaurant network; Resy curates high-end NY/LA + Amex partnership; Tock specializes in prepaid + tasting menus + ticketed events. None expose a public consumer-booking API — agent does search + drafts + surfaces a deep-link OR uses `playwright-mcp` browser automation.

## When to use this skill

- **"Get me a table at <restaurant>"** — direct booking request.
- **"Find a restaurant near <hotel/venue>"** — on-trip dining research.
- **"Hard-to-book restaurant" (Carbone, Don Angie, Tatiana)** — Resy / SevenRooms reservation drops.
- **"Tasting menu / chef's table booking"** — Tock for prepaid + tickets.
- **Adding restaurant reservations to vacation brief** — see `vacation-planning-end-to-end`.

**Do NOT use this skill when:**
- General gift/shopping research — see `gift-research-shopping`.
- Errand routing (delivery vs reservation) — see `errand-routing-doordash-uber-eats-instacart`.
- Adding to calendar without booking — call `google-calendar-mcp` directly.

## Pick the right platform

| Need | Tool | Why |
|---|---|---|
| Default US restaurant search + most coverage | **OpenTable** | Largest US network; diner-points loyalty |
| Curated high-end + NY/LA + Amex tie | **Resy** | Curation lens + Amex Platinum reservation priority |
| Prepaid tasting menus + ticketed events | **Tock** | Designed for restaurants with cost-of-cancellation |
| Mid-tier + integrated reviews | **Yelp Reservations** | Yelp ecosystem |
| Concierge / white-glove for very-hard | **Sandwich / Amex Centurion** | Pay or have cardholder |

## Setup

### OpenTable (Affiliate API — partner only)

OpenTable does NOT offer a public consumer-booking API. The Affiliate API is partner-only:
- Apply at https://platform.opentable.com/documentation/
- Requires business justification + revenue share

Without affiliate access: use `playwright-mcp` for browser automation OR surface deep-links to user-completion.

### Resy (no public API)

No public booking API. Browser automation only.

```bash
# Direct URL pattern
echo "https://resy.com/cities/ny/<restaurant-slug>?date=2026-07-15&seats=2"
```

### Tock (no public API)

```bash
echo "https://www.exploretock.com/<restaurant-slug>"
```

### Playwright MCP

Already in `mcp_servers`. Use for restaurant browse + auto-fill book forms.

```bash
mcp tool playwright.navigate \
  --url "https://www.opentable.com/r/<restaurant-slug>"
```

### `firecrawl-mcp` for restaurant discovery + reviews

```bash
mcp tool firecrawl.scrape \
  --url "https://ny.eater.com/maps/best-restaurants-nyc"
```

## Common recipes

### Recipe 1: Search OpenTable for a name (browser-driven)

```bash
mcp tool playwright.navigate \
  --url "https://www.opentable.com/s?dateTime=2026-07-15T19%3A30&covers=2&term=carbone&metroId=8"
mcp tool playwright.snapshot
# Extract slot availabilities visible in DOM
```

### Recipe 2: Direct deep-link (user-completion)

```bash
# Build user-clickable URL
DATE="2026-07-15"
TIME="19:30"
SEATS=2
RESTAURANT_SLUG="carbone-new-york"

echo "https://www.opentable.com/r/$RESTAURANT_SLUG?dateTime=${DATE}T${TIME}&covers=$SEATS"
```

Send to user via `gmail-mcp` with intro: "Tap to confirm; auto-syncs to your TripIt + calendar after."

### Recipe 3: Resy availability check (playwright)

```bash
mcp tool playwright.navigate \
  --url "https://resy.com/cities/ny?date=2026-07-15&seats=2&query=don%20angie"
mcp tool playwright.snapshot
```

Resy uses dynamic JS — wait for DOM stable before extract.

### Recipe 4: Tock booking flow (prepaid)

```bash
mcp tool playwright.navigate \
  --url "https://www.exploretock.com/atomix"
# Slot selector then prepay flow; user-completion required for payment.
```

### Recipe 5: Eater Guides — restaurant clusters by city

```bash
mcp tool firecrawl.scrape \
  --url "https://ny.eater.com/maps/best-restaurants-nyc" \
  --format markdown
```

### Recipe 6: Post-booking → calendar hold

```bash
mcp tool google-calendar.create_event \
  --calendarId primary \
  --summary "Dinner @ Carbone" \
  --location "181 Thompson St, New York, NY 10012" \
  --start "2026-07-15T19:30:00-04:00" \
  --end   "2026-07-15T21:30:00-04:00" \
  --description "Confirmation: ABC123\nParty: 2\nResy/OT link: <url>\nDress code: smart casual" \
  --reminders '[{"method":"popup","minutes":60},{"method":"popup","minutes":1440}]'
```

### Recipe 7: Multi-night dining plan for trip

```python
PLAN = [
  {"date":"2026-07-15","name":"Carbone","slot":"19:30","party":2,"reservation":"OT"},
  {"date":"2026-07-16","name":"Atomix","slot":"19:00","party":2,"reservation":"Tock-prepaid"},
  {"date":"2026-07-17","name":"Don Angie","slot":"20:00","party":2,"reservation":"Resy"},
]
for p in PLAN:
    # surface deep-link per platform
    print(p['name'], p['slot'], p['reservation'])
```

### Recipe 8: Watch for cancellations (Resy drops)

For hard-to-book restaurants, run a polling watch via `n8n-workflow-automation`:

```yaml
# n8n workflow
- trigger: cron */15 * * * *
- step1: playwright.navigate https://resy.com/cities/ny/don-angie?date=2026-07-15&seats=2
- step2: snapshot + detect "slots available" DOM
- step3: if true, gmail-mcp send "Resy drop alert"
```

### Recipe 9: Cancel a reservation

OpenTable: pull confirmation URL from email → playwright navigate → click "Modify/Cancel".
Resy: same pattern — open confirmation deep-link → Cancel.

```bash
mcp tool playwright.navigate --url "<confirmation-url>"
mcp tool playwright.click --selector "[data-testid='cancel-reservation']"
```

### Recipe 10: Dietary / allergy notes injection

When booking, surface a structured note to attach:

```markdown
**Party of 2, anniversary celebration**
- Allergies: shellfish (severe)
- Preferences: vegetarian option for guest
- Special: birthday plate if possible
- Loyalty: OT Diner Points #12345
```

`gmail-mcp` can deliver these to the restaurant directly post-booking.

### Recipe 11: SevenRooms reservation discovery

Some high-end restaurants (NoMad, ABC Cocina) use SevenRooms backend. Same pattern: playwright + URL.

```bash
mcp tool playwright.navigate \
  --url "https://www.sevenrooms.com/reservations/<restaurant>?date=2026-07-15&size=2"
```

### Recipe 12: OpenTable Diner Points status check

```bash
# Login required; use playwright
mcp tool playwright.navigate --url "https://www.opentable.com/my/profile"
# Extract points balance + tier
```

## Examples

### Example 1: Anniversary dinner — NYC

**Goal:** Saturday Jul 18, 2026; need a great anniversary spot for 2.

**Steps:**
1. Recipe 5: pull Eater NY Top 10 guide.
2. Ask user: "Italian / French / Japanese / American / surprise?"
3. Filter candidates by user preference + availability via Recipe 1 (OT) and Recipe 3 (Resy).
4. Surface 3 options: Carbone (OT), Atomix (Tock prepaid), Don Angie (Resy).
5. Recommend Don Angie (anniversary, romantic, NYC Italian).
6. Recipe 2: surface deep-link.
7. After user confirms: Recipe 6 (calendar hold) + Recipe 10 (anniversary note to restaurant via gmail).

**Result:** Reservation deep-link sent + calendar hold + anniversary note delivered.

### Example 2: Hard-to-book — watch for cancellation

**Goal:** Get a 2-top at Carbone in 2 weeks.

**Steps:**
1. Recipe 1: initial check — full.
2. Recipe 8: set up n8n watch every 15 min on date window.
3. On drop alert: `gmail-mcp` notify user.
4. User completes booking; Recipe 6 adds to calendar.

**Result:** Watch set; user gets first-strike opportunity.

### Example 3: 3-night Tokyo dining plan

**Goal:** Solidify dinner reservations for Jul 15-17 Tokyo trip.

**Steps:**
1. Recipe 5: pull Tabelog / Eater Tokyo / Time Out Tokyo.
2. Ask user: 1 Michelin star night + 2 izakaya / casual?
3. Surface options + book:
   - Sushi Saito (call concierge — no online)
   - Inua (Tock prepaid; Recipe 4)
   - Toritama Roppongi (walk-in OK; mark on map)
4. Recipe 6: 3 calendar holds with addresses.
5. Add to `vacation-planning-end-to-end` master brief.

**Result:** 3-night dining plan locked.

## Edge cases / gotchas

- **No public booking APIs**: All recipes rely on `playwright-mcp` OR user-completion deep-links. Don't promise auto-booking.
- **OpenTable Affiliate**: Real auto-booking requires Affiliate API access (business agreement). Source: https://platform.opentable.com/about/affiliate
- **Resy bot defense**: Resy actively blocks scrapers; rotate user-agent, use Resy's official iOS app for trickiest drops.
- **Tock prepay**: Cancellation = forfeit deposit. Surface this clearly before user confirms.
- **Time zone in calendar holds**: Always include `-04:00`/`-07:00` in `--start` to avoid mis-display.
- **Dress code**: Some restaurants enforce smart-casual / jacket. Surface dress code in Recipe 6 description.
- **Special-occasion plate**: Don't promise — many restaurants ignore the note; surface as "request, not guarantee."
- **Allergy compliance**: For severe allergies, ALWAYS call the restaurant directly post-booking + cite kitchen confirmation in calendar description.
- **No-show fee**: OpenTable can charge $25-50 no-show on premium reservations. Surface to user before booking.
- **Concierge fallback**: For very-hard reservations (French Laundry, Atomix), surface Amex Centurion / hotel concierge / Sandwich as backup — not all are in scope for agent.
- **Calendar 1h vs 2h**: Default 2h hold is safe for dinner (longer for tasting menu — 3h). Don't underestimate.
- **Bilingual restaurants (Japan, France)**: Form may default to local language. Use playwright `--locale en-US` if available.
- **Browser auth required**: Some Resy / Tock flows require login. Either skip (deep-link to user) or set up authenticated playwright session.

## Sources

- [OpenTable Platform docs](https://platform.opentable.com/documentation/)
- [OpenTable Affiliate](https://platform.opentable.com/about/affiliate)
- [Resy help / about](https://resy.com/help)
- [Tock (Squarespace)](https://www.exploretock.com/)
- [SevenRooms](https://sevenrooms.com/)
- [Eater Guides](https://www.eater.com/maps)
- [Amex Centurion Concierge](https://www.americanexpress.com/us/credit-cards/centurion/)
