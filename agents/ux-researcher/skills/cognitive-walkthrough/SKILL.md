<!--
Sources:
Wharton, Lewis, Polson — Cognitive Walkthrough
NN/g — Cognitive Walkthrough — https://www.nngroup.com/articles/cognitive-walkthrough/
Wikipedia — https://en.wikipedia.org/wiki/Cognitive_walkthrough
-->
# Cognitive Walkthrough — SKILL

Wharton-Lewis-Polson 4-question method. For each user step, ask: (1) Will user try right effect? (2) Will they notice the correct action? (3) Will they associate action with effect? (4) Will they see progress? "No" = friction. Specifically for novice users + first-time flows. Solo or 1-3 evaluators.

## When to use

- Pre-launch evaluation of a flow targeting novice / first-time users.
- Triage for high-drop-off funnels (pair with analytics).
- Onboarding redesign before recruit-based testing.
- Pairing with heuristic eval for complementary coverage.

Trigger phrases: "cognitive walkthrough", "walk through this flow", "novice user friction", "first-time experience", "4-question method", "walkthrough this onboarding".

## Setup

```bash
# Playwright MCP for live flow capture
# Figma MCP for prototype walkthrough
# Notion for the walkthrough doc
```

## Common recipes

### Recipe 1: The 4 Wharton-Lewis-Polson questions

```markdown
# Per user step, ask:

## Q1: Will the user try to produce the right effect?
- Does the user know this step is needed?
- Is the goal clear from context?
- (Failure: user doesn't know they need to do this step)

## Q2: Will the user notice the correct action is available?
- Is the right control visible?
- Is it discoverable?
- (Failure: button hidden / control ambiguous)

## Q3: Will the user associate the correct action with the effect they want?
- Does the label match the user's intent?
- Does the control affordance signal what it does?
- (Failure: label says "Save" but user wants "Submit"; meaning mismatch)

## Q4: If the correct action is performed, will the user see progress?
- Is feedback clear?
- Does the user know they're on the right path?
- (Failure: success silent; user repeats or backs out)

# "No" to any = friction point.
```

### Recipe 2: Per-step matrix template

```markdown
# Step [N]: [Action description]

| Q | Question | Answer | Reason |
|---|---|---|---|
| Q1 | Will user try right effect? | Y/N | [reason] |
| Q2 | Will they notice correct action? | Y/N | [reason] |
| Q3 | Will they associate action with effect? | Y/N | [reason] |
| Q4 | Will they see progress? | Y/N | [reason] |

**Friction risk:** [low / medium / high]
**Failed questions:** [list]
**Recommendation:** [specific fix per failed Q]
```

### Recipe 3: Walkthrough procedure (60-90 min)

```markdown
# Procedure (1-3 evaluators)

## 1. Define user + task (5 min)
- "Novice user in [persona segment]"
- "Goal: [outcome they want]"
- Print + tape persona to wall (literally — keeps focus on novice)

## 2. List steps (10 min)
- Each user step in the ideal path (5-15 steps)
- Each step = one user action
- Don't skip "obvious" steps (e.g., "click submit") — those fail too

## 3. Walk through each step (45-60 min)
- For each step, run the 4 questions
- Capture answer + reason
- Take screenshot

## 4. Triage friction (10 min)
- Sort steps by # failed questions
- Sort by which Q failed (Q2 visibility issues vs Q3 label issues)
- Top 3-5 fixes

## 5. Write up (15 min)
- Walkthrough doc per Recipe 5
```

### Recipe 4: Where each question failure points to a fix

| Failed Q | Pattern | Fix |
|---|---|---|
| Q1 (no try) | User doesn't know step needed | Add context / instructions / wizard |
| Q2 (no notice) | Control hidden / camouflaged | Visual hierarchy / contrast / position |
| Q3 (no associate) | Label / icon wrong | Rename / change icon / add tooltip |
| Q4 (no progress) | Feedback missing | Loading state / success message / step indicator |

### Recipe 5: Walkthrough report template

```markdown
# Cognitive Walkthrough: [Flow Name]

**Evaluators:** [Names — 1 to 3]
**Date:** [YYYY-MM-DD]
**Target user:** [novice / power user / specific persona]
**Target task:** [outcome]

## Flow summary
[1-2 sentences — what the user is trying to do, start to finish]

## Steps + 4-question matrix

### Step 1: [Action]
- Q1 (right effect?): Y — "Welcome screen shows clear next step"
- Q2 (correct action visible?): Y — "Primary button center, high contrast"
- Q3 (action ↔ effect match?): Y — "Label 'Set up workspace' matches their goal"
- Q4 (sees progress?): Y — "Step 1 of 5 indicator"
- **Friction risk:** low
- **Failed Qs:** none

### Step 2: [Action]
- Q1: Y
- Q2: N — "Team-member field hidden in advanced settings"
- Q3: N — "Label 'Members' could mean members of what?"
- Q4: Y
- **Friction risk:** high
- **Failed Qs:** Q2, Q3
- **Recommendation:** Surface team-member field directly in main flow; rename to "Add teammates"

### Step 3: ...

## Friction map (visual)

| Step | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| 1 | ✓ | ✓ | ✓ | ✓ |
| 2 | ✓ | ✗ | ✗ | ✓ |
| 3 | ✓ | ✓ | ✓ | ✗ |
| 4 | ✓ | ✓ | ✓ | ✓ |
| 5 | ✗ | ✓ | ✓ | ✓ |

## Top fix priorities
1. **Step 2 — Q2 + Q3:** Surface + rename team field
2. **Step 3 — Q4:** Add post-import success confirmation
3. **Step 5 — Q1:** Add context for why upgrade matters here

## Recommended next steps
- [Fix high-risk steps]
- [Re-walkthrough after fixes]
- [Schedule moderated test on remaining concerns]
```

