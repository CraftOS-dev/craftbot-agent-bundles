<!--
Source: https://www.irs.gov/forms-pubs/about-form-5471
Source: https://www.irs.gov/forms-pubs/about-form-8865
Source: https://www.irs.gov/forms-pubs/about-form-5472
Source: https://www.irs.gov/businesses/international-businesses/transfer-pricing
Source: https://www.oecd.org/tax/beps/beps-actions/action13/
Reference role.md: "International tax + transfer pricing"
-->

# International tax — Form 5471 + 8865 + 5472 + transfer pricing

CFC (Controlled Foreign Corporation) reporting (Form 5471), foreign partnership reporting (Form 8865), foreign-owned US corp reportable transactions (Form 5472, $25K penalty per missed filing), transfer pricing studies (OECD-aligned 3-tier docs: Master File + Local File + CbCR), GILTI / Subpart F inclusions, FDII (Foreign-Derived Intangible Income), foreign tax credit Form 1118.

## When to use

- Form 5471: 10%+ US ownership of foreign corp → categories 1-5 filer determination.
- Form 8865: 10%+ US ownership of foreign partnership; or contributed property worth $100K+; or acquired/disposed 10%+ interest.
- Form 5472: 25%+ foreign owner of US corp OR foreign corp engaged in US trade with reportable related-party transactions.
- Transfer pricing study: any cross-border intercompany transaction (services, IP licensing, cost-sharing, inventory transfer).
- GILTI (Global Intangible Low-Taxed Income) calculation for US shareholders of CFCs.
- Subpart F income inclusion (passive + personal services + similar low-tax income).
- FDII (Foreign-Derived Intangible Income) §250 deduction.
- Foreign tax credit Form 1118 (corp) / 1116 (individual).
- Stripe Atlas / Clerky founders forming US C-corp from abroad → 5472 from day one.
- Trigger phrases: "Form 5471", "Form 8865", "Form 5472", "CFC", "GILTI", "Subpart F", "FDII", "transfer pricing", "TP study", "Section 482", "cost sharing", "Master File", "Local File", "CbCR".

NOT for: domestic US-only structures (use `form-1120-corp-income-tax-filing`); Pillar 2 / GloBE (use `pillar-2-globe-cbcr-international`); FBAR / FinCEN 114 (out of scope — refer to `compliance-agent`); BEA / Treasury reporting (out of scope).

## Setup

### Bloomberg Tax Transfer Pricing

```bash
# Bloomberg paid platform; uses BloombergTax.com
# Login: https://www.bloombergtax.com/
# Includes RoyaltyStat comparable database access (paid tier)
```

### ONESOURCE Transfer Pricing (Thomson Reuters)

```bash
# Same enterprise license as ONESOURCE Tax Provision
export ONESOURCE_API_KEY="..."
curl -H "Authorization: Bearer $ONESOURCE_API_KEY" \
  https://onesource.thomsonreuters.com/api/v1/tp-studies
```

### RoyaltyStat / RoyaltyRange (paid comparable databases)

```bash
# Paid databases for arm's-length licensing benchmarks
# RoyaltyStat: https://www.royaltystat.com/
# RoyaltyRange: https://www.royaltyrange.com/
```

### Preparer software (Drake / ProConnect / UltraTax / CCH)

```bash
# All handle 5471 / 8865 / 5472 module
# CCH ProSystem fx International for enterprise
```

## Common recipes

### Recipe 1 — Form 5471 categories of filer determination

