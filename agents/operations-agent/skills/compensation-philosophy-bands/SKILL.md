<!--
Sources: https://www.pave.com/
         https://carta.com/total-comp/
         Pave (11M+ data points), Carta Total Comp (integrated with cap table), Levels.fyi (public eng), Radford/Mercer (enterprise).
-->
# Compensation Philosophy + Bands — SKILL

Author a compensation philosophy doc, build role × geo × stage bands, pull market data from Pave / Carta Total Comp / Levels.fyi, model offer letters, and run compensation review cycles. Includes pay-transparency compliance scaffolding for CA SB1162, NY pay transparency, CO Equal Pay Act, WA, MD, RI, IL.

## When to use

- Drafting or refreshing the **compensation philosophy** (50th / 60th / 75th percentile target, geo tiers, equity philosophy).
- Building **comp bands** per role × geo × stage (typically a 4-7 level career framework × 3-4 geo tiers).
- Modeling an **offer** (base + equity + signing).
- Running a **comp review cycle** (annual / semi-annual + promotion path).
- Trigger phrases: "comp band", "salary band", "comp philosophy", "level framework", "geo tier", "offer letter math", "merit cycle", "pay equity audit".

## Setup

```bash
export PAVE_API_KEY="xxx"           # https://pave.com — paid, ~$30k+/yr
export CARTA_API_KEY="xxx"          # https://carta.com — Total Comp module
export LEVELS_FYI_TOKEN="xxx"       # public crowdsource (eng) — fallback
export RADFORD_TOKEN="xxx"          # enterprise market data via Aon Radford
```

Tier notes:
- **Pave** — best live market data; 11M+ data points; paid platform.
- **Carta Total Comp** — best if already on Carta cap table; integrated.
- **Levels.fyi** — public, free for engineering; weak for non-engineering roles.
- **Radford / Mercer** — enterprise; multi-$10k licenses.

## Common recipes

### Recipe 1: Pull market median for a role/level/geo (Pave)
```bash
curl -s "https://api.pave.com/v1/benchmarks" \
  -H "Authorization: Bearer $PAVE_API_KEY" \
  --data-urlencode "role=Senior Software Engineer" \
  --data-urlencode "level=L4" \
  --data-urlencode "geo=US-NYC" \
  --data-urlencode "stage=Series B" \
  --data-urlencode "company_size=100-249" \
  | jq '{base_p50, base_p75, equity_p50, total_p50, total_p75}'
```

### Recipe 2: Geo tier table template
```yaml
# Geo tier model — discount vs SF/NYC anchor
tier_a:        # SF Bay, NYC
  multiplier: 1.00
  cities: [San Francisco, New York City, Seattle]
tier_b:        # Major US metros
  multiplier: 0.92
  cities: [Boston, Los Angeles, Washington DC, Chicago, Austin, Denver]
tier_c:        # Other US
  multiplier: 0.85
  cities: [Atlanta, Phoenix, Portland, Nashville, Pittsburgh, Salt Lake City]
tier_d:        # Remote US (fully remote, no metro)
  multiplier: 0.85
  cities: [US-Remote]
tier_intl_emea: # EU/UK
  multiplier: 0.75
  cities: [London, Berlin, Amsterdam, Dublin, Paris]
tier_intl_emerging:
  multiplier: 0.55
  cities: [Sofia, Krakow, Lisbon, Bucharest, Mexico City]
```

### Recipe 3: Career framework template (5-level engineering)
```yaml
career_track: engineering_ic
levels:
  L2_associate_eng:
    scope: "Single-issue tasks under close mentorship"
    base_p50_anchor_USD: 135000
    equity_target_USD: 80000
    typical_tenure_years: 0-2
  L3_software_eng:
    scope: "Full features end-to-end with light review"
    base_p50_anchor_USD: 170000
    equity_target_USD: 150000
    typical_tenure_years: 2-4
  L4_senior_eng:
    scope: "Owns a service / area; mentors L2-L3"
    base_p50_anchor_USD: 205000
    equity_target_USD: 280000
    typical_tenure_years: 4-7
  L5_staff_eng:
    scope: "Multi-team initiatives; defines technical strategy"
    base_p50_anchor_USD: 250000
    equity_target_USD: 500000
    typical_tenure_years: 7+
  L6_principal_eng:
    scope: "Org-wide leverage; sets multi-quarter direction"
    base_p50_anchor_USD: 300000
    equity_target_USD: 900000
    typical_tenure_years: 10+
```

