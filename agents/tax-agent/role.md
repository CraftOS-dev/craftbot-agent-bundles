# Tax Agent — Role Content (appended to AGENT.md)

> This file appends to `AGENT.md` and is **not** loaded into the agent's default context. The agent reads `soul.md` every turn and **greps** this file for deep references when stuck.
>
> Search-friendly headings include: "Capability reference", "Form 1120 playbook", "Form 1065 / 1120-S playbook", "Sales tax nexus playbook", "Payroll tax playbook", "1099 family playbook", "R&D credit playbook", "QSBS Section 1202 playbook", "Section 174 capitalization playbook", "NOL Section 382 playbook", "Pillar 2 GloBE playbook", "BOI / CTA playbook", "IRS notice response playbook", "ASC 740 provision playbook", "Equity comp tax playbook", "Transfer pricing playbook", "State apportionment playbook", "Opportunity Zone playbook", "Section 1031 playbook", "Section 280E playbook", "Section 274 meals entertainment playbook", "Audit prep playbook", "Antipattern catalog", "SOTA tool reference", "OBBB 2025 reference", "TCJA reference", "Wayfair reference", "IRA 2022 reference".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Federal tax forms (filing surface)

- **Form 1120** — C-corp income tax return; due 15th day of 4th month after year-end (April 15 calendar-year); 6-month extension via Form 7004.
- **Form 1120-S** — S-corp return; due 15th day of 3rd month after year-end (March 15 calendar-year); extension via Form 7004.
- **Form 1065** — Partnership return; due 15th day of 3rd month after year-end (March 15 calendar-year); K-1 distribution mandatory.
- **Schedule M-1** — Book-to-tax reconciliation (small entities); attached to 1120 / 1065 / 1120-S.
- **Schedule M-3** — Detailed book-to-tax reconciliation (>$10M assets); attached to 1120 / 1065 / 1120-S.
- **Schedule K-1** — Per-partner / per-shareholder allocation; distributed by 15th day of 3rd month after year-end.
- **Schedule K-2 / K-3** — International items per partner; mandatory 2022+.
- **Form 941** — Quarterly federal payroll tax; due last day of month after quarter end.
- **Form 940** — Annual FUTA; due January 31 prior year.
- **Form 944** — Annual payroll tax (small employer alternative to 941; IRS notifies eligibility).
- **Form 1099-NEC** — Contractor payments ≥$600.
- **Form 1099-MISC** — Other non-employee compensation, rent, prizes.
- **Form 1099-K** — Marketplace / payment-processor reporting; threshold rollout: 2024 $5K → 2025 $2.5K → 2026 $600.
- **Form 1099-DIV / 1099-INT / 1099-B** — Dividends / interest / broker.
- **Form 1042-S** — Foreign person US-source income; 30% default withholding.
- **Form W-2** — Employee wages + withholding.
- **Form W-3** — W-2 transmittal.
- **Form 5471** — 10%+ US-owned foreign corp; Categories 1-5 of filers.
- **Form 8865** — Foreign partnership reporting.
- **Form 5472** — 25%+ foreign-owned US corp reportable transactions; $25K penalty per missed filing.
- **Form 6765** — R&D credit (Section 41).
- **Form 8974** — Payroll-offset R&D credit election for startups (Section 41(h)).
- **Form 8975** — Country-by-Country Report (CbCR) for €750M+ MNCs.
- **Form 8997** — QOF (Opportunity Zone) annual reporting.
- **Form 8824** — Section 1031 like-kind exchange.
- **Form 8949 + Schedule D** — Capital gains + QSBS exclusion.
- **Form 7004** — Automatic 6-month extension.
- **Form 4626** — Corporate AMT (CAMT — 15% on $1B+ AFSI post-IRA 2022).
- **Form 6251** — Individual AMT (ISO bargain element).
- **Form 4562** — Depreciation + amortization; Section 179 + bonus depreciation.
- **Form 8275 / 8275-R** — Disclosure to avoid substantial-understatement penalty.
- **Form 9465** — Installment agreement request.
- **Form 656** — Offer in Compromise.
- **Form 12203** — Request for appeals review.
- **Form 1118** — Foreign tax credit (corp).
- **Form 1116** — Foreign tax credit (individual).
- **Form 1120-W** — Corp quarterly estimated tax.
- **Form 1040-ES** — Individual quarterly estimated tax.
- **Form 2553** — S-corp election.
- **Form 8832** — Entity classification election.

### Preparer software platforms supported

- **Drake Tax** — SMB / firm leader; 1040 / 1120 / 1065 / 1120-S / 990; Drake API for data import/export; ~$2-5K/yr per seat.
- **Intuit ProConnect** — Lacerte's cloud version; tier-priced; tightly integrated with QBO.
- **Intuit Lacerte** — Desktop power-user (1040 / 1120 / 1065 / 1120-S / 990 / 706); top-tier for complex returns.
- **Thomson Reuters UltraTax CS** — Enterprise firm software; Tax Data Connect for API.
- **CCH Axcess Tax** — Cloud-native Wolters Kluwer; CCH Cloud API.
- **CCH ProSystem fx Tax** — On-premise CCH counterpart.
- **Drake** specifically: Drake Cloud (hosted) + Drake Premier (managed cloud) + Drake Tax (desktop).
- **TaxSlayer Pro** — Mid-market alt.
- **TaxAct Professional** — SMB.
- **ATX (Wolters Kluwer)** — SMB.
- **Bench / Pilot / TaxFyle / 1-800Accountant / Sphere** — Managed corp tax filing for startups.

### Sales tax platforms

- **Anrok** — SaaS-specific; 200+ jurisdictions; $100/mo Starter; auto-registration + filing.
- **Stripe Tax** — Embedded Stripe-only; tax/calculations + tax/transactions + tax/registrations APIs.
- **Avalara AvaTax** — Enterprise ERP integration; opaque pricing.
- **TaxJar (now Stripe-owned)** — E-commerce; $90/mo Tax Complete; 600+ categories.
- **Numeral** — AI-first; handles registrations + filings end-to-end.
- **Sphere** — Modern automation; sales + use + business licenses.
- **Quaderno** — SaaS-friendly; alt to Anrok.
- **Vertex Indirect Tax O Series** — Enterprise.
- **TaxCloud** — SMB freemium.

### Income tax + apportionment (multi-state)

- **Avalara Income Tax** — multi-state apportionment dashboard.
- **Vertex Income Tax (formerly Tax Series)** — Enterprise.
- **Sphere** — Apportionment + nexus + filing.
- **Bloomberg Tax State Tax Research** — Statutory database.
- **CCH State Tax Research** — Alt statutory database.

### R&D credit platforms

- **MainStreet** — Startups; ~10-20% qualifying R&D wages back; $300K payroll-offset cap.
- **Neo Tax** — AI-driven R&D credit + QSBS.
- **Strike Tax Advisory** — Managed R&D credit; covers audit defense.
- **TaxRobot** — Self-serve R&D credit.
- **AlphaCredit** — Mid-market R&D.
- **Cherry Bekaert / BDO / RSM** — Managed R&D credit service (regional + Big 6).

### QSBS / Section 1202 trackers

- **Carta QSBS** — Integrated with cap table; tiered exclusion modeling.
- **Pulley QSBS** — Pre-seed / Series A.
- **TrueQSBS** — Standalone QSBS tracker.
- **Section 1202 Calculator** — Free online calc.
- **Brilliant** — Equity-comp + QSBS combined.

### Tax provision (ASC 740)

- **Bloomberg Tax Provision (CorpTax)** — Enterprise; multi-entity consolidation.
- **ONESOURCE Tax Provision (Thomson Reuters)** — Enterprise alt.
- **Longview Tax** — Enterprise alt; CCH-owned.
- **Tax Prodigy** — SMB.
- **Insightsoftware Tax Reporting** — Mid-market.

### International tax + transfer pricing

- **Bloomberg Tax Transfer Pricing** — TP studies + benchmark.
- **ONESOURCE Transfer Pricing** — Alt.
- **RoyaltyStat / RoyaltyRange** — TP comparable databases (paid).
- **OECD Pillar 2 reporting**: Bloomberg Pillar 2, ONESOURCE Pillar 2, Longview Pillar 2.
- **KPMG / EY / BDO / PwC / Deloitte** — Managed TP service for >$25M revenue.

### Workpaper + binder

- **Caseware** — Audit + tax binder; standard for CPA firms.
- **AdvanceFlow (Thomson Reuters)** — Cloud workpaper alt.
- **Workiva** — GRC + audit + tax workpaper.
- **CCH ProSystem fx Engagement** — Workpaper software.

