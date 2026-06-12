<!--
Sources:
- Swag.com: https://swag.com
- Custom Ink: https://www.customink.com
- Imprint Direct: https://www.imprint.com
- 4imprint: https://www.4imprint.com
- Branded: https://www.branded.com
- Sticker Mule: https://www.stickermule.com
- Allbirds (sustainable): https://www.allbirds.com
- Patagonia Provisions: https://www.patagoniaprovisions.com
- Green Eco Promos: https://www.greenecopromos.com
- EventManagerBlog Swag: https://www.eventmanagerblog.com/conference-swag-ideas
-->
# Gift Bag + Swag Sourcing — SKILL

End-to-end swag pipeline: budget + sustainability decision → vendor selection → design + approval → quote → PO → drop-ship → day-of distribution → post-event NPS on swag. Bad swag becomes landfill within 30 days. Good swag (intentional, useful, sustainable) extends event lifetime as brand impression. Default: fewer items, higher quality, sustainability story.

## When to use this skill

- Conference / summit needing welcome swag bag for attendees (200-5,000 units)
- Sponsor-funded swag bag stuffers (sponsor brand + your event brand)
- Speaker gifts (premium tier, post-event thank-you)
- Sponsor booth giveaways (lead capture incentive)
- Virtual event swag mailed to attendee homes pre-event
- Sustainability-mandated event (carbon-neutral, B Corp, ESG-driven)

**Do NOT use this skill when:**
- <50 attendee workshop (skip formal swag; coffee mug from local shop is fine)
- Closed-door briefing where swag feels transactional
- High-end gala / awards (defer to specialist gifting concierge)
- B2C festival (different vendor tier — Etsy / Redbubble for indie)

## Setup

### Tools

- `cli-anything` for Swag.com / Custom Ink / 4imprint quote API
- `firecrawl-mcp` for vendor catalog scraping (lookup specific products)
- `gmail-mcp` for PO + tracking number management
- `notion-mcp` for vendor comparison + approval tracker
- `canva-mcp` / `figma-mcp` for swag artwork preparation

### Vendor decision matrix

| Need | First-stop | Notes |
|---|---|---|
| Modern + sustainability options | Swag.com | Mid-market, B Corp catalog, ethical sourcing |
| Full-service + broadest catalog | Custom Ink | Reliable, branded apparel default |
| Broad catalog + bulk pricing | Imprint Direct | Mass-market, large catalogs |
| Modern alt + faster turnaround | Branded | 5-7 day rush options |
| Stickers + small items premium | Sticker Mule | Vinyl stickers, magnets |
| Bulk + mass-market | 4imprint | Aggressive bulk pricing |
| Premium sustainable + storytelling | Allbirds + Patagonia | Higher unit cost, brand alignment |
| Sustainability-focused | Green Eco Promos | Recycled, compostable, biodegradable |

## Common recipes

### Recipe 1: Swag budget + scope decision

```markdown
# Swag Decision Matrix — DevConf 2027 — 600 attendees

## Total swag budget: $9K (cap at $15 per attendee)

## Tier breakdown
- General attendee bag (550 units × $12 = $6,600)
  - Branded tote (recycled canvas)
  - Notebook (recycled paper)
  - Pen (bamboo, refillable)
  - Sticker pack (3 stickers)
  - 1 sponsor item (in-kind)

- VIP / Speaker bag (50 units × $30 = $1,500)
  - Premium tote (eco-leather)
  - Quality water bottle (S'well or Klean Kanteen)
  - Premium notebook (Field Notes)
  - Branded headphones (sponsored)

- Sponsor booth giveaways (sponsor-funded; pass-through coordination)
  - Sticker packs (Sticker Mule)
  - Premium stress balls (B Corp vendor)
  - Power banks (sponsor budget)

## Sustainability scorecard
- 65% recycled materials
- 20% sustainably-grown materials (bamboo, organic cotton)
- 100% domestic shipping (USA-based vendors)
- 0% plastic single-use items
- Drop-ship direct to venue (no warehouse staging)
- Carbon offset for shipping ($95)

## Quality threshold: would an attendee keep this for 6+ months?
```

