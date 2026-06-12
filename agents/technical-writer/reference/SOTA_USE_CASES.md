# Technical Writer — SOTA Use Case Map (June 2026)

Per-use-case mapping from agent capability to concrete SOTA mechanism. Each row names the tool, the agent's execution path (which CraftBot MCP/skill actually runs it), the canonical source, and a confidence verdict.

Legend:
- `✓` — agent can execute the SOTA path end-to-end today with shipped MCPs/skills.
- `⚠` — agent can execute the SOTA path but with a known caveat (auth scope, paid tier, env dep).
- `✗` — SOTA path requires a tool the agent cannot reach (deferred / future work).

Bundled skill packs (in `skills/`) referenced below:
`mintlify-api-docs`, `redocly-openapi-pipeline`, `openapi-sdk-generation`, `log4brains-adr-management`, `git-cliff-changelog`, `release-please-automation`, `lychee-link-checking`, `vale-prose-linting`, `pytest-markdown-docs-validation`, `pa11y-axe-accessibility-audit`, `microsoft-clarity-doc-analytics`, `ga4-doc-analytics`, `sphinx-typedoc-reference-docs`, `docusaurus-vitepress-starlight-mkdocs`, `d2-mermaid-diagrams`, `diataxis-divio-system`, `deepl-translation-i18n`, `zero-hallucination-readme`, `algolia-doc-search`.

---

## Write READMEs
- **SOTA approach:** Repo introspection (filesystem + `git ls-files`) → command ground-truthing (`--help` probes) → 5-second-test layout (What / Why / Quick Start above Installation). Never hallucinate flags, install paths, or runtime requirements.
- **Agent execution path:** `filesystem` MCP reads the workspace; `cli-anything` runs `git ls-files`, `npm pkg get scripts`, `uv run --help`, `make help`, `<binary> --help`. Authoring follows `skills/zero-hallucination-readme` + `skills/doc-coauthoring`.
- **Source:** https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/06-developer-experience/readme-generator.md
- **Confidence:** ✓

## Write API docs
- **SOTA approach:** Mintlify CLI (auto-generated playgrounds + llms.txt + MCP integration) for AI-first docs OR Redocly CLI lint+bundle+build with Scalar/ReDoc rendering for self-hosted. OpenAPI 3.1 with JSON Schema draft 2020-12.
- **Agent execution path:** `cli-anything` (`npm i -g mintlify @redocly/cli @scalar/cli` then `mint dev`, `mint deploy`, `redocly lint`, `redocly bundle`, `redocly build-docs`). Bundled skills: `mintlify-api-docs`, `redocly-openapi-pipeline`, `openapi-spec-generation`.
- **Source:** https://www.mintlify.com/library/best-api-docs-and-sdk-generation-tools + https://github.com/Redocly/redocly-cli
- **Confidence:** ✓

## Write tutorials
- **SOTA approach:** Diátaxis "tutorial" mode (learning-oriented, hands-on, guaranteed success) with all code fences validated via `pytest-markdown-docs` (Modal Labs) or `mktestdocs`. Five exercise types (fill-in / debug / extension / from-scratch / refactor).
- **Agent execution path:** `cli-anything` (`uv add --dev pytest pytest-markdown-docs && pytest --markdown-docs docs/`). Bundled skills: `pytest-markdown-docs-validation`, `diataxis-divio-system`, `doc-coauthoring`.
- **Source:** https://github.com/modal-labs/pytest-markdown-docs + https://diataxis.fr/tutorials/
- **Confidence:** ✓

## Write reference docs
- **SOTA approach:** Auto-generate from source so the spec is always live: Sphinx + `sphinx-autodoc-typehints` (Python), TypeDoc (TypeScript), Doxygen (C/C++), `cargo doc`/rustdoc (Rust). Enforce the standard entry format (Type/Default/Required/Since/Deprecated/Description/Parameters/Returns/Throws/Examples/See Also) via Vale.
- **Agent execution path:** `cli-anything` (`uvx sphinx-build -b html docs/ _build/`, `npx typedoc`, `doxygen`, `cargo doc`). Schema-driven DB references go through `postgresql-mcp`. Bundled skill: `sphinx-typedoc-reference-docs`.
- **Source:** https://www.sphinx-doc.org/ + https://typedoc.org/
- **Confidence:** ✓

## Write conceptual guides
- **SOTA approach:** Diátaxis "explanation" mode (understanding-oriented, makes sense of the topic). Pair with D2 architecture diagrams and Vale section-vocabulary rules so the explanation stays explanatory (no embedded step-by-steps).
- **Agent execution path:** `filesystem` for source reads; `cli-anything` to install D2 (`curl -fsSL https://d2lang.com/install.sh | sh`) and Vale (`brew install vale` or release tarball). Bundled skills: `d2-mermaid-diagrams`, `diataxis-divio-system`, `vale-prose-linting`.
- **Source:** https://diataxis.fr/explanation/ + https://d2lang.com/
- **Confidence:** ✓

