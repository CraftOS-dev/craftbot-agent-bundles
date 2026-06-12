<!--
Sources:
- Cvent Event Catering Software: https://www.cvent.com/en/event-marketing-management/event-catering-software
- NACE National Association for Catering and Events: https://www.nace.net
- FDA Food Allergen Labeling Act: https://www.fda.gov/food/food-allergensgluten-free-guidance
-->
# Catering Coordination (Dietary + Allergy) — SKILL

The catering pipeline from registration to plate. Diet capture at reg → aggregation → BEO (Banquet Event Order) draft → 72-hour count lock → day-of execution. Allergies are a legal and safety issue; this skill enforces the chain of custody.

## When to use this skill

- Any event with F&B service (breakfast / lunch / dinner / breaks / receptions)
- Multi-day event with refresh cadence
- Allergy disclosed at registration (severe / mild / moderate)
- Cultural / religious diet (kosher, halal) — needs vendor capability check
- Buffet vs plated vs station vs family-style decision
- Late-binding count changes (3-day before event)

**Do NOT use this skill when:**
- Event has no F&B (e.g., short standup meeting)
- Recipient outsources F&B to event manager — coordinate, don't execute
- Venue prohibits outside catering AND in-house is non-flexible — use `venue-contract-negotiation` to push for allowance

## Setup

### Tools

- Registration platform API (Cvent / Bizzabo / Splash) for dietary capture
- `notion-mcp` for aggregated count + BEO tracker
- `gmail-mcp` for BEO transmission to venue
- `slack-mcp` for day-of dietary alerts
- `docx` for BEO document

### Dietary categories (standardize across reg platforms)

- **Standard** — no restriction
- **Vegan** — no animal products
- **Vegetarian** — no meat or fish
- **Pescatarian** — fish OK, no meat
- **Gluten-free** — no wheat, barley, rye
- **Kosher** — certified kosher (NOT same as kosher-style)
- **Halal** — certified halal
- **Allergies** — free-text capture (severity)
- **Other** — free-text (e.g., low-FODMAP, paleo)

## Common recipes

### Recipe 1: Dietary capture at registration

```javascript
// Cvent custom field setup (one-time per event)
{
  "fieldName": "dietary_requirement",
  "fieldType": "multi_select",
  "options": ["Standard", "Vegan", "Vegetarian", "Pescatarian", "Gluten-free", "Kosher", "Halal", "Other"],
  "required": true
}

{
  "fieldName": "food_allergies",
  "fieldType": "long_text",
  "label": "Please list any food allergies and severity (e.g., 'severe peanut, mild dairy'). If none, type 'None'.",
  "required": true
}

{
  "fieldName": "allergy_severity",
  "fieldType": "single_select",
  "options": ["None", "Mild (preference)", "Moderate", "Severe (anaphylaxis)"],
  "required": false
}
```

### Recipe 2: Aggregate counts (export → Notion DB)

```python
# Pseudo via cli-anything
attendees = cvent.export_attendees(event_id)

dietary_counts = {
    'standard': 0,
    'vegan': 0,
    'vegetarian': 0,
    'pescatarian': 0,
    'gluten_free': 0,
    'kosher': 0,
    'halal': 0,
    'allergies': []
}

for a in attendees:
    dietary_counts[a.dietary] += 1
    if a.allergies and a.allergies != 'None':
        dietary_counts['allergies'].append({
            'name': a.name,
            'allergy': a.allergies,
            'severity': a.allergy_severity
        })

# Push to Notion
notion.update_page(beo_page_id, dietary_counts)
```

### Recipe 3: BEO draft (7 days out)

Send to venue catering manager 7 days before event:

