# Event Planner — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Event format decision tree", "Venue contract redline checklist", "Run-of-show template", "Speaker management playbook", "Sponsor management framework", "BEO catering template", "Accessibility ADA Title III audit", "ROI measurement formula", "Day-of operations playbook", "Post-event distribution playbook", "Crisis / contingency playbook", "MC briefing template", "Emergency action plan template", "SOTA tool reference".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Event formats this agent handles

- **In-person conference** (200-10,000 attendees, multi-day, multi-track, sponsor-funded)
- **In-person summit** (50-300 attendees, single-day, single-track, exec-targeted)
- **In-person workshop** (10-50 attendees, hands-on, training-focused)
- **In-person meetup** (20-200 attendees, community-led, recurring)
- **Hybrid conference / summit** (in-person + virtual simultaneously, networking critical)
- **Virtual webinar** (50-50,000 viewers, single broadcast, low-touch)
- **Virtual conference** (300-10,000 viewers, multi-track + networking + Q&A)
- **Virtual workshop** (10-50 attendees, hands-on, breakout rooms)
- **Roadshow / multi-city tour** (recurring same format, multiple cities)
- **Trade-show booth** (sponsor side; sourcing booth, lead capture, walkable schedule)
- **Customer advisory board** (8-15 exec attendees, retention-focused, sometimes defer to `customer-success`)
- **Awards gala / dinner** (100-500 attendees, social-heavy, AV-heavy)

### Event-management platforms (2026 SOTA, comparison)

- **Cvent** — Enterprise tier ($10K+/year). Full RFP + reg + agenda + sponsorships + room blocks + check-in. Default for large + complex.
- **Bizzabo (Klik)** — Mid-market ($5K-$15K/year). Modern + mobile-first. SmartBadge NFC for lead capture.
- **Splash** — Brand-led ($3K-$10K/year). Best for marketing-led events with brand fidelity. Custom event sites + email + ticketing.
- **Eventbrite** — Consumer high-volume. Free tier + transaction fees. Default for paid public events.
- **RingCentral Events (formerly Hopin)** — Virtual-native ($5K-$15K/year). Best for virtual-first or hybrid.
- **Whova** — Mobile app primary. Affordable ($1K-$5K/year). Community board + agenda + Q&A + matchmaking.
- **Brella** — AI-driven matchmaking ($2K-$8K/year). Best for networking-heavy events.
- **Swapcard** — Combined experience + content + matchmaking. Mid-market.
- **EventMobi** — Branded mid-market alternative. Custom mobile apps.
- **Stova (formerly Aventri)** — Enterprise alt to Cvent. Strong on B2B trade shows.
- **Hubilo** — Indian-headquartered, growing global. Virtual + hybrid.
- **vFairs** — Virtual + hybrid, trade-show focus.
- **Airmeet** — Virtual-native, AI matchmaking.
- **Zuddl** — Hybrid + virtual, enterprise focus.
- **Welcome** — Boutique event experience.

### A/V production tiers

- **In-house basic** ($1K-$5K): PowerPoint Mac + 2 wireless mics + projector. Single room, <50 attendees.
- **In-house mid** ($5K-$20K): Multiple mics + mixing console + 2-3 displays + basic lighting. Single room, 50-200 attendees.
- **Vendor mid** ($15K-$50K, day rate): Encore Global, Freeman, AVT Event Tech. Multi-room, 200-500 attendees.
- **Vendor enterprise** ($50K-$500K, day rate): Encore Global, Freeman, multi-camera production, custom builds, multi-room synchronized streaming.

### Streaming + AV software (2026 SOTA)

- **Cloud studio (no-install)**: Restream Studio, StreamYard, Riverside Studio, Tella
- **Multi-platform broadcast**: Restream, StreamYard (one upload → multiple platforms)
- **Open-source production**: OBS Studio (free, customizable scenes), Streamlabs (OBS fork)
- **Pro multi-cam**: vMix, Wirecast (paid, full broadcast control)
- **Hardware encoders**: LiveU LU800 (4G/5G bonded), Teradek Cube, Haivision Makito
- **Separate-track podcast**: Riverside Studio, SquadCast (now Descript), Zencastr
- **Webinar platforms**: Demio (no-download marketing), Livestorm (evergreen + on-demand), Zoom Events (enterprise hybrid), MS Teams Live Events (internal), Webex Events (enterprise alt), Run The World, Twine, Welcome
- **Low-latency interactive (WebRTC)**: Brella, Swapcard, RingCentral Events, Zoom Events (sub-second latency for Q&A)

### Audience Q&A + interactive

- **Slido** (Cisco) — moderated Q&A + polls + word clouds + word maps. Enterprise tier for API.
- **Mentimeter** — word clouds + interactive polls + presentation embeds.
- **Pigeonhole Live** — enterprise event Q&A.
- **AhaSlides** — low-cost Q&A + polls + quizzes.
- **Wooclap** — education-focused interactive.
- **Kahoot** — quiz-format gamified.

### Speaker + CFP platforms

- **Sessionize** — built for event organizers (CFP, agenda, comm). Default for tech conferences.
- **Papercall** — open-source community events.
- **Pretalx** — open-source CFP + agenda.
- **OnceHub / Calendly / Cal.com** — speaker scheduling for 1:1.
- **OnceHub** — round-robin / team scheduling.

### Speaker bureaus

- **BigSpeak** — generalist, high-budget keynote speakers.
- **All American Speakers Bureau** — broad catalog, mid-budget.
- **Washington Speakers Bureau** — political + business speakers.
- **Harry Walker Agency** — political + thought-leader speakers.
- **APB Speakers** — author + business speakers.
- **The Lavin Agency** — author-focused.

### Accessibility vendors

- **CART captioning**: Aberdeen, 3PlayMedia, Caption Mate, Cielo24, AI-Media (Ai-Live)
- **ASL interpretation**: Sorenson Communications, Purple Communications, Communication Access Center (CAC), local SL agencies
- **Sensory-friendly consulting**: AccessibleArts.org, KultureCity (Sensory-friendly venue certification)
- **AI live captioning fallback**: Otter.ai, Sonix, AWS Transcribe (lower quality than CART)

### Event insurance

- **GatherGuard** (Markel) — short-term event cancellation + general liability
- **Eventsured** — same coverage scope, alt provider
- **Markel Events** — broader portfolio coverage
- **TULIP (Tenant User Liability Insurance Program)** — for nonprofits / one-time events
- **Recipient often has corporate GL** — adds event as additional insured

### Industry organizations (2026 active)

- **MPI (Meeting Professionals International)** — generalist professional org, benchmarks + contracts
- **PCMA (Professional Convention Management Association)** — corporate events focus
- **IAEE (International Association of Exhibitions and Events)** — trade-show focus
- **ILEA (International Live Events Association)** — production / experience focus
- **NACE (National Association for Catering and Events)** — F&B focus
- **CEMA (Corporate Event Marketing Association)** — corporate marketing events

