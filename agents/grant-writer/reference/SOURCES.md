# Grant Writer — Source Attribution

This file maps every section of `soul.md` and `role.md` back to the SOTA research that informed it. It is part of the bundle but is **not** loaded into the agent's context — it exists for human verification and future updates.

Upstream agent definitions were not downloaded in the v1 build pass; the v1 SOTA mapping was derived from web research (2026 sources cited below) plus the seeds in the per-agent build prompt. See `reference/INVENTORY.md` for the upstream-pull plan in v2.

---

## soul.md → source map

| Section in soul.md | Source(s) |
|---|---|
| Opening persona intro (action verbs) | METHODOLOGY.md operator framing rule + composition synthesis from `reference/SOTA_USE_CASES.md` Step 4 research |
| Three load-bearing convictions | Composition synthesis from build prompt + sector consensus (Spark the Fire, Get Fully Funded, Grant Writing Academy) |
| "Always disclose consult-a-professional" rider | `legal-counsel/soul.md` disclosure pattern + `finance-controller/soul.md` accounting rider |
| Purpose | Composition synthesis informed by every SOTA_USE_CASES.md row |
| Execution stack | `reference/SOTA_USE_CASES.md` — top SOTA per use case + Grants.gov / SAM.gov / Candid / Instrumentl + Sopact + eCFR + ProPublica + Benevity / YourCause / Bonterra |
| When invoked — Prospect research mode | https://open.gsa.gov/api/get-opportunities-public-api/ + https://projects.propublica.org/nonprofits/api + https://www.instrumentl.com/ + https://candid.org/ |
| When invoked — LOI mode | https://www.northwestern.edu/foundationrelations/grant-writing-guide/proposal-resources/letter-of-inquiry/ + https://getfullyfunded.com/how-to-write-a-killer-letter-of-inquiry-loi-to-get-a-grant/ |
| When invoked — Full proposal mode | https://giddingsconsulting.com/blog/grant-proposal-template-nonprofit/ + https://www.cms.gov/about-cms/work-us/cms-grants/cooperative-agreements/how-apply-cms-grants/cms-guidance-preparing-budget-request-and-narrative |
| When invoked — Logic model mode | https://www.sopact.com/use-case/logic-model + https://wkkf.issuelab.org/resource/logic-model-development-guide.html + https://www.sopact.com/use-case/theory-of-change-vs-logic-model |
| When invoked — Budget narrative mode | https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-E/subject-group-ECFRd93f2a98b1f6455 + CMS budget narrative guidance |
| When invoked — Grants.gov submission mode | https://sam.gov/workspace + https://www.grants.gov/forms/sf-424-family.html + https://open.gsa.gov/api/get-opportunities-public-api/ |
| When invoked — Grant reporting mode | https://www.grants.gov/forms/post-award-reporting-forms.html + SF-425 + SF-PPR template guidance |
| When invoked — Cultivation mode | https://www.insidephilanthropy.com/explainers/what-is-a-letter-of-inquiry-loi + Northwestern Foundation Relations guide |
| When invoked — Compliance audit mode | https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200 + https://grantedai.com/blog/federal-grants-regulatory-overhaul-2026 |
| When invoked — Declined-grant iteration mode | https://grantwritingacademy.substack.com/p/tracking-patterns-in-rejections-the + https://fundingforgood.org/rejected-what-to-do-if-your-grant-proposal-is-denied/ |
| Core operating rules (18 bullets) | Synthesis of sector consensus: 2 CFR 200 (allowability), Grants.gov SAM verification, Sopact logic-model priority, Grant Writing Academy portfolio-level patterns, professional-disclosure pattern (lifted from `legal-counsel`) |
| Mode-specific decisions | `reference/SOTA_USE_CASES.md` Step 4 Phase B research |
| Quality gates | Composition synthesis informed by per-mode 2026 SOTA practice |
| Output format | Composition synthesis (`.docx` standard + `.xlsx` budgets + Notion pipeline) |
| Communication style | `finance-controller/soul.md` direct-but-empathetic pattern + sector style (Grant Writing Academy, Spark the Fire) |
| When to push back | Composition synthesis from rule application + funder-priority match rule |
| When to defer | Build prompt sibling-agent specs + composition synthesis |
| PROACTIVE self-init footer | METHODOLOGY.md standard footer + role-specific questions from build prompt |
| Closing rule | Restatement of three convictions + professional-disclosure rider |

---

## role.md → source map

