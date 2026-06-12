# Finance Controller — Role Content (appended to AGENT.md)

> This file appends to `AGENT.md` and is **not** loaded into the agent's default context. The agent reads `soul.md` every turn and **greps** this file for deep references when stuck.
>
> Search-friendly headings include: "Capability reference", "Monthly close playbook", "13-week cash flow playbook", "Runway and burn analysis playbook", "Unit economics playbook", "Cap table playbook", "ASC 606 revenue recognition playbook", "Equity grant playbook", "Audit prep playbook", "Sales tax playbook", "Investor update playbook", "Dunning email templates", "Antipattern catalog", "SOTA tool reference", "Bessemer 2026 benchmarks".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Accounting platforms supported

- **Xero** — primary via `xero-mcp` (catalog) + `xero` default skill (Maton-managed OAuth gateway). API: Contacts, Invoices, BankTransactions, Reports (P&L / BalanceSheet / CashSummary / AgedReceivables / AgedPayables / TrialBalance), Journals.
- **QuickBooks Online** — via Intuit official MCP (`intuit/quickbooks-online-mcp-server`, 143 tools, 11 reports) installed via `cli-anything`. OAuth 2.0 via developer.intuit.com.
- **NetSuite** — via Apideck / Knit unified MCP (`cli-anything`) when recipient has it; mid-market.
- **Sage Intacct** — same as NetSuite, mid-market.
- **Wave** (free, very small biz) — `cli-anything` + REST.
- **FreshBooks** — `cli-anything` + REST.

### Billing / revenue platforms

- **Stripe** — `stripe-mcp` (catalog) + `stripe-api` default skill. Billing, Revenue Recognition (0.25%), Sigma queries, Radar fraud, Tax.
- **Chargebee** — mid-market subscription; ASC 606 in product.
- **Maxio** (formerly SaaSOptics + Chargify) — audit-grade ASC 606, deferred revenue waterfalls, finance-led B2B SaaS.
- **Recurly** — involuntary-churn focus.
- **Paddle** — Merchant of Record (5% + $0.50, handles global sales tax); self-serve / micro-SaaS.
- **Lemon Squeezy** — MoR alt; smaller / indie.
- **Orb / Metronome** — usage-based pricing.

### Banking / treasury platforms

- **Mercury** — primary startup banking; invite-only API; treasury ~5% APY.
- **Brex** — multi-entity, 50+ countries; treasury; AI expense automation; *acquired by Capital One Jan 2026, $5.15B, close mid-2026*.
- **Ramp** — expense management leader; cards + AP automation + treasury (newer).
- **Modern Treasury** — multi-bank payment rails; payment ops; embedded finance.
- **Plaid** — bank-account linking + transaction aggregation; 12K+ US institutions.
- **Meow / Relay** — alt small-biz checking.

### Cap-table / equity platforms

- **Carta** — industry standard at Series A+; 40K+ companies, 7K+ VC funds. Partner API invite-only; mock at `https://mock-api.carta.com`. $5K-$80K/yr.
- **Pulley** — pre-seed to Series A; free tier <25 stakeholders; SAFE-first; 5-day 409A delivery; $1K-3.5K+/yr.
- **AngelList Stack** — bundled formation + cap table + payroll.
- **Capdesk** (UK / EU acquired by Carta).
- **Eqvista, Cake** — alts.

### FP&A / financial modeling platforms

- **Causal** — driver-based, visual multidimensional formulas; Seed–Series B; acquired by LucaNet Oct 2024.
- **Mosaic.tech** — Series C+ standard; multi-entity consolidation; acquired by Hibob Feb 2025.
- **Cube** — AI agent + native Excel/Sheets integration.
- **Runway** (financial planning) — UX-first; early-stage.
- **Drivetrain** — mid-market alt.
- **Vena / Anaplan / Workday Adaptive Planning** — enterprise.
- **Jirav** — SMB FP&A.

### Tax / compliance platforms

- **Anrok** — SaaS-specific multi-state sales tax; $100/mo Starter; 200+ jurisdictions.
- **Stripe Tax** — embedded; Stripe-only.
- **Avalara (AvaTax)** — enterprise ERP; opaque pricing.
- **TaxJar** — $90/mo Tax Complete; 600+ categories.
- **Quaderno** — SaaS-friendly alt.
- **Numeral** — newer AI-first.

### Investor reporting / fundraising platforms

- **Visible.vc** — Standard Investor Update template; Data Rooms; investor pipeline.
- **DocSend** — engagement analytics on shared decks.
- **Carta Investor Relations** module — integrated with cap table.
- **Foundersuite** — investor CRM.
- **AngelList Updates** — for AL-Stack companies.

### Audit / GRC platforms

- **Workiva** — internal audit, GRC, PBC list management.
- **Numeric.io** — month-end close automation.
- **Pilot AI Accountant** (launched Feb 2026).
- **Truewind** — AI-native bookkeeping for startups.

### Procurement / SaaS spend platforms

- **Vendr** — managed procurement; $18B+ benchmark database.
- **Tropic** — AI-driven; Tropic 2025 report = top-10 vendors = 74% of spend.
- **Spendflo** — AI procurement + managed sourcing.
- **Sastrify** — EU-focused.
- **SpendHound, Vertice, Zylo, Zluri, Torii, CloudEagle, Cledara** — alts.

### Equity research / public-comp sources

- `sec-edgar-mcp` — SEC EDGAR XBRL filings (10-K / 10-Q / 8-K) for peer financials, IPO comparables.
- `octagon-sec-mcp` — alt SEC research.
- `yahoo-finance-mcp` / `alpha-vantage-mcp` — public-market stock data.
- `mcp-finance` — multi-source finance aggregator.

---

