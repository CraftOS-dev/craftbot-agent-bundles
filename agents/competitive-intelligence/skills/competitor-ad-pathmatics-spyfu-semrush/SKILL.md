<!--
Sources: Meta Ad Library https://www.facebook.com/ads/library
         LinkedIn Ad Library https://www.linkedin.com/ad-library/
         Google Ads Transparency Center https://adstransparency.google.com/
         TikTok Creative Center https://library.tiktok.com/ads
         Pathmatics https://sensortower.com/product/digital-advertising/pathmatics
         SpyFu https://www.spyfu.com/
         SEMrush https://www.semrush.com/
         AdLibrary API guide https://adlibrary.com/guides/best-ad-spy-api
Companion playbook: role.md → "Signal layer cadence" → Ad library row + "SOTA tool reference"
-->

# Competitor ad intelligence (Pathmatics / SpyFu / SEMrush + free ad libraries)

Free official libraries cover ~80% of CI ad signal — Meta Ad Library (FB + IG, active + historical), LinkedIn Ad Library (with EU+UK spend bands), Google Ads Transparency Center (Search + Display + YouTube), TikTok Creative Center, X Ads Library. Paid uplift: Pathmatics (cross-channel desktop/mobile/social/video/CTV spend estimates), SpyFu (Google search ads + keyword history 18+ years), SEMrush. Use to inventory creative themes, channel mix, spend trends, and emerging messaging.

## When to use

- "What ads is [competitor] running?"
- "Did Acme launch a new campaign?"
- "What's their creative theme this quarter?"
- "How much are they spending on paid?"
- "Which keywords are they bidding on?"
- Detect new product launch via paid amplification
- Cross-reference with messaging-tracking-diff for narrative shifts

## When NOT to use

- Organic SEO position → use `competitor-seo-ahrefs-semrush-organic`
- App store ad SDK adoption → use `competitor-app-intel-sensor-tower-data-ai`
- Influencer / earned media → use social-listening (Brandwatch / Talkwalker) component in `continuous-competitor-monitoring-klue-kompyte-crayon`

## Setup

```bash
# Free official ad libraries — no key needed for most
# Meta Ad Library API requires a Meta developer app token
export META_APP_ID="..."
export META_APP_SECRET="..."
export META_ACCESS_TOKEN="..."     # https://developers.facebook.com/docs/marketing-api/access

# Pathmatics (enterprise; Sensor Tower / Adyntel)
export PATHMATICS_API_KEY="..."

# SpyFu (from $39/mo; API on Professional+)
export SPYFU_API_KEY="..."

# SEMrush (from $130/mo; .Trends from $289/mo)
export SEMRUSH_API_KEY="..."

# Firecrawl for HTML scrape fallback (LinkedIn, Google, TikTok)
export FIRECRAWL_API_KEY="..."
```

MCPs in `agent.yaml`: `playwright-mcp`, `firecrawl-mcp`, `cli-anything`, `slack-mcp`, `notion-mcp`.

## Common recipes

### Recipe 1: Meta Ad Library API (free, official)

```bash
# Search Acme active commercial ads
curl "https://graph.facebook.com/v19.0/ads_archive?\
search_terms=Acme%20Corp&\
ad_reached_countries=['US','GB','DE']&\
ad_active_status=ACTIVE&\
fields=id,ad_creative_body,ad_snapshot_url,ad_delivery_start_time,ad_delivery_stop_time,page_name,impressions,spend&\
access_token=$META_ACCESS_TOKEN"
```

Returns: creative body text, snapshot URL, delivery window, page name. Impressions + spend are reported in ranges (e.g., "10K-50K impressions") for non-political ads. EU DSA mandates broader transparency since 2024.

### Recipe 2: LinkedIn Ad Library (free, page scrape)

```bash
# LinkedIn Ad Library is a public page; use playwright-mcp for JS rendering
# URL pattern: https://www.linkedin.com/ad-library/search?accountOwner=Acme%20Corp
curl -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -d '{
    "url": "https://www.linkedin.com/ad-library/search?accountOwner=Acme%20Corp",
    "formats": ["markdown", "rawHtml"]
  }'
```

EU + UK ads include spend bands (e.g., "EUR 1,000-5,000"); US ads show creative + page only.

### Recipe 3: Google Ads Transparency Center (free, page scrape)

```bash
# Per-advertiser page: https://adstransparency.google.com/advertiser/<id>
# Find advertiser_id by searching from the homepage
# Use playwright-mcp since page is JS-heavy
```

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://adstransparency.google.com/?region=US&topic=all&domain=acme.example.com")
    page.wait_for_selector("a[href*='/advertiser/']")
    advertiser_url = page.query_selector("a[href*='/advertiser/']").get_attribute("href")
    page.goto(f"https://adstransparency.google.com{advertiser_url}")
    ads = page.query_selector_all("[data-creative-id]")
    for ad in ads:
        print(ad.text_content(), ad.get_attribute("data-format"))
    browser.close()
