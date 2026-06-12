# Senior Python Engineer — Source Attribution

This file maps every section of `soul.md` and `role.md` back to the downloaded reference file it was lifted from. It is part of the bundle but is **not** loaded into the agent's context — it exists for human verification and future updates.

Raw originals are in `reference/agents/` and `reference/skills/`. Full source URLs are in `agent.yaml → sources` and `reference/INVENTORY.md`.

---

## soul.md → source map

| Section in soul.md | Source file(s) |
|---|---|
| Opening identity paragraph | `reference/agents/voltagent-python-pro.md` (intro paragraph) |
| "You also act as a senior code reviewer..." | `reference/agents/voltagent-code-reviewer.md` + `reference/agents/voltagent-debugger.md` (intros) |
| Purpose | `reference/agents/wshobson-python-pro.md` (## Purpose) |
| When invoked — dev variant | `reference/agents/voltagent-python-pro.md` (When invoked) |
| When invoked — code review variant | `reference/agents/voltagent-code-reviewer.md` (When invoked) |
| When invoked — debugging variant | `reference/agents/voltagent-debugger.md` (When invoked) |
| Python development checklist | `reference/agents/voltagent-python-pro.md` (Python development checklist) |
| Pythonic patterns and idioms | `reference/agents/voltagent-python-pro.md` (Pythonic patterns and idioms) |
| Type system mastery | `reference/agents/voltagent-python-pro.md` (Type system mastery) + `reference/skills/python-type-safety/SKILL.md` |
| Async and concurrent programming | `reference/agents/voltagent-python-pro.md` + `reference/skills/async-python-patterns/SKILL.md` |
| Sync vs Async decision table | `reference/skills/async-python-patterns/SKILL.md` (decision table) |
| Common async pitfalls | `reference/skills/async-python-patterns/SKILL.md` (Common Pitfalls) |
| Web framework expertise | `reference/agents/voltagent-python-pro.md` (Web framework expertise) |
| Testing methodology | `reference/agents/voltagent-python-pro.md` + `reference/skills/python-testing-patterns/SKILL.md` |
| Test structure (AAA) | `reference/skills/python-testing-patterns/SKILL.md` (Core Concepts) |
| Test naming convention | `reference/skills/python-testing-patterns/SKILL.md` (Test Naming Convention) |
| Test types coverage | `reference/agents/wshobson-test-automator.md` (Capabilities) |
| Package management | `reference/agents/voltagent-python-pro.md` + `reference/skills/python-packaging/SKILL.md` |
| Modern packaging standards | `reference/skills/python-packaging/SKILL.md` |
| Performance optimization | `reference/agents/voltagent-python-pro.md` + `reference/skills/python-performance-optimization/SKILL.md` + `reference/agents/wshobson-performance-engineer.md` |
| Order of typical wins (7 steps) | `reference/skills/python-performance-optimization/SKILL.md` (Primary Optimization Strategies) |
| Security best practices | `reference/agents/voltagent-python-pro.md` + `reference/agents/voltagent-backend-developer.md` (Security implementation standards) |
| Code review priority (9 items) | `reference/agents/voltagent-code-reviewer.md` (Review categories) |
| Code review checklist | `reference/agents/voltagent-code-reviewer.md` (Code review checklist) |
| Constructive feedback approach | `reference/agents/voltagent-code-reviewer.md` (Constructive feedback) |
| Anti-patterns checklist (14 items) | `reference/skills/python-anti-patterns/SKILL.md` (Quick Review Checklist) |
| Debugging checklist | `reference/agents/voltagent-debugger.md` (Debugging checklist) |
| Diagnostic approach (8 steps) | `reference/agents/voltagent-debugger.md` (Diagnostic approach) |
| Debugging techniques | `reference/agents/voltagent-debugger.md` (Debugging techniques) |
| Common bug patterns | `reference/agents/voltagent-debugger.md` (Common bug patterns) |
| Debugging mindset | `reference/agents/voltagent-debugger.md` (Debugging mindset) |
| Error handling rules | `reference/skills/python-error-handling/SKILL.md` (Best Practices Summary) |
| Resource management rules | `reference/skills/python-resource-management/SKILL.md` (Best Practices Summary) |
| Resilience rules | `reference/skills/python-resilience/SKILL.md` (Critical Recommendations) |
| Design principles | `reference/skills/python-design-patterns/SKILL.md` (Best Practices Summary) |
| Layering rule | `reference/skills/python-design-patterns/SKILL.md` (Troubleshooting) |
| Code style rules | `reference/skills/python-code-style/SKILL.md` (Best Practices Summary) |
| Project structure rules | `reference/skills/python-project-structure/SKILL.md` (Best Practices Summary) |
| Behavioral traits | `reference/agents/wshobson-python-pro.md` + `reference/agents/voltagent-python-pro.md` (Behavioral Traits) |
| Response approach (8 steps) | `reference/agents/wshobson-python-pro.md` (Response Approach) |
| Example interactions | `reference/agents/wshobson-python-pro.md` (Example Interactions, 8 of 10) |
| When to push back / defer | Authored from the synthesis (no direct lift) — informed by Behavioral Traits + Constructive Feedback sections |
| On first conversation (PROACTIVE init) | `agent_bundle/PROGRESS.md` design decision #3 |
| Closing rule | `reference/agents/voltagent-python-pro.md` (closing line) |

---

## role.md → source map

| Section in role.md | Source file(s) |
|---|---|
| Antipattern catalog (all 14 BAD/GOOD pairs) | `reference/skills/python-anti-patterns/SKILL.md` |
| Common fixes summary table | `reference/skills/python-anti-patterns/SKILL.md` |
| Code review playbook — review preparation | `reference/agents/voltagent-code-reviewer.md` (Review Preparation) |
| Code review playbook — context evaluation | `reference/agents/voltagent-code-reviewer.md` (Context evaluation) |
| Code review playbook — implementation phase | `reference/agents/voltagent-code-reviewer.md` (Implementation Phase) |
| Code review playbook — review patterns | `reference/agents/voltagent-code-reviewer.md` (Review patterns) |
| Code review playbook — categories | `reference/agents/voltagent-code-reviewer.md` (Review categories) |
| Code review playbook — best practices enforcement | `reference/agents/voltagent-code-reviewer.md` (Best practices enforcement) |
| Code review playbook — constructive feedback shape | `reference/agents/voltagent-code-reviewer.md` (Constructive feedback) |
| Debugging procedure — issue analysis | `reference/agents/voltagent-debugger.md` (Issue Analysis) |
| Debugging procedure — systematic debugging | `reference/agents/voltagent-debugger.md` (Implementation Phase) |
| Debugging procedure — resolution checklist | `reference/agents/voltagent-debugger.md` (Resolution Excellence) |
| Debugging procedure — error analysis | `reference/agents/voltagent-debugger.md` (Error analysis) |
| Debugging procedure — memory debugging | `reference/agents/voltagent-debugger.md` (Memory debugging) |
| Debugging procedure — concurrency | `reference/agents/voltagent-debugger.md` (Concurrency issues) |
| Debugging procedure — production debugging | `reference/agents/voltagent-debugger.md` (Production debugging) |
| Debugging procedure — postmortem | `reference/agents/voltagent-debugger.md` (Postmortem process) |
| Performance investigation — steps 1-3 | `reference/skills/python-performance-optimization/SKILL.md` |
| Performance investigation — observability stack | `reference/agents/wshobson-performance-engineer.md` (Modern Observability & Monitoring) |
| Performance investigation — load testing | `reference/agents/wshobson-performance-engineer.md` (Modern Load Testing) |
| Performance investigation — caching architecture | `reference/agents/wshobson-performance-engineer.md` (Multi-Tier Caching) |
| Performance investigation — verify | `reference/skills/python-performance-optimization/SKILL.md` |
| Refactoring — class growing | `reference/skills/python-design-patterns/SKILL.md` (Troubleshooting) |
| Refactoring — 7+ constructor params | `reference/skills/python-design-patterns/SKILL.md` (Troubleshooting) |
| Refactoring — deep composition | `reference/skills/python-design-patterns/SKILL.md` (Troubleshooting) |
| Refactoring — duplication diverging | `reference/skills/python-design-patterns/SKILL.md` (Troubleshooting) |
| Refactoring — service-layer importing from API | `reference/skills/python-design-patterns/SKILL.md` (Troubleshooting) |
| Refactoring — rename rollout | Authored from the synthesis (not in any single reference) |
| Refactoring — sync→async | `reference/skills/async-python-patterns/SKILL.md` informs; procedure authored from the synthesis |
| Testing reference patterns — retry behavior | `reference/skills/python-testing-patterns/SKILL.md` (Testing Retry Behavior) |
| Testing reference patterns — freezegun | `reference/skills/python-testing-patterns/SKILL.md` (Mocking Time with Freezegun) |
| Testing reference patterns — markers | `reference/skills/python-testing-patterns/SKILL.md` (Test Markers) |
| Testing reference patterns — coverage | `reference/skills/python-testing-patterns/SKILL.md` (Coverage Reporting) |
| Async patterns deep reference — all subsections | `reference/skills/async-python-patterns/SKILL.md` (Pattern 1-5 + Common Pitfalls) |
| Pydantic validation patterns | `reference/skills/python-error-handling/SKILL.md` (Pattern 3: Pydantic for Complex Validation) |
| Resource management deep examples — all | `reference/skills/python-resource-management/SKILL.md` (Patterns 1-3) |
| Type system deep examples — Result class | `reference/skills/python-type-safety/SKILL.md` (Pattern 4: Generic Classes) |
| Type system deep examples — type narrowing | `reference/skills/python-type-safety/SKILL.md` (Pattern 3: Type Narrowing with Guards) |

---

## Notes on "authored from synthesis"

A handful of small sections in soul.md and role.md were composed locally rather than lifted verbatim. They are listed above with "Authored from the synthesis." Each is short and operational (push-back rules, rename rollout procedure, sync→async procedure summary). They are not domain claims, they're operational glue between lifted sections.

The PROACTIVE.md self-init footer is a CraftBot-specific design decision documented in `agent_bundle/PROGRESS.md` and is the same across all v0 agents.

---

## How to update this agent

If you want to refresh content from upstream:

1. Re-fetch the source files listed in `reference/INVENTORY.md` and overwrite `reference/agents/*.md` / `reference/skills/*/SKILL.md` in place.
2. Diff against the previous versions to see what changed.
3. Update the corresponding sections of `soul.md` and `role.md` to match.
4. Update this `SOURCES.md` if section names or source URLs changed.
5. Re-run `build.py` to regenerate `dist/senior-python-engineer.craftbot`.

Because the reference files are stored verbatim with source URLs, this update path is mechanical and traceable.

---

## SOTA tool sources (June 2026)

Per-tool source table for the 2026 SOTA stack. Every tool listed here ships
with a dedicated SKILL.md under `skills/` and is referenced from role.md
under `## SOTA tool reference (June 2026)`.

### Universal execution verb

| Tool | Source | Skill pack |
|---|---|---|
| `uv` | https://docs.astral.sh/uv/ · https://github.com/astral-sh/uv | `uv-uvx-modern-toolchain` |
| `uvx` | https://docs.astral.sh/uv/guides/tools/ | `uv-uvx-modern-toolchain` |

### Lint + format

| Tool | Source | Skill pack |
|---|---|---|
| `ruff` | https://docs.astral.sh/ruff/ · https://github.com/astral-sh/ruff | `ruff-lint-format-all-in-one` |
| `ruff-pre-commit` | https://github.com/astral-sh/ruff-pre-commit | `ruff-lint-format-all-in-one`, `pre-commit-hook-pipeline` |

### Type checking

| Tool | Source | Skill pack |
|---|---|---|
| `mypy` | https://mypy.readthedocs.io/ | role.md SOTA section |
| `pyright` | https://github.com/microsoft/pyright | role.md SOTA section |
| `pyrefly` (Meta, v1.0 May 2026) | https://github.com/facebook/pyrefly · https://github.com/facebook/pyrefly/releases/tag/1.0.0 | `pyrefly-meta-type-checker` |
| `ty` (Astral, beta) | https://docs.astral.sh/ty/ | role.md SOTA section |

### Testing

| Tool | Source | Skill pack |
|---|---|---|
| `pytest` 9.x + `pytest-xdist` + `pytest-asyncio` | https://docs.pytest.org/ | uses existing `python-testing-patterns` |
| `slipcover` | https://github.com/plasma-umass/slipcover | role.md SOTA section |
| `hypothesis` | https://hypothesis.readthedocs.io/ | `hypothesis-property-based` |
| `mutmut` | https://github.com/boxed/mutmut · https://johal.in/mutation-testing-with-mutmut-python-for-code-reliability-2026/ | `mutmut-mutation-testing` |
| `syrupy` | https://github.com/syrupy-project/syrupy | role.md SOTA section |
| `respx` | https://lundberg.github.io/respx/ | role.md SOTA section |
| `vcrpy` | https://vcrpy.readthedocs.io/ | role.md SOTA section |
| `pytest-httpx` | https://pypi.org/project/pytest-httpx/ | role.md SOTA section |
| `testcontainers` | https://github.com/testcontainers/testcontainers-python | `testcontainers-integration-testing` |
| `pyfakefs` | https://github.com/pytest-dev/pyfakefs | `testcontainers-integration-testing` |

### Profilers

| Tool | Source | Skill pack |
|---|---|---|
| `py-spy` | https://github.com/benfred/py-spy | `py-spy-cpu-profiling` |
| `memray` (Bloomberg) | https://github.com/bloomberg/memray · https://bloomberg.github.io/memray/ | `memray-memory-profiling` |
| `pytest-memray` | https://github.com/bloomberg/pytest-memray | `memray-memory-profiling` |
| `scalene` (Plasma/UMass) | https://github.com/plasma-umass/scalene | `scalene-ai-optimization` |
| `viztracer` | https://github.com/gaogaotiantian/viztracer | `viztracer-asyncio-timeline` |
| Perfetto UI | https://ui.perfetto.dev/ | `viztracer-asyncio-timeline` |
| Speedscope | https://www.speedscope.app/ · https://github.com/jlfwong/speedscope | `py-spy-cpu-profiling` |
| `pyinstrument` | https://github.com/joerick/pyinstrument | role.md SOTA section |
| `austin` | https://github.com/P403n1x87/austin | role.md SOTA section |
| Sentry Profiling | https://docs.sentry.io/product/profiling/ | role.md SOTA section |
| Pyroscope | https://pyroscope.io/ | role.md SOTA section |
| Datadog Continuous Profiler | https://docs.datadoghq.com/profiler/ | role.md SOTA section |

### Debugging

| Tool | Source | Skill pack |
|---|---|---|
| `loguru` | https://github.com/Delgan/loguru | role.md SOTA section |
| `icecream` | https://github.com/gruns/icecream | role.md SOTA section |
| `snoop` / `pysnooper` | https://github.com/alexmojaki/snoop · https://github.com/cool-RR/PySnooper | role.md SOTA section |
| `pudb` | https://github.com/inducer/pudb | role.md SOTA section |
| `pdb++` | https://github.com/pdbpp/pdbpp | role.md SOTA section |
| `web-pdb` | https://github.com/romanvm/python-web-pdb | role.md SOTA section |
| `debugpy` | https://github.com/microsoft/debugpy | role.md SOTA section |

### Refactoring / codemods

| Tool | Source | Skill pack |
|---|---|---|
| `libcst` (Meta/Instagram) | https://github.com/Instagram/LibCST · https://libcst.readthedocs.io/ | `libcst-codemods` |
| `rope` | https://github.com/python-rope/rope | role.md SOTA section |
| `ruff --select=UP --fix` | https://docs.astral.sh/ruff/rules/#pyupgrade-up | `ruff-lint-format-all-in-one` |

### Security / quality

| Tool | Source | Skill pack |
|---|---|---|
| `bandit` | https://bandit.readthedocs.io/ | `semgrep-bandit-security-audit` |
| `semgrep` | https://semgrep.dev/ · https://semgrep.dev/p/bandit | `semgrep-bandit-security-audit` |
| `pip-audit` (PyPA) | https://pypi.org/project/pip-audit/ | `semgrep-bandit-security-audit` |
| `osv-scanner` (Google) | https://google.github.io/osv-scanner/ | `semgrep-bandit-security-audit` |
| `gitleaks` | https://github.com/gitleaks/gitleaks | `semgrep-bandit-security-audit`, `pre-commit-hook-pipeline` |
| `trufflehog` | https://github.com/trufflesecurity/trufflehog | `semgrep-bandit-security-audit` |
| `vulture` | https://github.com/jendrikseipp/vulture | role.md SOTA section |
| CodeQL | https://codeql.github.com/ | `semgrep-bandit-security-audit` (alt comparison) |

### Code review automation

| Tool | Source | Skill pack |
|---|---|---|
| CodeRabbit | https://www.coderabbit.ai/ | USE_CASES.md |
| Greptile | https://www.greptile.com/ | USE_CASES.md |
| Qodo Merge 2.0 | https://www.qodo.ai/products/qodo-merge/ | USE_CASES.md |

### Web frameworks (2026 SOTA)

| Tool | Source | Skill pack |
|---|---|---|
| FastAPI 0.115+ | https://fastapi.tiangolo.com/ | `fastapi-litestar-modern-web` |
| Litestar | https://litestar.dev/ | `fastapi-litestar-modern-web` |
| Robyn | https://robyn.tech/ | `fastapi-litestar-modern-web` |
| Django Ninja | https://django-ninja.dev/ | `fastapi-litestar-modern-web` |
| Pydantic v2 | https://docs.pydantic.dev/latest/ | `fastapi-litestar-modern-web` |
| msgspec | https://github.com/jcrist/msgspec | `fastapi-litestar-modern-web` |
| pydantic-settings | https://docs.pydantic.dev/latest/concepts/pydantic_settings/ | `fastapi-litestar-modern-web` |

### Database / ORM

| Tool | Source | Skill pack |
|---|---|---|
| SQLAlchemy 2.x async | https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html | `sqlalchemy-2x-async-postgres` |
| asyncpg | https://magicstack.github.io/asyncpg/ | `sqlalchemy-2x-async-postgres` |
| Alembic | https://alembic.sqlalchemy.org/ | `sqlalchemy-2x-async-postgres` |
| SQLModel | https://sqlmodel.tiangolo.com/ | `sqlalchemy-2x-async-postgres` |

### CLI

| Tool | Source | Skill pack |
|---|---|---|
| Typer | https://typer.tiangolo.com/ | role.md SOTA section |
| Cyclopts | https://cyclopts.readthedocs.io/ | role.md SOTA section |
| Click | https://click.palletsprojects.com/ | role.md SOTA section |
| rich-click | https://github.com/ewels/rich-click | role.md SOTA section |

### Async

| Tool | Source | Skill pack |
|---|---|---|
| `uvloop` | https://uvloop.readthedocs.io/ | `fastapi-litestar-modern-web`, role.md SOTA section |
| `anyio` | https://anyio.readthedocs.io/ | role.md SOTA section |
| `trio` | https://trio.readthedocs.io/ | role.md SOTA section |
| `aiomultiprocess` | https://github.com/omnilib/aiomultiprocess | role.md SOTA section |

### Performance optimization

| Tool | Source | Skill pack |
|---|---|---|
| JAX | https://jax.readthedocs.io/ | role.md SOTA section |
| Numba | https://numba.readthedocs.io/ | role.md SOTA section |
| Cython | https://cython.org/ | role.md SOTA section |
| mypyc | https://mypyc.readthedocs.io/ | role.md SOTA section |
| Mojo (Modular) | https://www.modular.com/mojo | role.md SOTA section |
| Ray | https://www.ray.io/ | role.md SOTA section |
| dask | https://www.dask.org/ | role.md SOTA section |
| joblib | https://joblib.readthedocs.io/ | role.md SOTA section |
| cachetools | https://cachetools.readthedocs.io/ | role.md SOTA section |
| aiocache | https://aiocache.readthedocs.io/ | role.md SOTA section |
| redis-py | https://redis.readthedocs.io/ | role.md SOTA section |

### Packaging

| Tool | Source | Skill pack |
|---|---|---|
| `hatchling` | https://hatch.pypa.io/ | uses existing `python-packaging` |
| `flit` | https://flit.pypa.io/ | uses existing `python-packaging` |
| PEPs 517/518/621/660 | https://peps.python.org/ | uses existing `python-packaging` |
| PEP 723 inline scripts | https://peps.python.org/pep-0723/ | `uv-uvx-modern-toolchain` |
| PEP 735 dependency groups | https://peps.python.org/pep-0735/ | `uv-uvx-modern-toolchain` |

### Git workflow

| Tool | Source | Skill pack |
|---|---|---|
| `commitizen` | https://commitizen-tools.github.io/commitizen/ | `commitizen-semver-automation` |
| Conventional Commits 1.0 | https://www.conventionalcommits.org/en/v1.0.0/ | `commitizen-semver-automation` |
| Semantic Versioning 2.0 | https://semver.org/ | `commitizen-semver-automation` |
| Keep a Changelog | https://keepachangelog.com/ | `commitizen-semver-automation` |
| `pre-commit` | https://pre-commit.com/ | `pre-commit-hook-pipeline` |
| `gh` CLI | https://cli.github.com/ | uses default `github` skill |

### ADRs

| Tool | Source | Skill pack |
|---|---|---|
| MADR 4.0 | https://adr.github.io/madr/ | `log4brains-adr-management` |
| log4brains | https://github.com/thomvaill/log4brains | `log4brains-adr-management` |
| adr-tools (npryce) | https://github.com/npryce/adr-tools | `log4brains-adr-management` |
| adr-kit (kschlt) | https://github.com/kschlt/adr-kit | `log4brains-adr-management` |
| ADR community | https://adr.github.io/ | `log4brains-adr-management` |

### Observability

| Tool | Source | Skill pack |
|---|---|---|
| OpenTelemetry Python | https://opentelemetry.io/docs/languages/python/ | `opentelemetry-observability` |
| OTel contrib (auto-instrument) | https://github.com/open-telemetry/opentelemetry-python-contrib | `opentelemetry-observability` |
| Sentry Python | https://docs.sentry.io/platforms/python/ | `opentelemetry-observability` |
| Honeycomb | https://docs.honeycomb.io/getting-data-in/opentelemetry/python/ | `opentelemetry-observability` |
| Datadog APM | https://docs.datadoghq.com/tracing/setup_overview/open_standards/python/ | `opentelemetry-observability` |

### Skill pack inventory (NEW June 2026)

| Skill pack | Tools covered |
|---|---|
| `uv-uvx-modern-toolchain` | uv, uvx |
| `ruff-lint-format-all-in-one` | ruff (lint + format) |
| `pyrefly-meta-type-checker` | pyrefly v1.0 |
| `py-spy-cpu-profiling` | py-spy |
| `memray-memory-profiling` | memray, pytest-memray |
| `scalene-ai-optimization` | scalene |
| `viztracer-asyncio-timeline` | viztracer, Perfetto |
| `libcst-codemods` | libcst |
| `mutmut-mutation-testing` | mutmut |
| `testcontainers-integration-testing` | testcontainers, pyfakefs |
| `hypothesis-property-based` | hypothesis |
| `commitizen-semver-automation` | commitizen |
| `pre-commit-hook-pipeline` | pre-commit + ruff/pyrefly/bandit/gitleaks/commitizen hooks |
| `semgrep-bandit-security-audit` | semgrep, bandit, pip-audit, gitleaks, osv-scanner |
| `fastapi-litestar-modern-web` | FastAPI, Litestar, Robyn, Django Ninja, Pydantic v2, msgspec, uvloop |
| `sqlalchemy-2x-async-postgres` | SQLAlchemy 2.x async, asyncpg, Alembic, SQLModel |
| `log4brains-adr-management` | MADR 4.0, log4brains, adr-tools, adr-kit |
| `opentelemetry-observability` | OpenTelemetry Python, Sentry, Honeycomb, Datadog APM |
