<!--
Sources: https://www.outsail.co/post/lattice-vs-15five-vs-culture-amp-performance
         https://www.performancereviewssoftware.com/blog/lattice-vs-culture-amp-vs-15five-comparison/
Lattice = default growth-stage. 15Five = $9-15 PEPM, week-to-deploy. Culture Amp = research DNA. Leapsome = widest breadth.
-->
# Performance Review Cycle — Lattice / 15Five / Culture Amp / Leapsome — SKILL

Author and run performance review cycles, calibration sessions, 1:1 cadences, and engagement surveys across the four SOTA growth-stage perf-mgmt platforms. Owns cycle authoring (template + question bank + raters + deadlines), calibration runs, 1:1 agenda templates, and eNPS / engagement / exit survey design.

## When to use

- Standing up a **review cycle** (annual, biannual, continuous).
- Authoring a **1:1 cadence + template** for managers.
- Running a **calibration** across managers/teams.
- Designing an **engagement survey** (eNPS, pulse, exit).
- Trigger phrases: "review cycle", "1:1", "calibration", "self review", "manager review", "peer review", "eNPS", "engagement survey", "exit survey".

## Setup

```bash
export LATTICE_API_KEY="xxx"        # https://developers.lattice.com — Enterprise tier
export FIFTEEN5_TOKEN="xxx"         # 15Five Public API
export CULTUREAMP_TOKEN="xxx"       # Culture Amp Account API
export LEAPSOME_API_KEY="xxx"       # Leapsome Open API
export TYPEFORM_TOKEN="xxx"         # Fallback survey when no platform key
export TALLY_TOKEN="xxx"            # Fallback alt
```

Tier notes:
- **Lattice** API requires Enterprise plan; Pro tier exposes webhooks only.
- **15Five** API is on Engage/Perform tier and above.
- **Culture Amp** Account API requires Connect / Engage / Perform module.
- **Leapsome** Open API available across plans.

## Common recipes

### Recipe 1: Author a review cycle (Lattice)
```bash
curl -s -X POST "https://api.latticehq.com/v1/review_cycles" \
  -H "Authorization: Bearer $LATTICE_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"H2 2026 Performance Review",
    "type":"360",
    "include_self_review":true,
    "include_manager_review":true,
    "include_peer_review":true,
    "include_upward_review":false,
    "scheduled_open_date":"2026-09-01",
    "scheduled_close_date":"2026-09-30",
    "calibration_window_start":"2026-10-01",
    "calibration_window_end":"2026-10-10",
    "rating_scale":{"name":"5-point","values":["Below","Approaching","Meets","Exceeds","Vastly Exceeds"]}
  }'
```

### Recipe 2: Question bank for self + manager review
```json
{
  "self_review": [
    {"prompt":"What achievement are you most proud of this cycle?","type":"long_text"},
    {"prompt":"Where did you fall short of your goals? What did you learn?","type":"long_text"},
    {"prompt":"What is one stretch goal for the next cycle?","type":"long_text"},
    {"prompt":"Self-rating on each of your role competencies","type":"rating_per_competency"}
  ],
  "manager_review": [
    {"prompt":"Summarize impact this cycle in 3-5 bullets.","type":"long_text"},
    {"prompt":"Rate performance against role expectations.","type":"rating_5"},
    {"prompt":"One strength to double down on.","type":"short_text"},
    {"prompt":"One growth area, with a specific behavioral example.","type":"long_text"},
    {"prompt":"Promotion readiness: ready / not yet / needs another cycle.","type":"single_select"}
  ],
  "peer_review": [
    {"prompt":"What does this person do exceptionally well?","type":"long_text"},
    {"prompt":"What would make them more effective?","type":"long_text"}
  ]
}
```

