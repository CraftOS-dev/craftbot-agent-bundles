<!--
Source: https://developer.xero.com/documentation/api/accounting/reports/#agedreceivablesbycontact
Source: https://docs.stripe.com/billing/subscriptions/smart-retries
Source: https://docs.mercury.com/reference/payments
Reference role.md: "Dunning email templates"
-->

# AR aging + AP aging + collections / dunning

Receivables collection (dunning cadence, days 0/7/14/30) and payables management (vendor pay runs, early-pay discount math). Standard cadence + templates that recover 80%+ of overdue AR without escalation.

## When to use

- Weekly AR review: who's late, who needs a chase.
- Monthly close: aging reports for tie-out to BS.
- AP pay run scheduling.
- Collections escalation (Day 30+ service hold).
- Stripe Smart Retries for failed card payments.
- Trigger phrases: "AR aging", "chase invoices", "dunning", "pay vendors", "AP", "service hold".

NOT for: legal collections (defer to `legal-counsel`); cap-table receivables (use `carta-pulley-cap-table`).

## Setup

```bash
# AR / AP data — already shipped via:
# - xero-mcp (catalog) + default xero skill
# - cli-anything + Intuit QBO MCP

# Dunning execution:
# - gmail-mcp (catalog) — primary
# - outlook-mcp (catalog) — alt
# - slack-mcp (catalog) — internal notify

# Card retry (for B2C SaaS):
# - stripe-mcp — Smart Retries configuration
```

## AR aging buckets (standard)

| Bucket | Action | Owner |
|---|---|---|
| Current (0 days) | Day-0 reminder when invoice issued | Auto |
| 1-30 days | Day-7 first chase; Day-14 firm | Controller |
| 31-60 days | Day-30 service-hold notice; manager review | Controller + CSM |
| 61-90 days | Escalation; CSM + Founder | Cross-functional |
| 90+ days | Allowance booking; legal review | Founder + legal |

## Common recipes

### Recipe 1 — Pull AR aging (Xero)

```javascript
xero.reports.aged_receivables_by_contact({
  date: "2026-06-30",
  fromDate: null,
  toDate: null
})
// Returns rows: contact + current + 1-30 + 31-60 + 61-90 + 90+ + total
```

### Recipe 2 — Pull AR aging (QBO)

```bash
curl -H "Authorization: Bearer $QBO_TOKEN" \
  "https://quickbooks.api.intuit.com/v3/company/$QBO_REALM_ID/reports/AgedReceivables?\
report_date=2026-06-30&aging_period=30&num_periods=4"
```

### Recipe 3 — Day 0 reminder (auto on invoice issuance)

```python
# Via gmail-mcp
def send_day_0_reminder(invoice):
    body = f"""
Hi {invoice.contact_first_name},

A quick note that invoice #{invoice.number} for ${invoice.amount:,.2f} is due
{invoice.due_date}. You can pay via the link below:

{invoice.payment_link}

If there are any questions about the invoice, just reply here — happy
to walk through line items.

Thanks,
{sender_name}
"""
    gmail.send(
      to=invoice.contact_email,
      subject=f"Invoice {invoice.number} — ${invoice.amount:,.2f} due {invoice.due_date}",
      body=body
    )
```

### Recipe 4 — Day 7 past due first chase

```python
def send_day_7_chase(invoice):
    body = f"""
Hi {invoice.contact_first_name},

Quick check-in: invoice #{invoice.number} for ${invoice.amount:,.2f} was due
{invoice.due_date} and is now 7 days past due. Could you let me know the
expected payment date so we can update our records?

If you've already sent it, please ignore — bank-feed delay is real.

Thanks,
{sender_name}
"""
    gmail.send(to=invoice.contact_email,
               subject=f"Invoice {invoice.number} past due — ${invoice.amount:,.2f}",
               body=body)
```

### Recipe 5 — Day 14 firm chase

```python
def send_day_14_firm(invoice):
    body = f"""
Hi {invoice.contact_first_name},

Invoice #{invoice.number} for ${invoice.amount:,.2f} is now 14 days past due.
Per our terms, we need to receive payment by {invoice.due_date + timedelta(days=21)}.

If there's a payment issue or dispute, please reply here today and we'll
work through it. If it's been paid, please send us the confirmation.

Thanks,
{sender_name}
"""
    gmail.send(to=invoice.contact_email,
               subject=f"Invoice {invoice.number} — 14 days past due — please pay by {due_plus_21}",
               body=body)
```

### Recipe 6 — Day 30 service hold notice

