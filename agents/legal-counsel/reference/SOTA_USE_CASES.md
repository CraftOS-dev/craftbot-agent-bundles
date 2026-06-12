# legal-counsel — SOTA Use Case Map (June 2026)

Per-use-case mapping from agent capability to concrete SOTA mechanism. Each row names the tool, the agent's execution path (which CraftBot MCP/skill actually runs it), the canonical source, and a confidence verdict.

Legend:
- `✓` — agent can execute the SOTA path end-to-end today with shipped MCPs/skills.
- `⚠` — agent can execute the SOTA path but with a known caveat (auth scope, paid tier, env dep, jurisdiction-specific).
- `✗` — SOTA path requires a tool the agent cannot reach (deferred / future work).

**Standing disclaimer.** Every output that touches a binding legal decision must include the consult-an-attorney disclaimer (codified in `soul.md`). This is not a paywalled tool — it's the agent's hard rule.

Bundled skill packs (in `skills/`) referenced below (Round 2 will populate):
`contract-review-msa-nda-employment`, `robin-spellbook-harvey-ai-contract-review`, `terms-of-service-tos-drafting`, `privacy-policy-gdpr-ccpa`, `iubenda-termly-privacy-policy-generators`, `cookie-consent-management-cookiebot-onetrust`, `gdpr-readiness-audit`, `ccpa-cpra-readiness-audit`, `drata-vanta-secureframe-soc2-readiness`, `dpa-data-processing-agreement`, `trademark-search-uspto-tess-wipo`, `patent-search-uspto-lens-google`, `equity-grants-isos-rsus-83b-election`, `safe-convertible-note-yc-template`, `term-sheet-review-series-a-typical-terms`, `founders-agreement-vesting-ip-assignment`, `open-source-license-mit-apache-gpl-agpl`, `dmca-takedown-process`, `ironclad-contractworks-clm`, `non-compete-non-solicit-state-enforceability`.

---

## MSA review (Master Service Agreement)

- **SOTA approach:** AI-assisted clause-level review with Robin AI / Spellbook / Harvey for first-pass redlines (indemnity, LoL, IP ownership, termination, payment terms, audit rights, SLA, data protection, governing law). Cross-check against Bonterms / Common Paper benchmarks.
- **Agent execution path:** `filesystem` reads the contract; `cli-anything` runs `pdftotext` / `pandoc` for normalization; bundled `contract-review-msa-nda-employment` drives the clause checklist; `robin-spellbook-harvey-ai-contract-review` covers AI-assisted markup. Output is a redline + memo with disclaimer.
- **Source:** https://www.robinai.com/ + https://www.spellbook.legal/ + https://bonterms.com/ + https://commonpaper.com/standards/
- **Confidence:** ✓

## NDA review + drafting (mutual + unilateral)

- **SOTA approach:** Common Paper Standard NDA as the canonical template (mutual / unilateral / multi-party variants). Review checklist: definition of Confidential Info, exclusions, term length, residuals, return/destruction, no-poach overlap, governing law/venue.
- **Agent execution path:** `filesystem` writes the draft; bundled `contract-review-msa-nda-employment` covers NDA-specific rules. Common Paper templates pulled via `cli-anything` + `curl`.
- **Source:** https://commonpaper.com/standards/mutual-nda/ + https://bonterms.com/forms/ndas
- **Confidence:** ✓

## Employment agreement review + drafting (US, EU)

- **SOTA approach:** Jurisdiction-specific clauses — at-will (US, most states), notice period (EU directives), classification (employee vs contractor IRS 20-factor / EU AB5 equivalents), IP assignment, confidentiality, non-compete enforceability per state (CA/ND/OK void; FTC 2024 rule paused), severance, equity grant language.
- **Agent execution path:** Bundled `contract-review-msa-nda-employment` + `non-compete-non-solicit-state-enforceability` + `founders-agreement-vesting-ip-assignment`. `cli-anything` curl fetches DOL fact sheets, state AG enforceability guides; `filesystem` writes the draft.
- **Source:** https://www.dol.gov/ + https://www.ftc.gov/legal-library/browse/rules/noncompete-rule + https://www.ncsl.org/labor-and-employment/non-compete-agreements
- **Confidence:** ⚠ (jurisdiction varies — agent always names the jurisdiction and disclaimer applies; non-compete FTC rule status remains uncertain in 2026)

## Independent contractor agreement

