<!--
Source: https://www.workiva.com/solutions/internal-audit-management
Source: https://www.compliance-seminars.com/post/audit-planning-checklist-for-auditors-in-2026
Source: https://www.zi.consulting/zeroed-insights/when-to-start-audit-prep
Reference role.md: "Audit prep playbook"
-->

# Audit prep — Big 4 / regional financial audit

90-day pre-fieldwork preparation: PBC list management, supporting schedules library, T-90 / T-60 / T-30 timeline. Designed for first-time SaaS audit (Big 4) and recurring annual.

## When to use

- First-time financial audit announced (typically required at Series B+, customer SOC2, IPO track).
- Annual audit prep (recurring).
- Audit findings remediation between cycles.
- Pre-due-diligence on M&A or strategic transaction.
- Trigger phrases: "audit prep", "PBC list", "auditor questions", "fieldwork", "SOC2 financial", "quality of earnings".

NOT for: SOC2 security audit (separate workflow with engineering); tax audit (separate workflow with CPA).

## Setup

```bash
# Source data — already shipped:
# - xero-mcp / Intuit QBO MCP for trial balance + GL detail
# - stripe-mcp / stripe-revenue-recognition-asc606 for revenue schedules
# - carta-pulley-cap-table for cap-table + equity rollforward
# - mercury-modern-treasury-banking for bank statements

# Audit collaboration platform options:
# - Workiva (most common Big 4): https://www.workiva.com/solutions/internal-audit-management
# - AuditBoard
# - Auditfile
# - Or shared Google Drive / Dropbox for smaller audits
```

## The audit timeline (working backward from fieldwork)

```
T-90 (3 months pre-fieldwork)
- Entity understanding doc with auditor
- Risk assessment
- Materiality threshold set (typically 5% of pre-tax income, or 0.5-1% of revenue)
- Scoping decisions (in-scope entities, locations, processes)

T-60
- Internal control walkthroughs
- Identify in-scope material accounts
- Trial balance generated (preliminary)
- Auditor sends PBC list

T-30
- PBC list finalized and assigned to owners
- Supporting schedules being built (in parallel with close)
- Initial submission to auditor
- Process narrative documents

FIELDWORK (2-6 weeks typically)
- Respond to auditor sample selections
- Provide GL detail per sample
- Document explanations + reconciliations
- Resolve proposed adjustments
- Management representation letter

POST-FIELDWORK
- Audit committee review
- Management letter response
- Final reports (audit opinion, financial statements, internal controls letter)
```

## Standard PBC list structure

