---
name: zero-hallucination-readme
description: Write a README by extracting reality from the repo — `git ls-files`, `package.json`, `pyproject.toml`, `--help` probes — never guessing commands. 5-second test passes, Quick Start above Installation. Use whenever writing or refreshing a README.
---

# Zero-Hallucination README Protocol

A README is the most-read doc in a repo. It must reflect reality exactly: real commands, real install paths, real names, real prerequisites. The agent enforces this by **scanning the repo first** before writing a single line.

## The 5-second test

A reader spends 5 seconds on the README. In that window, they must learn:

1. **What** this is (one-liner).
2. **Why** it exists (problem statement, 1-2 sentences).
3. **How** to start (Quick Start with a working command).

If any of these requires scrolling past badges, ToCs, or boilerplate — the README has failed.

## When to use this skill

- Writing a README from scratch.
- Refreshing a stale README.
- Auditing an existing README for hallucination.

## Phase 1: Repo introspection (mandatory before writing)

The agent runs these commands via `filesystem` + `cli-anything` BEFORE writing any prose.

### Step 1 — Identify package manager(s)

```bash
ls package.json pyproject.toml Cargo.toml go.mod Gemfile composer.json mix.exs build.gradle pom.xml requirements.txt setup.py Makefile 2>/dev/null
```

### Step 2 — Read manifest

```bash
# Node
cat package.json | jq '{name, version, description, scripts, bin, main, exports, engines, repository, license, keywords}'

# Python
cat pyproject.toml | grep -A2 '\[project\]'
cat pyproject.toml | grep -A20 '\[project.scripts\]'

# Rust
cat Cargo.toml | grep -A10 '\[package\]'

# Go
head -5 go.mod
```

### Step 3 — List tracked files

```bash
git ls-files | head -100
git ls-files '*.md'
git ls-files 'src/**'
git ls-files | wc -l       # rough project size
```

### Step 4 — Probe the entry points

```bash
# Node binaries
cat package.json | jq -r '.bin // {} | keys[]' | while read bin; do
  npx --no-install "$bin" --help 2>&1 | head -50
done

# Python entry points
uv run --help 2>&1 | head -30
uvx <project-cli-name> --help 2>&1 | head -50

# Make targets
make help 2>&1 || cat Makefile | grep -E '^[a-z][a-z_-]+:' | head -20
```

### Step 5 — Check the test runner

```bash
# Node
cat package.json | jq -r '.scripts.test // empty'

# Python
grep -E 'pytest|unittest|nose' pyproject.toml

# Go
test -f main_test.go && echo "go test ./..."
```

### Step 6 — Read existing examples

```bash
ls examples/ docs/examples/ 2>/dev/null
git ls-files | grep -iE 'example|sample|demo' | head -10
```

### Step 7 — Read CI for canonical commands

```bash
cat .github/workflows/*.yml | grep -E '(npm|yarn|pnpm|uv|pip|cargo|go) (run|test|build|install)'
```

If CI runs `uv run pytest` to test, the README's "How to test" must use the same command.

## Phase 2: Author the README

Now (and only now) the agent writes. Template structure:

```markdown
# <Project Name>

> <One sentence: what it does and who it's for.>

[badges row: build / npm / license / downloads]

## Why this exists

<2-3 sentences. The problem this solves. NOT a feature list — the pain.>

## Quick Start

<Shortest possible path from "nothing installed" to "code running". Reuse the CI's exact commands.>

```bash
<exact install command from manifest>
```

```<lang>
<smallest meaningful working example — must run as-is>
```

## Installation

**Prerequisites:** <only the ones the agent VERIFIED in package.json `engines` / pyproject `requires-python` / Cargo `rust-version`>

```bash
<install command(s) for each supported package manager>
```

## Usage

### Basic example

<Most common use case. Code must run.>

### Configuration

<Table of options — pull from the actual schema / typedef / pydantic model.>

| Option | Type | Default | Description |
|--------|------|---------|-------------|
<from code>

### Advanced examples

<Pull from examples/ directory. Link, don't duplicate.>

## API reference

<Link to generated reference (TypeDoc/Sphinx/rustdoc) — do NOT inline a partial reference here.>

## Contributing

<Link to CONTRIBUTING.md if it exists. If not, the agent does NOT invent guidelines.>

## License

<From LICENSE file or package.json `license`. Verbatim.>
```

