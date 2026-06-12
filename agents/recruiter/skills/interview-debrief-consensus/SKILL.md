<!--
Sources: https://www.greenhouse.io/blog/the-perfect-interview-debrief
         https://lattice.com/library/the-interview-debrief-template
         https://www.metaview.ai/resources/blog/structured-interview-debriefs
Debrief within 24-48h. Position-then-evidence protocol prevents anchoring.
Hire-bar: unanimous yes OR competency owner strong-yes + no veto.
Disagree-and-commit allowed with logged dissent + 30-day check-in.
-->
# Interview Debrief — Consensus + Disagree-and-Commit — SKILL

The 30-45 minute meeting that turns 5 scorecards into a hire / no-hire decision. Position-then-evidence protocol to break anchoring; consensus default; disagree-and-commit when consensus is impossible; logged dissent.

## When to use

- User asks to **facilitate a debrief**, **break a tie**, **handle a veto**, **document a disagree-and-commit**, **post-debrief decision push**.
- Trigger phrases: "debrief tomorrow at 3", "panel split", "one interviewer vetoed", "disagree and commit", "hire bar met?", "decision log".

## Setup

```bash
export GREENHOUSE_API_KEY="xxx"
export GH_USER_ID="xxx"
export ASHBY_API_KEY="xxx"
export ZOOM_OAUTH_TOKEN="xxx"
export OTTER_API_KEY="xxx"
```

## Common recipes

### Recipe 1: Pull all scorecards before debrief (Greenhouse)
```bash
APP_ID=<id>
curl -s -u "$GREENHOUSE_API_KEY:" \
  "https://harvest.greenhouse.io/v1/applications/$APP_ID/scorecards" \
  | jq '.[] | {interview: .interview, interviewer: .submitted_by.name, recommendation: .overall_recommendation, attributes: .attributes}'
```

### Recipe 2: Pull all feedback (Ashby)
```bash
curl -s -X POST "https://api.ashbyhq.com/feedback.list" \
  -u "$ASHBY_API_KEY:" -H "Content-Type: application/json" \
  -d '{"applicationId":"<app_id>"}' \
  | jq '.results[] | {interviewer: .submittedByUser.name, overallRating, summary, ratings}'
```

### Recipe 3: Debrief agenda (Notion template — read at start)
```
# {Candidate} — Debrief — {Date}
**Total time:** 30-45 min
**Facilitator:** Recruiter
**Decision required by:** EOD today

## Step 1 — Position-then-evidence (10 min)
Each interviewer states yes / no FIRST + 2 specific behavioral evidence points.
NO discussion until everyone has spoken. This avoids anchoring + groupthink.

## Step 2 — Open discussion (15 min)
- Surface where positions converge + diverge
- For divergence: ask each side for strongest counter-argument to their own position
- Reference kit's BAR rubric — was scoring consistent?

## Step 3 — Decision (10 min)
Hire-bar rules:
- Unanimous yes → hire-bar met
- Competency owner strong yes + no veto → hire-bar met
- One veto → hold for stronger evidence OR no-hire
- Tie / hold → propose specific evidence we'd need (deeper reference + working session)

If disagree-and-commit:
- Dissenter logs position + reasoning in ATS
- Team commits; revisit at 30-day check-in if hired
```