### Recipe 6: Use Playwright to capture each step

```bash
# Pseudo-MCP — walk through flow capturing screen per step
mcp tool playwright.navigate --url "https://app.example.com/onboarding"
mcp tool playwright.screenshot --output "step1.png"

# Simulate novice action
mcp tool playwright.click --selector "[data-testid='start-cta']"
mcp tool playwright.screenshot --output "step2.png"

# Repeat per step
# Note: screen-by-screen capture acts as the walkthrough record
```

### Recipe 7: Combine with heuristic evaluation

```markdown
# Pairing strategy

## Cognitive walkthrough = novice perspective on flow
## Heuristic eval = expert principles check on interface

## Together:
- Run heuristic eval first (catches obvious interface issues)
- Fix the worst
- Then cognitive walkthrough (catches flow-specific friction)
- Fix those
- Then moderated usability with 5 real users (catches what evaluators missed)
```

### Recipe 8: Persona-anchored walkthrough

```markdown
# Persona anchor — tape to wall during walkthrough

**Target persona: First-time solo founder**
- Has never used a CRM
- Last used Outlook in 2019
- Knows email, knows web forms
- Doesn't know what "pipeline" or "lead score" mean
- Is mildly nervous about messing up

# When asking each Q, ask: "Would THIS person..."
# Keeps evaluator from thinking like a power user
```

### Recipe 9: When to skip walkthrough + go to user testing

| Situation | Action |
|---|---|
| You have budget + time + recruit | Skip walkthrough, run 5 moderated users |
| You don't have prototype yet | Walkthrough on paper / wireframe |
| You need rapid pre-launch sanity check | Walkthrough (1 evaluator, 90 min) |
| You suspect novice friction but unsure | Walkthrough first, then targeted moderated |

### Recipe 10: Walkthrough as a teaching tool

```markdown
# Run walkthrough WITH the team that built the flow

## Goal: empathy + alignment
- 60-min session with designer + PM + 1-2 engineers
- Walk through flow as a "novice founder"
- Use 4 questions live
- Designer sees their own design through novice eyes
- Engineer sees where defensive code is needed
- PM sees real friction, not abstract bugs

## Output
- Team understanding shared
- Issues triaged + assigned
- Design + dev follow-up scheduled
```

## Examples

### Example 1: Pre-launch walkthrough on rewritten onboarding
**Goal:** Catch novice friction before moderated round.

**Steps:**
1. Define persona + task (Recipe 3).
2. List 8 steps in ideal path.
3. Walk through each (Recipe 1-2).
4. Capture screens via Playwright (Recipe 6).
5. Write up report (Recipe 5).
6. Triage top 3 friction points → fix sprint.
7. Re-walkthrough after fixes.
8. Then moderated round.

**Result:** Higher-quality moderated round (avoids burning user time on obvious flow issues).

### Example 2: Walkthrough as design review
**Goal:** Get team alignment on onboarding direction.

**Steps:**
1. 60-min team session (Recipe 10).
2. Designer + PM + engineers in the room.
3. Walk through novice-persona scenario.
4. Capture issues in shared doc.
5. Triage + assign.

**Result:** Shared understanding + clear fix backlog.

## Edge cases / gotchas

- **Expert mindset during walkthrough.** Tape persona to wall; force novice perspective.
- **Skipping "obvious" steps.** Click submit fails too. Walk every step.
- **Q4 missing.** Most-skipped question. Always check progress feedback.
- **Walkthrough on stable design only.** If design is still volatile, lower-fidelity sketch walkthrough first.
- **Mistaking walkthrough for user research.** Walkthrough = expert method. Not a substitute for real users.
- **Single-evaluator unchecked.** Caveat in report header.
- **Walkthrough on completed product without users.** Better than nothing, but limited.
- **No screenshots.** Becomes opinion. Always capture evidence per step.
- **Friction triage as "all important."** Sort by severity + Q-failed pattern.
- **Rewalkthrough after fixes skipped.** Original flow may have shifted; verify.
- **Mixing walkthrough types.** Stay with novice persona for one pass; do power-user pass separately if needed.

## Sources

- [NN/g — Cognitive Walkthrough](https://www.nngroup.com/articles/cognitive-walkthrough/)
- [Wharton, Lewis, Polson — Cognitive Walkthrough Method](https://en.wikipedia.org/wiki/Cognitive_walkthrough)
- [Caroline Jarrett — Cognitive walkthrough simplified](https://www.usertesting.com/blog/cognitive-walkthrough)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Figma Dev Mode MCP](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Dev-Mode-MCP-Server)
- [Polson, Lewis, Rieman, Wharton — Cognitive walkthroughs: a method for theory-based evaluation](https://dl.acm.org/doi/10.1006/imms.1992.1075)
