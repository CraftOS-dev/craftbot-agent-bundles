# Compliance Agent — Use Cases

**Tier:** general · **Category:** compliance
**Core job:** Senior compliance officer for solo founders, startups, and small-to-mid-market teams — SOC 2, ISO 27001, GDPR, CCPA, HIPAA, PCI DSS, AML/KYC, vendor risk + TPRM, vulnerability management, security awareness, incident response, breach notification, data classification + DLP, policy library authoring, AI governance (EU AI Act + NIST AI RMF + ISO 42001), whistleblower programs, risk registers, and regulatory horizon scanning. Always recommends a qualified compliance professional, licensed auditor, or privacy attorney for binding decisions.

> **Disclaimer (load-bearing):** This agent is NOT a substitute for a qualified compliance professional, licensed auditor, or privacy attorney. Every output that touches a binding regulatory, audit, or control-binding decision includes the consult-a-qualified-professional disclaimer. Use this agent to assess, plan, draft, and run programs; use qualified professionals for audit opinions, regulator-facing filings, binding control acceptance, and enforcement responses. DISTINCT from `legal-counsel` (binding contracts, IP, T&C) — `compliance-agent` handles ongoing GRC + privacy + security + risk programs.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Compliance framework readiness + audit prep

- SOC 2 Type I + II readiness (Vanta / Drata / Secureframe / Sprinto / Thoropass setup)
- SOC 2 Trust Services Criteria (TSC) mapping (CC1-CC9 + A + C + PI + P)
- ISO 27001 ISMS readiness (2022 update — 93 Annex A controls in 4 themes)
- ISO 27017 (cloud) / 27018 (PII processor) / 27701 (PIMS) / 42001 (AIMS) add-ons
- External audit prep + auditor coordination (Big 4 + Schellman + A-LIGN + Coalfire + KirkpatrickPrice)
- Internal audit testing (ISO 9.2; SOC 2 readiness)
- Compliance certification roadmap + sequencing (`compliance-cert-planner` default skill)

### Privacy programs (GDPR, CCPA, US state laws, sector laws)

- GDPR Article 30 ROPA (records of processing)
- GDPR DPIA (data protection impact assessment) — CNIL PIA tool execution
- GDPR DSAR (data subject access request) handling
- CCPA / CPRA right-to-delete + right-to-know + right-to-correct + right-to-limit workflow
- US state privacy law expansion mapping (19+ states as of 2026)
- LGPD / PIPEDA / PIPL / APPI / POPIA / APP mapping
- Cookie consent + IAB TCF v2.2 + Google Consent Mode v2
- International data transfers (SCC 2021/914 + TIA post-Schrems II)
- DPO designation + role
- Privacy by Design + Default

### HIPAA (healthcare)

- HIPAA risk assessment (45 CFR §164.308(a)(1)(ii)(A))
- HIPAA Security Rule administrative + physical + technical safeguards
- HIPAA Privacy Rule + Notice of Privacy Practices (NPP)
- Business Associate Agreement (BAA) management
- Sub-BA flow-down
- Breach notification (60 days individuals + 500+ media + HHS portal)
- HITECH + state law overlay (CMIA, NY SHIELD)

### PCI DSS (cardholder data)

- PCI DSS v4.0 scope reduction + tokenization
- Cardholder Data Environment (CDE) segmentation
- SAQ-A vs A-EP vs B vs B-IP vs C vs C-VT vs D selection
- ROC vs SAQ decision (Level 1 vs L2-L4)
- ASV scan + pen test scheduling (Req. 11.3 + 11.4)
- v4.0 future-dated requirements (effective March 2025; steady-state 2026)
- QSA selection + coordination

### AML / KYC / sanctions / financial crime

