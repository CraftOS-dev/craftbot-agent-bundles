# Finance Controller — Sources

Section-to-source map for `soul.md` and `role.md`. This file ships in the bundle but is **not** loaded into the agent's context — it exists for humans verifying provenance and for future refreshes.

The per-use-case SOTA mapping with confidence flags is at `reference/SOTA_USE_CASES.md`. URLs in `agent.yaml → sources` and the per-tool table below.

The v1 build did not download upstream agent reference files into `reference/agents/` (no dedicated `finance-controller` / `cfo` / `controller` v0 agent exists in the four public catalogs as of the build date — see `reference/INVENTORY.md`). The composition synthesizes finance practitioner conventions (Controller mantra, ASC 606 five-step, Bessemer SaaS benchmarks, 13-week rolling cash forecast methodology, Y Combinator post-money SAFE, Visible.vc Standard investor update, Big 4 PBC list management) and grounds every claim in the cited URLs below.

---

## soul.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Title + persona intro | Composition: Controller / fractional-CFO role conventions (Beancount.io 2026 SaaS Metrics Stack; Eagle Rock CFO benchmarks); seed prompt convictions | "Reconcile weekly, close monthly" is a long-standing Controller mantra; "cash is the only number" is PG / Mercury convention |
| Purpose | Composition: hand-off rules from seed prompt + sibling agents (`sales-agent`, future `legal-counsel`, future `product-manager`) | Always-disclose footer per seed prompt requirement |
| Execution stack | `reference/SOTA_USE_CASES.md` | Built from per-use-case SOTA research; mirrors the 20 bundled skill packs |
| When invoked — Monthly close | Composition synthesizing pilot.com, numeric.io, articsledge.com, intuit Enterprise close-checklist documentation | 5-10 day close convention from CPA practice |
| When invoked — 13-week cash forecast | Intuit Enterprise blog · Graphite Financial · Cash Flow Frog · ModelReef.io | Methodology fully cited |
| When invoked — Runway / burn | Mercury blog · Northstar Financial · ModelReef | Net burn = (opening − closing) / months; Default Alive from PG |
| When invoked — Unit economics | Beancount.io · SaaSMag · Eagle Rock CFO · uplifitgtm.com · wallstreetprep.com | Rule of 40 = Brad Feld; all 2026 benchmarks cited |
| When invoked — Investor update | Visible.vc Standard template · YC investor update template · Carta blog | Mandatory asks + lowlights from Visible convention |
| When invoked — Cap table / 409A / equity grant | Carta API docs · Pulley API · YC SAFE documents · Pulley 83(b) FAQ | Instrument types per US tax conventions |
| When invoked — Fundraising data room | Visible.vc Data Rooms · YC documents · Carta data room guide | Section checklist standard across sources |
| When invoked — Audit prep | Compliance Seminars · Workiva · Jadian.com (PBC list) · Zeroed-In Consulting | T-90 / T-60 / T-30 timeline from CPA practice |
| When invoked — Sales tax / VAT | TaxCloud · Numeral · Stripe Tax docs · Anrok docs | Nexus + taxability matrix per state |
| When invoked — AR / AP / collections | Composition synthesizing Xero/QBO aging convention + dunning cadence templates | Day 0 / 7 / 14 / 30 cadence from collection-agency practice |
| When invoked — FP&A | Causal · Mosaic · Cube · Drivetrain blog · Value Add VC | Driver-based per modern FP&A platforms |
| Core operating rules | Composition: Controller / CFO body of knowledge (CPA practice + Bessemer 2026 capital-efficiency posture + PG "Default Alive" + ASC 606 / ASC 718 disclosure norms) | "Always disclose" rule per seed prompt |
| Mode-specific decisions | Source-mapped per mode (same as When invoked rows) | Done-when definitions from CPA close-discipline |
| Quality gates | Composition synthesizing CPA tie-out convention + materiality threshold practice | Materiality = 5% pre-tax income (Big 4 default) |
| Output format | Composition: standard financial-deliverable conventions (Pandoc, xlsx, branded PDF) | $K/$M with one decimal — financial-statement norm |
| Communication style | Composition: lead-with-cash + conservative phrasing per Controller practice + Mercury / Bessemer 2026 posture | — |
| When to push back | Composition: ASC 606 / ASC 350 / ASC 985-20 / IRC 409A + 83(b) IRS guidance | Cited statutory/standard references |
| When to defer | Composition: hand-off matrix from seed prompt sibling agents | Always-disclose CPA / CFO per seed prompt |
| PROACTIVE self-init footer | `METHODOLOGY.md` standard pattern | Routine questions tailored to controller workflow (accounting platform, close cadence, fundraising/runway status) |
| Closing rule | Restatement of three load-bearing convictions from seed prompt | — |

