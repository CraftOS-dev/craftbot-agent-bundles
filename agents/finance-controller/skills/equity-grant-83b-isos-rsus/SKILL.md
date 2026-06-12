<!--
Source: https://help.pulley.com/en/articles/4781385-83-b-election-faq
Source: https://carta.com/learn/equity/asc-718/
Source: https://pulley.com/products/esop-management-software
Source: https://www.irs.gov/pub/irs-pdf/p525.pdf (IRS Pub 525)
Reference role.md: "Equity grant playbook"
-->

# Equity grants — ISO / NSO / RSU / SAFE / 83(b)

Grant mechanics + tax treatment + 83(b) 30-day window + AMT $100K rule + ASC 718 stock-based comp expense. Covers founder restricted stock through Series C employee grants.

## When to use

- Issuing any equity grant: founder restricted stock, employee ISO/NSO, advisor NSO, contractor stock, board grants.
- 83(b) election (CRITICAL — 30-day window).
- 409A check before grant (must equal current FMV).
- ASC 718 expense waterfall for monthly close.
- Modeling SAFE → priced round conversion.
- Trigger phrases: "grant equity", "ISO", "NSO", "RSU", "SAFE", "83(b)", "AMT", "ASC 718", "vesting".

NOT for: cap-table maintenance (use `carta-pulley-cap-table`); legal opinion (defer to `legal-counsel`).

## Setup

This skill primarily uses the cap-table tools (Carta / Pulley — see `carta-pulley-cap-table`) plus IRS forms and standard accounting libraries:

```bash
# Cap-table platform (Carta or Pulley) — see carta-pulley-cap-table for OAuth setup
export CARTA_TOKEN="..."   # OR
# Pulley dashboard access (no public API)

# 83(b) reminders + delivery (already shipped):
# - remindme skill (for 25/29/30 day reminders)
# - gmail-mcp (for 83(b) confirmation outreach)

# ASC 718 fair-value computation:
pip install scipy           # Black-Scholes via scipy.stats.norm

# IRS 83(b) filing template — standard PDF
# Download: https://www.irs.gov/forms-pubs/about-form-83-b
```

Auth / env vars summary:
- `CARTA_TOKEN` — for issuing grants programmatically (invite-only; see `carta-pulley-cap-table`)
- No env needed for ASC 718 computation (pure Python)
- 83(b) filings are paper-mail to IRS (no API)

## Grant decision tree

```
Grantee = employee?
├── YES → ISO preferred (tax-advantaged) → check $100K AMT rule (Recipe 6)
│         If exceeded → split: ISO portion + NSO portion
└── NO → Contractor / advisor / board member?
        ├── YES → NSO only (ISOs are W-2-only)
        └── NO → Founder? → restricted stock + 83(b) election (Recipe 2)

Grantee = late-stage / public-track employee?
└── YES → RSU (double-trigger common)

Pre-priced fundraise instrument?
└── YES → SAFE (post-money standard 2026) or convertible note
```

## Instrument quick-reference

### ISO (Incentive Stock Option)

- **Eligibility:** W-2 employee only
- **Tax at grant:** none
- **Tax at exercise:** no regular tax; AMT on spread (bargain element)
- **Tax at sale:** LTCG if held 1yr post-exercise + 2yr post-grant; else ordinary income
- **$100K AMT rule:** if (strike × shares becoming exercisable in calendar year) > $100K, excess is NSO-treated
- **90-day post-termination exercise window** (or expire); some companies extend to 7-10 years
- **Strike price:** ≥ current 409A FMV (mandatory; below = 409A penalty 20% federal)

### NSO (Non-Qualified Stock Option)

- **Eligibility:** anyone (employee, contractor, advisor, board)
- **Tax at grant:** none (if strike ≥ FMV)
- **Tax at exercise:** ordinary income on spread between strike and FMV (employer W-2 / 1099-NEC)
- **Tax at sale:** capital gain on appreciation post-exercise
- **No holding-period advantage** vs ISO