### Recipe 2: Vendor quote request

```bash
# Email Swag.com for quote
mcp tool gmail.send_email \
  --to "sales@swag.com" \
  --subject "Quote request — DevConf 2027 — 550 attendee bags + 50 VIP" \
  --body "$(cat <<'EOF'
Hi Swag.com team,

Looking for quotes on swag for DevConf 2027, Sept 15-17 in Chicago.

Bag composition (550 general + 50 VIP):

General attendee bag (550 units):
- Tote: recycled canvas (12" x 14"), 1-color logo print
- Notebook: 5x7", recycled paper, 1-color cover print
- Pen: bamboo / refillable, 1-color print
- Sticker pack: 3 vinyl stickers (already sourced from Sticker Mule)

VIP / Speaker bag (50 units):
- Premium tote: eco-leather, embossed logo
- Branded water bottle: S'well 17oz or equivalent
- Premium notebook: Field Notes 3-pack
- Branded socks: organic cotton, brand colors

Timeline: needed at venue Sept 12 (3 days before event)
Drop-ship to: Hilton Chicago, 720 S Michigan Ave, attn: Pat S.

Sustainability priority: prefer B Corp + recycled materials
Carbon offset for shipping desired

Quote breakdown: per-unit + setup fees + total + shipping
Production timeline + approval process

[Sender]
EOF
)"
```

### Recipe 3: Comparison matrix

```python
# Build vendor comparison in Notion
vendors_data = [
    {'vendor': 'Swag.com', 'unit_cost': 11.50, 'setup': 0, 'shipping': 380, 'sustainability_score': 9, 'turnaround_days': 21, 'b_corp': True},
    {'vendor': 'Custom Ink', 'unit_cost': 9.80, 'setup': 250, 'shipping': 420, 'sustainability_score': 6, 'turnaround_days': 18, 'b_corp': False},
    {'vendor': 'Branded', 'unit_cost': 12.20, 'setup': 0, 'shipping': 350, 'sustainability_score': 8, 'turnaround_days': 14, 'b_corp': True},
    {'vendor': '4imprint', 'unit_cost': 8.20, 'setup': 0, 'shipping': 450, 'sustainability_score': 4, 'turnaround_days': 25, 'b_corp': False}
]

for v in vendors_data:
    v['total_cost'] = 550 * v['unit_cost'] + v['setup'] + v['shipping']
    notion.create_db_row('vendor-comparison', v)

# Decision: Swag.com (B Corp + 9/10 sustainability + reasonable cost)
```

### Recipe 4: Artwork preparation

```bash
# Prepare logo files in required formats
# Most vendors need:
# - Vector: SVG / PDF / AI / EPS
# - Raster: PNG @ 300 DPI minimum, 4000x4000+
# - Color: spot color (Pantone) for screen print; CMYK for full color

# Generate via canva-mcp / figma-mcp
mcp tool figma.export \
  --file "devconf-logo.fig" \
  --format svg pdf png \
  --scale 4 \
  --output-dir "swag-artwork/"

# Per-item placement preview (mockup)
mcp tool canva.create_mockup \
  --template "tote-bag-mockup" \
  --logo "swag-artwork/devconf-logo.svg" \
  --colors "#0066CC,#FFD700" \
  --output "tote-mockup.png"
```

### Recipe 5: Approval workflow

```python
# Send approval request with mockups
mcp_tool('gmail.send_email',
         to=['marketing-lead@us.com', 'event-director@us.com'],
         subject='Swag approval — DevConf 2027 — review mockups by Friday',
         body='Mockups attached. Approve all OR flag changes.',
         attachments=['tote-mockup.png', 'notebook-mockup.png', 'pen-mockup.png'])

# Track approval in Notion
notion.create_db_row('swag-approvals', {
    'item': 'Tote bag',
    'vendor': 'Swag.com',
    'mockup_url': 'tote-mockup.png',
    'approval_status': 'Pending',
    'approver': 'event-director@us.com',
    'requested_date': '2027-08-01',
    'response_due': '2027-08-08'
})
```

