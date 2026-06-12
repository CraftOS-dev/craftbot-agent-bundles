# Grant Writer — Use Cases

**Tier:** general · **Category:** fundraising
**Core job:** End-to-end grant writing operator — research, draft, submit, report, iterate. Covers federal / state / foundation / corporate funders for nonprofits, fiscally sponsored projects, and social enterprises.

> Ships with the SOTA 2026 grant-writing stack (Grants.gov + SAM.gov + Candid + Instrumentl + Grantable + Sopact + eCFR + ProPublica 990s + Benevity / YourCause / Bonterra) — executes the full grant lifecycle from prospect research to LOI to full proposal to SF-424 submission prep to grant reporting to declined-grant iteration. Always discloses "consult a licensed CPA / nonprofit attorney for binding compliance, tax, or audit decisions."

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Prospect research
- Federal grant discovery via Grants.gov + SAM.gov APIs
- Foundation discovery via Candid + Instrumentl + GrantStation + ProPublica 990
- Corporate giving research via SEC 10-K + CSR reports + Benevity/YourCause Causes
- DAF (donor-advised fund) discovery (Instrumentl unique)
- Alignment scoring + top-20 ranked prospect list

### Authoring
- Letter of Inquiry (LOI) drafting — 2-3 pg structure mirroring funder priorities
- Concept paper drafting
- Full proposal authoring — 8 standard sections (Exec Summary, Need, Project Description, Methods, Evaluation, Capability, Budget+Narrative, Sustainability)
- AI-assist via Grantable / GrantBoost / FundRobin / Instrumentl writing assistant
- Logic model construction (Inputs → Activities → Outputs → Outcomes → Impact)
- Theory of Change with causal narrative + assumption surfacing
- Budget narrative + budget justification (line-by-line allowable + allocable + reasonable)
- Sustainability planning

### Compliance + forms
- IRS 501(c)(3) compliance docs (determination letter, 990s, policies, board roster)
- SF-424 family completion (SF-424, SF-424A, SF-424B, SF-424C, SF-424D, Short Org, Mandatory, Individual)
- SF-LLL (Disclosure of Lobbying Activity)
- Federal grant compliance per 2 CFR 200 Subparts A-F (OMB Uniform Guidance) + 45 CFR 75 (NIH) + 2024 update + 2026 proposed rewrite
- Subaward management per 2 CFR 200.331 (risk assessment + monitoring plan + FFATA)
- Matching funds / in-kind strategy per 2 CFR 200.306 (Independent Sector volunteer rates)
- Indirect cost rate: de minimis 15% MTDC OR NICRA negotiation (HHS PSC / DOI IBC / DHHS CAS)

### Submission + reporting
- Grants.gov Workspace submission prep + SF-424 family XML payload + signed PDFs
- SAM.gov entity registration verification (UEI + CAGE Code; annual renewal)
- Playwright UI walkthrough for Grants.gov / Submittable / Fluxx / Foundant when API lacks submit endpoint
- Interim grant reports (SF-425 Federal Financial Report + SF-PPR Performance Progress Report)
- Final grant reports
- Funder-portal narrative for foundations (Submittable / Fluxx / Foundant / Bonterra / Blackbaud Grantmaking)
- Reconciliation of financial reports to general ledger via `xero-mcp`

### Pipeline + relationships
- Grant deadline calendar management (Instrumentl ≥10 grants; Google Calendar + Notion + Airtable <10)
- Multi-grant pipeline DB (research → cultivate → draft → submit → decide → report → renewal)
- Foundation cultivation cadence (12-month touch schedule)
- Program officer relationship management (CRM-tracked PO call → LOI → site visit → renewal)
- Donor CRM integration (Bloomerang / DonorPerfect / Salesforce Nonprofit Cloud / Little Green Light / Kindful)

### Strategy + iteration
- Funding mix analysis (federal vs state vs foundation vs corp vs individual)
- Declined-grant feedback request + portfolio-level pattern tracking + portfolio pivot
- Capital campaign proposal authoring (case for support + quiet/public phases)
- Capacity-building grant proposals (Kresge / Hewlett / Packard / Ford patterns)
- Equipment grants (justification + maintenance plan)
- Fiscal sponsorship coordination (Model A/C/F selection + sponsor matching)
- Multi-year grant projections + sustainability planning

### Audit + compliance ops
- Single Audit threshold tracking ($1M post-Oct 2024 / $750K prior)
- SF-SAC Data Collection Form prep + Federal Audit Clearinghouse (fac.gov) submission prep
- SEFA (Schedule of Expenditures of Federal Awards) prep
- Board / exec briefing on grant compliance posture

