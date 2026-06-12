<!--
Sources:
Bob Moesta — switch interview — https://www.demand-side.com/switch-interview
Tony Ulwick — outcome statements — https://jtbd.info/outcome-statements
Rob Fitzpatrick — The Mom Test — https://www.momtestbook.com
Christensen — Competing Against Luck
-->
# JTBD Interview Script + Execution — SKILL

Run a Jobs-to-be-Done study. Bob Moesta switch-interview timeline ("walk me through the day you switched"). Ulwick outcome statements (direction + unit + object + context). Mom Test rules from Rob Fitzpatrick (ask about life not opinion, specifics not generalities). 15-25 interviews on one job to reach saturation; themes stabilize at 12-15.

## When to use

- Generative research — discovering *why* customers switched / hired your product.
- Mapping push/pull/anxiety/habit forces to find adoption levers.
- Surfacing outcome statements that drive opportunity discovery.
- Pre-PRD discovery for a feature targeting a specific job.
- Onboarding new PM/designer to a user segment they don't know.

Trigger phrases: "JTBD interview", "switch interview", "why did they buy", "forces of progress", "outcome statements", "discovery interviews for X", "talk to customers about Y job".

## Setup

```bash
# Notion for guide + repo
curl -fsSL "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28"

# Dovetail for synthesis
curl -fsSL "https://dovetail.com/api/v1/me" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN"

# Calendly for scheduling
curl -fsSL "https://api.calendly.com/users/me" \
  -H "Authorization: Bearer $CALENDLY_API_TOKEN"

# Otter for transcription
curl -fsSL "https://otter.ai/api/v1/me" \
  -H "Authorization: Bearer $OTTER_API_KEY"
```

Auth: per-platform tokens (see other skills for setup).

## Common recipes

### Recipe 1: Switch interview guide (Moesta — paste-ready)

```markdown
# JTBD Switch Interview Guide — [Job Name]

**Researcher:** [Name] · **Duration:** 60 minutes
**Goal:** Surface the timeline + forces around switching to [your product / category]

## Pre-interview warmup (5 min)
- Role, company, what they do day-to-day on [domain]
- Set frame: "I want to understand the day you decided to try [X]. Walk me through it like a story."
- Recording consent

## The switch event (the anchor)
> "Walk me through the day you signed up / switched / bought. Where were you? What was happening?"

Probes:
- "What were you doing right before?"
- "What triggered the search?"
- "What time of day / week / month?"

## Before — push (current situation pushed them out)
> "What was wrong with what you had before? What broke that day?"

Probes:
- "What made it especially bad on that day?"
- "What had you been tolerating for weeks/months that suddenly felt unbearable?"

## Before — pull (new solution pulled them in)
> "What were you hoping the new thing would do for you?"

Probes:
- "What outcome were you imagining?"
- "What was the headline benefit in your head?"

## Considered set (alternatives)
> "What other options did you look at? What did you compare to?"

Probes:
- "Why did you reject those?"
- "What turned you off about each?"
- "What about staying with [old way] — why didn't you?"

## Anxiety (what almost stopped them)
> "What worried you about switching? What almost stopped you?"

Probes:
- "What was the cost in time / money / risk?"
- "Who had to approve this?"
- "What did you do to reduce the worry?"

## Habit (what was hard to give up)
> "What was hard to leave behind from the old way?"

Probes:
- "What was familiar / comfortable that you missed?"
- "How long did you stick with the old way before switching, even though you knew it wasn't working?"

## After — outcome (what changed)
> "Walk me through your first week with [X]. What changed? What didn't?"

Probes:
- "What was easier than expected? Harder?"
- "Did the outcome match what you hoped?"

## Calibration (counterfactual)
> "If we made [hypothetical change to X], how would your day be different?"
> "What's the one thing you wish [X] did that it doesn't?"

## Close
- "Anything I didn't ask that would be useful?"
- Thank + incentive logistics

## Mom Test guardrails (re-read before each call)
- ❌ Don't pitch
- ❌ Don't ask "would you" (hypothetical)
- ❌ Don't ask "do you think" (opinion)
- ✅ Ask about past actions, specific moments
- ✅ Silence after a question is fine; users fill the gap
- ✅ "Tell me more about that" / "Can you give me a specific example?"
```

### Recipe 2: Mom Test rewrite cheat sheet

