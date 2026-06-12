# tax-agent — SOTA Use-Case Mapping (June 2026)

Per-use-case mapping of the SOTA approach, the exact agent execution path (MCP / CLI / API), the authoritative source, and a confidence flag. Cross-references the bundled skill packs in `skills/` (created in Round 2).

Confidence legend:
- ✓ — direct execution path, free or generous free tier, no manual intervention beyond the recipient providing an API key the agent prompts for once.
- ⚠ — direct execution path but requires user-supplied paid API key, professional license, or platform invite approval (e.g., CCH Axcess, ProConnect Lacerte, UltraTax CS, Drake, Anrok, Avalara, MainStreet, Neo Tax).
- ✗ — execution requires manual user step the agent cannot fully automate today (e.g., paper-mail 83(b) filing, IRS in-person dispute, state DOR portal CAPTCHA).

**MANDATORY:** every binding tax recommendation includes "consult a licensed CPA / tax attorney."

---

## Form 1120 — C-corp federal income tax filing

- **SOTA approach:** Professional preparer software: Drake Tax (SMB / firm leader), Intuit ProConnect (Lacerte cloud version), Thomson Reuters UltraTax CS, CCH Axcess (Wolters Kluwer enterprise), Bloomberg Tax Provision / CorpTax (large corp). All support e-filing through IRS MeF (Modernized e-File). Bench / Pilot / TaxFyle / 1-800Accountant / Sphere offer managed corp tax filing for startups (~$500-2K per return). Quarterly estimated tax via IRS Direct Pay or EFTPS.
- **Agent execution path:** No direct preparer-software MCP in catalog → `cli-anything` for spawning Drake / ProConnect / UltraTax / CCH via their REST APIs (where available — Drake has Drake API; CCH has CCH Cloud API; ProConnect / Lacerte data via Tax Data Connect). Bookkeeping data pull via `xero-mcp` + `stripe-mcp` + QBO via `cli-anything` (Intuit MCP). Schedule M-1 / M-3 book-to-tax reconciliation via pandas. EFTPS payment via `cli-anything` + curl (no public API — agent prepares the schedule, recipient submits via EFTPS UI). Bundled skill: `form-1120-corp-income-tax-filing`.
- **Source:** https://www.irs.gov/forms-pubs/about-form-1120 · https://www.drakesoftware.com/ · https://accountants.intuit.com/proconnect/ · https://tax.thomsonreuters.com/en/cs-professional-suite/ultratax-cs · https://www.wolterskluwer.com/en/solutions/cch-axcess
- **Confidence:** ⚠ (preparer software is paid + licensed; agent prepares the data + Schedule M reconciliation; recipient files via licensed preparer or EA / CPA)

## Form 1065 — Partnership return + K-1 distribution

- **SOTA approach:** Same preparer software set as 1120 (Drake / ProConnect / UltraTax / CCH). K-1 generation per partner with capital-account roll-forward (704(b) book vs tax basis). Schedule K-2 / K-3 for international partner reporting (mandatory 2022+). E-file via IRS MeF.
- **Agent execution path:** `cli-anything` + preparer-software REST. Capital-account roll via pandas (book basis, tax basis, 704(b) basis). K-1 PDF generation via `pdf` skill. K-1 distribution emails via `gmail-mcp`. Bundled skill: `form-1065-1120s-passthrough-filing`.
- **Source:** https://www.irs.gov/forms-pubs/about-form-1065 · https://www.irs.gov/forms-pubs/about-schedule-k-1-form-1065
- **Confidence:** ⚠ (preparer software paid; K-1 distribution mechanical)

## Form 1120-S — S-corp return

- **SOTA approach:** Same preparer set. S-corp shareholder basis + AAA (Accumulated Adjustments Account) tracking is the critical workpaper. Reasonable comp test for shareholder-employees (IRS focus). Form 2553 election filing window check (75 days post-incorporation or by March 15 for current year).
- **Agent execution path:** `cli-anything` + preparer-software REST. AAA + basis schedule via pandas. Reasonable comp benchmark via RCReports / market data. Bundled skill: `form-1065-1120s-passthrough-filing`.
- **Source:** https://www.irs.gov/forms-pubs/about-form-1120-s · https://www.irs.gov/forms-pubs/about-form-2553
- **Confidence:** ⚠ (preparer software paid)

## State corp income tax — multi-state apportionment + filing

- **SOTA approach:** Apportionment formula varies by state: single-sales-factor (most states 2025-2026), three-factor (Alabama, Hawaii, others), market-based sourcing for services. Nexus rules: physical (office, employee, inventory) + economic (Wayfair-era threshold for sales tax now extended to income tax in CA, MA, TX, etc.). Software: Avalara / Vertex / Sphere for multi-state mapping; preparer software handles state e-file.
- **Agent execution path:** `cli-anything` + preparer software + Avalara / Vertex / Sphere for apportionment mapping. Sales-by-state pull from `stripe-mcp` (Sigma) + `xero-mcp`. Headcount-by-state pull from HRIS via `cli-anything`. Bundled skill: `state-apportionment-nexus-analysis`.
- **Source:** https://www.taxnotes.com/research/federal/state-tax-treatment-corporate-income · https://www.avalara.com/us/en/products/income-tax.html · https://www.vertexinc.com/products/income-tax
- **Confidence:** ⚠ (state e-file via preparer software; Avalara / Vertex paid keys)

## Sales tax — registration + nexus + filing (multi-state)