- AML program design (BSA / FinCEN / OFAC + EU 6AMLD/AMLR + UK MLR)
- Five BSA Pillars (CIP + CDD + EDD + TM + SAR)
- Customer due diligence (CDD / EDD) — Sumsub / Persona / Jumio / Onfido / Trulioo / Veriff / Alloy integration
- Sanctions screening (ComplyAdvantage / Refinitiv / Dow Jones / OFAC SDN)
- Transaction monitoring + SAR / CTR filing
- Crypto compliance (Chainalysis / Elliptic / TRM Labs + MiCA + FATF Travel Rule)
- BSA Officer designation
- Independent AML audit

### Vendor risk + third-party risk management (TPRM)

- Vendor inventory + tiering (data sensitivity × business criticality)
- Vendor risk assessment (BitSight / SecurityScorecard / UpGuard / Vanta Vendor)
- TPRM lifecycle (sourcing → DD → contracting → onboarding → monitoring → reassessment → offboarding)
- Vendor security questionnaire response (CAIQ v4 / SIG Lite/Core/Plus / custom)
- Trust Center maintenance (Vanta / Drata / Secureframe / Whistic / SafeBase)
- Continuous monitoring (rating drift + breach intel)
- DPA + BAA + SCC + security addendum review (hand off to `legal-counsel` for binding terms)

### Vulnerability management + offensive security

- Vulnerability management program (Tenable One / Qualys VMDR / Rapid7 InsightVM)
- Application security (Snyk / GitHub Advanced Security / Semgrep / Checkmarx / SonarQube)
- Cloud-native security (Wiz / Orca / Lacework CNAPP)
- OSS scanning (OpenVAS / Nuclei / Trivy / Grype / Syft SBOM)
- Penetration testing coordination (HackerOne / Bugcrowd / Cobalt / Synack / Intigriti / YesWeHack)
- Bug bounty program design (severity scale + SLA + reward schedule + scope)
- Red team exercise scoping
- Remediation SLA matrices (Critical 14d / High 30d / Medium 90d)
- KEV catalog + EPSS-aware prioritization
- Supply chain risk (`supply-chain-risk-auditor` default — OSS dep risk)

### Security awareness + phishing

- Security awareness training program (KnowBe4 / Hoxhunt / SoSafe / Living Security / Arsen)
- Phishing simulation (multi-vector: email + SMS + voice + QR + deepfake)
- Role-based training matrix
- Compliance training (HIPAA / PCI / SOX / AML / Code of Conduct)
- AI use training (NEW 2024+)
- Repeat-clicker intervention + just-in-time learning

### Incident response + breach notification

- Incident response plan (NIST SP 800-61 Rev. 3 — April 2025)
- IR playbooks per scenario (ransomware / BEC / data breach / ATO / insider / 3P / AI compromise)
- CSIRT roster + on-call rotation
- Tabletop exercise design + execution + debrief
- Post-incident review (PIR) template
- IR retainer evaluation (CrowdStrike / Mandiant / Stroz Friedberg / Kroll / Coveware)
- Breach coach + PR/comms agency identification
- Breach notification (72hr GDPR + 50-state US + SEC 8-K + NYDFS + NIS2 + HIPAA + sector)
- Phased / supplemental notification (GDPR Art. 33(4))
- Communication to affected individuals + regulators + media

### Data classification + DLP

- Sensitivity label taxonomy (Public / Internal / Confidential / Restricted)
- Data classification per source category (PII / PHI / CHD / source code / IP)
- DLP rule set design + tuning
- Endpoint + network + cloud + email DLP architecture (Purview / Nightfall / Cyberhaven DDR / Varonis)
- GenAI exfiltration controls (Cyberhaven Data Lineage)
- Insider risk monitoring

### Data retention + deletion

- Retention schedule (per-category × jurisdiction × purpose × legal hold)
- Sector retention (HIPAA 6yr / FINRA 17a-4 / SOX 5-7yr / PCI 1yr authorization)
- Deletion runbook + automation (platform purge APIs)
- Litigation hold management

### Policy library authoring

