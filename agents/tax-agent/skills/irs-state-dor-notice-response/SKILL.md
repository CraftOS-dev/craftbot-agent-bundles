<!--
Source: https://www.irs.gov/individuals/understanding-your-cp2000-notice
Source: https://www.taxpayeradvocate.irs.gov/notices/
Source: https://www.aicpa.org/topic/tax/irs-notice-response
Source: https://www.taxadmin.org/state-tax-agencies
Reference role.md: "IRS / state DOR notice response"
-->

# IRS + state DOR notice response — CP2000 / CP501 / CP504 / state notices

Map notice codes (federal CP series + state-specific) to response strategy. Common: CP2000 (underreporter inquiry); CP501 (balance due reminder); CP504 (intent to levy — urgent 30 days); CP523 (installment default); CP14 (balance due first notice). Response options: agree+pay, disagree+Form 12203, installment Form 9465, Offer in Compromise Form 656, CDP hearing. Track 30/60/90-day deadlines via `remindme`.

## When to use

- Receive IRS notice (CP series or LTR) — identify code, determine response strategy, draft response.
- State DOR notice (each state has own notice code system).
- Statutory Notice of Deficiency (90-day letter) — must petition Tax Court within 90 days.
- 30-day letter (proposed adjustment) — respond to Appeals or accept.
- Installment agreement request (when balance due unaffordable).
- Penalty abatement request (first-time abatement, reasonable cause).
- Offer in Compromise (large unaffordable balance, doubt-as-to-collectibility / doubt-as-to-liability).
- Collection Due Process (CDP) hearing request before levy.
- Trigger phrases: "CP2000", "CP501", "CP504", "CP523", "CP14", "notice of deficiency", "30-day letter", "90-day letter", "Form 12203", "Form 9465 installment", "Form 656 offer in compromise", "OIC", "CDP", "state DOR notice", "audit letter".

NOT for: actual audit conduct / IDR response (use `tax-audit-prep-response-federal-state`); state DOR sales tax-specific notice (covered here for tax notice; for filing logistics use `multistate-sales-tax-anrok-stripe-avalara`).

## Setup

### IRS notice code library

```bash
# AICPA + Tax Notes maintain comprehensive notice libraries
# https://www.aicpa.org/topic/tax/irs-notice-response
# https://www.taxnotes.com/research/federal/irs-notices-letters
# Free general: https://www.taxpayeradvocate.irs.gov/notices/
```

### Optima Tax Relief / TaxRise (managed)

```bash
# Managed services for individual / small business notice response
# https://optimataxrelief.com/
# https://www.taxrise.com/
# Cost: typically % of balance + retainer; $750-3K
```

### Drake / ProConnect / UltraTax / CCH (preparer-software native)

```bash
# All preparer software include notice response templates
# Drake Documents → Letter Library → CP2000 response
```

## Common IRS notice codes

| Code | Meaning | Response window | Action |
|---|---|---|---|
| CP14 | Balance due first notice | 21 days | Pay or request installment |
| CP501 | Balance due reminder #1 | 35 days | Pay or contact |
| CP503 | Balance due reminder #2 | 35 days | Pay or contact urgently |
| CP504 | Intent to levy | 30 days | Pay, installment, or CDP request |
| CP523 | Installment agreement default | 30 days | Cure default or reinstate |
| CP2000 | Underreporter inquiry | 30 days | Respond agree/disagree |
| CP2501 | Underreporter inquiry follow-up | 30 days | Final position |
| CP3219A | Statutory Notice of Deficiency (90-day letter) | 90 days | Petition Tax Court OR pay |
| CP90 | Intent to levy (alt format) | 30 days | Similar to CP504 |
| CP91 | SS levy notice | 30 days | Respond before levy |
| CP297 | Pre-levy notice (employer) | 30 days | Levy on wages imminent |
| CP2100 / CP2100A | Backup withholding (1099 mismatch) | 15 days | Send B-Notice to payee |
| LT11 | Final notice of intent to levy | 30 days | CDP hearing right |
| LT16 | Math error correction | 60 days | Accept or dispute |
| Letter 525 / 5067 | 30-day letter (Examination Report) | 30 days | Appeals or accept |
| Letter 3219 | 90-day letter (Notice of Deficiency) | 90 days | Tax Court or pay |
| Letter 4883C / 5071C / 5447C | Identity verification | 30 days | Verify identity |
| Letter 6173 | 1099-K underreporting | 30 days | Respond agree/disagree |

