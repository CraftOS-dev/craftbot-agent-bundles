# Tax Agent — Use Cases

**Tier:** specialized · **Category:** finance / tax
**Core job:** Operational tax preparer — federal / state / multi-jurisdiction corp + payroll + sales/use tax filings, R&D credits, QSBS, transfer pricing, Pillar 2 / BEPS, IRS notice response, ASC 740 provision.

> Ships with the SOTA 2026 operational tax stack — Drake / ProConnect / UltraTax / CCH Axcess for Forms 1120 / 1065 / 1120-S; Anrok / Stripe Tax / Avalara / Numeral / Sphere for multi-state sales tax; Gusto / Rippling / ADP / Paychex for payroll tax (941 / 940); Track1099 / Tax1099 for 1099 family; MainStreet / Neo Tax / Strike Tax for R&D credit (Form 6765); Carta QSBS / Pulley / TrueQSBS for Section 1202 (incl. Big Beautiful Bill 2025 tiered exclusion 50/75/100%); Bloomberg Tax Provision / ONESOURCE / Longview for ASC 740; OECD Pillar 2 / GloBE tools for €750M+ MNCs; FinCEN BOSS for BOI; IRS notice library + state DOR portals for notice response. Sits under `finance-controller` (parent — bookkeeping + monthly close + ASC 740 inputs) and adjacent to `finance-agent` (strategic finance), `legal-counsel` (entity formation legal mechanics), `compliance-agent` (regulatory reporting). **MANDATORY disclaimer:** every binding tax output includes "Consult a licensed CPA / tax attorney for binding tax decisions" — humans + a licensed practitioner approve binding tax filings; the agent computes, models, reconciles, drafts, and surfaces.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Federal corporate income tax — filing surface

- Form 1120 (C-corp income tax filing)
- Form 1065 (partnership return + K-1 distribution)
- Form 1120-S (S-corp return + AAA + shareholder basis tracking)
- Schedule M-1 / M-3 book-to-tax reconciliation
- Schedule K-1 / K-2 / K-3 (international items for partners)
- Schedule UTP (Uncertain Tax Positions) for >$10M assets
- Form 7004 extension filings

### State + local corporate income tax

- Multi-state income tax filings (single-sales factor vs three-factor apportionment)
- Market-based sourcing vs cost-of-performance for services
- Throwback / throwout rules per state
- State nexus determinations (post-Wayfair extended to income tax: CA $735K / NY $1.27M / MA $500K / TX $500K / WA $100K)

### Payroll tax

- Form 941 (quarterly federal payroll tax)
- Form 940 (annual FUTA)
- Form 944 (annual alt for small employer)
- State income tax withholding (CA EDD, NY DTF, etc.)
- State unemployment (SUTA) per state experience rating
- State disability (CA SDI, NJ SDI, NY SDI, RI TDI, HI TDI)
- Local taxes (NYC, Yonkers, PA local, OH local)
- Quarterly estimated tax (Form 1120-W corp; Form 1040-ES individual)
- EFTPS deposit scheduling

### 1099 family + W-2

- Form 1099-NEC (contractor payments ≥$600)
- Form 1099-MISC
- Form 1099-K (marketplace / payment-processor; 2024 $5K → 2025 $2.5K → 2026 $600)
- Form 1099-DIV / INT / B (dividends, interest, broker)
- Form 1042-S (foreign person US-source income; 30% default withholding)
- Form W-2 + W-3
- E-filing mandate (10+ forms total, 2024+)

### Multi-state sales tax + use tax

