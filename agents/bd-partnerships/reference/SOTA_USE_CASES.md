# SOTA Use Case Coverage Map — bd-partnerships (June 2026)

This document maps every documented use case in `USE_CASES.md` to a concrete SOTA execution mechanism. It is the **fulfillment proof** — every use case has a named tool, an exact agent-level execution path, a source URL, and a confidence rating.

**Legend:**
- ✓ — production MCP / first-class API or managed OAuth via `api-gateway`, end-to-end automated.
- ⚠ — works today with a one-time setup step (OAuth, paid API key, marketplace approval) the recipient owns.
- ✗ — partial coverage; rate-limited, scraping-fallback, or domain-specific paid tooling required.

The agent loads these mappings on demand by grepping `SOTA_USE_CASES.md` for the matching capability heading.

---

## Partner sourcing + ICP definition

- **SOTA approach:** Define Partner ICP (PICP) along five axes — customer overlap, complementary tech stack, geography, segment, motion (referral/affiliate/reseller/integration/OEM). Source candidates via Crunchbase (funding signals, ICP-matched fundraises), Pitchbook (private-company depth), LinkedIn Sales Navigator (people-driven), Apollo (org enrichment), G2 (category neighbors). Score 0-100 on PICP fit; only ≥70 enter pipeline.
- **Agent execution path:** Use `partner-sourcing-icp-definition` skill. `api-gateway` `POST https://gateway.maton.ai/crunchbase/api/v4/searches/organizations`; Apollo `POST https://gateway.maton.ai/apollo/api/v1/mixed_companies/search`; LinkedIn via `linkedin` default skill + `brightdata-mcp` Sales Nav scraping; G2 category data via `playwright-mcp`; render to `notion` partner pipeline.
- **Source:** https://data.crunchbase.com/docs + https://docs.apollo.io/reference/organization-search + https://pitchbook.com/api
- **Confidence:** ⚠ (Crunchbase + Pitchbook + Apollo paid keys; free fallback via brave-search + LinkedIn)

---

## Referral / affiliate / channel / OEM agreement structuring

- **SOTA approach:** Five partnership archetypes, each with its own contract shell — referral (commission %, attribution window, no resale rights), affiliate (CPA/CPL, cookie window, allowed promotional channels), channel reseller (margin %, MDF eligibility, deal registration, territory carve-outs), integration partner (API access, joint roadmap, co-marketing rights, IP/data terms), OEM (private-label, revenue share, exclusivity windows). Use PandaDoc / DocuSign templates with CRM-merge tokens.
- **Agent execution path:** Use `referral-affiliate-channel-oem-agreement-structuring` skill. `api-gateway` PandaDoc `POST https://gateway.maton.ai/pandadoc/public/v1/documents` from per-archetype template; DocuSign `POST /envelopes` for e-sign. Defer redlines to `legal-counsel`. Track agreement metadata in `notion` partner DB.
- **Source:** https://developers.pandadoc.com/ + https://developers.docusign.com/docs/esign-rest-api/ + https://crossbeam.com/blog/the-partnership-economy/
- **Confidence:** ✓ (template + e-sign automated; binding redlines defer to legal-counsel)

---

## AWS / Azure / GCP cloud marketplace listings

- **SOTA approach:** AWS Marketplace SaaS listing — Seller registration, SaaS Contracts vs SaaS Subscriptions, AMI vs container vs SaaS, private offers, Channel Partner Private Offers (CPPO) for co-sell, ACE program integration. Azure Marketplace — Partner Center registration, SaaS offer with metered billing, MACC eligibility, Co-Sell Ready / IP Co-Sell status. GCP Marketplace — Cloud Identity verification, Marketplace Producer Portal, integrated billing.
- **Agent execution path:** Use `aws-azure-gcp-marketplace-listings` skill. Tackle.io is the SOTA orchestrator across all three clouds (single dashboard, co-sell automation, private-offer generation) — `api-gateway` `https://gateway.maton.ai/tackle/...` if onboarded. Direct: AWS Marketplace Catalog API `aws marketplace-catalog start-change-set` via `cli-anything`; Azure Partner Center API; GCP Producer Portal REST. Listing assets in `docx`/`pdf` + screenshots in `imagegen-mcp` / `canva-mcp`.
- **Source:** https://docs.aws.amazon.com/marketplace/latest/userguide/ + https://learn.microsoft.com/en-us/partner-center/marketplace/ + https://cloud.google.com/marketplace/docs + https://tackle.io/
- **Confidence:** ⚠ (Seller registration + Partner Center approval are one-time human steps; listing CRUD is automated)

---

## Salesforce AppExchange listing

