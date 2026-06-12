# Research Analyst — SOTA Use-Case Mapping (June 2026)

Per-use-case mapping of the SOTA approach, the exact agent execution path (MCP / CLI / API), the authoritative source, and a confidence flag. Cross-references the bundled skill packs in `skills/`.

Confidence legend:
- ✓ — direct execution path, free or generous free tier, no manual intervention
- ⚠ — direct execution path but requires user-supplied API key or paid tier
- ✗ — execution requires manual user step or a paywalled portion the agent cannot fully automate

---

## General topic investigation

- **SOTA approach:** Triangulate Perplexity Sonar Pro / Sonar Deep Research (F=0.858 SimpleQA factuality, multi-step retrieval + synthesis) with Exa.ai neural search (sub-200ms, semantic) and Brave/DDG keyword backstop. Use Claude Opus 4.7 extended thinking to reconcile contradictions.
- **Agent execution path:** `cli-anything` → `curl https://api.perplexity.ai/chat/completions` with model `sonar-pro` or `sonar-deep-research`. `cli-anything` → `pip install exa-py` + `Exa(api_key).search_and_contents(q, type='neural')`. Cross-validate via `brave-search` / `duckduckgo-search` and `gemini` MCP. See `skills/perplexity-deep-research/`, `skills/exa-neural-search/`.
- **Source:** https://docs.perplexity.ai/docs/sonar/models/sonar-deep-research · https://exa.ai/
- **Confidence:** ⚠ (Perplexity + Exa keys; both have generous free tiers)

## Market research (TAM / SAM / SOM, segmentation, opportunity)

- **SOTA approach:** SEC EDGAR XBRL `companyfacts` for line-item revenue / segment data from 10-K filings (free, 10 rps); Crunchbase API for company / funding / exec data; Similarweb free API for traffic share; pytrends for demand signal; OpenAlex / Semantic Scholar for academic market sizing studies.
- **Agent execution path:** `sec-edgar-mcp` → CIK lookup → `curl https://data.sec.gov/api/xbrl/companyfacts/CIK{10digit}.json`. `cli-anything` → `curl -H "X-cb-user-key:$KEY" https://api.crunchbase.com/api/v4/searches/organizations`. `cli-anything` → `pip install pytrends` + `TrendReq().interest_over_time()`. See `skills/sec-edgar-market-sizing/`, `skills/crunchbase-market-research/`.
- **Source:** https://www.sec.gov/edgar/sec-api-documentation · https://data.crunchbase.com/docs/using-the-api · https://github.com/DaWe35/Similarweb-free-API
- **Confidence:** ⚠ (SEC EDGAR free; Crunchbase paid $49/mo Basic; Similarweb free tier limited)

## Competitive intelligence (SWOT, benchmarking, monitoring)

- **SOTA approach:** SEC EDGAR for financials, Lens.org Patent API for IP positioning, USPTO PatentsView for trend signals, Wappalyzer for competitor tech stack, GitHub repo intel for engineering signals, playwright-mcp for pricing-page scrape.
- **Agent execution path:** `sec-edgar-mcp` for financials. `uspto-mcp` + `cli-anything` → `curl -H "Authorization: Bearer $LENS_TOKEN" https://api.lens.org/patent/search`. `cli-anything` → `pip install python-Wappalyzer` for tech stack detection. `github-api` for repo/commit/contributor analysis. `playwright-mcp` for JS-rendered pricing pages. See `skills/competitive-intelligence-tech-stack/`, `skills/patents-uspto-lens/`.
- **Source:** https://docs.api.lens.org/ · https://data.uspto.gov/apis/getting-started · https://www.wappalyzer.com/
- **Confidence:** ✓ (all primary tools have free or free-non-commercial tiers)

## Trend analysis (weak-signal detection, 8 source types)

