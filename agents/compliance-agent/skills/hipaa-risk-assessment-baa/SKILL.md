---
name: hipaa-risk-assessment-baa
description: Perform HIPAA Security Rule risk analysis (45 CFR §164.308(a)(1)(ii)(A)) per NIST SP 800-66 Rev. 2 (2024). Execute the HHS Security Risk Assessment Tool. Author Business Associate Agreements (BAAs) per §164.504(e) using HHS sample provisions. Cover Administrative + Physical + Technical safeguards, HITECH breach-direct-liability, and 60-day breach notification.
---

# HIPAA Risk Assessment + BAA — Security Rule §164.308 + §164.504(e)

HIPAA Security Rule (45 CFR §§164.302-318) governs PHI confidentiality + integrity + availability. The foundational obligation is the §164.308(a)(1)(ii)(A) Risk Analysis. NIST SP 800-66 Rev. 2 (2024) is the canonical methodology. HHS offers a free Security Risk Assessment (SRA) Tool for small/mid orgs. BAAs per §164.504(e) are mandatory for every Business Associate relationship.

## When to use

User says:
- "HIPAA risk assessment" / "Security Rule risk analysis"
- "164.308" / "Administrative Safeguards"
- "BAA" / "Business Associate Agreement"
- "Subcontractor BAA" / "Sub-BA flow-down"
- "HHS SRA Tool"
- "60-day breach notification" / "PHI breach"
- "HITECH" / "Omnibus Rule"
- "Covered Entity vs Business Associate"
- "Minimum necessary"
- "PHI inventory"

Companion skills: `breach-notification-gdpr-72hr-state-laws`, `risk-register-maintenance-scoring`, `data-classification-dlp-purview-nightfall`, `vendor-security-questionnaire-caiq-sig`.

## Setup

```bash
# HHS SRA Tool (free; small/medium orgs)
# https://www.healthit.gov/topic/privacy-security-and-hipaa/security-risk-assessment-tool
# Windows installer (Excel-based + standalone)
curl -fsSL -o sra_tool_setup.msi \
  https://www.healthit.gov/sra-tool-installation

# HHS Sample BAA provisions
curl -fsSL -o hhs_sample_baa.html \
  https://www.hhs.gov/hipaa/for-professionals/covered-entities/sample-business-associate-agreement-provisions/index.html

# NIST SP 800-66 Rev. 2 (2024)
curl -fsSL -o nist_800_66_r2.pdf \
  https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-66r2.pdf

# HHS Security Rule guidance
curl -fsSL https://www.hhs.gov/hipaa/for-professionals/security/guidance/index.html > /tmp/hhs_sec.html

# Paid HIPAA-specialized platforms (recipient supplies token)
export DRATA_API_KEY=<drata>
export VANTA_API_KEY=<vanta>
export COMPLIANCY_GROUP_API_KEY=<compliancy>
export ACCOUNTABLE_HQ_API_KEY=<accountablehq>
```

Auth notes:
- HHS SRA Tool: free, Windows-native (MS Excel + standalone .NET).
- Drata HIPAA, Vanta HIPAA: paid; HIPAA framework module included.
- Aptible: paid HIPAA-as-a-service hosting (HITRUST-adjacent).
- MedStack: paid containerized PHI platform.

## Common recipes

### Recipe 1: Determine your role

```text
Covered Entity (CE) — 45 CFR §160.103:
- Health plan (insurer, HMO, employer-sponsored plan over 50 EE, Medicare/Medicaid)
- Healthcare clearinghouse
- Healthcare provider that transmits health info electronically in standard
  HIPAA transactions (claims, eligibility, referrals)

Business Associate (BA):
- Creates, receives, maintains, OR transmits PHI on behalf of a CE for a
  function regulated by HIPAA.
- Includes subcontractors of BAs.
- Common BAs: cloud hosting (AWS, Azure, GCP), EHR vendors, claims
  processors, billing services, transcription, IT consultants, legal,
  attorneys handling PHI.

Hybrid Entity:
- Single legal entity with both HIPAA-covered and non-covered functions.
- Must designate the healthcare component.

Org self-test:
1. Do you provide healthcare services?
2. Do you transmit electronic transactions in standard HIPAA format?
3. Are you a health plan?
4. Are you a clearinghouse?
5. Do you process PHI on behalf of a CE under contract?

If 1+2 OR 3 OR 4 → CE. If 5 → BA. Both → both apply.
```

