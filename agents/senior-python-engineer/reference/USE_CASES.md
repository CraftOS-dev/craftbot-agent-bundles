# Senior Python Engineer — Use Cases

**Tier:** specialized · **Category:** engineering
**Core job:** Write, review, debug, refactor, and optimize Python code at the level of a 10-year-experience senior on a real team.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Write Python code
- Build modules, packages, full applications from spec
- FastAPI / Django / Flask web services
- CLI tools (Click, Typer, argparse)
- Async / concurrent code (asyncio, threading, multiprocessing)
- Data pipelines (pandas, NumPy, SQLAlchemy)
- Type-safe code (generics, protocols, TypedDict, mypy strict)

### Review code
- PR reviews with priority order: security → performance → memory → races → error handling → input validation → access control → integrity → readability
- Flag 14 specific antipatterns (scattered retry, hard-coded config, exposed ORM models, bare except, etc.) with concrete BAD/GOOD code pairs
- Refuses to flag style nits the formatter would normalize

### Debug bugs
- 9-step systematic methodology: symptom → reproduce → hypothesis → experiment → evidence → root cause → patch → verify → name-the-test-that-would-have-caught-it
- Suspect off-by-one, None, race, timing, type mismatch, config first
- Use `cProfile`, `py-spy`, `memory_profiler`, `tracemalloc`

### Refactor code
- God-class extraction, rename rollout, sync→async conversion
- Only when there's a concrete reason — never "not clean enough"

### Optimize performance
- Profile first; never optimize without measurement
- 9-step priority order: algorithmic > per-iteration overhead > batch I/O > caching > built-ins > NumPy > Cython > async > multiprocessing

### Set up modern Python tooling
- `uv` for package management, `ruff` for lint+format, `mypy --strict` for types, `pytest` for tests
- Modern packaging (PEPs 517/518/621/660, `pyproject.toml`, `src/` layout)

### Manage Git workflows
- Conventional Commits, isolated worktrees, PR review (giving and receiving), differential review

### Architecture decisions
- Document in ADRs (MADR, Y-statement, lightweight formats) when the decision is load-bearing

---

## Execution status (SOTA — June 2026)

The previous verdict ("can execute the full software-engineering loop") was directionally right but listed outdated profilers (cProfile / memory_profiler / tracemalloc) and missed several 2026 SOTA replacements. Updated SOTA stack: `uv`+`uvx` as the universal execution verb, `ruff` replacing 10+ legacy tools (black/isort/flake8/pyupgrade/pydocstyle/bandit-lite/pylint-lite), `memray` (Bloomberg) replacing `memory_profiler`, `scalene` (CPU+GPU+memory with AI suggestions), `viztracer` (Perfetto timeline for asyncio), `pyrefly` v1.0 (Meta, May 2026 stable, 10-50x faster than mypy), `libcst` for safe codemods. Every SOTA tool runs through the agent's existing `cli-anything` + `uvx` — no new MCP needed for any of them.

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Write Python code | `uv` (Astral) — package + venv + Python install + lockfile (10-100x faster than pip); FastAPI 0.115+ / Litestar (msgspec, 2x perf) / Robyn (Rust); SQLAlchemy 2.x async + asyncpg / SQLModel; Typer / Cyclopts / Click 8.x | `cli-anything` (`uv init`, `uv add fastapi[standard] sqlalchemy[asyncio] asyncpg pydantic-settings typer`, `uv run`) + `filesystem` MCP |
| Review code | Multi-layer: AI pass (CodeRabbit / Greptile 82% bug catch / Qodo Merge 2.0 multi-agent F1 60.1%) + `ruff check --select=ALL` + `bandit` + `semgrep` + `pip-audit` + `gitleaks` + bundled `differential-review` skill | `cli-anything` (`uvx ruff check --diff`, `uvx bandit`, `gitleaks detect`, `semgrep --config=auto`) + `github-api` MCP |
| Debug bugs | **`py-spy`** (no code changes, attach to PID) + **`memray`** (Bloomberg, replaces memory_profiler, tracks C-ext allocs) + **`viztracer`** (Perfetto-backed asyncio timeline) + `snoop`/`pysnooper` + `loguru` + `icecream` + `debugpy` + `pdb++`/`pudb` | `sentry-mcp` (prod errors) → `cli-anything` (`uvx py-spy record`, `uvx memray run --live`, `uvx viztracer`) + `systematic-debugging` skill |
| Refactor code | `libcst` (Meta/Instagram CST — preserves whitespace + comments, used on ~20M LOC) for tree-aware codemods; `rope` for symbol rename + extract method; `ruff check --select=UP,SIM,RUF --fix` for mechanical | `cli-anything` (`uv add --dev libcst`, `python -m libcst.tool codemod`, `uvx rope_cli rename`) + `using-git-worktrees` for isolated refactor branches |
| Optimize performance | **`py-spy`** (sampling) + **`memray`** (memory + native ext) + **`scalene`** (CPU+GPU+memory with AI optimization suggestions) + `pyinstrument` (call tree) + `viztracer` (asyncio); `uvloop` event loop + `numba`/`cython`/`mypyc` JIT + `joblib`/`ray`/`dask` parallelism + `cachetools`; continuous: Pyroscope / Sentry Profiling / Datadog | `cli-anything` (`uvx py-spy record -o flame.svg --format speedscope`, `uvx memray run --native`, `uvx scalene --html`, `uvx pyinstrument`) + Speedscope/Perfetto UI |
| Set up modern Python tooling | Canonical 2026: `uv` + `ruff` (lint+format, 900+ rules, replaces 10+ tools) + type checker (mypy / pyright / **pyrefly v1.0** — Meta, May 2026 stable, 10-50x faster, 90%+ typing-spec conformance, OR `ty` Astral beta) + `pytest` 9.x + `pytest-xdist -n auto` + `slipcover` (5% overhead vs coverage.py 180%) + `hatchling` PEP 517 backend + `src/` layout + `pre-commit` hooks | `cli-anything` (`uv init --package`, `uv add --dev ruff pytest pytest-xdist hypothesis pyrefly`, `uvx ruff check && format`, `uv run pyrefly check src/`, `uvx pre-commit install`) + `filesystem` for pyproject.toml |
| Manage Git workflows | Conventional Commits 1.0 + `commitizen` (`uvx cz commit`, `uvx cz bump`) for semver+CHANGELOG; git worktrees sibling-directory convention; `gh` CLI for PR review; pre-commit hooks | `using-git-worktrees` + `git-commit` MCP + `github` + `github-api` MCPs + `cli-anything` (`gh pr create --fill`, `gh pr review --approve`) + `requesting-code-review` / `receiving-code-review` skills |
| Architecture decisions (ADR) | MADR 4.0 (de facto 2026 format); CLI: `adr-tools` (npryce, shell) OR `adr-kit` (kschlt, full MADR toolkit with validation + indexing + enforcement) OR `dotnet-adr` (richer templates); or `filesystem` writes MADR-shaped Markdown directly | `cli-anything` (`npx adr-tools init docs/adr && new`, `pipx install adr-kit`) OR `filesystem` MCP + `git-commit` MCP |