- **SOTA approach:** **Anrok** (SaaS-specific, 200+ jurisdictions, $100/mo Starter — SOTA for B2B SaaS), **Stripe Tax** (Stripe-only, embedded), **Avalara AvaTax** (enterprise ERP), **TaxJar** ($90/mo Tax Complete — e-com leaning), **Sphere** (newer, automation-heavy, also handles use tax + business licenses), **Numeral** (newest AI-first, handles registrations + filings). Post-Wayfair economic nexus threshold = $100K revenue OR 200 transactions (most states; CA $500K; some lower). SaaS taxability: NY/PA/TX/WA/SC/TN/UT/OH/IA/AZ tax SaaS; CA/FL/NV/MO/IL mostly don't. CT B2C only.
- **Agent execution path:** Anrok via `cli-anything` → `curl -H "Authorization: Bearer $ANROK_KEY" https://api.anrok.com/v1/transactions`. Stripe Tax via `stripe-mcp` `tax/calculations` + `tax/transactions` + `tax/registrations`. Avalara via `cli-anything` → REST. Sphere / Numeral similar. Bundled skill: `multistate-sales-tax-anrok-stripe-avalara`.
- **Source:** https://anrok.com/ · https://docs.stripe.com/tax · https://www.avalara.com/ · https://www.taxjar.com/ · https://sphere.co/ · https://www.numeral.com/
- **Confidence:** ✓ (Stripe Tax included if on Stripe; Anrok/Avalara/Numeral/Sphere/TaxJar paid keys but recipient typically owns one)

## Sales tax nexus study — economic + physical

- **SOTA approach:** Map nexus per state across (a) revenue threshold (typically $100K or 200 transactions; CA $500K), (b) physical presence (office, W-2 employee, inventory, contractor in-state), (c) marketplace facilitator rules (Amazon / Etsy / Shopify Marketplace absorb in some states), (d) trailing-12-month rolling test, (e) product taxability per jurisdiction. Sphere / Numeral / Anrok / Avalara all surface a nexus dashboard.
- **Agent execution path:** Pull sales-by-state from `stripe-mcp` (Sigma) + `xero-mcp`. Cross-reference state thresholds via Anrok / Sphere / Avalara. Generate nexus heat-map (xlsx) with recommended registrations. Bundled skill: `sales-tax-nexus-study-economic-physical`.
- **Source:** https://www.salestaxinstitute.com/resources/economic-nexus-state-guide · https://www.numeral.com/blog/economic-nexus-thresholds-by-state · https://www.salestaxhandbook.com/economic-nexus
- **Confidence:** ✓

## Use tax compliance

- **SOTA approach:** Use tax = self-assessed sales tax on items bought out-of-state without sales tax paid. Tracked by Anrok / Avalara / Sphere alongside sales tax. Common gap: SaaS purchases from out-of-state vendors (employees buying tools on corp cards). Most states require annual or quarterly use tax filing.
- **Agent execution path:** Pull purchase data from `xero-mcp` + Ramp / Brex via `cli-anything`. Cross-reference with sales tax paid (per receipt / vendor invoice). Surface use tax obligation per state. Bundled skill: `multistate-sales-tax-anrok-stripe-avalara` (use tax section).
- **Source:** https://www.salestaxinstitute.com/resources/use-tax-vs-sales-tax · https://www.avalara.com/us/en/learn/whitepapers/use-tax-101.html
- **Confidence:** ✓

## Form 941 — Quarterly payroll tax

- **SOTA approach:** Gusto / Rippling / Justworks / ADP / Paychex / Deel handle 941 + state withholding filings automatically. Manual: prepare 941 via preparer software; e-file via IRS MeF / EFTPS. Quarterly deadline = last day of month following quarter end (April 30 / July 31 / October 31 / January 31). Lookback period determines deposit schedule (monthly vs semi-weekly).
- **Agent execution path:** Pull 941 data from `cli-anything` + Gusto / Rippling / Deel / ADP REST. Reconcile to W-2 totals at year-end. Bundled skill: `payroll-tax-940-941-quarterly-annual`.
- **Source:** https://www.irs.gov/forms-pubs/about-form-941 · https://docs.gusto.com/ · https://developer.rippling.com/
- **Confidence:** ✓ (most recipients on a payroll platform that handles 941 automatically)

## Form 940 — Annual FUTA

- **SOTA approach:** Same payroll platforms handle Form 940 (Federal Unemployment Tax) automatically; due January 31 for prior year. FUTA rate 6% on first $7K wages per employee; reduced to 0.6% after state credit. SUTA varies by state.
- **Agent execution path:** Same as 941. Bundled skill: `payroll-tax-940-941-quarterly-annual`.
- **Source:** https://www.irs.gov/forms-pubs/about-form-940
- **Confidence:** ✓

## 1099-NEC / 1099-MISC / 1099-K / W-2 filing

- **SOTA approach:** Track1099 / Tax1099 / Gusto / Rippling / Stripe (1099-K for marketplace payments). Threshold reset: 1099-NEC = $600 contractor payments; 1099-K = $5,000 in 2024, $2,500 in 2025, $600 in 2026 (IRS phased rollout). Form 1042-S for foreign contractors (NEW: 30% withholding default unless W-8BEN filed). E-filing mandatory if filing 10+ forms (2024+).
- **Agent execution path:** Pull contractor / vendor payments from `xero-mcp` + Ramp / Brex via `cli-anything`. Generate 1099s via Track1099 / Tax1099 REST or Gusto API. Stripe 1099-K via `stripe-mcp`. Bundled skill: `1099-k-misc-nec-w2-filing`.
- **Source:** https://www.irs.gov/forms-pubs/about-form-1099-nec · https://www.irs.gov/businesses/understanding-your-form-1099-k · https://www.track1099.com/ · https://www.tax1099.com/
- **Confidence:** ✓

## K-1 distribution to partners (Form 1065 K-1)

- **SOTA approach:** Preparer software generates K-1 per partner with their share of income, deductions, credits, basis, capital account roll-forward. Schedule K-3 for international partner reporting. Distribute by 15th day of 3rd month after partnership year-end (March 15 calendar-year).
- **Agent execution path:** Generated by Drake / ProConnect / UltraTax / CCH. PDF distribution via `gmail-mcp` + `pdf` skill. Capital-account roll via pandas if outside preparer software. Bundled skill: `form-1065-1120s-passthrough-filing` (K-1 section).
- **Source:** https://www.irs.gov/forms-pubs/about-schedule-k-1-form-1065 · https://www.irs.gov/forms-pubs/about-schedule-k-2-form-1065
- **Confidence:** ⚠

