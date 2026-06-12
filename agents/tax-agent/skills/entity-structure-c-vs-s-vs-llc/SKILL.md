<!--
Source: https://www.fenwick.com/insights/publications/choice-of-entity-startups
Source: https://carta.com/blog/c-corp-vs-s-corp-vs-llc/
Source: https://stripe.com/atlas/guides
Source: https://www.irs.gov/businesses/small-businesses-self-employed/business-structures
Source: https://www.irs.gov/forms-pubs/about-form-2553
Source: https://www.irs.gov/forms-pubs/about-form-8832
Source: https://www.irs.gov/pub/irs-drop/n-21-23.pdf (Section 280E)
Reference role.md: "C-corp vs S-corp vs LLC — which?" + "Section 280E (cannabis)"
-->

# Entity structure — C-corp vs S-corp vs LLC vs partnership

Decision framework for choosing the legal/tax entity type at formation OR at restructure. Trade-offs across (1) capital raising, (2) tax pass-through vs double-tax, (3) QSBS qualification, (4) self-employment tax, (5) Section 199A QBI, (6) Section 280E cannabis disallowance, (7) state-level recognition. Entity-selection wizards: Stripe Atlas, Clerky, LegalZoom; Carta for cap-table modeling.

## When to use

- Founder asks "C-corp vs S-corp vs LLC?" at formation OR is considering restructure (LLC → C-corp pre-VC raise; C-corp → S-corp for tax efficiency post-pivot; LLC → C-corp before QSBS clock starts).
- Cannabis business asks about Section 280E exposure + restructure to separate plant-touching entity from ancillary services.
- Pass-through entity considering Section 199A QBI deduction qualification (specified service trade or business limits).
- Multi-state entity weighing where to incorporate vs where to register as foreign entity.
- Trigger phrases: "C-corp vs S-corp", "entity choice", "S-election", "QSBS qualification", "199A QBI", "280E cannabis", "Delaware incorporation", "Wyoming LLC", "convert LLC to C-corp", "F-reorganization".

NOT for: actual entity formation legal mechanics — defer to `legal-counsel` agent for state filings, operating agreements, shareholder agreements; payroll setup once formed (use `payroll-tax-940-941-quarterly-annual`); ongoing tax filings (use `form-1120-corp-income-tax-filing` or `form-1065-1120s-passthrough-filing`).

## Setup

### Carta — cap table + QSBS tracking

```bash
# Carta REST API
export CARTA_API_KEY="..."
curl -H "Authorization: Bearer $CARTA_API_KEY" \
  https://api.carta.com/v1/firms/{id}/companies
```

### Stripe Atlas — Delaware C-corp formation

```bash
# Atlas formation portal (web; no agent-callable API)
# Atlas Tax Advisory included: https://stripe.com/atlas/tax
```

### Clerky — Delaware C-corp formation, founder-friendly

```bash
# Clerky docs at https://www.clerky.com/ (web-only filing)
```

### IRS — entity classification election

```bash
# Form 8832 (Entity Classification Election) — LLC elect to be taxed as C-corp / partnership
# Form 2553 (S-corp Election) — qualified entities elect S-corp tax treatment
# Form 8869 (Qualified Subchapter S Subsidiary) — QSub election
# All filed on paper or via preparer software; no public API
```

### Decision matrix template

```bash
# Build xlsx decision matrix
pip install openpyxl pandas
```

## Common recipes

### Recipe 1 — Decision matrix scoring by profile

