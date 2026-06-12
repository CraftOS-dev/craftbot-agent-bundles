# Business Development / Partnerships — Use Cases

**Tier:** **general** · **Category:** business-dev
**Core job:** End-to-end BD/partnerships operations — partner sourcing, agreement structuring across 5 archetypes, marketplace listings across 10+ marketplaces, partner enablement + certification, co-marketing, MDF allocation, channel pricing + deal registration, integration roadmap planning, Crossbeam/Reveal account mapping, scorecards, ecosystem mapping, partner-led events, partner-sourced pipeline tracking, channel conflict resolution, Partner Advisory Board, Partner NPS, 90-day onboarding, integration health, joint customer stories, QBRs, off-boarding.

> Ships with the SOTA 2026 partnerships stack (Crossbeam + Reveal + Snowflake Native Apps for account mapping; Partnerstack + Tackle + Allbound + Impartner + Channeltivity for PRM; Tackle + cloud CLIs for AWS/Azure/GCP marketplaces; sfdx Code Analyzer for AppExchange; HubSpot + Shopify + Slack + OpenAI + Stripe + Atlassian + AppSource portal APIs; PandaDoc + DocuSign for agreement structuring; Apollo + Crunchbase + Pitchbook + LinkedIn for sourcing; Canvas LMS for certification; Zoom + Goldcast + ON24 for joint webinars; Sentry + PostHog for integration health; Typeform for Partner NPS) — executes end-to-end, not just direct.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Partner sourcing + pipeline
- Partner sourcing (Crunchbase + Apollo + LinkedIn Sales Navigator + Pitchbook + G2 waterfall)
- PICP (Partner ICP) definition with 5-axis scoring rubric
- Ecosystem mapping + tech-stack discovery (BuiltWith + Clay + DrawIO / Figma visualization)
- Joint target-account list authoring

### Agreement structuring
- Referral partner agreements (commission % + attribution window + no resale)
- Affiliate partner agreements (CPA / CPL + cookie window + allowed promotional channels)
- Channel reseller agreements (margin tier + MDF + certifications + deal-reg + MAP)
- Integration partner agreements (API access + joint roadmap + co-marketing + IP / data terms + monitoring SLA)
- OEM agreements (private-label + revenue share + exclusivity + IP escrow + transition rights)
- Joint Marketing Agreement (JMA) for co-marketing
- Termination + off-boarding packages

### Marketplace launches
- AWS Marketplace SaaS listings (SaaS Contracts / SaaS Subscriptions / Container / AMI), private offers, CPPO
- Azure Marketplace SaaS offers, MACC eligibility, Co-Sell Ready / IP Co-Sell
- GCP Marketplace listings + integrated billing
- Salesforce AppExchange listing + Security Review prep (sfdx Code Analyzer)
- HubSpot App Marketplace listing
- Shopify App Store listing + Built for Shopify badge
- Slack App Directory listing
- OpenAI GPT Store listing
- Stripe Marketplace + Stripe Connect payout
- Atlassian Marketplace listing (Cloud + Data Center) + Cloud Fortified
- Microsoft AppSource SaaS offer + Co-Sell Ready

### Partner enablement
- Tiered partner certification programs (Foundation / Specialist / Expert)
- LMS course authoring (HubSpot Academy + Trailhead + Canvas LMS + Allbound LMS patterns)
- Partner battlecards + enablement content (decks, demos, sandbox)
- Sandbox / dev-env provisioning for integration partners

### Co-marketing
- Co-marketing campaign design (joint plan + asset suite + distribution split + measurement)
- Joint Marketing Agreement (JMA) execution
- Joint customer story production (interview + draft + co-publish)
- Partner-led webinars + events (Zoom / Goldcast / ON24)
- Co-branded asset production (cross-agent with marketing-agent)

### Channel mechanics
- Channel pricing + discount tier design (Authorized / Silver / Gold matrix)
- MDF (market development fund) allocation + tracking with POP discipline
- Deal registration workflow (48h SLA + protected window + margin uplift)
- Channel conflict resolution (first-to-register + appeal path + quarterly conflict report)
- Channel-pricing exception handling + discount approval matrix

