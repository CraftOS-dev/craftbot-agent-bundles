---
name: tprm-third-party-risk-lifecycle
description: Third-party risk management lifecycle — sourcing+selection (RFP security questions, SOC 2 request), due diligence + tiering, contracting (DPA, BAA, SCC, security addendum, audit rights), onboarding (least-privilege, baseline scan), continuous monitoring (BitSight/SecurityScorecard drift alerts), periodic reassessment (annual SIG refresh for Tier 1; quarterly for critical), termination + offboarding (data return/destruction certification).
---

# TPRM Lifecycle — Sourcing → Selection → Contracting → Onboarding → Monitoring → Reassessment → Offboarding

7-stage lifecycle covering vendor risk from RFP through contractual termination. Inventory discipline (most orgs underestimate vendor count 2-5x). Tiering drives effort. Continuous monitoring beats point-in-time questionnaires.

## When to use

User says:
- "TPRM lifecycle" / "vendor lifecycle"
- "Vendor onboarding" / "vendor offboarding"
- "Vendor tiering" / "Tier 1 / Tier 2"
- "Vendor inventory" / "shadow IT"
- "Vendor contract renewal review"
- "Sub-processor management"
- "Data Processing Agreement" / "DPA"
- "Audit rights clause"

Companion skills: `vendor-risk-bitsight-securityscorecard-upguard`, `vendor-security-questionnaire-caiq-sig`, `data-retention-deletion-policy`.

## Setup

```bash
# Free standards + frameworks
# Shared Assessments SIG
curl -fsSL https://sharedassessments.org/sig/ > /tmp/sig.html

# NIST Supply Chain Risk Management
curl -fsSL https://csrc.nist.gov/publications/detail/sp/800-161/rev-1/final > /tmp/scrm.html

# NIST SP 800-161 Rev. 1 (SCRM for federal info systems)
curl -fsSL -o nist_800_161_r1.pdf https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-161r1.pdf

# UpGuard TPRM Lifecycle blog (industry-standard playbook)
curl -fsSL https://www.upguard.com/blog/vendor-risk-management > /tmp/upguard_tprm.html

# CSA CAIQ v4
curl -fsSL https://cloudsecurityalliance.org/research/cloud-controls-matrix > /tmp/caiq.html
```

## Common recipes

### Recipe 1: Vendor inventory discovery (find the hidden vendors)

```text
Most orgs underestimate vendor count by 2-5x. Cross-reference these sources:

Financial sources:
- AP / vendor master file (CFO)
- Corporate card statements (Brex, Ramp, Divvy, Stripe)
- Procurement system (Coupa, Ariba)

Identity sources:
- SSO logs (Okta, JumpCloud, Google Workspace, Microsoft Entra ID)
- SaaS app inventory (Microsoft 365 / Google Workspace third-party apps)
- SCIM / OAuth grants

Network + Endpoint:
- DNS query logs (SaaS app detection — Cloudflare DNS, Cisco Umbrella)
- CASB (Netskope, Zscaler, McAfee Skyhigh)
- EDR app inventory (CrowdStrike, SentinelOne)

Code + dev sources:
- Dependency manifests (package.json, requirements.txt, Gemfile, go.mod)
- GitHub Actions / CI/CD workflows
- Cloud account vendor (AWS Marketplace, GCP Marketplace subscriptions)

Department interviews:
- Eng, Product, Sales, Mktg, HR, Finance, CS, Legal each maintain shadow
  vendor inventory.
```

### Recipe 2: Vendor tiering matrix

```text
Tier 1 — CRITICAL
- Handles personal data / PHI / financial data / IP
- Or supports business-critical functions (hosting, identity, payments)
- Or has privileged access to production systems
Examples: AWS, Stripe, Okta, Salesforce, Snowflake, Datadog, Github Enterprise

Tier 2 — HIGH
- Handles internal-only sensitive data
- Or supports important business processes
- Or accesses internal systems (read-only)
Examples: Notion, Linear, BambooHR, Mailchimp, Segment

Tier 3 — MODERATE
- Non-sensitive data + accesses systems
Examples: Calendly, DocSend, Loom

Tier 4 — LOW
- Registration only — no data, no system access
Examples: Brand assets vendors, swag, content distribution

Reassessment cadence:
- Tier 1: continuous monitoring + annual full reassessment
- Tier 2: continuous monitoring + biennial reassessment
- Tier 3: news monitoring + triennial reassessment
- Tier 4: contract renewal review only
```

