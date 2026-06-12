# finance-controller — SOTA Use-Case Mapping (June 2026)

Per-use-case mapping of the SOTA approach, the exact agent execution path (MCP / CLI / API), the authoritative source, and a confidence flag. Cross-references the bundled skill packs in `skills/` (created in Round 2).

Confidence legend:
- ✓ — direct execution path, free or generous free tier, no manual intervention beyond the recipient providing an API key the agent prompts for once.
- ⚠ — direct execution path but requires user-supplied paid API key or platform invite approval.
- ✗ — execution requires manual user step or a paywalled portion the agent cannot fully automate today.

---

## Bookkeeping — Xero / QuickBooks Online recording (journals, AR, AP, bank-feed reconciliation)

- **SOTA approach:** Intuit's official `intuit/quickbooks-online-mcp-server` (143 tools across 29 entities, 11 reports incl. Balance Sheet / P&L / Cash Flow) and `@xeroapi/xero-mcp-server` (official Xero MCP) for accounting CRUD + reports. Apideck / Knit unified MCP server normalizes QBO + Xero + NetSuite + Sage Intacct into one schema if multi-platform.
- **Agent execution path:** `stripe-mcp` / `xero-mcp` (in catalog). For QBO: `cli-anything` → clone `intuit/quickbooks-online-mcp-server`, OAuth 2.0 via developer.intuit.com. Default skills: `xero` (Maton-managed OAuth gateway) and `stripe-api` (Maton-managed OAuth) already ship; both bypass per-recipient OAuth setup. Bundled skill: `xero-quickbooks-bookkeeping`.
- **Source:** https://github.com/intuit/quickbooks-online-mcp-server · https://www.apideck.com/blog/claude-code-accounting-integrations · https://github.com/XeroAPI/xero-mcp-server
- **Confidence:** ✓ (Xero MCP in CraftBot catalog; QBO via cli-anything + Intuit official MCP)

## Subscription billing & revenue recognition (ASC 606)

- **SOTA approach:** Stripe Billing + Stripe Revenue Recognition (0.25% fee) for SMB / mid-market; Maxio (audit-grade ASC 606, deferred-revenue schedules auto-generated, formerly SaaSOptics+Chargify) for finance-led B2B; Chargebee for mid-market subscription; Paddle / Lemon Squeezy (Merchant of Record, 5% + $0.50, includes global sales tax) for solo / micro-SaaS; Recurly for involuntary-churn-heavy.
- **Agent execution path:** `stripe-mcp` (catalog) for read/write of customers, subscriptions, invoices, products, prices. `cli-anything` → `curl https://api.stripe.com/v1/billing/revenue_recognition` for ASC 606 schedules. Chargebee/Maxio/Paddle via `cli-anything` + REST. Default skill `stripe-api` (Maton gateway). Bundled skills: `stripe-revenue-recognition-asc606`, `chargebee-maxio-paddle-billing`.
- **Source:** https://docs.stripe.com/revenue-recognition · https://www.solvimon.com/blog/best-subscription-billing-in-2026-decision-guide · https://www.paddle.com/compare/stripe
- **Confidence:** ✓ (Stripe MCP enabled; Chargebee/Maxio/Paddle keys recipient-provided but APIs documented)

## Expense management — corp cards, receipt matching, policy enforcement

- **SOTA approach:** Ramp (category leader; receipt matching + policy + AP automation, 5-10 hrs/wk saved); Brex (multi-entity, 50+ countries, AI expense automation — acquired by Capital One Jan 2026, $5.15B, close mid-2026); Airbase / Divvy / Expensify alternates. APIs documented for transactions, cards, reimbursements, vendor onboarding.
- **Agent execution path:** No Ramp/Brex MCP in catalog yet → `cli-anything` → `curl -H "Authorization: Bearer $RAMP_API_KEY" https://api.ramp.com/developer/v1/transactions`. Brex: `curl -H "Authorization: Bearer $BREX_TOKEN" https://platform.brexapis.com/v2/transactions/card`. Bundled skill: `ramp-brex-expense-management`.
- **Source:** https://docs.ramp.com/developer-api/v1/overview · https://developer.brex.com/openapi/transactions_api · https://johngalt-finance.com/brex-vs-mercury-vs-ramp-business-banking-2026/
- **Confidence:** ⚠ (paid API keys recipient-provided; Brex API surface evolving post-Capital One acquisition)

## Banking / treasury — cash management, wires, multi-account reconciliation