## Write ADRs
- **SOTA approach:** Log4brains for the full ADR lifecycle — visual site, CLI, git-log metadata inference (`npx log4brains init docs/adr` → `log4brains new` → `log4brains build`). Use MADR 4.0 markdown template with Y-statement variants. adr-kit (kschlt) for MADR validation + indexing + enforcement when running in CI. adr-tools (npryce) as the legacy fallback.
- **Agent execution path:** `cli-anything` (`npx log4brains@latest init docs/adr`, `npx log4brains new "Decision title"`, `npx log4brains build`; `pipx install adr-kit` then `adr-kit validate`). Bundled skill: `log4brains-adr-management` + existing `architecture-decision-records`.
- **Source:** https://github.com/thomvaill/log4brains + https://adr.github.io/madr/ + https://github.com/kschlt/adr-kit
- **Confidence:** ✓

## Write changelogs
- **SOTA approach:** git-cliff (Rust, 120ms / 10k commits, no Node dependency) for CHANGELOG.md from Conventional Commits. release-please (Google) for full release-PR automation (auto-PR with SemVer bump + CHANGELOG diff + tag on merge). Keep a Changelog as the canonical output format.
- **Agent execution path:** `cli-anything` (`pipx install git-cliff` or `cargo install git-cliff`; then `git-cliff -o CHANGELOG.md`). For release-please: `github` MCP writes `.github/workflows/release-please.yml` invoking `googleapis/release-please-action@v4`. Bundled skills: `git-cliff-changelog`, `release-please-automation` + existing `changelog-automation`.
- **Source:** https://github.com/orhun/git-cliff + https://github.com/googleapis/release-please
- **Confidence:** ✓

## Architect doc systems
- **SOTA approach:** Pick by stack — Docusaurus (React/MDX, 3M weekly DLs, best versioning), VitePress (Vue, fastest builds), Astro Starlight (Islands architecture, fastest cold builds), MkDocs Material (Python, simplest config), Mintlify (SaaS, AI-first, hosted). Deploy to Cloudflare Pages / Vercel / GitHub Pages depending on org infra.
- **Agent execution path:** `cli-anything` for every scaffolder (`npx create-docusaurus@latest`, `npm create vitepress@latest`, `npm create astro@latest -- --template starlight`, `uv add mkdocs-material && mkdocs new .`). `github` MCP writes the deploy workflow. Bundled skill: `docusaurus-vitepress-starlight-mkdocs`.
- **Source:** https://docusaurus.io/ + https://vitepress.dev/ + https://starlight.astro.build/ + https://squidfunk.github.io/mkdocs-material/
- **Confidence:** ✓

## Apply Divio / Diátaxis
- **SOTA approach:** File-system separation (`docs/tutorials/`, `docs/how-to/`, `docs/reference/`, `docs/explanation/`) + Vale custom-style rule enforcing section vocabulary (no "you'll learn" in reference; no "as you'll recall" in tutorial) + sidebar mapping in Docusaurus/Starlight.
- **Agent execution path:** `filesystem` to scaffold the four directories; `cli-anything` to install Vale and write `.vale.ini` + `.vale/styles/Diataxis/` rules. Bundled skill: `diataxis-divio-system` + `vale-prose-linting`.
- **Source:** https://diataxis.fr/ + https://vale.sh/docs/topics/styles/
- **Confidence:** ✓

## Audit existing docs
- **SOTA approach:** Multi-tool gate — Vale `--output=JSON` (prose), Lychee (links, fastest 2026), markdownlint-cli2 (structure), alex (insensitive language), pytest-markdown-docs (code-fence execution), pa11y-ci + axe-core (WCAG 2.2 AA), Microsoft Clarity MCP (free behavioral analytics + heatmaps), GA4 Data API (high-exit pages / scroll depth / engagement), Algolia DocSearch Insights API (top-searched terms vs content gaps).
- **Agent execution path:** `cli-anything` runs every linter and emits JSON; `mcp__claude_ai_microsoft_clarity` (or `cli-anything` curl) for Clarity; `cli-anything` Python script using `google-analytics-data` for GA4; `cli-anything` curl for Algolia Insights. Bundled skills: `vale-prose-linting`, `lychee-link-checking`, `pa11y-axe-accessibility-audit`, `pytest-markdown-docs-validation`, `microsoft-clarity-doc-analytics`, `ga4-doc-analytics`, `algolia-doc-search`.
- **Source:** https://vale.sh/ + https://github.com/lycheeverse/lychee + https://github.com/pa11y/pa11y + https://learn.microsoft.com/en-us/clarity/third-party-integrations/clarity-mcp-server
- **Confidence:** ⚠ (Clarity/GA4/Algolia require per-project OAuth or API keys; tooling itself is wired)