## Monthly close playbook

### Timeline (5-10 business days from cutoff)

- **Day 1-2:** Cutoff confirmed. Pull bank feeds + credit-card statements + payroll register + AR/AP aging. Tag any pending invoices that should hit the period (cutoff discipline).
- **Day 3-5:** Reconcile bank-feed to ledger. Book missing transactions. Book accruals (deferred revenue, prepaid expenses, accrued payroll, accrued AP, accrued interest).
- **Day 5-7:** Run trial balance. Tie BS subledgers: AR aging → BS AR; AP aging → BS AP; fixed-asset register → PP&E net; equity rollforward → BS equity.
- **Day 7-9:** Generate P&L, Balance Sheet, Cash Flow. Tie CF roll to BS movement. Compute variance vs budget (>10% unfavorable flagged with one-line narrative).
- **Day 10:** Close period. Generate close memo + supporting schedules package. Distribute.

### Standard accrual conventions

- **Deferred revenue:** Customer invoiced or paid for service not yet delivered. Dr Cash / AR; Cr Deferred Revenue. Recognize ratably over service period (ASC 606).
- **Accrued revenue:** Service delivered but not yet invoiced. Dr Accrued Revenue; Cr Revenue.
- **Prepaid expense:** Cash paid for service not yet consumed (annual SaaS, annual insurance, rent prepayment). Dr Prepaid; Cr Cash. Amortize over service period.
- **Accrued expense:** Service consumed but invoice not yet received (utilities, contractors). Dr Expense; Cr Accrued Expense. Reverse when invoice arrives.
- **Accrued payroll:** Payroll period that straddles month-end. Dr Salary Expense; Cr Accrued Payroll. Reverse when paid.
- **Bad-debt allowance:** Estimate of uncollectable AR. Dr Bad-Debt Expense; Cr Allowance for Doubtful Accounts.
- **Depreciation:** Monthly amortization of PP&E per useful-life schedule. Dr Depreciation Expense; Cr Accumulated Depreciation.

### Journal-entry naming convention

`YYYY-MM-DD | [CATEGORY] | Description | [REF: Source doc / system]`

Example: `2026-06-30 | ACCRUAL | June AWS hosting accrual based on usage report | REF: AWS Billing 2026-06`

### Tie-out checklist

- [ ] Cash per BS = bank statements (all accounts) at cutoff
- [ ] AR per BS = AR aging report total
- [ ] AP per BS = AP aging report total
- [ ] Inventory per BS = inventory subledger (if applicable)
- [ ] PP&E per BS = fixed-asset register net
- [ ] Deferred revenue per BS = unearned revenue schedule
- [ ] Equity per BS = cap-table equity rollforward + retained earnings + period net income
- [ ] Total assets = total liabilities + total equity (to the penny)
- [ ] Net income on P&L = net income on CF statement
- [ ] Cash CF roll = closing cash − opening cash on BS

---

## 13-week cash flow playbook

### Structure

Three sections, one row per line item, 13 weekly columns (W1-W13).

```
                          | W1 | W2 | W3 | ... | W13 |
INFLOWS                   |    |    |    |     |     |
  Customer collections    |    |    |    |     |     |
  Other inflows (raise)   |    |    |    |     |     |
  Total inflows           |    |    |    |     |     |
OUTFLOWS                  |    |    |    |     |     |
  Payroll (semi-mo / bi)  |    |    |    |     |     |
  Rent / lease            |    |    |    |     |     |
  Vendor / AP             |    |    |    |     |     |
  Taxes (sales / payroll) |    |    |    |     |     |
  Debt service            |    |    |    |     |     |
  Subscriptions / SaaS    |    |    |    |     |     |
  One-time outflows       |    |    |    |     |     |
  Total outflows          |    |    |    |     |     |
NET CASH (in − out)       |    |    |    |     |     |
Opening cash              |    |    |    |     |     |
Closing cash              |    |    |    |     |     |
```

### Inflow timing

- Use **historical days-to-pay** per customer, not invoice date. If Customer X historically pays 47 days late, an invoice dated June 1 hits cash July 18, not June 1.
- For new customers, use industry average (45-60 days B2B SaaS, 30 days e-com).
- For pipeline / expected closes: include only if commit-stage with high probability (>80%), and quote conservative ACV.

### Outflow timing

- **Payroll:** semi-monthly (15th + last day), bi-weekly (every other Friday), or monthly (last day). Set the rule once, project mechanically.
- **Rent:** 1st of the month.
- **Vendor AP:** pay date = invoice date + net terms (most commonly net 30). Capture early-pay discounts when 2/10 (= 36% annualized return).
- **Taxes:** sales tax filing schedule per state; payroll taxes per cadence; quarterly federal estimates.
- **Subscriptions:** annual on anniversary date; monthly on signup-date.

### Update cadence

Refresh **every Monday morning** with: (1) actual closing cash from bank as of Friday, (2) last week's actual receipts + disbursements roll-forward, (3) any new pipeline closes or expected hits, (4) rebase W1-W13 from Monday.

### Critical signal

The week when cumulative closing cash drops below the **operating buffer** (typically 6 weeks of forward outflows) is the stop-the-line week. Surface it in the cover commentary.

---

## Runway and burn analysis playbook

### Definitions

- **Gross burn:** total monthly cash outflows (all OPEX + capex + debt service)
- **Net burn:** gross burn − cash inflows (cash basis revenue, not accrual)
- **Runway months:** current cash ÷ trailing-3-month average net burn
- **Default Alive (PG):** at current growth and current burn, does the company reach profitability before cash runs out? If yes = Default Alive; if no = Default Dead.
- **Burn multiple:** net burn ÷ net new ARR. <1.5x = healthy; <1.0x = elite; >2x = burning to grow inefficiently.

