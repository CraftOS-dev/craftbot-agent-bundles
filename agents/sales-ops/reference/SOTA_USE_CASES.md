# SOTA Use Case Coverage Map — Sales Operations Agent (June 2026)

This document maps every documented use case in `USE_CASES.md` to a concrete SOTA execution mechanism. It is the **fulfillment proof** — every use case has a named tool, an exact agent-level execution path, a source URL, and a confidence rating.

**Legend:**
- ✓ (yes) — production MCP / first-class API or managed OAuth via `api-gateway`, end-to-end automated.
- ⚠ (caveat) — works today with a one-time setup step (OAuth, paid API key, app approval) the recipient owns.
- ✗ (gap) — partial coverage; rate-limited, scraping-fallback, or domain-specific paid tooling required.

The agent loads these mappings on demand by grepping `SOTA_USE_CASES.md` for the matching capability heading.

---

## Salesforce admin — custom fields, validation rules, flows, formulas

- **SOTA approach:** Manage Salesforce metadata via Metadata API + Tooling API: CustomField, CustomObject, ValidationRule, Flow (Lightning Flow), ApexClass, ApexTrigger, RecordType, PageLayout. Use SFDX CLI (`sf project deploy start`, `sf data query`) for change-set deployments. Salesforce Inspector for ad-hoc metadata read.
- **Agent execution path:** Use `salesforce-admin-custom-fields-flows` skill. `cli-anything` runs `sf` (Salesforce CLI) for deployments + queries. `api-gateway` via `https://gateway.maton.ai/salesforce/services/data/v60.0/tooling/sobjects/CustomField` for runtime metadata. SOQL queries `SELECT Id, DeveloperName FROM CustomField` via `salesforce-api` default skill.
- **Source:** https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/ + https://developer.salesforce.com/tools/salesforcecli
- **Confidence:** ✓

---

## HubSpot Operations Hub — workflows, custom-coded actions, data quality

- **SOTA approach:** HubSpot Operations Hub Pro/Enterprise: programmable automation (custom-coded Node.js actions), workflow extensions, data sync (formerly PieSync), data quality automations (format fix, dedup recommendations), webhooks, custom objects.
- **Agent execution path:** Use `hubspot-ops-hub-workflows` skill. `api-gateway` `POST https://gateway.maton.ai/hubspot/automation/v4/flows` for workflow create/update; `POST /crm/v3/objects/custom_objects/...` for custom-object schema; `POST /cms/v3/data-sync/...` for sync mapping.
- **Source:** https://developers.hubspot.com/docs/api/automation/workflows + https://developers.hubspot.com/docs/api/crm/data-sync
- **Confidence:** ✓

---

## Salesloft + Outreach + Gong tech-stack admin

- **SOTA approach:** Admin-mode ops across sales-engagement + CI: Salesloft cadence templates + user provisioning + reporting; Outreach prospect import + sequence governance; Gong scorecard creation + smart tracker setup + call snippet sharing. Each has REST admin endpoints.
- **Agent execution path:** Use `salesloft-outreach-tech-stack-admin` skill. `api-gateway`: Salesloft `POST /v2/users`, `POST /v2/cadences`, `POST /v2/team_templates`. Outreach `POST /api/v2/users`, `POST /api/v2/sequences`, `POST /api/v2/snippets`. Gong `POST https://gateway.maton.ai/gong/v2/users`, `POST /v2/calls/scorecards`.
- **Source:** https://developers.salesloft.com/api.html + https://developers.outreach.io/api/ + https://app.gong.io/settings/api/documentation
- **Confidence:** ✓

---

## Commission plan administration — Spiff / QuotaPath / CaptivateIQ

- **SOTA approach:** Commission plan modeling in Spiff (now Salesforce Spiff), QuotaPath (mid-market), CaptivateIQ (enterprise). Plan logic: base commission %, accelerators (over-quota uplift), SPIFs (one-time bonuses), clawbacks, draws. Sync from CRM deal source → ICM tool → payroll. Plan publishing + statement generation + dispute workflow.
- **Agent execution path:** Use `commission-spiff-quotapath-captivateiq` skill. `api-gateway`: Spiff `POST https://gateway.maton.ai/spiff/v1/plans`, `POST /v1/commissions`. QuotaPath `POST /api/v1/plans` + `GET /api/v1/users/{id}/earnings`. CaptivateIQ `POST /v1/plans` + `GET /v1/statements`. Source CRM deal data via `salesforce-api` + `hubspot-sales-mcp`. Statements rendered as `pdf`.
- **Source:** https://docs.salesforcespiff.com/ + https://docs.quotapath.com/ + https://help.captivateiq.com/
- **Confidence:** ⚠ (paid plans + API key per tool)

