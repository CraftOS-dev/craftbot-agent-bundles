# Sales Operations — Source Attribution

Section-to-source map for `soul.md` and `role.md`. **Not** loaded into context — for human verification.

URLs in `agent.yaml → sources` and `reference/INVENTORY.md`. Per-use-case SOTA mapping in `reference/SOTA_USE_CASES.md`.

---

## soul.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Opening identity + 3 convictions | Composition synthesis distilling load-bearing rules: stage-definitions-foundation (Salesforce + HubSpot validation rule docs + Gong pipeline management research), dispute-time-burn-20% (industry SalesOps surveys + Spiff / CaptivateIQ help center dispute SLAs), CRM-source-of-truth (Salesforce best practices + Validity data-quality research) | Three convictions composed from industry-standard sources |
| Purpose | HubSpot Operations Hub + Salesforce Admin Trail + OpenView SaaS sales tech stack frameworks for end-to-end SalesOps role definition | |
| Execution stack | `reference/SOTA_USE_CASES.md` — 20 bundled skill packs + default skills | Built from per-use-case SOTA mapping |
| When invoked — Admin change mode | Salesforce Metadata API + Tooling API + SFDX CLI deployment patterns | |
| When invoked — Commission plan admin mode | Spiff + QuotaPath + CaptivateIQ plan modeling patterns + pre/post comp delta methodology | |
| When invoked — Commission dispute mode | Spiff dispute API + CaptivateIQ audit-log API + 5-day SLA industry standard | |
| When invoked — Forecast accuracy mode | Clari three-bucket methodology + Gong forecasting research + commit-accuracy tracking patterns | |
| When invoked — CPQ configuration mode | Salesforce CPQ developer guide + Conga CPQ + DealHub CPQ documentation | |
| When invoked — Lead routing mode | LeanData docs + Chili Piper API + Distribute routing patterns | |
| When invoked — Duplicate management mode | LeanData Dedup + Cloudingo + DupeBlocker (Validity) documentation | |
| When invoked — Enrichment waterfall mode | Apollo + ZoomInfo + Clay + Demandbase API documentation + waterfall pattern | |
| When invoked — Pipeline metrics dashboards mode | Salesforce CRMA REST + Looker SDK + Sigma + Hex documentation | |
| When invoked — Deal desk mode | Salesforce Approval Process + HubSpot Approvals + DealHub deal-desk module | |
| When invoked — Stack consolidation mode | OpenView SaaS sales tech stack methodology + tool admin APIs | |
| When invoked — Win/loss rollup mode | Gong win/loss research + Clozd methodology + drift detection patterns | |
| Core operating rules | Merged from: Salesforce admin best practices (sandbox-before-production), validation-rule patterns (Salesforce documentation), commission dispute SLA standards (Spiff / CaptivateIQ), three-bucket forecast discipline (Clari), dedup fuzzy match thresholds (Cloudingo + LeanData), CPQ versioning (Salesforce CPQ best practices), routing testability (LeanData docs), schema bloat audit (Salesforce Tooling API patterns) | |
| Mode-specific decisions | One entry per mode keyed to the matching tool playbook (Salesforce admin / commission / CPQ / lead routing / dedup / enrichment / dashboards / deal desk / stack audit / win/loss / ramp) | |
| Quality gates | Composite: sandbox + rollback (Salesforce best practices); audit-trail integrity (ICM tooling standards); dependency check (Salesforce Tooling API); routing test (LeanData docs); dedup threshold (Cloudingo / LeanData); forecast bucket discipline (Clari); stage criteria enforcement (Salesforce validation rules); tool utilization audit (OpenView framework); dashboard one-source-of-truth (CRMA / Looker best practices); enablement tag taxonomy (Highspot docs) | |
| Output format | Composite: admin change spec template + commission plan logic template + dispute audit-trail PDF template + forecast snapshot template + CPQ config YAML + routing rules table + dedup report template + dashboard format + Slack alert spec + stack audit template + win/loss rollup template (all in role.md) | |
| Communication style | Composition synthesis informed by SalesOps practitioner conventions (concrete numbers, specific risks, active voice, source-of-truth citation) | |
| When to push back | Refuse: production deploy without sandbox; commission dispute without audit trail; field delete without dependency check; single-number forecast; low-confidence auto-merge; skip routing test; Friday afternoon CPQ deploy; keep low-utilization tool; skip win/loss tagging. Sources: Salesforce best practices + ICM tooling standards + Clari forecasting methodology + LeanData dedup docs + OpenView audit framework | |
| When to defer | Composition: sibling agents in CraftBot catalog (sales-agent, data-analyst, finance-controller, marketing-agent, customer-support-agent, legal-counsel, senior-python-engineer, operations-agent, research-analyst) | |
| First-conversation routine questions | Standard PROACTIVE.md self-init pattern from METHODOLOGY.md; questions adapted to SalesOps workflows (CRM, commission tool, biggest pain) | |
| Closing rule | Distilled from soul.md convictions + Salesforce sandbox-first best practice + ICM audit-trail standards + Clari forecast discipline | |

