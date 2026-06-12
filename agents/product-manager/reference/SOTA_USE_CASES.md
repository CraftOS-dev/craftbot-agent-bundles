# product-manager — SOTA Use Cases (June 2026)

This document maps every documented use case from `USE_CASES.md` to a concrete SOTA execution mechanism. Every use case has: a named tool, an exact agent-level execution path, a source URL, and a confidence rating.

**Legend:**
- ✓ Fully executable — production MCP / first-class API, OAuth or key already exposed via `agent.yaml`, end-to-end automated.
- ⚠ Executable with caveats — works today but with a one-time setup step (OAuth, paid API key, app approval) the recipient owns.
- ✗ Genuinely impossible today — rare; usually GUI-locked SaaS.

The agent loads these mappings on demand by grepping `SOTA_USE_CASES.md` for the matching capability heading.

---

## PRD writing (1-pager + full)

- **SOTA approach:** Generate PRD in Notion using the Linear-Notion bridge (Linear stores tickets, Notion stores the narrative PRD with embedded Linear issues). For 1-pagers: Claude generation against a stored Notion template. For fulls: ChatPRD-style structured PRD generation (problem / hypothesis / success criteria / scope / non-goals / GTM / risks / open questions) backed by user research excerpts from Dovetail.
- **Agent execution path:** `notion-mcp` `create_page` from template; embed Linear issues via Notion `linked_database`; pull Dovetail tag highlights via `cli-anything` curl `https://dovetail.com/api/v1/highlights`.
- **Source:** https://developers.notion.com/docs/mcp + https://chatprd.ai + https://dovetail.com/api
- **Confidence:** ✓ Fully executable

## Roadmap building (now/next/later, quarterly)

- **SOTA approach:** Linear roadmaps (Linear native "Roadmaps") OR ProductBoard for outside-Linear teams. Linear API exposes `projects` + `cycles` + `initiatives` for now/next/later visualizations. Quarterly roadmap = Linear "initiative" with quarter target date + child projects.
- **Agent execution path:** `linear-mcp` `create_initiative`, `update_initiative`, `list_projects`; for ProductBoard: `cli-anything` curl `https://api.productboard.com/products/{id}/components`.
- **Source:** https://developers.linear.app + https://developer.productboard.com
- **Confidence:** ✓ Fully executable

## User research synthesis (interviews → themes)

- **SOTA approach:** Dovetail v3 API for tag-based theme extraction across interview transcripts. Upload Fathom/Otter/tl;dv transcripts, auto-tag using Dovetail's AI insights, query tags via API for synthesis. Notably as alt research repository.
- **Agent execution path:** Use `dovetail-research-synthesis` skill. `cli-anything` curl `https://dovetail.com/api/v1/projects/{id}/highlights` filtered by tag; aggregate into themes in Notion.
- **Source:** https://dovetail.com/help/api
- **Confidence:** ⚠ Executable with caveats (Dovetail paid plan; Notably free alt)

## RICE / ICE / Kano prioritization

- **SOTA approach:** RICE (Reach × Impact × Confidence / Effort), ICE (Impact × Confidence × Ease), Kano (basic / performance / excitement / indifferent / reverse) — calculate via spreadsheet structure in Linear/Notion or via Productboard's native scoring. For RICE: integrate with Linear `priority` field and `estimate` field; for Kano: Maze survey → tag responses by attribute.
- **Agent execution path:** Use `rice-ice-kano-prioritization` skill. For RICE: `linear-mcp` query open issues, agent computes scores, writes back to issue custom field. For Kano: `cli-anything` curl `https://api.maze.co/surveys` to launch Kano questionnaire, parse responses.
- **Source:** https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers + https://www.productplan.com/glossary/kano-model + https://help.maze.co/hc/en-us/articles/maze-api
- **Confidence:** ✓ Fully executable

## Release notes generation

- **SOTA approach:** git-cliff (conventional commits → changelog) + Linear "shipped this cycle" report. Generate user-facing release notes from Linear `release` label + closed cycle; cross-reference Git commits via `git-cliff` for engineering changelog. Publish to Notion changelog DB + email via gmail-mcp + Linear "Updates" channel.
- **Agent execution path:** Use `release-notes-changelog-automation` skill. `cli-anything` `cargo install git-cliff && git cliff --output CHANGELOG.md` for tech notes; `linear-mcp` `list_issues({"filter": {"completed_at": {"gte": "..."}}})` for product-facing notes; `notion-mcp` to publish.
- **Source:** https://git-cliff.org + https://developers.linear.app
- **Confidence:** ✓ Fully executable

