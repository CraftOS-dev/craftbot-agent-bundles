---
name: whistleblower-program-navex-ethicspoint
description: Whistleblower program design + operation per EU Whistleblower Directive 2019/1937 + SOX 806 + Dodd-Frank + state laws. Internal + external reporting channels, confidentiality + non-retaliation, 7-day acknowledgment + 3-month response. 2026 SOTA: NAVEX EthicsPoint (largest), Lighthouse Services, Convercent (OneTrust), Whispli, FaceUp (EU strong), AllVoices, Speakfully. Multi-channel (web/phone/app), multi-language, anonymous option, case management with chain-of-custody.
---

# Whistleblower / Ethics Hotline Program

EU Whistleblower Directive 2019/1937 mandatory for orgs 50+ EE (phased). SOX 806 + Dodd-Frank whistleblower protections (US public). Multi-channel intake; non-retaliation; case management chain-of-custody.

## When to use

User says:
- "Whistleblower program" / "ethics hotline"
- "EU Whistleblower Directive" / "2019/1937"
- "SOX 806" / "Sarbanes-Oxley whistleblower"
- "Dodd-Frank whistleblower"
- "NAVEX EthicsPoint" / "Lighthouse Services" / "Whispli" / "FaceUp"
- "Code of Conduct" / "anti-retaliation"
- "Internal reporting channel"

Companion skills: `policy-authoring-cybersecurity-aup-byod`, `incident-response-nist-sp-800-61`.

## Setup

```bash
# EU Whistleblower Directive 2019/1937
curl -fsSL https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32019L1937 > /tmp/euwbd.html

# SOX (Sarbanes-Oxley Act §806)
curl -fsSL https://www.congress.gov/bill/107th-congress/house-bill/3763 > /tmp/sox.html

# Dodd-Frank Section 922 (SEC whistleblower)
curl -fsSL https://www.sec.gov/whistleblower > /tmp/sec_wb.html

# Paid platforms
# https://www.navex.com/en-us/products/navex-one-grc-information-system/ethicspoint-hotline-incident-management/
# https://www.lighthouse-services.com/
# https://www.convercent.com/
# https://www.whispli.com/
# https://faceup.com/
# https://www.allvoices.co/
# https://www.speakfully.com/

export NAVEX_API_KEY=<dashboard>
export WHISPLI_API_KEY=<dashboard>
export FACEUP_API_KEY=<dashboard>
```

## Common recipes

### Recipe 1: EU Whistleblower Directive 2019/1937 — applicability

```text
Effective: Dec 17, 2021 (large entities); Dec 17, 2023 (50-249 EE
private + smaller municipalities).

Scope:
- Legal entities in private sector with 50+ EE
- Public sector entities (subject to Member State threshold)
- Specific sectors regardless of size (financial services per Anti-Money
  Laundering Directive)

Internal reporting channel requirements (Art. 8):
- Confidential + secure intake
- Acknowledgment within 7 days
- "Diligent follow-up" (investigation)
- Feedback within 3 months
- Person/dept designated to receive + handle reports

External reporting (Art. 11):
- Member State authority (varies — typically national ombudsman, labor
  inspectorate, financial regulator)
- Used when internal not appropriate

Public disclosure (Art. 15):
- Allowed as last resort if no action OR imminent harm

Protected from retaliation (Art. 19):
- Termination, demotion, harassment, blacklisting, etc.
- Reverse burden of proof
- Remedies + compensation

Scope of reportable matters (Art. 2):
- Breaches of Union law in: public procurement, financial services,
  product safety, environmental protection, public health, consumer
  protection, AML, taxation, etc.
- Member States may extend to national-law violations.
```

### Recipe 2: US SOX + Dodd-Frank framework

```text
SOX §806 (18 USC §1514A) — public companies:
- Protects from retaliation for reporting fraud against shareholders
- Includes reporting to federal regulator, member of Congress, supervisor
- Tier: SOX 806 covers public companies + contractors
- 180-day filing window (OSHA + DOJ)
- Remedies: reinstatement, back pay, special damages, attorneys' fees

Dodd-Frank Wall Street Reform §922 (15 USC §78u-6) — SEC whistleblowers:
- Monetary award: 10-30% of monetary sanctions >$1M
- Anonymous reporting allowed (via attorney intermediary required)
- Protection from retaliation
- SEC Office of the Whistleblower portal: https://www.sec.gov/whistleblower

CFTC + IRS + OSHA similar whistleblower programs.

State whistleblower laws — vary; many cover broader categories than SOX
(California Labor Code §1102.5, etc.).
```

