<!--
Source: https://docs.ramp.com/developer-api/v1/overview
Source: https://developer.brex.com/
Source: https://johngalt-finance.com/brex-vs-mercury-vs-ramp-business-banking-2026/
Note: Brex acquired by Capital One Jan 2026 ($5.15B); API surface evolving through mid-2026 close.
-->

# Ramp + Brex — expense management, corp cards, AP automation

Programmatic access to corp-card transactions, receipts, policy enforcement, vendor onboarding, and AP automation. Ramp leads expense management (5-10 hrs/wk saved per Tropic benchmark); Brex multi-entity + 50+ countries (acquired by Capital One Jan 2026, $5.15B, close mid-2026).

## When to use

- Pull card transaction data into Xero/QBO close.
- Match receipts to transactions; enforce capture policy.
- Issue / freeze / set limits on virtual + physical cards.
- Vendor onboarding + AP bill payment automation.
- Reimbursement workflow.
- Trigger phrases: "card spend", "expense report", "receipt match", "vendor pay run", "set card limit".

NOT for: bank-account treasury (use `mercury-modern-treasury-banking`); cap-table grants (use `carta-pulley-cap-table`); subscription billing (use `stripe-revenue-recognition-asc606`).

## Setup

### Ramp

```bash
# 1. Dashboard → Settings → Developer → Generate API key
export RAMP_CLIENT_ID="..."
export RAMP_CLIENT_SECRET="..."

# 2. Get access token (OAuth client credentials grant)
TOKEN=$(curl -s -X POST https://api.ramp.com/developer/v1/token \
  -u "$RAMP_CLIENT_ID:$RAMP_CLIENT_SECRET" \
  -d "grant_type=client_credentials&scope=transactions:read cards:write users:read")
export RAMP_API_TOKEN=$(echo $TOKEN | jq -r .access_token)
```

Scopes: `transactions:read`, `cards:write`, `users:read`, `reimbursements:read`, `bills:write`, etc. Lock scopes per role.

### Brex

```bash
# Dashboard → Developer → Create app → OAuth or User Token
export BREX_TOKEN="..."

# Test
curl -H "Authorization: Bearer $BREX_TOKEN" \
  https://platform.brexapis.com/v2/transactions/card
```

Note: Brex API in transition post-Capital One. Plan for endpoint changes through Q3 2026.

## Common recipes

### Recipe 1 — Pull card transactions (Ramp)

```bash
curl -H "Authorization: Bearer $RAMP_API_TOKEN" \
  "https://api.ramp.com/developer/v1/transactions?\
from_date=2026-06-01&to_date=2026-06-30&page_size=100&\
order_by_date_desc=true"
```

Returns: `merchant_name`, `amount`, `card_holder`, `category`, `receipt_url`, `policy_violation`, `accounting_field_selections`.

### Recipe 2 — Pull card transactions (Brex)

```bash
curl -H "Authorization: Bearer $BREX_TOKEN" \
  "https://platform.brexapis.com/v2/transactions/card?\
posted_at_start=2026-06-01T00:00:00Z&posted_at_end=2026-06-30T23:59:59Z&\
limit=100"
```

### Recipe 3 — Issue virtual card (Ramp)

```bash
curl -X POST "https://api.ramp.com/developer/v1/cards" \
  -H "Authorization: Bearer $RAMP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "$USER_ID",
    "spending_restrictions": {
      "amount": 50000,
      "interval": "MONTHLY",
      "categories": [],
      "vendor_blacklist": [],
      "vendor_whitelist": ["aws.amazon.com","openai.com"]
    },
    "display_name": "AWS / OpenAI — Eng — Jane"
  }'
```

### Recipe 4 — Issue card (Brex)