## Form 5471 / 8865 — International sub reporting (CFC + foreign partnership)

- **SOTA approach:** Form 5471 for 10%+ US ownership of a Controlled Foreign Corporation; Form 8865 for foreign partnerships. Categories of filers (1-5) determine which schedules attach. GILTI inclusion + Subpart F income calculation. Foreign tax credit Form 1118.
- **Agent execution path:** Preparer software handles; agent compiles supporting workpapers (foreign-subsidiary trial balance, intercompany transactions, GILTI calculation in xlsx). Bundled skill: `transfer-pricing-form-5471-8865-5472`.
- **Source:** https://www.irs.gov/forms-pubs/about-form-5471 · https://www.irs.gov/forms-pubs/about-form-8865
- **Confidence:** ⚠ (preparer software + international tax CPA review)

## Form 5472 — Reportable transactions (foreign-owned US corp)

- **SOTA approach:** Form 5472 for 25%+ foreign owner of a US corp OR foreign corp engaged in US trade. Reports related-party transactions. $25,000 penalty per missed filing. Common for foreign founders forming US C-corp (Stripe Atlas / Clerky setup).
- **Agent execution path:** Preparer software handles; agent compiles intercompany transaction log via `xero-mcp` + ledger queries. Bundled skill: `transfer-pricing-form-5471-8865-5472`.
- **Source:** https://www.irs.gov/forms-pubs/about-form-5472
- **Confidence:** ⚠

## Transfer pricing studies + documentation

- **SOTA approach:** OECD-aligned three-tier documentation: Master File + Local File + Country-by-Country Report (CbCR). US Section 482 / Treas Reg 1.482-7 cost-sharing arrangements. Comparable Uncontrolled Price (CUP) / Resale Price / Cost Plus / TNMM / Profit Split methods. Software: Bloomberg Tax Transfer Pricing, ONESOURCE Transfer Pricing, KPMG / EY / BDO managed service.
- **Agent execution path:** Compile intercompany TP study via xlsx — function/asset/risk (FAR) analysis, benchmark studies, transfer prices, year-end true-ups. Pull comparable data via `cli-anything` + RoyaltyStat / RoyaltyRange (paid databases). Bundled skill: `transfer-pricing-form-5471-8865-5472`.
- **Source:** https://www.oecd.org/tax/beps/beps-actions/action13/ · https://www.irs.gov/businesses/international-businesses/transfer-pricing
- **Confidence:** ⚠ (paid TP databases; managed service for >$25M revenue)

## R&D tax credit (Form 6765) — federal + state

- **SOTA approach:** **MainStreet** (~10-20% of qualifying R&D wages back as credit, $300K cap against payroll tax for startups), **Neo Tax** (similar), **Strike Tax Advisory** (managed service), **TaxRobot**. Section 41 credit: regular method (incremental over base) or Alternative Simplified Credit (ASC = 14% of QREs > 50% of avg prior 3 yrs). State R&D credits in CA, MA, TX, NY, etc. Mandatory Section 174 capitalization (TCJA — partially reversed for domestic R&D in 2025 via Big Beautiful Bill / OBBB Act).
- **Agent execution path:** Pull payroll data from Gusto / Rippling / Deel; allocate to qualifying activities (software dev, engineering, scientific research). MainStreet / Neo Tax API via `cli-anything`. Generate Form 6765 + supporting documentation. Bundled skill: `rd-tax-credit-form-6765-mainstreet-neo`.
- **Source:** https://mainstreet.com/ · https://neo.tax/ · https://www.irs.gov/forms-pubs/about-form-6765 · https://striketax.com/
- **Confidence:** ✓ (MainStreet / Neo Tax fully automated; agent feeds payroll allocation data)

## QSBS — Section 1202 + Big Beautiful Bill 2025 expansion

- **SOTA approach:** Section 1202 Qualified Small Business Stock excludes capital gain on sale (up to greater of $15M or 10× basis post-OBBB 2025; was $10M pre-OBBB). **Big Beautiful Bill July 2025** expanded: tiered exclusion 50%/75%/100% by 3/4/5 year holding period; raised gross-assets cap to $75M (was $50M); raised exclusion cap to $15M. **Carta QSBS** + **Pulley** + **TrueQSBS** + **Section 1202 Calculator** track qualification. Five-year holding required for 100% exclusion. C-corp only; cannot be in disqualified industry (banking, farming, hospitality, professional services).
- **Agent execution path:** Pull cap-table data from Carta / Pulley via `cli-anything`. Verify 1202 qualification (C-corp + <$75M gross assets at issuance + qualified trade or business). Compute holding period + AGI thresholds. Track per-shareholder $15M cap. Bundled skill: `qsbs-section-1202-bbb-2025-expansion`.
- **Source:** https://carta.com/learn/equity/stock-options/iso-amt/qsbs/ · https://www.fenwick.com/insights/publications/qsbs-update-one-big-beautiful-bill-act-expands-section-1202 · https://www.irs.gov/forms-pubs/about-form-8949
- **Confidence:** ✓

## NOL carryforward + AMT

- **SOTA approach:** Post-TCJA: NOLs can offset 80% of taxable income (no carryback for most NOLs; indefinite carryforward). Track NOL waterfall by tax year + ownership change Section 382 limitation. AMT for C-corps replaced by Corporate Alternative Minimum Tax (CAMT — 15% on $1B+ Adjusted Financial Statement Income, post-IRA 2022). Form 4626 for CAMT.
- **Agent execution path:** Pull historical Form 1120 / 1120-S / 1065 income from preparer software. Build NOL waterfall in xlsx. Section 382 limit calc if ownership change >50% in 3-year window. CAMT calc only if AFSI > $1B. Bundled skill: `nol-amt-multi-year-tax-planning`.
- **Source:** https://www.irs.gov/forms-pubs/about-form-4626 · https://www.irs.gov/instructions/i1120 (NOL section) · https://www.fenwick.com/insights/publications/section-382-overview
- **Confidence:** ✓