### Recipe 3: Stage 1 — Sourcing + Selection

```text
Pre-RFP security screen (5-10 yes/no questions to disqualify early):

1. Do you maintain a current SOC 2 Type II report? <Y/N>
2. Are you ISO 27001 certified? <Y/N>
3. Have you had a publicly disclosed breach in the past 24 months? <Y/N — if Y, details>
4. Do you offer a DPA / BAA / SCC compatible with our regulatory requirements? <Y/N>
5. Do you support SSO (SAML / OIDC)? <Y/N>
6. Do you support MFA at the user level? <Y/N>
7. Do you offer customer-managed encryption keys (BYOK)? <Y/N>
8. Will you commit to audit rights? <Y/N>
9. Where is data hosted (regions)? <list>
10. What is your standard breach notification timeline? <hours>

Reference checks:
- 2-3 current customers (same vertical / size)
- BitSight + SecurityScorecard external rating
- Glassdoor / G2 reviews (cultural / operational signals)

Output: Vendor selection memo (1-2 pages); RFP scoring matrix.
```

### Recipe 4: Stage 2 — Due Diligence + Tiering

```text
Per Tier 1:
- SIG Plus (~1100 questions) OR CAIQ v4 + custom security questions
- SOC 2 Type II (current; carve-outs reviewed)
- ISO 27001 cert + SoA reviewed
- DPA + BAA + SCC + TIA (if EU transfer)
- Pen test report (most recent)
- Insurance certificates ($M cyber liability minimum)
- Financial review (Tier 1 critical vendors — financial viability)
- D&O + incident-history review

Per Tier 2:
- SIG Core (~700 questions) OR CAIQ
- SOC 2 Type II
- DPA

Per Tier 3:
- SIG Lite (~125 questions) OR shorter custom
- DPA if any data shared

Per Tier 4:
- Registration + standard contract

Document:
- Vendor scorecard (per `vendor-risk-bitsight-securityscorecard-upguard`)
- Tiering decision rationale
- Approval workflow signoff
```

### Recipe 5: Stage 3 — Contracting (hand off to `legal-counsel`)

```markdown
# Required Contract Components

## DPA (Data Processing Agreement) — GDPR Art. 28
- Subject + duration + nature + purpose
- Type of personal data + categories of data subjects
- Controller + processor rights + obligations
- Sub-processor approval mechanism (30-day notice + objection right)
- Security measures (Schedule — TOMs)
- DSR support obligations
- Breach notification (commit to <72h for vendor to notify)
- Audit rights
- Return + deletion at termination

## BAA (Business Associate Agreement) — HIPAA §164.504(e)
- Permitted uses + disclosures
- Safeguards per §§164.308, 310, 312, 316
- Reporting (breach within 60 days)
- Sub-BA flow-down
- Individual rights cooperation
- HHS compliance
- Return / destruction at termination

## SCC + TIA (Standard Contractual Clauses 2021/914)
- EU → non-adequacy jurisdiction transfer
- Module 2 (Controller → Processor) or 3 (Processor → Processor)
- Annex I, II, III completed
- TIA documented per `gdpr-article-30-ropa-dpia`

## Security Addendum
- Compliance with SOC 2 / ISO 27001 / industry standard X
- Vulnerability remediation SLA
- Pen test annual; share executive summary
- Encryption requirements
- Logging + audit trail retention
- Incident response cooperation
- Insurance + indemnification
- Right to audit (third party or self-attest evidence)

## SLA
- Uptime + response time + resolution time
- Credits or penalties for missed SLAs

## Termination
- Convenience + cause (material breach, regulatory)
- Data return + destruction certification (within 30 days)
- Transition assistance
- Survival of confidentiality + data protection
```

