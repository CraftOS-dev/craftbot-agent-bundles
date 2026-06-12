<!--
Source: https://www.atlassian.com/agile/tutorials/bug-tracking-with-jira · https://www.atlassian.com/agile/project-management/issue-triage
Authored: June 2026 for the qa-engineer agent bundle.
-->

# Defect Triage — Severity × Priority Matrix + SLA

Severity (S1–S4 — engineering impact) and Priority (P0–P3 — business
urgency) are different axes. The 2026 SOTA: a published Sev × Pri matrix
with explicit SLAs, weekly triage cadence, auto-labelling by source signal
(Sentry / PostHog / NPS), and bug-bashes for backlog burn-down.

## When to use

- Backlog of N open bugs — what to fix next?
- Production incident — classify + assign SLA
- Weekly triage meeting — process new bugs
- Disagreement between dev + PM on "fix it now or later"
- Trigger phrases: "triage", "severity", "priority", "SLA", "P0", "S1",
  "bug bash", "defect", "backlog grooming"

## Setup

```bash
# Jira / Linear via MCP (jira-mcp / linear-mcp)
# Sentry integration (sentry-mcp)
# PostHog product issues (posthog-mcp)
```

Auth: tokens configured at the MCP level.

## Common recipes

### Recipe 1 — Severity × Priority matrix

```markdown
| Severity \ Priority | P0 (ship-blocker) | P1 (next release) | P2 (backlog) | P3 (nice-to-have) |
|---|---|---|---|---|
| **S1 — crash / data loss / security** | Hotfix < 24h | Fix current sprint | — | — |
| **S2 — major broken / no workaround** | Fix current sprint | Fix next sprint | Backlog | — |
| **S3 — minor broken / workaround exists** | — | Fix next sprint | Backlog | Tech debt |
| **S4 — cosmetic / docs** | — | — | Backlog | Tech debt / won't fix |
```

- **Severity** — engineering impact, set by QA + dev
- **Priority** — business urgency, set by PM/PO
- High S + Low P is valid (corner case crashing 0.1% of users = S1/P2)

### Recipe 2 — SLA table

```markdown
| Quadrant | Triage SLA | Fix SLA | Verify SLA |
|---|---|---|---|
| S1/P0 | < 1h | < 24h | < 4h post-fix |
| S2/P0 | < 4h | < 1 sprint | < 1 day post-fix |
| S2/P1 | < 1 day | < 2 sprints | < 1 week |
| S3/P2 | < 1 week | backlog | when picked up |
| S4/P3 | < 1 month | maybe | n/a |
```

### Recipe 3 — Severity decision tree

```markdown
START
  → Is data lost or unrecoverable?  YES → S1
  → Does it crash the app / kernel panic / WSOD?  YES → S1
  → Is it a security breach / authz bypass / PII leak?  YES → S1
  → Does a primary user journey not work?  YES → S2
  → Is there a workaround?  YES → at most S3
  → Is it visual / typo / log noise?  YES → S4
  → Otherwise → S3
```

### Recipe 4 — Priority decision tree

```markdown
START
  → Does it block a paying customer right now?  YES → P0
  → Will it block the next release?  YES → P1
  → How many users affected?
     - >5% of MAU → at most P1
     - 1-5% → P2
     - <1% (long-tail) → P3
  → Revenue impact / NPS impact:
     - direct revenue loss → P0/P1
     - brand / churn risk → P1
     - low signal → P2/P3
```

### Recipe 5 — Jira automation rules (auto-label)

```yaml
# Jira Automation rule example (yaml-ish)
trigger: Issue Created
condition: Issue Type = Bug AND project = APP
actions:
  - if: labels contains "sentry-crash"  → severity = S1
  - if: summary contains "5xx" OR "crash"  → severity = S1
  - if: labels contains "a11y"             → severity = S2
  - if: labels contains "typo"             → severity = S4
  - if: reporter is paid-customer          → priority = P1
```

### Recipe 6 — Linear triage view (built-in)

```markdown
## Linear Triage workflow
1. Create View → filter: status=Triage
2. Per-issue:
   - Set severity (custom field S1-S4)
   - Set priority (Linear's built-in 0-4)
   - Assign owner
   - Move to Backlog | This Sprint | Hotfix
3. SLA enforcement via Linear "stale" filter — bug in Triage > 24h escalates
```

### Recipe 7 — Weekly triage meeting

```markdown
## Triage — <date> — 30 min

### Attendees
QA (facilitator), Dev lead, PM, Support lead

### Agenda
- 5m: new bugs since last triage (top 10)
- 15m: walk through, set sev/pri per matrix
- 5m: SLA breaches — escalate ownership
- 5m: stats — open bugs by quadrant, age distribution

### Output
- Every new bug has sev + pri + owner + label
- Slack digest to #qa-channel
```

### Recipe 8 — Bug bash backlog burn-down

```markdown
## Bug Bash — clear S3/S4 backlog

- Pre-bash: query for S3+S4 open > 90 days
- 90-min session: triage / verify / close
- Likely outcomes:
  - Close as "no longer reproduces" (~30%)
  - Close as "won't fix" with rationale (~20%)
  - Promote 1-2 to S2 (~5%)
  - Leave as-is (~45%)
```

### Recipe 9 — Sev/Pri label sync from sources

