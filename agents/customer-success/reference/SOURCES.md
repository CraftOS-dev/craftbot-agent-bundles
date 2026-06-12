# Customer Success — Source Attribution

Section-to-source map for `soul.md` and `role.md`. **Not** loaded into context — for human verification.

Authoritative SOTA mapping lives at `reference/SOTA_USE_CASES.md`. URLs in `agent.yaml → sources`.

This agent's v1 build pass derived its SOTA content from direct web research on the 2026 customer-success platform stack rather than downloaded reference agent files. Round 2 of the methodology can backfill `reference/agents/` with downloads from wshobson/agents, VoltAgent/awesome-claude-code-subagents, msitarzewski/agency-agents.

This agent is **distinct from `customer-support-agent`** — different motion (proactive vs reactive). Voice + structure mirror the adjacent agent but content is independently sourced.

---

## soul.md → source map

| Section | Source(s) |
|---|---|
| Opening identity + 3 convictions | composition synthesis distilling load-bearing rules from CS doctrine: Vitally / Gainsight playbooks (NRR > GRR > new logo); success-plan-as-outcome industry practice; ChurnZero / Catalyst onboarding doctrine (renewal starts on day 1) |
| Distinction from customer-support-agent | adjacent agent definition at `agent_bundle/agents/customer-support-agent/` — explicit motion difference |
| Purpose | composition from Vitally + Gainsight + ChurnZero + Pendo customer-journey doctrine + bug-normalization / VOC industry practice |
| Execution stack | `reference/SOTA_USE_CASES.md` — one bullet per bundled skill pack, named per Round 1 prompt |
| When invoked — Onboarding mode | Vitally Projects + Pendo Engage + Day 0-90 industry framework |
| When invoked — Success plan mode | Catalyst Playbooks + Vitally Projects + outcome-led framework |
| When invoked — QBR mode | Calendly + Zoom + Fathom + PostHog + PPTX industry-standard QBR cadence |
| When invoked — Health scoring mode | Vitally / Catalyst / ChurnZero / Gainsight health score doctrine + composite formula industry pattern |
| When invoked — NRR / GRR mode | Stripe + Salesforce + industry-standard NRR/GRR cohort math |
| When invoked — Expansion mode | Pocus / Common Room / Endgame PLG signal doctrine + composite scoring |
| When invoked — Renewal mode (90-day) | industry-standard T-90 / T-60 / T-30 / T-7 cadence + PandaDoc / DocuSign workflow |
| When invoked — Churn save mode | ChurnZero AI / Vitally AI / Sturdy + industry-standard save play |
| When invoked — Advocacy mode | Influitive + Delighted promoter pipeline + Stripe credit / Tremendous reward fulfillment |
| When invoked — Voice-of-customer mode | multi-source synthesis pattern (interviews + NPS + tickets + CSP) + Linear handoff |
| When invoked — CAB mode | Bevy / Slack Connect / Discord CAB community pattern |
| When invoked — In-app onboarding mode | Pendo + Userpilot + Appcues flow design pattern |
| When invoked — Survey ops mode | Delighted + Survicate + Sprig multi-event survey cadence |
| Core operating rules | merged from CS platform doctrine: Vitally (NRR > GRR > new logo); Catalyst (outcomes not features); Gainsight (renewal starts on day 1); industry health-score honesty rule; multi-threading enterprise patterns; voice-of-customer Linear handoff industry rule |
| Mode-specific decisions | one entry per mode keyed to the matching platform / tool reference |
| Quality gates | platform-native quality gates: Vitally Project structure, Catalyst Playbook structure, Statuspage-equivalent renewal-board structure, Delighted detractor auto-routing, Linear VOC handoff |
| Output format | composition from each platform's canonical formats (Vitally Project, Catalyst Playbook, PandaDoc proposal, PPTX QBR deck, Notion success plan / CAB roster / VOC report) |
| Communication style | distilled from voice doctrine across Vitally + Catalyst + ChurnZero best-practice; AI-slop catch list adapted from customer-support-agent's voltagent-content-quality-editor pattern, narrowed to CS-specific phrases (sales-y openers, performative empathy, fake commitment) |
| When to push back | composition synthesis informed by roadmap-honesty rule, health-score honesty rule, commercial-deferral rule, success-plan outcome rule |
| When to defer | composition synthesis with explicit sibling-agent hand-offs (sales-agent, product-manager, marketing-agent, customer-support-agent, finance-controller, legal-counsel, technical-writer, ux-researcher, senior-python-engineer) |
| First-conversation routine questions | standard PROACTIVE.md self-init pattern (METHODOLOGY.md decision #3); questions adapted to CS workflows (CSP / NRR target / primary churn driver) |
| Closing rule | distilled summary of the three convictions + sibling-agent hand-off pattern |

---

## role.md → source map

| Section | Source(s) |
|---|---|
| Capability reference → CSPs | Vitally / Catalyst / Gainsight / ChurnZero / Totango / Custify / Velaris / Planhat vendor docs |
| Capability reference → Health + churn AI | ChurnZero AI / Vitally AI / Sturdy / Custify AI vendor docs |
| Capability reference → In-product onboarding | Pendo / Userpilot / Appcues / Chameleon / Whatfix / ProductFruits vendor docs |
| Capability reference → Product analytics tied to CS | PostHog / Mixpanel / Amplitude / Heap / FullStory / LogRocket vendor docs |
| Capability reference → Customer comms + outreach | Mixmax / Outreach / Salesloft / Klaviyo / Customer.io / Iterable vendor docs |
| Capability reference → Customer interview / call | Calendly / Zoom / Granola / Fathom / tl;dv / Otter.ai vendor docs |
| Capability reference → Survey / VoC | Delighted / Survicate / Sprig / Wootric / Iterate / Hotjar / Typeform vendor docs |
| Capability reference → Renewal + commercial | Stripe Subscriptions / Salesforce CPQ / Zuora / PandaDoc / DocuSign / Ironclad vendor docs |
| Capability reference → Advocacy + reference | Influitive / Slapfive / UserEvidence / Champion vendor docs |
| Capability reference → Customer academy / certification | Skilljar / Northpass / WorkRamp / Intellum vendor docs |
| Capability reference → Referral programs | Friendbuy / Referral Rock / Mention Me / GrowSurf / Tremendous vendor docs |
| Capability reference → PLG + community signals | Pocus / Koala / Endgame / Common Room vendor docs |
| Capability reference → CAB community | Bevy / Mighty Networks / Slack Connect / Discord vendor docs |
| Capability reference → CRM | HubSpot / Salesforce / Attio / Pipedrive / Zoho vendor docs |
| Capability reference → Warehouse + reverse-ETL + BI | PostgreSQL / Census / Hightouch / dbt / Metabase / Looker / Hex / Mode vendor docs |
| Onboarding playbook + Day 0-90 framework | composition synthesis from Vitally Projects + Gainsight Customer Journey + Pendo Engage + industry-standard onboarding doctrine |
| Onboarding plan template | composition synthesis informed by Vitally Project schema + industry-standard milestone-driven onboarding |
| Success plan playbook + template | composition synthesis from Catalyst Playbooks + Vitally Projects + Gainsight success-plan patterns; outcomes-not-features rule from industry CS best practice |
| QBR playbook + T-21 cadence | composition synthesis from Gainsight / Catalyst / Vitally QBR doctrine + industry-standard 15-slide deck template |
| QBR deck template (15 slides) | composition synthesis from Gainsight / Vitally / Catalyst QBR pattern + customer-success industry best practice |
| Action item recap template | composition synthesis from common QBR post-meeting communication patterns |
| Health scoring playbook + composite formula | composition synthesis from Vitally / Catalyst / Gainsight / ChurnZero composite-formula patterns; weights (40/20/15/10/10/5) are industry baseline (recipient should tune) |
| Risk flags + CSP writeback patterns | composition synthesis from CSP integration patterns; Vitally REST `/customers/<id>/traits` is canonical |
| Free fallback (dbt nightly model) | composition synthesis from dbt + HubSpot custom property pattern documented in HubSpot dev docs |
| NRR GRR playbook + cohort SQL | composition synthesis from Stripe Subscriptions API + standard SaaS cohort-revenue computation (industry definition: NRR = (S + E - C - X) / S, GRR = (S - C - X) / S) |
| Expansion opportunity playbook + composite score | composition synthesis from Pocus / Common Room PLG-signal patterns + PostHog HogQL cohort patterns; weights (30/25/20/15/10) are industry baseline |
| Expansion outreach template | composition synthesis from CSM-led usage-uplift outreach best practice |
| Renewal playbook (90-day) + T-90/60/30/7 cadence | composition synthesis from industry-standard 90-day renewal preparation doctrine + PandaDoc / DocuSign workflow |
| Renewal pricing template (xlsx) | composition synthesis from CPQ pricing-uplift pattern + multi-year discount industry standard |
| Forecast accuracy logging | composition synthesis from Clari / Salesforce CPQ forecast-discipline pattern |
| Churn save playbook + signal trigger | composition synthesis from ChurnZero AI / Vitally AI / Sturdy save-motion patterns + industry-standard 4-of-6 composite trigger rule |
| Save plan template | composition synthesis from industry-standard save-play structure |
| At-risk identification playbook + nightly SQL | composition synthesis from Vitally + Catalyst at-risk view patterns + Postgres warehouse implementation |
| In-app onboarding playbook + flow schema (JSON) | composition synthesis from Pendo Engage + Userpilot + Appcues flow definition patterns; JSON schema is illustrative |
| A/B test pattern | composition synthesis from PostHog cohort + Pendo/Userpilot variant patterns |
| Survey ops playbook + cadence table | composition synthesis from Delighted / Survicate / Sprig recommended cadence + industry-standard CSAT/CES/NPS post-event delivery |
| Detractor / promoter playbook | composition synthesis from Delighted recommended detractor handling + Influitive promoter qualification |
| Voice of customer playbook + synthesis process | composition synthesis from multi-source VOC industry pattern + embedding cluster pattern + product-routing best practice |
| VOC report template | composition synthesis from industry-standard VOC-to-product report structure |
| CAB playbook + roster + cadence | composition synthesis from Bevy + Slack Connect + Discord CAB patterns + industry-standard 8-12 customer roster |
| Quarterly CAB agenda | composition synthesis from common CAB facilitation patterns |
| Advocacy playbook + promoter qualification | composition synthesis from Influitive + Delighted promoter-pipeline patterns + industry-standard advocacy ask hierarchy |
| Advocacy outreach template | composition synthesis from Influitive + Slapfive outreach best practice |
| Referral playbook | composition synthesis from Friendbuy + Referral Rock + Tremendous referral-program patterns |
| Adoption tracking playbook + SQL view | composition synthesis from PostHog HogQL + Pendo Adopt + Amplitude/Mixpanel cohort patterns |
| Adoption score formula | composition synthesis from industry-standard composite adoption score; weights (40/30/20/10) are baseline |
| Ramp-to-value playbook + TTFV/TTRV definitions | composition synthesis from PostHog funnel + Pendo Adopt + industry-standard ramp definitions |
| Multi-threading enterprise playbook | composition synthesis from Gainsight + Salesforce multi-threading doctrine + industry-standard role mapping (Champion / Sponsor / EB / Tech Eval / End Users) |
| Customer touchpoint cadence playbook | composition synthesis from Mixmax + Outreach + Salesloft tier-based cadence pattern |
| AI-slop catch list — CS edition | adapted from customer-support-agent's voltagent-content-quality-editor pattern, narrowed to CS-specific phrases ("Hope you're doing well!", "Just touching base", "Circling back", "Per my last email", "Working on it" without ticket) |
| Antipattern catalog (feature list as success plan / vanity QBR / health score dishonesty / renewal at T-30 / VOC as anecdotes / single-threaded enterprise / roadmap fabrication) | composition synthesis from common CS failure modes documented across Vitally / Catalyst / Gainsight community + industry post-mortems |
| Reporting + dashboard patterns | composition synthesis from CSP + Census/Hightouch + dbt + BI tool patterns |
| SOTA tool reference | `reference/SOTA_USE_CASES.md` — one H3 per bundled skill pack |
| Updated mappings | translation table: generic category → SOTA replacement |

---

## Notes on "authored from synthesis"

Several sections in this v1 build are composition-synthesis on top of platform documentation rather than verbatim lifts from a reference agent. This is appropriate for v1 — Round 2 can backfill with concrete reference-agent files:

- **Three opening convictions in soul.md** — distillation of CS platform doctrine: "NRR > GRR > new logo" (industry-standard CS metric hierarchy), "success plans need outcomes, not features" (Catalyst / Vitally outcome-led doctrine), "renewal starts on day 1" (Gainsight / ChurnZero onboarding-as-first-save doctrine).
- **Health score composite formula** — weights (40/20/15/10/10/5) are industry-baseline composite; recipient should tune to their business model. Documented as a starting point.
- **NRR / GRR cohort SQL** — composition synthesis from Stripe Subscriptions API + standard SaaS cohort-revenue computation; the formula itself is industry-standard.
- **Expansion composite score** — weights (30/25/20/15/10) are industry-baseline; tune per recipient.
- **At-risk identification SQL view** — composition synthesis from Vitally + Catalyst at-risk-view patterns implemented in Postgres.
- **In-app onboarding flow JSON schema** — illustrative; the actual schemas differ per platform (Pendo / Userpilot / Appcues each have their own).
- **AI-slop catch list — CS edition** — adapted from customer-support-agent's voltagent-content-quality-editor pattern, narrowed to CS-specific phrases ("Hope you're doing well!", "Just touching base", "Circling back", "Per my last email", "Working on it" without an open Linear ticket).
- **Antipattern catalog** — composition synthesis from common CS-failure modes across Vitally / Catalyst / Gainsight communities + industry post-mortems.
- **Save plan + advocacy + referral templates** — composition synthesis from industry-standard structures; not lifted from a single source.
- **First-conversation PROACTIVE.md self-init** — standard pattern from METHODOLOGY.md with CS-specific routine questions (CSP / NRR target / primary churn driver).

No fabricated benchmarks, fake quotes, or fake customer stories. All platform features cited are real and verifiable via the URLs in `agent.yaml → sources`.

---

## How to update this agent

1. **Round 2 backfill (recommended):** download 4-6 reference agents from wshobson/agents (look for `plugins/customer-success/`), VoltAgent/awesome-claude-code-subagents (categories/09-customer-success/), msitarzewski/agency-agents into `reference/agents/`. Diff against composition synthesis; tighten role.md voice where reference language is stronger.
2. **Refresh SOTA tool list:** SOTA changes monthly. Re-fetch each tool's docs URL (in `agent.yaml → sources`); update SOTA_USE_CASES.md confidence ratings if anything shifted.
3. **Refresh CraftBot MCP catalog:** if new MCPs land (e.g., Vitally MCP, Catalyst MCP, Gainsight MCP, Pendo MCP, Userpilot MCP, Delighted MCP, Influitive MCP), promote them in `agent.yaml` and update role.md SOTA tool reference.
4. **Re-run `build.py`** to regenerate the .craftbot bundle.

---

## SOTA tool sources (June 2026)

These sources back the `role.md → SOTA tool reference (June 2026)` section, the `reference/SOTA_USE_CASES.md` per-use-case mapping, and the 22 bundled skill packs in `skills/` (Round 2 populates SKILL.md contents).

| Tool | Source URL | Used for |
|---|---|---|
| Vitally API | https://docs.vitally.io/reference | `skills/customer-health-scoring-vitally-catalyst-churnzero/SKILL.md` + `skills/playbook-automation-churnzero-plays/SKILL.md` + Projects for success plans |
| Catalyst (Totango) API | https://help.catalyst.io/ | enterprise CSP alt for health scoring + playbooks |
| Gainsight Journey Orchestrator | https://help.gainsight.com/docs/journey-orchestrator/ | enterprise playbook automation alt |
| ChurnZero + ChurnZero AI | https://help.churnzero.com/hc/en-us | ChurnZero Plays + churn AI signal extraction |
| Totango / Custify / Velaris / Planhat | https://www.totango.com/docs/api | alt CSPs |
| Sturdy AI | https://www.sturdy.ai/ | AI churn signal extraction from comms data |
| Pendo Engage + Pendo Adopt | https://developers.pendo.io/ | `skills/in-app-onboarding-userpilot-appcues-pendo/SKILL.md` |
| Userpilot API | https://docs.userpilot.com/ | in-app onboarding alt |
| Appcues API | https://help.appcues.com/en/articles/123-appcues-rest-api | in-app onboarding alt |
| Chameleon + Whatfix + ProductFruits | https://help.chameleon.io/en/articles/3402836-chameleon-api | in-app onboarding alts (ProductFruits free tier) |
| PostHog Query API + Funnels + Cohorts | https://posthog.com/docs/api/queries | `skills/adoption-metric-feature-usage/SKILL.md` + `skills/ramp-to-value-tracking/SKILL.md` + `skills/expansion-opportunity-identification/SKILL.md` + churn signal detection |
| Mixpanel Query API | https://developer.mixpanel.com/reference/query-api | alt product analytics |
| Amplitude Analytics API | https://amplitude.com/docs/apis/analytics | alt product analytics |
| Heap + FullStory | https://developers.heap.io/reference | alt product analytics + session replay |
| Pocus + Koala + Endgame | https://www.pocus.com/ | PLG signal aggregation for expansion |
| Common Room API | https://docs.commonroom.io/ | community + dark social signal aggregation |
| Calendly API v2 | https://developer.calendly.com/api-docs/ | QBR + interview + reference call + CAB meeting scheduling |
| Zoom API | https://developers.zoom.us/docs/api/ | QBR + interview + CAB meeting hosting + recording |
| Fathom API | https://help.fathom.video/en/articles/8430832-fathom-api | QBR + interview transcript + action-item extraction |
| Granola + tl;dv + Otter.ai | https://www.granola.ai/ | alt AI notetakers |
| Delighted API | https://app.delighted.com/docs/api | `skills/nps-csat-ces-tracking/SKILL.md` + promoter list for advocacy + detractor escalation |
| Survicate API | https://developers.survicate.com/ | alt survey vendor |
| Sprig API | https://docs.sprig.com/ | event-triggered in-product micro-surveys |
| Wootric / InMoment | https://www.inmoment.com/ | incumbent NPS/CSAT alt |
| Mixmax API | https://help.mixmax.com/hc/en-us | renewal + customer touchpoint cadence |
| Outreach API | https://developers.outreach.io/api/ | expansion sequence orchestration + cadence alt |
| Salesloft API | https://developers.salesloft.com/api.html | alt cadence platform |
| Klaviyo API | https://developers.klaviyo.com/en/reference/api_overview | expansion email sequences (product-led) |
| Customer.io API | https://customer.io/docs/api/ | alt lifecycle email |
| Iterable API | https://api.iterable.com/api/docs | enterprise lifecycle email |
| PandaDoc API | https://developers.pandadoc.com/ | `skills/renewal-management-90-day-prep/SKILL.md` proposal generation |
| DocuSign eSign API | https://developers.docusign.com/docs/esign-rest-api/ | enterprise e-sign |
| Ironclad API | https://developer.ironcladapp.com/ | enterprise CLM alt |
| Salesforce CPQ + Zuora | https://developer.salesforce.com/docs/atlas.en-us.cpq_dev_api.meta/cpq_dev_api/ | enterprise CPQ for renewal uplift |
| Stripe Subscriptions + Billing API | https://stripe.com/docs/api/subscriptions | `skills/nrr-grr-ownership-metrics/SKILL.md` + renewal cadence + referral credits + subscription state |
| HubSpot CRM API | https://developers.hubspot.com/docs/api/crm/contacts | free CSP fallback + exec-sponsor tracking |
| Salesforce REST + SOQL | https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/ | enterprise CRM, contact-role multi-threading |
| Influitive API | https://docs.influitive.com/ | `skills/customer-advocacy-case-study-reference/SKILL.md` |
| Slapfive + UserEvidence + Champion | https://help.slapfive.com/ | alt advocacy + reference platforms |
| Skilljar API | https://help.skilljar.com/hc/en-us/categories/200182230 | `skills/success-enablement-academy-certification/SKILL.md` |
| Northpass + WorkRamp + Intellum | https://www.workramp.com/ | alt customer academy LMS |
| Friendbuy API | https://developers.friendbuy.com/ | `skills/referral-programs/SKILL.md` |
| Referral Rock + Mention Me + GrowSurf | https://www.referralrock.com/ | alt referral program platforms |
| Tremendous API | https://help.tremendous.com/hc/en-us/categories/360002107552-API | gift card / payout fulfillment for referral + advocacy |
| Bevy | https://www.bevy.com/ | CAB community platform |
| Slack Connect API | https://api.slack.com/connect | B2B Slack channels + CAB |
| PagerDuty REST API | https://developer.pagerduty.com/api-reference/ | at-risk customer escalation on-call (rare) |
| Notion API | https://developers.notion.com/ | success plans + CAB roster + VOC insights DB + renewal board + advocacy tracker fallback |
| Census + Hightouch reverse-ETL | https://docs.getcensus.com/ | CSP + analytics → warehouse → BI |
| Native CraftBot MCPs (`linear-mcp`, `jira-mcp`, `slack-mcp`, `discord-mcp`, `discord-mcp-full`, `ms-teams-mcp`, `twilio-mcp`, `stripe-mcp`, `posthog-mcp`, `mixpanel-mcp`, `amplitude-mcp`, `deepl-mcp`, `gmail-mcp`, `outlook-mcp`, `notion-mcp`, `postgresql-mcp`, `canva-mcp`, `figma-mcp`, `imagegen-mcp`, `playwright-mcp`, `firecrawl-mcp`, `brightdata-mcp`, `zoom-mcp`) | `agent.yaml` | per-platform execution surface for outreach, comms, escalation, analytics, multilingual, design, scraping, scheduling |

**Total:** 22 bundled skill packs (Round 2 fills SKILL.md) + 23 native MCPs + ~25 external SaaS APIs (paid + free fallbacks documented) covering ~95% of `USE_CASES.md` documented use cases. See `reference/SOTA_USE_CASES.md` for the per-use-case confidence map.