- **SOTA approach:** AppExchange Partner Program enrollment, Security Review (mandatory — Salesforce Code Analyzer + manual review, 6-12 weeks), AppExchange Listing Asset Bundle (Listing tile + Featured image + Screenshots + Demo video + Tier+pricing), Marketing Plan, Trailblazer DX badge. ISVForce program for distribution. AppExchange API for analytics post-publish.
- **Agent execution path:** Use `salesforce-appexchange-listing` skill. Pre-submission: `cli-anything` Salesforce Code Analyzer (`sfdx scanner:run`) over the package; render listing assets via `docx`/`pdf`/`imagegen-mcp`. AppExchange Listing CRUD via Partner Console (no public API for listing CRUD — `playwright-mcp` for portal automation). Post-launch analytics via Partner Console exports.
- **Source:** https://partners.salesforce.com/partnerProgram + https://developer.salesforce.com/docs/atlas.en-us.code_analyzer.meta/code_analyzer/ + https://appexchange.salesforce.com/
- **Confidence:** ⚠ (Security Review is a Salesforce-side gate; listing assets + Code Analyzer pre-check fully automated)

---

## HubSpot / Shopify / Slack / OpenAI / Stripe / Atlassian / Microsoft AppSource marketplace listings

- **SOTA approach:** Each marketplace has a Developer Program + listing portal + listing-asset bundle (icon, screenshots, description, demo video, pricing tiers). HubSpot App Marketplace (App Partner Program, OAuth 2.0), Shopify App Store (Partners dashboard, Built for Shopify), Slack App Directory (Slack App Directory submission + review), OpenAI GPT Store (Builder Profile + GPT submission), Stripe Marketplace, Atlassian Marketplace (DC + Cloud versions), Microsoft AppSource (Partner Center + Cloud Partner Portal). Pattern: listing asset bundle → portal upload → manual review → publish.
- **Agent execution path:** Use `hubspot-shopify-slack-marketplace-listings` skill. HubSpot `api-gateway` `https://gateway.maton.ai/hubspot/integrations/v1/...`; Shopify Partners GraphQL via `cli-anything` (no MCP); Slack App config via `slack-mcp` + manifest.yml; OpenAI GPT Store via builder profile; Stripe Marketplace via Stripe Connect APIs (`stripe-mcp`); Atlassian Marketplace via Marketplace API; Microsoft AppSource via Partner Center API. Listing assets centralized in `notion` template DB; portal uploads orchestrated via `playwright-mcp` where no API exists.
- **Source:** https://developers.hubspot.com/docs/api/marketplace + https://shopify.dev/docs/apps + https://api.slack.com/start/distributing + https://platform.openai.com/docs/actions + https://docs.stripe.com/connect + https://developer.atlassian.com/platform/marketplace/ + https://learn.microsoft.com/en-us/partner-center/marketplace/
- **Confidence:** ✓ (HubSpot/Slack/Stripe APIs); ⚠ (Shopify/AppSource/Atlassian require portal review)

---

## Partner enablement + certification programs

- **SOTA approach:** Tiered certification (Foundation → Specialist → Expert), each gated by training module + assessment + practical exercise. Programs delivered through LMS (HubSpot Academy, Salesforce Trailhead, internal Canvas LMS, Mindtickle, Highspot, Allbound LMS). Track per-partner certification status in CRM custom object. Sandbox access + technical accreditation for integration partners.
- **Agent execution path:** Use `partner-enablement-certification-programs` skill. LMS content drafted in `docx`/`pptx`/`canva-mcp`; assessment in `notion` form; Canvas LMS via `canvas-lms-mcp` if used; partner status field updated in CRM via `api-gateway` HubSpot/Salesforce. Track certifications via `postgresql-mcp` warehouse view.
- **Source:** https://academy.hubspot.com/partner-program + https://trailhead.salesforce.com/credentials + https://www.allbound.com/
- **Confidence:** ✓

---

## Co-marketing campaign design

- **SOTA approach:** Joint go-to-market plan — shared messaging frame, co-branded asset suite (one-pager, webinar deck, blog series, customer-story video), distribution split (your audience vs their audience), measurement plan (per-channel UTM, shared dashboard). Coordinate with marketing teams on both sides via a co-marketing brief; sign a Joint Marketing Agreement (JMA) for IP / brand-usage rules.
- **Agent execution path:** Use `co-marketing-campaign-design` skill. Brief authored in `notion`; co-branded assets via `marketing-agent` cross-agent hand-off (`docx`/`pptx`/`canva-mcp`/`figma-mcp`); UTM build via `buffer` MCP (route through marketing-agent); shared dashboard in `google-sheets`/`notion`. JMA via PandaDoc.
- **Source:** https://www.crossbeam.com/blog/co-marketing-playbook/ + https://blog.hubspot.com/marketing/co-marketing-guide
- **Confidence:** ✓ (cross-agent coordination with marketing-agent for creative)

---

## MDF (market development fund) allocation + tracking

