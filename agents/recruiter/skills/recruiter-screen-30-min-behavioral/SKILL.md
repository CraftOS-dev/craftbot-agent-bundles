<!--
Sources: https://www.smartrecruiters.com/resources/articles/the-recruiter-screen-call
         https://brighthire.ai/
         https://www.metaview.ai/
         https://hbr.org/2016/05/structured-interviews
Recruiter screen = 30 min structured: 5 rapport + 10 role-fit + 5 motivation
+ 5 comp expectation + 5 Q&A. Schmidt-Hunter r=0.51 for structured vs 0.20
unstructured. Scorecard within 24h.
-->
# Recruiter Screen — 30-min Structured Behavioral — SKILL

The first calibrated human conversation in the loop. 30 minutes, structured agenda, scorecard within 24h. Validates must-haves, captures comp expectation, sets candidate-experience tone.

## When to use

- User asks to **run a recruiter screen**, **prep for screen**, **debrief screen**, **convert screen to scorecard**, **decide advance / decline post-screen**.
- Standardizing screen practice for a new recruiter on the team.
- Trigger phrases: "do a screen", "screen call prep", "after the screen", "advance or decline", "comp expectation captured", "Zoom recording for screen".

## Setup

```bash
# Zoom (recording + transcription)
export ZOOM_OAUTH_TOKEN="xxx"                # https://marketplace.zoom.us/
# Otter / Fathom / Read.ai (auto-transcript + AI summary)
export OTTER_API_KEY="xxx"                   # https://otter.ai/api
# BrightHire / Metaview (interview intelligence — paid)
export BRIGHTHIRE_API_KEY="xxx"              # https://brighthire.ai/
# Greenhouse / Ashby / Lever for scorecard push
export GREENHOUSE_API_KEY="xxx"
export GH_USER_ID="xxx"
```

## Common recipes

### Recipe 1: Schedule the screen (Calendly)
```bash
# Send Calendly link with 30-min Zoom event type
curl -s -H "Authorization: Bearer $CALENDLY_TOKEN" \
  "https://api.calendly.com/scheduling_links" \
  -X POST -H "Content-Type: application/json" \
  -d '{"max_event_count":1,"owner":"https://api.calendly.com/event_types/<event_type_uuid>","owner_type":"EventType"}'
```

### Recipe 2: Record + transcribe via Zoom + Otter
```bash
# Zoom — enable cloud recording on the meeting
curl -s -X PATCH "https://api.zoom.us/v2/meetings/<meeting_id>" \
  -H "Authorization: Bearer $ZOOM_OAUTH_TOKEN" \
  -d '{"settings":{"auto_recording":"cloud","cloud_recording":true}}'

# Otter — fetch transcript post-meeting
curl -s -H "Authorization: Bearer $OTTER_API_KEY" \
  "https://otter.ai/api/v2/speeches/<speech_id>/transcript"
```

### Recipe 3: Screen agenda (Notion template)
```
[5 min — Rapport + intro + role context]
- "Quick intro: I'm [name], recruiter at [company]. Today is 30 min, structured."
- Company 1-min pitch: stage, funding, product, current team, scaling toward.
- Role 1-min pitch: title, what they'd own, who they'd work with, why we're hiring now.

[10 min — Role fit]
- "Walk me through your last role: scope, team, biggest things you shipped."
- One STAR per critical must-have.
- Cross-check 1-3 disqualifiers via question phrasing.

[5 min — Motivation]
- "Why are you looking now?"
- "What attracted you to [company]?"
- "If you got an offer in 2 weeks, what would you need to feel great saying yes?"

[5 min — Comp expectation]
- "Quick comp note: we're at $X-$Y base + Z% bonus + W equity. What range works for you?"
- NEVER anchor on their previous salary (banned in CA, NY, MA, WA, IL, CO, RI, +).
- Capture: range, flex, equity-vs-cash preference, non-monetary asks.

[5 min — Q&A + next steps]
- "What can I answer for you?"
- Transparent timeline. Confirm within 5 business days.
```