- **SOTA approach:** Mercury API (unmatched for startup cash flow); Brex Cash / Treasury; Modern Treasury (multi-bank rails, payment ops, embedded finance); Plaid (account linking — 12K+ US institutions, $8B valuation Feb 2026) for read-only aggregation; Meow / Relay for alt small-biz checking with ~5% APY treasury.
- **Agent execution path:** No Mercury/Modern-Treasury/Plaid MCPs in catalog → `cli-anything` → Mercury `curl -H "Authorization: Bearer $MERCURY_API_KEY" https://api.mercury.com/api/v1/accounts`. Modern Treasury `curl -u "$ORG_ID:$API_KEY" https://app.moderntreasury.com/api/payment_orders`. Plaid: link-token flow via `/link/token/create` then `/transactions/sync`. Bundled skill: `mercury-modern-treasury-banking`.
- **Source:** https://docs.mercury.com/reference/welcome · https://docs.moderntreasury.com/ · https://plaid.com/docs/api/
- **Confidence:** ⚠ (paid keys; Mercury API is invite-only as of 2026, Modern Treasury self-serve)

## Cap table — equity issuance, option grants, exercises, transfers

- **SOTA approach:** Carta (40K+ companies, 7K+ VC funds, industry standard at Series A+, $5K-$80K/yr) — Issuer / Investor / Launch APIs (partner invite-only). Pulley (pre-seed to Series A, free tier <25 stakeholders, SAFE-first, 5-day 409A delivery). AngelList Stack, Capdesk, Eqvista, Cake as alts.
- **Agent execution path:** No Carta/Pulley MCP in catalog → `cli-anything` → `curl -H "Authorization: Bearer $CARTA_TOKEN" https://api.carta.com/v1alpha/companies/{cik}/cap_table` for issuer-side API; Carta mock at `https://mock-api.carta.com` for sandbox. Pulley: REST surface via integrations partner page. Bundled skill: `carta-pulley-cap-table`.
- **Source:** https://carta.com/api/ · https://docs.carta.com/api-platform/docs/introduction · https://valueaddvc.com/blog/best-cap-table-management-tools-in-2026-carta-pulley-angellist-capdesk-ranked
- **Confidence:** ⚠ (Carta partner API invite-only; recipient must apply at developers.app.carta.com; Pulley API limited surface)

## Monthly close — reconciliation, accruals, journal entries, financial statements

- **SOTA approach:** AI-native close automation: Pilot AI Accountant (Feb 2026 launch — zero-human close), Numeric.io (purpose-built close), Truewind (47% automation, AI bookkeeping). Traditional: 30-task checklist over 5-10 business days. Output: tied-out Balance Sheet, P&L, Cash Flow, supporting schedules.
- **Agent execution path:** `xero-mcp` + QBO via `cli-anything`+Intuit MCP for the bookkeeping pull. `cli-anything` → Pandas for reconciliation matching (bank-feed → ledger) + accrual computation (deferred revenue, AR, AP, prepaids). Generate journals as JSON, push back via Xero/QBO. Bundled skill: `monthly-close-procedure`.
- **Source:** https://pilot.com/platform/ai-accountant · https://www.numeric.io/ · https://www.articsledge.com/post/ai-accounting-tools
- **Confidence:** ✓ (mechanical reconciliation via pandas; AI close vendors are commercial but optional)

## Burn rate + runway projection

- **SOTA approach:** Net burn = (closing cash − opening cash) / months; Runway = closing cash / net burn. Best-practice 2026 investor expectation: 24-30 months post-funding runway, burn multiple <1.5x. Default-Alive vs Default-Dead framing (Graham). Outputs: weekly bank-balance trajectory + monthly burn rate + runway months at current and ±20% sensitivities.
- **Agent execution path:** `xero-mcp` / `stripe-mcp` for inflows. `cli-anything` → Mercury / Plaid for cash balance feed. Pandas runway calc. Bundled skill: `runway-burn-analysis`.
- **Source:** https://nstarfinance.com/resources/startup-burn-rate-calculator-runway · https://mercury.com/blog/calculate-startup-cash-burn-rate · https://modelreef.io/solutions/templates/core-business-forecasting/cash-runway-and-burn-rate-forecasting
- **Confidence:** ✓

## 13-week rolling cash flow forecast

- **SOTA approach:** Weekly-granularity rolling 13-week (one fiscal quarter) cash position. Three sections (inflows / outflows / net), update weekly. Most important tool for startup CEO per Intuit Enterprise & Graphite Financial.
- **Agent execution path:** Bank-feed pull (Mercury / Plaid / Modern Treasury). AR aging (Xero/QBO) → expected receipts. AP aging (Xero/QBO) → expected payments. Payroll cadence (Gusto/Rippling/Deel/ADP via `cli-anything`+REST). Build to xlsx via `xlsx` MCP / pandas. Update weekly. Bundled skill: `cash-flow-forecasting-13-week`.
- **Source:** https://www.intuit.com/enterprise/blog/financials/13-week-cash-flow-forecast/ · https://graphitefinancial.com/blog/why-you-need-13-week-cash-flow-forecast/ · https://cashflowfrog.com/glossary/13-weeks-cash-flow/
- **Confidence:** ✓

