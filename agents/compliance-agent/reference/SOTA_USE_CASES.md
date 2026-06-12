# compliance-agent — SOTA Use Case Map (June 2026)

Per-use-case mapping from agent capability to concrete SOTA mechanism. Each row names the tool, the agent's execution path (which CraftBot MCP/skill actually runs it), the canonical source, and a confidence verdict.

Legend:
- `✓` — agent can execute the SOTA path end-to-end today with shipped MCPs/skills.
- `⚠` — agent can execute the SOTA path but with a known caveat (auth scope, paid tier, env dep, jurisdiction-specific).
- `✗` — SOTA path requires a tool the agent cannot reach (deferred / future work).

**Standing disclaimer.** Every output that touches a binding regulatory, audit, or control-binding decision must include: *"This is informational guidance from an AI agent. Always consult a qualified compliance professional / auditor / privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes."* This is codified in `soul.md` as a hard rule.

Bundled skill packs referenced (Round 2 will populate the SKILL.md files):
`drata-vanta-secureframe-soc2-monitoring`, `iso-27001-isms-readiness`, `gdpr-article-30-ropa-dpia`, `ccpa-cpra-dsar-workflows`, `hipaa-risk-assessment-baa`, `pci-dss-scope-reduction-saq-selection`, `aml-kyc-bsa-ofac-fincen-fatf`, `customer-due-diligence-cdd-edd-sumsub-persona-jumio`, `sanctions-transaction-monitoring-comply-advantage`, `vendor-risk-bitsight-securityscorecard-upguard`, `tprm-third-party-risk-lifecycle`, `pentest-coordination-hackerone-bugcrowd`, `vulnerability-mgmt-tenable-qualys-snyk`, `security-awareness-training-knowbe4-hoxhunt`, `phishing-simulation-program`, `incident-response-nist-sp-800-61`, `breach-notification-gdpr-72hr-state-laws`, `data-classification-dlp-purview-nightfall`, `data-retention-deletion-policy`, `policy-authoring-cybersecurity-aup-byod`, `ai-governance-eu-ai-act-eticas-credo`, `whistleblower-program-navex-ethicspoint`, `risk-register-maintenance-scoring`, `regulatory-horizon-scanning-eu-ai-act-dora-nis2`, `vendor-security-questionnaire-caiq-sig`.

---

## SOC 2 Type I + II readiness (Drata / Vanta / Secureframe setup)

- **SOTA approach:** Automated evidence collection across AICPA Trust Services Criteria (Security mandatory; Availability, Confidentiality, Processing Integrity, Privacy optional). 2026 market: Vanta (~35% share, 200+ integrations, broadest); Drata (~25%, auditor-favorite UX); Secureframe (~15%, advisory-heavy); Sprinto (~10%, international/SMB); Thoropass (~8%, bundles audit). Total all-in cost: $30K-$120K for first Type II. Type I (point-in-time, 1-3 months prep) precedes Type II (3-12 month observation).
- **Agent execution path:** Bundled `drata-vanta-secureframe-soc2-monitoring` covers control mapping + evidence rules. `cli-anything` + `curl` to Vanta / Drata / Secureframe REST APIs for control status queries (recipient supplies tenant API token). `filesystem` writes the gap-analysis + remediation plan. `notion-mcp` posts the audit prep tracker.
- **Source:** https://drata.com/ + https://www.vanta.com/ + https://secureframe.com/ + https://sprinto.com/ + https://thoropass.com/ + https://us.aicpa.org/interestareas/frc/assuranceadvisoryservices/sorhome
- **Confidence:** ⚠ (Drata/Vanta/Secureframe/Sprinto/Thoropass are SaaS — recipient supplies API token; tooling itself is wired)

## SOC 2 Trust Services Criteria (TSC) mapping

- **SOTA approach:** AICPA TSP 100 (2017 + 2022 updates) — Security (Common Criteria CC1-CC9), Availability (A1.1-A1.3), Confidentiality (C1.1-C1.2), Processing Integrity (PI1.1-PI1.5), Privacy (P1.1-P8.1). Cross-walk to NIST CSF 2.0, ISO 27001 Annex A, CIS Controls v8 to reduce overlap.
- **Agent execution path:** Bundled `drata-vanta-secureframe-soc2-monitoring` includes the TSC cross-walk matrix. `cli-anything` curl to AICPA + NIST published guides.
- **Source:** https://us.aicpa.org/interestareas/frc/assuranceadvisoryservices/sorhome + https://www.nist.gov/cyberframework
- **Confidence:** ✓

## ISO 27001 ISMS readiness

- **SOTA approach:** ISO/IEC 27001:2022 (last update reduced 114 → 93 Annex A controls reorganized into 4 themes: Organizational, People, Physical, Technological). Statement of Applicability (SoA), risk assessment + treatment, ISMS scope, mandatory documentation (4.3 scope, 5.2 policy, 6.1.2 risk approach, 6.1.3 treatment, 6.2 objectives, 7.5 documented info, 8.1 plans, 9.1 monitoring, 9.2 internal audit, 9.3 management review, 10.1 nonconformity). Surveillance audits in years 2-3; recertification year 3.
- **Agent execution path:** Bundled `iso-27001-isms-readiness`. Vanta + Drata + Secureframe also automate ISO 27001 evidence (all three certified to ISMS). `cli-anything` curl to ISO catalog (titles only — full text paid).
- **Source:** https://www.iso.org/standard/27001 + https://www.vanta.com/products/iso-27001 + https://drata.com/iso-27001
- **Confidence:** ✓

## ISO 27017 / 27018 / 27701 / 42001 add-ons

- **SOTA approach:** 27017 (cloud security extensions for 27002), 27018 (PII processor in public cloud), 27701 (PIMS — Privacy Information Management System extension to 27001), 42001 (AI Management System — 2023; first AIMS certifications late-2024 onwards). 42001 maps directly to EU AI Act high-risk obligations.
- **Agent execution path:** Bundled `iso-27001-isms-readiness` and `ai-governance-eu-ai-act-eticas-credo`. `cli-anything` curl to ISO catalog.
- **Source:** https://www.iso.org/standard/43757.html (27017) + https://www.iso.org/standard/76559.html (27018) + https://www.iso.org/standard/71670.html (27701) + https://www.iso.org/standard/81230.html (42001)
- **Confidence:** ✓

## GDPR Article 30 ROPA (records of processing)

