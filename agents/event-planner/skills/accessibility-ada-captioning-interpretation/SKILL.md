<!--
Sources:
- ADA Title III: https://www.ada.gov/topics/title-iii/
- ADA 36.303 (auxiliary aids): https://www.ada.gov/regs2010/titleIII_2010/titleIII_2010_regulations.htm#a36303
- Aberdeen Captioning: https://www.aberdeen.io
- 3PlayMedia: https://www.3playmedia.com
- Caption Mate: https://captionmate.com
- Cielo24: https://cielo24.com
- AI-Media (Ai-Live): https://www.ai-media.tv
- Sorenson Communications: https://sorenson.com
- Purple Communications: https://www.purple.us
- KultureCity: https://www.kulturecity.org
- Otter.ai: https://otter.ai
- AWS Transcribe: https://aws.amazon.com/transcribe/
- Accessible Arts Design: https://accessibleartsdesign.org
-->
# Accessibility (ADA Title III + CART + ASL) — SKILL

End-to-end accessibility pipeline: ADA Title III audit → accommodation capture at registration → CART captioning + ASL interpretation booking → sensory-friendly + materials → day-of execution → post-event compliance. Title III mandates auxiliary aids (Section 36.303); failing to provide is legal liability. Best practice: build accessibility into design, not retrofit.

## When to use this skill

- New event venue + format → ADA Title III audit
- Attendee accommodation request submitted at registration
- Booking CART captioning + ASL interpretation (14-21 days out)
- Day-of accessibility execution (sensory room, listening device handoff, materials)
- Post-event compliance documentation (lawsuit risk mitigation)
- Hybrid event needing both in-room + virtual accessibility

**Do NOT use this skill when:**
- Pure broadcast with no in-person attendees (still need captioning for ADA in some jurisdictions; consult)
- Closed-door briefing where all attendees confirmed accessible (skip formal audit; still document)
- B2C festival with different accessibility framework (consult specialist)

## Setup

### Tools

- `gmail-mcp` for vendor booking + accommodation request follow-up
- `notion-mcp` for accommodation request DB + vendor tracker
- `cli-anything` for Aberdeen / 3PlayMedia / AI-Media API
- `cli-anything` for venue accessibility verification via Cvent metadata

### Vendor contacts (pre-vetted)

```yaml
CART (real-time captioning):
- Aberdeen Captioning: services@aberdeen.io | 800-525-6678
- 3PlayMedia: hello@3playmedia.com | 855-3PLAY-ME
- Caption Mate: info@captionmate.com
- Cielo24: sales@cielo24.com
- AI-Media (Ai-Live): info@ai-media.tv

ASL interpretation:
- Sorenson Communications: 866-327-8877
- Purple Communications: contact@purple.us
- Local: search via Registry of Interpreters for the Deaf (RID) registry

Sensory:
- AccessibleArts.org: info@accessibleartsdesign.org
- KultureCity (venue certification): info@kulturecity.org

AI fallback:
- Otter.ai: API key configurable
- AWS Transcribe: AWS console
- Sonix: API tier required
```

## Common recipes

### Recipe 1: ADA Title III audit checklist (per venue)

```markdown
# ADA Title III Audit — Hilton Chicago — DevConf 2027

## Section 36.303 — Auxiliary Aids and Services

### Physical access
- [ ] Wheelchair access to ALL attendee areas (registration, sessions, dining, restrooms, networking)
- [ ] Accessible parking: 1 spot per 25 (first 100), then sliding (≥ 4 spots for 100 attendees)
- [ ] Accessible parking within 50 ft of accessible entrance
- [ ] Accessible restrooms on same floor as sessions (max 200 ft travel)
- [ ] Elevator access if multi-floor (capacity 1,500 lbs minimum)
- [ ] Ramps where steps exist (slope max 1:12)
- [ ] Service animal accommodation (water dish + relief area mapped)

### Hearing accessibility
- [ ] CART (real-time captioning) — booked 14+ days out
- [ ] Listening device (FM / IR loop) — venue provides (verify)
- [ ] ASL interpretation — booked 21+ days out for keynotes + 60+ min sessions
- [ ] AI captioning backup (Otter.ai / AWS Transcribe)

### Visual accessibility
- [ ] Large-print materials (registration form, agenda, signage) — 14+ days out
- [ ] Braille materials (registration confirmation, agenda) — 14+ days out if requested
- [ ] High-contrast signage (WCAG AA 4.5:1 ratio)
- [ ] Audio description for visual-heavy sessions (rare; ask 14+ days out)

### Sensory-friendly
- [ ] Quiet room (low light, low noise, no fragrance)
- [ ] Sensory kit (noise-canceling headphones, fidget objects)
- [ ] Low-stim signage (clear, non-blinking)
- [ ] Reduced-stim session option (one breakout in quiet room)

### Cognitive accessibility
- [ ] Simple-language agenda summary (alternative to dense agenda)
- [ ] Visual schedule (color-coded by track + time)
- [ ] Wayfinding signage (clear, illustrated)

### Compliance documentation
- [ ] Venue ADA self-certification on file (Cvent supplier metadata OR direct from venue)
- [ ] Vendor contracts signed (CART, ASL)
- [ ] Accommodation request log archived (post-event)
- [ ] Incident response plan documented
```

