<!--
Sources: https://hbr.org/2016/05/structured-interviews
         https://www.greenhouse.io/blog/structured-interview-questions
         https://www.ashbyhq.com/learn/articles/structured-interviewing
         https://psycnet.apa.org/record/1998-10661-006
STAR (Situation/Task/Action/Result) + BAR (Behaviorally-Anchored Rubric).
Schmidt-Hunter: unstructured r=0.20 → structured r=0.51. 2.5× predictive lift.
-->
# Structured Behavioral Interviewing — STAR / BAR — SKILL

Author the questions and rubric that make interviews predictive. STAR for question shape, BAR (1-5 behaviorally-anchored levels) for scoring. The single biggest predictive-validity lift in hiring.

## When to use

- User asks to **author STAR questions for a role**, **build BAR rubric**, **calibrate interviewers**, **diagnose a non-predictive interview kit**.
- Trigger phrases: "STAR question for X competency", "rubric for system design", "calibrate the panel", "this kit isn't predicting", "Schmidt Hunter", "behavioral evidence", "anchored rating scale".
- Pair with `interview-kit-rubric-weighted-scoring` for full kit assembly.

## Setup

```bash
# Knowledge base (question bank + rubric)
export NOTION_TOKEN="xxx"                    # https://developers.notion.com/

# Push to ATS interview kit
export GREENHOUSE_API_KEY="xxx"
export ASHBY_API_KEY="xxx"
```

No paid tooling required; the methodology is the value. BrightHire / Metaview / Pillar add AI-coaching layer but aren't required.

## Common recipes

### Recipe 1: STAR question template
```
"Tell me about a time when [specific challenging context aligned with competency].
What was the situation? What was your task? What did you do specifically? What was the outcome — and what did you learn?"

Examples:
- System design: "Tell me about a time you designed a system that needed to scale 10×. What were the constraints? What did you propose? What was the outcome?"
- Conflict: "Tell me about a time you disagreed with a senior peer's technical decision. How did you raise it? What happened?"
- Coaching (mgmt): "Tell me about a time you coached an underperforming report. What was the approach? Outcome?"
- Prioritization: "Tell me about a difficult prioritization call between two important projects. How did you decide?"
```

### Recipe 2: BAR rubric template (1-5 scale)
```
1 (Failed)     — Could not articulate; named tools without rationale; gave hypothetical not actual example.
2 (Below bar)  — Named one trade-off but didn't quantify; surface-level analysis.
3 (Met bar)    — Named 3+ trade-offs; chose primary axis; quantified scale/bottleneck.
4 (Exceeded)   — Met + counter-proposed alternative + quantified cost/latency/reliability impact.
5 (Role-model) — Drove the discussion; raised novel angle; proactively flagged unknowns.

Each anchor must reference OBSERVABLE BEHAVIOR — not personality traits.
BAD: "Strong communicator" → GOOD: "Surfaced disagreement using data, not opinion"
```

### Recipe 3: Competency model authoring (Notion)
```markdown
# Senior Backend Engineer — Competency Model

## Competencies (4-6 total; more = noise)
1. **System design** — owns: HM + senior IC
2. **Code quality + debugging** — owns: peer engineer
3. **Collaboration + technical leadership** — owns: peer + skip-level
4. **Values fit + motivation** — owns: HM + recruiter screen

## STAR questions per competency (2-3 each)
### System design
- Q1: "Tell me about a system you designed that needed to handle 10× growth..."
- Q2: "Walk me through a system where you balanced reliability vs feature velocity..."
- Q3: "Tell me about a time you proposed a design the team initially disagreed with..."

## BAR rubric per question (1-5)
[As in Recipe 2]

## Per-stage assignment matrix
Recruiter screen: comp 4
HM screen: comp 4 deeper + comp 1 light
Technical (90 min live-pairing): comp 2 + comp 3 partial
System design (60 min): comp 1 + comp 3 partial
Onsite peer panel (3× 45 min): comps 2, 3, cross-cut
Skip-level: comp 3 + comp 4 leadership signal
```

