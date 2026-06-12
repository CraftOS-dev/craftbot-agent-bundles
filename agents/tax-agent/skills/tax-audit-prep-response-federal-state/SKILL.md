<!--
Source: https://www.irs.gov/businesses/small-businesses-self-employed/irs-audits
Source: https://www.aicpa.org/topic/tax/irs-examination-defense
Source: https://www.irs.gov/forms-pubs/about-form-4549
Source: https://www.irs.gov/forms-pubs/about-form-12203
Source: https://www.irs.gov/forms-pubs/about-form-8275
Source: https://www.taxpayeradvocate.irs.gov/notices/
Reference role.md: "Audit prep playbook" — substantiation library + IRS audit timeline + 30/90-day letter
-->

# Tax audit prep + response — federal + state

Pre-build a contemporaneous substantiation library (PBC-style — prepared by client) so audits don't blow up. When notice arrives: respond IDR (Information Document Request) within 30 days, escalate to Appeals via Form 12203 on 30-day letter, file Tax Court petition on 90-day letter (Statutory Notice of Deficiency). Coverage: federal IRS + state DOR audits. Tools: Caseware audit binder; Bloomberg Tax Audit Workpaper; Defense Tax Partners managed defense.

## When to use

- Audit notice received (IRS or state DOR) — first 30 days are critical.
- Pre-audit substantiation library setup — quarterly cadence (highest ROI).
- IDR (Information Document Request) response preparation.
- 30-day letter (proposed adjustments) — decision to accept, protest, or escalate to Appeals.
- 90-day letter / Statutory Notice of Deficiency — file Tax Court petition or default to assessment.
- Form 8275 / 8275-R disclosure when taking a contrary position pre-filing.
- Trigger phrases: "got a CP2000", "IRS audit notice", "IDR response", "Letter 2205", "30-day letter", "Form 4549", "Statutory Notice of Deficiency", "Tax Court", "Appeals protest", "Form 12203", "Form 8275 disclosure".

NOT for: routine CP2000 underreporter notices (use `irs-state-dor-notice-response` for that simpler flow); collection actions (CP504, intent to levy — separate workflow); audit-related transfer pricing defense (use `transfer-pricing-form-5471-8865-5472`).

## Setup

### Caseware + AdvanceFlow — audit binder + workpaper

```bash
# Caseware Cloud
export CASEWARE_API_KEY="..."
curl -H "Authorization: Bearer $CASEWARE_API_KEY" \
  https://api.caseware.com/v1/files
# Standard binder template: leadsheets, tickmarks, workpaper index
```

### Bloomberg Tax Audit Workpaper / IRS Practice & Procedure

```bash
# Bloomberg subscription; no public API
# Access via https://pro.bloombergtax.com/
```

### Defense Tax Partners — managed defense (referral)

```bash
# https://defensetax.com/ — referral; no API
```

### File-organizer + google-drive (PBC library)

```bash
# Build substantiation library structure:
# /tax-substantiation/
#   /2024/, /2025/, /2026/
#     /contracts/
#     /invoices-ar/
#     /invoices-ap/
#     /payroll-registers/
#     /equity-grants/
#     /rd-project-logs/
#     /transfer-pricing/
#     /mileage-logs/
#     /receipts/
```

### TaxAct Power-of-Attorney (Form 2848) prep

```bash
# Required to represent recipient before IRS
# Form 2848 specifies tax years + tax types covered
```

## Common recipes

### Recipe 1 — IRS audit timeline + critical deadlines

```python
from datetime import date, timedelta

notice_date = date(2026, 4, 15)
# IRS audit phases:
phases = {
    "L2205 Notice of Audit":             notice_date,
    "Opening interview (within 30 days)": notice_date + timedelta(days=21),
    "IDR response deadline":             notice_date + timedelta(days=30),
    "Examiner review":                   notice_date + timedelta(days=120),
    "Form 4549 (30-day letter) proposed": notice_date + timedelta(days=180),
    "30-day protest deadline (Form 12203)": notice_date + timedelta(days=210),
    "Appeals conference":                notice_date + timedelta(days=300),
    "L3219 (90-day SND)":                notice_date + timedelta(days=400),
    "Tax Court petition deadline":       notice_date + timedelta(days=490),  # 90 day from SND
}
for phase, dt in phases.items():
    print(f"{dt}: {phase}")
```

