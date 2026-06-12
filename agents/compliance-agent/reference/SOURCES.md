# Compliance Agent — Source Attribution

This file maps every section of `soul.md` and `role.md` back to the research source(s) it was derived from. It is part of the bundle but is **not** loaded into the agent's context — it exists for human verification and future updates.

Upstream reference agents have not been downloaded in v1 (see `reference/INVENTORY.md`). Provenance is the SOTA web research summarized in `reference/SOTA_USE_CASES.md`. The "Notes on authored-from-synthesis" section below flags the small portions composed locally as operational glue.

---

## soul.md → source map

| Section in soul.md | Source(s) |
|---|---|
| Title + opening identity + three load-bearing convictions | Authored from synthesis of the agent's per-agent prompt + `agent_bundle/METHODOLOGY.md` (load-bearing convictions pattern); convictions sourced from compliance practitioner consensus (AICPA TSP 100 implementation guides + ISO 27001 lead-implementer materials + IAPP frameworks) |
| Purpose | Authored from synthesis informed by per-agent prompt's "one-line role" + Vanta/Drata/Secureframe/OneTrust public marketing of scope + `reference/SOTA_USE_CASES.md` |
| Execution stack | `reference/SOTA_USE_CASES.md` (per-use-case skill-pack mapping) |
| When invoked — Readiness assessment mode | `reference/SOTA_USE_CASES.md` § "SOC 2 Type I + II readiness" + "ISO 27001 ISMS readiness" + "HIPAA risk assessment" + "PCI DSS scope" + "GDPR readiness audit" + "CCPA / CPRA readiness audit" |
| When invoked — Privacy program mode | `reference/SOTA_USE_CASES.md` § "GDPR Art. 30 ROPA" + "GDPR DPIA" + "GDPR DSAR handling" + "CCPA / CPRA right-to-delete + right-to-know" |
| When invoked — AML/KYC program mode | `reference/SOTA_USE_CASES.md` § "AML / KYC / BSA / OFAC / FinCEN / FATF program" + "Customer due diligence (CDD / EDD)" + "Sanctions screening + transaction monitoring + SARs" |
| When invoked — Vendor risk / TPRM mode | `reference/SOTA_USE_CASES.md` § "Vendor risk assessment" + "TPRM lifecycle" + "Vendor security questionnaire response" |
| When invoked — Incident response / breach mode | `reference/SOTA_USE_CASES.md` § "Incident response plan (NIST SP 800-61 Rev. 3)" + "Breach notification (72-hour GDPR + US state laws + sector laws)" + NIST SP 800-61 r3 (April 2025) + CSF 2.0 |
| When invoked — AI governance mode | `reference/SOTA_USE_CASES.md` § "AI governance (EU AI Act + NIST AI RMF + ISO 42001)" + EU AI Act Regulation 2024/1689 + NIST AI RMF 1.0 + ISO/IEC 42001:2023 |
| When invoked — Policy authoring mode | `reference/SOTA_USE_CASES.md` § "Policy authoring (cybersecurity, AUP, BYOD, AI use, remote work)" + SANS + CIS templates |
| When invoked — Regulatory horizon mode | `reference/SOTA_USE_CASES.md` § "Regulatory horizon scanning" + EU Commission + IAPP + NCSL trackers |
| Core operating rules (~18 bullets) | Synthesis from the per-agent prompt's "CRITICAL DISCLAIMER" + AICPA Code of Professional Conduct framing (for what the AI is NOT replacing — independent auditor) + ABA Model Rules 5.5 (UPL) + ICO/EDPB enforcement-driven best practices |
| Mode-specific decisions | `reference/SOTA_USE_CASES.md` per-use-case rows + Vanta + Drata + Secureframe public best-practice content + framework primary sources (TSP 100 / ISO 27001 / GDPR / CCPA / HIPAA / PCI DSS / NIST publications) |
| Quality gates | Authored from synthesis of the CRITICAL DISCLAIMER + AICPA Code framing + framework completeness checklists (TSP 100 / Annex A / Security Rule / PCI / Art. 30) |
| Output format | Authored from synthesis informed by docx / pdf / xlsx / markdown-converter skill defaults + standard auditor + regulator deliverable conventions |
| Communication style | Authored from synthesis aligned with the load-bearing conviction "documentation is half the audit" + risk-based prioritization principle |
| When to push back | Synthesis from AICPA Code (independence + objectivity) + audit evidence integrity practice + ABA Model Rules 5.5 (UPL) |
| When to defer (sibling agents) | Per-agent prompt's defer rules + CraftBot agent catalog (legal-counsel, devops-engineer, customer-support-agent, ceo-agent (future), operations-agent (future), finance-controller, marketing-agent) |
| On first conversation (PROACTIVE init) | `METHODOLOGY.md` standard footer; the 3 routine questions tailored from the per-agent prompt |
| Closing rule | Authored from synthesis restating the three convictions |

---

## role.md → source map

