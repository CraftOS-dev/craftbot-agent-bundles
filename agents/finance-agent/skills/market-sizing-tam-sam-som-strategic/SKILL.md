<!--
Source: https://waveup.com/blog/tam-sam-som/
Source: https://qubit.capital/blog/bottom-up-market-sizing
Source: https://otio.ai/blog/crunchbase-vs-pitchbook
Reference role.md: "Market sizing playbook"
-->

# Market sizing — TAM / SAM / SOM (strategic, not just sales)

Computes defensible market sizing for pitch deck / strategic plan / board / M&A use. 2026 standard: lead with bottom-up (ICP-fitting accounts × realistic ACV); triangulate with top-down (industry reports × SAM%). Carta 2025 data: founders presenting both close 40% faster. TAM for context; SAM for strategy; SOM for the 3-year plan.

## When to use

- Pitch deck slide 4-6 (Market section).
- Board strategic plan annual refresh.
- New product / new geography expansion case.
- M&A target screen — what's the addressable market of the combined entity.
- Trigger phrases: "TAM", "SAM", "SOM", "market sizing", "addressable market", "bottom-up TAM", "ICP × ACV".

NOT for: revenue forecast (use `driver-based-revenue-modeling`); competitor landscape (separate research task).

## Setup

```bash
uvx --with pandas --with numpy --with requests python -c "import pandas, requests"

# SEC EDGAR (free; for peer revenue triangulation)
# Public; no key
curl -s "https://data.sec.gov/submissions/CIK0001318605.json" -H "User-Agent: yourname@example.com"

# Crunchbase (paid for full data; free for basic)
export CRUNCHBASE_API_KEY="<from Crunchbase API>"

# PitchBook / CB Insights (paid; recipient supplies)
export PITCHBOOK_API_KEY="<recipient supplies>"
```

## The framework

```
TAM (Total Addressable Market)
  Total demand if 100% of market bought your category, in your geos.
  Usually huge ($10B+); used for context only.

SAM (Serviceable Addressable Market)
  TAM × (your ICP fit × geographies you sell in × tier you serve)
  Realistic ceiling at your current product + GTM.

SOM (Serviceable Obtainable Market)
  SAM × (3-year market share you can plausibly capture)
  Equals 3-year revenue plan.
```

### Three methods (use ALL THREE; triangulate)

```
1. BOTTOM-UP (PRIMARY — most defensible)
   N accounts in ICP × Avg ACV × penetration%

2. TOP-DOWN (TRIANGULATION)
   Industry report total spend × your category share %

3. VALUE-THEORY
   Customer pain × willingness to pay × population suffering pain
   (For category-creating startups where no industry report exists.)
```

## Common recipes

### Recipe 1 — Bottom-up TAM (ICP × ACV)

```python
def bottom_up_tam(icp_accounts, avg_acv):
    return icp_accounts * avg_acv

# Example: US mid-market SaaS, 250-2,500 employees, finance teams
# US Census: ~94,000 US firms in 250-2,499 employee band
# Industry: ~70% have finance team (rest outsource); ~50% in target verticals
icp_us = 94_000 * 0.70 * 0.50
avg_acv = 32_000
tam = bottom_up_tam(icp_us, avg_acv)
print(f"Bottom-up US TAM: ${tam/1e9:.2f}B")
```

### Recipe 2 — Pull peer revenues from SEC EDGAR

```python
import requests

def edgar_company_facts(cik, headers={"User-Agent": "you@example.com"}):
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
    return requests.get(url, headers=headers).json()

# Example: Workday CIK 0001327811
data = edgar_company_facts(1327811)
revenues = data["facts"]["us-gaap"]["Revenues"]["units"]["USD"]
# Pick most recent annual
annual = [r for r in revenues if r.get("fp") == "FY"]
print(annual[-1])
```

### Recipe 3 — Top-down triangulation

```python
def top_down_sam(industry_total_spend, your_category_share):
    return industry_total_spend * your_category_share

# Industry: "US enterprise software" Gartner 2025 = $720B
# Your category: "AI finance ops" = ~0.4% of enterprise software
sam_top = top_down_sam(720e9, 0.004)
print(f"Top-down SAM: ${sam_top/1e9:.2f}B")
```

### Recipe 4 — Bottom-up vs top-down triangulation

```python
def triangulate(bottom_up, top_down, tolerance=0.30):
    delta = abs(bottom_up - top_down) / max(bottom_up, top_down)
    return {
        "bottom_up": bottom_up,
        "top_down": top_down,
        "delta_pct": delta,
        "converged": delta < tolerance,
        "midpoint": (bottom_up + top_down) / 2
    }

# Bottom-up SAM $2.1B; top-down SAM $2.9B → 28% delta → converged
print(triangulate(2.1e9, 2.9e9))
```

### Recipe 5 — SOM (3-year plan)

```python
def som_3yr(sam, yr1_share, yr2_share, yr3_share, growth_rate):
    """yr3_share: target market share in year 3"""
    yr1_revenue = sam * yr1_share
    yr2_sam = sam * (1 + growth_rate)
    yr2_revenue = yr2_sam * yr2_share
    yr3_sam = yr2_sam * (1 + growth_rate)
    yr3_revenue = yr3_sam * yr3_share
    return {"y1": yr1_revenue, "y2": yr2_revenue, "y3": yr3_revenue, "cagr": (yr3_revenue/yr1_revenue)**(1/2)-1}

# Plausible early-stage: 0.05% → 0.15% → 0.30% share
print(som_3yr(2.5e9, 0.0005, 0.0015, 0.0030, growth_rate=0.12))
```

### Recipe 6 — Segment-decomposed TAM (per ICP tier)

