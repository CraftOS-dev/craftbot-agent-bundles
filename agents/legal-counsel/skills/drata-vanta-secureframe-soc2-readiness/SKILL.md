---
name: drata-vanta-secureframe-soc2-readiness
description: Prepare for SOC 2 Type I + II audits via Drata, Vanta, or SecureFrame. Map AICPA TSP 100 Trust Services Criteria, set up automated evidence collection across cloud + identity + code + ticketing, pick the right auditor, and bridge between Type II periods. Output is a gap-analysis + remediation plan with the consult-an-attorney disclaimer.
---

# SOC 2 Readiness — Drata / Vanta / SecureFrame

SOC 2 is the de facto B2B SaaS security audit standard in 2026. Drata / Vanta / SecureFrame are the three dominant automation platforms.

## When to use

User says:

- "Prep for SOC 2"
- "We need a SOC 2 report for an enterprise deal"
- "Drata / Vanta / SecureFrame setup"
- "Type I vs Type II?"
- "What controls do we need?"
- "Pick a SOC 2 auditor"
- "Bridge letter"
- "Remediate SOC 2 findings"

Companion skills:
- `gdpr-readiness-audit` — separate GDPR audit.
- `ccpa-cpra-readiness-audit` — separate CCPA audit.

## Setup

```bash
# Drata
# https://drata.com/
# Tiers: starts ~$7,500/year (Foundations) → enterprise quote
# Sign up + connect first integration in 10 min

# Vanta
# https://www.vanta.com/
# Tiers: ~$8,000/year starter → enterprise quote

# SecureFrame
# https://secureframe.com/
# Tiers: starts ~$7,500/year → enterprise quote

# All three: REST APIs for automated evidence collection
export DRATA_API_KEY=<dashboard>
export VANTA_API_KEY=<dashboard>
export SECUREFRAME_API_KEY=<dashboard>

# AICPA Trust Services Criteria
curl -fsSL -o aicpa_tsp.pdf https://us.aicpa.org/content/dam/aicpa/interestareas/frc/assuranceadvisoryservices/downloadabledocuments/trust-services-criteria.pdf
```

## Common recipes

### Recipe 1: Pick Type I vs Type II
```text
Type I (point-in-time):
- 1-3 month prep
- Auditor verifies design of controls AS OF a date
- $5k-15k audit fee
- Useful for: first SOC 2, faster signal to customers
- LIMITED enterprise sales signal (many enterprises require Type II)

Type II (observation period):
- 3-12 month observation window (6 months most common first-time)
- Auditor verifies design AND operating effectiveness over the window
- $15k-50k audit fee
- REQUIRED by most enterprise customers
- Annual renewal expected; bridge letters between periods
```

### Recipe 2: Pick Trust Services Criteria
```text
TSP 100 (AICPA):

Security (Common Criteria — MANDATORY):
- Control environment
- Communication + information
- Risk assessment
- Monitoring activities
- Control activities
- Logical + physical access
- System operations
- Change management
- Risk mitigation

Availability (optional):
- Uptime + performance + capacity

Confidentiality (optional):
- Designated confidential info handling
- (Required if you handle customer-confidential data — most B2B SaaS)

Processing Integrity (optional):
- Accuracy of processing (financial / transactional)

Privacy (optional):
- PII handling per AICPA Privacy Framework
- (Often skipped because GDPR/CCPA covers it)

Default scoping for B2B SaaS: Security + Availability + Confidentiality.
```

### Recipe 3: Drata setup (typical)
```text
1. Sign up at https://drata.com → free trial / paid tier.
2. Connect integrations:
   - Cloud: AWS / GCP / Azure (IAM, EC2, S3 buckets, security groups)
   - Identity: Okta / JumpCloud / Google Workspace / Azure AD
   - Code: GitHub / GitLab / Bitbucket
   - Ticketing: Jira / Linear / Asana
   - HR: BambooHR / Rippling / Gusto
   - Endpoint: Kandji / Jamf / Intune / Drata Agent
   - Background check: Checkr / Drata-integrated
   - Security tools: Snyk / Datadog / PagerDuty / SentinelOne
3. Drata auto-collects evidence per control.
4. Drata's policy library: customize 25-30 policies (security, access, change mgmt, IR, BCP, vendor mgmt, AUP, classification).
5. Assign owners + due dates for each control.
6. Drata dashboard shows real-time readiness %.
```

### Recipe 4: Vanta setup (typical)
```text
1. Sign up at https://vanta.com.
2. Connect integrations (100+ pre-built: AWS, GCP, GitHub, Okta, etc.).
3. Vanta's control library — assign owners.
4. Policy templates — customize.
5. Continuous monitoring auto-flags drift.
6. Vanta's "Trust Center" page for public-facing customer questions.
```