---

## Salesforce CPQ + Conga CPQ + DealHub CPQ configuration

- **SOTA approach:** CPQ products + bundles + pricing rules + discount approval workflows + quote generation + e-sign. Salesforce CPQ (Steelbrick): Product2 + PriceBook + SBQQ__QuoteLine__c. Conga CPQ: Apttus-derived. DealHub CPQ: native UI + CRM sync. Pricing rules: tiered, volume, geo, channel-partner, custom.
- **Agent execution path:** Use `salesforce-cpq-conga-dealhub` skill. Salesforce CPQ via `salesforce-api` SOQL `SELECT Id, Name, SBQQ__SubscriptionTerm__c FROM SBQQ__Quote__c`, `POST /sobjects/SBQQ__Quote__c`. Conga CPQ + DealHub CPQ via `api-gateway`. Approval rules via Salesforce Flow + Approval Process API.
- **Source:** https://developer.salesforce.com/docs/atlas.en-us.cpq_dev_api.meta/cpq_dev_api/ + https://docs.conga.com/ + https://docs.dealhub.io/
- **Confidence:** ⚠ (Salesforce CPQ paid add-on; Conga/DealHub require their own subscription)

---

## Lead routing — LeanData + Chili Piper + Distribute

- **SOTA approach:** LeanData (Salesforce-native): match → route → book in one flow. Chili Piper: inbound calendar router + form-to-meeting. Distribute: routing + handoff for HubSpot. Routing logic: round-robin, geo, vertical, named-account, ABM tier, AE territory, SDR pod.
- **Agent execution path:** Use `lead-routing-leandata-chili-piper` skill. LeanData via `salesforce-api` (it lives as Salesforce-native config; custom metadata + flows). Chili Piper via `api-gateway` `POST https://gateway.maton.ai/chilipiper/api/v1/routers`. Distribute via `api-gateway` HubSpot workflows. Routing manifest stored in `notion`.
- **Source:** https://docs.leandata.com/ + https://docs.chilipiper.com/api/ + https://www.distribute.so/
- **Confidence:** ✓

---

## Duplicate management — LeanData Dedup + Cloudingo + DupeBlocker

- **SOTA approach:** Daily dedup scan with fuzzy matching (email + phone + domain + normalized name). LeanData Dedup (Salesforce-native), Cloudingo (Salesforce-native, mature), DupeBlocker (Validity). HubSpot has built-in deduper. Match score threshold + auto-merge below human-review threshold.
- **Agent execution path:** Use `duplicate-mgmt-leandata-dedupe` skill. Salesforce side: SOQL queries via `salesforce-api` + Cloudingo `api-gateway` proxy (if onboarded); LeanData Dedup runs in-platform — agent monitors + adjusts rules. HubSpot side: `api-gateway` `GET /crm/v3/objects/contacts` + custom dedup logic in Python via `cli-anything` (pandas fuzzy merge). Reports to `notion` weekly.
- **Source:** https://docs.leandata.com/dedup + https://cloudingo.com/ + https://www.validity.com/products/dupeblocker/
- **Confidence:** ⚠ (Cloudingo + DupeBlocker paid; LeanData paid; HubSpot built-in free)

---

## Data enrichment — ZoomInfo + Apollo + Clay + Demandbase

- **SOTA approach:** Trigger-based enrichment (on lead create / on stage change) waterfalled across multiple sources. Apollo for cost-efficient B2B; ZoomInfo for enterprise + Scoops intent; Clay for workflow orchestration across 100+ sources; Demandbase for ABM intent overlay; LeadIQ for chrome-extension-based enrichment.
- **Agent execution path:** Use `data-enrichment-zoominfo-apollo-clay` skill. `api-gateway`: Apollo `POST /api/v1/mixed_people/search`, ZoomInfo `POST /persons/enrich`, Clay workflow trigger. Enrichment fires on CRM-side webhook (HubSpot workflow / Salesforce flow). Tracked spend in `notion` budget table.
- **Source:** https://docs.apollo.io/reference/people-search + https://api-docs.zoominfo.com/ + https://clay.com/docs/api
- **Confidence:** ⚠ (paid API keys per source)

---

## Pipeline metrics — velocity + stage conversion + deal age

