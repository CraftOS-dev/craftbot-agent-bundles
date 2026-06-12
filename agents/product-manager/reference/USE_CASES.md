# Product Manager — Use Cases

**Tier:** **general** · **Category:** product
**Core job:** End-to-end product management for solo founders and small product teams — PRDs, roadmaps, research synthesis, prioritization, experimentation, OKRs, sprint planning, launches, stakeholder comms.

> Ships with the SOTA product-management stack (Linear / Notion / Figma Dev Mode MCPs + Dovetail / Maze / Amplitude / Mixpanel / PostHog / Statsig / GrowthBook / Lattice / FullStory / LogRocket via `cli-anything` + curl). Executes end-to-end — drafts PRDs, writes them to Notion, files Linear issues, queries analytics, designs experiments, generates stakeholder updates. Not just direct.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### PRDs and specs
- 1-pager PRDs (lightweight, exec-friendly)
- Full PRDs (engineering-ready, full scope + acceptance criteria + tracking spec)
- PRD AI-assistance and review (rubric: clarity, measurable success criteria, scope/non-goal boundary, primary user named)
- Feature specs + acceptance criteria (Given/When/Then format)
- Discovery → delivery handoff packets

### Roadmaps
- Now/Next/Later roadmap building (quarterly cadence)
- Annual roadmap (with explicit hypothesis framing)
- Internal roadmap (Linear roadmap link + all-hands deck)
- External roadmap (Productboard portal, "What's Next" page)
- Cross-team dependency mapping
- Sunsetting features / deprecation planning

### User research
- Customer interview script generation (JTBD + Lenny templates)
- Interview synthesis (transcripts → themes via Dovetail)
- Jobs-to-be-Done research (outcome statements, forces of progress)
- Usability testing (moderated + unmoderated via Maze)
- NPS / CSAT / SUS surveys
- Voice-of-customer (VoC) aggregation across support / sales / surveys / social
- Session replay analysis (qualitative UX + bug insights)

### Prioritization
- RICE scoring (default backlog ranking)
- ICE scoring (default experiment prioritization)
- Kano categorization (basic / performance / excitement / indifferent / reverse)
- MoSCoW (scope cuts under deadline)
- WSJF (SAFe-adjacent shops)
- Opportunity solution tree (Teresa Torres)

### Experimentation
- A/B test hypothesis design + pre-registration
- Sample size + MDE + power + duration calculation
- Multi-variant + holdout + bandit experiments
- Sequential testing setup
- Experiment readout (statistical significance + decision)

### OKRs
- Quarterly + annual OKR drafting (3-5 objectives × 2-4 KRs)
- Stretch calibration (60-70% confidence at start)
- KR auto-tracking from analytics MCPs
- Weekly/biweekly OKR check-ins

### Delivery + execution
- Sprint planning (cycle scoping in Linear)
- Story breakdown (parent + child issues; estimate fitting)
- User story mapping (Patton backbone → walking skeleton → release slices)
- Backlog grooming

### Launches
- Launch tier classification (P0 megalaunch / P1 standard / P2 silent ship)
- Launch checklist (engineering / design / docs / marketing / sales / support / analytics)
- Cross-team coordination
- Post-launch retro (within 2 weeks)
- Release notes (user-facing) + changelog (engineering)

### Stakeholder comms
- Weekly stakeholder updates (Wins / Lowlights / Asks / Plans / Metrics)
- Monthly updates with OKR check-in
- Quarterly board updates
- All-hands decks (pptx)
- Customer-facing change comms

### Strategy
- Annual product strategy doc (Rumelt kernel: diagnosis / guiding policy / coherent actions)
- 7 Powers moat analysis (Helmer)
- North Star metric definition
- Pricing + packaging experiments (Van Westendorp PSM)
- Competitive product teardown (structured analysis)

### Design collaboration
- Figma Dev Mode review (frames, components, design tokens)
- PRD-to-Figma handoff
- Copy writing on frames (defers to design for layout)

### Beta program management
- Lightweight beta via PostHog feature flags + targeted segment
- Full Centercode beta program (tester recruitment, NDA, structured feedback)
- Beta entry + exit criteria

### Feedback loops
- Linear / Productboard insights inbox setup
- Per-source aggregation (Intercom / Zendesk / Gong / Maze / Twitter)
- Weekly theme synthesis

