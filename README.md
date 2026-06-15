![CraftBot Agent Bundles](assets/craftbot_top_banner.jpg)

# 💼 CraftBot Agent Bundles

**Turn stock [CraftBot](https://github.com/CraftOS-dev/CraftBot) into a senior specialist with one click.**

Import a `.craftbot` file into the CraftBot, your agent walks in as a CEO, lawyer, marketing lead, Python engineer, video producer, or 37 others. No prompt engineering. No system-prompt wrangling. Already wired to the right MCPs and skills for the job.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agents](https://img.shields.io/badge/Agents-42-success)](#the-catalog)
[![Skill packs](https://img.shields.io/badge/Skill%20packs-800%2B-blueviolet)](#whats-actually-inside-a-bundle)
[![SOTA fulfillment](https://img.shields.io/badge/SOTA%20fulfillment-%E2%89%A590%25-brightgreen)](#why-these-arent-just-prompts)
[![Built for CraftBot](https://img.shields.io/badge/Built%20for-CraftBot-orange)](https://github.com/CraftOS-dev/CraftBot)
[![Quality gates](https://img.shields.io/badge/Quality%20gates-13-informational)](verify.py)

> Your CraftBot deserve a role.

---

## 👉 Stop "prompting" an AI. Start hiring one.

Most agent repos give you a 600-word system prompt and call it a day. The agent sounds confident. Then you ask it to actually *send the investor update* — and it tells you what *you* should do.

Every bundle in this repo went through a research pipeline that asks one question, per use case, per role:

> **"What is the 2026 SOTA way for an autonomous agent to actually execute this task?"**

The answer becomes a real wiring decision — an MCP server, a SOTA skill pack, a CLI tool, an API. Not a paragraph of advice.

The result, per agent on average:

| Metric | Per agent |
|---|---|
| Bundled SOTA skill packs (the **hands** of the agent) | **~22** |
| CraftBot default skills enabled | **~23** |
| MCP servers pre-wired | **~22** |
| Use cases verified executable end-to-end | **≥90%** |
| Lines of cited reference research | **~3,000** |
| Sources cited in `SOURCES.md` | **20–80** |

That is the difference between a *prompt* and an *operator*.

---

## 🧰 Quick start (60 seconds)

1. **Install [CraftBot](https://github.com/CraftOS-dev/CraftBot)** — self-hosted, BYOK (Claude / GPT / Gemini / Ollama), Win/Mac/Linux.
2. **Download a bundle** from [`bundles/`](bundles/) — pick by role and date stamp (e.g. `ceo-agent-20260611.craftbot`).
3. **Drag it into CraftBot's Settings → Import Agent Profile.**
4. CraftBot imports the SOUL (persona + operating rules), the bundled skills, and recommends which MCP servers to enable. You fill in API keys for the platforms you actually use.
5. Talk to your new specialist. It will ask 2–3 questions about your routines and offer to schedule them proactively.

That's it. No CLI install, no `.cursorrules`, no plugin marketplace, no `claude.md` mosaic.

---

## 👔 The catalog (42 agents, growing more and more)

Every agent is either a **General** (covers a whole domain end-to-end — good for solo founders) or a **Specialized** (drills deep into a niche — good for teams composing a roster). Most domains ship both. Users compose.

### 🎯 Executive & Strategy

| Agent | Tier | Skills | MCPs | What can they do |
|---|---|---|---|---|
| [`ceo-agent`](agents/ceo-agent/) | General | 47 | 27 | Drafts strategy docs, board packs, investor updates, OKR cascades, all-hands prep, decision logs |
| [`project-manager`](agents/project-manager/) | General | 62 | 21 | Executes cross-functional deliverables, charters, WBS, Gantt charts, status reports, retros |
| [`operations-agent`](agents/operations-agent/) | General | 49 | 29 | Runs end-to-end business operations: ATS, HRIS, procurement, tool-building, workflow automation |
| [`finance-agent`](agents/finance-agent/) | General | 46 | 22 | Authors FP&A models, capital allocation frameworks, term sheets, fundraising pitch materials |
| [`growth-agent`](agents/growth-agent/) | General | 47 | 12 | Designs growth loops, activation mechanics, retention strategies, experimentation, attribution frameworks |
| [`investor-relations`](agents/investor-relations/) | General | 47 | 27 | Prepares investor updates, earnings materials, SEC filings, analyst relations management |

### ⚙️ Engineering

| Agent | Tier | Skills | MCPs | What can they do |
|---|---|---|---|---|
| [`senior-python-engineer`](agents/senior-python-engineer/) | Specialized | 43 | 5 | Writes, reviews, debugs, refactors, and optimizes Python code with advanced tooling |
| [`devops-engineer`](agents/devops-engineer/) | Specialized | 35 | 8 | Ships and operates production infrastructure: containers, Kubernetes, IaC, GitOps, CI/CD |
| [`frontend-engineer`](agents/frontend-engineer/) | Specialized | 38 | 11 | Writes, reviews, debugs, refactors, tests, audits, and deploys production frontend code |
| [`qa-engineer`](agents/qa-engineer/) | Specialized | 37 | 11 | Owns test strategy, suite infrastructure, cross-cutting quality, accessibility, performance, security |

### 📈 Marketing & Growth

| Agent | Tier | Skills | MCPs | What can they do |
|---|---|---|---|---|
| [`marketing-agent`](agents/marketing-agent/) | General | 39 | 20 | Runs end-to-end marketing: content strategy, SEO, social, email, growth loops |
| [`video-creator`](agents/video-creator/) | Specialized | 30 | 20 | Produces marketing videos: scripts, editing, color grading, audio, subtitles, YouTube optimization |
| [`seo-specialist`](agents/seo-specialist/) | Specialized | 37 | 17 | Executes technical SEO: cannibalization audits, log analysis, programmatic SEO, AEO strategies |
| [`email-strategist`](agents/email-strategist/) | Specialized | 38 | 16 | Manages email lifecycle: DMARC setup, IP warming, segmentation, post-MPP measurement |
| [`ads-specialist`](agents/ads-specialist/) | Specialized | 41 | 25 | Operates paid-ads campaigns: Meta, Google, TikTok, LinkedIn, SKAN 4.0, MMM modeling |
| [`content-creator`](agents/content-creator/) | Specialized | 40 | 26 | Creates multi-format content: newsletters, podcasts, repurposing, cross-platform publishing |
| [`social-media-manager`](agents/social-media-manager/) | Specialized | 41 | 31 | Manages social platforms: publishing, community engagement, influencer outreach, social commerce |
| [`pr-comms`](agents/pr-comms/) | General | 41 | 36 | Executes PR and comms: media relations, press releases, crisis comms, thought leadership |
| [`community-manager`](agents/community-manager/) | General | 38 | 27 | Operates end-to-end communities: platform selection, moderation, engagement, events, CAB management |

### 💰 Sales & Customer

| Agent | Tier | Skills | MCPs | What can they do |
|---|---|---|---|---|
| [`sales-agent`](agents/sales-agent/) | General | 48 | 26 | Runs end-to-end revenue: outreach, CRM management, pipeline, deal coaching, proposals |
| [`sales-ops`](agents/sales-ops/) | Specialized | 44 | 19 | Operates sales systems: CRM admin, commission management, CPQ, lead routing, forecasting |
| [`customer-success`](agents/customer-success/) | General | 49 | 25 | Executes customer success: onboarding, QBRs, health scoring, NRR/GRR, expansion, renewals |
| [`customer-support-agent`](agents/customer-support-agent/) | General | 37 | 21 | Manages customer support: triage, templates, FAQ, escalation, SLA tracking, sentiment analysis |

### 🎬 Content & Documentation

| Agent | Tier | Skills | MCPs | What can they do |
|---|---|---|---|---|
| [`technical-writer`](agents/technical-writer/) | Specialized | 36 | 9 | Writes developer documentation: READMEs, API references, tutorials, ADRs developers actually use |
| [`docgen-automation`](agents/docgen-automation/) | Specialized | 48 | 23 | Automates document creation: templates, conditional assembly, e-signatures, AI extraction, CLM |
| [`knowledge-base-manager`](agents/knowledge-base-manager/) | Specialized | 37 | 17 | Designs knowledge bases: taxonomy, search optimization, analytics, deflection measurement, localization |
| [`l10n`](agents/l10n/) | Specialized | 39 | 13 | Ships product locales: TMS pipelines, CAT tools, translation memory, RTL/CJK testing |
| [`grant-writer`](agents/grant-writer/) | General | 50 | 20 | Researches grants, drafts LOIs, ensures compliance, manages submissions, handles reporting requirements |

### 🔬 Research & Analytics

| Agent | Tier | Skills | MCPs | What can they do |
|---|---|---|---|---|
| [`research-analyst`](agents/research-analyst/) | General | 40 | 16 | Investigates topics, evaluates sources, synthesizes insights, delivers actionable findings with attribution |
| [`data-analyst`](agents/data-analyst/) | Specialized | 44 | 16 | Performs warehouse SQL analysis: dbt, cohort analysis, A/B testing, attribution, anomaly detection |
| [`ux-researcher`](agents/ux-researcher/) | Specialized | 54 | 18 | Conducts end-to-end UX research: planning, usability testing, IA testing, JTBD, personas |
| [`competitive-intelligence`](agents/competitive-intelligence/) | Specialized | 53 | 21 | Monitors competitors continuously, authors battlecards, integrates win/loss CI using public sources |

### ⚖️ Legal, Compliance & Finance

| Agent | Tier | Skills | MCPs | What can they do |
|---|---|---|---|---|
| [`legal-counsel`](agents/legal-counsel/) | General | 42 | 12 | Reviews contracts, drafts T&Cs, covers IP basics, GDPR/CCPA, equity grant documentation |
| [`compliance-agent`](agents/compliance-agent/) | General | 50 | 18 | Manages compliance: SOC 2, ISO 27001, GDPR, CCPA, HIPAA, PCI DSS, AML/KYC, TPRM |
| [`finance-controller`](agents/finance-controller/) | General | 45 | 22 | Operates end-to-end finance: bookkeeping, monthly close, cash forecasting, SaaS metrics, cap table |
| [`tax-agent`](agents/tax-agent/) | Specialized | 44 | 19 | Prepares tax filings: federal, state, multi-jurisdiction, R&D credits, QSBS, transfer pricing |

### 🌱 People, Product & Personal

| Agent | Tier | Skills | MCPs | What can they do |
|---|---|---|---|---|
| [`product-manager`](agents/product-manager/) | General | 57 | 18 | Discovers user needs, prioritizes roadmap, defines specs, manages cross-functional product execution |
| [`recruiter`](agents/recruiter/) | Specialized | 63 | 27 | Sources, screens, interviews candidates; negotiates offers; manages hiring pipeline end-to-end |
| [`talent-sourcer`](agents/talent-sourcer/) | Specialized | 54 | 21 | Identifies top talent, sources passive candidates, builds pipeline, creates talent benchmarks |
| [`event-planner`](agents/event-planner/) | General | 41 | 34 | Plans events end-to-end: venue selection, budgeting, logistics, vendor management, post-event analysis |
| [`personal-assistant`](agents/personal-assistant/) | General | 59 | 56 | Manages schedules, email, travel, expenses, research, administrative tasks for busy executives |
| [`bd-partnerships`](agents/bd-partnerships/) | General | 47 | 30 | Identifies partnership opportunities, structures deals, manages relationship lifecycles, expansion planning |

**Catalog totals:** 42 agents · ~1,900 skill enables · ~920 MCP enables · 805+ bundled SOTA skill packs.

---

## What's actually inside a bundle

A `.craftbot` file is a zip. Unzip one to see exactly what gets imported:

```
ceo-agent-20260611.craftbot
├── manifest.json              ← bundle metadata + content inventory
├── README.md                  ← human-readable summary of this specific agent
├── profile/
│   ├── SOUL.md                ← persona + operating rules (ALWAYS-on context)
│   └── AGENT.md               ← deep reference (grep-only, not in default context)
├── skills/
│   ├── enabled.json           ← list of skills to enable
│   └── <bundled-skill>/SKILL.md   ← shipped SOTA capability packs (the agent's "hands")
└── mcp/
    └── servers.json           ← MCP servers to enable; secrets stripped, you fill keys
```

Per-agent source (under [`agents/<slug>/`](agents/)) also ships:

- `USE_CASES.md` — what the agent can execute today, with explicit caveat table for the rest. **Honest about gaps.** If something needs a paid API or hits a hard wall, it says so up top.
- `SOURCES.md` — every section in SOUL.md / AGENT.md mapped back to a downloaded reference file. No "trust me, bro."
- `reference/SOTA_USE_CASES.md` — per-use-case SOTA tool mapping. The research artifact that drove the bundle's wiring.

---

## ✨ Why these aren't just prompts

The repo is held to a methodology — see [METHODOLOGY.md](METHODOLOGY.md) — that the build pipeline enforces. Every bundle passes 13 automated gates before [`build.py`](build.py) will emit a zip:

1. **`agent.yaml` parses + has required fields**
2. **`soul.md` token discipline** — soft warn at 400 lines, hard fail at 600 (this is in your context every turn — every line costs forever)
3. **Operator framing** — `soul.md` intro window is scanned for banned advisory verbs (`covers`, `leans on`, `expertise spans`, `advise`, `guide`, `suggest`). Hard fails unless balanced by ≥4 action verbs (`writes`, `ships`, `runs`, `queries`, `deploys`). The agents are operators, not advisors.
4. **`role.md` has a SOTA tool reference section** — grep target
5. **`USE_CASES.md` present**
6. **`SOURCES.md` present** — provenance audit
7. **`reference/SOTA_USE_CASES.md` present** — Phase-B research artifact
8. **Every `enabled_skills` name resolves** — bundled folder or CraftBot default
9. **Every bundled `SKILL.md` exists and is non-trivial**
10. **Every `mcp_servers` name exists** in CraftBot's MCP catalog
11. **No inline citations** (`[from:` / `[merged:`) leaking into context — citations live in SOURCES.md
12. **PROACTIVE self-init footer present** in `soul.md` — same wording everywhere; the agent asks about routines on first run and offers to schedule them
13. **Fulfillment ≥90%** parsed from `SOTA_USE_CASES.md` — below 90% means the research isn't done

Run it yourself:

```bash
python verify.py                  # all agents, 13 gates each
python verify.py ceo-agent        # one agent
python build.py                   # builds dist/*.craftbot (refuses if verify fails)
python build.py senior-python-engineer
```

---

## What CraftBot uniquely enables (and why these bundles only work here)

CraftBot isn't another wrapper around a chat completion. It is **"the agent that builds and operates its own SaaS tools."** These bundles are designed around three CraftBot-specific capabilities:

- **Living UI** — agents can build / evolve / read / write their own small custom apps inside CraftBot. The CEO agent's KPI dashboard, the recruiter's scorecard board, the analyst's report draft — these aren't markdown, they're live apps the agent runs.
- **Memory + RAG + daily distillation** — agents remember your company name, runway, board members, last quarter's OKRs across sessions. No re-onboarding every conversation.
- **Proactive scheduling** — every bundle's `SOUL.md` ends with the same PROACTIVE footer. On first conversation the agent asks 2–3 routine questions and proposes a `PROACTIVE.md` that fires those routines on a schedule. The CEO agent runs your weekly board pack pull. The IR agent runs your monthly investor update draft. The growth agent runs your weekly experiment readout.

Try to import a `.craftbot` into Claude Code or Cursor and it will not work. By design. These bundles assume the host knows how to run skills, enable MCPs, and host Living UI apps.

---

## Bundles you can hire today

Pick a role. The bundle is in [`bundles/`](bundles/) named `<slug>-<YYYYMMDD>.craftbot`. The most recent date stamp is the current version.

```
bundles/ceo-agent.craftbot                       131 KB
bundles/senior-python-engineer.craftbot          115 KB
bundles/marketing-agent.craftbot                 113 KB
bundles/video-creator.craftbot                    80 KB
bundles/legal-counsel.craftbot                   160 KB
... and more
```

Bundles are deliberately small (<300 KB) because CraftBot defaults aren't re-shipped — only **SOTA skill packs that aren't already on the recipient's install** travel inside the zip.

---

## 🛠️ Build your own agent bundle

The pipeline is the README. Read [METHODOLOGY.md](METHODOLOGY.md) front to back, then look at [`agents/senior-python-engineer/`](agents/senior-python-engineer/) as a worked example. The 10-step workflow in short:

1. Plan the agent — add a row to [PROGRESS.md](PROGRESS.md)
2. Research and download SOTA references — 4–8 reference agents + 8–15 reference skill packs, verbatim, into `agents/<slug>/reference/`
3. Build `INVENTORY.md` and **pause for approval** — the proof you researched
4. Map ≥15 use cases, research SOTA per use case → `reference/SOTA_USE_CASES.md`
5. Compose `agent.yaml` — every catalog-matched MCP and bundled skill from Step 4 included
6. Compose `soul.md` (always-on, lean) + `role.md` (grep-only, deep)
7. Write `SOURCES.md` — section→source map
8. Write `USE_CASES.md` — honest execution table
9. Run `python verify.py <slug>` until all 13 gates pass
10. Run `python build.py <slug>` to emit the `.craftbot`

Contributions welcome. The bar is: pass [`verify.py`](verify.py), ≥90% fulfillment, every line cited.

---

## Acknowledgements

This repo would not exist without the open work of:

- **[CraftOS-dev/CraftBot](https://github.com/CraftOS-dev/CraftBot)** — the agent runtime these bundles target.
- **[wshobson/agents](https://github.com/wshobson/agents)** (192 agents, 156 skills) — primary reference for engineering / data / infra skill packs.
- **[VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)** (154 agents) — primary reference for category structure and language specialists.
- **[msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)** (232 agents) — primary reference for agency / marketing / specialized creator roles.
- **[vijaythecoder/awesome-claude-agents](https://github.com/vijaythecoder/awesome-claude-agents)** (24 agents) — primary reference for framework specialists and orchestration patterns.

Where a bundled `SKILL.md` was derived from one of these upstream packs, the source URL is in the file's opening HTML comment, and the source is mirrored in `SOURCES.md`. We stand on shoulders.

---

## License

[MIT](LICENSE). Bundles, methodology, and pipeline are all yours to fork, repackage, and resell. In this case, do cite the upstreams.

---

## Star history

If you find yourself coming back to this repo, **star it**. It tells contributors which bundles to prioritize next. Star count drives the next roster.
