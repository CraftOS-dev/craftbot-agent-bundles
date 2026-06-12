<!--
Source: https://www.dwt.com/blogs/startup-law-blog/2025/07/qsbs-big-beautiful-bill-tax-code-upgrades
Source: https://kruzeconsulting.com/blog/big-beautiful-bill/
Source: https://dashboard.mainstreet.com/welcome/guideline
Source: https://carta.com/learn/startups/tax-planning/qsbs/
Reference role.md: "Tax strategy playbook"
-->

# Tax strategy — QSBS (Big Beautiful Bill 2025) + R&D credit + holdco

The strategic-finance tax stack: (1) QSBS Section 1202 — Big Beautiful Bill 2025 expanded benefit, (2) R&D credit (Sec 41 + QSB payroll-tax election), (3) holding company structures for IP / international / M&A. 2026 SOTA platforms: MainStreet (auto-claim R&D + cash advance), Neo.tax, Haven, Pilot R&D module, Shay CPA, Kruze Consulting, Burkland.

## When to use

- Pre-IPO / pre-exit QSBS planning (5-year holding requirement triggers).
- Annual R&D credit claim cycle (Q1 prior-year, Q3 current-year estimation).
- Holdco structure decision (pre-international, pre-M&A, pre-IP transfer).
- Equity issuance with QSBS implications.
- Trigger phrases: "QSBS", "Section 1202", "R&D credit", "MainStreet", "Neo.tax", "holdco", "holding company", "Big Beautiful Bill", "tax strategy".

NOT for: bookkeeping / monthly close (use finance-controller); transfer pricing (use `international-entity-transfer-pricing`).

## Setup

```bash
# Recipient supplies:
export MAINSTREET_API_KEY="<MainStreet dashboard>"
export NEOTAX_API_KEY="<Neo.tax dashboard>"

# CPA firm engagement:
# Shay CPA, Kruze Consulting, Burkland, Pilot.com for QSB filings
```

## QSBS — Big Beautiful Bill 2025 expansion

```
PRE-BIG-BEAUTIFUL-BILL (legacy):
  Asset cap: $50M gross assets at issuance
  Individual benefit cap: $10M OR 10× basis (whichever greater)
  Exclusion: 100% capital gain if held ≥5yr (Sec 1202(a)(4))
  Stock issued: post Aug 2010 = 100%; pre Aug 2010 partial

POST-BIG-BEAUTIFUL-BILL (effective July 2025 for newly issued QSBS):
  Asset cap: RAISED to $75M
  Individual benefit cap: RAISED to $15M (or 10× basis)
  Exclusion: TIERED — 50% at 3yr | 75% at 4yr | 100% at 5yr+
  Stock must be issued after July 4, 2025 to qualify for new caps
  Earlier-issued stock = grandfathered to old rules

QUALIFICATIONS (still required):
  □ C-corp
  □ Gross assets ≤$75M at time of issuance (new cap)
  □ Active business (≤80% of assets in qualified trade or business)
  □ Stock acquired at original issuance (not secondary)
  □ Holder is individual, trust, or pass-through (not C-corp)
  □ No redemption from holder in 2yr before / after issuance > de minimis
```

## R&D credit — Section 41 + QSB payroll-tax election

```
SEC 41 R&D CREDIT (federal):
  4 tests: (1) permitted purpose, (2) elimination of uncertainty,
            (3) process of experimentation, (4) technological in nature
  Credit: ~10% of QREs (Qualified Research Expenses)
  QREs: wages of R&D staff + supplies + contractor cost (65% rate) + cloud computing

QSB PAYROLL-TAX ELECTION:
  Up to $500K/yr against employer payroll tax (FICA 6.2%) for first 5 years
  Eligibility: ≤$5M gross receipts current year AND no gross receipts in any
                tax year > 5 years before current year
  Stripe / Gusto / Rippling integration to apply credit monthly

STATE R&D CREDITS:
  CA 15% non-refundable (separate calc)
  NY ~3-6%
  TX 5%
  MA ~5-10%

DOCUMENTATION:
  Project descriptions tying to 4 tests
  Time-tracking on R&D vs non-R&D activity
  Expense allocation (W-2 wages, contractor 1099, cloud hosting receipts)
```