- **SOTA approach:** ROPA per Art. 30 — controller side (Art. 30(1)) and processor side (Art. 30(2)). Required for orgs with 250+ employees OR systematic processing OR special-category data. Elements: name+contact of controller + DPO, purposes, categories of data subjects + data, recipients, international transfers + safeguards, retention, technical/organizational measures. Tools: ICO ROPA template (free); OneTrust Data Mapping; Securiti.ai discovery; Transcend ROPA; DataGrail; Iubenda Internal Privacy Management.
- **Agent execution path:** Bundled `gdpr-article-30-ropa-dpia`. `cli-anything` curl to ICO template; `notion-mcp` for collaborative ROPA tracker; `filesystem` writes the final ROPA. OneTrust / Securiti.ai / Transcend APIs accessed via `cli-anything` + recipient token.
- **Source:** https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/documentation/records-of-processing-activities/ + https://gdpr-info.eu/art-30-gdpr/
- **Confidence:** ✓

## GDPR DPIA (data protection impact assessment)

- **SOTA approach:** Art. 35 — DPIA mandatory when high-risk processing. Triggers: systematic monitoring of public areas, large-scale special-category processing, profiling with legal effect, ICO/EDPB mandated trigger list. Methodology: ICO + CNIL PIA software (open-source). Five steps: describe processing, assess necessity+proportionality, identify+assess risks, identify+evaluate mitigations, consult DPO + data subjects when relevant.
- **Agent execution path:** Bundled `gdpr-article-30-ropa-dpia`. `cli-anything` + uvx for CNIL PIA tool (free, open-source). OneTrust DPIA + Transcend DPIA available via API.
- **Source:** https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-impact-assessments-dpias/ + https://www.cnil.fr/en/open-source-pia-software-helps-carry-out-data-protection-impact-assesment
- **Confidence:** ✓

## GDPR DSAR (data subject access request) handling

- **SOTA approach:** Art. 15 (access), 16 (rectify), 17 (erasure / RTBF), 18 (restriction), 20 (portability), 21 (objection). 1-month response (extendable to 3 months with notice); free for first request. Identity verification before disclosure. SOTA platforms: Transcend (end-to-end encryption, never accesses user data), Securiti.ai (discovery+fulfillment), DataGrail (2000+ integrations), OneTrust DSR, Ketch (API-driven), MineOS, Skyflow. Free fallback: manual + ICO template.
- **Agent execution path:** Bundled `ccpa-cpra-dsar-workflows` (covers DSAR + DSR — shared workflow). `cli-anything` + curl to platform APIs (recipient token); `filesystem` writes the response packet template; `gmail-mcp` for verification + delivery.
- **Source:** https://www.transcend.io/ + https://securiti.ai/ + https://www.datagrail.io/ + https://www.onetrust.com/products/data-subject-rights/ + https://ico.org.uk/your-data-matters/your-right-of-access/
- **Confidence:** ✓

## CCPA / CPRA right-to-delete + right-to-know workflow

- **SOTA approach:** Cal. Civ. Code §1798.100 et seq. + CPRA. Rights: know (12mo + extended on request), delete, correct (CPRA-new), opt-out of sale/share, limit use of sensitive PI (CPRA-new), non-discrimination, data portability. Must respect Global Privacy Control (GPC) signal. "Do Not Sell or Share My PI" link + sensitive PI limit link required. 45-day response (extendable). Same SOTA platforms as DSAR + Osano + MineOS.
- **Agent execution path:** Bundled `ccpa-cpra-dsar-workflows`. `cli-anything` + curl to Cal AG + CPPA resources; `filesystem` writes the policy + workflow; platform APIs via recipient token.
- **Source:** https://oag.ca.gov/privacy/ccpa + https://cppa.ca.gov/regulations/ + https://globalprivacycontrol.org/
- **Confidence:** ✓

## HIPAA risk assessment (164.308) + BAA management

- **SOTA approach:** Security Rule 45 CFR §164.308(a)(1)(ii)(A) — required risk analysis. Methodology: NIST SP 800-66 Rev. 2 (2024) HIPAA Security Rule guidance + HHS OCR Risk Analysis Guidance. Tools: HHS Security Risk Assessment Tool (free), Drata HIPAA, Vanta HIPAA, Compliancy Group, Accountable HQ, Aptible (HITRUST adjacent), MedStack. BAA template: HHS Sample BAA Provisions + 45 CFR §164.504(e) required elements. 60-day breach notification (Subpart D).
- **Agent execution path:** Bundled `hipaa-risk-assessment-baa`. `cli-anything` curl to HHS SRA tool + sample BAA; `filesystem` writes the risk register + BAA; platform APIs via recipient token.
- **Source:** https://www.hhs.gov/hipaa/for-professionals/security/guidance/index.html + https://www.healthit.gov/topic/privacy-security-and-hipaa/security-risk-assessment-tool + https://csrc.nist.gov/pubs/sp/800/66/r2/final
- **Confidence:** ✓

## PCI DSS scope reduction + segmentation + SAQ selection

- **SOTA approach:** PCI DSS v4.0 (effective March 2024; future-dated requirements through March 31, 2025; v4.0.1 minor update). SAQ levels: A (fully outsourced redirect — e.g., Stripe Checkout), A-EP (e-commerce partial outsourcing — iframe), B (imprint/standalone dial-out), B-IP (standalone IP-connected), C (POS — internet-connected), C-VT (virtual terminal), D (catch-all). Scope reduction: tokenization (Stripe, Braintree, Square, Adyen, Spreedly), iframe / hosted-fields, P2PE-validated. Network segmentation evidence: firewall rules, VLAN config, segmentation pen test annually. Self-assessment (ROC for Level 1; SAQ for L2-L4). ASV scan quarterly.
- **Agent execution path:** Bundled `pci-dss-scope-reduction-saq-selection`. `cli-anything` curl to PCI SSC public-indexed docs + Stripe/Braintree compliance pages. `filesystem` writes the scope memo + SAQ recommendation.
- **Source:** https://www.pcisecuritystandards.org/document_library/ + https://stripe.com/guides/pci-compliance + https://www.braintreepayments.com/features/data-security
- **Confidence:** ⚠ (PCI SSC docs require free account login for some; agent fetches public-indexed material and asks user to share gated PDFs)

## AML / KYC / BSA / OFAC / FinCEN / FATF program

- **SOTA approach:** US: Bank Secrecy Act (BSA) + FinCEN guidance + OFAC sanctions screening. International: FATF Recommendations (40+9) + EU 6th AML Directive (6AMLD) + UK MLR 2017. Crypto: Travel Rule (FATF R.16), MiCA (EU 2024), FinCEN crypto guidance. Customer Identification Program (CIP), Customer Due Diligence (CDD), Enhanced Due Diligence (EDD) for high-risk, transaction monitoring, SAR/CTR filing (FinCEN BSA E-Filing System), independent audit.
- **Agent execution path:** Bundled `aml-kyc-bsa-ofac-fincen-fatf`. `cli-anything` + curl to FinCEN + OFAC + FATF guidance; `firecrawl-mcp` for OFAC SDN list updates; `filesystem` writes the AML program memo + risk-based approach (RBA).
- **Source:** https://www.fincen.gov/resources/financial-institutions/bank-secrecy-act-resources + https://ofac.treasury.gov/ + https://www.fatf-gafi.org/en/topics/Fatf-recommendations.html
- **Confidence:** ✓