### Recipe 2: PHI vs ePHI vs de-identified

```text
PHI (Protected Health Information): individually identifiable health info
- Past / present / future physical or mental health
- Past / present / future payment for healthcare
- Identifiable to a specific individual

ePHI (electronic PHI): PHI in any electronic form

De-identified data — Safe Harbor (§164.514(b)(2)):
- Remove 18 specific identifiers (names, geographic <state, dates <year for
  most, phone, fax, email, SSN, MRN, account #, certificate/license #,
  vehicle ID, device ID, web URL, IP, biometric, face photo, other unique
  identifier).
- AND no actual knowledge of re-identification ability.

De-identified — Expert Determination (§164.514(b)(1)):
- Statistical expert certifies very small re-identification risk.
- Document the methodology.

Limited Data Set (§164.514(e)) — between PHI and de-identified:
- Removes 16 of 18 identifiers (keeps dates + geographic to state/zip).
- Use under Data Use Agreement.
```

### Recipe 3: Risk analysis methodology (NIST SP 800-66 r2)

```text
Step 1 — Identify scope of analysis (where does PHI live? flow? rest?)
Step 2 — Gather data (inventory systems, applications, devices, vendors,
         users with PHI access)
Step 3 — Identify + document potential threats + vulnerabilities
  - Natural (flood, fire, earthquake)
  - Human intentional (hacker, malicious insider, theft)
  - Human unintentional (user error, misconfiguration, lost device)
  - Environmental (power failure, HVAC, hardware failure)
Step 4 — Assess current security measures (existing controls + their
         effectiveness)
Step 5 — Determine likelihood of threat occurrence (Low / Medium / High)
Step 6 — Determine potential impact of threat occurrence (Low / Medium / High)
Step 7 — Determine level of risk (likelihood × impact matrix)
Step 8 — Identify security measures + finalize documentation
Step 9 — Periodic review + updates (annual + on material change)

Output:
- Risk Analysis Report (filed with security policies)
- Risk Management Plan (§164.308(a)(1)(ii)(B)) — addresses the risks
```

### Recipe 4: HHS SRA Tool walkthrough

```text
1. Download + install from healthit.gov.
2. Standalone version (recommended for small/mid orgs):
   - Create new assessment
   - Enter org demographics
   - 7 sections: Vendor + Tech mgmt, Risk mgmt, Compliance + workforce,
     Asset + facility, Operational mgmt, Communications, IS + Sec Aware
   - Each Q: Y/N/Partial + threats + vulnerabilities + likelihood + impact
3. Excel version (for larger orgs preferring spreadsheet):
   - Same questions in Excel workbook
4. Export risk analysis report (PDF).
5. Save assessment artifacts; revisit annually + on material change.

Note: SRA Tool is HHS-recommended but NOT mandatory. Larger orgs typically
use Vanta / Drata / Compliancy Group / Accountable HQ for automation.
```

### Recipe 5: Security Rule control map — Administrative §164.308

```text
§164.308(a)(1) Security Management Process
  (i) Standard: implement policies and procedures to prevent, detect,
      contain, correct security violations
  (ii)(A) REQUIRED: Risk Analysis
  (ii)(B) REQUIRED: Risk Management
  (ii)(C) REQUIRED: Sanction Policy
  (ii)(D) REQUIRED: Info System Activity Review

§164.308(a)(2) REQUIRED: Assigned Security Responsibility
§164.308(a)(3) Workforce Security
  (i) Standard
  (ii)(A) ADDRESSABLE: Authorization + Supervision
  (ii)(B) ADDRESSABLE: Workforce Clearance
  (ii)(C) ADDRESSABLE: Termination Procedures

§164.308(a)(4) Info Access Management
  (ii)(A) REQUIRED: Isolating Healthcare Clearinghouse (if applicable)
  (ii)(B) ADDRESSABLE: Access Authorization
  (ii)(C) ADDRESSABLE: Access Establishment + Modification

§164.308(a)(5) Security Awareness + Training
  (ii)(A) ADDRESSABLE: Security Reminders
  (ii)(B) ADDRESSABLE: Protection from Malicious Software
  (ii)(C) ADDRESSABLE: Log-in Monitoring
  (ii)(D) ADDRESSABLE: Password Management

§164.308(a)(6) Security Incident Procedures
  (ii) REQUIRED: Response + Reporting

§164.308(a)(7) Contingency Plan
  (ii)(A) REQUIRED: Data Backup Plan
  (ii)(B) REQUIRED: Disaster Recovery Plan
  (ii)(C) REQUIRED: Emergency Mode Operation Plan
  (ii)(D) ADDRESSABLE: Testing + Revision
  (ii)(E) ADDRESSABLE: Applications + Data Criticality Analysis

§164.308(a)(8) REQUIRED: Evaluation (periodic technical + non-technical
                evaluation)

§164.308(b) Business Associate Contracts
  (1) REQUIRED: written contract or other arrangement
  (4) REQUIRED: written confirmation
```

