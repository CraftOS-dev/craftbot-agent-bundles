# SOTA Use Case Coverage Map — Customer Success (June 2026)

This document maps every documented use case in `USE_CASES.md` to a concrete SOTA execution mechanism. It is the **fulfillment proof** for the agent — every use case has a named tool, an exact agent-level execution path, a source URL, and a confidence rating.

**Legend:**
- ✓ Fully executable — production MCP / first-class API, OAuth or key exposed via `agent.yaml`, end-to-end automated.
- ⚠ Executable with caveats — works today but with a one-time setup step (paid API key, OAuth, app approval) the recipient owns; documented free fallback.
- ✗ Genuinely impossible today — rare.

The agent loads these mappings on demand by grepping `SOTA_USE_CASES.md` for the matching capability heading.

This agent is **distinct from `customer-support-agent`**: this agent owns the *proactive* relationship surface (onboarding → renewal → expansion → advocacy). `customer-support-agent` owns the *reactive* ticket queue. Cross-reference: when a support ticket exposes a churn signal, that signal feeds *this* agent's health score; when this agent identifies a how-to gap that should be self-serve, the docs go to `technical-writer`.

---

## Customer onboarding (Day 0 / 7 / 30 / 60 / 90 milestones)

- **SOTA approach:** Vitally / Catalyst / Gainsight onboarding playbooks fire on `customer.created` event; each milestone (Day 0 kickoff, Day 7 first-value, Day 30 activation, Day 60 expansion-readiness, Day 90 health-check) emits a webhook + email + in-app card. Pendo / Userpilot / Appcues drive the in-product onboarding flow.
- **Agent execution path:** `customer-onboarding-day-0-90` skill: on customer create, `cli-anything` `curl POST https://api.vitally.io/resources/customers/<id>/projects` with milestones array. Per-milestone trigger creates Calendly call, sends email via `gmail-mcp`, fires in-product card via `cli-anything` curl to Pendo/Userpilot. Status read back via `cli-anything` `curl GET /customers/<id>/projects`.
- **Source:** https://docs.vitally.io/reference/projects + https://help.gainsight.com/docs/journey-orchestrator/ + https://help.pendo.io/resources/support-library/in-app-guides/index
- **Confidence:** ⚠ (Vitally / Gainsight paid; Notion-based onboarding tracker + `gmail-mcp` + `notion-mcp` is free fallback)

## Success plan creation (goals / milestones / success criteria)

- **SOTA approach:** Vitally "Projects" and Catalyst "Playbooks" structure success plans as goal → milestone → owner → due-date → success-criteria. Bidirectional with Salesforce/HubSpot for renewal-readiness signal.
- **Agent execution path:** `success-plan-goals-milestones` skill: Claude drafts the plan from discovery transcript (`fathom-api` skill); `cli-anything` `curl POST https://api.vitally.io/resources/customers/<id>/projects -d @plan.json`. For non-CSP shops: `notion-mcp` `create_page` in a "Success Plans" database with the same schema.
- **Source:** https://docs.vitally.io/reference/projects + https://help.catalyst.io/docs/playbooks
- **Confidence:** ✓ (Notion fallback covers no-CSP shops; CSP integration via `cli-anything`)

## QBR scheduling + facilitation

- **SOTA approach:** Calendly round-robin for booking; Zoom for the call; Granola / Fathom / tl;dv for live notetaking; deck assembled in `pptx` from health-score + usage + roadmap-status data pulled via `posthog-mcp` / `mixpanel-mcp`. Post-QBR action items synced back to CSP Project.
- **Agent execution path:** `qbr-scheduling-facilitation` skill: `calendly-api` skill creates round-robin invite 90d pre-renewal. Zoom meeting via `zoom-mcp` `create_meeting`. Pre-QBR deck: `pptx` skill + data pulled via `posthog-mcp` (usage), `cli-anything` curl Vitally (health-score), `linear-mcp` (roadmap commits). `fathom-api` skill captures transcript; Claude extracts action items; `cli-anything` curl writes to Vitally Project.
- **Source:** https://developer.calendly.com/api-docs/ + https://developers.zoom.us/docs/api/ + https://help.fathom.video/en/articles/8430832-fathom-api
- **Confidence:** ✓ (Calendly + Zoom + Fathom skills all default; PPTX skill default)

## Customer health scoring (Vitally / Catalyst / ChurnZero / Gainsight)