- **SOTA approach:** Fan out across 8 source types in parallel: pytrends (search), HN Algolia (tech discourse), PRAW Reddit (community), GDELT 2.0 DOC API (global news in 65 languages, 3-month rolling), USPTO + Lens (patents), arXiv + OpenAlex (academic leading indicators), `ai-news-collectors` (general news), YouTube MCP (video). Cross-validate signal across ≥3 independent sources before declaring a trend.
- **Agent execution path:** Parallel calls: `cli-anything` → `pip install pytrends praw gdeltdoc`. `reddit-mcp` for community signal. `cli-anything` → `curl https://hn.algolia.com/api/v1/search?query=X`. `uspto-mcp` + Lens.org for patents. arXiv via Paper Search MCP. `youtube-mcp`. `ai-news-collectors`. See `skills/trend-fan-out-multi-source/`, `skills/gdelt-news-monitoring/`.
- **Source:** https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/ · https://hn.algolia.com/api · https://github.com/GeneralMills/pytrends
- **Confidence:** ✓ (all free; Reddit PRAW 60 rpm, arXiv 1 req / 3s)

## Scientific literature review

- **SOTA approach:** Paper Search MCP (single install wraps arXiv + PubMed + bioRxiv + medRxiv + Google Scholar + Semantic Scholar + CrossRef + OpenAlex + PMC + CORE + Europe PMC + dblp + OpenAIRE + SSRN + Unpaywall — 20+ sources). Layer scite.ai for citation context (supporting vs contradicting classification across 1.2B citations). Use ClinicalTrials.gov v2 for medical evidence. Mistral / Gemini OCR for scanned-only PDFs.
- **Agent execution path:** `cli-anything` → install `openags/paper-search-mcp`. Direct API access via `cli-anything` → `curl https://api.semanticscholar.org/graph/v1/paper/search?query=X` (1000 rps unauth). `curl https://api.openalex.org/works?search=X&filter=publication_year:>2024`. `curl https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=X`. `curl https://clinicaltrials.gov/api/v2/studies?query.cond=X`. `mistral-ocr-mcp` / `gemini-ocr-mcp` for image-only PDFs. See `skills/paper-search-mcp/`, `skills/semantic-scholar-openalex/`, `skills/ocr-scanned-academic-papers/`.
- **Source:** https://mcpservers.org/servers/openags/paper-search-mcp · https://www.semanticscholar.org/product/api · https://docs.openalex.org/api-entities/works/search-works
- **Confidence:** ✓ (all free or generous unauthenticated tiers; scite.ai requires paid key)

## Data research (discovery, collection, validation)

- **SOTA approach:** Kaggle CLI for community datasets, Hugging Face Datasets for ML benchmarks, FRED (816k+ economic series), World Bank + IMF + OECD SDMX-JSON + Eurostat + BLS APIs for authoritative time series. Use `lifelines` for survival / retention modeling, `pandas` for joins / cleaning.
- **Agent execution path:** `cli-anything` → `pip install kaggle datasets fredapi wbdata pandas`. `huggingface-mcp` for HF discovery. `kaggle datasets download -d X`. `Fred(api_key).get_series('GDP')`. `wbdata.get_dataframe({'NY.GDP.MKTP.CD':'gdp'})`. See `skills/kaggle-huggingface-datasets/`, `skills/authoritative-data-fred-worldbank/`.
- **Source:** https://fred.stlouisfed.org/docs/api/fred/ · https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation · https://huggingface.co/docs/datasets/index · https://pypi.org/project/kaggle/
- **Confidence:** ✓ (FRED free key; World Bank no key; Kaggle requires API token file; HF no key for public datasets)

## Targeted search / information retrieval (precision > 90%)

- **SOTA approach:** Brave/DDG with Boolean operators (`AND`/`OR`/`NOT`/`""`/site:/filetype:); Exa.ai neural with `includeDomains` whitelist + `excludeDomains` blacklist + `useAutoprompt`; OpenAlex filter DSL for academic precision (`filter=publication_year:>2024,authorships.author.id:A123`).
- **Agent execution path:** `brave-search` + `duckduckgo-search` for Boolean. `cli-anything` → `Exa(api_key).search_and_contents(q, type='neural', includeDomains=['nature.com','science.org'])`. `cli-anything` → `curl 'https://api.openalex.org/works?search=...&filter=...'`. See `skills/exa-neural-search/`, `skills/semantic-scholar-openalex/`.
- **Source:** https://docs.exa.ai/ · https://docs.openalex.org/how-to-use-the-api/filter-entity-lists
- **Confidence:** ⚠ (Exa key required; OpenAlex / Brave / DDG free)