| Bad (opinion / hypothetical) | Good (behavioral / specific) |
|---|---|
| "Do you think email is overwhelming?" | "How many emails did you get yesterday? How many did you read?" |
| "Would you pay for AI summaries?" | "Tell me about the last subscription you bought for work." |
| "Is the onboarding easy?" | "Walk me through what you did the first day you signed up." |
| "What features would you want?" | "What problem are you trying to solve that nothing solves today?" |
| "How important is X to you?" | "What's the last time X cost you time or money?" |

### Recipe 3: Forces of progress capture template

After each interview, fill in:

```markdown
# Participant: [PID] · [Role] · [Switched from → to]

## Push (what was wrong before)
- [specific event / pain — verbatim]

## Pull (what they hoped for)
- [outcome they imagined — verbatim]

## Anxiety (what almost stopped)
- [worry / risk — verbatim]

## Habit (what was hard to leave)
- [familiar / comfortable — verbatim]

## Adoption decision: (push + pull) vs (anxiety + habit)
- [which dominated? what tipped the balance?]
```

Adoption when **(push + pull) > (anxiety + habit)**.

### Recipe 4: Ulwick outcome statement format

`<direction> the <unit of measure> of <object> when <context>`

Direction: minimize / maximize / improve / reduce / increase
Unit: time / likelihood / number / amount / cost / ease
Object: the thing being measured
Context: the situation / when this matters

Examples:
- "minimize **the time** it takes **to find a customer's last reply** when **checking the inbox at start of day**"
- "maximize **the likelihood** of **converting a trial to paid** when **usage drops in week 2**"
- "minimize **the number** of **manual data-entry steps** when **importing leads from a CSV**"

### Recipe 5: Extract outcome statements from a transcript

```python
# Manual pass after transcription
def extract_outcomes(transcript):
    """
    Look for sentences containing pain/desire language:
    - "I wish..." / "I want..." / "I need..."
    - "...took me an hour" / "...waste time"
    - "If I could..." / "It would be amazing if..."

    Rephrase as: direction + unit + object + context
    """
    candidates = []
    triggers = ["I wish", "I want", "I need", "took me", "waste", "if I could", "would be amazing"]
    for line in transcript.split("\n"):
        if any(t in line.lower() for t in triggers):
            candidates.append(line)
    return candidates

# Then human-rephrase each into outcome statement
```

### Recipe 6: Push the guide + recruit + record pipeline

```bash
# 1. Notion: create interview guide from template
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28" \
  -d '{"parent":{"database_id":"<guides-db>"},"properties":{...}}'

# 2. Calendly: scheduling event type
curl -X POST "https://api.calendly.com/event_types" \
  -H "Authorization: Bearer $CALENDLY_API_TOKEN" \
  -d '{"name":"JTBD interview — Q3","duration":60,"kind":"solo"}'

# 3. Recruit via recruit-user-interviews-respondent-dscout skill

# 4. Zoom auto-record → Otter transcript → Dovetail upload
# (see moderated-1on1-usability-think-aloud Recipe 4 for the pipeline)
```

### Recipe 7: Dovetail tag taxonomy for JTBD

```markdown
# Suggested JTBD tag taxonomy

## Force tags (top-level)
- force/push
- force/pull
- force/anxiety
- force/habit

## Timeline tags
- timeline/first-thought
- timeline/passive-looking
- timeline/active-looking
- timeline/deciding
- timeline/first-use
- timeline/ongoing

## Outcome tags
- outcome/<verbatim job phrase>

## Persona tags
- persona/<segment>

## Affect tags
- affect/pain
- affect/delight
- affect/confusion
- affect/relief
```

### Recipe 8: Saturation check

```python
def saturation_check(interviews, themes_per_interview):
    """
    saturation when ≤2 net-new themes per interview for 2 consecutive interviews
    """
    new_per = []
    seen = set()
    for i, themes in enumerate(themes_per_interview):
        new = themes - seen
        new_per.append(len(new))
        seen |= set(themes)
    # Saturated if last 2 interviews added ≤2 new themes each
    return all(n <= 2 for n in new_per[-2:])

# Plan 15-25 interviews; expect saturation around 12-15
```

### Recipe 9: Post-interview tagging cadence

```markdown
# Tagging discipline

- **Within 24h of interview:** upload transcript to Dovetail; tag the most vivid 5-10 quotes
- **Within 1 week of all interviews:** complete tagging at quote level
- **After full tagging:** cluster tags into themes (≤7); rename to behavior-led labels
- **Synthesis output:** per-theme verbatim count + 2-3 quotes + recommended action
```