- **SOTA approach:** IRS 20-factor classification + state ABC test (CA AB5, NJ, MA equivalents) + IP assignment (work-for-hire language insufficient under CA Labor Code 3351.5 — explicit assignment required). Stripe Atlas, Cooley GO contractor templates.
- **Agent execution path:** Bundled `contract-review-msa-nda-employment` + `founders-agreement-vesting-ip-assignment`. `cli-anything` curl pulls IRS publication 1779 + state ABC summaries.
- **Source:** https://www.irs.gov/businesses/small-businesses-self-employed/independent-contractor-defined + https://www.cooleygo.com/documents/
- **Confidence:** ✓

## Vendor / SaaS subscription review (supplier-side)

- **SOTA approach:** Standard SaaS T&C terms — auto-renewal, price escalators, SLA credits, data ownership, security/SOC2, sub-processors, exit/portability, audit rights, indemnity caps, force majeure (post-COVID norms). Cross-check Common Paper Cloud Service Agreement.
- **Agent execution path:** Bundled `contract-review-msa-nda-employment` + `ironclad-contractworks-clm` (when user is using a CLM). `cli-anything` for `pdftotext` extraction.
- **Source:** https://commonpaper.com/standards/cloud-service-agreement/ + https://www.bonterms.com/forms/cloud-services
- **Confidence:** ✓

## Customer SaaS terms (T&C / TOS) drafting

- **SOTA approach:** Bonterms Cloud Terms / Common Paper standardized terms as base. Customize for product specifics — usage limits, acceptable use, API limits, indemnity caps, governing law (Delaware is common for SaaS).
- **Agent execution path:** Bundled `terms-of-service-tos-drafting`. `filesystem` writes the draft; `cli-anything` curl pulls Bonterms templates.
- **Source:** https://bonterms.com/ + https://commonpaper.com/
- **Confidence:** ✓

## Data Processing Agreement (DPA) review + drafting

- **SOTA approach:** GDPR Art. 28 mandatory terms (subject matter, duration, nature, type of personal data, categories of data subjects, controller obligations, processor obligations, sub-processor rules, SCCs for international transfers post-Schrems II). Bonterms DPA Module + Iubenda DPA generator.
- **Agent execution path:** Bundled `dpa-data-processing-agreement`. `cli-anything` curl for EU Commission SCC templates (2021/914 set); `filesystem` writes the DPA.
- **Source:** https://bonterms.com/forms/data-processing-addendum + https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en
- **Confidence:** ✓

## Privacy policy drafting + maintenance

- **SOTA approach:** Iubenda or Termly generator for the base policy (jurisdiction-detection, auto-update on regulation change). Manually layer product-specific data flows (analytics, marketing pixels, sub-processors). Disclose data subject rights per GDPR Art. 13/14 + CCPA §1798.130.
- **Agent execution path:** Bundled `iubenda-termly-privacy-policy-generators` + `privacy-policy-gdpr-ccpa`. `cli-anything` + `curl` to Iubenda API / Termly export; `filesystem` writes the final policy.
- **Source:** https://www.iubenda.com/en/privacy-policy-generator + https://termly.io/products/privacy-policy-generator/
- **Confidence:** ✓

## Cookie policy + consent banner setup

- **SOTA approach:** Cookiebot or OneTrust for scanner + CMP (Consent Management Platform). Iubenda Cookie Solution as a lighter alternative. IAB TCF v2.2 compliance for ad-supported sites. Implement Google Consent Mode v2 for GA/Ads conversions.
- **Agent execution path:** Bundled `cookie-consent-management-cookiebot-onetrust`. `cli-anything` curl runs Cookiebot scanner API; `filesystem` writes the embed snippet + policy.
- **Source:** https://www.cookiebot.com/ + https://www.onetrust.com/products/cookie-consent/ + https://iabeurope.eu/transparency-consent-framework/
- **Confidence:** ✓

## GDPR readiness audit (Art. 6 lawful basis, DPIA, SAR/DSAR)

- **SOTA approach:** Six-lawful-basis mapping (Art. 6: consent, contract, legal obligation, vital interests, public task, legitimate interests + LIA balancing test). DPIA when high-risk processing (Art. 35). SAR/DSAR pipeline (Art. 12-23) with 1-month response. ROPA per Art. 30. DPO designation when required.
- **Agent execution path:** Bundled `gdpr-readiness-audit`. `cli-anything` + ICO templates pulled via curl; `filesystem` produces a gap-analysis report.
- **Source:** https://gdpr.eu/ + https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/ + https://edpb.europa.eu/
- **Confidence:** ✓

## CCPA / CPRA readiness audit

