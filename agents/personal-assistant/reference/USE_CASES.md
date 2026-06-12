# Personal Assistant — Use Cases

**Tier:** general · **Category:** productivity
**Core job:** Personal EA / chief-of-staff operator — calendar protection + time blocking, scheduling links, travel orchestration (flights / hotels / cars / itinerary), expense tracking + receipt OCR, restaurant reservations, meeting prep briefs from transcripts, follow-up email drafting, email triage, task management cross-platform, errand routing (food / groceries / handyman), gift research + buying, contact book maintenance + personal CRM, birthday + anniversary tracking, password management, async video drafting, subscription tracking + cancellation, family calendar coordination, vacation planning end-to-end, doctor / dentist scheduling, dry cleaning + car maintenance reminders, smart-home control.

> Ships with the SOTA 2026 personal-assistant stack — Motion / Reclaim.ai / Sunsama for calendar protection; Calendly / Cal.com / OnceHub for scheduling links; TripIt / Hopper / Google Flights / Booking / Amadeus for travel; Expensify / Ramp / Brex (Capital One) for expense; OpenTable / Resy / Tock for reservations; Granola / Fathom / Fireflies / tl;dv for meeting notes; Superhuman / Shortwave / Hey.com for email; Todoist / Things / TickTick / Notion / Apple Reminders for tasks; DoorDash / Uber Eats / Instacart / TaskRabbit for errands; Amazon / Etsy / Uncommon Goods for gifts; Cardhop / Notion / Clay for contacts; 1Password / Bitwarden for passwords; Loom for async video; Rocket Money / YNAB / Lunch Money / Actual Budget for subscription tracking; Google Family / Apple Family / Cozi for family calendar; Home Assistant / HomeKit / Alexa for smart home. Executes calendar / email / task / travel / expense / reservation / gift / contact / family / smart-home work end-to-end. **For consumer-platform booking surfaces with no public consumer API** (OpenTable / DoorDash / Resy / Zocdoc / event-ticket purchase / Loom recording), agent does search + draft + posts calendar holds + surfaces direct-link for user-completion. **Always defers binding personal tax / legal advice to a licensed CPA / attorney** — agent organizes the question + drafts what to ask; the licensed professional answers.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Calendar protection + time blocking
- Block daily focus time (Motion / Reclaim.ai / Sunsama)
- Recurring family time + gym + recovery time
- Buffer time before / after meetings
- Sunday weekly cadence audit
- Time-leak detection + reclaim

### Meeting scheduling (external + internal)
- Calendly + Cal.com + OnceHub scheduling links
- Direct calendar invite via `google-calendar-mcp`
- Round-robin + routing forms (Cal.com)
- Reclaim Smart 1:1s (mutual focus-window match)
- Recurring 1:1 + team cadence

### Travel booking (flights, hotels, cars, transit)
- Flight search via Google Flights / Hopper / KAYAK
- Hotel search via Booking / Amadeus / Agoda
- Car rental via Booking / KAYAK
- TripIt auto-parse from confirmation email
- Pre-departure checklist + reminders
- Loyalty program application + tier match

### Expense tracking + receipt OCR + reimbursement
- Receipt OCR via `gemini-ocr-mcp` / `mistral-ocr-mcp`
- Categorize per company policy
- Reconcile to corp-card txns (Ramp / Brex)
- Submit via Expensify REST
- Outstanding-items follow-up

### Restaurant reservations
- OpenTable / Resy / Tock browsing
- Booking via API where available, deep-link otherwise
- Calendar hold for reservation
- Reminder triggers (1d / 1h before)

### Meeting prep briefs (1:1 + recurring)
- Pull transcripts from Fathom / Fireflies via REST / GraphQL
- Extract action items + commitments + open threads
- Refresh person-context (last news, role change, projects)
- Compose one-page brief 15-30min before meeting

### Follow-up email drafting (after meetings)
- Pull transcript + extract per-recipient action items
- Draft per-recipient email summarizing their commitments + ours + open threads
- Surface for user review before send

### Email triage to inbox zero
- Gmail filter set for auto-archive (newsletters / receipts / marketing)
- AI bundle setup (Shortwave / Superhuman)
- Daily 2-window ritual (morning + end-of-day)
- Bulk-snooze for deferred replies
- Draft top 5-10 actual-reply emails