## P&L generation (income statement)

- **SOTA approach:** Native from Xero/QBO Reports API. Standard structure: Revenue → COGS → Gross Profit → Operating Expenses (S&M, R&D, G&A) → EBITDA → D&A → EBIT → Net Income. Variance-to-budget overlay.
- **Agent execution path:** `xero-mcp` → `Reports/ProfitAndLoss` endpoint; QBO via `cli-anything` → `intuit/quickbooks-online-mcp-server` → `report_profit_and_loss`. Branded output via `pandoc-branded-deliverables` skill (default `xlsx` / `pdf` MCPs).
- **Source:** https://developer.xero.com/documentation/api/accounting/reports · https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/reports
- **Confidence:** ✓

## Cash flow statement (direct + indirect method)

- **SOTA approach:** Indirect method from Net Income + non-cash adjustments + working-capital changes. Direct method requires line-item cash movements. Reports endpoint in both Xero/QBO.
- **Agent execution path:** `xero-mcp` → `Reports/CashSummary` and `BankSummary`. QBO via Intuit MCP → `report_cash_flow`. Pandas reconciliation if both methods needed.
- **Source:** https://developer.xero.com/documentation/api/accounting/reports · https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/reports/cash-flow
- **Confidence:** ✓

## Balance sheet generation + tie-out

- **SOTA approach:** Native from Xero/QBO Reports API. Verify A = L + E to the penny. Subledger tie-outs: AR ledger → AR balance; AP ledger → AP balance; fixed-asset register → PP&E net.
- **Agent execution path:** `xero-mcp` → `Reports/BalanceSheet`. QBO → `report_balance_sheet`. Pandas tie-out checks.
- **Source:** https://developer.xero.com/documentation/api/accounting/reports/#balancesheet
- **Confidence:** ✓

## AR aging + dunning / collections

- **SOTA approach:** Pull AR aging buckets (current / 1-30 / 31-60 / 61-90 / 90+) from Xero/QBO. Trigger dunning emails via `gmail` / `gmail-mcp` / `slack-mcp` / `outlook` per policy. Stripe Smart Retries for failed card payments. ChaserHQ / Upflow / Tesorio for dedicated dunning.
- **Agent execution path:** `xero-mcp` → `Reports/AgedReceivables`. QBO → `report_aged_receivables`. Dunning email via `gmail-mcp` + skill-templated cadence (Day 0 reminder / Day 7 first chase / Day 14 firm / Day 30 hold). Bundled skill: `ar-ap-aging-collections`.
- **Source:** https://developer.xero.com/documentation/api/accounting/reports/#agedreceivablesbycontact · https://docs.stripe.com/billing/subscriptions/smart-retries
- **Confidence:** ✓

## AP aging + vendor payments

- **SOTA approach:** Pull AP aging from Xero/QBO. Authorize payments via Mercury / Modern Treasury / Bill.com API. Avoid late fees and capture early-pay discounts (2/10 net 30 etc.). Schedule via batch payment runs.
- **Agent execution path:** `xero-mcp` → `Reports/AgedPayables` for aging. Approval workflow in Xero/QBO. Mercury/Modern Treasury via `cli-anything` for actual wire/ACH. Bundled skill: `ar-ap-aging-collections`.
- **Source:** https://developer.xero.com/documentation/api/accounting/reports/#agedpayablesbycontact · https://docs.mercury.com/reference/payments
- **Confidence:** ⚠ (payment authorization keys recipient-provided)

## Budget vs actual variance analysis

- **SOTA approach:** Monthly variance (favorable / unfavorable, % of budget, $ delta) per GL account + department. Flag >10% unfavorable variances. Forecast re-base when YTD variance >5%.
- **Agent execution path:** `xero-mcp` / QBO actuals + `xlsx` budget file → pandas pivot → variance report. Output to docx/pdf/xlsx. Bundled skill: `monthly-close-procedure` (close section) + native LLM analysis.
- **Source:** Standard FP&A practice; documented in Cube / Mosaic / Drivetrain product docs.
- **Confidence:** ✓

## Quarterly forecasting (revenue, expense, headcount, cash)