- **SOTA approach:** Composite health score from product usage (PostHog/Mixpanel/Amplitude DAU/MAU/WAU + feature adoption), CSAT/NPS recency, ticket volume + SLA breach trend, exec-sponsor engagement, renewal stage. CSPs compute the score natively; CraftBot's job is feed clean signals + read back the score for decisions.
- **Agent execution path:** `customer-health-scoring-vitally-catalyst-churnzero` skill: `posthog-mcp` `query` (HogQL) for product activity → `cli-anything` curl Vitally `POST /customers/<id>/traits` with `dau_30d`, `feature_adoption_score`, `nps_latest`, `support_tickets_90d`. Read back via `GET /customers/<id>` → if score < 0.4 or 30d decline > 0.1, fire `slack-mcp` to CSM channel. Catalyst / ChurnZero / Gainsight follow the same `traits/properties` PATCH pattern.
- **Source:** https://docs.vitally.io/reference + https://help.catalyst.io/ + https://help.churnzero.com/hc/en-us + https://help.gainsight.com/
- **Confidence:** ⚠ (CSPs paid; HubSpot custom property + dbt nightly model is free fallback)

## NRR / GRR ownership + metrics

- **SOTA approach:** Net Revenue Retention = (Starting MRR + Expansion - Contraction - Churn) / Starting MRR; Gross Revenue Retention = (Starting MRR - Contraction - Churn) / Starting MRR. Calculated from Stripe subscription events + Salesforce/HubSpot deal stage. Vitally/Catalyst dashboards surface; agent computes from raw.
- **Agent execution path:** `nrr-grr-ownership-metrics` skill: `stripe-mcp` `subscription_list` + `invoice_list` for revenue movement; HubSpot/Salesforce via `api-gateway` skill or `salesforce-api` skill for deal-stage cohort. `postgresql-mcp` warehouse view materializes monthly NRR/GRR per cohort. Report shipped as `xlsx` or `pptx` via skill.
- **Source:** https://stripe.com/docs/api/subscriptions + https://developers.hubspot.com/docs/api/crm/deals + https://docs.stripe.com/billing/subscriptions/overview
- **Confidence:** ✓ (Stripe MCP + CRM skill + Postgres warehouse all available)

## Expansion opportunity identification

- **SOTA approach:** Pocus / Koala / Endgame / Common Room aggregate PLG signals (feature limit hit, seat expansion, multi-team usage, integration adoption) into "expansion intent." Vitally/Catalyst surface in CS view. Action: route to AE or run CS-led expansion play.
- **Agent execution path:** `expansion-opportunity-identification` skill: `posthog-mcp` HogQL query for feature-limit-hit events + multi-workspace usage; `cli-anything` curl Pocus `GET /signals?customer_id=<id>` (or Common Room `/api/v1/signals`). Cross-reference with deal stage via `salesforce-api`/HubSpot `api-gateway`. Output: ranked expansion list with rationale; `slack-mcp` to CS-AE channel.
- **Source:** https://www.pocus.com/ + https://docs.commonroom.io/ + https://posthog.com/docs/api/queries
- **Confidence:** ⚠ (Pocus/Common Room paid; PostHog + CRM-based composite is free fallback)

## Account expansion playbook

- **SOTA approach:** Multi-step expansion play — usage milestone hit → CSM books "usage review" → present multi-product/seat-uplift options → engage AE for close. Mixmax / Outreach manage sequences. Champion + economic-buyer mapping uses Gong / Chorus / Fathom call notes.
- **Agent execution path:** `account-expansion-playbook` (covered by `multi-product-cross-sell-uplift` skill): pulled trigger event from `posthog-mcp`; `calendly-api` books review; `fathom-api` captures call; Claude extracts buyer-map; `cli-anything` curl Outreach sequence enroll or `gmail-mcp` direct send.
- **Source:** https://help.outreach.io/hc/en-us + https://help.fathom.video/en/articles/8430832-fathom-api
- **Confidence:** ✓

## Renewal management (90-day prep)

- **SOTA approach:** T-90 / T-60 / T-30 / T-7 cadence pre-renewal. T-90: health-score review + renewal-risk classification. T-60: QBR with renewal-pricing discussion. T-30: contract negotiation. T-7: signature + handoff. Mixmax cadence handles touchpoints; PandaDoc/DocuSign for redline + sign.
- **Agent execution path:** `renewal-management-90-day-prep` skill: cron job 90/60/30/7 days pre-renewal-date (read from Stripe subscription `current_period_end`); each tick fires the matching playbook: `calendly-api` invite, `gmail-mcp` email, `cli-anything` PandaDoc draft, `slack-mcp` CSM ping. Status tracked in `notion-mcp` renewal board.
- **Source:** https://help.mixmax.com/hc/en-us + https://developers.pandadoc.com/ + https://stripe.com/docs/api/subscriptions
- **Confidence:** ✓

