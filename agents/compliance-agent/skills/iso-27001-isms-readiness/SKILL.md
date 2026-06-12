---
name: iso-27001-isms-readiness
description: Prepare for ISO/IEC 27001:2022 certification — ISMS structure (mandatory clauses 4-10), Statement of Applicability (SoA) against 93 Annex A controls in 4 themes, risk assessment + treatment (ISO 27005), internal audit + management review, Stage 1 + Stage 2 + surveillance cycle. Add-on modules: 27017 cloud, 27018 PII processor, 27701 PIMS, 42001 AI Management System. Output is a gap analysis + remediation plan with the consult-a-compliance-professional disclaimer.
---

# ISO 27001:2022 ISMS Readiness + Add-on Modules

ISO/IEC 27001:2022 is the international ISMS (Information Security Management System) standard. The 2022 update consolidated Annex A from 114 → 93 controls reorganized into 4 themes. Add-on modules 27017 (cloud), 27018 (cloud PII processor), 27701 (PIMS), and 42001 (AI Management System) extend the base ISMS.

## When to use

User says:
- "ISO 27001 prep" / "ISMS readiness" / "ISO certification"
- "Statement of Applicability" / "SoA"
- "Annex A controls" / "93 controls" / "4 themes"
- "Stage 1 audit" / "Stage 2 audit" / "Surveillance audit"
- "Internal ISMS audit" (Clause 9.2)
- "Management review" (Clause 9.3)
- "ISO 27017 cloud" / "27018 PII" / "27701 PIMS" / "42001 AI"
- "Cross-walk ISO to SOC 2 / NIST"

Companion skills: `drata-vanta-secureframe-soc2-monitoring`, `risk-register-maintenance-scoring`, `ai-governance-eu-ai-act-eticas-credo`, `policy-authoring-cybersecurity-aup-byod`.

## Setup

```bash
# ISO catalog (titles + abstracts only — full text paid)
curl -fsSL https://www.iso.org/standard/27001 > /tmp/iso27001_landing.html
curl -fsSL https://www.iso.org/standard/43757.html > /tmp/iso27017_landing.html
curl -fsSL https://www.iso.org/standard/76559.html > /tmp/iso27018_landing.html
curl -fsSL https://www.iso.org/standard/71670.html > /tmp/iso27701_landing.html
curl -fsSL https://www.iso.org/standard/81230.html > /tmp/iso42001_landing.html

# Recipient buys the standard from ISO or ANSI ($150-$200 USD per standard).
# Free alternatives for control descriptions:
#   - NIST CSF 2.0 (cross-walks to ISO 27001:2022)
#   - CIS Controls v8 mapping to ISO Annex A

# Automation platforms (multi-framework — same as SOC 2 stack)
export DRATA_API_KEY=<drata-dashboard>
export VANTA_API_KEY=<vanta-dashboard>
export SECUREFRAME_API_KEY=<secureframe-dashboard>
```

Auth notes:
- ISO full-text PDFs are paywalled. Use ANSI Webstore (ansi.org) or BSI Shop (bsigroup.com).
- BSI Knowledge subscription bundles 27001:2022 + 27002:2022 + 27005:2022 + 27017 + 27018 + 27701 + 42001.

## Common recipes

### Recipe 1: Mandatory ISMS clauses (4-10) — what must exist

