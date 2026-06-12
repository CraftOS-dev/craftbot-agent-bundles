<!--
Source: https://carta.com/learn/equity/stock-options/iso-amt/qsbs/
Source: https://www.fenwick.com/insights/publications/qsbs-update-one-big-beautiful-bill-act-expands-section-1202
Source: https://www.irs.gov/forms-pubs/about-form-8949
Source: https://www.law.cornell.edu/uscode/text/26/1202
Reference role.md: "QSBS Section 1202"
-->

# QSBS — Section 1202 + One Big Beautiful Bill 2025 expansion

Qualified Small Business Stock (QSBS) exclusion under IRC Section 1202: exclude federal capital gain on sale of qualified C-corp stock. OBBB July 2025 expansion: **tiered exclusion 50%/75%/100%** by **3/4/5-year holding** (replaces flat 100% at 5-yr); raised **$15M cap** (was $10M); raised **$75M gross-assets test** (was $50M); raised **$25M qualified business gross-assets-at-acquisition test**. Software: Carta QSBS, Pulley, TrueQSBS, Section 1202 Calculator. C-corp only; excluded industries: banking, farming, hospitality, professional services.

## When to use

- Founder, employee, or investor receives or contemplates C-corp stock — verify QSBS qualification at issuance.
- Pre-sale stock-sale planning: optimize for 5-year holding (100% exclusion) vs early-exit (50% or 75%).
- Stack QSBS using multiple shareholders (spouse, kids, trusts) for $15M cap × N exclusions.
- Section 1045 rollover when selling pre-5-year and reinvesting in QSBS.
- Gross-assets test monitoring as company raises capital (must be ≤ $75M at issuance).
- Trigger phrases: "QSBS", "Section 1202", "1045 rollover", "qualified small business", "gross assets test", "$10M cap", "$15M cap", "Big Beautiful Bill", "OBBB QSBS".

NOT for: NSO/ISO/RSU tax mechanics (use `iso-nso-rsu-employee-tax-treatment`); employer-level equity grant tax (same); cap table valuation (defer to `carta-pulley-cap-table` finance skill); 83(b) election mechanics (covered in `iso-nso-rsu-employee-tax-treatment`).

## OBBB 2025 changes vs pre-OBBB

| Item | Pre-OBBB (2010-2025) | Post-OBBB (Aug 2025+) |
|---|---|---|
| Holding period for 100% exclusion | 5 years | 5 years |
| Holding period for 75% exclusion | n/a | 4 years |
| Holding period for 50% exclusion | n/a | 3 years |
| Cap (greater of $X or 10× basis) | $10M | $15M |
| Gross-assets ceiling (at issuance) | $50M | $75M |
| Effective for stock issued after | 9/27/2010 | 8/1/2025 (date of OBBB enactment) |

OBBB changes apply to stock ACQUIRED after 8/1/2025; pre-OBBB stock still under old rules.

## Setup

### Carta QSBS module

```bash
# Carta Equity Plan / Cap Table includes QSBS tracking
export CARTA_API_KEY="..."
curl -H "Authorization: Bearer $CARTA_API_KEY" \
  https://api.carta.com/v1/companies/{cid}/qsbs
```

### Pulley

```bash
export PULLEY_API_KEY="..."
curl -H "Authorization: Bearer $PULLEY_API_KEY" \
  https://api.pulley.com/v1/equity/qsbs
```

### TrueQSBS

```bash
# https://www.trueqsbs.com/
# Specialized QSBS qualification analysis service
# Engagement: ~$2-5K initial qualification + annual review
```

### Section 1202 Calculator (free)

```bash
# https://www.section1202calculator.com/
# Free public calculator for QSBS scenarios
```

## Common recipes

### Recipe 1 — QSBS qualification at issuance