```python
# Category 1a: US shareholder of "Section 965-specified foreign corp" (repatriation)
# Category 1b: US shareholder of CFC that received Section 965 inclusion
# Category 1c: US shareholder of foreign corp with non-corp US owner
# Category 2: US officer/director when 10%+ owner reorganizes
# Category 3: US person acquiring/disposing 10%+ stock
# Category 4: US person who CONTROLS foreign corp (>50% by vote/value)
# Category 5a: US shareholder of CFC owning > 10% by vote AND CFC > 50%-controlled
# Category 5b: US shareholder of CFC, where unrelated CFC related-party gain
# Category 5c: US shareholder of CFC that's only via Sec 318 attribution

def determine_5471_category(ownership_pct, is_us_shareholder, is_cfc, 
                            acquired_disposed_in_yr, controls_foreign_corp):
    categories = []
    if ownership_pct >= 0.10 and is_us_shareholder and is_cfc:
        categories.append("5a")
    if controls_foreign_corp:
        categories.append("4")
    if acquired_disposed_in_yr and ownership_pct >= 0.10:
        categories.append("3")
    # ...
    return categories
```

### Recipe 2 — Form 5471 schedules required per category

```python
# Schedules attached vary by category:
SCHEDULES_BY_CATEGORY = {
    "1a": ["E", "G", "H", "I", "J", "M", "P", "Q", "R"],
    "3": ["A", "B", "C", "F", "G", "M"],
    "4": ["A", "B", "C", "F", "G", "H", "I", "J", "M", "Q", "R"],
    "5a": ["E", "G", "H", "I", "J", "M", "P", "Q", "R"],
}
# Schedule J: accumulated E&P
# Schedule M: transactions between CFC + shareholders
# Schedule P: previously taxed E&P (PTEP)
# Schedule Q: CFC income by CFC income group
# Schedule R: distributions from foreign corp
```

### Recipe 3 — GILTI calculation (US shareholder of CFC)

```python
# GILTI = net CFC tested income > Net Deemed Tangible Income Return
# Net Deemed Tangible Income Return (NDTIR) = 10% × QBAI − interest expense

cfc_tested_income = 850_000  # CFC income except passive, FBC, ETI, etc.
qbai = 1_200_000             # Qualified Business Asset Investment
interest_expense_allocated = 35_000

ndtir = 0.10 * qbai - interest_expense_allocated  # = 85_000
gilti_inclusion = cfc_tested_income - ndtir       # = 765_000

# Section 250 deduction for C-corp: 50% of GILTI (post-2025 reduced to 37.5%)
sec250_deduction_pct = 0.50  # pre-2026; 0.375 post-2025 per TCJA sunset
gilti_taxable = gilti_inclusion * (1 - sec250_deduction_pct)
gilti_federal_tax = gilti_taxable * 0.21  # 21% corp rate × 50% inclusion = 10.5% effective
# Post-2025: × 37.5% inclusion × 21% = 13.125% effective
```

### Recipe 4 — Subpart F income (passive CFC income)

```python
# Subpart F includes: 
#  - FPHCI (Foreign Personal Holding Co Income) — dividends, interest, rent, royalty
#  - FBC (Foreign Base Company) Sales income — buy/sell with related party
#  - FBC Services income — services for/on behalf of related party
#  - Insurance income
#  - Section 245A "hybrid dividend" provisions

# De minimis exception: Subpart F < lesser of 5% gross income OR $1M → no inclusion
# Full inclusion if > 70% of gross income

subpart_f_income = 125_000
cfc_gross_income = 2_400_000
de_minimis_threshold = min(0.05 * cfc_gross_income, 1_000_000)  # = 120,000
if subpart_f_income < de_minimis_threshold:
    subpart_f_inclusion = 0
else:
    subpart_f_inclusion = subpart_f_income
```

### Recipe 5 — Form 5472 reportable transaction log (foreign-owned US corp)

```python
# Form 5472 attached to Form 1120 each year
# Required if 25%+ foreign owner AND reportable transactions exist
# Schedule of related-party transactions, both incoming and outgoing
# $25,000 penalty per missed filing (NOT per form — substantial)

import pandas as pd
reportable_txns = pd.read_sql("""
SELECT counterparty_name, counterparty_country,
       category, amount, transaction_date
FROM intercompany_transactions
WHERE counterparty_is_25pct_owner_or_related = true
  AND transaction_date BETWEEN '2025-01-01' AND '2025-12-31'
ORDER BY amount DESC
""", db)

# Form 5472 Part IV categories:
# Sales of stock in trade, Sales of tangible property, Royalties, 
# Interest received, Rents received, etc.
```

