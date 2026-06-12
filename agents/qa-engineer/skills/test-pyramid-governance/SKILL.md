<!--
Source: https://martinfowler.com/articles/practical-test-pyramid.html · https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications · https://thoughtworks.com/radar
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Test Pyramid Governance — Pyramid vs Trophy + Suite-Size SLOs

The 2026 debate: **Pyramid** (unit > integration > E2E, Fowler) is the
classical heuristic; **Trophy** (integration-heavy, Kent C. Dodds) is
increasingly preferred for AI-first teams since LLM-generated code makes
unit ratios less meaningful. Govern via tagged tiers, suite-size SLOs (unit
< 100 ms median, integration < 5 s, E2E < 60 s), and Thoughtworks
Radar-aligned policy.

## When to use

- New repo deciding test architecture
- Existing repo with too many E2E tests (slow CI)
- Repo with too few integration tests (bugs slip through)
- Auditing pyramid health — what's the unit / integration / E2E ratio?
- Trigger phrases: "test pyramid", "trophy", "test ratio", "too many E2E",
  "suite duration", "coverage policy"

## Setup

```bash
# Coverage and tagging tools per language
uv add --dev coverage pytest-cov         # Python
npm i -D vitest @vitest/coverage-v8 c8   # JS/TS
# Java: jacoco
# .NET: coverlet
```

Auth: none.

## Common recipes

### Recipe 1 — Pyramid vs Trophy decision

```markdown
## Pyramid (Fowler) — when to choose
- Heavy backend, business logic, mature codebase
- Many pure functions / domain objects
- Strong unit-test discipline already
- Target: 70% unit / 20% integration / 10% E2E

## Trophy (Kent C. Dodds) — when to choose
- React/Vue/Svelte UI-heavy
- AI-assisted code where unit tests are easily generated but lower signal
- Microservices where integration boundaries are the risk
- Target: 25% static / 15% unit / 40% integration / 15% E2E / 5% manual
```

### Recipe 2 — Tier tagging (pytest)

```python
# pyproject.toml
[tool.pytest.ini_options]
markers = [
  "unit:        < 100ms; in-memory; no I/O",
  "integration: < 5s; real DB / fakes; one process boundary",
  "e2e:         < 60s; full stack; browser or full API",
  "manual:      not in CI; documented checklists only",
]

# tests/unit/test_pricing.py
@pytest.mark.unit
def test_apply_discount(): ...

# tests/integration/test_orders_db.py
@pytest.mark.integration
def test_orders_persisted(): ...

# tests/e2e/test_checkout_flow.py
@pytest.mark.e2e
def test_full_checkout(): ...
```

```bash
uvx pytest -m unit          # < 30 s for 1000s of tests
uvx pytest -m integration   # < 5 min
uvx pytest -m e2e           # < 15 min
```

### Recipe 3 — Tier tagging (Vitest / Playwright)

```ts
// vitest.config.ts
import { defineConfig } from "vitest/config";
export default defineConfig({
  test: {
    projects: [
      { name: "unit", testMatch: ["**/*.unit.test.ts"], testTimeout: 100 },
      { name: "integration", testMatch: ["**/*.integration.test.ts"], testTimeout: 5000 },
    ],
  },
});

// playwright.config.ts — separate runner for e2e
// projects: [{ name: 'e2e', testMatch: '**/*.e2e.spec.ts', timeout: 60_000 }]
```

### Recipe 4 — Suite-size SLOs in CI

```yaml
# .github/workflows/suite-slo.yml
- name: Unit median duration SLO
  run: |
    uvx pytest -m unit --durations=10 --collect-only -q > out.txt
    npx vitest list --reporter=json > vitest.json
    # Custom script asserts median < 100ms

- name: E2E count SLO
  run: |
    COUNT=$(grep -c '@pytest.mark.e2e' tests/e2e/**/*.py)
    if [ "$COUNT" -gt 50 ]; then
      echo "E2E count $COUNT > 50; promote some to integration"
      exit 1
    fi
```

### Recipe 5 — Audit current ratio

```bash
# pytest
uvx pytest --collect-only -q -m unit        | wc -l
uvx pytest --collect-only -q -m integration | wc -l
uvx pytest --collect-only -q -m e2e         | wc -l

# Output:
#   1247 unit
#    332 integration
#     48 e2e
# Ratio: 76% / 20% / 4% — looks pyramid-shaped
```

### Recipe 6 — Coverage policy per tier

```ini
# pyproject.toml
[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
fail_under = 80      # combined coverage
exclude_lines = [
  "pragma: no cover",
  "raise NotImplementedError",
]

# Tier-specific coverage:
# tests/unit/        → 90% line on src/domain/
# tests/integration/ → 70% line on src/adapters/
# tests/e2e/         → 50% line on src/web/
```

### Recipe 7 — Mutation score per tier (companion metric)

```bash
# Unit tier
uvx mutmut run --paths-to-mutate=src/domain/ --tests-dir=tests/unit/
# Expect kill rate > 80% — unit tests should kill mutants of core logic

# E2E tier — don't run mutation; too slow + low signal
```

### Recipe 8 — Quarantine flat tests in tier

```python
@pytest.mark.quarantine  # excluded from gate; tracked separately
def test_flaky_payment_flow(): ...
```

```ini
addopts = -m "not quarantine"
```

### Recipe 9 — Test promotion / demotion criteria

```markdown
## Promote unit → integration
- Unit test mocks > 3 collaborators
- Mock setup > 20 lines
- Test doesn't exercise the real seam

## Promote integration → E2E
- Tests the user-facing journey end-to-end
- Spans 3+ services / process boundaries

## Demote E2E → integration
- Only tests one service's HTTP contract
- Could be replaced by API test + mocked downstream

## Demote integration → unit
- Test only exercises pure logic
- Boots heavy fixture for no I/O reason
```