---

## role.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Capability reference → SalesOps motions | Composition synthesis — standard end-to-end SalesOps role inventory (HubSpot Operations Hub + Salesforce Admin Trail + OpenView playbooks) | |
| Capability reference → SalesOps technology categories | Composition: named CRMs, sales engagement, ICM, CPQ, forecasting, routing, dedup, enrichment, territory, enablement, analytics, warehouse, deal desk tools from industry sources | |
| Salesforce admin playbook → SFDX deploy workflow | Salesforce CLI documentation (`sf project deploy`, `sf data query`, `sf wave dataset deploy`) | |
| Salesforce admin playbook → Tooling API field-usage audit | Salesforce Tooling API documentation (CustomField, Report, Flow objects) | |
| Salesforce admin playbook → Validation rule patterns | Salesforce validation rule documentation + industry-standard MEDDIC + discount approval patterns | |
| Salesforce admin playbook → Lightning Flow patterns | Salesforce Lightning Flow documentation (record-triggered, scheduled, screen flows) | |
| HubSpot Operations Hub playbook → Workflow patterns | HubSpot Workflow API documentation + custom-coded action examples | |
| HubSpot Operations Hub playbook → Data sync mapping | HubSpot Data Sync API (PieSync successor) documentation | |
| Commission plan modeling playbook → Plan logic chain | Spiff + QuotaPath + CaptivateIQ help center plan documentation + industry-standard commission patterns (base rate, accelerators, SPIFs, clawbacks, draws) | |
| Commission plan modeling playbook → Plan template | Composition synthesis YAML format from Spiff + QuotaPath + CaptivateIQ commonalities | |
| Commission plan modeling playbook → Pre/post delta workflow | Industry-standard plan change methodology + ICM best practices | |
| Commission dispute audit-trail template | Spiff + CaptivateIQ dispute API documentation + audit-log structure | 5-section template synthesized |
| Salesforce CPQ rollout playbook → Pricing rule patterns | Salesforce CPQ developer guide + industry-standard tiered / volume / multi-year / bundle pricing patterns | |
| Salesforce CPQ rollout playbook → Bundle dependency rules | Salesforce CPQ Quote Line documentation | |
| Salesforce CPQ rollout playbook → Approval Process playbook | Salesforce Approval Process documentation + industry-standard discount tier matrix | |
| Lead routing playbook → LeanData routing patterns | LeanData documentation + Salesforce-native config patterns | |
| Lead routing playbook → Chili Piper routing patterns | Chili Piper API documentation + router config examples | |
| Duplicate management playbook → Fuzzy match thresholds | Cloudingo + LeanData Dedup + rapidfuzz documentation + industry-standard match scoring | |
| Duplicate management playbook → Cloudingo / LeanData workflow | Cloudingo + LeanData Dedup help center documentation | |
| Duplicate management playbook → Custom Python fuzzy dedup | rapidfuzz library documentation + pandas patterns | |
| Enrichment waterfall playbook → Apollo / ZoomInfo / Clay / Demandbase source order | Apollo + ZoomInfo + Clay + Demandbase API documentation + industry-standard waterfall pattern | |
| Pipeline metrics methodology → Velocity formula | Sales Velocity formula (Salesforce + Gong industry standard) | |
| Pipeline metrics methodology → Stage conversion % | Standard CRM pipeline analytics methodology | |
| Pipeline metrics methodology → Deal age in stage | Gong stalled-deal research (1.5× median threshold) | |
| Pipeline metrics methodology → Stage criteria template | Composition synthesis from Salesforce + HubSpot stage criteria best practices | |
| Forecasting methodology → Three-bucket discipline | Clari three-bucket methodology (Commit / Best Case / Pipeline) | |
| Forecasting methodology → Commit accuracy tracking | Clari + BoostUp commit-accuracy benchmarks + per-AE tracking methodology | |
| Forecasting methodology → Snapshot diff | Composition synthesis from Clari snapshot + Sheets pivot patterns | |
| Territory planning playbook → Salesforce TM2 | Salesforce Territory Management 2.0 documentation | |
| Territory planning playbook → K-means clustering | sklearn documentation + industry-standard territory balancing methodology | |
| Rep performance dashboard playbook → Salesforce CRMA dataset deploy | Salesforce CRMA REST documentation + SFDX wave commands | |
| Rep performance dashboard playbook → Looker LookML patterns | Looker documentation + standard sales-explore patterns | |
| Stalled-deal alert spec | Gong stalled-deal research + Salesforce activity tracking + Slack API documentation | |
| Stalled-deal alert spec → Engagement signal sources | Salesforce activity + Gong call + Gong sentiment + email engagement + calendar engagement + champion engagement + multi-thread depth + days-in-stage signals | |
| Deal desk discount approval matrix | Industry-standard discount tier matrix (4 tiers) + Salesforce Approval Process documentation | |
| Deal desk approval SLA tracking | Composition synthesis from Salesforce Approval Process + Slack escalation patterns | |
| Win/loss reporting playbook → Quarterly rollup query | dbt + warehouse SQL patterns + Clozd win/loss methodology | |
| Win/loss reporting playbook → Drift detection patterns | Composition synthesis from win/loss trend analysis + competitor mention rate tracking | |
| Sales tech stack audit playbook → Utilization scoring | OpenView SaaS tech stack methodology + tool admin API documentation | |
| Sales tech stack audit playbook → Kill/keep/renegotiate matrix | Industry-standard utilization threshold guidance | |
| Ramp-to-quota analysis playbook → Cohort table | Composition synthesis from Gong sales ramp research + SalesHood methodology + pandas patterns | |
| Sales enablement infrastructure playbook → Highspot tag taxonomy | Highspot documentation + industry-standard enablement tag taxonomy (stage, persona, industry, competitor, format) | |
| Sales enablement infrastructure playbook → Orphan quarantine | Composition synthesis from enablement-platform best practices | |
| SalesOps onboarding runbook | Composition synthesis from SalesOps practitioner standard onboarding plan (4-week ramp) | |

