<!--
Source: https://stryker-mutator.io/ · https://github.com/boxed/mutmut · https://pitest.org/
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Mutation Testing — Stryker + mutmut + Pitest

Coverage tells you the code ran. Mutation testing tells you the tests
actually catch bugs. The 2026 stack: **Stryker** for JS / TS / .NET / Scala
(Thoughtworks Radar 2026 Trial; AI-pruned mutants reduce noise 30%);
**mutmut** for Python (88.5% detection, 1200 mutants/min); **Pitest** for
Java / JVM. Kill rate complements coverage as the real quality metric.

## When to use

- Coverage is high but defects still escape
- New module — verify tests actually catch bugs before merging
- Regression hardening on critical code paths
- Justify killing low-value tests (low-mutation-kill = noise)
- Trigger phrases: "mutation testing", "Stryker", "mutmut", "Pitest",
  "kill rate", "mutation score", "test quality", "coverage is not enough"

Do NOT use for: integration / E2E tests (too slow); UI rendering tests;
suites already < 30% coverage (fix coverage first).

## Setup

```bash
# Stryker (JS/TS)
npx stryker init

# mutmut (Python)
uv add --dev mutmut
# Or
uvx mutmut --version

# Pitest (Java — Maven)
# Add to pom.xml:
#   <plugin>org.pitest:pitest-maven:1.16.x</plugin>

# cargo-mutants (Rust)
cargo install cargo-mutants
```

Auth: Stryker Dashboard token (optional, free) `STRYKER_DASHBOARD_API_KEY`.

## Common recipes

### Recipe 1 — Stryker JS/TS config

```js
// stryker.conf.mjs
export default {
  packageManager: "npm",
  reporters: ["html", "clear-text", "progress", "dashboard"],
  testRunner: "vitest",   // or jest, mocha, jasmine
  mutate: [
    "src/**/*.ts",
    "!src/**/*.spec.ts",
    "!src/**/*.test.ts",
  ],
  thresholds: { high: 80, low: 60, break: 50 },
  concurrency: 4,
  timeoutMS: 60000,
  ignoreStatic: true,
  incremental: true,
  incrementalFile: ".stryker-tmp/incremental.json",
};
```

```bash
npx stryker run
# Opens HTML report at reports/mutation/html/index.html
```

### Recipe 2 — mutmut (Python)

```bash
# pyproject.toml
[tool.mutmut]
paths_to_mutate = "src/domain/"
tests_dir = "tests/unit/"
runner = "uvx pytest -x --no-header -q"
backup = false
```

```bash
uvx mutmut run                # run all mutants
uvx mutmut results            # summary
uvx mutmut show 1             # inspect mutant 1
uvx mutmut show all           # all mutants
uvx mutmut html               # generate HTML report
```

### Recipe 3 — Pitest (Java)

```xml
<!-- pom.xml -->
<plugin>
  <groupId>org.pitest</groupId>
  <artifactId>pitest-maven</artifactId>
  <version>1.16.0</version>
  <configuration>
    <targetClasses>
      <param>com.example.domain.*</param>
    </targetClasses>
    <targetTests>
      <param>com.example.domain.*Test</param>
    </targetTests>
    <mutators>
      <mutator>STRONGER</mutator>
    </mutators>
    <mutationThreshold>60</mutationThreshold>
    <outputFormats>
      <param>HTML</param>
      <param>XML</param>
    </outputFormats>
  </configuration>
</plugin>
```

```bash
mvn test-compile org.pitest:pitest-maven:mutationCoverage
# Report at target/pit-reports/<timestamp>/index.html
```

### Recipe 4 — Incremental Stryker (only changed files)

```bash
npx stryker run --incremental
# Only mutates files changed since last run
# Stores .stryker-tmp/incremental.json
```

```yaml
# CI
- name: Stryker incremental
  run: npx stryker run --incremental
- uses: actions/cache@v4
  with:
    path: .stryker-tmp
    key: stryker-${{ github.sha }}
    restore-keys: stryker-
```

### Recipe 5 — Reading the report

```
File          Mutation score  # killed  # survived  # timeout  # no coverage
─────────────────────────────────────────────────────────────────────────────
pricing.ts          92.3%        36          3          0          0
discount.ts         68.4%        13          6          0          0
user.ts             47.1%         8          9          0          0     <-- attention
```

- **Killed** — tests caught the mutant. Good.
- **Survived** — tests did NOT catch. Your tests have a hole.
- **No coverage** — code not run by any test. Coverage hole.
- **Timeout** — likely infinite loop introduced by mutation; counts as
  killed.

### Recipe 6 — Inspect survived mutants

```bash
# mutmut
uvx mutmut show 12
# Diff view:
#   - if amount > 100:
#   + if amount >= 100:
#     return amount * 0.9

# Stryker — open HTML report → click survived → see mutated code + which tests ran
```

Fix: add a test for the boundary `amount = 100`. Re-run; mutant killed.

### Recipe 7 — Common mutators

```markdown
| Mutator | Example | What it catches |
|---|---|---|
| Conditional boundary | `>` → `>=` | off-by-one |
| Negate conditional | `if (x)` → `if (!x)` | inverted logic |
| Math operator | `+` → `-` | arithmetic |
| Return value | `return x` → `return null` | unchecked return |
| String literal | `"hello"` → `""` | string-based decisions |
| Increment | `++` → `--` | counter direction |
| Remove statement | `doSomething()` → `(removed)` | side-effect tests |
| Logical operator | `&&` → `\|\|` | short-circuit |
```