### Recipe 6 — Transfer pricing 3-tier documentation

```python
# OECD BEPS Action 13: 3-tier TP documentation

# 1. Master File (group-level):
#    - Organizational structure, business description, intangibles,
#      financial activities, financial / tax positions
master_file = {
    "section_a": "Group organizational chart (multi-tier)",
    "section_b": "Business description (products, value drivers, geography)",
    "section_c": "Intangibles (IP ownership, R&D)",
    "section_d": "Financial activities (intercompany loans, cash pooling)",
    "section_e": "Financial and tax positions (key TP policies)",
}

# 2. Local File (entity-level, per jurisdiction):
#    - Description of MNE entity, controlled transactions, financial info
local_file_germany = {
    "section_a": "Local entity description (DE GmbH function/risk/asset)",
    "section_b": "Controlled transactions detail per category",
    "section_c": "Local financial information (P&L, BS, controlled txn split)",
}

# 3. Country-by-Country Report (CbCR — for MNEs with €750M+ revenue):
#    - Per-jurisdiction revenue, profit/loss, tax paid, employees
# Filed via Form 8975 + Schedule A
# Threshold conversion: ~$850M USD (varies with FX)
```

### Recipe 7 — Arm's-length pricing methods (Section 482)

```python
# CUP (Comparable Uncontrolled Price) — most direct; use when comparable
#   third-party transactions exist
# Resale Price Method — for distributors (gross margin benchmark)
# Cost Plus Method — for manufacturers (markup over costs benchmark)
# TNMM (Transactional Net Margin Method) — net margin benchmark
# Profit Split — for highly integrated value chains
# Section 482-7 — cost sharing arrangement for IP development

# Most software cost-sharing US-DE setup:
# US develops IP; DE pays Platform Contribution Transaction (PCT) for 
# pre-existing IP + ongoing Cost Sharing Payments for R&D costs.

# Best method per IRS Reg 1.482-1(c) — facts-and-circumstances
# Each MNE picks best method; documents reasoning in TP study
```

### Recipe 8 — Cost sharing arrangement (Section 482-7) setup

```python
# Required for software / IP-heavy structures
# Each participant owns rights to use IP in respective territory
# Pre-existing IP transferred for Platform Contribution Transaction (PCT)
# Going-forward R&D costs shared per Reasonably Anticipated Benefits (RAB)

cost_sharing_doc = {
    "participants": ["US Parent", "DE GmbH"],
    "ip_territories": {"US Parent": "Americas", "DE GmbH": "EMEA + APAC"},
    "rab_share": {"US Parent": 0.45, "DE GmbH": 0.55},  # by anticipated revenue
    "pct_payment_de_to_us": 8_400_000,  # one-time PCT for pre-existing IP
    "annual_cost_share_us_to_de": 3_200_000,  # annual cost sharing payment
}
```

### Recipe 9 — Year-end TP true-up

```python
# Most MNEs operate on target margin (e.g., DE distributor: 6% operating margin)
# Year-end true-up adjusts intercompany pricing to hit target
import pandas as pd
de_results = {
    "revenue": 12_500_000,
    "cogs": 9_800_000,
    "operating_expenses": 1_650_000,
    "target_operating_margin": 0.06,
}
target_profit = de_results["revenue"] * de_results["target_operating_margin"]
actual_profit = (de_results["revenue"] - de_results["cogs"] 
                 - de_results["operating_expenses"])
true_up_amount = target_profit - actual_profit
# If positive: US Parent makes IC sale at lower price to DE (reduces DE COGS)
# If negative: US Parent invoices DE for additional service charge
```

### Recipe 10 — Form 1118 foreign tax credit

