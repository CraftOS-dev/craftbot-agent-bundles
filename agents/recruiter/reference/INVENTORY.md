# recruiter — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research, ATS / interviewing / offer / candidate experience / DEI / metrics platform documentation, and 2025-2026 recruiting-industry sources (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`).

This Round 1 build deliberately defers Round 2 (per-skill-pack `SKILL.md` contents) — `agent.yaml` reserves the 24 bundled skill-pack names; the folders under `skills/<name>/` are populated by a separate runtime build subagent.

For future tightening: pull 4-6 reference agents from wshobson/agents, VoltAgent/awesome-claude-code-subagents, msitarzewski/agency-agents, vijaythecoder/awesome-claude-agents into `reference/agents/`, and 6-10 reference skills (Greenhouse Inclusion, Karat interview-as-a-service, Goodtime scheduling, Pave / Levels.fyi comp intel, Checkr background checks, Glassdoor employer brand) into `reference/skills/`.

## Sibling agents this recruiter coordinates with

- `talent-sourcer` — top-of-funnel sourcing (sibling specialist; hands candidates over on "Applied" stage)
- `operations-agent` — parent (broader HR/IT ops + payroll + onboarding + handbook)
- `ceo-agent` — exec hiring strategy, comp philosophy, board-level talent decisions
- `legal-counsel` — binding employment-law / offer-letter wording / non-compete / EEO
- `marketing-agent` — long-form employer-brand campaigns + paid recruitment ads

## Coverage breakdown (June 2026)

- 33 mapped use cases in `SOTA_USE_CASES.md`
- 24 bundled SOTA skill packs reserved in `agent.yaml` (Round 2 will populate `SKILL.md` files)
- 39 CraftBot default skills enabled (already shipped on recipient's install)
- 27 MCP servers enabled (every name verified against `app/config/mcp_config.json`)
- ~95% fulfillment (the ⚠ rows are "the recipient owns the paid seat" — every gap has a free fallback path)
