---
name: breach-notification-gdpr-72hr-state-laws
description: Breach notification matrix — GDPR Art. 33 (72h to SA) + Art. 34 (data subjects if high risk); UK GDPR (ICO 72h); US state laws (50 + DC + PR + USVI via NCSL); HIPAA §§164.404-408 (60-day individual + 500+ media + HHS portal); SEC 8-K Item 1.05 (4 business days material); NYDFS 23 NYCRR 500.17 (72h); EU NIS2 (24h early + 72h incident + 1mo final); EU DORA (4h major ICT + 1bd initial + 1mo final); GLBA Safeguards (30 days 500+).
---

# Breach Notification Matrix — GDPR + US State + Sector + Public-Company

Multi-regulator decision tree + notification packet templates + decision tree per scenario. Standard requires 72h GDPR; varies down to 4h (DORA major ICT) up to 60d (HIPAA individual).

## When to use

User says:
- "Breach notification" / "data breach notice"
- "GDPR 72 hour" / "Article 33" / "Article 34"
- "State breach law" / "NCSL" / "CCPA breach"
- "HIPAA breach" / "60 days"
- "SEC 8-K cyber" / "Item 1.05"
- "NYDFS breach" / "72 hour"
- "NIS2 24h" / "DORA 4h"
- "Breach decision tree"

Companion skills: `incident-response-nist-sp-800-61`, `hipaa-risk-assessment-baa`, `gdpr-article-30-ropa-dpia`.

## Setup

```bash
# Free public sources
# NCSL US State Breach Notification Laws
curl -fsSL https://www.ncsl.org/technology-and-communication/security-breach-notification-laws > /tmp/ncsl.html

# GDPR Articles
curl -fsSL https://gdpr-info.eu/art-33-gdpr/ > /tmp/art33.html
curl -fsSL https://gdpr-info.eu/art-34-gdpr/ > /tmp/art34.html

# HIPAA Subpart D
curl -fsSL https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html > /tmp/hipaa_breach.html

# SEC final rule (cyber disclosure)
curl -fsSL -o sec_cyber.pdf https://www.sec.gov/files/rules/final/2023/33-11216.pdf

# NYDFS 23 NYCRR 500
curl -fsSL https://www.dfs.ny.gov/industry_guidance/cybersecurity > /tmp/nydfs.html

# NIS2 + DORA
curl -fsSL https://digital-strategy.ec.europa.eu/en/policies/nis2-directive > /tmp/nis2.html
curl -fsSL https://www.eiopa.europa.eu/digital-operational-resilience-act-dora_en > /tmp/dora.html

# State AG breach portals — varies by state; lookup at NCSL or IAPP tracker.
```

## Common recipes

### Recipe 1: Breach decision matrix

| Regulator / law | Window | Trigger | Recipient | Format |
|---|---|---|---|---|
| GDPR Art. 33 | 72h from awareness | Personal data breach risking rights | Supervisory authority | DPA form per Member State |
| GDPR Art. 34 | "without undue delay" | High risk to rights/freedoms | Data subjects | Direct comms |
| UK GDPR | 72h | Same as GDPR | ICO | ICO online form |
| CCPA §1798.82 (CA) | "without unreasonable delay" | Unencrypted PI breach | Affected + Cal AG if 500+ | Required form |
| US state laws | 30-90d typical (varies) | PII breach | Affected + state AG + sometimes credit bureaus | Per state law |
| HIPAA §164.404 | 60d from discovery | Unsecured PHI breach | Affected individuals | Written |
| HIPAA §164.406 | 60d | Breach of 500+ residents of state | Prominent media in state | Press release |
| HIPAA §164.408 | 60d (500+); annual (<500) | All breaches | HHS OCR | Online portal |
| HIPAA BA → CE (§164.410) | 60d from discovery | BA's discovery of breach | Covered Entity | Written |
| SEC 8-K Item 1.05 | 4 business days from material determination | Material cybersecurity incident | SEC + investors | 8-K filing |
| NYDFS 23 NYCRR 500.17 | 72h from determination | Cybersecurity event | NYDFS | Online portal |
| EU NIS2 Art. 23 | 24h early warning + 72h incident + 1mo final | Significant incident (essential/important entities) | National CSIRT/CA | National portal |
| EU DORA Art. 19 | 4h (major ICT) + 1bd (initial) + 1mo (final) | Major ICT-related incident | National CA → ESAs | DORA framework |
| GLBA Safeguards (2024 update) | 30d | 500+ consumer security event | FTC | Online portal |
| PCI DSS (card brands) | Immediate | CHD breach | Acquirer/card brand | Forensic notification per agreement |
| FERPA | "without undue delay" + 60d notice | Education-record breach | Affected + DoE | Direct + DoE form |

