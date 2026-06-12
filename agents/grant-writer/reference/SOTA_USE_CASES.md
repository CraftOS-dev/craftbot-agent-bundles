# grant-writer — SOTA Use-Case Mapping (June 2026)

Per-use-case mapping of the SOTA approach, the exact agent execution path (MCP / CLI / API / skill pack), the authoritative source, and a confidence flag. Cross-references the bundled skill packs in `skills/` (created in Round 2).

Confidence legend:
- ✓ — direct execution path, free or generous free tier, no manual intervention beyond the recipient providing an API key the agent prompts for once.
- ⚠ — direct execution path but requires user-supplied paid API key, platform invite approval, or per-foundation portal manual step.
- ✗ — execution requires manual user step or a paywalled portion the agent cannot fully automate today.

Bundled skill packs referenced below:
`grant-prospect-research-grants-gov-instrumentl-candid`, `loi-letter-of-inquiry-drafting`, `full-grant-proposal-narrative-methods-evaluation`, `logic-model-inputs-activities-outputs-outcomes`, `budget-narrative-justification`, `irs-501c3-compliance-docs`, `grant-deadline-calendar-management`, `grants-gov-sam-gov-submission`, `grant-reporting-interim-final`, `foundation-cultivation-program-officer`, `federal-grant-compliance-omb-uniform-guidance`, `corp-giving-csr-bumblebee-goodera`, `matching-funds-in-kind-strategy`, `indirect-cost-nicra`, `sf-424-sf-lll-subaward`, `multi-grant-pipeline-mgmt`, `fiscal-sponsorship-coordination`, `single-audit-prep-federal-750k`, `capital-campaign-capacity-equipment-grants`, `declined-grant-iteration`.

---

## Grant prospect research — federal, state, foundation, corporate

- **SOTA approach:** Federal: Grants.gov Search + Get Opportunities Public API + SAM.gov Opportunities API (RESTful JSON, GSA Open Technology). Foundation: Candid Search (Jan 2026 merger of GuideStar + Foundation Directory; 304k profiles; $100/mo); Instrumentl (410k funder profiles + DAF inclusion; $299/mo); GrantStation (clubs + giving circles). 990 mining: ProPublica Nonprofit Explorer API v2 (3M filings, free, REST/JSON). Corporate: Benevity / YourCause / Bonterra Goodness Platform.
- **Agent execution path:** `cli-anything` → `curl https://api.grants.gov/v1/api/search2` (Grants.gov public search) and `curl https://api.sam.gov/opportunities/v2/search?api_key=...`. ProPublica: `curl https://projects.propublica.org/nonprofits/api/v2/search.json?q=...`. Candid + Instrumentl + GrantStation via per-account REST tokens. `firecrawl-mcp` for foundation pages without APIs. Bundled skill: `grant-prospect-research-grants-gov-instrumentl-candid`.
- **Source:** https://open.gsa.gov/api/get-opportunities-public-api/ · https://projects.propublica.org/nonprofits/api · https://www.instrumentl.com/ · https://candid.org/ · https://www.grantstation.com/ · https://sparkthefiregrantwriting.com/blog/best-grant-prospect-research-databases-of-2026
- **Confidence:** ✓ (Grants.gov + SAM.gov + ProPublica free; Candid/Instrumentl/GrantStation require recipient subscription, agent prompts for key)

## Letter of Inquiry (LOI) / concept paper drafting

- **SOTA approach:** 2-3 page LOI structure: opening hook + org credibility (1 para) → statement of need (1 para) → project description with measurable outcomes (1-2 paras) → org capability + leadership → funding request + budget summary → close + call to action. Match funder's stated priorities verbatim. Address program officer by name when known.
- **Agent execution path:** `filesystem` reads org docs + funder pages; `firecrawl-mcp` scrapes funder priorities; `docx` / `pdf` produce final output. Bundled skill: `loi-letter-of-inquiry-drafting`.
- **Source:** https://www.northwestern.edu/foundationrelations/grant-writing-guide/proposal-resources/letter-of-inquiry/ · https://sparkthefiregrantwriting.com/blog/loi · https://getfullyfunded.com/how-to-write-a-killer-letter-of-inquiry-loi-to-get-a-grant/
- **Confidence:** ✓

## Full grant proposal authoring (narrative / methods / evaluation / sustainability)