### Recipe 3: 1:1 cadence + template (15Five Weekly)
```bash
curl -s -X POST "https://api.15five.com/v1/objectives/checkin_template" \
  -H "Authorization: Token $FIFTEEN5_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "name":"Weekly 1:1 — Manager + Direct",
    "cadence":"weekly",
    "questions":[
      {"text":"What went well this week?","type":"text"},
      {"text":"Where did you get stuck or need help?","type":"text"},
      {"text":"What is the most important thing for next week?","type":"text"},
      {"text":"Rate your morale 1-5","type":"rating_5"},
      {"text":"Topics to discuss in our 1:1","type":"text"}
    ]
  }'
```

### Recipe 4: Engagement survey (Culture Amp)
```bash
curl -s -X POST "https://api.cultureamp.com/v1/surveys" \
  -H "Authorization: Bearer $CULTUREAMP_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "name":"H2 2026 Engagement",
    "type":"engagement",
    "open_date":"2026-08-15",
    "close_date":"2026-08-29",
    "demographics":["department","tenure_bucket","location"],
    "factors":["motivation","alignment","leadership","manager_effectiveness","peer_relationships","growth","wellbeing"],
    "anonymity_threshold":5
  }'
```

### Recipe 5: eNPS standard question (Typeform fallback)
```bash
curl -s -X POST "https://api.typeform.com/forms" \
  -H "Authorization: Bearer $TYPEFORM_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "title":"eNPS Q3 2026",
    "fields":[
      {"title":"On a scale of 0-10, how likely are you to recommend this company as a place to work?","type":"opinion_scale","properties":{"steps":11,"start_at_one":false}},
      {"title":"What is the single biggest reason for your score?","type":"long_text"},
      {"title":"What would move your score up by 1?","type":"long_text"}
    ]
  }'
```

### Recipe 6: Calibration session prep (Lattice)
```bash
# Pull all ratings for a team, group by manager, surface outliers
curl -s "https://api.latticehq.com/v1/review_cycles/<cycle>/ratings?team_id=<team>" \
  -H "Authorization: Bearer $LATTICE_API_KEY" \
  | jq '[.[] | {employee, manager, rating, percentile: (.rating / 5 * 100)}]
        | group_by(.manager)
        | map({manager: .[0].manager, avg: (map(.rating) | add/length), exceeds_pct: (map(select(.rating>=4)) | length / length * 100)})'
```

### Recipe 7: Calibration grid (9-box) Notion publish
```python
# 9-box: performance × potential per direct report
import requests, os
NOTION = {'Authorization': f"Bearer {os.environ['NOTION_TOKEN']}", 'Notion-Version':'2022-06-28'}
for emp in lattice_emps:
    box = compute_9box(emp['perf_rating'], emp['potential_rating'])
    requests.post('https://api.notion.com/v1/pages', headers=NOTION, json={
        'parent':{'database_id':'<calibration-db>'},
        'properties':{
            'Name':{'title':[{'text':{'content':emp['name']}}]},
            '9-Box':{'select':{'name':box}},      # e.g., "Star","Core","Risk"
            'Manager':{'people':[{'id':emp['manager_id']}]}
        }
    })
```

### Recipe 8: Manager training rollout (Leapsome Learning)
```bash
curl -s -X POST "https://api.leapsome.com/v1/learning/paths" \
  -H "Authorization: Bearer $LEAPSOME_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "title":"New Manager — First 90 Days",
    "modules":[
      {"title":"Running a great 1:1","duration_minutes":30},
      {"title":"Giving difficult feedback","duration_minutes":45},
      {"title":"Compensation conversations","duration_minutes":30},
      {"title":"Performance plans (PIP) — when and how","duration_minutes":60}
    ],
    "assign_to":"role:Manager",
    "due_within_days":90
  }'
```

### Recipe 9: Exit survey (template)
```json
{
  "questions": [
    {"prompt":"What is the primary reason you are leaving?","type":"single_select","options":["Comp","Growth","Manager","Work-life","Culture","Role fit","Other"]},
    {"prompt":"Would you recommend working here? (0-10)","type":"opinion_scale"},
    {"prompt":"What did we get right that we should keep doing?","type":"long_text"},
    {"prompt":"What is the single biggest improvement we could make?","type":"long_text"},
    {"prompt":"Would you return in the future under different circumstances?","type":"single_select","options":["Yes","Maybe","No"]}
  ]
}
```