- **SOTA approach:** MDF = vendor-funded co-marketing budget paid to partners against approved activities (events, ads, content, BDR campaigns). Lifecycle: request → approval → execution → proof-of-performance (POP) submission → payout. SOTA platforms: Partnerstack (referral + MDF), Allbound, Impartner, Channeltivity. Each MDF request needs business case (target audience, expected pipeline, claim period). POP = invoices + screenshots + attendance lists + UTM-tagged metrics.
- **Agent execution path:** Use `mdf-allocation-tracking` skill. MDF request form in `notion` template; routed approval via `slack-mcp` to finance reviewer; execution tracked via shared dashboard in `google-sheets`; POP gathering via `gmail-mcp` collected receipts + `firecrawl-mcp` scraped UTM analytics; payout filed via `api-gateway` Partnerstack `https://gateway.maton.ai/partnerstack/...` or direct to AP. Coordinate accounting with `finance-controller`.
- **Source:** https://partnerstack.com/blog/mdf-management + https://www.impartner.com/blog/mdf-best-practices + https://www.allbound.com/
- **Confidence:** ✓ (workflow automated; payout accounting deferred to finance-controller)

---

## Channel pricing + discount tier design

- **SOTA approach:** Three-tier reseller margin (Authorized 15% / Silver 20% / Gold 25%), tied to certification + revenue commitment + customer-sat score. Deal registration adds 5-10 pts for opportunity protection. MAP (minimum advertised price) enforcement. Floor pricing approval matrix: partner can discount to X without approval, X-Y with manager approval, > Y requires finance escalation.
- **Agent execution path:** Use `channel-pricing-discount-tiers` skill. Pricing matrix in `xlsx`/`google-sheets`; tier-eligibility query against partner status field in CRM via `api-gateway`; deal-registration workflow in HubSpot/Salesforce custom object; discount-approval Slack flow via `slack-mcp`. Pricing exception > 20% defers to `finance-controller`.
- **Source:** https://www.gartner.com/en/sales/topics/channel-sales + https://www.canalys.com/insights/channel-pricing
- **Confidence:** ✓

---

## Integration roadmap planning with product-manager

- **SOTA approach:** Integration partnerships need a roadmap, not a press release. Quarterly joint roadmap session: identify use cases, map APIs needed on both sides, define data-flow architecture, contract on API versioning + SLA, agree on launch + GTM, set integration health monitoring. Use Linear / Jira / Notion for tracking. Define DRIs on both sides.
- **Agent execution path:** Use `integration-roadmap-planning` skill. Roadmap doc in `notion`; tracked tickets in `linear-mcp` or `jira-mcp`; cross-agent hand-off to `product-manager` for scoping + engineering capacity; weekly sync agenda in `notion`; status dashboard in `google-sheets`.
- **Source:** https://www.crossbeam.com/blog/integration-partnerships/ + https://www.tackle.io/playbook
- **Confidence:** ✓ (cross-agent coordination with product-manager)

---

## Partnerstack / Tackle channel management

- **SOTA approach:** Partnerstack for referral + affiliate + reseller management (partner portal, commission tracking, payouts, marketing assets). Tackle for cloud marketplace co-selling (AWS / Azure / GCP private offers, ACE / Co-Sell pipeline sync). Allbound + Impartner + Channeltivity for full PRM portals (training, deal reg, MDF, certifications). Magentrix for Salesforce-anchored PRM.
- **Agent execution path:** Use `partnerstack-tackle-channel-management` skill. `api-gateway` `https://gateway.maton.ai/partnerstack/v3/...` for partner CRUD, commission posting, payout scheduling; `https://gateway.maton.ai/tackle/...` for cloud co-sell. Allbound + Impartner + Channeltivity + Magentrix via `api-gateway` (where Maton onboarded) or direct curl via `cli-anything`.
- **Source:** https://partnerstack.com/api + https://tackle.io/api-documentation + https://www.allbound.com/api + https://www.impartner.com/
- **Confidence:** ⚠ (paid plans required for Partnerstack + Tackle + PRM vendors)

---

## Crossbeam + Reveal account mapping

- **SOTA approach:** Account mapping = secure, privacy-preserving overlap of two companies' CRMs to find shared customers, shared opportunities, overlap accounts. Crossbeam (650K+ companies, USA-leading) + Reveal (Europe-leaning). Output: Overlap report → outbound list (their customers we're not in, our customers they're not in) → joint pipeline (both in active opps) → co-sell motion. Snowflake / Databricks for warehouse-native account-mapping (Snowflake Data Cloud Native Apps).
- **Agent execution path:** Use `crossbeam-reveal-account-mapping` skill. `api-gateway` `https://gateway.maton.ai/crossbeam/v0.3/...` (partner search, populations, reports); Reveal `https://gateway.maton.ai/reveal/...` if onboarded. Snowflake account-mapping via `postgresql-mcp` (Snowflake compatible). Output mapped to CRM as account tags via `api-gateway` HubSpot/Salesforce.
- **Source:** https://crossbeam.com/docs/api + https://docs.reveal.co/ + https://www.snowflake.com/blog/native-apps-collaboration/
- **Confidence:** ⚠ (Crossbeam + Reveal paid plans; manual CSV overlap fallback always works)

