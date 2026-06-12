<!--
Source: https://www.intuit.com/enterprise/blog/financials/13-week-cash-flow-forecast/
Source: https://graphitefinancial.com/blog/why-you-need-13-week-cash-flow-forecast/
Source: https://cashflowfrog.com/glossary/13-weeks-cash-flow/
Reference role.md: "13-week cash flow playbook"
-->

# Cash flow forecasting — rolling 13-week

The single most important tool for a startup CFO: weekly-granularity cash position projected 13 weeks (one fiscal quarter) forward. Updated every Monday. Surfaces "stop-the-line" weeks before they happen.

## When to use

- Every Monday morning at small/early-stage companies.
- Pre-fundraise: shows precise timing of when raise must close.
- Pre-major-spend: validates impact of a $X commitment.
- AP timing decisions: which bills to pay this week vs delay.
- Cash sweep decisions: how much can move to treasury safely.
- Trigger phrases: "13-week", "weekly cash", "stop-the-line", "Monday cash update", "rolling forecast".

NOT for: monthly P&L forecasting (use `causal-mosaic-financial-modeling`); runway months at a glance (use `runway-burn-analysis`); long-range planning (use 5-year model in Causal).

## Setup

Reuses bundled + default skills:

```bash
# Banking — pull current balance + last-week transactions
# - mercury-modern-treasury-banking (this agent)
# - plaid for external accounts

# AR/AP aging — projected inflows + outflows
# - xero-quickbooks-bookkeeping (this agent)

# Output — xlsx for the model + google-sheet for shared editing
```

## Structure (the canonical layout)

Three sections, 13 weekly columns, weekly cadence:

```
                              W1   W2   W3   ...   W13   TOTAL
INFLOWS
  Customer collections        Xkk  Xkk  Xkk        Xkk    Xkk
  Refunds in                  0    0    0          0      0
  Tax refunds                 0    0    0          0      0
  Financing (raise / debt)    0    0    0          0      0
  Other inflows               0    0    0          0      0
  TOTAL INFLOWS               Xkk  Xkk  Xkk        Xkk    Xkk

OUTFLOWS
  Payroll (semi-mo / bi-wk)   Xkk  0    Xkk        Xkk    Xkk
  Contractor / 1099           Xkk  0    0          0      Xkk
  Rent / lease                Xkk  0    0          Xkk    Xkk
  Vendor / AP                 Xkk  Xkk  Xkk        Xkk    Xkk
  SaaS subscriptions          Xkk  Xkk  Xkk        Xkk    Xkk
  Insurance / benefits        Xkk  0    0          0      Xkk
  Taxes (sales / payroll)     0    Xkk  0          Xkk    Xkk
  Debt service                0    0    Xkk        0      Xkk
  One-time outflows           0    0    0          0      0
  TOTAL OUTFLOWS              Xkk  Xkk  Xkk        Xkk    Xkk

NET CASH                      Xkk  Xkk  Xkk        Xkk    Xkk
Opening cash                  Xkk
Closing cash                  Xkk  Xkk  Xkk        Xkk    Xkk
```

## Common recipes

### Recipe 1 — Initialize template (xlsx)

```python
import openpyxl
from datetime import date, timedelta

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "13W Cash"

# Weekly dates
start_monday = date(2026, 6, 9)  # first Monday of forecast
weeks = [(start_monday + timedelta(weeks=i)).isoformat() for i in range(13)]

# Headers
ws.cell(1, 1, "Line item")
for i, w in enumerate(weeks):
    ws.cell(1, i+2, w)
ws.cell(1, 15, "TOTAL")

# Sections
row = 2
for section, items in [
  ("INFLOWS", ["Customer collections", "Refunds in", "Tax refunds", "Financing", "Other inflows"]),
  ("OUTFLOWS", ["Payroll", "Contractor", "Rent", "Vendor AP", "SaaS subscriptions",
                "Insurance/benefits", "Taxes", "Debt service", "One-time"])
]:
    ws.cell(row, 1, section)
    row += 1
    for it in items:
        ws.cell(row, 1, it)
        # Total formula
        ws.cell(row, 15, f"=SUM(B{row}:N{row})")
        row += 1
    # Section total
    ws.cell(row, 1, f"TOTAL {section}")
    for col in range(2, 16):
        ws.cell(row, col, f"=SUM({chr(64+col)}3:{chr(64+col)}{row-1})")
    row += 2

# Net + opening + closing
ws.cell(row, 1, "NET CASH")
row += 1
ws.cell(row, 1, "Opening cash")
row += 1
ws.cell(row, 1, "Closing cash")

wb.save("13_week_forecast_2026Q3.xlsx")
```

