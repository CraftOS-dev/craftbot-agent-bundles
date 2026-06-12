<!--
Source: https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs · https://playwright.dev/docs/test-sharding · https://pytest-xdist.readthedocs.io/
Authored: June 2026 for the qa-engineer agent bundle.
-->

# CI/CD Test Integration — Matrix + Sharding + Caching

The 2026 CI test stack: **GitHub Actions matrix** (default for most teams) /
**CircleCI** / **GitLab CI** with **sharding** (Playwright `--shard=1/4`,
pytest-xdist `-n auto`), aggressive caching (deps + browsers + Docker layers),
fail-fast on smoke, parallel on regression, nightly long-running. Goal:
< 10 min PR / < 30 min main.

## When to use

- New repo wiring CI for the first time
- Existing CI slow (> 15 min PR)
- Tests run sequentially when they could parallelize
- Cache misses on every build
- Trigger phrases: "CI parallelization", "sharding", "matrix",
  "pytest-xdist", "Playwright shard", "GitHub Actions", "cache",
  "fail-fast"

## Setup

```bash
# pytest parallel
uv add --dev pytest-xdist pytest-rerunfailures

# Playwright sharding — built-in
npx playwright test --shard=1/4

# JUnit / SARIF tooling
uv add --dev pytest-junitxml
```

Auth: GitHub Actions runs natively; PATs for cross-repo dispatches only.

## Common recipes

### Recipe 1 — pytest-xdist parallel

```bash
uvx pytest -n auto                # use all CPU cores
uvx pytest -n 4                   # 4 workers
uvx pytest -n auto --dist=loadscope    # group by class/module
uvx pytest -n auto --dist=loadfile     # group by file
```

```ini
[tool.pytest.ini_options]
addopts = "-n auto --dist=loadgroup"
```

### Recipe 2 — Playwright sharding in CI

```yaml
# .github/workflows/e2e.yml
jobs:
  e2e:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: 'npm' }
      - run: npm ci
      - name: Cache Playwright browsers
        uses: actions/cache@v4
        with:
          path: ~/.cache/ms-playwright
          key: ${{ runner.os }}-pw-${{ hashFiles('package-lock.json') }}
      - run: npx playwright install --with-deps chromium
      - run: npx playwright test --shard=${{ matrix.shard }}/4
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report-${{ matrix.shard }}
          path: playwright-report/
```

### Recipe 3 — Merge sharded reports

```yaml
  merge-reports:
    if: always()
    needs: e2e
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - uses: actions/download-artifact@v4
        with:
          path: all-blobs
          pattern: playwright-report-*
          merge-multiple: true
      - run: npx playwright merge-reports --reporter=html ./all-blobs
      - uses: actions/upload-artifact@v4
        with: { name: full-html-report, path: playwright-report }
```

### Recipe 4 — Tier-aware CI

```yaml
on:
  pull_request:
  push: { branches: [main] }
  schedule: [{ cron: '0 3 * * *' }]

jobs:
  smoke:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npx playwright test --project=smoke

  critical:
    if: github.ref == 'refs/heads/main'
    needs: smoke
    runs-on: ubuntu-latest
    timeout-minutes: 35
    strategy: { matrix: { shard: [1,2,3,4] } }
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test --project=critical --shard=${{ matrix.shard }}/4

  extended:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    timeout-minutes: 180
    strategy: { matrix: { shard: [1,2,3,4,5,6,7,8] } }
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test --project=extended --shard=${{ matrix.shard }}/8
```

### Recipe 5 — Caching strategy

```yaml
# Node deps
- uses: actions/setup-node@v4
  with: { node-version: 22, cache: 'npm' }

# Python (uv)
- uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: uv-${{ hashFiles('uv.lock') }}

# Playwright browsers
- uses: actions/cache@v4
  with:
    path: ~/.cache/ms-playwright
    key: pw-${{ hashFiles('package-lock.json') }}

# Docker layer cache (Buildx)
- uses: docker/setup-buildx-action@v3
- uses: docker/build-push-action@v6
  with: { cache-from: type=gha, cache-to: type=gha,mode=max }
```

### Recipe 6 — Fail-fast on smoke

```yaml
jobs:
  smoke:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - run: npx playwright test --project=smoke
  full:
    needs: smoke   # blocked until smoke passes
    if: success()
    runs-on: ubuntu-latest
    strategy: { fail-fast: false, matrix: { shard: [1,2,3,4] } }
    steps:
      - run: npx playwright test --shard=${{ matrix.shard }}/4
```

### Recipe 7 — Selective test runs (only changed files)

```yaml
- uses: dorny/paths-filter@v3
  id: changes
  with:
    filters: |
      frontend: 'apps/web/**'
      backend: 'apps/api/**'

- if: steps.changes.outputs.frontend == 'true'
  run: npx playwright test --project=smoke

- if: steps.changes.outputs.backend == 'true'
  run: uvx pytest tests/backend/
```

### Recipe 8 — pytest CI workflow

```yaml
jobs:
  pytest:
    runs-on: ubuntu-latest
    strategy: { matrix: { python: ['3.11', '3.12', '3.13'] } }
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv python install ${{ matrix.python }}
      - run: uv sync --all-extras
      - run: uvx pytest -n auto --junitxml=junit.xml --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v4
        with: { files: coverage.xml }
      - uses: dorny/test-reporter@v1
        if: always()
        with:
          name: pytest (${{ matrix.python }})
          path: junit.xml
          reporter: java-junit
```

### Recipe 9 — Allure / merge into one report