### Recipe 4: Push STAR questions into Greenhouse interview kit
```bash
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -X PATCH "https://harvest.greenhouse.io/v1/jobs/<job_id>/job_stages/<stage_id>/interviews/<interview_id>" \
  -H "Content-Type: application/json" \
  -d '{
    "interview_kit":{
      "instructions":"60-min system-design interview. Score System Design (weight 3). See BAR rubric below.",
      "questions":[
        {"question":"Tell me about a system you designed that needed to handle 10× growth. Constraints? Proposal? Outcome?","competencies":["system-design"]},
        {"question":"Walk me through a system where you balanced reliability vs feature velocity. How did you trade off?","competencies":["system-design"]}
      ],
      "evaluation_criteria":[
        {"name":"System design","description":"BAR 1-5: 1 failed, 3 met (3+ trade-offs + quantified), 5 role-model (drove discussion + novel angle)","weight":3}
      ]
    }
  }'
```

### Recipe 5: Push to Ashby feedback form with weighted question
```bash
curl -s -X POST "https://api.ashbyhq.com/feedbackForm.create" \
  -u "$ASHBY_API_KEY:" \
  -d '{
    "title":"System Design — Senior Backend",
    "questions":[
      {
        "id":"system_design",
        "title":"System design (BAR 1-5; see anchor description)",
        "type":"RatingFromOneToFour",
        "weight":3,
        "description":"1: failed — no trade-offs articulated. 3: met — 3+ trade-offs quantified. 4: exceeded — counter-proposal + quantified impact."
      },
      {
        "id":"evidence",
        "title":"Behavioral evidence (quote candidate words)",
        "type":"LongText",
        "required":true
      }
    ]
  }'
```

### Recipe 6: Calibration session script (45 min, pre-loop)
```
[5 min] — Why structured interviews predict 2.5× better (Schmidt & Hunter r=0.51).
[10 min] — Walk through competency model + per-stage assignment matrix.
[15 min] — For each competency, read STAR question + walk through BAR levels with sample answers.
[10 min] — Practice scoring: interviewer reads a transcript snippet, scores 1-5, group debates anchor.
[5 min] — Q&A + commitments (everyone owns 1-2 competencies; scorecards within 24h).
```

### Recipe 7: Detect halo / horns effect post-debrief
```python
# Pull all scorecards per interview loop; flag interviewers whose ratings cluster too tightly
import requests, os, statistics
from collections import defaultdict

GH = (os.environ['GREENHOUSE_API_KEY'], '')
JOB_ID = '<id>'
apps = requests.get(
    f'https://harvest.greenhouse.io/v1/jobs/{JOB_ID}/applications?per_page=100',
    auth=GH
).json()

per_interviewer = defaultdict(list)
for a in apps:
    for sc in requests.get(
        f"https://harvest.greenhouse.io/v1/applications/{a['id']}/scorecards",
        auth=GH
    ).json():
        for attr in sc.get('attributes', []):
            if attr.get('rating'):
                per_interviewer[sc['submitted_by']['id']].append(attr['rating'])

for uid, ratings in per_interviewer.items():
    if len(ratings) > 10:
        std = statistics.stdev(ratings)
        mean = statistics.mean(ratings)
        if std < 0.5:
            print(f"⚠ Interviewer {uid}: low variance ({std:.2f}). Halo/horns risk; recalibrate.")
        elif mean > 4.0 or mean < 2.0:
            print(f"⚠ Interviewer {uid}: extreme mean ({mean:.2f}). Anchor drift; recalibrate.")
```

### Recipe 8: Question quality audit
```
Bad STAR question (cut):
- "What's your biggest weakness?" (hypothetical, no behavior)
- "Tell me about yourself" (no specific challenge)
- "Are you a team player?" (yes/no with no evidence)

Good STAR question (keep):
- "Tell me about the last technical decision you regret. What did you learn?"
- "Walk me through a time you had to make a trade-off between A and B. How did you decide?"
- "Tell me about a time you delivered a hard message to your team. Method?"
```

### Recipe 9: Behaviorally-anchored vs personality-anchored
```
BAD (personality):
1 Poor communicator → 3 Average → 5 Strong communicator

GOOD (behavioral):
1 Could not explain core concept without jargon; required 3+ clarifying questions.
3 Explained core concept in domain language; defended choice when questioned.
5 Adapted depth to audience; surfaced disagreement using data; left interviewer learning something.
```

