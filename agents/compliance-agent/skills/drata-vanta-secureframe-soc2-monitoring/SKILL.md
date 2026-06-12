---
name: drata-vanta-secureframe-soc2-monitoring
description: Continuous SOC 2 monitoring + multi-framework GRC automation via Vanta, Drata, Secureframe, Sprinto, or Thoropass. Map AICPA TSP 100 Trust Services Criteria, set up automated evidence collection, coordinate auditors, manage findings, bridge between Type II observation periods, and operate the cross-framework crosswalk so one control set earns SOC 2 + ISO 27001 + HIPAA + GDPR simultaneously.
---

# SOC 2 + Multi-Framework GRC Monitoring — Drata / Vanta / Secureframe / Sprinto / Thoropass

SOC 2 is the dominant US B2B SaaS security audit standard in 2026. The five GRC automation platforms below cover 90%+ of mid-market deployments. This skill operates as a continuous monitoring + audit-coordination pack, NOT a one-shot readiness sprint. The agent uses it to query control status via API, generate gap remediation tickets, draft management responses to findings, and ship cross-framework evidence mapping.

## When to use

User says:
- "SOC 2 readiness" / "Type I vs Type II" / "We need a SOC 2 report"
- "Set up Vanta / Drata / Secureframe / Sprinto / Thoropass"
- "Continuous SOC 2 monitoring"
- "TSC mapping" / "Trust Services Criteria"
- "Cross-walk SOC 2 to ISO / HIPAA / NIST CSF"
- "Bridge letter" / "Auditor coordination" / "Management response"
- "Sub-service organization carve-out" / "CUEC" / "Complementary User Entity Controls"
- "Drata API integration" / "Vanta API"

Companion skills: `iso-27001-isms-readiness`, `risk-register-maintenance-scoring`, `policy-authoring-cybersecurity-aup-byod`, `vendor-security-questionnaire-caiq-sig`.

## Setup

```bash
# Platform sign-up URLs (recipient supplies tenant API token)
#   https://drata.com/        Drata — ~$7,500/yr base; auditor-favorite UX
#   https://www.vanta.com/    Vanta — ~$8,000/yr base; ~35% market share; broadest integrations
#   https://secureframe.com/  Secureframe — ~$7,500/yr base; advisory-heavy
#   https://sprinto.com/      Sprinto — mid-market international
#   https://thoropass.com/    Thoropass — bundles automation + audit

# Env vars (recipient supplies)
export DRATA_API_KEY=<drata-dashboard>
export VANTA_API_KEY=<vanta-dashboard>
export VANTA_CLIENT_ID=<vanta-oauth>
export VANTA_CLIENT_SECRET=<vanta-oauth>
export SECUREFRAME_API_KEY=<secureframe-dashboard>
export SPRINTO_API_KEY=<sprinto-dashboard>

# AICPA Trust Services Criteria (free, public)
curl -fsSL -o aicpa_tsp_100.pdf \
  https://us.aicpa.org/content/dam/aicpa/interestareas/frc/assuranceadvisoryservices/downloadabledocuments/trust-services-criteria.pdf

# NIST CSF 2.0 (anchor for cross-walks)
curl -fsSL -o nist_csf_2.pdf \
  https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf
```

Auth notes:
- `DRATA_API_KEY` — Drata Public API (developers.drata.com). Token scope: read-only is sufficient for monitoring; read-write for ticket creation.
- `VANTA_API_KEY` — Vanta supports both static API keys (legacy) and OAuth 2.0 (preferred 2026). OAuth scopes: `controls:read`, `tests:read`, `policies:read`.
- All platforms: free trial typically 14 days; production tenants gated behind paid contract.

## Common recipes

### Recipe 1: Pick Type I vs Type II