### Integration partnerships
- Integration roadmap planning with joint API surface mapping
- API versioning + SLA documentation
- Integration health monitoring (Sentry errors + PostHog adoption + shared dashboard)
- Deprecation planning + customer-impact communication
- Cross-agent integration scoping hand-off to product-manager

### Account mapping + co-sell
- Crossbeam account mapping (US-leading)
- Reveal account mapping (EU-leading)
- Snowflake Native Apps + Data Clean Room (data-mature partners)
- Joint pipeline tracking + co-sell motion design

### Partner program operations
- Partner scorecard authoring (quarterly, ≥ 4 KPIs per partner type)
- Partner-sourced pipeline tracking (CRM source-field + weekly rollup)
- 90-day partner onboarding playbook
- Tier transition reviews (quarterly + at annual renewal)
- Partnerstack / Tackle / Allbound / Impartner / Channeltivity / Magentrix PRM ops
- Partner CRM / PRM hygiene (monthly cron)

### Strategic governance
- Partner Advisory Board (PAB) — 6-12 partners, quarterly + annual summit
- Partner NPS quarterly survey + detractor recovery
- Quarterly Business Reviews (QBR) with strategic partners
- Off-boarding + termination workflow with reconciliation

### Cross-agent coordination
- Hand-off to sales-agent for direct deal motion
- Hand-off to marketing-agent for co-marketing creative + co-branded assets
- Hand-off to product-manager for integration scoping + sprint commits
- Hand-off to legal-counsel for binding contract redlines (OEM IP escrow, MSA negotiation, DPA)
- Hand-off to finance-controller for MDF accounting + commission accounting + pricing exceptions
- Hand-off to customer-support-agent for detractor recovery on customer-side issues
- Hand-off to video-creator for joint customer story video production

---

## Execution status (SOTA — June 2026)