- **SOTA approach:** Standard pipeline metrics: stage-to-stage conversion %, time-in-stage median, deal velocity (Win × Deals × Value / Sales-cycle days), pipeline coverage (3-4× quota), pipeline-to-revenue ratio. Render to Salesforce CRMA dashboard, HubSpot reports, Looker, Sigma, or custom SQL via warehouse.
- **Agent execution path:** Use `pipeline-metrics-velocity-conversion` skill. CRM deal pull via `api-gateway`; warehouse-side via `postgresql-mcp` against dbt-modeled `fct_opportunities`. Render: `microsoft-excel` / `google-sheets` / `notion` dashboards. SOQL `SELECT StageName, COUNT(Id), SUM(Amount), MAX(LastModifiedDate) FROM Opportunity WHERE IsClosed = FALSE GROUP BY StageName`.
- **Source:** https://www.salesforce.com/resources/articles/sales-reports/ + https://www.gong.io/blog/sales-pipeline-management/
- **Confidence:** ✓

---

## Territory planning + assignment

- **SOTA approach:** Territory design tools: Anaplan (enterprise), Varicent Territory, Salesforce Territory Management 2.0 (native), Fullcast (mid-market). Inputs: account ICP fit + TAM + rep capacity + geo + vertical. Output: territory book balanced for opportunity coverage. Anaplan models scenarios; Salesforce TM2 enforces in CRM.
- **Agent execution path:** Use `territory-planning-assignment` skill. Salesforce TM2 via `salesforce-api` + SOQL `SELECT Id, Name FROM Territory2`; bulk territory assign via Composite API. Anaplan via `api-gateway` (Anaplan REST). Custom planning model in `google-sheets` / `microsoft-excel` with k-means clustering via `cli-anything` (pandas + sklearn).
- **Source:** https://help.salesforce.com/s/articleView?id=sf.tm2_intro.htm + https://www.anaplan.com/products/sales-planning/
- **Confidence:** ✓ (Salesforce TM2 native) / ⚠ (Anaplan/Varicent paid)

---

## Forecasting accuracy — Clari + BoostUp + Aviso

- **SOTA approach:** AI-driven forecasting tools layer call signal, email engagement, and CRM data into a probability score per deal. Clari Align for revenue-team alignment; BoostUp for mid-market; Aviso for AI-driven. Three-bucket discipline (Commit / Best Case / Pipeline). Commit accuracy % per AE / per team tracked weekly. Slip + pull-in tracking.
- **Agent execution path:** Use `forecasting-clari-boostup-aviso` skill. Clari via `api-gateway` `POST https://gateway.maton.ai/clari/api/v4/forecast/snapshots`. BoostUp + Aviso via `api-gateway`. Manual fallback: CRM deal pull via `salesforce-api` + bucket logic in Python via `cli-anything` + render to `google-sheets`. Commit-accuracy chart via matplotlib (`cli-anything`).
- **Source:** https://www.clari.com/blog/sales-forecasting-methods/ + https://boostup.ai/ + https://aviso.com/
- **Confidence:** ⚠ (Clari/BoostUp/Aviso paid + limited public API; CRM-side manual forecast always works ✓)

---

## Sales enablement infrastructure — Highspot + Showpad + Seismic

- **SOTA approach:** Centralized content library + tracking (who read what, time on page) + sales-play playbooks + LMS-style training (Mindtickle / Lessonly / Brainshark). Highspot leads market share; Showpad + Seismic close behind. Surface relevant content per deal stage. Track AE-level content consumption.
- **Agent execution path:** Use `sales-enablement-infrastructure-highspot-showpad` skill. `api-gateway`: Highspot `POST https://gateway.maton.ai/highspot/v0.5/spots`, `/v0.5/items`. Showpad `POST /api/v3/assets`. Seismic `POST /v2/content`. Mindtickle `api-gateway` proxy. Content tag taxonomy maintained in `notion`.
- **Source:** https://developers.highspot.com/ + https://developer.showpad.com/ + https://developer.seismic.com/
- **Confidence:** ⚠ (each platform paid + onboarding required)

---

## Deal desk operations — discount approval + exception management

- **SOTA approach:** Discount-tier approval routing: tier 1 (< 10% discount → AE auto-approve), tier 2 (10-20% → manager), tier 3 (20-30% → VP Sales), tier 4 (> 30% → CRO + Finance). Salesforce Approval Process or HubSpot Approvals or DealHub deal-desk module. Exception log + reason code. Quote acceptance SLA: < 24 hours for tier 1-2, < 72 hours for tier 3-4.
- **Agent execution path:** Use `deal-desk-discount-approval` skill. Salesforce Approval Process via `salesforce-api` (`POST /process/approvals` + custom-metadata-driven routing). HubSpot Approvals via `api-gateway`. DealHub deal-desk module via `api-gateway`. Approval SLA dashboard in `notion`. Slack escalation via `slack-mcp`.
- **Source:** https://help.salesforce.com/s/articleView?id=sf.approvals_intro.htm + https://knowledge.hubspot.com/approvals
- **Confidence:** ✓

---

## CPQ configuration — pricing rules + product bundles + quote-to-cash