```

### Recipe 4: TikTok Creative Center (free)

```bash
# https://library.tiktok.com/ads — search by advertiser name
# JS-heavy; use playwright-mcp
```

```python
with sync_playwright() as p:
    page = p.chromium.launch().new_page()
    page.goto("https://library.tiktok.com/ads?region=US&adv_name=Acme%20Corp")
    page.wait_for_selector(".ad-card")
    cards = page.query_selector_all(".ad-card")
    for c in cards:
        creative_url = c.query_selector("video, img").get_attribute("src")
        copy = c.query_selector(".ad-copy").text_content()
        print(copy, creative_url)
```

### Recipe 5: X (Twitter) Ads Library (free)

```bash
# https://ads.twitter.com/transparency for advertiser-side
# Limited compared to FB/Google; spend-tier visible for political; commercial creative public.
```

### Recipe 6: Pathmatics — cross-channel spend estimates

```bash
curl -H "Authorization: Bearer $PATHMATICS_API_KEY" \
  "https://api.pathmatics.com/v2/brands/acme/spend?channel=all&since=2026-04-01"
```

Returns: estimated spend by channel (desktop display, mobile display, social, video, CTV), month over month. ~70-85% accurate vs disclosed budgets (per Pathmatics methodology).

### Recipe 7: SpyFu — Google search ads history

```bash
# 18+ years of search-ad history across 38 countries
curl "https://www.spyfu.com/apis/url_api/get_seo_kws?\
domain=acme.example.com&\
api_id=$SPYFU_API_KEY"
```

Endpoint returns: top paid keywords, ad copy variants seen, position trend, est CPC.

### Recipe 8: SEMrush Advertising Research

```bash
curl "https://api.semrush.com/?\
type=domain_adwords&\
key=$SEMRUSH_API_KEY&\
domain=acme.example.com&\
database=us&\
display_limit=50"
```

Returns: paid keywords, CPC, est. monthly traffic, ad copy. SEMrush is paid-keyword strong; Ahrefs is organic-strong.

### Recipe 9: Creative theme extraction across libraries

```python
import anthropic
client = anthropic.Anthropic()

ALL_AD_COPIES = open("acme_ad_copies_q2.txt").read()
prompt = f"""Cluster these ad copy headlines + bodies into 3-5 creative themes.
For each theme, give:
- name
- example_count
- representative_copy (verbatim)
- inferred_target_audience
- inferred_funnel_stage (awareness/consideration/decision)

Ad copies:
{ALL_AD_COPIES}
"""
msg = client.messages.create(
    model="claude-opus-4-7-1m",
    max_tokens=3000,
    messages=[{"role":"user","content":prompt}],
)
```

### Recipe 10: Channel-mix snapshot

```python
# Per-competitor channel mix from Pathmatics or library counts
import pandas as pd
mix = pd.DataFrame({
    "channel": ["Meta","LinkedIn","Google Search","Google Display","YouTube","TikTok","X"],
    "active_ads": [42, 18, 67, 24, 9, 14, 5],
    "est_spend_$k": [120, 80, 200, 45, 60, 25, 8],  # Pathmatics
})
mix.sort_values("est_spend_$k", ascending=False)
```

### Recipe 11: Diff ad creative week-over-week

```python
prior = set(open("acme_meta_ads_2026-06-04.txt").read().splitlines())
curr  = set(open("acme_meta_ads_2026-06-11.txt").read().splitlines())
new = curr - prior; retired = prior - curr
print("NEW:", new); print("RETIRED:", retired)
```

### Recipe 12: Slack hot signal on new campaign

```python
def notify_new_campaign(competitor, theme, sample_copy, channels):
    requests.post(SLACK_WEBHOOK_URL, json={
        "text": f":megaphone: {competitor} launched new campaign: *{theme}*\n"
                f"Sample copy: _{sample_copy}_\nChannels: {', '.join(channels)}",
        "channel": "#ci-hotline",
    })
```

## Examples

### Example 1: Map Acme's full ad portfolio for $0

**Goal:** Inventory Acme's active ads across all major channels, free path only.

**Steps:**
1. Recipe 1 → Meta Ad Library API for all active Acme ads (FB+IG, all geos).
2. Recipe 2 → LinkedIn Ad Library scrape.
3. Recipe 3 → Google Ads Transparency.
4. Recipe 4 → TikTok Creative Center.
5. Recipe 5 → X Ads Library.
6. Recipe 9 → LLM cluster into themes.
7. Recipe 10 → channel-mix table (counts, not spend).
8. Recipe 12 → post any new theme to `#ci-hotline`.

