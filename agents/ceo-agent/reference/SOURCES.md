# CEO Agent — Sources

> Section→source map for `soul.md` and `role.md`. Ships in the bundle but is **not** loaded into the agent's context. For humans verifying provenance and for future updates.

## soul.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Title + persona intro | Synthesis from `reference/SOTA_USE_CASES.md` + sibling agents `marketing-agent` and `product-manager` shape | Convictions ("time is finite / decisions over alignment / hire slow fire fast") synthesize Sacks operating cadence + topgrading + standard CEO playbook canon |
| Purpose | `reference/SOTA_USE_CASES.md` Section "Use cases" + sibling-agent defer pattern | |
| Execution stack | `reference/SOTA_USE_CASES.md` 25 use case rows | Built directly from SOTA mapping; each bullet = a skill pack |
| When invoked (modes) | `reference/SOTA_USE_CASES.md` per-use-case rows + David Sacks operating cadence | Mode-per-verb breakdown mirrors `marketing-agent` and `product-manager` |
| Core operating rules | Synthesis from: David Sacks cadence, Geoff Smart topgrading, Atlassian DACI, Gary Klein pre-mortem, Annie Duke decision journal, Rumelt strategy | |
| Mode-specific decisions | Per-mode SOTA mapping in `reference/SOTA_USE_CASES.md` | |
| Quality gates | Synthesis from playbook templates in `role.md` | |
| Output format | Synthesis from template patterns in `role.md` | |
| Communication style | CEO-canon active-voice + specificity (Lenny update format, Sacks cadence dashboards) | |
| When to push back | Synthesis from hard rules (Rumelt bad-strategy check, DACI single-A, topgrading, pre-mortem mandatory) | |
| When to defer | Sibling-agent slugs from per-agent prompt + adjacency to `marketing-agent` / `product-manager` defer patterns | |
| PROACTIVE self-init footer | `METHODOLOGY.md` standard footer | Same wording across all agents; only the 3 routine questions changed (stage / team size / 90-day priorities) |

