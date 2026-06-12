# Sales Operations — Use Cases

**Tier:** **specialized** · **Category:** sales (sub-tier under `sales-agent`)
**Core job:** Run the systems beneath the selling motion — CRM admin (Salesforce / HubSpot fields, validation, flows, approvals), commission plan administration + dispute resolution (Spiff / QuotaPath / CaptivateIQ), CPQ configuration (Salesforce CPQ / Conga / DealHub), lead routing (LeanData / Chili Piper), duplicate management, data enrichment orchestration, pipeline metrics + reporting, territory planning, sales tech stack admin (Salesloft / Outreach / Gong), deal desk operations, forecasting accuracy (Clari / BoostUp / Aviso), rep performance dashboards (CRMA / Looker / Sigma / Hex), stalled deal alerts, ramp-to-quota analysis, contact-account hierarchy maintenance, win/loss reporting at scale, sales enablement infrastructure (Highspot / Showpad / Seismic), sales tech stack consolidation audits.

> Ships with the SOTA 2026 SalesOps stack (Salesforce + HubSpot Operations Hub admin, Spiff/QuotaPath/CaptivateIQ commission, Salesforce CPQ + Conga + DealHub, LeanData + Chili Piper routing, ZoomInfo + Apollo + Clay enrichment, Clari + BoostUp + Aviso forecasting, Highspot + Showpad + Seismic enablement, Salesforce CRMA + Looker + Sigma + Hex dashboards, SFDX CLI for admin deploys, dbt + warehouse for pipeline metrics) — executes end-to-end, not just direct.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### CRM admin (Salesforce / HubSpot / Pipedrive / Dynamics / Attio / Zoho)
- Custom fields + custom objects + record types + page layouts
- Validation rules (stage criteria enforcement, required field gating, discount threshold gating)
- Lightning Flows (record-triggered, scheduled, screen flows) + HubSpot Workflows
- Approval Processes (discount tiers, exception management)
- Formulas + roll-up summaries
- Apex deploys (admin scope only — light triggers + helper classes via SFDX)
- Schema audit + unused-field cleanup
- Lead-to-opportunity conversion hygiene (required-field enforcement on convert)

### Commission plan administration
- Commission plan modeling (Spiff / QuotaPath / CaptivateIQ / Performio / Xactly / Everstage)
- Plan logic: base rate, accelerators, SPIFs, clawbacks, draws, ramp tiers
- Plan publishing + monthly statement generation
- Pre/post comp delta analysis when plans change
- Commission dispute resolution with audit-trail PDFs (5-day SLA)
- Audit-trail integrity (every payment reconstructable from source CRM deal data)

### CPQ + revenue
- Salesforce CPQ (Steelbrick) pricing rules + product bundles + approval rules
- Conga CPQ (Apttus-derived) admin
- DealHub CPQ admin + deal-desk module
- Pricing logic: tiered, volume, geo, channel-partner, multi-year ramp, bundle discount
- Quote-to-cash chain configuration (CPQ → e-sign → order → billing via Stripe)
- Approval threshold management (discount tier matrix)

### Lead routing + book-of-business
- LeanData (Salesforce-native) routing + match + book
- Chili Piper inbound calendar router (form-to-meeting)
- Distribute (HubSpot-focused)
- Routing logic: round-robin, geo, vertical, ABM-tier, named-account, AE territory, SDR pod
- Routing testing (10 synthetic leads per route before deploy)
- Routing accuracy tracking (correct vs. mis-routed)

### Duplicate management
- LeanData Dedup (Salesforce-native)
- Cloudingo (Salesforce-native, mature fuzzy match)
- DupeBlocker (Validity)
- Native HubSpot dedup
- Custom Python fuzzy match via `cli-anything` (rapidfuzz) when paid tool absent
- Auto-merge above high-confidence threshold; human-review queue for low-confidence
- Twin-as-one false positive monitoring

