# talent-sourcer — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research and the seed list in the build prompt (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`).

For future tightening: pull 4-6 reference agents from `wshobson/agents` (recruiter, talent-sourcer, people-ops), `VoltAgent/awesome-claude-code-subagents` (categories/08-business-product/recruiter), `msitarzewski/agency-agents` (people/recruiter, people/talent-sourcer), and `vijaythecoder/awesome-claude-agents` into `reference/agents/`. Pull 6-10 reference skills (linkedin-boolean-builder, github-sourcing-cli, dovetail-style-talent-crm, gem-sequence-author, etc.) into `reference/skills/`.

## Reference Agents (planned for v2)

| File | Source | Status |
|---|---|---|
| `agents/wshobson-recruiter.md` | https://github.com/wshobson/agents/tree/main/plugins/people-ops/agents | not downloaded |
| `agents/voltagent-recruiter.md` | https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/recruiter.md | not downloaded |
| `agents/msitarzewski-recruiter.md` | https://github.com/msitarzewski/agency-agents/blob/main/people/recruiter.md | not downloaded |
| `agents/msitarzewski-sourcing.md` | https://github.com/msitarzewski/agency-agents/blob/main/people/sourcing.md | not downloaded |

## SOTA Research Sources (used in v1 build)

The SOTA mapping in `SOTA_USE_CASES.md` is grounded in 2025-2026 talent-sourcing practice across these published references (full URLs in `SOTA_USE_CASES.md` and `SOURCES.md`):

- LinkedIn Recruiter + Sales Navigator + Talent Solutions APIs (business.linkedin.com, developer.linkedin.com)
- LinkedIn Boolean search 2026 guide (talentprise.com, Built In, hireEZ)
- GitHub talent mining 2026 (hireEZ blog, Kula, Built In, Leoforce)
- SeekOut / Findem / AmazingHiring diversity sourcing + 800M+ profile graphs (selectsoftwarereviews.com, juicebox.ai/seekout, leonar.app)
- Gem AI-first sourcing CRM with 800M+ profiles + sequencing (gem.com, selectsoftwarereviews.com)
- hireEZ AI Boolean builder + 45+ platform aggregation (explore.hireez.com)
- Beamery enterprise talent CRM (beamery.com)
- Phenom / Eightfold AI / Symphony Talent (SmashFly) talent experience platforms
- Loxo / Leonar / Juicebox / Manatal AI sourcing platforms
- Contact-finder APIs: Apollo, Clay, Lusha, Hunter.io, Snov.io, RocketReach, AnyMail Finder, Findymail, ContactOut, Derrick
- Apollo.io 275M+ contacts + Crunchbase 4M+ company graph
- Wellfound (formerly AngelList Talent) 35K+ companies + Hired curated matching
- Built In US tech hubs + Otta curated startup roles
- Toptal (top 3%) + Turing (24h match) + Andela (Africa-focused) + Arc.dev (1% accept) + Lemon.io (24-48h, startup focus)
- RepVue sales talent + compensation transparency (repvue.com)
- Textio + Datapeople inclusive job description optimization
- Dribbble + Behance designer portfolio sourcing
- ATS integration: Greenhouse + Lever + Ashby APIs (handoff target)
- Stack Overflow developer profile sourcing (Jobs discontinued 2022; reputation + tags still searchable)
- Cold InMail 2026 response rate playbooks: <400 chars + 16-27-char subjects + 78% lift from profile-view-first
- Diversity sourcing channels: /dev/color, Code2040, Black Founders Matter, Lesbians Who Tech, Out in Tech, Latinas in Tech, Project Include
- Boomerang / alumni networks: 35% of 2025 hires returning; $4,200/hire savings (Bain, 50+ corp alumni programs)
- Vetted contractor marketplaces for fractional/specialist hires

## Sources Considered But Not Downloaded

| Source | Why excluded |
|---|---|
| Sourcing.io, Hiretual (legacy hireEZ name), Entelo (acquired) | hireEZ + SeekOut cover the aggregator surface; Entelo absorbed |
| Indeed Recruiter, Monster, ZipRecruiter | High-volume job-board surface is sourced via ATS posting integrations, not direct outreach; out of scope for talent-sourcer |
| Workable, Recruitee, BambooHR ATS | Greenhouse / Lever / Ashby cover the recruiter-facing ATS handoff; others mapped via cli-anything fallback |
| Jobvite Engage, Bullhorn | Agency-recruiter surfaces; talent-sourcer is in-house focused |
| Restless Bandit, Ideal AI (legacy AI sourcing) | SeekOut + Eightfold absorbed the AI matching surface |

---

**v1 build approach:** SOTA-driven from published 2025-2026 sources. The agent ships with strong execution paths for every documented use case via LinkedIn Boolean strings authored programmatically, GitHub talent mining via REST + cli-anything, SeekOut / Findem / AmazingHiring / hireEZ aggregator routing, Gem / Beamery talent-CRM sequencing, Apollo / Clay / RocketReach / Findymail contact enrichment, Greenhouse / Ashby / Lever ATS handoff, Toptal / Turing / Andela / Arc.dev / Lemon.io vetted-marketplace routing, Textio / Datapeople JD optimization, Dribbble / Behance + RepVue niche sourcing, and `cli-anything` + curl for any remaining gap. Sourcing strategy, Boolean authoring, multi-channel diversification, outreach campaigns, hot-list management, target-company mapping, and metrics all have named SOTA execution paths.