### Recipe 8 — Mutation score threshold in CI

```yaml
# Stryker
- run: npx stryker run
# Stryker exits non-zero if score < `break` threshold

# mutmut
- run: uvx mutmut run
- run: |
    SCORE=$(uvx mutmut results | grep -oP '\d+(?=%)' | head -1)
    if [ "$SCORE" -lt 60 ]; then
      echo "Mutation score $SCORE% < 60%"
      exit 1
    fi
```

### Recipe 9 — Exclude generated / vendor code

```js
// Stryker
mutate: [
  "src/**/*.ts",
  "!src/generated/**",
  "!src/vendor/**",
  "!src/**/*.constants.ts",
],
```

```toml
# mutmut
paths_to_exclude = "src/generated/, src/vendor/"
```

### Recipe 10 — AI-pruned mutants (Stryker 2026)

```js
// stryker.conf.mjs
export default {
  // experimental — needs Stryker plugin
  plugins: ["@stryker-mutator/ai-prune"],
  aiPrune: {
    model: "claude-sonnet-4",
    apiKey: process.env.ANTHROPIC_API_KEY,
    // Drops mutants the AI predicts are equivalent or unreachable
    threshold: 0.7,
  },
};
```

Saves 30% wall-clock per Thoughtworks Radar 2026.

### Recipe 11 — Stryker Dashboard publishing

```bash
STRYKER_DASHBOARD_API_KEY=... npx stryker run --reporters=dashboard
# Open https://dashboard.stryker-mutator.io/reports/<repo>
```

PR description badge:
```markdown
[![Mutation testing badge](https://img.shields.io/endpoint?style=flat&url=https%3A%2F%2Fbadge-api.stryker-mutator.io%2Fgithub.com%2Forg%2Frepo%2Fmain)](https://dashboard.stryker-mutator.io/reports/github.com/org/repo/main)
```

### Recipe 12 — cargo-mutants (Rust)

```bash
cargo install cargo-mutants
cargo mutants -- --workspace
cargo mutants --in-place -- -p crate-name
```

## Examples

### Example 1: Bootstrap mutation testing on a new module

**Goal:** Apply Stryker to `src/pricing/` first.

1. `npx stryker init` (Recipe Setup).
2. Configure to mutate only `src/pricing/` (Recipe 1).
3. First run — capture baseline score (likely 40-60%).
4. Open HTML report; inspect survived (Recipe 6).
5. Add tests for boundary / negation / return-value cases.
6. Re-run until > 80%.
7. Wire CI break threshold 60% (Recipe 8); incremental from now on.

### Example 2: Justify removing low-value tests

**Goal:** Suite has 1200 tests; want to find busy-work tests.

1. `uvx mutmut run` with full suite.
2. Compare mutation kill rate to coverage:
   - 100% coverage + 30% kill rate = tests run code but don't assert.
3. Open each file; check which tests killed mutants.
4. Tests that killed 0 mutants are candidates for review / removal.
5. PR description names the test that "would have caught" missing cases.

## Edge cases / gotchas

- **Slow on large suites** — mutmut and Stryker run the test suite once per
  mutant. Use incremental mode (Recipe 4).
- **Equivalent mutants** — semantically identical to original; can't be
  killed. Causes apparent ceiling. AI-pruning (Recipe 10) helps.
- **String / log messages mutated** — usually don't matter. Exclude with
  `ignoreStatic` (Stryker) or wrap in `# pragma: no cover`.
- **Tests that pass by accident** — mutation testing exposes them. Don't
  delete the test — strengthen the assertion.
- **Flaky tests confound mutation testing** — fix flakes first.
- **100% kill rate is suspicious** — likely tautological tests. Inspect a
  random sample.
- **Time-mutator on date code** — `time.time()` → `0` breaks every test;
  exclude or accept.
- **IO-mutator on tests with mocks** — `requests.get()` → removed; mocked
  anyway. Survived but harmless. Exclude IO calls.
- **Long-running mutmut** — `--ci` mode; or `--paths-to-mutate` to one file.
- **Stryker `incremental` cache stale** — delete `.stryker-tmp/` after
  refactor.
- **Pitest mutants for getters/setters** — set `mutators=STRONGER`; default
  includes them and inflates count.
- **Coverage tools interfere** — disable coverage when running mutation;
  it slows things further.

## Sources

- [Stryker Mutator](https://stryker-mutator.io/)
- [Stryker config](https://stryker-mutator.io/docs/stryker-js/configuration/)
- [Stryker Dashboard](https://dashboard.stryker-mutator.io/)
- [mutmut](https://github.com/boxed/mutmut)
- [mutmut docs](https://mutmut.readthedocs.io/)
- [Pitest](https://pitest.org/)
- [Pitest mutators](https://pitest.org/quickstart/mutators/)
- [cargo-mutants](https://github.com/sourcefrog/cargo-mutants)
- [Thoughtworks Tech Radar — mutation testing](https://www.thoughtworks.com/radar/techniques/mutation-testing)
- [Mutation Testing as Quality Metric](https://stryker-mutator.io/blog/mutation-testing-as-a-quality-metric/)
- [Equivalence problem (PIT)](https://blog.pitest.org/equivalent-mutations/)
