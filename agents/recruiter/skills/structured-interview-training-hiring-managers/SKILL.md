<!--
Sources: https://brighthire.ai/
         https://www.metaview.ai/
         https://www.pillar.hr/
         https://www.greenhouse.io/blog/interviewer-training
2026 SOTA: BrightHire / Metaview = post-interview recording + AI summary; Pillar = real-time
coaching during the interview. Structured-interview lift: r=0.20 → r=0.51 predictive validity
(Schmidt & Hunter). Workshop format canonical: 90-min hands-on, recertification annually.
-->
# Structured Interview Training — Hiring Managers — SKILL

Run the 90-min hands-on workshop that trains hiring managers + interviewers to author structured kits, write STAR questions, score on BAR rubric, avoid bias, and facilitate debrief. Deploy interview-intelligence tools (BrightHire / Metaview / Pillar) for replay-based coaching + recertification.

## When to use

- New hiring manager (new hire OR newly promoted from IC): 90-min workshop before first loop.
- Existing HM: annual recertification.
- New interviewer (any IC running first loop): condensed 60-min variant.
- Trigger phrases: "train hiring manager", "interview training", "BrightHire setup", "Metaview replay", "Pillar coaching", "interviewer certification", "structured interview workshop".

## Setup

```bash
# Interview intelligence
export BRIGHTHIRE_API_KEY="xxx"      # https://docs.brighthire.ai/
export METAVIEW_API_KEY="xxx"        # https://docs.metaview.ai/
export PILLAR_API_KEY="xxx"          # https://docs.pillar.hr/

# ATS handoff (workshop completion → ATS interviewer pool)
export GREENHOUSE_API_KEY="harvest_xxx"
export GH_USER_ID="123456"
export ASHBY_API_KEY="xxx"

# Scheduling
export GOOGLE_CAL_OAUTH="<bearer>"   # google-calendar-mcp

# Slides + materials
# python-pptx for workshop deck; notion-mcp for rubric library
```

Auth model: BrightHire / Metaview / Pillar are recipient-paid seats. APIs are first-class. Zoom recording auto-uploads to BrightHire / Metaview via Zoom App marketplace integration.

## Common recipes

### Recipe 1: Configure BrightHire to auto-record interviews (Zoom App)
```bash
# Set up BrightHire Zoom App in admin marketplace (one-time, UI):
# Zoom Marketplace → BrightHire → Authorize → assign meeting hosts.
# Verify scope: meeting.read, recording.read, transcription.read.
# Per-interview: BrightHire pulls from Zoom 5-10 min after meeting ends.

# Programmatic check: list recent recordings
curl -s -H "Authorization: Bearer $BRIGHTHIRE_API_KEY" \
  "https://api.brighthire.ai/v1/interviews?since=2026-06-01" \
  | jq '.[] | {id, candidate_name, interviewer_name, duration_min, summary_status}'
```

### Recipe 2: Pull BrightHire AI summary + speaker analytics
```bash
curl -s -H "Authorization: Bearer $BRIGHTHIRE_API_KEY" \
  "https://api.brighthire.ai/v1/interviews/<id>/summary" \
  | jq '{candidate_talk_pct, interviewer_talk_pct, key_moments, sentiment, follow_up_questions}'
```
Use in HM coaching: "you talked 70% of the time; target <40% in behavioral interview."

### Recipe 3: Metaview — auto-transcribe + smart notes
```bash
curl -s -H "Authorization: Bearer $METAVIEW_API_KEY" \
  "https://api.metaview.ai/v1/interviews/<id>/transcript" \
  | jq '.utterances[] | {speaker, start, end, text}'
# Smart notes endpoint surfaces STAR-format extraction.
curl -s -H "Authorization: Bearer $METAVIEW_API_KEY" \
  "https://api.metaview.ai/v1/interviews/<id>/notes?format=star"
```

### Recipe 4: Pillar — real-time coaching during interview
```bash
# Pillar runs as Zoom App overlay; offers real-time prompts to interviewer.
# Per-role question bank loaded from notion-mcp; configured per HM:
curl -s -X POST -H "Authorization: Bearer $PILLAR_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.pillar.hr/v1/question_banks" \
  -d '{
    "role": "Senior Backend Engineer",
    "competencies": ["system-design", "code-quality", "collaboration"],
    "questions": [...]
  }'
```

