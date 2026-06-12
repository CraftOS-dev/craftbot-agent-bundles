<!--
Sources: Semantic Scholar Graph API https://www.semanticscholar.org/product/api
         OpenAlex API https://docs.openalex.org/
Rate limits: Semantic Scholar 1000 rps unauth; OpenAlex 100k req/day polite pool
-->

# Semantic Scholar Graph + OpenAlex — the two highest-ROI academic APIs

Of the 20+ sources behind `paper-search-mcp`, these two return the most leverage per call:

- **Semantic Scholar Graph API** — 200M+ papers, **1000 rps unauthenticated**, ML-enriched `influentialCitationCount`, embedding-based recommendations, citation context labels (background / methodology / result).
- **OpenAlex API** — 250M+ works (open license, free), powerful filter DSL (`filter=k:v,k:v`), polite-pool mailto for unthrottled access, comprehensive author / institution / venue networks.

When you need raw structured paper data with rich metadata at scale, these are the right tools.

## When to use this skill

- Citation graph walking (forward + backward)
- Field-of-study filtered review
- Author / institution network analysis
- Influence ranking (Semantic Scholar `influentialCitationCount` ≠ raw citation count)
- Open-access detection + DOI resolution
- Venue prestige ranking (h-index per journal/conference)
- Bulk paper enrichment for downstream synthesis

## When NOT to use

- For full-text PDF retrieval → use Unpaywall via `paper-search-mcp`, then OCR if scanned
- For citation context (supporting vs contradicting) → use scite.ai
- For pre-prints not yet on arXiv → use bioRxiv/medRxiv via `paper-search-mcp`
- For non-English-language papers → coverage is uneven; supplement with regional databases

## Setup

```bash
# Semantic Scholar — no key needed for 1000 rps unauth tier
# Optional: free API key for 1500 rps via https://www.semanticscholar.org/product/api/tutorial

# OpenAlex — no key, just polite-pool email
export OPENALEX_EMAIL="you@example.com"
```

## Semantic Scholar recipes

### Recipe 1 — Search papers

```bash
curl "https://api.semanticscholar.org/graph/v1/paper/search?\
query=large+language+model+reasoning&\
limit=50&\
fields=title,year,citationCount,influentialCitationCount,authors,venue,openAccessPdf,abstract,fieldsOfStudy"
```

`influentialCitationCount` is Semantic Scholar's ML-graded subset — citations that materially extend the work, not throwaway references. More signal than raw `citationCount`.

### Recipe 2 — Paper detail + references + citations

```bash
# By DOI
curl "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1038/s41586-024-08145-x?\
fields=title,abstract,references.title,references.year,references.authors,citations.title,citations.year,citations.authors"

# By S2 paper ID
curl "https://api.semanticscholar.org/graph/v1/paper/649def34f8be52c8b66281af98ae884c09aef38b?fields=..."
```

### Recipe 3 — Author papers + h-index

```bash
# Search author
curl "https://api.semanticscholar.org/graph/v1/author/search?query=Geoffrey+Hinton&fields=name,affiliations,hIndex,paperCount,citationCount"

# Author's papers
curl "https://api.semanticscholar.org/graph/v1/author/{author_id}/papers?fields=title,year,citationCount,venue&limit=100"
```

### Recipe 4 — Recommendations (embedding-based)

```bash
curl -X POST "https://api.semanticscholar.org/recommendations/v1/papers" \
  -H "Content-Type: application/json" \
  -d '{"positivePaperIds":["DOI:10.1038/s41586-024-08145-x"], "negativePaperIds":[], "limit":50}'
```

Useful for "find me more papers like this one" — the embedding-based recommender is better than keyword search for adjacent literatures.

### Recipe 5 — Batch lookup

```bash
# Up to 500 paper IDs per call
curl -X POST "https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,year,citationCount" \
  -H "Content-Type: application/json" \
  -d '{"ids":["DOI:10.xxx/yyy","DOI:10.xxx/zzz","..."]}'
```

## OpenAlex recipes

### Recipe 6 — Search with filter DSL

```bash
# Recent open-access reviews in a field, sorted by citations
curl "https://api.openalex.org/works?\
search=large+language+models&\
filter=publication_year:>2024,is_oa:true,type:review,cited_by_count:>50&\
sort=cited_by_count:desc&\
per-page=50&\
mailto=$OPENALEX_EMAIL"
```

Key filters (`filter=k:v,k:v` AND between, `|` OR within value):

| Filter | Example |
|---|---|
| `publication_year` | `publication_year:2025` or `>2024` or `<=2020` |
| `is_oa` | `is_oa:true` (open access) |
| `type` | `type:review`, `type:article`, `type:dataset` |
| `cited_by_count` | `>100`, `>50` |
| `authorships.author.id` | `A123456789` |
| `authorships.institutions.id` | `I1283280994` (MIT) |
| `primary_topic.id` | OpenAlex topic ID |
| `concepts.id` | concept ID (deprecated, use topics) |
| `language` | `language:en` |
| `from_publication_date` | `2024-01-01` |
| `to_publication_date` | `2025-12-31` |
| `has_doi` | `has_doi:true` |
| `has_orcid` | `authorships.author.has_orcid:true` |

