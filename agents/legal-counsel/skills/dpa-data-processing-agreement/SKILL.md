---
name: dpa-data-processing-agreement
description: Draft + review GDPR Art. 28 Data Processing Agreements + integrate EU Standard Contractual Clauses (SCCs 2021/914) Module 1-4 + Transfer Impact Assessment (TIA) post-Schrems II. Use when a controller-processor relationship is forming or being reviewed. Output is a complete DPA + SCC bundle with the consult-an-attorney disclaimer.
---

# Data Processing Agreement (DPA) — GDPR Art. 28 + EU SCCs

Distinct from `contract-review-msa-nda-employment` (commercial contract) and `privacy-policy-gdpr-ccpa` (controller-to-data-subject notice).

## When to use

User says:

- "Draft a DPA"
- "Review this vendor's DPA"
- "What SCC modules do I need?"
- "TIA / Transfer Impact Assessment"
- "Sub-processor terms"
- "EU SCC integration"
- "CCPA service-provider agreement" (sister CPRA contract; some overlap)
- "BCR / Binding Corporate Rules"

Companion skills:
- `contract-review-msa-nda-employment` — commercial MSA / SOW.
- `privacy-policy-gdpr-ccpa` — privacy policy (notice to subjects).
- `gdpr-readiness-audit` — underlying GDPR posture.

## Setup

```bash
# Open DPA templates
curl -fsSL -o bonterms-dpa.docx https://bonterms.com/forms/data-processing-addendum
curl -fsSL -o common-paper-dpa.html https://commonpaper.com/standards/data-processing-addendum/

# EU SCC (2021/914 — Modules 1-4)
curl -fsSL -o scc_2021_914.pdf https://commission.europa.eu/system/files/2021-06/standard_contractual_clauses_-_text_2.pdf
# Or HTML: https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj

# UK International Data Transfer Addendum (UK IDTA) / UK Addendum to EU SCC
curl -fsSL -o uk_idta.pdf https://ico.org.uk/media/for-organisations/documents/4019539/international-data-transfer-addendum.pdf

# Schrems II + TIA references
# https://edpb.europa.eu/our-work-tools/our-documents/recommendations/recommendations-012020-measures-supplement-transfer_en

# Python helpers
pip install pandas python-docx
```

## Common recipes

### Recipe 1: GDPR Art. 28(3) mandatory terms checklist
```markdown
- [ ] Subject matter + duration of processing
- [ ] Nature + purpose of processing
- [ ] Type of personal data + categories of data subjects
- [ ] Obligations + rights of controller
- [ ] Processor only on documented instructions from controller
- [ ] Personnel commitment to confidentiality
- [ ] Security measures per Art. 32
- [ ] Sub-processor terms (Art. 28(2)+(4)) — written authorization + flow-down
- [ ] Assist controller with data subject rights (Art. 12-23)
- [ ] Assist with Art. 32 security + Art. 33-34 breach + Art. 35 DPIA + Art. 36 prior consultation
- [ ] At end of services: delete or return PII + delete copies (unless law requires retention)
- [ ] Make available all info needed for Art. 28 compliance + audit / inspection rights
- [ ] Inform controller if instructions appear to violate GDPR / EU law
```

### Recipe 2: Bonterms DPA Module — fast path
```bash
curl -fsSL -o dpa.docx https://bonterms.com/forms/data-processing-addendum
```
Bonterms DPA is the leading 2026 open DPA template. Modular: pick relevant sections (controller-processor / processor-processor / SCC integration / BAA layering). Pre-filled with Art. 28(3) mandatory terms.

### Recipe 3: Common Paper DPA — alternative
Common Paper DPA uses a cover-sheet format with pre-built clauses. Use if you prefer the checkbox style.