```bash
curl -X POST "https://platform.brexapis.com/v2/cards" \
  -H "Authorization: Bearer $BREX_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "owner": { "type": "USER", "user_id": "$USER_ID" },
    "card_name": "Brex Virtual — Software",
    "card_type": "VIRTUAL",
    "limit_type": "RECURRING",
    "limit": { "amount": 100000, "currency": "USD" },
    "limit_interval": "MONTHLY"
  }'
```

### Recipe 5 — Set GL coding rule (Ramp)

```bash
# Auto-tag merchant to GL account in Xero/QBO
curl -X POST "https://api.ramp.com/developer/v1/accounting/rules" \
  -H "Authorization: Bearer $RAMP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "merchant_name_contains": "AWS",
    "default_gl_account_id": "$XERO_HOSTING_ACCT_ID",
    "default_class": "Engineering"
  }'
```

### Recipe 6 — Upload + match receipt (Ramp)

```bash
curl -X POST "https://api.ramp.com/developer/v1/transactions/$TXN_ID/receipts" \
  -H "Authorization: Bearer $RAMP_API_TOKEN" \
  -F "receipt=@/path/to/receipt.jpg"
```

Auto-matches via Ramp's OCR. For broken matches → escalate to `gemini-ocr-mcp` / `mistral-ocr-mcp`.

### Recipe 7 — Find missing-receipt transactions

```bash
curl -H "Authorization: Bearer $RAMP_API_TOKEN" \
  "https://api.ramp.com/developer/v1/transactions?\
has_receipt=false&from_date=2026-06-01&to_date=2026-06-30&\
amount_min=2500"   # IRS substantiation threshold = $75; we set higher for policy
```

### Recipe 8 — Vendor + AP bill (Ramp Bill Pay)

```bash
# Create vendor
curl -X POST "https://api.ramp.com/developer/v1/bills/vendors" \
  -H "Authorization: Bearer $RAMP_API_TOKEN" \
  -d '{ "name":"Acme Hosting","email":"ar@acmehost.com","payment_method":"ACH" }'

# Create bill
curl -X POST "https://api.ramp.com/developer/v1/bills" \
  -H "Authorization: Bearer $RAMP_API_TOKEN" \
  -d '{ "vendor_id":"$VEND_ID","amount":12000,"currency":"USD",
        "due_date":"2026-07-15","line_items":[{
          "amount":12000,"gl_account_id":"$ACCT","memo":"June hosting"
        }] }'

# Approve + pay
curl -X POST "https://api.ramp.com/developer/v1/bills/$BILL_ID/approve" \
  -H "Authorization: Bearer $RAMP_API_TOKEN"
```

### Recipe 9 — Reimbursement workflow (Ramp)

```bash
# Pull pending reimbursements
curl -H "Authorization: Bearer $RAMP_API_TOKEN" \
  "https://api.ramp.com/developer/v1/reimbursements?status=PENDING_APPROVAL"

# Approve
curl -X POST "https://api.ramp.com/developer/v1/reimbursements/$REIMB_ID/approve" \
  -H "Authorization: Bearer $RAMP_API_TOKEN"
```

### Recipe 10 — Sync Ramp/Brex → Xero monthly

```python
# Pull all closed transactions for period
import requests, os
txns = requests.get(
  "https://api.ramp.com/developer/v1/transactions",
  headers={"Authorization": f"Bearer {os.environ['RAMP_API_TOKEN']}"},
  params={"from_date":"2026-06-01","to_date":"2026-06-30","page_size":200}
).json()

# Map each to Xero bank transaction
for t in txns["data"]:
    xero.bank_transactions.create({
      "type":"SPEND",
      "contact":{"name": t["merchant_name"]},
      "lineItems":[{
        "description": f"Ramp: {t['merchant_name']} — {t['memo']}",
        "unitAmount": t["amount"],
        "accountCode": t["accounting_field_selections"]["gl_account_id"]
      }],
      "bankAccount":{"accountID": "$RAMP_CARD_ACCT"},
      "date": t["transaction_date"],
      "reference": t["id"]
    })
```