### RSU (Restricted Stock Unit)

- **Eligibility:** any employee (typically later-stage / public-track)
- **Tax at vest:** ordinary income on FMV at vest (treated like cash comp)
- **Tax at sale:** capital gain on appreciation post-vest
- **Double-trigger:** common in private — vests only on (time AND liquidity event)
- **Single-trigger:** auto-vests on time — less common; bigger tax bill at vest

### Restricted Stock (Common, with vesting)

- **Eligibility:** founders, early hires
- **Tax default:** ordinary income at vest on (FMV at vest − price paid)
- **With 83(b) election:** elect to pay tax at grant date on (FMV at grant − price paid); future appreciation is LTCG
- **83(b) window:** **30 days from grant date** (HARD DEADLINE)

### SAFE (Simple Agreement for Future Equity)

- **YC standard:** post-money (default since 2018) or pre-money
- **Terms:** valuation cap + discount (typically 20%); MFN clause optional
- **No interest, no maturity** (vs convertible note)
- **Tax:** investor pays nothing at SAFE; converts to equity at next priced round
- **Conversion:** at lower of (cap-based price) or (Series A price × (1 − discount))

### Convertible Note

- **Debt that converts:** has interest (4-8% typical) + maturity (typically 18-36 months)
- **Cap + discount** same as SAFE
- **Conversion:** at next priced round OR maturity (with conversion price formula or repayment)

## Common recipes

### Recipe 1 — Standard 4-yr / 1-yr cliff vesting schedule

```python
from datetime import date
from dateutil.relativedelta import relativedelta

def vesting_schedule(grant_date, total_shares, cliff_months=12, total_months=48):
    """Standard: 25% on cliff, then monthly through month 48."""
    schedule = []
    cliff_date = grant_date + relativedelta(months=cliff_months)
    cliff_shares = total_shares * cliff_months / total_months

    schedule.append({"vest_date": cliff_date, "shares_vested": cliff_shares})

    monthly_after_cliff = (total_shares - cliff_shares) / (total_months - cliff_months)
    for m in range(1, total_months - cliff_months + 1):
        schedule.append({
          "vest_date": cliff_date + relativedelta(months=m),
          "shares_vested": cliff_shares + monthly_after_cliff * m
        })
    return schedule

# Example: 10,000 share grant on 2026-06-15
sched = vesting_schedule(date(2026,6,15), 10_000)
print(sched[0])   # cliff: 2027-06-15, 2500 shares
print(sched[-1])  # final: 2030-06-15, 10000 shares
```

### Recipe 2 — 83(b) election (30-day window)

```python
def schedule_83b_reminder(grantee_email, grant_date):
    """Schedule reminder day-25, day-29, day-30 (hard deadline)."""
    deadline = grant_date + relativedelta(days=30)
    day_25 = grant_date + relativedelta(days=25)

    # Send via gmail-mcp / remindme
    gmail.send(
      to=grantee_email,
      cc="legal@company.com",
      subject="83(b) ELECTION DEADLINE — file by " + str(deadline),
      body=f"""
Dear {grantee_name},

Per IRS rules, the 83(b) election on your equity grant must be filed
within 30 days of grant date.

Grant date: {grant_date}
Deadline: {deadline}
Days remaining: {(deadline - date.today()).days}

To file:
1. Sign attached 83(b) form (cc'd legal).
2. Mail certified return-receipt to:
   Internal Revenue Service Center [address by state — see https://www.irs.gov/filing/where-to-file-paper-tax-returns]
3. Send copy to company HR (no FAX).
4. Keep original receipt in personal records.

Missing the 30-day window = no election possible = ordinary income tax
on every future vesting tranche at then-current FMV. For high-growth
companies, this is typically a $100K-$1M+ tax difference.

Please confirm receipt and intended filing date by replying here.

[Auto-reminder at day 25 and day 29.]
"""
    )
```

