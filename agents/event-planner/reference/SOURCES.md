# Event Planner — Sources

This file is the section→source map for `soul.md` and `role.md`. Ships in the bundle but is **not** loaded into the agent's context. For humans verifying provenance and for future updates.

The v1 build pass derived the SOTA mapping from web research + the per-agent seed prompt's curated 2026 tool list rather than downloading upstream agent definitions. For future tightening, follow the upstream-research path documented in `reference/INVENTORY.md`.

## soul.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Title + persona intro | Per-agent seed prompt convictions + `reference/SOTA_USE_CASES.md` SOTA tool mapping | Action-verb-first per template mandate |
| Purpose | Per-agent seed prompt sibling-agent hand-offs + `reference/SOTA_USE_CASES.md` use case categories | |
| Execution stack | `reference/SOTA_USE_CASES.md` recommended skill packs section | 23 bundled skill packs named; full how-to lives in each `skills/<name>/SKILL.md` (Round 2 generates) |
| When invoked | PCMA 2026 + MPI + Bizzabo + Cvent platform docs per mode | Mode-specific decision tree per Step 4 SOTA research |
| Core operating rules | MPI Anatomy of a Venue Contract (F&B floor, attrition cap, force majeure scope) + ADA Title III + 72-hour catering count convention | |
| Mode-specific decisions | `reference/SOTA_USE_CASES.md` per-use-case mechanism | |
| Quality gates | Per-mode QA from each skill pack's domain (Cvent reg flow, MPI contract redline, run-of-show 5-column format, BEO 72-hour lock) | |
| Output format | Industry-standard formats (BEO, run-of-show cue sheet, sponsor prospectus pptx, emergency action plan) | |
| Communication style | Voice + AI-slop discipline (consistent with marketing-agent + pr-comms peer agents) | |
| When to push back / defer | Per-agent seed prompt sibling-agent hand-offs (marketing-agent, pr-comms, bd-partnerships, operations-agent, customer-success) | |
| PROACTIVE self-init footer | `agent_bundle/METHODOLOGY.md` standard footer | Same wording across all agents; only routine questions adapted |

## role.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Capability reference | Per-platform docs (Cvent / Bizzabo / Splash / Eventbrite / RingCentral Events / Whova / Brella / Swapcard / Sessionize / Restream / OBS / Slido) + 2026 SOTA event tech comparison posts | |
| Event format decision tree | PCMA 2026 Business Events Industry Outlook (cost benchmarks) + Bizzabo event ROI data + per-agent seed prompt audience categorization | |
| Venue contract redline checklist | MPI Anatomy of a Venue Contract + eventmanagerblog.com event contract guide + post-2020 force majeure scope conventions | |
| Run-of-show template | eventmanagerblog.com run-of-show template + broadcast-style 5-column cue sheet (Time / Item / Speaker / A/V Cue / Notes) | |
| Speaker management playbook | Cvent SpeakerHub docs + speaker bureau outreach norms (BigSpeak / All American Speakers Bureau) + Sessionize CFP workflow | |
| Sponsor management framework | eventmanagerblog.com sponsorship management + Ungerboeck sponsorship + Bizzabo Klik SmartBadge lead capture | |
| BEO catering template | Cvent Catering & Banquets Module docs + 72-hour count lock industry convention + ADA Title III dietary accommodation | |
| Accessibility ADA Title III audit | ADA Title III + Section 36.303 + AccessibleArts.org event accessibility checklist + Aberdeen CART + Sorenson ASL booking norms | |
| ROI measurement formula | Bizzabo event ROI calculation + PCMA 2026 cost-per-attendee benchmarks + multi-touch attribution windows (90/180/365 days) | |
| Day-of operations playbook | Cvent OnArrival check-in + composite of vendor docs (PSAV/Encore/Freeman ops norms) + emergency action plan industry standards | |
| Post-event distribution playbook | Bizzabo Marketing Hub + Klaviyo post-event email lifecycle + YouTube + OpenAI Whisper transcription | |
| Crisis / contingency playbook | NFPA emergency action plan + post-2020 force majeure conventions + venue safety officer sign-off norms | |
| MC briefing template | Composite of MC briefing norms + emergency script templates | |
| Emergency action plan template | NFPA + venue safety officer sign-off + ADA accessibility for evacuation | |
| SOTA tool reference | `reference/SOTA_USE_CASES.md` + per-tool docs (Cvent / Bizzabo / Splash / etc.) | One H3 per tool with skill pack pointer |
| SOTA execution playbook | `reference/SOTA_USE_CASES.md` per-use-case mechanism mapping | Quick-lookup table for agent retrieval |

