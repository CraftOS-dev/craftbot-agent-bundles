# UX Researcher — Source Attribution

Section-to-source map for `soul.md` and `role.md`. **Not** loaded into context — for human verification.

URLs in `agent.yaml → sources` and `reference/INVENTORY.md`. Per-use-case mapping in `reference/SOTA_USE_CASES.md`.

---

## soul.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Title + persona intro + three convictions | Composition synthesis distilling load-bearing rules from Nielsen Norman Group (5-user discount usability), Rob Fitzpatrick "Mom Test" (behavior beats intent), Erika Hall "Just Enough Research" (recruitment quality) | Convictions are well-established in 2025-2026 UX research canon; framing is synthesized |
| Purpose | Synthesis from NN/g + Erika Hall + Marty Cagan + Teresa Torres on the role of research in product decisions | |
| Execution stack | `reference/SOTA_USE_CASES.md` | Every bullet maps to a row in the SOTA table |
| When invoked — Research planning mode | Erika Hall "Just Enough Research" question-first hierarchy + NN/g method matrix | https://www.nngroup.com/articles/which-ux-research-methods/ |
| When invoked — Recruitment mode | User Interviews / Respondent screener guides + Erika Hall recruitment hygiene + NN/g anti-screen guidance | https://www.userinterviews.com/blog/screener-survey-template |
| When invoked — Moderated usability mode | NN/g think-aloud protocol + Krug "Don't Make Me Think" + Nielsen 5-user rule | https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/ + https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/ |
| When invoked — Unmoderated usability mode | Maze + UserTesting + Lyssna platform docs + NN/g unmoderated guidance | https://help.maze.co + https://www.usertesting.com + https://help.lyssna.com |
| When invoked — IA testing mode | NN/g tree testing + card sort + first-click guidance + Optimal Workshop docs | https://www.nngroup.com/articles/tree-testing/ + https://help.optimalworkshop.com |
| When invoked — JTBD interview mode | Bob Moesta switch interview + Tony Ulwick outcome statements + Rob Fitzpatrick Mom Test | https://www.demand-side.com/switch-interview + https://jtbd.info/outcome-statements + https://www.momtestbook.com |
| When invoked — Synthesis mode | Daniel Pidcock atomic UX research + Dovetail synthesis methodology | https://www.atomicresearch.co + https://dovetail.com/blog/atomic-research |
| When invoked — Heuristic + cognitive walkthrough mode | NN/g 10 heuristics + Wharton-Lewis-Polson cognitive walkthrough | https://www.nngroup.com/articles/ten-usability-heuristics/ + https://www.nngroup.com/articles/cognitive-walkthrough/ |
| When invoked — Accessibility research mode | W3C WAI involving users with disabilities + Fable + axe-core/pa11y baseline | https://www.w3.org/WAI/test-evaluate/involving-users/ + https://makeitfable.com + https://www.deque.com/axe/ |
| When invoked — Diary study mode | dscout diary study templates + NN/g longitudinal research guidance | https://dscout.com/people-nerds/diary-study-template + https://www.nngroup.com/articles/diary-studies/ |
| When invoked — ResearchOps mode | Kate Towsey "Research That Scales" + ResearchOps Community | https://researchops.community |
| Core operating rules | Merged: Nielsen Norman Group canon (5-user rule, method matrix, heuristics), Fitzpatrick Mom Test (behavior beats intent, no leading questions), Erika Hall recruitment hygiene, Pidcock atomic UX research, Holtzblatt accessibility (own assistive tech), Krug discount usability | |
| Mode-specific decisions | Per-mode lift from the matching reference (NN/g / Erika Hall / Moesta / Ulwick / Pidcock / Holtzblatt) | |
| Quality gates | Synthesis from NN/g severity scale + Pidcock atomic research model + WCAG 2.2 conformance criteria + Mom Test interview hygiene + Nielsen 5-user rule | |
| Output format | Standard UX research artifact conventions (research plan / screener / discussion guide / readout / persona / journey map) — Notion + Dovetail + Excalidraw native formats | |
| Communication style | NN/g "writing for stakeholders" + Erika Hall "Just Enough Research" + Lenny Rachitsky "outcome-led communication" | |
| When to push back | Synthesis from NN/g UX research anti-patterns + Fitzpatrick Mom Test refusal rules + Erika Hall research-as-theater warnings | https://www.nngroup.com/articles/ux-research-mistakes/ |
| When to defer | Synthesis of CraftBot agent catalog (product-manager, data-analyst, growth-agent, frontend-engineer, marketing-agent) responsibility boundaries | |
| First-conversation routine questions | Standard PROACTIVE.md self-init pattern from `METHODOLOGY.md` with UX-research-specific routine questions | Same wording mechanic across all CraftBot agents |
| Closing rule | Distilled from Nielsen Norman canon + Mom Test + Erika Hall closing principles | |