- Anrok (SaaS-specific multi-state)
- Stripe Tax (embedded; Stripe-only)
- Avalara AvaTax (enterprise)
- TaxJar (e-commerce; Stripe-owned)
- Numeral (AI-first)
- Sphere (sales + use + business licenses)
- Quaderno / Vertex (alts)
- Sales tax nexus study (economic post-Wayfair + physical + marketplace facilitator)
- Use tax compliance (self-assessed on out-of-state purchases)
- SaaS taxability per jurisdiction (NY/PA/TX/WA tax SaaS; CA/FL/NV/MO don't)
- Sales tax audit response

### International tax + transfer pricing

- Form 5471 (CFC reporting — 10%+ US ownership of foreign corp)
- Form 8865 (foreign partnership reporting)
- Form 5472 (foreign-owned US corp reportable transactions — $25K penalty per missed)
- Form 1118 (foreign tax credit — corp)
- Form 1116 (foreign tax credit — individual)
- GILTI / Subpart F income inclusion
- Transfer pricing studies (OECD three-tier: Master + Local + CbCR)
- TP methods: CUP / Resale Price / Cost Plus / TNMM / Profit Split
- FAR (Functions / Assets / Risks) analysis
- Cost-sharing arrangements (Treas Reg 1.482-7)
- Section 482 + Treas Reg 1.482-7

### Pillar 2 / GloBE / CbCR (only triggers at €750M+ MNCs)

- Income Inclusion Rule (IIR)
- Undertaxed Profit Rule (UTPR)
- Qualified Domestic Minimum Top-up Tax (QDMTT)
- ETR computation per jurisdiction
- Top-up tax calculation
- Country-by-Country Reporting (Form 8975 US)

### Beneficial Ownership (CTA / BOI)

- FinCEN BOI report preparation
- BOSS portal data file format
- Domestic exemption (March 2025 interim final rule)
- Foreign-registered entity filing (still required)
- 30-day update window on BO info changes

### R&D tax credit (Form 6765)

- MainStreet / Neo Tax / Strike Tax / TaxRobot integration
- Section 41 four-part test substantiation
- QRE (Qualified Research Expenses) allocation: wages / contract research (65%) / supplies / cloud
- Regular method vs Alternative Simplified Credit (ASC) method
- Payroll-offset election (Section 41(h)) for startups <$5M revenue + Form 8974
- State R&D credits (CA, MA, TX, NY, etc.)
- Substantiation memo (IRS Tier 1 audit issue)

### Section 174 R&D capitalization

- TCJA 2017 mandatory capitalization (5-yr domestic; 15-yr foreign)
- Big Beautiful Bill 2025 reversal — domestic immediate expensing restored retroactive to 2025
- Pre-2025 amortization waterfall continued
- Section 174 vs Section 41 scope difference

### QSBS Section 1202 (incl. Big Beautiful Bill 2025 expansion)

- Carta QSBS / Pulley / TrueQSBS qualification tracking
- C-corp + gross-assets ≤ $75M (was $50M pre-OBBB) qualification at issuance
- Qualified trade or business test (IRC 1202(e)(3))
- OBBB 2025 tiered exclusion: 3-yr 50% / 4-yr 75% / 5-yr 100%
- Per-shareholder $15M cap (was $10M) OR 10× basis (greater)
- Form 8949 (Code Q) + Schedule D at sale

### NOL + Section 382 + CAMT

- NOL waterfall by tax year of origination
- Post-TCJA 80% taxable-income limit; indefinite carryforward
- Section 382 ownership-change limit (>50% change in 3-yr testing period)
- 5% shareholder grouping rules
- CAMT (Corporate AMT) 15% on AFSI > $1B post-IRA 2022 (Form 4626)
- Pre-2018 NOL legacy rules

### Equity comp tax — ISO / NSO / RSU / ESPP + 83(b)

- ISO mechanics ($100K AMT rule; 1-yr post-exercise + 2-yr post-grant for LTCG; 90-day post-termination exercise)
- NSO ordinary income at exercise
- RSU ordinary income at vest
- ESPP qualifying vs disqualifying disposition
- AMT bargain element (Form 6251)
- Form 3921 (ISO exercise)
- 83(b) election — 30-day window for restricted stock + early-exercise
- Section 409A penalty avoidance

### Fringe benefit tax — Section 132 + Section 274

- Section 132 exclusions: transit $315/mo + parking $315/mo 2026; adoption $16,810; dependent-care FSA $5,000; educational assistance $5,250
- Section 274(n)(1) 50% meal limit
- Section 274(a)(1) entertainment disallowance
- Section 274(e)(4) 100% all-employee events
- De minimis fringe (occasional benefits)
- Qualified employee discount

### Opportunity Zones + Section 1031

- Section 1400Z QOF — 180-day investment window from gain
- 5/7/10-yr step-up tiers
- Form 8997 annual QOF reporting
- OBBB 2025 extension through 2033
- Section 1031 like-kind exchange (real property only post-TCJA)
- 45-day identification window + 180-day closing window
- Qualified Intermediary requirement
- Form 8824 exchange reporting

### Section 280E — cannabis disallowance

- Plant-touching entity vs ancillary services entity separation
- COGS-only deduction allowed (Section 471 inventory)
- DEA Schedule III reclassification status (still pending mid-2026)
- Section 199A QBI interaction

### Entity structure analysis (C-corp / S-corp / LLC / partnership)

- Decision matrix per criteria: capital plans, shareholder profile, tax treatment, QSBS, SE tax, state recognition
- Multi-year ETR scenarios per structure
- Section 199A QBI (pass-through; sunsets 2028 post-OBBB)
- Section 1202 QSBS (C-corp only)
- Section 280E (cannabis Section 471 only)
- Form 2553 (S-corp election); Form 8832 (entity classification)

### State apportionment + nexus analysis

- Single-sales factor (most states 2025-2026)
- Three-factor apportionment (AK, HI, MA, MT, NM, FL, etc.)
- Market-based sourcing vs cost-of-performance for services
- Throwback / throwout rules
- State income tax economic nexus thresholds post-Wayfair

### IRS + state DOR notice response

- CP2000 (underreporter) — 30 days
- CP501 / CP503 (balance due reminders) — 21 days
- CP504 (intent to levy state refund) — 30 days URGENT
- CP90 / Letter 1058 (Final Notice of Intent to Levy — FNTL) — 30 days URGENT
- CP523 (installment default) — 30 days
- Letter 3219 (Statutory Notice of Deficiency — 90-day letter)
- Form 12203 (appeals review request)
- Form 12153 (CDP hearing request)
- Form 9465 (installment agreement)
- Form 656 (Offer in Compromise)
- Form 433-A / 433-B (Collection Information Statement)
- State DOR notice templates per state

### ASC 740 tax provision

- M-1 / M-3 book-to-tax reconciliation
- Current tax payable
- Deferred tax asset / liability per temp diff
- Valuation allowance assessment (MLTN — more-likely-than-not)
- Uncertain Tax Positions (UTP / FIN 48 / ASC 740-10)
- Effective Tax Rate (ETR) reconciliation
- Bloomberg Tax Provision / ONESOURCE / Longview integration
- Schedule UTP (Form 1120) for >$10M assets

### Multi-year tax planning

- 3-5 year multi-year tax model
- NOL utilization timing + Section 382 limit
- R&D credit carryover
- QSBS 3/4/5-yr holding tier planning
- Section 174 amortization waterfall
- Stock comp ASC 718 vs tax timing
- State nexus expansion sequencing

### Tax audit prep + response (federal + state)

- Substantiation library (contemporaneous documentation)
- IDR (Information Document Request) response
- Bloomberg Tax Audit Workpaper / Caseware audit binder
- 30-day letter → 90-day SND → Tax Court petition workflow
- Voluntary Disclosure Agreement (VDA) for late-discovered nexus
- Form 8275 / 8275-R disclosure (avoid substantial-understatement penalty)

### Quarterly estimated tax

- Form 1120-W (corp) deadlines: April 15 / June 15 / September 15 / December 15
- Form 1040-ES (individual): April 15 / June 15 / September 15 / January 15
- Safe harbor (100% prior year liability; 110% if AGI > $150K)
- Underpayment penalty (Form 2210)
- EFTPS / IRS Direct Pay scheduling

### Excise tax (Form 720 / 730 / 11-C — niche)

- Quarterly Form 720 (fuel, retail, manufacturer, communications, air transport)
- Form 11-C (wagering occupational)
- Form 730 (monthly wagering)
- Crypto exchange FinCEN MSB registration

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case above appears here as a row. Source: `reference/SOTA_USE_CASES.md`.

| Use case | SOTA mechanism | Path |
|---|---|---|
| Form 1120 (C-corp) | Drake / ProConnect / UltraTax / CCH Axcess | `cli-anything` + preparer REST + `xero-mcp` |
| Form 1065 (partnership) + K-1 | Same preparer set | `cli-anything` + preparer + pandas K-1 |
| Form 1120-S (S-corp) | Same preparer set | `cli-anything` + preparer + AAA pandas |
| Schedule M-1 / M-3 | Pandas reconciliation | `xero-mcp` + xlsx |
| State corp income + apportionment | Avalara / Vertex / Sphere + preparer | `cli-anything` + Avalara / Vertex |
| Form 941 quarterly + 940 annual | Gusto / Rippling / ADP / Paychex | `cli-anything` + payroll REST |
| State payroll + SUTA + SDI | Same payroll platforms | `cli-anything` + payroll REST |
| Quarterly estimated tax (1120-W / 1040-ES) | Form + EFTPS | `xero-mcp` + safe-harbor calc + `remindme` |
| 1099-NEC / MISC / K / W-2 | Track1099 / Tax1099 / Stripe 1099-K | `cli-anything` + Track1099 + `stripe-mcp` |
| Form 1042-S (foreign contractor) | Preparer + Track1099 | `cli-anything` + Track1099 + W-8BEN tracking |
| Multi-state sales tax | Anrok / Stripe Tax / Avalara / Numeral / Sphere | `cli-anything` + `stripe-mcp` tax |
| Sales tax nexus study | Anrok / Sphere / Avalara dashboards | `stripe-mcp` Sigma + state-threshold matrix |
| Use tax compliance | Anrok / Avalara | `xero-mcp` + Ramp/Brex via `cli-anything` |
| Sales tax audit response | Substantiation + state DOR templates | `irs-state-dor-notice-response` |
| Form 5471 (CFC) | Preparer + intl tax CPA | `cli-anything` + preparer + xlsx workpapers |
| Form 8865 (foreign partnership) | Same preparer set | `cli-anything` + preparer + xlsx |
| Form 5472 (foreign-owned US corp) | Preparer | `xero-mcp` + preparer |
| Transfer pricing studies | Bloomberg TP / ONESOURCE / EY-managed | xlsx FAR analysis + benchmark |
| GILTI / Subpart F | Preparer + xlsx | `cli-anything` + preparer |
| Pillar 2 / GloBE / CbCR (Form 8975) | Bloomberg / ONESOURCE / Longview Pillar 2 | xlsx ETR-by-jurisdiction |
| BOI / CTA (FinCEN BOSS) | FinCEN BOSS portal | Data prep + manual file via portal |
| R&D credit Form 6765 | MainStreet / Neo Tax / Strike Tax | `cli-anything` + MainStreet API + Gusto/Rippling |
| Section 41(h) payroll-offset election | Form 6765 + 8974 | Preparer + Form 8974 with 941 |
| Section 174 R&D capitalization | Preparer + xlsx waterfall | `xero-mcp` + Gusto/Rippling allocation |
| QSBS Section 1202 (OBBB 2025) | Carta QSBS / Pulley / TrueQSBS | `cli-anything` + Carta + xlsx tiered exclusion |
| NOL waterfall + Section 382 | Pandas + Bloomberg Tax Section 382 | `cli-anything` + preparer + pandas |
| CAMT (Form 4626) — only $1B+ AFSI | Preparer | `cli-anything` + preparer |
| Entity structure (C / S / LLC / partnership) | Decision matrix | xlsx scoring matrix |
| State apportionment + nexus | Avalara / Vertex / Sphere | `stripe-mcp` Sigma + HRIS pull + apportionment |
| ISO / NSO / RSU / ESPP tax | Carta / Pulley / Brilliant | `cli-anything` + Carta + Form 6251 AMT calc |
| 83(b) election (30-day window) | Paper file IRS + `remindme` | `remindme` day 25 + Carta tracker |
| Fringe benefit Section 132 / 274 | Preparer + expense category map | `xero-mcp` + Ramp/Brex categorization |
| Section 1031 like-kind (real property) | QI + Form 8824 + 45/180-day | `remindme` 45/180-day + Form 8824 |
| OZ Section 1400Z (QOF) | Form 8997 + 5/7/10-yr step-up | `remindme` deferral schedule + Form 8997 |
| Section 280E (cannabis) | Entity restructure + COGS allocation | xlsx COGS vs disallowed OpEx |
| IRS notice (CP2000 / CP504 / etc.) | TaxNotes IRS Notice Library + AICPA | `cli-anything` + pattern-match + `remindme` |
| State DOR notice | State-specific portals | Same as IRS; state deadline tracker |
| ASC 740 provision | Bloomberg / ONESOURCE / Longview / Tax Prodigy | `xero-mcp` + M-1/M-3 pandas + REST push |
| Schedule UTP (>$10M assets) | Preparer + FIN 48 documentation | Pandas UTP register |
| Multi-year tax planning | xlsx driver-based + sensitivity | `xero-mcp` + xlsx |
| Tax audit prep + response | Bloomberg Audit + Caseware | `file-organizer` + audit-ready workpapers |
| Form 8275 / 8275-R disclosure | Preparer + position memo | `cli-anything` + preparer |
| Excise tax (Form 720 / 730 / 11-C) | Preparer + EFTPS | `cli-anything` + preparer + EFTPS UI prep |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Preparer software (Drake / ProConnect / UltraTax / CCH) | ⚠ | Paid + licensed; agent prepares book-to-tax workpapers + Schedule M-1/M-3 + supporting docs; recipient files via their licensed preparer or EA / CPA. Direct e-file via IRS MeF requires preparer credentials. |
| Avalara / Vertex apportionment dashboards | ⚠ | Paid keys for full multi-state coverage; agent can compute apportionment in xlsx without them but the platforms surface jurisdiction-specific edge cases (throwback, throwout, Joyce / Finnigan, single-sales factor variants). |
| Form 5471 / 8865 / 5472 + transfer pricing | ⚠ | Require international tax CPA review per IRS guidance; agent compiles all workpapers but does NOT sign the return. TP studies require comparable databases (RoyaltyStat / RoyaltyRange — paid) for benchmark. |
| ASC 740 provision software (Bloomberg / ONESOURCE / Longview) | ⚠ | Paid; agent computes M-1/M-3 + deferred schedule in pandas and pushes via REST when key provided. |
| Pillar 2 / GloBE | ⚠ | Only triggers at €750M+ revenue (<1% of recipients); paid software at that scale. |
| Anrok / Numeral / Sphere / Avalara sales tax | ⚠ | Paid keys; Stripe Tax included if on Stripe. Recipient typically owns one platform already. |
| MainStreet / Neo Tax / Strike Tax R&D credit | ⚠ | Paid; ~$2-10K per credit claim or % of credit. Free fallback: agent prepares Form 6765 + substantiation in xlsx without managed service. |
| Carta / Pulley QSBS module | ⚠ | Included with Carta / Pulley subscription; recipient owns one or both. Standalone TrueQSBS available. |
| FinCEN BOSS portal filing | ✓ | No public API — agent prepares data file; recipient files via portal. Post-March 2025 IFR: only foreign-registered entities required. |
| 83(b) election (paper file to IRS) | ✗ | IRS requires PAPER filing by certified mail; no electronic option. Agent schedules `remindme` day 25; recipient files paper return-receipt. |
| Voluntary Disclosure Agreement (VDA) — state DOR | ⚠ | Requires state-specific application; agent drafts; recipient submits via state DOR portal. |
| Tax Court petition | ✗ | 90-day deadline from SND; petition filed by attorney admitted to Tax Court. Agent prepares facts memo; tax attorney files. |
| IRS Offer in Compromise (Form 656) | ⚠ | Agent drafts + computes per Form 433-A/B; recipient + CPA submits. |
| Binding tax filings + IRS Tax Court + state administrative hearings | ⚠ | **MANDATORY disclaimer: "Consult a licensed CPA / tax attorney for binding tax decisions."** Agent computes, models, drafts, surfaces — humans + their CPA / tax attorney approve binding actions. |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a named SOTA tool with an exact agent execution path. All ⚠ entries resolve once the recipient (a) provides their preparer software API key OR (b) hires a CPA / EA who owns the preparer software (and the agent supplies the workpapers). The two ✗ entries (83(b) paper filing, Tax Court petition) are statutorily restricted to paper / licensed-attorney filings — the agent schedules deadlines + prepares materials, but the recipient + licensed practitioner executes. The MANDATORY "consult a licensed CPA / tax attorney" disclosure is operational discipline — not a capability gap.

---

## When to use this agent

- "File our Form 1120 for tax year 2025 — we have R&D credit and Section 174 capitalization questions."
- "Are we registered for sales tax in the right states? We're a SaaS hitting $5M ARR with customers in all 50 states."
- "Got a CP2000 notice from the IRS — draft a response. Pulling our supporting GL."
- "We're considering a Section 1202 QSBS sale in Q4 — verify qualification + tiered exclusion under OBBB 2025."
- "Claim our R&D credit via MainStreet; we have a $300K eligible spend and want the payroll-offset election."
- "Foreign owner of our US corp — what's our Form 5472 exposure?"
- "Build our 2026 ASC 740 tax provision — current + deferred + valuation allowance + UTP."
- "We just hired an employee in WA — review our nexus footprint + payroll tax registration."
- "Should we elect S-corp status or stay LLC? We're at $800K revenue + 2 founders."
- "Our partnership year-end is December 31 — generate K-1s for all 5 partners."
- "Quarterly estimated tax for Q3 — compute safe harbor + schedule EFTPS deposit."
- "We're cannabis (plant-touching) — restructure to minimize Section 280E exposure."
- "ISO exercise window — compute AMT bargain element + recommend timing."
- "Got an audit notice — compile substantiation library for [tax year]."

---

## When NOT to use this agent

- **Bookkeeping + monthly close + ASC 740 close inputs** — hand off to `finance-controller` (parent). Tax-agent pulls from finance-controller's closed books; finance-controller owns the GL, accruals, and ASC 740 close-package inputs. Tax-agent owns the M-1 / M-3 tax-side reconciliation.
- **Capital allocation + multi-year strategic finance + fundraising prep + investor updates** — hand off to `finance-agent`. Tax-agent's multi-year tax model feeds the strategic finance model; finance-agent owns the capital plan.
- **Binding entity-formation legal mechanics + employment agreements + IP assignment + securities filings (Form D, etc.) + ESOP plan documents** — hand off to `legal-counsel`. Tax-agent surfaces entity-choice tax trade-offs; legal-counsel files Articles + drafts operating agreements + plan documents.
- **Regulatory compliance reporting** (SOC 2, ISO 27001, GDPR, HIPAA, PCI-DSS, BSA AML) — hand off to `compliance-agent`. Tax-agent owns tax-statutory compliance (CTA / BOI is gray area — agent owns BOI; compliance-agent owns the broader regulatory surface).
- **Sales pipeline / ARR forecast / quota planning** — hand off to `sales-agent`. Tax-agent uses ARR data as input to nexus + apportionment, not as source of truth.
- **Code-level data pulls / custom ETL into a warehouse for tax workpapers** — hand off to `senior-python-engineer`. Tax-agent designs the SQL; engineer builds the pipeline.
- **Marketing attribution / paid-channel ROI** — hand off to `marketing-agent`. Not tax-agent's domain.
- **Personal income tax / individual 1040 / personal investment tax planning** — out of scope for the operational corp tax surface. Agent will handle 1042-S for foreign contractors and Form 6251 (AMT individual) for ISO exercise, but personal-finance tax planning is not this agent's job.
- **Binding tax filings + IRS Tax Court petitions + state administrative hearings + Offer in Compromise binding negotiation** — defer to a licensed CPA / tax attorney. **MANDATORY disclaimer.** Agent computes, models, drafts, surfaces — humans + their CPA / tax attorney approve binding actions.
- **State-specific aggressive tax positions** (e.g., domicile change, charitable trust, etc.) — defer to a licensed CPA / state-and-local-tax specialist. Agent flags the position + drafts a research memo + schedules disclosure (Form 8275 / 8275-R if applicable); recipient + CPA approve.
