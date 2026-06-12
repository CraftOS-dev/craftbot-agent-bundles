# Operations Agent — Sources

Section-to-source map for `soul.md` and `role.md`. This file ships in the bundle but is **not** loaded into the agent's context — it exists for humans verifying provenance and for future refreshes.

The per-use-case SOTA mapping with confidence flags is at `reference/SOTA_USE_CASES.md`. URLs in `agent.yaml → sources` and the per-tool table below.

The v1 build did not download upstream agent reference files into `reference/agents/` (no dedicated `operations-agent` / `head-of-people` / `vp-people` / `business-operations` v0 agent exists in the four public catalogs as of the build date — see `reference/INVENTORY.md`). The composition synthesizes operations-practitioner conventions (Divio Diátaxis doc taxonomy, NIST AI RMF, Big-4 audit PBC list patterns, FAANG-derived SCIM provisioning rules, US multi-state employment-law variances, EU GDPR Art. 17, 2026 Tropic SaaS spending benchmark, Bessemer / Eagle Rock comp band convention, blameless post-mortem Google SRE template) and grounds every claim in the cited URLs below.

---

## soul.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Title + persona intro | Composition: ops-lead / HRBP / IT-ops / procurement-lead role conventions; seed prompt convictions | "Documented process beats heroic individual" is a long-standing ops mantra; "automation pays for itself in months but only if used" is standard ops-engineering posture; "vendor lock-in is technical debt with a billing schedule" extends Joel Spolsky strategy + 2025-2026 SaaS-buyer literature |
| Purpose | Composition: hand-off rules from seed prompt + sibling agents (`legal-counsel`, `finance-controller`, `devops-engineer`, `ceo-agent`, `product-manager`, `compliance-agent`) | Always-disclose footer per seed prompt requirement |
| Execution stack | `reference/SOTA_USE_CASES.md` | Built from per-use-case SOTA research; mirrors the 22 bundled skill packs |
| When invoked — Hiring | Index.dev ATS comparison · Unified.to ATS API guide · Cavuno public job posting APIs guide | Pass-through targets from common ops benchmark data |
| When invoked — Onboarding | HiBob HRIS comparison · Rippling MDM review · WorkOS SCIM provisioning guide | Day-0 / Day-1 / Week-1 / 30-60-90 from common Day-1 onboarding ops practice |
| When invoked — Offboarding | Rippling MDM review · WorkOS SCIM provisioning · state-specific final-paycheck conventions (CA labor code; IL Wage Payment Act; MA Wage Act) | Same-day SCIM deprovisioning from security practice |
| When invoked — Performance review cycle | Outsail Lattice/15Five/Culture Amp comparison · Performance Reviews Software 2026 comparison · feedbackpulse Lattice alternatives | Calibration session structure from FAANG comp-cycle convention |
| When invoked — Vendor evaluation | SpendHound 2026 SaaS spend mgmt · Tropic vs Spendflo · Najar Spendflo alternatives · Joel Spolsky Strategy Letter V (core vs context) | TCO matrix from common procurement practice |
| When invoked — SaaS spend audit | Tropic 2025 SaaS Buying Trends · SpendHound Vendr alternatives | Top-10 = 74% of spend from Tropic benchmark |
| When invoked — Procurement intake | Ramp Procurement docs · CTOClub SaaS spend mgmt review · SpendHound benchmarks | Spend-tier approval routing standard |
| When invoked — Internal tool building | ToolJet vs Budibase vs Appsmith comparison · OpenHelm Retool comparison · OpenAlternative Retool alternatives | Platform pick by stage + use case |
| When invoked — Workflow automation | Automation Labs Zapier vs Make vs n8n 2026 · n8n Blog AI workflow tools · HatchWorks n8n vs Zapier 2026 | n8n 2.0 Jan 2026 LangChain + 70 AI nodes |
| When invoked — Process documentation | Tango Scribe alternatives · Docsie Scribe vs Tango · Tango process documentation 2026 | Divio / Diátaxis taxonomy from canonical Daniele Procida 2017 |
| When invoked — SSO / IAM | Security Boulevard Auth0/Okta/Stytch/WorkOS/SSOJet 2026 · WorkOS SCIM providers · SIIT JumpCloud vs Okta | Stage-based platform pick from buyer-stage framework |
| When invoked — Device management | Technology Match Intune vs Jamf vs Iru 2026 · Iru Kandji alternatives · Rippling MDM review | Iru rebrand Oct 2025; Apple DDM transition for Intune |
| When invoked — Payroll | John Galt Finance Gusto vs Justworks vs Rippling · HiBob HRIS comparison | Stage-based platform pick |
| When invoked — EOR global hiring | Deel vs Remote · Native Teams Deel vs Oyster · Alcor Pebl alternatives · WhichPayroll EOR API access | Deel only EOR with public API + sandbox + webhooks pre-contract |
| When invoked — Process documentation | (see above) | — |
| When invoked — Vendor risk assessment | Secureframe SOC 2 vs questionnaires · SOC2 Auditors questionnaire guide · Copla 2026 risk assessment guide | 73% SOC 2 + 70% questionnaires per Secureframe 2026 benchmark |
| When invoked — BCP / DR | Atlas Systems vendor risk checklist · NMS Consulting vendor risk · Google SRE blameless post-mortem (cite below) | BIA + RTO/RPO standard from BC/DR practice |
| Core operating rules | Composition: ops body of knowledge (security practice + employment-law variance + SaaS-buyer-2026 posture + Google SRE) | "Always disclose" rule per seed prompt |
| Mode-specific decisions | Source-mapped per mode (same as When invoked rows) | Done-when definitions from ops discipline |
| Quality gates | Composition synthesizing ops + security + procurement practice | Source standards cited inline |
| Output format | Composition: standard ops-deliverable conventions (Notion KB, Pandoc, xlsx, branded PDF) | — |
| Communication style | Composition: stage-aware + lock-in-transparent + DECISION REQUIRED label patterns | — |
| When to push back | Composition: state-specific employment law + SOC 2 vendor practice + procurement discipline | Cited statutory/standard references where binding |
| When to defer | Composition: hand-off matrix from seed prompt sibling agents | Always-disclose `legal-counsel` for binding employment-law / vendor-contract / insurance-binder review |
| PROACTIVE self-init footer | `METHODOLOGY.md` standard pattern | Routine questions tailored to ops workflow (team size, HRIS, pain point) |
| Closing rule | Restatement of three load-bearing convictions from seed prompt | — |

