---
name: budget-narrative-justification
description: Build reviewer-ready budget narratives paired with SF-424A — every line allowable + allocable + reasonable per 2 CFR 200 Subpart E + agency cost principles. Use when the user says "write a budget narrative" / "justify our budget" / "draft the budget section".
---

# Budget narrative + budget justification

Federal reviewers score narrative not spreadsheet. Every budget line must be allowable under cost principles (2 CFR 200 Subpart E), allocable to the project, and reasonable given the market. The narrative explains your math — without it, even a correct budget gets downscored.

Disclaimer: For binding decisions on cost allowability, indirect cost classification, or audit risk, consult a qualified grants professional or CPA.

## When to use

- Drafting a federal grant proposal (Subpart E compliance required)
- Drafting a foundation proposal where the funder requires budget narrative
- Multi-year project budget across period of performance
- Revising a budget after declined proposal with "budget unclear" feedback
- Subaward / pass-through budget detail per 2 CFR 200.331

Do NOT use this skill for:
- SF-424A form fill alone (→ `sf-424-sf-lll-subaward`)
- Indirect cost rate negotiation strategy (→ `indirect-cost-nicra`)
- Match / in-kind valuation methodology (→ `matching-funds-in-kind-strategy`)
- Capital budget construction (→ `capital-campaign-capacity-equipment-grants`)

## Setup

```bash
# Tools
# - xlsx (SF-424A spreadsheet + multi-year detail)
# - docx (narrative)
# - cli-anything → eCFR for 2 CFR 200 lookups

# Templates
ls agent_bundle/agents/grant-writer/templates/sf424a_multiyear.xlsx
ls agent_bundle/agents/grant-writer/templates/budget_narrative.docx

# Reference: 2 CFR 200 Subpart E
curl https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-E
```

Auth / API key requirements: None. eCFR is free + open.

## Common recipes

### Recipe 1: SF-424A object class categories

```markdown
| Code | Category | Examples |
|---|---|---|
| a | Personnel | Salaries (PI, project staff) |
| b | Fringe Benefits | Health, retirement, payroll tax (FICA, SUTA, FUTA) |
| c | Travel | Per diem, mileage, lodging, airfare |
| d | Equipment | Items ≥$10K per 2024 update |
| e | Supplies | Items <$10K |
| f | Contractual | Subawards (first $25K in MTDC), consultants |
| g | Construction | Land, buildings (construction grants only) |
| h | Other | Communications, rent, printing, software subscriptions |
| i | Total Direct | Sum of a-h |
| j | Indirect | De minimis 15% MTDC OR NICRA rate × MTDC |
| k | Total | Direct + Indirect |
```

### Recipe 2: The three federal cost tests for every line

```
Allowability: Permitted by 2 CFR 200 Subpart E + agency-specific cost principles + NOFO.
Allocability: Charged in proportion to the benefit received by the project.
Reasonableness: A prudent person would have paid the price for the good / service.

Federal reviewers score lines that fail any of these. Document each in narrative.
```

### Recipe 3: Personnel budget detail

```markdown
**a. Personnel — $XXX,XXX**

| Role | Base salary | % FTE | Months | Cost |
|---|---|---|---|---|
| PI (Dr. Chen) | $120,000 | 20% | 12 | $24,000 |
| Project Manager (TBD) | $85,000 | 100% | 12 | $85,000 |
| Evaluator | $95,000 | 30% | 12 | $28,500 |
| Data Analyst | $70,000 | 50% | 12 | $35,000 |

**Allowability:** Personnel compensation is allowable per 2 CFR 200.430.
**Allocability:** Effort calculated via time-and-effort certification (200.430(i)).
PI 20% allocation reflects scientific oversight + IRB management.
**Reasonableness:** Salaries benchmarked against BLS OEWS 2024 for SOC code
21-1018 (Substance abuse, behavioral disorder, & mental health counselors) at 75th percentile.
```

### Recipe 4: Fringe benefits

```markdown
**b. Fringe Benefits — $XX,XXX**

Org's actual fringe rate from FY24 audited financials: 26.5% of personnel.
Components: FICA 7.65%, SUTA 1.5%, FUTA 0.6%, health insurance 12%, retirement 4.7%.

Fringe = 26.5% × $172,500 (Personnel) = $45,712

**Allowability:** Per 2 CFR 200.431.
**Basis:** Organization-wide pooled fringe rate, audited.
```

### Recipe 5: Travel

