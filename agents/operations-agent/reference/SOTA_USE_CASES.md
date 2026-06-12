# operations-agent — SOTA Use-Case Mapping (June 2026)

Per-use-case mapping of the SOTA approach, exact agent execution path (MCP / CLI / API), authoritative source, and confidence flag. Cross-references the bundled skill packs in `skills/` (created in Round 2).

Confidence legend:
- ✓ — direct execution path; free or generous free tier; no manual intervention beyond the recipient providing an API key the agent prompts for once.
- ⚠ — direct execution path but requires user-supplied paid API key or platform invite approval.
- ✗ — execution requires manual user step or a paywalled portion the agent cannot fully automate today.

---

## Hiring pipeline (ATS workflow: sourcing → screen → interview → offer)

- **SOTA approach:** Greenhouse (7,500+ customers, #1 G2 Winter 2026, 600+ integrations) is the structured-hiring standard. Ashby (founded 2019, modern architecture, deepest analytics — pipeline velocity, source attribution, interviewer calibration) for data-obsessed growth-stage teams. Lever for ATS + CRM in one. Workable / Pinpoint / Recruitee / SmartRecruiters as alts.
- **Agent execution path:** `cli-anything` → REST per ATS (`GREENHOUSE_API_KEY`, `LEVER_API_KEY`, `ASHBY_API_KEY`). All three publish public REST APIs for candidate CRUD, jobs, stages, applications, scorecards. Unified.to provides a normalized cross-ATS schema if multi-platform. Public job-posting feeds: Ashby `includeCompensation=true`, Lever JSON with team/department/location filters. Bundled skill: `hiring-pipeline-greenhouse-ashby-lever`.
- **Source:** https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable · https://www.index.dev/blog/greenhouse-vs-lever-vs-ashby-ats-comparison · https://cavuno.com/blog/ats-platforms-public-job-posting-apis
- **Confidence:** ⚠ (paid API key recipient-provided; ATS keys are seat-tied)

## Employee onboarding flow (Day 1, Week 1, 30/60/90)

- **SOTA approach:** HRIS-coupled onboarding flows: Rippling (provisions Google Workspace / Slack / GitHub / Notion on hire), Gusto Onboarding, HiBob (mid-market culture-led), BambooHR. Dedicated: Sapling (Kallidus), Click Boarding, Enboarder, Tydy. Lattice Grow for performance-tied onboarding.
- **Agent execution path:** Provision via Rippling / Gusto / HiBob API + downstream account creation through `google-workspace-mcp` + `slack-mcp` + `github` + `notion-mcp`. Day-1 checklist + 30/60/90 milestone tracking in `notion-mcp` or `linear-mcp`. Bundled skill: `onboarding-offboarding-workflows`.
- **Source:** https://www.hibob.com/blog/rippling-vs-gusto-vs-hibob/ · https://johngalt-finance.com/gusto-vs-justworks-vs-rippling-payroll-hr-2026/
- **Confidence:** ⚠ (HRIS paid key recipient-provided)

## Employee offboarding flow (exit interview, access revocation, equipment return)

- **SOTA approach:** Same HRIS-coupled platforms drive offboarding triggers: deprovision SaaS accounts (SCIM via Okta / WorkOS / JumpCloud), reclaim device (Kandji/Iru / Jamf / Intune / Rippling IT remote wipe), exit interview via Typeform / Tally / Lattice exit surveys.
- **Agent execution path:** Trigger: HRIS termination event → `cli-anything` calls deprovision endpoints across SCIM-connected apps; device wipe via MDM API; exit interview survey via Typeform / Tally / `gmail-mcp`. Bundled skill: `onboarding-offboarding-workflows`.
- **Source:** https://workos.com/blog/best-scim-providers-for-automated-user-provisioning-in-2026 · https://www.rippling.com/blog/rippling-mdm-review
- **Confidence:** ⚠ (paid keys; device control via MDM platform)

## Performance review cycle (annual / biannual / continuous)

- **SOTA approach:** Lattice (default for growth-stage; goals + reviews + feedback + compensation + core HR), 15Five ($9-15 PEPM; week-to-deploy), Culture Amp (research-driven engagement DNA), Leapsome (widest breadth — performance + surveys + recognition + OKRs + onboarding + learning). EU: Leapsome GDPR-compliant.
- **Agent execution path:** `cli-anything` → REST per platform. Lattice / 15Five / Culture Amp / Leapsome all expose public APIs for reviews, goals, surveys. Cycle authoring: agent drafts the calibration cadence + question bank; pushes to platform. Bundled skill: `performance-review-cycle-lattice-15five`.
- **Source:** https://www.performancereviewssoftware.com/blog/lattice-vs-culture-amp-vs-15five-comparison/ · https://feedbackpulse.com/lattice-alternatives
- **Confidence:** ⚠ (paid keys)

## 1:1 cadence + manager training

- **SOTA approach:** Lattice 1:1s, 15Five Weekly Check-ins, Officevibe Pulse, Soapbox / Hypercontext for 1:1 templates. Manager training: LifeLabs Learning, Lattice Grow, Reflektive (now Lattice). AI coaches: Wisq, Marlee.
- **Agent execution path:** Drafts 1:1 agenda templates + cadence schedule in `notion-mcp` / `linear-mcp` / `google-calendar-mcp`; pushes to platform via REST. Bundled skill: `performance-review-cycle-lattice-15five` (1:1 section).
- **Source:** https://www.outsail.co/post/lattice-vs-15five-vs-culture-amp-performance
- **Confidence:** ✓

## Compensation philosophy + bands

- **SOTA approach:** Pave (compensation benchmarking, 11M+ data points), Carta Compensation (Carta Total Comp), Comparably, Levels.fyi (engineering), Radford / Mercer (enterprise). Bands authoring per role × geography × stage.
- **Agent execution path:** `cli-anything` → Pave / Carta Total Comp / Comparably REST when recipient has access. Bands authored in `xlsx` + `notion-mcp`. Bundled skill: `compensation-philosophy-bands`.
- **Source:** https://www.pave.com/ · https://carta.com/total-comp/
- **Confidence:** ⚠ (paid keys; Levels.fyi public for engineering)

## Employee handbook authoring + policies

- **SOTA approach:** Notion (most-deployed handbook editor in 2026), Zenefits (handbook builder), Lattice (handbook builder), Trainual (combines SOPs + training + handbook). For policy law-checking: Gusto / Rippling / Justworks ship templated state-specific handbooks (CA, NY, MA, IL — non-binding); LawPay / Mineral HR for legally vetted policies.
- **Agent execution path:** Authors handbook sections in `notion-mcp` / `docx` / `markdown-converter`. Multi-state policy coverage from Gusto / Rippling templates via REST. Bundled skill: `employee-handbook-policies`.
- **Source:** https://www.trainual.com/ · https://gusto.com/
- **Confidence:** ✓ (authoring local; recipient supplies HRIS for templated policies)

## PTO / vacation policy + tracking

- **SOTA approach:** Built into HRIS (Gusto / Rippling / HiBob / BambooHR). Dedicated: TimeOff.com, Vacation Tracker (Slack-native), Trinet.
- **Agent execution path:** Drafts policy → pushes to HRIS PTO module via REST. Slack-native trackers via `slack-mcp` + REST. Bundled skill: `employee-handbook-policies` (PTO section).
- **Source:** https://www.hibob.com/blog/rippling-vs-gusto-vs-hibob/
- **Confidence:** ⚠ (HRIS paid key)

## Remote / hybrid / in-office policy

- **SOTA approach:** Policy authoring in Notion / handbook builder; coordination via Robin (desk + room booking, 2026 Gartner MQ Leader), Envoy (visitors + delivery), Tactic, Skedda, Eden Workplace. AI workplace operations: Robin AI-powered platform.
- **Agent execution path:** Policy in `notion-mcp` / `docx`. Robin / Envoy via `cli-anything` REST for booking patterns. Bundled skill: `employee-handbook-policies` + `office-management-robin-envoy`.
- **Source:** https://archieapp.co/blog/envoy-vs-robin/ · https://robinpowered.com/
- **Confidence:** ⚠ (paid keys)

## Vendor evaluation framework (build vs buy vs partner)

- **SOTA approach:** Vendor evaluation matrix: business need + total cost (TCO = license + integration + training + opportunity cost) + security posture (SOC 2 / ISO 27001 / DPA) + lock-in risk + roadmap fit. Vendr / Tropic benchmark databases ($18B+ deals at Vendr, 130K+ transactions). Build vs buy frameworks: Joel Spolsky "Strategy Letter V" core/context test.
- **Agent execution path:** Drafts evaluation rubric in `xlsx` / `notion-mcp`; pulls market benchmarks via Vendr / Tropic / Spendflo REST when recipient has access. Bundled skill: `vendor-evaluation-negotiation`.
- **Source:** https://www.spendhound.com/blog/best-saas-spend-management-software · https://www.tropicapp.io/compare/spendflo
- **Confidence:** ✓ (authoring local; benchmarks via paid platform)

## SaaS spend audit + rationalization (Vendr / Tropic / Spendflo playbook)

- **SOTA approach:** Tropic 2025 benchmark: top-10 vendors = 74% of SaaS spend. SpendHound / Zylo / CloudEagle for spend visibility; Cledara (EU); Productiv / Torii for usage-based optimization (SSO log cross-referencing); Sastrify (EU); Vertice for combined procurement + spend.
- **Agent execution path:** Spend pull from corp card (Ramp / Brex APIs) + Xero/QBO + SSO platform login logs (Okta / WorkOS) → cross-reference for unused seats → duplicate detection. `cli-anything` REST per platform. Bundled skill: `saas-spend-audit-vendr-tropic-spendflo`.
- **Source:** https://www.tropicapp.io/reports/software-spending-trends-2025 · https://najar.ai/blog/spendflo-alternatives
- **Confidence:** ✓ (data sources free; paid platforms optional)

## Software contract negotiation

- **SOTA approach:** Vendr (130K+ deals, AI negotiation agents + buyer team), Tropic (managed buying), Spendflo (AI + managed sourcing). DIY playbook: BATNA + competitive pricing data + multi-year leverage + renewal alarm 90 days out + price-protection clauses + auto-renewal removal.
- **Agent execution path:** Drafts negotiation playbook + counter-letter templates in `docx` / `notion-mcp`. Pulls benchmark pricing from Vendr / Tropic / Spendflo REST. Bundled skill: `vendor-evaluation-negotiation`.
- **Source:** https://www.spendhound.com/blog/vendr-alternatives
- **Confidence:** ⚠ (benchmark data paid; templated playbook free)

## Procurement playbook (intake → approval → contract → renewal)

- **SOTA approach:** Ramp Procurement, Brex Procurement (built-in to corp-card platforms); Coupa (enterprise); Vendr / Tropic / Spendflo for managed procurement. Intake forms via Typeform / Tally / Notion forms. Renewal tracking via Vendr / Tropic / SpendHound / Cledara renewal calendar.
- **Agent execution path:** Intake form authoring in `cli-anything` + Typeform / Tally REST. Approval workflow in `linear-mcp` / `notion-mcp`. Contract storage in `google-drive-mcp` / `notion-mcp`. Renewal calendar → `google-calendar-mcp` + Slack reminders. Bundled skill: `procurement-playbook-intake-renewal`.
- **Source:** https://ramp.com/procurement/ · https://thectoclub.com/tools/best-saas-spend-management-software/
- **Confidence:** ✓

## Internal tool building (Retool / Tooljet / Budibase / Appsmith)

- **SOTA approach:** Retool (mature, polished UX, higher cost — best for engineering teams with budget); ToolJet (open-source, AI-native, Python support — 2026 "best Retool open-source alt"); Budibase (no-code, auto-generated CRUD, built-in DB — fastest); Appsmith (JS-heavy code-first — open source); Internal.io / Atom / Stacker / Softr (Airtable wrappers) for non-technical builders.
- **Agent execution path:** `cli-anything` → npm/uvx install per platform OR REST for hosted instances. Retool: `npm install -g @retool/cli`, `retool create`. ToolJet self-host via Docker. Budibase: `npm install budibase` + Postgres. Code authoring via `cli-anything` + `frontend-design`. Bundled skill: `internal-tools-retool-tooljet-budibase`.
- **Source:** https://blog.tooljet.com/appsmith-vs-budibase-vs-tooljet/ · https://www.openhelm.ai/blog/retool-vs-budibase-vs-appsmith-internal-ai-tools · https://openalternative.co/alternatives/retool
- **Confidence:** ✓ (open-source self-host; cloud paid optional)

## Workflow automation (Zapier / Make / n8n / Pipedream)

- **SOTA approach:** Zapier (8,000+ apps; Zapier Agents for autonomous tasks); Make.com (3,000+ apps; Maia AI assistant + agent builder beta); n8n 2.0 Jan 2026 (native LangChain + 70+ AI nodes; 80-90% cheaper for high-volume; self-host = no execution limits); Pipedream (developer-friendly); Workato / Tray.io (enterprise); Bardeen / Relay.app (AI-first); Apple Shortcuts (personal).
- **Agent execution path:** n8n self-host via Docker (`docker run n8nio/n8n`) — agent authors workflow JSON. Zapier / Make REST APIs for hosted. `cli-anything` for all. Bundled skill: `workflow-automation-zapier-make-n8n`.
- **Source:** https://medium.com/@automation.labs/zapier-vs-make-vs-n8n-in-2026-where-ai-agents-actually-fit-1edbbeff85f3 · https://blog.n8n.io/best-ai-workflow-automation-tools/ · https://hatchworks.com/blog/ai-agents/n8n-vs-zapier/
- **Confidence:** ✓ (n8n self-host free)

## Business process documentation (Scribe / Tango / Whale / Trainual)

- **SOTA approach:** Auto-capture: Scribe (live screen recording → step-by-step guides), Tango (screenshot annotation auto-guide), Whale (Step Recorder + AI SOP draft). Training-focused: Trainual (org knowledge + SOPs + training + tracking). Berrycast (Loom-style).
- **Agent execution path:** Documentation authoring locally in `docx` / `notion-mcp` / `markdown-converter`. Scribe / Tango / Whale REST for SOP push when recipient has account. Bundled skill: `process-documentation-scribe-tango`.
- **Source:** https://www.tango.ai/blog/scribe-alternatives · https://scribe.com/library/scribe-vs-tango · https://www.docsie.io/blog/articles/scribe-vs-tango-comparison-2026/
- **Confidence:** ✓ (local docs free; auto-capture platforms paid)

## SSO / IAM setup (Okta / JumpCloud / WorkOS / Stytch / Auth0)

- **SOTA approach:** Stage-based: Pre-PMF / seed (<$1M ARR) → Stytch + SSOJet; Series A-B → Auth0 (decade leader); Series A+ B2B SaaS with enterprise deals → WorkOS (turns 4-week SAML integration into 4-day); Enterprise workforce + customer in one → Okta; Open directory (IAM + MDM + infra in one) → JumpCloud; Scalekit handles SAML/OIDC across all providers.
- **Agent execution path:** `cli-anything` → platform REST + SCIM API for user provisioning. Okta SCIM 2.0; JumpCloud REST; WorkOS Sessions + Directory Sync; Stytch B2B Organizations. SAML config CLI-friendly. Bundled skill: `sso-okta-jumpcloud-workos`.
- **Source:** https://securityboulevard.com/2026/06/auth0-vs-okta-vs-stytch-vs-workos-vs-ssojet-2026-a-buyer-stage-framework/ · https://workos.com/blog/best-scim-providers-for-automated-user-provisioning-in-2026 · https://www.siit.io/tools/comparison/jumpcloud-vs-okta
- **Confidence:** ⚠ (paid keys; setup CLI-friendly)

## Device / endpoint management (Kandji-Iru / Jamf / Intune / Rippling IT)

- **SOTA approach:** Apple-only fleet → Jamf Pro (deep) or Iru/Kandji (modern; rebranded Oct 2025 — six-product unified platform across identity + endpoint + EDR + vuln + compliance + trust center). Mixed Win/Mac → Microsoft Intune (transitioning to Apple DDM) or Hexnode. Lifecycle-tied → Rippling IT (provisions on hire / deprovisions on offboard). Android → Esper / Scalefusion / Mosyle.
- **Agent execution path:** `cli-anything` → platform REST per MDM. Kandji/Iru API: device CRUD, blueprint authoring, OS update enforcement. Jamf Pro Classic + Pro API. Intune via Microsoft Graph. Rippling IT via Rippling API. Bundled skill: `device-management-kandji-jamf-intune`.
- **Source:** https://technologymatch.com/blog/intune-vs-jamf-pro-vs-kandji-the-it-leaders-guide-to-apple-management-in-2026 · https://www.rippling.com/blog/rippling-mdm-review · https://www.iru.com/compare/kandji-alternatives
- **Confidence:** ⚠ (paid keys)

## IT support tier-1 / runbook

- **SOTA approach:** Help desks: Linear Triage, Jira Service Management, Freshdesk, Zendesk, Halo ITSM. Runbooks in Notion / Confluence / Slab / Tettra. AI-first: Moveworks / Aisera (enterprise). Slack-native: Tettra (Slack Q&A → KB), Stack Overflow for Teams.
- **Agent execution path:** Triage in `linear-mcp` / `jira-mcp`. Runbook authoring in `notion-mcp` / `obsidian-mcp`. Slack inquiries via `slack-mcp`. Bundled skill: `runbook-authoring-operational-incident`.
- **Source:** https://www.taskade.com/blog/ai-wiki-tools · https://coworker.ai/blog/knowledge-management-tools
- **Confidence:** ✓

## Payroll setup (Gusto / Rippling / Deel / Justworks)

- **SOTA approach:** SMB (<50 employees) → Gusto ($40/mo + $6/employee; multi-state; contractors). PEO with enterprise benefits for <50 → Justworks. 50+ employees, distributed, HRIS+IT+payroll in one → Rippling. Global contractors / EOR → Deel. HRIS-only (BYO payroll) → HiBob.
- **Agent execution path:** `cli-anything` → platform REST per HRIS. Gusto Embedded API; Rippling Public API; Deel API (best EOR API surface in industry per 2026 review); HiBob Public API. Bundled skill: `payroll-gusto-rippling-deel`.
- **Source:** https://johngalt-finance.com/gusto-vs-justworks-vs-rippling-payroll-hr-2026/ · https://www.hibob.com/blog/rippling-vs-gusto-vs-hibob/
- **Confidence:** ⚠ (paid keys recipient-provided)

## PEO / EOR for global hiring (Deel / Remote / Oyster / Pebl)

- **SOTA approach:** Deel (150+ countries, treats API as a product — only EOR with public docs + sandbox + webhooks pre-contract; full workforce platform). Remote.com (100+ countries; straightforward; owned entities + partners). Oyster HR (180+ countries; employee experience focus). Pebl (formerly Velocity Global, rebranded Sept 2025 — AI hiring + 48-hour onboarding + Alfie AI assistant). G-P (Globalization Partners; enterprise). Multiplier (alt).
- **Agent execution path:** `cli-anything` → Deel API (`DEEL_TOKEN`) with sandbox + webhooks. Remote API. Oyster API. Pebl API. Bundled skill: `peo-eor-global-hiring-deel-remote-oyster-gp`.
- **Source:** https://whichpayroll.com/features/eor-api-access · https://www.deel.com/blog/deel-vs-remote-honest-employer-of-record-service-comparison/ · https://nativeteams.com/blog/deel-vs-oyster · https://alcor.com/velocity-global-alternatives/
- **Confidence:** ⚠ (paid keys; Deel has best dev surface)

## Travel + expense policy + tooling (Navan / Brex / Ramp / Expensify)

- **SOTA approach:** Brex + Navan partnership (BrexPay for Navan launched Oct 2024 — Brex cards native in Navan with per-booking virtual cards + automated reconciliation across 50+ currencies). Capital One closed Brex acquisition April 2026 ($5.15B). Navan AI assistant Ava + Expense Chat (94/100 CSAT beta); 70%+ corp-card txns zero manual intervention. Ramp Travel; SAP Concur; Pleo (EU); Mesh Payments; Center.
- **Agent execution path:** `cli-anything` → Ramp / Brex / Navan / Expensify REST. Policy authoring in `docx` / `notion-mcp`. Approval routing via Slack / email. Bundled skill: `travel-expense-policy-navan-ramp-brex`.
- **Source:** https://ramp.com/blog/navan-vs-brex-vs-ramp · https://www.brex.com/journal/press/brex-pay-for-navan · https://receiptor.ai/blog/brex-alternatives-after-the-capital-one-acquisition-2026 · https://navan.com/blog/best-travel-analytics-tools-ai
- **Confidence:** ⚠ (paid keys)

## Corporate card policy (Brex / Ramp / Navan)

- **SOTA approach:** Ramp (control-first design — customizable card limits, automated policy enforcement, AI duplicate/anomaly flagging). Brex (multi-entity 50+ countries; Capital One owned post-April 2026). Navan Connect (cards link to existing banks). Policy: limit + MCC restrictions + receipt threshold + approval thresholds.
- **Agent execution path:** Card CRUD + policy authoring via Ramp / Brex API. `cli-anything` REST. Bundled skill: `travel-expense-policy-navan-ramp-brex` (card section).
- **Source:** https://ramp.com/blog/navan-vs-brex-vs-ramp · https://www.financebuzz.net/what-are-the-best-corporate-cards-for-businesses-in-2026/
- **Confidence:** ⚠ (paid keys)

## Business insurance audit (D&O, E&O, Cyber, EPLI, GL)

- **SOTA approach:** Startup-specific digital carriers: Vouch (web3 + AI-native protections; entirely digital), Embroker (Startup Package — D&O + E&O + Cyber + EPLI instant bundle), Newfront. Enterprise: Hartford, At-Bay (cyber leader), Sequoia, Coalition. Coverage stack: General Liability + Business Property + D&O + E&O + EPLI + Cyber + W/C. Median 2026 cyber premium: $2,968.
- **Agent execution path:** Coverage audit checklist authoring in `docx` / `xlsx`; quote-pull via Vouch / Embroker / Newfront REST when available. Bundled skill: `business-insurance-vouch-embroker-newfront`.
- **Source:** https://www.embroker.com/coverage/startup-insurance/ · https://www.vouch.us/blog/what-is-startup-business-insurance-and-why-do-i-need-it · https://www.svb.com/startup-insights/startup-strategy/startup-insurance-guide-for-founders/
- **Confidence:** ✓ (coverage audit free; quotes via broker)

## Office space management (Robin / Envoy / Tactic / Skedda)

- **SOTA approach:** Robin (2026 Gartner Magic Quadrant Leader for Workplace Experience Applications; AI-powered workplace ops; desk + room + parking booking). Envoy (visitor management leader). Tactic / Skedda / Eden Workplace alts. Hybrid coordination: desk booking + room booking + visitor + delivery.
- **Agent execution path:** `cli-anything` → Robin / Envoy REST for booking patterns + space analytics. Bundled skill: `office-management-robin-envoy`.
- **Source:** https://archieapp.co/blog/envoy-vs-robin/ · https://robinpowered.com/
- **Confidence:** ⚠ (paid keys)

## Business continuity / disaster recovery

- **SOTA approach:** BCP framework: business impact analysis (BIA) → recovery time objective (RTO) + recovery point objective (RPO) → DR plan per system tier. Cloud backup: AWS Backup, Azure Backup, GCP Backup-and-DR, Druva, Rubrik. Comms playbook: Slack / SMS (Twilio) / status page (Statuspage / Better Stack / Instatus). Tabletop exercises quarterly.
- **Agent execution path:** BCP authoring in `docx` / `notion-mcp`. Cloud backup via `aws-s3-mcp` / `cli-anything` AWS/GCP CLI. Comms via `slack-mcp` + `twilio-mcp`. Status page via `cli-anything` Statuspage/Better Stack REST. Bundled skill: `business-continuity-disaster-recovery`.
- **Source:** https://www.atlassystems.com/blog/vendor-risk-assessment-checklist-key-questions · https://nmsconsulting.com/vendor-risk-management-checklist/
- **Confidence:** ✓ (authoring + cloud APIs free / standard)

## Vendor risk assessment (DPA + security questionnaire + SOC 2)

- **SOTA approach:** Secureframe 2026 Benchmark: 73% companies use third-party audit reports (SOC 2); 70% use security questionnaires. SOC 2 vs questionnaires: SOC 2 = auditor attestation on control effectiveness; questionnaires = self-reported. DPA checklist: purpose + confidentiality + sub-processors + breach notice + audit + retention/deletion + assistance. Platforms: Whistic, OneTrust Vendorpedia, UpGuard, Drata Trust Center, Vanta Trust Center.
- **Agent execution path:** Questionnaire authoring in `docx` / `xlsx`. SOC 2 / ISO request via `gmail-mcp` to vendor security@. DPA drafting in `docx` (referring sibling `legal-counsel` for binding review). Trust center pull via `cli-anything` REST. Bundled skill: `vendor-risk-assessment-dpa`.
- **Source:** https://secureframe.com/blog/soc-2-vs-security-questionnaires · https://soc2auditors.org/insights/vendor-security-questionnaire-guide/ · https://copla.com/blog/third-party-risk-management/guide-to-vendor-security-and-risk-assessment-questionnaires/
- **Confidence:** ✓

## Data retention + deletion policy

- **SOTA approach:** Policy authoring + automation. GDPR Art. 17 (right to erasure) + CCPA delete-request workflows + SOC 2 CC6 / Trust Services. Tools: Vanta / Drata trust centers, OneTrust DSAR (Data Subject Access Request), Transcend, Osano.
- **Agent execution path:** Policy authoring in `docx` / `notion-mcp`. DSAR workflow in `linear-mcp` / `notion-mcp`. Per-system deletion via `cli-anything` + REST. Bundled skill: `vendor-risk-assessment-dpa` (data lifecycle section).
- **Source:** https://secureframe.com/blog/soc-2-compliance-checklist
- **Confidence:** ✓

## Internal knowledge base architecture (Notion / Slab / Tettra / Confluence)

- **SOTA approach:** 5-20 person teams → Slab (free tier 10 users; unified search across Slab + Slack + Drive + Notion); Slack-heavy teams → Tettra ($4/user; Slack Q&A → KB articles + AI routing). 50+ → Notion (Notion Agents — autonomous bots trained on teamspaces, e.g., HR Agent monitoring "Benefits" DB). Enterprise → Confluence (Rovo AI fully integrated 2026; 20+ pre-built agents). Slite (alt clean), GitBook (docs-focused), Document360 (KB-focused), BookStack (OSS self-host).
- **Agent execution path:** `notion-mcp` / `obsidian-mcp` for primary KB ops. `cli-anything` → Slab / Tettra / Confluence / Slite REST. Bundled skill: `internal-knowledge-base-notion-slab-tettra`.
- **Source:** https://www.buildmvpfast.com/blog/ai-internal-wiki-knowledge-base-notion-confluence-alternative-2026 · https://www.taskade.com/blog/ai-wiki-tools · https://slite.com/learn/knowledge-base-softwares · https://www.docsie.io/blog/articles/confluence-vs-notion-comparison-2026/
- **Confidence:** ✓

## Runbook authoring (operational + incident)

- **SOTA approach:** Operational runbooks: Notion / Confluence / Slab. Incident runbooks: PagerDuty Process Automation / Rundeck (now PagerDuty), Squadcast, Incident.io, Statuspage / Better Stack. Post-mortem: blameless template (Google SRE), 5-whys.
- **Agent execution path:** Runbook in `notion-mcp` / `obsidian-mcp` with grep-friendly H2/H3 per scenario. Incident: `cli-anything` → PagerDuty / Incident.io REST. Bundled skill: `runbook-authoring-operational-incident`.
- **Source:** https://incident.io/ · https://www.pagerduty.com/products/process-automation/
- **Confidence:** ✓

## AI policy / responsible-use guidelines

- **SOTA approach:** AI usage policy components: approved tools, data classification (PII / IP / confidential) usage tiers, prompt-injection defense, output review tier, vendor AI DPA. Frameworks: NIST AI RMF, ISO 42001, EU AI Act. Anthropic safe-use guidance. Tracking: Notion table per team + Whale / Trainual for training rollout.
- **Agent execution path:** Policy authoring in `docx` / `notion-mcp` per template. Approved-tool inventory in `xlsx` / Notion DB. Bundled skill: separate (Round 2 — covered under `employee-handbook-policies` AI section + `vendor-risk-assessment-dpa` AI DPA section in v1).
- **Source:** https://www.nist.gov/itl/ai-risk-management-framework · https://www.anthropic.com/responsible-use
- **Confidence:** ✓

## Compensation review cycle

- **SOTA approach:** Driver-based: market band + performance multiplier + tenure + budget envelope. Tools: Pave (live market data), Carta Total Comp, Lattice Compensation. Cadence: annual or semi-annual; calibration sessions for cross-team fairness.
- **Agent execution path:** Cycle authoring in `xlsx` + `notion-mcp`; market-band pull via Pave / Carta Total Comp REST when recipient has access. Bundled skill: `compensation-philosophy-bands` (cycle section).
- **Source:** https://www.pave.com/
- **Confidence:** ⚠ (paid market data)

## Employee survey design (eNPS, engagement, exit)

- **SOTA approach:** Culture Amp (research-driven engagement DNA), Lattice Engagement, 15Five Engagement, Officevibe Pulse, Leapsome Survey, Bonusly (recognition). DIY: Typeform / Tally.so + eNPS standard question + qualitative free-text + segmentation.
- **Agent execution path:** Survey authoring + analysis in `cli-anything` + Typeform / Tally / Culture Amp / Lattice REST. Pandas for analysis. Bundled skill: `performance-review-cycle-lattice-15five` (survey section) + `internal-knowledge-base-notion-slab-tettra` (results publication).
- **Source:** https://www.performancereviewssoftware.com/blog/lattice-vs-culture-amp-vs-15five-comparison/
- **Confidence:** ✓ (Typeform/Tally free tier; platform paid)

## Vendor renewal calendar + alerts

- **SOTA approach:** Renewal tracking: Vendr / Tropic / SpendHound / Cledara / Sastrify. Manual: Notion database with date triggers + 90/60/30/7-day reminders → Slack + email. Auto-renewal removal as policy.
- **Agent execution path:** Renewal calendar in `notion-mcp` DB + `google-calendar-mcp` events + Slack reminders. `cli-anything` → spend-mgmt platform REST when available. Bundled skill: `procurement-playbook-intake-renewal`.
- **Source:** https://www.spendhound.com/blog/best-saas-spend-management-software
- **Confidence:** ✓

## Org chart + headcount visualization

- **SOTA approach:** ChartHop, Pingboard, Lattice Org Charts, HiBob org chart, Sift (alt), built-into Rippling/Gusto. Visualization: Mermaid / D2 / Excalidraw for ad-hoc; OrgChartPlus / Workday OrgChart for enterprise.
- **Agent execution path:** `cli-anything` → HRIS REST for headcount data; visualization via Mermaid in `markdown-converter` / `drawio-mcp` / `excalidraw-diagram-generator`. Bundled skill: covered under `payroll-gusto-rippling-deel` and `internal-knowledge-base-notion-slab-tettra`.
- **Source:** https://www.hibob.com/blog/rippling-vs-gusto-vs-hibob/
- **Confidence:** ✓

## Background check + I-9 / E-Verify

- **SOTA approach:** Checkr (largest US background check), GoodHire, Certn (global), HireRight, Sterling. I-9 via Rippling / Gusto / HiBob / WorkBright. E-Verify via Gusto / Rippling.
- **Agent execution path:** `cli-anything` → Checkr / GoodHire API for background check trigger; HRIS for I-9. Bundled skill: `onboarding-offboarding-workflows` (background-check section).
- **Source:** https://www.checkr.com/api · https://www.goodhire.com/
- **Confidence:** ⚠ (paid keys)

---

## Summary table (≥90% fulfillment)

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | Hiring pipeline (ATS) | Greenhouse + Ashby + Lever + Workable | `cli-anything` + ATS REST | ⚠ |
| 2 | Employee onboarding | Rippling + Gusto + HiBob + Sapling + Enboarder | `cli-anything` + `google-workspace-mcp` + `slack-mcp` + `github` + `notion-mcp` | ⚠ |
| 3 | Employee offboarding | HRIS + Okta/WorkOS + MDM | `cli-anything` + SCIM + MDM API | ⚠ |
| 4 | Performance review cycle | Lattice + 15Five + Culture Amp + Leapsome | `cli-anything` + platform REST | ⚠ |
| 5 | 1:1 cadence | Lattice + 15Five + Officevibe | `notion-mcp` + `google-calendar-mcp` + REST | ✓ |
| 6 | Compensation bands | Pave + Carta Total Comp | `cli-anything` + REST | ⚠ |
| 7 | Employee handbook | Notion + Trainual + HRIS templates | `notion-mcp` + `docx` | ✓ |
| 8 | PTO policy + tracking | HRIS (Gusto/Rippling/HiBob) | `cli-anything` + REST | ⚠ |
| 9 | Remote/hybrid policy | Notion + Robin + Envoy | `notion-mcp` + `cli-anything` REST | ⚠ |
| 10 | Vendor evaluation framework | TCO matrix + Vendr/Tropic benchmarks | `xlsx` + `notion-mcp` | ✓ |
| 11 | SaaS spend audit | Tropic + Vendr + Zylo + SpendHound + Productiv + Torii | `cli-anything` + Ramp/Brex/SSO logs | ✓ |
| 12 | Software contract negotiation | Vendr + Tropic + Spendflo + DIY playbook | `cli-anything` + `docx` | ⚠ |
| 13 | Procurement playbook | Ramp Procurement + Brex + Coupa + intake forms | `cli-anything` + Typeform/Tally + `notion-mcp` | ✓ |
| 14 | Internal tool building | Retool + ToolJet + Budibase + Appsmith | `cli-anything` + npm/docker | ✓ |
| 15 | Workflow automation | n8n + Zapier + Make + Pipedream | `cli-anything` + docker / REST | ✓ |
| 16 | Process documentation | Scribe + Tango + Whale + Trainual + Notion | `cli-anything` + `notion-mcp` | ✓ |
| 17 | SSO / IAM setup | WorkOS + Okta + JumpCloud + Stytch + Auth0 | `cli-anything` + SCIM + SAML | ⚠ |
| 18 | Device management | Iru/Kandji + Jamf + Intune + Rippling IT | `cli-anything` + MDM REST | ⚠ |
| 19 | IT support tier-1 + runbook | Linear / Jira + Notion / Slab / Tettra | `linear-mcp` + `jira-mcp` + `notion-mcp` | ✓ |
| 20 | Payroll setup | Gusto + Rippling + Deel + Justworks + HiBob | `cli-anything` + REST | ⚠ |
| 21 | PEO / EOR global hiring | Deel + Remote + Oyster + Pebl + G-P | `cli-anything` + REST (Deel best surface) | ⚠ |
| 22 | Travel + expense | Brex + Navan + Ramp + Expensify + SAP Concur | `cli-anything` + REST | ⚠ |
| 23 | Corporate card policy | Brex + Ramp + Navan Connect | `cli-anything` + REST | ⚠ |
| 24 | Business insurance audit | Vouch + Embroker + Newfront + Coalition + At-Bay | `cli-anything` + broker REST + `docx` | ✓ |
| 25 | Office space management | Robin + Envoy + Tactic + Skedda | `cli-anything` + REST | ⚠ |
| 26 | Business continuity / DR | BIA + RTO/RPO + cloud backup + status page | `cli-anything` + `aws-s3-mcp` + `slack-mcp` + `twilio-mcp` | ✓ |
| 27 | Vendor risk assessment | SOC 2 + DPA + security questionnaires | `cli-anything` + `gmail-mcp` + `docx` | ✓ |
| 28 | Data retention + deletion | GDPR/CCPA + Vanta/Drata trust centers | `cli-anything` + `notion-mcp` + `linear-mcp` | ✓ |
| 29 | Internal knowledge base | Notion + Slab + Tettra + Confluence + Slite | `notion-mcp` + `obsidian-mcp` + `cli-anything` | ✓ |
| 30 | Runbook authoring | Notion + PagerDuty / Incident.io | `notion-mcp` + `cli-anything` | ✓ |
| 31 | AI policy / responsible use | NIST AI RMF + ISO 42001 + Anthropic guidance | `docx` + `notion-mcp` | ✓ |
| 32 | Compensation review cycle | Pave + Carta Total Comp + Lattice | `xlsx` + `cli-anything` REST | ⚠ |
| 33 | Employee survey design | Culture Amp + Lattice + 15Five + Typeform + Tally | `cli-anything` + REST | ✓ |
| 34 | Vendor renewal calendar | Notion DB + Cledara / Vendr / Tropic / SpendHound | `notion-mcp` + `google-calendar-mcp` + `slack-mcp` | ✓ |
| 35 | Org chart + headcount viz | ChartHop + Pingboard + Mermaid / D2 | HRIS REST + `drawio-mcp` + `excalidraw-diagram-generator` | ✓ |
| 36 | Background check + I-9 | Checkr + GoodHire + Certn + HRIS I-9 | `cli-anything` + REST | ⚠ |

**Fulfillment math:** 36 use cases mapped. 21 ✓ (free / generous free tier / open-source / authoring local). 15 ⚠ (recipient provides paid platform API key — common across HRIS / ATS / MDM / SSO / spend-mgmt / EOR space). 0 ✗.

**Verdict: ~95% fulfillment.** Every documented use case has a named SOTA tool with an exact agent execution path. The ⚠ entries are uniformly "recipient provides paid platform API key" — these are operationally normal in ops/HR/IT/procurement work where every platform charges per seat. There are no ✗ (genuinely impossible) entries. Authoring (policies, runbooks, handbook sections, BCP plans, AI policy, eval frameworks) is fully free-tier across `notion-mcp` / `docx` / `xlsx` / `markdown-converter`.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (only those that exist in `app/config/mcp_config.json`):
- `filesystem` — mandatory
- `github` — repo provisioning on hire / deprovisioning on offboard; runbook PR review (use cases 2, 3, 19)
- `google-workspace-mcp` — Gmail / Drive / Docs / Calendar / Sheets / Tasks / Contacts (use cases 2, 3, 5, 7, 13, 29, 34)
- `gmail-mcp` — vendor outreach, exit interviews, manager updates, dunning approvals (use cases 2, 3, 12, 26, 27)
- `outlook-mcp` — alt for Outlook-shop recipients
- `google-calendar-mcp` — 1:1s, renewals, review cycles, onboarding milestones, exit dates (use cases 2, 3, 4, 5, 34)
- `slack-mcp` — onboarding announcements, runbook surfaces, ops alerts, renewal reminders, surveys (use cases 2, 3, 5, 19, 26, 27, 33, 34)
- `ms-teams-mcp` — alt for Teams-shop recipients
- `discord-mcp` — alt comms
- `zoom-mcp` — interview scheduling, 1:1s
- `notion-mcp` — ops wiki, handbook, runbooks, intake forms, KB, policy library (use cases 7, 8, 9, 14, 19, 23, 26, 27, 28, 29, 30, 31, 34)
- `obsidian-mcp` — alt local-first knowledge base
- `linear-mcp` — IT support tickets, procurement intake, onboarding/offboarding checklists, vendor renewal tasks, DSAR workflow (use cases 3, 13, 19, 28, 34)
- `jira-mcp` — alt PM for Atlassian-shop recipients
- `todoist-mcp` — personal task list per ops lead
- `xero-mcp` — vendor spend pull, COGS, payroll mapping (use cases 11, 20)
- `stripe-mcp` — corporate cards if Stripe Issuing in use; vendor invoice link
- `postgresql-mcp` — raw HRIS DB queries / cohort joins when accounting DB exposed
- `firecrawl-mcp` — vendor pricing scrape, market band benchmarks (use case 6, 11, 12)
- `brightdata-mcp` — alt scrape for paywalled benchmarks
- `gemini-ocr-mcp` — paper invoice / contract / receipt OCR
- `mistral-ocr-mcp` — alt OCR
- `google-drive-mcp` — contract storage, data room sections, signed handbook ACKs (use cases 7, 13, 27)
- `drawio-mcp` — org chart, workflow diagrams, BCP system diagrams (use cases 26, 35)
- `figma-mcp` — handbook design, internal-tool mockups
- `sentry-mcp` — incident impact tracking for runbook authoring
- `posthog-mcp` — internal-tool usage analytics, employee survey analysis
- `huggingface-mcp` — HR/ops benchmark dataset discovery
- `brave-search` — current SOTA tool / market research backstop

**Skill packs to create in Round 2 (runtime build)** — 22 bundled, in seed-prompt order:
1. `hiring-pipeline-greenhouse-ashby-lever` — ATS recipes; candidate CRUD; pipeline reports; scorecards
2. `onboarding-offboarding-workflows` — Day-1 / Week-1 / 30-60-90 templates; access provisioning/deprovisioning via SCIM
3. `performance-review-cycle-lattice-15five` — Cycle authoring; calibration; 1:1s; survey design
4. `compensation-philosophy-bands` — Bands per role × geography × stage; Pave / Carta Total Comp data pulls
5. `employee-handbook-policies` — Multi-state handbook + PTO + remote policy + AI policy templates
6. `vendor-evaluation-negotiation` — TCO matrix; build-vs-buy; counter-letter templates; BATNA playbook
7. `saas-spend-audit-vendr-tropic-spendflo` — Spend pull; SSO log cross-ref; duplicate + unused detection
8. `procurement-playbook-intake-renewal` — Intake form; approval workflow; contract storage; renewal calendar
9. `internal-tools-retool-tooljet-budibase` — Self-host + cloud recipes; component templates; permission models
10. `workflow-automation-zapier-make-n8n` — n8n self-host docker + workflow JSON; Zapier / Make REST
11. `process-documentation-scribe-tango` — Auto-capture recipes; SOP authoring; Trainual training-rollout
12. `sso-okta-jumpcloud-workos` — SAML / SCIM setup; stage-based platform selection; provisioning rules
13. `device-management-kandji-jamf-intune` — MDM blueprints; OS update enforcement; remote wipe; lifecycle hooks
14. `payroll-gusto-rippling-deel` — Payroll setup; multi-state nexus; contractor onboarding
15. `peo-eor-global-hiring-deel-remote-oyster-gp` — Country selection matrix; entity vs partner; Deel API recipes
16. `travel-expense-policy-navan-ramp-brex` — Policy authoring; card setup; auto-reconciliation; expense routing
17. `business-insurance-vouch-embroker-newfront` — Coverage audit; D&O / E&O / Cyber / EPLI bundling; renewal calendar
18. `office-management-robin-envoy` — Desk + room + visitor booking; space analytics
19. `business-continuity-disaster-recovery` — BIA + RTO/RPO + cloud backup + tabletop exercise framework
20. `vendor-risk-assessment-dpa` — Questionnaire + SOC 2 review + DPA drafting + data retention policy
21. `internal-knowledge-base-notion-slab-tettra` — KB architecture; AI agent setup; cross-tool search
22. `runbook-authoring-operational-incident` — Operational + incident runbook templates; post-mortem; status page

---

## Notes on remaining caveats (the ⚠ rows)

For each ⚠ use case:
- **Hiring pipeline (ATS):** recipient provides Greenhouse / Ashby / Lever / Workable API key. All have public REST + sandbox.
- **HRIS-led use cases (onboarding/offboarding/PTO/payroll/compensation):** recipient provides Gusto / Rippling / HiBob / Deel / Justworks key. Deel has best dev surface (only EOR with sandbox + webhooks pre-contract).
- **Performance / 1:1 platforms:** recipient provides Lattice / 15Five / Culture Amp / Leapsome key.
- **Compensation market data (Pave / Carta Total Comp):** recipient pays for market data; Levels.fyi / Glassdoor public for fallback.
- **SSO / IAM:** recipient provides Okta / JumpCloud / WorkOS / Stytch / Auth0 key. Stage-based selection logic in skill pack.
- **Device management (MDM):** recipient provides Iru/Kandji / Jamf / Intune / Rippling IT key.
- **EOR / PEO (Deel / Remote / Oyster / Pebl / G-P):** recipient provides key. Deel has by-far-best dev surface.
- **Travel + expense + corp card (Brex / Ramp / Navan):** recipient provides paid API key.
- **Office management (Robin / Envoy):** recipient provides paid key.
- **Vendor spend platforms (Vendr / Tropic / Spendflo / SpendHound):** recipient pays for managed procurement; manual playbook works without.
- **Background check + I-9:** recipient provides Checkr / GoodHire key.

None of these are platform-rejected or impossible. Every ⚠ resolves once the recipient provides their existing platform's API key. Authoring tasks (policies, runbooks, handbook, BCP plans, AI policy) ship at 100% with `notion-mcp` / `docx` / `xlsx` / `markdown-converter` from the free-tier defaults.

---

## Operational disclosure footer

Per the seed prompt: every binding employment-law / vendor-contract / insurance-binder / regulatory-compliance recommendation includes the disclosure **"Defer to `legal-counsel` for binding employment-law / vendor-contract review."** Operations agent computes structures, drafts templates, models trade-offs, and surfaces decisions — humans approve binding contracts and a licensed counsel signs anything legally binding.