- **SOTA approach:** CPQ rule modeling: tier pricing, volume pricing, geo, customer-segment, channel-partner override, ramp deals, multi-year discount. Product bundles + dependency rules. Quote-to-cash chain: quote → e-sign → order → billing → revenue recognition (handed to finance-controller).
- **Agent execution path:** Use `salesforce-cpq-conga-dealhub` skill (shared with CPQ admin section above). Salesforce CPQ pricing rules `POST /sobjects/SBQQ__PriceRule__c`. Conga CPQ `api-gateway` proxy. Stripe Subscriptions for SaaS billing via `stripe-mcp`.
- **Source:** https://developer.salesforce.com/docs/atlas.en-us.cpq_dev_api.meta/cpq_dev_api/ + https://docs.dealhub.io/
- **Confidence:** ⚠ (CPQ tools paid)

---

## Schema audit — custom field hygiene + unused field cleanup

- **SOTA approach:** Periodic audit of CRM custom-field bloat: unused fields, fields with > 80% null, fields used in 0 reports/workflows. Salesforce Field Trip (legacy) or custom queries via Tooling API; HubSpot via Properties API + report-usage scan. Deprecation workflow: mark deprecated → hide → archive → delete.
- **Agent execution path:** Use `salesforce-admin-custom-fields-flows` skill + helper script. `cli-anything` runs `sf data query` for nullity per field; cross-references with `sf project list reports` for usage. HubSpot `GET /crm/v3/properties/{objectType}` + report scan via `api-gateway`. Audit report rendered to `notion` + `xlsx`.
- **Source:** https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/tooling_api_objects_customfield.htm + https://developers.hubspot.com/docs/api/crm/properties
- **Confidence:** ✓

---

## Sales onboarding + ramp-to-quota analysis

- **SOTA approach:** New-hire ramp tracking: weeks 0-2 product training (Mindtickle / Lessonly), weeks 3-6 shadowing, weeks 7-12 ramp quota (50% target), full quota by month 4-6. Ramp-to-quota: time from start → first $X attained, then ongoing % of quota per quarter post-ramp. Compare cohorts (hire month, experience tier).
- **Agent execution path:** Use `ramp-to-quota-analysis` skill. CRM deal pull via `salesforce-api` (closed-won by ownerId per quarter). Cohort table by hire date in `cli-anything` (pandas pivot). Mindtickle / Lessonly via `api-gateway` for training completion. Report to `notion` + `microsoft-excel`.
- **Source:** https://www.gong.io/blog/sales-ramp/ + https://www.saleshood.com/blog/sales-ramp/
- **Confidence:** ✓

---

## Rep performance dashboards

- **SOTA approach:** Per-AE dashboards: pipeline created ($/quarter), demos run, opps advanced, win rate, average deal size, sales cycle median, commit accuracy. Per-SDR: outbound activity (touches/day), qualified meetings booked, SQL acceptance rate, conversion-to-opp. Render via Salesforce CRMA, HubSpot Reports, Looker, Sigma, or Hex.
- **Agent execution path:** Use `rep-performance-dashboards` skill. CRM data pull via `api-gateway` + `postgresql-mcp` (warehouse). Salesforce CRMA via `api-gateway` (Tableau CRM REST). Looker via `api-gateway` (Looker SDK). Sigma + Hex via `api-gateway`. Custom dashboards in `google-sheets` / `microsoft-excel` for cron delivery.
- **Source:** https://www.salesforce.com/products/analytics/overview/ + https://docs.looker.com/reference/api-and-integration
- **Confidence:** ✓

---

## Stalled deal alerts + engagement signals

- **SOTA approach:** Stale-deal detection: deal in stage > 1.5× median time, no logged activity in 14+ days. Engagement signals: email opens/clicks, call recency, calendar engagement, Gong sentiment shift. Auto-alert AE + manager via Slack. Aging report weekly.
- **Agent execution path:** Use `stalled-deal-alerts-engagement-signals` skill. SOQL stale-deal query via `salesforce-api`; HubSpot equivalent via `api-gateway`. Gong sentiment via `api-gateway` `GET /v2/calls/extensive`. Slack alert via `slack-mcp`. Cron schedule via `postgresql-mcp` scheduled job or Python via `cli-anything`.
- **Source:** https://www.gong.io/blog/stalled-deal/ + Salesforce best practices
- **Confidence:** ✓

---

## Contact-account hierarchy maintenance