```text
Clause 4 — Context of the organization
- 4.1 Internal + external issues affecting ISMS purpose
- 4.2 Interested parties + their requirements
- 4.3 ISMS SCOPE statement (documented; signed)
- 4.4 ISMS itself

Clause 5 — Leadership
- 5.1 Leadership + commitment
- 5.2 Information Security Policy (documented; communicated)
- 5.3 Roles + responsibilities + authorities

Clause 6 — Planning
- 6.1.1 Actions to address risks + opportunities
- 6.1.2 Risk ASSESSMENT process (documented)
- 6.1.3 Risk TREATMENT process + SoA + treatment plan
- 6.2 Information security OBJECTIVES (measurable; reviewed)
- 6.3 Planning of changes

Clause 7 — Support
- 7.1 Resources
- 7.2 Competence
- 7.3 Awareness
- 7.4 Communication
- 7.5 Documented information (control of)

Clause 8 — Operation
- 8.1 Operational planning + control
- 8.2 Risk assessment performed at planned intervals + on change
- 8.3 Risk treatment plan implementation

Clause 9 — Performance evaluation
- 9.1 Monitoring + measurement + analysis + evaluation
- 9.2 INTERNAL AUDIT (annual minimum; planned program)
- 9.3 MANAGEMENT REVIEW (annual minimum; documented inputs + outputs)

Clause 10 — Improvement
- 10.1 Nonconformity + corrective action
- 10.2 Continual improvement
```

### Recipe 2: Annex A — 93 controls, 4 themes (2022 update)

```text
A.5 Organizational (37 controls) — policies, roles, segregation, threat intel,
    project security, info classification + handling, supplier security, info
    exchange, incident management, BC, identity mgmt, access rights.

A.6 People (8 controls) — screening, terms + conditions, awareness + training,
    disciplinary process, remote work, NDA.

A.7 Physical (14 controls) — security perimeter, entry, secure areas, working
    in secure areas, desks + screens, equipment siting, supply utilities,
    cabling, maintenance, removal, off-premises, disposal, storage media,
    terminals.

A.8 Technological (34 controls) — endpoint, privileged access, info access,
    code, source code access, secure dev, lifecycle, authentication, capacity,
    malware, vuln mgmt, config mgmt, deletion, masking, leak prevention,
    backup, redundancy, logging, monitoring, clock sync, privileged utility,
    install of apps, networks, network controls, network segregation, DNS +
    filtering, secure dev lifecycle, software dev lifecycle, secure dev
    environment, outsourced dev, testing, security test acceptance, prod-test
    data separation, cloud security.
```

Full control list: ISO/IEC 27002:2022 (the implementation guidance companion).

### Recipe 3: Statement of Applicability (SoA) template

```markdown
# Statement of Applicability — <Co.>
**Standard:** ISO/IEC 27001:2022
**Version:** <X.Y>
**Approval:** <Name, role, date>
**Scope reference:** <pointer to ISMS scope statement>

| Annex A control | Title | Applicable? (Y/N) | Justification | Implementation status | Evidence ref |
|---|---|---|---|---|---|
| A.5.1 | Policies for information security | Y | Required by all org activities | Implemented | Policy library §1.1 |
| A.5.2 | Information security roles + responsibilities | Y | Required | Implemented | Role matrix R-001 |
| A.5.7 | Threat intelligence | Y | Required for SOC ops | Implemented | TI feed config |
| A.7.1 | Physical security perimeters | N | Fully remote org; no physical perimeter | N/A | Remote-work policy §3 |
| ... | ... | ... | ... | ... | ... |

**Note:** ALL 93 controls must appear with a status (Y/N + justification).
```

### Recipe 4: Risk assessment per ISO 27005:2022

```text
For each information asset OR process:
1. IDENTIFY threats + vulnerabilities
2. ANALYZE — likelihood × impact (5x5 ordinal default; FAIR for quant)
3. EVALUATE — compare against risk acceptance criteria
4. TREAT — modify (controls) / share (insurance, vendor) / retain (accept) / avoid

Output: Risk Register (see risk-register-maintenance-scoring skill pack) + Risk
Treatment Plan + SoA control selection.

Trigger conditions for re-assessment:
- Annual minimum (Clause 8.2)
- On material change (new product, system, vendor, regulation)
- After incident affecting risk landscape
```

### Recipe 5: Stage 1 + Stage 2 + surveillance + recertification cycle

