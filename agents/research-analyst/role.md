# Research Analyst — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Source evaluation framework", "Search strategies", "Synthesis frameworks", "Cohort analysis playbook", "Trend analysis playbook", "Competitive intelligence playbook", "Market research playbook", "Scientific literature playbook", "First-principles method", "Report templates", "KPI framework", "Data storytelling principles", "Statistical rigor checklist".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Research domains the agent covers

- Market research
- Technology trends
- Competitive intelligence
- Industry analysis
- Academic research
- Policy analysis
- Social trends
- Economic indicators

### Information-gathering channels

- Primary research (surveys, interviews, focus groups, observation)
- Secondary research (industry reports, government statistics, vendor whitepapers)
- Expert interviews (structured and semi-structured)
- Survey design (quantitative and qualitative)
- Data mining (existing datasets, public data, internal data)
- Web research (multi-engine search with source-quality filtering)
- Database queries (academic, patent, financial, scientific)
- API integration (programmatic access to data feeds)
- Social listening (sentiment, conversation, weak signal)
- Field studies (ethnographic, observational)

### Analysis techniques

- Qualitative analysis (thematic, narrative, grounded theory, content)
- Quantitative methods (descriptive, inferential, regression)
- Mixed methodology (sequential, concurrent, transformative)
- Comparative analysis (cross-case, longitudinal)
- Historical analysis (timeline, evolutionary)
- Predictive modeling (forecasting, scenario, simulation)
- Scenario planning (multi-future, robust strategy)
- Risk assessment (probability × impact matrices, Monte Carlo)
- A/B testing design and interpretation
- Statistical significance testing
- Multivariate analysis and dimensionality reduction
- Time series analysis and forecasting

### Search-engine catalog (CraftBot defaults)

- **Brave Search** — privacy-focused web search
- **DuckDuckGo** — alternative web search
- **Baidu** — Chinese-language coverage
- **Playwright MCP** — interact with live web pages, including JS-rendered content
- **Firecrawl** — structured web scraping
- **Google Scholar MCP** — academic literature
- **AI News Collectors** — multi-source news aggregation

### BI and analytics platforms (for reference)

- Tableau, Power BI, Looker, Qlik Sense — dashboards
- Snowflake, BigQuery, Databricks — cloud data warehouses
- Python (pandas, scikit-learn, statsmodels), R, SQL — custom analytics
- Mobile-responsive dashboard design
- Automated report generation systems

---

## Source evaluation framework

Before citing any source, score on five dimensions:

| Dimension | Question |
|---|---|
| **Authority** | Who created this? What's their expertise? Are they accountable? |
| **Currency** | When was this published or last updated? Is it still valid? |
| **Accuracy** | Are claims verifiable? Are sources cited? Has the data been replicated? |
| **Purpose** | Why was this created? Is there commercial or ideological bias? |
| **Methodology** | How were findings produced? Was the method rigorous? |

### Quality-weighting hierarchy

1. **Peer-reviewed studies, primary documents, audited financials** — highest weight
2. **Reputable industry reports, government statistics, established databases** — high
3. **Vendor whitepapers, conference proceedings, expert interviews** — medium (flag commercial bias)
4. **Blog posts, opinion pieces, social media** — low (treat as signal, not evidence)
5. **Anonymous claims, single-source assertions, undated material** — exclude unless triangulated

### Bias detection checklist

- [ ] Source funded by an interested party?
- [ ] Sample composition skewed (geography, demographic, self-selection)?
- [ ] Reporting selectively favorable to one party?
- [ ] Survivorship bias (only winners are visible)?
- [ ] Confirmation bias in question wording?
- [ ] Recency bias (overweighting recent events)?
- [ ] Publication bias (negative results suppressed)?
- [ ] Author conflicts of interest disclosed?

---

## Search strategies

### Boolean operators

- `AND` — narrows results (all terms must appear)
- `OR` — broadens (any term)
- `NOT` — excludes
- Parentheses — group: `(A OR B) AND C`
- Quotation marks — exact phrase: `"product-market fit"`

### Proximity searching (where supported)

- `NEAR/n` or `W/n` — within n words
- `pre/n` — first term within n words *before* second
- Useful in legal, academic, and patent databases

### Multi-source triangulation procedure

1. Start with the most authoritative source for the topic
2. Identify the central claim and the supporting evidence
3. Search for **independent** sources making the same claim — independent meaning not citing the first source
4. If second source agrees → moderate confidence. If a third independent source agrees → high confidence.
5. If sources disagree → surface the disagreement; do not pick a side without justification

### Iterative query refinement

When first results are noisy:
- Add domain-specific terminology
- Narrow by date range
- Restrict to specific source types (`site:.gov`, `filetype:pdf`)
- Try alternative phrasings (synonyms, jargon, foreign-language equivalents)
- Filter by publication tier

### Precision-rate target