```
01_TB
  /01_Trial_Balance_YearEnd.xlsx
  /02_Chart_of_Accounts.xlsx
  /03_Adjusting_Journal_Entries.xlsx
  /04_TB_Prior_Year.xlsx

02_AR
  /01_AR_Aging_YearEnd.xlsx
  /02_AR_Rollforward.xlsx
  /03_Top_Customer_Detail.xlsx       # 10 largest by AR balance
  /04_Bad_Debt_Allowance_Computation.xlsx
  /05_AR_Subsequent_Receipts.xlsx    # cash received post year-end

03_AP
  /01_AP_Aging_YearEnd.xlsx
  /02_AP_Rollforward.xlsx
  /03_Top_Vendor_Detail.xlsx         # 10 largest
  /04_AP_Subsequent_Payments.xlsx
  /05_Accrued_Liabilities_Detail.xlsx

04_PPE
  /01_Fixed_Asset_Register.xlsx
  /02_PPE_Rollforward.xlsx
  /03_Depreciation_Schedule.xlsx
  /04_Additions_Detail.xlsx
  /05_Disposals_Detail.xlsx
  /06_Impairment_Testing.xlsx        # if applicable

05_Revenue_and_DefRev
  /01_Revenue_by_Customer.xlsx
  /02_Revenue_by_Product.xlsx
  /03_Deferred_Revenue_Waterfall.xlsx  # from stripe-revenue-recognition-asc606
  /04_ASC_606_Contract_Review/         # sample of large contracts
  /05_Contract_Cost_Capitalization.xlsx # ASC 340-40
  /06_Revenue_Rollforward.xlsx

06_Equity_and_StockComp
  /01_Cap_Table_YearEnd.pdf            # from Carta
  /02_Option_Register.xlsx              # all grants outstanding
  /03_ASC_718_Expense_Waterfall.xlsx
  /04_Stock_Comp_Expense_Detail.xlsx
  /05_Equity_Rollforward.xlsx
  /06_Board_Meeting_Minutes/             # full year
  /07_SAFE_Convertible_Note_Schedule.xlsx

07_Payroll
  /01_Payroll_Register_Annual.xlsx
  /02_Payroll_Tax_Filings/               # 941s, W-3, state filings
  /03_W2_W3_Reconciliation.xlsx
  /04_Bonus_Accrual_Detail.xlsx
  /05_Equity_Comp_Roll_From_Payroll.xlsx

08_Debt
  /01_Loan_Agreements/                   # all current debt
  /02_Amortization_Schedule.xlsx
  /03_Interest_Expense_Detail.xlsx
  /04_Covenant_Compliance_Worksheet.xlsx
  /05_Debt_Rollforward.xlsx

09_Leases
  /01_Lease_Agreements/
  /02_ASC_842_Right_of_Use_Asset.xlsx
  /03_ASC_842_Lease_Liability.xlsx
  /04_Lease_Expense_Detail.xlsx
  /05_Future_Lease_Payments.xlsx

10_Tax
  /01_Tax_Provision_Detail.xlsx
  /02_Deferred_Tax_Computation.xlsx
  /03_State_Nexus_Map.xlsx               # from anrok-stripe-tax-sales-tax-compliance
  /04_R&D_Credit_Documentation/
  /05_Federal_Tax_Returns/
  /06_State_Tax_Returns/

99_Other
  /01_Bank_Statements_Full_Year/
  /02_Bank_Reconciliations/
  /03_Board_Minutes/                     # already in 06 but cross-link
  /04_Material_Contracts/                 # customer + vendor over materiality
  /05_Confirmation_Letters/               # bank, attorneys, customers, debtors
  /06_Insurance_Policies/
  /07_Subsequent_Events_Memo.docx
```

## Common recipes

### Recipe 1 — Export year-end trial balance

```bash
# Xero
curl -G "https://api.xero.com/api.xro/2.0/Reports/TrialBalance" \
  -H "Authorization: Bearer $XERO_TOKEN" \
  -H "Xero-tenant-id: $TENANT_ID" \
  -d "date=2026-12-31"
# Export to xlsx with full account detail + debits/credits/balance

# QBO
curl -H "Authorization: Bearer $QBO_TOKEN" \
  "https://quickbooks.api.intuit.com/v3/company/$REALM/reports/TrialBalance?date=2026-12-31"
```

### Recipe 2 — Build AR roll-forward

```python
# AR_RF = Beginning AR + Sales − Cash Receipts − Write-offs ± Adjustments = Ending AR
import pandas as pd

ar_beg = xero.reports.aged_receivables_by_contact(date="2025-12-31").total
sales = xero.reports.profit_and_loss(fromDate="2026-01-01", toDate="2026-12-31").revenue
receipts = bank.customer_receipts(start="2026-01-01", end="2026-12-31")
writeoffs = xero.journals.list(where='Narration like "%write%off%" AND Date in 2026').total
adjustments = xero.adjustments(year=2026).total
ar_end_computed = ar_beg + sales - receipts - writeoffs + adjustments
ar_end_actual = xero.reports.aged_receivables_by_contact(date="2026-12-31").total

variance = ar_end_computed - ar_end_actual
print(f"AR Rollforward: Beg ${ar_beg:,.0f} + Sales ${sales:,.0f} - Receipts ${receipts:,.0f} "
      f"- Writeoffs ${writeoffs:,.0f} + Adj ${adjustments:,.0f} = ${ar_end_computed:,.0f} | "
      f"Actual ${ar_end_actual:,.0f} | Variance ${variance:,.0f}")
# Variance must be < materiality
```

### Recipe 3 — ASC 606 contract sample for revenue testing