```python
# C-corp claims FTC for foreign income taxes paid
# Limit: US tax × (foreign-source TI / total TI)
# Separate basket limitations: 
#   - GILTI (Section 904(d)(1)(A))
#   - Foreign branch (Section 904(d)(1)(B))
#   - Passive category (Section 904(d)(1)(C))
#   - General category (Section 904(d)(1)(D))
#   - Section 901(j) (sanctioned countries)
#   - Treaty-resourced

foreign_tax_paid = 425_000
total_taxable_income = 4_200_000
foreign_source_ti = 1_350_000
us_tax_rate = 0.21
ftc_limit = us_tax_rate * total_taxable_income * (foreign_source_ti / total_taxable_income)
ftc_allowed = min(foreign_tax_paid, ftc_limit)
ftc_carryforward = max(0, foreign_tax_paid - ftc_allowed)  # 10-yr carryforward
```

## Examples

### Example 1: Stripe Atlas C-corp founded by Singapore resident

**Goal:** US C-corp wholly owned by non-resident; first year no operations.

**Steps:**

1. Register C-corp via Stripe Atlas / Clerky.
2. Foreign founder = 100% shareholder → 25%+ foreign ownership → Form 5472 required.
3. Even with zero revenue, Form 5472 still required IF reportable transactions (initial capital contribution = reportable).
4. Reportable transactions year 1: initial capitalization $50K from foreign founder.
5. File Form 5472 attached to Form 1120 (even if 1120 is zero-revenue).
6. Penalty for missed 5472: $25K (substantial — even for inactive shell).

**Result:** Compliance from day one; avoid $25K penalty.

### Example 2: US SaaS with German GmbH distributor, $15M revenue

**Goal:** US parent, DE GmbH distributes EMEA, intercompany transactions needing TP study.

**Steps:**

1. Form 5471 for DE GmbH: Category 4 (US Parent controls); Schedules A/B/C/F/G/H/I/J/M.
2. TP study: DE GmbH = limited-risk distributor → target 6% operating margin via TNMM.
3. Benchmark study: pull DE distributor comparables from RoyaltyStat / Bureau van Dijk Amadeus.
4. Local File for Germany (mandatory for €5M+ revenue in DE).
5. Master File at group level.
6. Subpart F check: DE GmbH operating income → not FPHCI; not Subpart F.
7. GILTI inclusion: DE GmbH tested income $850K − NDTIR ($85K) = $765K GILTI; Section 250 50% deduction → $382K taxable × 21% = $80K US tax.
8. Foreign Tax Credit Form 1118 for German corporate tax paid on DE GmbH profits.

**Result:** Form 5471 + TP study + GILTI calculation + FTC; compliant cross-border structure.

### Example 3: Foreign LLC partner in US partnership, $2M revenue

**Goal:** Cayman partner holds 30% of US LP; LP has US operating income + foreign-source.

**Steps:**

