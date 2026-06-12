<!--
Source: https://docs.astral.sh/uv/
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# uv / uvx — Modern Python Toolchain

`uv` (Astral, Rust) is the universal verb for Python: package manager, virtual
environment manager, Python interpreter installer, and lockfile tool — all in
one binary, 10-100x faster than pip/poetry/pyenv. `uvx` is its ephemeral tool
runner (equivalent of `pipx run`), the agent's default way to invoke any
CLI tool without polluting the project environment.

## When to use this skill

- Initializing a new Python project (replaces `poetry new` / `python -m venv`)
- Adding/removing dependencies (replaces `pip install` / `poetry add`)
- Running tools ephemerally — `ruff`, `mypy`, `pytest`, `bandit`, `py-spy`,
  `memray`, `scalene`, etc. — without committing them as project deps
- Installing/managing Python interpreters (replaces `pyenv`)
- Migrating an existing project from pip/poetry/pipenv to uv
- Lockfile-driven reproducible installs in CI/CD
- One-off scripts using PEP 723 inline metadata

## Setup

### Install `uv` (one-liner)

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Via pip if you must
pip install uv
```

### Verify

```bash
uv --version    # ⇒ uv 0.5.x or later
uvx --version
```

`uv` writes its config to `pyproject.toml` (`[tool.uv]` section) and reads
`uv.lock` for deterministic installs. No `requirements.txt` needed.

## Common recipes

### Recipe 1 — Initialize a new project

```bash
# Library / package
uv init --package my-lib                    # adds src/ layout, hatchling build backend
cd my-lib

# Application (no build)
uv init my-app
cd my-app
```

`uv init --package` produces a `src/`-layout project with `hatchling` as the
PEP 517 backend, a `pyproject.toml` pinned to `requires-python`, and an
initial `uv.lock`.

### Recipe 2 — Add / remove dependencies

```bash
uv add fastapi[standard] sqlalchemy[asyncio] asyncpg pydantic-settings
uv add --dev ruff pytest pytest-xdist hypothesis pyrefly
uv add --group docs sphinx myst-parser           # PEP 735 dependency groups
uv remove requests                               # uninstall
```

Every `uv add` updates `pyproject.toml` AND `uv.lock` atomically. The agent
should NEVER hand-edit `uv.lock`.

### Recipe 3 — Run things

```bash
uv run python -m my_pkg                          # in-venv invocation
uv run pytest -n auto                            # uses project deps
uv run --with httpx python check.py              # add a transient dep
uv sync                                          # install lockfile contents
uv sync --frozen                                 # CI mode — fail if lockfile is stale
```

### Recipe 4 — `uvx` ephemeral tools (the agent's universal verb)

```bash
uvx ruff check --select=ALL --fix .
uvx ruff format .
uvx mypy --strict src/
uvx pytest tests/
uvx bandit -r src/
uvx pip-audit
uvx py-spy record -o flame.svg -- python script.py
uvx memray run --native python script.py
uvx scalene --html script.py
uvx pyinstrument script.py
uvx cz commit                                    # commitizen
uvx pre-commit install
```

`uvx <tool>` installs the tool into a managed cache, runs it, exits — no
project pollution. Subsequent `uvx <tool>` invocations are near-instant.

Specific tool version:

```bash
uvx ruff@0.5.0 check .
uvx --python 3.12 mypy src/
```

### Recipe 5 — Install / manage Python interpreters

```bash
uv python install 3.12                # download CPython 3.12
uv python install 3.13 3.14           # multiple versions
uv python list                        # show available + installed
uv python pin 3.12                    # write .python-version
uv venv --python 3.12                 # create venv with specific interpreter
```

This replaces `pyenv` entirely. No shims, no shell hacks.

### Recipe 6 — Migrate from pip / poetry / pipenv

From `requirements.txt`:

```bash
uv init
uv add -r requirements.txt
uv add --dev -r requirements-dev.txt
```

From `poetry`:

```bash
# uv reads poetry's pyproject.toml almost verbatim
uv sync                               # uv recognises [tool.poetry.dependencies]
# OR convert formally:
uvx migrate-to-uv                     # community converter
```

Replace `poetry run X` with `uv run X`, `poetry add X` with `uv add X`,
`poetry install` with `uv sync`.

### Recipe 7 — PEP 723 inline scripts

For one-off scripts that need dependencies without a project:

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx",
#   "rich",
# ]
# ///
import httpx
from rich import print
print(httpx.get("https://api.github.com").json())
```

