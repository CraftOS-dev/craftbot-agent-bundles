<!--
Source: https://sessionize.com/
Papercall: https://www.papercall.io/
Pretalx: https://pretalx.com/
-->
# Conference Speaking Submission — SKILL

CFP discovery + abstract drafting + speaker bio + `playwright-mcp` submission across Sessionize, Papercall.io, Pretalx, and bespoke event forms. Match speaker expertise to event audience. Track speaking calendar in Notion + `google-calendar-mcp`. Pull recordings via `youtube-mcp-transcript` for post-event repurposing.

## When to use this skill

- **Quarterly CFP submission cycle** — submit 5-15 talks per quarter across relevant events.
- **Headliner spot at flagship event** — strategic pitch to a single major conference.
- **Annual conference circuit planning** — pre-plan speaker positioning for next 12 months.
- **Speaker-bench expansion** — multiple execs as speakers; manage assignments.
- **Post-event content harvesting** — pull recording, generate LinkedIn / Substack / blog from talk.

**Do NOT use this skill when:**
- The speaking gig is a podcast — use `podcast-tour-booking-for-execs`.
- The opportunity is a press interview at a conference (not a talk) — use `media-training-spokesperson-prep`.
- The "event" is the company's own conference (defer to marketing/events team).

## Setup

### Sessionize

```bash
# Speaker profile setup at https://sessionize.com
# Most events use Sessionize for CFP management; structured CSV export
export SESSIONIZE_SPEAKER_ID="<id>"
# No public submission API; submit via UI or via event-specific embed
```

### Papercall.io

```bash
# Papercall has API for some events
export PAPERCALL_API_KEY="<key>"
export PAPERCALL_API_BASE="https://www.papercall.io/api/v1"
```

### Pretalx (open-source)

```bash
# Per event Pretalx instance
export PRETALX_INSTANCE="https://pretalx.example-event.com"
export PRETALX_API_KEY="<key>"
```

### CFP discovery sources

```yaml
aggregators:
  - https://sessionize.com/calls-for-speakers
  - https://www.papercall.io/cfps
  - https://callforpapers.lanyrd.com/  # archive, useful for past CFP patterns
  - https://confs.tech/  # tech-focused
  - https://www.dev.events/

industry_specific:
  - https://www.eventscase.com/blog/2026-marketing-conferences-list
  - https://www.saastr.com/saastr-annual/  # SaaS
  - https://www.kdd.org/  # data + AI
  - https://www.usenix.org/conferences  # systems
```

### Notion CFP DB schema

Per CFP:
- `event_name` (text)
- `event_url` (URL)
- `cfp_url` (URL)
- `cfp_platform` (select: Sessionize, Papercall, Pretalx, bespoke)
- `cfp_deadline` (date)
- `event_dates` (date range)
- `location` (text)
- `audience_size` (number)
- `audience_persona` (rich text)
- `topic_themes` (multi-select)
- `track_options` (multi-select)
- `format` (select: keynote, plenary, breakout, panel, lightning, workshop)
- `length_minutes` (number)
- `paid_speaker` (checkbox)
- `travel_covered` (checkbox)
- `submission_status` (select: identified, drafting, submitted, accepted, declined, withdrawn)
- `speaker_assigned` (text)
- `submission_url` (URL)
- `acceptance_status` (select: pending, accepted, waitlist, rejected)

### Speaker-bench DB

Per speaker:
- `name` (text)
- `title` (text)
- `expertise_tags` (multi-select)
- `signature_talks` (multi-text: 5 talks they can give)
- `audience_levels` (multi-select: technical, executive, mixed, beginner)
- `travel_availability` (rich text)
- `prior_speaking_engagements` (multi-text)
- `headshot_url` (URL)
- `bio_short_60w` (text)
- `bio_medium_150w` (text)
- `bio_long_300w` (text)

## Common recipes

### Recipe 1: CFP discovery (firecrawl + Sessionize)

