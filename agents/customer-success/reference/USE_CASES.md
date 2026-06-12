# Customer Success — Use Cases

**Tier:** **general** · **Category:** customer-success
**Core job:** End-to-end customer success — onboarding (Day 0/7/30/60/90), success plans, QBRs, health scoring (Vitally / Catalyst / ChurnZero / Gainsight), NRR/GRR ownership, expansion identification, 90-day renewal management, churn save motion, customer advocacy, voice-of-customer reporting, in-app onboarding (Pendo / Userpilot / Appcues), NPS/CSAT/CES tracking, CAB, referrals.

> Ships with the SOTA customer-success stack (Vitally / Catalyst / Gainsight / ChurnZero CSPs; Pendo / Userpilot / Appcues in-app onboarding; PostHog / Mixpanel / Amplitude adoption analytics; Delighted / Survicate / Sprig surveys; Mixmax / Outreach / Klaviyo cadence; Calendly / Zoom / Fathom interview + call; PandaDoc / DocuSign / Ironclad contracts; Stripe subscriptions; Influitive / Slapfive / UserEvidence advocacy; Skilljar academy; Friendbuy / Tremendous referrals; Bevy / Slack Connect / Discord CAB community) — executes end-to-end, not just direct. This file is bundled but **not** loaded into the agent's context.

> **DISTINCT from `customer-support-agent`** (reactive ticket-driven support). This agent owns the *proactive* surface: onboarding → adoption → renewal → expansion → advocacy.

---

## What this agent is supposed to do

### Customer onboarding
- Day 0 / 7 / 30 / 60 / 90 milestone framework
- Kickoff call + use-case confirmation + exec-sponsor naming
- TTFV (Time to First Value) tracking + intervention if slipping
- In-product onboarding flow design (Pendo / Userpilot / Appcues / Chameleon / Whatfix / ProductFruits)
- Email + Slack + in-app reinforcement cadence

### Success plan creation
- Outcome-led (not feature-led) goal definition
- Measurable success criteria + target date + customer-side + CSM-side owners
- Bi-weekly review cadence + monthly exec-sponsor update
- CSP Project (Vitally / Catalyst) or Notion DB fallback

### QBR scheduling + facilitation
- T-21 / T-7 / T-3 / T-0 / T+1 cadence
- Calendly round-robin booking + Zoom hosting
- Fathom transcript + Claude action-item extraction
- 15-slide deck assembly (PPTX) — Wins / Adoption / Open Items / Roadmap / Renewal Outlook
- Post-QBR action-item recap email + sync to CSP Project

### Customer health scoring
- Composite formula (adoption + CSAT/NPS + sentiment + ticket volume + exec engagement + renewal stage)
- Writeback to CSP (Vitally / Catalyst / ChurnZero / Gainsight / Totango) via REST
- HubSpot custom property fallback for no-CSP shops
- Risk flags (Red < 0.4 / Yellow 30d decline / sharp drop) → auto-escalation

### NRR / GRR ownership + metrics
- Net Revenue Retention computation from Stripe + CRM cohort
- Gross Revenue Retention by cohort
- Warehouse view (`postgresql-mcp`) refreshed nightly
- Monthly xlsx model + quarterly pptx board summary

### Expansion opportunity identification
- PostHog HogQL queries (feature-limit-hit, multi-workspace, integration-adopted)
- Pocus / Common Room / Koala / Endgame PLG signal integration
- Composite expansion score + ranked list
- AE-led close vs CSM-led usage uplift routing

### Account expansion playbook
- Multi-step expansion play (usage milestone → usage review → multi-product/seat-uplift options → AE handoff)
- Mixmax / Outreach / Salesloft sequence orchestration
- Champion + economic-buyer mapping from Gong / Chorus / Fathom call notes

### Renewal management (90-day prep)
- T-90 risk classification (Green / Yellow / Red)
- T-60 QBR with renewal-pricing discussion
- T-30 contract draft via PandaDoc / DocuSign
- T-7 e-sign + Slack pin renewal status
- Forecast accuracy target ≥ 95%

### Churn save motion (early warning + intervention)
- Composite signal trigger (usage drop + sponsor gone + NPS detractor + sentiment drop + SLA breaches + renewal risk)
- Save plan: exec outreach + commercial offer (with approval gate) + roadmap commitment via Linear
- Save call book + recording + outcome tracking

### Customer advocacy programs (case studies / references / G2 reviews)
- Promoter list from Delighted (NPS ≥ 9) + CSAT delight signal
- Advocacy invite cadence (G2 / Capterra review → reference call → case study → conference)
- Reward fulfillment via Stripe credit or Tremendous gift card
- Influitive / Slapfive / UserEvidence platform integration