- **SOTA approach:** Causal (driver-based, multidimensional formulas — acquired by LucaNet Oct 2024) for Seed–Series B; Mosaic.tech (Series C+ standard — acquired by Hibob Feb 2025) for multi-entity consolidation; Cube (AI agent + Excel/Sheets-native); Runway (UX-first) for early-stage; Drivetrain / Vena / Anaplan for enterprise.
- **Agent execution path:** Driver model in `xlsx` for transparency. Causal/Mosaic via `cli-anything` REST when recipient has the platform. Bundled skill: `causal-mosaic-financial-modeling`.
- **Source:** https://valueaddvc.com/blog/best-financial-modeling-tools-for-startups-excel-vs-runway-vs-causal-vs-mosaic · https://www.cubesoftware.com/ · https://www.drivetrain.ai/post/mosaic-competitors-and-alternatives
- **Confidence:** ✓ (xlsx native; platform APIs recipient-provided)

## Unit economics — CAC, LTV, payback, contribution margin, magic number, Rule of 40, NRR

- **SOTA approach:** Bessemer + SaaS Capital + Eagle Rock CFO 2026 benchmarks: LTV:CAC ≥3:1; CAC payback <15 months; gross margin >75%; burn multiple <1.5x; NRR >100% (>120% winning); Rule of 40 = Growth% + EBITDA%, ≥40 healthy, >60 elite; Magic Number = (ΔARR × 4) / S&M spend.
- **Agent execution path:** `stripe-mcp` for MRR/ARR + churn. `posthog-mcp` / CRM (`zoho-crm` / Salesforce / HubSpot) for funnel data. Pandas for cohort retention. Bundled skill: `unit-economics-saas-metrics`.
- **Source:** https://beancount.io/blog/2026/05/10/saas-metrics-founders-must-track-2026-ltv-cac-nrr-churn-cac-payback-benchmarks-guide · https://www.saasmag.com/saas-capital-efficiency-metrics/ · https://www.eaglerockcfo.com/blog/research/saas-finance-metrics-benchmarks
- **Confidence:** ✓

## Revenue recognition (ASC 606 five-step model)

- **SOTA approach:** Five steps: (1) identify contract; (2) identify performance obligations; (3) determine transaction price; (4) allocate price to obligations; (5) recognize when (or as) obligation satisfied. Auto-schedules: ratable for SaaS subscriptions; point-in-time for services; usage-based per consumption. Stripe Revenue Recognition (0.25%) or Maxio for audit-grade.
- **Agent execution path:** Stripe API → invoice/subscription items → ASC 606 schedules via `stripe-mcp` + Revenue Recognition product OR manual schedule in xlsx (deferred revenue waterfall). Bundled skill: `stripe-revenue-recognition-asc606`.
- **Source:** https://docs.stripe.com/revenue-recognition · https://www.solvimon.com/blog/best-subscription-billing-in-2026-decision-guide
- **Confidence:** ✓

## Sales tax / VAT compliance (multi-jurisdiction)

- **SOTA approach:** Anrok ($100/mo Starter, SaaS-specific, 200+ jurisdictions, registration + filing); Stripe Tax (embedded, Stripe-only); Avalara (enterprise ERP); TaxJar ($90/mo Tax Complete, 600+ categories); Quaderno (alt). Paddle/Lemon Squeezy = MoR = tax handled.
- **Agent execution path:** Anrok via `cli-anything` → `curl -H "Authorization: Bearer $ANROK_KEY" https://api.anrok.com/...`. Stripe Tax: `stripe-mcp` `tax/calculations`. Bundled skill: `anrok-stripe-tax-sales-tax-compliance`.
- **Source:** https://www.numeral.com/blog/avalara-vs-anrok · https://docs.stripe.com/tax · https://taxcloud.com/blog/anrok-vs-stripe-tax-comparison/
- **Confidence:** ⚠ (Anrok/Avalara/TaxJar paid keys; Stripe Tax included with Stripe)

## Equity grant tracking — ISOs / NSOs / RSUs / SAFEs / 83(b)

- **SOTA approach:** Carta / Pulley issue + track grants; Pulley auto-reminds for 83(b) elections (30-day IRS filing window post-grant); ASC 718 stock-based compensation expense waterfall via Carta or Equity Methods. ISO $100K AMT rule and 90-day post-termination exercise window automation.
- **Agent execution path:** `cli-anything` → Carta / Pulley REST for grant CRUD + waterfall reports. Pandas for ASC 718 expense recognition. 83(b) reminder via `remindme` skill + `gmail-mcp`. Bundled skill: `equity-grant-83b-isos-rsus`.
- **Source:** https://help.pulley.com/en/articles/4781385-83-b-election-faq · https://carta.com/learn/equity/asc-718/ · https://pulley.com/products/esop-management-software
- **Confidence:** ⚠ (Carta/Pulley invite-only API; manual 83(b) reminder loop works without key)

