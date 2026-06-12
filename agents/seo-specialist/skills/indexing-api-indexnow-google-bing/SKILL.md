<!--
Source: https://developers.google.com/search/apis/indexing-api/v3/quickstart
Source: https://www.indexnow.org/documentation
Source: https://www.bing.com/webmasters/help/url-submission-api-3a9bea73
Depth: Google Indexing API + Bing IndexNow + Bing Webmaster API at scale
-->
# Indexing API — Google Indexing + Bing IndexNow + Webmaster

## When to use

Reach for this skill when the user asks for: "submit URLs to Google", "Indexing API", "IndexNow", "Bing submit URLs", "instant indexing", "ping Yandex", "Naver indexing", "after migration submit URLs", "programmatic SEO indexing rollout", "request reindex". This is the depth specialist — covers Google Indexing API (200/day default + quota request), Bing IndexNow (free + instant + supports Yandex / Naver), Bing Webmaster Tools API (bulk submission). Submit per-page after content publish; batch after migration; daily during programmatic SEO rollout.

## Setup

```bash
# Google Indexing API via Suganthan GSC MCP (preferred wrapper)
npx suganthan-gsc-mcp@2.2.2 --help
# Setup: OAuth + enable Google Indexing API in GCP
# console.cloud.google.com/apis/library/indexing.googleapis.com

# Bing IndexNow
# Generate IndexNow key
openssl rand -hex 16  # 32-character hex
# Host at https://example.com/<key>.txt with key as file content

# Bing Webmaster Tools API
# Sign up at https://www.bing.com/webmasters/about; verify property
export BING_WEBMASTER_API_KEY="<from bing.com/webmasters/api-settings>"
```

Auth/pricing summary:
- Google Indexing API — free; 200/day default quota; request increase at https://support.google.com/webmasters/contact/indexing-api-quota
- Bing IndexNow — free; no quota documented; supports Yandex + Naver via same protocol
- Bing Webmaster Tools API — free; 10K URLs/day

## Common recipes

### Recipe 1: Google Indexing API — single URL submit
```bash
# Via Suganthan GSC MCP
mcp tool suganthan-gsc.submit_url \
  --url "https://example.com/new-post" \
  --type "URL_UPDATED"

# Direct API
curl -X POST "https://indexing.googleapis.com/v3/urlNotifications:publish" \
  -H "Authorization: Bearer $GSC_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url":"https://example.com/new-post",
    "type":"URL_UPDATED"
  }'
```
`URL_UPDATED` = new or modified; `URL_DELETED` = removed (sends 410 signal).

### Recipe 2: Google Indexing API — batch submit (Suganthan wrapper)
```bash
# Suganthan handles batching against 200/day quota
mcp tool suganthan-gsc.submit_batch \
  --urls_file "@/tmp/urls-to-index.txt" \
  --type "URL_UPDATED"
# urls-to-index.txt: one URL per line
```

```python
# Direct batch via Google Indexing API (rate-limited at 100 calls/100 sec)
import requests, time

def batch_submit_google(urls, gsc_token, batch_size=100):
    submitted = []
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i+batch_size]
        for url in batch:
            r = requests.post(
                'https://indexing.googleapis.com/v3/urlNotifications:publish',
                headers={'Authorization': f'Bearer {gsc_token}','Content-Type':'application/json'},
                json={'url': url, 'type': 'URL_UPDATED'}
            )
            submitted.append({'url': url, 'status': r.status_code, 'response': r.json()})
        time.sleep(60)  # spread to avoid quota
    return submitted
```

### Recipe 3: Bing IndexNow — single URL
```bash
# Generate + host key first (one-time)
KEY=$(openssl rand -hex 16)
echo "$KEY" > /var/www/example.com/$KEY.txt

# Submit single URL
curl -X POST "https://api.indexnow.org/indexnow?url=https://example.com/page&key=$KEY"

# Also works via Bing direct
curl -X POST "https://www.bing.com/indexnow?url=https://example.com/page&key=$KEY"

# Yandex
curl -X POST "https://yandex.com/indexnow?url=https://example.com/page&key=$KEY"
```

### Recipe 4: Bing IndexNow — batch URL submission
```bash
# JSON POST for multiple URLs
curl -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json" \
  -d '{
    "host":"example.com",
    "key":"'$KEY'",
    "keyLocation":"https://example.com/'$KEY'.txt",
    "urlList":[
      "https://example.com/page-1",
      "https://example.com/page-2",
      "https://example.com/page-3"
    ]
  }'

# Returns 200 OK if accepted; 202 if processing; 400/422 invalid
```
Up to 10,000 URLs per batch request. Multiple batches per day fine.

### Recipe 5: Bing Webmaster Tools API — bulk submit
```bash
curl -X POST "https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlBatch?apikey=$BING_WEBMASTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "siteUrl":"https://example.com",
    "urlList":[
      "https://example.com/page-1",
      "https://example.com/page-2"
    ]
  }'
```
Up to 10K URLs/day. Bing Webmaster requires verified property.