---

## Execution status (SOTA — June 2026)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Grant prospect research (federal) | Grants.gov + SAM.gov Get Opportunities Public APIs | `cli-anything` curl + `grant-prospect-research-grants-gov-instrumentl-candid` |
| Grant prospect research (foundation) | Candid Search ($100/mo post-merger) + Instrumentl ($299/mo) + GrantStation ($99/yr) | `cli-anything` curl + REST APIs + bundled skill |
| Grant prospect research (corp) | Benevity Causes + YourCause + Bonterra Causes + SEC 10-K + CSR reports | `firecrawl-mcp` + `sec-edgar-mcp` + bundled skill |
| 990 mining (free) | ProPublica Nonprofit Explorer API v2 (3M filings) | `cli-anything` curl + bundled skill |
| LOI / concept paper drafting | 2-3 pg structure mirroring funder priorities | `loi-letter-of-inquiry-drafting` + `docx` + `gmail-mcp` |
| Full proposal authoring | 8-section standard + AI-assist (Grantable / GrantBoost / FundRobin / Instrumentl) | `full-grant-proposal-narrative-methods-evaluation` + `cli-anything` + `docx` |
| Logic model + Theory of Change | 5-column Kellogg + Sopact wizard + `drawio-mcp` visualization | `logic-model-inputs-activities-outputs-outcomes` + `drawio-mcp` |
| Budget narrative + SF-424A | 2 CFR 200 Subpart E + Subpart D (200.306 match, 200.331 subaward) + CMS template | `budget-narrative-justification` + `xlsx` |
| IRS 501(c)(3) compliance packet | IRS EO search + ready-attach docs assembly | `irs-501c3-compliance-docs` + `cli-anything` + `docx` |
| Grant deadline calendar | Instrumentl (≥10 grants) OR `google-calendar-mcp` + `notion-mcp` + Airtable (<10) | `grant-deadline-calendar-management` |
| Grants.gov Workspace submission | SAM.gov entity active + Workspace SF-424 prep + Playwright UI walkthrough | `grants-gov-sam-gov-submission` + `playwright-mcp` |
| SF-424 family + SF-LLL forms | XML payload + fillable PDFs + 2 CFR 200.331 monitoring | `sf-424-sf-lll-subaward` + `pdf` + `xlsx` + `docx` |
| Grant reporting (federal SF-425 + SF-PPR) | GL pull via `xero-mcp` + reconcile to budget + outcome data vs logic-model targets | `grant-reporting-interim-final` + `xero-mcp` + `xlsx` + `docx` |
| Grant reporting (foundation portal) | Funder-portal narrative + financial reconciliation | `grant-reporting-interim-final` + `firecrawl-mcp` + `docx` |
| Foundation cultivation cadence | Multi-touch 12-month schedule + PO call before LOI + CRM tracking | `foundation-cultivation-program-officer` + `gmail-mcp` + `notion-mcp` + `google-calendar-mcp` |
| Federal compliance (2 CFR 200 + 45 CFR 75) | eCFR live regulation queries + 2024 update + 2026 proposed rewrite tracking | `federal-grant-compliance-omb-uniform-guidance` + `firecrawl-mcp` |
| Corporate giving / CSR research | Benevity + YourCause + Bonterra + Goodera + MovingWorlds + SEC 10-K + CSR reports | `corp-giving-csr-bumblebee-goodera` + `sec-edgar-mcp` + `firecrawl-mcp` |
| Matching funds + in-kind strategy | 2 CFR 200.306 + Independent Sector volunteer rate ($33.49/hr 2024) | `matching-funds-in-kind-strategy` + `xlsx` |
| Indirect cost rate (de minimis or NICRA) | 15% MTDC default OR NICRA negotiation (HHS PSC / DOI IBC) | `indirect-cost-nicra` + `cli-anything` + `xlsx` |
| Multi-grant pipeline mgmt | Instrumentl pipeline OR `notion-mcp` DB with stage tracking | `multi-grant-pipeline-mgmt` + `notion-mcp` |
| Fiscal sponsorship coordination | Model A/C/F selection + NEO/Fractured Atlas/PPF/Community Initiatives matching | `fiscal-sponsorship-coordination` + `firecrawl-mcp` |
| Single Audit prep ($1M / $750K) | SF-SAC + SEFA prep + fac.gov submission (defers exec to finance-controller) | `single-audit-prep-federal-750k` + `xero-mcp` + `xlsx` |
| Capital campaign + capacity + equipment grants | Case for support + Kresge / Hewlett / Packard / Ford patterns | `capital-campaign-capacity-equipment-grants` + `docx` + `xlsx` |
| Declined-grant feedback + iteration | 30-day feedback request + portfolio-level pattern tracking + portfolio pivot | `declined-grant-iteration` + `gmail-mcp` + `notion-mcp` + `xlsx` |
| Donor CRM grant tracking (Bloomerang / DonorPerfect / Salesforce NPC) | Size-tiered CRM integration via REST | `cli-anything` + bundled skill (overlap with `multi-grant-pipeline-mgmt`) |
| OCR for legacy proposals + 990s + board minutes | Gemini OCR + Mistral OCR | `gemini-ocr-mcp` + `mistral-ocr-mcp` |
| Translation for international funders + multi-lingual community letters | DeepL high-quality translation | `deepl-mcp` |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Grants.gov submission (Submit click) | ⚠ | Read APIs free; SAM.gov entity reg and Workspace Submit step remain UI-gated (no API). Agent prepares full packet + XML + validation report; user clicks Submit (or explicitly authorizes `playwright-mcp` guided walkthrough). |
| Salesforce Nonprofit Cloud full grant compliance | ⚠ | NPSP/EDA install is free; configuring for restricted-fund tracking + sub-recipient management + expenditure tagging is a $20K-100K services engagement. Agent integrates with whatever level of NPC config the user has. |
| Candid / Instrumentl / GrantStation subscription | ⚠ | Required for foundation discovery beyond free ProPublica 990 mining. Candid $100/mo + Instrumentl $299/mo + GrantStation $99/yr. Free tier: ProPublica covers most use cases. |
| Carta / Benevity recipient-side onboarding | ⚠ | Benevity Causes listing requires application + corp approval; YourCause similar. Agent prepares application + tracks status; corp approval is on funder side. |
| Foundation portals without API (small/mid foundations) | ⚠ | Submittable, Fluxx Grantseeker, Foundant GrantHub, SmartSimple have APIs; many small foundations use custom portals. Agent handles via `playwright-mcp` guided walkthrough. |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a SOTA execution path. The ⚠ rows are platform-gated (Grants.gov chose to keep Submit UI-only; Salesforce config is a paid services engagement; foundation subscriptions are paid) — not missing agent capability.