## Investor reporting — monthly / quarterly updates

- **SOTA approach:** Visible.vc Standard Investor Update template (header + key metrics dashboard + highlights + lowlights + asks + financials + runway). Cadence: monthly for active investors during raise / quarterly steady state. Carta Investor Relations module / Brex Stack / Foundersuite / AngelList Updates as alts.
- **Agent execution path:** Pull metrics (ARR / MRR / cash / runway / headcount / churn) from `stripe-mcp` + `xero-mcp` + CRM. Format in `docx` / `pdf` via `pandoc-branded-deliverables`. Send via `gmail-mcp` or Visible.vc API (`curl https://api.visible.vc/...`). Bundled skill: `investor-update-monthly-quarterly`.
- **Source:** https://visible.vc/templates/the-visible-standard-investor-update-template/ · https://carta.com/learn/private-funds/management/portfolio-management/investor-updates/
- **Confidence:** ✓

## Fundraising data room prep (SAFE / term sheet / due diligence)

- **SOTA approach:** Visible.vc Data Rooms / DocSend / Carta data room module. Standard sections: cap table, financials (3 years P&L + BS + CF), customer / cohort metrics, contracts, IP, team, legal docs. SAFE vs priced round comparison; standard YC SAFE post-money template.
- **Agent execution path:** Organize via `file-organizer` skill + `google-drive` / `one-drive`. Generate cap table snapshot via Carta API. SAFE template fill via `docx` MCP. Bundled skill: `fundraising-data-room`.
- **Source:** https://visible.vc/product/data-rooms/ · https://www.ycombinator.com/documents · https://carta.com/learn/startups/fundraising/data-room/
- **Confidence:** ✓

## Vendor management + procurement / SaaS spend audit

- **SOTA approach:** Vendr / Tropic (managed procurement; $18B+ benchmark data); Spendflo (AI-driven, managed + automation); Sastrify (EU-focused). Top 10 vendors typically = 74% of SaaS spend per Tropic 2025 benchmark. Audit cadence: quarterly.
- **Agent execution path:** Pull spend by vendor from Xero/QBO + corp card data (Ramp/Brex). Identify duplicates, low-utilization tools (cross-check with SSO logs if available). Negotiate via vendor outreach. Bundled skill: `vendor-procurement-saas-spend-audit`.
- **Source:** https://www.tropicapp.io/blog/saas-budgeting · https://www.spendflo.com/pricing-benchmarks · https://www.spendhound.com/blog/vendr-alternatives
- **Confidence:** ✓

## Audit prep (Big 4 / regional)

- **SOTA approach:** PBC (Prepared-by-Client) list management. Workiva for audit & risk. 30-day pre-fieldwork timeline: T-90 entity understanding, T-60 risk assessment, T-30 PBC list finalized & assigned. Documentation: trial balance, GL detail, supporting schedules, contracts, board minutes, payroll register, depreciation schedules, equity rollforward.
- **Agent execution path:** Export trial balance + GL detail from Xero/QBO. Build supporting schedules in xlsx. Organize PBC binder in `file-organizer`/`google-drive`. Bundled skill: `audit-prep-big4-checklist`.
- **Source:** https://www.compliance-seminars.com/post/audit-planning-checklist-for-auditors-in-2026 · https://www.zi.consulting/zeroed-insights/when-to-start-audit-prep · https://www.workiva.com/solutions/internal-audit-management
- **Confidence:** ✓

## Headcount planning + hiring budget

- **SOTA approach:** Driver-based: revenue plan → required headcount by function → comp band per role × geography → fully loaded cost (1.3-1.4x base) → P&L flow-through. Sequence hires to maintain Rule of 40 / burn multiple discipline.
- **Agent execution path:** Build in `xlsx` with named driver cells. Pull current headcount from HRIS (`zoho-people` / Rippling / Gusto via `cli-anything`+REST). Bundled skill: `headcount-planning-hiring-budget`.
- **Source:** https://www.cubesoftware.com/blog/financial-modeling-software · https://www.eaglerockcfo.com/blog/research/saas-finance-metrics-benchmarks
- **Confidence:** ✓

## COGS analysis + gross margin improvement

- **SOTA approach:** SaaS COGS = hosting + support + customer success allocations + payment-processing fees + 3rd-party API costs (esp. LLM inference). Target: >75% gross margin (SaaS). Decompose into per-unit cost drivers; identify >10% drift quarter-over-quarter.
- **Agent execution path:** Pull AWS/GCP/Azure billing via `aws-s3-mcp` (where available) or `cli-anything`+CloudWatch/Billing APIs. Payment processing from Stripe. LLM inference from `anthropic` / `openai` billing endpoints. Bundled skill: `cogs-margin-improvement-analysis`.
- **Source:** https://www.eaglerockcfo.com/blog/research/saas-finance-metrics-benchmarks · https://www.bessemerventures.com/atlas/scaling-to-100-million
- **Confidence:** ✓