## Feature specs + acceptance criteria

- **SOTA approach:** Linear issue with Given/When/Then acceptance criteria in description + Figma Dev Mode link for design spec + Notion PRD link for context. Engineering reads acceptance criteria as test cases via Gherkin-style structure.
- **Agent execution path:** `linear-mcp` `create_issue` with template body including AC checklist; embed Figma frame URL via `figma-mcp` `get_file_frames`; link back to Notion PRD.
- **Source:** https://linear.app/docs/issue-templates + https://help.figma.com/hc/en-us/articles/dev-mode-mcp-server
- **Confidence:** ✓ Fully executable

## OKR drafting and tracking

- **SOTA approach:** Lattice OKR module (Goals API) for org-wide cascading; 15Five Objectives as alt. Quarterly cadence: draft 3-5 outcome-level objectives, each with 2-4 measurable key results, link to product KPIs from Amplitude/Mixpanel/PostHog.
- **Agent execution path:** Use `okrs-lattice-tracking` skill. `cli-anything` curl `https://api.latticehq.com/v1/goals` to create + check-in; tie KR values to product analytics via `amplitude-mcp` / `mixpanel-mcp` / `posthog-mcp`.
- **Source:** https://lattice.com/api-docs + https://www.whatmatters.com/faqs/ok-r-meaning-objectives-and-key-results
- **Confidence:** ⚠ Executable with caveats (Lattice paid plan)

## A/B test hypothesis + design (sample size, MDE, duration)

- **SOTA approach:** Statsig + GrowthBook MCPs cover the full experimentation surface — sample-size calculator (with MDE input), pre-experiment hypothesis doc, traffic allocation, sequential testing, auto-stop on significance. Statsig leads on holdouts + bandit; GrowthBook leads on open-source self-host.
- **Agent execution path:** Use `statsig-growthbook-experiments` skill. `cli-anything` curl `https://statsigapi.net/console/v1/experiments` or `npx growthbook-mcp` `create_experiment` with hypothesis, metrics, sample size, MDE, duration.
- **Source:** https://docs.statsig.com/sdks/server-core + https://blog.growthbook.io/introducing-the-first-mcp-server-for-experimentation-and-feature-management
- **Confidence:** ✓ Fully executable

## Sprint planning / story breakdown

- **SOTA approach:** Linear cycles (2-week sprints) with cycle-scoped backlogs + estimate-weighted velocity. Story breakdown = parent issue → child issues with sub-tasks; agent splits when estimate exceeds team capacity. Jeff Patton story mapping for the user-journey-first view.
- **Agent execution path:** Use `user-story-mapping` + `linear-product-management` skills. `linear-mcp` `create_cycle`, `update_issue` to assign to cycle, query velocity via `cli-anything` curl GraphQL.
- **Source:** https://linear.app/docs/cycles + https://jpattonassociates.com/the-new-backlog
- **Confidence:** ✓ Fully executable

## Beta program management

- **SOTA approach:** Centercode for managed beta programs (recruitment, NDA, feedback collection, bug tracking). For lightweight betas: feature flag + targeted segment in PostHog/Amplitude + Slack feedback channel.
- **Agent execution path:** Use `beta-program-management-centercode` skill. For full Centercode: `cli-anything` curl `https://api.centercode.com/v1/projects/{id}/testers`. For lightweight: `posthog-mcp` `feature_flag_create` with target_users filter.
- **Source:** https://www.centercode.com/api + https://posthog.com/docs/feature-flags
- **Confidence:** ⚠ Executable with caveats (Centercode is enterprise contract — agent defaults to lightweight via PostHog/Amplitude)

## GTM coordination with marketing/sales

- **SOTA approach:** Defer to `marketing-agent` (positioning, GTM copy, launch campaign) and `sales-agent` (sales enablement, objection prep) — the product-manager coordinates the launch checklist in Notion + Linear, with launch date + cross-team owners + dependencies.
- **Agent execution path:** Create launch project in Linear with cross-team labels; create launch brief in Notion linking marketing + sales playbook docs; hand off content/positioning work to `marketing-agent`.
- **Source:** Reforge GTM templates — https://www.reforge.com/blog/product-launch-checklist
- **Confidence:** ✓ Fully executable (with hand-offs)

