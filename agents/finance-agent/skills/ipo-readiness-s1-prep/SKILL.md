<!--
Source: https://www.crosscountry-consulting.com/insights/blog/ipo-readiness-steps-focus-areas/
Source: https://carta.com/learn/startups/exit-strategies/ipo/readiness/
Source: https://www.eisneramper.com/insights/ipo-insights/ipo-readiness-guide/
Reference role.md: "IPO readiness playbook"
-->

# IPO readiness + S-1 prep — 5-dimension framework

Cross Country Consulting / Carta / EisnerAmper / Deloitte playbooks. 2026 standard: 18-24 months pre-IPO start. Five dimensions: financial systems (ERP + close automation), governance + board, internal controls + audit-ready, human capital + comp disclosure (8-category SEC requirement), MD&A drafting + risk factors. Comp analysis via PitchBook + S&P Capital IQ + recent S-1s on SEC EDGAR.

## When to use

- Board approves IPO path; 18-24mo countdown.
- Confidential S-1 drafting (DRS — draft registration statement).
- IPO comp analysis for valuation discussion.
- Direct listing / SPAC alternative evaluation.
- Trigger phrases: "IPO readiness", "S-1 prep", "IPO comp", "DRS", "draft registration", "ICFR", "SOX", "MD&A", "direct listing".

NOT for: M&A exit (use `ma-target-screen-and-qoe`); strategic partnerships (use `strategic-partnership-jv-structuring`).

## Setup

```bash
uvx --with pandas --with numpy --with requests python -c "import pandas, requests"

# SEC EDGAR (free) — recent S-1 comps
export SEC_USER_AGENT="you@example.com"

# Optional paid: PitchBook, S&P Capital IQ
```

## The 5-dimension framework

```
DIMENSION 1 — FINANCIAL SYSTEMS
  • ERP at scale (NetSuite, Sage Intacct, SAP S/4HANA)
  • Close automation (5-7 day close minimum; 3-4 days IPO-grade)
  • Revenue recognition (ASC 606) — automated; auditable
  • SBC accounting (ASC 718) — Carta / Shareworks
  • Lease accounting (ASC 842)
  • Tax provision automation

DIMENSION 2 — GOVERNANCE + BOARD
  • Board composition: ≥3 independent directors; financial expert; audit committee
  • Audit committee: ≥3 independents, all financially literate, ≥1 financial expert (SEC def)
  • Comp committee, nom/gov committee — all independent
  • Board charter, committee charters
  • Insider trading policy
  • Whistleblower hotline

DIMENSION 3 — INTERNAL CONTROLS + AUDIT-READY (SOX)
  • ICFR (Internal Control over Financial Reporting) framework (COSO 2013)
  • Auditor (Big-4 or large regional) engaged ≥18mo pre-IPO
  • Last 3 years GAAP audits (PCAOB standard)
  • SOX 404(a) management assessment readiness Year 1 post-IPO
  • SOX 404(b) external auditor opinion Year 2 post-IPO (or earlier if EGC graduates)

DIMENSION 4 — HUMAN CAPITAL + COMP DISCLOSURE
  • Comp disclosure (CD&A — Compensation Discussion & Analysis)
  • 8 SEC-mandated comp categories: salary, bonus, stock awards, option awards,
    non-equity incentives, pension, other comp, total
  • Pay ratio (CEO vs median employee)
  • Stock-based comp expense (ASC 718) accurate + disclosed

DIMENSION 5 — MD&A + RISK FACTORS
  • MD&A (Management Discussion & Analysis) — 3 years
  • Risk factors — comprehensive; standard ~30-60 risks for SaaS
  • Use of proceeds
  • Dilution + capitalization disclosure
  • Selected historical financials
  • Industry + market data (cite sources)
```

## The S-1 structure (high level)

```
1. Cover Page + Prospectus Summary
2. Risk Factors
3. Use of Proceeds
4. Dividend Policy
5. Capitalization
6. Dilution
7. Selected Financial Data (5yr)
8. MD&A (3yr discussion)
9. Business Description (market + product + GTM)
10. Management (officers, directors)
11. Executive Compensation (CD&A + tables)
12. Certain Relationships + Related-Party Transactions
13. Principal Stockholders
14. Description of Capital Stock
15. Shares Eligible for Future Sale
16. Underwriting
17. Legal Matters
18. Experts (auditor)
19. F-pages: Audited financial statements
20. Exhibits (cap table, employment agreements, key contracts, opinions of counsel)
```

