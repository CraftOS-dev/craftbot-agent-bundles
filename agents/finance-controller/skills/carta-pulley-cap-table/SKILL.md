<!--
Source: https://carta.com/api/
Source: https://docs.carta.com/api-platform/docs/introduction
Source: https://pulley.com/products/esop-management-software
Source: https://help.pulley.com/en/articles/4781385-83-b-election-faq
Source: https://valueaddvc.com/blog/best-cap-table-management-tools-in-2026-carta-pulley-angellist-capdesk-ranked
-->

# Carta + Pulley — cap table, 409A, equity grants, ASC 718

Programmatic cap-table maintenance, option grant tracking, 409A workflow, ASC 718 stock-based comp expense, and SAFE modeling. Carta = industry standard at Series A+ (40K+ companies, partner API invite-only); Pulley = pre-seed to Series A (free tier <25 stakeholders, 5-day 409A).

## When to use

- Issue / track equity grants (ISOs, NSOs, RSUs, SAFEs, common stock).
- Pull cap-table snapshot for board / investor reporting.
- Compute fully-diluted ownership; model dilution on new round.
- 409A FMV tracking + re-valuation scheduling.
- ASC 718 stock-based compensation expense waterfall.
- SAFE → priced round conversion modeling.
- Trigger phrases: "update the cap table", "grant equity", "409A", "ASC 718", "model dilution", "SAFE conversion".

NOT for: payroll execution (separate HRIS/payroll system); legal opinion (defer to `legal-counsel`).

## Setup

### Carta

```bash
# Carta Partner API is INVITE-ONLY.
# 1. Apply at developers.app.carta.com → 1-2 week approval
# 2. OAuth 2.0 setup
export CARTA_CLIENT_ID="..."
export CARTA_CLIENT_SECRET="..."
export CARTA_REDIRECT_URI="..."

# Get token via OAuth code flow:
TOKEN=$(curl -X POST https://login.app.carta.com/oauth/token \
  -d "grant_type=authorization_code" \
  -d "client_id=$CARTA_CLIENT_ID" \
  -d "client_secret=$CARTA_CLIENT_SECRET" \
  -d "code=$AUTH_CODE" \
  -d "redirect_uri=$CARTA_REDIRECT_URI")
export CARTA_TOKEN=$(echo $TOKEN | jq -r .access_token)

# Mock API for testing (no invite needed):
# https://mock-api.carta.com — same schema, fake data
```

### Pulley

```bash
# Pulley has limited public API; most access via dashboard.
# For programmatic access: contact partnerships@pulley.com or use CSV export/import.
# Free tier: <25 stakeholders.
```

## Standard equity instruments — quick reference

| Instrument | Best for | Tax treatment | Notes |
|---|---|---|---|
| Common stock | Founders, early employees | Ordinary income at vest unless 83(b) | Restricted with vesting (4-yr, 1-yr cliff standard) |
| Preferred stock | Investors (priced rounds) | Capital gains at sale | Liquidation pref (1x non-participating standard) |
| ISO | Employee only | LTCG if held 1yr post-exercise + 2yr post-grant; AMT exposure | $100K AMT rule per year |
| NSO | Anyone (contractor, advisor) | Ordinary income on exercise spread | Less tax-efficient than ISO |
| RSU | Later-stage / public-track | Ordinary income at vest | Double-trigger common (time + liquidity) |
| SAFE | Pre-priced fundraise | Converts at next priced round | YC post-money standard 2026 |
| Convertible note | Pre-priced (older) | Debt → equity at conversion | Has interest + maturity |

## Common recipes

### Recipe 1 — Pull cap table snapshot (Carta)

```bash
curl -H "Authorization: Bearer $CARTA_TOKEN" \
  "https://api.carta.com/v1alpha/companies/$COMPANY_ID/cap-table?as_of=2026-06-30"
```

Returns common + preferred + options + warrants + SAFEs with as-converted shares.

