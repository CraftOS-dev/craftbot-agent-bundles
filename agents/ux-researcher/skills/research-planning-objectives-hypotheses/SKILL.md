<!--
Sources:
NN/g — When to Use Which UX Research Method — https://www.nngroup.com/articles/which-ux-research-methods/
Erika Hall — Just Enough Research — https://abookapart.com/products/just-enough-research
Dovetail v3 API — https://dovetail.com/help/api
-->
# Research Planning + Objectives + Hypotheses — SKILL

Plan a study against a *decision*, not a topic. Stakeholder goal → research questions (≤5) → testable hypotheses → method per question (Nielsen Norman matrix) → sample + recruitment criteria → deliverable. Anything else is research theater.

## When to use

- A stakeholder asks for research without naming the decision it informs.
- You need to pick the right method (interview vs survey vs usability vs tree test) given the question type.
- You need to scope time + budget + sample size before kicking off recruitment.
- You need to publish a research plan to Notion + a Dovetail project for the synthesis side.

Trigger phrases: "plan a study", "what method should we use", "research plan for X", "scope this research", "write a research brief", "what should we ask users about Y".

## Setup

```bash
# Notion for the canonical plan
curl -fsSL "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28"

# Dovetail for the paired research project
curl -fsSL "https://dovetail.com/api/v1/projects" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN"
```

Auth:
- `NOTION_API_KEY` — Notion integration token; share the `Research Plans` database with the integration.
- `DOVETAIL_API_TOKEN` — Dovetail → Settings → API. Paid plan ($199/mo+).

## Common recipes

### Recipe 1: Erika Hall question-first hierarchy

Drive every research plan from this hierarchy. Skip a level and the plan is theater.

1. **Decision (1 sentence)** — what changes based on findings? "We'll scope notifications surface in Q3" OR "We'll deprioritize the inbox redesign for next quarter."
2. **Research questions (≤5)** — specific, answerable by data.
3. **Hypotheses (optional, testable)** — what would change our mind.
4. **Method per question** — Nielsen Norman matrix (next recipe).
5. **Sample + recruitment** — segment + behavior + anti-screens.
6. **Deliverable** — readout doc + Dovetail insights + Linear handoff.

### Recipe 2: NN/g method matrix (pick the method by question type)

| Question type | First-choice method | Alt |
|---|---|---|
| What do users *do*? (behavior) | Analytics + session replay + contextual inquiry | Diary study (longitudinal) |
| What do users *think*? (attitude) | Interview | Survey for scale |
| Generative (discover what matters) | JTBD interview, diary study, ethnography | Contextual inquiry |
| Evaluative (test a design) | Moderated usability (5/round) OR unmoderated (Maze/UserTesting) | Heuristic eval + cognitive walkthrough |
| Qualitative (why) | Interview, think-aloud, contextual inquiry | — |
| Quantitative (how much) | Survey (100-400/segment), large-N tree test, A/B test | — |
| Where do users get stuck in IA? | Tree test (Treejack, N≥50) | Card sort if categories not yet defined |
| First-impression / hierarchy | First-click (Chalkmark, N≥30) + 5-second (Lyssna) | — |

### Recipe 3: Research plan template (Notion)

```markdown
# Research Plan: [Study Name]

**Date:** [YYYY-MM-DD] · **Researcher:** [Name] · **Stakeholder:** [Name + role]

## Decision this informs
[1-2 sentences — what decision changes based on findings? Without this, the study is theater.]

## Research questions (≤5)
1. [Specific question — answerable by data]
2. ...

## Hypotheses (optional)
- [Hypothesis with falsifiable prediction]

## Method
- **Choice:** [moderated usability / tree test / JTBD interview / diary study / heuristic eval / etc]
- **Rationale:** [Why this method for these questions — pick from NN/g matrix]
- **Sample size + justification:** [N + reason]

## Sample + recruitment
- **Segment:** [Behavioral + demographic criteria]
- **Anti-screens:** [Professional respondent guard, industry guard]
- **Panel:** [User Interviews / Respondent / dscout / Prolific / in-house]
- **Incentive:** [$X per session]

## Timeline
- Recruit: [date range]
- Sessions: [date range]
- Synthesis: [date range]
- Readout: [date]

## Deliverable
[Notion readout + Dovetail insights + Linear handoff?]

## Risks
- [Recruitment / scoping / stakeholder alignment]
```

### Recipe 4: Push the plan to Notion

```bash
PLAN_DB="<research-plans-db-id>"

curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "{
    \"parent\": {\"database_id\": \"$PLAN_DB\"},
    \"properties\": {
      \"Name\": {\"title\": [{\"text\": {\"content\": \"Inbox-overload generative — Q3 2026\"}}]},
      \"Status\": {\"select\": {\"name\": \"Planning\"}},
      \"Method\": {\"select\": {\"name\": \"JTBD interview\"}},
      \"Sample target\": {\"number\": 12}
    }
  }"
```

### Recipe 5: Pair the plan to a Dovetail project

```bash
# Create the Dovetail project; tag the project ID into the Notion plan
PROJECT_ID=$(curl -fsSL -X POST "https://dovetail.com/api/v1/projects" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Inbox-overload generative — Q3 2026","template":"interview_study"}' \
  | jq -r '.data.id')

echo "Dovetail project: $PROJECT_ID"
# Then PATCH the Notion plan to add the Dovetail URL field
```

### Recipe 6: Sample-size justification cheat sheet