## First-principles thinking

- **SOTA approach:** Claude Opus 4.7 extended thinking (low/medium/high/max effort) for the 5-step decomposition (define / assumptions / challenge / extract / rebuild). Gemini MCP adversarial cross-check ("what's wrong with this reasoning chain?"). Kialo argument trees for structured pro/con if user-facing.
- **Agent execution path:** Self (Claude Opus 4.7) with `extended_thinking` effort knob — start at `medium`, escalate to `high` / `max` if the reasoning chain is novel. `gemini` MCP for second-opinion adversarial review. `concise-planning` + `brainstorming` skills for divergent generation. See `skills/first-principles-claude-extended/`.
- **Source:** https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking
- **Confidence:** ✓ (self-hosted reasoning + Gemini MCP already enabled)

## Cohort analysis (N-day retention, Aha Moment, retention curves)

- **SOTA approach:** PostHog cohorts endpoint for live cohort fetch / HogQL queries; `lifelines` Kaplan-Meier survival analysis for retention curves with confidence intervals; pandas pivot for cohort retention tables; `postgresql-mcp` for raw event-table joins when product analytics is unavailable.
- **Agent execution path:** `posthog-mcp` → cohorts endpoint or `cli-anything` → `curl -H "Authorization: Bearer $KEY" https://app.posthog.com/api/projects/{id}/cohorts/`. `cli-anything` → `pip install lifelines` + `KaplanMeierFitter().fit(durations, events).plot_survival_function()`. `postgresql-mcp` for raw event queries. See `skills/cohort-retention-lifelines/`.
- **Source:** https://posthog.com/docs/api/cohorts · https://lifelines.readthedocs.io/
- **Confidence:** ✓ (PostHog free tier 1M events/mo; lifelines free)

## KPI framework design (SMART, 3-tier, 5-7 KPI limit, dynamic thresholds)

- **SOTA approach:** LLM-driven framework synthesis using the `kpi-dashboard-design` skill pack (already bundled). Pandas quantile on historical baselines via `postgresql-mcp` for dynamic threshold derivation (rolling mean ± k·σ instead of static cutoffs).
- **Agent execution path:** `kpi-dashboard-design` skill for framework. `concise-planning` + `brainstorming` for KPI candidate generation. `postgresql-mcp` + `cli-anything` (pandas) for baseline quantile computation. See `skills/kpi-dashboard-design/` (existing).
- **Source:** Existing skill pack (wshobson business-analytics).
- **Confidence:** ✓

## Data storytelling

- **SOTA approach:** Plotly (interactive HTML/PNG via `kaleido`), Altair / Vega-Lite (declarative grammar of graphics), matplotlib + seaborn (publication-grade static), Mermaid CLI for diagrams, Datawrapper API ($799+/mo) for embed-grade. Use `data-storytelling` skill pack (Setup → Conflict → Resolution, "start with so-what").
- **Agent execution path:** `data-storytelling` skill (existing). `cli-anything` → `pip install plotly altair matplotlib seaborn kaleido`. `cli-anything` → `npm i -g @mermaid-js/mermaid-cli` + `mmdc -i diagram.mmd -o diagram.png`. See `skills/data-storytelling-plotly-altair/`.
- **Source:** https://plotly.com/python/ · https://altair-viz.github.io/ · https://www.datawrapper.de/
- **Confidence:** ✓ (all open-source; Datawrapper paid optional)

## Deliverables (briefing / report / trend / CI / market / scientific syntheses)

- **SOTA approach:** Pandoc with `--reference-doc=template.docx` for branded DOCX; `--pdf-engine=xelatex` for PDF; `pptx` template via Pandoc + `--reference-doc=template.pptx` or `python-pptx`; `xlsx` for cohort / comparison tables. Mermaid CLI for diagrams embedded in markdown.
- **Agent execution path:** `cli-anything` → `pandoc report.md -o report.docx --reference-doc=template.docx`. Existing `docx` / `pdf` / `pptx` / `xlsx` MCPs for primitives. `git-commit` for version iteration. See `skills/pandoc-branded-deliverables/`.
- **Source:** https://pandoc.org/MANUAL.html
- **Confidence:** ✓