---

## role.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Capability reference → Accounting platforms | GitHub intuit/quickbooks-online-mcp-server · Xero API docs · Apideck unified accounting · Knit unified MCP · NetSuite / Sage Intacct / Wave / FreshBooks docs | All platform docs cited |
| Capability reference → Billing / revenue platforms | Stripe docs · Chargebee docs · Maxio · Recurly · Paddle developer · Lemon Squeezy · Orb · Metronome | Solvimon comparison post 2026 |
| Capability reference → Banking / treasury platforms | Mercury docs · Brex developer · Ramp docs · Modern Treasury docs · Plaid docs · Meow / Relay marketing | Brex acquisition by Capital One Jan 2026 cited |
| Capability reference → Cap-table / equity platforms | Carta API · Pulley · AngelList Stack · Capdesk · Eqvista · Cake | Value Add VC 2026 ranking |
| Capability reference → FP&A platforms | Causal (LucaNet) · Mosaic (Hibob) · Cube · Runway · Drivetrain · Vena · Anaplan · Workday Adaptive · Jirav | Value Add VC + Cube + Drivetrain 2026 comparisons |
| Capability reference → Tax / compliance | Anrok · Stripe Tax · Avalara · TaxJar · Quaderno · Numeral | TaxCloud / Numeral comparison posts |
| Capability reference → Investor reporting platforms | Visible.vc · DocSend · Carta IR · Foundersuite · AngelList Updates | Visible.vc product pages |
| Capability reference → Audit / GRC | Workiva · Numeric.io · Pilot AI Accountant · Truewind | Pilot Feb 2026 launch + Truewind 47% automation claim |
| Capability reference → Procurement | Vendr · Tropic · Spendflo · Sastrify · SpendHound · Vertice · Zylo · Zluri · Torii · CloudEagle · Cledara | Tropic 2025 report + Spendflo + Vendr alts post |
| Capability reference → Equity research sources | SEC EDGAR docs · Octagon SEC · Yahoo Finance · Alpha Vantage · mcp-finance | All MCPs in CraftBot catalog |
| Monthly close playbook | Composition: pilot.com · numeric.io · articsledge.com · Intuit Enterprise close docs + CPA practice (accrual conventions, journal naming) | Standard CPA tie-out checklist |
| 13-week cash flow playbook | Intuit Enterprise blog · Graphite Financial · Cash Flow Frog · ModelReef | Three-section structure standard |
| Runway and burn analysis playbook | Mercury blog · Northstar Financial · ModelReef · IdeaProof startup runway calculator | Burn multiple convention from Bessemer/SaaS Capital |
| Unit economics playbook | Beancount.io · SaaSMag · Eagle Rock CFO · upliftgtm.com · wallstreetprep.com · designrevision.com SaaS benchmarks | All 2026 benchmarks cited |
| Cap table playbook | Carta API docs · Pulley · YC SAFE documents · Pulley 83(b) FAQ · Story.law cap-table guide · Value Add VC · Mercury Raise software stack | Standard instruments per US tax + securities law conventions |
| ASC 606 revenue recognition playbook | Stripe Revenue Recognition docs · FASB ASC 606 standard | Five-step model is FASB statutory |
| Equity grant playbook | Pulley 83(b) FAQ · Carta ASC 718 article · Pulley ESOP product · IRS 83(b) instructions | Statutory references |
| Audit prep playbook | Compliance Seminars 2026 audit checklist · Workiva audit & risk · Jadian.com PBC list · Zeroed-In Consulting startup audit readiness | T-90 / T-60 / T-30 timeline from Big 4 practice |
| Sales tax / VAT playbook | TaxCloud · Numeral Avalara comparison · Stripe Tax docs · Anrok docs · Avalara docs | Nexus + taxability matrix per state |
| Investor update playbook | Visible.vc Standard template · YC investor update template · Visible.vc How-to-write blog · Capboard | Mandatory asks + lowlights from Visible convention |
| Dunning email templates | Composition: standard collection-agency cadence (Day 0 / 7 / 14 / 30) | Templates synthesized from common B2B collection practice |
| Antipattern catalog | Composition: ASC 606 / ASC 350 / ASC 985-20 / IRC 409A / IRS 83(b) statutes + Bessemer / SaaS Capital posture + standard CPA practice | All antipatterns map to specific statutes or established norms |
| SOTA tool reference | Per-tool sources cited inline (table below) | One source per tool minimum |
| SOTA execution playbook table | Built from `reference/SOTA_USE_CASES.md` mapping | First-stop skill pack per user request type |
| Brief / output templates | Composition: standard close memo / 13-week cash forecast / investor update conventions | Synthesized formats |
| Closing rules | Restatement of three load-bearing convictions + hand-off matrix | — |

