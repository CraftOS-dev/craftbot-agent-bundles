<!--
Sources:
- Sessionize Conference CFP: https://sessionize.com
- BigSpeak speaker bureau: https://www.bigspeak.com
- All American Speakers Bureau: https://www.allamericanspeakers.com
- Cvent SpeakerHub: https://www.cvent.com/en/event-marketing-management/speakerhub
- DocuSign API: https://developers.docusign.com
- google-flights-mcp: https://github.com/google-flights-mcp
-->
# Speaker Management (Sourcing → Prep → Day-of) — SKILL

End-to-end speaker pipeline: sourcing via Sessionize/bureaus/internal/customer paths → outreach → contracting → travel booking → rehearsal → tech check → day-of execution → post-event follow-up. Speakers ARE the event's content; manage them like the high-value contractors they are.

## When to use this skill

- New event needing 5-50 speakers
- Replacing a no-show speaker (last-minute substitution)
- Re-engaging past speakers for next year
- Multi-track conference needing track-specific subject-matter experts
- Customer summit needing customer speaker stories (defer scheduling to `customer-success`)
- Executive briefing needing C-level speakers (high-touch handling)

**Do NOT use this skill when:**
- Single internal team member speaking (no contracting needed)
- Speaker provided by sponsor (sponsor handles contracting; you handle logistics)
- Event is pure panel format with no individual keynotes (different framing)

## Setup

### Tools

- `firecrawl-mcp` + `brave-search` for speaker research
- `youtube-mcp-transcript` for past-talk research
- `gmail-mcp` for outreach + contracts + travel + day-of comms
- `notion-mcp` for speaker DB (status, contract, travel, prep)
- `zoom-mcp` for rehearsal calls
- `docx` for speaker agreement template
- `google-flights-mcp` for flight search
- `cli-anything` for Amadeus / DocuSign API curl

### Sessionize API

```bash
export SESSIONIZE_TOKEN="<api-key>"

# Base endpoint
# https://sessionize.com/api/v2/
```

## Common recipes

### Recipe 1: Sourcing path decision tree

```
Speaker need → source via:
─────────────────────────────────
Subject-matter technical (devs, engineers) → Sessionize CFP (open) + community direct outreach
Customer story / case study             → Internal customer DB + sales hand-off (defer to customer-success)
C-level executive / industry            → Speaker bureau (BigSpeak / All American / Washington Speakers)
Specialized academic                    → University outreach + Twitter / LinkedIn
Internal employee / leadership          → No sourcing; book direct
Sponsor-provided                        → Sponsor handles selection; you handle prep
Comedian / entertainment                → Bureau (BigSpeak Entertainment / Harry Walker)
Author / thought leader                 → Author's agency (Lavin / APB)
```

### Recipe 2: Sessionize CFP setup (open submission)

```bash
# Create event
curl -X POST https://sessionize.com/api/v2/events \
  -H "Authorization: Bearer $SESSIONIZE_TOKEN" \
  -d '{
    "name": "DevConf 2026",
    "url": "devconf2026",
    "startDate": "2026-09-15",
    "endDate": "2026-09-17"
  }'

# Create CFP
curl -X POST https://sessionize.com/api/v2/events/$EVENT_ID/cfp \
  -d '{
    "title": "Speak at DevConf 2026",
    "description": "We want experts on [topics]. CFP closes [date].",
    "topics": ["AI", "Infra", "Frontend", "DevOps"],
    "sessionLengths": [30, 60, 90],
    "submissionDeadline": "2026-06-30",
    "questions": [
      "Session title (max 80 chars)",
      "Session abstract (max 1500 chars)",
      "What level (beginner / intermediate / advanced)?",
      "Who is your audience?",
      "What's your bio (max 300 chars)?",
      "Have you given a similar talk? Link to video if so."
    ]
  }'
```

### Recipe 3: Direct outreach (custom-targeted)

Research speaker first:

```bash
# Find recent talks / articles
mcp tool brave-search.search --q "<speaker name> talk video 2025"
mcp tool youtube-mcp-transcript.get --video-url "<latest-talk>"
mcp tool firecrawl.scrape --url "<speaker-blog>"
```

Generate personalized pitch:

```bash
mcp tool gmail.send_email \
  --to "<speaker email>" \
  --subject "Career outcome — would [Name] keynote our event?" \
  --body "$(cat <<'EOF'
Hi [Speaker],

I caught your [recent talk title] at [event/podcast] last month — particularly your point about [specific takeaway]. Genuinely shifted my view on [topic].

I'm organizing DevConf 2026 (Sep 15-17, Chicago) — 500 senior engineers + leads from [type companies]. The theme is [theme].

I'd love to invite you for a 30-min keynote on [specific topic angle that ties to their recent thinking].

We cover:
- Speaker fee: $X,XXX
- Round-trip travel + 2 nights at the host hotel
- Recording rights (you keep IP; we own event recording for distribution)

Could we get on a 30-min call to discuss?

Thanks,
[Sender]
EOF
)"
```