---

## Execution status (SOTA — June 2026)

Every documented use case has a SOTA execution mechanism. Linear/Notion/Figma cover the workspace surface; Dovetail/Maze cover the research surface; Amplitude/Mixpanel/PostHog cover analytics; Statsig/GrowthBook cover experimentation; Lattice covers OKRs; FullStory/LogRocket (+ Clarity free fallback) cover session replay.

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| PRD writing (1-pager + full) | Notion MCP + Linear MCP + Dovetail tag pull | `notion-mcp` + `linear-mcp` + `cli-anything` Dovetail curl |
| PRD AI-assistance and review | Claude vs rubric (problem / hypothesis / primary user / success / scope / non-goals / risks / tracking) | `notion-mcp` read + Claude review pass |
| Roadmap building (now/next/later, quarterly) | Linear initiatives + projects + cycles | `linear-mcp` `create_initiative` + `create_project` |
| Annual roadmap with hypothesis framing | Linear roadmap link + Notion strategy doc | `linear-mcp` + `notion-mcp` |
| Cross-team dependency mapping | Linear initiatives `add_dependency` + RACI in Notion + Excalidraw graph | `linear-mcp` + `excalidraw-diagram-generator` |
| Sunsetting features / deprecation | Analytics MCP (low-usage proof) + Linear deprecation project + customer comms | `amplitude-mcp` / `posthog-mcp` + `linear-mcp` + `gmail-mcp` |
| Customer interview script generation | Lenny + JTBD templates in Notion | `notion-mcp` + script library |
| Interview synthesis | Dovetail v3 — tag-based theme extraction | `cli-anything` curl `https://dovetail.com/api/v1/highlights` |
| JTBD research | Outcome statement framework + Dovetail tagging | `notion-mcp` + Dovetail curl |
| Usability testing (moderated + unmoderated) | Maze API | `cli-anything` curl `https://api.maze.co/v1` |
| NPS / CSAT / SUS surveys | Maze surveys | `cli-anything` Maze API |
| VoC aggregation | Multi-source per-API → Dovetail or Productboard insights | `cli-anything` per source + insights API |
| Session replay analysis | FullStory / LogRocket / Clarity | `cli-anything` curl per platform |
| RICE / ICE / Kano prioritization | Linear custom-field writeback + Maze for Kano | `linear-mcp` + Maze API |
| MoSCoW / WSJF | Linear labels + custom fields | `linear-mcp` `update_issue` |
| A/B test hypothesis + design | Statsig / GrowthBook MCP | Statsig curl OR `npx growthbook-mcp` |
| Sample size + MDE + duration calc | Statsig / GrowthBook calculator endpoint | `cli-anything` curl |
| Multi-variant + holdout + bandit | Statsig (bandit) / GrowthBook (multi-variant) | per-platform MCP |
| Experiment readout | Statsig `/results` / GrowthBook `/results` + Notion doc | per-platform MCP + `notion-mcp` |
| OKR drafting and tracking | Lattice Goals API + analytics MCP KR auto-checkin | `cli-anything` Lattice curl + `amplitude-mcp` |
| Weekly OKR check-in | Lattice + Linear cycle status | `cli-anything` Lattice + `linear-mcp` |
| Sprint planning (cycle scoping) | Linear cycles + estimate-weighted velocity | `linear-mcp` `create_cycle` |
| Story breakdown | Linear parent + child issues | `linear-mcp` `bulk_create_issues` |
| User story mapping | Patton backbone in Excalidraw + Linear sync | `excalidraw-diagram-generator` + `linear-mcp` bulk_create |
| Discovery → delivery handoff | Linear issue with PRD/Figma/AC links + cycle | `linear-mcp` + `figma-mcp` + `notion-mcp` |
| Launch coordination (P0/P1/P2) | Linear cross-team project + Notion checklist | `linear-mcp` + `notion-mcp` |
| Release notes (user-facing) | Linear cycle issue list + Notion changelog | `linear-mcp` + `notion-mcp` |
| Engineering changelog | git-cliff from conventional commits | `cli-anything` `git cliff --output CHANGELOG.md` |
| Post-launch retro | Notion retro template + analytics impact | `notion-mcp` + analytics MCP |
| Weekly stakeholder update | Lenny format auto-aggregated (Linear + analytics + Dovetail) | `linear-mcp` + analytics + Dovetail + `notion-mcp` + `gmail-mcp` |
| Monthly / quarterly stakeholder update | Same + OKR check-in section | `linear-mcp` + Lattice + analytics + `notion-mcp` |
| All-hands deck | pptx skill with outcome-led structure | `pptx` |
| Annual strategy doc (Rumelt + 7 Powers) | Notion long-form generation with kernel structure | `notion-mcp` |
| North Star metric definition | Analytics MCP query + Notion doc | analytics MCP + `notion-mcp` |
| Pricing + packaging experiments | Maze Van Westendorp PSM + Statsig/GrowthBook packaging test | Maze API + Statsig/GrowthBook MCP |
| Competitive product teardown | Firecrawl + Playwright + Brave Search + Notion | `firecrawl-mcp` + `playwright-mcp` + `brave-search` + `notion-mcp` |
| Figma Dev Mode review | Figma Dev Mode MCP | `figma-mcp` `get_file_frames`, `get_components` |
| PRD-to-Figma handoff | Linear issue with Figma frame URL | `linear-mcp` + `figma-mcp` |
| Lightweight beta (feature flag) | PostHog feature flags + target_users filter | `posthog-mcp` `feature_flag_create` |
| Full beta program (Centercode) | Centercode API | `cli-anything` curl `https://api.centercode.com/v1` |
| Feedback loop centralization | Linear feedback view OR Productboard insights inbox | `linear-mcp` + per-source curl OR Productboard `/insights` |
| Per-source aggregation (Intercom / Zendesk / Gong / etc) | per-platform OAuth + standardized JSON to insights inbox | `cli-anything` per source |

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Dovetail v3 (research synthesis) | ⚠ | Paid plan ($199/mo+); Notably free alt covers tag-based aggregation |
| Lattice OKR module | ⚠ | Paid HR-stack tool; 15Five Objectives alt; Notion DB fallback if no OKR tool |
| Centercode beta management | ⚠ | Enterprise contract; agent defaults to PostHog feature-flag lightweight beta unless recipient configures Centercode |
| FullStory / LogRocket session replay | ⚠ | Paid plans (>$200/mo); Microsoft Clarity is free fallback (less polished) |
| Per-source OAuth (Intercom / Zendesk / Gong / Maze etc) | ⚠ | Each platform requires its own one-time OAuth; afterwards fully automated |
| Productboard external roadmap portal | ⚠ | Paid plan; agent uses Linear roadmap shared link as default |
| ChatPRD / Kraftful AI PRD review | ⚠ | Optional — agent's `notion-prds-roadmaps` skill implements the same rubric directly via Claude |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a concrete execution path. The ⚠ rows are all paid SaaS the recipient owns (or free alternatives ship by default). No use case is genuinely impossible.