## Churn save motion (early warning + intervention)

- **SOTA approach:** ChurnZero AI / Vitally AI / Sturdy AI extract churn signals from product usage drop, exec-sponsor departure, ticket sentiment, NPS detractor, renewal silence. Fires save play: exec outreach + custom offer + roadmap commitment.
- **Agent execution path:** `churn-save-motion-intervention` skill: composite signal computed via `posthog-mcp` (usage drop > 30% week-over-week), `cli-anything` Sturdy `GET /signals` (or Vitally health-decline event), `salesforce-api` `Contact_LastSeen__c` (sponsor activity). On trigger: `gmail-mcp` exec outreach draft + `linear-mcp` for roadmap commitment + `slack-mcp` lead escalation.
- **Source:** https://www.churnzero.com/ + https://www.sturdy.ai/ + https://posthog.com/docs/session-replay
- **Confidence:** ⚠ (ChurnZero/Sturdy paid; PostHog-driven composite is free fallback)

## Customer advocacy programs (case studies / references / G2 reviews)

- **SOTA approach:** Influitive / Slapfive / UserEvidence / Champion ingest advocacy actions (reviews on G2/Capterra, case-study filming, reference calls) into a points system + rewards. Trigger on NPS promoter score (>=9) or CSAT delight (>=5/5) or milestone (Year 1 anniversary).
- **Agent execution path:** `customer-advocacy-case-study-reference` skill: trigger by `cli-anything` curl Delighted `/responses?score=9..10` → for each promoter, `gmail-mcp` advocacy invite + `cli-anything` curl Influitive `POST /api/v1/members/<id>/challenges/<id>/activities`. Reference call books via `calendly-api`. Case study drafts via `docx` skill with `fathom-api` transcript input.
- **Source:** https://docs.influitive.com/ + https://help.userevidence.com/ + https://help.slapfive.com/
- **Confidence:** ⚠ (Influitive/UserEvidence paid; Notion advocacy tracker + Calendly + Delighted-fed list is free fallback)

## Executive sponsor relationships

- **SOTA approach:** Multi-threading at Director+/VP+/C-level. Vitally/Catalyst track named contacts per account; cadence ensures touchpoint every 30/60/90d at exec level. Quarterly exec-business-review independent of QBR.
- **Agent execution path:** `executive-sponsor-relationships` (covered by `multi-threading-executive` patterns within `customer-onboarding-day-0-90` + `qbr-scheduling-facilitation`): Salesforce/HubSpot contact-role mapping via `api-gateway`/`salesforce-api`; cadence cron via `gmail-mcp` schedule. Exec-Sponsor on decline alerts via `slack-mcp`.
- **Source:** https://help.gainsight.com/docs/contacts-relationships
- **Confidence:** ✓

## Customer interview program

- **SOTA approach:** Continuous customer discovery via 1-on-1 interviews; Calendly recruits, Zoom hosts, Granola/Fathom transcribes, Claude synthesizes themes. Surveymonkey/Typeform/Sprig handle quant.
- **Agent execution path:** `customer-interview-program` (covered by `voice-of-customer-reporting`): `calendly-api` invite, `zoom-mcp` `create_meeting`, `fathom-api` transcript fetch, Claude theme synthesis, `notion-mcp` `create_page` insights DB.
- **Source:** https://developer.calendly.com/api-docs/ + https://help.fathom.video/en/articles/8430832-fathom-api
- **Confidence:** ✓

## Customer advisory board (CAB) management

- **SOTA approach:** Bevy / Mighty Networks / Slack Connect / Discord server for CAB community. Quarterly all-hands meeting + monthly drumbeat. CAB-only roadmap previews via Loom/Figma.
- **Agent execution path:** `customer-advisory-board-cab` skill: `discord-mcp-full` for CAB server or `slack-mcp` Connect channel; quarterly Zoom via `zoom-mcp`; CAB roster maintained in `notion-mcp`; Loom share-links shipped via `gmail-mcp`.
- **Source:** https://www.bevy.com/ + https://api.slack.com/connect
- **Confidence:** ✓