## SOTA tool sources (June 2026)

| Tool | Source URL | Used for |
|---|---|---|
| Cvent Supplier Network | https://www.cvent.com/en/event-marketing-management/venue-sourcing-software | Venue sourcing API; hospitality marketplace RFP issuance |
| Cvent Passkey | https://www.cvent.com/en/hospitality-cloud/passkey | Room block management; attrition tracking |
| Cvent OnArrival | https://www.cvent.com/en/event-marketing-management/on-arrival-event-check-in-software | Badge printing on demand; check-in kiosk |
| Cvent Catering & Banquets | https://www.cvent.com/en/event-marketing-management/event-catering-software | BEO drafting; dietary capture |
| Bizzabo / Klik SmartBadge | https://www.bizzabo.com/klik | NFC lead capture; sponsor booth coordination |
| Splash | https://splashthat.com | Brand-first event websites; marketing-led mid-market events |
| Eventbrite Platform API | https://www.eventbrite.com/platform/api | Consumer high-volume ticketing |
| RingCentral Events (Hopin) | https://hopin.com/developers | Virtual-native + hybrid event platform |
| Whova API | https://whova.com/api | Mobile app primary; affordable event tier |
| Brella Matchmaking | https://brella.io | AI-driven networking; interest taxonomy + meeting scheduling |
| Swapcard | https://www.swapcard.com | Event experience + content + matchmaking combined |
| Sessionize | https://sessionize.com | Conference CFP platform; track design; speaker management |
| Papercall | https://www.papercall.io | Open-source community CFP |
| Pretalx | https://pretalx.com | Open-source CFP + agenda |
| Slido (Cisco) | https://www.slido.com/api | Moderated Q&A; live polls |
| Restream | https://restream.io | Multi-platform broadcast; cloud streaming |
| StreamYard | https://streamyard.com | Browser-based cloud streaming |
| Riverside Studio | https://riverside.fm | Separate-track podcast recording; cloud studio |
| OBS Studio | https://obsproject.com | Open-source hybrid multi-cam production |
| Demio | https://demio.com | No-download marketing webinars |
| Livestorm | https://livestorm.co | Evergreen + on-demand webinars |
| Encore Global | https://www.encoreglobal.com | A/V vendor (venue-tied + custom builds) |
| Freeman | https://www.freeman.com | A/V vendor (custom builds + enterprise) |
| MPI Venue Contract guide | https://www.mpi.org/blog/article/the-anatomy-of-a-venue-contract | Venue contract redline checklist |
| Eventmanagerblog Event Contract | https://www.eventmanagerblog.com/event-contract | Contract redline + force majeure scope post-2020 |
| Eventmanagerblog Run-of-Show | https://www.eventmanagerblog.com/run-of-show-template | 5-column cue sheet format |
| Eventmanagerblog Sponsorship | https://www.eventmanagerblog.com/sponsorship-management | Sponsor tier definitions + contract-as-tracker |
| Eventmanagerblog Photography | https://www.eventmanagerblog.com/event-photography-checklist | Photographer brief + shot list |
| Eventmanagerblog MC Host | https://www.eventmanagerblog.com/mc-host-event | MC briefing template |
| Eventmanagerblog Sponsorship Prospectus | https://www.eventmanagerblog.com/sponsorship-prospectus | Sponsor prospectus pptx structure |
| Ungerboeck sponsorship management | https://www.ungerboeck.com/sponsorship-management | Sponsor deliverable tracking conventions |
| Aberdeen CART | https://www.aberdeen.com | CART captioning vendor for accessibility |
| 3PlayMedia | https://www.3playmedia.com | Alt CART captioning vendor |
| Sorenson Communications | https://sorenson.com | ASL interpretation vendor |
| Purple Communications | https://www.purple.us | Alt ASL interpretation vendor |
| ADA Title III + Section 36.303 | https://www.ada.gov/topics/title-iii/ | ADA accessibility mandate |
| AccessibleArts.org checklist | https://accessibleartsdesign.org/event-accessibility-checklist/ | Accessibility provisions for events |
| GatherGuard event insurance | https://gatherguard.com | Event cancellation + GL insurance |
| Eventsured | https://eventsured.com | Alt event insurance |
| Delighted NPS | https://delighted.com | Post-event NPS measurement |
| OpenAI Whisper | https://openai.com/research/whisper | Open-source transcription |
| OpenWeatherMap | https://openweathermap.org/api | Weather contingency forecasting |
| Swag.com | https://swag.com | Modern swag sourcing + sustainability |
| Custom Ink | https://www.customink.com | Full-service swag sourcing |
| PCMA 2026 Business Events Outlook | https://www.pcma.org/research-insights/2026-business-events-industry-outlook/ | Cost-per-attendee benchmarks; format mix |
| Bizzabo Event ROI | https://www.bizzabo.com/blog/event-roi-calculation | Pipeline-influenced revenue formula |
| MPI | https://www.mpi.org | Industry org + contract benchmarks |
| PCMA | https://www.pcma.org | Industry org + corporate events |
| IAEE | https://www.iaee.com | Industry org + trade shows |
| ILEA | https://www.ileahub.com | Industry org + production / experience |
| NACE | https://nace.net | Industry org + F&B |
| CEMA | https://cemaonline.com | Industry org + corporate marketing events |
| Bevy CMX | https://www.bevylabs.com | Community-led event management |
| Sessionize | https://sessionize.com | CFP platform |