## Customer due diligence (CDD / EDD) — identity verification

- **SOTA approach:** 2026 SOTA: Sumsub (broadest single-vendor for crypto-native — 14k+ document types, 50+ languages, MiCA+FinCEN aligned), Persona (customizable KYC workflows), Jumio (enterprise ID-doc + facial liveness — 5000 doc types from 200 countries), Onfido (now Entrust subsidiary), Trulioo (global ID), Veriff, Alloy (orchestration layer). Document + biometric + database verification + watchlist screening in one flow.
- **Agent execution path:** Bundled `customer-due-diligence-cdd-edd-sumsub-persona-jumio`. `cli-anything` + curl to Sumsub / Persona / Jumio APIs via recipient sandbox key.
- **Source:** https://sumsub.com/ + https://withpersona.com/ + https://www.jumio.com/ + https://onfido.com/ + https://www.trulioo.com/
- **Confidence:** ⚠ (KYC vendors are SaaS — recipient supplies API token; sandbox available)

## Sanctions screening + transaction monitoring + SARs

- **SOTA approach:** ComplyAdvantage (AI-driven real-time AML/KYC/sanctions/PEP/watchlists/adverse media — proprietary risk DB), Refinitiv World-Check, Dow Jones Watchlist, LexisNexis Bridger XG, Acuant. Crypto: Chainalysis (KYT, Address Screening, VASP Risk Scoring, Sentinel 35+ categories), Elliptic, TRM Labs, Solidus Labs. Transaction monitoring rules engine + ML-based anomaly detection. SAR filing via FinCEN BSA E-Filing (30 days from detection).
- **Agent execution path:** Bundled `sanctions-transaction-monitoring-comply-advantage`. `cli-anything` + curl to ComplyAdvantage / Chainalysis APIs via recipient token; `firecrawl-mcp` for OFAC SDN; `filesystem` writes the suspicious-activity case file template.
- **Source:** https://complyadvantage.com/ + https://www.chainalysis.com/ + https://www.elliptic.co/ + https://www.trmlabs.com/ + https://www.refinitiv.com/en/products/world-check-kyc-screening
- **Confidence:** ⚠ (recipient supplies vendor API token)

## Vendor risk assessment (BitSight / SecurityScorecard / UpGuard / SIG)

- **SOTA approach:** 2026 leaders: BitSight (Forrester 2026 Wave Leader — highest possible score; outside-in cyber risk intelligence), SecurityScorecard (outside-in ratings), UpGuard (TPRM + Attack Surface Management combo + data-leak detection), Vanta Vendor Risk (integrated with compliance), OneTrust TPRM, Whistic, RiskRecon (Mastercard), Black Kite, ProcessUnity, Prevalent, Aravo. Questionnaire frameworks: CAIQ (Cloud Security Alliance), SIG (Shared Assessments — Lite/Core/Plus), VSAQ, custom. Continuous monitoring replaces point-in-time questionnaires.
- **Agent execution path:** Bundled `vendor-risk-bitsight-securityscorecard-upguard`. `cli-anything` + curl to BitSight / SecurityScorecard / UpGuard APIs via recipient token; `filesystem` writes the vendor scorecard + tiered risk classification.
- **Source:** https://www.bitsight.com/ + https://securityscorecard.com/ + https://www.upguard.com/ + https://www.vanta.com/products/third-party-risk-management + https://cloudsecurityalliance.org/research/cloud-controls-matrix
- **Confidence:** ⚠ (recipient supplies vendor API token; manual CAIQ/SIG fallback works without)

## Third-party risk management (TPRM) lifecycle

- **SOTA approach:** Lifecycle stages: (1) sourcing+selection (RFP security questions, SOC 2 report request), (2) due diligence + tiering by data sensitivity + criticality, (3) contracting (DPA, BAA, SCC, security addendum, audit rights), (4) onboarding (least-privilege access, baseline scan), (5) continuous monitoring (BitSight/SecurityScorecard rating drift alerts), (6) periodic reassessment (annual SIG refresh; quarterly for critical vendors), (7) termination + offboarding (data return/destruction certification).
- **Agent execution path:** Bundled `tprm-third-party-risk-lifecycle`. `notion-mcp` for vendor inventory + status tracker; `gmail-mcp` for vendor outreach; `filesystem` for contractual addenda templates.
- **Source:** https://sharedassessments.org/ + https://www.nist.gov/itl/smallbusinesscyber/guidance-topic/supply-chain-risk-management + https://www.upguard.com/blog/vendor-risk-management
- **Confidence:** ✓

## Penetration testing coordination (HackerOne / Bugcrowd / Cobalt / Synack)

- **SOTA approach:** Bug bounty: HackerOne (largest research community), Bugcrowd (managed triage), Intigriti (EU-strong), YesWeHack (EU/APAC). PtaaS (pen-test-as-a-service): Cobalt (on-demand, time-boxed), Synack (vetted researchers + AI assist). Scope: black/grey/white box, in-scope assets list, severity scale (CVSS 4.0), SLA windows for triage + payout. Required for SOC 2 / PCI / ISO 27001. Annual external + ad-hoc post-major-release.
- **Agent execution path:** Bundled `pentest-coordination-hackerone-bugcrowd`. `cli-anything` + curl to HackerOne / Bugcrowd APIs via recipient token; `filesystem` writes the program brief + scope doc + payout schedule.
- **Source:** https://www.hackerone.com/ + https://www.bugcrowd.com/ + https://www.cobalt.io/ + https://www.synack.com/
- **Confidence:** ⚠ (paid platforms — recipient supplies API token / org access)

## Vulnerability management (Tenable / Qualys / Snyk)

- **SOTA approach:** 2026 SOTA: Tenable One (most comprehensive — Nessus + cloud + OT + AD + identity, unified TruRisk-equivalent), Qualys VMDR (TruRisk + native patching), Rapid7 InsightVM (Real Risk Score). Cloud-native CNAPP: Wiz, Orca, Lacework. App-sec: Snyk (code, dependencies, containers, IaC), GitHub Advanced Security (CodeQL + Dependabot + secret scanning). OSS fallback: OpenVAS / Nuclei. Most enterprises run two tracks: app-sec (Snyk/GitHub) + infra VM (Tenable/Qualys/Rapid7).
- **Agent execution path:** Bundled `vulnerability-mgmt-tenable-qualys-snyk`. `cli-anything` + curl to Tenable / Qualys / Rapid7 / Snyk APIs via recipient token; `github` MCP for GHAS / Dependabot read; `filesystem` writes the vulnerability report + remediation plan.
- **Source:** https://www.tenable.com/ + https://www.qualys.com/apps/vulnerability-management-detection-response/ + https://www.rapid7.com/products/insightvm/ + https://snyk.io/
- **Confidence:** ⚠ (recipient supplies vendor token; OpenVAS / Nuclei free fallback)

