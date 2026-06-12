# Finance Controller — Use Cases

**Tier:** general · **Category:** finance
**Core job:** End-to-end finance operator — bookkeeping, monthly close, cash forecasting, SaaS metrics, cap table, ASC 606, AR/AP, audits, investor updates, fundraising data room.

> Ships with the SOTA 2026 finance stack — Xero / QuickBooks Online (Intuit official MCP) for bookkeeping; Stripe (incl. Revenue Recognition for ASC 606); Mercury / Modern Treasury / Plaid for banking; Ramp / Brex for expense management; Carta / Pulley for cap table + 409A + equity grants; Causal / Mosaic / Cube for FP&A; Anrok / Stripe Tax for sales tax; Visible.vc Standard template for investor updates; Workiva-style PBC list for audit prep. Executes end-to-end against the books, billing, banking, and cap table — does not just direct the user. **Always discloses "consult a licensed CPA / CFO for binding financial / tax decisions"** — humans approve binding actions; the agent computes, models, and surfaces.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Bookkeeping + accounting
- Daily / weekly transaction recording in Xero or QuickBooks Online
- Bank-feed reconciliation (Mercury / Plaid / Modern Treasury → ledger)
- Credit-card statement reconciliation (Ramp / Brex / corp cards → ledger)
- Chart-of-accounts setup and ongoing maintenance
- Subledger maintenance (AR, AP, fixed-asset register, deferred revenue waterfall)

### Monthly close
- 5-10 business day close cycle (cutoff → tie-out → distribution)
- Accrual conventions (deferred revenue, prepaids, accrued payroll, accrued AP, bad-debt allowance, depreciation)
- Trial balance + journal-entry preparation with documentation
- P&L, Balance Sheet, Cash Flow statement generation + tie-out
- Subledger reconciliation (AR/AP/PP&E/equity rollforward)
- Variance vs budget (>10% unfavorable flagged with narrative)
- Close memo + supporting schedules distribution

### Cash management + runway
- Daily cash position pull from all bank / treasury accounts
- Burn rate computation (gross + net) from trailing 3 closed months
- Runway months calculation + Default-Alive / Default-Dead verdict
- 13-week rolling cash flow forecast (weekly granularity; Monday refresh)
- Sensitivity analysis (±20% revenue, ±20% expense)
- Treasury sweep recommendations (yield optimization on idle cash)

### SaaS unit economics
- ARR / MRR snapshot + delta
- CAC + LTV + LTV:CAC + CAC payback (months)
- Net Revenue Retention (NRR) + Gross Revenue Retention (GRR)
- Magic Number + Rule of 40 + Burn Multiple
- ARR per employee + headcount efficiency
- Benchmark vs 2026 Bessemer / SaaS Capital / Eagle Rock CFO stage targets
- Improvement lever identification per metric

### Revenue + billing
- ASC 606 five-step revenue recognition
- Deferred revenue waterfall (monthly recognition schedule)
- Multi-product / multi-element arrangement allocation
- Subscription billing setup (Stripe / Chargebee / Maxio / Paddle / Recurly decision)
- Merchant-of-Record evaluation (Paddle / Lemon Squeezy vs in-house tax)

### AR + AP
- AR aging analysis (current / 1-30 / 31-60 / 61-90 / 90+)
- Dunning cadence (Day 0 / 7 / 14 / 30 templates) via Gmail
- Bad-debt allowance computation
- AP aging + batch payment runs (human-approved, dual-approval for >$10K)
- Early-pay discount math (2/10 net 30 = 36% annualized)
- Vendor reconciliation

### Cap table + equity
- Cap-table maintenance (Carta / Pulley) — issuance, exercises, transfers, terminations
- Fully-diluted reconciliation per round
- Dilution math (priced rounds, SAFE conversions)
- Standard YC post-money SAFE template + modeling
- Convertible note modeling (cap + discount + interest + maturity)
- Option grant administration (ISOs / NSOs / RSUs)
- 409A valuation prep + tracking (Carta ~$2-4K/yr; Pulley 5-day delivery)
- ASC 718 stock-based compensation expense waterfall