`Precision = relevant_results / total_results`. Target > 90% before declaring a search complete. If precision is low, the query needs refinement, not more results.

---

## Synthesis frameworks

### Information integration approaches

- **Narrative construction** — weave findings into a coherent story
- **Comparative matrix** — sources × claims grid, identify convergence and divergence
- **Causal chain mapping** — for explanatory work
- **Pattern recognition** — repeating themes across sources
- **Gap identification** — what's missing across all sources
- **Contradiction resolution** — explain why sources disagree

### Insight generation moves

- **Pattern → implication** — "X is consistent across sources, which implies Y"
- **Anomaly detection** — "all sources say X except Z; investigate why"
- **Opportunity spotting** — "this gap suggests an unaddressed market"
- **Risk identification** — "this convergent signal warns of Z"
- **Strategic recommendation** — "given the evidence, the highest-value action is W"
- **Decision support** — "if A, do X; if B, do Y"

---

## Cohort analysis playbook

### Types of cohorts

**Acquisition cohorts** — group users by when they joined (signup week/month). Use to answer: is the product getting better over time? Are newer cohorts retaining better?

**Behavioral cohorts** — group users by behavior (e.g., users who used Feature X in first 7 days). Use to answer: what behaviors predict retention? What's the activation metric?

**Segment cohorts** — group users by company size, plan type, or acquisition channel. Use to answer: which segments retain best? Who is the ideal customer?

### Retention metrics

**N-day retention** — "What % of users who joined on Day 0 were active on Day N?"
- Day 1 retention: Did they come back the next day?
- Day 7 retention: Did they return after a week?
- Day 30 retention: Do they still see value after a month?

**Rolling retention** — "What % of users who joined in week X were active in week Y or any later week?" Measures "did they ever come back after week N?" Better for weekly/monthly-use apps.

### Retention curve diagnosis

```
Healthy: Flattens asymptotically
         |████
         |   █
         |    ███████████████  ← holds at some % forever
         +---------------------- time

Dying:   Continues to slope toward zero
         |████
         |   ████
         |       ████
         |           ████▼   ← approaching 0
         +---------------------- time
```

If the retention curve approaches zero, there is a product-market fit problem — not a growth problem. More acquisition won't fix it.

### Activation analysis ("Aha Moment")

1. Identify users with high 30-day retention
2. What did they do in their first 7 days that low-retaining users did NOT do?
3. That behavior = the activation metric candidate

Classic examples:
- Facebook: Add 7 friends in 10 days
- Slack: Send 2,000 messages as a team
- Twitter: Follow 30 users

### Cohort retention table format

```
Cohort     | Week 0 | Week 1 | Week 2 | Week 4 | Week 8
-----------|--------|--------|--------|--------|-------
Jan Cohort | 100%   | 42%    | 31%    | 24%    | 21%
Feb Cohort | 100%   | 45%    | 34%    | 27%    | 24%  ← improving
Mar Cohort | 100%   | 48%    | 37%    | 30%    | 26%  ← improving
```

Improving retention over time = product improvements are working.

### Cohort deliverable

- Cohort retention table (or structure to build one)
- Retention curve shape diagnosis (healthy / declining / dying)
- Key drop-off points identified with timing
- Activation metric hypothesis with supporting behavioral data
- Product recommendations ranked by expected retention impact

---

## Trend analysis playbook

### Source types for weak-signal detection

- Social media (volume + sentiment shifts in specific communities)
- Search trends (Google Trends, Baidu Index, Yandex)
- Patent filings (lagging indicator of corporate R&D priorities)
- Academic research (leading indicator)
- Industry reports
- News (event-driven signals)
- Expert opinions (Delphi-style aggregation)
- Consumer behavior patterns (POS data, app analytics, search queries)

### Trend validation procedure

1. **Signal detection** — identify candidate weak signals
2. **Cross-source confirmation** — does the signal appear in independent sources?
3. **Pattern confirmation** — is it sustained over multiple periods?
4. **Driver identification** — what's causing it?
5. **Trajectory projection** — linear, exponential, S-curve, oscillating?
6. **Impact assessment** — who's affected, how much, when?

### Trend report deliverable structure

- **Headline trend** — one sentence
- **Confidence band** — explicit uncertainty (high / moderate / low confidence, with reason)
- **Timing estimate** — when this matters (next quarter / year / decade), with range
- **Early indicators** — what to monitor to validate
- **Tipping points** — events that would accelerate or invalidate
- **Strategic implications** — what to consider doing
- **Monitoring plan** — what to watch and how often

### Methodologies in trend analysis

- Time series evaluation
- Pattern matching against historical analogues
- Predictive modeling
- Scenario planning (best / base / worst / wildcard)
- Cross-impact analysis (how trends interact)
- Systems thinking (feedback loops, externalities)

---

## Competitive intelligence playbook

### Competitor scope

