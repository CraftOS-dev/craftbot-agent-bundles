# compliance-agent — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`).

For future tightening, pull 4-6 reference agents from `wshobson/agents`, `VoltAgent/awesome-claude-code-subagents`, `msitarzewski/agency-agents`, `vijaythecoder/awesome-claude-agents` into `reference/agents/`, and 6-10 reference skills into `reference/skills/`. Candidate agents to mirror once available:

- Security / compliance auditor (SOC 2, ISO 27001, GDPR, CCPA, HIPAA, PCI)
- Privacy engineer / DPO assistant
- AML / KYC / sanctions screening
- Vendor / third-party risk management (TPRM)
- Vulnerability management + pentest coordination
- Security awareness / phishing simulation

## Sources considered but not downloaded

- **Anthropic skills repo** — no published `compliance` skills as of June 2026.
- **wshobson plugins** — `compliance-and-governance` plugin exists but was not downloaded; queued for v1 refresh.
- **VoltAgent categories** — `08-finance-and-legal` and `09-security` house adjacent agents; queued for v1 refresh.
- **msitarzewski agency-agents** — `compliance-officer` and `security-auditor` queued for v1 refresh.

## SOTA tooling sources

Primary research lanes for the agent's day-to-day stack (each cited per use case in `SOTA_USE_CASES.md`):

1. **GRC / multi-framework compliance automation** — Vanta (~35% market share, broadest), Drata (~25%, auditor-favorite), Secureframe (~15%, advisory-heavy), Sprinto (~10%, mid-market international), Thoropass (~8%, bundles audit services), Hyperproof, AuditBoard, Tugboat Logic (Onspring), Anecdotes, Strike Graph, LogicGate, ServiceNow GRC, Archer (RSA), MetricStream, Workiva, Trustero.
2. **GDPR / CCPA / multi-jurisdiction privacy** — OneTrust (enterprise default), TrustArc, Securiti.ai (discovery+classification), Transcend (DSR-first, encrypted), DataGrail (2000+ integrations), Ketch (API-driven consent), BigID, MineOS, Iubenda, Termly, Osano, Cookiebot.
3. **HIPAA** — Drata HIPAA, Vanta HIPAA, Compliancy Group, Accountable HQ, Aptible (HITRUST), MedStack.
4. **PCI DSS** — A-LIGN, Secureframe PCI, Drata PCI, Trustwave, Sysnet (Forter), ControlScan, plus PCI SSC document library.
5. **AML / KYC / sanctions** — Sumsub (broadest, 14k+ document types), Persona (customizable), Jumio (enterprise ID-doc), Onfido, Trulioo, Veriff, Alloy, ComplyAdvantage (real-time AI screening), Chainalysis + Elliptic + TRM Labs (crypto), Refinitiv World-Check, Dow Jones Watchlist, LexisNexis Risk Solutions, Acuant.
6. **Vendor risk / TPRM** — BitSight (Forrester 2026 Leader, highest score), SecurityScorecard (outside-in ratings), UpGuard (combines TPRM+ASM), Vanta Vendor Risk, OneTrust TPRM, ProcessUnity, Whistic, RiskRecon, Black Kite, Aravo, Prevalent.
7. **Vulnerability management** — Tenable One (Nessus heritage), Qualys VMDR (TruRisk + native patch), Rapid7 InsightVM (Real Risk Score), Snyk (app-sec + IaC), Wiz / Orca (CNAPP), GitHub Advanced Security, OpenVAS (OSS), Microsoft Defender VM, Nucleus Security, Vulcan Cyber.
8. **Pentest / bug bounty** — HackerOne, Bugcrowd, Cobalt, Synack, Intigriti, YesWeHack.
9. **Security awareness training** — KnowBe4 (largest library), Hoxhunt (behavioral/adaptive), SoSafe (EU/NIS2/GDPR strong), Living Security (board-level HRM), Curricula (Huntress), Proofpoint, NINJIO, MetaCompliance, Infosec IQ, Arsen.
10. **DLP / data classification** — Microsoft Purview (M365-native), Nightfall (API-first SaaS), Cyberhaven (Data Lineage / DDR — 2026 unified platform), Varonis, Forcepoint, Symantec DLP, Digital Guardian.
11. **SIEM / log aggregation (for audits)** — Splunk (catalog: `splunk-mcp`), Datadog Cloud SIEM, Elastic Security, Microsoft Sentinel, IBM QRadar, Sumo Logic, LogRhythm, Panther.
12. **AI governance** — Credo AI (policy packs for EU AI Act, NIST AI RMF, ISO 42001, SOC 2), Holistic AI (continuous audit trails), Robust Intelligence, Fairly AI, Modulos, Surecloud.
13. **Whistleblower / ethics** — NAVEX EthicsPoint, Lighthouse Services, Convercent (OneTrust), Whispli, FaceUp, AllVoices.
14. **Policy management** — PowerDMS, NAVEX, ComplianceBridge.
15. **Industry-specific** — FINRA/SEC: Smarsh, Global Relay; FDA pharma/medtech: MasterControl, Veeva Vault; DORA (EU financial resilience) trackers.
16. **Regulator / standard primary sources** — AICPA TSP 100 (SOC 2), ISO/IEC 27001:2022 / 27017 / 27018 / 27701 / 42001, NIST CSF 2.0 + SP 800-61 Rev. 3 (April 2025) + SP 800-53, PCI SSC v4.0, ICO + EDPB + CPPA + Cal AG, HHS + OCR HIPAA, EU Commission (SCCs, AI Act, DSA/DMA, DORA, NIS2), FinCEN + OFAC + FATF.

Each tool used as a SOTA mechanism in this agent has a canonical URL recorded in `SOURCES.md` "SOTA tool sources (June 2026)" and in the per-use-case rows of `SOTA_USE_CASES.md`.