### Recipe 2: GDPR Art. 33 + 34 — what constitutes a breach

```text
"Personal data breach" (GDPR Art. 4(12)):
"a breach of security leading to the accidental or unlawful destruction,
loss, alteration, unauthorised disclosure of, or access to, personal data
transmitted, stored or otherwise processed."

Three categories (Working Party 250 + EDPB):
1. Confidentiality breach — unauthorized disclosure / access
2. Integrity breach — unauthorized alteration
3. Availability breach — accidental loss / destruction

Notification thresholds:
- Art. 33 to SA: ANY breach UNLESS unlikely to result in risk to rights.
- Art. 34 to data subjects: HIGH risk to rights.

GDPR Art. 33 timing:
- "without undue delay and, where feasible, not later than 72 hours after
  having become aware"
- "Where the notification to the supervisory authority is not made within
  72 hours, it shall be accompanied by reasons for the delay."
- Phased notification allowed when facts incomplete.

What "awareness" means: when controller has reasonable degree of certainty
that a security incident occurred that led to personal data being
compromised. NOT when controller first heard a rumor.
```

### Recipe 3: GDPR Art. 33 notification packet template

```markdown
# Personal Data Breach Notification — GDPR Art. 33

**To:** <Lead Supervisory Authority>
**From:** <Controller name> (DPO contact: <email>)
**Date of notification:** <YYYY-MM-DD HH:MM UTC>
**Awareness date:** <YYYY-MM-DD HH:MM UTC>
**Within 72 hours?** Yes / No (if No: justification)

## 1. Nature of the breach (Art. 33(3)(a))
- Type: Confidentiality / Integrity / Availability
- Description: <what happened>
- Categories of data subjects affected: <list>
- Approximate number of data subjects: <#>
- Categories of personal data: <list — incl. special category if applicable>
- Approximate number of records: <#>

## 2. DPO / contact (Art. 33(3)(b))
<Name + role + email + phone>

## 3. Likely consequences (Art. 33(3)(c))
<Impact on data subjects — identity theft, financial loss, discrimination,
reputational damage, etc.>

## 4. Measures taken or proposed (Art. 33(3)(d))
- Containment: <actions>
- Investigation: <ongoing — partner firms>
- Mitigation: <data subject support — credit monitoring, etc.>
- Remediation: <root cause fixes>

## 5. Cross-border processing
- Lead SA: <named SA>
- Other SAs concerned: <list>

## 6. Phased notification (if applicable)
- Initial information; further information to follow by <date>.

## 7. Signature
DPO: <name + date>
```

### Recipe 4: GDPR Art. 34 data subject notification template

```markdown
# Important: Data Security Incident Notification

**Date:** <YYYY-MM-DD>
**Reference:** <Incident ID>

Dear <name>,

We are writing to notify you of a data security incident that may affect
your personal information.

## What happened
On <date>, we discovered that <description of breach>. Our investigation
indicates that <attacker / cause> may have accessed your information.

## What information was involved
The incident may have involved the following information about you:
- <Category 1>
- <Category 2>
- (NOT: <financial / SSN / etc. if not actually involved>)

## What we are doing
- Engaged forensic firm + breach coach
- Notified <supervisory authority>
- Implemented additional security measures
- Providing <free credit monitoring + ID theft protection>

## What you should do
- <Reset password if applicable>
- <Monitor accounts for suspicious activity>
- <Free credit monitoring enrollment URL>
- <Identity Theft Hotline: 1-877-IDTHEFT (US) or local equivalent>

## More information
Contact <DPO email + phone>. Visit <FAQ URL> for updates.

Sincerely,
<Co. name>

---
*This communication is required by law and may not be reproduced.*
```

### Recipe 5: US state breach notification — pattern + state variation

