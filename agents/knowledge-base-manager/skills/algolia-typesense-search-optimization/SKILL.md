---
name: algolia-typesense-search-optimization
description: KB search optimization — Algolia DocSearch, Typesense, MeiliSearch, Pagefind, Orama. Synonyms, ranking, autocomplete, federated search, Insights API. Use when search is "bad", no-result-found is high, or building a search experience from scratch.
---

# Algolia / Typesense / MeiliSearch / Pagefind / Orama — KB search optimization

## When to use

User says "search is bad", "people can't find articles", "high no-result rate", "add search to docs", "rank tracking for KB search". Reach here AFTER taxonomy is settled (synonyms map vocabulary back to canonical category names).

Defer hosted-app search (Algolia for product, not docs) to `frontend-agent`. This skill is KB-search specific.

## Setup

```bash
# Algolia DocSearch (free for OSS): apply at https://docsearch.algolia.com/apply
# Algolia Crawler (paid):
npm i -g algolia-cli

# Typesense (self-hosted):
docker run -d -p 8108:8108 -v $(pwd)/data:/data \
  typesense/typesense:0.25.2 --data-dir=/data --api-key=xyz --enable-cors

# MeiliSearch (self-hosted):
curl -L https://install.meilisearch.com | sh
./meilisearch --master-key=xyz

# Pagefind (static):
npx pagefind --site dist

# Orama (in-browser):
npm i @orama/orama
```

Auth / API key requirements:
- `ALGOLIA_APP_ID` + `ALGOLIA_ADMIN_KEY` + `ALGOLIA_ANALYTICS_KEY` — Algolia dashboard
- `TYPESENSE_API_KEY` — set at boot
- `MEILI_MASTER_KEY` — set at boot

## Common recipes

### Recipe 1: Bootstrap Algolia DocSearch (free OSS)

After approval, drop in your docs site config:

```javascript
// docusaurus.config.js
themeConfig: {
  algolia: {
    appId: 'XXXX',
    apiKey: 'search-only-key',
    indexName: 'acme',
    contextualSearch: true,
    insights: true,
  },
}
```

### Recipe 2: Push synonyms via Algolia Rules API

```bash
cat > synonyms.json <<'EOF'
[
  {"objectID":"syn-sso","type":"synonym","synonyms":["sso","single sign on","single-sign-on","saml","oidc"]},
  {"objectID":"syn-webhook","type":"synonym","synonyms":["webhook","callback","event subscription"]},
  {"objectID":"syn-key","type":"synonym","synonyms":["api key","token","bearer token","auth token"]}
]
EOF

curl -X POST "https://${ALGOLIA_APP_ID}-dsn.algolia.net/1/indexes/acme/synonyms/batch?replaceExistingSynonyms=true" \
  -H "X-Algolia-Application-Id: $ALGOLIA_APP_ID" \
  -H "X-Algolia-API-Key: $ALGOLIA_ADMIN_KEY" \
  -H 'Content-Type: application/json' \
  --data @synonyms.json
```

### Recipe 3: Configure custom ranking

```bash
curl -X PUT "https://${ALGOLIA_APP_ID}-dsn.algolia.net/1/indexes/acme/settings" \
  -H "X-Algolia-Application-Id: $ALGOLIA_APP_ID" \
  -H "X-Algolia-API-Key: $ALGOLIA_ADMIN_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "searchableAttributes": ["title","unordered(h1)","unordered(description)","unordered(content)","tags"],
    "customRanking": ["desc(views_30d)","desc(helpful_pct)","desc(last_modified_ts)"],
    "ranking": ["typo","geo","words","filters","proximity","attribute","exact","custom"]
  }'
```

### Recipe 4: Typesense synonyms collection

```bash
curl -X PUT "http://localhost:8108/collections/docs/synonyms/sso" \
  -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"synonyms":["sso","single sign on","saml","oidc"]}'

# Verify
curl "http://localhost:8108/collections/docs/synonyms" \
  -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}"
```

### Recipe 5: Pull top-searched (Algolia Insights)

```bash
curl -G 'https://analytics.algolia.com/2/searches' \
  -H "X-Algolia-Application-Id: $ALGOLIA_APP_ID" \
  -H "X-Algolia-API-Key: $ALGOLIA_ANALYTICS_KEY" \
  --data-urlencode 'index=acme' \
  --data-urlencode "startDate=$(date -d '30 days ago' +%F)" \
  --data-urlencode "endDate=$(date +%F)" \
  --data-urlencode 'limit=50' \
  | jq -r '.searches[] | "\(.count)\t\(.search)\t\(.clickThroughRate)"' \
  > top-searched.tsv
```

### Recipe 6: Pull no-result-found queries

```bash
curl -G 'https://analytics.algolia.com/2/searches/noResults' \
  -H "X-Algolia-Application-Id: $ALGOLIA_APP_ID" \
  -H "X-Algolia-API-Key: $ALGOLIA_ANALYTICS_KEY" \
  --data-urlencode 'index=acme' \
  --data-urlencode "startDate=$(date -d '7 days ago' +%F)" \
  | jq -r '.searches[] | "\(.count)\t\(.search)"' \
  | sort -rn > no-result-7d.tsv
```

### Recipe 7: MeiliSearch — synonyms + typo tolerance

