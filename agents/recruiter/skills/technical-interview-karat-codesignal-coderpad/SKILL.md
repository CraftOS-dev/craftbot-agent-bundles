<!--
Sources: https://karat.com/product/
         https://codesignal.com/
         https://coderpad.io/
         https://www.hackerrank.com/products/recruiter
2026 SOTA: live-pairing > take-home (AI cheat risk + candidate-hostile); Karat (IAS) for high
volume; CoderPad gold standard for live; CodeSignal ICF for async filter at top-of-funnel;
HackerRank broad library + budget mid.
Platform decision matrix lives in role.md "Karat / CodeSignal / CoderPad / HackerRank — platform
decision matrix".
-->
# Technical Interview — Karat / CodeSignal / CoderPad / HackerRank — SKILL

Run technical interviews via the right tool for the volume + bias-audit + budget constraint: Karat interview-as-a-service for high volume; CoderPad for live-pairing (gold standard); CodeSignal Industry Coding Framework for async top-of-funnel; HackerRank for breadth + budget; Codility for EU + anti-cheat focus. Live-pairing > take-home in 2026 (AI cheat risk + candidate-hostile).

## When to use

- Question authoring: building role-specific live-pairing problems + rubrics.
- Live-pairing session: setup, language, drawing-mode, recording, post-pad scoring.
- High-volume scaling: Karat as outsourced interview-as-a-service.
- Async top-of-funnel filter: CodeSignal ICF for >500 applicants per req.
- Trigger phrases: "live pairing", "CoderPad", "Karat", "CodeSignal ICF", "HackerRank", "take-home assessment", "technical interview", "AI cheat detection".

Platform decision matrix lives in `role.md` "Karat / CodeSignal / CoderPad / HackerRank — platform decision matrix".

## Setup

```bash
# CoderPad
export CODERPAD_API_KEY="xxx"               # https://coderpad.io/help/api/

# CodeSignal
export CODESIGNAL_API_KEY="xxx"             # https://docs.codesignal.com/recruiter

# HackerRank
export HACKERRANK_API_KEY="xxx"             # https://www.hackerrank.com/work/api

# Karat (partner API — recipient onboarded via Karat sales)
export KARAT_PARTNER_ID="xxx"
export KARAT_API_KEY="xxx"

# Codility
export CODILITY_API_KEY="xxx"

# ATS for sync
export GREENHOUSE_API_KEY="harvest_xxx"
export GH_USER_ID="123456"
export ASHBY_API_KEY="xxx"
```

Auth model: each platform basic-auth or Bearer-token; first-class APIs across all four.

## Common recipes

### Recipe 1: Create CoderPad live-pairing pad
```bash
curl -s -X POST -H "Authorization: Bearer $CODERPAD_API_KEY" \
  -H "Content-Type: application/json" \
  "https://coderpad.io/api/v1/pads" \
  -d '{
    "title": "Senior Backend — Live Pairing — Jane Doe",
    "language": "python",
    "starter_code": "# URL shortener: encode/decode short URL\n",
    "interviewer_email": "interviewer@acme.com",
    "candidate_email": "jane@example.com",
    "duration_minutes": 90,
    "drawing_mode": true,
    "playback": true,
    "anti_cheat": true
  }'
```
Returns `pad_id` + `interview_url` + `candidate_url`. Drawing mode reduces external IDE / AI tab-switch risk.

### Recipe 2: List candidate pad history (for scorecard authoring)
```bash
curl -s -H "Authorization: Bearer $CODERPAD_API_KEY" \
  "https://coderpad.io/api/v1/pads?candidate_email=jane@example.com" \
  | jq '.pads[] | {id, language, created_at, interviewer_email, completed: .ended_at != null}'
```

### Recipe 3: Pull pad playback + transcript
```bash
curl -s -H "Authorization: Bearer $CODERPAD_API_KEY" \
  "https://coderpad.io/api/v1/pads/<pad_id>/playback" \
  -o playback.json
# Use for: review code progression, AI-tab-switch detection, calibration.
```

### Recipe 4: Send CodeSignal async assessment (ICF)
```bash
curl -s -X POST -H "Authorization: Bearer $CODESIGNAL_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.codesignal.com/v1/recruiter/assessments" \
  -d '{
    "test_id": "<icf_test_id>",
    "candidate_email": "jane@example.com",
    "expire_at": "2026-06-20T00:00:00Z",
    "ai_cheat_detection_enabled": true,
    "tab_switch_detection": true,
    "callback_url": "https://hooks.example.com/codesignal/assessment"
  }'
```
ICF (Industry Coding Framework) = standardized scoring across cohort; Cosmo AI detects AI-tool use.