### Recipe 4: Submit Greenhouse scorecard within 24h
```bash
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -H "Content-Type: application/json" \
  -X PATCH "https://harvest.greenhouse.io/v1/applications/<app_id>/scorecards/<scorecard_id>" \
  -d '{
    "overall_recommendation":"yes",
    "attributes":[
      {"name":"Motivation + role-fit","rating":4},
      {"name":"Communication","rating":4},
      {"name":"Comp band aligned","rating":3}
    ],
    "submitted_by_id": '"$GH_USER_ID"'
  }'
```

### Recipe 5: Submit Ashby feedback
```bash
curl -s -X POST "https://api.ashbyhq.com/feedback.submit" \
  -u "$ASHBY_API_KEY:" -H "Content-Type: application/json" \
  -d '{
    "applicationId":"<app_id>",
    "feedbackFormId":"<form_id>",
    "submittedAt":"2026-06-12T15:00:00Z",
    "ratings":[
      {"questionId":"q_motivation","value":4},
      {"questionId":"q_communication","value":4},
      {"questionId":"q_comp_alignment","value":3}
    ],
    "summary":"Strong motivation, comp aligned at upper end of band. Advance to HM screen.",
    "overallRating":"advance"
  }'
```

### Recipe 6: BrightHire — pull AI summary + key moments
```bash
curl -s -H "Authorization: Bearer $BRIGHTHIRE_API_KEY" \
  "https://api.brighthire.ai/v1/interviews/<interview_id>/summary" \
  | jq '{summary, key_moments, sentiment, keywords}'
```

### Recipe 7: Compute comp expectation vs band — auto-flag
```python
# Pave-anchored band check
import os, requests
PAVE_KEY = os.environ['PAVE_API_KEY']
band = requests.get(
    'https://api.pave.com/v1/comp/benchmark',
    params={'role': 'engineer', 'level': 'senior', 'geo': 'sf', 'company_size': '200-500'},
    headers={'Authorization': f'Bearer {PAVE_KEY}'}
).json()

candidate_expectation = 195000   # captured in screen
band_50 = band['base_salary']['p50']
band_75 = band['base_salary']['p75']

if candidate_expectation > band_75 * 1.1:
    flag = "EXCEEDS_BAND — escalate to HM for decision before HM screen"
elif candidate_expectation < band_50 * 0.85:
    flag = "BELOW_BAND — under-leveling risk or strong negotiation lever"
else:
    flag = "WITHIN_BAND"
print(flag)
```

### Recipe 8: HM handoff summary (Notion)
```markdown
# {Candidate Name} — Recruiter Screen Summary
- **Date:** {date}
- **Recruiter:** {recruiter}
- **Recommendation:** Advance / Decline
- **Comp expectation:** ${range}; flex on {base/equity/signing}; preferences: {cash/equity}
- **Motivation:** {1-2 sentences in their words}
- **Strengths:** {2-3 bullets with behavioral evidence}
- **Concerns:** {1-2 bullets with specific gap}
- **HM prep ask:** {1-3 specific things to validate in HM screen}
```

### Recipe 9: Auto-send next-step email post-screen
```bash
# Advance to HM screen — send within 24h
gh_app_advance_template_id=<id>
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -X POST "https://harvest.greenhouse.io/v1/applications/<app_id>/emails" \
  -d '{"email_template_id":'$gh_app_advance_template_id',"send_at":"now"}'
```

### Recipe 10: Decline template — post-screen
```bash
# See candidate-experience-sla-status-updates for full template library
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -X POST "https://harvest.greenhouse.io/v1/applications/<app_id>/reject" \
  -d '{
    "rejection_reason_id":<id>,
    "rejection_email":{"send_email_at":"now","email_template_id":<post_screen_decline_id>}
  }'
```

## Examples

