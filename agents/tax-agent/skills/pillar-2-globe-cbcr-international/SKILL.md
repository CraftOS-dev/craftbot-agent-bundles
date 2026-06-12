<!--
Source: https://www.oecd.org/tax/beps/pillar-two-implementation-package.htm
Source: https://www.oecd.org/tax/beps/beps-actions/action13/
Source: https://www.irs.gov/forms-pubs/about-form-8975
Source: https://www.bloombergtax.com/tax-provision/
Reference role.md: "Pillar 2 / GloBE / CbCR"
-->

# Pillar 2 / GloBE + CbCR — international minimum tax

OECD Pillar 2 / GloBE (Global Anti-Base Erosion) framework: 15% minimum effective tax rate for MNCs with €750M+ consolidated revenue. Three pillars: IIR (Income Inclusion Rule) in parent jurisdiction; UTPR (Undertaxed Profits Rule) as backstop; QDMTT (Qualified Domestic Minimum Top-up Tax) in source country. Country-by-Country Reporting (CbCR) Form 8975 in US. Software: Bloomberg Tax Pillar 2, ONESOURCE Pillar 2, Longview Pillar 2.

## When to use

- MNC with consolidated revenue €750M+ in 2 of prior 4 fiscal years.
- US ultimate parent ("US-MNE") preparing CbCR Form 8975.
- US subsidiary of foreign-parented MNE receiving CbCR data for Schedule M-3 / disclosures.
- GloBE ETR (Effective Tax Rate) calculation per jurisdiction.
- Top-up Tax computation when jurisdictional ETR < 15%.
- IIR vs UTPR vs QDMTT jurisdictional rule application.
- Substance-Based Income Exclusion (SBIE) calculation.
- Trigger phrases: "Pillar 2", "Pillar Two", "GloBE", "GloBE Information Return", "IIR", "UTPR", "QDMTT", "SBIE", "country-by-country", "CbCR", "Form 8975", "BEPS Action 13", "minimum tax", "top-up tax".

NOT for: US-only domestic structures (use `form-1120-corp-income-tax-filing`); single-country foreign sub Form 5471 (use `transfer-pricing-form-5471-8865-5472`); ASC 740 deferred tax presentation including Pillar 2 (use `asc-740-tax-provision-deferred`).

## Setup

### Bloomberg Tax Pillar 2

```bash
# Bloomberg Tax Provision module + Pillar 2 add-on
# https://www.bloombergtax.com/pillar-two/
export BLOOMBERGTAX_API_KEY="..."
curl -H "Authorization: Bearer $BLOOMBERGTAX_API_KEY" \
  https://api.bloombergtax.com/v1/pillar2/calculations
```

### ONESOURCE Pillar 2 (Thomson Reuters)

```bash
export ONESOURCE_API_KEY="..."
curl -H "Authorization: Bearer $ONESOURCE_API_KEY" \
  https://onesource.thomsonreuters.com/api/v1/pillar2
```

### Longview Pillar 2 (insightsoftware)

```bash
# https://insightsoftware.com/longview/
# Enterprise tax provision + Pillar 2 module
```

### Sphere / Anrok CbCR services

```bash
# Anrok / Sphere offer CbCR module for mid-cap MNEs
# Most enterprise MNEs use Bloomberg / ONESOURCE / Longview
```

## Pillar 2 building blocks

| Term | Meaning |
|---|---|
| GloBE | OECD Global Anti-Base Erosion rules |
| IIR | Income Inclusion Rule — top-up tax in PARENT jurisdiction |
| UTPR | Undertaxed Profits Rule — backstop in OTHER jurisdictions |
| QDMTT | Qualified Domestic Minimum Top-up Tax — preserves rev for source country |
| ETR | Effective Tax Rate per jurisdiction |
| GloBE Income | Financial accounting income with adjustments |
| Covered Taxes | Income taxes + deferred tax (with adjustments) |
| Top-up Tax | (15% − ETR) × GloBE Income (after SBIE) |
| SBIE | Substance-Based Income Exclusion (payroll + tangible asset carve-out) |

## Jurisdictional implementation status (2026)

