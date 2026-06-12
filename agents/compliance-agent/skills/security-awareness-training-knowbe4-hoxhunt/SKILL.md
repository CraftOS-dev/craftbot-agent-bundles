---
name: security-awareness-training-knowbe4-hoxhunt
description: Security awareness training programs via KnowBe4 (largest content library), Hoxhunt (behavioral / adaptive), SoSafe (EU NIS2 + GDPR), Living Security (board-level HRM), Proofpoint (DLP combo), Arsen (2026 deepfake / voice sim leader), Curricula (Huntress), NINJIO, MetaCompliance, Infosec IQ. Annual mandatory + monthly phishing + role-based content. Required by SOC 2 CC1.4 + ISO 27001 A.6.3 + HIPAA §164.308(a)(5) + PCI DSS Req. 12.6 + GDPR Art. 32 + NIS2 + GLBA.
---

# Security Awareness Training Programs

Annual mandatory baseline + monthly phishing + role-based content + measurement-driven iteration. Compliance-mandated. 2026 standout: AI deepfake / voice simulation (Arsen + Adaptive Security pioneered).

## When to use

User says:
- "Security awareness training" / "SAT"
- "KnowBe4" / "Hoxhunt" / "SoSafe" / "Living Security" / "Arsen"
- "Annual training matrix"
- "GDPR Art. 32 awareness"
- "HIPAA training" / "NIS2 awareness"
- "Role-based security training"
- "AI use training" / "GenAI policy training"

Companion skills: `phishing-simulation-program`, `policy-authoring-cybersecurity-aup-byod`.

## Setup

```bash
# https://www.knowbe4.com/  — largest content library
# https://hoxhunt.com/      — behavioral/adaptive
# https://sosafe-awareness.com/  — EU NIS2 + GDPR strong
# https://www.livingsecurity.com/  — HRM dashboards
# https://www.arsen.co/     — AI deepfake/voice sim
# https://www.curricula.com/ — story-driven (Huntress)
# https://ninjio.com/        — animated
# https://www.metacompliance.com/ — EU compliance
# https://www.infosecinstitute.com/iq/ — comprehensive

export KNOWBE4_API_KEY=<dashboard>
export KNOWBE4_REGION=us  # or eu
export HOXHUNT_API_KEY=<dashboard>
export SOSAFE_API_KEY=<dashboard>
```

Auth notes:
- KnowBe4 KMSAT API requires Diamond tier or above.
- Hoxhunt: API for SSO + reporting; full training delivery web.
- SoSafe: GDPR-friendly EU hosting standard.

## Common recipes

### Recipe 1: Vendor pick guide (2026)

```text
KnowBe4 — pick when:
- Highest volume + compliance documentation primary
- US-based + comprehensive content library
- Phishing sim + training bundle
- Lowest cost at scale

Hoxhunt — pick when:
- Behavioral / adaptive (per-user difficulty)
- Engagement-driven (high participation)
- Want continuous micro-learning vs annual mandatory

SoSafe — pick when:
- EU primary (NIS2 + GDPR aligned)
- Gamification-heavy
- Multi-language EU coverage

Living Security — pick when:
- Board needs HRM (Human Risk Management) dashboards
- Want consolidated risk scoring per user
- Less content depth acceptable

Proofpoint — pick when:
- Already on Proofpoint email security
- Want DLP + awareness bundle

Arsen — pick when:
- High AI deepfake / vishing risk
- Executive impersonation defense critical
- Cutting-edge program

Curricula (Huntress) — pick when:
- SMB / mid-market story-driven content
- Huntress security stack synergy

NINJIO — pick when:
- Animated storytelling for engagement
- Monthly micro-episodes

MetaCompliance — pick when:
- EU + heavy compliance documentation
- Multi-policy attestation workflow integrated
```

### Recipe 2: Annual mandatory training topics (baseline)

