<!--
Sources:
NN/g — Democratize UX Research — https://www.nngroup.com/articles/democratize-ux-research/
User Interviews — Democratizing User Research — https://www.userinterviews.com/blog/democratizing-user-research
ResearchOps Community — https://researchops.community
-->
# Research Democratization + Training — SKILL

Train PMs / designers / engineers on the "research basics that don't suck" curriculum: Mom Test interview rules, participant ethics, screener basics, when to call in a researcher. Output: Notion training wiki + cheat sheets + pptx kickoff deck + office hours cadence.

## When to use

- Onboarding new PM / designer to your research practice.
- Building a "PMs can run discovery, researchers run rigor" model.
- Scaling research influence beyond a small research team.
- Establishing escalation matrix (when DIY, when call researcher).

Trigger phrases: "train team on research", "democratize research", "research basics for PMs", "office hours", "research wiki", "team training".

## Setup

```bash
# Notion for wiki + training pages
curl -fsSL "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28"

# Gmail for office-hours invites
curl -fsSL "https://gmail.googleapis.com/gmail/v1/users/me/profile" \
  -H "Authorization: Bearer $GMAIL_ACCESS_TOKEN"

# pptx skill for kickoff deck
```

## Common recipes

### Recipe 1: Research democratization curriculum

```markdown
# "Research basics that don't suck" curriculum

## Module 1: Why research (15 min)
- The decision research informs
- Behavior beats stated intent
- 5 users surface 85% of issues

## Module 2: Mom Test rules (30 min)
- Ask about life, not opinion
- Ask about specifics, not generalities
- Avoid leading questions
- Avoid hypotheticals
- Silence is fine
- 30-min role-play exercise

## Module 3: Screener basics (30 min)
- 1-3 must-have behavioral criteria
- Anti-screens (pros, panel pollution)
- Right incentive ($50/$100/$200 by segment)
- Recording consent

## Module 4: Running an interview (45 min)
- Pre-session warmup
- Outcome-framed tasks (think-aloud)
- Probing without leading
- Debrief
- Live demo + role-play

## Module 5: Synthesis without burnout (30 min)
- Tag at quote level, not memory
- Cluster tags into themes
- Theme = ≥3 participants mentioned
- Always cite source

## Module 6: When to call in a researcher (15 min)
- The escalation matrix (Recipe 4)
- Office hours
- Self-serve resources

## Module 7: Ethics (15 min)
- Consent for recording
- GDPR / CCPA
- Right to withdraw
- Honorarium fairness
```

### Recipe 2: Notion wiki structure

```markdown
# Research Wiki (Notion) — structure

## Front page
- "Start here" — 1-min orientation
- Office hours signup
- Active studies
- Recent insights

## Self-serve playbooks
- "Run a customer interview" (10-min playbook + checklist)
- "Run an unmoderated test" (Maze setup)
- "Run a usability test" (5-user Lookback / Zoom)
- "Run a survey" (Sprig / Typeform recipes)

## Templates (downloadable)
- Screener template
- Interview guide template
- Research plan template
- Readout template

## Cheat sheets (1-pagers)
- Mom Test rules
- Sample size cheat sheet
- Anti-screen patterns
- Heuristic eval — Nielsen 10
- Severity scale 0-4

## Decision aids
- "Which method should I use?" — NN/g matrix
- "Which platform should I recruit on?"
- Sample size cheat sheet

## Research repository
- Personas
- Journey maps
- Insights library (link to Dovetail)
```

### Recipe 3: 1-page cheat sheet templates

```markdown
# Cheat Sheet: Mom Test rules

## ✅ Do
- Ask about past actions: "Walk me through the last time you..."
- Ask about specifics: "What did you do yesterday?"
- Use silence to elicit more

## ❌ Don't
- "Would you use X?" (hypothetical)
- "Do you think Y is good?" (opinion)
- "Was that easy?" (leading)

## Quick rephrase test
| Bad | Good |
|---|---|
| "Would you pay?" | "Tell me about the last subscription you bought" |
| "Do you like X?" | "Walk me through how you used X yesterday" |
| "Is the onboarding easy?" | "What did you do the first day?" |

# Sources
- The Mom Test by Rob Fitzpatrick
- See research wiki for full playbook
```

