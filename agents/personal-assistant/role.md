# Personal Assistant — Role Content (appended to AGENT.md)

> This file appends to `AGENT.md` and is **not** loaded into the agent's default context. The agent reads `soul.md` every turn and **greps** this file for deep references when stuck.
>
> Search-friendly headings include: "Capability reference", "Calendar protection playbook", "Scheduling playbook", "Travel booking playbook", "Expense filing playbook", "Inbox triage playbook", "Vacation planning playbook", "Subscription audit playbook", "Family calendar playbook", "Gift research playbook", "Meeting prep playbook", "Async standup playbook", "Smart home playbook", "Antipattern catalog", "SOTA tool reference", "TripIt parse rules", "Reclaim defense pattern", "Calendly event-type matrix", "Notion gift-log schema", "Vacation brief template".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Calendar / scheduling platforms supported

- **Motion** — AI auto-scheduler; auto-reshuffles when meetings shift; per-priority block protection; calendar + task in one. Best for power-users who want one app to own everything.
- **Reclaim.ai** — Smart 1:1s find mutually-defended windows; Habits defend focus blocks across colleagues; Analytics surface time-spent patterns. Best for teams already on Google Calendar.
- **Sunsama** — Morning + evening rituals; multi-source task pull (Todoist / Asana / Linear / Notion); calm-aware design. Best for power-users who want a daily-ritual layer.
- **Akiflow** — Universal inbox + calendar; consolidates 30+ sources. Best for users with task fragmentation across many apps.
- **Fellow** — 1:1 + team meeting + agenda + action items. Best for managers.
- **OnceHub** — round-robin + complex routing; enterprise scheduling.
- **Calendly** — largest mind-share; deep workflows on paid tier; rich integrations.
- **Cal.com** — open-source; self-host; dev-friendly; routing forms.
- **SavvyCal** — overlay-style scheduling; reduces back-and-forth.
- **Apple Calendar Family Sharing** — iOS-native shared calendars.
- **Cozi** — family-specific (calendar + meal + shopping + chores).
- **TimeTree** — multi-region; shared with locking.

### Email clients / triage tools

- **Superhuman** — fastest keyboard shortcuts; built-in AI assistant; speed-optimized; paid.
- **Shortwave** — Inbox AI bundles; thread summaries; AI search; freemium.
- **Spike** — chat-style inbox.
- **Hey.com** — Imbox/Feed/Paper Trail; opinionated; paid.
- **Mimestream** — Gmail-native Mac client.
- **Spark** — multi-platform smart inbox; free; AI included on Premium.
- **Apple Mail / Gmail / Outlook** — defaults; baseline workflows.

### Task management platforms

- **Todoist** — largest GTD ecosystem; Natural Language; cross-platform; paid for productivity.
- **Things 3** — Apple-only refinement; single-purchase no subscription; ideal for clean GTD.
- **TickTick** — Pomodoro + habits + free tier.
- **Notion Tasks** — database-driven; cross-domain integration.
- **Apple Reminders** — Apple-native; voice-first; shared lists.
- **Linear** — engineering tracker; prosumers use for life.
- **OmniFocus** — Mac/iOS power-user GTD; subscription.
- **Asana** — team-focused.
- **Microsoft To-Do** — Microsoft-ecosystem.
- **Any.do** — multi-platform.

### Travel booking platforms

- **TripIt Pro** — itinerary aggregation + email parsing + flight tracking + airport reqs.
- **Hopper** — predictive flight pricing (proprietary ML); hotel + car deals.
- **Google Flights** — broadest metasearch + price tracking + flexible-dates + price graphs.
- **KAYAK** — metasearch with strong filters.
- **Booking.com** — hotel breadth + free cancellation rate.
- **Airbnb** — short-term rental + Plus tier.
- **Plum Guide** — vetted high-end short-term rentals.
- **VRBO** — vacation rental.
- **Amadeus** — GDS surface for developer access.
- **Sabre** — GDS surface (legacy).
- **Amex Travel** — points redemption (Pay With Points).
- **Capital One Travel** — Hopper-powered.
- **Wanderlog** — itinerary collab + map view.
- **Roadtrippers** — US road-trip route planning.

### Expense / receipt tools

- **Expensify** — SmartScan OCR + auto-categorize + auto-submit; mainstream.
- **Ramp** — corporate card + spend mgmt; AI-driven reconciliation.
- **Brex** — corporate card; acquired by Capital One April 2026.
- **Dext (Receipt Bank)** — receipt-only OCR for accountants.
- **Concur** — enterprise T&E; SAP-owned.
- **Apple Wallet / Google Wallet** — receipt capture for personal.
- **Receipt Hog** — receipt-to-cash app for retail receipts.

### Restaurant + reservation platforms

- **OpenTable** — largest US restaurant network + diner rewards.
- **Resy** — curated discovery + high-end NY/LA + Amex partnership.
- **Tock** — prepaid + tasting menus + ticketed events.
- **Yelp Reservations** — mid-tier; aggregated reviews.
- **SevenRooms** — restaurant CRM (back-of-house).
- **Eater Guides** — curated city guides (research).

### Meeting note tools

- **Granola** — 2026 mind-share leader; AI native-note-taker (not just transcribe — structures).
- **Fathom** — free tier + Zoom-native; AI summaries.
- **Fireflies** — multi-platform; searchable knowledge graph; team-shareable.
- **tl;dv** — multilingual + free tier; Zoom + Meet + Teams.
- **Otter.ai** — legacy; strong meeting recall + speaker ID.
- **Krisp** — audio + noise-canceling; transcription.
- **Loom** — async video (different surface but related).

### Errand / delivery platforms

- **DoorDash** — largest US food delivery; expanded to retail (DashMart, RedCard partnerships).
- **Uber Eats** — food + groceries via Cornershop; integrated with Uber loyalty.
- **Instacart** — groceries from Costco / Whole Foods / H-E-B / Wegmans.
- **Shipt** — Target + Costco delivery.
- **Postmates** — acquired by Uber Eats.
- **TaskRabbit** — multi-stop errands; furniture assembly; handyman.
- **Amazon Fresh / Same-Day** — Amazon grocery + general retail.
- **Sandwich** — concierge for white-glove tasks.

### Gift research surfaces

