<!--
Source: https://dora.dev/research/ · https://martinfowler.com/articles/qualityMetrics.html · https://docs.sonarsource.com/sonarqube-server/
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Quality KPIs — Escape Rate + MTTR + Flakiness + Mutation Score

The 2026 QA KPI stack: **escape rate** (defects found post-release / total —
target < 5%), **MTTR** (P0 < 24h, P1 < 7d), **flakiness** (< 2% of CI
runs), **coverage trend**, **mutation score** (> 60% on changed files),
**DORA** (change-failure rate, lead time, deploy freq, restore time).
SonarQube + CodeClimate for code-quality gates. Reported in weekly digest +
sprint retro.

## When to use

- Setting up QA KPI dashboard for the first time
- Weekly QA digest needed for engineering leadership
- Quality regression — which lever moved?
- Justifying QA headcount / tooling investment
- Trigger phrases: "quality KPIs", "escape rate", "MTTR", "flakiness",
  "mutation score", "coverage", "DORA", "SonarQube", "CodeClimate"

## Setup

```bash
# Data sources
# - Jira / Linear for defects (jira-mcp / linear-mcp)
# - GitHub Actions for CI run history (github-api MCP)
# - Sentry for prod errors (sentry-mcp)
# - PostHog for product-side defect signals (posthog-mcp)
# - SonarQube / SonarCloud for code quality
# - mutmut / Stryker / Pitest output

# Visualization
# - Grafana dashboard
# - PostHog dashboard
# - Notion table
# - Excel / Google Sheets weekly
```

Auth: tokens for each data source.

## Common recipes

### Recipe 1 — Master KPI scorecard

```markdown
# Quality Scorecard — Sprint <NN> — <date>

## Outcome KPIs (what users feel)
| KPI | Target | Actual | Trend | Verdict |
|---|---|---|---|---|
| Escape rate | < 5% | 3% | ▼ | ✓ |
| P0 MTTR | < 24h | n/a | — | ✓ |
| P1 MTTR | < 7d | 3d | ▼ | ✓ |
| User-reported defects | < 5 / wk | 2 / wk | ▼ | ✓ |
| NPS detractor-mentioned bugs | < 3 / mo | 1 / mo | flat | ✓ |

## Process KPIs (how the team runs)
| KPI | Target | Actual | Trend | Verdict |
|---|---|---|---|---|
| Flakiness | < 2% | 4% | ▲ | ✗ |
| CI duration (PR) | < 10 min | 8 min | flat | ✓ |
| Coverage delta | > -1% | +0.4% | flat | ✓ |
| Mutation score (changed) | > 60% | 67% | ▲ | ✓ |
| Smoke duration | < 5 min | 4m 23s | flat | ✓ |
| Tests skipped (quarantine) | < 10 | 7 | flat | ✓ |
| Open quarantine > 14d | 0 | 1 | ▲ | ✗ |

## DORA (delivery)
| Metric | Elite | Actual | Trend |
|---|---|---|---|
| Lead time | < 1d | 1.2d | ▼ |
| Deploy freq | multi/day | daily | flat |
| Change failure | < 5% | 4% | ▼ |
| MTTR | < 1h | 35m | ▼ |
```

### Recipe 2 — Escape rate calculation

```python
# scripts/escape_rate.py
"""Defects found post-release / total defects in window."""
from datetime import datetime, timedelta
import jira  # jira-mcp wrapper

def escape_rate(release_tag: str, window_days: int = 14):
    release_date = jira.get_release_date(release_tag)
    window_end = release_date + timedelta(days=window_days)

    all_defects = jira.search(
        f'project = APP AND issuetype = Bug AND created >= "{release_date}" '
        f'AND created <= "{window_end}"'
    )
    post_release = [d for d in all_defects if d.found_in_env == "production"]

    return {
        "release": release_tag,
        "window": f"{release_date} to {window_end}",
        "total": len(all_defects),
        "post_release": len(post_release),
        "escape_rate": len(post_release) / len(all_defects) if all_defects else 0,
    }

print(escape_rate("v1.42"))
# {'release': 'v1.42', 'total': 47, 'post_release': 2, 'escape_rate': 0.043}
```

### Recipe 3 — MTTR per severity

```python
def mttr_by_severity(window_days: int = 30):
    defects = jira.search(
        f'project = APP AND status = Closed AND resolutiondate >= -{window_days}d'
    )
    by_sev = collections.defaultdict(list)
    for d in defects:
        if d.severity:
            delta = (d.resolution_date - d.created).total_seconds() / 3600  # hours
            by_sev[d.severity].append(delta)

    for sev in ["S1", "S2", "S3", "S4"]:
        if by_sev[sev]:
            median = statistics.median(by_sev[sev])
            print(f"{sev} MTTR median: {median:.1f}h  (n={len(by_sev[sev])})")
```

