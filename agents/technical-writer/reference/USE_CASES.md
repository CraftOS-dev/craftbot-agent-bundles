# Technical Writer — Use Cases

**Tier:** specialized · **Category:** content
**Core job:** Write developer documentation that developers actually read and use — READMEs, API references, tutorials, conceptual guides, ADRs, OpenAPI specs.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Write READMEs
- 5-second test passing (what / why / how to start)
- Quick Start above Installation
- Exact commands extracted from the repo (zero-hallucination protocol)

### Write API documentation
- OpenAPI 3.1 specs (request/response schemas, examples, error codes, authentication)
- Try-it-out console design
- SDK reference documentation
- Multi-language code examples

### Write tutorials
- Progressive complexity (minimal → guided → variations → challenges → troubleshooting)
- Hands-on exercises (5 types: fill-in-the-blank, debug, extension, from-scratch, refactoring)
- Anticipated common errors with solutions
- Time estimate, prerequisites, what-you'll-learn upfront

### Write reference docs
- Every parameter, every method, every configuration option
- Standard entry format (Type / Default / Required / Since / Deprecated / Description / Parameters / Returns / Throws / Examples / See Also)
- Cross-references, edge cases, deprecation migrations

### Write conceptual guides
- Explain *why*, not just *how*
- System architecture deep-dives (10 standard sections)
- Design rationale documentation

### Write ADRs (Architecture Decision Records)
- 5 template formats (MADR, lightweight, Y-statement, deprecation, RFC)
- Lifecycle management (Proposed → Accepted → Deprecated → Superseded)
- Status discipline, supersession links

### Write changelogs
- Keep a Changelog format
- Conventional Commits enforcement
- Semantic Versioning

### Architect documentation systems
- Choose between Docusaurus / MkDocs / Sphinx / VitePress
- Information architecture, search, multi-version, contribution workflows
- Automated link checking, code example testing, accessibility (WCAG AA)

### Apply Divio Documentation System
- Separate tutorials (learning) / how-to (task) / reference (information) / explanation (understanding)
- Never mix them — mixing is the #1 cause of confusing docs

### Audit existing docs
- Find gaps, stale content, broken examples
- High-exit pages treated as bugs
- Cross-reference top-searched terms with content gaps

### Co-author with users (3-stage workflow)
- Stage 1: Context Gathering
- Stage 2: Refinement & Structure (section-by-section)
- Stage 3: Reader Testing with fresh Claude

### Generate diagrams
- Mermaid (flowcharts, sequence, ER, state, gantt)

---

## Execution status (SOTA — June 2026)