```bash
# Weekly cron: pull open CFPs
firecrawl scrape --url "https://sessionize.com/calls-for-speakers" \
| jq -r '.markdown' \
> sessionize_open.md

# Claude extracts structured CFPs
prompt="Read this CFP page. Output JSON array of {event_name, cfp_url, cfp_deadline, event_dates, location, audience_persona, topic_themes, format_options}. Skip events past deadline."
new_cfps=$(claude --file sessionize_open.md --prompt "$prompt")

# Also Papercall
firecrawl scrape --url "https://www.papercall.io/cfps" | claude --prompt "$prompt" >> new_cfps.json

# Upsert to Notion
echo "$new_cfps" | jq -c '.[]' | while read cfp; do
  notion-mcp upsert_page --db cfp_targets --properties "$cfp"
done
```

### Recipe 2: Match CFPs to speaker bench

```python
# For each open CFP, score match against each speaker
cfps = notion.query(filter={"submission_status": "identified"})
speakers = notion.query(database="speaker_bench")

for cfp in cfps:
  for speaker in speakers:
    score = match_score(cfp, speaker)
    if score > 0.7:
      notion.update(cfp['id'], 
        speaker_assigned=speaker['name'],
        submission_status='drafting'
      )

def match_score(cfp, speaker):
  topic_overlap = jaccard(cfp['topic_themes'], speaker['expertise_tags'])
  audience_fit = audience_match(cfp['audience_persona'], speaker['audience_levels'])
  travel_ok = check_travel_availability(speaker, cfp['event_dates'], cfp['location'])
  return (topic_overlap * 0.5) + (audience_fit * 0.3) + (1 if travel_ok else 0) * 0.2
```

### Recipe 3: Abstract draft per CFP

```python
prompt = f"""
Draft a talk abstract for this CFP.

EVENT: {cfp['event_name']}
AUDIENCE: {cfp['audience_persona']}
TOPIC THEMES: {cfp['topic_themes']}
FORMAT: {cfp['format']} ({cfp['length_minutes']} min)
SPEAKER: {speaker['name']}, {speaker['title']}
SPEAKER EXPERTISE: {speaker['expertise_tags']}
SPEAKER SIGNATURE TALKS: {speaker['signature_talks']}

REQUIREMENTS:
- Talk title (under 80 chars, no buzzwords)
- Abstract (200-400 words depending on event spec)
- 3-5 takeaways for the audience
- Why this speaker (1 sentence credibility hook)

STRUCTURE for abstract:
- Hook: industry context (50 words)
- The problem / question (50 words)
- The talk content: 3 sections (200 words)
- Takeaways (50 words)

NO buzzwords. NO "leverage", "synergize", "best practices". NO sales pitch.
First sentence MUST hook on a SPECIFIC industry moment or data point.
"""
abstract = claude(prompt)
```

### Recipe 4: Submit via Sessionize (web form)

```javascript
// playwright-mcp script
const browser = await playwright.chromium.launch();
const page = await browser.newPage();

// Auth via stored session
await page.context().storageState({ path: 'sessionize_session.json' });
await page.goto(cfp.submission_url);

// Fill title + abstract
await page.fill('input[name="title"]', talk.title);
await page.fill('textarea[name="abstract"]', talk.abstract);
await page.fill('textarea[name="takeaways"]', talk.takeaways);

// Select format + track
await page.selectOption('select[name="format"]', cfp.format);
await page.selectOption('select[name="track"]', cfp.track);

// Upload speaker headshot
await page.setInputFiles('input[name="speaker_headshot"]', speaker.headshot_path);

// Speaker bio
await page.fill('textarea[name="speaker_bio"]', speaker.bio_medium_150w);

// Submit
await page.click('button:has-text("Submit Proposal")');

// Screenshot confirmation
const confirmId = await page.textContent('.confirmation-id');
await page.screenshot({ path: `submissions/${cfp.event_name}_confirmation.png` });

return { event: cfp.event_name, confirmation: confirmId };
```

### Recipe 5: Papercall API submission

```bash
curl -X POST "$PAPERCALL_API_BASE/cfps/$cfp_id/proposals" \
  -H "X-Api-Key: $PAPERCALL_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"$title\",
    \"abstract\": \"$abstract\",
    \"description\": \"$detailed_description\",
    \"tags\": [\"$tag1\",\"$tag2\"],
    \"audience_level\": \"$level\",
    \"speakers\": [{
      \"name\": \"$speaker_name\",
      \"bio\": \"$speaker_bio\",
      \"email\": \"$speaker_email\",
      \"profile_picture_url\": \"$headshot_url\"
    }]
  }"
```