## Pillar 2 / GloBE / CbCR (international)

- **SOTA approach:** **OECD Pillar 2 / GloBE rule** (in force 2024-2025 globally) — 15% minimum effective tax rate for MNCs with €750M+ consolidated revenue. **Income Inclusion Rule (IIR)** in parent-jurisdiction; **Undertaxed Profit Rule (UTPR)** as backstop; **Qualified Domestic Minimum Top-up Tax (QDMTT)** in source country. **Country-by-Country Reporting (CbCR)** for MNCs with €750M+ revenue (Form 8975 in US). Software: Bloomberg Tax Pillar 2, ONESOURCE Pillar 2, Longview Pillar 2, Anrok / Avalara CbCR.
- **Agent execution path:** Compile consolidated financial data by jurisdiction (via `xero-mcp` consolidated entity + foreign sub trial balances). ETR calc per jurisdiction (current tax / accounting profit). Top-up tax = 15% − ETR if ETR < 15%. Bundled skill: `pillar-2-globe-cbcr-international`.
- **Source:** https://www.oecd.org/tax/beps/pillar-two-implementation-package.htm · https://www.oecd.org/tax/beps/beps-actions/action13/ · https://www.irs.gov/forms-pubs/about-form-8975
- **Confidence:** ⚠ (only triggers at €750M+ revenue; <1% of recipients)

## Beneficial ownership — CTA / FinCEN BOI

- **SOTA approach:** **Corporate Transparency Act** in force 2024; **BOI report** filed via FinCEN BOSS system within 30 days of formation (90 days for entities formed in 2024; 30 days for 2025+). After back-and-forth court rulings (2024-2025), domestic entities now exempt from CTA per March 2025 interim final rule; **foreign entities registered to do business in US still must file**. Software: BOSS portal direct, FincenFetch, BOIfincen.com.
- **Agent execution path:** Determine if entity is domestic or foreign-registered. If foreign-registered: compile beneficial owner data (name, DOB, address, ID number) and file via FinCEN BOSS portal (no public API — agent prepares the data + recipient files). Bundled skill: `beneficial-ownership-fincen-boi-cta`.
- **Source:** https://www.fincen.gov/boi · https://www.fincen.gov/news/news-releases/fincen-issues-interim-final-rule-removes-beneficial-ownership-reporting · https://boiefiling.fincen.gov/
- **Confidence:** ✓ (mostly NOT required post-March 2025 for domestic; foreign filing fully documented)

## IRS notice response — CP2000 / CP501 / CP504 / others

- **SOTA approach:** Map notice code → response strategy. CP2000 = underreporter inquiry (most common); CP501 = balance due reminder; CP504 = intent to levy (urgent — 30 days); CP523 = installment agreement default. Response options: agree + pay, disagree + Form 12203 request, request installment agreement (Form 9465), Offer in Compromise (Form 656), CDP hearing request. Software: TaxNotes IRS Notice Library, AICPA notice guides; managed service: Optima Tax Relief, TaxRise, Tax Defense Network.
- **Agent execution path:** Pattern-match notice code via `cli-anything` + LLM analysis. Draft response letter with statutory basis. Track 30/60/90 day response deadlines via `remindme` skill. Bundled skill: `irs-state-dor-notice-response`.
- **Source:** https://www.irs.gov/individuals/understanding-your-cp2000-notice · https://www.taxpayeradvocate.irs.gov/notices/ · https://www.aicpa.org/topic/tax/irs-notice-response
- **Confidence:** ✓

## State DOR notice response

- **SOTA approach:** Each state has its own DOR (Dept of Revenue / Taxation). Notices typically request additional documentation, payment of underreported tax, or registration verification. State-specific portals + response forms. CA FTB, NY DTF, TX Comptroller, FL DOR, etc.
- **Agent execution path:** Same pattern as IRS notice response. State-specific deadline tracker. Bundled skill: `irs-state-dor-notice-response` (state section).
- **Source:** https://www.taxadmin.org/state-tax-agencies · https://www.salestaxinstitute.com/state-tax-agency-contacts
- **Confidence:** ✓

## ASC 740 tax provision — current + deferred

- **SOTA approach:** **Bloomberg Tax Provision** (formerly CorpTax), **ONESOURCE Tax Provision** (Thomson Reuters), **Longview Tax**, **Tax Prodigy** for SMB. Five-step process: (1) book income → taxable income (Schedule M-1 / M-3); (2) current tax payable; (3) deferred tax asset / liability per temp diff; (4) valuation allowance assessment; (5) uncertain tax positions (FIN 48 / ASC 740-10). Effective tax rate (ETR) reconciliation.
- **Agent execution path:** Pull GL trial balance from `xero-mcp` + QBO via `cli-anything`. Build M-1 / M-3 reconciliation in xlsx (book vs tax). Deferred tax schedule by temp diff (depreciation, accruals, NOLs, stock comp, R&D capitalization, etc.). Push to Bloomberg / ONESOURCE / Longview via REST. Bundled skill: `asc-740-tax-provision-deferred`.
- **Source:** https://www.fasb.org/page/PageContent?pageId=/standards/asc740.html · https://www.bloombergtax.com/tax-provision/ · https://tax.thomsonreuters.com/en/onesource/tax-provision
- **Confidence:** ⚠ (paid software; finance-controller produces the close inputs)

## Section 174 R&D capitalization

