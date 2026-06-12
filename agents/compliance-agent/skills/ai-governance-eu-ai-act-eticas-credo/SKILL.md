---
name: ai-governance-eu-ai-act-eticas-credo
description: AI governance program — EU AI Act (Regulation 2024/1689; bans Feb 2025; GPAI obligations Aug 2025; high-risk obligations effective August 2, 2026; penalties up to €35M / 7% global revenue) + NIST AI Risk Management Framework 1.0 + ISO/IEC 42001:2023 AI Management System. Tools: Credo AI (policy packs), Holistic AI (continuous audit), Robust Intelligence, Fairly AI, Modulos. AI inventory + risk classification + bias + model cards + post-market monitoring.
---

# AI Governance — EU AI Act + NIST AI RMF + ISO 42001

EU AI Act high-risk obligations effective **August 2, 2026** (bans Feb 2025; GPAI Aug 2025). Penalties up to €35M or 7% global revenue. NIST AI RMF 1.0 (voluntary; widely adopted). ISO/IEC 42001:2023 (AIMS — certifiable).

## When to use

User says:
- "EU AI Act" / "AI Act compliance"
- "NIST AI RMF"
- "ISO 42001" / "AI Management System"
- "AI inventory" / "AI risk classification"
- "Model card" / "datasheet for datasets"
- "Bias testing" / "fairness assessment"
- "AI governance" / "AI policy"
- "High-risk AI"
- "GPAI" / "General Purpose AI"
- "Post-market monitoring AI"

Companion skills: `iso-27001-isms-readiness`, `policy-authoring-cybersecurity-aup-byod`, `risk-register-maintenance-scoring`.

## Setup

```bash
# EU AI Act
curl -fsSL https://artificialintelligenceact.eu/ > /tmp/aiact.html
curl -fsSL -o aiact_text.pdf https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32024R1689

# NIST AI RMF 1.0
curl -fsSL -o nist_ai_rmf.pdf https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf

# NIST GenAI Profile (NIST.AI.600-1)
curl -fsSL -o nist_genai.pdf https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf

# ISO 42001 landing
curl -fsSL https://www.iso.org/standard/81230.html > /tmp/iso42001.html

# AI governance platforms
# https://www.credo.ai/
# https://www.holisticai.com/
# https://www.robustintelligence.com/
# https://www.fairly.ai/
# https://www.modulos.ai/

export CREDO_AI_API_KEY=<dashboard>
export HOLISTIC_AI_API_KEY=<dashboard>

# OWASP LLM Top 10
curl -fsSL https://owasp.org/www-project-top-10-for-large-language-model-applications/ > /tmp/owasp_llm.html

# MITRE ATLAS (AI threat matrix)
curl -fsSL https://atlas.mitre.org/ > /tmp/atlas.html
```

## Common recipes

### Recipe 1: EU AI Act risk classification

```text
PROHIBITED (Art. 5; effective Feb 2025):
- Subliminal manipulation
- Exploitation of vulnerabilities
- Social scoring by public authorities
- Real-time remote biometric identification in public for law enforcement
  (narrow exceptions)
- Untargeted scraping of facial images for FR databases
- Emotion recognition in workplace + education (limited exceptions)
- Biometric categorization based on protected characteristics
- Predictive policing based solely on profiling

HIGH-RISK (Annex III; effective Aug 2, 2026):
- Biometrics (categorization, FR, emotion in non-prohibited contexts)
- Critical infrastructure (energy, transport, water)
- Education + vocational training (admissions, evaluation, monitoring)
- Employment (CV screening, candidate evaluation, performance, promotion,
  termination, task allocation, monitoring)
- Essential private + public services (welfare scoring, credit scoring,
  insurance pricing, emergency dispatch)
- Law enforcement (predictive, evidence reliability, profiling)
- Migration + border control
- Justice + democratic processes (case prediction, voter manipulation)
- Safety components of regulated products (Annex I — toys, medical devices,
  machinery, etc.)

LIMITED RISK (Art. 50; transparency obligations):
- Chatbots / AI interaction (must disclose to user)
- Emotion recognition (notify subject)
- Biometric categorization (notify subject)
- Deepfakes (label as artificially generated unless exception)

MINIMAL RISK:
- Spam filters, video games, basic ML
- Voluntary codes of conduct encouraged

GPAI (Art. 51; effective Aug 2025):
- General-Purpose AI Models with systemic risk (training compute >10^25 FLOPs)
  → enhanced obligations
- Standard GPAI → transparency + copyright training docs + summary of
  training content
```