### Recipe 2 — Fully-diluted total reconciliation

```python
# Sum all instruments → must reconcile to single FD total
import requests, os
ct = requests.get(
  f"https://api.carta.com/v1alpha/companies/{COMPANY_ID}/cap-table",
  headers={"Authorization": f"Bearer {os.environ['CARTA_TOKEN']}"}
).json()

common      = sum(h["shares"] for h in ct["common_holders"])
preferred   = sum(h["shares"] for h in ct["preferred_holders"])
options_out = sum(g["shares"] for g in ct["option_grants"]
                  if g["status"] in ("outstanding","vested","unvested"))
options_pool_avail = ct["option_pool"]["available_shares"]
warrants    = sum(w["shares"] for w in ct.get("warrants", []))
safes_as_converted = sum(
  s["amount_invested"] / min(s["valuation_cap"], next_round_pre_money * (1-s["discount"]))
  * fd_pre_safe_shares for s in ct.get("safes", [])
)

fd_total = common + preferred + options_out + options_pool_avail + warrants + safes_as_converted
print(f"Fully-diluted total: {fd_total:,.0f} shares")
```

### Recipe 3 — Create option grant (Carta)

```bash
curl -X POST "https://api.carta.com/v1alpha/companies/$COMPANY_ID/option-grants" \
  -H "Authorization: Bearer $CARTA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "stakeholder_id": "$STAKE_ID",
    "shares": 10000,
    "exercise_price": 1.25,             // must equal current 409A FMV
    "grant_date": "2026-06-15",
    "vesting_schedule": {
      "type": "standard_4yr_1yr_cliff",
      "cliff_months": 12,
      "total_months": 48
    },
    "instrument_type": "ISO",
    "expiration_years": 10
  }'
```

### Recipe 4 — Schedule 409A re-valuation

```bash
# 409A required: annual, OR after material event (round, M&A discussion, top-line shift)
# Carta 409A service: ~$2-4K, 5-30 days delivery
# Pulley 409A: ~$1K, 5-day delivery

curl -X POST "https://api.carta.com/v1alpha/companies/$COMPANY_ID/409a-valuations/request" \
  -H "Authorization: Bearer $CARTA_TOKEN" \
  -d '{
    "as_of_date": "2026-06-30",
    "trigger": "annual_refresh",
    "company_materials": {
      "latest_financials_url": "https://...",
      "cap_table_url": "https://...",
      "recent_round_terms": "..."
    }
  }'
```

### Recipe 5 — Generate ASC 718 expense waterfall

```python
# Per grant, compute fair value at grant date (Black-Scholes), recognize ratably over vest
from scipy.stats import norm
import math, pandas as pd

def black_scholes(S, K, T, r, sigma):
    """S=stock price (FMV), K=strike, T=years to expiration, r=risk-free, sigma=vol"""
    d1 = (math.log(S/K) + (r + sigma**2/2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * norm.cdf(d1) - K * math.exp(-r*T) * norm.cdf(d2)

# Per grant
fair_value_per_share = black_scholes(
  S=1.25,   # 409A FMV at grant
  K=1.25,   # strike (= FMV for ISO)
  T=6.25,   # SAB 107 expected term (mid of 4-yr vest + 10-yr exp)
  r=0.045,  # 5-yr Treasury yield
  sigma=0.65 # peer-group vol, 60-80% for early-stage SaaS
)
grant_value = fair_value_per_share * 10000  # 10K shares grant
monthly_expense = grant_value / 48  # 48-month vest

# Build waterfall — for each month of vest, $X expense
waterfall = pd.DataFrame({
  "month": pd.date_range("2026-07-01", periods=48, freq="MS"),
  "monthly_expense": [monthly_expense] * 48
})
```

### Recipe 6 — Model dilution from new round

