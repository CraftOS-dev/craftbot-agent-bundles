<!--
Source: https://muckrack.com/pr-software/api
Cision: https://www.cision.com/products/cision-one/
Roxhill: https://www.roxhillmedia.com/
-->
# Media List Building — Muck Rack + Cision + Roxhill — SKILL

Build, maintain, and auto-refresh journalist media lists from Muck Rack (US default), Cision (broadcast + podcast), and Roxhill (UK/EU). Store as a relationship CRM in Notion with outlet-change webhook alerts, last-pitched/last-placed dates, and beat tags for fast journalist-to-story matching.

## When to use this skill

- **New campaign launch** — build a 50-200-journalist target list filtered by beat + outlet + recent coverage.
- **Routine relationship maintenance** — quarterly list refresh, beat-shift detection, outlet-change alerts.
- **Specific story pitching** — narrow query for "journalists who wrote about MPP measurement in last 90 days at tier-1 outlets."
- **Crisis comms** — pre-built tier-1 list ready to fire individual `gmail-mcp` sends in <10 min.
- **Multi-region launches** — Muck Rack for US, Roxhill for UK/EU, Cision for broadcast across regions.

**Do NOT use this skill when:**
- Pitching a specific HARO/Featured/Qwoted query — use `haro-qwoted-featured-sme-quotes` (the journalist is already named).
- Booking podcast guest spots — use `podcast-tour-booking-for-execs`.
- Submitting to award judges — use `award-list-submissions-inc-forbes-fast-co`.

## Setup

### Muck Rack API

```bash
# Subscription tiers: $5K-$10K+/year per seat
# Generate API key in https://muckrack.com/account/api
export MUCKRACK_API_KEY="<key>"
export MUCKRACK_API_BASE="https://api.muckrack.com/v1"
```

### Cision CisionOne API

```bash
# Enterprise pricing (~$15K-$30K/year)
export CISION_USERNAME="<account>"
export CISION_API_KEY="<key>"
export CISION_API_BASE="https://api.cisionone.com/v1"
```

### Roxhill API (UK/EU)

```bash
# £8K-£15K/year
export ROXHILL_API_KEY="<key>"
export ROXHILL_API_BASE="https://api.roxhillmedia.com/v1"
```

### Notion media-list DB schema

Required fields (per row = one journalist):
- `name` (text)
- `outlet` (text)
- `outlet_tier` (T1/T2/T3/T4 select)
- `email` (email)
- `phone` (text, optional)
- `twitter` / `bluesky` / `linkedin` (URLs)
- `beats` (multi-select: AI, Healthtech, Climate, Fintech, etc.)
- `region` (US / EU / UK / APAC / LatAm)
- `last_5_article_urls` (multi-text)
- `last_pitched` (date)
- `last_placement` (date + URL)
- `relationship_signal` (text: prior coffee, met at conf, intro via X)
- `prefs` (text: morning email, no Friday pitches, embargo OK)
- `muckrack_id` (text, for webhook updates)
- `attribution_history` (multi-text: on-record / on-background defaults)

## Common recipes

### Recipe 1: Build a new media list (Claude-described → Muck Rack AI Media List Agent)

```bash
# Natural-language brief
brief='Tier-1 tech journalists covering email marketing, MPP measurement, or Klaviyo
in the US, who published in the last 60 days.'

curl -X POST "$MUCKRACK_API_BASE/media-list-agent/build" \
  -H "Authorization: Bearer $MUCKRACK_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"description\": \"$brief\",
    \"max_results\": 75,
    \"filters\": {
      \"region\": [\"US\"],
      \"published_within_days\": 60,
      \"min_outlet_tier\": \"T2\"
    }
  }" | jq '.journalists[] | {name, outlet, beat, last_article_url}' > media_list.json
```

### Recipe 2: Search by beat + outlet + keywords

```bash
curl "$MUCKRACK_API_BASE/search?\
beat=email-marketing&\
outlet=techcrunch,bloomberg,wsj,axios&\
keyword=MPP+measurement&\
published_within_days=90&\
limit=50" \
  -H "Authorization: Bearer $MUCKRACK_API_KEY" \
| jq '.results[] | {id, name, outlet, email, recent_articles: [.recent_articles[0:3] | .[] | {title, url, date}]}'
```