### Recipe 6: Stage 4 — Onboarding

```text
Day 1-7:
- Provision account with SSO + MFA
- Least-privilege role assignment
- Add to vendor inventory (Notion/spreadsheet)
- Subscribe to status page + security advisories
- Configure continuous monitoring (BitSight/SecurityScorecard/UpGuard)
- Add to sub-processor list in your privacy policy
- DPA-flowdown notification (Art. 28) if changes affect customers

Day 8-30:
- Baseline outside-in scan
- Integrate with SIEM (forward audit logs if vendor supports)
- IR plan update (add as detection source)
- TPRM tracker: scorecard + next review date

First 90 days:
- Verify in-production usage matches RFP commitments
- Quarterly review check-in
```

### Recipe 7: Stage 5 — Continuous monitoring

```text
Automated:
- BitSight / SecurityScorecard / UpGuard daily rating drift
- News + adverse-media monitoring (vendor name + executives)
- SOC 2 bridge letter calendar (alert at 30 days remaining)
- Breach notification feeds (have-I-been-pwned for credentials,
  SecurityScorecard breach watch)
- Status page subscriptions
- Vendor security advisories (mailing list, RSS)

Manual quarterly:
- Tier 1 vendors: 30-min sync; review open findings, ratings, news
- Risk register touch-up

Manual annual (Tier 1):
- Full reassessment per Stage 2
- DPA/BAA renewal
- Contract review

Triggered:
- Vendor breach → immediate response per
  `vendor-risk-bitsight-securityscorecard-upguard` Recipe 13
- Vendor M&A → re-tier; redo due diligence; DPA flow-down
- Major rating drop → review per drift handler
- Regulatory inquiry → cooperate; coordinate with legal counsel
```

### Recipe 8: Stage 6 — Periodic reassessment

```text
Annual (Tier 1):
- Reissue SIG Plus / CAIQ refresh
- SOC 2 Type II re-review (look for new findings, scope changes)
- ISO 27001 surveillance audit results
- Pen test refresh
- DPA / BAA / SCC re-execute or extend
- Insurance recertification
- Contract terms drift review

Biennial (Tier 2):
- SIG Core refresh
- SOC 2 Type II review

Triennial (Tier 3):
- SIG Lite refresh
- News monitoring continues

Event-driven (any tier):
- Material change in service offering
- Breach
- Ownership change
- Geographic expansion
- New regulatory in scope
```

### Recipe 9: Stage 7 — Termination + Offboarding

```text
Pre-termination notice (30-90 days):
- Notify vendor in writing per contract
- Internal: notify users; document migration plan
- Legal: identify surviving obligations (data protection, confidentiality)

Termination day:
- Disable SSO grants
- Revoke API keys + service accounts
- Remove from CI/CD secrets
- Disable webhooks

Post-termination (30 days):
- Request data return (export per DPA)
- Request data destruction certification (per DPA §<X>)
- Vendor confirms destruction in writing
- File destruction certificate (retain per evidence schedule)

Post-termination (90 days):
- Confirm sub-processor cascade also terminated
- Re-screen for any residual access
- Update privacy policy (remove from sub-processor list)
- Notify customers if material processor change (per existing DPA terms)

Survival:
- Confidentiality (perpetual or per contract)
- Indemnification (per contract)
- Data protection (until destruction complete)
- Audit rights for retained records
```

### Recipe 10: Sub-processor change notification

```markdown
# Sub-Processor List Change Notice

To: Affected customers (per DPA notification list)
Date: <YYYY-MM-DD>

We are updating our sub-processor list:

## Added
- <Vendor X> — <purpose> — <jurisdiction> — effective <date>

## Removed
- <Vendor Y> — replaced <date>

## Modified
- <Vendor Z> — additional sub-processing scope <description>

## Your right to object
Per our DPA §<X>, you may object to this change within 30 days. To object,
reply to this email with reason.

## Sub-processor list URL
<https://co./trust/sub-processors>

Questions: privacy@<co>.

---
*Disclaimer per template.*
```