```bash
# Set synonyms
curl -X PUT "http://localhost:7700/indexes/docs/settings/synonyms" \
  -H "Authorization: Bearer ${MEILI_MASTER_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"webhook":["callback","event handler"],"sso":["saml","oidc","single sign on"]}'

# Tune typo tolerance
curl -X PUT "http://localhost:7700/indexes/docs/settings/typo-tolerance" \
  -H "Authorization: Bearer ${MEILI_MASTER_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"enabled":true,"minWordSizeForTypos":{"oneTypo":4,"twoTypos":8}}'
```

### Recipe 8: Pagefind — zero-infra static search

```bash
# Build docs site (Astro/Hugo/MkDocs/Jekyll)
npm run build

# Index the output
npx pagefind --site dist

# In your template:
# <link href="/pagefind/pagefind-ui.css" rel="stylesheet">
# <script src="/pagefind/pagefind-ui.js"></script>
# <div id="search"></div>
# <script>new PagefindUI({element:"#search"})</script>
```

### Recipe 9: Orama — vector + lexical

```javascript
import { create, insert, search } from '@orama/orama';
import { persistToFile, restoreFromFile } from '@orama/plugin-data-persistence/server';

const db = await create({
  schema: { title:'string', body:'string', tags:'string[]', embedding:'vector[384]' },
  components: {
    tokenizer: { language: 'english' },
  },
});

await insert(db, { title: 'SSO setup', body: '...', tags:['auth'], embedding: [/*...*/] });

const results = await search(db, { term: 'single sign on', mode: 'hybrid' });
```

### Recipe 10: Federated search across multiple product indices

```bash
# Algolia Multi-Index Query
curl -X POST "https://${ALGOLIA_APP_ID}-dsn.algolia.net/1/indexes/*/queries" \
  -H "X-Algolia-Application-Id: $ALGOLIA_APP_ID" \
  -H "X-Algolia-API-Key: $ALGOLIA_SEARCH_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"requests":[
    {"indexName":"docs-product-a","query":"webhook","params":"hitsPerPage=5"},
    {"indexName":"docs-product-b","query":"webhook","params":"hitsPerPage=5"}
  ]}'
```

### Recipe 11: Autocomplete on top-50 queries

```javascript
// algoliasearch-helper
const helper = algoliasearchHelper(client, 'acme', { hitsPerPage: 7 });
helper.setQueryParameter('queryType', 'prefixAll');
helper.setQueryParameter('attributesToHighlight', ['title','h1']);
```

## Examples

### Example 1: Audit + fix bad search

**Goal:** no-result rate is 23%, CTR is 41%. Cut no-result to <10%, raise CTR to >60%.

**Steps:**
1. Pull no-result-7d.tsv (Recipe 6); top 50 are the gap list.
2. Bucket no-result terms: (a) typos (add to typo tolerance), (b) synonyms (push to Rules API), (c) missing content (open issues for authors).
3. Push synonyms (Recipe 2 or 7).
4. Pull top-searched + CTR per page (Recipe 5).
5. Pages with position 1 + CTR <40% have title/snippet mismatch — rewrite title + meta.
6. Set custom ranking (Recipe 3) on views_30d + helpful_pct.
7. Re-pull after 7d; verify no-result <10%, CTR >60%.

**Result:** Synonyms cover 80% of no-result; remaining 20% become content roadmap.

### Example 2: Migrate from Algolia to Typesense (cost)

**Goal:** $300/mo Algolia bill → self-hosted Typesense.

**Steps:**
1. `docker run typesense/typesense:0.25.2`.
2. Export Algolia index: `algolia objects browse --indexName acme > export.json`.
3. Import to Typesense: `curl -X POST http://localhost:8108/collections/docs/documents/import?action=upsert -d @export.json`.
4. Port synonyms (Recipe 4).
5. Swap search-UI client to `typesense-instantsearch-adapter`.
6. A/B for 2 weeks; sunset Algolia.

**Result:** $0 + $40/mo VPS instead of $300/mo.

## Edge cases / gotchas

- **Algolia DocSearch only free for OSS** — closed-source = paid Algolia (>$30/mo for tiny indexes; scales fast).
- **JS-rendered SPAs** — Algolia crawler needs `renderJavaScript:true` (paid plan only); prefer SSR.
- **Synonyms cap on Algolia** — 100 per index on free; 5000+ on Build plan.
- **Typesense memory** — RAM-resident; budget 1.5× index size.
- **MeiliSearch typo tolerance default** — tries 1 typo for ≥5-char words, 2 typos for ≥9. Tune per language.
- **Pagefind index size** — keep under 5MB total (browser-side download); use `data-pagefind-meta` to control extracted fields.
- **Insights API needs analytics-only API key**, not the admin key.
- **Index name collisions in federated search** — namespace by `docs-` prefix per product.
- **Synonym pruning** — review monthly; remove synonyms with zero fires.
- **Don't index archived content** — but keep in search if banner clearly states "archived"; configurable via filter.

## Sources

- Algolia DocSearch: https://docsearch.algolia.com/
- Algolia Synonyms API: https://www.algolia.com/doc/api-reference/api-methods/synonyms/
- Algolia Insights: https://www.algolia.com/doc/rest-api/analytics/
- Typesense synonyms: https://typesense.org/docs/0.25.2/api/synonyms.html
- MeiliSearch settings: https://www.meilisearch.com/docs/reference/api/settings
- Pagefind: https://pagefind.app/
- Orama: https://docs.orama.com/
- Comparison (2025): https://typesense.org/typesense-vs-algolia/