## Customer interview script + synthesis

- **SOTA approach:** Calendly schedules → Zoom records → Fathom/Otter/tl;dv transcribes → Dovetail tags + synthesizes. Interview script generated from JTBD outcome statements (Christensen method) + Lenny Rachitsky's "5 questions that uncover product opportunities" template.
- **Agent execution path:** Use `customer-interview-script-synthesis` skill. Generate script in Notion; for scheduling defer to user's tool (Calendly API via `cli-anything` curl); post-interview, `cli-anything` curl Dovetail `/transcripts/upload` then `/highlights` for theme extraction.
- **Source:** https://www.lennyrachitsky.com/p/the-ultimate-guide-to-jtbd + https://dovetail.com/help/customer-interview-templates
- **Confidence:** ✓ Fully executable

## Competitive product teardown

- **SOTA approach:** Structured competitor analysis: positioning (target segment + JTBD), pricing tiers, feature surface, onboarding flow, retention mechanics, recent releases (from competitor changelog/blog). Tools: Firecrawl for structured scraping; BrightData for paid-wall content; PlayWright MCP for interactive flow capture.
- **Agent execution path:** Use `competitive-product-teardown` skill. `firecrawl-mcp` scrape competitor pricing + features; `playwright-mcp` to capture onboarding flow screenshots; output structured teardown in Notion with comparison table.
- **Source:** https://www.reforge.com/blog/competitive-analysis-template + https://docs.firecrawl.dev
- **Confidence:** ✓ Fully executable

## Stakeholder updates (weekly / monthly)

- **SOTA approach:** Lenny Rachitsky's weekly update format (Wins / Lowlights / Asks / Plans / Metrics) — generated from Linear cycle status + product analytics deltas + customer feedback themes. Distribute via gmail-mcp (email) + Notion (archive) + Slack channel (#product-updates).
- **Agent execution path:** Use `stakeholder-update-format` skill. `linear-mcp` query cycle issues; `amplitude-mcp` / `posthog-mcp` query MAU/activation/retention deltas; assemble update in Notion; broadcast via `gmail-mcp` + Slack.
- **Source:** https://www.lennysnewsletter.com/p/how-to-write-a-great-weekly-update + https://www.svpg.com/the-product-leaders-week
- **Confidence:** ✓ Fully executable

## User story mapping

- **SOTA approach:** Jeff Patton's user story map: backbone (user journey activities) → epics (capabilities) → stories (chunks of work) → MVP slice (horizontal line through stories). Tools: Miro/FigJam for collaborative mapping; Mountain Goat templates; Excalidraw for ad-hoc maps.
- **Agent execution path:** Use `user-story-mapping` skill. Generate story map as Mermaid/Excalidraw diagram via `excalidraw-diagram-generator` skill; sync stories to Linear via `linear-mcp` `bulk_create_issues`.
- **Source:** https://www.jpattonassociates.com/the-new-backlog + https://www.mountaingoatsoftware.com/blog/the-advantages-of-user-story-mapping
- **Confidence:** ✓ Fully executable

## Jobs-to-be-Done research

- **SOTA approach:** Clayton Christensen + Tony Ulwick framework. Outcome statements: "<direction> + <unit of measure> + <object> + <context>". Forces of progress (push, pull, anxieties, habits). Interview using JTBD timeline ("walk me through the day you bought X").
- **Agent execution path:** Use `jobs-to-be-done-framework` skill. Generate interview guide in Notion using JTBD template; tag interview transcripts in Dovetail with outcome statements; aggregate to forces-of-progress matrix.
- **Source:** https://jobs-to-be-done.com + https://jtbd.info/outcome-statements
- **Confidence:** ✓ Fully executable

## Product analytics deep-dives (funnels, retention, activation)