### Recipe 10: PRD handoff with JTBD evidence

```markdown
# PRD: [Feature] — Powered by JTBD research

## The job (Ulwick outcome statement)
"[direction] the [unit] of [object] when [context]"

Source: 11 of 15 JTBD interviews surfaced this outcome.

## Forces map (Moesta)
- **Push:** [what's wrong now — 8 of 15 mentions]
- **Pull:** [outcome desired — 10 of 15]
- **Anxiety:** [adoption blocker — 6 of 15]
- **Habit:** [inertia source — 5 of 15]

## Adoption equation
(push + pull) currently > (anxiety + habit) for [segment], but anxiety is high.
Feature should reduce anxiety by [specific design choice].

## Success metric tied to outcome
- Pre-feature: [baseline measurement of outcome]
- Post-feature: [target measurement]

## Evidence
- Dovetail project: [link]
- Verbatim highlights: [link]
- Research plan: [link]
```

## Examples

### Example 1: JTBD on solo founder onboarding
**Goal:** Discover what job solo founders hire your product for in week 1.

**Steps:**
1. Write guide (Recipe 1) tailored to onboarding switch event.
2. Recruit 15-20 via Respondent or User Interviews.
3. Run interviews; capture force notes (Recipe 3) per call.
4. Transcribe via Otter, upload to Dovetail (Recipe 6).
5. Tag with force + timeline + outcome taxonomy (Recipe 7).
6. Extract outcome statements (Recipe 4-5).
7. Check saturation (Recipe 8).
8. PRD handoff (Recipe 10).

**Result:** Outcome statement + forces map + designed-for-adoption brief.

### Example 2: Refine an Ulwick outcome from messy data
**Goal:** Convert "users say inbox is overwhelming" into a measurable outcome.

**Steps:**
1. Re-read 5 transcripts for sentences matching trigger phrases (Recipe 5).
2. Cluster verbatims about inbox pain.
3. Rephrase as outcome (Recipe 4): "minimize the time it takes to find priority emails when checking inbox at start of day."
4. Tie to a measurable: median time to first action on priority email.

**Result:** Operationalizable outcome ready for design + metric.

## Edge cases / gotchas

- **Pitching during interview.** PMs slip into pitching ~30% of way through. Re-read Mom Test before each call.
- **Asking opinion ("would you...").** Hypothetical answers are unreliable. Use behavioral past-tense always.
- **Skipping the switch anchor.** Without the day-of-switch anchor, the timeline collapses to "I just like it."
- **No probes.** Most gold comes from probes after first answer. Allow silence; "tell me more."
- **One-question saturation.** Adopting a "found it" mindset after 5 interviews = premature. Plan 15.
- **Conflating different jobs.** Same product can be hired for 2-3 distinct jobs. Tag carefully; don't merge.
- **Outcome statements that aren't measurable.** "Be more productive" = not an outcome. Direction + unit + object + context.
- **Validation theater.** JTBD framed as "validate the feature" = confirmation bias. JTBD is generative.
- **Skipping anxiety/habit.** Forces is 4-part. Most interviewers under-explore anxiety + habit and over-emphasize push + pull.
- **Recording without consent.** Always ask at start; document in transcript header.
- **Synthesizing from memory.** Tag at quote level in Dovetail; don't synthesize from gut.

## Sources

- [Bob Moesta — switch interview method](https://www.demand-side.com/switch-interview)
- [Tony Ulwick — Outcome Statements](https://jtbd.info/outcome-statements)
- [Rob Fitzpatrick — The Mom Test](https://www.momtestbook.com)
- [Christensen — Competing Against Luck](https://www.amazon.com/Competing-Against-Luck-Innovation-Customer/dp/0062435612)
- [Alan Klement — Replacing The User Story With The Job Story](https://jtbd.info/replacing-the-user-story-with-the-job-story-af7cdee10c27)
- [Rewired Group JTBD interview methodology](https://www.jobs-to-be-done.com/jobs-to-be-done-interview-1d4b18e3c2e0)
- [Dovetail v3 API](https://dovetail.com/help/api)
- [Lenny Rachitsky — ultimate guide to JTBD](https://www.lennysnewsletter.com/p/the-ultimate-guide-to-jtbd)
