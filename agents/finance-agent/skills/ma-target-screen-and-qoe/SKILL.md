<!--
Source: https://finsider.ai/blog/ma-software-tools/
Source: https://anderscpa.com/learn/blog/quality-of-earnings-report-analysis-due-diligence-guide/
Source: https://otio.ai/blog/crunchbase-vs-pitchbook
Source: https://otio.ai/blog/cb-insights-vs-pitchbook
Reference role.md: "M&A target screen playbook"
-->

# M&A target screen + Quality of Earnings (QoE) pre-work

Combines Bain/McKinsey-grade target screening with Finsider-style automated QoE pre-work. 2026 SOTA: Finsider auto-QoE (74-point GL scan, 95% material-issue catch vs 65% manual, 60% faster). QoE cost $20K-$75K mid-market, 3-6 weeks via EisnerAmper / Anders / Bridgepoint / BDO / RSM. Sell-side QoE now standard for all but smallest deals.

## When to use

- Build vs buy strategic decision triggered (target M&A as alternative).
- Acquirer side: screen candidates, compute valuation, prepare LOI economics.
- Sell-side: prepare own books for QoE before going to market.
- Pre-IOI diligence to triangulate seller-claimed financials.
- Trigger phrases: "M&A", "acquisition target", "QoE", "quality of earnings", "buy-side diligence", "sell-side prep", "target screen", "acquihire".

NOT for: corp-dev partnership analysis (use `strategic-partnership-jv-structuring`); pure capital allocation (use `capital-allocation-framework`).

## Setup

```bash
uvx --with pandas --with numpy --with openpyxl --with requests python -c "import pandas, openpyxl, requests"

# Free fallback (no paywall):
# SEC EDGAR — public-comp financials
export SEC_USER_AGENT="you@example.com"

# Paid (recipient supplies):
export PITCHBOOK_API_KEY="<recipient>"
export CB_INSIGHTS_API_KEY="<recipient>"
export CRUNCHBASE_API_KEY="<recipient; free tier OK>"
export FINSIDER_API_KEY="<recipient — auto-QoE>"
```

## The M&A workflow

```
STAGE 1 — TARGET SCREEN (1-2 weeks)
  Strategic fit + ARR scale fit + valuation reasonability + cultural fit + integration cost
  Output: Short list 3-7 targets ranked

STAGE 2 — INDICATION OF INTEREST (IOI) — 1 week
  Non-binding indicative range based on revenue multiple comp set
  Output: Letter w/ range + diligence asks

STAGE 3 — LIMITED DILIGENCE → LOI (2-4 weeks)
  Phase 1 QoE pre-work; commercial diligence; deep dive on top-1 target
  Output: Letter of Intent (binding to negotiate exclusively)

STAGE 4 — FULL DILIGENCE (6-12 weeks)
  Full QoE (EisnerAmper / Anders / Bridgepoint / BDO / RSM)
  Legal / tax / IT / HR diligence streams
  Output: Diligence report; SPA negotiation

STAGE 5 — CLOSE (2-4 weeks)
  Purchase price adjustment for working capital; final SPA; transaction docs
  Output: Closed deal
```

## Common recipes

### Recipe 1 — Strategic fit screen scorecard

```python
import pandas as pd

CRITERIA = {
    "product_fit":         (0, 5),   # 0-5; 5 = direct complement
    "market_fit":          (0, 5),   # ICP overlap
    "team_fit":            (0, 5),   # talent + culture
    "arr_scale_fit":       (0, 5),   # 5 if 10-30% of acquirer ARR; less if too small or too large
    "valuation_reasonable": (0, 5),  # vs comp set
    "integration_cost":    (0, 5),   # 5 = low cost
    "differentiation_moat": (0, 5),  # IP, customer base
}

def score_target(target, weights=None):
    weights = weights or {k: 1.0 for k in CRITERIA}
    total = sum(target[k] * weights[k] for k in CRITERIA)
    max_total = sum(5 * weights[k] for k in CRITERIA)
    return total / max_total

targets = pd.DataFrame([
    {"name": "Target A", "product_fit": 5, "market_fit": 4, "team_fit": 4, "arr_scale_fit": 5,
     "valuation_reasonable": 3, "integration_cost": 4, "differentiation_moat": 4},
    {"name": "Target B", "product_fit": 4, "market_fit": 5, "team_fit": 3, "arr_scale_fit": 3,
     "valuation_reasonable": 4, "integration_cost": 5, "differentiation_moat": 3},
])
targets["score"] = targets.apply(lambda r: score_target(r.to_dict()), axis=1)
print(targets.sort_values("score", ascending=False))
```

