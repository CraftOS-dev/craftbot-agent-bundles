<!--
Sources: https://www.greenhouse.io/blog/interview-kits
         https://www.ashbyhq.com/learn/articles/interview-kit-design
         https://www.lever.co/blog/interview-feedback-forms
Interview kit = competency model + per-stage assignment matrix + weighted
rubric + sample questions + calibration notes. 4-6 competencies typical;
each interviewer owns 1-2. Quarterly recalibration.
-->
# Interview Kit + Weighted Scoring Rubric — SKILL

Assemble the kit that runs the loop: which interviewer owns which competency, weighted scoring per question, calibration notes, and ATS-deployed templates. Pairs with `structured-interview-star-bar` (the questions) — this skill is the **assembly + weighting + assignment + deployment** layer.

## When to use

- User asks to **build interview kit for new role**, **set weights**, **assign interviewers to competencies**, **deploy kit to ATS**, **quarterly kit refresh**, **post-hire retro on kit**.
- Trigger phrases: "kit for role X", "weight system design more", "who owns competency Y", "deploy kit to Greenhouse", "calibrate panel", "kit refresh".

## Setup

```bash
export NOTION_TOKEN="xxx"                    # source-of-truth kit storage
export GREENHOUSE_API_KEY="xxx"
export ASHBY_API_KEY="xxx"
export LEVER_API_KEY="xxx"
```

## Common recipes

### Recipe 1: Kit anatomy (Notion template)
```markdown
# {Role} — Interview Kit v{N} (last calibrated {date})

## Competencies (4-6 total)
| # | Competency | Weight | Owner stage |
|---|---|---|---|
| 1 | System design | 3 | HM screen + System Design interview |
| 2 | Code quality + debugging | 3 | Technical (live-pairing) |
| 3 | Collaboration + technical leadership | 2 | Peer panel + Skip-level |
| 4 | Values fit + motivation | 1 | Recruiter screen + HM screen |

Weights sum to 9. Each stage has a primary competency owner.

## Per-stage assignment matrix
| Stage | Interviewer | Primary competency | Secondary |
|---|---|---|---|
| Recruiter screen (30 min) | {recruiter} | Values fit | — |
| HM screen (45 min) | {HM} | Values fit deeper | System design light |
| Technical live-pairing (90 min) | {peer engineer 1} | Code quality | Collaboration |
| System design (60 min) | {senior IC / staff} | System design | Collaboration |
| Onsite peer panel × 3 (45 min each) | {peers} | Distribute comps 2 + 3 + cross-cut | — |
| Skip-level (30 min) | {skip} | Collaboration + Values | — |

## STAR questions per competency
[See structured-interview-star-bar — 2-3 STAR per competency]

## BAR rubric per question (1-5)
[See structured-interview-star-bar — observable behaviors only]

## Calibration notes
- Kickoff calibration session before first loop.
- Sample answers per BAR level for each question.
- Quarterly recalibration.
- Post-hire retro at 6 months (which questions predicted performance).
```

### Recipe 2: Weight assignment heuristic
```
Weights reflect "if this competency is weak, can we still hire?"
- Weight 3 (core): NO — competency owner can veto on a 2 here.
- Weight 2 (important): One 2 acceptable with strong 4+ elsewhere.
- Weight 1 (nice-to-have): One 2 acceptable; coachable post-hire.

Typical distribution:
- Senior IC: 3+3+2+1 (two core technical, one collaboration, one values)
- Mgmt: 3+3+2+2 (people-mgmt + product-sense core; technical + values supporting)
- Sales: 3+3+2+1 (quota attainment + discovery core; collaboration + values)
```

### Recipe 3: Push complete kit to Greenhouse
```bash
# For each stage, PATCH the interview with the kit's competency + rubric
for stage_id in $(echo "$STAGE_IDS"); do
  curl -s -u "$GREENHOUSE_API_KEY:" \
    -H "On-Behalf-Of: $GH_USER_ID" \
    -X PATCH "https://harvest.greenhouse.io/v1/jobs/$JOB_ID/job_stages/$stage_id/interviews/<interview_id>" \
    -H "Content-Type: application/json" \
    -d @"./kit/stage_${stage_id}.json"
done

# Where stage_xxx.json includes:
# {
#   "interview_kit": {
#     "instructions": "...",
#     "questions": [...],
#     "evaluation_criteria": [{"name":"System design","weight":3,"description":"BAR 1-5..."}]
#   }
# }
```