```text
Stage 1 (Documentation review):
- Duration: ~1 week
- Auditor reviews ISMS scope, policy, SoA, risk assessment, treatment plan,
  internal audit + management review records.
- Output: Stage 1 report identifying readiness gaps.
- Outcome: Recommendation to proceed (or remediate first).

Stage 2 (Implementation audit):
- Duration: 2-3 weeks for SMB; longer for enterprise
- Auditor verifies ISMS is implemented + operating.
- Sample testing of evidence per control.
- Output: Stage 2 report + nonconformities (major / minor).
- Outcome: Certification (if no major nonconformities).

Certification cycle (3 years):
- Year 1 (post-cert) — Surveillance audit 1 (reduced scope, ~1 week)
- Year 2 — Surveillance audit 2 (reduced scope, ~1 week)
- Year 3 — Recertification (full audit, similar to Stage 2)

Surveillance focuses on:
- Internal audit results
- Management review
- Incidents + nonconformities + corrective actions
- Sample of controls (rotates)
- Changes since last audit
```

### Recipe 6: Cert body shortlist (2026)

```text
Mid-market accessible:
- Schellman (US + global; SOC 2 + ISO bundle common)
- A-LIGN (US + global; broad compliance practice)
- Coalfire ISO (security-focused)
- LRQA (formerly Lloyd's Register)
- BSI (premium + global recognition; UK origin)

EU strong:
- TÜV (multiple — TÜV Rheinland, TÜV SÜD, TÜV NORD)
- Bureau Veritas
- SGS

Cost benchmark (2026): $15K-$50K for SMB Stage 1 + Stage 2; $5K-$15K
surveillance year. Verify cert body is accredited by IAF member (ANAB in US,
UKAS in UK, DAkkS in DE, etc.) — accreditation IS the cert body's authority.
```

### Recipe 7: Add-on — ISO/IEC 27017:2015 (cloud security)

```text
27017 = extension of 27002 with cloud-specific guidance.
Applies to BOTH cloud service providers AND cloud customers.
Adds 7 new controls + cloud-specific guidance for existing 27002 controls.

Use when:
- You provide cloud services (CSP)
- Customers require cloud-specific assurance
- You're hosted entirely on cloud (most SaaS) — demonstrates shared
  responsibility model awareness.

Cert path: 27017 is certifiable AS AN EXTENSION to your 27001 cert. Same cert
body extends scope.
```

### Recipe 8: Add-on — ISO/IEC 27018:2019 (PII processor in public cloud)

```text
27018 = code of practice for protecting PII in public cloud (processor role).
Mandatory for cloud processors handling PII under GDPR Art. 28.

Key requirements:
- Customer (data controller) explicit consent for sub-processors
- Return / deletion of PII at contract end
- Disclosure of sub-processors + locations
- Transparency on PII processing
- PII breach notification

Cert path: certifiable as extension to 27001 cert.
```

### Recipe 9: Add-on — ISO/IEC 27701:2019 (PIMS — Privacy Information Management System)

```text
27701 = extension to 27001 for privacy. Maps to GDPR Art. 5-49.

Add-on requirements:
- Privacy controls per PII controller AND/OR PII processor role
- Data subject rights handling (maps to GDPR Art. 12-23)
- DPIA process (maps to GDPR Art. 35)
- Privacy by design + default
- International transfer mechanisms

Use when:
- GDPR / CCPA in scope
- Customer asks for privacy certification
- Want one combined ISMS + PIMS certification

Cert path: extension to 27001 cert; same cert body.
```

### Recipe 10: Add-on — ISO/IEC 42001:2023 (AI Management System — AIMS)

```text
42001 = AI Management System standard (published Dec 2023; first
certifications late 2024 onwards).

Maps directly to EU AI Act high-risk obligations (effective Aug 2, 2026) and
NIST AI RMF 1.0.

Core requirements:
- AI policy + objectives
- AI risk assessment per system (impact + likelihood)
- AI lifecycle management (design → deployment → monitoring → decommission)
- AI system documentation + model cards
- Data governance for AI training data
- Bias + fairness assessment
- Human oversight (for high-risk per EU AI Act)
- Post-deployment monitoring

Cert path: standalone OR extension to 27001. Schellman, A-LIGN, BSI offering
42001 cert in 2026.

Companion skill: ai-governance-eu-ai-act-eticas-credo.
```