```text
Type I (point-in-time):
- 1-3 month prep
- Auditor verifies DESIGN of controls AS OF a date
- $5K-$15K audit fee
- Use case: first SOC 2 to unblock enterprise pipeline; signal-only
- LIMITATION: many enterprise customers won't accept Type I

Type II (observation period):
- 3-12 month observation window (6 months most common first-time)
- Auditor verifies DESIGN AND OPERATING EFFECTIVENESS over the window
- $15K-$50K audit fee
- REQUIRED by most enterprise customers
- Annual renewal expected; bridge letters between periods
```

### Recipe 2: Trust Services Criteria (TSP 100) scope selection

```text
Security (Common Criteria CC1-CC9 — MANDATORY for every SOC 2):
- CC1 Control Environment
- CC2 Communication + Information
- CC3 Risk Assessment
- CC4 Monitoring Activities
- CC5 Control Activities
- CC6 Logical + Physical Access
- CC7 System Operations
- CC8 Change Management
- CC9 Risk Mitigation

Optional categories (pick based on customer asks):
- Availability (A1.1-A1.3) — uptime + capacity + recovery; common for SaaS
- Confidentiality (C1.1-C1.2) — designated confidential info; common for B2B
- Processing Integrity (PI1.1-PI1.5) — accuracy of financial/transactional
- Privacy (P1.1-P8.1) — PII per AICPA Privacy Framework; often skipped (GDPR/CCPA covers)

Default scoping for B2B SaaS: Security + Availability + Confidentiality.
```

### Recipe 3: Drata API — pull control status

```bash
# https://developers.drata.com
# All controls with status
curl -X GET 'https://public-api.drata.com/v1/controls' \
  -H "Authorization: Bearer $DRATA_API_KEY" \
  -H "Accept: application/json" | jq '.data[] | {id, name, status, framework}'

# Failing tests
curl -X GET 'https://public-api.drata.com/v1/tests?status=FAILING' \
  -H "Authorization: Bearer $DRATA_API_KEY" | jq '.data[] | {id, name, controlId, lastFailedAt}'

# Personnel without MFA
curl -X GET 'https://public-api.drata.com/v1/personnel?mfaEnabled=false' \
  -H "Authorization: Bearer $DRATA_API_KEY"
```

### Recipe 4: Vanta API — control + test queries

```bash
# https://developer.vanta.com (OAuth 2.0 preferred)
# Get OAuth token
TOKEN=$(curl -X POST https://api.vanta.com/oauth/token \
  -H "Content-Type: application/json" \
  -d "{\"client_id\":\"$VANTA_CLIENT_ID\",\"client_secret\":\"$VANTA_CLIENT_SECRET\",\"grant_type\":\"client_credentials\",\"scope\":\"vanta-api.all:read\"}" \
  | jq -r '.access_token')

# List controls
curl -X GET 'https://api.vanta.com/v1/controls' \
  -H "Authorization: Bearer $TOKEN" | jq '.data[]'

# Failing tests (evidence drift)
curl -X GET 'https://api.vanta.com/v1/tests?statuses=FAILING' \
  -H "Authorization: Bearer $TOKEN"
```

### Recipe 5: Secureframe API

```bash
# https://secureframe.com/hubfs/Secureframe-API.pdf
curl -X GET 'https://api.secureframe.com/v1/tests' \
  -H "Authorization: Bearer $SECUREFRAME_API_KEY"
```

### Recipe 6: Sprinto API

```bash
# https://docs.sprinto.com/sprinto-public-api
curl -X GET 'https://api.sprinto.com/v1/controls' \
  -H "Authorization: Bearer $SPRINTO_API_KEY"
```

### Recipe 7: Cross-framework control crosswalk