## Examples

### Example 1: Monthly close — pull and book all Ramp card spend

**Goal:** All June 2026 Ramp card transactions in Xero by close day 3.

**Steps:**

1. Pull transactions (Recipe 1) for 2026-06-01 → 2026-06-30.
2. For each txn without receipt + amount >$75: flag for cardholder action (gmail).
3. For each txn with policy violation: flag for manager review.
4. Apply GL coding rules (Recipe 5 results) → 90%+ should be auto-coded.
5. Push to Xero (Recipe 10).
6. Reconcile: Ramp total spend = Xero "Ramp Card" bank-feed account total.

**Result:** All card spend booked + tied; flagged exceptions sent to humans.

### Example 2: New hire — issue Ramp card with budget

**Goal:** Engineering hire needs $500/mo for AWS personal account + $50/mo for AI tools, no other categories.

**Steps:**

1. Create Ramp user via `/users` POST.
2. Issue card (Recipe 3) with `amount: 55000` (cents = $550), `interval: MONTHLY`, `vendor_whitelist: ["aws.amazon.com","openai.com","anthropic.com"]`.
3. Set policy: receipt required >$25, auto-coded to "R&D — Software & Subscriptions".
4. Card ships physical + virtual immediately available in dashboard.

**Result:** Controlled spend with auto-coding; no monthly approval needed.

## Edge cases / gotchas

- **Brex API in transition (2026):** Capital One acquisition closes mid-2026. Some endpoints may be deprecated; subscribe to `developer.brex.com` changelog. Plan for 30-day deprecation notices.
- **Rate limits:** Ramp 1000 req/min; Brex 600 req/min. Cache where possible.
- **Webhook delivery delays:** transactions are typically posted within 1-2 days of swipe; pending vs posted differ on the API. For close, use `posted_at` ≤ cutoff, not `created_at`.
- **Receipt OCR confidence:** Ramp's auto-match accuracy ~95%. Always sample-review high-dollar (>$1000) auto-matches.
- **Policy violations are warnings, not blocks:** Ramp + Brex allow transactions through and flag them. If you need hard blocks, set vendor blocklists or spending category restrictions on the card itself.
- **Cardholder vs user IDs:** Ramp `user_id` is org-scoped; same person at different orgs has different IDs. Don't cross-reference.
- **Currency mismatch:** virtual cards transact in card-issue currency. Foreign-merchant txns get FX-converted (typically 0% Ramp, 0% Brex for first $X, then 1%).
- **Reimbursement timing:** approved reimbursements process via ACH = 1-3 business days. Plan close with ACH cutoff in mind.
- **Bill Pay approval thresholds:** set 2-person approval on bills >$10K (Ramp `approval_chain`). Standard SOX-lite policy.
- **GL coding sync direction:** Ramp can push or pull GL accounts. Pull is recommended (Xero/QBO is source of truth for CoA).
- **Closed cards still queryable:** terminated cards retain transaction history; include `card_status=ALL` if you want closed/cancelled card txns.

## Sources

- Ramp Developer API: https://docs.ramp.com/developer-api/v1/overview
- Brex Developer Platform: https://developer.brex.com/
- Ramp vs Brex vs Mercury 2026: https://johngalt-finance.com/brex-vs-mercury-vs-ramp-business-banking-2026/
- Capital One acquires Brex (Jan 2026): https://www.capitalone.com/about/newsroom/capital-one-brex/
- Tropic 2025 SaaS spend trends: https://www.tropicapp.io/reports/software-spending-trends-2025

## Related skills

- `mercury-modern-treasury-banking` — bank-account side; cash management
- `ar-ap-aging-collections` — AP bill side; Recipe 8 plugs into the close
- `monthly-close-procedure` — Recipe 10 is the close-day-3 step
- `vendor-procurement-saas-spend-audit` — uses Ramp transaction data for spend audit