### Recipe 6: Track submission status

```bash
# Check status weekly
for submission in $(notion query 'cfp_targets WHERE submission_status=submitted'); do
  event=$(echo "$submission" | jq -r .event_name)
  platform=$(echo "$submission" | jq -r .cfp_platform)

  case $platform in
    "Papercall")
      status=$(curl "$PAPERCALL_API_BASE/proposals/$(echo $submission | jq -r .proposal_id)" \
        -H "X-Api-Key: $PAPERCALL_API_KEY" | jq -r .state)
      ;;
    "Sessionize")
      # No API; playwright check
      status=$(playwright_check_sessionize.js "$cfp_url")
      ;;
  esac

  if [ "$status" != "submitted" ]; then
    notion-mcp update_row --id $(echo "$submission" | jq -r .id) \
      --acceptance_status "$status"

    if [ "$status" = "accepted" ]; then
      # Auto-schedule prep + travel
      google-calendar-mcp create_event \
        --title "Speaking: $event" \
        --date "$(echo $submission | jq -r .event_dates)"
      slack-mcp send --channel "#speaking" \
        --text "ACCEPTED: $event for $speaker_name on $event_dates"
    fi
  fi
done
```

### Recipe 7: Pre-talk prep

```bash
# 4-6 weeks before event
# 1. Pull prior talks by same speaker for cadence reminder
# 2. Pair with media-training-spokesperson-prep skill for Q&A drill
# 3. Generate slide deck via pptx skill or canva-mcp

# Slide deck structure for 30-min talk
prompt="Generate slide outline for a 30-min talk on '$title'.

ABSTRACT: $abstract
AUDIENCE: $audience
TAKEAWAYS: $takeaways

Outline 12-18 slides:
- 1: Title + speaker
- 2: Hook (the industry moment)
- 3: The problem / question
- 4-10: 3 main sections, 2-3 slides each
- 11-12: Takeaways + call to action
- 13-15: Q&A backup slides (anticipated questions)

For each slide: title + 3-5 bullet talking points + suggested visual."
deck=$(claude --prompt "$prompt")

# Render to pptx
pptx-mcp render --template "speaker_deck.pptx" --content "$deck" --output "$event_deck.pptx"
```

### Recipe 8: Post-talk repurposing

```bash
# After the event, recording usually available on YouTube within 1-4 weeks
# Pull transcript via youtube-mcp-transcript

talk_url="https://youtube.com/watch?v=<id>"
mcp tool youtube-mcp-transcript.get_transcript --url "$talk_url" > talk_transcript.txt

# Generate repurposing assets
prompt="Read this conference talk transcript. Generate:
1. A 1500-word LinkedIn newsletter article based on the talk
2. A 600-word blog post version
3. A 6-tweet thread distilling the takeaways
4. 3-5 quotable moments (15-30 sec each) for video clipping
Output as JSON with separate keys per asset."
repurpose=$(claude --file talk_transcript.txt --prompt "$prompt")

# Queue assets in notion editorial calendar
echo "$repurpose" | jq -c 'to_entries[]' | while read asset; do
  notion-mcp create_page --db editorial_calendar --properties "$asset"
done
```

## Examples — annual speaking program

```yaml
exec: Jane Smith, CEO Acme
goal: 6-10 speaking engagements/year, mix of flagship + tier-2

q1_planning:
  - audit prior year speaking outcomes
  - identify 2-3 flagship targets for year (SaaStr Annual, Web Summit, TechCrunch Disrupt)
  - identify 8-12 tier-2 targets (industry conferences)
  - update speaker bench: signature talks library (5 reusable talks)

quarterly_cycle:
  - cfp discovery cron (Sessionize + Papercall + Pretalx + manual scan)
  - submit 8-15 proposals per quarter
  - target 30-50% accept rate

per_acceptance:
  - calendar holds for travel
  - prep schedule (4-6 weeks before)
  - slide deck (pptx skill + canva-mcp)
  - mock dry-run with PR lead
  - mcp-tts audio drill morning of
  - day-of: bring slides, backup laptop, photo for social

post-talk:
  - youtube-mcp-transcript when recording posts
  - repurposing assets (LinkedIn / blog / Twitter thread / clip)
  - thank-you note to event organizer
  - share recording link with event community
  - update Notion speaker bench with this signature talk
```

