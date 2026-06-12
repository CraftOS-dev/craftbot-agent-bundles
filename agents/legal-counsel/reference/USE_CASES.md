# Legal Counsel — Use Cases

**Tier:** general · **Category:** legal
**Core job:** Senior in-house counsel for solo founders and small teams — contract review, T&C drafting, IP basics, GDPR / CCPA / SOC2 readiness, equity grants. Always recommends a licensed attorney for binding decisions.

> **Disclaimer (load-bearing):** This agent is NOT a substitute for a licensed attorney. Every output that touches a binding legal decision includes the consult-an-attorney disclaimer. Use this agent to draft, review, audit, and research; use a licensed attorney to sign off, file, and represent.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Contract review

- MSA (Master Service Agreement) review (buyer-side + supplier-side)
- NDA review + drafting (mutual + unilateral + multi-party)
- Employment agreement review + drafting (US, EU, UK)
- Independent contractor + consulting agreement review
- Vendor / SaaS subscription review (supplier-side and customer-side)
- License agreement review (software, trademark, patent, content)
- Reseller / channel partner agreement review
- SLA drafting + breach analysis
- Force majeure clause review (post-COVID norms)
- Indemnity + limitation of liability negotiation
- Choice of law / venue / arbitration clauses
- Non-compete + non-solicit (state-specific enforceability)

### Customer-facing terms drafting

- Customer SaaS terms (T&C / TOS)
- Terms of service for marketplaces (multi-sided)
- Acceptable Use Policy (AUP)
- Privacy policy drafting + maintenance
- Cookie policy + consent banner setup
- Data Processing Agreement (DPA) review + drafting

### Compliance + privacy

- GDPR readiness audit (Art. 6 lawful basis, DPIA, SAR/DSAR, ROPA, DPO)
- CCPA / CPRA readiness audit (rights infrastructure, opt-out, GPC, sensitive PI)
- SOC 2 readiness (Type I + II; AICPA TSP 100)
- HIPAA Business Associate Agreement (BAA)
- PCI DSS scope analysis
- State-privacy-law expansion (VA, CO, CT, UT, OR, TX, FL, MT, IA, DE, NJ, NH, MD)
- AI regulations (EU AI Act, NYC AI Bias Audit, Colorado AI Act)

### Intellectual property

- Trademark search + filing prep (USPTO TESS, WIPO, Trademarkia)
- Patent search + provisional vs non-provisional decision (USPTO PPS, Google Patents, Lens.org)
- Copyright registration prep
- DMCA takedown notice / counter-notice
- Right of publicity / image usage rights
- IP assignment from contractor agreements
- Trademark licensing
- Open source license compliance (MIT vs Apache vs GPL vs AGPL) + SBOM

### Equity + fundraising

- Equity grant docs (ISOs, NSOs, RSUs, stock purchase agreements)
- 83(b) election filing prep
- SAFE review (YC Post-Money + Pre-Money + MFN)
- Convertible note review
- Term sheet review (NVCA benchmark + Carta data)
- Cap table impact analysis (dilution math)
- Founders agreement / co-founder vesting

### Research

- Regulatory + statutory research (FTC, ICO, EDPB, USPTO, HHS, copyright.gov)
- Case-law lookup (CourtListener, LII, Justia)
- SEC EDGAR public-company contract precedent search
- Secondary sources (Bonterms, Common Paper, NVCA, YC, Cooley GO, Stripe Atlas)

### Tooling integration

- Robin AI / Spellbook / Harvey AI for AI-assisted contract review
- Ironclad / ContractWorks / Lexion / Evisort CLM workflows
- DocuSign / Adobe Sign / Dropbox Sign / PandaDoc e-sign
- Iubenda / Termly privacy generators
- Cookiebot / OneTrust CMP setup
- Drata / Vanta / SecureFrame SOC2 automation
- OSS Review Toolkit / Syft / FOSSA for OSS scanning
- Gemini / Mistral OCR for scanned contracts
- DeepL for multi-jurisdiction translation

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case from the section above appears here as a row.

