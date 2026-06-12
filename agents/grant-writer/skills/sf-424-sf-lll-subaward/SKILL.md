---
name: sf-424-sf-lll-subaward
description: Complete the SF-424 family forms, SF-LLL lobbying disclosure, and set up subaward agreements that meet 2 CFR 200.331 monitoring requirements. Use when the user says "fill out SF-424" / "we have a subrecipient" / "lobbying disclosure" / "set up a subaward".
---

# SF-424 family + SF-LLL + subaward setup

The SF-424 family is the OMB-standard application package for federal assistance. SF-LLL is the lobbying disclosure attached only if lobbying activity is present. Subaward setup per 2 CFR 200.331 requires risk assessment + monitoring plan + written agreement. This skill is the mechanics layer — content of the narrative belongs to other skills.

Disclaimer: For binding decisions on whether activity triggers SF-LLL, sub-recipient vs contractor classification, or subaward indemnification terms, consult a qualified grants professional or nonprofit attorney.

## When to use

- Federal grant submission requires SF-424 + SF-424A + SF-424B (most common)
- Construction grant requires SF-424C + SF-424D
- Project budget includes a sub-recipient (organization receiving federal funds through you)
- Lobbying activity has occurred related to the federal grant (triggers SF-LLL)
- Annual review of sub-recipient monitoring plan
- First subaward setup — need agreement template + risk assessment

Do NOT use this skill for:
- Grants.gov Workspace UI walkthrough → `grants-gov-sam-gov-submission`
- Budget narrative content → `budget-narrative-justification`
- SAM.gov entity registration → `grants-gov-sam-gov-submission`
- Sub-recipient performance reporting → `grant-reporting-interim-final`

## Setup

```bash
# Form download (free PDFs)
# https://www.grants.gov/forms/forms-repository/sf-424-family

# SF-424 family forms (download from above)
# - SF-424.pdf (general)
# - SF-424A.pdf (budget non-construction)
# - SF-424B.pdf (assurances non-construction)
# - SF-424C.pdf (budget construction)
# - SF-424D.pdf (assurances construction)
# - SF-LLL.pdf (lobbying disclosure)

# Tools: pdf (form fill), xlsx (SF-424A spreadsheet), docx (SF-LLL + subaward agreement)
```

Auth / API key requirements: None for forms. Subaward agreement signed by authorized representatives of both parties.

## Common recipes

### Recipe 1: SF-424 family decision tree

```markdown
## Which SF-424 do I use?

Federal grant application?
├── Construction grant? → SF-424C + SF-424D
├── Mandatory / formula / block grant? → SF-424 Mandatory family
├── Short form allowed (NOFO says "SF-424 Short Org")? → SF-424 Short Org
├── Individual / fellowship / traveler? → SF-424 Individual family
└── Standard discretionary? → SF-424 + SF-424A + SF-424B + program-specific
```

### Recipe 2: SF-424 field-by-field

```markdown
## SF-424 main form

| Box | Field | Source |
|---|---|---|
| 1 | Type of submission | Application / Pre-application / Changed-Corrected |
| 2 | Type of application | New / Continuation / Revision (+ Other: amend) |
| 3 | Date received | Auto-filled at submit; leave blank |
| 4 | Applicant identifier | Internal tracking ID; optional |
| 5a | Federal entity identifier | If passed through state, leave blank |
| 5b | Federal award identifier | Continuation/revision only; leave blank for new |
| 6 | Date received by state | State pass-through only; leave blank otherwise |
| 7 | State application identifier | State pass-through only |
| 8 | Applicant info | Legal name, EIN, UEI, mailing addr, phone (from SAM) |
| 9 | Type of applicant | A: state govt; B: county; C: city/township; D: special district; E: regional; F: independent school; G: public/state college; H: public/Indian housing auth; I: Indian/Native American tribal govt (federally recognized); J: Indian/Native American tribal govt (other); K: Indian/Native American tribal designated; L: public/Indian housing; M: nonprofit with 501(c)(3) status; N: nonprofit without 501(c)(3); O: private institution of higher ed; P: individual; Q: for-profit small; R: for-profit other than small; S: Native American tribal organization; T: U.S. territory; U: nonprofit (faith-based); V: regional educational service agency; W: child welfare agency; X: Native village/regional non-profit; Y: other |
| 10 | Name of federal agency | From NOFO |
| 11 | Catalog of federal domestic assistance (CFDA) | From NOFO (e.g., 93.110) |
| 12 | Funding opportunity number | From NOFO |
| 13 | Competition identification | If multiple competitions under one opp |
| 14 | Areas affected | County / state list |
| 15 | Project title | Match Workspace, budget, narrative |
| 16 | Congressional districts | Applicant (16a) + Project location (16b) |
| 17 | Proposed project | Start date + end date |
| 18 | Estimated funding | a-Federal / b-Applicant / c-State / d-Local / e-Other / f-Program income / g-Total |
| 19 | State review under EO 12372 | Yes (state reviewed) / No (program not covered) / N/A |
| 20 | Delinquent on federal debt | Yes / No (must be No to be eligible) |
| 21 | Authorized representative signature | AOR — legally binding |
```

