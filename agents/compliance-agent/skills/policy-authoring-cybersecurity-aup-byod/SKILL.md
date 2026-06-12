---
name: policy-authoring-cybersecurity-aup-byod
description: Author the SOC 2 + ISO 27001 + HIPAA + PCI baseline policy library — Information Security, Access Control, Change Management, Incident Response, BCP/DR, Vendor Management, Acceptable Use, Data Classification, Cryptography, Asset Management, Risk Management, BYOD, Remote Work, AI Acceptable Use (NEW 2024+), Whistleblower / Code of Conduct, Privacy / Data Protection. Free templates from SANS + CIS + Vanta/Drata sample libraries. Manage via PowerDMS / NAVEX PolicyTech / in-platform.
---

# Policy Authoring — Cybersecurity + AUP + BYOD + AI Use + Remote

Author the full policy library baseline required by SOC 2 + ISO 27001 + HIPAA + PCI DSS + GDPR. Free templates: SANS Information Security Policy Project + CIS Policy Templates + Vanta / Drata / Secureframe libraries. Management: PowerDMS, NAVEX PolicyTech, ComplianceBridge.

## When to use

User says:
- "Policy library" / "policy authoring"
- "Information Security Policy" / "AUP" / "BYOD" / "Remote Work"
- "AI Use policy" / "GenAI policy"
- "Cryptography policy" / "Access Control policy"
- "Policy management" / "PolicyTech" / "PowerDMS"
- "Sample policy templates" / "SANS templates" / "CIS templates"
- "Code of Conduct" / "Whistleblower"

Companion skills: `drata-vanta-secureframe-soc2-monitoring`, `iso-27001-isms-readiness`, `whistleblower-program-navex-ethicspoint`.

## Setup

```bash
# SANS Information Security Policy Project (free templates)
curl -fsSL https://www.sans.org/information-security-policy/ > /tmp/sans.html

# CIS Policy Templates (free)
curl -fsSL https://www.cisecurity.org/insights/white-papers/cis-security-policy-templates > /tmp/cis.html

# Vanta sample library (with paid acct)
# Drata sample library (with paid acct)
# Secureframe sample library (with paid acct)

# Policy management platforms
# https://www.powerdms.com/
# https://www.navex.com/en-us/products/policy/
# https://www.compliancebridge.com/
```

## Common recipes

### Recipe 1: Required policy library (compliance baseline)

```text
SOC 2 + ISO 27001 baseline (14-20 policies minimum):

1.  Information Security Policy (master)
2.  Acceptable Use Policy (AUP)
3.  Access Control Policy
4.  Change Management Policy
5.  Incident Response Policy
6.  Business Continuity + Disaster Recovery Policy
7.  Vendor Management / TPRM Policy
8.  Data Classification Policy
9.  Cryptography Policy
10. Asset Management Policy
11. Risk Management Policy
12. Vulnerability Management Policy
13. Awareness + Training Policy
14. Backup + Recovery Policy
15. BYOD Policy
16. Remote Work Policy
17. AI Use Policy (NEW 2024+)
18. Code of Conduct / Whistleblower
19. Privacy / Data Protection Policy
20. Physical Security Policy (or noted N/A for fully remote)

HIPAA-specific:
- Privacy Policy (covered entity)
- HIPAA Security Policies (admin, physical, technical)
- Sanctions Policy
- BAA Management Policy

PCI DSS-specific:
- Cardholder Data Handling Policy
- Network Security Controls Policy

GDPR-specific:
- DSAR / DSR Handling Procedure
- ROPA Maintenance Procedure
- DPIA Procedure
- Breach Notification Procedure
- Sub-processor Management Procedure

Sector-specific:
- AML Program (BSA/MSB)
- Trading + Personal Account Dealing (broker-dealer)
- Records Retention (sector-specific)
- Anti-Bribery + Corruption (FCPA/UKBA)
```

### Recipe 2: Policy structure (template skeleton)