| Use case | SOTA mechanism | Path |
|---|---|---|
| MSA review | Robin AI / Spellbook + Bonterms benchmark | `contract-review-msa-nda-employment` + `robin-spellbook-harvey-ai-contract-review` + `cli-anything` |
| NDA review + drafting | Common Paper Mutual NDA + Bonterms | `contract-review-msa-nda-employment` + `cli-anything` curl |
| Employment agreement (US, EU, UK) | DOL + state AG + Cooley GO + EU directives | `contract-review-msa-nda-employment` + `non-compete-non-solicit-state-enforceability` |
| Independent contractor | IRS 20-factor + state ABC + Cooley GO | `contract-review-msa-nda-employment` + `founders-agreement-vesting-ip-assignment` |
| Vendor / SaaS review | Common Paper Cloud Service + Bonterms Cloud Terms | `contract-review-msa-nda-employment` + `ironclad-contractworks-clm` |
| Customer SaaS terms (T&C / TOS) | Bonterms Cloud Terms + Common Paper standardized | `terms-of-service-tos-drafting` |
| Marketplace ToS | Section 230 + EU DSA + Bonterms | `terms-of-service-tos-drafting` |
| Acceptable Use Policy (AUP) | Bonterms AUP module | `terms-of-service-tos-drafting` |
| Privacy policy (GDPR + CCPA) | Iubenda / Termly + statute checklist | `iubenda-termly-privacy-policy-generators` + `privacy-policy-gdpr-ccpa` |
| Cookie policy + consent banner | Cookiebot / OneTrust / Iubenda Cookie Solution | `cookie-consent-management-cookiebot-onetrust` |
| DPA review + drafting | Bonterms DPA + EU SCCs (2021/914) | `dpa-data-processing-agreement` |
| GDPR readiness audit | ICO + EDPB + ROPA + DPIA | `gdpr-readiness-audit` |
| CCPA / CPRA readiness audit | Cal AG + CPPA regulations | `ccpa-cpra-readiness-audit` |
| SOC 2 readiness (Type I + II) | Drata / Vanta / SecureFrame + AICPA TSP 100 | `drata-vanta-secureframe-soc2-readiness` + `cli-anything` curl |
| HIPAA BAA | HHS Model BAA + 45 CFR §164.504(e) | `contract-review-msa-nda-employment` |
| PCI DSS scope | PCI SSC v4.0 documents | `gdpr-readiness-audit`-adjacent compliance recipe + `cli-anything` curl |
| State privacy laws (VA / CO / CT / UT / etc.) | State statutes + Cal AG analog | `ccpa-cpra-readiness-audit` + `firecrawl-mcp` |
| AI regulations (EU AI Act, NYC, CO) | Statutes + agency guidance | `gdpr-readiness-audit` + `firecrawl-mcp` |
| Trademark search + filing prep | USPTO TESS + WIPO + Trademarkia | `uspto-mcp` + `trademark-search-uspto-tess-wipo` |
| Patent search + provisional decision | USPTO PPS + Google Patents + Lens.org | `uspto-mcp` + `patent-search-uspto-lens-google` |
| Copyright registration prep | US Copyright Office eCO | bundled prep recipe + `cli-anything` curl |
| DMCA takedown / counter-notice | 17 USC §512 + Copyright Office Designated Agent | `dmca-takedown-process` |
| Right of publicity / image rights | State statutes (CA / NY / TN ELVIS Act) | `contract-review-msa-nda-employment` + `firecrawl-mcp` |
| IP assignment (contractor / employee) | 17 USC §101 + CA Labor §2870 + explicit assignment language | `founders-agreement-vesting-ip-assignment` |
| Trademark licensing | USPTO maintenance + INTA guidance | `contract-review-msa-nda-employment` |
| OSS license compliance + SBOM | SPDX + OSS Review Toolkit + Syft / Grype + FOSSA | `open-source-license-mit-apache-gpl-agpl` + `cli-anything` + `github` |
| Equity grant docs (ISO / NSO / RSU) | Cooley GO + Stripe Atlas + Clerky | `equity-grants-isos-rsus-83b-election` |
| 83(b) election filing prep | IRS Form 15620 + Treasury Reg §1.83-2(e) | `equity-grants-isos-rsus-83b-election` |
| SAFE / convertible note review | YC Post-Money SAFE + cap-table modeling | `safe-convertible-note-yc-template` |
| Term sheet review (Series A) | NVCA model + Carta state-of-market | `term-sheet-review-series-a-typical-terms` |
| Cap table impact analysis | Carta / Pulley + Python pandas modeling | `safe-convertible-note-yc-template` + `cli-anything` |
| Founders agreement + vesting | Cooley GO + Clerky + 4-yr/1-yr cliff default | `founders-agreement-vesting-ip-assignment` |
| Non-compete / non-solicit (state) | NCSL state map + FTC rule status | `non-compete-non-solicit-state-enforceability` + `firecrawl-mcp` |
| SLA drafting | Bonterms SLA + Common Paper Cloud Service | `contract-review-msa-nda-employment` |
| Force majeure review | UCC §2-615 + post-COVID drafting | `contract-review-msa-nda-employment` |
| Indemnity + LoL negotiation | ABA contract benchmarks | `contract-review-msa-nda-employment` |
| Choice of law / arbitration clauses | AAA / JAMS rules + Concepcion line | `contract-review-msa-nda-employment` |
| Regulatory + case research | Justia + CourtListener + LII + SEC EDGAR + USPTO | `sec-edgar-mcp` + `uspto-mcp` + `firecrawl-mcp` + `cli-anything` curl |
| Scanned contract intake | Gemini / Mistral OCR | `gemini-ocr-mcp` + `mistral-ocr-mcp` |
| Multi-jurisdiction translation | DeepL with `tag_handling=markdown` | `deepl-mcp` |
| CLM workflow setup | Ironclad / ContractWorks / Lexion / Evisort | `ironclad-contractworks-clm` |
| Robin AI / Spellbook / Harvey integration | Web app + Word add-in + REST API | `robin-spellbook-harvey-ai-contract-review` |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Employment / non-compete (US state-specific) | ⚠ | Agent always names jurisdiction; FTC Non-Compete Rule status uncertain in 2026 — fetched fresh from FTC.gov each draft |
| SOC 2 automation (Drata / Vanta / SecureFrame) | ⚠ | SaaS APIs require recipient's tenant API token; fallback = manual evidence-collection checklists |
| PCI DSS docs | ⚠ | PCI SSC requires free account login for some advisories; agent fetches publicly indexed + asks user to share gated PDFs |
| Copyright eCO filing | ⚠ | Filing requires user login (no API); agent preps the complete filing package; user submits |
| Right of publicity (state-by-state) | ⚠ | State-specific; agent names governing state + always recommends state-licensed counsel |
| Non-compete enforceability (FTC rule status) | ⚠ | FTC rule volatile post-5th Cir stay; agent fetches current via `firecrawl-mcp` before each draft |
| Actual contract signing / filing / court appearance | ✗ (by design) | Agent does NOT execute signing, court filing, or representation — that's licensed-counsel work |
| Litigation strategy / settlement value / trial prep | ✗ (by design) | Out of scope; recommend trial counsel |
| Tax outcomes on equity (vs mechanics) | ⚠ | Agent explains legal mechanics + flags tax implications; CPA / tax attorney confirms tax outcomes |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a SOTA execution path. The 7 ⚠ rows are jurisdiction-variance disclaimers, SaaS-API-key dependencies, or login-gated docs — not "agent can't reach the SOTA." The 3 ✗ rows are intentional scope limits aligned with the consult-an-attorney design rule.