Run with `uv run script.py` — uv reads the inline metadata, builds an
ephemeral venv, runs the script. No project, no manual venv.

### Recipe 8 — CI/CD lockfile workflow

```yaml
# GitHub Actions
- uses: astral-sh/setup-uv@v3
  with:
    enable-cache: true
- run: uv sync --frozen
- run: uv run pytest -n auto
```

`--frozen` fails the build if `uv.lock` is out of sync with `pyproject.toml`.
Prevents drift between dev and CI.

## Configuration reference (`pyproject.toml`)

```toml
[project]
name = "my-pkg"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115",
    "sqlalchemy[asyncio]>=2.0",
]

[dependency-groups]                   # PEP 735
dev = ["ruff>=0.5", "pytest>=8", "pyrefly>=1.0"]
docs = ["sphinx>=7"]

[tool.uv]
default-groups = ["dev"]              # include dev group by default
package = true                        # build with hatchling

[tool.uv.sources]
# Override a dep with a local path / git / index
my-internal = { path = "../my-internal" }
private-lib = { git = "https://github.com/org/repo", tag = "v1.0" }

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## Edge cases

- **Pre-existing `.venv`**: `uv` will reuse `.venv/` in the project root.
  If the interpreter doesn't match `requires-python`, it rebuilds.
- **Workspace / monorepo**: `[tool.uv.workspace]` declares member packages.
  `uv sync` installs all members in editable mode.
- **Private indices**: `[tool.uv.index]` lists alternative PyPI mirrors;
  per-dep override via `[tool.uv.sources]`.
- **Air-gapped installs**: `uv export --format requirements-txt > req.txt`
  for legacy tooling; `uv pip install` on the air-gapped side.
- **Editable installs**: `uv add --editable ./local-pkg` or use a workspace.
- **Python compatibility check**: `uv lock --upgrade` re-resolves with the
  newest matching versions; `uv lock --upgrade-package fastapi` for single.
- **Cache locations**: `~/.cache/uv` on Linux/macOS, `%LOCALAPPDATA%\uv` on
  Windows. `uv cache clean` to nuke.

## What `uv` replaces

| Legacy tool | uv equivalent |
|---|---|
| `pip install X` | `uv add X` (or `uv pip install X` for legacy compat) |
| `pip install -r requirements.txt` | `uv add -r requirements.txt` |
| `python -m venv .venv` | `uv venv` |
| `pip-compile` (pip-tools) | `uv lock` |
| `poetry add X` | `uv add X` |
| `poetry install` | `uv sync` |
| `poetry run X` | `uv run X` |
| `pipenv install X` | `uv add X` |
| `pyenv install 3.12` | `uv python install 3.12` |
| `pyenv local 3.12` | `uv python pin 3.12` |
| `pipx install X` | `uv tool install X` (persistent) |
| `pipx run X` | `uvx X` (ephemeral) |

## Sources

- https://docs.astral.sh/uv/ — official docs
- https://docs.astral.sh/uv/guides/projects/ — project workflow
- https://docs.astral.sh/uv/guides/scripts/ — PEP 723 inline scripts
- https://github.com/astral-sh/uv — source
- https://astral.sh/blog/uv — initial announcement
- https://peps.python.org/pep-0735/ — dependency groups