```markdown
**c. Travel — $XX,XXX**

| Purpose | Travelers | Trips | Days | Per-diem | Cost |
|---|---|---|---|---|---|
| Annual federal grantee meeting (D.C.) | 2 | 1 | 3 | $282/day | $1,692 + $800 air × 2 = $3,292 |
| Site visits to subgrantees (3 sites × 2 visits) | 1 | 6 | 1 | $200/day | $1,200 + $500 air × 6 = $4,200 |

Per-diem rates per GSA https://www.gsa.gov/travel/plan-book/per-diem-rates.

**Allowability:** Per 2 CFR 200.474. Foreign travel requires prior approval.
**Reasonableness:** Coach airfare; standard hotel; GSA rates for per-diem.
```

### Recipe 6: Equipment vs Supplies threshold

```markdown
**d. Equipment — $XX,XXX**

Equipment threshold raised to $10,000 per item in Oct 2024 revision (2 CFR 200.439).
Items ≥$10K listed here; items <$10K in Supplies (e).

| Item | Quantity | Unit cost | Total |
|---|---|---|---|
| 3D printer for prototyping lab | 1 | $12,500 | $12,500 |

**Allowability:** Necessary for project activities (prototype iteration).
**Allocability:** 100% dedicated to project; tagged in inventory.
**Reasonableness:** Three vendor quotes obtained; lowest selected.

**e. Supplies — $XX,XXX**

| Item | Quantity | Unit cost | Total |
|---|---|---|---|
| Printing curriculum materials | 200 sets | $25 | $5,000 |
| Postage for follow-up surveys | 600 mailings | $0.85 | $510 |
| Office supplies (allocable share) | n/a | n/a | $1,200 |
```

### Recipe 7: Contractual / subawards

```markdown
**f. Contractual — $XX,XXX**

| Subaward | Scope | Total |
|---|---|---|
| University X Evaluation | Quasi-experimental impact eval | $85,000 |
| Community Org Y service delivery | Direct service to 60 families | $50,000 |

**Subaward monitoring per 2 CFR 200.331:**
- Risk assessment completed pre-award (financial stability, prior audit, capacity).
- Monitoring: quarterly progress reports + annual site visit + quarterly financial review.
- FFATA reporting if >$30,000.

**MTDC base note:** First $25,000 of each subaward is included in MTDC base for
indirect cost calculation; amounts beyond $25,000 are excluded (2 CFR 200.414).
```

### Recipe 8: Other (rent, comms, software, printing)

```markdown
**h. Other — $XX,XXX**

| Item | Cost | Justification |
|---|---|---|
| Project share of office rent (15% × $36K) | $5,400 | 15% allocation per square-footage. |
| Communications (phone, internet share) | $1,800 | Same 15% share. |
| Software subscriptions (REDCap, Qualtrics) | $3,200 | Required for data collection. |
| Printing reports + dissemination | $1,500 | Final report + 4 quarterly reports. |
```

### Recipe 9: Indirect cost line

```markdown
**i. Total Direct Costs — $XXX,XXX**

**j. Indirect Costs — $XX,XXX**

De Minimis 15% MTDC per 2 CFR 200.414(f) (updated Oct 2024 from 10% to 15%).

MTDC base calculation:
- Total Direct Costs:                $250,000
- LESS Equipment (>$10K each):      ($12,500)
- LESS Subaward portions >$25K:     ($85,000 subaward - $25,000 in MTDC = -$60,000)
- LESS Participant support:               $0
- LESS Pass-through beyond $25K:           $0
- LESS Rental costs:                  ($5,400)
- MTDC base:                        $172,100

Indirect: 15% × $172,100 = $25,815

**k. Total Project Costs — $XXX,XXX**

Direct ($250,000) + Indirect ($25,815) = $275,815
```

### Recipe 10: Multi-year period of performance budget

```bash
# Each year is a column on SF-424A worksheet
# Build in xlsx with formulas:
# Year 1, Year 2, Year 3, Cumulative
# Object class rows with Year 1 + escalation factors (typical 3-4% annual)
# Total column at right
```

```markdown
| Object class | Year 1 | Year 2 | Year 3 | Total |
|---|---|---|---|---|
| a. Personnel | $172,500 | $177,675 | $183,005 | $533,180 |
| b. Fringe | $45,712 | $47,084 | $48,496 | $141,292 |
| ... | ... | ... | ... | ... |
| k. Total | $275,815 | $283,650 | $291,720 | $851,185 |
```

### Recipe 11: Match column on SF-424A

```markdown
| Object class | Federal Share | Recipient Share (Match) | Total |
|---|---|---|---|
| a. Personnel | $138,000 | $34,500 | $172,500 |
| b. Fringe | $36,570 | $9,142 | $45,712 |
| ... | ... | ... | ... |
| k. Total | $220,652 | $55,163 | $275,815 |

Match: 20% non-federal share, verified per match strategy
(see matching-funds-in-kind-strategy skill).
```

### Recipe 12: Reconciliation check

