---
name: matching-funds-in-kind-strategy
description: Build a match + in-kind contribution strategy that complies with 2 CFR 200.306 — value, document, and track cash match and third-party in-kind separately. Use when the user says "we need a match" / "value our volunteer hours" / "track in-kind" / "the NOFO requires 25% match".
---

# Matching funds + in-kind strategy

Federal NOFOs (and many foundations) require a match — non-federal share contributed to the project. Per 2 CFR 200.306, match must be verifiable, allowable, allocable, necessary, and reasonable. Third-party in-kind (e.g., volunteer hours, donated goods, donated space) counts if documented at fair value. Cash match and in-kind get tracked SEPARATELY on SF-425.

Disclaimer: For binding determinations on whether a contribution qualifies as match (especially cost-sharing across federal awards, indirect cost as match, or salary cap interactions), consult a qualified grants professional or CPA.

## When to use

- A NOFO requires a non-federal match (e.g., 25%, 50%, 100%, 200%)
- Foundation requires "leverage" or "match" demonstration
- Cultivating in-kind donors (volunteers, pro bono services, donated space, donated supplies)
- Multi-year project needs annual match commitment letters
- Auditor requests match documentation during Single Audit
- Building a match tracker for a portfolio of grants

Do NOT use this skill for:
- Federal cost principles for direct costs → `budget-narrative-justification` + `federal-grant-compliance-omb-uniform-guidance`
- Indirect cost rate selection → `indirect-cost-nicra`
- Multi-grant pipeline tracking → `multi-grant-pipeline-mgmt`
- Final SF-425 financial reporting of match → `grant-reporting-interim-final`

## Setup

```bash
# No paid tools required.
# Reference:
# - 2 CFR 200.306 (cost sharing / matching): https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D
# - Independent Sector volunteer time rate (annual): https://independentsector.org/resource/value-of-volunteer-time/

# Tools used: xlsx (match tracker), docx (in-kind letters), gmail-mcp (donor confirmations)

# Match tracker template (in xlsx)
# Columns: Grant | Source | Type (Cash / In-kind) | Description | Date Provided | Fair Value | Documentation
```

Auth / API key requirements: None.

## Common recipes

### Recipe 1: Match terminology — get it right

```markdown
| Term | Meaning |
|---|---|
| Match | Non-federal share required by the NOFO |
| Cost-share | Synonym for match (NIH uses "cost-share"; HHS uses "match") |
| Cash match | Non-federal cash contributed to the project (org funds, other grant funds, donor gifts) |
| In-kind match | Third-party goods/services contributed at fair value |
| Hard match | Cash |
| Soft match | In-kind |
| Mandatory match | NOFO requires; ineligible if not met |
| Voluntary match | Org offers above the requirement to signal commitment |
| Leverage | Foundation-side term; less strict documentation than federal match |
```

### Recipe 2: Compute the required match amount

```markdown
## Match calculation
If NOFO says "25% match":
- Federal share = 75% of total project
- Non-federal share = 25% of total project
- Match RATIO = 25 / 75 = 33.3% of federal request

Example: federal request $300K, 25% match required
- Federal: $300K (75% of total)
- Match: $100K (25% of total)
- Total project: $400K
- Match-to-federal ratio: 33.3%

## Match is on TOTAL, not on federal request — read NOFO carefully
- Some NOFOs: "25% of TOTAL project costs"
- Some NOFOs: "25% of federal request" → $300K × 25% = $75K
- Difference is significant; misreading = under-match = ineligibility
```

### Recipe 3: Sources of allowable match (federal)

```markdown
## Allowable match sources (2 CFR 200.306)
✓ Org's unrestricted cash applied to project
✓ Other non-federal grant funds (foundation, state, corporate, individual donor) — only if NOT already cost-shared on another federal award
✓ Third-party in-kind (volunteer hours, donated goods, donated space, donated professional services)
✓ Earned program income retained per 200.307
✓ Unrecovered indirect costs (with prior agency approval per 200.306(c))

## NOT allowable match
✗ Federal funds (cannot match federal with federal unless statute allows; rare)
✗ Costs incurred before period of performance
✗ Costs charged to another federal award (double-dipping)
✗ Donated goods you'd buy anyway with project funds (must be net-new)
✗ Volunteer time from federal employees acting in official capacity
✗ Unrealistic future commitments (must be documented in hand)
```

### Recipe 4: Value third-party in-kind contributions