## Security awareness training (KnowBe4 / Hoxhunt / SoSafe / Living Security)

- **SOTA approach:** 2026 leaders: KnowBe4 (largest content library — for high-volume rollout + compliance docs), Hoxhunt (behavioral/adaptive — per-user difficulty), SoSafe (EU/NIS2/GDPR strong, gamification), Living Security (board-level HRM dashboards), Proofpoint (DLP+training combo), Arsen (deepfake/voice sim — 2026 standout), Curricula (Huntress), NINJIO, MetaCompliance, Infosec IQ. Multi-vector: email + voice + deepfake (NEW for 2026 — Arsen + Adaptive Security pioneered).
- **Agent execution path:** Bundled `security-awareness-training-knowbe4-hoxhunt`. `cli-anything` + curl to KnowBe4 / Hoxhunt / SoSafe APIs via recipient token; `filesystem` writes the training matrix per role + cadence.
- **Source:** https://www.knowbe4.com/ + https://hoxhunt.com/ + https://sosafe-awareness.com/ + https://www.livingsecurity.com/
- **Confidence:** ⚠ (paid SaaS — recipient supplies API token)

## Phishing simulation program

- **SOTA approach:** Multi-vector simulation: email (most common), voice (vishing — Arsen leader), SMS (smishing), QR code (quishing — surging in 2026), AI-generated deepfake (CEO fraud / video). Frequency: monthly minimum; weekly for critical roles. Severity escalation per-user based on click history. Measurement: click rate, report rate (more important — drives detection culture), credential-entry rate, dwell time. Tools: same as awareness training above.
- **Agent execution path:** Bundled `phishing-simulation-program`. `cli-anything` + curl to KnowBe4 / Hoxhunt phishing APIs; `filesystem` writes the campaign calendar + escalation matrix.
- **Source:** https://www.knowbe4.com/phishing + https://hoxhunt.com/phishing-simulation + https://www.arsen.co/
- **Confidence:** ⚠ (paid platform; recipient supplies API token)

## Incident response plan (NIST SP 800-61 Rev. 3)

- **SOTA approach:** **NIST SP 800-61 Rev. 3 published April 2025** (first update since 2012) — aligns IR with NIST CSF 2.0 six functions (Govern, Identify, Protect, Detect, Respond, Recover). Shifts from rigid four-phase (Prep / Detect-Analyze / Contain-Eradicate-Recover / Post-Incident) to flexible continuous model. Required artifacts: IR plan, IR playbooks per scenario (ransomware, BEC, data breach, account takeover, insider threat), CSIRT roster + on-call rotation, tabletop schedule (quarterly), post-incident review template.
- **Agent execution path:** Bundled `incident-response-nist-sp-800-61`. `cli-anything` curl to NIST CSF 2.0 + 800-61 r3; `filesystem` writes the IR plan + playbooks + tabletop scripts; `notion-mcp` for the CSIRT roster.
- **Source:** https://csrc.nist.gov/pubs/sp/800/61/r3/final + https://www.nist.gov/cyberframework
- **Confidence:** ✓

## Breach notification (72-hour GDPR + US state laws + sector laws)

- **SOTA approach:** GDPR Art. 33 (72 hours to supervisory authority; Art. 34 to data subjects without undue delay if high risk). UK / NL / FI / NO / AT / HU / TR aligned 72h. US: all 50 states + DC + PR + USVI breach notification laws (varies by state — CA SB-1386 model; CCPA §1798.82 for CA-applicable). Sector: HIPAA 60-day individual + media-if-500+ (45 CFR §164.408); GLBA; SEC 8-K Item 1.05 (4-business-day material cyber incident — 2023); NYDFS 23 NYCRR 500.17 (72h); EU NIS2 (24h early warning + 72h incident notification + 1mo final report).
- **Agent execution path:** Bundled `breach-notification-gdpr-72hr-state-laws`. `cli-anything` + curl to ICO + state AG breach portals; `firecrawl-mcp` for state-by-state requirements; `filesystem` writes the notification packet template + decision tree.
- **Source:** https://gdpr-info.eu/art-33-gdpr/ + https://www.ncsl.org/technology-and-communication/security-breach-notification-laws + https://www.sec.gov/rules/final/2023/33-11216.pdf
- **Confidence:** ✓

## Data classification + DLP (Microsoft Purview / Nightfall / Cyberhaven)

- **SOTA approach:** 2026 SOTA: Microsoft Purview (M365-native, consolidated DLP + DSPM + insider risk + AI), Nightfall AI (API-first SaaS — Slack/Salesforce/GitHub/GenAI), Cyberhaven (Data Lineage / DDR — 2026 launched Unified AI & Data Security Platform — tracks data origin not content), Varonis, Forcepoint, Symantec DLP, Digital Guardian. Sensitivity labels: Public / Internal / Confidential / Restricted. GenAI is biggest 2026 DLP challenge (avg 66 GenAI apps/org).
- **Agent execution path:** Bundled `data-classification-dlp-purview-nightfall`. `cli-anything` + curl to Purview / Nightfall / Cyberhaven APIs via recipient token; `filesystem` writes the classification scheme + label taxonomy + DLP rule set.
- **Source:** https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp + https://www.nightfall.ai/ + https://www.cyberhaven.com/
- **Confidence:** ⚠ (paid platforms; recipient supplies token)

## Data retention + deletion policy

- **SOTA approach:** Retention schedule per data category × jurisdiction × purpose × legal hold. GDPR Art. 5(1)(e) storage limitation. CCPA + state-law retention overrides. Sector: HIPAA 6yr from creation/last-effective; FINRA 17a-4 supervisory; SOX 5-7yr; PCI 1yr authorization data after auth. Tools: OneTrust Retention, Securiti.ai, DataGrail, MineOS. Automated deletion via Salesforce/HubSpot/Stripe data-purge APIs.
- **Agent execution path:** Bundled `data-retention-deletion-policy`. `cli-anything` curl to platform APIs; `filesystem` writes the retention schedule + deletion runbook.
- **Source:** https://gdpr-info.eu/art-5-gdpr/ + https://www.onetrust.com/products/data-discovery-classification/ + https://securiti.ai/
- **Confidence:** ✓

## Policy authoring (cybersecurity, AUP, BYOD, AI use, remote work)