```python
# Auditor will sample 25-40 contracts; pre-build the review pack for top 20 + sample of remaining
contracts = stripe.invoices.list(
  status="paid", created_after="2026-01-01", created_before="2026-12-31"
)
top_20 = sorted(contracts, key=lambda c: c.amount, reverse=True)[:20]

for contract in top_20:
    # Build per-contract memo
    memo = f"""
CONTRACT REVIEW MEMO

Customer: {contract.customer.name}
Invoice: {contract.id}
Amount: ${contract.amount/100:,.0f}
Service period: {contract.metadata.service_start} - {contract.metadata.service_end}

ASC 606 Five-Step Analysis:
1. Contract: signed agreement attached; commercial substance + collection probable
2. Performance obligations: {contract.metadata.po_description}
3. Transaction price: ${contract.amount/100:,.0f} fixed; no variable consideration
4. Allocation: 100% to {contract.metadata.po_count} obligations
5. Recognition: {contract.metadata.recognition_method}

Revenue recognized in 2026: ${recognized_2026}
Deferred revenue at 12/31/2026: ${deferred_at_yearend}

Supporting documents:
- Signed contract: link
- Customer email confirming acceptance: link
- Performance evidence (delivery / service date): link
"""
    # Save memo + supporting docs in 05_Revenue_and_DefRev/04_ASC_606_Contract_Review/
```

### Recipe 4 — ASC 718 expense waterfall

```python
# Pull from carta-pulley-cap-table Recipe 5
# Bring forward all grants + monthly expense per grant
import pandas as pd
asc718 = pd.read_excel("data/asc_718_waterfall.xlsx", index_col=0)
total_expense_2026 = asc718.loc[:, "2026-01":"2026-12"].sum().sum()

# Tie out to P&L stock-based comp expense account
pl_sbc = xero.reports.profit_and_loss(...).get_account("6800").balance
print(f"ASC 718 waterfall: ${total_expense_2026:,.0f} | GL: ${pl_sbc:,.0f} | Diff: ${total_expense_2026 - pl_sbc:,.0f}")
```

### Recipe 5 — Equity rollforward

```python
def equity_rollforward(beg_date, end_date):
    """Beginning Equity + Stock Issuances + Net Income − Distributions + SBC = Ending Equity"""
    beg_equity = xero.reports.balance_sheet(date=beg_date).equity_total
    period_net_income = xero.reports.profit_and_loss(fromDate=beg_date, toDate=end_date).net_income
    period_sbc = asc718_total_expense(year=2026)  # from Recipe 4
    period_issuances = carta.equity_issuances(start=beg_date, end=end_date)
    period_distributions = 0  # rare for startups

    computed_end = beg_equity + period_issuances + period_net_income - period_distributions + period_sbc
    actual_end = xero.reports.balance_sheet(date=end_date).equity_total
    print(f"Equity rollforward: Beg + Issuances + NI + SBC = ${computed_end:,.0f} | Actual ${actual_end:,.0f}")
    assert abs(computed_end - actual_end) < materiality
```

### Recipe 6 — Bank reconciliations (per account, per month)

```python
# Auditors look at bank recs for outliers
for month in months_in_year(2026):
    for account in bank_accounts:
        rec = {
          "bank_balance_per_statement": bank.statement_balance(account, month_end),
          "deposits_in_transit": deposits_uncleared_at_month_end(account, month_end),
          "outstanding_checks": outstanding_at_month_end(account, month_end),
          "adjusted_bank_balance": ...,
          "gl_balance": xero.account_balance(account.gl_code, month_end),
          "variance": "to_be_computed"
        }
        rec["variance"] = rec["adjusted_bank_balance"] - rec["gl_balance"]
        save_to_pbc(f"09_Other/02_Bank_Reconciliations/{account.name}_{month_end}.xlsx", rec)
```

### Recipe 7 — Subsequent events memo

After year-end (12/31), any events through audit-completion date that affect financial statements:

