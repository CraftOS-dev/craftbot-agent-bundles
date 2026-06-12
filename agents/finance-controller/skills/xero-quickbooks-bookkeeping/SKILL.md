<!--
Source: https://github.com/intuit/quickbooks-online-mcp-server (143 tools, 11 reports)
Source: https://github.com/XeroAPI/xero-mcp-server (official Xero MCP)
Source: https://www.apideck.com/blog/claude-code-accounting-integrations
-->

# Xero + QuickBooks Online — bookkeeping CRUD and reports

Official MCP wrappers for the two dominant SMB accounting platforms. Xero MCP (`@xeroapi/xero-mcp-server`) covers Contacts / Invoices / Bills / BankTransactions / Reports / Journals. Intuit QBO MCP (`intuit/quickbooks-online-mcp-server`) wraps 143 tools across 29 entities with 11 financial reports.

## When to use

- Daily / weekly bookkeeping: create invoices, bills, payments, journal entries.
- Pull monthly close reports: P&L, Balance Sheet, Cash Flow, Aged Receivables, Aged Payables, Trial Balance.
- Reconcile bank-feed lines to ledger entries.
- Read chart of accounts; set up a new CoA from a SaaS template.
- Bridge data into 13-week cash forecast or unit-economics models.
- Trigger phrases: "close the books", "pull P&L", "create invoice", "what's our AR", "reconcile bank".

Do NOT use for: ASC 606 deferred-revenue schedules (use `stripe-revenue-recognition-asc606`), cap-table accounting (use `carta-pulley-cap-table`), or expense card transactions (use `ramp-brex-expense-management`).

## Setup

### Xero (preferred path — Maton-managed OAuth gateway already ships)

```bash
# The default `xero` skill uses Maton's OAuth gateway — no per-recipient OAuth
# setup required. Enable `xero-mcp` in CraftBot MCP settings; recipient
# authorizes once via the Xero consent screen.
```

If self-hosting the MCP:

```bash
npx -y @xeroapi/xero-mcp-server@latest
# Auth: PKCE flow via developer.xero.com
# Env: XERO_CLIENT_ID, XERO_CLIENT_SECRET, XERO_REDIRECT_URI
```

### QuickBooks Online (Intuit official MCP)

```bash
git clone https://github.com/intuit/quickbooks-online-mcp-server
cd quickbooks-online-mcp-server
npm install && npm run build
# Auth: OAuth 2.0 from developer.intuit.com → Create App → "Accounting" scope
export QBO_CLIENT_ID="..."
export QBO_CLIENT_SECRET="..."
export QBO_REDIRECT_URI="https://localhost:8080/callback"
export QBO_ENVIRONMENT="production"   # or "sandbox" for dev
export QBO_REALM_ID="..."             # Company ID surfaced after OAuth
```

Auth scopes required: `com.intuit.quickbooks.accounting` (read+write).

## Common recipes

### Recipe 1 — Pull current-month P&L (Xero)

```javascript
// via xero-mcp tool surface
xero.reports.profit_and_loss({
  fromDate: "2026-06-01",
  toDate: "2026-06-30",
  periods: 1,
  timeframe: "MONTH",
  trackingCategoryId: null,        // omit for unsegmented
  standardLayout: true
})
```

### Recipe 2 — Pull current-month P&L (QBO)

```bash
# via cli-anything → Intuit MCP
uvx --from intuit-quickbooks-mcp qbo-mcp-server \
  --report profit_and_loss \
  --start 2026-06-01 --end 2026-06-30 \
  --realm $QBO_REALM_ID
```

REST equivalent:

```bash
curl -H "Authorization: Bearer $QBO_TOKEN" \
  -H "Accept: application/json" \
  "https://quickbooks.api.intuit.com/v3/company/$QBO_REALM_ID/reports/ProfitAndLoss?start_date=2026-06-01&end_date=2026-06-30"
```

### Recipe 3 — Aged Receivables for dunning

```javascript
xero.reports.aged_receivables_by_contact({
  date: "2026-06-30",
  fromDate: null,
  toDate: null
})
```

QBO equivalent: `report_aged_receivables` with `aging_period=30` and `aging_method=Report_Date`.

### Recipe 4 — Create invoice (Xero)