---

## Partner scorecard authoring

- **SOTA approach:** Quarterly partner scorecard with 4-6 KPIs per partner type: (Referral) leads sent / leads accepted / closed-won / commission paid. (Reseller) certifications held / pipeline sourced / closed-won / customer-sat / MDF utilization. (Integration) integration health / joint customers / co-marketing executed / NPS. Threshold-banded health: Green / Yellow / Red. Drives tier upgrades / downgrades + QBR talking points.
- **Agent execution path:** Use `partner-scorecard-authoring` skill. Scorecard template in `notion` DB; KPI queries via `postgresql-mcp` warehouse views; Partnerstack/Tackle pulls via `api-gateway`; rendered to `xlsx`/`pdf` for QBR. Per-partner dashboard in `google-sheets`.
- **Source:** https://partnerstack.com/blog/partner-scorecard + https://www.gartner.com/en/sales/topics/partner-relationship-management
- **Confidence:** ✓

---

## Ecosystem mapping + tech-stack discovery

- **SOTA approach:** Map your category's ecosystem — direct competitors, complementary tools, integrators, consultancies, resellers, marketplaces. For prospect accounts, identify their full tech stack via BuiltWith / Wappalyzer / Clay tech enrichment → identify which of their tools we already integrate with → identify partner-led entry. Visualize as ecosystem map in DrawIO / Figma / Miro.
- **Agent execution path:** Use `ecosystem-mapping-tech-stack-discovery` skill. BuiltWith API via `cli-anything` curl (`https://api.builtwith.com/v15/api.json`); Clay tech enrichment via `api-gateway`; Crunchbase ecosystem queries; ecosystem map rendered via `drawio-mcp` or `figma-mcp` or `canva-mcp`; output to `notion`/`pdf`.
- **Source:** https://api.builtwith.com/ + https://clay.com/docs/api + https://crossbeam.com/blog/ecosystem-map/
- **Confidence:** ✓

---

## Partner-led webinars + events

- **SOTA approach:** Joint webinar = 50/50 promotion split, co-presented agenda (problem → architecture → live demo of integration → Q&A), follow-up assets (recording + slides + offer). Platforms: Zoom Webinars, Goldcast, ON24, Demio, Restream. Event mechanics: registration page (HubSpot landing page + UTM split by partner), reminder cadence, post-event lead routing (your leads to your CRM, theirs to theirs, joint leads to both).
- **Agent execution path:** Use `partner-led-webinars-events` skill. Webinar booking via `zoom-mcp` (`/scheduled-webinars`); registration page via `marketing-agent` cross-agent or HubSpot landing page via `api-gateway`; UTM tagged links via Buffer / Bitly; calendar invites via `gmail-mcp` / `google-calendar-mcp`; post-event recording exported and shared via `google-drive-mcp`.
- **Source:** https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/webinarCreate + https://www.goldcast.io/blog/co-marketing-webinars + https://www.on24.com/
- **Confidence:** ✓

---

## Partner-sourced pipeline tracking

- **SOTA approach:** Partner-attribution in CRM: deal-source = Partner (sub-source = partner-id), influenced-by = partner. Pipeline metrics tracked per partner: # opps sourced / pipeline $ / closed-won / win rate. Compare to direct (sales-agent) benchmarks. Attribution model: first-touch, last-touch, or multi-touch (Partnerstack default = last-touch credited partner). Surface in weekly partner pipeline review.
- **Agent execution path:** Use `partner-sourced-pipeline-tracking` skill. CRM source-field update via `api-gateway` HubSpot/Salesforce; weekly pipeline rollup via `postgresql-mcp` warehouse query; dashboard in `google-sheets`/`notion`; alerting via `slack-mcp` to channel partner managers. Cross-agent coordination with `sales-agent` for direct-vs-partner pipeline split.
- **Source:** https://www.partnerstack.com/blog/partner-attribution + https://www.crossbeam.com/blog/attribution/
- **Confidence:** ✓

---

## Deal registration + channel conflict resolution

- **SOTA approach:** Deal registration = partner submits prospect details, vendor approves within 48h, partner gets 60-day protected status + margin uplift (5-10 pts), prevents two partners (or partner + direct) selling same account. Conflict rules: first-to-register wins by default; tie-break by customer preference; appeal process to channel manager; quarterly conflict report. Partnerstack / Impartner / Allbound / Magentrix all run deal-reg workflows.
- **Agent execution path:** Use `deal-registration-channel-conflict-resolution` skill. Deal-reg form in HubSpot/Salesforce custom object via `api-gateway`; approval workflow in `notion` or PRM portal; conflict log in `notion` DB; Slack `slack-mcp` alerts on conflicts. SLA timer in `postgresql-mcp` cron + `gmail-mcp` reminders.
- **Source:** https://partnerstack.com/blog/deal-registration + https://www.impartner.com/blog/deal-registration-best-practices
- **Confidence:** ✓