### Conference CFP platforms

- **Sessionize** — default for tech conferences (open + private CFP)
- **Papercall** — open-source community events
- **Pretalx** — open-source, German-led, used by many EU events
- **CFP-app** — open-source GitHub repo (BlackHat-style)

### Promo + swag vendors

- **Swag.com** — modern, mid-market, sustainability options
- **Custom Ink** — full-service, broad catalog, bulk pricing
- **Imprint Direct** — broad catalog, bulk pricing
- **Branded** — modern alt, faster turnaround
- **Sticker Mule** — stickers + small items, premium feel
- **4imprint** — broad catalog, mass market
- **Allbirds + Patagonia** — premium sustainable swag
- **Green Eco Promos** — sustainability-focused

---

## Event format decision tree

Use this when the user asks "should this be in-person, virtual, or hybrid?"

### Step 1: Attendee target + geographic spread

- **<50 attendees, single region** → in-person workshop OR small summit
- **50-300 attendees, single region** → in-person summit OR small conference
- **300-3000 attendees, multi-region** → in-person conference (with travel grant for select attendees) OR hybrid
- **3000-10000 attendees** → in-person mega-conference (with virtual streaming) OR hybrid
- **Global (multi-region required)** → hybrid OR virtual
- **>10000 viewers** → virtual conference OR multi-region hybrid (multiple in-person hubs + virtual)

### Step 2: Business outcome

- **MQL / lead generation** → hybrid (in-person quality + virtual reach) OR virtual webinar
- **Customer retention / customer summit** → in-person summit (defer to `customer-success` for programming)
- **Brand / category leadership** → in-person conference + virtual streaming for reach
- **Revenue (pay-to-attend)** → in-person conference (higher ticket) OR virtual conference (lower ticket)
- **Investor / partner / industry relations** → in-person summit OR hybrid (defer to `bd-partnerships` for relationship work)
- **Talent / recruiting** → in-person career fair OR virtual job fair
- **Education / training** → workshop format (in-person OR virtual depending on hands-on need)

### Step 3: Content density + interactivity

- **Keynote + multi-track, deep technical content** → in-person OR hybrid (virtual loses focus on dense content)
- **Networking-critical (matchmaking, meetings)** → in-person OR hybrid with strong matchmaking platform (Brella)
- **Light keynote + Q&A only** → virtual webinar
- **Workshop with hands-on lab** → in-person OR virtual with breakout rooms

### Step 4: Budget envelope vs format cost

- 2026 cost-per-attendee benchmarks (PCMA + Bizzabo data):
  - **In-person**: $800-$2,500 per attendee (avg ~$1,400)
  - **Hybrid**: $500-$1,200 per attendee (avg ~$900)
  - **Virtual**: $50-$300 per attendee (avg ~$135)
- If budget per attendee is materially below the floor for the chosen format, downgrade format OR cut features (catering, swag, AV tier)

### Step 5: Sponsor revenue dependency

- **>40% of revenue from sponsors** → in-person OR hybrid (sponsor booths + lead capture justify their ticket)
- **<10% sponsor revenue** → format-agnostic
- **In between** → hybrid (sponsor virtual booth + in-person booth)

---

## Venue contract redline checklist

Use this on every venue contract before user signoff.

### F&B (Food + Beverage) minimum
- **Negotiate as FLOOR, not target.** "F&B minimum $25,000" = the venue's guaranteed revenue floor. You'll typically spend MORE than the minimum.
- **Push back on minimum >70% of projected F&B spend.** Venues often set minimums at 100%+ to lock you in.
- **Avoid F&B minimum + room rate minimum.** Pick one, not both.

### Attrition clause (room block)
- **Cap attrition at 80% pickup with sliding scale.** Below 80%, you owe the difference at full rack rate.
- **80-90% pickup**: 0% attrition penalty
- **70-80% pickup**: 25% of unsold rooms × rack rate
- **<70% pickup**: 50% of unsold rooms × rack rate (negotiate; venue usually wants 100%)
- **Always include re-marketing clause:** venue must attempt to re-sell unsold rooms before charging attrition.

### Force majeure clause
- **MUST cover (post-2020):**
  - Pandemic / epidemic / health emergency
  - Civil unrest / riots / public safety
  - Extreme weather (hurricane, blizzard, flooding)
  - Government shutdown (visa restrictions, travel bans)
  - Terrorism
- **Generic "Acts of God" is NOT enough.** Push for explicit named events.
- **Negotiate full refund of deposits if invoked >90 days out.**

### Cancellation schedule
- **Sliding scale based on lead time:**
  - >365 days out: 10% of total contract value (deposit forfeit)
  - 180-365 days: 25%
  - 90-180 days: 50%
  - 60-90 days: 75%
  - <60 days: 100%
- **Push for full refund on extreme weather / force majeure.**

### Outside vendor allowance
- **A/V**: Venue often mandates in-house A/V at 2-3x market rate. Push for outside-vendor allowance.
- **Catering**: Most venues require in-house catering (revenue stream). Push for select outside vendors (kosher, halal, allergy-specific).
- **Décor + floral**: Usually open to outside vendors; confirm.

### Deposit + payment schedule
- **Standard:** 25% on signing / 25% 90 days out / 50% on event date
- **Push for:** 10-15% on signing if relationship is new; refundable to 90 days out

### Insurance + indemnification
- **Mutual indemnification preferred** (each party responsible for own liability)
- **Confirm venue's GL coverage:** $1M-$2M per occurrence minimum
- **Recipient adds event as additional insured** on their own GL policy

### Recording + livestream rights
- **Recipient retains ALL rights to event content** (speakers, sessions, attendee likeness with consent)
- **Venue cannot use recording for marketing without recipient permission**

### Outdoor + transit-dependent contingency
- **Indoor backup plan named**
- **Weather-related cancellation defined** (e.g., NOAA-issued storm warning triggers cancellation; full refund)

---

## Run-of-show template

The run-of-show is the operational layer above the agenda. Print copies for stage manager + AV lead + venue ops + MC.

### Format: 5-column cue sheet

```
| Time | Item | Speaker or Stage | A/V Cue | Notes |
|------|------|------------------|---------|-------|
| 8:00 | Doors open + registration open | Lobby | Music in (background playlist) | Greeters at door, swag pickup, dietary tag visible on badge |
| 8:30 | Coffee + light breakfast | Pre-function room | — | 50 vegan / 30 GF / 5 kosher / 3 halal counts |
| 9:00 | Welcome + house keeping | Main stage / MC | Mics on, slides up, applause music ready | MC: 5 min max, no fluff, transition to keynote |
| 9:05 | Keynote: "Title" | Main stage / Speaker A | Slides up (16:9), mic on lapel + handheld backup, lower-third "Speaker A, Title", music out | 30 min talk + 10 min Q&A via Slido session ABC123 |
| 9:45 | Transition | Main stage | Music in (5 sec fade-in), lighting half-down for stage swap, lower-third out | 10 min for stage swap + speaker change |
| 9:55 | Panel: "Topic" | Main stage / 3 panelists | Slides up (16:9), 4 mics on, lower-third per panelist rotated | Moderator brief: bridge phrases, time keeping |
| 10:30 | Networking break + sponsor coffee station | Pre-function room | Music in, lighting full, audio dampened in main stage | Sponsor coffee (Gold tier) — confirm logo on cups, branded napkins, branded coffee cart |
| 10:50 | Transition warning | All | Bell tone in main stage + announcement: "We resume in 5 minutes" | Ops sweep room for stragglers |
| ...  | ...  | ...              | ...     | ...   |
```