### Recipe 5: Pull CodeSignal result
```bash
curl -s -H "Authorization: Bearer $CODESIGNAL_API_KEY" \
  "https://api.codesignal.com/v1/recruiter/assessments/<assessment_id>" \
  | jq '{candidate_email, score, icf_score, anti_cheat_flags, completion_time_sec}'
# icf_score: 0-850 like SAT scale; thresholds by role (typically 750+ for staff IC)
```

### Recipe 6: HackerRank recruiter platform — send test
```bash
curl -s -X POST -H "Authorization: Bearer $HACKERRANK_API_KEY" \
  -H "Content-Type: application/json" \
  "https://www.hackerrank.com/x/api/v3/candidates" \
  -d '{
    "email": "jane@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "test_id": "<test_id>"
  }'
```

### Recipe 7: Codility test invite (EU-favored, strong anti-cheat)
```bash
curl -s -X POST -u "$CODILITY_API_KEY:" \
  -H "Content-Type: application/json" \
  "https://app.codility.com/api/v3/tickets" \
  -d '{
    "test_id": "<test_id>",
    "candidate_email": "jane@example.com",
    "max_duration_minutes": 120,
    "settings": {"anti_cheat_strict": true, "proctor": true}
  }'
```

### Recipe 8: Karat schedule interview (partner API)
```bash
curl -s -X POST -H "Authorization: Bearer $KARAT_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.karat.com/v1/interviews" \
  -d '{
    "partner_id": "'$KARAT_PARTNER_ID'",
    "candidate": {"email": "jane@example.com", "first_name": "Jane", "last_name": "Doe"},
    "role_template": "senior_backend_engineer",
    "loop_type": "tech_screen_90min",
    "availability_window": ["2026-06-15", "2026-06-22"],
    "ats_candidate_id": "<gh_id>"
  }'
```

### Recipe 9: Pull Karat scorecard
```bash
curl -s -H "Authorization: Bearer $KARAT_API_KEY" \
  "https://api.karat.com/v1/interviews/<interview_id>/scorecard" \
  | jq '{recommendation, competency_scores, transcript_summary, bias_audit_compliant}'
# Karat returns: hire/no-hire + scored rubric + AI-summarized transcript
```

### Recipe 10: Push CoderPad / Karat result to Greenhouse scorecard
```bash
# After live pad: human interviewer submits scorecard to Greenhouse
curl -s -X PATCH -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -H "Content-Type: application/json" \
  "https://harvest.greenhouse.io/v1/applications/<app_id>/scorecards/<scorecard_id>" \
  -d '{
    "overall_recommendation": "yes",
    "attributes": [
      {"name": "Problem decomposition", "rating": 4},
      {"name": "Code quality", "rating": 4},
      {"name": "Communication", "rating": 5}
    ],
    "submitted_by_id": '"$GH_USER_ID"'
  }'
```

### Recipe 11: Tab-switch + AI-tool detection review
```python
# CoderPad: playback shows when candidate switched tabs (often signals AI tool use)
# CodeSignal Cosmo: AI-tool detection score (0-1, higher = more likely AI-assisted)
# Don't auto-reject on detection — calibrate threshold; could be legitimate doc-search.
# Flag for human review; ask candidate during interview about approach.
```

### Recipe 12: Live-pairing question authoring (per role + competency)
```markdown
# Live-pairing problem — Senior Backend Engineer

## Problem
URL shortener:
- Input: long URL
- Output: short hash (6 chars)
- Reverse: short hash → long URL
- Edge: collisions, expiration, analytics

## Time
- 90 min (incl. 5 intro + 5 questions at end)

## Expected coverage
- 0-15 min: clarification + design (data model + collision strategy)
- 15-60 min: implementation (encode/decode + storage)
- 60-80 min: extension (concurrency / scale / persistence)
- 80-90 min: candidate Q&A

## BAR rubric (per role.md "Interview kit components")
- 1 (failed): can't decompose; gets stuck on encode
- 2 (below): solves encode/decode but no collision handling
- 3 (met): solves encode/decode + collision strategy + edge cases
- 4 (exceeded): met + scale analysis + persistence model
- 5 (role-model): met + raises consistency / sharding / analytics extension proactively

## Sample answers per BAR level
{snippet of code at level 3 vs level 5}
```

## Examples