| Control area | SOC 2 TSC | ISO 27001:2022 Annex A | HIPAA Security | PCI DSS v4.0 | NIST CSF 2.0 |
|---|---|---|---|---|---|
| Information Security Policy | CC1.1 | A.5.1 | §164.316(a) | Req. 12.1 | GV.PO-01 |
| Access Control / IAM | CC6.1, CC6.2, CC6.3 | A.5.15, A.5.16, A.8.2, A.8.3 | §164.308(a)(3), §164.312(a) | Req. 7, 8 | PR.AA |
| Encryption at rest / in transit | CC6.7 | A.8.24 | §164.312(a)(2)(iv), §164.312(e)(1) | Req. 3, 4 | PR.DS-01, 02 |
| Logging + monitoring | CC7.2 | A.8.15, A.8.16 | §164.308(a)(1)(ii)(D) | Req. 10 | DE.CM |
| Change management | CC8.1 | A.8.32 | §164.308(a)(8) | Req. 6.5 | PR.PS-06 |
| Vulnerability management | CC7.1 | A.8.8 | §164.308(a)(8) | Req. 11.3 | DE.CM-09 |
| Pen testing | CC4.1 | A.8.29 | §164.308(a)(8) | Req. 11.4 | DE.CM-09 |
| Incident response | CC7.4, CC7.5 | A.5.24-A.5.28 | §164.308(a)(6) | Req. 12.10 | RS.MA, RS.AN |
| Risk assessment | CC3.1, CC3.2 | A.6.1.2, A.6.1.3 | §164.308(a)(1)(ii)(A) | Req. 12.3 | ID.RA, GV.RM |
| Vendor / TPRM | CC9.2 | A.5.19-A.5.23 | §164.308(b), §164.314(a) | Req. 12.8 | GV.SC, ID.SC |
| Awareness training | CC1.4 | A.6.3 | §164.308(a)(5) | Req. 12.6 | PR.AT |
| Business continuity | A1.2 | A.5.29, A.5.30 | §164.308(a)(7) | Req. 12.10 | RC.RP |

**Rule:** when authoring a control, name ALL frameworks it satisfies. One policy → many certifications.

### Recipe 8: Critical control inventory (cross-platform must-haves)

```text
Identity + access:
- MFA on all employees (admin + standard)
- Quarterly access reviews (evidence: reviewer name + date + scope)
- Offboarding within 24 hours of termination
- Privileged access logged + reviewed

Encryption:
- TLS 1.2+ in transit (TLS 1.3 preferred)
- AES-256 at rest
- KMS-managed keys; rotation policy

Vulnerability management:
- Scan + patch SLA (Critical 14d, High 30d per PCI DSS Req. 6.3.1)
- Annual external pen test

Logging:
- 1-year audit log retention minimum
- SIEM coverage (Splunk / Datadog / Sentinel / Panther)

Change management:
- PR-gated production deploys
- Branch protection on main

Incident response:
- IR plan (NIST SP 800-61 r3 aligned)
- On-call rotation
- Quarterly tabletops
- Post-incident reviews (PIR)

Backup + recovery:
- RTO / RPO defined per system
- Annual restore test

Vendor management:
- SOC 2 / ISO report on file for every Tier 1 vendor
- DPA + BAA + SCC where applicable
```

### Recipe 9: Bridge letter request template

```text
To: <Auditor partner>
Subject: Bridge letter request — <Co.> SOC 2 Type II

Hi <name>,

Requesting a bridge letter covering the period <date — last report end> to <date — current>.

Our current Type II observation window is <start> to <end>, with the report scheduled for delivery <date>. We have a customer prospect requesting interim assurance for a procurement gate on <date>.

No material changes to controls or scope since the previous Type II.

Please confirm fee + turnaround.

Thanks,
<name>
```

Bridge letters typically cost $500-$1,000 and turn around in 5-10 business days.

### Recipe 10: Management response to audit finding