### Recipe 6: IndexNow CMS plugin alternative
```
For sites on WordPress / Wix / Cloudflare, native IndexNow support exists:
- WordPress: install "IndexNow" plugin OR All in One SEO / Yoast SEO
- Cloudflare: Speed > Optimization > IndexNow (auto-ping all changed URLs)
- Wix: native; auto-pings on publish
- Shopify: via app
- Squarespace: not native; manual

Auto-ping on every URL change recommended for content-heavy sites.
```

### Recipe 7: Submission rollout for programmatic SEO launch
```python
# 8000 new URLs to submit across 40 days
import os

all_urls = open('all-new-urls.txt').read().splitlines()
chunks = [all_urls[i:i+200] for i in range(0, len(all_urls), 200)]

# Daily cron
def daily_submit(chunk_index):
    chunk = chunks[chunk_index]

    # Google Indexing API (200/day)
    with open('/tmp/today-batch.txt','w') as f:
        f.write('\n'.join(chunk))
    subprocess.run([
        'mcp','tool','suganthan-gsc.submit_batch',
        '--urls_file','@/tmp/today-batch.txt',
        '--type','URL_UPDATED'
    ])

    # Bing IndexNow (no quota; all 200 in one request)
    requests.post('https://api.indexnow.org/indexnow',
        json={'host':'example.com','key':KEY,'keyLocation':f'https://example.com/{KEY}.txt','urlList': [f'https://example.com{p}' for p in chunk]}
    )

    # Mark submitted in DB
    db.execute("UPDATE pages SET submitted_at=NOW() WHERE slug IN (%s)" %
               ','.join(["'%s'" % p for p in chunk]))

# Cron daily for 40 days
```

### Recipe 8: Sitemap submission via API
```bash
# Google: submit sitemap (also done via Search Console UI)
mcp tool suganthan-gsc.submit_sitemap \
  --site_url "sc-domain:example.com" \
  --sitemap_url "https://example.com/sitemap.xml"

# Bing: submit sitemap via Webmaster API
curl -X POST "https://ssl.bing.com/webmaster/api.svc/json/SubmitFeed?apikey=$BING_WEBMASTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"siteUrl":"https://example.com","feedUrl":"https://example.com/sitemap.xml"}'

# IndexNow: include sitemap URL via standard URL submit
curl "https://api.indexnow.org/indexnow?url=https://example.com/sitemap.xml&key=$KEY"
```

### Recipe 9: Confirm submission accepted
```bash
# Google: GSC URL Inspection API (see js-rendering-csr-ssr-ssg-isr-indexing-impact skill)
curl -X POST "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect" \
  -H "Authorization: Bearer $GSC_TOKEN" \
  -d '{"inspectionUrl":"https://example.com/page","siteUrl":"sc-domain:example.com"}'
# Look for: indexStatusResult.lastCrawlTime (Google saw it after submit)

# Bing: Webmaster API URL status
curl "https://ssl.bing.com/webmaster/api.svc/json/GetUrlInfo?apikey=$BING_WEBMASTER_API_KEY&siteUrl=https://example.com&urlList=[\"https://example.com/page\"]"
```

### Recipe 10: Quota tracking for Google Indexing API
```python
# Track usage to stay under daily quota
import datetime, json

QUOTA_FILE = '/tmp/google-indexing-quota.json'

def submit_with_quota_track(url, gsc_token):
    # Load today's usage
    today = datetime.date.today().isoformat()
    try:
        usage = json.load(open(QUOTA_FILE))
    except FileNotFoundError:
        usage = {}

    today_count = usage.get(today, 0)
    if today_count >= 200:
        print(f"Quota exceeded: {today_count}/200")
        return None

    # Submit
    r = requests.post(
        'https://indexing.googleapis.com/v3/urlNotifications:publish',
        headers={'Authorization': f'Bearer {gsc_token}'},
        json={'url': url, 'type': 'URL_UPDATED'}
    )

    if r.status_code == 200:
        usage[today] = today_count + 1
        json.dump(usage, open(QUOTA_FILE,'w'))
    elif r.status_code == 429:
        print('Rate limited — try again later')
    elif r.status_code == 403 and 'Quota exceeded' in r.text:
        print('Daily quota exceeded')

    return r
```

### Recipe 11: Quota increase request (Google Indexing API)
```
1. Go to https://support.google.com/webmasters/contact/indexing-api-quota
2. Fill form with:
   - Property URL
   - Current quota usage pattern (200/day with 8000-page backlog)
   - Use case (programmatic SEO, JobPosting, Livestream, or general content)
   - Site authority signals (DR, organic traffic, GSC verification)
3. Wait 5-15 business days for response
4. Approved quotas: typically 500-5000/day; rare cases up to 25K/day
```