- Information Security Policy + variants per framework
- Access Control / Change Management / Incident Response / BC-DR / Vendor Management
- AUP (Acceptable Use Policy) + BYOD + Remote Work
- Data Classification + Cryptography + Asset Management + Risk Management
- Vulnerability Management + Logging + Privacy / Data Protection
- AI Acceptable Use Policy (NEW 2024+)
- Code of Conduct + Whistleblower / Non-Retaliation
- HIPAA Sanction Policy + Workforce Security Policy
- PCI-specific Sensitive Data Handling
- Policy attestation tracking (PowerDMS / NAVEX PolicyTech / Vanta / Drata)

### AI governance (EU AI Act + NIST AI RMF + ISO 42001)

- AI system inventory (including 3P SaaS embedded AI)
- EU AI Act risk classification (prohibited / high-risk / limited-risk / minimal-risk; GPAI)
- High-risk obligations (effective Aug 2, 2026)
- Model cards + data governance protocols
- Bias + fairness + explainability + robustness testing
- Adversarial / systemic-risk GPAI evaluation
- Post-market monitoring + serious-incident reporting
- ISO 42001 AIMS readiness
- NIST AI RMF cross-mapping
- Credo AI / Holistic AI / Robust Intelligence / Fairly AI / Modulos integration

### Whistleblower / ethics programs

- Internal reporting channel setup (web + phone + app + email + in-person)
- Multi-language + anonymous option
- 7-day acknowledgment + 3-month response (EU Directive)
- Investigation playbook + investigator independence
- Anti-retaliation policy + tracking
- Annual board-level metrics report
- NAVEX EthicsPoint / Lighthouse / Convercent / Whispli / FaceUp / AllVoices integration

### Risk management

- Risk register (NIST SP 800-30 + ISO 27005 + FAIR / OpenFAIR)
- Inherent vs residual risk scoring (5x5 ordinal or monetized FAIR)
- Treatment plans (accept / mitigate / transfer / avoid)
- Annual + quarterly + event-driven refresh
- Heat map visualization
- Board-level risk dashboard

### Regulatory horizon scanning

- EU AI Act (high-risk Aug 2, 2026)
- EU DORA (Jan 17, 2025; 2026 enforcement)
- EU NIS2 (transposition + 2026 enforcement)
- EU Data Act (Sept 12, 2025)
- EU MiCA (crypto enforcement)
- EU Cyber Resilience Act (Dec 2027 mfr)
- EU Whistleblower Directive
- UK DPDIB
- US state privacy expansion (19+ states by 2026)
- SEC cyber 8-K Item 1.05
- NYDFS 23 NYCRR 500
- CMMC 2.0 (2025-Q4 Phase 1)
- GLBA Safeguards Rule update
- Colorado AI Act
- Illinois BIPA litigation trends
- Brazil LGPD / China PIPL / Japan APPI / Australia Privacy Act reform

### Industry-specific overlays

- Financial services (FINRA 4511 / 17a-4 / SEC 8-K / Marketing Rule / GLBA / NYDFS / DORA)
- Healthcare (HIPAA + HITECH + 42 CFR Part 2 + ONC Cures Act)
- Pharma / medtech (21 CFR Part 11 + GxP + MDR + IVDR + QSR)
- Crypto (FinCEN + OFAC + SEC + CFTC + MiCA + FATF + MTL)
- DoD contractors (CMMC 2.0 + NIST 800-171 + DFARS)
- EU operational resilience (DORA + NIS2)
- Children's data (COPPA + Age-Appropriate Design)

### SIEM + log retention (audit support)

- SIEM query for audit evidence (Splunk / Datadog / Sentinel / Elastic / Panther)
- Log retention per framework (SOC 2 / PCI / HIPAA / GDPR)
- Incident forensics
- Anomaly detection rules
- Regulator query response

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case from the section above appears here as a row.