### Recipe 4 — Flakiness rate from CI history

```python
def flakiness(repo: str, days: int = 7):
    runs = gh.list_workflow_runs(repo, "e2e.yml", created=f">={days}d")
    flaky_runs = 0
    for r in runs:
        report = json.loads(r.artifacts["playwright-report"].download())
        if any(t["status"] == "flaky" for t in report["tests"]):
            flaky_runs += 1
    return flaky_runs / len(runs) if runs else 0

print(f"Flakiness: {flakiness('org/repo'):.1%}")
```

### Recipe 5 — Coverage trend over time

```bash
# pytest-cov writes coverage.xml
uvx pytest --cov=src --cov-report=xml --cov-report=term

# Upload to Codecov / Coveralls
codecov -f coverage.xml

# Plot trend
curl -H "Authorization: Bearer $CODECOV_TOKEN" \
  "https://codecov.io/api/v2/github/$ORG/repos/$REPO/coverage/trend?days=90" \
  | jq '.results[] | {date, coverage}'
```

### Recipe 6 — Mutation score per release

```bash
# After mutmut run
uvx mutmut results --no-color > mutmut.txt
SCORE=$(grep "tested" mutmut.txt | grep -oP '\d+(?=/\d+)')
TOTAL=$(grep "tested" mutmut.txt | grep -oP '(?<=/)\d+')
PCT=$(echo "scale=2; $SCORE * 100 / $TOTAL" | bc)
echo "Mutation score: $PCT%"
```

Track per release in Notion or Grafana.

### Recipe 7 — SonarQube quality gates

```bash
# Self-host
docker run -d --name sonarqube -p 9000:9000 sonarqube:lts-community

# Scan
sonar-scanner \
  -Dsonar.projectKey=myproject \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=$SONAR_TOKEN \
  -Dsonar.coverage.exclusions=**/test/**
```

```yaml
# Quality Gate UI → set:
# - Coverage > 80%
# - Duplications < 3%
# - Maintainability rating: A
# - Reliability rating: A
# - Security rating: A
# - Security hotspots reviewed: 100%
# - New code conditions: same as above on changed lines
```

### Recipe 8 — CodeClimate maintainability

```yaml
# .codeclimate.yml
version: "2"
plugins:
  duplication:
    enabled: true
  fixme:
    enabled: true
  structure:
    enabled: true
checks:
  argument-count: { config: { threshold: 4 } }
  complex-logic: { config: { threshold: 4 } }
  file-lines: { config: { threshold: 250 } }
  method-complexity: { config: { threshold: 5 } }
```

```bash
codeclimate analyze
codeclimate engines:install
```

### Recipe 9 — Weekly QA digest

```markdown
# QA Weekly — Sprint <NN> — <date>

**Escape rate:** 3% (target < 5%) — ▼
**P0 MTTR:** n/a (0 P0)
**P1 MTTR:** 3d (target < 7d) — ▼
**Flakiness:** 4% (target < 2%) — ▲ ⚠
**Coverage:** line 82.4% / branch 73.1% / mutation 67%
**Suite duration:** smoke 4m / critical 22m / extended 1h 47m
**DORA change-failure:** 4% — ▼

**Top 3 quality risks this week:**
1. Flakiness rising in checkout — Alice investigating
2. Mutation score regressed 5% in refunds module — Bob to add property tests
3. 3 quarantined tests past 14d deadline — delete this week

**Quarantined tests:** 7 (open ticket count); fix-by deadlines this week: T-1284 (Fri)

**Top defects closed:** PROJ-1284 (S2 — refund off-by-one), PROJ-1300 (S2 — invite spam)
```

### Recipe 10 — Grafana dashboard panels

```json
// Grafana panels (sketch)
{
  "panels": [
    { "title": "Escape rate (30d)", "datasource": "postgres", "query": "..." },
    { "title": "Flakiness (7d)", "datasource": "github-actions", "query": "..." },
    { "title": "Coverage trend (90d)", "datasource": "codecov", "query": "..." },
    { "title": "Mutation score (last release)", "datasource": "ci-artifacts" },
    { "title": "DORA quartet", "datasource": "..." }
  ]
}
```

### Recipe 11 — Slack weekly digest automation