### Recipe 3: Multi-channel intake design

```text
Channel mix (EU Directive + best practice):

Web form (most common):
- Hosted by third party (e.g., NAVEX EthicsPoint, FaceUp)
- 24/7 available
- Multi-language
- Anonymous option
- File attachment support
- Encrypted in transit + at rest

Phone hotline:
- 24/7 toll-free
- Multi-language interpreter
- Anonymous option
- Recorded with consent

Mobile app:
- iOS + Android
- Offline draft capability
- Push notifications

Email (with caution):
- Encrypted email (PGP / S/MIME)
- Anonymous option requires intermediary

In-person:
- Designated officer
- Privacy-protected space
- Optional

Written letter:
- Mailed to designated officer
- Privacy + chain-of-custody

For EU: minimum web + phone + in-person available.
```

### Recipe 4: Confidentiality + anonymity

```text
Confidentiality (default):
- Reporter's identity is known to designated officer but treated as
  confidential.
- Identity disclosed only to investigators on need-to-know basis.
- Identity NOT disclosed to subject of report or wider org.

Anonymity (where permitted):
- Reporter doesn't provide name.
- Two-way communication via case number + secure portal.
- Reporter can attach evidence without identity.

Note: anonymous reporters less protected in some jurisdictions (e.g., 
SOX requires named reports for full anti-retaliation protection).

EU Directive doesn't require Member States to accept anonymous reports
(left to Member State discretion); 16 of 27 Member States accept.
```

### Recipe 5: Case management workflow

```markdown
# Whistleblower Case — <Case ID>

**Intake date:** <YYYY-MM-DD>
**Channel:** <Web / Phone / App / In-person / Email>
**Reporter:** <Name / Anonymous (with case ID)>
**Designated officer:** <name>

## Acknowledgment (7-day SLA)
- [ ] Acknowledgment sent: <date>

## Initial assessment (within 14 days)
- Category: <financial / safety / discrimination / harassment / corruption
  / data privacy / AML / etc.>
- Urgency: <Immediate harm / Active / Historical>
- Investigator assigned: <name + role>
- Conflicts of interest screened? <Y/N>

## Investigation
- Interview list: <named individuals>
- Document collection: <list>
- Outside counsel: <if applicable>
- Forensic: <if applicable>

## Findings
- Substantiated / Not substantiated / Insufficient evidence
- Findings memo: <attached>

## Corrective action
- Disciplinary: <if substantiated>
- Process change: <described>
- Training: <described>
- Regulator notification: <if required>

## Feedback to reporter (3-month SLA — EU Directive Art. 9)
- [ ] Feedback delivered: <date>

## Non-retaliation monitoring
- 6-month check-in with reporter (if not anonymous)
- 12-month check-in

## Closure
- Date: <YYYY-MM-DD>
- Reviewer sign-off: <name>

## Retention
- 5 years minimum (often 7-10 years for regulated industries)
- Anonymous case records retained even longer

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

### Recipe 6: Non-retaliation policy + monitoring

```markdown
# Non-Retaliation Policy

## Statement
<Co.> prohibits any retaliation against persons reporting concerns in
good faith, regardless of whether the concern is substantiated.

## Prohibited retaliation
- Termination, suspension, demotion
- Reduction in pay, hours, benefits
- Negative performance review unrelated to performance
- Reassignment to less desirable role / location
- Discrimination, harassment, threats
- Failure to promote
- Blacklisting (preventing future employment)
- Disclosure of reporter's identity beyond need-to-know

## Reporting retaliation
Suspected retaliation can be reported via the same channels (Web hotline /
Phone / Email).

## Investigation
Independent investigation within 14 days; remediation within 60 days if
substantiated.

## Burden of proof (EU Directive Art. 21(5))
Where reporter shows they made a protected report + then suffered
detriment, presumption is detriment is in response to the report. Org
must rebut.