### 1099 family filing

- **Track1099** — Electronic 1099 filing; mainstream.
- **Tax1099** — Alt e-filing.
- **Yearli** — Greatland's 1099 product.
- **eFile4Biz** — Alt.
- **Gusto / Rippling / ADP / Paychex / Justworks** — Payroll platforms handle 1099 + W-2 automatically.

### Payroll platforms (for 941 / 940 / 1099 / W-2)

- **Gusto** — SMB leader; 941 + state withholding auto.
- **Rippling** — All-in-one (HRIS + payroll + IT).
- **ADP RUN** — SMB.
- **ADP Workforce Now** — Mid-market.
- **Paychex Flex** — SMB / mid-market.
- **Deel** — Global contractor + EOR.
- **Justworks** — PEO model.
- **OnPay** — SMB freemium.

### Federal + state payment portals

- **EFTPS** — Electronic Federal Tax Payment System; mandatory for corp deposits.
- **IRS Direct Pay** — Individual federal tax payments.
- **IRS e-Services** — Online preparer + bulk e-file.
- **IRS MeF (Modernized e-File)** — E-filing system used by preparer software.
- **FinCEN BOSS portal** — BOI report filing.
- **State DOR portals** — Per-state (CA FTB, NY DTF, TX Comptroller, FL DOR, etc.).

---

## Form 1120 playbook (C-corp federal income tax)

### Timeline (60-90 days from fiscal year-end)

- **T-90 (close fiscal year):** GL closed; trial balance generated; book accruals booked via `finance-controller`; ASC 740 close inputs received.
- **T-60:** M-1 / M-3 reconciliation drafted; permanent + temporary differences identified; R&D credit Form 6765 substantiation built; international forms (5471 / 5472 / 8865) workpapers compiled.
- **T-30:** Form 1120 + schedules drafted in preparer software; depreciation Form 4562 reconciled; NOL waterfall + Section 382 limit checked; CAMT (Form 4626) checked if AFSI > $1B.
- **T-0 (April 15 calendar-year):** Sign + e-file via IRS MeF through preparer software. OR file Form 7004 for 6-month extension (Oct 15 deadline) — DOES NOT extend payment deadline.

### Schedule M-1 / M-3 reconciliation (book → tax)

**Permanent differences** (book ≠ tax forever):
- Tax-exempt interest (book income; not taxable)
- Officer life insurance (book expense; not deductible)
- 50% meals limit (Section 274(n)(1))
- Entertainment disallowance (Section 274(a)(1))
- Fines + penalties (not deductible)
- Section 280E disallowance (cannabis)
- Federal income tax expense (not deductible)
- Domestic Production Activities Deduction (DPAD — pre-TCJA)

**Temporary differences** (book ≠ tax timing; reverse over time):
- Depreciation (book straight-line vs tax MACRS + bonus + Section 179)
- Deferred revenue (book ratable vs tax recognition rules)
- Accrued compensation (book accrual vs tax cash basis for unpaid)
- Bad-debt allowance (book reserve vs tax write-off)
- Stock-based compensation (book ASC 718 ratable vs tax at vest / exercise)
- R&D Section 174 capitalization (TCJA: 5-yr domestic / 15-yr foreign — OBBB 2025 restored immediate expensing for domestic R&D)
- Goodwill amortization (book none for ASC 350 unless impaired vs tax 15-yr Section 197)
- Inventory UNICAP (Section 263A — book expense vs tax capitalized)

### Form 1120 schedules

- **Schedule C** — Dividends income + Section 250 GILTI / FDII deduction
- **Schedule J** — Tax computation + credits
- **Schedule K** — Other info (business activity, accounting method, audit history)
- **Schedule L** — Balance sheet per books
- **Schedule M-1 / M-3** — Book-to-tax reconciliation
- **Schedule N** — Foreign operations (if applicable)
- **Schedule UTP** — Uncertain Tax Positions (FIN 48); required if assets > $10M

### Tie-out checklist

- [ ] Schedule L cash = Balance Sheet cash per books (tied to bank)
- [ ] Schedule L equity = cap table + retained earnings
- [ ] M-1 / M-3 book net income = Income Statement net income
- [ ] M-1 / M-3 taxable income = Schedule J line 28 = Page 1 line 30
- [ ] Depreciation Form 4562 ties to Schedule M-1 / M-3 temp diff
- [ ] R&D Form 6765 credit ties to Schedule J credit line
- [ ] State income tax expense (M-1 perm diff)
- [ ] Federal income tax expense (M-1 perm diff)
- [ ] NOL deduction ties to NOL waterfall + Section 382 limit
- [ ] CAMT (Form 4626) tested if AFSI > $1B

---

## Form 1065 / 1120-S playbook (partnership + S-corp)

### Partnership-specific items

- **K-1 generation** — Each partner gets a K-1 by 15th day of 3rd month after year-end (March 15 calendar). Allocation per partnership agreement (special allocations under 704(b) economic-effect rules).
- **Schedule K-2 / K-3** — International items per partner (mandatory 2022+).
- **704(b) book basis vs tax basis vs GAAP basis** — Three separate capital account rollforwards.
- **Section 754 election** — Inside basis adjustment on partner death / sale / distribution; one-time election.
- **Section 743(b) adjustment** — Inside basis step-up for new partner buying interest.
- **Section 734(b) adjustment** — Inside basis adjustment for distributions.
- **At-risk + passive activity** — Limit deductions per partner under Sections 465 + 469.

### S-corp specific items

- **Form 2553 election** — File by 75th day of year-of-election OR by March 15 for current year.
- **AAA (Accumulated Adjustments Account)** — Tracks S-corp's accumulated taxable income for distribution-vs-dividend treatment.
- **Shareholder basis** — Required workpaper; limits deductible losses (Section 1366(d)).
- **Reasonable compensation test** — Shareholder-employees must take W-2 reasonable comp before distributions (IRS audit focus).
- **Form 7203** — Shareholder basis attachment (mandatory 2022+).
- **100-shareholder limit + US-citizen-only requirement**.
- **Section 1374 built-in gains tax** — Applies for 5 yrs after C-to-S conversion.

---

## Sales tax nexus playbook

### Nexus mapping (post-Wayfair June 2018)

**Economic nexus thresholds** (most states):
- $100K revenue OR 200 transactions in 12-month period (rolling)
- CA: $500K
- NY: $500K + 100 transactions
- TX: $500K
- WA: $100K (no transaction threshold)
- KS: $100K (no transaction threshold)
- TN: $100K + 100 transactions

**Physical nexus** (always triggers):
- Office / brick-and-mortar
- W-2 employee in state
- Inventory in state (incl. Amazon FBA in some states)
- Contractor in state (in most states)
- Trade show booth (sometimes)

**Marketplace facilitator** (absorbs nexus in some states):
- Amazon, eBay, Etsy, Walmart, Shopify Marketplace (per state — varies)
- Seller may still have nexus from non-marketplace channels

### Product taxability matrix (SaaS — June 2026)

**Tax SaaS as default:**
- NY, PA, TX (B2B), WA, SC, TN, UT, OH, IA, AZ, RI, MA (some), MS, NM, HI, WV, DC

**Don't tax SaaS:**
- CA, FL, NV, MO, IL (most), GA (most), MD (some), CO, OR (no sales tax), MT (no sales tax), NH (no sales tax), DE (no sales tax), AK (no statewide)

**Tax with caveats:**
- CT (B2C only — B2B exempt)
- VA (yes for tangible; SaaS analyzed per characteristic)
- MN (yes for prewritten software; varies)
- KS (yes since 2020)
- IN (yes since 2024)

### Workflow

1. Pull revenue-by-state from `stripe-mcp` Sigma + `xero-mcp` for trailing 12 months
2. Map nexus per state (economic + physical + marketplace facilitator absorption)
3. Map product taxability per state (SaaS, services, tangible)
4. Recommend platform (Anrok for SaaS multi-state; Stripe Tax if 100% Stripe; Avalara for enterprise ERP; Sphere for use tax + business licenses; Numeral for AI-first)
5. Register where nexus is triggered (some states 4-12 weeks lead time)
6. Configure platform to calculate at checkout / invoice + remit + file per cadence (monthly / quarterly / annual per state + volume)
7. Reconcile filings to GL sales-tax-payable account each close

---

## Payroll tax playbook

### Form 941 quarterly + Form 940 annual

**Form 941 deposit schedule** (per IRS lookback period — calendar year 2 yrs prior):
- **Lookback ≤ $50K:** monthly deposits (15th of following month)
- **Lookback > $50K:** semi-weekly deposits (Wed-Fri payment = following Wed; Sat-Tue payment = following Fri)
- **>$100K single-day liability:** next-banking-day deposit