```markdown
# <Policy Name>

**Document ID:** POL-001
**Version:** 1.0
**Approved by:** <Owner / Exec Sponsor>
**Effective date:** <YYYY-MM-DD>
**Next review:** <YYYY-MM-DD (annual)>
**Owner:** <Function — e.g. CISO>
**Scope:** All employees, contractors, third parties accessing <Co.>
systems and data.

## 1. Purpose
<Why this policy exists. Reference frameworks: SOC 2 CC<X.X>, ISO 27001
A.<X.X>, HIPAA §<X>, PCI DSS Req. <X>, GDPR Art. <X>.>

## 2. Scope
<Systems, locations, roles in scope. Exclusions noted.>

## 3. Definitions
<Terms used; align with framework definitions.>

## 4. Policy
<Imperatives — "Employees MUST do X." "X SHALL NOT be Y." Avoid weak
language like "should" unless intentional.>

### 4.1 <Subsection>
### 4.2 <Subsection>

## 5. Roles + Responsibilities
- Owner: <named role + accountabilities>
- Custodian / Operator: <role>
- All staff: <baseline behaviors>

## 6. Compliance + Enforcement
<Consequences of violation; escalation; HR involvement.>

## 7. Exceptions
<Exception process — written request, approver, time-bound, registered in
exception registry.>

## 8. Related documents
<Linked policies, procedures, standards, guidelines.>

## 9. Revision history
| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | <date> | <name> | Initial |

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

### Recipe 3: Acceptable Use Policy (AUP) template

```markdown
# Acceptable Use Policy

## 1. Purpose
Govern appropriate use of <Co.> information systems + data.

## 2. Scope
Employees, contractors, interns, third parties accessing <Co.> systems.

## 3. Policy

### 3.1 Authorized use
Use of <Co.> systems is restricted to legitimate business purposes.
Incidental personal use is permitted IF it does not interfere with work,
violate other policies, consume material resources, or expose <Co.> to
risk.

### 3.2 Prohibited use
The following are prohibited:
- Sharing credentials with anyone (including coworkers, family, vendors)
- Connecting unauthorized devices to <Co.> networks
- Installing unauthorized software
- Bypassing security controls (VPN, MFA, firewall)
- Accessing data not required for role
- Disclosing confidential information without authorization
- Using <Co.> systems for illegal activity, harassment, hate speech, or
  pornography
- Personal cryptocurrency mining
- Personal commercial activity

### 3.3 Email + communications
- All email is subject to filtering + archive
- No expectation of privacy on <Co.> systems
- Personal accounts (Gmail, etc.) must not be used for <Co.> business
- Auto-forwarding to external accounts is prohibited

### 3.4 Internet use
- Web filtering is in effect
- Bypass via personal VPN is prohibited

### 3.5 Mobile devices + BYOD
See BYOD Policy.

### 3.6 Remote work
See Remote Work Policy.

### 3.7 AI / GenAI use
See AI Use Policy.

### 3.8 Social media
- Personal social media use must not represent <Co.>
- Confidential information must not be disclosed
- Disclaimers required when posting about <Co.> matters

### 3.9 Software + intellectual property
- Use only licensed software
- IP created in scope of employment belongs to <Co.>
- Open source use per Open Source Policy (if applicable)

### 3.10 Reporting violations
Report to <Sec / HR / Legal>. Non-retaliation policy applies.

## 4. Enforcement
Violations may result in disciplinary action up to termination + civil /
criminal action.

## 5. Acknowledgment
All employees must acknowledge this policy annually + on policy change.

---
*Disclaimer per template.*
```

### Recipe 4: BYOD Policy template

```markdown
# Bring Your Own Device (BYOD) Policy

## 1. Purpose
Govern use of personal devices to access <Co.> resources.

## 2. Scope
All personal devices (laptop, tablet, smartphone) used for <Co.> work.

## 3. Eligibility
- All employees may use BYOD for email + calendar + chat.
- Privileged users (Eng with prod access, Finance with sensitive data)
  must use <Co.>-issued devices.

## 4. Requirements

### 4.1 Enrollment
- Device must be enrolled in <MDM — Jamf / Intune / Kandji / WS1>
- <Co.> reserves right to remote-wipe enrolled device
- Removal from MDM = removal of <Co.> data access

### 4.2 Device hygiene
- Up-to-date OS + apps
- Full-disk encryption enabled
- Screen lock + biometric or strong PIN
- Find-My / device tracking enabled
- No jailbreak / root

### 4.3 Application separation
- <Co.> data accessed via approved apps only (Office Mobile, Outlook,
  Workspace mobile, Slack, etc.)
