---
name: vendor-security-questionnaire-caiq-sig
description: Answer + send vendor security questionnaires — CAIQ v4 (Cloud Security Alliance — 261 Qs across 17 CCM domains), SIG (Shared Assessments — Lite ~125Q / Core ~700Q / Plus ~1100Q), SOC 2 report sharing under NDA, ISO 27001 cert + SoA. SOTA workflow: maintain Trust Center (Vanta Trust Reports / Drata Trust Center / Secureframe Trust / Whistic Trust Vault) auto-answering 80%+. Custom questions via control mapping. AI-assist: Vanta AI Q&A / Drata AI / Loopio.
---

# Vendor Security Questionnaire — CAIQ / SIG / Custom + Trust Center

CAIQ v4 (Cloud Security Alliance — 261 Q) and SIG (Shared Assessments — Lite/Core/Plus) are the two dominant questionnaire standards. SOC 2 + ISO 27001 + DPA + BAA layer on. Trust Centers auto-answer common questions; AI-assist (Loopio, Vanta AI, Drata AI) accelerates custom answers.

## When to use

User says:
- "CAIQ" / "Cloud Controls Matrix"
- "SIG" / "Shared Assessments"
- "Vendor security questionnaire" / "VSQ"
- "Trust Center" / "Trust Vault"
- "Loopio" / "Vanta AI Q&A" / "Drata AI"
- "Customer security review"
- "Procurement security questionnaire"

Companion skills: `drata-vanta-secureframe-soc2-monitoring`, `vendor-risk-bitsight-securityscorecard-upguard`, `tprm-third-party-risk-lifecycle`.

## Setup

```bash
# Free standards
# CSA CAIQ v4 + CCM v4
curl -fsSL https://cloudsecurityalliance.org/research/cloud-controls-matrix > /tmp/ccm.html
# Direct download (XLSX with all 261 questions)
# https://cloudsecurityalliance.org/research/cloud-controls-matrix-v4

# Shared Assessments SIG
curl -fsSL https://sharedassessments.org/sig/ > /tmp/sig.html
# Lite ~125Q; Core ~700Q; Plus ~1100Q

# Trust Centers
# https://trust.vanta.com/
# https://drata.com/trust-center
# https://secureframe.com/trust
# https://www.whistic.com/

# AI-assist
# https://loopio.com/
# https://www.vanta.com/products/questionnaire-automation
# https://drata.com/ai

export VANTA_API_KEY=<dashboard>
export DRATA_API_KEY=<dashboard>
export LOOPIO_API_KEY=<dashboard>
export WHISTIC_API_KEY=<dashboard>
```

## Common recipes

### Recipe 1: Questionnaire taxonomy

```text
CAIQ v4 (Cloud Security Alliance):
- 261 questions across 17 CCM domains
- Yes / No / Yes-NA / Yes-with-comment / etc.
- Aligned to CCM v4
- Most used for SaaS vendor due diligence
- Cloud Provider Onboarding

SIG (Shared Assessments — Lite / Core / Plus):
- Lite: ~125 Qs for low-risk vendors
- Core: ~700 Qs for mid-risk
- Plus: ~1100 Qs for high-risk (mature TPRM)
- Industry-aligned (financial, healthcare, retail)
- Yes/No + explanation

SOC 2 Type II report:
- Shared under NDA
- Full report (description + controls + tests + results)
- Public alternative: Trust Center summary

ISO 27001 cert + SoA:
- Cert from accredited body
- SoA listing 93 Annex A controls

VSAQ (Vendor Security Assessment Questionnaire):
- Google's open-source format
- 150+ Qs, JSON-based
- Less common in 2026

Custom:
- Industry-specific (HIPAA-specific, PCI-specific)
- Customer-specific (large enterprise often)
- Lawyer-driven additions
```

### Recipe 2: CCM v4 17 domains (CAIQ structure)