### Recipe 6: PO + tracking

```bash
# After approval, place PO
mcp tool gmail.send_email \
  --to "sales@swag.com" \
  --subject "PO — DevConf 2027 — approved + ready to produce" \
  --body "Approved per attached mockups. Production go-ahead. Please send PO + tracking once shipped."

# Track in Notion
notion.update_row('swag-tracker', {
    'vendor': 'Swag.com',
    'po_number': 'PO-2027-093',
    'production_start': '2027-08-10',
    'expected_delivery': '2027-09-12',
    'tracking_number': null,  # update when shipped
    'amount': 6980
})
```

### Recipe 7: Drop-ship to venue

```markdown
# Drop-Ship Coordination — DevConf 2027

## Shipping address
Hilton Chicago — Loading Dock
720 S Michigan Ave, Chicago, IL 60605
Attn: Pat S. (Event Director) / DevConf 2027

## Delivery window
Sept 12, 2027 — 8am-5pm CT (3 days before event)

## Venue receiving capacity
Up to 50 cubic feet OK in storage room
Notify venue 7 days out via venue ops contact

## Receiving instructions
- Match PO numbers with bill of lading
- Photograph any damage at receipt
- Count quantities; flag shortage immediately
- Store in secure room (not loading dock)
- Move to ballroom Day 2 (Sept 13) for staging
```

### Recipe 8: Day-of distribution (registration check-in)

```markdown
# Swag Distribution at Check-In

## Setup
- 6 ft table at check-in (after badge handoff)
- Bags pre-filled (Day 2 by volunteers); separated by tier
- 1 staff per 100 attendees (550 attendees → 6 staff)

## Per-tier distribution
- General attendees: tote bag with pre-filled items
- VIP / Speaker: separate VIP table; tote + extras
- Sponsor staff: brief intro to sponsor booth + 1 sponsor product

## Stuffer items (1 sponsor product per bag)
- Pre-coordinate with sponsors (logo on stuffer + insert card)
- Sponsor-funded; pass-through coordination

## Tracking
- Count given out per hour (overflow detection)
- Flag if bags run short (target +5% buffer)
```

### Recipe 9: Virtual event swag (mailed pre-event)

```python
# For virtual events, mail swag to attendees pre-event
virtual_attendees = whova.get_event_registrations('devconf-virtual-2027')

for a in virtual_attendees:
    if a.confirmed and a.mailing_address:
        # Trigger drop-ship to attendee address via vendor API
        swag_dot_com.create_drop_ship_order({
            'recipient_name': a.full_name,
            'address': a.mailing_address,
            'items': ['standard_virtual_bag'],
            'delivery_window': '2027-09-08 to 2027-09-12',  # 1 week before event
            'message': 'Welcome to DevConf 2027 — see you online!'
        })
```

### Recipe 10: Post-event swag NPS

```bash
# In post-event NPS survey, ask about swag
# Add to Typeform (already sent via event-analytics-engagement-nps)
# - "Did you find the swag bag useful?"  1-5 scale
# - "Which item did you actually use?"   multi-choice
# - "What should we add next year?"      free-text

# Aggregate response
swag_results = typeform.get_responses('devconf-2027-swag')
favorites = aggregate(swag_results, 'used_item')
suggestions = extract_themes(swag_results, 'add_next_year')
```

## Examples

### Example A: 600-attendee conference, $15/attendee budget, sustainability-led

```
Bag composition (general 550 units):
- Recycled canvas tote: $5.50/unit (Swag.com)
- Recycled notebook: $3.20/unit
- Bamboo pen: $1.80/unit
- Sticker pack from Sticker Mule: $1.50/unit
- Sponsor stuffer (in-kind): $0/unit
Total per attendee: $12.00
Total cost: $6,600 (general) + $1,500 (VIP) = $8,100

Sustainability outcomes:
- 80% recycled / sustainably-sourced
- B Corp vendor (Swag.com)
- $95 carbon offset
- 0 plastic single-use

Post-event NPS:
- 78% rated swag bag "useful"
- 65% kept tote after event
- Top mentioned item: bamboo pen (60%)
```