```text
NCSL maintains the canonical list (https://www.ncsl.org/...).

Typical state law structure:
1. "Personal information" definition — name + (SSN OR DL OR financial
   account OR medical OR biometric OR username+password).
2. "Breach" definition — unauthorized acquisition of unencrypted PI.
3. Encryption safe harbor — if encrypted AND key not breached, no notice.
4. Timing: "most expedient time possible and without unreasonable delay"
   OR specific days (30-90 typical).
5. Recipients: affected residents + state AG + sometimes consumer reporting
   agencies (3 nationwide if 1000+).
6. Method: written OR email + posting OR substitute notice if cost-
   prohibitive (>$250K OR >500K affected OR no addresses).
7. Content: incident description + types of info + steps to protect + 
   contact info.

State-specific notable rules:
- California (CCPA §1798.82 + AG portal at 500+): submit copy of notice to
  Cal AG.
- Massachusetts (M.G.L. c. 93H): requires WISP (Written Info Sec Plan).
- New York SHIELD Act: covers electronic + paper.
- Texas (TX Bus. & Com. Code §521): notify TX residents in any state.
- Illinois PIPA: 500+ → IL AG within 5 business days.
- Florida Information Protection Act: 30 days.
- Connecticut (CTPSL): 90 days max + 60 to credit monitoring (if SSN).
- Vermont (9 V.S.A. §2435): 45 days; sliced rules for unauthorized
  acquisition vs access.
```

### Recipe 6: HIPAA §§164.404-408 breach notification

```text
Breach (§164.402):
- Acquisition, access, use, disclosure of unsecured PHI not permitted.
- Presumed breach UNLESS low-probability of compromise per 4-factor risk
  assessment:
  (1) Nature + extent of PHI
  (2) Unauthorized recipient
  (3) Whether PHI was actually acquired/viewed
  (4) Mitigation extent

Unsecured PHI: not rendered unusable/unreadable. Encryption (AES + key
control) + destruction = "secured" per HHS guidance.

Notifications:
- Individuals (§164.404): 60 days from discovery; written via first-class
  mail OR email if individual agreed.
- Media (§164.406): if 500+ residents of state, prominent media outlet,
  60 days.
- HHS (§164.408):
  - 500+: 60 days, online portal (https://ocrportal.hhs.gov/ocr/breach).
  - <500: annually by Feb 60 days after year end.

BA → CE (§164.410): 60 days from BA's discovery; written; identify each
individual affected.

Substitute notice (§164.404(d)): if insufficient or out-of-date contact
info for ≥10 individuals, post on home page for 90 days OR major print/
broadcast media + toll-free 90-day hotline.
```

### Recipe 7: HIPAA breach notification template (individual)

```markdown
[Letterhead]
<Date — within 60 days of discovery>

<Patient Name>
<Address>

Re: Notice of Data Security Incident

Dear <name>,

We are writing to inform you of a recent security incident that may have
affected your protected health information.

## What happened
On <date>, <description of incident>.

## Information involved
The incident may have involved your: <name, DOB, MRN, address, diagnosis,
treatment, payment info — list specific categories>.

## What we are doing
- Engaged forensic specialists
- Notified HHS OCR
- Implemented enhanced safeguards

## What you can do
- Review your medical bills for unfamiliar charges
- Monitor your credit reports (free 1x/yr from each bureau)
- Place a fraud alert via Equifax/Experian/TransUnion
- We are offering <X months of free credit monitoring + identity theft
  protection> — enrollment URL: <link>

## For more information
Contact us at <phone> or <email>. Visit <FAQ URL>.

Sincerely,
<Privacy Officer Name>
<Covered Entity>

---
*Required by 45 CFR §164.404.*
```

### Recipe 8: SEC 8-K Item 1.05 cyber disclosure

```text
SEC Rule 33-11216 (effective Dec 2023 large filer; June 2024 smaller).

Trigger: registrant determines that a cybersecurity incident is MATERIAL.

Timeline: 4 business days from materiality determination.

Materiality assessment:
- Quantitative + qualitative factors
- Affected systems, data, operations
- Customer + supplier impact
- Financial harm
- Reputational harm
- Legal + regulatory exposure
- Strategic / competitive impact

Permissible delay: U.S. Attorney General determines disclosure poses
substantial risk to national security or public safety (max 30 days +
extensions).

Item 1.05 content:
- Material aspects of nature, scope, timing
- Material impact OR reasonably likely material impact on registrant
- Refer to Form 10-K Item 1C (Cybersecurity disclosure — risk mgmt,
  strategy, governance — annual).

Amendments required for material updates within 4 business days.

Annual disclosure (10-K Item 1C):
- Risk management + strategy
- Governance + Board oversight
- Management role + expertise
```

### Recipe 9: NYDFS 23 NYCRR 500.17 (72h)

```text
Covered entity (NY-licensed financial entity).

72h notification trigger:
- Has affected any material part of normal operations, AND
- Notice required to any government body, self-regulatory body, or any other
  supervisory body, AND
- Reasonable likelihood of materially harming any material part of the
  normal operations of the Covered Entity.

OR

- A cybersecurity event that is determined to have impacted nonpublic
  information.

Notification: NYDFS online portal.

Annual cyber compliance certification (§500.17(b)): submitted via online
portal by April 15.

500.17 amendments effective Nov 2023 (Phase 1) + 2024-2025 (Phase 2)
expanded governance requirements + ransom payment notification.

Ransom payment: 24h notification of payment; 30 days to file explanation
+ alternatives considered.
```

