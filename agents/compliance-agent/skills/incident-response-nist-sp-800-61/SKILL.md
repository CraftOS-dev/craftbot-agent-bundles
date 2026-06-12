---
name: incident-response-nist-sp-800-61
description: Incident response plan + playbooks aligned to NIST SP 800-61 Rev. 3 (April 2025; first update since 2012) + NIST CSF 2.0 six functions (Govern, Identify, Protect, Detect, Respond, Recover). Per-scenario playbooks (ransomware, BEC, data breach, ATO, insider, vendor, DDoS, lost device, AI-system compromise). CSIRT roster + on-call. Quarterly tabletops. IR retainers (CrowdStrike / Mandiant / Stroz Friedberg / Kroll / Coveware).
---

# IR Plan + Playbooks — NIST SP 800-61 Rev. 3 + CSF 2.0

NIST SP 800-61 Rev. 3 (April 2025) is the canonical IR guide. Shifts from rigid 4-phase to continuous CSF-2.0-aligned model. Required for SOC 2 CC7.4-5 + ISO 27001 A.5.24-28 + HIPAA §164.308(a)(6) + PCI Req. 12.10 + NYDFS + NIS2.

## When to use

User says:
- "Incident response plan" / "IR plan"
- "IR playbook" / "ransomware playbook" / "BEC playbook"
- "Tabletop exercise" / "TTX"
- "CSIRT" / "on-call rotation" / "IR retainer"
- "NIST 800-61" / "CSF 2.0 Respond / Recover"
- "Post-incident review" / "PIR"
- "Breach coach"

Companion skills: `breach-notification-gdpr-72hr-state-laws`, `data-classification-dlp-purview-nightfall`.

## Setup

```bash
# NIST SP 800-61 Rev. 3
curl -fsSL -o nist_800_61_r3.pdf https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf

# NIST CSF 2.0
curl -fsSL -o nist_csf_2.pdf https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf

# CISA IR Playbook
curl -fsSL -o cisa_ir_playbook.pdf https://www.cisa.gov/sites/default/files/2024-08/Federal_Government_Cybersecurity_Incident_and_Vulnerability_Response_Playbooks_508C.pdf

# IR retainer firm contact list (build internal)
# Major firms 2026: CrowdStrike, Mandiant (Google), Stroz Friedberg, Kroll, 
# Coveware (ransom negotiation), Booz Allen, Palo Alto Unit 42, Trustwave SpiderLabs

# Breach coach firms (privacy/cyber attorneys)
# Mullen Coughlin, BakerHostetler, Davis Wright Tremaine, Kennedys, Wilson Elser
```

## Common recipes

### Recipe 1: CSF 2.0 six functions (IR mapping)

```text
GOVERN (GV) — new in CSF 2.0
- IR program ownership + roles
- Policy + scope + exec accountability
- Retainer + insurance agreements
- Annual IR plan review

IDENTIFY (ID)
- Asset inventory (critical for blast-radius assessment)
- Threat landscape monitoring
- Vulnerability state
- Supply chain risk visibility

PROTECT (PR)
- Preventive controls (the more this works, the fewer incidents)
- Awareness training
- Secure configuration
- Data security at rest + in transit

DETECT (DE)
- SIEM / EDR alerting
- Anomaly detection
- Threat intel matching
- User reports
- Network monitoring

RESPOND (RS)
- Triage + severity classification
- Containment (short-term + long-term)
- Eradication (remove root cause)
- Communication (internal + external + regulator)

RECOVER (RC)
- System restoration
- Validation (confirm clean)
- Post-incident review (PIR / lessons learned)
- Improvement actions
```

### Recipe 2: IR Plan structure