| Region | IIR effective | UTPR effective | QDMTT effective |
|---|---|---|---|
| EU (Member States) | 2024 fiscal years | 2025 fiscal years | varies by member |
| UK | 2024 | 2025 | yes |
| Japan | 2024 | 2025 | yes |
| South Korea | 2024 | 2025 | yes |
| Canada | 2024 | 2025 | yes |
| Australia | 2024 | 2025 | yes |
| United States | NOT enacted | NOT enacted | NOT enacted |
| Singapore | 2025 | 2025 | yes |
| Switzerland | 2024 | 2025 | yes (cantonal) |

US has NOT enacted IIR/UTPR/QDMTT. US-MNEs subject to other-jurisdiction IIR on foreign-parent or to UTPR if US ETR < 15% (rare since 21% corp rate; GILTI may bring effective sub-15%).

## Common recipes

### Recipe 1 — €750M revenue threshold test

```python
# In-scope if consolidated revenue >= €750M in 2 of last 4 fiscal years
# Excludes: government entities, international orgs, non-profits, pension funds,
#   investment funds (in some cases)

import pandas as pd
revenue_history = pd.DataFrame([
    {"year": 2022, "consolidated_revenue_eur": 680_000_000},
    {"year": 2023, "consolidated_revenue_eur": 745_000_000},
    {"year": 2024, "consolidated_revenue_eur": 820_000_000},
    {"year": 2025, "consolidated_revenue_eur": 910_000_000},
])
in_scope_2026 = sum(revenue_history.consolidated_revenue_eur >= 750_000_000) >= 2
# Two of last 4 yrs (2024 + 2025) >= 750M → in scope for 2026 fiscal year
```

### Recipe 2 — ETR per jurisdiction calculation

```python
# Step 1: identify "Constituent Entities" per jurisdiction (all entities)
# Step 2: compute GloBE Income for each entity (book income with adjustments)
# Step 3: compute Covered Taxes for each entity (income tax + adj for deferred)
# Step 4: aggregate per jurisdiction
# Step 5: ETR = sum(Covered Taxes) / sum(GloBE Income) per jurisdiction

jurisdictions = pd.DataFrame([
    {
        "jurisdiction": "Ireland",
        "globe_income": 45_000_000,
        "covered_taxes": 4_500_000,    # 10% effective due to IP regime
        "etr": 0.10,                    # 10% < 15% → top-up
        "tangible_assets_5pct": 250_000,
        "payroll_5pct": 1_800_000,
        "sbie": 2_050_000,
    },
    {
        "jurisdiction": "Germany",
        "globe_income": 28_000_000,
        "covered_taxes": 8_400_000,    # 30% effective
        "etr": 0.30,                    # > 15% → no top-up
    },
    {
        "jurisdiction": "United States",
        "globe_income": 120_000_000,
        "covered_taxes": 22_800_000,   # 19% effective
        "etr": 0.19,                    # > 15% → no top-up
    },
])
```

### Recipe 3 — Top-up tax calculation

```python
# Top-up tax = (15% − ETR) × (GloBE Income − SBIE) per jurisdiction
# SBIE phase-in: 7.8% payroll + 7.8% tangible in 2026, declining to 5% / 5% by 2032

ireland = jurisdictions[jurisdictions.jurisdiction == "Ireland"].iloc[0]
sbie_2026 = (ireland.payroll_5pct * 9.8/100) + (ireland.tangible_assets_5pct * 7.8/100)
# Note: SBIE percentages are step-down values, varies by year

income_subject_to_top_up = ireland.globe_income - sbie_2026
top_up_rate = 0.15 - ireland.etr  # = 0.05
top_up_tax = income_subject_to_top_up * top_up_rate
print(f"Ireland top-up tax: ${top_up_tax:,.0f}")
```

### Recipe 4 — IIR application (parent jurisdiction)

```python
# IIR collected in JURISDICTION OF UPN (Ultimate Parent Entity)
# Or in intermediate parent if UPN jurisdiction has no IIR

# Example: German parent owns Irish IP-holding sub
# DE has IIR → DE collects top-up tax on IE under-taxation
# US parent owns same Irish sub → US has NO IIR → top-up falls to UTPR jurisdictions

def iir_application(upn_jurisdiction, has_iir):
    if has_iir.get(upn_jurisdiction):
        return upn_jurisdiction  # UPN jurisdiction collects
    # Fall to intermediate parents in chain
    for intermediate in intermediate_parents_chain:
        if has_iir.get(intermediate):
            return intermediate
    return "UTPR"
```

