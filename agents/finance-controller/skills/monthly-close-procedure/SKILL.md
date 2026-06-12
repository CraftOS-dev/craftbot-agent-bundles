<!--
Source: https://pilot.com/platform/ai-accountant
Source: https://www.numeric.io/
Source: https://www.truewind.ai/
Source: https://www.articsledge.com/post/ai-accounting-tools
Reference role.md: "Monthly close playbook" section
-->

# Monthly close procedure — 5-10 day close

End-to-end monthly close procedure: cutoff → reconcile → accrue → tie-out → report. Modern AI-assisted close vendors (Pilot AI Accountant Feb 2026, Numeric.io, Truewind 47% automation) supplement but don't replace the discipline.

## When to use

- Every month at cutoff (typically day 1 of new month).
- Period-end (quarterly, annual) close — same procedure, deeper review.
- First close at a new entity (build the runbook).
- Audit prep — close discipline is the audit's first pass.
- Trigger phrases: "close the books", "month-end", "tie out", "accrue", "trial balance".

NOT for: ad-hoc snapshot reports (use `xero-quickbooks-bookkeeping` for raw report pulls). NOT for tax provision (separate quarterly procedure).

## Setup

No external setup beyond:

```bash
# Accounting platform access (already shipped):
# - xero-mcp + xero default skill
# - Intuit MCP via cli-anything

# Banking access for cutoff reconciliation:
export MERCURY_API_KEY="..."   # or Plaid for multi-bank
```

## The 5-10 business day close timeline

```
Day 0 (cutoff)        ────────── cutoff date (e.g., 2026-06-30)
Day 1-2               Pull all data; tag late items
Day 3-5               Reconcile + accrue + post journals
Day 5-7               Trial balance + subledger tie-outs
Day 7-9              Generate P&L / BS / CF; variance vs budget
Day 10                Close period; close memo; distribute
```

Faster close target: 5 days (top-decile); 10 days = typical SaaS startup; >15 days = process issue.

## Common recipes

### Recipe 1 — Day 1: Pull all source data

```python
# Bank statements
bank_txns = mercury.transactions(start=cutoff_minus_30, end=cutoff)

# Credit card / corp card
ramp_txns = ramp.transactions(from_date=cutoff_minus_30, to_date=cutoff)

# Payroll register
gusto_register = gusto.payroll_runs(start=cutoff_minus_30, end=cutoff)

# AR / AP aging
ar = xero.reports.aged_receivables_by_contact(date=cutoff)
ap = xero.reports.aged_payables_by_contact(date=cutoff)

# Stripe revenue
stripe_rev = stripe.revenue_summary(start=cutoff_minus_30, end=cutoff)
```

### Recipe 2 — Day 2: Tag late items (cutoff discipline)

```python
# Find transactions post-cutoff that should be IN the closing period
# (received late but service rendered before cutoff)
late_invoices = [
  inv for inv in xero.invoices.list()
  if inv.invoice_date > cutoff
     and any(line.service_date <= cutoff for line in inv.line_items)
]
# Reclassify these to the closing period via accrual
```

### Recipe 3 — Day 3-5: Bank reconciliation

```python
# Match bank-feed lines to ledger
unreconciled = xero.bank_transactions.list(
  where='IsReconciled==false AND Date<=DateTime(2026,06,30)'
)
for txn in unreconciled:
    # Auto-match by amount + date window
    candidates = xero.invoices.list(
      where=f"AmountDue=={txn.amount} AND Date>=DateTime(2026,06,{txn.day-3})"
    )
    if len(candidates) == 1:
        xero.payments.create(
          invoice={"invoiceID": candidates[0].id},
          account={"accountID": txn.bank_account_id},
          amount=txn.amount,
          date=txn.date
        )
    # Else: flag for human review
```

### Recipe 4 — Day 3-5: Standard accrual entries