- No copy-paste from work to personal apps (MAM controls)
- No screenshot of confidential content
- Public cloud personal accounts may NOT store work data

### 4.4 Lost / stolen
Report immediately to <Sec> for remote wipe.

### 4.5 Departure
- Confirm remote wipe / device de-enrollment.

## 5. Reimbursement
<Per HR — phone stipend / data plan / etc.>

## 6. Privacy
<Co.> may access metadata + apply MAM/MDM controls; cannot access
personal data on device.

---
*Disclaimer per template.*
```

### Recipe 5: AI Use Policy template (NEW 2024+)

```markdown
# AI / Generative AI Acceptable Use Policy

## 1. Purpose
Govern employee use of generative AI tools (LLMs, image gen, voice gen)
in business context.

## 2. Scope
All employees + contractors + third parties using GenAI on behalf of
<Co.>.

## 3. Approved tools
The following tools have been reviewed for security + privacy + DPA:
- <ChatGPT Team / Claude for Work / Gemini Workspace / M365 Copilot / 
  vendor-specific list>

Unsanctioned tools (consumer ChatGPT, public Claude, unknown LLM) ARE
PROHIBITED for handling <Co.> data.

## 4. Data classification rules
- PUBLIC data: OK in any approved tool
- INTERNAL data: OK in approved tools with enterprise tier
- CONFIDENTIAL data: only in approved tools with DPA + no-training
- RESTRICTED data (PII, PHI, PCI, source code): NEVER use in any GenAI

## 5. Use guidelines
- Verify output before relying (LLM hallucination risk)
- Cite source for factual claims
- Don't represent AI-generated content as solely human-created
- Don't auto-publish without review
- Customer-facing AI features: user notice required
- Training data submission to vendor: must opt-out

## 6. Customer + third-party content
- Don't paste customer-shared docs without consent
- Don't use AI to analyze sensitive third-party docs
- Respect IP + copyright

## 7. Code generation
- AI-suggested code requires human review
- Don't blindly trust security claims of AI suggestions
- License compatibility check for AI-derived code

## 8. Prohibited uses
- Generating misleading content (synthetic CEO speech, deceptive imagery)
- Bypassing identity verification with AI synthesis
- Mass-personalized phishing or social engineering
- Replacing required human judgment in HR, hiring, performance, legal
- Decisions with legal or significant effects on persons without human
  oversight (GDPR Art. 22 + EU AI Act)

## 9. Compliance + audit
- AI tool use is logged + reviewed
- Annual training required

## 10. Reporting concerns
<Sec / Privacy / Manager>. Non-retaliation.

---
*Disclaimer per template.*
```

### Recipe 6: Remote Work Policy template

```markdown
# Remote Work Policy

## 1. Purpose
Govern security + productivity expectations for remote work.

## 2. Scope
Employees working from home or any non-office location.

## 3. Workspace
- Private workspace with door (for confidential calls)
- Secure storage for physical documents
- No work documents visible to others

## 4. Network
- Home Wi-Fi must be encrypted (WPA2/3); change default password
- Use of <Co.>-provided VPN for any production access
- Public Wi-Fi prohibited unless VPN-tunneled
- Hotspot from personal phone preferred over hotel/coffee shop Wi-Fi

## 5. Device
- <Co.>-issued device preferred for production access
- BYOD per BYOD Policy

## 6. Shared spaces
- Coffee shops: screen privacy filter; no confidential calls overheard
- Coworking: tag confidential calls in private booth
- Travel: avoid airport / hotel lobby work on confidential

## 7. International travel
- 30-day work-from-X policy: notify HR + IT + Tax
- Notify Sec for country-restricted (sanctions, surveillance)
- VPN config + travel device per IT

## 8. Hours + availability
Per individual employment agreement.

## 9. Equipment
<Co.> provides + reimburses per equipment policy.

---
*Disclaimer per template.*
```

### Recipe 7: Cryptography Policy template

```markdown
# Cryptography Policy

## 1. Purpose
Establish requirements for cryptographic use of <Co.> data.

## 2. Scope
All <Co.> data at rest and in transit.

## 3. Standards

### 3.1 At rest
- AES-256-GCM minimum
- Database (Postgres, MySQL, Snowflake, BigQuery): customer-managed key
  (CMK) preferred
