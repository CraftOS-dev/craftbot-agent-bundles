<!--
Source: https://stan.store/blog/stan-store-vs-linktree/
Linktree API: https://help.linktr.ee/hc/en-us/categories/360003752772-Developer-Tools
Beacons: https://beacons.ai/
Stan Store: https://stan.store/
-->
# Link-in-Bio — Linktree + Beacons + Stan Store — SKILL

Single bio link → multiple destinations. Linktree (50M+ users, REST API) is the agent-executable default; Beacons (AI brand outreach + email + storefront) and Stan Store (creator monetization, no transaction fees on products) covered via Playwright when API gaps exist. Sync bio page weekly from master Notion DB.

## When to use this skill

- **Updating the brand bio link** after campaign launch.
- **Adding seasonal / time-bound links** (sale page, RSVP form, AMA registration).
- **Reordering links** based on conversion data.
- **A/B testing link order / copy / icons**.
- **Bulk sync** of bio across multiple platforms (each platform has its own link slot — IG, TikTok, LinkedIn, Threads, etc.).

**Do NOT use this skill when:**
- Single one-off direct URL — paste directly into platform bio field.
- E-commerce storefront — `social-commerce-tiktok-instagram-pinterest-shops`.

## Setup

### Linktree REST API

```bash
export LINKTREE_TOKEN="<api-key>"
# Endpoint: https://api.linktr.ee/v1/
# Free tier: 5 links. Pro $5/mo: unlimited. Premium $20/mo: analytics + scheduling
```

### Beacons (Playwright fallback)

```bash
# Beacons doesn't expose public API for link CRUD as of June 2026
# Use playwright-mcp for UI automation
export BEACONS_USERNAME="<user>"
export BEACONS_PASSWORD="<pass>"
# Or session cookie:
export BEACONS_SESSION_COOKIE="<cookie>"
```

### Stan Store (Playwright fallback)

```bash
# Stan Store API limited; UI automation needed for full CRUD
export STAN_USERNAME="<user>"
export STAN_PASSWORD="<pass>"
```

### Notion Link Master DB

Columns: `Link title / Destination URL / UTM convention / Icon / Order / Status (active/scheduled/expired) / Platform (where it shows: IG/TikTok/LinkedIn/all) / Click-through rate / Last 30d clicks / A/B variant`.

## Common recipes

### Recipe 1: Linktree create / update link

```bash
# Create new link
curl -X POST https://api.linktr.ee/v1/links \
  -H "Authorization: Bearer $LINKTREE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Spring sale — 25% off",
    "url":"https://yourshop.com/sale?utm_source=linktree&utm_medium=bio&utm_campaign=spring26",
    "thumbnail_url":"https://cdn.example.com/thumb.jpg",
    "active":true,
    "schedule_start":"2026-06-12T00:00:00Z",
    "schedule_end":"2026-06-30T23:59:59Z"
  }'
# Returns: {id: "link_abc123", ...}

# Update link order
curl -X PATCH https://api.linktr.ee/v1/links/link_abc123 \
  -H "Authorization: Bearer $LINKTREE_TOKEN" \
  -d '{"position": 1}'

# Delete link
curl -X DELETE https://api.linktr.ee/v1/links/link_abc123 \
  -H "Authorization: Bearer $LINKTREE_TOKEN"
```

### Recipe 2: Linktree analytics pull

```bash
curl -G https://api.linktr.ee/v1/analytics/links \
  -H "Authorization: Bearer $LINKTREE_TOKEN" \
  -d "since=$(date -u -d '30 days ago' +%Y-%m-%d)" \
  -d "until=$(date -u +%Y-%m-%d)"
# Returns: per-link clicks, click-through rate, geo breakdown
```

### Recipe 3: Beacons via Playwright

```javascript
// playwright_scripts/beacons_update.js
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({
    storageState: 'beacons-auth.json'  // pre-saved session
  });
  const page = await ctx.newPage();
  await page.goto('https://beacons.ai/dashboard');
  await page.click('text=Add Link');
  await page.fill('input[name="title"]', process.env.LINK_TITLE);
  await page.fill('input[name="url"]', process.env.LINK_URL);
  await page.click('button:has-text("Save")');
  await page.waitForSelector('text=Link saved');
  await browser.close();
})();
```

Invoke:

```bash
LINK_TITLE="Spring sale" LINK_URL="https://..." \
  mcp tool playwright.run --script "beacons_update.js"
```

