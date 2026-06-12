<!--
Source: https://unicorncurrencies.com/forcfo/b2b-fx-platforms-compared/
Source: https://www.airwallex.com/ca/blog/strategies-companies-hedge-strengthening-home-currency
Source: https://blog.ibanfirst.com/en/airwallex-alternatives
Reference role.md: "FX hedging playbook"
-->

# FX hedging strategies — spot / forward / options / natural

Risk-tiered FX hedging: spot for short exposure, forwards for predictable 30-180 day, options for variable with cap. Hedge ratio rule: 50-80% of committed exposure; never overhedge (creates speculation). Natural hedging first (match revenue currency to expense currency via local entity). 2026 SOTA platforms: Wise Business (spot), Airwallex (forward + options), Revolut Business (fixed + flexible forwards), OANDA / XE (pure FX desks).

## When to use

- International revenue exposure (UK/EU/APAC SaaS).
- International expense exposure (overseas contractors, local entity payroll).
- M&A involving foreign target.
- Treasury policy refresh; hedging policy formalization.
- Trigger phrases: "FX hedging", "forward contract", "FX exposure", "currency risk", "GBP/USD", "EUR/USD", "Airwallex", "Wise forward", "natural hedge".

NOT for: international entity formation (use `international-entity-transfer-pricing`); treasury yield (use `treasury-yield-ladder-risk-tier`).

## Setup

```bash
uvx --with pandas --with numpy --with yfinance python -c "import pandas, yfinance"

# FX platform APIs (recipient supplies)
export WISE_API_KEY="<wise.com/business/api>"
export AIRWALLEX_API_KEY="<airwallex.com/api>"
export REVOLUT_BUSINESS_API_KEY="<revolut business API>"
export OANDA_API_KEY="<oanda fxTrade API>"
```

## FX hedging hierarchy

```
TIER 1 — NATURAL HEDGE (free; do this first)
  Match revenue currency to expense currency via local entity
  Example: GBP revenue → pay UK contractors / UK office in GBP from same GBP account
  Eliminates exposure; no derivative cost

TIER 2 — SPOT TRANSACTIONS (cheap; <30-day exposure)
  Convert at current rate; no forward commitment
  Cost: spread (0.4-1.5% via Wise/Mercury; 2-4% via traditional bank)
  Tools: Wise Business, Mercury International, Brex Multi-Currency

TIER 3 — FORWARD CONTRACTS (predictable; 30-180 day exposure)
  Lock today's rate for future delivery
  No upfront cost; spread embedded (~0.5-1.5%)
  Tools: Airwallex Forwards, Revolut Business Forwards, OANDA, traditional bank
  Subtype: fixed-date forward; flexible-date forward (settle anytime within window)

TIER 4 — OPTIONS (variable exposure with cap; expensive)
  Right but not obligation to convert at strike
  Premium paid upfront (~1-5% of notional depending on tenor + vol)
  Tools: Airwallex Premium Options, traditional bank FX desk
  Use case: bidding on M&A target priced in foreign currency

TIER 5 — SWAPS (long-duration; institutional)
  Cross-currency swap; rare for startups
  Use case: pre-IPO companies with multi-year debt in non-functional currency
```

## Hedge ratio guidance

```
EXPOSURE TYPE          HEDGE RATIO         INSTRUMENT
─────────────────────────────────────────────────────────────
Already-invoiced AR    80-100%             Spot or short forward
Backlog revenue        50-80%              Forward
Forecast revenue       30-50%              Forward or option
Speculative            0% (don't hedge)    —

EXPENSE EXPOSURE       HEDGE RATIO         INSTRUMENT
─────────────────────────────────────────────────────────────
Confirmed payroll      80-100%             Forward
Variable contractor    50-70%              Forward / option
Forecast hosting       30-50%              Option (capped)
─────────────────────────────────────────────────────────────
```

## Common recipes

### Recipe 1 — FX exposure inventory

```python
import pandas as pd

def fx_exposure(receivables, payables, by_currency=True):
    """receivables, payables: list of {currency, amount, expected_date}"""
    rec_df = pd.DataFrame(receivables)
    pay_df = pd.DataFrame(payables)
    net = rec_df.groupby("currency")["amount"].sum() - pay_df.groupby("currency")["amount"].sum()
    return net.to_frame("net_exposure_local").reset_index()

receivables = [
    {"currency": "GBP", "amount": 850_000, "expected_date": "2026-09-30"},
    {"currency": "EUR", "amount": 1_200_000, "expected_date": "2026-10-15"},
]
payables = [
    {"currency": "GBP", "amount": 320_000, "expected_date": "2026-09-15"},
    {"currency": "EUR", "amount": 480_000, "expected_date": "2026-10-01"},
]
print(fx_exposure(receivables, payables))
# Net: GBP +530K, EUR +720K → hedge these
```

### Recipe 2 — Forward contract sizing

