<!--
Source: https://support.google.com/google-ads/answer/2404244
Source: https://revealbot.com/blog/facebook-dayparting
Native geo + Google ad_schedule + Revealbot dayparting (Meta deprecated native dayparting 2024).
-->
# Geo Targeting + Dayparting — SKILL

Geo targeting is platform-native and well-supported across all paid channels. **Dayparting** is messier — Google has native `ad_schedule`, TikTok has a toggle, Meta deprecated native dayparting in 2024 (use Revealbot or scheduled API toggles). This skill ships geo specs, dayparting rules, and platform-specific recipes.

## When to use this skill

- **Time-zone-sensitive offers** — restaurant launches, event tickets, time-bounded promo.
- **B2B workday concentration** — pause overnight + weekends for LinkedIn / Google Search B2B.
- **Service-area business** — local plumber, dentist, gym (zip / radius targeting).
- **Shipping-bounded e-com** — exclude regions you can't ship to.
- **High-fraud regions exclusion** — block known fraud-heavy geos.
- **Multi-market with budget split** — per-region budget allocation.

**Do NOT use this skill when:**
- Global digital product, 24/7 buy intent — let platforms decide.
- New account (first 30d) — restrict less; let platforms learn first.

## Setup

### Platform geo capabilities

| Platform | Geo levels | Format |
|---|---|---|
| Meta | country, region, city, zip, radius | `geo_locations.{countries,regions,cities,zips}` |
| Google | country, region, city, zip, radius | `location_id` from Geo Targets database |
| TikTok | country, region, city | `location_ids` |
| LinkedIn | country, region, metro | `geo` URN |
| Reddit | country, region, city, metro | `geolocations` |

### Dayparting

| Platform | Native dayparting | Workaround |
|---|---|---|
| Meta | DEPRECATED (2024) | Revealbot rule / scheduled API toggle |
| Google | YES (`ad_schedule`) | Native, supports day-of-week + hour ranges + bid modifiers |
| TikTok | YES (ad group toggle) | Native |
| LinkedIn | NO | Scheduled pause/resume via API cron |
| Reddit | NO | Scheduled pause/resume |

## Common recipes

### Recipe 1: Meta geo targeting — multiple cities + radius

```bash
mcp tool meta-ads.create_adset \
  --name "Geo-NYC-Boston-DC" \
  --campaign_id "$CAMPAIGN_ID" \
  --daily_budget 5000 \
  --targeting '{
    "geo_locations": {
      "cities": [
        {"key":"2421836","name":"New York","radius":25,"distance_unit":"mile"},
        {"key":"2393808","name":"Boston","radius":25,"distance_unit":"mile"},
        {"key":"2406835","name":"Washington","radius":25,"distance_unit":"mile"}
      ],
      "location_types": ["home","recent"]
    },
    "age_min": 25, "age_max": 65
  }'
```

City keys via Meta Marketing API search:
```bash
curl "https://graph.facebook.com/v19.0/search?type=adgeolocation&q=Boston&access_token=$META_TOKEN"
```

### Recipe 2: Meta geo exclusion — fraud-heavy regions

```bash
mcp tool meta-ads.update_adset \
  --adset_id "$ADSET_ID" \
  --targeting '{
    "geo_locations":{"countries":["US","CA","UK","AU"]},
    "excluded_geo_locations":{
      "countries":["NG","BD","PK"],
      "regions":[{"key":"<region-id>"}]
    }
  }'
```

### Recipe 3: Google ad_schedule — B2B workday

```bash
# Add ad_schedule criterion to campaign (Mon-Fri 8am-6pm Pacific)
mcp tool google-ads.add_campaign_criterion \
  --customer_id "$CID" \
  --campaign_id "$CAMPAIGN_ID" \
  --criterion_type "AD_SCHEDULE" \
  --ad_schedule '{
    "day_of_week":"MONDAY","start_hour":8,"end_hour":18,"start_minute":"ZERO","end_minute":"ZERO",
    "bid_modifier":1.0
  }'

# Repeat for Tue-Fri
for day in TUESDAY WEDNESDAY THURSDAY FRIDAY; do
  mcp tool google-ads.add_campaign_criterion \
    --campaign_id "$CAMPAIGN_ID" --criterion_type "AD_SCHEDULE" \
    --ad_schedule '{"day_of_week":"'$day'","start_hour":8,"end_hour":18,"start_minute":"ZERO","end_minute":"ZERO","bid_modifier":1.0}'
done
```