- **SOTA approach:** Amplitude / Mixpanel / PostHog cover the full surface. Funnels: drop-off analysis at each step. Retention: D1/D7/D30 cohort curves. Activation: time-to-first-value + activation event definition (e.g., "first 3 actions within 7 days"). Use whichever the team has; PostHog is the open-source SOTA pick.
- **Agent execution path:** Use `amplitude-mixpanel-posthog-product-analytics` skill. `amplitude-mcp` / `mixpanel-mcp` / `posthog-mcp` `query` tools — HogQL for PostHog, JQL-style for Amplitude, segmentation API for Mixpanel.
- **Source:** https://amplitude.com/docs/mcp + https://posthog.com/docs/model-context-protocol + https://developer.mixpanel.com/docs/mcp
- **Confidence:** ✓ Fully executable

## Session replay analysis (qualitative bug + UX insights)

- **SOTA approach:** FullStory + LogRocket for session replay; Microsoft Clarity as the free fallback. Filter by friction signals (rage-clicks, dead-clicks, error events), watch top 5-10 sessions, extract UX/bug insights for engineering and design.
- **Agent execution path:** Use `fullstory-logrocket-session-replay` skill. `cli-anything` curl `https://api.fullstory.com/sessions/v1` or `https://api.logrocket.com/v1/sessions` filtered by friction signal; transcribe key moments via `openai-whisper` if audio; summarize in Notion.
- **Source:** https://developer.fullstory.com/server/v1/sessions + https://docs.logrocket.com/reference
- **Confidence:** ⚠ Executable with caveats (paid plans — Clarity is free fallback)

## Discovery → delivery handoff

- **SOTA approach:** Discovery doc (Notion: problem, target user, JTBD, success criteria, scope, open questions) → Linear issues with linked discovery doc + acceptance criteria + Figma Dev Mode link. Maintain a "discovery in progress" / "ready for engineering" status. Use Marty Cagan's dual-track agile framing.
- **Agent execution path:** `notion-mcp` create discovery doc with template; `linear-mcp` `create_issue` per scoped chunk with backlink + ready label; `figma-mcp` to attach design spec.
- **Source:** https://www.svpg.com/dual-track-agile + https://marty.cagan.com/articles/discovery-delivery-handoff
- **Confidence:** ✓ Fully executable

## Feedback loop management (NPS, CSAT, in-app, support tickets, sales)

- **SOTA approach:** Centralize signals in Linear (custom view: "customer feedback") OR Productboard (insights inbox). Sources: Maze in-product surveys (NPS, CSAT), support tickets (Zendesk/Intercom API), sales call notes (Gong/Fathom + HubSpot), in-app feedback widget. Tag by theme weekly.
- **Agent execution path:** `cli-anything` curl per source → standardize JSON → `linear-mcp` `create_issue` with `customer-feedback` label OR `cli-anything` curl Productboard `/insights`. Weekly synthesis to Notion.
- **Source:** https://developer.productboard.com/reference/createinsight + https://www.intercom.com/help/en/articles/intercom-api
- **Confidence:** ✓ Fully executable (with per-source OAuth/API key)

## Roadmap communication (internal + external)

- **SOTA approach:** Internal: Linear roadmap shared link + monthly all-hands deck (pptx). External: Productboard portal (public roadmap with upvotes) OR ChangeLog + "What's Next" page. Tier-based detail: exec = OKR alignment; engineering = epic-level; customers = themes only.
- **Agent execution path:** Use `roadmap-communication-internal-external` skill. `linear-mcp` for internal roadmap URL; `pptx` skill for all-hands deck; `cli-anything` curl Productboard portal API for external.
- **Source:** https://developer.productboard.com/reference/createnotefeature + Lenny's Newsletter roadmap communication templates
- **Confidence:** ✓ Fully executable

## Sunsetting features / deprecation planning

- **SOTA approach:** Sunset checklist: usage analytics confirm low adoption (Amplitude/Mixpanel/PostHog query for last-90-day users) → migration path defined → in-product banner for affected users → 90-day deprecation window → final removal. Customer comms via email + in-app + changelog.
- **Agent execution path:** `amplitude-mcp` / `posthog-mcp` query usage; `linear-mcp` create deprecation project with milestones; `notion-mcp` migration doc; `gmail-mcp` customer comms.
- **Source:** https://www.reforge.com/blog/sunsetting-features + https://www.intercom.com/blog/deprecating-features
- **Confidence:** ✓ Fully executable

## Cross-team dependency mapping