## Common recipes

### Recipe 1 — QSBS eligibility check

```python
def qsbs_eligible(stock_issued_date, gross_assets_at_issuance, current_holder_type,
                  active_business, holding_years):
    """Check QSBS qualification per Sec 1202."""
    issues = []
    new_cap = 75_000_000 if stock_issued_date >= "2025-07-04" else 50_000_000
    if gross_assets_at_issuance > new_cap:
        issues.append(f"Gross assets ${gross_assets_at_issuance/1e6:.1f}M exceeds {new_cap/1e6:.0f}M cap")
    if not active_business:
        issues.append("Must be active business (≤80% assets in qualified trade)")
    if current_holder_type == "C-corp":
        issues.append("Holder must be individual, trust, or pass-through (not C-corp)")
    if holding_years < 5 and stock_issued_date < "2025-07-04":
        issues.append(f"Pre-BBB stock requires ≥5yr hold for 100% exclusion (currently {holding_years}yr)")

    # New tiered for post-BBB stock
    exclusion_pct = 0
    if stock_issued_date >= "2025-07-04":
        if holding_years >= 5: exclusion_pct = 1.00
        elif holding_years >= 4: exclusion_pct = 0.75
        elif holding_years >= 3: exclusion_pct = 0.50
    else:
        exclusion_pct = 1.00 if holding_years >= 5 else 0

    return {"eligible": len(issues) == 0, "issues": issues, "exclusion_pct": exclusion_pct, "asset_cap": new_cap}

print(qsbs_eligible("2025-08-15", 45_000_000, "individual", True, 4))
```

### Recipe 2 — QSBS benefit calculation

```python
def qsbs_benefit(realized_gain_per_holder, exclusion_pct, basis_per_holder, stock_issued_date):
    cap = 15_000_000 if stock_issued_date >= "2025-07-04" else 10_000_000
    individual_cap = max(cap, 10 * basis_per_holder)
    eligible_gain = min(realized_gain_per_holder, individual_cap)
    excluded = eligible_gain * exclusion_pct
    taxable_gain = realized_gain_per_holder - excluded
    fed_lt_cap_gains_rate = 0.20
    fed_tax_saved = excluded * fed_lt_cap_gains_rate
    return {
        "realized_gain": realized_gain_per_holder,
        "individual_cap": individual_cap,
        "exclusion_pct": exclusion_pct,
        "excluded_gain": excluded,
        "taxable_gain": taxable_gain,
        "fed_tax_saved": fed_tax_saved
    }

# Founder w/ $1M basis sells $20M of post-BBB QSBS after 5+ years
print(qsbs_benefit(20_000_000, 1.0, 1_000_000, "2025-08-15"))
# Caps at $15M (new BBB cap); $5M still taxable
```

### Recipe 3 — R&D credit QSB payroll-tax-offset model

```python
def rd_credit_qsb(total_qre, federal_credit_rate=0.10, qsb_payroll_cap=500_000):
    """Sec 41 credit + QSB payroll-tax election."""
    federal_credit = total_qre * federal_credit_rate
    payroll_offset_used = min(federal_credit, qsb_payroll_cap)
    rolled_forward = federal_credit - payroll_offset_used
    return {
        "total_qre": total_qre,
        "federal_credit": federal_credit,
        "payroll_offset_used_this_year": payroll_offset_used,
        "carried_forward_to_income_tax": rolled_forward
    }

# $3M QRE, QSB
print(rd_credit_qsb(3_000_000))
# Credit $300K; can use all against payroll (under $500K cap)
```

### Recipe 4 — QRE classification helper

```python
def classify_qre(employee_records):
    """employee_records: list of {role, salary, pct_time_rd}"""
    QUALIFIED_ROLES = ["engineer", "data_scientist", "research", "product", "design"]
    qre_wages = 0
    for emp in employee_records:
        if any(r in emp["role"].lower() for r in QUALIFIED_ROLES):
            qre_wages += emp["salary"] * emp["pct_time_rd"]
    return qre_wages

emps = [
    {"role": "Software Engineer", "salary": 180_000, "pct_time_rd": 0.85},
    {"role": "Product Manager", "salary": 160_000, "pct_time_rd": 0.50},
    {"role": "Sales AE", "salary": 130_000, "pct_time_rd": 0.0},
    {"role": "Data Scientist", "salary": 195_000, "pct_time_rd": 0.95},
]
print(f"Qualified wages: ${classify_qre(emps):,.0f}")
```