| Use case | SOTA mechanism | Path |
|---|---|---|
| SOC 2 Type I + II readiness | Vanta / Drata / Secureframe / Sprinto / Thoropass | `drata-vanta-secureframe-soc2-monitoring` + `cli-anything` curl |
| SOC 2 TSC mapping | AICPA TSP 100 cross-walked to NIST CSF 2.0 / ISO 27001 / CIS v8 | `drata-vanta-secureframe-soc2-monitoring` |
| ISO 27001 ISMS readiness | ISO/IEC 27001:2022 + Vanta/Drata/Secureframe ISO modules | `iso-27001-isms-readiness` |
| ISO 27017 / 27018 / 27701 / 42001 add-ons | ISO catalog + Vanta/Drata multi-framework | `iso-27001-isms-readiness` + `ai-governance-eu-ai-act-eticas-credo` |
| External audit prep + auditor coordination | Big 4 + Schellman + A-LIGN + Coalfire + KirkpatrickPrice + Sensiba | `drata-vanta-secureframe-soc2-monitoring` + `notion-mcp` |
| Internal audit testing | ISO 9.2 + SOC 2 readiness | `drata-vanta-secureframe-soc2-monitoring` + `iso-27001-isms-readiness` |
| Compliance certification roadmap | Applicability + shared controls + sequencing | `compliance-cert-planner` (default) + `drata-vanta-secureframe-soc2-monitoring` |
| GDPR Art. 30 ROPA | ICO ROPA + OneTrust / Securiti / Transcend / DataGrail | `gdpr-article-30-ropa-dpia` + `notion-mcp` |
| GDPR DPIA | ICO + CNIL PIA tool (open-source) | `gdpr-article-30-ropa-dpia` + `cli-anything` uvx |
| GDPR DSAR handling | Transcend / Securiti / DataGrail / OneTrust DSR / Ketch | `ccpa-cpra-dsar-workflows` + `gmail-mcp` |
| CCPA / CPRA right-to-delete + know | Cal AG + CPPA + GPC + DSR platforms | `ccpa-cpra-dsar-workflows` |
| US state privacy law mapping | IAPP US State Privacy Tracker + state AGs | `regulatory-horizon-scanning-eu-ai-act-dora-nis2` + `firecrawl-mcp` |
| International transfer mechanisms | SCC 2021/914 + TIA + adequacy decisions | `gdpr-article-30-ropa-dpia` + `firecrawl-mcp` |
| Cookie consent | OneTrust / Cookiebot / TrustArc / Iubenda / Termly / Osano | hand off to `legal-counsel` for binding privacy policy text; agent provides compliance content |
| HIPAA risk assessment + BAA | HHS SRA tool + NIST SP 800-66 r2 + HHS Sample BAA | `hipaa-risk-assessment-baa` |
| HIPAA Security Rule (admin / physical / technical) | 45 CFR §§164.308-312 | `hipaa-risk-assessment-baa` |
| Breach notification (HIPAA + GDPR + state + sector) | NCSL state map + GDPR Art. 33/34 + HHS portal + SEC 8-K | `breach-notification-gdpr-72hr-state-laws` + `firecrawl-mcp` |
| PCI DSS scope reduction + SAQ | PCI SSC v4.0 + Stripe / Braintree tokenization | `pci-dss-scope-reduction-saq-selection` |
| QSA selection + coordination | A-LIGN / Coalfire / Trustwave / Sysnet / Schellman | `pci-dss-scope-reduction-saq-selection` + `gmail-mcp` |
| AML / KYC / BSA / OFAC / FinCEN / FATF | FinCEN + OFAC + FATF + EU AMLR/AMLD6 + UK MLR | `aml-kyc-bsa-ofac-fincen-fatf` + `firecrawl-mcp` |
| CDD / EDD identity verification | Sumsub / Persona / Jumio / Onfido / Trulioo / Veriff / Alloy | `customer-due-diligence-cdd-edd-sumsub-persona-jumio` |
| Sanctions + transaction monitoring + SAR | ComplyAdvantage / Chainalysis / Elliptic / Refinitiv / Dow Jones | `sanctions-transaction-monitoring-comply-advantage` |
| Crypto compliance (MiCA + FATF Travel Rule) | Chainalysis / Elliptic / TRM Labs + Sumsub crypto | `sanctions-transaction-monitoring-comply-advantage` + `customer-due-diligence-cdd-edd-sumsub-persona-jumio` |
| Vendor inventory + tiering | M365 + Google Workspace + AP + SaaS access reviews | `tprm-third-party-risk-lifecycle` + `notion-mcp` |
| Vendor risk ratings | BitSight (Forrester 2026 Leader) / SecurityScorecard / UpGuard / Vanta Vendor | `vendor-risk-bitsight-securityscorecard-upguard` |
| TPRM lifecycle | Shared Assessments SIG + NIST SCRM + UpGuard | `tprm-third-party-risk-lifecycle` |
| Vendor security questionnaire (CAIQ / SIG) | CAIQ v4 + SIG Lite/Core/Plus + Trust Centers | `vendor-security-questionnaire-caiq-sig` |
| Trust Center maintenance | Vanta Trust / Drata Trust / Secureframe Trust / Whistic Vault / SafeBase | `vendor-security-questionnaire-caiq-sig` |
| Vulnerability management (infra + cloud) | Tenable One + Qualys VMDR + Rapid7 InsightVM + Wiz / Orca | `vulnerability-mgmt-tenable-qualys-snyk` |
| Application security | Snyk + GitHub Advanced Security + Semgrep + Checkmarx | `vulnerability-mgmt-tenable-qualys-snyk` + `github` MCP |
| OSS supply chain risk | OpenVAS + Nuclei + Trivy + Grype + Syft SBOM + supply-chain-risk-auditor | `supply-chain-risk-auditor` (default) + `vulnerability-mgmt-tenable-qualys-snyk` + `github` MCP |
| Pentest coordination | HackerOne + Bugcrowd + Cobalt + Synack + Intigriti + YesWeHack | `pentest-coordination-hackerone-bugcrowd` |
| Bug bounty program design | HackerOne / Bugcrowd + severity + reward + scope | `pentest-coordination-hackerone-bugcrowd` |
| Security awareness training | KnowBe4 + Hoxhunt + SoSafe + Living Security | `security-awareness-training-knowbe4-hoxhunt` |
| Phishing simulation (multi-vector) | KnowBe4 / Hoxhunt / Arsen (email + voice + QR + deepfake) | `phishing-simulation-program` |
| Role-based training matrix | KnowBe4 / Hoxhunt + Cornerstone / Litmos for compliance LMS | `security-awareness-training-knowbe4-hoxhunt` + `policy-authoring-cybersecurity-aup-byod` |
| Incident response (NIST SP 800-61 r3) | NIST SP 800-61 r3 (Apr 2025) + CSF 2.0 | `incident-response-nist-sp-800-61` + `splunk-mcp` + `sentry-mcp` |
| IR retainer evaluation | CrowdStrike + Mandiant + Stroz Friedberg + Kroll + Coveware | `incident-response-nist-sp-800-61` |
| Tabletop exercise | Scenario rotation (ransomware / BEC / 3P / AI / insider) | `incident-response-nist-sp-800-61` |
| Data classification + DLP | Microsoft Purview + Nightfall + Cyberhaven (DDR + Data Lineage) | `data-classification-dlp-purview-nightfall` |
| GenAI exfiltration controls | Cyberhaven Data Lineage + Nightfall AI + Purview | `data-classification-dlp-purview-nightfall` |
| Data retention + deletion policy | OneTrust / Securiti / DataGrail + sector retention | `data-retention-deletion-policy` |
| Policy library authoring | SANS + CIS templates + PowerDMS / NAVEX + Vanta/Drata libraries | `policy-authoring-cybersecurity-aup-byod` |
| AI governance (EU AI Act + NIST AI RMF + ISO 42001) | Credo AI + Holistic AI + Robust Intelligence + Modulos | `ai-governance-eu-ai-act-eticas-credo` |
| AI inventory + risk classification | Per EU AI Act Annex III + GPAI separately | `ai-governance-eu-ai-act-eticas-credo` |
| Whistleblower program (EU Directive 2019/1937 + SOX 806) | NAVEX EthicsPoint + Lighthouse + Convercent + FaceUp | `whistleblower-program-navex-ethicspoint` |
| Risk register + scoring (NIST 800-30 + ISO 27005 + FAIR) | Vanta / Drata / LogicGate / AuditBoard / OpenFAIR | `risk-register-maintenance-scoring` + `notion-mcp` |
| Regulatory horizon scanning (DORA / NIS2 / EU AI Act / state privacy) | EU Commission + IAPP tracker + NCSL state map + reg pages | `regulatory-horizon-scanning-eu-ai-act-dora-nis2` + `firecrawl-mcp` |
| Industry-specific (FINRA / SEC / FDA / DORA) | Smarsh / Global Relay / Theta Lake (FinSvc); MasterControl / Veeva (FDA) | `regulatory-horizon-scanning-eu-ai-act-dora-nis2` + `firecrawl-mcp` |
| SIEM / log retention for audits | Splunk + Datadog + Sentinel + Elastic + Panther | `splunk-mcp` + `cli-anything` curl |
| Translate policies / audit reports | DeepL multi-jurisdiction | `deepl-mcp` |
| Scanned policy / evidence intake | Gemini OCR + Mistral OCR | `gemini-ocr-mcp` + `mistral-ocr-mcp` |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| SOC 2 automation (Vanta / Drata / Secureframe / Sprinto / Thoropass) | ⚠ | SaaS APIs require recipient's tenant API token; fallback = manual evidence-collection checklists |
| PCI DSS docs | ⚠ | PCI SSC requires free account login for some advisories; agent fetches publicly indexed + asks user to share gated PDFs |
| KYC vendors (Sumsub / Persona / Jumio / Onfido / Trulioo / Veriff / Alloy) | ⚠ | SaaS APIs require recipient's token + sandbox access |
| Sanctions monitoring (ComplyAdvantage / Chainalysis / Refinitiv / Dow Jones) | ⚠ | Paid platforms; recipient supplies token; OFAC SDN free fallback |
| TPRM ratings (BitSight / SecurityScorecard / UpGuard) | ⚠ | Paid; recipient supplies token; manual CAIQ/SIG fallback works without ratings |
| Pentest platforms (HackerOne / Bugcrowd / Cobalt / Synack) | ⚠ | Paid; recipient supplies API + program slug |
| Vulnerability management (Tenable / Qualys / Rapid7 / Snyk) | ⚠ | Paid + recipient token; OSS fallback: OpenVAS, Nuclei, Trivy, Grype |
| Awareness training (KnowBe4 / Hoxhunt / SoSafe / Living Security / Arsen) | ⚠ | Paid; recipient supplies token; SANS + CISA free fallback |
| DLP platforms (Purview / Nightfall / Cyberhaven / Varonis) | ⚠ | Paid; recipient supplies token; M365 Purview included in E5 |
| AI governance platforms (Credo AI / Holistic AI / Robust Intelligence / Modulos) | ⚠ | Paid; recipient supplies token; manual NIST AI RMF + ISO 42001 + EU AI Act gap analysis fallback |
| Whistleblower platforms (NAVEX / Lighthouse / Convercent / Whispli / FaceUp) | ⚠ | Paid; recipient supplies token; secure intake email + manual case management for tiny orgs |
| Industry-specific (FINRA / SEC / FDA / DORA tools) | ⚠ | Agent confirms applicable framework first; framework-specific paid tools optional; primary regulator docs are public |
| Binding audit opinion / regulator filing / professional engagement | ✗ (by design) | Agent does NOT execute audit opinion sign-off, regulator filings, or formal regulatory examination response — that's qualified-professional work |
| Binding legal contract review (DPA / BAA / SCC / MSA) | ✗ (by design) | Hand off to `legal-counsel` (sibling agent) — agent provides compliance content, not binding contract negotiation |
| Technical control implementation in code / IaC | ✗ (by design) | Hand off to `devops-engineer` — agent specs controls, devops implements |
| Litigation strategy / settlement / regulatory examination strategy | ✗ (by design) | Out of scope; recommend licensed attorney / breach coach |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a SOTA execution path. The 12 ⚠ rows are all SaaS-API-key dependencies with documented free fallbacks (free regulator tools + open-source compliance tooling — ICO ROPA template, CNIL PIA tool, HHS SRA tool, OFAC SDN list, SANS + CIS policy templates, NIST SP 800-61 r3, IAPP tracker, NCSL state map, OSS scanners). The 4 ✗ rows are intentional scope limits aligned with the consult-a-qualified-professional design rule + sibling-agent hand-offs.