**Form 941 deadlines** (quarterly):
- Q1: April 30 / Q2: July 31 / Q3: October 31 / Q4: January 31

**Form 940 FUTA** (annual; due January 31 for prior year):
- 6% on first $7K wages per employee
- Reduced to 0.6% after state SUTA credit

### State payroll tax

- **State income tax withholding** — varies (CA EDD, NY DTF, TX no state PIT, FL no state PIT, WA no state PIT).
- **State unemployment (SUTA)** — varies by state experience rating.
- **State disability** — CA SDI, NJ SDI, NY SDI, RI TDI, HI TDI.
- **Local taxes** — NYC tax, Yonkers tax, PA local, OH local, etc.

### Quarterly estimated tax

- **Form 1120-W (corp):** April 15 / June 15 / September 15 / December 15
- **Form 1040-ES (individual):** April 15 / June 15 / September 15 / January 15 (following year)
- **Safe harbor:** 100% of prior year liability avoids underpayment penalty (110% if AGI > $150K)
- **Form 2210** — Underpayment penalty calculation
- **EFTPS** — payment portal

---

## 1099 family playbook

### Threshold rollout (2024-2026)

- **1099-NEC** — Contractor payments ≥$600 (unchanged)
- **1099-K** — Marketplace / payment-processor reporting:
  - 2023 and prior: $20K + 200 transactions
  - 2024: $5K (lowered)
  - 2025: $2.5K (lowered)
  - 2026: $600 (final IRS phased rollout)

### Form 1042-S — Foreign person US-source income

- **30% withholding default** unless W-8BEN filed (treaty rate or exemption)
- **W-8BEN-E** for foreign entities
- **W-8ECI** for foreign person with US trade
- **W-8EXP** for foreign government
- **Quarterly Form 1042 deposits**; Form 1042-S annual recipient form; Form 1042 annual return

### E-filing mandate

- **2024+:** mandatory e-file if filing 10+ forms across all types (1099, W-2, 1042-S, 941, etc.) — was 250+ pre-2024
- **Track1099 / Tax1099 / Yearli** handle e-file automatically
- **Gusto / Rippling / ADP / Stripe** for payroll-platform-integrated 1099s

---

## R&D credit playbook (Form 6765)

### Section 41 four-part test

1. **Permitted purpose** — develop or improve product / process / software / technique / formula / invention
2. **Technological in nature** — relies on physical / biological / engineering / computer science
3. **Process of experimentation** — evaluate alternatives via modeling, simulation, systematic trial-error
4. **Eliminate uncertainty** — at outset, capability / methodology / appropriate design uncertain

### QRE (Qualified Research Expenses) categories

- **Wages** — W-2 wages for qualifying research; subject to Section 41(b)(2)(A) substantial test
- **Contract research** — 65% of payments to US contractors performing qualifying research
- **Supplies** — Materials used in qualifying research (not deductible as inventory)
- **Cloud computing** — Per Notice 2023-63 + Treas Reg 1.41-2(b)(3), cloud services count

### Computation methods

**Regular method (Section 41(a)):**
- Credit = 20% × (current year QRE − base amount)
- Base amount = fixed-base % × avg gross receipts last 4 yrs
- Fixed-base % = QRE / gross receipts in 1984-1988 (capped 16%)
- Floor: 50% × current year QRE

**Alternative Simplified Credit (ASC) method (Section 41(c)(5)):**
- Credit = 14% × (current year QRE − 50% × avg prior 3-yr QRE)
- If no prior 3-yr QRE: 6% × current year QRE
- Pick higher of regular vs ASC

### Payroll-offset election (Section 41(h)) — startups only

- Qualified small business: <$5M gross receipts current year + first year of gross receipts within last 5 yrs
- Election: up to $500K credit against employer payroll tax (Section 41(h)(2))
- File Form 6765 + Form 8974 with payroll tax return (Form 941)

### Substantiation requirements (IRS Tier 1 audit issue)

- Project-by-project documentation
- Time tracking allocating R&D hours per project
- Technological uncertainty descriptions per project
- Process-of-experimentation log per project
- Contract research agreement copies (verify "rights" + "economic risk" tests)
- Supplies invoices linked to specific projects

### Section 174 capitalization interaction

**TCJA 2017** (in effect 2022+ tax years):
- Section 174 R&D = mandatory capitalization + amortization
- Domestic R&D: 5-yr straight-line (no mid-year convention; ratable monthly)
- Foreign R&D: 15-yr straight-line
- "Section 174 R&D" defined broader than Section 41 QRE — includes software dev, even if not credit-qualifying

**OBBB July 2025** (retroactive to TY 2025):
- Domestic R&D: immediate expensing restored
- Foreign R&D: still 15-yr amortization
- Pre-2025 capitalized R&D: continue amortizing original schedule (no catch-up deduction allowed)

---

## QSBS Section 1202 playbook (OBBB 2025 expansion)

### Qualification requirements at issuance

- **C-corp only** (not S-corp, partnership, LLC)
- **Gross assets ≤ $75M** at issuance (was $50M pre-OBBB July 2025) — INCLUDES cash from issuance
- **Original issuance** — stock acquired directly from corp (not secondary)
- **Substantially all** of assets used in qualified trade or business
- **5-yr active business test** — during substantially all of holding period

### Qualified trade or business EXCLUDES

- Banking / insurance / financing / leasing / investing
- Farming
- Mining (some)
- Hotel / restaurant / hospitality
- Professional services (health, law, engineering, architecture, accounting, actuarial, consulting, athletics, performing arts, financial services, brokerage)
- Per IRC Section 1202(e)(3)

### Big Beautiful Bill July 2025 tiered exclusion

| Holding period | Exclusion % | Pre-OBBB (TY ≤2024) |
|---|---|---|
| <3 yrs | 0% | 0% |
| 3 yrs | 50% | 0% (binary — 5 yr or nothing) |
| 4 yrs | 75% | 0% |
| ≥5 yrs | 100% | 100% (5 yr was binary threshold) |

### Cap per shareholder

- **Greater of $15M (was $10M pre-OBBB) OR 10× basis**
- Per-shareholder, per-issuer
- Spouse + family attribution rules apply

### AMT / NII / state-level treatment

- **No AMT preference for QSBS post-2010** (Section 1202(a)(4))
- **No NII tax (Section 1411)** on excluded gain
- **State treatment varies:** CA / PA / NJ generally DON'T follow federal QSBS; NY / MA / CT do (with state-specific rules)

### Workflow

1. Verify at issuance: C-corp + gross-assets test + qualified-trade test
2. Track per-shareholder holding period (Carta QSBS / Pulley / TrueQSBS)
3. Monitor ongoing qualification (active-business test)
4. Plan sale timing — hold to 5-yr for 100% exclusion if possible
5. At sale: Form 8949 (Code Q for QSBS) + Schedule D
6. Document substantiation: cap-table at issuance, gross-assets snapshot, qualified-trade test memo, holding-period log

---

## NOL + Section 382 + CAMT playbook

### NOL post-TCJA (Tax Cuts and Jobs Act 2017)

- **Post-2017 NOLs** — 80% taxable-income limit; indefinite carryforward; no carryback (except 2018-2020 CARES Act 5-yr carryback)
- **Pre-2018 NOLs** — 20-yr carryforward; 2-yr carryback (old rules); no 80% limit
- Track separately by tax year of origination

### Section 382 ownership change limit

- **Trigger:** >50% ownership change (by value) of 5% shareholders in 3-yr testing period
- **Limit:** post-change NOL utilization = pre-change value × federal long-term tax-exempt rate (LTTER ~4-5% mid-2026)
- **5% shareholder grouping rules** — public-group attribution; private equity / VC fund attribution
- **Software:** Bloomberg Tax Section 382 + custom xlsx
- **Built-in gains / losses** — NUBIG / NUBIL adjustments to limit (5-yr recognition period)

### CAMT (Corporate Alternative Minimum Tax — post-IRA 2022)

- **15% on Adjusted Financial Statement Income (AFSI)** > $1B (averaged over 3 prior years)
- **Affected:** ~150 large US corps (mostly Fortune 500)
- **AFSI** starts with GAAP book income + adjustments (depreciation, equity comp, NOLs, etc.)
- **Form 4626** — calculation
- **Almost never triggers** for startups / SMB

### NOL waterfall workpaper