```bash
# Cross-check before submission:
# 1. SF-424A grand total = Budget narrative grand total = Project narrative cost mentions
# 2. Multi-year totals = Cumulative line on SF-424A
# 3. Indirect rate × MTDC base = Indirect line (to the dollar)
# 4. Each subaward's first $25K included in MTDC base; remainder excluded
# 5. Match column ≥ NOFO required match percentage
```

A 1-cent reconciliation error gets flagged in differential review.

## Examples

### Example 1: $500K, 3-year federal proposal budget narrative

**Goal:** Build SF-424A + budget narrative for a $500K HRSA grant.

**Steps:**
1. Build personnel table: PI + PM + Evaluator + Data Analyst with FTE % per year.
2. Apply org fringe rate (audited) to personnel = b.
3. Travel: GSA per-diem + coach airfare for 1 federal meeting + 6 site visits.
4. Equipment: 1 $12K item (above threshold).
5. Supplies: curriculum printing + postage + office allocable share.
6. Contractual: 2 subawards (University evaluator $85K + service partner $50K) with subaward monitoring narrative.
7. Other: rent + comms + software + printing (allocable shares).
8. Compute MTDC base (subtract equipment, subaward >$25K, rent).
9. Apply de minimis 15% MTDC.
10. Build multi-year columns with 3% escalation.
11. Reconcile to project narrative cost mentions.
12. Render to DOCX narrative + XLSX SF-424A.

**Result:** Budget narrative ready for federal scoring + reconciled SF-424A spreadsheet.

### Example 2: Foundation budget revision after decline feedback

**Goal:** Revise a declined foundation budget where reviewers said "budget unclear."

**Steps:**
1. Compare declined budget to foundation's published budget guidance.
2. Add per-line allowability + allocability + reasonableness paragraphs.
3. Add multi-year columns with explicit escalation.
4. Add match column with sources (cash + in-kind documented).
5. Reduce indirect rate if foundation caps it (many foundations cap at 10-15%).
6. Reconcile to narrative.

**Result:** Revised budget narrative resubmitted with cleaner reviewer pathway.

## Edge cases / gotchas

- **De Minimis 15% MTDC is the 2024 rate.** Old proposals citing 10% are out of date. Cite the updated 2 CFR 200.414(f).
- **NIH FY26 reverts to 45 CFR 75.** NIH may publish a separate ceiling indirect rate. Check NIH NOT-OD-26-072.
- **MTDC base exclusions:** Equipment >$10K, subaward portions >$25K, participant support, pass-through >$25K, rental, certain scholarships. Failing to exclude these inflates indirect.
- **Foundations cap indirect.** Many foundations cap at 10% or refuse indirect. Read funder budget guidance before defaulting to 15%.
- **Salary cap on federal grants.** NIH executive level II salary cap ($221,900 in 2025). Salaries above cap require split charging.
- **Participant support costs are NOT in MTDC.** Stipends, travel for research participants, registration fees for trainees. Federal forbids indirect on these.
- **Time-and-effort certification.** Personnel charged to federal must have time-and-effort records (200.430(i)) — quarterly or semi-annual.
- **Equipment threshold:** Items ≥$10K (2024 revision). Below $10K = Supplies. Subject to property management standards per 200.439.
- **Construction grants use SF-424C/D.** Different budget structure (not object class). Use the right form family.
- **Sub-recipient vs Contractor distinction.** Sub-recipient (substantive program scope, monitoring required) vs Contractor (procurement vendor, market relationship). Per 2 CFR 200.331(b).
- **Disclaimer:** Binding interpretation of cost allowability → qualified grants professional / CPA.

## Sources

- 2 CFR 200 Subpart E — Cost Principles: https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-E
- 2 CFR 200.414 — Indirect (F&A) costs (updated Oct 2024): https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-E/subject-group-ECFRd93f2a98b1f6455/section-200.414
- 2 CFR 200.439 — Equipment (updated $10K threshold Oct 2024): https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-E/subject-group-ECFR8feb4c5...../section-200.439
- 2 CFR 200.331 — Subrecipient management: https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D/section-200.331
- Clark Nuber — De Minimis 15% MTDC update: https://clarknuber.com/articles/uniform-guidance-the-de-minimis-indirect-cost-rate-updated/
- CMS Budget Request + Narrative Guidance: https://www.cms.gov/about-cms/work-us/cms-grants/cooperative-agreements/how-apply-cms-grants/cms-guidance-preparing-budget-request-and-narrative
- GSA Per-Diem Rates: https://www.gsa.gov/travel/plan-book/per-diem-rates
- OpenGrants — Budget Narrative Example: https://opengrants.io/grant-budget-narrative-example-numbers-changed/
- BLS Occupational Employment Statistics: https://www.bls.gov/oes/
