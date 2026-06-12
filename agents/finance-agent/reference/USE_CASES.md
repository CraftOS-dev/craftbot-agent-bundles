# Finance Agent — Use Cases

**Tier:** general · **Category:** finance
**Core job:** Senior strategic finance / fractional CFO — capital allocation, fundraising strategy, term sheet review, FP&A long-range planning, M&A consideration, optimal capital structure, treasury yield, equity comp design, IPO readiness, board CFO package, investor relations strategy.

> Ships with the 2026 SOTA strategic-finance stack — Runway / Causal / Mosaic / Cube / Knolli for FP&A; NVCA Oct 2025 model + YC SAFE for fundraising; Carta / Pulley for 409A; Visible.vc / DocSend / Papermark for data rooms; Rho / Mercury Treasury / Public.com / Brex Yield for treasury; Damodaran 2026 datasets for capital allocation; Finsider for M&A QoE; MainStreet / Neo.tax for R&D credits; Big Beautiful Bill 2025 QSBS update; Stripe Atlas / Foothold America for international entity; Airwallex / Revolut Business / OANDA for FX hedging; Cross Country / Carta / EisnerAmper / Deloitte for IPO readiness. **PAIRS with `finance-controller`** (operational/tactical bookkeeping / monthly close / AR-AP / sales tax / audit prep) — does not replace it. **Always discloses "consult a licensed CFO / CPA / qualified investment advisor for binding strategic-finance decisions"** — humans approve binding actions; the agent models, surfaces trade-offs, and drafts deliverables.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### FP&A — long-range modeling + scenarios
- Three-statement financial model (P&L / BS / CF tied; driver-based)
- Driver-based revenue modeling (SaaS / e-com / marketplace; cohort × ACV × NRR)
- Scenario planning (base / bull / bear + sensitivity tornado + Monte Carlo)
- Customer LTV strategic analysis (bottom-up cohort by segment / channel)
- Segment unit economics (per-segment LTV / CAC / payback)
- Pricing strategy modeling (cohort price elasticity; Van Westendorp PSM)
- Market sizing (TAM / SAM / SOM — bottom-up + top-down triangulation, strategic-finance lens)

### Capital allocation + capital structure
- Capital allocation framework (Damodaran ROIC vs WACC ladder; reinvest / return / reserve)
- Optimal capital structure (stage-graded debt-equity mix; WACC; blended-stack 2026)
- Build-vs-buy-vs-partner-vs-license decision matrix (corporate development)

### Fundraising strategy + term sheet
- Fundraising strategy (priced equity vs SAFE vs venture debt vs RBF vs secondaries; capital-stack blend 2026)
- Term sheet review (NVCA Oct 2025 model; clause-by-clause vs market; 1x non-participating + broad-based WA standard)
- 409A valuation negotiation (OPM/PWERM hybrid; 12-25% discount range; refresh triggers)
- Pitch deck financial slides (6-metric max; growth → unit econ → path to profit; 2026 standard)
- Investor data room curation (8 sections; Visible.vc / DocSend / Papermark / Carta IR)

### Investor relations + board
- Board CFO financial package (10-slide Cube/Vena structure; T-28 prep; T-7 pre-wire)
- Investor update (CFO voice; Visible.vc Standard CFO variant; YC variant)
- Investor research + outreach (PitchBook / CB Insights / Crunchbase / Tracxn / SEC EDGAR comps)

### M&A + corp dev
- M&A target screen (5-criteria scorecard; Bain/McKinsey playbook)
- Due diligence (buy-side + sell-side QoE pre-work; Finsider 74-point GL scan)
- Corporate development playbook (build vs buy vs partner vs license — NPV/IRR/EV)
- Strategic partnership financial structuring (JV — EY/Ankura five-essentials; equity vs commercial)

### Treasury + banking strategy
- Treasury optimization (3-tier yield ladder — operating HYSA / reserve T-bill / strategic surplus)
- Multi-bank strategy (post-SVB; Mercury / Brex / Rho / Modern Treasury)
- FX risk hedging strategies (Wise / Airwallex / Revolut Business / OANDA; spot / forward / option)