```
Tax Yr | Originated | Carryforward Bal | 80% Limit (current yr taxable inc × 80%) | Used | Remaining | Section 382 Limit (if applicable)
2018   | $X         | $A               | $L                                       | $U   | $A-$U     | $S
2019   | $Y         | $B               | ...                                      | ...  | ...       | ...
...
```

---

## Pillar 2 / GloBE / CbCR playbook

### Pillar 2 mechanics (OECD Inclusive Framework)

- **Trigger:** MNC consolidated revenue > €750M (~$800M USD)
- **Rule:** 15% minimum effective tax rate per jurisdiction
- **Income Inclusion Rule (IIR):** parent jurisdiction tops-up to 15%
- **Undertaxed Profit Rule (UTPR):** if no IIR, source country tops up
- **Qualified Domestic Minimum Top-up Tax (QDMTT):** source country pre-empts top-up
- **In force:** 2024 (some EU + UK + South Korea + Japan); 2025+ widening

### ETR computation per jurisdiction

```
ETR (jurisdiction) = Covered Taxes / GloBE Income
Top-up Tax = max(0, 15% − ETR) × Excess Profit
Excess Profit = GloBE Income − Substance-Based Income Exclusion (SBIE)
SBIE = 5% × tangible assets + 5% × payroll (transition: 8% / 10% phased)
```

### CbCR Form 8975

- **Trigger:** US MNC parent with > €750M consolidated revenue
- **Report per jurisdiction:** revenue, profit before tax, income tax paid + accrued, headcount, tangible assets
- **Due:** with US parent's Form 1120 (April 15 calendar)
- **Exchanged automatically with OECD partners**

### Workflow

1. Verify €750M threshold (consolidated revenue)
2. Compile financial data by jurisdiction (via `xero-mcp` consolidated entity + foreign sub trial balances)
3. Compute ETR per jurisdiction
4. Compute top-up tax = (15% − ETR) × Excess Profit
5. File via Bloomberg Pillar 2 / ONESOURCE Pillar 2 / Longview if available

---

## BOI / CTA playbook (FinCEN Beneficial Ownership)

### CTA timeline + status

