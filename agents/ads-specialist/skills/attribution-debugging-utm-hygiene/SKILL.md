<!--
Source: https://funnel.io/blog/utm-builder
UTM hygiene + attribution debugging (VTC vs CTC; Funnel.io / Improvado normalization).
-->
# Attribution Debugging + UTM Hygiene — SKILL

UTM hygiene is the unglamorous foundation. 90% of attribution debugging traces to inconsistent UTM conventions or missing parameters. This skill ships the convention spec, the audit query, the dedup check, and the cross-platform reconciliation pattern.

## When to use this skill

- **New account onboarding** — set UTM convention before first campaign.
- **Reporting discrepancy** — Meta says $X, GA4 says $Y, Triple Whale says $Z.
- **Attribution model switch** — document baseline before switching.
- **Quarterly attribution audit** — verify VTC vs CTC windows + dedup.
- **New platform launch** — extend UTM convention to new channel.

**Do NOT use this skill when:**
- Pre-attribution platform setup (configure pixel / CAPI first).
- Server-side tracking implementation (see `server-side-tracking-gtm-s-stape`).
- Pure MMM (different model; see `mmm-meridian-robyn-recast-pymc`).

## Setup

### UTM convention (mandatory across all channels)

```
utm_source     = channel name (lowercase, no spaces): meta, google, tiktok, linkedin, reddit, klaviyo, organic-tiktok
utm_medium     = paid (always), email, organic, referral, affiliate
utm_campaign   = kebab-case campaign slug: q3-cold-prospecting, brand-defense, abm-tier1
utm_content    = ad_set_id (numeric platform ID) OR creative-cell-id: cell-c7, adset-12345
utm_term       = keyword (Google Search only) OR audience identifier
```

Example:
```
https://brand.com/lp?utm_source=meta&utm_medium=paid&utm_campaign=q3-cold-prospecting&utm_content=adset-23845827&utm_term=lal-1pct
```

### Audit baseline tools

- **`bitly-utm-campaign-tracking` skill** — bulk-link generation + registry
- **Funnel.io** — normalized cross-platform ad data warehouse pipe
- **Improvado** — enterprise alt to Funnel
- **Supermetrics** — low-cost via Google Sheets
- **GA4** — UTM-stamped session report

### VTC vs CTC defaults (2026)

| Platform | Default click window | Default view window | Notes |
|---|---|---|---|
| Meta | 1d-click | 1d-view | post-ATT default; 7d-click ENABLE_OPTIMIZED_TARGETING |
| Google Search/Shopping | 30d | n/a | data-driven attribution default |
| Google Display/YouTube | 30d | 1d | |
| TikTok | 7d | 1d | |
| LinkedIn | 30d | 7d | |
| Reddit | 7d | 1d | |
| GA4 | Data-driven (DDA) | DDA | configurable |

## Common recipes

### Recipe 1: Pull all active destination URLs across Meta

```bash
mcp tool meta-ads.list_ads --status ACTIVE --fields '["id","name","creative"]' > meta-active-ads.json

jq '.[] | {ad_id: .id, link: .creative.object_story_spec.link_data.link}' meta-active-ads.json > meta-urls.json
```

### Recipe 2: UTM convention validator

```python
import re, json
PATTERN = re.compile(
  r'^https?://[^?]+\?'
  r'(?=.*utm_source=(?P<source>[a-z0-9_-]+))'
  r'(?=.*utm_medium=(?P<medium>paid|email|organic|referral|affiliate))'
  r'(?=.*utm_campaign=(?P<campaign>[a-z0-9_-]+))'
  r'(?=.*utm_content=(?P<content>[a-z0-9_-]+))'
)
ALLOWED_SOURCES = {"meta","google","tiktok","linkedin","reddit","klaviyo","organic-tiktok"}

violations = []
for entry in json.load(open("meta-urls.json")):
    url = entry["link"] or ""
    m = PATTERN.search(url)
    if not m:
        violations.append({"ad_id": entry["ad_id"], "issue": "regex_fail", "url": url})
        continue
    if m["source"] not in ALLOWED_SOURCES:
        violations.append({"ad_id": entry["ad_id"], "issue": f"bad_source:{m['source']}"})
    if m["medium"] != "paid":
        violations.append({"ad_id": entry["ad_id"], "issue": f"bad_medium:{m['medium']}"})

print(json.dumps(violations, indent=2))
```