| Section in role.md | Source(s) |
|---|---|
| Capability reference → Funder ecosystem map | Sector consensus (Candid + Instrumentl + Spark the Fire + Grant Writing Academy) |
| Capability reference → Federal cost principles | https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200 + https://clarknuber.com/articles/uniform-guidance-the-de-minimis-indirect-cost-rate-updated/ + https://grantedai.com/blog/federal-grants-regulatory-overhaul-2026 |
| Capability reference → SF-424 family forms | https://www.grants.gov/forms/forms-repository/sf-424-family + https://www.grants.gov/forms/sf-424-mandatory-family.html |
| Capability reference → Foundation databases | https://sparkthefiregrantwriting.com/blog/best-grant-prospect-research-databases-of-2026 + https://grantsights.com/blog/best-grant-research-tools-nonprofits-2026 + https://www.instrumentl.com/blog/best-grant-websites + https://empowerchangeconsulting.com/2025/07/31/instrumentl-vs-candid-vs-grantstation-2025-which-grant-platform-fits-small-nonprofits/ |
| Capability reference → Submission portals | https://submit.com/resources/blog/best-grant-management-software-for-nonprofits-2026/ + https://www.plinth.org.uk/en-US/complete-guide/grant-management-systems-compared + https://theleadpastor.com/tools/best-grant-management-software/ |
| Capability reference → Donor / grant CRM tier | https://nonprofitpoint.com/best-crm-for-nonprofits/ + https://cube84.com/blog/bloomerang-vs-salesforce-nonprofit-cloud-vs-npsp-which-crm-is-best-for-your-nonprofit + https://bloomerang.com/blog/nonprofit-crm/ |
| Capability reference → Fiscal sponsorship models | https://www.fiscalsponsors.org/ + https://www.501c3.org/what-is-a-fiscal-sponsor/ + https://joinit.com/blog/fiscal-sponsorship-organizations + https://www.councilofnonprofits.org/running-nonprofit/administration-and-financial-management/fiscal-sponsorship-nonprofits |
| Capability reference → CSR / corporate giving platforms | https://benevity.com/ + https://www.bonterratech.com/ + https://www.goodera.com/ + https://movingworlds.org/ + https://stratuslive.com/blog/7-best-workplace-giving-platforms/ + https://www.vantagecircle.com/en/blog/best-employee-giving-software/ |
| Federal grant compliance playbook | https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200 + https://grantedai.com/blog/omb-uniform-guidance-overhaul-2-cfr-200-may-29-2026-pre-issuance-political-review-october-1-effective-strategy + https://grantsights.com/blog/2-cfr-200-uniform-guidance-guide |
| LOI playbook | https://www.northwestern.edu/foundationrelations/grant-writing-guide/proposal-resources/letter-of-inquiry/ + https://getfullyfunded.com/how-to-write-a-killer-letter-of-inquiry-loi-to-get-a-grant/ + https://sparkthefiregrantwriting.com/blog/loi + https://www.cummingsfoundation.org/grants/pdfs/LOI-Guide-Sample.pdf |
| Full proposal playbook | https://giddingsconsulting.com/blog/grant-proposal-template-nonprofit/ + https://www.grantbite.com/en/blog/grant-proposal-templates-free-downloads + https://www.thompsongrants.com/blog/sample-grant-proposal-template/ + https://opengrants.io/grant-budget-narrative-example-numbers-changed/ |
| Logic model playbook | https://www.sopact.com/use-case/logic-model + https://wkkf.issuelab.org/resource/logic-model-development-guide.html + https://www.sopact.com/use-case/theory-of-change-vs-logic-model + https://extension.okstate.edu/fact-sheets/understanding-and-building-logic-models-for-grants.html |
| Budget narrative playbook | https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-E/subject-group-ECFRd93f2a98b1f6455 + https://www.cms.gov/about-cms/work-us/cms-grants/cooperative-agreements/how-apply-cms-grants/cms-guidance-preparing-budget-request-and-narrative + https://opengrants.io/grant-budget-narrative-example-numbers-changed/ + https://technicalwriterhq.com/writing/grant-writing/grant-proposal-budget-template/ |
| Grants.gov submission playbook | https://sam.gov/workspace + https://www.grants.gov/forms/sf-424-family.html + https://open.gsa.gov/api/get-opportunities-public-api/ + https://www.grants.gov/forms.html |
| Grant reporting playbook | https://www.grants.gov/forms/post-award-reporting-forms.html + SF-425 + SF-PPR template guidance |
| Foundation cultivation playbook | https://www.northwestern.edu/foundationrelations/grant-writing-guide/proposal-resources/letter-of-inquiry/ + https://www.insidephilanthropy.com/explainers/what-is-a-letter-of-inquiry-loi + https://nonprofitpoint.com/best-crm-for-nonprofits/ |
| Declined-grant analysis playbook | https://grantwritingacademy.substack.com/p/tracking-patterns-in-rejections-the + https://fundingforgood.org/rejected-what-to-do-if-your-grant-proposal-is-denied/ + https://www.fundrobin.com/articles/thought-leadership/nonprofit-grant-rejection-smart-matching-solution/ + https://grantedai.com/blog/national-science-foundation-rejection-rates-what-to-know |
| Indirect cost reference | https://clarknuber.com/articles/uniform-guidance-the-de-minimis-indirect-cost-rate-updated/ + https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-E/subject-group-ECFRd93f2a98b1f6455 + https://grantedai.com/blog/indirect-cost-rate-negotiation-first-time-grantees |
| SF-424 family reference | https://www.grants.gov/forms/forms-repository/sf-424-family + https://www.grants.gov/forms/sf-424-mandatory-family.html + https://www.grants.gov/forms/forms-repository/sf-424-short-organization-family + https://www.grants.gov/forms/forms-repository/sf-424-individual-family |
| Single Audit reference | https://www.fac.gov/audit-resources/submission-guide/about/ + https://grantedai.com/blog/single-audit-threshold-1-million-nonprofit-compliance-uniform-guidance-strategy-2026 + https://www.councilofnonprofits.org/running-nonprofit/nonprofit-audit-guidec/federal-law-audit-requirements + https://hbkcpa.com/insights/first-time-single-audit-nonprofit-federal-funding/ |
| Fiscal sponsorship reference | https://www.fiscalsponsors.org/ + https://www.501c3.org/what-is-a-fiscal-sponsor/ + https://joinit.com/blog/fiscal-sponsorship-organizations + https://www.councilofnonprofits.org/running-nonprofit/administration-and-financial-management/fiscal-sponsorship-nonprofits |
| Corporate giving reference | https://benevity.com/ + https://www.bonterratech.com/ + https://www.goodera.com/ + https://movingworlds.org/ + https://stratuslive.com/blog/7-best-workplace-giving-platforms/ |
| SOTA tool reference (per-tool subsections) | `reference/SOTA_USE_CASES.md` + per-tool URLs in SOTA sources table below |
| SOTA execution playbook | `reference/SOTA_USE_CASES.md` summary table |

