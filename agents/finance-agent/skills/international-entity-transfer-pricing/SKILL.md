<!--
Source: https://basefirma.com/transfer-pricing-for-start-ups-and-international-expansions/
Source: https://kruzeconsulting.com/blog/transfer-pricing/
Source: https://www.footholdamerica.com/blog/planning-your-2026-us-expansion-essential-checklist-for-international-businesses/
Reference role.md: "International + transfer pricing playbook"
-->

# International entity + transfer pricing — startup playbook

Entity decision tree (subsidiary vs branch vs contractor) + transfer pricing (arm's-length principle for intra-group goods/services/IP/financing). SOTA implementers: Stripe Atlas (entity formation), Foothold America (US expansion for international cos), Stripe/Tipalti (intra-group payments), Avalara (transfer pricing module), BaseFirma / Valentiam / PKF Littlejohn (transfer pricing consultants).

## When to use

- International expansion planning (UK/EU/APAC launch).
- Pre-Series B prep: setting up parent-sub structure for global ops.
- IP transfer to holdco for licensing optimization.
- Annual transfer pricing study refresh.
- Trigger phrases: "international expansion", "transfer pricing", "subsidiary vs branch", "intra-group", "Stripe Atlas", "foothold America", "arm's-length", "UK entity", "DE entity".

NOT for: FX hedging (use `fx-hedging-strategies`); domestic-only tax (use `tax-strategy-qsbs-rd-credit-holdco`).

## Setup

```bash
uvx --with pandas python -c "import pandas"

# Stripe Atlas (US entity for non-US founders; $500 + state fees)
# https://stripe.com/atlas

# Foothold America (US expansion for international cos)
# https://www.footholdamerica.com

# Transfer pricing consultants:
# BaseFirma, Valentiam, PKF Littlejohn, KPMG, Big-4
```

## Entity decision tree

```
NO LOCAL PRESENCE NEEDED (test market, < 6mo)
  → CONTRACTOR / PEO (Deel, Remote, Oyster, Velocity Global)
  Pros: Zero entity setup; payroll handled
  Cons: ~10-15% premium; not for permanent operations
  Tax: No PE (permanent establishment) trigger if structured right

LOCAL PRESENCE NEEDED (operating, 6-24mo)
  → BRANCH OFFICE
  Pros: Quick setup; parent absorbs tax
  Cons: Parent taxed on branch profits; double-tax risk
  Tax: Treated as extension of parent

LONG-TERM OPERATION (>24mo, employees, sales contracts)
  → SUBSIDIARY (independent entity)
  Pros: Limited liability; local tax efficiency; clean exit
  Cons: Setup cost + annual compliance ($5K-$50K depending on jurisdiction)
  Tax: Independent; transfer pricing studies required for cross-border flows
```

## Common entity formation costs (2026)

```
Delaware C-corp (USA):  $250-$500 + Stripe Atlas $500 + Foothold America $X
UK Ltd (Companies House): £12 + ~$1K-$3K annual compliance
Ireland Ltd:             €50 + ~$3K-$5K annual
Germany GmbH:            €25K equity + ~$5K-$10K annual
Netherlands BV:          ~€2-5K + ~$3K-$5K annual
Singapore Pte Ltd:       SGD 300 + ~$2K-$5K annual + nominee director
Hong Kong Ltd:           HKD 2K + ~$2K-$4K annual + nominee director
Australia Pty Ltd:       AUD 500 + ~$2K-$4K annual + ASIC dir
```

## Transfer pricing — arm's-length principle (ALP)

```
INTRA-GROUP TRANSACTIONS REQUIRING TP STUDY:
  1. Goods sale (parent → sub)
  2. Services (R&D from parent; sales/marketing from sub)
  3. IP license (parent IP → sub royalty)
  4. Cost-sharing arrangements
  5. Intra-group financing (parent loan → sub interest)

METHODS (OECD Transfer Pricing Guidelines):
  - CUP (Comparable Uncontrolled Price) — direct comp
  - Cost Plus — base cost + arm's-length markup
  - Resale Price — sub resale - arm's-length margin
  - TNMM (Transactional Net Margin) — net margin benchmark
  - Profit Split — for highly integrated value chains

ALP DOCUMENTATION REQUIREMENTS:
  - Functional analysis (who does what; who owns IP)
  - Benchmarking study (comparable transactions)
  - Inter-company agreement (signed contract)
  - Annual update at minimum
  - Country-by-country reporting if >€750M consolidated revenue (large startups)
```

## Common recipes

### Recipe 1 — Entity recommendation logic

```python
def entity_recommendation(duration_months, headcount, revenue_local, sales_contracts):
    if duration_months < 6 and headcount < 3 and not sales_contracts:
        return "CONTRACTOR / PEO (Deel/Remote/Oyster)"
    if duration_months < 24 and headcount < 5:
        return "BRANCH OFFICE"
    if duration_months >= 24 or headcount >= 5 or sales_contracts or revenue_local > 500_000:
        return "SUBSIDIARY (incorporate locally)"
    return "EVALUATE — consult tax counsel"

print(entity_recommendation(36, 8, 1_200_000, True))
```

### Recipe 2 — Cost-plus markup calculation

```python
def cost_plus_markup(base_cost, target_markup_pct, peer_markups=None):
    """Service company sub charges parent on cost-plus basis."""
    fee = base_cost * (1 + target_markup_pct)
    return {"base_cost": base_cost, "markup_pct": target_markup_pct, "fee_to_parent": fee}

# UK sales sub charges US parent for sales services: 8% cost-plus markup (typical SaaS)
print(cost_plus_markup(2_500_000, 0.08))
```

### Recipe 3 — IP royalty rate determination

```python
def ip_royalty_rate(industry, ip_type, comparables=None):
    """Typical SaaS IP royalty rates per Profit Indicator method."""
    rates = {
        "SaaS_brand":        (0.05, 0.10),
        "SaaS_software":     (0.08, 0.15),
        "SaaS_proprietary_algo": (0.10, 0.25),
        "Pharma_compound":   (0.10, 0.25),
        "Consumer_brand":    (0.02, 0.08),
    }
    low, high = rates.get(f"{industry}_{ip_type}", (0.05, 0.15))
    return {"royalty_rate_low": low, "royalty_rate_high": high, "midpoint": (low + high) / 2}

print(ip_royalty_rate("SaaS", "software"))
```

### Recipe 4 — Intra-group loan pricing

```python
def intra_group_loan_pricing(parent_rating, term_years, base_rate):
    """Arm's-length interest rate on parent → sub loan."""
    # Spread by parent creditworthiness
    spreads = {"AAA": 0.005, "AA": 0.010, "A": 0.020, "BBB": 0.035, "BB": 0.060}
    spread = spreads.get(parent_rating, 0.040)
    # Term premium
    term_premium = term_years * 0.0015
    return base_rate + spread + term_premium

# 5yr USD intra-group loan; parent BB-rated; UST 5yr = 4%
print(intra_group_loan_pricing("BB", 5, 0.04))
```

### Recipe 5 — Functional analysis template

```python
def functional_analysis(entity_name, functions, risks, assets, people):
    """Required for TP documentation."""
    return {
        "entity": entity_name,
        "key_functions": functions,
        "key_risks": risks,
        "significant_assets": assets,
        "key_people": people,
        "remuneration_basis": (
            "Cost plus" if "service" in functions else
            "Profit split" if "IP development" in functions else
            "Resale price" if "distribution" in functions else
            "TNMM (default)"
        )
    }

print(functional_analysis(
    entity_name="Acme UK Ltd",
    functions=["sales", "customer success", "post-sale service"],
    risks=["credit risk on UK customers", "currency risk GBP/USD"],
    assets=["customer relationships", "UK office equipment"],
    people=["UK Country Manager + 5 AEs + 3 CSMs"]
))
```

### Recipe 6 — Permanent Establishment (PE) trigger check

```python
def pe_trigger_check(local_employees, local_office, local_sales_contracts, local_inventory, treaty_country):
    """Most-favored-treaty default: PE triggered if any 'Fixed Place of Business'.
    Excludes: storage, preparatory, auxiliary."""
    triggers = []
    if local_office: triggers.append("Fixed office")
    if local_employees and any(e["role"] in ["Sales", "Mgmt", "Engineering"] for e in local_employees):
        triggers.append("Dependent agents")
    if local_sales_contracts: triggers.append("Authority to conclude contracts")
    if local_inventory: triggers.append("Inventory storage (beyond aux/prep)")
    return {"PE_likely": len(triggers) > 0, "triggers": triggers,
            "implication": "Local corp tax filing required" if triggers else "No local filing"}

print(pe_trigger_check(
    local_employees=[{"role": "Sales", "name": "UK AE"}],
    local_office=True, local_sales_contracts=True, local_inventory=False, treaty_country="UK"
))
```

### Recipe 7 — Stripe Atlas + UK + DE expansion playbook

```
US Holdco + UK + DE OpCo (typical SaaS Series B):

Step 1 (Month 1): Existing US Delaware C-corp = Holdco
Step 2 (Month 1-2): Stripe Atlas — incorporate UK Ltd; assign US holdco as 100% shareholder
Step 3 (Month 2-3): Incorporate DE GmbH; €25K equity contribution from US holdco
Step 4 (Month 3): Inter-company services agreement: US holdco → UK Ltd (cost-plus 8%); DE GmbH → UK Ltd
Step 5 (Month 3): IP licensing agreement: US holdco licenses to UK Ltd (royalty 10% of local revenue) and DE GmbH (royalty 10%)
Step 6 (Month 4): Engage BaseFirma / Valentiam for TP study; documentation by Q4 close
Step 7 (Ongoing): Annual TP refresh; benchmarking study every 2-3 years
```

### Recipe 8 — TP study documentation checklist

```
TP study should include:
  □ Functional analysis (each entity: functions, risks, assets, people)
  □ Benchmarking study (peer companies; OECD-approved methods)
  □ Inter-company agreements (signed before transactions occur)
  □ Pricing memo (justification for chosen method + markup)
  □ Country-by-country reporting (if applicable; >€750M consolidated)
  □ Annual update / refresh

Engaged provider responsibilities:
  □ Benchmarking using paid databases (Compustat, Orbis, ktMine)
  □ Functional analysis interviews
  □ OECD-compliant documentation packs
  □ Filing assistance (IRS Form 8975, local equivalents)
```

### Recipe 9 — Tax-treaty optimization (US-UK example)

```python
def tax_treaty_optimization(parent_jurisdiction, sub_jurisdiction, payment_type):
    """Typical withholding rates under common treaties."""
    rates = {
        ("US", "UK"): {"dividends": 0.05, "royalties": 0.0, "interest": 0.0},  # US-UK treaty
        ("US", "Ireland"): {"dividends": 0.05, "royalties": 0.0, "interest": 0.0},
        ("US", "Singapore"): {"dividends": 0.05, "royalties": 0.0, "interest": 0.0},
        ("US", "Germany"): {"dividends": 0.05, "royalties": 0.0, "interest": 0.0},
        ("US", "Canada"): {"dividends": 0.05, "royalties": 0.0, "interest": 0.10},
    }
    return rates.get((parent_jurisdiction, sub_jurisdiction), {}).get(payment_type)

# US holdco → UK Ltd royalty
print(tax_treaty_optimization("US", "UK", "royalties"))  # 0% — favorable
```

## Examples

### Example 1: US SaaS launching UK + DE

**Goal:** Set up entity + TP structure.

**Steps:**
1. Recipe 1 → SUBSIDIARY (long-term ops).
2. Recipe 7 → Stripe Atlas UK + GmbH formation.
3. Recipe 5 → functional analysis per entity.
4. Recipe 2-3 → cost-plus markup for services + royalty rate for IP.
5. Recipe 9 → tax-treaty withholding rates.
6. Engage BaseFirma / Valentiam for benchmarking study.
7. Sign inter-company agreements BEFORE transactions begin.

**Result:** Compliant US-UK-DE structure; aggregate effective tax rate optimized.

### Example 2: PE risk reduction for contractor model

**Goal:** Test "UK contractor + US sales" without triggering PE.

**Steps:**
1. Recipe 6 → PE trigger check.
2. Structure: UK contractor receives sales commissions; no authority to bind contracts; works from home.
3. All contract conclusion done from US.
4. Confirm "preparatory or auxiliary" exception applies.
5. Document boundaries; refresh annually.

**Result:** UK presence without UK corp tax filing (until contractor role expands).

## Edge cases / gotchas

- **PE trigger is low-bar in some jurisdictions.** France, Italy, Spain aggressive on PE; UK/Ireland more business-friendly.
- **Cost-plus markup ranges.** OECD typical 3-10% for low-risk services; SaaS sales sub typical 5-8%; software dev typical 5-10%.
- **IP royalty 10%+ attracts scrutiny.** Defensible if benchmarked; otherwise IRS / HMRC challenges.
- **Stripe Atlas $500 doesn't include local compliance.** Annual filings + nominee director (Singapore/HK) extra.
- **Intra-group loans need formal documentation.** Without signed loan agreement + interest paid, may be reclassified as equity.
- **CFC (Controlled Foreign Corporation) rules.** US Subpart F + GILTI may include UK/DE/etc. sub income in US parent's tax. Plan w/ tax counsel.
- **Country-by-Country Reporting (CbCR).** Only at €750M+ consolidated; not relevant for most startups.
- **Treaty shopping is policed.** Structuring through Ireland / Netherlands purely for tax = scrutinized.
- **Pillar 2 (15% global minimum tax).** Applies to MNE groups with €750M+ revenue; startups under threshold.
- **Local director / shareholder requirements.** Singapore, HK, UAE require local director / agent. Adds annual fees.
- **DEPP (Diverted Profits Penalty) UK.** Aggressive transfer pricing in UK = 25% penalty + interest.
- **TP study cost.** $25K-$100K initial; $5K-$25K annual refresh.
- **Inter-company agreements must be SIGNED BEFORE TRANSACTIONS.** Backdating is fraud + audit risk.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions. International entity formation + transfer pricing requires licensed legal counsel (local jurisdiction) + licensed CPA / tax attorney sign-off. Defer all binding decisions accordingly.**

## Sources

- BaseFirma TP for startups: https://basefirma.com/transfer-pricing-for-start-ups-and-international-expansions/
- Kruze TP guide: https://kruzeconsulting.com/blog/transfer-pricing/
- Foothold America 2026 US expansion: https://www.footholdamerica.com/blog/planning-your-2026-us-expansion-essential-checklist-for-international-businesses/
- OECD TP Guidelines: https://www.oecd.org/tax/transfer-pricing/
- IRS TP center: https://www.irs.gov/businesses/corporations/transfer-pricing
- Stripe Atlas: https://stripe.com/atlas
- Deel: https://www.deel.com
- Remote: https://remote.com

## Related skills

- `tax-strategy-qsbs-rd-credit-holdco` — holdco for IP transfer.
- `fx-hedging-strategies` — currency exposure from intl entities.
- `capital-structure-debt-equity-mix-stage` — intra-group financing.
- `m-a-target-screen-and-qoe` — cross-border M&A structuring.