### Recipe 2 — Substantiation library structure (proactive)

```python
# Build BEFORE audit; refresh quarterly
# Each tax position needs contemporaneous documentation

substantiation_categories = {
    "deferred_revenue_waterfall": {
        "source": "xero-mcp / postgresql-mcp",
        "evidence": "contract, invoice, ASC 606 schedule",
        "audit_risk": "ASC 606 income recognition + book-tax timing",
    },
    "rd_credit_qres": {
        "source": "Gusto + project-level time tracking",
        "evidence": "project description, technological-uncertainty memo, 4-part-test memo",
        "audit_risk": "IRS Tier 1 — full project-level review",
    },
    "equity_grants_83b": {
        "source": "Carta / Pulley",
        "evidence": "grant agreement, 83(b) IRS certified mail receipt",
        "audit_risk": "compensation timing + AMT preference reversal",
    },
    "transfer_pricing": {
        "source": "intercompany agreements + benchmark study",
        "evidence": "Master File, Local File, comparables, FAR analysis",
        "audit_risk": "Section 482 transfer-pricing adjustment + penalty",
    },
    "section_174_capitalization": {
        "source": "xero-mcp + Treas Reg 1.174-2 allocation",
        "evidence": "domestic vs foreign R&D allocation memo",
        "audit_risk": "Section 174 mis-categorization",
    },
    "mileage_listed_property": {
        "source": "MileIQ / Everlance / manual log",
        "evidence": "contemporaneous mileage log (Section 274(d))",
        "audit_risk": "vehicle deduction disallowance",
    },
}
```

### Recipe 3 — IDR (Information Document Request) response

```python
# IDR format: numbered list of document requests with deadline
# Response must be COMPLETE + TIMELY (30 days standard)
# Late / incomplete → summons risk + adverse inference

idr_response_checklist = [
    "Read each IDR item carefully — ambiguous = clarify in writing FIRST",
    "Identify documents in substantiation library (Recipe 2)",
    "Bates-number each document for response",
    "Build response index (item # → bates range)",
    "Privilege review: attorney-client, work-product",
    "Submit via secure portal (IDR.gov) or hand-delivery — never email IRS",
    "Retain copy of response + IDR + delivery confirmation",
    "Track open IDRs vs resolved",
]

# Privilege protection
# Section 7525 federally authorized tax practitioner privilege — limited
# Attorney-client = strongest. Engage tax attorney if novel issues.
```

### Recipe 4 — 30-day letter (Form 4549) protest

```python
# Form 4549 = proposed adjustments
# 30 days to:
# (a) AGREE — sign + pay; or
# (b) PROTEST → Office of Appeals (small case < $25K = informal; large case = formal Form 12203)

# Formal protest content (per IRS Pub 5):
# 1. Recipient name + address + EIN + phone
# 2. Statement: "Request administrative consideration by Office of Appeals"
# 3. Date + symbols + items from 30-day letter being protested
# 4. Tax periods involved
# 5. Statement of findings being contested
# 6. Statement of facts (sworn under penalty of perjury)
# 7. Statement of law + authorities
# 8. Statement of position
# 9. Signature

# File via mail (certified) to address in 30-day letter
# Submit Form 2848 with protest if represented
```

### Recipe 5 — 90-day Statutory Notice of Deficiency (SND, Letter 3219)

