<!--
Source: https://integrations.expensify.com/Integration-Server/doc/ + https://docs.ramp.com/ + https://developer.brex.com/
Comparison: https://www.softwaresuggest.com/blog/expense-tracking-software-comparison-2026
-->
# Expense Tracking — Expensify / Ramp / Brex — SKILL

File expense reports in <15 minutes: OCR receipts → categorize → reconcile to corp-card txns → submit via REST. Expensify SmartScan owns mainstream receipt OCR; Ramp + Brex own corp-card with auto-reconciliation; Brex was acquired by Capital One April 2026 — API surface evolving.

## When to use this skill

- **"File my expense report" / "submit receipts"** — direct trigger.
- **Post-trip reconciliation** — match receipts to corp-card txns.
- **Recurring monthly expense closeout** — last day of month batch.
- **Personal Schedule C / business deduction tracking** — categorize for tax filing.

**Do NOT use this skill when:**
- Personal-finance budgeting / spend analysis — see `subscription-tracker-cancellation` + `actual-budget-mcp`.
- Receipt-only archival (no expense report) — use `invoice-organizer` + `file-organizer`.
- Tax filing itself — defer to licensed CPA. (See `role.md` closing rules.)

## Pick the right tool

| Profile | Recommendation | Why |
|---|---|---|
| Mainstream SMB or consumer, mainly need receipt → report | **Expensify** | SmartScan OCR + auto-categorize + auto-submit |
| Series-A+ company, need corp-card + auto-reconcile | **Ramp** | Free corp card + spend mgmt + AI close |
| Startup, need card + integrations + (post-Capital One) | **Brex** | Strong AP automation; Cap One acq Apr 2026 |
| Enterprise T&E with SAP | **Concur** | Old guard; SAP-owned |
| Receipt-only OCR for accountants | **Dext** | Receipt Bank lineage |

## Setup

### Expensify (REST — Integration Server)

```bash
# Generate Partner ID + Partner Secret in policy admin:
# https://www.expensify.com/admin/policies?param=integrations
export EXPENSIFY_PARTNER_USER_ID="<id>"
export EXPENSIFY_PARTNER_USER_SECRET="<secret>"
```

Docs: https://integrations.expensify.com/Integration-Server/doc/

### Ramp (REST API)

```bash
# Generate Client ID + Secret at https://app.ramp.com/developer
export RAMP_CLIENT_ID="<id>"
export RAMP_CLIENT_SECRET="<secret>"

# OAuth client credentials
RAMP_TOKEN=$(curl -s https://api.ramp.com/developer/v1/token \
  -u "$RAMP_CLIENT_ID:$RAMP_CLIENT_SECRET" \
  -d "grant_type=client_credentials&scope=transactions:read receipts:write" \
  | jq -r .access_token)

curl -s https://api.ramp.com/developer/v1/transactions \
  -H "Authorization: Bearer $RAMP_TOKEN"
```

Docs: https://docs.ramp.com/

### Brex (REST API — note: Capital One transition Apr 2026)

```bash
# Generate at https://dashboard.brex.com/developer
export BREX_USER_TOKEN="<token>"
curl -s https://platform.brexapis.com/v2/transactions/card \
  -H "Authorization: Bearer $BREX_USER_TOKEN"
```

Docs: https://developer.brex.com/

### OCR — gemini-ocr-mcp or mistral-ocr-mcp

Both wired in `mcp_servers`. Use whichever has the user's key.

## Common recipes

### Recipe 1: OCR a receipt image

```bash
mcp tool gemini-ocr.extract \
  --image-path "/tmp/receipt_2026-06-09_starbucks.jpg" \
  --schema '{"vendor":"","amount":0,"date":"","payment_last4":"","category_hint":""}'
```

Returns structured fields: vendor, amount, date, payment_last4, category_hint.

### Recipe 2: Categorize per policy

```python
CATEGORIES = {
    'United|Delta|American|Alaska|Southwest|JetBlue': 'Travel - Airfare',
    'Marriott|Hilton|Hyatt|IHG|Accor': 'Travel - Lodging',
    'Uber|Lyft|Taxi': 'Travel - Ground',
    'Starbucks|Cafe|Coffee': 'Meals & Entertainment',
    'Office Depot|Staples|Amazon Business': 'Office Expenses',
}
import re
def categorize(vendor):
    for pat, cat in CATEGORIES.items():
        if re.search(pat, vendor, re.I): return cat
    return 'Misc'
```

See role.md for the full Expensify category mapping table.

### Recipe 3: Push a single receipt to Expensify