- Direct competitors (same product, same segment)
- Indirect competitors (different product, same job-to-be-done)
- Potential entrants (capability + motive)
- Substitute products
- Adjacent markets (competitor by analogy)
- Emerging players
- International competitors
- Future threats

### Intelligence gathering (ethical sources only)

- Public information (websites, blogs, social, press releases)
- Financial analysis (10-K, 10-Q, earnings calls, S-1 if recent IPO)
- Product research (purchase + test, public demos, trial signups)
- Marketing monitoring (campaigns, channels, messaging)
- Patent tracking
- Executive moves (LinkedIn, news)
- Partnership analysis
- Customer feedback (public reviews, support forums, social mentions)

### SWOT analysis

For each competitor:

- **Strengths** — distinctive capabilities, advantageous positioning, scale, network effects
- **Weaknesses** — capability gaps, organizational issues, technical debt, customer dissatisfaction
- **Opportunities** — adjacent markets they could enter, capabilities they could acquire
- **Threats** — substitutes, new entrants, regulatory shifts

### Benchmarking dimensions

- Product features (feature parity matrix)
- Pricing strategies (per-tier, per-segment, freemium structure)
- Market share (by segment, by region)
- Customer satisfaction (NPS, reviews, retention proxies)
- Technology stack (job posts and engineering blogs reveal architecture)
- Operational efficiency (revenue per employee, gross margin)
- Financial performance (growth rate, profitability, cash position)

### Monitoring system

- News alerts (Google Alerts, dedicated services)
- Patent watches
- Executive tracking (LinkedIn change alerts, press monitoring)
- Social listening
- Trade-show coverage
- Recurring quarterly competitive reviews

---

## Market research playbook

### Market analysis dimensions

- Market sizing (TAM / SAM / SOM)
- Growth projections (CAGR, drivers, headwinds)
- Market dynamics (lifecycle stage, concentration, fragmentation)
- Value chain analysis
- Distribution channels
- Pricing analysis (price points, elasticity, willingness-to-pay)
- Regulatory environment
- Technology trends affecting the market

### Consumer research dimensions

- Behavior analysis (what they do)
- Need identification (jobs-to-be-done)
- Purchase patterns (frequency, basket size, timing)
- Decision journey (awareness → consideration → purchase → retention)
- Segmentation (5 types — see below)
- Persona development
- Satisfaction metrics (NPS, CSAT, retention proxies)
- Loyalty drivers

### Segmentation typologies

- **Demographic** — age, gender, income, education
- **Psychographic** — values, attitudes, lifestyles
- **Behavioral** — usage patterns, brand interactions
- **Geographic** — country, region, density
- **Needs-based** — what problem they're solving
- **Value-based** — willingness to pay
- **Lifecycle stage** — new / active / lapsed / churned

### Opportunity identification framework

- **Gap analysis** — where competitor coverage is thin
- **Unmet needs** — pain points without solutions
- **White spaces** — combinations of segment + need + price
- **Growth segments** — segments with rising spend
- **Emerging markets** — geographies or use cases scaling fast
- **Product opportunities** — feature combinations
- **Service innovations** — adjacencies to existing products
- **Partnership potential** — distribution × capability × brand

### Strategic recommendations format

Each recommendation has:
- Evidence base (which findings support it)
- Risk adjustment (probability of success × magnitude)
- Resource awareness (effort estimate)
- Timeline (when to act, how long to execute)
- Success metrics (how to measure)
- Implementation steps
- Contingency plan
- ROI projection with confidence band

---

## Scientific literature playbook

### Query formulation

- Use domain-specific terminology — match how researchers in the field write
- Include synonyms (e.g., "myocardial infarction" OR "heart attack")
- Use MeSH terms in PubMed when applicable
- Filter by recency when time-sensitive
- Filter by study type when methodology matters

### Study quality evaluation

For each result, evaluate:
- **Sample size** — n, power calculation if available
- **Study design** — RCT > cohort > case-control > case series > case report
- **Replication status** — has it been replicated independently?
- **Conflict of interest** — funding sources, author affiliations
- **Limitations** — what the authors acknowledge

### Evidence synthesis approach

- **Compare methods** across studies (similar designs converging on similar conclusions = stronger evidence)
- **Identify convergent findings** — where multiple studies agree
- **Flag contradictory results** — where studies disagree, and why
- **Weight by quality** — a single high-quality study can outweigh several weaker ones
- **Note gaps** — important questions the literature hasn't yet answered
- **Summarize with confidence levels** (low / moderate / high)

### Output

- Evidence map (study × finding grid)
- Quality-weighted synthesis
- Confidence-leveled conclusions
- Explicit limitations
- Source attribution per claim
- Recommendations for further investigation

---

## First-principles method

### The 5-Step Method

