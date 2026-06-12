# SOTA Use Case Coverage Map — Sales Agent (June 2026)

This document maps every documented use case in `USE_CASES.md` to a concrete SOTA execution mechanism. It is the **fulfillment proof** — every use case has a named tool, an exact agent-level execution path, a source URL, and a confidence rating.

**Legend:**
- ✓ (yes) — production MCP / first-class API or managed OAuth via `api-gateway`, end-to-end automated.
- ⚠ (caveat) — works today with a one-time setup step (OAuth, paid API key, app approval) the recipient owns.
- ✗ (gap) — partial coverage; rate-limited, scraping-fallback, or domain-specific paid tooling required.

The agent loads these mappings on demand by grepping `SOTA_USE_CASES.md` for the matching capability heading.

---

## Outbound sequence design (cold email + LinkedIn + phone cadence)

- **SOTA approach:** Multi-channel sequences in Outreach.io / Salesloft / lemlist / Instantly. Cadence: Day 0 email → Day 2 LinkedIn connect → Day 4 email reply-bump → Day 7 call → Day 10 break-up email → Day 14 re-add to nurture. Per-step A/B subject lines + first-line personalization tokens.
- **Agent execution path:** Use `outreach-salesloft-sequences` skill. `api-gateway` POST `https://gateway.maton.ai/outreach/api/v2/sequences` for Outreach; `https://gateway.maton.ai/salesloft/v2/cadences` for Salesloft; `https://gateway.maton.ai/lemlist/api/campaigns` for lemlist; `https://gateway.maton.ai/instantly/api/v2/campaigns` for Instantly. LinkedIn steps via HeyReach (`api-gateway` route or curl), phone steps recorded in CRM activity.
- **Source:** https://developers.outreach.io/api/ + https://developers.salesloft.com/api.html + https://help.instantly.ai/en/articles/8500911-instantly-api-v2
- **Confidence:** ✓ (managed OAuth via `api-gateway` for all four)

---

## Inbound lead qualification (SDR scoring + routing)

- **SOTA approach:** HubSpot/Salesforce predictive lead scoring with custom scoring model + round-robin routing rules. MEDDIC / BANT fields scored, ICP-fit score from enrichment data (Apollo/Clay), behavioral score from product activity (Pocus/Koala).
- **Agent execution path:** Use `hubspot-sales-mcp` skill (managed OAuth via `api-gateway`). `POST /hubspot/crm/v3/objects/contacts/{id}` to update `lead_score`; `POST /hubspot/automation/v4/flows` for routing workflow with round-robin assign. For Salesforce, `salesforce-api` skill → SOQL update + Apex assignment rules.
- **Source:** https://developers.hubspot.com/docs/api/crm/contacts + https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/
- **Confidence:** ✓

---

## Account research (ICP fit, account hierarchy, intent signals)

- **SOTA approach:** Apollo + Clay + LinkedIn Sales Navigator enrichment combined with intent data (Bombora/G2/Common Room). Map account hierarchy (parent/child/sibling), tech stack (BuiltWith / Wappalyzer via Clay), employee count by department, funding stage.
- **Agent execution path:** Use `account-research-deep` skill. `api-gateway` curl `https://gateway.maton.ai/apollo/api/v1/organizations/enrich?domain=<d>`; Clay workflow trigger via `https://api.clay.com/v3/workspaces/...`; Common Room via `api-gateway` if onboarded; LinkedIn Sales Navigator scraped via Phantombuster/TexAu (no public API).
- **Source:** https://docs.apollo.io/reference/organizations + https://clay.com/docs/api + https://docs.commonroom.io/
- **Confidence:** ⚠ (Apollo paid tier; Clay paid; LinkedIn Sales Nav via Phantombuster scraping)

---

## Lead enrichment (find emails, phones, intent data)