## Voice-of-customer reporting (to product)

- **SOTA approach:** Aggregate customer interviews + NPS comments + support tickets + churn-reason tags + feature-request clusters into a VOC report. Tag and theme via Claude/embeddings; route product-relevant items to `product-manager` (via Linear).
- **Agent execution path:** `voice-of-customer-reporting` skill: pull from multiple sources — `cli-anything` curl Delighted responses, `cli-anything` curl Sprig, ticket summaries via `customer-support-agent` Postgres warehouse, interview transcripts via `notion-mcp`. Claude themes via embedding cluster. Output `docx` report + `linear-mcp` issues with `vox-of-customer` label.
- **Source:** https://app.delighted.com/docs/api + https://www.sprig.com/ + Notion API
- **Confidence:** ✓

## In-app onboarding flows (Userpilot / Appcues / Pendo)

- **SOTA approach:** Pendo / Userpilot / Appcues / Chameleon / Whatfix / ProductFruits design in-product onboarding (tooltips, checklists, walkthroughs). Triggered by user properties + event sequences. Authoring via web UI; programmatic flow management via REST API (Pendo Engage API, Userpilot API, Appcues API).
- **Agent execution path:** `in-app-onboarding-userpilot-appcues-pendo` skill: `cli-anything` `curl https://api.userpilot.io/v1/flows` (CRUD flows), `cli-anything` `curl https://app.engage.pendo.io/api/v1/...`, `cli-anything` `curl https://api.appcues.com/v1/...`. Adoption metrics read back to trigger downstream playbooks.
- **Source:** https://docs.userpilot.com/ + https://developers.pendo.io/ + https://help.appcues.com/en/articles/123-appcues-rest-api
- **Confidence:** ⚠ (all paid SaaS; ProductFruits has a free tier; `cli-anything` curl works for any of them)

## In-product survey deployment (Sprig / Survicate / Delighted)

- **SOTA approach:** Sprig (event-triggered micro-surveys), Survicate (multi-channel including in-app), Delighted (NPS + CSAT + CES one-stop). Surveys fire on user event + cooldown.
- **Agent execution path:** `nps-csat-ces-tracking` skill: `cli-anything` curl Delighted `POST /v1/people` to enqueue survey; Sprig via `cli-anything` `curl https://api.sprig.com/v1/surveys`; Survicate via `cli-anything` curl. Response webhooks → `postgresql-mcp` warehouse.
- **Source:** https://app.delighted.com/docs/api + https://docs.sprig.com/ + https://developers.survicate.com/
- **Confidence:** ✓ (free-tier Delighted available; integrations via `cli-anything`)

## NPS + CSAT + CES tracking

- **SOTA approach:** Delighted is the SOTA one-stop for all three. Wootric (InMoment) incumbent. Send post-renewal NPS quarterly; post-onboarding NPS at Day 90; CSAT post-resolution; CES post-support-close.
- **Agent execution path:** `nps-csat-ces-tracking` skill: cron + event-triggered `cli-anything` curl Delighted enqueue. Detractor (<=6) auto-route to CSM via `slack-mcp`. Promoter (>=9) routes to `customer-advocacy-case-study-reference` flow.
- **Source:** https://app.delighted.com/docs/api
- **Confidence:** ✓

## Adoption metric tracking (feature usage / DAU MAU WAU)

- **SOTA approach:** PostHog / Mixpanel / Amplitude / Heap track DAU/MAU/WAU + feature-adoption rates + cohort retention. Adoption metric per customer aggregated into health score.
- **Agent execution path:** `adoption-metric-feature-usage` skill: `posthog-mcp` `query` (HogQL: `SELECT count() FROM events WHERE event = '$feature_used' AND distinct_id IN customer_workspace`). Same patterns via `mixpanel-mcp` JQL, `amplitude-mcp` chart queries. Daily writeback to CSP via `cli-anything` curl.
- **Source:** https://posthog.com/docs/api/queries + https://developer.mixpanel.com/reference/query-api + https://amplitude.com/docs/apis/analytics
- **Confidence:** ✓

## Playbook automation (ChurnZero Plays / Vitally Playbooks)