### Recipe 4: Speaker contract template

```markdown
# Speaker Agreement — [Speaker Name]

## Event
- Event name: [...]
- Date: [...]
- Venue: [...]
- Audience: [persona + size]

## Speaker commitment
- Session: [Title + topic + length + format]
- Rehearsal: [date + time + medium (Zoom / in-person)]
- Pre-event prep:
  - Deck audit by [date 14 days out]
  - Bio + photo + headshot by [date 21 days out]
- Day-of:
  - Arrival: [time]
  - Mic check: [time]
  - On-stage: [time]
  - Post-session networking until [time]

## Compensation
- Speaking fee: $[amount]
- Travel cap: $[amount] (economy + lodging at event hotel)
- Per diem: $[amount] per day
- Payment terms: Net 30 after event

## Rights
- Recording: Recipient owns all rights to event recording (audio + video)
- Speaker likeness: Granted for event marketing (still images, short clips)
- Speaker IP: Speaker retains IP in slides + content
- Confidentiality: Speaker confirms no NDA conflicts with content shared

## Cancellation
- Speaker cancellation >90 days: full deposit refund
- Speaker cancellation 30-90 days: speaker covers replacement search cost (up to $X)
- Recipient cancellation: per force majeure scope OR full payment

## Signed by:
[Speaker name + date]
[Recipient name + date]
```

Generate + send for DocuSign:

```bash
mcp tool docx.create --output "speaker_agreement_<name>.docx" \
  --content "$(envsubst < speaker_contract_template.md)"

curl -X POST https://demo.docusign.net/restapi/v2.1/accounts/$DS_ACCOUNT_ID/envelopes \
  -H "Authorization: Bearer $DS_TOKEN" \
  -d "{
    \"emailSubject\": \"Speaker Agreement for DevConf 2026\",
    \"documents\": [{\"documentBase64\": \"$(base64 speaker_agreement.docx)\", \"name\": \"agreement.docx\"}],
    \"recipients\": {\"signers\": [{\"email\": \"$SPEAKER_EMAIL\", \"name\": \"$SPEAKER_NAME\", \"recipientId\": \"1\"}]},
    \"status\": \"sent\"
  }"
```

### Recipe 5: Travel + lodging booking

```bash
# Flight search via google-flights-mcp
mcp tool google-flights.search \
  --origin "SFO" \
  --destination "ORD" \
  --departure "2026-09-14" \
  --return "2026-09-18" \
  --class "economy"

# Top result → book via TripActions / Egencia OR direct airline
mcp tool gmail.send_email \
  --to "<speaker email>" \
  --subject "Your DevConf 2026 itinerary" \
  --body "Hi <speaker>, attached is your itinerary..."
```

Itinerary email template:

```markdown
# Your DevConf 2026 itinerary

## Flights
- Outbound: SFO → ORD, Sep 14, AA 1234, depart 9:00am PT, arrive 3:00pm CT
- Return: ORD → SFO, Sep 18, AA 5678, depart 5:00pm CT, arrive 7:30pm PT

## Lodging
- Host hotel: Marriott Marquis Chicago
- Check-in: Sep 14, 3:00pm
- Check-out: Sep 18, 11:00am
- Confirmation #: ABC123
- Room comped under event block

## Ground transportation
- Airport → hotel: Uber (reimbursable, save receipt OR use comp code XYZ)
- Hotel → venue: 5-min walk (mapped below)

## Day-of contact
- Tech runner (your escort): [Name + phone]
- Stage manager: [Name + phone]

## Per diem
- $X/day reimbursable via [process]
```

### Recipe 6: Slide audit (14 days out)

Per speaker:
- Aspect ratio: must be 16:9 (not 4:3)
- Contrast: ≥4.5:1 ratio (WCAG AA)
- Font: ≥24pt body, ≥36pt headers
- No reading from slides (verbal coaching)
- Logo placement consistent with brand kit
- Confidence: tested against actual audience

```bash
# AI-assisted audit
mcp tool pptx.audit --file "speaker_deck.pptx" --checks "aspect_ratio,contrast,font_size,readability"
```

### Recipe 7: Rehearsal (7 days out)

```bash
# Schedule via zoom-mcp
mcp tool zoom.create_meeting \
  --topic "Rehearsal - [Speaker Name] - DevConf 2026" \
  --start_time "2026-09-08T15:00:00Z" \
  --duration 60 \
  --attendees "$SPEAKER_EMAIL,stage-manager@recipient.com,producer@recipient.com"
```