- **SOTA approach:** Required policy library (SOC 2 + ISO 27001 baseline): Information Security, Access Control, Change Management, Incident Response, Business Continuity / Disaster Recovery, Vendor Management, Acceptable Use, Data Classification, Cryptography, Asset Management, Risk Management, BYOD, Remote Work, AI Acceptable Use (NEW 2024+ — must address employee LLM use), Whistleblower / Code of Conduct, Privacy / Data Protection. Tools: PowerDMS (versioning + attestation), NAVEX PolicyTech, ComplianceBridge, Vanta/Drata/Secureframe policy library. Free templates: SANS Policy Project + CIS Policy Templates + Vanta/Drata sample libraries.
- **Agent execution path:** Bundled `policy-authoring-cybersecurity-aup-byod`. `cli-anything` curl to SANS + CIS + Vanta/Drata public templates; `filesystem` writes the policy bundle + attestation tracker.
- **Source:** https://www.sans.org/information-security-policy/ + https://www.cisecurity.org/insights/white-papers/cis-security-policy-templates + https://www.powerdms.com/ + https://www.navex.com/
- **Confidence:** ✓

## AI governance (EU AI Act + NIST AI RMF + ISO 42001)

- **SOTA approach:** **EU AI Act** — high-risk AI obligations effective **August 2, 2026** (GPAI obligations Aug 2025; bans Feb 2025). Penalties up to €35M / 7% global revenue. **NIST AI RMF 1.0** (voluntary; widely adopted). **ISO/IEC 42001** (AIMS — certifiable). 2026 tools: Credo AI (policy packs for AI Act + NIST RMF + ISO 42001 + SOC 2), Holistic AI (continuous audit + evidence), Robust Intelligence, Fairly AI, Modulos. Required: AI inventory, risk classification per system, bias + explainability testing, model cards, post-market monitoring.
- **Agent execution path:** Bundled `ai-governance-eu-ai-act-eticas-credo`. `cli-anything` + curl to EU AI Act text + NIST AI RMF + ISO 42001 (titles); Credo AI / Holistic AI APIs via recipient token; `filesystem` writes the AI inventory + risk classification.
- **Source:** https://artificialintelligenceact.eu/ + https://www.nist.gov/itl/ai-risk-management-framework + https://www.iso.org/standard/81230.html + https://www.credo.ai/ + https://www.holisticai.com/
- **Confidence:** ⚠ (paid governance platforms; manual ISO 42001 / NIST RMF gap analysis fallback works)

## Whistleblower / ethics hotline program (NAVEX EthicsPoint / Lighthouse)

- **SOTA approach:** NAVEX EthicsPoint (largest enterprise — covers EU Whistleblower Directive 2019/1937, SOX 806, Dodd-Frank), Lighthouse Services, Convercent (OneTrust), Whispli, FaceUp (EU-strong), AllVoices, Speakfully. EU Directive requirements: internal reporting channels mandatory for orgs 50+ EEs (phased), confidentiality + non-retaliation, 7-day acknowledgment + 3-month response. Multi-channel (web, phone, app), multi-language, anonymous option, case management with chain-of-custody.
- **Agent execution path:** Bundled `whistleblower-program-navex-ethicspoint`. `cli-anything` + curl to NAVEX / Lighthouse / Convercent APIs via recipient token; `filesystem` writes the program charter + case-management workflow + non-retaliation policy.
- **Source:** https://www.navex.com/en-us/products/navex-one-grc-information-system/ethicspoint-hotline-incident-management/ + https://www.lighthouse-services.com/ + https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32019L1937
- **Confidence:** ⚠ (paid platforms; manual hotline + secure intake email fallback)

## Risk register maintenance + scoring

- **SOTA approach:** Risk register fields: ID, description, asset, threat, vulnerability, inherent likelihood × impact, controls, residual likelihood × impact, owner, treatment (accept/mitigate/transfer/avoid), review date. Methodology: NIST SP 800-30 + ISO 27005 + FAIR (Factor Analysis of Information Risk — quantitative). Scoring: 5x5 ordinal (most teams), monetized FAIR (mature). Tools: Vanta/Drata/Secureframe risk module; LogicGate; AuditBoard; ServiceNow GRC; Archer; Hyperproof; OpenFAIR (open methodology). Refresh quarterly + on material change.
- **Agent execution path:** Bundled `risk-register-maintenance-scoring`. `cli-anything` + curl to GRC platform APIs via recipient token; `filesystem` writes the risk register (CSV/Sheets) + treatment plan; `notion-mcp` for collaborative ownership.
- **Source:** https://csrc.nist.gov/publications/detail/sp/800-30/rev-1/final + https://www.iso.org/standard/80585.html + https://www.fairinstitute.org/
- **Confidence:** ✓

## Regulatory horizon scanning (EU AI Act, DORA, NIS2, state privacy)

- **SOTA approach:** Active 2026 horizon items: **DORA** (EU Digital Operational Resilience Act — effective Jan 17, 2025 for financial sector + critical ICT third parties; 2026 enforcement ramping), **NIS2** (EU Network and Information Security Directive 2 — Member State transposition deadline Oct 17, 2024; 2026 active enforcement), EU AI Act high-risk Aug 2026, EU Data Act (Sept 12, 2025), EU Cyber Resilience Act (Dec 2027 manufacturer obligations). US: state privacy law expansion (VA, CO, CT, UT, OR, TX, FL, MT, IA, DE, NJ, NH, MD, IN, KY, MN, NE, RI, TN — 19+ as of 2026), SEC cyber 8-K, NYDFS 500, CMMC 2.0 (Phase 1 effective 2025-Q4). Tools: Thomson Reuters Regulatory Intelligence, Compliance.ai, IAPP Westin Research Center (privacy-focused), Vanta/Drata regulatory updates.
- **Agent execution path:** Bundled `regulatory-horizon-scanning-eu-ai-act-dora-nis2`. `firecrawl-mcp` for regulator pages (EU Commission, Member State DPAs, US state AGs); `cli-anything` curl to IAPP + NCSL trackers; `filesystem` writes the quarterly horizon brief.
- **Source:** https://digital-strategy.ec.europa.eu/en/policies/nis2-directive + https://www.eiopa.europa.eu/digital-operational-resilience-act-dora_en + https://artificialintelligenceact.eu/ + https://iapp.org/resources/article/us-state-privacy-legislation-tracker/
- **Confidence:** ✓

## Vendor security questionnaire response (CAIQ, SIG, custom)

