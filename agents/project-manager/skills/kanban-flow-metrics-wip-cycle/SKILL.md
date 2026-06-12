<!--
Source: https://www.atlassian.com/agile/kanban/metrics
Source: https://linear.app/docs/cycles
-->
# Kanban Flow Metrics (WIP / Cycle / Lead Time / Throughput) — SKILL

Cumulative Flow Diagram + WIP limits + cycle/lead time + throughput. The four leading indicators of flow health for Kanban-style teams.

## When to use

- Diagnosing flow problems: bottleneck identification via CFD.
- Setting WIP limits per column.
- Computing cycle time (start → done) + lead time (added → done) for SLA.
- Throughput forecasting for stakeholder commitments.
- Comparing scrum-vs-kanban metrics for a methodology-selection decision.

Trigger phrases: "WIP limit", "cycle time", "lead time", "throughput", "CFD", "cumulative flow", "kanban metrics", "bottleneck", "flow health".

## Setup

```bash
# Linear ships native; pull issues with timestamps
mcp tool linear.list_issues --help

# Python + matplotlib for CFD + percentile compute
uvx --from matplotlib python -c "import matplotlib; print(matplotlib.__version__)"
```

## Common recipes

### Recipe 1: Flow metric formulas
```
WIP (work-in-progress)   = count of issues in "started" / "in progress" states at time T
Cycle time (CT)          = completedAt - startedAt   (per issue; report 50th + 85th percentile)
Lead time (LT)           = completedAt - createdAt   (per issue; report 50th + 85th percentile)
Throughput (TP)          = count of issues with state=Done in [T1, T2]  (typically per week)

Little's Law:
  CT_avg = WIP_avg / TP_avg     (approximate; for stable flow)
  Implication: reduce WIP → faster cycle time (at same throughput)

WIP age:
  How long has this WIP item been in progress?
  Stale WIP (CT > 85th percentile) → escalate before it becomes a blocker
```

### Recipe 2: WIP limits (column-level)
```
Per-column WIP limits (default rule of thumb):
  "In progress" / "doing"   | ≤ team size + 50% (e.g., 5 devs → 7 limit)
  "Review" / "in review"    | ≤ team size      (e.g., 5 devs → 5 limit)
  "Testing" / "QA"          | ≤ QA count + 100% (e.g., 2 QAs → 4 limit)
  "Blocked"                 | none (count as signal; investigate any >3)

Soft limits = warn; hard limits = block PR / drag.
Linear: native WIP limits per workflow state (Settings → Workflow).
Jira: WIP limits per column on board.
```

### Recipe 3: Pull Linear issues with timestamps for CFD
```bash
# 12 weeks of data, all issues
curl -s "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d '{"query":"{ issues(filter:{updatedAt:{gte:\"2026-03-15\"}}, first:500){ nodes { id title createdAt startedAt completedAt state { name type } } } }"}' \
> issues.json
```

### Recipe 4: Cumulative Flow Diagram (CFD) generation
```python
# cfd.py — usage: uvx --from matplotlib python cfd.py issues.json
import json, sys
from datetime import datetime, timedelta
from collections import Counter
import matplotlib.pyplot as plt

issues = json.load(open(sys.argv[1]))["data"]["issues"]["nodes"]

# Generate weekly buckets
start_date = datetime(2026, 3, 15)
end_date   = datetime(2026, 6, 7)
weeks = []
cur = start_date
while cur <= end_date:
    weeks.append(cur)
    cur += timedelta(weeks=1)

# For each week, count issues in each state
states = ["backlog", "started", "completed"]
data = {s: [] for s in states}
for w in weeks:
    week_end = w + timedelta(weeks=1)
    counts = Counter()
    for i in issues:
        created = datetime.fromisoformat(i["createdAt"].rstrip("Z"))
        started = datetime.fromisoformat(i["startedAt"].rstrip("Z")) if i["startedAt"] else None
        completed = datetime.fromisoformat(i["completedAt"].rstrip("Z")) if i["completedAt"] else None
        if completed and completed <= week_end:
            counts["completed"] += 1
        elif started and started <= week_end:
            counts["started"] += 1
        elif created <= week_end:
            counts["backlog"] += 1
    for s in states:
        data[s].append(counts[s])

# Plot stacked area
fig, ax = plt.subplots(figsize=(12, 6))
ax.stackplot(weeks, data["completed"], data["started"], data["backlog"],
             labels=["Completed", "In progress", "Backlog"],
             colors=["#70ad47", "#5b9bd5", "#a5a5a5"])
ax.legend(loc="upper left")
ax.set_xlabel("Week")
ax.set_ylabel("Cumulative count")
ax.set_title("Cumulative Flow Diagram — Onboarding Revamp Q3")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("cfd.png")
```

