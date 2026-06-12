<!--
Source: https://bitly.com/blog/use-bitly-as-utm-builder/
Bitly bulk_shorten API — up to 100k links per call
-->
# Bitly UTM Campaign Tracking — SKILL

Bitly's `bulk_shorten` API accepts up to 100,000 long URLs per call and returns short links with UTMs preserved. SOTA for any campaign with >5 destinations — beats single-shorten loops and beats Google's url-builder UI.

## When to use this skill

- **Multi-channel campaign launch** — same UTM convention applied across 10-1000s of links.
- **Newsletter / email links** at scale — every link UTM-tagged + shortened.
- **Influencer / partner programs** — track per-partner with unique UTMs.
- **Social cascade with platform-specific UTMs** — `utm_source=linkedin` vs `utm_source=twitter`.
- **A/B variant tracking** — `utm_content=variant_a` vs `variant_b`.
- **Click-through monitoring** — Bitly dashboard shows clicks per shortlink.

**Do NOT use this skill when:**
- **Internal redirects** with no need for click tracking — use your own redirect.
- **One-off link** — direct shortener at https://bitly.com is fine.

## Setup

### Auth

```bash
# Generate at https://app.bitly.com/settings/api/
export BITLY_TOKEN="<token>"
export BITLY_GROUP_GUID="<group-guid>"  # workspace ID
export BITLY_CUSTOM_DOMAIN="link.brand.com"  # optional branded domain
```

### UTM convention

Standard 5-param UTM convention enforced across all Bitly campaigns:

| Param | Purpose | Examples |
|---|---|---|
| `utm_source` | Channel | `twitter`, `linkedin`, `email`, `paid-google` |
| `utm_medium` | Type | `social`, `cpc`, `email`, `display`, `referral` |
| `utm_campaign` | Campaign name | `q3-launch-2026`, `welcome-series` |
| `utm_content` | Variant / placement | `hero-cta`, `footer-cta`, `variant-a` |
| `utm_term` | Keyword (paid) | `marketing+automation`, `crm` |

Use kebab-case, lowercase, no spaces. Underscore allowed.

## Common recipes

### Recipe 1: Single link with UTMs

```bash
LONG_URL="https://yourbrand.com/lp/q3-launch?utm_source=linkedin&utm_medium=social&utm_campaign=q3-launch-2026&utm_content=hero-cta"

curl -X POST https://api-ssl.bitly.com/v4/shorten \
  -H "Authorization: Bearer $BITLY_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"long_url\":\"$LONG_URL\",\"group_guid\":\"$BITLY_GROUP_GUID\",\"domain\":\"$BITLY_CUSTOM_DOMAIN\"}"
```

Returns:

```json
{"link":"https://link.brand.com/3abcXyz","id":"link.brand.com/3abcXyz","long_url":"...","created_at":"..."}
```

### Recipe 2: Bulk shorten (up to 100k)

Build CSV / JSON of long URLs:

```json
{
  "group_guid": "<group>",
  "domain": "link.brand.com",
  "long_urls": [
    {"long_url":"https://brand.com/lp?utm_source=linkedin&utm_medium=social&utm_campaign=q3","tags":["q3-launch","linkedin"]},
    {"long_url":"https://brand.com/lp?utm_source=twitter&utm_medium=social&utm_campaign=q3","tags":["q3-launch","twitter"]},
    {"long_url":"https://brand.com/lp?utm_source=email&utm_medium=email&utm_campaign=q3","tags":["q3-launch","email"]}
  ]
}
```

POST:

```bash
curl -X POST https://api-ssl.bitly.com/v4/bulk_shorten \
  -H "Authorization: Bearer $BITLY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @utms.json
```

Returns array of short links matching input order.

### Recipe 3: CSV → bulk_shorten flow

```bash
# Step 1: prepare CSV with destination URL + UTM params per row
cat campaign-links.csv
# destination,utm_source,utm_medium,utm_campaign,utm_content
# /lp,linkedin,social,q3,hero
# /lp,linkedin,social,q3,footer
# /lp,twitter,social,q3,hero
# /pricing,email,email,q3,header-cta

# Step 2: python preprocess
python3 - <<'EOF'
import csv, json, urllib.parse
base = 'https://yourbrand.com'
rows = []
with open('campaign-links.csv') as f:
    for row in csv.DictReader(f):
        utm = {k:v for k,v in row.items() if k.startswith('utm_')}
        long_url = f"{base}{row['destination']}?{urllib.parse.urlencode(utm)}"
        rows.append({'long_url': long_url, 'tags': [row['utm_campaign'], row['utm_source']]})

payload = {'group_guid': '<group>', 'domain': 'link.brand.com', 'long_urls': rows}
with open('payload.json','w') as f: json.dump(payload, f)
EOF

# Step 3: POST
curl -X POST https://api-ssl.bitly.com/v4/bulk_shorten \
  -H "Authorization: Bearer $BITLY_TOKEN" \
  -d @payload.json > shortlinks.json
```

### Recipe 4: Per-influencer link program

```python
# 50 influencers, each gets a unique UTM
influencers = [
    {'name':'Alice','handle':'@alice','platform':'tiktok'},
    {'name':'Bob','handle':'@bob','platform':'instagram'},
    ...
]

base = 'https://yourbrand.com/promo'
rows = []
for inf in influencers:
    utm = f"utm_source={inf['platform']}&utm_medium=influencer&utm_campaign=q3-launch&utm_content={inf['handle'].replace('@','')}"
    rows.append({'long_url': f"{base}?{utm}", 'tags':['influencer', inf['name']]})

# Bulk shorten
payload = {'group_guid':'<group>','domain':'link.brand.com','long_urls':rows}
resp = requests.post('https://api-ssl.bitly.com/v4/bulk_shorten',
                     headers={'Authorization':f'Bearer {token}'},
                     json=payload).json()

# Hand each influencer their unique short link
for inf, link in zip(influencers, resp['results']):
    notion.create_page(db='influencers', properties={
        'Name': inf['name'],
        'Platform': inf['platform'],
        'Shortlink': link['link'],
    })
```