### Recipe 5 — MainStreet auto-claim flow

```bash
# Connect payroll (one-time)
curl -X POST "https://api.mainstreet.com/v1/onboarding/payroll" \
  -H "Authorization: Bearer $MAINSTREET_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"payroll_provider": "gusto", "api_key": "gusto_token"}'

# Estimate R&D credit
curl "https://api.mainstreet.com/v1/credits/estimate?year=2025" \
  -H "Authorization: Bearer $MAINSTREET_API_KEY"

# Submit Form 6765 (R&D credit) — auto-prepared
curl -X POST "https://api.mainstreet.com/v1/filings/form6765" \
  -H "Authorization: Bearer $MAINSTREET_API_KEY" \
  -d '{"tax_year": 2025, "submit": true}'
```

### Recipe 6 — Holding company structure decision

```python
def holdco_decision(operating_entities, jurisdictions, ip_holder_separate, m_a_planned):
    """Decision tree for holdco structure."""
    rationale = []
    if len(operating_entities) > 1:
        rationale.append("Multiple operating entities → holdco simplifies governance + tax")
    if len(jurisdictions) > 1:
        rationale.append("Cross-border → holdco for tax treaty optimization (typical Delaware C-corp parent)")
    if ip_holder_separate:
        rationale.append("Separate IP holdco → asset protection + license-fee transfer pricing")
    if m_a_planned:
        rationale.append("M&A planned → holdco lets you buy/sell operating subs without disrupting parent equity")

    structure = "Single C-corp" if not rationale else "Holdco recommended"
    return {"structure": structure, "rationale": rationale}

print(holdco_decision(["US OpCo", "UK OpCo"], ["US", "UK"], True, True))
```

### Recipe 7 — Section 1045 rollover (defer QSBS gain)

```python
def section_1045_rollover(qsbs_gain, replacement_qsbs_purchased, replacement_window_days=60):
    """If holder reinvests proceeds into new QSBS within 60 days, defer gain."""
    if replacement_window_days > 60:
        return {"qualifies": False, "reason": "Outside 60-day window"}
    deferred = min(qsbs_gain, replacement_qsbs_purchased)
    return {
        "qualifies": True,
        "deferred_gain": deferred,
        "remaining_recognized": qsbs_gain - deferred,
        "new_holding_period": "Tacked to original QSBS"
    }

print(section_1045_rollover(8_000_000, 8_000_000, 45))
```

### Recipe 8 — QSBS planning checklist

```
Annual:
  □ Confirm gross assets stay below $75M (post-BBB) until next issuance
  □ Verify active business test (≤80% qualified assets)
  □ Track each holder's QSBS basis + issuance date separately
  □ Track each holder's holding period start

Pre-issuance (new round, new grant):
  □ Confirm asset cap headroom for issuance amount
  □ Pre-issuance: cap raised → ensure new stock qualifies under new cap
  □ Document active business at issuance date

Pre-exit:
  □ Map each holder's eligibility (basis, holding years, issuance date)
  □ Compute aggregate excluded vs taxable for each holder
  □ Sec 1045 rollover plan for any holders mid-hold (<5yr)
  □ Strategic gifting / trust planning (each non-grantor trust = separate $15M cap)
```

### Recipe 9 — Tax-strategy memo template

```markdown
# Tax Strategy Memo — Acme Inc Aug 2026

## QSBS posture
- 14 stockholders qualify
- All stock issued after Aug 2010; mix of pre-BBB and post-BBB issuance
- Aggregate excluded gain estimate at $200M exit: $135M (90% exclusion)
- Action: refresh QSBS attestation letter; confirm asset cap headroom

## R&D credit posture
- 2025 QRE estimate: $3.1M (60% engineering wages, 25% contractor, 15% cloud)
- Federal credit: ~$310K
- QSB payroll-tax election: max $500K — well under cap
- Action: MainStreet engaged Q3; Form 6765 filing Q1 2027

## Holdco structure
- Current: Delaware C-corp single entity
- Planned: pre-international launch (UK 2027) → US Delaware holdco + UK OpCo
- IP licensing arm: defer until international entity formed

## Next steps
- Engage Shay CPA for QSBS attestation
- File Form 6765 via MainStreet
- Draft IP licensing playbook
```

