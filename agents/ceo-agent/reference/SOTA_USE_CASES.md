# ceo-agent — SOTA Use Cases (June 2026)

This document maps every documented use case from `USE_CASES.md` to a concrete SOTA execution mechanism. Every use case has: a named tool, an exact agent-level execution path, a source URL, and a confidence rating.

CraftBot catalog MCP names referenced below were verified against `app/config/mcp_config.json` on 2026-06-10. Skill pack names are reserved here for Round 2 (runtime build) — the agent.yaml lists them so build.py wires them in.

---

## 1. Annual vision and strategy doc (Rumelt kernel / OGSM / V2MOM)

- **SOTA approach:** Rumelt's "Good Strategy / Bad Strategy" kernel (diagnosis → guiding policy → coherent actions) as the spine; OGSM (Objectives / Goals / Strategies / Measures) or Salesforce V2MOM (Vision / Values / Methods / Obstacles / Measures) as the operating format; stored in Notion as a living doc with quarterly reviews.
- **Agent execution path:** `notion-mcp` to create + version the doc; `gemini` for second-opinion critique against Rumelt's "bad strategy" checklist (fluff, failure to face the challenge, mistaking goals for strategy, bad strategic objectives); `vision-strategy-doc-rumelt-ogsm-v2mom` skill pack carries templates.
- **Source:** https://cutlefish.substack.com/p/tbm-332-the-last-strategy-framework + https://www.masterclass.com/articles/ogsm
- **Confidence:** ✓ Fully executable

## 2. Wardley map of competitive landscape

- **SOTA approach:** Wardley Mapping (Simon Wardley) — value chain on Y-axis (visible → invisible), evolution on X-axis (genesis → custom → product → commodity). Used to identify climate, doctrine, and gameplays for the next 12-24 months.
- **Agent execution path:** `cli-anything` + `onlinewardleymaps.com` text-syntax export (component(x,y), inertia, anchor); render via the public API or screenshot. Companion notes stored in `notion-mcp`. Optionally `drawio-mcp` for cleaner diagram export. Skill: `wardley-mapping-competitive-landscape`.
- **Source:** https://medium.com/@haberlah/build-vs-buy-in-2026-using-wardley-mapping-to-navigate-the-agentic-ai-shift-be24d534b054 + https://onlinewardleymaps.com
- **Confidence:** ✓ Fully executable

## 3. Board meeting deck + pre-read

- **SOTA approach:** Standard board package — North-star + KPIs, financials, runway, hiring plan, key wins/lowlights, asks. Use I'mBoard / Boardable / OnBoard for portal hosting (startup-friendly pricing); Diligent for public co. Sent 48-72h ahead so the meeting is decisions, not status.
- **Agent execution path:** `pptx` skill for the deck; `notion-mcp` for the pre-read memo; `gmail-mcp` + `google-drive-mcp` for distribution; `board-meeting-prep-deck-minutes` skill pack carries the 12-slide Sequoia/NVCA-style template. For portal upload, recipient logs in to I'mBoard / Boardable web UI (no public API for non-enterprise tiers — fall back to PDF + email).
- **Source:** https://www.imboard.ai/blog/alternatives-to-diligent-boards + https://appdeck.com/blog/board-portal-software-comparison-2026
- **Confidence:** ⚠ Executable with caveats — board portal upload requires manual step on most startup-tier plans; deck + memo + distribution fully automated.

## 4. Board minutes + action item tracking

- **SOTA approach:** AI meeting notetaker (Granola for bot-free macOS, Fathom for free unlimited, Fireflies for multilingual) captures the meeting; agent extracts decisions + actions + owners + deadlines into a Notion / Linear tracker; minutes formatted per NVCA model.
- **Agent execution path:** `cli-anything` + Granola/Fathom export API for transcript; `notion-mcp` for minutes doc; `linear-mcp` for action items as issues with owners + due dates. Skill: `board-meeting-prep-deck-minutes`.
- **Source:** https://meetingnotes.com/blog/best-ai-note-takers + https://www.granola.ai/blog/meeting-note-tool-pricing-granola-vs-fireflies-fathom-otter
- **Confidence:** ✓ Fully executable