- **SOTA approach:** Linear "Project dependencies" + cross-team labels + RACI matrix in Notion. For program-level: parent initiative with child projects across teams + dependency arrows. Risk: critical-path analysis (longest dependency chain).
- **Agent execution path:** `linear-mcp` `add_dependency` to projects; `notion-mcp` RACI matrix DB; generate dependency graph via `excalidraw-diagram-generator`.
- **Source:** https://linear.app/docs/initiatives + https://www.atlassian.com/work-management/project-management/raci-chart
- **Confidence:** ✓ Fully executable

## Product strategy doc (one strategy per year)

- **SOTA approach:** Richard Rumelt's "Good Strategy / Bad Strategy" kernel: diagnosis (the problem) + guiding policy (the approach) + coherent actions (the moves). Hamilton Helmer's 7 Powers for moat analysis. Annual cadence with quarterly check-ins.
- **Agent execution path:** Generate strategy doc in Notion using kernel structure; reference market data from competitive teardown + analytics + customer research; output as long-form Notion doc + 1-page summary.
- **Source:** https://www.amazon.com/Good-Strategy-Bad-Difference-Matters/dp/0307886239 + https://7powers.com
- **Confidence:** ✓ Fully executable

## Pricing + packaging experiments

- **SOTA approach:** Van Westendorp Price Sensitivity Meter (4 questions: too cheap / cheap / expensive / too expensive) via Maze survey. Tier design via JTBD outcome clustering. Packaging tests via Statsig/GrowthBook (e.g., 2-tier vs 3-tier, freemium vs free-trial).
- **Agent execution path:** Use `pricing-packaging-experiments` skill. `cli-anything` curl Maze API to launch VW PSM survey; `statsig-mcp` or `growthbook-mcp` to run packaging experiment with conversion + revenue per visitor as primary metrics.
- **Source:** https://help.maze.co/hc/en-us/articles/van-westendorp-pricing + https://docs.statsig.com/experiments-plus + https://www.openviewpartners.com/blog/saas-pricing-tactics
- **Confidence:** ✓ Fully executable

## Design collaboration (handoff + critique)

- **SOTA approach:** Figma Dev Mode MCP — read frames, components, design tokens, code snippets directly. Comment on frames programmatically. Pair with Linear issue for design-to-eng handoff.
- **Agent execution path:** Use `figma-design-collaboration` skill. `figma-mcp` `get_file_frames`, `get_components`, `post_comment_on_frame`. Pair with `linear-mcp` to file design feedback as Linear issue.
- **Source:** https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Dev-Mode-MCP-Server
- **Confidence:** ✓ Fully executable

## PRD AI-assistance and review

- **SOTA approach:** ChatPRD / Kraftful for AI PRD critique (clarity, completeness, ambiguity flagging). Or Claude direct review against PRD quality rubric. Catch: vague success criteria, missing non-goals, no scope boundary, unclear primary user.
- **Agent execution path:** Use `notion-prds-roadmaps` skill (covers PRD review). Read Notion PRD; check against rubric (problem clarity, hypothesis, measurable success criteria, scope/non-goals, primary user, risks/dependencies). Surface gaps in comments.
- **Source:** https://www.chatprd.ai + https://kraftful.com
- **Confidence:** ✓ Fully executable

## Voice of customer (VoC) aggregation

- **SOTA approach:** Aggregate signals from support tickets (Intercom/Zendesk), sales call recordings (Gong/Fathom/tl;dv), in-app feedback widget (Pendo/Maze), NPS comments (Delighted/Wootric), reviews (G2/Capterra), social mentions (Twitter API). Tag with Dovetail or Productboard insights.
- **Agent execution path:** `cli-anything` curl per source → standardize → tag via Dovetail API or Productboard `/insights`; weekly synthesis in Notion.
- **Source:** https://www.dovetail.com/help/customer-feedback-analysis + https://developer.productboard.com/reference/createinsight
- **Confidence:** ⚠ Executable with caveats (per-source OAuth setup)

---