### Customer advisory board (CAB) management
- 8-12 customer roster (tier + vertical + geo mix)
- Quarterly all-hands meeting (Zoom + Fathom)
- Monthly drumbeat (roadmap previews + early access + exclusive content)
- CAB Discord / Slack Connect for between-meeting community

### Voice-of-customer reporting (to product)
- Synthesis from 6 sources (interviews, NPS comments, CSAT comments, ticket-cluster themes, churn-reason tags, in-product surveys)
- Theme extraction via embedding cluster
- Tag per theme (product / support / sales / marketing) → route accordingly
- Linear issues for product with customer count + revenue impact + recommended action
- Quarterly VOC report via docx

### Executive sponsor relationships
- Multi-threading: Champion (Director+) + Exec Sponsor (VP+) + Economic Buyer + Technical Evaluator + End Users
- Cadence per role (weekly / monthly / quarterly)
- Single point of failure detection + intervention
- Salesforce / HubSpot contact-role mapping

### Customer interview programs
- Recruit via Calendly
- Host via Zoom + Fathom transcript
- Theme synthesis via Claude
- Insights DB in Notion

### In-app onboarding flows (Pendo / Userpilot / Appcues)
- Flow design schema (trigger / audience / steps / exit / metric)
- Push to platform via REST API
- A/B test pattern with PostHog cohort comparison
- Adoption metric readback

### In-product survey deployment (Sprig / Survicate / Delighted)
- Event-triggered micro-surveys (Sprig)
- Multi-channel deployment (Survicate)
- Post-event NPS / CSAT / CES (Delighted)
- Response webhook → warehouse

### NPS / CSAT / CES tracking
- NPS quarterly (independent of support events)
- NPS post-onboarding at Day 90
- CSAT post-support-close (1h delay)
- CES post-resolution (24h delay)
- Detractor (≤6 NPS / ≤2 CSAT) → CSM within 1h
- Promoter (≥9 NPS / 5 CSAT) → advocacy flow

### Adoption metric tracking (feature usage / DAU MAU WAU)
- PostHog HogQL per-customer cohort queries
- DAU / MAU / WAU rollup
- Key feature adoption rate
- Per-customer adoption score writeback to CSP

### Playbook automation (ChurnZero Plays / Vitally Playbooks)
- CSP-native plays (ChurnZero / Vitally / Catalyst / Gainsight)
- Python orchestration fallback (cron + Postgres state + MCP execution)
- Trigger → action → outcome tracking

### Ramp-to-value tracking (time-to-first-value / time-to-repeat-value)
- TTFV definition + target (< 7d self-serve, < 30d enterprise)
- TTRV definition + target (< 14d)
- PostHog funnel queries
- Slippage intervention (CSM outreach + in-app card + call)

### At-risk identification + escalation
- Nightly composite risk view (health score + sponsor activity + ticket sentiment + renewal stage)
- Risk tier (Red / Yellow / Green) → auto-escalation
- Slack alert + Linear save-plan issue creation
- Renewal board update

### Customer touchpoint cadence
- Tier-based cadence (Enterprise weekly / Growth bi-weekly / Starter monthly / Free quarterly)
- Mixmax / Outreach / Salesloft orchestration
- Email + Slack Connect + in-app card mix

### Success enablement content (training / certification / customer academy)
- Skilljar / Northpass / WorkRamp / Intellum LMS integration
- Customer academy enrollment on milestone trigger
- Certification completion → adoption-signal writeback
- Notion + Loom fallback for free academy

### Referral programs
- Promoter trigger (NPS ≥ 8)
- Reward fulfillment (Stripe credit / Tremendous gift card / Friendbuy orchestration)
- Quarterly reminder cadence

### Customer milestone tracking + anniversary celebration
- Year 1 / 2 / 3 anniversaries
- ARR milestones ($1M processed, 10K users, etc.)
- Auto-send congrats + advocacy invite
- Imagegen for anniversary card

### Feature adoption interventions
- PostHog cohort (active + key feature not used by Day N)
- Pendo / Userpilot nudge via REST
- Email follow-up if no adoption within 7d
- Iterate copy + flow

### Expansion email sequences (multi-product cross-sell)
- Cohort identification via expansion-opportunity step
- Klaviyo / Customer.io / Iterable / Outreach sequence orchestration
- Personalization with usage stats
- A/B test variants

### Contract uplift management (renewal pricing + negotiation)
- PandaDoc / DocuSign / Ironclad contract drafting
- Salesforce CPQ / Zuora pricing for enterprise
- xlsx pricing model with line-item delta
- Approval routing via Notion renewal board