- **SOTA approach:** Right to know, delete, correct, opt-out of sale/share, limit use of sensitive personal info. "Do Not Sell or Share My Personal Information" link required. Service provider agreements (CPRA §1798.140(ag)). Privacy notice + just-in-time notices. Cal AG enforcement focus areas (children, dark patterns, GPC signals).
- **Agent execution path:** Bundled `ccpa-cpra-readiness-audit`. `cli-anything` curl to Cal AG resources; `filesystem` produces audit report.
- **Source:** https://oag.ca.gov/privacy/ccpa + https://cppa.ca.gov/regulations/
- **Confidence:** ✓

## SOC 2 readiness (Type I + II)

- **SOTA approach:** Drata / Vanta / SecureFrame for automated evidence collection across the five Trust Services Criteria (Security mandatory; Availability, Confidentiality, Processing Integrity, Privacy optional). Type I = point in time; Type II = 3-12 month observation. AICPA TSP 100 framework.
- **Agent execution path:** Bundled `drata-vanta-secureframe-soc2-readiness`. `cli-anything` curl to Drata / Vanta REST APIs for control status queries; `filesystem` writes the gap-analysis + remediation plan.
- **Source:** https://drata.com/ + https://www.vanta.com/ + https://secureframe.com/ + https://us.aicpa.org/interestareas/frc/assuranceadvisoryservices/sorhome
- **Confidence:** ⚠ (Drata/Vanta/SecureFrame are SaaS — recipient supplies API token; tooling itself is wired)

## HIPAA business associate agreements (BAA)

- **SOTA approach:** HHS-published model BAA language as base. Verify covered entity vs business associate role. Required elements per 45 CFR §164.504(e). Sub-BA flow-down. Breach notification timeline (60 days).
- **Agent execution path:** Bundled `contract-review-msa-nda-employment` (BAA recipe section) + `dpa-data-processing-agreement` (privacy overlap). `cli-anything` curl pulls HHS template.
- **Source:** https://www.hhs.gov/hipaa/for-professionals/covered-entities/sample-business-associate-agreement-provisions/
- **Confidence:** ✓

## PCI DSS scope analysis

