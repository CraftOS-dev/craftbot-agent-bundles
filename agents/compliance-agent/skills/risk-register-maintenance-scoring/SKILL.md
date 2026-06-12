---
name: risk-register-maintenance-scoring
description: Build + maintain risk register per NIST SP 800-30 + ISO/IEC 27005:2022 + FAIR (Factor Analysis of Information Risk; quantitative). Fields per risk: ID, description, asset, threat, vulnerability, inherent likelihood × impact, controls, residual likelihood × impact, owner, treatment (accept / mitigate / transfer / avoid), review date. Scoring: 5x5 ordinal (most teams) or monetized FAIR (mature). Tools: Vanta / Drata / Secureframe risk module, LogicGate, AuditBoard, ServiceNow GRC, Archer, Hyperproof, OpenFAIR. Refresh quarterly + on material change.
---

# Risk Register — NIST SP 800-30 + ISO 27005 + FAIR

Risk register is the single biggest GRC discipline. NIST SP 800-30 Rev. 1 + ISO/IEC 27005:2022 are methodology. FAIR / OpenFAIR for monetized quantification. Vanta / Drata / Secureframe ship register modules; LogicGate / AuditBoard / Hyperproof for enterprise.

## When to use

User says:
- "Risk register" / "risk inventory"
- "Risk scoring" / "5x5 matrix"
- "FAIR" / "OpenFAIR" / "quantitative risk"
- "NIST 800-30" / "ISO 27005"
- "Risk treatment" / "accept / mitigate / transfer / avoid"
- "Residual risk"
- "Risk owner"
- "LogicGate" / "AuditBoard" / "Hyperproof" / "Archer"

Companion skills: `drata-vanta-secureframe-soc2-monitoring`, `iso-27001-isms-readiness`, `tprm-third-party-risk-lifecycle`.

## Setup

```bash
# NIST SP 800-30 Rev. 1
curl -fsSL -o nist_800_30_r1.pdf https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf

# ISO/IEC 27005:2022
curl -fsSL https://www.iso.org/standard/80585.html > /tmp/iso27005.html

# FAIR Institute
curl -fsSL https://www.fairinstitute.org/ > /tmp/fair.html

# OpenFAIR (Open Group)
curl -fsSL https://www.opengroup.org/forum/security/openfair > /tmp/openfair.html

# NIST SP 800-37 Rev. 2 (RMF)
curl -fsSL -o nist_800_37_r2.pdf https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-37r2.pdf

# Paid platforms
# https://www.vanta.com/products/risk-management
# https://drata.com/risk-management
# https://www.logicgate.com/
# https://www.auditboard.com/
# https://www.servicenow.com/products/governance-risk-and-compliance.html
# https://www.archerirm.com/
# https://hyperproof.io/

export VANTA_API_KEY=<dashboard>
export DRATA_API_KEY=<dashboard>
export LOGICGATE_API_KEY=<dashboard>
```

## Common recipes

### Recipe 1: Risk Register field schema

```text
Core fields:
- ID (RISK-001)
- Title
- Description (5W: what could happen, how, who's affected)
- Asset (system, data, process, vendor in scope)
- Asset criticality (Tier 1/2/3/4)
- Threat (source of harm: nation-state, malicious insider, accidental, 
  environmental, regulatory, supply chain, etc.)
- Vulnerability (what weakness)
- Existing controls (preventive, detective, corrective, compensating)
- Inherent likelihood (1-5)
- Inherent impact (1-5)
- Inherent risk score (likelihood × impact)
- Control effectiveness (% reduction)
- Residual likelihood (1-5)
- Residual impact (1-5)
- Residual risk score (likelihood × impact)
- Treatment (Accept / Mitigate / Transfer / Avoid)
- Treatment plan (if Mitigate)
- Owner (role + name)
- Status (Open / In progress / Closed)
- Identified date
- Last review date
- Next review date
- Linked controls (control IDs)
- Linked incidents (incident IDs)
- Linked findings (audit findings)
- Cost of treatment ($)
- Tags (framework: SOC 2 / ISO 27001 / GDPR / etc.)
```