### Recipe 11: Internal audit (Clause 9.2) checklist

```markdown
# Internal ISMS Audit Plan — <Co.> — <year>

**Purpose:** Verify ISMS conforms to ISO/IEC 27001:2022 + organization's
requirements + is effectively implemented and maintained (Clause 9.2.1).

**Scope:** Full ISMS (rotating focus areas per year).
**Auditor:** <independent, qualified — internal or external>
**Audit criteria:** ISO 27001:2022 clauses 4-10 + Annex A + ISMS docs.

## Audit schedule
| Quarter | Focus area | Auditor | Duration |
|---|---|---|---|
| Q1 | Leadership + planning (Cl. 5, 6) | <name> | 2 days |
| Q2 | Operation + risk treatment (Cl. 8) | <name> | 3 days |
| Q3 | Annex A.5 + A.6 sample | <name> | 3 days |
| Q4 | Annex A.8 sample + management review prep | <name> | 4 days |

## Reporting
- Findings classified: Major nonconformity / Minor nonconformity / Observation
- 30-day corrective action plan for nonconformities
- Audit report to management review input
```

### Recipe 12: Management review (Clause 9.3) agenda

```markdown
# ISMS Management Review — <Co.> — <date>

**Attendees:** ISMS Owner, CISO/Security Lead, IT Lead, Privacy Lead, CFO
(resource decisions), CEO/Exec sponsor.

**Inputs (required per Clause 9.3.2):**
1. Status of prior management review actions
2. Changes in internal/external issues + interested parties
3. Information security performance — nonconformities + corrective actions,
   monitoring + measurement results, audit results, fulfillment of objectives
4. Feedback from interested parties
5. Results of risk assessment + status of risk treatment plan
6. Opportunities for continual improvement

**Outputs (required per Clause 9.3.3):**
- Decisions on continual improvement opportunities
- Any changes needed to the ISMS

**Documented:** Minutes signed by ISMS Owner; retained per documented info
retention policy.
```

### Recipe 13: ISO 27001 → SOC 2 crosswalk for joint audit efficiency

| ISO 27001:2022 | SOC 2 TSC | Notes |
|---|---|---|
| 4.3 ISMS Scope | SOC 2 system description | Reuse same scope doc |
| 5.2 Info Sec Policy | CC1.1 | One policy, two reports |
| 6.1.2 Risk Assessment | CC3.1 | One methodology |
| 9.2 Internal Audit | CC4.1 | Internal audit feeds both |
| A.5.7 Threat intel | CC7.1 | Same threat feed |
| A.8.8 Vuln mgmt | CC7.1 | Same VM program |
| A.5.24-28 Incident mgmt | CC7.4, CC7.5 | Same IR plan |
| A.5.19-23 Supplier security | CC9.2 | Same TPRM program |
| A.6.3 Awareness | CC1.4 | Same training |

Schellman + A-LIGN offer joint SOC 2 + ISO 27001 audits — 30-50% effort savings vs sequential.

## Examples

### Example 1: First-time ISO 27001 cert (mid-stage SaaS)

**Goal:** Achieve ISO 27001:2022 cert in 12 months alongside SOC 2 Type II.

**Steps:**
1. Confirm scope: production environment + supporting business functions.
2. Use Vanta or Drata for combined evidence (both support 27001:2022 framework).
3. Write 4.3 scope statement; 5.2 policy; risk assessment per ISO 27005.
4. Build SoA against 93 Annex A controls.
5. Implement controls; collect evidence in Vanta/Drata.
6. Q3: internal audit (Recipe 11).
7. Q4: management review (Recipe 12).
8. Engage Schellman for joint SOC 2 + ISO 27001 audit.
9. Stage 1 → Stage 2 → cert issued.

