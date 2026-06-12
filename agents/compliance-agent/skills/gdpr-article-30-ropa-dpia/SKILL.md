---
name: gdpr-article-30-ropa-dpia
description: Build + maintain GDPR core artifacts — Article 30 Records of Processing Activities (ROPA), Article 35 Data Protection Impact Assessment (DPIA), Legitimate Interests Assessment (LIA per Art. 6(1)(f)), and Transfer Impact Assessment (TIA post-Schrems II) for international transfers. Free fallback uses ICO templates + CNIL PIA Tool; paid SOTA via OneTrust / Securiti.ai / Transcend / DataGrail.
---

# GDPR Core — ROPA + DPIA + LIA + TIA

GDPR (EU 2016/679) is the global privacy benchmark. Article 30 ROPA is the foundational inventory. Article 35 DPIA is mandatory for high-risk processing. Article 6(1)(f) LIA is required whenever legitimate interests is the lawful basis. Post-Schrems II (CJEU 2020) TIA accompanies SCCs.

## When to use

User says:
- "GDPR ROPA" / "Article 30 records" / "Records of Processing"
- "DPIA" / "Data Protection Impact Assessment"
- "LIA" / "Legitimate Interests Assessment"
- "TIA" / "Transfer Impact Assessment" / "Schrems II"
- "SCCs" / "Standard Contractual Clauses"
- "Lawful basis" / "Article 6"
- "DPO designation" / "Article 37"
- "Privacy by design" / "Article 25"
- "EU representative" / "Article 27"

Companion skills: `ccpa-cpra-dsar-workflows`, `data-retention-deletion-policy`, `breach-notification-gdpr-72hr-state-laws`, `vendor-security-questionnaire-caiq-sig`.

## Setup

```bash
# Free official templates + tools
# ICO (UK) ROPA controller template
curl -fsSL -o ico_ropa_controller.xlsx \
  https://ico.org.uk/media/for-organisations/documents/1064/documentation-self-assessment-controller.xlsx

# ICO ROPA processor template
curl -fsSL -o ico_ropa_processor.xlsx \
  https://ico.org.uk/media/for-organisations/documents/2172937/documentation-self-assessment-processor.xlsx

# CNIL PIA Tool (open-source DPIA tool — desktop + web)
# https://www.cnil.fr/en/open-source-pia-software-helps-carry-out-data-protection-impact-assesment
# GitHub: https://github.com/LINCnil/pia
# Desktop (Electron):
curl -fsSL -o cnil_pia_linux.AppImage \
  https://github.com/LINCnil/pia/releases/latest/download/pia-linux.AppImage
# Or web version: docker run -p 8080:80 lincnil/pia

# EDPB SCC 2021/914 templates
curl -fsSL -o scc_2021_914.pdf \
  https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj

# Paid SOTA platforms (recipient supplies API token)
export ONETRUST_API_KEY=<onetrust-dashboard>
export SECURITI_API_KEY=<securiti-dashboard>
export TRANSCEND_API_KEY=<transcend-dashboard>
export DATAGRAIL_API_KEY=<datagrail-dashboard>
export KETCH_API_KEY=<ketch-dashboard>
```

Auth notes:
- ICO templates are free + public. CNIL PIA is open-source (AGPL).
- OneTrust / Securiti / Transcend / DataGrail / Ketch are paid SaaS; tokens from tenant admin.

## Common recipes

### Recipe 1: Lawful basis decision tree (Art. 6)

```text
For each processing activity, name EXACTLY ONE basis:

(a) Consent — Art. 7 strict requirements: freely given, specific, informed,
    unambiguous, withdrawable. NOT default for employment, B2B, or
    contractual.

(b) Contract necessity — performance of contract WITH the data subject (or
    pre-contract steps at their request). NOT third-party benefit.

(c) Legal obligation — EU or Member State law mandates the processing.
    Examples: tax, AML/KYC, employment law records.

(d) Vital interests — life of the data subject or another person. Narrow.

(e) Public task — exercise of official authority. Public sector mainly.

(f) Legitimate interests — needs LIA balancing test. NOT available to public
    authorities for their tasks. Most common for B2B marketing, fraud
    prevention, IT security.

Special-category data (Art. 9 — health, race, religion, sexual orientation,
biometric, genetic, political, trade union, philosophical beliefs):
- Need Art. 6 basis + Art. 9 condition (consent / employment law / vital
  interests / etc.).

Criminal data (Art. 10):
- Need legal authorization.
```

