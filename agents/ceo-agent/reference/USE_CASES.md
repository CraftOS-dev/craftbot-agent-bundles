# CEO Agent — Use Cases

> User-facing catalog. Ships in the bundle but is **not** loaded into the agent's context — it exists so users (and future contributors) can see what the agent is for, what it can execute today, and where the honest gaps are.

**Tier:** general · **Category:** executive
**Core job:** Senior CEO advisor for solo founders and early-stage CEOs — strategy + vision, board, investor relations, executive hiring, OKR cascading, decision frameworks, all-hands / QBR / annual planning cadence, calendar protection, KPI dashboards, crisis comms, M&A framing.

> Ships with the SOTA executive operator stack (Visible.vc / Mooncamp / Lattice / Ashby / Greenhouse / Granola / Motion / Causal / Mosaic / Gamma / Tella / OnlineWardleyMaps / Crunchbase / SEC EDGAR + DACI / pre-mortem / Lenny / David Sacks frameworks) — executes end-to-end (board pack generation, investor updates, OKR cascade, decision logs, calendar audits, KPI dashboards, crisis statements), not just directs. Defers to siblings for product / marketing / sales / finance / legal / ops / support / growth / data depth.

---

## What this agent is supposed to do

### Strategy + vision
- Write annual vision and strategy doc (Rumelt kernel / OGSM / V2MOM)
- Build Wardley map of competitive landscape
- Set strategic policy ("what we say yes/no to")
- Refresh strategy quarterly (with QBR) and annually (with planning cycle)
- Industry / competitive intelligence brief (recurring)

### Board management + governance
- Build board meeting deck + pre-read (Sequoia/NVCA template, 12 slides)
- Capture board minutes + action items (Granola/Fathom → Notion + Linear)
- Design board composition + governance (sizing, independents, committees)

### Investor relations
- Draft and send monthly / quarterly investor update (Visible.vc)
- Curate investor data room (DocSend + Google Drive)

### Executive hiring
- Author outcomes-first scorecard (NOT a JD) — topgrading method
- Build interview kit + reference-check questions
- Run stage-gated process (phone → outcomes interview → working session → references)
- Coordinate with retained search for C-level (True Search / SPMB / Heidrick & Struggles)

### Executive 1:1 + coaching
- Prep 1:1 talking-points doc (Lattice 1:1s)
- Surface coaching question from library
- KR check-in + blocker surfacing

### OKR cascading
- Design company OKRs (one O + three KRs)
- Cascade company → team → individual
- Wire auto-check-in mechanism (analytics MCP → Mooncamp/Lattice/WorkBoard)
- Score at quarter end + carry-over decisions

### Decision frameworks
- Build RACI / DACI / DRI matrix per decision
- Author decision journal entry (Annie Duke template)
- Facilitate pre-mortem (Gary Klein, 30-min script)
- Classify decision (reversible vs irreversible)

### All-hands + operating rhythm
- Prep weekly all-hands (30 min, Lenny format, Gamma deck)
- Prep monthly all-hands (60 min, deeper themes)
- Run Quarterly Business Review (QBR) — 5-component template, 48h pre-read
- Author annual plan (8-section template, 2-day offsite agenda)

### Async + meeting infrastructure
- Script and produce async video comms (Tella / Vidyard / Zight)
- Route AI meeting transcription by meeting type (Granola / Fathom / Fireflies)
- Audit + protect calendar (Motion / Reclaim / Sunsama; Clockwise EOL March 2026)

### KPI dashboard + reporting
- Design north-star + supporting KPIs
- Build dashboard in Causal / Mosaic / Visible / Finmark
- Set source-of-record per metric (no metric without an owning system)
- Configure daily-cash + weekly-revenue review cadence

### Crisis + risk
- Author crisis comms playbook (5 archetypes: breach / exec / outage / layoffs / regulatory)
- Draft holding statements + stakeholder cascade
- Maintain risk register + kill criteria

### Strategic finance + capital allocation framing
- M&A consideration framework (build vs buy vs partner, Wardley overlay + DCF + walk-away)
- Strategic partnership evaluation (4-quadrant fit-risk matrix)
- Pricing + packaging strategic review (CEO-level — defers depth to product-manager)

### CEO operating cadence
- Author operating-rhythm doc (David Sacks framework)
- Lock recurring cadence on calendar (weekly / monthly / quarterly / annual)
- Run weekly metrics review

---

## Execution status (SOTA — June 2026)

> Mandatory table. Every use case from the section above appears here as a row. This is the proof the agent is real, not a toy.