### Recipe 3: SF-424A budget detail

```markdown
## SF-424A — Section A: Budget Summary

| Object class | Federal | Non-Federal | Total |
|---|---|---|---|
| a. Personnel | $X | $Y | $X+Y |
| b. Fringe Benefits | | | |
| c. Travel | | | |
| d. Equipment | | | |
| e. Supplies | | | |
| f. Contractual | | | |
| g. Construction | | | |
| h. Other | | | |
| i. Total Direct (sum a-h) | | | |
| j. Indirect | | | |
| k. Total (i + j) | | | |

## SF-424A — Section B: Budget Categories per Federal Activity
For each grant program / activity, list a-k columns

## SF-424A — Section C: Non-Federal Resources
| Source | Cash | In-kind | Total |
|---|---|---|---|
| Applicant | $ | $ | $ |
| State | | | |
| Other | | | |

## SF-424A — Section D: Forecasted Cash Needs (Federal cash request by quarter)

## SF-424A — Section E: Budget Estimates for Federal Funds Needed for Balance of Project (multi-year)
```

### Recipe 4: SF-424B assurances (read before signing)

```markdown
## SF-424B Assurances — Non-Construction
The applicant certifies (among other things):
1. Legal authority to apply
2. Comply with 2 CFR 200 (Uniform Guidance) + cost principles
3. Maintain accounting system + audit per Single Audit Act
4. Comply with Civil Rights Act of 1964 (Title VI), Section 504 of Rehab Act, ADA
5. Comply with Age Discrimination Act of 1975
6. Comply with Hatch Act limits on political activity
7. Comply with environmental laws (NEPA, etc.)
8. Comply with Davis-Bacon Act (construction wage rates)
9. Comply with Drug-Free Workplace Act
10. Comply with Trafficking Victims Protection Act
11. Comply with Lobbying Disclosure Act (triggers SF-LLL if lobbying)
12. No false statements (False Claims Act exposure)

Read before signing. Signature = legally binding.
```

### Recipe 5: SF-LLL — when required

```markdown
## SF-LLL triggers
File SF-LLL ONLY if BOTH:
- Federal grant > $100K
- Lobbying activity has occurred or is committed in connection with the application
  - "Lobbying" = attempting to influence federal officer/employee/Member of Congress regarding the AWARDING of a federal contract, grant, loan, or cooperative agreement
  - Communication with PO about technical / clarifying matters = NOT lobbying
  - Hiring a lobbyist to push for award = lobbying
  - Educational outreach on policy = NOT lobbying for the specific award

## SF-LLL fields
| Field | Content |
|---|---|
| Type of federal action | a: contract; b: grant; c: cooperative agreement; d: loan; e: loan guarantee; f: loan insurance |
| Status of federal action | a: bid/offer/application; b: initial award; c: post-award |
| Report type | a: initial filing; b: material change |
| Reporting entity | Prime (your org) or sub-awardee |
| Federal program name + CFDA | From NOFO |
| Federal action $ amount | Federal request |
| Lobbying registrant name/address | The lobbyist or firm engaged |
| Individuals performing services | Names of lobbyists |
| Signature | AOR |
```

### Recipe 6: Sub-recipient vs contractor classification