### Recipe 2 — Revenue-multiple comparable valuation

```python
def comp_valuation(target_arr, peer_multiples):
    """peer_multiples: list of ARR multiples from comp set."""
    import numpy as np
    return {
        "p25": target_arr * np.percentile(peer_multiples, 25),
        "median": target_arr * np.percentile(peer_multiples, 50),
        "p75": target_arr * np.percentile(peer_multiples, 75),
    }

# Recent SaaS M&A multiples 2026: 4-12× ARR depending on growth + margin
print(comp_valuation(target_arr=2_000_000, peer_multiples=[5.2, 6.8, 4.1, 8.5, 7.2, 9.1, 11.0, 5.8]))
```

### Recipe 3 — Pull peer comps from SEC EDGAR

```python
import requests

def edgar_facts(cik, headers=None):
    headers = headers or {"User-Agent": "you@example.com"}
    return requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json", headers=headers).json()

# Public SaaS comp CIKs: Workday 1327811, ServiceNow 1373715, Salesforce 1108524
for cik in [1327811, 1373715, 1108524]:
    f = edgar_facts(cik)
    rev = f["facts"]["us-gaap"].get("Revenues") or f["facts"]["us-gaap"].get("RevenueFromContractWithCustomerExcludingAssessedTax")
    print(cik, [(r["fp"], r["val"]) for r in rev["units"]["USD"][-2:]])
```

### Recipe 4 — DCF for cash-flow-positive targets

```python
def dcf_valuation(fcf_projections, terminal_growth, wacc, terminal_year=5):
    """fcf_projections: list of expected FCF year 1..N."""
    pv = sum(fcf / (1 + wacc) ** (t+1) for t, fcf in enumerate(fcf_projections))
    terminal_fcf = fcf_projections[-1] * (1 + terminal_growth)
    terminal_value = terminal_fcf / (wacc - terminal_growth)
    pv_terminal = terminal_value / (1 + wacc) ** terminal_year
    return {"pv_explicit": pv, "pv_terminal": pv_terminal, "enterprise_value": pv + pv_terminal}

# Cash-positive target: $400K, $600K, $850K, $1.1M, $1.4M FCF; WACC 12%, terminal growth 3%
print(dcf_valuation([400_000, 600_000, 850_000, 1_100_000, 1_400_000], 0.03, 0.12))
```

### Recipe 5 — QoE: GL anomaly scan (Finsider-style)

