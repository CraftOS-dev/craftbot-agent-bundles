<!--
Source: https://instituteprojectmanagement.com/blog/critical-path-method/
Source: https://networkx.org/documentation/stable/reference/algorithms/dag.html
Source: https://smartsheet.redoc.ly
-->
# Critical Path Method (CPM) — SKILL

Forward pass + backward pass + float calculation + critical-path identification + schedule compression (crash / fast-track). The 1957-vintage method still drives every Gantt + EVM in 2026.

## When to use

- Computing earliest/latest start + finish + float for a network of tasks.
- Identifying the critical path (zero-float chain) — the longest path that determines project duration.
- Schedule compression analysis: which tasks to crash or fast-track for what cost.
- Slip impact analysis when a task overruns: how much does the project end date move?
- Cross-validating Smartsheet's `inCriticalPath` flag with networkx computation.

Trigger phrases: "critical path", "forward pass", "float", "schedule compression", "crash the schedule", "what's the longest chain", "slack", "schedule slip impact".

## Setup

```bash
# CPM computation needs Python + networkx. uvx ships ephemeral.
uvx --from networkx python -c "import networkx as nx; print(nx.__version__)"

# Smartsheet native CPM (preferred when sheet already exists):
curl -s "https://api.smartsheet.com/2.0/sheets/<sheet-id>" \
  -H "Authorization: Bearer $SMARTSHEET_TOKEN" \
| jq '.rows[] | select(.inCriticalPath) | .cells[1].value'
```

Auth:
- `SMARTSHEET_TOKEN` — if using Smartsheet native CPM (paid Pro+ plan)
- None for networkx (free)

## Common recipes

### Recipe 1: CPM forward + backward pass formulas
```
INPUTS per task: duration d, predecessors P

Forward pass (compute ES, EF):
  ES(task)  = max( EF(p) for p in predecessors )   # 0 if no preds
  EF(task)  = ES(task) + duration(task)

Project finish EF = max( EF(all leaves) )

Backward pass (compute LS, LF):
  Set LF(project finish nodes) = project EF
  LF(task)  = min( LS(s) for s in successors )
  LS(task)  = LF(task) - duration(task)

Float (slack):
  Total float (TF)  = LS - ES = LF - EF   # how late can it slip without delaying project end
  Free float  (FF)  = min(ES of successors) - EF   # without delaying any successor

Critical path:
  All tasks with TF = 0  →  on the critical path
  (Sometimes parallel critical chains exist)
```

### Recipe 2: networkx CPM script
```python
# cpm.py — usage: uvx --from networkx python cpm.py tasks.json
import json, sys
import networkx as nx

# Input format:
# tasks.json = [
#   {"id":"A","duration":5,"deps":[]},
#   {"id":"B","duration":3,"deps":["A"]},
#   {"id":"C","duration":7,"deps":["A"]},
#   {"id":"D","duration":4,"deps":["B","C"]}
# ]
tasks = json.load(open(sys.argv[1]))
G = nx.DiGraph()
for t in tasks:
    G.add_node(t["id"], duration=t["duration"])
for t in tasks:
    for d in t["deps"]:
        G.add_edge(d, t["id"])

# Forward pass
for n in nx.topological_sort(G):
    preds = list(G.predecessors(n))
    es = max((G.nodes[p]["ef"] for p in preds), default=0)
    G.nodes[n]["es"] = es
    G.nodes[n]["ef"] = es + G.nodes[n]["duration"]

project_ef = max(G.nodes[n]["ef"] for n in G.nodes)

# Backward pass
for n in reversed(list(nx.topological_sort(G))):
    succs = list(G.successors(n))
    lf = min((G.nodes[s]["ls"] for s in succs), default=project_ef)
    G.nodes[n]["lf"] = lf
    G.nodes[n]["ls"] = lf - G.nodes[n]["duration"]

# Float + critical path
critical = []
for n in G.nodes:
    tf = G.nodes[n]["ls"] - G.nodes[n]["es"]
    G.nodes[n]["tf"] = tf
    if tf == 0:
        critical.append(n)

print(f"Project duration: {project_ef} days")
print(f"Critical path: {critical}")
print("\nPer-task ES/EF/LS/LF/Float:")
for n in nx.topological_sort(G):
    d = G.nodes[n]
    print(f"  {n}: ES={d['es']} EF={d['ef']} LS={d['ls']} LF={d['lf']} TF={d['tf']}{' [CRITICAL]' if d['tf']==0 else ''}")
```

### Recipe 3: CPM with multiple critical paths
```python
# Same script — if multiple zero-float chains, all show up in `critical`
# To extract distinct paths:
critical_subgraph = G.subgraph(critical)
sources = [n for n in critical_subgraph if critical_subgraph.in_degree(n) == 0]
sinks   = [n for n in critical_subgraph if critical_subgraph.out_degree(n) == 0]
all_paths = []
for s in sources:
    for sink in sinks:
        for path in nx.all_simple_paths(critical_subgraph, s, sink):
            all_paths.append(path)
print(f"Distinct critical paths: {len(all_paths)}")
for p in all_paths: print("  -", " → ".join(p))
```