```python
# Five qualification tests:
def qsbs_qualified_at_issuance(issuance_data):
    # 1. Entity Type: C-corp (NOT LLC, S-corp, partnership)
    if issuance_data["entity_type"] != "C-corp":
        return False, "Not a C-corp"
    
    # 2. Gross Assets: <= $75M at all times before AND immediately after issuance
    #    (Pre-OBBB stock: $50M)
    cap = 75_000_000 if issuance_data["issuance_date"] >= "2025-08-01" else 50_000_000
    if issuance_data["gross_assets_at_issuance"] > cap:
        return False, f"Gross assets > ${cap:,.0f}"
    
    # 3. Qualified Trade or Business (NOT in excluded list):
    excluded = [
        "health", "law", "engineering", "architecture", "accounting",
        "actuarial science", "performing arts", "consulting", "athletics",
        "financial services", "brokerage services", "any trade or business"
        " where the principal asset is the reputation or skill of employee/owner",
        "banking", "insurance", "financing", "leasing", "investing",
        "farming", "mining (oil/gas)", "production of products subject to depletion",
        "hotel/motel/restaurant", "similar businesses",
    ]
    if any(x in issuance_data["business_description"].lower() for x in excluded):
        return False, "Excluded trade or business"
    
    # 4. Active Business Requirement: 80%+ of assets used in qualified trade
    if issuance_data["active_asset_pct"] < 0.80:
        return False, "Active assets < 80%"
    
    # 5. Stock issued in exchange for money, property (not stock), or services
    if issuance_data["consideration"] not in ["cash", "property", "services"]:
        return False, "Invalid consideration"
    
    return True, "Qualified"
```

### Recipe 2 — Holding-period tiered exclusion (OBBB)

```python
# Post-OBBB stock acquired 8/1/2025+:
def tiered_exclusion(holding_months):
    if holding_months >= 60: return 1.00  # 100% if 5+ years
    if holding_months >= 48: return 0.75  # 75% if 4 years
    if holding_months >= 36: return 0.50  # 50% if 3 years
    return 0.00  # 0% if < 3 years

# Pre-OBBB stock (issued 9/27/2010 - 7/31/2025):
def pre_obbb_exclusion(holding_months):
    return 1.00 if holding_months >= 60 else 0.00
```

### Recipe 3 — Per-shareholder $15M cap (post-OBBB)

```python
# Cap = greater of:
#  (a) $15M (post-OBBB; was $10M pre-OBBB)
#  (b) 10× shareholder's adjusted basis in QSBS sold during taxable year

shareholder_basis = 800_000
gain_realized = 18_000_000
holding_months = 62

post_obbb = True  # if stock issued after 8/1/2025
cap_dollar = 15_000_000 if post_obbb else 10_000_000
cap_10x_basis = 10 * shareholder_basis  # = 8M
gain_cap = max(cap_dollar, cap_10x_basis)  # = 15M

exclusion_pct = tiered_exclusion(holding_months) if post_obbb else pre_obbb_exclusion(holding_months)
excluded_gain = min(gain_realized, gain_cap) * exclusion_pct
taxable_gain = gain_realized - excluded_gain

# = 18M - (15M × 100%) = 3M taxable
# 3M taxed at LTCG rate 20% + NIIT 3.8% = 23.8% federal
print(f"Excluded: ${excluded_gain:,.0f} | Taxable: ${taxable_gain:,.0f}")
```

### Recipe 4 — Section 1045 rollover (pre-5-yr exit)

```python
# Sell QSBS held > 6 months but < 5 years
# Reinvest into "replacement QSBS" within 60 days
# Defer gain (basis carries to replacement)
# Tack holding period from original

sale_proceeds = 4_800_000
original_basis = 200_000
gain = sale_proceeds - original_basis  # = 4.6M

# Rollover into new QSBS company within 60 days
rollover_amount = 4_300_000  # invested in replacement QSBS
deferred_gain = min(gain, rollover_amount)  # = 4.3M
recognized_gain = gain - deferred_gain  # = 0.3M (excess proceeds taxable)
new_basis = rollover_amount - deferred_gain  # basis carries to new
```

### Recipe 5 — QSBS stacking via family / trusts

