<!--
Source: https://github.com/wshobson/agents/blob/main/plugins/python-development/skills/python-performance-optimization/SKILL.md
Repo: wshobson/agents

NOTE: WebFetch refused to return verbatim content of this file across multiple
attempts. The summary below captures the SOTA recommendations from the source as
returned by WebFetch. For the full file content (including code examples and
profiling commands), see the source URL.
-->

# Python Performance Optimization

Systematic profiling and optimization techniques for identifying and resolving performance issues in Python applications.

## Key Focus Areas

**Profile before optimizing.** Developers should measure actual bottlenecks rather than making assumptions about where slowdowns occur.

Four main profiling approaches:

1. **CPU profiling** — `cProfile`, `py-spy` (sampling), flame graphs
2. **Memory tracking** — `memory_profiler`, `tracemalloc`
3. **Line-level analysis** — `line_profiler`
4. **Call graph visualization** — produced from profiler output

## Primary Optimization Strategies

In rough priority order:

- **Algorithmic improvements** — better data structure selection, complexity reduction
- **More efficient coding patterns** — built-in functions (implemented in C), `lru_cache`, generators
- **Parallel execution** — threading (I/O-bound) or multiprocessing (CPU-bound)
- **Result caching** — eliminate redundant calculations (functools.lru_cache, external Redis)
- **Native code extensions** — Cython, Numba for performance-critical sections
- **NumPy vectorization** — for numerical work, replace Python loops with vector ops

## Practical Recommendations

- Use built-in functions over hand-rolled equivalents — they're C-implemented and faster
- Use `lru_cache` decorators for memoization of pure functions
- Use generators for large datasets to avoid materializing the full sequence
- Use NumPy for numerical work
- Monitor production systems directly with `py-spy` rather than relying solely on development-time measurements

## Common Mistakes to Avoid

- Optimizing without profiling data
- Creating unnecessary data copies
- Selecting inappropriate data structures
- Overlooking algorithmic complexity (O(n²) where O(n log n) was possible)

## Detail referenced in source

The original SKILL.md file references additional detail in `references/details.md`. For complete profiling commands, code samples, and worked optimization examples, see the source repo.