### Cue types

- **Mic on / mic off** — per speaker
- **Slides up / slides out** — per session
- **Lower-third on / lower-third off** — per speaker (name + title)
- **Music in (track) / music out** — transitions, breaks, walk-on, walk-off
- **Lighting** — full, half, stage-only, full-down (between sessions)
- **Camera cut** — for hybrid / multi-cam (wide / tight on speaker / audience reaction)
- **Captioning overlay** — on for hybrid / accessibility-mandated
- **Stream cut** — for hybrid; cut to break slide during transition

### Contingency built in

- **Speaker no-show** — MC fills with industry anecdote (5 min) + transition to next session OR Q&A extension
- **A/V failure** — backup mic + backup laptop + backup slides on USB + analog whiteboard
- **Catering delay** — MC extends Q&A OR adds 10-min intermission
- **Medical emergency** — designated runner contacts EMT (on-site for >300 attendees); MC pauses program if affecting view
- **Fire alarm** — full evac to designated assembly point; MC has pre-written script

### Physical printed binders

- **Stage manager binder**: full run-of-show + emergency action plan + vendor contact tree
- **AV lead binder**: cue sheet + backup tech inventory + IT contacts
- **Venue ops binder**: BEO + catering refresh schedule + room reset cues
- **MC binder**: cue sheet + speaker bios + filler material + emergency scripts

---

## Speaker management playbook

### Step 1: Sourcing

- **Internal speakers (executives, employees)** — preferred for product-related content
- **Customer speakers** — case study + customer story (defer scheduling to `customer-success`)
- **Industry experts** — sourced via Sessionize CFP (open) OR direct outreach
- **Keynote / paid speakers** — sourced via speaker bureau (BigSpeak / All American / Washington Speakers)

### Step 2: Outreach (per pr-comms pattern, adapted)

- **Subject** under 49 chars: "[Specific outcome] — would [Name] keynote our event?"
- **Body** under 200 words:
  - Cite a specific recent talk or article (`firecrawl-mcp` + `youtube-mcp-transcript` for research)
  - Audience demographic + size + business value
  - Compensation + travel coverage + recording rights
  - One ask: "30-min call to discuss?"
- **Personal 1:1 send via `gmail-mcp`** — never bulk

### Step 3: Contracting

Standard speaker agreement (`docx` template + DocuSign API curl):

```markdown
# Speaker Agreement — [Speaker Name]

## Event
- Event name: [...]
- Date: [...]
- Venue: [...]
- Audience: [persona + size]

## Speaker commitment
- Session: [...] (Title + topic + length + format)
- Rehearsal: [date + time + medium]
- Pre-event prep: Deck audit by [date]; bio + photo by [date]
- Day-of: Arrival [time]; mic check [time]; on-stage [time]; post-session networking until [time]

## Compensation
- Speaking fee: $[amount]
- Travel cap: $[amount] (economy + lodging at event hotel)
- Per diem: $[amount] per day
- Net 30 payment after event

## Rights
- Recording: Recipient owns all rights to event recording
- Speaker likeness: Granted for event marketing
- Speaker IP: Speaker retains IP in their slides + content
- Confidentiality: Speaker confirms no NDA conflicts with content shared

## Cancellation
- Speaker cancellation >90 days: full refund of any deposit
- Speaker cancellation 30-90 days: speaker covers replacement search cost
- Recipient cancellation: per force majeure scope OR full payment
```

### Step 4: Travel + lodging

- Book 30 days out (avoid last-minute markup)
- `google-flights-mcp` search; or Amadeus Hotels API
- Lodging at event hotel (room block sub-block for speakers)
- Itinerary email with: flight number + arrival time + driver pickup + hotel address + check-in time + venue address + Day-of contact

### Step 5: Prep

- **14 days out**: Deck audit
  - 16:9 aspect ratio (not 4:3)
  - Contrast ≥4.5:1 (WCAG AA)
  - Font ≥24pt body, ≥36pt headers (visible from back of room)
  - No reading from slides — slides are visuals, speaker carries narrative
  - Audience tested against the actual audience (not generic)
- **7 days out**: Rehearsal via `zoom-mcp` with stage manager + producer
  - Time the talk; cut to length
  - Practice transitions to/from MC, panel
  - Confirm A/V cues
- **24 hours out**: Tech check at venue
  - Walk the stage
  - Mic check (lapel + backup)
  - Slide projection check
  - Lighting check
- **Day-of cue sheet** per speaker (sent 48h before):
  - Green room arrival time
  - Mic check time
  - Walk-on cue (music / lighting)
  - On-stage time
  - Walk-off cue
  - Post-session networking window

### Step 6: Day-of execution

- **Green room** — water, coffee, snacks, charging stations, mic check station
- **Tech runner** — speaker's escort to/from stage
- **Stage manager** — radio comms with AV lead, MC, ops
- **Post-session interview** — capture quote + photo for marketing

---

## Sponsor management framework

### Tier definition (typical SaaS conference, 200-500 attendees)

| Tier | Investment | Deliverables |
|---|---|---|
| **Platinum** | $50K-$100K+ | 30-min keynote slot, premium booth (20×20), 5 attendee passes, branded networking event, attendee list (opted-in), full logo placement (signage, website, app, recordings), post-event report |
| **Gold** | $25K-$50K | 20-min breakout session, premium booth (10×20), 4 attendee passes, sponsored coffee break, prominent logo placement, post-event report |
| **Silver** | $10K-$25K | 10-min lightning talk, standard booth (10×10), 3 attendee passes, logo placement, lead capture access |
| **Bronze** | $3K-$10K | Standard booth (10×10), 2 attendee passes, logo placement, lead capture access |
| **In-Kind** | varies | Coffee bar / lunch / swag bag / charging stations (in exchange for tier-equivalent visibility) |

### Sponsor prospectus (pptx template)

Slides:
1. **Cover** — event name + dates + audience teaser
2. **Audience** — persona + demographic + decision-maker share + spend power
3. **Attendance** — projected + past-event reference + return-attendee rate
4. **Value proposition** — what sponsors gain (brand + leads + relationships + recruiting)
5. **Tier comparison** — table per deliverable
6. **Past sponsors** — logos (with permission)
7. **Investment + ROI** — per-tier cost + benchmark conversion rates
8. **CTA** — call to commit + deadline + contact