## Common state DOR notice codes

| State | Common notices | Resources |
|---|---|---|
| CA (FTB) | FTB 3950 (balance due), FTB 4925 (proposed assessment) | ftb.ca.gov |
| NY (DTF) | DTF-960 (delinquency), L-2031 (assessment) | tax.ny.gov |
| TX (Comptroller) | Form 89-224 (audit notice) | comptroller.texas.gov |
| FL (DOR) | DR-840 (assessment) | floridarevenue.com |
| MA (DOR) | Notice of Intent to Assess (NIA) | mass.gov/dor |

Each state has DOR portal with own notice library. Full list: https://www.taxadmin.org/state-tax-agencies

## Common recipes

### Recipe 1 — Decode notice + determine response strategy

```python
# Pattern-match notice code in document scan via OCR
# Use gemini-ocr-mcp on paper notice scan
notice_text = gemini_ocr.extract_text("notice.pdf")
notice_code = extract_code_pattern(notice_text)  # e.g., "CP2000"

NOTICE_PLAYBOOK = {
    "CP2000": {
        "type": "underreporter inquiry",
        "deadline_days": 30,
        "response_options": [
            "Agree + pay balance",
            "Disagree + respond with statement of position",
            "Partial agree + provide documentation for disagreed items",
        ],
        "form_to_attach": "Response form included with CP2000",
        "documentation": "1099s, W-2s, brokerage statements, schedules",
    },
    "CP504": {
        "type": "intent to levy (urgent)",
        "deadline_days": 30,
        "response_options": [
            "Pay in full",
            "Request installment agreement Form 9465",
            "Request CDP hearing Form 12153 (30 days from CP504)",
            "Submit Offer in Compromise Form 656",
            "Currently Not Collectible status (Form 53)",
        ],
    },
    "CP3219A": {  # 90-day letter
        "type": "Statutory Notice of Deficiency",
        "deadline_days": 90,
        "response_options": [
            "Petition US Tax Court (within 90 days — STATUTORY, no extension)",
            "Pay deficiency + file refund claim later",
            "Sign Form 5564 (waiver) — agree to assessment",
        ],
        "critical": "90-day SOL is STATUTORY; missed = lose Tax Court rights",
    },
    # ...
}
```

### Recipe 2 — CP2000 underreporter response

```python
# CP2000 most common notice — IRS matched 1099/W-2/brokerage to your return
# Three response modes:
#  Agree: sign + pay (or pay later)
#  Disagree: explain in writing with documentation
#  Partial: agree to some items, disagree to others

cp2000_response = {
    "form_8821": "Tax Information Authorization if CPA preparing",
    "form_2848": "Power of Attorney if practitioner representing",
    "response_letter": {
        "header": "Re: CP2000 Notice dated [DATE] for TY [YEAR]",
        "items_addressed": [
            {
                "irs_proposed_adjustment": "$3,500 unreported 1099-NEC from Acme Co",
                "your_position": "Agree — reported on Schedule C line 1, included in $X gross",
                "supporting_doc": "Schedule C extract + bank deposit detail",
            },
            {
                "irs_proposed_adjustment": "$1,800 unreported 1099-MISC from XYZ",
                "your_position": "Disagree — XYZ payment was reimbursement of expenses, not income",
                "supporting_doc": "Expense reimbursement contract + receipts",
            },
        ],
        "summary": "Net adjustment: $X tax due (or refund)",
        "signature": "Taxpayer signature under penalty of perjury",
    },
    "attachments": ["1099 copies", "Schedule C", "bank statements", "contracts"],
}
```

### Recipe 3 — CP504 levy avoidance

```python
# CP504 = imminent levy threat. Must act within 30 days.
# Five paths:
options = {
    "1_pay_in_full": "Pay via EFTPS or check w/ voucher",
    "2_installment_agreement": "Form 9465 — direct debit installment ($31/mo setup fee waived if direct deb < $50K balance + 72-month payoff)",
    "3_cdp_hearing": "Form 12153 within 30 days — pauses collection while Appeals reviews",
    "4_offer_in_compromise": "Form 656 + $205 fee + 20% deposit OR poverty waiver; takes 6-12 months",
    "5_currently_not_collectible": "Form 433-F financial statement; IRS pauses collection if no ability to pay; statute keeps running",
}
```

