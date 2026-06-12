<!--
Source: https://docs.mercury.com/reference/welcome
Source: https://docs.moderntreasury.com/
Source: https://plaid.com/docs/api/
Source: https://johngalt-finance.com/brex-vs-mercury-vs-ramp-business-banking-2026/
-->

# Mercury + Modern Treasury + Plaid — banking & treasury operations

Programmatic banking for startups: Mercury (primary startup bank, ~5% APY treasury, invite-only API), Modern Treasury (multi-bank payment rails), Plaid (read-only account aggregation across 12K+ US institutions).

## When to use

- Pull current cash balance for runway calculation.
- Schedule wires / ACH from operating account.
- Sweep idle cash to treasury (~5% APY as of mid-2026).
- Aggregate balances across multiple bank accounts via Plaid.
- Reconcile bank transactions to GL.
- Trigger phrases: "what's our cash", "send wire", "sweep to treasury", "link bank account", "13-week cash".

NOT for: corp-card transactions (use `ramp-brex-expense-management`); subscription billing receipts (`stripe-revenue-recognition-asc606`); cap-table issuance (`carta-pulley-cap-table`).

## Setup

### Mercury

```bash
# Mercury API is INVITE-ONLY as of 2026.
# 1. Mercury Dashboard → Settings → API → "Request API access"
# 2. Approval typically 2-5 business days
# 3. Generate API key (read-only OR read+write — request explicitly)
export MERCURY_API_KEY="secret-token:..."

# Test
curl -H "Authorization: Bearer $MERCURY_API_KEY" \
  https://api.mercury.com/api/v1/accounts
```

### Modern Treasury

```bash
# Self-serve at app.moderntreasury.com → API Keys
export MODERN_TREASURY_ORG_ID="org_..."
export MODERN_TREASURY_API_KEY="..."

# Test
curl -u "$MODERN_TREASURY_ORG_ID:$MODERN_TREASURY_API_KEY" \
  "https://app.moderntreasury.com/api/connections"
```

### Plaid

```bash
# Get keys at dashboard.plaid.com (free dev tier)
export PLAID_CLIENT_ID="..."
export PLAID_SECRET="..."         # different per env (sandbox / dev / production)
export PLAID_ENV="production"

# Plaid uses Link tokens for user-facing connect, then access tokens for API.
# For controller use: pre-link the company accounts → store access_token.
```

## Common recipes

### Recipe 1 — Pull all account balances (Mercury)

```bash
curl -H "Authorization: Bearer $MERCURY_API_KEY" \
  https://api.mercury.com/api/v1/accounts | jq '.accounts[] | {name, currentBalance, availableBalance}'
```

Returns checking + treasury + savings. `availableBalance` excludes pending; `currentBalance` includes pending.

### Recipe 2 — Pull transactions (Mercury)

```bash
curl -H "Authorization: Bearer $MERCURY_API_KEY" \
  "https://api.mercury.com/api/v1/account/$ACCT_ID/transactions?\
limit=100&start=2026-06-01&end=2026-06-30"
```

Use for monthly close bank-feed reconciliation against Xero/QBO.

### Recipe 3 — Send ACH (Mercury)

```bash
curl -X POST "https://api.mercury.com/api/v1/account/$ACCT_ID/transactions" \
  -H "Authorization: Bearer $MERCURY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "paymentMethod": "ach",
    "recipientId": "$RECIP_ID",
    "amount": 50000.00,
    "note": "Q3 vendor payment — Acme Hosting"
  }'

# Status follows: pending → submitted → sent → completed (or failed)
```

### Recipe 4 — Send wire (Mercury)

```bash
curl -X POST "https://api.mercury.com/api/v1/account/$ACCT_ID/transactions" \
  -H "Authorization: Bearer $MERCURY_API_KEY" \
  -d '{
    "paymentMethod": "wire",
    "recipientId": "$RECIP_ID",
    "amount": 250000.00,
    "note": "Series A close — escrow to seller"
  }'
```

Domestic wires ~$15 fee at Mercury; international ~$50 + FX spread.

### Recipe 5 — Aggregate balances across all banks (Plaid)