### Recipe 2: 5×5 ordinal risk matrix

```text
Likelihood (annual probability):
1 — Rare (<5%)
2 — Unlikely (5-15%)
3 — Possible (15-40%)
4 — Likely (40-75%)
5 — Almost certain (>75%)

Impact:
1 — Negligible (<$10K, minor disruption, no customer impact)
2 — Minor ($10K-$100K, contained, few customers)
3 — Moderate ($100K-$1M, public note, some customer churn)
4 — Major ($1M-$10M, regulatory action, customer departure, brand)
5 — Severe (>$10M, existential threat, regulatory shutdown)

Risk score = Likelihood × Impact
Bands:
- Critical: 20-25 (red)
- High: 12-16 (orange)
- Medium: 6-10 (yellow)
- Low: 1-5 (green)

Tune ranges to org tolerance.
```

### Recipe 3: Treatment decision matrix

```text
ACCEPT — when:
- Cost of mitigation exceeds risk reduction
- Risk is below tolerance
- Strategic risk-taking (intentional business risk)
Documentation: written acceptance by risk owner + senior management.
Review: annually + on material change.

MITIGATE — when:
- Cost-effective control reduces risk meaningfully
- Default approach
Documentation: control implementation plan + owner + due date.

TRANSFER — when:
- Insurance covers (cyber liability, E&O, D&O)
- Contractual transfer (vendor takes ownership)
- Outsourcing to qualified provider
Documentation: policy / contract; verify coverage adequacy.

AVOID — when:
- Risk exceeds tolerance + cannot be mitigated
- Activity / function discontinued
Documentation: written decision + alternative path.

Most mature programs: 60% mitigate, 20% accept, 15% transfer, 5% avoid.
```

### Recipe 4: NIST SP 800-30 Risk Assessment process

```text
1. PREPARE — define purpose, scope, assumptions, constraints, threat sources,
   risk model, analytic approach.
2. CONDUCT —
   2a. Identify threat sources
   2b. Identify threat events
   2c. Identify vulnerabilities
   2d. Determine likelihood
   2e. Determine impact
   2f. Determine risk
3. COMMUNICATE — risk results to stakeholders.
4. MAINTAIN — monitor + update.

Tier-driven (NIST RMF):
- Tier 1: Organization-wide risk
- Tier 2: Mission / business process risk
- Tier 3: Information system risk
```

### Recipe 5: ISO 27005:2022 alignment

```text
Aligns with ISO 27001 Clause 6.1.

Process:
1. Establishing context (scope, criteria, organization)
2. Risk identification (assets, threats, vulnerabilities, impacts)
3. Risk analysis (likelihood × consequence)
4. Risk evaluation (compare against criteria)
5. Risk treatment (modify / share / retain / avoid)
6. Risk acceptance (residual)
7. Risk communication + consultation
8. Risk monitoring + review

Documentation feeds Statement of Applicability (SoA).
```

### Recipe 6: FAIR — Factor Analysis of Information Risk

```text
FAIR = quantitative risk methodology. Monetizes risk.

Risk = Loss Event Frequency × Loss Magnitude

Loss Event Frequency = Threat Event Frequency × Vulnerability
- Threat Event Frequency (TEF): how often threat agent attempts
- Vulnerability: probability threat succeeds

Loss Magnitude:
- Primary loss: response, replacement, productivity
- Secondary loss: fines, judgments, reputation, customer churn

Output: distribution (e.g., expected annual loss $250K; 95th percentile
$1.5M).

FAIR Tools:
- RiskLens (commercial — official FAIR vendor)
- Open-source: pyfair, RAR (R)

Use when:
- Board needs $ language
- Insurance limit setting
- Investment justification ($X risk reduction for $Y control)
- Comparing disparate risks

Skill level: requires statistical literacy; Monte Carlo simulation.
```