### Recipe 10: EU NIS2 Art. 23 + DORA Art. 19

```text
NIS2 (Directive (EU) 2022/2555):
- Applies to "essential entities" + "important entities" (large + medium
  in critical sectors).
- 24-hour EARLY WARNING (no detail required; just notice).
- 72-hour INCIDENT NOTIFICATION (description + indicators of compromise +
  type of threat).
- 1-month FINAL REPORT (detailed incident description + severity + cause +
  ongoing impact + cross-border).

DORA (Regulation (EU) 2022/2554):
- Applies to financial entities + ICT third-party providers.
- 4 HOURS for MAJOR ICT-related incident initial classification.
- 1 BUSINESS DAY initial notification to NCA.
- 1 MONTH final report.

Cybersecurity incident classification (NIS2):
- Significant incident definition (Art. 23(3)):
  - Causes or capable of causing severe operational disruption OR financial
    loss OR considerable material/non-material damage by affecting other
    natural/legal persons.
```

### Recipe 11: Combined notification timeline matrix

```text
Per scenario, what regulators have you triggered?

| Sector / data | Regulators triggered |
|---|---|
| EU personal data of any kind | GDPR Art. 33 (72h SA) + Art. 34 (data subjects if high risk) |
| EU + US dual exposure | Above + US state laws |
| US PII | State law of each affected state + Cal AG (CCPA) if CA |
| PHI in US | HIPAA Subpart D + state laws (if PI overlap) |
| US financial customer | GLBA Safeguards 2024 update (30d 500+) + state |
| EU financial (DORA) | DORA 4h + 1bd + 1mo + NIS2 (overlap) |
| EU essential entity | NIS2 24h + 72h + 1mo |
| US-listed company material | SEC 8-K 4bd + state + GDPR (if EU customers) |
| NY-licensed financial | NYDFS 72h + state laws + GLBA + SEC if listed |
| CHD breach | Card brand acquirer (per agreement) + state PI laws |
| DoD contractor | DoD DIBNet 72h + state |
| Education records | FERPA + state |
| Children online | COPPA + state |

Build matrix per incident; coordinate breach coach.
```

### Recipe 12: Notification cost ranges (US, 2026)

```text
Per affected individual:
- Notification letter postage + production: $1-$3
- Email notification: $0.05-$0.50
- Substitute notice (web + media): $50K-$500K
- Credit monitoring (1yr free): $10-$30/individual
- Identity theft protection: $5-$20/individual
- Hotline (60-90 days): $50K-$200K
- Forensics: $25K-$500K depending on scope
- Breach coach legal fees: $50K-$1M+
- PR: $25K-$200K

Per-record total range: $150-$300+ direct cost + indirect.

Ponemon Cost of Data Breach Report (annual):
- Global avg: $4.88M (2024)
- US avg: $9.36M
- Healthcare: $9.77M
- Financial: $6.08M

Insurance recovers fraction; check policy sublimits.
```

### Recipe 13: Notification document inventory

```text
Required artifacts to retain:
- Awareness timeline (when did we know what)
- Risk assessment (4-factor for HIPAA; rights-risk for GDPR)
- 4-factor decision (HIPAA) OR Art. 33 decision (GDPR)
- All notifications sent (regulator + individuals + media)
- Acknowledgment receipts
- Sample letters + variations
- Substitute notice posting (web archive)
- Hotline transcript summaries
- Vendor / forensic / breach coach engagement letters + reports
- Insurance claim correspondence
- Post-incident review

Retention: 6 years HIPAA; 3-7 years GDPR (per Member State DPA); 5 years
NYDFS; 7+ years for litigation hold.
```

## Examples

### Example 1: 72h GDPR notification

**Goal:** Confirmed EU customer data exposure; notify lead SA + assess Art. 34.

**Steps:**
1. T+0: SOC discovers EDR alert → confirms breach.
2. T+2h: Containment; DPO notified.
3. T+24h: Initial risk assessment; 50K EU records confirmed exposed.
4. T+48h: Art. 33 packet drafted (Recipe 3); breach coach reviews.
5. T+70h: Submit to Irish DPC (lead SA per main establishment).
6. T+72h: Acknowledgment received.
7. T+5d: Art. 34 individual notice — high risk to rights given record categories.
8. T+30d: Final report to DPC.

**Result:** Compliant GDPR notification; auditable evidence.