```markdown
## Finding <ID> — <short title>

**Criterion:** <e.g. CC6.1 — Logical access security software>
**Observation:** <auditor's observation, copy verbatim>
**Severity (auditor):** <High / Medium / Low>

### Management response

**Acknowledgment:** We acknowledge the observation.

**Root cause:** <brief — process gap, tooling gap, ownership gap>

**Corrective action:**
1. <Action 1 — owner — due date>
2. <Action 2 — owner — due date>

**Status:** <Open / In progress / Closed>
**Target close date:** <YYYY-MM-DD>
**Compensating control during remediation:** <if applicable>

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

### Recipe 11: Sub-service organization carve-out vs inclusive

```text
Carve-out method (most common for SaaS using AWS/GCP/Azure):
- Sub-service org's controls are NOT in scope of your SOC 2 report.
- Your report describes the services they perform but excludes their controls.
- You list Complementary Subservice Organization Controls (CSOCs) the sub-service org must implement.
- Customer reads YOUR SOC 2 + AWS/GCP/Azure SOC 2 separately.

Inclusive method (rare):
- Sub-service org's controls ARE in scope.
- Their controls tested by your auditor.
- Requires sub-service cooperation; AWS / GCP / Azure won't do this.

CUECs (Complementary User Entity Controls):
- What YOUR customers must do to inherit your controls.
- Example: customer must rotate API keys per your password policy.
- Document in SOC 2 Section 5 description.
```

### Recipe 12: Audit coordination calendar (Type II annual)

```text
Month  Activity
T-3    Auditor RFP + selection
T-2    Kickoff + walkthrough scoping
T-1    Pre-audit mock + last-mile remediation
T 0    Observation window starts
T+1    Monthly evidence sync with auditor portal
T+3    Mid-period checkpoint
T+5    Quarter check + drift remediation
T+6    Observation window ends (6mo first-time)
T+7    Auditor fieldwork (walkthroughs + sample testing)
T+8    Findings + management response
T+9    Report delivery
T+10   Customer distribution + bridge letter setup
```

### Recipe 13: SOC 2 readiness gap report template

```markdown
# SOC 2 Readiness Audit — <Co.>

**Date:** <YYYY-MM-DD>
**Author:** Compliance Agent (AI)
**TSC scope:** Security + Availability + Confidentiality
**Target:** Type II report by <date>
**Platform:** <Drata / Vanta / Secureframe / Sprinto / Thoropass>
**Auditor:** <name>

## Current readiness: <%>

## Gaps by criterion
### CC1 (Control Environment): <N> open
### CC2 (Communication): <N> open
### CC3 (Risk Assessment): <N> open
### CC4 (Monitoring): <N> open
### CC5 (Control Activities): <N> open
### CC6 (Logical + Physical Access): <N> open
### CC7 (System Operations): <N> open
### CC8 (Change Management): <N> open
### CC9 (Risk Mitigation): <N> open
### A1 (Availability): <N> open
### C1 (Confidentiality): <N> open

## Remediation plan
| Gap | Priority | Owner | Deadline |
|---|---|---|---|
| Enable MFA on remaining admin accounts | HIGH | Eng | <date> |
| Document IR Plan (NIST 800-61 r3) | HIGH | Sec | <date> |
| Quarterly access review process | MED | IT | <date> |

## Next steps
- Continue platform remediation
- Schedule auditor kickoff for <quarter>
- Begin 6-month Type II observation <quarter>

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

## Examples

### Example 1: First Type I via Drata for enterprise close

**Goal:** Ship Type I report in 90 days to unblock $500K ARR enterprise deal.