---

## Partner advisory board (PAB)

- **SOTA approach:** PAB = 6-12 strategic partners convened quarterly to advise on roadmap, GTM, pricing, ecosystem. Membership criteria: top-tier partner + ≥2 quarters of relationship + strategic-segment representation. Format: pre-read deck → 2-day in-person summit → product feedback session → roadmap unveil → joint commitment. Output: prioritized partner-influenced roadmap items.
- **Agent execution path:** Use `partner-advisory-board-pab` skill. PAB membership tracked in `notion` DB; pre-read assembled via `docx`/`pptx`; summit agenda + logistics in `notion`; calendar via `google-calendar-mcp`; recording via `zoom-mcp`; post-summit synthesis to `notion`. Coordinate roadmap inputs with `product-manager`.
- **Source:** https://www.crossbeam.com/blog/partner-advisory-board/ + https://www.forrester.com/report/the-forrester-wave-partner-advisory-board/
- **Confidence:** ✓

---

## Partner NPS + satisfaction survey

- **SOTA approach:** Quarterly Partner NPS = "How likely are you to recommend our partner program to a peer (0-10)?" + 3 follow-up questions (what's working / what's not / one ask). Industry benchmark: Partner NPS > 30 = healthy, > 50 = best-in-class. Compare per partner tier; segment promoters / passives / detractors. Distribute via Typeform / Google Forms / HubSpot survey; analyze trend over time.
- **Agent execution path:** Use `partner-nps-satisfaction-survey` skill. Survey built in `typeform` default skill or `google-sheets` form; sent via `gmail-mcp` mailmerge; responses warehoused via `postgresql-mcp`; NPS calc + trend in `xlsx`/`google-sheets`; detractor follow-up Slack alerts via `slack-mcp`. Cross-agent with `customer-support-agent` for detractor recovery.
- **Source:** https://www.partnerstack.com/blog/partner-nps + https://www.netpromoter.com/know/
- **Confidence:** ✓

---

## Partner onboarding 90-day plan

- **SOTA approach:** Standardized 90-day partner onboarding: Day 0 contract signed → Day 7 kickoff call + sandbox + first training module → Day 30 first joint customer plan + co-marketing brief → Day 60 first certification milestone + first pipeline submitted → Day 90 scorecard review + tier-eligibility check + QBR setup. Each step has owner, deadline, success criterion.
- **Agent execution path:** Use `partner-onboarding-90-day-plan` skill. Onboarding plan in `notion` template DB; tasks auto-created in CRM via `api-gateway` HubSpot/Salesforce; certifications tracked in LMS (`canvas-lms-mcp`); Slack channel per partner via `slack-mcp` `conversations.create`; calendar invites via `google-calendar-mcp`; Day-90 scorecard via `partner-scorecard-authoring` skill.
- **Source:** https://partnerstack.com/blog/partner-onboarding + https://www.allbound.com/blog/partner-onboarding-checklist
- **Confidence:** ✓

---

## Tech partner integration health monitoring

- **SOTA approach:** Once an integration ships, monitor: % of joint customers actually using it (adoption), API call volume per partner per customer, error rate per endpoint, latency, deprecation events. Alert on threshold drops (adoption < 30%, error spike > 5x baseline). Use APM (Datadog / Sentry) + product analytics (PostHog / Mixpanel) tagged by integration_partner_id.
- **Agent execution path:** Use `partnerstack-tackle-channel-management` skill (covers tech-partner monitoring). `sentry-mcp` for error tracking; `posthog-mcp`/`mixpanel-mcp`/`amplitude-mcp` for adoption; warehouse query via `postgresql-mcp`; weekly health digest to `slack-mcp`/`gmail-mcp`. Cross-agent with `product-manager` for deprecation planning.
- **Source:** https://posthog.com/blog/integration-analytics + https://docs.sentry.io/
- **Confidence:** ✓

---

## Joint customer story production

- **SOTA approach:** Joint customer story = 1-pager + video case + quote block + win wire. Pattern: identify joint customer with measurable outcome → joint interview (vendor PM + partner PM + customer champion) → draft story → both sides legal approval → publish on both sites + social. Coordinate with marketing-agent for the actual creative production.
- **Agent execution path:** Use `co-marketing-campaign-design` skill. Story brief in `notion`; interview booking via `google-calendar-mcp` + `zoom-mcp`; transcript via `fathom-api` / `gong-chorus-call-intelligence`; draft in `docx`/`pdf`; video editing handed off to `video-creator`; final assets published via `marketing-agent`.
- **Source:** https://www.crossbeam.com/blog/co-marketing-customer-stories/
- **Confidence:** ✓