- **Amazon** — broadest catalog + Prime delivery + AI gift suggestions.
- **Etsy** — handmade + personalized.
- **Uncommon Goods** — curated unique gifts.
- **Goldbelly** — food gifts from regional restaurants.
- **1-800-Flowers** — floral standards.
- **Spongelle / Allbirds / etc.** — boutique direct-to-consumer.
- **Wirecutter Gifts** — researched gift guides.
- **NYT Wirecutter Holiday Guides** — annual curated gift lists.

### Contact management tools

- **Cardhop** — Mac/iOS contact CRM; bday + relationship metadata.
- **Notion Contacts DB** — cross-link to projects/companies; relational.
- **Clay** — personal CRM + relationship intelligence + AI nudges.
- **Cloze** — auto-history from email/calendar; "people-first."
- **Apple Contacts** — native; iCloud sync.
- **Google Contacts** — Google ecosystem.

### Password management

- **1Password** — best UX + family/team sharing + Watchtower breach alerts + SSH agent + Developer.
- **Bitwarden** — open-source + free tier + self-hostable.
- **LastPass** — legacy enterprise.
- **Apple Keychain** — built-in macOS/iOS.
- **Dashlane** — legacy consumer.
- **NordPass / Proton Pass / Keeper** — alternatives.

### Smart home platforms

- **Apple HomeKit** — iOS deep integration; Matter compatible.
- **Google Home / Nest** — Android-first; ML-aware.
- **Amazon Alexa** — largest device catalog.
- **Home Assistant** — open-source; DIY; supports thousands of devices.
- **SmartThings** — Samsung; Matter compatible.

### Personal finance / subscription tracking

- **Rocket Money** (formerly Truebill) — auto-detects subs + cancellation negotiation.
- **Bobby** — manual subscription tracker (simple).
- **Trim** — negotiation assistant.
- **Hiatus** — subscription mgmt + bill negotiation.
- **YNAB (You Need A Budget)** — zero-based budgeting; envelope method.
- **Lunch Money** — modern personal finance + collaborative + custom.
- **Actual Budget** — open-source budgeting.
- **Monarch Money** — Mint replacement (post-Intuit shutdown).
- **Copilot** — Apple-only modern personal finance.
- **PocketGuard** — focused on overspending detection.

### Workflow automation platforms

- **Apple Shortcuts** — iOS/macOS personal automation; powerful + free.
- **Zapier** — 8,000+ apps; broadest catalog.
- **Make.com** — visual builder + agents; 3,000+ apps.
- **n8n** — open-source + LangChain integration + self-host = no execution limits.
- **IFTTT** — legacy consumer.
- **Pipedream** — code + UI hybrid; developer-friendly.
- **Bardeen** — AI-first prompt-driven browser automation.

---

## Calendar protection playbook

Block focus time and family time so the calendar reflects the user's actual priorities.

1. **Audit current state.** Pull the next 4 weeks via `google-calendar-mcp` + categorize each event (focus / meeting / family / personal / dead-time). Surface the actual ratio.
2. **Recommend the protection model.**
   - **Motion** — power-user; want app to own scheduling; ok with auto-reshuffle.
   - **Reclaim.ai** — keep Google Calendar; defend focus + Smart 1:1s; team-friendly.
   - **Sunsama** — value the morning + evening ritual; multi-source task pull.
3. **Configure default protections.**
   - **Focus block.** Daily 9-11am or per-user pattern; "Focus Time" with "do not disturb" event.
   - **Family time.** Daily 6-8pm dinner; "Family Dinner" recurring; protected against work meetings.
   - **Gym / movement.** 3x/week; recurring 7-8am or noon.
   - **Recovery / off.** Weekend mornings; Sunday evening for week-prep.
   - **Buffer.** 15min before each meeting; 30min after a long session.
4. **Set scheduling-link defaults.** Working hours match the protected blocks; min 24h notice; max 3 events per day; cancellation policy.
5. **Audit weekly.** Sunday 8pm review — protected blocks honored? Reshuffle this week?

### Concrete examples — Reclaim defense pattern

```yaml
# Reclaim Habits config (illustrative — actual config via Reclaim UI)
- name: Deep Focus AM
  duration: 2h
  pattern: weekday-9am
  defense: hard  # cannot be overridden by external bookings
  reschedule_window: same-day-only

- name: Family Dinner
  duration: 1.5h
  pattern: daily-6pm
  defense: hard
  exception_pattern: travel-day

- name: Gym
  duration: 1h
  pattern: mwf-7am
  defense: soft  # can be reshuffled to PM if morning hard-conflict
  reschedule_window: same-day
```

### Concrete examples — Motion auto-schedule rules

```
Project: Q3 Strategy Doc
- Effort estimate: 6h
- Deadline: 2026-08-15
- Schedule rule: Deep Focus AM blocks only
- Motion auto-schedules: 3 × 2h sessions across 3 days before deadline
- Reshuffles if: meeting conflict, scope change, deadline pull-in

Project: Weekly Inbox Triage
- Effort: 20min
- Cadence: Monday + Thursday 4pm
- Schedule rule: any 20-min slot
```

---

## Scheduling playbook

Publish scheduling links that filter noise and route to the right calendar.

1. **Define event types.**
   - **Intro / 15min.** Short qualifier; cheap to grant; quick disqualifier.
   - **Standard 30min.** Default for working sessions.
   - **Deep 1h.** Important conversations; longer prep.
   - **Group event.** Specific date + multiple attendees.
2. **Configure per type.**
   - Working hours: respect protected blocks (see Calendar protection)
   - Buffer: 15min before + after
   - Max per day: 3-5 depending on energy
   - Min notice: 24h external, 4h internal
   - Cancellation: 24h required, no-show fee if applicable
   - Required fields: name + email + what's-this-about
   - Confirmation: auto-include Zoom link, calendar invite, follow-up email
3. **Use round-robin if available.** When 2-3 people share a calendar surface, route to first-available.
4. **Use routing forms (Cal.com / Calendly Routing) for triage.** Different question paths route to different calendars (sales vs support vs exec).
5. **Test before publishing.** Book against yourself + verify confirmations + calendar block.

### Calendly event-type matrix (illustrative)

| Type | Duration | Buffer | Min notice | Max/day | Cancel policy | Required |
|---|---|---|---|---|---|---|
| Intro Coffee | 15min | 5/10 | 24h | 4 | 4h | name + email + topic |
| Working Session | 30min | 15/15 | 24h | 5 | 24h | name + email + agenda |
| Deep Conversation | 1h | 30/30 | 48h | 2 | 48h | name + email + prep doc link |
| External Sales | 30min | 15/15 | 48h | 3 | 48h | name + email + company + use case |
| Family Block | n/a | n/a | n/a | n/a | n/a | (use blocked event, not link) |