```python
import pandas as pd

# Score each entity type on each criterion (0-5)
matrix = pd.DataFrame([
    {"criterion": "Raise VC capital",         "C-corp": 5, "S-corp": 1, "LLC": 2, "Partnership": 1},
    {"criterion": "QSBS qualification",       "C-corp": 5, "S-corp": 0, "LLC": 0, "Partnership": 0},
    {"criterion": "Pass-through (single tax)","C-corp": 0, "S-corp": 5, "LLC": 5, "Partnership": 5},
    {"criterion": "199A 20% QBI deduction",   "C-corp": 0, "S-corp": 4, "LLC": 4, "Partnership": 4},
    {"criterion": "Self-employment tax shield","C-corp": 5, "S-corp": 4, "LLC": 1, "Partnership": 1},
    {"criterion": "Unlimited shareholders",   "C-corp": 5, "S-corp": 1, "LLC": 5, "Partnership": 5},
    {"criterion": "Non-US shareholders",      "C-corp": 5, "S-corp": 0, "LLC": 5, "Partnership": 5},
    {"criterion": "Operational simplicity",   "C-corp": 3, "S-corp": 3, "LLC": 5, "Partnership": 4},
    {"criterion": "ESOP / stock options",     "C-corp": 5, "S-corp": 3, "LLC": 2, "Partnership": 1},
    {"criterion": "TX/OH/WA no entity income tax", "C-corp": 0, "S-corp": 5, "LLC": 5, "Partnership": 5},
])

# Weight by recipient profile (VC-backed SaaS startup)
weights = {"Raise VC capital": 5, "QSBS qualification": 5, "ESOP / stock options": 4,
           "Self-employment tax shield": 2, "Pass-through (single tax)": 1}
matrix["weighted_C"] = matrix.apply(
    lambda r: r["C-corp"] * weights.get(r["criterion"], 1), axis=1
)
print(matrix.groupby(level=0).sum())
```

### Recipe 2 — C-corp double-tax cost vs pass-through

```python
# Single-shareholder $1M pretax income
pretax = 1_000_000

# C-corp double-tax
corp_tax = pretax * 0.21
dividend_after_corp = pretax - corp_tax
qualified_div_tax = dividend_after_corp * 0.238  # 20% LTCG + 3.8% NIIT
total_c_corp = corp_tax + qualified_div_tax

# Pass-through (S-corp / LLC) — top marginal individual
passthrough_tax = pretax * 0.37
sec199a = pretax * 0.20 if pretax < 383_900 else 0  # 2026 SSTB phaseout
passthrough_net = (pretax - sec199a) * 0.37

print(f"C-corp total tax: ${total_c_corp:,.0f} ({total_c_corp/pretax:.1%})")
print(f"Pass-through total tax: ${passthrough_net:,.0f} ({passthrough_net/pretax:.1%})")
```

### Recipe 3 — Section 1202 QSBS qualification check (C-corp only)

```python
# QSBS requires:
# 1. C-corp domestic (not S-corp / LLC / partnership)
# 2. Active business (not SSTB: health, law, finance, brokerage, consulting)
# 3. Gross assets < $75M at issuance (post-OBBB July 2025; was $50M)
# 4. 5-year hold (or tiered 3/4/5-yr at 50/75/100% per OBBB 2025)
# 5. Original issuance (not secondary purchase)

is_c_corp = True
is_active = True  # NOT SSTB
gross_assets_at_issuance = 42_000_000  # < $75M
holding_years = 5.2

qsbs_qualified = (is_c_corp and is_active 
                  and gross_assets_at_issuance < 75_000_000 
                  and holding_years >= 5)
exclusion_cap = max(15_000_000, 10 * shareholder_basis)  # OBBB 2025: $15M
```

### Recipe 4 — Section 199A QBI deduction (pass-through only)

```python
# 20% deduction on qualified business income (QBI)
# Phaseout 2026: $241,950 single / $483,900 MFJ
# SSTB (health, law, accounting, consulting, financial services, brokerage, investing) 
# phases out fully above $533,900 MFJ

qbi = 425_000
taxable_income = 480_000
is_sstb = False  # SaaS = not SSTB

if not is_sstb or taxable_income < 483_900:
    sec199a_deduction = min(qbi * 0.20, taxable_income * 0.20)
else:
    sec199a_deduction = 0

# Also check W-2 wages limit (50% of W-2) + UBIA limit
w2_limit = w2_wages_paid * 0.50
ubia_limit = (w2_wages_paid * 0.25) + (qualified_property_ubia * 0.025)
sec199a_deduction = min(sec199a_deduction, max(w2_limit, ubia_limit))
```

### Recipe 5 — S-corp reasonable compensation check

```python
# IRS scrutiny: S-corp owner must pay reasonable W-2 wages BEFORE distributions
# Distribution-only treatment = SE tax avoidance = audit risk + reclassification

revenue = 1_200_000
profit_margin = 0.40
owner_role = "CEO + tech lead"
industry_median_salary = 195_000  # via BLS / RCReports / Salary.com

# Rule of thumb: reasonable comp ≥ industry median for role
recommended_w2 = max(industry_median_salary, revenue * 0.20)
# Remaining = K-1 distribution (no SE tax)
```

