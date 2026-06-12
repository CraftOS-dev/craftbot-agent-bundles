<!--
Sources: https://crosschq.com/360-reference-checks/
         https://www.checkster.com/
         https://www.skillsurvey.com/recruiter-pre-hire-360/
3-4 references (manager + peer + report + optional skip/customer).
Structured 6-8 question script. Survey + phone for senior+. ≤72h SLA.
Crosschq / Checkster / SkillSurvey paid; Typeform + Gmail + Zoom free fallback.
-->
# Reference Checking — Structured 3-4 References — SKILL

Structured reference checks via Crosschq / Checkster / SkillSurvey (paid digital 360) or Typeform + Gmail + Zoom (free phone fallback). 3-4 references; 6-8 question script; ≤72h SLA. Output: reference packet attached to ATS, hire-bar signal for offer extension.

## When to use

- User asks to **start references**, **send Crosschq invite**, **collect reference packet**, **phone references for senior+ role**, **reference flagged a concern**, **reference packet for offer go / no-go**.
- Trigger phrases: "kick off references", "send Crosschq", "reference pre-offer", "manager + peer references", "reference flag review".

## Setup

```bash
# Crosschq (paid)
export CROSSCHQ_API_KEY="xxx"                # https://crosschq.com/api/

# Checkster (paid)
export CHECKSTER_API_KEY="xxx"               # https://www.checkster.com/

# SkillSurvey (paid)
export SKILLSURVEY_API_KEY="xxx"             # https://www.skillsurvey.com/

# Free fallback: Typeform + Gmail + Zoom
export TYPEFORM_TOKEN="xxx"                  # https://developer.typeform.com/
export GMAIL_OAUTH="xxx"
```

## Common recipes

### Recipe 1: Structured 6-8 question script (use across all platforms)
```
1. "In what capacity did you work with [candidate]? Period? Reporting relationship?"
2. "What was [candidate]'s primary scope of responsibility?"
3. "What's the most significant project / outcome you saw them ship?"
4. "How would you describe their working style? Strongest collaborator behaviors?"
5. "What's a growth area where they were stretching? How did they respond to feedback?"
6. "On a 1-10 scale, would you hire them again? Context for any score below 8?"
7. "Is there anything I haven't asked that I should know to make a great hire?"
8. (Senior+ only) "How did they handle [specific challenge — underperforming report, ambiguous priorities, exec disagreement]?"
```

### Recipe 2: Crosschq — send 360 reference request
```bash
curl -s -X POST "https://api.crosschq.com/v1/reference_requests" \
  -H "Authorization: Bearer $CROSSCHQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate":{
      "first_name":"Jane","last_name":"Doe","email":"jane@example.com",
      "position_title":"Senior Backend Engineer"
    },
    "reference_template_id":"<template_id>",
    "min_references_required":3,
    "reference_types":["manager","peer","report"],
    "send_reminder_after_hours":48
  }'
```

### Recipe 3: Crosschq — poll status + pull report
```bash
# Poll status
curl -s -H "Authorization: Bearer $CROSSCHQ_API_KEY" \
  "https://api.crosschq.com/v1/reference_requests/<request_id>"

# Pull complete report
curl -s -H "Authorization: Bearer $CROSSCHQ_API_KEY" \
  "https://api.crosschq.com/v1/reference_requests/<request_id>/report" \
  | jq '{summary, score, flags, references: [.references[] | {name, relationship, responses, ratings}]}'
```

### Recipe 4: Checkster — survey-based reference distribution
```bash
curl -s -X POST "https://api.checkster.com/v2/surveys" \
  -H "Authorization: Bearer $CHECKSTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "survey_template_id":"<template_id>",
    "candidate_email":"jane@example.com",
    "min_completed_surveys":3,
    "auto_remind":true
  }'
```

### Recipe 5: SkillSurvey — pre-hire 360
```bash
curl -s -X POST "https://api.skillsurvey.com/v1/projects" \
  -H "Authorization: Bearer $SKILLSURVEY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate":{"name":"Jane Doe","email":"jane@example.com"},
    "survey_id":"<id>",
    "reference_count_min":3,
    "include_self_assessment":true
  }'
```

### Recipe 6: Free fallback — Typeform 360 reference survey
```bash
# Create one-off Typeform survey from a template
curl -s -X POST "https://api.typeform.com/forms" \
  -H "Authorization: Bearer $TYPEFORM_TOKEN" \
  -H "Content-Type: application/json" \
  -d @typeform_360_reference.json
# Then send link via Gmail to each reference with personal note.
```

### Recipe 7: Reference request email (Gmail)
```
Subject: Reference for {candidate_name} — 15-min ask
Hi {reference_name},

{Candidate} has asked us to confirm references as part of our final interview process for {role} at {company}. They spoke very highly of working with you.

Would you be open to a 15-min Zoom call this week, or to filling out a short survey (link below)?

If a call works, please use this Calendly: {link}
If survey is easier: {typeform_link} — takes ~10 min.

Everything you share is treated confidentially and only used to inform the hiring decision.

Thank you,
{recruiter_name}
```

### Recipe 8: Phone reference — note-taking template
```markdown
# {Candidate} — Reference Call — {Reference Name}
**Date:** {date}
**Duration:** {min}
**Relationship:** {manager/peer/report/customer/skip}
**Period worked together:** {start} - {end} ({months/years})

## Question responses
1. Capacity / period / reporting:
2. Primary scope of responsibility:
3. Most significant project / outcome:
4. Working style + collaborator behaviors:
5. Growth area + response to feedback:
6. Would-you-hire-again (1-10) + context for any sub-8:
7. Anything I haven't asked:

## Recruiter observations
- Tone / hesitation noted: 
- Inconsistencies vs interview signal: 
- Flags / concerns: 

## Recommendation impact
- Reinforces hire (1-5 strength): 
- Flag for HM discussion: 
```

