---
name: kb-seo-aeo-geo-public-ranking
description: Public KB SEO + AEO/GEO — Schema.org Article/FAQPage/HowTo JSON-LD, llms.txt for ChatGPT/Perplexity citation, canonical URLs, breadcrumbs, topic clusters, Ahrefs/SEMrush rank tracking, AthenaHQ for AEO citation share. Use when KB needs Google + AI-search visibility.
---

# KB SEO / AEO / GEO — public-ranking + AI-search citation

## When to use

User says "KB SEO", "rank in Google", "AI citation", "AEO", "Perplexity should cite us", "llms.txt", "structured data for docs". Defer pure marketing-SEO to `seo-specialist`. This skill is specifically the KB / docs-site overlay.

## Setup

```bash
# JSON-LD helpers
pipx install python-frontmatter pyld
npm i -g schema-dts-gen

# Rank tracking (paid)
# Ahrefs: https://ahrefs.com/api ($500+/mo)
# SEMrush: https://www.semrush.com/api/ (paid)

# Free AEO: SerpAPI for rank checks (limited free tier)
pipx install google-search-results

# AthenaHQ for AEO
# https://athenahq.ai/  (paid)
```

Auth / API key requirements:
- `AHREFS_TOKEN` (paid)
- `SEMRUSH_KEY` (paid)
- `ATHENAHQ_TOKEN` (paid)
- `SERPAPI_KEY` (free 100/mo)

## Common recipes

### Recipe 1: Schema.org Article JSON-LD

```html
<!-- per-article head injection -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "Set up SSO with Okta",
  "datePublished": "2026-04-01",
  "dateModified": "2026-06-09",
  "author": {"@type":"Organization","name":"Acme"},
  "publisher": {"@type":"Organization","name":"Acme","logo":{"@type":"ImageObject","url":"https://acme.com/logo.png"}},
  "mainEntityOfPage": {"@type":"WebPage","@id":"https://docs.acme.com/how-to/authentication/sso-okta"},
  "image": "https://docs.acme.com/og/sso-okta.png"
}
</script>
```

### Recipe 2: HowTo schema for tutorial articles

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "Set up SSO with Okta",
  "totalTime": "PT15M",
  "step": [
    {"@type":"HowToStep","name":"Create an Okta app","text":"In Okta admin..."},
    {"@type":"HowToStep","name":"Add SAML config","text":"Paste the metadata..."},
    {"@type":"HowToStep","name":"Test login","text":"Click sign in with Okta."}
  ]
}
</script>
```

### Recipe 3: FAQPage schema for Q&A pages

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {"@type":"Question","name":"What is SSO?","acceptedAnswer":{"@type":"Answer","text":"Single sign-on is..."}},
    {"@type":"Question","name":"Does Okta support SCIM?","acceptedAnswer":{"@type":"Answer","text":"Yes..."}}
  ]
}
</script>
```

### Recipe 4: Auto-inject JSON-LD via Docusaurus plugin

```javascript
// src/plugins/json-ld-plugin/index.js
module.exports = function() {
  return {
    name: 'json-ld-plugin',
    async contentLoaded({content, actions}) {
      actions.setGlobalData(content);
    },
    injectHtmlTags() {
      return {
        headTags: [{
          tagName: 'script',
          attributes: {type:'application/ld+json'},
          innerHTML: JSON.stringify({"@context":"https://schema.org","@type":"WebSite",...}),
        }],
      };
    },
  };
};
```

### Recipe 5: llms.txt at site root

```bash
cat > public/llms.txt <<'EOF'
# Acme docs

> Acme provides API + SDKs for [domain]. The docs cover get-started, how-to, concept, reference, and troubleshooting.

## Get started
- [Quickstart](https://docs.acme.com/get-started/quickstart): 5-min hands-on.
- [First integration](https://docs.acme.com/get-started/first-integration): build the canonical example.

## How-to
- [SSO with Okta](https://docs.acme.com/how-to/authentication/sso-okta)
- [Webhook retry strategy](https://docs.acme.com/how-to/webhooks/retry-strategy)

## Reference
- [REST API](https://docs.acme.com/reference/api)
- [Webhook event types](https://docs.acme.com/reference/webhook-events)

## Optional
- [llms-full.txt](https://docs.acme.com/llms-full.txt): full text of all docs for ingestion.
EOF
```

### Recipe 6: llms-full.txt generation

```python
# scripts/generate-llms-full.py
import pathlib
out = pathlib.Path('public/llms-full.txt')
parts = []
for p in sorted(pathlib.Path('docs').rglob('*.md')):
    if '_archived' in p.parts: continue
    parts.append(f"# {p.stem}\n\n{p.read_text()}\n\n---\n\n")
out.write_text('\n'.join(parts))
```

### Recipe 7: Canonical + meta description per page

```yaml
---
title: "Set up SSO with Okta"
slug: how-to/authentication/sso-okta
description: "Step-by-step guide to configure Okta SAML SSO with Acme. Includes troubleshooting common errors."
canonical: https://docs.acme.com/how-to/authentication/sso-okta
---
```