### Recipe 2 — Inflow estimation per customer

```python
# Use historical days-to-pay per customer
import pandas as pd
from datetime import timedelta

# Pull invoice payment history per customer
ar = xero.invoices.list(where='Status=="AUTHORISED" AND AmountDue>0')

# Compute days-to-pay history
payment_history = pd.read_sql("""
  SELECT customer_id, invoice_date, paid_date,
         (paid_date - invoice_date) AS days_to_pay
  FROM payments
""", db)
median_days_to_pay = payment_history.groupby("customer_id")["days_to_pay"].median()

# Project each outstanding invoice
projected_inflows = []
for inv in ar:
    cust_dtp = median_days_to_pay.get(inv.customer_id, 45)  # default 45 days B2B SaaS
    projected_date = inv.invoice_date + timedelta(days=cust_dtp)
    week_offset = (projected_date - start_monday).days // 7
    if 0 <= week_offset < 13:
        projected_inflows.append({
          "customer": inv.customer,
          "amount": inv.amount_due,
          "week": week_offset,
          "projected_date": projected_date
        })
```

### Recipe 3 — Pipeline-stage adjustment

```python
# Include forecasted closes only if commit-stage with >80% probability
# Conservative on ACV

from itertools import groupby

pipeline = crm.opportunities(stage="Commit", expected_close_within_days=90)
for opp in pipeline:
    if opp.probability >= 0.80:
        conservative_acv = opp.acv * 0.85   # 15% haircut for negotiation/scope reduction
        cash_landing = opp.expected_close_date + timedelta(days=45)  # standard B2B
        week_offset = (cash_landing - start_monday).days // 7
        if 0 <= week_offset < 13:
            projected_inflows.append({
              "source": "pipeline",
              "customer": opp.account_name,
              "amount": conservative_acv * opp.probability,  # probability-weighted
              "week": week_offset
            })
```

### Recipe 4 — Outflow timing rules

```python
def outflow_schedule(cutoff_date):
    schedule = []

    # Payroll: semi-monthly = 15th + last day; bi-weekly = every other Friday
    for w in range(13):
        wk_start = start_monday + timedelta(weeks=w)
        wk_end = wk_start + timedelta(days=6)
        # Semi-monthly: hits 15th and last day
        for day in [15, 30, 31]:
            try:
                pay_date = wk_start.replace(day=day)
                if wk_start <= pay_date <= wk_end:
                    schedule.append({"category":"payroll","week":w,"amount":monthly_payroll/2})
            except ValueError:
                pass

    # Rent: 1st of the month
    for w in range(13):
        wk_start = start_monday + timedelta(weeks=w)
        for d in range(7):
            day = wk_start + timedelta(days=d)
            if day.day == 1:
                schedule.append({"category":"rent","week":w,"amount":monthly_rent})

    # SaaS: annual renewals (anniversary date) + monthly (signup-date)
    for sub in subscriptions:
        next_charge = sub.next_billing_date
        week_offset = (next_charge - start_monday).days // 7
        if 0 <= week_offset < 13:
            schedule.append({"category":"saas","week":week_offset,"amount":sub.amount})

    # AP — use invoice date + net terms
    for bill in xero.bills.list(status="AUTHORISED"):
        pay_date = bill.invoice_date + timedelta(days=bill.net_terms)
        week_offset = (pay_date - start_monday).days // 7
        if 0 <= week_offset < 13:
            schedule.append({"category":"vendor","week":week_offset,"amount":bill.amount})

    return schedule
```

### Recipe 5 — Build the forecast (combine inflows + outflows)