### Recipe 5: Workshop schedule via google-calendar-mcp
```python
# google-calendar-mcp insert event
event = {
  "summary": "Interview Training: Senior Backend Hiring",
  "description": "90-min workshop. Pre-work: read scorecard + STAR question bank.",
  "start": {"dateTime": "2026-06-15T14:00:00-07:00"},
  "end": {"dateTime": "2026-06-15T15:30:00-07:00"},
  "attendees": [{"email": "hm@acme.com"}, {"email": "recruiter@acme.com"}],
  "conferenceData": {"createRequest": {"requestId": "uuid", "conferenceSolutionKey": {"type": "hangoutsMeet"}}}
}
# google_calendar.events.insert(calendarId="primary", body=event, conferenceDataVersion=1)
```

### Recipe 6: Workshop deck via python-pptx (90-min agenda)
```python
from pptx import Presentation
from pptx.util import Pt, Inches
prs = Presentation()
agenda = [
  ("0-10 min", "Why structured: r=0.20 → r=0.51 predictive validity (Schmidt & Hunter 2016)"),
  ("10-25 min", "Outcome scorecard authoring — 12-month deliverables, not JD tasks"),
  ("25-45 min", "STAR question writing — workshop 3 questions per attendee"),
  ("45-60 min", "BAR rubric — 1-5 with behavioral anchors per level"),
  ("60-75 min", "Bias awareness — IAT + halo/horns + anchoring; practice interview"),
  ("75-85 min", "Debrief facilitation — position-then-evidence protocol"),
  ("85-90 min", "Recertification path + BrightHire / Metaview replay assignment"),
]
for time, topic in agenda:
  slide = prs.slides.add_slide(prs.slide_layouts[5])
  slide.shapes.title.text = f"{time} — {topic}"
prs.save("hm_workshop_deck.pptx")
```

### Recipe 7: Practice-interview rubric + grading sheet
```text
# In notion-mcp page "HM Practice Interview Rubric":
| Competency | Question asked? | STAR follow-up? | Specific behavioral evidence captured? | BAR score assigned? |
|---|---|---|---|---|
| System design | Y/N | Y/N | Y/N | 1-5 |
| Code quality | Y/N | Y/N | Y/N | 1-5 |
| Collaboration | Y/N | Y/N | Y/N | 1-5 |
# Trainee runs practice interview with peer (15 min) → grader scores → debrief.
```

### Recipe 8: Mark interviewer as "trained" in Greenhouse
```bash
# Custom user field tracks training completion + last-recert date
curl -s -X PATCH -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -H "Content-Type: application/json" \
  "https://harvest.greenhouse.io/v1/users/<user_id>" \
  -d '{"custom_fields": {"interviewer_trained": true, "last_recert_date": "2026-06-15"}}'
```
Scheduler (`interview-panel-goodtime-ashby-scheduling`) gates panel staffing on `interviewer_trained=true`.

### Recipe 9: Mark interviewer trained in Ashby
```bash
curl -s -X POST -u "$ASHBY_API_KEY:" \
  -H "Content-Type: application/json" \
  "https://api.ashbyhq.com/user.update" \
  -d '{"userId": "<id>", "customFields": {"interviewer_trained": true, "last_recert": "2026-06-15"}}'
```

### Recipe 10: Quarterly recertification trigger (HRIS sync)
```python
# Pull interviewers whose last_recert_date >12 months ago
import requests, os, datetime
users = requests.get(
  "https://harvest.greenhouse.io/v1/users?per_page=200",
  auth=(os.environ["GREENHOUSE_API_KEY"], "")
).json()
cut = (datetime.datetime.utcnow() - datetime.timedelta(days=365)).isoformat()
due = [u for u in users if u.get("custom_fields", {}).get("last_recert_date", "1970") < cut]
for u in due:
  print(f"RECERT DUE: {u['name']} {u['emails'][0]['email']}")
  # Schedule via Recipe 5; send Slack DM with BrightHire replay link.
```

### Recipe 11: BrightHire replay-based coaching session
```bash
# Pull HM's last 3 interviews; surface 3 coaching moments per interview.
curl -s -H "Authorization: Bearer $BRIGHTHIRE_API_KEY" \
  "https://api.brighthire.ai/v1/interviews?interviewer_email=hm@acme.com&since=2026-04-01&limit=3" \
  | jq '.[] | {id, candidate: .candidate_name, talk_ratio: .interviewer_talk_pct,
              moments: .key_moments[:3]}'
# Review with HM in 30-min 1:1; flag patterns (over-talking, leading questions, halo).
```