| Section in role.md | Source(s) |
|---|---|
| Capability reference → Frameworks in scope | Aggregated from AICPA TSP 100 + ISO catalog (27001 / 27017 / 27018 / 27701 / 42001) + NIST publications (CSF 2.0 / SP 800-53 r5 / SP 800-171 / SP 800-30 r1 / SP 800-61 r3 / SP 800-66 r2 / AI RMF 1.0) + GDPR / UK GDPR / CCPA / CPRA + 19+ US state privacy statutes + LGPD / PIPEDA / PIPL / APPI / POPIA / APP + HIPAA (45 CFR Parts 160/162/164) + HITECH + PCI DSS v4.0 / v4.0.1 + BSA + FinCEN + OFAC + PATRIOT Act + AML Act 2020 + FATF Recommendations + EU AML (6AMLD/AMLR/AMLD6/AMLA/MiCA) + UK MLR 2017 + EU AI Act (Regulation 2024/1689) + EU NIS2 + EU DORA + EU DSA/DMA + EU Data Act + EU CRA + SEC Rule 33-11216 + NYDFS 23 NYCRR 500 + CMMC 2.0 + SOX + COPPA + FERPA + GLBA + TCPA + CAN-SPAM + CASL + ePrivacy Directive + FTC §5 |
| Capability reference → Industry-specific overlays | FINRA (Rule 4511 + 17a-4) + SEC (17a-3/4 + Marketing Rule + 8-K + Reg S-P) + GLBA Safeguards + NYDFS + HIPAA + HITECH + 42 CFR Part 2 + ONC Cures Act + FDA (21 CFR Part 11 + GxP + MDR + IVDR) + EU MiCA + FATF Travel Rule + CMMC 2.0 + NIST 800-171 + DFARS + EU DORA + EU NIS2 + COPPA + Age-Appropriate Design |
| Capability reference → SOTA platforms in scope | Aggregated from web research summarized in `reference/SOTA_USE_CASES.md` + Cavanex / Strac / SecureLeap / ComplyJet / TheNextWeb / Vanta resource comparisons for 2026 GRC market share; Vanta/Drata blog comparisons; UpGuard / Hoxhunt / RansomLeak / Brightside competitive analyses for awareness training; Cyberhaven / Underdefense / Currentware for DLP; Valtik / Underdefense / GuptaDeepak for vulnerability mgmt |
| Framework cross-walk table | Synthesis from AICPA TSP 100 + ISO 27001:2022 Annex A + 45 CFR §§164.308-312 + PCI DSS v4.0 + NIST CSF 2.0 — control-by-control cross-walk built from each framework's published mapping + Vanta/Drata/Secureframe published cross-framework mappings |
| SOC 2 readiness playbook | Synthesis from AICPA TSP 100 + Vanta + Drata + Secureframe public readiness materials + auditor practice notes (Schellman + A-LIGN + Coalfire blogs) + 2026 market share comparisons (Cavanex / Strac / SecureLeap) |
| ISO 27001 readiness playbook | ISO/IEC 27001:2022 standard text + ISO/IEC 27002:2022 + ISO/IEC 27005:2022 + BSI / Schellman / A-LIGN / LRQA practice notes |
| GDPR readiness checklist | GDPR text (Art. 2-3, 6, 9-10, 13-23, 25, 28, 30, 32-35, 37, 44-49) + ICO guidance + EDPB guidelines + post-Schrems II Transfer Impact Assessment guidance + CNIL PIA tool documentation |
| CCPA readiness checklist | Cal. Civ. Code §§1798.100-1798.199 + CPRA additions + CPPA regulations + Cal AG enforcement focus areas + IAPP US state privacy tracker (19+ state expansion) |
| HIPAA readiness checklist | 45 CFR Parts 160 / 162 / 164 + Subpart D (Breach Notification) + NIST SP 800-66 Rev. 2 (2024) + HHS HealthIT SRA Tool documentation + HHS Sample BAA Provisions + HITECH text + state law (CMIA, NY SHIELD) |
| PCI DSS readiness checklist | PCI DSS v4.0 + v4.0.1 standard text + SAQ documentation + PCI SSC Self-Assessment Questionnaire instructions + Stripe / Braintree / Adyen tokenization guidance + 2026 QSA practice notes (A-LIGN / Coalfire / Trustwave) |
| AML KYC program playbook | BSA + FinCEN Customer Due Diligence final rule (2018) + FinCEN guidance + OFAC sanctions framework + PATRIOT Act + AML Act 2020 + FATF Recommendations + EU 6AMLD + EU AMLR + EU MiCA + UK MLR 2017 + FCA AML handbook + Sumsub / Persona / Jumio / ComplyAdvantage / Chainalysis public documentation |
| Vendor risk playbook | Shared Assessments SIG framework + Cloud Security Alliance CAIQ v4 + CCM + NIST SCRM + UpGuard / BitSight / SecurityScorecard public methodology + Vanta vendor risk documentation + Forrester Wave Cybersecurity Risk Rating Platforms Q2 2026 |
| TPRM lifecycle playbook | Synthesis from Shared Assessments + NIST SCRM + UpGuard playbook + practitioner consensus on lifecycle stages |
| Pentest coordination playbook | CVSS 4.0 documentation (FIRST.org) + HackerOne / Bugcrowd / Cobalt / Synack / Intigriti public program design materials + SOC 2 CC4.1 + ISO 27001 A.8.29 + PCI DSS Req. 11.4 + NYDFS Part 500 |
| Vulnerability management playbook | Tenable / Qualys / Rapid7 / Snyk / GitHub Advanced Security public documentation + CISA KEV catalog + EPSS (FIRST.org) + CVSS 4.0 + 2026 buyer guides (Valtik Studios / Underdefense / Gupta Deepak / Luniq) + OWASP + PCI DSS Req. 6.3.1 remediation timelines |
| Security awareness playbook | KnowBe4 + Hoxhunt + SoSafe + Living Security + Arsen + Proofpoint + NINJIO + MetaCompliance public methodology + 2026 buyer guides (Brightside AI / RansomLeak / Adaptive Security) |
| Phishing simulation playbook | KnowBe4 + Hoxhunt + Arsen public methodology + 2026 multi-vector (email + voice + QR + deepfake) research |
| Incident response playbook | NIST SP 800-61 Rev. 3 (April 2025) + NIST CSF 2.0 + practitioner consensus on playbooks-per-scenario + IR retainer firm practice notes (CrowdStrike + Mandiant + Stroz + Kroll + Coveware) |
| Breach notification matrix | GDPR Art. 33 + 34 + UK GDPR + CCPA §1798.82 + NCSL 50-state breach notification tracker + 45 CFR §§164.400-414 (HIPAA Subpart D) + SEC Rule 33-11216 + NYDFS 23 NYCRR 500.17 + EU NIS2 + EU DORA + GLBA Safeguards (2024 update) + FERPA |
| DLP classification playbook | NIST SP 800-60 + ISO 27001 A.5.12/13 + practitioner consensus on 4-tier label taxonomy + Microsoft Purview / Nightfall / Cyberhaven / Varonis public documentation + 2026 GenAI exfiltration research (Cyberhaven / Currentware / Underdefense) |
| Policy library reference | SOC 2 minimum policies (Vanta / Drata sample library) + ISO 27001 minimum policies + HIPAA Security Rule documentation requirements (§§164.316) + PCI DSS Req. 12 documentation + SANS Information Security Policy Project + CIS Security Policy Templates |
| AI governance playbook | EU AI Act (Regulation 2024/1689) full text + Annex III + NIST AI RMF 1.0 + ISO/IEC 42001:2023 + Credo AI + Holistic AI + Robust Intelligence + Modulos / Surecloud public guidance |
| EU AI Act risk classification | EU AI Act text (Titles II-IV + Annex III) + Article 50 (transparency for limited-risk) + GPAI requirements (Art. 51-55) + penalty schedule (Art. 99) |
| Whistleblower program playbook | EU Whistleblower Directive 2019/1937 full text + SOX §806 + Dodd-Frank §922 + OSHA whistleblower statutes + NAVEX EthicsPoint / Lighthouse / Convercent / Whispli / FaceUp / AllVoices public methodology |
| Risk register reference | NIST SP 800-30 Rev. 1 + ISO/IEC 27005:2022 + FAIR Institute (OpenFAIR) + COSO ERM + Octave Allegro (CMU SEI) + Vanta / Drata risk module documentation |
| Regulatory horizon table | EU AI Act + EU DORA + EU NIS2 + EU Data Act + EU MiCA + EU CRA + EU Whistleblower Directive + UK GDPR + DPDIB + CCPA + 19+ US state privacy laws + SEC Cyber 8-K + NYDFS + CMMC 2.0 + FedRAMP + GLBA + HIPAA NPRMs + Colorado AI Act + NYC AI Bias Audit + Illinois BIPA + Brazil LGPD + Australia Privacy Act + China PIPL + Japan APPI + FATF Travel Rule |
| Vendor security questionnaire playbook | Cloud Security Alliance CAIQ v4 + Shared Assessments SIG (Lite/Core/Plus) + Trust Center patterns (Vanta / Drata / Secureframe / Whistic / SafeBase) + AI questionnaire automation (Vanta + Drata + Loopio + Responsive) |
| Antipattern catalog | Composition synthesis informed by common compliance mistakes documented in: AICPA / ISACA practice notes (SOC 2 / ISO 27001) + ICO + EDPB enforcement actions (GDPR) + Cal AG / CPPA enforcement (CCPA) + HHS OCR enforcement (HIPAA) + PCI SSC + FinCEN / OFAC enforcement (AML) + KnowBe4 / Hoxhunt program design + EU AI Act guidance + practitioner consensus on each antipattern. Each antipattern's underlying statute / standard is cited inline. |
| Disclaimer templates | Composed to be deployable; aligned with the load-bearing CRITICAL DISCLAIMER + AICPA Code of Professional Conduct framing + ABA Model Rules 5.5 (UPL) |
| SOTA tool reference (June 2026) | `reference/SOTA_USE_CASES.md` + per-tool source URLs (cited in the SOTA sources table below) |
| SOTA execution playbook | `reference/SOTA_USE_CASES.md` summary table |
| Closing rules | Authored from synthesis restating soul.md convictions |