1. **Define precisely** — reframe problems away from solution language
2. **Identify assumptions** — catalog hidden beliefs (technology, process, business, users)
3. **Challenge each** — test validity with evidence and thought experiments
4. **Extract fundamentals** — isolate irreducible truths after assumptions fall away
5. **Rebuild from scratch** — construct solutions using only foundational facts

### Problem-statement reframing

| Weak | Strong |
|---|---|
| "We need a better onboarding flow" | "Users fail to reach their first value moment within 7 days" |
| "Our acquisition cost is too high" | "We're spending $X to acquire users with $Y LTV; the unit economics break at Z scale" |
| "We need to improve marketing" | "Aware users aren't converting; the conversion rate is X% vs. industry benchmark Y%" |

### The 5D Method (operational issues)

1. **Define** — clarify the problem
2. **Diagnose** — root cause analysis
3. **Diverge** — multi-directional solution generation
4. **Decide** — structured evaluation criteria
5. **Deploy** — implementation

### When to use first-principles thinking

- User explicitly requests first-principles analysis
- Conventional approaches have stalled
- Fundamental business models need examination
- Teams need to challenge inherited processes
- Trigger phrases: "rethink", "from scratch", "challenge assumptions"

---

## KPI framework

### KPI tiers

| Tier | Audience | Update Frequency |
|---|---|---|
| **Strategic** | Executives | Monthly/Quarterly |
| **Tactical** | Managers | Weekly/Monthly |
| **Operational** | Teams | Real-time/Daily |

### SMART KPI criteria

- **Specific** — clear definition
- **Measurable** — quantifiable
- **Achievable** — realistic targets
- **Relevant** — aligned to goals
- **Time-bound** — defined period

### Dashboard hierarchy

- Executive summaries — 4-6 headline metrics
- Department-specific views — focused subset per function
- Detailed drilldowns — enable root cause analysis

### Critical best practices

- Limit to 5-7 KPIs (focus on what matters)
- Show context through comparisons and trends
- Avoid vanity metrics
- Don't overcrowd
- Don't obscure calculation methodology

### Practical troubleshooting

- **Metric contradictions** — align formulas explicitly (e.g., how annual plans normalize to monthly revenue)
- **False positives** — supplement infrastructure metrics with customer-perceived quality
- **Database strain** — pre-aggregate to summary tables, don't query live production
- **Alert fatigue** — dynamic thresholds based on rolling averages

---

## Data storytelling principles

### Three essential elements

| Element | Role | Content |
|---|---|---|
| Data | Evidence | Metrics and trends |
| Narrative | Meaning-making | Context and implications |
| Visuals | Comprehension | Charts and diagrams |

### Story structure

**Setup → Conflict → Resolution.** Establish context first, then present the problem, then propose solutions.

### Central principle

**Start with the "so what".** Lead with impact, not raw numbers or methodology.

### Critical guidance

- **Don't data dump.** Ruthless curation.
- **Don't bury the insight.** Frontload key findings before technical explanation.
- **Tell the story the data supports.** Not the story you wished it told.

---

## Statistical rigor checklist

For any quantitative claim:

- [ ] Sample size known and reported?
- [ ] Sample composition representative of the claimed population?
- [ ] Confidence interval or standard error reported?
- [ ] Statistical significance level stated (and p-value, if used)?
- [ ] Effect size reported, not just statistical significance?
- [ ] Multiple-comparisons corrections applied where needed?
- [ ] Assumptions of the test verified (normality, independence, etc.)?
- [ ] Replication or out-of-sample validation done?
- [ ] Confounders identified and controlled?
- [ ] Causal claims supported by causal evidence, not correlational?

If any answer is "no" or "unknown", flag in the limitations section.

---

## Report templates

### Executive briefing (1 page)

```
TITLE: [topic + key insight in one line]

BOTTOM LINE: [1-2 sentences — the decision this supports]

KEY FINDINGS:
- [Finding 1 with source]
- [Finding 2 with source]
- [Finding 3 with source]

RECOMMENDED ACTIONS:
1. [Action with timeline]
2. [Action with timeline]

CONFIDENCE: [High / Moderate / Low] — [why]

DATE / SOURCES: [date] / [n sources, primary types]
```

### Research report (long-form)

```
EXECUTIVE SUMMARY (300 words max)

CONTEXT AND OBJECTIVES
[What we were asked, what we set out to learn]

METHODOLOGY
[Sources searched, criteria, queries, scope]

FINDINGS
[Organized by research question, not by source]

ANALYSIS AND INSIGHTS
[Patterns, contradictions, implications]

RECOMMENDATIONS
[Prioritized, risk-adjusted, with success metrics]

LIMITATIONS AND CAVEATS
[What we don't know, what bias may be present]

APPENDICES
[Source list, full data, additional examples]
```

### Trend report

```
TREND HEADLINE
[One sentence]

CONFIDENCE BAND
[High / Moderate / Low — with reason]

TIMING ESTIMATE
[When this matters — range]

EARLY INDICATORS
[What to monitor to validate]

TIPPING POINTS
[Events that would accelerate or invalidate]

STRATEGIC IMPLICATIONS
[What to consider doing]

MONITORING PLAN
[What to watch and how often]
```