### Recipe 5: Click-through analytics per shortlink

```bash
# Get clicks for a single shortlink
curl "https://api-ssl.bitly.com/v4/bitlinks/$BITLINK_ID/clicks?unit=day&units=30" \
  -H "Authorization: Bearer $BITLY_TOKEN"

# By country / referrer / device
curl "https://api-ssl.bitly.com/v4/bitlinks/$BITLINK_ID/countries" \
  -H "Authorization: Bearer $BITLY_TOKEN"
```

### Recipe 6: Campaign-tagged analytics rollup

```bash
# All links tagged "q3-launch"
curl "https://api-ssl.bitly.com/v4/groups/$BITLY_GROUP_GUID/bitlinks?tags=q3-launch" \
  -H "Authorization: Bearer $BITLY_TOKEN" \
| jq -r '.links[].id' \
| while read id; do
    clicks=$(curl -s "https://api-ssl.bitly.com/v4/bitlinks/$id/clicks_summary?unit=day&units=30" -H "Authorization: Bearer $BITLY_TOKEN" | jq .total_clicks)
    echo "$id: $clicks clicks"
  done
```

### Recipe 7: Branded domain setup (link.brand.com)

```bash
# Step 1: DNS — add CNAME to bitly.com
# link.brand.com CNAME bsndbk.com (Bitly's CNAME target)

# Step 2: Register in Bitly dashboard
# Settings → Custom domain → Add link.brand.com → wait for verification

# Step 3: Use in API
# Add `"domain":"link.brand.com"` to all shorten calls
```

Branded domains: higher CTR (users trust `link.brand.com` more than `bit.ly/3abcXyz`).

### Recipe 8: QR code generation

```bash
# Get QR for a shortlink
curl "https://api-ssl.bitly.com/v4/bitlinks/$BITLINK_ID/qr?image_format=svg" \
  -H "Authorization: Bearer $BITLY_TOKEN" \
  > qr.svg
```

Use for offline campaigns (print, packaging, signage).

## Examples — Q3 launch UTM matrix

```yaml
campaign: q3-launch-2026
destinations:
  lp: https://brand.com/lp/q3
  pricing: https://brand.com/pricing?promo=q3
  blog_announce: https://brand.com/blog/q3-launch

channels:
  linkedin:
    medium: social
    contents: [hero, footer, comment]
  twitter:
    medium: social
    contents: [tweet-1, tweet-2, thread-final]
  threads:
    medium: social
    contents: [main, follow-up]
  email_newsletter:
    medium: email
    contents: [header, mid-body, footer]
  email_drip:
    medium: email
    contents: [d1, d3, d7, d14]
  paid_google:
    medium: cpc
    contents: [search-ad-1, search-ad-2]
  paid_meta:
    medium: cpc
    contents: [video-hero, carousel-features]
  influencers:
    medium: influencer
    contents: [<unique-per-influencer>]
```

Total combinations: ~3 × 8 × 4 (avg contents) = 96 unique URLs. Single bulk_shorten call → 96 short links → distribute to channels.

## Edge cases

### URL length
Bitly accepts URLs up to 2048 chars. UTMs can blow past this on path-heavy URLs. Consider parameter shortening (`utm_source=li` instead of `linkedin`) only if URL > 2000 chars.

### Custom slugs
For high-visibility links, set custom slug:

```bash
curl -X POST https://api-ssl.bitly.com/v4/shorten \
  -d '{"long_url":"...","custom_bitlink":"link.brand.com/q3-launch"}'
```

Watch for conflicts — Bitly returns 409 if slug taken.

### Rate limits
- 100 req/min (single shorten)
- bulk_shorten: 1 req per 100k URLs counts as 1 call
- 1,000 req/hour for analytics endpoints

### Tags
Tag every shortlink with campaign + channel for later rollup. Max 100 tags per link.

### Bitly plan tiers
- **Free**: 10 custom links/mo, no bulk API, no branded domain
- **Core**: $29/mo, 100/mo, bulk + branded
- **Growth**: $199/mo, 1500/mo, deep link mgmt
- **Premium**: custom, unlimited bulk, dedicated support

For marketing-agent automation, Growth minimum.

### UTM hygiene
- Lowercase everything
- Consistent naming (`q3-launch`, not `q3_launch` or `Q3-Launch`)
- Document conventions in Notion campaign brief template
- GA4 normalizes some sources — don't expect exact match in reports

### Privacy / consent
Bitly tracks clicks via cookies. In EU, consent mode applies — if user hasn't consented, click counted but no fingerprint. Document in privacy policy.

### Link expiration / archival
Bitly doesn't auto-expire. For time-sensitive campaigns, set `archived=true` after end-date to remove from active dashboards (still works as redirect).

### Alternative: dub.co (modern open-source)
Open-source alternative with similar API: https://dub.co — self-hosted free; cloud at $20+/mo. Has built-in UTM builder UI + bulk import.

## Sources

- **Bitly as UTM builder blog**: https://bitly.com/blog/use-bitly-as-utm-builder/
- **Bitly API v4 docs**: https://dev.bitly.com/api-reference
- **Bulk shorten endpoint**: https://dev.bitly.com/api-reference/#bulkShorten
- **UTM convention guide (Google)**: https://support.google.com/analytics/answer/10917952
- **Alternative dub.co**: https://dub.co