### Recipe 3: Auto-fix missing UTM via Meta MCP update

```python
for v in violations:
    # Construct corrected URL
    new_url = f"https://brand.com/lp?utm_source=meta&utm_medium=paid&utm_campaign={CAMPAIGN_SLUG}&utm_content=adset-{ADSET_ID}"
    # Update via Meta MCP
    mcp_call("meta-ads.update_creative", {
      "creative_id": v["creative_id"],
      "link": new_url
    })
```

### Recipe 4: CAPI dedup check — Meta

```bash
# Send test event with known event_id, both via pixel (client) + CAPI (server)
EVENT_ID="dedup-test-$(date +%s)"

# Server-side via CAPI
curl -X POST "https://graph.facebook.com/v19.0/$PIXEL_ID/events" \
  -d "data=[{
    'event_name':'Test',
    'event_time':$(date +%s),
    'event_id':'$EVENT_ID',
    'action_source':'website',
    'user_data':{'em':'<sha256-test-email>'}
  }]&access_token=$META_CAPI_TOKEN"

# Then verify Meta Events Manager → Test Events → search for event_id
# Should see EXACTLY 1 event registered (deduped). If 2 → dedup broken.
```

### Recipe 5: Cross-platform reconciliation — Meta vs GA4 vs MTA

```sql
-- Compare reported conversions over a fixed week
WITH meta_reported AS (
  SELECT campaign_id, date, conversions, conversions_value
  FROM ads_warehouse.meta_insights
  WHERE date = '2026-06-01'
),
ga4_attr AS (
  SELECT 
    utm_campaign,
    COUNT(*) AS sessions_with_purchase,
    SUM(purchase_revenue) AS revenue
  FROM analytics.ga4_events
  WHERE event_date = '2026-06-01' AND event_name = 'purchase'
  GROUP BY utm_campaign
),
mta_tw AS (
  SELECT campaign_id, date, attributed_revenue
  FROM ads_warehouse.triple_whale_attribution
  WHERE date = '2026-06-01'
)
SELECT
  COALESCE(m.campaign_id, g.utm_campaign, t.campaign_id) AS campaign,
  m.conversions AS meta_reported_conv,
  m.conversions_value AS meta_reported_rev,
  g.sessions_with_purchase AS ga4_sessions,
  g.revenue AS ga4_rev,
  t.attributed_revenue AS tw_rev,
  ROUND(m.conversions_value / NULLIF(g.revenue, 0), 2) AS meta_vs_ga4
FROM meta_reported m
FULL OUTER JOIN ga4_attr g ON m.campaign_id = g.utm_campaign
FULL OUTER JOIN mta_tw t ON m.campaign_id = t.campaign_id;
```

Document the gap. Don't try to "fix" it — pick one source of truth per quarter.

### Recipe 6: Funnel.io daily export integration

```bash
curl "https://api.funnel.io/v1/data-export/<export-id>" \
  -H "Authorization: Bearer $FUNNEL_API_KEY" \
  -o funnel-export-$(date +%Y-%m-%d).csv

# Pipe into PostgreSQL warehouse
psql "$DATABASE_URL" -c "\\copy ads_warehouse.platform_daily_spend FROM 'funnel-export-2026-06-09.csv' CSV HEADER"
```

### Recipe 7: VTC vs CTC report

```bash
# Meta — pull both attribution windows for same campaign
mcp tool meta-ads.get_campaign_insights \
  --campaign_id "$CAMPAIGN_ID" \
  --action_attribution_windows '["1d_click","7d_click","1d_view","7d_view"]' \
  --metrics '["conversions","conversions_value"]' \
  --date_preset "last_30d"

# Document the spread between 1d_click vs 7d_click+1d_view
```

### Recipe 8: GTM-S event_id verification

```bash
# Confirm GTM Server-side container forwards event_id correctly
curl -X POST "https://sgtm.brand.com/g/collect" \
  -H "Content-Type: application/json" \
  -d '{
    "event_name":"purchase",
    "event_id":"trace-'$(date +%s)'",
    "user_data":{"em":"<sha256>"},
    "custom_data":{"value":99.99,"currency":"USD"}
  }'

# Then check Meta Events Manager → Test Events for the same event_id
# Then check GA4 DebugView for the same event_id
# Both should appear within 60s. Mismatch = pipeline bug.
```

## Examples — quarterly audit deliverable (docx)