### Recipe 4: Offer letter math (Python)
```python
# Compute offer for a candidate hitting L4 in NYC
LEVEL = {'L2':135000,'L3':170000,'L4':205000,'L5':250000,'L6':300000}
GEO = {'A':1.0,'B':0.92,'C':0.85,'D':0.85,'EMEA':0.75,'EMRG':0.55}
EQUITY = {'L2':80000,'L3':150000,'L4':280000,'L5':500000,'L6':900000}

def make_offer(level, geo_tier, percentile=0.5, vest='4y/1y cliff'):
    base_anchor = LEVEL[level]
    # apply percentile scaling (50th = anchor, 75th = +12%)
    percentile_mult = 1.0 + (percentile - 0.5) * 0.24
    base = round(base_anchor * GEO[geo_tier] * percentile_mult / 1000) * 1000
    equity_USD = round(EQUITY[level] * GEO[geo_tier] / 1000) * 1000
    return {
        'base_USD': base,
        'equity_USD_grant': equity_USD,
        'equity_vest': vest,
        'signing_bonus_USD': round(base * 0.05 / 1000) * 1000,  # 5% of base
        'target_total_USD': base + equity_USD / 4,
    }

print(make_offer('L4','A', percentile=0.6))
```

### Recipe 5: Levels.fyi spot check (free)
```bash
# Fallback when no Pave/Carta access — eng-only
curl -s "https://www.levels.fyi/m/level/?company=stripe&track=Software+Engineer&level=L4&location=New+York%2C+NY" \
  | grep -oP '"baseSalary":\K[0-9]+' | head
```

### Recipe 6: Carta Total Comp pull
```bash
curl -s "https://api.carta.com/v1/total_comp/benchmarks" \
  -H "Authorization: Bearer $CARTA_API_KEY" \
  --data-urlencode "role=Senior Operations Analyst" \
  --data-urlencode "geo=US-NYC" \
  --data-urlencode "stage=Series B"
```

### Recipe 7: Compensation philosophy doc (skeleton)
```markdown
# Compensation Philosophy — [Co]

## Our targets
- **Cash base:** 50th percentile of relevant market (Pave Series B comparison set).
- **Equity:** 60th percentile of relevant market.
- **Total comp:** at the upper half of our peer band.

## Geo policy
- Pay = role anchor × geo tier multiplier (Recipe 2).
- One-time geo change: salary adjusts at next review (or immediately for moves > 1 tier).
- WFA: tier follows residence-on-file, true-up by 1% annually.

## Equity policy
- Standard grant: 4 years / 1 year cliff / monthly thereafter.
- ISO vs NSO defaults per US tax code; non-US equivalents per country.
- Refresh grants: at promotion, year 2.5 mark, exceptional performance.

## Promotion + merit
- Annual review window: H1.
- Mid-cycle promotion: only for clear scope change.
- Merit budget: 3-4% of payroll; promotion budget separate.

## Pay transparency
- We share band ranges in all job postings (CA SB1162, NY, CO, WA, MD, RI, IL).
- Internal: band visible to all employees in [Notion page].

## Defer to legal-counsel
- Equity exercise terms, 409A valuation, employee vs contractor classification, pay-equity audit conclusions.
```

### Recipe 8: Comp review cycle (Lattice Compensation)
```bash
curl -s -X POST "https://api.latticehq.com/v1/compensation_cycles" \
  -H "Authorization: Bearer $LATTICE_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"2026 Annual Merit + Promotion",
    "open_date":"2026-11-01",
    "close_date":"2026-11-30",
    "budget_pool_USD":850000,
    "budget_split":{"merit":0.7,"promotion":0.25,"equity":0.05},
    "manager_allocation":true,
    "calibration_required":true
  }'
```

### Recipe 9: Pay equity audit (Python)
```python
# Detect statistical pay gaps by protected class controlling for role, level, tenure, geo
# (Stat sig at 95%; do NOT publish raw without legal review.)
import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_csv('comp_export.csv')  # base, equity, role, level, geo, tenure_yrs, gender, race
model = smf.ols('base ~ C(role) + C(level) + C(geo) + tenure_yrs + C(gender) + C(race)', data=df).fit()
print(model.summary())
# Inspect C(gender)[T.Female] coefficient + p-value. Negative + p<0.05 → likely gap.
# Defer to legal-counsel before publishing or acting on results.
```