---

## role.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Capability reference → ATS platforms | Unified.to · Index.dev · Cavuno · Pin ATS rankings | All comparison posts 2026 |
| Capability reference → HRIS / payroll | John Galt Finance · HiBob · Rippling · Gusto docs | 2026 stage-based selection |
| Capability reference → EOR / PEO | Deel · Remote · Oyster · Pebl/Velocity Global · G-P · Alcor alternatives | Pebl rebrand Sept 2025 |
| Capability reference → Performance / engagement | Outsail · Performance Reviews Software · feedbackpulse Lattice alts | 15Five $9-15 PEPM; Lattice growth-stage default |
| Capability reference → Compensation platforms | Pave docs · Carta Total Comp docs · Levels.fyi · Radford/Mercer reference | Public crowdsource fallback for engineering |
| Capability reference → Vendor / SaaS management | Vendr · Tropic · Spendflo · SpendHound · Sastrify · Cledara · Zylo · CloudEagle · Productiv · Torii · Vertice | 2026 comparison data |
| Capability reference → Workflow automation | n8n Blog · Zapier Agents · Make Maia · HatchWorks comparison · Pipedream/Workato docs | n8n 2.0 Jan 2026; native LangChain; 70+ AI nodes |
| Capability reference → Internal tool platforms | ToolJet blog · Budibase docs · Appsmith docs · Retool docs · Internal.io · Glide · Stacker · Softr | 2026 OSS comparison |
| Capability reference → Device management | Technology Match · Iru rebrand announcement · Rippling MDM review · SIIT MDM software · Mosyle docs | Iru = Kandji rebrand Oct 2025 |
| Capability reference → SSO / IAM | Security Boulevard buyer-stage framework · WorkOS SCIM guide · SIIT JumpCloud vs Okta · Auth0 docs · Stytch B2B docs | 2026 stage-based selection |
| Capability reference → Process documentation | Tango Scribe alternatives · Docsie Scribe vs Tango · Whale · Trainual · Notion Agents · Confluence Rovo | Auto-capture landscape 2026 |
| Capability reference → Travel + expense + corp card | Ramp Navan Brex comparison · Brex CapOne acquisition · Navan AI features · Receiptor AI Brex alternatives | Brex acquired April 2026; Navan Ava + Expense Chat |
| Capability reference → Insurance | Embroker Startup Package · Vouch · SVB Founders Guide · Coalition Cyber · At-Bay | 2026 startup carrier landscape |
| Capability reference → Office / workplace | Archie Envoy vs Robin · Robin 2026 Gartner MQ · Envoy docs · Skedda · Tactic · Eden | Robin 2026 Gartner MQ Leader |
| Capability reference → KB platforms | BuildMVPFast AI wikis · Slite KB software · Docsie Confluence vs Notion · Taskade AI wiki tools | Notion Agents 2026; Confluence Rovo 2026 |
| Capability reference → Background check + I-9 | Checkr · GoodHire · Certn · HireRight · WorkBright · Gusto/Rippling I-9 modules | Standard providers |
| Capability reference → Forms / surveys | Typeform docs · Tally.so · BlockSurvey · SurveyMonkey | Common providers |
| Hiring playbook | Composition: ATS pipeline conventions + structured-hiring practice + bias-review guardrails (Joblint / Textio) | Pass-through targets from common ops benchmark data |
| Onboarding playbook | Composition: Day-0 / Day-1 / Week-1 / 30-60-90 from common ops practice + WorkOS SCIM provisioning + Apple ABM / Microsoft AutoPilot | Provisioning matrix from cross-platform mapping |
| Offboarding playbook | Composition: same-day SCIM deprovisioning security practice + state-specific final-paycheck rules (CA labor code; IL Wage Payment Act; MA Wage Act) | Access revocation priority from security practice |
| Performance cycle playbook | Composition: cycle structure + 5-point Likert + calibration session from common comp-cycle convention | Comp-decision matrix synthesized from common practice |
| Compensation bands playbook | Pave docs · Carta Total Comp docs · Levels.fyi · Radford convention | Geo-tier convention from common comp-band practice |
| Vendor evaluation playbook | Composition: TCO matrix + Spolsky Strategy Letter V (core vs context) + 2026 procurement practice | Stages 0-5 synthesized from common procurement convention |
| SaaS spend audit playbook | Tropic 2025 benchmark · SpendHound · Productiv usage-based | Top-10 = 74% benchmark; common duplicates list curated |
| Procurement intake playbook | Composition: spend-tier approval routing + standard intake form fields | Approval thresholds standard convention |
| Internal tools playbook | ToolJet vs Budibase vs Appsmith comparison · OpenHelm Retool comparison · platform docs | Platform pick by use case + stage |
| Workflow automation playbook | Automation Labs · n8n Blog · HatchWorks · Pipedream/Workato docs · Apple Shortcuts | n8n 80-90% cost advantage for high volume |
| Process documentation playbook | Tango Scribe alternatives · Divio / Diátaxis (Daniele Procida 2017) · Confluence Rovo AI · Notion Agents | Divio quadrant standard taxonomy |
| SSO setup playbook | Security Boulevard buyer-stage · WorkOS SCIM guide · SIIT JumpCloud vs Okta · stage-based pick framework | Stage-based selection from 2026 buyer-stage framework |
| Device management playbook | Technology Match · Iru rebrand · Rippling MDM · Apple ABM / Microsoft AutoPilot | Lifecycle hooks from common practice |
| Payroll setup playbook | John Galt Finance · HiBob comparison · Gusto/Rippling/Deel/Justworks docs | Stage + state nexus from common payroll practice |
| EOR global hiring playbook | Deel vs Remote · Native Teams Deel vs Oyster · Alcor Pebl alternatives · WhichPayroll EOR API access · country-specific employment-law literature (CLT Brazil; PFL UK; Fair Work Act AU; etc.) | Country gotchas common practitioner reference |
| Travel and expense playbook | Ramp Navan Brex comparison · Brex acquisition news · Navan docs | Stage-match policy framework |
| Insurance audit playbook | Embroker Startup Package · Vouch · SVB Founders Guide · Coalition · At-Bay | Coverage stack by stage standard convention |
| Office management playbook | Archie Envoy vs Robin · Robin 2026 Gartner MQ | Robin Gartner Leader 2026 |
| Business continuity playbook | Composition: BIA + RTO/RPO tier table + Google SRE blameless post-mortem + Statuspage/Better Stack/PagerDuty/Incident.io docs | Tier table from common BC/DR practice |
| Vendor risk assessment playbook | Secureframe SOC 2 vs questionnaires · SOC2 Auditors questionnaire guide · Copla 2026 risk guide | 73% SOC 2 + 70% questionnaires per Secureframe |
| Internal knowledge base playbook | BuildMVPFast AI wikis · Slite KB software · Notion Agents 2026 · Tettra Slack-native · Confluence Rovo 2026 | Team-size pick from KB platform comparison |
| Runbook authoring playbook | Composition: blameless post-mortem (Google SRE Site Reliability Engineering book / Postmortem Culture chapter) + PagerDuty / Incident.io conventions | Standard practitioner playbook |
| AI policy playbook | NIST AI RMF (NIST 2023 AI Risk Management Framework) · ISO/IEC 42001:2024 · EU AI Act 2024/1689 · Anthropic responsible-use guidance | Frameworks cited inline |
| Renewal calendar template | Composition: SaaS contract management common practice + Notion DB pattern | — |
| Intake form templates | Composition: Typeform / Tally / Notion form patterns + spend-tier approval routing | — |
| Handbook section index | Composition: multi-state US handbook standard sections (CA / NY / IL / MA / WA labor codes; FLSA; FMLA; ADA; Title VII) + AI policy framework | State labor codes referenced; binding interpretation deferred to `legal-counsel` |
| Antipattern catalog | Composition: common ops failure modes mapped to specific source-of-truth standards (SCIM provisioning, SOC 2 review, post-mortem culture) | All antipatterns map to specific industry conventions |
| SOTA tool reference | Per-tool sources cited inline (in role.md sections) | One source per tool minimum |
| SOTA execution playbook table | Built from `reference/SOTA_USE_CASES.md` mapping | First-stop skill pack per user request type |
| Brief / output templates | Composition: standard vendor-eval / onboarding-plan / spend-audit conventions | Synthesized formats |
| Closing rules | Restatement of three load-bearing convictions + hand-off matrix | — |