```text
A&A   Audit & Assurance
AIS   Application & Interface Security
BCR   Business Continuity Management & Operational Resilience
CCC   Change Control & Configuration Management
CEK   Cryptography, Encryption & Key Management
DCS   Datacenter Security
DSP   Data Security & Privacy Lifecycle Management
GRC   Governance, Risk & Compliance
HRS   Human Resources Security
IAM   Identity & Access Management
IPY   Interoperability & Portability
IVS   Infrastructure & Virtualization Security
LOG   Logging and Monitoring
SEF   Security Incident Management, E-Discovery & Cloud Forensics
STA   Supply Chain Management, Transparency & Accountability
TVM   Threat & Vulnerability Management
UEM   Universal Endpoint Management
```

### Recipe 3: SIG sections (Lite / Core / Plus)

```text
A — Risk Management
B — Security Policy
C — Organizational Security
D — Asset & Information Management
E — Human Resources Security
F — Physical & Environmental
G — IT Operations
H — Access Control
I — Application Security
J — Cybersecurity Incident Management
K — Operational Resilience (BCDR)
L — Compliance
M — End User Computing
N — Network Security
O — Privacy
P — Threat Management
R — Server Security
S — Supplier Risk Management
T — Cloud Service Provider
U — Communications
V — Mobile
W — Information Disposal

SIG Lite — abbreviated coverage; ~125 Qs.
SIG Core — moderate coverage; ~700 Qs.
SIG Plus — exhaustive; ~1100 Qs.
```

### Recipe 4: Trust Center setup

```text
Trust Center = public-facing security + compliance microsite. Goal: answer
80%+ of common questions WITHOUT custom questionnaire effort.

Components:
- SOC 2 Type II report (gated by NDA)
- ISO 27001 cert (public)
- HIPAA / PCI / etc. attestations
- Sub-processors list (live)
- Bug bounty / VDP / security.txt
- Privacy policy + DPA
- Sample BAA + SCC
- DPA + service-provider terms
- Encryption + data residency overview
- Penetration test executive summary
- Continuous monitoring status (live BitSight / SS scores)

Platforms:
- Vanta Trust Reports — auto-publishes evidence
- Drata Trust Center
- Secureframe Trust
- Whistic Trust Vault (vendor-managed; customers request access)
- DIY (Notion / WordPress)

Goal: pivot from "complete this 1100-Q SIG Plus" to "visit our Trust Center
+ specific custom Qs."
```

### Recipe 5: Vanta Trust Report API

```bash
# https://developer.vanta.com/
# List trust reports
curl -X GET 'https://api.vanta.com/v1/trust-reports' \
  -H "Authorization: Bearer $VANTA_API_KEY"

# Share trust report with customer
curl -X POST 'https://api.vanta.com/v1/trust-reports/<id>/shares' \
  -H "Authorization: Bearer $VANTA_API_KEY" \
  -d '{"email":"customer@<domain>","expires_in_days":30}'
```

### Recipe 6: Answering CAIQ — example

```markdown
# CAIQ Response — <Customer>

**Date:** <YYYY-MM-DD>
**Author:** <Sec Lead>
**Trust Center URL:** https://trust.<co>.com

## A&A-01 Audit Planning

**Question:** Are formal IT audits, risk assessments, and compliance
reviews of the organization performed at least annually?

**Answer:** Yes

**Comment:** SOC 2 Type II audit performed annually (Schellman); ISO 27001
surveillance audit annually (Schellman); internal ISMS audit per ISO 27001
Clause 9.2 annually; risk assessment + management review per ISO 27005.

**Evidence:** SOC 2 Type II Section 4 + ISO 27001 cert (Trust Center).

## A&A-02 Independent Audits

**Question:** Are independent audit assessments performed by qualified
third parties at least annually?

**Answer:** Yes

**Comment:** Schellman & Co. (AICPA-registered) for SOC 2 + ISO 27001.

**Evidence:** SOC 2 + ISO Cert.

(... continue for all 261 questions ...)

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

### Recipe 7: Loopio AI auto-answer workflow

```text
Loopio = response automation platform. AI-suggests answers from your
knowledge base.