### Recipe 4: Push weighted feedback form (Ashby)
```bash
curl -s -X POST "https://api.ashbyhq.com/feedbackForm.create" \
  -u "$ASHBY_API_KEY:" -H "Content-Type: application/json" \
  -d '{
    "title":"Onsite Loop — Senior Backend",
    "questions":[
      {"id":"system_design","title":"System design","type":"RatingFromOneToFour","weight":3,"competency":"system-design"},
      {"id":"code_quality","title":"Code quality + debugging","type":"RatingFromOneToFour","weight":3,"competency":"code-quality"},
      {"id":"collaboration","title":"Collaboration + leadership","type":"RatingFromOneToFour","weight":2,"competency":"collaboration"},
      {"id":"values","title":"Values fit + motivation","type":"RatingFromOneToFour","weight":1,"competency":"values"},
      {"id":"summary","title":"3-5 sentence summary with behavioral evidence","type":"LongText","required":true},
      {"id":"recommendation","title":"Overall recommendation","type":"MultipleChoice","options":["Strong yes","Yes","No","Strong no"],"required":true}
    ]
  }'
```

### Recipe 5: Push feedback template to Lever
```bash
curl -s -u "$LEVER_API_KEY:" \
  -X POST "https://api.lever.co/v1/feedback_templates?perform_as=$LEVER_USER_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "text":"Onsite Loop — Senior Backend",
    "instructions":"Score each competency on BAR 1-5. Quote candidate behavioral evidence.",
    "fields":[
      {"text":"System design","type":"score","weight":3},
      {"text":"Code quality + debugging","type":"score","weight":3},
      {"text":"Collaboration","type":"score","weight":2},
      {"text":"Behavioral evidence","type":"textarea","required":true}
    ]
  }'
```

### Recipe 6: Compute weighted composite score
```python
# After all scorecards submitted for a candidate
scorecards = [
  {'comp': 'system_design', 'weight': 3, 'rating': 4},
  {'comp': 'code_quality', 'weight': 3, 'rating': 4},
  {'comp': 'collaboration', 'weight': 2, 'rating': 5},
  {'comp': 'values', 'weight': 1, 'rating': 4},
]
weighted_sum = sum(s['weight'] * s['rating'] for s in scorecards)
weight_total = sum(s['weight'] for s in scorecards)
composite = weighted_sum / weight_total
print(f"Composite: {composite:.2f} / 5  (hire bar = 3.5)")

# Apply veto rule: any "weight-3 competency at rating 2" = no-hire regardless of composite
veto = any(s['weight'] == 3 and s['rating'] <= 2 for s in scorecards)
if veto:
    print("VETO: core competency below bar — no-hire")
```

### Recipe 7: Per-stage assignment audit
```python
# Pull all interviews for a job; flag if competency owner missing or duplicated
import requests, os
from collections import defaultdict
GH = (os.environ['GREENHOUSE_API_KEY'], '')
JOB_ID = '<id>'

stages = requests.get(f'https://harvest.greenhouse.io/v1/jobs/{JOB_ID}/job_stages', auth=GH).json()
comp_coverage = defaultdict(list)
for st in stages:
    for iv in requests.get(
        f"https://harvest.greenhouse.io/v1/jobs/{JOB_ID}/job_stages/{st['id']}/interviews",
        auth=GH
    ).json():
        for crit in iv.get('interview_kit', {}).get('evaluation_criteria', []):
            comp_coverage[crit['name']].append({'stage': st['name'], 'weight': crit['weight']})

required = {'System design', 'Code quality', 'Collaboration', 'Values fit'}
missing = required - set(comp_coverage.keys())
if missing:
    print(f"❌ MISSING competency coverage: {missing}")
for comp, owners in comp_coverage.items():
    if len(owners) > 2:
        print(f"⚠ {comp} is owned by {len(owners)} stages (duplication)")
```

### Recipe 8: Calibration meeting agenda + practice scoring
```
[5 min]  — Why this kit + Schmidt-Hunter r=0.51
[10 min] — Walk through competencies + weights + assignments
[15 min] — Per-competency: read STAR + walk through BAR with sample answers
[10 min] — Practice: read transcript snippet, all score independently, debate
[5 min]  — Commitments: scorecards within 24h, quote behavioral evidence
```