### Recipe 6: Security Rule — Physical §164.310

```text
§164.310(a) Facility Access Controls
  (ii)(A) ADDRESSABLE: Contingency Operations
  (ii)(B) ADDRESSABLE: Facility Security Plan
  (ii)(C) ADDRESSABLE: Access Control + Validation Procedures
  (ii)(D) ADDRESSABLE: Maintenance Records

§164.310(b) REQUIRED: Workstation Use
§164.310(c) REQUIRED: Workstation Security
§164.310(d) Device + Media Controls
  (ii)(A) REQUIRED: Disposal
  (ii)(B) REQUIRED: Media Re-use
  (ii)(C) ADDRESSABLE: Accountability
  (ii)(D) ADDRESSABLE: Data Backup + Storage
```

### Recipe 7: Security Rule — Technical §164.312

```text
§164.312(a) Access Control
  (i) Standard
  (ii)(A) REQUIRED: Unique User Identification
  (ii)(B) REQUIRED: Emergency Access Procedure
  (ii)(C) ADDRESSABLE: Automatic Logoff
  (ii)(D) ADDRESSABLE: Encryption + Decryption

§164.312(b) REQUIRED: Audit Controls
§164.312(c) Integrity
  (ii) ADDRESSABLE: Mechanism to Authenticate ePHI
§164.312(d) REQUIRED: Person/Entity Authentication
§164.312(e) Transmission Security
  (ii)(A) ADDRESSABLE: Integrity Controls
  (ii)(B) ADDRESSABLE: Encryption
```

### Recipe 8: "Addressable" vs "Required" distinction

```text
REQUIRED: Must implement as specified.

ADDRESSABLE: Org evaluates:
- Is the specification reasonable + appropriate for our environment? If yes,
  implement.
- If no, must:
  (a) Document why it's not reasonable + appropriate, AND
  (b) Implement equivalent alternative measure if reasonable + appropriate,
  OR
  (c) Document why no equivalent alternative is reasonable + appropriate.

Addressable is NOT optional. It's "implement OR document equivalent OR
document why neither." Auditors expect documented reasoning either way.
```

### Recipe 9: Business Associate Agreement (BAA) — required elements (§164.504(e))

```markdown
# Business Associate Agreement

**Covered Entity:** <Co.>
**Business Associate:** <Vendor>
**Effective date:** <YYYY-MM-DD>

## 1. Definitions
Adopt definitions from 45 CFR §§ 160.103, 164.103, 164.304, 164.501.

## 2. Permitted Uses + Disclosures (§164.504(e)(2)(i))
BA may use + disclose PHI ONLY as permitted by this BAA and as required for
the services described in <underlying service agreement>.

## 3. Required by Law
BA may disclose as required by law (§164.504(e)(2)(i)(B)).

## 4. Safeguards (§164.504(e)(2)(ii)(B))
BA will implement administrative, physical, technical safeguards reasonably
+ appropriately designed to prevent unauthorized use/disclosure of PHI per
§164.308, §164.310, §164.312, §164.316.

## 5. Reporting (§164.504(e)(2)(ii)(C))
BA will report:
- Use or disclosure not permitted by this BAA
- Security incident (§164.304)
- Breach of unsecured PHI per Subpart D (§164.410 — 60 days from discovery
  by BA)

## 6. Subcontractors (§164.504(e)(2)(ii)(D))
BA will ensure any subcontractor that creates, receives, maintains, or
transmits PHI on behalf of BA agrees in writing to the same restrictions and
conditions ("flow-down BAA").

## 7. Individual Rights Cooperation (§164.504(e)(2)(ii)(E)-(G))
BA will:
- Make PHI available for individual access (§164.524)
- Make PHI available for amendment (§164.526)
- Provide accounting of disclosures (§164.528)

## 8. CE Compliance (§164.504(e)(2)(ii)(H))
BA will make internal practices, books, records available to HHS Secretary
for compliance determination.

## 9. Return / Destruction (§164.504(e)(2)(ii)(I))
Upon termination, BA will return or destroy all PHI (and ensure any sub-BA
does the same). If infeasible, extend protections + limit further uses.

## 10. Termination for Cause (§164.504(e)(2)(iii))
CE may terminate if BA materially breaches; provide cure period or
immediate termination if cure impossible.

## 11. Survival
Sections 5, 6, 9 survive termination.

---
*Disclaimer per template.*
```