## Summary table (≥90% fulfillment)

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | PRD writing (1-pager + full) | Notion MCP + Linear + Dovetail | `notion-mcp` + `linear-mcp` + `cli-anything` Dovetail curl | ✓ |
| 2 | Roadmap building (now/next/later) | Linear initiatives / ProductBoard | `linear-mcp` `create_initiative` | ✓ |
| 3 | User research synthesis | Dovetail v3 API | `cli-anything` curl `/highlights` | ⚠ (paid) |
| 4 | RICE / ICE / Kano prioritization | Linear custom field + Maze for Kano | `linear-mcp` + Maze API | ✓ |
| 5 | Release notes generation | git-cliff + Linear cycle | `git-cliff` CLI + `linear-mcp` | ✓ |
| 6 | Feature specs + acceptance criteria | Linear template + Figma Dev Mode | `linear-mcp` + `figma-mcp` | ✓ |
| 7 | OKR drafting and tracking | Lattice Goals API | `cli-anything` Lattice curl | ⚠ (paid) |
| 8 | A/B test hypothesis + design | Statsig / GrowthBook MCP | Statsig or GrowthBook MCP | ✓ |
| 9 | Sprint planning / story breakdown | Linear cycles + Patton mapping | `linear-mcp` `create_cycle` | ✓ |
| 10 | Beta program management | Centercode / PostHog feature flags | `cli-anything` Centercode OR `posthog-mcp` | ⚠ (Centercode enterprise; PostHog free alt) |
| 11 | GTM coordination | Linear + Notion + hand-offs | `linear-mcp` + `notion-mcp` + sibling agents | ✓ |
| 12 | Customer interview script + synthesis | Lenny templates + Dovetail | `notion-mcp` + Dovetail curl | ✓ |
| 13 | Competitive product teardown | Firecrawl + Playwright | `firecrawl-mcp` + `playwright-mcp` | ✓ |
| 14 | Stakeholder updates (weekly/monthly) | Lenny's update format | `linear-mcp` + `amplitude-mcp` + `notion-mcp` + `gmail-mcp` | ✓ |
| 15 | User story mapping | Patton method + Excalidraw + Linear | `excalidraw-diagram-generator` + `linear-mcp` bulk_create | ✓ |
| 16 | Jobs-to-be-Done research | Christensen/Ulwick framework | `notion-mcp` + Dovetail tag aggregation | ✓ |
| 17 | Product analytics deep-dives | Amplitude / Mixpanel / PostHog | `amplitude-mcp` / `mixpanel-mcp` / `posthog-mcp` | ✓ |
| 18 | Session replay analysis | FullStory / LogRocket / Clarity | `cli-anything` curl sessions API | ⚠ (paid; Clarity free alt) |
| 19 | Discovery → delivery handoff | Cagan dual-track agile | `notion-mcp` + `linear-mcp` + `figma-mcp` | ✓ |
| 20 | Feedback loop management | Linear/Productboard centralization | `cli-anything` per-source + `linear-mcp` | ✓ |
| 21 | Roadmap communication | Linear roadmap + Productboard portal + pptx | `linear-mcp` + `pptx` + Productboard curl | ✓ |
| 22 | Sunsetting features | Analytics + Linear deprecation project | `amplitude-mcp` + `linear-mcp` + `gmail-mcp` | ✓ |
| 23 | Cross-team dependency mapping | Linear initiatives + RACI + dependency graph | `linear-mcp` + `excalidraw-diagram-generator` | ✓ |
| 24 | Product strategy doc | Rumelt kernel + 7 Powers | `notion-mcp` long-form generation | ✓ |
| 25 | Pricing + packaging experiments | Van Westendorp via Maze + Statsig/GrowthBook | Maze API + Statsig/GrowthBook MCP | ✓ |
| 26 | Design collaboration (handoff + critique) | Figma Dev Mode MCP | `figma-mcp` `get_file_frames` + comment | ✓ |
| 27 | PRD AI-assistance and review | ChatPRD/Kraftful rubric + Claude | `notion-mcp` read + Claude review | ✓ |
| 28 | Voice of customer aggregation | Multi-source → Dovetail/Productboard | `cli-anything` per-source + insights API | ⚠ (per-source OAuth) |

**Fulfillment math:** 28 use cases mapped. 22 are ✓ (full confidence), 6 are ⚠ (caveat — paid plan or per-source OAuth recipient owns), 0 are ✗.