### Tax strategy
- QSBS strategy (Big Beautiful Bill 2025 — $75M cap / $15M individual / tiered exclusion)
- R&D tax credit (MainStreet / Neo.tax / Haven; up to $500K/yr against payroll)
- Holding company structures (IP transfer / international / M&A optimization)
- Sales tax / VAT compliance strategy (pairs with `finance-controller`)

### International + transfer pricing
- International expansion finance structure (entity decision tree — Stripe Atlas / Foothold)
- Transfer pricing (arm's-length; intra-group agreements; CUP / Cost Plus / TNMM)

### Equity + compensation
- Equity compensation plan design (10-20% initial pool; 3-5% annual evergreen; per-employee evergreen rule)
- ISO / NSO / RSU mix per stage and role
- Refresh strategy (≥18-month tenure; significant role expansion)

### IPO + exit readiness
- IPO readiness scorecard (5-dimension: financial systems / governance / controls / human capital / MD&A)
- S-1 prep + comp analysis (SEC EDGAR for recent S-1s in sector)
- SPAC vs Direct Listing alternatives

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case above appears here as a row. Source: `reference/SOTA_USE_CASES.md`.

| Use case | SOTA mechanism | Path |
|---|---|---|
| Three-statement financial model | Runway / Causal / Mosaic / Cube / Knolli / Excel | `three-statement-financial-model-tied` + `xlsx` + `xero-mcp` + `cli-anything` |
| Driver-based revenue (SaaS / e-com / marketplace) | Stripe Sigma + PostHog cohorts | `driver-based-revenue-modeling` + `stripe-mcp` + `posthog-mcp` |
| Scenario + sensitivity + Monte Carlo | NumPy/SciPy + Causal native | `scenario-planning-monte-carlo` + `cli-anything` + `xlsx` |
| Capital allocation framework | Damodaran 2026 + ROIC vs WACC ladder | `capital-allocation-framework` + `xlsx` |
| Pricing strategy modeling | Stripe Sigma + cohort elasticity | `driver-based-revenue-modeling` + `stripe-mcp` + `posthog-mcp` |
| Customer LTV strategic (cohort) | lifelines + Stripe + PostHog | `ltv-cohort-strategic` + `cli-anything` + `stripe-mcp` |
| Segment unit economics | Stripe + xero + xlsx pivot | `ltv-cohort-strategic` + `stripe-mcp` + `xero-mcp` |
| Market sizing (TAM/SAM/SOM) | SEC EDGAR + PitchBook + bottom-up | `market-sizing-tam-sam-som-strategic` + `sec-edgar-mcp` + `firecrawl-mcp` |
| Fundraising strategy | NVCA + YC SAFE + RBF/venture debt matrix | `fundraising-strategy-priced-safe-venture-debt-rbf` + `cli-anything` |
| 409A valuation negotiation | OPM/PWERM hybrid; Carta/Pulley/Aranca | `409a-valuation-negotiation` + `cli-anything` + `xlsx` |
| Term sheet (NVCA-grade) review | NVCA Oct 2025 model + Cooley GO | `term-sheet-nvca-grade-review` + `cli-anything` + `docx` |
| Pitch deck financial slides | 6-metric max; path to profit 2026 | `pitch-deck-financial-slides` + `pptx` |
| Investor data room curation | Visible.vc / DocSend / Papermark | `investor-data-room-curation` + `file-organizer` + `cli-anything` |
| Board CFO financial package | Cube/Vena 10-slide structure | `board-cfo-financial-package` + `pptx` + `xlsx` |
| M&A target screen + QoE pre-work | Finsider + EisnerAmper + comps | `ma-target-screen-and-qoe` + `sec-edgar-mcp` + `cli-anything` |
| Corp dev (build/buy/partner/license) | NPV/IRR/EV matrix | `strategic-partnership-jv-structuring` + `xlsx` + `docx` |
| Strategic partnership / JV structuring | EY/Ankura five-essentials | `strategic-partnership-jv-structuring` + `xlsx` + `docx` |
| Treasury yield ladder | Rho / Public.com / Mercury Treasury / Brex Yield | `treasury-yield-ladder-risk-tier` + `cli-anything` + `yahoo-finance-mcp` |
| Multi-bank banking strategy (post-SVB) | Mercury + Brex + Rho + Modern Treasury | `treasury-yield-ladder-risk-tier` + `cli-anything` |
| Capital structure optimization | WACC + blended stack 2026 | `capital-structure-debt-equity-mix-stage` + `xlsx` |
| QSBS strategy (Big Beautiful Bill 2025) | Carta + Wilson Sonsini / Cooley guides | `tax-strategy-qsbs-rd-credit-holdco` + `cli-anything` + `docx` |
| R&D tax credit strategy | MainStreet + Neo.tax + Haven | `tax-strategy-qsbs-rd-credit-holdco` + `cli-anything` |
| Holding company structures | IP / international / M&A; counsel + CPA | `tax-strategy-qsbs-rd-credit-holdco` + `docx` |
| International entity + transfer pricing | Stripe Atlas + BaseFirma + Foothold America | `international-entity-transfer-pricing` + `cli-anything` + `docx` |
| FX risk hedging | Wise / Airwallex / Revolut Business / OANDA | `fx-hedging-strategies` + `cli-anything` + `xlsx` |
| IPO readiness / S-1 prep | Cross Country + Carta + EisnerAmper + Deloitte | `ipo-readiness-s1-prep` + `sec-edgar-mcp` + `xlsx` |
| SPAC / direct listing alts | Comp filings + framework matrix | `ipo-readiness-s1-prep` + `sec-edgar-mcp` + `docx` |
| Equity comp design (pool/evergreen) | First Round + Holloway + NASPP | `equity-comp-design-pool-evergreen` + `cli-anything` + `xlsx` |
| Investor update (CFO voice) | Visible.vc Standard CFO variant + YC | `investor-update-cfo-voice` + `cli-anything` + `docx` + `gmail-mcp` |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| 409A valuation issuance | ⚠ | Carta / Pulley / Aranca UI submission required for actual valuation issuance. Agent prepares OPM/PWERM tournament model, tracks status, drafts methodology memo. Free fallback: Carta in-house (included with cap-table sub) or Pulley 5-day $1K-$3.5K. **Defer binding 409A to licensed valuation firm.** |
| M&A target screen (PitchBook / CB Insights) | ⚠ | PitchBook ($15K+/yr) and CB Insights ($50K+/yr) paywalled. Free fallback: `sec-edgar-mcp` (public comps), Crunchbase free tier, AngelList Pro $2K/yr light alt. Recipient provides API key for paid tools. |
| Due diligence QoE attestation | ⚠ | Final QoE requires licensed CPA firm (EisnerAmper / Anders / BDO / RSM / regional). Agent does Finsider-style pre-work — 74-point GL anomaly scan, working capital normalization, tax exposure schedule. **Always disclose "consult licensed CPA for binding QoE."** |
| Mercury / Brex API access | ⚠ | Mercury API invite-only (free for accountholders). Brex API surface evolving through Capital One acquisition close mid-2026. Free fallback: dashboards for manual export; agent processes the exports. |
| Tax strategy binding sign-off | ⚠ | Final tax positions (QSBS / R&D / holdco) require licensed CPA / tax attorney. Agent models structure, surfaces eligibility scorecard, drafts memo. **Always disclose "consult licensed CPA / tax attorney."** |
| International entity + transfer pricing | ⚠ | Entity formation requires licensed counsel in each jurisdiction. Transfer pricing study requires licensed CPA / TP firm (BaseFirma / Valentiam / Big-4). Agent models intra-group flows, drafts intra-group agreements, identifies tax exposure. **Always disclose + defer to `legal-counsel` and licensed CPA.** |
| Term sheet binding sign-off | ⚠ | Agent surfaces clause-by-clause vs NVCA Oct 2025 model + market norms. **Defer binding sign-off to `legal-counsel`** — agent does not opine on enforceability. |
| Capital allocation / M&A / fundraising decisions | ⚠ | **Always disclose "consult a licensed CFO / CPA / qualified investment advisor for binding strategic-finance decisions."** Agent computes structure, models trade-offs, drafts the memo — humans + their professional advisors approve binding actions. |
| Investor research APIs (PitchBook / CB Insights / Tracxn / AngelList Pro) | ⚠ | Recipient provides paid API keys. Free fallback: `sec-edgar-mcp` (public-side), `firecrawl-mcp` for public industry summaries. |
| QSBS / R&D credit application | ⚠ | MainStreet / Neo.tax / Haven require recipient to connect payroll + accounting systems. Free fallback: agent drafts application + supporting docs; recipient submits via platform. |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a named SOTA tool with an exact agent execution path. All ⚠ entries resolve once the recipient provides their existing platform's API key (Carta / Pulley / PitchBook / CB Insights / Mercury / Brex / MainStreet / Neo.tax / Anrok / Avalara), engages a licensed professional (CPA / counsel / valuation firm), or completes an invite-only application (Mercury API, Carta partner API). The "consult a licensed CFO / CPA / qualified investment advisor" disclosure is operational discipline — not a capability gap. There are no ✗ rows.

---

## When to use this agent

- "Should we raise priced Series A or extension SAFE — model dilution + runway for both."
- "Review this term sheet clause-by-clause vs NVCA Oct 2025 standard."
- "Build a 3-statement model with base / bull / bear and Monte Carlo on runway-to-zero."
- "Where should we allocate the next $5M — sales hires, marketing, product, or runway buffer?"
- "Negotiate our 409A — what's the defensible preferred-to-common discount range?"
- "Curate our Series A data room — Visible.vc or DocSend?"
- "Screen 10 M&A targets in the developer-tools space — strategic fit + valuation + cultural fit."
- "Optimize our treasury — we have $15M idle and only Mercury HYSA."
- "Are we ready to start IPO prep? Score us on the 5-dimension readiness framework."
- "Design our option pool for Series B — what evergreen % do we plan, and how do we sequence refreshes?"
- "Should we use venture debt or RBF for the next $3M — we're at $5M ARR, capital-efficient."
- "QSBS strategy for the founders — eligibility check under Big Beautiful Bill 2025."
- "Expand to UK + DE — entity structure + transfer pricing recommendation."
- "Hedge our EUR exposure — we have €200K/mo net outflow committed for 12 months."

---

## When NOT to use this agent

- **Bookkeeping / monthly close / AR / AP / sales tax / audit prep / operational unit econ computation** — hand off to `finance-controller`. They own the books and the close; this agent uses their actuals as input. PAIR them on investor updates (controller drafts metric pack; this agent shapes CFO-voice narrative + asks).
- **Binding term-sheet legal sign-off / IP transfer / employment agreement drafting / entity formation legal mechanics / binding M&A docs** — hand off to `legal-counsel`. This agent surfaces clause-by-clause vs NVCA + market; counsel opines on enforceability.
- **Sales pipeline / ARR forecast / quota planning / committed-pipeline accuracy** — hand off to `sales-agent`. This agent uses their forecast as revenue input to FP&A.
- **Product-side cohort definitions / activation funnel / feature-level engagement** — hand off to `product-manager` (when in catalog). This agent computes the dollars; product owns the cohort definition.
- **Marketing attribution / paid-channel ROI deep-dive** — hand off to `marketing-agent`. They own funnel; this agent owns $ totals + LTV/CAC strategic interpretation.
- **Code-level data ETL / custom warehouse pipeline** — hand off to `senior-python-engineer`. This agent designs the SQL; they build the pipeline.
- **Board-deck narrative slides (vs financial slides) / vision / story polish** — hand off to `marketing-agent` or `technical-writer`. This agent owns financials slides + decision memos.
- **Personal finance / individual taxes / household budgeting** — out of scope. This is a strategic-finance / fractional-CFO agent for businesses and founders. Personal-finance tools (`ynab-mcp`, `lunchmoney-mcp`, `actual-budget-mcp`) exist in catalog but are not this agent's job.
- **Binding financial / tax / equity / M&A / fundraising / valuation decisions** — defer to a licensed CFO / CPA / counsel / qualified investment advisor / valuation firm. **Always disclosed.** This agent models, surfaces trade-offs, drafts deliverables; humans + their professional advisors approve binding actions.