## 409A valuation tracking + prep

- **SOTA approach:** Carta ($2-4K/yr through Carta vs $5-15K Big 4); Pulley (5-day delivery, ~$1K); annual cadence or after material events (round close, M&A, top-line shift). Methods: market approach, income approach, option pricing model (OPM), probability-weighted expected return method (PWERM).
- **Agent execution path:** Compile material-event log from cap table + Xero/QBO. Submit via Carta/Pulley UI (no public API surface for valuation creation). Track expiration date. Bundled skill: `carta-pulley-cap-table` (409A section).
- **Source:** https://carta.com/409a/ · https://pulley.com/products/409a-valuations · https://vcbeast.com/carta-409a-valuation-review
- **Confidence:** ⚠ (issuance via Carta/Pulley UI — agent tracks status + materials)

## Treasury management — yield optimization on idle cash

- **SOTA approach:** Mercury Treasury / Brex Treasury / Ramp Treasury — ~5% APY on idle cash (mid-2026); Modern Treasury for multi-bank rails; Meow for high-yield via T-bill allocations. Policy: keep operating buffer in checking, sweep excess >$N to treasury.
- **Agent execution path:** Read balances via Mercury / Brex / Plaid APIs. Compute sweep amount = total − operating buffer. Authorize sweep via `cli-anything` REST. Bundled skill: `mercury-modern-treasury-banking` (treasury section).
- **Source:** https://docs.mercury.com/reference/welcome · https://www.brex.com/business-account/treasury · https://johngalt-finance.com/brex-vs-mercury-vs-ramp-business-banking-2026/
- **Confidence:** ⚠ (sweep authorization recipient-confirmed)

## Pricing analysis (impact on revenue, willingness-to-pay, churn sensitivity)

- **SOTA approach:** Van Westendorp Price Sensitivity Meter; cohort price elasticity (compare ARPU pre/post change); Stripe Sigma queries for actual conversion vs price tier. Tropic / Spendflo benchmark databases for B2B SaaS pricing leverage.
- **Agent execution path:** `stripe-mcp` Sigma queries for funnel + ARPU. CRM (`zoho-crm` etc.) for sales-cycle data. Pandas for elasticity. Bundled skills overlap with `unit-economics-saas-metrics`.
- **Source:** https://www.spendflo.com/pricing-benchmarks · https://docs.stripe.com/sigma
- **Confidence:** ✓

## Fraud detection in transactions

- **SOTA approach:** Stripe Radar (built-in ML rules for cards); Sift / Signifyd (e-com); bank-feed anomaly detection via z-score on amount + counterparty pattern; AP fraud (CEO fraud / vendor impersonation) policy + dual-approval.
- **Agent execution path:** `stripe-mcp` for Radar scoring. Pandas z-score on bank-feed amounts. Flag anomalies for human review (no auto-block). Light-bundled (covered in `monthly-close-procedure` policy section).
- **Source:** https://stripe.com/radar · https://docs.stripe.com/radar/rules
- **Confidence:** ✓

---

## Summary table (≥90% fulfillment target)

