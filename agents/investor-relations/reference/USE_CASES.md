# Investor Relations — Use Cases

**Tier:** general · **Category:** executive
**Core job:** Senior IR operator — monthly/quarterly investor updates, earnings prep, equity-analyst relations, roadshow + NDR logistics, SEC filings drafting (10-K / 10-Q / 8-K / DEF 14A / S-1), IR website management, 13F shareholder tracking, shareholder Q&A maintenance, ESG-for-investors reporting (IFRS S1/S2 + GRI 2025 + SASB + TCFD), investor day / capital markets day, quiet-period management, embargoed-disclosure protocols, M&A investor comms, fund-of-funds + LP reporting, dividend / buyback / secondary announcements, IPO readiness on the IR side, and cap-table comms.

> Ships with the 2026 SOTA IR stack — Visible.vc / DocSend / Papermark / AngelList Updates / Carta IR for private-co updates + data rooms; Workiva + SEC EDGAR Next 2025 for SEC filings; Q4 Inc. + Notified for IR websites + earnings calls + investor day; AlphaSense + Sentieo + Tegus + Bloomberg Terminal + FactSet + Refinitiv + PitchBook + S&P Capital IQ for analyst research; ISS Voting Insights + Glass Lewis Proxy Paper + Diligent + Computershare / EQ for proxy + governance; Mention + Brandwatch + Talkwalker + Meltwater + Cision for media monitoring; IFRS S1/S2 + GRI 2025 + SASB + TCFD + CDP + MSCI ESG + Sustainalytics for ESG-for-investors; Whale Wisdom + 13F Info + SEC EDGAR XBRL for 13F shareholder tracking; ICR + FTI + Joele Frank + Sard Verbinnen + Kekst CNC for senior IR + M&A comms advisory; ILPA 3.0 + Allvue + Carta LP + Visible LP + Affinity for LP reporting; Notified + Business Wire + PR Newswire + Globe Newswire for press distribution. **PAIRS with `finance-agent`** (financial modeling, capital allocation, S-1 financials, term sheet, treasury, FX) — does not replace it. PAIRS with `ceo-agent` (board mgmt + CEO-voice narrative). **Always discloses "consult licensed securities counsel for binding SEC filings, Reg FD interpretation, and disclosure-law decisions"** — counsel + auditors approve binding actions; the agent drafts, runs the playbook, and curates the audience.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Private-company IR (investor updates + data rooms)

- Monthly investor update (Visible.vc Standard — TL;DR cash + runway / KPIs / highlights / lowlights / asks / financials)
- Quarterly board + investor letter (institutional cadence; OKR scorecard + KPIs + risks + asks)
- Annual shareholder letter (Buffett/Bezos/Dimon bar; 1500-3500 words; year + multi-year strategy + capital allocation)
- Cap-table communication to existing investors (post-round narrative; secondary mechanics; employee tender; cleanup)
- Investor data room curation (IR-side ongoing reference; Visible.vc / DocSend / Papermark; 8 sections)

### Public-company IR (filings + earnings + analyst + governance)

- Earnings call script + 50-150-question Q&A binder prep (AlphaSense / Sentieo / Tegus pattern mining)
- 10-K drafting (Workiva narrative sections; SEC EDGAR Next 2025; counsel hand-off)
- 10-Q drafting (streamlined; quarterly cadence)
- 8-K event reporting (4-business-day trigger; Item 1.01 / 2.02 / 5.02 / 7.01 / 8.01)
- Proxy statement (DEF 14A) drafting (CD&A + Summary Comp + Item 402(v) pay-versus-performance + ISS/Glass Lewis pre-engagement)
- Equity analyst relations (coverage matrix + 1-2x/Q 1:1s + post-earnings call-back roster + analyst note alerts)
- IR website management (Q4 Inc. / Notified CMS; monthly accessibility + uptime audit)
- Roadshow + non-deal roadshow (NDR) logistics (sell-side corporate access + briefing books with 13F snapshots)
- Quarterly earnings press release (Reg G recon + Safe Harbor + GAAP/non-GAAP)
- Guidance setting (FactSet / Refinitiv / AlphaSense consensus; range vs point; under-promise+over-deliver)
- 13F shareholder monitoring (Whale Wisdom / 13F Info / SEC EDGAR XBRL; monthly delta + new buyer/seller flag)
- Shareholder Q&A library maintenance (100-300 entries; per-topic; quarterly refresh)
- News + media monitoring (IR lens — analyst notes / activist / class action / ESG controversy / regulatory)