### Recipe 5 — UTPR (Undertaxed Profits Rule) backstop

```python
# UTPR triggers if IIR doesn't capture top-up tax
# Allocates remaining top-up across UTPR jurisdictions based on:
#  - 50% based on tangible assets in jurisdiction
#  - 50% based on payroll in jurisdiction

remaining_top_up = 25_000_000  # not captured by IIR
utpr_jurisdictions = pd.DataFrame([
    {"j": "DE", "tangible": 80_000_000, "payroll": 45_000_000},
    {"j": "JP", "tangible": 65_000_000, "payroll": 32_000_000},
    {"j": "KR", "tangible": 22_000_000, "payroll": 18_000_000},
])
total_tangible = utpr_jurisdictions.tangible.sum()
total_payroll = utpr_jurisdictions.payroll.sum()
utpr_jurisdictions["share"] = (
    (utpr_jurisdictions.tangible / total_tangible) * 0.5 
    + (utpr_jurisdictions.payroll / total_payroll) * 0.5
)
utpr_jurisdictions["utpr_alloc"] = utpr_jurisdictions.share * remaining_top_up
```

### Recipe 6 — QDMTT (Qualified Domestic Minimum Top-up Tax)

```python
# Jurisdiction-level "self-help" rule:
# Source country imposes its own top-up to keep revenue locally
# Recognized by other Pillar 2 jurisdictions → no double-tax
# Most low-tax jurisdictions enacted: IE (2024), CH (2024), SG (2025), 
#   LU, MT, others

# Example: Ireland enacts QDMTT → Irish source income top-up paid to Irish revenue
#   instead of German UPN under IIR
ireland_qdmtt_paid = 2_500_000  # Ireland collects directly
# Recognized by Germany; reduces IIR claim by Germany
```

### Recipe 7 — Transitional CbCR safe harbor (through 2027)

```python
# Available 2024-2026 fiscal years (extended to 2027 for late-introduced rules)
# Eliminates top-up tax in jurisdiction if any of 3 tests met:
#  1. De minimis: revenue < €10M AND profit < €1M
#  2. Routine profit: ETR >= 15% (using CbCR data + simplified covered taxes)
#  3. Simplified ETR (transitional rates):
#       - 2024: 15%
#       - 2025: 16%
#       - 2026: 17%

cbcr_jurisdiction = {
    "j": "Ireland",
    "revenue_eur": 35_000_000,
    "profit_before_tax_eur": 12_000_000,
    "income_tax_accrued_eur": 1_800_000,
}
de_minimis = cbcr_jurisdiction["revenue_eur"] < 10_000_000 and cbcr_jurisdiction["profit_before_tax_eur"] < 1_000_000
routine_etr = cbcr_jurisdiction["income_tax_accrued_eur"] / cbcr_jurisdiction["profit_before_tax_eur"]
simplified_etr_test_2026 = routine_etr >= 0.17

safe_harbor_applies = de_minimis or (routine_etr >= 0.15) or simplified_etr_test_2026
# If safe harbor applies → no detailed Pillar 2 calc required for that jurisdiction
```

### Recipe 8 — Form 8975 + Schedule A (US CbCR)

```python
# US-MNE with $850M+ revenue files Form 8975 with Form 1120
# Schedule A: per-jurisdiction summary
#   Columns: Revenue (unrelated/related), PBT, Taxes paid, Taxes accrued, 
#            Capital, Earnings, Tangible assets ex cash, Employees

import pandas as pd
schedule_a = pd.DataFrame([
    {
        "jurisdiction": "United States",
        "rev_unrelated": 1_240_000_000,
        "rev_related": 85_000_000,
        "pbt": 245_000_000,
        "income_tax_paid_cash": 38_000_000,
        "income_tax_accrued": 45_000_000,
        "stated_capital": 250_000_000,
        "accumulated_earnings": 1_800_000_000,
        "tangible_assets": 285_000_000,
        "fte": 2_450,
    },
    {
        "jurisdiction": "Ireland",
        "rev_unrelated": 38_000_000,
        "rev_related": 280_000_000,  # IP licensing from group
        "pbt": 245_000_000,
        "income_tax_paid_cash": 24_500_000,
        "income_tax_accrued": 24_500_000,
        "stated_capital": 1_000_000,
        "accumulated_earnings": 1_400_000_000,
        "tangible_assets": 5_500_000,
        "fte": 18,
    },
    # ... per jurisdiction
])
```

