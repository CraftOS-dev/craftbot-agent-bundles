<!--
Sources:
NN/g — 10 Usability Heuristics — https://www.nngroup.com/articles/ten-usability-heuristics/
NN/g — How to Conduct a Heuristic Evaluation — https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/
NN/g — Severity Ratings — https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/
-->
# Heuristic Evaluation — Nielsen's 10 — SKILL

Nielsen Norman 10 heuristics + severity scale 0-4. 3-5 evaluators independently rate, then merge. Pair with `cognitive-walkthrough` for novice-flow gaps. Output: prioritized issue list with severity × frequency × business impact + screenshot evidence.

## When to use

- Pre-launch expert review on a new feature.
- Quick triage of an existing interface for problem hot spots.
- Pre-research (cheaper) before recruiting users for moderated test.
- Standardized framework for design review across teams.

Trigger phrases: "heuristic eval", "Nielsen 10", "evaluate this interface", "expert review", "severity rate", "audit the UX", "10 heuristics".

## Setup

```bash
# Playwright MCP for live interface capture
# Figma MCP for prototype review

# Notion for the report
curl -fsSL "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28"
```

## Common recipes

### Recipe 1: Nielsen's 10 heuristics

```markdown
# Nielsen's 10 usability heuristics (memorize these)

1. **Visibility of system status** — Keep users informed; feedback within reasonable time
2. **Match between system and real world** — User language, not jargon; familiar concepts
3. **User control and freedom** — Undo, redo, clearly marked exits
4. **Consistency and standards** — Same words/actions mean same things; platform conventions
5. **Error prevention** — Better than error messages; confirm destructive actions
6. **Recognition rather than recall** — Make options visible; don't make users remember
7. **Flexibility and efficiency of use** — Shortcuts for experts; defaults for novices
8. **Aesthetic and minimalist design** — Every extra unit of info competes with relevant info
9. **Help users recognize, diagnose, recover from errors** — Plain language, suggest fix
10. **Help and documentation** — Easy to search, focused on user task, concrete steps
```

### Recipe 2: Severity scale (Nielsen 0-4)

```markdown
# Severity ratings

- **0 — Not a problem at all** (false flag)
- **1 — Cosmetic problem only** — fix if time
- **2 — Minor usability problem** — low priority
- **3 — Major usability problem** — fix high priority
- **4 — Usability catastrophe** — must fix before release; blocks task

## Prioritization
priority = severity × frequency × business_impact
- Severity from rating
- Frequency = % of users likely to encounter
- Business impact = revenue / churn / brand impact (1-5)
```

### Recipe 3: Evaluation procedure (per evaluator)

```markdown
# Procedure (3-5 evaluators independently)

## 1. First walkthrough — absorb (15-30 min)
- No judging yet — get the flow
- Note primary user goal
- Take screenshots of every screen

## 2. Second walkthrough — evaluate (60-90 min)
- For each screen + flow:
  - Walk through each user step
  - Check against each of 10 heuristics
  - Note violations + severity
  - Take screenshot + annotate

## 3. Independent report
- Capture issue with:
  - Screenshot + screen URL
  - Heuristic violated (1-10)
  - Severity (0-4)
  - User impact description
  - Recommended fix

## 4. Reconciliation meeting (60 min)
- Each evaluator presents their list
- Merge duplicates
- Reconcile severity disagreements
- Output: single combined issue list
```

### Recipe 4: Live interface capture via Playwright

```bash
# Use playwright-mcp to capture screens for each step
# Pseudo MCP usage:
mcp tool playwright.navigate --url "https://app.example.com/onboarding"
mcp tool playwright.screenshot --output "screen1.png"
mcp tool playwright.click --selector "button.next"
mcp tool playwright.screenshot --output "screen2.png"
# Repeat for each step

# Capture interactions + flag broken states
mcp tool playwright.console_logs > console.log
```

### Recipe 5: Figma prototype evaluation

```bash
# Use figma-mcp to access prototype frames
mcp tool figma.get_frames --file "https://www.figma.com/proto/abc123"
# Returns each frame with components + design tokens
# Evaluate against heuristics; comment on frames programmatically:
mcp tool figma.add_comment --frame "Onboarding/Step1" --text "Heuristic 6: button label 'Continue' doesn't recall action. Consider 'Set up workspace →'"
```

### Recipe 6: Issue capture template (per issue)

```markdown
## Issue #[N] — [Title]

**Severity:** [4 — Catastrophe / 3 — Major / 2 — Minor / 1 — Cosmetic]
**Heuristic violated:** #[1-10 — name]
**Screen:** [URL or Figma frame link]
**Frequency:** [% likely to encounter — high / medium / low]
**Business impact:** [revenue / churn / brand — 1-5]

### Description
[What's wrong, in 1-2 sentences]

### User impact
[How users get blocked / confused]

### Evidence
![screenshot with annotation](path/to/screenshot.png)

### Recommendation
[Specific fix]

### Priority score
[severity × frequency × business_impact]
```

### Recipe 7: Standard report template