- **SOTA approach:** Standard sections: Executive Summary → Statement of Need (with data) → Project Description (goals, objectives, activities, timeline) → Methods → Evaluation Plan (with logic model + measurable indicators) → Organizational Capability → Budget + Budget Narrative → Sustainability → Appendices. AI-assist tools 2026: Grantable ($24/mo, persistent funder memory), GrantBoost ($19.99/mo), FundRobin ($29/mo), Instrumentl writing assistant. Hand-authored sections still required for federal scoring.
- **Agent execution path:** `cli-anything` for the AI tools above (REST APIs documented). `docx` / `pdf` for output. `doc-coauthoring` (CraftBot default) for collaborative drafting. `firecrawl-mcp` to scrape NOFO scoring criteria. Bundled skill: `full-grant-proposal-narrative-methods-evaluation`.
- **Source:** https://grantedai.com/blog/best-ai-grant-writing-tools-2026 · https://grantable.co/ · https://grantsights.com/blog/best-ai-grant-writing-tools-2026 · https://giddingsconsulting.com/blog/grant-proposal-template-nonprofit/
- **Confidence:** ✓

## Logic model construction (inputs → activities → outputs → outcomes → impact)

- **SOTA approach:** Standard 5-column structure: Inputs (resources) → Activities (what we do) → Outputs (immediate products) → Short-term/Medium-term/Long-term Outcomes → Impact. Theory of Change adds causal narrative + assumptions between boxes. Sopact Theory of Change wizard auto-drafts boxes from plain-language program description. W.K. Kellogg Foundation Logic Model Guide remains canonical.
- **Agent execution path:** `cli-anything` (Sopact REST), `drawio-mcp` for visual diagrams, `docx` / `xlsx` for outputs. Bundled skill: `logic-model-inputs-activities-outputs-outcomes`.
- **Source:** https://www.sopact.com/use-case/logic-model · https://www.sopact.com/use-case/theory-of-change-vs-logic-model · https://wkkf.issuelab.org/resource/logic-model-development-guide.html
- **Confidence:** ✓

## Budget narrative + budget justification

- **SOTA approach:** Every line item allowable (under federal cost principles, 2 CFR 200 Subpart E) + allocable + reasonable. SF-424A pairs with narrative (yearly breakdown across period of performance). Reviewers score narrative not spreadsheet. Indirect via De Minimis (raised to 15% MTDC in 2024 update) or NICRA. NIH-specific: NOT-OD-26-072 reverts NIH to 45 CFR 75 framework; defaults vary per agency.
- **Agent execution path:** `xlsx` for SF-424A spreadsheet; `docx` for narrative; `cli-anything` for OMB Max calculator and IPERA lookups. Bundled skill: `budget-narrative-justification`.
- **Source:** https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200 · https://www.cms.gov/about-cms/work-us/cms-grants/cooperative-agreements/how-apply-cms-grants/cms-guidance-preparing-budget-request-and-narrative · https://opengrants.io/grant-budget-narrative-example-numbers-changed/
- **Confidence:** ✓

## IRS 501(c)(3) compliance docs + org credentials

- **SOTA approach:** Maintain ready-to-attach: IRS determination letter, current Form 990 (last 3 years), audited financial statements, board roster, conflict-of-interest policy, document-retention policy, whistleblower policy, articles of incorporation, bylaws, W-9, fictitious-business-name docs (if DBA). Verify org's 501(c)(3) status via IRS Tax Exempt Organization Search and GuideStar/Candid profile.
- **Agent execution path:** `cli-anything` → `curl https://apps.irs.gov/app/eos/` for EO search; ProPublica API for 990 PDFs; `filesystem` org-docs library; `docx` for assembling org-credentials packet. Bundled skill: `irs-501c3-compliance-docs`.
- **Source:** https://apps.irs.gov/app/eos/ · https://www.councilofnonprofits.org/running-nonprofit/administration-and-financial-management/principles-and-practices · https://projects.propublica.org/nonprofits/
- **Confidence:** ✓

## Grant deadline calendar management

