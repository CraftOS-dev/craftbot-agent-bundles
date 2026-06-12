<!--
Source: https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking
Companion playbook: role.md → "First-principles method"
Cross-check: gemini MCP for adversarial review
-->

# First-principles thinking — Claude Opus 4.7 extended thinking

Operationalizes the role.md first-principles playbook by using Claude Opus 4.7's `extended_thinking` capability for the 5-step decomposition, with Gemini as the adversarial cross-check.

## When to use this skill

- User explicitly requests first-principles analysis
- Conventional approaches have stalled
- Fundamental business model needs examination
- Teams need to challenge inherited processes
- Trigger phrases: "rethink", "from scratch", "challenge assumptions", "from first principles", "why does this even exist"
- Strategy formulation under high uncertainty
- Identifying load-bearing assumptions in a proposed plan

## When NOT to use

- Routine factual questions (overkill — use plain Sonar/Brave)
- When user wants conventional best-practice recommendations (this is the opposite of best practice; it questions them)
- For literature review (use `paper-search-mcp`)
- When data is plentiful and a model would answer better than reasoning

## The 5-step method (recap from role.md)

1. **Define precisely** — reframe problems away from solution language
2. **Identify assumptions** — catalog hidden beliefs (technology, process, business, users)
3. **Challenge each** — test validity with evidence and thought experiments
4. **Extract fundamentals** — isolate irreducible truths after assumptions fall away
5. **Rebuild from scratch** — construct solutions using only foundational facts

## Setup

Extended thinking is a built-in capability of Claude Opus 4.7. No setup beyond invoking the model with the right effort knob.

```
Effort levels:
- low    — ~1k thinking tokens, surface-level decomposition
- medium — ~5k thinking tokens, default for first-principles
- high   — ~20k thinking tokens, novel reasoning chains
- max    — ~64k thinking tokens, deepest analysis
```

For the agent itself (running on Opus 4.7), use the `extended_thinking` parameter in the system call.

## Common recipes

### Recipe 1 — The default loop (medium effort)

When the user asks a first-principles question, run this loop:

```
[medium effort extended thinking]

Step 1 — Define precisely
- What is being optimized?
- What is the boundary of the system?
- What outcomes count as success / failure?
- Reframe weak → strong problem statement (see role.md "Problem-statement reframing")

Step 2 — Identify assumptions
List ≥10 assumptions across these categories:
- Technology assumptions ("must use X stack")
- Process assumptions ("decisions go through Y workflow")
- Business assumptions ("customers will pay Z")
- User assumptions ("users want / behave like W")
- Regulatory assumptions ("we have to comply with V")
- Resource assumptions ("we have N people / $M budget")
- Time assumptions ("must launch by date Q")

Step 3 — Challenge each
For each assumption:
- Is it a constraint of physics / regulation, or just convention?
- Has it been tested? When? Has the world changed since?
- What would change if it were false?

Step 4 — Extract fundamentals
After surviving assumptions are tagged "validated" and others "dropped", what remains?
These irreducible truths are the foundation.

Step 5 — Rebuild from scratch
Construct ≥3 candidate solutions using ONLY the validated fundamentals.
At least one should be deliberately heterodox.
Compare against the conventional solution.
```

### Recipe 2 — High-effort for novel domains

Escalate to `high` or `max` effort when:

- No clear best-practice exists (novel tech, emerging market)
- The conventional solution has known catastrophic failure modes
- The decision is irreversible / multi-year
- Stakes are >$1M or strategic

```
[high effort extended thinking]
# Same 5 steps, but the model spends more time:
# - generating more candidate assumptions
# - running deeper thought experiments to challenge each
# - exploring further from conventional solutions in step 5
```

### Recipe 3 — Gemini adversarial cross-check (the pattern)

Run the 5-step decomposition with Claude, then run an adversarial review with Gemini:

```
PROMPT TO gemini-mcp:

You are a contrarian reviewer. Below is a first-principles analysis by another AI:

<paste Claude's output>

Identify:
1. Assumptions Claude classified as "validated" that you think are still suspect
2. Fundamentals Claude listed that you think rest on hidden assumptions
3. Solutions Claude proposed that fail in obvious scenarios
4. Solutions Claude didn't propose that are worth considering

Be merciless. Your job is to find weaknesses, not validate.
```

If Gemini finds load-bearing weaknesses, iterate. The two-model adversarial pattern catches blind spots a single chain-of-thought can miss.

### Recipe 4 — Problem-statement reframing

Before any decomposition, sharpen the question. From role.md:

| Weak | Strong |
|---|---|
| "We need a better onboarding flow" | "Users fail to reach their first value moment within 7 days" |
| "Our acquisition cost is too high" | "We're spending $X to acquire users with $Y LTV; the unit economics break at Z scale" |
| "We need to improve marketing" | "Aware users aren't converting; the conversion rate is X% vs. industry benchmark Y%" |

Pattern: shift from solution-language ("we need X") to **observable, measurable outcome-language**. A weak question elicits a conventional answer; a strong question elicits a first-principles answer.

### Recipe 5 — The 5D method (operational issues, not strategic)

For *operational* problems (not strategy), use 5D:

1. **Define** — clarify the problem
2. **Diagnose** — root cause analysis (5 whys, fishbone)
3. **Diverge** — multi-directional solution generation (use `brainstorming` skill)
4. **Decide** — structured evaluation criteria, weighted scoring
5. **Deploy** — implementation plan with owners + timeline

5D is faster than 5-step first-principles; use 5D when the problem has a known structure but a solution must be selected, and use 5-step when the problem structure itself needs examination.

### Recipe 6 — Capturing the output

The first-principles decomposition typically yields a deliverable like:

```
PROBLEM STATEMENT (reframed, strong)
   <one sentence>

ASSUMPTIONS AUDITED (N total)
   ✓ Validated (M):  <list with evidence>
   ✗ Dropped   (N-M): <list with reason>
   ⚠ Uncertain (K):  <list — flagged for further investigation>

FUNDAMENTALS
   <bullets of irreducible truths>

CANDIDATE SOLUTIONS
   1. <Conventional>     — pros/cons
   2. <Heterodox A>      — pros/cons
   3. <Heterodox B>      — pros/cons

RECOMMENDATION
   <pick + rationale + risks>

OPEN QUESTIONS
   <items flagged for further investigation>
```

## Edge cases

- **Effort knob diminishing returns:** `max` is rarely worth the latency cost over `high` for first-principles work. Use `max` only when the user explicitly asks for the deepest possible analysis.
- **Anchoring bias:** if the user asked the question with a preferred solution embedded ("should we use Kubernetes?"), the decomposition will anchor on that solution. Reframe to "What's the right deployment substrate?" before running.
- **Confirmation bias:** Claude's chain-of-thought can rationalize the conventional answer. The Gemini adversarial pass is the primary mitigation.
- **Knowing when to stop:** if step 4 yields fewer than 3 fundamentals, the decomposition is incomplete. If it yields more than 10, you haven't reduced enough.
- **Validation rigor:** "validated" assumptions still need evidence. The audit should cite a source per validation, not "common knowledge."
- **Practical infeasibility:** the rebuilt solution may be theoretically right but operationally infeasible. Always include a "transition path from current state" section.
- **Group-think mitigation:** for high-stakes, also run the same prompt with role-played personas (skeptical CFO, contrarian engineer, regulatory lawyer) and merge the critiques.

## Sources

- Claude extended thinking: https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking
- Anthropic best-practices for extended thinking: https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking#best-practices
- role.md → "First-principles method" (this bundle)
- VoltAgent first-principles-thinking: https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/10-research-analysis/first-principles-thinking.md

## Related skills

- `concise-planning` (default) — for the step-5 rebuild plan
- `brainstorming` (default) — for divergent generation in step 3 and 5D step 3
- `perplexity-deep-research` — when assumptions need external evidence