### Example 1: First screen for Senior Backend candidate
**Goal:** 30 min Zoom, calibrated scorecard, comp captured, HM handoff in <24h.
**Steps:**
1. Calendly 30-min screen with Zoom + cloud recording (Recipe 1, 2).
2. Open Notion screen template (Recipe 3); fill live.
3. Within 2h of call: Otter transcript + AI summary review (Recipe 6).
4. Push scorecard with `overall_recommendation: yes` + comp expectation (Recipe 4).
5. Notion handoff summary posted in `#hiring-{role}` Slack thread (Recipe 8).
6. Auto-advance to HM screen (Recipe 9) → HM gets calibrated context before their screen.

**Result:** HM walks into their screen knowing motivation, comp, strengths, and 1-2 things to specifically validate.

### Example 2: Screen reveals under-leveling — decline + reconnect for adjacent role
**Goal:** Candidate is strong but at Mid-level not Senior; preserve relationship for the adjacent req.
**Steps:**
1. Run normal screen.
2. Auto-flag from Recipe 7: `BELOW_BAND — under-leveling risk`.
3. Submit scorecard `overall_recommendation: no` with specific reason "level mismatch — strong skills at L4, role is L5".
4. Send decline + reconnection template (Recipe 10).
5. Tag candidate `RECONNECT-MID-Q3` for sourcer follow-up.

**Result:** Candidate gets honest feedback + reconnection promise; pipeline option preserved.

## Edge cases / gotchas

- **Never anchor on previous salary.** Banned in CA, NY (statewide + NYC), MA, WA, IL, CO, RI, ME, NV, DE, AL, CT, GA (Atlanta), NJ, NC (Mecklenburg), OH (Cincinnati / Columbus / Toledo), PA (Philadelphia), SC (Columbia), VT, +. Always lead with **your** band first; ask **their range**.
- **Pay-transparency disclosure.** CA SB 1162, NY S9427, CO Equal Pay for Equal Work, WA SB 5761, MD HB 123, IL HB 3129 — comp band must be disclosed proactively in JD AND screen.
- **Zoom recording consent.** Two-party consent states (CA, FL, IL, MD, MA, MT, NV, NH, PA, WA) — recording requires verbal consent at start of call; document in scorecard ("Candidate consented to recording at 0:30").
- **Otter / Fathom / Read.ai data retention.** Default: 90 days. Set to 365+ for audit trail. Configure per-org retention policy in tool settings.
- **24h scorecard SLA.** Beyond 24h, recall fades + scorecards become rationalizations. Hard rule: scorecard before EOD or first thing next morning.
- **Comp captured in scorecard but NOT in candidate notes.** Notes are visible to interviewers downstream and can bias HM screen comp framing. Comp lives in offer-negotiation prep doc + recruiter scorecard only.
- **Decline tone.** Post-screen declines must be specific (one concrete reason) + non-generic (no boilerplate). Boilerplate post-screen declines tank candidate-NPS and Glassdoor rating.
- **BrightHire / Metaview / Pillar legal scope.** Some jurisdictions (IL AI Video Interview Act, CO SB 24-205) require explicit consent + disclosure before recording is processed by AI. Check `legal-counsel` for AI-recording disclosure language.
- **Defer to `legal-counsel`** for: salary-history compliance per jurisdiction, AI-recording consent language, pay-transparency JD wording.

## Sources

- [SmartRecruiters — Recruiter Screen Call](https://www.smartrecruiters.com/resources/articles/the-recruiter-screen-call)
- [HBR — Structured Interviews](https://hbr.org/2016/05/structured-interviews)
- [BrightHire](https://brighthire.ai/)
- [Metaview](https://www.metaview.ai/)
- [Schmidt & Hunter (1998/2016) — Validity and Utility of Selection Methods](https://psycnet.apa.org/record/1998-10661-006)
- [Greenhouse — Structured Interview Questions](https://www.greenhouse.io/blog/structured-interview-questions)
- [Zoom Cloud Recording API](https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/#operation/recordingsList)
- [Otter API](https://otter.ai/api)