---

## Travel booking playbook

Book flight + hotel + car with TripIt parsing, calendar holds, and reminder triggers.

1. **Gather constraints.**
   - Origin / destination
   - Date range
   - Flexibility (anchor day, full window)
   - Class preference + airline loyalty status + max budget
   - Hotel chain preference + min star rating + neighborhood
   - Car: needed? class? pickup location?
2. **Search flights.** `google-flights-mcp` for breadth; check Hopper for prediction. Optimize for: total time (not just ticket price) + reasonable connection (90min minimum) + protected airline status.
3. **Recommend + confirm.** Surface 3 options with: ticket price + total travel time + layover + cabin + cancellation policy. Highlight the recommended one + cite reason.
4. **Book.** Via airline website or aggregator. If user-completion required (Hopper, points redemption), surface deep-link.
5. **Search + book hotel.** `amadeus-hotels-mcp` / `booking-mcp` / `agoda-api-mcp`. Optimize for: distance to event venue + breakfast included + free cancellation if dates unstable + loyalty match.
6. **Search + book car if needed.** Search via Booking / KAYAK; choose midsize / SUV per preference.
7. **Pipe to TripIt.** TripIt auto-parses confirmation emails from inbox; verify ingestion.
8. **Calendar holds via `google-calendar-mcp`.**
   - Flight departure (3h before for international, 2h domestic)
   - Flight arrival + ground transport
   - Hotel checkin / checkout
   - Online check-in reminder 24h before
   - Return travel mirror
9. **Surface trip summary** — `notion-mcp` or `docx`. Cover: airline + confirmation + seat + hotel + confirmation + addresses + ground transport plan + packing seed.

### TripIt parse rules

TripIt parses confirmation emails from these sender domains automatically:
- Major US carriers: aa.com, delta.com, united.com, southwest.com, jetblue.com, alaska.com, hawaiianair.com, sun-country.com, allegiantair.com, spirit.com, frontier.com
- International: ba.com, lh.com, klm.com, af.com (Air France), eva.com, china.com.cn, ek.com (Emirates), qantas.com.au, qatarairways.com, singaporeair.com, koreanair.com, etihad.ae, asianair.com, ana.co.jp, jal.co.jp, turkishairlines.com
- Hotels: marriott.com, hilton.com, hyatt.com, ihg.com, accor.com, choice-hotels.com, booking.com, hotels.com, expedia.com
- Cars: hertz.com, avis.com, enterprise.com, sixt.com, budget.com
- Trains: amtrak.com, eurail.com, sncf.com
- Cruises: royal-caribbean.com, ncl.com, carnival.com

If TripIt can't parse: forward to plans@tripit.com manually; or add reservation via TripIt web UI.

### Concrete examples — pre-trip checklist

```markdown
# Trip Pre-Departure Checklist (T-1 day)

- [ ] Online check-in completed (T-24h)
- [ ] Boarding pass saved to Apple Wallet / Google Wallet
- [ ] TSA PreCheck / Global Entry on ticket
- [ ] Loyalty number on ticket
- [ ] Seat selected
- [ ] Hotel confirmation in TripIt
- [ ] Ground transport booked (Uber / rental / public transit)
- [ ] Calendar holds active
- [ ] Reminders triggered for: check-in, departure, arrival
- [ ] Out-of-office set
- [ ] Travel insurance reviewed
- [ ] Power adapter / cables / chargers
- [ ] International: passport in date, visa if applicable
- [ ] Bag tags + ID tag with destination address
```

---

## Expense filing playbook

File expense reports from a trip in <15 minutes.

1. **Capture receipts.**
   - Corp-card: pull from Ramp / Brex / Expensify auto-sync
   - Physical: photograph at point-of-purchase; archive to Apple / Google Wallet
   - Recurring (hotel, ground transport, meals): batch capture end-of-day
2. **OCR via `gemini-ocr-mcp` / `mistral-ocr-mcp`.** Extract: vendor + amount + date + payment method + category hint.
3. **Categorize per company policy.** Common: Travel / Lodging / Meals / Ground / Per Diem / Misc.
4. **Reconcile to corp-card txns.** Match receipt → txn → flag any orphan txn for "where's the receipt" follow-up.
5. **Submit via Expensify REST.**
   ```bash
   # Illustrative — actual Expensify auth flow varies
   curl -X POST https://integrations.expensify.com/Integration-Server/ExpensifyIntegrations \
     -d "requestJobDescription={
       \"type\":\"create\",
       \"credentials\":{\"partnerUserID\":\"...\",\"partnerUserSecret\":\"...\"},
       \"inputSettings\":{\"type\":\"reportExporter\",\"reportType\":\"trip\"}
     }"
   ```
6. **Output:** Submitted report URL + cover-note summary + outstanding items list.

### Expensify category mapping (illustrative)

| Receipt vendor | Expensify category | Tax category | Per diem? |
|---|---|---|---|
| United / Delta / American | Travel - Airfare | Travel | No |
| Marriott / Hilton / Hyatt | Travel - Lodging | Travel | No |
| Uber / Lyft / Taxi | Travel - Ground | Travel | No |
| Restaurant during trip | Meals & Entertainment | Meals | Yes (cap) |
| Coffee shop | Meals & Entertainment | Meals | Yes |
| Office supply | Office Expenses | OpEx | No |
| Wi-Fi / SIM card | Travel - Communications | Travel | No |
| Conference fee | Professional Development | Education | No |
| Parking | Travel - Ground | Travel | No |

---

## Inbox triage playbook

Triage to zero in 30 minutes via batch + filter + AI bundle.

1. **Pull unread.** Via `gmail-mcp` get unread count + sample by category.
2. **Classify by category.**
   - **Newsletter / blog digest** — auto-archive to "Read Later" label
   - **Receipt / shipping confirm** — auto-archive to "Receipts" label
   - **Marketing** — auto-archive to "Marketing" label
   - **Calendar invite / response** — auto-process to calendar
   - **Personal (people you actually know)** — keep in Inbox for reply
   - **Service notification** — surface critical, archive routine
