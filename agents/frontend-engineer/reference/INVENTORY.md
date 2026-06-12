# frontend-engineer — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`) and from the curated SOTA tool seed list in the build prompt.

For future tightening: pull 4-6 reference agents from `wshobson/agents` (look in `plugins/frontend-development/agents/` and `plugins/web-development/agents/` — e.g., `react-pro`, `nextjs-pro`, `vue-expert`, `frontend-developer`, `web-performance-engineer`, `accessibility-auditor`), `VoltAgent/awesome-claude-code-subagents` (`categories/02-language-specialists/`, `categories/01-core-development/frontend-developer.md`, `categories/04-quality-security/`), `msitarzewski/agency-agents` (engineering folder), and `vijaythecoder/awesome-claude-agents` (framework specialists) into `reference/agents/`. Also pull 6-10 reference skills (React, Vue, Svelte, Next.js, accessibility, performance, testing) into `reference/skills/`.

---

## Sources Considered But Not Downloaded (v1 pass)

| Source | Why excluded for v1 |
|---|---|
| `wshobson/agents/plugins/frontend-development/skills/*` | Lower marginal value vs the curated 2026 SOTA seed list — pull in v1 tightening pass. |
| `anthropics/skills` (algorithmic-art, frontend-design, web-design-guidelines) | CraftBot already ships these as default skills — re-bundling would duplicate. |
| `vercel/next.js` examples, `withastro/docs`, `sveltejs/learn.svelte.dev` | Authoritative platform docs; cited directly in `SOTA_USE_CASES.md` rather than re-downloaded. |

---

## What gets used at composition time

`agent.yaml`, `soul.md`, `role.md`, `USE_CASES.md` are composed from:

1. The **SOTA tool seed list** in the build prompt (28 use cases × concrete 2025-2026 tools)
2. **Platform-authoritative docs** (react.dev, nextjs.org, vuejs.org, svelte.dev, astro.build, vitejs.dev, tailwindcss.com, playwright.dev, web.dev/vitals, w3.org/WAI/WCAG22) — cited inline in `SOTA_USE_CASES.md`
3. **CraftBot's MCP catalog** (`app/config/mcp_config.json`, 197+ servers) — cross-referenced for every SOTA tool
4. **CraftBot's default skills folder** (`<repo>/skills/`, 197+ skills) — audited for matches; relevant defaults referenced in `agent.yaml`