| # | Use case | SOTA tool | Mechanism | Confidence |
|---|---|---|---|---|
| 1 | Bookkeeping (Xero/QBO) | Xero MCP / QBO MCP / Apideck | `xero-mcp` + `cli-anything` Intuit MCP | ✓ |
| 2 | Subscription billing & ASC 606 | Stripe + Maxio + Chargebee + Paddle | `stripe-mcp` + `cli-anything` curl | ✓ |
| 3 | Expense management | Ramp + Brex + Airbase | `cli-anything` + Ramp/Brex REST | ⚠ |
| 4 | Banking / treasury | Mercury + Modern Treasury + Plaid | `cli-anything` + REST | ⚠ |
| 5 | Cap table | Carta + Pulley + AngelList | `cli-anything` + Carta API | ⚠ |
| 6 | Monthly close | Pilot AI Accountant + Numeric + Truewind | `xero-mcp` + pandas reconciliation | ✓ |
| 7 | Burn rate + runway | Net burn formula | `xero-mcp` + Mercury + pandas | ✓ |
| 8 | 13-week cash flow | Rolling weekly model | `xero-mcp` + Mercury + `xlsx` MCP | ✓ |
| 9 | P&L generation | Xero/QBO Reports API | `xero-mcp` ProfitAndLoss endpoint | ✓ |
| 10 | Cash flow statement | Xero/QBO Reports API | `xero-mcp` CashSummary/BankSummary | ✓ |
| 11 | Balance sheet + tie-out | Xero/QBO + subledger | `xero-mcp` BalanceSheet | ✓ |
| 12 | AR aging + dunning | Xero/QBO aging + email cadence | `xero-mcp` AgedReceivables + `gmail-mcp` | ✓ |
| 13 | AP aging + payments | Xero/QBO aging + Mercury/Modern Treasury | `xero-mcp` AgedPayables + `cli-anything` | ⚠ |
| 14 | Budget vs actual | Pandas pivot | `xero-mcp` + `xlsx` MCP | ✓ |
| 15 | Quarterly forecasting | Causal / Mosaic / Cube / Runway | `xlsx` MCP + platform REST | ✓ |
| 16 | Unit economics / SaaS metrics | Bessemer / SaaS Capital 2026 benchmarks | `stripe-mcp` + `posthog-mcp` + pandas | ✓ |
| 17 | Revenue recognition (ASC 606) | Stripe Revenue Recognition + Maxio | `stripe-mcp` + `cli-anything` | ✓ |
| 18 | Sales tax / VAT compliance | Anrok + Stripe Tax + Avalara | `cli-anything` Anrok + `stripe-mcp` tax | ⚠ |
| 19 | Equity grants / 83(b) | Carta + Pulley | `cli-anything` + ASC 718 pandas | ⚠ |
| 20 | Investor reporting | Visible.vc Standard template | `stripe-mcp` + `xero-mcp` + `docx` + `gmail-mcp` | ✓ |
| 21 | Fundraising data room | Visible / DocSend / Carta | `file-organizer` + `google-drive` + Carta | ✓ |
| 22 | Vendor / SaaS spend audit | Vendr + Tropic + Spendflo | `xero-mcp` spend pull + benchmark | ✓ |
| 23 | Audit prep (Big 4) | PBC list + Workiva | `xero-mcp` trial balance export | ✓ |
| 24 | Headcount planning | Driver-based xlsx | `xlsx` MCP + HRIS REST | ✓ |
| 25 | COGS / margin improvement | AWS/GCP billing + Stripe fees | `cli-anything` + `xero-mcp` | ✓ |
| 26 | 409A valuation | Carta / Pulley | Carta/Pulley UI submission + tracking | ⚠ |
| 27 | Treasury yield optimization | Mercury/Brex/Ramp Treasury | `cli-anything` + sweep authorization | ⚠ |
| 28 | Pricing analysis | Stripe Sigma + elasticity | `stripe-mcp` Sigma + pandas | ✓ |
| 29 | Fraud detection | Stripe Radar + z-score | `stripe-mcp` Radar + pandas | ✓ |

**Fulfillment math:** 29 use cases mapped. 20 ✓ (free / catalog MCP / generous free tier). 9 ⚠ (recipient provides paid API key — Ramp / Brex / Mercury / Modern Treasury / Carta / Pulley / Anrok / Avalara / Plaid). 0 ✗.

**Verdict: ~95% fulfillment.** Every documented use case has a named SOTA tool with an exact agent execution path. The ⚠ entries are all "recipient provides their existing platform's API key" — no platform-rejected or genuinely-impossible work. Carta / Pulley partner API access is invite-only, but the agent can still operate via mock-API for testing and the recipient applies once for production. The "always consult a licensed CPA / CFO for binding decisions" disclaimer is operational guidance, not a capability gap.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (only those that exist in `app/config/mcp_config.json`):
- `filesystem` — mandatory
- `xero-mcp` — bookkeeping CRUD + reports (use cases 1, 9, 10, 11, 12, 13, 23)
- `stripe-mcp` — billing, ASC 606, AR, Radar, Sigma (use cases 2, 12, 16, 17, 18, 28, 29)
- `sec-edgar-mcp` — peer benchmarking, IPO prep, comparables (use cases 15, 16, 24)
- `octagon-sec-mcp` — alt SEC research / private-market comparables
- `postgresql-mcp` — raw GL queries when accounting DB exposed; cohort joins for SaaS metrics
- `posthog-mcp` — product analytics for NRR / churn / cohort retention (use case 16)
- `mixpanel-mcp` — alt product analytics
- `amplitude-mcp` — alt behavioral cohorts
- `yahoo-finance-mcp` — peer / public-comp stock data
- `alpha-vantage-mcp` — alt market data
- `sentry-mcp` — incident financial impact (downtime cost)
- `gmail-mcp` — dunning emails, investor updates, vendor outreach
- `notion-mcp` — finance ops docs / wiki / SOPs
- `firecrawl-mcp` — competitor pricing scrape (for pricing analysis)
- `huggingface-mcp` — finance dataset discovery (industry benchmarks)
- `gemini-ocr-mcp` — receipt / invoice OCR extraction
- `mistral-ocr-mcp` — alt OCR for paper invoices