### Recipe 9 — GloBE Information Return (GIR)

```python
# Annual GloBE Information Return — filed in jurisdiction of UPE or 
#   designated local entity
# Due 15 months after end of fiscal year (18 months for first year)
# Standardized GIR template adopted by OECD
# In US: filed via IRS Schedule (still pending; possibly Schedule G to Form 8975)

# Contents:
#  Part A: General info (UPE name, group structure)
#  Part B: ETR calculation per jurisdiction
#  Part C: Top-up tax per jurisdiction  
#  Part D: SBIE per jurisdiction
#  Part E: Elections + safe harbors
```

### Recipe 10 — ASC 740 Pillar 2 disclosure

```python
# ASC 740-10-50 disclosure requirements:
#  - Description of Pillar 2 exposure
#  - Estimated top-up tax in affected jurisdictions
#  - Material elections (e.g., SBIE elections, transitional safe harbor)
# IFRS / IAS 12 amendment requires similar disclosures

# In financial statements:
asc_740_disclosure = """
The Company is in scope of OECD Pillar 2 rules effective for fiscal years 
beginning on or after [date]. As of [reporting date], the Company's 
jurisdictional ETRs in [Ireland, Singapore, Cayman Islands] are below 
the 15% minimum, resulting in estimated top-up tax of $X.X million for 
FY2026. The Company applies the transitional CbCR safe harbor in 
[Germany, France, UK].
"""
```

## Examples

### Example 1: US-parented software MNE, $1.2B revenue, Irish IP holding

**Goal:** US C-corp $850M US revenue + $350M Irish sub revenue (IP licensing). Pillar 2 effective 2026.

**Steps:**

1. €750M+ test: yes (>$900M USD).
2. ETR per jurisdiction:
   - US: $245M PBT, $45M covered tax → 18% ETR ≥ 15% → no top-up.
   - Ireland: $245M PBT, $24.5M covered tax → 10% ETR < 15% → $36.75M top-up (before SBIE).
3. SBIE Ireland: 9.8% × $1.8M payroll + 7.8% × $5.5M tangible = $605K. Subject to top-up: $244.4M; top-up tax: $12.2M.
4. IIR: US has no IIR → falls to UTPR or QDMTT.
5. Ireland QDMTT (active 2024): Ireland collects $12.2M directly.
6. CbCR Form 8975 + Schedule A filed with Form 1120.
7. ASC 740 disclosure: $12.2M Pillar 2 exposure in Ireland.
8. Avoid scrutiny: ensure IP holding has substance (employees + decision-makers in IE).

**Result:** $12.2M paid to Ireland via QDMTT; no double-tax via other jurisdictions.

### Example 2: Mid-cap MNE €820M revenue, applies transitional safe harbor

**Goal:** €820M revenue MNE; multiple jurisdictions; minimize complexity via safe harbor.

**Steps:**

1. In-scope confirmed.
2. CbCR data per jurisdiction available.
3. For each jurisdiction, test 3 transitional safe harbors:
   - DE: rev €150M, profit €25M, tax €7.5M → routine ETR 30% → safe.
   - UK: rev €80M, profit €12M, tax €3M → routine ETR 25% → safe.
   - LU: rev €5M, profit €0.8M → de minimis exception → safe.
   - SG: rev €40M, profit €8M, tax €1.6M → routine ETR 20% > 17% (2026 simplified) → safe.
4. All jurisdictions pass safe harbor → no detailed Pillar 2 calc; minimal compliance burden.

**Result:** Transitional safe harbor; no top-up tax; reduced compliance.

### Example 3: Below-threshold but watching growth

**Goal:** €600M revenue MNE; close to threshold; monitor.

**Steps:**

1. Not in-scope FY 2026 (only 1 of last 4 yrs ≥ €750M).
2. Forecast revenue: €820M FY 2026, €920M FY 2027.
3. By FY 2027, 2 of last 4 yrs >= €750M → in-scope FY 2027.
4. Begin Pillar 2 readiness: data architecture, CbCR clean-up, jurisdictional ETR baseline.
5. Engage Bloomberg / ONESOURCE Pillar 2 software 12 mo before in-scope.
6. ASC 740 disclosure: future Pillar 2 exposure (qualitative).