```python
# Pre-money $20M, raise $5M, post-money $25M, with pool top-up to 12%
pre_money = 20_000_000
investment = 5_000_000
post_money = pre_money + investment

# Pool top-up: target 12% pool post-close
existing_fd = 10_000_000          # pre-round shares
target_pool_pct = 0.12
required_pool_post = existing_fd * target_pool_pct / (1 - target_pool_pct)

# Investor ownership
new_investor_pct = investment / post_money     # 5/25 = 20%
existing_dilution = pre_money / post_money     # 20/25 = 80%

# Founder before vs after (assuming pool comes from pre-money — standard)
founder_pre = 0.50
founder_post = founder_pre * (existing_fd / (existing_fd + required_pool_post)) * existing_dilution
print(f"Founder: {founder_pre:.1%} → {founder_post:.1%}")
```

### Recipe 7 — SAFE → priced round conversion

```python
# YC post-money SAFE: $1M invested, $10M cap, 20% discount
safe_invested = 1_000_000
safe_cap = 10_000_000
safe_discount = 0.20

# Series A: $15M pre-money, $5M raise, fully-diluted pre-A = 10M shares
priced_pre_money = 15_000_000
priced_investment = 5_000_000
fd_pre_a = 10_000_000

# Cap-based price per share
price_per_share_cap = safe_cap / fd_pre_a              # $1.00

# Discount-based price
price_per_share_a = priced_pre_money / fd_pre_a        # $1.50
price_per_share_discount = price_per_share_a * (1 - safe_discount)  # $1.20

# SAFE converts at LOWER
safe_conversion_price = min(price_per_share_cap, price_per_share_discount)  # $1.00
safe_shares = safe_invested / safe_conversion_price                          # 1,000,000 shares
print(f"SAFE conversion: {safe_shares:,.0f} shares at ${safe_conversion_price:.2f}/share")
```

### Recipe 8 — 83(b) election reminder

```python
# On every restricted stock grant or early-exercise → schedule reminder
import datetime
grant_date = datetime.date(2026, 6, 15)
day_25 = grant_date + datetime.timedelta(days=25)  # 2026-07-10
deadline = grant_date + datetime.timedelta(days=30)  # 2026-07-15

# Auto-create reminder via remindme skill + gmail-mcp:
# "83(b) ELECTION DEADLINE — file by 2026-07-15 (5 days from this notice)"
#  → cc legal counsel
#  → attach 83(b) form pre-filled from Carta / Pulley template
```

Carta and Pulley both auto-prompt for 83(b) within their UIs — but assume failure mode: always set independent reminder.

### Recipe 9 — ISO $100K AMT rule check

```python
# Rule: if (strike × shares becoming exercisable in calendar year) > $100K,
# the excess is treated as NSO.
def iso_100k_split(grants, year):
    """grants: list of {strike, shares_vesting_in_year}"""
    sorted_g = sorted(grants, key=lambda g: g["grant_date"])  # FIFO
    iso_value = 0
    iso_count = 0
    for g in sorted_g:
        value = g["strike"] * g["shares_vesting_in_year"]
        if iso_value + value <= 100_000:
            iso_count += g["shares_vesting_in_year"]
            iso_value += value
        else:
            # Split — some ISO, rest NSO
            remaining = 100_000 - iso_value
            iso_shares = int(remaining / g["strike"])
            iso_count += iso_shares
            # Remainder is NSO
            iso_value = 100_000
    return iso_count
```

### Recipe 10 — Vested vs unvested split (for departure)

```bash
# When employee leaves, compute exact vested shares as of departure
curl -H "Authorization: Bearer $CARTA_TOKEN" \
  "https://api.carta.com/v1alpha/companies/$COMPANY_ID/option-grants/$GRANT_ID?as_of=2026-06-15"

# Standard 90-day post-termination exercise window
# Notify cardholder + counsel
```

## Examples

### Example 1: Series A close — recompute fully-diluted

**Goal:** Founder wants to know post-Series A ownership splits.

**Steps:**

