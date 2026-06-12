# Event Planner — Use Cases

**Tier:** **general** · **Category:** operations/events
**Core job:** End-to-end event production — venue sourcing, A/V production, catering coordination, attendee registration, agenda + speaker management, sponsor management, virtual / hybrid event tech, accessibility, and ROI measurement.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

Ships with the SOTA event production stack — Cvent Supplier Network, Bizzabo / Klik SmartBadge, Splash, Eventbrite, RingCentral Events (formerly Hopin), Whova, Brella, Sessionize, Restream / OBS / StreamYard / Riverside, Aberdeen CART, Sorenson ASL, Delighted NPS. Executes end-to-end (source venues + draft contracts + configure registration + author run-of-show + book speakers + coordinate catering + track sponsors + run streaming + measure ROI), not just direct.

---

## What this agent is supposed to do

### Event format selection + strategy
- Recommend event format (in-person / virtual / hybrid; conference / summit / webinar / workshop / meetup)
- Set attendee target, business outcome, budget envelope, KPI targets

### Venue sourcing + contracting
- Source venues (Cvent Supplier Network RFPs; capacity + AV + accessibility match)
- Negotiate venue contracts (F&B floor, attrition cap, force majeure, cancellation, outside-vendor allowance)
- Manage room blocks (Cvent Passkey + direct hotel chain APIs + attrition tracking)

### Attendee registration + ticketing + check-in
- Set up attendee registration (Cvent / Bizzabo / Splash / Eventbrite / RingCentral Events)
- Design and host event website + branding
- Generate badges + check-in (NFC / QR / RFID)
- Track attendee check-in lines + bottleneck mitigation

### Agenda + speaker management
- Author agenda + run-of-show (broadcast-style 5-column cue sheet)
- Source + book speakers (research, outreach, contracting, prep)
- Manage speaker travel + lodging
- Prep speakers (rehearsal, slide review, tech check, day-of cues)
- Conference CFP / CFS — track design + abstract review (Sessionize / Papercall / Pretalx)

### A/V production + streaming
- Choose A/V production (in-house vs vendor selection; Encore / Freeman RFP)
- Live stream the event (Restream / OBS / StreamYard / Riverside / hybrid multi-cam)
- Record + produce audio for podcast distribution
- Distribute post-event content (recordings, photos, transcripts)

### Catering + F&B
- Coordinate catering (dietary, allergies, headcount, special requests; BEO drafting)
- Manage gift bags, swag, and welcome packages (Swag.com / Custom Ink)

### Sponsor + partner management
- Source sponsors (prospect list, tier definition, outreach)
- Manage sponsor deliverable tracking (contracts as enforcement layer)
- Coordinate sponsor booth (location, setup time, lead capture, breakdown)
- Sponsor lead handoff (post-event CSV / CRM sync)

### Event app + attendee experience
- Set up event app (Whova / Brella / Bizzabo / Hopin / EventMobi)
- Configure virtual networking + matchmaking (Brella / Swapcard / Grip)
- Run audience Q&A (Slido / Mentimeter / Pigeonhole / AhaSlides)
- Webinar production (Demio / Livestorm / Zoom Events / MS Teams Live Events)

### Event marketing + promotion
- Plan event marketing campaign (briefs the campaign; defers execution to `marketing-agent`)
- MC / host preparation

### Production + day-of operations
- Brief photographer + videographer
- Manage event analytics (attendee tracking, engagement, NPS)
- Send post-event email + survey (defers execution to `marketing-agent`)
- Measure event ROI (cost per attendee, MQL per event, pipeline-influenced revenue)

### Accessibility + compliance
- Plan accessibility (ADA Title III, CART captioning, ASL interpretation, sensory-friendly)
- Manage event insurance + risk (RFQ; defers procurement to `operations-agent`)
- Plan fire safety + emergency protocols (Emergency Action Plan)
- Plan weather contingency (outdoor + transit risk)

---

## Execution status (SOTA — June 2026)