### Data enrichment orchestration
- Apollo (cost-efficient B2B baseline)
- ZoomInfo (gaps + Scoops intent)
- Clay (workflow orchestration across 100+ sources)
- Demandbase (ABM intent overlay)
- Waterfall source order configuration
- Trigger-based enrichment (on lead create / on stage change / quarterly refresh)
- Spend cap per record + source-quality compare (which source's data leads to closed-won)

### Pipeline metrics + reporting
- Velocity (Sales Velocity formula: Win × Deals × Value / Cycle days)
- Stage-to-stage conversion %
- Deal age in stage + stale-deal detection
- Win rate
- Pipeline coverage ratio (3-4× quarterly quota target)
- Pipeline-to-revenue ratio

### Pipeline-stage definitions + criteria-based progression
- Entry + exit criteria per stage documented
- Validation rule enforcement (Salesforce) or Workflow condition (HubSpot)
- Stage criteria reference doc in `notion` with one source of truth per metric

### Territory planning + assignment
- Salesforce Territory Management 2.0 (native)
- Anaplan sales planning (enterprise scenario modeling)
- Fullcast (mid-market)
- K-means territory clustering via `cli-anything` (sklearn) for custom design
- Account-to-territory assignment + balance check (similar TAM + similar account count per territory)

### Forecasting accuracy
- Clari Align (revenue-team alignment)
- BoostUp (mid-market)
- Aviso (AI-driven)
- Gong Forecast (call-data-integrated)
- Three-bucket discipline (Commit / Best Case / Pipeline) — manual fallback via CRM + Sheets
- Commit accuracy tracking per AE per quarter
- Slippage + pull-in pattern detection
- Forecast snapshot diff weekly (Slack digest to manager)

### Sales enablement infrastructure
- Highspot (content + spots + analytics)
- Showpad (asset + tag taxonomy + analytics)
- Seismic (LiveDoc + enterprise content)
- Mindtickle / Lessonly (training + LMS)
- Tag taxonomy maintenance (stage, persona, industry, competitor, format)
- Orphan content quarantine

### Deal desk operations
- Discount tier approval routing (Tier 1: < 10% / Tier 2: 10-20% / Tier 3: 20-30% / Tier 4: > 30%)
- SLA tracking (24h / 48h / 72h / 96h escalation)
- Exception management with reason code logging
- Quote acceptance SLA dashboard

### Rep performance dashboards
- Salesforce CRMA / Einstein Analytics / Tableau CRM dataset + dashboard deploys
- Looker LookML models + dashboards
- Sigma + Hex (warehouse-native dashboards)
- HubSpot Reports
- Per-AE metrics: pipeline created, demos run, opps advanced, win rate, average deal size, cycle median, commit accuracy
- Per-SDR metrics: outbound activity, SQL conversion, SDR-to-AE acceptance, demo conversion

### Sales attainment dashboards
- Per-AE quota attainment (closed-won $ ÷ quota $) tracked weekly
- Per-team rollup
- Color-coded (green > 90%, yellow 70-90%, red < 70%)
- Year-over-year compare + cohort by tenure

### Stalled-deal alerts + engagement signals
- Stale-deal detection (in-stage > 1.5× median + no logged activity in 14+ days)
- Engagement signals (email opens, call recency, calendar engagement, Gong sentiment shift)
- Slack alert with recommended NBA (hand-off from `sales-agent`)
- Aging report weekly

### Ramp-to-quota analysis
- New-hire cohort tracking (hire month + experience tier)
- Time-to-first-closed-won
- Monthly attainment % from start date
- Training completion correlation (Mindtickle / Lessonly data)
- Median ramp curve per cohort

### Contact-account hierarchy maintenance
- Salesforce Account Hierarchy (parent-child-sibling)
- LeanData BookBuilder
- D&B Direct+ refresh (M&A, divestitures, subsidiary mapping)
- HubSpot Company hierarchy via associations API

### Win/loss reporting at scale
- Quarterly + annual rollup with structured tags (industry, deal size, sales cycle, primary competitor, lost reason)
- Drift detection (competitor mention rate change, cycle-time bloat, lost-reason shift)
- Trend dashboard + executive summary

### Sales tech stack consolidation
- Per-tool utilization scoring (active users / licensed; cost per active user)
- < 30% utilization flagged for kill or renegotiate
- Overlap detection (Apollo + ZoomInfo + Cognism, e.g.) → consolidate to one + fallback
- Renewal renegotiation playbook (60 days pre-renewal)
- Annual stack review cadence

### Salesforce CRMA dashboard ops
- Dataset deploy via `sf wave dataset deploy`
- Dashboard create + edit
- External data source ingestion (Snowflake, BigQuery, dbt)
- Embed in Lightning home pages
- Predictive Einstein Discovery setup

### Cross-functional ops handoffs
- Sales engineering (technical demo support) — handoff to `senior-python-engineer` or future `solutions-engineer`
- Commission GL + revenue recognition — handoff to `finance-controller`
- Lead source quality (ad targeting, content quality, MQL→SQL conversion at top of funnel) — handoff to `marketing-agent`
- Deep predictive analytics (cohort survival, attribution modeling, propensity scoring) — handoff to `data-analyst`
- Customer health + renewal authoring — handoff to future `customer-success` agent (use `customer-support-agent` as stand-in)

---

## Execution status (SOTA — June 2026)

The 2026 SOTA SalesOps stack closes the historic "can advise on systems, can't deploy them" gap. Salesforce admin via SFDX CLI + Metadata + Tooling APIs; HubSpot Operations Hub workflows + custom-coded actions + data sync via `api-gateway`; commission tooling (Spiff / QuotaPath / CaptivateIQ) via `api-gateway` managed OAuth; CPQ (Salesforce CPQ via `salesforce-api`; Conga + DealHub via `api-gateway`); lead routing (LeanData via Salesforce-native + Chili Piper via `api-gateway`); enrichment waterfall (Apollo + ZoomInfo + Clay + Demandbase via `api-gateway`); forecasting (Clari + BoostUp + Aviso via `api-gateway`, manual fallback via CRM + Sheets); enablement (Highspot + Showpad + Seismic via `api-gateway`); dashboards (Salesforce CRMA via SFDX wave commands; Looker + Sigma + Hex via `api-gateway`; warehouse via `postgresql-mcp` + dbt).

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Salesforce admin (fields, validation, flows) | Salesforce Metadata + Tooling + SFDX CLI | `cli-anything` + `salesforce-api` + `api-gateway` (`salesforce-admin-custom-fields-flows` skill) |
| HubSpot Operations Hub workflows | HubSpot Ops Hub | `api-gateway` (`hubspot-ops-hub-workflows` skill) |
| HubSpot custom-coded actions | HubSpot Ops Hub Pro | `api-gateway` (`hubspot-ops-hub-workflows` skill) |
| HubSpot data sync mapping | HubSpot Data Sync (PieSync successor) | `api-gateway` (`hubspot-ops-hub-workflows` skill) |
| Salesloft + Outreach + Gong admin | Salesloft + Outreach + Gong Admin APIs | `api-gateway` (`salesloft-outreach-tech-stack-admin` skill) |
| Apollo + Clay admin (enrichment ops) | Apollo + Clay admin APIs | `api-gateway` (`salesloft-outreach-tech-stack-admin` skill) |
| Commission plan administration | Spiff + QuotaPath + CaptivateIQ + Performio + Xactly | `api-gateway` (`commission-spiff-quotapath-captivateiq` skill) |
| Commission dispute resolution + audit trail | Spiff + CaptivateIQ + QuotaPath dispute APIs + audit-log queries | `api-gateway` + `salesforce-api` + `pdf` (`commission-dispute-audit-trail` skill) |
| Salesforce CPQ configuration | Salesforce CPQ (Steelbrick) | `salesforce-api` + SFDX (`salesforce-cpq-conga-dealhub` skill) |
| Conga CPQ + DealHub CPQ | Conga + DealHub | `api-gateway` (`salesforce-cpq-conga-dealhub` skill) |
| Quote-to-cash configuration | CPQ → e-sign → order → Stripe billing | composite skills + `stripe-mcp` |
| Lead routing (LeanData) | LeanData (Salesforce-native) | `salesforce-api` (`lead-routing-leandata-chili-piper` skill) |
| Lead routing (Chili Piper) | Chili Piper router config | `api-gateway` (`lead-routing-leandata-chili-piper` skill) |
| Lead routing (Distribute / native Salesforce assignment) | Distribute + Salesforce Assignment Rules | `api-gateway` + `salesforce-api` |
| Duplicate management (LeanData Dedup) | LeanData Dedup (Salesforce-native) | `salesforce-api` (`duplicate-mgmt-leandata-dedupe` skill) |
| Duplicate management (Cloudingo / DupeBlocker) | Cloudingo + DupeBlocker (Validity) | `api-gateway` (`duplicate-mgmt-leandata-dedupe` skill) |
| Duplicate management (native + custom fuzzy) | HubSpot built-in + Python rapidfuzz fallback | `cli-anything` + `api-gateway` |
| Data enrichment waterfall | Apollo → ZoomInfo → Clay → Demandbase | `api-gateway` (`data-enrichment-zoominfo-apollo-clay` skill) |
| Pipeline metrics (velocity, conversion, age) | Salesforce CRMA + HubSpot Reports + warehouse + dbt | `api-gateway` + `postgresql-mcp` (`pipeline-metrics-velocity-conversion` skill) |
| Pipeline-stage criteria + enforcement | Salesforce validation rules + HubSpot Workflow conditions | `salesforce-api` + `api-gateway` (`pipeline-metrics-velocity-conversion` skill) |
| Territory planning (Salesforce TM2) | Salesforce Territory Management 2.0 | `salesforce-api` (`territory-planning-assignment` skill) |
| Territory planning (Anaplan / Fullcast) | Anaplan + Fullcast | `api-gateway` (`territory-planning-assignment` skill) |
| K-means territory clustering | sklearn-based custom design | `cli-anything` (`territory-planning-assignment` skill) |
| Forecasting (Clari / BoostUp / Aviso) | Clari + BoostUp + Aviso | `api-gateway` (`forecasting-clari-boostup-aviso` skill) |
| Forecasting (manual three-bucket fallback) | CRM + Sheets | `salesforce-api` + `cli-anything` + `google-sheets` (`forecasting-clari-boostup-aviso` skill) |
| Commit accuracy tracking | CRM forecast snapshots + AE rollup | `cli-anything` + `salesforce-api` (`forecasting-clari-boostup-aviso` skill) |
| Sales enablement (Highspot / Showpad / Seismic) | Highspot + Showpad + Seismic + Mindtickle | `api-gateway` (`sales-enablement-infrastructure-highspot-showpad` skill) |
| Deal desk discount approval | Salesforce Approval Process + HubSpot Approvals + DealHub deal-desk | `salesforce-api` + `api-gateway` (`deal-desk-discount-approval` skill) |
| Rep performance dashboards (Salesforce CRMA) | Salesforce CRMA via SFDX wave commands | `cli-anything` + `salesforce-api` (`rep-performance-dashboards` skill) |
| Rep performance dashboards (Looker / Sigma / Hex) | Looker + Sigma + Hex | `api-gateway` + `postgresql-mcp` (`rep-performance-dashboards` skill) |
| Sales attainment dashboards (quota %) | CRM + quota source (Anaplan / Notion) | `api-gateway` + `cli-anything` + `google-sheets` (`rep-performance-dashboards` skill) |
| Stalled-deal alerts + engagement signals | CRM stale-deal query + Gong sentiment + Slack alert | `salesforce-api` + `api-gateway` + `slack-mcp` (`stalled-deal-alerts-engagement-signals` skill) |
| Ramp-to-quota analysis | CRM cohort + Mindtickle / Lessonly training data | `salesforce-api` + `cli-anything` + `api-gateway` (`ramp-to-quota-analysis` skill) |
| Contact-account hierarchy maintenance | Salesforce Account Hierarchy + LeanData BookBuilder + D&B Direct+ | `salesforce-api` + `api-gateway` (`contact-account-hierarchy-maintenance` skill) |
| Win/loss reporting at scale | CRM rollup + Gong sentiment + tag pivot + drift detection | `salesforce-api` + `cli-anything` + `microsoft-excel` (`win-loss-reporting-at-scale` skill) |
| Sales tech stack consolidation audit | Tool admin APIs (last-login + utilization) | `api-gateway` + `cli-anything` (`sales-tech-stack-consolidation-audit` skill) |
| Schema audit (unused custom fields) | Salesforce Tooling API + HubSpot Properties API | `cli-anything` + `salesforce-api` + `api-gateway` (`salesforce-admin-custom-fields-flows` skill) |
| Lead-to-opportunity conversion hygiene | Salesforce LeadConvert + HubSpot workflows | `salesforce-api` + `api-gateway` |
| Salesforce CRMA dataset + dashboard deploy | Salesforce CRMA REST + SFDX wave commands | `cli-anything` + `salesforce-api` + `api-gateway` (`rep-performance-dashboards` skill) |

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Spiff / QuotaPath / CaptivateIQ | ⚠ | Paid ICM platforms; `api-gateway` proxies when Maton-onboarded; free fallback: build commission model in `google-sheets` / `microsoft-excel` from CRM closed-won — works up to ~30 reps before maintenance burden warrants paid tool |
| Salesforce CPQ / Conga CPQ / DealHub CPQ | ⚠ | Each is a paid add-on / separate subscription; `salesforce-api` reads CPQ objects natively if installed; fallback: `google-sheets` quote calculator + `pdf` quote template |
| ZoomInfo / Apollo / Clay / Demandbase | ⚠ | Paid API keys; `api-gateway` proxies Apollo + Clay when Maton-onboarded; free fallback: manual research via LinkedIn + `brave-search` |
| Cloudingo / DupeBlocker / LeanData Dedup | ⚠ | Paid Salesforce dedup tools; free fallback: HubSpot built-in dedup + Salesforce native Duplicate Rules + custom Python rapidfuzz via `cli-anything` |
| Clari / BoostUp / Aviso | ⚠ | Paid forecasting platforms with limited public API; manual three-bucket forecasting via CRM + Sheets is always available; covers methodology, not predictive ML layer |
| Highspot / Showpad / Seismic | ⚠ | Paid enablement platforms; free fallback: content infrastructure in `notion` + `google-drive` with tagged folder structure; lacks per-asset tracking + per-AE analytics |
| Apex trigger / Lightning Web Component dev | ⚠ | This agent handles admin-scope Apex (light helper triggers + validation logic); for full LWC + Apex development hand off to `senior-python-engineer` or specialist Salesforce dev agent (future) |
| Real-time dispute UX (chat-style) | ⚠ | Disputes resolved async with PDF audit trail; for chat-style real-time resolution UX, build a custom in-Salesforce screen flow via `salesforce-admin-custom-fields-flows` |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a concrete execution path. The historic "advise, don't deploy" gaps are closed via SFDX CLI for Salesforce admin, `api-gateway` managed OAuth for SaaS tools, and dedicated default skills (`salesforce-api`, `pipedrive-api`, `attio-api`, etc.). The remaining 5% is paywalled ICM / CPQ / enrichment / forecasting / enablement tooling (recipient's own key) — the methodology runs via CRM-native + `cli-anything` fallback when the paid tool isn't onboarded.

---

## When to use this agent

- "Deploy a validation rule blocking Discovery → Evaluation advance without Champion populated"
- "Audit our Salesforce schema and tell me which custom fields are unused"
- "Model a new commission plan with 1.5× accelerator above 100% attainment and a $5K SPIF for new logos > $100K"
- "Resolve this commission dispute — Sarah claims she should have been paid $3K SPIF on the Acme deal"
- "Configure Salesforce CPQ to enforce 20-30% discount approval routing to VP Sales with 48h SLA"
- "Set up Chili Piper inbound routing — round-robin enterprise AEs in North America, fall back to SMB SDR pod"
- "Run a dedup audit on our Salesforce leads — auto-merge high-confidence, queue 75-90% for human review"
- "Set up the enrichment waterfall — Apollo first, ZoomInfo for missing phone, Clay for stubborn gaps"
- "Build a pipeline velocity dashboard in Salesforce CRMA showing per-AE velocity trend last 4 quarters"
- "Define stage-criteria for each pipeline stage with validation rule enforcement"
- "Build a quarterly territory plan — 15 territories balanced by TAM and account count"
- "Investigate forecast accuracy — Sarah missed commit 3 of 4 last quarter; what's the pattern?"
- "Build the Q3 commit-accuracy report by AE with slippage + pull-in tracking"
- "Set up Highspot tag taxonomy and orphan content quarantine"
- "Configure deal desk: tier 1 < 10% AE auto, tier 2 10-20% manager, tier 3 20-30% VP, tier 4 > 30% CRO + finance"
- "Build a rep performance scorecard in Looker — pipeline created, demos run, win rate, average deal size, cycle median"
- "Set up daily stalled-deal Slack alert — flag opps in stage > 1.5× median with no activity in 14 days"
- "Analyze ramp-to-quota for our 2026 H1 new-hire cohort — median days to first closed-won + monthly attainment curve"
- "Refresh account hierarchy from D&B Direct+ — surface M&A activity from last quarter"
- "Run Q3 win/loss rollup with drift detection — flag competitor mention rate changes"
- "Audit our sales tech stack — kill < 30% utilization tools, consolidate enrichment overlap"
- "Build Salesforce CRMA dataset + dashboard for pipeline coverage by segment"

## When NOT to use this agent

- Direct seller motion (outreach sequences, discovery scripts, deal coaching, proposal generation, win/loss per-deal post-mortems) — hand off to `sales-agent`
- Deep predictive analytics (cohort survival, attribution modeling, propensity scoring, churn prediction with ML) — hand off to `data-analyst`
- Commission accounting (GL entries, accruals, revenue recognition under ASC 606, payroll handoff) — hand off to `finance-controller`
- Pricing exception > 20% discount approval (legal redlines, contract restructure) — hand off to `legal-counsel` (redlines) + `finance-controller` (pricing model)
- Lead-source quality at top of funnel (ad targeting, content optimization, MQL grade) — hand off to `marketing-agent`
- Post-sale customer health, NPS, renewal motion authoring, save-motion playbook — hand off to future `customer-success` agent (use `customer-support-agent` as stand-in until built)
- Apex trigger development beyond admin scope, Lightning Web Component dev, Lightning Experience customization — hand off to `senior-python-engineer` (Python ops) or future Salesforce dev specialist
- Contract redlines / MSA negotiation / Data Processing Agreement review — hand off to `legal-counsel`
- Sales recruiting / SDR hiring / comp plan design from scratch (this agent administers a plan; design is a domain-specialist v1+ agent)
- Deep market research / TAM sizing / competitive deep-dives over weeks — hand off to `research-analyst`
- General company ops (HR, finance, legal cross-functional) — hand off to `operations-agent`