### Recipe 10: Post-hire retro — which kit predicted offer success
```python
# 6-month post-hire: pull scorecards vs 6-month performance rating
# If interviewer X consistently gave high scores to underperformers → recalibrate
# If question Q never differentiated → cut from kit
```

## Examples

### Example 1: Author kit for Engineering Manager role
**Goal:** 5-competency model with STAR + BAR, deployed to Greenhouse, calibration session run.
**Steps:**
1. Define competencies in Notion (Recipe 3): people-mgmt, technical-judgment, product-sense, conflict, values.
2. Draft 2-3 STAR per competency (Recipe 1).
3. Anchor each with BAR levels (Recipe 2) — observable behaviors only (Recipe 9).
4. Push to Greenhouse (Recipe 4) for each interview stage.
5. Run 45-min calibration session with panel (Recipe 6) — practice score 2 transcript snippets.
6. Quarterly recalibration via Recipe 7 (variance check) + Recipe 10 (post-hire performance link).

**Result:** Calibrated panel; predictive interview kit; defensible scoring.

### Example 2: Audit + fix a non-predictive kit
**Goal:** Engineering team complains interviews don't predict performance. Kit was authored 18 months ago.
**Steps:**
1. Pull scorecards via Recipe 7 — find low-variance interviewer (halo).
2. Audit questions via Recipe 8 — cut 3 hypothetical / personality questions.
3. Rewrite BAR anchors from personality to behavioral (Recipe 9) for 4 competencies.
4. Run mandatory recalibration (Recipe 6) before kit re-enters production.
5. Add post-hire feedback loop (Recipe 10) — review at 6 months.

**Result:** Kit predictive validity restored; interviewer drift caught early; HM trust rebuilt.

## Edge cases / gotchas

- **Hypothetical questions don't work.** "What would you do if..." → candidate gives rehearsed answer. Always anchor on past behavior.
- **Trait-based rubrics destroy predictive validity.** "Confident" / "passionate" / "humble" are not measurable. Convert every anchor to observable behavior.
- **3+ competencies per interview = noise.** Each interview should own 1-2 competencies. More = surface-level coverage.
- **Calibration only at launch is insufficient.** Quarterly recalibration; new interviewers calibrate before first loop.
- **Sample answers per BAR level are non-negotiable** for new interviewers. Without them, "3 = met bar" drifts to "3 = fine".
- **BAR scale of 1-5 vs 1-4.** 1-4 forces a side (no middle). 1-5 includes a true "neutral" — better when you want graduated nuance, worse when you want forced choice.
- **Schmidt & Hunter meta-analysis** baseline: structured interview r=0.51, unstructured r=0.20, work sample r=0.54, IQ r=0.51, integrity test r=0.41, reference check r=0.26. Combine structured interview + work sample = strongest combination.
- **"Cultural fit" without behavioral anchors becomes pattern-matching bias.** Define as observable behaviors (e.g., "demonstrates customer empathy in past examples") not "vibes match".
- **Behavioral evidence must be quoted from the candidate's actual words** in the scorecard. Paraphrasing without quotes = gut feel.
- **Defer to `legal-counsel`** for: question wording that could imply protected-class basis (e.g., "are you planning a family" — never asked), AI-recording of interview-answer analysis, EEO-compliant question authoring.

## Sources

- [HBR — Structured Interviews Predict Performance](https://hbr.org/2016/05/structured-interviews)
- [Greenhouse — Structured Interview Questions](https://www.greenhouse.io/blog/structured-interview-questions)
- [Ashby — Structured Interviewing](https://www.ashbyhq.com/learn/articles/structured-interviewing)
- [Schmidt & Hunter — Validity and Utility of Selection Methods (1998 + 2016 update)](https://psycnet.apa.org/record/1998-10661-006)
- [SHRM — Behaviorally Anchored Rating Scales](https://www.shrm.org/topics-tools/tools/toolkits/using-rating-scales-recommendations)
- [Lever — Interview Feedback Forms](https://www.lever.co/blog/interview-feedback-forms)