```python
import pandas as pd

inflows_by_week = pd.DataFrame(projected_inflows).groupby("week")["amount"].sum()
outflows_by_week = pd.DataFrame(outflow_schedule(today)).groupby(["week","category"])["amount"].sum().unstack(fill_value=0)

opening_cash = total_cash_now()  # from runway skill
weeks = range(13)
closing = []
running = opening_cash
for w in weeks:
    inflow = inflows_by_week.get(w, 0)
    outflow = outflows_by_week.loc[w].sum() if w in outflows_by_week.index else 0
    net = inflow - outflow
    running += net
    closing.append({"week": w, "inflow": inflow, "outflow": outflow, "net": net, "closing": running})

print(pd.DataFrame(closing))
```

### Recipe 6 — Find stop-the-line week

```python
operating_buffer_weeks = 6
weekly_outflow_avg = sum(outflow_schedule(today)["amount"]) / 13
operating_buffer_dollars = weekly_outflow_avg * operating_buffer_weeks

# Walk closing-cash trajectory; find first week below buffer
stop_the_line_week = None
for row in closing_trajectory:
    if row["closing"] < operating_buffer_dollars:
        stop_the_line_week = row["week"]
        break

if stop_the_line_week is not None:
    actual_date = start_monday + timedelta(weeks=stop_the_line_week)
    surface_to_founder(
      f"STOP-THE-LINE: Week {stop_the_line_week} ({actual_date}). "
      f"Closing cash projected ${closing_trajectory[stop_the_line_week]['closing']:,.0f} "
      f"vs operating buffer ${operating_buffer_dollars:,.0f}."
    )
```

### Recipe 7 — Monday morning refresh procedure

```python
def monday_refresh():
    """Run every Monday at 8am."""
    # 1. Pull actual closing cash from Friday EOD
    friday = today - timedelta(days=3)
    actual_close = bank_balance_as_of(friday)

    # 2. Pull last week's actual receipts + disbursements
    last_week_actuals = bank_transactions_between(today - timedelta(days=7), today)

    # 3. Compare to W1 projection (was last Monday's W1)
    variance = actual_close - last_monday_projection["W1 closing"]

    # 4. Rebase: shift all weeks one column left; add new W13 row.
    new_forecast = build_forecast_from(today)  # Recipe 5 with today as new start

    # 5. Compare new W1-W12 to previously W2-W13 (lookback)
    for w in range(12):
        old_proj = last_monday_projection[f"W{w+2} closing"]
        new_proj = new_forecast[f"W{w+1} closing"]
        if abs(new_proj - old_proj) > 50_000:  # >$50K shift
            flag_change(week=w, old=old_proj, new=new_proj)

    return new_forecast
```

### Recipe 8 — Early-pay discount math (2/10 net 30)

```python
# "2/10 net 30" = 2% discount if paid within 10 days; full due day 30
# Annualized return on early payment = 2% / (20-day delay) × 365 days = 36.5%

def early_pay_decision(bill):
    discount = 0.02
    early_window = 10
    full_terms = 30
    if bill.discount_offered:
        annualized = (discount / (full_terms - early_window)) * 365
        opportunity_cost = treasury_apy()  # ~5% APY
        if annualized > opportunity_cost:
            return f"PAY EARLY: ${bill.amount * (1-discount):.0f} (save ${bill.amount * discount:.0f}, annualized {annualized:.0%})"
    return f"PAY ON TERMS: day {full_terms}"
```

### Recipe 9 — AP delay decision

```python
# If cash tight, defer AP to align with inflows
def ap_deferral_recommendation(closing_trajectory, ap_due_this_week, late_fee_pct=0.015):
    if closing_trajectory[0]["closing"] < ap_due_this_week:
        # Cash insufficient — recommend defer
        for w, row in enumerate(closing_trajectory[1:5]):  # check next 4 weeks
            if row["closing"] > ap_due_this_week:
                deferred_late_fee = ap_due_this_week * late_fee_pct * w
                return f"DEFER AP to week {w+1}: late fee ${deferred_late_fee:.0f}"
    return "PAY ON TIME"
```

### Recipe 10 — Cover commentary template

Standard format the founder reads first:

```
AS OF: 2026-06-09 (Monday)
OPENING CASH: $1,420,000
WEEK 13 PROJECTED CLOSING: $682,000
WEEKS UNTIL OPERATING BUFFER ($340K) TRIGGERED: 9 (Aug 11)

KEY ASSUMPTIONS
- Customer collections per historical days-to-pay (median 41 days B2B)
- One commit-stage deal ($72K) lands week 6 at 80% probability
- Q2 payroll tax payment hits week 4 ($28K)
- No new financing inflows

KEY RISKS
- Top 3 customers represent 47% of week-6 collections; one delay = -$110K
- Q3 hosting reserve renewal week 5 ($45K AWS RI)
- Sales tax filing deadline week 8 ($14K Anrok)

REQUESTED DECISIONS
- AWS RI 1-year vs 3-year commit (3-yr saves 30% but $200K upfront)
- Defer to Q3? Or one-time stop-gap from founder?
```

## Examples

### Example 1: First 13-week forecast for new Series A company

**Goal:** Build from scratch with no prior model.

**Steps:**

1. Initialize template (Recipe 1).
2. Pull current cash (Recipe 1 of `runway-burn-analysis`).
3. List all customers + 12-mo invoice history → median days-to-pay (Recipe 2).
4. List CRM commit-stage pipeline (Recipe 3) with 80%+ probability.
5. Build outflow schedule (Recipe 4): payroll cadence, rent, SaaS renewals, AP aging.
6. Combine + compute closing trajectory (Recipe 5).
7. Identify stop-the-line week if any (Recipe 6).
8. Write cover commentary (Recipe 10).
9. Share with founder. Schedule weekly Monday refresh.

**Result:** Tied-out 13-week model; founder knows exact cash trajectory.

### Example 2: Monday refresh after AR delay

**Goal:** Last week's W1 projected $200K collections; actual was $120K.

**Steps:**

1. Run Recipe 7 Monday refresh.
2. Variance: −$80K in week 1.
3. Investigate: 2 large customers paid 5 days late.
4. Update median days-to-pay for those customers (+3 days).
5. Re-project remaining inflows → shifts $40K from W2 → W3 (other customer impact).
6. New W13 closing cash: $642K (vs prior $682K).
7. Run Recipe 6 stop-the-line: still week 9, unchanged.
8. Surface variance + new W13 number in Monday note.

**Result:** Founder sees the AR delay, knows it's manageable.

## Edge cases / gotchas

- **Days-to-pay vs invoice date:** new customers have no history. Use B2B SaaS median: 45-60 days; e-commerce: ≤30 days; enterprise: 60-90 days.
- **Pipeline-stage hygiene:** sales-stage labels vary by company. Map your team's "commit" / "best case" / "verbal" to probabilities consistently (commit = 80%, best case = 50%, verbal = 30%).
- **Round-financing inflow:** include only after term sheet signed; mark probability separately if before close.
- **Holiday weeks:** the week of Thanksgiving / Christmas / July 4 has compressed collection patterns; expect slip into next week.
- **End-of-quarter spike:** B2B customers often pay invoices in last week of their fiscal quarter. Track customer fiscal calendars for top accounts.
- **Multi-currency:** if you bill in EUR/GBP and receive in USD, FX exposes you. Use forward FX rate or assume −2% conversion.
- **One-time items:** tax refund, founder loan repayment, M&A milestone — flag these separately, don't smooth.
- **Forecast vs actual feedback loop:** after each week, log variance per line. Quarterly: are your projections systematically optimistic? Recalibrate.
- **Don't double-count:** projected pipeline collections AND deferred-revenue release don't both happen — deferred is already in cash.
- **Build vs use:** every quarter, validate the forecast was useful. If you never look at it after Monday, the model is wasted effort.

## Sources

- Intuit Enterprise — 13-week cash flow: https://www.intuit.com/enterprise/blog/financials/13-week-cash-flow-forecast/
- Graphite Financial — why 13-week: https://graphitefinancial.com/blog/why-you-need-13-week-cash-flow-forecast/
- Cashflow Frog — 13-week glossary: https://cashflowfrog.com/glossary/13-weeks-cash-flow/
- Early-pay discount math: https://www.investopedia.com/terms/d/discount-method.asp

## Related skills

- `mercury-modern-treasury-banking` — bank balances + transactions
- `xero-quickbooks-bookkeeping` — AR/AP aging feeds
- `ar-ap-aging-collections` — inflow timing per customer (days-to-pay)
- `runway-burn-analysis` — monthly view of same cash trajectory
- `vendor-procurement-saas-spend-audit` — outflow optimization
