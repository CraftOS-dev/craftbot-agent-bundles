# Grant Writer — deep reference

This appends to `AGENT.md`. It is **not** in the agent's default context. Grep it when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Federal grant compliance playbook", "LOI playbook", "Full proposal playbook", "Logic model playbook", "Budget narrative playbook", "Grants.gov submission playbook", "Grant reporting playbook", "Foundation cultivation playbook", "Declined grant analysis playbook", "Indirect cost reference", "SF-424 family reference", "Single Audit reference", "Fiscal sponsorship reference", "Corporate giving reference", "SOTA tool reference".

For provenance of any section, see `SOURCES.md` in this bundle.

---

## Capability reference

Factual reference — funder ecosystems, federal frameworks, form families, indirect cost rules, and submission portals. SOUL.md does not carry these; grep here when the user asks "what should I use for X?"

### Funder ecosystem map (2026)

| Type | Sub-type | Examples |
|---|---|---|
| Federal | Discretionary grant | NIH (HHS), NSF, ED, DOJ, HUD, USDA, EPA, HRSA, SAMHSA |
| Federal | Formula grant | Title I (ED), CDBG (HUD), TANF (HHS), Ryan White (HRSA) |
| Federal | Cooperative agreement | CDC, HRSA, NSF, USAID |
| State | Discretionary | State DOH, DCFS, DPI, NEA state arts councils |
| State | Pass-through federal | Title V, CCDBG, ESSA pass-throughs |
| Foundation | Private foundation | Gates, Ford, MacArthur, Hewlett, Packard, Kresge, Robert Wood Johnson |
| Foundation | Community foundation | Silicon Valley CF, Greater NY CF, Cleveland Foundation, Chicago Community Trust |
| Foundation | Family foundation | Walton, Bloomberg, Bezos Earth Fund |
| Foundation | Operating foundation | J. Paul Getty Trust, Russell Sage Foundation |
| Corporate | Direct giving | Microsoft Philanthropies, Google.org, Salesforce.org, Amazon Future Engineer |
| Corporate | CSR platform-mediated | Benevity Causes, YourCause CSRconnect, Bonterra |
| Corporate | Employee giving / match | Workplace giving programs (United Way historically; Benevity / YourCause now) |
| DAF | Donor-Advised Fund | Fidelity Charitable, Schwab Charitable, Vanguard Charitable, Silicon Valley CF DAF |
| Government quasi | Cooperative non-federal | National Endowment for Democracy, Knight Foundation |

### Federal cost principles (2026)

| Topic | 2 CFR 200 cite | NIH 45 CFR 75 cite | 2024 / 2026 Update |
|---|---|---|---|
| De Minimis Indirect | 200.414(f) | 75.414(f) | Raised 10% → 15% MTDC (Oct 2024) |
| Subaward base for MTDC | 200.331(a)(8) | 75.331(a)(8) | Raised to $50K (Oct 2024) |
| Equipment threshold | 200.439 | 75.439 | Raised to $10K (Oct 2024) |
| Single Audit threshold | 200.501 | 75.501 | Raised $750K → $1M (Oct 2024 awards) |
| Cost principles (Subpart E) | 200.400-200.476 | 75.400-75.476 | Stable; OMB May 29 2026 rewrite under comment |
| Indirect rate negotiation | 200.414 | 75.414 | Not revised in 2026 proposed rule |

### SF-424 family forms

| Form | Purpose | When required |
|---|---|---|
| SF-424 | Application for Federal Assistance (general) | Most discretionary grants |
| SF-424A | Budget Information — Non-Construction | Most non-construction grants |
| SF-424B | Assurances — Non-Construction | Most non-construction grants |
| SF-424C | Budget Information — Construction | Construction grants only |
| SF-424D | Assurances — Construction | Construction grants only |
| SF-424 Short Org | Short Organizational | Simplified submissions |
| SF-424 Individual | For individuals | Personal grants (fellowships, traveler grants) |
| SF-424 Mandatory | For mandatory programs | Block grants, formula grants |
| SF-LLL | Disclosure of Lobbying | Only if lobbying activity present |
| SF-424A worksheets | Object class budget | Personnel, fringe, travel, equipment, supplies, contractual, other, total direct, indirect, total |
| SF-425 | Federal Financial Report | Post-award financial reporting |
| SF-PPR | Performance Progress Report | Post-award programmatic reporting |
| SF-SAC | Data Collection Form for Single Audit | Single Audit only ($1M+ federal expenditures) |

### Foundation databases (2026)

| Tool | Records | Pricing | Unique strength |
|---|---|---|---|
| Candid Search | 304K funder profiles | $100/mo (down from $299 post-merger) | Geographic mapping to legislative district |
| Instrumentl | 410K funder profiles + DAFs | $299/mo | Includes DAFs (rare); built-in pipeline tracker |
| GrantStation | ~6K active funders | $99/yr | Clubs / associations / giving circles filter (unique) |
| ProPublica Nonprofit Explorer | 3M 990 filings | Free + API | Full-text 990 search; download PDFs |
| Foundation Directory Online (legacy) | Merged into Candid 2026 | (deprecated) | — |
| GrantWatch | 16K+ funders | $18-$199/mo | Daily refresh + email alerts |
| OpenGrants | ~5K funders | Freemium | Marketplace + Pro grant writers |
| Grantable | 130K from 990 + targeted research | $24/mo | AI proposal-drafting integrated |

### Submission portals (2026)

| Portal | Sector | Submit API? |
|---|---|---|
| Grants.gov Workspace | Federal | Read APIs only; submit via UI |
| SAM.gov | Federal entity reg | Read APIs only; entity-reg via UI |
| Submittable | Foundations, awards | REST API for applicants + funders |
| Fluxx Grantseeker | Foundations | API for select tenants |
| Foundant GrantHub | Foundations | API for select tenants |
| Bonterra | Corp + foundation | REST API |
| Blackbaud Grantmaking | Foundations | SKY API |
| SmartSimple | Foundations | API |
| SurveyMonkey Apply (FluidReview) | Foundations + awards | REST API |
| GrantHub by Foundant | Grantseeker-side tracking | Limited API |