## Common recipes

### Recipe 1 — Readiness scorecard

```python
def ipo_readiness_score(dimensions):
    """dimensions: dict of {dim_name: {item_name: status}}; status ∈ {0,1,2,3}
       0=not started, 1=in progress, 2=ready, 3=audit-tested"""
    out = []
    for dim, items in dimensions.items():
        scores = list(items.values())
        avg = sum(scores) / len(scores) if scores else 0
        out.append({"dimension": dim, "items_total": len(scores),
                    "avg_score": avg, "ready": avg >= 2.0})
    return out

dimensions = {
    "Financial Systems": {"NetSuite_at_scale": 2, "Close_5day": 1, "ASC606_auto": 2, "ASC718_carta": 3},
    "Governance": {"Indep_directors": 1, "Audit_committee": 1, "Comp_committee": 0},
    "Internal Controls": {"ICFR_framework": 0, "Auditor_engaged": 2, "3yr_audits": 2},
    "Human Capital": {"CD&A_drafted": 0, "Pay_ratio_calc": 0},
    "MD&A": {"3yr_MDA": 0, "Risk_factors": 0, "Use_of_proceeds": 0}
}
for r in ipo_readiness_score(dimensions): print(r)
```

### Recipe 2 — Timeline — 24-month plan

```
T-24mo to T-18mo:
  • Big-4 auditor selected; PCAOB-grade audits begin (3yr historicals)
  • CFO / Controller hired (if not already public-grade)
  • Board: add ≥3 independent directors; form audit committee
  • Cap table cleanup (eliminate fragmented holders, simplify pref stack)

T-18mo to T-12mo:
  • ICFR framework documented (COSO 2013)
  • Underwriter beauty contest; engage lead + co-managers
  • Confidential S-1 drafting begins
  • SEC pre-filing communication
  • CFO + IR team scaling

T-12mo to T-6mo:
  • Confidential S-1 submission (DRS — Draft Registration Statement)
  • SEC review (3-5 rounds of comments)
  • Address SEC comments; refile
  • Comp consultant for CD&A
  • Risk factor review w/ counsel

T-6mo to T-3mo:
  • Public S-1 filing
  • SEC effectiveness + roadshow prep
  • Investor education
  • Analyst day

T-3mo to T-0:
  • Roadshow (2 weeks)
  • Pricing meeting (~T-7 days)
  • Pricing call (~T-1 day)
  • IPO date (price + open trading)

T+0 to T+6mo:
  • Lockup period (180 days standard)
  • Quiet period (40 days pre-S-1 effectiveness)
  • SOX 404(a) management assessment

T+12mo to T+24mo:
  • SOX 404(b) external auditor opinion (when EGC graduates)
```

### Recipe 3 — Comp set selection (SEC EDGAR S-1 fetch)

```python
import requests

def fetch_s1(cik, headers=None):
    headers = headers or {"User-Agent": "you@example.com"}
    submissions = requests.get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json", headers=headers).json()
    s1_forms = [f for f in submissions["filings"]["recent"]["form"] if "S-1" in f]
    return s1_forms

# Recent SaaS IPO CIKs (examples): Reddit, Astera Labs, Klaviyo, etc.
# Pull comparable S-1s to study disclosures, multiples, executive comp
```

### Recipe 4 — Revenue multiple at IPO

```python
def ipo_revenue_multiple(comp_set):
    """comp_set: list of {company, ipo_market_cap, ttm_revenue, growth_rate}"""
    import pandas as pd
    df = pd.DataFrame(comp_set)
    df["multiple"] = df["ipo_market_cap"] / df["ttm_revenue"]
    return {
        "median_multiple": df["multiple"].median(),
        "p25": df["multiple"].quantile(0.25),
        "p75": df["multiple"].quantile(0.75),
        "by_company": df
    }

print(ipo_revenue_multiple([
    {"company": "Klaviyo", "ipo_market_cap": 9_200_000_000, "ttm_revenue": 587_000_000, "growth_rate": 0.61},
    {"company": "Reddit", "ipo_market_cap": 6_400_000_000, "ttm_revenue": 804_000_000, "growth_rate": 0.21},
    {"company": "Astera Labs", "ipo_market_cap": 5_500_000_000, "ttm_revenue": 120_000_000, "growth_rate": 1.85},
]))
```