```python
def send_day_30_service_hold(invoice):
    body = f"""
Hi {invoice.contact_first_name},

Invoice #{invoice.number} for ${invoice.amount:,.2f} is 30 days past due. Per
our terms, we'll pause service on {today + timedelta(days=3)} if payment is not received.

I want to avoid that — please reply today so we can find a resolution.

Thanks,
{sender_name}
"""
    gmail.send(to=invoice.contact_email,
               subject=f"Invoice {invoice.number} — service hold notice",
               body=body)
    # Also: notify CSM via Slack
    slack.send_message(channel="#cs-account-issues",
      text=f"⚠ Day-30 service-hold notice sent to {invoice.contact}. "
           f"Inv #{invoice.number} ${invoice.amount:,.0f}. CSM action: align on resolution.")
```

### Recipe 7 — Dunning orchestrator (weekly loop)

```python
import datetime
def dunning_cycle(today):
    ar = xero.reports.aged_receivables_by_contact(date=today)
    for inv in xero.invoices.list(where='Status=="AUTHORISED" AND AmountDue>0'):
        days_past_due = (today - inv.due_date).days
        if days_past_due < 0:
            continue  # not yet due
        elif days_past_due == 0:
            send_day_0_reminder(inv)
        elif days_past_due == 7:
            send_day_7_chase(inv)
        elif days_past_due == 14:
            send_day_14_firm(inv)
        elif days_past_due == 30:
            send_day_30_service_hold(inv)
        elif days_past_due >= 60:
            escalate_to_founder(inv)
```

### Recipe 8 — Stripe Smart Retries for failed cards

```bash
# Configure retry schedule for failed subscription charges
curl -X POST https://api.stripe.com/v1/billing/billing_settings/retry_rules \
  -u $STRIPE_API_KEY: \
  -d "max_retry_attempts=4" \
  -d "retry_intervals=3,7,10,14"  # days between retries
```

Smart Retries recovers 14-38% of involuntary churn (Stripe benchmark).

### Recipe 9 — Pull AP aging + schedule pay run

```python
ap = xero.reports.aged_payables_by_contact(date=today)
# Sort vendors by criticality + due date
pay_run = []
for vendor in ap.contacts:
    for bill in vendor.bills:
        if bill.days_past_due > 0:
            priority = "URGENT"
        elif bill.discount_offered and bill.days_until_discount_window <= 5:
            priority = "EARLY_PAY_DISCOUNT"
        elif bill.days_until_due <= 7:
            priority = "DUE_WEEK"
        else:
            priority = "DEFER"

        pay_run.append({
          "vendor": vendor.name, "bill": bill.number,
          "amount": bill.amount, "priority": priority,
          "discount_available": bill.discount_offered
        })

# Output: pay run sorted by priority
sorted_pay_run = sorted(pay_run, key=lambda x: ["URGENT","EARLY_PAY_DISCOUNT","DUE_WEEK","DEFER"].index(x["priority"]))
```

### Recipe 10 — Early-pay discount evaluator

```python
def early_pay_decision(bill, treasury_apy=0.05):
    """2/10 net 30 = 2% off if paid by day 10; full due day 30"""
    if not bill.discount_offered:
        return ("PAY_ON_TERMS", 0)

    discount = bill.discount_pct       # e.g., 0.02
    discount_window_days = bill.discount_window  # e.g., 10
    full_terms_days = bill.net_terms   # e.g., 30
    days_paid_early = full_terms_days - discount_window_days

    # Annualized return on early payment
    annualized = (discount / days_paid_early) * 365

    if annualized > treasury_apy:
        savings = bill.amount * discount
        return ("PAY_EARLY", savings)
    return ("PAY_ON_TERMS", 0)

# Example: 2/10 net 30 → annualized 36.5% → far better than 5% APY → PAY EARLY
```

### Recipe 11 — DSO calculation

```python
# Days Sales Outstanding = AR balance / daily revenue
# = AR / (Revenue / Days in period)

def dso(ar_balance, revenue, period_days=30):
    return ar_balance / (revenue / period_days)

# Benchmark by industry:
# - SaaS (mostly card): DSO 10-20 days
# - SaaS B2B (invoiced): DSO 30-45 days
# - Enterprise: DSO 45-75 days
# - Anything > 60 days for B2B = collection issue
```

### Recipe 12 — Bad debt allowance estimate

