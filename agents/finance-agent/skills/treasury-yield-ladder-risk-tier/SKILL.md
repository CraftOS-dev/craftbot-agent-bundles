<!--
Source: https://www.rho.co/blog/treasury-management-software
Source: https://www.rho.co/blog/guide-to-t-bill-ladders
Source: https://yieldalley.com/t-bill-ladder-how-to-build-one/
Reference role.md: "Treasury yield ladder playbook"
-->

# Treasury yield ladder — three-tier risk allocation

Builds the multi-tier treasury structure that became standard post-SVB collapse: Operating (6-8 wks of outflows; HYSA), Reserve (3-6mo; T-bill ladder), Strategic surplus (>6mo; longer-duration). 2026 T-bill yields ~3.68% (1-3mo); state/local tax-exempt = +0.4-0.6pp equivalent. SOTA platforms: Rho (automated T-bill ladder), Public.com (custom ladders), Meow (BNY Mellon custody), TreasuryDirect (direct), Mercury Treasury, Brex Yield.

## When to use

- Post-raise cash deployment plan ($5M+ idle cash).
- Annual treasury policy refresh.
- Yield-curve change reaction (Fed rate move).
- Multi-bank strategy decision post-SVB.
- Trigger phrases: "treasury", "yield ladder", "T-bills", "treasury allocation", "idle cash", "treasury management", "Rho", "Public.com Treasury".

NOT for: capital allocation (use `capital-allocation-framework`); banking strategy alone (covered briefly here, see role.md "Multi-bank" section).

## Setup

```bash
# Yield curve data (free)
# yfinance for ^IRX (13wk T-bill), ^FVX (5yr), ^TNX (10yr)
uvx --with yfinance --with pandas --with matplotlib python -c "import yfinance; print(yfinance.__version__)"

# Treasury Direct for direct T-bill purchase (free; no key)
# https://www.treasurydirect.gov/

# Rho / Public.com / Mercury Treasury APIs (recipient supplies)
export RHO_API_KEY="<from Rho Settings>"
export PUBLIC_API_KEY="<from Public.com>"
```

## The three-tier framework

```
TIER 1 — OPERATING (6-8 weeks of cash outflows)
  Risk: zero (FDIC + HYSA)
  Yield 2026: 4.0-5.0% APY
  Vehicles: Mercury (4.X% promotional), Brex Cash, Wealthfront Cash (4.5%),
            Rho operating, Bank of America Commercial Checking
  Use: payroll, AP, daily ops

TIER 2 — RESERVE (3-6 months runway)
  Risk: very low (T-bills, government MMFs)
  Yield 2026: 3.5-4.0%
  Vehicles: T-bill ladder (1-12 month), Vanguard Federal MMF (VMFXX),
            Fidelity Government MMF (FZDXX)
  Use: known capital needs in next 6 months

TIER 3 — STRATEGIC SURPLUS (> 6 months out)
  Risk: low (T-notes, investment-grade corp, brokered CDs)
  Yield 2026: 3.7-5.0% depending on duration
  Vehicles: 2-3yr T-notes, brokered CDs, short-duration corp ETF (e.g. VCSH)
  Use: long-term capital surplus
```

### Allocation by stage

```
Pre-seed / Seed ($1M-$5M cash):
  Tier 1: 100% (just keep it in HYSA; complexity not worth it)

Series A ($5M-$20M cash):
  Tier 1: 30-40% (operating + 6 weeks runway)
  Tier 2: 50-60% (T-bill ladder 1-6mo)
  Tier 3: 0-10% (typically none — keep flexibility)

Series B+ ($20M-$100M cash):
  Tier 1: 15-25%
  Tier 2: 40-55%
  Tier 3: 25-40% (longer-duration; lower volatility budget)

Late stage (>$100M cash):
  Tier 1: 10-15%
  Tier 2: 35-45%
  Tier 3: 40-55% (institutional treasury policy required)
```

## Common recipes

### Recipe 1 — Compute tier allocation

```python
def compute_treasury_allocation(cash_balance, monthly_outflows, stage):
    operating_weeks = 6 if stage in ("Seed", "Series A") else 8
    tier1_target = monthly_outflows * (operating_weeks / 4.33)
    if stage in ("pre-seed", "Seed"):
        return {"tier1": cash_balance, "tier2": 0, "tier3": 0}

    if stage == "Series A":
        tier1 = min(tier1_target, cash_balance)
        remaining = cash_balance - tier1
        tier2 = remaining * 0.85
        tier3 = remaining * 0.15
    elif stage == "Series B":
        tier1 = min(tier1_target, cash_balance)
        remaining = cash_balance - tier1
        tier2 = remaining * 0.55
        tier3 = remaining * 0.45
    else:  # late
        tier1 = min(tier1_target, cash_balance)
        remaining = cash_balance - tier1
        tier2 = remaining * 0.40
        tier3 = remaining * 0.60
    return {"tier1": tier1, "tier2": tier2, "tier3": tier3}

# Series A SaaS: $15M cash, $450K/mo outflows
print(compute_treasury_allocation(15_000_000, 450_000, "Series A"))
```