### Sponsor outreach (per pr-comms pattern, adapted)

- **Subject** under 49 chars: "[Event name] — [tier] sponsor seat?"
- **Body** under 200 words:
  - Cite a recent business signal (their funding round, product launch, hiring spree)
  - Audience demographic + decision-maker share
  - Tier value-prop with concrete deliverable list
  - Investment + ROI benchmark
  - One ask: "30-min call to discuss?"
- **Attach pptx prospectus**

### Contract → deliverable extraction → tracker

Per signed contract:
- Parse contract for ALL deliverables (logo placement: signage / website / app / email / video; booth size + location; speaker slot; sponsored item; attendee list scope; recording rights; post-event report)
- Create `notion-mcp` DB rows: Deliverable / Tier / Owner / Due Date / Status / Notes
- Weekly digest to sponsor + internal team
- Pre-event sponsor walk-through (booth location, lead capture setup, sponsored item timing)

### Lead handoff (post-event)

- Within 48 hours of event close
- Export leads from event platform (Cvent LeadCapture / Klik / Whova Lead Scanner)
- Format: CSV with attendee name + email + company + title + opt-in confirmation + interaction notes
- Sync to sponsor's CRM via `cli-anything` (HubSpot / Salesforce / Marketo API)
- Email sponsor with summary + CSV + CRM sync confirmation

---

## BEO catering template

Banquet Event Order — finalize 7 days out, lock 72 hours out.

```markdown
# BEO — [Event Name] — [Date]

## Venue + Room
- Venue: [...]
- Room(s): [...]
- Setup: [theater / classroom / banquet rounds / cocktail / mixed]

## Meals
### Day 1 — Continental Breakfast (8:00am-9:00am)
- Total headcount: 200 (locked 72h out)
- Dietary:
  - Standard: 175
  - Vegan: 12
  - Gluten-free: 8
  - Halal: 3
  - Kosher: 2
- Menu: [...]
- Refresh: 8:00 (initial set) + 8:30 (replenish hot items)

### Day 1 — Coffee Break (10:30am-11:00am)
- Sponsored by [Gold sponsor] — branded coffee cart + napkins + signage
- Headcount: 200
- Menu: Coffee + tea + assorted bites
- Refresh: 10:25 set + 10:45 replenish

### Day 1 — Lunch (12:30pm-1:30pm)
- Total headcount: 200 (locked 72h out)
- Dietary:
  - Standard: 175
  - Vegan: 12
  - Gluten-free: 8
  - Halal: 3
  - Kosher: 2 (pre-packaged + labeled)
- Menu: [...]
- Service: [buffet / plated / family-style]
- Refresh: 12:30 set + 1:00 replenish

### Day 1 — Networking Reception (5:30pm-7:30pm)
- Headcount: 200
- Cash bar OR open bar (with consumption cap $X,XXX)
- Hors d'oeuvres: passed + station mix
- Dietary specials available on request

## Allergy notes (free-text from registration)
- Attendee A: tree nut allergy (severe)
- Attendee B: shellfish allergy (mild)
- Attendee C: vegan + soy-free
- [Each handled by chef per allergen protocol]

## A/V + room setup per meal
- Breakfast: house music in pre-function; main stage AV down
- Lunch: house music in main stage; live mic on for emcee announcements
- Reception: ambient music in pre-function; live mic for sponsor introduction

## Service staff requirements
- Breakfast: 4 servers + 1 chef
- Lunch: 6 servers + 1 chef
- Reception: 8 servers + 1 chef + 2 bartenders

## Pricing
- Per-person breakfast: $32
- Per-person lunch: $58
- Per-person coffee break: $18
- Per-person reception (3hr open bar + heavy hors): $95
- Total F&B per attendee: $203
- Total F&B (200 attendees): $40,600
- F&B contractual minimum: $35,000 ✓ exceeded

## Day-of contacts
- Recipient ops lead: [name + phone]
- Venue catering manager: [name + phone]
- Backup: [name + phone]
```

---

## Accessibility ADA Title III audit

Apply on every event, every venue.

### Section 36.303 — Auxiliary Aids and Services

- [ ] **Wheelchair access** to all attendee areas (registration, sessions, dining, restrooms, networking)
- [ ] **Accessible parking** within 50 ft of accessible entrance (1 spot per 25 spots for first 100; sliding after)
- [ ] **Accessible restrooms** within reasonable distance (typically same floor)
- [ ] **Listening device** for hearing-impaired (FM / IR loop) — venue typically provides
- [ ] **Alternate-format materials** (large print, Braille if requested 14+ days out)
- [ ] **Service animal accommodation** (water, relief area)

### CART captioning (real-time captioning)

- [ ] Book Aberdeen / 3PlayMedia / Caption Mate / Cielo24 / AI-Media 14+ days out
- [ ] Provide content brief (industry jargon, speaker names, technical terms) 7 days out
- [ ] Streaming integration confirmed (caption overlay on stream OR separate display)
- [ ] Backup AI captioning (Otter.ai / AWS Transcribe) tested

### ASL interpretation

- [ ] Book Sorenson / Purple Communications / local agency 21+ days out
- [ ] 2 interpreters per session >60 min (they rotate every 20 min)
- [ ] Provide content brief + speaker bios + jargon glossary 7 days out
- [ ] On-stage placement (in light, visible from rear of room)
- [ ] Hybrid: dedicated camera + lower-third on interpreter

### Sensory-friendly

- [ ] Quiet room available (low light, low noise, no fragrance)
- [ ] Sensory kit (noise-canceling headphones, fidgets)
- [ ] Low-stim signage (clear, non-blinking)
- [ ] Reduced-stim session option (e.g., one breakout in quiet room)
- [ ] KultureCity Sensory-Friendly Venue Certification (premium tier)

### Disclosure at registration

- [ ] Accommodation request field (free-text) at reg
- [ ] Response within 48 hours
- [ ] Confirmation 14 days out
- [ ] Day-of contact named for emergent requests

---

## ROI measurement formula

### Cost per attendee
```
Total event cost / Registered attendees = Cost per attendee
```
2026 benchmarks (PCMA + Bizzabo):
- In-person: $800-$2,500 (avg $1,400)
- Hybrid: $500-$1,200 (avg $900)
- Virtual: $50-$300 (avg $135)

### MQL per event
```
MQLs (event source) / Registered attendees = MQL rate
```
Pull from HubSpot / Salesforce / Marketo via `cli-anything`. MQL rate benchmark: 20-30% for in-person, 10-15% for virtual.

### Pipeline-influenced revenue
```
Revenue from opportunities with event in attribution path (within 90/180/365 days) = Pipeline-influenced revenue
```
Multi-touch attribution:
- **90-day window**: short-cycle deals influenced by event
- **180-day window**: typical B2B sales cycle
- **365-day window**: enterprise sales cycle