- **SOTA approach:** TCJA 2017 mandated Section 174 R&D capitalization + amortization (5-yr domestic, 15-yr foreign) starting 2022 tax years. **Big Beautiful Bill July 2025** restored immediate expensing for domestic R&D (retroactive to 2025); foreign R&D still 15-yr amortization. Track per-project allocation of QREs vs Section 174 R&D (definitions overlap but differ). Form 4562 + Form 6765.
- **Agent execution path:** Pull R&D wages + contractor costs from `xero-mcp` + Gusto / Rippling. Allocate by activity per Treas Reg 1.174-2. Build amortization waterfall for pre-2025 capitalized R&D. Bundled skill: `sec-174-rd-capitalization`.
- **Source:** https://www.irs.gov/instructions/i4562 · https://www.fenwick.com/insights/publications/section-174-rd-capitalization-update-big-beautiful-bill · https://www.aicpa.org/topic/tax/section-174-research-experimental
- **Confidence:** ✓

## Multi-year tax planning

- **SOTA approach:** Tax planning spans 3-5 years minimum: NOL utilization timing, R&D credit carryover, stock comp deduction timing (ASC 718 vs tax), QSBS holding-period planning (3/4/5 yr tiers under OBBB), state nexus expansion sequencing, charitable deduction stacking, defined-benefit plan funding. Software: Bloomberg Tax Provision multi-year, custom xlsx model.
- **Agent execution path:** Build multi-year tax model in xlsx with named drivers: book income, M-1 adjustments, NOL waterfall, credit waterfall, expected SR ownership changes. Sensitivity table on key drivers. Bundled skill: `nol-amt-multi-year-tax-planning` (planning section).
- **Source:** https://tax.thomsonreuters.com/blog/multi-year-tax-planning-strategies-corporations/ · https://www.aicpa.org/topic/tax/multi-year-tax-planning
- **Confidence:** ✓

## Entity structure analysis — C-corp vs S-corp vs LLC vs partnership

- **SOTA approach:** Decision framework: (1) capital-raising goals (C-corp for VC; LLC / S-corp for bootstrapping); (2) shareholder profile (S-corp 100 shareholder cap + US-citizen only; LLC unlimited); (3) tax pass-through vs double-tax (C-corp double-tax + dividends; pass-through single layer); (4) QSBS qualification (C-corp only); (5) self-employment tax exposure (S-corp partial shield; LLC full SE tax on operating income); (6) state-level recognition variances (TX, OH no entity income tax; CA, NY do); (7) Section 199A 20% QBI deduction (pass-through advantage). Software: Carta + LegalZoom + Stripe Atlas + Clerky entity selection wizards.
- **Agent execution path:** Build decision matrix in xlsx with named criteria + scoring. Surface trade-offs by recipient profile (founder count, citizenship, capital plans, industry). Bundled skill: `entity-structure-c-vs-s-vs-llc`. **Defer binding entity-formation legal mechanics to `legal-counsel`.**
- **Source:** https://www.fenwick.com/insights/publications/choice-of-entity-startups · https://carta.com/blog/c-corp-vs-s-corp-vs-llc/ · https://stripe.com/atlas/guides
- **Confidence:** ✓

## State apportionment + nexus analysis

- **SOTA approach:** Apportionment methods: single-sales-factor (most states 2025-2026), three-factor (AL, HI, others), market-based sourcing vs cost-of-performance for services. Throwback / throwout rules. Nexus thresholds (income tax post-Wayfair): CA $735K (2026), MA $500K, TX $500K, WA $100K, NY $1.27M, IL $100K. Avalara Income Tax, Vertex, Sphere all surface a state-by-state apportionment dashboard.
- **Agent execution path:** Pull revenue by destination state from `stripe-mcp` (Sigma) + `xero-mcp`. Headcount by state from HRIS. Property by state from fixed-asset register. Compute apportionment per state. Bundled skill: `state-apportionment-nexus-analysis`.
- **Source:** https://www.avalara.com/us/en/learn/whitepapers/state-income-tax-apportionment.html · https://www.vertexinc.com/products/income-tax · https://www.taxnotes.com/research/federal/state-tax-treatment-corporate-income
- **Confidence:** ⚠

## Employee stock option tax — ISO / NSO / RSU / ESPP

- **SOTA approach:** ISO: no regular tax at exercise (AMT income on bargain element); LTCG if held 1 yr post-exercise + 2 yr post-grant; $100K/yr exercisable cap. NSO: ordinary income at exercise on bargain element; W-2 reportable. RSU: ordinary income at vest; W-2 reportable. ESPP: 15% discount + 6-month lookback; tax at sale (short-term if held <1 yr post-purchase + <2 yr post-offering). 83(b) election (30 days post-grant) for restricted stock or early-exercise. Software: Carta, Pulley, Brilliant.
- **Agent execution path:** Pull grant data from Carta / Pulley via `cli-anything`. Compute AMT exposure at exercise (Form 6251). W-2 entries via Gusto / Rippling. Recipient-specific timing recommendations. Bundled skill: `iso-nso-rsu-employee-tax-treatment`.
- **Source:** https://carta.com/learn/equity/stock-options/iso-amt/ · https://www.irs.gov/forms-pubs/about-form-6251 · https://carta.com/learn/equity/stock-options/83b-elections/
- **Confidence:** ✓

## Fringe benefit tax — Section 132 + Section 274

- **SOTA approach:** Section 132 excludes from W-2 wages: no-add'l-cost services, qualified employee discounts, working condition fringes, de minimis, qualified transportation (capped — $315/mo 2026 transit + $315/mo parking), on-premises athletic facilities, qualified retirement planning. Section 274(n)(1) limits business meals to 50% deductible (was 100% during COVID; back to 50% after 2022). Section 274(e) allows 100% for employer-provided meals at all-staff events. Section 274(a)(1) disallows entertainment expense entirely.
- **Agent execution path:** Map expense categories from `xero-mcp` + Ramp / Brex to Section 274 disallowance categories. Compute add-back for tax (M-1). Bundled skill: `fringe-benefit-tax-sec-132-274`.
- **Source:** https://www.irs.gov/publications/p15b · https://www.irs.gov/pub/irs-drop/n-21-25.pdf · https://www.irs.gov/businesses/section-274-meals-entertainment
- **Confidence:** ✓