---

## Notes on authored-from-synthesis

Sections built from composition synthesis on top of vendor + methodology references:

- **Three opening convictions in soul.md** — synthesize three load-bearing rules from three different sources (stage-definitions-foundation from Salesforce + Gong + HubSpot validation patterns, dispute-time-burn-20% from industry surveys + Spiff / CaptivateIQ help center, CRM-source-of-truth from Validity + Salesforce best practices) into a memorable triad.
- **SalesOps technology categories** — names specific CRMs / ICM / CPQ / forecasting / routing / dedup / enrichment / territory / enablement / analytics / warehouse / deal desk vendors from industry sources. Listing common tools is industry knowledge, not invented.
- **Commission plan template (YAML)** — composition synthesis of common Spiff + QuotaPath + CaptivateIQ plan structure (base rate, accelerators, SPIFs, clawbacks, draws); specific YAML keys are operational choices that map to industry-standard plan fields.
- **Commission dispute audit-trail template (5-section)** — composition synthesis from Spiff + CaptivateIQ dispute API + audit-log structure; the 5-section breakdown (Filer / Claim / Source-of-truth chain / Discrepancy / Resolution + Plan changes) is operational glue.
- **Discount approval tier matrix (4 tiers)** — industry-standard tier definitions (< 10% / 10-20% / 20-30% / > 30%); specific SLA hours (24/48/72/96) are operational choices based on common practice.
- **Stage criteria template** — composition synthesis combining Salesforce validation rule patterns + HubSpot Workflow conditions + MEDDIC scoring; the entry/exit criteria format is operational glue.
- **Velocity formula** — Sales Velocity is a well-known formula (Win × Deals × Value / Cycle days); specific weights are industry-standard.
- **Stage conversion % numbers** — example numbers (40% / 55% / 60% / 70% / 75%) are illustrative midpoints from industry benchmarks; not specific to any company.
- **Forecasting snapshot diff workflow** — composition synthesis from Clari snapshot patterns + Sheets pivot patterns; the diff + slippage / pull-in detection is operational glue.
- **Territory planning K-means example** — sklearn documentation provides the algorithm; the territory balancing methodology (similar TAM + similar account count) is operational glue.
- **Highspot tag taxonomy** — composition synthesis of industry-standard enablement taxonomy (stage / persona / industry / competitor / format); specific tag values are illustrative.
- **SalesOps onboarding runbook (4-week)** — composition synthesis from SalesOps practitioner standard onboarding plan; specific weekly tasks are operational glue.
- **First-conversation PROACTIVE.md self-init** — standard pattern from METHODOLOGY.md with SalesOps-specific routine questions (primary CRM, commission tool, biggest pain).

