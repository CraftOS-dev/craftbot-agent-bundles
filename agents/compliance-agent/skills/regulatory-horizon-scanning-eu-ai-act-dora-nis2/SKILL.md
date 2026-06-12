---
name: regulatory-horizon-scanning-eu-ai-act-dora-nis2
description: Quarterly regulatory horizon brief — DORA (effective Jan 17, 2025; 2026 enforcement ramping), NIS2 (transposition Oct 17, 2024; 2026 active enforcement), EU AI Act (bans Feb 2025; GPAI Aug 2025; high-risk Aug 2, 2026), EU Data Act (Sept 12, 2025), EU Cyber Resilience Act (Dec 2027 manufacturer obligations), US state privacy expansion (19+ states 2026), SEC cyber 8-K, NYDFS 500 expansions, CMMC 2.0 Phase 1 2025-Q4. Tools: Thomson Reuters Regulatory Intelligence, Compliance.ai, IAPP, Vanta / Drata regulatory updates.
---

# Regulatory Horizon Scanning — Quarterly Brief

Active 2026 regulatory horizon spans privacy + cyber + AI + financial + sector. Quarterly brief covers in-force-this-quarter + coming-this-year + watch-list. Tools: IAPP State Privacy Tracker + Thomson Reuters + Compliance.ai + Vanta/Drata regulatory updates.

## When to use

User says:
- "Regulatory horizon" / "upcoming regulations"
- "DORA" / "NIS2" / "EU AI Act" / "Data Act" / "CRA"
- "State privacy law expansion"
- "SEC cyber 8-K"
- "NYDFS 500"
- "CMMC 2.0"
- "Quarterly compliance brief"
- "Regulatory watchlist"

Companion skills: `ai-governance-eu-ai-act-eticas-credo`, `gdpr-article-30-ropa-dpia`, `risk-register-maintenance-scoring`.

## Setup

```bash
# Free trackers + portals
# IAPP US State Privacy Tracker
curl -fsSL https://iapp.org/resources/article/us-state-privacy-legislation-tracker/ > /tmp/iapp.html

# IAPP Global Privacy Tracker
curl -fsSL https://iapp.org/resources/article/global-privacy-law-and-dpa-directory/ > /tmp/iapp_global.html

# NCSL US State Laws Tracker (security + privacy)
curl -fsSL https://www.ncsl.org/technology-and-communication/security-breach-notification-laws > /tmp/ncsl_breach.html
curl -fsSL https://www.ncsl.org/technology-and-communication/state-laws-related-to-digital-privacy > /tmp/ncsl_privacy.html

# EU Commission Digital Strategy
curl -fsSL https://digital-strategy.ec.europa.eu/en/policies > /tmp/eu_ds.html

# US Federal Register
curl -fsSL "https://www.federalregister.gov/api/v1/documents?conditions[agencies][]=securities-and-exchange-commission&conditions[type][]=rule" > /tmp/fed_reg.json

# UK Gov Cyber
curl -fsSL https://www.gov.uk/government/organisations/department-for-science-innovation-and-technology > /tmp/uk_dsit.html

# Paid trackers
# https://www.thomsonreuters.com/en/products/regulatory-intelligence/
# https://compliance.ai/
# https://www.lexisnexis.com/en-us/products/lexis-plus.page
```

## Common recipes

### Recipe 1: EU DORA (Digital Operational Resilience Act)

```text
Regulation (EU) 2022/2554. In force Jan 17, 2025.

Applies to:
- Financial entities (banks, insurance, investment firms, payment + e-money,
  crypto-asset service providers per MiCA)
- ICT third-party providers serving financial entities
- Auditors (Annex)

Key obligations:
1. ICT Risk Management Framework (Art. 5-15) — proportionate to scale
2. Incident reporting (Art. 17-23) — 4h initial classification + 24h initial
   notification + 1mo final report
3. Digital Operational Resilience Testing (Art. 24-27) — TLPT (Threat-Led
   Penetration Testing) for designated entities every 3 years
4. ICT Third Party Risk Management (Art. 28-44) — register, oversight,
   contracts include specific clauses
5. Information Sharing (Art. 45-49) — voluntary intelligence sharing

Penalties: per Member State (typically fines proportional to severity).

Compliance: lead Member State NCA + ESAs (EBA, EIOPA, ESMA).

Critical Third Party (CTP) designation (top providers): direct ESA oversight.
```