### Recipe 4 — Installment agreement (Form 9465)

```python
# Online Payment Agreement (OPA) for balance < $50K + 6-yr payoff
# https://www.irs.gov/payments/online-payment-agreement-application
# No form needed; instant approval if eligible

# Streamlined installment $50K-$100K: 84-month payoff
# Non-streamlined > $100K: requires Form 433-F financial disclosure

ia_request = {
    "balance_due": 45_000,
    "monthly_payment_requested": 800,
    "months_to_payoff": 56,  # ~4.7 yrs
    "direct_debit": True,    # waives $31 setup fee
    "form": "Form 9465",
    "eligibility": "Yes — < $50K + < 72 mo",
}
```

### Recipe 5 — Offer in Compromise (Form 656)

```python
# OIC types:
#  - Doubt as to Collectibility (DATC): IRS can't collect the full balance
#  - Doubt as to Liability (DATL): genuine dispute about tax owed
#  - Effective Tax Administration (ETA): exceptional circumstances

# Minimum offer calculation (DATC):
#   Net Realizable Equity in assets + (Future Income × period)
#   Period: 12 months if lump-sum offer; 24 months if 24-mo installment offer

assets = 35_000  # equity in vehicles, bank, investments
monthly_disposable_income = 425
oic_minimum_lump_sum = assets + (monthly_disposable_income * 12)  # = 40,100
oic_minimum_24mo = assets + (monthly_disposable_income * 24)       # = 45,200

# Submission:
oic_package = {
    "form_656": "Offer in Compromise application",
    "form_433_a_oic": "Individual Collection Information Statement",
    "form_433_b_oic": "Business CIS (if business OIC)",
    "user_fee": 205,  # $205 (waived for low-income)
    "initial_payment": 0.20 * oic_minimum_lump_sum,  # 20% deposit
    "documentation": "Bank statements, pay stubs, vehicle titles, etc.",
}
```

### Recipe 6 — Penalty abatement request

```python
# First-Time Abate (FTA): if 3-yr clean compliance history + filed all returns
#   Auto-grant for failure-to-file, failure-to-pay, failure-to-deposit penalties
# https://www.irs.gov/payments/penalty-relief-due-to-first-time-abate

# Reasonable Cause (RC): specific circumstances (illness, natural disaster, 
#   reliance on tax pro, etc.)
# Form 843 OR written request

fta_request = {
    "request_type": "First-Time Abate",
    "tax_year": 2024,
    "penalties_to_abate": ["Failure-to-file: $400", "Failure-to-pay: $250"],
    "clean_history_years": [2021, 2022, 2023],  # 3 yrs prior clean
    "method": "Call IRS Practitioner Line 866-860-4259 OR submit Form 843",
}
```

### Recipe 7 — Power of Attorney (Form 2848) + Form 8821

```python
# Form 2848: full authority to receive notices, represent taxpayer at IRS
# Form 8821: limited authority (Tax Information Authorization) — read-only

poa_form_2848 = {
    "taxpayer_name": "Acme Inc",
    "taxpayer_tin": "12-3456789",
    "representative": "Jane Smith CPA",
    "representative_caf": "1234-56789R",
    "tax_matters": ["Form 1120 — Tax Years 2023, 2024, 2025"],
    "acts_authorized": "All except endorse refund checks",
    "specific_uses": "Receive copies of all notices + correspondence",
}
```

### Recipe 8 — Statutory Notice of Deficiency (90-day letter) response

```python
# CP3219A or Letter 3219 = 90-day letter
# THREE response paths:
#  1. Pay deficiency + file refund claim (Form 843 / 1040X)
#  2. Petition Tax Court (within 90 DAYS — NO EXTENSION; 150 days if outside US)
#  3. Do nothing → IRS assesses + begins collection

# Petition Tax Court:
#   Filing fee $60; file electronically at https://ustaxcourt.gov/electronic_access.html
#   Small Tax Case ($50K or less): simplified procedures
#   Regular case: > $50K
#   Burden of proof on taxpayer (with exceptions Section 7491)

# 90-day clock STARTS from notice mailing date (not receipt)
# Postmark rule: petition must be POSTMARKED within 90 days

import datetime
notice_date = datetime.date(2026, 5, 12)
deadline = notice_date + datetime.timedelta(days=90)
# = 2026-08-10
```