Bid modifier 1.2 = +20% bid during peak hour; 0.5 = -50% during low-intent window.

### Recipe 4: Google geo targeting via GAQL — location IDs

```bash
# Find geo_target_constant IDs
mcp tool google-ads.search --customer_id "$CID" --query "
  SELECT geo_target_constant.id, geo_target_constant.name, geo_target_constant.country_code, geo_target_constant.target_type
  FROM geo_target_constant
  WHERE geo_target_constant.name LIKE 'Boston%'"

# Apply to campaign
mcp tool google-ads.add_campaign_criterion \
  --campaign_id "$CAMPAIGN_ID" \
  --criterion_type "LOCATION" \
  --geo_target_constant "geoTargetConstants/1018127"   # Boston, MA
```

### Recipe 5: TikTok dayparting — native via ad group

```bash
curl -X POST "https://business-api.tiktok.com/open_api/v1.3/adgroup/update/" \
  -H "Access-Token: $TT_ACCESS_TOKEN" \
  -d '{
    "advertiser_id":"'$TT_ADVERTISER_ID'",
    "adgroup_id":"'$ADGROUP_ID'",
    "schedule_type":"SCHEDULE_CUSTOMIZE",
    "dayparting":"010000000000000000111111111111111111111111111100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    "schedule_start_time":"2026-06-10 00:00:00",
    "schedule_end_time":"2026-12-31 23:59:59"
  }'
```

The `dayparting` string is 168 chars (24h × 7d). `1` = active, `0` = paused. Order: Mon 0h, 1h, ... 23h, Tue 0h, ...

### Recipe 6: Meta dayparting via Revealbot

```yaml
# Revealbot config (UI-driven; document for repro)
rule_pause_overnight:
  name: "Meta — Pause overnight US East cohort"
  applies_to: adsets where name contains "US-East"
  conditions:
    - hour_local: between 00:00 and 09:00
      timezone: America/New_York
  action: pause
  cooldown: 1h

rule_resume_morning:
  name: "Meta — Resume US East cohort 9am"
  applies_to: same adsets as above
  conditions:
    - hour_local: 09:00
      timezone: America/New_York
  action: enable
  cooldown: 1h
```

### Recipe 7: Custom Python dayparting cron (no Revealbot)

```python
# Cron: 0 * * * * /scripts/meta-dayparting.py
import requests, os, datetime, pytz

ny = pytz.timezone("America/New_York")
now = datetime.datetime.now(ny)
hour = now.hour

# US-East adsets pause overnight 00-09, active 09-23
us_east_adsets = ["adset-id-1","adset-id-2"]
target_status = "ACTIVE" if 9 <= hour < 23 else "PAUSED"

for adset_id in us_east_adsets:
    requests.post(
      f"https://graph.facebook.com/v19.0/{adset_id}",
      data={"status": target_status, "access_token": os.environ["META_ACCESS_TOKEN"]})
```

### Recipe 8: Per-region budget split on Meta (separate adsets)

```bash
for region in US-East US-Central US-West; do
  case $region in
    US-East)    cities='[{"key":"2421836"},{"key":"2393808"},{"key":"2406835"}]'; budget=5000;;
    US-Central) cities='[{"key":"4887398"},{"key":"4684888"}]'; budget=3000;;
    US-West)    cities='[{"key":"5368361"},{"key":"5391959"}]'; budget=4000;;
  esac
  
  mcp tool meta-ads.create_adset \
    --campaign_id "$CAMPAIGN_ID" \
    --name "Geo-$region" \
    --daily_budget $budget \
    --targeting '{"geo_locations":{"cities":'$cities'}}'
done
```

### Recipe 9: Shipping-zone exclusion (e-com)

```bash
# Exclude US territories you don't ship to (Alaska, Hawaii, PR)
mcp tool meta-ads.update_adset \
  --adset_id "$ADSET_ID" \
  --targeting '{
    "geo_locations":{"countries":["US"]},
    "excluded_geo_locations":{"regions":[
      {"key":"3899","name":"Alaska"},
      {"key":"3903","name":"Hawaii"},
      {"key":"3917","name":"Puerto Rico"}
    ]}
  }'
```

