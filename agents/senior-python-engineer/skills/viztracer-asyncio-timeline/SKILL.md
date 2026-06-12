<!--
Source: https://github.com/gaogaotiantian/viztracer · https://viztracer.readthedocs.io/
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# viztracer — Perfetto-Backed Asyncio Timeline Profiler

`viztracer` (Tian Gao) is a deterministic tracer that produces a **timeline
view** of every function call, exported as JSON for Google's Perfetto UI.
Unlike sampling profilers (py-spy, scalene), viztracer records every
function entry/exit — giving you an actual timeline you can scrub through.

This is the 2026 SOTA for asyncio task-contention diagnosis where "which
coroutine ran when?" is the question, not "what's the hottest function?"

## When to use this skill

- Asyncio deadlock / starvation / contention diagnosis
- "Why did this task wait so long?" timeline scrubbing
- Multi-process / multi-threaded trace combination
- Visualising the temporal order of awaits in a complex coroutine graph
- Reproducing a transient bug via a recorded trace
- Educational: showing other engineers what `await` actually does

Do NOT use viztracer for: production attach (overhead is 1.5-2x — too high),
flamegraph aggregations (use py-spy), memory profiling (use memray), or
short scripts where `time` alone tells the story.

## Setup

```bash
uv add --dev viztracer
# OR ephemeral
uvx viztracer python script.py
```

Cross-platform. Outputs `result.json` (HTML view or Perfetto-compatible).

## Common recipes

### Recipe 1 — Trace + view in Perfetto

```bash
uvx viztracer python script.py
# Produces result.json
# Open https://ui.perfetto.dev/, drag-drop result.json
```

The Perfetto UI shows each thread/process as a swimlane, with function calls
as colored bars on the timeline. Click any bar for stack details. Search,
filter, zoom.

### Recipe 2 — Built-in HTML viewer

```bash
uvx viztracer --output_file trace.html python script.py
open trace.html              # standalone, no Perfetto needed
```

Single self-contained HTML file. Best for sharing in PRs / issue threads.

### Recipe 3 — Asyncio task timeline

```bash
uvx viztracer --log_async python my_async_app.py
```

`--log_async` records every coroutine creation, awaits, and resumes —
producing a true asyncio task swimlane in the Perfetto view. This is the
killer feature.

### Recipe 4 — Attach to a function only

For long-running services, recording everything is overkill. Trace just one
function:

```python
from viztracer import VizTracer

with VizTracer(output_file="trace.json", log_async=True) as tracer:
    await my_problematic_function(args)
```

Records only the scope of the `with` block. Adds 1.5-2x overhead to that
scope, zero elsewhere.

### Recipe 5 — Multi-process tracing

```bash
uvx viztracer --multi_process python service.py
# Produces per-process JSON files, then merged
```

For gunicorn / multiprocessing workers, generates one trace per process and
combines into a single Perfetto timeline. See cross-process await/result
ordering.

### Recipe 6 — Custom log events

Annotate the trace with domain-specific events:

```python
from viztracer import VizTracer, get_tracer

tracer = VizTracer(output_file="trace.json")
tracer.start()

with tracer.log_event("db_query"):
    rows = await conn.fetch("SELECT ...")

tracer.log_instant("cache_hit", args={"key": cache_key})

tracer.stop()
tracer.save()
```

In Perfetto, `log_event` shows as a custom bar; `log_instant` as a vertical
line. Use for "this is when the cache was checked", "this is when the DB
replied", etc.

### Recipe 7 — Sampling mode (lower overhead)

```bash
uvx viztracer --tracer_entries 1000000 --include_files src/ python script.py
```

`--tracer_entries` caps the buffer; `--include_files` skips library code
(huge overhead reduction). Once viztracer is too slow, switch to py-spy
sampling.

### Recipe 8 — Diff two traces

No built-in diff. Workflow:
1. Save `before.json` and `after.json`.
2. Open both in separate Perfetto tabs.
3. Use the "Pin to Top" feature to keep the comparison aligned.

## Interpreting an asyncio timeline

Typical layout in Perfetto with `--log_async`:

```
main thread
  ├── event_loop.run_until_complete
  │     ├── Task-1 [coroutine_a]   ████   ░░░░░   █████
  │     ├── Task-2 [coroutine_b]   ░░░░   █████   ░░░░░
  │     └── Task-3 [coroutine_c]   ░     ░░░░░░░░░░░    ████
  └── ...
```

- **█ blocks** — coroutine is currently running (holds the event loop).
- **░ gaps** — coroutine is awaiting (suspended).
- **Gaps where you expected work** — accidental serial awaits where
  `asyncio.gather` would parallelize.
- **Long █ blocks** — blocking call inside async (a `time.sleep`,
  `requests.get`, CPU-bound work). Convert to `await asyncio.sleep` or
  `await asyncio.to_thread(...)`.
- **Task starvation** — one task hogs the loop, others get no █ blocks.
  Yield more frequently or move CPU work off-loop.

## Edge cases

- **Overhead**: 1.5-2x slowdown. Not for production. For prod use, run a
  short window via `with VizTracer(...)` around the suspect path.
- **Trace file size**: 5-50 MB typical, can hit hundreds of MB on busy
  code. Use `--max_stack_depth` and `--include_files` to constrain.
- **Multiprocessing pickling**: `--multi_process` works for `spawn` and
  `fork`; pickling complex types may fail — keep traces of payloads small.
- **C extension internals**: viztracer doesn't see inside C extensions
  (asyncpg, orjson). Top-level calls visible; internals not.
- **Cython-compiled code**: similar — visible at boundaries, internals
  opaque.
- **Coroutine name mangling**: lambdas / nested async functions get auto-
  generated names; rename inline lambdas to named functions for clearer
  traces.
- **Jupyter integration**: `%load_ext viztracer && %%viztracer cell-code`
  gives you a trace per cell.

## Comparison

| Need | Best tool |
|---|---|
| "Where is CPU going?" | `py-spy` (sampling, lowest overhead) |
| "When did this task run?" | **`viztracer`** (deterministic timeline) |
| Memory leak / native allocs | `memray` |
| Per-line CPU + memory + AI hints | `scalene` |
| Narrative call tree | `pyinstrument` |

In practice: start with py-spy ("is it CPU-bound at all?"); if yes and it's
asyncio, switch to viztracer to see WHEN tasks ran; for the inner loop's
hot spots, drop down to scalene or py-spy `--native`.

## CLI quick reference

```
viztracer                  # trace mode
viztracer --output_file FILE
viztracer --log_async            # asyncio task swimlanes
viztracer --log_func_args        # capture argument reprs (expensive)
viztracer --log_return_value     # capture return reprs (expensive)
viztracer --multi_process        # multi-process tracing
viztracer --include_files PAT    # only trace these paths
viztracer --exclude_files PAT    # skip these paths
viztracer --tracer_entries N     # buffer size
viztracer --max_stack_depth N    # stack depth cap
viztracer --plugin perfetto      # use Perfetto exporter (default in v1+)
```

## Sources

- https://github.com/gaogaotiantian/viztracer — source
- https://viztracer.readthedocs.io/ — full docs
- https://ui.perfetto.dev/ — Perfetto UI (drag-drop the JSON)
- https://docs.python.org/3/library/asyncio-task.html — asyncio task model
- https://viztracer.readthedocs.io/en/latest/concurrency.html — concurrency tracing guide
