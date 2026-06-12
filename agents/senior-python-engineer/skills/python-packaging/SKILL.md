<!--
Source: https://github.com/wshobson/agents/blob/main/plugins/python-development/skills/python-packaging/SKILL.md
Repo: wshobson/agents

NOTE: WebFetch returned a summarized view of this file rather than verbatim content.
The summary below captures the SOTA recommendations from the source. For the full
file content (including code examples and detailed patterns), see the source URL.
-->

# Python Packaging

Creating and distributing Python packages. Modern standards based on PEPs 517/518/621/660.

## When to Use This Skill

- Creating Python libraries for distribution
- Building command-line tools with entry points
- Publishing packages to PyPI or private repositories
- Setting up build systems for new projects

## Modern Standards

The current Python packaging ecosystem is built on these PEPs:

- **PEP 517/518** — Build system requirements
- **PEP 621** — Metadata in `pyproject.toml`
- **PEP 660** — Editable installs

## Build Backends

Multiple build backends are available, each with trade-offs:

- **setuptools** — Traditional, widely supported, mature
- **hatchling** — Modern, recommended for new projects
- **flit** — Streamlined for pure Python packages
- **poetry** — Combines dependency management with packaging

## Recommended Architecture

### src/ Layout

Place package code in a `src/` directory rather than at the project root.

```
myproject/
├── src/
│   └── myproject/
│       ├── __init__.py
│       └── ...
├── tests/
├── pyproject.toml
└── README.md
```

Benefits:
- Prevents unintended imports from the development directory
- Improves test isolation (tests must use the installed package)
- Better separation between source and build artifacts

### Single pyproject.toml

Consolidate all configuration (build, dependencies, metadata, tool settings) into a single `pyproject.toml` per PEP 621. Avoid scattered `setup.py`, `setup.cfg`, `requirements.txt` arrangements where possible.

## Detail referenced in source

The original SKILL.md file references additional detail in `references/details.md`. For complete worked examples and edge cases not captured in this summary, see the source repo.