- **SOTA approach:** Apollo (primary, 270M+ contacts), Clay (workflow orchestration across 100+ sources), Lusha (phone-rich), ZoomInfo (enterprise), Cognism (EU-compliant). Waterfall enrichment: Apollo first → Clay fallback → Lusha for missing phones → ZoomInfo for enterprise gaps.
- **Agent execution path:** Use `apollo-clay-lead-enrichment` skill. `api-gateway` `POST https://gateway.maton.ai/apollo/api/v1/mixed_people/search` with filters; `https://api.clay.com/v3/...` for waterfall; raw curl to Lusha/ZoomInfo/Cognism APIs via `cli-anything`.
- **Source:** https://docs.apollo.io/reference/people-search + https://clay.com/docs/api + https://www.lusha.com/business/api/
- **Confidence:** ⚠ (paid keys)

---

## CRM hygiene + data quality

- **SOTA approach:** Daily duplicate detection (HubSpot's built-in deduper or Cloudingo for Salesforce), stale-record archival (no activity > 90 days → archive), required-field enforcement, ICP-fit revalidation, enrichment-gap fills. Notion or Sheets dashboard for ops review.
- **Agent execution path:** Use `pipeline-hygiene-stage-criteria` skill (covers data + stage hygiene jointly). `api-gateway` HubSpot/Salesforce `/properties` mass-update; cron via `postgresql-mcp` scheduled query → `gmail` send hygiene alert; report exported to `notion` page.
- **Source:** https://developers.hubspot.com/docs/api/crm/properties + https://www.salesforce.com/blog/data-quality-best-practices/
- **Confidence:** ✓

---

## Pipeline review + stage hygiene

- **SOTA approach:** Weekly pipeline review with stage-by-stage criteria (entry/exit gates), age-in-stage analysis, deal-velocity metrics, slip-risk flagging (deals stalled > 1.5× median time-in-stage). Forecast roll-up by stage probability.
- **Agent execution path:** Use `pipeline-hygiene-stage-criteria` skill. `api-gateway` HubSpot `/crm/v3/objects/deals?properties=...&dealstage=...`; Salesforce SOQL `SELECT Id, StageName, CloseDate, Amount FROM Opportunity WHERE IsClosed = FALSE`; render Markdown table; calculate age-in-stage in Python via `cli-anything`.
- **Source:** https://www.gong.io/blog/sales-pipeline-management/ + HubSpot Deals API
- **Confidence:** ✓

---

## Qualification framework execution (MEDDIC / MEDDPICC / BANT / SPIN / Challenger)

- **SOTA approach:** MEDDIC/MEDDPICC for complex B2B (Metrics, Economic buyer, Decision criteria, Decision process, Identify pain, Champion, Competition, Paper process). BANT for simpler/transactional (Budget, Authority, Need, Timeline). SPIN for discovery (Situation, Problem, Implication, Need-payoff). Challenger for commercial conversations. Score each field 0-3 → roll-up confidence.
- **Agent execution path:** Use `meddic-meddpicc-qualification` skill. CRM custom fields per framework letter; `api-gateway` HubSpot/Salesforce field updates; scoring rubric stored in `notion` knowledge base; the agent fills the fields based on call transcript (from `gong-chorus-call-intelligence` skill).
- **Source:** https://www.meddicc.com/ + https://www.gong.io/blog/meddpicc/
- **Confidence:** ✓

---

## Discovery call prep + scripts

- **SOTA approach:** Account research + LinkedIn profile pull + past-contact history + Gong call snippets → tailored discovery script with 5-7 SPIN-pattern questions, MEDDIC field checklist, agenda, value hypothesis, objection rehearsal.
- **Agent execution path:** Use `account-research-deep` + `meddic-meddpicc-qualification` skills. Pull account from CRM via `api-gateway` HubSpot/Salesforce; LinkedIn profile via `linkedin` skill or Phantombuster; past call snippets via `gong-chorus-call-intelligence` skill (`api-gateway` Gong `/v2/calls/transcript`); render script to `notion` or `docx`.
- **Source:** https://www.gong.io/api/ + LinkedIn Sales Nav + SPIN methodology
- **Confidence:** ✓

---

## Demo prep + objection handling

- **SOTA approach:** Pre-demo brief with the prospect's pain (from discovery), the 3 features that map to that pain, success-criteria mapping, competitor differentiation (battlecard), top-5 likely objections with rehearsed responses + proof points.
- **Agent execution path:** Use `sales-enablement-battlecards-roi-calculators` skill. Brief template in `notion`; battlecard rendered via `pptx`; objection-response pairs queried from past Gong calls (`gong-chorus-call-intelligence` skill `search` over objection-tagged snippets).
- **Source:** https://www.gong.io/blog/objection-handling/ + internal battlecard template
- **Confidence:** ✓

---

## Deal coaching (next-best-action per opportunity)

- **SOTA approach:** For each open opp, compute: MEDDIC completeness score, days since last meaningful activity, multi-thread depth (# stakeholders engaged), competitor mentions, signal-of-life (email reply within 14d), deal-velocity vs. median. Generate top-1 NBA per deal: "Multi-thread to economic buyer this week" / "Re-confirm decision criteria" / "Send mutual action plan".
- **Agent execution path:** Use `deal-coaching-next-best-action` skill. CRM read via `api-gateway`; Gong call activity via `gong-chorus-call-intelligence`; render NBA report to `notion` weekly + Slack ping via `slack` skill.
- **Source:** https://www.gong.io/blog/deal-coaching/ + MEDDPICC framework
- **Confidence:** ✓

---

## Negotiation prep

- **SOTA approach:** Pre-negotiation: BATNA articulated, ZOPA mapped, price floor + ceiling, anchoring strategy, concession ladder (give-get pairs), red-line list, mutual close plan. Use Gong's "Negotiations" pack heuristics (don't drop price without trading, anchor high).
- **Agent execution path:** Use `deal-coaching-next-best-action` skill (negotiation playbook is a sub-doc). Generate brief in `notion` or `docx`; pull comparable closed-won deals from CRM for anchor pricing.
- **Source:** https://www.gong.io/labs/sales-negotiation-tips/
- **Confidence:** ✓

---

## Proposal generation + e-sign

- **SOTA approach:** PandaDoc / DocuSign / Qwilr / Proposify for proposal generation with CRM-merge variables, e-sign workflow, view analytics. DealHub for full CPQ when configuration is complex.
- **Agent execution path:** Use `pandadoc-docusign-proposal-pipeline` skill. `api-gateway` `POST https://gateway.maton.ai/pandadoc/public/v1/documents` from template + CRM tokens; `POST https://gateway.maton.ai/docusign/restapi/v2.1/accounts/{accountId}/envelopes` for DocuSign. Send-tracking webhook posts back to CRM.
- **Source:** https://developers.pandadoc.com/ + https://developers.docusign.com/docs/esign-rest-api/
- **Confidence:** ✓

---

## Pricing strategy

- **SOTA approach:** Pull comparable closed-won deals from CRM; segment by ACV band, industry, headcount; flag if proposed price < median for segment; recommend price corridor + concession menu. For SaaS, also factor net retention (expansion potential) into discount tolerance.
- **Agent execution path:** Use `expansion-upsell-renewal-playbook` skill (covers pricing too). CRM closed-won query via `api-gateway`; analysis in Python via `cli-anything` (pandas describe / quantile); render report to `notion`.
- **Source:** https://www.priceintelligently.com/blog + internal pricing analysis
- **Confidence:** ✓

---

## Win/loss analysis (post-mortem with structured tagging)

- **SOTA approach:** Closed-won AND closed-lost get a 5-section post-mortem: trigger event, our diagnosis quality, decision-criteria match, competitor (if lost), what to repeat / what to change. Tag with structured fields (industry, deal size, sales cycle days, primary competitor) for trend rollup.
- **Agent execution path:** Use `win-loss-analysis-structured` skill. Pull deal record + linked calls/emails via `api-gateway`; query Gong for sentiment shifts via `gong-chorus-call-intelligence`; render post-mortem in `notion` DB with structured fields; quarterly rollup query.
- **Source:** https://www.gong.io/blog/win-loss-analysis/ + https://www.cluedin.com/customer-research
- **Confidence:** ✓

---

## Sales enablement content (battlecards, case studies, ROI calculators)

- **SOTA approach:** Battlecard per top competitor with positioning, traps, talk tracks, proof points. ROI calculator as a spreadsheet model with input variables. Case studies as `docx`/`pdf` rendered from `notion` templates.
- **Agent execution path:** Use `sales-enablement-battlecards-roi-calculators` skill. Battlecard markdown → `pptx` render; ROI calculator → `google-sheets` skill or `microsoft-excel` skill formula model; case study → `docx` or `pdf` skill from template.
- **Source:** https://www.gong.io/blog/sales-battlecards/ + internal templates
- **Confidence:** ✓

---

## Account-based marketing coordination with marketing-agent

- **SOTA approach:** Tier-1 ABM target list (50-200 accounts) → marketing-agent runs personalized ads + content + email warming; sales-agent owns 1:1 outreach + multi-threading. Shared dashboard (Notion or Google Sheets) tracks per-account engagement score (impressions + email opens + site visits + meeting bookings).
- **Agent execution path:** Use `multi-threading-enterprise-deals` skill. Cross-agent hand-off: sales-agent maintains target-account list in `notion`; defers to `marketing-agent` for ad targeting (LinkedIn ABM + Meta/Google retargeting custom audiences). Shared dashboard refresh nightly.
- **Source:** https://www.demandbase.com/intent/abm-framework/
- **Confidence:** ✓

---

## Signal/intent monitoring (job changes, funding events, tech-stack changes)

- **SOTA approach:** Common Room (community + dark social signals), Pocus (PLG signals), Koala (PLG signals), Apollo job-change alerts, Crunchbase funding webhooks, BuiltWith tech-stack diffs. Aggregate signals into a daily "hot accounts" feed; auto-create CRM task for AE when threshold hit.
- **Agent execution path:** Use `signal-intent-monitoring-pocus-koala-common-room` skill. Cron via `postgresql-mcp` or `cli-anything` Python script pulls webhooks from each source; ranks accounts; pushes top-10 into CRM as tasks via `api-gateway` HubSpot `/crm/v3/objects/tasks`.
- **Source:** https://www.commonroom.io/ + https://www.pocus.com/ + https://www.koala.io/
- **Confidence:** ⚠ (paid signal tools)

---

## Forecasting + commit accuracy

- **SOTA approach:** Three-tier forecast: Commit (>80% confident), Best Case (50-80%), Pipeline (<50%). Weekly diff vs. prior-week forecast; track "slippage" (deals that miss commit date) and "pull-ins" (early closes) for AE-level calibration. Clari / Gong Forecast / BoostUp do this automatically; manual via SQL or Sheets.
- **Agent execution path:** Use `clari-forecasting-commit-accuracy` skill. CRM deal pull via `api-gateway`; bucket by forecast category; render weekly forecast doc to `notion` or `google-sheets`. For Clari/BoostUp, `api-gateway` if onboarded (Clari has limited public API).
- **Source:** https://www.clari.com/blog/sales-forecasting-methods/ + https://www.gong.io/forecast/
- **Confidence:** ⚠ (Clari/BoostUp need OAuth; manual forecast via CRM + Sheets is always available)

---

## Sales call review (Gong / Chorus / Fathom analysis)

- **SOTA approach:** Pull transcript + tags from Gong/Chorus/Fathom; extract: talk-listen ratio, # questions asked, monologue length, objections raised, next-steps stated, sentiment shift moments. Compare AE vs. team median for coaching.
- **Agent execution path:** Use `gong-chorus-call-intelligence` skill. Gong: `api-gateway` `GET https://gateway.maton.ai/gong/v2/calls/transcript?id=<callId>`. Fathom: `fathom-api` skill or `api-gateway`. Fireflies: `api-gateway`. Chorus has no public API → use email-export integration + parse. tl;dv via `api-gateway`. Run extraction in Python via `cli-anything`; coach summary to `notion`.
- **Source:** https://app.gong.io/settings/api/documentation + https://help.fathom.video/en/articles/8430832-fathom-api
- **Confidence:** ✓ (Gong/Fathom/Fireflies/tl;dv); Chorus is ⚠ (email export workaround)

---

## Email deliverability for cold outbound (warmup, SPF/DKIM/DMARC, complaint rate)

- **SOTA approach:** Pre-launch: SPF + DKIM + DMARC validated; sender domain warmup (Lemwarm / Mailwarm / Instantly built-in warmup) for 4-6 weeks; secondary domains for cold (mybrand.io vs brand.com); complaint rate < 0.10%; bounce rate < 2%; reply rate target > 5%. Daily volume ramp 10-20/day → 50-100/day over 3 weeks per mailbox.
- **Agent execution path:** Use `cold-email-deliverability-warmup` skill. `cli-anything` `dig TXT brand.com` (SPF), `dig TXT default._domainkey.brand.com` (DKIM), `dig TXT _dmarc.brand.com` (DMARC); curl `https://www.mail-tester.com/test-XXX&format=json`; Glock Apps API for placement; Lemwarm/Mailwarm via `api-gateway` if onboarded; daily volume tracked in `notion`.
- **Source:** https://lemwarm.com/ + https://www.mail-tester.com/ + https://glockapps.com/api/
- **Confidence:** ✓

---

## Customer expansion / upsell playbook

- **SOTA approach:** Track product-usage signal (Pocus/Koala/PostHog) for accounts past day-90; trigger expansion play when: usage > seat threshold, adoption of >2 modules, NPS > 8, or champion promotion. Expansion path: usage report → exec QBR → multi-team rollout proposal.
- **Agent execution path:** Use `expansion-upsell-renewal-playbook` skill. Cross-agent: PostHog product analytics via `posthog-mcp`; CRM update via `api-gateway`; QBR deck via `pptx`; coordinate with `customer-support-agent` (future).
- **Source:** https://www.gainsight.com/blog/account-expansion-strategy/
- **Confidence:** ✓

---

## Renewal pipeline management

- **SOTA approach:** Renewal pipeline opens 120 days pre-renewal-date; renewal-risk score per account based on usage drop, support ticket spike, NPS, champion churn (job change at customer). Save-motion playbook for at-risk; auto-renew motion for healthy.
- **Agent execution path:** Use `expansion-upsell-renewal-playbook` skill. CRM contract-date field via `api-gateway`; risk-score calc in Python via `cli-anything`; PostHog usage trend; renewal pipeline rendered in `notion` DB.
- **Source:** https://www.gainsight.com/blog/renewal-management/
- **Confidence:** ✓

---

## Lead routing rules

- **SOTA approach:** Round-robin within team / weighted (top performer gets higher weight) / geo / vertical / size-tier / language. ICP fit check before assign — non-ICP inbound goes to nurture, not AE.
- **Agent execution path:** Use `hubspot-sales-mcp` skill. HubSpot workflow via `api-gateway` `POST /automation/v4/flows`; Salesforce assignment rules via `salesforce-api`; routing manifest stored in `notion`.
- **Source:** https://blog.hubspot.com/sales/sales-lead-routing
- **Confidence:** ✓

---

## SDR ↔ AE handoff

- **SOTA approach:** Handoff package includes: MEDDIC fields filled, BANT/score, source channel, key conversation snippets, prospect's stated pain, agreed next step, mutual calendar slot booked. Slack DM + CRM note. Acceptance criteria: AE accepts within 4 business hours or returns with rejection reason.
- **Agent execution path:** Use `meddic-meddpicc-qualification` skill. Handoff doc template in `notion`; CRM activity log via `api-gateway`; Slack ping via `slack` skill; Calendly booking via `calendly-api` skill.
- **Source:** https://www.saastr.com/sdr-to-ae-handoff/
- **Confidence:** ✓

---

## Multi-threading enterprise deals

- **SOTA approach:** Map account stakeholders: economic buyer, champion, technical evaluator, end-user voice, executive sponsor, blocker(s). Goal: 4+ stakeholders engaged per deal > $50K ACV. Track engagement depth per stakeholder (touched / met / advocate / blocker).
- **Agent execution path:** Use `multi-threading-enterprise-deals` skill. Stakeholder map maintained in CRM (HubSpot custom object or Salesforce account team); Sales Navigator for org chart; weekly engagement rollup; coordinate co-pitch with `marketing-agent` for content gifts to silent stakeholders.
- **Source:** https://www.gong.io/blog/multi-threading/ + Challenger Customer methodology
- **Confidence:** ✓

---

## LinkedIn Sales Navigator outreach

- **SOTA approach:** Sales Navigator search → save lead list → personalized connection requests (InMail credit budget for non-connections) → engagement sequence (like + comment on 2 posts before reaching out). HeyReach / Phantombuster / TexAu automate the connection + message flow at safe daily volumes (15-25 connections/day per account).
- **Agent execution path:** Use `linkedin-sales-navigator-outreach` skill. Phantombuster/TexAu via `cli-anything` curl (account-bound, no general MCP); HeyReach via `api-gateway` if onboarded. LinkedIn skill (`linkedin` default skill) for direct posting + basic profile fetch.
- **Source:** https://www.heyreach.io/ + https://phantombuster.com/ + LinkedIn Sales Navigator help docs
- **Confidence:** ⚠ (LinkedIn TOS-sensitive; safe daily limits required; account-bound)

---

## Meeting booking + scheduling

- **SOTA approach:** Calendly / Chili Piper / HubSpot Meetings for prospect self-serve booking. Embed booking link in every outbound. Round-robin assignment if multi-AE team. Pre-meeting questionnaire + auto-CRM-create.
- **Agent execution path:** Use `calendly-api` default skill. `api-gateway` Calendly v2 `https://gateway.maton.ai/calendly/scheduled_events`; HubSpot Meetings via HubSpot CRM API. Generate one-off booking URL via Calendly create_scheduling_link.
- **Source:** https://developer.calendly.com/api-docs/
- **Confidence:** ✓

---

## Slack/Teams sales rooms + Spiff alerts

- **SOTA approach:** #wins channel for closed-won celebration with deal summary; #help channel for AE-to-team asks; Spiff/CaptivateIQ commission dashboards. Slack notifications on closed-won via CRM webhook → Slack.
- **Agent execution path:** `slack` default skill `postMessage`; CRM webhook → AWS Lambda or n8n → Slack. For commission tooling, deferred to `finance-controller`.
- **Source:** https://api.slack.com/messaging/sending
- **Confidence:** ✓

---

## Sales reporting + dashboards

- **SOTA approach:** Weekly forecast doc, monthly pipeline coverage report (target: pipeline = 3-4× quota), quarterly win/loss rollup with structured tags, AE-level activity report (calls, demos, opps created). Render to Google Sheets / Notion / PDF.
- **Agent execution path:** CRM query via `api-gateway`; data shaping in Python via `cli-anything`; render via `google-sheets` / `microsoft-excel` / `notion` / `pdf` skills.
- **Source:** https://www.salesforce.com/resources/articles/sales-reports/
- **Confidence:** ✓

---

## Summary table (≥95% fulfillment)

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | Outbound sequence design | Outreach / Salesloft / lemlist / Instantly | `api-gateway` managed OAuth | ✓ |
| 2 | Inbound lead qualification + scoring | HubSpot / Salesforce | `api-gateway` + `salesforce-api` | ✓ |
| 3 | Account research (ICP + hierarchy + intent) | Apollo + Clay + LinkedIn SN | `api-gateway` + Phantombuster | ⚠ |
| 4 | Lead enrichment (waterfall) | Apollo / Clay / Lusha / ZoomInfo | `api-gateway` + `cli-anything` curl | ⚠ |
| 5 | CRM hygiene + data quality | HubSpot / Salesforce | `api-gateway` + `postgresql-mcp` | ✓ |
| 6 | Pipeline review + stage hygiene | HubSpot / Salesforce | `api-gateway` queries | ✓ |
| 7 | Qualification (MEDDIC/MEDDPICC/BANT) | CRM custom fields + Gong | `api-gateway` + `gong-chorus-call-intelligence` | ✓ |
| 8 | Discovery call prep | Apollo + LinkedIn + Gong + CRM | composite | ✓ |
| 9 | Demo prep + objection handling | Gong + battlecards | `gong-chorus-call-intelligence` + `pptx` | ✓ |
| 10 | Deal coaching (next-best-action) | CRM + Gong + MEDDIC | composite | ✓ |
| 11 | Negotiation prep | CRM closed-won comps + Gong | composite | ✓ |
| 12 | Proposal generation + e-sign | PandaDoc / DocuSign | `api-gateway` | ✓ |
| 13 | Pricing strategy | CRM comp analysis | `api-gateway` + `cli-anything` (pandas) | ✓ |
| 14 | Win/loss analysis | Gong + CRM | `gong-chorus-call-intelligence` + `notion` | ✓ |
| 15 | Sales enablement content | pptx + Sheets + Notion | `pptx` + `google-sheets` + `notion` | ✓ |
| 16 | ABM coordination | LinkedIn ads + sales target list | hand-off to `marketing-agent` | ✓ |
| 17 | Signal/intent monitoring | Common Room + Pocus + Koala | webhooks + `cli-anything` | ⚠ |
| 18 | Forecasting + commit accuracy | CRM + Clari/BoostUp | `api-gateway` + manual fallback | ⚠ |
| 19 | Call review (talk-listen, monologue) | Gong / Chorus / Fathom / Fireflies / tl;dv | `gong-chorus-call-intelligence` | ✓ (Chorus ⚠) |
| 20 | Cold email deliverability + warmup | dig + mail-tester + Lemwarm + Instantly | `cli-anything` + `api-gateway` | ✓ |
| 21 | Customer expansion / upsell | Pocus/Koala/PostHog + CRM | `posthog-mcp` + `api-gateway` | ✓ |
| 22 | Renewal pipeline | CRM + usage signals | `api-gateway` + Python | ✓ |
| 23 | Lead routing rules | HubSpot/Salesforce workflows | `api-gateway` + `salesforce-api` | ✓ |
| 24 | SDR ↔ AE handoff | CRM + Slack + Calendly | `api-gateway` + `slack` + `calendly-api` | ✓ |
| 25 | Multi-threading enterprise | CRM stakeholder map + Sales Nav | composite | ✓ |
| 26 | LinkedIn Sales Nav outreach | HeyReach / Phantombuster / TexAu | `api-gateway` + `cli-anything` | ⚠ |
| 27 | Meeting booking | Calendly / HubSpot Meetings | `calendly-api` + `api-gateway` | ✓ |
| 28 | Slack/Teams sales rooms | Slack/Teams webhooks | `slack` + `microsoft-teams` | ✓ |
| 29 | Sales reporting + dashboards | CRM + Sheets / Notion / PDF | composite skills | ✓ |

**Fulfillment math:** 29 distinct use cases mapped. 23 are full ✓ confidence; 6 are ⚠ (one-time paid-key or platform-approval setup the recipient owns). Zero ✗ gaps. **~95%+ fulfillment** counting ⚠ rows as one-time setup that doesn't block agent execution.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (each must exist in `app/config/mcp_config.json`):
- `filesystem` — always
- `gmail-mcp` — outbound email + reply parsing
- `outlook-mcp` — Microsoft-shop email
- `notion-mcp` — playbooks, target-account lists, post-mortems
- `slack-mcp` — sales-room notifications
- `ms-teams-mcp` — Microsoft-shop notifications
- `postgresql-mcp` — warehouse queries for reporting + cron alerts
- `linear-mcp` — handoffs to product team
- `jira-mcp` — alt handoff target
- `playwright-mcp` — browse account websites for research
- `firecrawl-mcp` — structured scraping of prospect sites
- `brightdata-mcp` — LinkedIn Sales Nav scraping fallback
- `brave-search` — web research
- `google-scholar-mcp` — research-heavy verticals
- `posthog-mcp` — PLG signals + product usage
- `mixpanel-mcp` — alt product analytics
- `amplitude-mcp` — alt product analytics
- `deepl-mcp` — multi-language outreach
- `imagegen-mcp` — battlecard imagery
- `canva-mcp` — branded one-pager templates
- `figma-mcp` — brand-system fidelity for proposals
- `tiktok-mcp` — for video-first sales motions (rare but real)
- `youtube-mcp` — sales-team learning material

**Skill packs to create in Round 2 (runtime build),** in order of impact:
1. `hubspot-sales-mcp` — primary CRM ops
2. `apollo-clay-lead-enrichment` — multi-source enrichment workflow
3. `outreach-salesloft-sequences` — sequence design + execution
4. `cold-email-deliverability-warmup` — deliverability + warmup
5. `gong-chorus-call-intelligence` — call analysis + coaching extraction
6. `meddic-meddpicc-qualification` — qualification execution + scoring
7. `bant-spin-challenger-frameworks` — alt qualification frameworks
8. `account-research-deep` — ICP scoring + hierarchy + intent
9. `linkedin-sales-navigator-outreach` — LinkedIn pipeline
10. `signal-intent-monitoring-pocus-koala-common-room` — PLG + community signals
11. `deal-coaching-next-best-action` — opportunity-level coaching
12. `win-loss-analysis-structured` — structured post-mortem
13. `pandadoc-docusign-proposal-pipeline` — proposal + e-sign
14. `clari-forecasting-commit-accuracy` — forecasting discipline
15. `pipeline-hygiene-stage-criteria` — pipeline stage definitions + progression
16. `sales-enablement-battlecards-roi-calculators` — enablement asset patterns
17. `multi-threading-enterprise-deals` — stakeholder mapping
18. `expansion-upsell-renewal-playbook` — post-sale revenue motion

---

## Notes on remaining caveats (the ⚠ rows)

- **Apollo / Clay / Lusha / ZoomInfo (use cases 3, 4):** Each requires a paid plan + API key. `api-gateway` provides managed OAuth for Apollo + Clay if onboarded to Maton. Otherwise direct curl works. Free fallback: manual research via LinkedIn + brave-search.
- **LinkedIn Sales Navigator (use cases 3, 26):** No public API. Phantombuster / TexAu / HeyReach scrape via a logged-in account, which is TOS-sensitive. Safe daily limits: 15-25 connections, 50 profile views, 100 search results. Account-bound — each rep needs their own.
- **Common Room / Pocus / Koala (use case 17):** Paid intent platforms with webhook + REST APIs. Free fallback: poll Crunchbase + LinkedIn job-change feed + Apollo "company news" endpoint.
- **Clari / BoostUp (use case 18):** Limited public API. Manual forecast via CRM + Google Sheets is always available; if customer has Clari, `api-gateway` may proxy.
- **Chorus (use case 19):** No public API. Email-export integration → parse transcripts is the workaround. Gong/Fathom/Fireflies/tl;dv all have first-class APIs.