```markdown
## Sub-recipient OR contractor? (2 CFR 200.331)

| Test | Sub-recipient | Contractor |
|---|---|---|
| Programmatic decision-making | Yes — makes program decisions | No — follows your spec |
| Performance measured against fed objectives | Yes | No |
| Responsibility for compliance w/ fed program requirements | Yes | No |
| Use of federal funds to carry out program | Yes | No (provides goods/services) |
| Operates in a competitive environment | No | Yes (competitive procurement) |
| Provides goods / services for many customers | No | Yes |

## If checking 3+ sub-recipient boxes → sub-recipient → 2 CFR 200.331 applies
## If checking 3+ contractor boxes → contractor → 2 CFR 200.317-200.327 procurement rules apply
```

### Recipe 7: Sub-recipient risk assessment (2 CFR 200.332)

```markdown
## Pre-award risk assessment
For each prospective sub-recipient, assess:
1. Prior experience with same/similar federal awards (PROPN: ProPublica + FAPIIS)
2. Audit results: prior Single Audit findings? Material weaknesses? Unresolved findings?
3. Financial stability: audited financials, going concern flags
4. Programmatic capacity: track record, staff qualifications, infrastructure
5. Personnel changes: leadership stability
6. Federal debarment: SAM.gov exclusion list check

## Risk classification
- Low risk: established federal sub-awardee, clean audit, stable leadership
- Medium risk: limited federal experience OR some prior findings (resolved)
- High risk: first federal subaward, going concern flag, unresolved audit findings

## Risk-based monitoring intensity
- Low: annual financial review + annual programmatic report
- Medium: quarterly financial + quarterly programmatic + 1 site visit/yr
- High: monthly financial + monthly programmatic + 2+ site visits/yr + reimbursement (not advance)
```

### Recipe 8: Subaward agreement template

```markdown
## Subaward Agreement (key clauses)

1. **Parties + period of performance** — recipient (prime) + sub-recipient; start/end dates
2. **Federal award identifier** — prime award number, CFDA, federal agency, period of perf
3. **Scope of work** — detailed deliverables, activities, milestones
4. **Total subaward amount + budget** — by object class, federal/non-federal share
5. **Payment terms** — reimbursement (preferred) or advance with monthly cash reconciliation
6. **Indirect cost rate** — sub's NICRA or de minimis or NOFO cap
7. **Compliance requirements** — flow down 2 CFR 200 to sub; specific applicable terms
8. **FFATA reporting** — for sub-awards > $30K (transparency.gov reporting)
9. **Reporting requirements** — financial + performance per recipient's schedule
10. **Monitoring + site visits** — schedule + scope
11. **Audit requirements** — sub's Single Audit if ≥ $1M federal; right of access
12. **Subrecipient certifications** — debarment, anti-lobbying, drug-free workplace, etc.
13. **Termination clauses** — for cause, for convenience, expiration
14. **IP / data rights** — per federal award terms
15. **Notice + dispute resolution** — addresses, escalation, governing law
16. **Indemnification + insurance** — usually mutual indemnification + sub maintains GL/PL insurance
17. **Signatures + dates** — AORs for both parties
```

### Recipe 9: FFATA reporting (sub-awards > $30K)

```markdown
## FFATA Subaward Reporting System (FSRS)
Per FFATA, prime recipients must report sub-awards > $30K within 30 days of subaward.

Report at: https://www.fsrs.gov/
Required data:
- Sub-recipient name, address, DUNS/UEI
- Sub-award amount
- Sub-award date
- Period of performance
- Description
- Place of performance
- Officer compensation (top 5) IF sub-recipient meets size thresholds

Update annually. Failure to report = potential disallowance.
```

### Recipe 10: Subaward monitoring annual checklist

```markdown
## Annual sub-recipient monitoring

| Task | Cadence | Owner |
|---|---|---|
| Pre-award risk reassessment | Annually + at renewal | Grant writer + finance |
| Financial reports review | Per agreement (monthly/quarterly) | Finance |
| Performance reports review | Per agreement | Grant writer + program |
| Site visit | 1-2x/yr depending on risk | Program + finance |
| Single Audit review | Within 9 mo of sub's FY-end | Finance |
| Corrective action plan tracking | If audit findings, monthly | Finance + grant writer |
| Closeout | At subaward end | Grant writer + finance |
```

## Examples

### Example 1: Standard discretionary submission — SF-424 + 424A + 424B

**Goal:** Submit a $300K HRSA application with no construction, no subawards, no lobbying.