### Recipe 2: EU NIS2 Directive

```text
Directive (EU) 2022/2555. Member State transposition deadline Oct 17, 2024.
Active enforcement 2026.

Applies to:
- ESSENTIAL ENTITIES (large in critical sectors): energy, transport, banking,
  financial market infra, health, drinking water, waste water, digital infra
  (incl. cloud, data center, CDN, DNS, TLD registries), ICT service mgmt,
  public administration, space.
- IMPORTANT ENTITIES (medium in critical sectors + large in other listed
  sectors): postal/courier, waste mgmt, chemicals, food, manufacturing of
  critical products, digital providers (online marketplaces, search,
  social networking), research.

Key obligations:
1. Cybersecurity risk management measures (Art. 21) — 10 named areas incl.
   policies, incident handling, BC, supply chain, secure dev, basic cyber
   hygiene, encryption, HR access, awareness training, multi-factor auth,
   secure communications.
2. Reporting (Art. 23) — 24h early warning + 72h incident notification + 1mo
   final report.
3. Governance — management bodies must approve cybersecurity measures + take
   training.
4. Supervision + enforcement — Member States designate competent authorities.

Penalties:
- Essential: up to €10M OR 2% global turnover (whichever higher)
- Important: up to €7M OR 1.4% global turnover

Management liability — managers can be held personally accountable.
```

### Recipe 3: EU AI Act (Regulation 2024/1689)

```text
See `ai-governance-eu-ai-act-eticas-credo` for detailed coverage.

Key 2026 milestone: August 2, 2026 — high-risk AI obligations effective.

Penalties:
- Prohibited AI (Art. 5): €35M / 7% global revenue
- Non-compliance high-risk: €15M / 3%
- Other non-compliance: €7.5M / 1.5%

Phased applicability:
- Feb 2, 2025 — Bans (Art. 5) + AI literacy (Art. 4)
- Aug 2, 2025 — GPAI obligations (Art. 51-55) + governance + penalties
- Aug 2, 2026 — High-risk Annex III + transparency (Art. 50)
- Aug 2, 2027 — High-risk Annex I (safety components of regulated products)
```

### Recipe 4: EU Data Act

```text
Regulation (EU) 2023/2854. Applicable from Sept 12, 2025.

Applies to:
- Manufacturers of connected products + suppliers of related services
- Data holders + recipients
- B2B + B2C data sharing

Key obligations:
1. Access to data by users of connected products
2. B2B data sharing on FRAND terms
3. Public sector access in exceptional need
4. Switching cloud + edge providers (Chapter VI)
5. Interoperability (Chapter VIII)
6. Smart contracts requirements (Art. 36)

Cloud switching: providers must facilitate switching with reduced fees over
time (no fee from Jan 2027).
```

### Recipe 5: EU Cyber Resilience Act (CRA)

```text
Regulation (EU) 2024/2847. Manufacturer obligations effective Dec 11, 2027.

Applies to: products with digital elements (PDE) — hardware + software.

Key obligations:
1. Security-by-design + by-default
2. Vulnerability handling — SBOM, security updates throughout support
3. Conformity assessment (self-assessment vs notified body for class III)
4. CE marking
5. Incident reporting (24h actively-exploited vuln + 72h significant
   incidents)
6. Documentation (Annex II)
7. Reporting + cooperation with ENISA

Penalties: €15M / 2.5% global revenue.

Free + open-source carve-out — most OSS not in scope unless monetized.
```

### Recipe 6: US state privacy laws — 2026 status