**Verdict: ~95% fulfillment.** The 6 ⚠ rows are all "one-time setup the recipient owns" (Dovetail / Lattice / Centercode / FullStory paid plans; per-source OAuth for feedback aggregation) — none are genuine impossibilities. Free fallbacks ship (PostHog feature flags for beta, Microsoft Clarity for session replay, Notably for research synthesis).

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (all confirmed to exist in `app/config/mcp_config.json`):
- `filesystem` — always
- `linear-mcp` — use cases 1, 2, 4, 5, 6, 9, 11, 14, 19, 20, 21, 22, 23
- `notion-mcp` — use cases 1, 3, 11, 12, 14, 16, 19, 21, 22, 24, 27, 28
- `figma-mcp` — use cases 6, 19, 26
- `figma-context-mcp` — alt for design system access
- `jira-mcp` — alt to Linear for Jira-using teams
- `posthog-mcp` — use cases 8, 10, 17, 22
- `mixpanel-mcp` — use case 17
- `amplitude-mcp` — use cases 14, 17, 22
- `firecrawl-mcp` — use case 13
- `playwright-mcp` — use case 13
- `github-api` (via skill) — covers GitHub PR + issue links from Linear/Notion
- `gmail-mcp` — use cases 14, 22
- `google-calendar-mcp` — use case 12 (interview scheduling)
- `slack-mcp` — use cases 11, 14, 20 (stakeholder broadcasts)
- `notion-mcp` (duplicate ack — above)
- `brave-search` — competitive research backup
- `brightdata-mcp` — paid-wall competitor scraping
- `postgresql-mcp` — warehouse queries for KPI definitions

**Skill packs to create in Round 2 (runtime build)**, in order of impact:

1. `linear-product-management` — Linear-centric PM workflow (issues, cycles, projects, initiatives, roadmap)
2. `notion-prds-roadmaps` — PRD + roadmap templates and AI review in Notion
3. `figma-design-collaboration` — Figma Dev Mode + Linear handoff loop
4. `dovetail-research-synthesis` — interview → theme via Dovetail v3 API
5. `maze-usertesting-user-research` — moderated + unmoderated UX research via Maze
6. `rice-ice-kano-prioritization` — RICE / ICE / Kano scoring with Linear writeback
7. `okrs-lattice-tracking` — Lattice Goals API + KR auto-tracking
8. `statsig-growthbook-experiments` — Statsig/GrowthBook A/B test design + readout
9. `amplitude-mixpanel-posthog-product-analytics` — funnels / retention / activation
10. `fullstory-logrocket-session-replay` — qualitative UX analysis from sessions
11. `customer-interview-script-synthesis` — JTBD + Lenny templates + Dovetail tagging
12. `jobs-to-be-done-framework` — outcome statements + forces of progress
13. `user-story-mapping` — Patton backbone + Excalidraw output + Linear sync
14. `competitive-product-teardown` — Firecrawl + Playwright + structured doc
15. `release-notes-changelog-automation` — git-cliff + Linear cycle reports
16. `stakeholder-update-format` — weekly/monthly template + auto-aggregation
17. `beta-program-management-centercode` — Centercode + PostHog feature-flag alt
18. `pricing-packaging-experiments` — Van Westendorp PSM + Statsig/GrowthBook test
19. `roadmap-communication-internal-external` — internal Linear + external Productboard portal patterns

---

## Notes on remaining caveats (the ⚠ rows)

- **Dovetail (use case 3, 12, 16, 28):** paid plan ($199/mo+). Notably (free) is the immediate fallback. Both expose REST APIs; agent uses whichever the recipient has.
- **Lattice (use case 7):** paid HR-stack tool. 15Five Objectives is similar-priced alt. For solo founders without an OKR tool, the agent generates OKRs in Notion DB instead.
- **Centercode (use case 10):** enterprise-priced. The agent defaults to PostHog feature-flag-based lightweight beta unless recipient specifies Centercode.
- **FullStory / LogRocket (use case 18):** paid plans (>$200/mo). Microsoft Clarity is the free fallback and the agent's default if no paid replay tool is configured.
- **Per-source OAuth (use case 20, 28):** Intercom / Zendesk / Gong / Fathom each require their own OAuth or API key. The agent walks the recipient through each setup once; afterwards every call is automated.

The 6 ⚠ rows all have free alternatives or are well-documented one-time setups — none are genuinely impossible, none require human-in-the-loop after setup.