**Result:** Two certs from one effort; ~30-50% cost savings vs sequential.

### Example 2: Add 27701 PIMS to existing 27001

**Goal:** Add GDPR-aligned privacy cert to current ISO 27001:2022 cert.

**Steps:**
1. Document additional privacy controls per 27701 Annex B + C.
2. Update ROPA (see `gdpr-article-30-ropa-dpia`).
3. Update SoA to include PIMS-specific controls.
4. Engage current cert body for extension audit.
5. Stage 1 + Stage 2 extension → cert issued covering 27001 + 27701.

**Result:** Combined ISMS + PIMS cert; satisfies GDPR Art. 32 + 42.

### Example 3: 42001 AI Management System for AI-first SaaS

**Goal:** Achieve 42001 cert to demonstrate EU AI Act preparedness.

**Steps:**
1. Build AI inventory (see `ai-governance-eu-ai-act-eticas-credo`).
2. Per-system risk classification per EU AI Act.
3. Document AI lifecycle (design → deployment → monitoring → decommission).
4. Model cards for each production model.
5. Human oversight design for high-risk systems.
6. Engage Schellman / BSI / A-LIGN for 42001 audit.
7. Stage 1 + Stage 2 → cert.

**Result:** 42001 cert; demonstrable EU AI Act readiness; commercial differentiator.

## Edge cases / gotchas

- **2022 update consolidated 114 → 93 controls.** Don't reuse pre-2022 SoA; control IDs changed.
- **Cert bodies must be IAF-accredited.** Verify ANAB / UKAS / DAkkS / etc. accreditation before contracting.
- **Stage 1 nonconformities don't block Stage 2 immediately,** but must be remediated before Stage 2 cert decision.
- **Major nonconformity at Stage 2 = no cert.** Minor nonconformities are remediated within 90 days post-Stage 2.
- **Surveillance audits rotate scope** — different controls sampled each year. Maintain evidence for all 93 controls year-round.
- **27001 cert is for the ISMS, not for products.** A product cannot be "ISO 27001 certified"; the org's ISMS is.
- **Joint SOC 2 + ISO 27001 audits** save effort but require coordinating two distinct standards. Some auditors do it well; some don't. Reference-check.
- **42001 is new (2023).** Pioneers face cert-body learning curve; expect longer Stage 1 + Stage 2 cycles in 2026.
- **27017 / 27018 / 27701 / 42001 are extensions, not standalone.** All require 27001 base ISMS (or equivalent management system).
- **ISO standards are paywalled.** ~$150-$200 USD per standard. Budget BSI Knowledge or ANSI subscription for orgs with multiple ISO scopes.
- **Documented information control (Clause 7.5) is heavily audited.** Version control + approval + retention + change tracking are non-negotiable.
- **Internal auditors must be independent** of the area they audit (Clause 9.2.2). Engineer cannot audit own team's controls.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) — base standard
- [ISO/IEC 27002:2022](https://www.iso.org/standard/75652.html) — controls implementation guidance
- [ISO/IEC 27005:2022](https://www.iso.org/standard/80585.html) — ISMS risk management
- [ISO/IEC 27017:2015](https://www.iso.org/standard/43757.html) — cloud security
- [ISO/IEC 27018:2019](https://www.iso.org/standard/76559.html) — cloud PII processor
- [ISO/IEC 27701:2019](https://www.iso.org/standard/71670.html) — PIMS
- [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html) — AI Management System
- [IAF — accreditation member list](https://iaf.nu/en/members/)
- [ANAB accreditation lookup](https://anab.ansi.org/credentialing/management-systems)
- [BSI Knowledge subscription](https://knowledge.bsigroup.com/)
- [Schellman ISO 27001](https://www.schellman.com/iso/iso-27001)
- [A-LIGN ISO 27001](https://www.a-lign.com/services/iso/iso-27001)
- [NIST CSF 2.0 ISO 27001 crosswalk](https://www.nist.gov/cyberframework/framework)
