---
name: single-audit-prep-federal-750k
description: Track Single Audit threshold ($1M post-Oct 2024 / $750K pre-Oct 2024), prep the Schedule of Expenditures of Federal Awards (SEFA), brief the auditor, and submit SF-SAC to fac.gov. Grant-writer side of the work; defers binding audit execution to finance-controller. Use when the user says "are we triggering Single Audit?" / "prep SEFA" / "fac.gov submission" / "single audit prep".
---

# Single Audit prep (federal $1M / $750K threshold)

A Single Audit is an entity-wide independent CPA audit triggered when cumulative federal expenditures hit the threshold in a fiscal year ($1M for awards issued on/after Oct 1, 2024; $750K for awards issued before). Grant writer responsibilities: track the threshold, prep the SEFA, brief the auditor on each award, respond to programmatic findings. The actual audit execution and audit opinion stay with `finance-controller` + the independent CPA firm.

Disclaimer: Single Audit is a legally required compliance audit. Audit opinions, finding determinations, and SF-SAC certification are the independent CPA firm's responsibility under AICPA standards. For binding decisions, consult your CPA + qualified grants professional.

## When to use

- Cumulative federal expenditures in FY approaching threshold
- First Single Audit (first time triggering)
- Multi-year grants straddling Oct 1, 2024 (dual-threshold scenario)
- Auditor onboarding for upcoming Single Audit
- Responding to programmatic finding (post-audit)
- SF-SAC submission to fac.gov
- Sub-recipient monitoring around Single Audit threshold

Do NOT use this skill for:
- Audit execution + opinion (→ `finance-controller` + CPA firm)
- General federal compliance → `federal-grant-compliance-omb-uniform-guidance`
- Indirect rate audit defense → `indirect-cost-nicra`
- Final SF-425 reporting → `grant-reporting-interim-final`

## Setup

```bash
# Tools: xero-mcp / xlsx (SEFA prep), cli-anything (fac.gov submission), docx (auditor briefing)

# Federal Audit Clearinghouse
# Submission portal: https://www.fac.gov/

# Reference (free)
# 2 CFR 200 Subpart F — Audit Requirements
# https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-F

# OMB Compliance Supplement (annual)
# Most recent: https://www.whitehouse.gov/omb/circulars/
```

Auth / API key requirements: fac.gov account for SF-SAC submission. Independent CPA firm AICPA license verified.

## Common recipes

### Recipe 1: Threshold decision tree

```markdown
## Are we triggering Single Audit?

Step 1: Cumulative federal expenditures in current FY?
├── < $750K → No Single Audit (regardless of award date)
├── $750K - $1M → DEPENDS on award issuance dates:
│   - All awards issued BEFORE Oct 1, 2024 → Single Audit required ($750K threshold applies)
│   - All awards issued ON/AFTER Oct 1, 2024 → No Single Audit (raised threshold)
│   - MIXED awards → Apply BOTH thresholds; conservative path = audit if either triggered
└── ≥ $1M → Single Audit required regardless of award date

## Federal expenditures =
- Federal cash + non-cash assistance EXPENDED during FY
- NOT awarded; expended
- Includes pass-through from states / other federal recipients
- Excludes program income (with exceptions per 200.502)
```

### Recipe 2: Schedule of Expenditures of Federal Awards (SEFA)

```markdown
## SEFA format (typical)

| CFDA / ALN | Federal program name | Pass-through entity (if applicable) | Pass-through ID | Award $ | Expended (current FY) $ | Sub-awards (passed through to others) $ |
|---|---|---|---|---|---|---|
| 93.110 | Maternal & Child Health Block Grant | (Direct) | | 300,000 | 87,500 | 25,000 |
| 93.092 | Personal Responsibility Education | State DOH | DOH-2024-PREP-001 | 150,000 | 50,000 | 0 |
| 14.218 | Community Development Block Grant | (Direct) | | 250,000 | 100,000 | 0 |
| (etc) | | | | | | |

Total Federal Expenditures: $XXX

Notes to SEFA:
1. Basis of accounting (accrual or modified cash)
2. Indirect cost rate elected (de minimis 15% MTDC OR NICRA rate)
3. Subaward methodology (if pass-through)
4. Loan / loan guarantee disclosures (if any)
5. Federal share vs match share
```

### Recipe 3: Build SEFA from accounting system

```bash
# Pull federal-fund expenditures from Xero / QuickBooks
# Map each federal grant to a unique tracking code in chart of accounts

# Example Xero export (via xero-mcp)
# Get journal entries tagged with federal grant codes

curl -X GET "https://api.xero.com/api.xro/2.0/Reports/ProfitAndLoss?\
fromDate=2025-07-01&toDate=2026-06-30&\
trackingCategoryID=<federal_funds_tracking_id>" \
  -H "Authorization: Bearer $XERO_TOKEN"

# Aggregate by CFDA / ALN; export to xlsx
# Reconcile to SF-425 quarterly reports to the dollar
```