1. Form 8865 Category 4 for Cayman partner: US LP > 50% US-owned, but Cayman is 10%+ foreign partner.
2. Schedule K-3 to Cayman partner with foreign-source income breakout.
3. Withholding under Section 1446: 21% withholding on Effectively Connected Income to foreign partner.
4. Quarterly withholding deposits via EFTPS using Form 8804/8805.
5. Annual reconciliation on Form 8804 (US LP's withholding return).
6. Distribute K-3 to Cayman partner by partnership return due date.

**Result:** Withholding obligation met; foreign partner reporting clean.

## Edge cases / gotchas

- **$25K penalty for missed 5472:** per filing missed, NOT capped. Common for Stripe Atlas founders who don't realize the requirement.
- **Section 6038 penalties for missed 5471:** $10K initial, +$10K per 30 days after IRS notice (max $50K). Plus reduction of FTC by 10% per missed filing.
- **Section 6679 for missed 8865:** $10K initial, +$10K per 30-day period (max $50K).
- **Statute of limitations stays OPEN until 5471/5472/8865 filed.** Filing late doesn't trigger SOL.
- **GILTI Section 250 deduction sunset:** 50% deduction drops to 37.5% post-2025 per TCJA → effective GILTI rate rises from 10.5% to 13.125%.
- **FDII Section 250 deduction sunset:** 37.5% drops to 21.875% post-2025 → effective FDII rate rises from 13.125% to 16.4%.
- **Cost-sharing arrangement audits:** IRS aggressively audits PCT valuation. Use qualified appraiser; document RAB share basis.
- **Pillar 2 / GloBE interaction with GILTI:** GILTI is creditable in some Pillar 2 jurisdictions; Treasury negotiating final rules (2025-2026).
- **Schedule K-2/K-3 mandatory 2022+:** even domestic-only partnerships unless all-US partners certify in writing.
- **Form 8990 business interest limitation** applies to Section 163(j) at CFC level too; included in Form 5471 Schedule G.
- **Section 482 documentation safe harbor:** contemporaneous documentation reduces 20% transactional adjustment penalty under Section 6662(e).
- **Foreign branch separate basket:** post-TCJA 2017 — branch income separated into own FTC basket; can't blend with general category.
- **Country-by-Country Reporting (CbCR):** mandatory for MNEs with €750M+ revenue. Form 8975 in US; OECD member countries auto-exchange CbCRs.
- **FBAR (FinCEN 114):** separate from 5471 — required for US persons with $10K+ aggregate foreign financial accounts. Different deadline (April 15 with auto-extension to October 15).
- **Form 3520 / 3520-A:** foreign trust + gift reporting, separate from 5471/5472/8865.
- **Section 78 gross-up:** when claiming FTC on Subpart F / GILTI, must "gross up" Subpart F income by deemed-paid foreign tax (no longer applies post-2018 for actual cash dividends).

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- IRS Form 5471: https://www.irs.gov/forms-pubs/about-form-5471
- IRS Form 8865: https://www.irs.gov/forms-pubs/about-form-8865
- IRS Form 5472: https://www.irs.gov/forms-pubs/about-form-5472
- IRS Form 1118 (corp FTC): https://www.irs.gov/forms-pubs/about-form-1118
- IRS Form 8975 (CbCR): https://www.irs.gov/forms-pubs/about-form-8975
- IRS Form 8990 (interest limitation): https://www.irs.gov/forms-pubs/about-form-8990
- IRS Form 8993 (FDII): https://www.irs.gov/forms-pubs/about-form-8993
- IRS Form 8992 (GILTI): https://www.irs.gov/forms-pubs/about-form-8992
- IRS Form 8804/8805 (withholding on foreign partners): https://www.irs.gov/forms-pubs/about-form-8804
- IRS Transfer Pricing landing page: https://www.irs.gov/businesses/international-businesses/transfer-pricing
- IRC Section 482: https://www.law.cornell.edu/uscode/text/26/482
- Treas Reg 1.482-7 (cost sharing): https://www.law.cornell.edu/cfr/text/26/1.482-7
- OECD BEPS Action 13: https://www.oecd.org/tax/beps/beps-actions/action13/
- OECD TP Guidelines 2022: https://www.oecd.org/tax/transfer-pricing/oecd-transfer-pricing-guidelines-for-multinational-enterprises-and-tax-administrations-20769717.htm
- Bloomberg Tax Provision: https://www.bloombergtax.com/tax-provision/
- ONESOURCE Transfer Pricing: https://tax.thomsonreuters.com/en/onesource/transfer-pricing

## Related skills

- `pillar-2-globe-cbcr-international` — OECD Pillar 2 + GloBE
- `form-1120-corp-income-tax-filing` — C-corp returns including GILTI inclusion
- `asc-740-tax-provision-deferred` — deferred tax on GILTI / Subpart F
- `state-apportionment-nexus-analysis` — state treatment of GILTI / Subpart F