---

## Summary table (≥95% fulfillment)

| Use case | SOTA mechanism (primary) | Path | Confidence |
|---|---|---|---|
| General topic investigation | Perplexity Sonar Deep Research + Exa neural + Claude extended thinking | `cli-anything` curl + `gemini` cross-check | ⚠ |
| Market research | SEC EDGAR XBRL + Crunchbase + Similarweb + pytrends | `sec-edgar-mcp` + `cli-anything` | ⚠ |
| Competitive intelligence | SEC EDGAR + USPTO + Lens.org + Wappalyzer + GitHub | `sec-edgar-mcp` + `uspto-mcp` + `cli-anything` + `github-api` | ✓ |
| Trend analysis | pytrends + HN Algolia + PRAW + GDELT + USPTO + arXiv | `cli-anything` + `reddit-mcp` + `uspto-mcp` | ✓ |
| Scientific literature | Paper Search MCP (20+ sources) + scite.ai + ClinicalTrials.gov v2 | `cli-anything` (`openags/paper-search-mcp`) + `google-scholar-mcp` | ✓ |
| Data research | Kaggle CLI + HF Datasets + FRED + World Bank + IMF + OECD + BLS | `huggingface-mcp` + `cli-anything` | ✓ |
| Targeted search | Boolean + Exa `includeDomains` + OpenAlex filter DSL | existing search MCPs + `cli-anything` | ⚠ |
| First-principles | Claude Opus 4.7 extended thinking + Gemini adversarial | self + `gemini` MCP | ✓ |
| Cohort analysis | PostHog cohorts + lifelines Kaplan-Meier + pandas | `posthog-mcp` + `cli-anything` | ✓ |
| KPI framework | `kpi-dashboard-design` skill + pandas quantile baselines | bundled skill + `postgresql-mcp` + `cli-anything` | ✓ |
| Data storytelling | Plotly + Altair + matplotlib + Mermaid + Datawrapper | `data-storytelling` skill + `cli-anything` | ✓ |
| Deliverables | Pandoc `--reference-doc` + docx/pdf/pptx/xlsx MCPs | `cli-anything` Pandoc + MCPs | ✓ |
| Foreign-language sources | DeepL MCP | `deepl-mcp` | ✓ |
| Scanned PDFs | Mistral / Gemini OCR | `mistral-ocr-mcp` + `gemini-ocr-mcp` | ✓ |

**Estimated fulfillment: ~96%.** Remaining 4% gaps:

| Gap | Mitigation |
|---|---|
| Statista / IBISWorld paywall | `firecrawl-mcp` / `brightdata-mcp` for public portions; flag in limitations |
| Crunchbase Pro / Datawrapper Enterprise | Free tiers / fallback to SEC EDGAR + Similarweb-free + Plotly |
| Real-time financial market data | Out of scope (analyst designs metrics; eng builds dashboard) |

---

## How this maps to the bundled skill packs

| Use case | Primary skill pack(s) |
|---|---|
| General topic investigation | `perplexity-deep-research`, `exa-neural-search` |
| Market research | `sec-edgar-market-sizing`, `crunchbase-market-research` |
| Competitive intelligence | `competitive-intelligence-tech-stack`, `patents-uspto-lens` |
| Trend analysis | `trend-fan-out-multi-source`, `gdelt-news-monitoring` |
| Scientific literature | `paper-search-mcp`, `semantic-scholar-openalex`, `ocr-scanned-academic-papers` |
| Data research | `kaggle-huggingface-datasets`, `authoritative-data-fred-worldbank` |
| Targeted search | `exa-neural-search`, `semantic-scholar-openalex` |
| First-principles | `first-principles-claude-extended` |
| Cohort analysis | `cohort-retention-lifelines` |
| KPI framework | `kpi-dashboard-design` (existing) |
| Data storytelling | `data-storytelling-plotly-altair`, `data-storytelling` (existing) |
| Deliverables | `pandoc-branded-deliverables` |