83(b) is the single highest-stakes detail in equity comp. Always cc legal counsel.

### Recipe 3 — ISO $100K AMT rule check

```python
def iso_100k_check(grants, strike_price, calendar_year):
    """
    grants: list of {grant_date, shares_vesting_in_year, instrument}
    Returns: (shares_treated_as_ISO, shares_treated_as_NSO)
    """
    sorted_g = sorted(grants, key=lambda g: g["grant_date"])  # FIFO ordering
    iso_value_used = 0
    iso_shares = 0
    nso_shares = 0

    for g in sorted_g:
        value = strike_price * g["shares_vesting_in_year"]
        if iso_value_used + value <= 100_000:
            iso_shares += g["shares_vesting_in_year"]
            iso_value_used += value
        else:
            remaining_capacity = 100_000 - iso_value_used
            iso_portion_shares = remaining_capacity / strike_price
            iso_shares += int(iso_portion_shares)
            nso_shares += g["shares_vesting_in_year"] - int(iso_portion_shares)
            iso_value_used = 100_000

    return iso_shares, nso_shares
```

If exceeded, split grant in Carta/Pulley: ISO portion + NSO portion. Disclose in offer letter.

### Recipe 4 — ASC 718 fair value at grant (Black-Scholes)

```python
import math
from scipy.stats import norm

def black_scholes_call(S, K, T, r, sigma):
    """
    S = stock price (current 409A FMV)
    K = strike price (= FMV for ISO)
    T = expected term in years (SAB 107: simple average of vest + contractual term)
    r = risk-free rate (5-yr Treasury)
    sigma = volatility (peer-group historical; 60-80% for early SaaS)
    """
    d1 = (math.log(S/K) + (r + sigma**2/2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * norm.cdf(d1) - K * math.exp(-r*T) * norm.cdf(d2)

# Example: ISO grant 10K shares, $1.25 FMV/strike, 4-yr vest, 10-yr expiration
# SAB 107 expected term ≈ (vest + contractual)/2 = (4 + 10)/2 = 7, conservative use 6.25
fv_per_share = black_scholes_call(S=1.25, K=1.25, T=6.25, r=0.045, sigma=0.65)
grant_value = fv_per_share * 10_000
monthly_expense = grant_value / 48
print(f"Fair value/share: ${fv_per_share:.4f} | Total grant value: ${grant_value:,.0f}")
print(f"Monthly ASC 718 expense: ${monthly_expense:,.0f}")
```

### Recipe 5 — ASC 718 expense waterfall (all grants)

```python
import pandas as pd
from dateutil.relativedelta import relativedelta

def asc_718_waterfall(grants, fmv_at_grant, risk_free=0.045, vol=0.65):
    waterfall = []
    for g in grants:
        fv = black_scholes_call(
          S=fmv_at_grant[g.grant_date], K=g.strike,
          T=g.expected_term_years, r=risk_free, sigma=vol
        )
        total_value = fv * g.shares
        monthly = total_value / g.vesting_months
        for m in range(g.vesting_months):
            waterfall.append({
              "grant_id": g.id,
              "month": (g.grant_date + relativedelta(months=m)).replace(day=1),
              "expense": monthly
            })
    return pd.DataFrame(waterfall).pivot_table(
      index="grant_id", columns="month", values="expense", fill_value=0
    )

# Period expense = sum of monthly columns in close period
```

Book monthly: Dr Stock-Based Compensation Expense / Cr Additional Paid-In Capital.

### Recipe 6 — Forfeit on departure