**Steps:**
1. Pull SAM-verified org info into SF-424 boxes 8 (Recipe 2).
2. NOFO indicates Type of Applicant M (nonprofit 501(c)(3)).
3. Box 18: Federal $300K + Applicant $50K match + Total $350K.
4. SF-424A Section A: Object class breakdown matching budget narrative.
5. SF-424A Section C: Non-federal $50K match.
6. SF-424A Section D: Quarterly cash needs $75K x 4.
7. SF-424B: AOR reads + signs all assurances.
8. NO SF-LLL (no lobbying activity).
9. Package all three; upload to Grants.gov Workspace; validate.

**Result:** Compliant application package; AOR submits per `grants-gov-sam-gov-submission`.

### Example 2: Subaward setup for a $400K NIH R01 with $80K sub-recipient

**Goal:** Issue subaward to a university partner for evaluation work.

**Steps:**
1. Sub-recipient vs contractor analysis (Recipe 6): University makes programmatic decisions on evaluation methodology → sub-recipient.
2. Pre-award risk assessment (Recipe 7): University has 50+ prior federal awards, clean audit → LOW risk.
3. Subaward agreement drafted (Recipe 8); route through `legal-counsel` for review.
4. Subaward amount $80K; first $25K in MTDC base; $55K excluded.
5. Sub's indirect: applies sub's NICRA (28%) on sub's $80K; flows through.
6. FFATA report filed within 30 days of executed subaward (Recipe 9).
7. Monitoring schedule: quarterly financial + biannual programmatic + 1 site visit (low risk).
8. Sub's Single Audit reviewed (sub already does Single Audit due to size).

**Result:** Compliant subaward; monitoring schedule documented; FFATA filed.

## Edge cases / gotchas

- **SF-LLL is rarely needed.** Most nonprofits don't lobby for specific awards. If unsure, default to "no SF-LLL" but document the determination.
- **AOR vs Workspace owner.** AOR signs SF-424 box 21. Workspace owner can be anyone; AOR must be the legally authorized signer.
- **Box 19 EO 12372 state review.** Most states have NO state plan; default "Program not covered". Some programs DO require state plan review (e.g., USDA). Check NOFO.
- **Box 20 Delinquent on federal debt = ELIGIBILITY.** Must answer No. If Yes (rare), org is ineligible.
- **SF-424A and budget narrative must reconcile to the dollar.** If SF-424A says Personnel $80K, budget narrative says Personnel $80,500, reviewers flag.
- **Sub-recipient vs contractor matters for audit.** Sub-recipients are subject to 2 CFR 200.331; contractors are not. Misclassification = audit finding.
- **First $25K rule changed.** Pre-Oct 2024: first $25K of EACH subaward. Post-Oct 2024: first $25K TOTAL across all subawards. Verify on every NOFO.
- **FFATA threshold $30K stable since 2010.** Sub-award > $30K = FFATA report required.
- **State pass-through and assurances.** When you receive a federal pass-through from a state, your SF-424B assurances STILL apply.
- **Construction grants are a different family.** SF-424C + SF-424D and Davis-Bacon wage rates apply. Route through procurement specialist.
- **Lobbying definition is narrow.** Educational policy work, association advocacy = NOT lobbying for the specific award. Hiring registered lobbyists = lobbying. When unclear, route through `legal-counsel`.
- **Disclaimer.** For binding decisions on subaward vs contract classification, lobbying determination, or indemnification clauses, consult a qualified grants professional or nonprofit attorney.

## Sources

- SF-424 family (forms repository): https://www.grants.gov/forms/forms-repository/sf-424-family
- SF-424 Mandatory family: https://www.grants.gov/forms/sf-424-mandatory-family.html
- SF-424 Short Organization: https://www.grants.gov/forms/forms-repository/sf-424-short-organization-family
- SF-424 Individual: https://www.grants.gov/forms/forms-repository/sf-424-individual-family
- SF-LLL form + instructions: https://www.grants.gov/forms/post-award-reporting-forms.html
- 2 CFR 200.331 (Subrecipient + contractor determinations): https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D/section-200.331
- 2 CFR 200.332 (Requirements for pass-through entities): https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D
- FFATA Subaward Reporting System (FSRS): https://www.fsrs.gov/
- USAspending FFATA guidance: https://www.usaspending.gov/help/ffata-subaward-reporting
- Lobbying Disclosure Act guidance: https://lobbyingdisclosure.house.gov/