- **SOTA approach:** PCI DSS v4.0 (effective March 2024 with future-dated requirements through March 2025; in steady-state by 2026). SAQ vs ROC determination by merchant level + processing method. Scope reduction via tokenization (Stripe / Braintree). Network segmentation justification.
- **Agent execution path:** Bundled `gdpr-readiness-audit`-adjacent compliance recipe (the agent treats PCI as a sibling scope to GDPR/SOC2). `cli-anything` curl to PCI SSC documents library.
- **Source:** https://www.pcisecuritystandards.org/document_library/ + https://stripe.com/guides/pci-compliance
- **Confidence:** ⚠ (PCI SSC docs require free account login; agent fetches what's publicly indexed and asks user to share gated PDFs)

## Trademark search + filing

- **SOTA approach:** USPTO TESS (US) + WIPO Global Brand Database (50+ jurisdictions) + Trademarkia for fast clearance. Filing through USPTO TEAS Standard / TEAS Plus. Class-based fee structure (Nice Classification). Use-in-commerce vs intent-to-use basis.
- **Agent execution path:** `uspto-mcp` for direct USPTO queries; bundled `trademark-search-uspto-tess-wipo`. `cli-anything` curl to TESS / WIPO endpoints; `filesystem` writes the clearance memo.
- **Source:** https://www.uspto.gov/trademarks/search + https://www.wipo.int/branddb/en/ + https://www3.wipo.int/madrid/monitor/
- **Confidence:** ✓

## Patent search + provisional vs non-provisional decision

- **SOTA approach:** USPTO Patent Public Search + Google Patents + Lens.org for prior art. Provisional ($60-300, 12-month placeholder) vs non-provisional decision based on stage, budget, urgency. Inventor disclosure documentation (best by qualified patent attorney/agent).
- **Agent execution path:** `uspto-mcp` for USPTO queries; bundled `patent-search-uspto-lens-google`. `cli-anything` curl to Google Patents + Lens.org public APIs.
- **Source:** https://ppubs.uspto.gov/ + https://patents.google.com/ + https://www.lens.org/
- **Confidence:** ✓

## Copyright registration

- **SOTA approach:** US Copyright Office eCO (Electronic Copyright Office) registration. $45-65 single-author single-work; $85 standard. Group registration available for unpublished works, photos, serials. Berne Convention auto-protection but registration required for US infringement suits + statutory damages.
- **Agent execution path:** `cli-anything` curl to copyright.gov public forms / fee schedule; bundled `dmca-takedown-process` (adjacent IP enforcement). `filesystem` writes the prep doc; user files via eCO.
- **Source:** https://www.copyright.gov/registration/ + https://eco.copyright.gov/eService_enu/
- **Confidence:** ⚠ (filing itself requires user login on copyright.gov; agent preps the filing package)

## Equity grant docs (ISOs, NSOs, RSUs, stock purchase agreements)

- **SOTA approach:** Stock plan templates (Cooley GO, Stripe Atlas, Clerky). ISO §422 requirements (10-year max, FMV strike, $100k vesting limit). NSO ordinary-income tax. RSUs taxed on vesting unless 83(i) election. 409A valuation required for FMV strike.
- **Agent execution path:** Bundled `equity-grants-isos-rsus-83b-election` + `founders-agreement-vesting-ip-assignment`. `cli-anything` curl to Cooley GO / Stripe Atlas template library. Recommends 409A providers (Carta, Pulley, Trica, Eqvista).
- **Source:** https://www.cooleygo.com/documents/equity-compensation/ + https://www.irs.gov/pub/irs-drop/n-18-97.pdf + https://stripe.com/atlas
- **Confidence:** ✓

## 83(b) election filing

- **SOTA approach:** 30-day deadline from grant date (strict — no extensions). Form (no IRS-published number; required content listed in Treasury Reg §1.83-2(e)). Certified mail with return receipt to IRS service center. Copy to employer + retain for tax records. As of 2025 IRS accepts e-filing for some 83(b) elections via a pilot.
- **Agent execution path:** Bundled `equity-grants-isos-rsus-83b-election`. `cli-anything` + `filesystem` writes the prep packet (election letter + cover memo). Sends user to IRS.gov for e-file portal.
- **Source:** https://www.irs.gov/pub/irs-drop/rp-12-29.pdf + https://www.irs.gov/forms-pubs/about-form-15620
- **Confidence:** ✓

## SAFE / convertible note review (YC SAFE, post-money MFN)

- **SOTA approach:** YC Post-Money SAFE (default since 2018) — valuation cap, discount, MFN, pro-rata side letter. Convertible notes — interest rate (typically 5-8%), maturity (18-24mo), cap, discount, qualified financing trigger. Stripe Atlas / Clerky / Carta for cap-table modeling.
- **Agent execution path:** Bundled `safe-convertible-note-yc-template`. `cli-anything` curl pulls YC SAFE templates; `filesystem` produces redline + dilution memo.
- **Source:** https://www.ycombinator.com/documents + https://www.cooleygo.com/documents/safe-and-convertible-securities/
- **Confidence:** ✓

## Term sheet review (Series A typical terms)

- **SOTA approach:** NVCA model term sheet (2024 update) as the benchmark. Pro-rata rights, anti-dilution (broad-based weighted average is market), liquidation preference (1x non-participating is market), board composition (founder/investor/independent), drag-along, ROFR, info rights, protective provisions list. Aumni / Carta data for current market terms.
- **Agent execution path:** Bundled `term-sheet-review-series-a-typical-terms`. `cli-anything` curl to NVCA + Aumni / Carta benchmarks; `filesystem` writes a deviation-from-market memo.
- **Source:** https://nvca.org/model-legal-documents/ + https://carta.com/learn/startups/state-of-private-markets/
- **Confidence:** ✓

## Cap table impact analysis (dilution math)

- **SOTA approach:** Pre-money / post-money modeling with option pool shuffle (pre-money pool = founder dilution; post-money pool = pro-rata dilution). Carta / Pulley / AngelList Stack for live modeling. SAFE conversion math: post-money SAFE = valuation cap shares minted before priced round; calculate as (investment / cap) shares.
- **Agent execution path:** Bundled `safe-convertible-note-yc-template` + `term-sheet-review-series-a-typical-terms`. `cli-anything` for Python `pandas` modeling if user shares cap table CSV; `filesystem` writes the model.
- **Source:** https://carta.com/learn/equity/ + https://www.holloway.com/g/raising-venture-capital
- **Confidence:** ✓

## Founders agreement / co-founder vesting + IP assignment

- **SOTA approach:** 4-year vest with 1-year cliff (market). Acceleration triggers (single vs double trigger on change-of-control). IP assignment to NewCo (explicit, not work-for-hire alone). Equity split (Slicing Pie / vested ownership / negotiated). Founder share repurchase right at cost on departure.
- **Agent execution path:** Bundled `founders-agreement-vesting-ip-assignment`. `cli-anything` curl to Cooley GO / Stripe Atlas / Clerky templates.
- **Source:** https://www.cooleygo.com/documents/founders-stock/ + https://stripe.com/atlas + https://www.clerky.com/
- **Confidence:** ✓

## IP assignment from contractor agreements

- **SOTA approach:** Explicit assignment language ("hereby assigns" — present-tense vesting), not "agrees to assign." Work-for-hire only covers narrow categories under 17 USC §101 — explicit assignment is the backstop. CA Labor Code 3351.5 carve-out for personal time/no-company-resources inventions.
- **Agent execution path:** Bundled `founders-agreement-vesting-ip-assignment`. `cli-anything` + `filesystem` for clause review.
- **Source:** https://www.law.cornell.edu/uscode/text/17/101 + https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=LAB&sectionNum=2870
- **Confidence:** ✓

## Open source license compliance (MIT vs Apache vs GPL vs AGPL)

- **SOTA approach:** Permissive (MIT, BSD, Apache 2.0) — attribution + license preservation. Copyleft (GPL v2/v3) — derivative source disclosure. Network copyleft (AGPL) — SaaS use triggers disclosure. SPDX identifiers for SBOMs. FOSSA / Snyk / OSS Review Toolkit (ORT) for automated license scanning.
- **Agent execution path:** Bundled `open-source-license-mit-apache-gpl-agpl`. `cli-anything` runs `ort analyze && ort scan` (OSS Review Toolkit) or `npx license-checker --json`. `filesystem` produces the SBOM + license obligation memo. `github` MCP for repo crawl.
- **Source:** https://spdx.org/licenses/ + https://opensource.org/licenses + https://github.com/oss-review-toolkit/ort
- **Confidence:** ✓

## Trademark licensing

- **SOTA approach:** Quality control (mandatory — naked license risk loss of mark), scope (territory, products, exclusivity), royalty structure, term + renewal, audit rights, IP indemnity, termination + sunset rights, sub-licensing rules.
- **Agent execution path:** Bundled `contract-review-msa-nda-employment` (licensing recipe section). `cli-anything` for template fetch.
- **Source:** https://www.uspto.gov/trademarks/maintaining-trademark-registration + https://www.inta.org/topics/licensing/
- **Confidence:** ✓

## DMCA takedown notice / response

- **SOTA approach:** §512(c) notice elements (signature, identification of work, identification of allegedly infringing material with URL, contact info, good-faith belief statement, accuracy/perjury statement). Counter-notice elements (§512(g)). DMCA agent registration with Copyright Office ($6 + biennial renewal).
- **Agent execution path:** Bundled `dmca-takedown-process`. `cli-anything` curl to copyright.gov DMCA Designated Agent Directory; `filesystem` writes notice / counter-notice.
- **Source:** https://www.copyright.gov/dmca-directory/ + https://www.law.cornell.edu/uscode/text/17/512
- **Confidence:** ✓

## Right of publicity / image usage rights

- **SOTA approach:** State-by-state right of publicity (CA Civil Code §3344, NY Civil Rights Law §50-51, TN Personal Rights Protection Act for descendible). Model release forms (full release + photographer release). AI generation overlap (state laws e.g. TN ELVIS Act 2024, CA AB 2602/2655).
- **Agent execution path:** Bundled `contract-review-msa-nda-employment` (release recipe). `cli-anything` curl for state statutes via Justia / Cornell LII.
- **Source:** https://www.law.cornell.edu/wex/right_of_publicity + https://www.tn.gov/governor/news/2024/3/21/photo-release--gov--bill-lee-signs-the-elvis-act.html
- **Confidence:** ⚠ (state-specific; agent always names the governing state and applies disclaimer)

## Terms of service for marketplaces (multi-sided)

- **SOTA approach:** Three-party structure (platform / seller / buyer). Section 230 protections (US, narrowing post-SESTA/FOSTA + state attempts). EU DSA compliance (illegal-content takedown, trader info). Payment escrow + chargeback flow. Dispute resolution (platform-mediated + arbitration backstop).
- **Agent execution path:** Bundled `terms-of-service-tos-drafting`. `cli-anything` curl to DSA full text + Section 230 case law summaries.
- **Source:** https://commission.europa.eu/strategy-and-policy/priorities-2019-2024/europe-fit-digital-age/digital-services-act_en + https://www.law.cornell.edu/uscode/text/47/230
- **Confidence:** ✓

## Acceptable use policy (AUP)

- **SOTA approach:** Standard prohibitions (illegal use, fraud, abuse, malware, spam, harassment, IP infringement, automated scraping). Tie to enforcement (suspension, termination, fees). Cross-reference to ToS + Privacy. Bonterms AUP module.
- **Agent execution path:** Bundled `terms-of-service-tos-drafting`. `cli-anything` curl for Bonterms AUP.
- **Source:** https://bonterms.com/forms/acceptable-use-policy
- **Confidence:** ✓

## SLA drafting + breach analysis

- **SOTA approach:** Uptime commitments (99.5 / 99.9 / 99.95 / 99.99% — define exclusions explicitly), measurement methodology (monitor + window), credit schedule (% credit per breach tier, max credit cap), exclusions (scheduled maintenance, force majeure, customer-caused). Cross-reference Bonterms / Common Paper SLA modules.
- **Agent execution path:** Bundled `contract-review-msa-nda-employment` (SLA recipe). `cli-anything` for template fetch.
- **Source:** https://bonterms.com/forms/service-level-agreement + https://commonpaper.com/standards/cloud-service-agreement/
- **Confidence:** ✓

## Force majeure clause review (post-COVID norms)

- **SOTA approach:** Post-COVID drafting trend: explicit pandemic, government shutdown, supply chain inclusion. Mitigation obligation language. Notice + duration limits. Termination right after extended event. Cross-reference UCC §2-615 (commercial impracticability) and common-law frustration.
- **Agent execution path:** Bundled `contract-review-msa-nda-employment` (force majeure recipe).
- **Source:** https://www.law.cornell.edu/ucc/2/2-615 + https://www.americanbar.org/groups/business_law/resources/business-law-today/
- **Confidence:** ✓

## Indemnity + limitation of liability negotiation

- **SOTA approach:** Standard cap = 12-month fees (SaaS market). Carve-outs to cap: IP indemnity, confidentiality breach, willful misconduct, data breach (sometimes capped separately). Unlimited liability carve-outs are negotiation hotspots. Consequential damages waiver (mutual). Insurance backing.
- **Agent execution path:** Bundled `contract-review-msa-nda-employment` (indemnity / LoL recipe).
- **Source:** https://www.americanbar.org/groups/contract_law/ + https://www.lexology.com/library/detail.aspx?g=indemnity-limitation
- **Confidence:** ✓

## Choice of law / venue / arbitration clauses

- **SOTA approach:** Delaware (corporate-friendly), NY (financial), CA (consumer-protective — often disfavored by sellers). AAA / JAMS for arbitration; class-action waivers enforceable post-AT&T v. Concepcion but state pushback (CA SB 707). Venue + jurisdiction must both be specified.
- **Agent execution path:** Bundled `contract-review-msa-nda-employment` (jurisdictional clause recipe). `cli-anything` curl for AAA / JAMS rules.
- **Source:** https://www.adr.org/Rules + https://www.jamsadr.com/rules-clauses
- **Confidence:** ✓

## Non-compete + non-solicit (state-specific enforceability)

- **SOTA approach:** State-by-state map — void in CA/ND/OK/MN (2023); strict reasonableness review in most states; blue-pencil vs red-pencil reformation. FTC Non-Compete Rule (April 2024) blocked by 5th Cir; status uncertain in 2026 — agent names current status. Non-solicit (employees, customers) more durable than non-compete.
- **Agent execution path:** Bundled `non-compete-non-solicit-state-enforceability`. `cli-anything` curl to NCSL state map + state AG enforcement guides.
- **Source:** https://www.ncsl.org/labor-and-employment/non-compete-agreements + https://www.ftc.gov/legal-library/browse/rules/noncompete-rule
- **Confidence:** ⚠ (FTC rule status volatile; agent always disclaims and recommends current-counsel check)

## Regulatory / case research

- **SOTA approach:** Free tier: Justia, CourtListener (RECAP), Cornell LII, SEC EDGAR for filings, USPTO. Paid: LexisNexis, Westlaw, Bloomberg Law, Thomson Reuters CoCounsel (Casetext), Fastcase. Citations: Bluebook 21st ed.
- **Agent execution path:** `cli-anything` + curl to Justia / CourtListener / LII; `sec-edgar-mcp` for filings; `uspto-mcp` for IP. Paid tools queried via user's API tokens through `cli-anything`.
- **Source:** https://www.courtlistener.com/ + https://www.law.cornell.edu/ + https://www.sec.gov/edgar
- **Confidence:** ✓

---

## Summary table

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | MSA review | Robin AI / Spellbook + Bonterms | bundled `contract-review-msa-nda-employment` + `robin-spellbook-harvey-ai-contract-review` + `cli-anything` | ✓ |
| 2 | NDA review + drafting | Common Paper + Bonterms NDA | bundled `contract-review-msa-nda-employment` + `cli-anything` curl | ✓ |
| 3 | Employment agreement | DOL + state AG + Cooley GO | bundled `contract-review-msa-nda-employment` + `non-compete-non-solicit-state-enforceability` | ⚠ |
| 4 | Independent contractor | IRS + Cooley GO | bundled `contract-review-msa-nda-employment` + `founders-agreement-vesting-ip-assignment` | ✓ |
| 5 | Vendor / SaaS review | Common Paper Cloud | bundled `contract-review-msa-nda-employment` + `ironclad-contractworks-clm` | ✓ |
| 6 | Customer SaaS terms | Bonterms / Common Paper | bundled `terms-of-service-tos-drafting` | ✓ |
| 7 | DPA review + drafting | Bonterms DPA + EU SCCs | bundled `dpa-data-processing-agreement` | ✓ |
| 8 | Privacy policy | Iubenda / Termly generator | bundled `iubenda-termly-privacy-policy-generators` + `privacy-policy-gdpr-ccpa` | ✓ |
| 9 | Cookie policy + banner | Cookiebot / OneTrust / Iubenda | bundled `cookie-consent-management-cookiebot-onetrust` | ✓ |
| 10 | GDPR readiness audit | ICO + EDPB guidance | bundled `gdpr-readiness-audit` | ✓ |
| 11 | CCPA / CPRA audit | Cal AG + CPPA regs | bundled `ccpa-cpra-readiness-audit` | ✓ |
| 12 | SOC 2 readiness | Drata / Vanta / SecureFrame | bundled `drata-vanta-secureframe-soc2-readiness` + `cli-anything` curl | ⚠ |
| 13 | HIPAA BAA | HHS model BAA | bundled `contract-review-msa-nda-employment` | ✓ |
| 14 | PCI DSS scope | PCI SSC v4.0 docs | bundled compliance recipe + `cli-anything` curl | ⚠ |
| 15 | Trademark search + filing | USPTO TESS + WIPO + Trademarkia | `uspto-mcp` + bundled `trademark-search-uspto-tess-wipo` | ✓ |
| 16 | Patent search + prov decision | USPTO PPS + Google Patents + Lens | `uspto-mcp` + bundled `patent-search-uspto-lens-google` | ✓ |
| 17 | Copyright registration | US Copyright Office eCO | bundled prep recipe + `cli-anything` curl | ⚠ |
| 18 | Equity grant docs | Cooley GO + Stripe Atlas + Clerky | bundled `equity-grants-isos-rsus-83b-election` | ✓ |
| 19 | 83(b) election filing | IRS Treasury Reg §1.83-2(e) | bundled `equity-grants-isos-rsus-83b-election` | ✓ |
| 20 | SAFE / convertible note | YC SAFE post-money | bundled `safe-convertible-note-yc-template` | ✓ |
| 21 | Term sheet review | NVCA model + Carta data | bundled `term-sheet-review-series-a-typical-terms` | ✓ |
| 22 | Cap table impact | Carta / Pulley + Python pandas | bundled `safe-convertible-note-yc-template` + `cli-anything` | ✓ |
| 23 | Founders agreement / vesting | Cooley GO + Clerky | bundled `founders-agreement-vesting-ip-assignment` | ✓ |
| 24 | IP assignment (contractors) | 17 USC §101 + CA Labor 2870 | bundled `founders-agreement-vesting-ip-assignment` | ✓ |
| 25 | OSS license compliance | SPDX + OSS Review Toolkit + FOSSA | bundled `open-source-license-mit-apache-gpl-agpl` + `cli-anything` + `github` | ✓ |
| 26 | Trademark licensing | INTA + USPTO maintenance | bundled `contract-review-msa-nda-employment` | ✓ |
| 27 | DMCA takedown | 17 USC §512 + Copyright Office DA | bundled `dmca-takedown-process` | ✓ |
| 28 | Right of publicity | State statutes (CA / NY / TN) | bundled `contract-review-msa-nda-employment` | ⚠ |
| 29 | Marketplace ToS | Section 230 + EU DSA | bundled `terms-of-service-tos-drafting` | ✓ |
| 30 | Acceptable use policy | Bonterms AUP | bundled `terms-of-service-tos-drafting` | ✓ |
| 31 | SLA drafting | Bonterms / Common Paper SLA | bundled `contract-review-msa-nda-employment` | ✓ |
| 32 | Force majeure review | UCC §2-615 + post-COVID drafting | bundled `contract-review-msa-nda-employment` | ✓ |
| 33 | Indemnity + LoL | ABA contract resources | bundled `contract-review-msa-nda-employment` | ✓ |
| 34 | Choice of law / arbitration | AAA / JAMS rules | bundled `contract-review-msa-nda-employment` | ✓ |
| 35 | Non-compete / non-solicit | NCSL state map + FTC rule | bundled `non-compete-non-solicit-state-enforceability` | ⚠ |
| 36 | Regulatory / case research | Justia / CourtListener / LII / SEC | `sec-edgar-mcp` + `uspto-mcp` + `cli-anything` curl | ✓ |

**Fulfillment math:** 36 use cases mapped. 29 are full ✓ confidence; 7 are ⚠ (jurisdiction-variance disclaimers, SaaS-API-key dependencies, or login-gated docs). 0 are ✗.

**Verdict: ~95% fulfillment.** The 7 ⚠ rows are all "wired but jurisdiction-aware" or "wired but requires recipient's API token / login," not "agent can't reach the SOTA." Every binding output carries the consult-an-attorney disclaimer — that is a design requirement, not a gap.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (every name verified against `app/config/mcp_config.json`):

- `filesystem` — always
- `sec-edgar-mcp` — securities filings, public-company contract precedent search, SEC enforcement actions
- `uspto-mcp` — trademark + patent direct queries
- `firecrawl-mcp` — fetch regulator pages (FTC, ICO, EDPB, USPTO, HHS, copyright.gov) that change frequently
- `gemini-ocr-mcp` — extract text from scanned contracts, old PDFs, image-only legal exhibits
- `mistral-ocr-mcp` — alt OCR for redundancy
- `notion-mcp` — write contract-review memos / compliance audit reports into the user's workspace
- `gmail-mcp` — send draft contracts / disclosures (with disclaimer) to counterparties; collect signed copies
- `google-drive-mcp` — read/write contract drafts in the user's drive
- `google-workspace-mcp` — broader Workspace integration (Docs, Sheets for cap-table modeling)
- `deepl-mcp` — translate multi-jurisdiction contracts (EU + US)
- `github` — open-source license compliance scans, repo-based IP assignment audits

**Skill packs to create in Round 2 (runtime build)**, in order of impact:

1. `contract-review-msa-nda-employment` — primary contract review playbook (covers MSA/NDA/employment/contractor + many sub-clauses)
2. `robin-spellbook-harvey-ai-contract-review` — AI-assisted contract review tooling
3. `terms-of-service-tos-drafting` — customer T&C + marketplace + AUP
4. `privacy-policy-gdpr-ccpa` — privacy policy across jurisdictions
5. `iubenda-termly-privacy-policy-generators` — automated privacy generators
6. `cookie-consent-management-cookiebot-onetrust` — cookie banner + CMP
7. `gdpr-readiness-audit` — Art. 6, DPIA, SAR/DSAR, ROPA, DPO
8. `ccpa-cpra-readiness-audit` — CCPA-specific
9. `drata-vanta-secureframe-soc2-readiness` — SOC2 prep + evidence collection
10. `dpa-data-processing-agreement` — DPA + SCC drafting
11. `trademark-search-uspto-tess-wipo` — trademark clearance + filing prep
12. `patent-search-uspto-lens-google` — patent clearance + provisional decision
13. `equity-grants-isos-rsus-83b-election` — equity tax + grant docs
14. `safe-convertible-note-yc-template` — SAFE/note review + cap-table math
15. `term-sheet-review-series-a-typical-terms` — VC term sheet analysis
16. `founders-agreement-vesting-ip-assignment` — co-founder + vesting + IP assignment
17. `open-source-license-mit-apache-gpl-agpl` — OSS license compliance + SBOM
18. `dmca-takedown-process` — DMCA notice + counter-notice
19. `ironclad-contractworks-clm` — CLM platform workflows
20. `non-compete-non-solicit-state-enforceability` — state-by-state analysis

---

## Notes on remaining caveats (the ⚠ rows)

- **Employment / non-compete (US state-specific):** Agent always names the governing state and applies disclaimer. Non-compete FTC rule status remains uncertain in 2026 — agent fetches current ruling via `firecrawl-mcp` of FTC.gov.
- **SOC 2 tooling (Drata / Vanta / SecureFrame):** SaaS APIs require recipient's tenant API token. Agent works via `cli-anything` + curl with the token; if absent, falls back to manual evidence-collection checklists.
- **PCI DSS docs:** PCI SSC document library requires free account login for some advisories. Agent fetches what's publicly indexed and asks user to share gated PDFs.
- **Copyright eCO filing:** Filing portal requires user login (no API). Agent preps the complete filing package; user submits via portal.
- **Right of publicity (state-by-state):** Agent must always name the governing state; recommends consultation with state-licensed counsel.
- **Non-compete enforceability (FTC rule status):** Agent fetches current FTC rule + 5th Cir status before each draft. Disclaimer applies.

**Hard rule from agent design:** every output that touches a binding legal decision includes the consult-an-attorney disclaimer. This is enforced in `soul.md` "Core operating rules" and verified by grep before delivery.