### ROI formula
```
(Pipeline-influenced revenue - Total event cost) / Total event cost = ROI %
```
Benchmark: 3-5x ROI is typical for well-executed conferences; 8-15x for high-conversion event types (CSO summits, customer-only).

### Engagement score (in-event)

Composite of:
- Session attendance rate (sessions attended / sessions available)
- Q&A participation rate (questions asked or upvoted / attendees)
- Networking connections (meetings booked or scheduled via app / attendees)
- Sponsor booth visits / attendees
- App usage rate (logged in / registered)

Benchmark: >60% session attendance, >40% Q&A engagement, >30% networking, >70% sponsor visits.

### NPS measurement

- Delighted API or Typeform 48h post-event
- Question: "How likely are you to recommend [Event Name] to a colleague?" 0-10 scale
- NPS = % Promoters (9-10) - % Detractors (0-6)
- Benchmark: >50 is strong; >70 is exceptional

### ROI report structure

```markdown
# [Event Name] ROI Report — [Month, Year]

## Executive summary
- Registered: X / attended: Y (attendance rate Z%)
- NPS: N (vs target M)
- Pipeline-influenced revenue: $X (vs cost $Y; ROI Z%)
- MQLs: X (rate Y%)
- Notable wins + losses

## Cost breakdown
- Venue + AV: $X (Y%)
- Catering + F&B: $X (Y%)
- Speaker fees + travel: $X (Y%)
- Marketing + promo: $X (Y%)
- Swag + signage: $X (Y%)
- Sponsorship revenue: -$X (offset)
- Net cost: $X
- Cost per attendee: $X

## Performance vs targets
- Attendance: X / target Y (Z% achievement)
- NPS: X / target Y
- MQLs: X / target Y
- Pipeline: $X / target $Y

## Vendor performance ratings
- [Vendor name]: [rating + notes]
- [...]

## Sponsor satisfaction
- Per-tier survey results
- Renewal likelihood per sponsor

## Attendee feedback themes
- Top 3 positive themes (with verbatims)
- Top 3 critical themes (with verbatims)
- Verbatims for marketing reuse (with permission)

## Recommendations for next event
- [Continue]
- [Change]
- [Discontinue]
```

---

## Day-of operations playbook

### 24 hours before event

- [ ] Walk-through with venue + AV + security + ops (in-person OR virtual + video)
- [ ] Confirm catering BEO + 72h count lock submitted
- [ ] Confirm all speakers checked in (or arriving morning-of)
- [ ] Confirm AV tech check completed
- [ ] Print run-of-show binders + emergency action plan + vendor contact tree
- [ ] Confirm accessibility services in place (CART + ASL + listening device)
- [ ] Test all platforms end-to-end (event app, registration check-in, Q&A platform, streaming if hybrid)
- [ ] Set check-in queue alert thresholds (>5 min wait → `slack-mcp` alert)
- [ ] Confirm photographer + videographer arrival time + shot list
- [ ] Confirm sponsor booth setup time + sponsor walk-through

### Morning of event

- [ ] AV tech check 2 hours before doors
- [ ] Catering setup 1 hour before breakfast service
- [ ] Sponsor booth setup 2 hours before doors
- [ ] Speaker green room ready 1 hour before first session
- [ ] Registration check-in tech check 30 min before doors
- [ ] Photographer in position 30 min before doors

### During event — real-time monitoring

- **Check-in queue depth** via `cli-anything` polling platform API every 60s → `slack-mcp` ops alert if queue >50 OR wait >5 min
- **Session attendance** tracked per session for capacity planning + sponsor reporting
- **Q&A participation** via Slido / Pigeonhole moderation queue
- **Networking** matchmaking nudges via Brella / Swapcard
- **Dietary specials** real-time alert if late attendee with allergy adds
- **Vendor coordination** via `slack-mcp` ops channel (catering refresh timing, AV cue triggers, photographer shot reminders)

### Emergency response

- **Medical** — designated EMT on-site for >300 attendees; MC pauses program if affecting view; escort to private area
- **Fire alarm** — full evac to designated assembly point; MC has pre-written script; head count at assembly point
- **Active threat** — venue lockdown protocol per venue security plan; comms tree triggered
- **Power outage** — backup mic + backup laptop; MC fills with anecdote; venue facility lead resolves
- **AV failure** — backup mic + analog whiteboard; MC fills with Q&A extension OR networking break

### End of event

- [ ] Teardown timing per run-of-show
- [ ] Speaker thank-you photo opportunity
- [ ] Sponsor lead capture data export
- [ ] Lost & found logged
- [ ] Vendor checkout + final payments authorized
- [ ] Photographer + videographer final upload schedule confirmed

---

## Post-event distribution playbook

### Within 24 hours

- Thank-you email to ALL attendees (segmented by tier: speaker / sponsor / VIP / general)
- Thank-you email to speakers (with photo from event + recording link teaser)
- Thank-you email to sponsors (with lead capture summary + recording teaser)
- Internal team post-event hand-off + initial highlights

### Within 48 hours

- NPS survey via Delighted to ALL attendees
- Qualitative feedback survey (top 3 highlights + top 1 critique) via Typeform
- Photo highlights to social media via `marketing-agent` hand-off
- Press release / earned media if newsworthy via `pr-comms` hand-off

### Within 7 days

- Recording upload to YouTube via `youtube-mcp` (per session)
- Whisper transcription per session
- Photos delivered to attendees (Pixieset / SmugMug client gallery)
- Slides delivered to attendees (with speaker permission)
- Sponsor lead handoff complete (CSV + CRM sync)
- Speaker honorarium + travel reimbursement processed

### Within 14 days

- ROI report drafted (cost per attendee + MQL + pipeline-influenced revenue)
- Vendor performance ratings drafted
- Post-mortem doc with ops team
- Attendee feedback themes analyzed
- Verbatim quotes captured for marketing (with permission)

### Within 30 days

- ROI report finalized + circulated to executive team
- Renewal conversations with sponsors initiated (via `bd-partnerships`)
- Customer-event reference program activated (via `customer-success`)
- Marketing repurposing: blog series, social cascade, podcast episodes via `marketing-agent`
- Speaker engagement for next event initiated (with feedback from rating)

---

## Crisis / contingency playbook

### Speaker no-show

- MC fills with industry anecdote (5 min)
- Transition to next session OR Q&A extension
- Apologize publicly only if attendee impact is material
- Sponsor of no-show speaker session: post-event reach-out with mitigation

### A/V failure (mic, slides, projection)

- Backup mic (lapel + handheld + 2 spares per stage)
- Backup laptop (with all decks pre-loaded)
- Backup slides on USB
- Analog whiteboard for emergency

### Catering failure (delay, wrong count, allergy incident)

- Allergy incident: notify medical + isolate dish + label new dish
- Wrong count: communicate to venue immediately; negotiate replacement OR refund
- Delay: MC extends Q&A; ops investigates; communicate ETA to attendees

### Technology failure (registration, streaming, app)