```python
# Each shareholder gets own $15M cap
# Strategy: gift QSBS to family members BEFORE sale to multiply caps

founder_shares = 1_000_000
spouse_gift = 200_000      # married couples = 2 × $15M caps
trust_for_kids = 200_000   # 1 NING trust = 1 × $15M cap (if separate taxpayer)
sibling_gift = 100_000     # additional cap if sold to unrelated buyer

# Federal gift tax: annual exclusion $18K (2026); lifetime exemption $13.99M (2026)
# Use lifetime exemption for QSBS gifts to children (NING trust)

# Critical: gift must be BEFORE the buyer is identified to avoid 
#   "step transaction" doctrine collapse
```

### Recipe 6 — Gross-assets test monitoring (raise tracking)

```python
# $75M gross-assets test (post-OBBB) measured "at all times before and 
#   immediately after" issuance
# If you raise capital pushing gross assets > $75M, FUTURE issuances 
#   lose QSBS qualification (but prior issuances stay qualified)

import pandas as pd
cap_history = pd.DataFrame([
    {"date": "2024-03-15", "round": "Seed", "raise": 2_500_000, 
     "gross_assets_after": 2_300_000, "qsbs_eligible": True},
    {"date": "2025-06-20", "round": "Series A", "raise": 12_000_000,
     "gross_assets_after": 13_500_000, "qsbs_eligible": True},
    {"date": "2026-09-10", "round": "Series B", "raise": 45_000_000,
     "gross_assets_after": 52_000_000, "qsbs_eligible": True},  # < 75M
    {"date": "2027-04-22", "round": "Series C", "raise": 60_000_000,
     "gross_assets_after": 95_000_000, "qsbs_eligible": False},  # > 75M
])
# Series C stock NOT QSBS — but Seed/A/B remain QSBS forever
```

### Recipe 7 — Active business + 80% asset test

```python
# 80%+ of assets must be used in active qualified trade or business
# "Used" = engaged in trade, NOT held for investment
# Cash + securities NOT active assets (with exceptions for 1-yr working capital reserve)

balance_sheet = {
    "cash": 35_000_000,
    "marketable_securities": 5_000_000,
    "ppe_net": 8_000_000,
    "intangibles_software": 22_000_000,
    "operating_capital_required": 12_000_000,
}
active_assets = (balance_sheet["ppe_net"] 
                 + balance_sheet["intangibles_software"]
                 + balance_sheet["operating_capital_required"])
total_assets = sum(balance_sheet[k] for k in ["cash","marketable_securities","ppe_net","intangibles_software"])
active_pct = active_assets / total_assets
# If < 80%, may fail active business test — risk QSBS for future periods
```

### Recipe 8 — Form 8949 + Schedule D reporting

```python
# Report sale on Form 8949 with code Q in column (f) for QSBS exclusion
# Schedule D summary
# Form 6251 AMT preference: 7% of excluded gain (Section 57(a)(7))

form_8949 = {
    "description": "Acme Inc QSBS — 250K shares",
    "date_acquired": "2024-06-15",
    "date_sold": "2029-08-20",  # 62 mo holding
    "proceeds": 18_000_000,
    "basis": 800_000,
    "code": "Q",  # QSBS exclusion
    "adjustment": -15_000_000,  # excluded portion
    "gain_loss": 2_200_000,  # taxable portion
}

# AMT preference (Section 57(a)(7) — 7% of excluded amount)
amt_preference = 15_000_000 * 0.07  # = 1.05M added to AMTI on Form 6251
```

### Recipe 9 — State QSBS conformity

```python
# State conformity varies:
STATE_QSBS_CONFORMITY = {
    "CA": "NONE",  # California does NOT recognize Section 1202; full state tax
    "NY": "FULL",  # Conforms to federal exclusion
    "TX": "n/a",   # No state income tax
    "FL": "n/a",   # No state income tax
    "MA": "PARTIAL", # Conforms with modifications
    "NJ": "NONE",
    "PA": "NONE",
    "WA": "n/a",   # No state income tax
}
# CA founders selling QSBS face 13.3% state tax on full gain even if 100% federal exclusion
# Some founders pre-sale relocate to no-tax state (TX, FL, WA, NV); IRS scrutiny on residency
```