### Recipe 7: Risk register entry template

```markdown
# Risk Register Entry

**ID:** RISK-001
**Title:** Customer DB exfiltration via SQL injection
**Date identified:** <YYYY-MM-DD>
**Owner:** <CISO / Eng Lead>
**Last reviewed:** <YYYY-MM-DD>
**Next review:** <quarterly>
**Frameworks:** SOC 2 CC6.6 + CC7.1; ISO 27001 A.5.30, A.8.7, A.8.8; PCI Req 6.2.4

## Description
Attacker exploits SQL injection in customer-facing API to exfiltrate
production database containing 50M customer records.

## Asset
- Customer database (`customers.production`)
- Asset criticality: Tier 1
- Data sensitivity: Restricted (PII)
- Records: 50M

## Threat + vulnerability
- Threat: external attacker (organized crime, nation-state)
- Vulnerability: input validation gap on /api/v1/search endpoint
- Attack vector: HTTP injection

## Existing controls
- WAF (Cloudflare) — partial protection
- Pen-test annually (last: 2026-03; this finding was found)
- Code review (mandatory PR review)
- Application input sanitization library

## Inherent risk (no controls)
- Likelihood: 4 (Likely — common attack)
- Impact: 5 (Severe — 50M records, GDPR €20M + churn + brand)
- Inherent score: 20 (Critical)

## Control effectiveness
- WAF: ~70%
- Code review: ~50%
- Combined: ~85%

## Residual risk
- Likelihood: 2 (Unlikely — controls reduce)
- Impact: 5 (Severe — if it happens, still severe)
- Residual score: 10 (Medium)

## Treatment
- Mitigate
- Action: parameterized queries refactor on /api/v1/search; due 2026-07-15
- Owner: Backend Eng Lead
- Cost: 2 sprints (~$30K dev time)
- Insurance transfer: $10M cyber liability covers
- Acceptance: residual after mitigation

## Status
- Open — in-progress
- Notes: refactor underway; expected close 2026-07-15

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

### Recipe 8: Risk taxonomy (cover all categories)

```text
Strategic risks:
- Competitive
- Strategic execution
- Reputation
- M&A integration

Operational risks:
- Process failure
- People (key person, fraud)
- Systems (downtime, performance)
- Vendor / third party

Financial risks:
- Liquidity
- Credit
- Market
- FX
- Tax

Compliance + regulatory:
- Privacy (GDPR, CCPA, state)
- Security (SOC 2, ISO, HIPAA, PCI)
- Sector-specific (FINRA, SEC, FDA, FAA)
- AML / sanctions
- AI Act
- Anti-bribery (FCPA, UKBA)

Information security:
- Cyber attack (external, insider)
- Data loss / breach
- Ransomware
- BEC
- Supply chain
- Cloud config
- Identity (account takeover)
- App-sec (vuln, code injection)
- Physical

Technology:
- Tech debt
- Vendor lock-in
- AI / ML
- Architecture
- DevOps maturity
- Cloud cost

People:
- Talent retention
- Knowledge concentration
- Culture
- DEI

ESG / sustainability:
- Climate
- Supply chain ethics
- Environmental impact
- Social (community, customer harm)
```

### Recipe 9: Vanta / Drata risk module workflow

```bash
# Vanta risk management module
curl -X GET 'https://api.vanta.com/v1/risks' \
  -H "Authorization: Bearer $VANTA_API_KEY"

# Create a risk
curl -X POST 'https://api.vanta.com/v1/risks' \
  -H "Authorization: Bearer $VANTA_API_KEY" \
  -d '{
    "name":"SQL injection on customer API",
    "category":"Information Security",
    "owner":"<user-id>",
    "likelihood":4,
    "impact":5,
    "treatment":"MITIGATE"
  }'

# Drata
curl -X GET 'https://public-api.drata.com/v1/risks' \
  -H "Authorization: Bearer $DRATA_API_KEY"