```python
def estimate_allowance(ar_aging):
    """Standard allowance percentages per bucket"""
    return (
      ar_aging.bucket_current * 0.005 +    # 0.5% on current
      ar_aging.bucket_1_30   * 0.02  +    # 2% on 1-30
      ar_aging.bucket_31_60  * 0.10  +    # 10% on 31-60
      ar_aging.bucket_61_90  * 0.30  +    # 30% on 61-90
      ar_aging.bucket_90_plus* 0.75       # 75% on 90+
    )
# Book as journal: Dr Bad Debt Expense / Cr Allowance for Doubtful Accounts
```

## Examples

### Example 1: Weekly AR sweep

**Goal:** Every Tuesday morning, send all due dunning emails.

**Steps:**

1. Pull AR aging (Recipe 1).
2. Run dunning cycle (Recipe 7) for today.
3. Log each email sent to internal CRM / spreadsheet.
4. Flag any invoice >60d past due to founder + legal review (Recipe 7 escalate branch).
5. Summarize to Slack `#finance-ar`:
   ```
   AR Aging 2026-06-09:
   - Current: $124K
   - 1-30: $52K (12 emails sent today)
   - 31-60: $18K (5 service-hold notices sent)
   - 61-90: $8K (2 escalations to founder)
   - 90+: $3K (allowance recommended)
   Total AR: $205K | DSO: 31 days (target ≤ 35)
   ```

**Result:** Predictable cadence; DSO trends down; founder only involved on 60+.

### Example 2: AP pay run with early-pay discounts

**Goal:** Weekly pay run optimizing cash + discounts.

**Steps:**

1. Pull AP aging (Recipe 9).
2. Evaluate each bill via Recipe 10.
3. Build pay run priority list:
   - URGENT (past due): 3 bills, $14K
   - EARLY_PAY_DISCOUNT: 4 bills, save $620 vs full terms
   - DUE_WEEK: 8 bills, $42K
   - DEFER: 11 bills, $58K (sit until next week)
4. Surface to founder: "DECISION REQUIRED — pay run $56K this week, saves $620 via early discounts. Approve?"
5. On approval, batch payment via Mercury (Recipe 3 of `mercury-modern-treasury-banking`).
6. Record payments in Xero against each bill.

**Result:** $56K AP cleared; $620 discount captured; 11 bills deferred.

## Edge cases / gotchas

- **Day-7 chase is the highest ROI single intervention** — 60%+ of overdue AR pays in the first chase.
- **Bank-feed delay:** "If you've already sent it, please ignore" — this softens the email. Always include.
- **Avoid sending chases on Mondays / Fridays** — Tuesday-Thursday gets better response rates.
- **Personalization:** key-account chases should come from the relationship owner (CSM, founder), not generic finance@. Template still works but signature matters.
- **Dispute path:** Day-14 must include "if there's a dispute, please reply today" — disputed AR has a different workflow (resolve dispute before chase escalates).
- **Service hold is real, not theater:** Day-30 commitment must be enforced. If product allows it, set up automated suspension after notice period. If not, manual SOP.
- **Time zone:** for global customers, send chases at recipient business hours, not yours.
- **Sales-tax on uncollected invoices:** if you've already remitted sales tax on the invoice but it ages out as bad debt, you can claim a refund in most states. Anrok / Avalara handle this; document.
- **Customer payment plan:** if customer requests a payment plan, draft a written agreement (1-page) + new invoice for each installment. Don't accept oral promises.
- **AP timing arbitrage:** stretching AP from net 30 to net 45 is industry norm in tight quarters; vendors expect 5-15 days slip. Don't apologize unless asked.
- **AP fraud risk:** new vendor + bank-account change request = always verify via phone callback before paying. CEO-fraud / vendor-impersonation scams target AP departments.
- **Stripe Smart Retries timing:** default Stripe retries 3 times; configurable to 4. For card-based subscription, set max_retry_attempts=4 + smart retry intervals (Recipe 8).

## Sources

- Xero Aged Receivables: https://developer.xero.com/documentation/api/accounting/reports/#agedreceivablesbycontact
- Xero Aged Payables: https://developer.xero.com/documentation/api/accounting/reports/#agedpayablesbycontact
- Stripe Smart Retries: https://docs.stripe.com/billing/subscriptions/smart-retries
- Mercury payments: https://docs.mercury.com/reference/payments
- ChaserHQ benchmarks: https://www.chaserhq.com/blog
- ChaserHQ: https://www.chaserhq.com/
- Upflow: https://upflow.io/
- Tesorio: https://www.tesorio.com/

## Related skills

- `xero-quickbooks-bookkeeping` — provides AR/AP aging reports
- `cash-flow-forecasting-13-week` — uses days-to-pay history from this skill
- `monthly-close-procedure` — uses aging reports for tie-out
- `mercury-modern-treasury-banking` — executes AP payments