### Recipe 4: Compute hire-bar logic
```python
# Apply decision rules across scorecards
scorecards = [
  {'interviewer': 'A', 'role': 'system_design_owner', 'rec': 'strong_yes', 'comp3_rating': 4},
  {'interviewer': 'B', 'role': 'code_quality_owner', 'rec': 'yes', 'comp3_rating': 4},
  {'interviewer': 'C', 'role': 'peer', 'rec': 'yes', 'comp3_rating': 3},
  {'interviewer': 'D', 'role': 'peer', 'rec': 'no', 'comp3_rating': 2},
  {'interviewer': 'E', 'role': 'skip', 'rec': 'yes', 'comp3_rating': 3},
]

recs = [s['rec'] for s in scorecards]
veto = any(s['rec'] == 'strong_no' for s in scorecards)
owner_strong_yes = any(s['role'].endswith('_owner') and s['rec'] == 'strong_yes' for s in scorecards)
unanimous_yes = all(r in ('yes', 'strong_yes') for r in recs)
single_no = sum(1 for r in recs if r == 'no')

if veto:
    decision = "HOLD or NO-HIRE — strong_no veto"
elif unanimous_yes:
    decision = "HIRE — unanimous"
elif owner_strong_yes and single_no <= 1:
    decision = "HIRE — competency owner strong yes + no veto"
elif single_no >= 2:
    decision = "HOLD or NO-HIRE — 2+ no votes"
else:
    decision = "DISCUSS — surface divergence + propose evidence to break tie"
print(decision)
```

### Recipe 5: Log decision in Greenhouse activity feed
```bash
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -X POST "https://harvest.greenhouse.io/v1/applications/<app_id>/activity_feed/notes" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id":'"$GH_USER_ID"',
    "body":"DEBRIEF DECISION: HIRE.\n\nPosition-then-evidence:\n- A (sys design owner): strong yes — drove discussion + counter-proposed\n- B (code quality): yes — clean code, good debugging instinct\n- C (peer): yes — strong collaborator\n- D (peer): no — concerns on team-lead readiness\n- E (skip): yes — high values fit\n\nDecision rule applied: competency owner strong yes + no veto = hire-bar met. D logged dissent re: team-lead readiness; 30-day check-in scheduled.",
    "visibility":"public"
  }'
```

### Recipe 6: Move candidate to Offer stage
```bash
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -X PATCH "https://harvest.greenhouse.io/v1/applications/<app_id>" \
  -d '{"job_stage_id":<OFFER_STAGE_ID>}'
```

### Recipe 7: No-hire path — reject with specific feedback
```bash
# See candidate-experience-sla-status-updates for full decline template
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -X POST "https://harvest.greenhouse.io/v1/applications/<app_id>/reject" \
  -d '{
    "rejection_reason_id":<id>,
    "notes":"Onsite decline. Team valued system design depth (4); concerns on team-lead readiness (2). Reconnect for adjacent IC role in 6 months.",
    "rejection_email":{"send_email_at":"now","email_template_id":<POST_ONSITE_TEMPLATE>}
  }'
```

### Recipe 8: Disagree-and-commit log entry
```bash
# Dissenter logs their position separately so it's preserved
curl -s -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: <dissenter_user_id>" \
  -X POST "https://harvest.greenhouse.io/v1/applications/<app_id>/activity_feed/notes" \
  -d '{
    "body":"DISAGREE-AND-COMMIT: I voted no based on team-lead readiness. Team voted hire on competency owner strong yes. I am committing to support the hire. 30-day check-in scheduled with manager to validate ramp.",
    "visibility":"public"
  }'
```

### Recipe 9: Async debrief (when synchronous impossible)
```
Format (BrightHire / Slack thread):
1. Recruiter posts thread with: candidate name + role + scorecards link.
2. Each interviewer posts position-then-evidence in thread (NO REACTIONS until everyone posts).
3. After all posts, 24h discussion window opens.
4. Recruiter calls decision EOD next day with logged rationale.
```

### Recipe 10: 30-day check-in calendar event (if disagree-and-commit)
```bash
gcalcli add \
  --calendar "<hm@company.com>" \
  --title "30-day check-in: {candidate_name} (disagree-and-commit follow-up)" \
  --when "{accept_date + 30d} 14:00" \
  --duration 30 \
  --description "Validate dissenter's concern: team-lead readiness ramp. Loop in {dissenter}."
```

## Examples