```markdown
# Incident Response Plan — <Co.>

**Version:** <X.Y>
**Approved by:** <Exec Sponsor / Board>
**Effective:** <date>
**Annual review:** <date>
**Owner:** <Sec Lead / CSIRT lead>

## 1. Purpose + scope
Cover incidents affecting confidentiality, integrity, availability of
production systems, employee data, customer data, intellectual property.

## 2. Roles + responsibilities
- Executive Sponsor: <C-level — decisions on disclosure, retainer use,
  litigation hold>
- CSIRT Lead: <Sec Lead — runs incident; coordinates teams>
- SecOps: <triage, containment, forensics>
- Engineering: <patches, code, restoration>
- IT Operations: <network, endpoint, infra>
- Legal: <regulatory, contractual, litigation hold, attorney-client
  privilege>
- Privacy / DPO: <DSR, breach notification scope, regulator coordination>
- Communications / PR: <press, customer comms, employees>
- HR: <if insider; if employee impacted>
- External: IR retainer firm, breach coach, PR firm, forensic firm

## 3. Severity matrix
| SEV | Definition | Examples | Activation |
|---|---|---|---|
| SEV-1 Critical | Confirmed material data exfil OR ransomware OR mass account compromise | Customer DB breach, ransomware encrypting prod | Full CSIRT + Exec |
| SEV-2 High | Material risk to data/operations; isolated | Targeted phishing successful; minor segment compromise | CSIRT Lead + relevant teams |
| SEV-3 Medium | Potential issue; investigation underway | Suspicious admin login; vendor breach (we may be affected) | On-call SecOps + lead consult |
| SEV-4 Low | False positive / noise | Routine phish report; benign anomaly | On-call SecOps |

## 4. Escalation matrix
- SEV-1: Page CSIRT + Exec immediately (24/7).
- SEV-2: Page CSIRT during business hrs; escalate to Exec within 4h.
- SEV-3: Open ticket; review same day.
- SEV-4: Log + close.

## 5. Communication tree
- Internal slack: #ir-active-<incident-id>
- Status updates: every 2h SEV-1; every 4h SEV-2; daily SEV-3
- War room: Zoom <link>
- External: per breach notification matrix
  (`breach-notification-gdpr-72hr-state-laws`)

## 6. Tabletop schedule
Quarterly minimum. Scenarios rotate.

## 7. Retainer + contacts
- IR firm: <name> — <24/7 number>
- Breach coach: <law firm> — <24/7 number>
- Forensic firm: <name>
- PR firm: <name>
- Insurance broker: <name>

## 8. Annual review + improvement
Lessons-learned action items tracked + closed.

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

### Recipe 3: Ransomware playbook

```markdown
# Ransomware Playbook

## Detect
- EDR alerts (CrowdStrike / SentinelOne / Defender)
- Sudden mass-file encryption notifications
- Ransom note appearance
- Backup tampering alert

## Triage (first 60 min)
1. Confirm: real ransomware vs false positive?
2. Identify ransomware family (Conti, LockBit, ALPHV, Akira, etc.) via
   ransom note + EDR telemetry. Check Coveware + ID Ransomware.
3. Identify blast radius: which hosts, networks, data?
4. Engage IR retainer firm immediately.
5. Engage breach coach for attorney-client privileged investigation.
6. Activate cyber insurance — notify within 24h per policy.

## Contain (first 2 hours)
1. Network isolate affected hosts (don't power off — preserves volatile
   memory for forensics).
2. Disable AD accounts of compromised users.
3. Block C2 IPs at perimeter + DNS.
4. Disable shared file servers if encrypting.
5. Preserve evidence (memory dump, disk image, logs).

## Eradicate (4-24 hours)
1. Forensic firm investigates entry vector.
2. Identify + close vulnerability.
3. Confirm no persistence mechanisms remain.
4. Patch + rebuild compromised systems (don't restore from backup of
   compromised period).

## Recover (24h-2 weeks)
1. Restore from clean backups.
2. Validate integrity.
3. Phased re-connection to network.
4. Monitor for re-infection 30+ days.

## Communicate
- Internal: every 2h to Exec + CSIRT.
- Customers: per breach notification matrix.
- Regulators: GDPR 72h; HIPAA 60d; SEC 4 business days if material.
- Insurance: per policy.
- Ransom: NEVER pay without legal + insurance + OFAC check. Coveware /
  Mandiant handle ransom negotiation if needed.

## OFAC consideration
Paying ransom to sanctioned entities (Conti, LockBit affiliates, etc.) =
OFAC violation. Treasury OFAC Oct 2020 advisory clarified.

