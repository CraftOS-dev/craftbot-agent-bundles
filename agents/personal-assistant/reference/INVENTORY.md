# personal-assistant — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in SOTA_USE_CASES.md and SOURCES.md) and from the seed prompt's curated 2026 SOTA tool lists across calendar/scheduling, email triage, travel booking, expense tracking, restaurant reservations, meeting note capture, task management, errand routing, gift research, contact management, password management, async video, family calendar coordination, and vacation planning.

The seed prompt enumerated 25+ use cases and 18 bundled skill packs reserved for Round 2, all cross-referenced against the CraftBot MCP catalog and default-skill folder in this build pass. The closest sibling agent (`operations-agent`) covers company-scale HR/IT/vendor ops; the closest exec-level sibling (`ceo-agent`) covers strategic executive work. The personal-assistant fills the **individual** workflow gap — personal calendar, personal travel, personal errands, gift shopping, restaurant reservations, family coordination — and routes binding tax/legal questions away (personal taxes are not in scope).

For future tightening: pull 4-6 reference agents from `wshobson/agents` (any `plugins/personal-assistant/` or `plugins/productivity/`), `VoltAgent/awesome-claude-code-subagents` (`categories/productivity/` if present), `msitarzewski/agency-agents` (EA / chief-of-staff / lifestyle-manager specialists), and 6-10 reference skills (Calendly / Cal.com scheduling recipes, Motion / Reclaim.ai calendar protection, TripIt / Hopper travel orchestration, Expensify / Ramp expense capture, OpenTable / Resy reservation, Granola / Fathom meeting note extraction, Todoist / Things task management, 1Password CLI recipes) into `reference/agents/` and `reference/skills/`.

Sources considered but not downloaded in v1:
- `github.com/wshobson/agents` — no dedicated personal-assistant plugin observed as of build date (June 2026); operations adjacent agents may overlap. Recheck quarterly.
- `github.com/VoltAgent/awesome-claude-code-subagents` — no dedicated EA agent observed; productivity adjacent agents may exist (recheck).
- `github.com/msitarzewski/agency-agents` — strong on agency / marketing roles; EA / chief-of-staff coverage thin (recheck for EA / scheduling-coordinator agents).
- `github.com/JSONbored/claudepro-directory` — search for `assistant` / `scheduling` / `task` / `email-triage` skills.