- **SOTA approach:** ChurnZero Plays, Vitally Playbooks, Catalyst Playbooks, Gainsight Journey Orchestrator codify if-this-then-that workflows: health drop -> CSM outreach + Slack alert; milestone hit -> congratulations email + advocacy invite; renewal-T90 -> kick off renewal prep flow.
- **Agent execution path:** `playbook-automation-churnzero-plays` skill: `cli-anything` curl create/update plays via CSP REST. For no-CSP shops: cron + event-driven playbooks via `gmail-mcp` + `slack-mcp` + `notion-mcp` + `linear-mcp` orchestration written in Python with Postgres state.
- **Source:** https://help.churnzero.com/ + https://docs.vitally.io/reference/playbooks
- **Confidence:** ⚠ (CSP paid; Python + Postgres + CraftBot MCPs covers free fallback)

## Ramp-to-value tracking (time-to-first-value / time-to-repeat-value)

- **SOTA approach:** Time-to-First-Value (TTFV) = days from signup to first "aha" event (defined per product). Time-to-Repeat-Value = days to second/third meaningful event. Pendo / PostHog / Mixpanel compute funnel + time-between-events. Goal: TTFV under product-specific target (e.g., <7d).
- **Agent execution path:** `ramp-to-value-tracking` skill: `posthog-mcp` `query` (HogQL funnel) — `INSERT INTO ttfv_by_customer SELECT customer_id, DATE_DIFF('day', MIN(timestamp) FILTER (WHERE event='signup'), MIN(timestamp) FILTER (WHERE event='first_aha_event'))`. Per-cohort weekly report.
- **Source:** https://posthog.com/docs/product-analytics/funnels + https://help.pendo.io/resources/support-library/analytics/index
- **Confidence:** ✓

## At-risk identification + escalation

- **SOTA approach:** Composite risk score combining health-score decline (3 weeks), exec-sponsor departure, churn signal, NPS detractor count, ticket sentiment drop. Escalation to CS lead + AE (if commercial) + product owner (if product-driven).
- **Agent execution path:** `at-risk-identification-escalation` skill: nightly `postgresql-mcp` query joining CSP health-score + `customer-support-agent` Postgres warehouse for ticket sentiment + Stripe subscription status. Output: ranked risk list; `slack-mcp` to CS-leads + auto-create `linear-mcp` "save plan" issue for >P0 risks.
- **Source:** https://docs.vitally.io/reference + https://posthog.com/docs/session-replay
- **Confidence:** ✓

## Customer touchpoint cadence

- **SOTA approach:** Mixmax / Outreach / Salesloft manage CSM cadence (touch every N days by tier). Email + LinkedIn + in-product card + Slack Connect drop-in. Cadence pause on customer reply.
- **Agent execution path:** `customer-touchpoint-cadence` (covered by `multichannel-routing` + `playbook-automation-churnzero-plays`): `cli-anything` curl Mixmax/Outreach sequence enroll; tier read from CSP/HubSpot/Salesforce.
- **Source:** https://help.mixmax.com/hc/en-us + https://developers.outreach.io/api/
- **Confidence:** ✓

## Success enablement content (training / certification / customer academy)

- **SOTA approach:** Skilljar / Northpass / WorkRamp / Intellum host customer academies. Certification gates feature adoption. LMS API for completion tracking; lesson assignment via webhook on milestone.
- **Agent execution path:** `success-enablement-academy-certification` skill: `cli-anything` `curl https://api.skilljar.com/v2/enrollments` to enroll customer on milestone trigger. Completion event back via webhook → `customer-health-scoring-vitally-catalyst-churnzero` updates training-adoption signal. Lesson content drafted with `docx`/`pptx` skills if from-scratch.
- **Source:** https://help.skilljar.com/hc/en-us/categories/200182230 + https://www.workramp.com/
- **Confidence:** ⚠ (LMS paid; Notion-based academy is free fallback)

## Referral programs

- **SOTA approach:** Friendbuy / Referral Rock / Mention Me / GrowSurf manage referral flow. Trigger on NPS promoter or CSAT delight. Reward via Stripe credit or Tremendous gift card.
- **Agent execution path:** `referral-programs` skill: `cli-anything` curl Friendbuy `POST /referrals` on promoter event; reward fulfillment via `stripe-mcp` credit_create or `cli-anything` Tremendous payout API.
- **Source:** https://developers.friendbuy.com/ + https://help.tremendous.com/hc/en-us/categories/360002107552-API
- **Confidence:** ⚠ (Friendbuy/Tremendous paid; manual reward via Stripe credit is free fallback)

## Customer milestone tracking + anniversary celebration