### Equity tax mechanics
- 83(b) election 30-day window tracking + reminder
- $100K ISO AMT rule compliance
- 90-day post-termination exercise window administration
- AMT exposure estimate at exercise
- Long-term vs short-term capital gains analysis

### FP&A — budget, forecast, scenario
- Annual budget (3-statement, bottom-up by department)
- Quarterly forecast (revenue, expenses, headcount, cash)
- Scenario modeling (base / downside / upside)
- Driver-based modeling in Causal / Mosaic / Cube / Runway or xlsx
- Re-base when YTD variance >5%

### Headcount + comp planning
- Driver-based headcount per function
- Comp band per role × geography
- Fully loaded cost (1.3-1.4x base) → P&L flow
- Sequence hires against Rule of 40 / burn multiple discipline

### COGS + gross margin
- COGS decomposition (hosting + support + payment fees + LLM inference + customer success)
- Gross margin trend + drivers
- >75% SaaS gross margin target diagnostics

### Sales tax + VAT compliance
- Nexus mapping (economic + physical) per state
- SaaS product taxability matrix per jurisdiction
- Platform selection (Anrok / Stripe Tax / Avalara / TaxJar / MoR)
- Multi-state registration coordination
- Filing calendar maintenance + reconciliation to GL

### Investor relations + reporting
- Monthly investor update (Visible.vc Standard template — TL;DR / metrics / highlights / lowlights / asks / financials)
- Quarterly board pack (financials + KPIs + narrative)
- Lead-investor cadence management
- Y Combinator template variant for YC-backed companies

### Fundraising + data room
- Data-room organization (cap table / financials / metrics / contracts / IP / team / legal)
- Standard YC post-money SAFE template fill
- Term-sheet clause-by-clause comparison vs market norms (economics + control + other)
- Diligence Q&A coordination

### Audit prep + GRC
- Big 4 / regional audit prep (T-90 / T-60 / T-30 timeline)
- PBC (Prepared-by-Client) list management + owner assignment
- Supporting schedules library (AR roll, AP roll, PP&E roll, deferred revenue waterfall, equity rollforward, payroll register, debt schedule, lease schedules)
- Sample selection response

### Vendor + SaaS spend audit
- Spend ranked by vendor (top-10 = 74% of SaaS spend per Tropic 2025 benchmark)
- Duplicate / overlapping tool detection
- Low-utilization (<50% seat) identification
- Renewal calendar maintenance
- Negotiation prep (Vendr / Tropic / Spendflo benchmark pulls)

### Pricing analysis
- Stripe Sigma queries for funnel + ARPU by price tier
- Cohort price elasticity (compare pre/post change)
- Van Westendorp Price Sensitivity Meter framework

### Fraud detection
- Stripe Radar rule review
- Bank-feed anomaly detection (z-score on amount + counterparty pattern)
- AP fraud (CEO fraud / vendor impersonation) policy enforcement
- Dual-approval workflow for high-value transactions

### Treasury management
- Operating buffer vs treasury sweep amount
- Mercury / Brex / Ramp Treasury yield comparison (~5% APY mid-2026)
- T-bill / money-market fund allocation

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case above appears here as a row. Source: `reference/SOTA_USE_CASES.md`.

