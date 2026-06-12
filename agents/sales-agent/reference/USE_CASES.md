# Sales Agent — Use Cases

**Tier:** **general** · **Category:** sales
**Core job:** End-to-end revenue operations for solo founders and small revenue teams — outreach, CRM hygiene, pipeline review, qualification, deal coaching, proposals, win/loss, forecasting, expansion, renewal — across all the major sales platforms.

> Ships with the SOTA 2026 sales stack (HubSpot/Salesforce CRM, Apollo+Clay enrichment, Outreach/Salesloft/lemlist/Instantly sequences, Gong/Fathom call intelligence, PandaDoc/DocuSign proposals, MEDDIC/MEDDPICC/BANT/SPIN/Challenger qualification, Pocus/Koala/Common Room signals, Clari forecasting) — executes end-to-end, not just direct.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Outbound + prospecting
- Outbound sequence design (cold email + LinkedIn + phone cadence) — multi-channel, A/B subject+first-line, deliverability-passing
- Lead enrichment waterfall (Apollo → Clay → Lusha → ZoomInfo → Cognism)
- Account research (ICP fit scoring, account hierarchy, tech stack, funding stage, trigger events)
- LinkedIn Sales Navigator outreach (HeyReach / Phantombuster / TexAu at safe daily volumes)
- Cold email deliverability + sender warmup (SPF/DKIM/DMARC, 4-week warmup, mail-tester ≥ 9/10)

### Inbound + qualification
- Inbound lead qualification + scoring (firmographic + behavioral)
- Lead routing rules (round-robin / weighted / vertical / size-tier)
- SDR ↔ AE handoff with structured template + 4-hour acceptance SLA
- Qualification framework execution: MEDDIC / MEDDPICC / BANT / SPIN / Challenger (scoring rubric 0-3 per field)

### CRM + pipeline
- CRM hygiene + data quality (duplicates, stale archive, required-field enforcement)
- Pipeline review + stage hygiene (stage criteria, age-in-stage, stalled-deal detection, coverage ratio)
- Forecasting + commit accuracy (Commit / Best Case / Pipeline; per-AE slippage tracking)
- Pipeline reporting + dashboards (Notion / Google Sheets / PDF)

### Deal execution
- Discovery call prep (account research + SPIN questions + MEDDIC checklist + objection rehearsal)
- Demo prep (storyline, feature→pain mapping, battlecard, objection responses)
- Deal coaching per opportunity (single next-best-action with literal execution copy)
- Multi-threading enterprise deals (stakeholder map, engagement depth, content gifts to silent stakeholders)
- Negotiation prep (BATNA / ZOPA, anchoring strategy, concession ladder, closed-won comparables)
- Proposal generation + e-sign (PandaDoc / DocuSign with CRM-merge tokens)
- Pricing strategy (closed-won comparables, corridor + concession menu)
- Mutual action plans (MAPs) for deals > 60-day cycle

### Post-close
- Win/loss analysis (5-section structured post-mortem with tags for quarterly rollup)
- Customer expansion / upsell playbook (PLG signals → QBR → multi-team rollout)
- Renewal pipeline management (120-day pre-renewal opening with health scoring; save motion for at-risk)

### Intelligence + monitoring
- Call review (Gong / Chorus / Fathom / Fireflies / tl;dv — talk-listen ratio, monologue length, objections, sentiment)
- Signal/intent monitoring (Common Room + Pocus + Koala + Apollo job-changes + Crunchbase + BuiltWith)
- Daily hot-accounts digest with CRM task auto-creation

### Sales enablement
- Battlecards (per top competitor — positioning, traps, proof points)
- ROI calculators (input variables → computed outputs, rendered to xlsx/sheets)
- Case studies (rendered to docx/pdf from notion templates)
- Cross-agent coordination (ABM with marketing-agent; legal redlines deferred to legal-counsel; commission to finance-controller)

---

## Execution status (SOTA — June 2026)

