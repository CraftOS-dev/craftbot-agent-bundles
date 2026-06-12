# Technical Writer — Source Attribution

This file maps every section of `soul.md` and `role.md` back to the downloaded reference file it was lifted from. It is part of the bundle but is **not** loaded into the agent's context — it exists for human verification and future updates.

Raw originals are in `reference/agents/` and `reference/skills/`. Full source URLs are in `agent.yaml → sources` and `reference/INVENTORY.md`.

---

## soul.md → source map

| Section in soul.md | Source file(s) |
|---|---|
| Opening identity paragraph | `reference/agents/msitarzewski-technical-writer.md` (intro paragraphs) |
| "Zero-hallucination protocol" framing | `reference/agents/voltagent-readme-generator.md` (zero-hallucination protocols) |
| Purpose | `reference/agents/msitarzewski-technical-writer.md` (Core Mission) + `reference/agents/wshobson-docs-architect.md` |
| When invoked — README mode | `reference/agents/voltagent-readme-generator.md` (When invoked + Ultradetailed scanning) |
| When invoked — API docs mode | `reference/agents/voltagent-api-documenter.md` (When invoked) + `reference/agents/wshobson-api-documenter.md` (Response Approach) |
| When invoked — Tutorial mode | `reference/agents/wshobson-tutorial-engineer.md` (Tutorial Development Process) |
| When invoked — Reference docs mode | `reference/agents/wshobson-reference-builder.md` (Reference Building Process) |
| When invoked — Architecture docs mode | `reference/agents/wshobson-docs-architect.md` (Documentation Process) |
| When invoked — ADR mode | `reference/skills/architecture-decision-records/SKILL.md` (Core Concepts) |
| When invoked — Audit mode | `reference/agents/voltagent-documentation-engineer.md` (Documentation Analysis) |
| Core operating rules (14 bullets) | `reference/agents/msitarzewski-technical-writer.md` (Critical Rules, Quality Gates, Communication Style) + `reference/agents/voltagent-readme-generator.md` (Zero-hallucination protocols) |
| Mode-specific decisions — README | `reference/agents/voltagent-readme-generator.md` (README responsibilities) + `reference/agents/msitarzewski-technical-writer.md` (5-second test) |
| Mode-specific decisions — API docs | `reference/agents/voltagent-api-documenter.md` (Documentation patterns) + `reference/agents/wshobson-api-documenter.md` (OpenAPI best practices) |
| Mode-specific decisions — Tutorial | `reference/agents/wshobson-tutorial-engineer.md` (Writing Principles + Progressive Sections) |
| Mode-specific decisions — Reference | `reference/agents/wshobson-reference-builder.md` (Best Practices) |
| Mode-specific decisions — Architecture | `reference/agents/wshobson-docs-architect.md` (Output Characteristics + Key Sections) |
| Mode-specific decisions — ADR | `reference/skills/architecture-decision-records/SKILL.md` (Templates + Best Practices) |
| Mode-specific decisions — Audit | `reference/agents/voltagent-documentation-engineer.md` (Documentation Analysis) |
| Divio Documentation System | `reference/agents/msitarzewski-technical-writer.md` (Advanced Capabilities → Documentation Architecture) |
| Quality gates per mode | `reference/agents/msitarzewski-technical-writer.md` (Success Metrics) + `reference/agents/wshobson-tutorial-engineer.md` (Quality Checklist) + `reference/agents/voltagent-documentation-engineer.md` (Documentation checklist) |
| Output format | `reference/agents/wshobson-docs-architect.md` (Output Format) + `reference/agents/wshobson-reference-builder.md` (Output Formats) |
| Communication style | `reference/agents/msitarzewski-technical-writer.md` (Your Communication Style) |
| When to push back | Authored from the synthesis (operational glue informed by Critical Rules + Quality Gates) |
| When to defer | Authored from the synthesis |
| On first conversation (PROACTIVE init) | `agent_bundle/PROGRESS.md` design decision #3 — wording standard across all agents; questions adapted from the role |
| Closing rule | `reference/agents/msitarzewski-technical-writer.md` (Memory section + identity tagline) |

---

## role.md → source map

