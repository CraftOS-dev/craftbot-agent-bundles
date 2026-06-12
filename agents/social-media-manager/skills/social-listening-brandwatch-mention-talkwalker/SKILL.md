<!--
Source: https://brand24.com/
Brand24 MCP: launched Jan 2026
Brandwatch listening tier comparison: https://www.brandwatch.com/blog/social-listening-tools/
Meltwater: https://www.meltwater.com/en/blog/top-social-listening-tools
Talkwalker (Hootsuite): https://www.talkwalker.com/
-->
# Social Listening — Brand24 / Brandwatch / Talkwalker / Meltwater — SKILL

Listen across 25M+ social + web sources via Brand24 MCP (Jan 2026 launch, AI sentiment with sarcasm + regional-slang handling). Falls through to Talkwalker (30+ networks + 150M web sources, 5-year historical, Hootsuite ecosystem) and Meltwater (TV / radio / podcast / print) for enterprise reach. Daily triage feeds `sentiment-mention-triage`, `social-crisis-comms`, and `ugc-reposting-policy-workflow`.

## When to use this skill

- **Daily brand mention sweep** — who's saying what + sentiment + reach.
- **Hashtag tracking** — branded campaign hashtag volume + co-occurrence + drift.
- **Competitive listening** — competitor mentions, share of voice.
- **Crisis early-detection** — webhook on threshold breach pipes into `social-crisis-comms`.
- **UGC discovery** — branded-hashtag uses + tags feed `ugc-reposting-policy-workflow`.
- **Earned media measurement** — when TV / podcast / print coverage matters, fall to Meltwater.

**Do NOT use this skill when:**
- You need the actual reply to a mention — use `community-engagement-comments-dms-at-scale`.
- The signal is from your own audience (followers, customers) — use platform analytics + `posthog-mcp`.
- A trend is global / not branded — use `social-trend-monitoring-tiktok-sounds-reels`.

## Setup

### Brand24 MCP (default — SMB to mid-market)

```bash
npx -y @brand24/mcp-server@latest
export BRAND24_API_KEY="<key>"   # Individual plan $199/mo, Team $399/mo
export BRAND24_PROJECT_ID="<id>"
```

Or direct REST: `https://api.brand24.com/v3`.

### Talkwalker (enterprise, Hootsuite ecosystem)

```bash
export TALKWALKER_ACCESS_TOKEN="<oauth-token>"
# Endpoint: https://api.talkwalker.com/v1/
```

### Meltwater (earned-media tier)

```bash
export MELTWATER_API_KEY="<key>"
# Endpoint: https://api.meltwater.com/v3
```

### Brandwatch / Sprinklr

Used via dashboard exports for clustering analysis; agent reads exported CSV via `filesystem`.

### Project / topic setup (Brand24)

Each "project" = a tracked entity (brand / campaign / competitor / hashtag). Configure via dashboard with:

- Keywords: brand names, common misspellings, branded hashtags
- Exclude: noise terms, ambiguous homonyms
- Sources: enable all (X, IG, TikTok, FB, YouTube, Reddit, blogs, news, podcasts, forums)
- Language: target locales
- Alerts: webhook → Slack on volume / sentiment thresholds

## Common recipes

### Recipe 1: Daily mention pull (Brand24)

```bash
mcp tool brand24.get_mentions \
  --project_id "$BRAND24_PROJECT_ID" \
  --since "$(date -u -d 'yesterday' +%Y-%m-%d)" \
  --limit 500
```

REST equivalent:

```bash
curl -H "Authorization: Bearer $BRAND24_API_KEY" \
  "https://api.brand24.com/v3/projects/$BRAND24_PROJECT_ID/mentions?since=2026-06-10&limit=500" \
  | jq '.mentions[] | {url, content, author, sentiment, reach, source, created_at}'
```

### Recipe 2: Sentiment breakdown