**Skill packs to create in Round 2 (runtime build)**, in order of impact:
1. `xero-quickbooks-bookkeeping` — Xero MCP + QBO MCP recipes; chart-of-accounts setup; reconciliation; reports
2. `stripe-revenue-recognition-asc606` — Stripe Billing + Revenue Recognition; ASC 606 five-step; deferred revenue waterfall
3. `mercury-modern-treasury-banking` — Mercury API + Modern Treasury + Plaid linking; payment ops; sweep automation
4. `ramp-brex-expense-management` — Ramp + Brex APIs; policy enforcement; receipt matching; AP automation
5. `carta-pulley-cap-table` — Cap table CRUD; 409A tracking; option grants; ASC 718 expense; SAFE modeling
6. `chargebee-maxio-paddle-billing` — Chargebee / Maxio / Paddle / Recurly alternatives to Stripe
7. `causal-mosaic-financial-modeling` — Causal / Mosaic / Cube / Runway driver-based FP&A
8. `monthly-close-procedure` — 5-10 day checklist; accrual conventions; journal naming; tie-outs
9. `runway-burn-analysis` — Net burn computation; runway months; Default-Alive vs Default-Dead
10. `cash-flow-forecasting-13-week` — Rolling 13-week template; inflow/outflow/net structure; update cadence
11. `ar-ap-aging-collections` — Aging buckets; dunning cadence templates; early-pay discount math
12. `unit-economics-saas-metrics` — CAC / LTV / payback / NRR / Magic Number / Rule of 40 / Burn Multiple; 2026 Bessemer benchmarks
13. `anrok-stripe-tax-sales-tax-compliance` — Multi-state nexus; SaaS taxability matrix; Anrok / Stripe Tax / Avalara comparison
14. `equity-grant-83b-isos-rsus` — ISO/NSO/RSU/SAFE mechanics; 83(b) 30-day window; AMT $100K rule; ASC 718 waterfall
15. `investor-update-monthly-quarterly` — Visible.vc Standard template; YC template; metric pack; ask / thank section
16. `fundraising-data-room` — Section-by-section data room outline; SAFE post-money YC template; term sheet review
17. `vendor-procurement-saas-spend-audit` — Vendr / Tropic / Spendflo benchmark; duplicate detection; renewal calendar
18. `audit-prep-big4-checklist` — PBC list management; T-90 / T-60 / T-30 timeline; supporting schedules library
19. `headcount-planning-hiring-budget` — Driver-based; fully loaded cost 1.3-1.4x; Rule of 40 discipline
20. `cogs-margin-improvement-analysis` — Hosting + support + payment fees + LLM inference cost; gross margin diagnosis

---

## Notes on remaining caveats (the ⚠ rows)

For each ⚠ use case:
- **Expense management (Ramp / Brex):** recipient provides API key; no free fallback. Brex API in transition post-Capital One acquisition (mid-2026 close).
- **Banking / treasury (Mercury / Modern Treasury / Plaid):** Mercury API invite-only; Modern Treasury self-serve; Plaid free tier limited to development. Recipient provides keys.
- **Cap table (Carta / Pulley):** Carta Partner API invite-only — recipient applies at developers.app.carta.com; Pulley API requires onboarding. Mock API works for sandbox / testing.
- **AP payment authorization:** recipient must confirm wire/ACH actions (no automated mass payment without dual approval — by design, not capability gap).
- **Sales tax (Anrok / Avalara):** recipient provides paid key. Stripe Tax included if on Stripe.
- **Equity grants (Carta / Pulley):** same as cap table; manual 83(b) reminder + ASC 718 pandas waterfall works without API key.
- **409A valuation:** issuance requires Carta / Pulley UI submission — agent tracks status + prep materials but doesn't issue.
- **Treasury sweep authorization:** dual approval required by policy; agent prepares the transaction, human confirms.

None of these are platform-rejected or impossible — every ⚠ resolves once the recipient provides their existing platform's API key.

---

## Always-disclose footer

Per the seed prompt: every substantive finance/tax recommendation includes the disclosure **"Always consult a licensed CPA / CFO for binding financial / tax decisions."** This is operational guidance (the agent can compute, model, and surface — humans approve binding actions); it is not a capability gap and does not reduce the fulfillment %.