- Registration: manual badges from backup printer OR generic badge + manual log
- Streaming: backup stream key + backup encoder; producer escalates to platform support
- App: paper agenda fallback (always have 50 printed copies); session capacity managed manually

### Weather contingency (outdoor / transit risk)

- **72h out**: Forecast check; trigger indoor backup planning if needed
- **48h out**: Decision tree — outdoor / hybrid / indoor only
- **24h out**: Final decision communicated; transit advisory if needed
- **Day-of**: Real-time NOAA monitoring; cancellation if storm warning issued; full refund per force majeure

### Public health incident (food poisoning, infectious disease, viral outbreak)

- Notify local public health department
- Isolate affected attendees / area
- Comms tree to all attendees within 4 hours
- Defer to `pr-comms` for crisis comms
- Defer to `operations-agent` for insurance claim

### Media / PR crisis (controversial speaker, attendee misconduct, sponsor blowback)

- Defer to `pr-comms` for crisis comms (per their 24/48/72-hour playbook)
- Pause comms until guidance from PR
- Recipient legal + executive sign-off on response

---

## MC briefing template

Send to MC 48 hours before event.

```markdown
# MC Brief — [Event Name] — [Date]

## Audience
- Persona + size
- Tone expectation: [formal / conversational / playful]

## MC role
- Welcome + housekeeping (5 min max)
- Session transitions (30-60 sec each)
- Audience engagement (filler if needed)
- Emergency scripts (fire, medical)
- Sponsor mentions per script

## Speakers
- [Per speaker]: bio + 1-sentence intro + ask
- Specific filler content per speaker if Q&A runs short

## Run-of-show
- [Attached as `xlsx` + physical binder]

## Sponsor mentions per script
- [Verbatim sponsor mention text per timing]

## Filler material
- Industry anecdote 1: [...]
- Industry anecdote 2: [...]
- Audience interaction prompt 1: [...]
- Audience interaction prompt 2: [...]

## Emergency scripts
- Fire alarm: "Please follow staff to the [exit] in [direction]; we'll resume once cleared."
- Medical: "We have a momentary pause; please remain in your seats; we'll resume shortly."
- Technical: "We're resolving a brief technical issue; thank you for your patience."

## Day-of contacts
- Ops lead: [name + phone]
- Tech runner (your escort): [name + phone]
- Stage manager: [name + phone]

## Rehearsal
- [Date + time + medium (in-person OR `zoom-mcp`)]
```

---

## Emergency action plan template

Required by venue + venue safety officer / fire marshal sign-off.

```markdown
# Emergency Action Plan — [Event Name] — [Venue]

## Designated Personnel
- Event Director: [name + phone]
- Safety Officer: [name + phone]
- Venue Facility Lead: [name + phone]
- First Aid / EMT Lead: [name + phone]
- Comms Lead: [name + phone]

## Assembly Points (Evacuation)
- Primary: [location] — [distance from venue]
- Alternative: [location] — [distance]
- Wheelchair-accessible: [location]

## Comms Tree
- Detector → Safety Officer → Venue Facility Lead + MC + Event Director
- Event Director → Comms Lead → press / public if needed (defer to `pr-comms`)

## Per Scenario Response

### Fire / Smoke
1. Verify with venue facility lead
2. Activate fire alarm
3. MC reads evacuation script
4. Staff direct attendees to nearest exit + assembly point
5. Head count at assembly point
6. Wait for venue fire marshal all-clear

### Medical Emergency
1. Notify EMT Lead immediately
2. Clear area around attendee
3. EMT triages; calls 911 if needed
4. MC pauses program if affecting view
5. Document incident; notify recipient legal

### Active Threat
1. Venue lockdown per venue security plan
2. Comms tree triggered
3. Defer to venue security + law enforcement
4. Post-incident: comms via `pr-comms`

### Severe Weather
1. NOAA storm warning triggers protocol
2. MC reads shelter-in-place script
3. Direct attendees away from windows
4. Wait for all-clear from venue facility

### Power Outage
1. Backup mic + analog whiteboard
2. MC fills with anecdote or Q&A
3. Venue facility lead resolves
4. Resume per timing
```

---

## SOTA tool reference (June 2026)

This section is grep-only — the agent uses keyword-driven retrieval to surface the right skill pack for the user's task. Headings are intentionally search-friendly. Every entry links to a detailed `SKILL.md` in `skills/` that ships in this bundle and loads on demand.

**Full coverage map:** see `reference/SOTA_USE_CASES.md` for the per-use-case mapping and confidence rating.

### Cvent Supplier Network + venue sourcing

Cvent Supplier Network is the SOTA hospitality marketplace (300K+ venues globally). Cvent Venue Sourcing API issues RFPs programmatically; proposals returned via API + dashboard. Filter by city + capacity + AV + accessibility + dates + room block need.

- **Skill:** `skills/venue-sourcing-cvent-splash-bizzabo/SKILL.md`
- **Endpoint:** `https://api-platform.cvent.com/v1/venues/...`
- **Auth:** OAuth → `CVENT_API_TOKEN`
- **Key calls:** `search_venues`, `create_rfp`, `get_proposals`, `compare_proposals`
- **Source:** https://www.cvent.com/en/event-marketing-management/venue-sourcing-software

### Bizzabo Venue Concierge + Klik SmartBadge

Bizzabo Venue Concierge (included in Bizzabo subscription) for mid-market venue sourcing. Klik SmartBadge NFC for lead capture at sponsor booths — integrates directly with HubSpot / Salesforce / Marketo for lead sync.

- **Skill:** `skills/venue-sourcing-cvent-splash-bizzabo/SKILL.md`
- **Endpoint:** `https://api.bizzabo.com/...`
- **Auth:** OAuth → `BIZZABO_TOKEN`
- **Source:** https://www.bizzabo.com + https://www.bizzabo.com/klik

### Splash event marketing platform

Splash for brand-first event sites (mid-market marketing-led events). REST API for event creation + brand kit upload + ticketing + reg + email. Best for events where the brand visual matters more than the registration depth.

- **Skill:** `skills/attendee-registration-cvent-eventbrite-splash/SKILL.md`
- **Endpoint:** `https://api.splashthat.com/v1/...`
- **Auth:** API key → `SPLASH_API_KEY`
- **Source:** https://splashthat.com

### Eventbrite consumer ticketing

Eventbrite for consumer high-volume ticketing (free + paid public events). Free tier + transaction fees. Default for paid public events with high volume + low-touch reg.

- **Skill:** `skills/attendee-registration-cvent-eventbrite-splash/SKILL.md`
- **Endpoint:** `https://www.eventbriteapi.com/v3/...`
- **Auth:** OAuth → `EVENTBRITE_TOKEN`
- **Source:** https://www.eventbrite.com/platform/api

### RingCentral Events (formerly Hopin)

RingCentral Events for virtual-native + hybrid events. Best for events where networking + low-latency interaction matter (virtual networking, hybrid Q&A bridge). Acquired by RingCentral 2024; API still active.