```python
# SND issued when 30-day window expires + no agreement / protest
# OR Appeals doesn't resolve
# 90 DAYS (150 if outside US) to:
# (a) Pay assessed deficiency; or
# (b) File petition in US Tax Court (no payment required)

# DEFAULT after 90 days = assessment + collection (CP504 etc.)
# Tax Court is the ONLY forum to litigate WITHOUT paying first

snd_window = 90  # days
# Court petition options:
# 1. US Tax Court — no prepayment, jury trial NOT available
# 2. US District Court — must pay + refund claim first
# 3. US Court of Federal Claims — same as district + jurisdiction limits

# Tax Court petition form (T.C. Form 2) + filing fee $60
# Available e-filing via DAWSON: https://dawson.ustaxcourt.gov/
```

### Recipe 6 — Form 8275 / 8275-R disclosure (pre-filing)

```python
# File WITH return when taking position contrary to clear guidance
# Form 8275: position contrary to "substantial authority" but disclosed
# Form 8275-R: position contrary to specific Treas Reg

# Avoids substantial-understatement penalty (Section 6662 — 20% understatement)
# REQUIRED if taking realistic-possibility-of-success but not substantial-authority

# Form 8275 content:
# - Schedule of items being disclosed
# - Detailed description of each item
# - Citation of authority (or lack of)
# - Adequate disclosure standard met

# Common 8275 / 8275-R triggers:
# - R&D credit aggressive QRE allocation
# - Section 199A SSTB borderline classification
# - Bad debt deduction timing (Section 166)
# - Reasonable comp S-corp distribution
```

### Recipe 7 — Audit-period extension via Form 872

```python
# Statute of limitations: 3 years from filing (Section 6501)
# Extends to 6 years if > 25% gross income omitted
# UNLIMITED if fraud OR no return filed

# IRS may request EXTENSION via Form 872 (Consent to Extend Time to Assess Tax)
# Considerations:
# - Refusing = forces IRS to assess on what they have (often disadvantageous)
# - Agreeing = gives IRS more time but typically more flexible negotiations
# - Restricted Form 872-A: open-ended; either party may terminate with 90 days notice
# - Limit by SPECIFIC ISSUES (not blanket) if possible

# Decision rule: usually agree to LIMITED extension when negotiating; refuse blanket
```

### Recipe 8 — State DOR audit response

```python
# State DOR audits parallel federal but with KEY DIFFERENCES:

state_audit_specifics = {
    "CA FTB": {
        "lookback": "4 years (Section 19057 CA RTC)",
        "appeals": "Office of Tax Appeals (OTA) — Form OTA-1",
        "tax_court_equivalent": "Superior Court (post-OTA)",
        "deadline_to_protest": "60 days from Notice of Action",
    },
    "NY DTF": {
        "lookback": "3 years",
        "appeals": "Bureau of Conciliation + Mediation Services → Tax Appeals Tribunal",
        "deadline_to_petition": "90 days from notice",
    },
    "TX Comptroller": {
        "lookback": "4 years",
        "appeals": "Comptroller Hearings → State Office of Administrative Hearings",
        "deadline_to_protest": "60 days from deficiency",
    },
    "MA DOR": {
        "lookback": "3 years",
        "appeals": "Appellate Tax Board (ATB)",
        "deadline_to_petition": "60 days from NOA",
    },
}

# Multi-state audit coordination: state may piggyback on IRS findings (RAR — Revenue Agent Report)
# Federal RAR triggers state amended return obligation in most states (30-180 days)
```

### Recipe 9 — Audit-ready workpaper index (Caseware structure)

```python
# Standard tax audit binder structure (Caseware / AdvanceFlow):
binder_index = {
    "100": "General — engagement letter, organization, prior-year returns",
    "200": "Income — sales, services, interest, dividends, gain/loss",
    "300": "Cost of sales — inventory, COGS schedule",
    "400": "Operating expenses — depreciation, amortization, payroll, rent",
    "500": "Other deductions — interest, charitable, R&D, taxes",
    "600": "Schedules — M-1, M-3, L, K",
    "700": "Tax payments — quarterly estimates, withholding",
    "800": "Credits — R&D, foreign tax, energy",
    "900": "International — 5471, 8865, 5472, transfer pricing",
    "1000": "State + local — apportionment, throwback, PTET",
    "1100": "Equity comp — Carta export, 3921, 3922",
    "1200": "Substantiation — receipts, mileage logs, contracts",
}
```