### Computation procedure

1. Pull last 3 closed months' P&L from `xero-mcp` / QBO MCP.
2. Pull last 3 closed months' bank balance from Mercury / Plaid / Modern Treasury.
3. Net burn = (cash opening month 1) − (cash closing month 3), divided by 3.
4. Runway = current cash ÷ net burn.
5. Sensitivity table: ±20% revenue, ±20% expense, full matrix.
6. Default Alive test: project revenue at current growth rate; project burn at current expense run-rate; find break-even month; compare to runway-end month.

### 2026 investor expectations

- **24-30 months post-funding runway** baseline expectation.
- **Burn multiple < 1.5x** baseline; <1.0x for top-decile valuations.
- The era of grow-at-all-costs is over per 2026 SaaS data — capital efficiency is baseline.

### Output format

Surface in this order: (1) current cash, (2) net burn last 3 mo, (3) runway in months, (4) Default Alive / Default Dead verdict, (5) burn multiple, (6) sensitivity grid, (7) recommendation queue if runway < 18 months (cut / raise / accelerate revenue / mix).

---

## Unit economics playbook

### Core SaaS metrics

| Metric | Formula | 2026 healthy benchmark | 2026 elite |
|---|---|---|---|
| ARR | MRR × 12 | — | — |
| CAC | Total S&M spend / new logos acquired (period) | — | — |
| CAC payback (months) | CAC / (ARPU × gross margin) | < 18 | < 12 |
| LTV | (ARPU × gross margin) / churn% | — | — |
| LTV:CAC | LTV / CAC | ≥ 3:1 | ≥ 5:1 |
| Gross margin | (Revenue − COGS) / Revenue | > 75% | > 80% |
| Net Revenue Retention (NRR) | (Starting MRR + expansion − churn − contraction) / Starting MRR | ≥ 100% | ≥ 120% |
| Gross Revenue Retention (GRR) | (Starting MRR − churn − contraction) / Starting MRR | ≥ 90% | ≥ 95% |
| Magic Number | (Current ARR − Prior ARR) × 4 / S&M spend | > 0.75 | > 1.5 |
| Rule of 40 | Growth% + EBITDA% | ≥ 40 | ≥ 60 |
| Burn Multiple | Net burn / net new ARR | < 1.5 | < 1.0 |
| ARR per employee | ARR / headcount | — | improving YoY |

### Computation procedure

1. Pull ARR / MRR from `stripe-mcp` Sigma queries (or Maxio / Chargebee equivalent).
2. Pull churn + expansion from `posthog-mcp` / CRM cohort analysis.
3. S&M spend from `xero-mcp` GL (filter to S&M cost centers).
4. Gross margin from P&L (Revenue − COGS) / Revenue.
5. Compute each metric; benchmark against 2026 stage targets (Seed / A / B / C+).
6. Surface improvement levers per metric:
   - Low NRR → expansion motion / pricing tier rework / churn root-cause
   - Long CAC payback → channel mix / ICP tightening / sales cycle shorten
   - High burn multiple → growth-efficiency (cut S&M waste) before adding $
   - Low Rule of 40 → either growth deficit or margin deficit — diagnose which

---

## Cap table playbook

### Standard instruments

- **Common stock** — founder / employee shares; usually with vesting (4-yr, 1-yr cliff).
- **Preferred stock** — investor-issued; priced rounds (Series Seed / A / B / etc.). Liquidation pref (1x non-participating standard), anti-dilution (weighted average broad-based standard), board rights.
- **ISO (Incentive Stock Option)** — employee only; tax-advantaged if held 1 yr post-exercise + 2 yr post-grant; $100K AMT rule (exercisable value > $100K/yr loses ISO treatment); 90-day post-termination exercise window.
- **NSO (Non-Qualified Stock Option)** — anyone; ordinary income tax at exercise on bargain element; no holding-period advantage.
- **RSU (Restricted Stock Unit)** — usually later-stage / public-track; double-trigger vesting common (time + liquidity event).
- **SAFE (Simple Agreement for Future Equity)** — YC standard. Post-money (default 2026) or pre-money. Valuation cap + discount. MFN clause optional. Converts to preferred at next priced round.
- **Convertible Note** — debt that converts to equity; has interest + maturity; valuation cap + discount.

### Fully-diluted total reconciliation

```
+ Common shares outstanding
+ Preferred shares outstanding (each series)
+ Options outstanding (exercised + vested + unvested + reserved pool)
+ Warrants outstanding
+ SAFE / convertible note as-converted (assume cap or discount, whichever lower)
= Fully diluted total
```

Any new issuance must reconcile to this total + new shares = updated total.

### Dilution math (priced round)

1. Pre-money valuation = $X
2. Investment = $Y
3. Post-money valuation = X + Y
4. New investor ownership = Y / (X + Y)
5. Existing dilution = X / (X + Y); each existing holder dilutes proportionally
6. Option pool top-up usually done **before** new investor counts (pre-money pool refresh) — this dilutes existing more

### SAFE → priced round conversion (YC post-money standard)

- Valuation cap $C; discount D% (e.g., 20%).
- At priced round at pre-money $P with investment $I:
  - Cap-based price = $C / fully-diluted shares pre-SAFE
  - Discount-based price = Series A price × (1 − D)
  - SAFE converts at the lower of the two
- Post-money SAFE: SAFE holders' ownership target is preserved by issuing new pre-money shares to the cap.

---

## ASC 606 revenue recognition playbook

### Five-step model

1. **Identify the contract** with the customer (written / oral / implied, enforceable).
2. **Identify the performance obligations** (distinct goods/services in the contract).
3. **Determine the transaction price** (variable consideration estimated and constrained).
4. **Allocate the transaction price** to performance obligations (relative standalone selling price).
5. **Recognize revenue when (or as)** performance obligation is satisfied.

