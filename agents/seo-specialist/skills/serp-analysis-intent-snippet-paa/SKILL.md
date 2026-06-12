<!--
Source: https://docs.dataforseo.com/v3/serp/google/organic/live/regular/
Source: https://developers.google.com/search/docs/appearance/featured-snippet
Source: https://serpapi.com/search-api
Depth: SERP feature analysis + intent classification + Featured Snippet + PAA optimization at scale
-->
# SERP Analysis — Intent + Featured Snippet + PAA

## When to use

Reach for this skill when the user asks for: "SERP analysis", "what features are on this SERP", "Featured Snippet opportunity", "People Also Ask questions", "PAA optimization", "what intent does this query have", "snippet reverse-engineering", "image pack opportunity", "video carousel SERP", "Top Stories eligibility", "local pack". This is the depth specialist — uses DataForSEO SERP API ($0.0006/SERP) for programmatic SERP scraping with full feature coverage, captures PAA + Featured Snippet format + competitor URL set per query. Pairs with `schema-org-deep-jsonld-eeat` for FAQPage schema after PAA extraction.

## Setup

```bash
# DataForSEO — primary cheap programmatic SERP scraper
# Sign up at dataforseo.com → API credentials in dashboard
export DFS_LOGIN="<your-login>"
export DFS_PASS="<your-password>"

# SerpAPI — alt with simpler interface, $50+/mo
export SERPAPI_KEY="<from serpapi.com/manage-api-key>"

# Serper.dev — cheapest alt at $50/100K queries
export SERPER_KEY="<from serper.dev/api-key>"

# Apify Google Search SERP Scraper — cheapest fallback
export APIFY_TOKEN="<from console.apify.com/account/integrations>"
```

Auth / pricing:
- `DFS_LOGIN` + `DFS_PASS` — DataForSEO Basic Auth; $0.0006/SERP (Google), prepay $50 min
- `SERPAPI_KEY` — $50/mo for 5000 searches; cleaner JSON; live results
- `SERPER_KEY` — $50 for 100K queries; cheapest reliable; minimal feature coverage

## Common recipes

### Recipe 1: DataForSEO Google SERP with full feature capture
```bash
curl -X POST "https://api.dataforseo.com/v3/serp/google/organic/live/advanced" \
  -u "$DFS_LOGIN:$DFS_PASS" \
  -H "Content-Type: application/json" \
  -d '[{
    "keyword":"marketing automation",
    "location_code":2840,
    "language_code":"en",
    "device":"desktop",
    "depth":100
  }]'
```
`location_code=2840` is US. `depth=100` returns top-100 organic + ALL features (Featured Snippet, PAA, Knowledge Panel, Top Stories, Local Pack, Video Carousel, Image Pack, Shopping Ads, Site Links, Tweets, etc.).

### Recipe 2: Parse SERP features per query
```python
import requests, json

def serp_analysis(keyword):
    r = requests.post(
        "https://api.dataforseo.com/v3/serp/google/organic/live/advanced",
        auth=(DFS_LOGIN, DFS_PASS),
        json=[{"keyword":keyword,"location_code":2840,"language_code":"en","device":"desktop","depth":100}]
    )
    items = r.json()['tasks'][0]['result'][0]['items']

    features = {
        'featured_snippet': [],
        'people_also_ask': [],
        'knowledge_panel': [],
        'top_stories': [],
        'local_pack': [],
        'video_carousel': [],
        'image_pack': [],
        'shopping': [],
    }

    organic_urls = []
    for item in items:
        t = item['type']
        if t == 'organic':
            organic_urls.append({'url':item['url'],'title':item['title'],'position':item['rank_absolute']})
        elif t == 'featured_snippet':
            features['featured_snippet'].append({'url':item.get('url'),'description':item.get('description'),'snippet_type':item.get('featured_title')})
        elif t == 'people_also_ask':
            features['people_also_ask'] = [i['title'] for i in item.get('items',[])]
        elif t in features:
            features[t].append(item)

    return {'organic': organic_urls, 'features': features}

# Run
result = serp_analysis("marketing automation")
print(f"Featured Snippet: {result['features']['featured_snippet']}")
print(f"PAA: {result['features']['people_also_ask']}")
```

### Recipe 3: Intent classification via SERP features (more reliable than Ahrefs heuristic)
```python
def classify_intent_from_serp(serp):
    features = serp['features']

    # Transactional signals
    if features['shopping'] or any('buy' in u['title'].lower() or 'price' in u['title'].lower() for u in serp['organic'][:5]):
        return 'Transactional'

    # Commercial signals
    if any('best' in u['title'].lower() or 'vs' in u['title'].lower() or 'review' in u['title'].lower() for u in serp['organic'][:5]):
        return 'Commercial'

    # Informational signals
    if features['people_also_ask'] or features['featured_snippet']:
        return 'Informational'

    # Navigational signals
    if features['knowledge_panel'] and len(serp['organic']) > 0 and any(t in serp['organic'][0]['title'].lower() for t in ['login','sign in','homepage']):
        return 'Navigational'

    return 'Mixed'
```