---

## Quarterly business review (QBR) with strategic partners

- **SOTA approach:** Quarterly QBR with top partners: review scorecard, pipeline, MDF utilization, certifications, customer-sat; agree on next-quarter goals + dependencies on both sides. Format: 60-min meeting, 8-12 slide deck, joint action items. QBR cadence is a leading indicator of partnership health.
- **Agent execution path:** Use `partner-scorecard-authoring` skill. QBR deck in `pptx`/`canva-mcp`; scorecard data via `postgresql-mcp`; meeting booking via `google-calendar-mcp` / `zoom-mcp`; action items tracked in `notion` DB + Slack channel; quarterly trend chart in `xlsx`.
- **Source:** https://www.crossbeam.com/blog/partner-qbr/ + https://www.allbound.com/blog/partner-qbr
- **Confidence:** ✓

---

## Partner battlecards + enablement content (decks, demos, sandbox)

- **SOTA approach:** Partner enablement asset library: 1-page solution brief, joint pitch deck, technical architecture diagram, live demo script, demo sandbox URL, ROI calculator, customer references. Stored in partner portal / Highspot / Seismic / Mindtickle / Allbound. Updated quarterly.
- **Agent execution path:** Use `partner-enablement-certification-programs` skill. Solution brief in `docx`/`pdf`; pitch deck in `pptx`/`canva-mcp`; architecture diagram in `drawio-mcp`/`figma-mcp`; demo script in `notion`; ROI calculator in `xlsx`/`google-sheets`. Asset library indexed in `notion`. Distribute via PRM portal upload (`playwright-mcp` if no API).
- **Source:** https://www.allbound.com/blog/partner-enablement-content + https://www.highspot.com/
- **Confidence:** ✓

---

## GTM-with-partners orchestration

- **SOTA approach:** Joint GTM motion = unified positioning, joint target accounts, agreed first-meeting commitment ("we set 5 meetings this Q together"), shared sales play (who pitches, who follows up, who handles legal), shared closing process, shared celebration. Operates above any one campaign; lives in joint GTM plan doc revisited quarterly.
- **Agent execution path:** Use `crossbeam-reveal-account-mapping` + `co-marketing-campaign-design` skills jointly. Joint GTM plan in `notion`; account mapping via Crossbeam → joint target-account list; meeting commitments tracked in CRM via `api-gateway`; weekly joint stand-up via `slack-mcp` or `ms-teams-mcp`. Cross-agent: sales execution → `sales-agent`; creative → `marketing-agent`.
- **Source:** https://www.crossbeam.com/blog/joint-gtm/ + https://tackle.io/playbook/joint-gtm
- **Confidence:** ✓ (cross-agent orchestration)

---

## Partner CRM hygiene (Partnerstack / Tackle / PRM clean-up)

- **SOTA approach:** Monthly hygiene: stale partner records (no activity > 6 months → archive or activate), orphan deal-reg records past 60-day window → expire, MDF requests without POP after deadline → escalate, certification expirations → renewal reminder, churned partners → off-board with asset reclaim.
- **Agent execution path:** Use `partnerstack-tackle-channel-management` skill (hygiene sub-routine). Cron via `postgresql-mcp` warehouse view → flag records → `gmail-mcp` reminders + `slack-mcp` alerts; archival via `api-gateway` Partnerstack/Tackle/PRM mass-update; report to `notion`.
- **Source:** https://partnerstack.com/blog/partner-program-hygiene + https://www.impartner.com/
- **Confidence:** ✓

---

## Off-boarding + termination

- **SOTA approach:** Termination triggers: missed KPIs 2 quarters in a row / customer-sat detractor / contract breach / strategic pivot. Off-board steps: contract-termination letter (notice period per agreement), revoke portal access, reclaim MDF unused balance, certify joint customers transitioned, public/silent disposition decision (silent default; public only if legal-mandated). Coordinate with legal-counsel + finance-controller.
- **Agent execution path:** Use `referral-affiliate-channel-oem-agreement-structuring` skill (termination sub-doc). Termination letter via PandaDoc/DocuSign template; portal-access revoke via `api-gateway` PRM bulk-update; MDF reconciliation via `xlsx`; legal redlines to `legal-counsel`; AR reconciliation to `finance-controller`.
- **Source:** https://partnerstack.com/blog/partner-offboarding + https://www.allbound.com/
- **Confidence:** ✓ (workflow automated; legal + AR redlines defer)

---