```python
def forward_size(exposure_amount, hedge_ratio, current_spot_rate, forward_rate):
    """Compute notional + forward-vs-spot implied yield."""
    hedged_amount = exposure_amount * hedge_ratio
    return {
        "exposure": exposure_amount,
        "hedge_ratio": hedge_ratio,
        "hedged_amount_local": hedged_amount,
        "spot_rate": current_spot_rate,
        "forward_rate": forward_rate,
        "implied_carry": (forward_rate / current_spot_rate - 1),
        "hedged_amount_in_home": hedged_amount * forward_rate
    }

# GBP 530K receivable in 90 days; hedge 70%
# Current GBP/USD = 1.28; 90-day forward = 1.2845
print(forward_size(530_000, 0.70, 1.28, 1.2845))
```

### Recipe 3 — Spot conversion (Wise API)

```bash
curl -X POST "https://api.wise.com/v1/quotes" \
  -H "Authorization: Bearer $WISE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"profile": YOUR_PROFILE_ID, "source": "GBP", "target": "USD", "sourceAmount": 100000}'

# Create transfer using quote
curl -X POST "https://api.wise.com/v1/transfers" \
  -H "Authorization: Bearer $WISE_API_KEY" \
  -d '{"quoteUuid": "QUOTE_UUID", "targetAccount": ACCOUNT_ID, "reference": "Q3 GBP conversion"}'
```

### Recipe 4 — Forward contract (Airwallex API)

```bash
# Get forward quote
curl -X POST "https://api.airwallex.com/api/v1/fx_forwards/quote" \
  -H "Authorization: Bearer $AIRWALLEX_API_KEY" \
  -d '{
    "sell_currency": "GBP",
    "buy_currency": "USD",
    "sell_amount": 371000,
    "settlement_date": "2026-09-30",
    "type": "fixed"
  }'

# Execute forward
curl -X POST "https://api.airwallex.com/api/v1/fx_forwards" \
  -H "Authorization: Bearer $AIRWALLEX_API_KEY" \
  -d '{"quote_id": "QUOTE_ID"}'
```

### Recipe 5 — Option contract pricing (Black-Scholes for forex)

```python
from scipy.stats import norm
import math

def fx_option_premium(spot, strike, time_years, rate_domestic, rate_foreign, volatility, option_type="call"):
    """Garman-Kohlhagen FX option model."""
    d1 = (math.log(spot / strike) + (rate_domestic - rate_foreign + 0.5 * volatility**2) * time_years) / (volatility * math.sqrt(time_years))
    d2 = d1 - volatility * math.sqrt(time_years)
    if option_type == "call":
        premium = spot * math.exp(-rate_foreign * time_years) * norm.cdf(d1) - strike * math.exp(-rate_domestic * time_years) * norm.cdf(d2)
    else:
        premium = strike * math.exp(-rate_domestic * time_years) * norm.cdf(-d2) - spot * math.exp(-rate_foreign * time_years) * norm.cdf(-d1)
    return premium

# 90-day GBP put @ 1.28 strike; spot 1.28; USD rate 4%, GBP rate 4.5%, vol 8%
print(f"Option premium per GBP: ${fx_option_premium(1.28, 1.28, 90/365, 0.04, 0.045, 0.08, 'put'):.4f}")
```

### Recipe 6 — Natural hedge analysis

```python
def natural_hedge_score(revenue_by_ccy, expenses_by_ccy):
    """Higher score = more natural hedge."""
    out = []
    for ccy in set(list(revenue_by_ccy.keys()) + list(expenses_by_ccy.keys())):
        rev = revenue_by_ccy.get(ccy, 0)
        exp = expenses_by_ccy.get(ccy, 0)
        net = rev - exp
        ratio = min(rev, exp) / max(rev, exp) if max(rev, exp) > 0 else 0
        out.append({"currency": ccy, "revenue": rev, "expense": exp, "net": net, "natural_hedge_ratio": ratio})
    return pd.DataFrame(out)

print(natural_hedge_score(
    revenue_by_ccy={"USD": 12_000_000, "GBP": 2_500_000, "EUR": 1_800_000},
    expenses_by_ccy={"USD": 10_500_000, "GBP": 1_200_000, "EUR": 280_000}
))
# GBP: 48% natural hedge; EUR: 16% — high net EUR exposure to hedge
```

### Recipe 7 — Hedge ladder for backlog revenue

```python
def hedge_ladder(monthly_exposures, hedge_ratios):
    """Build ladder of forwards matching expected receipts."""
    out = []
    for month, exp in monthly_exposures.items():
        ratio = hedge_ratios.get(month, 0.50)
        out.append({"month": month, "exposure": exp, "hedge_ratio": ratio, "hedged": exp * ratio})
    return pd.DataFrame(out)

ladder = hedge_ladder(
    monthly_exposures={"M+1": 150_000, "M+2": 170_000, "M+3": 180_000, "M+4": 200_000, "M+5": 200_000},
    hedge_ratios={"M+1": 0.80, "M+2": 0.70, "M+3": 0.60, "M+4": 0.50, "M+5": 0.40}
)
print(ladder)
```

### Recipe 8 — Mark-to-market hedge valuation