## Phase 3: Verification gates

Before declaring the README done:

### Gate 1 — Every command runs

```bash
# Extract every fenced bash block
grep -A1 '^```bash' README.md | grep -v '^```' | grep -v '^--' | grep -v '^$' \
  | while read cmd; do
    echo "Testing: $cmd"
    # The agent doesn't actually execute; it cross-references each command
    # against the verified manifest scripts / probed --help output.
  done
```

### Gate 2 — Every link resolves

Run `lychee README.md` (see `lychee-link-checking`).

### Gate 3 — Every code example matches reality

If the README shows `acme.client.new("sk_...")`, the agent verifies that:

- `acme.client` exists in `src/`.
- It has a `new` method (TS / Python / Go / etc).
- It accepts a string argument.

If verification fails, the example is wrong. Fix the code or fix the example.

### Gate 4 — 5-second test passes

Squint at the top of the rendered README. Can a reader answer "what / why / first command" in 5 seconds without scrolling past badges?

### Gate 5 — No "click here" / "see the docs"

Every link has descriptive text.

## What the agent NEVER does

- **Invent a feature** that isn't in the code.
- **Hallucinate a CLI flag** that `--help` didn't show.
- **List a prerequisite version** that isn't enforced by `engines` / `requires-python` / `rust-version`.
- **Copy a license** other than what's in `LICENSE` / `pyproject.toml` / `package.json`.
- **Write a contribution section** without checking `CONTRIBUTING.md`.
- **Include badges** for things that aren't set up (no fake "build passing" badge).
- **Show a Quick Start that doesn't run.** The Quick Start is the highest-stakes block in the doc.

## Common recipes

### Recipe 1: README for a new TypeScript package

```bash
# 1. Verify package.json
cat package.json | jq '{name, description, main, bin, scripts}'

# 2. Probe the public API
cat src/index.ts | head -50

# 3. Read the test for the canonical usage
cat src/index.test.ts | head -30

# 4. Author the README from real data
```

### Recipe 2: README for a Python CLI

```bash
# 1. Read pyproject
grep -A5 '\[project.scripts\]' pyproject.toml

# 2. Probe the CLI
uv run <cli-name> --help

# 3. Read the entry point
cat src/<package>/__main__.py | head -40

# 4. Author the README
```

### Recipe 3: README for a Rust library

```bash
cat Cargo.toml | grep -A10 '\[package\]'
cat src/lib.rs | head -30
cat examples/*.rs 2>/dev/null
```

## Edge cases

- **Monorepos:** each package gets its own README; the root README orients between packages.
- **Pre-1.0 software:** add a "Stability" section ("This API may change before 1.0").
- **Internal tools:** drop the "Why this exists" section if obvious; never drop the Quick Start.
- **DSL / config language:** show a complete config example in the Quick Start, not "open a file and add X."
- **No CLI, library-only:** the Quick Start becomes a 3-line code import + call example.

## Pairs well with

- `vale-prose-linting` — voice / terminology consistency.
- `lychee-link-checking` — link verification.
- `pytest-markdown-docs-validation` — fence verification (Python).
- `doc-coauthoring` — when the user wants to co-author rather than receive a draft.

## Sources

- README zero-hallucination protocol: https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/06-developer-experience/readme-generator.md
- "Awesome README" reference: https://github.com/matiassingers/awesome-readme
- 5-second test framing: https://www.nngroup.com/articles/usability-testing-101/