- **Corporate Transparency Act passed January 2021** — effective January 1, 2024
- **March 2024:** federal court declared CTA unconstitutional (Nat'l Small Business United v. Yellen); injunction limited
- **December 2024:** 5th Circuit affirmed → SCOTUS stay
- **January 2025:** SCOTUS lifted stay; CTA back in force
- **February 2025:** Texas court re-issued injunction
- **March 2025:** Treasury interim final rule — domestic entities EXEMPT; only foreign-registered entities file
- **Status as of June 2026:** foreign-registered entities continue to file via FinCEN BOSS portal

### Filing process (foreign-registered entities)

1. Compile beneficial owner data per BO:
   - Full legal name
   - Date of birth
   - Residential street address
   - Unique identifying number (US driver's license / US / foreign passport)
   - Image of ID document
2. Compile company applicant data (first 2 individuals filing entity registration)
3. File via FinCEN BOSS portal (no public API — agent prepares the data file; recipient files via portal)
4. Update within 30 days of any change to BO info

### Substantial control test (beneficial owner)

A BO is anyone who either:
- Owns ≥25% of equity OR
- Exercises substantial control (Senior Officer, has authority to make important decisions, etc.)

---

## IRS notice response playbook

### Common notice codes + response

| Code | Description | Response window | Action |
|---|---|---|---|
| CP01H | Identity theft (locked SSN) | — | File ID theft affidavit Form 14039 |
| CP2000 | Underreporter (W-2 / 1099 vs reported) | 30 days | Agree + pay OR disagree + supporting docs |
| CP14 | Balance due notice | 21 days | Pay or installment Form 9465 |
| CP90 | Final notice of intent to levy (FNTL) | 30 days | **URGENT** — file Form 12153 CDP hearing or pay |
| CP501 | Reminder of balance due | 21 days | Pay or installment |
| CP503 | 2nd notice | 21 days | Pay or installment |
| CP504 | Intent to levy state tax refund | 30 days | **URGENT** — pay or installment or CDP hearing |
| CP523 | Installment agreement default | 30 days | Reinstate installment |
| CP2501 | Underreporter (similar to CP2000) | 30 days | Agree or disagree |
| Letter 3219 | Statutory Notice of Deficiency (SND, "90-day letter") | 90 days | **HARD DEADLINE** — Tax Court petition or letter expires |
| Letter 1058 | FNTL — Final notice of intent to levy | 30 days | **URGENT** — CDP hearing request |

### Response forms

- **Form 12203** — Request for appeals review
- **Form 12153** — CDP (Collection Due Process) hearing request
- **Form 9465** — Installment agreement request
- **Form 656** — Offer in Compromise
- **Form 433-A / 433-B** — Collection Information Statement (individual / business)
- **Form 8857** — Innocent spouse relief
- **Form 911** — Taxpayer Advocate Service request

### Workflow

1. Pattern-match notice code (use `firecrawl-mcp` to scrape current IRS.gov notice descriptions if uncertain)
2. Pull supporting GL detail from `xero-mcp` + preparer software workpaper to verify position
3. Draft response: agree + pay, disagree + Form 12203, installment Form 9465, OIC Form 656, CDP Form 12153
4. Schedule deadline via `remindme` (30 / 60 / 90 day per notice type)
5. Send via certified mail (RetUrn Receipt) or e-fax tracking
6. **MANDATORY disclosure**: "Consult a licensed CPA / tax attorney; >$25K assessments require legal representation."

---

## ASC 740 tax provision playbook

### Five-step process

1. **Book → Taxable Income** — Apply M-1 / M-3 permanent + temporary differences
2. **Current Tax Payable** — Taxable income × statutory rate (federal 21% + state apportioned)
3. **Deferred Tax** — Temporary differences × enacted statutory rate
4. **Valuation Allowance** — Reduce DTA if more-likely-than-not (MLTN) not realizable
5. **Uncertain Tax Positions (UTP / FIN 48 / ASC 740-10)** — Recognize if MLTN sustained on technical merits; measure at largest amount > 50% likely

### Deferred tax temp diff library

- Depreciation (book straight-line vs tax MACRS + bonus)
- Deferred revenue
- Accrued comp (book accrued; tax cash for unpaid)
- Bad-debt allowance
- Stock-based compensation (ASC 718 vs tax at exercise / vest)
- R&D Section 174 capitalization (TCJA: 5-yr/15-yr — OBBB 2025: domestic now expensed)
- Goodwill (ASC 350 vs Section 197 15-yr)
- Lease (ASC 842 ROU asset vs tax operating-lease deduction)
- NOL carryforward (DTA)
- Tax credit carryforward (DTA — R&D, foreign tax credit, etc.)
- Capital loss carryforward (DTA)

### Valuation allowance assessment

- **Positive evidence:** profit history, future projections, NOL carryforward, tax planning strategies
- **Negative evidence:** history of losses, expiring NOLs, going-concern doubt
- **MLTN = > 50% probability of realization**

### UTP / FIN 48 documentation

- **Recognition step:** is position MLTN sustained on technical merits (assuming IRS audit)?
- **Measurement step:** largest amount > 50% probability of being sustained
- **Disclosure:** Schedule UTP (Form 1120) if assets > $10M
- **Software:** Bloomberg Tax UTP module, ONESOURCE UTP

### ETR reconciliation

```
Statutory federal rate                21.0%
State income tax (net of fed benefit)  +X%
Permanent differences:
  Section 274 meals                   +Y%
  Tax-exempt income                   −Z%
  Section 199A QBI                    −W%
R&D credit                            −R%
Foreign rate differential             ±V%
Section 199A QBI                      −P%
Valuation allowance change            ±Q%
UTP change                            ±U%
                                     -----
Effective tax rate                     N%
```

---

## Equity comp tax playbook

### ISO mechanics

- **Strike price ≥ current 409A FMV** (mandatory; below = 409A penalty)
- **$100K AMT rule** — if (strike × shares becoming exercisable in calendar year) > $100K, the excess is NSO-treated
- **90-day post-termination exercise window** standard
- **Long-term holding:** 1 yr post-exercise + 2 yr post-grant for LTCG + ISO disposition
- **AMT bargain element** at exercise — (FMV at exercise − strike) × shares = AMT income
- **Form 6251** AMT computation
- **Form 3921** issued by employer for each ISO exercise

### NSO mechanics

- **Ordinary income at exercise** on bargain element (FMV − strike) × shares
- **W-2 reportable** (subject to FICA + Medicare)
- **No holding-period advantage** — basis = FMV at exercise; gain/loss measured from there

### RSU mechanics

- **Ordinary income at vest** on FMV × shares
- **W-2 reportable** (subject to FICA + Medicare)
- **Net-share withholding** common — employer withholds ~22-37% via share sale
- **Holding period starts at vest** for capital gain

### ESPP mechanics

- **15% discount** + **6-month lookback** standard Section 423 plan
- **Qualifying disposition:** ≥1 yr from purchase + ≥2 yr from offering date → 15% ordinary + LTCG on appreciation
- **Disqualifying disposition:** sold within 1 yr of purchase OR within 2 yr of offering → ordinary income on spread + ST/LT capital gain on appreciation

### 83(b) election (CRITICAL — 30-day window)

- **Applies to:** restricted stock subject to vesting OR early-exercised options
- **What it does:** elect to pay ordinary income tax on spread between FMV and price paid at grant date (vs at vesting)
- **30-day filing window from grant date** to IRS — missed = no election
- **File:** signed form to IRS by mail (certified return-receipt); copy to employer; copy to personal records
- **Default agent action:** schedule `remindme` day 25 to ensure filing by day 30

---

## Transfer pricing playbook

### Section 482 + Treas Reg 1.482-7

**Methods (best-method rule per Treas Reg 1.482-1(c)):**
- **CUP (Comparable Uncontrolled Price)** — Most direct; uses identical or near-identical transactions
- **Resale Price Method** — For distributors; gross margin benchmark
- **Cost Plus Method** — For manufacturers / service providers; cost mark-up benchmark
- **CPM (Comparable Profits Method)** / **TNMM** (OECD-equivalent) — net profit indicator vs comparables
- **Profit Split Method** — Allocate combined profit by relative contribution
- **Unspecified methods** — If above don't apply

### OECD three-tier documentation

- **Master File** — Group structure, business overview, intangibles, financial activity, financial / tax position; one per MNC
- **Local File** — Country-specific; controlled transactions, comparables, financials of local entity
- **CbCR (Form 8975 in US)** — Per-jurisdiction revenue, profit, tax, headcount, assets

### Functions / Assets / Risks (FAR) analysis

For each related-party entity:
- **Functions** — what does it DO? (R&D, manufacturing, distribution, marketing, services)
- **Assets** — what does it OWN? (tangible, intangible, contracts)
- **Risks** — what does it BEAR? (market, credit, FX, R&D, warranty)

### Cost-sharing arrangement (CSA) under Treas Reg 1.482-7

- Participants share R&D costs + economic rights to intangibles by territory
- "Buy-in" payment for pre-existing intangibles
- "Platform Contribution Transaction (PCT)" — Stock-Based Compensation must be included (per IRS appeals 2016+ Altera ruling)

---

## State apportionment playbook

### Apportionment formulas (2025-2026)

**Single-sales factor** (most states):
- AL, CA, CO, CT, DC, GA, IL, IN, IA, KY, LA, ME, MD, MI, MN, MO, NE, NJ, NY, NC, ND, OH (CAT), OK, OR, PA, RI, SC, TN, UT, VT, VA, WA (B&O), WI, WV

**Three-factor (property + payroll + sales)**:
- AK, AR, FL, HI, ID, KS, MA, MT, NM, OH (option), TX (margin), WY

**Throwback rule** (sales not taxed in destination → throw back to origin):
- AL, AR, AK, CA, HI, ID, IL, IN, KS, LA, ME, MA, MS, MO, NE, NH, NM, ND, OK, OR, PA, RI, UT, VT, WI

**Throwout rule** (alt — exclude from denominator):
- ME, NJ, OR (partial)

### Market-based sourcing vs cost-of-performance

**Market-based sourcing (services / SaaS):**
- Sources to BUYER location
- States: AL, CA, CT, DC, GA, IL, IA, KY, LA, ME, MD, MA, MI, MN, MO, NE, NJ, NY, NC, OH (CAT), OK, OR, PA, RI, TN, UT, VT, WA (B&O), WI

**Cost-of-performance:**
- Sources to where MOST cost incurred
- States: AK, AZ, AR, CO, FL, HI, ID, IN, KS, MT, NV (no income tax), NH, NM, ND, SC, SD, TX (margin), VA, WV, WY

### State income tax economic nexus thresholds (2026)

| State | Threshold | Rule |
|---|---|---|
| CA | $735,019 (2026; CPI-adj) | Sales factor presence ($X) OR property ($86K) OR payroll ($86K) |
| MA | $500,000 | Sales > threshold |
| TX | $500,000 | Margin tax sales nexus |
| WA | $100,000 | B&O tax |
| NY | $1,272,000 (2026) | Sales > threshold |
| IL | $100,000 OR 200 txns | (income tax adopted Wayfair) |
| TN | $500,000 | F&E tax |
| HI | $100,000 OR 200 txns | |
| KS | $250,000 | |
| MI | $350,000 | |
| OH | CAT — $150K | |
| PA | $500,000 | |
| RI | $1,000,000 | |
| VA | $500,000 | |
| WI | $100,000 OR 200 txns | |

---

## Section 1031 + Opportunity Zone playbook

### Section 1031 (like-kind exchange) — post-TCJA

- **Real property only** (post-TCJA 2017 — no personal property)
- **45-day identification window** from date of sale (replacement property)
- **180-day closing window** (or due date of return, whichever earlier)
- **Qualified Intermediary (QI)** required (taxpayer cannot touch funds)
- **Boot** = non-like-kind consideration → taxable
- **Form 8824** + Schedule attached to 1040 / 1120

### Section 1400Z Opportunity Zones — post-OBBB

- **Investment in QOF within 180 days** of capital gain recognition → defer gain
- **5-yr hold:** 10% basis step-up
- **7-yr hold:** additional 5% (total 15%)
- **10-yr hold:** post-acquisition appreciation 100% excluded
- **Deferred gain recognized:** December 31, 2026 (extended to 2033 by OBBB 2025)
- **Form 8997** — Annual QOF investment reporting
- **Form 8949** + Schedule D — Gain deferral election

---

## Section 280E (cannabis) + Section 274 (meals/entertainment) playbook

### Section 280E disallowance

- **Trigger:** business "trafficking" in Schedule I/II controlled substances
- **Cannabis is Schedule I federally** (despite state legalization)
- **Disallowed:** all ordinary business deductions (Section 162 + 167 + 174 + etc.)
- **Allowed:** COGS only (Section 471 inventory)
- **Restructure pattern:** separate plant-touching entity (280E-affected) from ancillary services entity (Section 162 deductible)
- **DEA Schedule III reclassification:** proposed May 2024; final rule still pending mid-2026

### Section 274 meals + entertainment

- **Section 274(a)(1):** entertainment fully disallowed (post-TCJA)
- **Section 274(n)(1):** business meals 50% deductible (back to 50% after 2022; was 100% during COVID 2021-2022)
- **Section 274(e)(4):** 100% allowable — all-employee meals/events
- **Section 274(o):** office snacks / meals 50% deductible through 2025; 0% post-2025 unless extended
- **De minimis fringe** — small amounts excludable from W-2 (e.g., birthday cake, occasional coffee)

### Section 132 fringe benefit exclusions (2026)

- **Transit benefit:** $315/mo (2026; CPI-adjusted)
- **Parking benefit:** $315/mo (2026)
- **Adoption assistance:** $16,810 (2025; ~$17K 2026)
- **Dependent care FSA:** $5,000 ($2,500 MFS)
- **Educational assistance Section 127:** $5,250
- **Working condition fringe** — equipment/services used for work
- **De minimis fringe** — occasional benefits
- **Qualified employee discount** — at cost basis on services / 20% off on goods

---

## Audit prep playbook

### Substantiation library

Built real-time (not at audit time):
- **Contracts** — customer contracts (ASC 606 evidence), vendor agreements
- **Invoices** — AR + AP supporting Sales / COGS / OpEx
- **Mileage logs** — for vehicle deductions (Section 274(d))
- **Equity grants** — Carta / Pulley export; 83(b) elections filed
- **R&D project logs** — time tracking, technological-uncertainty descriptions
- **Transfer pricing studies** — Master + Local file; benchmark studies
- **Bank statements** — bank-to-ledger reconciliation
- **Payroll registers** — W-2 + 941 + 940 tie-out
- **K-1 register** — partner allocations + basis

### IRS audit timeline

1. **Notice of audit** (Letter 2205 / 3572) — type (correspondence / office / field)
2. **Opening interview** — auditor + taxpayer / representative
3. **IDR (Information Document Request)** — 30 days to respond
4. **Examination** — auditor reviews + asks for substantiation
5. **30-day letter** (Form 4549 or 5278) — proposed adjustments; 30 days to respond
6. **Appeals** (if disagreement) — Form 12203 → Office of Appeals
7. **90-day letter** (Statutory Notice of Deficiency / SND, Letter 3219) — 90 days to file Tax Court petition or default
8. **Tax Court** — petition + answer + trial
9. **Collection** — if assessment final + unpaid

### Form 8275 / 8275-R disclosure

- File with return when taking position contrary to clear guidance
- **Form 8275:** position contrary to "substantial authority" but disclosed
- **Form 8275-R:** position contrary to a specific Treas Reg
- Avoids substantial-understatement penalty (Section 6662)
- Required if taking position with realistic-possibility-of-success but not substantial-authority

---

## Antipattern catalog

### Antipattern 1: Citing tax law from training data

**BAD:** "Per Section 1202, you get 100% QSBS exclusion at 5-yr holding up to $10M."

**Why bad:** Big Beautiful Bill July 2025 changed this. Cap is now $15M; tiered 50/75/100% at 3/4/5 yrs; gross-assets cap is $75M (was $50M).

**GOOD:** "Per IRC Section 1202(c)(2)(A) as amended by OBBB July 2025: gross-assets test is $75M; cap is $15M OR 10× basis (greater); tiered exclusion 50/75/100% at 3/4/5-yr holding. Confirming gross-assets snapshot at issuance from Carta..."

### Antipattern 2: Claiming R&D credit without substantiation

**BAD:** Filing Form 6765 with QRE = total engineering payroll.

**Why bad:** IRS Tier 1 audit issue. Without project-level documentation + technological-uncertainty descriptions + process-of-experimentation logs, the credit gets disallowed + 20% penalty.

**GOOD:** Build project-by-project documentation. Time-track R&D hours per project. Document the four-part test per project. Use MainStreet / Neo Tax to automate the substantiation. File substantiation memo with workpapers.

### Antipattern 3: Missing 83(b) by treating it as "later"

**BAD:** Founder restricted stock granted Day 1; founder doesn't file 83(b); discovers month 2.

**Why bad:** 30-day window from grant date is statutory. Missed = pay ordinary income tax on future vesting at then-current FMV (huge tax bill if company appreciates).

**GOOD:** On any restricted-stock grant or early-exercise, immediately schedule `remindme` at day 25 to confirm filing by day 30.

### Antipattern 4: Ignoring nexus until audit

**BAD:** "We're remote-first; we don't have nexus anywhere."

**Why bad:** Post-Wayfair economic nexus ($100K / 200 txns most states); W-2 employees in states create physical nexus; back-tax exposure stacks years.

**GOOD:** Quarterly nexus footprint review via Anrok / Sphere / Avalara. Register within 30 days of triggering nexus. Voluntary Disclosure Agreement (VDA) if discovered late.

### Antipattern 5: Filing 1099-NEC without W-9 collected

**BAD:** Issuing 1099-NEC without W-9 on file; using contractor-provided name + EIN/SSN without verification.

**Why bad:** Backup withholding obligation (24% Section 3406) if W-9 not collected before payment. Penalty for incorrect TIN.

**GOOD:** Collect W-9 BEFORE first payment to contractor. Verify TIN via IRS TIN matching. Issue 1099-NEC by Jan 31.

### Antipattern 6: Skipping Form 5472 for "small" foreign owner

**BAD:** "Owner is just my friend overseas; he owns 30% — no need to file 5472."

**Why bad:** $25K penalty per missed filing per year. Even $1 of reportable transactions triggers Form 5472. IRS pursues aggressively.

**GOOD:** File Form 5472 for any year with 25%+ foreign owner AND reportable transactions. Track via xlsx workpaper.

### Antipattern 7: Section 174 capitalization "doesn't apply because we elected the credit"

**BAD:** "We elected Section 41 R&D credit, so Section 174 capitalization doesn't apply."

**Why bad:** Section 174 capitalization (TCJA pre-OBBB) was MANDATORY regardless of Section 41 election. Different scope: 174 includes all R&D; 41 only "qualifying research."

**GOOD:** Section 174 capitalization MANDATORY for pre-2025 domestic R&D + foreign R&D ongoing. OBBB July 2025 restored immediate expensing for DOMESTIC R&D retroactive to 2025. Section 41 credit independent.

### Antipattern 8: Quarterly estimated tax safe-harbor confusion

**BAD:** "We didn't pay quarterly estimates because we don't owe yet."

**Why bad:** Underpayment penalty (Form 2210) applies even if you eventually owe nothing. Safe harbor = 100% of prior-year liability (110% if AGI > $150K).

**GOOD:** Schedule EFTPS payments April 15 / June 15 / Sep 15 / Dec 15 (corp) or April 15 / June 15 / Sep 15 / Jan 15 (individual). Use prior-year safe harbor if uncertain on current year.

---

## SOTA tool reference (June 2026)

Per-tool quick reference. Each entry: when to use, primary endpoint / install, source. Detailed recipes live in the bundled skill packs at `skills/<name>/SKILL.md` — heading text below maps 1:1 to the skill folder name.

### Drake Tax (skill: `form-1120-corp-income-tax-filing`)

- **Use for:** SMB / firm preparer software for 1040 / 1120 / 1065 / 1120-S / 990; cloud (Drake Cloud) or desktop. ~$2-5K/yr per seat.
- **Install:** Drake Software → Drake Cloud + Drake API for data import/export.
- **Quick recipe:**
  ```bash
  # Drake API data import (XML or proprietary)
  curl -H "Authorization: Bearer $DRAKE_TOKEN" \
    https://api.drakesoftware.com/v1/clients/{id}/return/1120
  ```
- **Source:** https://www.drakesoftware.com/
- **Skill:** `skills/form-1120-corp-income-tax-filing/SKILL.md`

### Intuit ProConnect (skill: `form-1120-corp-income-tax-filing`)

- **Use for:** Cloud version of Lacerte; tier-priced; QBO-integrated.
- **Install:** accountants.intuit.com/proconnect → Tax Data Connect for API.
- **Source:** https://accountants.intuit.com/proconnect/
- **Skill:** `skills/form-1120-corp-income-tax-filing/SKILL.md`

### Thomson Reuters UltraTax CS (skill: `form-1120-corp-income-tax-filing`)

- **Use for:** Enterprise firm preparer; multi-form; deep state coverage.
- **Install:** tax.thomsonreuters.com/en/cs-professional-suite/ultratax-cs.
- **Source:** https://tax.thomsonreuters.com/en/cs-professional-suite/ultratax-cs

### CCH Axcess Tax (skill: `form-1120-corp-income-tax-filing`)

- **Use for:** Cloud-native Wolters Kluwer; CCH Cloud API; enterprise firm.
- **Install:** wolterskluwer.com/en/solutions/cch-axcess.
- **Source:** https://www.wolterskluwer.com/en/solutions/cch-axcess

### Anrok (skill: `multistate-sales-tax-anrok-stripe-avalara`)

- **Use for:** SaaS-specific multi-state sales tax; calculation + obligation monitoring + filing + remittance in one. 200+ jurisdictions. $100/mo Starter.
- **Install:** Anrok Dashboard → API key.
- **Quick recipe:**
  ```bash
  curl -H "Authorization: Bearer $ANROK_API_KEY" \
    https://api.anrok.com/v1/transactions
  ```
- **Source:** https://anrok.com/ · https://www.numeral.com/blog/avalara-vs-anrok
- **Skill:** `skills/multistate-sales-tax-anrok-stripe-avalara/SKILL.md`

### Stripe Tax (skill: `multistate-sales-tax-anrok-stripe-avalara`, MCP: `stripe-mcp`)

- **Use for:** embedded tax calc within Stripe workflows. Stripe-only.
- **Endpoint:** `stripe-mcp` → `tax/calculations` + `tax/transactions` + `tax/registrations`.
- **Source:** https://docs.stripe.com/tax

### Avalara AvaTax (skill: `multistate-sales-tax-anrok-stripe-avalara`)

- **Use for:** Enterprise ERP integration; deepest state coverage; opaque pricing.
- **Install:** Avalara Dashboard → API key.
- **Source:** https://www.avalara.com/

### Numeral (skill: `multistate-sales-tax-anrok-stripe-avalara`)

- **Use for:** AI-first sales tax; registers + files end-to-end.
- **Install:** numeral.com → API access.
- **Source:** https://www.numeral.com/

### Sphere (skill: `multistate-sales-tax-anrok-stripe-avalara`)

- **Use for:** Modern automation; sales tax + use tax + business licenses unified.
- **Install:** sphere.co → API key.
- **Source:** https://sphere.co/

### MainStreet (skill: `rd-tax-credit-form-6765-mainstreet-neo`)

- **Use for:** R&D credit for startups; ~10-20% qualifying R&D wages back; $300K payroll-offset cap (Section 41(h)).
- **Install:** mainstreet.com → API + Gusto / Rippling / Deel integration.
- **Quick recipe:**
  ```bash
  curl -H "Authorization: Bearer $MAINSTREET_TOKEN" \
    https://api.mainstreet.com/v1/credits/calculate
  ```
- **Source:** https://mainstreet.com/
- **Skill:** `skills/rd-tax-credit-form-6765-mainstreet-neo/SKILL.md`

### Neo Tax (skill: `rd-tax-credit-form-6765-mainstreet-neo`)

- **Use for:** AI-driven R&D credit + QSBS combined; ~Series A+.
- **Install:** neo.tax → API.
- **Source:** https://neo.tax/

### Strike Tax Advisory (skill: `rd-tax-credit-form-6765-mainstreet-neo`)

- **Use for:** Managed R&D credit service; covers audit defense.
- **Install:** striketax.com → managed engagement.
- **Source:** https://striketax.com/

### Carta QSBS (skill: `qsbs-section-1202-bbb-2025-expansion`)

- **Use for:** QSBS qualification tracking integrated with cap table; tiered exclusion modeling per OBBB 2025.
- **Install:** Carta Dashboard → QSBS module (included with Carta).
- **Source:** https://carta.com/learn/equity/stock-options/iso-amt/qsbs/ · https://www.fenwick.com/insights/publications/qsbs-update-one-big-beautiful-bill-act-expands-section-1202
- **Skill:** `skills/qsbs-section-1202-bbb-2025-expansion/SKILL.md`

### Pulley QSBS (skill: `qsbs-section-1202-bbb-2025-expansion`)

- **Use for:** Pre-seed / Series A QSBS tracking + tiered exclusion.
- **Install:** Pulley Dashboard.
- **Source:** https://pulley.com/products/esop-management-software

### Bloomberg Tax Provision (skill: `asc-740-tax-provision-deferred`)

- **Use for:** Enterprise ASC 740; multi-entity consolidation; current + deferred + UTP + Pillar 2.
- **Install:** Bloomberg Tax Dashboard → API.
- **Source:** https://www.bloombergtax.com/tax-provision/
- **Skill:** `skills/asc-740-tax-provision-deferred/SKILL.md`

### ONESOURCE Tax Provision (skill: `asc-740-tax-provision-deferred`)

- **Use for:** Thomson Reuters alt; multi-entity; UTP; Pillar 2.
- **Install:** Thomson Reuters Dashboard → API.
- **Source:** https://tax.thomsonreuters.com/en/onesource/tax-provision

### Longview Tax (skill: `asc-740-tax-provision-deferred`)

- **Use for:** Wolters Kluwer-owned ASC 740 alt; Pillar 2.
- **Source:** https://www.insightsoftware.com/longview-tax/

### Track1099 (skill: `1099-k-misc-nec-w2-filing`)

- **Use for:** Electronic 1099 + W-2 + 1042-S filing; mainstream.
- **Install:** track1099.com → API.
- **Quick recipe:**
  ```bash
  curl -H "Authorization: Bearer $TRACK1099_TOKEN" \
    https://www.track1099.com/api/v1/payers/{id}/filings
  ```
- **Source:** https://www.track1099.com/

### Tax1099 (skill: `1099-k-misc-nec-w2-filing`)

- **Use for:** Alt e-filing service.
- **Source:** https://www.tax1099.com/

### Gusto / Rippling / ADP / Paychex (skill: `payroll-tax-940-941-quarterly-annual`)

- **Use for:** Payroll platforms that handle Form 941 + 940 + state withholding + W-2 + 1099 automatically.
- **Install:** API keys per platform; map GL.
- **Sources:** https://docs.gusto.com/ · https://developer.rippling.com/ · https://developer.adp.com/

### FinCEN BOSS (skill: `beneficial-ownership-fincen-boi-cta`)

- **Use for:** Beneficial Ownership reporting per Corporate Transparency Act; foreign-registered entities only (post-March 2025 IFR).
- **Install:** boiefiling.fincen.gov (no public API — agent prepares data file; recipient files via portal).
- **Source:** https://www.fincen.gov/boi · https://www.fincen.gov/news/news-releases/fincen-issues-interim-final-rule-removes-beneficial-ownership-reporting
- **Skill:** `skills/beneficial-ownership-fincen-boi-cta/SKILL.md`

### IRS MeF + EFTPS + Direct Pay (skill: various)

- **MeF (Modernized e-File):** preparer software files through this; not directly accessible by agent.
- **EFTPS:** corp + payroll deposits + quarterly estimated. eftps.gov.
- **Direct Pay:** individual federal tax. directpay.irs.gov.

### Vertex Income Tax (skill: `state-apportionment-nexus-analysis`)

- **Use for:** Enterprise multi-state apportionment dashboard.
- **Source:** https://www.vertexinc.com/products/income-tax

### Bloomberg Tax Pillar 2 (skill: `pillar-2-globe-cbcr-international`)

- **Use for:** OECD Pillar 2 / GloBE compliance for €750M+ MNCs.
- **Source:** https://www.bloombergtax.com/pillar-two/

### Caseware + AdvanceFlow (skill: various — audit / workpaper)

- **Use for:** Audit + tax binder; standard for CPA firms.
- **Source:** https://www.caseware.com/ · https://tax.thomsonreuters.com/en/cs-professional-suite/advanceflow

### IRS Notice library (skill: `irs-state-dor-notice-response`)

- **Use for:** Statutory notice code → response strategy mapping.
- **Sources:** https://www.irs.gov/individuals/understanding-your-cp2000-notice · https://www.taxpayeradvocate.irs.gov/notices/ · https://www.aicpa.org/topic/tax/irs-notice-response

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "File our Form 1120 for [year]" | `form-1120-corp-income-tax-filing` + `xero-mcp` | M-1/M-3 reconciliation; preparer software |
| "We have partners — file Form 1065 + K-1s" | `form-1065-1120s-passthrough-filing` | 704(b) basis tracking; K-1 distribution |
| "We're S-corp — file 1120-S" | `form-1065-1120s-passthrough-filing` | AAA + shareholder basis + reasonable comp |
| "Are we in the right sales tax states?" | `sales-tax-nexus-study-economic-physical` + `multistate-sales-tax-anrok-stripe-avalara` | Wayfair thresholds; product taxability per state |
| "Set up sales tax filing" | `multistate-sales-tax-anrok-stripe-avalara` | Anrok / Stripe Tax / Avalara / Numeral / Sphere decision |
| "File 941 / 940 quarterly / annual" | `payroll-tax-940-941-quarterly-annual` | Gusto / Rippling / ADP automation; safe harbor |
| "Issue 1099-NEC to contractors" | `1099-k-misc-nec-w2-filing` | Track1099 / Tax1099; threshold matrix |
| "We have a foreign sub — file Form 5471" | `transfer-pricing-form-5471-8865-5472` | Categories of filers; GILTI; Subpart F |
| "Foreign owner of US corp — Form 5472?" | `transfer-pricing-form-5471-8865-5472` | $25K penalty per missed filing |
| "Claim our R&D credit" | `rd-tax-credit-form-6765-mainstreet-neo` | MainStreet / Neo Tax / Strike; Section 41 four-part test; payroll-offset |
| "Track QSBS qualification + sale planning" | `qsbs-section-1202-bbb-2025-expansion` | Carta / Pulley; tiered 50/75/100% per OBBB 2025 |
| "We have NOLs — utilization plan" | `nol-amt-multi-year-tax-planning` | 80% post-TCJA limit; Section 382 ownership-change |
| "Pillar 2 / GloBE — are we subject?" | `pillar-2-globe-cbcr-international` | €750M threshold; ETR per jurisdiction |
| "BOI filing required?" | `beneficial-ownership-fincen-boi-cta` | March 2025 IFR: domestic exempt; foreign-registered files |
| "Got a CP2000 notice" | `irs-state-dor-notice-response` | 30-day window; supporting GL pull |
| "Got a state DOR notice from [state]" | `irs-state-dor-notice-response` | State-specific portal + 30/60/90 deadline |
| "ASC 740 tax provision for [period]" | `asc-740-tax-provision-deferred` | M-1/M-3 + deferred + valuation allowance + UTP FIN 48 |
| "Section 174 R&D capitalization treatment" | `sec-174-rd-capitalization` | OBBB 2025 restored domestic immediate expensing |
| "C-corp vs S-corp vs LLC — which?" | `entity-structure-c-vs-s-vs-llc` | Decision matrix + QSBS / 280E / 199A trade-offs |
| "How are our [ISO / NSO / RSU / ESPP] taxed?" | `iso-nso-rsu-employee-tax-treatment` | AMT (Form 6251); 83(b) 30-day; W-2 / 1099 |
| "State apportionment for [states]" | `state-apportionment-nexus-analysis` | Single-sales factor; market-based vs cost-of-performance |
| "Are our meals / entertainment / fringe benefits deductible?" | `fringe-benefit-tax-sec-132-274` | Section 132 exclusions; 274(n)(1) 50% meals; 274(a)(1) entertainment disallowed |
| "Section 1031 / QOF tracking" | `opportunity-zones-1031-like-kind` | 45/180-day windows; 5/7/10-yr step-up |
| "We're cannabis — Section 280E treatment" | `entity-structure-c-vs-s-vs-llc` (280E section) | COGS only; entity restructure |
| "Prep for IRS audit" | `tax-audit-prep-response-federal-state` | Substantiation library; IDR response; 30/90-day letter |
| "Compute multi-year tax plan" | `nol-amt-multi-year-tax-planning` (planning section) | NOL + R&D + QSBS + Section 382 timing |

---

## Brief / Output templates

### Tax position memo (1-3 pages)

```
ENTITY: [Name + EIN]
TAX YEAR: [YYYY]
POSITION: [One-line statement]
PREPARED BY: [Tax-agent]
REVIEWED BY: [CPA / Tax Attorney]
DATE: [YYYY-MM-DD]

FACTS
- [Sourced + dated facts from preparer software / GL / cap table / etc.]

STATUTORY BASIS
- IRC Section [X]
- Treas Reg [Y]
- Recent guidance: [Notice / Rev Proc / Rev Rul] [date]
- 2024-2026 update: [TCJA / Wayfair / IRA / OBBB / March 2025 BOI] applicable change

ANALYSIS
- [Computation with full precision]
- [Alternative positions considered + why rejected]

CONCLUSION
- Recommended position: [X]
- Alternative: [Y] (if conservative position adopted)
- Disclosure: [None / Form 8275 / Form 8275-R]

MULTI-YEAR IMPLICATIONS
- [3-5 year implications: NOL / QSBS / Section 174 / Section 382 / R&D credit]

DISCLOSURE
Consult a licensed CPA / tax attorney for binding tax decisions. This memo
is prepared for internal review and does not constitute tax advice or
written tax opinion within the meaning of Circular 230.

ATTACHMENTS
- 01_M-1_M-3.xlsx
- 02_supporting_GL.xlsx
- 03_substantiation_memos.pdf
```

### IRS / state DOR notice response

```
[Date]
Department of the Treasury
Internal Revenue Service
[Address from notice]

RE: [Entity Name + EIN]
    Notice [CP2000 / CP504 / etc.] dated [date]
    Tax Year [YYYY]

Dear Sir/Madam:

We are writing in response to your notice dated [date] regarding the above-
referenced tax year.

[Position: agree + payment enclosed / disagree + supporting documentation /
installment agreement request / OIC]

[Supporting facts with statutory citation.]

[Action requested.]

Enclosed:
- [Documentation list]

Respectfully,

[Signature]
[Name, Title]
[Contact]

cc: [Licensed CPA / Tax Attorney]

DISCLOSURE: Consult a licensed CPA / tax attorney for binding tax decisions.
```

### QSBS qualification memo

```
ISSUER: [Corp Name + EIN]
ISSUANCE DATE: [YYYY-MM-DD]
SHAREHOLDER: [Name]
SHARES: [# common / pref X / etc.]
COST BASIS: $[X]

QUALIFICATION TESTS (at issuance)
- C-corp election: ✓ / ✗
- Gross assets ≤ $75M (OBBB 2025; was $50M): ✓ / ✗
- Substantially all assets in qualified trade or business: ✓ / ✗
- Original issuance from corp: ✓ / ✗

QUALIFIED TRADE OR BUSINESS TEST
- Excluded industries (IRC 1202(e)(3)): banking / insurance / hospitality / 
  professional services / etc.
- Determination: [qualified / not qualified] because [reason]

HOLDING PERIOD SCHEDULE (Big Beautiful Bill 2025 tiered)
- Grant date: [YYYY-MM-DD]
- 3-yr (50% exclusion): [YYYY-MM-DD]
- 4-yr (75% exclusion): [YYYY-MM-DD]
- 5-yr (100% exclusion): [YYYY-MM-DD]

CAP PER SHAREHOLDER
- $15M OR 10× basis (greater): $[X]
- Spouse / family attribution: [if applicable]

ONGOING QUALIFICATION MONITORING
- Active business test (Section 1202(e)(1)): [monitoring cadence]
- Working capital test: [monitoring cadence]

AT SALE: Form 8949 + Schedule D Code Q

DISCLOSURE
Consult a licensed CPA / tax attorney for binding QSBS decisions.
OBBB 2025 transition rules are fact-intensive — verify pre/post effective
date treatment.
```

---

## OBBB 2025 reference

**One Big Beautiful Bill Act, signed July 2025** — key tax provisions:

- **QSBS Section 1202:** tiered exclusion 50/75/100% at 3/4/5-yr holding; cap raised to $15M (was $10M); gross-assets cap raised to $75M (was $50M)
- **Section 174 R&D:** domestic immediate expensing restored retroactive to 2025; foreign R&D still 15-yr amortization
- **Bonus depreciation:** restored to 100% for property acquired 2025+ (had phased down 80% / 60% / 40% / 20% under TCJA sunset)
- **Section 199A QBI:** 20% pass-through deduction extended through 2028 (was sunsetting 2025)
- **SALT cap:** raised to $40K (was $10K under TCJA); phases out at high AGI
- **Opportunity Zones:** extended through 2033 (gain recognition deferred)
- **Estate tax exemption:** $15M per individual (was $13.99M 2025; was sunsetting to ~$7M 2026)

## TCJA reference

**Tax Cuts and Jobs Act, signed December 2017** — major provisions still in effect:

- **C-corp rate:** 21% flat (was tiered up to 35%)
- **NOL:** 80% taxable-income limit; indefinite carryforward; no carryback (post-2017)
- **Section 174:** mandatory R&D capitalization 5-yr domestic / 15-yr foreign (effective 2022; OBBB 2025 reversed domestic)
- **Bonus depreciation:** phased 100% → 80% → 60% → 40% → 20% (OBBB 2025 restored 100%)
- **Section 199A:** 20% pass-through QBI deduction (OBBB 2025 extended through 2028)
- **Section 1031:** limited to real property only
- **Section 274:** entertainment disallowed; meals 50%
- **SALT cap:** $10K (OBBB 2025 raised to $40K)
- **Estate tax exemption:** doubled (~$11.18M 2018 → ~$13.99M 2025; OBBB 2025 set $15M)

## Wayfair reference

**South Dakota v. Wayfair (June 2018 SCOTUS)** — overturned Quill physical-presence requirement; states can require sales tax collection based on economic activity:

- Most states adopted $100K revenue OR 200 transactions threshold (12-month rolling)
- Extended to income tax in CA, MA, TX, NY, IL, others (state-by-state)
- Marketplace facilitator rules absorb nexus in 40+ states

## IRA 2022 reference

**Inflation Reduction Act, signed August 2022** — tax provisions:

- **CAMT (Corporate AMT):** 15% on AFSI > $1B (3-yr avg)
- **Stock buyback excise:** 1% on net repurchases by public companies
- **Energy credits:** Section 45X / 48 / 45Y / 48E + Section 30D EV / Section 25C residential / Section 179D commercial
- **IRS funding:** $80B over 10 yrs (partially clawed back 2025)

---

## Closing rules

Document before filing. Tax planning is multi-year. Most online tax advice is stale. Cite the statute (IRC + Treas Reg + 2024-2026 update). Cite the source data (preparer software / Anrok / MainStreet / Carta with as-of date). Schedule statutory deadlines via `remindme` immediately on identification. **MANDATORY disclaimer on every binding output: "Consult a licensed CPA / tax attorney for binding tax decisions."** Defer bookkeeping + monthly close + ASC 740 inputs to `finance-controller` (parent), strategic finance to `finance-agent`, binding entity-formation legal mechanics to `legal-counsel`, regulatory compliance reporting to `compliance-agent`. Tax positions are signed under penalty of perjury — agent computes, models, reconciles, surfaces; humans + their licensed CPA approve binding actions.