```bash
# Expensify CreateTransactions API call
curl -X POST 'https://integrations.expensify.com/Integration-Server/ExpensifyIntegrations' \
  -d "requestJobDescription={
    \"type\":\"create\",
    \"credentials\":{\"partnerUserID\":\"$EXPENSIFY_PARTNER_USER_ID\",\"partnerUserSecret\":\"$EXPENSIFY_PARTNER_USER_SECRET\"},
    \"inputSettings\":{
      \"type\":\"transactionCreator\",
      \"transactionList\":[{
        \"created\":\"2026-06-09\",
        \"merchant\":\"Starbucks\",
        \"amount\":725,
        \"currency\":\"USD\",
        \"category\":\"Meals & Entertainment\",
        \"tag\":\"Trip-NYC-Jun2026\"
      }]
    }
  }"
```

Note: Expensify amounts are in cents.

### Recipe 4: Pull Ramp transactions for a date range

```bash
curl -s 'https://api.ramp.com/developer/v1/transactions?from=2026-06-01&to=2026-06-30&page_size=200' \
  -H "Authorization: Bearer $RAMP_TOKEN" \
  | jq '.data[] | {id, merchant_name, amount, posted_at, sk_category}'
```

### Recipe 5: Attach receipt to a Ramp transaction

```bash
TXN_ID="<ramp-txn-id>"
curl -X POST "https://api.ramp.com/developer/v1/transactions/$TXN_ID/receipts" \
  -H "Authorization: Bearer $RAMP_TOKEN" \
  -F "file=@/tmp/receipt.jpg"
```

### Recipe 6: Pull Brex card transactions

```bash
curl -s 'https://platform.brexapis.com/v2/transactions/card?posted_at_start=2026-06-01' \
  -H "Authorization: Bearer $BREX_USER_TOKEN" \
  | jq '.items[] | {id, merchant_name, amount, posted_at}'
```

### Recipe 7: Match receipts to corp-card txns (Python)

```python
import requests, os, datetime
def fetch_ramp_txns(start, end):
    r = requests.get(f"https://api.ramp.com/developer/v1/transactions?from={start}&to={end}&page_size=200",
                     headers={"Authorization":f"Bearer {os.environ['RAMP_TOKEN']}"})
    return r.json().get('data', [])

receipts = [...]  # from OCR
txns = fetch_ramp_txns("2026-06-01", "2026-06-30")
matched, orphans = [], []
for txn in txns:
    cand = [r for r in receipts
            if abs(r['amount'] - abs(txn['amount'])) < 0.5
            and r['vendor'].lower() in txn['merchant_name'].lower()]
    if cand: matched.append((txn, cand[0]))
    else: orphans.append(txn)
print(f"{len(matched)} matched, {len(orphans)} orphans")
```

### Recipe 8: Create an Expensify report from transactions

```bash
curl -X POST 'https://integrations.expensify.com/Integration-Server/ExpensifyIntegrations' \
  -d "requestJobDescription={
    \"type\":\"create\",
    \"credentials\":{\"partnerUserID\":\"$EXPENSIFY_PARTNER_USER_ID\",\"partnerUserSecret\":\"$EXPENSIFY_PARTNER_USER_SECRET\"},
    \"inputSettings\":{
      \"type\":\"reportCreator\",
      \"reportName\":\"Trip NYC Jun 2026\",
      \"transactionListIDs\":[123,124,125]
    }
  }"
```

### Recipe 9: Submit the report for approval

```bash
curl -X POST 'https://integrations.expensify.com/Integration-Server/ExpensifyIntegrations' \
  -d "requestJobDescription={
    \"type\":\"create\",
    \"credentials\":{\"partnerUserID\":\"$EXPENSIFY_PARTNER_USER_ID\",\"partnerUserSecret\":\"$EXPENSIFY_PARTNER_USER_SECRET\"},
    \"inputSettings\":{
      \"type\":\"reportSubmitter\",
      \"reportID\":\"<report-id>\"
    }
  }"
```

### Recipe 10: Batch OCR a folder of receipts

```bash
for f in ~/Documents/Receipts/2026-06/*.{jpg,png,pdf}; do
  mcp tool gemini-ocr.extract --image-path "$f" \
    --schema '{"vendor":"","amount":0,"date":"","payment_last4":"","category_hint":""}' \
    > "${f}.json"
done

# Consolidate
jq -s '.' ~/Documents/Receipts/2026-06/*.json > receipts_june.json
```

### Recipe 11: Reconcile orphan corp-card txns (no receipt found)

```bash
# Surface orphans for user to chase
echo "Orphan transactions needing receipts:"
jq -r '.[] | "\(.posted_at) \(.merchant_name) $\(.amount/100)"' orphans.json
```

Then `gmail-mcp` to draft "where's the receipt" email to user with the list.