### Recipe 10: 60-day breach notification (Subpart D — §§164.400-414)

```text
Breach (§164.402):
- Acquisition, access, use, disclosure of unsecured PHI not permitted
- Presumed breach UNLESS low-probability of compromise per 4-factor risk
  assessment:
  (1) Nature + extent of PHI (identifiers, severity)
  (2) Unauthorized recipient (who got it; trust level)
  (3) Whether PHI was actually acquired/viewed
  (4) Mitigation extent (e.g., recovered + confirmed not shared)

Unsecured PHI: not rendered unusable, unreadable, indecipherable to
unauthorized persons. Encryption + destruction = "secured" per HHS guidance.

Notification timelines:
- Individuals: 60 days from DISCOVERY by CE (§164.404)
- Media: if 500+ in a state, prominent media within 60 days (§164.406)
- HHS: 
  - 500+: 60 days, online portal (§164.408(b))
  - <500: annual summary by Feb 60 days after year end (§164.408(c))
- Business Associate to CE: 60 days from discovery (§164.410)

Notice contents (§164.404(c)):
- What happened + when
- Types of PHI involved
- Steps individuals should take
- What CE is doing
- Contact info

Civil penalties (HITECH tiered):
- Tier 1 (Did not know): $137-$68,928 per violation; $2,067,813 annual cap
- Tier 2 (Reasonable cause): $1,379-$68,928; $2M cap
- Tier 3 (Willful neglect, corrected): $13,785-$68,928; $2M cap
- Tier 4 (Willful neglect, not corrected): $68,928-$2,067,813; $2M cap
(2024 adjusted annual caps; re-check annually)
```

### Recipe 11: Encryption for "secured" PHI (per HHS guidance)

```text
HHS Guidance: "secured" = rendered unusable, unreadable, indecipherable.

Acceptable methods:
- Data at rest: AES with key ≥128-bit (NIST SP 800-111). AES-256 standard.
- Data in motion: TLS 1.2+ per NIST SP 800-52 r2. TLS 1.3 preferred.
- Data destruction: NIST SP 800-88 r1 media sanitization (Clear / Purge /
  Destroy).

Use of encryption = "safe harbor" — encrypted PHI breach = no notification
required (provided key not also breached).

KMS / HSM:
- AWS KMS, GCP KMS, Azure Key Vault, HashiCorp Vault.
- Customer-managed keys (CMK) preferred for BAAs.
```

### Recipe 12: HITECH overlay (2009 + Omnibus 2013)

```text
Direct BA liability — HITECH made BAs directly liable for Security Rule +
some Privacy Rule provisions. Pre-HITECH, BAs were only contractually
liable to CE.

Sub-BA flow-down — Subcontractors of BAs are BAs themselves. BAA flow-down
mandatory.

Breach notification — HITECH codified breach rule (then Omnibus refined
2013).

Enhanced penalties (tiered).

Audit program — HHS OCR conducts audits (Phase 1 + 2 + 3).

EHR + Meaningful Use — separate but referenced.
```

## Examples

### Example 1: New BA onboarding for healthtech startup

**Goal:** Stand up HIPAA-compliant SaaS, sign BAAs with sub-processors, launch.

