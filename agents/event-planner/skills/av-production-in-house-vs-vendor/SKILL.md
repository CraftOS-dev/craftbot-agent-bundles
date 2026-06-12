<!--
Sources:
- Encore Global: https://www.encoreglobal.com
- Freeman: https://www.freeman.com
- AVT Event Tech: https://avt.com
- ILEA Production Standards: https://www.ileahub.com
-->
# A/V Production (In-House vs Vendor) — SKILL

A/V is 20-40% of event budget and the #1 source of attendee complaints when it fails. This skill is the decision tree (in-house vs venue's in-house vs outside vendor) + RFP workflow + day-of tech specifications.

## When to use this skill

- New event needing AV decision (any in-person or hybrid event)
- Venue mandates in-house A/V at high markup → evaluate outside-vendor pushback
- Multi-room conference needing complex production
- Hybrid event needing simultaneous streaming + in-person production
- Multi-camera live broadcast (keynote with B-roll, panel + audience reaction)
- Recording / post-event content production

**Do NOT use this skill when:**
- Single-room <50 attendee workshop → use venue's house system or DIY (Mac + projector + 2 mics)
- Pure virtual event → use `live-streaming-restream-obs-streamyard` instead
- Sound system only (no projection, no lighting, no streaming) → venue rental sufficient

## Setup

### Tools

- `gmail-mcp` for RFP issuance
- `notion-mcp` for vendor comparison DB
- `docx` for tech rider / spec document
- `pdf` for vendor proposals
- `drawio-mcp` for stage diagram + cable run

### Decision tree inputs

- Attendee count + rooms simultaneous
- Format (in-person / hybrid)
- Recording / streaming requirements
- Lighting requirements (gala + theatrical / standard / minimal)
- Multi-camera needs
- Venue's in-house mandate (often hidden in contract)

## Common recipes

### Recipe 1: AV tier decision tree

```
Tier 1: DIY in-house ($1K-$5K)
─────────────────────────────
- Single room, <50 attendees
- PowerPoint + Mac/PC + 2 wireless mics + projector
- No streaming, no recording
- Acceptable for: small workshops, internal team meetings

Tier 2: Venue's in-house A/V ($5K-$30K)
─────────────────────────────
- Single room, 50-200 attendees
- House sound system + venue's projector + venue's mics
- Basic lighting (existing room lighting)
- Acceptable for: small conferences, summits

Tier 3: Outside mid-tier vendor ($15K-$50K, day rate)
─────────────────────────────────────
- Multi-room, 200-500 attendees
- Encore Global, Freeman, AVT Event Tech, BCS Communications
- Multi-camera basic, lighting design, broadcast quality
- Acceptable for: regional conferences, mid-market summits

Tier 4: Outside enterprise vendor ($50K-$500K, day rate)
────────────────────────────────────────
- Multi-room, 500+ attendees, multi-camera production, lighting design, broadcast quality
- Encore Global, Freeman, ProShow, AVMS
- Custom stages, lighting design, complex broadcast, hybrid streaming
- Acceptable for: tier-1 conferences, mega-events, customer summits
```

### Recipe 2: Venue in-house mandate evaluation

When venue mandates in-house AV (common in hotels):

```python
# Decision matrix
venue_inhouse_quote = 45000   # what venue quoted
market_rate = 18000           # comparable outside vendor quote
total_cost_with_rigging = 23000  # outside + venue rigging fee

if total_cost_with_rigging < venue_inhouse_quote * 0.6:
    # Push hard for outside vendor allowance
    # See venue-contract-negotiation skill, Recipe 6
    pass
elif total_cost_with_rigging < venue_inhouse_quote * 0.8:
    # Outside vendor with rigging fee, marginal savings
    # Weight against integration headache, redundant insurance
    pass
else:
    # Stick with venue in-house; not worth fight
    pass
```

### Recipe 3: Vendor RFP issuance

Generate RFP per these specs:

```markdown
# A/V Production RFP — [Event Name]

## Event details
- Date(s): YYYY-MM-DD
- Venue: [name + address]
- Attendees: [number]
- Format: In-person / Hybrid

## Rooms + capacity
- Main stage: [capacity] (theater seating)
- Breakout A: [capacity] (classroom)
- Breakout B: [capacity] (classroom)
- Networking reception: [capacity] (cocktail / standing)

## Per-room requirements
### Main stage
- Sound: line array PA system + 4 mixers + 6 wireless mics (4 lapel + 2 handheld)
- Visual: 2x rear-projection screens (16:9, 14K lumens minimum)
- Lighting: 8x moving heads + LED uplights + house wash
- Multi-camera: 3 cameras (wide / tight on speaker / audience reaction)
- Recording: ProRes 422 master + H.264 streaming
- Hybrid streaming: HDMI feed to OBS / RTMP push
- Captioning: dedicated caption feed (overlay on stream)

### Breakout rooms
- Sound: room PA + 2 mics + DI for laptop
- Visual: 1x projector (10K lumens, 16:9)
- Lighting: house wash

### Reception
- Sound: portable PA + 2 mics + DJ booth integration
- Lighting: uplights + accent

## Crew + labor
- Stage manager (full day)
- Audio engineer (per room)
- Camera operators (3 for main stage)
- Lighting designer + operator
- Streaming engineer (hybrid only)
- 24-hour setup window required
- Move-out same day as event close

## Hybrid / streaming
- Platform: YouTube Live + RingCentral Events bridge
- Encoder: Hardware (LiveU LU800 4G/5G bonded for redundancy)
- Captioning: vendor-supplied CART feed (overlay)

## Recording deliverables
- Per-session ProRes master (delivered Day +7)
- Per-session H.264 1080p (Day +3)
- Per-session 30-sec teaser (Day +5)

## Insurance
- $2M general liability per occurrence
- Worker's comp per state
- Equipment damage coverage

## Schedule
- Proposal due: YYYY-MM-DD
- Site visit: YYYY-MM-DD
- Decision: YYYY-MM-DD
- Contract signed: YYYY-MM-DD
- Setup: Event date - 1

## Budget envelope
$X,XXX - $XX,XXX

## Contact
[Name + email]
```

Issue to 3-5 vendors:

```bash
mcp tool gmail.send_email \
  --to "sales@encoreglobal.com,sales@freeman.com,sales@avt.com" \
  --subject "RFP — [Event Name] — A/V Production — Q3 2026" \
  --body "$(cat av_rfp.md)" \
  --attachments "stage_diagram.pdf,event_brief.pdf"
```

### Recipe 4: Vendor comparison matrix

```bash
mcp tool notion.create_database --name "av-vendor-comparison" --properties '{
  "Vendor": "title",
  "Total Quote": "number",
  "Day Rate": "number",
  "Labor Hours": "number",
  "Equipment Included": "text",
  "Hybrid Streaming": "checkbox",
  "Recording Format": "select",
  "Insurance": "text",
  "References (similar events)": "text",
  "Site Visit Completed": "checkbox",
  "Strengths": "text",
  "Weaknesses": "text",
  "Recommendation": "select:1st|2nd|3rd|reject"
}'
```

### Recipe 5: Tech rider for speakers (sent 14 days out)

Speakers need to know what's provided. Generate per-speaker tech rider:

```markdown
# Tech Rider — [Speaker Name] — [Event Name]

## What we're providing
- Lapel mic (Shure SM58 wireless) + handheld backup
- Slide clicker (Logitech R400)
- Confidence monitor at front of stage (showing your slides + countdown clock)
- 16:9 1920x1080 projection
- HDMI input for your laptop OR USB-C
- Dedicated audio out for video clips with sound

## What you need to bring
- Your laptop OR USB stick with slide deck (we'll have laptop too as backup)
- HDMI adapter if non-standard port (we have USB-C → HDMI on hand)
- Wireless mouse / clicker (optional; we provide R400)

## Slide format requirements
- 16:9 aspect ratio (1920x1080)
- Font ≥24pt body, ≥36pt headers
- Contrast ratio ≥4.5:1 (WCAG AA)
- No reading from slides

## Tech check window
- [Date + time]
- [Location: green room behind main stage]
- Bring laptop + slides on USB backup

## Day-of contact
- Stage manager: [Name + phone]
- AV lead: [Name + phone]
```

### Recipe 6: Stage diagram (drawio)