### Recipe 9: Reference packet — push to ATS as attachment
```bash
# Greenhouse
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -X POST "https://harvest.greenhouse.io/v1/candidates/<candidate_id>/attachments" \
  -F "filename=reference_packet_$(date +%Y%m%d).pdf" \
  -F "type=other" \
  -F "content=@./reference_packet.pdf"

# Ashby
curl -s -X POST "https://api.ashbyhq.com/file.upload" \
  -u "$ASHBY_API_KEY:" \
  -F "file=@./reference_packet.pdf" \
  -F "linkedResourceType=candidate" \
  -F "linkedResourceId=<candidate_id>"
```

### Recipe 10: Reference packet review pre-offer
```python
# Compute reference packet score + flag inconsistencies
references = [
  {'name': 'Maria', 'relationship': 'manager', 'wyha': 9, 'flags': []},
  {'name': 'Tom', 'relationship': 'peer', 'wyha': 8, 'flags': []},
  {'name': 'Aisha', 'relationship': 'report', 'wyha': 7, 'flags': ['1:1 cadence inconsistent']},
]
avg_wyha = sum(r['wyha'] for r in references) / len(references)
all_flags = [f for r in references for f in r['flags']]
recommend = "GO for offer" if avg_wyha >= 8 and not any('serious' in f for f in all_flags) else "HOLD for HM discussion"
print(f"WYHA avg: {avg_wyha}; flags: {all_flags}; recommendation: {recommend}")
```

## Examples

### Example 1: Crosschq for Senior Backend pre-offer
**Goal:** 3 references (1 manager + 1 peer + 1 report) collected in 72h before offer extension.
**Steps:**
1. Crosschq POST `/v1/reference_requests` (Recipe 2) with template requiring manager + peer + report.
2. Crosschq emails candidate; candidate submits 3-5 reference names + contact.
3. Crosschq distributes survey to references; sends 48h reminders.
4. At 72h: poll status (Recipe 3); pull complete report.
5. Review for flags + score < 8 contexts; loop in HM if flags.
6. Push packet to Greenhouse (Recipe 9).
7. If `recommend: GO` (Recipe 10) → proceed to offer extension.

**Result:** Reference signal validates offer extension; flags surfaced before offer; defensible decision.

### Example 2: Phone references for VP Eng (no Crosschq seat)
**Goal:** 4 deep phone references for VP-level hire; one ambiguous-priorities-handling question.
**Steps:**
1. Recruiter requests 4 references from candidate (2 prior managers + 1 peer/board member + 1 direct report).
2. Send personal Gmail request (Recipe 7) with Calendly link.
3. Run 30-min Zoom calls; take notes via Recipe 8 template.
4. Add senior+ Q8: "Walk me through how they handled [exec-level priority conflict]."
5. Compile reference packet in Notion → export to PDF.
6. Push to ATS (Recipe 9).
7. Brief CEO / hiring leader before offer; flag any concerns from Q5 or Q6.

**Result:** Deeper reference signal for senior role; flags surfaced; defensible decision.

## Edge cases / gotchas

- **Manager + peer + report mix is non-negotiable.** Manager-only references = sample bias; peer-only = no authority signal; report-only = no leadership signal.
- **Self-selected references skew positive.** Crosschq's 360 model + back-channel references mitigate; phone references with probing follow-up reveal real signal.
- **WYHA (would-you-hire-again) score < 8 is the canary.** Anything 7 or below warrants a follow-up probe — most references know to give 8+; a 7 means something specific.
- **Inconsistency between references.** If manager says "great strategic thinker" but report says "no strategic clarity" → flag for HM discussion. Pattern of inconsistency is a hire signal in itself.
- **Never reference-check without candidate consent.** Back-channel references (where candidate didn't supply) require explicit candidate consent + are illegal in some jurisdictions for non-finalist candidates.
- **GDPR + reference data.** EU candidates: reference data subject to GDPR; can request deletion. Document retention policy.
- **Crosschq / Checkster / SkillSurvey data retention.** Default 12-24 months; configure per legal-counsel guidance.
- **Reference fatigue.** Don't request 6+ references; respect the reference's time. 3 well-chosen > 6 perfunctory.
- **Personal-vs-professional reference mix.** Senior+ roles: 3 professional. Junior IC: 2 professional + 1 character reference acceptable.
- **Reference reveals a problem post-offer-extension.** Rescinding requires `legal-counsel` involvement; FCRA disclosure if reference check was outsourced; documented individualized assessment.
- **Defer to `legal-counsel`** for: rescission wording, GDPR / CPRA reference-data retention, jurisdiction-specific consent requirements, back-channel reference legality.

## Sources

- [Crosschq — 360 Reference Checks](https://crosschq.com/360-reference-checks/)
- [Checkster — Reference Check Platform](https://www.checkster.com/)
- [SkillSurvey — Recruiter Pre-Hire 360](https://www.skillsurvey.com/recruiter-pre-hire-360/)
- [Typeform Developer Docs](https://developer.typeform.com/)
- [Greenhouse Harvest — Attachments](https://developers.greenhouse.io/harvest.html#post-attachment)
- [SHRM — Reference Checking](https://www.shrm.org/topics-tools/tools/toolkits/conducting-background-investigations-reference-checks)