```python
# Deferred revenue release (from Stripe Rev Rec or manual waterfall)
xero.manual_journals.create({
  "narration": "2026-06-30 | ACCRUAL | Deferred revenue release — June",
  "date": "2026-06-30", "status": "POSTED",
  "journalLines": [
    {"lineAmount": -45_000, "accountCode": "210", "description": "Dr Deferred Revenue"},
    {"lineAmount":  45_000, "accountCode": "400", "description": "Cr SaaS Revenue"}
  ]
})

# Accrued payroll (period straddles cutoff)
xero.manual_journals.create({
  "narration": "2026-06-30 | ACCRUAL | Accrued payroll — June 16-30 period",
  "date": "2026-06-30", "status": "POSTED",
  "journalLines": [
    {"lineAmount":  62_000, "accountCode": "6000", "description": "Dr Salaries Expense"},
    {"lineAmount": -62_000, "accountCode": "2110", "description": "Cr Accrued Payroll"}
  ]
})

# Prepaid expense amortization (annual SaaS, etc.)
xero.manual_journals.create({
  "narration": "2026-06-30 | ACCRUAL | June portion — annual Notion subscription",
  "date": "2026-06-30", "status": "POSTED",
  "journalLines": [
    {"lineAmount":  500, "accountCode": "6300", "description": "Dr SaaS Expense"},
    {"lineAmount": -500, "accountCode": "1200", "description": "Cr Prepaid"}
  ]
})

# Accrued expense (June AWS invoice arrives in July)
xero.manual_journals.create({
  "narration": "2026-06-30 | ACCRUAL | June AWS — estimate from billing report",
  "date": "2026-06-30", "status": "POSTED",
  "journalLines": [
    {"lineAmount":  18_500, "accountCode": "5000", "description": "Dr Hosting Expense"},
    {"lineAmount": -18_500, "accountCode": "2100", "description": "Cr Accrued Expense"}
  ]
})

# Depreciation
xero.manual_journals.create({
  "narration": "2026-06-30 | ACCRUAL | June depreciation",
  "date": "2026-06-30", "status": "POSTED",
  "journalLines": [
    {"lineAmount":  3_200, "accountCode": "6500", "description": "Dr Depreciation"},
    {"lineAmount": -3_200, "accountCode": "1510", "description": "Cr Accum Depreciation"}
  ]
})

# Bad debt allowance (if AR >90d unpaid)
ar_90d = ar.where_aging_bucket > 90
bad_debt = ar_90d.total * 0.30  # 30% allowance on 90+
xero.manual_journals.create({
  "narration": "2026-06-30 | ACCRUAL | Bad debt allowance estimate",
  "date": "2026-06-30", "status": "POSTED",
  "journalLines": [
    {"lineAmount":  bad_debt, "accountCode": "6900", "description": "Dr Bad Debt Expense"},
    {"lineAmount": -bad_debt, "accountCode": "1110", "description": "Cr Allowance Doubtful Accts"}
  ]
})
```

### Recipe 5 — Day 5-7: Trial balance + subledger tie-out

```python
tb = xero.reports.trial_balance(date="2026-06-30")
# Total Debits must equal Total Credits

# Tie out each BS account
ar_subledger_total = ar.total
ar_bs_balance = tb.get("1100")  # AR account
assert abs(ar_subledger_total - ar_bs_balance) < 1.00, f"AR mismatch: {ar_subledger_total} vs {ar_bs_balance}"

ap_subledger_total = ap.total
ap_bs_balance = tb.get("2000")
assert abs(ap_subledger_total - ap_bs_balance) < 1.00

# Deferred revenue per BS vs waterfall sum
def_rev_waterfall = stripe.deferred_revenue_balance(as_of="2026-06-30")
def_rev_bs = tb.get("2300") + tb.get("2310")
assert abs(def_rev_waterfall - def_rev_bs) < 50  # $50 materiality

# Cash per BS vs bank statements
bank_total = sum(mercury.account_balances(as_of="2026-06-30").values())
cash_bs = tb.get("1000") + tb.get("1010")
assert abs(bank_total - cash_bs) < 1.00

# Equity reconciliation
equity_rollforward_total = carta.cap_table_equity(as_of="2026-06-30") + tb.get("retained_earnings_opening") + period_net_income
equity_bs = tb.get("3000") + tb.get("3010") + tb.get("3500")
assert abs(equity_rollforward_total - equity_bs) < 100
```

### Recipe 6 — Day 7-9: Generate financial statements

