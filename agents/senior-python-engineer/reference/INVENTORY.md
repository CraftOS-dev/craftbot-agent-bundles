# Senior Python Engineer — Reference Inventory

This folder holds the **raw downloaded SOTA material** used to compose the agent.
Every file here came from an external source — nothing was authored locally.

**Composition rule:** when authoring `agent.yaml`, `soul.md`, and `role.md`, every section must be traceable back to one or more files in this folder.

---

## Reference Agents (8 files)

Each is a full agent definition from a high-quality open-source agent repo, treated as source material for our agent's persona + workflows.

| File | Source repo | Source URL | Description | Status |
|---|---|---|---|---|
| `agents/wshobson-python-pro.md` | wshobson/agents | [link](https://github.com/wshobson/agents/blob/main/plugins/python-development/agents/python-pro.md) | Master Python 3.12+ with modern tooling (uv, ruff, pydantic, FastAPI). Heavy capability map across 9 sub-domains. | full |
| `agents/wshobson-backend-architect.md` | wshobson/agents | [link](https://github.com/wshobson/agents/blob/main/plugins/backend-development/agents/backend-architect.md) | Scalable API design, microservices, distributed systems, resilience patterns. | full |
| `agents/wshobson-test-automator.md` | wshobson/agents | [link](https://github.com/wshobson/agents/blob/main/plugins/backend-development/agents/test-automator.md) | Build comprehensive test suites (unit, integration, E2E) during feature work. | full |
| `agents/wshobson-performance-engineer.md` | wshobson/agents | [link](https://github.com/wshobson/agents/blob/main/plugins/application-performance/agents/performance-engineer.md) | Modern observability, OpenTelemetry, profiling, load testing, caching. | full |
| `agents/voltagent-python-pro.md` | VoltAgent/awesome-claude-code-subagents | [link](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/02-language-specialists/python-pro.md) | Senior Python developer focus: type-safe code, async patterns, Pythonic idioms, workflow protocols. | full |
| `agents/voltagent-code-reviewer.md` | VoltAgent/awesome-claude-code-subagents | [link](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/04-quality-security/code-reviewer.md) | Comprehensive code review focusing on quality, security, performance, and best practices. | full |
| `agents/voltagent-debugger.md` | VoltAgent/awesome-claude-code-subagents | [link](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/04-quality-security/debugger.md) | Systematic debugging: hypothesis, evidence, root cause isolation, prevention. | full |
| `agents/voltagent-backend-developer.md` | VoltAgent/awesome-claude-code-subagents | [link](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/01-core-development/backend-developer.md) | Server-side APIs and microservices with auth, performance, observability. | full |

## Reference Skills (12 files)

Real `SKILL.md` files from wshobson/agents' `plugins/python-development/skills/` directory. These are SOTA skill packs we will **copy into the agent bundle** under `agents/senior-python-engineer/skills/` for distribution with the `.craftbot`.

| File | Source URL | Description | Status |
|---|---|---|---|
| `skills/python-code-style/SKILL.md` | [link](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-code-style) | Modern Python tooling: ruff, mypy, pyright config; PEP 8 naming; Google-style docstrings; 120-char lines. | full |
| `skills/python-anti-patterns/SKILL.md` | [link](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-anti-patterns) | Checklist of common mistakes with BAD/GOOD code pairs across infra, architecture, error handling, resources, types, tests. | full |
| `skills/python-error-handling/SKILL.md` | [link](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-error-handling) | Fail-fast validation, meaningful exception hierarchies, partial-failure handling, Pydantic, exception mapping table. | full |
| `skills/python-testing-patterns/SKILL.md` | [link](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-testing-patterns) | pytest patterns: AAA structure, naming conventions, retry testing, freezegun for time, markers, coverage. | full |
| `skills/python-type-safety/SKILL.md` | [link](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-type-safety) | Type hints, modern union syntax, type narrowing, generics, protocols, mypy strict. | full |
| `skills/python-design-patterns/SKILL.md` | [link](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-design-patterns) | KISS, SRP, composition over inheritance, Rule of Three, layering rules, troubleshooting guide. | full |
| `skills/python-resource-management/SKILL.md` | [link](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-resource-management) | Context managers (sync/async), `@contextmanager`, unconditional cleanup, ExitStack, streaming. | full |
| `skills/async-python-patterns/SKILL.md` | [link](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/async-python-patterns) | asyncio fundamentals, gather, tasks, error handling, timeouts, cancellation, common pitfalls. | full |
| `skills/python-project-structure/SKILL.md` | [link](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-project-structure) | `src/` layout, `__all__` discipline, flat hierarchies, test colocation strategies, layered vs domain-driven structures. | full |
| `skills/python-packaging/SKILL.md` | [link](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-packaging) | Modern packaging: PEPs 517/518/621/660; build backends; src/ layout; single `pyproject.toml`. | **summary** (WebFetch refused verbatim) |
| `skills/python-resilience/SKILL.md` | [link](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-resilience) | Transient vs permanent failures, exponential backoff + jitter, `tenacity`, timeouts as mandatory. | **summary** (WebFetch refused verbatim) |
| `skills/python-performance-optimization/SKILL.md` | [link](https://github.com/wshobson/agents/tree/main/plugins/python-development/skills/python-performance-optimization) | Profile-first methodology; cProfile/py-spy/memory_profiler; algorithm → built-ins → cache → numpy → C. | **summary** (WebFetch refused verbatim) |

## Sources Considered But Not Downloaded

| Source | Why excluded |
|---|---|
| `anthropics/skills` (official Anthropic skill library) | Inventory checked — contains only design/document/content skills (algorithmic-art, brand-guidelines, canvas-design, docx, pdf, pptx, frontend-design, etc.). **No code-engineering skills exist there yet.** |
| `anthropics/claude-cookbooks` | Notebook-style recipes for SDK usage, not packaged SKILL.md files. Not in the right format to bundle. |
| `JSONbored/claudepro-directory` | Web directory; skill files not exposed in a directly-downloadable tree at expected path. |
| `vijaythecoder/awesome-claude-agents` | Lists 24 agents but at framework-specialist tier (Laravel/Rails/Vue) — overlap with material already harvested from wshobson + VoltAgent. |
| `msitarzewski/agency-agents` | 232 agents, but skews toward agency / non-engineering roles (marketing, design). Not the highest-value source for senior Python engineer. |
| `wshobson/agents` — remaining python-development skills (background-jobs, configuration, observability, project-setup, uv-package-manager) + `commands/python-scaffold.md` | Available but lower marginal value for the agent's persona/decision-making. Can be added later if you want broader operational coverage. |
| `wshobson/agents` — `backend-development/skills/` (api-design-principles, architecture-patterns, cqrs-implementation, microservices-patterns, saga-orchestration, etc.) | Architectural; would belong to a `backend-architect` agent (future v1) rather than the Python engineer specifically. |

---

## Status check

- ✅ 8 agent reference files saved verbatim
- ✅ 9 skill files saved verbatim
- ⚠️ 3 skill files saved as **WebFetch summaries** rather than verbatim source. Each is clearly marked at the top of its SKILL.md with a NOTE block. Substance preserved; code examples reduced.
- ✅ All sources cited with URL + repo

## What gets used at composition time

When I write `agent.yaml` / `soul.md` / `role.md`, the rule is: **every bullet, every section, every claim must point back to a specific file in this folder.** No invented content. No generic philosophy. The skill folder under `skills/` (the 12 listed above) gets copied into `agents/senior-python-engineer/skills/` for inclusion in the `.craftbot` bundle.

## Waiting for approval

Stop here per the agreed workflow. Tell me:
1. Is this set of references sufficient, or should I dig for more?
2. Are there sources I should drop?
3. Are the 3 "summary" skills (packaging, resilience, performance-optimization) acceptable as-is, or do you want me to try a different fetch strategy to get them verbatim?

Only after your go-ahead do I move to composition.