### Recipe 4: Stan Store via Playwright

Same pattern as Recipe 3, target `https://stan.store/dashboard/products`. Stan Store distinguishes:
- Free / paid digital products (PDF, course)
- 1:1 booking (calendar link)
- Memberships
- Affiliate links

Use Playwright to create + reorder.

### Recipe 5: Weekly sync from Notion master DB

```python
# Pull Notion master, push to all bio platforms
links = notion.query(link_master_db, filter={'Status':'active'},
                     sort='Order asc')

# Sync Linktree
existing = linktree.get_links()
existing_by_url = {l['url']: l for l in existing}
for l in links:
    if l['Destination URL'] in existing_by_url:
        linktree.patch(existing_by_url[l['Destination URL']]['id'],
                       title=l['Link title'], position=l['Order'])
    else:
        linktree.create(title=l['Link title'], url=l['Destination URL'],
                        position=l['Order'])

# Remove links not in master
master_urls = {l['Destination URL'] for l in links}
for url, link in existing_by_url.items():
    if url not in master_urls:
        linktree.delete(link['id'])

# Repeat for Beacons / Stan via Playwright
mcp tool playwright.run --script "beacons_bulk_sync.js" --input "$(echo $links | base64)"
```

### Recipe 6: Per-platform bio URL with tracking

Each platform's bio link should have unique UTM:

```python
PLATFORM_BIO = {
    'instagram': 'https://linktr.ee/yourbrand?p=ig',
    'tiktok':    'https://linktr.ee/yourbrand?p=tt',
    'threads':   'https://linktr.ee/yourbrand?p=th',
    'linkedin':  'https://linktr.ee/yourbrand?p=li',
    'bluesky':   'https://linktr.ee/yourbrand?p=bs',
    'pinterest': 'https://linktr.ee/yourbrand?p=pn',
}
# Linktree captures the ?p= parameter in per-visitor analytics
# PostHog also picks up the URL via UTM if set
```

### Recipe 7: A/B test link copy

```python
# Variant A: "Free 14-day trial"
# Variant B: "Get started — no card required"
import random

linktree.update(link_a_id, active=(today.day % 2 == 0))
linktree.update(link_b_id, active=(today.day % 2 == 1))

# After 14 days, pick winner by CTR
ctr_a = linktree.get_analytics(link_a_id)['ctr']
ctr_b = linktree.get_analytics(link_b_id)['ctr']
winner = 'A' if ctr_a > ctr_b else 'B'
slack.post('#growth', f"A/B test winner: {winner} (CTR A {ctr_a:.2%} vs B {ctr_b:.2%})")
```

### Recipe 8: Scheduled link expiry

Linktree Pro supports `schedule_start` / `schedule_end`. For free / Beacons / Stan, agent watchdog:

```python
# Daily 6am cron
for l in notion.query(link_master_db, filter={'Expires__lte': now}):
    if l['Linktree ID']:
        linktree.patch(l['Linktree ID'], active=False)
    notion.update(l['id'], {'Status': 'expired'})
```

### Recipe 9: Per-platform link slot rules

| Platform | Bio link slots | Notes |
|---|---|---|
| Instagram | 1 (or 5 with "Add yours" feature) | Use Linktree multi-link |
| TikTok | 1 (1k+ followers) | Use Linktree |
| LinkedIn | 1 personal + 1 company website + multiple in "About" | Use Linktree for company |
| Threads | 1 via IG bio inheritance | Inherits from IG |
| Bluesky | Multiple plaintext in profile | Direct URLs OK |
| Pinterest | 1 website + multiple board links | Direct URL OK |
| Twitter / X | 1 website + 1 location URL | Use Linktree |

### Recipe 10: Conversion-weighted link order

```python
# Recompute order based on last 7-day conversion value, not just clicks
for l in linktree.get_links():
    sessions = posthog.query(f"""
        SELECT count(*) FROM events
        WHERE event='purchase' AND properties.referrer LIKE '%linktr.ee%link_id={l['id']}%'
        AND timestamp > now() - INTERVAL 7 DAY
    """)
    revenue = posthog.query("... revenue join ...")
    l['conv_value'] = revenue['result']

ranked = sorted(linktree.get_links(), key=lambda x: -x['conv_value'])
for i, l in enumerate(ranked):
    linktree.patch(l['id'], position=i+1)
```