### Recipe 4: Major vs non-major program determination

```markdown
## Auditor's risk-based approach (Type A/B + Type A high-risk)

Type A program threshold (per 200.518):
- $0-$3.5M total federal awards: Type A = ≥ $750K
- $3.5M-$10M: Type A = ≥ $750K (lookback) or $300K (if smaller)
- $10M-$100M: Type A = 3% of total federal awards (min $1M)
- $100M-$1B: Type A = 0.30% × total
- $1B+: Type A = 0.15% × total

Type A high-risk if (any of):
- Prior audit had findings
- Significant changes in personnel, systems, prior audit
- Federal agency special concerns

Type B programs assessed as low-risk by default; auditor selects a subset using "Type B risk assessment" criteria.

## Major programs = Type A + selected Type B = at least 40% of federal expenditures audited
```

### Recipe 5: Audit timeline

```markdown
## Single Audit calendar (FY ending June 30 example)

| Month | Milestone |
|---|---|
| Jul (FY-end) | Close books; finalize federal expenditures |
| Aug | SEFA draft; CPA RFP if changing firms |
| Sep | Auditor engagement letter signed |
| Oct-Nov | Auditor fieldwork |
| Dec-Jan | Draft audit report + findings (if any) |
| Feb | Final audit report issued |
| Mar | SF-SAC submitted to fac.gov |
| Mar 31 (9 mo after FY-end) | Submission deadline |

## Single Audit Act due date: 9 months after FY-end
- FY ending Dec 31 → due Sep 30
- FY ending Jun 30 → due Mar 31
- Late submission = ineligibility for new federal awards
```

### Recipe 6: Auditor briefing memo (per award)

```markdown
## Briefing memo template

For each federal award:
1. Award name + agency + CFDA + period of performance
2. NOFO + scoring rubric (so auditor sees programmatic objectives)
3. Award terms (budget, match, reporting cadence)
4. Spending status (current expenditures vs budget)
5. Match status (cash + in-kind)
6. Sub-recipients (per 2 CFR 200.331)
7. Allowable cost basis (cost principles applied)
8. Indirect rate election + computation
9. Prior audit findings (if any) + corrective actions
10. Active grants on issue / pending modifications

## Why this matters
Briefing memo reduces auditor learning curve = faster fieldwork = lower fees + fewer findings.
```

### Recipe 7: Common findings + how to prevent

```markdown
## Top Single Audit findings (sector pattern)

| Finding | Root cause | Prevention |
|---|---|---|
| Inadequate sub-recipient monitoring | No risk assessment; no monitoring plan | `sf-424-sf-lll-subaward` Recipe 7 |
| Time + activity reporting weakness | Personnel split-funded without time studies | Quarterly time studies per 200.430(i) |
| Unallowable costs | Lobbying / alcohol / entertainment charged | Cost-principle training; pre-spend review |
| Indirect rate misapplication | Wrong base (TDC vs MTDC); wrong rate | `indirect-cost-nicra` Recipe 2 |
| FFATA reporting gaps | Sub-awards > $30K not reported | Automate FFATA report on subaward execution |
| Match documentation missing | Volunteer hours without log; donor letter missing | `matching-funds-in-kind-strategy` Recipe 6 |
| Drawdown / cash management | Holding fed cash > 3 days unspent | Just-in-time drawdown policy |
| Procurement non-compliance | No bids on contracts > $250K | Procurement policy + bid documentation |
| Equipment tracking | No inventory + no physical verification | Annual equipment inventory |
| Program income | Not reported on SF-425 line 10l | Program income tracking in GL |
```

### Recipe 8: SF-SAC submission to fac.gov

```markdown
## Submission flow

1. CPA finalizes audit; issues opinion + findings (if any)
2. Recipient prepares SF-SAC data:
   - Part I: General Information (recipient name, EIN, auditor)
   - Part II: Audit Findings (yes/no per finding category)
   - Part III: Federal Awards (SEFA data)
   - Part IV: Findings detail (if any)
3. Recipient certifies via electronic signature at fac.gov
4. CPA certifies via electronic signature at fac.gov
5. PDF of audit report uploaded as single PDF
6. Submission complete; receipt + audit number issued

## fac.gov account
- Recipient role: federal awardee
- Auditor role: CPA firm (must be registered)
- Public-facing data: SEFA + findings (PII / certain details redacted)
```

### Recipe 9: Corrective action plan (post-finding)

```markdown
## Findings response

If finding issued:
1. Acknowledge + don't dispute (admit to expedite remediation OR formally challenge with evidence)
2. Document corrective action plan:
   - Finding description
   - Root cause (be honest)
   - Corrective actions (specific + measurable)
   - Owner + due date
   - Evidence of correction (policy update, training, system change)
3. Submit corrective action plan with audit report (Part IV of SF-SAC)
4. Auditor verifies in next year's fieldwork
5. Federal agency may issue "management decision" within 6 months of audit submission

## Repeat findings
A repeat finding = 2 consecutive years = severe red flag = potential funding pause
```