```python
def vested_on_departure(grant, departure_date):
    """Returns shares vested as of departure (90-day exercise window for ISOs)."""
    schedule = vesting_schedule(grant.grant_date, grant.shares,
                                grant.cliff_months, grant.total_months)
    vested = max([s["shares_vested"] for s in schedule if s["vest_date"] <= departure_date],
                 default=0)
    if grant.instrument == "ISO":
        exercise_deadline = departure_date + relativedelta(days=90)
        # Or longer if company extended window
        return {"vested_shares": vested, "exercise_deadline": exercise_deadline}
    return {"vested_shares": vested}
```

### Recipe 7 — Early exercise + 83(b) on early-exercised options

```python
# Early exercise = exercise option before vest (purchase unvested shares, subject to repurchase)
# Combined with 83(b): pay ordinary income tax NOW on spread at exercise date
# Future appreciation = LTCG (if held >1yr post-exercise)

def early_exercise_decision(current_fmv, strike, shares, expected_exit_fmv, years_to_exit):
    # Pay strike up front
    cash_required = strike * shares
    # 83(b): pay tax now on $0 spread (if strike = current FMV at exercise = ISO/NSO grant rule)
    # Future gain: LTCG on (exit_fmv − strike) × shares
    expected_ltcg = (expected_exit_fmv - strike) * shares
    expected_tax_saved = expected_ltcg * (0.37 - 0.20)  # ordinary - LTCG ≈ 17pp
    return {
      "cash_required": cash_required,
      "tax_saved_vs_late_exercise": expected_tax_saved,
      "breakeven_if_company_fails": cash_required  # loss if exit < strike
    }
```

### Recipe 8 — SAFE conversion modeler

```python
def safe_conversion(safe_invested, safe_cap, safe_discount,
                    priced_pre_money, priced_investment, fd_pre_safe):
    """Returns: (conversion_price, conversion_shares)"""
    price_per_share_cap = safe_cap / fd_pre_safe
    price_per_share_a = priced_pre_money / fd_pre_safe
    price_per_share_disc = price_per_share_a * (1 - safe_discount)

    conv_price = min(price_per_share_cap, price_per_share_disc)
    conv_shares = safe_invested / conv_price
    return conv_price, conv_shares

# Example
price, shares = safe_conversion(
  safe_invested=1_000_000, safe_cap=10_000_000, safe_discount=0.20,
  priced_pre_money=15_000_000, priced_investment=5_000_000, fd_pre_safe=10_000_000
)
print(f"SAFE converts at ${price:.2f}/share → {shares:,.0f} shares")
```

### Recipe 9 — Post-termination exercise window extension decision

```
Standard: 90 days post-termination to exercise vested options.
Extended: some companies offer 7-10 years.

Pros of extending:
- Better employee value proposition (more retention; better talent acquisition)
- Aligns with reality that early exercise + 83(b) is often not financially feasible

Cons:
- Tax: ISOs lose ISO status if held 90+ days post-termination
- ASC 718: extending window = modification = remeasure fair value → potentially more expense
- Dilution: more options exercised later = more shares outstanding

Recommendation: extend to 7-10 years if competitive in hiring market; remeasure ASC 718.
```

### Recipe 10 — Cap table impact preview (before grant)

```python
def grant_impact_preview(grant_shares, current_fd_total):
    new_fd_total = current_fd_total + grant_shares
    grantee_ownership = grant_shares / new_fd_total
    dilution_per_existing_holder = grant_shares / new_fd_total

    return {
      "grantee_ownership": f"{grantee_ownership:.2%}",
      "dilution_per_existing": f"{dilution_per_existing_holder:.3%}",
      "new_fd_total": new_fd_total
    }
```

Run this before every grant; surface to founder before signing.

## Examples

### Example 1: First employee hire — ISO grant

**Goal:** Senior SWE offered 5,000 ISO at $1.25 strike (current 409A FMV).

**Steps:**