### Common patterns

- **SaaS subscription** — single PO satisfied ratably over the subscription term. Monthly recognition straight-line.
- **Setup / implementation fee** — if distinct, recognized at setup completion. If not distinct (only useful with the subscription), recognized over subscription term.
- **Professional services** — distinct if separately negotiated and not required for SaaS use; point-in-time on delivery or percent-complete.
- **Term license + maintenance** — license at start (point-in-time), maintenance ratably.
- **Usage-based** — recognize as usage occurs; for fixed minimums, recognize over time and true up.
- **Multi-year discount** — bills upfront; recognized ratably; deferred revenue waterfall is the entire prepaid balance.

### Deferred revenue waterfall

For each invoice / subscription, schedule monthly recognition over service term. Sum the waterfall = balance sheet deferred revenue.

Example: $12,000 annual SaaS invoiced June 1 → recognize $1,000/mo Jun-May. June BS deferred revenue = $11,000; July = $10,000; etc.

### Output

- Stripe Revenue Recognition product (0.25%) auto-generates this.
- Manual: xlsx waterfall — invoice on rows, months on columns, recognition $/month in cells, sum down columns = monthly recognized revenue, sum across rows = total invoice.

---

## Equity grant playbook

### Grant decision tree

1. **Grantee employee?** → ISO (preferred if eligible) or NSO.
2. **Grantee contractor / advisor?** → NSO or restricted stock.
3. **Grantee founder?** → restricted stock with vesting + 83(b) election.
4. **Grantee post-IPO-track?** → RSU.

### 83(b) election (CRITICAL — 30-day window)

- Applies to: restricted stock subject to vesting OR early-exercised options.
- What it does: elect to pay ordinary income tax on the spread between FMV and price paid at grant date (vs at vesting). Future appreciation is long-term capital gain.
- **30-day filing window from grant date** to IRS — missed window = no election possible.
- File: signed form to IRS by mail (certified return-receipt); copy to employer; keep copy in personal records.
- Default agent action: **on every restricted-stock or early-exercise grant, schedule a `remindme` task at day 25 to ensure filing by day 30.**

### ISO mechanics

- Strike price ≥ current 409A FMV (mandatory; below = 409A penalty).
- $100K AMT rule: if (strike × shares becoming exercisable in calendar year) > $100K, the excess is NSO-treated.
- 90-day post-termination exercise window standard (some companies extend to 10 years — surface as policy decision).
- Long-term holding: 1 yr post-exercise + 2 yr post-grant for LTCG treatment + ISO disposition.
- AMT exposure on exercise: bargain element at exercise is AMT income (even if not regular income).

### ASC 718 stock-based compensation expense

- Compute fair value at grant date using Black-Scholes or binomial model.
- Recognize expense over vesting period (straight-line for cliff + ratable; graded for tranches).
- Pull from Carta / Pulley's ASC 718 module OR build pandas waterfall.

---

## Audit prep playbook (Big 4 / regional)

### Timeline

- **T-90 (3 months pre-fieldwork):** Entity understanding doc with auditor. Risk assessment. Materiality threshold set. Scoping decisions.
- **T-60:** Internal control walkthroughs. Identify in-scope material accounts. Trial balance generated.
- **T-30:** PBC (Prepared-by-Client) list finalized and assigned to owners. Supporting schedules being built. Initial submission to auditor.
- **Fieldwork (typically 2-6 weeks):** Respond to auditor sample selections. Provide GL detail. Document explanations. Resolve adjustments.
- **Post-fieldwork:** Audit committee review. Management letter response. Final reports.

### PBC list standard items

- 01_TB: Trial balance + chart of accounts
- 02_AR: AR roll-forward, aging, top-customer detail, allowance computation
- 03_AP: AP roll-forward, aging, top-vendor detail
- 04_PPE: Fixed-asset register, depreciation schedule, additions/disposals
- 05_DefRev: Deferred revenue waterfall, ASC 606 contract review (samples)
- 06_Equity: Cap table, option register, ASC 718 expense waterfall, board minutes
- 07_Payroll: Payroll register, payroll tax filings, equity comp roll
- 08_Debt: Loan agreements, amortization schedules, covenant compliance
- 09_Leases: Lease agreements, ASC 842 right-of-use asset + lease liability schedules
- 10_Tax: Tax provision, deferred tax computation, state nexus map
- 99_Other: Bank statements, board minutes, contracts (material), confirmations

---

## Sales tax / VAT playbook

### Nexus mapping

- **Physical nexus:** office, employee, warehouse, inventory in state.
- **Economic nexus (post-Wayfair):** typically $100K revenue OR 200 transactions in 12-month period (varies by state — CA $500K; some lower).
- For SaaS: also map jurisdictions that tax software-as-a-service:
  - Tax SaaS as default: NY, PA, TX, WA, SC, TN, UT, OH, IA, AZ
  - Don't tax SaaS: CA, FL, NV, MO, IL (most)
  - Tax with caveats: CT (B2C only), MA (some), DC (yes)

### Platform recommendation matrix

| Use case | Recommended |
|---|---|
| 100% Stripe + < 5 states | Stripe Tax |
| SaaS-specific, multi-state, < $50M | Anrok |
| Enterprise ERP (NetSuite / Sage), multi-jurisdiction | Avalara |
| E-commerce, physical goods | TaxJar or Avalara |
| MoR-eligible, want to outsource entirely | Paddle or Lemon Squeezy |
| EU-focused, VAT | Quaderno or Avalara |

### Workflow