## Examples

### Example A: Pre-launch bio prep

```yaml
campaign: summer_drop
T-7:
  add_link:
    title: "Coming June 15 — pre-register"
    url: "https://shop.com/preregister?utm_source=linktree&utm_campaign=summer_drop"
    position: 1
T-0:
  update_link_1:
    title: "Shop the drop"
    url: "https://shop.com/summer-drop?utm_source=linktree"
T+30:
  expire_link_1: deactivate
  promote_link_2: position 1
```

### Example B: Multi-platform bio rotation

```python
# Every Sunday, rotate bio link based on weekly priority
weekly_priority = notion.get(week_priority_db, this_week)
# e.g., this week: blog post launch
new_bio = {
    'instagram': 'https://linktr.ee/brand?p=ig&hi=blog_launch',
    'tiktok':    'https://linktr.ee/brand?p=tt&hi=blog_launch',
    ...
}
for platform, url in new_bio.items():
    update_platform_bio(platform, url)  # via per-platform MCP
```

### Example C: Stan Store creator commerce setup

```yaml
stan_store_setup:
  products:
    - type: digital
      title: "Notion template — Editorial calendar"
      price: $19
      delivery: PDF + Notion duplication link
    - type: 1on1
      title: "30-min content audit"
      price: $99
      calendar: Calendly embed
    - type: course
      title: "TikTok growth playbook"
      price: $149
      delivery: 12 video modules + community access
  bio_link: https://stan.store/yourbrand
```

## Edge cases

### Linktree free tier limits
5 links max, no analytics, no scheduling. Pro $5/mo unlocks. For brand accounts, Premium $20/mo for full analytics + Sensei AI.

### API rate limits
Linktree: 60 req/min. Bulk operations need batching.

### Playwright session expiry
Beacons / Stan sessions expire (typically 7-14 days). Refresh via authenticated login flow or persist `storageState`. Watchdog on 401 → re-authenticate.

### URL parameter strip
Some platforms strip URL parameters when re-rendering bio (Threads sometimes; LinkedIn rarely). Use short links (`bit.ly`) where strip risk exists.

### Conversion attribution lag
PostHog / Shopify report conversion 1-7 days post-click; recipe 10 weighting needs 7+ day rolling window, not real-time.

### Multi-currency
Stan Store + Beacons handle USD-only on standard plans. For multi-currency, use platform-specific localized stores or external Shopify.

### Page load + SEO
Linktree page is JS-rendered; doesn't pass link equity. Don't use for SEO. For SEO-relevant pages, link directly to your domain.

### Branded URL
Linktree Pro: custom domain (`go.yourbrand.com`). Improves CTR ~10-15% (Linktree internal data). One-time DNS setup.

### Mobile rendering
All three are mobile-first. Verify thumbnail aspect (1:1, ~500x500) renders well on iOS / Android. Avoid text-heavy thumbnails.

### Accessibility
Add alt-text to thumbnails (Linktree: title alt-text inferred). Beacons + Stan: manually set via Playwright.

### IG bio link analytics gap
Instagram's own bio click tracking is gated to Creator / Business tier. Linktree click + PostHog UTM are the workable stack.

### Stan Store transaction fee
Stan Store charges 0% on physical products, 0% on digital with paid plan ($29/mo), 5% on free plan. Compare to Linktree (no transactions) vs. Shopify (2.9% + 30¢).

### Region-specific bio
TikTok / IG creator accounts may have audience in different regions. Use Linktree's location-based redirect (Pro) or per-platform UTM (Recipe 6) to segment.

### Bio link death
If primary bio URL goes 404, every platform bio breaks at once. Set monitoring: weekly Playwright check that bio URL returns 200.

## Sources

- **Linktree Developer Docs**: https://help.linktr.ee/hc/en-us/categories/360003752772-Developer-Tools
- **Linktree API reference (v1)**: https://developers.linktr.ee/
- **Beacons**: https://beacons.ai/
- **Stan Store**: https://stan.store/
- **Stan Store vs Linktree (2026)**: https://stan.store/blog/stan-store-vs-linktree/
- **Beacons vs Linktree (2026)**: https://talkspresso.com/blog/beacons-vs-linktree-2026
- **Bonsai link-in-bio**: https://www.hellobonsai.com/
- **PostHog UTM join**: https://posthog.com/docs/data/utm-segmentation