### Recipe 12: New-HM 30-60-90 training plan
```text
# Day 0: 90-min workshop (Recipe 6) + practice interview (Recipe 7).
# Day 7: First real interview shadowed by recruiter; debrief immediately.
# Day 30: BrightHire replay coaching (Recipe 11) of first 3 interviews.
# Day 60: Solo loop facilitator certification (debrief facilitation lead).
# Day 90: Self-serve; Recipe 8 marks `interviewer_trained=true`.
```

## Examples

### Example 1: First-time HM onboarding
**Goal:** New HM Sarah promoted from IC; running first loop in 2 weeks.
**Steps:**
1. Recipe 5: schedule 90-min workshop T-7 days before first loop.
2. Recipe 6: deliver workshop with deck.
3. Recipe 7: peer practice interview at minute 45.
4. Recipe 1 setup: BrightHire records Sarah's first 3 real interviews.
5. Recipe 11: 30-min coaching review with Sarah after interviews 1, 3, 5.
6. Recipe 8: mark `interviewer_trained=true` after coaching review post-interview 3.

**Result:** Sarah trained, calibrated, replay-coached. Scorecard quality high from day 1.

### Example 2: Existing HM annual recert
**Goal:** Annual recertification for the engineering HM cohort.
**Steps:**
1. Recipe 10: nightly cron flags HMs due for recert.
2. Recipe 11 pulls each HM's last 3 interviews; recruiter previews patterns.
3. Recipe 5 schedules 30-min recert sync per HM (not full workshop — focused on patterns).
4. Recipe 8 updates `last_recert_date`.

**Result:** Recert burden distributed monthly, not annual fire-drill.

### Example 3: Pillar real-time coaching pilot for new IC interviewers
**Goal:** New IC interviewer Jake runs first interview with live coaching overlay.
**Steps:**
1. Recipe 4: load question bank for Jake's role + competency.
2. Pre-interview: Jake reviews scorecard + 3 sample STAR follow-ups.
3. During interview: Pillar overlay prompts Jake when candidate gives vague answer ("ask for specific quantification" / "STAR-T: outcome?").
4. Post-interview: Pillar's session summary + recommended next-time improvements.

**Result:** Jake's first interview hits structured-quality bar without a year of practice.

## Edge cases / gotchas

- **HM time scarcity.** 90-min workshop hard to schedule for senior HMs. Compress to 60 min if needed but never <60; cutting bias awareness or practice interview destroys the value.
- **BrightHire / Metaview Zoom App permissions.** Requires admin-level Zoom marketplace install; meeting host must be using the licensed Zoom account; recording must be ON. Misconfig → no recording = no replay.
- **Candidate consent on recording.** Two-party consent states (CA, IL, MA, MT, NH, PA, WA, +): record disclosure required at meeting start. BrightHire / Metaview include auto-disclosure prompts; verify enabled.
- **Pillar real-time prompts can distract.** New interviewers love it; senior interviewers find it noisy. Make opt-in per interviewer.
- **Practice interview quality.** Peer-grader bias; rotate graders + use rubric (Recipe 7) to reduce variance.
- **Recertification ≠ recheckbox.** Annual recert should review BrightHire patterns + 1 practice interview; not a Slack-DM "you good?" Confirm via Recipe 11 + 30-min sync.
- **`interviewer_trained=true` is gateable.** Use it in scheduler (`interview-panel-goodtime-ashby-scheduling`) — untrained interviewers should never staff a loop solo.
- **Training data privacy.** BrightHire / Metaview store interview transcripts; vendor-side retention varies (default 12-24 mo). Confirm vendor DPA covers your data-retention obligations.
- **AI summary ≠ ground truth.** AI summaries hallucinate edge details. Always verify against transcript before using in performance review or rejection rationale.
- **Defer to `legal-counsel`** for: candidate-consent recording wording (per state), interview-intelligence vendor DPA review, bias-training content (avoid making promises about bias elimination).

## Sources

- [BrightHire](https://brighthire.ai/) + [BrightHire docs](https://docs.brighthire.ai/)
- [Metaview](https://www.metaview.ai/) + [Metaview docs](https://docs.metaview.ai/)
- [Pillar.hr](https://www.pillar.hr/)
- [Greenhouse interviewer training](https://www.greenhouse.io/blog/interviewer-training)
- [Schmidt & Hunter 2016 update on structured interview validity](https://journals.aom.org/doi/10.5465/amj.2014.0407)
- [Project Implicit (IAT)](https://implicit.harvard.edu/implicit/)
- [HBR — Structured Interviews](https://hbr.org/2016/05/structured-interviews)
- [Zoom App Marketplace](https://marketplace.zoom.us/)