```text
In force (Jan 2026):
- California (CCPA + CPRA — most mature; CPPA enforcement)
- Virginia (CDPA — 2023)
- Colorado (CPA — 2023)
- Connecticut (CTDPA — 2023)
- Utah (UCPA — 2023)
- Iowa (ICDPA — 2025)
- Oregon (OCPA — July 2024)
- Texas (TDPSA — July 2024)
- Tennessee (TIPA — July 2025)
- Montana (MCDPA — Oct 2024)
- Delaware (DPDPA — Jan 2025)
- New Jersey (NJDPA — Jan 2025)
- New Hampshire (NHDPA — Jan 2025)
- Maryland (MODPA — Oct 2025)

In force during 2026:
- Indiana (Jan 2026)
- Kentucky (Jan 2026)
- Minnesota (July 2026)
- Nebraska (Jan 2026)
- Rhode Island (Jan 2026)

Common features:
- Consumer rights (access, delete, correct, opt-out of sale/share/profiling)
- Universal opt-out (GPC recognition — strongest in CA, CO)
- Sensitive data category opt-in (CO/CT/UT)
- Data protection assessment for high-risk processing
- DPA + service-provider agreements
- Penalty: typically $7,500-$25K/violation; per-violation can stack rapidly

Federal: no comprehensive federal privacy law as of 2026.

Track via IAPP State Privacy Tracker (live).
```

### Recipe 7: US sector-specific federal

```text
SEC Cyber Disclosure (33-11216, Dec 2023):
- 8-K Item 1.05 — material cyber 4 business days
- 10-K Item 1C — risk mgmt + governance disclosure

NYDFS 23 NYCRR 500:
- Phase 1 Nov 2023 — governance + risk + access + training
- Phase 2 Nov 2024 — incident reporting expansion, asset inventory, BCP/DR
- Annual cyber compliance certification

CMMC 2.0 (DoD):
- Phase 1: Q4 2025 — initial implementation
- Phase 2: 2026 — expanded
- Three levels (Foundational / Advanced / Expert)
- NIST SP 800-171 baseline for Level 2

GLBA Safeguards Rule (2024 update):
- Designated Qualified Individual
- Risk assessment
- Encryption (in motion, at rest)
- MFA, secure dev
- Awareness training
- Incident response + 30-day notification (500+)

HIPAA enforcement — no major rule changes 2024-2026 but OCR enforcement
intensifying (esp. risk analysis adequacy).

CMS Interoperability + Patient Access (CMS-9115-F) — payer + provider data
exchange.

FTC Health Breach Notification Rule (2024 update) — broader applicability
to health apps + connected devices.
```

### Recipe 8: International expansion (non-EU/US)

```text
UK:
- UK GDPR (post-Brexit Data Protection Act 2018)
- Data Protection and Digital Information Bill 2024 (DPDI) — reform
  pending
- Cyber Resilience Strategy

Canada:
- PIPEDA (federal) + provincial laws
- Bill C-27 (AI + Data) — pending
- Quebec Law 25 (in force Sept 2023)

Brazil:
- LGPD enforcement intensifying
- ANPD regulator
- DPIA + DPO requirements

China:
- PIPL (Personal Information Protection Law)
- CSL (Cybersecurity Law)
- DSL (Data Security Law)
- Cross-border transfer security assessment

Japan:
- APPI (2022 amendment in force)
- PPC regulator

India:
- DPDPA (Digital Personal Data Protection Act 2023)
- Data Protection Board (DPB)

Australia:
- Privacy Act 1988 + Privacy Amendment Act 2022 (penalties to $50M)
- 2023 Reform White Paper changes pending

South Africa:
- POPIA enforcement

Singapore:
- PDPA + Cybersecurity Act 2018
```

### Recipe 9: Quarterly horizon brief template