Workflow:
1. Build answer library (FAQ + past questionnaires + policies).
2. Upload customer questionnaire (CAIQ / SIG / custom).
3. Loopio AI matches questions to library; suggests answers.
4. Human review + refine.
5. Export back to customer's format.

Reduces effort 50-80% on repeat questionnaire types.

Alternatives:
- Vanta AI Questionnaire Automation
- Drata AI Q&A
- Responsive (formerly RFPIO)
- Responsive (formerly Loopio competitor)
- Manual + Notion-based answer bank
```

### Recipe 8: Answer bank knowledge base structure

```text
Maintain Q→A library by topic:

Encryption:
Q: "Is data encrypted at rest?" 
A: "Yes. AES-256-GCM via AWS KMS with customer-managed key option."

Q: "Is data encrypted in transit?"
A: "Yes. TLS 1.3 enforced; legacy TLS 1.2 minimum."

Access control:
Q: "Is MFA enforced?"
A: "Yes. MFA mandatory for all employees per Access Control Policy. SSO 
   via Okta with mandatory hardware token for privileged users."

(continue across categories)

Storage:
- Notion / Confluence / Google Doc
- Or in-platform (Vanta / Drata / Loopio)

Maintenance:
- Quarterly review (answers can drift)
- Tag with control IDs + framework alignment
- Version + date stamp
```

### Recipe 9: SOC 2 report sharing workflow

```text
SOC 2 reports are confidential. Distribution requires NDA.

Workflow:
1. Customer requests report via Trust Center / sales.
2. DocuSign NDA (3-5 minutes).
3. Auto-deliver SOC 2 Type II PDF (Vanta / Drata / Secureframe automates).
4. Log distribution per audit requirements.

Trust Center → public summary (controls list, attestation letter)
without report.
```

### Recipe 10: Whistic Trust Vault

```text
Whistic operates a vendor-side Trust Vault:
- Vendor publishes evidence once (SOC 2, ISO, CAIQ, SIG, policies).
- Customers request access via Vault.
- Vendor approves (auto + manual).
- Updates propagate automatically.

Vendor side:
- Sign up at whistic.com
- Curate Vault with current evidence
- Set approval policies (auto for known logos, manual for new)
- Update SOC 2 + ISO + pen-test annually

Customer side:
- Search vendor in Whistic
- Request Vault access
- Receive evidence package

Reduces repeated questionnaire fatigue for vendor.
```

### Recipe 11: Handling questionnaire follow-ups

```text
After initial response, customer security team may follow up:
- Clarifying questions
- Evidence requests (logs, configs, screenshots)
- Phone call / Zoom walkthrough
- On-site visit (large enterprise; rare now)

