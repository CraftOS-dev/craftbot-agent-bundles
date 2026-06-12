---
name: algolia-doc-search
description: Algolia DocSearch — free hosted search for OSS docs. Crawler config, theming, and the Insights API for top-searched-terms-vs-content-gaps analytics. Use when adding search to a docs site OR auditing search behavior.
---

# Algolia DocSearch + Insights API

Algolia DocSearch is the de facto search for open-source docs sites in 2026. Free for OSS projects, hosted crawler, drop-in search UI for Docusaurus/VitePress/Starlight/MkDocs/Mintlify.

The Insights API surfaces what readers searched for vs what they clicked — high-signal data for closing content gaps.

## When to use this skill

- Add search to a docs site.
- Audit "what do readers search for that we don't have a page for?"
- Cross-reference search queries with low-engagement pages.

## Setup

### Step 1 — Apply for DocSearch (OSS only)

https://docsearch.algolia.com/apply — free for open-source projects. For commercial docs, use a paid Algolia plan and self-configure the crawler.

After approval, Algolia provisions:

- An `appId`.
- A search-only API key (`apiKey`).
- An index name.
- A crawler that runs on a schedule.

### Step 2 — Wire the search UI

#### Docusaurus

```javascript
// docusaurus.config.js
themeConfig: {
  algolia: {
    appId: 'XXXXXXXXXX',
    apiKey: 'aaaaaaaaaaaaaaaaaaaaaaaa',
    indexName: 'acme',
    contextualSearch: true,         // restrict by current docs version + locale
    searchPagePath: 'search',
    insights: true,                  // enable Insights tracking
  },
},
```

#### VitePress

```typescript
themeConfig: {
  search: {
    provider: 'algolia',
    options: {
      appId: 'XXXXXXXXXX',
      apiKey: 'aaaaaaaaaaaaaaaaaaaaaaaa',
      indexName: 'acme',
      insights: true,
    },
  },
},
```

#### Starlight

```javascript
import starlight from '@astrojs/starlight';
import starlightDocSearch from '@astrojs/starlight-docsearch';

export default defineConfig({
  integrations: [starlight({
    plugins: [starlightDocSearch({
      appId: 'XXXXXXXXXX',
      apiKey: 'aaaaaaaaaaaaaaaaaaaaaaaa',
      indexName: 'acme',
    })],
  })],
});
```

#### MkDocs Material

```yaml
extra:
  algolia:
    appId: XXXXXXXXXX
    apiKey: aaaaaaaaaaaaaaaaaaaaaaaa
    indexName: acme
```

### Step 3 — Crawler config (self-hosted Algolia or DocSearch managed)

```json
// crawler.json
{
  "appId": "XXXXXXXXXX",
  "apiKey": "<admin key>",
  "rateLimit": 8,
  "startUrls": ["https://docs.example.com/"],
  "renderJavaScript": false,
  "sitemaps": ["https://docs.example.com/sitemap.xml"],
  "ignoreCanonicalTo": false,
  "discoveryPatterns": ["https://docs.example.com/**"],
  "schedule": "at 06:00 every 1 day",
  "actions": [{
    "indexName": "acme",
    "pathsToMatch": ["https://docs.example.com/**"],
    "recordExtractor": {
      "_source": "docsearch-recommended"
    }
  }]
}
```

DocSearch ships a recommended record extractor that picks up h1/h2/h3 hierarchy and content automatically.

## Common recipes — search analytics with the Insights API

### Recipe 1: Top searched terms

```bash
curl -X GET 'https://insights.algolia.io/1/searches/top-searches' \
  -H "X-Algolia-Application-Id: $ALGOLIA_APP_ID" \
  -H "X-Algolia-API-Key: $ALGOLIA_ADMIN_KEY" \
  -G \
  --data-urlencode 'index=acme' \
  --data-urlencode 'startDate=2026-05-01' \
  --data-urlencode 'endDate=2026-05-31' \
  --data-urlencode 'limit=50'
```

Returns: `[{ search: "webhook", count: 432, clickThroughRate: 0.31, ... }]`.

### Recipe 2: Searches with NO clicks ("we have no answer")

```bash
curl -X GET 'https://insights.algolia.io/1/searches/noClicks' \
  -H "X-Algolia-Application-Id: $ALGOLIA_APP_ID" \
  -H "X-Algolia-API-Key: $ALGOLIA_ADMIN_KEY" \
  -G \
  --data-urlencode 'index=acme' \
  --data-urlencode 'startDate=2026-05-01' \
  --data-urlencode 'endDate=2026-05-31'
```