## Remedies
- Reinstatement
- Back pay + benefits restoration
- Compensation for emotional + reputational harm
- Attorneys' fees + costs
- Punitive damages (jurisdiction-dependent)

---
*Disclaimer per template.*
```

### Recipe 7: NAVEX EthicsPoint workflow

```text
NAVEX EthicsPoint — largest enterprise whistleblower platform.

Features:
- Multi-channel intake (web + phone + app + in-person)
- 200+ languages
- Anonymous option with two-way messaging
- Case management with workflow + audit trail
- Integration with NAVEX PolicyTech, IRS, GRC
- Compliance with EU Directive, SOX, Dodd-Frank, country-specific

Deployment:
1. Subscribe + customize intake (categories, urgency, languages).
2. Designate Officer + investigators.
3. Customize feedback templates.
4. Integrate with internal directory + case ticketing.
5. Train designated officers.
6. Publicize internally + externally (compliant per region).
7. Quarterly reporting to Audit Committee / Board.

Pricing: $20K-$200K/yr depending on EE + features.
```

### Recipe 8: FaceUp (EU-strong alternative)

```text
FaceUp — EU-focused; strong for EU Directive 2019/1937 compliance.

Features:
- GDPR-compliant EU hosting (EU data residency)
- Anonymous reporting with case ID
- 100+ languages
- Multi-tenant for groups
- Lower cost than enterprise NAVEX
- Mobile app

Free tier for orgs 50-100 EE; paid tier scales.

Common picks for EU SMB.
```

### Recipe 9: Reporting cadence to governance

```text
Internal reporting:
- Designated Officer maintains case log.
- Confidential summary to Audit Committee quarterly.
- Annual report to Board.
- Minimum metadata only: counts by category + status.
- NEVER identify reporters unless legally compelled.

External reporting (where required):
- SEC Whistleblower Office (Dodd-Frank annual disclosures)
- Member State authority (per EU Directive)
- Industry-specific (FinCEN SAR, OSHA, etc.)

Public reporting (some orgs include in CSR / sustainability):
- Aggregated counts only
- "No identifiable trends in retaliation" sort of statement
- Multi-year trends
```

### Recipe 10: Reportable category taxonomy

```text
Common categories (customize per industry):

Financial / fraud:
- Accounting irregularities
- Misuse of company funds
- Vendor kickbacks
- Bribery (FCPA, UKBA)
- Insider trading
- Money laundering
- Sanctions violations

People / culture:
- Harassment (sexual, racial, etc.)
- Discrimination
- Workplace violence
- Workplace safety violations
- Substance abuse on job
- Unfair employment practices

Operational / regulatory:
- Health + safety violations
- Environmental violations
- Quality control fraud
- Data privacy violations (GDPR, CCPA)
- Cybersecurity gaps not reported
- Anti-trust violations

Other:
- Conflict of interest
- Confidentiality breach
- Theft
- Misuse of company property
- Other (free text)
```

### Recipe 11: Designated officer requirements

```text
Designated officer (impartial person or function):
- Independence from operational management
- No conflict of interest
- Training on:
  - Investigation methodology
  - Non-retaliation principles
  - Legal privilege + confidentiality
  - Cross-cultural / linguistic considerations
  - Trauma-informed interviewing

Often outsourced to:
- Internal Audit (with carve-out from operational reporting)
- Legal Counsel (with privilege concerns navigated)
- Ethics / Compliance function
- External law firm (independence advantage)

EU Directive Art. 8(3): a third party can be designated person.
```

### Recipe 12: Communication + awareness

```text
Make program visible:
- Onboarding training
- Annual awareness training
- Posters in physical workplaces
- Intranet pages with channel access
- Code of Conduct prominently links
- Mentioned in Privacy / Ethics policy

Multi-language:
- Major languages in jurisdiction
- EU: minimum local Member State language + English

Disclosure to subject of report:
- After investigation conclusion (per Art. 17 EU Directive)
- With identity of reporter protected
```

### Recipe 13: Annual program audit

```text
Required by some frameworks; best practice:
- Counts by category (trends)
- Substantiation rate (10-20% typical)
- Average time to acknowledgment + feedback
- Categories of corrective action
- Non-retaliation incidents (target: 0)
- Reporter feedback (where possible)
- Channel usage distribution
- Recommendations for program improvement

