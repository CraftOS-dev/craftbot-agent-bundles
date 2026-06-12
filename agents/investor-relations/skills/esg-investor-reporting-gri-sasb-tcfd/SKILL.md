<!--
Source: https://www.ifrs.org/issued-standards/ifrs-sustainability-standards/
Source: https://www.globalreporting.org/standards/standards-development/
Source: https://www.workiva.com/solutions/esg-reporting
Source: https://www.cdp.net/en
Source: https://www.fsb-tcfd.org/recommendations/
Source: https://www.sec.gov/news/press-release/2024-31
Reference role.md: "ESG investor reporting playbook"
Round 2 enrichment: framework selection matrix + IFRS S1/S2 + GRI 2025 + SASB + TCFD + CDP library + Workiva ESG REST + MSCI/Sustainalytics QC.
-->

# ESG-for-investors reporting (IFRS S1/S2 + GRI 2025 + SASB + TCFD)

Drafts the ESG-for-investors report against the 2026 framework hierarchy: IFRS S1 (general) + S2 (climate) as baseline, SASB (sector-specific, now under IFRS), GRI 2025 (stakeholder lens; CSRD-required in EU), TCFD (climate; subsumed by IFRS S2 but still referenced), CDP (free climate / water / forest disclosure). Workiva ESG is the drafting platform. **Defers framework selection to `compliance-agent`; binding sign-off to `legal-counsel`.**

## When to use

- Annual ESG-for-investors report drafting.
- Sustainability section of 10-K Item 1 / 1A (climate risk).
- CDP annual climate / water / forest disclosure.
- MSCI ESG / Sustainalytics / S&P Global ESG rating preparation.
- EU CSRD ESRS compliance (if EU listed or material EU operations).
- Trigger phrases: "ESG report", "sustainability report", "IFRS S1", "IFRS S2", "GRI 2025", "TCFD", "CDP", "climate disclosure", "CSRD".

NOT for: framework selection (use `compliance-agent`); financial materials' climate risk modeling (use `finance-agent`); SEC climate disclosure rule binding interpretation (use `legal-counsel`).

## Setup

```bash
# Workiva ESG (preferred — paid)
export WORKIVA_API_KEY="<from Workiva Admin -> API>"     # $60K+/yr bundle

# CDP (free)
export CDP_API_KEY="<from CDP Disclosure Portal>"

# MSCI ESG / Sustainalytics / S&P Global (paid; for rating QC)
export MSCI_ESG_API_KEY="<from MSCI ESG Manager>"           # $40K+/yr
export SUSTAINALYTICS_API_KEY="<from Sustainalytics>"       # $30K+/yr
export SP_GLOBAL_ESG_API_KEY="<from S&P Global ESG>"        # $30K+/yr

# Tools: docx for portable draft; sec-edgar-mcp for climate-rule precedent
```

Auth / API key requirements:
- `WORKIVA_API_KEY` — Workiva ESG module bundled with SEC Reporting ($60K+/yr).
- CDP — free for issuers (mandatory for many institutional ESG raters).
- MSCI/Sustainalytics/S&P — paid; for rating preparedness (recipient may have one).
- Free fallback: native PDF drafting + CDP direct submission.

Data inputs:
- Scope 1 + 2 GHG emissions inventory (annual; CDP-compatible).
- Scope 3 (where material; 15 categories under GHG Protocol).
- Energy consumption (kWh; renewable %; intensity).
- Water (withdrawal; consumption; stress-area).
- Waste (hazardous; non-hazardous; circular).
- DEI metrics (board diversity; workforce diversity).
- Climate scenario analysis (2 deg C, NZE 2050 paths).
- TCFD 4 pillars (governance / strategy / risk mgmt / metrics + targets).
- Materiality assessment.
- Auditor third-party verification (limited / reasonable assurance level).

## Framework stack (2026)

| Framework | Status (2026) | Scope | Audience |
|-----------|--------------|-------|----------|
| **IFRS S1** | Active — baseline globally via ISSB | General sustainability | All investors |
| **IFRS S2** | Active — climate (subsumes TCFD) | Climate-specific | All investors |
| **SASB** | Now under IFRS; sector-specific quantitative | 77 sector standards | Investors (financial materiality) |
| **GRI 2025** | Active — broader stakeholder lens; CSRD-required in EU | Stakeholders + investors | All stakeholders |
| **TCFD** | Subsumed by IFRS S2; still referenced | Climate | Investors |
| **CDP** | Active — climate / water / forest (free) | Sector + theme | Public + raters |
| **SEC Climate Rule** | Adopted 2024 (partial stays); 10-K Item 1A; effective phased 2025+ | Climate | US issuers |
| **EU CSRD ESRS** | Active — EU listed cos + EU subs | All sustainability | EU regulators + investors |