### Recipe 2: NIST AI RMF 1.0 functions

```text
GOVERN — AI risk management culture, structure, capacities, policies.
MAP    — Context for AI system: categorization, capabilities, intended +
         unintended use, impacts, dependencies.
MEASURE — Analyze + assess + benchmark + monitor risk + impact.
MANAGE — Allocate resources, document, communicate, respond.

Cross-references EU AI Act + ISO 42001 + OECD AI Principles.

NIST AI 600-1 GenAI Profile (2024) — specific to generative AI: 12 risk
categories including hallucination, CBRN, harmful bias, confabulation, etc.
```

### Recipe 3: ISO 42001 — AI Management System

```text
Mandatory clauses (similar to 27001):
4. Context of organization
5. Leadership
6. Planning (incl. AI risk assessment)
7. Support (resources, competence, awareness, communication)
8. Operation (AI lifecycle management)
9. Performance evaluation (monitoring, audit, management review)
10. Improvement

Annex A — AI-specific controls (~38 controls):
A.2 Policies for AI
A.3 Internal organization for AI
A.4 Resources for AI systems
A.5 Assessing impacts on individuals + societies
A.6 AI system life cycle
A.7 Data for AI systems
A.8 Information for interested parties of AI systems
A.9 Use of AI systems
A.10 Third party + customer relationships

Cert path: 27001 + 42001 OR standalone 42001. Schellman, A-LIGN, BSI
offering 42001 cert in 2026.
```

### Recipe 4: AI inventory template

```markdown
# AI Inventory — <Co.>

**Date:** <YYYY-MM-DD>
**Owner:** <AI Governance Lead>

| ID | System name | Use case | EU AI Act class | NIST RMF context | ISO 42001 controls | Owner | Status |
|---|---|---|---|---|---|---|---|
| AI-001 | Customer support chatbot | Support resolution | Limited risk (Art. 50 disclosure) | Customer-facing | A.5, A.6, A.7, A.8 | CX Lead | Production |
| AI-002 | Resume screening tool | Candidate scoring | HIGH-RISK (Annex III §5(a)) | Internal HR | A.5, A.6, A.7, A.8, A.9 | HR + AI Gov | Pre-deployment review |
| AI-003 | LLM-based code completion | Eng productivity | Minimal (subject to data leakage controls) | Internal dev | A.4, A.7 | Eng | Production |
| AI-004 | ML-based fraud scoring | Risk decisions | HIGH-RISK (financial scoring) | Customer transactions | A.5, A.6, A.7, A.8, A.9, A.10 | Risk Lead | Production |

For each system, also document:
- Provider (in-house / vendor)
- Training data sources + lineage
- Inputs / outputs
- Decision authority (autonomous vs human-in-loop)
- Affected populations
- Last bias + accuracy assessment
- Last security + adversarial test
- Post-market monitoring cadence
```

### Recipe 5: Per-system risk assessment template

