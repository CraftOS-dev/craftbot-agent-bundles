---
name: gdpr-readiness-audit
description: Audit GDPR readiness — Art. 6 lawful basis mapping, DPIA for high-risk processing, DSAR pipeline, ROPA, DPO designation, breach notification (72-hour), international transfers (SCC + TIA). Use for compliance audits + gap analysis + remediation plans. Output is a gap-analysis report with the consult-an-attorney disclaimer.
---

# GDPR Readiness Audit

## When to use

User says:

- "Audit our GDPR compliance"
- "Are we GDPR compliant?"
- "Do we need a DPO?"
- "Set up DSAR / SAR handling"
- "Run a DPIA for [new product feature]"
- "Build a ROPA"
- "Verify our SCCs / international transfer mechanism"
- "What's our 72-hour breach notification process?"

Companion skills:
- `privacy-policy-gdpr-ccpa` — privacy policy itself.
- `ccpa-cpra-readiness-audit` — sister audit for US states.
- `dpa-data-processing-agreement` — Art. 28 DPA drafting.
- `cookie-consent-management-cookiebot-onetrust` — ePrivacy / cookies.

## Setup

```bash
# Fetch current ICO + EDPB + Eur-Lex templates
curl -fsSL -o ico_lia.html https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/a-guide-to-lawful-basis/legitimate-interests/
curl -fsSL -o ico_dpia.html https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/guide-to-accountability-and-governance/data-protection-impact-assessments-dpias/
curl -fsSL -o edpb_dpia.html https://edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-42022-data-protection-impact-assessments_en
curl -fsSL -o ico_ropa.html https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/guide-to-accountability-and-governance/documentation/

# EU SCC (2021/914)
curl -fsSL -o scc_module1-4.pdf https://commission.europa.eu/system/files/2021-06/standard_contractual_clauses_-_text_2.pdf

# Python helpers
pip install pandas openpyxl jinja2
```

Auth / API keys: none required for audit-stage work.

## Common recipes

### Recipe 1: Scope determination (Art. 3 territorial + Art. 2 material)
```python
# scope_check.py
applies = []
# Establishment-based (Art. 3(1))
if has_eu_establishment:
    applies.append("Art. 3(1) — EU establishment")
# Targeting (Art. 3(2)(a))
if targets_eu_subjects:  # ads in EU lang/currency, ships to EU, EU domain
    applies.append("Art. 3(2)(a) — targeting EU data subjects")
# Monitoring (Art. 3(2)(b))
if monitors_eu_subjects:  # behavior tracking, cookies, profiling
    applies.append("Art. 3(2)(b) — monitoring EU data subjects")

print("GDPR applies:", bool(applies), applies)
```

### Recipe 2: Lawful basis mapping (Art. 6 + Art. 9)
```python
# lawful_basis.py
import pandas as pd
mapping = pd.DataFrame([
    {"activity": "Account creation", "data": "Email, password, name",
     "basis": "Art. 6(1)(b) Contract", "art9": None},
    {"activity": "Marketing emails", "data": "Email, preference",
     "basis": "Art. 6(1)(a) Consent", "art9": None},
    {"activity": "Security logs", "data": "IP, session, fingerprint",
     "basis": "Art. 6(1)(f) Legitimate interest", "art9": None,
     "lia_required": True},
    {"activity": "Tax reporting", "data": "Payment + identity",
     "basis": "Art. 6(1)(c) Legal obligation", "art9": None},
    {"activity": "Health data integration", "data": "Health records",
     "basis": "Art. 6(1)(a) Consent", "art9": "Art. 9(2)(a) Explicit consent"},
])
mapping.to_markdown("lawful_basis.md", index=False)
```

### Recipe 3: Legitimate Interests Assessment (LIA) — three-part test
```markdown
# LIA — <Activity>

## 1. Purpose test (legitimate interest)
- What is the interest? <description>
- Is it lawful, ethical, real?
- Whose interest? Controller, third party, public, data subject?

## 2. Necessity test
- Is the processing necessary? Can the purpose be achieved with less data?
- Is there a less intrusive alternative?

## 3. Balancing test
- Reasonable expectations of data subjects?
- Nature of data (sensitive? children?)
- Possible impact (negative consequences?)
- Safeguards (encryption, minimization, deletion)?

## Outcome
- Legitimate interest applies? Yes / No
- If yes: documented LIA on file; data subject right to object honored.
- If no: switch to consent or other basis.
```
ICO LIA template: https://ico.org.uk/media/for-organisations/forms/2258436/lia-template.docx