### Recipe 2: Article 30 ROPA — controller side template

```markdown
# Records of Processing Activities (ROPA) — Controller
**Org:** <Co.>
**Last updated:** <date>
**DPO contact:** <email if applicable>

## Processing Activity: <name>

| Field | Detail |
|---|---|
| Activity ID | RPA-001 |
| Activity name | Customer support ticket handling |
| Purpose | Resolve customer support inquiries |
| Lawful basis (Art. 6) | (b) Contract |
| Special-category basis (Art. 9) | N/A |
| Categories of data subjects | Customers, end users |
| Categories of personal data | Name, email, account ID, support ticket content |
| Recipients (internal) | Customer Support team |
| Recipients (external — processors) | Zendesk (US), Slack (US) |
| International transfers | US (Zendesk, Slack) |
| Transfer safeguard | EU-US Data Privacy Framework + SCCs as fallback |
| Retention period | 3 years from ticket close (per retention schedule) |
| Technical + organizational measures | TLS 1.3, AES-256 at rest, SSO, MFA, audit logging, quarterly access review |
| DPIA required? | No (low risk; not in EDPB high-risk list) |

(Repeat per processing activity.)
```

### Recipe 3: Article 30 ROPA — processor side template

```markdown
# Records of Processing Activities (ROPA) — Processor

| Field | Detail |
|---|---|
| Processor name | <Co.> |
| Processor contact | <email> |
| Controller name | <Customer Co.> |
| Controller contact | <Customer DPO> |
| Categories of processing | Hosting, storage, analytics on customer data |
| Categories of data subjects | Controller's end users |
| Categories of personal data | Per controller's instructions; documented in MSA Schedule A |
| International transfers | US (primary region) |
| Transfer safeguard | DPF + SCCs |
| Technical + organizational measures | ISO 27001:2022 + SOC 2 Type II controls |
| Sub-processors | AWS (us-east-1, eu-west-1), Snowflake, Datadog (see sub-processor list at <URL>) |
```

### Recipe 4: ROPA mandatory triggers (Art. 30(5) exceptions)

```text
Art. 30 ROPA required UNLESS ALL of:
- Org has FEWER than 250 employees AND
- Processing is OCCASIONAL AND
- Processing does NOT include special-category data (Art. 9) AND
- Processing does NOT include criminal data (Art. 10) AND
- Processing is NOT likely to result in risk to data subjects' rights

In practice: almost every org maintains ROPA. The exception rarely applies
because "occasional" + "no risk" is a high bar.
```

### Recipe 5: DPIA decision — when is it mandatory?

```text
Art. 35(3) mandatory triggers:
- Systematic + extensive evaluation including profiling, producing legal or
  similarly significant effects
- Large-scale processing of special-category (Art. 9) or criminal (Art. 10)
- Systematic monitoring of publicly accessible areas on a large scale

EDPB + Member State DPA "must-DPIA" lists add (varies by country):
- Innovative use of new tech (AI, biometrics, IoT)
- Vulnerable data subjects (children, employees, patients)
- Cross-border data transfers outside EU
- Matching / combining datasets
- Genetic / biometric for identification
- Decisions based solely on automated processing

If uncertain, perform a PRE-DPIA screening (5-10 questions); document the
decision either way.
```

### Recipe 6: DPIA execution via CNIL PIA Tool