### Recipe 2: Accommodation request capture at registration

Add to registration form (free-text + checkbox):

```markdown
# Registration Accommodation Request

## Do you require any accommodations to fully participate in DevConf 2027?
☐ Yes (please specify below)
☐ No

## If yes, please specify (free-text)
[                                                          ]
[                                                          ]
[                                                          ]

## Specific request types (optional checkboxes)
☐ Wheelchair access
☐ ASL interpretation
☐ CART captioning (real-time text)
☐ Listening device
☐ Large-print materials
☐ Braille materials
☐ Quiet / sensory-friendly room
☐ Dietary accommodation (separate form)
☐ Service animal accommodation
☐ Other (specify above)

## Response timeline
We confirm accommodations within 48 hours and finalize 14 days before the event.

## Day-of contact
Our accessibility lead [Name] will be on-site reachable at [phone] and [email].
```

### Recipe 3: Vendor booking (CART)

```bash
# Email Aberdeen Captioning 14+ days out
mcp tool gmail.send_email \
  --to "services@aberdeen.io" \
  --subject "CART captioning request — DevConf 2027 — Sept 15-17" \
  --body "$(cat <<'EOF'
Hi Aberdeen team,

Booking CART captioning for DevConf 2027 in Chicago, Sept 15-17.

Sessions requiring captioning (28 sessions, 18 hours total):
- Day 1: Keynote (60 min), 3 panels (60 min each), 6 breakouts (45 min each)
- Day 2: 8 breakouts, 1 keynote
- Day 3: 4 workshops (90 min each)

Format: Hybrid (in-person + virtual streaming)
- In-person: caption display screen at front of room (we provide hardware)
- Virtual: caption stream overlay on broadcast (we will integrate)

Content brief: tech / AI / engineering jargon
[Brief attached + speaker bios + technical glossary]

Hours: 18 total, plus 2 hr buffer for transitions
Quote request: please confirm rate + scope by [date]

Looking forward to working with you.

[Sender]
EOF
)"
```

### Recipe 4: Vendor booking (ASL interpretation)

```bash
# Email Sorenson 21+ days out
mcp tool gmail.send_email \
  --to "scheduling@sorenson.com" \
  --subject "ASL interpretation — DevConf 2027 — Sept 15-17" \
  --body "$(cat <<'EOF'
Hi Sorenson team,

Booking ASL interpretation for DevConf 2027 in Chicago.

Sessions requiring ASL (subset of full conference):
- Day 1: Keynote (60 min) + 3 panels (60 min each) = 4 hours
- Day 2: Keynote (60 min) + 4 sessions (45 min each) = 4 hours
- Day 3: 2 workshops (90 min each) = 3 hours
Total: 11 hours

Interpreter team: 2 per session (rotate every 20 min on sessions >60 min)
On-stage placement: in-light, visible from rear of room

Content brief attached: tech / AI / engineering jargon glossary + speaker bios

Quote + interpreter team confirmation by [date]?

Best,
[Sender]
EOF
)"
```

### Recipe 5: AI captioning backup (Otter.ai)

```bash
# As fallback IF CART vendor cancels
mcp tool gmail.send_email \
  --to "support@otter.ai" \
  --subject "Enterprise live captioning — DevConf 2027 backup" \
  --body "Setting up Otter.ai live captioning as backup for primary CART vendor. Sessions list attached. Please confirm Enterprise account access for live captioning + transcript export."

# At session start, launch Otter live captioning
mcp tool otter.start_live_caption \
  --meeting "devconf-keynote-2027-09-15" \
  --audio-source "venue-mixer-output" \
  --display "stream-overlay"
```