### Recipe 4: Data Protection Impact Assessment (DPIA) — Art. 35
```markdown
# DPIA — <Project Name>

## 1. Description of processing
- Nature, scope, context, purposes
- Personal data flows (diagram)

## 2. Necessity + proportionality assessment
- Is it necessary for the purpose?
- Proportionate to risk?

## 3. Risk assessment to data subject rights
| Risk | Likelihood | Severity | Score |
|---|---|---|---|
| Unauthorized access | Low | High | Med |
| Excessive collection | Med | Med | Med |
| Profiling without consent | High | High | High |

## 4. Mitigating measures
- Encryption at rest + in transit (TLS 1.3, AES-256)
- Pseudonymization where possible
- Access controls + audit logs
- Retention limits + automated deletion
- Consent banner + opt-out flow

## 5. Residual risk
- After mitigation: Low / Med / High
- If High: Art. 36 prior consultation with supervisory authority

## 6. Consultation
- DPO opinion
- Data subjects (when feasible)

## 7. Decision
- Proceed / proceed with modifications / abandon

## 8. Review schedule
- Every 12 months OR on material change
```
DPIA triggers (Art. 35(3)): systematic + extensive evaluation (profiling) producing legal effects; large-scale special-category data; systematic monitoring of public areas. EDPB Guidelines 4/2022 + ICO sample DPIAs.

### Recipe 5: Records of Processing Activities (ROPA) — Art. 30
```python
# ropa.py
import pandas as pd
ropa = pd.DataFrame([
    {"name_processing": "Customer support",
     "purpose": "Respond to inquiries",
     "data_categories": "Email, name, conversation history",
     "data_subjects": "Customers",
     "recipients": "Zendesk (processor)",
     "transfers": "US (Zendesk) — EU SCC 2021/914 Module 2",
     "retention": "3 years from last contact",
     "tom": "Encrypted at rest + TLS in transit; SSO; audit log"},
    {"name_processing": "Marketing",
     "purpose": "Send promotional emails (consent-based)",
     "data_categories": "Email, name, preferences",
     "data_subjects": "Marketing subscribers",
     "recipients": "Mailchimp",
     "transfers": "US — DPF certified",
     "retention": "Until consent withdrawn",
     "tom": "Encrypted at rest; unsubscribe link"},
])
ropa.to_markdown("ropa.md", index=False)
ropa.to_excel("ropa.xlsx", index=False)
```
ICO ROPA template: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/documentation/

### Recipe 6: Data Subject Access Request (DSAR) handling pipeline
```text
Intake:
- Public form at <yoursite>/privacy/dsar OR privacy@<co>
- Required: subject identification + request type (access / delete / correct / restrict / portability / object)

Verification:
- For account holders: re-authenticate (password + MFA)
- For non-account: gov-ID + matching record
- 1-3 verification steps proportionate to risk

Workflow:
- Day 0: Acknowledge receipt within 72 hours
- Day 1-5: Verify identity
- Day 6-25: Gather data across all systems (use a runbook per system: prod DB, analytics, backups, third-parties)
- Day 26-30: Quality check + draft response
- Day 30: Deliver (extendable to 90 days for complex requests with notice)

Tooling:
- OneTrust DSAR / Iubenda DSAR portal route + track
- Or homegrown: Zendesk macro + Notion runbook
```

### Recipe 7: Breach notification — Art. 33 (authority) + Art. 34 (data subjects)
```text
Hour 0 (discovery): Identify scope
- What data? How many subjects? What systems?
- Is it a personal data breach? (confidentiality, integrity, availability)

Hour 0-24: Triage
- Severity assessment
- Containment + remediation

Hour 24-72: Decision tree
- Likely to result in risk to rights & freedoms?
  - YES → Notify supervisory authority within 72 hours (Art. 33)
  - High risk? → Notify data subjects without undue delay (Art. 34)
- Document decision even if no notification (Art. 33(5))

Notification content:
- Nature of breach
- Categories + approximate number of subjects + records
- DPO contact / privacy contact
- Likely consequences
- Measures taken + proposed

Format: ICO / national DPA breach report form.
```