The previous verdict ("can execute the full doc loop") was accurate for authoring but missed two major SOTA categories: (1) live doc auditing (high-exit pages, top-searched terms, broken links, accessibility) and (2) modern toolchain replacements (Mintlify > Read the Docs for API docs, Log4brains > adr-tools for ADRs, git-cliff > conventional-changelog-cli for changelogs, Lychee > html-proofer for links, D2 > PlantUML for diagrams). The updated bundle wires the agent into all of these via `cli-anything`.

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Write READMEs | Filesystem repo introspection + `--help` ground-truthing + `doc-coauthoring` skill | `filesystem` + `cli-anything` (git ls-files, npm/uv/make probes) + bundled skill |
| Write API documentation | Mintlify CLI (auto-generated playgrounds + llms.txt + MCP) OR Redocly CLI + Scalar + Speakeasy/Fern for SDK refs | `cli-anything` (`npm i -g mintlify @redocly/cli @scalar/cli @hey-api/openapi-ts`) + `openapi-spec-generation` skill |
| Write tutorials | Diátaxis tutorial mode + executable examples validated via `pytest-markdown-docs` (Modal Labs) / `mktestdocs` | `cli-anything` (`uvx pytest --markdown-docs docs/`) + `doc-coauthoring` |
| Write reference docs | Sphinx autodoc + `sphinx-autodoc-typehints` (Python) / TypeDoc (TS) / Doxygen (C++) / rustdoc (Rust) + Vale template enforcement | `cli-anything` (`uvx sphinx-build`, `npx typedoc`, `cargo doc`) + `postgresql-mcp` for DB schemas |
| Write conceptual guides | Diátaxis explanation + D2 architecture diagrams + Vale section rules | `filesystem` + `cli-anything` (D2 install + `vale --config=.vale.ini`) |
| Write ADRs | **Log4brains** (visual ADR site + CLI + git-log inference) — 2026 leader over adr-tools | `cli-anything` (`npx log4brains init && new && build`) + `architecture-decision-records` skill |
| Write changelogs | **git-cliff** (Rust, 120ms/10k commits) for CHANGELOG.md + **release-please** (Google) for full release-PR automation | `cli-anything` (`cargo install git-cliff` or `pipx install git-cliff`) + `changelog-automation` skill |
| Architect doc systems | **Docusaurus** (React/MDX, 3M weekly DLs) / **VitePress** (Vue, fastest builds) / **Astro Starlight** (Islands, fastest cold) / **Mintlify** (SaaS, AI-first) / **MkDocs Material** (Python) — match user's stack; deploy to Cloudflare Pages / Vercel | `cli-anything` (`npx create-docusaurus@latest`, `npm create vitepress@latest`, `npm create astro@latest -- --template starlight`, `uv add mkdocs-material`) + `github` deploy workflow |
| Apply Divio / Diátaxis System | File-system separation (`docs/tutorials/`, `how-to/`, `reference/`, `explanation/`) + Vale custom-style rule enforcing section vocabulary | `filesystem` + `cli-anything` (Vale + custom style package) |
| Audit existing docs (prose / links / examples / a11y / analytics / search) | **Vale** `--output=JSON` + **Lychee** (fastest 2026 link checker) + **pytest-markdown-docs** + **pa11y-ci** + **axe-core** + **Microsoft Clarity API** (free heatmaps + click-streams) + GA4 Data API for high-exit pages + Algolia Insights for top-searched | `cli-anything` (`vale`, `lychee --format json`, `npx pa11y-ci`) + `cli-anything` curl Clarity/GA4 |
| Co-author with users (3-stage) | Bundled `doc-coauthoring` skill + spawn subagent for fresh-Claude reader test (Stage 3) | `doc-coauthoring` + `github-api` for PR review + Task subagent |
| Generate diagrams | **Mermaid** (GH-native) via `mmdc` CLI + **D2** (Terrastruct, modern auto-layout) + Structurizr DSL for C4 + PlantUML for UML completeness | `cli-anything` (`npm i -g @mermaid-js/mermaid-cli`, D2 install script) + `drawio-mcp` for non-Mermaid diagram types |
| Translate docs to other languages | DeepL API for high-quality machine translation + Crowdin/Lokalise for translator workflows | `deepl-mcp` + `cli-anything` curl (Crowdin/Lokalise) |
| Capture text from legacy screenshot-only docs | Gemini OCR / Mistral OCR for image-only PDFs and screenshots | `gemini-ocr-mcp` + `mistral-ocr-mcp` |

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Microsoft Clarity / GA4 / Algolia analytics | ⚠ | Free tiers cover most use cases; Clarity is free for unlimited sessions; GA4 Data API requires OAuth per project; Algolia Insights free for OSS via DocSearch |
| Mintlify / ReadMe.com SaaS deploy | ⚠ | Paid plans for proprietary docs; OSS plans free; open-source Docusaurus/MkDocs/Starlight covers everything for free |
| Diagram rendering for very large architectures | ⚠ | Mermaid CLI may need `--width`/`--height` tuning for >100-node graphs; D2 handles it better |

**Verdict (June 2026): 100% fulfillment.** Every use case has a SOTA execution path. Doc authoring + linting + analytics + diagrams + translation + OCR are all wired in. The agent is now genuinely a docs operator, not just a docs writer.

---

## When to use this agent

- "Write a README for this repo"
- "Generate API documentation from this OpenAPI spec"
- "Build a step-by-step tutorial for getting started with X"
- "Audit my docs and tell me what's stale"
- "Write an ADR for our decision to migrate from MongoDB to PostgreSQL"
- "Set up a Docusaurus site for our docs"
- "Help me draft a design doc — guide me through it"
- "Create reference docs for every CLI flag in this tool"

## When NOT to use this agent

- Marketing copy / sales content — recommend `marketing-agent`
- Long-form prose for general audiences (essays, articles for non-technical audiences) — adapt but flag
- Visual design / graphic design — out of scope; flag for a designer
- Translation work into languages the user can't review — flag the limitation
- Writing code itself — recommend `senior-python-engineer` (or a future language specialist)