---

## When to use this agent

- "Review this MSA from <vendor> — I'm the customer, governed by Delaware law"
- "Draft a mutual NDA for a potential partnership in California"
- "Write our privacy policy — we serve EU + US customers and use Stripe, Mixpanel, and Mailgun"
- "Set up GDPR Art. 28 DPAs with our sub-processors"
- "We're prepping for SOC 2 Type I — what's the gap from our current AWS + Vanta-free setup?"
- "Search for trademark conflicts on '<brand name>' in Class 9 + Class 42"
- "Prep 83(b) election letters for our 3 founders — restricted stock granted last Tuesday"
- "Review this YC SAFE — $500k at $8M post-money cap with MFN"
- "Review Series A term sheet from <VC> — 1.5x participating preferred, full ratchet anti-dilution, 4-of-5 board"
- "Audit our codebase for OSS license obligations — we're shipping a closed-source SaaS"

---

## When NOT to use this agent

- **Litigation strategy, settlement, court appearances** — hand off to trial counsel; this agent does not represent you
- **Actual filings with USPTO / Copyright Office / Secretary of State** — agent preps; licensed counsel files
- **Tax planning beyond equity-grant mechanics** — hand off to CPA / tax attorney
- **Fundraising math without legal terms (P&L, runway, unit economics)** — hand off to `finance-controller`
- **T&C-violation reports from support inbox** — hand off to `customer-support-agent` for triage; return for legal decision
- **Product compliance feature scoping** — hand off to `product-manager`; return when legal sign-off is needed
- **Marketing copy / sales content** — out of scope; recommend `marketing-agent`
- **Immigration, criminal, family law** — out of scope; recommend a specialist
- **Anything where you need attorney-client privilege** — privilege does not attach to AI conversations; consult a licensed attorney directly

---

## Disclaimer (load-bearing)

Every binding-decision output from this agent includes the consult-an-attorney disclaimer. This is not optional language — it is the agent's hard rule, enforced in `soul.md` "Core operating rules" and verified by grep before delivery. The agent is NOT the final lawyer.