### Task management cross-platform
- Todoist (default GTD ecosystem)
- Things 3 (Apple-only refinement)
- TickTick (Pomodoro + habits + free)
- Notion Tasks (database-driven)
- Apple Reminders (voice-first)
- Cross-app sync via webhook / API

### Errand routing (food, groceries, handyman)
- DoorDash / Uber Eats / Instacart price + availability compare
- TaskRabbit for multi-stop errands + handyman
- Amazon Same-Day for general retail
- Sandwich concierge for white-glove
- Reorder pattern learning

### Gift research + shopping
- Cross-store search (Amazon + Etsy + Uncommon Goods + Goldbelly + Wirecutter)
- Recipient log per person (past gifts + reactions + interests + sizes + allergies)
- Compare 3-5 options per occasion
- Order via API or surface deep-link
- Card / message drafting

### Contact book maintenance + personal CRM
- Dedup contacts across iCloud / Google / Notion / Cardhop
- Enrich with bday + relationship metadata
- Personal CRM via Clay / Cloze / Notion
- Auto-history from email / calendar
- Reminder cadence (last-talked-to)

### Birthday + anniversary tracking
- Notion DB with date triggers
- Recurring `n8n-workflow-automation` workflow
- Lead-time milestones (T-14d research, T-7d order, T-3d card, day-of message)
- Gift fulfillment integration

### Password management
- 1Password CLI (`op`) for secret retrieval + injection
- Family / team sharing
- Watchtower breach alerts
- New account setup with generated password
- Apple Keychain + Bitwarden alternatives

### Async video drafting (Loom)
- Script + outline drafting
- Share-to email composition
- Transcript pull from Loom REST after recording
- Comment + reaction follow-up

### Subscription tracking + cancellation
- Personal-finance txn pull via `actual-budget-mcp` / `ynab-mcp` / `lunchmoney-mcp`
- Detect recurring + duplicates + low-usage
- Cancellation outreach drafting
- Retention-offer negotiation (DIY or Rocket Money)
- Annual savings projection

### Family calendar coordination
- Shared Google Family / Apple Family / Cozi
- Per-member individual + shared subscription
- Anchor event protection (school dropoff, kid recital, family dinner)
- Chore-rotation matrix
- Conflict detection 24-48h advance

### Vacation planning end-to-end
- Destination research via `firecrawl-mcp`
- Day-by-day itinerary build
- Flight + hotel + activity + restaurant booking
- TripIt consolidated itinerary
- Vacation brief deliverable (Notion / docx)
- Packing list seed
- Pre-trip checklist

### Doctor / dentist appointment scheduling
- Zocdoc search + booking (partner API only)
- MyChart (Epic-based hospitals) for record + booking
- Outreach drafting to receptionist when no API
- Calendar hold + reminder set

### Special-occasion reservation + event tickets
- OpenTable Premier / concierge desk outreach
- SeatGeek / StubHub / Ticketmaster search
- Watch + price-track for sold-out events
- Booking via API where available, deep-link otherwise

### Dry cleaning + car maintenance reminders
- Apple Reminders / Todoist recurring chore management
- Car service interval tracking (CarFax-based recommendations)
- Rinse / Cleanly pickup integration
- Calendar holds for service appointments

### Inbox-zero workflow (rule-based + AI assist)
- Forte CODE method / Merlin Mann 5 actions
- Filter set + AI bundles
- 2-window daily ritual
- Template + snippet library

### Async standup notes for boss
- Pull yesterday's completed + meetings + commitments
- Pull today's planned + scheduled + blockers
- 3-bullet format compose
- Post via Slack (Geekbot-style) / Gmail (digest) / Notion (daily log)

### Smart home control
- Apple HomeKit / Google Home / Alexa / Home Assistant
- Scene + automation design (Wake / Leave / Home / Movie / Sleep / Vacation)
- Trigger → action automation
- Voice control + presence-based

### Recurring task automation (workflows for routines)
- Apple Shortcuts (iOS/macOS personal)
- Zapier / Make / n8n (cross-app)
- Trigger types: date, calendar event, email, location, geo-fence
- Dry-run + test before production