## role.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Capability reference (strategy frameworks) | Rumelt + OGSM + V2MOM + Wardley + Porter + Blue Ocean + Helmer 7 Powers + AARRR — synthesis from canonical sources | All names verified via web search June 2026 |
| Capability reference (decision frameworks) | Atlassian DACI + Apple DRI + Bain RAPID + Annie Duke decision journal + Gary Klein pre-mortem + Bezos 2-way/1-way door + Eisenhower matrix | |
| Capability reference (capital allocation) | Standard CFO/CEO finance canon (DCF / NPV / IRR / payback / real options / LTV:CAC) | Defers depth to `finance-agent` |
| Capability reference (board governance) | NVCA Model Docs + Cooley GO + Sequoia + Carta governance docs | |
| Sibling agent hand-off matrix | Per-agent prompt sibling list + adjacent agents in catalog | |
| Strategy doc playbook | `reference/SOTA_USE_CASES.md` use case 1 + Rumelt source | https://cutlefish.substack.com/p/tbm-332-the-last-strategy-framework |
| Wardley mapping playbook | `reference/SOTA_USE_CASES.md` use case 2 + OnlineWardleyMaps | https://onlinewardleymaps.com |
| Board pack playbook | `reference/SOTA_USE_CASES.md` use case 3-4 + NVCA + Sequoia template | https://www.imboard.ai/blog/alternatives-to-diligent-boards |
| Investor update playbook | `reference/SOTA_USE_CASES.md` use case 5 + Visible.vc | https://visible.vc/blog/investor-update-software/ |
| Executive hiring playbook | `reference/SOTA_USE_CASES.md` use case 7 + Geoff Smart topgrading | https://www.index.dev/blog/greenhouse-vs-lever-vs-ashby-ats-comparison |
| OKR cascade playbook | `reference/SOTA_USE_CASES.md` use case 9 + Christina Wodtke radical focus | https://mooncamp.com/blog/best-okr-software |
| Decision frameworks playbook | `reference/SOTA_USE_CASES.md` use case 10-11 + Atlassian + Klein + Duke | https://www.atlassian.com/team-playbook/plays/daci + https://www.gary-klein.com/premortem |
| All-hands playbook | `reference/SOTA_USE_CASES.md` use case 12 + Lenny Rachitsky format | https://www.lennysnewsletter.com/p/how-to-write-a-great-weekly-update |
| QBR playbook | `reference/SOTA_USE_CASES.md` use case 13 + Stellafai 5-component template | https://www.stellafai.com/post/how-to-run-a-stellar-quarterly-business-review-meeting |
| Annual planning playbook | `reference/SOTA_USE_CASES.md` use case 14 + David Sacks cadence | https://www.capitaly.vc/blog/david-sacks-operating-cadence-weekly-metrics-okrs-ceo-dashboard |
| Calendar audit playbook | `reference/SOTA_USE_CASES.md` use case 17 + Motion/Reclaim/Sunsama comparison | https://temporal.day/blog/motion-vs-reclaim-vs-clockwise-vs-akiflow-vs-sunsama |
| KPI dashboard playbook | `reference/SOTA_USE_CASES.md` use case 18 + Causal/Mosaic/Visible/Finmark | https://valueaddvc.com/blog/best-financial-modeling-tools-for-startups-excel-vs-runway-vs-causal-vs-mosaic |
| Crisis comms playbook | `reference/SOTA_USE_CASES.md` use case 19 + standard 5-archetype playbook | https://www.theempiremag.com/the-ceo-playbook-2026/ |
| M&A framework playbook | `reference/SOTA_USE_CASES.md` use case 20 + Wardley overlay + standard DCF | https://medium.com/@haberlah/build-vs-buy-in-2026-using-wardley-mapping-to-navigate-the-agentic-ai-shift-be24d534b054 |
| Operating cadence playbook | `reference/SOTA_USE_CASES.md` use case 21 + David Sacks | https://www.capitaly.vc/blog/david-sacks-operating-cadence-weekly-metrics-okrs-ceo-dashboard |
| Antipattern catalog | Synthesized BAD/GOOD pairs from the 7 documented antipatterns CEOs hit (bad strategy / two-approver DACI / vague scorecard / status-update all-hands / no pre-mortem / no-lowlights update / skipped references) | |
| Reference patterns | Standard pre-mortem / weekly metrics review / 1:1 templates synthesized from playbooks above | |
| SOTA tool reference | `reference/SOTA_USE_CASES.md` per-tool entries + web research June 2026 | One H3 per tool — grep-friendly |
| SOTA execution playbook table | `reference/SOTA_USE_CASES.md` summary table mapped to user-ask phrasing | |

## SOTA tool sources (June 2026)

> One row per SOTA tool referenced in the agent. All URLs verified via web search.