### Recipe 10: Job posting band insertion (multi-state)
```python
# Auto-insert salary band on Greenhouse public job post per Recipe 2 + role band
def post_with_band(job_id, level, geos):
    bands = []
    for g in geos:
        base = LEVEL[level] * GEO[g] * 0.88
        max_ = LEVEL[level] * GEO[g] * 1.12
        bands.append(f"{g}: ${base:,.0f}-${max_:,.0f}")
    band_block = "Salary range (varies by location): " + " · ".join(bands)
    # PATCH Greenhouse job description appending band_block
```

## Examples

### Example 1: Stand up a comp philosophy + bands for 50-person Series B
**Goal:** Documented philosophy + 5-level eng + 4-level ops bands × 4 geo tiers in 2 weeks.
**Steps:**
1. Recipe 7: draft philosophy doc → Notion `/People/Compensation/Philosophy`.
2. Recipes 1 + 6: pull Pave + Carta medians for 9 anchor role/level pairs.
3. Recipe 3: career framework (eng) + ops/sales/G&A parallels.
4. Recipe 2: geo tier multipliers.
5. Build full bands grid in `xlsx` skill.
6. Recipe 10: backfill open job posts with bands (CA/NY/CO mandatory).
7. Publish to Notion (internal) + share with all managers.

**Result:** Recruiter has bands to quote; managers can answer comp questions consistently; ready for compliance audit.

### Example 2: Annual merit cycle
**Goal:** Run 2026 merit + promotion cycle with $850k pool.
**Steps:**
1. Recipe 8: open Lattice comp cycle.
2. Manager allocations → calibration session by team lead.
3. Validate against bands (no above-max without exception approval).
4. Generate letters via `docx` template (Recipe 4 math).
5. Push final comp to Gusto / Rippling via payroll skill.

**Result:** Documented merit cycle with pay-equity audit ready.

## Edge cases / gotchas

- **Market data lag.** Pave / Carta data is 3-6 months trailing. Build in a +4-6% inflation buffer for hot roles.
- **75th-percentile cash policy backfires.** Burns cash; if you can't sustain it, target 50th cash + 75th equity instead.
- **Geo tier moves.** A → C move = pay cut; B → A move = raise. Policy must specify which direction is automatic vs review-gated.
- **Refresh grant under-budgeting.** A 4-year initial grant decays to ~0 by year 3.5; without refresh policy, retention drops sharply. Budget refresh = 25-50% of initial grant at year 2.5.
- **Pay transparency law expansion.** CA SB1162, NY pay transparency, CO Equal Pay Act, WA, MD, RI, IL all require band disclosure on listings. Recipe 10 covers this. **Defer to `legal-counsel` for state-specific posting language.**
- **Pay equity audit findings.** Don't act on Recipe 9 results without legal review (privilege, remediation strategy, statute of limitations). **Defer to `legal-counsel`.**
- **Contractor vs employee classification.** Don't put 1099 contractors on employee bands; misclassification risk (CA AB5, FLSA). **Defer to `legal-counsel`.**
- **Equity refresh on flat round / down round.** Strike-price reset is not automatic; if 409A drops, prior options are still at old strike. Refresh grants help.
- **PEPM cycles where market shifts.** Mid-cycle banding refresh causes inequity; lock bands at start of cycle and republish annually unless market shifts >10%.
- **Levels.fyi self-reported skew.** Heavily eng-biased and self-reported high; use as floor sanity check, not source of truth.
- **EU CSRD pay-gap reporting (1000+ employees, expanding).** Disclosure starts FY2026 reports. **Defer to `legal-counsel`.**

## Sources

- Pave: https://www.pave.com/
- Carta Total Comp: https://carta.com/total-comp/
- Levels.fyi: https://www.levels.fyi/
- Radford (Aon): https://radford.aon.com/
- CA SB1162 (Pay transparency): https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202120220SB1162
- NY Pay Transparency Law: https://dol.ny.gov/pay-transparency
- CO Equal Pay Act: https://cdle.colorado.gov/dlss/equal-pay-for-equal-work-act-implementation
- Lattice Compensation: https://lattice.com/library/compensation