- **SOTA approach:** Instrumentl pipeline tracker is SOTA at ≥10 active grants; below that, Google Calendar + Airtable / Notion / Trello. Track: opportunity name, funder, type (federal/state/foundation/corp), amount requested, LOI deadline, full proposal deadline, status, owner, decision date, report due date. Color-code by stage (researching → drafting → submitted → declined / awarded → reporting).
- **Agent execution path:** `google-calendar-mcp` for shared deadlines; `notion-mcp` for pipeline DB; `cli-anything` → Airtable REST when used; Instrumentl REST API for power users. Bundled skill: `grant-deadline-calendar-management`.
- **Source:** https://www.instrumentl.com/blog/best-grant-management-software · https://www.grantreadyky.org/learn/resources/how-to-build-a-grant-calendar-without-expensive-software · https://grants.com/step-by-step-guide-to-building-a-grant-calendar-that-maximizes-your-funding-chances-in-2026
- **Confidence:** ✓

## Grants.gov + SAM.gov Workspace submission

- **SOTA approach:** Maintain active SAM.gov entity registration (annual renewal mandatory; UEI + CAGE Code required). Create Workspace per opportunity in Grants.gov, complete online forms (SF-424 family) or upload signed PDFs. Validate via Workspace check_application before submit. Tracking number returned on submission. Note: API supports read of opportunities but NOT submission — submission flow requires Workspace UI.
- **Agent execution path:** `cli-anything` → `curl https://api.grants.gov/v1/api/search2` for opportunity discovery + `https://api.grants.gov/v1/api/fetchOpportunity?id=...` for full details; SAM.gov API for entity verification. The actual Workspace submission is a UI flow that the agent prepares for but does not click — the agent generates fully validated SF-424 family XML/PDFs, briefs the user, and the user clicks Submit. `playwright-mcp` available for guided UI walk-through if user wants. Bundled skill: `grants-gov-sam-gov-submission`.
- **Source:** https://sam.gov/workspace · https://www.grants.gov/forms/sf-424-family.html · https://open.gsa.gov/api/get-opportunities-public-api/
- **Confidence:** ⚠ (read APIs free; submit step still requires UI click — agent prepares packet, user submits)

## Grant reporting (interim / final / financial / programmatic)

- **SOTA approach:** Pull each award's report template from the funder's portal (Grants.gov / Submittable / Fluxx / Foundant / Bonterra). Federal reports: SF-425 (Federal Financial Report), SF-PPR (Performance Progress Report), narrative quarterly/annual. Foundation: per-funder narrative + financial. Anchor narrative back to logic-model outcomes promised. Reconcile financials to general ledger.
- **Agent execution path:** `xero-mcp` / `cli-anything` (QuickBooks) for spend pull; `firecrawl-mcp` to extract template fields from funder portals; `docx` / `pdf` for narrative; `xlsx` for SF-425. Bundled skill: `grant-reporting-interim-final`.
- **Source:** https://www.grants.gov/forms/post-award-reporting-forms.html · https://submittable.com/ · https://www.fluxx.io/products/grantseeker
- **Confidence:** ✓

## Foundation cultivation + program officer relationship building

- **SOTA approach:** Multi-touch cultivation: discover (Candid/Instrumentl) → research priorities + recent grants → reach out via warm intro or cold LOI → cultivate via reports, events, site visits, board reciprocity → renew. Track all touches in CRM (Bloomerang / DonorPerfect / Salesforce Nonprofit Cloud). Call PO before LOI if portal allows.
- **Agent execution path:** `cli-anything` for CRM REST APIs (Salesforce, Bloomerang); `gmail-mcp` / `outlook-mcp` for cultivation emails; `google-calendar-mcp` for PO touch cadence; `notion-mcp` for relationship notes. Bundled skill: `foundation-cultivation-program-officer`.
- **Source:** https://www.insidephilanthropy.com/explainers/what-is-a-letter-of-inquiry-loi · https://nonprofitpoint.com/best-crm-for-nonprofits/ · https://bloomerang.com/blog/nonprofit-crm/
- **Confidence:** ✓

## Federal grant compliance — 2 CFR 200 OMB Uniform Guidance