```python
pnl = xero.reports.profit_and_loss(fromDate="2026-06-01", toDate="2026-06-30")
bs = xero.reports.balance_sheet(date="2026-06-30")
cf = xero.reports.cash_summary(fromDate="2026-06-01", toDate="2026-06-30")

# Verify A = L + E
assert abs(bs.total_assets - (bs.total_liabilities + bs.total_equity)) < 1.00

# Verify CF reconciliation: closing cash - opening cash = net cash flow
opening_cash = bs.cash_opening
closing_cash = bs.cash_closing
net_cash = closing_cash - opening_cash
assert abs(net_cash - cf.total) < 1.00
```

### Recipe 7 — Day 7-9: Variance vs budget

```python
budget = xero.reports.budget_summary(fromDate="2026-06-01", toDate="2026-06-30")
variance = pd.merge(pnl_df, budget_df, on="account")
variance["pct"] = (variance.actual - variance.budget) / variance.budget
flagged = variance[variance.pct.abs() > 0.10]  # >10% unfavorable threshold

# One-line narrative for each flagged item
narratives = {
  "Hosting": "Higher AWS spend due to traffic spike + new ML cluster",
  "Travel":  "Lower than budgeted — Q2 conferences moved to Q3",
  # ...
}
```

### Recipe 8 — Day 10: Close memo + package

Standard close memo template (see `role.md` "Brief / Output templates"):

```markdown
COMPANY: [Name]
PERIOD CLOSED: June 2026
CLOSE DATE: 2026-07-08
PREPARED BY: Controller
REVIEWED BY: Founder / CFO

TL;DR
- Net loss $(187K); cash $1.42M; runway 14.2 months; main variance: hosting +35% vs budget

P&L SUMMARY
- Revenue $324K (+12% MoM, +5% vs budget)
- COGS $76K (gross margin 76.5%, target 78%)
- OpEx $435K (+8% vs budget)
- EBITDA $(187K)

BALANCE SHEET HIGHLIGHTS
- Cash $1.42M (-$210K MoM)
- AR $87K (DSO 23 days)
- AP $42K
- Deferred Revenue $612K

CASH FLOW SUMMARY
- Operating CF $(187K)
- Investing CF $(8K) — laptops
- Financing CF $0
- Net Change $(195K)

VARIANCE NARRATIVE
- Hosting +35% vs budget — new ML inference cluster; lifetime expected
- Travel −60% vs budget — Q2 conferences shifted Q3
- Headcount on plan (28 vs 28 budget)

OPEN ITEMS / RISKS
- $34K AR >60d at risk; dunning Day 14 today
- AWS RI commit decision needed by 2026-07-15

ATTACHMENTS
- 01_TB.xlsx, 02_PL.pdf, 03_BS.pdf, 04_CF.pdf, 05_AR_aging.xlsx, 06_AP_aging.xlsx, 07_close_journals.xlsx
```

### Recipe 9 — Auto-generated journal naming

Standard format: `YYYY-MM-DD | [CATEGORY] | Description | [REF: source]`

Categories: `ACCRUAL`, `ADJUSTMENT`, `RECLASS`, `DEPRECIATION`, `AMORTIZATION`, `EQUITY`, `TAX`, `INTERCO`

Examples:
- `2026-06-30 | ACCRUAL | June hosting estimate from AWS usage | REF: AWS Billing 2026-06`
- `2026-06-30 | DEPRECIATION | June PP&E monthly | REF: FA Register row 23-31`
- `2026-06-30 | RECLASS | Move Q2 prepaid IT services to expense | REF: Vendor invoice INV-9821`

### Recipe 10 — AI-assisted close (Numeric / Truewind / Pilot)

```bash
# These platforms ingest from Xero/QBO + bank/card APIs, generate proposed journals,
# and surface anomalies. Workflow:
# 1. Connect Numeric to Xero + Mercury + Ramp
# 2. Run "auto-close" → proposed journals + flagged anomalies
# 3. Controller reviews, approves, posts via Numeric → Xero
# 4. Generate close memo from Numeric → review → distribute
# Cost: $500-$3K/mo depending on volume + entity count
```