### Recipe 7 — Single work by DOI

```bash
curl "https://api.openalex.org/works/doi:10.1038/s41586-024-08145-x?mailto=$OPENALEX_EMAIL"
# Returns: referenced_works, related_works, cited_by_count, primary_topic, concepts, etc.
```

### Recipe 8 — Author profile + co-author graph

```bash
# Find author by name (returns OpenAlex author ID)
curl "https://api.openalex.org/authors?search=Geoffrey+Hinton&mailto=$OPENALEX_EMAIL"

# Author detail
curl "https://api.openalex.org/authors/A2110226808?mailto=$OPENALEX_EMAIL"

# All of their works
curl "https://api.openalex.org/works?filter=authorships.author.id:A2110226808&per-page=200&mailto=$OPENALEX_EMAIL"
```

### Recipe 9 — Institution analysis

```bash
# All papers from Stanford in 2024 in AI/ML topics
curl "https://api.openalex.org/works?\
filter=authorships.institutions.id:I97018004,publication_year:2024,primary_topic.id:T10883&\
per-page=200&\
mailto=$OPENALEX_EMAIL"
```

### Recipe 10 — Citation graph walking via referenced_works

```python
import requests, networkx as nx
G = nx.DiGraph()
seed_doi = "10.1038/s41586-024-08145-x"

def add_paper(doi, depth):
    r = requests.get(f"https://api.openalex.org/works/doi:{doi}?mailto={EMAIL}").json()
    G.add_node(r["id"], title=r["title"], year=r["publication_year"], citations=r["cited_by_count"])
    if depth > 0:
        for ref in r.get("referenced_works", [])[:20]:
            r2 = requests.get(f"https://api.openalex.org/works/{ref.split('/')[-1]}?mailto={EMAIL}").json()
            G.add_edge(r["id"], r2["id"])
            add_paper(r2.get("doi","").replace("https://doi.org/",""), depth - 1)

add_paper(seed_doi, depth=2)
# Now run PageRank for foundational papers
ranks = nx.pagerank(G)
```

### Recipe 11 — Topic / concept exploration

OpenAlex uses *Topics* (current, replaces old *Concepts*):

```bash
# Find topics matching "transformer"
curl "https://api.openalex.org/topics?search=transformer&mailto=$OPENALEX_EMAIL"

# All works in topic T10883 (or whichever ID)
curl "https://api.openalex.org/works?filter=primary_topic.id:T10883&per-page=200&mailto=$OPENALEX_EMAIL"
```

## Combining the two

The strongest workflow uses both:

```python
# Step 1: Discover via OpenAlex's filter DSL (broad, structured)
oa_papers = openalex_search(filter="primary_topic.id:T10883,publication_year:>2024,cited_by_count:>20")

# Step 2: Enrich with Semantic Scholar's influence + embedding metrics
for paper in oa_papers:
    s2 = ss_lookup(doi=paper["doi"])
    paper["influentialCitationCount"] = s2["influentialCitationCount"]
    paper["embedding"] = s2["embedding"]  # for downstream clustering

# Step 3: Cluster by S2 embeddings → identify research-thread clusters
```

## Edge cases

- **Rate limits:** Semantic Scholar 1000 rps unauth, but bursty calls can 429. Insert ~1ms delay or use the official Python SDK which handles backoff. OpenAlex 10 rps polite pool — politeness pays off.
- **DOI resolution mismatch:** Same paper may have different DOIs in S2 vs OpenAlex (preprint vs published). Cross-reference both before deduplication.
- **`influentialCitationCount` interpretation:** S2 trains a classifier on whether a citation is "influential" (extends the work) vs incidental. Threshold-based, not perfect; useful as relative ranking.
- **Field-of-study granularity:** S2's `fieldsOfStudy` is coarse (~20 fields). OpenAlex Topics are 4000+ fine-grained — prefer OpenAlex for narrow filtering.
- **Open-access detection:** OpenAlex's `is_oa` is conservative (only confirmed OA). For broader OA detection use Unpaywall (more aggressive).
- **Citation counts drift:** Both APIs update citation counts daily. Snapshot the date when reporting.
- **Author disambiguation:** common names (e.g., "Wei Wang") have hundreds of authors. Always confirm by ORCID or institution.

## Sources

- Semantic Scholar Graph API: https://api.semanticscholar.org/api-docs/graph
- Semantic Scholar Recommendations API: https://api.semanticscholar.org/api-docs/recommendations
- OpenAlex docs: https://docs.openalex.org/
- OpenAlex filter syntax: https://docs.openalex.org/how-to-use-the-api/filter-entity-lists
- OpenAlex Topics taxonomy: https://docs.openalex.org/api-entities/topics

## Related skills

- `paper-search-mcp` — broader source coverage; this is the deep-dive for the two highest-ROI APIs
- `ocr-scanned-academic-papers` — for the PDF retrieval step
- `perplexity-deep-research` — synthesizes the papers these APIs surface