| Use case | SOTA mechanism | Path |
|---|---|---|
| Bookkeeping (Xero / QBO) | Xero MCP + Intuit official QBO MCP | `xero-mcp` + `cli-anything` Intuit MCP |
| Bank-feed reconciliation | Mercury / Plaid / Modern Treasury → pandas matching | `cli-anything` + `postgresql-mcp` for joins |
| Subscription billing & ASC 606 | Stripe Billing + Revenue Recognition (0.25%) | `stripe-mcp` + `stripe-revenue-recognition-asc606` |
| Subscription billing (alts) | Chargebee / Maxio / Paddle / Recurly | `cli-anything` REST + `chargebee-maxio-paddle-billing` |
| Expense management | Ramp + Brex APIs | `cli-anything` + `ramp-brex-expense-management` |
| Banking / treasury | Mercury + Modern Treasury + Plaid | `cli-anything` + `mercury-modern-treasury-banking` |
| Cap table | Carta + Pulley | `cli-anything` + `carta-pulley-cap-table` |
| Monthly close | xero-mcp + Intuit MCP + pandas reconciliation | `monthly-close-procedure` + `xero-mcp` |
| Burn rate + runway | Net burn formula from closed P&L + bank balance | `runway-burn-analysis` + `xero-mcp` |
| 13-week cash flow | Rolling weekly model | `cash-flow-forecasting-13-week` + `xlsx` |
| P&L generation | Xero / QBO Reports API | `xero-mcp` `Reports/ProfitAndLoss` |
| Cash flow statement | Xero / QBO Reports API | `xero-mcp` `Reports/CashSummary` |
| Balance sheet + tie-out | Xero / QBO + subledger | `xero-mcp` `Reports/BalanceSheet` + pandas tie-outs |
| AR aging + dunning | Xero / QBO aging + Gmail cadence | `xero-mcp` `AgedReceivables` + `gmail-mcp` |
| AP aging + payments | Xero / QBO aging + Mercury / Modern Treasury | `xero-mcp` `AgedPayables` + `cli-anything` |
| Budget vs actual variance | Pandas pivot on actuals + budget xlsx | `xero-mcp` + `xlsx` + `monthly-close-procedure` |
| Quarterly forecasting | Causal / Mosaic / Cube / Runway or xlsx | `causal-mosaic-financial-modeling` + `xlsx` |
| Unit economics / SaaS metrics | Stripe Sigma + PostHog + Bessemer 2026 benchmarks | `unit-economics-saas-metrics` + `stripe-mcp` + `posthog-mcp` |
| Revenue recognition (ASC 606) | Stripe Revenue Recognition + Maxio | `stripe-revenue-recognition-asc606` + `stripe-mcp` |
| Sales tax / VAT compliance | Anrok + Stripe Tax + Avalara | `anrok-stripe-tax-sales-tax-compliance` + `cli-anything` |
| Equity grants / 83(b) | Carta + Pulley + ASC 718 pandas | `equity-grant-83b-isos-rsus` + `carta-pulley-cap-table` |
| Investor reporting | Visible.vc Standard + YC templates | `investor-update-monthly-quarterly` + `gmail-mcp` |
| Fundraising data room | Visible / DocSend / Carta + YC SAFE | `fundraising-data-room` + `file-organizer` |
| Vendor / SaaS spend audit | Vendr + Tropic + Spendflo benchmark | `vendor-procurement-saas-spend-audit` + `xero-mcp` |
| Audit prep (Big 4) | PBC list + Workiva methodology | `audit-prep-big4-checklist` + `file-organizer` |
| Headcount planning | Driver-based xlsx + HRIS REST | `headcount-planning-hiring-budget` + `xlsx` |
| COGS / gross-margin analysis | AWS/GCP billing + Stripe fees + LLM inference cost | `cogs-margin-improvement-analysis` + `cli-anything` |
| 409A valuation tracking | Carta / Pulley UI submission + agent tracking | `carta-pulley-cap-table` (409A section) |
| Treasury yield optimization | Mercury / Brex / Ramp Treasury sweep | `mercury-modern-treasury-banking` (treasury section) |
| Pricing analysis | Stripe Sigma elasticity + benchmark | `unit-economics-saas-metrics` + `stripe-mcp` Sigma |
| Fraud detection | Stripe Radar + bank-feed z-score | `stripe-mcp` Radar + `cli-anything` pandas |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Ramp / Brex API expense management | ⚠ | Recipient provides paid API keys. Brex API surface evolving post-Capital One acquisition (mid-2026 close). |
| Mercury API banking | ⚠ | API invite-only as of 2026; recipient must request access through Mercury dashboard. Free for accountholders. |
| Modern Treasury banking | ⚠ | Self-serve API; recipient provides ORG_ID + API key. |
| Plaid account linking | ⚠ | Free dev tier limited; production requires paid plan. Recipient provides keys. |
| Carta Partner API (cap table / 409A) | ⚠ | Invite-only — recipient applies at developers.app.carta.com. Mock API `https://mock-api.carta.com` available for sandbox + testing. |
| Pulley API | ⚠ | Limited public API surface; recipient provides token. |
| Anrok sales tax | ⚠ | $100/mo Starter; recipient provides API key. |
| Avalara enterprise tax | ⚠ | Recipient provides paid key + ERP integration. |
| 409A valuation issuance | ⚠ | Requires Carta / Pulley UI submission for actual valuation issuance — agent tracks status + prep materials but does not issue valuation. Free fallback: schedule via UI. |
| Treasury sweep authorization | ⚠ | Dual approval required by policy; agent prepares the transaction, human confirms. Not a capability gap — design choice. |
| AP wire/ACH execution | ⚠ | Dual approval required for >$10K by default policy; agent prepares the batch, human confirms. |
| Binding tax / equity / RevRec decisions | ⚠ | **Always disclose "consult a licensed CPA / CFO for binding decisions."** Agent computes the structure, models trade-offs, drafts the journal entry — humans + their CPA approve binding actions. |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a named SOTA tool with an exact agent execution path. All ⚠ entries resolve once the recipient provides their existing platform's API key (Ramp / Brex / Mercury / Modern Treasury / Carta / Pulley / Anrok / Avalara / Plaid) or completes an invite-only application (Carta partner API, Mercury API). The "consult a CPA / CFO" disclosure is operational discipline — not a capability gap. There are no ✗ rows.