### Recipe 5 — Lockup expiry impact model

```python
def lockup_impact(insider_shares, total_float, lockup_days=180, avg_daily_volume_pct=0.005):
    """Model dilution shock when lockup expires."""
    insider_pct_of_total = insider_shares / (insider_shares + total_float)
    days_to_absorb = insider_shares / (total_float * avg_daily_volume_pct) if total_float else float('inf')
    return {
        "insider_shares": insider_shares,
        "public_float": total_float,
        "insider_pct_of_total": insider_pct_of_total,
        "days_to_absorb_at_avg_volume": days_to_absorb,
        "expected_price_pressure": "HIGH" if days_to_absorb > 100 else "MODERATE"
    }

print(lockup_impact(insider_shares=85_000_000, total_float=24_000_000))
```

### Recipe 6 — CD&A draft helper

```markdown
# Compensation Discussion & Analysis (Outline)

## Compensation Philosophy
[Pay-for-performance; alignment with stockholders; market-competitive]

## Compensation Mix
| Element | CEO | Other NEOs |
|---|---|---|
| Base Salary | 20% | 30% |
| Annual Bonus | 25% | 25% |
| LTI (equity) | 50% | 40% |
| Other / Benefits | 5% | 5% |

## Compensation Tables
- Summary Compensation Table (3yr) — 8 SEC-mandated categories
- Grants of Plan-Based Awards
- Outstanding Equity Awards at FY-End
- Option Exercises and Stock Vested
- Pension Benefits (often N/A for SaaS)
- Non-Qualified Deferred Comp
- Potential Payments upon Termination / CoC

## Pay Ratio
CEO compensation $X,XXX,XXX ÷ Median employee compensation $XXX,XXX = X:1
```

### Recipe 7 — Risk factors — SaaS standard set

```python
SAAS_RISK_FACTORS = {
    "Business + GTM": [
        "Limited operating history",
        "History of losses / future profitability uncertain",
        "Customer concentration",
        "Reliance on key personnel",
        "Competition + new entrants",
        "Failure to maintain NRR / customer retention",
        "Unpredictability of new customer acquisition",
    ],
    "Product + Tech": [
        "Software defects / outages",
        "Cybersecurity incidents",
        "Data privacy (GDPR, CCPA, CPRA)",
        "AI / LLM dependence risks",
        "Open source license risks",
        "Reliance on third-party platforms (AWS, Stripe, etc.)",
    ],
    "Financial": [
        "Need for additional capital",
        "Quarterly revenue volatility",
        "FX risk",
        "Tax (changes in tax law, transfer pricing)",
    ],
    "Regulatory": [
        "Privacy regulations (sector-specific)",
        "Export control + sanctions",
        "Anti-corruption (FCPA)",
        "Section 16 / insider trading",
    ],
    "Corporate Structure": [
        "Dual-class shares (if applicable)",
        "Anti-takeover provisions",
        "Concentrated voting / control",
        "Tax loss carryforwards w/ change-of-control limitations",
    ]
}
```

### Recipe 8 — Direct listing vs SPAC vs traditional IPO comparison

```python
def listing_path_comparison():
    return [
        {"path": "Traditional IPO",  "raise_capital": True,  "underwriting_spread": "5-7%",
         "process_months": "12-18",  "complexity": "HIGH",   "price_stability": "Med"},
        {"path": "Direct listing",   "raise_capital": False, "underwriting_spread": "0%",
         "process_months": "9-12",   "complexity": "MED",    "price_stability": "Low"},
        {"path": "SPAC merger",      "raise_capital": True,  "underwriting_spread": "Sponsor 20%",
         "process_months": "4-6",    "complexity": "LOW",    "price_stability": "Low — post-merger underperformance norm"}
    ]
```

### Recipe 9 — Underwriter selection scorecard

