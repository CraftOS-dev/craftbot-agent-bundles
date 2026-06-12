<!--
Source: https://www.satisfice.com/download/session-based-test-management · https://www.ministryoftesting.com/dojo/lessons/exploratory-testing
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Exploratory Testing — Charters + Session-Based (SBTM)

Session-Based Test Management (James Bach + Jon Bach, refined by Michael
Bolton) structures exploratory testing as time-boxed sessions around a
**charter** (mission statement) with **session sheets** capturing notes, bugs,
issues, and questions. The 2026 SOTA: charter in Notion/Markdown, 60-90 min
sessions, RapidReporter or Excalidraw mind-map artifacts, debrief in 5 min.

## When to use

- New feature lacks formal acceptance criteria; need to explore unknowns
- Investigating reported but unreproducible bug
- Pre-release "bug bash" coordination
- Risk discovery early in the sprint (before scripted tests)
- After a major refactor — what broke that we didn't think of?
- Trigger phrases: "exploratory testing", "bug bash", "charter", "session",
  "SBTM", "explore", "test idea generation"

Do NOT use for: scripted regression (use Playwright/pytest); contract
verification (use Pact); compliance evidence (use ISO 29119 plan).

## Setup

```bash
# Rapid Reporter — Bolton's note-taking tool (Windows; or web alternatives)
# https://testing.gershon.info/reporter/

# Or use Markdown templates committed to repo
mkdir -p docs/exploratory/charters docs/exploratory/sessions

# Excalidraw / draw.io for risk mind-maps
npm i -g @excalidraw/excalidraw
```

Auth: none. Notion sign-off via `notion-mcp`.

## Common recipes

### Recipe 1 — Charter template

`docs/exploratory/charters/<feature>-<idx>.md`:

```markdown
# Charter — <Feature> — <focus>

**Charter ID:** ET-<slug>-<NN>
**Date:** <YYYY-MM-DD>
**Tester:** <name>
**Time-box:** 90 min

## Mission
Explore <feature/area>
With <resources: build, env, data, tools>
To discover <information: risks, bugs, UX gaps, performance>

## Areas in scope
- <Area 1>
- <Area 2>

## Areas explicitly NOT in scope
- <Area>

## Heuristics / oracles to apply
- HICCUPPS (History, Image, Comparable products, Claims, User expectations,
  Product, Purpose, Statutes)
- CRUSSPIC STMPL (Capability, Reliability, Usability, Security, Scalability,
  Performance, Installability, Compatibility, Supportability, Testability,
  Maintainability, Portability, Localizability)
```

Example mission:
> Explore the new password-reset flow with a staging build (`v1.42-rc.3`) and
> Mailtrap inbox to discover token-handling weaknesses, UI surprises, and rate-
> limit gaps.

### Recipe 2 — Session sheet template

`docs/exploratory/sessions/<charter>-<date>.md`:

```markdown
# Session — ET-payments-01 — 2026-06-09

## Charter
Explore payment-method add/remove flow with seeded Stripe test cards to
discover validation, idempotency, and UI-state bugs.

## Session breakdown (T-B-S)
- Test design / execution: 55 min  (60%)
- Bug investigation: 25 min        (25%)
- Setup / interruption: 10 min     (10%)

## Notes
- N: tried adding card 4242 4242 4242 4242 — works
- N: switched to 4000 0000 0000 9995 (decline) — error message clear
- ? : what happens if I submit the form twice quickly?
  → tried double-click — second request 409 (good, idempotency works)
- B: BUG — empty CVV silently submits, returns 500 instead of 400
- B: BUG — back-button after successful add re-submits the form
- I : ISSUE — no aria-live announcement on add success

## Bugs
| ID | Severity | Repro | Notes |
|---|---|---|---|
| B1 | S2 | submit with empty CVV | 500 returned; should be 400 |
| B2 | S2 | back button after add | duplicate card added |

## Open questions
- Q: what's the rate limit per user?
- Q: does Stripe webhook retry idempotency-key collisions?

## Debrief targets
- 5 min PARSL review with QA peer
- File B1, B2 in Jira (S2/P1)
- Ask backend lead Q1, Q2 on Slack
```

### Recipe 3 — PARSL debrief checklist (Bach/Bolton)

After each session, a peer reviews via PARSL:

```markdown
## PARSL debrief — ET-payments-01
- **P** ast: what did the tester do?  → exercised add/remove on 4 card types
- **A** ctivity: what was the activity ratio? → 60/25/10 within target
- **R** esults: what bugs/issues? → 2 bugs, 1 a11y issue
- **S** etup: were there blockers? → 10 min on Mailtrap config
- **L** earning: what did we learn? → idempotency works, validation does not
```

### Recipe 4 — Tour-based test-idea generation

Pick a "tour" per session for fresh perspective:
- **Money tour** — every place money is shown / charged / refunded
- **Landmark tour** — major features hit in sequence
- **Antisocial tour** — input the rude / invalid / impossible
- **Garbage collector tour** — every error path, every cleanup
- **Configuration tour** — every settings toggle
- **Feature tour** — the happy path only
- **Stress tour** — high concurrency / size / repetition
- **Security tour** — XSS / SQLi / IDOR / authz bypass

Source: Whittaker's *Exploratory Software Testing*.

### Recipe 5 — HICCUPPS oracle in practice

