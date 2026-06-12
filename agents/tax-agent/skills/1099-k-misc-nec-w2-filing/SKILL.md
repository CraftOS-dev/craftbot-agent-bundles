<!--
Source: https://www.irs.gov/forms-pubs/about-form-1099-nec
Source: https://www.irs.gov/forms-pubs/about-form-1099-misc
Source: https://www.irs.gov/businesses/understanding-your-form-1099-k
Source: https://www.track1099.com/
Source: https://www.tax1099.com/
Source: https://www.irs.gov/forms-pubs/about-form-1042-s
Reference role.md: "1099 family + W-2 filing"
-->

# 1099-NEC / MISC / K + W-2 + 1042-S — annual contractor / employee tax filings

Annual issuance of 1099-NEC (contractor), 1099-MISC (rent, royalties, other), 1099-K (marketplace), W-2 (employee), 1042-S (foreign contractor with 30% withholding). E-file via Track1099 / Tax1099 / Gusto / Rippling / Stripe. Threshold matrix + IRIS portal + state-1099 requirements.

## When to use

- January annual 1099 issuance to contractors (1099-NEC for $600+ payments).
- 1099-MISC for rent, royalty, attorney, other payments $600+ (or $10 royalty).
- 1099-K for marketplace/payment processor payments (Stripe, PayPal, eBay).
- W-2 issuance to employees (January 31 due date).
- W-3 transmittal for W-2 totals.
- 1042-S for foreign contractor payments (30% default withholding unless W-8BEN filed).
- 1098 series (mortgage interest, student loan, tuition).
- Trigger phrases: "1099", "W-2", "1042-S", "Track1099", "Tax1099", "contractor tax", "W-9", "W-8BEN", "FATCA", "backup withholding", "IRIS portal".

NOT for: payroll tax 941/940 (use `payroll-tax-940-941-quarterly-annual`); equity comp W-2 entries (use `iso-nso-rsu-employee-tax-treatment`); foreign sub Form 5471/8865 (use `transfer-pricing-form-5471-8865-5472`).

## Setup

### Track1099 (most popular)

```bash
export TRACK1099_API_KEY="..."
curl -H "Authorization: Bearer $TRACK1099_API_KEY" \
  https://www.track1099.com/api/v2/forms
```

### Tax1099

```bash
export TAX1099_API_KEY="..."
curl -H "Authorization: Bearer $TAX1099_API_KEY" \
  https://www.tax1099.com/api/v2/forms
```

### Stripe 1099-K (auto-issued by Stripe)

```bash
# Stripe issues 1099-K to merchants who exceed threshold
# Pull 1099-K data via Stripe API
curl -u $STRIPE_API_KEY: \
  https://api.stripe.com/v1/tax/forms?type=1099-k
```

### Gusto W-2 (auto-issued)

```bash
curl -H "Authorization: Bearer $GUSTO_API_KEY" \
  https://api.gusto.com/v1/companies/{cid}/w2s?year=2025
```

### IRS IRIS (Information Returns Intake System) — direct e-file

```bash
# IRIS replaces FIRE system; direct IRS portal for 1099 e-filing
# https://www.irs.gov/filing/e-file-forms-1099-with-iris
# Requires TCC (Transmitter Control Code) — apply via IR Application
# Required if filing 10+ information returns (2024+ threshold)
```

## Threshold matrix (2026)

| Form | Trigger threshold | Notes |
|---|---|---|
| 1099-NEC | $600+ contractor payments | Box 1; mandatory if $600 paid in trade/business |
| 1099-MISC Box 1 | $600+ rent | Office, equipment, land |
| 1099-MISC Box 2 | $10+ royalty | |
| 1099-MISC Box 3 | $600+ other income | Prizes, awards, lawsuit damages |
| 1099-MISC Box 7 | $5,000+ direct seller | Consumer products to buyers for resale |
| 1099-K (2026) | $600+ payment processor (NEW LOWER, originally $20K + 200 txn) | Stripe / PayPal / Venmo / eBay |
| W-2 | Any wage payment | All employees |
| 1042-S | All US-source income to NRA | 30% default withholding unless W-8BEN |
| 1099-INT | $10+ interest | |
| 1099-DIV | $10+ dividends | |
| 1099-R | $10+ retirement distribution | |
| 1099-B | All broker transactions | |
| 1098 | $600+ mortgage interest | |
| 1098-T | All qualified tuition payments | |

## 1099-K threshold rollout (post-ARPA 2021)

- **Pre-2023:** $20,000 + 200 transactions
- **2023:** delayed (IRS Notice 2023-10)
- **2024:** $5,000 (IRS Notice 2023-74)
- **2025:** $2,500 (IRS phased)
- **2026 onward:** $600 (statutory)