```bash
# Launch desktop app
./cnil_pia_linux.AppImage

# Or web (Docker)
docker run -d -p 8080:80 --name cnil-pia lincnil/pia
# Open http://localhost:8080

# CNIL PIA structure (5 steps per Art. 35(7)):
# 1. Context — processing description + purposes + assets
# 2. Fundamental principles — necessity + proportionality + lawful basis
# 3. Risks — likelihood × severity for each threat
# 4. Validation — sign-off + residual risk
# 5. (Optional) Consultation with DPO + data subjects

# Export: PDF / JSON report for filing + supervisory authority consultation
# (Art. 36) if residual risk remains high.
```

### Recipe 7: DPIA template (manual fallback)

```markdown
# Data Protection Impact Assessment — <Activity name>

**Date:** <date>
**Author:** <name>
**DPO consulted:** <name + date>
**Approval:** <Privacy Lead + Exec sponsor>

## 1. Describe the processing
- Nature: <what data is processed; how>
- Scope: <volume, scale, geography, retention>
- Context: <relationship with data subjects, expectations>
- Purposes: <why; benefits to org and data subjects>

## 2. Necessity + proportionality
- Lawful basis (Art. 6): <one of the six>
- Special-category condition (Art. 9): <if applicable>
- Is this the minimum data needed? <Y/N + justification>
- Alternative less-invasive methods considered? <list + why rejected>

## 3. Consultation
- Data subjects consulted? <if appropriate>
- DPO consulted: <name + date>
- Other stakeholders: <list>

## 4. Identify + assess risks
| Risk | Likelihood (L/M/H) | Severity (L/M/H) | Risk score |
|---|---|---|---|
| Unauthorized access | M | H | High |
| Excessive collection | L | M | Med |
| Inaccurate data | L | L | Low |
| ... | ... | ... | ... |

## 5. Mitigations
| Risk | Mitigation | Residual risk |
|---|---|---|
| Unauthorized access | MFA + RBAC + audit logging + quarterly access review | Low |
| ... | ... | ... |

## 6. Outcome
- Acceptable residual risk? <Y/N>
- Supervisory authority prior consultation (Art. 36) required? <Y if residual = High>

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

### Recipe 8: LIA (Legitimate Interests Assessment) three-part test

```markdown
# Legitimate Interests Assessment — <Activity name>

## Part 1: Purpose test
- What is the legitimate interest? <e.g. fraud prevention, B2B marketing>
- Whose interest? <controller, third party, society>
- Why important? <commercial necessity, ethical, regulatory expectation>

## Part 2: Necessity test
- Is the processing necessary to achieve the purpose? <Y/N>
- Are there less-invasive means? <list + why rejected>
- Is the data minimization principle observed? <Y/N + how>

## Part 3: Balancing test
- Reasonable expectations of data subjects? <Y/N>
- Nature of the relationship (existing customer vs cold prospect)? <describe>
- Sensitivity of data? <Art. 9 / Art. 10 categories invoked?>
- Potential impact on data subjects (positive + negative)? <describe>
- Safeguards (encryption, opt-out, transparency)? <list>
- Are children involved? <Y/N — if Y, presume balancing FAILS unless strong justification>

## Outcome
- LIA passes? <Y/N>
- If N: re-engineer (use consent / contract instead, or drop activity).

---
*Disclaimer per template.*
```

### Recipe 9: TIA (Transfer Impact Assessment) per Schrems II

```markdown
# Transfer Impact Assessment — <Transfer>

**Data exporter:** <Co.> (EU/EEA)
**Data importer:** <Vendor> (<jurisdiction>)
**Transfer mechanism:** SCCs 2021/914 Module <2 / 3 / 4>
**Date:** <date>

## 1. Transfer description
- Categories of personal data: <list>
- Volume + frequency: <e.g. 10M records/month, continuous>
- Recipients: <importer + sub-processors>
- Onward transfers: <list>

## 2. Importer jurisdiction assessment
- Country: <e.g. US>
- Adequacy decision? <Y/N — EU-US DPF is partial>
- Surveillance laws (US: FISA 702, EO 12333, CLOUD Act, etc.): <summary>
- Government access regimes + safeguards: <summary>
- EDPB country-specific guidance (US, UK, CH, etc.): <reference>