1. Pull current cap table (Recipe 1).
2. Pull existing SAFEs (Recipe 2 sub-loop).
3. Model conversion (Recipe 7) at priced round terms.
4. Compute new pool top-up (Recipe 6, target 12% post).
5. Add Series A preferred shares: $5M / price per share.
6. Sum: new FD = existing common + existing preferred + converted SAFEs + new pool + Series A preferred.
7. Per-stakeholder ownership = stakeholder shares / new FD.

**Result:** Spreadsheet of every stakeholder pre vs post Series A; founder confirms before signing term sheet.

### Example 2: First ISO grant for new hire

**Goal:** Engineering hire offer letter includes 5,000 ISO grant.

**Steps:**

1. Confirm 409A is fresh (<12 months, no material events since). If stale → request re-val (Recipe 4) first.
2. Strike price = current 409A FMV (mandatory; below = 409A penalty).
3. Create grant (Recipe 3) with vesting 4-yr / 1-yr cliff.
4. Compute ASC 718 fair value (Recipe 5) → adds $X/mo to comp expense.
5. Verify $100K AMT (Recipe 9) — confirm grant won't push past threshold.
6. Send offer letter + grant agreement.
7. Schedule onboarding reminder: confirm grant agreement signed within 30 days.

**Result:** Grant booked in Carta; ASC 718 expense flows into next close; cap-table reflects new FD.

## Edge cases / gotchas

- **Carta API invite-only:** without partner access, manual UI work or CSV import/export only. Mock API at mock-api.carta.com works for testing.
- **409A staleness penalty (IRC 409A):** 20% federal penalty + interest on the difference if FMV stale. Re-val at: annual, M&A discussions, large round, financial structure change, top-line shift >50%.
- **Pulley API limitations:** programmatic access is limited; rely on CSV exports for cap-table snapshots and dashboard for grant CRUD.
- **Vesting acceleration:** double-trigger (change-of-control + termination without cause) is standard; single-trigger is investor red flag. Confirm in grant agreement, not just Carta default.
- **Repricing options:** if you reprice (e.g., during down round), it's a Modification under ASC 718 → new fair value vs old fair value, incremental expense recognized. Don't forget.
- **SAFE post-money vs pre-money:** YC default switched to post-money in 2018; older SAFEs may be pre-money — dilution math differs significantly. Read the document; don't assume.
- **Convertible notes have interest:** unlike SAFEs, notes accrue interest (typically 4-8%) until conversion. Include accrued interest in conversion amount.
- **Carta data vs source-of-truth:** if there's any disagreement between Carta and the signed grant agreement, the signed agreement governs. Always retain PDF copies.
- **Foreign employees:** ISO requires US employee/contractor; for foreign employees, must be NSO. Carta defaults can mis-categorize.
- **AMT computation lag:** AMT on ISO exercise hits in the year of exercise even if no regular tax liability. Surface to employee at exercise time.
- **Mock API data:** Carta mock-api is fake — don't import its results to anything real.

## Sources

- Carta API platform: https://carta.com/api/
- Carta API docs: https://docs.carta.com/api-platform/docs/introduction
- Carta 409A: https://carta.com/409a/
- Pulley 409A: https://pulley.com/products/409a-valuations
- Pulley ESOP: https://pulley.com/products/esop-management-software
- Pulley 83(b) FAQ: https://help.pulley.com/en/articles/4781385-83-b-election-faq
- ASC 718 (Carta): https://carta.com/learn/equity/asc-718/
- YC SAFE documents: https://www.ycombinator.com/documents
- 2026 cap-table tool ranking: https://valueaddvc.com/blog/best-cap-table-management-tools-in-2026-carta-pulley-angellist-capdesk-ranked

## Related skills

- `equity-grant-83b-isos-rsus` — deep dive on grant mechanics + 83(b)
- `fundraising-data-room` — uses Recipe 1 cap-table snapshot
- `investor-update-monthly-quarterly` — board pack uses cap-table summary
- `audit-prep-big4-checklist` — auditors request Recipe 5 ASC 718 waterfall