---

## Notes on "authored from synthesis"

Sections composed locally rather than lifted from a single source (all operational glue, not domain claims):

- **Three load-bearing convictions** — distilled from sector consensus across Spark the Fire / Get Fully Funded / Grant Writing Academy + Sopact logic-model priority + SOTA_USE_CASES.md research.
- **When to push back / When to defer** — operational glue derived from rule application + sibling-agent specs in the per-agent build prompt.
- **First-conversation PROACTIVE questions** — adapted from the standard METHODOLOGY.md PROACTIVE pattern; the 3 role-specific questions (org type / funding mix / next 90-day deadline) come from the build prompt.
- **Communication style examples** — phrasings composed to model the "direct but empathetic + funder-language-mirror" tone derived from the role.

These are operational glue; they do not introduce knowledge claims that lack a source.

---

## How to update this agent

If you want to refresh content from upstream:

1. Re-fetch the SOTA tool URLs listed below to confirm endpoints + pricing + features haven't changed.
2. Update `reference/SOTA_USE_CASES.md` confidence ratings if applicable.
3. Update the corresponding sections of `soul.md` / `role.md` / `USE_CASES.md` to match.
4. Update this `SOURCES.md` table if sections moved or sources were superseded.
5. Re-run `python verify.py grant-writer` to confirm structure intact.
6. Re-build: `python build.py grant-writer` produces a fresh `.craftbot`.

The sources are stored with full URLs, so the update path is mechanical and traceable.

---

## SOTA sources (June 2026)

The `role.md → SOTA tool reference (June 2026)` section and the bundled SOTA skill packs (`skills/grant-prospect-research-grants-gov-instrumentl-candid/`, `skills/loi-letter-of-inquiry-drafting/`, etc.) trace to these primary sources. Each row pairs the tool with the canonical URL the agent consulted.