```markdown
# AI System Risk Assessment — <System Name>

**Date:** <date>
**System:** <name + version>
**Reviewer:** <name>

## 1. Context (NIST MAP)
- Use case
- Intended users
- Decision impact (legal / significant / minor)
- Affected populations
- Geographies + jurisdictions

## 2. EU AI Act classification
- Risk class (Prohibited / High / Limited / Minimal / GPAI)
- Relevant Annex
- Applicable obligations (per Art. 8-21 for high-risk)

## 3. Bias + fairness (NIST MEASURE)
- Protected attributes considered: <list>
- Bias metrics: <demographic parity / equal opportunity / disparate impact>
- Last assessment: <date + result>
- Mitigation: <pre-/in-/post-processing>

## 4. Robustness + accuracy
- Performance: <test set accuracy / F1 / AUC>
- Adversarial robustness: <test results>
- Out-of-distribution behavior: <tested>
- Drift monitoring: <frequency>

## 5. Privacy
- Training data PII content: <none / pseudonymized / aggregated>
- Inference-time data: <stored? aggregated? deleted?>
- Member inference + model extraction risk: <tested>

## 6. Security
- Adversarial attack surface (prompt injection, data poisoning,
  evasion): <addressed>
- Access controls
- Model + data encryption

## 7. Transparency + documentation
- Model card: <linked>
- Datasheet for datasets: <linked>
- User-facing transparency: <chatbot disclaimer / AI-label>

## 8. Human oversight (high-risk required)
- Type: <decision review / override / monitoring>
- Frequency: <per decision / sample / threshold>
- Operator training: <documented>

## 9. Conformity assessment (high-risk required)
- Self-assessment OR notified body
- Documentation per Art. 11 + Annex IV

## 10. Post-market monitoring (high-risk required)
- Performance metric thresholds
- Reporting cadence
- Serious incident notification (Art. 73)

## Decision
- Approve / Approve with conditions / Defer / Reject

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

### Recipe 6: Model card template (Google Research format)

```markdown
# Model Card — <Model Name v X.Y>

## Model details
- Developed by: <team>
- Date: <date>
- Version: <version>
- Type: <classification / regression / generative LLM / vision>
- Architecture: <e.g. transformer encoder-decoder, ~7B params>
- Paper / documentation: <URL>

## Intended use
- Primary intended uses: <list>
- Primary intended users: <list>
- Out-of-scope use cases: <list — e.g. medical diagnosis, legal advice>

## Factors
- Relevant subgroups: <demographics, geographies, languages>
- Evaluation factors: <accuracy, bias metrics, latency>

## Metrics
- Performance: <accuracy / F1 / BLEU / etc. with confidence intervals>
- Disaggregated by factor: <per subgroup>

## Evaluation data
- Datasets: <name + version + source + license>
- Motivation
- Preprocessing

## Training data
- Datasets: <name + version>
- Lineage + licensing
- Total size + composition
- PII removal + de-bias steps
- Curation methodology

## Quantitative analyses
- Unitary results
- Intersectional results (subgroup × subgroup)

## Ethical considerations
- Sensitive use cases
- Potential harms + mitigations

## Caveats + recommendations
- Limitations
- Recommended human oversight
- Recommended monitoring
```

### Recipe 7: GPAI obligations (Aug 2025)

```text
Standard GPAI (Art. 53):
- Technical documentation (training process, evaluation, intended use)
- Information + documentation to downstream providers
- EU copyright compliance + summary of training content publicly published
- Cooperation with AI Office

Systemic Risk GPAI (Art. 55; compute >10^25 FLOPs OR designated):
- Above + 
- Standardized model evaluations (incl. adversarial)
- Serious incident reporting
- Cybersecurity protection of model + physical infra
- Energy consumption documentation

Open-source GPAI exemption (Art. 53(2)) for some obligations IF released
under free + open-source license AND parameters + architecture +
documentation public.
```

### Recipe 8: EU AI Act high-risk conformity assessment

```text
Pre-deployment (Art. 43):
1. Risk management system (Art. 9) — ongoing process
2. Data + data governance (Art. 10) — training/test sets quality
3. Technical documentation (Art. 11) — Annex IV
4. Record-keeping (Art. 12) — automatic logging
5. Transparency + info to deployers (Art. 13)
6. Human oversight (Art. 14)
7. Accuracy + robustness + cybersecurity (Art. 15)
8. Quality management system (Art. 17)
9. Conformity assessment — Annex VI (internal) OR Annex VII (with notified body)
10. EU declaration of conformity + CE marking
11. Registration in EU database (Art. 49)

