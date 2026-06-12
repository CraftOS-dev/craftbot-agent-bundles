# Research Analyst — Source Attribution

Section-to-source map for soul.md and role.md. This file is part of the bundle but is **not** loaded into context — it exists for human verification and future refreshes.

Raw downloads are in `reference/agents/` and `reference/skills/`. URLs in `agent.yaml → sources` and `reference/INVENTORY.md`.

---

## soul.md → source map

| Section | Source(s) |
|---|---|
| Opening identity | `reference/agents/voltagent-research-analyst.md` (intro) |
| "You are a generalist" framing | composition synthesis based on VoltAgent research-analysis category being broad (11 agents) |
| Purpose | `voltagent-research-analyst.md` (Purpose) + `wshobson-business-analyst.md` (Purpose) |
| When invoked — General research | `voltagent-research-analyst.md` (When invoked + Research methodology) |
| When invoked — Market research | `voltagent-market-researcher.md` (When invoked + Market analysis + Strategic insights) |
| When invoked — Competitive intelligence | `voltagent-competitive-analyst.md` (Competitor identification + SWOT + Strategic recommendations) |
| When invoked — Trend analysis | `voltagent-trend-analyst.md` (Workflow phases + methodologies) |
| When invoked — Scientific literature | `voltagent-scientific-literature-researcher.md` (When invoked + Search strategy + Evidence synthesis) |
| When invoked — Data research | `voltagent-data-researcher.md` (operational framework) |
| When invoked — Targeted search | `voltagent-search-specialist.md` (Boolean operators, precision rate target) |
| When invoked — First-principles | `voltagent-first-principles-thinking.md` (5-step method + reframing principle + 5D method) |
| Core operating rules | merged across `voltagent-research-analyst.md` (Research best practices + Quality control) + `voltagent-scientific-literature-researcher.md` (limitation transparency + quality weighting) + `voltagent-competitive-analyst.md` (ethical methods) + `voltagent-search-specialist.md` (precision target) |
| Mode-specific decisions | one entry per reference agent matched to its mode |
| Quality gates | `voltagent-research-analyst.md` (Research analysis checklist + Excellence checklist) |
| Output format | `voltagent-research-analyst.md` (Report creation + Communication excellence) + `data-storytelling/SKILL.md` (Setup → Conflict → Resolution + so-what principle) |
| Communication style | `voltagent-research-analyst.md` (Communication excellence) + `data-storytelling/SKILL.md` |
| When to push back | composition synthesis derived from `voltagent-research-analyst.md` (Quality assurance + Bias control) and `voltagent-competitive-analyst.md` (ethical methods) |
| When to defer | composition synthesis |
| First-conversation routine questions | standard PROACTIVE.md self-init pattern (`PROGRESS.md` decision #3); questions tailored to research workflows |
| Closing rule | `voltagent-research-analyst.md` (closing line) |

---

## role.md → source map

| Section | Source(s) |
|---|---|
| Capability reference → Research domains | `voltagent-research-analyst.md` (Research domains) |
| Capability reference → Information-gathering channels | `voltagent-research-analyst.md` (Information gathering) |
| Capability reference → Analysis techniques | `voltagent-research-analyst.md` (Analysis techniques) + `wshobson-business-analyst.md` (Statistical Analysis) |
| Capability reference → Search-engine catalog | composition synthesis (CraftBot defaults: brave-search, duckduckgo, baidu, playwright-mcp, firecrawl, google-scholar-mcp, ai-news-collectors) |
| Capability reference → BI and analytics platforms | `wshobson-business-analyst.md` (Modern Analytics Platforms) |
| Source evaluation framework | `voltagent-research-analyst.md` (Source evaluation) — extended with the 5-dimension scoring matrix from composition |
| Bias detection checklist | `voltagent-research-analyst.md` (Quality assurance → Bias checking) + composition synthesis |
| Search strategies — Boolean operators | `voltagent-search-specialist.md` (Boolean operators) |
| Search strategies — Proximity searching | `voltagent-search-specialist.md` (proximity searching) |
| Search strategies — Multi-source triangulation | `voltagent-research-analyst.md` (Source triangulation) |
| Search strategies — Iterative refinement | `voltagent-search-specialist.md` (iterative refinement) |
| Synthesis frameworks | `voltagent-research-analyst.md` (Synthesis strategies + Insight generation) |
| Cohort analysis playbook | `voltagent-cohort-analysis.md` (entire file — Types of cohorts, Retention metrics, Retention curve diagnosis, Activation analysis, Table format) |
| Trend analysis playbook | `voltagent-trend-analyst.md` (Primary functions + Key methodologies + Workflow phases + Strategic communication) |
| Competitive intelligence playbook | `voltagent-competitive-analyst.md` (Competitor identification + Intelligence gathering + SWOT + Benchmarking + Monitoring systems) |
| Market research playbook | `voltagent-market-researcher.md` (Market analysis + Consumer research + Segmentation + Opportunity identification + Strategic recommendations) |
| Scientific literature playbook | `voltagent-scientific-literature-researcher.md` (Search strategy + Evidence synthesis + Domain expertise) |
| First-principles method | `voltagent-first-principles-thinking.md` (5-step method + Reframing + 5D Method + Recommended applications) |
| KPI framework | `skills/kpi-dashboard-design/SKILL.md` (entire skill — tiers, SMART, hierarchy, best practices, troubleshooting) |
| Data storytelling principles | `skills/data-storytelling/SKILL.md` (entire skill — 3 essential elements, story structure, central principle, critical guidance) |
| Statistical rigor checklist | composition synthesis informed by `wshobson-business-analyst.md` (Statistical Analysis) + `voltagent-scientific-literature-researcher.md` (study quality evaluation) |
| Report templates (executive briefing / research report / trend report / competitive intelligence report) | composition synthesis combining `voltagent-research-analyst.md` (Report creation), `voltagent-trend-analyst.md` (Strategic Communication), `voltagent-competitive-analyst.md` (Strategic recommendations format) |
| Writing principles condensed | merged from `data-storytelling/SKILL.md` + `voltagent-research-analyst.md` (Communication excellence) |

---

## Notes on "authored from synthesis"

Several role.md sections include composition synthesis on top of the referenced material:

- **Source evaluation framework — 5-dimension scoring matrix** — methodology synthesized from VoltAgent's "Source evaluation" bullet list into an explicit framework. Domain claims (authority/currency/accuracy/purpose/methodology) come from the references; the matrix shape is composed.
- **Bias detection checklist** — VoltAgent lists "bias checking" as a quality concern; the 8-item checklist below was synthesized to make it actionable.
- **Statistical rigor checklist** — items come from `wshobson-business-analyst.md` and `voltagent-scientific-literature-researcher.md`; the checklist format is composed.
- **Report templates** — section names and structure synthesized from the references' descriptions of what reports should contain.
- **Capability reference → Search-engine catalog** — names the CraftBot default skills enabled in `agent.yaml`; descriptions are summaries of those CraftBot skills.

The first-conversation PROACTIVE.md self-init footer is the standard pattern (PROGRESS.md decision #3), adapted with research-specific routine questions.

---

## How to update this agent

1. Re-fetch source files listed in `reference/INVENTORY.md`, overwrite `reference/agents/*.md` and `reference/skills/*/SKILL.md` in place
2. Diff against previous versions to see what changed
3. Update corresponding sections of `soul.md` and `role.md`
4. Update this `SOURCES.md` if section names or source URLs changed
5. Re-run `build.py` to regenerate `dist/research-analyst.craftbot`

---

## SOTA tool sources (June 2026)

Source map for the SOTA-tool reference section in `role.md` and the bundled skill packs in `skills/`. Per-use-case mapping with confidence flags lives in `reference/SOTA_USE_CASES.md`.

| Tool / API | Source URL | Skill pack(s) |
|---|---|---|
| Paper Search MCP (openags) | https://mcpservers.org/servers/openags/paper-search-mcp | `paper-search-mcp` |
| Perplexity Sonar (Pro / Deep Research) | https://docs.perplexity.ai/docs/sonar/models/sonar-deep-research | `perplexity-deep-research` |
| Perplexity pricing | https://docs.perplexity.ai/docs/pricing | `perplexity-deep-research` |
| Exa.ai (neural search) | https://exa.ai/ · https://docs.exa.ai/ | `exa-neural-search` |
| SEC EDGAR API | https://www.sec.gov/edgar/sec-api-documentation | `sec-edgar-market-sizing` |
| SEC XBRL frames | https://www.sec.gov/structureddata/xbrl-data-frames | `sec-edgar-market-sizing` |
| USPTO PatentsView | https://data.uspto.gov/apis/getting-started · https://patentsview.org/apis/api-endpoints | `patents-uspto-lens` |
| Lens.org Patent API | https://docs.api.lens.org/ | `patents-uspto-lens` |
| Crunchbase API | https://data.crunchbase.com/docs/using-the-api | `crunchbase-market-research` |
| Similarweb free API | https://github.com/DaWe35/Similarweb-free-API | `crunchbase-market-research` |
| pytrends (Google Trends) | https://github.com/GeneralMills/pytrends | `trend-fan-out-multi-source` |
| PRAW (Reddit) | https://praw.readthedocs.io/ | `trend-fan-out-multi-source` |
| HN Algolia Search | https://hn.algolia.com/api | `trend-fan-out-multi-source` |
| GDELT 2.0 DOC API | https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/ | `gdelt-news-monitoring` |
| GDELT GKG codebook | https://blog.gdeltproject.org/the-gdelt-global-knowledge-graph-gkg-data-format-codebook-v2-1/ | `gdelt-news-monitoring` |
| arXiv API | https://info.arxiv.org/help/api/user-manual.html | `paper-search-mcp`, `trend-fan-out-multi-source` |
| CrossRef REST | https://www.crossref.org/documentation/retrieve-metadata/rest-api/ | `paper-search-mcp` |
| Europe PMC REST | https://europepmc.org/RestfulWebService | `paper-search-mcp` |
| ClinicalTrials.gov v2 | https://clinicaltrials.gov/data-api/api | `paper-search-mcp` |
| Semantic Scholar Graph | https://www.semanticscholar.org/product/api · https://api.semanticscholar.org/api-docs/graph | `semantic-scholar-openalex`, `paper-search-mcp` |
| Semantic Scholar Recommendations | https://api.semanticscholar.org/api-docs/recommendations | `semantic-scholar-openalex` |
| OpenAlex | https://docs.openalex.org/ | `semantic-scholar-openalex`, `paper-search-mcp` |
| OpenAlex filter syntax | https://docs.openalex.org/how-to-use-the-api/filter-entity-lists | `semantic-scholar-openalex` |
| PubMed E-utilities | https://www.ncbi.nlm.nih.gov/books/NBK25497/ | `paper-search-mcp` |
| scite.ai | https://help.scite.ai/en-us/category/scite-api-tomi6w/ | `paper-search-mcp` |
| Unpaywall | https://unpaywall.org/products/api | `paper-search-mcp` |
| Kaggle API | https://github.com/Kaggle/kaggle-api · https://pypi.org/project/kaggle/ | `kaggle-huggingface-datasets` |
| Hugging Face Datasets | https://huggingface.co/docs/datasets/index | `kaggle-huggingface-datasets` |
| Hugging Face Hub Python | https://huggingface.co/docs/huggingface_hub/ | `kaggle-huggingface-datasets` |
| FRED API | https://fred.stlouisfed.org/docs/api/fred/ · https://github.com/mortada/fredapi | `authoritative-data-fred-worldbank` |
| World Bank Indicators | https://datahelpdesk.worldbank.org/knowledgebase/articles/889392 | `authoritative-data-fred-worldbank` |
| IMF DataMapper | https://www.imf.org/external/datamapper/api/help | `authoritative-data-fred-worldbank` |
| OECD SDMX-JSON | https://data.oecd.org/api/ | `authoritative-data-fred-worldbank` |
| Eurostat REST | https://ec.europa.eu/eurostat/web/main/data/web-services | `authoritative-data-fred-worldbank` |
| BLS Developers | https://www.bls.gov/developers/ | `authoritative-data-fred-worldbank` |
| PostHog Cohorts | https://posthog.com/docs/api/cohorts | `cohort-retention-lifelines` |
| PostHog HogQL | https://posthog.com/docs/hogql | `cohort-retention-lifelines` |
| lifelines (Kaplan-Meier) | https://lifelines.readthedocs.io/ | `cohort-retention-lifelines` |
| Claude extended thinking | https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking | `first-principles-claude-extended` |
| Plotly Python | https://plotly.com/python/ | `data-storytelling-plotly-altair` |
| Altair | https://altair-viz.github.io/ | `data-storytelling-plotly-altair` |
| Vega-Lite | https://vega.github.io/vega-lite/ | `data-storytelling-plotly-altair` |
| matplotlib | https://matplotlib.org/ | `data-storytelling-plotly-altair` |
| seaborn | https://seaborn.pydata.org/ | `data-storytelling-plotly-altair` |
| kaleido (Plotly export) | https://github.com/plotly/Kaleido | `data-storytelling-plotly-altair` |
| Datawrapper API | https://developer.datawrapper.de/ | `data-storytelling-plotly-altair` |
| Mermaid CLI | https://github.com/mermaid-js/mermaid-cli | `data-storytelling-plotly-altair` |
| Pandoc | https://pandoc.org/MANUAL.html | `pandoc-branded-deliverables` |
| pandoc-crossref | https://lierdakil.github.io/pandoc-crossref/ | `pandoc-branded-deliverables` |
| Mistral OCR | https://docs.mistral.ai/capabilities/document/ | `ocr-scanned-academic-papers` |
| Gemini document understanding | https://ai.google.dev/gemini-api/docs/document-processing | `ocr-scanned-academic-papers` |
| DeepL document API | https://developers.deepl.com/docs/api-reference/document | (deepl-mcp) |
| Wappalyzer | https://www.wappalyzer.com/ | `competitive-intelligence-tech-stack` |
| python-Wappalyzer | https://github.com/chorsley/python-Wappalyzer | `competitive-intelligence-tech-stack` |
| GitHub REST API | https://docs.github.com/en/rest | `competitive-intelligence-tech-stack` |

### Bundled skill packs (`skills/`) — file map

| Skill folder | Companion playbook in role.md |
|---|---|
| `paper-search-mcp/` | Scientific literature playbook |
| `perplexity-deep-research/` | Search strategies → Multi-source triangulation |
| `exa-neural-search/` | Search strategies → Iterative query refinement |
| `sec-edgar-market-sizing/` | Market research playbook → Market sizing |
| `patents-uspto-lens/` | Competitive intelligence playbook, Trend analysis playbook |
| `trend-fan-out-multi-source/` | Trend analysis playbook |
| `gdelt-news-monitoring/` | Trend analysis playbook → Source types for weak-signal detection |
| `semantic-scholar-openalex/` | Scientific literature playbook |
| `authoritative-data-fred-worldbank/` | Capability reference → Information-gathering channels |
| `kaggle-huggingface-datasets/` | Capability reference → Data mining |
| `cohort-retention-lifelines/` | Cohort analysis playbook |
| `first-principles-claude-extended/` | First-principles method |
| `data-storytelling-plotly-altair/` | Data storytelling principles |
| `pandoc-branded-deliverables/` | Report templates |
| `competitive-intelligence-tech-stack/` | Competitive intelligence playbook |
| `crunchbase-market-research/` | Market research playbook → Private-company segment |
| `ocr-scanned-academic-papers/` | Scientific literature playbook → Foreign / scanned PDFs |

### Per-use-case mapping

See `reference/SOTA_USE_CASES.md` for the per-use-case SOTA approach, agent execution path, source URL, and confidence flag (✓ / ⚠ / ✗) — required reading for understanding what the agent can and cannot fully automate.