### Recipe 6 — Section 280E cannabis allocation

```python
# 280E disallows ALL Section 162 ordinary business deductions for 
# Schedule I/II trafficking (cannabis still Schedule I federally mid-2026)
# Only Section 471 COGS is deductible

revenue = 4_500_000
direct_costs = {
    "cultivation_labor": 480_000,   # COGS
    "seeds_nutrients": 95_000,      # COGS
    "rent_growroom": 240_000,       # COGS (allocable)
    "utilities_growroom": 85_000,   # COGS (allocable)
    "packaging": 62_000,            # COGS
}
opex_disallowed = {
    "marketing": 145_000,           # 280E disallowed
    "sales_salaries": 320_000,      # 280E disallowed
    "admin_rent": 95_000,           # 280E disallowed
    "professional_fees": 78_000,    # 280E disallowed
}

cogs = sum(direct_costs.values())
taxable_income = revenue - cogs  # no OpEx deduction
# Effective tax rate often 60-80% for plant-touching cannabis
```

### Recipe 7 — LLC → C-corp conversion (F-reorganization)

```python
# F-reorg: mere change of form; no gain recognition
# Common before VC raise (VCs require Delaware C-corp)
# Mechanics:
# 1. Form new Delaware C-corp
# 2. LLC members exchange LLC interests for C-corp stock
# 3. LLC files final Form 1065 (short year)
# 4. C-corp starts new tax year Day 1 post-conversion
# 5. QSBS clock starts at C-corp formation date — NOT at LLC formation

llc_formation_date = "2023-03-15"
c_corp_conversion_date = "2026-01-15"
qsbs_clock_starts = c_corp_conversion_date  # NOT 2023-03-15
qsbs_eligible_after = "2029-01-15"  # 3-yr tier post-OBBB
```

### Recipe 8 — State entity recognition variance

```python
# Many states diverge from federal entity classification:
state_recognition = {
    "CA": {"S-corp": "1.5% franchise tax min $800", "LLC": "$800 + LLC fee tiers"},
    "TX": {"no entity income tax — margin tax instead"},
    "OH": {"no entity income tax — CAT tax instead"},
    "WA": {"no entity income tax — B&O tax"},
    "TN": {"F&E tax on entities incl. LLCs"},
    "NY": {"S-corp must elect separately at state level (form CT-6)"},
    "NJ": {"S-corp must elect at state level (CBT-2553)"},
}
```

## Examples

### Example 1: VC-backed SaaS founder — LLC or C-corp?

**Goal:** Two technical founders, no revenue yet, planning to raise seed round in 6 months. Considering LLC (saw "LLCs are simpler" online) vs Delaware C-corp.

**Steps:**
1. Recipe 1 decision matrix weighted for VC capital + QSBS + stock options:
   - C-corp scores 25/25 on critical criteria
   - LLC scores 4/25
2. Critical factors:
   - VCs cannot invest in LLCs (most fund LPAs prohibit pass-through K-1s).
   - QSBS clock requires C-corp from day 1 (Recipe 3).
   - Stock options + 409A valuation require C-corp.
3. Conversion from LLC later costs $5-15K legal + restarts QSBS clock.

**Result:** Delaware C-corp via Stripe Atlas. File 83(b) within 30 days of founder restricted-stock grants.

### Example 2: Service consulting firm — S-corp or LLC?

**Goal:** Two co-founders providing IT consulting; $850K projected revenue; both work full-time. No external capital.

**Steps:**
1. Eliminate C-corp: no plans to raise capital + double-tax penalty.
2. S-corp vs LLC analysis:
   - SE tax savings (Recipe 5): S-corp pays W-2 wages + K-1 distribution; LLC subject to full SE tax on operating income.
   - 199A QBI deduction available for both (Recipe 4) — but consulting IS SSTB; phaseout at $483,900 MFJ 2026.
3. Reasonable comp at $185K each (BLS IT consulting median) leaves $480K distribution split → SE tax savings ~$37K/yr vs LLC.

**Result:** LLC electing S-corp via Form 2553. Recommend payroll setup via Gusto + quarterly W-2 vs distribution review.

### Example 3: Cannabis dispensary — 280E restructure

**Goal:** Single-entity LLC retail cannabis dispensary, $4.5M revenue, all expenses currently in one P&L. Owner sees crushing tax burden.