### Recipe 6: Materials in alternate format

```bash
# Large-print materials (registration form + agenda)
# Use 18-22pt fonts; high contrast; serif preferred (Garamond, Times)
mcp tool pandoc.convert \
  --input "agenda.md" \
  --output "agenda-large-print.pdf" \
  --pdf-engine "weasyprint" \
  --css "large-print.css"

# Braille materials (request 21+ days out from vendor)
# Vendor: Braille Plus (https://www.brailleplus.net)
mcp tool gmail.send_email \
  --to "info@brailleplus.net" \
  --subject "Braille materials — DevConf 2027" \
  --body "Need Braille version of registration confirmation + agenda + venue map. 2 attendees requesting."
```

### Recipe 7: Sensory-friendly room setup

```markdown
# Quiet Room — Hilton Chicago — DevConf 2027

## Location
Room 218 (off main expo hall, sound-isolated)

## Setup
- Low lighting (lamps; no overhead fluorescent)
- No music
- No fragrance / scented products
- Sensory kit available: noise-canceling headphones, fidget objects, weighted lap pads
- Whiteboard for text-based communication
- Sign: "Quiet Room — Please speak softly"

## Schedule
- Open: 8:00am - 6:00pm Days 1-3
- Monitored by accessibility lead (rotation)

## Sensory-friendly session option
- Workshop on Day 3 in quiet room
- Reduced audience (cap 20)
- Lower stim: no music, no flashing slides, calm pace
```

### Recipe 8: Day-of accessibility execution

```python
# Pre-event preparation
accommodations = notion.query_db('devconf-2027-accommodations')

for req in accommodations:
    # Confirm 14 days out
    if req.confirmed == False:
        mcp_tool('gmail.send_email',
                 to=req.email,
                 subject='Your DevConf accommodation — confirmed',
                 body=render_confirmation(req))
        req.confirmed = True

# Day-of: 30 min before doors
ops_lead.confirm_setup({
    'listening_devices_at_reg': True,
    'cart_display_on_stage': True,
    'asl_interpreter_on_stage': True,
    'quiet_room_open': True,
    'sensory_kit_available': True,
    'large_print_at_reg': 50,
    'braille_at_reg': 2,
    'wheelchair_seating_marked': True
})
```

### Recipe 9: Hybrid event accessibility (in-room + virtual)

```markdown
# Hybrid Accessibility Cue Sheet

## In-room captioning
- CART display: 4x6 ft monitor at front of main stage
- Backup: AI captions via Otter on secondary display
- Sign language interpreter on stage (lit, camera-friendly)

## Virtual stream captioning
- CART captions stream as overlay (AI-Media integration)
- Backup: YouTube auto-captions enabled
- Sign language interpreter visible in virtual stream (dedicated camera + lower-third)

## Virtual attendee accommodations
- Closed captions: configurable in player
- Audio description track: separate stream URL (rare; pre-arrange)
- Sign language: ON by default (overlay on main video)
- Volume + speed controls: standard player

## Reverse accommodation (virtual → in-room)
- If in-room CART fails, switch to virtual feed for captions
- If in-room ASL interpreter unavailable, virtual interpreter overlay via screen
```

### Recipe 10: Post-event compliance documentation

```python
# Archive accommodation requests + responses for compliance
compliance_log = {
    'event_id': 'devconf-2027',
    'total_attendees': 580,
    'accommodation_requests': len(accommodations),
    'requests_fulfilled': sum(1 for a in accommodations if a.fulfilled),
    'requests_unfulfilled': sum(1 for a in accommodations if not a.fulfilled),
    'unfulfilled_reasons': [a.notes for a in accommodations if not a.fulfilled],
    'cart_hours_delivered': 18,
    'asl_hours_delivered': 11,
    'listening_devices_distributed': 7,
    'large_print_materials_distributed': 12,
    'sensory_room_visits': 23,
    'incident_log': [],
    'compliance_status': 'Title III compliant'
}

notion.create_db_row(database='compliance-log', properties=compliance_log)
```

## Examples

### Example A: 600-attendee conference, full accessibility stack