1. Map nexus per state (revenue, transactions, physical presence).
2. Map product taxability per state.
3. Register where nexus is triggered (each state has a separate registration; some take 4-12 weeks).
4. Configure platform to calculate at checkout / invoice.
5. Remit + file per cadence (monthly / quarterly / annual depending on volume + state).
6. Reconcile filings to GL sales tax payable account each close.

---

## Investor update playbook

### Visible.vc Standard template (monthly)

```
SUBJECT: [Company Name] — [Month YYYY] Update

TL;DR — 3-5 lines, lead with cash + biggest win

KEY METRICS (table)
- Cash on hand: $X | Runway: Y months | Net burn: $Z/mo
- ARR: $X (±% MoM) | MRR: $Y | NRR: Z%
- New logos: X | Logo churn: Y | Net new ARR: $Z
- Headcount: X (start) | hires: Y | departures: Z

HIGHLIGHTS (3-5 bullets)
- [Win 1 — quantified]
- [Win 2]
- [Win 3]

LOWLIGHTS (3-5 bullets — yes, this is mandatory)
- [Challenge 1]
- [Challenge 2]

ASKS (mandatory; don't leave empty)
- Intros to [specific personas / companies]
- Help with [specific decision / hire / customer]

FINANCIALS (1-page summary; full pack in data room)
- P&L summary, Balance Sheet summary, Cash trend

THANKS
[Sign-off]
```

### Cadence

- **Active raise:** monthly (or bi-weekly during pipeline closure).
- **Steady state:** monthly to lead investors, quarterly to all.
- **Post-IPO-track:** quarterly with audit-aligned content.

### Conservative number discipline

- ARR = month-end snapshot of currently invoicing customers, not pipeline.
- Bookings = signed contracts in period, with effective dates clear.
- Pipeline = label as pipeline, not revenue. "$2M qualified pipeline" not "$2M tracking."
- Runway = current cash ÷ trailing-3-month net burn, not forecasted burn.

---

## Dunning email templates

### Day 0 — Friendly reminder (when invoice issued)

```
Subject: Invoice [#] — $[amount] due [date]

Hi [Name],

A quick note that invoice #[N] for $[amount] is due [date]. You can pay
via [link / wire instructions / ACH details].

If there are any questions about the invoice, just reply here — happy
to walk through line items.

Thanks,
[Sender]
```

### Day 7 past due — First chase

```
Subject: Invoice [#] past due — $[amount]

Hi [Name],

Quick check-in: invoice #[N] for $[amount] was due [date] and is now
7 days past due. Could you let me know the expected payment date so
we can update our records?

If you've already sent it, please ignore — bank-feed delay is real.

Thanks,
[Sender]
```

### Day 14 past due — Firm

```
Subject: Invoice [#] — 14 days past due — please pay by [date]

Hi [Name],

Invoice #[N] for $[amount] is now 14 days past due. Per our terms,
we need to receive payment by [date].

If there's a payment issue or dispute, please reply here today and
we'll work through it. If it's been paid, please send us the confirmation.

Thanks,
[Sender]
```

### Day 30 past due — Escalation / service hold

```
Subject: Invoice [#] — service hold notice

Hi [Name],

Invoice #[N] for $[amount] is 30 days past due. Per our terms, we'll
pause service on [date + 3 business days] if payment is not received.

I want to avoid that — please reply today so we can find a resolution.

Thanks,
[Sender]
```

---

## Antipattern catalog

### Antipattern 1: Quoting ARR from memory or prior conversation

**BAD:** "Last we talked, ARR was $1.2M, so runway is..."

**Why bad:** stale data = wrong data. ARR changes weekly. Decisions based on stale numbers compound.

**GOOD:** "Let me pull current ARR from Stripe Sigma — give me a moment... ARR is $1.27M as of 2026-06-08 per Stripe."

### Antipattern 2: Channel-stuffing / pulling revenue forward

**BAD:** Customer signs annual contract in June, pays upfront $120K. Book all $120K as revenue in June to make the quarter.

**Why bad:** violates ASC 606. Auditors restate. Investors lose trust.

**GOOD:** Dr Cash $120K; Cr Deferred Revenue $120K. Recognize $10K/mo over 12 months. Book deferred revenue waterfall.

### Antipattern 3: Capitalizing routine software / SaaS

**BAD:** Capitalize annual Notion subscription as software asset, amortize over 12 months.

**Why bad:** OPEX masquerading as capex inflates EBITDA artificially. Auditors will reclass.

**GOOD:** Expense as SaaS subscription in the period consumed. Prepay treatment if invoiced upfront (Dr Prepaid; Cr Cash; amortize to expense ratably).

### Antipattern 4: Granting ISOs below 409A FMV

**BAD:** "We haven't updated 409A in 18 months — let's just use last year's number to grant new ISOs."

**Why bad:** IRC 409A penalty: 20% federal penalty + interest on the difference if FMV is stale (>12 months since last 409A, or material event triggered re-valuation).

**GOOD:** Schedule fresh 409A through Carta / Pulley (~$1-4K, 5-30 days). Use updated FMV. Hold grants pending.

### Antipattern 5: Investor update with no lowlights or asks

**BAD:** "Crushing it! ARR up 30% MoM. Team morale high. Onward!"

**Why bad:** Investors don't believe it. Anyone running a startup has challenges. No-asks = "I don't need your network" = a closed loop.

**GOOD:** Three highlights, three lowlights, three asks. Even if asks are "intros to X persona at Y company."

### Antipattern 6: Runway computed from forecast burn instead of actual

**BAD:** "Our budget says we'll burn $80K/mo, so we have 22 months."

**Why bad:** Budgets are usually optimistic. Actual burn is what matters for survival.

**GOOD:** Use trailing-3-month average net burn from closed books. If that's $120K, runway is ~15 months — surface this.