### Donor / grant CRM tier (match to org size)

| Org revenue | Recommended CRM | Grant tracking notes |
|---|---|---|
| < $1M | Bloomerang (no native grants) + Notion pipeline; OR Givebutter | Pair with separate Notion/Airtable grant tracker |
| $1-10M | DonorPerfect (light grants); Bloomerang Standard | DonorPerfect handles awards + deadlines + notes |
| > $10M | Salesforce Nonprofit Cloud (NPSP/EDA) | Full grant compliance with $20K-100K configuration |
| Enterprise | Bonterra Guided Fundraising; Blackbaud Raiser's Edge NXT | Bundled grants + giving |
| Specialty | Little Green Light; Kindful (acquired by Bloomerang) | Light-touch alternatives |

### Fiscal sponsorship models

| Model | Description | Sponsor examples |
|---|---|---|
| Model A | Comprehensive — sponsored project IS sponsor's project; sponsor liability | Tides Foundation (legacy) |
| Model C | Pre-approved grant relationship — most common; sponsor passes funds | NEO Philanthropy, Players Philanthropy Fund, Community Initiatives, Third Sector New England |
| Model F | Single-member LLC — sponsored project is sponsor's LLC | Less common |
| Open Collective Foundation | (dissolved Dec 31, 2024) | — |
| Fractured Atlas | Artists & creators | Model C for artists |
| NCRP / Community Initiatives | Multi-purpose | Model C national |

### CSR / corporate giving platforms (2026)

| Platform | Position | Used by |
|---|---|---|
| Benevity Goodness Platform | Market leader; AI-native | >50% Fortune 100 |
| YourCause CSRconnect (Blackbaud) | Enterprise CSR | Fortune 1000 |
| Bonterra | All-in-one CSR + grants | Mid-market |
| Goodera | Corp volunteering specialist | 50K+ nonprofit network |
| MovingWorlds | Skills-based volunteering specialist | Pair with Benevity |
| Givinga | Workplace giving | Emerging |
| Uncommon Giving | DAF-style workplace giving | Emerging |

---

## Federal grant compliance playbook

When a user mentions a federal NOFO or post-award compliance question, follow this procedure.

1. **Step 1: Identify the cost-principle framework.** Most federal awards use 2 CFR 200; NIH uses 45 CFR 75 per NOT-OD-26-072 (FY2026); NASA uses 14 CFR 1260. Pull the framework citation from the NOFO.
2. **Step 2: Check the 2024 + proposed 2026 updates.** De Minimis raised 10% → 15% MTDC; subaward base raised to $50K; equipment threshold raised to $10K; Single Audit threshold raised $750K → $1M. The OMB May 29 2026 proposed rule (comment by July 13 2026; effective Oct 1, 2026) adds political pre-issuance review for discretionary grants — flag if relevant.
3. **Step 3: Verify SAM.gov entity registration is active.** UEI + CAGE Code required; annual renewal mandatory; lapsed = ineligible. Renewal takes 7-10 business days.
4. **Step 4: Match indirect cost approach.** If first-time grantee or no NICRA — de minimis 15% MTDC (no federal approval required; can use indefinitely). If existing NICRA — apply rate per NICRA letter. NIH may set a separate published rate per 45 CFR 75.
5. **Step 5: Compute MTDC base correctly.** Modified Total Direct Costs = total direct costs MINUS: capital expenditures (>$10K), subcontract amounts over $25K (only first $25K is in base), participant support costs, pass-through funds to sub-recipients beyond the first $25K, rental costs, certain federal scholarships.
6. **Step 6: Subaward monitoring per 2 CFR 200.331.** For every sub-recipient: risk assessment (financial stability, prior audit findings, programmatic capacity) + monitoring plan (reports, site visits, financial reviews) + documented agreement (FFATA reporting if >$30K).
7. **Step 7: Track Single Audit threshold.** Cumulative federal expenditures across all awards in the FY. Threshold $1M (post-Oct 2024 awards) OR $750K (pre-Oct 2024 awards). Dual-compliance environment persists through orgs with multi-year grants straddling the date.

### Federal grant lifecycle stages

| Stage | Activities | Key forms |
|---|---|---|
| Pre-award | Prospect research, eligibility check, SAM.gov reg, LOI, proposal | SF-424 family |
| Award | Notice of Award, accept/decline, set up project codes in GL | NoA |
| Post-award | Spend down per approved budget, report quarterly/annually, document outcomes | SF-425, SF-PPR |
| Closeout | Final report, return unspent funds, archive records | Final SF-425, final SF-PPR |
| Audit | Single Audit if ≥$1M federal expenditures in FY | SF-SAC + SEFA |

### Reference: 2 CFR 200 subparts

- **Subpart A — Acronyms and Definitions**
- **Subpart B — General Provisions**
- **Subpart C — Pre-Federal Award Requirements** — including non-federal entity responsibilities + 200.205 risk assessment
- **Subpart D — Post-Federal Award Requirements** — including 200.300 statutory requirements, 200.305 payment, 200.306 cost sharing, 200.331 subrecipient management
- **Subpart E — Cost Principles** — 200.400-200.476 — general principles + selected items of cost (allowability of fringe, travel, equipment, IT)
- **Subpart F — Audit Requirements** — 200.500-200.521 — Single Audit, SF-SAC, fac.gov submission

---

## LOI playbook

Standard 2-3 page Letter of Inquiry. Page-limit aware.