```markdown
# Attribution Debugging Memo — Brand Q3 2026

## Current stack
- Pixels: Meta + TikTok + Google EC + Reddit
- CAPI: Meta (via Stape GTM-S), TikTok Events API (direct), Google EC for Web
- GTM client: GTM-ABC123 (gtag.js)
- GTM server: sgtm.brand.com on Stape
- GA4: 123456789, attribution = data-driven
- MTA: Triple Whale
- MMP (mobile): AppsFlyer

## P0 findings (fix this week, >$1K/week impact)
1. **CAPI dedup broken on Meta.** Test events show 2 records per event_id 
   (pixel + CAPI both registering). Meta is retraining on duped signal.
   Impact: est. $4,200/week wasted spend on inflated conversion signal.
2. **Pixel match rate 41%** (target 75%+). Hashed email missing on 60% of 
   events from server side. Add `em` to all CAPI payloads.

## P1 findings (fix this month, >$1K/month)
1. **14 ads missing utm_content.** Attribution broken on these in GA4 + Triple 
   Whale. Auto-fix via Recipe 3.
2. **Inconsistent UTM casing.** `utm_campaign=Q3-Cold` vs `utm_campaign=q3-cold`. 
   GA4 sees as 2 campaigns. Normalize to lowercase.

## P2 findings (data hygiene)
1. **Naming convention violated** on 31 of 89 campaigns. Recommend bulk rename.
2. **VTC window mismatch.** Meta defaulting to 1d-click+1d-view; Triple Whale 
   joining at 7d. Document chosen window per platform.

## Remediation checklist
- [ ] Fix CAPI dedup (Stape GTM-S template needs event_id forwarding)
- [ ] Add hashed email to all CAPI payloads (server template var)
- [ ] Auto-fix 14 missing utm_content
- [ ] Normalize UTM casing via auto-rewrite
- [ ] Document chosen attribution window: 7d-click + 1d-view (Meta)

## Recommended attribution model for Q3
- Primary: Data-driven (GA4)
- Shadow: Triple Whale (cross-check, not anchor)
- Revisit at QBR
```

## Edge cases

### UTM stripping on redirect
Some CMS / link shorteners strip UTMs on redirect. Test every destination URL end-to-end (browser dev tools → final URL → params present).

### iOS Safari ITP cookie expiry
Safari truncates 3rd-party cookies to 7d. Use first-party cookies via GTM-S OR `fbc/fbp` cookies from Meta pixel that survive longer.

### Custom Audiences from URL params
Custom audience based on `utm_source=meta` URL match needs the param in the actual URL (post-redirect). Stripped UTMs = empty audience.

### Klaviyo / email UTM mismatch
Email links default `utm_source=email` — but Klaviyo also adds its own (`_kx` param). Normalize via UTM strip rule.

### Multi-currency UTM
Conversion values from different markets reported in different currencies. Normalize to USD via FX before reconciliation.

### Brand vs non-brand search collision
If both brand campaign and non-brand campaign use `utm_source=google` + `utm_medium=cpc` without `utm_campaign` distinction, GA4 collapses them. Force `utm_campaign` per campaign.

### Cookieless Chrome 2026
Chrome's Privacy Sandbox roll-out continues. Attribution Reporting API and Topics API replace cookies for retargeting. Plan migration via `mobile-attribution-skan-appsflyer-adjust-branch` skill.

### MMP cross-channel double-counting
AppsFlyer / Adjust may attribute the same install to both Meta and Google. Reconcile via MMP's incrementality / dedup rules.

### Triple Whale window
Triple Whale defaults to "Last touch + 28d." Different from Meta's 1d-click. Document the gap.

### GA4 vs Universal Analytics
GA4 attribution model is data-driven by default (different from UA's last-click). Trends from UA era are not comparable.

## Sources

- Funnel.io UTM builder: https://funnel.io/blog/utm-builder
- Funnel.io API docs: https://funnel.io/api-docs
- Improvado API: https://improvado.io/api-documentation
- Meta attribution windows: https://www.facebook.com/business/help/2750122080536504
- Meta CAPI dedup: https://developers.facebook.com/docs/marketing-api/conversions-api/deduplicate-pixel-and-server-events
- GA4 attribution: https://support.google.com/analytics/answer/10596866
- Privacy Sandbox status: https://privacysandbox.com/
- Safari ITP: https://webkit.org/blog/category/privacy/
- Triple Whale attribution windows: https://help.triplewhale.com/en/articles/attribution