```bash
mcp tool brand24.get_sentiment_breakdown \
  --project_id "$BRAND24_PROJECT_ID" \
  --period "last_7_days"
# Returns: {positive_count, negative_count, neutral_count, sentiment_score: -1..1}
```

### Recipe 3: Webhook → Slack (threshold alert)

```bash
mcp tool brand24.subscribe_webhook \
  --project_id "$BRAND24_PROJECT_ID" \
  --event "threshold_breach" \
  --url "https://hooks.slack.com/services/<...>" \
  --conditions '{"negative_volume_24h": ">2x_baseline", "single_mention_reach": ">100000"}'
```

When fired, the webhook handler should trigger `social-crisis-comms` immediately.

### Recipe 4: Talkwalker historical query (enterprise)

```bash
curl -X POST https://api.talkwalker.com/v1/search \
  -H "Authorization: Bearer $TALKWALKER_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "(\"yourbrand\" OR \"#yourbrand\") AND NOT (\"yourbrandfanpage\")",
    "from": "2025-06-01",
    "to": "2026-06-01",
    "sources": ["twitter","instagram","tiktok","reddit","facebook","youtube","news","blogs"],
    "languages": ["en","es","de"],
    "limit": 1000
  }'
```

### Recipe 5: Hashtag co-occurrence (campaign drift detection)

```bash
mcp tool brand24.get_co_occurrence \
  --project_id "$BRAND24_PROJECT_ID" \
  --tag "#yourbrandcampaign" \
  --period "last_30_days"
# Returns: [{co_tag: "#summer", count: 142}, ...]
```

Pipe into Notion campaign DB to see what audiences are pairing your hashtag with — early signal of intent or drift.

### Recipe 6: Share of voice (competitor tracking)

```python
brands = ['yourbrand', 'competitor1', 'competitor2', 'competitor3']
sov = {}
for b in brands:
    res = brand24.get_mentions(project_id=projects[b], since=7_days_ago)
    sov[b] = sum(m['reach'] for m in res['mentions'])
total = sum(sov.values())
for b, reach in sov.items():
    print(f"{b}: {reach:,} reach ({100*reach/total:.1f}% SoV)")
```

### Recipe 7: Daily triage table → Notion

```python
mentions = brand24.get_mentions(project_id, since='yesterday', limit=500)
for m in mentions:
    notion.create_page(triage_db, {
        'URL': m['url'],
        'Date': m['created_at'],
        'Channel': m['source'],
        'Author': m['author'],
        'Sentiment': m['sentiment'],  # positive | neutral | negative
        'Reach': m['reach'],
        'Action': decide_action(m),  # reshare / dm-author / monitor / crisis-watch
        'Status': 'new'
    })
```

`decide_action` rules per role.md social listening playbook:
- positive + reach > 10k → reshare candidate
- positive + reach < 10k + UGC pattern → ugc-rights-request
- negative + reach > 100k → crisis-watch
- negative + reach < 100k → dm-author (quiet resolve)
- neutral + reach > 1M → opportunity-watch

### Recipe 8: Meltwater earned-media pull (when needed)

```bash
curl -H "Authorization: Bearer $MELTWATER_API_KEY" \
  "https://api.meltwater.com/v3/search?q=yourbrand&media_types=tv,radio,podcast,print&since=2026-06-01"
```

Use for PR / earned-media reporting — not for routine daily triage.

### Recipe 9: Sentiment delta alert (rolling baseline)

```python
# Track 7-day rolling baseline; alert if today is 2x worse
baseline_neg_per_day = avg([day_neg_count(d) for d in last_7_days])
today_neg = day_neg_count(today)
if today_neg > 2 * baseline_neg_per_day:
    slack.post('#social-listening', f"Negative volume spike: {today_neg} vs baseline {baseline_neg_per_day:.0f}/day")
    trigger_crisis_watch()
```

## Examples

### Example A: Morning brief (9am cron)