```javascript
xero.invoices.create({
  type: "ACCREC",                  // Accounts Receivable
  contact: { contactID: "$customerId" },
  lineItems: [{
    description: "Pro tier — June 2026",
    quantity: 1,
    unitAmount: 99.00,
    accountCode: "200",            // Sales (per CoA)
    taxType: "OUTPUT"              // or NONE; jurisdiction-dependent
  }],
  date: "2026-06-01",
  dueDate: "2026-07-01",           // net-30
  reference: "INV-2026-0612",
  status: "AUTHORISED"             // or "DRAFT"
})
```

### Recipe 5 — Bank reconciliation (match bank-feed → ledger)

```javascript
// 1. Pull unreconciled bank transactions
const lines = await xero.bank_transactions.list({
  where: 'IsReconciled==false AND BankAccount.AccountID==Guid("$bankAcctId")'
});
// 2. For each line, find matching invoice/bill by amount + date window ±3d
// 3. Allocate via xero.invoices.payments.create or xero.bills.payments.create
xero.payments.create({
  invoice: { invoiceID: "$invoiceId" },
  account: { accountID: "$bankAcctId" },
  date: "2026-06-15",
  amount: 99.00,
  reference: "Bank xfer 2026-06-15"
});
```

### Recipe 6 — Post a manual journal entry

```javascript
// Deferred revenue release (ASC 606 monthly recognition)
xero.manual_journals.create({
  narration: "2026-06-30 | ACCRUAL | Deferred revenue release — Customer X",
  date: "2026-06-30",
  status: "POSTED",
  journalLines: [
    { lineAmount: -1000.00, accountCode: "210", description: "Dr Deferred Revenue" },
    { lineAmount:  1000.00, accountCode: "200", description: "Cr Revenue — SaaS" }
  ]
});
```

### Recipe 7 — Trial Balance (QBO)

```bash
curl -H "Authorization: Bearer $QBO_TOKEN" \
  "https://quickbooks.api.intuit.com/v3/company/$QBO_REALM_ID/reports/TrialBalance?date_macro=Last+Month"
```

Use this for monthly close tie-out: every BS account total must equal subledger total to the penny.

### Recipe 8 — Set up SaaS chart of accounts

Standard SaaS CoA (recipient swaps account numbers per platform):

```
1xxx Assets
  1000 Cash — Operating
  1010 Cash — Treasury (sweep)
  1100 Accounts Receivable
  1110 Allowance for Doubtful Accounts
  1200 Prepaid Expenses
  1500 PP&E (capitalized hardware / leasehold)
  1510 Accumulated Depreciation
2xxx Liabilities
  2000 Accounts Payable
  2100 Accrued Expenses
  2110 Accrued Payroll
  2200 Sales Tax Payable
  2300 Deferred Revenue — Current
  2310 Deferred Revenue — Long-term
3xxx Equity
  3000 Common Stock
  3010 Preferred Stock — Seed
  3500 Retained Earnings
4xxx Revenue
  4000 SaaS Subscription Revenue
  4100 Professional Services Revenue
  4200 Usage / Overage Revenue
5xxx COGS
  5000 Hosting (AWS / GCP)
  5050 Third-party APIs (LLM inference, etc.)
  5100 Customer Support — Salaries
  5200 Payment Processing Fees
6xxx OpEx
  6000 S&M — Salaries
  6010 S&M — Marketing programs
  6100 R&D — Salaries
  6200 G&A — Salaries
  6300 G&A — Rent / utilities / SaaS subscriptions
```

### Recipe 9 — Cash Flow (indirect method) from QBO

```bash
curl -H "Authorization: Bearer $QBO_TOKEN" \
  "https://quickbooks.api.intuit.com/v3/company/$QBO_REALM_ID/reports/CashFlow?start_date=2026-06-01&end_date=2026-06-30&summarize_column_by=Month"
```

### Recipe 10 — Bulk export GL detail for audit

```javascript
// Xero — pull general ledger journal export
xero.journals.list({
  ifModifiedSince: "2026-01-01T00:00:00Z",
  offset: 0
});
// Returns batches of 100 — iterate until empty
```

## Examples

### Example 1: Full monthly close — pull all reports in one batch

**Goal:** Generate close package for June 2026.

**Steps:**

1. Confirm cutoff: ensure all June bank transactions imported.
2. Pull P&L (Recipe 1).
3. Pull Balance Sheet:
   ```javascript
   xero.reports.balance_sheet({ date: "2026-06-30", standardLayout: true });
   ```
