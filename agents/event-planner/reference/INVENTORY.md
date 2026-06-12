# event-planner — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in SOTA_USE_CASES.md and SOURCES.md) plus the per-agent seed prompt's curated 2026 tool list.

For future tightening: pull 4-6 reference agents from wshobson/agents (look in `plugins/operations/` and `plugins/marketing/agents/`), VoltAgent/awesome-claude-code-subagents (categories `08-business-product/`, `06-customer-experience/`), msitarzewski/agency-agents (operations + marketing folders), vijaythecoder/awesome-claude-agents into `reference/agents/`, and 6-10 reference skills into `reference/skills/`.

Topics worth deeper upstream research before v2:

- Event management platform comparison 2026 (Cvent vs Bizzabo vs Splash vs Hopin vs Eventbrite vs Stova vs Hubilo vs Brella vs Whova)
- Hybrid event production playbooks (low-latency streaming + interactive Q&A + matchmaking)
- Sponsor contract deliverable tracking (legal-light contract enforcement workflows)
- Run-of-show format conventions (broadcast vs conference vs trade-show conventions)
- Event ROI measurement (MQL per event, pipeline-influenced revenue, CAC payback for event-sourced deals)
- Accessibility playbooks (ADA Title III, AccessibleArts.org standards, CART captioning, ASL interpretation booking)
- MPI/PCMA/IAEE 2026 industry standards
- Conference CFP/CFS programs (Sessionize / Papercall / Pretalx track-design conventions)

For now the SOTA mapping rests on per-platform docs + comparison posts (cited per row in `SOTA_USE_CASES.md`) and the seed prompt's tool list.