### Recipe 11: Vendor onboarding checklist

```markdown
# Vendor Onboarding — <Vendor>

## Pre-contract
- [ ] Pre-RFP security screen passed
- [ ] References checked (2-3)
- [ ] Initial BitSight / SS rating pulled
- [ ] Due diligence per tier complete

## Contract
- [ ] MSA + DPA + (BAA / SCC / industry addendum)
- [ ] Security addendum
- [ ] SLA agreed
- [ ] Termination + data return language confirmed
- [ ] Insurance certs received

## Provisioning
- [ ] SSO connected
- [ ] MFA enforced
- [ ] RBAC roles defined
- [ ] Least-privilege initial access
- [ ] Production access via approval workflow
- [ ] API key vault entry created

## Inventory + monitoring
- [ ] Added to vendor inventory tracker
- [ ] Tier assigned + documented
- [ ] BitSight / SS / UpGuard monitoring subscribed
- [ ] Bridge-letter / cert calendar entry
- [ ] Sub-processor disclosure updated in policy
- [ ] Status page subscribed
- [ ] Audit logs forwarded to SIEM (if supported)
- [ ] IR plan updated (detection source)

## Sign-off
- [ ] Security lead approval
- [ ] Privacy lead approval (if PII)
- [ ] Legal counsel approval (if novel terms)
- [ ] Executive approval (if Tier 1 critical or > $X spend)

---
*Disclaimer per template.*
```

### Recipe 12: Vendor offboarding checklist

```markdown
# Vendor Offboarding — <Vendor>

## Notice + planning
- [ ] Notice period started (per contract)
- [ ] Internal users notified
- [ ] Migration plan documented (if replacing)
- [ ] Data export plan (formats, locations)
- [ ] Survival obligations identified

## Termination day
- [ ] SSO grants revoked
- [ ] API keys + service accounts revoked
- [ ] CI/CD secret rotated/removed
- [ ] Webhooks disabled

## Data return
- [ ] Data exported (per DPA terms)
- [ ] Customer data exported (if customer-managed)
- [ ] Format verified

## Data destruction
- [ ] Destruction request issued
- [ ] Vendor certificate received
- [ ] Sub-processor flow-down destruction confirmed
- [ ] Filed in evidence repository

## Inventory updates
- [ ] Removed from vendor tracker
- [ ] Removed from sub-processor list (privacy policy)
- [ ] Monitoring disabled (BitSight subscription cancel)
- [ ] IR plan updated

## Final sign-off
- [ ] Security lead
- [ ] Privacy lead (if PII)
- [ ] Legal counsel (surviving obligations)

---
*Disclaimer per template.*
```

### Recipe 13: NIST SP 800-161 supply chain risk

```text
NIST SP 800-161 Rev. 1 (Federal SCRM) maps:
- C-SCRM (Cybersecurity SCRM) — vendor + sub-tier + open-source
- Tier-based risk integration (Enterprise / Mission/Business / System)
- Acquisition risk
- Geographic + foreign-ownership risk
- Counterfeit + tampering risk

Apply NIST 800-161 in addition to ISO 27001 A.5.19-23 + SOC 2 CC9.2 + 
PCI DSS Req. 12.8 when org has federal contracts, defense supply chain, or
critical infrastructure exposure.
```

## Examples

### Example 1: Stand up TPRM at a 50-person SaaS

**Goal:** Build TPRM program from zero in 30 days.

**Steps:**
1. Inventory discovery (Recipe 1): expect to find 80-150 vendors.
2. Tier each (Recipe 2). Tier 1: AWS, Stripe, Okta, Datadog, GitHub — 5-10. Tier 2: 20-30. Tier 3+4: rest.
3. Pull BitSight ratings on Tier 1 + 2.
4. Request SOC 2 / ISO from Tier 1 vendors.
5. DPA execution sweep — Tier 1 + 2 must have DPAs.
6. Set up continuous monitoring (BitSight + UpGuard) for Tier 1.
7. Document program in TPRM policy.

