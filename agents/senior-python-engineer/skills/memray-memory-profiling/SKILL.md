<!--
Source: https://github.com/bloomberg/memray · https://bloomberg.github.io/memray/
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# memray — Memory Profiling (Replaces memory_profiler)

`memray` (Bloomberg, 2022+) is a memory profiler for Python that tracks ALL
allocations — including native C-extension allocations via `LD_PRELOAD` — and
produces interactive flamegraphs, summary tables, and live-mode console views.
It is the 2026 SOTA replacement for `memory_profiler` (which only sees Python
allocations and uses heavy line-by-line instrumentation).

## When to use this skill

- "Memory keeps growing" investigations (leaks, retained references)
- Profiling NumPy / PyTorch / pandas pipelines where C-ext allocs dominate
- Comparing memory before/after a refactor
- Hunting allocation hotspots in import time or hot loops
- Production-style diagnosis without code changes
- Replacing legacy `memory_profiler` and `@profile` decorators

Do NOT use memray for: latency profiling (use `py-spy`/`pyinstrument`),
allocation count alone for short scripts (`tracemalloc` is fine), or
production continuous profiling (use Sentry Profiling/Pyroscope).

## Setup

```bash
uv add --dev memray            # project-local for fixtures
# OR ephemeral
uvx memray run script.py
```

Linux + macOS only. On Windows use WSL2.

## Common recipes

### Recipe 1 — Record + flamegraph

```bash
uvx memray run -o capture.bin python script.py
uvx memray flamegraph capture.bin           # writes memray-flamegraph-capture.html
open memray-flamegraph-capture.html         # browser, interactive
```

The flamegraph shows allocation by stack — width = bytes allocated, NOT
calls.

### Recipe 2 — Track native allocations (the killer feature)

```bash
uvx memray run --native -o capture.bin python script.py
uvx memray flamegraph capture.bin
```

`--native` uses `LD_PRELOAD` to capture `malloc`/`free` from C extensions
(NumPy, pandas, Torch, scikit-learn, asyncpg). This is the unique advantage
over `tracemalloc` / `memory_profiler`.

### Recipe 3 — Live mode (TUI)

```bash
uvx memray run --live python script.py      # opens curses-style TUI
```

The TUI shows top allocators in real time, sortable by allocation count,
total bytes, or own bytes. Press `O` to switch, `Q` to quit. Perfect for
"is this loop leaking?" reality checks.

### Recipe 4 — Report flavors

```bash
uvx memray flamegraph capture.bin           # interactive HTML
uvx memray tree capture.bin                 # ASCII call tree
uvx memray summary capture.bin              # top-10 table
uvx memray stats capture.bin                # high-level stats
uvx memray transform table capture.bin      # all allocations as CSV
```

### Recipe 5 — Leak mode

```bash
uvx memray run --trace-python-allocators --leaks -o capture.bin python script.py
uvx memray flamegraph --leaks capture.bin
```

`--leaks` mode reports only memory ALLOCATED but never FREED by the end of
the recording. Crucial for long-running services and import-time leaks.

### Recipe 6 — Allocator tracking

```bash
uvx memray run --trace-python-allocators -o capture.bin python script.py
```

Captures Python's small-object allocator (pool) calls — useful when you
suspect `bytes`/`str` churn but the flamegraph shows nothing in C.

### Recipe 7 — pytest integration

```bash
uv add --dev pytest-memray
```

```python
# tests/test_memory.py
import pytest

@pytest.mark.limit_memory("100 MB")
def test_pipeline_uses_under_100mb():
    run_pipeline(big_input)
```

```bash
uv run pytest --memray tests/
```

Generates a memray report per test + fails any test exceeding the declared
budget. Great regression gate.

### Recipe 8 — Long-running service / web app

```bash
# Inside a docker exec or systemd-run wrapper
memray run --output /tmp/cap.bin -- gunicorn app:asgi --workers=4
# Send traffic for a minute, then Ctrl-C
memray flamegraph /tmp/cap.bin
```

For a daemon you can't restart, use `memray attach <PID>` (Linux,
requires CAP_SYS_PTRACE). For continuous production memory profiling, use
Sentry Profiling or Pyroscope instead.

### Recipe 9 — Diff two captures (regression hunt)

```bash
uvx memray run -o before.bin python script.py
# apply change
uvx memray run -o after.bin python script.py
uvx memray flamegraph --temporal before.bin
uvx memray flamegraph --temporal after.bin
# Visually compare. (No built-in diff; export tables and diff in pandas.)
```

## Output interpretation

In the flamegraph:
- **X-axis** — allocations grouped by stack frame (alphabetical by default).
- **Y-axis** — call depth (top = leaf where allocation happened).
- **Width** — TOTAL bytes allocated through that frame. Look for unexpectedly
  wide frames.
- **Color** — random by default; the "diff" mode colors regressions red.

Common patterns:
- Wide frame inside `pandas` / `numpy` / `torch` → unavoidable; look for
  redundant copies upstream.
- Wide frame inside `json.loads` / `pickle.loads` → consider `orjson` /
  `msgspec`.
- Wide frame inside `str.format` / f-strings → look for string churn loops.
- Wide frame inside `pydantic` `__init__` → consider `model_construct` for
  trusted inputs (skips validation).

## Edge cases

- **Windows**: not supported natively. Use WSL2.
- **Multi-process**: pass `--follow-fork` to track child processes.
- **gevent / eventlet**: monkey-patched event loops can confuse stack capture;
  prefer `--native` mode.
- **Threading**: memray captures per-thread; flamegraph aggregates by stack.
- **`__pycache__`**: byte-compiled files don't affect memray.
- **Capture file size**: large captures (GB) can occur. Use `--aggregate`
  or shorter recording windows.
- **Permissions for `attach`**: Linux requires `CAP_SYS_PTRACE` or root;
  inside containers, set `--cap-add=SYS_PTRACE`.
- **Native libs without symbols**: stripped binaries show as `???`. Install
  debug symbols (`apt install python3-dbg`) for better stacks.

## What memray replaces

| Legacy tool | memray equivalent |
|---|---|
| `mprof run script.py && mprof plot` | `uvx memray run -o cap.bin script.py && uvx memray flamegraph cap.bin` |
| `@profile` decorator (memory_profiler) | none needed — memray works without code changes |
| `tracemalloc.start() ... take_snapshot()` | `uvx memray run --trace-python-allocators` |
| `objgraph.show_growth()` | `uvx memray run --live` |
| `pympler.muppy.get_objects()` | `uvx memray summary cap.bin` |

`tracemalloc` is still fine for stdlib-only contexts (no third-party install
allowed) but memray's `--native` mode is strictly more powerful when allowed.

## Sources

- https://github.com/bloomberg/memray — source + README
- https://bloomberg.github.io/memray/ — full docs
- https://bloomberg.github.io/memray/flamegraph.html — flamegraph reading guide
- https://bloomberg.github.io/memray/native_mode.html — native mode internals
- https://github.com/bloomberg/pytest-memray — pytest plugin
- PyCon 2022 talk: https://www.youtube.com/watch?v=4hjueHpcVUM