```python
import pandas as pd

segments = pd.DataFrame([
    {"segment": "SMB",        "n_accounts": 850_000, "acv": 6_500, "fit_pct": 0.30},
    {"segment": "Mid-market", "n_accounts": 94_000,  "acv": 32_000, "fit_pct": 0.45},
    {"segment": "Enterprise", "n_accounts": 8_500,   "acv": 180_000, "fit_pct": 0.65},
])
segments["addressable"] = segments["n_accounts"] * segments["fit_pct"] * segments["acv"]
print(segments)
print(f"Total bottom-up TAM: ${segments['addressable'].sum()/1e9:.2f}B")
```

### Recipe 7 — Geographic decomposition

```python
geographies = pd.DataFrame([
    {"geo": "US",     "share_pct": 0.42, "addressable": 8_700e6},
    {"geo": "EU",     "share_pct": 0.28, "addressable": 5_800e6},
    {"geo": "UK",     "share_pct": 0.10, "addressable": 2_100e6},
    {"geo": "APAC",   "share_pct": 0.15, "addressable": 3_100e6},
    {"geo": "RoW",    "share_pct": 0.05, "addressable": 1_000e6},
])
print(geographies)
```

### Recipe 8 — Census / industry report fetch (US)

```bash
# US Census Statistics of US Businesses (SUSB) — establishments by employee size
curl -s "https://api.census.gov/data/2021/cbp?get=ESTAB,NAICS2017_LABEL,EMPSZES_LABEL&for=us:*&NAICS2017=541511&EMPSZES=212" \
  -H "Accept: application/json"
# NAICS 541511 = Custom Computer Programming; EMPSZES 212 = 250-499 employees
```

### Recipe 9 — Sanity check vs comp revenues

```python
def comp_check(your_sam_estimate, peer_revenues):
    """peer_revenues: list of annual revenue from comp set."""
    peer_total = sum(peer_revenues)
    ratio = peer_total / your_sam_estimate
    return {
        "peer_total_revenue": peer_total,
        "your_sam": your_sam_estimate,
        "peer_share_of_sam": ratio,
        "sanity": "PLAUSIBLE" if 0.05 < ratio < 0.50 else "REVIEW"
    }

# Top 5 comp set: $1.2B / $480M / $190M / $85M / $42M = $1.997B
print(comp_check(your_sam_estimate=5_000_000_000, peer_revenues=[1.2e9, 0.48e9, 0.19e9, 0.085e9, 0.042e9]))
```

## Examples

### Example 1: Pitch deck market slide (Series A)

**Goal:** Defensible TAM/SAM/SOM slide.

**Steps:**
1. Recipe 1 → bottom-up TAM by primary ICP × ACV.
2. Recipe 8 → fetch Census data for ICP account count.
3. Recipe 3 → top-down SAM from industry report.
4. Recipe 4 → triangulate; should converge within 30%.
5. Recipe 5 → SOM 3-year plan tied to revenue forecast.
6. Recipe 9 → sanity check vs peer revenues.

**Result:** Slide that survives investor pushback. Each number traces to a source.

### Example 2: International expansion case (UK + DE)

**Goal:** Size opportunity for UK + DE launch.

**Steps:**
1. Recipe 7 → geo decomposition; UK + DE = 20-30% of global SAM.
2. Recipe 1 → ICP × ACV for UK + DE specifically.
3. Recipe 8 → equivalents: UK ONS, German Destatis for account counts.
4. Recipe 5 → SOM for UK + DE; tie to expansion P&L (use `international-entity-transfer-pricing`).
5. Recipe 9 → sanity check vs local competitors' revenues.

**Result:** Case for UK + DE launch grounded in cohort math.

## Edge cases / gotchas

- **TAM inflation is the #1 deck-killer.** "$100B TAM" without bottom-up backing is an investor red flag. Use $X-50B max, with backing.
- **Triangulation gap > 30%.** Re-check ICP definition or top-down assumption. Don't average wildly different estimates.
- **Industry reports vary by 2-3×.** Gartner vs IDC vs Forrester for the same category. Cite the source explicitly.
- **ACV varies by segment.** Don't use blended ACV against full ICP count; segment decompose.
- **Penetration assumptions.** 100% penetration is unrealistic; even category leaders hold <40%. Cap at 25-40% for SAM.
- **Geographic SAM != Geographic TAM × global%.** US tends to over-index for SaaS adoption; UK / DE lag 2-3 years.
- **SOM > 5% market share in Year 3** = aggressive; investors will discount.
- **Census data lag.** US Census SUSB has 2-3 year lag. Adjust if industry is moving fast.
- **PitchBook / CB Insights paywall.** Free fallbacks: Crunchbase basic, AngelList Pro, SEC EDGAR for public comps.
- **"Bottom-up" with anecdotes ≠ bottom-up.** Need explicit ICP definition + account count source + ACV source.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions.**

## Sources

- WaveUp TAM/SAM/SOM 2026: https://waveup.com/blog/tam-sam-som/
- Qubit bottom-up market sizing: https://qubit.capital/blog/bottom-up-market-sizing
- Crunchbase vs PitchBook 2026: https://otio.ai/blog/crunchbase-vs-pitchbook
- SEC EDGAR API: https://www.sec.gov/edgar/sec-api-documentation
- US Census SUSB: https://www.census.gov/programs-surveys/susb.html
- Crunchbase API: https://data.crunchbase.com/docs
- Carta market data: https://carta.com/data/

## Related skills

- `pitch-deck-financial-slides` — surfaces SOM as 3-year revenue plan.
- `driver-based-revenue-modeling` — bottom-up SOM = revenue forecast input.
- `ma-target-screen-and-qoe` — combined-entity TAM analysis.
- `ltv-cohort-strategic` — segment LTV justifies SAM segmentation.