```python
import pandas as pd

def gl_anomaly_scan(gl_df):
    """gl_df: GL transactions (date, account, amount, vendor, memo)."""
    flags = []

    # 1. Round-number entries (likely estimates / accruals)
    round_threshold = 1000
    round_entries = gl_df[gl_df["amount"].abs() % round_threshold == 0]
    if len(round_entries) > 50:
        flags.append({"flag": "round_number_entries", "count": len(round_entries),
                      "concern": "Possible estimates not properly accrued; investigate"})

    # 2. Period-end clustering (cookie-jar reserves?)
    gl_df["day_of_month"] = pd.to_datetime(gl_df["date"]).dt.day
    last_5_days = gl_df[gl_df["day_of_month"] >= 26]
    pct_last_5 = len(last_5_days) / len(gl_df)
    if pct_last_5 > 0.40:
        flags.append({"flag": "period_end_clustering", "pct": pct_last_5,
                      "concern": "Possible income smoothing; investigate manual JEs"})

    # 3. Concentration: top-5 vendors share of OpEx
    vendor_concentration = gl_df.groupby("vendor")["amount"].sum().abs().sort_values(ascending=False).head(5)
    total_opex = gl_df["amount"].abs().sum()
    top5_pct = vendor_concentration.sum() / total_opex if total_opex else 0
    if top5_pct > 0.60:
        flags.append({"flag": "vendor_concentration", "pct": top5_pct,
                      "concern": "High vendor concentration; renewal/pricing risk"})

    # 4. Related-party transactions
    related = gl_df[gl_df["memo"].str.contains("founder|insider|related", case=False, na=False)]
    if len(related) > 0:
        flags.append({"flag": "related_party", "count": len(related),
                      "concern": "Related-party transactions need separate disclosure"})

    return flags
```

### Recipe 6 — QoE: revenue recognition adjustments

```python
def qoe_revenue_adjustments(reported_revenue, deferred_revenue_change, prepay_revenue, services_one_off):
    """Convert reported revenue → recurring run-rate basis."""
    adjusted = reported_revenue
    # Add back deferred revenue (if reported is cash-basis)
    adjusted += deferred_revenue_change
    # Subtract prepaid / one-off revenue
    adjusted -= prepay_revenue
    # Subtract one-off services revenue
    adjusted -= services_one_off
    return {
        "reported_revenue": reported_revenue,
        "adjusted_recurring_revenue": adjusted,
        "adjustment_pct": (adjusted - reported_revenue) / reported_revenue if reported_revenue else 0
    }
```

### Recipe 7 — Working capital normalization

```python
def working_capital_normalization(actual_wc, peer_wc_median, target_revenue, dso_actual, dpo_actual):
    """Compute working-capital target for purchase-price adjustment."""
    target_wc_pct_of_revenue = peer_wc_median  # e.g. 12-18% for SaaS
    target_wc = target_revenue * target_wc_pct_of_revenue
    deficiency = max(0, target_wc - actual_wc)
    return {
        "target_wc": target_wc,
        "actual_wc": actual_wc,
        "deficiency": deficiency,
        "price_adjustment": -deficiency,  # buyer claws back from purchase price
        "dso_actual": dso_actual,
        "dpo_actual": dpo_actual,
    }
```

### Recipe 8 — Synergy quantification

```python
def synergy_model(revenue_synergies, cost_synergies, one_time_costs, integration_years=3, wacc=0.12):
    """NPV of synergies net of integration costs."""
    cumulative_synergies = []
    for yr in range(1, integration_years + 1):
        ramp = min(1.0, yr / integration_years)
        yr_synergy = (revenue_synergies + cost_synergies) * ramp
        cumulative_synergies.append(yr_synergy / (1 + wacc) ** yr)
    return {
        "pv_synergies": sum(cumulative_synergies),
        "one_time_costs": one_time_costs,
        "net_pv": sum(cumulative_synergies) - one_time_costs
    }

print(synergy_model(revenue_synergies=800_000, cost_synergies=1_200_000, one_time_costs=2_500_000))
```

### Recipe 9 — Sell-side prep checklist

```
QoE-ready preparation (sell-side, 6-12 months before going to market):
  □ Move accounting to accrual basis if cash-basis
  □ Clean up related-party transactions; document
  □ Resolve any audit findings; complete next audit
  □ Document revenue recognition policy (ASC 606)
  □ Document customer contract terms (renewal rates, MSAs)
  □ Document cohort retention with methodology
  □ Document COGS classification (no opex hidden in COGS or vice versa)
  □ Document SBC expense; treatment in EBITDA
  □ Document any one-time / non-recurring items
  □ Document customer concentration (top-10 by ARR)
  □ Document vendor concentration (top-10 by spend)
  □ Document IP ownership + assignment chain (PIIA all employees)
  □ Document open source license inventory (FOSSA / BlackDuck)
  □ Document key person dependency (founder, top-3 engineers, top-3 customers)
```