```python
def mtm_forward(notional, contract_rate, current_rate, days_to_settlement, discount_rate=0.04):
    """Mark-to-market value of outstanding forward."""
    pv_factor = 1 / (1 + discount_rate * days_to_settlement / 365)
    mtm = notional * (contract_rate - current_rate) * pv_factor
    return mtm

# GBP 100K forward at 1.2845; current spot 1.2780; 45 days remaining
print(f"MTM gain/loss: ${mtm_forward(100_000, 1.2845, 1.2780, 45):.0f}")
# Positive = gain (sold GBP higher than current spot)
```

### Recipe 9 — FX policy document template

```markdown
# FX Hedging Policy — Acme Inc.

## Objective
Reduce earnings volatility from FX fluctuations on committed and forecast exposure;
do not speculate on FX.

## Exposure types + hedge ratios
- Booked AR / AP (≤30 days): 80-100% spot or short forward
- Backlog (30-180 days): 50-80% forward
- Forecast (180-365 days): 30-50% forward or option
- Speculative: 0% (no hedging)

## Approved instruments
Spot, fixed-date forwards, flexible-date forwards, vanilla options
(call/put). NOT approved: structured derivatives, leveraged products.

## Approved providers
Wise Business (spot), Airwallex (forwards + options),
Revolut Business (forwards), traditional bank FX desk (large notional).

## Approval thresholds
- ≤$500K notional: CFO sole approval
- $500K-$5M: CFO + CEO approval
- >$5M: Board approval

## Review cadence
Quarterly review; monthly MTM tracking.
```

## Examples

### Example 1: UK SaaS w/ GBP revenue exposure

**Goal:** Hedge GBP receivables over next 6 months.

**Steps:**
1. Recipe 1 → exposure inventory; net GBP +530K next 6mo.
2. Recipe 6 → natural hedge analysis; 48% covered by GBP expenses.
3. Remaining 52% (≈$275K equivalent) needs hedging.
4. Recipe 7 → hedge ladder; 80% near-term, 40% out-month.
5. Recipe 4 → Airwallex forward contracts at each step.
6. Recipe 8 → monthly MTM tracking; report to board.

**Result:** Reduced earnings volatility; predictable USD revenue.

### Example 2: M&A target priced in EUR

**Goal:** Cap downside on EUR purchase price.

**Steps:**
1. Target purchase EUR 25M, signing 90 days out.
2. Recipe 5 → option premium for EUR call at strike 1.10 (current spot 1.08).
3. Premium ~1.5% of notional ≈ EUR 375K.
4. Lock in maximum USD cost; if EUR falls, let option expire.
5. Disclose hedge to deal team + board.

**Result:** USD cost cap; deal protected against EUR appreciation.

## Edge cases / gotchas

- **Overhedging = speculation.** Never hedge >100% of expected exposure.
- **Wise Business: spot only.** No forwards. Use Airwallex / Revolut Business for forwards.
- **Forward MTM swings can be material.** Mid-quarter MTM losses on outstanding forwards may surprise the board. Disclose policy.
- **Option premium = sunk cost.** If option expires worthless, premium is lost. Budget accordingly.
- **Local-entity natural hedge requires entity (PE trigger).** Cross-ref `international-entity-transfer-pricing` for entity decision.
- **Cross-currency settlement on weekends.** Settlements lag if signing Fri afternoon; may push 3 business days.
- **Counterparty risk.** Airwallex, Revolut Business are regulated; smaller fintechs may not be. Diversify if notional > $5M.
- **Hedge accounting (ASC 815 / IFRS 9).** If using hedge accounting, formal documentation required at inception. Most startups don't qualify; recognize MTM through P&L.
- **Tax treatment of FX gains/losses.** Realized = ordinary income / loss; unrealized MTM may or may not be recognized depending on jurisdiction.
- **Currency controls.** Some currencies (CNY, INR, BRL) have capital controls limiting forward availability.
- **Brexit / regulatory drift.** UK platforms may face EU access restrictions; check provider regulatory status annually.
- **Don't hedge speculative exposure.** If "we MIGHT win a deal," don't pre-hedge. Wait until contracted.

> ⚠ **This is informational guidance from an AI agent. Always consult a licensed CFO, CPA, or qualified investment advisor before making binding strategic-finance decisions.**

## Sources

- Unicorn Currencies B2B FX 2026: https://unicorncurrencies.com/forcfo/b2b-fx-platforms-compared/
- Airwallex hedging strategies: https://www.airwallex.com/ca/blog/strategies-companies-hedge-strengthening-home-currency
- iBanFirst Airwallex alternatives: https://blog.ibanfirst.com/en/airwallex-alternatives
- Wise Business API: https://api-docs.wise.com/
- Airwallex API: https://www.airwallex.com/docs/api
- Revolut Business API: https://developer.revolut.com/docs/business
- OANDA fxTrade API: https://developer.oanda.com/rest-live-v20/introduction/
- ASC 815 Hedge Accounting: https://asc.fasb.org/topic&trid=2229074

## Related skills

- `treasury-yield-ladder-risk-tier` — FX-tier overlap.
- `international-entity-transfer-pricing` — natural-hedge enabler.
- `three-statement-financial-model-tied` — MTM through IS (or OCI w/ hedge accounting).
- `board-cfo-financial-package` — hedge slide in board pack.