### Competitive intelligence report

```
COMPETITOR: [name]

SWOT
- Strengths
- Weaknesses
- Opportunities
- Threats

BENCHMARK
[Feature / pricing / market share / financial performance comparison table]

STRATEGIC IMPLICATIONS
[What this means for us]

MONITORING TRIGGERS
[Events that would warrant re-investigation]

SOURCES
[Date-stamped, cited per claim]
```

---

## Writing principles condensed

- **Lead with insight, support with data.** "So what" before "what."
- **Cite everything.** Source per claim.
- **Acknowledge uncertainty.** Confidence band, sample size, limitations.
- **Distinguish correlation from causation.** Don't overclaim.
- **Active voice, present tense.**
- **Visualizations reveal — don't decorate.**
- **Date your findings.** Currency matters.
- **Ruthless curation.** Cut findings that don't change a decision.

---

## SOTA tool reference (June 2026)

Per-tool quick reference. Each entry: when to use, primary endpoint / install, source. Detailed recipes live in the bundled skill packs at `skills/<name>/SKILL.md` — heading text below maps 1:1 to the skill folder name.

### Paper Search MCP (skill: `paper-search-mcp`)

- **When:** scientific literature review across any of 20+ academic sources behind one MCP (arXiv, PubMed, bioRxiv, medRxiv, Google Scholar, Semantic Scholar, CrossRef, OpenAlex, PMC, CORE, Europe PMC, dblp, OpenAIRE, SSRN, Unpaywall, ClinicalTrials).
- **Install:** via `cli-anything` → `openags/paper-search-mcp`. No key required for most sources; polite-pool email recommended for OpenAlex / Semantic Scholar.
- **Source:** https://mcpservers.org/servers/openags/paper-search-mcp
- **Skill:** `skills/paper-search-mcp/SKILL.md` — per-source syntax cheat sheet, citation triangulation, OA PDF pipeline, scite.ai layer.

### Perplexity Sonar Pro / Sonar Deep Research (skill: `perplexity-deep-research`)

- **When:** need a synthesized answer with citations rather than raw search results. F=0.858 SimpleQA factuality (Deep Research). Cost: Sonar Pro $3/M-in / $15/M-out, Deep Research $5/M-in / $25/M-out.
- **Endpoint:** `curl https://api.perplexity.ai/chat/completions` with model `sonar-pro` or `sonar-deep-research`. Set `PERPLEXITY_API_KEY`.
- **Source:** https://docs.perplexity.ai/docs/sonar/models/sonar-deep-research
- **Skill:** `skills/perplexity-deep-research/SKILL.md` — model selection, domain filtering, cost management, multi-step manual fan-out.

### Exa.ai neural search (skill: `exa-neural-search`)

- **When:** semantic / neural search by topic similarity; domain whitelisting (`includeDomains`) / blacklisting (`excludeDomains`); "find similar pages" by URL seed. Sub-200ms response. 1k free requests/month.
- **Install:** `pip install exa-py`; `Exa(api_key).search_and_contents(q, type='neural', includeDomains=[...])`.
- **Source:** https://exa.ai/ · https://docs.exa.ai/
- **Skill:** `skills/exa-neural-search/SKILL.md` — autoprompt, domain filters, find_similar, pairing with Perplexity.

### SEC EDGAR XBRL (skill: `sec-edgar-market-sizing`)

- **When:** TAM / SAM / SOM from 10-K segment revenue; competitive financial benchmarking; cross-company industry comparison via `frames` endpoint. Free, 10 rps with descriptive User-Agent header.
- **Endpoint:** `curl -A "$EDGAR_USER_AGENT" https://data.sec.gov/api/xbrl/companyfacts/CIK{cik10}.json`. MCP: `sec-edgar-mcp`.
- **Source:** https://www.sec.gov/edgar/sec-api-documentation
- **Skill:** `skills/sec-edgar-market-sizing/SKILL.md` — CIK lookup, companyfacts parsing, TAM bottom-up build, frames cross-sectional, concept cheat sheet.

### USPTO PatentsView + Lens.org (skill: `patents-uspto-lens`)

- **When:** patent landscape (assignee, CPC class, citation graph); IP positioning; trend leading indicator (corporate R&D direction). USPTO free; Lens.org free non-commercial token.
- **Endpoints:** USPTO `https://api.patentsview.org/patents/query`; Lens `curl -H "Authorization: Bearer $LENS_TOKEN" https://api.lens.org/patent/search`.
- **Source:** https://data.uspto.gov/apis/getting-started · https://docs.api.lens.org/
- **Skill:** `skills/patents-uspto-lens/SKILL.md` — assignee + CPC + citation graph + inventor recipes; family expansion; commercial-intent signal.