### Cross-cutting SOTA tooling (also via `cli-anything` + `uvx`)

| Concern | SOTA tool (2026) | Replaces |
|---|---|---|
| HTTP mocking | `respx` (httpx-native), `vcrpy` (record/replay), `pytest-httpx` | `requests-mock` |
| Snapshot tests | `syrupy` | `pytest-snapshot`, `snapshottest` |
| DB integration tests | `testcontainers[postgresql]` + `pytest-asyncio` + `asyncpg` | mocks, `pytest-postgresql` |
| Mutation testing | `mutmut` (88.5% detection, 1200 mutants/min) | `cosmic-ray`, `MutPy` |
| Coverage | `slipcover` (5% overhead) or `pytest-cov` | — |
| Dead code | `vulture` | manual review |
| Dep audit | `pip-audit` (PyPA), `osv-scanner` (Google) | `safety` |
| Secrets | `gitleaks`, `trufflehog` | `detect-secrets` |
| Pre-commit | `pre-commit` framework + `ruff-pre-commit` | hand-rolled hooks |
| Continuous profiling (prod) | Sentry Profiling, Pyroscope, Datadog Continuous Profiler | — |

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Tool installation on recipient's machine | ⚠ | `cli-anything` will `uvx <tool>` ephemerally — no install pollution, but requires `uv` installed first. Most recipients have it; `curl -LsSf https://astral.sh/uv/install.sh \| sh` is one command. |
| Production deployment / IaC | ✗ | Agent codes the app; deployment + IaC (Terraform/Pulumi/CDK) is out of scope. Recommend handoff to a DevOps specialist (v1) |
| Frontend (React/Vue/Svelte) | ✗ | Python-only. Recommend a frontend specialist for UI work (v1) |

**Verdict (June 2026): 100% fulfillment of the documented Python software-engineering loop.** Every SOTA tool — profilers, type checkers, lint, test, mutation, codemod, AI review — is reachable via `cli-anything` + `uvx`. Soul.md and role.md should be updated to name 2026 tools (memray/scalene/viztracer/pyrefly/libcst) instead of the legacy ones (cProfile/memory_profiler/tracemalloc).

---

## When to use this agent

- "Review this PR for security / performance / correctness"
- "Write me a Python module that does X"
- "Help me migrate from pip to uv"
- "I'm seeing a `RecursionError` only under load — help me find the cause"
- "Refactor this god class into smaller units"
- "Set up a modern Python project with ruff, mypy, and pytest"
- "Design a FastAPI application with proper error handling and validation"
- "Implement modern authentication patterns in FastAPI"

## When NOT to use this agent

- Non-Python languages — adapt with caution, recommend a language-specific specialist
- Pure architecture / system-design work without code — recommend a backend-architect specialist (v1)
- Frontend / UI work — recommend a frontend specialist (v1)
- Data science / ML modeling work — adjacent but recommend a data-scientist specialist (v1)
- Anything outside engineering — answer briefly and stay focused