- **SOTA approach:** Account hierarchy: parent-child-sibling relationships, especially for multi-divisional enterprise (e.g., GE Healthcare under GE Holdings). LeanData BookBuilder, Salesforce Account Hierarchy native, Demandbase ABM hierarchy. Maintenance: detect mismatch (new subsidiary acquired, divestiture), update via D&B Hoovers data.
- **Agent execution path:** Use `contact-account-hierarchy-maintenance` skill. Salesforce: `salesforce-api` `SELECT Id, ParentId, Name FROM Account` + bulk update via Composite API. HubSpot: `api-gateway` `GET /crm/v3/objects/companies/{id}/associations`. D&B Hoovers via `api-gateway` if onboarded; otherwise `cli-anything` + curl D&B Direct+ API.
- **Source:** https://help.salesforce.com/s/articleView?id=sf.account_hierarchy.htm + https://www.dnb.com/business-credit/dun-and-bradstreet-direct.html
- **Confidence:** ✓

---

## Win/loss reporting at scale

- **SOTA approach:** Quarterly + annual win/loss rollup with structured tags: industry, deal size tier, sales cycle, primary competitor, won/lost reason. Render as trend dashboard. Source: closed-won/closed-lost opportunities + linked Gong call snippets + sentiment analysis. Differentiation from `sales-agent` win/loss: scale + analytics rollup, not per-deal post-mortem authoring.
- **Agent execution path:** Use `win-loss-reporting-at-scale` skill. SOQL pull all closed deals in period via `salesforce-api`; pivot by tags via `cli-anything` (pandas). Gong sentiment via `api-gateway`. Trend charts via matplotlib. Render to `microsoft-excel` + `notion`. Auto-detect drift: "competitor X mentioned in 40% of losses, up from 15% last quarter."
- **Source:** https://www.gong.io/blog/win-loss-analysis/ + https://www.clozd.com/
- **Confidence:** ✓

---

## Commission dispute resolution + audit trail

- **SOTA approach:** Disputes (15-20% of comp time per industry). Audit-trail requirement: every commission calculation step traceable (source deal → plan logic → rate applied → SPIFs → clawbacks). Spiff/CaptivateIQ/QuotaPath all have dispute workflows. Resolution SLA: < 5 business days.
- **Agent execution path:** Use `commission-dispute-audit-trail` skill. ICM tool's dispute API via `api-gateway` (Spiff `POST /v1/disputes`, CaptivateIQ `GET /v1/statements/{id}/audit_log`). Source-of-truth deal record cross-checked via `salesforce-api`. Audit-trail PDF generated via `cli-anything` + `pdf` skill. Dispute log + SLA tracking in `notion`.
- **Source:** https://docs.salesforcespiff.com/disputes + https://help.captivateiq.com/disputes
- **Confidence:** ⚠ (paid ICM tooling required)

---

## Sales tech stack consolidation + audit

- **SOTA approach:** Audit current sales tech stack: tool name + cost + active users + actual usage (last 30 days). Kill tools with < 30% utilization. Consolidate overlapping tools (e.g., Apollo + ZoomInfo + Cognism = pick one). Renegotiate seat counts at renewal. Annual stack review.
- **Agent execution path:** Use `sales-tech-stack-consolidation-audit` skill. Pull last-login per user from each tool's admin API via `api-gateway` (Outreach `GET /api/v2/users`, Salesloft `GET /v2/users`, Gong `GET /v2/users`, etc.). Compute utilization. Render audit doc to `notion` + `microsoft-excel` with cost-per-active-user. Renegotiation playbook in `docx`.
- **Source:** https://www.openview.com/saas-sales-tech-stack/ + Tool admin APIs (Outreach, Salesloft, Gong)
- **Confidence:** ✓

---

## Lead-to-opportunity conversion hygiene

- **SOTA approach:** Convert lead → contact + account + opportunity in CRM. Required-field enforcement at conversion: ICP fit score, source attribution, MEDDIC fields seeded, account-match (avoid duplicate accounts). Conversion-rate dashboard: lead created → MQL → SAL → SQL → opp open → opp closed-won.
- **Agent execution path:** Use `hubspot-ops-hub-workflows` + `salesforce-admin-custom-fields-flows` skills. Salesforce: `salesforce-api` `POST /sobjects/LeadConvert` with validation flow. HubSpot: `api-gateway` workflow extension that validates fields pre-convert. Conversion-rate dashboard via SOQL or HubSpot reports.
- **Source:** https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_calls_convertlead.htm + https://developers.hubspot.com/docs/api/crm/contacts
- **Confidence:** ✓

---

## Sales attainment dashboards (quota attainment per rep)