| Tool | Source URL | Used for |
|---|---|---|
| Rumelt — Good Strategy / Bad Strategy | https://cutlefish.substack.com/p/tbm-332-the-last-strategy-framework | Strategy doc spine, bad-strategy checklist |
| OGSM framework | https://www.masterclass.com/articles/ogsm | Strategy operating format |
| V2MOM framework | Salesforce canonical reference (Marc Benioff) | Strategy operating format alt |
| Wardley Maps | https://medium.com/@haberlah/build-vs-buy-in-2026-using-wardley-mapping-to-navigate-the-agentic-ai-shift-be24d534b054 | Competitive landscape mapping |
| OnlineWardleyMaps | https://onlinewardleymaps.com | Free public Wardley map text syntax + render |
| Hamilton Helmer 7 Powers | https://7powers.com | Moat analysis in strategy doc |
| NVCA Model Documents | https://nvca.org | Board governance + Series Seed/A model docs |
| Cooley GO Board templates | https://www.cooleygo.com | Board consent, written consents, minutes templates |
| Sequoia Pitch Deck template | https://www.sequoiacap.com (Sequoia archive) | Board update + fundraising deck spine |
| I'mBoard / Boardable / OnBoard / Diligent | https://www.imboard.ai/blog/alternatives-to-diligent-boards + https://appdeck.com/blog/board-portal-software-comparison-2026 | Board portal selection by stage |
| Granola / Fathom / Fireflies / Otter | https://meetingnotes.com/blog/best-ai-note-takers + https://www.granola.ai/blog/meeting-note-tool-pricing-granola-vs-fireflies-fathom-otter | AI meeting transcription routing |
| Visible.vc | https://visible.vc/blog/investor-update-software/ + https://visible.vc/investor-updates/ | Monthly/quarterly investor updates |
| Carta | https://carta.com/best-cap-table-software/ | Cap table + investor reporting (Series A+) |
| AngelList Stack Updates | https://startupowl.com/reviews/angellist | Free investor update fallback |
| DocSend | https://docsend.com | Tracked-link data room distribution |
| Greenhouse / Ashby / Lever | https://www.index.dev/blog/greenhouse-vs-lever-vs-ashby-ats-comparison + https://www.ashbyhq.com/ | Executive recruiting ATS |
| Geoff Smart "Who" (topgrading) | https://geoffsmart.com (canonical) | Outcomes-first scorecard + 360 references |
| True Search / SPMB / Heidrick & Struggles | Industry-standard retained-search firms | C-level retained search |
| Mooncamp | https://mooncamp.com/blog/best-okr-software | OKR platform — design-conscious teams <150 |
| Lattice Goals + 1:1s | https://www.tability.io/compare/platform/lattice + https://lattice.com/api-docs | OKRs + 1:1s + reviews HR-integrated |
| WorkBoard (Quantive acq.) | https://mooncamp.com/blog/best-okr-software | OKR — 200+ employees, auto-tracking |
| Christina Wodtke "Radical Focus" | https://eleganthack.com | OKR philosophy — one O + three KRs |
| Atlassian DACI | https://www.atlassian.com/team-playbook/plays/daci | Single-Approver decision framework |
| RACI / DACI / RAPID comparison | https://dectrack.com/en/blog/decision-models-raci-daci-rapid | Decision framework chooser |
| Gary Klein pre-mortem | https://www.gary-klein.com/premortem | Pre-mortem method (~30% better risk ID) |
| Annie Duke decision journal | https://grahammann.net/book-notes/how-to-decide-annie-duke | Decision journal template |
| Lenny Rachitsky weekly update | https://www.lennysnewsletter.com/p/how-to-write-a-great-weekly-update | All-hands + weekly update format |
| Gamma | https://posteverywhere.ai/blog/15-best-ai-presentation-makers | Deck generation (default — Tome shutdown 2025) |
| Beautiful.ai | https://posteverywhere.ai/blog/15-best-ai-presentation-makers | Deck generation — PPT compatibility, brand controls |
| QBR 5-component template | https://www.stellafai.com/post/how-to-run-a-stellar-quarterly-business-review-meeting + https://www.sybill.ai/blogs/qbr-templates-agendas-and-best-practices | QBR structure |
| David Sacks operating cadence | https://www.capitaly.vc/blog/david-sacks-operating-cadence-weekly-metrics-okrs-ceo-dashboard | Weekly/monthly/quarterly/annual rhythm |
| HashiCorp operating cadence | https://www.hashicorp.com/en/how-hashicorp-works/articles/operating-cadence | Operating-cadence-doc reference |
| Tella / Vidyard / Zight / Berrycast | https://zight.com/blog/best-loom-alternatives-2026/ + https://supademo.com/blog/loom-alternatives | Async video comms |
| Motion / Reclaim / Sunsama / Akiflow / Morgen | https://temporal.day/blog/motion-vs-reclaim-vs-clockwise-vs-akiflow-vs-sunsama + https://arahi.ai/blog/best-time-blocking-apps-and-planners-2026 | Calendar protection |
| Causal | https://valueaddvc.com/blog/best-financial-modeling-tools-for-startups-excel-vs-runway-vs-causal-vs-mosaic | FP&A — Seed-Series B default |
| Mosaic | https://valueaddvc.com/blog/best-financial-modeling-tools-for-startups-excel-vs-runway-vs-causal-vs-mosaic | FP&A — Series C+ standard |
| Finmark | https://www.g2.com/products/finmark/reviews | Startup-budgeting + KPI metrics dashboard |
| PitchBook | https://otio.ai/blog/cb-insights-vs-pitchbook | M&A + private-market enterprise intel ($20k+/yr) |
| CB Insights | https://otio.ai/blog/cb-insights-vs-pitchbook | M&A + trend-forward predictive intel |
| Crunchbase | https://otio.ai/blog/crunchbase-vs-pitchbook | Accessible startup + investor DB ($29-49/mo) |
| Tracxn | https://www.reviewadda.com/institute/article/518/tracxn-vs-crunchbase-vs-dealroom-vs-pitchbook-vs-cb-insights | Startup intelligence + sector mapping |
| The Empire Magazine — CEO Playbook 2026 | https://www.theempiremag.com/the-ceo-playbook-2026/ | 2026 CEO playbook + crisis comms framing |

