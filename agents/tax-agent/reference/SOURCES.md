# Tax Agent — Sources

Section-to-source map for `soul.md` and `role.md`. This file ships in the bundle but is **not** loaded into the agent's context — it exists for humans verifying provenance and for future refreshes.

The per-use-case SOTA mapping with confidence flags is at `reference/SOTA_USE_CASES.md`. URLs in `agent.yaml → sources` and the per-tool table below.

The v1 build did not download upstream agent reference files into `reference/agents/` (no dedicated `tax-agent` / `tax-preparer` / `tax-advisor` v0 agent exists in the four public catalogs as of the build date — see `reference/INVENTORY.md`). The composition synthesizes CPA / tax-preparer practitioner body-of-knowledge (IRC statutory references, IRS form instructions, FASB ASC 740, OECD BEPS / Pillar 2, FinCEN CTA / BOI rule, state DOR conventions, Big Beautiful Bill 2025, TCJA 2017, IRA 2022, Wayfair 2018) and grounds every claim in the cited URLs below.

---

## soul.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Title + persona intro | Composition: tax-preparer / EA / CPA role conventions; seed prompt convictions ("documentation BEFORE filing", "tax planning is multi-year", "most tax loopholes online are 5+ years out of date") | Action-verb-first per `_templates/soul_md_skeleton.md` operator-framing rule |
| MANDATORY disclaimer | Per seed prompt; per IRS Circular 230 + AICPA Code of Conduct + state CPA boards | Every binding tax output ends with "Consult a licensed CPA / tax attorney" |
| Purpose | Composition: hand-off rules from seed prompt + sibling agents (`finance-controller` parent, `finance-agent`, `legal-counsel`, `compliance-agent`) | Defer binding tax decisions to licensed CPA / tax attorney |
| Execution stack | `reference/SOTA_USE_CASES.md` | Built from per-use-case SOTA research; mirrors the 21 bundled skill packs |
| When invoked — Form 1120 / 1065 / 1120-S | IRS instructions per form + Drake / ProConnect / UltraTax / CCH docs + CPA practice (M-1 / M-3 reconciliation) | All standard preparer-software workflows |
| When invoked — Multi-state sales tax | Anrok docs · Stripe Tax docs · Avalara docs · Numeral docs · Sphere docs · Sales Tax Institute economic nexus state guide | Post-Wayfair thresholds |
| When invoked — Payroll tax + 1099 + W-2 | Gusto / Rippling / ADP docs + IRS Form 941 / 940 / 1099 instructions | Standard payroll-platform workflow |
| When invoked — R&D credit | MainStreet docs · Neo Tax docs · Strike Tax docs · IRS Form 6765 instructions · Treas Reg 1.41-4 + 1.174-2 | Section 41 four-part test |
| When invoked — QSBS Section 1202 | Carta QSBS guide · Fenwick QSBS update (OBBB 2025) · IRC Section 1202(c)(2)(A) | OBBB July 2025 tiered exclusion |
| When invoked — International (5471 / 5472 / 8865 / TP) | IRS instructions per form · OECD BEPS Action 13 · Treas Reg 1.482-1 + 1.482-7 | Section 482 best-method rule |
| When invoked — BOI / CTA | FinCEN BOI page + March 2025 interim final rule | Domestic exempt; foreign-registered files |
| When invoked — IRS notice response | IRS.gov notice descriptions · Taxpayer Advocate Service · AICPA notice response guides | Per notice code response strategy |
| When invoked — ASC 740 provision | FASB ASC 740 · Bloomberg Tax Provision docs · ONESOURCE docs · Longview docs | Five-step process |
| When invoked — Equity comp tax | Carta ISO/AMT guide · 83(b) election guide · IRS Form 6251 instructions · IRC Section 422 (ISO) | $100K AMT rule + 1-yr/2-yr LTCG |
| When invoked — Entity structure | Fenwick choice-of-entity startup guide · Carta C-corp vs S-corp vs LLC · Stripe Atlas guides | Decision matrix per stage |
| When invoked — Multi-year tax planning | Thomson Reuters multi-year planning · AICPA multi-year planning | Driver-based model |
| Core operating rules | Composition: tax-preparer / EA / CPA body of knowledge (Circular 230 + AICPA Code of Conduct + IRS substantial-authority standards) | "Most online tax advice is stale" rule per seed prompt |
| Mode-specific decisions | Source-mapped per mode (same as When invoked rows) | Done-when definitions from CPA practice |
| Quality gates | Composition: tax preparation standards + AICPA tax-practice standards + IRS Form 8275 disclosure norms | Statutory citation mandatory |
| Output format | Composition: standard tax-deliverable conventions (memo + xlsx + docx) | $K/$M with one decimal in narrative; full precision in workpaper |
| Communication style | Composition: tax-preparer practice (statute-cite first; data-source second; multi-year framing third) | — |
| When to push back | Composition: IRC + Treas Reg + Substantial Understatement Penalty (Section 6662) | "Don't claim R&D without substantiation" anchors to Tier 1 audit risk |
| When to defer | Composition: hand-off matrix from seed prompt sibling agents | Always-disclose CPA / tax attorney per seed prompt |
| PROACTIVE self-init footer | `METHODOLOGY.md` standard pattern | Routine questions tailored to tax surface (entity type, state of incorporation, active notice/audit/deadline) |
| Closing rule | Restatement of three load-bearing convictions from seed prompt + mandatory disclaimer | — |

