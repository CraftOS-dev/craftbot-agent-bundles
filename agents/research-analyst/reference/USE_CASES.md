# Research Analyst — Use Cases

**Tier:** general · **Category:** research
**Core job:** Investigate any topic, evaluate sources, synthesize across multiple angles, deliver actionable insights with full attribution.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### General topic investigation
- Any domain — technology, policy, science, business, social, economic
- Multi-source triangulation (never single-source for substantive claims)
- 5-dimension source evaluation (authority / currency / accuracy / purpose / methodology)
- 8-item bias detection checklist
- Quality-weighted synthesis with confidence levels

### Market research
- Market sizing (TAM / SAM / SOM)
- Consumer behavior analysis (5 segmentation typologies — demographic, psychographic, behavioral, geographic, needs-based)
- Competitive landscape mapping
- Opportunity identification (gap analysis, white spaces, growth segments)
- Strategic recommendations with ROI projections and risk adjustment

### Competitive intelligence
- Direct + indirect + potential-entrant + substitute competitor mapping
- SWOT analysis
- Public-information only (ethical methods)
- Benchmarking dimensions (product, pricing, market share, financials, tech stack)
- Monitoring systems

### Trend analysis
- Weak-signal detection across 8 source types (social, search, patents, academic, news, expert, consumer behavior, etc.)
- Pattern validation
- Trajectory projection (linear, exponential, S-curve, oscillating)
- Scenario planning (best / base / worst / wildcard)
- Cross-impact analysis
- Trend report with confidence bands and timing estimates

### Scientific literature review
- Search via Google Scholar, PubMed, BGPT, domain databases
- Quality-weighted evidence (sample size, study design, replication status)
- Convergent vs contradictory findings
- Confidence-leveled conclusions (low / moderate / high)
- Limitations transparency

### Data research
- Discovery, collection, validation across sources
- Exploratory + statistical analysis
- Reproducibility requirements
- 10-item statistical rigor checklist

### Targeted search / information retrieval
- Boolean operators (AND / OR / NOT, parentheses, quotes)
- Proximity searching where supported
- Precision-rate target > 90%
- Document the search methodology so others can reproduce it

### First-principles thinking
- 5-step method (define / assumptions / challenge / extract / rebuild)
- Problem-statement reframing (weak → strong)
- 5D method for operational issues (Define / Diagnose / Diverge / Decide / Deploy)

### Cohort analysis
- Acquisition / behavioral / segment cohorts
- N-day and rolling retention metrics
- Retention curve diagnosis (healthy / declining / dying)
- Activation analysis ("Aha Moment" identification)

### KPI framework design
- 3-tier framework (strategic / tactical / operational)
- SMART criteria
- 5-7 KPI limit
- Dynamic thresholds vs static cutoffs

### Data storytelling
- Setup → Conflict → Resolution structure
- Start with the "so what"
- 3 elements: data (evidence) + narrative (meaning) + visuals (comprehension)

### Deliverables
- Executive briefings (1 page)
- Full research reports (long-form)
- Trend reports (headline + confidence + timing + indicators + monitoring)
- Competitive intelligence reports (SWOT + benchmark + monitoring)
- Market analyses (sizing + segments + opportunities + recommendations)
- Scientific syntheses (evidence-graded, confidence-leveled)

---

## Execution status (SOTA — June 2026)