**Result:** Full free-tier ad portfolio with creative themes; no spend estimates but channel mix + creative inventory complete.

### Example 2: Detect Acme's product-launch campaign

**Goal:** Detect Acme's new feature launch via paid amplification before it hits the changelog.

**Steps:**
1. Recipes 1-5 → daily diff (Recipe 11).
2. Spike: 28 new ad creatives on Meta + LinkedIn in 2 days.
3. Recipe 9 → LLM clusters reveal common theme: "AI Copilot for Sales."
4. Cross-check changelog (continuous monitoring) — no release announcement yet.
5. Cross-check hiring intel (Recipe 5 of hiring skill) — 6 LLM-eng job posts L60D.

**Verdict:** Acme launching AI Copilot imminently; battlecard pane 4 (parity) and pane 1 (positioning) flagged for refresh.

### Example 3: Paid uplift — Pathmatics spend snapshot

**Goal:** Quantify Acme's spend tier for war-game scenario.

**Steps:**
1. Recipe 6 → Pathmatics last 90 days spend by channel.
2. Cross-reference with SimilarWeb traffic (referral channel).
3. Estimate spend efficiency (cost per visit).

**Result:** "Acme spending ~$580k/mo paid in Q2, ~$210/visit on Google Search — high CPC category." Inform pricing-leverage discussion.

## Edge cases / gotchas

- **Meta Ad Library impressions in ranges** — non-political ads report ranges, not exact numbers. EU DSA mandates broader transparency since 2024 but ranges still apply.
- **Meta Marketing API rate limit** — burst 200 calls per hour per app token; design pagination + sleep.
- **LinkedIn Ad Library JS-heavy** — Firecrawl alone may not capture; use `playwright-mcp` with wait-for-selector.
- **Google Ads Transparency Center** — region-specific; check US + EU + key markets separately. URL params include `region=US`.
- **TikTok Creative Center search is fuzzy** — advertiser-name match imprecise; expect to manually disambiguate.
- **X Ads Library — narrow** — historical political ads only by default; commercial limited.
- **Pathmatics methodology accuracy** — ~70-85% vs disclosed; treat as directional, not exact.
- **SpyFu data depth varies by geo** — strong US/UK; weaker outside English-speaking markets.
- **SEMrush vs Ahrefs paid keyword overlap** — SEMrush often catches more paid-only keywords; Ahrefs stronger on organic. Use both if budget allows.
- **EU DSA disclosure scope** — political/issue ads must disclose; commercial creative public but spend bands only for political ads in some jurisdictions.
- **Creative storage** — Meta returns `ad_snapshot_url` (image/video); persist locally before they expire (typically 1-2 years post-stop).
- **Don't impersonate to access advertiser-side data** — SCIP hard no. Stick to public libraries.
- **Ad copy de-dup** — same creative may appear under multiple variants (UTM-only differences). De-dup by hash of stripped copy.
- **Active vs historical** — Meta ad_active_status flag matters. For trend analysis, query both ACTIVE and ALL with delivery dates.
- **PROACTIVE.md cadence** — weekly default per role.md signal cadence table; daily during launch detection war-games.
- **Provenance footer** — cite library URL + retrieval date for every claim; Pathmatics is paid-source-class.

## Sources

- Meta Ad Library — https://www.facebook.com/ads/library
- Meta Marketing API ad_archive — https://developers.facebook.com/docs/marketing-api/reference/ads-archive
- LinkedIn Ad Library — https://www.linkedin.com/ad-library/
- Google Ads Transparency Center — https://adstransparency.google.com/
- TikTok Creative Center — https://library.tiktok.com/ads
- Pathmatics — https://sensortower.com/product/digital-advertising/pathmatics
- SpyFu — https://www.spyfu.com/
- SEMrush Advertising Research — https://www.semrush.com/advertising-research
- AdLibrary API guide — https://adlibrary.com/guides/best-ad-spy-api
- EU DSA Ad Transparency — https://commission.europa.eu/strategy-and-policy/priorities-2019-2024/europe-fit-digital-age/digital-services-act_en
- role.md → "Signal layer cadence" → Ad library row; "SOTA tool reference" → Pathmatics / SpyFu / Meta / LinkedIn / Google / TikTok

## Related skills

- `competitor-messaging-tracking-diff` — pair ad themes with LP / homepage messaging
- `competitor-seo-ahrefs-semrush-organic` — organic + paid pair via SEMrush
- `continuous-competitor-monitoring-klue-kompyte-crayon` — ad library is one of the fan-out layers
- `feature-parity-tracking` — new ad campaign may signal a feature ship
- `ethical-public-source-methodology` — all ad library data is public; no SCIP concerns