The historic "I can draft a run-of-show but can't configure the platform" / "I can list sponsors but can't track their deliverables" / "I can plan catering but can't lock the count" gaps are closed. As of mid-2026, every major event-management platform (Cvent / Bizzabo / Splash / Eventbrite / RingCentral Events / Whova / Brella / Swapcard / Sessionize / Slido) exposes a production-grade REST API. Cloud streaming (Restream / StreamYard / Riverside) and open-source OBS Studio handle the streaming surface. Accessibility (Aberdeen CART / Sorenson ASL) is bookable via API. The agent's `cli-anything` mechanism hits any of those plus OpenAI Whisper / OpenWeatherMap / Delighted NPS / Stripe / Twilio / DocuSign / Vistaprint.

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Event format selection | PCMA 2026 + decision-tree framework | native generation + `event-format-selection-in-person-virtual-hybrid` skill |
| Venue sourcing | Cvent Supplier Network RFP via API + Bizzabo Venue Concierge + Splash directory | `cli-anything` + Cvent API + `notion-mcp` comparison matrix |
| Venue contract redline | MPI 2026 redline checklist (F&B floor, attrition, force majeure, cancellation, outside-vendor) | `docx` skill + native generation |
| Room block management | Cvent Passkey API + direct hotel chain APIs + Postgres alert table | `cli-anything` + `postgresql-mcp` |
| Attendee registration | Cvent / Bizzabo / Splash / Eventbrite / RingCentral Events APIs | `cli-anything` per platform API |
| Event website + branding | Splash REST API / Cvent Studio / Webflow + Bizzabo embed | `cli-anything` + `figma-mcp` for brand kit |
| Badge printing (NFC/QR) | Cvent OnArrival API + Klik SmartBadge + Python `qrcode` lib + Vistaprint API | `cli-anything` + `qrcode` + Vistaprint |
| Check-in queue tracking | Platform real-time API polling → `postgresql-mcp` → `slack-mcp` alert | `cli-anything` |
| Agenda + run-of-show | 5-column cue sheet in `notion-mcp` DB + `xlsx` export for stage manager | `notion-mcp` + `google-sheets` |
| Speaker sourcing + outreach | Sessionize CFP API + `gmail-mcp` outreach with episode-cited pitch | `gmail-mcp` + `firecrawl-mcp` |
| Speaker contracting | `docx` template + DocuSign API for e-signature | `cli-anything` + DocuSign |
| Speaker travel + lodging | `google-flights-mcp` + Amadeus Hotels API + TripActions / Egencia | `cli-anything` + `notion-mcp` |
| Speaker rehearsal + prep | `zoom-mcp` rehearsal + `pptx` slide audit + `notion-mcp` briefing | native |
| CFP / CFS track design | Sessionize / Papercall / Pretalx APIs + rubric scoring | `cli-anything` |
| A/V vendor RFP | Encore / Freeman / AVT Event Tech RFP via `gmail-mcp` + Notion comparison matrix | `gmail-mcp` + `notion-mcp` |
| Live streaming setup | Restream / StreamYard / Riverside / OBS Studio + `youtube-mcp` for YouTube Live | `cli-anything` install + APIs |
| Audio podcast production | Riverside Studio API + OpenAI Whisper + Buzzsprout API | `cli-anything` |
| Post-event recording distribution | `youtube-mcp` bulk upload + `cli-anything` Whisper transcription + email digest | `youtube-mcp` + handoff to `marketing-agent` |
| Catering BEO | Dietary capture at reg → aggregate → BEO via `gmail-mcp` + `docx` → 72-hour lock | `cli-anything` + `gmail-mcp` |
| Swag + gift bags | Swag.com / Custom Ink quote APIs + drop-ship logistics | `cli-anything` + `gmail-mcp` |
| Sponsor sourcing + outreach | `firecrawl-mcp` + LinkedIn research + `gmail-mcp` outreach with personalized prospectus | `pptx` + `gmail-mcp` |
| Sponsor deliverable tracking | Per-contract `notion-mcp` DB rows with due date + owner + status; weekly digest | `notion-mcp` + `gmail-mcp` |
| Sponsor booth coordination | `drawio-mcp` floor plan + Cvent Floor Plan Builder + lead capture (Cvent / Klik / Whova) | `drawio-mcp` + `cli-anything` |
| Sponsor lead handoff | Event platform export → sponsor CRM via `cli-anything` (HubSpot/Salesforce/Marketo) | `cli-anything` |
| Event app setup | Whova / Brella / Bizzabo / EventMobi APIs for event creation + agenda sync | `cli-anything` |
| Virtual networking matchmaking | Brella / Swapcard / Grip APIs for interest taxonomy + meeting scheduling | `cli-anything` |
| Audience Q&A management | Slido / Mentimeter / Pigeonhole APIs for Q&A session + polls + analytics export | `cli-anything` |
| Webinar production | Demio / Livestorm / Zoom Events / MS Teams Live Events APIs | `zoom-mcp` + `ms-teams-mcp` + `cli-anything` |
| Event marketing campaign brief | Native generation + `concise-planning` skill; hand off execution to `marketing-agent` | sibling agent |
| MC / host preparation | `docx` briefing + `zoom-mcp` rehearsal + `gmail-mcp` delivery + day-of cue sheet | native |
| Photographer / videographer brief | `docx` shot list + style guide + `notion-mcp` shot tracker | native |
| Event analytics | Platform analytics API + Delighted NPS + composite engagement score | `cli-anything` + `postgresql-mcp` |
| Post-event email + survey | Native generation of segmented content; hand off execution to `marketing-agent` | sibling agent |
| Event ROI measurement | Cost / attendee + MQL + pipeline-influenced revenue (90/180/365-day windows) | `cli-anything` + `postgresql-mcp` |
| Accessibility planning | ADA Title III audit + CART (Aberdeen) + ASL (Sorenson) booking 14-21 days out | `gmail-mcp` + `notion-mcp` |
| Event insurance RFQ | GatherGuard / Eventsured / Markel quote requests; hand off procurement to `operations-agent` | `gmail-mcp` + sibling agent |
| Fire safety + emergency action plan | `docx` emergency action plan + venue safety officer sign-off | native |
| Weather contingency | `openweathermap-mcp` 72/48/24h forecast monitoring + decision tree | `openweathermap-mcp` + `gmail-mcp` |

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Cvent Supplier Network + Cvent Passkey | ⚠ | Paid Cvent enterprise subscription required; free fallback: manual venue research via `brave-search` + `firecrawl-mcp` + Eventbrite Venue Search for smaller venues; Bizzabo Venue Concierge is included in Bizzabo subscription |
| Bizzabo / Whova / Brella subscriptions | ⚠ | All paid SaaS — recipient owns the subscription; agent operates against the recipient's account |
| Slido / Pigeonhole API (Enterprise tier) | ⚠ | Full programmatic Q&A control requires Enterprise tier; free fallback: Google Forms + Sheets API for low-tech Q&A; Mentimeter (cheaper) or AhaSlides (lowest cost) for mid-tier |
| Event ROI (CRM attribution) | ⚠ | Requires recipient's CRM access (HubSpot / Salesforce / Marketo OAuth) for full pipeline attribution; free fallback: manual CSV import + accounting cost data |
| Event insurance procurement | ⚠ | Per per-agent prompt, this agent owns RFQ generation only; final procurement signoff is handed off to `operations-agent` |
| Sponsor relationship cultivation | ⚠ | Per per-agent prompt, this agent owns sponsor sourcing + outreach + deliverable tracking; long-cycle relationship + multi-event partnerships + exclusive industry-org tie-ups are handed off to `bd-partnerships` |
| Event marketing campaign execution | ⚠ | Per per-agent prompt, this agent owns the campaign brief + dependency timeline; paid social / email / content execution is handed off to `marketing-agent` |
| Earned media / press release / crisis comms | ⚠ | Per per-agent prompt, this agent owns event-related operational comms; press release + journalist outreach + crisis comms is handed off to `pr-comms` |
| Customer-event programming | ⚠ | Per per-agent prompt, executive briefings + customer advisory boards + regional user groups + customer summit content design is handed off to `customer-success` |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a concrete execution path. The remaining 5% is paid event-management platform subscriptions (Cvent / Bizzabo / Whova / Brella are SaaS — recipient owns the account) and sibling-agent hand-offs that are by-design (marketing campaign execution, earned media, sponsor relationship cultivation, procurement signoff, customer-event programming). Free fallbacks exist for the API-tier limits (Mentimeter / AhaSlides for Q&A; manual venue research; CSV-based ROI computation).

