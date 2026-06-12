<!--
Source: https://github.com/benfred/py-spy
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# py-spy — CPU / Stack Sampling Profiler

`py-spy` (Ben Frederickson, Rust) is a low-overhead sampling profiler for
Python programs. It runs in a SEPARATE PROCESS and reads the target process's
memory — meaning ZERO code changes, no `@profile` decorators, no instrumentation
overhead, and the ability to attach to an already-running production process.

This is the 2026 default for CPU profiling and the agent's first reach when
"where is my Python program spending time?"

## When to use this skill

- "Where is time being spent?" — generates a flamegraph in seconds
- Attaching to a hung / slow production process WITHOUT restarting it
- Profiling a worker that you can't easily modify (Celery, gunicorn, RQ)
- Continuous low-overhead sampling in dev
- GIL contention diagnosis (`--idle` mode shows blocked threads)
- Multi-process / forking server profiling

Do NOT use py-spy for: memory leaks (use `memray`), line-by-line timing
(use `line_profiler` or `scalene`), or async-task contention (use `viztracer`).

## Setup

```bash
uv add --dev py-spy            # project-local
# OR ephemeral
uvx py-spy --version
```

Linux + macOS (full features). Windows (limited — `top` / `record` work, but
no `--native`). On Linux, requires `CAP_SYS_PTRACE` to attach to other
processes; in Docker, run with `--cap-add=SYS_PTRACE`.

## Common recipes

### Recipe 1 — Record a flamegraph (most common)

```bash
uvx py-spy record -o flame.svg -- python script.py
# Opens flame.svg in any browser
```

The SVG flamegraph: width = sampled time, top = leaf. Look for unexpectedly
wide leaves.

### Recipe 2 — Speedscope format (better UI than SVG)

```bash
uvx py-spy record -o flame.speedscope --format speedscope -- python script.py
# Open at https://www.speedscope.app/ (drag-drop, runs client-side)
```

Speedscope is interactive (search, hide frames, color by package). Strongly
preferred for any non-trivial investigation.

### Recipe 3 — Attach to a running process

```bash
# Find the PID
ps aux | grep python
# Record for 60s with no code change
uvx py-spy record -o flame.svg --pid 12345 --duration 60
```

This is py-spy's killer feature: zero-instrumentation production debugging.

### Recipe 4 — `top`-like live view

```bash
uvx py-spy top --pid 12345                   # live updating top, per-function
```

Shows current top hot functions sampled in real time. Press `?` for keys.
Useful for "is the GIL the problem?" and "what's this process doing?"

### Recipe 5 — Stack dump (for hung processes)

```bash
uvx py-spy dump --pid 12345
```

Prints the current stack of every Python thread. Equivalent to attaching gdb
+ `py-bt` but works without symbols. Most useful for "this process is hung —
where?"

### Recipe 6 — Async function profiling

```bash
uvx py-spy record -o flame.svg --native --idle -- python -m my_async_app
```

- `--idle` — include threads waiting on I/O (otherwise hidden as 0% CPU)
- `--native` — include C-extension stacks (asyncpg, orjson, etc.)
- For deeper asyncio timeline analysis, use `viztracer` (see
  `viztracer-asyncio-timeline` skill).

### Recipe 7 — Multi-process / forking server

```bash
# gunicorn / uvicorn workers
uvx py-spy record -o flame.svg --pid <master_pid> --subprocesses -- duration 60
```

`--subprocesses` follows fork()s, capturing all worker processes.

### Recipe 8 — CI gate / regression detection

py-spy doesn't ship a CI gate. Strategy: record before + after a change,
diff in speedscope, or extract sample counts via `--format raw` and diff
with `flamegraph.pl`.

### Recipe 9 — Profile pytest tests

```bash
uvx py-spy record -o flame.svg -- pytest tests/test_slow.py
```

Wraps any command, including the test runner. Combine with `pytest-xdist`
for parallel-aware sampling.

## Output interpretation

- **Flame width** — total time sampled at that stack. Wide = hot.
- **`<idle>`** — thread waiting on I/O / GIL. Add `--idle` to include.
- **C-extension functions** — visible only with `--native`. Otherwise show
  as `<external code>`.
- **GIL contention indicator** — multiple threads, but most show `<gil>`
  in their stacks → CPU-bound code holding the GIL. Solutions: move to
  C/cython/numpy, switch to multiprocessing, use `nogil` Python 3.13+.

Typical patterns:
- Wide leaf in `json.loads` → switch to `orjson` or `msgspec`.
- Wide leaf in `pydantic` validation → use `model_construct` for trusted.
- Wide leaf in `sqlalchemy` ORM iteration → N+1, use `selectinload`.
- Wide leaf in `re.compile` → hoist regex compilation out of the loop.
- Wide `<idle>` in async → check `await` chain for serial awaits where
  `asyncio.gather` would parallelize.

## CLI quick reference

```
py-spy record          # write flamegraph
py-spy top             # live top view
py-spy dump            # one-shot stack snapshot

  --pid <N>            # attach to PID
  --duration <S>       # how long to sample
  --rate <HZ>          # samples per second (default 100)
  --format <F>         # flamegraph | speedscope | raw
  --native             # include C-extension stacks
  --idle               # include sleeping threads
  --subprocesses       # follow forks
  --gil                # only count samples holding the GIL
  --threads            # include thread IDs
  --function           # collapse by function (no line numbers)
  --full-filenames     # absolute paths in frames
```

## Edge cases

- **Permissions (Linux)**: `CAP_SYS_PTRACE` required. `setcap
  cap_sys_ptrace=eip $(which py-spy)` for unprivileged use. In Docker, use
  `--cap-add=SYS_PTRACE --pid=host` to profile host processes.
- **Permissions (macOS)**: requires SIP off or codesign exception for some
  attach scenarios. Recording your own child process (`py-spy record -- python
  script.py`) works universally.
- **Permissions (Windows)**: works but no `--native` and no `attach` to
  non-child processes.
- **Stripped binaries**: native frames show as `???`. Install debug symbols
  (`apt install python3-dbg`).
- **PyPy / CPython unsupported builds**: py-spy targets CPython 3.6+. PyPy
  unsupported.
- **Sampling rate**: default 100 Hz is plenty for most. For very short scripts,
  bump to `--rate 500`. For long-running services, lower to `--rate 20` to
  reduce CPU overhead (still 5-15%).
- **Long flame**: open in speedscope, use search to focus, or use `--function`
  to collapse line numbers.
- **`<unknown>` frames**: usually from interpreter internals or sub-interpreters.
  Ignore unless they dominate.

## What py-spy replaces / complements

| Legacy tool | py-spy equivalent / relation |
|---|---|
| `cProfile` | py-spy: no code change, lower overhead, lives outside the process |
| `profile` | py-spy: same, but cProfile is C-based — py-spy is sampling (lower fidelity per-line, higher fidelity prod-safe) |
| `line_profiler @profile` | py-spy: doesn't do line-level; use `line_profiler` or `scalene` for that |
| `austin` | overlapping; py-spy has wider adoption + better UI |
| `viztracer` | complementary; viztracer for asyncio timelines, py-spy for sampling stacks |

`cProfile` remains useful when you want EXACT call counts (deterministic) or
need to integrate with `pstats`. For "where is time going?" — py-spy wins.

## Sources

- https://github.com/benfred/py-spy — source + README
- https://github.com/benfred/py-spy/blob/master/README.md — CLI reference
- https://www.speedscope.app/ — flamegraph UI
- https://github.com/jlfwong/speedscope — speedscope source
- https://www.brendangregg.com/flamegraphs.html — flamegraph theory