1. **Opening hook (1 short paragraph).** Address PO by name. Reference what attracted you to this funder (a recent grant, an article they wrote, a priority they published). Identify your org + your ask in 2 sentences.
2. **Statement of need (1 paragraph).** Quantified problem with primary-source data. Geographic scope. Why this is urgent NOW.
3. **Project description (1-2 paragraphs).** Goal → 2-3 measurable objectives → primary activities → expected outcomes (3-12 months) → tied to logic model.
4. **Org credibility (1 paragraph).** Years in operation, prior similar work, key partners, evaluation track record. Specific past outcomes (numbers).
5. **Funding request + budget summary (1 short paragraph).** Amount requested + project total + match/leverage + project period.
6. **Close + call to action.** "We welcome the opportunity to submit a full proposal" OR "Please let us know if a 15-minute call would help."

### LOI structural rules
- ≤ 3 pages — most funders are strict; some cap at 2.
- Single-spaced, 11-12 pt, 1" margins.
- No appendices unless the funder explicitly invites.
- Mirror the funder's language verbatim where possible (their priority phrases, their geography phrasing, their outcome categories).
- Address the PO by name if known; "Dear Program Officer" only if you can't find the name.

### LOI example structure

```markdown
# Letter of Inquiry: <Project Name>
**To:** <PO Name>, Program Officer, <Funder>
**From:** <Org name>, <date>
**Re:** <Funder's program area> — <One-line project>

Dear <PO First Name>,

[Opening hook — reference their recent grant to <peer org> or their published priority of <topic>. Name your org + your ask in 2 sentences.]

**The need.** [Quantified problem with primary-source citation. "In <geography>, X% of <population> experience <problem> (Source). This is up Y% since <year>." Why now.]

**Our project.** [Goal → 2-3 objectives → activities → outcomes. Tied to logic model. Time-bounded.]

**Our org.** [Years operating; prior similar work with numbers; key partners; evaluation capability.]

**The ask.** We request $<amount> over <period> against a total project budget of $<total> ($<match> in match/leverage from <sources>).

We welcome the opportunity to submit a full proposal. Please let me know if a brief call would help clarify our fit with <Funder>'s <priority> priority.

Sincerely,
<Name>, <Title>
<Email> | <Phone>
```

---

## Full proposal playbook

When a user wants a full federal or foundation proposal.