```markdown
# Regulatory Horizon Brief — <Quarter Year>

**Prepared by:** Compliance Lead
**Date:** <YYYY-MM-DD>
**Audience:** Board + Exec Team

## TLDR
- <Top 3 items this quarter>

## In force this quarter
| Regulation | Effective | Applicability | Action this quarter | Status |
|---|---|---|---|---|
| Minnesota Consumer Data Privacy Act | July 2026 | If >100K MN consumers | Confirm sub-processor + UA opt-in for sensitive | In progress |
| EU AI Act high-risk obligations | Aug 2, 2026 | High-risk systems | Conformity assessment for resume screening | In progress |

## Coming this year
| Regulation | Effective | Applicability | Prep needed |
|---|---|---|---|
| EU CRA (manufacturer) | Dec 2027 | Connected products | SBOM + vuln process |
| CMMC 2.0 Phase 2 | 2026 | DoD contractors | NIST 800-171 verification |
| Indian DPDPA — rules | TBD 2026 | India personal data | Privacy notice + DPO + DPB readiness |

## Watch-list (1-2 year horizon)
- US federal privacy law (APRA / ADPPA debates ongoing)
- EU Cyber Solidarity Act
- EU FRIA expansion for AI deployment
- US AI executive order successor

## Action items
| Owner | Action | Due |
|---|---|---|
| Legal | Update privacy notice for MN | 2026-07-01 |
| AI Gov Lead | Begin conformity assessment for HR AI | 2026-07-15 |
| Risk Lead | Add EU CRA risk to register | 2026-07-01 |

## Reading + references
- IAPP State Privacy Tracker
- EU Commission Digital Strategy
- IAPP Westin Center

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

### Recipe 10: Source list for horizon scanning

```text
Free sources (recommended for quarterly cadence):
- IAPP — US State Privacy Tracker + Westin Research Center
- NCSL — US state laws
- EU Commission — Digital Strategy
- Member State DPAs (CNIL, ICO, AEPD, BfDI, DPC, etc.)
- EDPB — Guidelines
- ENISA — EU agency for cybersecurity
- US Federal Register
- SEC Press Releases + Final Rules
- NIST publications
- Treasury OFAC SDN updates
- FTC enforcement actions
- HHS OCR enforcement

Paid sources:
- Thomson Reuters Regulatory Intelligence
- Compliance.ai
- LexisNexis Risk Solutions
- Bloomberg Government
- Dentons / DLA Piper / Hogan Lovells alerts (often free with sign-up)
- Privacy + Cyber blogs (Wilson Sonsini, Davis Wright Tremaine, etc.)
```

### Recipe 11: Vendor regulatory updates

```text
Vanta / Drata / Secureframe ship regulatory updates:
- Auto-add new framework + control changes
- Notify of effective-date changes
- Suggest evidence updates

Subscribe to:
- Vanta blog
- Drata blog
- Secureframe blog
- Hoxhunt blog (cyber + GDPR)
- Compliance.ai newsletter
- IAPP Daily Dashboard
```

### Recipe 12: Risk register integration

```text
Each regulation → risk register entry:
- Risk: non-compliance with <regulation>
- Asset: org / data category in scope
- Inherent likelihood: depends on enforcement maturity
- Inherent impact: depends on penalty + customer churn
- Treatment: implement controls + monitor

Tag risks with effective dates → quarterly refresh surfaces approaching
deadlines.
```

### Recipe 13: Communication to leadership

```text
Cadence:
- Quarterly brief to Board / Exec (this skill pack)
- Annual planning input
- Ad-hoc memo for material change (new regulation, enforcement uptick)

Format:
- Top 3 items front-loaded
- Risk-based impact assessment
- Required action + owner + due date
- Investment ask if significant