**Steps:**
1. Determine role: BA (processing PHI for CE customers).
2. Risk analysis per Recipe 3 + 4 (HHS SRA Tool).
3. Implement controls per Recipes 5-7.
4. Identify sub-processors handling PHI: AWS, Datadog, Stripe (if accepting copay).
5. Execute BAA with each sub-processor (AWS BAA standard, Datadog has BAA, Stripe doesn't typically).
6. Author customer-facing BAA template (Recipe 9).
7. Document encryption per Recipe 11.
8. Author IR playbook (`incident-response-nist-sp-800-61`) + breach notification matrix (`breach-notification-gdpr-72hr-state-laws`).

**Result:** Production-ready PHI environment; signable BAA for customer asks.

### Example 2: Annual HIPAA risk analysis refresh

**Goal:** Refresh §164.308(a)(1)(ii)(A) risk analysis per annual cadence.

**Steps:**
1. Reload prior risk analysis.
2. Inventory changes since last RA (new systems, new vendors, new staff, new processing).
3. SRA Tool: walk through 7 sections.
4. Update threats + vulnerabilities; re-score likelihood × impact.
5. Update Risk Management Plan with new corrective actions.
6. Senior management review + sign-off.
7. File RA report; calendar for next year.

**Result:** Current RA on file; defensible in HHS OCR audit.

### Example 3: PHI breach decision + notification

**Goal:** Employee emailed PHI to wrong recipient. Decide notification.

**Steps:**
1. Discover: 2026-06-10.
2. 4-factor risk assessment (Recipe 10):
   - Nature: name + DOB + Dx (Tier 2 sensitive).
   - Recipient: another internal employee (trusted; within workforce).
   - Acquired/viewed: recipient confirms email opened; subject scanned.
   - Mitigation: recipient deletes; certifies destruction.
3. Conclusion: low probability of compromise. NOT a breach per §164.402.
4. Document determination + retain for 6 years.
5. Update sanction policy + train sender on minimum-necessary.

**Result:** Documented non-breach; corrective action; no public notification required.

## Edge cases / gotchas

- **Addressable ≠ optional.** Addressable specs require documented reasoning either way. Auditors penalize undocumented "we didn't think it applied."
- **Workforce includes contractors + volunteers + interns**, not just employees.
- **Hybrid entities require careful designation.** Healthcare component must be documented; non-healthcare component still subject to other laws.
- **State law preemption** — HIPAA preempts conflicting state law UNLESS state law is more stringent. California CMIA, NY SHIELD, MA 201 CMR 17 can layer additional requirements.
- **Texting PHI is NOT inherently HIPAA-compliant.** Standard SMS is unencrypted. Encrypted messaging (Signal, OhMD, TigerText) or secure portals required.
- **Email is not "secured" by default.** Use TLS-enforced delivery (Office 365 / Workspace can enforce) or encrypted email gateways.
- **De-identification is a high bar.** Safe Harbor's 18-identifier removal is strict; expert determination requires statistician.
- **AWS / GCP / Azure BAA scope.** Only AWS services listed on the AWS HIPAA Eligible Services list are in scope of AWS BAA. Using non-eligible service for PHI = violation.
- **OCR audit + enforcement.** OCR conducts random + complaint-driven audits. 2024+ enforcement has emphasized risk analysis adequacy and patch management.
- **Substance use disorder (42 CFR Part 2)** is stricter than HIPAA for SUD treatment records. Separate consent rules.
- **HIPAA penalties cap per category per year** ($2M+ as of 2024). Multiple categories possible.
- **Right of access requests** — patient access requests under §164.524 are a top OCR enforcement area. 30-day response.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [HHS HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/index.html)
- [HHS Security Rule Guidance](https://www.hhs.gov/hipaa/for-professionals/security/guidance/index.html)
- [HHS Sample BAA Provisions](https://www.hhs.gov/hipaa/for-professionals/covered-entities/sample-business-associate-agreement-provisions/index.html)
- [NIST SP 800-66 Rev. 2 (2024)](https://csrc.nist.gov/pubs/sp/800/66/r2/final)
- [HHS HealthIT SRA Tool](https://www.healthit.gov/topic/privacy-security-and-hipaa/security-risk-assessment-tool)
- [HHS Breach Notification Rule](https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html)
- [HHS Breach Portal](https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf)
- [AWS HIPAA Eligible Services](https://aws.amazon.com/compliance/hipaa-eligible-services-reference/)
- [GCP HIPAA Compliance](https://cloud.google.com/security/compliance/hipaa)
- [Azure HIPAA / HITRUST](https://learn.microsoft.com/en-us/azure/compliance/offerings/offering-hipaa-us)
- [Drata HIPAA](https://drata.com/hipaa)
- [Vanta HIPAA](https://www.vanta.com/products/hipaa)
- [Compliancy Group](https://compliancy-group.com/)
- [Accountable HQ](https://accountablehq.com/)
- [Aptible (HITRUST + HIPAA hosting)](https://www.aptible.com/)
- [MedStack](https://medstack.co/)