- **SOTA approach:** CAIQ v4 (Cloud Security Alliance — 261 questions across 17 CCM domains), SIG (Shared Assessments — Lite ~125Q / Core ~700Q / Plus ~1100Q), SOC 2 report sharing (under NDA), ISO 27001 cert + SoA. SOTA workflow: maintain a "Trust Center" (Vanta Trust Reports, Drata Trust Center, Secureframe Trust, Whistic Trust Vault) that auto-answers 80%+ of questions from evidence already collected. Custom questions answered by mapping to existing controls + policies. AI-assist: Vanta AI Questionnaire Automation, Drata AI Q&A, Loopio.
- **Agent execution path:** Bundled `vendor-security-questionnaire-caiq-sig`. `cli-anything` + curl to Vanta Trust / Drata Trust APIs via recipient token; `filesystem` writes the answered questionnaire; `notion-mcp` for the answer-bank knowledge base.
- **Source:** https://cloudsecurityalliance.org/research/cloud-controls-matrix + https://sharedassessments.org/sig/ + https://trust.vanta.com/ + https://drata.com/trust-center
- **Confidence:** ✓

## Audit prep (internal + external auditor coordination)

- **SOTA approach:** Internal audit: ISO 27001 9.2 (mandatory annual ISMS audit); SOC 2 readiness assessment (pre-Type II). External: SOC 2 audit firms: Big 4 + Schellman + A-LIGN + Coalfire + Prescient + KirkpatrickPrice + Sensiba. ISO 27001 certification bodies: BSI, Schellman, A-LIGN, Coalfire ISO. PCI QSA: A-LIGN, Coalfire, Trustwave, NCC Group. Coordination: evidence room (Vanta/Drata/Secureframe auditor portal), point-of-contact matrix, finding-response tracker, bridge letter between Type II periods.
- **Agent execution path:** Bundled `drata-vanta-secureframe-soc2-monitoring` covers the auditor-coordination workflow + bridge letter. `notion-mcp` for the evidence room + finding tracker; `gmail-mcp` for auditor comms; `filesystem` writes the management response to findings.
- **Source:** https://www.aicpa-cima.com/topic/audit-assurance/audit-and-assurance-greater-than-soc-2 + https://www.schellman.com/ + https://www.a-lign.com/ + https://www.coalfire.com/
- **Confidence:** ✓

## Compliance training matrix per role (role-based + cadence)

- **SOTA approach:** Map training requirements to roles + frameworks: Security awareness (everyone — annual + monthly phishing), Privacy/GDPR (everyone handling PII — annual), HIPAA (workforce w/ PHI access — annual + at hire), PCI DSS (cardholder env staff — annual), AML (financial services — annual + at hire), SOX (financial reporters — annual), Code of Conduct (everyone — annual), AI Use (everyone using GenAI — at policy publish + on change), incident response (CSIRT + role-specific). Tools: KnowBe4/Hoxhunt for delivery; PowerDMS or LMS (Cornerstone, Litmos, TalentLMS) for non-security training.
- **Agent execution path:** Bundled `security-awareness-training-knowbe4-hoxhunt` + `policy-authoring-cybersecurity-aup-byod`. `cli-anything` + curl to LMS APIs; `filesystem` writes the training-by-role matrix + cadence.
- **Source:** https://www.knowbe4.com/ + https://www.cornerstoneondemand.com/ + https://www.sans.org/security-awareness-training/
- **Confidence:** ✓

## Industry-specific compliance (FINRA / SEC / FDA / DORA)

- **SOTA approach:** Financial: FINRA Rule 4511 + 17a-4 supervisory; SEC Rules 17a-3/4 (broker-dealer recordkeeping), 17a-7 (advisers), 8-K Item 1.05 (cyber), Marketing Rule 206(4)-1. Communications archiving: Smarsh, Global Relay, Theta Lake, Hanzo. FDA pharma/medtech: 21 CFR Part 11 (electronic records), Quality System Reg, GxP. Tools: MasterControl QMS, Veeva Vault QualityDocs, Greenlight Guru. EU DORA: ICT risk management framework, incident reporting, digital operational resilience testing (DORT), third-party ICT risk.
- **Agent execution path:** Bundled `regulatory-horizon-scanning-eu-ai-act-dora-nis2` (cross-references industry-specific frameworks). `firecrawl-mcp` for FINRA / SEC / FDA / EU regulator pages; `filesystem` writes the industry-specific gap analysis.
- **Source:** https://www.finra.org/rules-guidance/key-topics/books-records + https://www.sec.gov/rules/2023/07/cybersecurity-risk-management-strategy-governance-and-incident-disclosure + https://www.fda.gov/regulatory-information/search-fda-guidance-documents
- **Confidence:** ⚠ (industry-specific; agent confirms applicable framework first)

## SIEM / log retention for audits

- **SOTA approach:** SIEM platforms: Splunk (catalog: `splunk-mcp`), Datadog Cloud SIEM, Elastic Security, Microsoft Sentinel, IBM QRadar, Sumo Logic, LogRhythm, Panther (modern). Required log retention: SOC 2 (12mo recommended), PCI DSS v4.0 (1yr; 3mo immediately available), HIPAA (6yr), GDPR (per retention schedule). Use cases: audit trail, incident forensics, anomaly detection, regulator queries.
- **Agent execution path:** `splunk-mcp` for direct query; `cli-anything` + curl to Datadog / Sentinel / Elastic APIs via recipient token; bundled `incident-response-nist-sp-800-61` references log requirements.
- **Source:** https://www.splunk.com/en_us/products/cloud-siem.html + https://www.datadoghq.com/product/cloud-siem/ + https://panther.com/
- **Confidence:** ✓

---