```bash
# For each linked account, sync transactions + balance
curl -X POST https://production.plaid.com/transactions/sync \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "'$PLAID_CLIENT_ID'",
    "secret": "'$PLAID_SECRET'",
    "access_token": "'$ACCESS_TOKEN'",
    "cursor": ""
  }'

# Balance only:
curl -X POST https://production.plaid.com/accounts/balance/get \
  -H "Content-Type: application/json" \
  -d '{"client_id":"'$PLAID_CLIENT_ID'","secret":"'$PLAID_SECRET'","access_token":"'$AT'"}'
```

### Recipe 6 — Sweep operating → treasury (Mercury)

```bash
# Step 1: get current operating + treasury balances
OPS_BAL=$(curl -s -H "Authorization: Bearer $MERCURY_API_KEY" \
  "https://api.mercury.com/api/v1/account/$OPS_ID" | jq .availableBalance)

# Step 2: compute sweep amount = operating − operating buffer (e.g., $200K)
SWEEP=$(echo "$OPS_BAL - 200000" | bc)

# Step 3: transfer if positive
if (( $(echo "$SWEEP > 0" | bc -l) )); then
  curl -X POST "https://api.mercury.com/api/v1/account/$OPS_ID/transactions" \
    -H "Authorization: Bearer $MERCURY_API_KEY" \
    -d '{
      "paymentMethod": "internal_transfer",
      "recipientAccountId": "'$TREASURY_ID'",
      "amount": '$SWEEP',
      "note": "Weekly sweep — operating buffer = $200K"
    }'
fi
```

Always require human approval for sweep > $1M (see `monthly-close-procedure` antipattern catalog).

### Recipe 7 — Modern Treasury payment order (multi-bank)

```bash
curl -X POST "https://app.moderntreasury.com/api/payment_orders" \
  -u "$MODERN_TREASURY_ORG_ID:$MODERN_TREASURY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "ach",
    "amount": 100000,
    "direction": "credit",
    "originating_account_id": "$ORIG_ACCT",
    "receiving_account_id": "$RECEIVING_ACCT",
    "currency": "USD",
    "description": "Payroll run 2026-06-30"
  }'
```

Use Modern Treasury when you have multiple banks (e.g., Mercury + Chase + Bank of America) and want one programmatic surface.

### Recipe 8 — Reconcile bank feed → GL

```python
# Pull Mercury txns
import requests, os, datetime
txns = requests.get(
  f"https://api.mercury.com/api/v1/account/{ACCT_ID}/transactions",
  headers={"Authorization": f"Bearer {os.environ['MERCURY_API_KEY']}"},
  params={"limit":500, "start":"2026-06-01", "end":"2026-06-30"}
).json()["transactions"]

# Pull Xero bank transactions for same account
xero_txns = xero.bank_transactions.list(
  where=f'BankAccount.AccountID==Guid("{XERO_MERCURY_ACCT_ID}") AND ' \
        'Date>=DateTime(2026,06,01) AND Date<=DateTime(2026,06,30)'
)

# Match by amount + date ±3d
unmatched_mercury = [m for m in txns if not any(
  abs(m["amount"]) == abs(float(x["Total"])) and
  abs((datetime.datetime.fromisoformat(m["postedAt"]) - x["Date"]).days) <= 3
  for x in xero_txns
)]
print(f"Unmatched Mercury txns: {len(unmatched_mercury)}")
```

### Recipe 9 — Plaid Link token for new bank connection

```bash
# Generate Link token (server-side)
curl -X POST https://production.plaid.com/link/token/create \
  -H "Content-Type: application/json" \
  -d '{
    "client_id":"'$PLAID_CLIENT_ID'",
    "secret":"'$PLAID_SECRET'",
    "client_name":"CraftBot — Finance",
    "country_codes":["US"],
    "language":"en",
    "user":{"client_user_id":"company-id-123"},
    "products":["transactions","auth"]
  }'

# Front-end opens Plaid Link with token; user picks bank + auths.
# Front-end returns public_token to server.
# Server exchanges for access_token:
curl -X POST https://production.plaid.com/item/public_token/exchange \
  -d '{"client_id":"'$PLAID_CLIENT_ID'","secret":"'$PLAID_SECRET'","public_token":"'$PT'"}'

# Persist returned access_token — use for /transactions/sync etc.
```

### Recipe 10 — Compute net burn from bank balances