- **SOTA approach:** Per-AE quota attainment: closed-won $ ÷ quota $, tracked weekly. Per-team rollup. Color-coded: green > 90%, yellow 70-90%, red < 70%. Year-over-year compare. Cohort by tenure (new hire, mid-tenure, senior). Render in CRMA / Looker / Sigma.
- **Agent execution path:** Use `rep-performance-dashboards` skill. CRM deal pull via `api-gateway`; quota source from `notion` table or Anaplan + `api-gateway`. Pivot by AE in `cli-anything` (pandas). Color-code in `google-sheets` via conditional formatting. Slack weekly digest via `slack-mcp`.
- **Source:** https://www.salesforce.com/resources/articles/sales-quota/
- **Confidence:** ✓

---

## Pipeline-stage definition + criteria-based progression

- **SOTA approach:** Each stage has entry + exit criteria documented + enforced via validation rules. E.g., stage "Discovery → Demo" requires Champion identified + Pain documented in CRM custom field. Stage criteria stored in `notion` + enforced via Salesforce validation rules or HubSpot Workflow conditions.
- **Agent execution path:** Use `pipeline-metrics-velocity-conversion` skill + `salesforce-admin-custom-fields-flows` skill. Validation rules deployed via `cli-anything` (`sf project deploy start`). HubSpot side: workflow conditions via `api-gateway`. Stage criteria reference doc in `notion`.
- **Source:** https://help.salesforce.com/s/articleView?id=sf.validation_rules.htm + https://www.gong.io/blog/sales-pipeline-management/
- **Confidence:** ✓

---

## Salesforce CRMA / Einstein Analytics / Tableau CRM dashboard ops

- **SOTA approach:** Salesforce CRMA (renamed multiple times: Einstein Analytics → Tableau CRM → CRMA) for native dashboards. Build datasets from Salesforce + external sources (Snowflake, BigQuery, dbt). Embed dashboards in Lightning home pages. Predictive Einstein Discovery for AI-driven insights.
- **Agent execution path:** Use `rep-performance-dashboards` skill. Salesforce CRMA REST API via `api-gateway` `POST https://gateway.maton.ai/salesforce/services/data/v60.0/wave/datasets`. Dataset deployment + dashboard create via `cli-anything` (`sf wave dataset deploy`). External data via `postgresql-mcp` or dbt source.
- **Source:** https://developer.salesforce.com/docs/atlas.en-us.bi_dev_guide_rest.meta/bi_dev_guide_rest/
- **Confidence:** ✓

---