### Recipe 3: Pull full journalist profile (for warm pitch personalization)

```bash
curl "$MUCKRACK_API_BASE/journalists/$muckrack_id?include=articles,social,podcasts" \
  -H "Authorization: Bearer $MUCKRACK_API_KEY" \
| jq '{
    name: .name,
    title: .title,
    outlet: .outlet.name,
    bio: .bio,
    beats: .beats,
    last_10_articles: .articles[0:10] | map({title, url, date}),
    twitter_handle: .social.twitter,
    bluesky_handle: .social.bluesky,
    recent_pods: .podcast_appearances[0:5]
  }'
```

### Recipe 4: Cision broadcast + podcast index

```bash
# Cision excels at broadcast (TV/radio) + podcast indexing
curl "$CISION_API_BASE/journalists/search?\
medium=broadcast,podcast&\
beat=technology&\
region=US&\
limit=50" \
  -u "$CISION_USERNAME:$CISION_API_KEY" \
| jq '.results[] | {name, outlet, medium, show_name, audience_estimate}'
```

### Recipe 5: Roxhill (UK/EU trade press)

```bash
curl "$ROXHILL_API_BASE/search?\
beat=fintech&\
country=GB,FR,DE&\
outlet_type=trade&\
limit=50" \
  -H "X-API-Key: $ROXHILL_API_KEY" \
| jq '.journalists[] | {name, outlet, country, language, last_article_url}'
```

### Recipe 6: Sync results into Notion CRM

```python
# pseudo-code
import json
for j in json.load(open('media_list.json')):
    notion.create_page(
      database_id=MEDIA_LIST_DB,
      properties={
        'name': {'title': [{'text': {'content': j['name']}}]},
        'outlet': {'rich_text': [{'text': {'content': j['outlet']}}]},
        'outlet_tier': {'select': {'name': resolve_tier(j['outlet'])}},
        'email': {'email': j['email']},
        'beats': {'multi_select': [{'name': b} for b in j['beats']]},
        'muckrack_id': {'rich_text': [{'text': {'content': str(j['id'])}}]},
        'last_5_article_urls': {'rich_text': [{'text': {'content': '\n'.join(j['recent_articles'])}}]},
      }
    )
```

### Recipe 7: Outlet-change webhook (auto-update Notion)

```bash
# One-time subscription
curl -X POST "$MUCKRACK_API_BASE/webhooks" \
  -H "Authorization: Bearer $MUCKRACK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "journalist.outlet_change",
    "callback_url": "https://your-handler.com/webhook/muckrack",
    "filters": {"list_ids": ["<your-list-id>"]}
  }'

# Webhook handler (pseudo)
def handle_outlet_change(payload):
    j_id = payload['journalist_id']
    new_outlet = payload['new_outlet']
    notion.update_row(filter={'muckrack_id': j_id}, set={'outlet': new_outlet})
    gmail_mcp.send(
        to='pr-lead@acme.com',
        subject=f"{payload['journalist_name']} moved to {new_outlet}",
        body=f"Update relationship notes; consider re-intro email."
    )
```

### Recipe 8: Weekly list-hygiene cron

```bash
# Run every Monday morning
for j in $(notion query 'media_list/all'); do
  muckrack_id=$(echo "$j" | jq -r .muckrack_id)
  fresh=$(curl -s "$MUCKRACK_API_BASE/journalists/$muckrack_id" -H "Authorization: Bearer $MUCKRACK_API_KEY")

  current_outlet=$(echo "$fresh" | jq -r .outlet.name)
  prior_outlet=$(echo "$j" | jq -r .outlet)

  if [ "$current_outlet" != "$prior_outlet" ]; then
    notion-mcp update_row --id $(echo "$j" | jq -r .id) --outlet "$current_outlet"
    echo "Updated: ${prior_outlet} -> ${current_outlet} for $(echo "$j" | jq -r .name)"
  fi
done
```

## Examples — campaign-targeted list build