---

## role.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Capability reference → Research artifact types | Industry canon (NN/g / Erika Hall / Pidcock); standard UX research catalog | |
| Capability reference → Research method matrix | NN/g "When to Use Which UX Research Method" matrix | https://www.nngroup.com/articles/which-ux-research-methods/ |
| Capability reference → Sample size rules | Nielsen 5-user + Optimal Workshop guidance + dscout diary study guides + WCAG accessibility research norms | https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/ |
| Capability reference → Frameworks + canon | Compiled from primary sources: NN/g, Erika Hall, Fitzpatrick, Moesta, Christensen/Ulwick, Torres, Holtzblatt+Beyer, Pidcock, Towsey, Krug, Cooper, Young, WCAG, Wharton-Lewis-Polson, Kohavi, Kahneman | All primary sources cited inline + in SOTA tool sources table |
| Capability reference → Severity scale | Nielsen Norman Group | https://www.nngroup.com/articles/severity-ratings-for-usability-problems/ |
| Capability reference → Sibling-agent boundaries | CraftBot agent catalog | Cross-references to product-manager, data-analyst, growth-agent, frontend-engineer, marketing-agent |
| Research planning playbook (question-first hierarchy + template) | Erika Hall "Just Enough Research" | https://abookapart.com/products/just-enough-research |
| Recruitment playbook (panel routing + screener template + anti-screen rules) | User Interviews + Respondent platform guides + Erika Hall recruitment hygiene + NN/g anti-screen guidance | https://www.userinterviews.com/blog + https://respondent.io/help |
| Moderated usability playbook (think-aloud + Lookback/Zoom+Otter pipelines) | NN/g think-aloud guide + Lookback docs + Otter.ai API docs | https://www.nngroup.com/articles/thinking-aloud-the-1-usability-tool/ |
| Unmoderated usability playbook (platform routing + post-test metrics) | Maze + UserTesting + Lyssna platform docs + SUS / UMUX-Lite primary literature | https://help.maze.co + Brooke 1996 SUS paper |
| IA testing playbook (tree / card sort / first-click / 5-second) | Optimal Workshop docs + NN/g IA testing guides | https://www.nngroup.com/articles/tree-testing/ + https://www.nngroup.com/articles/card-sorting-definition/ |
| JTBD interview playbook (Moesta + Mom Test + Ulwick) | Bob Moesta switch interview + Rob Fitzpatrick Mom Test + Tony Ulwick outcome statements + Christensen JTBD canon | https://www.demand-side.com + https://www.momtestbook.com + https://jtbd.info |
| Synthesis playbook (atomic UX research + tag taxonomy + readout) | Daniel Pidcock atomic UX research model + Dovetail synthesis methodology | https://www.atomicresearch.co + https://dovetail.com/blog/atomic-research |
| Heuristic evaluation playbook (Nielsen 10 + severity + report) | NN/g 10 heuristics + severity guide + report structure | https://www.nngroup.com/articles/ten-usability-heuristics/ + https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/ |
| Cognitive walkthrough playbook (4 questions) | Wharton-Lewis-Polson + NN/g cognitive walkthrough guide | https://www.nngroup.com/articles/cognitive-walkthrough/ |
| Accessibility research playbook (axe/pa11y baseline + Fable + own assistive tech) | W3C WAI + Fable engineering + Deque axe-core + pa11y docs + WCAG 2.2 spec | https://www.w3.org/WAI/test-evaluate/involving-users/ + https://www.w3.org/TR/WCAG22/ + https://www.deque.com/axe/ |
| Diary study playbook (dscout missions) | dscout diary study templates + NN/g longitudinal research | https://dscout.com/people-nerds/diary-study-template |
| Persona authoring playbook (behavioral + tag-grounded) | Alan Cooper goal-directed personas + Indi Young thinking-style personas + NN/g persona guide | https://www.nngroup.com/articles/persona/ + https://indiyoung.com/portfolio/thinking-styles |
| Journey map + service blueprint playbook | NN/g customer journey + service blueprint guides + Holtzblatt influence | https://www.nngroup.com/articles/customer-journey-mapping/ + https://www.nngroup.com/articles/service-blueprints-definition/ |
| Antipattern catalog | Synthesis of NN/g + Mom Test + Erika Hall + Pidcock + WCAG anti-patterns | Specific BAD/GOOD pairs are illustrative composition; each maps to a canonical source |
| SOTA tool reference (per-tool entries) | Per-tool sources cited inline (Dovetail / Maze / Optimal Workshop / etc) | See SOTA tool sources table below |
| SOTA execution playbook (request → skill pack) | Generated from `reference/SOTA_USE_CASES.md` | |