1. **Step 1: Read the NOFO end-to-end.** Extract: eligibility, scoring rubric, page limits per section, required attachments, deadline, submission method, contact (PO).
2. **Step 2: Map NOFO outline to your sections.** Mirror it exactly. Reviewers score against the rubric; deviation costs points.
3. **Step 3: Build the logic model FIRST.** Inputs → Activities → Outputs → Outcomes → Impact. Add Theory of Change causal narrative + assumptions if foundation.
4. **Step 4: Draft sections in this order:**
   - Statement of Need (the easiest to start; pull data citations)
   - Project Description (goals → objectives → activities → timeline)
   - Methods (how the activities will be executed; evidence base)
   - Evaluation Plan (linked to logic model; methods + indicators + data collection + analysis)
   - Org Capability (years operating, prior grants, key staff, evaluation track record)
   - Sustainability (post-grant funding plan)
   - Executive Summary (drafted LAST — it's a summary, not an intro)
5. **Step 5: Budget last.** Reconcile SF-424A to narrative to project-narrative cost mentions to the dollar.
6. **Step 6: Appendices.** IRS determination letter, board roster, audited financials, key staff bios, letters of support, evaluation tool samples.
7. **Step 7: Internal review before submit.** Differential review with finance + program lead + ED. Use `requesting-code-review` if reviewers grep that pattern.

### Standard proposal section template

```markdown
## Statement of Need
- Quantified problem with primary-source citation
- Geographic scope
- Population most affected
- Existing gaps in services / why current approaches fall short
- Why now

## Project Description
- Goal (1 sentence)
- Objectives (2-4, measurable, time-bounded, SMART)
- Activities (per objective)
- Timeline (Gantt or quarterly table)
- Target population + outreach plan
- Partnerships

## Methods
- Evidence base for the approach (cite studies)
- Why this approach not alternatives
- Implementation steps + milestones
- Roles (FTE allocation per activity)

## Evaluation Plan
- Logic model (or attach as Appendix)
- Indicators per outcome (linked to logic model boxes)
- Data sources + collection schedule + analysis methods
- Evaluation partner (if applicable)
- Sample size + power calculation if research-oriented
- Reporting cadence to funder

## Organizational Capability
- Years operating, mission, 501(c)(3) status
- Prior grant history with similar funders + dollar amounts
- Key staff with bios + relevant experience
- Evaluation track record
- Financial health (audit status, reserves)

## Budget Narrative
- Per object class category (Personnel, Fringe, Travel, Equipment, Supplies, Contractual, Other, Indirect)
- Per line: amount + calculation + allowability + allocability + reasonableness
- Reconcile to SF-424A to the dollar

## Sustainability
- Post-grant funding plan (other funders, earned revenue, individual donors)
- Capacity built that persists
- Partnerships that continue
```

---

## Logic model playbook

Inputs → Activities → Outputs → Outcomes → Impact, in 5 columns.

1. **Step 1: Inputs.** Resources committed: staff FTE, $$, partners, facilities, materials, evaluation tools.
2. **Step 2: Activities.** What we DO: training delivered, services provided, advocacy meetings, research conducted, materials disseminated.
3. **Step 3: Outputs.** Immediate countable products: # people trained, # services delivered, # materials distributed, # convenings held.
4. **Step 4: Short-term Outcomes (3-12 months).** Changes in knowledge / skills / attitudes / awareness. Measurable with pre/post.
5. **Step 5: Medium-term Outcomes (1-3 years).** Changes in behavior / practice / decision / policy.
6. **Step 6: Long-term Outcomes / Impact (3-5+ years).** Changes in condition / status / quality of life / systems.

### Theory of Change add-on (foundation requests)

Add causal arrows + assumptions between boxes + evidence base for each assumption.

```
Activity X → Output Y → Outcome Z
Assumption: [why X causes Y; why Y causes Z]
Evidence: [study / past program data / peer-reviewed support]
```

### Indicator framework per outcome

For every outcome row in the logic model:
- **Indicator:** what gets measured (e.g., "% of participants demonstrating skill X")
- **Data source:** survey, observation, administrative record
- **Collection schedule:** pre/post, monthly, annually
- **Analysis method:** descriptive stats, comparison, regression, qualitative coding
- **Target:** what success looks like (e.g., "70% by end of year 1")

---

## Budget narrative playbook

Federal budgets require every line to be allowable + allocable + reasonable.

### Standard SF-424A object class structure

| Category | Examples | Allowable? | Allocability |
|---|---|---|---|
| a. Personnel | Salaries (PI, project staff) | Yes | % FTE to this project |
| b. Fringe Benefits | Health, retirement, payroll tax | Yes | Same % as personnel |
| c. Travel | Per diem, mileage, lodging | Yes if necessary + reasonable | Justified per trip |
| d. Equipment | Items ≥$10K per 2024 update | Yes if necessary | Direct or shared |
| e. Supplies | Items <$10K | Yes | Direct to project |
| f. Contractual | Subawards (first $25K in MTDC base), consultants | Yes per 200.331 monitoring | Per subaward |
| g. Construction | Land, buildings | Only for construction grants | — |
| h. Other | Communications, rent, printing | Yes | Allocable |
| i. Total Direct | Sum of a-h | — | — |
| j. Indirect | De minimis 15% MTDC OR NICRA rate × MTDC | — | — |
| k. Total | Direct + Indirect | — | — |

### Indirect cost decision tree

```
Have NICRA?
├── Yes → Apply NICRA rate × MTDC base
│         (Cite NICRA letter date + cognizant agency)
│         (If NIH award, check 45 CFR 75 specific rate)
└── No  → De Minimis 15% MTDC
          (Per 2 CFR 200.414(f) updated Oct 2024)
          (No federal approval; can use indefinitely)
          (Cannot use if NICRA exists for the org)
```

### MTDC base computation

MTDC = Total Direct Costs MINUS:
- Capital expenditures (equipment >$10K)
- Subaward portions beyond first $25K
- Participant support costs
- Pass-through to sub-recipients beyond first $25K
- Rental costs
- Certain federal scholarships

### Budget narrative template

```markdown
**a. Personnel — $XX,XXX**
- <Role> @ <% FTE> for <period>: $<amount> ($<base salary> × <FTE>%)
- <Role> @ <% FTE> for <period>: $<amount>
Allowability: 2 CFR 200.430 (Compensation — personal services).
Allocability: <% FTE> to this project per <basis: time study / activity report>.
Reasonableness: salary benchmarked against [BLS occupational data / sector survey].

**b. Fringe Benefits — $XX,XXX**
<rate>% × Personnel = $<amount>.
Basis: org's actual fringe rate from FY<year> audited financials.

[Continue for c-h]

**i. Total Direct Costs — $XXX,XXX**

**j. Indirect Costs — $XX,XXX**
De Minimis 15% MTDC per 2 CFR 200.414(f).
MTDC base: Total Direct $<X> MINUS Equipment $<Y> MINUS Subaward >$25K $<Z> = $<MTDC>.
Indirect: 15% × $<MTDC> = $<Indirect>.

**k. Total Project — $XXX,XXX**
```

---

## Grants.gov submission playbook

1. **Step 1: SAM.gov entity registration must be ACTIVE.** Verify at `sam.gov/entity-registration`. Renewal annual; lapses = ineligible. 7-10 business days for renewal.
2. **Step 2: Confirm UEI + CAGE Code.** UEI (12-char alpha-numeric) replaced DUNS; SAM auto-generates. CAGE Code from DLA.
3. **Step 3: Create Workspace.** In Grants.gov, find opportunity → Apply → Create New Workspace.
4. **Step 4: Add forms to Workspace.** SF-424 family + program-specific forms (e.g., Project Narrative Attachment Form, Performance Site Location Form for NIH).
5. **Step 5: Complete forms.** Online forms preferred (auto-validation); fillable PDFs as fallback.
6. **Step 6: Validate.** Workspace → Check Application → resolve all errors.
7. **Step 7: User submits.** Authorized Organization Representative (AOR) clicks Submit. Agent does NOT submit on user's behalf without explicit authorization.
8. **Step 8: Receipt confirmation.** Tracking number returned; record in `notion-mcp` pipeline; calendar report deadlines.

### Common Grants.gov submission errors

| Error | Cause | Fix |
|---|---|---|
| "Entity not registered or expired" | SAM.gov lapsed | Renew at sam.gov |
| "Invalid UEI" | Mismatch SAM ↔ application | Confirm UEI matches SAM entity |
| "Form schema validation error" | Field type mismatch | Re-validate in Workspace |
| "File too large" | Attachment >100MB | Compress or split |
| "Special character not allowed" | Em-dash, smart quotes in PDF | Re-save as plain text or generic PDF |

---

## Grant reporting playbook

Reporting begins at award acceptance, not 11 months later.

1. **Step 1: At award acceptance, calendar all report deadlines.** SF-425 cadence (typically quarterly), SF-PPR cadence (typically annual), final report due 90 days after period of performance ends.
2. **Step 2: Set up outcome-data collection on day 1.** Talk to program team about what gets measured + how + by whom + how often.
3. **Step 3: Pull GL via `xero-mcp` monthly to keep spend reconciled to budget.** Flag variances >10% early — don't surprise the funder at report time.
4. **Step 4: At report time, pull SF-425 from `xero-mcp` GL.** Object class categories matching SF-424A. Federal Share, Recipient Share, Program Income separately.
5. **Step 5: Draft SF-PPR narrative anchored to logic-model outcomes promised.** For each outcome:
   - Target promised at award
   - Actual achieved this reporting period
   - Cumulative achieved to date
   - Variance + explanation
   - Evidence (attach evaluation tool data)
6. **Step 6: Reconcile SF-425 to SF-PPR.** Numbers should not contradict; financial spend should map to programmatic activities reported.
7. **Step 7: Submit per funder portal (Grants.gov for federal, funder-portal for foundation).**

### SF-425 + SF-PPR alignment template

```markdown
## Federal Financial Report (SF-425)
- Federal Cash Receipts: $<X>
- Federal Cash Disbursements: $<Y>
- Federal Share of Expenditures: $<Z>
- Unobligated Balance: $<X-Y>
- Recipient Share: $<match>
- Program Income (if any): $<income>

## Performance Progress Report (SF-PPR)
- Goal 1 — <goal text>
  - Objective 1.1 (target: <T>): Actual <A>, Cumulative <C>, Variance <V%>
    - Activities: <list>
    - Outcomes evidence: <data summary>
  - Objective 1.2 (target: <T>): Actual <A>, Cumulative <C>, Variance <V%>
- Goal 2 — <goal text>
  - <continue>

## Challenges + Changes
- <Any deviations from original plan + rationale + plan to address>

## Next Period Plan
- <Activities + milestones for the next reporting period>
```

---

## Foundation cultivation playbook

Foundations don't fund based on one proposal — they fund based on a cultivated relationship.

### 12-month cultivation cadence

| Month | Touch | Tool |
|---|---|---|
| 1 | Research PO + funder priorities | `firecrawl-mcp` + ProPublica + Candid |
| 1 | LinkedIn / personal-network introduction request | `gmail-mcp` |
| 2 | PO call request (15 min) — confirm fit before LOI | `gmail-mcp` + `google-calendar-mcp` |
| 3 | LOI sent (if invited or unsolicited per portal allowance) | `docx` + `gmail-mcp` |
| 4-5 | Full proposal (if LOI accepted) | proposal mode |
| 6 | Decision + thank-you + offer site visit | `gmail-mcp` |
| 7-12 | Annual report / impact update (whether awarded or not) | `docx` |
| 12 | Renewal LOI / next-cycle outreach | LOI mode |

### Foundation profile card (in `notion-mcp`)

```markdown
# <Foundation Name>
- **Tax ID:** <EIN>
- **Annual giving:** $<amount> (from latest 990 PF)
- **Geographic focus:** <areas>
- **Program areas:** <areas>
- **Avg grant size:** $<amount> (from last 10 grants)
- **Range:** $<min> - $<max>
- **Cycle:** LOI <month>, Full proposal <month>, Decision <month>
- **PO name:** <Name>
  - Background: <years at foundation; prior role>
  - LinkedIn: <link>
  - Publications: <if any>
- **Recent grantees (signal):** <peer orgs awarded last 12 months>
- **Our touches log:**
  - <date>: <touch type> — <notes>
```

---

## Declined-grant analysis playbook

Track declines at portfolio level, not proposal level.

1. **Step 1: Within 30 days of decline, request feedback.** Specific, professional, brief.
   ```
   Dear [PO Name],
   Thank you for the recent decision on our <project> proposal. We value <Foundation>'s
   commitment to <priority area> and want to learn from our submission. If your review
   process allows, would you be willing to share any feedback on what could strengthen
   a future submission?
   Best, [Name]
   ```
2. **Step 2: If feedback is not offered, run an internal debrief.** Grant writer + program lead + finance read the NOFO + the proposal + publicly known peer projects funded by this funder. Agree on the most plausible primary decline reason category.
3. **Step 3: Log in `notion-mcp` declined-grant table.** Funder, project, amount requested, decline reason (offered or hypothesized), pattern category.
4. **Step 4: Decline reason categories.**
   - Funder priority mismatch (we pitched outside their stated priorities)
   - Geographic misalignment
   - Amount mismatch (too high vs avg grant; too low to bother)
   - Weak evaluation plan
   - Weak org credibility / track record gap
   - Vague need statement
   - Budget misalignment (too much indirect; missing match)
   - Crowded field (highly competitive cycle)
   - Late submission / non-compliant
   - Unknown
5. **Step 5: Pattern-level analysis after 5+ declines.** Aggregate by category. The top category becomes a portfolio-level pivot.
6. **Step 6: Portfolio-level pivots (not proposal-level).**
   - "Weak evaluation" across 5 declines → formalize partnership with university / evaluation firm; invest in org-wide outcomes framework.
   - "Vague need statement" → adopt a tighter need-statement methodology org-wide (specific population + quantified gap + primary-source citation).
   - "Priority mismatch" → tighten prospect-research alignment scoring.
   - "Budget misalignment" → standardize indirect strategy + match approach.

### Decline pattern memo template

```markdown
# Declined-Grant Pattern Memo — <Date>

**Period:** <date range>
**Total declines analyzed:** <N>
**Total awarded in same period:** <M>
**Decline rate:** <N/(N+M)>%

## Pattern analysis
| Category | Count | % of declines |
|---|---|---|
| <Category 1> | X | Y% |
| <Category 2> | X | Y% |

## Top pattern: <Category>
- Examples: <funder + proposal>; <funder + proposal>; <funder + proposal>
- Root cause hypothesis: <hypothesis>
- Evidence: <feedback received + internal debriefs + peer-org analysis>

## Recommended portfolio-level pivot
- Action 1: <specific>
- Action 2: <specific>
- Investment required: $<amount> or <FTE>
- Expected impact: <reduce category X declines from Y% to Z% within N months>
```

---

## Indirect cost reference

### De Minimis (15% MTDC per 2 CFR 200.414(f), updated Oct 2024)

- Available to any non-federal entity that has never had a federally negotiated rate.
- 15% of Modified Total Direct Costs (MTDC).
- Can be used indefinitely.
- No federal approval required.
- MTDC excludes: capital (>$10K), subaward portions over $25K, participant support costs, pass-through, rental, certain scholarships.

### NICRA (Negotiated Indirect Cost Rate Agreement)

Cognizant agency by entity type:
- Most universities: ED Office of Indirect Cost Negotiation
- Most nonprofits (≥$10M federal funding): HHS Program Support Center (PSC)
- Native American tribes: DOI Interior Business Center (IBC) Indirect Cost Services
- States / local govts: DHHS Cost Allocation Services

NICRA proposal contains:
- Indirect cost pool: G&A + facilities + admin
- Direct cost base: typically MTDC
- Resulting rate
- Audit / single-audit basis

Rate types:
- **Provisional** — agreed temporary rate during negotiation
- **Predetermined** — fixed for 2-4 years prospectively
- **Fixed with carry-forward** — set initially, adjusted by carry-forward of over/under-recovery
- **Final** — set after fiscal year close

### NIH 45 CFR 75 reversion (FY2026 per NOT-OD-26-072)

NIH awards in FY2026 revert to 45 CFR Part 75 indirect cost provisions (vs 2 CFR 200). Practical impact: NIH may publish a separate ceiling rate; the de minimis still available at NIH's discretion.

---

## SF-424 family reference

### Form decision tree

```
Federal grant application?
├── Construction grant? → SF-424C + SF-424D
├── Mandatory program (block grant)? → SF-424 Mandatory family
├── Short form allowed (NOFO says so)? → SF-424 Short Org
├── Individual application? → SF-424 Individual family
└── Standard discretionary? → SF-424 + SF-424A + SF-424B + program-specific
```

### Object class categories (SF-424A)

a. Personnel | b. Fringe Benefits | c. Travel | d. Equipment | e. Supplies | f. Contractual | g. Construction | h. Other | i. Total Direct | j. Indirect | k. Total

### Required attachments (typical)

- IRS determination letter (501(c)(3))
- Audited financial statements (last 3 years)
- Board of Directors roster
- Project Narrative
- Budget Narrative
- Logic Model / Evaluation Plan
- Letters of Support / Commitment
- Key Staff CVs / Bios
- Existing certifications (e.g., SAMHSA, HRSA Accreditation)

---

## Single Audit reference

### Threshold

- $1M+ federal expenditures in FY for awards issued ON OR AFTER Oct 1, 2024
- $750K+ for awards issued BEFORE Oct 1, 2024
- Dual compliance: orgs with multi-year grants straddling the date apply BOTH thresholds depending on the source award

### Required deliverables

- Schedule of Expenditures of Federal Awards (SEFA) prepared by org
- SF-SAC Data Collection Form submitted to fac.gov
- Independent CPA firm audit (NOT internal)
- Reporting deadline: 9 months after fiscal year-end

### Grant-writer's role vs `finance-controller`

- **Grant-writer:** Track threshold throughout the year; prep SEFA from grant-system data; brief auditor on each award (NOFO + award terms + cost principles).
- **`finance-controller`:** Execute the audit, lead PBC list response, sign audited financial statements.

---

## Fiscal sponsorship reference

### Model A vs Model C vs Model F

- **Model A — Comprehensive.** Sponsored project IS the sponsor's program. Sponsor has full legal + financial liability. Best for: long-term projects considering eventual independent 501(c)(3) status.
- **Model C — Pre-Approved Grant Relationship.** Most common. Sponsor passes funds to sponsored project per agreement; sponsored project has separate governance. Best for: short-to-medium term, project teams who want quick start without forming 501(c)(3).
- **Model F — Single-Member LLC.** Sponsored project is sponsor's LLC. Less common.

### Top fiscal sponsors (2026)

| Sponsor | Specialty | Admin fee | Notes |
|---|---|---|---|
| NEO Philanthropy | Social justice + advocacy | 6-8% | Comprehensive |
| Fractured Atlas | Artists + creators | 7% | Largest for artists |
| Players Philanthropy Fund | Athletes + sports | 5% | Sports-focused |
| Community Initiatives | Multi-purpose | 7-9% | Bay Area-strong |
| Third Sector New England | New England multi-purpose | 7% | TSNE |
| NCRP | Multi-purpose | varies | National Center for Responsive Philanthropy |
| The Common Counsel | Progressive multi-purpose | 6-9% | Coastal |
| Open Collective Foundation | DISSOLVED Dec 31, 2024 | — | No longer an option |

### Fiscal sponsorship agreement key terms

- Term length + termination
- Admin fee structure (% of grants, % of expenses, flat fee)
- Decision-making authority (sponsor vs project)
- Use of sponsor's tax-exempt status (Model A vs C distinction)
- Indemnification + insurance
- Intellectual property + name rights
- Exit clause (project becomes own 501(c)(3))

Hand-off: binding fiscal sponsorship agreement review → `legal-counsel`.

---

## Corporate giving reference

### CSR research workflow

1. Pull target corp's most recent 10-K via `sec-edgar-mcp` — look for ESG / sustainability / community sections.
2. Pull CSR / Impact / Sustainability report from corp website via `firecrawl-mcp`.
3. Identify their stated priorities + recent grant recipients.
4. Check Benevity / YourCause Causes listing for which platform mediates their giving.
5. Find the right contact: Foundation president (for a Corporate Foundation), Head of Philanthropy / CSR (for direct giving), Community Affairs Director (for local giving programs).

### Match to platform

- **Benevity Goodness Platform** — most likely if a Fortune 1000 corp; apply to be on Causes list.
- **YourCause CSRconnect (Blackbaud)** — large enterprise; apply via Blackbaud nonprofit portal.
- **Bonterra** — mid-market; apply via Bonterra Causes.
- **Direct** — smaller orgs / family-owned biz; pitch through executive contact.

### Corporate giving proposal differences (vs foundation)

- Focus on alignment with corp's brand + ESG narrative.
- Quantify employee engagement / volunteer hours.
- Offer co-branding + recognition opportunities.
- Pitch in fiscal-year cycles (often calendar year for corps).
- Multi-year commitments rarer; ask for renewal annually.

---

## SOTA tool reference (June 2026)

Grep-friendly per-tool reference. Each entry points at the bundled skill pack with the full recipe. Use this when deciding "what tool should I use for X?" Use the linked skill when actually executing.

### Grants.gov (Get Opportunities Public API)

Federal grant search + opportunity-detail JSON. Free, no auth.

- Endpoint: `https://api.grants.gov/v1/api/search2`
- Use: `curl -X POST -d '{"keyword":"early childhood education"}' ...`
- Best for: federal NOFO discovery + opportunity full text + close dates.
- Skill pack: `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md`.
- Source: https://open.gsa.gov/api/get-opportunities-public-api/

### SAM.gov Opportunity Management API

Federal opportunity + entity registration verification.

- Endpoint: `https://api.sam.gov/opportunities/v2/search?api_key=...`
- Auth: SAM.gov API key (free).
- Best for: federal opportunity discovery + UEI / CAGE verification + entity-status check.
- Skill pack: `skills/grants-gov-sam-gov-submission/SKILL.md`.
- Source: https://open.gsa.gov/api/opportunities-api/

### ProPublica Nonprofit Explorer API v2

3M+ Form 990 filings. Free, no auth.

- Endpoint: `https://projects.propublica.org/nonprofits/api/v2/search.json?q=...`
- Use: `curl 'https://projects.propublica.org/nonprofits/api/v2/organizations/<EIN>.json'`
- Best for: funder due diligence + grant-giver discovery + 501(c)(3) verification + free 990 PDF download.
- Skill pack: `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md`.
- Source: https://projects.propublica.org/nonprofits/api

### Candid (Search + GuideStar merger Jan 2026)

304K funder profiles + geographic mapping + AI matching.

- Pricing: $100/mo (down from $299 post-merger).
- Best for: foundation discovery + geographic targeting (city / county / legislative district) + AI strategic recommendations.
- Skill pack: `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md`.
- Source: https://candid.org/

### Instrumentl

410K funder profiles + DAFs + AI proposal-drafting + pipeline tracker.

- Pricing: $299/mo.
- Best for: nonprofits with ≥10 active grants + want unified discovery+pipeline+AI assist. Includes DAF data (rare).
- Skill pack: `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md`.
- Source: https://www.instrumentl.com/

### GrantStation

~6K active funders + clubs / associations / giving circles filter.

- Pricing: $99/yr (annual subscription).
- Best for: orgs targeting service clubs, civic associations, giving circles (unique to GrantStation).
- Skill pack: `skills/grant-prospect-research-grants-gov-instrumentl-candid/SKILL.md`.
- Source: https://www.grantstation.com/

### Grantable

AI-native grant writing + 130K funder DB from 990s.

- Pricing: $24/mo.
- Best for: persistent funder memory + AI proposal drafting + full lifecycle management at low cost.
- Skill pack: `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md`.
- Source: https://grantable.co/

### GrantBoost

AI grant proposal answer generator from opportunity paste-in.

- Pricing: $19.99/mo Pro; free tier.
- Best for: one-off proposal AI assist without discovery / pipeline overhead.
- Skill pack: `skills/full-grant-proposal-narrative-methods-evaluation/SKILL.md`.
- Source: https://www.grantboost.io/

### FundRobin

AI smart-matching for declined-grant root cause analysis.

- Pricing: $29/mo.
- Best for: declined-grant pattern matching + smart matching to improve next-cycle alignment.
- Skill pack: `skills/declined-grant-iteration/SKILL.md`.
- Source: https://www.fundrobin.com/

### Sopact Theory of Change wizard

Auto-drafts logic-model + Theory of Change from plain-language program description.

- Best for: rapid logic-model drafting + assumption surfacing.
- Skill pack: `skills/logic-model-inputs-activities-outputs-outcomes/SKILL.md`.
- Source: https://www.sopact.com/use-case/logic-model

### W.K. Kellogg Foundation Logic Model Development Guide

Canonical 5-column logic model methodology (still the 2026 industry standard).

- Best for: anchor methodology citation in evaluation sections.
- Skill pack: `skills/logic-model-inputs-activities-outputs-outcomes/SKILL.md`.
- Source: https://wkkf.issuelab.org/resource/logic-model-development-guide.html

### eCFR (Electronic Code of Federal Regulations)

Live 2 CFR 200 + 45 CFR 75 + agency-specific cost principles.

- Endpoint: `https://www.ecfr.gov/api/...` for versioned regulation queries.
- Best for: ground-truth federal compliance citations + regulatory change detection.
- Skill pack: `skills/federal-grant-compliance-omb-uniform-guidance/SKILL.md`.
- Source: https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200

### IRS Tax Exempt Organization Search (EO)

Live 501(c)(3) status verification.

- Endpoint: `https://apps.irs.gov/app/eos/`
- Best for: verify funder's 501(c)(3) status + private-foundation classification.
- Skill pack: `skills/irs-501c3-compliance-docs/SKILL.md`.
- Source: https://apps.irs.gov/app/eos/

### Federal Audit Clearinghouse (fac.gov)

SF-SAC Data Collection Form submission for Single Audit.

- Endpoint: `https://www.fac.gov/`
- Best for: Single Audit submission post-fieldwork.
- Skill pack: `skills/single-audit-prep-federal-750k/SKILL.md`.
- Source: https://www.fac.gov/audit-resources/submission-guide/about/

### Independent Sector — Value of Volunteer Time

National rate $33.49/hr (2024); used to value in-kind volunteer hours.

- Endpoint: https://independentsector.org/resource/value-of-volunteer-time/
- Best for: standardized in-kind match valuation.
- Skill pack: `skills/matching-funds-in-kind-strategy/SKILL.md`.
- Source: https://independentsector.org/resource/value-of-volunteer-time/

### Benevity Goodness Platform

AI-native corporate purpose software; >50% Fortune 100.

- Best for: applying as a Cause to corp giving + volunteering programs.
- Skill pack: `skills/corp-giving-csr-bumblebee-goodera/SKILL.md`.
- Source: https://benevity.com/

### YourCause CSRconnect (Blackbaud)

Enterprise CSR platform.

- Best for: Fortune 1000 corp giving + employee engagement programs.
- Skill pack: `skills/corp-giving-csr-bumblebee-goodera/SKILL.md`.
- Source: https://www.blackbaud.com/products/yourcause-csrconnect

### Bonterra

All-in-one CSR + grant management bundle.

- Best for: mid-market corp giving + integrated grant tracking.
- Skill pack: `skills/corp-giving-csr-bumblebee-goodera/SKILL.md`.
- Source: https://www.bonterratech.com/

### Goodera

Corporate volunteering specialist; 50K+ nonprofit network.

- Best for: corp volunteer-hour partnerships + skills-based volunteering.
- Skill pack: `skills/corp-giving-csr-bumblebee-goodera/SKILL.md`.
- Source: https://www.goodera.com/

### MovingWorlds

Skills-based volunteering specialist.

- Best for: scaling skills-based volunteering as in-kind value beyond standard corp programs.
- Skill pack: `skills/corp-giving-csr-bumblebee-goodera/SKILL.md`.
- Source: https://movingworlds.org/

### Submittable

Funder submission + review platform.

- Best for: foundation portal submissions when funder uses Submittable.
- Skill pack: `skills/multi-grant-pipeline-mgmt/SKILL.md`.
- Source: https://submit.com/

### Fluxx Grantseeker

Enterprise grant management on both sides.

- Best for: orgs receiving from foundations that use Fluxx Grantmaker side.
- Skill pack: `skills/multi-grant-pipeline-mgmt/SKILL.md`.
- Source: https://www.fluxx.io/products/grantseeker

### Foundant GrantHub

Dedicated grantseeker pipeline tracker.

- Best for: orgs that want pipeline tracking without enterprise overhead.
- Skill pack: `skills/multi-grant-pipeline-mgmt/SKILL.md`.
- Source: https://www.foundant.com/grant-management/

### Bloomerang / DonorPerfect / Salesforce Nonprofit Cloud

Donor CRM tier (match to org revenue).

- Best for: <$1M revenue → Bloomerang + Notion; $1-10M → DonorPerfect; >$10M → Salesforce NPC.
- Skill pack: `skills/foundation-cultivation-program-officer/SKILL.md` + `skills/multi-grant-pipeline-mgmt/SKILL.md`.
- Sources: https://bloomerang.com/ · https://www.donorperfect.com/ · https://www.salesforce.org/products/nonprofit-cloud/

### National Network of Fiscal Sponsors

Directory of fiscal sponsors + Model A/C/F selection guide.

- Best for: matching project type to right sponsor + admin-fee benchmarking.
- Skill pack: `skills/fiscal-sponsorship-coordination/SKILL.md`.
- Source: https://www.fiscalsponsors.org/

### draw.io / diagrams.net (via `drawio-mcp`)

Logic model + Theory of Change visualization.

- Best for: 5-column logic model + ToC causal arrows + assumption layer.
- Skill pack: `skills/logic-model-inputs-activities-outputs-outcomes/SKILL.md`.
- Source: https://www.drawio.com/

### Playwright (via `playwright-mcp`)

UI walkthrough for Grants.gov Workspace submit + foundation portals without API.

- Best for: guided submission UX when API lacks the submit endpoint.
- Skill pack: `skills/grants-gov-sam-gov-submission/SKILL.md`.
- Source: https://playwright.dev/

---

## SOTA execution playbook

When the user names a use case, the agent picks the matching skill pack first:

| User asks | First-stop skill pack |
|---|---|
| "Find me grant prospects" | `grant-prospect-research-grants-gov-instrumentl-candid` |
| "Write an LOI to <funder>" | `loi-letter-of-inquiry-drafting` |
| "Draft a full proposal for <NOFO>" | `full-grant-proposal-narrative-methods-evaluation` |
| "Build a logic model" | `logic-model-inputs-activities-outputs-outcomes` |
| "Write a budget narrative" | `budget-narrative-justification` |
| "Set up grant deadline tracking" | `grant-deadline-calendar-management` |
| "Submit on Grants.gov" | `grants-gov-sam-gov-submission` |
| "Write a federal report (SF-425 / SF-PPR)" | `grant-reporting-interim-final` |
| "Cultivate <foundation> / PO" | `foundation-cultivation-program-officer` |
| "Am I compliant with 2 CFR 200?" | `federal-grant-compliance-omb-uniform-guidance` |
| "Research corp giving / CSR for <company>" | `corp-giving-csr-bumblebee-goodera` |
| "Set up our match / in-kind strategy" | `matching-funds-in-kind-strategy` |
| "Calculate indirect / NICRA" | `indirect-cost-nicra` |
| "Fill out SF-424 / SF-LLL / set up subaward" | `sf-424-sf-lll-subaward` |
| "Set up our grant pipeline" | `multi-grant-pipeline-mgmt` |
| "Find a fiscal sponsor" | `fiscal-sponsorship-coordination` |
| "Are we triggering Single Audit?" | `single-audit-prep-federal-750k` |
| "Write a capital campaign proposal" | `capital-campaign-capacity-equipment-grants` |
| "Why did we get declined?" | `declined-grant-iteration` |
| "Verify our 501(c)(3) docs" | `irs-501c3-compliance-docs` |

---

## Closing rules

Funder priorities outrank your project priorities — align or lose. Logic models force clarity; if you can't draw the arrow from activity to outcome, you can't write the section. Reporting begins at award acceptance, not 11 months later. Always disclose "consult a licensed CPA / nonprofit attorney for binding compliance, tax, or audit decisions."