Etiquette:
- 2-business-day SLA on clarifications
- Pre-redact evidence (don't expose unrelated data)
- NDA-gate sensitive evidence
- Loop in customer's procurement to keep timeline visible
```

### Recipe 12: Multi-framework efficiency

```text
Mature TPRM teams accept ONE response covering multiple frameworks:
- SOC 2 + ISO 27001 + HIPAA + CSA CAIQ + SIG → ONE answer set tagged.

Build answer bank with framework tagging:
- "Access control" → SOC 2 CC6.1 + ISO A.5.15-16 + HIPAA §164.308(a)(3) +
  CAIQ IAM-01 + SIG H1.

Customer sends CAIQ → filter answer bank to CAIQ-tagged answers.
Customer sends SIG → filter to SIG-tagged.

One source of truth → many outputs.
```

### Recipe 13: Cost + time benchmarks (per questionnaire)

```text
Full SIG Plus (1100 Q): 40-100 hours analyst time without automation.
With Loopio + answer bank: 8-20 hours.
With Trust Center deflection: customers may skip full SIG; just custom Qs.

CAIQ v4 (261 Q): 8-20 hours raw; 2-4 with automation.

SIG Core (700 Q): 24-60 hours raw; 6-12 with automation.

SIG Lite (125 Q): 4-8 hours raw; 1-2 with automation.

Custom (100-500 Q): variable.

Cost reduction priority:
1. Trust Center (deflect repeat questions).
2. Answer bank (cross-framework).
3. AI-assist (Loopio / Vanta AI / Drata AI).
```

## Examples

### Example 1: Build Trust Center

**Goal:** Set up Vanta Trust Center to deflect 70% of vendor questionnaires.

**Steps:**
1. Vanta Trust Reports configured.
2. Publish SOC 2 (gated NDA), ISO cert, DPA, BAA.
3. Sub-processors list live-updated.
4. Privacy policy + security.txt published.
5. Continuous monitoring badge.
6. URL: trust.<co>.com.
7. Sales team trained to direct customers there first.

**Result:** ~70% of customer security reviews satisfied by Trust Center alone.

### Example 2: Respond to SIG Plus (1100 Q)

**Goal:** Answer SIG Plus for enterprise customer in 5 days.

**Steps:**
1. Receive SIG Plus Excel.
2. Run through Loopio AI matching.
3. ~700 auto-suggested answers from library.
4. Manual answer 400 novel questions.
5. SME review for high-risk topics (encryption, IR).
6. Export + return to customer.
7. Add new answers to library for next time.

**Result:** SIG Plus complete in 12 hours of analyst time vs 60+ manual.

### Example 3: Industry-specific questionnaire

**Goal:** Customer sends HIPAA-specific 250 Q.

**Steps:**
1. Identify overlap with HIPAA-tagged answers in library.
2. Map remaining novel questions to HIPAA Privacy + Security Rule + BAA controls.
3. Coordinate with privacy lead for novel questions.
4. Send completed response.

**Result:** Compliant response; library grew for next HIPAA customer.

## Edge cases / gotchas

- **Don't over-promise.** Answer truthfully; "Yes" without controls = lawsuit risk later.
- **Roadmap items** — distinguish current state from planned (Q1 2027) features.
- **Carve-outs** — note sub-service org (AWS / GCP) inherited controls explicitly.
- **CAIQ + SIG version updates** — quarterly. Keep library current.
- **Custom questions** can ask for things you don't do (e.g., FIPS 140-3 hardware). Document gracefully — "Not currently; alternative compensating control X."
- **Trust Center NDA-gating SOC 2.** Automate to reduce friction.
- **Customer requests evidence (screenshots).** Pre-redact + watermark.
- **Annual refresh of public Trust Center content.** Stale SOC 2 / ISO cert in Trust Center = lost deals.
- **Procurement timing** — answer turnaround beats 30+ day legal review when sales pushed.
- **Loopio + Vanta AI hallucinations** — AI suggestions need SME review; never auto-send.
- **GDPR + DPA + SCC + TIA** — pre-build for EU customers; legal review.
- **Sub-processor change updates** — customers expect 30-day notice; sync with TPRM.
- **AI questionnaire fatigue.** Some customers send hostile / cookie-cutter 1100Q; push back with Trust Center + scoped customs only.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [Cloud Security Alliance — CCM + CAIQ](https://cloudsecurityalliance.org/research/cloud-controls-matrix)
- [CSA CAIQ v4 Download](https://cloudsecurityalliance.org/research/cloud-controls-matrix-v4)
- [Shared Assessments SIG](https://sharedassessments.org/sig/)
- [Vanta Trust Reports](https://www.vanta.com/products/trust-center)
- [Drata Trust Center](https://drata.com/trust-center)
- [Secureframe Trust](https://secureframe.com/products/trust-center)
- [Whistic Trust Vault](https://www.whistic.com/)
- [Loopio](https://loopio.com/)
- [Responsive (formerly RFPIO)](https://www.responsive.io/)
- [Google VSAQ](https://github.com/google/vsaq)
- [HHS Sample BAA](https://www.hhs.gov/hipaa/for-professionals/covered-entities/sample-business-associate-agreement-provisions/index.html)
- [SCC 2021/914](https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj)
