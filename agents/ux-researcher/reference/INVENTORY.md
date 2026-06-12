# ux-researcher — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research and the seed list in the build prompt (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`).

For future tightening: pull 4-6 reference agents from `wshobson/agents` (ux-researcher, user-researcher, research-ops), `VoltAgent/awesome-claude-code-subagents` (categories/08-business-product/ux-researcher), `msitarzewski/agency-agents` (product/ux-researcher, design/user-research), and `vijaythecoder/awesome-claude-agents` into `reference/agents/`. Pull 6-10 reference skills (research-planning, screener-design, dovetail-synthesis, tree-test-analysis, jtbd-interview-coaching, etc.) into `reference/skills/`.

## Reference Agents (planned for v2)

| File | Source | Status |
|---|---|---|
| `agents/wshobson-ux-researcher.md` | https://github.com/wshobson/agents/tree/main/plugins/product-management/agents | not downloaded |
| `agents/voltagent-ux-researcher.md` | https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/ux-researcher.md | not downloaded |
| `agents/msitarzewski-ux-researcher.md` | https://github.com/msitarzewski/agency-agents/blob/main/design/ux-researcher.md | not downloaded |
| `agents/msitarzewski-user-research.md` | https://github.com/msitarzewski/agency-agents/blob/main/design/user-research.md | not downloaded |

## SOTA Research Sources (used in v1 build)

The SOTA mapping in `SOTA_USE_CASES.md` is grounded in 2025-2026 UX research practice across these published references (full URLs in `SOTA_USE_CASES.md` and `SOURCES.md`):

- Dovetail v3 + Notably + Marvin AI research repositories (dovetail.com, notably.ai, heymarvin.com)
- Maze API (moderated + unmoderated + tree test + first click + 5-second test) (maze.co)
- UserTesting + Lyssna + Userlytics (usertesting.com, lyssna.com)
- User Interviews + Respondent + Prolific + dscout panel recruitment (userinterviews.com, respondent.io, prolific.com, dscout.com)
- Optimal Workshop tree test + card sort + first-click (optimalworkshop.com)
- UXtweak research tools (uxtweak.com)
- Sprig + Survicate + Typeform in-product surveys (sprig.com, survicate.com)
- FullStory + LogRocket + Microsoft Clarity + Hotjar session intelligence
- Lookback + Zoom moderated sessions (lookback.io)
- Otter.ai + Granola + tl;dv + Whisper transcription
- Ethnio in-product intercept recruitment (ethn.io)
- Jobs-to-be-Done canon (Christensen + Ulwick + Bob Moesta)
- Rob Fitzpatrick "The Mom Test" + Teresa Torres continuous discovery
- Erika Hall "Just Enough Research"
- Nielsen Norman Group heuristics + research methodology
- Steve Krug "Don't Make Me Think" + cognitive walkthrough
- WCAG 2.2 + Microsoft Inclusive Design + accessibility research with disabilities
- ResearchOps Community + Kate Towsey "Research That Scales"

## Sources Considered But Not Downloaded

| Source | Why excluded |
|---|---|
| Aurelius, Condens, EnjoyHQ, Iterate research repositories | Dovetail / Notably / Marvin cover the SOTA repository surface; alternatives covered via cli-anything for users on those platforms |
| Discuss.io, Validately | Lookback + Zoom moderated coverage; Discuss.io is adjacent for paid market research |
| Pollfish | Prolific + User Interviews cover the academic + general panel surfaces |
| Userpilot, Pendo (product tours, not research) | In-product guides, not research; out of scope for ux-researcher |
| Hotjar Surveys (separate from heatmaps) | Sprig + Survicate cover the in-product survey surface more cleanly in 2026 |
| Smartlook | FullStory + LogRocket + Clarity cover the session-replay surface |
| UXPin, ProtoPie (prototype-only tools) | Figma covers the prototype-testing surface for moderated walkthroughs |

---

**v1 build approach:** SOTA-driven from published 2025-2026 sources. The agent ships with strong execution paths for every documented use case via Dovetail / Maze / Optimal Workshop / User Interviews / Sprig / FullStory + Clarity + Otter / Whisper + JTBD/Mom Test/Nielsen heuristics canon + `cli-anything` + curl for any remaining gap. Recruitment, screener, moderation, synthesis, IA testing, accessibility research, diary studies, ResearchOps tooling all have named SOTA execution paths.