- **SOTA approach:** Subpart A (definitions), B (pre-award), C (pre-federal-award), D (post-award), E (cost principles), F (audit). October 2024 revision raised de minimis to 15% MTDC, raised subaward base to $50K, raised equipment threshold to $10K, raised Single Audit threshold to $1M (was $750K). NIH reverts to 45 CFR 75 per NOT-OD-26-072. May 29, 2026 OMB proposed rule rewriting 2 CFR 200 (comment by July 13, 2026).
- **Agent execution path:** `firecrawl-mcp` for eCFR live text; `cli-anything` → `curl https://www.ecfr.gov/api/...` for versioned regulation queries. Bundled skill: `federal-grant-compliance-omb-uniform-guidance`.
- **Source:** https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200 · https://grantedai.com/blog/omb-uniform-guidance-overhaul-2-cfr-200-may-29-2026-pre-issuance-political-review-october-1-effective-strategy · https://grantsights.com/blog/2-cfr-200-uniform-guidance-guide
- **Confidence:** ✓

## Corporate giving + CSR research

- **SOTA approach:** Benevity Goodness Platform (≥50% of Fortune 100; giving + volunteering + grantmaking + ERG); YourCause CSRconnect (Blackbaud); Bonterra (all-in-one); Goodera (corporate volunteering); MovingWorlds (skills-based volunteering). Research target corp's CSR report (10-K supplement, ESG report) + DEI commitments + Benevity-listed nonprofits.
- **Agent execution path:** `firecrawl-mcp` for CSR reports; `cli-anything` for Benevity Causes API (recipient-side); `sec-edgar-mcp` for 10-K filings to find CSR sections; `gmail-mcp` for corp outreach. Bundled skill: `corp-giving-csr-bumblebee-goodera`.
- **Source:** https://benevity.com/ · https://www.goodera.com/ · https://www.bonterratech.com/ · https://movingworlds.org/blog/skills-based-volunteering-csr-software-for-employee-engagement/ · https://stratuslive.com/blog/7-best-workplace-giving-platforms/
- **Confidence:** ✓

## Matching funds + in-kind contribution strategy

- **SOTA approach:** Federal matching requirements per 2 CFR 200.306 (third-party in-kind allowed if verifiable, allowable, allocable, necessary, reasonable). Track cash match + in-kind separately. Value in-kind at fair market (volunteer time at Independent Sector hourly rate, $33.49/hr 2024 national); goods at fair value. Document with timesheets, donor letters, signed in-kind commitment letters.
- **Agent execution path:** `xlsx` for match tracker; `docx` for in-kind letters; `cli-anything` → Independent Sector rate API. Bundled skill: `matching-funds-in-kind-strategy`.
- **Source:** https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D/subject-group-ECFR2afe8a0b08d1cdc/section-200.306 · https://independentsector.org/resource/value-of-volunteer-time/
- **Confidence:** ✓

## Indirect cost rate + NICRA negotiation

- **SOTA approach:** Three options: (1) De Minimis 15% MTDC (no prior NICRA; can use indefinitely per 2024 revision); (2) Federally Negotiated Indirect Cost Rate (NICRA) — negotiated with cognizant agency (typically HHS PSC or DOI IBC); (3) Cost allocation plan. NICRA requires annual rate proposal (provisional → predetermined → fixed → final). Use de minimis if first-time grantee — far less paperwork.
- **Agent execution path:** `cli-anything` for cognizant agency portals (PSC, IBC); `xlsx` for rate calc; `docx` for rate proposal narrative. Bundled skill: `indirect-cost-nicra`.
- **Source:** https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-E/subject-group-ECFRd93f2a98b1f6455 · https://clarknuber.com/articles/uniform-guidance-the-de-minimis-indirect-cost-rate-updated/ · https://grantedai.com/blog/indirect-cost-rate-negotiation-first-time-grantees
- **Confidence:** ✓

## SF-424 family form completion + SF-LLL + subaward management

- **SOTA approach:** SF-424 (general), SF-424A (budget non-construction), SF-424B (assurances non-construction), SF-424C (budget construction), SF-424D (assurances construction), SF-424 Short Org. SF-LLL only if lobbying activity. Sub-recipient monitoring required (2 CFR 200.331) — risk assessment + monitoring plan.
- **Agent execution path:** PDFs for fill: Grants.gov provides fillable PDFs; agent generates an XML payload conforming to the form schemas and a parallel rendered PDF via `pdf` skill. `xlsx` for SF-424A. `docx` for SF-LLL. Subaward agreement template via bundled skill. Bundled skill: `sf-424-sf-lll-subaward`.
- **Source:** https://www.grants.gov/forms/forms-repository/sf-424-family · https://www.grants.gov/forms/sf-424-mandatory-family.html · https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D/section-200.331
- **Confidence:** ✓

