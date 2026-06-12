# Technical Writer — Reference Inventory

Raw downloaded SOTA material used to compose the agent. Nothing here was authored locally — every file was downloaded verbatim from an external source.

**Composition rule:** every section in `agent.yaml`, `soul.md`, and `role.md` must trace back to one or more files in this folder.

---

## Reference Agents (9 files)

| File | Source repo | Source URL | Description | Status |
|---|---|---|---|---|
| `agents/wshobson-api-documenter.md` | wshobson/agents | [link](https://github.com/wshobson/agents/blob/main/plugins/documentation-generation/agents/api-documenter.md) | Master API docs with OpenAPI 3.1, AI tooling, interactive portals, SDK generation, dev experience. Heavy capability map. | full |
| `agents/wshobson-docs-architect.md` | wshobson/agents | [link](https://github.com/wshobson/agents/blob/main/plugins/documentation-generation/agents/docs-architect.md) | Comprehensive long-form documentation from codebases — system manuals, architecture guides, technical deep-dives. | full |
| `agents/wshobson-tutorial-engineer.md` | wshobson/agents | [link](https://github.com/wshobson/agents/blob/main/plugins/documentation-generation/agents/tutorial-engineer.md) | Step-by-step tutorials and educational content. Pedagogical design + progressive disclosure + hands-on exercises. | full |
| `agents/wshobson-reference-builder.md` | wshobson/agents | [link](https://github.com/wshobson/agents/blob/main/plugins/documentation-generation/agents/reference-builder.md) | Exhaustive technical references — comprehensive parameter listings, configuration guides, searchable reference materials. | full |
| `agents/wshobson-mermaid-expert.md` | wshobson/agents | [link](https://github.com/wshobson/agents/blob/main/plugins/documentation-generation/agents/mermaid-expert.md) | Mermaid diagram creation across 8 diagram types (flowcharts, sequence, ER, state, gantt, etc.). | **summary** (WebFetch refused verbatim) |
| `agents/voltagent-documentation-engineer.md` | VoltAgent/awesome-claude-code-subagents | [link](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/06-developer-experience/documentation-engineer.md) | Senior documentation engineer — API docs, tutorials, architecture guides, automation, search optimization. | full |
| `agents/voltagent-api-documenter.md` | VoltAgent/awesome-claude-code-subagents | [link](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/07-specialized-domains/api-documenter.md) | API documenter: OpenAPI specs, interactive portals, SDK references, code examples, authentication guides. | full |
| `agents/voltagent-readme-generator.md` | VoltAgent/awesome-claude-code-subagents | [link](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/06-developer-experience/readme-generator.md) | Maintainer-ready READMEs with **zero-hallucination protocol** — extracts exact reality from repo, no guessing. | full |
| `agents/msitarzewski-technical-writer.md` | msitarzewski/agency-agents | [link](https://github.com/msitarzewski/agency-agents/blob/main/engineering/engineering-technical-writer.md) | Technical writer agent with full README + OpenAPI + tutorial + Docusaurus templates, Divio Documentation System reference, success metrics. **Richest single source.** | full |

## Reference Skills (4 files)

Real SKILL.md packs we will **bundle inside the .craftbot** under `agents/technical-writer/skills/`.

| File | Source URL | Description | Status |
|---|---|---|---|
| `skills/architecture-decision-records/SKILL.md` | [link](https://github.com/wshobson/agents/tree/main/plugins/documentation-generation/skills/architecture-decision-records) | ADRs — context/decision/consequences. 5 template formats (MADR, lightweight, Y-statement, deprecation, RFC). Directory structure, automation with adr-tools, review checklist. | full |
| `skills/changelog-automation/SKILL.md` | [link](https://github.com/wshobson/agents/tree/main/plugins/documentation-generation/skills/changelog-automation) | Keep a Changelog + Conventional Commits + semantic versioning. Commit examples, type table, automation tooling. | full |
| `skills/openapi-spec-generation/SKILL.md` | [link](https://github.com/wshobson/agents/tree/main/plugins/documentation-generation/skills/openapi-spec-generation) | OpenAPI 3.1 — structure, design-first vs code-first, best practices. | full |
| `skills/doc-coauthoring/SKILL.md` | [link](https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring) | **Official Anthropic skill.** 3-stage workflow (Context Gathering → Refinement & Structure → Reader Testing) for substantial writing tasks. | full |

## Sources Considered But Not Downloaded

| Source | Why excluded |
|---|---|
| `wshobson/agents` — `plugins/code-documentation/` skills | Likely overlaps with documentation-generation skills already harvested. Can add later if depth needed. |
| `wshobson/agents` — `plugins/content-marketing/` and `plugins/seo-content-creation/` | More appropriate for the **marketing-agent** (general) and **video-creator** (specialized) — different roles in v0 roster. |
| Anthropic skills — `docx`, `pdf`, `pptx` | Already shipped as CraftBot defaults. Recipient already has them via `skills_config.json`. |
| Anthropic skills — `internal-comms` | Adjacent to technical writing but more "team communications" oriented. Will reconsider for a `comms-writer` specialist in v1. |
| `vijaythecoder/awesome-claude-agents` | Lists agents at framework-specialist tier (Laravel/Rails/Vue) — not technical-writing focused. |

---

## Status check

- ✅ 8 agent reference files saved verbatim
- ✅ 4 skill files saved verbatim
- ⚠️ 1 agent file (`wshobson-mermaid-expert`) saved as **WebFetch summary** — clearly marked at top of file
- ✅ All sources cited with URL + repo

## What gets used at composition time

When I write `agent.yaml`, `soul.md`, and `role.md`, every section traces back to a specific file in this folder. The 4 skill folders under `skills/` get copied into `agents/technical-writer/skills/` to ship inside the `.craftbot`.

The **9 agent references** give a rich cross-cut:
- **Generalist documentation** (msitarzewski-technical-writer, wshobson-docs-architect, voltagent-documentation-engineer)
- **API-specialist** angle (wshobson-api-documenter, voltagent-api-documenter)
- **README-specialist** angle (voltagent-readme-generator with its zero-hallucination protocol)
- **Tutorial-specialist** angle (wshobson-tutorial-engineer)
- **Reference-specialist** angle (wshobson-reference-builder)
- **Diagram-specialist** angle (wshobson-mermaid-expert)

The msitarzewski file is the richest — full templates for README, OpenAPI, tutorials, and Docusaurus config, plus the Divio Documentation System reference and concrete success metrics.

## Waiting for approval

Stop here per the workflow. Tell me:
1. Is this set of references sufficient, or should I dig for more (e.g., the code-documentation plugin, content-marketing skills)?
2. Are there sources I should drop?
3. Accept the 1 summary file (mermaid-expert) as-is?

Only after your go-ahead do I move to composition (Step 4 — author `agent.yaml`, `soul.md`, `role.md`, copy skills into the bundle).