## Metrics library (core, 2026 IFRS S1/S2 + SASB-anchored)

```
ENVIRONMENT
- GHG Emissions (Scope 1, 2 location-based, 2 market-based, 3 by category)
- Emissions intensity (tCO2e / $ revenue)
- Energy (total kWh; renewable %; intensity)
- Water (withdrawal; consumption; stress-area exposure)
- Waste (hazardous; non-hazardous; landfill diversion)
- Climate scenario alignment (2C, 1.5C, NZE 2050)

SOCIAL
- Workforce diversity (gender; ethnicity; age)
- Board diversity (gender; independence; tenure)
- Employee engagement (eNPS or proxy)
- Health & safety (TRIR; LTI; fatalities)
- Pay equity (median pay gap; CEO ratio under Item 402(u))
- Training hours (per FTE)
- Customer privacy (incidents; data subjects affected)
- Human rights (supply chain audits)

GOVERNANCE
- Board oversight of ESG (committee charter, named director)
- Climate/cyber expertise on board
- Anti-corruption (incidents; training %)
- Whistleblower (reports; resolution)
- Executive comp linked to ESG metrics (% of LTI)
- Political contributions / lobbying expenditures
- Tax transparency
```

## Workflow

1. **Defer framework selection** to `compliance-agent` (typically IFRS S1/S2 + GRI 2025 + SASB + TCFD + CDP combination + SEC climate rule + CSRD if EU).
2. Pull metrics from `finance-agent`'s ERP + `compliance-agent`'s sustainability ops.
3. Materiality assessment + double-materiality (financial + impact) if CSRD.
4. Draft narrative + tagged metrics in Workiva ESG.
5. Third-party assurance (limited or reasonable per company stage).
6. QC against MSCI ESG + Sustainalytics rating criteria.
7. Counsel review for forward-looking ESG statements (Safe Harbor).
8. Publish: ESG PDF + IR website hub + 10-K cross-ref + CDP filing.

## Common recipes

### Recipe 1 — Pull SEC climate-rule precedent (10-K Item 1A)
```bash
mcp call sec-edgar-mcp fetch_form --ticker=$PEER_TICKER --form=10-K --section="Item 1A"
# Find peer climate-risk language for benchmarking
```

### Recipe 2 — Workiva ESG draft
```bash
curl -X POST -H "Authorization: Bearer $WORKIVA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "ESG_report",
    "frameworks": ["IFRS_S1", "IFRS_S2", "GRI_2025", "SASB", "TCFD"],
    "fiscal_year": 2026
  }' \
  "https://api.workiva.com/v1/documents"
```

### Recipe 3 — CDP climate disclosure submission
```bash
# CDP free submission; required for many ESG raters
curl -X POST -H "Authorization: Bearer $CDP_API_KEY" \
  -F "questionnaire=climate_change_2026" \
  -F "data=@cdp_climate_2026.json" \
  "https://api.cdp.net/v1/responses"
```

### Recipe 4 — GHG inventory build (Scope 1 + 2)
```python
# Scope 1: direct emissions (fuel, fleet, refrigerants)
scope_1 = sum([
    fuel_consumed_diesel_L * 2.68 / 1000,        # tCO2e
    fuel_consumed_natural_gas_m3 * 1.89 / 1000,
    refrigerant_R410A_kg * 2088 / 1000,
])
# Scope 2: location-based vs market-based
scope_2_location = sum(electricity_kWh_by_region * grid_factor_by_region) / 1000
scope_2_market = sum(electricity_kWh_with_renewable_PPA * 0 +
                     electricity_kWh_without_PPA * residual_mix_factor) / 1000
```

### Recipe 5 — IFRS S2 climate scenario analysis
```python
# Required: 2-3 scenarios; quantitative or qualitative
SCENARIOS = {
    "RCP 1.9 / NZE 2050": "1.5C aligned; physical risk lower; transition risk higher",
    "RCP 4.5 / Delayed Transition": "2-2.5C; mixed physical + transition",
    "RCP 8.5 / Current Policies": "3-4C; high physical risk; low transition",
}
# For each: assess our revenue, cost, asset exposure
```