Avoid:
- Comprehensive 50-reg dump (loses attention)
- Legal-jargon-heavy (translate to business)
- No action items (loses agency)
```

## Examples

### Example 1: Q2 2026 brief

**Goal:** Quarterly brief for Exec.

**Steps:**
1. Pull updates from IAPP + NCSL + EU Commission + Vanta blog.
2. Cross-reference our existing register entries.
3. Identify in-force-this-quarter (Minnesota, AI Act high-risk).
4. Draft brief per Recipe 9.
5. Distribute + present to Board.

**Result:** Strategic visibility; resource allocation aligned.

### Example 2: Onboarding a new market (India)

**Goal:** Launch in India; understand DPDPA.

**Steps:**
1. Read DPDPA full text.
2. Identify Data Fiduciary obligations.
3. DPO appointment + notification.
4. Update ROPA + privacy notice for India operations.
5. India data-residency assessment.
6. Risk register entry.
7. Brief Exec.

**Result:** Market entry compliant from day one.

### Example 3: EU AI Act prep sprint

**Goal:** 90-day sprint for Aug 2 2026 readiness.

**Steps:**
1. AI inventory completion.
2. Risk classification per system.
3. Conformity assessment for high-risk.
4. Pre-deployment documentation (Annex IV).
5. Post-market monitoring plan.
6. Register update.
7. Communicate to Board.

**Result:** Aug 2 2026 effective-date readiness.

## Edge cases / gotchas

- **Effective date != enforcement date.** Many regs delay enforcement; don't relax until enforcement.
- **State law variation in US.** 19+ state privacy laws diverge in detail; build per-state policy engine OR use SDR vendor (DataGrail, Securiti).
- **Brexit drift** — UK GDPR + EU GDPR diverging; track separately.
- **Member State transposition variation** — EU Directives implemented differently across 27 Member States; check national variant.
- **Sub-regulatory guidance** — DPAs + regulators publish guidance after the regulation; horizon scanning continues post-enforcement.
- **Penalties scale + stack** — one incident can trigger multiple regulators.
- **Industry codes of conduct** — voluntary but signal compliance + may be auditor-respected.
- **CMMC contract clauses** flow down — even subcontractors hit by prime's CMMC requirements.
- **Sandboxes + regulatory pilots** (e.g., UK ICO Sandbox, CNIL AI Sandbox) — opportunity to test pre-enforcement.
- **Material change disclosure** for SEC + NYDFS — annual disclosures must reflect changes.
- **Federal vs state preemption** — federal cyber rules don't preempt state breach laws; both apply.
- **Enforcement intensity varies** — Cal AG + Spanish AEPD + CNIL + Irish DPC most active; some Member State DPAs are dormant.
- **Penalty caps don't apply to all violations** — some count per violation per data subject.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [IAPP US State Privacy Tracker](https://iapp.org/resources/article/us-state-privacy-legislation-tracker/)
- [IAPP Global Privacy Tracker](https://iapp.org/resources/article/global-privacy-law-and-dpa-directory/)
- [NCSL State Laws](https://www.ncsl.org/)
- [EU Commission Digital Strategy](https://digital-strategy.ec.europa.eu/en/policies)
- [EU NIS2](https://eur-lex.europa.eu/eli/dir/2022/2555/oj)
- [EU DORA](https://eur-lex.europa.eu/eli/reg/2022/2554/oj)
- [EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- [EU Data Act](https://eur-lex.europa.eu/eli/reg/2023/2854/oj)
- [EU Cyber Resilience Act](https://eur-lex.europa.eu/eli/reg/2024/2847/oj)
- [SEC Cyber Disclosure](https://www.sec.gov/rules/final/2023/33-11216.pdf)
- [NYDFS 23 NYCRR 500](https://www.dfs.ny.gov/industry_guidance/cybersecurity)
- [DoD CMMC](https://dodcio.defense.gov/CMMC/)
- [FTC Safeguards Rule](https://www.ftc.gov/legal-library/browse/rules/safeguards-rule)
- [HHS OCR Enforcement](https://www.hhs.gov/hipaa/for-professionals/compliance-enforcement/index.html)
- [ENISA](https://www.enisa.europa.eu/)
- [Thomson Reuters Regulatory Intelligence](https://www.thomsonreuters.com/en/products/regulatory-intelligence/)
- [Compliance.ai](https://compliance.ai/)
- [IAPP Westin Research Center](https://iapp.org/resources/westin-research-center/)