## Edge cases

### Most CFPs need lead time (60-180 days)
Flagship events open CFP 6-12 months before the event. Tier-2 events 3-4 months. Build calendar of upcoming CFP openings; don't miss windows.

### Reuse + tailor signature talks
Speakers don't need 50 new talks/year. Maintain 3-5 signature talks; tailor each per CFP. Reuse abstract structure, swap data points for currency, adjust takeaways for audience.

### Travel logistics + cost
Track per-event:
- Travel covered (event pays vs speaker pays)
- Honorarium (yes/no/amount)
- Hotel covered
- Speaker fee waived (industry conferences vs paid)

Notion fields. Calculate cost-per-talk in retrospect.

### Accept ratio realism
Sessionize transparency reports show typical accept rates:
- Tier-1 events: 5-15%
- Tier-2: 20-30%
- Tier-3 / niche: 40-60%

Submit volume = (target talks accepted) / (accept rate). Plan accordingly.

### Single-track vs multi-track formats
Multi-track events accept more talks per slot; single-track is competitive. Adjust submission strategy:
- Multi-track: aim for breakout track that matches expertise
- Single-track: pitch for headliner / plenary; high bar

### Speaker bench expansion
Don't bottleneck on 1-2 speakers. Build bench:
- CEO for industry-level POV
- CTO for technical deep dives
- VP product for product-led GTM
- VP marketing for marketing strategy
- Customer (with permission) for case study sessions

Distribute speaking load + give multiple execs visibility.

### Bio + headshot maintenance
Speaker bios go stale fast. Quarterly audit:
- Update titles + roles
- Add recent press / talks
- Refresh headshot annually (2-year-old headshot is stale)
- 60w / 150w / 300w versions per speaker

### Customer co-presenter
For case-study talks: invite customer as co-presenter. Higher accept rate + customer reference value. Pre-clear via `customer-reference-program-pr`.

### Diversity considerations
Many event organizers track diversity in speaker lineup. Don't only pitch CEO if there are alternative speakers. Diverse speaker lineups also produce stronger talks.

### Recording rights
Some events claim full rights to recordings. Speakers should know:
- Will recording be paywalled or free?
- Can speaker repurpose freely?
- Can speaker post recording on owned channels post-event?

Read event T&Cs. Negotiate if rights are restrictive.

### Cancellation discipline
If event accepts and speaker can't attend, decline within 14 days. Don't no-show; that blacklists the speaker from future CFPs.

### Onsite logistics
Day-of: bring slides on 2 USBs + email + cloud. Bring backup laptop. Tech check 30 min before. Confirm AV setup. Don't rely on event WiFi.

### Cross-promote pre-event
1-2 weeks before:
- LinkedIn post: "Speaking at [event] on [topic]"
- Twitter announcement
- Add to email signature
- Mention in podcast guest spots
- Invite customers to attend

Drives ROI beyond just the speaking slot.

### Post-event measurement
Track per talk:
- Audience size + composition
- Reaction (NPS-style if event surveys)
- LinkedIn mentions during/after
- Press coverage
- Inbound from talk (leads, podcast invites, follow-up speaking)
- Repurposing engagement metrics

Feed into next-year planning.

### Pretalx for open-source / dev events
Pretalx is the open-source CFP system. Most dev conferences use it (FOSDEM, PyCon, etc.). Slightly different fields than Sessionize/Papercall. Per-instance API key.

## Sources

- **Sessionize**: https://sessionize.com/
- **Papercall.io**: https://www.papercall.io/
- **Pretalx**: https://pretalx.com/
- **Confs.tech (CFP discovery)**: https://confs.tech/
- **CallForPapers / Lanyrd archive**: https://callforpapers.lanyrd.com/
- **Sessionize transparency reports**: https://sessionize.com/transparency
- **Playwright**: https://playwright.dev/
- **Speaker bench best practices**: https://www.eventscase.com/blog/2026-marketing-conferences-list