### Recipe 9: Quarterly recalibration trigger
```python
# Trigger refresh if any of:
# - Last calibration > 90 days
# - Hire rate in role family changed >20% (over/under-hiring signal)
# - Post-hire 6-month performance correlation < 0.4 with composite score
# - New competency added or removed from competency model
```

### Recipe 10: Post-hire retro — what did the kit predict
```python
# 6 months after each hire: pull composite score from kit + 6-month perf rating
# Compute Spearman correlation per question
# Questions with low rho → cut from kit (don't differentiate)
# Interviewers with low rho → recalibrate (drift)
```

## Examples

### Example 1: Build kit for Senior Product Designer (new role)
**Goal:** 5-competency model, deployed to Ashby, calibration session held.
**Steps:**
1. Define competencies in Notion: craft, product thinking, collaboration, systems thinking, values (Recipe 1).
2. Assign weights: 3+3+2+1+1 — craft + product thinking are core (Recipe 2).
3. Per-stage assignment: portfolio review (craft), HM screen (product thinking + values), design crit (craft + systems), peer panel (collaboration), skip-level (values + collaboration).
4. Author STAR + BAR via `structured-interview-star-bar`.
5. Push weighted form via Recipe 4.
6. Run 45-min calibration with full panel (Recipe 8) — practice scoring on a sample portfolio.

**Result:** Kit live; panel calibrated; first loop runs Wednesday.

### Example 2: Diagnose under-performing kit
**Goal:** Engineering team complaint: "All hires score 4+ but half underperform at 6 months."
**Steps:**
1. Run Recipe 7 — find competency double-owned ("Code quality" in 4 interviews; halo amplification).
2. Run Recipe 10 — find one interviewer with rho=0.1 between scores and 6-mo performance (recalibrate).
3. Cut "Cultural fit" question — anchor isn't behavioral (Recipe 9 trigger).
4. Refresh kit: redistribute Code quality to one owner; rebuild Cultural fit anchor as observable behavior.
5. Mandatory recalibration session (Recipe 8) before next loop.

**Result:** Kit predictive validity restored; double-coverage gap closed; interviewer drift caught.

## Edge cases / gotchas

- **Weight 3 competency requires a competency OWNER.** A panel where 5 people all kinda score it = no real signal. One person owns; others contribute secondary.
- **Weight sum should be 7-10 for a 4-comp model, 9-12 for 5-comp.** Higher = harder math to interpret; lower = no signal differentiation.
- **Composite score is a guide, not the decision.** Veto rule (weight-3 competency at rating ≤2) overrides composite.
- **Don't add "Strong no" without veto power.** If "Strong no" doesn't veto, it's just "No" with extra theater.
- **More than 6 competencies = noise.** Cut to 4-6.
- **Same competency in 3+ stages = duplication + halo amplification.** Cap at 2 stages.
- **Kit refresh discipline.** Quarterly recalibration; post-hire retro at 6 months. Without retro, kits drift to vanity scoring.
- **Public job-board doesn't show kit, but panel can see it.** Greenhouse Inclusion-mode hides interviewer feedback from other interviewers until they submit — turn this on to avoid anchoring.
- **ATS export of kit for offline calibration.** Greenhouse / Ashby allow PDF / JSON export of kit + scorecards; use for calibration sessions, kit retro, and compliance archive.
- **Defer to `legal-counsel`** for: competency wording that could be discriminatory (e.g., "fits our young / energetic team"), AI-scoring of weighted rubrics in NYC LL144 jurisdiction, EEO-compliant rubric language.

## Sources

- [Greenhouse — Interview Kits](https://www.greenhouse.io/blog/interview-kits)
- [Ashby — Structured Interviewing](https://www.ashbyhq.com/learn/articles/structured-interviewing)
- [Lever — Interview Feedback Forms](https://www.lever.co/blog/interview-feedback-forms)
- [Greenhouse Harvest API — Interview Kits](https://developers.greenhouse.io/harvest.html#interview-kits)
- [Ashby Feedback Forms API](https://developers.ashbyhq.com/reference/feedbackformcreate)
- [HBR — Structured Interviews](https://hbr.org/2016/05/structured-interviews)