Use AI close to accelerate Recipes 3-5; never blindly approve auto-journals.

## Examples

### Example 1: First-time close at new SaaS startup

**Goal:** First monthly close for company that just incorporated 2 months ago.

**Steps:**

1. Day 1: Set CoA per `xero-quickbooks-bookkeeping` Recipe 8.
2. Day 1-2: Pull all bank txns since founding (Recipe 1).
3. Day 3-4: Reconcile bank-feed → ledger (Recipe 3).
4. Day 4-5: Book founding equity, opening cash, any prepaid SaaS (Recipe 4).
5. Day 5-6: Run TB (Recipe 5); tie out — discover deferred revenue not yet set up.
6. Day 7: Set up deferred revenue schedule for $24K annual contract.
7. Day 8: Re-run TB; verify A = L + E.
8. Day 8-9: Generate first P&L (Recipe 6); compute simple metrics (no variance yet — no budget).
9. Day 10: First close memo; distribute. Onboard founder to monthly cadence.

**Result:** Company has clean books from founding; ready for fundraise diligence.

### Example 2: Compressed 5-day close at Series B SaaS

**Goal:** Hit 5-day close target with mature processes.

**Steps:**

1. Day 1 (cutoff = day 0): all bank/card/payroll feeds auto-imported overnight; AR/AP aging pulled at 9am.
2. Day 2: Auto-reconciler runs (Numeric or pandas-based Recipe 3). 90%+ matched; 10% surfaced for review. Resolve by EOD.
3. Day 3: Accrual templates from prior close auto-prepopulate (Recipe 4); controller reviews + adjusts amounts.
4. Day 4: TB + tie-outs (Recipe 5); fix any breaks.
5. Day 5: Generate statements (Recipe 6); compute variance (Recipe 7); produce close memo (Recipe 8); distribute by EOD.

**Result:** Books closed 5 business days post cutoff; metrics ready for board meeting.

## Edge cases / gotchas

- **Cutoff discipline:** the single biggest source of close errors. Invoices dated July 3 for June services must accrue back. Train CSAs / sales / customer success on this.
- **Period locking:** once a period is closed, post any subsequent adjustments in the open period with clear narration tying back. Don't unlock unless materiality demands.
- **Materiality threshold:** for small startups, $50-$500 per item is typical materiality; for Series B+, $5K. Document and apply consistently.
- **Audit trail:** never delete a posted journal. Reverse + repost. Auditors look for deletes.
- **Auto-reconciler false positives:** 5-10% of auto-matches are wrong (same amount, different invoice). Spot-check large dollar matches.
- **Year-end gotchas:** depreciation full-year true-up; bad-debt review with allowance refresh; equity rollforward across full year; tax provision needed.
- **Multi-entity:** consolidate AFTER intercompany eliminations. Don't sum raw entity P&Ls.
- **FX revaluation:** monthly for foreign-currency-denominated AR/AP; quarterly for FX-denominated investments. Use period-end spot rate (ASC 830).
- **Reversing entries:** prior-month accruals should auto-reverse first of next month. Document policy; enforce.
- **First-time close errors:** missing CoA accounts (build the standard SaaS CoA first); deferred revenue not set up; founder/employee comp not booked.

## Sources

- Pilot AI Accountant: https://pilot.com/platform/ai-accountant
- Numeric.io: https://www.numeric.io/
- Truewind: https://www.truewind.ai/
- AI accounting tools comparison: https://www.articsledge.com/post/ai-accounting-tools
- ASC 842 (lease accounting accrual): https://www.fasb.org/jsp/FASB/Page/SectionPage&cid=1176156316498
- Materiality (PCAOB AS 2105): https://pcaobus.org/oversight/standards/auditing-standards/details/AS2105

## Related skills

- `xero-quickbooks-bookkeeping` — provides the source data + report pulls
- `stripe-revenue-recognition-asc606` — deferred revenue waterfall feeds Recipe 4
- `ar-ap-aging-collections` — aging reports feed Recipes 1 + 5
- `runway-burn-analysis` — uses Recipe 6 cash output
- `audit-prep-big4-checklist` — close discipline is the audit's foundation