### Multilingual customer comms
- DeepL translation for non-English-primary customers
- Per-language renewal + onboarding email templates
- Translation memory in Notion

---

## Execution status (SOTA — June 2026)

Every documented use case has a concrete SOTA execution mechanism. The "draft only, can't act" gaps are closed via shipped MCPs (PostHog / Mixpanel / Amplitude / Linear / Jira / Slack / Discord / Zoom / Twilio / Stripe / Notion / Postgres) and well-documented APIs (Vitally / Catalyst / Gainsight / ChurnZero / Pendo / Userpilot / Appcues / Delighted / Survicate / Sprig / Mixmax / Outreach / Klaviyo / PandaDoc / DocuSign / Influitive / Skilljar / Friendbuy / Tremendous / Pocus / Common Room / Calendly / Fathom) reachable through `cli-anything` curl + `api-gateway`.

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Customer onboarding (Day 0/7/30/60/90) | Vitally / Catalyst / Gainsight Projects + Pendo flows + email | `customer-onboarding-day-0-90` skill |
| Success plan creation | Vitally Projects / Catalyst Playbooks / Notion DB | `success-plan-goals-milestones` skill |
| QBR scheduling + facilitation | Calendly + Zoom + Fathom + PostHog + PPTX | `qbr-scheduling-facilitation` skill |
| Customer health scoring | Vitally / Catalyst / ChurnZero / Gainsight + composite formula | `customer-health-scoring-vitally-catalyst-churnzero` skill |
| NRR / GRR ownership + metrics | Stripe + CRM + Postgres cohort + xlsx + pptx | `nrr-grr-ownership-metrics` skill |
| Expansion opportunity identification | PostHog HogQL + Pocus / Common Room + CRM | `expansion-opportunity-identification` skill |
| Account expansion playbook | Outreach / Mixmax + Fathom + Calendly + gmail | `multi-product-cross-sell-uplift` skill |
| Renewal management (90-day prep) | Stripe + Mixmax + PandaDoc + DocuSign + Notion | `renewal-management-90-day-prep` skill |
| Churn save motion | Composite signal + exec outreach + Linear commitment + Slack approval | `churn-save-motion-intervention` skill |
| Customer advocacy (case studies / G2) | Delighted promoter list + Influitive + Stripe credit / Tremendous | `customer-advocacy-case-study-reference` skill |
| Customer advisory board (CAB) | Bevy / Slack Connect / Discord + Zoom + Fathom + Notion | `customer-advisory-board-cab` skill |
| Voice-of-customer reporting | Multi-source synthesis + Linear handoff + docx report | `voice-of-customer-reporting` skill |
| Executive sponsor relationships | Salesforce / HubSpot contact-role + cadence orchestration | covered by onboarding + QBR + cadence skills |
| Customer interview program | Calendly + Zoom + Fathom + Notion insights DB | covered by `voice-of-customer-reporting` + `qbr-scheduling-facilitation` |
| In-app onboarding flows | Pendo / Userpilot / Appcues / Chameleon / Whatfix / ProductFruits | `in-app-onboarding-userpilot-appcues-pendo` skill |
| In-product survey deployment | Sprig / Survicate / Delighted | `nps-csat-ces-tracking` skill |
| NPS / CSAT / CES tracking | Delighted + Survicate + Sprig | `nps-csat-ces-tracking` skill |
| Adoption metric tracking | PostHog / Mixpanel / Amplitude HogQL/JQL/charts | `adoption-metric-feature-usage` skill |
| Playbook automation | ChurnZero Plays / Vitally Playbooks / Python orchestration | `playbook-automation-churnzero-plays` skill |
| Ramp-to-value tracking (TTFV/TTRV) | PostHog funnel + Pendo analytics | `ramp-to-value-tracking` skill |
| At-risk identification + escalation | Postgres nightly view + Slack alert + Linear save-plan | `at-risk-identification-escalation` skill |
| Customer touchpoint cadence | Mixmax / Outreach / Salesloft + gmail-mcp | covered by playbook + renewal skills |
| Success enablement academy | Skilljar / Northpass / WorkRamp + Notion fallback | `success-enablement-academy-certification` skill |
| Referral programs | Friendbuy + Tremendous + Stripe credit | `referral-programs` skill |
| Customer milestone + anniversary | Trait threshold cron + gmail-mcp + imagegen | `customer-milestone-anniversary` skill |
| Feature adoption interventions | PostHog cohort + Pendo nudge + gmail follow-up | `feature-adoption-interventions` skill |
| Expansion email sequences | Klaviyo / Customer.io / Iterable / Outreach + cohort sync | `multi-product-cross-sell-uplift` skill |
| Contract uplift management | PandaDoc / DocuSign / Ironclad + xlsx pricing | covered by `renewal-management-90-day-prep` skill |
| Multilingual customer comms | DeepL MCP | `deepl-mcp` MCP |

