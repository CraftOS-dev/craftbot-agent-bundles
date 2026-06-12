<!--
Source: https://github.com/boxed/mutmut · https://mutmut.readthedocs.io/
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# mutmut — Mutation Testing for Python

`mutmut` (Anders Hovmöller) is the 2026 default mutation testing tool for
Python. Mutation testing answers the question: "If I deliberately break my
code, does my test suite catch it?" Published 2026 benchmark: 88.5%
mutation detection on average, ~1200 mutants/minute on commodity hardware.

Mutation testing is the gold-standard test-quality metric — line coverage
tells you what your tests TOUCH; mutation testing tells you what they
actually CHECK.

## When to use this skill

- Your test suite has 90%+ line coverage but you suspect tests are weak
- A bug slipped through despite full coverage — diagnose the gap
- New module just shipped, want a quality gate before merging
- CI nightly mutation run for long-term health monitoring
- Specific high-risk modules (auth, payments, crypto) — focused mutation runs
- Reviewing test PRs — verify the new tests actually detect mutations

Do NOT use mutmut on every PR (slow); for code with extensive integration
tests but no unit tests (mutmut works on unit-level mutations); for
abandoned modules nobody owns.

## Setup

```bash
uv add --dev mutmut
# OR ephemeral
uvx mutmut --version
```

## Common recipes

### Recipe 1 — Quick start

```toml
# pyproject.toml
[tool.mutmut]
paths_to_mutate = "src/"
runner = "uv run pytest -x --tb=short"
tests_dir = "tests/"
backup = false
also_copy = [".env.test"]
```

```bash
uvx mutmut run
uvx mutmut results
uvx mutmut show <mutant_id>
```

`mutmut run` generates mutants, runs the test suite against each, and
records survivors. `mutmut results` shows a summary; `mutmut show N`
displays the specific mutation that survived.

### Recipe 2 — Read survivors

```bash
uvx mutmut results
# Mutant survival counts per module

uvx mutmut show 42
# Shows mutant #42 diff vs original
```

A surviving mutant is a CONCRETE GAP: the code was changed and your tests
didn't notice. Read the diff, write a test that fails for the mutant,
re-run.

### Recipe 3 — Browse interactively

```bash
uvx mutmut browse
```

Curses UI listing all mutants. Filter by status (alive / killed / timeout /
skipped). Open a mutant inline for the diff. Mark "won't fix" with `s`.

### Recipe 4 — Generate HTML report

```bash
uvx mutmut html
# Writes html/index.html
open html/index.html
```

Per-file mutation score, drill-down to surviving mutants with diffs.

### Recipe 5 — Re-run only failed mutants

```bash
uvx mutmut run --rerun-all
# OR target a single mutant
uvx mutmut run --mutation-id=42
```

After fixing tests, re-run targeted mutants to confirm they now die.

### Recipe 6 — Parallel execution

```bash
uvx mutmut run --use-coverage
```

`--use-coverage` runs each mutant only against tests that touch the
mutated line (per pytest-cov data). Massive speedup vs running the full
suite every time.

### Recipe 7 — Skip mutants for certain patterns

```python
# In your code, mark lines mutmut should ignore
def expensive_init():  # pragma: no mutate
    return ExpensiveResource()
```

Or in config:

```toml
[tool.mutmut]
also_copy = [".env.test"]
disable_mutation_types = ["string", "decorator"]
```

### Recipe 8 — CI integration (nightly)

```yaml
# GitHub Actions — nightly
name: Mutation testing
on:
  schedule:
    - cron: "0 2 * * *"
jobs:
  mutmut:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync --frozen
      - run: uv run pytest                      # warm cache
      - run: uvx mutmut run --use-coverage
      - run: uvx mutmut junitxml > mutmut.xml
      - uses: actions/upload-artifact@v4
        with:
          name: mutmut
          path: mutmut.xml
```

Don't fail the build on surviving mutants unless your team has agreed on a
target. Use the artifact for trend tracking.

### Recipe 9 — Target a single module

```bash
uvx mutmut run --paths-to-mutate=src/auth/
```

Faster iteration for high-priority modules. Run on the whole codebase
weekly, on critical modules hourly.

## Mutation score targets

| Score | Interpretation |
|---|---|
| <50% | Tests are mostly smoke tests; treat with suspicion |
| 50-75% | Typical for legacy codebases — significant gaps |
| 75-90% | Healthy; address specific surviving mutants |
| 90-95% | Strong test suite; further gains have diminishing returns |
| >95% | Excellent; some surviving mutants may be unkillable (equivalent mutations) |

For critical paths (auth, payments, crypto): aim for >90%. For tooling code:
75-80% is fine.

## Common surviving mutant categories

1. **Boundary conditions** — mutant changes `<` to `<=`, tests pass.
   Fix: add tests for exact boundary values.
2. **Off-by-one** — mutant changes `range(n)` to `range(n+1)`, tests pass.
   Fix: assert exact iteration count.
3. **Conditional negation** — mutant changes `if x:` to `if not x:`, tests
   pass. Fix: add a false-branch test.
4. **Boolean operator swap** — mutant changes `and` to `or`. Fix: test both
   sides independently.
5. **Constant swap** — mutant changes `0` to `1`. Fix: assert the exact
   constant matters (e.g., enum value).
6. **String content** — mutant blanks out a log message. Fix: only matters
   if tests assert log content (often skipped intentionally).

## Edge cases

- **Equivalent mutants** — mutations that don't change observable behaviour
  (e.g., `x = x + 0`). Cannot be killed; mark as `skipped` or accept the
  score loss.
- **Test order dependence** — flaky tests cause false survivors. Run `pytest
  --random-order` first to flush these out.
- **Slow tests** — if a single mutant takes minutes, mutmut times out and
  reports `timeout`. Tune `--timeout=30` or use `--use-coverage`.
- **Stateful tests** — mutants that crash global state can break subsequent
  mutants. Use `pytest --forked` per mutant if seen.
- **CI cost** — full mutation run on a 50k-LOC project ~30 minutes with
  `--use-coverage`. Schedule nightly, not per-PR.
- **String/decorator mutations**: usually noise. Disable via
  `disable_mutation_types` to focus on logic.

## Comparison

| Tool | Status (June 2026) | Notes |
|---|---|---|
| **mutmut** | **active, SOTA** | best detection rate + speed; default choice |
| cosmic-ray | maintained | older; slower; richer mutation operators |
| MutPy | unmaintained | avoid |
| mutatest | low activity | avoid |

## Interpreting the workflow

1. Run `mutmut run` (warm up — slow first time).
2. Read `mutmut results` summary; aim for the module with the lowest score.
3. `mutmut show <id>` on a surviving mutant.
4. Write a test that would fail with the mutated code.
5. Confirm: `pytest tests/test_new.py` PASSES on original, FAILS on mutant.
6. `mutmut run --mutation-id=<id>` confirms the mutant now dies.
7. Repeat for next survivor.

## Sources

- https://github.com/boxed/mutmut — source
- https://mutmut.readthedocs.io/ — full docs
- https://johal.in/mutation-testing-with-mutmut-python-for-code-reliability-2026/ — 2026 benchmark write-up
- https://en.wikipedia.org/wiki/Mutation_testing — theory
- Offutt, "Mutation testing: A maturing technique" — academic foundation