### Recipe 10 — Privilege protection during audit

```python
# Communication classification:
# - Attorney-client privilege (strongest)
# - Section 7525 tax-practitioner privilege (CPA — FEDERAL ONLY; not state)
# - Kovel arrangement: CPA engaged THROUGH attorney → attorney-client extends to CPA
# - Work-product doctrine: documents prepared in anticipation of litigation

privilege_decision_tree = {
    "novel_aggressive_position": "Kovel arrangement: engage tax attorney → CPA via attorney",
    "routine_compliance": "Section 7525 protects CPA-prepared advice (federal)",
    "expected_state_audit": "Engage attorney (Section 7525 doesn't cover state)",
    "criminal_referral_risk": "ENGAGE TAX ATTORNEY IMMEDIATELY",
}
```

## Examples

### Example 1: Field audit notice for $42M revenue C-corp

**Goal:** L2205 Notice received for tax year 2024 Form 1120 (filed Q3 2025). Field audit assigned to IRS LB&I division.

**Steps:**
1. Recipe 1 timeline: response deadlines mapped; opening interview scheduled 21 days out.
2. Execute Form 2848 POA for CPA + tax attorney representation.
3. Recipe 2 substantiation library — pull 2024 R&D credit workpapers, transfer pricing study, M-1 reconciliation, deferred revenue waterfall.
4. Recipe 3 IDR pre-staging: anticipate likely IDR items (R&D Tier 1 issue, M-3 reconciliation, state apportionment).
5. Recipe 7 statute extension: limit to specific issues if requested.
6. Recipe 10 privilege: Kovel arrangement for R&D Section 174 aggressive allocation memo.
7. Quarterly Appeals readiness review during exam.

**Result:** IDR responses ready Day 30; substantiation library cross-indexed; defense team formed; client briefed on possible exposure.

### Example 2: 30-day letter protest to Appeals

**Goal:** Form 4549 received proposing $185K adjustment. Issues: $96K R&D credit disallowance + $54K bad debt timing + $35K travel & meals disallowed (substantiation).

**Steps:**
1. Recipe 4 formal protest drafted within 30 days:
   - R&D issue: cite Section 41 four-part test memo + project-level QRE allocation evidence.
   - Bad debt: Section 166 specific-charge-off vs reserve method — taxpayer used proper specific-charge-off; provide debtor list + collection efforts log.
   - T&E: produce mileage logs + restaurant receipts + business-purpose notes; concede $8K unsubstantiated portion.
2. Form 12203 attached + supporting docs bates-numbered.
3. Submit to Appeals office address on 30-day letter.
4. Appeals officer conference scheduled within 90-120 days.
5. Settlement framework: hazards-of-litigation valuation per Appeals manual.

**Result:** Appeals settlement at $42K total (vs original $185K proposed) — 77% reduction. No Tax Court litigation needed.

### Example 3: State DOR audit (CA FTB) post-federal RAR

**Goal:** Federal audit concluded with $73K adjustment. CA FTB issued parallel audit notice 60 days later citing RAR adjustment.

**Steps:**
1. Recipe 8 CA FTB process: 60-day protest window from Notice of Action.
2. Compute CA-apportionment impact: $73K federal adjustment × 22% CA apportionment = $16K state taxable income increase.
3. CA additional tax: $16K * 8.84% = ~$1,415.
4. Compare federal Appeals settlement: if federal reduced, request CA conformity reduction.
5. File CA protest if FTB doesn't auto-conform federal Appeals result.
6. If Office of Tax Appeals (OTA) needed: Form OTA-1 within 30 days of FTB protest denial.

**Result:** CA assessment reduced to $312 by matching federal Appeals reduction; no OTA petition needed.

## Edge cases / gotchas