---

## Notes on authored-from-synthesis

Sections composed as operational glue rather than lifted verbatim:

- **Three load-bearing convictions (soul.md)** — composed from compliance practitioner consensus across AICPA + ISACA + IAPP + ICO + EDPB materials; each conviction underpinned by published guidance.
- **Core operating rules (soul.md)** — ~18 bullets composed locally from the CRITICAL DISCLAIMER + AICPA Code of Professional Conduct (independence/objectivity framing for what the AI is NOT replacing) + ABA Model Rules + practical compliance-agent operational rules. None of these are domain claims that lack underlying support.
- **When to push back / When to defer (soul.md)** — operational glue. Domain claims (UPL, professional independence, scope of representation, framework conflicts) come from AICPA + ABA Model Rules; the framing is composed for agent-specific behavior.
- **Antipattern catalog (role.md)** — composition synthesis from common compliance mistakes documented in regulator enforcement actions + practitioner advisory commentary. Each antipattern's underlying statute / standard / regulator guidance is cited inline.
- **Disclaimer templates (role.md)** — composed to be deployable; aligned with the load-bearing CRITICAL DISCLAIMER + AICPA Code framing + ABA Model Rules 5.5 (UPL).
- **First-conversation routine questions (soul.md)** — adapted from the standard PROACTIVE.md self-init pattern in `METHODOLOGY.md`. The 3 role-specific questions are tailored to compliance workflows (active frameworks + jurisdictions + active audit / deadlines).
- **Framework cross-walk table (role.md)** — built control-by-control from each framework's published mapping; this is a synthesis (no single published source has the complete cross-walk in the agent's specific format), but every individual row is verifiable in the cited primary source.

