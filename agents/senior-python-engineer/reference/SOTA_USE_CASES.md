<!--
SOTA per-use-case mapping for senior-python-engineer (June 2026).

This file translates the documented use cases (see USE_CASES.md) into the exact
2026 SOTA tool + the concrete `uvx`/`uv run` command the agent should reach for.
Every tool listed here is reachable through the agent's existing `cli-anything`
skill — no MCP needed for any of them.

Confidence legend:
  ✓ — agent can fully execute this today via documented tools
  ⚠ — agent can execute but depends on environment (uv installed, network)
  ✗ — out of scope or requires a different specialist
-->

# Senior Python Engineer — SOTA use cases (June 2026)

This file maps each documented use case to its current SOTA tool and the exact
execution path. Read alongside `USE_CASES.md` (capabilities) and `role.md`
(deep tool reference). Skill packs implementing each tool live under
`agents/senior-python-engineer/skills/`.

---

## Write Python code
- **SOTA approach:** `uv` for project/venv/Python/lockfile management (10-100x
  faster than pip/poetry); FastAPI 0.115+ (default) / Litestar (msgspec, ~2x
  perf) / Robyn (Rust, perf-critical) for web; SQLAlchemy 2.x async + asyncpg
  for Postgres; SQLModel as Pydantic glue; Typer / Cyclopts / Click 8.x for
  CLIs; `hatchling` PEP 517 backend; `src/` layout mandatory.
- **Agent execution path:**
  ```
  uv init --package my-service
  uv add fastapi[standard] sqlalchemy[asyncio] asyncpg pydantic-settings typer uvloop
  uv add --dev ruff pytest pytest-xdist hypothesis pyrefly
  uv run python -m my_service
  ```
- **Source:** https://docs.astral.sh/uv/ · https://fastapi.tiangolo.com/ ·
  https://litestar.dev/ · https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- **Skill packs:** `uv-uvx-modern-toolchain`, `fastapi-litestar-modern-web`,
  `sqlalchemy-2x-async-postgres`
- **Confidence:** ✓

## Review code
- **SOTA approach:** Multi-layer review combining AI bots (CodeRabbit /
  Greptile — 82% bug catch / Qodo Merge 2.0 — multi-agent, F1 60.1%, free
  self-hosted) + `ruff check --select=ALL` (900+ rules) + `bandit` (security)
  + `semgrep --config=auto` (semantic patterns) + `pip-audit` (PyPA dep audit)
  + `gitleaks` (secrets) + bundled `differential-review` skill.
- **Agent execution path:**
  ```
  uvx ruff check --select=ALL --diff .
  uvx bandit -r src/
  uvx semgrep --config=auto --json --output=semgrep.json
  uvx pip-audit
  gitleaks detect --source=. --no-banner
  gh pr review <num> --request-changes --body "$(cat review.md)"
  ```
- **Source:** https://github.com/astral-sh/ruff · https://semgrep.dev/p/bandit
  · https://pypi.org/project/pip-audit/ · https://github.com/gitleaks/gitleaks
  · https://www.qodo.ai/products/qodo-merge/
- **Skill packs:** `ruff-lint-format-all-in-one`,
  `semgrep-bandit-security-audit`, `pre-commit-hook-pipeline`
- **Confidence:** ✓

## Debug bugs
- **SOTA approach:** `py-spy` (sampling, no code changes, attach to PID) for
  CPU/stack inspection; `memray` (Bloomberg, replaces `memory_profiler`,
  tracks NATIVE C-extension allocs via LD_PRELOAD) for memory; `viztracer`
  (Perfetto-backed timeline) for asyncio contention; `snoop`/`pysnooper` for
  variable trace; `loguru` for structured logging; `icecream` (`ic()`) for
  quick print debug; `pudb` (TUI) / `pdb++` / `web-pdb` / `debugpy` for
  interactive.
- **Agent execution path:**
  ```
  uvx py-spy record -o flame.svg --format speedscope -- python script.py
  uvx py-spy dump --pid <PID>         # attach to running process
  uvx memray run --native --live python script.py
  uvx memray flamegraph memray-script.py.bin
  uvx viztracer python script.py      # open result.json in Perfetto UI
  uv add --dev loguru icecream snoop
  ```
- **Source:** https://github.com/benfred/py-spy ·
  https://github.com/bloomberg/memray ·
  https://github.com/gaogaotiantian/viztracer ·
  https://github.com/Delgan/loguru · https://github.com/gruns/icecream
- **Skill packs:** `py-spy-cpu-profiling`, `memray-memory-profiling`,
  `viztracer-asyncio-timeline`
- **Confidence:** ✓

## Refactor code
- **SOTA approach:** `libcst` (Meta/Instagram CST — preserves whitespace +
  comments, used on ~20M LOC at Instagram) for tree-aware mass codemods;
  `rope` for symbol rename + extract method; `ruff check --select=UP,SIM,RUF
  --fix` for mechanical pyupgrade cleanups. Run refactors in isolated git
  worktrees (`using-git-worktrees` skill).