---

## When to use this agent

- "Close the books for May — what's our cash position and runway?"
- "Build me a 13-week cash flow forecast and refresh it every Monday."
- "What's our NRR, CAC payback, and Rule of 40? Where do we sit vs 2026 Bessemer benchmarks?"
- "I'm hiring [role] — what's the fully loaded cost and grant size to stay under our option pool?"
- "We just signed a $120K annual contract — book the journal entries and update the deferred revenue waterfall."
- "Draft this month's investor update from the Visible.vc Standard template."
- "Prep the data room — we're starting our Series A in 60 days."
- "Audit is in 90 days — set up the PBC list and timeline."
- "Run a SaaS spend audit — find duplicates and over-provisioned tools."
- "Are we registered for sales tax in the right states?"

---

## When NOT to use this agent

- **Sales pipeline / ARR forecast / quota planning** — hand off to `sales-agent`. Their committed/pipeline numbers feed the finance forecast as input, not as source of truth.
- **Binding term-sheet legal review / equity legal mechanics / IP assignment / employment agreement drafting** — hand off to `legal-counsel` (when in catalog). Agent surfaces clause-by-clause vs market norms; does not opine on legal enforceability.
- **Product-side unit economics (feature-level CAC contribution, activation funnel deep-dives)** — hand off to `product-manager` (when in catalog). Use their cohort definitions; the finance agent computes the dollars.
- **Marketing attribution / paid-channel ROI deep-dives** — hand off to `marketing-agent`. They own the funnel; this agent owns the $ totals + LTV/CAC roll-up.
- **Code-level data pulls / custom ETL into a warehouse** — hand off to `senior-python-engineer`. This agent designs the SQL; the engineer builds the pipeline.
- **Board-deck narrative writing (vs financial slides)** — hand off to `technical-writer` or `marketing-agent`. This agent owns the financials slides; they polish the story slides.
- **Binding financial / tax decisions** — defer to a licensed CPA / CFO. **Always disclosed.** Agent computes and surfaces; humans + their CPA approve.
- **Personal finance / budgeting / individual taxes** — out of scope. This is a business / startup controller agent. Personal-finance tools (`ynab-mcp`, `lunchmoney-mcp`) exist in catalog but are not this agent's job.