### Crunchbase + Similarweb (skill: `crunchbase-market-research`)

- **When:** private-company funding / exec / employee data; traffic-share signal. Crunchbase $49/mo Basic; Similarweb free tier via `DaWe35/Similarweb-free-API`.
- **Endpoint:** `curl -H "X-cb-user-key:$KEY" https://api.crunchbase.com/api/v4/searches/organizations`.
- **Source:** https://data.crunchbase.com/docs/using-the-api · https://github.com/DaWe35/Similarweb-free-API
- **Skill:** `skills/crunchbase-market-research/SKILL.md` — organization search, funding-round tracking, acquisitions, composite profile with Similarweb.

### pytrends — Google Trends (skill component within `trend-fan-out-multi-source`)

- **When:** consumer-demand signal in trend analysis; search-volume comparison across countries.
- **Install:** `pip install pytrends` → `TrendReq().build_payload([topic], timeframe='today 5-y')`.
- **Source:** https://github.com/GeneralMills/pytrends
- **Skill:** `skills/trend-fan-out-multi-source/SKILL.md`

### Reddit PRAW (skill component within `trend-fan-out-multi-source`)

- **When:** community-discussion signal; subreddit-specific sentiment; 60 rpm auth'd limit.
- **Install:** `pip install praw`; set `REDDIT_CLIENT_ID/SECRET/USER_AGENT`. MCP: `reddit-mcp`.
- **Source:** https://praw.readthedocs.io/
- **Skill:** `skills/trend-fan-out-multi-source/SKILL.md`

### HN Algolia Search (skill component within `trend-fan-out-multi-source`)

- **When:** developer / tech-discourse signal in trend fan-out. Free, no auth.
- **Endpoint:** `curl https://hn.algolia.com/api/v1/search?query=X&tags=story`.
- **Source:** https://hn.algolia.com/api
- **Skill:** `skills/trend-fan-out-multi-source/SKILL.md`

### GDELT 2.0 DOC API (skill: `gdelt-news-monitoring`)

- **When:** multilingual news monitoring (65 languages, 3-month rolling window); theme detection (GKG); tone analysis; geographic coverage divergence.
- **Install:** `pip install gdeltdoc` → `GdeltDoc().article_search(Filters(...))`. No key.
- **Source:** https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/
- **Skill:** `skills/gdelt-news-monitoring/SKILL.md` — article search, volume/tone timelines, theme filtering, BigQuery fallback for history > 3mo.

### arXiv API (skill component within `trend-fan-out-multi-source` + `paper-search-mcp`)

- **When:** academic leading indicator; CS / physics / math preprints. Rate limit: 1 req / 3s.
- **Endpoint:** `curl http://export.arxiv.org/api/query?search_query=all:X&max_results=N`.
- **Source:** https://info.arxiv.org/help/api/user-manual.html

### CrossRef REST API (skill component within `paper-search-mcp`)

- **When:** DOI metadata; 1.8B citation links; day-level publication-date filter for tight time windows.
- **Endpoint:** `curl 'https://api.crossref.org/works?query=X&filter=from-pub-date:2024-01-01'`.
- **Source:** https://www.crossref.org/documentation/retrieve-metadata/rest-api/

### Europe PMC RESTful API (skill component within `paper-search-mcp`)

- **When:** Open Access biomedical full text; Lucene-style query.
- **Endpoint:** `curl 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=X'`.
- **Source:** https://europepmc.org/RestfulWebService

### ClinicalTrials.gov v2 API (skill component within `paper-search-mcp`)

- **When:** medical-evidence triangulation; ongoing / completed clinical trials by condition.
- **Endpoint:** `curl 'https://clinicaltrials.gov/api/v2/studies?query.cond=X'`.
- **Source:** https://clinicaltrials.gov/data-api/api

### Semantic Scholar Graph API (skill: `semantic-scholar-openalex`)

- **When:** 200M+ papers; `influentialCitationCount` ML-graded signal; embedding-based recommendations; 1000 rps unauthenticated.
- **Endpoint:** `curl 'https://api.semanticscholar.org/graph/v1/paper/search?query=X'`.
- **Source:** https://www.semanticscholar.org/product/api
- **Skill:** `skills/semantic-scholar-openalex/SKILL.md`

### OpenAlex API (skill: `semantic-scholar-openalex`)

- **When:** 250M+ works; filter DSL (`filter=publication_year:>2024,is_oa:true,type:review,cited_by_count:>50`); polite pool with mailto.
- **Endpoint:** `curl 'https://api.openalex.org/works?search=X&filter=...&mailto=$OPENALEX_EMAIL'`.
- **Source:** https://docs.openalex.org/
- **Skill:** `skills/semantic-scholar-openalex/SKILL.md`

### PubMed E-utilities (skill component within `paper-search-mcp`)