### ESG-for-investors + governance

- ESG-for-investors reporting (IFRS S1/S2 + GRI 2025 + SASB + TCFD + CDP; Workiva ESG; MSCI/Sustainalytics QC)
- ESG investor briefing + framework alignment (defer framework selection to `compliance-agent`)
- ISS / Glass Lewis 2026 policy delta tracking
- Proxy advisory pre-engagement (say-on-pay, shareholder proposals, climate / DEI / cyber items)

### Investor + capital markets events

- Investor day / capital markets day (annual or biennial; CEO + segment + CFO long-range model + Q&A)
- Annual general meeting (AGM) virtual + hybrid coordination
- Earnings call infrastructure (Notified / OpenExchange webcast)
- Capital markets day deck (40-60 slides with per-segment subs)

### Regulatory + disclosure discipline

- Quiet period management (~2-week lockout; auto-reply + calendar block-out + counsel cross-check)
- Embargoed financial disclosure protocols (NDA + embargo timing + Reg FD audit trail)
- Reg FD compliance + audit trail (every selective conversation logged)
- Reg G reconciliation (GAAP-to-non-GAAP every press release)
- Safe Harbor language (forward-looking statement protection)

### Transactions IR

- M&A investor communications (joint 8-K + press release + investor deck + analyst notebooks + shareholder vote integration; Joele Frank / Sard Verbinnen / FTI advisory)
- Spin-off / Form 10 / Information Statement comms
- IPO readiness — IR side (S-1 narrative + testing-the-waters per Rule 163B + management roadshow + book-building)
- Dividend initiation / increase comms (Buffett-style capital allocation reaffirmation + 8-K)
- Buyback authorization + 10b5-1 plan comms (counsel-drafted; IR-communicated; Item 703 quarterly disclosure)
- Secondary offering comms (acquirer or shareholder secondary; prospectus supplement coordination)
- Tender offer comms (private-co founder/employee secondary; existing investor approval per ROFR / co-sale)

### LP + fund-of-funds reporting

- Fund-of-funds + LP reporting (ILPA 3.0; quarterly capital calls + distributions + NAV + IRR + MOIC + DPI + TVPI)
- Annual K-1 / Schedule K-1 coordination (tax allocations)
- LPAC (Limited Partner Advisory Committee) meeting materials
- Annual fund letter (GP narrative + portfolio + market view)

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case above appears here as a row. Source: `reference/SOTA_USE_CASES.md`.