```python
# Schedule cron — Mon 09:00
def send_weekly_digest():
    metrics = {
        "escape_rate": escape_rate("v1.42"),
        "mttr_p1": mttr_by_severity()[1]["P1"],
        "flakiness": flakiness("org/repo", 7),
        "coverage": codecov.latest("org/repo"),
        "mutation": parse_mutmut_results(),
    }
    msg = format_digest(metrics)
    slack.post("#qa-channel", msg)
```

### Recipe 12 — Pyramid of KPIs (what to track at what level)

```markdown
## Leadership / weekly
- Escape rate
- MTTR P0/P1
- DORA quartet
- CSAT / NPS bug-mentioned

## QA team / weekly
- Flakiness
- Coverage delta
- Mutation score (changed)
- Defects opened / closed
- Suite duration

## Per-PR / per-merge
- CI green
- Coverage delta
- Mutation regression
- A11y / security gate
- Number of tests added
```

### Recipe 13 — Anti-metrics (gameable / misleading)

```markdown
## Don't optimize for these alone
- Test count (you can pad)
- Coverage % (without mutation, vanity)
- Bug count (depends on reporting culture)
- CI green % (re-runs hide red)
- "Lines of test" (verbose tests aren't better tests)
```

### Recipe 14 — KPI regression alerting

```yaml
# .github/workflows/kpi-alert.yml
on: { schedule: [{ cron: '0 9 * * 1' }] }   # Monday 09:00
jobs:
  alert:
    runs-on: ubuntu-latest
    steps:
      - run: python scripts/compute_kpis.py > current.json
      - run: python scripts/compare_to_baseline.py current.json baseline.json
      - if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          payload: '{"text": "KPI regression detected — see ${{ github.run_id }}"}'
```

## Examples

### Example 1: First QA dashboard

**Goal:** Stand up KPI dashboard in 1 sprint.

1. Pick 5-7 KPIs (Recipe 1).
2. Data sources via MCP (jira / github / sentry / posthog).
3. Compute scripts (Recipes 2-6); cron weekly.
4. Slack digest (Recipe 11).
5. Notion page links to detailed dashboards.
6. Review at sprint retro.

### Example 2: KPI regression alert

**Goal:** Flakiness up from 1% to 4%; act fast.

1. Alert in Slack (Recipe 14).
2. Drill down per Recipe 4 — which tests + which week.
3. Open issues per flaky test (`flaky-test-quarantine-root-cause` skill).
4. Track to recovery: re-measure next Monday.
5. Sprint retro: discuss cause + counter-measure.

## Edge cases / gotchas

- **Escape rate by source** — Sentry-found vs Support-found differ; track
  both.
- **MTTR median vs mean** — median for typical; mean skewed by long tail.
  Show both.
- **Coverage on generated code** — exclude or it inflates the number.
- **Mutation on legacy** — score regression on old code may not be team's
  fault; threshold per-file or per-changed-line.
- **DORA gaming** — splitting one PR to inflate deploy count. Look at
  intent, not raw count.
- **Sample size for small teams** — weekly noise overshadows signal; report
  rolling 4-week average.
- **Sentry overcount** — same exception in 1000 sessions counts once for
  triage but inflates "errors". Use issue count, not event count.
- **Flakiness includes infrastructure flake** — DNS, runner, network. Tag
  source; separate suite-flake from infra-flake.
- **Mutation timeout = killed?** — most tools default yes; consider
  excluding timeouts from kill rate if running pure-IO code.
- **NPS detractor data lag** — 30 days behind shipping. Use as long-term
  signal.
- **Customer-impacting vs internal-detected** — escape rate should exclude
  internal-detected post-release (Sentry + observability) if they were
  not user-felt.

## Sources

- [DORA research](https://dora.dev/research/)
- [DORA quartet of metrics](https://dora.dev/quickcheck/)
- [Martin Fowler — Quality Metrics](https://martinfowler.com/articles/qualityMetrics.html)
- [SonarQube](https://docs.sonarsource.com/sonarqube-server/)
- [SonarCloud](https://www.sonarsource.com/products/sonarcloud/)
- [CodeClimate Quality](https://codeclimate.com/quality)
- [Codecov trends](https://docs.codecov.com/)
- [PostHog product analytics](https://posthog.com/docs)
- [Sentry release health](https://docs.sentry.io/product/releases/health/)
- [Atlassian — Quality metrics](https://www.atlassian.com/agile/software-development/metrics)
- [Goodhart's Law](https://en.wikipedia.org/wiki/Goodhart%27s_law)
- [Lighthouse CI scoring](https://web.dev/measure/)