### Recipe 4: EU SCC module selection (2021/914)
```text
Pick the right module based on parties:

Module 1: Controller → Controller (C2C)
- Both parties are controllers
- e.g., joint analytics; lead-gen partnerships

Module 2: Controller → Processor (C2P)
- DEFAULT for B2B SaaS (Customer = controller; Vendor = processor)
- Most common for vendor DPAs

Module 3: Processor → Processor (P2P)
- Sub-processor flow-down
- e.g., Vendor (processor) → Vendor's hosting (sub-processor)

Module 4: Processor → Controller (P2C)
- Less common — processor sending back to controller in different jurisdiction
```

### Recipe 5: SCC integration into DPA
```markdown
# DPA — Annex / Addendum

## Section X: International Data Transfers
Where Processor or its sub-processors transfer Personal Data of EU/UK Data Subjects outside the EEA / UK to a country without an EU adequacy decision, the parties agree:

(a) The EU Standard Contractual Clauses (Commission Implementing Decision (EU) 2021/914) ("EU SCCs"), Module [1 / 2 / 3 / 4] as appropriate, are hereby incorporated by reference and apply between Controller (as data exporter) and Processor (as data importer).

(b) For UK transfers, the UK International Data Transfer Addendum (UK IDTA) issued by the UK ICO is incorporated and applies.

(c) The Processor has conducted a Transfer Impact Assessment (TIA) per Schrems II + EDPB Recommendation 01/2020; supplementary measures (encryption, access controls, transparency reports) are detailed in Annex II of the EU SCCs.

(d) The Annexes to the EU SCCs are completed as follows:
- Annex I.A: Parties (controller / processor)
- Annex I.B: Description of transfer (categories of data subjects, categories of PII, special-category data, frequency, nature, purpose, retention)
- Annex I.C: Competent supervisory authority (per Art. 4(22) GDPR)
- Annex II: Technical + organizational measures (TOMs)
- Annex III: List of sub-processors

(e) In case of conflict between the DPA and the EU SCCs, the EU SCCs prevail.
```

### Recipe 6: Transfer Impact Assessment (TIA)
```markdown
# Transfer Impact Assessment

## 1. Data exporter / importer
- Exporter: <Co. — EU>
- Importer: <Vendor — US>

## 2. Nature of transfer
- Categories of data subjects
- Categories of PII
- Sensitive categories?
- Volume + frequency

## 3. Recipient country law assessment
- Relevant surveillance laws:
  - US: FISA §702, EO 12333, CLOUD Act
  - Others: country-specific
- Government access mechanisms
- Redress for non-citizens (EU-US DPF reduces this risk for DPF-certified entities)

## 4. Risk to data subject rights
- Likelihood of government access request
- Type of data → sensitivity
- Effective legal remedies?

## 5. Supplementary measures
- Encryption at rest + in transit (AES-256, TLS 1.3)
- Pseudonymization where possible
- Strong access controls (Zero Trust, MFA)
- Transparency reports (publish gov access requests received)
- Challenge any overbroad requests
- Limit data minimization

## 6. Decision
- Transfer can proceed? Yes / No
- If yes: SCC + supplementary measures in place
- If no: don't transfer; consider alternative (EU-hosted vendor; processor model)

## 7. Review schedule
- Re-assess on material change to recipient country law (annual minimum)
```

### Recipe 7: Sub-processor authorization
```markdown
## Sub-processor terms

The Processor may engage sub-processors subject to:
(a) Written authorization from Controller (general or specific)
(b) Notification before any new sub-processor (30 days unless emergency)
(c) Right of Controller to object on reasonable data protection grounds
(d) Pass-through of all DPA terms to sub-processor (Art. 28(4) flow-down)
(e) Processor remains fully liable for sub-processor performance

Current sub-processors listed at: <URL>

Notification method: email to designated DPO + dashboard + 30-day comment period.
```