---

## role.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Capability reference → Federal tax forms | IRS instructions per form (1120 / 1065 / 1120-S / 941 / 940 / 1099-NEC / 1099-K / W-2 / 5471 / 8865 / 5472 / 6765 / 8975 / 8997 / 8949 / 7004 / 4626 / 6251 / 4562 / 8275 / 9465 / 656 / 12203 / 1118 / 1116 / 2553 / 8832 / 8974) | All standard IRS forms |
| Capability reference → Preparer software | Drake docs · Intuit ProConnect / Lacerte docs · Thomson Reuters UltraTax CS · CCH Axcess docs · TaxSlayer / TaxAct / ATX | Standard professional preparer software set |
| Capability reference → Sales tax platforms | Anrok docs · Stripe Tax docs · Avalara docs · TaxJar docs · Numeral docs · Sphere docs · Quaderno · Vertex · TaxCloud | Standard sales tax SaaS set |
| Capability reference → Income tax + apportionment | Avalara Income Tax docs · Vertex Income Tax docs · Sphere docs · Bloomberg Tax · CCH State Tax Research | State apportionment platforms |
| Capability reference → R&D credit platforms | MainStreet docs · Neo Tax docs · Strike Tax docs · TaxRobot · AlphaCredit · Cherry Bekaert · BDO · RSM | R&D credit SaaS + managed services |
| Capability reference → QSBS trackers | Carta QSBS · Pulley QSBS · TrueQSBS · Brilliant | Section 1202 trackers |
| Capability reference → Tax provision (ASC 740) | Bloomberg Tax Provision · ONESOURCE Tax Provision · Longview Tax · Tax Prodigy · Insightsoftware | ASC 740 platforms |
| Capability reference → International tax + TP | Bloomberg TP · ONESOURCE TP · RoyaltyStat / RoyaltyRange · KPMG / EY / BDO / PwC / Deloitte | TP studies + Pillar 2 |
| Capability reference → Workpaper + binder | Caseware · AdvanceFlow · Workiva · CCH ProSystem fx Engagement | Audit + tax binder |
| Capability reference → 1099 family filing | Track1099 · Tax1099 · Yearli · eFile4Biz · Gusto / Rippling / ADP / Paychex / Justworks | E-filing services |
| Capability reference → Payroll platforms | Gusto · Rippling · ADP RUN · ADP Workforce Now · Paychex Flex · Deel · Justworks · OnPay | Payroll SaaS |
| Capability reference → Federal + state portals | EFTPS · IRS Direct Pay · IRS e-Services · IRS MeF · FinCEN BOSS · per-state DOR portals | Payment + filing portals |
| Form 1120 playbook | IRS Form 1120 instructions + CPA tax-prep practice + Drake / ProConnect / UltraTax / CCH docs | Standard timeline (60-90 days from year-end) |
| Form 1065 / 1120-S playbook | IRS Form 1065 / 1120-S instructions + 704(b) Treas Reg + IRS Form 2553 | Partnership + S-corp specifics |
| Sales tax nexus playbook | Sales Tax Institute economic nexus state guide · TaxJar 2026 sales tax software comparison · Wayfair v. South Dakota (2018) | Post-Wayfair thresholds; SaaS taxability matrix |
| Payroll tax playbook | IRS Form 941 / 940 instructions + Pub 15 (Circular E) + state DOR guides | Deposit schedule + safe harbor |
| 1099 family playbook | IRS Form 1099-NEC / 1099-K / 1042-S instructions + Track1099 / Tax1099 docs | 2024-2026 threshold rollout |
| R&D credit playbook | IRS Form 6765 instructions + Treas Reg 1.41-4 (substantiation) + Section 41(h) startup payroll-offset + Notice 2023-63 cloud R&D + MainStreet / Neo Tax / Strike Tax docs | Section 41 four-part test |
| QSBS Section 1202 playbook | IRC Section 1202 + Fenwick QSBS update (OBBB July 2025) + Carta QSBS guide | OBBB 2025 tiered exclusion 50/75/100% |
| NOL + Section 382 + CAMT playbook | IRC Section 172 (NOL) + Section 382 (ownership change) + Form 4626 (CAMT post-IRA 2022) + Bloomberg Section 382 | Post-TCJA NOL rules |
| Pillar 2 / GloBE / CbCR playbook | OECD Pillar 2 implementation package · BEPS Action 13 (CbCR) · IRS Form 8975 instructions | €750M+ MNC threshold |
| BOI / CTA playbook | FinCEN BOI page · March 2025 interim final rule · CTA litigation history (Nat'l Small Business United v. Yellen) | Domestic exempt post-March 2025 IFR; foreign-registered files |
| IRS notice response playbook | IRS.gov notice descriptions + Taxpayer Advocate Service guides + AICPA IRS notice response | Per notice code |
| ASC 740 provision playbook | FASB ASC 740 + Bloomberg Tax Provision docs + FIN 48 (ASC 740-10) UTP standard | Five-step process |
| Equity comp tax playbook | IRC Section 421-424 (statutory options) + Carta ISO/AMT guide + 83(b) election guide + Treas Reg 1.83-2 | $100K AMT rule + 30-day 83(b) window |
| Transfer pricing playbook | IRC Section 482 + Treas Reg 1.482-1 + 1.482-7 (cost sharing) + OECD TP Guidelines + Altera v. Commissioner (PCT stock-based comp) | Best-method rule; FAR analysis |
| State apportionment playbook | Tax Notes state corporate income tax research + Avalara / Vertex / Sphere apportionment docs | Single-sales factor vs three-factor |
| Section 1031 + OZ playbook | IRC Section 1031 (TCJA-limited to real property) + Section 1400Z-2 (OZ) + IRS Form 8824 / 8997 + OBBB 2025 OZ extension | 45/180-day windows |
| Section 280E + Section 274 playbook | IRC Section 280E + IRS Notice 2021-23 (cannabis) + IRC Section 274(n)(1) + 274(a)(1) + IRS Publication 15-B (fringe benefits) | DEA Schedule III pending |
| Audit prep playbook | AICPA IRS Examination Defense + Bloomberg Tax Audit Workpaper + Caseware audit binder methodology | Substantiation library + IDR response |
| Antipattern catalog | Composition: IRC + Treas Reg + IRS audit guidance (Tier 1 issues) + AICPA practice standards | Each antipattern maps to specific statute or established norm |
| SOTA tool reference | Per-tool sources cited inline (table below) | One source per tool minimum |
| SOTA execution playbook table | Built from `reference/SOTA_USE_CASES.md` mapping | First-stop skill pack per user request type |
| Brief / output templates | Composition: standard tax position memo + IRS notice response + QSBS qualification memo | Synthesized formats |
| OBBB 2025 reference | Fenwick OBBB updates + IRS guidance + AICPA OBBB summary | Key provisions: QSBS, Section 174, bonus dep, Section 199A, SALT cap, OZ, estate tax |
| TCJA reference | IRC + Treas Reg post-TCJA + IRS guidance | Major provisions still in effect; OBBB modifications noted |
| Wayfair reference | South Dakota v. Wayfair, 138 S. Ct. 2080 (2018) + state nexus adoption | Post-Wayfair economic nexus thresholds |
| IRA 2022 reference | IRC + Treas Reg post-IRA + IRS guidance + Notice 2023-7 (CAMT) | CAMT 15% on $1B+ AFSI; stock buyback excise; energy credits |
| Closing rules | Restatement of three load-bearing convictions + hand-off matrix + MANDATORY disclaimer | — |

---

## SOTA tool sources (June 2026)

> One row per SOTA tool referenced in the agent.

| Tool | Source URL | Used for |
|---|---|---|
| IRS Form 1120 instructions | https://www.irs.gov/forms-pubs/about-form-1120 | Form 1120 C-corp filing |
| IRS Form 1065 instructions | https://www.irs.gov/forms-pubs/about-form-1065 | Form 1065 partnership filing |
| IRS Form 1120-S instructions | https://www.irs.gov/forms-pubs/about-form-1120-s | Form 1120-S S-corp filing |
| IRS Schedule K-1 (Form 1065) | https://www.irs.gov/forms-pubs/about-schedule-k-1-form-1065 | K-1 distribution |
| IRS Schedule K-2 / K-3 | https://www.irs.gov/forms-pubs/about-schedule-k-2-form-1065 | International items per partner |
| IRS Form 941 + 940 | https://www.irs.gov/forms-pubs/about-form-941 · https://www.irs.gov/forms-pubs/about-form-940 | Payroll tax quarterly + annual |
| IRS Form 1099-NEC | https://www.irs.gov/forms-pubs/about-form-1099-nec | Contractor payments |
| IRS Form 1099-K threshold rollout | https://www.irs.gov/businesses/understanding-your-form-1099-k | 2024 $5K → 2025 $2.5K → 2026 $600 |
| IRS Form 1042-S (foreign) | https://www.irs.gov/forms-pubs/about-form-1042-s | 30% default withholding foreign person |
| IRS Form 5471 (CFC) | https://www.irs.gov/forms-pubs/about-form-5471 | 10%+ US-owned foreign corp |
| IRS Form 8865 (foreign partnership) | https://www.irs.gov/forms-pubs/about-form-8865 | Foreign partnership reporting |
| IRS Form 5472 (foreign-owned US) | https://www.irs.gov/forms-pubs/about-form-5472 | 25%+ foreign owner; $25K penalty per missed |
| IRS Form 6765 (R&D credit) | https://www.irs.gov/forms-pubs/about-form-6765 | Section 41 R&D credit |
| IRS Form 8974 (payroll offset election) | https://www.irs.gov/forms-pubs/about-form-8974 | Section 41(h) startup payroll-offset |
| IRS Form 8975 (CbCR) | https://www.irs.gov/forms-pubs/about-form-8975 | Country-by-Country Reporting |
| IRS Form 8997 (QOF) | https://www.irs.gov/forms-pubs/about-form-8997 | OZ QOF annual reporting |
| IRS Form 8824 (1031 like-kind) | https://www.irs.gov/forms-pubs/about-form-8824 | Section 1031 exchange |
| IRS Form 8949 + Schedule D | https://www.irs.gov/forms-pubs/about-form-8949 | Capital gains + QSBS Code Q |
| IRS Form 4626 (CAMT) | https://www.irs.gov/forms-pubs/about-form-4626 | Corp AMT post-IRA 2022 |
| IRS Form 6251 (AMT individual) | https://www.irs.gov/forms-pubs/about-form-6251 | Individual AMT incl. ISO bargain element |
| IRS Form 4562 (depreciation) | https://www.irs.gov/forms-pubs/about-form-4562 | Depreciation + Section 179 + bonus |
| IRS Form 8275 / 8275-R | https://www.irs.gov/forms-pubs/about-form-8275 | Disclosure to avoid 6662 penalty |
| IRS Form 1120-W (corp estimated) | https://www.irs.gov/forms-pubs/about-form-1120-w | Quarterly estimated tax |
| IRS Form 2553 (S-corp election) | https://www.irs.gov/forms-pubs/about-form-2553 | S-corp election; 75-day window |
| IRS Form 8832 (entity classification) | https://www.irs.gov/forms-pubs/about-form-8832 | Entity classification election |
| IRS Form 9465 (installment) | https://www.irs.gov/forms-pubs/about-form-9465 | Installment agreement request |
| IRS Form 656 (OIC) | https://www.irs.gov/forms-pubs/about-form-656 | Offer in Compromise |
| IRS Form 12203 (appeals) | https://www.irs.gov/forms-pubs/about-form-12203 | Appeals review request |
| IRS CP2000 notice | https://www.irs.gov/individuals/understanding-your-cp2000-notice | Underreporter inquiry response |
| IRS Taxpayer Advocate notice library | https://www.taxpayeradvocate.irs.gov/notices/ | Per-code response guidance |
| IRS EFTPS | https://www.irs.gov/payments/eftps-the-electronic-federal-tax-payment-system | Federal tax payments + corp deposits |
| IRS Direct Pay | https://www.irs.gov/payments/direct-pay | Individual federal tax payment |
| IRS Audit guidance | https://www.irs.gov/businesses/small-businesses-self-employed/irs-audits | IRS audit timeline + IDR response |
| IRS Pub 15 (Circular E) | https://www.irs.gov/publications/p15 | Employer's Tax Guide (payroll) |
| IRS Pub 15-B (fringe benefits) | https://www.irs.gov/publications/p15b | Section 132 fringe benefit exclusions |
| IRS Notice 2021-23 (cannabis) | https://www.irs.gov/pub/irs-drop/n-21-23.pdf | Section 280E disallowance |
| IRS Section 274 (meals + entertainment) | https://www.irs.gov/businesses/section-274-meals-entertainment | Section 274(n)(1) 50% limit |
| IRS Opportunity Zones | https://www.irs.gov/credits-deductions/opportunity-zones | Section 1400Z |
| Drake Tax | https://www.drakesoftware.com/ | SMB / firm preparer software |
| Intuit ProConnect | https://accountants.intuit.com/proconnect/ | Lacerte cloud preparer |
| Thomson Reuters UltraTax CS | https://tax.thomsonreuters.com/en/cs-professional-suite/ultratax-cs | Enterprise firm preparer |
| CCH Axcess (Wolters Kluwer) | https://www.wolterskluwer.com/en/solutions/cch-axcess | Cloud-native preparer |
| Bloomberg Tax Provision | https://www.bloombergtax.com/tax-provision/ | ASC 740; Pillar 2 |
| ONESOURCE Tax Provision | https://tax.thomsonreuters.com/en/onesource/tax-provision | Alt ASC 740 |
| Longview Tax | https://www.insightsoftware.com/longview-tax/ | Alt ASC 740 + Pillar 2 |
| Anrok | https://anrok.com/ | SaaS multi-state sales tax |
| Stripe Tax docs | https://docs.stripe.com/tax | Embedded sales tax |
| Avalara | https://www.avalara.com/ | Enterprise sales / income tax |
| Avalara — apportionment | https://www.avalara.com/us/en/products/income-tax.html | Multi-state income tax apportionment |
| TaxJar | https://www.taxjar.com/ | E-commerce sales tax |
| Numeral | https://www.numeral.com/ | AI-first sales tax |
| Numeral — Avalara vs Anrok | https://www.numeral.com/blog/avalara-vs-anrok | Platform decision |
| Sphere | https://sphere.co/ | Modern sales + use + business licenses |
| Vertex Income Tax | https://www.vertexinc.com/products/income-tax | Enterprise apportionment |
| Sales Tax Institute — Economic Nexus | https://www.salestaxinstitute.com/resources/economic-nexus-state-guide | Post-Wayfair thresholds per state |
| MainStreet | https://mainstreet.com/ | R&D credit for startups |
| Neo Tax | https://neo.tax/ | AI-driven R&D credit + QSBS |
| Strike Tax Advisory | https://striketax.com/ | Managed R&D credit |
| Carta — QSBS | https://carta.com/learn/equity/stock-options/iso-amt/qsbs/ | QSBS qualification + tracking |
| Carta — ISO + AMT | https://carta.com/learn/equity/stock-options/iso-amt/ | ISO mechanics |
| Carta — 83(b) elections | https://carta.com/learn/equity/stock-options/83b-elections/ | 83(b) 30-day window |
| Carta — C-corp vs S-corp vs LLC | https://carta.com/blog/c-corp-vs-s-corp-vs-llc/ | Entity choice |
| Pulley — ESOP | https://pulley.com/products/esop-management-software | Equity grants |
| Pulley — 83(b) FAQ | https://help.pulley.com/en/articles/4781385-83-b-election-faq | 83(b) mechanics |
| Pulley — 409A | https://pulley.com/products/409a-valuations | 409A delivery |
| Fenwick & West — QSBS / OBBB 2025 | https://www.fenwick.com/insights/publications/qsbs-update-one-big-beautiful-bill-act-expands-section-1202 | OBBB July 2025 expansion |
| Fenwick & West — Section 174 / OBBB 2025 | https://www.fenwick.com/insights/publications/section-174-rd-capitalization-update-big-beautiful-bill | OBBB domestic R&D immediate expensing |
| Fenwick & West — Section 382 | https://www.fenwick.com/insights/publications/section-382-overview | NOL ownership change |
| Fenwick & West — Choice of Entity | https://www.fenwick.com/insights/publications/choice-of-entity-startups | Entity choice for startups |
| OECD Pillar 2 / GloBE | https://www.oecd.org/tax/beps/pillar-two-implementation-package.htm | 15% minimum ETR |
| OECD BEPS Action 13 (CbCR) | https://www.oecd.org/tax/beps/beps-actions/action13/ | Country-by-Country Reporting |
| FinCEN BOI | https://www.fincen.gov/boi | Beneficial ownership reporting |
| FinCEN — March 2025 IFR | https://www.fincen.gov/news/news-releases/fincen-issues-interim-final-rule-removes-beneficial-ownership-reporting | Domestic exemption |
| FinCEN BOSS portal | https://boiefiling.fincen.gov/ | BOI filing portal |
| FASB ASC 740 (Income Taxes) | https://www.fasb.org/page/PageContent?pageId=/standards/asc740.html | ASC 740 tax provision standard |
| AICPA — IRS Examination Defense | https://www.aicpa.org/topic/tax/irs-examination-defense | Audit prep + response |
| AICPA — IRS Notice Response | https://www.aicpa.org/topic/tax/irs-notice-response | Per notice code response |
| AICPA — Multi-year tax planning | https://www.aicpa.org/topic/tax/multi-year-tax-planning | Multi-year planning conventions |
| AICPA — Section 174 R&D | https://www.aicpa.org/topic/tax/section-174-research-experimental | Section 174 capitalization |
| Thomson Reuters — Multi-year tax planning | https://tax.thomsonreuters.com/blog/multi-year-tax-planning-strategies-corporations/ | Multi-year planning |
| Track1099 | https://www.track1099.com/ | E-filing 1099 + W-2 + 1042-S |
| Tax1099 | https://www.tax1099.com/ | Alt e-filing service |
| Gusto Developer | https://docs.gusto.com/ | Gusto API |
| Rippling Developer | https://developer.rippling.com/ | Rippling API |
| ADP Developer | https://developer.adp.com/ | ADP API |
| Deel | https://www.deel.com/ | Global contractor + EOR |
| OECD Tax — TP Guidelines | https://www.oecd.org/tax/transfer-pricing/ | Transfer pricing guidance |
| IRS — Transfer Pricing | https://www.irs.gov/businesses/international-businesses/transfer-pricing | Section 482 |
| Taxnotes — State Corporate Income Tax | https://www.taxnotes.com/research/federal/state-tax-treatment-corporate-income | State apportionment + nexus |
| Salestaxhandbook — Economic Nexus | https://www.salestaxhandbook.com/economic-nexus | State nexus thresholds |
| Numeral — Economic Nexus Thresholds | https://www.numeral.com/blog/economic-nexus-thresholds-by-state | State nexus thresholds |
| Stripe Atlas — Guides | https://stripe.com/atlas/guides | Entity formation tax guides |
| TaxCloud | https://taxcloud.com/blog/anrok-vs-stripe-tax-comparison/ | Sales tax platform comparison |
| FederalRegister — DEA Schedule III (cannabis) | https://www.federalregister.gov/documents/2024/05/21/2024-11137/schedules-of-controlled-substances-rescheduling-of-marijuana | Cannabis reclassification status |
| CANORML — Section 280E | https://www.canorml.org/tax-policy/section-280e/ | Section 280E disallowance |
| Caseware | https://www.caseware.com/ | Tax + audit binder |
| AdvanceFlow (Thomson Reuters) | https://tax.thomsonreuters.com/en/cs-professional-suite/advanceflow | Cloud workpaper |
| Workiva — Audit & Risk | https://www.workiva.com/solutions/internal-audit-management | GRC + audit + tax workpaper |
| Tax Administration State Agencies | https://www.taxadmin.org/state-tax-agencies | State DOR contacts |
| Sales Tax Institute — State Tax Agency Contacts | https://www.salestaxinstitute.com/state-tax-agency-contacts | Per-state DOR portals |
| Bloomberg Tax — Pillar 2 | https://www.bloombergtax.com/pillar-two/ | Pillar 2 software |

---

## Notes on authored-from-synthesis

Sections that aren't directly lifted from a single source (these are operational glue, not domain claims):

- **MANDATORY disclaimer** ("Consult a licensed CPA / tax attorney for binding tax decisions") — operational discipline per the seed prompt + IRS Circular 230 + AICPA Code of Conduct + state CPA boards, not a single citable source. Reinforced by the seed prompt and consistently applied to every binding output.
- **Tax position memo template** — synthesized from standard CPA / tax-attorney deliverable formats; not lifted from one source. Inspired by AICPA tax-practice standards + Circular 230 written-advice rules.
- **IRS notice response template** — synthesized from common practitioner-letter format (TaxAct, AICPA, Bloomberg). Not a single canonical source.
- **QSBS qualification memo template** — synthesized from Fenwick + Carta + Pulley QSBS memos; the template captures the qualification tests + tiered exclusion + cap.
- **Journal-entry naming convention** (referenced inline) — same as `finance-controller` convention; not lifted from one source.
- **Antipattern catalog** — each individual antipattern grounds in a specific statute / IRS guidance / Treas Reg (IRC Section 1202, Section 41, Section 174, Section 482, Section 6662, IRC 6038A penalty, IRS Form 2210), but the BAD / GOOD pairing format is editorial.
- **PROACTIVE.md self-init footer** — standard `METHODOLOGY.md` pattern, only the routine questions changed to match tax surface (entity type, nexus, active notice/audit/deadline).
- **Hand-off matrix to sibling agents** — seed-prompt-driven; `finance-controller` (parent), `finance-agent`, `legal-counsel`, `compliance-agent` references reflect the catalog as of build date.
- **SOTA execution playbook table** — synthesized from per-use-case mapping in `reference/SOTA_USE_CASES.md`; the first-stop skill pack per user-request type is editorial routing.
- **Dunning email templates** (referenced only by reference, not duplicated here) — `finance-controller` owns these; tax-agent uses `gmail-mcp` for notice acknowledgments + K-1 distribution.

The base claims (Section 1202 qualification tests + OBBB tiered exclusion, Section 41 four-part test, Section 174 capitalization + OBBB domestic reversal, Section 382 ownership change, Section 274 meal/entertainment, Section 1031 45/180-day windows, Section 1400Z 5/7/10-yr step-up, Wayfair economic nexus thresholds, FinCEN CTA / BOI rule + March 2025 IFR, Pillar 2 €750M threshold + IIR / UTPR / QDMTT, IRS notice codes + response windows, ASC 740 five-step process + FIN 48 UTP) are all sourced to either statutory standards (IRC + Treas Reg + FASB ASC) or IRS / OECD / FinCEN authoritative guidance cited in the table above.

---

## How to update this agent

1. Re-fetch the SOTA tool source URLs listed above; check for tax law changes (new legislation like OBBB), API changes, new SaaS platforms, IRS form updates, FinCEN rule changes.
2. Tax updates the agent should monitor each year:
   - **January-April:** IRS publishes Rev Proc / Rev Rul / Notices for current tax year; preparer software releases.
   - **June-September:** Mid-year corporate tax legislative changes (typically); Treasury guidance.
   - **December:** Year-end planning publications + tax extender legislation.
   - **Quarterly:** State DOR rule changes for sales tax + apportionment.
3. Update the per-tool SOTA tool reference in `role.md` if anything has changed materially.
4. Update `agent.yaml` `mcp_servers` if a new tax-related MCP enters the catalog (e.g., a future Drake MCP, MainStreet MCP, Carta MCP, Anrok MCP).
5. Update `reference/SOTA_USE_CASES.md` confidence ratings if a paid integration becomes free or vice versa.
6. Re-run `python verify.py tax-agent` to confirm structure intact.
7. Re-build: `python build.py tax-agent` produces a fresh `.craftbot`.

For the canonical reference repos (Step 2 of methodology), recheck quarterly:
- `wshobson/agents` (plugins/finance — closest is `business-analyst`)
- `VoltAgent/awesome-claude-code-subagents` (categories/12-finance — none as of build date)
- `msitarzewski/agency-agents` (tax-preparer / fractional-tax — recheck)
- `JSONbored/claudepro-directory` — search for tax / CPA / accountant / preparer skills

When SOTA changes materially (new legislation, new IRS guidance, API endpoint change, platform acquisition closes, new MCP enters CraftBot catalog, new state Wayfair adoption), update the relevant bundled skill pack's `SKILL.md` first, then the SOTA tool source table here.

**Special attention items for refresh:**
- **OBBB 2025 transition rules** — Treasury / IRS will publish implementing guidance through 2026; QSBS + Section 174 + bonus depreciation + Section 199A + SALT cap + OZ all need monitoring
- **BOI / CTA status** — Litigation ongoing; court rulings + Treasury rule changes possible
- **Pillar 2 / GloBE** — Implementation widening 2026-2027; ETR computation methodologies refined
- **Section 174 R&D** — OBBB 2025 restored domestic immediate expensing; pre-2025 amortization waterfall still applies; AICPA + Big 4 publishing transition guidance
- **DEA Schedule III cannabis** — Final rule pending; Section 280E treatment changes if reclassified
- **1099-K threshold** — IRS phased rollout 2024-2026; may be delayed again by Congress