---

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Vitally / Catalyst / Gainsight / ChurnZero / Totango / Custify / Velaris (CSP) | ⚠ | Paid SaaS; HubSpot custom property + dbt nightly model is free fallback |
| ChurnZero AI / Vitally AI / Sturdy (churn AI) | ⚠ | Paid SaaS; composite PostHog + ticket-sentiment + Stripe signal is free fallback |
| Pocus / Common Room / Koala / Endgame (PLG signal) | ⚠ | Paid SaaS; PostHog HogQL composite is free fallback |
| Pendo / Userpilot / Appcues / Chameleon / Whatfix (in-app onboarding) | ⚠ | All paid; ProductFruits has free tier; agent drafts flow design either way |
| Influitive / Slapfive / UserEvidence / Champion (advocacy) | ⚠ | Paid SaaS; Notion advocacy tracker + Delighted-fed list + Calendly is free fallback |
| Skilljar / Northpass / WorkRamp / Intellum (LMS) | ⚠ | Paid LMS; Notion + Loom-recorded lessons + Calendly is free fallback |
| Friendbuy / Referral Rock / Mention Me / Tremendous (referral) | ⚠ | Paid; manual Stripe credit + Notion tracker is free fallback |
| Mixmax / Outreach / Salesloft (cadence) | ⚠ | Paid; `gmail-mcp` + cron scheduling is free fallback for low volume |
| Klaviyo / Customer.io / Iterable (lifecycle email) | ⚠ | Paid; `gmail-mcp` + cron is free fallback for low volume |
| PandaDoc / DocuSign / Ironclad (contracts) | ⚠ | Paid; `docx` + email signature workflow is free fallback |
| Granola / tl;dv / Otter.ai (alt notetakers) | ⚠ | Paid; Fathom has free tier as CraftBot default |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a concrete execution path. The 5% residual is paid SaaS APIs the recipient owns (CSP, in-app onboarding, advocacy, LMS, referrals, cadence) — each has a documented free or open-source fallback. The previous "agent can categorize but not act" / "agent can suggest but not execute" / "agent can read but not write back" gaps are closed via shipped MCPs (PostHog / Stripe / Linear / Notion / Postgres) + `cli-anything` curl against well-documented REST APIs + `api-gateway` for managed-OAuth platforms.

---

## When to use this agent

- "Onboard our newest enterprise customer — set up Day 0/7/30/60/90 milestones"
- "Build a success plan for [customer] focused on their Q2 outcomes"
- "Schedule and prep the Q1 QBR for [customer]"
- "Compute health scores for all customers and flag the at-risk ones"
- "Compute NRR / GRR for last quarter by cohort and tier"
- "Find expansion opportunities in our customer base ranked by ARR potential"
- "Start 90-day renewal prep for [customer] — classify risk and stage"
- "[Customer] is showing churn signals — fire the save play"
- "Pull a list of promoters from last quarter's NPS and send case-study invites"
- "Synthesize voice of customer for Q1 — themes, customer counts, recommended actions"
- "Set up our CAB — 12 customers, quarterly meetings"
- "Deploy the new in-app onboarding flow via Pendo"
- "Send post-onboarding NPS to customers hitting Day 90 this week"
- "Track DAU/MAU per customer and flag adoption drops"
- "Roll out a referral program with Stripe credit rewards"
- "Send the Year 1 anniversary celebration to customers hitting this milestone"

## When NOT to use this agent

- Reactive ticket-queue work, SLA breach management, KB drift detection — hand off to `customer-support-agent`
- New logo acquisition / cold outbound / pipeline generation — hand off to `sales-agent`
- Expansion close beyond CSM-led usage uplift (new SKUs, multi-year, contract redlines) — hand off to `sales-agent`
- Roadmap-grade VOC prioritization (RICE / MoSCoW / opportunity sizing) — hand off to `product-manager`
- Scale-grade case study writing or paid amplification — hand off to `marketing-agent`
- Docs rewrites at scale (not just gap-fill) — hand off to `technical-writer`
- Revenue recognition / commission / GL reconciliation — hand off to `finance-controller`
- Contract redlines beyond standard renewal uplift — hand off to `legal-counsel`
- In-product onboarding UX research at the discovery level — hand off to `ux-researcher` + `product-manager`
- Engineering work for the CS tooling stack itself — hand off to `senior-python-engineer`
- Brand voice strategy at the agency-engagement level — `marketing-agent`