### Example 2: SEC 8-K Item 1.05

**Goal:** Cyber incident materiality determination → 4-business-day 8-K.

**Steps:**
1. Materiality assessment with counsel + board's audit committee.
2. Determined material: confirmed unauthorized access to customer DB + financial impact >$10M.
3. T+0 (materiality determination): start 4-business-day clock.
4. Draft 8-K Item 1.05 with disclosure counsel (Recipe 8).
5. T+4bd: File 8-K via EDGAR.
6. Subsequent 8-K amendments for material updates.

**Result:** SEC compliance; minimized investor uncertainty.

### Example 3: HIPAA breach 750 affected

**Goal:** 750 patient records exposed (500+ threshold triggers media).

**Steps:**
1. Risk assessment (4-factor); confirms breach.
2. 60-day clock starts on discovery.
3. Notifications (Recipe 7) to all 750 individuals.
4. Media notification — prominent outlet in state (Recipe 6).
5. HHS OCR portal submission (Recipe 6).
6. State law overlay (CCPA if any CA residents).
7. Free credit monitoring + identity theft protection.
8. PIR; document retention 6 years.

**Result:** Compliant HIPAA breach response.

## Edge cases / gotchas

- **"Awareness" GDPR — controller-side definition.** "When you have a reasonable degree of certainty that a security incident occurred." Document why earlier awareness wasn't reached.
- **Materiality SEC isn't a count threshold.** Qualitative factors matter; consult counsel.
- **HHS portal small breach (<500) annual reporting.** Calendar Feb 28 each year.
- **CCPA + state AG portal at 500+.** Cal AG portal (https://oag.ca.gov/privacy/databreach/list) requires sample notice + count.
- **State AG portals vary widely** — some online, some PDF email; track per state.
- **Substitute notice expensive.** Only when actual notice infeasible; document.
- **Encryption safe harbor varies.** HIPAA safe harbor per HHS guidance (AES + key control); state laws sometimes broader.
- **Credit monitoring vs identity theft protection** — different offerings; choose based on harm.
- **Don't notify individuals before regulators** unless tight call; GDPR has staggered structure (SA first).
- **Coordinate with law enforcement.** Notifications can be delayed if law enforcement requests; document.
- **EU lead SA (one-stop-shop) selection** — main establishment determines lead SA. Cross-border processing.
- **Multilingual notices for EU + multinational** — use translation services + back-translation verification.
- **Bridge between vendor + your own breach** — vendor's clock and your clock are different; YOUR clock starts on YOUR awareness.
- **PCI brand-specific timing** varies per acquirer agreement; immediate notification common.
- **OFAC ransom check before paying.** Treasury Oct 2020 + Sept 2022 advisories.
- **Press release timing.** Coordinate with SEC 8-K + GDPR Art. 34 (which is "without undue delay" but accommodates regulator-first).
- **Litigation hold** — initiate at first indication of breach; preserve everything.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [GDPR Art. 33](https://gdpr-info.eu/art-33-gdpr/)
- [GDPR Art. 34](https://gdpr-info.eu/art-34-gdpr/)
- [EDPB Guidelines on personal data breach notification](https://edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-92022-personal-data-breach-notification_en)
- [ICO breach reporting (UK)](https://ico.org.uk/for-organisations/report-a-breach/)
- [NCSL US State Breach Laws](https://www.ncsl.org/technology-and-communication/security-breach-notification-laws)
- [Cal AG Breach Portal](https://oag.ca.gov/privacy/databreach/list)
- [HHS Breach Notification Rule](https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html)
- [HHS Breach Portal](https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf)
- [SEC Final Rule 33-11216 (Cyber Disclosure)](https://www.sec.gov/files/rules/final/2023/33-11216.pdf)
- [NYDFS 23 NYCRR 500](https://www.dfs.ny.gov/industry_guidance/cybersecurity)
- [EU NIS2 Directive (2022/2555)](https://eur-lex.europa.eu/eli/dir/2022/2555/oj)
- [EU DORA (2022/2554)](https://eur-lex.europa.eu/eli/reg/2022/2554/oj)
- [GLBA Safeguards Rule (2024 update)](https://www.ftc.gov/legal-library/browse/rules/safeguards-rule)
- [IAPP US State Privacy Tracker](https://iapp.org/resources/article/us-state-privacy-legislation-tracker/)
- [Ponemon Cost of Data Breach Report](https://www.ibm.com/reports/data-breach)
- [Treasury OFAC Ransomware Advisory (2020)](https://home.treasury.gov/system/files/126/ofac_ransomware_advisory.pdf)