### Recipe 12: Naver / Yandex / Baidu submission
```bash
# Naver (South Korea)
curl -X POST "https://searchadvisor.naver.com/indexnow?url=https://example.com/page&key=$KEY"

# Yandex (Russia)
curl -X POST "https://yandex.com/indexnow?url=https://example.com/page&key=$KEY"

# Baidu (China) — separate protocol, not IndexNow-compatible
# Baidu Tuiding API: must register at https://ziyuan.baidu.com
curl -H "Content-Type: text/plain" \
  --data-binary "https://example.com/page" \
  "http://data.zz.baidu.com/urls?site=https://example.com&token=$BAIDU_TOKEN"
```

## Examples

### Example 1: Programmatic SEO launch (8000 URLs over 40 days)
**Goal:** Submit all 8000 new URLs via Google Indexing API + IndexNow.

**Steps:**
1. Request Google Indexing API quota increase to 500/day (Recipe 11).
2. Recipe 7: daily cron submitting 500 URLs to Google, all 500 to IndexNow.
3. Mirror submissions to Bing Webmaster API (Recipe 5).
4. Track in DB: submitted_at timestamp.
5. After 16 days (8000/500): all submitted.
6. Recipe 9: spot-check via URL Inspection on samples.

**Result:** All 8000 indexed within 30-45 days vs 90-180 days passive.

### Example 2: Post-content-refresh resubmission
**Goal:** Refreshed 20 articles; want Google + Bing to re-crawl.

**Steps:**
1. Recipe 1 per article: Google Indexing API `URL_UPDATED`.
2. Recipe 3 per article: Bing IndexNow.
3. Wait 7-14 days for ranking signals to update.
4. Track via Suganthan GSC `content_decay` reversal (`content-decay-detection-refresh` skill).

**Result:** Faster ranking signal refresh after content updates.

### Example 3: Site migration day-0 rollout
**Goal:** 5000 new URLs post-migration; rapid indexing.

**Steps:**
1. Day 0: Recipe 7 chunked rollout starts (200-500/day depending on quota).
2. Bing IndexNow in single 5000-URL batch (no quota).
3. Bing Webmaster API: 5000 URLs in single call.
4. Recipe 8: submit new sitemap to all engines.
5. Daily monitoring via Suganthan GSC `index_coverage`.

**Result:** Migration indexing 2-3× faster than passive crawl.

## Edge cases / gotchas

- **Google Indexing API officially Job/Livestream-only** — docs state for JobPosting + BroadcastEvent schema only; in practice, Google accepts general URLs but uses it as a "request reindex" hint not a guarantee.
- **200/day quota is PER PROPERTY** — multi-property sites stack quotas.
- **`URL_UPDATED` vs `URL_DELETED`** — `URL_DELETED` sends 410 signal; only for genuinely removed pages.
- **IndexNow key must be hosted at site root** — `https://example.com/<key>.txt` returning the key as file content. 404 here = IndexNow rejects.
- **IndexNow doesn't guarantee crawl** — submission accepted ≠ Googlebot crawled. Use Search Console URL Inspection for verification.
- **Bing IndexNow shared with Yandex + Naver** — single key works across all three IndexNow-protocol search engines.
- **Bing Webmaster API requires property verification** — DNS / HTML file / meta tag.
- **Indexing API + sitemap not redundant** — sitemap is "discoverable URL list"; Indexing API is "please re-crawl this URL now." Use both.
- **Quota errors return 403 with specific message** — distinguish "rate limit" (429) from "quota" (403 + "Quota exceeded for quota metric...").
- **Sitemap pinging deprecated** — `https://www.google.com/ping?sitemap=...` removed by Google Aug 2023. Submit via GSC UI or API only.
- **Baidu indexing separate** — IndexNow not supported; uses Baidu Tuiding API with separate token.
- **Don't submit URLs that aren't ready** — submitting + immediately getting 404'd / noindex'd / robots-blocked URL wastes quota + signal.

## Sources

- [Google Indexing API quickstart](https://developers.google.com/search/apis/indexing-api/v3/quickstart)
- [Google Indexing API reference](https://developers.google.com/search/apis/indexing-api/v3/reference)
- [Google Indexing API quota request](https://support.google.com/webmasters/contact/indexing-api-quota)
- [Bing IndexNow documentation](https://www.indexnow.org/documentation)
- [Microsoft — IndexNow announcement](https://blogs.bing.com/webmaster/october-2021/IndexNow-Instantly-Index-your-web-content-in-Search-Engines)
- [Bing Webmaster Tools URL Submission API](https://www.bing.com/webmasters/help/url-submission-api-3a9bea73)
- [Suganthan GSC MCP v2.2.2](https://suganthan.com/blog/google-search-console-mcp-server/)
- [Naver Search Advisor](https://searchadvisor.naver.com/)
- [Yandex Webmaster](https://yandex.com/dev/webmaster/)
- [Baidu Tuiding API](https://ziyuan.baidu.com/linksubmit/index)
- [Google — sitemap pinging deprecated 2023](https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping)