**Result:** 18-month runway to in-scope; readiness program initiated.

## Edge cases / gotchas

- **US has NOT enacted IIR/UTPR/QDMTT** — US-MNEs subject to OTHER jurisdictions' IIR/UTPR. Watch ASC 740 disclosures.
- **GILTI vs Pillar 2 interaction:** GILTI ETR ~10.5% (50% Sec 250 deduction) often falls below 15% Pillar 2 minimum. Treasury negotiating credit mechanism.
- **Transitional safe harbor sunset:** available 2024-2026 (some jurisdictions 2027). After sunset, full Pillar 2 calc required.
- **GloBE Income vs CbCR Profit Before Tax:** different concepts. GloBE uses financial accounting income with specific adjustments. CbCR uses jurisdictional consolidated PBT.
- **Covered Taxes adjustments:** add back uncertain tax positions; exclude refundable tax credits (non-qualified); adjust deferred tax to GloBE rules.
- **SBIE phase-down:** payroll carve-out 9.8% (2024) → 5% (2032); tangible carve-out 7.8% → 5%. Watch schedule.
- **Income inclusion vs distribution:** Pillar 2 inclusion regardless of distribution. Some jurisdictions also tax on distribution (Estonia model) → coordination needed.
- **Investment fund + REIT exclusions:** generally excluded entities but COMPOSITES (e.g., fund's port-co subsidiaries) typically in scope.
- **Stateless entities:** entities without tax residence treated as stateless; specific allocation rules.
- **Joint Ventures:** different aggregation rules; check whether JV separately or with controlling parent group.
- **Acquisition / disposal of constituent entity:** rolling 4-yr revenue test includes acquired entity from acquisition date.
- **Refundable tax credits:** qualified refundable tax credits treated as income; non-qualified treated as reducing covered taxes.
- **Currency translation:** US-MNE uses presentation currency (USD); per-jurisdiction GloBE Income in functional currency translated at avg-rate (similar to ASC 830).
- **Pillar 2 deferred tax exception:** ASC 740-10-30-25(b) exempts Pillar 2 from deferred tax recognition (IAS 12 also exempt).
- **CbCR for US-MNEs:** $850M USD threshold (different from €750M); files Form 8975 + Schedule A annually.
- **Foreign-parented MNE filing CbCR through US sub:** "surrogate parent" rules — file Form 8975 if Q (Qualifying competent authority agreement) missing.
- **EU Public CbCR Directive:** separate from Pillar 2 / BEPS Action 13; EU now requires PUBLIC disclosure of CbCR data by large MNEs (2024+).

> WARNING **This is informational guidance from an AI agent. Always consult a licensed CPA or tax attorney in your jurisdiction before filing returns, claiming credits, or implementing binding tax positions.**

## Sources

- OECD Pillar 2 implementation: https://www.oecd.org/tax/beps/pillar-two-implementation-package.htm
- OECD GloBE Model Rules: https://www.oecd.org/tax/beps/tax-challenges-arising-from-the-digitalisation-of-the-economy-global-anti-base-erosion-model-rules-pillar-two.htm
- OECD GloBE Information Return: https://www.oecd.org/tax/beps/pillar-two-globe-information-return.pdf
- OECD BEPS Action 13 (CbCR): https://www.oecd.org/tax/beps/beps-actions/action13/
- IRS Form 8975: https://www.irs.gov/forms-pubs/about-form-8975
- IRS Country-by-Country Reporting: https://www.irs.gov/businesses/international-businesses/country-by-country-reporting
- EU Public CbCR Directive: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32021L2101
- Bloomberg Tax Pillar 2: https://www.bloombergtax.com/pillar-two/
- ONESOURCE Pillar 2: https://tax.thomsonreuters.com/en/onesource/pillar-two
- Longview Pillar 2: https://insightsoftware.com/solutions/by-need/tax-pillar-two/
- ASC 740-10-50 (Pillar 2 disclosure): https://asc.fasb.org/

## Related skills

- `transfer-pricing-form-5471-8865-5472` — 5471 + TP studies feed Pillar 2 inputs
- `asc-740-tax-provision-deferred` — ASC 740 Pillar 2 disclosure
- `form-1120-corp-income-tax-filing` — Form 8975 attached
- `state-apportionment-nexus-analysis` — US sub state apportionment under Pillar 2