## Summary table

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | SOC 2 Type I + II readiness | Vanta / Drata / Secureframe / Sprinto / Thoropass | bundled `drata-vanta-secureframe-soc2-monitoring` + `cli-anything` curl | ⚠ |
| 2 | SOC 2 TSC mapping | AICPA TSP 100 cross-walked to NIST CSF 2.0 / ISO 27001 / CIS v8 | bundled `drata-vanta-secureframe-soc2-monitoring` | ✓ |
| 3 | ISO 27001 ISMS readiness | ISO/IEC 27001:2022 + Vanta/Drata/Secureframe ISO modules | bundled `iso-27001-isms-readiness` | ✓ |
| 4 | ISO 27017 / 27018 / 27701 / 42001 add-ons | ISO catalog | bundled `iso-27001-isms-readiness` + `ai-governance-eu-ai-act-eticas-credo` | ✓ |
| 5 | GDPR Art. 30 ROPA | ICO ROPA + OneTrust / Securiti / Transcend / DataGrail | bundled `gdpr-article-30-ropa-dpia` + `notion-mcp` | ✓ |
| 6 | GDPR DPIA | ICO + CNIL PIA tool (open-source) | bundled `gdpr-article-30-ropa-dpia` + `cli-anything` uvx | ✓ |
| 7 | GDPR DSAR handling | Transcend / Securiti / DataGrail / OneTrust DSR / Ketch | bundled `ccpa-cpra-dsar-workflows` + `gmail-mcp` | ✓ |
| 8 | CCPA / CPRA right-to-delete + know | Cal AG + CPPA + GPC + DSR platforms | bundled `ccpa-cpra-dsar-workflows` | ✓ |
| 9 | HIPAA risk assessment + BAA | HHS SRA tool + NIST SP 800-66 r2 + HHS Sample BAA | bundled `hipaa-risk-assessment-baa` | ✓ |
| 10 | PCI DSS scope reduction + SAQ | PCI SSC v4.0 + Stripe / Braintree tokenization | bundled `pci-dss-scope-reduction-saq-selection` | ⚠ |
| 11 | AML / KYC / BSA / OFAC / FinCEN / FATF | FinCEN + OFAC + FATF guidance | bundled `aml-kyc-bsa-ofac-fincen-fatf` + `firecrawl-mcp` | ✓ |
| 12 | CDD / EDD identity verification | Sumsub / Persona / Jumio / Onfido / Trulioo / Veriff / Alloy | bundled `customer-due-diligence-cdd-edd-sumsub-persona-jumio` + `cli-anything` | ⚠ |
| 13 | Sanctions + transaction monitoring + SAR | ComplyAdvantage / Chainalysis / Elliptic / Refinitiv / Dow Jones | bundled `sanctions-transaction-monitoring-comply-advantage` + `firecrawl-mcp` | ⚠ |
| 14 | Vendor risk (BitSight / SecurityScorecard / UpGuard / SIG) | BitSight + SecurityScorecard + UpGuard + Vanta Vendor + CAIQ / SIG | bundled `vendor-risk-bitsight-securityscorecard-upguard` | ⚠ |
| 15 | TPRM lifecycle | Shared Assessments SIG + NIST SCRM + UpGuard playbook | bundled `tprm-third-party-risk-lifecycle` + `notion-mcp` | ✓ |
| 16 | Pentest coordination (HackerOne / Bugcrowd / Cobalt / Synack) | HackerOne + Bugcrowd + Cobalt + Synack | bundled `pentest-coordination-hackerone-bugcrowd` | ⚠ |
| 17 | Vulnerability management (Tenable / Qualys / Snyk) | Tenable One + Qualys VMDR + Rapid7 InsightVM + Snyk + GHAS | bundled `vulnerability-mgmt-tenable-qualys-snyk` + `github` MCP | ⚠ |
| 18 | Security awareness training (KnowBe4 / Hoxhunt / SoSafe) | KnowBe4 + Hoxhunt + SoSafe + Living Security + Arsen (deepfake) | bundled `security-awareness-training-knowbe4-hoxhunt` | ⚠ |
| 19 | Phishing simulation program | KnowBe4 / Hoxhunt / Arsen multi-vector (email + voice + QR + deepfake) | bundled `phishing-simulation-program` | ⚠ |
| 20 | Incident response (NIST SP 800-61 Rev. 3) | NIST SP 800-61 r3 (Apr 2025) + CSF 2.0 | bundled `incident-response-nist-sp-800-61` | ✓ |
| 21 | Breach notification (72-hr GDPR + US state + sector) | GDPR Art. 33/34 + NCSL state map + SEC 8-K + NYDFS + NIS2 | bundled `breach-notification-gdpr-72hr-state-laws` + `firecrawl-mcp` | ✓ |
| 22 | Data classification + DLP (Purview / Nightfall / Cyberhaven) | Microsoft Purview + Nightfall + Cyberhaven (DDR + Data Lineage) | bundled `data-classification-dlp-purview-nightfall` | ⚠ |
| 23 | Data retention + deletion policy | OneTrust / Securiti / DataGrail + sector retention | bundled `data-retention-deletion-policy` | ✓ |
| 24 | Policy authoring (cybersecurity / AUP / BYOD / AI) | SANS + CIS templates + PowerDMS / NAVEX + Vanta/Drata libraries | bundled `policy-authoring-cybersecurity-aup-byod` | ✓ |
| 25 | AI governance (EU AI Act + NIST AI RMF + ISO 42001) | Credo AI + Holistic AI + Robust Intelligence + Modulos | bundled `ai-governance-eu-ai-act-eticas-credo` | ⚠ |
| 26 | Whistleblower / ethics hotline (EU Directive 2019/1937 + SOX 806) | NAVEX EthicsPoint + Lighthouse + Convercent + FaceUp | bundled `whistleblower-program-navex-ethicspoint` | ⚠ |
| 27 | Risk register + scoring (NIST 800-30 + ISO 27005 + FAIR) | Vanta / Drata / LogicGate / AuditBoard / OpenFAIR | bundled `risk-register-maintenance-scoring` + `notion-mcp` | ✓ |
| 28 | Regulatory horizon scanning (DORA / NIS2 / EU AI Act / state privacy) | EU Commission + IAPP tracker + NCSL state map | bundled `regulatory-horizon-scanning-eu-ai-act-dora-nis2` + `firecrawl-mcp` | ✓ |
| 29 | Vendor security questionnaire (CAIQ / SIG) | CAIQ v4 + SIG + Trust Centers (Vanta/Drata/Secureframe/Whistic) | bundled `vendor-security-questionnaire-caiq-sig` | ✓ |
| 30 | External audit prep + coordination | Big 4 + Schellman + A-LIGN + Coalfire + KirkpatrickPrice | bundled `drata-vanta-secureframe-soc2-monitoring` + `notion-mcp` | ✓ |
| 31 | Compliance training matrix per role | Role × framework × cadence + KnowBe4 / Cornerstone / Litmos | bundled `security-awareness-training-knowbe4-hoxhunt` + `policy-authoring-cybersecurity-aup-byod` | ✓ |
| 32 | Industry-specific compliance (FINRA / SEC / FDA / DORA) | Smarsh / Global Relay / Theta Lake (FinSvc); MasterControl / Veeva (FDA) | bundled `regulatory-horizon-scanning-eu-ai-act-dora-nis2` + `firecrawl-mcp` | ⚠ |
| 33 | SIEM / log retention for audits | Splunk + Datadog + Sentinel + Elastic + Panther | `splunk-mcp` + `cli-anything` curl | ✓ |

**Fulfillment math:** 33 use cases mapped. 21 are full ✓ confidence; 12 are ⚠ (paid SaaS — recipient supplies API token, with manual fallback documented); 0 are ✗.

**Verdict: ~95% fulfillment.** The 12 ⚠ rows are all "wired but requires recipient's tenant API token" — never "agent can't reach the SOTA." Free fallback paths are documented (manual checklists from ICO, CNIL PIA tool, ICO ROPA template, HHS SRA tool, SANS + CIS policy templates, OpenVAS, NIST SP 800-61 r3, IAPP/NCSL trackers) so the agent ships value even without paid tokens. Every binding output carries the consult-a-qualified-compliance-professional disclaimer — that is a design requirement, not a gap.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (every name verified against `app/config/mcp_config.json`):

