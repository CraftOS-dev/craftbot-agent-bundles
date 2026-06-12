<!--
Sources: https://www.pinpointhq.com/ai/
         https://eightfold.ai/
         https://www.eeoc.gov/laws/guidance/ai-employment-decisions
         https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page
         https://leg.colorado.gov/bills/sb24-205
Critical compliance: NYC LL144 (annual bias audit + candidate disclosure), IL AI Video Interview
Act (consent), CO SB 24-205 (impact assessments eff Feb 2026). EEOC TVRA + Workday lawsuit
(2024 active) are the cautionary tales. Human-in-the-loop is non-negotiable.
-->
# AI Screening — Pinpoint / Eightfold — with Care — SKILL

Deploy AI-assisted screening (Pinpoint AI applicant ranking, Eightfold talent intelligence, Paradox Olivia high-volume) ONLY with: current bias audit, candidate disclosure, demographic-blind input, jurisdictional impact assessment, and human-in-the-loop final decision. Defer audit + jurisdictional compliance to `legal-counsel` before any deployment.

## When to use

- High-volume req (>500 applicants per req) where human screening capacity is binding constraint.
- Top-of-funnel ranking to filter to recruiter-screen-eligible pool.
- Talent intelligence (Eightfold): internal mobility + silver-medalist matching.
- Trigger phrases: "AI screening", "Pinpoint AI", "Eightfold matching", "Paradox Olivia", "auto-applicant ranking", "AI rejection", "bias audit", "NYC LL144", "AEDT compliance".

**Defer to `legal-counsel`** for: jurisdictional compliance (NYC / IL / CO / CA forthcoming), bias-audit vendor evaluation, disclosure language, impact-assessment template.
**Block deployment if:** bias audit >12 months old, disclosure not in place, human-in-the-loop not configured, EEO-1 categories don't pass 4/5 rule in vendor's reported audit.

## Setup

```bash
# Pinpoint AI
export PINPOINT_API_KEY="xxx"             # https://www.pinpointhq.com/developers

# Eightfold
export EIGHTFOLD_API_KEY="xxx"
export EIGHTFOLD_TENANT_ID="acme"

# Paradox Olivia
export PARADOX_API_KEY="xxx"

# Bias audit reports archive
export GOOGLE_DRIVE_OAUTH="<bearer>"

# Disclosure template repo
# Pull from notion-mcp; legal-counsel-approved per jurisdiction
```

Auth model: enterprise paid seat; bias-audit certificate often required before vendor enables API access. Vendor responsibilities split: vendor delivers audited model; recipient owns disclosure + impact assessment + human-in-the-loop oversight.

## Pre-deployment gate checklist

```text
[ ] Vendor bias audit report ≤12 months old, signed by qualified third-party auditor
[ ] Audit covers: race, gender, age (40+), disability proxies; per EEOC TVRA
[ ] 4/5 rule passes per EEO-1 category in vendor-reported audit
[ ] Candidate disclosure published on apply page + auto-ack email + JD
[ ] Disclosure language reviewed by legal-counsel per jurisdiction (NYC LL144, IL AI Video, CO SB 24-205)
[ ] Demographic-blind input confirmed (vendor doesn't ingest race/gender/age)
[ ] Human-in-the-loop final decision rule: no AI-only reject
[ ] Annual recert / audit cadence calendared
[ ] Adverse-impact monitoring quarterly per recruiter-metrics dashboard
[ ] Incident-response plan: how to roll back if model drifts or candidate complains
[ ] Data Processing Agreement (DPA) with vendor reviewed by legal
```

## Common recipes

### Recipe 1: Pinpoint AI — rank applicants per req
```bash
curl -s -X POST -H "Authorization: Bearer $PINPOINT_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.pinpointhq.com/v1/jobs/<job_id>/ai_ranking" \
  -d '{"top_n": 50, "exclude_demographic_fields": true}'
```
Returns ranked candidate list. **Human reviews top 50 before any rejection.**

### Recipe 2: Pull Pinpoint AI bias-audit report
```bash
curl -s -H "Authorization: Bearer $PINPOINT_API_KEY" \
  "https://api.pinpointhq.com/v1/ai/audit?since=2025-06-01" \
  | jq '{last_audit_date, auditor: .auditor_name, eeo_compliance: .eeoc_compliance_summary, four_fifths_pass: .four_fifths_rule_passes}'
```
If `last_audit_date >12 months old`: BLOCK deployment until refresh.

### Recipe 3: Eightfold — talent intelligence for internal candidate matching
```bash
curl -s -X POST -H "Authorization: Bearer $EIGHTFOLD_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.eightfold.ai/v3/jobs/<job_id>/matches" \
  -d '{"source": "internal", "limit": 25, "skill_match_threshold": 0.7}'
```
For internal mobility — feeds `internal-mobility-program` skill.