---

## When to use this agent

- "We're prepping for SOC 2 Type II — what's the gap from our current AWS + Vanta-free setup?"
- "Audit our GDPR readiness — we serve EU + US customers, use Stripe, Mixpanel, Mailgun, Intercom, OpenAI"
- "Set up our HIPAA program — we're a digital-health SaaS handling PHI for clinical-trial sites"
- "PCI DSS scope question — we use Stripe Checkout iframe + a custom internal admin tool that briefly handles last-4 — what SAQ?"
- "Build our AML program — crypto-exchange in DE serving EU + US"
- "Tier our vendors + set up TPRM lifecycle — we have ~40 SaaS vendors"
- "Coordinate annual pen test — we want HackerOne for app + Cobalt for API"
- "Roll out security awareness — 200 EE, mixed remote, Hoxhunt vs KnowBe4?"
- "Draft IR plan + playbooks per NIST SP 800-61 r3 + run a tabletop next month"
- "We have a possible breach — affected EU + CA users — what filings + clocks?"
- "Set up DLP — M365 shop, worried about GenAI exfiltration"
- "Write our full policy library — SOC 2 minimum 14, plus AI Acceptable Use"
- "EU AI Act readiness — we use OpenAI + Claude embeddings in our SaaS — high-risk?"
- "Set up whistleblower hotline — DE entity, 80 EE — EU Directive obligations?"
- "Build our risk register — we're at the 'spreadsheet sprawl' stage"
- "Quarterly regulatory horizon brief — EU + US FinSvc"
- "Answer this 400-question SIG from our biggest enterprise customer"
- "Plan our multi-framework cert roadmap: SOC 2 → ISO 27001 → ISO 27701 over 18 months"
- "Audit our open-source supply chain for risky deps"