```text
Required across SOC 2 + ISO + HIPAA + PCI + GDPR + NIS2 + GLBA + NYDFS:

1. Social engineering + phishing (email, voice, SMS, QR — NEW 2026: AI
   deepfake)
2. Password hygiene + MFA
3. Data handling + classification (Public / Internal / Confidential /
   Restricted)
4. Device security (BYOD overlap; lock screens, encryption, lost device
   reporting)
5. Acceptable Use (AUP) — internet, email, social media
6. Incident reporting (who to call, what to capture, no-blame culture)
7. AI use (NEW 2024+) — explicit ChatGPT / Claude / Copilot / Gemini rules
   for sensitive data
8. Privacy basics (GDPR / CCPA / your jurisdiction)
9. Working remotely (home network, VPN, public Wi-Fi)
10. Physical security (tailgating, clean desk, badge)

Role-based add-ons:
- Engineers: secure coding, secret management, SDLC
- Sales engineers: customer data handling, SE testing
- Finance: invoice fraud, ACH change verification
- HR: PII handling, social media reference checks
- Customer support: identity verification, social engineering
- Executives: targeted attack awareness, BEC defense
- IT / Admins: privileged access, change management
- Customer-facing: data subject rights, DPA / BAA handling
```

### Recipe 3: Cadence + delivery

```text
Annual mandatory: 30-45 min comprehensive course; track completion.

Monthly: phishing simulation (see `phishing-simulation-program`).

Quarterly: micro-learning (5-10 min on specific topic).

Trigger-based:
- At hire (within first 30 days)
- On policy change (re-attest)
- After incident affecting user (just-in-time)
- After failed phishing test (just-in-time learning)

Cadence variation by role:
- All-staff: annual + monthly phishing + quarterly micro
- Privileged users: above + additional privileged-access training quarterly
- Executives: above + targeted (BEC, deepfake) quarterly
- Compliance / SecOps: above + role-specific (vendor mgmt, IR, etc.)
```

### Recipe 4: KnowBe4 API — campaigns + reporting

```bash
# https://developer.knowbe4.com/
# List campaigns
curl -X GET "https://us.api.knowbe4.com/v1/training/campaigns" \
  -H "Authorization: Bearer $KNOWBE4_API_KEY"

# User completion status
curl -X GET "https://us.api.knowbe4.com/v1/training/campaigns/<id>/users" \
  -H "Authorization: Bearer $KNOWBE4_API_KEY"

# Phishing test results
curl -X GET "https://us.api.knowbe4.com/v1/phishing/security_tests/<test_id>/recipients" \
  -H "Authorization: Bearer $KNOWBE4_API_KEY"

# User risk score
curl -X GET "https://us.api.knowbe4.com/v1/users/<id>/risk_score_history" \
  -H "Authorization: Bearer $KNOWBE4_API_KEY"
```

### Recipe 5: Hoxhunt API

```bash
# https://docs.hoxhunt.com/api/
curl -X GET "https://api.hoxhunt.com/v1/users" \
  -H "Authorization: Bearer $HOXHUNT_API_KEY"

curl -X GET "https://api.hoxhunt.com/v1/teams/<id>/training-completion" \
  -H "Authorization: Bearer $HOXHUNT_API_KEY"
```

### Recipe 6: Training-by-role matrix template

```markdown
# Training Matrix — <Co.> — <Year>

| Role | Annual baseline | Quarterly micro | Phishing freq | Specialty | Cadence | Platform | Evidence |
|---|---|---|---|---|---|---|---|
| All staff | 45-min comprehensive | 10-min topic | Monthly | — | Annual + monthly | KnowBe4 | LMS completion |
| Engineer | + Secure coding 30-min | Secret mgmt 10-min | Monthly + dev-targeted | SDLC quarterly | Annual + quarterly | KnowBe4 + Snyk Learn | LMS + Snyk |
| Finance | + Invoice fraud 20-min | ACH verification 10-min | Weekly | BEC handling annual | Annual + monthly | KnowBe4 | LMS + drill records |
| HR | + PII handling 20-min | Recruitment fraud 10-min | Monthly | Background check 1x | Annual + monthly | KnowBe4 | LMS |
| CS | + Customer DSR 30-min | Social engineering 10-min | Weekly | Identity verification 1x | Annual + monthly | KnowBe4 | LMS + audit logs |
| Exec | + BEC defense 20-min | Deepfake awareness 10-min | Weekly | Targeted attack 1x | Annual + quarterly | Arsen | LMS |
| IT Admin | + Privileged access 30-min | Change mgmt 10-min | Monthly | Forensics + IR | Annual + quarterly | KnowBe4 | LMS |
| Compliance | + Framework refresh | Reg update 10-min | Monthly | Specific framework | Annual + quarterly | + Vanta training | LMS |
```

### Recipe 7: AI Use training topics