```python
# Net burn = (opening cash month 1) - (closing cash month 3) / 3
# All accounts summed (operating + treasury + savings)
opening = sum(plaid_balances_as_of("2026-04-01"))
closing = sum(plaid_balances_as_of("2026-06-30"))
net_burn = (opening - closing) / 3
runway_months = closing / net_burn if net_burn > 0 else float("inf")
print(f"Net burn: ${net_burn:,.0f}/mo | Runway: {runway_months:.1f} months")
```

See `runway-burn-analysis` for the full workflow.

## Examples

### Example 1: Weekly cash position update for 13-week forecast

**Goal:** Monday morning cash snapshot to refresh 13-week cash flow.

**Steps:**

1. Pull balances from Mercury (Recipe 1) + any external banks via Plaid (Recipe 5).
2. Sum total cash = operating + treasury + savings + external.
3. Pull last week's transactions (Recipe 2) — categorize into customer collections, AP payments, payroll, other.
4. Update W1 column in 13-week forecast (xlsx) with actuals.
5. Rebase W2-W13 from current date.

**Result:** Cash sheet ready for Monday team review by 9am.

### Example 2: Quarter-end sweep to treasury

**Goal:** Move idle cash to treasury for ~5% APY.

**Steps:**

1. Define operating buffer: 6 weeks of forward outflows from 13-week forecast = $300K.
2. Pull operating balance (Recipe 1) = $1.2M.
3. Compute sweep: $1.2M − $300K = $900K.
4. Surface to founder: "DECISION REQUIRED: sweep $900K from operating to treasury at ~5% APY = $45K/yr opportunity cost if left in checking. Approve?"
5. On approval, execute (Recipe 6).
6. Book journal: Dr Treasury Account / Cr Operating Account $900K.

**Result:** $45K/yr incremental yield captured; operating buffer preserved.

## Edge cases / gotchas

- **Mercury API invite-only:** if denied, fall back to Plaid for read-only aggregation; payments via Mercury web UI.
- **Mercury treasury is NOT FDIC-insured beyond standard limits.** Mercury Treasury invests in money-market funds + T-bills via Vanguard / Morgan Stanley. Per-bank insurance via sweep program. Disclose to founder.
- **Wire cutoff times:** domestic wires must be initiated before 3pm ET (Mercury) for same-day. International before noon ET. Late = next business day.
- **ACH timing:** standard ACH = 2-3 business days; same-day ACH (extra fee at most banks) = same day if before 1pm ET.
- **Plaid product gating:** `transactions` product = $0.30/account/mo; `auth` = $1.50/account; `balance` real-time = $0.10/call. Budget if connecting many accounts.
- **Plaid re-auth:** users must re-authenticate when bank rotates credentials. Set up `ITEM_LOGIN_REQUIRED` webhook → surface to user.
- **Modern Treasury bank counterparty setup:** before sending payments, the receiving account must be set up as a `counterparty`. ~1-day verification cycle for new counterparties.
- **Dual approval:** Mercury supports approver workflow on transactions >$X — configure in dashboard. API can submit + approve as separate calls if delegated.
- **FX exposure:** if you bank in USD and pay foreign vendors, Mercury / Modern Treasury convert at market + spread. For >$50K monthly FX, consider Wise / Airwallex.
- **API key rotation:** rotate every 90 days. Mercury supports multiple active keys for zero-downtime rotation.
- **Pending transactions:** never reconcile against `pending` status — they can be reversed. Wait for `posted` / `completed`.

## Sources

- Mercury API: https://docs.mercury.com/reference/welcome
- Mercury Treasury: https://mercury.com/treasury
- Modern Treasury docs: https://docs.moderntreasury.com/
- Plaid API: https://plaid.com/docs/api/
- Plaid pricing: https://plaid.com/pricing/
- Mercury vs Brex vs Ramp 2026: https://johngalt-finance.com/brex-vs-mercury-vs-ramp-business-banking-2026/
- FDIC sweep program: https://mercury.com/legal/fdic

## Related skills

- `runway-burn-analysis` — uses Recipe 1 + Recipe 10
- `cash-flow-forecasting-13-week` — uses Recipe 1 + Recipe 2 weekly
- `monthly-close-procedure` — uses Recipe 8 for bank reconciliation
- `ramp-brex-expense-management` — card side; complement to bank side