| Tool / framework | Source | Used in |
|---|---|---|
| Grants.gov Get Opportunities Public API | https://open.gsa.gov/api/get-opportunities-public-api/ | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` + `skills/grants-gov-sam-gov-submission/SKILL.md` |
| SAM.gov Opportunity Management API | https://open.gsa.gov/api/opportunities-api/ | `skills/grants-gov-sam-gov-submission/SKILL.md` |
| SAM.gov Workspace | https://sam.gov/workspace | `skills/grants-gov-sam-gov-submission/SKILL.md` |
| ProPublica Nonprofit Explorer API v2 | https://projects.propublica.org/nonprofits/api | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| ProPublica Nonprofit Explorer (project) | https://projects.propublica.org/nonprofits/ | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| Candid (post-merger Search) | https://candid.org/ | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| Candid pricing comparison 2026 | https://sparkthefiregrantwriting.com/blog/best-grant-prospect-research-databases-of-2026 | `reference/SOTA_USE_CASES.md` |
| Instrumentl | https://www.instrumentl.com/ | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` + `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| Instrumentl best grants websites 2026 | https://www.instrumentl.com/blog/best-grant-websites | `reference/SOTA_USE_CASES.md` |
| GrantStation | https://www.grantstation.com/ | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| Grantable | https://grantable.co/ | `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md` |
| GrantBoost | https://www.grantboost.io/ | `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md` |
| FundRobin | https://www.fundrobin.com/ | `skills/declined-grant-iteration/SKILL.md` |
| Best AI grant writing tools 2026 | https://grantedai.com/blog/best-ai-grant-writing-tools-2026 | `reference/SOTA_USE_CASES.md` |
| Grant Assistant by FreeWill | https://www.grantassistant.ai/resources/articles/the-best-ai-grant-writing-tools-for-nonprofits-in-2026 | `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md` |
| 2 CFR Part 200 (Uniform Guidance) | https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200 | `skills/federal-grant-compliance-omb-uniform-guidance/SKILL.md` + `skills/budget-narrative-justification/SKILL.md` |
| 2 CFR 200.306 (cost sharing / matching) | https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D/subject-group-ECFR2afe8a0b08d1cdc/section-200.306 | `skills/matching-funds-in-kind-strategy/SKILL.md` |
| 2 CFR 200.331 (subrecipient mgmt) | https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D/section-200.331 | `skills/sf-424-sf-lll-subaward/SKILL.md` |
| 2 CFR 200 Subpart E (cost principles) | https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-E/subject-group-ECFRd93f2a98b1f6455 | `skills/budget-narrative-justification/SKILL.md` + `skills/indirect-cost-nicra/SKILL.md` |
| OMB May 29 2026 proposed rewrite | https://grantedai.com/blog/omb-uniform-guidance-overhaul-2-cfr-200-may-29-2026-pre-issuance-political-review-october-1-effective-strategy | `skills/federal-grant-compliance-omb-uniform-guidance/SKILL.md` |
| 2 CFR 200 2026 federal compliance guide | https://grantsights.com/blog/2-cfr-200-uniform-guidance-guide | `skills/federal-grant-compliance-omb-uniform-guidance/SKILL.md` |
| Clark Nuber — De Minimis 15% update | https://clarknuber.com/articles/uniform-guidance-the-de-minimis-indirect-cost-rate-updated/ | `skills/indirect-cost-nicra/SKILL.md` |
| NIH NOT-OD-26-072 / 45 CFR 75 reversion | https://grantedai.com/blog/federal-grants-regulatory-overhaul-2026 | `skills/indirect-cost-nicra/SKILL.md` + `skills/federal-grant-compliance-omb-uniform-guidance/SKILL.md` |
| Indirect cost rate negotiation (first-time) | https://grantedai.com/blog/indirect-cost-rate-negotiation-first-time-grantees | `skills/indirect-cost-nicra/SKILL.md` |
| Grants.gov SF-424 Family | https://www.grants.gov/forms/forms-repository/sf-424-family | `skills/sf-424-sf-lll-subaward/SKILL.md` |
| Grants.gov SF-424 Mandatory Family | https://www.grants.gov/forms/forms-repository/sf-424-mandatory-family | `skills/sf-424-sf-lll-subaward/SKILL.md` |
| Grants.gov SF-424 Short Org Family | https://www.grants.gov/forms/forms-repository/sf-424-short-organization-family | `skills/sf-424-sf-lll-subaward/SKILL.md` |
| Grants.gov SF-424 Individual Family | https://www.grants.gov/forms/forms-repository/sf-424-individual-family | `skills/sf-424-sf-lll-subaward/SKILL.md` |
| Grants.gov forms repository | https://www.grants.gov/forms.html | `skills/sf-424-sf-lll-subaward/SKILL.md` |
| SF-424 deep dive | https://www.oreateai.com/blog/demystifying-the-sf424-your-essential-guide-to-federal-grant-applications/284873268e0c08f2983f4c73a4d06ff0 | `skills/sf-424-sf-lll-subaward/SKILL.md` |
| Northwestern Foundation Relations LOI | https://www.northwestern.edu/foundationrelations/grant-writing-guide/proposal-resources/letter-of-inquiry/ | `skills/loi-letter-of-inquiry-drafting/SKILL.md` |
| Get Fully Funded — Killer LOI | https://getfullyfunded.com/how-to-write-a-killer-letter-of-inquiry-loi-to-get-a-grant/ | `skills/loi-letter-of-inquiry-drafting/SKILL.md` |
| Inside Philanthropy — LOI Explainer | https://www.insidephilanthropy.com/explainers/what-is-a-letter-of-inquiry-loi | `skills/loi-letter-of-inquiry-drafting/SKILL.md` + `skills/foundation-cultivation-program-officer/SKILL.md` |
| Spark the Fire — LOI Guide | https://sparkthefiregrantwriting.com/blog/loi | `skills/loi-letter-of-inquiry-drafting/SKILL.md` |
| Cummings Foundation LOI Guide | https://www.cummingsfoundation.org/grants/pdfs/LOI-Guide-Sample.pdf | `skills/loi-letter-of-inquiry-drafting/SKILL.md` |
| Sopact Logic Model | https://www.sopact.com/use-case/logic-model | `skills/logic-model-inputs-activities-outputs-outcomes/SKILL.md` |
| Sopact Theory of Change | https://www.sopact.com/use-case/theory-of-change | `skills/logic-model-inputs-activities-outputs-outcomes/SKILL.md` |
| Sopact ToC vs Logic Model | https://www.sopact.com/use-case/theory-of-change-vs-logic-model | `skills/logic-model-inputs-activities-outputs-outcomes/SKILL.md` |
| Sopact Logic Model Template | https://www.sopact.com/use-case/logic-model-template | `skills/logic-model-inputs-activities-outputs-outcomes/SKILL.md` |
| W.K. Kellogg Logic Model Guide | https://wkkf.issuelab.org/resource/logic-model-development-guide.html | `skills/logic-model-inputs-activities-outputs-outcomes/SKILL.md` |
| Oklahoma State Logic Models for Grants | https://extension.okstate.edu/fact-sheets/understanding-and-building-logic-models-for-grants.html | `skills/logic-model-inputs-activities-outputs-outcomes/SKILL.md` |
| Soukup Strategic — Logic Models for Grant Proposals | https://soukupstrategicsolutions.com/articles/grants/logic-models-grant-proposals/ | `skills/logic-model-inputs-activities-outputs-outcomes/SKILL.md` |
| CMS Budget Request + Narrative | https://www.cms.gov/about-cms/work-us/cms-grants/cooperative-agreements/how-apply-cms-grants/cms-guidance-preparing-budget-request-and-narrative | `skills/budget-narrative-justification/SKILL.md` |
| Federal Grant Compliance 2026 Federal Compliance | https://grantmetric.com/insights/federal-compliance-2026 | `skills/federal-grant-compliance-omb-uniform-guidance/SKILL.md` |
| OpenGrants Budget Narrative Example | https://opengrants.io/grant-budget-narrative-example-numbers-changed/ | `skills/budget-narrative-justification/SKILL.md` |
| Technical Writer HQ — Grant Budget Template | https://technicalwriterhq.com/writing/grant-writing/grant-proposal-budget-template/ | `skills/budget-narrative-justification/SKILL.md` |
| Instrumentl Grant Budget Examples | https://www.instrumentl.com/blog/grant-budget-examples | `skills/budget-narrative-justification/SKILL.md` |
| Giddings Consulting — Grant Proposal Template | https://giddingsconsulting.com/blog/grant-proposal-template-nonprofit/ | `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md` |
| Grantsights — Federal Grant Proposal 2026 | https://grantsights.com/blog/how-to-write-a-federal-grant-proposal | `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md` |
| Grantbite Grant Proposal Templates | https://www.grantbite.com/en/blog/grant-proposal-templates-free-downloads | `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md` |
| Thompson Grants — Sample Templates | https://www.thompsongrants.com/blog/sample-grant-proposal-template/ | `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md` |
| HRSA SAC Sample Budget Narrative | https://bphc.hrsa.gov/funding/funding-opportunities/service-area-competition/sac-sample-budget-narrative | `skills/budget-narrative-justification/SKILL.md` |
| IRS Tax Exempt Organization Search | https://apps.irs.gov/app/eos/ | `skills/irs-501c3-compliance-docs/SKILL.md` |
| Federal Audit Clearinghouse (fac.gov) | https://www.fac.gov/audit-resources/submission-guide/about/ | `skills/single-audit-prep-federal-750k/SKILL.md` |
| SF-SAC Section 3 federal audit findings | https://www.fac.gov/audit-resources/sf-sac/federal-awards-audit-findings/ | `skills/single-audit-prep-federal-750k/SKILL.md` |
| Single Audit Act + Threshold $1M | https://grantedai.com/blog/single-audit-threshold-1-million-nonprofit-compliance-uniform-guidance-strategy-2026 | `skills/single-audit-prep-federal-750k/SKILL.md` |
| Single Audit Requirements (LegalClarity) | https://legalclarity.org/single-audit-act-requirements-thresholds-and-compliance/ | `skills/single-audit-prep-federal-750k/SKILL.md` |
| Council of Nonprofits Federal Audit | https://www.councilofnonprofits.org/running-nonprofit/nonprofit-audit-guidec/federal-law-audit-requirements | `skills/single-audit-prep-federal-750k/SKILL.md` |
| First Single Audit Prep (HBK) | https://hbkcpa.com/insights/first-time-single-audit-nonprofit-federal-funding/ | `skills/single-audit-prep-federal-750k/SKILL.md` |
| Single Audit (Aplos) | https://www.aplos.com/glossary/single-audit | `skills/single-audit-prep-federal-750k/SKILL.md` |
| Thompson Grants Audit Checklist | https://www.thompsongrants.com/blog/audit-checklist/ | `skills/single-audit-prep-federal-750k/SKILL.md` |
| National Network of Fiscal Sponsors | https://www.fiscalsponsors.org/ | `skills/fiscal-sponsorship-coordination/SKILL.md` |
| 501c3.org — What Is a Fiscal Sponsor | https://www.501c3.org/what-is-a-fiscal-sponsor/ | `skills/fiscal-sponsorship-coordination/SKILL.md` |
| Council of Nonprofits Fiscal Sponsorship | https://www.councilofnonprofits.org/running-nonprofit/administration-and-financial-management/fiscal-sponsorship-nonprofits | `skills/fiscal-sponsorship-coordination/SKILL.md` |
| Join It — Fiscal Sponsorship Orgs | https://joinit.com/blog/fiscal-sponsorship-organizations | `skills/fiscal-sponsorship-coordination/SKILL.md` |
| Johnson Center — Fiscal Sponsorship Trend | https://johnsoncenter.org/blog/the-fiscal-sponsorship-model-a-growing-trend-in-the-nonprofit-sector/ | `skills/fiscal-sponsorship-coordination/SKILL.md` |
| Open Collective Foundation (dissolved 2024) | https://opencollective.foundation/ | `skills/fiscal-sponsorship-coordination/SKILL.md` (deprecated option) |
| NEO Philanthropy | https://neophilanthropy.org/services/fiscal-sponsorship/ | `skills/fiscal-sponsorship-coordination/SKILL.md` |
| Benevity Goodness Platform | https://benevity.com/ | `skills/corp-giving-csr-bumblebee-goodera/SKILL.md` |
| YourCause CSRconnect (Blackbaud) | https://www.blackbaud.com/products/yourcause-csrconnect | `skills/corp-giving-csr-bumblebee-goodera/SKILL.md` |
| Bonterra | https://www.bonterratech.com/ | `skills/corp-giving-csr-bumblebee-goodera/SKILL.md` |
| Bonterra Submittable alternatives | https://www.bonterratech.com/blog/submittable-alternatives | `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| Goodera | https://www.goodera.com/ | `skills/corp-giving-csr-bumblebee-goodera/SKILL.md` |
| Goodera Corporate Volunteer Programs | https://www.goodera.com/blog/corporate-volunteer-programs-examples | `skills/corp-giving-csr-bumblebee-goodera/SKILL.md` |
| Goodera Volunteering Software | https://www.goodera.com/blog/corporate-volunteering-software | `skills/corp-giving-csr-bumblebee-goodera/SKILL.md` |
| MovingWorlds | https://movingworlds.org/ | `skills/corp-giving-csr-bumblebee-goodera/SKILL.md` |
| MovingWorlds — CSR Corporate Giving | https://movingworlds.org/blog/beyond-tax-deductions-csr-corporate-giving-2026 | `skills/corp-giving-csr-bumblebee-goodera/SKILL.md` |
| MovingWorlds — Skills-Based Volunteering | https://movingworlds.org/blog/skills-based-volunteering-csr-software-for-employee-engagement/ | `skills/corp-giving-csr-bumblebee-goodera/SKILL.md` |
| Uncommon Giving — Volunteer Platforms | https://uncommongiving.com/uncommon-blog/corporate-volunteering-platform/ | `skills/corp-giving-csr-bumblebee-goodera/SKILL.md` |
| StratusLive — Workplace Giving Platforms | https://stratuslive.com/blog/7-best-workplace-giving-platforms/ | `skills/corp-giving-csr-bumblebee-goodera/SKILL.md` |
| VantageCircle — Corp Giving Platforms 2026 | https://www.vantagecircle.com/en/blog/best-employee-giving-software/ | `skills/corp-giving-csr-bumblebee-goodera/SKILL.md` |
| Independent Sector — Volunteer Time Value | https://independentsector.org/resource/value-of-volunteer-time/ | `skills/matching-funds-in-kind-strategy/SKILL.md` |
| Bloomerang | https://bloomerang.com/ | `skills/foundation-cultivation-program-officer/SKILL.md` + `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| Bloomerang Best Nonprofit CRM | https://bloomerang.com/blog/nonprofit-crm/ | `skills/foundation-cultivation-program-officer/SKILL.md` |
| DonorPerfect | https://www.donorperfect.com/ | `skills/foundation-cultivation-program-officer/SKILL.md` |
| Salesforce Nonprofit Cloud | https://www.salesforce.org/products/nonprofit-cloud/ | `skills/foundation-cultivation-program-officer/SKILL.md` |
| Bloomerang vs Salesforce NPC | https://cube84.com/blog/bloomerang-vs-salesforce-nonprofit-cloud-vs-npsp-which-crm-is-best-for-your-nonprofit | `skills/foundation-cultivation-program-officer/SKILL.md` |
| Nonprofit Point — Best CRM 2026 | https://nonprofitpoint.com/best-crm-for-nonprofits/ | `skills/foundation-cultivation-program-officer/SKILL.md` |
| Submittable | https://submit.com/ | `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| Submittable Best GMS 2026 | https://submit.com/resources/blog/best-grant-management-software-for-nonprofits-2026/ | `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| Fluxx Grantseeker | https://www.fluxx.io/products/grantseeker | `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| Foundant GrantHub | https://www.foundant.com/grant-management/ | `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| Plinth — Grant Mgmt Systems Compared | https://www.plinth.org.uk/en-US/complete-guide/grant-management-systems-compared | `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| LeadPastor — Best GMS 2026 | https://theleadpastor.com/tools/best-grant-management-software/ | `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| Instrumentl GMS Comparison | https://www.instrumentl.com/blog/best-grant-management-software | `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| Live Impact Best GMS 2026 | https://www.liveimpact.org/blog/best-grant-management-software-for-nonprofits | `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| Sopact Foundant alternative | https://www.sopact.com/use-case/foundant-alternatives | `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| Sopact — Grant Management Software | https://www.sopact.com/use-case/grant-management-software | `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| Grant Ready KY — Build Grant Calendar | https://www.grantreadyky.org/learn/resources/how-to-build-a-grant-calendar-without-expensive-software | `skills/grant-deadline-calendar-management/SKILL.md` |
| Grants.com — Build Grant Calendar 2026 | https://grants.com/step-by-step-guide-to-building-a-grant-calendar-that-maximizes-your-funding-chances-in-2026-ultimate-planner-for-nonprofits-small-businesses/ | `skills/grant-deadline-calendar-management/SKILL.md` |
| Grant Writing Academy — Rejections Patterns | https://grantwritingacademy.substack.com/p/tracking-patterns-in-rejections-the | `skills/declined-grant-iteration/SKILL.md` |
| Grant Writing Academy — Rejected Proposals | https://grantwritingacademy.substack.com/p/why-your-grant-proposals-keep-getting | `skills/declined-grant-iteration/SKILL.md` |
| Funding for Good — Rejected: What to Do | https://fundingforgood.org/rejected-what-to-do-if-your-grant-proposal-is-denied/ | `skills/declined-grant-iteration/SKILL.md` |
| FundRobin Smart Matching | https://www.fundrobin.com/articles/thought-leadership/nonprofit-grant-rejection-smart-matching-solution/ | `skills/declined-grant-iteration/SKILL.md` |
| Granted AI NSF Rejection Patterns | https://grantedai.com/blog/national-science-foundation-rejection-rates-what-to-know | `skills/declined-grant-iteration/SKILL.md` |
| Granted AI NSF Grant Review | https://grantsights.com/blog/how-nsf-grant-review-works | `skills/declined-grant-iteration/SKILL.md` |
| Mazlo — Building Resilient Nonprofit | https://www.mazlo.com/blog/when-federal-funding-vanishes-how-to-build-a-more-resilient-nonprofit | `skills/declined-grant-iteration/SKILL.md` |
| Instrumentl — Federal Funding Changes 2026 | https://www.instrumentl.com/blog/federal-funding-changes-report | `skills/declined-grant-iteration/SKILL.md` + `skills/federal-grant-compliance-omb-uniform-guidance/SKILL.md` |
| GrantStation — Federal Actions Tracking | https://grantstation.com/gs-insights/tracking-federal-actions-impacting-nonprofit-sector | `skills/federal-grant-compliance-omb-uniform-guidance/SKILL.md` |
| Crowell — 2 CFR 200 Rewrite Analysis | https://www.crowell.com/en/insights/client-alerts/grants-overhauled-what-the-proposed-rewrite-of-2-cfr-part-200-means-for-federal-financial-assistance-award-recipients | `skills/federal-grant-compliance-omb-uniform-guidance/SKILL.md` |
| NACO — OMB Grant Rules Overhaul | https://www.naco.org/news/omb-proposes-major-overhaul-federal-grant-rules | `skills/federal-grant-compliance-omb-uniform-guidance/SKILL.md` |
| Grant Bite — Free Templates 2026 | https://www.grantbite.com/en/blog/grant-proposal-templates-free-downloads | `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md` |
| OpenGrants — Top Foundation Platforms 2026 | https://opengrants.io/foundations-for-grants-for-nonprofits/ | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| GrantBoost — Best Databases Tested | https://www.grantboost.io/blog/Top-3-Grant-Databases/ | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| Funding for Good — Database Comparison | https://fundingforgood.org/comparing-grant-research-databases/ | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| Empower Change — Instrumentl vs Candid vs GrantStation | https://empowerchangeconsulting.com/2025/07/31/instrumentl-vs-candid-vs-grantstation-2025-which-grant-platform-fits-small-nonprofits/ | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| Spark the Fire — Database Comparison 2026 | https://sparkthefiregrantwriting.com/blog/best-grant-prospect-research-databases-of-2026 | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| Grantsights — Best Research Tools 2026 | https://grantsights.com/blog/best-grant-research-tools-nonprofits-2026 | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| Granted AI — AI Tools Tested on NIH NSF SBIR | https://grantedai.com/blog/best-ai-grant-writing-tools-2026 | `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md` |
| Best AI Grant Writing Tools 2026 (Grantsights) | https://grantsights.com/blog/best-ai-grant-writing-tools-2026 | `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md` |
| Grantable Best AI Tools | https://grantable.co/guides/ai-grant-writing-tools | `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md` |
| Grantboost AI Tools | https://www.grantboost.io/blog/Best-AI-Tools/ | `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md` |
| Grant Assistant by FreeWill | https://www.grantassistant.ai/resources/articles/the-best-ai-grant-writing-tools-for-nonprofits-in-2026 | `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md` |
| Bestagentpick — Best AI Tools | https://bestagentpick.com/best-ai-grant-writing-tools-2026/ | `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md` |
| AI Tools Bakery — Best AI Grant Writing | https://aitoolsbakery.com/blog/best-ai-grant-writing-tools/ | `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md` |
| Texas Tech AI Grant Prep Guide | https://guides.library.ttu.edu/grant | `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md` |
| Skywork — Grantboost 2026 | https://skywork.ai/slide/en/grant-writing-ai-2026590284334899200 | `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md` |
| Charity Charge — Grant Mgmt Software | https://www.charitycharge.com/nonprofit-resources/grant-management-software/ | `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| Grant Frog — Top GMS | https://grantfrog.com/5-best-grants-management-software/ | `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| Trust Radius — Foundant Alternatives | https://www.trustradius.com/products/foundant-grant-lifecycle-manager/competitors | `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| Open PR — Grant Mgmt Market 2026 | https://www.openpr.com/news/4441077/grant-management-software-market-is-going-to-boom-blackbaud | `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| Gitnux Best Grantmaker | https://gitnux.org/best/grantmaker-software/ | `skills/multi-grant-pipeline-mgmt/SKILL.md` |
| Authencio Donor Mgmt 2026 | https://www.authencio.com/blog/best-donor-management-software-for-nonprofits-guide | `skills/foundation-cultivation-program-officer/SKILL.md` |
| Live Impact Nonprofit Database 2026 | https://www.liveimpact.org/blog/best-nonprofit-database-software-7-options-for-2026 | `skills/foundation-cultivation-program-officer/SKILL.md` |
| Neon One — Best CRMs 2026 | https://neonone.com/resources/blog/crms-for-nonprofits/ | `skills/foundation-cultivation-program-officer/SKILL.md` |
| Danetsoft — Nonprofit CRM 2026 | https://www.danetsoft.com/post/nonprofit-crm-software-the-tools-driving-donor-engagement | `skills/foundation-cultivation-program-officer/SKILL.md` |
| Softabase — Bloomerang Review 2026 | https://softabase.com/software/crm/bloomerang | `skills/foundation-cultivation-program-officer/SKILL.md` |
| GrantPipe — Best CRM 2026 | https://grantpipe.com/resources/best/best-crm-for-nonprofit-organizations/ | `skills/foundation-cultivation-program-officer/SKILL.md` |
| Grant Frog Free GMS 2026 | https://theleadpastor.com/tools/best-free-grant-management-software/ | `skills/grant-deadline-calendar-management/SKILL.md` |
| Grants.com Build Grant Calendar | https://grants.com/how-to-create-a-grant-calendar-in-2026-that-skyrockets-your-funding-success-the-ultimate-expert-guide/ | `skills/grant-deadline-calendar-management/SKILL.md` |
| Cummings Foundation LOI Sample | https://www.cummingsfoundation.org/grants/pdfs/LOI-Guide-Sample.pdf | `skills/loi-letter-of-inquiry-drafting/SKILL.md` |
| USF Letter of Intent | https://www.usf.edu/arts-sciences/research-scholarship/priority-qa/loi.aspx | `skills/loi-letter-of-inquiry-drafting/SKILL.md` |
| International Foundation LOI | https://www.intlfoundation.org/page/application-process | `skills/loi-letter-of-inquiry-drafting/SKILL.md` |
| Ahmanson LOI | https://theahmansonfoundation.org/letter-of-inquiry/ | `skills/loi-letter-of-inquiry-drafting/SKILL.md` |
| Ellbogen LOI | https://ellbogenfoundation.org/letter-of-inquiry/ | `skills/loi-letter-of-inquiry-drafting/SKILL.md` |
| GrantWatch — How to Write LOI | https://www.grantwatch.com/grantnews/how-to-write-an-loi-letter-of-intent-letter-of-interest-letter-of-inquiry-3/ | `skills/loi-letter-of-inquiry-drafting/SKILL.md` |
| SAM.gov API Documentation 2026 | https://govconapi.com/sam-gov-api-guide | `skills/grants-gov-sam-gov-submission/SKILL.md` |
| SAM.gov API Complete Guide 2026 | https://govconapi.com/sam-gov-api-complete-guide | `skills/grants-gov-sam-gov-submission/SKILL.md` |
| SAM.gov API Management Automation | https://sam.gov/workspace/contract/opp/c1814850600e46a3a79e7badbbc333cb/view | `skills/grants-gov-sam-gov-submission/SKILL.md` |
| SAM.gov API (SamSearch glossary) | https://samsearch.co/glossary/sam-gov-api | `skills/grants-gov-sam-gov-submission/SKILL.md` |
| Apify SAM.gov Monitor | https://apify.com/m_mamaev/sam-gov-opportunities-monitor | `skills/grants-gov-sam-gov-submission/SKILL.md` |
| Apify SAM.gov Contracts | https://apify.com/skootle/sam-gov-federal-contracts/api | `skills/grants-gov-sam-gov-submission/SKILL.md` |
| Apify ProPublica Nonprofit Scraper | https://apify.com/lulzasaur/propublica-nonprofit-scraper | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| Apify IRS 990 Nonprofit Search | https://apify.com/ryanclinton/nonprofit-explorer | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| ProPublica 3M Tax Records | https://www.propublica.org/nerds/new-search-full-text-of-3-million-nonprofit-tax-records-for-free | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| Nonprofit Open Data Collective — ProPublica API | https://nonprofit-open-data-collective.github.io/propublica-api/ | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| Punderthings ProPublica 990 | https://github.com/Punderthings/propublica990 | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| RPublica R Package | https://ropengov.github.io/RPublica/ | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| ProPublica Nonprofit Explorer GH | https://github.com/Nonprofit-Open-Data-Collective/propublica-api/blob/main/index.rmd | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| US DOT Safe Streets SS4A Forms | https://www.transportation.gov/grants/ss4a/standard-forms | `skills/sf-424-sf-lll-subaward/SKILL.md` |
| Instrumentl Review 2026 (Grantsights) | https://grantsights.com/blog/instrumentl-review-2026 | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| Spark the Fire — Innovations 2026 | https://sparkthefiregrantwriting.com/blog/grant-prospecting-software-innovations | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| Spark the Fire — Grant Research Category | https://sparkthefiregrantwriting.com/blog/category/Grant+Research | `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md` |
| Granted AI — Federal Regulatory Overhaul | https://grantedai.com/blog/federal-grants-regulatory-overhaul-2026 | `skills/federal-grant-compliance-omb-uniform-guidance/SKILL.md` |
| Benevity GH (AI-Native Corp Purpose) | https://benevity.com/ | `skills/corp-giving-csr-bumblebee-goodera/SKILL.md` |
| Gartner — Volunteering Platform Reviews | https://www.gartner.com/reviews/market/corporate-volunteering-platform | `skills/corp-giving-csr-bumblebee-goodera/SKILL.md` |

These sources informed the `SOTA tool reference (June 2026)` section in `role.md`, the per-use-case mapping in `reference/SOTA_USE_CASES.md`, and the bundled SOTA skill packs.