4. Pull Cash Summary:
   ```javascript
   xero.reports.cash_summary({ fromDate: "2026-06-01", toDate: "2026-06-30" });
   ```
5. Pull Aged AR + Aged AP (Recipe 3).
6. Pull Trial Balance:
   ```javascript
   xero.reports.trial_balance({ date: "2026-06-30" });
   ```
7. Verify A = L + E to the penny (tie-out check).
8. Export each to xlsx via `xlsx` skill; bundle into `06_2026_close.zip`.

**Result:** Close package with 6 tied-out reports ready for review.

### Example 2: Migrate from QBO → Xero (one-time)

**Goal:** Switch accounting platform with no data loss.

**Steps:**

1. Pull GL detail from QBO (Recipe 10 equivalent: `query=SELECT * FROM JournalEntry`).
2. Pull contacts (customers + vendors): QBO `query=SELECT * FROM Customer` and `Vendor`.
3. Build CoA mapping (QBO account → Xero account code).
4. Push contacts to Xero via `xero.contacts.create` batch.
5. Push opening trial balance via `xero.manual_journals.create` (single journal at conversion date).
6. Reconcile: re-pull TB from Xero, diff against QBO TB, tie out.

**Result:** Xero set up with QBO opening balances and contacts; recipient runs both platforms for 1 month to verify, then deprecates QBO.

## Edge cases / gotchas

- **OAuth token refresh:** Xero tokens expire in 30 min; refresh tokens in 60 days unless used. Intuit QBO tokens expire in 1 hour; refresh in 100 days. Set up auto-refresh in MCP host or expect failed calls.
- **Idempotency:** Xero supports `Idempotency-Key` header on creates; QBO uses `requestid` query param. Always set this on POSTs to prevent duplicate invoices if the call retries.
- **Rate limits:** Xero is 60 calls/min + 5K calls/day per tenant. QBO is 500 requests/minute, 10 requests/second per realm. Batch reads when possible (`page=1&pageSize=100`).
- **Multi-currency:** Xero has Multi-Currency add-on (~$54/mo for Established plan); QBO has it in higher tiers. If the company sells in multiple currencies, confirm the plan supports it before booking foreign-currency invoices.
- **Tracking categories (Xero) vs Classes/Locations (QBO):** for departmental P&L splits. Set these up before back-dating transactions — re-tagging old transactions is painful.
- **Manual journals vs invoices:** never use manual journals to record AR / AP movements that should be tracked in the subledger — it bypasses aging reports. Always use invoices/bills for trackable items; reserve manual journals for accruals, depreciation, equity, and reclasses.
- **Stale OAuth scopes:** If the recipient added a feature (e.g., projects in Xero) after first connect, re-consent is needed. Surface a "reconnect Xero" prompt rather than silently failing.
- **Locked periods:** Both platforms support period locks. If recipient locks 2026-06 and you try to post a 2026-06-30 journal, the call fails. Either request a temporary unlock or post the adjustment in the open period with a clear narration referencing the locked-period origin.
- **QBO sandbox vs production:** sandbox tokens won't authenticate against production endpoints. Verify `QBO_ENVIRONMENT` before any write.
- **Bank-feed delay:** Xero / QBO bank feeds typically lag 24-48 hours. For weekly cash-flow updates, supplement with direct Plaid pull (see `mercury-modern-treasury-banking`).

## Sources

- Intuit QuickBooks Online MCP Server: https://github.com/intuit/quickbooks-online-mcp-server
- Xero MCP Server (official): https://github.com/XeroAPI/xero-mcp-server
- Xero Accounting API: https://developer.xero.com/documentation/api/accounting/overview
- Intuit QBO API: https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/account
- Reports API (Xero): https://developer.xero.com/documentation/api/accounting/reports
- Reports API (QBO): https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/reports
- Apideck accounting integrations guide: https://www.apideck.com/blog/claude-code-accounting-integrations

## Related skills

- `stripe-revenue-recognition-asc606` — when invoices represent multi-month obligations
- `ar-ap-aging-collections` — uses the aged AR/AP outputs from Recipe 3
- `monthly-close-procedure` — orchestrates Recipe 1+2+3+9 into the full close package
- `audit-prep-big4-checklist` — uses Recipe 10 GL export for PBC submissions