- **Agent execution path:**
  ```
  uv add --dev libcst
  python -m libcst.tool initialize .
  python -m libcst.tool codemod rename_symbol.RenameCommand --old=Foo --new=Bar src/
  uvx rope_cli rename --old=old_name --new=new_name --module=src/pkg/mod.py
  uvx ruff check --select=UP,SIM,RUF --fix .
  ```
- **Source:** https://github.com/Instagram/LibCST ·
  https://github.com/python-rope/rope ·
  https://docs.astral.sh/ruff/rules/#pyupgrade-up
- **Skill packs:** `libcst-codemods`, `ruff-lint-format-all-in-one`
- **Confidence:** ✓

## Optimize performance
- **SOTA approach:** Profile-first (never speculate). Choose by symptom:
  `py-spy` (sampling, prod-safe) for CPU; `memray` for memory + native ext;
  `scalene` (Plasma/UMass) for unified CPU+GPU+memory with AI optimization
  suggestions; `pyinstrument` for narrative call-tree; `viztracer` for
  asyncio. Optimization order: algorithmic > batch I/O > caching > built-ins
  > `uvloop` event loop > `numba`/`cython`/`mypyc` JIT > `joblib`/`ray`/`dask`
  parallelism. Production continuous: Pyroscope / Sentry Profiling / Datadog
  Continuous Profiler.
- **Agent execution path:**
  ```
  uvx py-spy record -o flame.svg --format speedscope -- python script.py
  uvx memray run --native python script.py
  uvx memray flamegraph memray-script.py.bin
  uvx scalene --html --outfile profile.html script.py
  uvx pyinstrument script.py
  uvx viztracer python script.py
  uv add uvloop                       # drop-in faster event loop
  ```
  Open `flame.svg` in https://www.speedscope.app/ or `result.json` in
  https://ui.perfetto.dev/.
- **Source:** https://github.com/plasma-umass/scalene ·
  https://github.com/benfred/py-spy · https://github.com/bloomberg/memray ·
  https://github.com/joerick/pyinstrument · https://github.com/MagicStack/uvloop
- **Skill packs:** `py-spy-cpu-profiling`, `memray-memory-profiling`,
  `scalene-ai-optimization`, `viztracer-asyncio-timeline`
- **Confidence:** ✓

## Set up modern Python tooling
- **SOTA approach:** `uv` (project/venv/Python install/lockfile) + `ruff`
  (lint+format, 900+ rules, replaces black + isort + flake8 + pyupgrade +
  pydocstyle + bandit-lite + pylint-lite + autoflake + eradicate) + type
  checker (`mypy --strict` for prod default, `pyright` for fast,
  `pyrefly` v1.0 Meta — May 2026 stable, Rust, 10-50x faster than mypy with
  90%+ typing-spec conformance, `ty` Astral beta) + `pytest 9.x` +
  `pytest-xdist -n auto` + `slipcover` (5% overhead coverage vs pytest-cov
  180%) + `hatchling` PEP 517 backend + `src/` layout mandatory +
  `pre-commit` hooks + `commitizen` semver/CHANGELOG.
- **Agent execution path:**
  ```
  uv init --package my-pkg
  uv add --dev ruff pytest pytest-xdist pytest-asyncio pytest-cov hypothesis \
              pyrefly slipcover mutmut pre-commit commitizen
  uvx ruff check --select=ALL --fix . && uvx ruff format .
  uv run pyrefly check src/           # or: uv run mypy --strict src/
  uv run pytest -n auto --cov=src
  uvx pre-commit install
  ```
- **Source:** https://docs.astral.sh/uv/ · https://github.com/astral-sh/ruff
  · https://github.com/facebook/pyrefly/releases/tag/1.0.0 ·
  https://docs.astral.sh/ty/ · https://github.com/plasma-umass/slipcover
- **Skill packs:** `uv-uvx-modern-toolchain`, `ruff-lint-format-all-in-one`,
  `pyrefly-meta-type-checker`, `pre-commit-hook-pipeline`,
  `commitizen-semver-automation`
- **Confidence:** ✓

## Manage Git workflows
- **SOTA approach:** Conventional Commits 1.0 enforced via `commitizen`
  (`uvx cz commit` for conformant commits, `uvx cz bump` for semver +
  CHANGELOG); git worktrees sibling-directory convention (`using-git-worktrees`
  skill) for isolated feature work; `gh` CLI for PR review/comments;
  `pre-commit` framework + `ruff-pre-commit` hook (fast Rust hooks).
- **Agent execution path:**
  ```
  uvx cz commit                       # conformant commit
  uvx cz bump --changelog             # semver bump + CHANGELOG
  git worktree add ../proj-feature feature/x
  gh pr create --fill --reviewer <user>
  gh pr review <num> --approve --body "LGTM"
  uvx pre-commit run --all-files
  ```
- **Source:** https://commitizen-tools.github.io/commitizen/ ·
  https://pre-commit.com/ · https://cli.github.com/
- **Skill packs:** `commitizen-semver-automation`, `pre-commit-hook-pipeline`
- **Confidence:** ✓