- Object storage (S3, GCS, Azure Blob): SSE-KMS with rotation
- File-system: BitLocker (Windows), FileVault (macOS), LUKS (Linux)

### 3.2 In transit
- TLS 1.2 minimum (TLS 1.3 preferred)
- HSTS enabled
- Mutual TLS for service-to-service
- Modern cipher suites per Mozilla Modern Server-Side TLS
- Deprecated: SSL 2/3, TLS 1.0/1.1, RC4, MD5, SHA-1

### 3.3 Key management
- Generation: NIST SP 800-133-compliant RBG
- Storage: HSM or KMS (AWS KMS / GCP KMS / Azure Key Vault / HashiCorp Vault)
- Rotation: annual; on compromise; on personnel change
- Backup: encrypted offsite

### 3.4 Hashing
- Passwords: argon2 / bcrypt with cost >= 12 / scrypt
- Files: SHA-256+
- HMAC for integrity: HMAC-SHA-256+

### 3.5 Random numbers
- /dev/urandom (Linux), CryptGenRandom (Windows), SecureRandom (Java),
  secrets module (Python)

## 4. Approved algorithms
Per NIST SP 800-131A Rev. 2.

## 5. Post-quantum cryptography
- Monitor NIST PQC standardization (CRYSTALS-Kyber, CRYSTALS-Dilithium)
- Pilot hybrid (classical + PQC) per NIST IR 8413 + 8454

## 6. Compliance
- Annual key rotation evidence
- HSM / KMS access reviewed quarterly

---
*Disclaimer per template.*
```

### Recipe 8: Free template sources

```text
SANS Information Security Policy Project (free):
- https://www.sans.org/information-security-policy/
- 30+ free templates: Acceptable Encryption, Acceptable Use, Anti-Virus,
  Audit Vulnerability Scanning, Automatically Forwarded Email, BYOD,
  Clean Desk, Dial-In Access, etc.

CIS Policy Templates (free):
- https://www.cisecurity.org/insights/white-papers/cis-security-policy-templates
- 22 templates aligned to CIS Controls v8

NIST Cybersecurity Framework (free reference):
- https://www.nist.gov/cyberframework
- Map policies to CSF 2.0 functions

ISACA: paid templates
ISO 27002:2022: paid; control implementation guidance

Drata / Vanta / Secureframe sample libraries:
- Available to paid tenants; customize don't copy
```

### Recipe 9: Policy review + update cycle

```text
Annual mandatory review (most policies).
Trigger-based interim updates:
- Regulatory change (e.g., GDPR enforcement guidance, new EU AI Act
  obligations)
- Material control change
- Incident lessons-learned
- Audit finding
- M&A / org change

Workflow:
1. Owner reviews policy.
2. Updates drafted with redline.
3. Stakeholder consultation.
4. Exec / Owner approval.
5. New version published.
6. All-staff communication + attestation.
7. Filing in policy mgmt platform.
```

### Recipe 10: Attestation tracking

```text
Required by SOC 2 + ISO + HIPAA + PCI:

Annual attestation:
- New hire: 30 days from start
- Annual refresh: every 12 months (rolling)
- Policy change: 30 days from publication
- Re-acknowledge: on major version change (vs minor)

Track per user:
- Policy ID + version
- Acknowledgment timestamp
- IP + device

Platforms: PowerDMS, NAVEX PolicyTech, Vanta / Drata / Secureframe built-in.

LMS-style cadence — attach to security awareness training cycle.
```

### Recipe 11: PowerDMS workflow

```text
PowerDMS — most popular standalone policy mgmt for SMB / mid-market.

Features:
- Versioning + redline tracking
- Approval workflow
- Distribution + attestation
- Sign-in audit logging
- Mobile access for field workers
- Integration with Drata / Vanta

Typical workflow:
1. Owner drafts in PowerDMS editor.
2. Routed to stakeholders for review.
3. Approver signs off.
4. Published; distribution to specified group.
5. Recipients acknowledge; PowerDMS logs.
6. Periodic reminder for non-attested.
```

### Recipe 12: NAVEX PolicyTech / EthicsPoint integration

```text
NAVEX PolicyTech + EthicsPoint integrated for orgs needing combined
policy + whistleblower.