### Example 1: High-volume hiring with Karat
**Goal:** 40+ senior backend reqs/quarter; in-house interviewers maxed out.
**Steps:**
1. Decision: Karat — 24h turnaround, bias-audited, scales without internal IC fatigue.
2. Recipe 8: schedule per candidate.
3. Recipe 9: scorecard auto-flows to ATS.
4. Internal team conducts onsite (system design + culture); Karat handles technical screen.

**Result:** 80% reduction in internal IC interview hours; bias-audit defensible; scale unlocked.

### Example 2: Live-pairing for Series-A IC engineer hire (in-house path)
**Goal:** 12 reqs/quarter; team has interview bandwidth.
**Steps:**
1. Recipe 12: authored URL shortener problem; rubric calibrated.
2. Recipe 1: CoderPad pad created per interview.
3. 90-min live-pairing; interviewer follows rubric + scores in 24h.
4. Recipe 10: scorecard pushed to Greenhouse.
5. Quarterly: Recipe 3 review pads → recalibrate rubric.

**Result:** Predictive validity high; team owns calibration; cost = internal IC time.

### Example 3: CodeSignal ICF top-of-funnel filter
**Goal:** 1,200 applicants → top 80 to recruiter screen.
**Steps:**
1. Recipe 4: send ICF to all 1,200 over 7-day window.
2. Recipe 5: pull scores; bucketize.
3. Top 80 by ICF score → advance to recruiter screen.
4. Recipe 11: review Cosmo flags; human review borderline.

**Result:** Funnel narrowed at top; recruiter capacity preserved; bias mitigated by ICF standardization.

## Edge cases / gotchas

- **Take-home in 2026 = anti-pattern.** AI tools (Claude, GPT, Cursor) make take-homes signal-poor + candidate-hostile (unpaid weekend). Live-pairing or async-with-anti-cheat preferred.
- **Live-pair + screen-share + AI overlay risk.** Some candidates run AI on phone or second monitor. Drawing mode + interviewer questioning ("walk me through this decision") reduces.
- **CoderPad cost.** $30-90/pad. Volume justification ≥10 pads/month; otherwise Google Doc + Zoom shareable.
- **CodeSignal ICF cohort sensitivity.** ICF scoring is normed across cohort; absolute scores drift quarter-over-quarter. Use ICF score relative to peers, not as absolute "is this candidate good?"
- **Karat consistency vs nuance.** Karat interviewers are calibrated + bias-audited but lack company context. Use for top-of-loop screen; onsite + values-fit stays in-house.
- **HackerRank library quality varies.** Some questions are overused → search results contaminate. Author custom questions for senior+ roles.
- **Codility EU posture.** Designed for EU candidate base + GDPR-strict. Use when EU is primary hiring market.
- **Bias audit currency.** Karat publishes annual bias audit; verify ≤12 months old (NYC LL144 alignment).
- **Interviewer fatigue → poor rubric scores.** Cap interviewer load at 5 interviews/week (per `interview-panel-goodtime-ashby-scheduling` SLA).
- **Language drift.** Don't force a Java interview on a Python candidate. Match candidate's strongest language unless role requires specific stack.
- **Stress-induced poor signal.** First 10 min of pad often choppy; warm up with low-stakes question + clarification time. Don't score based on those minutes alone.
- **AI detection isn't ground truth.** Cosmo, CoderPad's flags, etc., have ~85-90% accuracy. False positives happen. Use as signal-to-investigate, not auto-reject.
- **Scorecard within 24h.** SLA per `role.md` "Recruiter screen 30-min agenda" tail end. Memory degrades fast; calibration requires fresh notes.
- **Defer to `legal-counsel`** for: bias audit vendor evaluation, AI-detection adverse-impact analysis, jurisdictional compliance for Karat (vendor disclosure under LL144).

## Sources

- [Karat](https://karat.com/product/) + [Karat Partner Docs](https://karat.com/partner-api)
- [CoderPad](https://coderpad.io/) + [CoderPad API](https://coderpad.io/help/api/)
- [CodeSignal](https://codesignal.com/) + [CodeSignal Recruiter Docs](https://docs.codesignal.com/recruiter)
- [HackerRank for Work](https://www.hackerrank.com/products/recruiter)
- [HackerRank API](https://www.hackerrank.com/work/api)
- [Codility](https://www.codility.com/)
- [Cosmo AI cheat detection (CodeSignal)](https://codesignal.com/cosmo/)
- [CoderPad Drawing Mode](https://coderpad.io/help/drawing-mode/)
- [Karat bias audit research](https://karat.com/research/)
- [Greenhouse Scorecards API](https://developers.greenhouse.io/harvest.html#scorecards)