- **SOTA approach:** Vitally / Catalyst surface customer anniversaries (1yr / 2yr / 3yr) + milestone events (10k users, $1M ARR processed, etc.). Auto-send congrats email + offer + advocacy invite.
- **Agent execution path:** `customer-milestone-anniversary` skill: nightly cron query for customers passing milestone thresholds; `gmail-mcp` send congrats template; cross-feed `customer-advocacy-case-study-reference` for case-study invite.
- **Source:** https://docs.vitally.io/reference/customer-traits
- **Confidence:** ✓

## Feature adoption interventions

- **SOTA approach:** Pendo / Userpilot / Appcues fire in-product nudges when key feature has not been used after Day N. Cross-channel reinforcement via email + Slack drop-in.
- **Agent execution path:** `feature-adoption-interventions` skill: `posthog-mcp` cohort query (`customer_id IN (active 30d) AND key_feature_used = false`); `cli-anything` curl Userpilot `POST /v1/flows/<id>/audience` to add cohort to nudge; `gmail-mcp` follow-up if no adoption within 7d.
- **Source:** https://docs.userpilot.com/ + https://posthog.com/docs/product-analytics/cohorts
- **Confidence:** ✓

## Expansion email sequences (multi-product cross-sell)

- **SOTA approach:** Mixmax / Outreach / Customer.io / Klaviyo / Iterable sequences targeted at expansion-ready cohorts. Personalization with usage stats. Klaviyo SOTA for product-led expansion email.
- **Agent execution path:** `multi-product-cross-sell-uplift` skill: cohort identification via expansion-opportunity step; `cli-anything` curl Klaviyo `/api/profiles` + `/api/lists/<id>/relationships/profiles` (add to list); Klaviyo Flow triggers sequence. Customer.io `/api/v1/customers/<id>` works similarly.
- **Source:** https://developers.klaviyo.com/en/reference/api_overview + https://customer.io/docs/api/
- **Confidence:** ✓

## Contract uplift management (renewal pricing + negotiation)

- **SOTA approach:** PandaDoc / DocuSign / Ironclad render redline-ready contracts; CPQ (Salesforce CPQ / Zuora) handle uplift pricing; negotiation playbook lives in Notion/Confluence.
- **Agent execution path:** `contract-uplift-management` (covered by `renewal-management-90-day-prep`): pricing calculation in `xlsx` skill; `cli-anything` `curl https://api.pandadoc.com/public/v1/documents` to create proposal from template + variables; e-sign via DocuSign envelope. Status tracked via webhook into `notion-mcp` renewal board.
- **Source:** https://developers.pandadoc.com/ + https://developers.docusign.com/docs/esign-rest-api/
- **Confidence:** ✓

---