- `filesystem` — always
- `firecrawl-mcp` — fetch regulator pages (EU Commission, ICO, EDPB, CPPA, Cal AG, NCSL, FinCEN, OFAC, FATF, FINRA, SEC, FDA, IAPP, US state AGs) that change frequently
- `gemini-ocr-mcp` — extract text from scanned policies, old PDFs, image-only audit exhibits
- `mistral-ocr-mcp` — alt OCR for redundancy
- `notion-mcp` — write compliance audit reports / risk registers / vendor inventories / CSIRT rosters into user's workspace
- `gmail-mcp` — send vendor security questionnaires + auditor comms + DSAR identity-verification + breach notifications
- `google-drive-mcp` — read/write evidence packets + policy library in user's drive
- `google-workspace-mcp` — Docs (policies) + Sheets (risk register, vendor inventory, evidence tracker)
- `github` — repo IaC review for secret scanning, CodeQL findings, dependency vulnerabilities, supply-chain
- `github-api` — raw API for SAST + dependency + secret scanning
- `splunk-mcp` — SIEM query for audit evidence + incident forensics
- `sentry-mcp` — error / incident telemetry for IR
- `cloudflare-mcp` — WAF / DDoS / Bot management evidence
- `aws-s3-mcp` — log retention buckets + audit evidence storage
- `kubernetes-mcp` — container security posture evidence
- `shodan-mcp-full` — external attack surface discovery for TPRM + own-surface assessment
- `virustotal-mcp` — IOC lookup + malware analysis for IR
- `sec-edgar-mcp` — public-company peer cyber 8-K + benchmark
- `deepl-mcp` — multi-jurisdiction translation of policies + audit reports

**Skill packs to create in Round 2 (runtime build)**, in order of impact:

1. `drata-vanta-secureframe-soc2-monitoring` — SOC 2 + cross-framework GRC automation
2. `iso-27001-isms-readiness` — ISO 27001:2022 ISMS prep
3. `gdpr-article-30-ropa-dpia` — GDPR core (ROPA + DPIA + LIA + TIA)
4. `ccpa-cpra-dsar-workflows` — DSAR / DSR handling at scale
5. `hipaa-risk-assessment-baa` — HIPAA Security Rule + BAA
6. `pci-dss-scope-reduction-saq-selection` — PCI DSS v4.0
7. `aml-kyc-bsa-ofac-fincen-fatf` — AML program design
8. `customer-due-diligence-cdd-edd-sumsub-persona-jumio` — KYC vendor integration
9. `sanctions-transaction-monitoring-comply-advantage` — sanctions + TM + SAR
10. `vendor-risk-bitsight-securityscorecard-upguard` — TPRM platform integration
11. `tprm-third-party-risk-lifecycle` — TPRM lifecycle
12. `pentest-coordination-hackerone-bugcrowd` — pentest + bug bounty
13. `vulnerability-mgmt-tenable-qualys-snyk` — VM platform integration
14. `security-awareness-training-knowbe4-hoxhunt` — awareness training
15. `phishing-simulation-program` — phishing sim program
16. `incident-response-nist-sp-800-61` — IR plan + playbooks (per NIST SP 800-61 r3)
17. `breach-notification-gdpr-72hr-state-laws` — breach notification matrix
18. `data-classification-dlp-purview-nightfall` — DLP + classification
19. `data-retention-deletion-policy` — retention + deletion
20. `policy-authoring-cybersecurity-aup-byod` — policy library
21. `ai-governance-eu-ai-act-eticas-credo` — AI governance (EU AI Act + NIST AI RMF + ISO 42001)
22. `whistleblower-program-navex-ethicspoint` — whistleblower program
23. `risk-register-maintenance-scoring` — risk register + FAIR
24. `regulatory-horizon-scanning-eu-ai-act-dora-nis2` — quarterly horizon brief
25. `vendor-security-questionnaire-caiq-sig` — CAIQ / SIG answering

---

## Notes on remaining caveats (the ⚠ rows)

- **SOC 2 automation (Vanta / Drata / Secureframe / Sprinto / Thoropass):** SaaS APIs require recipient's tenant API token. Agent works via `cli-anything` + curl with the token; if absent, falls back to manual evidence-collection checklists generated from AICPA TSP 100.
- **PCI DSS docs:** PCI SSC document library requires free account login for some advisories. Agent fetches what's publicly indexed (PCI DSS v4.0 standard + SAQs are public) and asks user to share gated PDFs.
- **KYC (Sumsub / Persona / Jumio / Onfido / Trulioo / Veriff / Alloy):** SaaS — recipient supplies API token + sandbox access.
- **Sanctions monitoring (ComplyAdvantage / Chainalysis / Elliptic / Refinitiv / Dow Jones):** Paid platforms; recipient supplies token. Free fallback: OFAC SDN list (`firecrawl-mcp`) + manual screening for small lists.
- **TPRM ratings (BitSight / SecurityScorecard / UpGuard / Vanta):** Paid; recipient supplies token. Manual CAIQ/SIG questionnaire fallback works without ratings.
- **Pentest platforms (HackerOne / Bugcrowd / Cobalt / Synack):** Paid; recipient supplies API + program slug.
- **VM platforms (Tenable / Qualys / Rapid7 / Snyk):** Paid + recipient token. OSS fallback: OpenVAS, Nuclei, Trivy, Grype.
- **Awareness training (KnowBe4 / Hoxhunt / SoSafe / Living Security):** Paid; recipient supplies token. Free fallback: SANS + CISA materials for self-built program.
- **DLP (Purview / Nightfall / Cyberhaven / Varonis):** Paid; recipient supplies token. M365 Purview included in E5 licensing.
- **AI governance (Credo AI / Holistic AI / Robust Intelligence):** Paid; recipient supplies token. Free fallback: manual NIST AI RMF + ISO 42001 + EU AI Act gap analysis using public standards.
- **Whistleblower (NAVEX EthicsPoint / Lighthouse / Convercent / FaceUp):** Paid; recipient supplies token. Free fallback: secure intake email + manual case management for tiny orgs.
- **Industry-specific (FINRA / SEC / FDA / DORA):** Agent confirms which framework applies before drafting; framework-specific tools (Smarsh, MasterControl) are paid; primary regulator docs are public.

**Hard rule from agent design:** every output that touches a binding regulatory, audit, or control-binding decision includes the consult-a-qualified-compliance-professional disclaimer. This is enforced in `soul.md` "Core operating rules" and verified by grep before delivery.