### Example B: 200-attendee summit, premium VIP gifting

```
Premium VIP bag (200 units × $50):
- Patagonia Provisions snack pack
- S'well water bottle (laser etched logo)
- Field Notes 3-pack
- Premium socks (organic cotton)
- Welcome card hand-written
Total: $10,000

Outcome: ALL attendees kept bag (premium feel)
Cost-per-impression: high but justified for exec audience
```

### Example C: Virtual event mailing, $20/attendee budget

```
Pre-event mailed kit (250 virtual attendees × $20):
- Recycled tote
- Notebook + pen
- Snack bar (sponsor-branded)
- Welcome letter
- Mailed to attendee home pre-event (1 week buffer)

Logistics:
- Drop-ship from Swag.com directly (no warehouse staging)
- $5/unit shipping included
- 92% delivered on time
- 8% delivered post-event (acceptable; still keeps mailing list goodwill)
```

## Edge cases

### Sponsor logo on swag conflict
If sponsor wants their logo on attendee bag, this is part of sponsor contract (see `sponsor-tier-deliverable-tracking`). Cap at 2-3 sponsor logos per item; otherwise becomes billboard.

### Sponsor in-kind item rejected
If sponsor-provided item is low-quality (cheap plastic, off-brand), it dilutes the entire bag. Push back with sponsor; offer alternative placement.

### Vendor production delay
Order 21+ days out; allow 3-day buffer at venue. If vendor delays past T-3, switch to courier express OR local backup vendor.

### Quantity over-order
Order 5-10% over expected attendance for VIP / speaker buffer. Avoid huge over-orders (lands in storage).

### Quantity under-order
Worse than over. If you under-order, you fail attendee #X who already has their badge. Always +5%.

### Allergen / dietary swag items
Snack bars in swag bags must have allergen labels. Check ingredients before ordering. Some attendees will not consume; provide opt-out.

### Apparel sizing
Branded apparel needs size range S-XXXL. Order by size distribution per audience (industry avg: 5% S, 15% M, 30% L, 30% XL, 15% XXL, 5% XXXL).

### Tax / customs on international shipping
International virtual event swag: customs duties + import taxes. Use vendor with local fulfillment (Swag.com EU partner for EU attendees).

### Branding ban at venue
Some venues prohibit branded swag in certain areas (historic sites). Verify with venue ops.

### Sponsor wants to drop swag at booth (not in bag)
Sponsors with their own swag at booth: coordinate with sponsor booth manager. Don't double-stuff bag.

### Last-minute swag changes
Once production starts (T-21), changes are expensive. Lock approvals 14 days out. Don't change post-PO.

### Forgotten swag at venue
After event, leftover swag at venue: option 1) donate to local nonprofit; option 2) ship back to org (costs +$200); option 3) destroy (worst). Plan in advance.

### Personalized swag (names on items)
For VIP / speaker bags, personalization possible but 2-3 week lead time. Confirm names early.

### Carbon footprint disclosure
For sustainability-mandated events, calculate + offset shipping carbon. Document for compliance + ESG reporting.

## Sources

- **Swag.com**: https://swag.com
- **Custom Ink**: https://www.customink.com
- **Imprint Direct**: https://www.imprint.com
- **4imprint**: https://www.4imprint.com
- **Branded**: https://www.branded.com
- **Sticker Mule**: https://www.stickermule.com
- **Allbirds**: https://www.allbirds.com
- **Patagonia Provisions**: https://www.patagoniaprovisions.com
- **Green Eco Promos**: https://www.greenecopromos.com
- **EventManagerBlog Swag**: https://www.eventmanagerblog.com/conference-swag-ideas
- **Field Notes**: https://fieldnotesbrand.com
- **Klean Kanteen**: https://www.kleankanteen.com
- **S'well**: https://www.swell.com