```

### Recipe 10: LogicGate Risk Cloud workflow

```text
LogicGate Risk Cloud (paid enterprise):
- Customizable workflow + risk register
- Multi-framework crosswalk
- Risk dashboards
- Treatment plan tracking
- Integration with ServiceNow, Jira, Vanta, Drata

API:
curl -X GET 'https://api.logicgate.com/api/v1/records' \
  -H "Authorization: Bearer $LOGICGATE_API_KEY"
```

### Recipe 11: Quarterly refresh process

```text
Quarterly refresh cycle:
- Review each risk owner's portfolio.
- Re-score likelihood + impact based on:
  - New threat intelligence
  - Recent incidents (internal + industry)
  - Control changes
  - Compensating control changes
  - Asset changes (new systems, decommissioned, M&A)
- Update treatment status.
- Close risks where treatment complete + residual acceptable.
- Add newly identified risks.

Cadence:
- Q1: Information security risks focus
- Q2: Operational + vendor risks focus
- Q3: Compliance + regulatory focus
- Q4: Strategic + financial focus
(plus full review each quarter for top-10 by score)
```

### Recipe 12: Top-N risk dashboard (Board view)

```markdown
# Top Risks Dashboard — <Quarter Year>

## Heatmap (5x5)
```
Impact 5: ■■■  ■■   ■        ■■■
Impact 4: ■    ■■   ■   ■
Impact 3:      ■■   ■■  ■
Impact 2:           ■   ■
Impact 1: 
          L=1  L=2 L=3 L=4 L=5
```

## Top 10 by residual score
| # | ID | Title | L | I | Score | Treatment | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| 1 | RISK-004 | EU AI Act high-risk readiness | 4 | 5 | 20 | Mitigate | AI Gov Lead | In progress |
| 2 | RISK-001 | SQL injection customer API | 2 | 5 | 10 | Mitigate | Eng Lead | Closing 7-15 |
| 3 | RISK-007 | Vendor X SOC 2 expired + no replacement | 3 | 4 | 12 | Mitigate | Procurement | In progress |
| 4 | RISK-012 | Ransomware via phishing | 3 | 5 | 15 | Mitigate | CISO | Continuous |
| 5 | RISK-008 | GDPR Art. 33 — undetected 72h breach exposure | 2 | 5 | 10 | Mitigate | CISO + DPO | In progress |

## Quarter-over-quarter trend
- Risks added: 4
- Risks closed: 7
- Risks escalated: 2 (RISK-004, RISK-012)
- Overall risk score (sum): 142 → 128 (down 10%)

## Treatment status
- Open / In progress: 23
- Closed (this quarter): 7
- Risk accepted: 3 (compensating control)

## Investment priorities (next quarter)
- $250K: AI governance platform (Credo AI)
- $150K: Pen test annual + supplemental
- $80K: SIEM upgrade

---
*Disclaimer per template.*
```

### Recipe 13: Risk owner accountability matrix

```text
Risk owner is accountable for:
- Maintaining accuracy of risk entry
- Treatment plan execution
- Quarterly re-scoring
- Reporting status updates
- Escalation when treatment slips
- Risk acceptance documentation (with senior mgmt approval)

Functional risk owners (typical):
- CISO: information security, cyber, IR, DR
- CTO: technology, architecture, vendor, IT
- COO: operations, process, people
- CFO: financial, tax, audit, liquidity
- DPO: privacy, GDPR, data subject rights
- CCO: regulatory, AML, sanctions
- General Counsel: legal, litigation, contract
- CEO: strategic, M&A, reputation
- Chief AI Officer / AI Governance Lead: AI risks