### Recipe 8: International transfer mechanism check
```text
For each cross-border data flow OUTSIDE EU / UK:
1. Is recipient in an adequacy decision country?
   - Adequacy list: Andorra, Argentina, Canada (commercial), Faroe Islands, Guernsey,
     Israel, Isle of Man, Japan, Jersey, NZ, Korea, Switzerland, UK, US (DPF certified entities)
   - YES → no further mechanism needed
2. If NO → use one of:
   a. EU SCC (2021/914) — Module 1 (C2C) / Module 2 (C2P) / Module 3 (P2P) / Module 4 (P2C)
   b. Binding Corporate Rules (BCR) — multinational only
   c. Art. 49 derogations (limited — explicit consent, contract necessary, public interest)
3. SCC requires Transfer Impact Assessment (TIA) post-Schrems II
   - Local law risk assessment (e.g., US FISA 702 surveillance)
   - Supplementary measures if needed (encryption, pseudonymization)
```

### Recipe 9: DPO designation decision
```python
# dpo_decision.py
dpo_required = (
    is_public_authority OR
    (core_activity_is_systematic_monitoring AND large_scale) OR
    (large_scale_special_category_data) OR
    (large_scale_criminal_conviction_data) OR
    (national_law_requires_dpo)  # DE requires DPO at 20+ employees processing
)
# If borderline: document decision in memo; consider voluntary DPO
```

### Recipe 10: Audit gap-analysis report skeleton
```markdown
# GDPR Readiness Audit — <Co.>

**Date:** 2026-06-09
**Auditor:** Legal Counsel (AI agent)
**Scope:** All processing of EU/UK personal data

## Executive summary
- HIGH gaps: <N>
- MED gaps: <N>
- LOW gaps: <N>
- Overall readiness: <%>

## Findings by area

### 1. Lawful basis (Art. 6)
- Status: <Compliant / Gaps>
- Gaps: <list>

### 2. Information to data subjects (Art. 13-14)
- Status:
- Gaps:

### 3. Data subject rights (Art. 12-23)
- Status:
- Gaps: DSAR portal exists? Verification process? SLA tracker?

### 4. Accountability (Art. 30 ROPA)
- Status:
- Gaps:

### 5. Data Protection by Design + Default (Art. 25)
- Status:
- Gaps:

### 6. DPIA (Art. 35)
- Status:
- Gaps: DPIAs on file for high-risk processing? Review schedule?

### 7. International transfers (Art. 44+)
- Status:
- Gaps: SCC in place? TIA documented? DPF certification?

### 8. Processor agreements (Art. 28)
- Status:
- Gaps: DPA with each sub-processor?

### 9. Security (Art. 32)
- Status:
- Gaps: Encryption, MFA, audit logs, pen-test?

### 10. Breach notification (Art. 33-34)
- Status:
- Gaps: Runbook on file? 72-hour SLA process?

### 11. DPO designation (Art. 37)
- Status: Required / Not required / Voluntary
- Gaps:

## Remediation plan
| Gap | Priority | Owner | Deadline |
|---|---|---|---|
| Sign DPA with vendor X | HIGH | Legal | 2026-07-15 |
| Document LIA for security logging | MED | DPO | 2026-08-01 |

---
**Disclaimer:** This is informational guidance from an AI agent. Always consult a licensed attorney in your jurisdiction before relying on this audit for compliance posture or regulatory filings.
```

## Examples

### Example 1: SaaS startup — first-time GDPR audit
**Goal:** Pre-EU-launch GDPR readiness.
**Steps:**
1. Recipe 1 scope check → confirms Art. 3 applicability.
2. Recipe 2 lawful basis map.
3. Recipe 3 LIA for each legitimate-interest activity.
4. Recipe 5 ROPA.
5. Recipe 8 transfer mechanism review.
6. Recipe 9 DPO designation decision.
7. Recipe 10 audit report.
8. Add disclaimer; deliver to user's licensed counsel.