### Recipe 4: Eightfold — silver-medalist re-engagement matching
```bash
curl -s -X POST -H "Authorization: Bearer $EIGHTFOLD_API_KEY" \
  -d '{"source": "talent_pool", "tag": "silver_medalist", "job_id": "<id>"}' \
  "https://api.eightfold.ai/v3/jobs/<job_id>/matches"
```

### Recipe 5: Paradox Olivia — high-volume conversational screen
```bash
# Olivia engages candidates via SMS/web chat; pre-qualifier questions; schedules screens.
curl -s -X POST -H "Authorization: Bearer $PARADOX_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.paradox.ai/v1/conversations" \
  -d '{
    "candidate_phone": "+15555550100",
    "job_id": "<job_id>",
    "flow_id": "<screening_flow_uuid>",
    "metadata": {"ats_application_id": "<id>"}
  }'
```
Use only for very high volume (retail, call-center, hourly). Not for IC engineering reqs.

### Recipe 6: NYC LL144 candidate disclosure block (apply page + ack email)
```text
"This employer uses an Automated Employment Decision Tool (AEDT) to assist in screening candidates
for [job title]. The tool was developed by [vendor]. The most recent bias audit, conducted by
[independent auditor] on [date], is available at: <link>.

You may request an accommodation (such as alternative selection method or assistance) by contacting
[email] at least 10 business days before your screening date.

NYC residents: per NYC Local Law 144, you have the right to request information about the data used
in the AEDT's decision-making."
```
**Defer exact wording per jurisdiction to `legal-counsel`.**

### Recipe 7: IL AI Video Interview Act consent
```text
"This interview will be recorded and analyzed by an AI tool to help our hiring team. Per Illinois
law (820 ILCS 42), you must consent before we proceed. You may decline AI analysis and complete
the interview without it.

[ ] I consent to AI analysis of my interview.
[ ] I decline; please proceed without AI analysis."
```

### Recipe 8: CO SB 24-205 impact assessment template
```text
# Required pre-deployment + annually for AEDTs affecting "consequential decisions"
# Template fields:
- Tool name + vendor + version
- Decision use case (rank / score / reject / advance)
- Personal data categories ingested
- Demographic-blind status
- Bias audit summary + 4/5 rule result
- Human oversight description
- Risk mitigation (rollback plan, complaint channel)
- Retention period for AI outputs
- Annual review owner
# Defer drafting to legal-counsel.
```

### Recipe 9: Quarterly adverse-impact monitoring (post-deployment)
```python
import pandas as pd
# Pull AI-screened candidate decisions per EEO-1 category over last 90 days
df = pd.read_csv("ai_decisions.csv")  # columns: candidate_id, eeo, ai_score, advanced
df["sel_rate"] = df.groupby("eeo")["advanced"].transform("mean")
maj_rate = df[df["eeo"] == "white_male"]["sel_rate"].iloc[0]
flags = []
for eeo in df["eeo"].unique():
  rate = df[df["eeo"] == eeo]["sel_rate"].iloc[0]
  if rate / max(0.001, maj_rate) < 0.80:
    flags.append({"eeo": eeo, "ratio": rate / maj_rate})
# Flags → legal-counsel for statistical significance test
print(flags)
```

### Recipe 10: Eightfold — workforce intelligence for org planning
```bash
curl -s -H "Authorization: Bearer $EIGHTFOLD_API_KEY" \
  "https://api.eightfold.ai/v3/workforce/skill_gap?role=staff_engineer&geo=us" \
  | jq '{gap_score, recommended_upskilling_paths, market_supply, market_demand}'
```
Hand to `operations-agent` for workforce planning; recruiter consumes for sourcing strategy.

### Recipe 11: Roll back AI-screening deployment if incident
```text
1. Disable AI ranking endpoint (Recipe 1) — fall back to human-only screening.
2. Reverse last 30 days of AI-only rejections (manual review of borderline scores).
3. Notify affected candidates per role.md "Decline template library" post-screen variant.
4. Coordinate with legal-counsel + DEI lead on next steps.
5. Vendor postmortem before re-enabling.
```

### Recipe 12: Vendor selection audit (pre-purchase)
```text
Questions for vendor before signing:
1. When was last bias audit? By whom? Show me the report.
2. What's audited? (Race / gender / age / disability proxies — all required.)
3. 4/5 rule result by category?
4. Demographic-blind input — what gets ingested?
5. Human-in-the-loop design — what's the default? (Should be: AI ranks, human decides.)
6. Disclosure language vendor provides per jurisdiction (NYC / IL / CO / CA).
7. Indemnity if vendor's model violates EEOC?
8. DPA: retention, subprocessor list, data residency.
9. Annual audit refresh cadence + how customer is notified.
10. Workday lawsuit awareness + their differentiation?
```

## Examples