**Steps:**
1. Confirm scope: Security + Confidentiality (no Availability needed — customer didn't ask).
2. Sign up Drata + connect AWS, Okta, GitHub, Jira, BambooHR, Linear.
3. Customize 25 policies from Drata library (don't accept defaults verbatim).
4. Assign owners + due dates per control.
5. 6-week remediation sprint focused on MFA gaps, offboarding SLA, backup test.
6. Engage Prescient Assurance for 60-day fieldwork.
7. Achieve Type I AS OF month 3.
8. Begin Type II observation immediately.

**Result:** Type I in hand, Type II window started, enterprise deal closes month 4.

### Example 2: Drift remediation via API monitoring

**Goal:** Detect + remediate control drift within 48 hours.

**Steps:**
1. Cron job polls Drata API daily: `GET /v1/tests?status=FAILING`.
2. For each new failure: auto-create Linear ticket with control ID + owner.
3. Slack notification to control owner.
4. Re-poll after 24h; escalate to manager if unresolved.

**Result:** Mean time to detect drift drops from monthly review to 24h.

### Example 3: Cross-framework efficiency — single control set, 4 certifications

**Goal:** Vanta-managed SOC 2 + ISO 27001 + HIPAA + GDPR with one control library.

**Steps:**
1. Use crosswalk (Recipe 7) to identify overlapping controls.
2. Tag each Vanta control with all applicable frameworks.
3. One policy update → automatically refreshes evidence across all four reports.
4. Coordinate auditor for SOC 2 + ISO joint audit (Schellman + A-LIGN both offer).

**Result:** Reduce annual GRC effort by 40-60% vs sequential framework projects.

## Edge cases / gotchas

- **SOC 2 reports are NOT public.** Distribution requires NDA. Trust Centers (trust.vanta.com, drata.com/trust-center) share controls summary publicly without report.
- **Type II observation window cannot be backdated.** Controls must be operating during the period. Implement BEFORE observation starts.
- **Drata / Vanta / Secureframe are NOT auditors.** AICPA independence rules prohibit consult-and-audit by same firm. Pick an AICPA-registered CPA firm separately.
- **Auditor independence rules (AICPA).** Drata / Vanta / Secureframe consulting partners cannot also audit you. Verify auditor independence at engagement.
- **CUECs shift work to YOUR customers.** Document them in Section 5; failure to follow CUECs voids inherited control assurance.
- **Sub-service carve-out is the default for AWS / GCP / Azure.** Inclusive is impractical — they won't allow your auditor to test their controls.
- **Continuous monitoring drift.** Daily-changing controls (MFA enrollment, offboarding SLA) drift quickly. Daily API polling beats monthly manual review.
- **"Privacy" TSC ≠ GDPR / CCPA compliance.** AICPA Privacy Framework is a different scheme. If customer asks for "privacy" SOC 2, confirm they don't actually mean GDPR.
- **Bridge letters are informal.** They're a comfort signal, not a substitute for an in-period report. Some sophisticated procurement teams reject bridge letters.
- **CMMC 2.0 ≠ SOC 2.** DoD contractors need separate CMMC accreditation; SOC 2 does not satisfy CMMC.
- **Pricing — first Type II typical all-in:** $7K-$30K platform + $15K-$50K audit + $5K-$15K pen test = $30K-$120K. Year 2+ drops 30-40%.
- **Cross-walk matrix is directional.** Auditor judgment varies on what "satisfies" a control. Confirm acceptable mappings with your auditor before relying.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [AICPA SOC 2 Resources](https://us.aicpa.org/interestareas/frc/assuranceadvisoryservices/sorhome)
- [AICPA TSP 100 Trust Services Criteria](https://us.aicpa.org/content/dam/aicpa/interestareas/frc/assuranceadvisoryservices/downloadabledocuments/trust-services-criteria.pdf)
- [Drata Developer API](https://developers.drata.com/)
- [Vanta Developer Platform](https://developer.vanta.com/)
- [Secureframe API docs](https://secureframe.com/)
- [Sprinto API](https://docs.sprinto.com/sprinto-public-api)
- [Thoropass](https://thoropass.com/)
- [Schellman SOC 2 audit](https://www.schellman.com/)
- [A-LIGN SOC 2 audit](https://www.a-lign.com/)
- [Coalfire](https://www.coalfire.com/)
- [KirkpatrickPrice](https://kirkpatrickprice.com/)
- [Prescient Assurance](https://prescientassurance.com/)
- [NIST CSF 2.0](https://www.nist.gov/cyberframework)