### Recipe 5: SecureFrame setup
```text
Similar workflow to Drata / Vanta.
Strength: simpler UX for first-time SOC 2.
Weakness: smaller integration catalog vs Drata.
```

### Recipe 6: Critical control areas (cross-platform)
| Control area | Examples | Automation? |
|---|---|---|
| Access management | MFA enabled all employees; quarterly access reviews; offboarding within 24 hours | Drata / Vanta integration |
| Encryption | TLS 1.2+ in transit; AES-256 at rest; KMS-managed keys | Cloud config check |
| Vulnerability mgmt | Scan + patch SLA; pen-test annual | Snyk / Dependabot |
| Logging + monitoring | Audit logs 1-year retention; SIEM | Datadog / CloudTrail |
| Change management | PRs require review; production deploys gated | GitHub branch protection |
| Incident response | IR runbook; on-call rotation; post-mortems | PagerDuty / Linear |
| Backup + recovery | RTO/RPO defined; tested annually | Cloud snapshot policy |
| Vendor management | DPAs + SOC 2 reports for each vendor; risk score | Drata vendor module |
| HR + background | Background check before hire; security awareness training | Checkr / Drata |
| Risk assessment | Annual + on material change | Drata risk module |
| Business continuity | BCP / DR plan; tested annually | Document + tabletop |
| Physical security | If on-prem: data center SOC 2 inheritance; locked office | Cloud → inherit from AWS / GCP |

### Recipe 7: Pick an auditor
```text
AICPA-registered CPA firm with cyber/IT audit practice. 2026 common picks:

Mid-market firms (most startups):
- Schellman & Company — well-known SOC 2 specialist
- A-LIGN — broad compliance practice
- Coalfire — security-focused
- Prescient Assurance — fast-turnaround for SaaS
- BARR Advisory — smaller boutique
- Strike Graph — bundle audit + automation

Big Four:
- Deloitte / PwC / EY / KPMG — for larger orgs; pricier

Drata / Vanta / SecureFrame all have auditor marketplaces with intro pricing.
```

### Recipe 8: Type I → Type II progression
```text
Year 1 timeline (typical):
- Month 0: Pick platform (Drata/Vanta/SecureFrame); start setup
- Month 1-3: Connect integrations, customize policies, remediate gaps
- Month 4: Type I audit (point-in-time)
- Month 5-10: Type II observation window (6 months)
- Month 11: Type II audit
- Month 12: Type II report delivered

Annual renewal:
- 12-month Type II observation window (continuous)
- Bridge letter from auditor for sales 1-2 months between report periods
```

### Recipe 9: API — Drata sample (pull control status)
```bash
# https://developers.drata.com
curl -X GET https://public-api.drata.com/v1/controls \
  -H "Authorization: Bearer $DRATA_API_KEY" \
  -H "Accept: application/json"
```

### Recipe 10: Bridge letter request
```text
For sales teams:
"Type II report from <date> to <date>; current Type II in progress through <date>."

Auditor issues bridge letter on request (~$500-1000) — covers gap between report periods. Provides ongoing assurance to customer prospects.
```

### Recipe 11: Vendor sub-processor risk reviews
```text
For each vendor handling customer data:
1. Request their SOC 2 report (Type II preferred).
2. Confirm scope covers your use case.
3. Check for "carve-outs" — subservice organizations.
4. Review their CUEC (Complementary User Entity Controls) — what YOU must do to inherit their controls.
5. Sign DPA + service-provider terms (CPRA-compliant).
6. Risk score (high / med / low) → review frequency.

Drata / Vanta vendor modules automate this workflow.
```

### Recipe 12: Common findings + remediation
```text
Frequent SOC 2 findings:
1. MFA gaps — some users without MFA enrolled (especially admin accounts)
2. Offboarding delays — terminated users still have access >24 hours later
3. Patch SLA misses — critical vulnerabilities open >30 days
4. Policy gaps — no documented incident response or BCP
5. Missing access reviews — quarterly review not performed
6. Vendor risk gaps — no SOC 2 report on file for critical vendor
7. Backup test gaps — not tested in last 12 months
8. Pen-test gap — older than 12 months
9. Code review gaps — direct-to-main commits without PR
10. Encryption gaps — S3 buckets / DBs not encrypted

Remediation runbook:
- Drata / Vanta / SecureFrame flag in dashboard
- Assign owner + deadline
- Re-test after fix
```