```
Vendor: Aberdeen CART + Sorenson ASL
Cost: $9K total (CART $6K + ASL $3K)
Sessions covered: 28 sessions, 18 hours CART, 11 hours ASL
Accommodation requests received: 14
Sensory room visits: 23 unique attendees
Compliance: Title III compliant; no incidents
Verbatim feedback (NPS): "First conference where I felt fully welcome." — Detractor → Promoter conversion
```

### Example B: Hybrid event, virtual-first captioning

```
In-person: 100 attendees, in-room CART display
Virtual: 800 attendees, caption overlay on stream
CART vendor: 3PlayMedia (integrated via AI-Media stream)
ASL: virtual-only interpreter (overlay on stream); none in-room (no requests)
Cost: $4K total
```

### Example C: Sensory-friendly attendee request

```
Attendee: requests sensory-friendly accommodation
Action:
1. Quiet room assigned (room 218, off main hall)
2. Sensory kit prepared (headphones + fidget + lap pad)
3. Reduced-stim workshop attendance arranged (Day 3)
4. Accessibility lead introduces themselves on Day 1
5. Follow-up post-event with NPS + qualitative feedback
Result: 5-star feedback, requests return for 2028
```

## Edge cases

### Vendor cancellation 7 days out
Primary CART / ASL vendor cancels. Activate backup: AI captioning (Otter) + remote ASL interpreter via Sorenson VRS. Lower quality but legally compliant.

### Multiple ASL dialects
ASL has regional dialects. For international attendees needing different sign language (BSL, JSL, etc.), book specialist provider. Sorenson covers most common.

### Service animal accommodations
Water dish + relief area within 100 ft of venue. Inform housekeeping. Verify venue allows service animals in all areas.

### Quiet room demand exceeding capacity
If multiple attendees need quiet room simultaneously, partition the room OR offer staggered access. Document in capacity plan.

### Caption display visibility
Front-of-room caption monitor must be visible from back row. Use 4x6 ft minimum; high contrast; 24+ pt font.

### Interpreter rotation in long sessions
ASL interpreters rotate every 20 min in 60+ min sessions. Have 2 interpreters per session; brief on hand-off cues.

### Accessibility request received <14 days out
Best effort. Document in incident log. Don't promise what can't be delivered (e.g., Braille materials).

### Title III enforcement
If non-compliance leads to complaint, ADA Title III enforcement via DOJ. Document accommodation requests + responses for legal defense.

### Hybrid stream captioning sync
Virtual attendees' captions may lag in-person captions by 2-3 sec due to stream latency. Acceptable but document.

### Audio description for visual-heavy sessions
Sessions with lots of code-on-screen, charts, or visual demos need audio description (narrator describes visuals). Rare request; build into AV setup.

### Sign language during Q&A
When attendee asks question, interpreter signs the question back to deaf attendees. When deaf attendee asks via sign, interpreter voices it. Two-way comms.

### Vendor cost trade-off
CART ($150-200/hr) vs ASL ($75-100/hr per interpreter; 2 needed) vs AI captioning ($50/event flat). Plan based on attendee request scope.

### Documentation for re-audit
Save vendor invoices + accommodation log for 3 years minimum (ADA compliance lookback period).

### Travel + lodging for accommodation
Some attendees need accessible hotel rooms (roll-in shower, lower fixtures). Coordinate with room block; see `room-block-hotel-partnerships`.

## Sources

- **ADA Title III**: https://www.ada.gov/topics/title-iii/
- **ADA 36.303 (auxiliary aids)**: https://www.ada.gov/regs2010/titleIII_2010/titleIII_2010_regulations.htm#a36303
- **Aberdeen Captioning**: https://www.aberdeen.io
- **3PlayMedia**: https://www.3playmedia.com
- **Caption Mate**: https://captionmate.com
- **Cielo24**: https://cielo24.com
- **AI-Media (Ai-Live)**: https://www.ai-media.tv
- **Sorenson Communications**: https://sorenson.com
- **Purple Communications**: https://www.purple.us
- **KultureCity**: https://www.kulturecity.org
- **Registry of Interpreters for the Deaf**: https://rid.org
- **Otter.ai**: https://otter.ai
- **AWS Transcribe**: https://aws.amazon.com/transcribe/
- **Accessible Arts Design**: https://accessibleartsdesign.org
- **Braille Plus**: https://www.brailleplus.net