Post-deployment:
- Post-market monitoring (Art. 72)
- Serious incident reporting (Art. 73 — 15 days from awareness)
- Corrective actions (Art. 19)
```

### Recipe 9: Credo AI policy pack

```bash
# https://www.credo.ai/
# Credo offers pre-built policy packs:
# - EU AI Act
# - NIST AI RMF
# - ISO/IEC 42001
# - SOC 2 + AI add-on
# - Industry-specific (FS, healthcare)

# API
curl -X GET 'https://api.credo.ai/v2/registers' \
  -H "Authorization: Bearer $CREDO_AI_API_KEY"

# Assessment
curl -X POST 'https://api.credo.ai/v2/assessments' \
  -H "Authorization: Bearer $CREDO_AI_API_KEY" \
  -d '{"system_id":"<id>","policy_pack":"eu-ai-act-2026"}'
```

### Recipe 10: Holistic AI continuous audit

```bash
# https://www.holisticai.com/
curl -X GET 'https://api.holisticai.com/v1/projects' \
  -H "Authorization: Bearer $HOLISTIC_AI_API_KEY"

# Bias test
curl -X POST 'https://api.holisticai.com/v1/bias/test' \
  -H "Authorization: Bearer $HOLISTIC_AI_API_KEY" \
  -d '{"model_id":"<id>","metric":"demographic_parity"}'
```

### Recipe 11: Bias testing approaches

```text
Pre-processing:
- Reweighing (Kamiran + Calders)
- Disparate impact remover
- Optimized preprocessing

In-processing:
- Adversarial debiasing
- Prejudice remover
- Meta-classifier

Post-processing:
- Equalized odds threshold optimization
- Calibrated equal odds