### Antipattern 7: Auto-paying without dual approval

**BAD:** Agent batches and submits all AP > 30 days past due automatically.

**Why bad:** No human checkpoint = fraud risk, vendor-impersonation exposure, errors that move money.

**GOOD:** Agent prepares batch, surfaces "DECISION REQUIRED: confirm batch of $X across N vendors." Human approves. Then execute.

### Antipattern 8: Missing 83(b) by treating it as "later"

**BAD:** Founder restricted stock granted Day 1; founder doesn't file 83(b); discovers month 2.

**Why bad:** 30-day window from grant date is hard. Missed = pay ordinary income tax on future vesting at then-current FMV (huge tax bill if company appreciates).

**GOOD:** On any restricted-stock grant or early-exercise, immediately schedule reminder at day 25 to confirm filing by day 30.

---

## SOTA tool reference (June 2026)

Per-tool quick reference. Each entry: when to use, primary endpoint / install, source. Detailed recipes live in the bundled skill packs at `skills/<name>/SKILL.md` — heading text below maps 1:1 to the skill folder name.

### Intuit QuickBooks Online MCP Server (skill: `xero-quickbooks-bookkeeping`)

- **Use for:** QBO bookkeeping CRUD across 29 entities (Customer, Vendor, Invoice, Bill, Payment, Journal, etc.) + 11 financial reports (P&L, Balance Sheet, Cash Flow, Aged Receivables, Aged Payables, Trial Balance).
- **Install:** `cli-anything` → `git clone https://github.com/intuit/quickbooks-online-mcp-server`, configure OAuth 2.0 via developer.intuit.com (Client ID + Secret).
- **Quick recipe:**
  ```bash
  uvx --from intuit-quickbooks-mcp qbo-mcp-server --report profit_and_loss --start 2026-01-01 --end 2026-06-30
  ```
- **Source:** https://github.com/intuit/quickbooks-online-mcp-server
- **Skill:** `skills/xero-quickbooks-bookkeeping/SKILL.md`

### Xero MCP Server (skill: `xero-quickbooks-bookkeeping`, MCP: `xero-mcp`)

- **Use for:** Xero accounting CRUD; same scope as QBO. Catalog MCP — recipient configures via Xero OAuth.
- **Install:** Enable `xero-mcp` in CraftBot MCP settings; OAuth at developer.xero.com.
- **Quick recipe:** `xero-mcp.reports.profit_and_loss(from='2026-06-01', to='2026-06-30')`
- **Source:** https://github.com/XeroAPI/xero-mcp-server
- **Skill:** `skills/xero-quickbooks-bookkeeping/SKILL.md`

### Stripe Revenue Recognition (skill: `stripe-revenue-recognition-asc606`, MCP: `stripe-mcp`)

- **Use for:** ASC 606 deferred revenue waterfall auto-generated from Stripe Billing data. 0.25% fee on top of standard processing.
- **Endpoint:** Stripe Dashboard → Revenue Recognition; API access via `stripe-mcp` reports endpoints.
- **Quick recipe:** Enable Revenue Recognition product in dashboard → configure recognition rules per product → export monthly waterfall via API.
- **Source:** https://docs.stripe.com/revenue-recognition
- **Skill:** `skills/stripe-revenue-recognition-asc606/SKILL.md`

### Maxio (skill: `chargebee-maxio-paddle-billing`)

- **Use for:** audit-grade ASC 606 for finance-led B2B SaaS; deferred revenue schedules auto-generated; books in days, not weeks. Built specifically for revenue-recognition-heavy SaaS.
- **Install:** `cli-anything` → REST API; `MAXIO_API_KEY` env var.
- **Source:** https://www.maxio.com/
- **Skill:** `skills/chargebee-maxio-paddle-billing/SKILL.md`

### Chargebee (skill: `chargebee-maxio-paddle-billing`)

- **Use for:** mid-market subscription billing; built-in revenue recognition; multi-currency; complex pricing rules.
- **Install:** `cli-anything` → `curl -u $CHARGEBEE_API_KEY https://[site].chargebee.com/api/v2/...`
- **Source:** https://apidocs.chargebee.com/

### Paddle / Lemon Squeezy (skill: `chargebee-maxio-paddle-billing`)

- **Use for:** Merchant of Record (MoR) — handles global sales tax / VAT / GST + currency + chargebacks in exchange for 5% + $0.50/txn. Best for self-serve / micro-SaaS without dedicated tax ops.
- **Install:** Paddle: `curl -H "Authorization: Bearer $PADDLE_API_KEY" https://api.paddle.com/...`; Lemon Squeezy similar.
- **Source:** https://developer.paddle.com/ · https://docs.lemonsqueezy.com/

### Mercury API (skill: `mercury-modern-treasury-banking`)

- **Use for:** startup banking; cash balance, transactions, wires, ACH, treasury (~5% APY on idle cash). API invite-only as of 2026.
- **Install:** Mercury Dashboard → Settings → API → request access; key in `MERCURY_API_KEY`.
- **Quick recipe:**
  ```bash
  curl -H "Authorization: Bearer $MERCURY_API_KEY" https://api.mercury.com/api/v1/accounts
  ```
- **Source:** https://docs.mercury.com/reference/welcome
- **Skill:** `skills/mercury-modern-treasury-banking/SKILL.md`

### Modern Treasury (skill: `mercury-modern-treasury-banking`)

- **Use for:** multi-bank payment rails; payment ops; embedded finance for non-banks. Self-serve API.
- **Install:** `MODERN_TREASURY_API_KEY` + `MODERN_TREASURY_ORG_ID`.
- **Quick recipe:**
  ```bash
  curl -u "$ORG_ID:$API_KEY" https://app.moderntreasury.com/api/payment_orders
  ```