```text
Mandatory topics for any role using GenAI:

1. What data can / cannot be used in prompts
   - PII / PHI / PCI / customer data → forbidden in public LLM
   - Internal-only data → enterprise tier (sandboxed)
   - Public data → fine

2. Approved tools (org-approved + sanctioned)
   - Enterprise ChatGPT / Claude Workspace / Gemini Workspace
   - Tools with explicit DPA + no-training opt-out

3. Verification
   - LLM hallucination risk
   - Always verify output before action
   - Cite source for factual claims

4. Output handling
   - Output may not be original (copyright / IP)
   - Output may be biased / inaccurate

5. Audit + logging
   - LLM activity logged for compliance
   - No bypass via personal accounts

6. Examples + counter-examples
   - Good: summarize public docs, draft non-sensitive emails
   - Bad: paste customer PII for analysis, generate medical advice

Course platforms:
- KnowBe4 KMSAT (AI module)
- SANS Institute (AI use)
- In-house via Loom + LMS
- Microsoft Copilot for M365 training
```

### Recipe 8: Measurement (what to track)

```text
Per user:
- Annual baseline completion (Y/N + date)
- Quarterly micro-learning completion rate
- Phishing test results (click rate / report rate per quarter)
- Risk score trend (vendor-aggregated)

Per cohort:
- Department + role + tenure breakdowns
- Region + language

Org-wide:
- % completed baseline (target >95%)
- % overdue baseline (action: re-assign + manager escalation at 30+ days)
- Click rate trend (decreases with maturity)
- Report rate trend (INCREASES with maturity — detection culture)
- Credential-entry rate
- Dwell time (faster recognition over time)

Industry benchmarks:
- KnowBe4 Annual Phishing Benchmark Report (free)
- Verizon DBIR (industry context)
- SANS Annual Awareness Report

Reporting:
- Monthly to security leadership
- Quarterly to executive team
- Annually to Board
```

### Recipe 9: Failed-test follow-up (just-in-time learning)

```text
On phishing test click / credential entry:
1. Auto-deliver 1-minute just-in-time learning video (not shame-and-blame).
2. Log on user's risk profile.
3. For repeat clickers (3+ in 12 months):
   - 1:1 with manager
   - Tailored coaching curriculum
   - Heightened scrutiny on sensitive actions (financial, access changes)
4. NEVER public shaming or single-out (kills culture).
```

### Recipe 10: Training completion enforcement workflow

```text
30 days before due: Email reminder + LMS notification.
14 days before: Manager notified.
7 days before: Daily reminder.
0 days (overdue): Manager + IT notified.
30 days overdue: 
  - Access restriction (read-only or temp suspension per AUP)
  - HR escalation
60 days overdue:
  - Mandatory in-person training session
  - Performance review note
90 days overdue:
  - Termination consideration per AUP
```

### Recipe 11: GDPR + NIS2 + HIPAA training language

```text
GDPR Art. 32: "training of employees" mandated as part of security
measures. Document curriculum + attendance.

NIS2 Art. 21(2)(g): "basic cyber hygiene practices and cybersecurity
training" mandatory for essential + important entities.

HIPAA §164.308(a)(5): "implement a security awareness and training program
for all members of its workforce (including management)".

PCI DSS Req. 12.6: "implement a formal security awareness program to make
all personnel aware of the cardholder data security policy and procedures."

SOC 2 CC1.4: "demonstrates commitment to attract, develop, and retain
competent individuals" — training is in scope.

ISO 27001 A.6.3: "personnel and relevant interested parties shall receive
appropriate information security awareness, education, and training."

GLBA Safeguards Rule (2024 update): "implement an information security
training program."

NYDFS 23 NYCRR 500.14: "annual cybersecurity awareness training."
```

### Recipe 12: SOC 2 evidence collection

```text
Required artifacts:
- Annual training curriculum (LMS roster + content list)
- Per-user completion record (timestamp + content + score if applicable)
- Phishing sim results (campaign + click rate + report rate)
- Sign-off attestation (annually + on policy change)
- Acceptable Use Policy attestation per employee
- Manager attestations (for direct reports' completion)

Storage: LMS + Drata / Vanta evidence pipeline (auto-pulled).
Retention: per policy (typically 3-7 years).
```

## Examples

### Example 1: Build baseline awareness program for SOC 2

**Goal:** Annual mandatory + monthly phishing for SOC 2 Type II evidence.