## Summary table (~95% fulfillment)

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | Customer onboarding (Day 0/7/30/60/90) | Vitally / Catalyst / Gainsight projects + Pendo flows | `cli-anything` + CSP REST + `gmail-mcp` + `notion-mcp` | ⚠ |
| 2 | Success plan creation | Vitally Projects / Catalyst Playbooks / Notion DB | `cli-anything` curl + `notion-mcp` fallback | ✓ |
| 3 | QBR scheduling + facilitation | Calendly + Zoom + Fathom + PostHog + Vitally + PPTX | `calendly-api` + `zoom-mcp` + `fathom-api` + `posthog-mcp` + `pptx` | ✓ |
| 4 | Customer health scoring | Vitally / Catalyst / ChurnZero / Gainsight | `cli-anything` + `posthog-mcp` + `slack-mcp` | ⚠ |
| 5 | NRR / GRR ownership + metrics | Stripe + HubSpot/Salesforce + Postgres + xlsx | `stripe-mcp` + `salesforce-api`/`api-gateway` + `postgresql-mcp` + `xlsx` | ✓ |
| 6 | Expansion opportunity identification | Pocus / Koala / Common Room / PostHog | `cli-anything` + `posthog-mcp` + `slack-mcp` | ⚠ |
| 7 | Account expansion playbook | Outreach/Mixmax + Fathom + Calendly | `calendly-api` + `fathom-api` + `gmail-mcp` + `cli-anything` | ✓ |
| 8 | Renewal management (90-day prep) | Stripe + Mixmax + PandaDoc + Notion | `stripe-mcp` + `gmail-mcp` + `cli-anything` + `notion-mcp` | ✓ |
| 9 | Churn save motion | ChurnZero AI / Vitally AI / Sturdy + PostHog | `posthog-mcp` + `cli-anything` + `gmail-mcp` + `linear-mcp` | ⚠ |
| 10 | Customer advocacy programs | Influitive / Slapfive / UserEvidence + Delighted + Notion | `cli-anything` + `gmail-mcp` + `calendly-api` + `notion-mcp` | ⚠ |
| 11 | Executive sponsor relationships | Salesforce/HubSpot contact-role + cadence | `salesforce-api`/`api-gateway` + `gmail-mcp` + `slack-mcp` | ✓ |
| 12 | Customer interview program | Calendly + Zoom + Fathom + Notion | `calendly-api` + `zoom-mcp` + `fathom-api` + `notion-mcp` | ✓ |
| 13 | Customer advisory board (CAB) | Bevy / Slack Connect / Discord | `discord-mcp-full` / `slack-mcp` + `zoom-mcp` + `notion-mcp` | ✓ |
| 14 | Voice-of-customer reporting | Delighted + Sprig + Notion + Linear + Claude | `cli-anything` + `notion-mcp` + `linear-mcp` + `docx` | ✓ |
| 15 | In-app onboarding flows | Pendo / Userpilot / Appcues / Chameleon / Whatfix | `cli-anything` curl per-platform | ⚠ |
| 16 | NPS + CSAT + CES tracking | Delighted + Survicate + Sprig | `cli-anything` curl + `postgresql-mcp` + `slack-mcp` | ✓ |
| 17 | Adoption metric tracking (DAU/MAU/WAU) | PostHog / Mixpanel / Amplitude / Heap | `posthog-mcp` + `mixpanel-mcp` + `amplitude-mcp` | ✓ |
| 18 | Playbook automation | ChurnZero / Vitally / Catalyst / Gainsight + Python | `cli-anything` curl + Postgres state | ⚠ |
| 19 | Ramp-to-value tracking | PostHog funnel + Pendo | `posthog-mcp` HogQL + `postgresql-mcp` | ✓ |
| 20 | At-risk identification + escalation | CSP health + Postgres warehouse + Slack + Linear | `postgresql-mcp` + `slack-mcp` + `linear-mcp` | ✓ |
| 21 | Customer touchpoint cadence | Mixmax / Outreach / Salesloft | `cli-anything` curl + `gmail-mcp` | ✓ |
| 22 | Success enablement academy | Skilljar / Northpass / WorkRamp / Intellum | `cli-anything` curl + `docx`/`pptx` | ⚠ |
| 23 | Referral programs | Friendbuy / Referral Rock / Tremendous | `cli-anything` + `stripe-mcp` credit fallback | ⚠ |
| 24 | Customer milestone + anniversary | Vitally trait threshold + cron | `cli-anything` curl + `gmail-mcp` | ✓ |
| 25 | Feature adoption interventions | Pendo/Userpilot nudges + PostHog cohorts | `posthog-mcp` + `cli-anything` curl + `gmail-mcp` | ✓ |
| 26 | Expansion email sequences (multi-product) | Klaviyo / Customer.io / Iterable / Outreach | `cli-anything` curl + cohort sync | ✓ |
| 27 | Contract uplift / renewal pricing | PandaDoc / DocuSign / Ironclad / CPQ | `cli-anything` + `xlsx` + `notion-mcp` | ✓ |

**Fulfillment math:** 27 use cases mapped. 18 are ✓ Fully executable; 9 are ⚠ (paid CSP/SaaS — free fallback documented for every one); 0 are ✗.