---

## When to use this agent

- "Write a 1-pager PRD for the notifications center"
- "Build the Q3 roadmap — what should go in now/next/later?"
- "Synthesize these 11 customer interview transcripts into themes"
- "Rank our backlog by RICE and recommend top-3 for next cycle"
- "Design an A/B test for the new onboarding flow — what sample size do we need?"
- "Draft our Q3 OKRs aligned to the activation target"
- "Generate the weekly product update for the exec team"
- "Why is D7 retention dropping among new signups?"
- "Teardown Notion vs Coda vs us — pricing and feature comparison"
- "Plan the launch of feature X for next month"

## When NOT to use this agent

- Marketing positioning / GTM messaging / launch campaigns — hand off to `marketing-agent`
- Sales pipeline analysis / objection prep / sales enablement collateral — hand off to `sales-agent`
- Support theme synthesis / churn driver investigation / help-center content — hand off to `customer-support-agent`
- Deep warehouse SQL or attribution modeling — hand off to `data-analyst` (v1) — until then, do best with `posthog-mcp` HogQL + `postgresql-mcp`
- Engineering scoping decisions / technical RFCs / architecture — hand off to `senior-python-engineer` or `frontend-engineer`
- Visual design / design system work / deep UX research depth — recommend a design specialist (v1)
- Writing technical product documentation (API docs, developer guides) — hand off to `technical-writer`
- Legal / compliance copy that needs legal review — draft, but flag for legal sign-off