### Recipe 6 — TCFD 4-pillar disclosure (subsumed by IFRS S2 but format remains)
```
GOVERNANCE: Board oversight + management's role
STRATEGY: Climate-related risks + opportunities; impact on business model + strategy
RISK MGMT: Identification + assessment + integration with overall risk
METRICS + TARGETS: Scope 1/2/3; targets; performance
```

### Recipe 7 — MSCI ESG rating QC pre-publication
```bash
curl -H "Authorization: Bearer $MSCI_ESG_API_KEY" \
  "https://api.msci.com/v1/esg/issuer-rating?issuer_id=$ISSUER&pillar=all"
# Returns: rating + pillar scores + gaps; close gaps before publication
```

### Recipe 8 — Sustainalytics ESG Risk Rating QC
```bash
curl -H "Authorization: Bearer $SUSTAINALYTICS_API_KEY" \
  "https://api.sustainalytics.com/v1/issuer-rating/$ISSUER_ID"
```

### Recipe 9 — Double-materiality (CSRD ESRS)
```python
# CSRD requires double-materiality: financial materiality + impact materiality
def double_materiality_score(topic):
    return {
        "financial_materiality": assess_revenue_cost_impact(topic),  # IFRS S1/S2
        "impact_materiality": assess_environment_society_impact(topic),  # GRI
    }
# Topic = material under CSRD if EITHER score is material
```

### Recipe 10 — SEC climate rule 10-K integration
```python
# SEC climate rule (adopted 2024) requires:
# Item 1A: material climate-related risks
# Item 7 MD&A: financial impact of severe weather + transition activities
# Notes: separate financial statement disclosures for severe weather, etc.
SEC_CLIMATE_RULE_SECTIONS = [
    "Item 1A Risk Factors — climate-related risks (acute + chronic; transition)",
    "Item 7 MD&A — financial impacts of severe weather + carbon offsets/RECs",
    "Notes — capitalized costs, expenditures, losses from severe weather > 1% pretax inc",
]
# Stay-bound; counsel monitors SEC progress
```

### Recipe 11 — Third-party assurance scope
```python
ASSURANCE_LEVELS = {
    "limited": "moderate level of assurance; 'plausibility' opinion; cheaper",
    "reasonable": "high level of assurance; equivalent to audit opinion; expensive",
}
# Big 4 (PwC / EY / Deloitte / KPMG) or specialist (ERM / Bureau Veritas / DNV)
# Start with limited; mature to reasonable over 2-3 years
```

### Recipe 12 — Materiality assessment (stakeholder + financial)
```python
# Survey stakeholders (investors, customers, employees, regulators, NGOs)
# Plot topics on 2D matrix: x = stakeholder importance, y = business impact
# Top-right quadrant = material topics
```

## Examples

### Example 1: First-time IFRS S1/S2 ESG report (mid-cap)

**Goal:** FY2026 ESG report; first-time IFRS S1/S2 adoption.

**Steps:**
1. T-9 months: `compliance-agent` selects frameworks; agree on IFRS S1/S2 + SASB + GRI + TCFD + CDP.
2. T-7: Materiality assessment (Recipe 12).
3. T-6: GHG inventory baseline (Recipe 4); engage assurance (Recipe 11; start with limited).
4. T-5: Pull peer ESG reports (Recipe 1) + MSCI rating gap analysis (Recipe 7).
5. T-4: Draft narrative in Workiva ESG (Recipe 2).
6. T-3: Climate scenario analysis (Recipe 5); TCFD 4-pillar (Recipe 6).
7. T-2: Third-party assurance review pass.
8. T-1: Counsel review of forward-looking statements.
9. T-0: Publish ESG PDF; CDP submission (Recipe 3); IR website hub (`ir-website-q4-notified`); 10-K cross-ref.
10. T+30: rating engagement — submit to MSCI / Sustainalytics / S&P Global.

**Result:** First-time IFRS S1/S2 report published; MSCI rating improved 1 notch within 6 months.

### Example 2: CSRD ESRS first-year compliance (EU listed)

**Goal:** EU CSRD ESRS first-year; double-materiality + assurance required.