### Recipe 5: CFD interpretation guide
```
Healthy CFD:
- 3 bands of roughly constant width
- "Completed" band growing steadily
- "Backlog" band growing modestly (some inflow)
- "In progress" band stable

Unhealthy patterns:
- Bulging "In progress" band  → WIP exploding → bottleneck downstream
- Flat "Completed" band       → throughput collapsed → investigate
- Spiky bands                 → batch behavior (sprint-end dumps) → smooth flow
- Wide "blocked" band         → dep / capacity issue

Bottleneck = column where work piles up.
```

### Recipe 6: Cycle time percentiles
```python
# cycle-time.py
import json, statistics
from datetime import datetime

issues = json.load(open("issues.json"))["data"]["issues"]["nodes"]
cycle_times = []
for i in issues:
    if i["startedAt"] and i["completedAt"]:
        s = datetime.fromisoformat(i["startedAt"].rstrip("Z"))
        c = datetime.fromisoformat(i["completedAt"].rstrip("Z"))
        cycle_times.append((c - s).total_seconds() / 86400)  # days

cycle_times.sort()
n = len(cycle_times)
print(f"N = {n}")
print(f"p50 (median): {cycle_times[n//2]:.1f} days")
print(f"p85: {cycle_times[int(n*0.85)]:.1f} days")
print(f"p95: {cycle_times[int(n*0.95)]:.1f} days")
print(f"max: {max(cycle_times):.1f} days")
```

### Recipe 7: Throughput per week
```python
# throughput.py
import json
from datetime import datetime, timedelta
from collections import Counter

issues = json.load(open("issues.json"))["data"]["issues"]["nodes"]
weekly = Counter()
for i in issues:
    if i["completedAt"]:
        d = datetime.fromisoformat(i["completedAt"].rstrip("Z"))
        # Get Monday of the week
        monday = d - timedelta(days=d.weekday())
        weekly[monday.date()] += 1

for week in sorted(weekly):
    print(f"  {week}: {weekly[week]} done")

# Rolling 4-week average for stable throughput forecast
weeks_sorted = sorted(weekly)
for i in range(3, len(weeks_sorted)):
    last_4 = [weekly[weeks_sorted[j]] for j in range(i-3, i+1)]
    print(f"  4-wk avg ending {weeks_sorted[i]}: {sum(last_4)/4:.1f} done/week")
```

### Recipe 8: Lead time vs cycle time
```python
# lead-vs-cycle.py
import json, statistics
from datetime import datetime

issues = json.load(open("issues.json"))["data"]["issues"]["nodes"]
lts, cts = [], []
for i in issues:
    if i["startedAt"] and i["completedAt"]:
        cr = datetime.fromisoformat(i["createdAt"].rstrip("Z"))
        st = datetime.fromisoformat(i["startedAt"].rstrip("Z"))
        co = datetime.fromisoformat(i["completedAt"].rstrip("Z"))
        lts.append((co - cr).total_seconds() / 86400)
        cts.append((co - st).total_seconds() / 86400)

print(f"Lead time (created→done):   median={statistics.median(lts):.1f}d, p85={sorted(lts)[int(len(lts)*0.85)]:.1f}d")
print(f"Cycle time (started→done):  median={statistics.median(cts):.1f}d, p85={sorted(cts)[int(len(cts)*0.85)]:.1f}d")
print(f"Queue time (LT - CT median): {statistics.median(lts) - statistics.median(cts):.1f}d")
```

### Recipe 9: WIP age check (stale-WIP detection)
```bash
# Issues started > p85 cycle time ago + still not done = stale
P85_DAYS=14
THRESHOLD=$(date -d "$P85_DAYS days ago" -Iseconds)

curl -s "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" \
  -d "{\"query\":\"{ issues(filter:{state:{type:{eq:\\\"started\\\"}}, startedAt:{lt:\\\"$THRESHOLD\\\"}}, first:50){ nodes { title startedAt assignee { name } } } }\"}" \
| jq '.data.issues.nodes[] | {title, startedAt, assignee: .assignee.name, age_days: ((now - (.startedAt | sub("Z$";"") | fromdateiso8601)) / 86400 | floor)}'
```

### Recipe 10: SLA from cycle time
```
SLA derivation from cycle time percentiles:
- 50th percentile CT = "typical"
- 85th percentile CT = "soft SLA"
- 95th percentile CT = "hard SLA"

Example for support team:
  CT p50 = 1d, p85 = 3d, p95 = 5d
  → Public SLA: "We respond within 5 business days, typically 1-3 days"

Don't quote the average — too sensitive to outliers; percentiles are honest.
```

### Recipe 11: Kanban-style status report block
```markdown
## Kanban flow this week
- WIP: 12 (limit 14)
- Throughput: 8 done this week (4-wk avg: 7.5/wk)
- Cycle time: p50=2.5d, p85=6d
- Lead time: p50=4d, p85=10d
- Stale WIP (>p85 age): 1 issue (LIN-289 — investigate)

### CFD trend
[Embed CFD PNG]

### Bottleneck signal
"Review" column WIP at 5/5; PRs piling. Action: pair review on rotating schedule.
```