---

## SOTA tool sources (June 2026)

| Tool | Source URL | Used for |
|---|---|---|
| Nielsen Norman Group — UX Research methods | https://www.nngroup.com/articles/which-ux-research-methods/ | Method matrix in `skills/research-planning-objectives-hypotheses/SKILL.md` |
| NN/g — 10 Usability Heuristics | https://www.nngroup.com/articles/ten-usability-heuristics/ | `skills/heuristic-evaluation-nielsen-10/SKILL.md` |
| NN/g — Severity Ratings | https://www.nngroup.com/articles/severity-ratings-for-usability-problems/ | Severity scale in `skills/heuristic-evaluation-nielsen-10/SKILL.md` |
| NN/g — Why You Only Need 5 Users | https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/ | 5-user rule (moderated mode core rule) |
| NN/g — Tree Testing + Card Sorting | https://www.nngroup.com/articles/tree-testing/ + https://www.nngroup.com/articles/card-sorting-definition/ | `skills/tree-testing-card-sort-optimal-workshop/SKILL.md` |
| NN/g — Cognitive Walkthrough | https://www.nngroup.com/articles/cognitive-walkthrough/ | `skills/cognitive-walkthrough/SKILL.md` |
| NN/g — Customer Journey + Service Blueprint | https://www.nngroup.com/articles/customer-journey-mapping/ + https://www.nngroup.com/articles/service-blueprints-definition/ | `skills/customer-journey-service-blueprint/SKILL.md` |
| NN/g — Persona | https://www.nngroup.com/articles/persona/ | `skills/persona-authoring-dovetail/SKILL.md` |
| NN/g — Diary Studies | https://www.nngroup.com/articles/diary-studies/ | `skills/diary-studies-dscout-7-30-day/SKILL.md` |
| Erika Hall — Just Enough Research | https://abookapart.com/products/just-enough-research | `skills/research-planning-objectives-hypotheses/SKILL.md` + `skills/screener-design-recruitment-criteria/SKILL.md` |
| Rob Fitzpatrick — The Mom Test | https://www.momtestbook.com | `skills/jtbd-interview-script-execution/SKILL.md` interview hygiene rules |
| Bob Moesta — Switch Interview | https://www.demand-side.com/switch-interview | `skills/jtbd-interview-script-execution/SKILL.md` |
| Tony Ulwick — Outcome Statements | https://jtbd.info/outcome-statements | `skills/jtbd-interview-script-execution/SKILL.md` + `skills/opportunity-solution-tree-jtbd-outcomes/SKILL.md` |
| Christensen / JTBD canon | https://jobs-to-be-done.com | JTBD framework grounding |
| Teresa Torres — Opportunity Solution Tree | https://www.producttalk.org/opportunity-solution-tree | `skills/opportunity-solution-tree-jtbd-outcomes/SKILL.md` |
| Holtzblatt + Beyer — Contextual Design | https://www.amazon.com/Contextual-Design-Customer-Centered-Interactive-Technologies/dp/1558604111 | `skills/contextual-inquiry-in-context-observation/SKILL.md` |
| Daniel Pidcock — Atomic UX Research | https://www.atomicresearch.co | `skills/dovetail-research-repository/SKILL.md` |
| Kate Towsey — Research That Scales | https://researchops.community | `skills/research-ops-panel-budget/SKILL.md` |
| Wharton-Lewis-Polson Cognitive Walkthrough method | https://en.wikipedia.org/wiki/Cognitive_walkthrough | `skills/cognitive-walkthrough/SKILL.md` |
| Steve Krug — Don't Make Me Think | https://www.amazon.com/Dont-Make-Me-Think-Usability/dp/0321965515 | Plain-language heuristics adjacent |
| Alan Cooper — Goal-Directed Personas / Indi Young — Thinking-Style Personas | https://www.alistapart.com/article/personas-make-users-memorable-for-product-team-members + https://indiyoung.com/portfolio/thinking-styles | `skills/persona-authoring-dovetail/SKILL.md` |
| WCAG 2.2 + W3C WAI | https://www.w3.org/TR/WCAG22/ + https://www.w3.org/WAI/test-evaluate/involving-users/ | `skills/accessibility-research-with-disabilities/SKILL.md` |
| Dovetail v3 API | https://dovetail.com/help/api | `skills/dovetail-research-repository/SKILL.md` + nearly every synthesis-adjacent pack |
| Notably (free alt) | https://notably.ai | Dovetail-equivalent synthesis for users without budget |
| Marvin (AI-first alt) | https://heymarvin.com | Auto-tagging + insight extraction alt |
| Maze API | https://help.maze.co/hc/en-us/articles/maze-api | `skills/unmoderated-maze-usertesting-lyssna/SKILL.md` + `skills/ai-prototype-testing-claude-chatgpt/SKILL.md` |
| UserTesting API | https://www.usertesting.com/api | `skills/unmoderated-maze-usertesting-lyssna/SKILL.md` |
| Lyssna API | https://help.lyssna.com/api | `skills/unmoderated-maze-usertesting-lyssna/SKILL.md` + `skills/first-click-5-second-tests/SKILL.md` |
| Optimal Workshop (Treejack / OptimalSort / Chalkmark) | https://help.optimalworkshop.com/en/articles/2079834-treejack-api | `skills/tree-testing-card-sort-optimal-workshop/SKILL.md` + `skills/first-click-5-second-tests/SKILL.md` |
| UXtweak (alt to Optimal Workshop) | https://www.uxtweak.com/docs/api | Alt to Optimal Workshop |
| User Interviews API | https://www.userinterviews.com/api | `skills/recruit-user-interviews-respondent-dscout/SKILL.md` |
| Respondent API | https://respondent.io/help | `skills/recruit-user-interviews-respondent-dscout/SKILL.md` (B2B specialist) |
| dscout API | https://dscout.com/api | `skills/recruit-user-interviews-respondent-dscout/SKILL.md` + `skills/diary-studies-dscout-7-30-day/SKILL.md` |
| Prolific API | https://docs.prolific.com | `skills/recruit-user-interviews-respondent-dscout/SKILL.md` (academic) |
| Lookback API | https://www.lookback.com/docs/api | `skills/moderated-1on1-usability-think-aloud/SKILL.md` |
| Otter.ai API | https://help.otter.ai/hc/en-us/articles/360062075953-Otter-API | Moderated transcription pipeline |
| tl;dv API | https://tldv.io/integrations | Zoom-native transcription alt |
| Granola | https://www.granola.ai | Mac-native transcription alt |
| OpenAI Whisper | https://github.com/openai/whisper | Local transcription (privacy-sensitive) |
| Sprig API | https://help.sprig.com/hc/en-us/articles/sprig-api | In-product event-triggered surveys |
| Survicate API | https://survicate.com/api | Multi-channel surveys |
| Typeform Create API | https://www.typeform.com/developers/create | Long-form surveys + free intercept fallback |
| FullStory Server API | https://developer.fullstory.com/server/v1 | Session replay (paid) |
| LogRocket API | https://docs.logrocket.com/reference | Session replay alt (paid) |
| Microsoft Clarity | https://clarity.microsoft.com | Session replay free fallback |
| Hotjar API | https://help.hotjar.com/hc/en-us/articles/hotjar-api | Cheap session replay + heatmaps |
| Ethnio API | https://ethn.io/api | In-product intercept recruitment |
| Fable Engineering | https://makeitfable.com | Accessibility research recruitment |
| axe-core CLI + pa11y | https://www.deque.com/axe/devtools + https://pa11y.org | Automated WCAG 2.2 baseline |
| Intercom + Zendesk APIs | https://developers.intercom.com + https://developer.zendesk.com | Support ticket pull → Dovetail |
| Hugging Face embeddings | https://huggingface.co/blog/text-clustering | Embedding-based clustering for high-volume thematic |
| Lenny Rachitsky — JTBD guide + readout templates | https://www.lennysnewsletter.com/p/the-ultimate-guide-to-jtbd | Readout templates + JTBD adjacent |
| Native CraftBot MCPs (notion-mcp / figma-mcp / playwright-mcp / linear-mcp / posthog-mcp / mixpanel-mcp / amplitude-mcp / firecrawl-mcp / gmail-mcp / slack-mcp / google-calendar-mcp / huggingface-mcp / openai-ocr-mcp / mistral-ocr-mcp / brave-search / brightdata-mcp / figma-context-mcp) | `app/config/mcp_config.json` | Per-platform automation surfaces in agent.yaml |