1. Verify 409A fresh (<12 months, no material events).
2. Run Recipe 10 cap-table impact → 0.45% dilution to existing.
3. Run Recipe 3 $100K AMT check → 5000 × $1.25 = $6,250 < $100K → fully ISO.
4. Recipe 1 generate vesting schedule (4-yr / 1-yr cliff).
5. Recipe 4 compute ASC 718 fair value → $4,123 monthly expense.
6. Issue grant in Carta with: strike $1.25, term 10 years, 90-day post-term window.
7. Send employee equity primer + grant agreement.
8. Schedule grant-agreement signature confirmation reminder (30-day).

**Result:** Employee onboarded; ASC 718 expense flows into next monthly close.

### Example 2: Founder restricted stock with 83(b)

**Goal:** Co-founder receives 2.5M restricted shares at par ($0.0001) on 2026-06-15.

**Steps:**

1. Issue restricted stock with 4-yr vest, no cliff (founder default).
2. **Immediately on grant day:** prepare 83(b) form, send to founder.
3. Schedule Recipe 2 reminder cadence (day 25, 29, 30).
4. Founder mails 83(b) certified return-receipt to IRS by day 30.
5. Founder ships copy to company HR.
6. Confirm receipt by day 31; if not confirmed, escalate.
7. Spread at grant = (FMV $0.0001 − $0.0001) × 2.5M = $0 → no current tax.
8. Future appreciation = LTCG on sale.

**Result:** Founder paid $0 tax at grant; all future appreciation is LTCG (vs ordinary at vest without 83(b)).

## Edge cases / gotchas

- **83(b) 30-day window is HARD.** No extensions. Day 31 = no election possible. The single most expensive miss in equity comp.
- **409A staleness:** strike < FMV = 409A penalty (20% federal + interest). Re-val before grants if 409A is older than 12 months or material event occurred.
- **ISO + AMT exposure:** ISO exercise creates AMT income even with no regular tax. Surface this BEFORE employee exercises a big grant.
- **Foreign employees:** ISOs are US-only (W-2). Foreign hires get NSOs.
- **Repricing options:** if you reprice (e.g., during down round), it's a Modification under ASC 718 → remeasure → incremental expense.
- **RSU double-trigger gotcha:** double-trigger RSUs don't vest until IPO/M&A. Employees who leave pre-liquidity get nothing — be transparent.
- **SAFE MFN (most favored nation):** holder gets benefit of any better terms granted to subsequent SAFE holders. Track and apply.
- **Convertible note interest accrual:** interest accrues until conversion; include in conversion amount. Often forgotten.
- **Cap-table truth:** Carta / Pulley are tools, not authoritative. Signed grant agreements + signed certificates govern. Retain originals.
- **Equity comp expense ≠ cash:** ASC 718 expense flows to P&L but isn't cash. Investors often adjust EBITDA for SBC.
- **Spousal consent:** community-property states (CA, TX, NV, AZ, others) require spousal consent on stock issuance. Check.
- **PTEP rules (Section 83(i)):** qualified employees of private companies may defer income tax on exercise/vesting for 5 years. Rarely used; complex.
- **AMT credit:** AMT paid on ISO exercise becomes a credit usable against future regular tax. Track this; it's recoverable.

## Sources

- IRS Publication 525 (Taxable & Nontaxable Income): https://www.irs.gov/pub/irs-pdf/p525.pdf
- 83(b) election (IRS): https://www.irs.gov/forms-pubs/about-form-83-b
- 83(b) FAQ (Pulley): https://help.pulley.com/en/articles/4781385-83-b-election-faq
- ASC 718 overview (Carta): https://carta.com/learn/equity/asc-718/
- ISO vs NSO: https://carta.com/learn/equity/stock-options/iso-vs-nso/
- YC SAFE documents: https://www.ycombinator.com/documents
- 409A valuation (Carta): https://carta.com/409a/

## Related skills

- `carta-pulley-cap-table` — issues the actual grants
- `monthly-close-procedure` — ASC 718 expense booked monthly
- `fundraising-data-room` — SAFE + option-pool documentation
- `investor-update-monthly-quarterly` — equity dilution metrics