Features:
- Policy + procedure library
- Whistleblower hotline (EthicsPoint)
- Case management
- EU Whistleblower Directive 2019/1937 compliance
- Multi-language + multi-jurisdiction
```

### Recipe 13: Vanta / Drata / Secureframe policy module

```text
All three platforms ship a policy library + attestation tracking.

Pros:
- Auto-mapped to controls
- Auto-collected attestation evidence for audit
- Update notifications when framework changes
- Free template starting point

Cons:
- Templates need customization (don't ship as-is)
- Less feature depth vs PowerDMS / NAVEX
- Vendor lock-in

For SMB starting SOC 2 / ISO journey: use Vanta / Drata / Secureframe.
For complex multi-policy + procedure orgs: PowerDMS or NAVEX.
```

## Examples

### Example 1: Stand up SOC 2 policy library

**Goal:** 14 policies for SOC 2 Type II in 30 days.

**Steps:**
1. Use Drata policy library as starting point.
2. Customize per Recipe 2 structure.
3. Adapt SANS + CIS templates.
4. Stakeholder review + Exec approval.
5. Publish + attestation.
6. Annual review calendar.

**Result:** SOC 2 CC1 / CC5 / CC9 policy evidence ready.

### Example 2: Add AI Use policy

**Goal:** Roll out GenAI policy in 14 days.

**Steps:**
1. Draft per Recipe 5.
2. Stakeholder consult: Eng, Product, Legal, Sec.
3. Define approved tools (Claude for Work + M365 Copilot).
4. Exec approval.
5. All-staff training (`security-awareness-training-knowbe4-hoxhunt`).
6. Attestation tracking.

**Result:** AI Use policy + training operational.

### Example 3: Annual policy review sprint

**Goal:** Review + update all 18 policies in Q4.

**Steps:**
1. Calendar 18 weeks (1 per week) for owner review.
2. Track in spreadsheet: policy + last review + current owner.
3. Redline + stakeholder consult.
4. Republish per cadence.
5. Re-attest for major version changes.
6. Drata / Vanta evidence pulled.

**Result:** Auditable annual review.

## Edge cases / gotchas

- **Policy ≠ procedure.** Policy = "what + why"; procedure = "how + by whom"; standard = "specific requirement"; guideline = "recommended practice."
- **Don't copy templates verbatim.** Customize to actual practice; auditors find mismatches.
- **Weak language traps.** "Should" reduces enforceability; use "must / shall" for required.
- **Multi-jurisdiction (EU + US + APAC).** Some policies require region variations.
- **Translations:** legal review of translations is mandatory for binding policies.
- **Attestation can be performative.** Reinforce with quiz + training.
- **Exception registry must be maintained.** Auditors check exception list + justifications.
- **Annual review cadence is mandatory for SOC 2 + ISO.** Track + audit.
- **Document control (Clause 7.5 ISO).** Version + approval + retention non-negotiable.
- **Sample library ≠ compliance.** Vanta / Drata templates need adaptation.
- **GDPR Privacy Policy ≠ Privacy Notice.** Internal policy (for employees) + external notice (for data subjects) are different docs.
- **Code of Conduct must reflect actual culture.** Misalignment surfaces in whistleblower complaints.
- **AI Use policy needs frequent refresh** as approved tools list evolves quarterly in 2026.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [SANS Information Security Policy Project](https://www.sans.org/information-security-policy/)
- [CIS Security Policy Templates](https://www.cisecurity.org/insights/white-papers/cis-security-policy-templates)
- [NIST CSF 2.0](https://www.nist.gov/cyberframework)
- [NIST SP 800-53 Rev. 5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- [NIST SP 800-131A Rev. 2 (Crypto)](https://csrc.nist.gov/pubs/sp/800/131/a/r2/final)
- [Mozilla Server-Side TLS](https://wiki.mozilla.org/Security/Server_Side_TLS)
- [PowerDMS](https://www.powerdms.com/)
- [NAVEX PolicyTech](https://www.navex.com/en-us/products/policy/)
- [ComplianceBridge](https://www.compliancebridge.com/)
- [ISACA Policy Resources](https://www.isaca.org/)
- [ISO/IEC 27002:2022 (Controls)](https://www.iso.org/standard/75652.html)
- [GDPR Art. 24 (Controller responsibilities)](https://gdpr-info.eu/art-24-gdpr/)