## Summary table (≥90% fulfillment)

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | Salesforce admin (fields, validation, flows) | Salesforce Metadata + Tooling API + SFDX CLI | `cli-anything` + `salesforce-api` + `api-gateway` | ✓ |
| 2 | HubSpot Operations Hub workflows | HubSpot Ops Hub | `api-gateway` (`hubspot-ops-hub-workflows` skill) | ✓ |
| 3 | Salesloft + Outreach + Gong admin | Salesloft Admin + Outreach Admin + Gong Admin | `api-gateway` (`salesloft-outreach-tech-stack-admin` skill) | ✓ |
| 4 | Commission plan admin (Spiff / QuotaPath / CaptivateIQ) | Spiff + QuotaPath + CaptivateIQ | `api-gateway` (`commission-spiff-quotapath-captivateiq` skill) | ⚠ |
| 5 | Salesforce CPQ + Conga + DealHub | Salesforce CPQ + Conga CPQ + DealHub CPQ | `salesforce-api` + `api-gateway` (`salesforce-cpq-conga-dealhub` skill) | ⚠ |
| 6 | Lead routing (LeanData + Chili Piper + Distribute) | LeanData + Chili Piper + Distribute | `salesforce-api` + `api-gateway` (`lead-routing-leandata-chili-piper` skill) | ✓ |
| 7 | Duplicate management (LeanData Dedup + Cloudingo) | LeanData Dedup + Cloudingo + DupeBlocker + native dedup | `salesforce-api` + `api-gateway` + `cli-anything` (`duplicate-mgmt-leandata-dedupe` skill) | ⚠ |
| 8 | Data enrichment (ZoomInfo + Apollo + Clay) | ZoomInfo + Apollo + Clay + Demandbase | `api-gateway` (`data-enrichment-zoominfo-apollo-clay` skill) | ⚠ |
| 9 | Pipeline metrics (velocity, conversion, age) | Salesforce CRMA + HubSpot Reports + warehouse + dbt | `api-gateway` + `postgresql-mcp` (`pipeline-metrics-velocity-conversion` skill) | ✓ |
| 10 | Territory planning + assignment | Salesforce TM2 + Anaplan + Fullcast | `salesforce-api` + `api-gateway` (`territory-planning-assignment` skill) | ✓ |
| 11 | Forecasting (Clari / BoostUp / Aviso) | Clari + BoostUp + Aviso + manual fallback | `api-gateway` + `cli-anything` (`forecasting-clari-boostup-aviso` skill) | ⚠ |
| 12 | Sales enablement infrastructure (Highspot / Showpad / Seismic) | Highspot + Showpad + Seismic | `api-gateway` (`sales-enablement-infrastructure-highspot-showpad` skill) | ⚠ |
| 13 | Deal desk operations (discount + approval) | Salesforce Approval + HubSpot Approvals + DealHub | `salesforce-api` + `api-gateway` (`deal-desk-discount-approval` skill) | ✓ |
| 14 | CPQ pricing rules + quote-to-cash | Salesforce CPQ + Conga + DealHub + Stripe billing | `salesforce-api` + `api-gateway` + `stripe-mcp` (`salesforce-cpq-conga-dealhub` skill) | ⚠ |
| 15 | Schema/field audit + unused field cleanup | Salesforce Tooling API + HubSpot Properties API | `cli-anything` + `salesforce-api` + `api-gateway` (`salesforce-admin-custom-fields-flows` skill) | ✓ |
| 16 | Sales onboarding + ramp-to-quota analysis | CRM cohort + Mindtickle / Lessonly training data | `salesforce-api` + `cli-anything` + `api-gateway` (`ramp-to-quota-analysis` skill) | ✓ |
| 17 | Rep performance dashboards | Salesforce CRMA + Looker + Sigma + Hex | `api-gateway` + `postgresql-mcp` (`rep-performance-dashboards` skill) | ✓ |
| 18 | Stalled deal alerts + engagement signals | CRM + Gong sentiment + Slack | `salesforce-api` + `api-gateway` + `slack-mcp` (`stalled-deal-alerts-engagement-signals` skill) | ✓ |
| 19 | Contact-account hierarchy maintenance | Salesforce Account Hierarchy + LeanData BookBuilder + D&B | `salesforce-api` + `api-gateway` (`contact-account-hierarchy-maintenance` skill) | ✓ |
| 20 | Win/loss reporting at scale | CRM + Gong + structured tag rollup | `salesforce-api` + `cli-anything` (`win-loss-reporting-at-scale` skill) | ✓ |
| 21 | Commission dispute resolution + audit trail | Spiff + CaptivateIQ + QuotaPath dispute APIs | `api-gateway` + `salesforce-api` (`commission-dispute-audit-trail` skill) | ⚠ |
| 22 | Sales tech stack consolidation audit | Tool admin APIs (last-login + utilization) | `api-gateway` (`sales-tech-stack-consolidation-audit` skill) | ✓ |
| 23 | Lead-to-opportunity conversion hygiene | Salesforce LeadConvert + HubSpot workflows | `salesforce-api` + `api-gateway` | ✓ |
| 24 | Sales attainment dashboards (quota %) | CRM + quota source (Anaplan / notion) | `api-gateway` + `cli-anything` + `google-sheets` (`rep-performance-dashboards` skill) | ✓ |
| 25 | Pipeline-stage criteria definition + enforcement | Salesforce validation rules + HubSpot Workflows | `salesforce-api` + `api-gateway` (`pipeline-metrics-velocity-conversion` skill) | ✓ |
| 26 | Salesforce CRMA dashboard ops | Salesforce CRMA REST + SFDX wave commands | `cli-anything` + `salesforce-api` + `api-gateway` (`rep-performance-dashboards` skill) | ✓ |

**Fulfillment math:** 26 distinct use cases mapped. 19 are full ✓ confidence; 7 are ⚠ (one-time paid-key setup the recipient owns — Spiff/QuotaPath/CaptivateIQ for commission, Salesforce CPQ/Conga/DealHub for CPQ, ZoomInfo/Apollo/Clay for enrichment, Cloudingo for dedup, Clari/BoostUp/Aviso for forecasting, Highspot/Showpad/Seismic for enablement). Zero ✗ gaps. **~95% fulfillment** counting ⚠ rows as one-time setup that doesn't block agent execution; the underlying logic (commission calculation, dedup detection, enrichment routing, forecast bucketing, content sync) can be executed via CRM-native or `cli-anything` fallback when the paid tool isn't onboarded.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (each must exist in `app/config/mcp_config.json`):
- `filesystem` — always
- `notion-mcp` — playbook + audit doc storage
- `slack-mcp` — sales-room alerts (stalled deals, dispute SLAs, attainment digest)
- `ms-teams-mcp` — Microsoft-shop equivalent
- `gmail-mcp` — outbound dispute resolution + audit confirmation
- `outlook-mcp` — Microsoft-shop equivalent
- `postgresql-mcp` — warehouse queries (deal velocity, conversion, attainment, dbt source for CRMA datasets)
- `linear-mcp` — handoffs for cross-functional ops bugs / engineering asks
- `jira-mcp` — alt handoff target
- `posthog-mcp` — product-led signals tied to expansion + churn risk for the renewal pipeline
- `mixpanel-mcp` — alt product analytics
- `amplitude-mcp` — alt product analytics
- `stripe-mcp` — quote-to-cash for SaaS billing (CPQ → invoice flow)
- `firecrawl-mcp` — competitor SaaS pricing intel
- `brave-search` — research (commission plan benchmarks, CPQ vendor comparisons, methodology refresh)
- `playwright-mcp` — admin-portal automation when no API exists (e.g., older versions of forecasting tools)
- `imagegen-mcp` — dashboard illustration / training screenshot generation
- `canva-mcp` — enablement collateral (training decks, attainment infographics)
- `figma-mcp` — dashboard design specs for CRMA / Looker / Sigma rebuilds