### Time audit + reclaim
- Reclaim.ai Analytics for time-in-meetings vs focus
- Toggl / RescueTime for app-level time tracking
- Weekly audit + reshuffle

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case above appears here as a row. Source: `reference/SOTA_USE_CASES.md`.

| Use case | SOTA mechanism | Path |
|---|---|---|
| Calendar protection + time blocking | Motion + Reclaim.ai + Sunsama | `cli-anything` + REST + `google-calendar-mcp` |
| Meeting scheduling (external + internal) | Calendly + Cal.com + OnceHub + Reclaim Smart 1:1s | `calendly-api` + `cli-anything` + `google-calendar-mcp` |
| Travel booking (flights / hotels / cars / transit) | TripIt + Hopper + Google Flights + Booking + Amadeus + Agoda | `google-flights-mcp` + `amadeus-hotels-mcp` + `booking-mcp` + `agoda-api-mcp` + `cli-anything` (TripIt) |
| Expense tracking + receipt OCR | Expensify SmartScan + Ramp + Brex (Capital One) + OCR | `cli-anything` + Expensify REST + `gemini-ocr-mcp` + `mistral-ocr-mcp` + `xero-mcp` |
| Restaurant reservations | OpenTable + Resy + Tock + Yelp | `playwright-mcp` + `google-calendar-mcp` |
| Meeting prep briefs from transcripts | Granola + Fathom + Fireflies + tl;dv + Otter.ai | `cli-anything` + Fathom REST + Fireflies GraphQL |
| Follow-up email drafting | Superhuman AI + Shortwave AI + per-recipient extraction | `gmail-mcp` + transcript-pull |
| Email triage to inbox zero | Superhuman + Shortwave + Hey.com + Gmail filters + AI bundles | `gmail-mcp` + `gmail-manager` + `cli-anything` |
| Task management cross-platform | Todoist + Things + TickTick + Notion + Apple Reminders | `todoist-mcp` + `apple-reminders` + `notion-mcp` + URL schemes |
| Errand routing (food / groceries / handyman) | DoorDash + Uber Eats + Instacart + Shipt + TaskRabbit + Amazon | `firecrawl-mcp` + `playwright-mcp` + `amazon-mcp` |
| Gift research + shopping | Amazon + Etsy + Uncommon Goods + Goldbelly + Wirecutter | `amazon-mcp` + `ebay-mcp` + `firecrawl-mcp` + `notion-mcp` |
| Contact book maintenance + personal CRM | Cardhop + Notion Contacts + Clay + Cloze + Apple Contacts | `notion-mcp` + `icloud-mcp` + `cli-anything` (Clay API) |
| Birthday + anniversary tracking | Notion DB + Cardhop + Apple Bday Calendar + n8n | `notion-mcp` + `google-calendar-mcp` + `n8n-workflow-automation` |
| Password management | 1Password CLI + Bitwarden + Apple Keychain | `1password` + `onepassword-mcp` + `bitwarden-mcp` |
| Async video drafting (Loom) | Loom + Vidyard + Tella + scripts | `cli-anything` + Loom REST + `gmail-mcp` |
| Subscription tracking + cancellation | Rocket Money + Bobby + Trim + budget tools | `actual-budget-mcp` + `ynab-mcp` + `lunchmoney-mcp` + `gmail-mcp` |
| Family calendar coordination | Google Family + Apple Family + Cozi + Skylight | `google-calendar-mcp` + `icloud-mcp` |
| Vacation planning end-to-end | TripIt + Hopper + Booking + Viator + Rome2Rio + Eater Guides | `firecrawl-mcp` + `google-flights-mcp` + `booking-mcp` + `google-maps-mcp` + `cli-anything` (TripIt) |
| Doctor / dentist appointments | Zocdoc + MyChart + Solv + Apple Health | `cli-anything` + Zocdoc partner + `apple-health-mcp` |
| Special-occasion reservation + event tickets | OpenTable Concierge + SeatGeek + StubHub + Ticketmaster | `cli-anything` + SeatGeek/StubHub/Ticketmaster REST |
| Dry cleaning + car maintenance reminders | Apple Reminders + Todoist + CarFax | `todoist-mcp` + `apple-reminders` + `n8n-workflow-automation` |
| Inbox-zero workflow (rule-based + AI) | Forte CODE + Merlin Mann + Shortwave + Superhuman | `gmail-mcp` + `gmail-manager` + `cli-anything` |
| Async standup notes for boss | Geekbot + Range + Standuply + Notion daily-log | `slack-mcp` + `notion-mcp` + `gmail-mcp` |
| Smart home control | Apple HomeKit + Google Home + Alexa + Home Assistant | `hass-mcp` + `home-assistant-mcp` + `advanced-ha-mcp` + `iot-mcp` |
| Recurring task automation | Apple Shortcuts + Zapier + Make + n8n + IFTTT | `n8n-workflow-automation` + `automation-workflows` + `cli-anything` |
| Time audit + reclaim | Reclaim.ai Analytics + Toggl + RescueTime | `cli-anything` + Reclaim Analytics REST + Toggl REST |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Restaurant reservations (OpenTable / Resy / Tock) | ⚠ | No consumer-booking API — agent does search + availability + calendar hold + surfaces direct-link for user-completion. `playwright-mcp` browser automation as fallback. Full automation requires OpenTable Affiliate / partner program. |
| Errand ordering (DoorDash / Uber Eats / Instacart) | ⚠ | Consumer ordering APIs not exposed (each has Drive / Partner API for fulfillment partners only). Agent does compare + surfaces best-option deep-link. Apple Shortcuts can chain user-confirmed orders. |
| Doctor / dentist booking (Zocdoc / MyChart) | ⚠ | Zocdoc Partner API gates booking to partners; MyChart booking is per-hospital. Agent searches + drafts outreach + surfaces URL. |
| Special-event tickets (SeatGeek / StubHub / Ticketmaster) | ⚠ | Search + price-track APIs exist; binding purchase typically requires user-completion. |
| Loom video recording | ⚠ | Recording is user-side (camera/mic). Agent writes script + outline + share-to email + reads transcript after recording. Full automation impossible without camera access. |
| Calendar / scheduling platform API keys (Motion / Reclaim / Calendly / Cal.com) | ⚠ | Recipient provides paid API key for premium features. All have sandbox / free-tier basics. |
| Travel platform API keys (TripIt Pro / Hopper / Amadeus / Booking) | ⚠ | Recipient provides paid API key for premium features. TripIt Lite + Google Flights free fallback. |
| Expensify / Ramp / Brex (Capital One) API keys | ⚠ | Recipient provides paid API key. Brex API surface evolving post-Capital One acquisition (April 2026). |
| Fathom / Fireflies / Otter / Granola transcript API keys | ⚠ | Recipient provides paid API key. Granola has no public API yet (June 2026); use export integration. |
| Superhuman / Shortwave email API keys | ⚠ | Limited public APIs; agent works through Gmail layer when those are surface frontends. |
| Todoist / Things / Notion / Linear API keys | ⚠ | Recipient provides paid API key for premium platforms (Todoist Pro). Things uses URL scheme (free). |
| 1Password / Bitwarden vault access | ⚠ | Recipient provides vault unlock via CLI (`op signin`). |
| Personal-finance budget tools (YNAB / Lunch Money / Actual / Rocket Money) | ⚠ | Recipient provides paid platform key + bank-link OAuth. |
| Smart-home device API access (HomeKit / Google Home / Alexa) | ⚠ | HomeKit has no API (relies on Apple Home Shortcuts); Google Home / Alexa partial API. Home Assistant fully agent-controllable. |
| Binding personal tax / legal advice | ⚠ | **Always disclose "this is not binding tax / legal advice; ask a licensed CPA / attorney."** Agent organizes question + drafts what to ask; licensed professional answers. Not a capability gap — operational discipline. |
| Investment portfolio rebalancing | ⚠ | Defer to a licensed CFP / advisor. Agent tracks + reports; advisor recommends binding. |
| Binding insurance / will / estate planning | ⚠ | Defer to a licensed attorney / broker. Agent surfaces options; professional binds. |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a named SOTA tool with an exact agent execution path. Search, drafting, research, calendar coordination, follow-up, tracking, and automation are fully agent-executable. The ⚠ rows for the 5 consumer-platform booking surfaces (restaurant, errand, doctor, event-ticket, Loom recording) are caveats where the final transaction step lacks a public API for individuals — agent does the research + drafting + calendar hold; user clicks complete. The remaining ⚠ entries are API-key gating (resolves once recipient provides their existing platform's API key — operationally normal). The "defer to licensed CPA / attorney / CFP / broker" disclosure on binding tax / legal / investment / insurance topics is operational discipline, not a capability gap. There are no ✗ rows.

---

## When to use this agent

- "Block 9-11am every weekday as deep focus time, family time 6-8pm, no meetings on Fridays after 3pm."
- "Send Sarah a Calendly link for a 30min intro coffee next week."
- "Book me a flight to JFK on July 15, returning July 18, aisle seat, hotel near Times Square under $400/night."
- "File my expense report from the Boston trip — receipts are in my photos roll + Ramp txns."
- "Get a table at Atelier Crenn for 8pm Saturday, party of 2."
- "Prep me for my 1:1 with Marcus tomorrow — pull the last transcript and surface action items."
- "Triage my inbox to zero — I have 137 unread."
- "Plan our trip to Tokyo in October — 7 days, party of 2, budget $5K, foodie."
- "Find a 50th-bday gift for my dad — he's into woodworking, last gift was a chisel set he loved."
- "Audit my subscriptions — I think I'm paying for 3 cloud storage services."
- "Sync our family calendar — kid's soccer game Saturday conflicts with my Friday-night work dinner."
- "Send a Loom to my report walking through the new project structure."
- "Remind me Mom's bday is in 3 weeks — research a gift, order it next Sunday, book dinner reservation."
- "Set up Apple Home routine for movie night — dim lights, lower thermostat, turn on TV."
- "Cancel my Audible subscription — write the email to support."
- "Find me a dentist in San Francisco that takes my insurance — book a cleaning for next week."

---

## When NOT to use this agent

- **Binding personal tax filings / tax interpretation** — hand off to a licensed CPA. Agent organizes question + drafts what to ask; CPA answers binding.
- **Binding legal questions / contract review / wills / estate planning** — hand off to a licensed attorney. Agent surfaces options + drafts question; attorney binds.
- **Investment advice / portfolio rebalancing / financial planning** — hand off to a licensed CFP / financial advisor. Agent tracks + reports personal spend; advisor recommends binding.
- **Insurance binding** (life / disability / umbrella / homeowner / renter) — hand off to a licensed insurance broker. Agent surfaces options + comparisons; broker binds.
- **Company-scale HR / hiring / onboarding / payroll / vendor management / SaaS audit / employee handbook** — hand off to `operations-agent`. They run go-to-team; this agent runs go-to-self.
- **Strategic executive work / board prep / C-suite calendar / equity philosophy / org design** — hand off to `ceo-agent`. They set strategy; this agent executes personal logistics.
- **Business financial reporting / AP / company books / forecasting / cap table maintenance** — hand off to `finance-controller`. They reconcile + report; this agent tracks personal spend.
- **Deep IT / DevOps / infrastructure / smart-home installation troubleshooting beyond config** — hand off to `devops-engineer`. They build infra; this agent configures routines.
- **Marketing / content creation / brand work / paid ads** — hand off to `marketing-agent`. They run go-to-market; this agent runs go-to-self.
- **Engineering / code review / API integration beyond `cli-anything` REST calls** — hand off to `senior-python-engineer` or specialist engineer.
- **Customer support / external customer ticket triage** — hand off to `customer-support-agent`. They handle external; this agent handles personal.
- **Sales pipeline / quota / commission plan** — hand off to `sales-agent`. They run pipeline; this agent runs personal scheduling for sales calls.
- **Research-grade competitive intelligence / market sizing / scientific literature review** — hand off to `research-analyst`. They run research; this agent runs personal info-organizing.
- **Out-of-scope: babysitting recommendations, medical advice, mental-health crisis intervention** — refuse; recommend specialist channels (childcare service, medical professional, crisis line).