Stripe / PayPal / Venmo / eBay / Etsy required to issue 1099-K above threshold. Recipients of personal payments NOT trade/business should NOT receive 1099-K but often do via processor over-issuance.

## Common recipes

### Recipe 1 — Annual 1099-NEC issuance via Track1099 (W-9 → 1099-NEC)

```python
# Step 1: collect W-9 from all paid contractors
# Step 2: pull annual payment totals from Xero + Ramp + Brex
# Step 3: filter ≥ $600 (1099-NEC required)
# Step 4: e-file via Track1099 (or Tax1099)

import requests, pandas as pd
contractor_payments = pd.read_sql("""
SELECT vendor_id, vendor_name, vendor_tin, vendor_address,
       SUM(amount) AS ytd_paid
FROM xero_payments
WHERE category = 'contractor'
  AND payment_date BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY vendor_id
HAVING SUM(amount) >= 600
""", db)

# E-file via Track1099
for _, row in contractor_payments.iterrows():
    requests.post(
        "https://www.track1099.com/api/v2/forms",
        headers={"Authorization": f"Bearer {TRACK1099_API_KEY}"},
        json={
            "form_type": "1099-NEC",
            "tax_year": 2025,
            "payer": {"ein": PAYER_EIN, "name": PAYER_NAME, "address": PAYER_ADDR},
            "recipient": {
                "tin": row.vendor_tin, "name": row.vendor_name,
                "address": row.vendor_address,
            },
            "box1_nonemployee_compensation": float(row.ytd_paid),
        }
    )
```

### Recipe 2 — W-9 collection workflow

```python
# Track1099 has free W-9 collection portal
# Auto-emails contractor; they fill in browser; cert TIN matching
# Required BEFORE first payment to avoid backup withholding
import requests
requests.post(
    "https://www.track1099.com/api/v2/w9-requests",
    headers={"Authorization": f"Bearer {TRACK1099_API_KEY}"},
    json={
        "recipient_email": "contractor@example.com",
        "recipient_name": "Jane Designer LLC",
        "due_date": "2026-01-31",
    }
)

# If W-9 not returned by first payment → backup withholding 24%
```

### Recipe 3 — TIN matching (IRS TIN Matching Program)

```bash
# IRS TIN Matching: confirm vendor TIN matches IRS records BEFORE filing
# Avoid CP2100/CP2100A "B-Notice" mismatches
# Free; e-Services portal at IRS.gov/Businesses/Small-Businesses-Self-Employed/
# Verify-EIN-and-TIN

# Via Track1099 (auto-submitted on form save)
# Via Tax1099 (same)
# Direct IRS bulk via TIN Matching Program (require e-Services account)
```

### Recipe 4 — 1099-MISC for rent / royalty / attorney payments

```python
# 1099-MISC boxes (2020+):
# Box 1: Rents ($600+)
# Box 2: Royalties ($10+)
# Box 3: Other income ($600+) — prizes, awards
# Box 4: Federal income tax withheld
# Box 5: Fishing boat proceeds
# Box 6: Medical/health care payments ($600+) — incl. corporations
# Box 7: Direct sales (consumer products) ($5,000+)
# Box 8: Substitute payments
# Box 10: Gross proceeds to attorney ($600+) — even if attorney is a corp
# Box 14: Crop insurance proceeds
# (Note: Box 7 NEC moved to 1099-NEC in 2020)
```

### Recipe 5 — 1042-S for foreign contractor (NRA)

```python
# 1042-S: foreign person receiving US-source income
# Default 30% withholding UNLESS:
#  (a) W-8BEN on file claiming treaty exemption (reduce/eliminate withholding)
#  (b) Services performed entirely outside US (not US-source)
#  (c) Independent personal services exception (Notice 2007-19 limited)

# Form W-8BEN (individual NRA): claim treaty benefits
# Form W-8BEN-E (foreign entity): same for foreign company
# Form 8233: claim personal services treaty exemption for compensation
# Form 1042 (annual employer summary): aggregate 1042-S totals
# Form 1042-T (transmittal): cover for 1042-S filings

import requests
requests.post(
    "https://www.track1099.com/api/v2/forms",
    headers={"Authorization": f"Bearer {TRACK1099_API_KEY}"},
    json={
        "form_type": "1042-S",
        "tax_year": 2025,
        "income_code": "16",  # scholarship/fellowship; "23" other
        "gross_income": 25_000,
        "withholding_allowance": 0,
        "tax_rate": 0.10,  # treaty rate per W-8BEN
        "tax_withheld": 2_500,
        "recipient_country_code": "DE",  # Germany
        "treaty_country": "Germany",
        # ...
    }
)
```

### Recipe 6 — Backup withholding (24%) when W-9 missing