- **Source:** https://docs.moderntreasury.com/

### Plaid (skill: `mercury-modern-treasury-banking`)

- **Use for:** read-only bank account linking + transaction aggregation across 12K+ US institutions. Best when consolidating multiple bank accounts.
- **Install:** Plaid Dashboard → Get API keys → link-token flow.
- **Quick recipe:**
  ```bash
  curl -H "PLAID-CLIENT-ID: $CID" -H "PLAID-SECRET: $SECRET" \
    -X POST https://production.plaid.com/transactions/sync \
    -d '{"access_token":"$AT","cursor":""}'
  ```
- **Source:** https://plaid.com/docs/api/

### Ramp API (skill: `ramp-brex-expense-management`)

- **Use for:** corp cards + expense automation + AP automation + receipt matching + policy enforcement. Leader in expense management.
- **Install:** Ramp Dashboard → Settings → Developer → API key.
- **Quick recipe:**
  ```bash
  curl -H "Authorization: Bearer $RAMP_API_KEY" \
    https://api.ramp.com/developer/v1/transactions?limit=100
  ```
- **Source:** https://docs.ramp.com/developer-api/v1/overview

### Brex API (skill: `ramp-brex-expense-management`)

- **Use for:** multi-entity corp cards (50+ countries), expense, treasury. *Acquired by Capital One Jan 2026 — API surface evolving through close mid-2026.*
- **Install:** Brex Dashboard → Developer → OAuth or token.
- **Quick recipe:**
  ```bash
  curl -H "Authorization: Bearer $BREX_TOKEN" \
    https://platform.brexapis.com/v2/transactions/card
  ```
- **Source:** https://developer.brex.com/

### Carta API (skill: `carta-pulley-cap-table`)

- **Use for:** cap-table maintenance; option grant CRUD; 409A workflow; ASC 718 expense waterfall; fund-side investor reporting. Partner API invite-only; mock at `https://mock-api.carta.com`.
- **Install:** Apply at developers.app.carta.com → invite-only approval → OAuth 2.0.
- **Quick recipe:**
  ```bash
  curl -H "Authorization: Bearer $CARTA_TOKEN" \
    https://api.carta.com/v1alpha/companies/{cik}/cap_table
  ```
- **Source:** https://carta.com/api/ · https://docs.carta.com/api-platform/docs/introduction

### Pulley (skill: `carta-pulley-cap-table`)

- **Use for:** pre-seed to Series A cap table; SAFE-first modeling; 5-day 409A. Free tier <25 stakeholders.
- **Install:** Pulley Dashboard → integrations → API access (limited surface).
- **Source:** https://pulley.com/products/esop-management-software

### Causal (skill: `causal-mosaic-financial-modeling`)

- **Use for:** driver-based, visual multidimensional formulas; scenario modeling; Seed–Series B sweet spot. Acquired by LucaNet Oct 2024.
- **Install:** Causal Dashboard → API key.
- **Source:** https://causal.app/ · https://valueaddvc.com/blog/best-financial-modeling-tools-for-startups-excel-vs-runway-vs-causal-vs-mosaic

### Mosaic.tech (skill: `causal-mosaic-financial-modeling`)

- **Use for:** Series C+ standard; multi-entity consolidation; integrates with ERP + CRM + HR; board dashboards. Acquired by Hibob Feb 2025.
- **Install:** Mosaic Dashboard → API.
- **Source:** https://www.mosaic.tech/

### Cube (skill: `causal-mosaic-financial-modeling`)

- **Use for:** AI agent + native Excel / Google Sheets integration. "Agentic finance layer for FP&A."
- **Install:** Cube Dashboard → API + Excel/Sheets connector.
- **Source:** https://www.cubesoftware.com/

### Anrok (skill: `anrok-stripe-tax-sales-tax-compliance`)

- **Use for:** SaaS-specific multi-state sales tax; calculation + obligation monitoring + filing + remittance in one. 200+ jurisdictions. $100/mo Starter.
- **Install:** Anrok Dashboard → API key.
- **Quick recipe:**
  ```bash
  curl -H "Authorization: Bearer $ANROK_API_KEY" \
    https://api.anrok.com/v1/transactions
  ```
- **Source:** https://www.numeral.com/blog/avalara-vs-anrok · https://anrok.com/

### Stripe Tax (skill: `anrok-stripe-tax-sales-tax-compliance`, MCP: `stripe-mcp`)

- **Use for:** embedded tax calc within Stripe workflows. Stripe-only; good if 100% Stripe revenue.
- **Endpoint:** `stripe-mcp` → `tax/calculations` + `tax/transactions`.
- **Source:** https://docs.stripe.com/tax

### Pilot AI Accountant (skill: `monthly-close-procedure`)

- **Use for:** "world's first AI Accountant" — Feb 2026 launch; runs onboarding to monthly close with claimed zero human intervention. Reference for autonomous-close design.
- **Source:** https://pilot.com/platform/ai-accountant

### Numeric.io (skill: `monthly-close-procedure`)

- **Use for:** month-end close automation; reconciliation; flux analysis; financial statement preparation.
- **Source:** https://www.numeric.io/

### Truewind (skill: `monthly-close-procedure`)

- **Use for:** AI-native bookkeeping for startups + accounting firms. 47% automation rate for month-end tasks.
- **Source:** https://www.truewind.ai/

### Visible.vc API (skill: `investor-update-monthly-quarterly`)

- **Use for:** investor update authoring + sending + tracking; Standard template + data rooms; investor pipeline / CRM.
- **Install:** Visible Dashboard → API.
- **Source:** https://visible.vc/templates/the-visible-standard-investor-update-template/ · https://visible.vc/product/data-rooms/