Total: 22 bundled SOTA skill packs + 17 native MCPs + 30+ canonical reference URLs covering ≥95% of USE_CASES.md documented use cases. See `reference/SOTA_USE_CASES.md` for the per-use-case confidence map.

---

## Notes on "authored from synthesis"

Several sections include composition synthesis on top of the referenced material:

- **Three opening convictions in soul.md** — synthesized from three load-bearing rules: Nielsen "talk to 5 users" (5-user rule), Mom Test "behavior beats stated intent" (Fitzpatrick), Erika Hall "recruitment quality > sample size" (Just Enough Research). Triad framing is composed; each conviction is sourced.
- **Research plan template in role.md** — synthesized from Erika Hall question-first hierarchy + NN/g method matrix + Notion standard PM/research plan template patterns. Specific section order is composed; each section maps to a source.
- **Screener template in role.md** — synthesized from User Interviews + Respondent screener guides + Erika Hall anti-screen guidance. Anti-screen list is composed from canonical patterns; each pattern maps to a source.
- **Readout template in role.md** — synthesized from NN/g research report structure + Dovetail insight format + Lenny Rachitsky outcome-led communication. Section order is composed.
- **Persona behavioral structure** — synthesized from NN/g persona guide + Cooper goal-directed personas + Young thinking-style personas. Behavioral grounding + tag-count anchoring is the SOTA convention as of 2026.
- **Antipattern catalog** — composed from NN/g + Mom Test + Erika Hall + Pidcock + WCAG anti-patterns commentary; specific BAD/GOOD pairs are illustrative composition; each pattern maps to a canonical source.
- **First-conversation PROACTIVE.md self-init** — standard pattern from METHODOLOGY.md with UX-research-specific routine questions.

