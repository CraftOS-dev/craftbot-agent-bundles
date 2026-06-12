<!--
Sources:
JTBD official — https://jobs-to-be-done.com
Outcome-Driven Innovation (Ulwick) — https://strategyn.com/jobs-to-be-done
Forces of Progress (ReWired) — https://jobstobedone.org
-->
# Jobs-to-be-Done Framework — SKILL

JTBD is the discovery framework that anchors product thinking on the *job* a user hires the product to do — not features. This pack ships the Christensen + Ulwick variants, the outcome-statement format, the forces-of-progress model, and the practical templates the PM agent reaches for.

## When to use

- Discovery research: defining the JTBD before scoping a feature.
- Generating outcome statements that become success metrics.
- Mapping forces of progress for adoption decisions (push, pull, anxiety, habit).
- Writing the PRD's "Problem" and "Hypothesis" sections grounded in a job, not an output.
- Differentiating job vs solution vs feature when stakeholders conflate.

Trigger phrases: "what's the job", "JTBD analysis", "outcome statement", "forces of progress", "what's the user hiring this for", "job map".

## Setup

This skill is pure framework — no API. It outputs into Notion/PRD/Linear via the relevant skills.

```bash
# Notion: house the JTBD artifacts (job statements, outcomes, force maps)
mcp tool notion.viewer
```

## Common recipes

### Recipe 1: Job statement format (Christensen)

```
When [situation],
I want to [motivation],
so I can [expected outcome].
```

**Examples:**

```
When I'm checking email at 8am,
I want to know if any customers replied overnight,
so I can respond before they ping the support channel.
```

```
When I'm planning the week on Monday morning,
I want to see what's on track and what's behind,
so I can decide what to drop or re-scope.
```

### Recipe 2: Outcome statement (Ulwick / ODI)

```
<direction> the <unit of measure> of <object> when <context>
```

- **Direction:** minimize / maximize / eliminate
- **Unit of measure:** time, cost, likelihood, count, effort
- **Object:** what you're measuring on
- **Context:** when this matters

**Examples:**

```
minimize the time it takes to find a customer's last reply when checking the inbox at start of day

minimize the likelihood of missing a deadline when planning the week

maximize the chance of converting a trial to paid when usage drops in the second week
```

### Recipe 3: Job map (Ulwick's 8 steps)

```
1. Define     — clarify the goal
2. Locate     — gather inputs/resources
3. Prepare    — set up
4. Confirm    — verify readiness
5. Execute    — do the job
6. Monitor    — track progress
7. Modify     — adjust as needed
8. Conclude   — wrap up
```

For each step, ask: "What's the desired outcome here? What goes wrong? What slows the user down?"

### Recipe 4: Forces of progress map

```
Adoption happens when:  (Push + Pull) > (Anxiety + Habit)

Push          Pull
of current    of new

(unsatisfactory) (attractive)

       v             ^
       |             |
       +-------------+
            User
       +-------------+
       |             |
       v             ^

Anxiety       Habit
of new        of current
```

Fill the 4 quadrants for each customer segment based on interview data.

### Recipe 5: Notion JTBD template

```markdown
# JTBD: [Job Title]

## Job statement
When **[situation]**, I want to **[motivation]**, so I can **[outcome]**.

## Primary user (segment)
[Named segment — e.g., "Solo founders on the $29/mo plan"]

## Job map (8 steps)
1. Define: ...
2. Locate: ...
3. Prepare: ...
4. Confirm: ...
5. Execute: ...
6. Monitor: ...
7. Modify: ...
8. Conclude: ...

## Outcomes (Ulwick format)
1. <direction> the <unit> of <object> when <context>
2. ...
3. ...
(Aim for 8-15 outcomes per job)

## Forces of progress
- **Push** (current is broken): ...
- **Pull** (new is attractive): ...
- **Anxiety** (worry about new): ...
- **Habit** (inertia of current): ...

## Current alternatives
- [Tool/method 1 — what user does today]
- [Tool/method 2]
- "Nothing / live with it" (non-consumption — often the real competitor)

## Hypothesis
If we help users [accomplish job step X with outcome Y], then [metric] will improve.

## Linked research
- Dovetail project: [link]
- Interview round: [link]
```

### Recipe 6: Generate the JTBD doc into Notion

```bash
mcp tool notion.create_page \
  --parent '{"database_id":"<jtbd-db>"}' \
  --properties '{
    "Name":{"title":[{"text":{"content":"JTBD — Stay on top of customer replies"}}]},
    "Segment":{"select":{"name":"Solo founder"}},
    "Status":{"select":{"name":"Active"}}
  }' \
  --children '[
    {"type":"heading_1","heading_1":{"rich_text":[{"text":{"content":"Job statement"}}]}},
    {"type":"paragraph","paragraph":{"rich_text":[
      {"text":{"content":"When ","annotations":{"italic":true}}},
      {"text":{"content":"checking email at 8am","annotations":{"bold":true}}},
      {"text":{"content":", I want to ","annotations":{"italic":true}}},
      {"text":{"content":"know if any customers replied overnight","annotations":{"bold":true}}},
      {"text":{"content":", so I can ","annotations":{"italic":true}}},
      {"text":{"content":"respond before they ping support","annotations":{"bold":true}}}
    ]}}
  ]'
```