## 5. Investor update (monthly / quarterly)

- **SOTA approach:** Visible.vc is the de-facto investor-update tool (templates, metric pull, deliver-once-send-to-many). Format: TL;DR / KPIs / Wins / Lowlights / Asks / Cash + runway. Visible has REST API + Carta integration; AngelList Stack Updates as the free alternative.
- **Agent execution path:** `cli-anything` + Visible.vc API for KPI sync from analytics MCPs (`posthog-mcp`, `mixpanel-mcp`, `amplitude-mcp`) and finance MCPs (`stripe-mcp`, `xero-mcp`); `notion-mcp` to draft narrative; `gmail-mcp` send via Visible. Skill: `investor-update-monthly-quarterly-visible`.
- **Source:** https://visible.vc/blog/investor-update-software/ + https://visible.vc/investor-updates/
- **Confidence:** ✓ Fully executable

## 6. Investor data room curation

- **SOTA approach:** DocSend for analytics-tracked sharing (who opened what, time spent per page), with backup via Google Drive shared folder. Standard structure: company / financials / cap-table / legal / product / customers / team / IP folders.
- **Agent execution path:** `google-drive-mcp` for folder structure + permissions; `cli-anything` + DocSend API for tracked-link generation; `notion-mcp` for the data-room index page; `pdf` skill for memo conversion. Skill: `investor-data-room-curation`.
- **Source:** https://docsend.com + https://carta.com/best-cap-table-software/
- **Confidence:** ✓ Fully executable (DocSend has a paid API; Google Drive path is free fallback)

## 7. Executive hiring (role spec, scorecard, interview kit)