## Co-author with users
- **SOTA approach:** 3-stage workflow (Context Gathering → Refinement & Structure → Reader Testing) from Anthropic's `doc-coauthoring` official skill. Stage 3 spawns a fresh Claude reader with no context bleed to surface ambiguities.
- **Agent execution path:** Bundled skill `doc-coauthoring` drives the conversation. Stage 3 uses `Task` subagent dispatch with a `general-purpose` agent given only the draft and a predicted reader question. `github-api` posts the resulting feedback as PR comments.
- **Source:** https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring
- **Confidence:** ✓

## Generate diagrams
- **SOTA approach:** Mermaid (GH-native, inline in markdown) is the default. D2 (Terrastruct, modern auto-layout, multi-theme) for complex architecture diagrams. PlantUML for full UML coverage. Structurizr DSL for C4 model. Render via `mmdc` and `d2` CLIs.
- **Agent execution path:** `cli-anything` (`npm i -g @mermaid-js/mermaid-cli` then `mmdc -i diagram.mmd -o diagram.svg -t dark -b transparent`; `curl -fsSL https://d2lang.com/install.sh | sh` then `d2 input.d2 output.svg`). `drawio-mcp` for diagram types not covered by text-first tools. Bundled skill: `d2-mermaid-diagrams`.
- **Source:** https://github.com/mermaid-js/mermaid-cli + https://github.com/terrastruct/d2
- **Confidence:** ✓

## Translate docs
- **SOTA approach:** DeepL API for high-quality machine translation; Crowdin or Lokalise for translator review workflows; doc-site locale routing (Docusaurus `i18n`, Starlight `locales`, MkDocs Material `i18n` plugin).
- **Agent execution path:** `deepl-mcp` for translation; `cli-anything` curl for Crowdin/Lokalise REST APIs; `filesystem` writes the locale tree. Bundled skill: `deepl-translation-i18n`.
- **Source:** https://www.deepl.com/docs-api + https://developer.crowdin.com/
- **Confidence:** ⚠ (DeepL API key required for free tier above 500k chars/month)

## Capture text from legacy
- **SOTA approach:** Gemini OCR or Mistral OCR for screenshot-only PDFs, scanned docs, image-only legacy archives. Post-process with markdownlint + Vale to bring captured text into the project's style.
- **Agent execution path:** `gemini-ocr-mcp` and `mistral-ocr-mcp` for the OCR pass; `filesystem` writes the result; `cli-anything` runs Vale + markdownlint to normalize.
- **Source:** Vendor docs (Gemini Vision API + Mistral OCR).
- **Confidence:** ✓

---

## Summary table

| Use case | SOTA mechanism | Primary skill pack | Confidence |
|---|---|---|---|
| Write READMEs | Filesystem + `--help` ground-truth | `zero-hallucination-readme` | ✓ |
| Write API docs | Mintlify CLI / Redocly + Scalar | `mintlify-api-docs`, `redocly-openapi-pipeline` | ✓ |
| Write tutorials | Diátaxis + `pytest-markdown-docs` | `pytest-markdown-docs-validation`, `diataxis-divio-system` | ✓ |
| Write reference docs | Sphinx autodoc / TypeDoc / Doxygen / rustdoc | `sphinx-typedoc-reference-docs` | ✓ |
| Write conceptual guides | Diátaxis explanation + D2 + Vale | `diataxis-divio-system`, `d2-mermaid-diagrams` | ✓ |
| Write ADRs | Log4brains + MADR 4.0 + adr-kit | `log4brains-adr-management` | ✓ |
| Write changelogs | git-cliff + release-please | `git-cliff-changelog`, `release-please-automation` | ✓ |
| Architect doc systems | Docusaurus / VitePress / Starlight / MkDocs Material | `docusaurus-vitepress-starlight-mkdocs` | ✓ |
| Apply Diátaxis | File-system separation + Vale rules | `diataxis-divio-system` | ✓ |
| Audit existing docs | Vale + Lychee + pa11y + Clarity + GA4 + Algolia | `vale-prose-linting`, `lychee-link-checking`, `pa11y-axe-accessibility-audit`, `microsoft-clarity-doc-analytics`, `ga4-doc-analytics`, `algolia-doc-search` | ⚠ |
| Co-author with users | 3-stage doc-coauthoring + fresh-Claude reader | `doc-coauthoring` | ✓ |
| Generate diagrams | Mermaid + D2 | `d2-mermaid-diagrams` | ✓ |
| Translate docs | DeepL + Crowdin/Lokalise | `deepl-translation-i18n` | ⚠ |
| Capture from legacy | Gemini OCR + Mistral OCR | (uses `gemini-ocr-mcp` / `mistral-ocr-mcp` directly) | ✓ |

**Fulfillment verdict:** ~100% of use cases have an executable SOTA path. The two `⚠` rows are tool-ready but gated on per-project credentials, not on missing agent capability.
