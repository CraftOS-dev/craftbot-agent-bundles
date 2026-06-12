<!--
Source: https://pre-commit.com/ · https://github.com/pre-commit/pre-commit
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# pre-commit — Hook Pipeline for Pre-Commit / Pre-Push Validation

`pre-commit` is the de facto multi-language framework for git hooks. In 2026
the canonical Python pre-commit pipeline is ruff + ruff-format + pyrefly (or
mypy) + bandit + gitleaks + commitizen — all running in milliseconds because
ruff and pyrefly are Rust.

## When to use this skill

- Setting up a new project's hook pipeline
- Adding security-blocking hooks (secrets, deps audit) to an existing repo
- Eliminating "the formatter ran post-commit" PR churn
- Enforcing Conventional Commits at commit-msg time
- CI/local parity for lint/type/security checks
- Onboarding new contributors with consistent expectations

Do NOT use pre-commit for: slow checks (>2s — move to CI); test suites (use
pre-push instead, or just CI); checks that need network access (flaky).

## Setup

```bash
uv add --dev pre-commit
# OR via uvx for the framework itself
uvx pre-commit install
```

```bash
uvx pre-commit install                                # default: pre-commit
uvx pre-commit install --hook-type pre-push
uvx pre-commit install --hook-type commit-msg
uvx pre-commit install --install-hooks                # cache hook environments
```

## Common recipes

### Recipe 1 — Canonical Python pre-commit pipeline

```yaml
# .pre-commit-config.yaml
default_install_hook_types: [pre-commit, commit-msg, pre-push]
fail_fast: false              # run all hooks even if one fails

repos:
  # Built-ins (always)
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-toml
      - id: check-added-large-files
        args: ["--maxkb=500"]
      - id: check-merge-conflict
      - id: detect-private-key

  # Ruff (lint + format)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # Type checking (pyrefly preferred, or mypy)
  - repo: https://github.com/facebook/pyrefly
    rev: v1.0.0
    hooks:
      - id: pyrefly
        args: [check, src/]
        language: system
        types: [python]

  # Security: bandit
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.9
    hooks:
      - id: bandit
        args: [-c, pyproject.toml]
        additional_dependencies: ["bandit[toml]"]

  # Secrets: gitleaks
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.4
    hooks:
      - id: gitleaks

  # Conformant commit messages
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.13.0
    hooks:
      - id: commitizen
        stages: [commit-msg]

  # Optional: pytest at pre-push
  - repo: local
    hooks:
      - id: pytest
        name: pytest (fast)
        entry: uv run pytest -x --tb=short -q
        language: system
        pass_filenames: false
        stages: [pre-push]
```

### Recipe 2 — Install + run once

```bash
uvx pre-commit install
uvx pre-commit run --all-files            # bootstrap pass
```

The first run installs hook environments (cached in `~/.cache/pre-commit/`).
Subsequent runs hit the cache.

### Recipe 3 — Auto-update hooks

```bash
uvx pre-commit autoupdate
git diff .pre-commit-config.yaml          # review version bumps
```

Run weekly / monthly to keep tools current. Commit the resulting bump as
`chore(pre-commit): bump hooks`.

### Recipe 4 — Skip hooks selectively

```bash
SKIP=ruff git commit -m "fix: emergency"  # skip ruff only
git commit --no-verify -m "..."           # skip all (use sparingly!)
```

For the agent: NEVER use `--no-verify` unless the user explicitly asked.
Fix the underlying issue and re-commit.

### Recipe 5 — CI parity

```yaml
# GitHub Actions
- uses: actions/checkout@v4
- uses: astral-sh/setup-uv@v3
- run: uv sync --frozen
- uses: pre-commit/action@v3.0.1
```

Runs the same hooks in CI. Catches anyone who pushed with `--no-verify`.

### Recipe 6 — Selective file types

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.5.0
  hooks:
    - id: ruff
      files: ^src/
      exclude: ^src/legacy/
      types_or: [python, pyi]