The 2026 SOTA partnerships stack closes the historic "can advise on partnerships, can't structure the agreement" / "can recommend AWS Marketplace, can't write the listing" / "can suggest Crossbeam, can't run the account map" gaps. PandaDoc + DocuSign + Tackle + Partnerstack + Allbound + Impartner + Crossbeam + Reveal + Crunchbase + Apollo + Canvas LMS + cloud CLIs (aws / az / gcloud / sfdx) are all proxied via `api-gateway` managed OAuth or accessible via `cli-anything`; HubSpot + Shopify + Slack + OpenAI + Stripe + Atlassian + AppSource portal automation handled via `playwright-mcp` where no public API exists.

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Partner sourcing + PICP definition | Crunchbase + Apollo + LinkedIn Sales Nav + G2 | `api-gateway` + `linkedin` + `brightdata-mcp` (`partner-sourcing-icp-definition` skill) |
| Referral / affiliate / reseller / integration / OEM agreement structuring | PandaDoc + DocuSign archetype templates | `api-gateway` (`referral-affiliate-channel-oem-agreement-structuring` skill) |
| AWS Marketplace listings | Tackle.io + AWS Marketplace Catalog API + AWS CLI | `api-gateway` + `cli-anything` (`aws-azure-gcp-marketplace-listings` skill) |
| Azure Marketplace listings | Tackle.io + Partner Center API + Azure CLI | `api-gateway` + `cli-anything` |
| GCP Marketplace listings | Tackle.io + Producer Portal + gcloud CLI | `api-gateway` + `cli-anything` |
| Salesforce AppExchange listing | sfdx Code Analyzer pre-check + Partner Console | `cli-anything` + `playwright-mcp` (`salesforce-appexchange-listing` skill) |
| HubSpot App Marketplace listing | HubSpot Developer API + portal | `api-gateway` + `playwright-mcp` (`hubspot-shopify-slack-marketplace-listings` skill) |
| Shopify App Store listing | Shopify Partners API + portal | `cli-anything` + `playwright-mcp` |
| Slack App Directory listing | Slack App manifest + slack-mcp | `slack-mcp` + `playwright-mcp` |
| OpenAI GPT Store listing | Builder portal + OpenAPI Actions | `playwright-mcp` |
| Stripe Marketplace listing | Stripe Apps SDK + Connect | `stripe-mcp` |
| Atlassian Marketplace listing | Marketplace API + portal | `cli-anything` + `playwright-mcp` |
| Microsoft AppSource SaaS offer | Partner Center API + portal | `cli-anything` + `playwright-mcp` |
| Partner enablement + certification programs | Canvas LMS + course/cert authoring | `canvas-lms-mcp` + `docx`/`pptx` + CRM via `api-gateway` (`partner-enablement-certification-programs` skill) |
| Co-marketing campaign design | Joint plan + co-branded assets via marketing-agent | `notion` + cross-agent `marketing-agent` (`co-marketing-campaign-design` skill) |
| MDF allocation + tracking | Partnerstack / Impartner / Allbound MDF + POP workflow | `api-gateway` + `notion` + `slack-mcp` + `xlsx` (`mdf-allocation-tracking` skill) |
| Channel pricing + discount tiers | Margin tier matrix + CRM custom obj | `xlsx`/`google-sheets` + CRM via `api-gateway` (`channel-pricing-discount-tiers` skill) |
| Integration roadmap planning | Joint roadmap doc + Linear/Jira tracking | `notion` + `linear-mcp`/`jira-mcp` + cross-agent `product-manager` (`integration-roadmap-planning` skill) |
| Partnerstack channel management | Partnerstack API | `api-gateway` (`partnerstack-tackle-channel-management` skill) |
| Tackle.io channel management | Tackle API | `api-gateway` |
| Allbound / Impartner / Channeltivity / Magentrix PRM | Each PRM's REST API or portal | `api-gateway` + `playwright-mcp` |
| Crossbeam account mapping | Crossbeam API + populations + reports | `api-gateway` (`crossbeam-reveal-account-mapping` skill) |
| Reveal account mapping | Reveal API | `api-gateway` |
| Snowflake Native Apps account mapping | Snowflake Data Clean Room + Native Apps | `postgresql-mcp` (Snowflake) |
| Partner scorecard authoring | Warehouse query + xlsx/pdf render | `postgresql-mcp` + `xlsx`/`pdf` (`partner-scorecard-authoring` skill) |
| Ecosystem mapping + tech-stack discovery | BuiltWith + Clay + DrawIO / Figma | `cli-anything` + `drawio-mcp`/`figma-mcp` (`ecosystem-mapping-tech-stack-discovery` skill) |
| Partner-led webinars + events | Zoom Webinars + Goldcast + landing pages | `zoom-mcp` + `gmail-mcp` + `google-calendar-mcp` (`partner-led-webinars-events` skill) |
| Partner-sourced pipeline tracking | CRM source-field + warehouse rollup | `api-gateway` + `postgresql-mcp` + `google-sheets` (`partner-sourced-pipeline-tracking` skill) |
| Deal registration + channel conflict resolution | CRM custom obj + SLA timers + Slack | `api-gateway` + `postgresql-mcp` + `slack-mcp` (`deal-registration-channel-conflict-resolution` skill) |
| Partner Advisory Board (PAB) | Quarterly summit + pre-read + synthesis | `notion` + `google-calendar-mcp` + `zoom-mcp` (`partner-advisory-board-pab` skill) |
| Partner NPS survey | Typeform NPS distribution + warehouse analysis | `typeform` + `gmail-mcp` + `postgresql-mcp` + `xlsx` (`partner-nps-satisfaction-survey` skill) |
| 90-day partner onboarding | Standardized template + LMS + CRM tasks | `notion` + `canvas-lms-mcp` + `api-gateway` (`partner-onboarding-90-day-plan` skill) |
| Tech-partner integration health monitoring | Sentry + PostHog tagged dashboards | `sentry-mcp` + `posthog-mcp`/`mixpanel-mcp` + `postgresql-mcp` |
| Joint customer story production | Interview + draft + co-publish | `fathom-api` + `docx` + cross-agent `video-creator`/`marketing-agent` |
| QBR with strategic partners | Quarterly meeting + scorecard deck | `pptx`/`canva-mcp` + `zoom-mcp` + `notion` |
| Partner CRM / PRM hygiene | Monthly clean-up + cron alerts | `postgresql-mcp` + `gmail-mcp` + `api-gateway` |
| Off-boarding + termination | Termination letter + reconciliation + transition | `api-gateway` (`pandadoc`) + cross-agent `legal-counsel` + `finance-controller` |

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Crunchbase / Pitchbook / Apollo (partner sourcing) | ⚠ | Paid plans + API keys; managed OAuth via `api-gateway` for Apollo + Crunchbase if Maton-onboarded; free fallback via brave-search + LinkedIn |
| Cloud marketplaces (AWS / Azure / GCP) | ⚠ | Seller / Partner Center / Producer Portal registration are one-time human KYC steps; listing CRUD post-enrollment fully automated |
| Salesforce AppExchange Security Review | ⚠ | 6-12 week Salesforce-side review gate; Code Analyzer pre-check + listing assets fully automated; Trailblazer DX badge auto on approval |
| Shopify / Atlassian / Microsoft AppSource | ⚠ | Portal review (3-15 day human approval); listing-asset upload + manifest CRUD automated |
| Partnerstack / Tackle / Allbound / Impartner / Channeltivity / Magentrix | ⚠ | Paid plans ($1-30k/mo); for solo founders without PRM, agent uses CRM custom objects + `notion` as system of record |
| Crossbeam / Reveal | ⚠ | Free tiers for first overlap; deep account mapping = paid; Snowflake Native Apps Data Clean Room as warehouse-native alternative |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a concrete execution path. The historic "advise, don't execute" gaps are closed via shipped MCPs, managed OAuth via `api-gateway`, dedicated default skills, and `playwright-mcp` for portal automation where no public API exists. The remaining ~5% is paywalled PRM / signal tools (recipient's own key), marketplace one-time KYC enrollment, and AppExchange Security Review (a vendor-side gate by design).

---

## When to use this agent

- "Source 30 referral partner candidates for our developer-tool product targeting fintech SMBs"
- "Draft a channel reseller agreement for a Gold-tier partner with $500K annual commit"
- "Launch our SaaS on AWS Marketplace this quarter with Co-Sell Ready"
- "Run sfdx Code Analyzer on our package and start the AppExchange submission"
- "List our app on the HubSpot App Marketplace + Shopify App Store + Slack App Directory"
- "Map account overlap with our top 5 strategic partners via Crossbeam"
- "Build the Q3 partner scorecard for our 12 strategic partners"
- "Design a co-marketing campaign with [Partner] — joint webinar + customer story + 4-week distribution"
- "Allocate $50K MDF across our Gold-tier partners for Q3"
- "Plan a joint integration roadmap with [Partner] — their REST API + our webhooks + 90-day launch"
- "Process this deal registration submission and check for conflicts"
- "Set up a Partner Advisory Board for next month — 8 strategic partners + product roadmap unveil"
- "Run the Q3 Partner NPS survey across all 24 partners"
- "Onboard a new integration partner with the 90-day plan"
- "Build the partner-sourced pipeline rollup for last week"
- "Off-board [Partner] — they've missed commit 2 quarters in a row"
- "Run the QBR with [Strategic Partner] next Tuesday — pre-read + scorecard + roadmap"

## When NOT to use this agent

- Direct deal motion (MEDDIC / cold sequences / discovery scripts / forecast) — hand off to `sales-agent`
- Top-of-funnel content (blog posts, ads, brand voice, landing pages, video creative) — hand off to `marketing-agent`
- Integration scoping + sprint commit + engineering capacity + architecture decisions — hand off to `product-manager`
- Binding contract redlines / MSA negotiation / DPA review / IP escrow terms in OEM / antitrust exposure — hand off to `legal-counsel`
- Commission accounting / MDF accounting + audit trail / revenue recognition / pricing exception > 20% discount / FX hedging on multi-currency partners — hand off to `finance-controller`
- Post-sale customer support / customer churn intervention / detractor recovery on customer-side issues — hand off to `customer-support-agent`
- Deep market research / TAM sizing / Gartner-style competitive deep-dives over weeks — hand off to `research-analyst`
- Joint customer story video editing + color grading + thumbnails — hand off to `video-creator`
- Engineering work for the partnership tech stack (e.g., build a custom Tackle integration, write a Crossbeam Snowflake Native App) — hand off to `senior-python-engineer`
- Sales-team hiring / partner-manager hiring / comp plan design — out of scope for v1 (specialist agent v2+)
- Antitrust / FCPA / GDPR cross-border compliance for global partner programs — hand off to `legal-counsel` and `compliance-agent`
- Cloud-marketplace-specific engineering (e.g., writing the SaaS Connector API, AWS Service Catalog integration, Salesforce package code) — hand off to `senior-python-engineer`