---

## SOTA tool sources (June 2026)

> One row per SOTA tool referenced in the agent.

| Tool | Source URL | Used for |
|---|---|---|
| Greenhouse | https://www.index.dev/blog/greenhouse-vs-lever-vs-ashby-ats-comparison | `hiring-pipeline-greenhouse-ashby-lever` (Greenhouse-half) |
| Ashby | https://cavuno.com/blog/ats-platforms-public-job-posting-apis | `hiring-pipeline-greenhouse-ashby-lever` (Ashby-half) |
| Lever | https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable | `hiring-pipeline-greenhouse-ashby-lever` (Lever-half) |
| Workable | https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable | ATS alt reference |
| Pin ATS rankings | https://www.pin.com/blog/best-applicant-tracking-systems/ | ATS landscape 2026 |
| Lever modern-ATS guide | https://www.lever.co/blog/modern-applicant-tracking-systems-what-to-look-for-in-2026 | ATS decision context |
| Visualping ATS rankings | https://visualping.io/blog/best-applicant-tracking-systems | ATS landscape 2026 |
| Gusto vs Justworks vs Rippling 2026 | https://johngalt-finance.com/gusto-vs-justworks-vs-rippling-payroll-hr-2026/ | `payroll-gusto-rippling-deel` (SMB section) |
| HiBob comparison | https://www.hibob.com/blog/rippling-vs-gusto-vs-hibob/ | `payroll-gusto-rippling-deel` (mid-market section) |
| Gusto vs Rippling | https://workology.com/gusto-vs-rippling-pricing-features-key-differences/ | Comparison reference |
| Juicebox Rippling alternatives | https://juicebox.ai/blog/rippling-alternatives | HRIS alt reference |
| Paylocity Rippling competitors | https://www.paylocity.com/why-paylocity/compare/lists/rippling-competitors/ | Mid-market HRIS context |
| Authencio Rippling review | https://www.authencio.com/blog/rippling-hr-it-payroll-guide-features-pricing-pros-cons-alternatives | Rippling all-in-one context |
| Deel vs Remote | https://www.deel.com/blog/deel-vs-remote-honest-employer-of-record-service-comparison/ | `peo-eor-global-hiring-deel-remote-oyster-gp` |
| Deel vs Velocity Global | https://www.deel.com/blog/deel-vs-velocity-global-honest-employer-of-record-service-comparison/ | EOR comparison |
| Deel vs Oyster | https://nativeteams.com/blog/deel-vs-oyster | `peo-eor-global-hiring-deel-remote-oyster-gp` (Oyster) |
| Pebl alternatives 2026 | https://alcor.com/velocity-global-alternatives/ | Pebl rebrand Sept 2025 |
| Gloroots Pebl alternatives 2026 | https://www.gloroots.com/blog/velocity-global-alternatives | EOR alt reference |
| EOR API access guide | https://whichpayroll.com/features/eor-api-access | Deel = only EOR with public API + sandbox + webhooks |
| Best EOR 2026 (Deel/Rippling/Remote/Papaya) | https://remote.com/blog/eor-peo/deel-vs-rippling-vs-remote-vs-papaya-global | EOR landscape 2026 |
| Best EOR services 2026 | https://remote.com/blog/eor-peo/best-eor-services | EOR landscape 2026 |
| Global employment platforms 2026 | https://www.recruiterslineup.com/top-global-employment-platforms/ | EOR landscape 2026 |
| 10 Best EOR companies 2026 | https://www.remotelytalents.com/blog/best-employer-of-record-eor-companies-hire-globally | EOR landscape 2026 |
| Lattice vs 15Five vs Culture Amp | https://www.outsail.co/post/lattice-vs-15five-vs-culture-amp-performance | `performance-review-cycle-lattice-15five` |
| Performance Reviews Software 2026 | https://www.performancereviewssoftware.com/blog/lattice-vs-culture-amp-vs-15five-comparison/ | 15Five $9-15 PEPM; Lattice default growth-stage |
| 15Five alternatives | https://peopleopsclub.com/software/15five/alternatives | Perf platform alt context |
| Lattice alternatives 2026 | https://feedbackpulse.com/lattice-alternatives | Perf platform alt context |
| Lattice vs Culture Amp | https://www.performyard.com/articles/lattice-vs-culture-amp | Perf comparison |
| Leapsome vs Culture Amp vs 15Five | https://www.saasworthy.com/compare/leapsome-vs-culture-amp-vs-15five-vs-engagewith?pIds=5119%2C7490%2C8288%2C31874 | Leapsome widest breadth |
| Leapsome alternatives | https://feedbackpulse.com/leapsome-alternatives | Perf platform alt context |
| 15Five vs Lattice | https://www.peoplepilot.io/blog/15five-vs-lattice-2026 | Perf comparison detail |
| Lattice vs 15Five vs Culture Amp evaluation | https://www.kutskoconsulting.com/blog/lattice-vs-15five-vs-culture-amp-how-to-evaluate-and-choose-software-to-enable-your-employees | Evaluation framework |
| Pave (compensation benchmarking) | https://www.pave.com/ | `compensation-philosophy-bands` |
| Carta Total Comp | https://carta.com/total-comp/ | `compensation-philosophy-bands` |
| Vendr | https://www.spendhound.com/blog/vendr-alternatives | `vendor-evaluation-negotiation` + `saas-spend-audit-vendr-tropic-spendflo` |
| Tropic vs Spendflo | https://www.tropicapp.io/compare/spendflo | Tropic comprehensive vendor mgmt |
| Tropic 2025 SaaS Buying Trends | https://www.tropicapp.io/reports/software-spending-trends-2025 | Top-10 = 74% of spend benchmark |
| Tropic SaaS budgeting | https://www.tropicapp.io/blog/saas-budgeting | Procurement context |
| Spendflo benchmarks | https://www.spendflo.com/pricing-benchmarks | `vendor-evaluation-negotiation` |
| Spendflo alternatives | https://najar.ai/blog/spendflo-alternatives | Procurement alt context |
| SpendHound 2026 SaaS spend mgmt | https://www.spendhound.com/blog/best-saas-spend-management-software | SaaS spend mgmt landscape 2026 |
| Nudge Security best SaaS spend tools | https://www.nudgesecurity.com/post/best-saas-spend-management-tools | SaaS spend landscape |
| CTOClub SaaS spend reviewed 2026 | https://thectoclub.com/tools/best-saas-spend-management-software/ | SaaS spend landscape |
| Gitnux SaaS spend mgmt 2026 | https://gitnux.org/best/saas-spend-management-software/ | SaaS spend landscape |
| SaasWorthy SaaS spend mgmt 2026 | https://www.saasworthy.com/list/saas-spend-management-software | SaaS spend landscape |
| Audit Friendly Tropic review | https://auditfriendly.co/software/tropic | Tropic review reference |
| n8n Blog AI workflow tools 2026 | https://blog.n8n.io/best-ai-workflow-automation-tools/ | `workflow-automation-zapier-make-n8n` |
| Zapier vs Make vs n8n 2026 | https://medium.com/@automation.labs/zapier-vs-make-vs-n8n-in-2026-where-ai-agents-actually-fit-1edbbeff85f3 | Comparison 2026 |
| HatchWorks n8n vs Zapier | https://hatchworks.com/blog/ai-agents/n8n-vs-zapier/ | n8n cost advantage 80-90% |
| Digital Applied Marketing automation | https://www.digitalapplied.com/blog/marketing-automation-ai-agents-make-zapier-n8n-2026 | AI workflow comparison |
| Digital Applied Zapier vs Make vs n8n | https://www.digitalapplied.com/blog/zapier-vs-make-vs-n8n-2026-automation-comparison | 2026 comparison |
| Genesys Growth Zapier vs Make vs n8n | https://genesysgrowth.com/blog/zapier-ai-vs-make-com-ai-vs-n8n-ai | Marketing-leader guide |
| Flowmondo n8n vs Zapier vs Make | https://www.flowmondo.com/article/n8n-vs-zapier-vs-make | Comparison |
| Intuz Make vs n8n vs Zapier | https://www.intuz.com/blog/make-vs-n8n-vs-zapier-detailed-comparison | 2026 detailed guide |
| FindSkill AI workflow automation guide | https://findskill.ai/blog/ai-workflow-automation-guide/ | AI workflow education |
| Finbyz n8n vs Zapier vs Make | https://finbyz.tech/n8n/insights/n8n-vs-zapier-vs-make-comparison | Comparison |
| ToolJet vs Budibase vs Appsmith | https://blog.tooljet.com/appsmith-vs-budibase-vs-tooljet/ | `internal-tools-retool-tooljet-budibase` (OSS pick) |
| Retool vs Budibase vs Appsmith | https://www.openhelm.ai/blog/retool-vs-budibase-vs-appsmith-internal-ai-tools | Retool commercial vs OSS trade-off |
| Open Source Retool Alternatives | https://openalternative.co/alternatives/retool | ToolJet best Retool OSS alt |
| Appsmith alternatives | https://www.weweb.io/blog/appsmith-alternatives-best-tools-guide | Internal tool alt reference |
| Refine Appsmith alternatives | https://refine.dev/alternatives/appsmith-alternatives/ | Internal tool alt reference |
| ToolJet Appsmith alternatives | https://blog.tooljet.com/appsmith-alternatives-for-internal-apps/ | Internal tool alt reference |
| Retool alternatives 2026 | https://atoms.dev/blog/retool-alternatives | Internal tool alt reference |
| UI Bakery Retool alternatives | https://uibakery.io/retool-alternatives | Internal tool alt reference |
| Modern DataTools Retool vs Appsmith vs Budibase | https://www.modern-datatools.com/compare/retool-vs-appsmith-vs-budibase | 2026 comparison |
| ToolJet migrate from Retool | https://blog.tooljet.com/migrate-from-retool-to-open-source-alternatives/ | Migration guide |
| Tango Scribe alternatives 2026 | https://www.tango.ai/blog/scribe-alternatives | `process-documentation-scribe-tango` |
| Scribe alternatives 2026 | https://scribe.com/library/scribe-alternatives-competitors | Auto-capture landscape |
| Waybook Scribe alternatives | https://www.waybook.com/blog/scribe-alternatives-the-best-tools-for-process-documentation | Auto-capture alt context |
| Scribe vs Tango | https://scribe.com/library/scribe-vs-tango | Auto-capture comparison |
| Docsie Scribe vs Tango | https://www.docsie.io/blog/articles/scribe-vs-tango-comparison-2026/ | Auto-capture comparison |
| Tango AI workflow documentation | https://www.tango.ai/blog/ai-workflow-documentation-tools | Auto-capture for AI automation |
| Tango process documentation 2026 | https://www.tango.ai/blog/process-documentation-software | Process doc landscape |
| Tango SOP creation 2026 | https://www.tango.ai/blog/sop-software | SOP software landscape |
| Glitter SOP software for small biz | https://www.glitter.io/blog/process-documentation/sop-software-for-small-business | SOP small-biz context |
| Auth0 vs Okta vs Stytch vs WorkOS vs SSOJet 2026 | https://securityboulevard.com/2026/06/auth0-vs-okta-vs-stytch-vs-workos-vs-ssojet-2026-a-buyer-stage-framework/ | `sso-okta-jumpcloud-workos` (stage-based) |
| Best WorkOS Alternatives | https://www.scalekit.com/blog/workos-alternatives | SSO alt context |
| Best SCIM providers 2026 | https://workos.com/blog/best-scim-providers-for-automated-user-provisioning-in-2026 | `sso-okta-jumpcloud-workos` (SCIM) |
| Best Clerk Alternatives | https://www.scalekit.com/blog/clerk-alternatives-for-b2b-ai-apps-in-2026 | B2B SSO alt context |
| 7 Best WorkOS Alternatives | https://www.loginradius.com/blog/identity/top-workos-alternatives | SSO alt context |
| JumpCloud vs Okta | https://www.siit.io/tools/comparison/jumpcloud-vs-okta | SSO/IAM comparison |
| JumpCloud Okta integration | https://www.okta.com/integrations/jumpcloud/ | Integration reference |
| Top 8 WorkOS Alternatives | https://www.descope.com/blog/post/workos-alternatives | SSO alt context |
| WorkOS | https://workos.com/ | WorkOS B2B enterprise readiness |
| JumpCloud review 2026 | https://ssojet.com/security-vendors/workforce-iam/jumpcloud/ | JumpCloud open directory |
| Intune vs Jamf vs Iru 2026 | https://technologymatch.com/blog/intune-vs-jamf-pro-vs-kandji-the-it-leaders-guide-to-apple-management-in-2026 | `device-management-kandji-jamf-intune` |
| Jamf alternatives 2026 | https://www.siit.io/tools/alternatives/jamf-alternatives | MDM alt context |
| MDM software 2026 | https://www.siit.io/blog/best-mdm-software | MDM landscape 2026 |
| Jamf vs Intune vs Iru UK 2026 | https://stabilise.io/blog/jamf-pro-vs-microsoft-intune-vs-iru-apple-mdm-comparison-2026 | UK perspective MDM 2026 |
| Primo MDM tools | https://www.getprimo.com/blog-infos/top-5-easiest-mdm-tools-to-deploy-for-small-it-teams | Small IT team MDM context |
| Factorial 10 best MDM 2026 | https://factorialhr.com/blog/best-mdm-software/ | MDM landscape 2026 |
| Iru Kandji alternatives | https://www.iru.com/compare/kandji-alternatives | Iru/Kandji rebrand Oct 2025 |
| Rippling MDM review | https://www.rippling.com/blog/rippling-mdm-review | Rippling IT lifecycle-tied MDM |
| Jamf vs Kandji 2025 | https://www.rippling.com/blog/jamf-vs-kandji | MDM comparison |
| Jamf vs Kandji 2026 | https://www.siit.io/tools/comparison/jamf-vs-kandji | MDM comparison |
| Ramp Navan vs Brex vs Ramp | https://ramp.com/blog/navan-vs-brex-vs-ramp | `travel-expense-policy-navan-ramp-brex` |
| Brex BrexPay for Navan | https://www.brex.com/journal/press/brex-pay-for-navan | BrexPay for Navan Oct 2024 |
| Brex acquisition Capital One | https://receiptor.ai/blog/brex-alternatives-after-the-capital-one-acquisition-2026 | Brex April 2026 acquisition |
| Navan best travel analytics AI 2026 | https://navan.com/blog/best-travel-analytics-tools-ai | Navan Ava + Expense Chat 94/100 CSAT |
| Navan revenue + funding | https://sacra.com/c/navan/ | Navan financials reference |
| Brex Pay Navan landing | https://www.brex.com/brexpay | Integration product detail |
| FinanceBuzz best corporate cards 2026 | https://www.financebuzz.net/what-are-the-best-corporate-cards-for-businesses-in-2026/ | Corporate card landscape 2026 |
| Ramp top Brex alternatives 2026 | https://ramp.com/blog/top-brex-alternatives | Brex alt context |
| Ramp Navan alternatives | https://ramp.com/blog/top-navan-alternatives | Navan alt context |
| Navan AI tools T&E | https://navan.com/blog/ai-tools-travel-expense-management | AI T&E context |
| Embroker startup insurance | https://www.embroker.com/coverage/startup-insurance/ | `business-insurance-vouch-embroker-newfront` (Embroker) |
| Vouch startup insurance 2026 | https://www.vouch.us/blog/what-is-startup-business-insurance-and-why-do-i-need-it | Vouch coverage guide |
| SVB Startup Insurance Guide | https://www.svb.com/startup-insights/startup-strategy/startup-insurance-guide-for-founders/ | Coverage stack by stage |
| Embroker review 2026 | https://startupsavant.com/service-reviews/embroker-business-insurance | Embroker review context |
| Vouch technology insurance | https://www.vouch.us/technology | Vouch tech-co coverage |
| Best startup insurance USA 2026 | https://tzpastpapers.com/new/best-business-insurance-for-startups-in-the-usa/ | Insurance landscape 2026 |
| Corgi vs Vouch | https://www.corgi.insure/blog/corgi-vs-vouch | Insurance alt context |
| Vouch startup insurance costs 2026 | https://www.vouch.us/blog/startup-insurance-costs | Premium reference |
| Insuranceopedia startup insurance | https://www.insuranceopedia.com/business-insurance/startup-insurance | Coverage education |
| Corgi ML startup insurance | https://www.corgi.insure/blog/what-insurance-do-machine-learning-startups-typically-carry-and-which-companies-provide-it | AI startup specific coverage |
| Envoy vs Robin 2026 | https://archieapp.co/blog/envoy-vs-robin/ | `office-management-robin-envoy` |
| Robin G2 review 2026 | https://www.g2.com/products/robin/reviews | Robin features review |
| Robin Software Advice | https://www.softwareadvice.com/desk-booking/robin-powered-profile/ | Robin product detail |
| Robin Powered | https://robinpowered.com/ | Robin 2026 Gartner MQ Leader |
| Robin CBInsights | https://www.cbinsights.com/company/robin | Robin company reference |
| Envoy alternatives | https://www.elia.io/blog/envoy-alternatives | Envoy alt context |
| Envoy alternatives Dibsido | https://dibsido.com/envoy-alternatives-compared | Envoy alt context |
| Robin alternatives | https://www.skedda.com/insights/best-robin-alternatives | Robin alt context |
| Robin pricing | https://www.vendr.com/marketplace/robin | Robin pricing reference |
| Workplace management 2026 | https://www.maptician.com/guide/8-best-workplace-management-software-platforms-for-hybrid-offices-in-2026/ | Workplace platform landscape |
| Secureframe SOC 2 vs questionnaires | https://secureframe.com/blog/soc-2-vs-security-questionnaires | `vendor-risk-assessment-dpa` (73% SOC 2 + 70% questionnaires) |
| SOC2 Auditors questionnaire guide | https://soc2auditors.org/insights/vendor-security-questionnaire-guide/ | Questionnaire framework |
| NMS Consulting vendor risk checklist | https://nmsconsulting.com/vendor-risk-management-checklist/ | Vendor risk practice |
| Censinet SOC 2 in vendor risk | https://censinet.com/perspectives/soc-2-reports-in-vendor-risk-assessments-key-use-cases | SOC 2 use cases in vendor risk |
| Copla 2026 vendor security guide | https://copla.com/blog/third-party-risk-management/guide-to-vendor-security-and-risk-assessment-questionnaires/ | DPA checklist standard |
| UpGuard SOC 2 third-party | https://www.upguard.com/blog/soc-2-third-party-requirements | SOC 2 third-party requirements |
| Secureframe SOC 2 checklist 2026 | https://secureframe.com/blog/soc-2-compliance-checklist | SOC 2 + Data retention compliance |
| Atlas Systems vendor risk checklist 2026 | https://www.atlassystems.com/blog/vendor-risk-assessment-checklist-key-questions | Vendor risk practice |
| SecureSlate questionnaire questions | https://getsecureslate.com/blog/10-important-questions-security-questionnaire-with-examples | Questionnaire question bank |
| Cynomi vendor risk assessment | https://cynomi.com/learn/vendor-risk-assessment-questionnaire/ | Risk assessment standard |
| BuildMVPFast AI internal wikis | https://www.buildmvpfast.com/blog/ai-internal-wiki-knowledge-base-notion-confluence-alternative-2026 | `internal-knowledge-base-notion-slab-tettra` (Notion Agents) |
| Taskade AI wiki tools 2026 | https://www.taskade.com/blog/ai-wiki-tools | KB landscape 2026 |
| Waybook best KB software 2026 | https://www.waybook.com/blog/best-knowledge-base-software | KB landscape |
| Docsie Confluence vs Notion 2026 | https://www.docsie.io/blog/articles/confluence-vs-notion-comparison-2026/ | Confluence Rovo 2026 |
| SIIT company wiki software 2026 | https://www.siit.io/blog/best-company-wiki-software | KB landscape |
| Docmost Slab alternatives | https://docmost.com/blog/slab-alternatives/ | Slab alt context |
| Coworker AI knowledge mgmt 2026 | https://coworker.ai/blog/knowledge-management-tools | KB enterprise landscape |
| Slite KB software 2026 | https://slite.com/learn/knowledge-base-softwares | Slab free <10 users |
| Slite Confluence alternatives 2026 | https://slite.com/learn/confluence-alternatives | Confluence alt context |
| Buildin AI KB tools | https://buildin.ai/blog/best-ai-powered-knowledge-base-tools | AI KB tools |
| Daniele Procida Divio Documentation System | https://documentation.divio.com/ | Divio/Diátaxis taxonomy standard |
| Google SRE Postmortem Culture | https://sre.google/sre-book/postmortem-culture/ | Blameless post-mortem template |
| NIST AI Risk Management Framework | https://www.nist.gov/itl/ai-risk-management-framework | AI policy framework |
| ISO/IEC 42001 AI Management System | https://www.iso.org/standard/81230.html | AI policy framework |
| Anthropic Responsible Use | https://www.anthropic.com/responsible-use | AI policy guidance |
| Checkr API | https://www.checkr.com/api | Background check API |
| GoodHire | https://www.goodhire.com/ | Background check |
| PagerDuty Process Automation | https://www.pagerduty.com/products/process-automation/ | Incident process automation |
| Incident.io | https://incident.io/ | Incident management |
| Ramp Procurement | https://ramp.com/procurement/ | `procurement-playbook-intake-renewal` |