### Recipe 10 — QSBS qualification opinion letter

```python
# Sale to acquirer: acquirer typically wants QSBS opinion letter from tax counsel
# Confirms qualification at issuance + holding period + exclusion eligibility
# TrueQSBS or law firm produces; ~$5-15K depending on complexity

opinion_letter_contents = [
    "Entity is C-corp throughout holding period",
    "Issuance date is X; pre/post-OBBB rule application",
    "Gross assets at issuance: $X (< $75M cap)",
    "Active trade test: $X active / $Y total = Z% (>= 80%)",
    "Qualified trade or business (not in excluded list)",
    "Original issuance to shareholder (not secondary)",
    "Holding period at sale: N months",
    "Applicable exclusion percentage: 50/75/100%",
    "Per-shareholder cap: $X (greater of $15M or 10× basis)",
]
```

## Examples

### Example 1: Solo founder, $25M exit at 6-year holding (post-OBBB stock)

**Goal:** Founder issued stock 9/2025 (post-OBBB), sells 11/2031 ($25M), basis $1K.

**Steps:**

1. Issuance: Sep 2025 = post-OBBB; 75M gross-asset cap; $15M dollar cap.
2. Qualification at issuance: C-corp + B2B SaaS (not excluded) + gross assets $2.1M + active.
3. Holding: Sep 2025 → Nov 2031 = 74 months ≥ 60 → 100% exclusion.
4. Gain: $25M − $1K = $24,999,000.
5. Cap = max($15M, 10× $1K = $10K) = $15M.
6. Excluded: min($25M gain, $15M cap) × 100% = $15M excluded.
7. Taxable: $24,999,000 − $15M = $9,999,000 × 23.8% (LTCG + NIIT) = $2.38M federal tax.
8. State: depends on residency (CA = full state tax on excluded portion too).
9. AMT preference: $15M × 7% = $1.05M added AMTI (minimal AMT impact typically).
10. Form 8949 code Q on individual 1040.

**Result:** $15M tax-free; $2.38M federal tax on $10M taxable.

### Example 2: Series A founder stacking $30M via spouse + 2 kid trusts (pre-OBBB)

**Goal:** Founder owns QSBS issued 2020 ($10M cap). Stacks to $30M exclusion.

**Steps:**

1. Identify M&A imminent (not signed).
2. Gift 1/3 shares to spouse (gift to spouse exempt from gift tax).
3. Gift 1/3 shares to 2 NING trusts for kids (use lifetime gift exemption $13.99M each).
4. Step transaction risk: gift BEFORE buyer identified; document gift independent of sale.
5. Sale occurs 18 months later: $30M gain attributable to QSBS.
6. Each of 3 shareholders (founder, spouse, NING trust) exclude $10M (pre-OBBB cap).
7. Total excluded: $30M, fully sheltered.

**Result:** Full $30M federal exclusion via stacking.

### Example 3: Founder sells at 3-year holding (post-OBBB) → 50% exclusion

**Goal:** Forced sale at 38 months due to acquirer; $12M gain.

**Steps:**

1. Holding 38 months → 36-47 mo bucket → 50% exclusion (post-OBBB).
2. Cap = $15M; gain $12M ≤ cap.
3. Excluded: $12M × 50% = $6M.
4. Taxable: $6M × 23.8% = $1.43M.
5. Consider Section 1045 rollover into another QSBS company: defers entirely.
6. AMT preference 7% × $6M = $420K AMTI add.

**Result:** Partial exclusion; rollover available if continuing in startup ecosystem.

## Edge cases / gotchas

