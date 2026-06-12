# Personal Assistant — Sources

> Section→source map for `soul.md` and `role.md`. Ships in the bundle but is **not** loaded into the agent's context. For humans verifying provenance and for future updates.

## soul.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Title + persona intro | Synthesis of seed prompt + SOTA research in `reference/SOTA_USE_CASES.md` | Action-verb-first per build instructions; 20+ verbs |
| Purpose | Synthesis of seed prompt convictions + `reference/SOTA_USE_CASES.md` | |
| Execution stack | `reference/SOTA_USE_CASES.md` (skill packs from seed prompt) | 18 skill packs reserved for Round 2 |
| When invoked | Per-mode entry procedures derived from SOTA mapping + Operations Agent shape | Mirrors operations-agent mode-structure but personal-scope |
| Core operating rules | Synthesis of seed prompt convictions + GTD / Inbox Zero / time-management canon (Allen / Mann / Forte) | |
| Mode-specific decisions | Per-mode quality bars derived from SOTA tool capability | |
| Quality gates | Derived from mode-specific quality bars + operational discipline principles | |
| Output format | Per-output convention | |
| Communication style | Synthesis from operations-agent shape + personal-assistant tone calibration | |
| When to push back / defer | Sibling-agent hand-off list per seed prompt + CraftBot catalog | |
| PROACTIVE self-init footer | `METHODOLOGY.md` standard footer | Routine questions adapted for personal scope |