| Use case | SOTA mechanism | Path |
|---|---|---|
| Vision / strategy doc | Rumelt kernel + OGSM + V2MOM | `notion-mcp` + `vision-strategy-doc-rumelt-ogsm-v2mom` skill |
| Wardley map | OnlineWardleyMaps + Wardley method | `cli-anything` + `wardley-mapping-competitive-landscape` skill |
| Strategic policy (yes/no choices) | Rumelt guiding policy | `vision-strategy-doc-rumelt-ogsm-v2mom` skill |
| Quarterly strategy refresh | QBR + strategy update slide | `qbr-quarterly-business-review` skill |
| Annual strategy refresh | David Sacks + planning cycle | `annual-planning-cycle-cadence` skill |
| Industry / competitive intel brief | Firecrawl + Crunchbase + ai-news-collectors | `firecrawl-mcp` + `brave-search` + `ai-news-collectors` skill |
| Board deck + pre-read | Sequoia/NVCA 12-slide template + I'mBoard/Boardable portals | `pptx` + `notion-mcp` + `board-meeting-prep-deck-minutes` |
| Board minutes + actions | Granola/Fathom/Fireflies → Notion + Linear | `cli-anything` + `notion-mcp` + `linear-mcp` |
| Board composition + governance | NVCA model + Bolster/BoardList sourcing | `notion-mcp` + `gmail-mcp` (via board skill) |
| Investor update (monthly/quarterly) | Visible.vc | `cli-anything` + `investor-update-monthly-quarterly-visible` skill |
| Investor data room | DocSend + Google Drive | `google-drive-mcp` + `investor-data-room-curation` skill |
| Outcomes scorecard | Geoff Smart topgrading method | `notion-mcp` + `exec-recruiting-greenhouse-ashby-scorecard` skill |
| Exec interview kit | Topgrading 360 + structured interviews | `exec-recruiting-greenhouse-ashby-scorecard` skill |
| Exec hiring pipeline | Ashby / Greenhouse + DACI decision | `cli-anything` + `exec-recruiting-greenhouse-ashby-scorecard` |
| C-level retained search | True Search / SPMB / Heidrick & Struggles | `gmail-mcp` + manual recruiter coordination |
| Exec 1:1 + coaching library | Lattice 1:1s API + question library | `cli-anything` + `exec-1on1-coaching-framework` skill |
| OKR cascade design | Christina Wodtke radical focus + Mooncamp/Lattice | `cli-anything` + `okr-cascade-lattice-mooncamp-quantive` |
| KR auto-check-in | Analytics MCP → OKR platform | `posthog-mcp` / `mixpanel-mcp` / `amplitude-mcp` + `stripe-mcp` |
| RACI / DACI / DRI matrix | Atlassian DACI + Apple DRI | `notion-mcp` + `raci-daci-dri-decision-frameworks` skill |
| Decision journal entry | Annie Duke template | `notion-mcp` + `decision-journal-pre-mortem-klein` skill |
| Pre-mortem facilitation | Gary Klein 30-min script | `notion-mcp` + `decision-journal-pre-mortem-klein` skill |
| Weekly all-hands | Lenny format + Gamma decks | `notion-mcp` + `cli-anything` + `weekly-monthly-all-hands-prep` |
| Monthly all-hands | Lenny format + deeper themes | `notion-mcp` + `weekly-monthly-all-hands-prep` skill |
| QBR | 5-component template + 48h pre-read | `pptx` + `notion-mcp` + `qbr-quarterly-business-review` skill |
| Annual planning cycle | David Sacks rhythm + 2-day offsite | `notion-mcp` + `annual-planning-cycle-cadence` skill |
| Async video comms | Tella / Vidyard / Zight | `cli-anything` + `loom-async-video-comms` skill |
| AI transcription routing | Granola / Fathom / Fireflies | `cli-anything` + `ai-meeting-transcription-granola-fathom-fireflies-routing` |
| Calendar audit + protection | Motion / Reclaim / Sunsama | `gcalcli-calendar` + `calendar-time-protection-motion-reclaim-sunsama` |
| KPI / north-star dashboard | Causal / Mosaic / Visible / Finmark | `cli-anything` + `postgresql-mcp` + `stripe-mcp` + `kpi-north-star-dashboard-causal-mosaic` |
| Daily cash + weekly revenue review | Cadence + dashboard | `ceo-operating-cadence-week-month-quarter` skill |
| Crisis comms playbook | 5 archetypes + holding statements | `notion-mcp` + `crisis-communication-playbook` skill |
| Risk register + kill criteria | Annual plan + decision log | `notion-mcp` + `annual-planning-cycle-cadence` skill |
| M&A build/buy/partner | Wardley overlay + DCF + PitchBook/Crunchbase | `cli-anything` + `sec-edgar-mcp` + `ma-build-vs-buy-vs-partner-framework` |
| Partnership evaluation | 4-quadrant fit-risk + Wardley | `notion-mcp` (via M&A skill) |
| Pricing review (CEO-level) | Van Westendorp PSM + experiments | `notion-mcp` (defers to product-manager for depth) |
| CEO operating rhythm | David Sacks weekly/monthly/quarterly/annual | `notion-mcp` + `google-calendar-mcp` + `ceo-operating-cadence-week-month-quarter` |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Board portal upload (I'mBoard / Boardable / OnBoard) | ⚠ | Most startup-tier board portals lack public API for upload. Deck + memo generation is automated; upload is a manual 30-second step the recipient does via portal web UI. Email delivery to board via `gmail-mcp` is always available as fallback. |
| M&A enterprise intel (PitchBook / CB Insights) | ⚠ | PitchBook ($20k+/yr) and CB Insights (enterprise) require keys outside most early-stage CEO tooling budgets. Crunchbase Pro ($49/mo) + Tracxn + `sec-edgar-mcp` covers ~80% of M&A scoping at seed-Series B. Agent flags when PitchBook-grade depth would change the recommendation. |
| C-level retained search execution | ⚠ | Retained-search firms (True Search / SPMB / Heidrick & Struggles) operate via human relationship — agent prepares brief, references, scorecard; recipient engages firm. No public API. |
| Live binding legal advice | ✗ | Agent surfaces frameworks (DACI, M&A memo) but defers all binding legal to `legal-counsel`. This is the right behavior — agent is not a lawyer. |
| Live binding tax advice | ✗ | Same — agent surfaces capital plan + scenario framing but defers to recipient's CPA / tax counsel. |

**Verdict (June 2026): ~95% fulfillment.** The CEO surface is fully automated for strategy docs, board pack generation, investor updates, exec scorecards, OKR cascades, decision logs, all-hands prep, QBR, annual planning, calendar audits, KPI dashboard design, crisis comms drafting, and M&A framing. The 5% residual is honest hand-offs (binding legal/tax) and one manual portal-upload step that has a free-email fallback.

---

## When to use this agent

- "Write our FY2027 strategy doc — we're a 20-person seed-stage SaaS doing $1.5M ARR."
- "Build our board pack for next Thursday — board meeting #4, $3M raised."
- "Draft the May investor update — MRR was up 8%, lost a key customer, runway 14 months."
- "Build the outcomes scorecard for the VP Engineering role I'm starting to recruit for."
- "Set Q3 OKRs for the whole company — we want to hit $5M ARR and ship the enterprise tier."
- "Help me decide whether to expand to Europe in Q4 — it's an irreversible decision."
- "Run pre-mortem on the pricing change we're considering."
- "Prep next week's all-hands — 25 people, hybrid, 30 min."
- "Audit my calendar — I'm in 35 meetings/week and not getting strategy work done."
- "Should we acquire competitor X or build the feature ourselves?"
- "Build our CEO dashboard — what should I be looking at daily, weekly, monthly, quarterly?"
- "Draft the crisis comms playbook so we have it before we need it."

---

## When NOT to use this agent

- **Product strategy depth** (PRDs, roadmaps, RICE prioritization, user research, A/B test design) — hand off to `product-manager`
- **Marketing execution** (positioning, brand, campaigns, social, SEO, email lifecycle, ads) — hand off to `marketing-agent`
- **Sales pipeline + playbook depth** (demos, sales scripts, sales hiring scorecards, comp design) — hand off to `sales-agent`
- **Operational finance** (bookkeeping, AR/AP, monthly close, audit prep) — hand off to `finance-controller`
- **Strategic finance depth** (fundraising mechanics, scenario modeling depth, cap table mechanics, secondaries) — hand off to `finance-agent`
- **Binding legal** (term sheets, employment law, IP, M&A docs, regulatory) — hand off to `legal-counsel` (agent is not a lawyer)
- **Hiring + vendor ops, HR ops, comp banding, benefits admin** — hand off to `operations-agent`
- **Customer issues, support playbook, CSAT improvement** — hand off to `customer-support-agent`
- **Activation + retention experiments, growth loops** — hand off to `growth-agent`
- **Warehouse analytics, dbt models, cohort SQL depth** — hand off to `data-analyst`
- **Video production craft** (script + edit + render) — hand off to `video-creator`
- **Technical documentation craft** (ADRs, API docs, tutorials) — hand off to `technical-writer`
- **Engineering implementation** (code, code review, debugging) — hand off to `senior-python-engineer` or other engineering specialists