```python
# Trigger conditions for backup withholding (Section 3406):
#  - Payee fails to furnish TIN
#  - IRS notifies payer that TIN is incorrect
#  - Payee fails to certify under penalty of perjury
#  - Payee subject to backup withholding from prior 1099 filing

# Apply 24% backup withholding to ALL future payments to that vendor
# Remit via Form 945 (annual non-payroll withholding) by January 31

vendor_status = check_w9_on_file(vendor_id)
if not vendor_status.has_valid_w9:
    backup_withhold = payment_amount * 0.24
    net_payment = payment_amount - backup_withhold
```

### Recipe 7 — State 1099 filing requirements

```python
# 39 states have own 1099 filing requirements (mostly mirror federal)
# Some states accept CF/SF (Combined Federal/State Filing) → IRS shares with state
# Others require direct state filing
STATE_1099_REQUIREMENTS = {
    "CA": "FTB direct file or CF/SF; threshold $600",
    "NY": "DTF direct file; threshold $600",
    "TX": "no state income tax → no 1099 filing",
    "FL": "no state income tax → no 1099 filing",
    "MA": "DOR direct file; threshold $600",
    "OR": "DOR direct file; threshold $600",
    # ... 33 more
}

# Track1099 / Tax1099 handle CF/SF + direct state filings auto
```

### Recipe 8 — Reconcile 1099-NEC totals to GL

```python
# Annual reconciliation: Track1099 issued totals → Xero "Contractor Expense" 
# account total YTD
track1099_total = sum(
    requests.get(
        "https://www.track1099.com/api/v2/forms"
        "?tax_year=2025&form_type=1099-NEC",
        headers={"Authorization": f"Bearer {TRACK1099_API_KEY}"}
    ).json()["forms"][i]["box1"]
    for i in range(...)
)
xero_contractor_total = (xero_client.reports.profit_and_loss(
    from_date="2025-01-01", to_date="2025-12-31"
).get_account("6300").amount)
diff = track1099_total - xero_contractor_total
# Should match within materiality; differences = un-issued 1099s or coding errors
```

### Recipe 9 — IRIS bulk 1099 file (10+ forms requirement)

```python
# E-filing mandatory if 10+ information returns aggregated (2024+)
# IRIS = IRS Information Returns Intake System
# Apply for TCC (Transmitter Control Code) via IR Application
# https://www.irs.gov/tax-professionals/iris-application-for-tcc

# IRIS supports:
#  - Online Web Form (manual entry, up to 100 forms)
#  - Bulk file upload (Pub 1220 schema CSV/XML)

# Track1099 / Tax1099 file via IRIS automatically
```

### Recipe 10 — Corrected 1099 issuance

```python
# Correction Type A: code "1" — correct previously filed
# Correction Type G: code "G" — void
# Mail recipient corrected copy + e-file corrected with IRS

requests.post(
    "https://www.track1099.com/api/v2/forms/corrections",
    headers={"Authorization": f"Bearer {TRACK1099_API_KEY}"},
    json={
        "original_form_id": "1099-NEC-2025-0042",
        "correction_type": "1",  # amend
        "corrected_box1": 18_500,  # was 16,500
    }
)
```

## Examples

### Example 1: SaaS startup, 22 contractors, year-end 1099-NEC

**Goal:** $312K total contractor payments, 22 contractors, year-end filing.

**Steps:**

1. November: Track1099 W-9 collection portal email sent to all contractors (Recipe 2).
2. December: confirm all W-9s in; chase 3 stragglers; apply backup withholding to 1 vendor who refused.
3. January 2: pull contractor payments from Xero + Ramp (Recipe 1).
4. January 15: review draft 1099-NECs in Track1099 dashboard.
5. January 25: e-file via Track1099 (CF/SF for state coverage).
6. January 31: paper copies mailed to recipients (Track1099 handles).
7. February: reconcile to GL (Recipe 8).

**Result:** 22 1099-NECs filed; CP2100 risk minimized by TIN matching at issuance.

### Example 2: Foreign-resident designer earning $45K, treaty country

**Goal:** German designer providing services from Germany; $45K annual.

**Steps:**

1. Collect Form W-8BEN claiming Germany-US treaty Article 14 (independent personal services).
2. Determine US-source vs foreign-source: services performed in Germany → foreign-source → NOT US-source → no withholding required, no 1042-S required.
3. Document foreign-source determination in vendor file (key risk: services performed in US, even via remote login on US server, could trip US-source).
4. Issue Form 1099 if vendor is US person (treaty does not change citizen status); not applicable here.
5. Annual review.

**Result:** No 1042-S withholding; treaty-supported documentation in vendor file.

### Example 3: Marketplace seller receiving 1099-K from Stripe