Common libraries:
- IBM AI Fairness 360 (https://aif360.res.ibm.com/)
- Microsoft Fairlearn (https://fairlearn.org/)
- Google What-If Tool

Metrics:
- Demographic parity (group base rates equal)
- Equal opportunity (TPR equal across groups)
- Equalized odds (TPR + FPR equal)
- Disparate impact ratio
- Calibration

Limitations: fairness metrics can conflict; pick aligned with domain risk.
```

### Recipe 12: Post-market monitoring + incident reporting

```text
EU AI Act Art. 72 — Post-Market Monitoring System:
- Collect data on AI performance in real use
- Monitor accuracy + safety + robustness
- Detect non-conformity
- Annual review minimum
- Plan documented per Annex VIII

EU AI Act Art. 73 — Serious Incident Reporting:
- Notify market surveillance authority within 15 days of awareness
- Serious incident = death, serious harm to health, serious + irreversible
  damage to fundamental rights, serious damage to property / environment
- Investigation cooperation

Cross-reference incident response (`incident-response-nist-sp-800-61`).
```

### Recipe 13: AI vendor evaluation checklist

```text
For AI vendors / sub-processors:
- EU AI Act compliance posture (high-risk Art. 25 obligations on providers)
- Model card + datasheet provided?
- Bias + fairness testing methodology?
- Training data lineage + IP rights?
- Customer-prompts treated as input only (no training)?
- DPA + SCC + TIA if EU transfer
- ISO 42001 cert?
- Incident reporting (15-day if serious)
- Liability allocation
- Service-level (uptime, accuracy SLA)
- Right to audit
- Termination + data return
```

## Examples

### Example 1: First AI inventory + classification

**Goal:** AI inventory + EU AI Act risk classification in 30 days.

**Steps:**
1. Inventory all AI systems (Recipe 4).
2. Per-system risk classification (Recipe 1 + 5).
3. Identify high-risk → conformity assessment path.
4. Limited risk → transparency disclosures.
5. Model cards (Recipe 6) for each.
6. AI Use policy (`policy-authoring-cybersecurity-aup-byod`).

**Result:** Pre-Aug 2026 readiness foundation.

### Example 2: High-risk system pre-deployment

**Goal:** Resume screening AI launch pre-Aug 2026.

**Steps:**
1. Classified high-risk per Annex III §5(a).
2. Conformity assessment per Recipe 8.
3. Bias testing per Recipe 11 (demographic + equal opportunity).
4. Human oversight: HR reviewer per shortlisted candidate.
5. Technical documentation per Annex IV.
6. Post-market monitoring plan (Recipe 12).
7. EU database registration (when registry opens).
8. CE marking + declaration of conformity.

**Result:** EU AI Act high-risk launch ready.

### Example 3: ISO 42001 cert

**Goal:** ISO 42001 cert as commercial differentiator.

**Steps:**
1. Build AIMS structure per Recipe 3.
2. Combine with existing 27001 ISMS.
3. Annex A controls implementation.
4. Internal audit (Clause 9.2).
5. Management review (Clause 9.3).
6. Engage Schellman / BSI / A-LIGN for Stage 1 + Stage 2.
7. Cert issued.

**Result:** 42001 cert; EU AI Act readiness signal.

## Edge cases / gotchas

- **EU AI Act extraterritorial.** Applies to providers placing on EU market OR systems whose output is used in EU. Most global SaaS in scope.
- **Penalties scale aggressive.** €35M / 7% (prohibited); €15M / 3% (non-compliance high-risk); €7.5M / 1.5% (other).
- **High-risk Aug 2026 deadline** is hard. Plan early.
- **GPAI obligations Aug 2025** apply now. Verify GPAI providers (OpenAI, Anthropic, Google, Meta, Mistral) comply.
- **Open-source exemption is narrow.** Doesn't apply to systemic risk GPAI; doesn't fully exempt downstream high-risk integration.
- **AI Act + GDPR overlap.** Art. 22 GDPR (no solely automated decision) + AI Act high-risk obligations stack.
- **DPIA + FRIA (Fundamental Rights Impact Assessment).** AI Act Art. 27 mandates FRIA for some high-risk deployments by public authorities + private actors providing public services.
- **EU database registration** — operational mechanism TBD; monitor EC implementation.
- **Notified body capacity** — early 42001 + AI Act conformity assessment availability constrained.
- **Bias metrics conflict.** Demographic parity + equal opportunity can be impossible to satisfy simultaneously. Document tradeoff.
- **Training data IP risk.** Recent litigation (NYT v OpenAI, GitHub Copilot suit). Track copyright + data licensing.
- **GenAI hallucination** is unmitigated risk; document + warn users.
- **Member State enforcement variation** — some DPAs more active on AI than others.
- **Code of Practice (GPAI)** by AI Office; voluntary but signals compliance.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [EU AI Act (Regulation 2024/1689)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R1689)
- [EU AI Act — Artificial Intelligence Act portal](https://artificialintelligenceact.eu/)
- [EU AI Office](https://digital-strategy.ec.europa.eu/en/policies/ai-office)
- [NIST AI Risk Management Framework 1.0](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST AI 100-1 (RMF doc)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
- [NIST AI 600-1 (GenAI Profile)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html)
- [ISO/IEC 23894:2023 (AI Risk)](https://www.iso.org/standard/77304.html)
- [ISO/IEC 23053 (ML Framework)](https://www.iso.org/standard/74438.html)
- [Credo AI](https://www.credo.ai/)
- [Holistic AI](https://www.holisticai.com/)
- [Robust Intelligence](https://www.robustintelligence.com/)
- [Fairly AI](https://www.fairly.ai/)
- [Modulos](https://www.modulos.ai/)
- [IBM AIF360](https://aif360.res.ibm.com/)
- [Microsoft Fairlearn](https://fairlearn.org/)
- [OECD AI Principles](https://oecd.ai/en/ai-principles)
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [MITRE ATLAS](https://atlas.mitre.org/)
- [Schellman ISO 42001](https://www.schellman.com/iso/iso-42001)