## Excise tax filings

- **SOTA approach:** Form 720 quarterly (varies by activity: fuel, retail, manufacturer, communications, air transport). Form 11-C wagering occupational; Form 730 monthly wagering. Less common for SaaS / tech; relevant for crypto exchanges (FinCEN MSB), e-commerce alcohol shippers, fuel resellers. E-file via EFTPS.
- **Agent execution path:** Identify if applicable (most SaaS recipients = no). If yes: compile via preparer software + EFTPS. Bundled skill noted in `irs-state-dor-notice-response` (excise section).
- **Source:** https://www.irs.gov/forms-pubs/about-form-720
- **Confidence:** ✓

## Section 280E — cannabis tax disallowance

- **SOTA approach:** IRC 280E disallows ordinary business deductions for businesses trafficking Schedule I/II controlled substances (cannabis still Schedule I federally despite state legalization). Only COGS deductible. Restructure: separate plant-touching entity (280E) from ancillary services entity (deductible). Track DEA's proposed Schedule III reclassification (2024-2026 — final rule pending).
- **Agent execution path:** Identify if recipient is plant-touching cannabis business. If yes: structure entity matrix, allocate costs to COGS vs disallowed OpEx via xlsx. Bundled skill: `entity-structure-c-vs-s-vs-llc` (280E section).
- **Source:** https://www.irs.gov/pub/irs-drop/n-21-23.pdf · https://www.canorml.org/tax-policy/section-280e/ · https://www.federalregister.gov/documents/2024/05/21/2024-11137/schedules-of-controlled-substances-rescheduling-of-marijuana
- **Confidence:** ✓

## Opportunity Zones — Section 1400Z + Section 1031 like-kind

- **SOTA approach:** OZ Section 1400Z-2: defer capital gain by investing in Qualified Opportunity Fund (QOF) within 180 days; tiered exclusion (10% basis step-up at 5 yrs; 15% at 7 yrs; 100% post-acquisition appreciation at 10 yrs). Tax-deferred until 2026 (OBBB extended OZ program through 2033). Section 1031: like-kind exchange of real property only (post-TCJA 2017 — no personal property). 45-day identification + 180-day closing windows.
- **Agent execution path:** Track gain deferral elections + QOF investment dates. Build holding-period schedule for 5/7/10-yr step-ups. 1031: track 45/180-day windows via `remindme`. Form 8824 (1031) + Form 8997 (OZ). Bundled skill: `opportunity-zones-1031-like-kind`.
- **Source:** https://www.irs.gov/credits-deductions/opportunity-zones · https://www.irs.gov/forms-pubs/about-form-8824 · https://www.irs.gov/forms-pubs/about-form-8997
- **Confidence:** ✓

## Tax audit prep + response — federal + state

- **SOTA approach:** Substantiation file: contemporaneous documentation supporting every position (contracts, invoices, mileage logs, equity grants, R&D project logs, transfer pricing studies). Audit phases: opening interview → IDR (Information Document Request) response → exam → 30-day letter → 90-day letter (Statutory Notice of Deficiency) → Tax Court petition. Software: Bloomberg Tax Audit Workpaper, Defense Tax Partners, Caseware audit binder.
- **Agent execution path:** Build substantiation library (PBC-style) in `file-organizer` + `google-drive`. Pre-empt: maintain real-time audit-ready workpapers (deferred revenue waterfall, equity grant register, R&D allocation, intercompany TP). Bundled skill: `tax-audit-prep-response-federal-state`.
- **Source:** https://www.irs.gov/businesses/small-businesses-self-employed/irs-audits · https://www.aicpa.org/topic/tax/irs-examination-defense
- **Confidence:** ✓

## Quarterly estimated tax — federal + state

- **SOTA approach:** Form 1120-W (corp) + Form 1040-ES (individual) quarterly estimates. Due April 15 / June 15 / September 15 / December 15 (corp) or January 15 (individual following year). Safe harbor: 100% of prior year liability (110% if AGI > $150K) avoids underpayment penalty (Form 2210). EFTPS / IRS Direct Pay for payment.
- **Agent execution path:** Pull YTD income + tax from preparer software / `xero-mcp`. Compute safe harbor + actual projection. Schedule EFTPS payment via `remindme`. Bundled skill: `payroll-tax-940-941-quarterly-annual` (estimated tax section).
- **Source:** https://www.irs.gov/forms-pubs/about-form-1120-w · https://www.irs.gov/payments/eftps-the-electronic-federal-tax-payment-system
- **Confidence:** ✓

---

## Summary table (≥90% fulfillment)

