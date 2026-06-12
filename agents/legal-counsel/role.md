# Legal Counsel — deep reference

This appends to `AGENT.md`. It is **not** in the agent's default context. Grep it when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "MSA review playbook", "NDA review playbook", "Employment agreement playbook", "Privacy policy checklist", "GDPR readiness checklist", "CCPA readiness checklist", "SOC2 readiness checklist", "Trademark search playbook", "Patent search playbook", "Equity grants reference", "83(b) election playbook", "SAFE review playbook", "Term sheet decision table", "Cap table modeling", "Founders agreement template", "OSS license obligation matrix", "DMCA takedown playbook", "Non-compete state map", "Antipattern catalog", "Disclaimer templates", "SOTA tool reference".

For provenance of any section, see `SOURCES.md` in this bundle and `reference/SOTA_USE_CASES.md`.

---

## Capability reference

Factual lists banished from `soul.md` (they don't drive turn-by-turn decisions but the agent grep-loads them on demand).

### Contract types in scope

- Master Service Agreement (MSA) — multi-engagement umbrella with SOW
- Statement of Work (SOW) — deal-specific under an MSA
- Non-Disclosure Agreement (NDA) — mutual, unilateral, multi-party
- Employment agreement — at-will (US) vs notice-based (EU / UK / AU)
- Independent contractor agreement — IRS 20-factor + state ABC test
- Consulting agreement — variant of contractor with deliverables
- Vendor / supplier agreement — buyer-side review
- SaaS subscription agreement — supplier-side and customer-side
- Customer T&C / Terms of Service (ToS)
- Acceptable Use Policy (AUP)
- Privacy policy
- Cookie policy
- Data Processing Agreement (DPA) — GDPR Art. 28
- Business Associate Agreement (BAA) — HIPAA 45 CFR §164.504(e)
- Service Level Agreement (SLA)
- License agreement — software, trademark, patent, content
- Reseller / distributor / channel partner agreement
- Affiliate / referral agreement
- Joint venture / JV agreement
- Asset purchase / stock purchase / merger agreement (review only — M&A counsel for deals)
- Founders agreement
- Co-founder vesting agreement
- IP assignment agreement
- Stock plan + grant docs (ISO, NSO, RSU, restricted stock purchase, early exercise)
- SAFE (post-money, pre-money)
- Convertible note
- Term sheet (Series Seed, A, B+)
- Stockholders agreement / Investor Rights Agreement / Voting Agreement / ROFR Agreement (NVCA model docs)
- Release / waiver / settlement (review only — recommend trial counsel for execution)

### Compliance regimes in scope

- GDPR (EU 2016/679 + EU member-state laws + UK GDPR post-Brexit)
- CCPA / CPRA (Cal. Civ. Code §1798.100 et seq., CPPA regulations)
- State privacy laws: VA CDPA, CO CPA, CT CTDPA, UT UCPA, OR OCPA, TX TDPSA, FL FDBR, MT, IA, DE, NJ, NH, MD (15+ as of 2026)
- SOC 2 (AICPA TSP 100; Trust Services Criteria — Security mandatory; Availability, Confidentiality, Processing Integrity, Privacy optional)
- HIPAA (45 CFR Parts 160, 162, 164) + HITECH
- PCI DSS v4.0
- COPPA (Children's Online Privacy Protection — 16 CFR Part 312)
- FERPA (educational records)
- GLBA (financial services privacy)
- ePrivacy Directive (EU 2002/58/EC + national implementations — cookies, marketing)
- CAN-SPAM (US email marketing) + CASL (Canada anti-spam)
- TCPA (US telephone consumer protection)
- ADA (accessibility — esp. websites; refs WCAG 2.2 AA via DOJ guidance)
- Section 5 FTC Act (unfair / deceptive practices)
- DSA + DMA (EU Digital Services Act + Digital Markets Act)
- AI regulations: EU AI Act, NYC AI Bias Audit Law, Colorado AI Act 2024

### IP regimes in scope

- US Patent (USPTO; utility, design, plant; provisional vs non-provisional)
- US Trademark (USPTO; TEAS Standard / TEAS Plus; Principal vs Supplemental Register)
- US Copyright (US Copyright Office; eCO portal)
- DMCA (17 USC §512)
- Trade secret (Defend Trade Secrets Act 2016 + state UTSA)
- International: Madrid Protocol (TM); PCT (Patent Cooperation Treaty); Berne Convention (Copyright); Hague Agreement (Industrial Design)

### Equity instruments in scope

- Incentive Stock Options (ISO) — IRC §422
- Non-Qualified Stock Options (NSO) — ordinary-income tax on exercise spread
- Restricted Stock — 83(b) election within 30 days
- Restricted Stock Units (RSU) — taxed on vesting (unless private and 83(i) election)
- Stock Appreciation Rights (SAR)
- Phantom Stock
- Employee Stock Purchase Plan (ESPP) — IRC §423 qualified
- Profits Interest (LLC) — Rev. Proc. 93-27 + 2001-43
- SAFE (Y Combinator: pre-money + post-money + MFN + valuation cap + discount variants)
- Convertible Note (interest, maturity, cap, discount, qualified financing)

### Funding rounds in scope (US C-corp default)

- Friends & Family (often common stock or SAFE)
- Pre-seed / Seed (SAFE or note typically; sometimes priced)
- Series Seed (priced — NVCA-light docs)
- Series A through E+ (full NVCA model docs)
- Bridge round (SAFE or note extending runway)
- Convertible round (cap-table-friendly)

### Document libraries (the agent reaches for first)

- **Common Paper** — NDA, Cloud Service, DPA, AUP, SLA, MSA (standardized + open)
- **Bonterms** — Cloud Terms, AUP, DPA, SLA, IDA (open template library)
- **Y Combinator** — SAFE (post-money default), MFN side letter, pro-rata side letter
- **Cooley GO** — Equity comp, founders stock, contractor, consulting, employment
- **Stripe Atlas** — Incorporation-bundle templates (also offered through Atlas program)
- **Clerky** — Cap-table + equity templates (incorporation + fundraising bundles)
- **NVCA Model Legal Documents** — Series A canonical: Term Sheet, Stock Purchase Agreement, Investor Rights Agreement, Voting Agreement, ROFR / Co-Sale Agreement, Restated Charter, Bylaws, Indemnification Agreement
- **AICPA TSP 100** — SOC 2 Trust Services Criteria
- **EU Commission SCC** — Module 1-4 (2021/914 set)
- **HHS Model BAA** — HIPAA BAA template
- **AAA / JAMS rules** — Arbitration clauses + venue
- **NAIC model laws** — Insurance regulatory baselines (referenced when applicable)

---

## MSA review playbook

1. **Confirm side, jurisdiction, deal type.** Are you buyer or seller? Governing state / country? Vendor SaaS, consulting services, hardware supply, IP licensing? Each shifts the redline priorities.
2. **Read the definitions section first.** Bad definitions break the rest of the contract. Specifically check: "Services", "Deliverables", "Confidential Information", "Affiliates", "Acceptance", "Effective Date".
3. **Walk the clause checklist (high → low priority):**
   - Term + termination (notice for convenience? for cause? cure period? effect on accrued fees?)
   - IP ownership (vendor retains vs assigns; carve-outs for pre-existing IP; licenses back)
   - Payment terms (invoice timing; net 30 / 60 / 90; late fees; disputed amounts; setoff)
   - SLA + remedies (uptime %; credits; cap on credits; sole-and-exclusive remedy?)
   - Warranties (what's promised; warranty period; warranty disclaimer)
   - Indemnification (mutual? IP indemnity for vendor? cap?)
   - Limitation of liability (cap amount — 12-month fees is market; carve-outs — IP indemnity, breach of confidentiality, gross negligence, data breach)
   - Confidentiality (term; return / destruction; residuals; permitted disclosures)
   - Data protection (data processor terms; SCC for EU transfers; sub-processor list)
   - Audit rights (frequency; notice; scope; cost allocation)
   - Compliance with laws (specific regulatory carve-outs)
   - Insurance (types + limits; additional insured)
   - Force majeure (post-COVID drafting; mitigation duty; termination right after extended event)
   - Assignment (consent required? Change-of-control consent?)
   - Governing law + venue + dispute resolution (negotiation → mediation → arbitration → litigation? Class waiver?)
   - Notices (method, address, deemed-received)
   - Entire agreement / order of precedence (between MSA / SOW / Order Form / website terms)
4. **Quantify each flag.** High / medium / low. Tie to likelihood + impact.
5. **Propose specific redlines.** Don't say "this is bad" — say "change Section X.Y from `<old>` to `<new>` because <reason>."
6. **Memo + redline.** Memo for the user (executive summary + flag list); redline for the counterparty.

### Concrete example flags

**Indemnification cap at 3-months fees with no carve-outs (vendor-side MSA, user is customer):**
- Risk: High. Below 2026 market (12 months is standard); no carve-outs means an IP infringement claim against vendor caps your recovery at the same level as a billing dispute.
- Redline: Push to 12-months fees as the base cap; carve-outs for IP indemnity, breach of confidentiality, data breach, willful misconduct, gross negligence (uncapped or 3-5x cap).
- Citation: ABA contract benchmarks; Common Paper Cloud Service Agreement Section 9.

**Auto-renewal for 12-month terms with 90-day non-renewal notice (vendor-side SaaS, user is customer):**
- Risk: Medium. Common pattern; predictable but easy to forget the deadline.
- Redline: Tighten to 30-day notice for non-renewal; require vendor to provide 60-day reminder before auto-renewal triggers (CA SB-1659 model).
- Citation: CA Bus. & Prof. Code §17602 (automatic renewal disclosure).

---

## NDA review playbook

1. **Mutual vs unilateral.** Mutual is default in 2026 for most B2B; unilateral when one party has clear info-asymmetry (e.g., M&A target sharing financials with bidder).
2. **Definition of Confidential Information.** Categories vs catch-all; written-marking requirement is dated and waivable in practice.
3. **Exclusions.** Standard: already known, independently developed, publicly available, required by law. Don't compromise these.
4. **Term.** 2-5 years for general business; perpetual for trade secrets specifically.
5. **Use restriction.** Tie to purpose. "For the purpose of evaluating a potential business relationship" — not unlimited.
6. **Return / destruction.** Both options. Allow electronic backups subject to ongoing confidentiality.
7. **No license / no obligation.** Standard recital — receiving party gets no license or commitment.
8. **Residuals.** Only accept residuals clause in narrow B2B IT contexts where unmemorized residual knowledge of personnel is unavoidable. Otherwise reject.
9. **Injunctive relief.** Standard — confidentiality breach causes irreparable harm; injunctive relief available without bond.
10. **Governing law / venue.** Match the underlying deal jurisdiction.

### Default: Common Paper Mutual NDA

Bonterms NDA + Common Paper Mutual NDA are the closest to "market" in 2026. Both are open templates; differences are stylistic (Common Paper uses checkbox cover sheet; Bonterms uses signature page with selected modules).

---

## Employment agreement playbook

### US (default state-specific)

1. **At-will status.** State explicitly; most US states are at-will-default but explicit is safer.
2. **Compensation.** Base, bonus structure, equity grant (if any), benefits, vacation, sick.
3. **Classification.** Exempt vs non-exempt (FLSA + state OT rules). Misclassification is the most common claim.
4. **Confidentiality + IP assignment.** Explicit assignment ("hereby assigns"); CA Labor Code §2870 carve-out for personal time / no-company-resources inventions.
5. **Non-compete.** Void in CA, ND, OK, MN (2023+). Strict-reasonableness review in most states. FTC Non-Compete Rule (April 2024) stayed by 5th Cir in August 2024; status uncertain in 2026 — fetch current.
6. **Non-solicit.** Employees and customers. More durable than non-compete; reasonable scope + duration.
7. **Severance + post-termination obligations.** Standard severance is 2-4 weeks for non-exec; 6-12 months for exec; equity acceleration on involuntary termination is exec-friendly.
8. **Choice of law / venue.** Employee-favorable state preferred by employees; employer typically pushes HQ state.
9. **Arbitration + class waiver.** Enforceable post-AT&T v. Concepcion. State pushback in CA (SB 707 on PAGA carve-out, AB 51 on mandatory arbitration of employment claims — blocked).
10. **Section 280G / 409A overlay.** Exec contracts only — golden parachute + deferred comp rules.

### EU

1. **Notice period.** Mandatory under EU directives + member-state law. Cannot be at-will.
2. **Termination grounds.** Must be objective / for-cause; many member states require notice + severance even for performance terminations.
3. **Probation period.** Typically 3-6 months, regulated.
4. **Working time directive.** Max 48-hour week; opt-outs in some states.
5. **Data protection.** Employee data is "personal data" under GDPR — lawful basis required (typically Art. 6(1)(b) contract performance + (f) legitimate interest balancing).
6. **Works council consultation.** Required for many termination + restructuring decisions in DE, NL, FR.

---

## Privacy policy checklist

GDPR Art. 13 + 14 mandatory elements (data collected directly from data subject vs from third parties):

- [ ] Identity + contact details of controller
- [ ] Contact of DPO if appointed
- [ ] Purposes of processing
- [ ] Lawful basis under Art. 6 (and Art. 9 if special-category data)
- [ ] Legitimate interests of controller (if Art. 6(1)(f))
- [ ] Recipients / categories of recipients (sub-processors)
- [ ] International transfer mechanism (SCC, BCR, adequacy decision, Art. 49 derogation)
- [ ] Retention period or criteria
- [ ] Data subject rights (access, rectification, erasure, restriction, portability, objection, no automated decision-making — including profiling)
- [ ] Right to withdraw consent (where Art. 6(1)(a) basis)
- [ ] Right to lodge complaint with supervisory authority
- [ ] Whether providing data is a statutory / contractual requirement + consequences
- [ ] Existence of automated decision-making + meaningful info about logic + consequences

CCPA §1798.130 + CPRA additions:

- [ ] Categories of personal info collected (per CCPA categories) — at or before collection
- [ ] Categories of sources
- [ ] Business or commercial purposes
- [ ] Categories of third parties shared with
- [ ] Right to know (specific pieces of info collected in last 12 months — CPRA extends beyond 12mo on request)
- [ ] Right to delete
- [ ] Right to correct (CPRA-new)
- [ ] Right to opt out of sale / share
- [ ] Right to limit use of sensitive personal info (CPRA-new)
- [ ] Right to non-discrimination
- [ ] "Do Not Sell or Share My Personal Information" link (homepage + collection points)
- [ ] Methods to submit requests (toll-free phone for businesses doing business primarily online — physical store waived)
- [ ] Verification process description

---

## GDPR readiness checklist

1. **Scope determination.** Material (processing of personal data — Art. 4(1)) + territorial (establishment in EU, or targeting EU, or monitoring EU subjects — Art. 3).
2. **Lawful basis mapping.** For every processing activity, name the Art. 6 basis (a-f). For special-category data, also Art. 9 condition.
3. **Legitimate Interests Assessment (LIA)** when Art. 6(1)(f). Three-part test: legitimate interest, necessity, balancing against data subject rights.
4. **Records of Processing Activities (ROPA)** — Art. 30. Required for organizations with > 250 employees or systematic processing or special-category data. Template: ICO ROPA tool.
5. **Privacy by Design + Default** — Art. 25.
6. **Data Protection Impact Assessment (DPIA)** when high-risk processing — Art. 35. Mandatory triggers: systematic monitoring of public areas; large-scale special-category; profiling for legal effects.
7. **Data Subject Rights handling.** 1-month response (extendable to 3 months for complex requests with notice). Free of charge for first request.
8. **Breach notification.** 72-hour to supervisory authority (Art. 33). Notification to data subjects without undue delay if high risk to rights and freedoms (Art. 34).
9. **DPO designation.** Required if public authority, or core activities = regular & systematic large-scale monitoring, or large-scale processing of special-category data — Art. 37.
10. **International transfers.** Adequacy decision (Andorra, Argentina, Canada commercial, Faroe Islands, Guernsey, Israel, IoM, Japan, Jersey, NZ, Republic of Korea, Switzerland, UK, US under EU-US Data Privacy Framework). Otherwise SCC (2021/914 set with TIA — Transfer Impact Assessment post-Schrems II) or BCR or Art. 49 derogations.
11. **Processor agreements.** Art. 28(3) mandatory contractual terms.
12. **Cookie consent.** ePrivacy Directive — consent before non-essential cookies. Strict in DE, FR, IT, ES; UK ICO guidance applies post-Brexit.

---

## CCPA readiness checklist

1. **Applicability.** For-profit doing business in CA + either: $25M+ gross revenue, 100k+ consumer households/devices/identifiers, or 50%+ revenue from selling/sharing personal info.
2. **Privacy notice at collection.** Categories collected + purposes + retention + rights — before or at collection.
3. **Full privacy policy.** Annual update.
4. **Rights infrastructure:**
   - Right to know (specific pieces in 12 months, CPRA extends on request)
   - Right to delete (with exceptions: complete transaction, security incident, free speech, etc.)
   - Right to correct (CPRA)
   - Right to opt out of sale / share (Sale = monetary or other valuable consideration; Share = cross-context behavioral advertising — CPRA-new)
   - Right to limit use of sensitive personal info (precise geolocation, racial/ethnic, religious, mail/email/text content, genetic, biometric, health, sex life/orientation, contents of mail/email/text, SSN, driver's license, financial account #)
   - Right to non-discrimination
   - Right to data portability
5. **"Do Not Sell or Share My Personal Information" link** — homepage + at collection.
6. **Sensitive PI limit link** — when applicable.
7. **GPC (Global Privacy Control) signal** — must respect; equivalent to opt-out request.
8. **Service provider agreements** — CPRA-specific contractual terms (CPRA §1798.140(ag)).
9. **Cal AG enforcement focus areas** — children's data, dark patterns, GPC signal compliance.
10. **CPPA enforcement** — California Privacy Protection Agency now lead enforcer (CPRA-created).

---

## SOC2 readiness checklist

1. **Pick framework version.** AICPA SOC 2 + Trust Services Criteria (TSP 100). Security = mandatory; Availability, Confidentiality, Processing Integrity, Privacy = optional.
2. **Pick Type I or II.** Type I = point-in-time (1-3 month prep). Type II = observation period (3-12 months) — what enterprise customers actually require.
3. **Choose automation platform.** Drata, Vanta, SecureFrame are the 2026 leaders. Drata = compliance-first features; Vanta = broadest catalog; SecureFrame = simpler UX. ALL three integrate with AWS, GCP, Azure, Okta, JumpCloud, GitHub, Slack, Asana, etc.
4. **Set up controls evidence collection.** Identity & access management; system operations; change management; risk mitigation; logical/physical access controls; security incident management; vendor risk management.
5. **Policy library.** Information security policy, access control policy, change management, incident response, business continuity, vendor management, acceptable use, data classification.
6. **Vendor security reviews.** Each subprocessor — SOC2 report + DPA + risk score.
7. **Penetration test.** Annual, by qualified third party.
8. **Risk assessment.** Annual; updated on material change.
9. **Auditor selection.** AICPA-registered CPA firm with cyber practice. Big 4 + Schellman + A-LIGN + Coalfire + Prescient Assurance are 2026 common.
10. **Bridge letter.** Between successive Type II periods to keep customers covered.

---

## Trademark search playbook

1. **Identify the mark + class.** Word mark vs design mark vs combined. Nice Classification (Class 9 = software, Class 35 = advertising/business, Class 42 = SaaS / IT services common for tech).
2. **USPTO TESS basic search.** Wordmark + variants (phonetic, plurals, near-misses, foreign equivalents). Note: TESS was redesigned in 2024 — current URL is `tmsearch.uspto.gov`.
3. **USPTO TESS expanded.** Cross-class (related goods/services); common-law marks via web + Google + Trademarkia.
4. **WIPO Global Brand Database.** International equivalents — 50+ jurisdictions.
5. **State trademark databases.** Each US state has its own (often less useful since federal preempts but still relevant for common-law).
6. **Domain + social-handle availability.** ICANN WHOIS + Namecheap + Instagram + X + TikTok handle check.
7. **Knock-out vs full clearance.** Knock-out is 2-3 hour pass; full clearance is 1-2 day deep dive — recommend full when filing budget supports.
8. **Filing prep.** TEAS Plus ($250/class) requires exact ID from USPTO Acceptable ID Manual + electronic communication. TEAS Standard ($350/class) allows custom ID + flexible communication. Use-in-commerce (§1(a)) requires specimen + first-use date; Intent-to-use (§1(b)) requires later Statement of Use within 6 months (extendable).
9. **Madrid Protocol filing for international.** Requires US base application/registration; filed through USPTO via Madrid Protocol Application; designated countries individually examine.
10. **Recommend TM attorney for actual filing.** Filing prep is in scope; submission requires counsel.

---

## Patent search playbook

1. **Scope determination.** Utility (process / machine / manufacture / composition of matter), design (ornamental design), plant (variety). Utility is what software/hardware founders ask about.
2. **Prior-art search lanes:**
   - USPTO Patent Public Search (`ppubs.uspto.gov`) — official US prior art.
   - Google Patents (`patents.google.com`) — best free interface, includes non-patent literature.
   - Lens.org — patent + scholar cross-reference.
   - EPO Espacenet — European + worldwide.
   - WIPO Patentscope — international.
3. **Search strategy.** Keyword + classification (CPC for current; IPC for legacy); inventor name; assignee company; citation chains (forward + backward).
4. **Patentability analysis.** Novelty (35 USC §102), non-obviousness (§103), utility (§101), eligibility (§101 abstract-idea exclusion post-Alice). Software-method patents have high §101 rejection rate.
5. **Provisional vs non-provisional.** Provisional ($60-300 micro entity / $130-300 small entity) buys 12 months priority + "patent pending" status; non-provisional ($400-1820+) starts substantive examination. File provisional fast if disclosure is imminent.
6. **Disclosure deadlines.** US has 1-year grace period after first public disclosure to file (35 USC §102(b)). Most other countries (EU, China, JP) require filing BEFORE any public disclosure. Always file before disclosing internationally.
7. **PCT filing for international.** Single application designating multiple jurisdictions; 30-month national phase deadline.
8. **Recommend patent attorney/agent.** Required to be registered with USPTO to prosecute applications. Filing prep is in scope; actual prosecution requires counsel.

---

## Equity grants reference

### ISO (Incentive Stock Option) — IRC §422

- **Holder requirement:** Employee only (not contractor, not consultant, not advisor).
- **Plan requirement:** Adopted by board; approved by shareholders within 12 months of adoption.
- **Term:** Max 10 years from grant (5 years if 10%+ shareholder).
- **Strike price:** ≥ FMV at grant (must be supported by 409A valuation). 10%+ shareholders: ≥ 110% FMV.
- **$100k vesting limit.** Aggregate FMV of ISOs vesting in any one calendar year capped at $100k (based on FMV at grant). Excess auto-converts to NSO.
- **Holding periods (for ISO favorable tax):** 2 years from grant + 1 year from exercise. Sale before = disqualifying disposition → ordinary income on spread.
- **AMT trigger:** ISO exercise spread is an AMT preference item — surprise AMT bill is the classic founder mistake.
- **Post-termination exercise:** 90 days (extendable in plan, but extension converts to NSO).

### NSO (Non-Qualified Stock Option)

- **Holder:** Anyone (employee, contractor, consultant, advisor, board).
- **Strike price:** ≥ FMV at grant (409A required) — else IRC §409A violations (immediate income + 20% penalty + interest).
- **Tax on exercise:** Ordinary income on spread (FMV at exercise − strike), even if not sold. Employer withholds.
- **Subsequent sale:** Capital gain/loss on (sale price − FMV at exercise).

### RSU (Restricted Stock Unit)

- **Promise of stock on vesting** (no exercise; no strike).
- **Tax on vesting:** Ordinary income on FMV at vest. Employer withholds (often via sell-to-cover or net-issuance).
- **Private-company RSU problem:** Liquidity event-triggered vesting historically; IRC §83(i) 2017 lets eligible private-company employees defer up to 5 years. Rarely used.
- **Public company default:** Quarterly vest.

### Restricted Stock (purchase agreement + vesting schedule)

- **Purchase at grant.** Pay strike price upfront (typically par value or FMV for early founders).
- **83(b) election.** 30 days from grant. Without it: ordinary income on FMV − purchase price as it vests. With it: ordinary income on FMV − purchase price at grant (often $0 if early); subsequent appreciation is capital gain.
- **Critical for founders + early employees with low FMV.**

### SAFE (Simple Agreement for Future Equity)

- **Post-Money SAFE (YC 2018+ default).** Investment / valuation cap = % ownership locked at signing, not at conversion. Easier dilution math.
- **Pre-Money SAFE (YC original).** Investment / (pre-money valuation + new SAFE money) — dilution depends on how much else converts in same round.
- **MFN side letter.** Most-Favored Nation — investor gets benefit of better terms offered to subsequent SAFEs/notes.
- **Pro-Rata Rights side letter.** Right to participate in subsequent priced rounds proportional to fully-diluted ownership.
- **Valuation Cap-Only vs Discount-Only vs Both.** Cap-only is dominant in 2026 for high-momentum rounds.

### Convertible Note

- **Like SAFE but with debt features:** interest (5-8%), maturity (18-24 months), automatic vs optional conversion at qualified financing.
- **Qualified financing threshold** — typically $1-2M.
- **Maturity event** — repayment vs conversion at cap vs conversion at most recent valuation.

---

## 83(b) election playbook

**This is the most-violated rule by founders. Surface it any time restricted stock comes up.**

1. **Trigger.** Restricted stock purchase (or early exercise of unvested options into restricted stock) where the stock is subject to substantial risk of forfeiture.
2. **Deadline.** 30 days from grant date. Strict. No extensions. Postmark date counts (file certified mail with return receipt).
3. **Filing.** As of 2024+, the IRS provides Form 15620 as a model election letter; users can still file a custom letter that meets Treasury Reg §1.83-2(e) content requirements:
   - Taxpayer name + address + SSN / TIN
   - Description of property
   - Date of transfer
   - Tax year
   - Nature of restrictions
   - FMV at time of transfer (without considering restrictions)
   - Amount paid for property
   - Statement that copies were furnished to person for whom services were performed
4. **Filing recipients:**
   - IRS service center where taxpayer files own return — certified mail with return receipt
   - Person for whom services performed (employer) — copy
   - Taxpayer retains copy for records
5. **No IRS receipt confirmation.** Keep the certified mail return receipt as proof.
6. **Tax consequence with 83(b):** Ordinary income on (FMV − purchase price) at grant. Subsequent appreciation = capital gain (long-term if held > 1 year). For early-stage where FMV ≈ purchase price, this is often $0 income at grant.
7. **Tax consequence WITHOUT 83(b):** Ordinary income as each vesting tranche releases — on FMV at vest minus purchase price. Catastrophic if company grows fast.

### Example timing

- Founder receives 1M shares of restricted stock on Jan 15, 2026 with 4-year vest. FMV = $0.0001/share (par). Purchase price = $100 total.
- WITH 83(b) filed by Feb 14, 2026: $0 income at grant ($100 paid − $100 FMV). All future appreciation = long-term capital gain after 1 year.
- WITHOUT 83(b): When 250k vest on Jan 15, 2027 and FMV is now $1/share: $249,975 ordinary income. Repeat each year.

---

## SAFE review playbook

1. **Variant identification.** YC Post-Money (default since 2018) vs YC Pre-Money (legacy). Modified by side letters (MFN, pro-rata).
2. **Economic terms:**
   - Valuation cap (lower cap = better for investor; founder dilution math runs against the cap)
   - Discount (typical 15-25% off priced-round share price)
   - Cap + discount: investor gets the better of the two
3. **Conversion trigger.** Qualified Equity Financing (typically priced round > $1M). At trigger: SAFE converts to preferred at lower of cap-implied price or discount-implied price.
4. **Liquidity event before priced round.** Cash-out: SAFE = max(investment amount, "as-if-converted" amount at cap).
5. **Dissolution.** SAFE holder is creditor for return of investment ahead of equity but behind debt.
6. **MFN side letter.** If subsequent SAFE/note has better terms, original investor can swap. Standard ask from sophisticated angels.
7. **Pro-rata side letter.** Right to participate in next priced round. Almost always negotiable.
8. **Modeling.** Post-Money SAFE makes math simpler: investor's % = investment / valuation cap (locked). Multiple SAFEs at different caps stack independently.

---

## Term sheet decision table (Series A typical terms)

| Term | Founder-friendly market (2026) | Investor-friendly variations | Negotiation lever |
|---|---|---|---|
| Liquidation preference | 1x non-participating | 1x participating with cap; 1.5-2x non-participating | Cap on participation; convert-to-common option |
| Anti-dilution | Broad-based weighted average | Narrow-based WA; full ratchet | Carve-outs (option pool refresh, conversions) |
| Pro-rata rights | Major investors only | All investors | Define "major investor" by check size |
| Board composition | Common 2 / Pref 1 / Independent 0 (Seed/A) — usually 3-5 total | Pref majority | Independent director seat |
| Protective provisions | Standard NVCA list | Expanded list (M&A, hire/fire CEO, budget, dividends, debt) | Trim to material items |
| Drag-along | Above majority of common + majority of preferred | Majority of preferred alone | Founder consent required (or board) |
| Tag-along / co-sale | Standard — pref can sell pro-rata if common sells | — | — |
| ROFR | Standard — company first, then investors | — | — |
| Information rights | Major investors only | All investors | Define major; restrict to financials + budget |
| Founder vesting | 4-year / 1-year cliff with double-trigger acceleration | Single trigger | Acceleration on CoC + termination |
| Option pool | Pre-money pool — 10-15% | Pre-money pool — 15-20% | Negotiate against post-money pool (investor dilution) |
| Dividends | Non-cumulative when declared | Cumulative | Reject cumulative |
| Conversion | 1:1 + adjustments | — | — |
| Pay-to-play | Standard NVCA carrot (lose preferred status if don't participate pro-rata in down rounds) | Stick (forced conversion to common) | Negotiate carrot vs stick |
| Redemption rights | None | Investor put after 5-7 years | Push to remove or extend |
| Founder reverse vesting / refresh | Often refreshed at A with new 3-4 year vest | — | Acceleration on involuntary termination |

---

## Cap table modeling

### Post-Money SAFE conversion math

For a single Post-Money SAFE with valuation cap $V and investment $I:

- Shares to SAFE holder at priced round = (Investment / Valuation Cap) × Post-Money Diluted Shares Outstanding
- Or simpler: SAFE holder ownership % (locked at signing) = I / V

### Pre-Money SAFE conversion (legacy YC SAFE)

- Share price = Pre-Money / (existing fully diluted + option pool refresh)
- SAFE conversion price = min(cap-implied price, discount × priced-round price)
- Shares = Investment / SAFE conversion price

### Series A dilution stack

For a $50M post-money round with $10M new investment + a $5M Post-Money SAFE at $25M cap:

1. SAFE converts first: $5M / $25M = 20% post-money lock
2. Series A: $10M / $50M = 20% post-money
3. Option pool refresh (say 10% post-money, pre-money): comes off pre-money — falls on existing holders
4. Existing common ownership = 100% − (SAFE 20%) − (Series A 20%) − (option pool refresh 10%) = 50% × ratio of pre-money common to total pre-money

### Python recipe (cli-anything friendly)

```python
# uvx python or pip install pandas
import pandas as pd
cap = pd.DataFrame([
    {"holder": "Founder A", "shares": 5_000_000, "type": "common"},
    {"holder": "Founder B", "shares": 5_000_000, "type": "common"},
    {"holder": "Option pool (allocated)", "shares": 2_000_000, "type": "option"},
    # SAFE expressed in $ and cap, not shares:
    {"holder": "SAFE Angel #1", "investment": 250_000, "cap": 8_000_000, "type": "post_money_safe"},
])
# Convert SAFEs at priced-round trigger; compute % ownership locked at cap = investment / cap.
```

---

## Founders agreement template

```markdown
# Founders Agreement — <Company Name>

## Parties
- Founder 1 (Founder A): name, role, address
- Founder 2 (Founder B): name, role, address

## Equity split + vesting
- Founder A: <X>% (<Y> shares)
- Founder B: <X>% (<Y> shares)
- Vesting: 4-year vest, 1-year cliff, monthly thereafter (standard)
- Acceleration:
  - Single trigger (CoC alone): 25% of unvested (negotiable)
  - Double trigger (CoC + involuntary termination within 12 months): 100% acceleration
- Pre-vested founder shares: full at start; reverse-vest with company repurchase right at cost
- Repurchase right on departure: company can repurchase unvested shares at purchase price; survives ROFR

## IP assignment
- Each founder hereby assigns to NewCo all IP related to the business made before or during the engagement
- Pre-existing IP: listed in Schedule A; explicitly excluded
- Includes inventions, code, designs, marks, trade secrets, copyrights

## Confidentiality
- Survives termination; perpetual for trade secrets

## Roles + responsibilities (advisory, not binding)
- Founder A: CEO — go-to-market, hiring, fundraising
- Founder B: CTO — product, engineering

## Decision-making
- Day-to-day: each founder for their domain
- Material decisions (fundraising, M&A, CEO change, dilution > 10%): mutual consent
- Tie-breaking: <independent advisor / board>

## Resignation + departure
- Notice period: 30 days
- Vested shares retained; unvested forfeited
- Non-compete: 12-month (subject to state enforceability)
- Non-solicit: 24-month employees + customers

## Dispute resolution
- Good-faith negotiation → mediation → AAA Commercial Arbitration → courts of <State>

## Governing law
- <State>, USA

## Disclaimer
- This document is informational. Both founders should engage a licensed attorney before signing.
```

---

## OSS license obligation matrix

| License | Type | Attribution? | Disclose source on distribution? | Disclose source on network use (SaaS)? | Patent grant? | Sub-license? |
|---|---|---|---|---|---|---|
| MIT | Permissive | Yes | No | No | No (implicit) | Yes |
| BSD-2-Clause | Permissive | Yes | No | No | No | Yes |
| BSD-3-Clause | Permissive | Yes | No | No | No | Yes |
| Apache 2.0 | Permissive | Yes + NOTICE file | No | No | Yes (explicit) | Yes |
| MPL 2.0 | Weak copyleft | Yes | File-level copyleft (modified files) | No | Yes | Yes |
| LGPL 2.1 / 3.0 | Library copyleft | Yes | Library code; linking allowed (LGPL) | No | LGPL 3.0: yes | Yes |
| GPL v2 | Copyleft | Yes | Whole work, on distribution | No (GPL = distribution copyleft only) | Yes (v2 implicit) | Yes (under GPL) |
| GPL v3 | Copyleft | Yes | Whole work, on distribution | No | Yes (explicit + anti-Tivoization) | Yes (under GPL) |
| AGPL v3 | Network copyleft | Yes | Whole work, on distribution + on SaaS use | YES | Yes | Yes (under AGPL) |
| SSPL v1 | Source-available (not OSI-approved) | Yes | Whole stack including all service infrastructure | YES | Yes | Restrictive |
| Elastic License 2.0 | Source-available (not OSS) | Yes | — | — | — | Restrictive |
| BUSL 1.1 | Time-delayed OSS | Yes | After change date (usually 4 years) → typically Apache 2.0 | — | — | Restrictive |
| CC0 | Public domain dedication | No | No | No | No | N/A |

### Scanning recipe

```bash
# OSS Review Toolkit (ORT) — most comprehensive 2026
ort analyze -i . -o ort-results/
ort scan -i ort-results/analyzer-result.yml -o ort-results/
ort evaluate -i ort-results/scan-result.yml --rules-file .ort/evaluator.rules.kts

# Or quick npm-only scan
npx license-checker --json --production > licenses.json

# Or Python only
pip install pip-licenses
pip-licenses --format=json --output-file=licenses.json

# SPDX SBOM via Syft (multi-ecosystem)
syft . -o spdx-json=sbom.spdx.json
```

---

## DMCA takedown playbook

### §512(c) Notification (taking content DOWN)

Required elements:

1. Physical or electronic signature of person authorized to act on behalf of owner
2. Identification of the copyrighted work claimed to have been infringed
3. Identification of the material that is claimed to be infringing AND information reasonably sufficient to permit the service provider to locate the material (URL)
4. Information reasonably sufficient to permit the service provider to contact the complaining party (address, phone, email)
5. A statement that the complaining party has a good faith belief that use is not authorized by the copyright owner, agent, or law
6. A statement that the information in the notification is accurate, AND under penalty of perjury, that the complaining party is authorized to act on behalf of the owner

### §512(g) Counter-Notification (getting content RESTORED)

Required elements:

1. Physical or electronic signature of the subscriber
2. Identification of the material removed + the location at which it appeared before removal
3. A statement under penalty of perjury that subscriber has a good faith belief that the material was removed as a result of mistake or misidentification
4. Subscriber's name, address, and telephone number
5. Statement consenting to jurisdiction of federal court in the district where subscriber's address is (or, if outside US, any judicial district in which the service provider may be found), AND acceptance of service of process

Service provider must:
- Forward counter-notice to original notifier
- Replace content in 10-14 business days unless original notifier sues

### DMCA Designated Agent registration

Required for service-provider safe harbor. File via copyright.gov DMCA Designated Agent Directory. $6 filing fee. Renew every 3 years.

---

## Non-compete state map (2026)

| State | Enforceability | Notes |
|---|---|---|
| California | Void (Bus. & Prof. Code §16600) | Strictest — even out-of-state choice of law overridden for CA employees |
| North Dakota | Void (Cent. Code §9-08-06) | — |
| Oklahoma | Void (15 OS §219A) | Limited carve-outs for sale-of-business |
| Minnesota | Void (Stat. §181.988, 2023) | Effective July 1 2023; no retroactive |
| Washington | Enforceable above wage threshold (~$120k employee / $250k contractor, 2024) | Strict notice + consideration rules |
| Massachusetts | Enforceable with strict requirements (G.L. c. 149 §24L, 2018) | Garden leave OR mutually agreed consideration |
| Texas | Enforceable if reasonable + supported by consideration | Strong blue-pencil tradition |
| Florida | Enforceable per Stat. §542.335 | Statutory framework favors employers |
| New York | Enforceable but case-law strict | NYC + state agency scrutiny on overreach |
| Illinois | Enforceable above wage threshold ($75k / $45k for non-solicit) | Strict notice + consideration |
| Colorado | Highly restricted (C.R.S. §8-2-113, 2022) | Limited to highly-compensated employees |
| Virginia | Limited (Code §40.1-28.7:8) | Low-wage employee carve-outs |
| Federal (FTC Rule) | Status uncertain in 2026 | Final rule April 2024; stayed by 5th Cir Aug 2024; supreme court silence; agent fetches current before drafting |

Non-solicit (employees + customers) is more durable than non-compete in nearly all states. 12-24 month + reasonable scope is market.

---

## Antipattern catalog

### Antipattern 1: Missing 83(b)

**BAD:** Founder accepts restricted stock grant on Day 1. Files nothing. 6 months later asks about tax.
**Why bad:** 30-day window expired. Vesting tranches now generate ordinary income year-over-year on FMV − $0 purchase price.
**GOOD:** File 83(b) within 30 days of grant via certified mail to IRS service center + copy to employer. Retain certified-mail return receipt.

### Antipattern 2: Non-compete in California

**BAD:** Standard 12-month non-compete in CA employee agreement, with choice-of-NY-law clause.
**Why bad:** CA Bus. & Prof. Code §16600 voids non-competes; CA courts apply CA law to CA employees regardless of choice-of-law (CA Lab. Code §925).
**GOOD:** Drop the non-compete for CA employees. Use a tight non-solicit (employees + customers, 12-24 months) + IP assignment + confidentiality. These hold up.

### Antipattern 3: "Work made for hire" alone for contractor IP

**BAD:** Contractor agreement says contractor work is "work made for hire" — no explicit assignment.
**Why bad:** 17 USC §101 "work for hire" only covers narrow categories (audiovisual works, contributions to collective works, translations, etc.). Software code is NOT in the list. Without explicit assignment, contractor may retain rights.
**GOOD:** Include both: "work made for hire" language as primary; "to the extent any work is not deemed work for hire, Contractor hereby assigns all right, title, and interest..." as backup.

### Antipattern 4: AGPL in closed-source SaaS

**BAD:** Developer pulls in MongoDB Community Server (SSPL) or an AGPL'd library in a closed SaaS product. Ships without disclosure.
**Why bad:** AGPL §13 triggers source-disclosure obligation when users interact with the modified work over a network. SSPL §13 extends further. Either license obligation propagates.
**GOOD:** Run OSS Review Toolkit before ship. Flag AGPL / SSPL / BUSL / Elastic License. Swap to permissive alternative or commercial license. Document SBOM.

### Antipattern 5: Copying privacy policy from another website

**BAD:** Founder copies a competitor's privacy policy verbatim into their site.
**Why bad:** (a) Copyright infringement on the policy text itself. (b) Disclosures don't match actual data practices — false statements to consumers expose to FTC §5 (unfair/deceptive) and state AG enforcement. (c) GDPR / CCPA-specific elements may not apply.
**GOOD:** Use Iubenda or Termly generator to build from scratch based on user's actual data flows. Verify against statute checklist. Update on every product change.

### Antipattern 6: No DPA with sub-processors

**BAD:** Startup serves EU customers, uses Stripe / AWS / Mailgun / Mixpanel. No DPA signed with any of them.
**Why bad:** GDPR Art. 28(3) requires a written contract between controller and processor covering specific terms. No DPA = direct breach.
**GOOD:** Sign each vendor's DPA (most have standard ones online — Stripe DPA, AWS DPA, etc.) AND maintain a sub-processor list in privacy policy. Update list before adding new sub-processors.

### Antipattern 7: Founder gives away too much equity in cap table

**BAD:** Three co-founders split 33/33/33. One leaves at month 9 (before cliff). 33% locked + leaves with all of it because no vesting.
**Why bad:** No vesting = no claw-back. Dead-equity cap-table = uninvestable.
**GOOD:** Day-1 founders agreement with 4-year vest, 1-year cliff, company repurchase right at cost on departure. Reverse-vest pre-vested shares.

### Antipattern 8: Filing trademark before clearance

**BAD:** Filing USPTO TEAS Plus application for a mark without searching first. USPTO Examiner finds prior registration — refusal under §2(d) likelihood of confusion.
**Why bad:** Application fee non-refundable ($250-350). Brand already shipped to market on the rejected mark.
**GOOD:** Knock-out search (TESS + WIPO + Trademarkia) before any branding commitment. Full clearance + opinion letter (from TM attorney) before filing.

---

## Disclaimer templates

### Standard (every binding-decision output)

> **Disclaimer:** This is informational guidance from an AI agent, not legal advice. Always consult a licensed attorney in your jurisdiction before signing, filing, or executing binding legal documents. No attorney-client relationship is formed by this communication.

### Long-form (memos, audits, multi-page outputs)

> **Disclaimer:** This document is informational guidance from an AI agent and does not constitute legal advice. The content reflects general principles and publicly available templates / statutes as of <date>. Laws vary by jurisdiction and change over time. No attorney-client relationship is formed by your use of this AI agent or by the delivery of this document. Before signing, filing, or executing any binding legal document, or before relying on this guidance for a material business decision, consult a licensed attorney in the relevant jurisdiction. The agent does not represent you in any matter.

### Privilege caveat (when user asks about confidentiality)

> Communications with an AI agent are NOT protected by attorney-client privilege. Privilege requires (a) an attorney licensed to practice law, (b) acting in that capacity, and (c) the communication for the purpose of legal advice. None of these apply here. Sensitive matters should be discussed with a licensed attorney.

---

## SOTA tool reference (June 2026)

Grep-friendly per-tool reference. Each entry points at the bundled skill pack with the full recipe. Use this when deciding "what tool should I use for X?" Use the linked skill when actually executing.

### Robin AI

AI-assisted contract review platform. Trained on legal data; produces redlines + plain-English summaries.

- Use: Web app + Microsoft Word add-in.
- Best for: First-pass redline of MSAs / NDAs / employment over 10 pages.
- API: Available for enterprise (REST). Webhook integration.
- Skill pack: `skills/robin-spellbook-harvey-ai-contract-review/SKILL.md`.
- Source: https://www.robinai.com/

### Spellbook

AI legal copilot for Microsoft Word. GPT-class drafting + clause suggestion + risk highlighting in Word.

- Use: Word add-in subscription.
- Best for: Drafting workflow in Word.
- Skill pack: `skills/robin-spellbook-harvey-ai-contract-review/SKILL.md`.
- Source: https://www.spellbook.legal/

### Harvey AI

Legal-specialized LLM platform. Enterprise-focused (Big Law).

- Use: Web app (enterprise).
- Best for: Reference for AI-legal SOTA; less relevant for solo / small-team workflows.
- Skill pack: `skills/robin-spellbook-harvey-ai-contract-review/SKILL.md`.
- Source: https://www.harvey.ai/

### LegalSifter

AI contract analysis with "Sifters" — concept detectors trained on legal patterns.

- Use: Web app + API.
- Best for: Custom-concept extraction across a contract corpus.
- Skill pack: `skills/contract-review-msa-nda-employment/SKILL.md` (alternatives section).
- Source: https://www.legalsifter.com/

### Ironclad

Enterprise CLM platform. Workflow automation, repository, AI clause discovery.

- Use: Web app + REST API.
- Best for: Recipient using Ironclad — integrate the agent's review output into existing workflows.
- API: Ironclad API (REST + webhooks).
- Skill pack: `skills/ironclad-contractworks-clm/SKILL.md`.
- Source: https://ironcladapp.com/

### ContractWorks

Mid-market CLM. Lighter than Ironclad; e-sig integrated.

- Skill pack: `skills/ironclad-contractworks-clm/SKILL.md`.
- Source: https://www.contractworks.com/

### Lexion

Mid-market CLM acquired by DocuSign (2024). Pre-execution workflow + repository.

- Skill pack: `skills/ironclad-contractworks-clm/SKILL.md`.
- Source: https://www.lexion.ai/

### Evisort / LinkSquares / Concord

Mid-market CLM alternatives. All include AI clause extraction.

- Skill pack: `skills/ironclad-contractworks-clm/SKILL.md`.
- Sources: https://www.evisort.com/ + https://linksquares.com/ + https://www.concord.app/

### DocuSign API

E-signature SOTA. REST + connectors.

- Install: `pip install docusign-esign` or `npm i docusign-esign`.
- Use: Envelope-create + recipients + signing-routing.
- Skill pack: `skills/ironclad-contractworks-clm/SKILL.md` (e-sign section).
- Source: https://developers.docusign.com/

### Adobe Sign / Dropbox Sign / PandaDoc

E-sign alternatives.

- Sources: https://developer.adobe.com/document-services/apis/sign/ + https://developers.hellosign.com/ + https://developers.pandadoc.com/

### Common Paper

Open standardized contract templates — NDA, Cloud Service, DPA, AUP.

- Use: Download template; customize for deal.
- Skill pack: `skills/contract-review-msa-nda-employment/SKILL.md` + `skills/terms-of-service-tos-drafting/SKILL.md`.
- Source: https://commonpaper.com/

### Bonterms

Open template library — Cloud Terms, AUP, DPA, SLA, IDA modules.

- Skill pack: `skills/terms-of-service-tos-drafting/SKILL.md`.
- Source: https://bonterms.com/

### Y Combinator SAFE

Default 2026 fundraise instrument for pre-priced rounds.

- Variants: Post-Money (default), Pre-Money (legacy), MFN, Cap-only, Discount-only, Cap-and-Discount.
- Skill pack: `skills/safe-convertible-note-yc-template/SKILL.md`.
- Source: https://www.ycombinator.com/documents

### Cooley GO

Free founder template library — equity comp, founders stock, employment, contractor.

- Skill pack: `skills/equity-grants-isos-rsus-83b-election/SKILL.md` + `skills/founders-agreement-vesting-ip-assignment/SKILL.md`.
- Source: https://www.cooleygo.com/documents/

### Stripe Atlas

Incorporation-bundle templates.

- Source: https://stripe.com/atlas

### Clerky

Cap-table + equity templates (incorporation + fundraising).

- Source: https://www.clerky.com/

### NVCA Model Legal Documents

Series A canonical docs.

- Skill pack: `skills/term-sheet-review-series-a-typical-terms/SKILL.md`.
- Source: https://nvca.org/model-legal-documents/

### USPTO TESS (tmsearch.uspto.gov)

US trademark search.

- Use: `uspto-mcp` MCP server OR direct web search.
- Skill pack: `skills/trademark-search-uspto-tess-wipo/SKILL.md`.
- Source: https://tmsearch.uspto.gov/

### USPTO Patent Public Search (ppubs.uspto.gov)

US patent search.

- Use: `uspto-mcp` MCP server OR direct web search.
- Skill pack: `skills/patent-search-uspto-lens-google/SKILL.md`.
- Source: https://ppubs.uspto.gov/

### Google Patents

Free patent search interface.

- Use: `cli-anything` + curl OR direct browse.
- Skill pack: `skills/patent-search-uspto-lens-google/SKILL.md`.
- Source: https://patents.google.com/

### Lens.org

Free patent + scholarly cross-reference.

- Skill pack: `skills/patent-search-uspto-lens-google/SKILL.md`.
- Source: https://www.lens.org/

### WIPO Global Brand Database

International trademark clearance.

- Source: https://www.wipo.int/branddb/en/

### Trademarkia

Fast common-law + USPTO clearance.

- Source: https://www.trademarkia.com/

### Iubenda

Privacy policy + cookie consent generator. Jurisdiction-aware; auto-update on regulation change.

- Install: Embed snippet + REST API.
- Skill pack: `skills/iubenda-termly-privacy-policy-generators/SKILL.md` + `skills/cookie-consent-management-cookiebot-onetrust/SKILL.md`.
- Source: https://www.iubenda.com/

### Termly

Alternative to Iubenda. Privacy policy + cookie consent + ToS generator.

- Skill pack: `skills/iubenda-termly-privacy-policy-generators/SKILL.md`.
- Source: https://termly.io/

### Cookiebot

Cookie scanner + CMP. IAB TCF v2.2 compliant.

- Install: Embed script + REST API.
- Skill pack: `skills/cookie-consent-management-cookiebot-onetrust/SKILL.md`.
- Source: https://www.cookiebot.com/

### OneTrust

Enterprise consent + privacy management.

- Skill pack: `skills/cookie-consent-management-cookiebot-onetrust/SKILL.md`.
- Source: https://www.onetrust.com/

### Osano / TrustArc

CMP alternatives.

- Sources: https://www.osano.com/ + https://trustarc.com/

### Drata

SOC 2 automation platform. Continuous monitoring + evidence collection.

- Install: REST API + integrations (AWS, GCP, Azure, Okta, GitHub, Asana, etc.).
- Skill pack: `skills/drata-vanta-secureframe-soc2-readiness/SKILL.md`.
- Source: https://drata.com/

### Vanta

SOC 2 / ISO 27001 / HIPAA / GDPR / PCI automation.

- Install: REST API.
- Skill pack: `skills/drata-vanta-secureframe-soc2-readiness/SKILL.md`.
- Source: https://www.vanta.com/

### SecureFrame

SOC 2 automation alternative.

- Skill pack: `skills/drata-vanta-secureframe-soc2-readiness/SKILL.md`.
- Source: https://secureframe.com/

### Thoropass (formerly Laika)

SOC 2 + auditor-in-a-box.

- Source: https://thoropass.com/

### Sprinto / Tugboat Logic / AuditBoard

Additional compliance automation.

- Sources: https://sprinto.com/ + https://www.tugboatlogic.com/ + https://www.auditboard.com/

### Carta

Cap-table + 409A valuation + equity admin.

- Install: REST API.
- Best for: Live cap-table modeling.
- Source: https://carta.com/

### Pulley

Carta alternative. Cap-table + equity admin.

- Source: https://pulley.com/

### AngelList Stack

Free formation + cap-table for early-stage.

- Source: https://www.angellist.com/stack

### OSS Review Toolkit (ORT)

Multi-ecosystem OSS license + vulnerability scanner.

- Install: `brew install ort` or via Docker.
- Use: `ort analyze -i . -o results/`; `ort scan -i results/analyzer-result.yml -o results/`.
- Skill pack: `skills/open-source-license-mit-apache-gpl-agpl/SKILL.md`.
- Source: https://github.com/oss-review-toolkit/ort

### FOSSA

Commercial OSS license + vulnerability scanner.

- Source: https://fossa.com/

### Snyk

Vulnerability + license scanning.

- Source: https://snyk.io/

### Syft + Grype

CLI SBOM + vulnerability scanning (Anchore).

- Install: `brew install syft grype`
- Use: `syft . -o spdx-json=sbom.spdx.json`; `grype sbom:sbom.spdx.json`.
- Skill pack: `skills/open-source-license-mit-apache-gpl-agpl/SKILL.md`.
- Source: https://github.com/anchore/syft

### SPDX License List

Canonical OSS license identifier list.

- Source: https://spdx.org/licenses/

### CourtListener (Free Law Project)

Free federal + state case law + PACER docket access (RECAP).

- Use: `cli-anything` curl to `courtlistener.com/api/rest/v3/`.
- Skill pack: research recipes in `skills/contract-review-msa-nda-employment/SKILL.md`.
- Source: https://www.courtlistener.com/

### Cornell Legal Information Institute (LII)

Free statute + regulation lookup. US Code + CFR + state codes.

- Use: `firecrawl-mcp` or `cli-anything` curl.
- Source: https://www.law.cornell.edu/

### Justia

Free secondary-source legal research.

- Source: https://www.justia.com/

### SEC EDGAR

Public-company filings (10-K, 10-Q, 8-K, S-1, DEF 14A, Form D, etc.).

- Use: `sec-edgar-mcp` MCP.
- Source: https://www.sec.gov/edgar

### LexisNexis / Westlaw / Bloomberg Law

Paid legal research platforms.

- Use: API access requires recipient's institutional credentials.
- Source: https://www.lexisnexis.com/ + https://www.thomsonreuters.com/en/products/westlaw.html + https://pro.bloomberglaw.com/

### Thomson Reuters CoCounsel (formerly Casetext)

AI-powered legal research + memo drafting.

- Source: https://www.thomsonreuters.com/en/cocounsel.html

### Fastcase / Casemaker

Lower-cost legal research platforms.

- Sources: https://www.fastcase.com/

### IRS Form 15620 (83(b) Model Election)

Model 83(b) election letter published by IRS 2024.

- Source: https://www.irs.gov/forms-pubs/about-form-15620

### EU Standard Contractual Clauses (SCC 2021/914)

EU Commission cross-border transfer mechanism.

- Source: https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en

### ICO (UK Information Commissioner's Office)

UK GDPR guidance + DPIA / ROPA templates.

- Source: https://ico.org.uk/

### EDPB (European Data Protection Board)

GDPR enforcement guidance + SCC clarifications.

- Source: https://edpb.europa.eu/

### California Privacy Protection Agency (CPPA)

CPRA enforcement + regulations.

- Source: https://cppa.ca.gov/

### HHS HIPAA Sample BAA

Model BAA from HHS.

- Source: https://www.hhs.gov/hipaa/for-professionals/covered-entities/sample-business-associate-agreement-provisions/

### FTC Non-Compete Rule

Final rule April 2024; stayed by 5th Cir August 2024; status uncertain in 2026.

- Source: https://www.ftc.gov/legal-library/browse/rules/noncompete-rule

### NCSL Non-Compete State Map

State-by-state non-compete enforceability tracker.

- Source: https://www.ncsl.org/labor-and-employment/non-compete-agreements

### AAA + JAMS Arbitration Rules

Commercial + employment arbitration rule sets.

- Sources: https://www.adr.org/Rules + https://www.jamsadr.com/rules-clauses

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Review this MSA" | `contract-review-msa-nda-employment` + `robin-spellbook-harvey-ai-contract-review` (if > 10pp) | Always confirm jurisdiction + side first |
| "Draft an NDA" | `contract-review-msa-nda-employment` | Start from Common Paper Mutual NDA |
| "Review this employment agreement" | `contract-review-msa-nda-employment` + `non-compete-non-solicit-state-enforceability` | Check state for non-compete |
| "Draft a contractor agreement" | `contract-review-msa-nda-employment` + `founders-agreement-vesting-ip-assignment` | IP assignment + classification critical |
| "Write our T&C / ToS" | `terms-of-service-tos-drafting` | Start from Bonterms / Common Paper |
| "Write our privacy policy" | `privacy-policy-gdpr-ccpa` + `iubenda-termly-privacy-policy-generators` | Confirm jurisdiction + data flows |
| "Set up cookie banner" | `cookie-consent-management-cookiebot-onetrust` | IAB TCF v2.2 for ad-supported |
| "Audit GDPR readiness" | `gdpr-readiness-audit` | Lawful basis mapping first |
| "Audit CCPA readiness" | `ccpa-cpra-readiness-audit` | Opt-out + GPC + sensitive PI |
| "Prep for SOC 2" | `drata-vanta-secureframe-soc2-readiness` | Type I before Type II |
| "Draft a DPA" | `dpa-data-processing-agreement` | Bonterms DPA + EU SCCs |
| "Search trademark for [mark]" | `trademark-search-uspto-tess-wipo` + `uspto-mcp` | TESS + WIPO + Trademarkia |
| "Search patent for [tech]" | `patent-search-uspto-lens-google` + `uspto-mcp` | PPS + Google + Lens |
| "Prepare equity grants" | `equity-grants-isos-rsus-83b-election` | 83(b) deadline alert |
| "Review YC SAFE" | `safe-convertible-note-yc-template` | Post-money default |
| "Review Series A term sheet" | `term-sheet-review-series-a-typical-terms` | NVCA benchmark + Carta data |
| "Draft founders agreement" | `founders-agreement-vesting-ip-assignment` | 4-yr / 1-yr cliff default |
| "Check OSS license obligations" | `open-source-license-mit-apache-gpl-agpl` + `github` MCP | ORT scan |
| "Draft DMCA takedown" | `dmca-takedown-process` | §512(c) elements |
| "What's our non-compete enforceability in [state]" | `non-compete-non-solicit-state-enforceability` | NCSL state map + current FTC rule status |
| "Research [statute / case]" | `firecrawl-mcp` + `sec-edgar-mcp` + `cli-anything` curl Justia / CourtListener / LII | Cite primary sources |
| "Extract text from scanned contract" | `gemini-ocr-mcp` + `mistral-ocr-mcp` | OCR-then-review |
| "Translate this contract (FR / DE / ES)" | `deepl-mcp` | Use `tag_handling=markdown` to preserve formatting |
| "Set up CLM workflow" | `ironclad-contractworks-clm` | Match user's existing platform |

---

## Closing rules

You are not the final lawyer. Every binding-decision output (a) names the governing jurisdiction, (b) cites primary statutes / regulations / cases / templates, (c) quantifies risk in high/medium/low tiers tied to likelihood × impact, (d) surfaces material deadlines, and (e) ends with the consult-an-attorney disclaimer. Templates start the draft; the user's licensed counsel finishes it.

The disclaimer is non-negotiable and is enforced by `soul.md` "Core operating rules" + the verification gate before delivery. Grep the output for "consult a licensed attorney" before sign-off.
