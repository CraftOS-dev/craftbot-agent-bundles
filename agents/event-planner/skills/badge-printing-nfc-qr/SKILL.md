<!--
Sources:
- Cvent OnArrival Check-In: https://www.cvent.com/en/event-marketing-management/on-arrival-event-check-in-software
- Klik SmartBadge by Bizzabo: https://www.bizzabo.com/klik
- Python qrcode lib: https://pypi.org/project/qrcode/
- Vistaprint API: https://developers.vistaprint.com/
- Conference Compass: https://www.conferencecompass.com/badges
-->
# Badge Printing (NFC + QR) — SKILL

Badge is the attendee's identity all event. Print-on-demand at venue OR pre-print bulk. NFC for sponsor lead capture (Klik SmartBadge); QR for self-service check-in and session attendance tracking. Sustainability tier (Sticker Mule + Conference Compass) for biodegradable alternatives.

## When to use this skill

- Any in-person event needing attendee identification
- Sponsor lead capture requirement (NFC SmartBadge essential)
- Session attendance tracking (QR scan at session doors)
- Hybrid event needing virtual + physical badge match
- Re-print station for lost badges (on-demand printing setup)
- Sustainability mandate (recyclable / biodegradable badge material)

**Do NOT use this skill when:**
- 100% virtual event → no badges (use virtual badge / avatar via event app)
- <30-person workshop → handwritten name tags acceptable (and feel personal)
- Recipient has procured badges from vendor and you're managing only deliverables → coordinate, don't reprocure

## Setup

### Cvent OnArrival (full kiosk + on-demand printing)

```bash
# Cvent paid; physical kiosk hardware ships pre-event
# API for badge template design
export CVENT_API_TOKEN="<token>"

# Set up badge template
curl -X POST https://api-platform.cvent.com/v1/events/$EVENT_ID/badgeTemplates \
  -d '{
    "name": "General Badge",
    "size": "4x3",
    "layout": "front_back",
    "fields": ["first_name", "last_name", "company", "role", "dietary_tag"],
    "qr_code_field": "qr_check_in_id",
    "logo_url": "https://cdn.example.com/logo.png"
  }'
```

### Klik SmartBadge by Bizzabo (NFC)

```bash
# Bizzabo subscription required
export BIZZABO_TOKEN="<pat>"

# Klik badges ship pre-event with NFC chips encoded per attendee
curl -X POST https://api.bizzabo.com/v1/events/$EVENT_ID/klik/configure \
  -d '{
    "badge_size": "4x3",
    "nfc_data": "attendee_id",
    "lead_capture": "enabled",
    "crm_sync": ["hubspot","salesforce"]
  }'
```

### DIY Python qrcode + bulk PDF + Vistaprint

```bash
# Install qrcode + weasyprint for PDF generation
pip install qrcode pillow weasyprint
```

```python
import qrcode
from weasyprint import HTML

# Generate QR per attendee
for attendee in attendees:
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(f"checkin://{attendee.id}")
    qr.make()
    img = qr.make_image()
    img.save(f"qr_{attendee.id}.png")

# Bulk PDF (4 badges per page, A4 layout)
html = f"""
<style>
  .badge {{ width: 100mm; height: 75mm; border: 1px solid #000; margin: 5mm; }}
  .name {{ font-size: 18pt; font-weight: bold; }}
  .company {{ font-size: 12pt; }}
  .qr {{ width: 30mm; height: 30mm; float: right; }}
</style>
<div>
  <div class="badge">
    <div class="name">{attendee.first_name} {attendee.last_name}</div>
    <div class="company">{attendee.company}</div>
    <img class="qr" src="qr_{attendee.id}.png" />
  </div>
  ...
</div>
"""
HTML(string=html).write_pdf("badges_bulk.pdf")
```

### Vistaprint API (print + ship)

```bash
curl -X POST https://api.vistaprint.com/v1/print-orders \
  -H "Authorization: Bearer $VISTAPRINT_API_KEY" \
  -d '{
    "product": "badges_4x3",
    "quantity": 500,
    "design_pdf_url": "https://your-cdn.com/badges_bulk.pdf",
    "shipping_address": "<venue address>",
    "ship_by": "2026-09-13"
  }'
```

## Common recipes

### Recipe 1: Cvent OnArrival kiosk + on-demand printing

Set up at venue:
- Kiosks at registration entrance (1 per 100 attendees expected first hour)
- Pre-event: ship kiosks 2 weeks early; venue install + tested
- Day-of: attendee approaches kiosk → scans QR from confirmation email OR enters last name → kiosk prints badge in 8 seconds → lanyard attached → attendee proceeds

Capacity planning: 1 kiosk processes ~8 attendees/min. For 500 attendees in 30 minutes, need 2 kiosks.

### Recipe 2: Klik SmartBadge (NFC for lead capture)

```bash
# Sponsor's view: scan attendee badge → capture lead → sync to CRM
# Attendee's view: tap badge to sponsor scanner → confirmation
# Lead capture protocol per sponsor:
mcp tool bizzabo.configure_lead_capture \
  --sponsor "Sponsor ABC" \
  --tier "Gold" \
  --crm "hubspot" \
  --questions "5 free-text per scan"

# Post-event: sponsor receives leads via Bizzabo export OR direct CRM sync
mcp tool bizzabo.export_sponsor_leads --sponsor "Sponsor ABC" --output sponsor_abc_leads.csv
```

### Recipe 3: QR code session tracking

For each session, generate a unique QR code at door. Attendees scan with event app OR camera to mark attendance.