### Recipe 10: Mid-cycle pulse (15Five)
```bash
curl -s -X POST "https://api.15five.com/v1/pulse" \
  -H "Authorization: Token $FIFTEEN5_TOKEN" -H "Content-Type: application/json" \
  -d '{"frequency":"biweekly","questions":[{"text":"How are you feeling this week? (1-5)","type":"rating_5"}]}'
```

## Examples

### Example 1: First-ever review cycle for a 35-person team
**Goal:** Stand up cycle from zero in 2 weeks, calibration, results delivery.
**Steps:**
1. Recipe 1: create Lattice cycle, scheduled open 2026-09-01, close 2026-09-30.
2. Recipe 2: customize the question bank in Lattice template.
3. Manager training rollout — Recipe 8.
4. Open cycle — automated email + Slack DM via Lattice.
5. Recipe 6: pull ratings, build calibration prep deck (`pptx` skill).
6. Calibration session — adjust outliers, publish final ratings.
7. Recipe 7: 9-box export to Notion for leadership review.

**Result:** Documented cycle, calibrated ratings, manager-ready compensation conversation inputs.

### Example 2: Stand up weekly 1:1 cadence + eNPS quarterly
**Goal:** Manager hygiene + lightweight pulse.
**Steps:**
1. Recipe 3 in 15Five — template + auto-assign to all manager pairs.
2. Recipe 10 — biweekly pulse, alternating with 1:1 weeks.
3. Recipe 5 — Typeform eNPS quarterly, results summary in Notion `People/Engagement/Q*`.

**Result:** Cadence runs itself; ops lead reviews trends monthly.

## Edge cases / gotchas

- **Anonymity thresholds.** Culture Amp default is 5; never report below threshold. Slicing by small demographics (e.g., one team of 3) leaks identity.
- **Calibration drift.** Without Recipe 6 prep, calibration sessions become "vibe sessions." Pre-pull ratings + outliers per manager.
- **Promotion readiness ≠ promotion budget.** Don't conflate. Headcount/comp budget is finance-driven (see `compensation-philosophy-bands`).
- **PIP triggers.** A "Below" rating ≠ PIP automatically. PIP requires HR + legal review; **defer to `legal-counsel`** for state-specific PIP/protected-class considerations.
- **Bias controls.** Lattice / 15Five have built-in bias-language detectors on free-text; review enabled by default.
- **eNPS frequency fatigue.** Quarterly is the sweet spot; monthly drives response-rate decay below 40%.
- **Self-review weighting.** Inflated self-ratings are common; never let self-rating > manager rating dictate calibration. Use a fixed manager-anchored process.
- **GDPR for survey free-text.** EU employees have right to erasure on personal data; anonymized survey results are exempt only if truly anonymized (no demographics with sample ≤ threshold).
- **Manager training scope.** Recipe 8 modules should include legal basics (protected-class language, FMLA references) — **defer to `legal-counsel` for the legal module review.**
- **Cycle slippage.** Open ≠ submitted. Track submission rate at day 5, 10, 15; auto-nudge non-submitters at 70% of window.

## Sources

- Outsail — Lattice vs 15Five vs Culture Amp: https://www.outsail.co/post/lattice-vs-15five-vs-culture-amp-performance
- PerformanceReviewsSoftware — Lattice vs Culture Amp vs 15Five 2026: https://www.performancereviewssoftware.com/blog/lattice-vs-culture-amp-vs-15five-comparison/
- Lattice Developer Docs: https://developers.lattice.com/
- 15Five API: https://developer.15five.com/
- Culture Amp Account API: https://academy.cultureamp.com/hc/en-us/articles/4404919039243
- Leapsome Open API: https://leapsome.com/api-docs
- Typeform API: https://www.typeform.com/developers/