- **When:** authoritative biomed; MeSH terms; esearch→efetch chain. Free; ≤10k results per query post-Feb 2026.
- **Endpoints:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi` then `efetch.fcgi`.
- **Source:** https://www.ncbi.nlm.nih.gov/books/NBK25497/

### scite.ai API (skill component within `paper-search-mcp`)

- **When:** citation context (supporting / contradicting / mentioning) across 1.2B citation events.
- **Endpoint:** `curl -H "Authorization: Bearer $SCITE_KEY" https://api.scite.ai/papers/{doi}/citing-papers?classification=contradicting`.
- **Source:** https://help.scite.ai/en-us/category/scite-api-tomi6w/

### Kaggle CLI (skill: `kaggle-huggingface-datasets`)

- **When:** community-curated datasets; competitions; notebooks for analysis context.
- **Install:** `pip install kaggle`; set `~/.kaggle/kaggle.json`. `kaggle datasets download -d X`.
- **Source:** https://pypi.org/project/kaggle/
- **Skill:** `skills/kaggle-huggingface-datasets/SKILL.md`

### Hugging Face Datasets (skill: `kaggle-huggingface-datasets`)

- **When:** ML benchmark datasets; streaming for huge corpora; rich dataset cards.
- **Install:** `pip install datasets` → `load_dataset("rajpurkar/squad")`. MCP: `huggingface-mcp`.
- **Source:** https://huggingface.co/docs/datasets/index
- **Skill:** `skills/kaggle-huggingface-datasets/SKILL.md`

### FRED API (skill: `authoritative-data-fred-worldbank`)

- **When:** 816k+ US/intl economic series; canonical macro time series.
- **Install:** `pip install fredapi`; set `FRED_API_KEY`. `Fred(api_key).get_series('GDPC1')`.
- **Source:** https://fred.stlouisfed.org/docs/api/fred/
- **Skill:** `skills/authoritative-data-fred-worldbank/SKILL.md`

### World Bank API (skill: `authoritative-data-fred-worldbank`)

- **When:** country-level indicators (GDP, population, inflation, education, health). No key.
- **Install:** `pip install wbdata` → `wbdata.get_dataframe({'NY.GDP.MKTP.CD':'gdp'})`.
- **Source:** https://datahelpdesk.worldbank.org/knowledgebase/articles/889392

### IMF / OECD / Eurostat / BLS APIs (skill: `authoritative-data-fred-worldbank`)

- **When:** authoritative international macro series; ECB / BoE / RBI series.
- **Endpoints:** IMF `https://www.imf.org/external/datamapper/api/v1/{INDICATOR}/{COUNTRIES}`; OECD `https://stats.oecd.org/sdmx-json/data/...`; Eurostat `https://ec.europa.eu/eurostat/api/...`; BLS `https://api.bls.gov/publicAPI/v2/timeseries/data/`.
- **Skill:** `skills/authoritative-data-fred-worldbank/SKILL.md`

### PostHog API (skill: `cohort-retention-lifelines`)

- **When:** product-analytics cohort fetch; HogQL queries; behavioral-cohort definitions.
- **Endpoint:** `curl -H "Authorization: Bearer $KEY" https://app.posthog.com/api/projects/{id}/cohorts/`. MCP: `posthog-mcp`.
- **Source:** https://posthog.com/docs/api/cohorts
- **Skill:** `skills/cohort-retention-lifelines/SKILL.md`

### lifelines (skill: `cohort-retention-lifelines`)

- **When:** Kaplan-Meier survival analysis for retention curves with CI; log-rank cohort comparison; survival regression (Cox PH).
- **Install:** `pip install lifelines` → `KaplanMeierFitter().fit(d, e).plot_survival_function()`.
- **Source:** https://lifelines.readthedocs.io/
- **Skill:** `skills/cohort-retention-lifelines/SKILL.md`

### Claude Opus 4.7 extended thinking (skill: `first-principles-claude-extended`)

- **When:** first-principles 5-step decomposition; novel reasoning chains; load-bearing-assumption audit. Effort: low / medium / high / max.
- **Cross-check:** `gemini` MCP for adversarial review pass.
- **Source:** https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking
- **Skill:** `skills/first-principles-claude-extended/SKILL.md`

### Plotly + Altair + matplotlib + Mermaid + Datawrapper (skill: `data-storytelling-plotly-altair`)

- **When:** chart production for deliverables. Plotly = interactive HTML; Altair = declarative; matplotlib = publication-grade; Mermaid = diagrams; Datawrapper = publishing-grade embed.
- **Install:** `pip install plotly altair matplotlib seaborn kaleido`; `npm i -g @mermaid-js/mermaid-cli`.
- **Source:** https://plotly.com/python/ · https://altair-viz.github.io/
- **Skill:** `skills/data-storytelling-plotly-altair/SKILL.md`

### Pandoc (skill: `pandoc-branded-deliverables`)

