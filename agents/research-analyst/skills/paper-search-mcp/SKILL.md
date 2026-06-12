<!--
Source: https://mcpservers.org/servers/openags/paper-search-mcp
Repo: openags/paper-search-mcp (single MCP wrapping 20+ academic sources)
Related: scite.ai for citation context (https://scite.ai/)
-->

# Paper Search MCP — unified academic search

Single MCP install that wraps arXiv, PubMed, bioRxiv, medRxiv, Google Scholar, Semantic Scholar, CrossRef, OpenAlex, PMC, CORE, Europe PMC, dblp, OpenAIRE, SSRN, Unpaywall (20+ academic sources behind one tool surface). Replaces the previous "stitch together 6 different MCPs" workflow.

## When to use this skill

- Scientific literature review (any field — biomed, ML, physics, social sciences, economics)
- Cross-source citation lookup (does this claim appear in independent papers?)
- Triangulating an academic claim across preprint + peer-reviewed venues (bioRxiv → published version)
- Finding open-access PDFs (Unpaywall + Europe PMC + CORE)
- Building a citation graph (Semantic Scholar Graph API + OpenAlex `referenced_works`)
- Comparing the agent's "what's the latest on X" answer against authoritative academic sources

## When NOT to use

- For tech-blog / industry-report content → use `exa-neural-search` or `perplexity-deep-research`
- For news → use `gdelt-news-monitoring` or `ai-news-collectors`
- For dataset discovery → use `kaggle-huggingface-datasets`
- For citation *context* (supporting vs contradicting) → layer scite.ai on top

## Setup

```bash
# Install Paper Search MCP via cli-anything
pip install paper-search-mcp
# OR use the openags hosted server (no install)
# See: https://mcpservers.org/servers/openags/paper-search-mcp

# Optional: scite.ai for citation context (paid)
export SCITE_API_KEY="..."
```

No API key required for the underlying sources, though some (Semantic Scholar, OpenAlex) recommend a polite-pool email:

```bash
export OPENALEX_EMAIL="you@example.com"   # adds to mailto= for polite pool (250M+ works)
```

## Per-source query syntax cheat-sheet

| Source | Syntax | Example | Notes |
|---|---|---|---|
| **arXiv** | `all:X`, `ti:X`, `au:X`, `cat:cs.AI` | `all:transformer+ti:attention+cat:cs.LG` | 1 req / 3s rate limit |
| **PubMed** | MeSH terms, `[ti]`, `[au]`, `[mh]` | `"myocardial infarction"[mh] AND statin[ti]` | E-utilities esearch→efetch chain |
| **bioRxiv / medRxiv** | preprint-specific server filter | server=biorxiv, q=CRISPR | preprints; pair with PubMed for published |
| **Semantic Scholar** | free-text + `fieldsOfStudy` filter | `query=GAN&fieldsOfStudy=Computer Science` | 1000 rps unauth |
| **OpenAlex** | `search=X&filter=k:v,k:v` filter DSL | `search=LLM&filter=publication_year:>2024,is_oa:true` | 250M+ works; polite pool |
| **CrossRef** | `query=X`, `filter=from-pub-date:2024-01` | `query=climate&rows=20` | 1.8B citation links |
| **Europe PMC** | Lucene-style | `query=ABSTRACT:CRISPR+AND+PUB_YEAR:2024` | Open Access full-text |
| **PMC** | full-text search | `term=CRISPR[abstract]` | via NCBI E-utilities |
| **CORE** | `q=X`, faceted | `q=climate+modeling&limit=20` | 200M+ OA papers |
| **dblp** | CS-focused author/venue | `q=John+Doe`, `q=NeurIPS+2024` | computer-science venues |
| **OpenAIRE** | EU OA research repository | `title=X&fromDateAccepted=2024-01-01` | |
| **SSRN** | social-sci preprints | abstract-id lookup | |
| **Unpaywall** | DOI → OA PDF link | `doi/10.xxx/yyy?email=...` | OA legality check |
| **Google Scholar** | free-text + operators | `"climate change" site:nature.com` | scraping; rate-sensitive |

## Common recipes

### Recipe 1 — Cross-source claim triangulation

```python
# Pseudocode — invoked through Paper Search MCP tool surface
claim = "GLP-1 agonists reduce cardiovascular mortality"

# 1. Authoritative trial evidence
pubmed_hits = paper_search.search(source="pubmed", query='"GLP-1" AND mortality[mh]', limit=20)
# 2. Preprint signal (pre-publication)
biorxiv_hits = paper_search.search(source="biorxiv", query="GLP-1 cardiovascular", limit=10)
# 3. Citation-graph centrality
ss_hits = paper_search.search(source="semantic_scholar", query="GLP-1 cardiovascular mortality",
                              fields=["title","year","citationCount","influentialCitationCount"], limit=20)
# 4. Filter to open access for PDF retrieval
oa = paper_search.search(source="openalex", query="GLP-1 cardiovascular",
                         filter="is_oa:true,publication_year:>2022", limit=20)
```

Triangulation rule: a claim is **moderate confidence** if it appears in PubMed *and* one preprint server with overlapping authors; **high confidence** if it appears in ≥3 independent peer-reviewed papers with no shared funder.

### Recipe 2 — Open-access PDF retrieval pipeline

```python
# Given a DOI, find the legal OA copy
doi = "10.1038/s41586-024-12345-6"
oa = paper_search.unpaywall(doi=doi, email=os.environ["OPENALEX_EMAIL"])
if oa.is_oa:
    pdf_url = oa.best_oa_location.url_for_pdf
    # Download via cli-anything for OCR or full-text analysis
    # If image-only PDF → escalate to mistral-ocr-mcp / gemini-ocr-mcp
```

### Recipe 3 — Citation context (scite.ai layer)

scite.ai classifies citations as supporting / contradicting / mentioning across 1.2B citation events:

```bash
curl -H "Authorization: Bearer $SCITE_API_KEY" \
     "https://api.scite.ai/papers/10.xxx/yyy/citing-papers?classification=contradicting"
```

Use when a single high-impact paper underlies a downstream claim — check whether the literature has contradicted it.

### Recipe 4 — Field-of-study filtered review

```bash
# OpenAlex filter DSL — recent, open-access, top-cited reviews in a field
curl "https://api.openalex.org/works?\
search=large+language+models&\
filter=publication_year:>2024,is_oa:true,type:review,cited_by_count:>50&\
sort=cited_by_count:desc&\
per-page=50&\
mailto=$OPENALEX_EMAIL"
```

### Recipe 5 — Author network expansion

```bash
# Semantic Scholar: given a seed paper, walk citation graph
curl "https://api.semanticscholar.org/graph/v1/paper/DOI:10.xxx/yyy?fields=references,citations,authors"
# Then for each author:
curl "https://api.semanticscholar.org/graph/v1/author/$AUTHOR_ID/papers?fields=title,year,citationCount&limit=100"
```

## Edge cases

- **Preprint vs published divergence:** bioRxiv preprint figures sometimes change before publication. Always check whether the published version (PubMed / journal DOI) supports the same conclusion. Flag if preprint-only.
- **Retraction watch:** Cross-check DOIs against `https://retractionwatch.com/` or PubMed `[pt] Retracted Publication`. A high-citation paper that's retracted is a red flag.
- **Predatory journals:** Cross-check the journal ISSN against Beall's List (archived) or DOAJ. If absent from DOAJ + low impact, treat as low-weight evidence.
- **Paywalled abstracts only:** Some Elsevier / Wiley papers return only the abstract. Use Unpaywall to find legal OA copies; if none, cite abstract + note paywall in limitations.
- **arXiv rate limit:** 1 req / 3 seconds. Batch arXiv last, or use OpenAlex (which mirrors arXiv with no per-request rate limit beyond polite pool).
- **Non-English literature:** Paper Search MCP returns titles in original language. Pair with `deepl-mcp` for translation of abstracts; OCR + DeepL for scanned non-English PDFs.
- **Date filtering precision:** OpenAlex uses `publication_year:>2024` (year-level); CrossRef uses `from-pub-date:2024-01-15` (day-level). Use CrossRef for tight time windows.

## Sources

- Paper Search MCP: https://mcpservers.org/servers/openags/paper-search-mcp
- arXiv API: https://info.arxiv.org/help/api/user-manual.html
- PubMed E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25497/
- Semantic Scholar Graph API: https://www.semanticscholar.org/product/api
- OpenAlex: https://docs.openalex.org/api-entities/works/search-works
- CrossRef REST: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- Europe PMC: https://europepmc.org/RestfulWebService
- Unpaywall: https://unpaywall.org/products/api
- scite.ai: https://help.scite.ai/en-us/category/scite-api-tomi6w/
- ClinicalTrials.gov v2 (for medical claim triangulation): https://clinicaltrials.gov/data-api/api

## Related skills

- `semantic-scholar-openalex` — deeper dive on the two highest-ROI APIs from the bundle
- `ocr-scanned-academic-papers` — when the PDF is image-only
- `perplexity-deep-research` — when you need synthesized answer, not raw papers