### Recipe 2 — Build T-bill ladder

```python
import pandas as pd

def build_tbill_ladder(amount, durations_months, yields):
    """Equal-weighted ladder across durations.
    durations_months: [1, 3, 6, 12]
    yields: matching annualized yields"""
    per_rung = amount / len(durations_months)
    rungs = []
    for d, y in zip(durations_months, yields):
        rungs.append({
            "duration_months": d,
            "amount": per_rung,
            "annual_yield": y,
            "expected_interest_at_maturity": per_rung * y * (d / 12),
            "maturity_month": d
        })
    df = pd.DataFrame(rungs)
    df["total_interest_to_maturity"] = df["expected_interest_at_maturity"]
    return df

# 2026 yield curve approx
ladder = build_tbill_ladder(
    amount=5_000_000,
    durations_months=[1, 3, 6, 9, 12],
    yields=[0.0370, 0.0368, 0.0365, 0.0360, 0.0355]
)
print(ladder)
print(f"Annualized blended yield: {(ladder['amount'] * ladder['annual_yield']).sum() / ladder['amount'].sum():.2%}")
```

### Recipe 3 — Pull yield curve from yfinance

```python
import yfinance as yf
import pandas as pd

def get_yield_curve():
    """Pull current Treasury yields."""
    tickers = {"^IRX": "13wk", "^FVX": "5yr", "^TNX": "10yr", "^TYX": "30yr"}
    data = {}
    for ticker, label in tickers.items():
        t = yf.Ticker(ticker)
        info = t.info
        data[label] = info.get("regularMarketPrice") or info.get("previousClose")
    return data

print(get_yield_curve())
```

### Recipe 4 — Tax-equivalent yield (state-tax-exempt T-bills)

```python
def tax_equivalent_yield(tbill_yield, state_tax_rate):
    """T-bill interest = exempt from state/local tax. Equivalent muni-style yield."""
    return tbill_yield / (1 - state_tax_rate)

# CA: state tax 8% on corp interest
print(tax_equivalent_yield(0.0370, state_tax_rate=0.088))
# Equivalent yield: ~4.06%
```

### Recipe 5 — Rho automated T-bill ladder

```bash
# Set up ladder via Rho API
curl -X POST "https://api.rho.co/v1/treasury/ladders" \
  -H "Authorization: Bearer $RHO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 5000000,
    "durations": ["1mo", "3mo", "6mo", "9mo", "12mo"],
    "weights": [0.20, 0.20, 0.20, 0.20, 0.20],
    "auto_reinvest": true
  }'

# Get current ladder positions
curl "https://api.rho.co/v1/treasury/ladders" -H "Authorization: Bearer $RHO_API_KEY"
```

### Recipe 6 — Direct T-bill purchase (TreasuryDirect)

```
TreasuryDirect direct purchase steps (manual; no API):
1. Create TreasuryDirect account (treasurydirect.gov)
2. Schedule auction participation (Mondays + Tuesdays for 4/8/13/26/52-week bills)
3. Submit non-competitive bid (always accepted at auction-set rate)
4. Funds settle Thursday post-auction
5. No fees; no commission

Limitations: $10M per auction per individual; corp accounts more complex.
```

### Recipe 7 — Multi-bank diversification

```python
def multi_bank_allocation(total_cash, max_per_bank_fdic=250_000):
    """Allocate >$250K FDIC limit across multiple banks for safety."""
    banks_needed = max(1, int(total_cash / max_per_bank_fdic) + 1)
    return {
        "banks_required": banks_needed,
        "allocation_per_bank": max_per_bank_fdic,
        "uninsured_excess": max(0, total_cash - banks_needed * max_per_bank_fdic),
        "recommendation": "Use Mercury IntraFi (auto-spreads across 25+ banks for FDIC coverage)"
    }

print(multi_bank_allocation(15_000_000))
```

### Recipe 8 — Interest income forecast

```python
def annual_interest_forecast(allocations, yields):
    """allocations: dict tier→$; yields: dict tier→annual yield"""
    return {tier: amt * yields[tier] for tier, amt in allocations.items()}, \
           sum(amt * yields[tier] for tier, amt in allocations.items())

allocations = {"tier1": 2_750_000, "tier2": 8_500_000, "tier3": 3_750_000}
yields = {"tier1": 0.045, "tier2": 0.0365, "tier3": 0.0420}
per_tier, total = annual_interest_forecast(allocations, yields)
print(per_tier, f"Total: ${total:,.0f}")
```

### Recipe 9 — Reinvestment cadence

```
Tier 2 (T-bill ladder) reinvestment:
  Every month, 1 rung matures; reinvest at next available 12mo rung
  Result: continuous 12-mo rolling ladder; always 12mo of staggered maturities

Tier 3 (longer-duration) reinvestment:
  Match to known capital event timing (e.g. anticipated Series B 18mo out)
  Avoid maturities concentrated at single point
```