---

## SOTA tool sources (June 2026)

> One row per SOTA tool referenced in the agent.

| Tool | Source URL | Used for |
|---|---|---|
| Intuit QBO MCP Server (official) | https://github.com/intuit/quickbooks-online-mcp-server | `xero-quickbooks-bookkeeping` (QBO half) |
| Xero MCP Server (official) | https://github.com/XeroAPI/xero-mcp-server | `xero-quickbooks-bookkeeping` (Xero half) |
| Apideck unified accounting | https://www.apideck.com/blog/claude-code-accounting-integrations · https://www.apideck.com/mcp-server | Multi-platform normalization context |
| Knit unified accounting MCP | https://www.getknit.dev/blog/quickbooks-online-api-integration-guide-in-depth | Alt unified MCP |
| QBO API guide | https://developer.intuit.com/app/developer/qbo/docs/develop | OAuth 2.0 + endpoints |
| Xero API reference | https://developer.xero.com/documentation/api/accounting/ | Reports endpoints (P&L / BS / CF / aging) |
| Stripe Billing | https://docs.stripe.com/billing | `stripe-revenue-recognition-asc606`; `stripe-mcp` |
| Stripe Revenue Recognition | https://docs.stripe.com/revenue-recognition | ASC 606 waterfall; 0.25% fee |
| Stripe Tax | https://docs.stripe.com/tax | `anrok-stripe-tax-sales-tax-compliance` (Stripe half) |
| Stripe Sigma | https://docs.stripe.com/sigma | Unit economics queries |
| Stripe Radar | https://stripe.com/radar | Fraud detection |
| Solvimon — best subscription billing 2026 | https://www.solvimon.com/blog/best-subscription-billing-in-2026-decision-guide | Stripe vs Chargebee vs Maxio vs Recurly vs Paddle decision |
| Chargebee API docs | https://apidocs.chargebee.com/ | `chargebee-maxio-paddle-billing` |
| Maxio | https://www.maxio.com/ | `chargebee-maxio-paddle-billing` (audit-grade ASC 606) |
| Paddle developer | https://developer.paddle.com/ | MoR alternative |
| Lemon Squeezy | https://docs.lemonsqueezy.com/ | MoR alternative |
| Mercury API | https://docs.mercury.com/reference/welcome | `mercury-modern-treasury-banking` |
| Modern Treasury | https://docs.moderntreasury.com/ | `mercury-modern-treasury-banking` |
| Plaid API | https://plaid.com/docs/api/ | Bank account linking |
| Mercury blog — calculate burn rate | https://mercury.com/blog/calculate-startup-cash-burn-rate | `runway-burn-analysis` |
| Ramp Developer API | https://docs.ramp.com/developer-api/v1/overview | `ramp-brex-expense-management` |
| Brex Developer Platform | https://developer.brex.com/ | `ramp-brex-expense-management` |
| John Galt Finance — Brex vs Mercury vs Ramp 2026 | https://johngalt-finance.com/brex-vs-mercury-vs-ramp-business-banking-2026/ | Platform decision context |
| Carta API platform | https://carta.com/api/ | `carta-pulley-cap-table` |
| Carta API docs | https://docs.carta.com/api-platform/docs/introduction | Cap table endpoints |
| Carta — best cap table software 2026 | https://carta.com/best-cap-table-software/ | Platform decision context |
| Pulley ESOP product | https://pulley.com/products/esop-management-software | `equity-grant-83b-isos-rsus` |
| Pulley 83(b) FAQ | https://help.pulley.com/en/articles/4781385-83-b-election-faq | 83(b) 30-day window |
| Pulley 409A | https://pulley.com/products/409a-valuations | 409A tracking |
| Value Add VC — best cap table 2026 | https://valueaddvc.com/blog/best-cap-table-management-tools-in-2026-carta-pulley-angellist-capdesk-ranked | Carta vs Pulley vs AngelList vs Capdesk |
| Y Combinator standard docs | https://www.ycombinator.com/documents | YC post-money SAFE template |
| Causal | https://causal.app/ | `causal-mosaic-financial-modeling` |
| Mosaic.tech | https://www.mosaic.tech/ | `causal-mosaic-financial-modeling` |
| Cube | https://www.cubesoftware.com/ | `causal-mosaic-financial-modeling` |
| Drivetrain — Mosaic alternatives 2026 | https://www.drivetrain.ai/post/mosaic-competitors-and-alternatives | FP&A platform context |
| Value Add VC — financial modeling tools 2026 | https://valueaddvc.com/blog/best-financial-modeling-tools-for-startups-excel-vs-runway-vs-causal-vs-mosaic | FP&A decision matrix |
| Intuit Enterprise — 13-week cash flow | https://www.intuit.com/enterprise/blog/financials/13-week-cash-flow-forecast/ | `cash-flow-forecasting-13-week` methodology |
| Graphite Financial — 13-week cash flow template | https://graphitefinancial.com/blog/why-you-need-13-week-cash-flow-forecast/ | Template structure |
| ModelReef — cash runway forecasting | https://modelreef.io/resources/articles/cash-flow-forecasting/cash-runway-forecasting-calculate-runway-burn-and-funding-timing-correctly | Methodology |
| Northstar Financial — startup burn rate | https://nstarfinance.com/resources/startup-burn-rate-calculator-runway | Burn rate computation |
| Beancount.io — 2026 SaaS metrics stack | https://beancount.io/blog/2026/05/10/saas-metrics-founders-must-track-2026-ltv-cac-nrr-churn-cac-payback-benchmarks-guide | 2026 benchmarks |
| SaaSMag — SaaS capital efficiency 2026 | https://www.saasmag.com/saas-capital-efficiency-metrics/ | Burn multiple + NRR benchmarks |
| Eagle Rock CFO — SaaS benchmarks by stage 2026 | https://www.eaglerockcfo.com/blog/research/saas-finance-metrics-benchmarks | Stage-graded targets (Seed / A / B / C+) |
| Bessemer Cloud 100 / valuation framework | https://www.bessemerventures.com/atlas/scaling-to-100-million | Bessemer 2:1 growth-to-profit weighting |
| Anrok | https://anrok.com/ · https://taxcloud.com/blog/anrok-alternatives/ | `anrok-stripe-tax-sales-tax-compliance` |
| Numeral — Avalara vs Anrok | https://www.numeral.com/blog/avalara-vs-anrok | Tax platform decision |
| TaxCloud — Anrok vs Stripe Tax | https://taxcloud.com/blog/anrok-vs-stripe-tax-comparison/ | Stripe Tax decision context |
| Avalara | https://www.avalara.com/ | Enterprise tax platform reference |
| TaxJar | https://www.taxjar.com/blog/2026-sales-tax-software-comparison | Sales tax platform comparison |
| Visible.vc Standard Investor Update template | https://visible.vc/templates/the-visible-standard-investor-update-template/ | `investor-update-monthly-quarterly` |
| Visible.vc — how to write the perfect investor update | https://visible.vc/blog/how-to-write-the-perfect-investor-update/ | Update content guidance |
| Visible.vc — Data Rooms | https://visible.vc/product/data-rooms/ | `fundraising-data-room` |
| Capboard — investor update templates | https://www.capboard.io/en/investor-relations/best-investor-update-templates | Alt template reference |
| Carta — investor updates | https://carta.com/learn/private-funds/management/portfolio-management/investor-updates/ | Carta IR module reference |
| Pilot AI Accountant | https://pilot.com/platform/ai-accountant | AI-native close reference |
| Numeric.io | https://www.numeric.io/ | AI-native close reference |
| Truewind | https://accountingaitools.com/tools/truewind/ · https://www.truewind.ai/ | AI bookkeeping reference |
| Workiva — Audit & Risk | https://www.workiva.com/solutions/internal-audit-management | `audit-prep-big4-checklist` |
| Compliance Seminars — 2026 audit checklist | https://www.compliance-seminars.com/post/audit-planning-checklist-for-auditors-in-2026 | Audit timeline |
| Zeroed-In Consulting — startup audit readiness | https://www.zi.consulting/zeroed-insights/when-to-start-audit-prep | Startup-specific audit prep |
| Jadian — Audit PBC List | https://www.jadian.com/audit-pbc-list-explained/ | PBC list management |
| Tropic — SaaS Buying Trends 2025 | https://www.tropicapp.io/reports/software-spending-trends-2025 | Top-10 = 74% of spend benchmark |
| Tropic — SaaS budgeting | https://www.tropicapp.io/blog/saas-budgeting | Procurement context |
| Spendflo pricing benchmarks | https://www.spendflo.com/pricing-benchmarks | `vendor-procurement-saas-spend-audit` |
| SpendHound — Vendr alternatives 2026 | https://www.spendhound.com/blog/vendr-alternatives | Procurement platform context |
| OpenBankingTracker — Plaid alternatives 2026 | https://www.openbankingtracker.com/api-aggregators/plaid/alternatives | Banking aggregation alternatives |
| Carta — IPO readiness | https://carta.com/learn/startups/exit-strategies/ipo/readiness/ | Audit + diligence prep |
| Carta — ASC 718 | https://carta.com/learn/equity/asc-718/ | Stock-based comp expense |
| Wall Street Prep — Rule of 40 (Brad Feld) | https://www.wallstreetprep.com/knowledge/rule-of-40/ | Rule of 40 origin / formula |

