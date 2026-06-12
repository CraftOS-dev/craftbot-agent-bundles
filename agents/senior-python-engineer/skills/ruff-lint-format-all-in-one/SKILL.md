<!--
Source: https://docs.astral.sh/ruff/ · https://github.com/astral-sh/ruff
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# ruff — All-in-one Lint + Format

`ruff` (Astral, Rust) is a single binary that replaces black + isort + flake8
+ pyupgrade + pydocstyle + bandit-lite + pylint-lite + autoflake + eradicate.
900+ rules, ~10-100x faster than the tools it replaces, auto-fix for ~80% of
findings.

## When to use this skill

- Setting up lint+format on a new project (replaces the entire flake8 stack)
- Auto-fixing mechanical issues during a refactor
- Pre-commit hook configuration
- CI gate for style/lint violations
- Migrating an existing project from black + isort + flake8 + pyupgrade
- Selective rule activation (e.g., security-only via `S` rules)

## Setup

```bash
uv add --dev ruff                         # project-local
# OR ephemeral
uvx ruff check .                          # no install needed
```

Verify: `uvx ruff --version` → 0.5.0 or later.

## Common recipes

### Recipe 1 — Bootstrap config

```toml
# pyproject.toml
[tool.ruff]
line-length = 120
target-version = "py312"
extend-exclude = [".venv", "dist", "build", "migrations"]

[tool.ruff.lint]
# Start broad, narrow later. ALL = enable every rule.
select = ["ALL"]
ignore = [
    "D",      # pydocstyle — pick subset later
    "ANN101", # missing self type — redundant
    "COM812", # trailing comma — handled by formatter
    "ISC001", # implicit string concat — handled by formatter
]

[tool.ruff.lint.per-file-ignores]
"tests/*"   = ["S101", "PLR2004"]  # asserts + magic numbers ok in tests
"__init__.py" = ["F401"]            # re-exports

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.isort]
known-first-party = ["my_pkg"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
docstring-code-format = true
```

### Recipe 2 — Run lint + format

```bash
uvx ruff check .                          # report only
uvx ruff check --fix .                    # auto-fix safe issues
uvx ruff check --fix --unsafe-fixes .     # auto-fix everything (review the diff!)
uvx ruff format .                         # format like black
uvx ruff check --diff .                   # preview lint fixes without writing
uvx ruff format --check .                 # CI gate — no writes, exit non-zero on diff
```

### Recipe 3 — Mechanical pyupgrade pass

When migrating a codebase to modern Python idioms:

```bash
uvx ruff check --select=UP,SIM,RUF,PT,B --fix .
uvx ruff format .
```

- `UP` — pyupgrade (3.10+ syntax: `T | None`, `list[T]`, walrus, match)
- `SIM` — flake8-simplify
- `RUF` — Ruff-specific (often catches genuine bugs)
- `PT` — flake8-pytest-style
- `B` — flake8-bugbear

This is the canonical refactor entry point; do it in its own commit.

### Recipe 4 — Security-only mode

```bash
uvx ruff check --select=S .               # flake8-bandit subset
```

Pair with `uvx bandit -r src/` for the full security audit (see
`semgrep-bandit-security-audit` skill).

### Recipe 5 — Pre-commit hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0                           # pin to a release
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

```bash
uvx pre-commit install
uvx pre-commit run --all-files
```

### Recipe 6 — CI gate

```yaml
# GitHub Actions
- uses: astral-sh/setup-uv@v3
- run: uvx ruff check .
- run: uvx ruff format --check .
```

Exit non-zero on any violation; PR is blocked until fixed.

### Recipe 7 — Narrow rule selection (after `ALL` triage)

Once `ALL` is too noisy, narrow:

```toml
[tool.ruff.lint]
select = [
    "E", "W",     # pycodestyle
    "F",          # pyflakes
    "I",          # isort
    "B",          # bugbear
    "UP",         # pyupgrade
    "SIM",        # simplify
    "RUF",        # Ruff-specific
    "S",          # bandit-lite
    "C4",         # comprehensions
    "PT",         # pytest-style
    "TID",        # tidy imports
    "PL",         # pylint-lite
    "TRY",        # tryceratops (exception patterns)
    "ASYNC",      # async-specific
]
```

## Rule families cheat-sheet

| Prefix | Origin | Use for |
|---|---|---|
| `E`, `W` | pycodestyle | basic style |
| `F` | pyflakes | unused imports, undefined names |
| `I` | isort | import ordering |
| `B` | bugbear | mutable defaults, unused loop vars, except patterns |
| `UP` | pyupgrade | modern Python idioms |
| `SIM` | simplify | simplifiable expressions |
| `RUF` | Ruff-specific | catches genuine logic bugs |
| `S` | bandit | security (hardcoded passwords, eval, weak crypto) |
| `C4` | comprehensions | comprehension efficiency |
| `PT` | pytest-style | fixtures, parametrize, raises |
| `D` | pydocstyle | docstring presence + format |
| `N` | pep8-naming | naming conventions |
| `ANN` | flake8-annotations | type hints presence |
| `ASYNC` | async-specific | blocking calls inside async |
| `PL` | pylint-lite | refactor candidates |
| `TRY` | tryceratops | try/except smells |
| `TID` | tidy imports | absolute imports, banned imports |
| `ERA` | eradicate | commented-out code |

## Edge cases

- **Per-file ignores**: `[tool.ruff.lint.per-file-ignores]` — e.g.,
  `"tests/*" = ["S101"]` to allow `assert` in tests.
- **Disable a single line**: `# noqa: F401` or `# noqa: F401, E501`.
- **Format docstrings**: `docstring-code-format = true` formats code blocks
  inside docstrings (uncommon).
- **Conflict with formatter**: COM812 / ISC001 must be ignored when using
  `ruff format` (otherwise infinite fight). Ruff prints a warning on startup
  reminding you.
- **Migrating from black**: line-length defaults differ (88 vs 120). Match
  whatever the repo standard is.
- **Migrating from flake8**: `flake8 --select` → `[tool.ruff.lint] select`.
  Most plugin codes map 1:1.
- **`--no-cache`**: rare, useful in CI if cache poisoning suspected.

## What ruff replaces

| Legacy tool | ruff equivalent |
|---|---|
| `black .` | `ruff format .` |
| `isort .` | `ruff check --select=I --fix .` (or via format) |
| `flake8 .` | `ruff check .` |
| `pyupgrade .` | `ruff check --select=UP --fix .` |
| `pydocstyle .` | `ruff check --select=D .` |
| `bandit -r .` (lite) | `ruff check --select=S .` (still run full bandit for prod audit) |
| `pylint .` (lite) | `ruff check --select=PL .` (still run pylint for full rules) |
| `autoflake .` | `ruff check --select=F401,F841 --fix .` |
| `eradicate .` | `ruff check --select=ERA --fix .` |

## Sources

- https://docs.astral.sh/ruff/ — full docs
- https://docs.astral.sh/ruff/rules/ — complete rule index
- https://docs.astral.sh/ruff/configuration/ — pyproject.toml options
- https://github.com/astral-sh/ruff — source
- https://github.com/astral-sh/ruff-pre-commit — pre-commit hook
- https://astral.sh/blog/the-ruff-formatter — formatter announcement
