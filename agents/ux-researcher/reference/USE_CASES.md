# UX Researcher — Use Cases

**Tier:** **specialized** · **Category:** product (under `product-manager` parent)
**Core job:** End-to-end UX research craft for product teams — research planning, screener design + panel recruitment, moderated + unmoderated usability testing, IA card sorts + tree tests, JTBD interviews, persona authoring, journey + service-blueprint mapping, heuristic evaluation + cognitive walkthroughs, accessibility research with users with disabilities, diary studies, contextual inquiry + ethnography, Dovetail synthesis + insight repository curation, NPS + support-ticket thematic analysis, ResearchOps panel + budget + tooling.

> Ships with the SOTA UX-research stack (Dovetail / Maze / UserTesting / Lyssna / Optimal Workshop / User Interviews / Respondent / dscout / Prolific / Lookback / Otter / Sprig + axe-core/pa11y + Fable for accessibility + Hugging Face for embedding clustering via `cli-anything` + curl). Executes end-to-end — drafts research plans, designs screeners + pushes to panels, runs moderated + unmoderated sessions, transcribes, tags + synthesizes in Dovetail, authors personas + journey maps, runs heuristic + cognitive walkthroughs. Not just direct.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Research planning + framing
- Research plan authoring (decision-first, ≤5 questions, method by NN/g matrix)
- Hypothesis framing (testable, falsifiable)
- Method picking (behavior vs attitude × qual vs quant × generative vs evaluative)
- Sample size justification (5 for moderated, 50 for tree test, 15-25 for JTBD, etc)
- Stakeholder alignment + sign-off (Erika Hall question-first hierarchy)

### Screener design + recruitment
- Screener generation for User Interviews / Respondent / Prolific
- Anti-screen for professional respondents + industry guards
- 4-platform panel routing (UI / Respondent / dscout / Prolific) by study type
- In-product intercept (Ethnio) when in-house recruit is needed
- Specialized recruit (Fable for accessibility, B2B segments via Respondent)
- Calendly scheduling + Zoom logistics

### Moderated 1:1 research
- Moderated usability tests (think-aloud protocol)
- JTBD switch interviews (Moesta timeline + Mom Test rules)
- Contextual inquiry / ethnographic field research (Holtzblatt 4-principles)
- Generative discovery interviews (problem identification)
- Evaluative interviews (concept testing, solution feedback)
- Lookback + Zoom + Otter.ai pipeline (recording + transcription)

### Unmoderated research
- Maze (Figma prototypes + click maps + heatmaps + SUS)
- UserTesting (enterprise, largest panel, video annotation)
- Lyssna (5-second, first-click, design-first tests)
- Task success + time-on-task + SUS / UMUX-Lite / SEQ measurement
- Multi-step prototype with branching paths

### IA testing
- Tree testing (Treejack — directness + success per task, ≥50 participants)
- Card sorting (OptimalSort — open / closed / hybrid, ≥30 participants)
- First-click testing (Chalkmark heatmap, 30+ participants)
- 5-second tests (Lyssna — recall + first impression)
- IA recommendation reports

### JTBD + outcome-driven research
- JTBD interview script generation (Moesta switch interview structure)
- Outcome statement generation (Ulwick direction + unit + object + context)
- Forces of progress mapping (push / pull / anxiety / habit 2×2)
- Opportunity solution tree authoring (Teresa Torres OST living map)
- Jobs hierarchy mapping

### Persona authoring + journey mapping
- Behavioral personas (tag-grounded from Dovetail; no demographic-only)
- Persona maintenance (refresh from new research)
- Customer journey maps (NN/g format with emotional curve + opportunity zones)
- Service blueprints (frontstage / backstage / support processes)
- Journey map visualization via Excalidraw + Notion narrative