## Notes on authored-from-synthesis

Sections that aren't directly lifted from a single source (rare — should always be operational glue, not domain claims):

- **soul.md persona intro** — synthesis from per-agent seed prompt convictions + the SOTA tool mapping in `reference/SOTA_USE_CASES.md`. The action-verb-first construction is per the `soul_md_skeleton.md` mandate.
- **soul.md execution stack list** — synthesis from `reference/SOTA_USE_CASES.md` recommended skill packs section. 23 skill packs named; per-tool how-to lives in each `skills/<name>/SKILL.md` (Round 2 generates).
- **role.md SOTA execution playbook table** — synthesis quick-lookup table from `reference/SOTA_USE_CASES.md` per-use-case mapping for agent grep-retrieval.

## Refreshing from upstream

When SOTA tools change (e.g., new event platform launch, new API endpoint, deprecated tool):
1. Update the relevant skill pack(s) in `agents/event-planner/skills/<name>/SKILL.md` (Round 2 will generate).
2. Update the SOTA sources table above.
3. Update `reference/SOTA_USE_CASES.md` confidence ratings if applicable.
4. Re-run `python verify.py event-planner` to confirm structure intact.
5. Re-build: `python build.py event-planner` produces a fresh `.craftbot`.

For the canonical reference repos:
- `wshobson/agents` — repull every quarter for SOTA agent definitions; check `plugins/operations/` and `plugins/marketing/agents/`.
- `VoltAgent/awesome-claude-code-subagents` — same cadence; check `categories/08-business-product/` and `categories/06-customer-experience/`.
- `msitarzewski/agency-agents` — same cadence; check operations + marketing folders.
- PCMA + MPI + IAEE + Bizzabo + Cvent annual reports — pull each year for fresh benchmarks.
