# Compliance Agent — deep reference

This appends to `AGENT.md`. It is **not** in the agent's default context. Grep it when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Framework cross-walk table", "SOC 2 readiness playbook", "ISO 27001 readiness playbook", "GDPR readiness checklist", "CCPA readiness checklist", "HIPAA readiness checklist", "PCI DSS readiness checklist", "AML KYC program playbook", "Vendor risk playbook", "TPRM lifecycle playbook", "Pentest coordination playbook", "Vulnerability management playbook", "Security awareness playbook", "Phishing simulation playbook", "Incident response playbook", "Breach notification matrix", "DLP classification playbook", "Policy library reference", "AI governance playbook", "EU AI Act risk classification", "Whistleblower program playbook", "Risk register reference", "Regulatory horizon table", "Vendor security questionnaire playbook", "Antipattern catalog", "Disclaimer templates", "SOTA tool reference".

For provenance of any section, see `SOURCES.md` in this bundle and `reference/SOTA_USE_CASES.md`.

---

## Capability reference

Factual lists banished from `soul.md` (they don't drive turn-by-turn decisions but the agent grep-loads them on demand).

### Frameworks in scope

- **SOC 2** (AICPA TSP 100 + 2017 + 2022 updates) — Trust Services Criteria: Security (mandatory; CC1.1-CC9.2 = 9 Common Criteria categories), Availability (A1.1-A1.3), Confidentiality (C1.1-C1.2), Processing Integrity (PI1.1-PI1.5), Privacy (P1.1-P8.1). Type I (point-in-time) + Type II (3-12mo observation).
- **ISO/IEC 27001:2022** — ISMS + 93 Annex A controls in 4 themes (Organizational A.5, People A.6, Physical A.7, Technological A.8). Mandatory clauses 4-10. SoA, risk treatment, internal audit, management review. Cert: Stage 1 + Stage 2 + Surveillance years 1-2 + Recert year 3.
- **ISO/IEC 27017:2015** — Cloud service security extensions for 27002.
- **ISO/IEC 27018:2019** — PII protection in public cloud (processor).
- **ISO/IEC 27701:2019** — PIMS extension to 27001 (Privacy Information Management System).
- **ISO/IEC 42001:2023** — AI Management System (AIMS). First AIMS certifications late-2024 onwards. Maps to EU AI Act high-risk obligations.
- **NIST CSF 2.0** (2024) — Six Functions: Govern (new in 2.0), Identify, Protect, Detect, Respond, Recover. Anchor for cross-framework mapping.
- **NIST SP 800-53 Rev. 5** — Federal control catalog (1100+ controls; baseline for FedRAMP, StateRAMP, CMMC overlap).
- **NIST SP 800-171** — CUI in non-federal systems (110 controls).
- **NIST SP 800-30 Rev. 1** — Risk assessment.
- **NIST SP 800-61 Rev. 3** (April 2025) — Incident response aligned to CSF 2.0.
- **NIST SP 800-66 Rev. 2** (2024) — HIPAA Security Rule guidance.
- **NIST AI RMF 1.0** — AI Risk Management Framework.
- **GDPR (EU 2016/679)** + UK GDPR (post-Brexit) + Member State implementations.
- **CCPA / CPRA** (Cal. Civ. Code §1798.100 et seq.) + CPPA regulations.
- **US state privacy laws (19+ as of 2026):** VA CDPA, CO CPA, CT CTDPA, UT UCPA, OR OCPA, TX TDPSA, FL FDBR, MT, IA, DE, NJ, NH, MD, IN, KY, MN, NE, RI, TN.
- **LGPD** (Brazil), **PIPEDA** (Canada), **PIPL** (China), **APPI** (Japan), **APP** (Australia), **POPIA** (South Africa).
- **HIPAA** (45 CFR Parts 160 + 162 + 164) + HITECH.
- **PCI DSS v4.0 / v4.0.1** (effective March 2024; future-dated through March 2025).
- **Bank Secrecy Act (BSA)** + FinCEN guidance + OFAC sanctions + USA PATRIOT Act + AML Act 2020.
- **FATF** Recommendations 40+9 + Travel Rule R.16 + Mutual Evaluation Reports.
- **EU AML:** 6AMLD + AMLR + AMLD6 + AMLA + MiCA (crypto 2024 → 2026 enforcement).
- **UK MLR 2017** + FCA AML handbook.
- **EU AI Act** (Regulation 2024/1689; high-risk obligations effective Aug 2, 2026; GPAI obligations Aug 2025; bans Feb 2025).
- **EU NIS2 Directive** (transposition Oct 17, 2024; 2026 active enforcement).
- **EU DORA** (effective Jan 17, 2025 for financial sector + critical ICT third parties).
- **EU DSA + DMA** (Digital Services Act + Digital Markets Act).
- **EU Data Act** (effective Sept 12, 2025).
- **EU Cyber Resilience Act (CRA)** (manufacturer obligations Dec 2027).
- **SEC Cyber Incident Disclosure** (Rule 33-11216; Form 8-K Item 1.05 — 4 business days material).
- **NYDFS 23 NYCRR 500** (cybersecurity for NY-licensed financial entities; 500.17 = 72h breach).
- **CMMC 2.0** (DoD; Phase 1 effective 2025-Q4 onwards).
- **SOX** §302, §404, §806 (whistleblower).
- **COPPA** (16 CFR Part 312 — children online).
- **FERPA** (educational records).
- **GLBA** (financial privacy + Safeguards Rule + 2023 updates).
- **TCPA + CAN-SPAM + CASL** (electronic communications).
- **FTC Act §5** (unfair / deceptive practices — broad enforcement anchor).
- **ePrivacy Directive** (cookies + electronic marketing).
- **HHS OCR + state AG enforcement** (HIPAA + state privacy).

### Industry-specific overlays

- **Financial services:** FINRA Rule 4511 + SEC 17a-3/4 + Marketing Rule + 8-K cyber + Reg S-P + GLBA Safeguards + NYDFS.
- **Healthcare:** HIPAA + HITECH + 42 CFR Part 2 (substance use) + ONC Health IT Cures Act.
- **Pharma / medtech:** 21 CFR Part 11 + Quality System Reg + GxP + MDR (EU) + IVDR (EU).
- **Crypto / digital assets:** FinCEN + OFAC + SEC + CFTC + MiCA (EU 2024) + FATF Travel Rule + state money transmitter (MTL).
- **DoD contractors:** CMMC 2.0 + NIST SP 800-171 + DFARS clauses.
- **EU operational resilience:** DORA (financial) + NIS2 (essential + important entities).
- **Children's data:** COPPA + Age-Appropriate Design Code (UK + CA + CT).

### SOTA platforms in scope

#### Multi-framework GRC automation
- Vanta (broadest 2026 catalog, ~35% share); Drata (~25%, auditor-favorite); Secureframe (~15%, advisory-heavy); Sprinto (~10%, mid-market); Thoropass (~8%, bundles audit); Hyperproof; AuditBoard; Anecdotes; LogicGate; Strike Graph; Tugboat Logic; ServiceNow GRC; Archer (RSA); MetricStream; Workiva; Trustero.

#### Privacy (GDPR / CCPA / multi-jurisdiction)
- OneTrust (enterprise default); TrustArc; Securiti.ai (discovery+classification); Transcend (encrypted DSR); DataGrail (2000+ integrations); Ketch (API-driven consent); BigID (data discovery); MineOS; Iubenda; Termly; Osano; Cookiebot.

#### HIPAA
- HHS Security Risk Assessment Tool (free); Drata HIPAA; Vanta HIPAA; Compliancy Group; Accountable HQ; Aptible (HITRUST-adjacent); MedStack.

#### PCI DSS
- PCI SSC document library (public); Stripe / Braintree / Adyen / Spreedly tokenization; A-LIGN / Coalfire / Trustwave / Sysnet (Forter) / ControlScan QSAs; Secureframe PCI; Drata PCI.

#### AML / KYC / sanctions
- KYC: Sumsub (broadest crypto-native); Persona (customizable); Jumio (enterprise ID-doc); Onfido (Entrust subsidiary); Trulioo; Veriff; Alloy (orchestration).
- Sanctions / monitoring: ComplyAdvantage (AI real-time); Refinitiv World-Check; Dow Jones Watchlist; LexisNexis Bridger XG; Acuant.
- Crypto: Chainalysis (KYT + Address Screening + Sentinel); Elliptic; TRM Labs; Solidus Labs.

#### Vendor risk / TPRM
- BitSight (Forrester 2026 Wave Leader); SecurityScorecard; UpGuard (TPRM + ASM); Vanta Vendor Risk; OneTrust TPRM; Whistic; RiskRecon (Mastercard); Black Kite; ProcessUnity; Prevalent; Aravo.

#### Pentest / bug bounty
- HackerOne; Bugcrowd; Cobalt; Synack; Intigriti; YesWeHack.

#### Vulnerability management
- Tenable One (Nessus); Qualys VMDR; Rapid7 InsightVM; Snyk; GitHub Advanced Security (CodeQL + Dependabot + secret scanning); Wiz / Orca / Lacework (CNAPP); Microsoft Defender VM; Nucleus Security; Vulcan Cyber.
- OSS: OpenVAS; Nuclei; Trivy; Grype; Syft (SBOM).

#### Security awareness / phishing
- KnowBe4 (largest content library); Hoxhunt (adaptive); SoSafe (EU/NIS2); Living Security (HRM); Proofpoint; Arsen (deepfake/voice sim 2026); Curricula (Huntress); NINJIO; MetaCompliance; Infosec IQ.

#### DLP / data classification
- Microsoft Purview (M365-native); Nightfall AI (API-first SaaS); Cyberhaven (Data Lineage / DDR — 2026 unified platform); Varonis; Forcepoint; Symantec DLP; Digital Guardian.

#### SIEM / log
- Splunk (catalog: `splunk-mcp`); Datadog Cloud SIEM; Elastic Security; Microsoft Sentinel; IBM QRadar; Sumo Logic; LogRhythm; Panther.

#### AI governance
- Credo AI (policy packs); Holistic AI (continuous audit); Robust Intelligence; Fairly AI; Modulos.

#### Whistleblower
- NAVEX EthicsPoint; Lighthouse Services; Convercent (OneTrust); Whispli; FaceUp (EU); AllVoices; Speakfully.

#### Policy management
- PowerDMS; NAVEX PolicyTech; ComplianceBridge; in-platform (Vanta / Drata / Secureframe policy libraries).

#### Communications archiving (FinSvc)
- Smarsh; Global Relay; Theta Lake; Hanzo.

#### Pharma / medtech QMS
- MasterControl; Veeva Vault QualityDocs; Greenlight Guru; Qualio.

---

## Framework cross-walk table

The single biggest efficiency lever — most controls satisfy multiple frameworks. Use this to author one policy / control set that earns multiple certifications.

| Control area | SOC 2 TSC | ISO 27001:2022 Annex A | HIPAA Security | PCI DSS v4.0 | NIST CSF 2.0 |
|---|---|---|---|---|---|
| Information Security Policy | CC1.1 | A.5.1 | §164.316(a) | Req. 12.1 | GV.PO-01 |
| Access Control / IAM | CC6.1, CC6.2, CC6.3 | A.5.15, A.5.16, A.8.2, A.8.3 | §164.308(a)(3), §164.312(a) | Req. 7, 8 | PR.AA |
| Encryption at rest / in transit | CC6.7 | A.8.24 | §164.312(a)(2)(iv), §164.312(e)(1) | Req. 3, 4 | PR.DS-01, 02 |
| Logging + monitoring | CC7.2 | A.8.15, A.8.16 | §164.308(a)(1)(ii)(D) | Req. 10 | DE.CM |
| Change management | CC8.1 | A.8.32 | §164.308(a)(8) | Req. 6.5 | PR.PS-06 |
| Vulnerability management | CC7.1 | A.8.8 | §164.308(a)(8) | Req. 11.3 | DE.CM-09, ID.RA-06 |
| Pen testing | CC4.1 | A.8.29 | §164.308(a)(8) | Req. 11.4 | DE.CM-09 |
| Incident response | CC7.4, CC7.5 | A.5.24-A.5.28 | §164.308(a)(6) | Req. 12.10 | RS.MA, RS.AN, RS.CO |
| Risk assessment | CC3.1, CC3.2 | A.6.1.2, A.6.1.3 | §164.308(a)(1)(ii)(A) | Req. 12.3 | ID.RA, GV.RM |
| Vendor / TPRM | CC9.2 | A.5.19-A.5.23 | §164.308(b), §164.314(a) | Req. 12.8 | GV.SC, ID.SC |
| Awareness training | CC1.4 | A.6.3 | §164.308(a)(5) | Req. 12.6 | PR.AT |
| Asset management | CC6.1 | A.5.9, A.5.10, A.8.1 | §164.310(d) | Req. 9, 12.5 | ID.AM |
| Physical security | CC6.4 | A.7.1-A.7.14 | §164.310 | Req. 9 | PR.AA-05 |
| Business continuity | A1.2 | A.5.29, A.5.30 | §164.308(a)(7) | Req. 12.10 | RC.RP |
| Data backup | A1.2 | A.8.13 | §164.308(a)(7)(ii)(A) | Req. 9.5 | PR.DS-11 |
| Cryptography | CC6.7 | A.8.24 | §164.312(a)(2)(iv) | Req. 3.5, 3.6 | PR.DS |

**Rule:** when recommending a control, name it once + name ALL frameworks it satisfies. One policy → many certifications.

---

## SOC 2 readiness playbook

1. **Confirm scope.** Which TSC (Security mandatory; Availability / Confidentiality / Processing Integrity / Privacy optional)? Customer asks usually drive A+C; SaaS handling regulated data adds PI; SaaS handling PII adds P (or do GDPR/CCPA separately).
2. **Pick Type I vs II.** Type I = point-in-time (1-3mo prep). Type II = 3-12mo observation (what enterprise customers require).
3. **Pick automation platform.** 2026 leaders: Vanta (broadest, ~35% share — default for greenfield); Drata (auditor-favorite UX — best if your auditor has a Drata practice); Secureframe (advisory-heavy — best for orgs wanting hand-holding); Sprinto (mid-market international); Thoropass (bundles audit). Migration between platforms is hard — pick once.
4. **Pick auditor.** Big 4 (KPMG / EY / Deloitte / PwC — enterprise + premium pricing). Mid-tier: Schellman, A-LIGN, Coalfire, KirkpatrickPrice, Sensiba (Sensiba SaaS-friendly + accessible). Specialized: Prescient Assurance, Insight Assurance. Verify the auditor's Drata/Vanta partner status.
5. **Map controls.** Walk TSP 100 + the cross-walk table above; consolidate against existing controls (don't rebuild what you have).
6. **Build evidence collection.** Vanta/Drata/Secureframe integrate with AWS, GCP, Azure, Okta, JumpCloud, Google Workspace, Microsoft 365, GitHub, Asana, Slack, Datadog, etc. Manual evidence for what doesn't integrate.
7. **Write policy library.** SOC 2 minimum 14 policies (see Policy library reference below). Vanta/Drata ship sample libraries — customize, don't copy.
8. **Run pre-audit readiness.** Internal mock 30-60 days before. Fix high-impact gaps. Stable-state evidence for the full observation window.
9. **Execute Type II observation window.** Don't game it — auditors expand testing on suspicion.
10. **Audit.** Walk-through + sample testing + management response to findings.
11. **Bridge letter** between successive Type II periods to keep customer SOC 2 reports current.

### Cost benchmark (2026)

- Platform license: $7K-$30K/year (Vanta/Drata/Secureframe mid-market). Drata cheaper for small; Vanta scales better for mid+.
- Auditor: $15K-$80K (varies by scope, TSC count, complexity). Big 4 premium.
- Internal effort: 0.25-0.5 FTE for prep; 0.1-0.25 FTE for steady-state.
- Total all-in first Type II: $30K-$120K.

---

## ISO 27001 readiness playbook

1. **Confirm scope.** Geographical, organizational, technical scope of the ISMS. Statement of Applicability (SoA) flows from this.
2. **Build the ISMS structure.** Mandatory clauses 4-10: 4 Context, 5 Leadership + Policy (5.2), 6 Planning + Risk (6.1.2 risk assessment approach + 6.1.3 risk treatment), 7 Support + Documented Info (7.5), 8 Operation + Operational Plans (8.1), 9 Performance Evaluation (9.1 monitoring + 9.2 internal audit + 9.3 management review), 10 Improvement + Nonconformity (10.1).
3. **Risk assessment + treatment.** ISO/IEC 27005 methodology default. For each risk: identify, analyze, evaluate, treat (modify / share / retain / avoid). Map to Annex A controls.
4. **Statement of Applicability (SoA).** Lists each of 93 Annex A controls + status (in scope or not) + justification. Mandatory.
5. **Annex A — 4 themes, 93 controls (2022 update from 114 controls).**
   - A.5 Organizational (37 controls): policies, roles, segregation, threat intel, project security, info classification + handling, supplier security, info exchange, incident management, BC, identity mgmt, access rights.
   - A.6 People (8 controls): screening, terms + conditions, awareness + training, disciplinary, remote work, NDA.
   - A.7 Physical (14 controls): security perimeter, entry, secure areas, working in secure areas, desks + screens, equipment siting, supply utilities, cabling, maintenance, removal, off-premises, disposal, storage media, terminals.
   - A.8 Technological (34 controls): endpoint, privileged access, info access, code, source code access, secure dev, lifecycle, authentication, capacity, malware, vuln mgmt, config mgmt, deletion, masking, leak prevention, backup, redundancy, logging, monitoring, clock sync, privileged utility, install of apps, networks, network controls, network segregation, DNS + filtering, secure dev lifecycle, software dev lifecycle, secure dev environment, outsourced dev, testing, security test acceptance, prod-test data separation, cloud security.
6. **Internal audit** (Clause 9.2). Annual minimum. Risk-based sampling.
7. **Management review** (Clause 9.3). Annual minimum + on material change.
8. **External audit.** Stage 1 (documentation review — week-long typical) → Stage 2 (implementation audit — 2-3 weeks). Cert issued post-Stage 2.
9. **Surveillance** years 1-2 (annual reduced-scope audit).
10. **Recertification year 3** (full audit).

### Cert body benchmark

BSI (premium + global recognition); Schellman; A-LIGN; Coalfire ISO; LRQA; SGS; TÜV (EU strong); Bureau Veritas. Cost: $15K-$50K for SMB; varies by scope.

---

## GDPR readiness checklist

1. **Material scope (Art. 2).** Processing of personal data by automated means or as part of a filing system.
2. **Territorial scope (Art. 3).** Establishment in EU OR targeting EU subjects OR monitoring EU subjects' behavior. Without EU establishment, EU representative (Art. 27) required.
3. **Lawful basis (Art. 6).** For every processing activity, name one of: (a) consent, (b) contract necessity, (c) legal obligation, (d) vital interests, (e) public task, (f) legitimate interests. For special-category data (Art. 9): additional condition required. For criminal data (Art. 10): legal authorization required.
4. **Legitimate Interests Assessment (LIA)** when basis is Art. 6(1)(f). Three-part test: (1) legitimate interest, (2) necessity, (3) balancing against data subject rights/freedoms.
5. **Privacy by Design + Default (Art. 25).** Build it in; don't retrofit.
6. **ROPA (Art. 30).** Required for orgs with 250+ EE OR systematic processing OR special-category data. Controller side Art. 30(1): name + contact controller + DPO, purposes, categories of data subjects + data, recipients, transfers + safeguards, retention, technical/organizational measures. Processor side Art. 30(2): name + contact processor + DPO + controllers, categories of processing per controller, transfers, measures.
7. **DPIA (Art. 35).** Mandatory triggers: systematic monitoring of public areas, large-scale special-category, profiling with legal effect, ICO/CNIL/EDPB-listed high-risk operations.
8. **Data Subject Rights (Art. 12-23).** Access (15), rectify (16), erasure / RTBF (17), restriction (18), portability (20), object (21), no solely automated decision (22 — incl. profiling), withdraw consent.
9. **Response timeline.** 1 month from receipt (extendable to 3 months for complex requests with notice). Free for first request.
10. **Breach notification (Art. 33).** 72 hours to supervisory authority. Art. 34: to data subjects without undue delay if high risk to rights/freedoms. Phased notification allowed if facts incomplete.
11. **DPO designation (Art. 37).** Required if public authority, OR core activities = regular & systematic large-scale monitoring, OR large-scale processing of special-category / criminal data.
12. **International transfers (Chapter V).** Adequacy decision (UK, Switzerland, Japan, South Korea, Israel, Canada commercial, NZ, Argentina, Andorra, Faroe Islands, Guernsey, Jersey, IoM, Uruguay, EU-US DPF), SCC 2021/914 with Transfer Impact Assessment (TIA — post-Schrems II), BCR, Art. 49 derogations.
13. **Processor agreements (Art. 28).** Mandatory contractual terms — must include in EVERY processor contract.
14. **Cookie consent.** ePrivacy Directive — opt-in for non-essential cookies. Strict in DE, FR, IT, ES; UK ICO guidance post-Brexit.
15. **Children (Art. 8).** Age of digital consent — varies by Member State (13-16).

### SOTA tooling

- **Discovery + ROPA:** Securiti.ai, OneTrust Data Mapping, Transcend, DataGrail, BigID, MineOS, Iubenda Internal.
- **DPIA execution:** CNIL PIA Tool (free, open-source — Python install via `cli-anything`), OneTrust DPIA, Transcend DPIA.
- **DSR fulfillment:** Transcend (encrypted), Securiti.ai, DataGrail (2000+ integrations), OneTrust DSR, Ketch, MineOS.
- **Consent + cookie:** OneTrust, Cookiebot, TrustArc, Iubenda Cookie, Termly, Osano.

---

## CCPA readiness checklist

1. **Applicability.** For-profit doing business in CA + either (a) $25M+ gross revenue, (b) 100k+ consumer households/devices/identifiers, (c) 50%+ revenue from selling/sharing personal info.
2. **Privacy notice at collection** (§1798.100). Categories collected + purposes + retention + rights — before or at collection.
3. **Full privacy policy** (annual update).
4. **Rights infrastructure:**
   - Right to know (§1798.110 — specific pieces in last 12 months; CPRA extends on request).
   - Right to delete (§1798.105 — exceptions: complete transaction, security incident, free speech, internal lawful use).
   - Right to correct (§1798.106 — CPRA-new).
   - Right to opt out of sale/share (§1798.120 — Sale = monetary or other valuable consideration; Share = cross-context behavioral advertising — CPRA-new).
   - Right to limit use of sensitive PI (§1798.121 — CPRA-new — precise geolocation, racial/ethnic, religious, mail/email/text content, genetic, biometric, health, sex life/orientation, contents of mail/email/text, SSN, driver's license, financial account #).
   - Right to non-discrimination (§1798.125).
   - Right to data portability (§1798.130).
5. **"Do Not Sell or Share My Personal Information" link** — homepage + at collection.
6. **Sensitive PI limit link** — when applicable.
7. **GPC (Global Privacy Control) signal** — Cal AG enforcement focus; treat as opt-out request.
8. **Service provider agreements** — CPRA-specific contractual terms (§1798.140(ag)).
9. **45-day response window** (extendable to 90 with notice).
10. **Cal AG + CPPA enforcement focus 2026:** children's data, dark patterns, GPC compliance, sensitive PI handling, third-party data sales tracking.

### State expansion (2026 — 19+ states)

Map applicability by revenue + consumer + data-broker thresholds across: VA CDPA, CO CPA, CT CTDPA, UT UCPA, OR OCPA, TX TDPSA, FL FDBR, MT, IA, DE, NJ, NH, MD, IN, KY, MN, NE, RI, TN. Most include know + delete + opt-out of sale/targeted ads + opt-in for sensitive. Universal-opt-out mechanism (GPC) recognition increasing.

---

## HIPAA readiness checklist

1. **Determine role.** Covered Entity (health plan, healthcare clearinghouse, healthcare provider transmitting electronic transactions in HIPAA-standard format) vs Business Associate vs Sub-BA. Hybrid entity status when only some functions are HIPAA-covered.
2. **Privacy Rule (45 CFR §§164.500-534).** Uses + disclosures, minimum necessary, individual rights (access, amendment, accounting of disclosures, restriction), authorization, NPP.
3. **Security Rule (§§164.302-318).** Administrative + Physical + Technical safeguards.
   - **Administrative (§164.308):** Security Management Process — risk analysis (a)(1)(ii)(A), risk management (a)(1)(ii)(B), sanction policy (a)(1)(ii)(C), info system activity review (a)(1)(ii)(D). Assigned Security Responsibility (a)(2). Workforce Security (a)(3). Information Access Management (a)(4). Awareness + Training (a)(5). Incident Procedures (a)(6). Contingency Plan (a)(7). Evaluation (a)(8). BAA (b).
   - **Physical (§164.310):** Facility Access (a), Workstation Use (b), Workstation Security (c), Device + Media Controls (d).
   - **Technical (§164.312):** Access Control (a), Audit Controls (b), Integrity (c), Person/Entity Authentication (d), Transmission Security (e).
4. **Risk Analysis (§164.308(a)(1)(ii)(A)).** Foundational obligation. NIST SP 800-66 Rev. 2 (2024) methodology. HHS SRA Tool (free) covers small/medium orgs.
5. **BAA (§164.504(e)).** Mandatory with every BA. HHS Sample BAA Provisions as base. Cover: permitted uses, safeguards, breach reporting (sub-BA flow-down), termination, return/destruction.
6. **Breach Notification Rule (Subpart D §§164.400-414).**
   - Individuals: 60 days from discovery, written.
   - Media: if 500+ individuals in a state, prominent media outlet, 60 days.
   - HHS: all breaches 500+ within 60 days; <500 annually by Feb 60 days after end of year.
   - Substitute notice if contact info inadequate.
7. **HITECH overlay.** Strengthens BA direct liability; defines unsecured PHI; raises civil penalties (tiered $137-$50,000 per violation per category; $1.5M cap per year per category).
8. **State law overlay.** California CMIA, NY SHIELD Act, others. State laws can be stricter than HIPAA.

### SOTA tooling

- **Free:** HHS HealthIT SRA Tool (Python/Windows installer); NIST SP 800-66 r2; HHS Sample BAA.
- **Paid platforms:** Drata HIPAA, Vanta HIPAA, Compliancy Group, Accountable HQ (mid-market), MedStack (containerized PHI), Aptible (HITRUST-adjacent + HIPAA hosting).

---

## PCI DSS readiness checklist

1. **Determine scope.** Cardholder Data Environment (CDE) = systems that store, process, or transmit cardholder data (CHD) or sensitive authentication data (SAD). Connected systems = CDE-adjacent and in-scope. Out-of-scope = no connection + no PHI/SAD touch.
2. **Scope reduction.** Tokenization (Stripe / Braintree / Adyen / Spreedly) eliminates CHD storage. Iframe / hosted-fields offload web-form intake. P2PE-validated POS eliminates SAD exposure between read and acquirer. Network segmentation isolates CDE from corporate.
3. **Pick SAQ vs ROC.**
   - **Level 1** (6M+ Visa/MC card transactions/year OR breach history): ROC (Report on Compliance) by QSA.
   - **Levels 2-4:** SAQ (Self-Assessment Questionnaire). Type by acceptance channel.
4. **SAQ types:**
   - **SAQ A:** Card-not-present (CNP) merchants, fully outsourced — e.g., redirect to Stripe Checkout, payment iframe with hosted fields. ~22 questions. Easiest path.
   - **SAQ A-EP:** E-commerce, payment page hosted by 3P but merchant impacts integrity of payment page — e.g., merchant-served HTML + 3P script. ~138 questions.
   - **SAQ B:** Imprint or standalone dial-out terminal only.
   - **SAQ B-IP:** Standalone IP-connected POS terminal only.
   - **SAQ C:** POS systems connected to internet.
   - **SAQ C-VT:** Virtual terminal only.
   - **SAQ D:** Catch-all for merchants + service providers not covered above. ~329 questions.
5. **v4.0 12 Requirement categories:** (1) network security controls, (2) secure config, (3) protect stored CHD, (4) protect transmitted CHD, (5) malware, (6) secure dev + maint, (7) restrict access by need-to-know, (8) identify + authenticate, (9) physical access, (10) log + monitor, (11) test security (incl. pen test 11.4 + ASV scans 11.3), (12) info security policy + risk + awareness.
6. **Annual obligations:** ASV external scans (quarterly), internal vuln scans (quarterly), pen test (annual + on significant change), segmentation pen test (annual for service providers; biennial for merchants), risk assessment, awareness training, policy review.
7. **v4.0 future-dated requirements** (effective March 31, 2025; in steady-state by 2026): authenticated internal scans, customized approach option, broader MFA, encryption inventory, more rigorous risk-based authentication.
8. **QSA** for Level 1. ISA (Internal Security Assessor) is HQ option.

### SOTA QSAs (2026)

A-LIGN; Coalfire; Trustwave; Sysnet (Forter); NCC Group; Schellman; Wesley K. Clark; ControlScan. Cost: $25K-$150K depending on scope.

---

## AML KYC program playbook

1. **Determine applicability.** US: bank, credit union, broker-dealer, mutual fund, futures commission merchant, MSB (incl. crypto exchanges), insurance, casino, dealer in precious metals, lawyer/notary in some contexts. EU: 6AMLD obliged entities + AMLR/AMLD6 + AMLA central oversight + MiCA for crypto.
2. **Five BSA Pillars** (FinCEN Customer Due Diligence final rule 2018):
   - **CIP (Customer Identification Program)** — verify identity at onboarding.
   - **CDD (Customer Due Diligence)** — beneficial ownership (25%+ ownership prong + 1 control prong), ongoing monitoring.
   - **EDD (Enhanced Due Diligence)** — high-risk customers (PEPs, high-risk jurisdictions, high-volume cash, correspondent banking).
   - **Transaction monitoring** — risk-based rules + ML-driven anomaly detection.
   - **SAR / CTR filing** — SAR within 30 days of detection (60 days if no subject identified); CTR for cash $10K+ same day or next business day.
3. **OFAC sanctions screening.** Real-time at onboarding + ongoing rescreening (daily for high-risk; weekly for medium; monthly for low). SDN List + Consolidated Sanctions List + Sectoral Sanctions Identifications + Foreign Sanctions Evaders. Subset: SSI, NSPM, BIS Entity List, DPL.
4. **Independent audit.** Annual minimum (federal MSB rule). Scope: program effectiveness, sample testing, gap analysis.
5. **Training.** Annual minimum for BSA Officer + relevant employees.
6. **BSA Officer designation.** Named, qualified, sufficient authority + resources.
7. **FATF Travel Rule (Recommendation 16).** Crypto: transmit originator/beneficiary info above threshold ($1k US for VASPs; varies by jurisdiction). 2026 enforcement broad.
8. **MiCA** (EU crypto — Markets in Crypto-Assets Regulation, in force June 30, 2024 + Dec 30, 2024 phases; 2026 enforcement intensifying). CASP authorization, governance, white papers for crypto-asset issuance, market abuse, prudential.

### SOTA vendor stack (2026)

- **KYC (identity verification):** Sumsub (broadest single-vendor for crypto-native; 14k+ doc types; MiCA + FinCEN aligned); Persona (customizable workflows; growth-stage stablecoin platforms); Jumio (enterprise-grade, AI ID-doc + facial liveness, 5k doc types / 200 countries); Onfido (Entrust subsidiary); Trulioo (global ID + KYB); Veriff; Alloy (orchestration layer — chain multiple vendors).
- **Sanctions / PEP / adverse media:** ComplyAdvantage (AI real-time, proprietary DB, low false-positive rate; CDD + case mgmt + reporting via Mesh platform); Refinitiv World-Check (largest DB); Dow Jones Watchlist; LexisNexis Bridger XG; Acuant; Sanction Scanner.
- **Crypto-specific:** Chainalysis (KYT for transaction monitoring; Address Screening; VASP Risk Scoring; Sentinel 35+ risk categories); Elliptic; TRM Labs; Solidus Labs (market surveillance).
- **Transaction monitoring (TradFi):** Actimize (NICE); SAS AML; Oracle FCCM; Fiserv AML Risk Manager; ComplyAdvantage Mesh.

### SAR template structure

(1) Subject identification (account number, identity, address). (2) Suspicious activity description (5W: who, what, when, where, why). (3) Activity total + duration. (4) Detection mechanism (transaction monitoring alert, employee tip, regulator inquiry). (5) Other parties involved. (6) Status of activity (continuing, ceased, etc.). (7) Filer + contact.

---

## Vendor risk playbook

1. **Inventory.** Where are vendors hiding? CFO P&L review; AP / vendor master; SaaS access reviews; SSO log; corporate card statements; M365/Google Workspace third-party app inventory. Most orgs underestimate vendor count by 2-5x.
2. **Tier.** Tier 1 (Critical): handles personal data / financial data / business-critical functions / IP. Tier 2 (High): handles internal-only sensitive data / supports critical business processes. Tier 3 (Moderate): handles non-sensitive but accesses systems. Tier 4 (Low): registration only — no data, no system access.
3. **Per tier — pre-onboarding due diligence:**
   - **Tier 1:** SIG Plus (~1100Q) OR CAIQ + SOC 2 Type II (current) + ISO 27001 + DPA + BAA (if PHI) + financial review + EUSCC if EU transfers + pen test report + insurance certs. Annual reassessment.
   - **Tier 2:** SIG Core (~700Q) + SOC 2 Type II + DPA. Biennial reassessment.
   - **Tier 3:** SIG Lite (~125Q) OR shorter custom + DPA if any data. Triennial.
   - **Tier 4:** Registration + standard contract.
4. **Continuous monitoring** (Tier 1 + 2): BitSight / SecurityScorecard / UpGuard rating drift alerts; news + breach monitoring via threat intel feeds; SOC 2 bridge letter tracking.
5. **Periodic reassessment.** Calendar driven (annual/biennial/triennial per tier) + event-driven (breach, ownership change, material service change).
6. **Termination / offboarding.** Data return or destruction certificate; access revocation; sub-processor termination; remaining contractual obligations review.

### SOTA platform (2026)

- **BitSight** — Forrester Wave Leader Q2 2026, highest possible score, outside-in cyber risk intelligence; enterprise default for outside-in ratings.
- **SecurityScorecard** — outside-in ratings + research-driven cyber intel.
- **UpGuard** — combines TPRM + Attack Surface Management + data-leak detection — best when you want TPRM + own-surface in one tool.
- **Vanta Vendor Risk** — integrated with compliance automation; best when already using Vanta for SOC 2/ISO.
- **OneTrust TPRM** — enterprise, integrates with privacy program.
- **Whistic** — Trust Vault model (vendor shares info once with all customers).
- **RiskRecon** (Mastercard) — outside-in ratings.
- **Black Kite** — quant-leaning ratings + FAIR-equivalent monetization.
- **ProcessUnity / Prevalent / Aravo** — enterprise GRC-integrated TPRM.

---

## TPRM lifecycle playbook

| Stage | Activities | Skill / tool |
|---|---|---|
| 1. Sourcing + selection | Pre-RFP security questions (5-10 yes/no); request SOC 2 report; check rating service | `vendor-risk-bitsight-securityscorecard-upguard` + `gmail-mcp` |
| 2. Due diligence + tiering | Full questionnaire (CAIQ / SIG by tier); reference SOC 2 / ISO / pen test; tier classification | `vendor-security-questionnaire-caiq-sig` + `tprm-third-party-risk-lifecycle` |
| 3. Contracting | DPA (GDPR Art. 28); BAA (HIPAA); SCC + TIA (EU transfers); security addendum; audit rights; insurance reqs | Hand off to `legal-counsel` for binding terms; agent provides compliance content |
| 4. Onboarding | Least-privilege access; baseline scan; integrate to SSO; classify data access; log subprocessor in privacy policy | `tprm-third-party-risk-lifecycle` |
| 5. Continuous monitoring | Rating service drift alerts; breach monitoring; SOC 2 bridge letter tracking; news feeds | `vendor-risk-bitsight-securityscorecard-upguard` |
| 6. Periodic reassessment | Per-tier cadence; refresh SIG/CAIQ; review SOC 2 / ISO recert | `vendor-security-questionnaire-caiq-sig` + `tprm-third-party-risk-lifecycle` |
| 7. Termination + offboarding | Data return/destruction cert; access revoke; sub-processor cleanup; doc retention | `tprm-third-party-risk-lifecycle` + `data-retention-deletion-policy` |

---

## Pentest coordination playbook

1. **Define scope.** Application (web / mobile / API), infrastructure (network / cloud / k8s), social engineering (phishing / vishing), physical, red team (objective-based). Black box / grey box / white box.
2. **Pick model.** Bug bounty (continuous; HackerOne, Bugcrowd, Intigriti, YesWeHack); PtaaS time-boxed (Cobalt, Synack); traditional consulting (NCC Group, Bishop Fox, Trail of Bits — enterprise + premium).
3. **Define SLAs.** Triage time (HackerOne / Bugcrowd offer managed triage). Resolution time by severity (Critical 14 days; High 30; Medium 90; Low best-effort — match PCI DSS Req. 6.3.1).
4. **Severity scale.** CVSS 4.0 (released Nov 2023 — replaces v3.1 as 2026 industry default). Custom modifiers for business impact.
5. **Reward schedule** (bug bounty). Tiered by severity + asset (Tier 1 critical app vs Tier 3 non-critical). $50-$50K typical range; $250K+ for critical RCE on critical asset.
6. **Disclosure policy.** Coordinated disclosure (90 days); see Project Zero model.
7. **Required by:** SOC 2 (annual external pen test for CC4.1); ISO 27001 (Annex A.8.29); PCI DSS (Req. 11.4); HIPAA evaluation (recommended); SOX (ITGC support); NYDFS (penetration test annually + vulnerability assessment biannually).

### 2026 platform pick guide

- **HackerOne** — largest community + best for high-volume programs.
- **Bugcrowd** — managed triage included; good for orgs without internal triage capacity.
- **Intigriti** — EU-strong (GDPR-friendly data handling).
- **YesWeHack** — EU/APAC-strong; .gov.fr partnerships.
- **Cobalt** — time-boxed PtaaS (4-week typical); good for SOC 2 annual pen test.
- **Synack** — vetted + cleared researchers; good for regulated (DoD, financial).

---

## Vulnerability management playbook

1. **Two-track approach.** App-sec (code, dependencies, containers, IaC) + Infra VM (servers, endpoints, networks).
2. **App-sec stack.** Snyk (SCA + SAST + IaC + container — most popular 2026); GitHub Advanced Security (CodeQL SAST + Dependabot SCA + secret scanning — included with GHE); Semgrep (open source + paid SAST); Checkmarx; SonarQube; Veracode.
3. **Infra VM stack.** Tenable One (most comprehensive 2026 — Nessus + cloud + OT + AD + identity; unified TruRisk-equivalent); Qualys VMDR (TruRisk + native patching included in base subscription); Rapid7 InsightVM (Real Risk Score). Cloud-native: Wiz, Orca, Lacework (CNAPP = CSPM + CWPP + CIEM).
4. **Open source fallback.** OpenVAS (Greenbone); Nuclei (template-based — fast + actively maintained); Trivy (containers + IaC + secrets); Grype (SBOM scanning); Syft (SBOM generation).
5. **Prioritization.** CVSS 4.0 base score + EPSS (Exploit Prediction Scoring System) + KEV (CISA Known Exploited Vulnerabilities Catalog) + asset criticality + business context. Move beyond CVSS-only to "exploitable + asset-critical + exposed" first.
6. **Remediation SLAs.** Match to PCI DSS Req. 6.3.1: Critical (CVSS 9.0-10.0) 14 days; High (7.0-8.9) 30 days; Medium (4.0-6.9) 90 days; Low best-effort. Increasingly strict for KEV-listed vulns.
7. **Patch management.** Tied to change management; emergency patch process for KEV / actively exploited.
8. **Reporting.** Monthly KPI: open / new / aged-out / SLA-breached / patched-in-period. By asset class + by severity.

---

## Security awareness playbook

1. **Annual mandatory baseline.** Required by SOC 2 (CC1.4), ISO 27001 (A.6.3), HIPAA (§164.308(a)(5)), PCI DSS (Req. 12.6), GLBA Safeguards Rule, NYDFS, GDPR Art. 32, EU AI Act (deployer transparency for high-risk).
2. **Topics:** social engineering / phishing, password hygiene + MFA, data handling + classification, device security (BYOD overlap), incident reporting, AI use (NEW 2024+ — explicit ChatGPT/Claude/Copilot use rules), privacy basics, role-specific (developer secure coding, sales-engineer customer data handling, finance fraud).
3. **Delivery cadence.** Annual mandatory + monthly phishing + quarterly micro-learning. Effective programs do continuous (not one-time annual).
4. **2026 vector expansion.** Multi-vector phishing: email + SMS (smishing) + voice (vishing) + QR (quishing — surging 2026) + deepfake AI video / audio (CEO fraud). Arsen + Adaptive Security pioneered AI deepfake sim.
5. **Measurement.** Click rate (decreases with maturity); report rate (INCREASES with maturity — more important — drives detection culture); credential-entry rate; dwell time; repeat-clicker tracking. Compare against industry benchmarks (KnowBe4 publishes annual report).
6. **Role-based training matrices.** Map: role × required training × cadence × delivery platform × evidence retention.

### 2026 platform pick guide

- **KnowBe4** — largest content library; best for high-volume rollout + compliance documentation; phone sim template-based (not adaptive AI).
- **Hoxhunt** — behavioral / adaptive (per-user difficulty); strong engagement metrics.
- **SoSafe** — EU-strong + gamification; best for NIS2 + GDPR-focused European orgs.
- **Living Security** — board-level Human Risk Management dashboards; less content depth.
- **Proofpoint** — DLP + training combo; legacy enterprise.
- **Arsen** — AI deepfake / voice sim 2026 standout.
- **Curricula (Huntress)** — story-driven; SMB.
- **NINJIO** — animated story-driven.
- **MetaCompliance** — EU + compliance-heavy.
- **Infosec IQ** — comprehensive + integrated phishing.

---

## Phishing simulation playbook

1. **Frequency.** Monthly minimum at org level. Weekly for critical roles (finance, exec assistants, executive team, customer-service handling sensitive data). Tied to events (after major announcements; quarterly fiscal cycle for finance scams).
2. **Vector mix.** Email (most common 80%+); SMS (10%); voice (5%); QR (5% — surging); deepfake (NEW 2026 — for orgs at risk of CEO fraud, vendor-impersonation invoice scams).
3. **Difficulty curve.** Easy templates (~30% click rate target) for new hires + first quarter; medium (~10-15%); hard (~5-8%) for mature orgs. Hoxhunt auto-adapts per-user.
4. **Themes.** Job applicant; package delivery (Q4 holiday); HR (W-2, benefits open enrollment); IT (password expiry, MFA reset); finance (invoice, ACH change request); vendor (CEO email forward); calendar / meeting invite spoof; AI assistant prompt-injection (NEW 2026).
5. **Reporting.** Click rate, report rate, credential-entry rate, dwell time, repeat-clicker rate. By department + role + tenure. Trend over time.
6. **Failed-click follow-up.** Just-in-time learning (1-min video) NOT shame-and-blame. Repeat-clickers get focused intervention (training + 1:1 with manager).
7. **Tied to broader program.** Phishing sim is part of awareness program, not in isolation. Pair with quarterly awareness training + monthly threat-of-the-month brief.

---

## Incident response playbook

**NIST SP 800-61 Rev. 3 (April 2025) — current standard.** Aligns IR with NIST CSF 2.0 six functions; shifts from rigid 4-phase to flexible continuous model.

### Phase mapping (CSF 2.0 aligned)

- **Govern (GV)** — IR program ownership, roles, policy, executive accountability, retainer agreements.
- **Identify (ID)** — asset inventory, threat landscape, supply chain, vulnerability state, risk posture.
- **Protect (PR)** — preventive controls, awareness, secure config, data security.
- **Detect (DE)** — SIEM / EDR alerts, anomaly detection, threat intel matching, user reports.
- **Respond (RS)** — triage, classification, containment, eradication, communication.
- **Recover (RC)** — restoration, validation, post-incident review, lessons learned.

### Required artifacts

1. **IR Plan** — high-level program + roles + escalation matrix + communication tree + tabletop schedule + retainer details. Approved by exec leadership. Reviewed annually.
2. **Playbooks per scenario** — ransomware, BEC (Business Email Compromise), data breach, account takeover, insider threat, third-party-induced (vendor breach), DDoS, lost device, AI-system compromise (NEW 2025+).
3. **CSIRT roster + on-call rotation** — primary + backup per role. SecOps lead, IT lead, legal, PR/comms, exec liaison, external counsel, breach coach, IR retainer firm.
4. **Tabletop exercise schedule** — quarterly minimum. Scenarios rotate. Document gaps + remediation actions.
5. **Post-Incident Review (PIR) template** — facts timeline, root cause, contributing factors, what worked, what didn't, action items + owners + due dates.

### Required retainers (mature orgs)

- IR firm (CrowdStrike, Mandiant, Stroz Friedberg, Kroll, Charles River Associates, Booz Allen, Coveware ransom negotiation).
- Breach coach (privacy/cyber attorney — Mullen Coughlin, Davis Wright Tremaine, BakerHostetler are 2026 frequent flyers).
- PR / comms agency.

### Detection sources

- SIEM: Splunk, Datadog Cloud SIEM, Microsoft Sentinel, Elastic Security, Panther, Sumo Logic, IBM QRadar, LogRhythm.
- EDR / XDR: CrowdStrike Falcon, SentinelOne, Microsoft Defender for Endpoint, Palo Alto Cortex XDR, Sophos XDR, Trend Vision One.
- Cloud: Wiz, Orca, Lacework; native (AWS GuardDuty, Azure Defender, GCP SCC).
- Email: Proofpoint, Abnormal Security, Mimecast.
- IDS / IPS: Suricata, Snort, Zeek.

---

## Breach notification matrix

| Regulator / law | Window | Trigger | Recipient | Format |
|---|---|---|---|---|
| GDPR Art. 33 | 72h from awareness | Personal data breach risking rights | Supervisory authority | DPA form per Member State |
| GDPR Art. 34 | "without undue delay" | High risk to rights/freedoms | Data subjects | Direct communication |
| UK GDPR | 72h | Same as GDPR | ICO | ICO form |
| CCPA §1798.82 (CA) | "without unreasonable delay" | Unencrypted/unredacted PI breach | Affected residents + Cal AG if 500+ | Required form |
| US state laws (varying) | 30-90 days typical (states vary) | PII breach (definitions vary) | Affected residents + state AG + sometimes credit bureaus | Per state law |
| HIPAA §164.404 | 60 days from discovery | Unsecured PHI breach | Affected individuals | Written |
| HIPAA §164.406 | 60 days | Breach of 500+ residents of state | Prominent media in state | Press release |
| HIPAA §164.408 | 60 days (500+); annual (<500) | All breaches | HHS OCR | Online portal |
| SEC 8-K Item 1.05 | 4 business days from material determination | Material cybersecurity incident | SEC + investors | 8-K filing |
| NYDFS 23 NYCRR 500.17 | 72h from determination | Cybersecurity event | NYDFS | Online portal |
| EU NIS2 | 24h early warning + 72h incident + 1mo final | Significant incident | National CSIRT / CA | National portal |
| EU DORA | 4h (major ICT incident) + 1 business day (initial) + 1 month (final) | Major ICT-related incident | National CA → ESAs | DORA framework |
| GLBA Safeguards (2024 update) | 30 days | 500+ consumer security event | FTC | Online portal |
| PCI DSS (card brands) | Immediate (per acquirer agreement) | CHD breach | Acquirer / card brand | Forensic notification |
| FERPA | "Without undue delay" + 60-day notice | Education-record breach | Affected + DoE | Direct + DoE form |

### Decision tree

1. **Is it a "breach"?** GDPR: personal data breach = "breach of security leading to accidental/unlawful destruction, loss, alteration, unauthorised disclosure of, or access to" personal data. Lower threshold than US state laws.
2. **Whose data?** Determines which laws + windows apply (often multiple simultaneously).
3. **What data?** PII (US), personal data (GDPR), PHI (HIPAA), CHD (PCI), customer data (NYDFS), education records (FERPA).
4. **How many affected?** 500-individual threshold triggers media + AG / HHS escalation.
5. **Is incident over?** GDPR allows phased notification (Art. 33(4)) — file at 72h with what you have; supplement when you have more.

---

## DLP classification playbook

1. **Sensitivity labels (4-tier baseline):**
   - **Public** — intended for public release (marketing, press releases, public docs).
   - **Internal** — for employees + contractors under NDA; no external sharing without approval.
   - **Confidential** — restricted to need-to-know within org; encryption required at rest + in transit; access logging.
   - **Restricted** — highest sensitivity; explicit access list + dual-control where applicable; geographic/jurisdiction restrictions; reportable on misuse.
2. **Classify by source category:**
   - PII (name, email, phone, address, IP) → Internal or Confidential.
   - PHI → Confidential or Restricted.
   - CHD (cardholder data) → Restricted (per PCI DSS).
   - Source code → Internal or Confidential.
   - Customer data → Confidential.
   - Trade secrets / IP → Restricted.
   - Financial records (pre-public) → Restricted.
3. **DLP rule sets:**
   - **Block** Restricted → external email/share/cloud upload.
   - **Encrypt** Confidential → external email/share with policy-based key.
   - **Warn + log** Internal → external.
   - **Allow + monitor** Public → external.
4. **2026 GenAI overlay.** Block paste of Confidential/Restricted into chat-based GenAI (ChatGPT, Claude, Gemini, Copilot, Perplexity). Allow into enterprise-tier GenAI with DPA + no-training agreement.
5. **Architecture.**
   - **Endpoint DLP** — agent on laptops + desktops (Purview Endpoint, Cyberhaven, Symantec, Forcepoint, Digital Guardian).
   - **Network DLP** — inline at perimeter / proxy (Forcepoint, Symantec, Zscaler).
   - **Cloud / SaaS DLP** — API integration to M365, Google Workspace, Slack, Salesforce, GitHub, Box, Dropbox (Nightfall, Cyberhaven, Purview, Lookout).
   - **Email DLP** — gateway (Proofpoint, Mimecast, Microsoft, Google).
6. **Tools (2026):**
   - **Microsoft Purview** — M365-native, consolidated DLP + DSPM + insider risk + AI. Strong if Microsoft-shop; gaps on macOS endpoints, non-Edge browsers, third-party SaaS.
   - **Nightfall AI** — API-first SaaS DLP; Slack, Salesforce, GitHub, GenAI. ~$10/user/month start; ~$23K/year median.
   - **Cyberhaven** — Data Lineage / DDR (Data Detection and Response) — 2026 unified platform. Tracks data origin, not just content — defeats evasion.
   - **Varonis** — file system + cloud data classification + behavior analytics.
   - **Forcepoint / Symantec / Digital Guardian** — legacy enterprise DLP.

---

## Policy library reference

### SOC 2 minimum (14)

1. Information Security Policy (overarching)
2. Access Control Policy
3. Change Management Policy
4. Incident Response Policy
5. Business Continuity / Disaster Recovery Policy
6. Vendor Management Policy
7. Acceptable Use Policy (AUP)
8. Data Classification Policy
9. Cryptography / Encryption Policy
10. Asset Management Policy
11. Risk Management Policy
12. Vulnerability Management Policy
13. Logging + Monitoring Policy
14. Privacy / Data Protection Policy

### ISO 27001:2022 minimum (12)

- Information Security Policy (5.2 explicit)
- Access Control Policy (A.5.15)
- Cryptography Policy (A.8.24)
- Backup Policy (A.8.13)
- Incident Management Policy (A.5.24-A.5.28)
- Information Classification + Handling Policy (A.5.12, A.5.13)
- Supplier Security Policy (A.5.19)
- Acceptable Use Policy (A.5.10)
- Logging Policy (A.8.15)
- Network Security Policy (A.8.20-A.8.23)
- Secure Development Policy (A.8.25-A.8.34)
- Mobile Device + Teleworking Policy (A.6.7, A.7.9)

### HIPAA minimum (8)

- Information Security Policy
- Workforce Security Policy
- Information Access Management Policy
- Awareness + Training Policy
- Incident Procedures Policy
- Contingency Plan (BC/DR)
- Risk Management Policy
- Sanction Policy

### PCI DSS minimum (7)

- Information Security Policy (Req. 12.1)
- Acceptable Use Policy (Req. 12.3)
- Risk Assessment Policy (Req. 12.3.1)
- Incident Response Policy (Req. 12.10)
- Vendor Management Policy (Req. 12.8)
- Awareness Training Policy (Req. 12.6)
- Sensitive Data Handling Policy (Req. 3, 4)

### Cross-framework single set (recommended approach)

Write ONCE, certify MANY: Information Security Policy serves SOC 2 CC1.1 + ISO 27001 A.5.1 + HIPAA §164.316(a) + PCI Req. 12.1. Apply same to every policy.

### NEW 2024+ required (any org with GenAI access)

- AI Acceptable Use Policy (employee LLM use rules — what data can/cannot go into ChatGPT/Claude/Gemini; approved enterprise vs personal accounts; auditability)
- AI Governance Policy (EU AI Act readiness, NIST AI RMF mapping, ISO 42001 alignment, model approval process, post-market monitoring)

### Free templates baseline

- **SANS Information Security Policy Project** — comprehensive free library (Policy + Procedure + Standard templates).
- **CIS Security Policy Templates** — aligned to CIS Controls v8.
- **Vanta + Drata + Secureframe sample libraries** — current 2026, framework-mapped.

### Policy management platforms

PowerDMS (versioning + attestation tracking); NAVEX PolicyTech; ComplianceBridge; in-platform (Vanta / Drata / Secureframe policy library).

---

## AI governance playbook

### EU AI Act risk classification

| Class | Examples | Obligations |
|---|---|---|
| **Prohibited** (Title II) | Social scoring, real-time biometric ID in public spaces (with exceptions), manipulative subliminal techniques, emotion recognition in workplace/edu, untargeted facial scraping for DBs | Banned outright. Effective Feb 2, 2025. |
| **High-risk** (Title III, Annex III) | Biometric ID + categorization; critical infrastructure; education + vocational training; employment / worker management; access to essential public + private services (credit, social benefits); law enforcement; migration / asylum / border; admin of justice + democratic processes | Risk management, data governance, technical documentation, record-keeping, transparency, human oversight, accuracy + robustness + cybersecurity, post-market monitoring + serious-incident reporting, conformity assessment, CE mark, EU declaration of conformity. Effective Aug 2, 2026. |
| **Limited-risk** (Title IV) | Chatbots (must disclose to user), emotion recognition (notify user), deepfakes (label clearly), AI-generated content | Transparency obligations. Effective Aug 2, 2026. |
| **Minimal-risk** | Most other AI | Voluntary codes of conduct. |
| **GPAI** (General-Purpose AI / foundation models) | Foundation models (GPT-4/5, Claude, Gemini, Llama, Mistral etc.) | Transparency + copyright compliance + technical documentation. Systemic-risk GPAI (>10^25 FLOPS training compute): additional risk assessment + adversarial testing + serious-incident reporting + cybersecurity. Effective Aug 2, 2025 (1-year head start). |

Penalties up to €35M / 7% global revenue (for prohibited); €15M / 3% (for other obligations); €7.5M / 1.5% (for incorrect info to authorities).

### NIST AI RMF 1.0 cross-walk

Four core functions: **Govern**, **Map** (context + risks), **Measure** (assess risks, monitor performance), **Manage** (prioritize + treat risks). 7 trustworthy AI characteristics: Valid + Reliable, Safe, Secure + Resilient, Accountable + Transparent, Explainable + Interpretable, Privacy-Enhanced, Fair (with Harmful Bias Managed).

### ISO/IEC 42001 (AIMS)

Certifiable AI Management System (2023). Maps directly to EU AI Act high-risk obligations. Provides recognized framework for operationalizing governance, documentation, risk management, oversight. ISO 42001 cert ≠ EU AI Act compliance but heavily overlaps. First AIMS certs late-2024 onwards.

### SOTA tooling

- **Credo AI** — policy packs for EU AI Act + NIST AI RMF + ISO 42001 + SOC 2. Centralized AI inventory + automated compliance workflows + audit-ready documentation.
- **Holistic AI** — continuous audit trails + evidence collection + connections to AI systems across cloud, code, data, enterprise.
- **Robust Intelligence** — adversarial testing + safety eval.
- **Fairly AI** — bias + fairness assessment.
- **Modulos** — broad AI governance.

### Required artifacts

(1) AI inventory (every AI system in use, including 3P SaaS embedding AI). (2) Per-system risk classification. (3) Model cards (data sources, training methodology, known limitations, intended use, prohibited use). (4) Data governance protocols (training data sourcing, IP, license, consent for personal data). (5) Bias + fairness testing reports. (6) Adversarial robustness testing (for high-risk + systemic-risk GPAI). (7) Human-oversight protocols. (8) Post-market monitoring + serious-incident reporting workflows. (9) Conformity assessment + EU declaration of conformity (high-risk only).

---

## Whistleblower program playbook

### EU Whistleblower Directive 2019/1937

- **Applicability:** Internal reporting channels mandatory for orgs 50+ EE (phased; full force).
- **Channels:** Internal + external + public disclosure (with conditions). Multi-format (web, phone, app), multi-language, anonymous option.
- **Workflow:** Acknowledge within 7 days; response within 3 months; case management with chain of custody; non-retaliation protection.
- **Protected disclosures:** EU law violations across financial services, AML, product safety, environment, public health, consumer protection, privacy + data protection, NIS, EU financial interests, EU internal market.

### US frameworks

- **SOX §806** — public company whistleblower protection (financial reporting + securities fraud).
- **Dodd-Frank §922** — SEC whistleblower (with bounty 10-30% of recovery above $1M).
- **OSHA Whistleblower** — 20+ statutes incl. environmental, transportation, food safety.
- **State** — most states have public + private sector whistleblower laws.

### SOTA platforms (2026)

- **NAVEX EthicsPoint** — enterprise default. Covers EU Directive + SOX + Dodd-Frank + state. Multi-language, multi-channel, integrated case mgmt.
- **Lighthouse Services** — mid-market.
- **Convercent (OneTrust)** — integrated with OneTrust GRC.
- **Whispli** — EU-strong; secure end-to-end encryption.
- **FaceUp** — EU-strong + good UX; non-profit + SMB.
- **AllVoices** — modern UX + LGBTQ+ + accessibility focus.
- **Speakfully** — workplace-relations focused.

### Program elements

1. **Policy:** Internal Reporting + Whistleblower Protection + Non-Retaliation. Clear scope of reportable concerns.
2. **Channels:** Web (24/7), phone (24/7 staffed), in-app reporting, email, postal mail, in-person (HR + ethics officer + GC).
3. **Anonymity option** — allowed; but verified-identity reports often get faster response.
4. **Intake + triage workflow** — initial assessment 7 days; investigation plan; report classification (HR / financial / safety / legal / other).
5. **Investigation playbook** — investigator independence; interview protocols; evidence preservation; report writing; remediation.
6. **Communication back to reporter** — acknowledge receipt within 7 days; substantive response within 3 months (EU directive); ongoing updates as appropriate (anonymous reporter via pseudonym).
7. **Anti-retaliation** — explicit policy; HR + manager training; periodic check-ins with reporter post-resolution; audit-trail of any adverse action against known reporters.
8. **Reporting / metrics** — board-level annual report on volumes + categories + resolution times + retaliation incidents.

---

## Risk register reference

### Fields

| Field | Description |
|---|---|
| Risk ID | Unique identifier (R-001, R-002, etc.) |
| Risk title | Short descriptive title |
| Risk description | Threat × vulnerability × asset × impact |
| Category | Strategic / Operational / Financial / Compliance / Reputational / Cyber |
| Asset(s) affected | Systems, data, people, processes |
| Threat actor | Insider / external / nation-state / opportunistic / supply-chain |
| Inherent likelihood | 1-5 (1=Rare → 5=Almost Certain) |
| Inherent impact | 1-5 (1=Insignificant → 5=Catastrophic) |
| Inherent risk score | Likelihood × Impact (1-25) OR risk matrix lookup |
| Current controls | Existing mitigations |
| Control effectiveness | 1-5 |
| Residual likelihood | Post-control |
| Residual impact | Post-control |
| Residual risk score | Post-control product |
| Treatment | Accept / Mitigate / Transfer / Avoid |
| Treatment plan | Specific actions if mitigating |
| Owner | Accountable person |
| Review date | Next assessment |
| Status | Open / In Treatment / Accepted / Closed |

### Methodologies

- **NIST SP 800-30 Rev. 1** — federal / general-purpose risk methodology.
- **ISO/IEC 27005:2022** — ISMS-specific risk methodology.
- **FAIR (Factor Analysis of Information Risk)** — quantitative, monetized risk. OpenFAIR is open methodology.
- **COSO ERM** — enterprise risk (financial + strategic; less cyber-specific).
- **Octave Allegro** (CMU SEI) — asset-driven qualitative.

### Scoring conventions

- **5×5 ordinal matrix** — most teams. Likelihood × Impact = score 1-25. Heat-map color: 1-4 green (low), 5-9 yellow (medium), 10-14 orange (high), 15-25 red (critical).
- **Monetized (FAIR)** — Loss Event Frequency (LEF) × Loss Magnitude (LM). Probabilistic distributions; Monte Carlo simulation. Used by mature orgs for executive + board decision-making.

### Refresh cadence

- Continuous (rolling — best practice).
- Quarterly review minimum at material level.
- Annual full refresh for all risks.
- Event-triggered (new framework, breach, material change in business / technology).

---

## Regulatory horizon table (2026)

| Item | Jurisdiction | Effective | Status |
|---|---|---|---|
| EU AI Act — bans | EU | Feb 2, 2025 | Active |
| EU AI Act — GPAI obligations | EU | Aug 2, 2025 | Active |
| EU AI Act — high-risk obligations | EU | **Aug 2, 2026** | Imminent — plan now |
| EU AI Act — full enforcement | EU | Aug 2, 2027 | Future |
| EU DORA | EU FinSvc | Jan 17, 2025 | Active — 2026 enforcement intensifying |
| EU NIS2 | EU | Oct 17, 2024 transposition | 2026 active enforcement |
| EU Data Act | EU | Sept 12, 2025 | Active |
| EU Cyber Resilience Act | EU | Dec 2027 manufacturer | Future |
| EU Whistleblower Directive | EU | Phased; full force | Active |
| EU GDPR enforcement updates | EU | Ongoing | Ongoing |
| EU AML Regulation (AMLR) | EU | 2025 transition | 2026 enforcement |
| EU MiCA (crypto) | EU | June 30, 2024 + Dec 30, 2024 phases | 2026 enforcement intensifying |
| UK GDPR + DPDIB | UK | DPDIB pending Royal Assent | UK GDPR active |
| CCPA / CPRA enforcement | CA | Ongoing | Cal AG + CPPA active |
| US state privacy expansion | Various US | Rolling (19+ states by 2026) | Active |
| SEC Cyber 8-K Item 1.05 | US public cos | Dec 2023 | Active |
| NYDFS 23 NYCRR 500 amendments (Nov 2023) | NY FinSvc | Nov 1, 2023 - 2024-2025 phases | Active |
| CMMC 2.0 Phase 1 | DoD contractors | 2025-Q4 | Phasing in |
| FedRAMP Modernization | US federal | Ongoing rollout | Ongoing |
| GLBA Safeguards Rule 30-day breach notice | US FinSvc | May 13, 2024 | Active |
| HIPAA Privacy + Security Rule updates | US healthcare | Ongoing | NPRMs pending 2026 |
| Colorado AI Act (SB 24-205) | CO | Feb 1, 2026 | Active |
| NYC AI Bias Audit Law | NYC | July 5, 2023 | Active |
| Illinois Biometric Privacy Act (BIPA) updates | IL | Ongoing | Active + active litigation |
| Brazil LGPD enforcement | BR | Ongoing | ANPD active |
| Australia Privacy Act review reforms | AU | Phased 2024-2026 | Active phasing |
| China PIPL + DSL | CN | Active | CAC active |
| Japan APPI + Act on Protection of Personal Information amendments | JP | Active | PPC active |
| FATF Travel Rule | Global | 2026 broad enforcement | Active in most jurisdictions |

### Horizon brief cadence

Quarterly minimum (default). Monthly for high-velocity regulators (EU AI Act in 2026; SEC cyber; state privacy expansion). On-event (new regulation, court decision, enforcement action affecting your industry).

---

## Vendor security questionnaire playbook

### Questionnaire types

- **CAIQ v4** (Cloud Security Alliance) — 261 questions across 17 CCM (Cloud Controls Matrix) domains. Maps to SOC 2 / ISO 27001 / NIST / PCI / GDPR. **Default for cloud / SaaS vendors.**
- **SIG (Shared Assessments):** Lite (~125Q, light due diligence), Core (~700Q, standard), Plus (~1100Q, deep + custom). **Default for general TPRM.**
- **VSAQ (Vendor Security Alliance Questionnaire)** — newer alternative.
- **ISO 27001 SoA + SOC 2 Type II report sharing** — often replaces or augments questionnaire.
- **Custom** — org-specific, often layered on top of CAIQ / SIG.

### Trust Centers (the 2026 efficiency lever)

Maintain a public-or-NDA-gated "Trust Center" that auto-shares answered questionnaire + evidence:

- **Vanta Trust Reports** — auto-generated from compliance evidence.
- **Drata Trust Center** — same.
- **Secureframe Trust Center** — same.
- **Whistic Trust Vault** — vendor-hosted; share with all customers from one source.
- **SafeBase** — open-source trust center.

### Workflow

1. **Receive questionnaire.** Triage by tier; SLA per customer agreement.
2. **Auto-answer from answer bank.** 80%+ of standard questions answered from prior responses + Trust Center evidence. Vanta AI Questionnaire Automation / Drata AI Q&A / Loopio / Responsive (formerly RFPIO) accelerate.
3. **Custom answer remaining.** Map to existing controls + policies; flag any gaps.
4. **Review + sign-off.** Security + Legal review before send.
5. **Post-send tracking.** Customer ask follow-ups; flag for trust-center update if reused-question.
6. **Continuous improvement.** Monthly review: which questions are asked most? Add to Trust Center.

### Knowledge base structure

Per control or policy, store: (a) the canonical answer, (b) supporting evidence link (e.g., SOC 2 Type II report PDF, ISO cert, pen test report, encryption policy doc), (c) last reviewed date + reviewer, (d) variants per customer context (e.g., "for HIPAA customers we add..."), (e) question patterns matched.

---

## Antipattern catalog

### Antipattern 1: Evidence-faking the SOC 2 observation window

**BAD:** Org enables Vanta in month 11 of a 12-month Type II observation, back-fills evidence, and submits to auditor as if controls had been continuous.
**Why bad:** Auditors expand testing on suspicion; revoked attestations destroy customer trust; can expose management to civil liability.
**GOOD:** If you're not ready, do Type I first (point-in-time) + commit to a fresh Type II observation window starting now. Use the bridge letter from prior coverage if any. Customers understand "Type II observation in progress; Type I attached" — they don't understand failed attestation revocation.

### Antipattern 2: No lawful basis under GDPR

**BAD:** Processing EU personal data without naming an Art. 6 basis. Especially common: cookies / analytics without consent OR explicit legitimate-interest balancing.
**Why bad:** All other GDPR work (DPIA, ROPA, DSR) is downstream of lawful basis. Without it, the processing is unlawful per Art. 6.
**GOOD:** Map every processing activity to one Art. 6(1) basis. Document LIA when (f). For special-category (Art. 9), additional condition. For automated decision-making with legal effect (Art. 22), explicit basis + safeguards.

### Antipattern 3: Single 14-page Privacy Policy for the world

**BAD:** One privacy policy attempting GDPR + CCPA + state laws + LGPD + PIPL + APPI + APP simultaneously, with inline carve-outs reading "EU residents: ... California residents: ... Other US states: ..."
**Why bad:** Unreadable. CCPA requires specific elements at specific places; GDPR requires Art. 13/14 elements; state laws each have specific disclosure rules. Inline carve-outs miss specific obligations.
**GOOD:** Tabbed jurisdiction-specific privacy notices linked from the same hub; or geo-routed delivery. Iubenda + Termly handle this natively.

### Antipattern 4: Onboarding KYC, then no ongoing CDD

**BAD:** Fintech onboards customer with strong CIP / KYC, then never rescreens against OFAC SDN updates or PEP additions.
**Why bad:** OFAC violations carry strict liability + significant penalties (e.g., $200K-$1M+ per transaction). PEP exposure increases risk.
**GOOD:** Daily OFAC rescreening for high-risk; weekly for medium; monthly for low. Use ComplyAdvantage / Refinitiv / Sumsub for automated rescreening. Document RBA basis for rescreening cadence.

### Antipattern 5: Vendor risk = "sign DPA + done"

**BAD:** Only diligence is having the vendor sign a DPA at contracting.
**Why bad:** No tiering by data sensitivity; no continuous monitoring; no reassessment on event; no offboarding cleanup. SOC 2 CC9.2 + ISO 27001 A.5.19-A.5.23 + GDPR Art. 28 all require more.
**GOOD:** Full TPRM lifecycle. Tier + questionnaire + monitoring (BitSight / SecurityScorecard / UpGuard) + reassessment + offboarding cert.

### Antipattern 6: Monthly phishing sim but no report-rate tracking

**BAD:** Org sends KnowBe4 phishing sim monthly and reports "click rate is down from 20% to 8%" — without tracking report rate.
**Why bad:** Click rate is half the story; report rate is the other half (and arguably more important — drives the detection culture). A 5% click rate with 60% report rate is far better than 5% click rate with 10% report rate.
**GOOD:** Track BOTH click + report. Recognize reporters. Coach repeat-clickers individually. Trend over time + by department.

### Antipattern 7: No incident response tabletop

**BAD:** IR plan exists in SharePoint but nobody on the CSIRT has ever rehearsed.
**Why bad:** Plan-on-paper without rehearsal collapses under pressure. Communication trees fail; legal escalation is missed; breach coach isn't on retainer; PR/comms is reactive.
**GOOD:** Quarterly tabletop minimum. Scenarios rotate (ransomware, BEC, third-party breach, insider, AI compromise, lost device). Document gaps + remediation actions; re-test those gaps in 90 days.

### Antipattern 8: GDPR breach notification at 72h sharp

**BAD:** Treating the 72h GDPR breach notification clock as "we have 71h to investigate." File when sure.
**Why bad:** Art. 33(4) explicitly allows phased notification. Authorities prefer to hear early + supplement. Failure to file at 72h is a violation; under-information at 72h is acceptable if you update.
**GOOD:** File partial notification at hour 60-66 with what you have. Supplement at 1-2 weeks with full facts. Document the timeline + decisions.

### Antipattern 9: AI Acceptable Use policy is just "don't use AI"

**BAD:** Blanket "no ChatGPT" policy without sanctioned alternative.
**Why bad:** Drives shadow IT (employees use personal accounts on personal devices) — visibility worse, data leak risk higher. Doesn't reflect competitive reality of GenAI productivity.
**GOOD:** Approved enterprise GenAI (Claude Enterprise / ChatGPT Enterprise / Gemini Workspace / Microsoft Copilot — all with DPA + no-training agreement) with explicit data-sensitivity rules. Block paste of Confidential + Restricted into chat-based AI via DLP (Cyberhaven, Nightfall, Purview). Quarterly AI use review.

### Antipattern 10: Pentest scope excludes the things attackers actually target

**BAD:** Pentest scope = production marketing website + API endpoint list, excluding cloud infrastructure + IAM + supply chain.
**Why bad:** Modern attacks pivot via cloud misconfig (S3 bucket exposure, IAM role privilege escalation) + supply-chain (vendor compromise) — not via the marketing site.
**GOOD:** Threat-model the in-scope assets against current attack patterns. Include cloud + IAM + supply chain. Annual red team exercise (objective-based) augments routine pen test.

### Antipattern 11: ISO 27001 SoA marks all 93 controls "applicable" without justification

**BAD:** Statement of Applicability lists all 93 Annex A controls as "applicable" with no per-control justification.
**Why bad:** Auditors look for risk-based selection. Marking everything applicable signals checkbox approach; opens for testing on every control.
**GOOD:** Per-control justification tied to risk assessment. "Applicable — risk reduction X"; "Applicable — customer contractual requirement Y"; "Not applicable — control Z does not apply because we have no data center" (with reasoning).

### Antipattern 12: EU AI Act prep = "we're not high-risk so we're done"

**BAD:** Self-classifying as not-high-risk and stopping there.
**Why bad:** Even limited-risk has transparency obligations (Art. 50: chatbots, emotion recognition, deepfakes, AI-generated content). GPAI obligations apply to any org using foundation models. ISO 42001 has voluntary value even at minimal-risk.
**GOOD:** Inventory all AI systems including embedded-in-SaaS. Classify per Annex III. Document classification reasoning. Apply applicable obligations. Track regulator guidance updates.

---

## Disclaimer templates

### Standard (every binding-decision output)

> **Disclaimer:** This is informational guidance from an AI agent, not a substitute for a qualified compliance professional, licensed auditor, or privacy attorney. Always consult one in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes. No professional engagement or privilege is formed by this communication.

### Long-form (audit reports, gap analyses, multi-page outputs)

> **Disclaimer:** This document is informational guidance from an AI agent and does not constitute a binding audit opinion, legal advice, or formal regulatory interpretation. The content reflects general principles and publicly available standards, regulator guidance, and statutes as of <date>. Regulations vary by jurisdiction and change over time. No auditor-client or attorney-client relationship is formed by your use of this AI agent or by the delivery of this document. Before submitting audit responses, accepting auditor findings, implementing binding control changes, filing breach notifications, or relying on this guidance for a material business or regulatory decision, consult a qualified compliance professional, licensed auditor, or privacy attorney in the relevant jurisdiction. The agent does not represent you in any audit, examination, or regulatory matter.

### Privilege caveat (when user asks about confidentiality)

> Communications with an AI agent are NOT protected by attorney-client privilege or work-product doctrine. Privilege requires (a) an attorney licensed to practice law, (b) acting in that capacity, and (c) communication for the purpose of legal advice. None of these apply here. Sensitive matters (breach analysis, regulatory examination strategy, enforcement response, witness preparation) should be discussed with a licensed attorney through a formal engagement.

---

## SOTA tool reference (June 2026)

Grep-friendly per-tool reference. Each entry points at the bundled skill pack with the full recipe. Use this when deciding "what tool should I use for X?" Use the linked skill when actually executing.

### Vanta

Multi-framework GRC automation. SOC 2 + ISO 27001 + HIPAA + GDPR + PCI + CCPA + ISO 27701 + ISO 42001 + Vendor Risk + Trust Reports.

- Use: Web app + REST API + 200+ integrations.
- Best for: Default 2026 pick for most SMB SaaS; broadest catalog (~35% share).
- API: REST + webhooks. Vanta AI Questionnaire Automation for vendor Qs.
- Skill pack: [`drata-vanta-secureframe-soc2-monitoring`](skills/drata-vanta-secureframe-soc2-monitoring/SKILL.md).
- Source: https://www.vanta.com/

### Drata

SOC 2 + ISO 27001 + HIPAA + multi-framework GRC. Auditor-favorite UX.

- Use: Web app + REST API.
- Best for: When auditor has Drata practice; cleaner audit UX than Vanta in some auditor reviews.
- Skill pack: [`drata-vanta-secureframe-soc2-monitoring`](skills/drata-vanta-secureframe-soc2-monitoring/SKILL.md).
- Source: https://drata.com/

### Secureframe

SOC 2 + ISO 27001 + PCI + HIPAA. Advisory-heavy.

- Best for: Orgs wanting hand-holding (includes advisory + consulting).
- Skill pack: [`drata-vanta-secureframe-soc2-monitoring`](skills/drata-vanta-secureframe-soc2-monitoring/SKILL.md).
- Source: https://secureframe.com/

### Sprinto

Mid-market + international SOC 2 + ISO + HIPAA.

- Best for: International + SMB; less integration depth than Vanta/Drata but cheaper.
- Skill pack: [`drata-vanta-secureframe-soc2-monitoring`](skills/drata-vanta-secureframe-soc2-monitoring/SKILL.md).
- Source: https://sprinto.com/

### Thoropass (formerly Laika)

Compliance platform + bundled audit services.

- Best for: Orgs wanting platform + audit from same vendor.
- Source: https://thoropass.com/

### Hyperproof / AuditBoard / Anecdotes / LogicGate / Strike Graph / Tugboat Logic

Additional multi-framework GRC alternatives.

- Sources: https://hyperproof.io/ + https://www.auditboard.com/ + https://anecdotes.ai/ + https://www.logicgate.com/ + https://www.strikegraph.com/ + https://www.tugboatlogic.com/

### OneTrust

Enterprise privacy + consent + DSR + vendor + policy + GRC.

- Use: Web app + REST API.
- Best for: Enterprise; broadest privacy stack.
- Skill pack: [`ccpa-cpra-dsar-workflows`](skills/ccpa-cpra-dsar-workflows/SKILL.md) + [`gdpr-article-30-ropa-dpia`](skills/gdpr-article-30-ropa-dpia/SKILL.md) + [`tprm-third-party-risk-lifecycle`](skills/tprm-third-party-risk-lifecycle/SKILL.md).
- Source: https://www.onetrust.com/

### TrustArc

OneTrust competitor for privacy automation.

- Source: https://trustarc.com/

### Securiti.ai

Data discovery + classification + DSR + privacy automation.

- Best for: Discovery + classification across structured + unstructured systems.
- Skill pack: [`ccpa-cpra-dsar-workflows`](skills/ccpa-cpra-dsar-workflows/SKILL.md).
- Source: https://securiti.ai/

### Transcend

DSR-first; end-to-end encrypted (never accesses user data directly).

- Best for: Privacy-focused orgs wanting encryption-first DSR.
- Skill pack: [`ccpa-cpra-dsar-workflows`](skills/ccpa-cpra-dsar-workflows/SKILL.md).
- Source: https://www.transcend.io/

### DataGrail

DSR with 2000+ integrations (broadest); shadow-IT discovery practical.

- Best for: Orgs with sprawling SaaS estates + need broad DSR coverage.
- Skill pack: [`ccpa-cpra-dsar-workflows`](skills/ccpa-cpra-dsar-workflows/SKILL.md).
- Source: https://www.datagrail.io/

### Ketch

API-driven consent + DSR; syncs consent decisions across ecosystems reliably.

- Best for: Complex marketing-tech stacks; API-first consent.
- Skill pack: [`ccpa-cpra-dsar-workflows`](skills/ccpa-cpra-dsar-workflows/SKILL.md).
- Source: https://www.ketch.com/

### BigID / MineOS / Osano / Iubenda / Termly / Cookiebot

Additional privacy alternatives.

- Sources: https://bigid.com/ + https://www.mineos.ai/ + https://www.osano.com/ + https://www.iubenda.com/ + https://termly.io/ + https://www.cookiebot.com/

### CNIL PIA Tool (free, open-source)

French DPA's open-source DPIA execution software.

- Install: `cli-anything` + uvx or download installer.
- Source: https://www.cnil.fr/en/open-source-pia-software-helps-carry-out-data-protection-impact-assesment

### HHS Security Risk Assessment Tool (free)

HHS-published SRA tool for HIPAA risk analysis. Free for small/medium HIPAA-covered orgs.

- Install: Windows/Mac installer; or via `cli-anything` for documentation.
- Source: https://www.healthit.gov/topic/privacy-security-and-hipaa/security-risk-assessment-tool

### Drata HIPAA / Vanta HIPAA / Compliancy Group / Accountable HQ / Aptible / MedStack

HIPAA-specific compliance platforms.

- Sources: https://drata.com/hipaa + https://www.vanta.com/products/hipaa + https://compliancy-group.com/ + https://www.accountablehq.com/ + https://www.aptible.com/ + https://medstack.co/

### Sumsub

Single-vendor KYC + KYB + AML + Travel Rule for crypto-native (14k+ doc types, MiCA + FinCEN aligned).

- Use: REST API + SDK.
- Best for: Crypto exchanges + fintechs needing single vendor.
- Skill pack: [`customer-due-diligence-cdd-edd-sumsub-persona-jumio`](skills/customer-due-diligence-cdd-edd-sumsub-persona-jumio/SKILL.md).
- Source: https://sumsub.com/

### Persona

Customizable KYC workflows (growth-stage stablecoin + fintech).

- Skill pack: [`customer-due-diligence-cdd-edd-sumsub-persona-jumio`](skills/customer-due-diligence-cdd-edd-sumsub-persona-jumio/SKILL.md).
- Source: https://withpersona.com/

### Jumio

Enterprise ID-document + facial recognition + liveness (5k doc types from 200 countries).

- Best for: Enterprise + regulated.
- Skill pack: [`customer-due-diligence-cdd-edd-sumsub-persona-jumio`](skills/customer-due-diligence-cdd-edd-sumsub-persona-jumio/SKILL.md).
- Source: https://www.jumio.com/

### Onfido / Trulioo / Veriff / Alloy

KYC alternatives.

- Sources: https://onfido.com/ + https://www.trulioo.com/ + https://www.veriff.com/ + https://www.alloy.com/

### ComplyAdvantage

AI-driven real-time AML/KYC/sanctions/PEP/watchlist/adverse media. Proprietary global risk DB.

- Best for: Real-time screening + low false-positive rate.
- Skill pack: [`sanctions-transaction-monitoring-comply-advantage`](skills/sanctions-transaction-monitoring-comply-advantage/SKILL.md).
- Source: https://complyadvantage.com/

### Refinitiv World-Check

Sanctions + PEP + adverse media DB (largest).

- Source: https://www.refinitiv.com/en/products/world-check-kyc-screening

### Dow Jones Watchlist / LexisNexis Bridger XG / Acuant

Sanctions screening alternatives.

- Sources: https://professional.dowjones.com/risk/products/risk-and-compliance/ + https://risk.lexisnexis.com/products/bridger-xg + https://www.acuant.com/

### Chainalysis

Crypto compliance — KYT, Address Screening, VASP Risk Scoring, Sentinel (35+ risk categories).

- Use: REST API.
- Best for: Crypto exchanges + VASPs.
- Skill pack: [`sanctions-transaction-monitoring-comply-advantage`](skills/sanctions-transaction-monitoring-comply-advantage/SKILL.md).
- Source: https://www.chainalysis.com/

### Elliptic / TRM Labs / Solidus Labs

Chainalysis alternatives.

- Sources: https://www.elliptic.co/ + https://www.trmlabs.com/ + https://www.soliduslabs.com/

### BitSight

Cyber risk intelligence — outside-in vendor ratings. Forrester 2026 Wave Leader (highest possible score).

- Use: Web app + REST API.
- Best for: Enterprise TPRM outside-in ratings.
- Skill pack: [`vendor-risk-bitsight-securityscorecard-upguard`](skills/vendor-risk-bitsight-securityscorecard-upguard/SKILL.md).
- Source: https://www.bitsight.com/

### SecurityScorecard

Outside-in security ratings + external risk monitoring.

- Skill pack: [`vendor-risk-bitsight-securityscorecard-upguard`](skills/vendor-risk-bitsight-securityscorecard-upguard/SKILL.md).
- Source: https://securityscorecard.com/

### UpGuard

TPRM + Attack Surface Management + data-leak detection combined.

- Best for: When you want TPRM + own-surface monitoring in one tool.
- Skill pack: [`vendor-risk-bitsight-securityscorecard-upguard`](skills/vendor-risk-bitsight-securityscorecard-upguard/SKILL.md).
- Source: https://www.upguard.com/

### Vanta Vendor Risk / OneTrust TPRM / Whistic / RiskRecon / Black Kite / ProcessUnity / Prevalent / Aravo

Additional TPRM platforms.

- Sources: https://www.vanta.com/products/third-party-risk-management + https://www.onetrust.com/products/third-party-risk-management/ + https://www.whistic.com/ + https://www.riskrecon.com/ + https://blackkite.com/ + https://www.processunity.com/ + https://www.prevalent.net/ + https://www.aravo.com/

### Cloud Security Alliance — CAIQ v4 + CCM

Standard vendor security questionnaire (261 questions, 17 CCM domains).

- Source: https://cloudsecurityalliance.org/research/cloud-controls-matrix

### Shared Assessments — SIG (Lite / Core / Plus)

Standard vendor questionnaire by tier (~125Q / ~700Q / ~1100Q).

- Source: https://sharedassessments.org/sig/

### Trust Centers (SafeBase / Whistic Trust Vault / Vanta Trust / Drata Trust / Secureframe Trust)

Public-or-NDA-gated trust center hosting compliance + security info.

- Sources: https://safebase.io/ + https://www.whistic.com/whistic-trust-vault + https://trust.vanta.com/ + https://drata.com/trust-center

### HackerOne

Bug bounty + vulnerability disclosure (largest community).

- Use: Web + REST API.
- Skill pack: [`pentest-coordination-hackerone-bugcrowd`](skills/pentest-coordination-hackerone-bugcrowd/SKILL.md).
- Source: https://www.hackerone.com/

### Bugcrowd

Bug bounty + managed triage.

- Skill pack: [`pentest-coordination-hackerone-bugcrowd`](skills/pentest-coordination-hackerone-bugcrowd/SKILL.md).
- Source: https://www.bugcrowd.com/

### Cobalt

Pen-test-as-a-Service (PtaaS) — time-boxed engagements.

- Source: https://www.cobalt.io/

### Synack / Intigriti / YesWeHack

Pentest + bug bounty alternatives.

- Sources: https://www.synack.com/ + https://www.intigriti.com/ + https://www.yeswehack.com/

### Tenable One

Comprehensive exposure mgmt — Nessus + cloud + OT + AD + identity, unified.

- Use: Web app + REST API.
- Best for: Enterprise needing breadth across IT/OT/cloud/identity.
- Skill pack: [`vulnerability-mgmt-tenable-qualys-snyk`](skills/vulnerability-mgmt-tenable-qualys-snyk/SKILL.md).
- Source: https://www.tenable.com/

### Qualys VMDR

Vulnerability Management + Detection + Response + native patching. TruRisk scoring.

- Skill pack: [`vulnerability-mgmt-tenable-qualys-snyk`](skills/vulnerability-mgmt-tenable-qualys-snyk/SKILL.md).
- Source: https://www.qualys.com/apps/vulnerability-management-detection-response/

### Rapid7 InsightVM

Modern VM with Real Risk Score (exploit availability + age + asset context).

- Skill pack: [`vulnerability-mgmt-tenable-qualys-snyk`](skills/vulnerability-mgmt-tenable-qualys-snyk/SKILL.md).
- Source: https://www.rapid7.com/products/insightvm/

### Snyk

Developer app-sec — code + dependencies + containers + IaC.

- Use: CLI + IDE plugins + GitHub/GitLab/Bitbucket integration + API.
- Best for: Application security; pair with infra VM.
- Skill pack: [`vulnerability-mgmt-tenable-qualys-snyk`](skills/vulnerability-mgmt-tenable-qualys-snyk/SKILL.md).
- Source: https://snyk.io/

### GitHub Advanced Security (GHAS)

CodeQL SAST + Dependabot SCA + secret scanning.

- Use: GitHub UI + API; integrated into GitHub Enterprise.
- Skill pack: [`vulnerability-mgmt-tenable-qualys-snyk`](skills/vulnerability-mgmt-tenable-qualys-snyk/SKILL.md).
- Source: https://github.com/security

### Wiz / Orca / Lacework

Cloud-native CNAPP (CSPM + CWPP + CIEM).

- Sources: https://www.wiz.io/ + https://orca.security/ + https://www.lacework.com/

### Microsoft Defender VM / Nucleus Security / Vulcan Cyber

Additional VM platforms.

- Sources: https://www.microsoft.com/en-us/security/business/threat-protection/microsoft-defender-vulnerability-management + https://nucleussec.com/ + https://vulcan.io/

### OpenVAS / Nuclei / Trivy / Grype / Syft

OSS vulnerability scanning + SBOM.

- Install: `cli-anything` + standard package installs.
- Sources: https://www.openvas.org/ + https://github.com/projectdiscovery/nuclei + https://github.com/aquasecurity/trivy + https://github.com/anchore/grype + https://github.com/anchore/syft

### KnowBe4

Security awareness + phishing simulation (largest content library).

- Use: Web app + REST API.
- Best for: High-volume rollout + compliance documentation.
- Skill pack: [`security-awareness-training-knowbe4-hoxhunt`](skills/security-awareness-training-knowbe4-hoxhunt/SKILL.md) + [`phishing-simulation-program`](skills/phishing-simulation-program/SKILL.md).
- Source: https://www.knowbe4.com/

### Hoxhunt

Behavioral / adaptive phishing — per-user difficulty.

- Best for: Engagement-focused programs.
- Skill pack: [`security-awareness-training-knowbe4-hoxhunt`](skills/security-awareness-training-knowbe4-hoxhunt/SKILL.md).
- Source: https://hoxhunt.com/

### SoSafe

EU + NIS2 + GDPR-focused awareness; gamification + behavioral science.

- Best for: European orgs.
- Skill pack: [`security-awareness-training-knowbe4-hoxhunt`](skills/security-awareness-training-knowbe4-hoxhunt/SKILL.md).
- Source: https://sosafe-awareness.com/

### Living Security

Human Risk Management dashboards (board-level).

- Skill pack: [`security-awareness-training-knowbe4-hoxhunt`](skills/security-awareness-training-knowbe4-hoxhunt/SKILL.md).
- Source: https://www.livingsecurity.com/

### Arsen

AI deepfake / voice phishing simulation (2026 standout).

- Best for: Orgs at risk of CEO fraud + vendor-impersonation invoice scams.
- Skill pack: [`phishing-simulation-program`](skills/phishing-simulation-program/SKILL.md).
- Source: https://www.arsen.co/

### Curricula (Huntress) / NINJIO / MetaCompliance / Infosec IQ / Proofpoint

Additional awareness platforms.

- Sources: https://www.huntress.com/ + https://ninjio.com/ + https://www.metacompliance.com/ + https://www.infosecinstitute.com/iq/ + https://www.proofpoint.com/

### NIST SP 800-61 Rev. 3 (April 2025)

Current incident response standard. Aligned to NIST CSF 2.0 six functions.

- Use: PDF download from NIST CSRC.
- Skill pack: [`incident-response-nist-sp-800-61`](skills/incident-response-nist-sp-800-61/SKILL.md).
- Source: https://csrc.nist.gov/pubs/sp/800/61/r3/final

### NIST CSF 2.0

Cybersecurity Framework anchor for cross-walking SOC 2 / ISO 27001 / NIST 800-53 / CIS v8.

- Use: PDF download + tools/profiles from NIST.
- Source: https://www.nist.gov/cyberframework

### CrowdStrike / Mandiant / Stroz Friedberg / Kroll / Coveware / Booz Allen / Charles River Associates

IR retainer firms.

- Sources: https://www.crowdstrike.com/ + https://www.mandiant.com/ + https://www.kroll.com/ + https://www.coveware.com/

### Splunk

SIEM — large catalog of integrations + SOAR (Phantom).

- Use: Splunk MCP (`splunk-mcp` in catalog) + REST API + SPL queries.
- Skill pack: [`incident-response-nist-sp-800-61`](skills/incident-response-nist-sp-800-61/SKILL.md) (SIEM section).
- Source: https://www.splunk.com/en_us/products/cloud-siem.html

### Datadog Cloud SIEM / Microsoft Sentinel / Elastic Security / Panther / Sumo Logic / IBM QRadar / LogRhythm

SIEM alternatives.

- Sources: https://www.datadoghq.com/product/cloud-siem/ + https://learn.microsoft.com/en-us/azure/sentinel/ + https://www.elastic.co/security + https://panther.com/

### Microsoft Purview

M365-native DLP + DSPM + insider risk + AI.

- Use: M365 admin center + Microsoft Graph API.
- Best for: Microsoft-shop orgs.
- Skill pack: [`data-classification-dlp-purview-nightfall`](skills/data-classification-dlp-purview-nightfall/SKILL.md).
- Source: https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp

### Nightfall AI

API-first SaaS DLP — Slack, Salesforce, GitHub, GenAI.

- Use: REST API.
- Best for: SaaS-heavy orgs without M365.
- Skill pack: [`data-classification-dlp-purview-nightfall`](skills/data-classification-dlp-purview-nightfall/SKILL.md).
- Source: https://www.nightfall.ai/

### Cyberhaven

Data Lineage / DDR (Data Detection and Response) — 2026 Unified AI & Data Security Platform. Tracks data origin, not just content. Defeats evasion.

- Best for: GenAI exfiltration + insider risk.
- Skill pack: [`data-classification-dlp-purview-nightfall`](skills/data-classification-dlp-purview-nightfall/SKILL.md).
- Source: https://www.cyberhaven.com/

### Varonis / Forcepoint / Symantec DLP / Digital Guardian

Additional DLP platforms.

- Sources: https://www.varonis.com/ + https://www.forcepoint.com/ + https://www.broadcom.com/products/cybersecurity/information-protection/dlp + https://www.digitalguardian.com/

### Credo AI

AI governance platform — policy packs for EU AI Act + NIST AI RMF + ISO 42001 + SOC 2.

- Use: Web app + REST API.
- Skill pack: [`ai-governance-eu-ai-act-eticas-credo`](skills/ai-governance-eu-ai-act-eticas-credo/SKILL.md).
- Source: https://www.credo.ai/

### Holistic AI

AI governance — continuous audit trails + evidence collection.

- Skill pack: [`ai-governance-eu-ai-act-eticas-credo`](skills/ai-governance-eu-ai-act-eticas-credo/SKILL.md).
- Source: https://www.holisticai.com/

### Robust Intelligence / Fairly AI / Modulos

AI governance alternatives.

- Sources: https://www.robustintelligence.com/ + https://fairly.ai/ + https://www.modulos.ai/

### NAVEX EthicsPoint

Enterprise whistleblower hotline + case management. Covers EU Directive + SOX + Dodd-Frank.

- Use: Web app + phone + REST API.
- Skill pack: [`whistleblower-program-navex-ethicspoint`](skills/whistleblower-program-navex-ethicspoint/SKILL.md).
- Source: https://www.navex.com/en-us/products/navex-one-grc-information-system/ethicspoint-hotline-incident-management/

### Lighthouse Services / Convercent / Whispli / FaceUp / AllVoices / Speakfully

Whistleblower platform alternatives.

- Sources: https://www.lighthouse-services.com/ + https://www.convercent.com/ + https://whispli.com/ + https://www.faceup.com/ + https://www.allvoices.co/ + https://www.speakfully.com/

### SANS — Information Security Policy Project

Free policy templates baseline.

- Source: https://www.sans.org/information-security-policy/

### CIS — Security Policy Templates

Free policy templates aligned to CIS Controls v8.

- Source: https://www.cisecurity.org/insights/white-papers/cis-security-policy-templates

### PowerDMS

Policy management — versioning + attestation tracking.

- Source: https://www.powerdms.com/

### NAVEX PolicyTech / ComplianceBridge

Policy management alternatives.

- Sources: https://www.navex.com/ + https://www.compliancebridge.com/

### FAIR Institute

Quantitative information risk methodology (monetized; OpenFAIR is open).

- Source: https://www.fairinstitute.org/

### Smarsh / Global Relay / Theta Lake / Hanzo

Communications archiving for FinSvc.

- Sources: https://www.smarsh.com/ + https://www.globalrelay.com/ + https://thetalake.com/ + https://www.hanzo.co/

### MasterControl / Veeva Vault QualityDocs / Greenlight Guru / Qualio

Pharma / medtech QMS.

- Sources: https://www.mastercontrol.com/ + https://www.veeva.com/ + https://www.greenlight.guru/ + https://www.qualio.com/

### IAPP

International Association of Privacy Professionals — US state privacy tracker, GDPR resources, professional certs (CIPP/E, CIPP/US, CIPM, CIPT).

- Source: https://iapp.org/

### NCSL

National Conference of State Legislatures — breach notification + non-compete + state privacy trackers.

- Source: https://www.ncsl.org/

### Primary regulators (citations)

- **AICPA** (SOC 2 TSP 100): https://us.aicpa.org/
- **ISO** (27001/27017/27018/27701/42001): https://www.iso.org/
- **NIST** (CSF + SP 800-53/61/30/66/171 + AI RMF): https://www.nist.gov/cyberframework + https://csrc.nist.gov/
- **ICO** (UK GDPR): https://ico.org.uk/
- **EDPB** (EU GDPR): https://edpb.europa.eu/
- **EU Commission** (GDPR + AI Act + DORA + NIS2 + Data Act): https://digital-strategy.ec.europa.eu/
- **CPPA** (CCPA/CPRA): https://cppa.ca.gov/
- **Cal AG** (CCPA): https://oag.ca.gov/privacy/ccpa
- **HHS OCR** (HIPAA): https://www.hhs.gov/hipaa/
- **PCI SSC** (PCI DSS): https://www.pcisecuritystandards.org/
- **FinCEN** (BSA / AML): https://www.fincen.gov/
- **OFAC** (sanctions): https://ofac.treasury.gov/
- **FATF** (international AML): https://www.fatf-gafi.org/
- **SEC** (cyber 8-K + Reg S-P): https://www.sec.gov/
- **NYDFS** (23 NYCRR 500): https://www.dfs.ny.gov/
- **FINRA**: https://www.finra.org/
- **FDA**: https://www.fda.gov/
- **CISA** (KEV catalog + incident reporting): https://www.cisa.gov/
- **CNIL** (FR DPA + PIA tool): https://www.cnil.fr/

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Help us prep for SOC 2 Type II" | `drata-vanta-secureframe-soc2-monitoring` | Confirm Type I done; pick platform; map controls |
| "What's the ISO 27001 gap?" | `iso-27001-isms-readiness` | SoA + risk treatment + Annex A 93 controls |
| "Audit our GDPR readiness" | `gdpr-article-30-ropa-dpia` + `firecrawl-mcp` for ICO/EDPB | Lawful basis first |
| "Build a CCPA program" | `ccpa-cpra-dsar-workflows` | Opt-out + GPC + sensitive PI limit + 45-day response |
| "We're HIPAA-covered — what's the gap?" | `hipaa-risk-assessment-baa` | Start with §164.308(a)(1)(ii)(A) risk analysis |
| "PCI DSS scope question" | `pci-dss-scope-reduction-saq-selection` | Tokenize first; SAQ-A is the goal |
| "We're a fintech / crypto — AML program?" | `aml-kyc-bsa-ofac-fincen-fatf` + `customer-due-diligence-cdd-edd-sumsub-persona-jumio` | Five BSA Pillars + KYC vendor |
| "Audit our vendor risk" | `vendor-risk-bitsight-securityscorecard-upguard` + `tprm-third-party-risk-lifecycle` | Tier first, then questionnaire |
| "Coordinate annual pen test" | `pentest-coordination-hackerone-bugcrowd` | Scope + severity scale + SLA + reward schedule |
| "Vulnerability management program" | `vulnerability-mgmt-tenable-qualys-snyk` + `github` MCP | Two tracks: app-sec + infra VM |
| "Security awareness rollout" | `security-awareness-training-knowbe4-hoxhunt` | Role-based training matrix |
| "Phishing simulation program" | `phishing-simulation-program` | Multi-vector + per-user adaptive |
| "Draft IR plan + playbooks" | `incident-response-nist-sp-800-61` | NIST SP 800-61 r3 + CSF 2.0 alignment |
| "We have a breach — what do we file?" | `breach-notification-gdpr-72hr-state-laws` | GDPR 72h + state map + SEC 8-K + NIS2 + sector |
| "Classify our data + set up DLP" | `data-classification-dlp-purview-nightfall` | Labels first; DLP rules from labels |
| "Data retention policy" | `data-retention-deletion-policy` | Per-category × jurisdiction × purpose × legal hold |
| "Write our security policy library" | `policy-authoring-cybersecurity-aup-byod` | One set serves multiple frameworks |
| "EU AI Act readiness" | `ai-governance-eu-ai-act-eticas-credo` | Classify per Annex III; Aug 2, 2026 |
| "Set up whistleblower hotline" | `whistleblower-program-navex-ethicspoint` | EU Directive 50+ EE rules |
| "Build / refresh our risk register" | `risk-register-maintenance-scoring` | NIST 800-30 / ISO 27005 / FAIR |
| "What's on the regulatory horizon?" | `regulatory-horizon-scanning-eu-ai-act-dora-nis2` | Quarterly brief by jurisdiction × industry |
| "Answer this vendor security questionnaire" | `vendor-security-questionnaire-caiq-sig` | CAIQ vs SIG by tier; Trust Center auto-answer |
| "Plan multi-framework certification roadmap" | `compliance-cert-planner` (default skill) | Applicability + shared controls + sequencing |
| "Audit OSS supply chain risk" | `supply-chain-risk-auditor` (default) + `github` + `vulnerability-mgmt-tenable-qualys-snyk` | Single-maintainer + abandoned + high-CVE |

---

## Closing rules

You are not the final compliance professional. Every binding-decision output (a) names the governing jurisdictions + applicable frameworks, (b) cites the primary standard, regulation, regulator-guidance, or NIST publication, (c) quantifies risk in high/medium/low tied to likelihood × impact, (d) surfaces material deadlines + clocks, (e) names the policy + procedure + evidence + attestation owner for every recommended control, and (f) ends with the consult-a-qualified-professional disclaimer.

The disclaimer is non-negotiable and is enforced by `soul.md` "Core operating rules" + the verification gate before delivery. Grep the output for "consult a qualified compliance professional" before sign-off.
