<!--
Source: https://www.facebook.com/ads/library/api
Source: https://adstransparency.google.com/
Competitor ad spying: Meta Ad Library API + Google Ads Transparency Center scrape.
-->
# Competitor Ad Spying — Meta Ad Library + Google Transparency — SKILL

The Meta Ad Library API is public, free, commercial-open — every brand's ads are visible. Google Ads Transparency Center is public web (no official API; scrape with `firecrawl-mcp`). This skill ships the queries, the scrape patterns, the categorization framework, and the output catalog for creative inspiration + competitive monitoring.

## When to use this skill

- **Pre-launch competitive scan** — what's working for the top 5 competitors?
- **Creative concept hunt** — reverse-engineer winning hooks.
- **Brand monitoring** — track when key competitors launch new campaigns.
- **Landing-page intel** — what URLs do competitors drive paid traffic to?
- **Quarterly competitive deck** — summary of competitor paid activity.

**Do NOT use this skill when:**
- Political / issue ads — different policy + API path.
- Real-time intel (Ad Library has 24h+ delay).
- Sensitive vertical without legal review (some markets restrict competitor intel).

## Setup

### Meta Ad Library

- Endpoint: `https://graph.facebook.com/v19.0/ads_archive`
- Auth: any Meta access token (`access_token` parameter)
- Rate: 200 calls/hour
- No app review required for commercial ads (only political/issue ads need app review)
- UI version: https://www.facebook.com/ads/library

### Google Ads Transparency Center

- UI: https://adstransparency.google.com/
- No official API — scrape via `firecrawl-mcp` or `brightdata-mcp`
- Per advertiser: `https://adstransparency.google.com/?advertiser={advertiser_id}&region=US`
- Returns: ad copy + display creatives + landing page URLs + last seen dates

### Paid alternatives

- **Pathmatics** — enterprise paid; display + social aggregation
- **WhatRunsWhere** — display ad intel
- **SpyFu** — Google Ads + keyword intel
- **SimilarWeb** — traffic + paid-channel mix

## Common recipes

### Recipe 1: Meta Ad Library — all active ads for a competitor page

```bash
COMPETITOR_PAGE_ID="123456789"

curl "https://graph.facebook.com/v19.0/ads_archive?\
search_page_ids=$COMPETITOR_PAGE_ID&\
ad_active_status=ACTIVE&\
ad_type=ALL&\
ad_reached_countries=['US']&\
fields=id,page_id,page_name,ad_creative_bodies,ad_creative_link_titles,ad_creative_link_descriptions,ad_snapshot_url,ad_delivery_start_time,ad_delivery_stop_time,impressions,spend,publisher_platforms,ad_creative_link_captions&\
access_token=$META_ADLIB_TOKEN&\
limit=500" \
  | jq '.data' > competitor-ads.json
```

Returns: ad copy bodies, headlines, snapshot URLs (clickable images), spend ranges, impression ranges, days running.

### Recipe 2: Meta Ad Library — search by keyword across all pages

```bash
curl "https://graph.facebook.com/v19.0/ads_archive?\
search_terms=skin+care+routine&\
ad_active_status=ACTIVE&\
ad_reached_countries=['US']&\
fields=id,page_id,page_name,ad_creative_bodies,ad_snapshot_url,impressions,spend&\
access_token=$META_ADLIB_TOKEN&\
limit=500"
```

### Recipe 3: Page ID lookup

```bash
# Lookup competitor's Meta Page ID
curl "https://graph.facebook.com/v19.0/pages/search?q=Glossier&access_token=$META_TOKEN"
# Returns: page IDs matching name
```

Alternative: visit `facebook.com/{competitor-handle}` in browser → view source → find `pageID` in HTML.

### Recipe 4: Filter Ad Library by impressions / spend tier