Every entry here is a missing doc page. Treat as a bug.

### Recipe 3: Searches with NO results

```bash
curl -X GET 'https://insights.algolia.io/1/searches/noResults' \
  -H "X-Algolia-Application-Id: $ALGOLIA_APP_ID" \
  -H "X-Algolia-API-Key: $ALGOLIA_ADMIN_KEY" \
  -G \
  --data-urlencode 'index=acme' \
  --data-urlencode 'startDate=2026-05-01' \
  --data-urlencode 'endDate=2026-05-31'
```

These are searches where Algolia returned nothing. Either:

- The content exists but isn't indexed (crawler config bug).
- The content doesn't exist (write it).
- The user used a synonym Algolia doesn't know (add a synonym).

### Recipe 4: Filter by user segment

If the docs distinguish between authenticated/unauthenticated readers, segment queries:

```bash
--data-urlencode 'tags=segment:authenticated'
```

### Recipe 5: Add synonyms

```bash
curl -X PUT "https://${ALGOLIA_APP_ID}.algolia.net/1/indexes/acme/synonyms/syn-webhook" \
  -H "X-Algolia-Application-Id: $ALGOLIA_APP_ID" \
  -H "X-Algolia-API-Key: $ALGOLIA_ADMIN_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "objectID": "syn-webhook",
    "type": "synonym",
    "synonyms": ["webhook", "callback", "event handler"]
  }'
```

Now searches for "callback" surface webhook docs.

### Recipe 6: Click-through rate per page

```bash
curl -X GET 'https://insights.algolia.io/1/clicks/positions' \
  -H "X-Algolia-Application-Id: $ALGOLIA_APP_ID" \
  -H "X-Algolia-API-Key: $ALGOLIA_ADMIN_KEY" \
  -G \
  --data-urlencode 'index=acme' \
  --data-urlencode 'startDate=2026-05-01' \
  --data-urlencode 'endDate=2026-05-31'
```

Position 1 with low CTR = the SERP snippet doesn't match the query intent. Rewrite the page title + meta description.

## Open-source alternatives

If the user can't / won't use Algolia:

| Tool | Setup |
|---|---|
| **Pagefind** | `npx pagefind --site dist/`; pure JS, no server, default for Starlight |
| **MeiliSearch** | self-host (Docker), instant search, multilingual |
| **Typesense** | self-host or cloud, near-Algolia ergonomics |
| **Orama** | embed in the app bundle, search runs in-browser |
| **Lunr.js** | Material's default; small projects only |

For most projects under 5k pages, Pagefind is the best free choice.

## Insights for non-Algolia search

- **Pagefind:** no built-in analytics; pair with Microsoft Clarity (see `microsoft-clarity-doc-analytics`) and instrument click events.
- **MeiliSearch:** Cloud plan ships search analytics; self-hosted requires custom logging.
- **Typesense:** Cloud plan ships analytics; self-hosted has `search.json` logging.

## Common recipes — combine with content audit

### Recipe 7: Build a "content gap" report

```bash
# 1. Pull top no-result searches from Algolia
NO_RESULT=$(curl ... noResults endpoint)

# 2. Cross-reference with existing pages
EXISTING=$(git ls-files docs/ | xargs grep -l -i 'webhook' 2>/dev/null)

# 3. Surface the gaps
echo "$NO_RESULT" | jq -r '.searches[] | .search' | while read q; do
  if ! echo "$EXISTING" | grep -qi "$q"; then
    echo "MISSING: $q (searched X times)"
  fi
done
```

## Edge cases

- **Index size limits:** DocSearch free tier indexes up to ~1M records. Most docs sites are well under.
- **Versioned docs:** use `facetFilters: ['version:latest']` to scope search to current version.
- **JS-rendered SPAs:** crawler config `renderJavaScript: true` (paid plans only); prefer SSR / static export.
- **PII in URLs:** strip query params from indexed URLs via crawler config.
- **MkDocs offline docs:** use Material's built-in `search` plugin; Algolia requires public URLs.

## Sources

- DocSearch: https://docsearch.algolia.com/
- Algolia Insights API: https://www.algolia.com/doc/rest-api/analytics/
- Algolia Crawler: https://www.algolia.com/doc/tools/crawler/
- Pagefind: https://pagefind.app/
- MeiliSearch: https://www.meilisearch.com/
- Typesense: https://typesense.org/
- Orama: https://oramasearch.com/