```markdown
# Heuristic Evaluation: [Interface Name]

**Evaluators:** [Names — 3 to 5]
**Date:** [YYYY-MM-DD]
**Scope:** [Pages / flows reviewed]

## Methodology
- Nielsen's 10 heuristics + severity 0-4
- N evaluators, independent then reconciled
- [N] screens reviewed; [N] interactions captured via Playwright

## Severity distribution
| Severity | Count |
|---|---|
| 4 Catastrophe | 2 |
| 3 Major | 8 |
| 2 Minor | 15 |
| 1 Cosmetic | 22 |

## Heuristic distribution
| Heuristic | Violations |
|---|---|
| H1 Status | 3 |
| H2 Real world | 5 |
| H3 Control | 2 |
| ... | |

## Top fix priorities (by severity × frequency × business impact)

### Priority 1: [Issue title] — Severity 4
[Full Recipe 6 block]

### Priority 2: ...

## Out-of-scope observations
[UX improvements that aren't heuristic violations — feature gaps, ideas]

## Appendix
- All issues (CSV / Notion table)
- Screenshots library
- Playwright session traces
```

### Recipe 8: Heuristic vs cognitive-walkthrough decision

| Method | Best for | Output |
|---|---|---|
| **Heuristic evaluation** | Expert review of interface against 10 principles | Severity-rated issue list |
| **Cognitive walkthrough** | Novice-user flow gaps | Friction map per step |
| **Use together** | Pre-launch check | Both surface complementary issues |

### Recipe 9: Single-evaluator caveats

```markdown
# Single-evaluator warning

If only 1 evaluator:
- ✅ OK for quick triage / sanity check
- ⚠ Will catch ~30% of issues (per Nielsen — solo finds ~35%)
- ⚠ Severity ratings less calibrated
- ⚠ Always disclose "N=1 evaluator" in report header

# Recommended: 3-5 evaluators
- 3 evaluators catch ~60% of issues
- 5 evaluators catch ~75% of issues
- Beyond 5: diminishing returns
```

### Recipe 10: Calibration session (before evaluation)

```markdown
# Calibration session (30 min — for evaluator team)

## Goal
Align on severity definitions + heuristic interpretation before independent eval.

## Agenda
1. Review the 10 heuristics aloud (5 min)
2. Review severity scale + examples (5 min)
3. Walk through 1 sample issue per evaluator + rate it together (15 min)
4. Discuss disagreements; refine shared understanding (5 min)

## Output
- Shared severity calibration
- Reduced reconciliation effort
- Higher inter-rater agreement
```

## Examples

### Example 1: Pre-launch heuristic eval on onboarding flow
**Goal:** Catch major UX issues before recruit-based testing.

**Steps:**
1. 3 evaluators (Recipe 9 rule).
2. Calibration session (Recipe 10).
3. Each does independent eval (Recipe 3) with Playwright capture (Recipe 4).
4. Capture issues per template (Recipe 6).
5. Reconciliation meeting; merge to single list.
6. Report (Recipe 7).
7. Triage in Linear; fix critical issues before moderated round.

**Result:** Issue list prioritized by severity × frequency × business impact.

### Example 2: Solo evaluation on a competitor product
**Goal:** Quick UX comparison teardown.

**Steps:**
1. Single evaluator with Recipe 9 caveat in header.
2. Walk through critical flows.
3. Note issues at quote level.
4. Output: lighter-weight report, internally framed as "expert opinion N=1."

**Result:** Useful for internal comparison, not actionable on its own.

## Edge cases / gotchas

- **Single evaluator without caveat.** Disclose; don't pass off as full eval.
- **No severity calibration.** Different evaluators rate same issue 2 vs 4. Run calibration session.
- **Issues without screenshots.** Becomes opinion + hard to act on. Always capture evidence.
- **Heuristic violation = severity 4.** Not automatic. Severity is impact, not principle.
- **Ignoring out-of-scope ideas.** Capture them in appendix — they often become next research's input.
- **Evaluating without user goal in mind.** Walk through with a user task; not abstract principle check.
- **Reconciliation by averaging.** Discuss + agree on rationale, don't average.
- **Skipping reconciliation.** Each evaluator's list alone misses where they disagree.
- **Cosmetic-heavy report.** Severity 1 issues drown out severity 3-4. Sort by priority, not order.
- **Pairing heuristic eval with same-week user research = good.** Heuristic catches obvious; user research catches non-obvious.
- **Aesthetic heuristic (#8) misused.** Don't use it as cover for personal taste. Anchor in "extra info competes with relevant info."

## Sources

- [NN/g — 10 Usability Heuristics for User Interface Design](https://www.nngroup.com/articles/ten-usability-heuristics/)
- [NN/g — How to Conduct a Heuristic Evaluation](https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/)
- [NN/g — How to Rate the Severity of Usability Problems](https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/)
- [Jakob Nielsen — Severity ratings](https://www.nngroup.com/articles/severity-ratings/)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Figma Dev Mode MCP](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Dev-Mode-MCP-Server)