```markdown
SUBSEQUENT EVENTS MEMO

Period covered: 2027-01-01 through 2027-03-15 (date of management representation letter)

EVENTS REQUIRING ADJUSTMENT (Type I — conditions existing at year-end):
- [Customer A] payment received 2027-02-15; AR was at 12/31; reduces AR by $X
- [Customer B] bankruptcy filed 2027-01-20; AR balance at 12/31 should be reserved fully

EVENTS REQUIRING DISCLOSURE (Type II — conditions arising after year-end):
- Series A close on 2027-02-28 ($10M raised); cap table will change post-audit period
- Office lease signed 2027-03-01 for new HQ
- Major customer contract signed 2027-01-15 ($500K ACV)

NON-EVENTS:
- No litigation initiated
- No regulatory matters
- No data breaches
- No covenant violations on debt
```

### Recipe 8 — Confirmation letter management

Auditors send confirmations directly to third parties:

```python
# Pre-build the list for auditor
confirmations = {
  "banks":     mercury_account_list() + plaid_linked_accounts(),
  "customers": top_20_ar_balances(),
  "vendors":   top_10_ap_balances(),
  "attorneys": ["Cooley LLP — corporate","Wilson Sonsini — IP"],
  "debt":      loan_holder_list(),
  "leases":    lessor_list(),
  "key_persons": ["founder","cfo","gc"],   # representation letter signers
}
# Provide to auditor as a structured xlsx
```

### Recipe 9 — Walkthrough narrative (control documentation)

For each material process, document:

```markdown
PROCESS NARRATIVE: Revenue Recognition

OBJECTIVE: Ensure revenue is recognized in accordance with ASC 606 at appropriate amounts and periods.

PROCESS OWNER: Controller

KEY CONTROLS:
1. New Contract Review (preventive)
   - Trigger: Any new contract or amendment >$10K
   - Performer: Controller
   - Frequency: Per contract
   - Evidence: Signed contract + ASC 606 analysis memo
   - Tested by: auditor sample

2. Monthly Revenue Reconciliation (detective)
   - Trigger: Month-end close
   - Performer: Controller
   - Frequency: Monthly
   - Evidence: Stripe revenue summary vs Xero GL revenue accounts
   - Threshold: variance >$500 investigated and documented

3. Annual ASC 606 Compliance Review (detective)
   - Trigger: Year-end
   - Performer: Controller + CFO
   - Frequency: Annual
   - Evidence: Compliance memo signed by both

KEY SYSTEMS:
- Stripe (source of subscription billing data)
- Stripe Revenue Recognition (ASC 606 schedules)
- Xero (general ledger)

INPUTS / OUTPUTS:
- Inputs: Customer contracts, invoice data, payment data
- Outputs: Recognized revenue P&L, Deferred revenue BS, revenue schedules

DATA FLOW: Contract signing → Stripe Billing → Stripe Rev Rec → Xero GL journal entries
```

### Recipe 10 — Management Representation Letter checklist

The MRL is signed by founder + controller/CFO; covers all material assertions. Standard items:

```markdown
MRL ITEMS (sample — auditor provides specific letter):

[ ] Financial statements fairly present in accordance with US GAAP
[ ] All transactions recorded
[ ] No unrecorded liabilities (specifically: guarantees, contingencies, off-BS arrangements)
[ ] Subsequent events disclosed (see Recipe 7)
[ ] Related-party transactions disclosed
[ ] Compliance with laws + regulations (no known violations)
[ ] No fraud (management, employees, vendors)
[ ] No knowledge of pending litigation not disclosed
[ ] Tax positions sustainable on examination
[ ] Customer concentrations disclosed
[ ] Material risks disclosed
[ ] Going concern assumption is appropriate (or alternative basis disclosed)
[ ] Internal controls assessed and any material weaknesses disclosed
```

## Examples

### Example 1: First Big 4 audit at Series B SaaS

**Goal:** Clean opinion on FY26 financial statements; auditor: Deloitte.

**Steps:**

**T-90:**
1. Engagement letter signed; PBC list received from Deloitte (typically 100-200 line items).
2. Set materiality with auditor ($X based on revenue or pre-tax income).
3. Schedule fieldwork dates.