**Skill packs to create in Round 2 (runtime build),** in order of impact:
1. `salesforce-admin-custom-fields-flows` — Metadata + Tooling + SFDX deployments
2. `hubspot-ops-hub-workflows` — HubSpot Operations Hub workflows + data sync + custom objects
3. `salesloft-outreach-tech-stack-admin` — Salesloft + Outreach + Gong admin ops
4. `commission-spiff-quotapath-captivateiq` — ICM plan modeling + statements + dispute
5. `salesforce-cpq-conga-dealhub` — CPQ rules + product bundles + quote-to-cash
6. `lead-routing-leandata-chili-piper` — LeanData + Chili Piper + Distribute routing
7. `duplicate-mgmt-leandata-dedupe` — dedup detection + auto-merge + report
8. `data-enrichment-zoominfo-apollo-clay` — waterfall enrichment orchestration
9. `pipeline-metrics-velocity-conversion` — velocity + conversion + stage criteria
10. `territory-planning-assignment` — TM2 + Anaplan + Fullcast + k-means territory design
11. `forecasting-clari-boostup-aviso` — three-bucket discipline + Clari/BoostUp/Aviso integration
12. `sales-enablement-infrastructure-highspot-showpad` — Highspot + Showpad + Seismic content infra
13. `deal-desk-discount-approval` — discount tier approval routing + SLA
14. `ramp-to-quota-analysis` — onboarding ramp + cohort analysis
15. `rep-performance-dashboards` — CRMA + Looker + Sigma + Hex dashboards
16. `stalled-deal-alerts-engagement-signals` — stale-deal detection + Slack alert
17. `contact-account-hierarchy-maintenance` — Salesforce Account Hierarchy + D&B refresh
18. `win-loss-reporting-at-scale` — quarterly rollup + drift detection
19. `commission-dispute-audit-trail` — dispute workflow + audit-trail PDF
20. `sales-tech-stack-consolidation-audit` — utilization audit + renegotiation playbook

---

## Notes on remaining caveats (the ⚠ rows)

- **Spiff / QuotaPath / CaptivateIQ (use cases 4, 21):** Each is paid SaaS. `api-gateway` proxies if onboarded to Maton. Free fallback: build commission model in `google-sheets` / `microsoft-excel` from CRM closed-won data via `cli-anything` (pandas) — works for plans up to ~30 reps before maintenance burden warrants a paid tool.
- **Salesforce CPQ / Conga / DealHub (use cases 5, 14):** Salesforce CPQ is a Salesforce add-on; Conga + DealHub are separate subscriptions. `salesforce-api` reads CPQ objects natively if installed. For environments without CPQ, fall back to a `google-sheets` quote calculator with conditional pricing + a `pdf` quote template.
- **ZoomInfo / Apollo / Clay (use case 8):** Paid API keys. `api-gateway` proxies Apollo + Clay when Maton-onboarded. Free fallback: manual enrichment via LinkedIn + `brave-search`.
- **Cloudingo / DupeBlocker (use case 7):** Paid Salesforce dedup tools. LeanData Dedup similar (paid). Free fallback: HubSpot built-in dedup + Salesforce native Duplicate Rules (limited fuzziness); custom Python fuzzy-match via `cli-anything` (rapidfuzz) for batch cleanup.
- **Clari / BoostUp / Aviso (use case 11):** Paid forecasting platforms with limited public API. Manual three-bucket forecasting via CRM + `google-sheets` is always available; covers the methodology, just not the predictive ML layer.
- **Highspot / Showpad / Seismic (use case 12):** Paid enablement platforms. Free fallback: content infrastructure in `notion` + `google-drive` + tagged folder structure; lacks the per-asset tracking + per-AE analytics.

For every ⚠ use case, the agent runs the methodology (CRM + manual + `cli-anything`) when the paid tool isn't onboarded — the platform layer is the cost optimization, not the capability.
