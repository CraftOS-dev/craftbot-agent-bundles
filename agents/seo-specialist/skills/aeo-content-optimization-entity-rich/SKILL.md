<!--
Source: https://surferseo.com/blog/geo-optimization/
Source: https://www.frase.io/blog/aeo-vs-seo/
Source: https://query.wikidata.org/
Source: https://developers.google.com/knowledge-graph
Depth: AEO content patterns (direct-answer + entity-rich + source authority + schema depth)
-->
# AEO Content Optimization — Entity-Rich + Source Authority

## When to use

Reach for this skill when the user asks for: "AEO optimization", "optimize for AI search", "make content citable by ChatGPT", "GEO content patterns", "Wikidata entity linking", "entity-rich content", "AI citation optimization", "structured Q&A for LLMs", "direct-answer block". This is the content-writing depth specialist for AEO — different signals than SEO (LLMs retrieve via embedding similarity + entity recognition + source authority, not Google's ranking algorithm). Covers direct-answer block pattern, Wikidata entity linking via SPARQL, source citation density, FAQPage/HowTo schema layering.

## Setup

```bash
# Wikidata SPARQL — free
curl -G https://query.wikidata.org/sparql \
  --data-urlencode "query=SELECT ?item WHERE { ?item rdfs:label 'OpenAI'@en } LIMIT 5" \
  -H "Accept: application/sparql-results+json"

# Google Knowledge Graph API — entity verification
export KG_KEY="<from console.cloud.google.com/apis/credentials>"

# Surfer GEO — AEO scoring (see content-cluster-architecture-marketmuse skill)
export SURFER_API_KEY="<from surferseo.com/app/settings>"

# Frase — AEO scoring alt
export FRASE_API_KEY="<from app.frase.io/account>"

# huggingface-mcp for NER (named entity recognition)
# Pre-configured via CraftBot MCP defaults
```

Auth requirements:
- `KG_KEY` — Google Knowledge Graph API key; free 100K queries/day
- `SURFER_API_KEY` — Advanced plan $129/mo for GEO scoring
- `FRASE_API_KEY` — Solo plan $45/mo
- No auth for Wikidata SPARQL (free, public)

## Common recipes

### Recipe 1: Direct-answer block pattern (lead with 40-60 word answer)
```markdown
# What is marketing automation?

Marketing automation is the use of software to automate repetitive marketing tasks — email campaigns, social media posting, lead nurturing, and analytics reporting. It enables teams to scale personalized customer outreach without proportionally scaling headcount, typically using triggered workflows based on user behavior or scheduled cadences.

Marketing automation platforms emerged in the early 2000s with Eloqua (founded 1999) and Marketo (2006). Today's leading vendors include [HubSpot](https://en.wikipedia.org/wiki/HubSpot), [Salesforce Marketing Cloud](https://en.wikipedia.org/wiki/Salesforce_Marketing_Cloud), and [ActiveCampaign](https://en.wikipedia.org/wiki/ActiveCampaign), each targeting different market segments...
```
Pattern: H1 = the question, first paragraph = 40-60 word answer (no preamble), second paragraph = context + entity links.

### Recipe 2: Wikidata SPARQL — verify + link entities
```bash
# Look up an entity by English label
curl -G https://query.wikidata.org/sparql \
  --data-urlencode "query=SELECT ?item ?itemLabel ?description WHERE { ?item rdfs:label 'HubSpot'@en . ?item schema:description ?description . FILTER(LANG(?description) = 'en') . SERVICE wikibase:label { bd:serviceParam wikibase:language 'en' } }" \
  -H "Accept: application/sparql-results+json"

# Returns: Q15279 = HubSpot, Inc.
```

```python
# Python pipeline: extract entities → verify on Wikidata → link in content
import requests, re

def get_wikidata_id(label):
    r = requests.get(
        'https://query.wikidata.org/sparql',
        params={'query': f'SELECT ?item WHERE {{ ?item rdfs:label "{label}"@en }} LIMIT 1', 'format': 'json'},
        headers={'Accept': 'application/sparql-results+json'}
    )
    bindings = r.json()['results']['bindings']
    return bindings[0]['item']['value'] if bindings else None

# Output: https://www.wikidata.org/wiki/Q15279
```

### Recipe 3: Google Knowledge Graph entity verification
```bash
# Check if Google recognizes the entity
curl "https://kgsearch.googleapis.com/v1/entities:search?query=HubSpot&key=$KG_KEY&limit=5"

# Returns:
# itemListElement[0].score >= 100 → strong entity recognition
# score < 100 → weak/missing — build entity via Wikipedia/Crunchbase/LinkedIn linkage
```

### Recipe 4: Entity extraction from content via huggingface-mcp
```python
# Named Entity Recognition via huggingface-mcp
import requests

def extract_entities(text):
    # Using HF NER model (e.g., dslim/bert-base-NER)
    r = mcp.call('huggingface.text_classification',
        model='dslim/bert-base-NER',
        inputs=text
    )
    entities = []
    for ent in r:
        if ent['entity_group'] in ['PER', 'ORG', 'LOC', 'MISC']:
            entities.append({'text': ent['word'], 'type': ent['entity_group'], 'score': ent['score']})
    return entities

# Example
text = "OpenAI was founded by Sam Altman and Elon Musk in 2015 in San Francisco."
entities = extract_entities(text)
# [{'text':'OpenAI','type':'ORG'}, {'text':'Sam Altman','type':'PER'}, ...]
```

### Recipe 5: Semantic markup wrap for entities (itemtype + itemprop)
```html
<p>
  <span itemscope itemtype="https://schema.org/Organization">
    <a itemprop="sameAs" href="https://en.wikipedia.org/wiki/OpenAI">
      <span itemprop="name">OpenAI</span>
    </a>
  </span>
  was founded by
  <span itemscope itemtype="https://schema.org/Person">
    <a itemprop="sameAs" href="https://en.wikipedia.org/wiki/Sam_Altman">
      <span itemprop="name">Sam Altman</span>
    </a>
  </span>
  and
  <span itemscope itemtype="https://schema.org/Person">
    <a itemprop="sameAs" href="https://en.wikipedia.org/wiki/Elon_Musk">
      <span itemprop="name">Elon Musk</span>
    </a>
  </span>
  in 2015.
</p>
```
Microdata + JSON-LD both work for entity signaling; JSON-LD preferred at scale.

### Recipe 6: Source citation density (≥2 outbound per page)
```markdown
According to [Google's 2024 spam policy update](https://developers.google.com/search/blog/2024/03/core-update-spam-policies), sites must demonstrate originality and expertise.

A [2023 study by HubSpot](https://www.hubspot.com/state-of-marketing) found that 80% of marketers use automation tools.

The [Search Engine Journal migration checklist](https://www.searchenginejournal.com/seo-website-migration-checklist/) recommends 301 over 302 for permanent moves.
```
Pattern: ≥2 outbound citations per article; prefer .gov / .edu / peer-reviewed for YMYL topics; inline citation format ("According to [Source]"). LLMs prefer citing content that itself cites.

### Recipe 7: Structured Q&A (FAQPage) for AI surface extraction
```html
<section>
  <h2>Frequently asked questions</h2>

  <div itemscope itemtype="https://schema.org/Question">
    <h3 itemprop="name">What is the best marketing automation tool for B2B?</h3>
    <div itemprop="acceptedAnswer" itemscope itemtype="https://schema.org/Answer">
      <p itemprop="text">For B2B specifically, HubSpot Marketing Hub (mid-market) and Marketo Engage (enterprise) are the most-cited tools in industry reviews. HubSpot starts at $50/mo; Marketo enterprise typically $1500+/mo. Both integrate with major CRMs.</p>
    </div>
  </div>

  <div itemscope itemtype="https://schema.org/Question">
    <h3 itemprop="name">How much does marketing automation cost?</h3>
    <div itemprop="acceptedAnswer" itemscope itemtype="https://schema.org/Answer">
      <p itemprop="text">Marketing automation costs range from $0 (free tiers like HubSpot Starter or Brevo) to $5000+/mo for enterprise platforms like Marketo Engage or Salesforce Marketing Cloud.</p>
    </div>
  </div>
</section>
```
Pair with FAQPage JSON-LD (see `schema-org-deep-jsonld-eeat` Recipe 3).

### Recipe 8: HowTo structured content (for "how to X" queries)
```html
<article itemscope itemtype="https://schema.org/HowTo">
  <h1 itemprop="name">How to set up marketing automation</h1>
  <p itemprop="description">Step-by-step guide to launching marketing automation in 90 days.</p>

  <div itemprop="step" itemscope itemtype="https://schema.org/HowToStep">
    <h2><span itemprop="position">1</span>. <span itemprop="name">Audit existing tools</span></h2>
    <p itemprop="text">Catalog every marketing tool currently in use; identify overlap and gaps.</p>
  </div>

  <div itemprop="step" itemscope itemtype="https://schema.org/HowToStep">
    <h2><span itemprop="position">2</span>. <span itemprop="name">Pick a platform</span></h2>
    <p itemprop="text">Evaluate based on team size, budget, and integration needs.</p>
  </div>
</article>
```

### Recipe 9: Surfer GEO score check
```bash
curl -X POST https://api.surferseo.com/v1/geo-score \
  -H "Authorization: Bearer $SURFER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content":"<full markdown of article>",
    "target_query":"marketing automation tools",
    "competitors":["competitor1.com/page-a"]
  }'
# Returns: geo_score (0-100), entity_density, structured_qa_count, source_citation_count, direct_answer_detected
```
Target: GEO score > 75 before shipping AEO-optimized content.

### Recipe 10: Frase Topic Model AEO check (cheaper alt)
```bash
curl -X POST https://api.frase.io/v1/aeo-score \
  -H "X-Api-Key: $FRASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content":"<markdown>",
    "query":"marketing automation tools",
    "lang":"en"
  }'
```

### Recipe 11: AEO content scoring checklist (manual)
```
For each article, score 0/1 per signal (target ≥7/10):

[ ] Direct-answer block in first 100 words (40-60 word answer)
[ ] H1 = primary question (matches LLM query pattern)
[ ] H2/H3 use question phrasing for primary subtopics
[ ] ≥3 named entities wrapped with semantic markup or itemtype
[ ] ≥1 entity linked to Wikidata or Wikipedia
[ ] ≥2 outbound citations to authoritative sources (.gov/.edu/peer-reviewed preferred for YMYL)
[ ] FAQPage JSON-LD present
[ ] Article + Person + Organization JSON-LD present
[ ] Original data or quote from named expert
[ ] dateModified within last 90 days
```

### Recipe 12: Entity authority build for new authors
```
Author has no Knowledge Graph entity (Recipe 3 score < 100)? Build it:

1. Create Wikipedia stub (must meet notability threshold)
2. Add LinkedIn profile with consistent name + photo + bio
3. Add Crunchbase profile if a founder/executive
4. Add ORCID if academic
5. Cross-reference in Person schema sameAs across all of the above
6. Wait 60-90 days for Google KG ingestion
7. Re-run Recipe 3 → confirm score ≥ 100
```

## Examples

### Example 1: Rewrite existing article for AEO
**Goal:** Article ranking #5 organically; wants AI citations too.

**Steps:**
1. Recipe 11: score current article (likely 3-5/10).
2. Add direct-answer block (Recipe 1).
3. Extract entities (Recipe 4), verify on Wikidata (Recipe 2), wrap in semantic markup (Recipe 5).
4. Add 2-3 outbound citations (Recipe 6).
5. Add FAQPage section + JSON-LD (Recipe 7).
6. Add Person + Organization JSON-LD (`schema-org-deep-jsonld-eeat` skill).
7. Recipe 9 (or 10): confirm GEO score > 75.
8. Reindex via Suganthan GSC `submit_url`.
9. Monitor citation share via `aeo-geo-citation-tracking-athena-profound-glasp` for 30 days.

**Result:** Article scoring for both organic + AEO; citation share appears within 14-30 days.

### Example 2: AEO content template for new content production
**Goal:** Brief for technical-writer that bakes AEO patterns into every new article.

**Steps:**
1. Build content template embedding Recipes 1, 6, 7, 8, 11.
2. Add to brief generator (`content-cluster-architecture-marketmuse` skill briefs).
3. Train technical-writer agent on the pattern via slash command or skill addition.

**Result:** Every new article ships AEO-ready.

### Example 3: Build author entity for new author
**Goal:** Author bio added to articles but no Knowledge Graph recognition.

**Steps:**
1. Recipe 3: confirm Google KG score < 100.
2. Recipe 12: build entity (Wikipedia + LinkedIn + Crunchbase + ORCID).
3. Update Person schema sameAs (`schema-org-deep-jsonld-eeat` Recipe 1).
4. Wait 60-90 days.
5. Recipe 3 re-check → confirm score ≥ 100.

**Result:** Author entity recognized; E-E-A-T uplift across all articles authored.

## Edge cases / gotchas

- **Wikidata SPARQL rate limit** — 60 req/min; for bulk lookups use cached results or sleep between calls.
- **Wikidata Q-IDs not always English-mapped** — non-Latin labels may need `?item rdfs:label "Label"@<lang>` query variants.
- **Google KG entity score < 100 doesn't mean ignored** — borderline (50-100) still helps. <50 is the real "not recognized" threshold.
- **Direct-answer block over-optimization** — don't put EVERY page's answer in 40-60 words; some topics need longer. Use only where the H1 question is direct.
- **FAQPage rich result reduced 2023** — but FAQPage schema still aids AEO extraction. Don't skip just because no SERP feature.
- **Schema for hidden content = penalty** — Q&A blocks behind "Show More" toggles loaded via JS lose schema validity.
- **Author entity build (Recipe 12) takes time** — 60-90 days for Google KG ingestion. Don't expect immediate effect.
- **GEO score gameable** — Surfer / Frase scores correlate with citation share but aren't direct signals. Don't optimize past score 80 — readability tradeoff.
- **Entity linking trade-off** — every entity wrapped in `<a href="https://wikipedia.org/...">` creates outbound links. Don't link 30 entities per page (looks spammy); link the 5-10 most central.
- **LLMs vary in entity-recognition** — ChatGPT excellent; Claude strong; Gemini variable; Perplexity uses retrieval not training so depends on source authority.
- **EU privacy (GDPR) and entity linking** — wrapping a Person entity is fine when person is publicly notable; don't entity-wrap private individuals (e.g., customer testimonial names).

## Sources

- [Surfer GEO optimization](https://surferseo.com/blog/geo-optimization/)
- [Frase — AEO vs SEO](https://www.frase.io/blog/aeo-vs-seo/)
- [Wikidata SPARQL service](https://query.wikidata.org/)
- [Wikidata SPARQL tutorial](https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries)
- [Google Knowledge Graph API](https://developers.google.com/knowledge-graph)
- [Schema.org Person type](https://schema.org/Person)
- [Schema.org FAQPage](https://schema.org/FAQPage)
- [Schema.org HowTo](https://schema.org/HowTo)
- [Search Engine Land — AEO patterns 2026](https://searchengineland.com/aeo-content-patterns)
- [HuggingFace NER models](https://huggingface.co/models?pipeline_tag=token-classification)