## Examples — three deployment patterns

### Pattern A — National DTC, full coverage

```yaml
geo: US, CA (all regions)
excluded: AK, HI, PR (shipping constraint)
dayparting: none (24/7 buy intent for DTC)
```

### Pattern B — B2B SaaS, workday concentration

```yaml
geo: US, CA, UK, AU (English-speaking)
dayparting_google: Mon-Fri 8am-6pm local time, +20% bid 10am-12pm
dayparting_linkedin: same workday schedule via cron-based pause/resume
dayparting_meta: Revealbot rule pause weekends
```

### Pattern C — Local service business, radius target

```yaml
geo:
  - city: Austin, TX
    radius: 25 miles
  - city: San Antonio, TX
    radius: 25 miles
dayparting: peak hours service business
  - Mon-Fri 6am-9pm
  - Sat 8am-8pm
  - Sun 10am-6pm
location_types: ["home","recent"]   # not just travelers
```

## Edge cases

### Meta location_types
- `home`: people who live there
- `recent`: in this location recently  
- `travel_in`: people traveling to this location

Default: all 3. For local businesses, restrict to `home` + `recent` to exclude tourists.

### Google location targeting nuance
- "Presence" (default): people physically in the location
- "Presence or interest": also includes people searching about it
- "Search interest": only people searching about it (rarely useful)

Set via Campaign settings → Location options:
```bash
mcp tool google-ads.update_campaign \
  --campaign_id "$ID" \
  --geo_target_type_setting '{"positive_geo_target_type":"PRESENCE","negative_geo_target_type":"PRESENCE"}'
```

### Radius minimum / maximum
- Meta: 1-50 miles
- Google: 1-500 miles
- For local: 5-25 miles typical

### Multiple zip codes (Meta)
Up to 250 zips per adset. For more, split into multiple adsets.

### TikTok dayparting string encoding
168 chars; Monday 00:00 = position 0; Sunday 23:00 = position 167. Tools that don't expose dayparting natively use bitmask via API.

### LinkedIn dayparting workaround
No native dayparting. Use cron + LinkedIn Marketing API to pause/resume campaign:
```bash
# Pause campaign at 18:00 Fri
curl -X POST "https://api.linkedin.com/rest/adCampaigns/$CAMPAIGN_ID?action=patch" \
  -d '{"patch":{"$set":{"status":"PAUSED"}}}'
```

### Bid modifier vs pause
Google bid modifier `0.5` (-50%) reduces but doesn't stop spend. Use bid modifier for soft dayparting, full pause for hard.

### Time zone conflict
Meta + Google use account-level time zone for reporting. Targeting time zone may differ (Google ad_schedule local time of viewer). Document chosen logic.

### Fraud-heavy regions
Common blocklist: Nigeria, Bangladesh, Pakistan, Vietnam (for B2C DTC fraud-pattern), but evaluate per vertical. Don't over-block legitimate markets.

### City key lookups
Meta:
```bash
curl "https://graph.facebook.com/v19.0/search?type=adgeolocation&q=Boston&access_token=$T"
```
Google: GAQL `geo_target_constant` query.
TikTok: Marketing API `/tool/region/`.

### Holiday/event scheduling
Use `start_time` / `end_time` on adset for event windows (Cyber Monday, conference). Avoid manual pause cron for these.

### Regulatory / political restrictions
Crypto / gambling / political content has region-specific rules. Check each platform's policy.

## Sources

- Meta geo targeting: https://www.facebook.com/business/help/202297959811696
- Meta Geo Targeting API search: https://developers.facebook.com/docs/marketing-api/audiences/reference/targeting-search
- Google ad_schedule: https://support.google.com/google-ads/answer/2404244
- Google geo targeting: https://support.google.com/google-ads/answer/2453995
- Google Geo Target Constants: https://developers.google.com/google-ads/api/reference/data/geotargets
- TikTok ad group dayparting: https://business-api.tiktok.com/portal/docs?id=1739585377598978
- Revealbot dayparting for Meta: https://revealbot.com/blog/facebook-dayparting
- LinkedIn campaign pause/resume API: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/ads-reporting/ad-campaign-groups
- Reddit geo targeting: https://ads-api.reddit.com/docs/v3/#tag/Ad-Groups