### Recipe 8: Breadcrumb schema

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type":"ListItem","position":1,"name":"Docs","item":"https://docs.acme.com/"},
    {"@type":"ListItem","position":2,"name":"How-to","item":"https://docs.acme.com/how-to"},
    {"@type":"ListItem","position":3,"name":"Authentication","item":"https://docs.acme.com/how-to/authentication"},
    {"@type":"ListItem","position":4,"name":"SSO with Okta"}
  ]
}
</script>
```

### Recipe 9: Sitemap.xml

```bash
# Most static-site generators emit; if not:
python -c "
import pathlib, datetime
print('<?xml version=\"1.0\" encoding=\"UTF-8\"?>')
print('<urlset xmlns=\"http://www.sitemaps.org/schemas/0.9\">')
for p in pathlib.Path('docs').rglob('*.md'):
    if '_archived' in p.parts: continue
    url = 'https://docs.acme.com/' + str(p.with_suffix('')).replace('\\\\','/')
    print(f'<url><loc>{url}</loc><lastmod>{datetime.date.today()}</lastmod></url>')
print('</urlset>')
" > public/sitemap.xml
```

### Recipe 10: Ahrefs rank tracking

```bash
curl -G "https://api.ahrefs.com/v3/site-explorer/positions" \
  -H "Authorization: Bearer $AHREFS_TOKEN" \
  --data-urlencode "target=docs.acme.com" \
  --data-urlencode "country=us" \
  --data-urlencode "limit=100" \
  | jq '.positions[] | {keyword, position, url}'
```

### Recipe 11: AthenaHQ AEO citation share

```bash
curl -X POST "https://api.athenahq.ai/v1/citations/search" \
  -H "Authorization: Bearer $ATHENAHQ_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "queries":["how to set up SSO Okta","webhook retry strategy"],
    "models":["chatgpt","perplexity","gemini","claude"],
    "domain_filter":"docs.acme.com"
  }'
```

### Recipe 12: Free AEO check via SerpAPI

```bash
curl "https://serpapi.com/search.json?engine=google&q=how+to+set+up+SSO+okta&api_key=$SERPAPI_KEY" \
  | jq '.organic_results[] | select(.link | contains("docs.acme.com")) | {position, title, snippet}'
```

### Recipe 13: Topic-cluster internal linking

```python
# scripts/topic-cluster-check.py
import pathlib, re, frontmatter
PILLAR = 'concept/how-auth-works.md'    # pillar article
pillar = pathlib.Path(f'docs/{PILLAR}')
spokes = []
for p in pathlib.Path('docs/how-to/authentication').rglob('*.md'):
    post = frontmatter.load(p)
    body = post.content
    if PILLAR.replace('.md','') not in body:
        spokes.append(p)
print("Spokes missing link back to pillar:")
for p in spokes: print(p)
```

## Examples

### Example 1: Make docs citable by ChatGPT / Perplexity

**Goal:** Increase AEO citation share from <5% to >30%.

**Steps:**
1. Add llms.txt + llms-full.txt (Recipes 5, 6).
2. Inject Schema.org per page (Recipes 1-3, 8).
3. Ensure canonical + meta description (Recipe 7).
4. Submit sitemap.xml to GSC + Bing Webmaster Tools (Recipe 9).
5. Track AEO via AthenaHQ (Recipe 11) or free SerpAPI for SGE/AIO presence (Recipe 12).
6. Iterate weekly: rewrite top-search articles missing AI citation.

**Result:** Docs cited in 30%+ of brand-relevant AI answers.

### Example 2: Topic-cluster build-out

**Goal:** Pillar article + 10 spoke how-tos all interlinked.

**Steps:**
1. Define pillar (Concept: "How auth works").
2. Identify spokes (every How-to in auth section).
3. Add canonical link to pillar from each spoke (Recipe 13).
4. Internal-link pillar back to each spoke.
5. Track pillar rank weekly (Recipe 10).

**Result:** Cluster ranks 1-3 organically for ~50 long-tail auth queries.

## Edge cases / gotchas

- **Google deprecated HowTo rich results** for many categories in 2024 — schema is still indexed but visible rich-result eligibility limited. Don't over-invest.
- **llms.txt is a proposal, not a standard** — Anthropic, OpenAI, Perplexity discuss support; no formal RFC. Ship anyway; cost is trivial.
- **JSON-LD validation** — use Google's Rich Results Test before shipping.
- **Canonical confusion in versioned docs** — point legacy versions to current; or self-canonical with `noindex` on legacy. Pick one.
- **Sitemap fresh-stamp** — `<lastmod>` should reflect content change, not build time. Use git log timestamp.
- **AthenaHQ / Profound paid only** — for free baseline, manually query ChatGPT/Perplexity weekly and grep brand mentions.
- **JS-rendered JSON-LD** — Google fetches rendered; Bing fetches raw. SSR is safer.
- **Breadcrumb schema and breadcrumb HTML must match** — Google's Rich Results Test flags mismatch.
- **Internal-link explosion** — over-linking inflates noise; ~3-7 contextual internal links per article is the sweet spot.

## Sources

- Schema.org Article: https://schema.org/Article
- Schema.org HowTo: https://schema.org/HowTo
- Schema.org FAQPage: https://schema.org/FAQPage
- Google Rich Results Test: https://search.google.com/test/rich-results
- llms.txt standard proposal: https://llmstxt.org/
- AthenaHQ AEO: https://docs.athenahq.ai/
- Profound AEO: https://www.tryprofound.com/
- Ahrefs API: https://ahrefs.com/api/documentation
- SEMrush API: https://www.semrush.com/api-documentation/
- SerpAPI: https://serpapi.com/search-api
- Topic cluster (HubSpot): https://blog.hubspot.com/marketing/topic-clusters-seo