---

## Notes on authored-from-synthesis

Sections that aren't directly lifted from a single source (these are operational glue, not domain claims):

- **Always-disclose footer** ("defer to `legal-counsel` for binding employment-law / vendor-contract / insurance-binder review") — operational discipline per the seed prompt + standard ops practice; not a single citable source.
- **Day-0 / Day-1 / Week-1 / 30-60-90 onboarding cadence** — synthesized from common ops practice (FAANG onboarding, common HR-program design); no single canonical source.
- **State-specific final-paycheck rules** — based on actual state labor codes (CA Labor Code § 226 / 227.3; IL Wage Payment Act 820 ILCS 115; MA Wage Act c.149 § 148) but specific implementation deferred to `legal-counsel` for binding interpretation.
- **Provisioning matrix per role** — synthesized from common SaaS-app provisioning patterns; not lifted from one source.
- **Onboarding plan template** — synthesized from common ops deliverables; multiple conventions exist.
- **Vendor evaluation 1-page memo template** — synthesized from common procurement deliverables.
- **Spend audit deck template** — synthesized from common ops review deliverables.
- **Comp-decision matrix** (rating × base raise × equity refresh × bonus % × promo) — synthesized from common comp-cycle conventions; specific %s are common practitioner ranges.
- **Antipattern catalog** — each antipattern grounds in a specific industry convention (SCIM provisioning practice, SOC 2 vendor review per Secureframe, blameless post-mortem per Google SRE), but the BAD / GOOD pairing format is editorial.
- **Renewal calendar template + intake form template** — synthesized from common ops automation patterns.
- **Per-country gotchas** (UK / Germany / France / Singapore / Australia / Brazil / India / Canada / Mexico) — based on actual labor codes (UK Working Time Regulations; Germany BetrVG; France Code du Travail; CLT Brazil; Fair Work Act AU; Singapore Employment Act; Mexico LFT) but specific implementation deferred to `legal-counsel` for binding interpretation.
- **AI policy framework integration** — composition referencing NIST AI RMF + ISO 42001 + EU AI Act + Anthropic guidance; specific implementation per company stage is editorial.
- **PROACTIVE.md self-init footer** — standard `METHODOLOGY.md` pattern, only the routine questions changed to match ops workflow.
- **Hand-off matrix to sibling agents** — seed-prompt-driven; `ceo-agent`, `compliance-agent` are forward references to agents not yet in the catalog as of build date.