### Recipe 13: SOC 2 readiness gap report
```markdown
# SOC 2 Readiness Audit — <Co.>

**Date:** 2026-06-09
**Auditor:** Legal Counsel (AI agent)
**TSC scope:** Security + Availability + Confidentiality
**Target:** Type II report by <date>

## Current readiness: <%>

## Gaps by criterion
### CC1 (Control Environment): X open
### CC2 (Communication): X open
### CC3 (Risk Assessment): X open
### CC4 (Monitoring): X open
### CC5 (Control Activities): X open
### CC6 (Logical + Physical Access): X open
### CC7 (System Operations): X open
### CC8 (Change Management): X open
### CC9 (Risk Mitigation): X open
### A1 (Availability): X open
### C1 (Confidentiality): X open

## Remediation plan
| Gap | Priority | Owner | Deadline |
|---|---|---|---|
| Enable MFA on remaining admin accounts | HIGH | Eng | 2026-06-15 |
| Document Incident Response Plan | HIGH | Sec | 2026-07-01 |
| Quarterly access review process | MED | IT | 2026-07-15 |

## Next steps
- Continue Drata remediation
- Schedule auditor kickoff for Q3
- Begin 6-month Type II observation Q4

---
**Disclaimer:** This is informational guidance from an AI agent. Always consult a licensed attorney + qualified CPA / auditor in your jurisdiction before relying on this assessment for compliance posture or audit readiness.
```

## Examples

### Example 1: First-time SOC 2 Type I (mid-stage SaaS)
**Goal:** Achieve Type I in 3 months for enterprise deal.
**Steps:**
1. Pick Drata (Recipe 3).
2. Pick scope: Security + Confidentiality (Recipe 2).
3. Connect AWS, Okta, GitHub, Jira (Recipe 3).
4. Customize 28 policies (Drata template library).
5. Run 4-6 week remediation sprint (Recipe 12).
6. Schedule audit with Schellman / A-LIGN / Prescient Assurance (Recipe 7).
7. Achieve Type I.
8. Begin Type II observation window.

**Result:** Type I report enabling enterprise close; Type II in pipeline.

### Example 2: Vendor risk review automation
**Goal:** Review 30 vendors annually.
**Steps:**
1. Drata vendor module → import vendor list.
2. Vendor questionnaire → automated send.
3. SOC 2 reports collected + parsed.
4. Risk scoring → high/med/low.
5. Annual review schedule.

**Result:** Compliant vendor management with low manual lift.

## Edge cases / gotchas

- **SOC 2 ≠ ISO 27001 ≠ HITRUST.** SOC 2 is most common in US B2B SaaS; ISO 27001 broader; HITRUST for healthcare. Customer asks dictate.
- **SOC 2 reports are NOT public.** Customer prospects must sign NDA before receiving. Drata / Vanta Trust Center pages share controls summary publicly.
- **Type II observation includes evidence FROM the period.** You can't backdate controls. Implement BEFORE observation start.
- **"Privacy" TSC overlaps with GDPR/CCPA work** but doesn't replace it. AICPA Privacy Framework + GDPR/CCPA are different.
- **Carve-out vs inclusive subservice organizations.** Your AWS controls are inherited via "inclusive" or carved out via "carve-out." Choose based on what AWS already controls.
- **CUECs (Complementary User Entity Controls) shift work to YOU.** Vendor's SOC 2 doesn't cover what you do — read CUECs carefully.
- **Drata / Vanta / SecureFrame ≠ auditor.** They prep + provide evidence; an AICPA CPA firm issues the report.
- **Continuous monitoring drift.** Even after Type II passes, daily controls can drift. Drata / Vanta alert on drift; address quickly to maintain compliance.
- **Auditor independence rules (AICPA).** Audit firm can't both consult on remediation AND audit. Choose carefully.
- **Cost timeline.** Year 1 typical: $7-15k Drata + $15-30k Type II audit + $5-10k pen-test = $30-55k. Year 2+: lower as ramp-up cost amortized.
- **Cybersecurity Maturity Model Certification (CMMC) is separate** — required for DoD contractors. Beyond SOC 2 scope.

> Warning: **This is informational guidance from an AI agent, not a substitute for a licensed attorney + qualified CPA / auditor. Always consult both before relying on this assessment for audit readiness, customer commitments, or binding decisions.**

## Sources

- [AICPA SOC 2 Resources](https://us.aicpa.org/interestareas/frc/assuranceadvisoryservices/sorhome) — official.
- [AICPA TSP 100 Trust Services Criteria](https://us.aicpa.org/content/dam/aicpa/interestareas/frc/assuranceadvisoryservices/downloadabledocuments/trust-services-criteria.pdf)
- [Drata](https://drata.com/) — automation platform.
- [Drata Developer API](https://developers.drata.com/) — REST API docs.
- [Vanta](https://www.vanta.com/) — automation platform.
- [SecureFrame](https://secureframe.com/) — automation platform.
- [Thoropass](https://thoropass.com/) — auditor-in-a-box alternative.
- [Schellman](https://www.schellman.com/) — SOC 2 audit firm.
- [A-LIGN](https://www.a-lign.com/) — SOC 2 audit firm.
- [Coalfire](https://www.coalfire.com/) — security-focused audit firm.
- Sister skills: `gdpr-readiness-audit`, `ccpa-cpra-readiness-audit`.