### Recipe 4: Escalation matrix

```markdown
# When to DIY vs call a researcher

| Situation | DIY OK? | Researcher? |
|---|---|---|
| Test a Figma prototype with 5 users | ✅ DIY (use moderated playbook) | If stakes high |
| Set up Maze unmoderated test | ✅ DIY | If stakes high |
| Quick survey on a feature | ✅ DIY (use Typeform) | — |
| 5-second test on landing page | ✅ DIY (Lyssna) | — |
| JTBD interviews on new segment | ⚠ Pair w/ researcher | ✅ Researcher leads |
| Accessibility research | ❌ Call researcher | ✅ Researcher leads |
| Contextual inquiry / field study | ❌ Call researcher | ✅ Researcher leads |
| Tree test on IA redesign | ⚠ Pair w/ researcher | ✅ Researcher reviews |
| New research repository setup | ❌ Call researcher | ✅ Researcher leads |
| Synthesis from >10 interviews | ❌ Call researcher | ✅ Researcher leads |
| Persona authoring | ❌ Call researcher | ✅ Researcher leads |
| Quarterly NPS thematic analysis | ⚠ Pair w/ researcher | ✅ Researcher leads |
```

### Recipe 5: Build kickoff deck (pptx)

```python
# Use pptx skill to generate the kickoff deck
slides = [
    {"title": "Research that doesn't suck — orientation",
     "body": "Why we research; What you can DIY; When to call us"},
    {"title": "The decision", "body": "Every study has a decision it informs"},
    {"title": "Behavior beats stated intent", "body": "Mom Test rules"},
    {"title": "Sample size", "body": "5 users = 85% of issues"},
    {"title": "Self-serve playbooks", "body": "Wiki tour"},
    {"title": "Office hours", "body": "Weekly Tue 2-3pm; book via [link]"},
    {"title": "Escalation matrix", "body": "When to DIY vs call us"},
    {"title": "Live Q&A", "body": ""}
]

# Push to pptx skill
```

### Recipe 6: Office hours cadence

```markdown
# Office hours model

## Cadence
- Weekly 60-min block, Tuesday 2-3pm
- 4 × 15-min consult slots per session
- Booking via Calendly

## What we cover
- "I'm planning research for X — review my plan"
- "I have these 8 interviews, how do I synthesize?"
- "Help me write a screener"
- "Pick the right method for my question"

## Pre-read required
- Submit: question + decision + draft plan/screener/etc.
- Researcher reviews ahead
- 15 min = consult, not blank-page work

## Slack channel
- #user-research-help
- Async questions answered within 1 business day
- Office hours signup pinned
```

### Recipe 7: Self-serve playbook template

```markdown
# Playbook: "Run a 5-user usability test"

**Audience:** PM, designer, junior researcher
**Time:** 1 week (recruit + sessions + synthesis)
**Output:** Top friction list + verbatim quotes

## Before you start (15 min)
- [ ] Name the decision this informs
- [ ] Define the persona (link to existing persona doc)
- [ ] Write 3-5 tasks (outcome-framed; see template)
- [ ] Check budget: $500 incentive (5 × $100)

## Recruit (2-3 days)
- [ ] Post project on User Interviews (template link)
- [ ] Use existing screener template
- [ ] Anti-screens for pros + competitors
- [ ] Recruit 7 (over-recruit for no-shows)

## Sessions (2 days)
- [ ] Pilot 1 session internally first
- [ ] Run 5 sessions with think-aloud protocol (cheat sheet)
- [ ] Capture observer notes (template)

## Synthesis (1-2 days)
- [ ] Upload transcripts to Dovetail (project link)
- [ ] Tag at quote level (taxonomy link)
- [ ] Pull 5 themes (≥3 participants each)
- [ ] Write readout (template)

## Stuck?
- Slack #user-research-help OR book office hours
```

### Recipe 8: Quarterly skills assessment