```python
import requests, json

r = requests.get("https://graph.facebook.com/v19.0/ads_archive", params={
  "search_page_ids": COMPETITOR_PAGE_ID,
  "ad_active_status": "ACTIVE",
  "ad_reached_countries": "['US']",
  "fields": "id,page_name,ad_creative_bodies,impressions,spend,ad_delivery_start_time,ad_snapshot_url",
  "access_token": META_ADLIB_TOKEN,
  "limit": 500
})

# Meta returns ranges like {"lower_bound":"100000","upper_bound":"199999"}
def avg_imp(d):
    if not d: return 0
    return (int(d.get("lower_bound",0)) + int(d.get("upper_bound",0))) // 2

ads = [
  {**a, "avg_imps": avg_imp(a.get("impressions")), "days_running": 
   (datetime.now() - datetime.fromisoformat(a["ad_delivery_start_time"].replace("Z","+00:00"))).days}
  for a in r.json()["data"]
]
high_impact = [a for a in ads if a["avg_imps"] > 100000 and a["days_running"] > 14]
print(f"{len(high_impact)} ads from this competitor have run 14d+ with 100K+ impressions")
```

### Recipe 5: Snapshot URL → asset download

```python
# ad_snapshot_url is a Meta-hosted preview URL
# For asset capture, use playwright-mcp to screenshot
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    for a in high_impact:
        page = browser.new_page()
        page.goto(a["ad_snapshot_url"])
        page.wait_for_load_state("networkidle")
        page.screenshot(path=f"competitor-ads/{a['id']}.png", full_page=True)
    browser.close()
```

### Recipe 6: Google Ads Transparency Center scrape

```bash
# Via firecrawl-mcp
mcp tool firecrawl.scrape \
  --url "https://adstransparency.google.com/?advertiser=$ADVERTISER_ID&region=US" \
  --formats '["markdown","html"]' \
  --only_main_content false \
  --wait_for 3000

# Output: markdown with ad copy + display creatives + LP URLs + last seen
```

Or via Python + playwright:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    page.goto(f"https://adstransparency.google.com/?advertiser={ADVERTISER_ID}&region=US")
    page.wait_for_selector(".ad-card")
    ads = page.query_selector_all(".ad-card")
    
    for ad in ads:
        headline = ad.query_selector(".headline")
        description = ad.query_selector(".description")
        last_seen = ad.query_selector(".last-seen")
        # Extract text + landing URL
```

### Recipe 7: Competitive catalog xlsx

```python
import openpyxl
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Competitor Ads"

ws.append(["Competitor","Platform","Ad ID","Hook (first 60 chars)","Format","Days running",
           "Impressions tier","Spend tier","LP URL","Snapshot","Hook category"])

for ad in all_ads:
    ws.append([
        ad["page_name"], "Meta", ad["id"],
        ad["ad_creative_bodies"][0][:60] if ad.get("ad_creative_bodies") else "",
        "Video" if "video" in ad.get("ad_creative_link_titles",[None])[0].lower() else "Image",
        ad["days_running"], ad["avg_imps"], 
        ad.get("spend",{}).get("lower_bound","0"),
        ad.get("ad_creative_link_captions",[""])[0],
        ad["ad_snapshot_url"],
        classify_hook(ad["ad_creative_bodies"][0]) if ad.get("ad_creative_bodies") else ""
    ])

wb.save("competitive-intel-2026Q3.xlsx")
```

### Recipe 8: Hook classification with LLM

```python
import anthropic
client = anthropic.Anthropic()

def classify_hook(body):
    r = client.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=64,
      messages=[{"role":"user","content":
        f"Classify this ad's hook in 1-2 words from: [problem-aware-question, founder-direct, testimonial-montage, result-driven, price-anchor, social-proof, demo-first, FOMO-urgency, pattern-interrupt, none]. Ad: \"{body[:200]}\". Answer only the category."
      }])
    return r.content[0].text.strip()
```

### Recipe 9: Brand monitoring — alert on new competitor ads

```python
# Daily cron — check for new ads from tracked competitors
import requests, os, json
from datetime import datetime, timedelta

YESTERDAY = (datetime.utcnow() - timedelta(days=1)).isoformat()