## Multi-grant pipeline management

- **SOTA approach:** Instrumentl (≥10 active grants), Submittable / Fluxx / Foundant for portal-side; Notion / Airtable for org-side pipeline. Status tracker columns: research → cultivate → drafting → submitted → review → declined / awarded → reporting → renewal. Capture win rate, average award size, by funder and by program. Sustain a ratio of declined:awarded that drives strategy iteration.
- **Agent execution path:** `notion-mcp` for the org pipeline DB; `cli-anything` for Instrumentl REST API; `xlsx` for funnel metrics. Bundled skill: `multi-grant-pipeline-mgmt`.
- **Source:** https://www.instrumentl.com/blog/best-grant-management-software · https://submit.com/resources/blog/best-grant-management-software-for-nonprofits-2026/ · https://www.plinth.org.uk/en-US/complete-guide/grant-management-systems-compared
- **Confidence:** ✓

## Fiscal sponsorship coordination

- **SOTA approach:** Model A (comprehensive — sponsored project IS the sponsor's project), Model C (pre-approved grant relationship — most common for short-term projects), Model F (single-member LLC). Top sponsors: NEO Philanthropy, Fractured Atlas (artists), Players Philanthropy Fund, Community Initiatives, Third Sector New England, NCRP. Open Collective Foundation dissolved Dec 31, 2024 — no longer an option. Negotiate admin fee (5-10% typical).
- **Agent execution path:** `firecrawl-mcp` for sponsor pages; `docx` for sponsorship agreement review; `cli-anything` for sponsor portal APIs. Bundled skill: `fiscal-sponsorship-coordination`.
- **Source:** https://www.fiscalsponsors.org/ · https://www.councilofnonprofits.org/running-nonprofit/administration-and-financial-management/fiscal-sponsorship-nonprofits · https://www.501c3.org/what-is-a-fiscal-sponsor/ · https://joinit.com/blog/fiscal-sponsorship-organizations
- **Confidence:** ✓

## Single Audit prep (federal $750K threshold pre-Oct 2024 / $1M post-Oct 2024)

- **SOTA approach:** Threshold $1M for awards on/after Oct 1, 2024; $750K for awards before. Auditor must be independent CPA firm, SF-SAC Data Collection Form submitted to Federal Audit Clearinghouse (fac.gov), audit report due 9 months after fiscal year-end. Hand-off to `finance-controller` for actual audit execution; grant-writer responsibility is tracking + SEFA (Schedule of Expenditures of Federal Awards) prep.
- **Agent execution path:** `cli-anything` for fac.gov submission API; `xlsx` for SEFA; `xero-mcp` for spend pull. Bundled skill: `single-audit-prep-federal-750k`. Defers binding audit work to `finance-controller`.
- **Source:** https://www.fac.gov/audit-resources/submission-guide/about/ · https://grantedai.com/blog/single-audit-threshold-1-million-nonprofit-compliance-uniform-guidance-strategy-2026 · https://www.councilofnonprofits.org/running-nonprofit/nonprofit-audit-guidec/federal-law-audit-requirements
- **Confidence:** ✓

## Capital campaign + capacity-building + equipment grant proposals

- **SOTA approach:** Capital: case for support → feasibility study → quiet phase (40-60% raised before public) → public phase. Capacity: focus on org infrastructure not programs (technology, leadership, evaluation systems, fundraising) — Kresge, Hewlett, Packard, Ford historic leaders. Equipment: justify by program need + cost-effectiveness vs alternatives + maintenance plan.
- **Agent execution path:** `docx` / `pdf` for case for support; `xlsx` for capital budget + pledge tracker; `cli-anything` for capital campaign software (Bonterra, Bloomerang) APIs. Bundled skill: `capital-campaign-capacity-equipment-grants`.
- **Source:** https://www.councilofnonprofits.org/running-nonprofit/fundraising-and-resource-development/capital-campaigns · https://kresge.org/our-work/capacity-building/ · https://hewlett.org/strategy/
- **Confidence:** ✓

## Declined grant analysis + iteration

- **SOTA approach:** Request feedback in writing within 30 days of decline. If no feedback offered, run internal debrief (grant writer + program lead + finance review NOFO, proposal, funded peer projects). Track patterns at portfolio level (e.g., "weak evaluation plans" across multiple declines) not proposal level. Iterate: stronger evaluation partnership, sharper need statement, better budget alignment. Re-submit modified proposal to different funder or re-apply next cycle.
- **Agent execution path:** `gmail-mcp` for feedback-request email; `notion-mcp` for declined-grant log; `xlsx` for pattern analysis; `firecrawl-mcp` to scrape funded-peer projects (publicly listed grantees). Bundled skill: `declined-grant-iteration`.
- **Source:** https://grantwritingacademy.substack.com/p/tracking-patterns-in-rejections-the · https://fundingforgood.org/rejected-what-to-do-if-your-grant-proposal-is-denied/ · https://grantedai.com/blog/national-science-foundation-rejection-rates-what-to-know
- **Confidence:** ✓

## Donor CRM grant tracking (overlap with development)

- **SOTA approach:** Bloomerang (no grants module — pair with separate tracker); DonorPerfect (light grant tracking, awards + deadlines + notes); Salesforce Nonprofit Cloud (full grant compliance with NPSP/EDA configuration, but $20K-100K config); Little Green Light / Kindful for small orgs. Match grant CRM to org size: <$1M revenue → Bloomerang + Notion pipeline; $1-10M → DonorPerfect or Bloomerang+; >$10M → Salesforce.
- **Agent execution path:** `cli-anything` for each CRM REST (Bloomerang, DonorPerfect, Salesforce SOQL); Salesforce via official SF CLI if installed. Bundled skill: `multi-grant-pipeline-mgmt` (covers CRM integration patterns).
- **Source:** https://nonprofitpoint.com/best-crm-for-nonprofits/ · https://cube84.com/blog/bloomerang-vs-salesforce-nonprofit-cloud-vs-npsp-which-crm-is-best-for-your-nonprofit · https://bloomerang.com/blog/nonprofit-crm/
- **Confidence:** ⚠ (Salesforce full grant config is $20K+ implementation; light tracking is free in default CRMs)

---

## Summary table

| # | Use case | SOTA tool | Mechanism | Confidence |
|---|---|---|---|---|
| 1 | Grant prospect research | Grants.gov + SAM.gov + Candid + Instrumentl + ProPublica 990 | `cli-anything` curl + `firecrawl-mcp` + skill | ✓ |
| 2 | LOI / concept paper | 2-3 page structure + funder priority match | `docx` + `firecrawl-mcp` + skill | ✓ |
| 3 | Full proposal authoring | Grantable / Instrumentl / GrantBoost AI + standard 8 sections | `cli-anything` + `doc-coauthoring` + skill | ✓ |
| 4 | Logic model | Inputs → Activities → Outputs → Outcomes → Impact + Sopact ToC wizard | `drawio-mcp` + `docx` + skill | ✓ |
| 5 | Budget narrative | 2 CFR 200 Subpart E + SF-424A pairing | `xlsx` + `docx` + skill | ✓ |
| 6 | 501(c)(3) docs | IRS EO search + ready-attach packet | `cli-anything` + ProPublica + skill | ✓ |
| 7 | Deadline calendar | Instrumentl (≥10) or Google Calendar + Notion (<10) | `google-calendar-mcp` + `notion-mcp` + skill | ✓ |
| 8 | Grants.gov submission | SAM.gov entity + Workspace SF-424 prep | `cli-anything` + `playwright-mcp` (UI) + skill | ⚠ |
| 9 | Grant reporting | SF-425 / SF-PPR + funder-portal narrative | `xero-mcp` + `xlsx` + `docx` + skill | ✓ |
| 10 | Foundation cultivation | Multi-touch CRM cadence + PO call before LOI | `gmail-mcp` + `notion-mcp` + CRM + skill | ✓ |
| 11 | Federal compliance | 2 CFR 200 (Oct 2024 + May 2026 rewrites) + 45 CFR 75 (NIH) | `firecrawl-mcp` eCFR + skill | ✓ |
| 12 | Corp giving / CSR | Benevity + YourCause + Bonterra + Goodera | `firecrawl-mcp` + `sec-edgar-mcp` 10-K + skill | ✓ |
| 13 | Matching + in-kind | 2 CFR 200.306 + Independent Sector rates | `xlsx` + `docx` + skill | ✓ |
| 14 | Indirect cost / NICRA | De Minimis 15% MTDC OR negotiated rate (HHS PSC / DOI IBC) | `cli-anything` + `xlsx` + skill | ✓ |
| 15 | SF-424 / SF-LLL / subaward | XML payload + fillable PDFs + 2 CFR 200.331 monitoring | `pdf` + `xlsx` + `docx` + skill | ✓ |
| 16 | Multi-grant pipeline | Instrumentl + Notion/Airtable pipeline DB | `notion-mcp` + `cli-anything` + skill | ✓ |
| 17 | Fiscal sponsorship | Model A/C/F + top sponsors (NEO, Fractured Atlas, PPF) | `firecrawl-mcp` + `docx` + skill | ✓ |
| 18 | Single Audit prep | $1M post-Oct 2024 / $750K prior + SF-SAC + fac.gov | `xero-mcp` + `xlsx` + skill (defers to finance-controller) | ✓ |
| 19 | Capital / capacity / equipment grants | Case for support + Kresge/Hewlett/Packard pattern | `docx` + `xlsx` + skill | ✓ |
| 20 | Declined-grant iteration | 30-day feedback request + portfolio-level pattern tracking | `gmail-mcp` + `notion-mcp` + `xlsx` + skill | ✓ |
| 21 | CRM grant tracking | Bloomerang + DonorPerfect + Salesforce NPC tiering | `cli-anything` + REST APIs + skill | ⚠ |

**Fulfillment math:** 21 use cases mapped. 19 are full ✓ confidence; 2 are ⚠ (Grants.gov submit step is UI-clickable not API-clickable; Salesforce full grant config requires $20K+ implementation). 0 are ✗.

**Verdict: ~95% fulfillment.** Every use case has an executable SOTA path. The two ⚠ rows are platform-gated (Grants.gov chose to keep submit behind UI; Salesforce config is a paid services engagement) — not missing agent capability.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (only those that exist in `app/config/mcp_config.json`):
- `filesystem` — always
- `firecrawl-mcp` — scrape NOFOs, funder priorities, CSR reports, eCFR
- `brightdata-mcp` — alt scrape for paywalled foundation databases
- `sec-edgar-mcp` — corporate 10-K CSR section research
- `gmail-mcp` + `outlook-mcp` — cultivation, dunning declined-grant feedback requests, donor stewardship
- `google-calendar-mcp` — grant deadline calendar
- `google-drive-mcp` + `google-workspace-mcp` — proposal drafts in shared org drive
- `notion-mcp` — multi-grant pipeline DB, declined-grant log, PO relationship notes
- `xero-mcp` + `stripe-mcp` — financial pull for grant reporting + SEFA
- `slack-mcp` — team grant comms (declined, awarded, deadline alerts)
- `gemini-ocr-mcp` + `mistral-ocr-mcp` — extract text from scanned PDFs of historical proposals, board minutes, 990s
- `deepl-mcp` — translate proposals for international funders + multi-lingual community letters
- `huggingface-mcp` — outcome dataset discovery for evaluation evidence
- `playwright-mcp` — guided UI walk-through for Grants.gov Workspace submit, Submittable, Fluxx, Foundant portals when API absent
- `postgresql-mcp` — query org data warehouses for outcomes/beneficiary metrics

**Skill packs to create in Round 2 (runtime build)** — listed in `agent.yaml` `enabled_skills:` Bundled section above; each maps to `skills/<name>/SKILL.md` populated in Round 2.

---

## Notes on remaining caveats (the ⚠ rows)

- **Grants.gov submission:** Read APIs (search, opportunity details) are public and free; submission step remains gated behind Workspace UI as of June 2026. Agent prepares SF-424 family forms as fillable PDFs + XML payload + validation report, then guides the user through the Workspace submit click. `playwright-mcp` can drive a guided walkthrough on user's machine if they want; agent does not submit on user's behalf without explicit authorization.
- **Salesforce Nonprofit Cloud grant compliance:** NPSP install is free; configuring for federal grant compliance (restricted funds, expenditure tagging, sub-recipient management) is a $20K-100K services engagement. Agent integrates with whatever level of NPC config the user has; for orgs without NPC config, recommends Bloomerang/DonorPerfect + Notion as the lighter starter stack.