- **IDR response timing is firm:** late = IRS may issue summons (Section 7602). Summons enforceable in district court → criminal contempt risk.
- **Section 7525 CPA privilege does NOT apply:** (a) before state DOR; (b) in criminal proceedings; (c) for tax-shelter promotion. Engage attorney.
- **Statute of limitations 3 yrs (Section 6501) extends to 6 yrs** if > 25% gross income omitted (Section 6501(e)). UNLIMITED if fraud or no return filed.
- **Form 872 (statute extension) refusal isn't always wrong** — forces IRS to assess on incomplete info. Some practitioners use as leverage.
- **Tax Court 90-day deadline is JURISDICTIONAL** — even one day late = case dismissed + forced to pay-then-refund litigation in district court.
- **No "burden of proof" reversal** if substantiation not produced — taxpayer bears burden (Section 7491 limited exception).
- **Section 6662 accuracy-related penalty (20%)** stacks with assessment. Avoid via Form 8275 disclosure OR reasonable-cause exception (Section 6664(c)).
- **Section 6663 civil fraud penalty (75%)** — IRS bears burden of clear-and-convincing evidence; criminal referral possible (Section 7201).
- **State conformity to federal RAR varies:** most states require amended return within 30-180 days of federal final determination. Failure = penalty + extended state SOL.
- **CP2000 underreporter notice** is NOT an audit — it's a computerized match. Response is FORM-based (response form attached); 30-day window. Far simpler than examination audit.
- **TFRP (Trust Fund Recovery Penalty, Section 6672)** — personal liability of responsible person for unpaid payroll trust fund taxes. 100% penalty. Separate appeals (Letter 1153 → Form 8848 protest).
- **Voluntary Disclosure Program** (criminal-risk situations) — IRS Criminal Investigation Division pre-clearance. NEVER attempt without attorney.
- **Field vs office vs correspondence audit** scope differs hugely:
  - Correspondence: single-issue, mail-based
  - Office: in-person at IRS office; multi-issue
  - Field: at recipient's place of business; comprehensive (LB&I division for large corps)

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- IRS Audits overview: https://www.irs.gov/businesses/small-businesses-self-employed/irs-audits
- AICPA IRS Examination Defense: https://www.aicpa.org/topic/tax/irs-examination-defense
- IRS Pub 1 (Your Rights as a Taxpayer): https://www.irs.gov/forms-pubs/about-publication-1
- IRS Pub 5 (Your Appeal Rights): https://www.irs.gov/forms-pubs/about-publication-5
- IRS Pub 556 (Examination of Returns + Appeal Rights): https://www.irs.gov/forms-pubs/about-publication-556
- IRS Form 4549 (Examination Report): https://www.irs.gov/forms-pubs/about-form-4549
- IRS Form 12203 (Request for Appeals Review): https://www.irs.gov/forms-pubs/about-form-12203
- IRS Form 8275 (Disclosure Statement): https://www.irs.gov/forms-pubs/about-form-8275
- IRS Form 872 (Consent to Extend Time): https://www.irs.gov/forms-pubs/about-form-872
- US Tax Court DAWSON e-filing: https://dawson.ustaxcourt.gov/
- Taxpayer Advocate notices: https://www.taxpayeradvocate.irs.gov/notices/
- CA FTB audit + appeals: https://www.ftb.ca.gov/help/contact/audits.html
- NY DTF audit + appeals: https://www.tax.ny.gov/enforcement/audit/
- Caseware: https://www.caseware.com/
- AdvanceFlow: https://tax.thomsonreuters.com/en/cs-professional-suite/advanceflow

## Related skills

- `irs-state-dor-notice-response` — routine non-audit notices (CP2000 etc.)
- `transfer-pricing-form-5471-8865-5472` — TP audit defense
- `rd-tax-credit-form-6765-mainstreet-neo` — R&D credit Tier 1 issue substantiation
- `sec-174-rd-capitalization` — Section 174 audit-risk allocation defense
- `state-apportionment-nexus-analysis` — state DOR audit coordination
- `form-1120-corp-income-tax-filing` — workpaper backup tying to return