```python
def underwriter_scorecard(banks):
    """banks: list of {name, sector_expertise, recent_deals, distribution_strength, ipo_aftermarket_perf, total_fee_pct}"""
    import pandas as pd
    df = pd.DataFrame(banks)
    df["composite_score"] = (
        df["sector_expertise"] * 0.30 +
        df["distribution_strength"] * 0.30 +
        df["recent_deals"] * 0.20 +
        df["ipo_aftermarket_perf"] * 0.20
    )
    return df.sort_values("composite_score", ascending=False)
```

## Examples

### Example 1: 18-month IPO countdown — Series D SaaS

**Goal:** Drive readiness across 5 dimensions.

**Steps:**
1. Recipe 1 → readiness scorecard; identify red items.
2. Recipe 2 → 18-mo timeline; assign owners.
3. Recipe 3 → comp-set S-1 fetch (5-7 recent SaaS IPOs).
4. Recipe 4 → comp multiple analysis; set valuation expectation.
5. Recipe 6 → CD&A drafting (engage Compensia / Pay Governance).
6. Recipe 7 → risk factors per category.
7. Pre-file confidential S-1 at T-12mo.

**Result:** S-1-ready posture by T-12mo.

### Example 2: Lockup expiry communication

**Goal:** Manage post-IPO Day 181 lockup expiry.

**Steps:**
1. Recipe 5 → model dilution shock; insider sell-down.
2. Plan 10b5-1 plans 90 days pre-expiry.
3. Communicate to top investors + analysts.
4. Consider staggered lockup release for key insiders.

**Result:** Smoother lockup expiry; less price shock.

## Edge cases / gotchas

- **EGC (Emerging Growth Company) status.** <$1.235B revenue → 5yr exemption from SOX 404(b); reduced disclosures. Most SaaS at IPO qualifies. Don't waste EGC benefits.
- **SEC review = 3-5 comment rounds.** Confidential DRS process gives time; build buffer.
- **Auditor lock-up.** Big-4 fee inflation 30-50% per year leading to IPO. Negotiate scope.
- **Cap-table cleanup = months of work.** Many startups have fragmented SAFEs, options, secondaries. Carta / Pulley audit early.
- **Cheap stock adjustment.** Sec 481 may require true-up of SBC if 409A FMV not defensible 12-24mo before IPO. Critical to engage 3rd-party 409A (not just Carta in-house) at T-18mo+.
- **SOX 404(a) is mgmt; 404(b) is auditor.** Big difference in scope + cost. Most EGCs delay 404(b).
- **Direct listing not for capital raises (mostly).** SEC now permits "primary direct listings"; still relatively new (Spotify, Slack, Coinbase, Reddit precursor).
- **SPAC underperforms post-merger.** Average -30% in first 12 months post-merger. Reputation severely diminished post-2022.
- **Lockup expiry = volatility event.** Plan comms + 10b5-1 plans for insiders.
- **Quiet period.** Strict SEC rules on what you can say pre-S-1 effectiveness. Coach all employees.
- **Confidential pre-filing.** Most companies use Confidential DRS (per JOBS Act) — avoids public scrutiny until effectiveness.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions. IPO process requires licensed securities counsel, audit firm, and underwriter sign-off.**

## Sources

- Cross Country Consulting IPO 2026: https://www.crosscountry-consulting.com/insights/blog/ipo-readiness-steps-focus-areas/
- Carta IPO readiness: https://carta.com/learn/startups/exit-strategies/ipo/readiness/
- EisnerAmper IPO readiness guide: https://www.eisneramper.com/insights/ipo-insights/ipo-readiness-guide/
- Deloitte IPO readiness: https://www2.deloitte.com/us/en/pages/audit/articles/ipo-readiness.html
- SEC EDGAR S-1 search: https://www.sec.gov/edgar/searchedgar/companysearch
- SEC JOBS Act EGC: https://www.sec.gov/smallbusiness/goingpublic/EGC
- SOX 404 guidance: https://www.sec.gov/info/smallbus/secg/icfrguide.htm
- COSO 2013 Framework: https://www.coso.org/Pages/default.aspx

## Related skills

- `409a-valuation-negotiation` — cheap stock walk for S-1.
- `equity-comp-design-pool-evergreen` — CD&A drives equity decisions.
- `three-statement-financial-model-tied` — S-1 historicals + MD&A.
- `term-sheet-nvca-grade-review` — preferred conversion at IPO.
- `board-cfo-financial-package` — pre-IPO board updates.
