<!--
Source: https://github.com/facebook/pyrefly · https://github.com/facebook/pyrefly/releases/tag/1.0.0
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# pyrefly — Meta's Rust-Based Type Checker (10-50x Faster than mypy)

`pyrefly` (Meta, Rust, v1.0 stable as of May 2026) is the next-generation
Python type checker — 10-50x faster than mypy with 90%+ typing-spec
conformance. Designed as the successor to Pyre internally at Meta.

It is one of three "fast" type checkers in the 2026 landscape (alongside
Microsoft's `pyright` and Astral's `ty`), and the agent should know when
to reach for which.

## When to use this skill

- New project — choose pyrefly as the default type checker
- Mypy is too slow on a large monorepo (>100k LOC); pyrefly is the migration
  target
- CI typecheck step taking minutes; pyrefly drops it to seconds
- IDE-style fast incremental rechecks
- Strict-mode type checking with low CI cost
- Migrating from Pyre (Meta's older checker — pyrefly is its successor)

Do NOT use pyrefly when: project already uses mypy plugins (django-stubs,
sqlalchemy-stubs) — mypy plugin ecosystem is still richer. For VSCode/Pylance
inline checking, `pyright` is the embedded engine. For Astral-stack
consistency, `ty` (beta) is in the same family as `uv`/`ruff`.

## Setup

```bash
uv add --dev pyrefly
# OR ephemeral
uvx pyrefly check src/
```

Pyrefly ships pre-built binaries for Linux/macOS/Windows. No Python required
for the binary itself (it's Rust), but it does need access to your Python
environment to resolve imports.

## Common recipes

### Recipe 1 — Bootstrap config

```toml
# pyproject.toml
[tool.pyrefly]
project-includes = ["src", "tests"]
project-excludes = ["build", "dist", ".venv"]
python-version = "3.12"
search-path = ["src"]                  # PYTHONPATH-style roots
# Strict mode (recommended for new projects)
errors = ["all"]
warnings = []
```

Run:

```bash
uv run pyrefly check src/
# Reports type errors with rich locations
```

### Recipe 2 — Strict mode

```toml
[tool.pyrefly]
# Equivalent to mypy --strict
errors = [
    "all",
    "missing-return-type",
    "missing-parameter-type",
    "implicit-any",
    "untyped-call",
    "unreachable",
]
```

### Recipe 3 — CI integration

```yaml
# GitHub Actions
- uses: astral-sh/setup-uv@v3
- run: uv sync --frozen
- run: uv run pyrefly check src/
```

Pyrefly exits non-zero on type errors. Fast enough (typically <5s on a
50k LOC project) to run on every commit.

### Recipe 4 — Watch mode (dev loop)

```bash
uv run pyrefly check --watch src/
```

Incremental rechecks on file change. Reports usually in 100-500ms.

### Recipe 5 — IDE / LSP integration

```bash
uv run pyrefly lsp
```

Implements the Language Server Protocol. Configure VSCode (or any LSP
client) to point at this; you get the same checks inline. Note: Pylance
uses pyright under the hood — for in-editor experience, pyright + Pylance
remains a great choice; pyrefly LSP is catching up.

### Recipe 6 — Migrating from mypy

```bash
# 1. Install pyrefly alongside mypy
uv add --dev pyrefly

# 2. Convert config — pyrefly understands many mypy.ini directives
uvx pyrefly init                        # generates [tool.pyrefly] from [tool.mypy]

# 3. Run both for a transition period
uv run pyrefly check src/
uv run mypy --strict src/

# 4. Compare error counts — pyrefly should report ≤ mypy
# 5. Once stable, remove mypy
uv remove --dev mypy
```

Pyrefly's typing-spec conformance is 90%+, so the vast majority of mypy
errors will also be flagged by pyrefly. Edge cases (mypy plugins, some
Protocol corner cases) may differ.

### Recipe 7 — Generate type stubs from runtime

```bash
uvx pyrefly infer src/
```

Inspects code, infers stubs, writes `.pyi` files. Useful for adding types to
a previously-untyped module without rewriting it.

### Recipe 8 — Selective module strictness

```toml
[tool.pyrefly]
errors = ["all"]

[[tool.pyrefly.module-overrides]]
match = ["legacy.*"]
errors = ["return-mismatch"]              # only this category for legacy code
```

Granular control while migrating a codebase incrementally.

## Type checker decision tree (June 2026)

| Need | Choose | Why |
|---|---|---|
| Production default, mature ecosystem, plugin support | **mypy** | most plugins (django-stubs, sqlalchemy-stubs, pydantic-mypy) |
| Fast incremental + VSCode/Pylance | **pyright** | Microsoft, embedded in Pylance, Node.js-fast |
| Largest codebase + strict + CI-fast | **pyrefly** | Rust, 10-50x faster than mypy at scale |
| Astral toolchain alignment (uv + ruff + ty) | **`ty`** | same vendor, integrates cleanly; v1.0 still pending |

Practical: most projects can ship with `mypy --strict` and be fine. Pyrefly
becomes worth the switch when (a) mypy takes >30s on your codebase or
(b) you want a single Rust toolchain for lint/format/type.

## Output interpretation

```
src/foo.py:42:5: implicit-any [no-untyped-def]
  Function "process" is missing a type annotation for parameter "data".
  Hint: Use `data: dict[str, Any]` or be specific.
```

Errors include:
- File + line + column
- Error code (`no-untyped-def`)
- Severity (`error` vs `warning`)
- Description + actionable hint

`--output=json` for machine-readable.

## Edge cases

- **mypy plugin parity**: pyrefly doesn't run mypy plugins. Use stub
  packages (e.g., `django-stubs[compatible]`) instead. SQLAlchemy 2.x has
  built-in types; pydantic v2 emits its own type-checker-friendly code.
- **Cython / C extensions**: provide `.pyi` stubs; pyrefly can't introspect
  binary modules.
- **Conditional imports**: `try/except ImportError` patterns; pyrefly's
  narrowing is good but if it complains, add `# pyrefly: ignore[X]`.
- **Dynamic typing patterns**: `setattr`, `eval`, `exec` will produce
  Any-cascades. Use `cast()` or `# pyrefly: ignore`.
- **`# type: ignore` compatibility**: pyrefly understands both mypy's
  `# type: ignore` and its own `# pyrefly: ignore`. Migration-friendly.
- **Multi-version checking**: pyrefly checks against ONE `python-version`
  per run. For matrix support, run per-version in CI.
- **Strict mode default**: pyrefly is more permissive than mypy `--strict`
  by default. Set `errors = ["all"]` for parity.

## Performance numbers (Meta's published benchmarks)

| Codebase | mypy | pyright | pyrefly |
|---|---|---|---|
| Small (~5k LOC) | 3s | 2s | 0.3s |
| Medium (~50k LOC) | 30s | 12s | 2s |
| Large (~500k LOC) | 600s | 90s | 12s |
| Instagram-internal (~5M LOC) | hours | minutes | tens of seconds |

These are cold runs; incremental rechecks are sub-second.

## Sources

- https://github.com/facebook/pyrefly — source
- https://github.com/facebook/pyrefly/releases/tag/1.0.0 — v1.0 release notes (May 2026)
- https://engineering.fb.com/2026/05/pyrefly-1-0-meta-type-checker/ — Meta engineering blog
- https://docs.astral.sh/ty/ — `ty` (Astral) — sibling option
- https://github.com/microsoft/pyright — pyright source
- https://typing.readthedocs.io/en/latest/spec/ — Python typing spec