### Recipe 4: Smartsheet → CPM input JSON
```bash
# Extract rows + predecessors from a Smartsheet sheet
curl -s "https://api.smartsheet.com/2.0/sheets/<sheet-id>" \
  -H "Authorization: Bearer $SMARTSHEET_TOKEN" \
| jq '[.rows[] | {
    id: (.id | tostring),
    name: .cells[1].value,
    duration: (.cells[2].value | sub("d$"; "") | tonumber),
    deps: ((.cells[5].objectValue.predecessors // []) | map(.rowId | tostring))
  }]' > tasks.json

# Pipe to networkx
uvx --from networkx python cpm.py tasks.json
```

### Recipe 5: Verify Smartsheet's native CPM matches networkx
```bash
# Smartsheet says these are critical:
smartsheet_critical=$(curl -s "https://api.smartsheet.com/2.0/sheets/<sheet-id>" \
  -H "Authorization: Bearer $SMARTSHEET_TOKEN" \
  | jq -r '.rows[] | select(.inCriticalPath) | .id | tostring' | sort)

# networkx says these are critical:
networkx_critical=$(uvx --from networkx python cpm.py tasks.json | grep CRITICAL | awk '{print $1}' | tr -d ':' | sort)

diff <(echo "$smartsheet_critical") <(echo "$networkx_critical")
# Empty diff = agreement
```

### Recipe 6: Crash analysis (add resources to critical task)
```python
# crash.py — find the lowest-cost-per-day reduction on the critical path
# Input adds: crash_options = [{"task":"A","new_duration":3,"crash_cost":4000}, ...]
import json, networkx as nx
# ... (build G as Recipe 2) ...

# For each critical task with crash option:
crash_options = json.load(open("crash.json"))
candidates = []
for opt in crash_options:
    t = opt["task"]
    if G.nodes[t]["tf"] != 0:
        continue  # not on critical path; crashing won't help
    days_saved = G.nodes[t]["duration"] - opt["new_duration"]
    cost_per_day = opt["crash_cost"] / days_saved
    candidates.append((cost_per_day, t, days_saved, opt["crash_cost"]))

candidates.sort()
print("Crash ranked by $/day saved:")
for c in candidates:
    print(f"  ${c[0]:.0f}/day  task={c[1]}  saves={c[2]}d  total=${c[3]}")
```

### Recipe 7: Fast-track analysis (overlap sequential tasks)
```
Fast-track procedure:
1. Find FS pairs on critical path: A → B where A.duration > 2 days
2. Re-model as SS with lag = A.duration × 0.5
   Old: A (10d, FS) → B
   New: A (10d), B starts 5d after A starts (SS+5d)
3. Recompute CPM
4. Capture introduced risk: B may need rework if A's last 50% reveals issues
5. Log fast-track in RAID (R-XXX) with mitigation plan
```

### Recipe 8: Slip-impact calculator
```python
# slip.py — what happens to project end if task X slips Y days?
import networkx as nx
# ... (build G as Recipe 2) ...

def slip_impact(G, task, slip_days):
    G2 = G.copy()
    G2.nodes[task]["duration"] += slip_days
    # Re-run forward pass
    for n in nx.topological_sort(G2):
        preds = list(G2.predecessors(n))
        G2.nodes[n]["ef"] = max((G2.nodes[p]["ef"] for p in preds), default=0) + G2.nodes[n]["duration"]
    new_end = max(G2.nodes[n]["ef"] for n in G2.nodes)
    return new_end

baseline = max(G.nodes[n]["ef"] for n in G.nodes)
for slip in [1, 2, 3, 5, 7, 10]:
    new_end = slip_impact(G, "1.1.3", slip)
    print(f"Slip 1.1.3 by {slip}d → project end +{new_end - baseline}d")
```

### Recipe 9: Float-by-task heatmap (for status report)
```python
# After Recipe 2, sort by float ascending:
sorted_tasks = sorted(G.nodes, key=lambda n: G.nodes[n]["tf"])
print("Float heatmap (red = low slack):")
for n in sorted_tasks[:15]:
    tf = G.nodes[n]["tf"]
    bar = "█" * max(1, 10 - tf) + "·" * max(0, tf)
    color = "🔴" if tf == 0 else ("🟠" if tf < 3 else "🟢")
    print(f"  {color} {n}: TF={tf}d {bar}")
```

### Recipe 10: Buffer analysis (Critical Chain — Goldratt)
```
Critical Chain (CCPM) extension to CPM:
1. Remove all task-level safety margins (use 50% confidence estimates, not 90%)
2. Aggregate buffer at project end:
   - Project buffer (PB) = 50% of critical chain duration
   - Feeding buffer (FB) at end of each non-critical chain merging into critical
3. Track buffer consumption weekly:
   - PB consumed > 33% with < 33% project done → RED
   - PB consumed > 66% with < 66% project done → CRITICAL escalation
```