### Recipe 4: Featured Snippet reverse-engineering
```python
def fs_format_extraction(serp):
    fs = serp['features']['featured_snippet']
    if not fs: return None

    fs_data = fs[0]
    description = fs_data.get('description','')

    # Format detection
    if '\n• ' in description or description.startswith('• '):
        return {'format': 'list', 'items': [l.strip('• ') for l in description.split('\n') if l.startswith('• ')]}
    if re.match(r'^\d+\.', description):
        return {'format': 'ordered_list', 'items': [...]}
    if '<table' in description.lower():
        return {'format': 'table', 'data': '...'}
    if len(description.split()) < 60:
        return {'format': 'paragraph', 'word_count': len(description.split()), 'content': description}
    return {'format': 'unknown'}

# Use: target a 40-60 word direct answer in first 100 words of your content
# Wrap in <p> tag with <strong> for the answer phrase
```

### Recipe 5: PAA extraction → FAQPage schema generation
```python
def paa_to_faqpage(serp):
    paa_questions = serp['features']['people_also_ask']
    if not paa_questions: return None

    # For each PAA Q, get the expanded answer
    paa_with_answers = []
    for q in paa_questions:
        # DataForSEO returns expanded answers in nested items
        # OR fetch the question's own SERP to get a sample answer
        sample_serp = serp_analysis(q)
        fs = sample_serp['features']['featured_snippet']
        answer = fs[0]['description'] if fs else f"<your answer to '{q}' here>"
        paa_with_answers.append({'q': q, 'a': answer})

    # Generate FAQPage JSON-LD
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type":"Question","name":qa['q'],"acceptedAnswer":{"@type":"Answer","text":qa['a']}}
            for qa in paa_with_answers
        ]
    }
```

### Recipe 6: Competitor URL set per query
```python
# Top-10 competitors for a target keyword
serp = serp_analysis("marketing automation tools")
top_10 = [u['url'] for u in serp['organic'][:10]]
print("Competitors to outrank:")
for i, url in enumerate(top_10, 1):
    print(f"{i}. {url}")

# Cross with Ahrefs site_explorer to see who's strongest
# (`ahrefs-deep-keyword-cluster-research` skill)
```

### Recipe 7: Multi-keyword batch SERP scrape
```bash
# 100 keywords in one batch (DataForSEO advanced endpoint)
curl -X POST "https://api.dataforseo.com/v3/serp/google/organic/live/advanced" \
  -u "$DFS_LOGIN:$DFS_PASS" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --argjson kws "$(cat keywords.json)" '$kws | map({keyword:., location_code:2840, language_code:"en", device:"desktop", depth:30})')"

# Returns array of 100 results in one billing unit (1 task per keyword)
```

### Recipe 8: SerpAPI live results (alt)
```bash
curl "https://serpapi.com/search.json?engine=google&q=marketing+automation&location=United+States&device=desktop&num=100&api_key=$SERPAPI_KEY"
```
Cleaner JSON, simpler params, but ~10× cost of DataForSEO.

### Recipe 9: Serper.dev cheap fallback
```bash
curl -X POST "https://google.serper.dev/search" \
  -H "X-API-KEY: $SERPER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q":"marketing automation","gl":"us","num":100}'
```

### Recipe 10: Track SERP feature ownership over time
```python
# Daily snapshot of who owns Featured Snippet + PAA for tracked keywords
import datetime, pandas as pd

tracked_kws = ['marketing automation','crm software','email marketing']
date = datetime.date.today()

snapshots = []
for kw in tracked_kws:
    serp = serp_analysis(kw)
    fs_url = serp['features']['featured_snippet'][0]['url'] if serp['features']['featured_snippet'] else None
    snapshots.append({
        'date': date,
        'keyword': kw,
        'fs_url': fs_url,
        'paa_count': len(serp['features']['people_also_ask']),
        'organic_1': serp['organic'][0]['url'] if serp['organic'] else None,
    })

pd.DataFrame(snapshots).to_csv(f'serp-snapshot-{date}.csv', index=False)
# Append daily → trend Featured Snippet wins / losses
```

### Recipe 11: Featured Snippet capture targeting workflow
```
Goal: capture Featured Snippet currently owned by competitor

1. Recipe 4: extract FS format (paragraph 40-60 words / list / table / video)
2. Restructure your content:
   - Paragraph FS: add 40-60 word answer in first 100 words, in <p> tag (no bullet, no heading wrap)
   - List FS: structure 4-8 step list in <ol> or <ul>, each item ≤10 words
   - Table FS: data table with <table> markup
3. Add FAQPage schema if PAA also present
4. Submit reindex via Suganthan GSC `submit_url`
5. Monitor via Recipe 10 daily — Google may flip Featured Snippet ownership within 1-7 days
```