No domain claims, methodology canon, or framework definitions were invented. Nielsen's 10 heuristics, severity scale, 5-user rule, Mom Test rules, Moesta switch interview structure, Ulwick outcome statement format, Holtzblatt 4 principles, Wharton-Lewis-Polson 4 questions, WCAG 2.2 criteria, Pidcock atomic UX research model — all are cited canon.

---

## How to update this agent

1. Re-pull SOTA tool docs (Dovetail / Maze / Optimal Workshop / User Interviews / Respondent / dscout / Prolific / Lookback / Otter / Sprig / FullStory / LogRocket / Fable / Ethnio / Hugging Face) every quarter — SOTA changes monthly.
2. Diff against previous versions; update `reference/SOTA_USE_CASES.md` confidence ratings.
3. Update corresponding sections of `soul.md` and `role.md`.
4. Update this `SOURCES.md` if section names or source URLs changed.
5. Re-run `python verify.py ux-researcher` to confirm structure intact.
6. Re-run `python build.py ux-researcher` to regenerate `dist/ux-researcher.craftbot`.

For canonical UX research reference repos:
- `wshobson/agents` — repull every quarter for any new UX research agent definitions.
- `VoltAgent/awesome-claude-code-subagents` — same cadence.
- `msitarzewski/agency-agents` — same cadence.
- Nielsen Norman Group articles — primary methodology source, repull annually.
- Erika Hall + Fitzpatrick + Moesta + Ulwick + Holtzblatt + Towsey published works — methodology canon, stable across years.