## Notes on authored-from-synthesis

Sections that aren't directly lifted from a single source (rare — should always be operational glue, not domain claims):

- **soul.md — load-bearing convictions** — synthesized from Sacks (time as resource), Atlassian DACI (decisions over alignment), Geoff Smart (hire slow / fire fast). No single canonical phrasing — these are three CEO-canon truths consolidated.
- **soul.md — communication style examples** — paraphrased standard CEO operator phrasing (active voice, specificity), not lifted from one source.
- **soul.md — when to push back rules** — synthesized from the hard rules of each playbook (Rumelt, DACI, topgrading, pre-mortem, Lenny update, all-hands). No single canonical source for the consolidated push-back list.
- **role.md — antipattern catalog BAD/GOOD pairs** — synthesized from the 7 documented antipatterns commonly hit by early-stage CEOs. Each pair illustrates a rule from the playbooks above.
- **role.md — reference patterns (1:1 / weekly review / pre-mortem)** — operational glue distilled from the playbooks. Pre-mortem facilitation is lifted from Klein; 1:1 structure and weekly review structure are standard CEO operating patterns.
- **role.md — comp benchmarks table** — directional ranges from Pave / Carta Total Comp / Option Impact (industry-standard 2026 sources). Verify current data before use; ranges shift quarterly.

## Refreshing from upstream

When SOTA tools change (e.g., new OKR platform launch, board portal API release, Visible product change):
1. Update the relevant skill pack(s) in `agents/ceo-agent/skills/<name>/SKILL.md` (Round 2 build).
2. Update the SOTA sources table above.
3. Update `reference/SOTA_USE_CASES.md` confidence ratings if applicable.
4. Re-run `python verify.py ceo-agent` to confirm structure intact.
5. Re-build: `python build.py ceo-agent` produces a fresh `.craftbot`.

Known SOTA-shift signals to watch:
- **Clockwise EOL March 2026** — already reflected; check for any successor consolidation
- **Tome shut down March 2025** — already reflected; Gamma is the de-facto deck default
- **BoardEffect + OnBoard merger (Diligent)** — already reflected; check pricing tier shifts
- **Quantive acquired by WorkBoard** — already reflected; check WorkBoard product naming
- **Visible.vc API expansion** — refresh skill pack if KPI auto-sync coverage expands
- **AngelList Stack changes** — Stack cap table no longer accepting new customers (Aug 2026)
- **Lattice Goals API maturity** — check for OKR auto-cascade improvements

For the canonical reference repos (Step 2):
- `wshobson/agents` — repull every quarter for SOTA agent definitions (chief-of-staff, executive-coach if added)
- `VoltAgent/awesome-claude-code-subagents` — same cadence
- `msitarzewski/agency-agents` — same cadence