---

## Notes on authored-from-synthesis

Sections that aren't directly lifted from a single source (these are operational glue, not domain claims):

- **Always-disclose footer** ("consult a licensed CPA / CFO for binding decisions") — operational discipline per the seed prompt, not a single citable source.
- **Dunning email templates** (Day 0 / 7 / 14 / 30) — synthesized from common B2B collection cadence. No single canonical source; the cadence is convention.
- **Journal-entry naming convention** (`YYYY-MM-DD | [CATEGORY] | Description | [REF]`) — synthesized from CPA practice; multiple conventions exist.
- **Close memo template** — synthesized from common CFO deliverable formats; not lifted from one source.
- **Antipattern catalog** — each individual antipattern grounds in a specific statute / ASC standard / IRS rule (ASC 606, ASC 350, ASC 985-20, IRC 409A, IRS 83(b) instructions), but the BAD / GOOD pairing format is editorial.
- **PROACTIVE.md self-init footer** — standard `METHODOLOGY.md` pattern, only the routine questions changed to match controller workflow.
- **Hand-off matrix to sibling agents** — seed-prompt-driven; `legal-counsel` and `product-manager` are forward references to agents not yet in the catalog as of build date.

The base claims (ASC 606 five-step, 83(b) 30-day window, ISO $100K AMT rule, Rule of 40 formula, NRR / CAC / LTV definitions, 13-week cash forecast structure, PBC list contents, Big 4 audit timeline) are all sourced to either statutory standards (FASB ASC, IRC, IRS instructions) or 2026 industry guides cited in the table above.

---

## How to update this agent

1. Re-fetch the SOTA tool source URLs listed above; check for API changes, new MCP servers, pricing changes, platform launches / acquisitions.
2. Update the per-tool SOTA tool reference in `role.md` if anything has changed materially.
3. Update `agent.yaml` `mcp_servers` if a new finance MCP enters the catalog (e.g., a future Carta MCP, Ramp MCP, Mercury MCP).
4. Update `reference/SOTA_USE_CASES.md` confidence ratings if a paid integration becomes free or vice versa.
5. Re-run `python verify.py finance-controller` to confirm structure intact.
6. Re-build: `python build.py finance-controller` produces a fresh `.craftbot`.

For the canonical reference repos (Step 2 of methodology), recheck quarterly:
- `wshobson/agents` (plugins/finance — none as of build date)
- `VoltAgent/awesome-claude-code-subagents` (categories/12-finance — none as of build date)
- `msitarzewski/agency-agents` (CFO / controller / bookkeeper — recheck)
- `JSONbored/claudepro-directory` — search for finance / controller / accountant skills

When SOTA changes materially (new model launch, API endpoint change, platform acquisition closes, new MCP enters CraftBot catalog), update the relevant bundled skill pack's `SKILL.md` first, then the SOTA tool source table here.