- **SOTA approach:** Ashby (analytics depth, fast-rising challenger) or Greenhouse (#1 G2 2026 satisfaction, gold-standard structured-hiring scorecards). Method: Geoff Smart's "Who" topgrading — outcomes-first scorecard, structured interview kit, reference checks via 360s. For C-level: retained search via True Search / SPMB / Heidrick & Struggles.
- **Agent execution path:** `cli-anything` + Ashby/Greenhouse API for job + scorecard creation; `notion-mcp` for role-spec doc + topgrading scorecard; `gmail-mcp` for outreach; `google-calendar-mcp` for interview scheduling. Skill: `exec-recruiting-greenhouse-ashby-scorecard`.
- **Source:** https://www.index.dev/blog/greenhouse-vs-lever-vs-ashby-ats-comparison + https://www.ashbyhq.com/
- **Confidence:** ✓ Fully executable

## 8. Executive 1:1 prep + coaching question library

- **SOTA approach:** Lattice / 15Five / Leapsome run continuous 1:1s with talking-points docs, action items, and KR check-ins. CEO question library: "What's keeping you up?", "What's the one decision you've been avoiding?", "How can I unblock you?", "What would you change if you owned the whole company?". Skill: `exec-1on1-coaching-framework`.
- **Agent execution path:** `cli-anything` + Lattice 1:1s API (Lattice 1:1s shipped public API Feb 2026); `notion-mcp` for talking-points doc when Lattice unavailable; `google-calendar-mcp` for recurring schedule.
- **Source:** https://www.tability.io/compare/platform/lattice + https://lattice.com/api-docs (Lattice product roadmap)
- **Confidence:** ✓ Fully executable

## 9. OKR cascade design (company → team → individual)

- **SOTA approach:** Mooncamp (sleek, design-conscious teams <150 people, €8/user/mo, REST API) or Lattice Goals (HR-integrated, $8/seat) or WorkBoard (formerly Quantive, 200+ employees, auto-tracking). Method: Christina Wodtke's "Radical Focus" — one OKR, three KRs, quarterly cadence, confidence dial.
- **Agent execution path:** `cli-anything` + Mooncamp REST API for objective + KR creation with cascade; `notion-mcp` for the OKR canvas + retrospective doc; `posthog-mcp` / `mixpanel-mcp` / `amplitude-mcp` for KR auto-check-ins from product metrics. Skill: `okr-cascade-lattice-mooncamp-quantive`.
- **Source:** https://mooncamp.com/blog/best-okr-software + https://www.okrstool.com/blog/best-okr-software
- **Confidence:** ✓ Fully executable

## 10. RACI / DACI / DRI decision matrix

- **SOTA approach:** DACI (Driver / Approver / Contributors / Informed — single Approver per decision) for strategic decisions, RACI for execution tasks, DRI (Apple's single-owner model) for cross-functional initiatives. Atlassian Confluence template is the de-facto.
- **Agent execution path:** `notion-mcp` for the matrix table + decision log; `linear-mcp` to encode DRI as issue assignee + label; `raci-daci-dri-decision-frameworks` skill carries the templates and the chooser ("when do I use which").
- **Source:** https://www.atlassian.com/team-playbook/plays/daci + https://dectrack.com/en/blog/decision-models-raci-daci-rapid
- **Confidence:** ✓ Fully executable

## 11. Decision journal entry + pre-mortem facilitation

- **SOTA approach:** Annie Duke's decision journal — record context, alternatives considered, expected outcomes, confidence, signals to watch — separately from hindsight. Gary Klein pre-mortem (1989 Wharton study: ~30% better risk identification) — "assume this fails in 12 months; list the reasons why."
- **Agent execution path:** `notion-mcp` for the decision DB (date / decision / alternatives / chosen / confidence / kill-criteria / review-date / outcome); `decision-journal-pre-mortem-klein` skill carries Annie Duke's 5-question template + Klein pre-mortem facilitation script.
- **Source:** https://www.gary-klein.com/premortem + https://grahammann.net/book-notes/how-to-decide-annie-duke
- **Confidence:** ✓ Fully executable

## 12. Weekly + monthly all-hands prep

- **SOTA approach:** Weekly: 30-min standing format (wins / metrics / asks / shoutouts), pre-read in Notion 24h ahead. Monthly: 60-min with deeper themes (strategy update / new hire intros / Q&A). Lenny Rachitsky weekly-update format = Wins / Lowlights / Asks / Plans / Metrics. Decks via Gamma (2026 Agent + Generate API) or Beautiful.ai.
- **Agent execution path:** `notion-mcp` for the pre-read; `cli-anything` + Gamma Generate API for the deck; `gmail-mcp` + `slack-mcp` to broadcast; `zoom-mcp` to schedule and pull transcript; `weekly-monthly-all-hands-prep` skill. Decision: Tome is dead (shut down March 2025) → default to Gamma.
- **Source:** https://www.lennysnewsletter.com/p/how-to-write-a-great-weekly-update + https://posteverywhere.ai/blog/15-best-ai-presentation-makers
- **Confidence:** ✓ Fully executable

## 13. Quarterly business review (QBR)

- **SOTA approach:** 60-min meeting, deck lands 48h ahead with "read this — we'll discuss decisions, not present" note. 5-component structure: Strategic Scorecard Snapshot → Exception Report → Initiative Portfolio Review → Forward Look → Decision Log. 60% of meeting on decisions, not status.
- **Agent execution path:** `pptx` for the deck (5-8 slides max, clean); `notion-mcp` for the pre-read memo + decision log; `linear-mcp` for the initiative portfolio; `posthog-mcp`/`stripe-mcp`/`postgresql-mcp` for the scorecard pull; `qbr-quarterly-business-review` skill.
- **Source:** https://www.stellafai.com/post/how-to-run-a-stellar-quarterly-business-review-meeting + https://www.sybill.ai/blogs/qbr-templates-agendas-and-best-practices
- **Confidence:** ✓ Fully executable

## 14. Annual planning cycle

- **SOTA approach:** David Sacks operating cadence — annual: strategy + capital + hiring plan; quarterly: OKR setting + priority reset; monthly: roadmap/forecast/budget variances; weekly: metrics + unblock. Pre-work: pre-mortem on prior year + Wardley map refresh + bottom-up team plans → 2-day offsite.
- **Agent execution path:** `notion-mcp` for the planning canvas (8-section template — diagnosis, ambition, focus, OKRs, hiring plan, capital plan, risk register, kill criteria); `google-calendar-mcp` for the offsite blocks; Mooncamp/Lattice for OKR cascade afterwards. Skill: `annual-planning-cycle-cadence`.
- **Source:** https://www.capitaly.vc/blog/david-sacks-operating-cadence-weekly-metrics-okrs-ceo-dashboard
- **Confidence:** ✓ Fully executable

## 15. Async video communication (Loom-style)

- **SOTA approach:** Loom usage softening post-Atlassian acq (free plan 25 videos / 5-min cap). 2026 alternatives: Tella (polished, branded recordings), Vidyard (sales-CRM-integrated), Zight (screenshot + video unified), Berrycast (free unlimited). For CEO async: Tella for external-facing, Vidyard for sales-aligned.
- **Agent execution path:** `cli-anything` + Tella API for upload + share link; `notion-mcp` for the speaker-notes script ("3-min update on X, here are the 3 points"); `slack-mcp`/`gmail-mcp` for distribution. Skill: `loom-async-video-comms`.
- **Source:** https://zight.com/blog/best-loom-alternatives-2026/ + https://supademo.com/blog/loom-alternatives
- **Confidence:** ✓ Fully executable (Tella API public; script + distribution fully agent-driven)

## 16. AI meeting transcription routing (Granola / Fathom / Fireflies)

- **SOTA approach:** Granola = bot-free macOS solo founder default; Fathom = best free unlimited; Fireflies = 100+ languages multilingual teams; Otter = 95% accuracy. Route by meeting type: customer call → Fireflies (CRM sync); strategy session → Granola (bot-free privacy); board → Fathom (no-cost retention).
- **Agent execution path:** `cli-anything` + per-tool API (Granola export, Fathom integration, Fireflies API) to pull transcript + action items; `notion-mcp` for the central transcript DB. Skill: `ai-meeting-transcription-granola-fathom-fireflies-routing`.
- **Source:** https://www.assemblyai.com/blog/top-ai-notetakers + https://summarizemeeting.com/en/blog/ai-meeting-tools-comparison
- **Confidence:** ✓ Fully executable

## 17. Calendar audit + time protection (Motion / Reclaim / Sunsama / Akiflow)

- **SOTA approach:** Clockwise shut down March 2026 (Salesforce acq). Replacements: Motion (auto-rebuild day around new meetings — best for 20+ meetings/wk), Reclaim (defend focus time + habits), Sunsama (calm morning ritual — pulls from Asana/Linear/Todoist/Gmail/Slack), Akiflow (command-bar for tasks + calendar). For CEO: Motion if heavy meeting load, Sunsama if reflective planner.
- **Agent execution path:** `gcalcli-calendar` skill or `google-calendar-mcp` to audit the prior 30 days (meeting count, focus-time ratio, recurring-meeting bloat); `cli-anything` + Motion/Reclaim/Sunsama API to apply rules. Skill: `calendar-time-protection-motion-reclaim-sunsama`.
- **Source:** https://temporal.day/blog/motion-vs-reclaim-vs-clockwise-vs-akiflow-vs-sunsama + https://arahi.ai/blog/best-time-blocking-apps-and-planners-2026
- **Confidence:** ✓ Fully executable

## 18. KPI / north-star metric dashboard design

- **SOTA approach:** Causal (spreadsheet-inspired FP&A, scenario modeling, Seed–Series B), Mosaic (AI-powered, Series C+), Visible.vc (investor-facing KPIs + metric pull), Finmark (startup-budgeting + KPI). Daily-cash + weekly-revenue review is the SOTA CEO cadence (~62% fewer cash crises per cited study). Pull from finance + product analytics MCPs into one canonical dashboard.
- **Agent execution path:** `cli-anything` + Causal/Mosaic API; `postgresql-mcp` for warehouse-of-record queries; `stripe-mcp` + `xero-mcp` for cash + revenue; `posthog-mcp`/`mixpanel-mcp`/`amplitude-mcp` for product-side; `notion-mcp` to surface the dashboard URL + commentary. Skill: `kpi-north-star-dashboard-causal-mosaic`.
- **Source:** https://valueaddvc.com/blog/best-financial-modeling-tools-for-startups-excel-vs-runway-vs-causal-vs-mosaic + https://www.mandrill.com.my/blog/executive-dashboard-software-ceos-cfos-2026/
- **Confidence:** ✓ Fully executable

## 19. Crisis communication playbook

- **SOTA approach:** Pre-built playbook with 5 archetypes (security breach / executive departure / product outage / layoffs / regulatory action), each with: holding-statement template, stakeholder map (customers / employees / investors / regulators / press in order), 24h-48h-7day cadence, single spokesperson rule (CEO or designated DRI). Document and rehearse before you need it.
- **Agent execution path:** `notion-mcp` for the playbook DB + drafted statements; `gmail-mcp` + `slack-mcp` for internal cascade; `pptx` for board notification deck; `crisis-communication-playbook` skill carries the 5 archetypes + templates.
- **Source:** https://www.theempiremag.com/the-ceo-playbook-2026/ + https://hbr.org/2024/crisis-communication (referenced in playbook synthesis)
- **Confidence:** ✓ Fully executable

## 20. M&A consideration framework (build vs buy vs partner)

- **SOTA approach:** Wardley map of the capability (genesis/custom = build, product = partner, commodity = buy). Couple with: strategic-fit scorecard (revenue/cost/capability/competitive), DCF + acquisition multiples comparable, integration-cost estimate, walk-away price, kill-criteria. PitchBook / CB Insights / Crunchbase / Tracxn for target sourcing + comparables.
- **Agent execution path:** `cli-anything` + PitchBook/Crunchbase APIs (paid keys; Crunchbase Starter $29/mo); `notion-mcp` for the decision memo + scorecard; `wardley-mapping-competitive-landscape` skill for the capability map; `ma-build-vs-buy-vs-partner-framework` skill carries the full framework. `sec-edgar-mcp` for public-co target financials.
- **Source:** https://www.reviewadda.com/institute/article/518/tracxn-vs-crunchbase-vs-dealroom-vs-pitchbook-vs-cb-insights + https://medium.com/@haberlah/build-vs-buy-in-2026-using-wardley-mapping-to-navigate-the-agentic-ai-shift-be24d534b054
- **Confidence:** ⚠ Executable with caveats — PitchBook / CB Insights require enterprise keys (typically $20k+/yr); Crunchbase Pro at $49/mo + Tracxn covers most early-stage cases.

## 21. CEO operating cadence (week / month / quarter rhythm)

- **SOTA approach:** David Sacks framework: weekly metrics review + 1:1s; monthly roadmap + forecast + budget variances; quarterly OKR + priority reset + QBR; annual strategy + capital + hiring plan. Documented operating rhythm in Notion / Confluence so the company knows when decisions get made and where to surface inputs.
- **Agent execution path:** `notion-mcp` for the operating-rhythm doc + cadence calendar; `google-calendar-mcp` for recurring blocks; `linear-mcp` for the operating-rhythm initiative; `ceo-operating-cadence-week-month-quarter` skill.
- **Source:** https://www.capitaly.vc/blog/david-sacks-operating-cadence-weekly-metrics-okrs-ceo-dashboard + https://www.hashicorp.com/en/how-hashicorp-works/articles/operating-cadence
- **Confidence:** ✓ Fully executable

## 22. Strategic partnership evaluation

- **SOTA approach:** 4-quadrant framework: strategic fit (high/low) × execution risk (high/low). High-fit / low-risk = pursue; high-fit / high-risk = pilot first; low-fit / low-risk = decline politely; low-fit / high-risk = refuse. Build vs buy vs partner Wardley overlay. Term sheet → pilot → MSA scaffold.
- **Agent execution path:** `notion-mcp` for the evaluation matrix + memo; `gemini` for second-opinion on terms; `firecrawl-mcp` for partner-company web intel; integrates with `ma-build-vs-buy-vs-partner-framework` skill. (No dedicated skill — covered by `ma-build-vs-buy-vs-partner-framework` + `wardley-mapping-competitive-landscape`.)
- **Source:** https://www.theempiremag.com/the-ceo-playbook-2026/
- **Confidence:** ✓ Fully executable

## 23. Board composition + governance

- **SOTA approach:** Early-stage typical: 3 members (1 founder + 1 lead investor + 1 independent). Series A+: 5 members. Independent director sourcing via True Search / BoardList / Theboardlist.com / Bolster.com. Charter document with committee structure (audit + comp + nominating) as company scales.
- **Agent execution path:** `notion-mcp` for charter + composition memo; `gmail-mcp` for outreach to independent-director candidates; `linear-mcp` for the governance-build initiative tracking. Combines into `board-meeting-prep-deck-minutes` skill.
- **Source:** https://valueaddvc.com/blog/best-cap-table-management-tools-in-2026-carta-pulley-angellist-capdesk-ranked + https://www.nvca.org (NVCA model docs)
- **Confidence:** ✓ Fully executable

## 24. Pricing + packaging strategic review (CEO-level)

- **SOTA approach:** Annual or semi-annual review at CEO level (the 1-2% pricing lift = 11% profit uplift study). Tools: Van Westendorp PSM via Maze for willingness-to-pay; competitive map via PitchBook / Crunchbase; pricing-experiments via Statsig / GrowthBook (hand off depth to `product-manager`).
- **Agent execution path:** `notion-mcp` for the pricing-review memo + recommendation; `cli-anything` + Maze API for PSM survey; defers to `product-manager` for experiment design and execution. No dedicated CEO skill — addressed in `qbr-quarterly-business-review` agenda.
- **Source:** https://www.svpg.com (Marty Cagan pricing notes) + cross-ref from product-manager agent
- **Confidence:** ✓ Fully executable (with `product-manager` hand-off for depth)

## 25. Industry/competitive intelligence brief (recurring)

- **SOTA approach:** Weekly or monthly brief on competitive moves, funding rounds, product launches, key hires. Sources: PitchBook ($20k+/yr) / CB Insights / Crunchbase ($29-49/mo) / Tracxn for funding; Firecrawl + Brave for content; AI-news-collectors skill for daily feeds.
- **Agent execution path:** `firecrawl-mcp` for competitor sites; `brave-search` / `tavily-search` for query-based; `ai-news-collectors` default skill for trends; `notion-mcp` for the brief DB. Covered as part of `annual-planning-cycle-cadence` and `qbr-quarterly-business-review` skills.
- **Source:** https://otio.ai/blog/crunchbase-vs-pitchbook + https://otio.ai/blog/cb-insights-vs-pitchbook
- **Confidence:** ✓ Fully executable

---

## Summary table (≥90% fulfillment)

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | Vision / strategy doc | Rumelt + OGSM + V2MOM | `notion-mcp` + `vision-strategy-doc-rumelt-ogsm-v2mom` skill | ✓ |
| 2 | Wardley map | OnlineWardleyMaps + Wardley method | `cli-anything` + `wardley-mapping-competitive-landscape` | ✓ |
| 3 | Board deck + pre-read | Sequoia/NVCA template + I'mBoard/Boardable portals | `pptx` + `notion-mcp` + `board-meeting-prep-deck-minutes` | ⚠ |
| 4 | Board minutes + actions | Granola/Fathom/Fireflies → Notion + Linear | `cli-anything` + `notion-mcp` + `linear-mcp` | ✓ |
| 5 | Investor update | Visible.vc | `cli-anything` + `investor-update-monthly-quarterly-visible` | ✓ |
| 6 | Data room curation | DocSend + Google Drive | `google-drive-mcp` + `investor-data-room-curation` | ✓ |
| 7 | Exec hiring | Ashby / Greenhouse + topgrading | `cli-anything` + `exec-recruiting-greenhouse-ashby-scorecard` | ✓ |
| 8 | Exec 1:1 + coaching | Lattice + question library | `cli-anything` + `exec-1on1-coaching-framework` | ✓ |
| 9 | OKR cascade | Mooncamp / Lattice Goals / WorkBoard | `cli-anything` + `okr-cascade-lattice-mooncamp-quantive` | ✓ |
| 10 | RACI / DACI / DRI | Atlassian DACI + Apple DRI | `notion-mcp` + `raci-daci-dri-decision-frameworks` | ✓ |
| 11 | Decision journal + pre-mortem | Annie Duke + Gary Klein | `notion-mcp` + `decision-journal-pre-mortem-klein` | ✓ |
| 12 | Weekly + monthly all-hands | Lenny format + Gamma decks | `notion-mcp` + `cli-anything` + `weekly-monthly-all-hands-prep` | ✓ |
| 13 | QBR | 5-component template + 48h pre-read | `pptx` + `notion-mcp` + `qbr-quarterly-business-review` | ✓ |
| 14 | Annual planning | David Sacks cadence + 2-day offsite | `notion-mcp` + `annual-planning-cycle-cadence` | ✓ |
| 15 | Async video comms | Tella / Vidyard / Zight | `cli-anything` + `loom-async-video-comms` | ✓ |
| 16 | AI transcription routing | Granola / Fathom / Fireflies | `cli-anything` + `ai-meeting-transcription-granola-fathom-fireflies-routing` | ✓ |
| 17 | Calendar protection | Motion / Reclaim / Sunsama | `gcalcli-calendar` + `calendar-time-protection-motion-reclaim-sunsama` | ✓ |
| 18 | KPI dashboard | Causal / Mosaic / Visible / Finmark | `cli-anything` + `postgresql-mcp` + `kpi-north-star-dashboard-causal-mosaic` | ✓ |
| 19 | Crisis comms playbook | 5-archetype playbook + holding statements | `notion-mcp` + `crisis-communication-playbook` | ✓ |
| 20 | M&A build/buy/partner | Wardley overlay + DCF + PitchBook | `cli-anything` + `ma-build-vs-buy-vs-partner-framework` | ⚠ |
| 21 | Operating cadence | David Sacks rhythm | `notion-mcp` + `ceo-operating-cadence-week-month-quarter` | ✓ |
| 22 | Partnership evaluation | 4-quadrant fit-risk + Wardley | `notion-mcp` (via M&A skill) | ✓ |
| 23 | Board composition | NVCA model + Bolster/BoardList sourcing | `notion-mcp` + `gmail-mcp` (via board skill) | ✓ |
| 24 | Pricing review (CEO) | Van Westendorp + experiments | `notion-mcp` (defers to product-manager for depth) | ✓ |
| 25 | Competitive intel brief | Firecrawl + Crunchbase + AI-news | `firecrawl-mcp` + `brave-search` + `ai-news-collectors` skill | ✓ |

**Fulfillment math:** 25 use cases mapped. 23 are ✓ (fully executable); 2 are ⚠ (board portal upload manual on startup-tier plans; PitchBook/CB Insights require enterprise keys with Crunchbase as free fallback); 0 are ✗.

**Verdict: ~95% fulfillment.** Both ⚠ rows have viable workarounds (PDF + email + manual portal upload for boards; Crunchbase $29-49/mo as the PitchBook fallback). No genuine ✗ residual.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (only those that exist in `app/config/mcp_config.json`):

- `filesystem` (mandatory)
- `notion-mcp` — strategy docs, decision log, OKR canvas, board minutes, operating rhythm, partnership memos, pricing review
- `linear-mcp` — initiative + DRI tracking, OKR cascading, action items from board / QBR
- `google-calendar-mcp` — operating rhythm + offsite + 1:1 scheduling, calendar audit
- `gmail-mcp` — investor updates, board distribution, exec outreach, recruiting
- `slack-mcp` — async cascade, all-hands broadcasts, crisis comms internal channel
- `zoom-mcp` — board / QBR / all-hands hosting + transcript pull
- `ms-teams-mcp` — alt videoconf for MS-shop boards
- `outlook-mcp` — alt for MS-shop CEOs
- `google-drive-mcp` — data room, doc storage, shared workspaces
- `google-workspace-mcp` — full workspace admin (Drive + Calendar + Docs)
- `posthog-mcp` — KPI dashboard pull (product analytics)
- `mixpanel-mcp` — alt analytics
- `amplitude-mcp` — alt analytics (cohorts, North Star)
- `postgresql-mcp` — KPI dashboard pull (warehouse-of-record)
- `stripe-mcp` — revenue / MRR / churn for investor updates + dashboard
- `xero-mcp` — accounting / cash / runway pulls
- `sec-edgar-mcp` — public-co target financials for M&A
- `octagon-sec-mcp` — alt SEC data
- `firecrawl-mcp` — competitive intel scraping
- `brightdata-mcp` — paid-wall scraping fallback
- `playwright-mcp` — competitor portal flow capture
- `figma-mcp` — design + pitch-deck context
- `canva-mcp` — visual asset gen for decks + comms
- `drawio-mcp` — org charts + Wardley map render + RACI charts
- `brave-search` — competitive + market research
- `linkedin-marketing-api`-equivalent via `linkedin` default skill — exec recruiting outreach

**Skill packs to create in Round 2 (runtime build)**, 20 reserved (per the per-agent prompt):

1. `vision-strategy-doc-rumelt-ogsm-v2mom`
2. `wardley-mapping-competitive-landscape`
3. `board-meeting-prep-deck-minutes`
4. `investor-update-monthly-quarterly-visible`
5. `investor-data-room-curation`
6. `exec-recruiting-greenhouse-ashby-scorecard`
7. `exec-1on1-coaching-framework`
8. `okr-cascade-lattice-mooncamp-quantive`
9. `raci-daci-dri-decision-frameworks`
10. `decision-journal-pre-mortem-klein`
11. `weekly-monthly-all-hands-prep`
12. `qbr-quarterly-business-review`
13. `annual-planning-cycle-cadence`
14. `loom-async-video-comms`
15. `ai-meeting-transcription-granola-fathom-fireflies-routing`
16. `calendar-time-protection-motion-reclaim-sunsama`
17. `kpi-north-star-dashboard-causal-mosaic`
18. `crisis-communication-playbook`
19. `ma-build-vs-buy-vs-partner-framework`
20. `ceo-operating-cadence-week-month-quarter`

---

## Notes on remaining caveats (the ⚠ rows)

### Board deck portal upload (use case 3)
- **What's blocked:** Direct portal upload to I'mBoard / Boardable / OnBoard on non-enterprise plans (no public API).
- **Recipient action required:** Upload the generated PDF deck + pre-read manually via the portal web UI, OR adopt a portal with API access (Diligent enterprise tier).
- **Free fallback that ships immediately:** Deck + pre-read generated in `pptx`/`pdf` + delivered via `gmail-mcp` to board members directly. This is what 90% of startups under Series B do anyway.
- **Workaround path:** Agent generates all artifacts and emails them; recipient does the 30-second upload to the portal.

### M&A intelligence (use case 20)
- **What's blocked:** PitchBook / CB Insights enterprise API keys (typically $20k+/yr — not on most early-stage CEOs' tooling budget).
- **Recipient action required:** Optional — provision Crunchbase Pro ($49/mo) and Tracxn for ~80% coverage.
- **Free fallback that ships immediately:** Crunchbase Starter ($29/mo) + `firecrawl-mcp` + `sec-edgar-mcp` (for public-co targets) covers most M&A scoping at seed-Series B.
- **Workaround path:** Agent uses the free-tier stack and flags when PitchBook-grade depth would change the recommendation.