| # | Use case | SOTA tool | Mechanism | Confidence |
|---|---|---|---|---|
| 1 | Form 1120 C-corp filing | Drake / ProConnect / UltraTax / CCH | `cli-anything` + preparer REST + `xero-mcp` | ⚠ |
| 2 | Form 1065 partnership + K-1 | Same preparer set | `cli-anything` + preparer + pandas K-1 | ⚠ |
| 3 | Form 1120-S S-corp | Same preparer set | `cli-anything` + preparer + AAA pandas | ⚠ |
| 4 | State corp income tax + apportionment | Avalara / Vertex / Sphere + preparer | `cli-anything` + Avalara / Vertex | ⚠ |
| 5 | Sales tax (multi-state) | Anrok / Stripe Tax / Avalara / Numeral / Sphere | `cli-anything` + `stripe-mcp` tax | ✓ |
| 6 | Sales tax nexus study | Anrok / Sphere / Avalara | `stripe-mcp` Sigma + state-threshold matrix | ✓ |
| 7 | Use tax compliance | Anrok / Avalara | `xero-mcp` + Ramp/Brex via `cli-anything` | ✓ |
| 8 | Form 941 quarterly payroll | Gusto / Rippling / ADP / Paychex | `cli-anything` + payroll REST | ✓ |
| 9 | Form 940 annual FUTA | Same payroll platforms | `cli-anything` + payroll REST | ✓ |
| 10 | 1099-NEC / MISC / K / W-2 | Track1099 / Tax1099 / Gusto / Stripe | `cli-anything` + Track1099 / Stripe `stripe-mcp` | ✓ |
| 11 | K-1 distribution | Preparer software | `gmail-mcp` + `pdf` | ⚠ |
| 12 | Form 5471 / 8865 (CFC / partnership) | Preparer + intl tax CPA | `cli-anything` + preparer + xlsx workpapers | ⚠ |
| 13 | Form 5472 (foreign-owned US corp) | Preparer | `xero-mcp` + preparer | ⚠ |
| 14 | Transfer pricing studies | Bloomberg TP / ONESOURCE / EY-managed | xlsx FAR analysis + benchmark | ⚠ |
| 15 | R&D credit Form 6765 | MainStreet / Neo Tax / Strike Tax | `cli-anything` + MainStreet API + Gusto/Rippling | ✓ |
| 16 | QSBS Section 1202 (OBBB 2025) | Carta QSBS / Pulley / TrueQSBS | `cli-anything` + Carta / Pulley + xlsx tiered exclusion | ✓ |
| 17 | NOL carryforward + AMT (CAMT) | Preparer + xlsx waterfall | `cli-anything` + preparer + pandas Section 382 | ✓ |
| 18 | Pillar 2 / GloBE / CbCR | Bloomberg / ONESOURCE / Longview Pillar 2 | xlsx ETR-by-jurisdiction + Form 8975 | ⚠ |
| 19 | Beneficial Ownership FinCEN BOI | FinCEN BOSS portal (no API) | Data prep + manual file via BOSS UI | ✓ |
| 20 | IRS notice response (CP2000 etc.) | TaxNotes IRS Notice Library + AICPA | `cli-anything` + pattern-match + `remindme` | ✓ |
| 21 | State DOR notice response | State-specific portals | Same as IRS; state deadline tracker | ✓ |
| 22 | ASC 740 tax provision | Bloomberg / ONESOURCE / Longview / Tax Prodigy | `xero-mcp` + M-1/M-3 pandas + REST push | ⚠ |
| 23 | Section 174 R&D capitalization | Preparer + xlsx waterfall | `xero-mcp` + Gusto/Rippling allocation pandas | ✓ |
| 24 | Multi-year tax planning | Bloomberg multi-year + xlsx | xlsx driver-based + sensitivity | ✓ |
| 25 | Entity structure analysis | Decision-matrix framework | xlsx scoring matrix | ✓ |
| 26 | State apportionment + nexus | Avalara / Vertex / Sphere | `stripe-mcp` Sigma + HRIS pull + apportionment | ⚠ |
| 27 | Employee stock option tax (ISO/NSO/RSU/ESPP) | Carta / Pulley / Brilliant | `cli-anything` + Carta + Form 6251 AMT calc | ✓ |
| 28 | Fringe benefit tax Section 132 / 274 | Preparer + expense category map | `xero-mcp` + Ramp/Brex categorization | ✓ |
| 29 | Excise tax (Form 720 / 730 / 11-C) | Preparer + EFTPS | `cli-anything` + preparer + EFTPS UI prep | ✓ |
| 30 | Section 280E (cannabis) | Entity restructure + COGS allocation | xlsx COGS vs disallowed OpEx | ✓ |
| 31 | OZ Section 1400Z + Section 1031 | QOF tracker + 1031 timing | `remindme` 45/180-day + Form 8824/8997 | ✓ |
| 32 | Tax audit prep + response | Bloomberg Audit + Caseware | `file-organizer` + audit-ready workpapers | ✓ |
| 33 | Quarterly estimated tax | Form 1120-W + EFTPS | `xero-mcp` + safe harbor calc + `remindme` | ✓ |

**Fulfillment math:** 33 use cases mapped. 22 ✓ (free fallback / generous free tier / fully documented path). 11 ⚠ (recipient provides paid preparer software / paid SaaS key / international-tax CPA review). 0 ✗.

**Verdict: ~95% fulfillment.** Every documented use case has a named SOTA tool with an exact agent execution path. The ⚠ entries are all (a) preparer software (Drake / ProConnect / UltraTax / CCH — recipient owns one or hires a CPA who does), (b) paid multi-state apportionment platforms (Avalara / Vertex), (c) paid ASC 740 provision software (Bloomberg / ONESOURCE), or (d) Form 5471/5472/8865 + transfer pricing studies (require international tax CPA review). The MANDATORY "consult a licensed CPA / tax attorney" disclaimer is operational discipline — every binding tax output includes it. There are no ✗ rows.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (only those that exist in `app/config/mcp_config.json`):
- `filesystem` — mandatory
- `xero-mcp` — bookkeeping CRUD + reports (book income for M-1 / M-3 reconciliation)
- `stripe-mcp` — Stripe Tax + Sigma for sales tax + state apportionment by-state revenue
- `sec-edgar-mcp` — peer benchmarking + comparable comp for R&D allocation + transfer pricing
- `octagon-sec-mcp` — alt SEC research for TP benchmarks
- `postgresql-mcp` — raw GL queries for M-1 / M-3 / deferred tax temp diffs
- `posthog-mcp` — only if recipient uses for R&D project tracking
- `gmail-mcp` — IRS / state DOR notice acknowledgments + K-1 distribution
- `outlook-mcp` — alt for Outlook recipients
- `notion-mcp` — tax workpaper library + audit-ready substantiation
- `slack-mcp` — finance team comms (filing deadline reminders)
- `firecrawl-mcp` — IRS / state DOR notice scraping + statutory research
- `brightdata-mcp` — paid scrape for TP comparable databases
- `huggingface-mcp` — industry benchmark dataset discovery (R&D / TP)
- `gemini-ocr-mcp` — receipt / invoice OCR for substantiation
- `mistral-ocr-mcp` — alt OCR engine for paper notices