```markdown
## Fair value methodology (2 CFR 200.306(e))

| In-kind type | Valuation basis |
|---|---|
| General volunteer hours | Independent Sector national rate ($33.49/hr 2024; updated annually) |
| Skilled volunteer hours | Equivalent labor market rate (e.g., CPA = BLS rate for accountant ~$45/hr) |
| Pro bono professional services | Donor's standard rate × hours (with written attestation) |
| Donated supplies | Vendor invoice or fair market value (FMV) at date of donation |
| Donated equipment (≥$10K) | Independent appraisal required |
| Donated space | Comparable rental rate (commercial sq ft × hrs/month) |
| Donated travel | Actual airfare receipts or per diem rate |
| Donated food (event) | FMV from caterer or grocery |

## Independent Sector rate (use for general volunteer hours)
- 2024 national: $33.49/hr
- State-specific rates published annually
- Per https://independentsector.org/resource/value-of-volunteer-time/
- Re-check rate before each report submission (updates annually April)
```

### Recipe 5: In-kind commitment letter template

```markdown
## In-Kind Donor Letter (collect BEFORE submission)

[Date]
[Recipient nonprofit address]

Re: In-Kind Commitment for <Project Name>

To Whom It May Concern,

[Donor org] commits to provide the following in-kind contribution to [Recipient nonprofit] for the
<Project Name> project funded by [Federal agency / Funder], period of performance
[start date] to [end date]:

| Item | Quantity | Fair Value | Basis |
|---|---|---|---|
| [Service / good] | [units] | $[amount] | [vendor quote / labor rate / FMV] |

Total in-kind contribution: $[total]

This contribution will be delivered during the period of performance, is not charged
to any other federal award, and is provided at no cost to the recipient. We will provide
detailed documentation (timesheets / receipts / signed delivery confirmation) at project close.

Sincerely,
[Authorized signer], [Title], [Donor org]
```

### Recipe 6: Volunteer hour tracking

```markdown
## Volunteer log requirements (per 200.306)
Each volunteer hour requires:
- Volunteer name
- Date
- Hours worked
- Project / activity
- Description of work
- Signature (volunteer + supervisor)
- Skill level (general vs skilled — affects rate)

## Volunteer log template (xlsx)
| Volunteer Name | Date | Hours | Activity | Skill Category | Rate Applied | Value |
|---|---|---|---|---|---|---|
| Jane Doe | 2026-06-01 | 4 | Direct service | General | $33.49 | $133.96 |
| Bob Smith CPA | 2026-06-15 | 8 | Bookkeeping | Skilled (CPA) | $52.00 | $416.00 |

Monthly aggregate goes into SF-425 Recipient Share.
```

### Recipe 7: Match tracker template

```markdown
## Portfolio match tracker (xlsx)

| Grant | Award $ | Match Required | Cash Match Committed | Cash Source | In-Kind Committed | In-Kind Source | YTD Achieved | Variance |
|---|---|---|---|---|---|---|---|---|
| HRSA #ABC | $300K | $100K (25%) | $60K | Smith Foundation $40K + org $20K | $40K | 1,200 vol hrs | $80K | -$20K |
| ED #XYZ | $200K | $100K (50%) | $80K | Annual fund | $20K | Donated space | $90K | -$10K |

## Variance flag = match < pace
- Q1: 25% YTD; Q2: 50%; etc.
- Below pace = sound alarm with development team
- If variance persists past Q3, formally amend match composition with PO
```

### Recipe 8: Reporting match on SF-425

```markdown
## SF-425 Federal Financial Report — match lines
- Line 10g: Federal Share of Expenditures
- Line 10i: Recipient Share REQUIRED (per award terms)
- Line 10j: Recipient Share OF EXPENDITURES (what you actually contributed)
- Line 10k: Remaining recipient share to be provided

## Cumulative vs reporting-period
- Most SF-425 cycles: cumulative + period
- Recipient share documented = cash + in-kind together
- Auditor will trace each in-kind line to volunteer log / donor letter / receipt
```

### Recipe 9: Match risk levels

```markdown
## Risk-tier your match composition

| Tier | Risk | Examples |
|---|---|---|
| Low risk | Cash in hand at award acceptance | Org unrestricted reserves; already-received grants |
| Medium risk | Cash committed in writing | Foundation MoU; pledge from individual donor |
| Higher risk | In-kind volunteer hours | Recurring volunteer program with track record |
| Highest risk | Future fundraising for match | "We'll raise $50K in match by Q4" — auditors disfavor |

## Minimum recommendation
50% of match should be in tiers 1-2 (cash in hand or committed) at award acceptance.
```