Rehearsal agenda:
1. Time the talk (target length ±2 min)
2. Practice transitions (MC intro / end / handoff)
3. Confirm A/V cues
4. Audience interaction script (if any)
5. Q&A simulation (3-5 anticipated questions)

### Recipe 8: Day-of cue sheet (sent 48h before)

Per speaker, condensed:

```markdown
# Day-of cue sheet — [Speaker Name]

## Pre-session
- Green room arrival: 1 hour before session
- Tech check: 45 min before
- Mic + slides confirmation: 30 min before

## Walk-on
- Cue: applause music + lighting full
- Walk: stage left → center
- MC introduces: [verbatim intro text]
- Lower-third: "[Name], [Title]"
- Slide: title slide

## During talk
- Duration: 30 min (target)
- Cue card at 25 min (5 min remaining)
- Cue card at 28 min (2 min remaining)
- Q&A start: 30 min
- Q&A end: 40 min

## Walk-off
- MC closes: "Thank you, [Name]"
- Lower-third: out
- Music: transition track in
- Lighting: stage-half-down

## Post-session
- Tech runner escort to networking area
- Photo opportunity at sponsor lounge
- Free until [time]
```

### Recipe 9: Post-event speaker follow-up

```bash
# Within 7 days
mcp tool gmail.send_email \
  --to "$SPEAKER_EMAIL" \
  --subject "Thank you + recording from DevConf 2026" \
  --body "Hi <speaker>, thank you for being part of DevConf 2026..."

# Include:
# - Recording link (YouTube unlisted + download link)
# - 1 attendee feedback verbatim (with permission)
# - Per diem reimbursement form (if not already)
# - Invitation to next year's event (optional)
```

## Examples

### Example A: Tech conference, 12 speakers via Sessionize CFP

- CFP open 4 months out
- 180 submissions; 12 accepted via rubric (relevance + speaker quality + topic mix)
- 4 rejected with personalized feedback
- 8 weeks lead time on contract → travel → rehearsal

### Example B: Customer summit, 5 customer speakers + 2 internal execs

- Customer speakers via customer-success hand-off
- Internal execs: direct calendar + slide review
- Lower-key contract (customer logo waiver, no fee)
- Slide audit ensures messaging consistency

### Example C: Industry summit, 3 paid keynote speakers via bureau

- Bureau finder fee: 10-15% of speaker fee
- Speaker fees: $25K-$50K each
- Travel first class on speaker's request
- Greenroom amenities premium
- VIP arrival + dedicated handler

## Edge cases

### Speaker no-show day-of
MC fills with industry anecdote (5 min); transition to next session OR Q&A extension. Comp affected sponsor / attendee value. Post-event: speaker covers replacement cost per contract.

### Speaker requests slide changes mid-event
Have backup laptop with their slides pre-loaded. Speakers should NOT handle their own laptop on stage.

### Speaker visa / international travel
Lead time 8-12 weeks for visa. Some countries refuse business visas for "compensated speaking." Verify with bureau or speaker's counsel.

### Speaker child-care / family travel
Some speakers travel with family. Comp additional rooms (often 1 family member) or stipend. Communicate in contract.

### Speaker dietary restrictions
Comp meals at host hotel OR cover restaurant meals near venue. Brief venue catering on speaker preferences.

### Speaker's slides not received pre-event
Speaker may want to keep slides private. Compromise: speaker uses their own laptop + backup laptop has placeholder + tech runner has thumb drive backup.

### Multi-session speakers
Some speakers do keynote + workshop + panel. Per-session compensation OR bundled package. Slide audit for ALL sessions.

### Bureau vs direct booking
Bureau saves search time + provides insurance against no-show + handles travel. Costs 10-15% premium. Direct booking saves cost but more risk.

### Customer speaker compensation
Usually no fee (customer is excited to speak). Travel + lodging comped. NDA-sensitive content may require speaker review on slide deck.

### Sponsor's executive as speaker
Coordinated through sponsor agreement; no separate speaker contract. But slide review + tech check + rehearsal still mandatory.

### Speaker mental health / break needs
Allow speaker to step out between sessions; designate a tech runner as point of contact for needs. Have backup speaker if speaker can't continue.

## Sources

- **Sessionize**: https://sessionize.com
- **BigSpeak**: https://www.bigspeak.com
- **All American Speakers Bureau**: https://www.allamericanspeakers.com
- **Cvent SpeakerHub**: https://www.cvent.com/en/event-marketing-management/speakerhub
- **DocuSign API**: https://developers.docusign.com
- **google-flights-mcp**: https://github.com/google-flights-mcp
- **Amadeus Travel API**: https://amadeus.com