| Section in role.md | Source file(s) |
|---|---|
| Capability reference → Documentation site generators | `reference/agents/wshobson-api-documenter.md` (Interactive Documentation Platforms) + `reference/agents/msitarzewski-technical-writer.md` (Docs-as-Code Infrastructure) |
| Capability reference → API documentation toolchain | `reference/agents/wshobson-api-documenter.md` (Modern Documentation Standards + Interactive Platforms) |
| Capability reference → SDK generation | `reference/agents/wshobson-api-documenter.md` (SDK and Code Generation) |
| Capability reference → Authoring quality tools | `reference/agents/msitarzewski-technical-writer.md` (Documentation Architecture → Docs Linting) |
| Capability reference → Diagramming | `reference/agents/wshobson-mermaid-expert.md` (capabilities + supported diagram types) |
| Capability reference → Documentation engineering checklist | `reference/agents/voltagent-documentation-engineer.md` (Documentation engineering checklist) |
| Capability reference → Documentation architecture concerns | `reference/agents/voltagent-documentation-engineer.md` (Documentation architecture) |
| Capability reference → Documentation testing | `reference/agents/voltagent-documentation-engineer.md` (Documentation testing) |
| Capability reference → Multi-version docs | `reference/agents/voltagent-documentation-engineer.md` (Multi-version documentation) |
| Capability reference → Search optimization | `reference/agents/voltagent-documentation-engineer.md` (Search optimization) |
| Capability reference → Contribution workflows | `reference/agents/voltagent-documentation-engineer.md` (Contribution workflows) |
| README template | `reference/agents/msitarzewski-technical-writer.md` (High-Quality README Template) |
| OpenAPI template | `reference/agents/msitarzewski-technical-writer.md` (OpenAPI Documentation Example) |
| OpenAPI best practices | `reference/agents/voltagent-api-documenter.md` (OpenAPI best practices) |
| Tutorial template | `reference/agents/msitarzewski-technical-writer.md` (Tutorial Structure Template) |
| Tutorial writing principles | `reference/agents/wshobson-tutorial-engineer.md` (Writing Principles) |
| Exercise types | `reference/agents/wshobson-tutorial-engineer.md` (Exercise Types) |
| Common tutorial formats | `reference/agents/wshobson-tutorial-engineer.md` (Common Tutorial Formats) |
| Docusaurus configuration | `reference/agents/msitarzewski-technical-writer.md` (Docusaurus Configuration) |
| Reference doc entry format | `reference/agents/wshobson-reference-builder.md` (Documentation Structure → Entry Format) |
| Hierarchical structure for reference docs | `reference/agents/wshobson-reference-builder.md` (Hierarchical Structure) |
| Navigation aids | `reference/agents/wshobson-reference-builder.md` (Navigation Aids) |
| Warnings and notes | `reference/agents/wshobson-reference-builder.md` (Warnings and Notes) |
| ADR templates (MADR, Lightweight, Y-Statement) | `reference/skills/architecture-decision-records/SKILL.md` (Templates 1, 2, 3) |
| ADR lifecycle | `reference/skills/architecture-decision-records/SKILL.md` (Core Concepts → ADR Lifecycle) |
| ADR directory structure | `reference/skills/architecture-decision-records/SKILL.md` (ADR Management → Directory Structure) |
| ADR automation | `reference/skills/architecture-decision-records/SKILL.md` (Automation with adr-tools) |
| ADR review checklist | `reference/skills/architecture-decision-records/SKILL.md` (Review Process) |
| ADR best practices | `reference/skills/architecture-decision-records/SKILL.md` (Best Practices → Do's and Don'ts) |
| Conventional Commits — examples | `reference/skills/changelog-automation/SKILL.md` (Commit Message Examples) |
| Conventional Commits — types table | `reference/skills/changelog-automation/SKILL.md` (Commit Types) |
| Keep a Changelog format | `reference/skills/changelog-automation/SKILL.md` (Core Concepts) |
| Release-notes structure | `reference/skills/changelog-automation/SKILL.md` (Release Note Sections) |
| Mermaid diagram catalog | `reference/agents/wshobson-mermaid-expert.md` (Supported diagram types) |
| Mermaid methodology | `reference/agents/wshobson-mermaid-expert.md` (Methodology) |
| Doc co-authoring workflow detail (3 stages) | `reference/skills/doc-coauthoring/SKILL.md` (Stage 1, 2, 3) |
| Success metrics | `reference/agents/msitarzewski-technical-writer.md` (Your Success Metrics) |
| Documentation audit checklist | `reference/agents/voltagent-documentation-engineer.md` (Documentation Analysis → Audit) + composition synthesis |
| Writing principles condensed | `reference/agents/msitarzewski-technical-writer.md` (Your Communication Style) |