```python
# scripts/sync_sentry_to_jira.py
# Pseudo via sentry-mcp + jira-mcp
import sentry
import jira

for issue in sentry.list_issues(project="app", status="unresolved", min_users=10):
    title = f"[Sentry] {issue['title']}"
    sev = "S1" if issue["count"] > 1000 else "S2"
    pri = "P0" if issue["users"] > 100 else "P1"
    jira.create_issue(title=title, severity=sev, priority=pri,
                      labels=["sentry", issue["culprit"]],
                      description=issue["url"])
```

### Recipe 10 — Bug filing template

```markdown
# Bug — <title>

## Severity / Priority
- Severity: S1 / S2 / S3 / S4
- Priority: P0 / P1 / P2 / P3
- Rationale: <why this quadrant>

## Repro
1. Step
2. Step
3. Observed: <what happens>
4. Expected: <what should happen>

## Environment
- Browser/Device: <Chrome 124 / iOS 18>
- Build: v1.42-rc.3 (commit <sha>)
- Account: <test account>
- Date: <timestamp>

## Evidence
- Screenshot: <link>
- Video / Loom: <link>
- Logs: <link>

## Impact
- Users affected: <count or % MAU>
- Workaround: <yes/no — describe>
- Source: <Sentry / Support / QA / UAT / user report>
```

### Recipe 11 — Stale bug auto-close

```yaml
# Linear / Jira automation
trigger: Schedule daily
condition: severity in (S3, S4) AND priority = P3 AND no_activity > 180d
action:
  - comment: "Closing stale. Reopen if still relevant."
  - status: Closed (Won't Fix)
```

### Recipe 12 — Escape-rate by severity

```markdown
## Sprint <NN> escape report
| Found in | S1 | S2 | S3 | S4 | Total |
|---|---|---|---|---|---|
| Dev / unit | 12 | 30 | 18 | 4 | 64 |
| QA / E2E | 1 | 8 | 12 | 6 | 27 |
| UAT | 0 | 1 | 3 | 1 | 5 |
| Post-release | 0 | 1 | 4 | 2 | 7 |
| Escape rate | 0% | 2.5% | 10.8% | 15.4% | 6.6% |
```

Track trend; aim S1/S2 escape rate < 1%.

## Examples

### Example 1: New bug from Support — triage in 1 hour

**Goal:** "Customer X can't check out — getting 500 error" arrives at 10:00.

1. QA reproduces — confirms 500 on `POST /checkout` for cards from EU. (Recipe 10)
2. Severity: data loss? No. Crash? Yes (500). → S1.
3. Priority: paying customers blocked. → P0.
4. SLA: hotfix < 24h. (Recipe 2)
5. Assign to backend on-call; file with `severity:S1` + `priority:P0` + `team:payments`.
6. Slack #incidents with Jira link.

### Example 2: Backlog grooming — 100 open S3 bugs

**Goal:** Halve the backlog without losing real bugs.

1. Query: S3 open > 90 days, no activity 30 days.
2. Bug bash (Recipe 8): split 50-50 with PM for 90 min.
3. Per bug: still reproduces? still relevant? still in scope?
4. Outcomes: ~50% closed (stale / no-repro / won't-fix).
5. Promote ~5% to S2 with new evidence.
6. Document policy: auto-close S3/S4 with no activity 180 days (Recipe 11).

## Edge cases / gotchas

- **Severity drift** — devs lobby for "S3 because workaround exists" when
  workaround is "users hit refresh 5 times". Triage facilitator has veto.
- **Priority politics** — every PM thinks their bug is P0. Maintain published
  matrix; P0 means "we will halt the release for this".
- **Source-bias** — Sentry crashes get S1 by default; support tickets often
  get S2. PostHog NPS-deflecting bugs underweighted. Balance signals.
- **Untriaged bugs > 1 week** — failure mode. Daily 15-min standup or
  automation alerts.
- **Reproduce-or-close** — bugs no one can reproduce stay open forever.
  Policy: close after 30 days "no repro"; reopen with evidence.
- **Customer-reported S1 without repro** — assign QA owner; pair on repro;
  collect logs + Sentry traces; never close until repro confirmed.
- **Hot-fix without regression test** — banned. Every S1 fix ships with a
  regression test in the same PR.
- **Security-severity** — overlay CVSS for sec bugs; CVSS ≥ 7.0 always S1.
- **Aging report metric** — track average age per quadrant; S1 should be
  hours-aged, never days. Visible in QA weekly digest.
- **One-off vs systemic** — if 3 S2 bugs in same area in 1 sprint, it's not
  3 bugs; it's a systemic issue. Root-cause + epic.

## Sources

- [Jira bug tracking guide](https://www.atlassian.com/agile/tutorials/bug-tracking-with-jira)
- [Jira issue triage](https://www.atlassian.com/agile/project-management/issue-triage)
- [Linear triage docs](https://linear.app/docs/triage)
- [Google SRE — incident severity](https://sre.google/sre-book/effective-troubleshooting/)
- [Atlassian — defect management](https://www.atlassian.com/agile/project-management/defect-management)
- [CVSS calculator](https://www.first.org/cvss/calculator/3.1)
- [Microsoft Engineering blog — bug triage](https://devblogs.microsoft.com/)
- [Severity vs priority deep dive (Spotify Engineering)](https://engineering.atspotify.com/)