### Recipe 12: Personal Schedule C-style categorization

For 1099 contractor / sole prop deductions:

```python
SCHED_C = {
    'Internet|Comcast|AT&T|Verizon': 'Utilities (Home Office %)',
    'Adobe|GitHub|Notion|Linear|Figma': 'Software',
    'United|Delta|Marriott|Uber': 'Travel',
    'Starbucks|Restaurant': 'Meals (50% deductible)',
    'AWS|GCP|Azure|Vercel': 'Cloud / Computing',
    'Coursera|Udemy|Pluralsight': 'Professional Development',
}
```

Push to `xero-mcp` for personal books.

## Examples

### Example 1: Post-trip 15-min closeout

**Goal:** Just got back from 4-day NYC trip; 18 receipts in photos folder + 22 corp-card txns.

**Steps:**
1. Recipe 10: batch OCR all 18 receipts → 18 JSON.
2. Recipe 4: pull Ramp txns for trip date range → 22 txns.
3. Recipe 7: match receipts to txns → 16 matched + 2 orphan txns + 2 orphan receipts.
4. Recipe 11: surface 2 orphan txns to user for "what was this?".
5. For unmatched receipts: confirm cash/personal-card; tag.
6. Recipe 3: push 18 receipts to Expensify.
7. Recipe 8: create "Trip NYC Jun 2026" report.
8. Recipe 9: submit for approval.
9. Archive receipts to `file-organizer` Trip-NYC-Jun2026 folder.

**Result:** Report submitted in ~12 min; orphans flagged for user.

### Example 2: Monthly close — solo founder

**Goal:** End of June 2026; categorize all month's spend; push to Xero personal books.

**Steps:**
1. Recipe 4: pull all Ramp txns June.
2. Recipe 12: Schedule C categorize.
3. `xero-mcp.create_bank_transactions`: push to Xero with categories.
4. `gmail-mcp`: forward monthly summary email to user + CPA.

**Result:** Month closed; CPA has data for quarterly estimate.

### Example 3: Brex transition contingency

**Goal:** User on Brex; April 2026 Capital One acquisition — verify API still functional.

**Steps:**
1. Recipe 6: smoke-test Brex API.
2. If 403/404 returned, surface migration note: "Brex API transitioning to Capital One; legacy Brex tokens valid through Q4 2026; new client credential exchange required after."
3. Recommend dual-track: Recipe 4 (Ramp) as primary forward; Brex API as fallback while transition in progress.

**Result:** Resilient closeout regardless of transition timing.

## Edge cases / gotchas

- **Expensify amounts in cents**: $7.25 → 725. Forget this and your numbers are 100× off.
- **Expensify report-by-trip vs by-month**: Decide once + stick. Mixing creates duplicate-receipt problems.
- **Ramp scopes**: `transactions:read`, `receipts:write`, `reimbursements:read` are common. Mismatched scope → 403.
- **Brex post-acquisition**: APIs likely change Q3-Q4 2026. Monitor https://developer.brex.com/changelog before any production use.
- **OCR confidence threshold**: Both gemini-ocr-mcp and mistral-ocr-mcp return per-field confidence. Below 0.85 → surface receipt for human-verify, not auto-categorize.
- **Currency**: Foreign receipts → ensure `currency` field is set correctly. Auto-categorize doesn't FX-convert; let Expensify or Ramp handle FX.
- **Tax category vs expense category**: Two-tier categorization. Schedule C uses tax categories (Meals 50%, Travel 100%) — distinct from internal expense categories. Map both.
- **PII on receipts**: Receipts often have last-4 of card, signature, etc. Don't archive to public bucket — use private `file-organizer` folder.
- **Duplicate receipts**: User photographs same receipt twice. Dedup by vendor + amount + date + last-4 before push.
- **Refunds**: Negative amounts in Ramp/Brex txns. Match to original receipt as "refund"; don't create new report line.
- **Personal vs business mixed**: If corp card was used for personal, must be reimbursed to company. Tag explicitly + Reimbursement Required.
- **CPA / attorney boundary**: Tax filing itself NOT in scope. Defer to licensed CPA always — see role.md closing rules.
- **Receipt aging**: Some companies require submission within 30 days of charge. Track `posted_at` + nudge user.

## Sources

- [Expensify Integration Server](https://integrations.expensify.com/Integration-Server/doc/)
- [Ramp docs](https://docs.ramp.com/)
- [Brex Developer](https://developer.brex.com/)
- [SoftwareSuggest expense comparison 2026](https://www.softwaresuggest.com/blog/expense-tracking-software-comparison-2026)
- [Concur (alt enterprise)](https://www.concur.com/)
- [Dext / Receipt Bank](https://dext.com/)