Org-wide aggregation: 1 risk leader (CRO or CCO or CISO depending on
maturity) consolidates + reports to Board.
```

## Examples

### Example 1: Stand up first risk register

**Goal:** Build risk register for SOC 2 + ISO 27001 evidence.

**Steps:**
1. Inventory risks per Recipe 8 categories.
2. Use Drata risk module.
3. Score with 5×5 (Recipe 2).
4. Assign owners (Recipe 13).
5. Treatment plans (Recipe 3).
6. Quarterly review (Recipe 11).
7. Board dashboard (Recipe 12).

**Result:** SOC 2 CC3.1 / CC3.2 + ISO 27001 Clause 6.1 evidence.

### Example 2: Quantify ransomware risk for cyber insurance

**Goal:** Use FAIR to justify $20M cyber liability limit.

**Steps:**
1. FAIR analysis of ransomware risk.
2. TEF = 0.1/yr (10% chance of successful attempt).
3. Loss Magnitude: primary (response, restore) ~$3M; secondary (fines, churn) ~$8-15M.
4. Monte Carlo: expected annual loss $1.1M; 95th percentile $18M.
5. Justify $20M cyber limit + $5M sublimit for ransom.
6. Broker presentation.

**Result:** Right-sized insurance with FAIR-based rationale.

### Example 3: Q3 quarterly refresh

**Goal:** Q3 refresh + Board report.

**Steps:**
1. Email owners 2 weeks before with update template.
2. Owner review + re-score.
3. Risk lead consolidates.
4. Top-10 dashboard (Recipe 12).
5. Board presentation.
6. Closure of treated risks.

**Result:** Auditable refresh; Board engagement.

## Edge cases / gotchas

- **Risk vs issue.** Risk = potential; issue = realized. Don't conflate.
- **Risk vs threat vs vulnerability.** Threat = source; vuln = weakness; risk = potential loss.
- **5×5 matrix is ordinal, not ratio.** Don't average scores; use ranks.
- **FAIR requires statistical literacy.** Don't introduce mid-skill without training; outcomes can mislead.
- **Risk acceptance must be documented + approved.** Verbal acceptance is not auditor-credible.
- **Closure isn't end.** Closed risks may recur; archive but track.
- **Owner accountability gaps.** "Everyone owns everything" = nobody. Single named owner.
- **Inherent vs residual confusion.** Document both; auditors expect.
- **Quarterly review cadence requires discipline.** Calendar; escalate stale.
- **Top-N visibility focuses Board.** Don't dump all 100+ risks in Board doc.
- **Crosswalk to frameworks** — tag each risk with all applicable framework controls; pulls audit evidence.
- **Tooling lock-in.** Mid-market starts in Vanta/Drata; outgrows to LogicGate/Hyperproof at $10M+ ARR with multi-framework.
- **Risk register ≠ audit findings.** Both feed risk picture; distinct origins.
- **AI Act + ISO 42001 — new risk category.** Refresh taxonomy.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [NIST SP 800-30 Rev. 1](https://csrc.nist.gov/publications/detail/sp/800-30/rev-1/final)
- [NIST SP 800-37 Rev. 2 (RMF)](https://csrc.nist.gov/pubs/sp/800/37/r2/final)
- [NIST SP 800-39 (Managing Risk)](https://csrc.nist.gov/publications/detail/sp/800-39/final)
- [ISO/IEC 27005:2022](https://www.iso.org/standard/80585.html)
- [FAIR Institute](https://www.fairinstitute.org/)
- [OpenFAIR (Open Group)](https://www.opengroup.org/forum/security/openfair)
- [RiskLens](https://www.risklens.com/)
- [Vanta Risk Management](https://www.vanta.com/products/risk-management)
- [Drata Risk Management](https://drata.com/risk-management)
- [Secureframe Risk](https://secureframe.com/products/risk-management)
- [LogicGate Risk Cloud](https://www.logicgate.com/)
- [AuditBoard](https://www.auditboard.com/)
- [ServiceNow GRC](https://www.servicenow.com/products/governance-risk-and-compliance.html)
- [Archer (RSA)](https://www.archerirm.com/)
- [Hyperproof](https://hyperproof.io/)
- [MetricStream](https://www.metricstream.com/)
- [Workiva](https://www.workiva.com/)