These are operational glue, not domain claims. They do not introduce knowledge claims that lack a source.

---

## How to update this agent

If you want to refresh content from upstream:

1. Re-fetch the SOTA sources listed in the table below — many of these (Vanta + Drata + Secureframe + ICO + EDPB + CPPA + HHS + PCI SSC + FinCEN + OFAC + FATF + EU Commission + NIST + AICPA + IAPP + NCSL + Forrester Wave) update quarterly or on major regulatory event.
2. Diff against the previous versions to see what changed.
3. Update the corresponding sections of `soul.md`, `role.md`, and `reference/SOTA_USE_CASES.md`.
4. Update this `SOURCES.md` if section names or source URLs changed.
5. Re-run `python verify.py compliance-agent` to confirm structure intact.
6. Re-run `python build.py compliance-agent` to regenerate `dist/compliance-agent.craftbot`.

The bundled skill packs (in `skills/`) are created in Round 2; their SKILL.md files cite tool-specific sources independently.

---

## SOTA tool sources (June 2026)

| Tool / framework | Source URL | Used in |
|---|---|---|
| AICPA — SOC 2 TSP 100 | https://us.aicpa.org/interestareas/frc/assuranceadvisoryservices/sorhome | `skills/drata-vanta-secureframe-soc2-monitoring` + cross-walk table |
| ISO/IEC 27001:2022 | https://www.iso.org/standard/27001 | `skills/iso-27001-isms-readiness` + cross-walk table |
| ISO/IEC 27017:2015 | https://www.iso.org/standard/43757.html | `skills/iso-27001-isms-readiness` |
| ISO/IEC 27018:2019 | https://www.iso.org/standard/76559.html | `skills/iso-27001-isms-readiness` |
| ISO/IEC 27701:2019 | https://www.iso.org/standard/71670.html | `skills/iso-27001-isms-readiness` + `skills/gdpr-article-30-ropa-dpia` |
| ISO/IEC 42001:2023 | https://www.iso.org/standard/81230.html | `skills/ai-governance-eu-ai-act-eticas-credo` |
| ISO/IEC 27005:2022 | https://www.iso.org/standard/80585.html | `skills/risk-register-maintenance-scoring` |
| NIST CSF 2.0 | https://www.nist.gov/cyberframework | All cross-walk + `skills/incident-response-nist-sp-800-61` |
| NIST SP 800-30 Rev. 1 | https://csrc.nist.gov/publications/detail/sp/800-30/rev-1/final | `skills/risk-register-maintenance-scoring` |
| NIST SP 800-53 Rev. 5 | https://csrc.nist.gov/pubs/sp/800/53/r5/final | Federal control catalog reference |
| NIST SP 800-61 Rev. 3 (April 2025) | https://csrc.nist.gov/pubs/sp/800/61/r3/final | `skills/incident-response-nist-sp-800-61` |
| NIST SP 800-66 Rev. 2 (2024) | https://csrc.nist.gov/pubs/sp/800/66/r2/final | `skills/hipaa-risk-assessment-baa` |
| NIST SP 800-171 | https://csrc.nist.gov/pubs/sp/800/171/r3/final | CMMC 2.0 reference |
| NIST AI RMF 1.0 | https://www.nist.gov/itl/ai-risk-management-framework | `skills/ai-governance-eu-ai-act-eticas-credo` |
| Vanta — SOC 2 / ISO / HIPAA / GDPR / PCI / Vendor | https://www.vanta.com/ | `skills/drata-vanta-secureframe-soc2-monitoring` + Vendor Risk skill + Trust Center pattern |
| Drata — Continuous Compliance | https://drata.com/ | `skills/drata-vanta-secureframe-soc2-monitoring` |
| Secureframe — SOC 2 / ISO / PCI / HIPAA | https://secureframe.com/ | `skills/drata-vanta-secureframe-soc2-monitoring` |
| Sprinto — Mid-market SOC 2 / ISO | https://sprinto.com/ | `skills/drata-vanta-secureframe-soc2-monitoring` |
| Thoropass (formerly Laika) | https://thoropass.com/ | `skills/drata-vanta-secureframe-soc2-monitoring` |
| Cavanex — Vanta vs Drata vs Secureframe vs Sprinto 2026 | https://cavanex.com/blog/soc-2-compliance-platforms-compared-2026 | Market share + positioning context |
| Vanta — Best TPRM 2026 | https://www.vanta.com/resources/best-tprm-software-in-2026-the-shift-to-continuous-monitoring | `skills/vendor-risk-bitsight-securityscorecard-upguard` |
| GDPR (EU 2016/679) | https://gdpr-info.eu/ | `skills/gdpr-article-30-ropa-dpia` + `skills/ccpa-cpra-dsar-workflows` + `skills/breach-notification-gdpr-72hr-state-laws` |
| ICO — UK GDPR Guidance | https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/ | `skills/gdpr-article-30-ropa-dpia` |
| EDPB — European Data Protection Board | https://edpb.europa.eu/ | `skills/gdpr-article-30-ropa-dpia` |
| CNIL PIA Tool (open-source) | https://www.cnil.fr/en/open-source-pia-software-helps-carry-out-data-protection-impact-assesment | `skills/gdpr-article-30-ropa-dpia` |
| EU SCC 2021/914 | https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en | `skills/gdpr-article-30-ropa-dpia` |
| California AG — CCPA | https://oag.ca.gov/privacy/ccpa | `skills/ccpa-cpra-dsar-workflows` |
| California Privacy Protection Agency (CPPA) | https://cppa.ca.gov/ | `skills/ccpa-cpra-dsar-workflows` |
| Transcend — DSR (encrypted) | https://www.transcend.io/ | `skills/ccpa-cpra-dsar-workflows` |
| Securiti.ai | https://securiti.ai/ | `skills/ccpa-cpra-dsar-workflows` + `skills/gdpr-article-30-ropa-dpia` |
| DataGrail | https://www.datagrail.io/ | `skills/ccpa-cpra-dsar-workflows` |
| OneTrust | https://www.onetrust.com/ | `skills/ccpa-cpra-dsar-workflows` + `skills/gdpr-article-30-ropa-dpia` + `skills/tprm-third-party-risk-lifecycle` |
| Ketch | https://www.ketch.com/ | `skills/ccpa-cpra-dsar-workflows` |
| BigID / MineOS / Osano / Iubenda / Termly / Cookiebot / TrustArc | https://bigid.com/ + https://www.mineos.ai/ + https://www.osano.com/ + https://www.iubenda.com/ + https://termly.io/ + https://www.cookiebot.com/ + https://trustarc.com/ | `skills/ccpa-cpra-dsar-workflows` (alternatives) |
| Ketch — Best Privacy 2026 | https://www.ketch.com/blog/posts/best-data-privacy-software | Privacy platform comparison context |
| HHS — HIPAA Security Rule Guidance + Sample BAA | https://www.hhs.gov/hipaa/for-professionals/security/guidance/index.html | `skills/hipaa-risk-assessment-baa` |
| HHS HealthIT — SRA Tool | https://www.healthit.gov/topic/privacy-security-and-hipaa/security-risk-assessment-tool | `skills/hipaa-risk-assessment-baa` |
| HHS Sample BAA Provisions | https://www.hhs.gov/hipaa/for-professionals/covered-entities/sample-business-associate-agreement-provisions/ | `skills/hipaa-risk-assessment-baa` |
| Drata / Vanta / Compliancy Group / Accountable HQ / Aptible / MedStack | https://drata.com/hipaa + https://www.vanta.com/products/hipaa + https://compliancy-group.com/ + https://www.accountablehq.com/ + https://www.aptible.com/ + https://medstack.co/ | `skills/hipaa-risk-assessment-baa` |
| PCI SSC — Document Library | https://www.pcisecuritystandards.org/document_library/ | `skills/pci-dss-scope-reduction-saq-selection` |
| Stripe — PCI Compliance Guide | https://stripe.com/guides/pci-compliance | `skills/pci-dss-scope-reduction-saq-selection` |
| Braintree | https://www.braintreepayments.com/features/data-security | `skills/pci-dss-scope-reduction-saq-selection` |
| FinCEN — BSA Resources | https://www.fincen.gov/resources/financial-institutions/bank-secrecy-act-resources | `skills/aml-kyc-bsa-ofac-fincen-fatf` |
| OFAC — Sanctions + SDN List | https://ofac.treasury.gov/ | `skills/aml-kyc-bsa-ofac-fincen-fatf` + `skills/sanctions-transaction-monitoring-comply-advantage` |
| FATF — Recommendations | https://www.fatf-gafi.org/en/topics/Fatf-recommendations.html | `skills/aml-kyc-bsa-ofac-fincen-fatf` |
| Sumsub — KYC / KYB / AML | https://sumsub.com/ | `skills/customer-due-diligence-cdd-edd-sumsub-persona-jumio` |
| Persona | https://withpersona.com/ | `skills/customer-due-diligence-cdd-edd-sumsub-persona-jumio` |
| Jumio | https://www.jumio.com/ | `skills/customer-due-diligence-cdd-edd-sumsub-persona-jumio` |
| Onfido / Trulioo / Veriff / Alloy | https://onfido.com/ + https://www.trulioo.com/ + https://www.veriff.com/ + https://www.alloy.com/ | `skills/customer-due-diligence-cdd-edd-sumsub-persona-jumio` |
| ComplyAdvantage | https://complyadvantage.com/ | `skills/sanctions-transaction-monitoring-comply-advantage` |
| Chainalysis | https://www.chainalysis.com/ | `skills/sanctions-transaction-monitoring-comply-advantage` |
| Elliptic / TRM Labs / Solidus Labs | https://www.elliptic.co/ + https://www.trmlabs.com/ + https://www.soliduslabs.com/ | `skills/sanctions-transaction-monitoring-comply-advantage` |
| Refinitiv World-Check | https://www.refinitiv.com/en/products/world-check-kyc-screening | `skills/sanctions-transaction-monitoring-comply-advantage` |
| Dow Jones / LexisNexis / Acuant / Sanction Scanner | https://professional.dowjones.com/risk/products/risk-and-compliance/ + https://risk.lexisnexis.com/products/bridger-xg + https://www.acuant.com/ + https://www.sanctionscanner.com/ | `skills/sanctions-transaction-monitoring-comply-advantage` |
| Quantexa — Best KYC 2026 | https://www.quantexa.com/resources/best-kyc-software-and-tools/ | KYC tools comparison context |
| BitSight | https://www.bitsight.com/ | `skills/vendor-risk-bitsight-securityscorecard-upguard` |
| Forrester Wave 2026 — Cybersecurity Risk Rating Platforms Q2 2026 | https://www.bitsight.com/news/bitsight-named-leader-2026-forrester-wave-cybersecurity-risk-rating-platforms | `skills/vendor-risk-bitsight-securityscorecard-upguard` |
| SecurityScorecard | https://securityscorecard.com/ | `skills/vendor-risk-bitsight-securityscorecard-upguard` |
| UpGuard | https://www.upguard.com/ | `skills/vendor-risk-bitsight-securityscorecard-upguard` |
| Vanta Vendor Risk | https://www.vanta.com/products/third-party-risk-management | `skills/vendor-risk-bitsight-securityscorecard-upguard` |
| Whistic / SafeBase / RiskRecon / Black Kite / ProcessUnity / Prevalent / Aravo | https://www.whistic.com/ + https://safebase.io/ + https://www.riskrecon.com/ + https://blackkite.com/ + https://www.processunity.com/ + https://www.prevalent.net/ + https://www.aravo.com/ | `skills/vendor-risk-bitsight-securityscorecard-upguard` (alternatives) |
| Shared Assessments SIG | https://sharedassessments.org/sig/ | `skills/vendor-security-questionnaire-caiq-sig` + `skills/tprm-third-party-risk-lifecycle` |
| Cloud Security Alliance — CAIQ v4 + CCM | https://cloudsecurityalliance.org/research/cloud-controls-matrix | `skills/vendor-security-questionnaire-caiq-sig` |
| HackerOne | https://www.hackerone.com/ | `skills/pentest-coordination-hackerone-bugcrowd` |
| Bugcrowd | https://www.bugcrowd.com/ | `skills/pentest-coordination-hackerone-bugcrowd` |
| Cobalt | https://www.cobalt.io/ | `skills/pentest-coordination-hackerone-bugcrowd` |
| Synack / Intigriti / YesWeHack | https://www.synack.com/ + https://www.intigriti.com/ + https://www.yeswehack.com/ | `skills/pentest-coordination-hackerone-bugcrowd` |
| CVSS 4.0 | https://www.first.org/cvss/v4-0/ | `skills/pentest-coordination-hackerone-bugcrowd` + `skills/vulnerability-mgmt-tenable-qualys-snyk` |
| Tenable One | https://www.tenable.com/ | `skills/vulnerability-mgmt-tenable-qualys-snyk` |
| Qualys VMDR | https://www.qualys.com/apps/vulnerability-management-detection-response/ | `skills/vulnerability-mgmt-tenable-qualys-snyk` |
| Rapid7 InsightVM | https://www.rapid7.com/products/insightvm/ | `skills/vulnerability-mgmt-tenable-qualys-snyk` |
| Snyk | https://snyk.io/ | `skills/vulnerability-mgmt-tenable-qualys-snyk` |
| GitHub Advanced Security | https://github.com/security | `skills/vulnerability-mgmt-tenable-qualys-snyk` + `github` MCP |
| Wiz / Orca / Lacework / Microsoft Defender VM | https://www.wiz.io/ + https://orca.security/ + https://www.lacework.com/ + https://www.microsoft.com/en-us/security/business/threat-protection/microsoft-defender-vulnerability-management | `skills/vulnerability-mgmt-tenable-qualys-snyk` (alternatives) |
| OpenVAS / Nuclei / Trivy / Grype / Syft | https://www.openvas.org/ + https://github.com/projectdiscovery/nuclei + https://github.com/aquasecurity/trivy + https://github.com/anchore/grype + https://github.com/anchore/syft | OSS scanners |
| Valtik Studios — VM Buyer Guide 2026 | https://www.valtikstudios.com/blog/vulnerability-management-buyer-guide-2026 | VM tool comparison context |
| CISA KEV Catalog | https://www.cisa.gov/known-exploited-vulnerabilities-catalog | `skills/vulnerability-mgmt-tenable-qualys-snyk` (prioritization) |
| EPSS (FIRST.org) | https://www.first.org/epss/ | `skills/vulnerability-mgmt-tenable-qualys-snyk` |
| KnowBe4 | https://www.knowbe4.com/ | `skills/security-awareness-training-knowbe4-hoxhunt` + `skills/phishing-simulation-program` |
| Hoxhunt | https://hoxhunt.com/ | `skills/security-awareness-training-knowbe4-hoxhunt` + `skills/phishing-simulation-program` |
| SoSafe | https://sosafe-awareness.com/ | `skills/security-awareness-training-knowbe4-hoxhunt` |
| Living Security | https://www.livingsecurity.com/ | `skills/security-awareness-training-knowbe4-hoxhunt` |
| Arsen — AI deepfake phishing | https://www.arsen.co/ | `skills/phishing-simulation-program` |
| Curricula (Huntress) / NINJIO / MetaCompliance / Infosec IQ / Proofpoint | https://www.huntress.com/ + https://ninjio.com/ + https://www.metacompliance.com/ + https://www.infosecinstitute.com/iq/ + https://www.proofpoint.com/ | `skills/security-awareness-training-knowbe4-hoxhunt` (alternatives) |
| Brightside AI — Security Awareness 2026 | https://www.brside.com/blog/best-security-awareness-training-platforms-for-2026 | Comparison context |
| Hoxhunt — KnowBe4 Competitors 2026 | https://hoxhunt.com/blog/knowbe4-competitors | Comparison context |
| NCSL — US State Breach Notification Laws | https://www.ncsl.org/technology-and-communication/security-breach-notification-laws | `skills/breach-notification-gdpr-72hr-state-laws` |
| SEC — Cyber 8-K Item 1.05 | https://www.sec.gov/rules/final/2023/33-11216.pdf | `skills/breach-notification-gdpr-72hr-state-laws` |
| NYDFS 23 NYCRR 500 | https://www.dfs.ny.gov/industry_guidance/cybersecurity | `skills/breach-notification-gdpr-72hr-state-laws` |
| EU NIS2 Directive | https://digital-strategy.ec.europa.eu/en/policies/nis2-directive | `skills/regulatory-horizon-scanning-eu-ai-act-dora-nis2` + `skills/breach-notification-gdpr-72hr-state-laws` |
| EU DORA | https://www.eiopa.europa.eu/digital-operational-resilience-act-dora_en | `skills/regulatory-horizon-scanning-eu-ai-act-dora-nis2` + `skills/breach-notification-gdpr-72hr-state-laws` |
| Microsoft Purview | https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp | `skills/data-classification-dlp-purview-nightfall` |
| Nightfall AI | https://www.nightfall.ai/ | `skills/data-classification-dlp-purview-nightfall` |
| Cyberhaven | https://www.cyberhaven.com/ | `skills/data-classification-dlp-purview-nightfall` |
| Cyberhaven — Top DLP Solutions 2026 | https://www.cyberhaven.com/blog/top-dlp-solutions | DLP comparison context |
| Varonis / Forcepoint / Symantec DLP / Digital Guardian | https://www.varonis.com/ + https://www.forcepoint.com/ + https://www.broadcom.com/products/cybersecurity/information-protection/dlp + https://www.digitalguardian.com/ | `skills/data-classification-dlp-purview-nightfall` (alternatives) |
| SANS — Information Security Policy Project | https://www.sans.org/information-security-policy/ | `skills/policy-authoring-cybersecurity-aup-byod` |
| CIS — Security Policy Templates | https://www.cisecurity.org/insights/white-papers/cis-security-policy-templates | `skills/policy-authoring-cybersecurity-aup-byod` |
| PowerDMS | https://www.powerdms.com/ | `skills/policy-authoring-cybersecurity-aup-byod` |
| NAVEX PolicyTech / ComplianceBridge | https://www.navex.com/ + https://www.compliancebridge.com/ | `skills/policy-authoring-cybersecurity-aup-byod` |
| EU AI Act (Regulation 2024/1689) | https://artificialintelligenceact.eu/ | `skills/ai-governance-eu-ai-act-eticas-credo` |
| Credo AI | https://www.credo.ai/ | `skills/ai-governance-eu-ai-act-eticas-credo` |
| Holistic AI | https://www.holisticai.com/ | `skills/ai-governance-eu-ai-act-eticas-credo` |
| Robust Intelligence / Fairly AI / Modulos | https://www.robustintelligence.com/ + https://fairly.ai/ + https://www.modulos.ai/ | `skills/ai-governance-eu-ai-act-eticas-credo` (alternatives) |
| PredictionGuard — EU AI Act Tools 2026 | https://predictionguard.com/blog/best-eu-ai-act-compliance-tools-for-enterprise-ai-programs-in-2026 | EU AI Act tools comparison context |
| Glocert — EU AI Act + ISO 42001 mapping | https://www.glocertinternational.com/resources/guides/eu-ai-act-mapping-iso-42001/ | EU AI Act + ISO 42001 cross-walk context |
| EU Whistleblower Directive 2019/1937 | https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32019L1937 | `skills/whistleblower-program-navex-ethicspoint` |
| NAVEX EthicsPoint | https://www.navex.com/en-us/products/navex-one-grc-information-system/ethicspoint-hotline-incident-management/ | `skills/whistleblower-program-navex-ethicspoint` |
| Lighthouse Services / Convercent / Whispli / FaceUp / AllVoices / Speakfully | https://www.lighthouse-services.com/ + https://www.convercent.com/ + https://whispli.com/ + https://www.faceup.com/ + https://www.allvoices.co/ + https://www.speakfully.com/ | `skills/whistleblower-program-navex-ethicspoint` (alternatives) |
| FAIR Institute | https://www.fairinstitute.org/ | `skills/risk-register-maintenance-scoring` |
| IAPP — US State Privacy Tracker | https://iapp.org/resources/article/us-state-privacy-legislation-tracker/ | `skills/regulatory-horizon-scanning-eu-ai-act-dora-nis2` |
| FINRA — Books and Records | https://www.finra.org/rules-guidance/key-topics/books-records | Industry-specific (FinSvc) |
| FDA — Guidance Documents | https://www.fda.gov/regulatory-information/search-fda-guidance-documents | Industry-specific (FDA pharma/medtech) |
| Smarsh / Global Relay / Theta Lake / Hanzo | https://www.smarsh.com/ + https://www.globalrelay.com/ + https://thetalake.com/ + https://www.hanzo.co/ | Industry-specific (FinSvc communications archiving) |
| MasterControl / Veeva Vault / Greenlight Guru / Qualio | https://www.mastercontrol.com/ + https://www.veeva.com/ + https://www.greenlight.guru/ + https://www.qualio.com/ | Industry-specific (FDA QMS) |
| Splunk Cloud SIEM | https://www.splunk.com/en_us/products/cloud-siem.html | `splunk-mcp` + `skills/incident-response-nist-sp-800-61` |
| Datadog Cloud SIEM / Microsoft Sentinel / Elastic Security / Panther / Sumo Logic / IBM QRadar / LogRhythm | https://www.datadoghq.com/product/cloud-siem/ + https://learn.microsoft.com/en-us/azure/sentinel/ + https://www.elastic.co/security + https://panther.com/ + https://www.sumologic.com/ + https://www.ibm.com/products/qradar-siem + https://logrhythm.com/ | `skills/incident-response-nist-sp-800-61` (SIEM alternatives) |
| CrowdStrike / Mandiant / Stroz Friedberg / Kroll / Coveware / Booz Allen | https://www.crowdstrike.com/ + https://www.mandiant.com/ + https://www.kroll.com/ + https://www.coveware.com/ + https://www.boozallen.com/ | `skills/incident-response-nist-sp-800-61` (IR retainer firms) |

---

These sources informed the `SOTA tool reference (June 2026)` section in `role.md`, the per-use-case mapping in `reference/SOTA_USE_CASES.md`, and the bundled SOTA skill packs (Round 2 creates the SKILL.md content).