## Post-incident
PIR within 30 days. Root cause + action items.

---
*Disclaimer per template.*
```

### Recipe 4: BEC (Business Email Compromise) playbook

```markdown
# BEC Playbook

## Trigger
- Finance reports unusual wire request
- Vendor reports invoice with changed bank
- IT detects unauthorized inbox rule (auto-forward)
- User reports compromise

## Containment (first hour)
1. Force password + MFA reset on compromised account.
2. Revoke all active sessions + OAuth tokens.
3. Pull inbox audit logs (forwarding rules, sent items).
4. Identify: who else received forwarded emails?
5. Reverse pending wires if possible (call bank immediately).

## Investigation
1. Email logs (Defender / Workspace) — trace attacker entry.
2. Sign-in logs (impossible travel, unfamiliar location).
3. Audit logs (delegate access, mailbox forwarding rules, app consent).
4. OAuth grant inventory — revoke unauthorized.
5. Did attacker access OneDrive / Drive / Box? Check.

## Eradicate
1. Remove forwarding rules + delegates.
2. Revoke OAuth consents.
3. Re-enable account post-cleanup.
4. Enable Conditional Access + improved sign-in policies.

## Communicate
- Finance: SOP refresh on wire verification.
- Customers: if their data accessed → breach notification.
- Vendors: if vendor impersonated → coordinate.
- Insurance: BEC has specific coverage; notify.