3. **Apply rule set.** Build Gmail filters via `cli-anything` + Gmail API; auto-archive matching patterns.
4. **AI bundle (Shortwave / Superhuman if available).** Group threads by topic; surface top 5 needing reply.
5. **Reply pass.** Compose 5-10 actual replies. Use templates for routine (thanks, will-respond-later, scheduling).
6. **Snooze pass.** Anything deferred → snooze to right time (Monday morning for low-pri, evening for time-sensitive).
7. **Output.** Inbox count delta + draft queue + next ritual scheduled.

### Inbox-zero filter set (illustrative)

```
# Auto-archive to label
from:(*@substack.com OR *@newsletter.* OR *@beehiiv.com OR mailchimp:* OR sendgrid:* OR *@updates.*) → Newsletter / archive
from:(*@amazon.com subject:order OR *@ebay.com subject:order OR *@etsy.com subject:order) → Receipts / archive
from:(noreply@calendar.google.com OR invite@gcal) → Calendar / process via gmail-mcp
from:(*@marketing.* OR subject:"unsubscribe") → Marketing / archive
from:(*@github.com subject:notification) → GitHub / archive

# Auto-star + Inbox
from:(boss@company.com OR partner@personal.com OR mom@family.com) → Inbox / star

# Send to AI bundle (Shortwave-style)
*remaining* → Inbox / AI Bundle
```

---

## Vacation planning playbook

Plan a multi-day trip end-to-end in 1-3 working sessions.