### Recipe 10: Indirect costs as match (with approval)

```markdown
## Unrecovered indirect as match
Per 2 CFR 200.306(c), with prior agency approval:
- If your NICRA rate is 25% but you only charge 15% as direct, the "unrecovered" 10% can count as match
- BUT: requires written agency approval BEFORE submission; not all agencies allow

Example:
- NICRA rate: 25% × MTDC of $200K = $50K
- Actual indirect charged: 15% × $200K = $30K
- Unrecovered indirect: $20K
- IF agency-approved: $20K counts toward match
```

## Examples

### Example 1: Build match for a $400K HRSA application with 25% match requirement

**Goal:** Source $100K match for a 3-year MCH project.

**Steps:**
1. Compute required match: $400K total × 25% = $100K non-federal share.
2. Identify cash sources: $60K from org unrestricted + $20K Smith Foundation MoU = $80K cash.
3. Identify in-kind: 600 volunteer hrs/yr × 3 yrs × $33.49 = $60,282 → use $40K conservative.
4. Recipe 5: collect in-kind commitment letters from each donor org (volunteer corps, donated space partner).
5. Recipe 7: build portfolio match tracker; baseline shown.
6. Document in Project Narrative + Budget Narrative.
7. Set quarterly variance check; alarm if YTD match < 75% of pace.

**Result:** $80K cash + $40K in-kind = $120K committed against $100K requirement (20% buffer).

### Example 2: Value volunteer hours for a foundation report

**Goal:** Demonstrate $30K leverage to Kresge for a $100K grant.

**Steps:**
1. Pull volunteer log: 1,000 hours in reporting period.
2. Apply Independent Sector rate: 1,000 × $33.49 = $33,490 general volunteer value.
3. Add skilled volunteer hours (5 board members × 10 hrs each × $75/hr) = $3,750.
4. Total in-kind: $37,240.
5. Add cash leverage from board giving: $15K.
6. Total leverage demonstrated: $52,240 against $30K target.
7. Document in report narrative + attach volunteer log summary.

**Result:** Leverage exceeded; Kresge renewal cultivation strengthened.

## Edge cases / gotchas

- **You can't match federal with federal (almost always).** Unless statute explicitly authorizes (rare — e.g., some HUD programs), federal funds CANNOT match federal.
- **Match counted on one award only.** A single donor gift can match ONE federal award; can't double-count across two.
- **Pre-award costs.** Costs incurred before period of performance don't count as match (with rare exceptions per 200.458).
- **Salary cap interaction (NIH).** If a researcher's salary is above NIH cap, the "above cap" portion can count as match.
- **Volunteer time for federal employees in official capacity = ineligible.** Off-duty federal employees as private citizens = eligible.
- **Documentation = the audit gate.** Auditors WILL trace every in-kind line. No documentation = disallowed = clawback risk.
- **Annual Independent Sector rate update.** Rate changes annually (April). Use the rate IN EFFECT at the time of the volunteer activity, not at report time.
- **State-specific rates.** Independent Sector publishes state-by-state rates; some auditors prefer state rate over national.
- **Donated services from related parties.** Donor must be third-party (not the recipient or related). Board members donating professional time = OK; staff "donating" overtime = NOT match (that's compensation).
- **Time studies for personnel charged < 100%.** If a staff member is split-funded across awards + match, you need time studies / activity reports per 200.430(i).
- **Disclaimer.** For binding determinations on whether a specific contribution qualifies as match, contact your federal program officer and/or consult a qualified grants professional / CPA.

## Sources

- 2 CFR 200.306 (Cost sharing or matching): https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D/subject-group-ECFR2afe8a0b08d1cdc/section-200.306
- 2 CFR 200.307 (Program income): https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D/subject-group-ECFR2afe8a0b08d1cdc/section-200.307
- 2 CFR 200.430 (Compensation — personal services): https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-E
- Independent Sector — Value of Volunteer Time: https://independentsector.org/resource/value-of-volunteer-time/
- Independent Sector — State-by-state rates: https://independentsector.org/resource/value-of-volunteer-time/
- HRSA Cost Share guidance: https://www.hrsa.gov/grants/manage-your-grant/matching-cost-share
- NIH cost-sharing: https://grants.nih.gov/grants/policy/nihgps/HTML5/section_8/8.1.3_cost_sharing_or_matching.htm