### Recipe 10: Dual-threshold scenario tracking

```markdown
## Multi-year grants straddling Oct 1, 2024

Example: 5-year grant awarded Aug 2023; $300K/yr → $1.5M total
- FY2024 expenditure (pre-Oct 1, 2024 award) → $750K threshold applies
- FY2025 expenditure (same award; pre-Oct 1, 2024 issuance) → $750K threshold applies
- New 2-yr grant Aug 2024 ($600K) → $1M threshold applies

## Conservative path (recommended)
Apply LOWER threshold ($750K) if ANY pre-Oct 1, 2024 federal expenditures present.
Reduces audit risk; small cost increase if borderline.

## Aggressive path (with CPA sign-off)
Track by award; apply correct threshold per award. Document methodology in SEFA notes.
```

## Examples

### Example 1: First Single Audit — FY ending June 30, 2026, $1.2M federal expenditures

**Goal:** Compliant Single Audit, on-time submission.

**Steps:**
1. Recipe 1: cumulative $1.2M; all awards post-Oct 2024 → $1M threshold applied → Single Audit required.
2. Aug: RFP three CPA firms with Single Audit experience; engage best fit.
3. Aug: Recipe 2 SEFA draft from Xero (Recipe 3); reconcile to SF-425s.
4. Sep: Auditor engagement letter signed; engagement begins.
5. Recipe 6: briefing memo for each of 4 federal awards.
6. Oct-Nov: auditor fieldwork; respond to PBC requests.
7. Dec-Jan: draft audit report; review with `finance-controller`.
8. Feb: final report issued; one minor finding (sub-recipient monitoring documentation).
9. Recipe 9: corrective action plan drafted (quarterly site visits; documented).
10. Mar: SF-SAC submitted to fac.gov; receipt logged.

**Result:** Compliant Single Audit; one minor finding remediated; ready for next year's audit baseline.

### Example 2: Dual-threshold scenario for org with mixed-date awards

**Goal:** Determine threshold for FY26.

**Steps:**
1. Pull all federal awards: 2 awards pre-Oct 2024, 3 awards post-Oct 2024.
2. Current FY federal expenditures: $850K total ($400K from pre-Oct awards, $450K from post-Oct).
3. Recipe 1 analysis: pre-Oct expenditures $400K < $750K; post-Oct $450K < $1M.
4. BUT cumulative $850K → conservative path = audit triggered ($750K threshold applied to whole).
5. Document determination methodology in SEFA notes.
6. Engage CPA for Single Audit.

**Result:** Audit done conservatively; CPA validates methodology; no agency dispute.

## Edge cases / gotchas

- **Threshold is on EXPENDITURES, not awards.** $5M award with $400K expended in FY = $400K toward threshold, not $5M.
- **Federal pass-through counts.** Funds received via state pass-through count as federal expenditures for Single Audit.
- **Cooperative agreements count.** Cooperative agreements (NIH, CDC) are federal awards for Single Audit purposes.
- **Loan + loan guarantees.** Federal loans / loan guarantees have separate treatment per 200.502; consult auditor.
- **Program income.** Generally counted; specific exceptions per 200.502.
- **Fiscal year alignment.** Single Audit FY = recipient's FY (not federal FY). Some orgs change FY to align with federal.
- **Auditor independence.** CPA cannot also do your bookkeeping (independence violation). Many small orgs run into this; need separate bookkeeping vs audit relationships.
- **Repeat findings = serious.** 2 consecutive years = agency may pause funding pending remediation.
- **Sub-recipient pass-through.** If you pass through to subs, you're responsible for their compliance. Sub's failure = your finding.
- **Late submission penalty.** Missing 9-month deadline = ineligibility for new federal awards until current. Not an extension-eligible deadline.
- **Audit fee benchmarking.** Single Audit typically adds $5K-$30K above standard financial audit fee.
- **Disclaimer.** Single Audit is independent CPA territory. Grant writer prepares + supports; CPA executes + opines + certifies. Binding decisions through CPA + `finance-controller`.

## Sources

- 2 CFR 200 Subpart F (Audit Requirements): https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-F
- Federal Audit Clearinghouse: https://www.fac.gov/
- FAC Audit Submission Guide: https://www.fac.gov/audit-resources/submission-guide/about/
- OMB Compliance Supplement (annual): https://www.whitehouse.gov/omb/circulars/
- AICPA Government Auditing Standards: https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-government
- Council of Nonprofits — Federal Audit Requirements: https://www.councilofnonprofits.org/running-nonprofit/nonprofit-audit-guidec/federal-law-audit-requirements
- Granted AI — Single Audit threshold 2026 strategy: https://grantedai.com/blog/single-audit-threshold-1-million-nonprofit-compliance-uniform-guidance-strategy-2026
- HBKCPA — First-time Single Audit: https://hbkcpa.com/insights/first-time-single-audit-nonprofit-federal-funding/