## 3. SCC clauses applied
- Module 2 (Controller-to-Processor): <if your role>
- Module 3 (Processor-to-Processor): <if your role>
- Optional Clause 7 docking? <Y/N>
- Annex I (parties + transfers + competent SA): <attached>
- Annex II (TOMs — technical + organizational measures): <attached>
- Annex III (sub-processors list): <attached>

## 4. Supplementary measures (post-Schrems II)
- Encryption in transit (TLS 1.3): <Y/N>
- Encryption at rest (AES-256, importer holds keys?): <Y/N — if importer
  holds keys, government can compel disclosure>
- BYOK / customer-managed keys: <Y/N>
- Pseudonymization: <Y/N>
- Split processing (only non-identifiable data crosses border): <Y/N>
- Contractual + organizational warrant canary, transparency reports: <Y/N>

## 5. Conclusion
- Does the transfer ensure essentially equivalent protection? <Y/N>
- If N: do NOT transfer; or apply additional supplementary measures.

---
*Disclaimer per template.*
```

### Recipe 10: OneTrust ROPA via API

```bash
curl -X GET 'https://app.onetrust.com/api/datamapping/v1/inventories/processing-activities' \
  -H "Authorization: Bearer $ONETRUST_API_KEY" \
  -H "Accept: application/json" | jq '.content[]'
```

### Recipe 11: Transcend ROPA + DPIA via API

```bash
# https://docs.transcend.io/
curl -X POST 'https://api.transcend.io/graphql' \
  -H "Authorization: Bearer $TRANSCEND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ dataMap { dataInventory { categories } } }"}'
```

### Recipe 12: DPO designation criteria (Art. 37)

```text
DPO is MANDATORY when:
- Public authority or body (except courts in judicial capacity)
- Core activities = regular + systematic monitoring of data subjects on a
  large scale
- Core activities = large-scale processing of special-category (Art. 9) or
  criminal (Art. 10) data

DPO requirements:
- Expert knowledge of data protection law + practice
- Independence — reports to highest management level, no conflict of
  interest, cannot be dismissed for performing DPO tasks
- Contact details published + communicated to supervisory authority
- Tasks (Art. 39): inform + advise, monitor compliance, advise on DPIAs,
  cooperate with supervisory authority, contact point

DPO can be employee OR external service contract. Group DPO permitted if
easily accessible from each establishment.
```

### Recipe 13: Cross-border representative (Art. 27)

```text
Required when:
- Org has NO EU establishment AND
- Processes EU personal data AND
- Processing is non-occasional OR includes special-category / criminal data
  large-scale.

EU Representative (Art. 27) acts as point of contact for supervisory
authorities + data subjects. Must be in a Member State where data subjects
are located.