## Architecture decisions (ADRs)
- **SOTA approach:** MADR 4.0 (de facto 2026 format) as the document shape;
  for tooling, choose `adr-tools` (npryce, shell, minimal) OR `adr-kit`
  (kschlt, full toolkit with validation + indexing + enforcement) OR
  `log4brains` (visual site for browsing) OR just author MADR Markdown
  directly under `docs/adr/NNNN-title.md`. Git inference + supersession
  links recommended.
- **Agent execution path:**
  ```
  npx adr-tools init docs/adr
  npx adr-tools new "Use FastAPI for the public API"
  # OR full toolkit:
  pipx install adr-kit
  adr-kit new "Adopt SQLAlchemy 2.x async"
  adr-kit validate
  # OR pure markdown:
  # write docs/adr/0001-use-fastapi.md following MADR 4.0 template
  ```
- **Source:** https://adr.github.io/madr/ ·
  https://github.com/npryce/adr-tools · https://github.com/kschlt/adr-kit ·
  https://github.com/thomvaill/log4brains
- **Skill packs:** `log4brains-adr-management`
- **Confidence:** ✓

---

## Cross-cutting SOTA tooling

| Concern | SOTA tool (2026) | Replaces | Execution path |
|---|---|---|---|
| HTTP mocking (sync/async) | `respx` (httpx-native), `pytest-httpx`, `vcrpy` (record/replay) | `requests-mock`, `responses` | `uv add --dev respx pytest-httpx vcrpy` |
| Snapshot tests | `syrupy` | `pytest-snapshot`, `snapshottest` | `uv add --dev syrupy` |
| DB integration tests | `testcontainers[postgresql]` + `pytest-asyncio` + `asyncpg`; `pyfakefs` for filesystem | mocks, `pytest-postgresql` | `uv add --dev "testcontainers[postgresql]" pytest-asyncio pyfakefs` |
| Mutation testing | `mutmut` (88.5% detection, 1200 mutants/min) | `cosmic-ray`, `MutPy` | `uvx mutmut run && uvx mutmut results` |
| Coverage | `slipcover` (5% overhead) or `pytest-cov` | manual | `uvx slipcover --branch -m pytest` |
| Dead code | `vulture` | manual review | `uvx vulture src/ tests/` |
| Dep audit | `pip-audit` (PyPA), `osv-scanner` (Google) | `safety` | `uvx pip-audit` or `osv-scanner --recursive .` |
| Secrets detection | `gitleaks`, `trufflehog` | `detect-secrets` | `gitleaks detect --source=. --no-banner` |
| Property-based testing | `hypothesis` | example-based only | `uv add --dev hypothesis` |
| Pre-commit | `pre-commit` framework + `ruff-pre-commit` hook | hand-rolled hooks | `uvx pre-commit install && uvx pre-commit run --all-files` |
| Continuous profiling (prod) | Sentry Profiling, Pyroscope, Datadog Continuous Profiler | log-only | install SDK + env vars |
| Observability | OpenTelemetry Python SDK + Sentry SDK + Honeycomb/Datadog APM | manual logging | `uv add opentelemetry-distro opentelemetry-exporter-otlp` |
| Conformant commits | `commitizen` | manual | `uvx cz commit && uvx cz bump --changelog` |
| Codemods (tree-aware) | `libcst` (Instagram) | `lib2to3`, regex | `uv add --dev libcst && python -m libcst.tool codemod ...` |

---

## Summary fulfillment table

| Use case | SOTA confidence | Path |
|---|---|---|
| Write Python code | ✓ | `cli-anything` (`uv init`, `uv add`, `uv run`) |
| Review code | ✓ | `cli-anything` (`uvx ruff/bandit/semgrep/pip-audit/gitleaks`) + `github-api` |
| Debug bugs | ✓ | `cli-anything` (`uvx py-spy/memray/viztracer`) + `sentry-mcp` |
| Refactor code | ✓ | `cli-anything` (`libcst`, `rope`, `ruff --fix`) + `using-git-worktrees` |
| Optimize performance | ✓ | `cli-anything` (`uvx py-spy/memray/scalene/pyinstrument/viztracer`) |
| Set up modern tooling | ✓ | `cli-anything` (`uv init`, `uv add --dev`, `pre-commit install`) |
| Manage Git workflows | ✓ | `git-commit` + `github`/`github-api` + `cli-anything` (`cz`, `gh`) |
| Architecture decisions | ✓ | `cli-anything` (`adr-tools`/`adr-kit`) + `filesystem` MCP |
| Tool installation on recipient | ⚠ | `uvx <tool>` is ephemeral — no install pollution — but requires `uv` installed first (`curl -LsSf https://astral.sh/uv/install.sh \| sh`) |
| Production deployment / IaC | ✗ | DevOps specialist (v1) |
| Frontend (React/Vue/Svelte) | ✗ | Frontend specialist (v1) |
| Data science / ML modeling | ✗ | Data-scientist specialist (v1) |

**Net SOTA fulfillment: ~100%** of the documented Python software-engineering
loop. Every SOTA tool — profilers, type checkers, lint, test, mutation,
codemod, security audit, AI review — is reachable through `cli-anything` +
`uvx`. No new MCP server is required for any 2026 SOTA tool.