**Result:** TPRM program live in 30 days; auditable for SOC 2 CC9.2.

### Example 2: Vendor M&A re-rating

**Goal:** Tier 1 vendor acquired by larger entity; reassess.

**Steps:**
1. Re-pull BitSight + SS — new corporate GUID may apply.
2. Request acquirer's SOC 2 / ISO; confirm scope still covers acquired services.
3. Re-execute DPA under new entity name.
4. Re-screen acquirer for sanctions / PEP / adverse media.
5. Re-tier if material change in capability / data flow.
6. Notify customers of sub-processor entity change (Recipe 10).

**Result:** Continuity preserved; compliance maintained through M&A.

### Example 3: Offboarding a critical vendor with PHI

**Goal:** Replace EHR vendor; ensure HIPAA-compliant data return + destruction.

**Steps:**
1. Notice per contract (60 days).
2. New vendor migration parallel.
3. Export PHI (encrypted; check integrity).
4. Confirm last-active record date.
5. Request BAA-compliant destruction certificate (Recipe 12).
6. Vendor sub-processor (cloud hosting) confirms cascade destruction.
7. Retain destruction cert 6 years (HIPAA).

**Result:** Clean HIPAA-compliant offboarding; audit-ready evidence.

## Edge cases / gotchas

- **Shadow IT inventory gap is the #1 TPRM finding.** Re-run discovery quarterly.
- **Tiering must be data-driven, not vendor-self-reported.** Vendors will under-tier themselves.
- **Sub-processor change notice (Art. 28)** is mandatory per most DPAs; failure can void customer DPAs.
- **AWS / Azure / GCP DPAs cover only their direct services.** Sub-sub-processors (e.g., third-party SaaS hosted on AWS) need separate DPAs.
- **Continuous monitoring cost.** $50K-$500K/yr for BitSight + SS on dozens-hundreds of Tier 1 + 2 vendors. Scope strategically.
- **Audit rights are rarely exercised** but matter contractually for regulatory inquiries. Don't waive.
- **Vendor breach response calendar.** GDPR Art. 33 clock starts when YOU become aware — not when vendor notifies you. Demand fast vendor notification.
- **Acquisition re-tier risk.** Some vendors get acquired by entities in adverse-rated jurisdictions; re-screen.
- **Data destruction certification quality varies.** Demand SHA-256 of erased data set or NIST 800-88 r1 evidence; "we deleted it, trust us" is insufficient for HIPAA / GDPR audits.
- **Insurance cert renewals lapse silently.** Calendar each expiration.
- **DPA + contract drift.** Vendor updates ToS unilaterally; calendar review at renewal.
- **Free-tier monitoring caps.** BitSight + SS free for self only; vendor monitoring paid.
- **Regulator focus 2024-2026.** DORA (EU financial), NYDFS, OCC, FCA, MAS expect documented TPRM lifecycle + continuous monitoring.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [Shared Assessments (SIG)](https://sharedassessments.org/)
- [NIST SP 800-161 Rev. 1 (C-SCRM)](https://csrc.nist.gov/pubs/sp/800/161/r1/final)
- [NIST SCRM Topic](https://www.nist.gov/itl/smallbusinesscyber/guidance-topic/supply-chain-risk-management)
- [UpGuard TPRM playbook](https://www.upguard.com/blog/vendor-risk-management)
- [BitSight](https://www.bitsight.com/)
- [SecurityScorecard](https://securityscorecard.com/)
- [CSA Cloud Controls Matrix + CAIQ](https://cloudsecurityalliance.org/research/cloud-controls-matrix)
- [SCC 2021/914](https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj)
- [HHS Sample BAA](https://www.hhs.gov/hipaa/for-professionals/covered-entities/sample-business-associate-agreement-provisions/index.html)
- [DORA — EU](https://www.eiopa.europa.eu/digital-operational-resilience-act-dora_en)
- [NYDFS 23 NYCRR 500.11 (Third Party SP Security)](https://www.dfs.ny.gov/industry_guidance/cybersecurity)