### Example 1: Pinpoint AI deployment for high-volume customer-success role
**Goal:** 1,200 applicants → top 80 to recruiter screen.
**Steps:**
1. Pre-deployment gate checklist passes.
2. Recipe 6 disclosure live on apply page + auto-ack.
3. Recipe 8 CO SB 24-205 impact assessment filed (since recipient does business in CO).
4. Recipe 1 ranks; recruiter reviews top 80 + spot-checks bottom 20 of the next 100 (sanity check).
5. Human decides all advances + rejections.
6. Recipe 9 monitors 4/5 rule monthly first quarter, then quarterly.

**Result:** Screening capacity 10× without AI-only reject; defensible compliance.

### Example 2: Eightfold internal mobility deployment
**Goal:** Surface internal candidates for newly opened Staff Eng req before external posting.
**Steps:**
1. Recipe 3 returns 15 internal matches >0.7 skill threshold.
2. Recruiter reviews + reaches out to top 5; coordinates with managers.
3. Internal candidates get 5 biz days first-look per `internal-mobility-program` skill.
4. If no internal hire: external posting + Recipe 4 for silver-medalist re-engagement.

**Result:** Internal-first culture; faster ramp; lower CPH.

### Example 3: Paradox Olivia for retail seasonal hiring (5,000 reqs)
**Goal:** Seasonal staffing scale.
**Steps:**
1. Vendor audit confirmed; disclosure live.
2. Recipe 5 starts conversations via SMS.
3. Olivia qualifies + schedules screens; pushes qualified to ATS.
4. Human recruiter takes over at "potentially qualified" stage.
5. Recipe 9 monthly monitoring.

**Result:** 80% reduction in time-per-screen; scales without recruiter pod expansion.

## Edge cases / gotchas

- **Bias audits ARE NOT created equal.** Vendor-funded audits with selective methodology aren't credible. Look for independent third-party (e.g., BABL AI, Holistic AI, Eticas) using EEOC TVRA-aligned methodology.
- **NYC LL144 enforcement.** $500-$1,500 per violation; running ≥1 day without bias audit = automatic violation. Use vendor's audit + post candidate disclosure.
- **Workday active lawsuit (Mobley v. Workday).** Plaintiff alleges Workday's algorithmic screening discriminates by race + age + disability. Active 2024-2026. Lesson: vendor's "trust us" isn't enough.
- **HireVue's 2019 facial-expression scoring.** Discontinued after EEOC concerns + Illinois LL violation; classic cautionary example. Don't deploy any tool that analyzes facial expression / voice tone for hiring decisions.
- **AI rejection at scale is the danger zone.** Even with audit, batch-rejecting 800 applicants because AI scored them low generates massive 4/5 risk. Always human-in-the-loop the reject decision.
- **Demographic-blind input still leaks signals.** Name, school, address, hobbies all proxy for demographics. Vendor must demonstrate proxy-detection mitigation, not just "we don't ingest race."
- **CO SB 24-205 (eff Feb 2026).** First-in-nation comprehensive AEDT impact assessment law. Impact assessments are 5-10 page legal docs. Coordinate with `legal-counsel` early; ~30 day prep.
- **CA AB 2930 (proposed 2024-2026).** California AEDT bill — track + prep for similar requirements. Most enterprise-scale recruiters in CA + NY + CO trifecta deployments.
- **Olivia / Paradox = conversational, not predictive.** Olivia is a conversational AI for screening flow — lower compliance burden than predictive ranking but still disclosure-eligible.
- **Vendor lock-in.** Eightfold + Pinpoint AI are deep integrations; switching costs 3-6 months. Negotiate exit + data-portability terms in DPA.
- **Recipient seat tier.** Eightfold enterprise tier required for talent-intelligence APIs; Pinpoint mid-market tier for AI ranking. SMB recipients should fall back to structured-human-screen baseline.
- **Defer to `legal-counsel`** for: vendor selection compliance evaluation, jurisdictional disclosure language, impact assessment authoring, adverse-impact statistical interpretation, incident response, DPA review.

## Sources

- [Pinpoint AI](https://www.pinpointhq.com/ai/) + [Pinpoint developer docs](https://www.pinpointhq.com/developers)
- [Eightfold AI](https://eightfold.ai/)
- [Paradox Olivia](https://www.paradox.ai/olivia)
- [EEOC AI in Employment Decisions](https://www.eeoc.gov/laws/guidance/ai-employment-decisions)
- [NYC LL144 — AEDT](https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page)
- [Illinois AI Video Interview Act (820 ILCS 42)](https://www.ilga.gov/legislation/ilcs/ilcs5.asp?ActID=4015)
- [Colorado SB 24-205](https://leg.colorado.gov/bills/sb24-205)
- [Mobley v. Workday (Workday lawsuit)](https://www.eeoc.gov/newsroom/Mobley-v-Workday)
- [HireVue 2019 EEOC discontinuation](https://epic.org/wp-content/uploads/privacy/ftc/hirevue/EPIC_FTC_HireVue_Complaint.pdf)
- [BABL AI (independent bias auditor)](https://babl.ai/)
- [Holistic AI auditor](https://www.holisticai.com/)
