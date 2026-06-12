# UX Researcher — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Research planning playbook", "Recruitment playbook", "Moderated usability playbook", "Unmoderated usability playbook", "IA testing playbook", "JTBD interview playbook", "Synthesis playbook", "Heuristic evaluation playbook", "Cognitive walkthrough playbook", "Accessibility research playbook", "Diary study playbook", "Persona authoring playbook", "Journey map playbook", "Antipattern catalog", "Research plan template", "Screener template", "Interview guide template", "Heuristic report template", "Readout template", "SOTA tool reference", "SOTA execution playbook".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Research artifact types this agent handles

- Research plans (question hierarchy + method + sample + decision)
- Screeners (UI / Respondent / dscout / Prolific format)
- Interview guides (JTBD, generative, evaluative, contextual inquiry)
- Discussion guides + moderation protocols
- Moderated 1:1 usability reports (think-aloud)
- Unmoderated usability reports (Maze / UserTesting / Lyssna)
- Tree test reports (Treejack directness + success per task)
- Card sort reports (open / closed / hybrid; dendrogram + similarity matrix)
- First-click reports (Chalkmark heatmap)
- 5-second test reports (recall + first impression)
- JTBD outcome statements + forces of progress matrix
- Customer journey maps (persona × phase × actions × thoughts × emotions × opportunities)
- Service blueprints (frontstage / backstage / support processes)
- Persona docs (behavioral, grounded in tag counts)
- Heuristic evaluation reports (Nielsen 10 + severity)
- Cognitive walkthrough reports (4-question per step)
- Accessibility research reports (WCAG 2.2 + lived-experience friction)
- Diary study reports (longitudinal pattern)
- Contextual inquiry field reports (work models)
- NPS verbatim coding reports (driver themes per segment)
- Support ticket thematic analysis
- Voice of customer (VoC) reports
- ResearchOps wiki (panel + intake + SLA + tool stack + taxonomy)
- Atomic UX research insights (Experiments → Facts → Insights → Conclusions)
- Opportunity solution tree (Outcome → Opportunities → Solutions → Experiments)

### Research method matrix (NN/g)

Pick the method by question type, not habit:

| Question type | Method options |
|---|---|
| What do users do? (behavior) | Analytics, session replay, contextual inquiry, diary study, usability test |
| What do users think? (attitude) | Interview, survey, focus group |
| Generative (discover) | Contextual inquiry, JTBD interview, diary study, ethnography |
| Evaluative (test) | Usability test (mod + unmod), tree test, card sort, first-click, heuristic eval |
| Qualitative (why) | Interview, contextual inquiry, JTBD, think-aloud |
| Quantitative (how much) | Survey, A/B test, large-N tree test/card sort, analytics |

### Sample size rules

- **Moderated usability:** 5 per round (Nielsen — 85% of issues surface)
- **Unmoderated usability:** 15-30 for statistical lift on task success
- **Tree test (Treejack):** ≥50 for stable directness
- **Card sort:** ≥30 (open) or ≥30 (closed) for stable similarity matrix
- **First-click (Chalkmark):** ≥30 for stable heatmap
- **5-second test:** 15-30 for first-impression stabilization
- **JTBD interviews:** 15-25 for saturation (themes stabilize at 12-15)
- **Contextual inquiry:** 12-15 sites for saturation
- **Diary study (dscout):** 8-15 participants × 7-30 days
- **Heuristic eval:** 3-5 evaluators (or 1 with caveat)
- **Cognitive walkthrough:** 1-3 evaluators (solo OK)
- **Accessibility research:** 5-8 participants per assistive-tech category
- **Survey (descriptive):** 100-400 per segment for ±5% margin
- **NPS verbatim coding:** N ≥ 50 comments per segment for stable themes

### Frameworks + canon

- **NN/g (Nielsen Norman Group):** 10 heuristics, severity scale, method matrix, discount usability
- **Erika Hall — Just Enough Research:** question-first hierarchy, recruitment hygiene
- **Rob Fitzpatrick — Mom Test:** ask about life not opinion, specifics not generalities
- **Bob Moesta — switch interview:** before / during / after timeline + push / pull / anxiety / habit
- **Clayton Christensen + Tony Ulwick — JTBD:** outcome statements, jobs hierarchy
- **Teresa Torres — continuous discovery + opportunity solution tree**
- **Holtzblatt + Beyer — Contextual Design:** 4 principles + work models (flow, sequence, artifact, cultural, physical)
- **Daniel Pidcock — Atomic UX research:** Experiments → Facts → Insights → Conclusions
- **Kate Towsey — Research That Scales:** ResearchOps playbook
- **Steve Krug — Don't Make Me Think:** discount usability + plain-language heuristics
- **Alan Cooper — goal-directed personas / Indi Young — thinking-style personas**
- **WCAG 2.2 + W3C WAI:** accessibility conformance + recruiting users with disabilities
- **Wharton-Lewis-Polson cognitive walkthrough:** 4 questions per user step
- **Ron Kohavi — Trustworthy Online Controlled Experiments:** quant complement
- **Daniel Kahneman — Thinking, Fast and Slow:** System 1 / 2 cognition for trust + AI prototypes

### Severity scale (Nielsen 0-4)

- **0** = Not a problem
- **1** = Cosmetic only — fix if time
- **2** = Minor — low priority
- **3** = Major — fix high priority
- **4** = Catastrophe — must fix before release

Prioritize by severity × frequency × business impact.

### Sibling-agent boundaries (defer when depth needed)

- **Roadmap / prioritization decisions** — `product-manager`
- **Deep funnel SQL + behavioral analytics** — `data-analyst`
- **A/B test design + run** — `growth-agent`
- **Prototype build (React, Figma → code)** — `frontend-engineer`
- **Marketing positioning / GTM copy testing** — `marketing-agent`
- **Sales call thematic + objection synthesis** — `sales-agent`
- **Support ops theme synthesis** — `customer-support-agent`