**Steps:**
1. Engage CSRD-specialist consultant (Big 4 or specialist).
2. Double-materiality assessment (Recipe 9).
3. Map IFRS S1/S2 + ESRS overlap (large; ~90% reusable).
4. Build full ESRS disclosure (E1-E5 environment; S1-S4 social; G1 governance).
5. Limited assurance year 1 (Recipe 11); reasonable assurance phase-in by year 3.
6. Counsel review.
7. File with EU regulator + publish.

**Result:** CSRD compliance; avoids regulatory finding.

## Edge cases / gotchas

- **Framework selection is `compliance-agent`'s decision.** IR drafts within whatever framework counsel + compliance choose; don't override.
- **Greenwashing risk.** Vague claims ("net zero by 2050") without interim targets + science alignment = SEC enforcement + activist lawsuit risk.
- **Scope 3 methodology choice.** GHG Protocol allows multiple methodologies; pick one + disclose; consistency matters.
- **Carbon offsets / RECs.** Disclosing market-based Scope 2 requires sourcing; must verify; greenwashing risk if not.
- **TCFD subsumption.** TCFD framework still useful for structure but IFRS S2 is the disclosure requirement.
- **CSRD applicability.** Triggers: EU listed; or EU sub revenue >EUR 150M + 2 of 3 (assets EUR 25M, employees 250, revenue EUR 50M); recipient must verify.
- **SEC climate rule litigation.** Multiple Circuit Court challenges (currently stayed); monitor.
- **MSCI rating dispute.** Methodology opacity; engage MSCI directly via portal.
- **Sustainalytics dispute resolution.** Per-controversy review available.
- **Forward-looking ESG statements.** Counsel must review Safe Harbor coverage; "net zero by X" is a forward statement.
- **Workiva ESG paywall.** $60K+/yr bundle. Free fallback: native PDF + CDP direct submission.
- **Stakeholder vs investor focus.** IFRS S1/S2 + SASB = investor-focused; GRI 2025 + CSRD = stakeholder-focused. Most cos do both.
- **Assurance scope creep.** Limited -> reasonable doubles cost; phase in.
- **Internal vs external metrics gap.** Internal sustainability ops may have data IR/compliance don't see; build single source of truth.
- **Industry benchmarking thinness.** Peer ESG reports vary wildly in quality; use top peers as bar.

> Mandatory disclaimer: ESG disclosures touching financial materiality are subject to SEC climate rule (where applicable), Reg G, Safe Harbor, and Reg FD. Forward-looking ESG statements (including net-zero targets, transition plans, scenario analysis) require Safe Harbor coverage. EU CSRD ESRS is a binding regulatory regime. **Consult licensed securities counsel** for binding ESG/climate/sustainability disclosure decisions, framework interpretation, Safe Harbor coverage on forward statements, and EDGAR/EU regulatory submission.

## Sources

- IFRS Sustainability Standards (S1 + S2): https://www.ifrs.org/issued-standards/ifrs-sustainability-standards/
- GRI 2025 Standards: https://www.globalreporting.org/standards/standards-development/
- SASB Standards (under IFRS): https://sasb.ifrs.org/standards/
- TCFD Recommendations: https://www.fsb-tcfd.org/recommendations/
- CDP Climate Disclosure: https://www.cdp.net/en
- Workiva ESG Reporting: https://www.workiva.com/solutions/esg-reporting
- SEC Climate Disclosure Rule (adopted 2024): https://www.sec.gov/news/press-release/2024-31
- EU CSRD ESRS Standards: https://finance.ec.europa.eu/regulation-and-supervision/financial-services-legislation/implementing-and-delegated-acts/corporate-sustainability-reporting-directive_en
- MSCI ESG Ratings: https://www.msci.com/our-solutions/esg-investing/esg-ratings-climate-search-tool
- Sustainalytics ESG Risk Ratings: https://www.sustainalytics.com/esg-ratings
- S&P Global ESG: https://www.spglobal.com/esg/
- GHG Protocol: https://ghgprotocol.org/
- See `role.md` -> "ESG investor reporting playbook"

## Related skills

- `10k-10q-drafting-workiva` — Item 1A climate risk + Item 7 MD&A integration.
- `ir-website-q4-notified` — ESG hub posting.
- `proxy-statement-drafting` — ESG governance disclosures.
- `quarterly-board-letter` — ESG progress narrative.
- `investor-day-capital-markets-day` — long-range ESG framework.