**T-60:**
4. Build PBC binder structure (sections 01-99).
5. Recipe 1: trial balance + COA exported.
6. Recipe 2-5: build core rollforwards.

**T-30:**
7. Initial PBC submission to Deloitte via Workiva.
8. Recipe 3: ASC 606 contract sample memos completed for top 20 contracts.
9. Recipe 9: process narratives for revenue, AR, AP, payroll, equity.

**Fieldwork (2-4 weeks):**
10. Recipe 8: confirmation list provided.
11. Daily auditor questions answered with 24-hour turnaround target.
12. Recipe 7: subsequent events log maintained.
13. Audit adjustments tracked; book corrections.

**Post-fieldwork:**
14. Audit committee review.
15. Recipe 10: MRL signed.
16. Final audit report received; opinion clean.

**Result:** First clean audit; relationship established for recurring; lessons learned for FY27.

### Example 2: Audit adjustment proposed mid-fieldwork

**Goal:** Auditor proposes adjustment on revenue recognition.

**Steps:**

1. Auditor finds: $80K of revenue recognized in 2026 should be deferred to 2027 (service started 12/15, not full period in 2026).
2. Pull contract + service-delivery evidence.
3. If auditor is right: book adjusting entry — Dr Revenue $80K / Cr Deferred Revenue $80K.
4. Document rationale in adjusting journal entries file (01_TB/03).
5. Update ASC 606 schedule.
6. Update revenue rollforward.
7. Net income impact: $(80K) flows through.

**Result:** Adjustment booked; financial statements re-printed.

## Edge cases / gotchas

- **Materiality setting:** the single biggest leverage point. Set it with auditor in advance; cannot be moved mid-audit. Typically 5% of pre-tax income for established companies; 0.5-1% of revenue for early-stage.
- **PBC list size:** first audit often 200+ items; recurring audit often 50-100. Don't underestimate.
- **Auditor independence:** they cannot do anything that could be seen as management. They can't bookkeep for you. Watch the line.
- **Section 302/404 (SOX):** if private and not SOX-applicable, you have more flexibility on controls documentation. If headed to IPO, build to SOX standard now.
- **Going concern:** if runway < 12 months at year-end + projected, auditor likely surfaces going concern. Mitigate via runway extension + going-concern memo with mitigation plan.
- **Related party transactions:** founder loans, family-member vendors, etc. Disclose all; auditor will find them.
- **Stock-based comp:** ASC 718 is a common audit adjustment area. Get ASC 718 right in close (Recipe 4); auditors test calculation.
- **Cap-table tie out:** Carta cap table must tie to legal records (signed certificates); discrepancies are audit findings.
- **Sample sizes:** auditors use statistical sampling; once you know typical sample sizes (often 25-40 per assertion), you can pre-package those PBC items.
- **Subsequent events cutoff:** ends with management representation letter signing (Recipe 10). Document everything between year-end and that date (Recipe 7).
- **Confirmations:** banks confirm cash; attorneys confirm litigation (none = letter from each firm). 100% response not required but >80% expected.
- **Annual audit lessons learned:** keep an "audit feedback" doc; year 2 should be smoother. Build templates for the recurring PBC items.

## Sources

- Workiva audit management: https://www.workiva.com/solutions/internal-audit-management
- Audit planning 2026: https://www.compliance-seminars.com/post/audit-planning-checklist-for-auditors-in-2026
- When to start audit prep: https://www.zi.consulting/zeroed-insights/when-to-start-audit-prep
- FASB Codification: https://asc.fasb.org/
- AICPA Audit Standards: https://www.aicpa-cima.com/topic/audit-assurance
- PCAOB: https://pcaobus.org/

## Related skills

- `monthly-close-procedure` — clean closes feed clean audit
- `xero-quickbooks-bookkeeping` — GL detail export for Recipe 1
- `stripe-revenue-recognition-asc606` — Recipe 3 ASC 606 contracts
- `carta-pulley-cap-table` — Recipe 4 ASC 718 + Recipe 5 equity rollforward
- `equity-grant-83b-isos-rsus` — equity comp documentation