```markdown
# BEO — [Event Name] — [Date]

## Venue + Room
- Venue: [...]
- Room(s): [...]
- Setup: [theater / classroom / banquet rounds / cocktail / mixed]
- Headcount: 200 (locked 72h out)

## Day 1 — Continental Breakfast (8:00am-9:00am)
- Setup: 7:00am
- Total headcount: 200
- Dietary breakdown:
  - Standard: 175
  - Vegan: 12 (separate labeled station)
  - Gluten-free: 8 (separate labeled station)
  - Halal: 3 (labeled tray)
  - Kosher: 2 (pre-packaged + labeled)
- Menu:
  - Standard: assorted pastries, fresh fruit, oatmeal station, eggs, bacon
  - Vegan: oat milk, fruit, vegan pastries, tofu scramble, vegan sausage
  - GF: GF pastries, fruit, yogurt parfaits, eggs
  - Halal: halal-certified meat, breads
  - Kosher: pre-packaged kosher meals
- Beverages: coffee, tea, juice, water
- Refresh: 8:30 (hot items replenished)

## Day 1 — Mid-Morning Coffee Break (10:30am-11:00am)
- Setup: 10:25am
- Headcount: 200
- Sponsored by [Gold sponsor] — branded coffee cart + napkins + signage
- Menu: coffee, tea, fruit, granola bars
- Standard, vegan, GF options all available

## Day 1 — Lunch (12:30pm-1:30pm)
- Setup: 12:15pm
- Total headcount: 200
- Service style: buffet (faster throughput) OR plated (more controlled allergens)
- Dietary breakdown: (same as breakfast)
- Menu: [...]
- Refresh: 1:00pm

## Allergy notes (free-text, individual)
- Attendee A (severe peanut): chef briefed, separate prep area, dedicated server delivers
- Attendee B (mild dairy): vegan options available
- Attendee C (vegan + soy-free): chef briefed; tofu replaced with chickpeas

## A/V + room setup per meal
- Breakfast: house music in pre-function; main stage AV down
- Lunch: house music in main stage; live mic on for emcee announcements

## Service staff requirements
- Breakfast: 4 servers + 1 chef + 1 dietary specialist
- Lunch: 6 servers + 1 chef + 1 dietary specialist
- Reception: 8 servers + 1 chef + 2 bartenders

## Pricing
- Per-person breakfast: $32
- Per-person lunch: $58
- Per-person coffee break: $18
- Total F&B per attendee: $108
- Total F&B (200 attendees): $21,600
- F&B contractual minimum: $20,000 ✓ exceeded

## Day-of contacts
- Recipient ops lead: [name + phone]
- Venue catering manager: [name + phone]
- Backup catering: [name + phone]
```

Send via `gmail-mcp`:

```bash
mcp tool gmail.send_email \
  --to "catering@venue.com" \
  --cc "ops@recipient.com" \
  --subject "BEO Draft — [Event Name] — [Date] — for review" \
  --body "$(cat beo_draft.md)" \
  --attachments "dietary_aggregated_counts.xlsx"
```

### Recipe 4: 72-hour count lock

Industry standard: final headcount locked 72 hours before event. Past this, venue can charge for the locked count regardless of actual show.

```python
from datetime import datetime, timedelta

event_date = datetime.fromisoformat('2026-09-15')
lock_deadline = event_date - timedelta(hours=72)

if datetime.now() > lock_deadline - timedelta(hours=24):
    # 24 hours before lock - send final reminder
    gmail.send_email(
        to='catering@venue.com',
        subject='Final headcount LOCKING in 24 hours',
        body=f'Current count: {final_count} (with +5% safety). Confirm receipt.'
    )

# At lock time:
lock_count = max(registered_count * 1.05, registered_count + 5)  # 5% safety OR 5 person minimum
gmail.send_email(
    to='catering@venue.com',
    subject=f'COUNT LOCKED at {lock_count} — [Event Name]',
    body=f'Final count locked at {lock_count}. Dietary breakdown attached.'
)
```

### Recipe 5: Day-of dietary alert (Slack)

```python
# On the day-of, attendee arrives + discloses new allergy at check-in
def handle_late_dietary(attendee, allergy):
    notion.update_attendee(attendee.id, dietary=allergy)
    slack.send_message(
        channel='event-catering-day-of',
        text=f':rotating_light: *NEW ALLERGY DISCLOSED*: {attendee.name} — {allergy}. '
             f'Notify catering. Severity: {attendee.severity}.'
    )
    gmail.send_email(
        to='catering@venue.com',
        subject=f'URGENT: New allergy disclosed — {attendee.name}',
        body=f'{attendee.name} just disclosed {allergy} at check-in. Severity: {attendee.severity}. Please notify chef.'
    )
```

### Recipe 6: Allergy incident protocol

If allergen incident at event:

```python
def handle_allergen_incident(attendee, incident):
    # 1. Notify medical
    twilio.send_sms(emt_phone, f'Allergen incident: {attendee.name} — {incident}. Location: {attendee.location}')
    # 2. Isolate dish (don't dispose; needed for review)
    # 3. Identify substitute dish; label clearly
    # 4. Log incident
    notion.create_page(database='incident-log', properties={...})
    # 5. Post-event: write to all attendees if affecting multiple
```

### Recipe 7: Sponsored coffee break coordination

When a sponsor pays for a coffee break (in-kind sponsorship):

```bash
# Verify in run-of-show + BEO
mcp tool notion.update_database_row \
  --database "run-of-show" \
  --row "coffee-break-day1-am" \
  --properties '{
    "Sponsor": "Sponsor ABC (Gold tier)",
    "Branded items": "coffee cart wrap, napkins, signage",
    "Logo placement": "above station + on napkins",
    "Announcement script": "Coffee provided by Sponsor ABC — leaders in [industry]. Find their booth at [location]."
  }'
```

Mark sponsor logo + napkin + cart prep in BEO. Verify day-of.

## Examples

### Example A: 200-attendee conference, 3-day, buffet style

- Day 1: continental breakfast + 2 coffee breaks + buffet lunch + networking reception
- Day 2: full breakfast + 2 coffee breaks + plated lunch (sponsored) + dinner gala
- Day 3: continental breakfast + 1 coffee break + grab-and-go lunch
- Total F&B budget: $42,500
- Dietary lock: 72 hours out at 215 (200 + 7.5% safety)

### Example B: 500-attendee mega-conference

- Higher complexity dietary tracking
- Use Cvent's dietary segmentation feature for per-meal counts
- Separate buffet stations per dietary (8 stations: standard / vegan / GF / halal / kosher etc)
- Increase chef-allergy specialist headcount
- Pre-pack kosher meals + alert kosher attendees of location

### Example C: 50-attendee customer summit, plated dinner

- Plated service (chef's preference for allergen control)
- Pre-arranged seating with dietary tags on placecards
- Server-runs-allergen-dish protocol (specific server per allergen)
- VIP-only menu OR mainstream menu w/ premium upcharge

## Edge cases

### Late allergy disclosure (day-of)
Chef MUST be informed. If severe (anaphylaxis), confirm EpiPen on-site (some venues require). Otherwise, substitute dish prepared in clean station.

### Cross-contamination at buffet
For severe allergies, use plated service OR dedicated allergen-free station with separate utensils. Buffet has cross-contamination risk venues warn about.

### Religious / cultural diet certification
Kosher: must be certified kosher (rabbinical supervision). "Kosher-style" is NOT kosher. Some venues partner with kosher caterers; verify in venue contract.

Halal: similar; verify certification.

### Plant-based / vegan options
Default 5-10% of attendee count for vegan options. If event audience is wellness/sustainability-focused, increase to 20%.

### Children + family attendees
Kids' menu separately if attendee count includes children. Add to BEO explicitly.

### Vendor catering vs venue catering
Some venues allow outside catering (rare for hotels, common for unique venues). If outside: confirm venue allows + insurance + serving license + outside vendor allowance fee.

### Late no-shows + waste
72-hour lock means recipient pays for no-shows. Some venues will donate to local food bank (waste-reduction practice). Ask in BEO process.

### Budget overrun (F&B exceeded contracted minimum AND projected)
Usually happens for high-attendance events. Confirm acceptable in budget; communicate to finance via `gmail-mcp` update.

### Beverage service (alcohol)
Cash bar vs open bar: significant cost difference. Open bar at $X/person × 200 = expensive. Cash bar saves $X but is attendee-friction. Cap consumption-based bar ($X cap).

### Local sourcing / sustainability
For sustainability-mandated events, source local farms + use seasonal menu + minimize plastic waste. Add to BEO + venue contract.

## Sources

- **Cvent Event Catering Software**: https://www.cvent.com/en/event-marketing-management/event-catering-software
- **NACE Standards**: https://www.nace.net
- **FDA Food Allergen Labeling Act**: https://www.fda.gov/food/food-allergensgluten-free-guidance
- **AllergyEats restaurant allergen training**: https://allergyeats.com/
- **PCMA F&B Best Practices**: https://www.pcma.org/convene/category/food-beverage/