Auditor: independent (internal audit OR external firm); report to Board.
```

## Examples

### Example 1: Stand up EU Directive-compliant program (50-EE org)

**Goal:** EU Whistleblower Directive compliance in 60 days.

**Steps:**
1. Pick FaceUp (EU-strong, GDPR-compliant).
2. Designate Officer (Compliance Lead).
3. Customize intake categories per Recipe 10.
4. Translate intake to local language(s) + English.
5. Communicate per Recipe 12.
6. Train Designated Officer (Recipe 11).
7. Quarterly report to Board.

**Result:** EU Directive Art. 8 + 9 compliance.

### Example 2: Investigate SAR-related concern

**Goal:** Anonymous report alleges AML program gap.

**Steps:**
1. Acknowledgment within 7 days.
2. Initial assessment: financial; severity Medium.
3. Investigator: outside counsel (independence + privilege).
4. Document collection + interviews.
5. Substantiated: process gap; corrective action + training.
6. SAR filing if regulator-reportable matter.
7. Feedback to reporter within 3 months.
8. Non-retaliation monitoring (anonymous case ID for 12 months).

**Result:** Compliant investigation + AML program improvement.

### Example 3: Annual program audit

**Goal:** Annual review for Board.

**Steps:**
1. Compile data per Recipe 13.
2. Trends analysis.
3. Compare to industry benchmarks (NAVEX Hotline Benchmark Report).
4. Recommendations.
5. Board presentation.

**Result:** Documented program audit; improvement priorities.

## Edge cases / gotchas

- **EU Directive applicability** to non-EU orgs with EU operations: yes if EU establishment.
- **Member State transposition variation.** Some Member States extend scope; some add reverse-burden-of-proof stronger.
- **SOX 806 vs Dodd-Frank.** Different protections + remedies; report can fall under both.
- **Dodd-Frank requires SEC report** for monetary award; internal-only doesn't qualify.
- **Attorney-client privilege concerns** with internal investigations; external counsel preserves privilege.
- **Anonymity weakens SOX protection.** Names enable retaliation claim; anonymity risks dilution.
- **Cross-border investigation** raises GDPR Art. 6 + Art. 9 issues (criminal data); coordinate with DPO.
- **Subject of report's rights.** Per Art. 17 EU Directive, must be informed (with reporter ID protected) at investigation conclusion.
- **Multilingual interpretation costs.** Budget for 24/7 phone hotline in major languages.
- **External counsel for sensitive investigations** = $300-$1,500/hr; budget accordingly.
- **Don't over-promise "anonymity."** Some jurisdictions or investigation needs require disclosure; explain limits upfront.
- **Pre-existing concerns** — when launching, expect backlog of latent reports; staff intake to handle.
- **Whistleblower retaliation claims** can far exceed underlying fraud; treat seriously.
- **Cross-jurisdictional reach (US Foreign Corrupt Practices Act).** Reports from any country can implicate US enforcement.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [EU Whistleblower Directive 2019/1937](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32019L1937)
- [SOX §806 (18 USC §1514A)](https://www.govinfo.gov/content/pkg/USCODE-2018-title18/html/USCODE-2018-title18-partI-chap73-sec1514A.htm)
- [Dodd-Frank §922 (15 USC §78u-6)](https://www.sec.gov/whistleblower)
- [SEC Office of the Whistleblower](https://www.sec.gov/whistleblower)
- [OSHA Whistleblower](https://www.whistleblowers.gov/)
- [CFTC Whistleblower](https://www.whistleblower.gov/)
- [IRS Whistleblower](https://www.irs.gov/compliance/whistleblower-office)
- [NAVEX EthicsPoint](https://www.navex.com/en-us/products/navex-one-grc-information-system/ethicspoint-hotline-incident-management/)
- [NAVEX Hotline Benchmark Report](https://www.navex.com/en-us/resources/benchmark-reports/regional-whistleblowing-hotline-benchmark-report/)
- [Lighthouse Services](https://www.lighthouse-services.com/)
- [Convercent (OneTrust)](https://www.convercent.com/)
- [Whispli](https://www.whispli.com/)
- [FaceUp](https://faceup.com/)
- [AllVoices](https://www.allvoices.co/)
- [Speakfully](https://www.speakfully.com/)