### Recipe 12: PAA optimization workflow
```
Goal: rank in PAA carousel for target queries

1. Recipe 5: extract PAA questions + sample answers from current SERP
2. Restructure article with each PAA Q as H2 or H3 immediately followed by 40-80 word answer
3. Add FAQPage JSON-LD with all PAA Qs
4. Submit reindex
5. PAA appearance via Suganthan GSC `serp_features --features paa` → confirm appearance + position

Note: PAA inclusion is sticky once won (vs Featured Snippet which can flip daily)
```

## Examples

### Example 1: SERP feature audit for 20-keyword cluster
**Goal:** Identify feature opportunities (FS, PAA, Image Pack, Video) for content optimization.

**Steps:**
1. Recipe 7: batch SERP scrape for all 20 keywords.
2. Recipe 2 per keyword: extract feature presence.
3. Tabulate: which features appear for which keywords + current owner.
4. Identify gaps: keywords where FS is winnable (low DR owner or weak answer format) or PAA you should expand into.
5. Output recommendation list per keyword → hand to content team.

**Result:** Prioritized SERP-feature opportunity backlog.

### Example 2: Featured Snippet capture for high-impressions / position-2 keyword
**Goal:** Steal the Featured Snippet from current owner.

**Steps:**
1. Recipe 4: reverse-engineer current FS format.
2. Recipe 6: verify your current position is ≤5 (snippets typically pulled from top 10).
3. Restructure content to match format (Recipe 11).
4. Reindex via Suganthan GSC.
5. Recipe 10: daily snapshot → confirm capture within 7-14 days.

**Result:** Featured Snippet capture → typically 20-40% CTR uplift.

### Example 3: Convert PAA questions into FAQPage schema deployment
**Goal:** Add FAQPage schema with PAA answers across content cluster.

**Steps:**
1. Per cluster page: Recipe 5 → extract PAA + generate FAQPage JSON-LD.
2. Inject schema into page templates (defer to `frontend-engineer` for CMS update).
3. Validate via `schema-org-deep-jsonld-eeat` (Recipes 10+11 in that skill).
4. Submit reindex per page via Suganthan GSC batch.
5. Monitor SERP for PAA appearance via Recipe 10.

**Result:** PAA presence + FAQPage rich result eligibility + AEO citation surface.

## Edge cases / gotchas

- **DataForSEO live vs cached** — `live/advanced` is fresh; `regular` is cached (faster, cheaper, may be 24-48h stale). Use `live` for current SERP analysis.
- **`location_code` matters** — `2840` US, `2826` UK, `2124` Canada. Wrong code = wrong SERP. Full list: https://docs.dataforseo.com/v3/serp/google/locations/
- **Featured Snippet sourced from organic 1-10, not always #1** — FS owner often position 2-5. Snippet quality > raw ranking.
- **FAQ rich result reduced Aug 2023** — only well-known authoritative sites get the SERP feature now. Still adds AEO value.
- **PAA carousel position rotates** — same query can show different PAA Qs across requests. Sample 3-5 requests per keyword for stable list.
- **DataForSEO billing per task** — batch endpoint = 1 task per keyword. 100 keywords = 100 tasks = $0.06.
- **SerpAPI residential IPs blocked** — site uses captcha. SerpAPI proxies typically work; if not, fallback to Apify or DataForSEO.
- **Mobile vs desktop SERPs differ significantly** — for mobile-first audit run both `device:"mobile"` and `device:"desktop"`.
- **Google personalization** — DataForSEO uses generic SERP (no user history). Real-user SERP may differ. Use Chrome incognito for verification.
- **Featured Snippet length cap ~290 chars** — paragraph snippets capped. Lists capped at 8 items.
- **Featured Snippet "no-snippet" opt-out** — sites can use `<meta name="robots" content="nosnippet">`. Don't if you want FS.
- **Google "Top Stories" eligibility requires news publisher status** — apply via Publisher Center.

## Sources

- [DataForSEO Google SERP API](https://docs.dataforseo.com/v3/serp/google/organic/live/regular/)
- [DataForSEO advanced SERP endpoint](https://docs.dataforseo.com/v3/serp/google/organic/live/advanced/)
- [DataForSEO locations](https://docs.dataforseo.com/v3/serp/google/locations/)
- [SerpAPI documentation](https://serpapi.com/search-api)
- [Serper.dev API](https://serper.dev/api)
- [Google Search Central — featured snippets](https://developers.google.com/search/docs/appearance/featured-snippet)
- [Google Search Central — FAQ structured data (limited 2023+)](https://developers.google.com/search/docs/appearance/structured-data/faqpage)
- [Apify Google Search Scraper](https://apify.com/apify/google-search-scraper)