```yaml
- run: uvx pytest --alluredir=allure-results
- uses: actions/upload-artifact@v4
  with: { name: allure-${{ matrix.shard }}, path: allure-results }

  publish:
    needs: pytest
    steps:
      - uses: actions/download-artifact@v4
        with: { pattern: allure-*, path: combined, merge-multiple: true }
      - uses: simple-elf/allure-report-action@master
        with: { allure_results: combined, allure_history: allure-history }
      - uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: allure-history
```

### Recipe 10 — Reusable workflow

```yaml
# .github/workflows/reusable-pw-shard.yml
on:
  workflow_call:
    inputs:
      shard-count: { required: true, type: number }
      project:     { required: true, type: string }

jobs:
  shard:
    runs-on: ubuntu-latest
    strategy: { matrix: { shard: [1,2,3,4,5,6,7,8] } }
    if: matrix.shard <= ${{ inputs.shard-count }}
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test --project=${{ inputs.project }} --shard=${{ matrix.shard }}/${{ inputs.shard-count }}
```

```yaml
# Caller
jobs:
  pw-smoke:
    uses: ./.github/workflows/reusable-pw-shard.yml
    with: { shard-count: 4, project: smoke }
```

### Recipe 11 — Required-status checks

```yaml
# Branch protection (via gh CLI)
gh api -X PUT /repos/$ORG/$REPO/branches/main/protection \
  -F required_status_checks.strict=true \
  -F required_status_checks.contexts[]="smoke" \
  -F required_status_checks.contexts[]="critical (shard 1)" \
  -F required_status_checks.contexts[]="critical (shard 2)" \
  -F required_status_checks.contexts[]="critical (shard 3)" \
  -F required_status_checks.contexts[]="critical (shard 4)"
```

### Recipe 12 — Retries + flake gate

```ts
// playwright.config.ts
retries: process.env.CI ? 2 : 0,
reporter: [["github"], ["html"]],

// fail PR if > 5% of tests retried
```

```yaml
- name: Flake gate
  run: |
    FLAKY=$(jq '.stats.flaky' playwright-report.json)
    EXPECTED=$(jq '.stats.expected' playwright-report.json)
    PCT=$(echo "scale=2; $FLAKY * 100 / $EXPECTED" | bc)
    if (( $(echo "$PCT > 5" | bc -l) )); then
      echo "Flake rate $PCT% > 5%"
      exit 1
    fi
```

### Recipe 13 — Docker layer cache for testcontainers

```yaml
- name: Pull testcontainers images
  run: |
    docker pull postgres:16
    docker pull redis:7
    docker pull confluentinc/cp-kafka:7.4.0
# pytest with testcontainers reuses pulled images
```

## Examples

### Example 1: Set up Playwright CI from scratch

**Goal:** Green CI on PR within 10 min.

1. Workflow (Recipe 2) — sharded smoke on PR.
2. Tier-aware structure (Recipe 4).
3. Caching (Recipe 5) — drops 2-3 min off cold runs.
4. Merge reports (Recipe 3) — single HTML for reviewers.
5. Branch protection (Recipe 11).

### Example 2: Optimize a 25-minute PR pipeline

**Goal:** Cut to < 10 min.

1. Audit: which jobs take longest? (3 min Docker build, 8 min E2E, 5 min lint).
2. Cache deps + Playwright browsers (Recipe 5) → saves 3 min.
3. Shard E2E 4-way (Recipe 2) → 8 min → 2 min wall clock.
4. Selective lint via paths-filter (Recipe 7) → only changed files.
5. Move extended E2E to main+nightly (Recipe 4).
6. Result: PR 8 min; main 15 min; nightly 60 min.

## Edge cases / gotchas

- **Sharding without merge** — 4 reports, no single view. Always merge.
- **`fail-fast: true` skips other shards** — useful for cost-saving, lethal
  for debugging. Use `fail-fast: false` on test matrices.
- **Cache eviction** — GitHub Actions caches evict at 10GB / repo. Use
  fine-grained keys; restore-keys for soft hit.
- **Cache key mismatch on lockfile change** — rebuild from scratch. Add
  `restore-keys` fallback.
- **Docker layer cache + privacy** — `cache-from: type=gha` is per-repo;
  no cross-repo cache.
- **Parallel pytest with order-dependent tests** — fails silently. Use
  `pytest-randomly` to surface; then fix.
- **Shared DB across tests** — pytest-xdist needs per-worker DB; use
  testcontainers or `pytest-xdist-worker-id`-suffixed schema.
- **Timeouts at job level** — set `timeout-minutes`; default is 6h waste.
- **Re-run failed jobs only** — GitHub re-run UI; for free-tier CI minutes,
  use `--last-failed` (pytest) on local rerun.
- **Pinned runner images change** — `ubuntu-latest` rolls forward; use
  `ubuntu-22.04` for reproducibility on critical CI.
- **Self-hosted runners** — faster but ops cost; secrets + tunneling
  considerations.
- **Bringing up DB before tests** — `services: postgres:` in jobs vs
  testcontainers in code; pick one to avoid double-setup.
- **CI-only flake** — if test passes locally but flakes in CI, likely
  resource contention; reduce parallelism or scale runner.

## Sources

- [GitHub Actions matrix](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs)
- [GitHub Actions caching](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)
- [Playwright sharding](https://playwright.dev/docs/test-sharding)
- [Playwright report merging](https://playwright.dev/docs/test-reporters#merge-reports-cli)
- [pytest-xdist](https://pytest-xdist.readthedocs.io/)
- [pytest-randomly](https://github.com/pytest-dev/pytest-randomly)
- [dorny/paths-filter](https://github.com/dorny/paths-filter)
- [astral-sh/setup-uv](https://github.com/astral-sh/setup-uv)
- [allure-report-action](https://github.com/marketplace/actions/allure-report-action)
- [Docker GitHub Actions cache](https://docs.docker.com/build/cache/backends/gha/)