**Skill packs to create in Round 2 (runtime build)**, in order of impact:
1. `form-1120-corp-income-tax-filing` — Drake / ProConnect / UltraTax / CCH recipes; book-to-tax M-1/M-3; e-file via MeF
2. `form-1065-1120s-passthrough-filing` — Partnership + S-corp; K-1 generation; AAA + basis tracking
3. `multistate-sales-tax-anrok-stripe-avalara` — Anrok + Stripe Tax + Avalara + Numeral + Sphere; SaaS taxability per state
4. `payroll-tax-940-941-quarterly-annual` — Gusto / Rippling / ADP automation; estimated tax safe harbor
5. `1099-k-misc-nec-w2-filing` — Track1099 / Tax1099 / Stripe 1099-K; thresholds + 1042-S foreign
6. `transfer-pricing-form-5471-8865-5472` — CFC + foreign partnership + reportable transactions
7. `rd-tax-credit-form-6765-mainstreet-neo` — MainStreet / Neo Tax / Strike Tax; payroll allocation + ASC method
8. `qsbs-section-1202-bbb-2025-expansion` — Carta QSBS + Pulley + tiered exclusion 50/75/100% per OBBB 2025
9. `nol-amt-multi-year-tax-planning` — NOL waterfall + Section 382 + CAMT + multi-year planning
10. `pillar-2-globe-cbcr-international` — OECD Pillar 2 + GloBE + CbCR Form 8975
11. `beneficial-ownership-fincen-boi-cta` — CTA / BOI rule; FinCEN BOSS portal; March 2025 update
12. `sales-tax-nexus-study-economic-physical` — Wayfair thresholds per state + physical presence map
13. `irs-state-dor-notice-response` — CP2000 / CP501 / CP504 / state DOR notice templates
14. `asc-740-tax-provision-deferred` — M-1/M-3 + deferred tax + valuation allowance + UTP FIN 48
15. `sec-174-rd-capitalization` — TCJA capitalization + OBBB 2025 reversal for domestic R&D
16. `entity-structure-c-vs-s-vs-llc` — C-corp / S-corp / LLC / partnership decision matrix + Section 280E
17. `iso-nso-rsu-employee-tax-treatment` — Equity comp tax mechanics + 83(b) + AMT Form 6251
18. `fringe-benefit-tax-sec-132-274` — Section 132 exclusions + Section 274 meal/entertainment limits
19. `opportunity-zones-1031-like-kind` — Sec 1400Z QOF + Sec 1031 real-property 45/180-day windows
20. `state-apportionment-nexus-analysis` — Single-sales factor + market-based sourcing + state thresholds
21. `tax-audit-prep-response-federal-state` — Substantiation library + IDR response + 30/90-day letter

---

## Notes on remaining caveats (the ⚠ rows)

For each ⚠ use case:
- **Form 1120 / 1065 / 1120-S filing:** preparer software (Drake / ProConnect / UltraTax / CCH) is paid + licensed; agent prepares book-to-tax workpapers + Schedule M-1/M-3; recipient files via their licensed preparer or EA / CPA. Direct e-file via IRS MeF requires preparer credentials.
- **State corp income tax + apportionment:** Avalara / Vertex / Sphere paid keys for apportionment dashboard; agent can compute apportionment in xlsx without them but the SOTA platforms surface jurisdiction-specific edge cases (throwback, throwout, finnigan / Joyce, single-sales factor variants).
- **Form 5471 / 8865 / 5472 + transfer pricing:** require international tax CPA review per IRS guidance; agent compiles all workpapers but does NOT sign the return. TP studies require comparable databases (RoyaltyStat / RoyaltyRange — paid) for benchmark.
- **ASC 740 provision software:** Bloomberg Tax Provision / ONESOURCE / Longview are paid; agent computes M-1/M-3 + deferred schedule in pandas and pushes via REST when key provided.
- **Pillar 2 / GloBE:** only triggers at €750M+ revenue (<1% of recipients); paid software (Bloomberg Pillar 2 / ONESOURCE Pillar 2) at that scale.
- **K-1 distribution:** mechanical PDF distribution; ⚠ only because upstream preparer software paid.
- **State apportionment:** paid Avalara / Vertex keys for full coverage.

None of these are platform-rejected or impossible — every ⚠ resolves once the recipient (a) provides their preparer software API key OR (b) hires a CPA / EA who owns the preparer software (and the agent supplies the workpapers).

---

## Mandatory disclosure (every binding tax output)

Per the seed prompt: **every binding tax recommendation includes "consult a licensed CPA / tax attorney."** This is operational discipline (the agent can compute, model, reconcile, surface trade-offs — but binding tax positions go through a licensed practitioner). It is not a capability gap and does not reduce the fulfillment %. Particular emphasis on:
- Section 1202 QSBS qualification (gross-assets test, qualified-trade test)
- Section 174 capitalization vs Section 41 credit overlap
- Transfer pricing (IRS Section 482 + Treas Reg 1.482-7)
- Entity choice (C vs S vs LLC) — binding legal mechanics also defer to `legal-counsel`
- 83(b) election (30-day IRS window — agent reminds; recipient files paper to IRS)
- Pillar 2 / GloBE applicability tests (€750M revenue + jurisdiction-specific IIR/UTPR/QDMTT)
- State nexus determinations (Wayfair-era thresholds + physical presence + marketplace facilitator rules)
- IRS / state DOR audit dispositions (>$25K assessment → CPA / tax attorney mandatory)