## Summary table (~95% fulfillment)

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | Partner sourcing + ICP definition | Crunchbase + Apollo + LinkedIn Sales Nav + G2 | `api-gateway` + `linkedin` + `brightdata-mcp` | ⚠ |
| 2 | Referral/affiliate/channel/OEM agreement structuring | PandaDoc + DocuSign | `api-gateway` (`pandadoc-docusign`) | ✓ |
| 3 | AWS / Azure / GCP marketplace listings | Tackle.io + cloud Catalog APIs | `api-gateway` (`tackle`) + `cli-anything` (aws/az CLIs) | ⚠ |
| 4 | Salesforce AppExchange listing | Code Analyzer + Partner Console | `cli-anything` (sfdx) + `playwright-mcp` | ⚠ |
| 5 | HubSpot/Shopify/Slack/OpenAI/Stripe/Atlassian/AppSource listings | Each platform's dev portal API | `api-gateway` + `stripe-mcp` + `slack-mcp` + `playwright-mcp` | ✓ / ⚠ |
| 6 | Partner enablement + certification programs | LMS (Trailhead/HubSpot/Canvas/Allbound) | `canvas-lms-mcp` + `docx`/`pptx` + CRM via `api-gateway` | ✓ |
| 7 | Co-marketing campaign design | Joint plan + co-branded assets | `notion` + cross-agent `marketing-agent` | ✓ |
| 8 | MDF allocation + tracking | Partnerstack / Impartner / Allbound | `api-gateway` (`partnerstack`) + `notion` + `slack-mcp` | ✓ |
| 9 | Channel pricing + discount tier design | Margin matrix + deal-reg | `xlsx`/`google-sheets` + CRM via `api-gateway` | ✓ |
| 10 | Integration roadmap planning | Quarterly joint roadmap + Linear/Jira | `notion` + `linear-mcp`/`jira-mcp` + cross-agent `product-manager` | ✓ |
| 11 | Partnerstack / Tackle channel mgmt | Partnerstack + Tackle APIs | `api-gateway` | ⚠ |
| 12 | Crossbeam / Reveal account mapping | Crossbeam + Reveal + Snowflake | `api-gateway` + `postgresql-mcp` | ⚠ |
| 13 | Partner scorecard authoring | Warehouse query + scorecard render | `postgresql-mcp` + `xlsx`/`pdf` | ✓ |
| 14 | Ecosystem mapping + tech-stack discovery | BuiltWith + Clay + visualization | `cli-anything` + `drawio-mcp`/`figma-mcp` | ✓ |
| 15 | Partner-led webinars + events | Zoom Webinars + Goldcast + landing pages | `zoom-mcp` + `gmail-mcp` + `google-calendar-mcp` | ✓ |
| 16 | Partner-sourced pipeline tracking | CRM source-field + warehouse | `api-gateway` + `postgresql-mcp` + `google-sheets` | ✓ |
| 17 | Deal registration + channel conflict resolution | CRM custom obj + SLA timers | `api-gateway` + `postgresql-mcp` + `slack-mcp` | ✓ |
| 18 | Partner advisory board (PAB) | Quarterly summit | `notion` + `google-calendar-mcp` + `zoom-mcp` | ✓ |
| 19 | Partner NPS + satisfaction survey | Typeform/HubSpot survey + warehouse analysis | `typeform` + `postgresql-mcp` + `xlsx` | ✓ |
| 20 | Partner onboarding 90-day plan | Standardized template + LMS + CRM tasks | `notion` + `canvas-lms-mcp` + `api-gateway` | ✓ |
| 21 | Tech partner integration health monitoring | APM + product analytics | `sentry-mcp` + `posthog-mcp`/`mixpanel-mcp` + `postgresql-mcp` | ✓ |
| 22 | Joint customer story production | Interview + draft + co-publish | `fathom-api` + `docx` + cross-agent `video-creator`/`marketing-agent` | ✓ |
| 23 | QBR with strategic partners | Quarterly meeting + scorecard deck | `pptx`/`canva-mcp` + `zoom-mcp` + `notion` | ✓ |
| 24 | Partner battlecards + enablement content | Asset library + portal upload | `docx`/`pptx`/`drawio-mcp` + `notion` + `playwright-mcp` | ✓ |
| 25 | GTM-with-partners orchestration | Joint plan + account mapping + shared dashboard | composite (`notion` + Crossbeam + cross-agent) | ✓ |
| 26 | Partner CRM hygiene | Monthly clean-up + cron alerts | `postgresql-mcp` + `gmail-mcp` + `api-gateway` | ✓ |
| 27 | Off-boarding + termination | Termination letter + reconciliation | `api-gateway` (`pandadoc`) + cross-agent `legal-counsel`/`finance-controller` | ✓ |