## Recovery / counsel
- FBI IC3 report (https://ic3.gov) for tracking + fund recovery.
- Bank fraud recovery process.
- Breach coach for legal + regulatory exposure.

---
*Disclaimer per template.*
```

### Recipe 5: Data breach playbook

```markdown
# Data Breach Playbook

## Trigger
- DLP alert (sensitive data egress)
- SIEM anomaly (mass data access)
- Vendor breach notification
- Public disclosure (paste site, dark web, news)
- Internal report

## Containment (first 24h)
1. Identify what data was accessed/exfiltrated.
2. Stop ongoing exfiltration (revoke access, block egress).
3. Preserve evidence per chain-of-custody.
4. Engage IR retainer + breach coach.

## Investigation (24-72h)
1. Forensic — timeline of access.
2. Identify affected records + data subjects.
3. Determine cause (vulnerability, insider, vendor).
4. Assess: was data encrypted? (HHS safe harbor — encrypted PHI = no
   notification per HIPAA).

## Notification decision matrix
- See `breach-notification-gdpr-72hr-state-laws` for matrix.
- GDPR 72h to SA (Art. 33); data subjects if high risk (Art. 34).
- HIPAA 60-day individuals; HHS for 500+; media if 500+ in state.
- US state laws per NCSL matrix.
- SEC 8-K Item 1.05 if material (4 business days).

## Eradicate + Recover
1. Patch entry vector.
2. Account hygiene (rotate creds, revoke tokens).
3. Strengthen controls based on root cause.

## Communicate
- Affected individuals (statutory notice).
- Regulators per matrix.
- Customers (if B2B + data shared).
- Public (if SEC 8-K or public disclosure required).
- Insurance.

---
*Disclaimer per template.*
```

### Recipe 6: Account takeover (ATO) playbook

```markdown
# Account Takeover Playbook

## Detect
- Impossible travel sign-in
- New device + new location + no MFA re-prompt
- Sudden privilege escalation
- Password change without legit ticket

## Contain
1. Disable compromised account (don't delete — preserve).
2. Revoke sessions + OAuth.
3. Reset MFA enrollment.
4. Inventory actions taken by compromised account (last 30-90 days).

## Investigate
1. Sign-in logs.
2. Privileged access logs.
3. Data accessed (DLP).
4. Other accounts targeted (lateral movement).

## Recover
1. User identity verification (out-of-band).
2. Re-enable account with fresh credentials + MFA.
3. Force password change for related accounts (shared credentials risk).

---
*Disclaimer per template.*
```

### Recipe 7: Insider threat playbook

```markdown
# Insider Threat Playbook

## Trigger
- DLP egress alert
- Unusual access pattern
- HR notice of impending termination
- Tip from coworker

## Coordinate
1. HR partnership essential (privacy + legal protections for employee).
2. Legal involvement before any monitoring or termination.
3. Document everything; chain of evidence.

## Contain
1. Quietly disable elevated access (if appropriate; risk of tipping off).
2. Snapshot endpoint forensics.
3. Mailbox + drive preservation.

## Investigate
1. Joint HR + Legal + Sec interview.
2. Forensic of endpoint + cloud activity.
3. Timeline of incidents.

## Resolve
- Termination + access removal (coordinated with HR + Legal).
- Restraining orders / legal action if warranted.
- Data return obligations (NDA, IP).

---
*Disclaimer per template.*
```

### Recipe 8: Vendor / third-party breach playbook

```markdown
# Vendor Breach Playbook

## Trigger
- Vendor announces breach
- BitSight / SS reports incident
- Customer asks about vendor exposure

## Assess (first 24h)
1. Confirm vendor exposure scope (data + systems).
2. Inventory data shared with vendor (per ROPA + DPA).
3. Engage vendor security team for forensics + timeline.

## Contain
1. Rotate credentials + API keys with vendor.
2. Pause data flows (if feasible).
3. Identify customer-facing exposure.

## Cascade notification
- Per GDPR Art. 33 — your awareness clock starts now.
- Per DPA — vendor must notify you per contract.
- Customers — per your DPA terms with them.

## Long-term
- Re-tier vendor.
- Consider termination.
- Insurance claim if covered.
- Update sub-processor list.

---
*Disclaimer per template.*
```

### Recipe 9: AI system compromise playbook (NEW 2025+)

```markdown
# AI System Compromise Playbook

## Trigger
- Model output deviation (drift > threshold)
- Prompt injection success
- Training data poisoning indicator
- Model extraction attack
- Adversarial input causing safety failure

## Contain
1. Roll back to last known-good model checkpoint.
2. Disable affected feature (kill switch).
3. Block adversarial input patterns.

## Investigate
1. Identify attack vector (prompt, data, model weights, runtime).
2. Forensic of training data lineage.
3. Customer impact assessment.

## Eradicate
1. Re-train on clean data if poisoned.
2. Update guardrails + safety filters.
3. Adversarial robustness testing.

## Communicate
- EU AI Act post-market monitoring obligation (for high-risk systems).
- Affected customers.
- Regulator if mandated.

## Coordinate with
- `ai-governance-eu-ai-act-eticas-credo` for AI Act compliance.

---
*Disclaimer per template.*
```

### Recipe 10: Tabletop exercise template

```markdown
# Tabletop Exercise — <Scenario>

**Date:** <YYYY-MM-DD>
**Duration:** 2-4 hours
**Facilitator:** <Internal Sec / external firm>
**Scribe:** <name>
**Attendees:** CSIRT + relevant participants

## Scenario
<Detailed paragraph — e.g., "Ransomware encrypts your primary production DB
at 03:14 UTC Friday. Customer dashboards show errors. Twitter is lighting
up. Customer Success is paged.">

## Inject 1 (T+30 min): What do you do?
<Each role describes action; facilitator probes for gaps>

## Inject 2 (T+2 hours): Threat actor demands $5M in BTC by Sunday 09:00.
<Discuss: pay/don't pay; OFAC check; insurance; communication>

## Inject 3 (T+6 hours): Reporter from <Major Outlet> calls.
<Discuss: PR response; coordinated comms; what to disclose>

## Inject 4 (T+24 hours): 12 customer C-levels demand a call.
<Discuss: legal hold; standard talking points; CEO availability>

## Debrief (post-scenario)
- What went well?
- What gaps surfaced?
- What action items emerged?

## Action items
| Owner | Action | Due |
|---|---|---|
| Sec Lead | Update IR plan §X | <date> |
| Legal | Review insurance ransomware coverage | <date> |
| Comms | Prepare draft public statement template | <date> |

---
*Disclaimer per template.*
```

### Recipe 11: Post-Incident Review (PIR) template

```markdown
# Post-Incident Review — <Incident ID>

**Incident:** <brief>
**Discovery date:** <YYYY-MM-DD>
**Resolution date:** <YYYY-MM-DD>
**Severity:** SEV-<n>
**Author:** <CSIRT lead>
**Review date:** <within 30 days>

## Timeline
| Timestamp | Event | Owner |
|---|---|---|
| 2026-06-10 03:14 UTC | Alert from EDR on Host A | SecOps |
| 2026-06-10 03:18 UTC | Triage — confirmed real | On-call Sec |
| 2026-06-10 03:24 UTC | Page CSIRT lead | PagerDuty |
| ... | ... | ... |

## Root cause
<Why this happened — technical + procedural + organizational>

## Contributing factors
- <Process / system / training gaps>

## What worked
- <Praise what went well — preserves culture>

## What didn't
- <Gaps; no individual blame>

## Action items
| Owner | Action | Priority | Due |
|---|---|---|---|
| Eng | Patch underlying vuln | High | <date> |
| Sec | Update detection signature | High | <date> |
| IT | Add backup test to monthly cadence | Med | <date> |
| Mgmt | Quarterly TTX on this scenario | Med | <date> |

## Data subjects affected
<Count + categories — sets up GDPR / breach notification >

## Cost
- Direct ($): <forensics, breach coach, comms, ransom if any>
- Indirect: <customer churn, brand>
- Insurance recovered: <$>

---
*Disclaimer per template.*
```

### Recipe 12: CSIRT roster + on-call template

```text
Primary roles:
- CSIRT Lead: <name> — <phone> — <pgp>
- Backup CSIRT Lead: <name>
- SecOps Lead: <name>
- Network / Infra: <name>
- Application / Eng: <name>
- IT Ops: <name>
- Legal Counsel: <name>
- Privacy / DPO: <name>
- Communications: <name>
- HR Liaison: <name>
- Exec Sponsor: <name>

On-call rotation:
- Tool: PagerDuty / Opsgenie / VictorOps
- Schedule: weekly rotation; primary + secondary
- Handoff: written log + checklist at shift change
- Escalation: 15min P0; 30min P1; 1h P2

External:
- IR retainer: <firm> — 24/7 — <#> — <SOW reference>
- Breach coach: <law firm> — 24/7 — <#>
- Forensic firm: <name>
- PR firm: <name>
- Insurance broker: <name>
- Insurance carrier 24/7 claim line: <#>
```

### Recipe 13: Required retainers (mature orgs)

```text
Retainers ensure 24/7 availability + pre-negotiated pricing.

IR firm retainer (~$25K-$75K/yr):
- CrowdStrike Services
- Mandiant (Google)
- Stroz Friedberg (Aon)
- Kroll
- Coveware (ransom negotiation specialty)
- Booz Allen Hamilton
- Palo Alto Unit 42
- Trustwave SpiderLabs
- Charles River Associates

Breach coach (~$10K-$30K/yr retainer + hourly when active):
- Mullen Coughlin (privacy + cyber)
- BakerHostetler (largest dedicated cyber practice)
- Davis Wright Tremaine
- Kennedys
- Wilson Elser
- DLA Piper

PR firm (~$5K-$15K/yr retainer):
- Edelman
- Sard Verbinnen
- Joele Frank
- (Industry-specific firms)

Cyber insurance:
- Limit: $1M-$10M typical mid-market; $25M+ enterprise
- Coverage: 1st-party (forensics, comms, ransom, BI) + 3rd-party (notification, defense, settlements)
- Sublimits: ransom payment often $250K-$5M; social engineering often
  excluded or sublimited
- Annual renewal; questionnaire + outside-in rating-driven
- Brokers: Marsh, Aon, WTW, Lockton, NFP
```

## Examples

### Example 1: Build IR plan for SOC 2 Type II

**Goal:** IR plan operational for SOC 2 CC7.4-5 evidence.

**Steps:**
1. Author IR plan per Recipe 2.
2. Per-scenario playbooks (Recipes 3-9).
3. CSIRT roster + on-call PagerDuty (Recipe 12).
4. IR retainer with CrowdStrike (Recipe 13).
5. Breach coach with Mullen Coughlin.
6. Cyber insurance via Marsh.
7. Quarterly TTX schedule (Recipe 10).
8. PIR template (Recipe 11) ready.

**Result:** SOC 2 CC7.4-5 + ISO A.5.24-28 evidence-ready.

### Example 2: Q3 tabletop — ransomware

**Goal:** Quarterly TTX covering ransomware scenario.

**Steps:**
1. Schedule 3-hour session with CSIRT + Exec + Legal.
2. Run scenario (Recipe 10).
3. Debrief + action items.
4. Update IR plan with gaps surfaced.
5. Repeat next quarter with new scenario.

**Result:** Documented TTX + improved plan.

### Example 3: Real incident — vendor breach

**Goal:** Vendor announces breach affecting our data.

**Steps:**
1. Activate vendor breach playbook (Recipe 8).
2. Inventory exposure per ROPA + DPA.
3. Notify breach coach + insurance.
4. Customer notification per `breach-notification-gdpr-72hr-state-laws`.
5. Vendor termination evaluation per `tprm-third-party-risk-lifecycle`.
6. PIR (Recipe 11) within 30 days.

**Result:** Cascading breach response executed; auditable.

## Edge cases / gotchas

- **NIST SP 800-61 Rev. 3 is the 2026 standard.** Previous 4-phase model is deprecated — use CSF 2.0 alignment.
- **Don't power off ransomware-affected hosts.** Memory state is forensic evidence; network-isolate instead.
- **OFAC ransom check** — paying to sanctioned actors is OFAC violation. Treasury 2020 + 2022 advisories. Coveware coordinates check.
- **Attorney-client privilege** — engage breach coach early; have forensic firm engaged through counsel to maintain privilege.
- **Insurance notification deadlines** — most policies require <24-48h. Failure = denied coverage.
- **SEC 8-K Item 1.05 timing** — 4 business days from MATERIAL determination, not from initial discovery. Counsel-driven materiality assessment.
- **NYDFS 72h is from determination of cybersecurity event,** not from initial alert.
- **GDPR 72h clock is from "awareness,"** not certainty. Document why awareness wasn't reached earlier.
- **HIPAA 60-day individual notice can be delayed for law enforcement.** Document the request in writing.
- **IR firm + insurance carrier panels** — most insurers require pre-approved firms. Match retainer to insurance panel.
- **Tabletops must surface real gaps.** "Everything went great" TTX = wasted time. Inject controversial decisions.
- **PIR culture** — no-blame; root cause focus. Punitive PIR kills future reporting.
- **NIS2 + DORA 24h initial notice** for EU essential entities — see `breach-notification-gdpr-72hr-state-laws`.
- **CMMC 2.0 incident reporting** for DoD contractors via DoD DIBNet portal — distinct workflow.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [NIST SP 800-61 Rev. 3 (April 2025)](https://csrc.nist.gov/pubs/sp/800/61/r3/final)
- [NIST CSF 2.0](https://www.nist.gov/cyberframework)
- [CISA IR Playbook](https://www.cisa.gov/sites/default/files/2024-08/Federal_Government_Cybersecurity_Incident_and_Vulnerability_Response_Playbooks_508C.pdf)
- [CISA Stop Ransomware](https://www.cisa.gov/stopransomware)
- [Treasury OFAC Ransom Advisory (2020)](https://home.treasury.gov/system/files/126/ofac_ransomware_advisory.pdf)
- [Coveware](https://www.coveware.com/)
- [CrowdStrike Services](https://www.crowdstrike.com/services/)
- [Mandiant Services](https://www.mandiant.com/services)
- [Stroz Friedberg](https://www.aon.com/cyber-solutions/stroz-friedberg)
- [Kroll Cyber Risk](https://www.kroll.com/en/services/cyber-risk)
- [Mullen Coughlin (breach coach)](https://www.mullen.law/)
- [BakerHostetler Privacy + Cyber](https://www.bakerlaw.com/services/privacy-and-data-protection)
- [FBI IC3](https://www.ic3.gov/)
- [No More Ransom](https://www.nomoreransom.org/)
- [ID Ransomware](https://id-ransomware.malwarehunterteam.com/)
- [APWG Reporting](https://apwg.org/reportphishing/)