- **OBBB effective date 8/1/2025:** stock issued before 8/1/2025 follows pre-OBBB rules ($10M cap, $50M gross assets, flat 100% at 5-yr). After 8/1/2025: tiered + $15M / $75M.
- **C-corp ONLY:** LLCs, S-corps, partnerships do NOT qualify. Convert LLC → C-corp BEFORE crossing $75M gross assets, otherwise lose QSBS forever for future-issued stock.
- **Original issuance:** must acquire DIRECTLY from issuer (not secondary market). Exceptions: gift, inheritance, partnership distribution.
- **Excluded businesses:** health, law, engineering, architecture, accounting, actuarial science, performing arts, consulting, athletics, financial services, brokerage; banking, insurance, leasing, investing, farming, oil/gas, mining, hotel/motel/restaurant. SaaS / tech / software / clean energy / manufacturing = NOT excluded.
- **Active business test 80%:** measured throughout holding period. Sudden cash hoard from large raise can dip below — careful with $100M+ raises holding excess cash > 1 yr.
- **Working capital reserve:** cash held for "reasonable working capital needs" not in next 2 yrs counts as active asset.
- **5-yr active business research / startup activities:** during R&D / startup phase before product launch, special rule deems active.
- **Step transaction on gifts:** IRS may collapse gift + sale if too close (no bright-line, typically 12+ months safer).
- **Spousal QSBS doubles cap** (each spouse own $15M cap if QSBS held in separate names). Marriage timing matters.
- **NING (Nevada / Delaware Incomplete Non-Grantor) trust:** can create separate taxpayer for QSBS stacking. Setup cost $5-15K; annual ~$2-5K.
- **CA non-conformity:** California does NOT recognize Section 1202; 13.3% state tax on full gain. Relocate residency PRE-SALE if feasible (180-day rule for residency).
- **AMT preference Section 57(a)(7):** 7% of excluded gain added to AMTI. Rarely creates AMT for individuals at high LTCG, but check Form 6251.
- **Conversion from LLC / S-corp:** stock issued after conversion = QSBS if other tests met. Stock holding starts at conversion (not original LLC interest acquisition).
- **Section 1045 60-day reinvestment:** strict deadline; can roll into multiple QSBS companies; tacks holding period.
- **Section 1244 small business stock:** different provision — converts ordinary loss treatment for $50K/$100K losses; NOT related to 1202 exclusion.
- **State residency for QSBS:** California aggressive on residency audits when founders relocate pre-sale. Establish bona fide new residency 6-12 mo pre-sale; sell after California departure.
- **Treasury regulations not yet issued for OBBB 2025 changes** — practitioners using statutory text; IRS guidance expected 2026-2027.

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- IRC Section 1202: https://www.law.cornell.edu/uscode/text/26/1202
- IRC Section 1045: https://www.law.cornell.edu/uscode/text/26/1045
- IRS Form 8949: https://www.irs.gov/forms-pubs/about-form-8949
- IRS Schedule D: https://www.irs.gov/forms-pubs/about-schedule-d-form-1040
- IRS Form 6251 (AMT): https://www.irs.gov/forms-pubs/about-form-6251
- Carta QSBS guide: https://carta.com/learn/equity/stock-options/iso-amt/qsbs/
- Fenwick & West — OBBB QSBS expansion: https://www.fenwick.com/insights/publications/qsbs-update-one-big-beautiful-bill-act-expands-section-1202
- One Big Beautiful Bill Act: https://www.congress.gov/bill/119th-congress/house-bill/1
- Pulley QSBS: https://pulley.com/equity/qsbs
- TrueQSBS: https://www.trueqsbs.com/
- Section 1202 Calculator: https://www.section1202calculator.com/
- Wood Smith Henning & Berman — Section 1202: https://www.section1202.com/

## Related skills

- `iso-nso-rsu-employee-tax-treatment` — equity comp tax timing
- `entity-structure-c-vs-s-vs-llc` — C-corp election for QSBS qualification
- `nol-amt-multi-year-tax-planning` — AMT preference + state planning
- `state-apportionment-nexus-analysis` — state residency for CA-non-conformity
- `form-1120-corp-income-tax-filing` — C-corp election + gross assets monitoring