```

`files` is a regex; `types_or` filters by content type detection.

### Recipe 7 — Custom local hook

```yaml
- repo: local
  hooks:
    - id: my-custom-check
      name: My custom check
      entry: uv run python scripts/check_invariants.py
      language: system
      types: [python]
      pass_filenames: true
      require_serial: true
```

For project-specific lint rules without publishing a hook repo.

### Recipe 8 — Stage-gated hooks

```yaml
- repo: local
  hooks:
    - id: full-test-suite
      name: Full test suite
      entry: uv run pytest
      language: system
      stages: [pre-push]                  # only on push, not commit
      pass_filenames: false
```

Pre-commit: fast checks only. Pre-push: heavier checks (tests, type
checking on large codebases, integration smoke).

### Recipe 9 — Performance tuning

Slow hooks are the #1 reason teams disable pre-commit. Targets:
- Total runtime <2 seconds on a typical commit (5-50 changed files).
- ruff = 100-300ms.
- pyrefly = 200-1000ms on changed files.
- bandit = 100-500ms.
- gitleaks = 100ms.

To diagnose:

```bash
time uvx pre-commit run --all-files
```

For individual hook timing, run them solo:

```bash
time uvx pre-commit run ruff --all-files
```

If a hook is slow:
- Limit `files` regex to just changed paths.
- Use `language: system` (cached env) instead of `language: python` (rebuilds).
- Move the hook to `pre-push` instead of `pre-commit`.

### Recipe 10 — Update across all repos in an org

Use `pre-commit-update` as a scheduled job, or `dependabot` for the
`.pre-commit-config.yaml` updates.

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pre-commit"
    directory: "/"
    schedule:
      interval: "weekly"
```

## Hook selection guide (by concern)

| Concern | Hook | Speed |
|---|---|---|
| Lint + format | `astral-sh/ruff-pre-commit` (ruff + ruff-format) | <300ms |
| Type checking (fast) | `facebook/pyrefly` | <1s |
| Type checking (mature) | `pre-commit/mirrors-mypy` | 5-30s — move to CI |
| Security audit | `PyCQA/bandit` | <500ms |
| Secrets scan | `gitleaks/gitleaks` | <200ms |
| Dependency audit | `pyupio/safety` or run `uvx pip-audit` in CI | 1-5s |
| Conformant commits | `commitizen-tools/commitizen` | <100ms |
| Generic file hygiene | `pre-commit/pre-commit-hooks` | <100ms |
| Custom rules | `repo: local` block | varies |

## Edge cases

- **First commit on a new repo**: hooks might fail because the env hasn't
  been cached yet. Run `uvx pre-commit run --all-files` first.
- **CI gotcha**: ensure CI checks out enough history (`fetch-depth: 0` for
  commitizen, `fetch-depth: 2` for diff-only ruff).
- **Hook environment drift**: if a hook starts failing mysteriously, run
  `uvx pre-commit clean && uvx pre-commit install --install-hooks`.
- **Large files**: `check-added-large-files` is essential — prevents
  accidental commits of binaries, datasets.
- **Merge commits**: hooks DON'T run on `git merge` by default. Use
  `--hook-type pre-merge-commit` explicitly.
- **Windows line endings**: pair with `.gitattributes` (`* text=auto eol=lf`)
  to avoid CRLF/LF churn.

## Comparison

| Framework | Notes |
|---|---|
| **pre-commit** | most-adopted, multi-language, large ecosystem |
| husky (Node) | JS-only |
| lefthook | newer, faster startup; less ecosystem |
| overcommit (Ruby) | Ruby-first; smaller ecosystem |

For Python projects, pre-commit is the default. Lefthook is a reasonable
alternative if startup time matters (Rust binary, no Python required).

## Sources

- https://pre-commit.com/ — full docs
- https://github.com/pre-commit/pre-commit — source
- https://github.com/astral-sh/ruff-pre-commit — ruff hook
- https://pre-commit.com/hooks.html — community hook registry
- https://github.com/pre-commit/pre-commit-hooks — built-ins