```bash
#!/bin/bash
# 1. Pull last 24hr mentions
mcp tool brand24.get_mentions --project_id "$BRAND24_PROJECT_ID" --since "$(date -u -d 'yesterday' +%Y-%m-%d)" > /tmp/mentions.json

# 2. Sentiment summary
mcp tool brand24.get_sentiment_breakdown --project_id "$BRAND24_PROJECT_ID" --period "yesterday" > /tmp/sentiment.json

# 3. Top 5 by reach
jq '.mentions | sort_by(-.reach) | .[0:5]' /tmp/mentions.json

# 4. Post Slack digest
python ./social_listening_digest.py /tmp/mentions.json /tmp/sentiment.json
```

### Example B: Campaign-specific listening project

For a campaign `#brandX_summer2026`:
1. Brand24 project: keywords = campaign hashtag + brand + product names
2. Webhook fires at >50 mentions/hour OR negative sentiment > 30%
3. Notion campaign DB tracks every mention with `Action` and `Status`
4. Daily 6pm summary: total reach / sentiment ratio / top creators using hashtag → UGC pipeline

### Example C: Crisis early-detection chain

```
Brand24 webhook (volume > 2x baseline AND negative > 50%)
  → Slack #crisis-watch with mention cluster URLs
  → Auto-trigger social-crisis-comms skill
  → Draft 3 statement variants (apology / clarification / holding)
  → Pin draft in Slack thread for human review
```

## Edge cases

### Brand24 source coverage gaps
Brand24 strong on social + blogs + forums; weaker on TV / radio / podcast. For those, fall to Meltwater. Brand24 limited China coverage — use `brightdata-mcp` for Weibo / Xiaohongshu.

### False positives on ambiguous brand names
A brand like "Apple" matches fruit-related content. Use AND / NOT operators + exclude common terms in project config.

### Reach numbers are estimates
Brand24 / Talkwalker estimate reach from follower count + post engagement; not actual impressions. Don't quote as exact; use as relative comparison.

### Dark social (DM / WhatsApp / private)
Not detectable by listening tools by definition. Surface via direct customer-feedback channels.

### Sentiment model regional drift
2026 Brand24 model handles English / Spanish / French / German / Portuguese / Italian sarcasm + slang well. Other languages — check confidence scores; manually review low-confidence negatives.

### Volume-based plans
Brand24 plans cap mentions/mo (Individual 2k, Team 10k, Pro 25k). Plan-overage stops tracking — set alert at 80% of monthly cap.

### Talkwalker / Meltwater pricing
Enterprise contracts $$$/yr. Don't recommend unless recipient is already a customer.

### Historical data
Brand24 retains 36 months for Pro plan. Talkwalker 5 years. Meltwater 5+ years. For longer history, use `brightdata-mcp` / `firecrawl` for archived web data.

### API rate limits
Brand24: 100 req/min per key. Talkwalker: depends on plan tier. Cache results per day to avoid re-querying same range.

### GDPR + author handles
Surfacing author handles + content is fair use under most TOS, but storing PII (real names, emails) extracted from posts triggers GDPR / CCPA. Don't store; reference by handle + post URL only.

### Webhook reliability
Set up retry + dead-letter queue. Brand24 webhook retries 3x with exponential backoff; if missed, recipient must poll.

## Sources

- **Brand24**: https://brand24.com/
- **Brand24 MCP launch announcement (Jan 2026)**: https://brand24.com/blog/brand24-mcp-server/
- **Brandwatch — top social listening tools 2026**: https://www.brandwatch.com/blog/social-listening-tools/
- **Meltwater — top 13 social listening tools 2026**: https://www.meltwater.com/en/blog/top-social-listening-tools
- **Talkwalker (Hootsuite)**: https://www.talkwalker.com/
- **Sprinklr Modern Research**: https://www.sprinklr.com/products/insights/modern-research/
- **Awario**: https://awario.com/
