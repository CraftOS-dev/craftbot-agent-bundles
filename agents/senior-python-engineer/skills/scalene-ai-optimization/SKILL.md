<!--
Source: https://github.com/plasma-umass/scalene
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# scalene — Unified CPU + GPU + Memory Profiler with AI Suggestions

`scalene` (Plasma Group, UMass) is a high-performance, AI-augmented Python
profiler. Unique among profilers: it measures CPU, GPU, AND memory in a single
run AND offers AI-generated optimization suggestions for hot lines, powered
by an LLM that reads the profile + code context.

## When to use this skill

- One-shot full-picture profile (CPU + memory + GPU) without three tools
- AI-assisted optimization suggestions for a specific hot line/function
- Distinguishing native vs Python time (scalene splits this natively)
- GPU work profiling (PyTorch / JAX / cupy)
- Comparing per-line CPU + memory side by side
- "What's the fastest way to speed this up?" exploration

Do NOT use scalene for: deep production attach (use `py-spy`), low-overhead
long-running services (use Pyroscope), or asyncio timeline (use `viztracer`).
The AI suggestions are best-effort — VERIFY before applying.

## Setup

```bash
uv add --dev scalene            # project-local
# OR ephemeral
uvx scalene script.py
```

Linux + macOS + Windows. AI suggestions require an OpenAI/Anthropic/local LLM
key (configured via `SCALENE_AI` env var or `~/.config/scalene/ai.json`).

## Common recipes

### Recipe 1 — Web UI (default)

```bash
uvx scalene script.py
# Auto-opens http://localhost:<port> with the profile
```

The web UI shows per-line CPU%, memory MB, GPU%, with code on the left and
a column called "AI" — click it to ask for optimization suggestions.

### Recipe 2 — HTML report (CI / share)

```bash
uvx scalene --html --outfile profile.html script.py
```

Single self-contained HTML file. Useful for PR comments, sharing with
non-Python teammates, or archiving baselines.

### Recipe 3 — CLI text output (CI gate)

```bash
uvx scalene --cli script.py
```

Plain text per-line breakdown. Pipe to a file for diffing in CI.

### Recipe 4 — Reduced profile (focus on hot lines only)

```bash
uvx scalene --reduced-profile script.py
```

Shows only lines exceeding 1% CPU or 100 KB allocation. The "AI" column is
much more useful in reduced mode — the LLM sees fewer noisy lines and gives
more targeted suggestions.

### Recipe 5 — Profile a long-running service

```bash
uvx scalene --pid 12345 --duration 30
```

Attach to a running process (Linux/macOS), sample for 30s. Less proven than
py-spy attach but works for ad-hoc inspection.

### Recipe 6 — GPU profiling

```bash
uvx scalene --gpu script.py
```

Captures NVIDIA GPU utilisation per Python line. Requires `nvidia-smi`
available. Useful for PyTorch / JAX hot paths.

### Recipe 7 — Memory-only mode

```bash
uvx scalene --memory script.py
```

Drops CPU sampling — lower overhead, focus on allocator activity. Less
powerful than `memray --native` but adds AI suggestions on top.

### Recipe 8 — Jupyter integration

```python
%load_ext scalene
%scrun --reduced-profile my_function()
```

Renders an inline scalene report in the notebook. Great for exploratory ML
work.

### Recipe 9 — AI optimization workflow

1. Run `uvx scalene --reduced-profile script.py`.
2. Open the web UI, find the line with the highest CPU% or memory.
3. Click the AI lightning bolt in that row.
4. Scalene sends the function + profile data to the LLM.
5. The LLM returns 2-3 candidate rewrites (e.g., "replace pandas iterrows
   with itertuples", "use numpy.dot instead of @").
6. Apply ONE candidate, re-run scalene, verify the change is measurable.

### Recipe 10 — Configure the AI backend

```bash
# ~/.config/scalene/ai.json
{
  "service": "openai",          # or "anthropic", "local"
  "model": "gpt-5",
  "api_key_env": "OPENAI_API_KEY"
}
```

For local-only environments, point at an Ollama-served LLM. No key leakage,
but suggestion quality varies.

## Output interpretation

Columns in scalene's web UI:
- **CPU% (Python)** — time the line spent in pure Python code.
- **CPU% (native)** — time spent in C extensions called from this line.
- **CPU% (system)** — time spent in syscalls / waiting.
- **Memory (MB)** — net allocation attributable to this line.
- **GPU%** — only with `--gpu` and CUDA available.
- **AI** — clickable; queries the LLM for suggestions.

The CPU split is unique. A line that's 80% "native" means optimising the
Python around it won't help — the C call is the bottleneck. A line that's
80% "Python" is where micro-optimisations matter.

Typical patterns:
- High Python% + high memory on a pandas `.apply` → vectorize with
  `numpy`/`pyarrow` operations.
- High native% in `json.loads` → switch to `orjson`/`msgspec`.
- High system% → I/O-bound; consider async or batching.
- High GPU% with mostly Python% → kernel launch overhead; batch operations
  or use `torch.compile`.

## Edge cases

- **AI hallucination**: scalene's AI suggestions can recommend wrong rewrites.
  ALWAYS benchmark the suggested change. Treat suggestions as one expert
  opinion, not a verdict.
- **Multiprocessing**: pass `--cli` and run scalene wrapping the master; child
  processes don't auto-instrument (limitation vs py-spy).
- **Cython / extensions**: scalene sees them as native, can't break inside.
  Use `py-spy --native` if you need C stacks.
- **Short scripts (<1s)**: not enough samples; bump `--cpu-sampling-rate`
  higher.
- **Large reports**: use `--reduced-profile` to focus on >1% lines.
- **Profiling cost**: scalene runs the code inside its instrumented profiler.
  Overhead is typically 10-30% — fine for dev, not for prod.
- **Windows GPU**: NVIDIA GPU profiling works; AMD/Intel GPU support is
  experimental.

## Comparison

| Need | Best tool | Why |
|---|---|---|
| Production stack sampling | `py-spy` | lowest overhead, attach to PID |
| Memory leak hunt | `memray --native` | unmatched native-alloc tracking |
| Asyncio task timeline | `viztracer` | Perfetto timeline |
| Narrative call tree | `pyinstrument` | most readable text output |
| Unified CPU + memory + GPU | **`scalene`** | only tool that does all three |
| AI-guided rewrites | **`scalene`** | unique LLM integration |
| Deterministic call counts | `cProfile` | true call counts, exact |

In practice: run `py-spy record` first for the 80/20 view, then run `scalene
--reduced-profile` for the AI hints and memory-correlation on the same hot
spots.

## Sources

- https://github.com/plasma-umass/scalene — source + README
- https://github.com/plasma-umass/scalene#using-scalene — full CLI reference
- https://www.youtube.com/watch?v=5iEf-_7mM1k — PyCon 2022 talk
- https://plasma-umass.org/ — research group
- Olin Liu, Sam Stern, Emery Berger papers on scalene's AI feature