The 2026 SOTA sales stack closes the historic "can advise, can't execute" gap. HubSpot/Salesforce/Apollo/Outreach/Salesloft/lemlist/Instantly/Gong/Fathom/Fireflies/PandaDoc/DocuSign/Calendly are all proxied via `api-gateway` managed OAuth; CRM-specific default skills exist for Attio, Pipedrive, Salesforce, Zoho CRM, Zoho Bigin; `cli-anything` handles dig/mail-tester/Glock Apps deliverability checks; PostgreSQL warehouse queries drive reporting; Slack/Teams handle notifications.

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Outbound sequence design | Outreach / Salesloft / lemlist / Instantly via managed OAuth | `api-gateway` (`outreach-salesloft-sequences` skill) |
| Lead enrichment waterfall | Apollo → Clay → Lusha → ZoomInfo | `api-gateway` + `cli-anything` (`apollo-clay-lead-enrichment` skill) |
| Account research | Apollo + Clay + LinkedIn + BuiltWith + Crunchbase + brave-search | `api-gateway` + `linkedin` + `brave-search` (`account-research-deep` skill) |
| LinkedIn Sales Nav outreach | HeyReach / Phantombuster / TexAu | `api-gateway` + `cli-anything` + `brightdata-mcp` |
| Cold email deliverability + warmup | dig + mail-tester + Glock Apps + Lemwarm + Instantly warmup | `cli-anything` + `api-gateway` |
| HubSpot CRM ops | HubSpot remote managed OAuth | `api-gateway` (`hubspot-sales-mcp` skill) |
| Salesforce CRM ops | Salesforce REST + SOQL via managed OAuth | `salesforce-api` skill + `api-gateway` |
| Attio / Pipedrive / Zoho CRM ops | Native default skills + `api-gateway` | `attio-api` / `pipedrive-api` / `zoho-crm` / `zoho-bigin` |
| Pipeline review + stage hygiene | CRM query + Python analysis | `api-gateway` + `cli-anything` (`pipeline-hygiene-stage-criteria` skill) |
| Qualification (MEDDIC/MEDDPICC/BANT/SPIN/Challenger) | CRM custom fields + Gong transcript signals | `api-gateway` + `gong-chorus-call-intelligence` |
| Discovery + demo prep | Composite: research + LinkedIn + past calls + battlecard | multiple skills |
| Deal coaching (next-best-action) | 7-signal composite → single NBA + literal copy | `deal-coaching-next-best-action` skill |
| Multi-threading enterprise | Stakeholder map + Sales Nav + content gifts via marketing-agent | `multi-threading-enterprise-deals` skill |
| Negotiation prep | BATNA / ZOPA / closed-won comps + concession ladder | composite |
| Proposal + e-sign | PandaDoc / DocuSign | `api-gateway` (`pandadoc-docusign-proposal-pipeline` skill) |
| Pricing strategy | Closed-won comp analysis (CRM + pandas) | `api-gateway` + `cli-anything` |
| Mutual action plans | MAP template + champion + close date | `notion` + `docx` |
| Win/loss post-mortem | Structured 5-section template + tags + rollup | `win-loss-analysis-structured` skill |
| Forecasting (Commit/BC/Pipeline) | CRM query + bucket categorization + per-AE breakdown | `clari-forecasting-commit-accuracy` skill |
| Call review (Gong/Fathom/Fireflies/tl;dv) | Transcript pull + talk-listen + objection mining | `gong-chorus-call-intelligence` skill |
| Signal/intent monitoring | Common Room + Pocus + Koala + Apollo + Crunchbase + BuiltWith | `signal-intent-monitoring-pocus-koala-common-room` skill |
| Customer expansion playbook | PostHog/Pocus usage + CRM + QBR deck | `expansion-upsell-renewal-playbook` skill + `posthog-mcp` |
| Renewal pipeline | CRM contract dates + usage trend + health score | `expansion-upsell-renewal-playbook` skill |
| CRM hygiene + data quality | Duplicate detection + stale archive + field enforcement | `api-gateway` + `postgresql-mcp` |
| Lead routing rules | HubSpot workflows / Salesforce assignment rules | `api-gateway` + `salesforce-api` |
| SDR ↔ AE handoff | Handoff template + CRM activity + Slack ping + Calendly | composite skills |
| Meeting booking | Calendly / HubSpot Meetings | `calendly-api` skill + `api-gateway` |
| Slack/Teams sales rooms | CRM webhook → channel post | `slack-mcp` + `ms-teams-mcp` |
| Battlecards + ROI calculators + case studies | pptx + xlsx + docx render from templates | `sales-enablement-battlecards-roi-calculators` skill |
| Sales reporting + dashboards | CRM query + render to Sheets/Notion/PDF | composite |
| ABM coordination | Cross-agent — target list owned here, ads via `marketing-agent` | hand-off |

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Apollo / Clay / Lusha / ZoomInfo | ⚠ | All require paid plans + API keys; `api-gateway` Apollo+Clay covered when Maton-onboarded; manual research + brave-search fallback always works |
| LinkedIn Sales Nav scraping | ⚠ | No public API; HeyReach/Phantombuster/TexAu use logged-in accounts; TOS-safe daily limits (15-25 connections, 50 profile views) — account-bound per rep |
| Common Room / Pocus / Koala | ⚠ | Paid signal platforms; manual fallback via Crunchbase + LinkedIn job-change feed + Apollo "company news" |
| Clari / BoostUp | ⚠ | Limited public API; manual forecast via CRM + Google Sheets always available |
| Chorus.ai | ⚠ | No public API; email-export integration is the workaround; Gong/Fathom/Fireflies/tl;dv have first-class APIs |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a concrete execution path. The historic "advise, don't execute" gaps are closed via shipped MCPs, managed OAuth via `api-gateway`, and dedicated default skills. The remaining 5% is paywalled signal/forecasting tools (recipient's own key) and LinkedIn TOS-sensitive scraping (account-bound by design).

---

## When to use this agent

- "Design a cold-email sequence for our SaaS aimed at VP Eng at 200-1000 employee companies"
- "Run a pipeline review and flag the deals at risk this quarter"
- "Score this deal using MEDDPICC and tell me where the gaps are"
- "Prep me for tomorrow's discovery call with Acme Corp"
- "Coach me on this deal — what's the next best action?"
- "Draft a mutual action plan for the Acme deal closing in 60 days"
- "Generate a proposal in PandaDoc for the $80K Acme deal"
- "Run the win/loss post-mortem on the deals we closed last month"
- "Build the Q3 forecast — Commit / Best Case / Pipeline by AE"
- "Set up cold-email warmup for our new outbound domain"
- "Enrich this list of 500 accounts with phone numbers and intent signals"
- "Pull last month's Gong calls and tell me where our reps are losing deals"
- "Plan the expansion motion for Acme — they hit usage threshold last week"
- "Build a battlecard for us vs. Competitor X"
- "Set up the renewal pipeline for Q4 — flag at-risk accounts"

## When NOT to use this agent

- Top-of-funnel content (blog posts, ads, brand voice, landing pages) — hand off to `marketing-agent`
- Post-sale support / customer issues / churn intervention — hand off to `customer-support-agent` (v1)
- Feature commitments / roadmap promises / product-market-fit hypotheses — hand off to `product-manager` (v1)
- Commission calculation / revenue recognition / pricing exceptions > 20% discount / finance models — hand off to `finance-controller` (v1)
- Contract redlines / MSA negotiation / DPA review — hand off to `legal-counsel` (v1)
- Deep market research / TAM sizing / competitive deep-dives over weeks — hand off to `research-analyst`
- Engineering work for the sales tech stack (e.g., build a Salesforce custom app, write Apex triggers) — hand off to `senior-python-engineer`
- Sales recruiting / SDR hiring / comp plan design — out of scope for this agent (v1+ specialist)
- CPQ implementation at enterprise scale (DealHub / Salesforce CPQ multi-tier) — this agent can design the rules; for full implementation, recommend a CPQ specialist (v1)