### Recipe 10 — Treasury policy document template

```markdown
# Treasury Policy — Acme Inc.

## Objective
Preserve principal, maintain liquidity for operating needs, earn yield consistent with risk tolerance.

## Tier structure
- Tier 1 (Operating): 6 weeks of outflows; FDIC-insured HYSA
- Tier 2 (Reserve): 6 months runway; T-bill ladder 1-12mo
- Tier 3 (Strategic): excess; T-notes 1-3yr OR money market funds

## Approved instruments
HYSA, T-bills (TreasuryDirect/Rho/Public.com), Federal MMF (Vanguard VMFXX),
T-notes ≤3yr, brokered CDs, prime MMF (limited 10% of total).

## Prohibited
Equity securities, sub-investment-grade corp, FX speculation, derivatives,
crypto, commercial paper from non-AAA issuers.

## Approval thresholds
- < $1M: CFO sole approval
- $1M-$5M: CFO + CEO approval
- > $5M: Board approval

## Multi-bank policy
Per single bank: $250K FDIC limit + Mercury IntraFi sweep for excess.
Minimum 2 operating banks for diversification.

## Review cadence
Quarterly to board; monthly internal.
```

## Examples

### Example 1: Series A SaaS — $15M just raised

**Goal:** Deploy efficiently.

**Steps:**
1. Recipe 1 → tier allocation ($2.75M / $8.5M / $3.75M).
2. Recipe 3 → current yield curve.
3. Recipe 2 → 5-rung T-bill ladder for Tier 2.
4. Recipe 5 → Rho automated; OR Recipe 6 → TreasuryDirect direct.
5. Recipe 8 → annual interest forecast ($550-600K).
6. Recipe 10 → write treasury policy; approve at board.

**Result:** $550K+/year interest income at near-zero risk.

### Example 2: Yield-curve shift — Fed cuts 50bps

**Goal:** Rebalance.

**Steps:**
1. Recipe 3 → updated yield curve.
2. Re-run Recipe 2 with new yields.
3. Decide: stay in shorter durations (capture future cuts) or lock in 6-12mo at current yields.
4. If recipe yields favor locking in, extend ladder duration mix.
5. Recompute Recipe 8.

**Result:** Defensible reallocation.

## Edge cases / gotchas

- **FDIC limit is $250K per depositor per bank.** Treasury > $250K = uninsured if single-bank. Use Mercury IntraFi or spread across banks.
- **Mercury IntraFi auto-spreads.** Across 25+ banks; coverage up to ~$5M. Beyond that, manual diversification.
- **T-bills are state-tax-exempt.** ~40-60bps equivalent yield boost vs CDs in high-tax states (CA, NY).
- **TreasuryDirect for corp = harder.** Easier via Rho / Public.com / Public Custody (Apex Clearing).
- **MMF "breaking the buck" risk (extreme).** Stick to Federal MMFs (Vanguard VMFXX, Fidelity FZDXX) — government securities only.
- **Reinvestment risk in declining yield environment.** Lock duration where you can (1yr T-bill > 1mo T-bill if rates expected to fall).
- **Liquidity penalty on early T-bill sale.** T-bills are highly liquid (secondary market), but selling before maturity may yield less than expected. Match duration to known cash needs.
- **Don't chase yield with corp debt.** Investment-grade corp = +30-80bps vs T-bill, but default risk + complexity. Stick to Treasuries until policy-approved otherwise.
- **Crypto / stablecoin treasury policies.** Some startups consider; most institutional auditors flag as concentration risk. Disclose if you use.
- **Treasury policy needs board approval.** Especially Tier 3 (longer duration).
- **Brex Yield post-Cap One merger.** Watch policy changes mid-2026; some Brex products may shift.
- **SVB lesson.** Multi-bank for safety; multi-vehicle for yield.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions.**

## Sources

- Rho treasury management 2026: https://www.rho.co/blog/treasury-management-software
- Rho T-bill ladder guide: https://www.rho.co/blog/guide-to-t-bill-ladders
- Yield Alley T-bill ladder: https://yieldalley.com/t-bill-ladder-how-to-build-one/
- Safety Yield T-bill ladder: https://safetyyield.com/guides/treasury-bill-ladder
- TreasuryDirect: https://www.treasurydirect.gov/
- Public.com Treasury: https://public.com/learn/treasury-bills
- Mercury IntraFi: https://mercury.com/treasury
- yfinance docs: https://pypi.org/project/yfinance/

## Related skills

- `capital-allocation-framework` — treasury is Priority 2 ("Reserve").
- `capital-structure-debt-equity-mix-stage` — interaction with debt covenants.
- `three-statement-financial-model-tied` — interest income forecast → IS.
- `board-cfo-financial-package` — treasury slide in board pack.