The previous "Can execute the full research loop" verdict was true for general web research but missed major SOTA improvements: PubMed/arXiv/OpenAlex unified access via Paper Search MCP, SEC EDGAR + USPTO direct MCPs for market/patent intelligence, Perplexity Sonar Deep Research API (F=0.858 SimpleQA factuality), Exa.ai neural search, and free authoritative time-series APIs (FRED, World Bank, IMF, OECD). With the updated MCP stack + `cli-anything`, the agent can hit any of these.

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| General topic investigation | Perplexity Sonar Pro / Sonar Deep Research API + Exa neural search + Brave/DDG triangulation | `cli-anything` curl (Perplexity, $3/M-in; Exa, 1k free/mo) + existing search MCPs |
| Market research (TAM/SAM/SOM) | SEC EDGAR XBRL API (free, 10 rps) + Crunchbase API + Similarweb | `sec-edgar-mcp` + `cli-anything` curl (Crunchbase $49/mo, Similarweb-free-API) |
| Competitive intelligence (SWOT, benchmarking) | SEC EDGAR + Lens.org Patent API + Wappalyzer + GitHub repo intel | `sec-edgar-mcp` + `cli-anything` (Lens.org, Wappalyzer) + `github` MCP + `playwright-mcp` pricing scrape |
| Trend analysis (8 source types, weak signals) | pytrends + HN Algolia API (free) + PRAW Reddit (60 rpm) + GDELT 2.0 DOC API + USPTO PatentsView + arXiv | `cli-anything` (`pip install pytrends praw gdeltdoc`) + `reddit-mcp` + `uspto-mcp` |
| Scientific literature review | Paper Search MCP (wraps arXiv/PubMed/bioRxiv/medRxiv/Semantic Scholar/CrossRef/OpenAlex/PMC/CORE/Europe PMC/dblp/OpenAIRE/SSRN/Unpaywall — single install) + scite.ai citation context + Consensus.app | `cli-anything` (`openags/paper-search-mcp`) + `google-scholar-mcp` |
| Data research (discovery + validation) | Kaggle CLI + Hugging Face Datasets + FRED API (816k+ series) + World Bank / IMF / OECD / BLS APIs | `huggingface-mcp` + `cli-anything` (`pip install kaggle fredapi wbdata`) |
| Targeted search (>90% precision, Boolean) | Brave/DDG boolean operators + Exa.ai neural with `includeDomains`/`excludeDomains` + OpenAlex filter DSL | existing search MCPs + `cli-anything` curl (Exa, OpenAlex) |
| First-principles thinking | Claude Opus 4.7 extended thinking (low/medium/high/max effort) + `gemini` MCP adversarial cross-check + Kialo argument trees | self + `gemini` + `concise-planning`/`brainstorming` skills |
| Cohort analysis (N-day retention, Aha Moment, retention curves) | PostHog API + `postgresql-mcp` + `lifelines` (Kaplan-Meier) for survival curves | `posthog-mcp` (cohorts endpoint) + `postgresql-mcp` + `cli-anything` (`pip install lifelines`) |
| KPI framework design (SMART, 3-tier, 5-7 limit, dynamic thresholds) | LLM reasoning + pandas quantile on historical baselines via `postgresql-mcp` | `concise-planning` + `brainstorming` + `postgresql-mcp` + `cli-anything` (pandas) |
| Data storytelling | Plotly + Altair / Vega-Lite + matplotlib + Datawrapper API + Mermaid CLI for diagrams + Pandoc for branded DOCX | `data-storytelling` skill + `cli-anything` (`pip install plotly altair kaleido`, `mmdc`, `pandoc`) |
| Deliverables (briefing, report, trend, CI, market, scientific) | `docx`/`pdf`/`pptx`/`xlsx` + Pandoc templates with `--reference-doc=template.docx` | existing MCPs + `cli-anything` Pandoc + `git-commit` for version iteration |
| Survey research (bonus, not in original list) | Typeform API / Google Forms API + webhooks | `cli-anything` curl |
| Foreign-language source synthesis | DeepL MCP for high-quality translation | `deepl-mcp` |
| Scanned PDF / image-only paper extraction | Mistral OCR / Gemini OCR for non-OCR'd academic PDFs | `mistral-ocr-mcp` + `gemini-ocr-mcp` |

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Crunchbase company/funding data | ⚠ | Free tier killed 2025; requires paid key ($49/mo Basic, $99/mo Pro) — recipient provides |
| Similarweb traffic data (deep) | ⚠ | Free API tier limited (`DaWe35/Similarweb-free-API`); commercial-grade requires paid subscription |
| Perplexity / Exa API keys | ⚠ | Both have generous free tiers; deep research workloads require paid plans |
| Some statistical databases (Statista, IBISWorld) | ⚠ | Paywalled; agent uses `firecrawl-mcp` or `brightdata-mcp` for what's publicly accessible |

**Verdict (June 2026): ~95% fulfillment.** The agent now closes the previously-flagged gaps for PubMed/arXiv/patents/datasets/cohort analysis with native MCPs and free APIs. Only paywalled premium business-intelligence (Crunchbase Pro, Statista, IBISWorld) require the user to provide a key — and the agent has fallback paths via `firecrawl-mcp`/`brightdata-mcp`/`playwright-mcp` for public portions.

---

## When to use this agent

- "Research the state of X market in 2026"
- "What's our competitive position vs Y?"
- "Find me the latest peer-reviewed evidence on Z"
- "Identify three emerging trends in [industry]"
- "Help me think through this problem from first principles"
- "Build a cohort analysis from this user data"
- "Design a KPI framework for our SaaS"
- "What do the analytics tell us about retention?"
- "Investigate this claim — is it supported by evidence?"

## When NOT to use this agent

- Implementation work (writing code based on research) — hand off to `senior-python-engineer`
- Writing marketing copy based on research — hand off to `marketing-agent`
- Producing documentation from research — hand off to `technical-writer`
- Real-time data dashboards / BI tool builds — flag as out of scope (analyst designs the metrics; engineer builds the dashboard)
- Insider / private-data acquisition — refuse; ethical methods only