### Recipe 12: Methodology signal: kanban vs scrum
```
WHEN KANBAN BEATS SCRUM:
- Continuous flow (support, ops, on-call)
- Unpredictable arrival rate (incidents)
- Mixed work types (no uniform "story")
- WIP discipline already strong
- Stakeholder cadence ≠ sprint cadence

WHEN SCRUM BEATS KANBAN:
- Project-scoped delivery (charter + ship date)
- Team needs cadence for stakeholder demos
- Backlog grooming + commitment ritual valuable
- Forecasting via velocity preferred over throughput

HYBRID (Scrumban):
- Scrum cadence + Kanban WIP limits
- Common in mature teams
```

### Recipe 13: Throughput forecast for stakeholder commitment
```
Question: "Will feature X ship by Q3 end?"
Method:
1. Compute remaining work (issues in scope, count)
2. Forecast throughput (rolling 4-wk avg)
3. Months remaining / avg per-month → total possible
4. Confidence band: p85 throughput pessimistic; p15 optimistic

Example:
  Remaining scope: 42 issues
  Throughput: 7.5/wk avg, 5/wk p85, 10/wk p15
  Weeks remaining: 8
  Pessimistic: 40 (5 × 8) → 95% confidence Q3 end
  Median:      60 (7.5 × 8) → comfortable
  Optimistic:  80 (10 × 8) → way ahead

Report to sponsor: "Q3 ship is 85-90% likely at current throughput."
```

## Examples

### Example 1: Diagnose flow bottleneck
**Goal:** Velocity collapsed last 2 weeks; figure out why.

**Steps:**
1. Generate CFD (Recipe 4).
2. Inspect: "In review" column ballooned from 3 to 9.
3. Reason: 2 senior reviewers OOO; juniors hesitant to approve.
4. Action: pair-review rotation; set WIP limit on review = 5; backfill OOO with cross-team reviewer.
5. Re-measure next week.

**Result:** Bottleneck identified Wed; mitigation by Fri; throughput restored Mon.

### Example 2: Set team SLA
**Goal:** Public-facing support SLA needed.

**Steps:**
1. Compute LT percentiles (Recipe 8) for support issues last 90 days.
2. p50=1.2d, p85=3.5d, p95=6.1d.
3. SLA: "Typical response 1-3 days; 95% within 6 business days."
4. Quote conservatively; update if percentiles improve.

**Result:** SLA backed by data, not aspiration.

### Example 3: Throughput-based ship-date forecast
**Goal:** Sponsor wants ship-date confidence for Q3.

**Steps:**
1. Recipe 13.
2. Result: 85-90% confidence.
3. Update sponsor brief.

**Result:** Quantified commitment; not "we think we'll make it."

## Edge cases / gotchas

- **Cycle time outliers skew averages.** Use percentiles (p50, p85), not means.
- **CFD requires good state hygiene.** Issues that skip states (created→done without "in progress") break CFD calculation.
- **WIP includes blocked.** Block ≠ done; count blocked WIP for total in-flight.
- **Throughput per "size class."** Mixing 1-pt and 13-pt issues confuses throughput. Bucket by size or use story-points-done.
- **Little's Law assumes stability.** Spiky flow breaks the approximation; use empirical p85 instead.
- **Sprint-end batch flushing.** Scrum teams artificially complete on Friday → spiky CFD. Smooth-flow Kanban is more honest.
- **WIP limits without team buy-in.** Enforced limits without team understanding why = workarounds (e.g., "in review" → "needs review" column).
- **Stale WIP > 30 days.** Probably needs to be closed or chopped, not finished. Triage weekly.
- **Lead time includes wait time.** LT - CT = queue time = how long it sat. If queue > 50% of LT, prioritization is broken.
- **Reopened issues distort percentiles.** Decide policy: count first-completion or final.
- **Throughput per "team capacity."** When 5 devs become 3, throughput shouldn't be expected to hold.
- **Forecasting from <3 months data is noisy.** Need at least 12 weeks for stable forecast.
- **Kanban skipped retros.** Continuous flow ≠ no improvement ritual. Still hold retros.
- **CFD requires Linear state mapping.** "started", "completed" are Linear state TYPES; if your team uses custom names, map to these types via API.
- **"Done" in Linear vs Done-Done.** Linear `state.type=completed` covers Done, Released, etc. — verify what counts.

## Sources

- [Atlassian Kanban metrics](https://www.atlassian.com/agile/kanban/metrics)
- [Linear cycles + analytics](https://linear.app/docs/cycles)
- [Little's Law explained](https://en.wikipedia.org/wiki/Little%27s_law)
- [Kanban University — practice guide](https://kanban.university/kanban-guide/)
- [ActionableAgile flow metrics](https://www.actionableagile.com)
- [Daniel Vacanti — Actionable Agile Metrics](https://www.actionableagile.com/book/)
- [Cumulative Flow Diagram guide](https://www.atlassian.com/agile/agile-at-scale/scaled-agile-framework)
- [Scrum.org evidence-based management](https://www.scrum.org/resources/evidence-based-management-guide)