### Recipe 8: Audit rights drafting
```markdown
## Audit + Inspection

(a) Once per 12-month period upon 30-day notice (more frequently on regulatory request or breach trigger).
(b) Controller (or qualified auditor) may inspect Processor's data processing activities.
(c) Processor may provide SOC 2 Type II report + ISO 27001 certificate in lieu of on-site audit (unless Controller has reasonable cause to require on-site).
(d) Costs borne by Controller unless audit reveals material non-compliance.
(e) Confidentiality obligations apply to auditor.
```

### Recipe 9: Annex II — Technical + Organizational Measures
```markdown
## Annex II — Technical and Organizational Measures (TOMs)

### Security of processing (Art. 32 GDPR)
1. **Pseudonymization + encryption:**
   - At-rest: AES-256
   - In-transit: TLS 1.3
   - Key management: AWS KMS / GCP Cloud KMS
2. **Confidentiality, integrity, availability of systems:**
   - Access controls (RBAC + ABAC)
   - MFA on all privileged accounts
   - Quarterly access reviews
   - Network segmentation
   - DDoS protection (Cloudflare)
3. **Restore availability + access on incident:**
   - Daily backups + cross-region replication
   - RTO: 4 hours; RPO: 1 hour
   - Tested quarterly
4. **Regular testing:**
   - Annual pen-test by qualified third party
   - Continuous vulnerability scanning (Snyk + AWS Inspector)
   - Quarterly tabletop IR exercises
5. **Personnel:**
   - Background checks
   - Annual security awareness training
   - Confidentiality agreements
6. **Logging + monitoring:**
   - Centralized SIEM (Datadog)
   - Audit logs 1-year retention
   - Alerting on anomalies
7. **Sub-processor management:**
   - Annual review + DPA + SOC 2 collection
```

### Recipe 10: DPA review checklist (when receiving vendor's DPA)
```markdown
- [ ] Vendor's DPA includes all Art. 28(3) terms (Recipe 1)
- [ ] SCC module appropriate to relationship (Recipe 4)
- [ ] Sub-processor terms acceptable (Recipe 7)
- [ ] Audit rights adequate (Recipe 8)
- [ ] TOMs disclosed at sufficient detail (Recipe 9)
- [ ] Liability + indemnity for data breach reasonable
- [ ] Notification SLA for breaches (24-72 hours)
- [ ] Data deletion / return on termination
- [ ] Governing law alignment with master agreement
- [ ] No unilateral right for vendor to amend
- [ ] Disclaimer in cover memo
```

### Recipe 11: HIPAA BAA layering (if PHI involved)
```text
If Processor also handles Protected Health Information (PHI):
- Layer HIPAA Business Associate Agreement (BAA) on top of DPA
- HHS sample BAA: https://www.hhs.gov/hipaa/for-professionals/covered-entities/sample-business-associate-agreement-provisions/
- Required terms per 45 CFR §164.504(e)
- See `contract-review-msa-nda-employment` Recipe 11 for BAA elements
```

### Recipe 12: CCPA service-provider agreement overlap
```text
For CA consumer data, the DPA may need CCPA service-provider terms per §1798.140(ag)(2):
- Process only for specified business purposes
- No selling / sharing
- No combining with PI from other sources unless allowed
- Compliance certification
- Right to take reasonable steps to remediate

Many 2026 DPAs are dual-purpose: GDPR + CCPA. See `ccpa-cpra-readiness-audit` Recipe 6.
```

## Examples

### Example 1: B2B SaaS vendor — draft outbound DPA
**Goal:** Vendor publishes a DPA for customers.
**Steps:**
1. Start with Bonterms DPA (Recipe 2).
2. Walk Recipe 1 Art. 28(3) checklist.
3. Add EU SCC Module 2 + Annexes (Recipe 5).
4. Pre-complete TOMs (Recipe 9) based on actual security posture.
5. Provide TIA (Recipe 6) on file; reference in Annex II.
6. Add sub-processor flow-down (Recipe 7).
7. Add audit rights (Recipe 8).
8. Layer CCPA service-provider terms (Recipe 12).
9. Add disclaimer + send to licensed counsel for sign-off.
10. Publish at vendor.com/legal/dpa.