### Recipe 9 — State DOR notice response template

```python
# State notices generally less standardized than federal
# Each state has own portal + form library

state_response_template = {
    "letter_header": (
        f"Re: [State DOR] Notice [#####] dated [DATE]\n"
        f"Taxpayer: [LEGAL NAME] / FEIN [TIN]\n"
        f"Tax type: [Income/Sales/Withholding]\n"
        f"Period: [DATE RANGE]\n"
    ),
    "body": "Position + documentation",
    "signature": "Authorized officer / representative",
    "attachments": "All supporting documentation",
    "submission_method": "Most states accept upload via state DOR portal; some require certified mail",
}
```

### Recipe 10 — 30-day Examination Report response (Letter 525)

```python
# Letter 525 / Form 4549 = Examination Report (proposed assessment)
# 30 days to respond before Statutory Notice of Deficiency issues
# Options:
#  - Agree: sign Form 870 (waiver) → assessment + payment
#  - Disagree: request Appeals via Form 4549-A protest letter
#  - Wait: IRS will issue 90-day letter → Tax Court option

protest_letter = {
    "header": "Re: Letter 525 dated [DATE] for [ENTITY] TY [YEAR]",
    "intent": "Request Appeals review of proposed adjustment",
    "facts": "Per item disputed: facts supporting position",
    "law": "IRC sections, regulations, case law supporting position",
    "argument": "Application of law to facts",
    "documentation": "Cite + attach supporting docs",
    "penalty_perjury_signature": True,
}
```

## Examples

### Example 1: Small business receives CP2000 for unreported 1099-NEC $4,800

**Goal:** S-corp received CP2000 alleging $4,800 unreported income.

**Steps:**

1. OCR notice via gemini-ocr-mcp; extract: CP2000, TY 2024, $4,800 1099-NEC from "Vendor X".
2. Search GL for Vendor X payments in TY 2024: found $4,800 received Dec 2024.
3. Cross-check Form 1120-S line 1 ordinary income: $4,800 was REPORTED but mis-coded to "Other income" on Schedule K line 10.
4. Position: Agree the income was reported, but on different line. No tax due.
5. Draft response letter (Recipe 2) explaining mapping.
6. Submit via IRS Document Upload Tool.
7. Track 60-day IRS response window via `remindme`.

**Result:** No tax due; CP2000 resolved by demonstrating income was reported elsewhere.

### Example 2: Individual receives CP504 $42,000 balance due

**Goal:** Founder received CP504 (intent to levy) for $42K balance from prior year 1040.

**Steps:**

1. Confirm balance ($42K) reasonable; verify amount via IRS Account Transcript.
2. Cannot pay in full; explore options (Recipe 3).
3. Online Payment Agreement (OPA) at irs.gov/payments — instant approval for < $50K balance + 72-month payoff.
4. Direct debit installment $585/mo for 72 months — waives setup fee.
5. Submit OPA; receive confirmation.
6. Calendar quarterly check-ins to ensure no defaults.
7. Penalty abatement request: First-Time Abate for failure-to-pay penalty ($1,400). Save $1,400 if granted.

**Result:** Installment agreement set; FTA granted; collection avoided.

### Example 3: C-corp receives 90-day letter for $185K deficiency

**Goal:** Audit disallowed R&D credit; 90-day letter issued; $185K deficiency.

**Steps:**

1. Confirm 90-day deadline (statutory; no extension).
2. Engage tax counsel + R&D credit specialist (MainStreet review).
3. Evaluate Tax Court vs pay+refund claim:
   - Tax Court: $60 filing fee; can press R&D credit substantiation; deficiency unpaid pending decision.
   - Pay + refund claim: pay $185K, file Form 1120-X amended return + Form 4549 + refund claim Form 843; if denied, sue in District Court / Court of Federal Claims.
4. Decision: Tax Court (preserve cash).
5. File petition within 90 days; small case if eligible.
6. Discovery + administrative response + Appeals attempt before trial.

**Result:** Tax Court petition timely filed; case proceeds.

## Edge cases / gotchas