### Heuristic + cognitive walkthrough
- Heuristic evaluation (Nielsen's 10 + severity 0-4)
- Cognitive walkthrough (Wharton-Lewis-Polson 4 questions per step)
- Severity-sorted issue list (severity × frequency × business impact)
- Linear issue handoff for engineering fixes
- Live URL evaluation (Playwright) + Figma prototype evaluation (Figma MCP)

### Accessibility research
- Automated WCAG 2.2 baseline (axe-core + pa11y CLI scans)
- User research with participants with disabilities (Fable + AccessWorks + Knowbility)
- Participants use own assistive tech (screen reader, magnifier, voice control)
- Lived-experience friction reports
- WCAG conformance mapping + fix prioritization

### Diary studies + longitudinal
- dscout missions (7-30 day mobile-first)
- Daily prompt cadence (text / photo / video / screen rec)
- Mid-study check-in interviews
- Longitudinal pattern synthesis (not snapshot)

### Contextual inquiry + ethnography
- On-site observation (homes / offices / retail / mobile-in-context)
- Holtzblatt 4 principles (context / partnership / interpretation / focus)
- Work models (flow / sequence / artifact / cultural / physical)
- Artifact library + thick-description field notes
- Cultural model generation

### Synthesis + repository
- Transcript upload + auto-transcription via Whisper / Otter / tl;dv
- Tag-level coding in Dovetail (atomic UX research model)
- Theme clustering (≤7 themes per study)
- Insight library curation (Pidcock Experiments → Facts → Insights → Conclusions)
- Cross-study pattern detection
- Tag taxonomy maintenance

### NPS + ticket + VoC analysis
- NPS verbatim thematic coding (per-segment: promoter / passive / detractor)
- Support ticket thematic analysis (Intercom / Zendesk / Front)
- Sales call thematic (Gong / Chorus / Fathom — defers depth to sales-agent)
- Voice-of-customer aggregation (multi-source → Dovetail / Productboard)
- Embedding-based clustering (Hugging Face) for high-volume (1000+ items)

### In-product surveys
- Sprig event-triggered micro-surveys
- Survicate multi-channel (email + in-product + link)
- Typeform long-form with branching
- SUS / UMUX-Lite / SEQ post-test surveys
- NPS implementation

### Session replay analysis
- Friction-signal filtered sessions (rage-clicks, dead-clicks, errors)
- FullStory / LogRocket (paid) / Hotjar / Microsoft Clarity (free)
- Qualitative bug + UX insight extraction
- Triangulation with funnel + cohort data

### Research operations
- Consented panel build + maintenance
- Intake form + SLA per request tier
- Tool stack matrix + budget tracking
- Tag taxonomy governance
- Office hours + democratization training (PMs / designers / engineers)

### AI prototype testing
- Maze unmoderated for AI-generated prototypes (Claude artifacts, v0, lovable, bolt)
- Hallucination check (does AI output match user intent?)
- Trust calibration (are users over-trusting AI confidence?)
- AI-specific friction patterns

### Research democratization + training
- Notion training wiki (research basics that don't suck)
- Mom Test interview rules cheat sheet
- "When to call a researcher" escalation matrix
- pptx kickoff deck + office hours cadence

### Stakeholder readouts
- Research repo entries (Notion narrative + Dovetail evidence)
- Insight + recommendation per theme (no insights without next step)
- Executive briefs (1-page TL;DR + decision recommendation)
- All-hands readout decks (pptx)

---

## Execution status (SOTA — June 2026)

Every documented use case has a SOTA execution mechanism. Dovetail / Notably / Marvin cover the repository surface; Maze / UserTesting / Lyssna cover unmoderated; Lookback + Otter / Zoom cover moderated; Optimal Workshop covers IA; User Interviews / Respondent / dscout / Prolific cover recruitment; Fable + axe-core + pa11y cover accessibility; Hugging Face covers high-volume embedding-based clustering.

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Research plan authoring | NN/g method matrix + Erika Hall question-first hierarchy + Notion template | `notion-mcp` + Dovetail project create |
| Hypothesis framing | Falsifiable hypothesis format | Notion plan + sign-off |
| Method picking (behavior vs attitude × qual vs quant) | NN/g UX research methods matrix | Decision rule embedded in `research-planning-objectives-hypotheses` skill |
| Sample size justification | Per-method minimums (Nielsen 5; Treejack 50; etc) | Documented in role.md |
| Screener generation | User Interviews / Respondent question libraries | `notion-mcp` + `cli-anything` curl per platform |
| Anti-screen for professional respondents | Industry guard + behavior guard | Skill pack template |
| Panel recruitment (UI) | User Interviews API | `cli-anything` curl `https://api.userinterviews.com/v1` |
| Panel recruitment (Respondent) | Respondent API for B2B specialist | `cli-anything` curl `https://api.respondent.io/v1` |
| Panel recruitment (dscout) | dscout API for mobile + diary | `cli-anything` curl `https://dscout.com/api/v1` |
| Panel recruitment (Prolific) | Prolific API for academic + survey | `cli-anything` curl `https://api.prolific.com` |
| In-product intercept (Ethnio) | Ethnio banner → screener → session | `cli-anything` curl `https://ethn.io/api/v1` |
| Calendly scheduling + Zoom | Calendly API + Zoom integration | `calendly-api` skill |
| Moderated usability (Lookback) | Lookback purpose-built moderated | `cli-anything` curl Lookback |
| Moderated usability (Zoom + Otter alt) | Zoom + Otter.ai pipeline | `google-calendar-mcp` + Otter curl |
| Live transcription (Otter / tl;dv / Granola / Whisper) | Route per platform | Otter curl + tl;dv curl + `openai-whisper-api` skill |
| JTBD switch interview | Moesta + Ulwick outcomes + Mom Test | `notion-mcp` + Dovetail tagging |
| Contextual inquiry / ethnography | Holtzblatt 4 principles + work models | `notion-mcp` + Otter + Dovetail |
| Generative + evaluative interviews | Standard interview structures | Skill pack templates |
| Unmoderated (Maze) | Maze API (Figma + click maps + SUS) | `cli-anything` curl `https://api.maze.co/v1` |
| Unmoderated (UserTesting) | UserTesting API (enterprise) | `cli-anything` curl `https://api.usertesting.com/v1` |
| Unmoderated (Lyssna) | Lyssna API (5-second + design tests) | `cli-anything` curl `https://api.lyssna.com/v1` |
| Tree testing | Treejack (Optimal Workshop) | `cli-anything` curl `https://api.optimalworkshop.com/v1/treejack` |
| Card sorting (open / closed / hybrid) | OptimalSort | `cli-anything` curl `https://api.optimalworkshop.com/v1/optimalsort` |
| First-click testing | Chalkmark | `cli-anything` curl `https://api.optimalworkshop.com/v1/chalkmark` |
| 5-second tests | Lyssna 5-second test | `cli-anything` curl Lyssna |
| Outcome statement generation (Ulwick) | direction + unit + object + context format | Skill pack template |
| Forces of progress mapping | push / pull / anxiety / habit 2×2 | `excalidraw-diagram-generator` + Dovetail tag counts |
| Opportunity solution tree | Teresa Torres OST | `excalidraw-diagram-generator` + `linear-mcp` |
| Behavioral persona authoring | Tag-grounded from Dovetail | Dovetail curl + `notion-mcp` |
| Persona maintenance | Refresh from new research | Same path |
| Customer journey map | NN/g format + emotional curve + opportunities | `excalidraw-diagram-generator` + `notion-mcp` |
| Service blueprint | Frontstage / backstage / support | `excalidraw-diagram-generator` + `notion-mcp` |
| Heuristic evaluation | Nielsen 10 + severity 0-4 | `playwright-mcp` + `figma-mcp` + `notion-mcp` |
| Cognitive walkthrough | Wharton-Lewis-Polson 4 questions | `figma-mcp` + `playwright-mcp` + `notion-mcp` |
| WCAG 2.2 automated baseline | axe-core + pa11y CLI scans | `cli-anything` `npx @axe-core/cli + npx pa11y` |
| Accessibility user research | Fable + AccessWorks + Knowbility recruit | `cli-anything` curl Fable |
| Diary studies (7-30 day) | dscout missions | `cli-anything` curl dscout |
| Tag-level synthesis (Dovetail) | Atomic UX research model | `cli-anything` curl Dovetail |
| Tag-level synthesis (Notably alt) | Free fallback | `cli-anything` curl Notably |
| Theme clustering | ≤7 themes per study | Skill pack methodology |
| Insight library curation | Pidcock atomic UX research | Dovetail + `notion-mcp` |
| Cross-study pattern detection | Tag taxonomy queries | Dovetail curl |
| NPS verbatim coding | Per-segment promoter / passive / detractor | `cli-anything` per NPS tool + Dovetail |
| Support ticket thematic | Intercom / Zendesk / Front → Dovetail | `cli-anything` per platform + Dovetail |
| Embedding-based clustering (high volume) | Hugging Face embeddings + UMAP + HDBSCAN | `huggingface-mcp` |
| In-product surveys (Sprig) | Event-triggered micro-surveys | `cli-anything` curl `https://api.sprig.com/v1` |
| In-product surveys (Survicate) | Multi-channel surveys | `cli-anything` curl Survicate |
| Long-form surveys (Typeform) | Branching logic | `cli-anything` curl Typeform |
| Session replay (FullStory) | Friction-signal filtered sessions | `cli-anything` curl FullStory |
| Session replay (LogRocket) | Same | `cli-anything` curl LogRocket |
| Session replay (Hotjar) | Cheap option | `cli-anything` curl Hotjar |
| Session replay (Clarity, free) | Free fallback | Dashboard export |
| ResearchOps wiki + intake | Kate Towsey playbook | `notion-mcp` |
| Tag taxonomy governance | Dovetail admin endpoints | `cli-anything` curl Dovetail |
| Panel budget tracking | Spreadsheet or finance MCP | `xlsx` skill or `xero-mcp` |
| Office hours + training | Calendly + Notion wiki | `gmail-mcp` + `notion-mcp` |
| Research democratization | Notion wiki + cheat sheets + pptx | `notion-mcp` + `pptx` |
| AI prototype testing | Maze with hallucination + trust gates | Maze API + skill pack rubric |
| Stakeholder readout (insight + rec) | Notion narrative + Dovetail evidence + Linear handoff | `notion-mcp` + `linear-mcp` |
| Executive brief | 1-page TL;DR + decision recommendation | `notion-mcp` + `pdf` skill |
| All-hands readout deck | pptx with outcome structure | `pptx` skill |

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Dovetail v3 (research repository) | ⚠ | Paid plan ($199/mo+); Notably (free) is immediate fallback, Marvin (AI-first) is alt |
| Optimal Workshop (Treejack / OptimalSort / Chalkmark) | ⚠ | Paid plan (~$166/mo Pro); UXtweak is cheaper alt; manual Google Sheets export for solo studies |
| dscout diary studies | ⚠ | Paid per-participant; Typeform + email cadence is lightweight free alt |
| Fable accessibility panel | ⚠ | Specialized recruit fee per session; axe-core/pa11y automated baseline ships free; general User Interviews with disability self-disclosure is fallback |
| FullStory / LogRocket session replay | ⚠ | Paid plans (>$200/mo); Microsoft Clarity is free fallback |
| Lookback moderated platform | ⚠ | Paid plan; Zoom + Otter.ai pipeline is free/cheap alt |
| Ethnio intercept | ⚠ | Paid plan; Typeform banner is free fallback |
| User Interviews / Respondent / dscout / Prolific panels | ⚠ | Paid per recruit (recipient owns spend) |
| Per-platform OAuth (Intercom / Zendesk / Front / HelpScout) | ⚠ | Each requires one-time OAuth/API key; afterwards fully automated |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a concrete execution path. The ⚠ rows are all paid SaaS the recipient owns (or free alternatives ship by default). No use case is genuinely impossible.

---

## When to use this agent

- "Plan a study to understand why D7 retention dropped among solo founders"
- "Recruit 5 PMs at B2B SaaS companies who have used our competitor for a moderated session next week"
- "Write the screener for a study on inbox-overload pain — anti-screen for market researchers"
- "Run a tree test on our proposed new IA — 50 participants, 6 tasks"
- "Synthesize these 12 interview transcripts into themes with verbatim quotes"
- "Author a persona for solo founders grounded in our last 15 customer interviews"
- "Heuristic-evaluate our new onboarding flow against Nielsen's 10"
- "Run a 14-day diary study on how our power users plan their week"
- "Set up our ResearchOps function — panel, intake form, tool stack, taxonomy"
- "Test this Claude-generated prototype for hallucination + user trust"
- "Build a customer journey map for the trial-to-paid conversion using interview data + analytics"
- "Code these 200 NPS comments by theme per segment (promoter / passive / detractor)"

## When NOT to use this agent

- Roadmap decisions and prioritization based on research → hand off to `product-manager` (parent agent — you provide the data, PM decides)
- Deep funnel SQL or attribution modeling → hand off to `data-analyst` (you provide qualitative why; they provide quantitative what)
- A/B test design + run + readout → hand off to `growth-agent` (you hand them hypothesis from research; they design + run the test)
- Prototype build (React, Figma → code) for what you're testing → hand off to `frontend-engineer`
- Marketing positioning / GTM copy testing depth → hand off to `marketing-agent` (you can still run the test if needed)
- Sales call thematic + objection synthesis → hand off to `sales-agent` (you do customer-job extraction from sales calls; they do sales-process insights)
- Support ops theme synthesis at depth → hand off to `customer-support-agent` (you do thematic coding if it feeds research)
- Technical documentation writing → hand off to `technical-writer`
- Legal/compliance review of research consent / GDPR setup → flag for legal review