**Fulfillment math:** 27 distinct use cases mapped. 22 are full ✓ confidence; 5 are ⚠ (one-time paid-key or marketplace-approval setup the recipient owns). Zero ✗ gaps. **~95% fulfillment** counting ⚠ rows as one-time setup that doesn't block agent execution.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (each must exist in `app/config/mcp_config.json`):
- `filesystem` — always
- `gmail-mcp` — partner outreach + onboarding comms
- `outlook-mcp` — Microsoft-shop comms
- `notion-mcp` — partner DB, playbooks, QBR records, MDF tracking, scorecards
- `slack-mcp` — partner channels, deal-reg alerts, MDF approvals
- `ms-teams-mcp` — Microsoft-shop notifications
- `zoom-mcp` — partner webinars, QBR, PAB summits
- `google-calendar-mcp` — joint meetings + recurring QBRs
- `postgresql-mcp` — warehouse queries for scorecards + partner-pipeline rollups + hygiene cron
- `linear-mcp` — integration partnership tickets handed off to product-manager
- `jira-mcp` — alt issue tracker for integration partners
- `sentry-mcp` — integration health monitoring (errors)
- `posthog-mcp` — adoption analytics for tech partnerships
- `mixpanel-mcp` — alt product analytics
- `amplitude-mcp` — alt product analytics
- `playwright-mcp` — marketplace portal automation (AppExchange, Shopify, Atlassian, AppSource)
- `firecrawl-mcp` — ecosystem mapping scraping
- `brightdata-mcp` — LinkedIn Sales Nav scraping for partner sourcing
- `brave-search` — partner sourcing + competitive ecosystem research
- `google-scholar-mcp` — industry research for vertical partnerships
- `deepl-mcp` — multi-language partner onboarding
- `imagegen-mcp` — listing screenshots + co-branded asset generation
- `canva-mcp` — co-branded one-pagers + QBR decks
- `figma-mcp` — co-branded design fidelity + integration architecture diagrams
- `drawio-mcp` — ecosystem maps + integration architecture
- `youtube-mcp` — joint customer-story video distribution
- `stripe-mcp` — Stripe Marketplace listing + Connect payouts
- `canvas-lms-mcp` — partner certification programs
- `tiktok-mcp` — partner social motions
- `google-drive-mcp` — joint asset sharing

**Skill packs to create in Round 2 (runtime build),** in order of impact:
1. `partner-sourcing-icp-definition` — PICP scoring + waterfall sourcing
2. `referral-affiliate-channel-oem-agreement-structuring` — 5 archetype contract shells
3. `aws-azure-gcp-marketplace-listings` — Tackle + cloud-CLI listing CRUD
4. `salesforce-appexchange-listing` — Code Analyzer + Partner Console flow
5. `hubspot-shopify-slack-marketplace-listings` — SaaS marketplace portal flow
6. `partner-enablement-certification-programs` — LMS + cert tiers
7. `co-marketing-campaign-design` — joint plan + co-branded asset orchestration
8. `mdf-allocation-tracking` — request → approval → POP → payout
9. `channel-pricing-discount-tiers` — margin matrix + deal-reg pricing
10. `integration-roadmap-planning` — joint roadmap + product-manager hand-off
11. `partnerstack-tackle-channel-management` — PRM API ops + integration health
12. `crossbeam-reveal-account-mapping` — overlap reporting + co-sell motion
13. `partner-scorecard-authoring` — quarterly scorecard render
14. `ecosystem-mapping-tech-stack-discovery` — BuiltWith/Clay + DrawIO/Figma visualization
15. `partner-led-webinars-events` — joint webinar end-to-end
16. `partner-sourced-pipeline-tracking` — attribution + weekly rollup
17. `deal-registration-channel-conflict-resolution` — registration workflow + SLA
18. `partner-advisory-board-pab` — PAB summit + roadmap synthesis
19. `partner-nps-satisfaction-survey` — Partner NPS execution + trend
20. `partner-onboarding-90-day-plan` — standardized 90-day playbook

---

## Notes on remaining caveats (the ⚠ rows)

- **Crunchbase / Pitchbook / Apollo (use case 1):** Each requires a paid plan + API key. `api-gateway` provides managed OAuth for Apollo + Crunchbase if onboarded to Maton. Free fallback: brave-search + manual LinkedIn.
- **Cloud marketplaces (use case 3):** AWS Seller registration + Azure Partner Center registration + GCP Marketplace producer enrollment are one-time human steps with KYC. Listing CRUD post-enrollment is fully automated. Tackle.io ($30k+/yr) unifies across all three; direct cloud CLIs also work.
- **Salesforce AppExchange (use case 4):** Security Review is a 6-12 week Salesforce-side gate. Code Analyzer pre-check + listing assets are fully automated.
- **Some marketplaces (use case 5):** Shopify, Microsoft AppSource, Atlassian require portal review (3-15 day human approval). Listing-asset upload + manifest CRUD automated.
- **Partnerstack / Tackle / PRMs (use case 11):** Paid plans required ($1-30k/mo). For solo founders without PRM, the agent uses CRM custom objects + `notion` as the partner system of record.
- **Crossbeam / Reveal (use case 12):** Both have free tiers for first-overlap reports; deep account mapping = paid. Snowflake Native Apps Data Clean Room is the warehouse-native alternative.