### Recipe 10 — Suite duration dashboard

```python
# scripts/suite_duration.py
import json, pathlib
def suite_stats(report_json):
    data = json.loads(pathlib.Path(report_json).read_text())
    tests = data["tests"]
    durations = sorted(t["duration"] for t in tests)
    return {
        "count": len(tests),
        "p50": durations[len(durations)//2],
        "p95": durations[int(len(durations)*0.95)],
        "max": durations[-1],
        "total": sum(durations),
    }

print(suite_stats("unit.json"))
print(suite_stats("integration.json"))
print(suite_stats("e2e.json"))
```

Trend over time; alert if any tier breaks SLO.

### Recipe 11 — Policy doc (`docs/testing/POLICY.md`)

```markdown
# Test Policy

## Tier definitions
| Tier | Time budget | Tools | What |
|------|-------------|-------|------|
| Unit | < 100 ms median | pytest / vitest | pure functions, no I/O |
| Integration | < 5 s median | pytest + testcontainers | DB, queue, real seams |
| E2E | < 60 s median | Playwright / pytest+httpx | full stack |
| Visual | < 30 s | Playwright toHaveScreenshot | pixel diff |
| A11y | < 30 s | axe + Lighthouse | WCAG 2.2 AA |
| Perf | nightly | k6 | thresholds |

## Ratio target — Trophy
25% static / 15% unit / 40% integration / 15% E2E / 5% manual

## CI gates
- Smoke (unit + integration) < 5 min, blocks PR
- Critical (smoke + E2E) < 30 min, blocks main
- Extended (full) nightly

## Suite-size caps
- E2E count: 50 max
- Single unit test: 200 ms max
- Single E2E test: 90 s max
- Total CI: 15 min PR / 60 min main

## Ownership
Authors own their tier choice. QA reviews at PR. Promotion/demotion
requires PR description rationale.
```

### Recipe 12 — Thoughtworks Radar alignment

```markdown
## 2026 Tech Radar positions
- ADOPT: Trophy for AI-first FE; integration tests with testcontainers
- TRIAL: Mutation testing alongside coverage; Stryker AI-pruned mutants
- ASSESS: Visual Regression with Applitools Visual AI; AI test authoring
- HOLD: 100%-coverage-as-goal; E2E for unit-coverable logic; manual regression
```

## Examples

### Example 1: Greenfield React + FastAPI — set Trophy from day 1

**Goal:** Right ratio from sprint 1.

1. Document policy (Recipe 11) with Trophy target.
2. Set Vitest + Playwright tier tagging (Recipe 3).
3. CI runs unit + integration on PR; E2E on main (Recipe 4 SLO).
4. Coverage policy: 80% combined; mutation 60% on domain (Recipe 6, 7).
5. Quarterly audit (Recipe 5) — adjust if drift.

### Example 2: Audit a slow CI — too many E2E

**Goal:** PR CI takes 30 min; want < 10 min.

1. `uvx pytest --collect-only -q -m e2e | wc -l` → 80 E2E.
2. Audit: 30 of those exercise pure backend logic.
3. Demote those to integration (Recipe 9); strip browser; use API directly.
4. Add E2E count SLO < 50 in CI (Recipe 4).
5. Run remaining E2E only post-merge (Recipe 11 CI gates).
6. CI drops to 8 min PR / 25 min main.

## Edge cases / gotchas

- **Coverage as the only goal** — 100% coverage with no mutation testing is
  a vanity number. Track mutation score alongside.
- **Tier inflation** — devs label all tests "unit" to keep tier ratio. Audit
  collected timing — actual median per tier reveals truth.
- **Trophy for everyone** — not all teams. Backend-heavy with no UI =
  Pyramid wins. Decide per-team / per-service.
- **Manual tier > 0** — some flows require human eyes (visual brand, UX
  feel). Don't pretend manual is 0.
- **Untagged tests** — fall through. Use `--strict-markers` (pytest) or
  custom CI step to fail.
- **E2E sharding to mask slowness** — 4 shards of 10 min each = 10 min wall
  clock, 40 min CPU. Cost matters.
- **Component tests not in pyramid** — Trophy treats them as integration;
  Pyramid often misses them. Decide.
- **Coverage delta is noisy** — set 1-2% tolerance in CI; otherwise rebases
  fail.
- **AI-generated unit tests of low signal** — keep them but track mutation
  kill rate; low-kill tests are noise.
- **Mutation score not measured per-tier** — unit tier should be measured;
  E2E tier doesn't make sense.
- **Suite-size caps fight features** — when team genuinely needs 60 E2E,
  raise the cap with a documented PR; don't bypass.

## Sources

- [The Practical Test Pyramid — Martin Fowler](https://martinfowler.com/articles/practical-test-pyramid.html)
- [The Testing Trophy — Kent C. Dodds](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
- [Just Say No to More End-to-End Tests — Google Testing](https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html)
- [Test Pyramid (Mike Cohn)](https://www.mountaingoatsoftware.com/blog/the-forgotten-layer-of-the-test-automation-pyramid)
- [Thoughtworks Tech Radar](https://www.thoughtworks.com/radar)
- [Coverage vs Mutation](https://stryker-mutator.io/blog/mutation-testing-as-a-quality-metric/)
- [vitest projects](https://vitest.dev/guide/projects)
- [pytest markers](https://docs.pytest.org/en/stable/how-to/mark.html)