### Example 1: Clean unanimous hire decision
**Goal:** 30-min debrief, decision logged, candidate moved to offer.
**Steps:**
1. Pre-debrief: pull all 5 scorecards (Recipe 1).
2. Read agenda at start (Recipe 3).
3. Position-then-evidence — everyone yes.
4. 5-min discussion confirms no concerns.
5. Recruiter calls decision: HIRE.
6. Log activity feed entry (Recipe 5).
7. Move candidate to Offer stage (Recipe 6).
8. Slack post in `#hiring-backend` with go.

**Result:** Decision in 30 min; candidate moves to offer same day.

### Example 2: Veto debrief
**Goal:** One interviewer strong-no after onsite; surface concern, decide path.
**Steps:**
1. Pre-debrief: pull all scorecards; flag strong-no.
2. Position-then-evidence — dissenter speaks first to avoid being silenced by majority.
3. Open discussion: ask dissenter for strongest counter to majority yes; ask majority for strongest counter to dissenter no.
4. Decision rule: strong-no veto → HOLD for stronger evidence (deeper reference + working session) OR NO-HIRE.
5. Decision called: NO-HIRE with reconnect note.
6. Log activity (Recipe 5); send post-onsite decline (Recipe 7).

**Result:** Defensible no-hire; candidate gets specific feedback + reconnection promise; dissenter's signal preserved.

### Example 3: Disagree-and-commit hire
**Goal:** 4 yes + 1 no; competency owner is yes; team commits past dissent.
**Steps:**
1. Pre-debrief: pull scorecards.
2. Position-then-evidence; dissenter concern surfaces (team-lead readiness).
3. Decision rule: competency owner strong yes + no veto → hire-bar met.
4. Dissenter logs position separately (Recipe 8).
5. 30-day check-in scheduled (Recipe 10) to validate ramp.
6. Move to Offer (Recipe 6).

**Result:** Hire decision; dissent preserved as future signal; check-in protects against confirmation bias.

## Edge cases / gotchas

- **Position-then-evidence is non-negotiable.** Skipping it → first speaker anchors everyone. The whole point is to surface independent positions before discussion contaminates them.
- **"Strong yes / yes / no / strong no"** — 4 options, no neutral. Forces a side.
- **Veto is a strong no, not a no.** Strong no = "I will not be able to work with this person" or "I observed a deal-breaker behavior." Treat seriously.
- **Disagree-and-commit must be logged**, with the dissenter's reasoning preserved. Otherwise, when the hire underperforms 6 months in, the team "forgets" who saw it coming.
- **30-day check-in is mandatory** for disagree-and-commit hires. Without it, dissent becomes irrelevant.
- **Debrief within 24-48h of last interview.** Beyond that, recall fades + scorecards become rationalizations.
- **Async debrief loses signal** compared to sync. Use only when sync genuinely impossible (multi-tz panel). Even then, enforce no-reactions-until-all-posted.
- **Recruiter facilitates but doesn't vote.** Recruiter signal is in the recruiter screen scorecard, not the debrief vote. Mixing creates conflict of interest on offer-accept rate.
- **Hiring manager shouldn't speak first.** Their position anchors the panel. Recruiter calls interviewers in random order; HM third or fourth.
- **Pre-debrief BrightHire / Metaview review** of interview recordings is gold for catching "I felt it" with no behavioral evidence. Defer to evidence over feelings.
- **Defer to `legal-counsel`** for: decision-rationale wording that could imply protected-class basis, AI-summary use in jurisdictions with consent law (IL, CO), retention of debrief notes for EEO audits.

## Sources

- [Greenhouse — The Perfect Interview Debrief](https://www.greenhouse.io/blog/the-perfect-interview-debrief)
- [Lattice — Interview Debrief Template](https://lattice.com/library/the-interview-debrief-template)
- [Metaview — Structured Interview Debriefs](https://www.metaview.ai/resources/blog/structured-interview-debriefs)
- [BrightHire — Debrief Intelligence](https://brighthire.ai/)
- [Amazon Leadership Principles — Disagree and Commit](https://www.amazon.jobs/principles)
- [Greenhouse Harvest API — Activity Feed](https://developers.greenhouse.io/harvest.html#activity-feed)