**Steps:**
1. Recipe 6: current structure → 60-80% effective tax rate.
2. Restructure proposal:
   - Plant-touching entity (NewCo Retail LLC) — 280E-affected; allocates rent / labor / packaging to COGS.
   - Ancillary services entity (NewCo Mgmt LLC) — operates marketing, admin, IT; bills NewCo Retail at arm's length.
   - Property entity (NewCo Realty LLC) — owns / leases real estate; charges rent.
3. Document intercompany agreements + transfer pricing study (cost-plus 10-15%).
4. Schedule III reclassification status check (DEA proposed May 2024; not yet final mid-2026).

**Result:** Effective tax rate drops from ~70% to ~45%; entity-level liability protection; ready for DEA Schedule III if/when finalized.

## Edge cases / gotchas

- **S-corp 100-shareholder cap + US-citizen-or-resident-alien only:** disqualifies VC investment AND foreign founders. Single non-US shareholder = automatic termination of S-election.
- **S-corp one-class-of-stock rule:** no preferred stock; no convertible notes with disproportionate rights → blocks VC preferred-equity rounds.
- **QSBS clock requires C-corp from issuance:** LLC → C-corp conversion restarts the 5-year clock (Recipe 7). If planning VC raise within 3 yrs, form C-corp immediately.
- **Section 199A SSTB definition:** consulting, health, law, accounting, financial services, brokerage, investing, athletics, performing arts excluded above income thresholds. SaaS / engineering NOT SSTB (favorable).
- **S-corp reasonable comp audits:** IRS aggressively reclassifies low-W-2 / high-distribution patterns. Document via RCReports / industry surveys.
- **Section 1202 active business requirement:** at least 80% of assets used in qualified trade or business. Excess cash > 20% = disqualification.
- **California $800 minimum franchise tax** applies to LLCs + S-corps + C-corps regardless of activity. Annual.
- **Delaware franchise tax for C-corps:** authorized-shares method OR assumed-par-value method (recommend the latter for low-revenue startups; can be $400 vs $180K with default method).
- **PTET (Pass-through Entity Tax) workaround for SALT cap:** S-corp / LLC elect to pay state tax at entity level → fully deductible (no $10K SALT cap). Available in ~36 states 2026.
- **F-reorg vs check-the-box election:** F-reorg (LLC → C-corp via state filing) is the clean path; check-the-box on Form 8832 may trigger gain on deemed liquidation if LLC has appreciated assets.
- **C-corp accumulated earnings tax (Section 531):** 20% penalty tax if retain earnings > $250K ($150K for personal service corp) without business need.
- **Personal Holding Company (Section 542) tax:** 20% on undistributed PHC income for closely-held C-corps deriving 60%+ income from passive sources.

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- Fenwick: Choice of Entity for Startups: https://www.fenwick.com/insights/publications/choice-of-entity-startups
- Carta: C-corp vs S-corp vs LLC: https://carta.com/blog/c-corp-vs-s-corp-vs-llc/
- Stripe Atlas guides: https://stripe.com/atlas/guides
- IRS Business Structures: https://www.irs.gov/businesses/small-businesses-self-employed/business-structures
- IRS Form 2553 (S-election): https://www.irs.gov/forms-pubs/about-form-2553
- IRS Form 8832 (Entity Classification): https://www.irs.gov/forms-pubs/about-form-8832
- IRS Section 280E notice: https://www.irs.gov/pub/irs-drop/n-21-23.pdf
- DEA Schedule III proposed rule: https://www.federalregister.gov/documents/2024/05/21/2024-11137/schedules-of-controlled-substances-rescheduling-of-marijuana
- AICPA 199A QBI guidance: https://www.aicpa.org/topic/tax/section-199a-qbi-deduction

## Related skills

- `qsbs-section-1202-bbb-2025-expansion` — QSBS qualification + OBBB 2025 expansion
- `form-1120-corp-income-tax-filing` — C-corp filing once formed
- `form-1065-1120s-passthrough-filing` — partnership / S-corp filing
- `state-apportionment-nexus-analysis` — multi-state recognition variance
- `payroll-tax-940-941-quarterly-annual` — S-corp reasonable comp setup
- `iso-nso-rsu-employee-tax-treatment` — equity comp requires C-corp