## role.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Capability reference | `reference/SOTA_USE_CASES.md` (tool inventory per category) | |
| Calendar protection playbook | Motion + Reclaim.ai + Sunsama docs (https://docs.usemotion.com/, https://reclaim.ai/api, https://www.sunsama.com/) | |
| Scheduling playbook | Calendly + Cal.com docs (https://developer.calendly.com/, https://cal.com/docs) | |
| Travel booking playbook | TripIt + Hopper + Google Flights references (https://tripit.github.io/api/, https://www.hopper.com/) | |
| Expense filing playbook | Expensify Integration Server docs (https://integrations.expensify.com/Integration-Server/doc/) | |
| Inbox triage playbook | Shortwave inbox zero method (https://www.shortwave.com/blog/inbox-zero-2026) + Merlin Mann inbox-zero principle | |
| Vacation planning playbook | TripIt + Wirecutter + Wired travel-planning references (https://www.tripit.com, https://www.wired.com/story/best-travel-planning-apps) | |
| Subscription audit playbook | Rocket Money + YNAB + Lunch Money + Actual Budget references (https://www.rocketmoney.com/, https://www.lunchmoney.app/) | |
| Family calendar playbook | Cozi + Google Family Sharing (https://www.cozi.com/, https://support.google.com/calendar/answer/37082) | |
| Gift research playbook | NYT Wirecutter Gift Guides (https://www.nytimes.com/wirecutter/gifts/) | |
| Meeting prep playbook | Fathom + Fireflies + Granola transcript-pull mechanics (https://docs.fathom.video/api/, https://granola.ai/) | |
| Async standup playbook | Geekbot + Range + Standuply references (https://geekbot.com/blog/best-async-standup-tools, https://www.range.co/) | |
| Smart home playbook | Home Assistant integrations (https://www.home-assistant.io/integrations/) | |
| Antipattern catalog | Synthesis from GTD / time-management canon + operational discipline | |
| SOTA tool reference | `reference/SOTA_USE_CASES.md` + per-tool docs | See SOTA sources table below |
| SOTA execution playbook | `reference/SOTA_USE_CASES.md` mapping | |
| Brief / Output templates | Derived from per-mode quality bars + standard professional templates | |

## SOTA tool sources (June 2026)

> One row per SOTA tool referenced in the agent.

| Tool | Source URL | Used for |
|---|---|---|
| Motion | https://docs.usemotion.com/ | AI auto-scheduler; calendar + tasks + projects in one app |
| Reclaim.ai | https://reclaim.ai/api | Smart 1:1s; Habits; Analytics; Google Calendar overlay |
| Sunsama | https://www.sunsama.com/ | Daily ritual planning; multi-source task pull |
| Reclaim Motion comparison | https://reclaim.ai/blog/motion-vs-reclaim-2026 | Calendar AI scheduler comparison |
| Sunsama Best Daily Planner | https://www.sunsama.com/blog/best-daily-planner-2026 | Daily ritual platform landscape |
| Calendly | https://developer.calendly.com/api-docs/ | Scheduling links + REST CRUD |
| Cal.com | https://cal.com/docs | Open-source scheduling + self-host |
| Calendly vs Cal.com vs SavvyCal | https://www.calendly.com/blog/calendly-vs-cal-com-vs-savvycal-2026 | Scheduling platform comparison |
| TripIt | https://tripit.github.io/api/ | Itinerary auto-parse + flight tracking |
| TripIt Developer | https://www.tripit.com/web/developer | Developer docs |
| Hopper | https://www.hopper.com/ | Predictive flight pricing |
| Google Flights | (via google-flights-mcp) | Flight metasearch |
| NerdWallet Best Flight Search Engines | https://www.nerdwallet.com/article/travel/best-flight-search-engines | Flight search landscape |
| Wired Best Travel Planning Apps | https://www.wired.com/story/best-travel-planning-apps | Vacation planning toolchain |
| Expensify Integration Server | https://integrations.expensify.com/Integration-Server/doc/ | Expense report CRUD via REST |
| SoftwareSuggest Expense Tracking | https://www.softwaresuggest.com/blog/expense-tracking-software-comparison-2026 | Expense platform comparison |
| OpenTable Platform Affiliate | https://platform.opentable.com/documentation/ | Reservation API surface; affiliate gating |
| Granola | https://granola.ai/ | AI native meeting note-taker |
| Fathom Docs | https://docs.fathom.video/api/ | Meeting transcript pull via REST |
| Superhuman AI | https://blog.superhuman.com/superhuman-ai | AI email assistant |
| Shortwave Best Email Clients | https://www.shortwave.com/blog/best-email-clients-2026 | Email client landscape |
| Shortwave Inbox Zero | https://www.shortwave.com/blog/inbox-zero-2026 | Inbox zero method 2026 |
| Zapier Best To-Do List Apps | https://www.zapier.com/blog/best-todo-list-apps | Task management comparison |
| Things by Cultured Code | https://culturedcode.com/things/support/articles/2803573/ | Things URL scheme |
| Todoist Developer | https://developer.todoist.com/ | Todoist REST API |
| DoorDash Developer | https://developer.doordash.com/en-US/ | DoorDash Drive API (partner-only) |
| NYT Wirecutter Gifts | https://www.nytimes.com/wirecutter/gifts/ | Curated gift research source |
| Flexibits Cardhop | https://www.flexibits.com/cardhop | Personal CRM (Mac/iOS) |
| Clay | https://clay.com/ | Personal CRM + relationship intelligence |
| Notion Birthday Template | https://www.notion.so/templates/birthday-tracker | Birthday tracking pattern |
| 1Password CLI | https://developer.1password.com/docs/cli/ | Vault access + secret injection |
| Loom Developer | https://dev.loom.com/ | Async video metadata + share-link CRUD |
| Rocket Money | https://www.rocketmoney.com/ | Subscription tracker + cancellation |
| Lunch Money | https://www.lunchmoney.app/ | Personal finance + budget |
| Cozi | https://www.cozi.com/ | Family calendar + meal + chore + shopping |
| Google Family Sharing | https://support.google.com/calendar/answer/37082 | Shared calendar pattern |
| Zocdoc | https://www.zocdoc.com/about | Doctor finder + Partner API gating |
| SeatGeek Platform | https://www.seatgeek.com/platform/ | Event ticket API |
| CarFax | https://www.carfax.com/ | Car maintenance schedule reference |
| Rinse | https://www.rinse.com/ | Dry-cleaning pickup |
| Geekbot Best Async Standup | https://geekbot.com/blog/best-async-standup-tools | Async standup tooling |
| Range | https://www.range.co/ | Async standup + week-in-review |
| Home Assistant Integrations | https://www.home-assistant.io/integrations/ | Smart home integration catalog |
| Zapier Best Automation Software | https://www.zapier.com/blog/best-automation-software/ | Personal automation comparison |

## Notes on authored-from-synthesis

Sections that aren't directly lifted from a single source (rare — operational glue):

- **Purpose paragraph** — synthesized from the seed prompt's convictions + the SOTA mapping; not a direct lift from any single source.
- **Core operating rules** — synthesized from GTD / time-management canon (Allen / Mann / Forte) + operational discipline principles. Each rule is rooted in a documented best-practice but the phrasing is composed for this agent's voice.
- **Mode-specific decisions** — composed quality bars per mode based on SOTA tool capability.
- **Antipattern catalog** — synthesis from time-management canon + observed personal-ops patterns. BAD/GOOD pairs are illustrative.
- **Output templates** — composed templates conforming to standard professional norms (itinerary, follow-up email, brief, standup).

## Refreshing from upstream

When SOTA tools change (e.g., Brex API surface evolves post-Capital One; Calendly v2 launches; new email client surpasses Superhuman):

1. Update the relevant skill pack(s) in `agents/personal-assistant/skills/<name>/SKILL.md`.
2. Update the SOTA sources table above.
3. Update `reference/SOTA_USE_CASES.md` confidence ratings if applicable.
4. Re-run `python verify.py personal-assistant` to confirm structure intact.
5. Re-build: `python build.py personal-assistant` produces a fresh `.craftbot`.

For the canonical reference repos (Step 2 of methodology):
- `wshobson/agents` — repull every quarter for SOTA agent definitions; recheck for productivity / personal-assistant plugins.
- `VoltAgent/awesome-claude-code-subagents` — same cadence.
- `msitarzewski/agency-agents` — same cadence; recheck EA / chief-of-staff coverage.
- `JSONbored/claudepro-directory` — same cadence.