Typical providers (2026): GDPR-Rep.eu, EU-Rep.io, Prighter, VeraSafe (EU + UK
+ CH + DPF rep packages).
```

## Examples

### Example 1: Build ROPA for a 50-person SaaS

**Goal:** Article 30 ROPA in 2 weeks for ICO inquiry.

**Steps:**
1. Inventory processing activities via team interviews (Eng, Sales, HR, Finance, Marketing, Support, Product).
2. Use ICO controller template (Recipe 2).
3. For each activity: purpose + lawful basis + data categories + recipients + transfers + retention + TOMs.
4. Identify sub-processors (Zendesk, Slack, AWS, Datadog, etc.).
5. For Art. 6(1)(f) activities: attach LIA (Recipe 8).
6. For US transfers: attach TIA (Recipe 9).
7. Publish internal; provide to ICO on request.

**Result:** Defensible ROPA; ICO closed inquiry; basis for DPIA decisions.

### Example 2: DPIA for new AI feature

**Goal:** DPIA before launching ML-driven scoring model.

**Steps:**
1. Pre-DPIA screening: Is this systematic profiling with legal/significant effect? Yes — DPIA required.
2. Launch CNIL PIA Tool (Recipe 6).
3. Step 1 (context): user behavior data → model → access decisions.
4. Step 2 (principles): Art. 6(1)(f); Art. 22 implications.
5. Step 3 (risks): bias, opacity, accuracy drift.
6. Step 4 (mitigations): bias testing, model card, human override, opt-out, transparency.
7. Step 5 (validation): DPO sign-off; residual risk = Medium.
8. No Art. 36 prior consultation required.
9. Maintain DPIA + revisit on model retraining.

**Result:** DPIA on file; launch unblocked; documented per Art. 35.

### Example 3: TIA for US vendor change

**Goal:** Vendor migration EU → US triggers TIA.

**Steps:**
1. Confirm SCCs 2021/914 Module 2 with new vendor.
2. TIA per Recipe 9.
3. US importer in scope of FISA 702? Yes (if "electronic communications service provider").
4. Supplementary measures: customer-held BYOK keys + pseudonymization.
5. EDPB recommendations 01/2020 referenced.
6. DPO sign-off; published as sub-processor in privacy policy.
7. Notify existing customers 30 days before migration (per DPA terms).

**Result:** Transfer compliant; documented for ICO/EDPB scrutiny.

## Edge cases / gotchas

- **ROPA exception (Art. 30(5)) is narrow.** "Occasional" + "no special-category" + "no risk" + "<250 EE" is hard to maintain. Most SMBs still maintain ROPA.
- **DPIA is REQUIRED before processing starts.** Retroactive DPIA does not cure pre-DPIA processing.
- **Prior consultation (Art. 36).** If residual risk remains High after mitigation, you MUST consult supervisory authority BEFORE processing.
- **Consent withdrawal (Art. 7(3)).** Must be as easy to withdraw as to give. Pre-checked boxes are not consent.
- **Legitimate interests is NOT a catch-all.** LIA must be documented and revisited periodically. Marketing to existing customers usually passes; cold prospecting often fails.
- **Schrems II made TIA non-optional** for transfers to non-adequacy jurisdictions. SCCs alone are insufficient.
- **EU-US DPF (2023) provides partial adequacy** for certified US importers — but only for transfers to certified entities. Verify importer is on dpf.gov list.
- **UK GDPR diverges in places** post-Brexit. UK ICO adequacy decisions list differs from EDPB.
- **DPO conflict of interest.** Cannot be CISO, GC, or Privacy Lead if those roles set policy that DPO advises on. Independence is auditable.
- **Children's data (Art. 8).** Age of digital consent: 13-16, varies by Member State. Parental consent verification required below.
- **Sub-processor changes require notice.** Most DPAs require 30-day notice + objection right.
- **Penalties: up to €20M or 4% global revenue** (whichever higher). Tier 1 violations (Art. 83(4)) capped at €10M / 2%.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [GDPR — full text](https://gdpr-info.eu/)
- [GDPR Art. 30 — ROPA](https://gdpr-info.eu/art-30-gdpr/)
- [GDPR Art. 35 — DPIA](https://gdpr-info.eu/art-35-gdpr/)
- [ICO ROPA templates (UK)](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/documentation/records-of-processing-activities/)
- [ICO DPIA guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/data-protection-impact-assessments-dpias/)
- [CNIL PIA Tool (open-source)](https://www.cnil.fr/en/open-source-pia-software-helps-carry-out-data-protection-impact-assesment)
- [CNIL PIA GitHub](https://github.com/LINCnil/pia)
- [EDPB guidelines on DPIA](https://edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-052022-art-72-application-art-6-1-f-gdpr-context_en)
- [SCCs 2021/914 (EU-Lex)](https://eur-lex.europa.eu/eli/dec_impl/2021/914/oj)
- [EDPB recommendations 01/2020 on supplementary measures (Schrems II)](https://edpb.europa.eu/our-work-tools/our-documents/recommendations/recommendations-012020-measures-supplement-transfer_en)
- [EU-US Data Privacy Framework](https://www.dataprivacyframework.gov/)
- [OneTrust Data Mapping](https://www.onetrust.com/products/data-mapping/)
- [Securiti.ai](https://securiti.ai/)
- [Transcend Data Mapping](https://www.transcend.io/)
- [DataGrail](https://www.datagrail.io/)