| Method | N | Rationale |
|---|---|---|
| Moderated usability | 5 per round | Nielsen — 85% of issues surface |
| Unmoderated usability | 15-30 | Statistical lift on task success |
| Tree test (Treejack) | ≥50 | Stable directness % |
| Card sort | ≥30 | Stable similarity matrix |
| First-click (Chalkmark) | ≥30 | Stable heatmap |
| 5-second test | 15-30 | First-impression stabilization |
| JTBD interviews | 15-25 | Saturation at 12-15 |
| Contextual inquiry | 12-15 sites | Saturation |
| Diary study (dscout) | 8-15 × 7-30 days | Longitudinal |
| Heuristic eval | 3-5 evaluators | Beyond 5, diminishing returns |
| Cognitive walkthrough | 1-3 evaluators | Solo OK |
| Accessibility | 5-8 per AT category | Per screen-reader / per magnifier / per switch |
| Survey (descriptive) | 100-400 per segment | ±5% margin |

### Recipe 7: Stakeholder alignment 1-pager (pre-research)

```markdown
# Research Brief: [Study Name] — Stakeholder Alignment

**To:** [Stakeholder name + role]
**From:** [Researcher]
**Date:** [YYYY-MM-DD]

## The decision
[What you'll decide based on findings. 1-2 sentences. Sign off here before recruit starts.]

## What this research will + will NOT tell you
- ✅ Will tell you: [specific outcome]
- ❌ Will not tell you: [common stakeholder request that's out of scope — be explicit]

## Sample + method (in plain English)
- We'll talk to [N] [segment] for [duration].
- We'll [method] — meaning [what happens].
- Cost: $[budget total].

## Timeline + readout
- Recruit + sessions: [date range]
- Readout to you: [date]

## Sign-off
- [ ] I confirm the decision above is what this study informs.
- [ ] I commit to attending the readout.
- [ ] I commit to acting on findings (per decision above) OR explaining why not.
```

### Recipe 8: Hypothesis examples (testable, falsifiable)

```markdown
# Hypothesis examples — what testable looks like

## Bad: "Users will love the new onboarding."
- Not falsifiable — "love" is unmeasurable
- Confirmation bias — wired to confirm

## Good: "≥4 of 5 moderated participants will complete the onboarding flow without researcher intervention."
- Falsifiable — clear threshold
- Operationalized — "intervention" defined as researcher having to give a hint

## Good: "Tree test directness % will improve from baseline 32% to ≥55% with the new IA."
- Comparable to prior data
- Specific metric + magnitude
```

### Recipe 9: Decision-without-research check

When the stakeholder doesn't actually need research, name it. Don't run vanity studies.

| Situation | Don't research — do this instead |
|---|---|
| Decision is already made (validation theater) | Skip; or run evaluative with willingness to find problems |
| Decision has no owner | Find the owner first |
| Budget for fix doesn't exist | Don't research yet — get fix budget committed first |
| Question is "would users like X?" (hypothetical) | Refuse hypothetical; run behavioral analytics + behavioral interview |
| Stakeholder wants 50 interviews "for confidence" | Push back — 5/round per Nielsen + iterate |

## Examples

### Example 1: Stakeholder says "let's run a survey on inbox"
**Goal:** Decide whether to scope a notification surface.

**Steps:**
1. Ask the decision (Recipe 1). Stakeholder confirms: "We'll scope notifications for Q3 IF we see inbox-overload signal."
2. Method matrix (Recipe 2): question is generative ("what's the pain shape") + behavioral ("when does it bite"). Survey is wrong; survey measures stated attitude. Pick JTBD interview (N=12) + Hotjar session replay friction pull.
3. Push plan to Notion (Recipe 4) + Dovetail project (Recipe 5).
4. Recruit via `recruit-user-interviews-respondent-dscout`.

**Result:** Right method, defensible scope, decision owner signed off.

### Example 2: Convert "let's test the prototype" into a real plan
**Goal:** Decide whether the onboarding redesign ships next sprint.

**Steps:**
1. Decision: "Ship if ≥4 of 5 moderated participants complete without intervention AND SUS ≥75."
2. Method: moderated usability with think-aloud (5 users) + unmoderated Maze (N=30) for SUS.
3. Hypothesis (Recipe 8): "≥4 of 5 will complete; SUS ≥75."
4. Sign-off 1-pager (Recipe 7) — stakeholder commits to act.
5. Recruit + run.

**Result:** Pre-committed decision criteria. No post-hoc reinterpretation.

## Edge cases / gotchas

- **No decision → no research.** If stakeholder can't name what they'll decide, the research is theater. Refuse or reframe.
- **Hypothesis ≠ prediction.** Hypothesis must be falsifiable AND would change the action. "We expect users to like the design" is not a hypothesis.
- **Method by habit ≠ method by question.** Push back if stakeholder demands a survey for an attitudinal/qual question.
- **Sample-size gold-plating.** "Let's recruit 30 for moderated" wastes budget. 5/round per Nielsen.
- **Plan in isolation.** Plans become stale if they don't link to Dovetail (raw evidence) + Notion (readout) + Linear (handoff). Tie all three at plan time.
- **No timeline → no plan.** Vague "this quarter" leaves recruiters waiting. Set dates.
- **Validation theater.** Research framed as "validate the design" is biased to confirm. Reframe as evaluative.
- **One research question is fine.** ≤5 is a ceiling, not a floor. One sharp question beats five vague ones.
- **Stakeholder commits to attend the readout.** If they don't, decision won't move — drop the study.

## Sources

- [NN/g — When to Use Which UX Research Method](https://www.nngroup.com/articles/which-ux-research-methods/)
- [NN/g — Why You Only Need to Test with 5 Users](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/)
- [Erika Hall — Just Enough Research](https://abookapart.com/products/just-enough-research)
- [Dovetail v3 API — projects](https://dovetail.com/help/api)
- [Notion API — databases](https://developers.notion.com/reference/database)
- [Teresa Torres — Continuous Discovery Habits](https://www.amazon.com/Continuous-Discovery-Habits-Discover-Products/dp/1736633309)