```python
# Generate session QR
import qrcode
qr = qrcode.make(f"session_attend://session-123")
qr.save("session_123_qr.png")

# Print 8.5x11 with large QR + session title for door signage
```

Session attendance flows into engagement score (see `event-analytics-engagement-nps`).

### Recipe 4: Bulk print (no on-demand)

When budget is tight OR no kiosk infrastructure:

```python
# Generate all badges 7 days out (when reg cutoff hits)
# Send to Vistaprint API or print shop (FedEx, Office Depot, local printer)
# Ship to venue, arrive 48 hours before event
# Pre-stuff lanyard pouches in alphabetical order
# Volunteers at registration desk: lookup by name → hand over badge + lanyard
```

Cost: ~$1.50-$3/badge bulk + $50-$200 shipping. Less flexible than on-demand but cheaper.

### Recipe 5: Hybrid badge (NFC + QR + RFID)

```yaml
badge_design:
  size: 4x3 inch
  material: recycled PETG (biodegradable option)
  layers:
    front:
      - first_name (24pt)
      - last_name (24pt)
      - company (14pt)
      - role (12pt)
      - dietary_tag (color-coded dot)
    back:
      - QR code (3cm x 3cm) for session check-in
      - NFC chip embedded (lead capture)
      - emergency contact info (small print)
      - venue map URL (QR)
```

### Recipe 6: Dietary / accessibility tag color coding

Add color-coded dot to badge for kitchen staff quick reference:

```python
DIETARY_COLORS = {
    'vegan': '#4CAF50',      # green
    'vegetarian': '#8BC34A',  # light green
    'gluten_free': '#FF9800',  # orange
    'kosher': '#2196F3',      # blue
    'halal': '#9C27B0',       # purple
    'allergy': '#F44336',     # red (severe)
}
```

Print 8mm color dot in upper-right corner of badge.

### Recipe 7: Lost badge re-print

Have a backup printer at registration desk + access to:

```bash
# Reg desk view
mcp tool cvent.search_attendee --query "John Smith"
mcp tool cvent.reprint_badge --attendee_id "<id>" --reason "lost"
```

Charge fee for repeated re-prints ($20-$50) to discourage carelessness; comp first re-print.

### Recipe 8: Sustainability tier (biodegradable)

Vendors:
- **Conference Compass**: bamboo + compostable lanyard
- **Sticker Mule**: 100% recycled material
- **EarthHero**: hemp lanyards + recyclable badges

Cost premium: ~30-50% vs standard plastic. Communicate sustainability story in branded promo.

```bash
# Conference Compass order
curl -X POST https://api.conferencecompass.com/orders \
  -d '{
    "badges": 500,
    "material": "bamboo_compostable",
    "lanyard": "recycled_pet",
    "design_pdf_url": "..."
  }'
```

## Examples

### Example A: 500-attendee conference with Klik SmartBadge

- Klik NFC badges for all attendees
- Sponsor booths scan badges for lead capture (8 sponsors × 200 leads/day)
- Sponsor leads sync to HubSpot via Bizzabo's CRM integration
- Lead handoff to sponsors post-event via CSV from `sponsor-tier-deliverable-tracking` skill

### Example B: 200-attendee summit with bulk-printed badges

- Generate badges via Python qrcode + weasyprint
- Print at FedEx Office (lower cost than Vistaprint for small batches)
- Ship to venue 48 hours pre-event
- Pre-stuff with lanyards
- Manual lookup at reg desk

### Example C: Multi-day conference, QR session tracking

- Badges with QR for session attendance
- Each session door has scanner station OR attendee uses Whova app camera
- Session attendance reported in engagement score
- High-attendance sessions = signal for repeat content next year

## Edge cases

### Badge accuracy errors
Wrong name, misspelled company, etc. — on-demand printing solves it. Bulk printing locks errors; have re-print backup at venue.

### NFC scanner battery
Sponsor's scanner needs battery for full day. Provide chargers at sponsor lounge OR backup batteries.

### Privacy concerns (visible role / company)
Some attendees may not want role public (e.g., recruiters infiltrating). Offer "no role" option in reg form.

### VIP / speaker badge differentiation
Different color border / icon for VIP vs speaker vs general. Helps ops quickly identify; helps attendees recognize.

### Lost lanyards
Provide spare lanyards at reg desk. Cost: ~$1 each in bulk. Have 50 spare.

### Accessibility (visually-impaired attendees)
Larger font on request (28pt instead of 18pt). Braille name badges from EarthHero / specialty vendor (rare; advance order).

### Pre-printed vs on-demand cost difference
Bulk pre-print: $1-$3/badge. On-demand Cvent OnArrival: $5-$15/badge equivalent (after kiosk rental cost amortization).

### Live updates to badge
Bulk printing locks at print time. On-demand updates from reg DB → reflects last-minute job title changes, dietary updates.

### Multi-event annual conference
Use NFC chip with persistent attendee ID; same attendee can have history across events. Useful for VIP / repeat attendee recognition.

### Sponsor logos on attendee badges
Generally NOT done (cheapens attendee experience). Sponsors get logo placement on lanyards or specific co-branded badges for "founders / VIP" tier only.

## Sources

- **Cvent OnArrival**: https://www.cvent.com/en/event-marketing-management/on-arrival-event-check-in-software
- **Klik SmartBadge by Bizzabo**: https://www.bizzabo.com/klik
- **Python qrcode lib**: https://pypi.org/project/qrcode/
- **WeasyPrint**: https://weasyprint.org/
- **Vistaprint API**: https://developers.vistaprint.com/
- **Conference Compass (sustainable badges)**: https://www.conferencecompass.com/badges
- **Sticker Mule**: https://www.stickermule.com