```bash
mcp tool drawio.create --name "main-stage-layout" --output stage_layout.drawio \
  --elements '{
    "stage_riser": {"x": 100, "y": 200, "w": 600, "h": 100, "label": "12'\''x16'\'' riser, 18'\'' high"},
    "projector_screen_left": {"x": 50, "y": 50, "w": 280, "h": 160, "label": "RP screen L (14K lumens)"},
    "projector_screen_right": {"x": 470, "y": 50, "w": 280, "h": 160, "label": "RP screen R (14K lumens)"},
    "podium": {"x": 350, "y": 220, "w": 100, "h": 80, "label": "podium + mic"},
    "audio_console": {"x": 700, "y": 350, "w": 100, "h": 60, "label": "FOH audio"},
    "camera_1": {"x": 380, "y": 400, "w": 40, "h": 40, "label": "Cam 1 (wide)"},
    "camera_2": {"x": 100, "y": 350, "w": 40, "h": 40, "label": "Cam 2 (tight)"},
    "camera_3": {"x": 700, "y": 200, "w": 40, "h": 40, "label": "Cam 3 (audience reaction)"}
  }'
```

### Recipe 7: Day-of cue communication

```bash
# Slack channel for AV crew + ops
mcp tool slack.send_message --channel "av-crew-event-2026" \
  --text ":radio: Mic check Stage A in 5 min. All hands."
mcp tool slack.send_message --channel "av-crew-event-2026" \
  --text ":projector: Slides up for keynote in 60 sec. Lower-third: '[Speaker], [Title]'"
```

Use radio comms in addition (audio Sennheiser units; one channel per crew).

## Examples

### Example A: 500-attendee conference, 3-track, hybrid

Tier 3 vendor selection (Encore Global):
- Total quote: $85K for 3-day event
- Includes: 3-room AV, hybrid streaming, multi-cam main stage, basic lighting
- Outside catering allowed (negotiated in venue contract)
- 24-hour setup, same-day teardown
- ProRes recording delivered day +7

### Example B: 200-attendee summit, single track, in-person only

Tier 2 venue in-house ($15K):
- Main stage only
- Venue's house projector + 4 wireless mics
- Basic lighting (room as-is)
- No recording, no streaming
- Saves $25K vs outside vendor, acceptable for tight-budget summit

### Example C: 2000-attendee mega-conference, 5-track, hybrid, multi-cam

Tier 4 enterprise vendor (Encore + Freeman split):
- Total quote: $220K for 3-day event
- Custom stage build, theatrical lighting, multi-cam broadcast
- Dedicated streaming engineer per stage
- LiveU 4G/5G bonded redundancy for remote streams
- Per-session ProRes + H.264 + caption files

## Edge cases

### Venue's house AV is mandatory (no outside vendor allowed in contract)
Negotiate AV-included rate INTO venue contract (reduces line-item; harder to compare). OR walk away if quote is materially above market — see `venue-contract-negotiation` Recipe 6.

### Vendor doesn't support hybrid streaming
Default to OBS Studio + LiveU encoder via in-house IT. See `live-streaming-restream-obs-streamyard` skill. Pair with venue AV for in-room production only.

### Equipment failure day-of
Backup mic + backup laptop + backup HDMI cable + backup projector lamp + analog whiteboard for emergency. Vendor must show backup inventory in proposal.

### Multi-vendor coordination
When using outside production vendor + venue's house sound + dedicated streaming engineer, define cable handoffs explicitly. Hold pre-event tech meeting (vendor + venue + streaming engineer) 24h before.

### Union labor requirements
Some venues (especially in NYC, Chicago, San Francisco) require IATSE or local union labor. Vendor must quote union-rate labor; verify in contract.

### Permits + power
Outdoor events or non-traditional venues may need temporary power (generator) + permits. Add to vendor scope or rent separately.

### Recording rights conflicts
Speakers may not consent to recording (some keynote speakers have "no recording" in contract). Document opt-out at speaker contracting (see `speaker-management-sourcing-prep`).

### Captioning integration
ASL interpreter on dedicated camera with lower-third + CART caption overlay on stream (see `accessibility-ada-captioning-interpretation` for booking). Vendor must accept caption feed from outside CART provider.

### Multi-language interpretation booths
For international events, simultaneous interpretation requires soundproof booths + dedicated audio channels per language + IR receivers for attendees. Add to RFP scope.

### Day-of changes (last-min speaker swap, broken slides)
Stage manager + vendor lead must have direct radio comms with MC + tech runner. Backup slides on USB for every session.

## Sources

- **Encore Global**: https://www.encoreglobal.com
- **Freeman**: https://www.freeman.com
- **AVT Event Tech**: https://avt.com
- **ILEA Production Standards**: https://www.ileahub.com
- **PSAV (now Encore)**: https://www.psav.com
- **InfoComm AV/IT Tech Standards**: https://www.avixa.org
