<!--
Sources:
NN/g — AI UX Research — https://www.nngroup.com/articles/ai-ux-research/
Maze — AI prototype testing — https://maze.co/blog/ai-prototype-testing
Daniel Kahneman — Thinking, Fast and Slow (trust calibration)
-->
# AI Prototype Testing — Claude / ChatGPT / v0 / lovable — SKILL

Test AI-generated prototypes (Claude artifacts, v0.dev, lovable.dev, bolt.new, Figma Make) the same way you test designed prototypes — task-based usability + think-aloud. Add 2 AI-specific quality gates: (1) hallucination check (does the output match user intent?), (2) trust calibration (are users over-trusting the AI's confidence?).

## When to use

- Validating an AI-generated artifact / prototype before shipping.
- Testing a Claude-built workflow against real user tasks.
- Comparing AI-generated UX vs designed UX.
- Discovery on whether to ship an AI-driven feature.
- Verifying that AI output is trusted appropriately (not too much, not too little).

Trigger phrases: "test AI prototype", "Claude artifact test", "v0 deploy test", "lovable test", "AI hallucination check", "trust calibration", "AI UX test".

## Setup

```bash
# Maze (URL-based unmoderated test — works for any deploy URL)
curl -fsSL "https://api.maze.co/v1/teams/me" \
  -H "Authorization: Bearer $MAZE_API_KEY"

# For moderated: see moderated-1on1-usability-think-aloud skill
```

## Common recipes

### Recipe 1: AI prototype URLs (where to point Maze)

| Tool | Deploy URL pattern |
|---|---|
| Claude artifact | `https://claude.ai/public/artifacts/...` (publishable URL) |
| v0.dev | `https://v0-...vercel.app` |
| lovable.dev | `https://lovable.dev/projects/.../preview` |
| bolt.new | `https://bolt.new/~/...` (StackBlitz preview) |
| Figma Make | `https://www.figma.com/proto/...` (uses prototype URL) |
| Replit Agent | `https://...replit.app` |

Use the deployed URL in any URL-accepting test platform (Maze, Lyssna, UserTesting).

### Recipe 2: AI-specific quality gates

```markdown
# Beyond standard usability — 2 AI-specific gates

## Gate 1: Hallucination check
- Does the AI output match user intent?
- Are facts / numbers / claims real?
- Is the recommendation appropriate?
- **Test:** task-based with verifiable ground truth ("Find the Q3 revenue figure" → check against known data)

## Gate 2: Trust calibration
- Are users over-trusting the AI's confident answer?
- Are users under-trusting and ignoring good output?
- **Test:** include 1-2 intentionally wrong/uncertain AI outputs; observe user response
- Probe: "How confident are you in this answer?" / "Would you cite this in a report?"
```

### Recipe 3: Maze unmoderated AI test setup

```bash
curl -X POST "https://api.maze.co/v1/campaigns" \
  -H "Authorization: Bearer $MAZE_API_KEY" \
  -d '{
    "name": "Claude artifact: support-ticket triage tool",
    "type": "url_test",
    "url": "https://claude.ai/public/artifacts/abc123",
    "blocks": [
      {
        "type": "task",
        "instruction": "Use this tool to triage 5 support tickets by priority. Walk through each ticket.",
        "success_criteria": "All 5 tickets categorized",
        "time_limit_seconds": 600
      },
      {
        "type": "likert",
        "question": "How accurate did the AI categorization feel?",
        "scale": 7
      },
      {
        "type": "open_text",
        "question": "Were there any answers from the AI that you doubted? Which ones?"
      },
      {
        "type": "likert",
        "question": "Would you trust this AI tool to triage real tickets without checking each one?",
        "scale": 7
      },
      {
        "type": "open_text",
        "question": "What would make you trust this tool more?"
      },
      {
        "type": "sus_survey"
      }
    ],
    "sample_target": 25
  }'
```

### Recipe 4: Moderated AI prototype test protocol

```markdown
# Moderated AI prototype test (60 min)

## Pre-session warmup
- Frame: "We're testing an AI tool. Your job is to use it like you would your own work."
- "Be skeptical when you should be. Trust when it feels right."

## Tasks (3-5)
### Task 1 (easy — AI succeeds)
- Outcome-framed
- Ground truth exists (you know correct answer)
- Observe: do they verify? Do they accept blindly?

### Task 2 (hard — AI confidently wrong)
- Intentionally inject an error / hallucination
- Observe: do they catch it? Probe: "How confident does the AI seem? Are you?"

### Task 3 (boundary — AI uncertain)
- Question where AI should say "I don't know"
- If AI fabricates, observe user response
- Probe: "What would you do next?"

## Probes
- "What part of this answer would you double-check?"
- "How would you verify this if it mattered?"
- "What would change your level of trust here?"

## Post-test
- Trust calibration scale (1-7) on multiple dimensions
- SUS / UMUX-Lite
- Open: "When did you most / least trust the tool?"
```

### Recipe 5: Trust calibration matrix

```python
# Calculate trust calibration per participant
def trust_calibration(participant_responses):
    """
    For each task:
    - was AI correct? (ground truth)
    - did user trust? (post-task likert)

    Calibration buckets:
    - Correctly trusted (AI right, user trusted) — ✓
    - Correctly skeptical (AI wrong, user skeptical) — ✓
    - Over-trust (AI wrong, user trusted) — ⚠⚠
    - Under-trust (AI right, user skeptical) — ⚠
    """
    matrix = {"correctly_trusted": 0, "correctly_skeptical": 0,
              "over_trust": 0, "under_trust": 0}
    for task in participant_responses["tasks"]:
        ai_correct = task["ground_truth_match"]
        user_trusted = task["trust_score"] >= 5
        if ai_correct and user_trusted: matrix["correctly_trusted"] += 1
        elif not ai_correct and not user_trusted: matrix["correctly_skeptical"] += 1
        elif not ai_correct and user_trusted: matrix["over_trust"] += 1
        elif ai_correct and not user_trusted: matrix["under_trust"] += 1
    return matrix

# Over-trust = launch blocker; under-trust = adoption risk
```

### Recipe 6: Hallucination audit checklist

```markdown
# Hallucination audit (per AI output category)

## Factual hallucination
- [ ] Numbers / dates / names verifiable against ground truth?
- [ ] References / citations resolve to real sources?
- [ ] Code snippets compile + behave as described?

## Reasoning hallucination
- [ ] Logical chain from input to output sound?
- [ ] Conclusions follow from premises?
- [ ] No fabricated intermediate steps?

## Behavioral hallucination
- [ ] AI doesn't claim capabilities it lacks?
- [ ] AI confidently abstains when uncertain?
- [ ] AI corrects when user provides counter-evidence?

## Per-task scoring
- Hallucination rate = % of tasks with detectable error
- Goal: <5% for production-ready AI tools
```

### Recipe 7: Compare AI prototype to designed prototype

```markdown
# A vs B: AI prototype vs designed prototype

## Setup
- Same user task
- A: AI-generated tool (Claude artifact / v0 / lovable)
- B: human-designed Figma prototype with same scope
- Recruit balanced N (15-20 per arm)

## Metrics
- Task success rate
- SUS
- Trust calibration
- Time on task
- "Would you choose this over your current tool?"

## Comparison
- AI prototype often faster to build but lower trust
- Designed prototype higher trust but slower iteration
- Decision: hybrid (AI-generated with human-design polish)?
```

### Recipe 8: AI-specific post-test survey

```markdown
# Post-test survey block (paste into Maze / Lyssna)

## Trust dimensions (each 1-7)
1. How accurate did the AI seem?
2. How honest was the AI about what it didn't know?
3. Would you trust this AI with real work?
4. Would you trust this AI without checking its output?
5. How would you describe your own confidence using this AI?

## Hallucination probe
- Did anything the AI said seem wrong?
- (open text) Describe the moment you doubted the AI.

## Adoption probe
- Would you use this tool weekly?
- What would make you switch from your current way of doing this?

## Brand / trust transfer
- Does this experience change how you feel about [company brand]? (open)
```

### Recipe 9: AI prototype test report template

```markdown
# AI Prototype Test: [Tool Name]

**Date:** [YYYY-MM-DD] · **N=[X]** · **Tool:** [Claude artifact / v0 / lovable]
**Researcher:** [Name]

## TL;DR
- Task success: [X%] (vs designed-prototype baseline [Y%])
- Trust calibration: [% over-trust, % under-trust, % correct]
- Hallucination rate: [X%]
- Recommendation: [ship / iterate / kill]

## Method
- N=[X] unmoderated via Maze + N=[Y] moderated via Lookback
- Tasks with mixed difficulty (easy / hard / boundary)
- Trust calibration matrix per participant

## AI quality gate findings

### Hallucination
- Detected rate: [X%]
- Hallucination types: [factual / reasoning / behavioral]
- Top examples: [list with evidence]

### Trust calibration
- Over-trust cases: [X%] — RISK
- Under-trust cases: [X%] — adoption risk
- Verbatim: "[quote on when they over-trusted]" — P3

## Standard usability findings

### Task success: [X%]
- Easy tasks: [Y%]
- Hard tasks: [Z%]

### SUS: [X]
### Top friction points
1. [Issue + evidence]
2. ...

## Recommendations
- [Critical fix to prevent over-trust]
- [Trust signal design — e.g., confidence indicators, source citations]
- [Adoption support]
- [Decision: ship / iterate / kill]
```

### Recipe 10: Continuous AI-tool monitoring

```markdown
# Post-launch AI quality monitoring

## In-product feedback
- Sprig event-triggered: after AI output, "Was this answer accurate? (Y/N)"
- Track per-feature accuracy rate over time

## Trust signal events
- Track user verification behavior (do they click "see source"?)
- Track user override behavior (do they edit AI output?)

## Periodic audits
- Weekly: human-review 20 random AI outputs for hallucination
- Monthly: trust calibration survey
- Quarterly: full moderated round
```

## Examples

### Example 1: Test a Claude artifact for support triage
**Goal:** Validate AI-generated triage tool before shipping.

**Steps:**
1. Define ground-truth tickets (Recipe 6).
2. Set up Maze test (Recipe 3) pointing at Claude artifact URL.
3. Include trust calibration probes (Recipe 8).
4. Run moderated round (Recipe 4) for trust calibration depth.
5. Compute trust matrix (Recipe 5).
6. Report (Recipe 9).
7. Decision: ship if trust over-rate <10% + SUS >68 + hallucination <5%.

**Result:** Defensible ship decision with AI-specific quality gates.

### Example 2: Compare v0-generated UI vs designed UI
**Goal:** Decide whether v0 generation is good enough to ship.

**Steps:**
1. Build both versions of same flow.
2. A/B unmoderated test (Recipe 7).
3. Pull metrics + verbatim.
4. Decision: hybrid (v0 + designer polish) often wins.

**Result:** Workflow decision for design team.

## Edge cases / gotchas

- **Standard SUS only.** Misses AI-specific risks. Always add trust + hallucination gates.
- **Over-trust ignored.** Big launch risk. Always probe.
- **No ground truth.** Hallucination undetectable. Always include verifiable tasks.
- **Single difficulty level.** Need mix: easy / hard / boundary.
- **AI tool changes mid-test.** Lock version for test window; AI tools update silently.
- **Demo session bias.** AI tools perform well in demos; daily-use friction surfaces only in longitudinal.
- **Misleading task framing.** "Try this AI tool" → users on best behavior. Frame as real work.
- **No verification probe.** Users don't say "I'd verify this" unprompted. Probe.
- **AI output deterministic in test only.** Real-world stochasticity not captured.
- **Brand trust transfer.** AI failure on Claude artifact damages company brand. Track this.
- **Adoption risk under-trust.** Don't over-correct toward skepticism; balance trust signals.
- **Ethics: deceiving participants with planted errors.** Disclose in debrief.

## Sources

- [NN/g — AI UX Research](https://www.nngroup.com/articles/ai-ux-research/)
- [Maze — AI Prototype Testing](https://maze.co/blog/ai-prototype-testing)
- [NN/g — Generative AI Adoption](https://www.nngroup.com/articles/generative-ai-adoption/)
- [Daniel Kahneman — Thinking, Fast and Slow](https://www.amazon.com/Thinking-Fast-Slow-Daniel-Kahneman/dp/0374533555)
- [Anthropic — Claude API + artifacts](https://docs.anthropic.com)
- [v0.dev](https://v0.dev)
- [lovable.dev](https://lovable.dev)
- [bolt.new](https://bolt.new)
- [NN/g — User Trust in AI Systems](https://www.nngroup.com/articles/ai-trust-user-control/)