**Goal:** $12K in Stripe payments; 1099-K issued; reconcile to revenue.

**Steps:**

1. Stripe auto-issues 1099-K (over $600 threshold 2026).
2. Pull 1099-K via Stripe API (Recipe Stripe 1099-K above).
3. Reconcile 1099-K box 1a (gross payments) to GL revenue.
4. Common diff: 1099-K = gross; GL revenue = net of refunds, discounts, fees.
5. Reconcile schedule: 1099-K $12,000 − refunds $400 − Stripe fees $360 = GL revenue $11,240.

**Result:** Documented reconciliation; ready for IRS automatic matching.

## Edge cases / gotchas

- **E-file mandatory at 10+ returns (2024+):** aggregate count across ALL info return types (1099 + W-2 + 1098 + 5498). Below 10 = paper allowed.
- **1099-K issuance vs reportable income:** receiving a 1099-K doesn't make non-business payments taxable. Document personal transactions separately. Stripe / PayPal / Venmo often over-issue.
- **Payments to corporations exempt from 1099 EXCEPT:** attorney fees (Box 10 always); medical/health care (Box 6 always); fishing boat proceeds.
- **W-9 → 1099 chain breaks:** if vendor name on 1099 doesn't match SSN/EIN on W-9, IRS sends CP2100. Match W-9 carefully.
- **Backup withholding 24%:** if not collected before first payment AND vendor refuses to provide W-9, payer becomes liable for the 24% on top of paying vendor.
- **1099-NEC vs 1099-MISC confusion:** 1099-NEC (revived 2020) = non-employee compensation only. 1099-MISC = all other.
- **1042-S for ALL US-source income to NRA:** even $1 is reportable. 30% withholding default unless treaty / Form 8233 / no US-source.
- **FATCA Chapter 4 withholding:** 30% on payments to non-FATCA-compliant foreign financial institutions. W-8BEN-E for foreign entities.
- **State 1099 due dates vary:** some states earlier than federal Jan 31 (e.g., NY Feb 28).
- **W-2 vs 1099 misclassification:** IRS aggressive on misclassified contractors. Section 530 relief if good-faith reliance on industry / prior IRS / professional advice. Worker classification status set by 20-factor test → SS-8 ruling.
- **De minimis safe harbor for filing errors:** if error in amount ≤ $100 and tax withholding ≤ $25, no penalty if not requested by recipient.
- **Correction within 30 days:** half-penalty if corrected within 30 days; full penalty after.
- **CF/SF (Combined Federal/State Filing):** IRS forwards 1099s to participating states. Track1099 / Tax1099 handle. CA / NY / OR / MA still require direct state filing.
- **Stripe / Square / PayPal 1099-K backup withholding:** if their TIN matching fails, payment processor will withhold 24% until corrected.
- **W-2 reissuance (Form W-2c):** correct W-2 errors; W-3c transmittal. Reconcile to amended 941-X if wages changed.
- **Section 6722 penalties:** $310 per failure-to-furnish-recipient 2026 (indexed); $310 per failure-to-file with IRS; doubled for intentional disregard ($630).

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- IRS Form 1099-NEC: https://www.irs.gov/forms-pubs/about-form-1099-nec
- IRS Form 1099-MISC: https://www.irs.gov/forms-pubs/about-form-1099-misc
- IRS Form 1099-K: https://www.irs.gov/businesses/understanding-your-form-1099-k
- IRS Form W-2: https://www.irs.gov/forms-pubs/about-form-w-2
- IRS Form 1042-S: https://www.irs.gov/forms-pubs/about-form-1042-s
- IRS Form W-9: https://www.irs.gov/forms-pubs/about-form-w-9
- IRS Form W-8BEN: https://www.irs.gov/forms-pubs/about-form-w-8-ben
- IRS Form W-8BEN-E: https://www.irs.gov/forms-pubs/about-form-w-8-ben-e
- IRS Form 945: https://www.irs.gov/forms-pubs/about-form-945
- IRS IRIS Portal: https://www.irs.gov/filing/e-file-forms-1099-with-iris
- IRS TIN Matching Program: https://www.irs.gov/tax-professionals/taxpayer-identification-number-tin-matching
- Track1099: https://www.track1099.com/
- Tax1099: https://www.tax1099.com/
- IRS Notice 2023-74 (1099-K threshold): https://www.irs.gov/pub/irs-drop/n-23-74.pdf

## Related skills

- `payroll-tax-940-941-quarterly-annual` — W-2 + 941 reconciliation
- `iso-nso-rsu-employee-tax-treatment` — equity comp W-2 box entries
- `transfer-pricing-form-5471-8865-5472` — foreign sub intercompany
- `irs-state-dor-notice-response` — CP2100 backup withholding response