### Recipe 7: Outcome → metric mapping (Ulwick opportunity scoring)

```python
# Score each outcome by Importance × max(Importance - Satisfaction, 0)
def opportunity_score(importance_1_10, satisfaction_1_10):
    """High importance + low satisfaction = unmet opportunity (>= 12 is hot)."""
    return importance_1_10 + max(importance_1_10 - satisfaction_1_10, 0)

# Example: outcome "minimize time to find customer reply"
# Importance: 9 (high), Satisfaction: 3 (poor)
print(opportunity_score(9, 3))  # → 15 → big opportunity
```

Survey via Maze: 2 questions per outcome (importance + current satisfaction). Send to 100+ users.

### Recipe 8: Forces interview probes

For each interview, surface all 4 forces with these probes:

- **Push:** "What was happening right before you started looking?"
- **Pull:** "What about [solution] made you want to try it?"
- **Anxiety:** "What were you worried about when you switched?"
- **Habit:** "What were you doing instead? Why did you stick with it for so long?"

### Recipe 9: Job vs solution vs feature decoupling

Stakeholders will conflate. The agent's job: distinguish.

| Layer | What it is | Example |
|---|---|---|
| **Job** | Stable, durable need | "Stay on top of customer replies" |
| **Solution** | A way to accomplish the job | "A notifications center" |
| **Feature** | A specific implementation | "Slack-style threading" |

Push back when someone says "we need feature X" — start at the job, validate that.

### Recipe 10: Anti-job (when NOT to use a product)

Sometimes a user fires your product. Map the anti-job:

```
When **[situation]**, I do NOT want to **[use this product]**, because **[reason]**.

When I'm onboarding a new teammate, I do NOT want to use [product] yet, because the setup time is longer than the value they'll get this week.
```

Anti-jobs surface in churn and onboarding-drop interviews. They reveal the *cost of using* the product.

## Examples

### Example 1: Discovery doc for a candidate feature
**Goal:** Validate that a notifications feature solves a real job.

**Steps:**
1. Conduct 8 customer interviews (see `customer-interview-script-synthesis`).
2. Write the job statement (Recipe 1) — confirm or revise based on transcripts.
3. Build the job map (Recipe 3) — identify which step has the most friction.
4. Map forces of progress (Recipe 4) — confirm push + pull > anxiety + habit.
5. Generate outcome statements (Recipe 2) — pick 3-5 that map to measurable metrics.
6. Score opportunity (Recipe 7) via Maze survey — focus on outcomes scoring 12+.
7. Write the PRD problem section anchored in the validated job (cite outcomes).

**Result:** PRD that's grounded in a job, not a feature wish; success criteria flow directly from outcomes.

### Example 2: Differentiate the JTBD from a feature debate
**Goal:** Sales wants "Slack integration"; PM uses JTBD to interrogate.

**Steps:**
1. Ask sales: "What job is the customer trying to do?" — likely: "share customer context with my team without leaving Slack."
2. Generate alternative solutions (notifications via email, browser extension, Linear-style "view in app") — same job, different solutions.
3. Score each solution against feasibility + reach + impact.
4. Push back: "Slack integration is one solution; here are 3. Let's test which one the job actually wants."

**Result:** No premature feature commitment; the job is the durable spec.

## Edge cases / gotchas

- **Job is not a goal.** "Grow my business" is a goal, not a job. Job = specific, situated, actionable.
- **One job can have many solutions.** Don't lock to a solution before validating the job is real and high-value.
- **Outcome statements without measurement = vague.** Always pair an outcome with how you'd measure it (analytics event, survey).
- **Forces are estimates from interviews, not absolutes.** They direct where to push (lower anxiety, raise pull).
- **Functional vs emotional vs social jobs.** Most jobs have all three layers — e.g., "save time" (functional) + "feel competent" (emotional) + "look organized to teammates" (social). Don't ignore the latter two.
- **JTBD vs persona.** Personas describe who; JTBD describes what they're trying to accomplish. Same person can have multiple jobs.
- **Ulwick outcomes are exhaustive (8-15 per job)** — don't stop at 3-4. Comprehensive outcome lists reveal under-served areas.
- **Survey sample for opportunity scoring** needs ≥100 responses per outcome for stable scores.
- **The "milkshake" example** is a tool, not gospel — don't force every job into a "switching" narrative.
- **Christensen's framing** is broader (story-shaped); Ulwick's is more structured. Use whichever surfaces the right thing for the question at hand.

## Sources

- [Jobs-to-be-Done.com — Christensen](https://jobs-to-be-done.com)
- [Strategyn / Ulwick — Outcome-Driven Innovation](https://strategyn.com/jobs-to-be-done)
- [ReWired Group — Forces of progress](https://jobstobedone.org)
- [Clayton Christensen — Competing Against Luck](https://www.amazon.com/Competing-Against-Luck-Innovation-Customer/dp/0062435612)
- [Tony Ulwick — Jobs to be Done: Theory to Practice](https://www.amazon.com/Jobs-Be-Done-Theory-Practice/dp/0990576744)
- [Lenny — JTBD ultimate guide](https://www.lennysnewsletter.com/p/the-ultimate-guide-to-jtbd)
- [Bob Moesta interview with Lenny](https://www.lennyrachitsky.com/podcast/the-jobs-to-be-done-framework-bob-moesta)