- **CP2000 = NOT a bill;** it's a proposed adjustment. Must respond within 30 days (60 if outside US).
- **90-day deadline STATUTORY:** no extension; missed = lose Tax Court rights; only option becomes pay+refund-claim.
- **Postmark rule for Tax Court petition:** USPS / DHL / FedEx certified mail postmark counts; not delivery date.
- **Designated private delivery services for postmark:** specific FedEx / UPS / DHL services qualify; check Pub 17.
- **CP2100 / CP2100A:** backup withholding 1099 mismatch; respond within 15 BUSINESS days; send B-Notice to payee.
- **First-Time Abate (FTA) ONLY for failure-to-file/pay/deposit penalties.** Not accuracy-related, fraud, or others.
- **Reasonable cause penalty abatement:** narrow; document specific event (death, illness, disaster, gov shutdown, advice from tax pro who failed); strict standard.
- **OIC user fee $205 + 20% deposit:** non-refundable even if OIC rejected. Low-income waiver if < 250% of poverty line.
- **OIC requires all returns filed + current quarterly estimates:** strict prerequisite.
- **CDP hearing rights:** triggered by CP504 / LT11 / LT16 / Letter 1058. Form 12153 within 30 days; pauses collection; Appeals reviews.
- **Equivalent Hearing:** if missed 30-day CDP window, request Equivalent Hearing — Appeals review but NO court review.
- **TFRP (Trust Fund Recovery Penalty) Section 6672:** personal liability for officers on unpaid employee withholding + FICA. Form 2751 30-day to respond, then Form 4180 interview, then assessment.
- **Statute of Limitations:** 3 years from filing for IRS to assess; 10 years from assessment for collection. Various tolling events (OIC, CDP, Tax Court).
- **State DOR levy ahead of IRS:** state DORs often act faster than IRS on collection. Track state notices separately.
- **Tax Practitioner Priority Service (PPS) line:** 866-860-4259 for CPAs/EAs with valid Form 2848. Much faster than general IRS line.
- **IRS Document Upload Tool (DUT):** modern way to submit CP2000 / audit responses. Faster than fax/mail.
- **Identity verification letters (5071C / 5447C):** common; resolve via IRS ID Verify site OR phone OR in-person TAC visit.
- **Amended return Form 1040X / 1120X:** correct previously filed return; statute restart for amended items.
- **Innocent Spouse Relief Form 8857:** if joint return and one spouse not liable for understatement; strict criteria.

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- IRS Notice Library (Taxpayer Advocate Service): https://www.taxpayeradvocate.irs.gov/notices/
- IRS Understanding Your IRS Notice or Letter: https://www.irs.gov/individuals/understanding-your-irs-notice-or-letter
- IRS CP2000 Notice: https://www.irs.gov/individuals/understanding-your-cp2000-notice
- IRS CP504 Notice: https://www.irs.gov/individuals/understanding-your-cp504-notice
- IRS Online Payment Agreement: https://www.irs.gov/payments/online-payment-agreement-application
- IRS Form 9465 Installment Agreement: https://www.irs.gov/forms-pubs/about-form-9465
- IRS Form 656 Offer in Compromise: https://www.irs.gov/forms-pubs/about-form-656
- IRS Form 12153 CDP Hearing Request: https://www.irs.gov/forms-pubs/about-form-12153
- IRS Form 2848 POA: https://www.irs.gov/forms-pubs/about-form-2848
- IRS Form 8821 Tax Information Authorization: https://www.irs.gov/forms-pubs/about-form-8821
- IRS First-Time Penalty Abatement: https://www.irs.gov/payments/penalty-relief-due-to-first-time-abate
- IRS Document Upload Tool: https://www.irs.gov/help/irs-document-upload-tool
- US Tax Court e-filing: https://ustaxcourt.gov/electronic_access.html
- Federation of Tax Administrators (state DORs): https://www.taxadmin.org/state-tax-agencies
- AICPA Notice Response: https://www.aicpa.org/topic/tax/irs-notice-response

## Related skills

- `tax-audit-prep-response-federal-state` — full audit conduct
- `payroll-tax-940-941-quarterly-annual` — TFRP / 941 notices
- `1099-k-misc-nec-w2-filing` — CP2100 backup withholding notices
- `multistate-sales-tax-anrok-stripe-avalara` — state DOR sales tax notices