```markdown
# Quarterly DIY-research health check

## Survey to PMs / designers (5 questions)
1. Did you run any research this quarter? (Y/N)
2. If yes, what method? (multi-select)
3. What was confusing or stuck? (open)
4. What would help you DIY more confidently? (open)
5. Likelihood to recommend research practice (1-7)

## Researcher review
- Read DIY readouts from quarter
- Note: where method was wrong, leading questions, etc.
- Surface common pitfalls in next training cycle
```

### Recipe 9: Recurring "research showcase" lunch-and-learn

```markdown
# Monthly research showcase (60 min)

## Format
- 2 × 20-min researcher-led presentations of recent insights
- 20 min Q&A
- Replay shared in #user-research channel

## Goal
- Surface insights to broader org
- Demonstrate research value
- Build cross-functional empathy

## Notion + Loom backup
- All decks saved to Notion
- Loom recording shared async
```

### Recipe 10: Anti-democratization risks

```markdown
# When NOT to democratize (so trust isn't lost)

## Don't push DIY for:
- High-stakes launch decisions (research team owns)
- Accessibility research (researcher + Fable)
- Pricing studies (rigor matters)
- Synthesis from raw transcripts (memory bias)
- Persona authoring (research grounding required)
- Setting up repository or taxonomy

## Symptoms of over-democratization
- DIY readouts citing 1 participant as "theme"
- Hypothetical questions surfacing as evidence
- Personas drifting toward marketing fiction
- Research repo cluttered with one-off docs

## Fix
- Pull back: researcher reviews all DIY readouts before publication
- Re-train on what went wrong
- Refresh escalation matrix
```

## Examples

### Example 1: Stand up research democratization practice
**Goal:** Enable 12 PMs to DIY common research.

**Steps:**
1. Build wiki (Recipe 2).
2. Author cheat sheets (Recipe 3).
3. Self-serve playbooks (Recipe 7) for top 3 method types.
4. Kickoff deck (Recipe 5).
5. Schedule weekly office hours (Recipe 6).
6. Train via session + lunch-and-learn (Recipe 9).
7. Quarterly health check (Recipe 8).

**Result:** PMs run discovery; researchers do high-rigor + accessibility + synthesis.

### Example 2: Recover from over-democratization
**Goal:** Recalibrate after DIY-research quality slipped.

**Steps:**
1. Survey + readout audit (Recipe 8).
2. Identify pitfalls (leading Qs, single-voice themes).
3. Refresh escalation matrix (Recipe 4) — pull more under researcher.
4. Targeted re-training on weakest area.
5. Researcher review of all DIY readouts for one quarter.

**Result:** Trust + quality restored.

## Edge cases / gotchas

- **Curriculum too long.** >2 hours = no completion. Keep core to 60-90 min total.
- **No office hours.** Wiki without humans = stale. Hold weekly slot consistently.
- **PMs running JTBD without rigor.** Pair-mode first, then DIY.
- **Hand-off without escalation matrix.** Vague "you can DIY most things" → quality drift.
- **No accountability.** Researcher reviewing DIY readouts is non-negotiable.
- **One-shot training.** Quarterly refresh + showcases needed.
- **Cultural mismatch.** Eng-heavy teams may resist "soft" methods. Lead with quant + behavior.
- **Researcher as bottleneck.** Democratize without losing rigor; escalation matrix balances.
- **Wiki without owner.** Assign librarian; refresh quarterly.
- **Training without practice.** Always include role-play / live exercise.
- **Lunch-and-learn empty.** Heavy promotion early; build the habit.

## Sources

- [NN/g — Democratize UX Research](https://www.nngroup.com/articles/democratize-ux-research/)
- [User Interviews — Democratizing User Research](https://www.userinterviews.com/blog/democratizing-user-research)
- [ResearchOps Community — Democratization](https://researchops.community)
- [Erika Hall — Just Enough Research](https://abookapart.com/products/just-enough-research)
- [Rob Fitzpatrick — The Mom Test](https://www.momtestbook.com)
- [Notion API — databases](https://developers.notion.com/reference/database)