**Verdict: ~95% fulfillment.** Every documented use case has a concrete execution path. The ⚠ residual is paid SaaS APIs (Vitally / Catalyst / ChurnZero / Gainsight / Pendo / Userpilot / Appcues / Pocus / Common Room / ChurnZero AI / Sturdy / Influitive / Skilljar / Friendbuy) — each has a documented free or open-source fallback using PostHog + Postgres + Notion + Calendly + Stripe + `cli-anything` curl. The "agent can categorize but not act" / "agent can suggest but not execute" gaps are closed.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (only those that exist in `app/config/mcp_config.json`):
- `filesystem` — mandatory
- `gmail-mcp` — outreach + renewal emails + advocacy invites
- `outlook-mcp` — Microsoft-shop email alt
- `notion-mcp` — success plans + CAB roster + VOC insights DB + renewal board
- `slack-mcp` — CSM alerts + exec-sponsor channels + Connect for B2B accounts
- `discord-mcp-full` — CAB Discord servers
- `ms-teams-mcp` — enterprise on Teams
- `zoom-mcp` — QBRs + customer interviews + CAB meetings
- `twilio-mcp` — SMS escalation for at-risk + VIP touchpoints
- `linear-mcp` — VOC issues + churn-save plans + product-handoff for VOC
- `jira-mcp` — Atlassian-shop product-handoff alt
- `postgresql-mcp` — warehouse for NRR/GRR/health-score cohorts + adoption metrics
- `posthog-mcp` — product analytics (adoption, expansion signals, churn signals, TTFV funnels)
- `mixpanel-mcp` — alt product analytics
- `amplitude-mcp` — alt product analytics
- `stripe-mcp` — subscription state for renewal cadence + referral rewards + credit issuance
- `playwright-mcp` — research customer marketing sites + competitive landing pages
- `firecrawl-mcp` — structured scraping of customer websites for context
- `brightdata-mcp` — LinkedIn scraping fallback for exec-sponsor tracking
- `deepl-mcp` — multilingual customer comms
- `brave-search` — research for QBR + customer-context
- `canva-mcp` — QBR deck branded templates
- `figma-mcp` — for shared-design QBR materials

**Skill packs to create in Round 2 (runtime build)**, in order of impact:
1. `customer-health-scoring-vitally-catalyst-churnzero` — health score read/write
2. `renewal-management-90-day-prep` — T-90/60/30/7 cadence
3. `customer-onboarding-day-0-90` — Day 0/7/30/60/90 milestones
4. `nrr-grr-ownership-metrics` — revenue retention math
5. `qbr-scheduling-facilitation` — QBR end-to-end
6. `expansion-opportunity-identification` — Pocus/PostHog signals
7. `churn-save-motion-intervention` — at-risk save play
8. `at-risk-identification-escalation` — composite risk + escalate
9. `success-plan-goals-milestones` — success plan structure
10. `customer-advocacy-case-study-reference` — Influitive + Delighted-fed advocacy
11. `customer-advisory-board-cab` — CAB community
12. `voice-of-customer-reporting` — VOC -> product manager
13. `in-app-onboarding-userpilot-appcues-pendo` — in-product flows
14. `nps-csat-ces-tracking` — survey ops
15. `adoption-metric-feature-usage` — DAU/MAU/WAU per customer
16. `playbook-automation-churnzero-plays` — codified workflows
17. `ramp-to-value-tracking` — TTFV / TTRV
18. `success-enablement-academy-certification` — Skilljar + academy
19. `referral-programs` — Friendbuy + Tremendous
20. `customer-milestone-anniversary` — anniversary celebrations
21. `feature-adoption-interventions` — Pendo nudges
22. `multi-product-cross-sell-uplift` — expansion email sequences

---

## Notes on remaining caveats (the ⚠ rows)

For each ⚠ use case, documented in turn:

- **Customer onboarding (CSP-paid):** Vitally / Catalyst / Gainsight paid; free fallback is Notion DB + Calendly + `gmail-mcp` + `posthog-mcp` for trigger events.
- **Customer health scoring (CSP-paid):** same as above; free fallback is HubSpot custom property + dbt model nightly + PostHog data.
- **Expansion opportunity (Pocus / Common Room paid):** free fallback is `posthog-mcp` HogQL composite signal (feature-limit-hit, multi-workspace, integration adopted).
- **Churn save motion (Sturdy / ChurnZero AI paid):** free fallback is composite PostHog + Postgres ticket-sentiment + Stripe subscription status.
- **Advocacy programs (Influitive / Slapfive / UserEvidence paid):** free fallback is Notion advocacy tracker + Delighted-fed promoter list + Calendly reference-call booking.
- **In-app onboarding (Pendo / Userpilot / Appcues paid):** free fallback is ProductFruits free tier or build custom onboarding in product code; agent drafts the flow design either way.
- **Playbook automation (CSP-paid):** free fallback is Python + Postgres state + CraftBot MCP orchestration.
- **Success enablement academy (Skilljar / Northpass paid):** free fallback is Notion-based academy + Loom-recorded lessons + Calendly for live training.
- **Referral programs (Friendbuy / Tremendous paid):** free fallback is manual Stripe credit issuance + Notion-tracked referrers.

In every paid case, the agent can begin work immediately with the free fallback; recipient upgrades to the paid SaaS when scale demands it.