```yaml
campaign: Series B announcement
target_size: 80 journalists
mix:
  - 12 tier-1 (NYT, WSJ, Bloomberg, Reuters, FT, Forbes, The Information, Axios Pro Rata)
  - 35 tier-2 trade (TechCrunch, VentureBeat, Crunchbase News, PitchBook News, etc.)
  - 25 tier-3 niche (sector-specific blogs + newsletters)
  - 8 broadcast (CNBC, Bloomberg TV, NPR Marketplace)

build_steps:
  1. muck rack ai media list agent: describe brief in natural language
  2. filter: published last 90 days + covered Series A/B + tech category
  3. enrich: pull each journalist's last 5 articles
  4. cross-check: roxhill for UK/EU adds + cision for broadcast
  5. sync to notion with relationship signals
  6. tag attribution defaults from notion interaction log
  7. flag any blacklisted outlets (prior embargo break)
```

## Edge cases

### List rot — addresses go stale fast
Journalists move every 18-36 months on average. Muck Rack auto-updates via webhook (recipe 7). Without that, lists rot 15-25%/year. Always re-verify before a campaign. Don't ship a 2-year-old list.

### Free fallback when no paid DB
If recipient doesn't have Muck Rack/Cision/Roxhill:
1. `brave-search` site search: `site:bloomberg.com "Jane Smith" -site:linkedin.com` → finds bylines + role
2. `firecrawl-mcp` outlet masthead crawl → captures team page
3. Public Twitter/Bluesky for handles
4. Featured.com daily digest mentions named journalists by beat
5. Manual entry into Notion — slower but works Day 1

### Attribution discipline pre-load
Every journalist row should have `attribution_default` populated FROM the first interaction onward. If a journalist says "let's keep this on background" once, default future to background unless they re-opt to on-record. Per the role.md interaction log discipline.

### Beat tagging discipline
Don't over-tag a journalist with 10 beats. Pick 2-3 primary beats. Over-tagging dilutes the search match score downstream.

### Outlet-tier rubric in Notion
Maintain the tier rubric in a separate Notion DB and join via `outlet` field:
- T1: NYT, WSJ, Bloomberg, Reuters, AP, FT, The Economist, major broadcast, Forbes, Fortune
- T2: TechCrunch, The Information, Axios Pro Rata, Marketing Brew, AdAge, Wired, The Verge, NPR
- T3: niche + regional + syndicated
- T4: self-published + owned

Auto-tag tier on every new journalist row.

### Broadcast vs print journalists
Different prep, different pitch length. Broadcast: 3-sentence pitch, hook + sound bite + spokesperson availability. Print: standard 150-word pitch with data + exclusive. Tag `medium` field per journalist.

### Podcast hosts on the list
Podcast hosts overlap with the `podcast-tour-booking-for-execs` skill workflow. Treat as a separate column rather than mixing into the journalist list — different pitch playbook.

### Region/language filter critical
US, UK, EU, APAC, LatAm each have different prefs. UK journalists hate Americanisms. German/French trade press require native-language pitches. Tag region + language on every row; route language via `deepl-mcp` when pitching.

### Notion 100-property limit
Notion DB cap is 100 properties per database. Stay under by keeping rich-text aggregations (`last_5_article_urls`) as single fields with newline separators, not 5 separate properties.

### Sensitive journalist data
Personal phone numbers and home addresses appear in Muck Rack/Cision — handle as PII. Restrict Notion DB access; never include in any shared doc.

### Cost-controlling Muck Rack queries
Muck Rack charges per query above contract tier. Build the list query-efficient: use AI Media List Agent (1 query → 75 results) instead of individual `/search` calls. Cache profiles for 30 days unless outlet-change webhook fires.

## Sources

- **Muck Rack API + Media DB**: https://muckrack.com/pr-software/api
- **Muck Rack media DB guide**: https://muckrack.com/blog/2024/07/18/media-database-guide/
- **Cision CisionOne**: https://www.cision.com/products/cision-one/
- **Roxhill Media**: https://www.roxhillmedia.com/
- **Notion API**: https://developers.notion.com/
- **Outlet tier rubric (PR industry standard)**: https://bospar.com/how-to-master-award-submissions/