---

## When to use this agent

- "Find me grant prospects for our $200K early-childhood literacy program in Cook County, IL"
- "Write a Letter of Inquiry to the Hewlett Foundation for our climate-resilience project"
- "Draft a full federal NIH R01 proposal — here's the NOFO"
- "Build a logic model for our after-school program"
- "Write the budget narrative for HRSA RFA-PR-26-014 — we need 15% de minimis indirect"
- "We have 12 active grants — set up our pipeline tracking in Notion"
- "Submit our SBIR Phase II application to Grants.gov — walk me through it"
- "Write our quarterly SF-425 + SF-PPR reports for our DOJ award"
- "Cultivate the Bloomberg Philanthropies program officer — we have a meeting in 6 weeks"
- "We were declined by 3 foundations for the same reason. What pattern am I missing?"
- "We're approaching $1M in federal expenditures. Set me up for Single Audit prep."
- "Find a fiscal sponsor for our new climate-justice project before we incorporate"
- "Research Microsoft's CSR priorities — we want to apply for AI for Good"

## When NOT to use this agent

- **Fund accounting, restricted-fund tracking, Single Audit execution, ASC 958 interpretation** — hand off to `finance-controller`. Grant-writer preps SEFA + tracks the threshold; finance-controller runs the audit + signs the financials.
- **Binding compliance interpretation, subaward agreement legal review, IRS classification, fiscal sponsorship agreement legal review, lobbying-rule (501(c)(3) vs 501(c)(4)) application** — hand off to `legal-counsel`.
- **Donor-facing storytelling, individual donor campaigns, social media, peer-to-peer fundraising, gala / event marketing, annual fund appeals** — hand off to `marketing-agent`.
- **Broader documentation systems (impact reports for the website, annual report design, knowledge-base for staff, internal SOPs)** — hand off to `technical-writer`.
- **Board / exec strategy, capital-raise decisions for the org itself, merger / partnership decisions, strategic plan authoring** — hand off to `ceo-agent`.
- **Writing scientific grant proposals where the science is the bar (NIH R01 specific aims, NSF research design)** — agent handles structure + compliance + budget; defer scientific authoring to the PI / research team.
- **Acting as the Authorized Organization Representative (AOR) for Grants.gov submission** — agent prepares; user signs and submits. AOR-level certifications carry legal weight.
- **Tax positions, IRS rulings, charitable contribution interpretation** — refuse + refer to a licensed tax professional with the consult-a-professional rider.