### Recipe 11: CPM output → status report block
```markdown
## Schedule (CPM)
- Project duration: 42 working days (baseline) → 45 (current, +3d)
- Critical path: 1.1.3 → 2.2.2 → 3.1.3 → 4.1.1
- At-risk float (<3 days): 4 tasks
- Schedule variance (SV days): -3d
- Mitigation: Crashing 3.1.3 (+$4k for -2d) brings end to +1d. Decision: approve crash → see CR-009.
```

## Examples

### Example 1: Compute CPM on a 47-leaf WBS
**Goal:** WBS done, durations estimated; need critical path before kickoff.

**Steps:**
1. Export tasks.json from Smartsheet (Recipe 4) — id, duration, deps.
2. Run `uvx --from networkx python cpm.py tasks.json` (Recipe 2).
3. Cross-check vs Smartsheet's `inCriticalPath` (Recipe 5).
4. Generate float heatmap (Recipe 9) for status report.
5. Log critical-path tasks in RAID as "high-attention" (top-5 weekly review).

**Result:** 7-task critical chain identified, 42-day baseline, 4 at-risk tasks flagged.

### Example 2: Crash decision under deadline pressure
**Goal:** Sponsor wants ship date 5 days sooner. Which tasks to crash?

**Steps:**
1. Identify crash options per critical task: hours to compress + cost (Recipe 6).
2. Rank by $/day saved.
3. Apply lowest-cost option; recompute CPM; check if new critical path emerged.
4. Iterate until 5 days saved or no more cost-effective crashes available.
5. Submit CR (cross-link change-request-management skill) with new cost + new baseline.

**Result:** "Crash 3.1.3 by 3d ($4k) + 2.2.2 by 2d ($3k) → 5d earlier ship; +$7k; CR-009."

### Example 3: Slip-impact analysis
**Goal:** Vendor delayed 3.1.3 by 4 days. How bad?

**Steps:**
1. Run Recipe 8 with task=3.1.3, slip_days=[1,2,3,4,5].
2. Output: 4-day slip → project end +4d (3.1.3 is critical; no float).
3. Check fast-track options (Recipe 7) for downstream tasks.
4. Status report RAG amber on schedule; CR if recovery not viable.

**Result:** "3.1.3 slip = critical, +4d to end. Fast-tracking 4.1.1 with 4.1.2 recovers 2d. Net slip +2d. Sponsor decision: accept or crash 4.1.2."

## Edge cases / gotchas

- **Critical path is the longest path, not the most "important" tasks.** Don't conflate criticality with priority.
- **Float assumes resource constraints satisfied.** If two non-critical tasks need the same person same week, schedule conflicts; resource-leveled CPM may shift critical path.
- **Free float ≠ total float.** Free float = slack without delaying any successor. Total float = slack without delaying project end. Free ≤ Total.
- **Multiple critical paths.** Parallel zero-float chains are common; track all of them in RAID.
- **Crashing introduces cost; fast-tracking introduces risk.** Document trade-off in CR.
- **Negative float.** If project deadline < computed EF, all tasks on critical path get negative float — means you're already late vs commitment. Either deadline moves or scope cuts.
- **Smartsheet CPM requires `projectSettings`.** Without working days set, every day counts including weekends — float computation diverges from reality.
- **Duration vs effort.** Duration = elapsed working time (5 days = 1 calendar week). Effort = person-hours. Allocation < 100% → duration > effort.
- **PERT instead of point estimate.** For volatile durations, replace `duration = d` with `expected = (o + 4m + p) / 6` per task; std-dev for risk.
- **Smartsheet predecessor lag affects critical path.** Negative lag (lead) is fine but easy to typo — check sheet preview.
- **networkx topological_sort fails on cycles.** If you have a cyclic dep, CPM is undefined — break the cycle.
- **CCPM vs CPM.** CCPM strips task buffers and aggregates them at chain ends. Switching mid-project requires rebaselining.
- **Renamed tasks break ID-based deps.** When pulling from Smartsheet rowId → task name, preserve rowId as the stable key in tasks.json.
- **Working days from calendar.** Holidays + PTO change effective durations. Sync `nonWorkingDays` to Float/Runn PTO data when computing for resource-leveled CPM.

## Sources

- [Critical Path Method canon (Institute of Project Management)](https://instituteprojectmanagement.com/blog/critical-path-method/)
- [PMI CPM guide](https://www.pmi.org/learning/library/critical-path-techniques-cpm-pert-7268)
- [networkx DAG algorithms](https://networkx.org/documentation/stable/reference/algorithms/dag.html)
- [Smartsheet inCriticalPath in API](https://community.smartsheet.com/discussion/79798/gantt-view-data-for-sheet-via-api)
- [Goldratt CCPM original](https://www.goldratt.com/critical-chain.html)
- [Smartsheet schedule compression guide](https://www.smartsheet.com/content-center/best-practices/project-management/schedule-compression)
- [PMBOK 7th Edition: scheduling performance domain](https://www.pmi.org/standards/pmbok)