---

## When NOT to use this agent

- **Binding audit opinion sign-off / formal regulator examination response** — hand off to licensed auditor / qualified compliance professional / privacy attorney; this agent does not represent you to auditors or regulators
- **Binding legal contracts (DPA / BAA / SCC / MSA / privacy policy text execution)** — hand off to `legal-counsel` (sibling agent)
- **Technical control implementation in code / infrastructure** — hand off to `devops-engineer`; agent specs controls, devops implements them
- **Customer-facing incident comms drafting** — hand off to `customer-support-agent`; agent provides legal/compliance content
- **Board-level governance committee minutes + risk reporting** — hand off to `ceo-agent` (when built); return for compliance content
- **Vendor commercial mgmt + procurement negotiation** — hand off to `operations-agent` (when built); return for vendor risk scoring
- **Budget + ROI on compliance investment** — hand off to `finance-controller`; return for cost-of-control input
- **Marketing copy / sales content** — out of scope; recommend `marketing-agent`
- **Litigation, criminal exposure, court appearances** — out of scope; trial counsel only
- **Tax outcomes** — frame the regulatory mechanics; CPA / tax attorney confirms tax outcomes
- **Anything requiring attorney-client privilege** — privilege does not attach to AI conversations; consult a licensed attorney directly
- **Pure information security architecture (zero trust design, micro-segmentation, EDR rollout)** — agent provides compliance requirements; hand off to security architect / `devops-engineer` for implementation choice

---

## Disclaimer (load-bearing)

Every binding-decision output from this agent includes the consult-a-qualified-compliance-professional disclaimer. This is not optional language — it is the agent's hard rule, enforced in `soul.md` "Core operating rules" and verified by grep before delivery. The agent is NOT the final compliance professional, licensed auditor, or privacy attorney.