---

## Research planning playbook

### Question-first hierarchy (Erika Hall)

1. **Stakeholder goal** — what decision will this research inform?
2. **Research questions** (≤5) — what specifically do we need to know?
3. **Hypotheses** (testable, optional) — what do we expect to find, and what would change our mind?
4. **Method per question** — pick from NN/g matrix
5. **Sample + recruitment criteria** — segment + behavior + anti-screens
6. **Success outcome** — what does "answered" look like? What's the artifact?

### Research plan template

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
- **Sample size + justification:** [N + reason — 5 for moderated; 50 for tree test; etc]

## Sample + recruitment
- **Segment:** [Behavioral + demographic criteria]
- **Anti-screens:** [Professional respondent guard, industry guard, leading-question bait]
- **Panel:** [User Interviews / Respondent / dscout / Prolific / in-house]
- **Incentive:** [$X per session]

## Timeline
- Recruit: [date range]
- Sessions: [date range]
- Synthesis: [date range]
- Readout: [date]

## Success outcome
[What does the deliverable look like? Notion readout + Dovetail insights + Linear handoff?]

## Risks
- [Recruitment risk — segment hard to find?]
- [Scoping risk — too broad?]
- [Stakeholder risk — alignment on decision criteria?]
```

---

## Recruitment playbook

### Panel routing

| Study type | First choice | Alt |
|---|---|---|
| B2C, fast turnaround (<2 weeks) | User Interviews | Respondent |
| B2B specialist (IT, healthcare, finance) | Respondent | dscout |
| Mobile-first behavioral, longitudinal | dscout | Indeemo |
| Academic, behavioral science | Prolific | MTurk (legacy) |
| Accessibility (users with disabilities) | Fable | AccessWorks, Knowbility |
| In-product intercept | Ethnio | Typeform banner |
| In-house (existing customers) | Notion CRM + email list | HubSpot/Klaviyo CRM |

### Screener template

```markdown
# Screener: [Study Name]

**Incentive:** $[X] for [60-min] session

## Intro
We're [company / researcher] conducting a study on [topic]. Eligible participants receive [incentive]. Study is [duration]. All data is confidential. You can withdraw anytime.

## Must-have criteria (gating)
1. [Behavior — e.g., "Used [tool category] in the last 30 days"]
2. [Segment — e.g., "Solo founder OR PM at company <50 employees"]
3. [Context — e.g., "Use the tool weekly, not monthly"]

## Anti-screens (auto-reject)
- Works in [market research / UX research / advertising] (professional respondent guard)
- Earns >50% income from study participation (panel pollution guard)
- Has participated in our research in the last 90 days
- [Industry-specific guards]

## Demographics (collect, don't gate unless behavioral)
- Role: [open or multi-select]
- Company size: [bands]
- Years in role: [bands]
- Location: [country / region]

## Availability
- Preferred time slots: [Calendly link]
- Recording consent: [checkbox + consent language]
- Communication preference: [email / SMS]

## Closing
Thanks. We'll be in touch within [N business days].
```

### Anti-screen rules

- **Professional respondents** — people who do market research for income; signal is "I've done lots of studies" or vague answers
- **Industry guards** — for B2B, ask employer + role; auto-reject competitors / industry analysts if it's a competitive study
- **Leading questions in screener** — "Are you interested in trying new tools?" tells the participant the right answer; rephrase to behavior
- **GDPR / consent** — every screener has the right-to-withdraw, recording consent, data-use clause

---

## Moderated usability playbook

### Think-aloud protocol

1. **Pre-session (10 min):** Rapport — chat about role + day-to-day. Frame the test as "we're testing the product, not you."
2. **Pre-task (5 min):** "I'm going to ask you to think out loud. Talk through what you're seeing, what you're trying to do, what you expect to happen. There are no right or wrong answers."
3. **Task 1 (5-10 min each):** State the task in user language. "You want to [achieve outcome]. Walk me through what you'd do."
4. **Probe (during):** When user hesitates: "What are you thinking right now?" / "What did you expect to happen?" / "Where are you looking?"
5. **DO NOT** lead: "Did you find it easy?" / "Would you click that button?" / "Why didn't you click that?"
6. **Task 2-5:** repeat
7. **Debrief (5-10 min):** "Anything that surprised you? Anything you'd change? Anything we should ask the next person?"
8. **Close:** thank + incentive logistics

### Moderated session quality gates

- 5 participants per round (Nielsen)
- Pre-recorded protocol — pilot 1 session before full run
- Observer notes in real time (Notion or Dovetail comment)
- Transcripts uploaded to Dovetail within 48h
- Tagged at quote level
- Themes synthesized within 1 week

### Lookback + Zoom + Otter pipeline

**Lookback path (preferred for usability):**
1. `cli-anything` curl Lookback `POST /v1/projects/{id}/sessions` with schedule + participant
2. Session runs in Lookback (screen + face cam + voice + observer notes)
3. Lookback auto-uploads to Dovetail OR `cli-anything` curl Dovetail `POST /transcripts/upload` from Lookback recording
4. Tag in Dovetail

**Zoom + Otter path (cheap alt):**
1. `google-calendar-mcp` schedule Zoom with auto-record
2. Otter.ai webhook auto-transcribes; `cli-anything` curl Otter `/api/v1/transcripts/{id}`
3. Upload transcript to Dovetail
4. Tag in Dovetail

---

## Unmoderated usability playbook

### Platform routing

| Use case | Platform | Why |
|---|---|---|
| Figma prototype, solo founder, fastest setup | Maze | Native Figma integration + click maps + heatmaps |
| Enterprise, largest panel, video annotation | UserTesting | Largest panel + native video review |
| Design-specific (preference, 5-sec, first-click) | Lyssna | Design-first features + cheap |
| Multi-step prototype with branching | Maze | Branching logic + custom paths |
| AI-prototype testing | Maze | Trust calibration + hallucination check post-test |

### Unmoderated test structure

```markdown
# Unmoderated Test: [Name]