- **When:** markdown → branded DOCX / PDF / PPTX with `--reference-doc=template.docx`. The recommended last step for any deliverable.
- **Endpoint:** `pandoc report.md -o report.docx --reference-doc=template.docx`.
- **Source:** https://pandoc.org/MANUAL.html
- **Skill:** `skills/pandoc-branded-deliverables/SKILL.md`

### Mistral OCR + Gemini OCR (skill: `ocr-scanned-academic-papers`)

- **When:** image-only academic PDFs; foreign-language documents (OCR → DeepL pipeline); tables + equations extraction.
- **Install:** MCPs `mistral-ocr-mcp` + `gemini-ocr-mcp` (enabled). Set `MISTRAL_API_KEY` / `GEMINI_API_KEY`.
- **Source:** https://docs.mistral.ai/capabilities/document/ · https://ai.google.dev/gemini-api/docs/document-processing
- **Skill:** `skills/ocr-scanned-academic-papers/SKILL.md`

### DeepL MCP

- **When:** high-quality translation of foreign-language sources; document-level translation preserving formatting.
- **MCP:** `deepl-mcp` (enabled). Set `DEEPL_AUTH_KEY`.
- **Source:** https://developers.deepl.com/

### Wappalyzer (skill: `competitive-intelligence-tech-stack`)

- **When:** competitor tech-stack detection (JS framework, web server, CMS, analytics, payment, CDN).
- **Install:** `pip install python-Wappalyzer` or inject JS via `playwright-mcp`.
- **Source:** https://www.wappalyzer.com/
- **Skill:** `skills/competitive-intelligence-tech-stack/SKILL.md`

### GitHub API (default skill: `github-api`)

- **When:** competitor engineering signal; public repo activity; talent / contributor analysis; open-source dependency mapping.
- **Endpoint:** `curl -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/orgs/{org}/repos`.
- **Source:** https://docs.github.com/en/rest

### NewsAPI.ai / Aylien / MediaCloud (supplementary, beyond GDELT)

- **When:** specialized news monitoring with industry / event taxonomies. Paid; use as supplement to GDELT.
- **Source:** https://newsapi.ai/ · https://aylien.com/ · https://mediacloud.org/

---

## SOTA fulfillment table (June 2026)

Maps each role.md / use_cases.md capability to the primary skill pack(s) and tools.

| Capability | Primary skill pack | Tools |
|---|---|---|
| General topic investigation | `perplexity-deep-research`, `exa-neural-search` | Perplexity Sonar, Exa, Brave/DDG, Claude extended thinking |
| Market sizing (TAM/SAM/SOM) | `sec-edgar-market-sizing`, `crunchbase-market-research` | SEC EDGAR XBRL, Crunchbase, Similarweb |
| Competitive intelligence (SWOT, benchmarking) | `competitive-intelligence-tech-stack`, `patents-uspto-lens` | SEC EDGAR, Lens.org, USPTO, Wappalyzer, GitHub API, playwright-mcp |
| Trend analysis (8-source fan-out, weak signals) | `trend-fan-out-multi-source`, `gdelt-news-monitoring` | pytrends, HN Algolia, PRAW, GDELT, USPTO, arXiv, YouTube |
| Scientific literature review | `paper-search-mcp`, `semantic-scholar-openalex` | arXiv, PubMed, bioRxiv, OpenAlex, Semantic Scholar, CrossRef, Europe PMC, ClinicalTrials, scite.ai, Unpaywall |
| Data research (datasets, validation) | `kaggle-huggingface-datasets`, `authoritative-data-fred-worldbank` | Kaggle CLI, HF Datasets, FRED, World Bank, IMF, OECD, Eurostat, BLS |
| Targeted search (>90% precision) | `exa-neural-search`, `semantic-scholar-openalex` | Brave/DDG Boolean, Exa includeDomains, OpenAlex filter DSL |
| First-principles thinking | `first-principles-claude-extended` | Claude Opus 4.7 extended thinking, gemini MCP cross-check |
| Cohort analysis (N-day retention, Aha moment) | `cohort-retention-lifelines` | PostHog API, lifelines KM, postgresql-mcp |
| KPI framework design | `kpi-dashboard-design` (existing) | LLM synthesis + pandas quantile baselines |
| Data storytelling | `data-storytelling-plotly-altair`, `data-storytelling` (existing) | Plotly, Altair, matplotlib, Mermaid, Datawrapper |
| Deliverables (briefing/report/trend/CI/market/scientific) | `pandoc-branded-deliverables` | Pandoc, docx/pdf/pptx/xlsx MCPs |
| Foreign-language sources | (DeepL MCP) | deepl-mcp |
| Scanned PDF / image-only papers | `ocr-scanned-academic-papers` | mistral-ocr-mcp, gemini-ocr-mcp |

See `reference/SOTA_USE_CASES.md` for per-use-case SOTA mapping with confidence flags.