```markdown
| Oracle | Question | Finding |
|---|---|---|
| H — History | Did this work before? | Yes — v1.41 worked; v1.42 broke |
| I — Image | Does it match brand standards? | OK |
| C — Comparable | What does Stripe Checkout do? | Stripe shows inline error; ours doesn't |
| C — Claims | What did the spec promise? | "Validates CVV before submit" — not implemented |
| U — User expectations | What would a user expect? | Inline error on blur |
| P — Product | Self-consistent? | No — login form validates inline; payment doesn't |
| P — Purpose | What's it for? | Accepting payment without surprise |
| S — Statutes | Legal / regulatory? | PCI says don't log card; check log scrubbing |
```

### Recipe 6 — Excalidraw mind-map of risks (visual brief)

```bash
npx @excalidraw/excalidraw
# Center: Feature
# Branches: HICCUPPS oracles → specific risks → specific tests
# Save as .excalidraw + .png in docs/exploratory/maps/
```

Commit alongside charter for traceability.

### Recipe 7 — Bug-bash playbook

```markdown
# Bug Bash — <date> — <feature>

## Pre-bash (T-1d)
- [ ] Charters drafted (one per pair)
- [ ] Test data seeded; URLs shared
- [ ] Loom of feature walkthrough
- [ ] Jira/Linear board with "BugBash-YYYYMMDD" tag

## Bash (60-90 min)
- 5 min — kickoff: charters, ground rules, NO duplicates
- 60-75 min — explore in pairs (tester + non-QA)
- 10 min — file bugs with bash tag

## Post-bash
- 15 min — group debrief: top 5 risks
- Triage in standup next day
- Bash retrospective: charter quality, coverage gaps, dupes
```

### Recipe 8 — Session metrics roll-up

```python
# scripts/session_metrics.py
from pathlib import Path
import re

bugs = []
for sheet in Path("docs/exploratory/sessions").glob("*.md"):
    for m in re.finditer(r"^\| (B\d+) \| (S[1-4]) \|", sheet.read_text(), re.M):
        bugs.append((sheet.stem, m.group(1), m.group(2)))

print(f"Total bugs: {len(bugs)}")
print(f"S1: {sum(1 for b in bugs if b[2]=='S1')}")
print(f"S2: {sum(1 for b in bugs if b[2]=='S2')}")
```

### Recipe 9 — Pair exploration (mob testing)

Two testers: one drives keyboard, one navigates ("I want to try ...").
Switch every 10-15 min. Captures more bugs than solo at the same time cost.

### Recipe 10 — Charters that drive scripted automation

When a session finds a regression-worthy bug:

```markdown
## Bug B2 → regression test
- **File:** `tests/regression/payments/double_submit.spec.ts`
- **Frame:** Playwright @smoke tag
- **Owner:** QA + backend pair
- **Linked PR:** #1284
```

Each session feeds the scripted suite — exploratory is the funnel.

## Examples

### Example 1: New feature exploration before scripted automation

**Goal:** Ship a payment-method UI with high confidence.

1. Write 3 charters: happy-path tour, money tour, antisocial tour.
2. Run 90-min sessions (one per charter); peer debrief 5 min each.
3. Capture bugs + questions in Jira with `et-payments` label.
4. Roll up findings; convert top 5 risks to scripted Playwright tests.
5. Sign-off: bugs S1/S2 fixed; scripted regression in CI.

### Example 2: Production incident — exploratory triage

**Goal:** Unreproducible bug "cart sometimes empties".

1. Charter: "Explore cart persistence across session events to discover loss
   conditions."
2. Tour list: login/logout, tab close, tab idle, multi-tab, network drop,
   localStorage clear, 24h idle.
3. Pair with backend dev for log access.
4. Session sheet captures repro: "logout then login within 30s drops cart".
5. File bug with exact repro + add Playwright regression next sprint.

## Edge cases / gotchas

- **Charters that read like specs** — "Verify X works" is a test case, not a
  charter. Charter says "Explore X to discover Y".
- **Sessions > 90 min** — fatigue, repeat-coverage. Stop. Debrief. Charter
  next session.
- **No debrief** — single biggest SBTM antipattern. 5 min PARSL with a peer
  doubles the value.
- **Session sheets in Slack threads** — vanish after 14 days on free tier.
  Commit to repo.
- **Counting bugs as the only metric** — SBTM also captures issues, questions,
  setup time, learnings. Optimize for learning over count.
- **Bug-bash without prep** — 20 people creating duplicate bugs for 60 min.
  Pre-bash charters + test-data prevent this.
- **Mistaking exploratory for "click around"** — SBTM is structured;
  unstructured wandering misses risk areas.
- **AI co-pilot exploration** — useful for idea generation; let it suggest
  tours, not write the session sheet for you.
- **Exploratory without time-box** — open-ended sessions never end; the
  90-min cap forces decisions.

## Sources

- [Session-Based Test Management — James Bach](https://www.satisfice.com/download/session-based-test-management)
- [SBTM Refined — Michael Bolton](https://www.satisfice.com/articles/sbtm.pdf)
- [Heuristic Test Strategy Model](https://www.satisfice.com/download/heuristic-test-strategy-model)
- [Exploratory Testing — Cem Kaner](http://www.kaner.com/pdfs/QAIExploring.pdf)
- [Whittaker — Exploratory Software Testing tours](https://blogs.msdn.microsoft.com/jamesw/)
- [Rapid Reporter — Shmuel Gershon](https://testing.gershon.info/reporter/)
- [Ministry of Testing — exploratory hub](https://www.ministryoftesting.com/dojo/lessons/exploratory-testing)