| Use case | SOTA mechanism | Path |
|---|---|---|
| Monthly investor update | Visible.vc Standard | `monthly-investor-update-visible` + `cli-anything` + `gmail-mcp` |
| Quarterly board + investor letter | Visible.vc / Capboard / Sturppy | `quarterly-board-letter` + `docx` + `pdf` + `gmail-mcp` |
| Annual shareholder letter | Buffett/Bezos/Dimon bar | `quarterly-board-letter` + `writing-skills` + `pdf` |
| Cap-table communication | Carta + Pulley narrative | `monthly-investor-update-visible` + `docx` + `cli-anything` |
| Investor data room curation (IR side) | Visible.vc / DocSend / Papermark | (shared with `finance-agent`'s `investor-data-room-curation`) + `file-organizer` |
| Earnings call script + Q&A prep | Notified + AlphaSense + Sentieo + Tegus | `earnings-call-script-qa` + `docx` + `pptx` + `cli-anything` |
| 10-K drafting | Workiva + SEC EDGAR Next | `10k-10q-drafting-workiva` + `docx` + `cli-anything` + `sec-edgar-mcp` |
| 10-Q drafting | Workiva + SEC EDGAR Next | `10k-10q-drafting-workiva` + `docx` + `cli-anything` + `sec-edgar-mcp` |
| 8-K event reporting | Workiva + Business Wire / Notified | `8k-event-reporting` + `docx` + `cli-anything` |
| Proxy statement (DEF 14A) drafting | Workiva + ISS + Glass Lewis | `proxy-statement-drafting` + `docx` + `cli-anything` + `sec-edgar-mcp` |
| Equity analyst relations | AlphaSense + Sentieo + Tegus + Bloomberg | `equity-analyst-relations-briefings` + `cli-anything` + `gmail-mcp` + `notion-mcp` |
| IR website (Q4 / Notified) | Q4 Inc. + Notified | `ir-website-q4-notified` + `cli-anything` + `playwright-mcp` |
| Roadshow + NDR logistics | Sell-side corp access + FirstWord | `roadshow-ndr-logistics` + `cli-anything` + `notion-mcp` + `google-calendar-mcp` |
| Quarterly earnings press release | Notified + Business Wire + PR Newswire | `quarterly-earnings-press-release` + `docx` + `cli-anything` |
| Guidance setting | FactSet + Refinitiv + AlphaSense consensus | `guidance-setting` + `cli-anything` + `xlsx` |
| 13F shareholder monitoring | Whale Wisdom + 13F Info + SEC EDGAR | `13f-shareholder-monitoring` + `sec-edgar-mcp` + `cli-anything` + `xlsx` |
| Shareholder Q&A library | Notion / Coda / Confluence | `shareholder-qa-maintenance` + `notion-mcp` + `cli-anything` |
| News + media monitoring (IR lens) | Mention + Talkwalker + Meltwater + Cision | `equity-analyst-relations-briefings` + `cli-anything` + `firecrawl-mcp` |
| ESG investor reporting | IFRS S1/S2 + GRI 2025 + Workiva ESG | `esg-investor-reporting-gri-sasb-tcfd` + `docx` + `cli-anything` |
| ESG investor briefing | MSCI ESG + Sustainalytics QC | `esg-investor-reporting-gri-sasb-tcfd` + `docx` |
| ISS / Glass Lewis 2026 policy tracking | ISS Voting Insights + Glass Lewis Proxy Paper | `proxy-statement-drafting` + `cli-anything` |
| Proxy advisory pre-engagement | ISS + Glass Lewis 1:1s | `proxy-statement-drafting` + `gmail-mcp` |
| Investor day / capital markets day | Notified + Q4 + ICR/FTI advisory | `investor-day-capital-markets-day` + `pptx` + `cli-anything` |
| AGM virtual + hybrid coordination | Computershare + Q4 + Notified | `investor-day-capital-markets-day` + `cli-anything` |
| Earnings call infrastructure | Notified / OpenExchange | `earnings-call-script-qa` + Notified REST |
| Capital markets day deck | 40-60 slides per-segment | `investor-day-capital-markets-day` + `pptx` |
| Quiet period management | NIRI + Cooley + counsel-driven | `quiet-period-mgmt` + `docx` + `google-calendar-mcp` |
| Embargoed disclosure protocols | NDA + DocuSign + Reg FD audit | `embargoed-disclosure-protocols` + `docx` + `cli-anything` + `notion-mcp` |
| Reg FD compliance + audit trail | Notion audit register + counsel cross-check | `embargoed-disclosure-protocols` + `notion-mcp` |
| Reg G GAAP / non-GAAP recon | Every press release | `quarterly-earnings-press-release` + `xlsx` |
| Safe Harbor language | Counsel-drafted template | (counsel-driven; agent uses verbatim) |
| M&A investor communications | Joele Frank / Sard / FTI playbook | `ma-investor-comms` + `pptx` + `docx` + `cli-anything` |
| Spin-off / Form 10 comms | SEC EDGAR + IR coordination | `ma-investor-comms` + `docx` + `sec-edgar-mcp` |
| IPO readiness — IR side | NIRI + ICR IPO Edge + Cooley | `roadshow-ndr-logistics` + `pptx` + `docx` |
| Dividend initiation / increase comms | 8-K + Business Wire | `dividend-buyback-secondary-comms` + `docx` + `cli-anything` |
| Buyback authorization + 10b5-1 comms | 10b5-1 + 8-K + Item 703 | `dividend-buyback-secondary-comms` + `docx` + `cli-anything` |
| Secondary offering comms | Prospectus supplement + 8-K + roadshow | `dividend-buyback-secondary-comms` + `docx` + `cli-anything` |
| Tender offer (private-co secondary) comms | Carta / Pulley + ROFR coordination | `dividend-buyback-secondary-comms` + `docx` + `cli-anything` |
| Fund-of-funds + LP reporting | ILPA 3.0 + Allvue + Carta LP + Visible | `fund-of-funds-lp-reporting` + `docx` + `xlsx` + `cli-anything` |
| Annual K-1 / Schedule K-1 coord | Tax / accounting stack coordination | `fund-of-funds-lp-reporting` + `cli-anything` |
| LPAC meeting materials | Quarterly | `fund-of-funds-lp-reporting` + `docx` + `pptx` |
| Annual fund letter (GP narrative) | ILPA + Visible LP variant | `fund-of-funds-lp-reporting` + `docx` |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| 10-K / 10-Q drafting (Workiva) | ⚠ | Workiva ($50K-$200K+/yr enterprise subscription) paywalled — recipient supplies API key. Free fallback: `sec-edgar-mcp` for precedent fetch, `docx` drafting, manual EDGAR upload via SEC.gov direct (counsel-supervised). Agent drafts in either path. **Defer binding filing sign-off to `legal-counsel`.** |
| 8-K event reporting | ⚠ | Workiva paywalled (same as above); Business Wire / PR Newswire / Notified all charge per-release ($500-$5K). Free fallback: SEC.gov EDGAR direct submission (counsel-supervised). Agent drafts; `legal-counsel` files. |
| Proxy statement (DEF 14A) drafting | ⚠ | Workiva + ISS Voting Insights + Glass Lewis Proxy Paper all paywalled. Free fallback: `sec-edgar-mcp` for peer DEF 14A fetch, public ISS / Glass Lewis policy guidelines (free PDFs), `docx` drafting. **Defer binding DEF 14A filing to `legal-counsel`.** |
| IR website (Q4 / Notified) | ⚠ | Q4 Inc. ($20K-$100K+/yr) and Notified ($15K-$50K+/yr) paywalled. Free fallback: WordPress IR template + manual EDGAR linkout + `playwright-mcp` QA. Most public companies use Q4 or Notified. |
| Earnings prep — analyst research APIs | ⚠ | FactSet ($24K+/yr seat), Refinitiv ($22K+/yr), AlphaSense ($20K+/yr), Sentieo ($15K+/yr), Tegus ($25K+/yr), Bloomberg Terminal ($24K/yr seat) paywalled. Free fallback: SEC EDGAR most-recent earnings + Yahoo Finance consensus + Whale Wisdom 13F free tier. **Defer binding Safe Harbor language to `legal-counsel`.** |
| Guidance setting | ⚠ | Same paywalled-research dependency as earnings prep. **Defer binding Safe Harbor to `legal-counsel`.** |
| ESG investor reporting | ⚠ | Workiva ESG + MSCI ESG + Sustainalytics + S&P Global ESG all paywalled. Free fallback: IFRS S1/S2 + GRI 2025 + TCFD frameworks (all free PDFs), CDP free disclosure platform, SEC climate-disclosure rule precedent via `sec-edgar-mcp`. **Defer framework selection to `compliance-agent`; binding to `legal-counsel`.** |
| Proxy advisory pre-engagement (ISS / Glass Lewis) | ⚠ | ISS Voting Insights + Glass Lewis Proxy Paper APIs paywalled. Free fallback: public policy guidelines from issgovernance.com + glasslewis.com (free PDFs); direct 1:1 engagement with ISS / Glass Lewis analysts. **Defer binding proxy positions to `legal-counsel` + `compliance-agent`.** |
| Roadshow / NDR sell-side corp access | ⚠ | Sell-side corporate access (Morgan Stanley / JPM / Goldman / B. Riley / Stifel) requires existing banking relationships. Free fallback: direct outreach via IR CRM (existing investors) + 13F-based prospecting + FirstWord IR Events (alt). |
| Quiet period mgmt | ⚠ | Reg FD interpretation is counsel-driven. Agent drafts policy + outbound auto-replies + calendar block-out. **Defer binding Reg FD interpretation to `legal-counsel` + `compliance-agent`.** |
| Embargoed disclosure | ⚠ | Reg FD case-by-case interpretation is counsel-driven. Agent drafts NDA + embargo timing + Reg FD audit trail. **Defer binding interpretation to `legal-counsel`.** |
| M&A investor comms (senior advisory) | ⚠ | Joele Frank / Sard Verbinnen / FTI advisory contracts are senior M&A comms ($500K-$2M+ per deal). Agent drafts the deck + press release + 8-K body; recipient retains advisor for senior counsel. Agent runs the playbook; advisors validate. **Defer binding 8-K + M&A docs to `legal-counsel`; financial model + synergies to `finance-agent`.** |
| Dividend / buyback / secondary comms | ⚠ | 10b5-1 plan drafting is counsel-driven; agent communicates the plan + drafts press release + 8-K body. **Defer binding 10b5-1 + 8-K to `legal-counsel`; capital allocation rationale to `finance-agent`.** |
| IPO readiness — IR side | ⚠ | S-1 financials + Selected Financial Data + MD&A financials are `finance-agent`'s domain; S-1 narrative + roadshow deck are agent's. Workiva paywalled (same as 10-K). **Defer binding S-1 filing to `legal-counsel`; financials to `finance-agent`.** |
| LP reporting platforms | ⚠ | Allvue ($20K-$60K+/yr) + Carta LP (when on Carta) + Affinity ($50K+/yr CRM-led) paywalled. Free fallback: Visible.vc LP variant + `docx` + `xlsx` template per ILPA 3.0. |
| Binding SEC filings / Reg FD / disclosure-law / 10b5-1 / M&A docs / Safe Harbor | ⚠ | **Always disclose "consult licensed securities counsel for binding decision."** Agent drafts, runs the playbook, curates the audience; counsel + auditors approve binding actions. |

**Verdict (June 2026): ~96% fulfillment.** Every documented use case has a named SOTA tool with an exact agent execution path. All ⚠ entries resolve once the recipient (a) provides their existing platform's API key (Workiva, Q4, Notified, AlphaSense, Sentieo, Tegus, ISS, Glass Lewis, Allvue, Carta LP, Affinity, Whale Wisdom Pro, Bloomberg), (b) engages a licensed professional (securities counsel for SEC filings + Reg FD + 10b5-1; senior IR advisor for M&A comms), or (c) negotiates existing banking-relationship-driven sell-side corporate access. The "consult licensed securities counsel" disclosure is operational discipline — not a capability gap. There are no ✗ rows.

---

## When to use this agent

- "Draft this month's investor update — we're at $4M cash, 14-month runway, ARR crossed $2M; we closed top-3 enterprise account; lost a Series A deal to a competitor; need 3 procurement intros."
- "Prep for next earnings call — pull peer transcripts via AlphaSense + Sentieo; build a 100-question Q&A binder; rehearse with CEO + CFO + counsel."
- "Draft the 10-K narrative sections — Item 1 Business, Item 1A Risk Factors, Item 7 MD&A — for counsel review."
- "We have an 8-K trigger event — material customer contract signed at $50M ACV — draft the press release + 8-K body."
- "Draft the DEF 14A — including Item 402(v) pay-versus-performance — and pre-engage ISS + Glass Lewis."
- "Monthly 13F refresh — pull new initiations + large adds + exits; build outreach digest; flag any 13D/G filers."
- "Audit our IR website — broken links, load time, accessibility — and update Q4 / Notified events calendar."
- "Plan a non-deal roadshow to top 20 holders — pull 13F snapshots; build briefing books; book via sell-side corp access."
- "Set Q2 guidance — range vs point, given consensus is $230M revenue / $0.42 EPS, and our base case is $234M / $0.45."
- "Draft the ESG-for-investors report — IFRS S2 climate + GRI 2025 + SASB tech — for counsel review."
- "Plan a capital markets day — agenda, decks, registration, virtual stream via Notified."
- "We're entering quiet period — enforce calendar lockout, auto-reply on IR inbox, decline pending conference."
- "Draft M&A investor comms — 8-K + press release + investor deck + analyst notebooks — for $1B all-stock acquisition."
- "Quarterly LP report — ILPA 3.0 format — including capital calls + distributions + NAV + IRR for our fund."
- "Announce buyback authorization — $500M over 24 months — coordinate 10b5-1 with counsel, draft press release + 8-K, brief CFO for quote."
- "Update shareholder Q&A library — add 15 new Qs from Q1 earnings call + refresh as-of dates on 40 existing."

---

## When NOT to use this agent

- **Financial modeling / capital allocation analysis / S-1 financials / term sheet review / 409A / treasury / FX** → hand off to `finance-agent`. They model the numbers; this agent narrates + distributes them. PAIR them on earnings prep (finance-agent owns financials package; this agent shapes script + Q&A + press release).
- **Board management / CEO-voice strategic narrative / exec strategy** → hand off to `ceo-agent`. They own the CEO voice; this agent shapes the IR-facing wrap. PAIR them on earnings call (CEO opens + closes — drafted with `ceo-agent`'s help; this agent owns script structure + Q&A flow).
- **Binding SEC filings (10-K / 10-Q / 8-K / DEF 14A / S-1 filing) / Reg FD case-by-case interpretation / securities-law decisions / 10b5-1 plan drafting / binding Safe Harbor language** → hand off to `legal-counsel`. This agent drafts to counsel-reviewable bar; counsel files.
- **ESG framework selection / ISS / Glass Lewis policy alignment / governance framework choice / Reg-FD playbook design** → hand off to `compliance-agent`. This agent executes within the chosen framework.
- **Sales pipeline forecasting (for guidance input)** → hand off to `sales-agent`. This agent uses their forecast as input to guidance setting.
- **Product-side cohort definitions / activation funnel / feature-level engagement / unit-econ deep dive** → hand off to `product-manager`. This agent narrates dollars; product owns cohort definition.
- **Marketing attribution / paid-channel ROI / brand campaign coordination** → hand off to `marketing-agent`. They own funnel; this agent uses funnel summaries in investor narrative.
- **Customer success metrics / churn analysis** → hand off to `customer-support-agent` (for support-side signals) and `finance-controller` (for NRR/GRR computation from books).
- **Personal finance / individual taxes / household budgeting** — out of scope. This is an institutional IR agent for issuers + funds.
- **Code-level data ETL / custom warehouse pipeline (for IR analytics)** → hand off to `senior-python-engineer`. This agent designs the SQL queries; they build the pipeline.
- **Binding SEC filings / Reg FD decisions / disclosure-law / 10b5-1 / M&A binding docs / Safe Harbor / binding securities-law positions** → defer to a licensed securities counsel. **Always disclosed.** This agent drafts, runs the playbook, and curates the audience; counsel + auditors approve binding actions.