The base claims (SOC 2 + DPA structure, GDPR Art. 17, CCPA delete-request, Divio doc taxonomy, Google SRE blameless post-mortem, NIST AI RMF, ISO 42001, Brex acquisition by Capital One April 2026, Kandji rebrand to Iru Oct 2025, n8n 2.0 Jan 2026 LangChain integration, Robin 2026 Gartner MQ Leader, Tropic 2025 top-10 = 74% benchmark, BrexPay for Navan Oct 2024 launch, Pebl rebrand from Velocity Global Sept 2025, Deel = only EOR with public API + sandbox + webhooks pre-contract, Greenhouse 7,500+ customers + #1 G2 Winter 2026, 15Five $9-15 PEPM, WorkOS 4-week→4-day SAML integration, Auth0 decade leader for Series A-B, Stytch B2B seed sweet spot, Iru six-product unified platform) are all sourced to the 2026 industry guides cited in the table above.

---

## How to update this agent

1. Re-fetch the SOTA tool source URLs listed above; check for API changes, new MCP servers, pricing changes, platform launches / acquisitions / rebrands.
2. Update the per-tool SOTA tool reference in `role.md` if anything has changed materially (e.g., further M&A in HRIS / MDM / EOR space).
3. Update `agent.yaml` `mcp_servers` if a new ops MCP enters the catalog (e.g., a future Greenhouse MCP, Ashby MCP, Rippling MCP, Deel MCP, Okta MCP, Iru MCP, n8n MCP, Lattice MCP).
4. Update `reference/SOTA_USE_CASES.md` confidence ratings if a paid integration becomes free or vice versa.
5. Re-run `python verify.py operations-agent` to confirm structure intact.
6. Re-build: `python build.py operations-agent` produces a fresh `.craftbot`.

For the canonical reference repos (Step 2 of methodology), recheck quarterly:
- `wshobson/agents` (plugins/people-ops, plugins/operations — none as of build date)
- `VoltAgent/awesome-claude-code-subagents` (categories/people-ops or operations — recheck)
- `msitarzewski/agency-agents` (HR / ops / procurement specialists — recheck)
- `JSONbored/claudepro-directory` — search for ops / hr / procurement / internal-tools / mdm skills

When SOTA changes materially (new model launch, API endpoint change, platform acquisition closes, new MCP enters CraftBot catalog, new state labor-law change), update the relevant bundled skill pack's `SKILL.md` first, then the SOTA tool source table here.