**Steps:**
1. Pick KnowBe4 (largest content library + lowest cost at 50-100 EE).
2. Configure annual KMSAT curriculum (Recipe 2).
3. Role-based add-ons per Recipe 6.
4. Monthly phishing campaigns (see `phishing-simulation-program`).
5. Quarterly micro-learning.
6. Drata / Vanta pulls completion data → SOC 2 evidence.
7. Monthly KPI report to leadership (Recipe 8).

**Result:** SOC 2 CC1.4 + ISO 27001 A.6.3 evidence; ~$15-$30/user/yr cost.

### Example 2: Add AI Use training mid-year

**Goal:** Roll out AI Use policy + training in 30 days.

**Steps:**
1. Draft AI Use policy (`policy-authoring-cybersecurity-aup-byod`).
2. KnowBe4 KMSAT AI module OR build internal 15-min course in LMS.
3. Mandatory completion: all staff within 30 days.
4. Attestation tied to AUP signature.
5. Monthly micro-learning on AI use evolves with policy.

**Result:** AI Use policy + training operational; baseline for EU AI Act + ISO 42001.

### Example 3: Executive deepfake defense (Arsen)

**Goal:** Train executive team for deepfake / voice attacks.

**Steps:**
1. Engage Arsen for AI deepfake / voice sim.
2. Targeted attack scenarios: CEO voice impersonation, CFO video deepfake.
3. Quarterly testing on exec team (not org-wide).
4. Just-in-time coaching post-fail.
5. Quarterly executive brief on threat landscape.

**Result:** Reduces exec susceptibility to BEC + deepfake.

## Edge cases / gotchas

- **Annual one-time isn't enough.** Effective programs do continuous (monthly + quarterly).
- **Report rate matters more than click rate.** High report rate = detection culture; low click rate alone insufficient.
- **Shame-and-blame culture backfires.** Failed tests reduce reporting. Just-in-time learning, not punishment.
- **Cultural + language localization.** EU + APAC roll-outs require native-language content.
- **Time-zone scheduling.** Avoid releasing training only in US business hours for global teams.
- **Completion ≠ comprehension.** Some platforms have low-effort completion paths. Pair with quizzes.
- **Manager engagement is critical.** Manager-led re-emphasis is highest-impact intervention.
- **Repeat clickers are not always low-performers.** Sometimes high-stress + high-volume roles (finance, sales) click more. Adjust expectations.
- **Auditor expectations for evidence.** Need completion + content + date + acknowledgment. Roster screenshots insufficient.
- **AI deepfake training is 2026 differentiator.** Standard email phishing training does not prepare for voice / video.
- **EU NIS2 essential / important entity** requires Board-level training (Art. 20).
- **HIPAA at-hire timing.** Workforce members must train BEFORE accessing PHI; auditors verify.
- **GDPR Art. 32 doesn't specify hours;** focus on documented + risk-appropriate.
- **Cost ranges:** KnowBe4 $15-$30/user/yr; Hoxhunt $20-$50/user/yr; Arsen $40-$80/user/yr; Living Security premium.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [KnowBe4](https://www.knowbe4.com/)
- [KnowBe4 Developer Portal](https://developer.knowbe4.com/)
- [Hoxhunt](https://hoxhunt.com/)
- [SoSafe](https://sosafe-awareness.com/)
- [Living Security](https://www.livingsecurity.com/)
- [Arsen](https://www.arsen.co/)
- [Curricula (Huntress)](https://www.curricula.com/)
- [NINJIO](https://ninjio.com/)
- [MetaCompliance](https://www.metacompliance.com/)
- [Infosec IQ](https://www.infosecinstitute.com/iq/)
- [Proofpoint Security Awareness](https://www.proofpoint.com/us/products/security-awareness-training)
- [KnowBe4 Phishing Benchmark Report](https://www.knowbe4.com/resource-center/free-research-tools/phishing-benchmark-report)
- [Verizon Data Breach Investigations Report](https://www.verizon.com/business/resources/reports/dbir/)
- [SANS Security Awareness Report](https://www.sans.org/security-awareness-training/resources/sans-security-awareness-report)
- [GDPR Art. 32 (Security of processing)](https://gdpr-info.eu/art-32-gdpr/)
- [NIS2 Article 21](https://eur-lex.europa.eu/eli/dir/2022/2555/oj)
- [HIPAA §164.308(a)(5)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-C/section-164.308)