## Examples

### Example 1: Buy-side screen for tuck-in acquisition

**Goal:** Acquire $2M ARR product for $10-20M.

**Steps:**
1. Recipe 1 → screen 7 candidates; rank.
2. Recipe 2 + 3 → comp valuation per top-3.
3. Recipe 4 → DCF for cash-positive top-1.
4. Recipe 5 + 6 → QoE pre-work on top-1.
5. Recipe 7 → working-capital normalization.
6. Recipe 8 → synergy model.
7. Submit IOI at p25 of comp range; negotiate to median.

**Result:** Defensible LOI economics.

### Example 2: Sell-side prep 9 months out

**Goal:** Prepare own books for QoE.

**Steps:**
1. Recipe 9 → checklist; gap-fill.
2. Recipe 5 → run anomaly scan on own GL; remediate.
3. Recipe 6 → adjust revenue recognition if needed.
4. Engage Big-4 or regional firm for sell-side QoE (Finsider for automated alt).
5. Build CIM (Confidential Information Memorandum) + data room (use `investor-data-room-curation`).

**Result:** QoE-ready posture; commands valuation premium.

## Edge cases / gotchas

- **PitchBook / CB Insights paywall.** $15K-$50K/yr each. Free fallbacks: SEC EDGAR (public), Crunchbase free tier (basic profiles), AngelList Pro ($2K/yr).
- **Comp multiples vary 3-5x.** SaaS M&A multiples 2026: 4-12× ARR; depends heavily on growth + margin + buyer type (strategic > financial). Use stratified comp set.
- **Working-capital adjustments steal value.** Buyer commonly normalizes to peer median; if target undermanaged WC, purchase price adjusts down.
- **70-90% of M&A destroys value (HBR/McKinsey).** Discount synergy estimates; require strategic logic + cultural fit.
- **QoE attestation requires licensed CPA.** Finsider's automated scan is pre-work; final report still EisnerAmper / Anders / etc.
- **Sell-side QoE now table stakes.** No QoE = signal to buyer that seller has something to hide.
- **Cookie-jar reserves (period-end JE clustering)** are #1 QoE finding. Recipe 5 catches these.
- **Related-party transactions.** Founder loans, family-member vendor contracts, intercompany flows. Must disclose; often diligence rabbit-hole.
- **Customer concentration > 20% from one logo = risk.** Many deals priced lower or earnout-structured for this.
- **Founder lock-up (typical 24-36 months post-close).** Material to founder personal economics; often confused for "vesting."
- **NDA before sharing financials.** Even at IOI stage.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions. QoE attestation requires engagement with a licensed CPA firm.**

## Sources

- Finsider M&A software tools 2026: https://finsider.ai/blog/ma-software-tools/
- Anders QoE guide: https://anderscpa.com/learn/blog/quality-of-earnings-report-analysis-due-diligence-guide/
- Crunchbase vs PitchBook 2026: https://otio.ai/blog/crunchbase-vs-pitchbook
- CB Insights vs PitchBook: https://otio.ai/blog/cb-insights-vs-pitchbook
- Windes QoE: https://windes.com/quality-of-earnings-earnings-report/
- HBR M&A failure rate: https://hbr.org/2011/03/the-big-idea-the-new-ma-playbook
- SEC EDGAR API: https://www.sec.gov/edgar/sec-api-documentation
- Bain M&A playbook: https://www.bain.com/insights/topics/mergers-and-acquisitions/

## Related skills

- `capital-allocation-framework` — M&A as one of 4 ladder priorities.
- `three-statement-financial-model-tied` — accretion analysis runs through this.
- `investor-data-room-curation` — sell-side data room.
- `term-sheet-nvca-grade-review` — equity component of M&A consideration.
- `strategic-partnership-jv-structuring` — alternative to acquisition.