## Examples

### Example 1: Pre-exit QSBS planning ($200M sale)

**Goal:** Maximize QSBS exclusion across founders + employees.

**Steps:**
1. Recipe 1 → eligibility for each holder.
2. Recipe 2 → benefit per holder.
3. Recipe 7 → Sec 1045 rollover for any holders mid-hold (<5yr).
4. Strategic gifting / trust planning: each non-grantor trust = separate $15M cap.
5. Engage QSBS attestation from licensed CPA / tax counsel.

**Result:** Exclusion maximized; aggregate tax savings $30-50M typical for $200M exit.

### Example 2: Annual R&D credit claim

**Goal:** Capture max R&D credit + offset payroll tax.

**Steps:**
1. Recipe 4 → classify QREs.
2. Recipe 3 → compute federal credit + QSB payroll-offset.
3. Recipe 5 → MainStreet integration + Form 6765 submission.
4. Apply monthly against employer FICA via Gusto / Rippling adjustment.
5. State credit (CA / NY / TX / MA) — separate filing.

**Result:** Cash savings = R&D credit × monthly payroll offset.

## Edge cases / gotchas

- **QSBS asset cap tested at issuance, not currently.** Once stock issued under cap, fine even if company grows past.
- **Big Beautiful Bill effective July 4, 2025.** Pre-BBB stock = old rules ($10M cap, 100% exclusion at 5yr). Post-BBB = new ($15M cap, tiered exclusion). Mixed cap tables common — track separately.
- **Sec 1045 reinvestment window = 60 days.** Strict.
- **QSBS exclusion + state tax.** Some states (CA) decoupled and tax QSBS gain at state level. Confirm jurisdiction.
- **Secondaries reset QSBS clock for buyer.** Important in pre-IPO secondaries — buyer doesn't get sellers' holding period.
- **R&D credit + SBC.** Stock-based comp may qualify as QRE; documentation rigorous.
- **R&D 4-test failures.** "Routine" software dev (e.g. UI tweaks, bug fixes) doesn't qualify; "experimental" (new algorithms, novel architectures) does.
- **Trust planning multiplier.** Each non-grantor trust = separate QSBS individual cap. Strategic for founders w/ $50M+ exits.
- **Holdco IP transfer triggers tax.** Sec 367 / 351 / 482 implications. Engage tax counsel before transfer.
- **R&D credit audit risk.** Documentation must be contemporaneous. Reconstructing post-hoc invites IRS challenge.
- **QSB payroll-tax election eligibility resets.** If company exceeds $5M gross receipts, election ends. Plan accordingly.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions. Tax positions require licensed CPA / tax attorney sign-off.**

## Sources

- DWT QSBS Big Beautiful Bill Jul 2025: https://www.dwt.com/blogs/startup-law-blog/2025/07/qsbs-big-beautiful-bill-tax-code-upgrades
- Kruze BBB tax changes: https://kruzeconsulting.com/blog/big-beautiful-bill/
- MainStreet R&D credit platform: https://dashboard.mainstreet.com/welcome/guideline
- Carta QSBS guide: https://carta.com/learn/startups/tax-planning/qsbs/
- Haven QSBS university: https://www.usehaven.com/tax-code-university/qsbs
- IRS Sec 1202 statute: https://www.irs.gov/pub/irs-drop/n-23-66.pdf
- IRS Form 6765 (R&D Credit): https://www.irs.gov/forms-pubs/about-form-6765
- IRS Sec 41 R&D credit overview: https://www.irs.gov/businesses/audit-techniques-guide-credit-for-increasing-research-activities

## Related skills

- `409a-valuation-negotiation` — QSBS interaction with valuation date.
- `international-entity-transfer-pricing` — holdco IP transfer pricing.
- `capital-allocation-framework` — tax-adjusted ROIC analysis.
- `equity-comp-design-pool-evergreen` — QSBS implications of grant timing.