- **Skill:** `skills/hybrid-event-low-latency-interaction/SKILL.md`
- **Endpoint:** `https://hopin.com/api/v1/...`
- **Auth:** API key → `HOPIN_TOKEN`
- **Source:** https://hopin.com/developers

### Whova event app

Whova for affordable mobile-app-primary events. Attendee directory + agenda + Q&A + community board + matchmaking. Lower price point than Cvent / Bizzabo for events <500 attendees.

- **Skill:** `skills/event-app-whova-brella-bizzabo/SKILL.md`
- **Endpoint:** `https://whova.com/api/v1/...`
- **Auth:** API key → `WHOVA_TOKEN`
- **Source:** https://whova.com/api

### Brella AI matchmaking

Brella for AI-driven networking. Interest taxonomy + meeting scheduling + interest-based intros. Best for events where 1:1 meetings are a primary driver of value (trade shows, customer summits).

- **Skill:** `skills/virtual-networking-brella-swapcard/SKILL.md`
- **Endpoint:** `https://api.brella.io/v1/...`
- **Auth:** API key → `BRELLA_TOKEN`
- **Source:** https://brella.io

### Swapcard event experience

Swapcard combines event experience + content + matchmaking. Mid-market alternative to Brella with stronger content + agenda integration.

- **Skill:** `skills/virtual-networking-brella-swapcard/SKILL.md`
- **Endpoint:** `https://api.swapcard.com/...`
- **Auth:** OAuth → `SWAPCARD_TOKEN`
- **Source:** https://www.swapcard.com

### Sessionize CFP platform

Sessionize is the SOTA conference CFP platform — built specifically for event organizers (private + public CFPs). Open APIs for CFP creation + abstract submission + agenda generation + speaker comm.

- **Skill:** `skills/speaker-management-sourcing-prep/SKILL.md` + `skills/conference-cfp-cfs-track-design/SKILL.md`
- **Endpoint:** `https://sessionize.com/api/v2/...`
- **Auth:** API key → `SESSIONIZE_TOKEN`
- **Key calls:** `create_event`, `create_cfp`, `list_submissions`, `set_agenda`
- **Source:** https://sessionize.com

### Slido Q&A + polls (Cisco)

Slido for moderated Q&A + live polls + word clouds. Enterprise tier required for full API access. Best for events where Q&A is high-stakes (executive briefings, customer summits) and moderation is mandatory.

- **Skill:** `skills/q-and-a-mgmt-slido-pigeonhole/SKILL.md`
- **Endpoint:** `https://api.slido.com/v1/...` (Enterprise tier)
- **Auth:** API key → `SLIDO_TOKEN`
- **Source:** https://www.slido.com/api

### Restream + StreamYard + Riverside

Cloud-based streaming for single-cam virtual events. Restream is multi-platform broadcast default. StreamYard is browser-based (no install). Riverside Studio captures separate-track local recording per speaker (for post-event podcast).

- **Skill:** `skills/live-streaming-restream-obs-streamyard/SKILL.md`
- **Endpoint:** `https://api.restream.io/v2/...`
- **Auth:** OAuth → `RESTREAM_TOKEN`
- **Source:** https://restream.io + https://streamyard.com + https://riverside.fm

### OBS Studio (open broadcast)

OBS Studio (free, open-source) for hybrid multi-cam production. Custom scenes + transitions + per-track audio. Pair with LiveU encoder (4G/5G bonded) for remote venue with unreliable internet.

- **Skill:** `skills/live-streaming-restream-obs-streamyard/SKILL.md`
- **Install:** `cli-anything` brew install (mac) OR apt-install (linux) OR Windows installer
- **Source:** https://obsproject.com

### Demio / Livestorm / Zoom Events webinar production

Webinar platform decision tree:
- **Demio** — marketing webinars, no-download, simple
- **Livestorm** — evergreen + on-demand
- **Zoom Events** — enterprise hybrid + branded
- **MS Teams Live Events** — internal company webinars
- **Webex Events** — enterprise alt

- **Skill:** `skills/live-streaming-restream-obs-streamyard/SKILL.md` (covers webinar platforms too)
- **Source:** https://demio.com + https://livestorm.co + https://www.zoom.us/events

### Aberdeen / 3PlayMedia CART captioning

CART (Communication Access Realtime Translation) captioning is the SOTA accessibility provision for hearing-impaired attendees. Book Aberdeen / 3PlayMedia / Caption Mate / Cielo24 / AI-Media 14+ days out. Streaming integration required for hybrid events.

- **Skill:** `skills/accessibility-ada-captioning-interpretation/SKILL.md`
- **Source:** https://www.aberdeen.com + https://www.3playmedia.com

### Sorenson / Purple ASL interpretation

ASL (American Sign Language) interpretation for deaf attendees. Book Sorenson Communications / Purple Communications / local SL agency 21+ days out. Two interpreters per session >60 min (they rotate every 20 min). On-stage placement in light, visible.

- **Skill:** `skills/accessibility-ada-captioning-interpretation/SKILL.md`
- **Source:** https://sorenson.com + https://www.purple.us

### Delighted NPS measurement

Delighted (Qualtrics-owned) for NPS surveys. API for survey triggering + result aggregation. Send 48 hours post-event. Alt: Typeform (more design flexibility, less NPS-specific).

- **Skill:** `skills/event-analytics-engagement-nps/SKILL.md`
- **Endpoint:** `https://api.delighted.com/v1/...`
- **Auth:** API key → `DELIGHTED_TOKEN`
- **Source:** https://delighted.com

### Whisper transcription (open source)

OpenAI Whisper for transcription of session recordings. Free + open source via `cli-anything` (`uvx openai-whisper`). Higher accuracy on conference speech than free alts; comparable to Rev / Trint at $0 cost.

- **Skill:** `skills/post-event-recordings-distribution/SKILL.md`
- **Install:** `cli-anything` `uvx openai-whisper recording.mp4 --model large-v3`
- **Source:** https://openai.com/research/whisper

### YouTube + Vimeo recording distribution

YouTube (via `youtube-mcp`) for free public recording distribution. Vimeo for premium / gated content. Both expose APIs for bulk upload + metadata + playlist organization.

- **Skill:** `skills/post-event-recordings-distribution/SKILL.md`
- **MCP:** `youtube-mcp` + `youtube-mcp-transcript`
- **Source:** https://www.youtube.com

### Swag.com + Custom Ink swag sourcing

Swag.com (modern, mid-market, sustainability options) + Custom Ink (full-service, broad catalog). Both expose quote APIs for bulk orders. Drop-ship to venue OR pre-event mail to virtual attendees.

- **Skill:** `skills/gift-bag-swag-sourcing/SKILL.md`
- **Source:** https://swag.com + https://www.customink.com

### Stripe paid registration