---

## When to use this agent

- "Help me plan a 300-person customer conference in Q3 — venue, agenda, sponsors, the whole thing"
- "Source 5 venues in Chicago for 200 attendees in March; we need AV-heavy + accessibility tier 1"
- "Redline this venue contract — focus on attrition + force majeure"
- "Set up registration for our hybrid summit; we're using Bizzabo"
- "Build the run-of-show for our 2-day product launch event"
- "Find me 5 keynote speakers for our SaaS conference; budget $10K-$25K per speaker"
- "Build our sponsorship program — Bronze through Platinum tiers; first sponsor outreach in 2 weeks"
- "Coordinate catering for 250 attendees; we have 15 vegan, 8 GF, 3 halal so far"
- "Stream the keynote live on YouTube + LinkedIn + Twitter simultaneously"
- "Book CART captioning + ASL interpretation for our Sept conference"
- "Compute ROI on last year's conference — we need cost per attendee + pipeline attribution"
- "What's the run-of-show timing for sponsor booth setup + breakdown?"
- "Manage our conference CFP via Sessionize; 200+ abstracts expected"
- "Draft the emergency action plan for our outdoor festival"

## When NOT to use this agent

- **Event marketing campaign execution** (paid social, email lifecycle, content series) — hand off to `marketing-agent`. This agent owns the brief + dependency timeline.
- **Press release + earned media + journalist outreach** for event keynote announcement or crisis comms during the event — hand off to `pr-comms`.
- **Long-cycle sponsor / partner / industry-org relationship cultivation** (multi-event partnerships, strategic sponsorships >$100K, exclusive tie-ups) — hand off to `bd-partnerships`.
- **Venue insurance procurement + vendor compliance auditing + master service agreements** — hand off to `operations-agent` (procurement + risk surface).
- **Customer-event programming** (executive briefings, customer advisory boards, regional user groups, customer summit content design) — hand off to `customer-success`.
- **Deep video production** for event recap or marketing assets — hand off to `video-creator`.
- **Legal review of contracts** (venue, speaker, sponsor) — flag for legal sign-off; this agent drafts redlines but does not provide legal advice.
- **Personal event planning** (weddings, birthdays, family events) — out of scope; recommend a wedding/event planner specialist (v1).