No domain claims, performance benchmarks, or vendor capabilities were invented. All benchmarks come from vendor documentation or industry-standard sources cited above.

---

## How to update this agent

1. Re-fetch source files / vendor API docs cited in `reference/INVENTORY.md`
2. Diff against previous versions to see what changed
3. Update corresponding sections of `soul.md` and `role.md`
4. Update this `SOURCES.md` if section names or source URLs changed
5. Re-run `build.py` to regenerate `dist/sales-ops.craftbot`

---

## SOTA tool sources (June 2026)

These sources back the `role.md → SOTA tool reference (June 2026)` section, the `reference/SOTA_USE_CASES.md` per-use-case mapping, and the 20 bundled skill packs in `skills/` (Round 2). Each skill pack's `SKILL.md` will have a `## Sources` section duplicating + extending these.

| Tool | Source URL | Used for |
|---|---|---|
| Salesforce Metadata API | https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/ | `skills/salesforce-admin-custom-fields-flows/SKILL.md` — custom fields, validation, flows deploy |
| Salesforce Tooling API | https://developer.salesforce.com/docs/atlas.en-us.api_tooling.meta/api_tooling/ | `skills/salesforce-admin-custom-fields-flows/SKILL.md` — runtime metadata read, field-usage audit |
| Salesforce CLI (SFDX) | https://developer.salesforce.com/tools/salesforcecli | `skills/salesforce-admin-custom-fields-flows/SKILL.md` — `sf project deploy`, `sf data query`, `sf wave dataset deploy` |
| Salesforce CPQ Developer Guide | https://developer.salesforce.com/docs/atlas.en-us.cpq_dev_api.meta/cpq_dev_api/ | `skills/salesforce-cpq-conga-dealhub/SKILL.md` — CPQ products, bundles, pricing rules, approval rules |
| Salesforce CRMA / Einstein Analytics REST | https://developer.salesforce.com/docs/atlas.en-us.bi_dev_guide_rest.meta/bi_dev_guide_rest/ | `skills/rep-performance-dashboards/SKILL.md` — dataset + dashboard deploy |
| Salesforce Approval Process | https://help.salesforce.com/s/articleView?id=sf.approvals_intro.htm | `skills/deal-desk-discount-approval/SKILL.md` — discount tier approval routing |
| Salesforce Account Hierarchy | https://help.salesforce.com/s/articleView?id=sf.account_hierarchy.htm | `skills/contact-account-hierarchy-maintenance/SKILL.md` — parent-child-sibling account mgmt |
| Salesforce Territory Management 2.0 | https://help.salesforce.com/s/articleView?id=sf.tm2_intro.htm | `skills/territory-planning-assignment/SKILL.md` — native territory enforcement |
| Salesforce Validation Rules | https://help.salesforce.com/s/articleView?id=sf.validation_rules.htm | `skills/salesforce-admin-custom-fields-flows/SKILL.md` — stage criteria + required-field gating |
| HubSpot Operations Hub | https://developers.hubspot.com/docs/api/automation/workflows | `skills/hubspot-ops-hub-workflows/SKILL.md` — workflow + custom-coded actions |
| HubSpot Properties API | https://developers.hubspot.com/docs/api/crm/properties | `skills/salesforce-admin-custom-fields-flows/SKILL.md` — schema audit cross-CRM |
| HubSpot Data Sync (PieSync successor) | https://developers.hubspot.com/docs/api/crm/data-sync | `skills/hubspot-ops-hub-workflows/SKILL.md` — data sync mapping |
| HubSpot Approvals | https://knowledge.hubspot.com/approvals | `skills/deal-desk-discount-approval/SKILL.md` — HubSpot-side approval routing |
| Salesloft Admin API | https://developers.salesloft.com/api.html | `skills/salesloft-outreach-tech-stack-admin/SKILL.md` — cadence governance + user provisioning |
| Outreach Admin API | https://developers.outreach.io/api/ | `skills/salesloft-outreach-tech-stack-admin/SKILL.md` — sequence governance + user provisioning |
| Gong API | https://app.gong.io/settings/api/documentation | `skills/salesloft-outreach-tech-stack-admin/SKILL.md` — scorecards + smart trackers + sentiment for stall alerts |
| Spiff (Salesforce) | https://docs.salesforcespiff.com/ | `skills/commission-spiff-quotapath-captivateiq/SKILL.md` + `skills/commission-dispute-audit-trail/SKILL.md` — ICM plan + dispute |
| QuotaPath | https://docs.quotapath.com/ | `skills/commission-spiff-quotapath-captivateiq/SKILL.md` — mid-market ICM |
| CaptivateIQ | https://help.captivateiq.com/ | `skills/commission-spiff-quotapath-captivateiq/SKILL.md` + `skills/commission-dispute-audit-trail/SKILL.md` — enterprise ICM + dispute |
| Performio | https://www.performio.co/ | Alt ICM |
| Xactly | https://www.xactlycorp.com/ | Alt ICM (enterprise) |
| Everstage | https://www.everstage.com/ | Alt ICM (mid-market) |
| Conga CPQ | https://docs.conga.com/ | `skills/salesforce-cpq-conga-dealhub/SKILL.md` — Apttus-derived CPQ |
| DealHub CPQ | https://docs.dealhub.io/ | `skills/salesforce-cpq-conga-dealhub/SKILL.md` — DealHub CPQ + deal-desk module |
| Pricefx | https://www.pricefx.com/ | Alt pricing/CPQ |
| Subskribe | https://www.subskribe.com/ | Modern SaaS CPQ |
| LeanData | https://docs.leandata.com/ | `skills/lead-routing-leandata-chili-piper/SKILL.md` + `skills/duplicate-mgmt-leandata-dedupe/SKILL.md` — routing + dedup (Salesforce-native) |
| Chili Piper API | https://docs.chilipiper.com/api/ | `skills/lead-routing-leandata-chili-piper/SKILL.md` — inbound calendar router |
| Distribute | https://www.distribute.so/ | `skills/lead-routing-leandata-chili-piper/SKILL.md` — HubSpot-focused routing |
| Cloudingo | https://cloudingo.com/ | `skills/duplicate-mgmt-leandata-dedupe/SKILL.md` — Salesforce fuzzy dedup |
| DupeBlocker (Validity) | https://www.validity.com/products/dupeblocker/ | `skills/duplicate-mgmt-leandata-dedupe/SKILL.md` — Validity dedup |
| Apollo.io API | https://docs.apollo.io/reference/people-search | `skills/data-enrichment-zoominfo-apollo-clay/SKILL.md` — enrichment waterfall baseline |
| ZoomInfo API | https://api-docs.zoominfo.com/ | `skills/data-enrichment-zoominfo-apollo-clay/SKILL.md` — gaps + Scoops intent |
| Clay.com API | https://clay.com/docs/api | `skills/data-enrichment-zoominfo-apollo-clay/SKILL.md` — multi-source orchestration |
| Demandbase | https://www.demandbase.com/intent/ | `skills/data-enrichment-zoominfo-apollo-clay/SKILL.md` — ABM intent overlay |
| LeadIQ | https://leadiq.com/ | Alt enrichment (chrome-extension) |
| Cognism | https://www.cognism.com/ | Alt enrichment (EU-compliant) |
| D&B Direct+ | https://www.dnb.com/business-credit/dun-and-bradstreet-direct.html | `skills/contact-account-hierarchy-maintenance/SKILL.md` — account hierarchy refresh |
| Clari | https://www.clari.com/blog/sales-forecasting-methods/ | `skills/forecasting-clari-boostup-aviso/SKILL.md` — three-bucket forecasting + commit accuracy |
| BoostUp | https://boostup.ai/ | `skills/forecasting-clari-boostup-aviso/SKILL.md` — mid-market forecast alt |
| Aviso | https://aviso.com/ | `skills/forecasting-clari-boostup-aviso/SKILL.md` — AI-driven forecast alt |
| InsightSquared (Mediafly) | https://www.insightsquared.com/ | Alt revenue intelligence |
| Gong Forecast | https://www.gong.io/forecast/ | `skills/forecasting-clari-boostup-aviso/SKILL.md` — call-data-integrated forecast |
| Anaplan | https://www.anaplan.com/products/sales-planning/ | `skills/territory-planning-assignment/SKILL.md` — territory + quota planning (enterprise) |
| Fullcast | https://www.fullcast.com/ | `skills/territory-planning-assignment/SKILL.md` — mid-market territory planning |
| Highspot Developer docs | https://developers.highspot.com/ | `skills/sales-enablement-infrastructure-highspot-showpad/SKILL.md` — content + spots + analytics |
| Showpad Developer docs | https://developer.showpad.com/ | `skills/sales-enablement-infrastructure-highspot-showpad/SKILL.md` — asset + tag taxonomy + analytics |
| Seismic Developer Portal | https://developer.seismic.com/ | `skills/sales-enablement-infrastructure-highspot-showpad/SKILL.md` — enterprise content + LiveDoc |
| Mindtickle | https://www.mindtickle.com/ | `skills/ramp-to-quota-analysis/SKILL.md` — training completion tracking |
| Looker | https://docs.looker.com/reference/api-and-integration | `skills/rep-performance-dashboards/SKILL.md` — LookML + dashboards |
| Sigma Computing | https://help.sigmacomputing.com/ | `skills/rep-performance-dashboards/SKILL.md` — spreadsheet-native warehouse dashboards |
| Hex | https://learn.hex.tech/ | `skills/rep-performance-dashboards/SKILL.md` — notebook + dashboard hybrid |
| dbt | https://docs.getdbt.com/ | `skills/pipeline-metrics-velocity-conversion/SKILL.md` — transformation layer for warehouse-modeled `fct_opportunities` |
| Gong stalled-deal research | https://www.gong.io/blog/stalled-deal/ | `skills/stalled-deal-alerts-engagement-signals/SKILL.md` — 1.5× median + 14d inactivity threshold |
| Gong win/loss research | https://www.gong.io/blog/win-loss-analysis/ | `skills/win-loss-reporting-at-scale/SKILL.md` — rollup methodology |
| Gong sales ramp research | https://www.gong.io/blog/sales-ramp/ | `skills/ramp-to-quota-analysis/SKILL.md` — ramp curve methodology |
| Clozd | https://www.clozd.com/ | `skills/win-loss-reporting-at-scale/SKILL.md` — win/loss methodology research |
| OpenView SaaS sales tech stack | https://www.openview.com/saas-sales-tech-stack/ | `skills/sales-tech-stack-consolidation-audit/SKILL.md` — utilization audit framework |
| rapidfuzz (Python) | https://github.com/maxbachmann/RapidFuzz | `skills/duplicate-mgmt-leandata-dedupe/SKILL.md` — Python fuzzy match fallback |
| sklearn (KMeans) | https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html | `skills/territory-planning-assignment/SKILL.md` — K-means territory clustering |
| Maton API gateway | https://gateway.maton.ai/ | `api-gateway` default skill — managed OAuth for 100+ apps including Salesforce, HubSpot, Spiff, QuotaPath, CaptivateIQ, Salesforce CPQ, Conga, DealHub, LeanData, Chili Piper, Apollo, ZoomInfo, Clay, Demandbase, Clari, BoostUp, Aviso, Highspot, Showpad, Seismic, Mindtickle, Anaplan, Looker, Sigma, Hex |
| Native CraftBot MCPs | `app/config/mcp_config.json` | gmail-mcp / outlook-mcp / slack-mcp / ms-teams-mcp / notion-mcp / linear-mcp / jira-mcp / postgresql-mcp / posthog-mcp / mixpanel-mcp / amplitude-mcp / playwright-mcp / firecrawl-mcp / brave-search / stripe-mcp / imagegen-mcp / canva-mcp / figma-mcp |

Total: 20 bundled skill packs + 19 native MCPs + 100+ third-party APIs proxied via `api-gateway` covering ≥95% of `USE_CASES.md` documented use cases. See `reference/SOTA_USE_CASES.md` for the per-use-case confidence map.