**Result:** Gap analysis + remediation plan ready for execution.

### Example 2: DPIA for AI feature
**Goal:** New AI-driven user-profiling feature.
**Steps:**
1. Recipe 4 DPIA — high-risk processing trigger (systematic profiling).
2. Risk + mitigation assessment.
3. DPO consultation.
4. If residual risk High → Art. 36 prior consultation with supervisory authority (ICO / Irish DPC).
5. Document decision; review every 12 months.

**Result:** Documented DPIA ready for any audit or DSAR escalation.

## Edge cases / gotchas

- **GDPR applies to non-EU companies with EU users.** Art. 3(2) is broad — if you ship to EU, accept EU currency, or track EU behavior, you're in scope.
- **Consent isn't the default basis.** Consent must be freely given, specific, informed, unambiguous. For service-essential data, use "contract" (b); over-using consent makes it harder to support service interruptions.
- **Schrems II + TIA.** SCCs alone aren't enough — you need a documented Transfer Impact Assessment evaluating local-law surveillance risk (US FISA 702 a key concern).
- **EU-US Data Privacy Framework (DPF) certification list.** US recipient must be DPF-certified at the time of transfer; verify https://www.dataprivacyframework.gov/list. Re-certification annual.
- **DPO is INDEPENDENT.** DPO can be employee or external; must report to highest management, not be dismissed for advice, no conflict of interest.
- **72-hour breach clock starts at AWARENESS, not occurrence.** "Becoming aware" requires reasonable certainty — investigation time is OK to clarify scope, but clock starts when triage confirms a breach.
- **Sub-processor without DPA = direct controller breach.** Art. 28(3) requires DPA before processing starts. Retrofitting after the fact doesn't cure the breach.
- **Children + Art. 8.** EU member states set age of digital consent between 13-16 (varies). UK: 13. France / Germany: 16.
- **ePrivacy is separate from GDPR.** Cookies + electronic marketing = ePrivacy Directive 2002/58/EC. Even with GDPR consent, you may still need ePrivacy consent.
- **Brexit + UK GDPR.** UK GDPR mirrors EU GDPR but ICO is independent. Cross-EU/UK transfers need separate consideration (UK adequacy decision in place but reviewable).
- **DSAR fee exception.** Art. 12(5) allows charging "reasonable fee" only for manifestly unfounded or excessive requests (e.g., 10+ requests/year from same subject). Default = free.
- **Right to erasure exceptions.** Art. 17(3) — freedom of expression, legal obligation, public health, archiving, defense of legal claims. Document refusal grounds carefully.

> Warning: **This is informational guidance from an AI agent. Always consult a licensed attorney in your jurisdiction before relying on a GDPR readiness audit for compliance posture, regulatory filings, or binding decisions.**

## Sources

- [GDPR Regulation (EU) 2016/679 — Eur-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj) — full text.
- [ICO UK GDPR Guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/) — practical interpretations.
- [EDPB Guidelines](https://edpb.europa.eu/our-work-tools/general-guidance/guidelines-recommendations-best-practices_en) — EU enforcement guidance.
- [EDPB Guidelines 04/2022 — DPIA](https://edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-42022-data-protection-impact-assessments_en) — DPIA methodology.
- [ICO LIA Template](https://ico.org.uk/media/for-organisations/forms/2258436/lia-template.docx) — Legitimate Interests Assessment.
- [ICO DPIA Guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/guide-to-accountability-and-governance/data-protection-impact-assessments-dpias/) — DPIA when + how.
- [EU SCC 2021/914](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en) — cross-border transfer mechanism.
- [EU-US Data Privacy Framework](https://www.dataprivacyframework.gov/) — DPF certification list.
- [Schrems II — CJEU C-311/18](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62018CJ0311) — SCC + TIA requirement.
- Sister skills: `privacy-policy-gdpr-ccpa`, `dpa-data-processing-agreement`, `cookie-consent-management-cookiebot-onetrust`.