for competitor in TRACKED_COMPETITORS:
    r = requests.get("https://graph.facebook.com/v19.0/ads_archive", params={
      "search_page_ids": competitor["page_id"],
      "ad_active_status": "ACTIVE",
      "ad_delivery_date_min": YESTERDAY,
      "fields": "id,page_name,ad_creative_bodies,ad_snapshot_url,ad_delivery_start_time",
      "access_token": META_ADLIB_TOKEN
    })
    new_ads = r.json()["data"]
    if new_ads:
        # Slack notification
        text = f":eyes: {len(new_ads)} new ads from {competitor['name']} today"
        for ad in new_ads[:5]:
            text += f"\n• {ad['ad_creative_bodies'][0][:80] if ad.get('ad_creative_bodies') else '(no copy)'}"
        requests.post(SLACK_WEBHOOK, json={"text": text})
```

## Examples — quarterly competitive intel deck

```yaml
deliverable: competitive-intel-2026Q3.pdf

structure:
  slide_1: Executive summary
    - 12 competitors tracked
    - 847 active ads catalogued
    - 23 new ads launched this quarter
    - top 3 themes: founder-UGC, sustainability, social proof
  
  slide_2-13: per competitor (one slide each)
    - Competitor name + page ID
    - Active ad count + tier
    - Hook themes (top 3)
    - Format mix (Video / Image / Carousel)
    - Top performing ad (by impressions tier × days running)
    - Landing page strategy (LP per category vs single LP)
    - Snapshot of 4 representative ads
  
  slide_14: Cross-competitor themes
    - "Founder UGC" rising — 7 of 12 competitors using
    - "Sustainability messaging" plateauing — only 3 still featuring
    - "Free shipping" ubiquitous — table stakes
    - "$20 off first order" — 5 competitors using exact dollar amount
  
  slide_15: Recommendations
    - 3 hook concepts to test (steal-with-pride from competitors)
    - 2 formats to add to mix (carousel format gap)
    - LP message-match opportunity (specific quote)
```

## Edge cases

### Public vs political ads
Commercial ads = open API access. Political/issue ads = App Review required. Most use cases are commercial.

### Stale data
Meta Ad Library shows ads even after delivery stopped. Filter by `ad_delivery_stop_time` IS NULL for "currently running."

### Impressions / spend = ranges only
Meta doesn't share exact numbers. Format: `{"lower_bound": "100000", "upper_bound": "199999"}`. Use averages or treat as tiers.

### Snapshot URL expires
`ad_snapshot_url` may break weeks/months later. Cache via playwright screenshot for permanent reference.

### Page ID not handle
Meta API requires Page ID (numeric), not handle. Use Pages Search API or scrape from page source.

### Google Transparency Center — selector instability
Google updates Transparency Center markup occasionally. Build resilient scraper with multiple selectors.

### Reverse-image search for creative match
Sometimes you have an image but not the page. Use Bing Visual Search or Yandex via `playwright-mcp` to find source.

### Region-specific ads
Meta `ad_reached_countries`; Google `region` param. Same advertiser may run different ads per market.

### Rate limits
Meta: 200 calls/hour. For tracking 50 competitors with 500 ads each, batch wisely or paginate over days.

### Legal / ethical use
Public ad data is legally collectable but check brand's policy on competitive intel. Don't reverse-engineer protected creative.

### Stealing-with-pride threshold
Concept inspiration = fine. Direct creative copy = trademark / copyright risk. Use competitor data to spot themes, then originate your execution.

### Pathmatics for display
Display ad intel (banner ads on publisher sites) not in Meta/Google Transparency. Pathmatics is paid alternative.

## Sources

- Meta Ad Library API: https://www.facebook.com/ads/library/api
- Meta Ad Library API reference: https://developers.facebook.com/docs/graph-api/reference/archived-ad/
- Meta Ad Library UI: https://www.facebook.com/ads/library
- Google Ads Transparency Center: https://adstransparency.google.com/
- Google Ads Transparency policy: https://support.google.com/transparencyreport/answer/13539062
- Pathmatics: https://www.pathmatics.com/
- WhatRunsWhere: https://www.whatrunswhere.com/
- SpyFu: https://www.spyfu.com/
- SimilarWeb advertising intel: https://www.similarweb.com/corp/marketing-intelligence/
- firecrawl-mcp: https://docs.firecrawl.dev/mcp