1. **Brief intake.** Destination, dates, budget, party size, travel style (boutique / luxury / budget / family / adventure), must-do list, hard no-list, deal-breakers (allergies, accessibility, etc.).
2. **Research.** `firecrawl-mcp` for destination guides (Wirecutter + locals' subreddit + Eater Guides + Lonely Planet); surface 5-7 candidate activities + 3-4 restaurant clusters + 1-2 neighborhoods to stay.
3. **Build day-by-day.** Anchor activity per day (avoid overpacking); meals (breakfast / lunch / dinner); transit between; afternoon rest buffer; one "wing-it" slot per day.
4. **Book in order.**
   - Flights (TripIt / `google-flights-mcp`) — first because they constrain everything
   - Hotels (per neighborhood pick + `booking-mcp`)
   - High-demand activities + restaurants (book 2-4 weeks before for popular)
   - Local transit (rental car, Eurail pass, transit cards)
5. **Reservation prep.** Restaurant reservations via OpenTable / Resy / Tock — surface deep-link if API-gated.
6. **Calendar holds via `google-calendar-mcp`.** Each major event + buffer + checkin + checkout.
7. **Pipe to TripIt.** Auto-itinerary parse from confirmation emails.
8. **Vacation brief deliverable.** `notion-mcp` or `docx` page with:
   - Cover: dates + party + destinations
   - Per-day H2: anchor + meals + transit + buffer + wing-it
   - Booking summary: confirmation numbers + addresses
   - Packing list seed
   - Emergency contacts + insurance info
   - Loyalty status reminders
9. **Pre-trip checks.** T-1 day: see "pre-departure checklist" above.

### Vacation brief template

```markdown
# Vacation: [Destination] — [Dates]
## Party: [Names + roles]
## Total budget: [Amount]

### Pre-trip
- Flights: [Carrier confirmation]
- Hotels: [Hotel confirmation, address, checkin/checkout]
- Cars / transit: [Pickup confirmation]
- Insurance: [Carrier, policy #, coverage]
- Loyalty: [Programs + status]
- Reservations: [Restaurant + activity + tour bookings]

### Day 1 — [Date]
- 09:00 — Flight arrival, ground transport to hotel
- 11:00 — Hotel checkin
- 12:30 — Lunch at [Restaurant], [address]
- 14:30 — Anchor activity: [Tour / museum / etc.]
- 18:00 — Wing-it window (could be: relax / explore / second activity)
- 19:30 — Dinner at [Restaurant], [address] — reservation confirmation [#]

### Day 2 — [Date]
[... same pattern ...]

### Last Day — [Date]
- 09:00 — Hotel checkout
- [...]
- 14:00 — Flight departure, ground transport

### Packing list seed
- [Per-day-count] socks, underwear, t-shirts
- Outerwear per weather forecast
- [...]
```

---

## Subscription audit playbook

Find and cancel unused subscriptions to save user $X / year.

1. **Pull txn data.** Via `actual-budget-mcp` / `ynab-mcp` / `lunchmoney-mcp` — last 12 months of recurring charges.
2. **Detect subscriptions.** Match by recurring vendor + recurring amount + monthly/annual cadence. Common patterns: streaming, cloud storage, gym, SaaS, magazines.
3. **Detect duplicates.** Multiple cloud storage (Dropbox + iCloud + Google One); overlapping streaming (Netflix + Hulu + Disney+); multiple notes apps.
4. **Detect low-usage.** Cross-reference with last-login dates (manual or via Rocket Money).
5. **Recommendation per subscription.**
   - **Keep** — actively used + good value
   - **Cancel** — unused + replaceable
   - **Negotiate** — used + overpriced (Rocket Money assistance)
   - **Downgrade** — used at lower tier
6. **Draft cancellation outreach.** Via `gmail-mcp` per merchant:
   - Submit cancellation form when available
   - Email customer support with cancellation request + cite reason
   - Retention-offer counter ("I'll stay for $X less" if value still there)
   - Executive escalation if customer-service stonewalls
7. **Output.** Subscription register + cut/keep/negotiate decisions + projected annual savings.

### Notion subscription DB schema

| Field | Type | Notes |
|---|---|---|
| Vendor | Title | Name |
| Service | Select | Streaming / Cloud / SaaS / Gym / News / Productivity |
| Monthly amount | Number | $ |
| Annual amount | Formula | Monthly × 12 |
| Cadence | Select | Monthly / Annual / Lifetime |
| Renewal date | Date | Next charge |
| Last used | Date | Manual update |
| Status | Select | Active / Negotiating / Cancelling / Cancelled |
| Cancel link | URL | Direct cancel form |
| Negotiation notes | Text | Retention-offer history |
| Decision | Select | Keep / Cancel / Negotiate / Downgrade |
| Annual savings if cut | Formula | Annual × (Decision == Cancel) |

---

## Family calendar playbook

Coordinate shared calendar so nobody double-books.

1. **Establish source-of-truth.** One shared calendar (Google Family Sharing OR Apple Family OR Cozi) — never two competing.
2. **Per-member individual calendars.** Each member has their own; subscribe to the shared.
3. **Define event categories.**
   - **Anchor** — non-movable (school dropoff, child's recital, doctor)
   - **Chore** — household routine (groceries, garbage, yard)
   - **Pickup / dropoff** — kid logistics
   - **Family event** — meal / game / outing
   - **Travel** — anyone's trip affecting household
4. **Color-code per member.** Each family member has a color; shared events use a family color.
5. **Conflict detection.** Run via `google-calendar-mcp` — anchor events vs work; surface 24-48h advance.
6. **Chore-rotation matrix.** Per recurring chore + per-member rotation; document in Notion / Cozi.
7. **Output.** Updated shared calendar + chore matrix + recurring patterns.

### Chore rotation matrix (illustrative)

| Chore | Member A | Member B | Member C |
|---|---|---|---|
| Garbage night | Mon / Wed | Tue / Thu | Fri |
| Groceries | Sat AM | — | — |
| Dishes | Mon-Wed | Thu-Sat | Sun |
| Laundry | Sat PM | — | — |
| School dropoff | Mon / Wed / Fri | Tue / Thu | — |
| School pickup | Tue / Thu | Mon / Wed / Fri | — |

---

## Gift research playbook

Buy the right gift + log it for next time.

1. **Confirm intake.** Recipient, occasion, budget, deadline, delivery address. Pull from gift log: past gifts, reactions, interests, sizes, allergies, deal-breakers.
2. **Research.**
   - `amazon-mcp` for catalog + price compare
   - `ebay-mcp` for marketplace
   - `firecrawl-mcp` + curated stores (Wirecutter, Uncommon Goods, Etsy, Goldbelly, etc.)
   - Cross-reference recipient interests (hobbies, currently-watching, sizes, allergies)
3. **Compare 3-5 options.** Each: price + delivery + review score + personalization + reason-this-fits.
4. **Recommend.** Cite the top choice; surface alternatives.
5. **Order.** Place via Amazon / etc., or surface deep-link if no consumer-API.
6. **Update gift log.** Add to recipient DB in `notion-mcp` with: date + occasion + gift + cost + delivery method + reaction (TBD).
7. **Card / message.** Draft a personal note; surface for user-edit before send.

### Notion gift-log DB schema (per recipient)

| Field | Type | Notes |
|---|---|---|
| Date | Date | When gifted |
| Occasion | Select | Birthday / Anniversary / Holiday / Thank-you / Just-because |
| Gift | Text | What was given |
| Cost | Number | $ |
| Source | URL | Where bought |
| Delivery method | Select | Hand / Shipped / Digital |
| Reaction | Select | Loved / Liked / Neutral / Negative / Unknown |
| Notes | Text | Context, why this fit |
| Avoid next time | Text | What didn't work, allergies discovered, etc. |

---

## Meeting prep playbook

Brief user before each 1:1 in 5 minutes.

1. **Pull prior transcript.** Via `cli-anything` + Fathom REST / Fireflies GraphQL.
2. **Extract.** Action items from prior session (theirs + ours); commitments made; open threads; key topics.
3. **Refresh person-context.** Last news (their company, role change, life event); recent achievements; ongoing projects.
4. **Compose brief.** One page:
   - Action items from last meeting (theirs + ours) + status
   - Open threads to revisit
   - This-session agenda from prior commitments
   - Person-context refresh (1-2 lines)
   - Suggested topics
5. **Deliver.** Via `gmail-mcp` (digest) or `notion-mcp` page; calendar entry note 15-30min before.
6. **Output.** Brief doc + reminder triggered.

### Meeting brief template

```markdown
# 1:1 Brief — [Date] [Time] [TZ]
## Attendee: [Name, role, last interaction]

## Action items from last session ([Date])
- **They committed:** [Item] — [status / outcome]
- **They committed:** [Item] — [status / outcome]
- **We committed:** [Item] — [status / outcome]

## Open threads
- [Topic]: [status]
- [Topic]: [status]

## Their context
- [Recent news, projects, life event — 2 lines]

## Suggested topics for this session
1. [...]
2. [...]
3. [...]

## Logistics
- Zoom: [link]
- Doc: [link]
- Prep doc: [link]
```

---

## Async standup playbook

Post daily standup to boss in 3 bullets.

1. **Pull yesterday's data.**
   - Completed tasks via `todoist-mcp` / `apple-reminders` / Linear / Things
   - Meetings attended via `google-calendar-mcp`
   - Commitments made via `cli-anything` + Fathom / Fireflies
2. **Pull today's data.**
   - Planned tasks (from Sunsama / Motion / Todoist today view)
   - Scheduled meetings via `google-calendar-mcp`
   - Anticipated blockers (from open threads in Notion / Linear)
3. **Compose 3-bullet format.**
   - **Yesterday:** [completed]
   - **Today:** [planned]
   - **Blockers:** [issues + ask]
4. **Post.** Via `slack-mcp` (Geekbot-style channel) or `gmail-mcp` (digest email) or `notion-mcp` (daily log).
5. **Output.** Posted standup + cross-link to source data.

### Standup post template

```markdown
**Standup for [Date]**

**Yesterday:**
- [Completed task / artifact shipped]
- [Meeting outcome]

**Today:**
- [Planned task]
- [Scheduled commit]

**Blockers:**
- [Issue] — [ask]
```

---

## Smart home playbook

Configure routines, not individual taps.

1. **Audit current devices.** Pull via `hass-mcp` / `home-assistant-mcp` / `iot-mcp` — list all devices + current state.
2. **Identify scenes.** Common scenes: Wake / Leave / Home / Movie / Sleep / Vacation.
3. **Identify automations.** Trigger → action:
   - Sunset → outdoor lights on
   - Front door opens → entryway light on
   - Last person leaves → all lights off + thermostat eco
   - Bedtime alarm → bedroom dim + thermostat sleep
   - Wake alarm → bedroom lights ramp + coffee maker on + news brief
4. **Recommend per device-mix.** Apple HomeKit (iOS), Google Home (Android), Alexa (broadest), Home Assistant (DIY + most flexible).
5. **Set up via:**
   - HomeKit scenes via iOS Home app (no API)
   - Google Home Routines via app
   - Alexa Routines via app
   - Home Assistant: YAML config via `hass-mcp` or web UI
6. **Test.** Each scene + each automation triggered manually + via natural-language.
7. **Output.** Scenes + automations live + tested + documented in Notion.

### Home Assistant automation YAML (illustrative)

```yaml
# config/automations.yaml

- alias: Sunset Outdoor Lights On
  trigger:
    - platform: sun
      event: sunset
      offset: '-00:15:00'
  action:
    - service: light.turn_on
      target:
        entity_id: light.outdoor_lights
      data:
        brightness_pct: 70

- alias: Last Person Leaves
  trigger:
    - platform: state
      entity_id: group.family
      to: 'not_home'
  action:
    - service: light.turn_off
      entity_id: all
    - service: climate.set_temperature
      target:
        entity_id: climate.living_room
      data:
        temperature: 68

- alias: Wake Up Sequence
  trigger:
    - platform: time
      at: '06:30:00'
  condition:
    - condition: time
      weekday: [mon, tue, wed, thu, fri]
  action:
    - service: light.turn_on
      target:
        entity_id: light.bedroom
      data:
        brightness: 50
        transition: 600
    - service: switch.turn_on
      entity_id: switch.coffee_maker
```

---

## Antipattern catalog

### Antipattern 1: To-do list without calendar slot

**BAD:**
```
TODO:
- Write Q3 strategy doc
- Plan vacation
- Call mom for her birthday
- Sign up for gym
- Subscribe to magazine
```

**Why it's bad:** Open list with no time allocation. Tasks become aspirations; hope is not a strategy. Long lists generate guilt without progress.

**GOOD:**
```
CALENDAR (next 7 days):
- Tue 10-12am: Q3 strategy doc (deep focus block)
- Wed 8pm: Call mom — pre-bday checkin
- Sat 9am: Vacation research (2h)
- Mon 7am: Gym intro session (booked)
- Subscribe to magazine: snoozed for Q4 review
```

**Why it's better:** Each commitment has a slot + a duration + a follow-through trigger. The list of tasks-without-slots is hidden until they're worth scheduling.

### Antipattern 2: Booking without confirmation pause for one-way doors

**BAD:**
- Auto-book non-refundable flight at lowest price
- Auto-book non-refundable hotel deposit
- Auto-send invoice without preview

**Why it's bad:** Flight change fee = $200; hotel deposit non-refundable; mis-sent email un-recallable. Speed beats reversibility for two-way doors but loses against one-way ones.

**GOOD:**
- For non-refundable bookings: surface "DECISION REQUIRED: Confirm to lock fare? (one-way door — $X change fee if you change)"
- For sensitive emails: draft + present + send only after explicit user OK
- For high-value txns: 2-tier confirmation

### Antipattern 3: TZ-implicit scheduling

**BAD:**
- "Meeting at 3pm tomorrow"
- "Flight at 7am"

**Why it's bad:** 3pm where? At the user's location? At the attendee's? At the destination? Misalignment causes missed flights and missed meetings.

**GOOD:**
- "Meeting at 3pm PT / 6pm ET tomorrow Wed July 22"
- "Flight DL1234 departs SFO 06:00 PDT, arrives JFK 14:30 EDT"

### Antipattern 4: Bday reminder set day-of

**BAD:**
- Birthday reminder set for 6am on Mom's birthday — no time to ship a gift
- Anniversary reminder set for the day-of — no time to plan dinner

**Why it's bad:** Gift fulfillment requires lead time. Day-of reminders are too late.

**GOOD:**
- 2 weeks before: gift research + decision
- 1 week before: gift ordered (shipping margin)
- 3 days before: card / message draft + dinner reservation
- Day-of: send message + final greet

### Antipattern 5: Inbox triage in stream, not in batch

**BAD:**
- Real-time inbox check
- Reply-on-arrival to every email
- Notification badge constantly tracked

**Why it's bad:** Continuous inbox is the enemy of deep work. Every interrupt costs 23-minute focus recovery.

**GOOD:**
- 2 daily inbox windows (e.g., 9:30am and 4:00pm) — 30min each
- Notifications off outside windows
- Filter set auto-handles 80% of inbound
- Snooze for deferred reply

### Antipattern 6: Subscription stacking without audit

**BAD:**
- Sign up for new SaaS / streaming / cloud storage without tracking
- Auto-renew unless cancelled
- No quarterly review

**Why it's bad:** Subscriptions accrete silently. Median consumer has 12+ recurring subscriptions; 4-5 are unused or duplicate.

**GOOD:**
- Quarterly audit via `actual-budget-mcp` / `ynab-mcp` / Rocket Money
- Notion subscription DB with renewal date + last-used + status
- Cancel low-usage; downgrade overpriced; negotiate when value still there

### Antipattern 7: Family calendar fragmented across apps

**BAD:**
- Mom uses Google Calendar; Dad uses Apple Calendar; Kid uses paper planner
- Events live in 3 sources; nobody knows what the others have

**Why it's bad:** Double-bookings, missed pickups, family coordination fails. Time-leak on text "wait when's the recital?"

**GOOD:**
- One shared family calendar (Google Family / Apple Family / Cozi)
- All members subscribe
- Anchor events tagged
- Conflict detection runs weekly

---

## SOTA tool reference (June 2026)

### Motion (AI calendar auto-scheduler)

**Use for:** Power-user wanting one app to own scheduling + tasks + projects.
**Skill pack:** [`calendar-protection-motion-reclaim-sunsama`](skills/calendar-protection-motion-reclaim-sunsama/SKILL.md)
**Install:** Mobile + web only; no CLI; REST API via Motion Developer
**Quick recipe:**
```bash
# Motion REST API (illustrative)
curl -X POST https://api.usemotion.com/v1/tasks \
  -H "X-API-Key: $MOTION_KEY" \
  -d '{"name":"Q3 Strategy Doc","duration":120,"deadline":"2026-08-15"}'
```
**Source:** https://docs.usemotion.com/

### Reclaim.ai (calendar protection + Smart 1:1s)

**Use for:** Keep Google Calendar; defend focus + habits + 1:1s across colleagues.
**Skill pack:** [`calendar-protection-motion-reclaim-sunsama`](skills/calendar-protection-motion-reclaim-sunsama/SKILL.md)
**Install:** Web app + Google Calendar OAuth
**Quick recipe:**
```bash
# Reclaim REST (illustrative)
curl -X POST https://api.reclaim.ai/api/habits \
  -H "Authorization: Bearer $RECLAIM_TOKEN" \
  -d '{"name":"Deep Focus","duration":7200,"pattern":"weekday-9am"}'
```
**Source:** https://reclaim.ai/api

### Sunsama (daily ritual planning)

**Use for:** Power-user wanting morning + evening rituals; multi-source task pull.
**Skill pack:** [`calendar-protection-motion-reclaim-sunsama`](skills/calendar-protection-motion-reclaim-sunsama/SKILL.md)
**Install:** Web + native macOS/Win/Linux + mobile
**Source:** https://www.sunsama.com/

### Calendly (scheduling links)

**Use for:** Sender-controlled scheduling links; broadest mind-share.
**Skill pack:** [`scheduling-calendly-cal-com-oncehub`](skills/scheduling-calendly-cal-com-oncehub/SKILL.md)
**Install:** Web; CLI via `calendly-api` skill
**Quick recipe:**
```bash
# Create scheduling link
curl -X POST https://api.calendly.com/scheduled_events \
  -H "Authorization: Bearer $CALENDLY_TOKEN"
```
**Source:** https://developer.calendly.com/api-docs/

### Cal.com (open-source scheduling)

**Use for:** Self-host + dev-friendly; routing forms + advanced workflows.
**Skill pack:** [`scheduling-calendly-cal-com-oncehub`](skills/scheduling-calendly-cal-com-oncehub/SKILL.md)
**Install:** `cli-anything` + `docker compose up -d`
**Source:** https://cal.com/docs

### TripIt (itinerary aggregation)

**Use for:** Auto-parse confirmation emails into one master itinerary.
**Skill pack:** [`travel-booking-tripit-hopper-kayak`](skills/travel-booking-tripit-hopper-kayak/SKILL.md)
**Install:** Mobile + web + email forwarding to plans@tripit.com
**Quick recipe:**
```bash
# TripIt API (OAuth required)
curl -X GET https://api.tripit.com/v1/list/trip \
  -H "Authorization: OAuth ..."
```
**Source:** https://tripit.github.io/api/

### Hopper (predictive flight pricing)

**Use for:** Hold-or-buy decision on flights.
**Skill pack:** [`travel-booking-tripit-hopper-kayak`](skills/travel-booking-tripit-hopper-kayak/SKILL.md)
**Install:** Mobile only; no API
**Source:** https://www.hopper.com/

### Expensify (expense reports + SmartScan OCR)

**Use for:** Receipt OCR + auto-categorize + auto-submit.
**Skill pack:** [`expense-tracking-expensify-ramp-brex`](skills/expense-tracking-expensify-ramp-brex/SKILL.md)
**Install:** Mobile + web + REST
**Quick recipe:**
```bash
# Expensify Integration Server (illustrative)
curl -X POST https://integrations.expensify.com/Integration-Server/ExpensifyIntegrations \
  -d "requestJobDescription={...}"
```
**Source:** https://integrations.expensify.com/Integration-Server/doc/

### OpenTable (restaurant reservations)

**Use for:** Largest US restaurant network for reservations.
**Skill pack:** [`restaurant-reservations-opentable-resy-tock`](skills/restaurant-reservations-opentable-resy-tock/SKILL.md)
**Install:** Web / mobile; Affiliate API for partners only
**Quick recipe:**
```bash
# Browse only (consumer API not exposed)
# Use playwright-mcp for browser automation; surface user-completion link
```
**Source:** https://platform.opentable.com/documentation/

### Granola (AI native meeting notes)

**Use for:** Mind-share leader 2026 for AI structured notes.
**Skill pack:** [`meeting-prep-briefs-from-granola-fathom`](skills/meeting-prep-briefs-from-granola-fathom/SKILL.md)
**Install:** Mac/Win desktop
**Source:** https://granola.ai/

### Fathom (free meeting recorder)

**Use for:** Free tier + Zoom-native + AI summaries.
**Skill pack:** [`meeting-prep-briefs-from-granola-fathom`](skills/meeting-prep-briefs-from-granola-fathom/SKILL.md)
**Install:** Web + Zoom integration
**Quick recipe:**
```bash
# Pull transcript
curl -X GET https://api.fathom.video/v1/meetings/$MEETING_ID/transcript \
  -H "X-API-Key: $FATHOM_KEY"
```
**Source:** https://docs.fathom.video/api/

### Superhuman (AI email assistant)

**Use for:** Fastest keyboard-driven triage + AI drafting.
**Skill pack:** [`email-triage-superhuman-shortwave`](skills/email-triage-superhuman-shortwave/SKILL.md)
**Install:** Web + Mac/iOS native
**Source:** https://blog.superhuman.com/superhuman-ai

### Shortwave (AI inbox bundles)

**Use for:** AI-organized bundles + thread summaries + AI search.
**Skill pack:** [`email-triage-superhuman-shortwave`](skills/email-triage-superhuman-shortwave/SKILL.md)
**Install:** Web + mobile
**Source:** https://www.shortwave.com/

### Todoist (cross-platform GTD)

**Use for:** Largest GTD ecosystem; Natural Language; cross-platform.
**Skill pack:** [`task-mgmt-todoist-things-notion`](skills/task-mgmt-todoist-things-notion/SKILL.md)
**Install:** All platforms; REST API
**Quick recipe:**
```bash
# Create task
curl -X POST https://api.todoist.com/rest/v2/tasks \
  -H "Authorization: Bearer $TODOIST_TOKEN" \
  -d '{"content":"Q3 strategy doc","due_string":"tomorrow at 10am"}'
```
**Source:** https://developer.todoist.com/

### Things 3 (Apple-only GTD)

**Use for:** Apple-only single-purchase clean GTD.
**Skill pack:** [`task-mgmt-todoist-things-notion`](skills/task-mgmt-todoist-things-notion/SKILL.md)
**Install:** Mac/iOS; URL scheme for automation
**Quick recipe:**
```bash
# Create task via URL scheme
open "things:///add?title=Q3+Strategy+Doc&when=tomorrow&list=Work"
```
**Source:** https://culturedcode.com/things/support/articles/2803573/

### 1Password (password vault + secrets)

**Use for:** Vault + family/team sharing + Watchtower + Developer integration.
**Skill pack:** [`password-mgmt-1password-bitwarden`](skills/password-mgmt-1password-bitwarden/SKILL.md)
**Install:** `op` CLI
**Quick recipe:**
```bash
op signin
op item get "GitHub" --fields password
op item create --category=login --title="MyService" username=me --generate-password=20
```
**Source:** https://developer.1password.com/docs/cli/

### Loom (async video)

**Use for:** Screen + face recorder + transcript + comment.
**Skill pack:** [`async-video-loom`](skills/async-video-loom/SKILL.md)
**Install:** Mac/iOS/Windows + Chrome ext + REST
**Source:** https://dev.loom.com/

### Rocket Money (subscription tracker)

**Use for:** Auto-detect + cancellation negotiation.
**Skill pack:** [`subscription-tracker-cancellation`](skills/subscription-tracker-cancellation/SKILL.md)
**Install:** Mobile + web + bank-link OAuth
**Source:** https://www.rocketmoney.com/

### Cozi (family organizer)

**Use for:** Family-specific calendar + meal + shopping + chore.
**Skill pack:** [`family-calendar-coordination`](skills/family-calendar-coordination/SKILL.md)
**Install:** Mobile + web (limited API)
**Source:** https://www.cozi.com/

### Notion (personal wiki + KB)

**Use for:** Personal wiki, gift log, contacts DB, family calendar.
**Skill pack:** (used by many)
**Install:** Web + mobile + native
**Quick recipe:**
```bash
# Search / create via notion-mcp
# See notion-mcp tool docs
```
**Source:** https://developers.notion.com/

### Home Assistant (open-source smart home)

**Use for:** DIY + most flexible smart-home integration.
**Skill pack:** (via `hass-mcp` + `automation-workflows`)
**Install:** Self-host (Pi / container) + Home Assistant OS
**Source:** https://www.home-assistant.io/

### Apple Shortcuts (iOS/macOS automation)

**Use for:** Personal automation; free.
**Skill pack:** (via `automation-workflows`)
**Install:** Built into iOS / macOS
**Source:** https://www.icloud.com/shortcuts/

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Block my calendar" / "protect focus" | `calendar-protection-motion-reclaim-sunsama` | Motion or Reclaim depending on user app preference |
| "Send me a Calendly link" | `scheduling-calendly-cal-com-oncehub` | Cal.com if self-host preferred |
| "Book a flight to X" | `travel-booking-tripit-hopper-kayak` | + `google-flights-mcp` |
| "File my expense report" | `expense-tracking-expensify-ramp-brex` | + OCR + Expensify REST |
| "Get me a table at [restaurant]" | `restaurant-reservations-opentable-resy-tock` | Likely surface deep-link (no consumer API) |
| "Prep me for my 1:1 with X" | `meeting-prep-briefs-from-granola-fathom` | Pull Fathom / Fireflies + compose brief |
| "Draft follow-up to today's meeting" | `follow-up-email-drafting` | Pull transcript + compose per-recipient |
| "Get my inbox to zero" | `email-triage-superhuman-shortwave` | Filter set + AI bundle + ritual schedule |
| "Add a task" | `task-mgmt-todoist-things-notion` | Default Todoist; Things for Apple-only |
| "Order dinner / groceries" | `errand-routing-doordash-uber-eats-instacart` | Likely surface deep-link |
| "Find a gift for X" | `gift-research-shopping` | + recipient log update |
| "Update my contacts" | `contact-book-maintenance-cardhop-notion` | + dedup + enrich |
| "Don't let me forget bdays" | `birthday-anniversary-tracking` | Notion DB + recurring reminders |
| "Where's my password for X?" | `password-mgmt-1password-bitwarden` | + 1Password CLI |
| "Send a Loom to X" | `async-video-loom` | Draft script + outline + share-to email |
| "Audit my subscriptions" | `subscription-tracker-cancellation` | + personal finance MCPs |
| "Sync our family calendar" | `family-calendar-coordination` | + Google / Apple Family |
| "Plan our trip to X" | `vacation-planning-end-to-end` | Multi-step over multiple sessions |
| "Turn off all lights" / "smart home" | `automation-workflows` + smart-home MCPs | + `hass-mcp` / `home-assistant-mcp` |
| "Find me a hotel" | `travel-booking-tripit-hopper-kayak` | + `booking-mcp` / `amadeus-hotels-mcp` |

---

## Brief / Output templates

### Travel itinerary template (Notion / docx)

```markdown
# Trip: [Destination] — [Dates]

**Party:** [Names]
**Budget:** [Total]
**Goals:** [What's the point of this trip]

## Departure
- Date: [Date]
- Flight: [Carrier + #]
- Confirmation: [#]
- Ground transport: [Method]
- Departure airport arrival: [Time + buffer]

## On-trip
[Per-day breakdown — see Vacation brief template]

## Return
- Date: [Date]
- Flight: [Carrier + #]
- Confirmation: [#]
- Ground transport: [Method]
- Out-of-office removed: [Date]

## References
- TripIt itinerary: [link]
- Calendar holds: [confirmed]
- Reminders set: [list]
- Loyalty status applied: [carriers]
```

### Meeting follow-up email template

```markdown
Subject: Follow-up from our [Topic] discussion

Hi [Name],

Thanks for the conversation today. Quick recap of what we landed on:

**You're going to:**
- [Action item with deadline]
- [Action item with deadline]

**I'll handle:**
- [Action item with deadline]
- [Action item with deadline]

**Open thread for next time:**
- [Topic to revisit]

Let me know if I missed anything. Looking forward to following up.

Best,
[Name]
```

### Birthday / anniversary reminder template

```markdown
# Upcoming: [Name]'s [Birthday/Anniversary] — [Date]

## Lead-time milestones
- T-14d (today): Gift research + decide
- T-7d: Gift ordered
- T-3d: Card / message drafted; dinner reservation booked
- Day-of: Send message; celebrate

## Recipient context (from gift log)
- Last gift: [Item, year, reaction]
- Interests: [...]
- Sizes / dietary: [...]
- Avoid: [...]

## Suggested gifts (from research)
1. [...] — [reason]
2. [...] — [reason]
3. [...] — [reason]

## Action
[Recommended choice + order link]
```

---

## Closing rules

Time blocks beat to-do lists; one-way doors deserve a moment; defaults beat decisions. When in doubt, the bookable / actionable / followable artifact wins over the advice / brainstorm / option-list. Calendar slot present + confirmation number recorded + TZ-explicit + reminder triggered + family-anchors protected + deferral disclosed when binding tax / legal. Defer binding personal tax / legal to a licensed CPA / attorney; company HR / IT / vendor ops to `operations-agent`; strategic exec / board work to `ceo-agent`; business finance / books to `finance-controller`.