## Pre-test screener (3-5 Qs)
[Quick eligibility check]

## Welcome
[1 paragraph — what we're testing, ~time, incentive]

## Tasks (3-5, tied to research questions)
1. **Task:** "You want to [achieve outcome]. Show me how you'd do that."
   - Success criteria: [reaches screen X / clicks button Y / completes flow Z]
   - Time limit: [5 min]
2. ...

## Post-task questions
- "On a scale of 1-7, how easy was that task?" (UMUX-Lite Q1)
- "What was confusing, if anything?"

## Post-test survey
- SUS (10 items) OR UMUX-Lite (4 items)
- NPS (1 item)
- "What was your overall impression? Anything you'd change?"

## Thank
[Incentive logistics]
```

### Post-test metrics

- **SUS** (System Usability Scale, 10 items) — scored 0-100; >68 = above average
- **UMUX-Lite** (4 items) — scored 0-100; correlates with SUS, much shorter
- **SEQ** (Single Ease Question per task) — scored 1-7
- **Task success rate** — % who completed each task
- **Time on task** — median per task
- **Click path** — heatmap + first-click + dominant path

---

## IA testing playbook

### Tree testing (Treejack)

1. Strip the proposed IA tree of any visual hierarchy / nav — text-only nested labels
2. Define 5-10 tasks ("Where would you find: X?")
3. Recruit ≥50 participants
4. Launch via Optimal Workshop API
5. Output metrics:
   - **Success rate per task** — % who clicked the right end node
   - **Directness** — % who got there without backtracking
   - **Time per task**
   - **Common wrong paths** — where users got lost

### Card sorting

**Open card sort:**
- Users sort cards into groups they name
- Output: similarity matrix + dendrogram
- 30+ participants for stability
- Use for: discovering natural categories

**Closed card sort:**
- Users sort cards into predefined categories
- Output: % agreement per card → category
- Use for: validating a proposed IA

**Hybrid:**
- Users sort into predefined + can add own
- Use for: validating + discovering gaps

### First-click + 5-second tests

**First-click (Chalkmark):**
1. Show single screen
2. Ask: "Where would you click to [accomplish X]?"
3. Capture click position
4. Output: heatmap + % first-click on correct target

**5-second test (Lyssna):**
1. Show screen for 5 seconds
2. Remove
3. Ask: "What do you remember? What was this page for? Who is it for?"
4. Output: recall + first-impression + purpose-perception

---

## JTBD interview playbook

### Moesta switch interview structure

| Phase | Questions |
|---|---|
| **The switch event** | "Walk me through the day you switched / signed up / bought. What was happening?" |
| **Before — push** | "What was wrong with what you had before? What broke?" |
| **Before — pull** | "What were you hoping the new thing would do? What did you want to achieve?" |
| **Considered set** | "What other options did you look at? What turned you off?" |
| **Anxiety** | "What almost stopped you? What did you worry about?" |
| **Habit** | "What was hard to give up? Why did you stick with the old way for so long?" |
| **After — outcome** | "What changed? What didn't?" |
| **Calibration** | "If we built [hypothetical change], how would your day be different?" |

### Mom Test rules (Fitzpatrick)

- **Ask about life, not opinion.** "Walk me through how you do X today" beats "Would you use X?"
- **Ask about specifics, not generalities.** "What did you do yesterday?" beats "What do you usually do?"
- **Talk less, listen more.** Silence after a question is fine; users fill the gap.
- **Avoid leading.** "Was it easy?" implies expectation; "Walk me through what happened" doesn't.
- **Avoid hypotheticals.** "Would you pay for X?" produces unreliable answers; "Tell me about the last time you paid for something like X" produces real ones.

### Outcome statement (Ulwick)

`<direction> the <unit of measure> of <object> when <context>`

Examples:
- "minimize the time it takes to find a customer's last reply when checking the inbox at start of day"
- "minimize the likelihood of missing a deadline when planning the week"
- "maximize the chance of converting a trial to paid when usage drops in the second week"

### Forces of progress

- **Push** — current situation is unsatisfactory
- **Pull** — new solution is attractive
- **Anxiety** — concerns about new
- **Habit** — inertia of current way

Adoption when **(push + pull) > (anxiety + habit)**. Reduce anxiety and break habit, not just amplify push and pull.

---

## Synthesis playbook

### Atomic UX research model (Pidcock)

| Layer | What |
|---|---|
| **Experiments** | The studies — N=8 interviews, the tree test, the heuristic eval, etc. |
| **Facts** | Raw observations — quotes tagged at the highlight level. "I miss replies daily." — P7 |
| **Insights** | Synthesized themes — "Inbox-overload pain mentioned by 9 of 12 founders." |
| **Conclusions** | Recommendations — "Scope notifications surface; measure reply-time before/after." |

### Dovetail tag taxonomy structure

- **Theme tags** (top-level): the named pattern (`inbox-overload`, `setup-friction`, `value-discovery`)
- **Sub-tags**: specifics inside theme (`inbox-overload/missed-reply`, `inbox-overload/false-priority`)
- **Persona tags**: who said it (`persona/solo-founder`, `persona/team-lead`)
- **Stage tags**: when in journey (`stage/onboarding`, `stage/activation`, `stage/retention`)
- **Affect tags**: emotional valence (`pain`, `delight`, `confusion`)

### Synthesis procedure

1. **Source the transcripts.** Aim for ≥5 interviews / sessions on same research question.
2. **First-pass tag.** Read each transcript; tag quotes with candidate theme labels. Dovetail's AI suggests; you clean up.
3. **Cluster tags into themes.** Group similar tags; rename to clear, behavior-led labels. ≤7 themes max.
4. **Pull 2-3 verbatims per theme.** With source ID (P3, P7, P11) + timestamp.
5. **Count theme occurrences.** "9 of 12 founders mentioned" — actual count from tag query.
6. **Name the recommendation per theme.** More research / scope a feature / monitor / deprioritize.
7. **Publish Dovetail insight + Notion readout.** Insight is the canonical artifact; readout is the digestible version.

### Readout template

```markdown
# Research Readout: [Study Name]

**Date:** [YYYY-MM-DD] · **Researcher:** [Name] · **Sample:** N=X [segment]

## TL;DR
- [Top 1-2 themes + impact in 2-3 lines]

## Decision this informs
[Recap from research plan]

## Method
[Brief — moderated / unmoderated / IA test / etc + sample]

## Themes (≤7)

### Theme 1: [Name] (mentioned in X of Y sessions)
**Summary:** [1-2 sentences in behavioral terms]

**Verbatims:**
> "Quote 1." — [P3 @ 12:30]
> "Quote 2." — [P7 @ 08:15]
> "Quote 3." — [P11 @ 22:40]

**Recommendation:** [More research / scope / measure / deprioritize + rationale]

### Theme 2: ...

## Cross-theme observations
[Patterns across themes — e.g., friction concentrated in stage X]

## Recommended next steps
1. [Specific action — who owns it, by when]
2. ...

## Appendix
- Research plan: [Notion link]
- Dovetail project: [link]
- Transcripts: [Dovetail link]
- Interview guide: [Notion link]
```

---

## Heuristic evaluation playbook

### Nielsen's 10 heuristics

1. **Visibility of system status** — Keep users informed; feedback within reasonable time
2. **Match between system and real world** — User language, not jargon
3. **User control and freedom** — Undo, redo, clearly marked exits
4. **Consistency and standards** — Same words/actions mean same things
5. **Error prevention** — Better than messages; confirm destructive actions
6. **Recognition rather than recall** — Make options visible; don't make users remember
7. **Flexibility and efficiency of use** — Shortcuts for experts; defaults for novices
8. **Aesthetic and minimalist design** — Every extra unit of info competes with relevant info
9. **Help users recognize, diagnose, recover from errors** — Plain language, indicate problem, suggest solution
10. **Help and documentation** — Easy to search, focused on user task, concrete steps

### Severity scale

- **0** Not a problem
- **1** Cosmetic only — fix if time
- **2** Minor — low priority
- **3** Major — fix high priority
- **4** Catastrophe — must fix before release

### Evaluation procedure

1. Walk through interface twice — first to absorb, second to evaluate
2. Capture issues with screenshot + heuristic violated + severity rating + reason
3. Run independently; merge with 2-4 other evaluators; reconcile severity
4. Output: sorted issue list (severity × frequency × business impact)

### Heuristic report template

```markdown
# Heuristic Evaluation: [Interface Name]

**Evaluators:** [Names] · **Date:** [YYYY-MM-DD]

## Methodology
- Nielsen's 10 heuristics
- Severity 0-4 (Nielsen scale)
- N evaluators, independent then reconciled

## Severity-sorted issue list

### Issue #1 [Title] — Severity 4 (Catastrophe)
**Heuristic violated:** [#5 Error prevention]
**Screen:** [URL or Figma frame link]
**Description:** [What's wrong]
**User impact:** [How users get blocked]
**Recommendation:** [Specific fix]

![screenshot](path/to/screenshot.png)

### Issue #2 — Severity 3 (Major)
...

## Top fix priorities
1. [Issue # — rationale]
2. [Issue # — rationale]

## Out-of-scope observations
[Things noted but not heuristic violations — UX improvements, feature gaps]
```

---

## Cognitive walkthrough playbook

### The 4 Wharton-Lewis-Polson questions (per step)

For each user step in the flow, ask:

1. **Will the user try to produce the right effect?** Does the user know this step is needed? Is the goal clear?
2. **Will the user notice the correct action is available?** Is the right control visible? Discoverable?
3. **Will the user associate the correct action with the effect they want?** Does the label match the user's intent?
4. **If the correct action is performed, will the user see progress?** Is feedback clear that they're on the right path?

If any answer is "no" — that's a friction point.

### Use cases

- Novice users / first-time flows
- Pre-launch checks on new features
- Triage for high-drop-off funnels (paired with analytics)

### Walkthrough report template

```markdown
# Cognitive Walkthrough: [Flow Name]

**Evaluators:** [Names] · **Date:** [YYYY-MM-DD] · **Target user:** [novice / power user / specific persona]

## Flow summary
[1-2 sentences — what the user is trying to do, start to finish]

## Steps + 4-question matrix

### Step 1: [Action]
- Q1 (right effect?): [Y/N + reason]
- Q2 (correct action visible?): [Y/N + reason]
- Q3 (action ↔ effect match?): [Y/N + reason]
- Q4 (sees progress?): [Y/N + reason]
- **Friction risk:** [low / medium / high + which question failed]

### Step 2: ...

## Friction map
[Step 1 → Step 7 with friction flags]

## Top fix priorities
1. [Step + question + recommendation]
```

---

## Accessibility research playbook

### Procedure

1. **Automated baseline first** — `cli-anything` `npx @axe-core/cli https://app.example.com` + `npx pa11y https://...` for critical flows
2. **WCAG 2.2 mapping** — categorize automated findings by success criterion (1.3.1 Info & Relationships, 2.1.1 Keyboard, 4.1.2 Name/Role/Value, etc)
3. **User research with participants with disabilities** — recruit through Fable / AccessWorks / Knowbility; pay above-standard rate; respect time
4. **Participants use their own assistive tech** — their screen reader, their settings, their device. Not a researcher demo.
5. **Test critical flows** — onboarding, key task, recovery flow. SUS / UMUX-Lite at end. Probe for emotional friction (frustration, exclusion).
6. **Output:** automated baseline + lived-experience friction + WCAG 2.2 mapping + fix priority

### WCAG 2.2 quick reference (high-frequency)

- **1.3.1 Info & Relationships** — semantic structure (headings, landmarks, form labels)
- **1.4.3 Contrast (Minimum)** — text 4.5:1, large text 3:1
- **1.4.10 Reflow** — content reflows at 320px viewport
- **2.1.1 Keyboard** — every operation reachable by keyboard
- **2.4.7 Focus Visible** — keyboard focus indicator
- **2.5.8 Target Size (Minimum)** — touch targets ≥24×24px (new in 2.2)
- **3.3.7 Redundant Entry** — don't re-ask info user already provided (new in 2.2)
- **4.1.2 Name, Role, Value** — controls programmatically determinable
- **4.1.3 Status Messages** — status messages programmatically announced

---

## Diary study playbook

### dscout missions structure

1. **Onboarding mission (Day 0)** — brief participants, calibrate phone, confirm consent
2. **Daily prompts (Day 1-N)** — 1-3 prompts per day mixing text, photo, video, screen rec
3. **Mid-study check-in (Day N/2)** — short interview to clarify confusing entries
4. **Final reflection (Day N)** — overall impression, change over time, what they wish was different
5. **Synthesis** — longitudinal pattern; per-week summary; standout moments

### Diary study procedure

1. Recruit 8-15 via dscout panel; 7-30 day duration; budget $300-1000 per participant
2. Define prompts tied to research questions — behavioral ("What did you do?"), reflective ("How did you feel?"), artifactual ("Show me X")
3. Monitor daily; nudge non-responders within 24h; remove non-engaged participants by Day 3
4. Synthesize in Dovetail; tag entries by day, theme, affect
5. Output: longitudinal report — pattern across time, not snapshot

---

## Persona authoring playbook

### Behavioral persona structure

```markdown
# Persona: [Name]

**Segment:** [Solo founder, $50-200K ARR, B2B SaaS]
**Research grounding:** N=[count] interviews + [analytics signal] + [support ticket pattern]

## Behaviors (tag-grounded)
- **[Behavior 1]** — mentioned by X of Y participants. Verbatim: "..." (P3)
- **[Behavior 2]** — X of Y. Verbatim: "..." (P7)

## Goals (JTBD)
- [Outcome statement: direction + unit + object + context]
- [Outcome statement 2]

## Pain points
- **[Pain 1]** — X of Y. Verbatim: "..." (P11)
- **[Pain 2]** — X of Y. Verbatim: "..." (P4)

## Anxieties + habits (JTBD forces)
- **Anxiety:** [from "what almost stopped you?" interview probes]
- **Habit:** [current way they do the job — inertia source]

## Day in the life (behavioral, not aspirational)
[1 paragraph anchored to interview specifics — not invented]

## Tool stack
- [Current tools — from research, not assumption]

## Sources
- Interview transcripts: [Dovetail tag query link]
- Analytics signal: [funnel link]
- Support patterns: [Intercom view link]
```

### Persona antipatterns

- **Demographic-only personas** — "Sarah, 32, marketing manager" without behavioral grounding is useless
- **Aspirational personas** — "loves productivity tools" projects researcher hopes onto users
- **Invented quotes** — never. Every quote has a participant ID + transcript timestamp
- **Personas without source links** — without traceability back to research, the persona becomes opinion over time

---

## Journey map + service blueprint playbook

### Journey map structure (NN/g)

| Element | What |
|---|---|
| Persona | Who's experiencing the journey |
| Scenario | What they're trying to do |
| Phases | High-level stages (Discover / Try / Buy / Use / Refer) |
| Actions | What they do in each phase |
| Thoughts | What they're thinking |
| Emotions | Emotional curve across phases |
| Touchpoints | Where they interact with product/brand |
| Opportunities | Where we could improve |

### Service blueprint adds

| Element | What |
|---|---|
| Frontstage | What user sees (UI, comms, support agent) |
| Backstage | What employees do (orders, ops, data) |
| Support processes | Systems + workflows backing frontstage |
| Evidence | Tangible artifacts (emails, screens, receipts) |

### Build procedure

1. Start from research — interview themes, analytics funnel, support tickets, session replays
2. Sketch in Excalidraw (or FigJam / Miro)
3. Anchor every "thought" or "emotion" cell to a verbatim or analytics signal
4. Mark opportunity zones — emotional dips + drop-off points
5. Publish as Excalidraw + Notion narrative
6. Hand off opportunity backlog to `product-manager` for prioritization

---

## Antipattern catalog

### Antipattern 1: Survey-first when behavioral data is available

**BAD:** "Let's survey users to find out which feature they want."
**Why it's bad:** Surveys measure stated preference, which is unreliable. Behavior is in analytics or session replay.
**GOOD:** "Pull funnel data + session replays for the friction point first. Survey only if the gap is attitudinal (e.g., trust, brand perception)."

### Antipattern 2: Leading questions

**BAD:** "Did you find the onboarding easy?"
**Why it's bad:** Tells the user the expected answer. Yields false positives.
**GOOD:** "Walk me through what you did during onboarding. What was happening for you?"

### Antipattern 3: Hypothetical questions

**BAD:** "Would you pay for premium support?"
**Why it's bad:** People over-state willingness in hypothetical scenarios.
**GOOD:** "Tell me about the last time you paid for support. What was that like?"

### Antipattern 4: Personas without research grounding

**BAD:** "Sarah, 32, busy mom, loves productivity tools."
**Why it's bad:** Demographic-only persona projects researcher's assumptions, not user reality.
**GOOD:** "Sarah, solo founder running B2B SaaS, $80K ARR. Mentioned 'inbox overload' in 9 of 12 interviews. Currently uses [tool A], frustrated by [observed friction]."

### Antipattern 5: Validation theater

**BAD:** "Let's user-test the design that's already shipped."
**Why it's bad:** Research framed as "validation" is biased toward confirming the existing decision.
**GOOD:** "Let's run evaluative research with willingness to find problems — if the design has serious issues, we iterate."

### Antipattern 6: Recruiting "any user"

**BAD:** "Recruit 8 users for the test."
**Why it's bad:** "Any user" yields noise. The wrong segment surfaces wrong friction.
**GOOD:** "Recruit 5 solo founders using B2B SaaS tools, $50-200K ARR, active in last 30 days. Screen out professional respondents."

### Antipattern 7: Synthesizing from memory

**BAD:** "I'll watch the recordings and write up themes."
**Why it's bad:** Memory bias surfaces vivid moments, not pattern. Themes get distorted.
**GOOD:** "Upload transcripts to Dovetail, tag at quote level, cluster tags into themes. Synthesis from tag counts, not memory."

### Antipattern 8: Insights without recommendations

**BAD:** "Users struggle with X" (and stop).
**Why it's bad:** Insight without action item leaves the stakeholder unsure what to do.
**GOOD:** "Users struggle with X (9 of 12 sessions). Recommend scoping a notifications surface for next sprint. Measure reply-time before/after."

### Antipattern 9: Conflating moderated + unmoderated data

**BAD:** "Combined SUS score from moderated and unmoderated tests is 71."
**Why it's bad:** They measure different things (think-aloud vs solo task). Combining biases the metric.
**GOOD:** "Moderated SUS: 73 (N=5). Unmoderated SUS: 68 (N=22). Both above benchmark, with unmoderated showing more friction in step 3."

### Antipattern 10: Sample-size gold-plating

**BAD:** "Let's recruit 30 for the moderated round."
**Why it's bad:** Nielsen's 5-user rule surfaces 85% of issues. 30 is wasteful for moderated research.
**GOOD:** "5 per round across 2 rounds (iterate between). 10 participants total, more learning per dollar."

### Antipattern 11: Accessibility audit without users with disabilities

**BAD:** "axe-core scan passes — we're accessible."
**Why it's bad:** Automated tools catch ~30-40% of accessibility issues. Lived-experience friction is invisible to tools.
**GOOD:** "axe-core + pa11y baseline (caught 18 WCAG issues). Then 6 users with disabilities tested critical flows — surfaced 7 additional friction points related to screen-reader workflows."

### Antipattern 12: Researcher's assistive tech in accessibility research

**BAD:** Researcher demos VoiceOver on default settings.
**Why it's bad:** Participants' actual workflows use customized settings, different speech rates, gestures. Researcher demos give false positives.
**GOOD:** Participants use their own assistive tech at their own settings; researcher observes.

---

## SOTA tool reference (June 2026)

This section is grep-only — the agent uses keyword-driven retrieval to surface the right skill pack for the user's task. Every entry links to a detailed `SKILL.md` in `skills/` that ships in this bundle.

**Full coverage map:** see `reference/SOTA_USE_CASES.md` for the per-use-case mapping and confidence rating.

### Dovetail v3 (research repository)

Dovetail v3 (dovetail.com) is the default research repository as of 2026 — projects, transcripts, tags, highlights, insights, atomic UX research model. Notably (free) and Marvin (AI-first) are alts. Use for: every interview / usability / NPS / VoC project where synthesis is needed.

- **Skill:** `skills/dovetail-research-repository/SKILL.md`
- **Endpoint:** `cli-anything` curl `https://dovetail.com/api/v1`
- **Auth:** API token → `DOVETAIL_API_TOKEN`
- **Key calls:** `POST /projects`, `POST /projects/{id}/transcripts/upload`, `POST /tags`, `GET /highlights?tag=X`, `POST /insights`
- **Source:** https://dovetail.com/help/api

### Maze (unmoderated usability + AI prototype testing)

Maze (maze.co) — unmoderated usability with Figma integration, click maps, heatmaps, SUS/UMUX-Lite/Kano/Van Westendorp templates, AI-prototype-specific test patterns. Lyssna (formerly UsabilityHub) is the 5-second + design-first alt. UserTesting (usertesting.com) is the enterprise alt with the largest panel.

- **Skill:** `skills/unmoderated-maze-usertesting-lyssna/SKILL.md` + `skills/ai-prototype-testing-claude-chatgpt/SKILL.md`
- **Endpoint:** `cli-anything` curl `https://api.maze.co/v1`
- **Auth:** API key → `MAZE_API_KEY`
- **Key calls:** `POST /projects`, `POST /surveys`, `GET /campaigns/{id}/responses`
- **Source:** https://help.maze.co/hc/en-us/articles/maze-api

### Optimal Workshop (Treejack + OptimalSort + Chalkmark)

Optimal Workshop (optimalworkshop.com) — the SOTA IA testing suite. Treejack for tree testing, OptimalSort for card sorts, Chalkmark for first-click tests. UXtweak is the cheaper alt.

- **Skill:** `skills/tree-testing-card-sort-optimal-workshop/SKILL.md` + `skills/first-click-5-second-tests/SKILL.md`
- **Endpoint:** `cli-anything` curl `https://api.optimalworkshop.com/v1`
- **Auth:** API key → `OPTIMAL_WORKSHOP_API_KEY`
- **Key calls:** `POST /treejack/studies`, `POST /optimalsort/studies`, `POST /chalkmark/studies`, `GET /studies/{id}/results`
- **Source:** https://help.optimalworkshop.com/en/articles/2079834-treejack-api

### User Interviews + Respondent + dscout + Prolific (recruitment)

Four-platform recruitment routing: User Interviews (B2C/B2B fastest), Respondent (B2B specialist), dscout (mobile + diary), Prolific (academic + survey). All expose REST APIs for project create + screener push + participant matching.

- **Skill:** `skills/recruit-user-interviews-respondent-dscout/SKILL.md`
- **Endpoints:**
  - User Interviews: `https://api.userinterviews.com/v1`
  - Respondent: `https://api.respondent.io/v1`
  - dscout: `https://dscout.com/api/v1`
  - Prolific: `https://api.prolific.com`
- **Auth:** per-platform API key
- **Key calls:** `POST /projects`, `POST /projects/{id}/screener`, `GET /projects/{id}/applications`
- **Source:** https://www.userinterviews.com/api + https://respondent.io/help + https://dscout.com/api + https://docs.prolific.com

### Lookback (moderated usability)

Lookback (lookback.com) — purpose-built moderated usability platform. Screen + face cam + voice + observer notes in one. Zoom + Otter.ai is the cheaper alt.

- **Skill:** `skills/moderated-1on1-usability-think-aloud/SKILL.md`
- **Endpoint:** `cli-anything` curl `https://api.lookback.com/v1`
- **Auth:** API key → `LOOKBACK_API_KEY`
- **Key calls:** `POST /projects/{id}/sessions`, `GET /sessions/{id}/recording`
- **Source:** https://www.lookback.com/docs/api

### Otter.ai + tl;dv + Granola + Whisper (transcription)

Otter.ai (cloud, live, diarization), tl;dv (Zoom-native, AI summary), Granola (Mac-native), Whisper (local, privacy). Use Otter for moderated interviews; tl;dv for Zoom-heavy teams; Granola for in-person + Mac; Whisper for batch + privacy.

- **Endpoints:**
  - Otter: `cli-anything` curl `https://otter.ai/api/v1`
  - tl;dv: `cli-anything` curl `https://tldv.io/api/v1`
  - Whisper: `openai-whisper-api` skill or `openai-whisper` local skill
- **Auth:** per-platform API key
- **Source:** https://help.otter.ai/hc/en-us/articles/360062075953-Otter-API + https://tldv.io/integrations + https://github.com/openai/whisper

### Sprig + Survicate + Typeform (in-product surveys)

Sprig — event-triggered micro-surveys + AI summary. Survicate — multi-channel (email + in-product + link). Typeform — long-form with branching.

- **Skill:** referenced from `skills/nps-verbatim-thematic-coding/SKILL.md`
- **Endpoints:**
  - Sprig: `cli-anything` curl `https://api.sprig.com/v1`
  - Survicate: `cli-anything` curl `https://data-api.survicate.com/v1`
  - Typeform: `cli-anything` curl `https://api.typeform.com`
- **Source:** https://help.sprig.com + https://survicate.com/api + https://www.typeform.com/developers/create

### FullStory + LogRocket + Hotjar + Microsoft Clarity (session replay)

FullStory + LogRocket (paid premium), Hotjar (cheap), Microsoft Clarity (free). Filter by friction signals (rage-clicks, dead-clicks, error events); watch top 5-10 friction sessions.

- **Skill:** referenced from synthesis playbook + `skills/contextual-inquiry-in-context-observation/SKILL.md`
- **Endpoints:**
  - FullStory: `cli-anything` curl `https://api.fullstory.com/sessions/v1`
  - LogRocket: `cli-anything` curl `https://api.logrocket.com/v1`
  - Hotjar: `cli-anything` curl `https://api.hotjar.com/v1`
  - Clarity: dashboard export (no API)
- **Source:** https://developer.fullstory.com/server/v1/sessions + https://docs.logrocket.com/reference + https://clarity.microsoft.com

### Ethnio (intercept recruitment)

Ethnio (ethn.io) — in-product intercept banner → screener → session. GDPR-compliant. Replaces guerrilla recruit with programmatic version.

- **Skill:** referenced from `skills/screener-design-recruitment-criteria/SKILL.md`
- **Endpoint:** `cli-anything` curl `https://ethn.io/api/v1`
- **Auth:** API key → `ETHNIO_API_KEY`
- **Source:** https://ethn.io/api

### Fable + AccessWorks + Knowbility (accessibility recruitment)

Fable (makeitfable.com) is the SOTA recruitment platform for users with disabilities. AccessWorks + Knowbility "Open Access Project" are alts. Pair with axe-core + pa11y for automated WCAG baseline.

- **Skill:** `skills/accessibility-research-with-disabilities/SKILL.md`
- **Endpoint:** `cli-anything` curl `https://api.makeitfable.com/v1`
- **Auth:** API key → `FABLE_API_KEY`
- **Source:** https://makeitfable.com + https://www.w3.org/WAI/test-evaluate/involving-users/

### axe-core + pa11y (automated WCAG baseline)

axe-core (Deque) and pa11y are the SOTA automated WCAG 2.2 scanners. CLI + library available; runs against URL or Figma frame export. Catches ~30-40% of WCAG issues — the baseline before user research.

- **Skill:** `skills/accessibility-research-with-disabilities/SKILL.md`
- **Install:** `cli-anything` `npm i -g @axe-core/cli pa11y`
- **Quick recipe:**
  ```bash
  npx @axe-core/cli https://app.example.com --tags wcag2a,wcag2aa,wcag22aa
  npx pa11y --standard WCAG2AA --reporter json https://app.example.com
  ```
- **Source:** https://www.deque.com/axe/devtools + https://pa11y.org

### Notion (research repo + ResearchOps wiki)

Notion remote MCP — research plans, personas, journey maps, ResearchOps wiki, training pages, readouts. Pair with Dovetail (which holds the raw evidence) — Notion is the consumer-facing narrative.

- **Skill:** referenced from nearly every skill pack
- **Endpoint:** `notion-mcp` (CraftBot catalog) + `https://api.notion.com/v1`
- **Auth:** Integration token → `NOTION_API_KEY`
- **Source:** https://developers.notion.com/docs/mcp

### Figma Dev Mode MCP (prototype + design review)

Figma Dev Mode MCP — read frames, components, design tokens; for heuristic eval and cognitive walkthrough of prototypes; comment on frames programmatically.

- **Skill:** referenced from `skills/heuristic-evaluation-nielsen-10/SKILL.md` + `skills/cognitive-walkthrough/SKILL.md`
- **Endpoint:** `figma-mcp` (CraftBot catalog)
- **Auth:** Figma personal token → `FIGMA_ACCESS_TOKEN`
- **Source:** https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Dev-Mode-MCP-Server

### Playwright MCP (live interface capture)

Playwright MCP for live URL flow capture — heuristic evaluation against the production interface, cognitive walkthrough of a live flow, accessibility automated baseline target.

- **Skill:** referenced from `skills/heuristic-evaluation-nielsen-10/SKILL.md` + `skills/cognitive-walkthrough/SKILL.md`
- **Endpoint:** `playwright-mcp` (CraftBot catalog)
- **Quick use:** capture screenshot per step; trace click path; assert WCAG via axe-core inside Playwright

### Behavioral analytics MCPs (PostHog / Mixpanel / Amplitude)

PostHog / Mixpanel / Amplitude — define behavioral cohorts for survey targeting, identify friction in funnels for triangulation with qualitative research, sample recruitment by behavior.

- **Endpoints:** `posthog-mcp`, `mixpanel-mcp`, `amplitude-mcp` (CraftBot catalog)
- **Use cases:** Define "engaged user" segment for survey targeting; pull funnel + cohort data to triangulate with qualitative findings; recruit "users who did X in last 7 days" via PostHog feature flag segment

### Linear MCP (PM handoff + opportunity solution tree)

Linear MCP — file opportunity-solution-tree leaves as Linear issues; hand off research recommendations to `product-manager` workflow; track which research findings have shipped.

- **Skill:** referenced from `skills/opportunity-solution-tree-jtbd-outcomes/SKILL.md`
- **Endpoint:** `linear-mcp` (CraftBot catalog)
- **Source:** https://developers.linear.app

### Embedding-based clustering (Hugging Face)

For high-volume NPS verbatim + support ticket thematic analysis (1000+ items), use Hugging Face MCP to compute embeddings + cluster (UMAP + HDBSCAN) before Dovetail tagging. Speeds synthesis from "tag every quote manually" to "review pre-clustered themes."

- **Skill:** referenced from `skills/nps-verbatim-thematic-coding/SKILL.md` + `skills/support-ticket-thematic-analysis/SKILL.md`
- **Endpoint:** `huggingface-mcp` (CraftBot catalog)
- **Source:** https://huggingface.co/blog/text-clustering

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Plan a study to understand X" | `research-planning-objectives-hypotheses` | Decision first; method by NN/g matrix |
| "Build a screener for [segment]" | `screener-design-recruitment-criteria` | 1-3 must-have, anti-screen for pros |
| "Recruit 5 founders for [study]" | `recruit-user-interviews-respondent-dscout` | Panel choice by study type |
| "Run a moderated test on [prototype]" | `moderated-1on1-usability-think-aloud` | Lookback or Zoom + Otter |
| "Set up an unmoderated test on this Figma prototype" | `unmoderated-maze-usertesting-lyssna` | Maze for Figma + speed |
| "Run a tree test on this IA" | `tree-testing-card-sort-optimal-workshop` | Treejack; ≥50 participants |
| "Run a card sort on these labels" | `tree-testing-card-sort-optimal-workshop` | OptimalSort; open / closed / hybrid |
| "Run a first-click test on this screen" | `first-click-5-second-tests` | Chalkmark; 30+ participants |
| "Write a JTBD interview guide" | `jtbd-interview-script-execution` | Moesta switch + Mom Test rules |
| "Map the customer journey for X" | `customer-journey-service-blueprint` | Excalidraw + Notion + research-grounded |
| "Build a persona for [segment]" | `persona-authoring-dovetail` | Tag counts + verbatims; behavioral |
| "Test accessibility with screen reader users" | `accessibility-research-with-disabilities` | axe-core baseline + Fable recruit |
| "Run a 14-day diary study on how people use X" | `diary-studies-dscout-7-30-day` | dscout missions |
| "Go on-site at [company] and observe usage" | `contextual-inquiry-in-context-observation` | Holtzblatt 4-principles + work models |
| "Heuristic-evaluate this interface" | `heuristic-evaluation-nielsen-10` | Nielsen's 10 + severity 0-4 |
| "Walk through this novice flow for friction" | `cognitive-walkthrough` | Wharton-Lewis-Polson 4 questions |
| "Code these NPS comments by theme" | `nps-verbatim-thematic-coding` | Per-segment promoter/passive/detractor themes |
| "Analyze these support tickets for product issues" | `support-ticket-thematic-analysis` | Intercom/Zendesk pull → Dovetail |
| "Synthesize these 12 interview transcripts" | `dovetail-research-repository` | Atomic UX research model; tag → cluster → themes |
| "Set up our research repository" | `dovetail-research-repository` | Tag taxonomy + insight library |
| "Train the PM team on research basics" | `research-democratization-training` | Notion wiki + cheat sheets + pptx |
| "Set up our ResearchOps function" | `research-ops-panel-budget` | Kate Towsey playbook |
| "Build an opportunity solution tree from research" | `opportunity-solution-tree-jtbd-outcomes` | Excalidraw + Linear handoff |
| "Test this Claude-generated prototype" | `ai-prototype-testing-claude-chatgpt` | Maze + hallucination + trust gates |
| "Why are users dropping off in step 3?" | `unmoderated-maze-usertesting-lyssna` + analytics | Triangulate qual + quant |
| "What do users think of our brand?" | survey via Sprig/Survicate/Typeform + JTBD probe | Don't survey behavioral Qs |

---

## Closing rules

Talk to 5 users, ship. Behavior beats stated intent. Recruitment quality beats sample size. The decision the research informs is non-negotiable.