### SEC EDGAR (MCP: `sec-edgar-mcp`)

- **Use for:** peer financials from 10-K / 10-Q / 8-K for benchmarking; IPO comparables; market sizing.
- **MCP:** `sec-edgar-mcp` (catalog) — recipient enables in CraftBot MCP settings.
- **Source:** https://www.sec.gov/edgar/sec-api-documentation

### PostHog (MCP: `posthog-mcp`)

- **Use for:** product analytics for NRR + cohort retention + activation funnel. HogQL queries for custom cohorts.
- **MCP:** `posthog-mcp` (catalog).
- **Source:** https://posthog.com/docs/api

### Vendr / Tropic / Spendflo (skill: `vendor-procurement-saas-spend-audit`)

- **Use for:** managed procurement + spend benchmarks for SaaS contracts; pricing leverage data; renewal automation.
- **Tropic 2025 benchmark:** top-10 SaaS vendors = 74% of total SaaS spend in typical company.
- **Source:** https://www.tropicapp.io/reports/software-spending-trends-2025 · https://www.spendflo.com/pricing-benchmarks

### Workiva (skill: `audit-prep-big4-checklist`)

- **Use for:** audit management + PBC list workflow + GRC dashboards. Most common Big 4 audit collaboration platform.
- **Source:** https://www.workiva.com/solutions/internal-audit-management

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Close the books for [month]" | `monthly-close-procedure` + `xero-quickbooks-bookkeeping` | 5-10 day timeline; tie-out checklist |
| "What's our cash / runway?" | `runway-burn-analysis` + `xero-quickbooks-bookkeeping` | Always start with trailing-3-month actual burn |
| "Build a 13-week cash forecast" | `cash-flow-forecasting-13-week` + `xlsx` | Refresh every Monday |
| "What's our NRR / Rule of 40 / Magic Number?" | `unit-economics-saas-metrics` + `stripe-mcp` + `posthog-mcp` | Benchmark vs 2026 stage targets |
| "Recognize this revenue contract" | `stripe-revenue-recognition-asc606` | Five-step ASC 606; deferred revenue waterfall |
| "I need to update the cap table" | `carta-pulley-cap-table` | Reconcile fully-diluted total; surface dilution math |
| "I'm granting equity to [hire]" | `equity-grant-83b-isos-rsus` + `carta-pulley-cap-table` | 83(b) reminder; FMV check; ASC 718 |
| "Draft this month's investor update" | `investor-update-monthly-quarterly` | Visible.vc Standard template; mandatory asks |
| "Prep the data room" | `fundraising-data-room` + `file-organizer` | Section checklist; YC SAFE template |
| "Audit is in 90 days" | `audit-prep-big4-checklist` | T-90 / T-60 / T-30 timeline; PBC list owners |
| "Are we in the right sales-tax states?" | `anrok-stripe-tax-sales-tax-compliance` | Nexus footprint + product taxability matrix |
| "Run a vendor / SaaS spend audit" | `vendor-procurement-saas-spend-audit` | Top-10 = 74% of spend; duplicates + renewals |
| "Build our 2027 budget" | `causal-mosaic-financial-modeling` + `headcount-planning-hiring-budget` | Driver-based; 3-statement |
| "Our gross margin is dropping" | `cogs-margin-improvement-analysis` | Hosting + support + payment fees + LLM inference decomposition |
| "Chase our AR" | `ar-ap-aging-collections` + `gmail-mcp` | Day 0 / 7 / 14 / 30 dunning cadence |
| "What's our 409A?" | `carta-pulley-cap-table` | Recompute when stale or material event |

---

## Brief / Output templates

### Monthly close memo (1-2 pages)

```
COMPANY: [Name]
PERIOD CLOSED: [Month YYYY]
CLOSE DATE: [Date completed]
PREPARED BY: [Controller]
REVIEWED BY: [CFO / Founder]

TL;DR
- [3 lines: net income, cash position, runway, top variance]

P&L SUMMARY
[Revenue / COGS / Gross Profit / OpEx / EBITDA — vs budget + prior period]

BALANCE SHEET HIGHLIGHTS
[Cash, AR, AP, Deferred Revenue, Equity changes]

CASH FLOW SUMMARY
[Operating / Investing / Financing]

VARIANCE NARRATIVE
- [Top 3-5 variances >10% with one-line explanation]

OPEN ITEMS / RISKS
- [Anything that needs management attention]

ATTACHMENTS
- 01_TB.xlsx, 02_PL.pdf, 03_BS.pdf, 04_CF.pdf, 05_AR_aging.xlsx, 06_AP_aging.xlsx
```

### 1-page investor update (Visible.vc Standard)

See "Investor update playbook" above for full template.

### 13-week cash forecast cover commentary

```
AS OF: [Date]
OPENING CASH: $[X]
WEEK 13 PROJECTED CLOSING CASH: $[Y]
WEEKS UNTIL CASH BUFFER (6 weeks of forward outflows) TRIGGERED: [N]

KEY ASSUMPTIONS
- [Top 3 assumptions driving the forecast]

KEY RISKS
- [Top 3 things that would push the forecast unfavorable]

REQUESTED DECISIONS
- [Any AP timing or financing decisions needed this week]
```

---

## Closing rules

Reconcile weekly. Close monthly. Run on fresh data. Lead with cash. Conservative on revenue, aggressive on COGS. Tie everything out to the penny (or to materiality with rationale). Always disclose "consult a licensed CPA / CFO" before binding financial / tax decisions. Defer pipeline forecasting to `sales-agent`; binding term-sheet review to `legal-counsel`; product-side unit economics to `product-manager`. Cash is the only number that matters until runway is more than 18 months.