**Result:** Vendor DPA ready for click-through customer execution.

### Example 2: Customer reviewing vendor's DPA
**Goal:** Customer evaluates a vendor DPA before signing MSA.
**Steps:**
1. Walk Recipe 10 review checklist.
2. Compare against Bonterms benchmark for deviations.
3. Flag gaps: missing sub-processor opt-out, vague TOMs, weak audit rights.
4. Propose redlines.
5. Verify TIA on file (or request).
6. Sign + execute via DocuSign.

**Result:** Vendor DPA accepted with negotiated terms.

## Edge cases / gotchas

- **DPA ≠ MSA.** Don't merge — keep as Addendum / Schedule with explicit "in case of conflict, DPA prevails" clause for personal data terms.
- **SCC 2021/914 supersedes 2010 SCCs.** Old SCCs (2010 set) expired December 27, 2022. Always use 2021/914.
- **UK uses UK IDTA OR UK Addendum to EU SCCs.** Either works post-Brexit. UK IDTA is standalone; UK Addendum tacks UK terms onto EU SCC.
- **EU-US DPF reduces TIA burden** for DPF-certified US recipients but doesn't eliminate it. TIA still required for non-DPF transfers + Schrems III risk.
- **General vs specific sub-processor authorization.** General authorization is common but requires notification + opt-out; specific authorization requires per-vendor consent. Document which.
- **Switching sub-processors mid-engagement.** Notify with reasonable lead time (typical 30 days). Failure to notify = breach.
- **Audit rights vs SOC 2 substitution.** SOC 2 Type II + ISO 27001 are common substitutes; reserve on-site audit for cause.
- **Data deletion vs retention on termination.** Vendor may need to retain for legal hold (litigation, tax, regulatory). Document exceptions clearly.
- **Liability for sub-processor breach.** Processor remains liable to Controller per Art. 28(4); don't accept "sub-processor breach excluded from cap" clause.
- **Joint controllers (Art. 26) vs processor.** If both parties determine purposes + means, they're joint controllers and need a different agreement (Art. 26 arrangement, not Art. 28 DPA). Common confusion in ad-tech.
- **Cross-border transfer to non-adequacy + non-DPF country.** SCC + supplementary measures + TIA all required. India, China, etc. require careful TIA.

> Warning: **This is informational guidance from an AI agent. Always consult a licensed attorney in your jurisdiction before signing, filing, or executing a Data Processing Agreement, Standard Contractual Clauses, or related binding legal documents.**

## Sources

- [GDPR Art. 28 — Eur-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679#d1e2917-1-1) — text.
- [EU SCC 2021/914](https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en) — Commission decision.
- [UK International Data Transfer Addendum](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-data-transfer-agreement-and-guidance/) — UK IDTA.
- [Bonterms DPA](https://bonterms.com/forms/data-processing-addendum) — open DPA template.
- [Common Paper DPA](https://commonpaper.com/standards/data-processing-addendum/) — open DPA template.
- [EDPB Recommendation 01/2020 — Schrems II Supplementary Measures](https://edpb.europa.eu/our-work-tools/our-documents/recommendations/recommendations-012020-measures-supplement-transfer_en) — TIA methodology.
- [Schrems II — CJEU C-311/18](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:62018CJ0311) — case requiring TIA + SCCs.
- [EU-US Data Privacy Framework](https://www.dataprivacyframework.gov/) — DPF certification.
- [HHS Sample BAA](https://www.hhs.gov/hipaa/for-professionals/covered-entities/sample-business-associate-agreement-provisions/) — HIPAA BAA.
- Sister skills: `privacy-policy-gdpr-ccpa`, `gdpr-readiness-audit`, `ccpa-cpra-readiness-audit`, `contract-review-msa-nda-employment`.