Stripe for paid event registration. PCI-compliant + supports tiered pricing (early bird / regular / late / VIP / sponsor pass) + group discounts + refund handling.

- **MCP:** `stripe-mcp` (in agent.yaml)
- **Source:** https://stripe.com

### Twilio SMS reminders

Twilio for day-of SMS reminders to attendees + speakers + vendors. 1,400+ API endpoints. Use for: venue arrival reminder, session start ping, sponsor meeting confirmation, emergency notification.

- **MCP:** `twilio-mcp` (in agent.yaml)
- **Source:** https://www.twilio.com

### OpenWeatherMap weather contingency

OpenWeatherMap API for 72/48/24h forecast monitoring. Trigger weather contingency comms when storm warning crosses threshold. Free tier sufficient for single event; paid for ongoing event-program use.

- **MCP:** `openweathermap-mcp` (in agent.yaml)
- **Source:** https://openweathermap.org/api

### drawio floor plans + booth layout

drawio (free, open-source) for floor plan + sponsor booth layout. Embeddable diagrams + collaborative editing. Cvent Floor Plan Builder is the paid alt (better venue-template library).

- **MCP:** `drawio-mcp` (in agent.yaml)
- **Source:** https://www.drawio.com

### Postgres analytics warehouse

`postgresql-mcp` for event analytics warehouse + alert table. Use for: cross-event ROI comparison, vendor rating history, sponsor satisfaction trend, attendee return rate, MQL conversion attribution.

- **MCP:** `postgresql-mcp` (in agent.yaml)

### PostHog reg page funnel tracking

`posthog-mcp` for event website + reg page funnel tracking. HogQL for: landing page conversion rate, reg form abandonment, paid social → reg attribution, AEO referrer share.

- **MCP:** `posthog-mcp` (in agent.yaml)

### Notion event hub + DBs

`notion-mcp` is the SOTA event hub: speaker DB + sponsor DB + run-of-show + BEO tracker + deliverable tracker + venue history + vendor ratings + post-mortem doc. All other tools sync to Notion as source of truth.

- **MCP:** `notion-mcp` (in agent.yaml)

### Slack ops alerts

`slack-mcp` for day-of ops alerts: check-in queue depth, dietary special add, AV cue trigger, vendor delay, weather threshold cross. Dedicated ops channel for event week.

- **MCP:** `slack-mcp` (in agent.yaml)

### Canva + Figma + imagegen design

`canva-mcp` for branded signage + name badges + social cards templates. `figma-mcp` for brand-system fidelity check + sponsor logo export. `imagegen-mcp` / `stability-ai-mcp` for AI image gen (speaker headshots fallback, social cards, signage variants).

- **MCPs:** `canva-mcp`, `figma-mcp`, `imagegen-mcp`, `stability-ai-mcp` (in agent.yaml)

### DeepL multi-language for international events

`deepl-mcp` for high-quality translation of registration emails, signage, accessibility comms for international events. Multi-language email + content workflow: source EN → translate per target language → store as per-language templates.

- **MCP:** `deepl-mcp` (in agent.yaml)

### Gmail + Outlook + Zoom + Teams coordination

`gmail-mcp` + `outlook-mcp` for speaker / sponsor / vendor outreach. `zoom-mcp` for rehearsals + vendor walk-throughs + Zoom Events webinars. `ms-teams-mcp` for recipients on Microsoft side + Teams Live Events internal.

- **MCPs:** `gmail-mcp`, `outlook-mcp`, `zoom-mcp`, `ms-teams-mcp` (in agent.yaml)

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Should this be in-person, virtual, or hybrid?" | `event-format-selection-in-person-virtual-hybrid` | Apply decision tree per audience + budget + content density |
| "Find me a venue for 500 attendees in Chicago in March" | `venue-sourcing-cvent-splash-bizzabo` | Cvent Supplier Network RFP via `cli-anything` |
| "Help me redline this venue contract" | `venue-contract-negotiation` | MPI redline checklist; F&B floor + attrition + force majeure + cancellation |
| "Set up registration for our conference" | `attendee-registration-cvent-eventbrite-splash` | Platform decision matrix first; then config |
| "Build the run-of-show" | `agenda-run-of-show-authoring` | 5-column cue sheet in `notion-mcp` + `xlsx` export |
| "Source 5 keynote speakers" | `speaker-management-sourcing-prep` | Sessionize / bureau / direct outreach; episode-cited pitch |
| "Set up our sponsorship program" | `sponsor-tier-deliverable-tracking` | Tier definition (Bronze/Silver/Gold/Platinum); prospectus; deliverable tracker |
| "Stream the event live" | `live-streaming-restream-obs-streamyard` | Decision tree: cloud vs OBS vs enterprise platform |
| "What's the run-of-show for hybrid Q&A?" | `hybrid-event-low-latency-interaction` | WebRTC platform (RingCentral Events / Brella / Swapcard); captioning overlay |
| "Book CART captioning + ASL interpretation" | `accessibility-ada-captioning-interpretation` | Aberdeen + Sorenson booking 14-21 days out |
| "Plan catering for 200 attendees" | `catering-coordination-dietary-allergy` | Dietary capture at reg → BEO 7 days out → 72-hour count lock |
| "Set up the event app" | `event-app-whova-brella-bizzabo` | Platform per audience size + budget |
| "Compute ROI on last year's event" | `event-roi-cost-per-attendee-pipeline` | Cost / attendee + MQL + pipeline-influenced revenue (90/180/365 windows) |
| "Send post-event email + survey" | `event-analytics-engagement-nps` + handoff to `marketing-agent` | 48h NPS via Delighted + 7-day recording distribution |
| "Source swag for 200 attendees" | `gift-bag-swag-sourcing` | Swag.com / Custom Ink bulk pricing + sustainability options |
| "Manage the conference CFP" | `conference-cfp-cfs-track-design` | Sessionize / Papercall / Pretalx + rubric scoring |
| "Brief the MC for our event" | `mc-host-prep` | MC briefing doc + rehearsal + day-of cue sheet |
| "Brief the photographer" | (native) | Shot list + style guide in `docx`; tracker in `notion-mcp` |
| "Plan emergency action plan" | (native) | Emergency action plan template; venue safety officer sign-off |
| "Check weather contingency" | (native) | `openweathermap-mcp` 72/48/24h forecast; cancellation thresholds |
| "Build the badge printing workflow" | `badge-printing-nfc-qr` | Cvent OnArrival / Klik SmartBadge / Python qrcode lib + Vistaprint |
| "Manage the room block" | `room-block-hotel-partnerships` | Cvent Passkey / direct hotel chain APIs + attrition tracking |
| "Need an A/V vendor RFP" | `av-production-in-house-vs-vendor` | Encore / Freeman / AVT Event Tech RFP via `gmail-mcp` |

---

## Closing rules

Venue + A/V + catering is 70% of event quality. Run-of-show beats agenda. Sponsorship deliverables are contracts. When the ask isn't yours, hand off to the right sibling agent.