---

## Notes on "authored from synthesis"

Small sections in soul.md were composed locally rather than lifted verbatim:

- **When to push back** (4 bullets) — operational glue derived from the Critical Rules and Quality Gates sections of msitarzewski. Anchors the rules in concrete user-facing situations.
- **When to defer** (4 bullets) — operational glue. Domain claims (project rules win, tool agnosticism, audience research is owned by user) come from the references; the framing is composed.
- **First-conversation routine questions** — adapted from the standard PROACTIVE.md self-init pattern (decision #3 in `PROGRESS.md`). The three role-specific questions are tailored to technical writing workflows.

These are operational glue, not domain claims. They do not introduce knowledge claims that lack a source.

---

## How to update this agent

If you want to refresh content from upstream:

1. Re-fetch the source files listed in `reference/INVENTORY.md` and overwrite `reference/agents/*.md` and `reference/skills/*/SKILL.md` in place.
2. Diff against the previous versions to see what changed.
3. Update the corresponding sections of `soul.md` and `role.md` to match.
4. Update this `SOURCES.md` if section names or source URLs changed.
5. Re-run `build.py` to regenerate `dist/technical-writer.craftbot`.

The reference files are stored verbatim with source URLs, so the update path is mechanical and traceable.

---

## SOTA sources (June 2026)

The `role.md → SOTA tool reference (June 2026)` section and the bundled SOTA skill packs (`skills/mintlify-api-docs/`, `skills/redocly-openapi-pipeline/`, etc.) trace to these primary sources. Each row pairs the tool with the canonical URL the agent consulted.

| Tool / framework | Source | Used in |
|---|---|---|
| Mintlify CLI | https://mintlify.com/docs/installation | `skills/mintlify-api-docs/SKILL.md` |
| Mintlify llms.txt | https://mintlify.com/blog/llmstxt | `skills/mintlify-api-docs/SKILL.md` |
| Mintlify MCP integration | https://mintlify.com/docs/integrations/mcp | `skills/mintlify-api-docs/SKILL.md` |
| Mintlify comparison | https://www.mintlify.com/library/best-api-docs-and-sdk-generation-tools | `reference/SOTA_USE_CASES.md` |
| Redocly CLI | https://github.com/Redocly/redocly-cli | `skills/redocly-openapi-pipeline/SKILL.md` |
| Redocly docs | https://redocly.com/docs/cli/ | `skills/redocly-openapi-pipeline/SKILL.md` |
| Scalar API reference | https://github.com/scalar/scalar | `skills/redocly-openapi-pipeline/SKILL.md` |
| OpenAPI 3.1 spec | https://spec.openapis.org/oas/v3.1.0 | `skills/redocly-openapi-pipeline/SKILL.md`, `skills/openapi-sdk-generation/SKILL.md` |
| @hey-api/openapi-ts | https://github.com/hey-api/openapi-ts | `skills/openapi-sdk-generation/SKILL.md` |
| @openapitools/openapi-generator-cli | https://github.com/OpenAPITools/openapi-generator-cli | `skills/openapi-sdk-generation/SKILL.md` |
| OpenAPI Generator | https://openapi-generator.tech/ | `skills/openapi-sdk-generation/SKILL.md` |
| Speakeasy | https://www.speakeasy.com/ | `skills/openapi-sdk-generation/SKILL.md` |
| Fern | https://www.buildwithfern.com/ | `skills/openapi-sdk-generation/SKILL.md` |
| Log4brains | https://github.com/thomvaill/log4brains | `skills/log4brains-adr-management/SKILL.md` |
| adr-kit | https://github.com/kschlt/adr-kit | `skills/log4brains-adr-management/SKILL.md` |
| MADR 4.0 template | https://adr.github.io/madr/ | `skills/log4brains-adr-management/SKILL.md` |
| adr-tools (legacy) | https://github.com/npryce/adr-tools | `skills/log4brains-adr-management/SKILL.md` |
| git-cliff | https://github.com/orhun/git-cliff | `skills/git-cliff-changelog/SKILL.md` |
| git-cliff docs | https://git-cliff.org/docs/ | `skills/git-cliff-changelog/SKILL.md` |
| git-cliff-action | https://github.com/orhun/git-cliff-action | `skills/git-cliff-changelog/SKILL.md` |
| Conventional Commits | https://www.conventionalcommits.org/ | `skills/git-cliff-changelog/SKILL.md`, `skills/release-please-automation/SKILL.md` |
| Keep a Changelog | https://keepachangelog.com/en/1.1.0/ | `skills/git-cliff-changelog/SKILL.md` |
| release-please | https://github.com/googleapis/release-please | `skills/release-please-automation/SKILL.md` |
| release-please-action | https://github.com/googleapis/release-please-action | `skills/release-please-automation/SKILL.md` |
| SemVer | https://semver.org/ | `skills/release-please-automation/SKILL.md` |
| Lychee | https://github.com/lycheeverse/lychee | `skills/lychee-link-checking/SKILL.md` |
| lychee-action | https://github.com/lycheeverse/lychee-action | `skills/lychee-link-checking/SKILL.md` |
| Lychee docs | https://lychee.cli.rs/ | `skills/lychee-link-checking/SKILL.md` |
| Vale | https://vale.sh/ | `skills/vale-prose-linting/SKILL.md` |
| Vale GitHub | https://github.com/errata-ai/vale | `skills/vale-prose-linting/SKILL.md` |
| Google style pack | https://github.com/errata-ai/Google | `skills/vale-prose-linting/SKILL.md` |
| Microsoft style pack | https://github.com/errata-ai/Microsoft | `skills/vale-prose-linting/SKILL.md` |
| write-good | https://github.com/errata-ai/write-good | `skills/vale-prose-linting/SKILL.md` |
| proselint | https://github.com/errata-ai/proselint | `skills/vale-prose-linting/SKILL.md` |
| alex (errata-ai pack) | https://github.com/errata-ai/alex | `skills/vale-prose-linting/SKILL.md` |
| pytest-markdown-docs (Modal) | https://github.com/modal-labs/pytest-markdown-docs | `skills/pytest-markdown-docs-validation/SKILL.md` |
| mktestdocs | https://github.com/koaning/mktestdocs | `skills/pytest-markdown-docs-validation/SKILL.md` |
| pa11y | https://github.com/pa11y/pa11y | `skills/pa11y-axe-accessibility-audit/SKILL.md` |
| pa11y-ci | https://github.com/pa11y/pa11y-ci | `skills/pa11y-axe-accessibility-audit/SKILL.md` |
| axe-core | https://github.com/dequelabs/axe-core | `skills/pa11y-axe-accessibility-audit/SKILL.md` |
| Lighthouse CI | https://github.com/GoogleChrome/lighthouse-ci | `skills/pa11y-axe-accessibility-audit/SKILL.md` |
| WCAG 2.2 AA quickref | https://www.w3.org/WAI/WCAG22/quickref/?levels=aa | `skills/pa11y-axe-accessibility-audit/SKILL.md` |
| Microsoft Clarity | https://clarity.microsoft.com/ | `skills/microsoft-clarity-doc-analytics/SKILL.md` |
| Clarity MCP server | https://learn.microsoft.com/en-us/clarity/third-party-integrations/clarity-mcp-server | `skills/microsoft-clarity-doc-analytics/SKILL.md` |
| Clarity Data Export API | https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api | `skills/microsoft-clarity-doc-analytics/SKILL.md` |
| google-analytics-data (PyPI) | https://pypi.org/project/google-analytics-data/ | `skills/ga4-doc-analytics/SKILL.md` |
| GA4 Data API | https://developers.google.com/analytics/devguides/reporting/data/v1 | `skills/ga4-doc-analytics/SKILL.md` |
| Sphinx | https://www.sphinx-doc.org/ | `skills/sphinx-typedoc-reference-docs/SKILL.md` |
| sphinx-autodoc-typehints | https://github.com/tox-dev/sphinx-autodoc-typehints | `skills/sphinx-typedoc-reference-docs/SKILL.md` |
| Furo theme | https://github.com/pradyunsg/furo | `skills/sphinx-typedoc-reference-docs/SKILL.md` |
| TypeDoc | https://typedoc.org/ | `skills/sphinx-typedoc-reference-docs/SKILL.md` |
| typedoc-plugin-markdown | https://typedoc-plugin-markdown.org/ | `skills/sphinx-typedoc-reference-docs/SKILL.md` |
| Doxygen | https://www.doxygen.nl/ | `skills/sphinx-typedoc-reference-docs/SKILL.md` |
| doxygen-awesome-css | https://github.com/jothepro/doxygen-awesome-css | `skills/sphinx-typedoc-reference-docs/SKILL.md` |
| rustdoc | https://doc.rust-lang.org/rustdoc/ | `skills/sphinx-typedoc-reference-docs/SKILL.md` |
| Docusaurus | https://docusaurus.io/ | `skills/docusaurus-vitepress-starlight-mkdocs/SKILL.md` |
| VitePress | https://vitepress.dev/ | `skills/docusaurus-vitepress-starlight-mkdocs/SKILL.md` |
| Astro Starlight | https://starlight.astro.build/ | `skills/docusaurus-vitepress-starlight-mkdocs/SKILL.md` |
| MkDocs Material | https://squidfunk.github.io/mkdocs-material/ | `skills/docusaurus-vitepress-starlight-mkdocs/SKILL.md` |
| Mermaid | https://mermaid.js.org/ | `skills/d2-mermaid-diagrams/SKILL.md` |
| Mermaid CLI | https://github.com/mermaid-js/mermaid-cli | `skills/d2-mermaid-diagrams/SKILL.md` |
| D2 (Terrastruct) | https://d2lang.com/ | `skills/d2-mermaid-diagrams/SKILL.md` |
| D2 GitHub | https://github.com/terrastruct/d2 | `skills/d2-mermaid-diagrams/SKILL.md` |
| PlantUML | https://plantuml.com/ | `skills/d2-mermaid-diagrams/SKILL.md` |
| Structurizr | https://structurizr.com/ | `skills/d2-mermaid-diagrams/SKILL.md` |
| C4 model | https://c4model.com/ | `skills/d2-mermaid-diagrams/SKILL.md` |
| Diátaxis framework | https://diataxis.fr/ | `skills/diataxis-divio-system/SKILL.md` |
| Divio "Four kinds of doc" | https://www.writethedocs.org/videos/eu/2017/the-four-kinds-of-documentation-and-why-you-need-to-understand-what-they-are-daniele-procida/ | `skills/diataxis-divio-system/SKILL.md` |
| DeepL API | https://developers.deepl.com/ | `skills/deepl-translation-i18n/SKILL.md` |
| Crowdin API | https://developer.crowdin.com/ | `skills/deepl-translation-i18n/SKILL.md` |
| Crowdin GitHub Action | https://github.com/crowdin/github-action | `skills/deepl-translation-i18n/SKILL.md` |
| Lokalise CLI | https://github.com/lokalise/lokalise-cli-2-go | `skills/deepl-translation-i18n/SKILL.md` |
| Awesome README | https://github.com/matiassingers/awesome-readme | `skills/zero-hallucination-readme/SKILL.md` |
| NN/g 5-second test | https://www.nngroup.com/articles/usability-testing-101/ | `skills/zero-hallucination-readme/SKILL.md` |
| Algolia DocSearch | https://docsearch.algolia.com/ | `skills/algolia-doc-search/SKILL.md` |
| Algolia Analytics API | https://www.algolia.com/doc/rest-api/analytics/ | `skills/algolia-doc-search/SKILL.md` |
| Algolia Crawler | https://www.algolia.com/doc/tools/crawler/ | `skills/algolia-doc-search/SKILL.md` |
| Pagefind | https://pagefind.app/ | `skills/algolia-doc-search/SKILL.md` |
| MeiliSearch | https://www.meilisearch.com/ | `skills/algolia-doc-search/SKILL.md` |
| Typesense | https://typesense.org/ | `skills/algolia-doc-search/SKILL.md` |
| Orama | https://oramasearch.com/ | `skills/algolia-doc-search/SKILL.md` |

These sources informed the `SOTA tool reference (June 2026)` section in `role.md`, the per-use-case mapping in `reference/SOTA_USE_CASES.md`, and the bundled SOTA skill packs.
