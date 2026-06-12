<!--
Source: https://brand24.com/blog/brand-monitoring-tools/
Brandwatch: https://www.brandwatch.com/
Meltwater: https://www.meltwater.com/
-->
# Brand Reputation Monitoring — Brand24 / Brandwatch / Meltwater + Free Fallback — SKILL

Paid stack (Brand24 $249/mo entry, Brandwatch $800-3K/mo enterprise, Meltwater $25K/yr typical) plus free fallback (`brave-search` + `reddit-mcp` + `twitter-mcp` + `firecrawl-mcp` cron). Tracks mention volume, sentiment velocity, share-of-voice, AI search citation share. Alert thresholds on sentiment drop > 20% or volume spike > 3x baseline.

## When to use this skill

- **Daily brand mention monitoring** — news, blog, social, podcast, forum coverage.
- **Predictive crisis detection** — sentiment velocity tracking before stories explode.
- **Competitive share of voice** — vs 3-10 competitors over weekly windows.
- **AEO/GEO citation tracking** — Brand24 Chatbeat (only native AI visibility dashboard) + Profound/AthenaHQ.
- **Reputation reporting** — weekly client digest of mentions + sentiment + key threads.

**Do NOT use this skill when:**
- The monitoring is for paid ads performance — defer to `marketing-agent`.
- The monitoring is for customer support feedback — defer to `customer-support-agent`.
- The monitoring is for specific review platforms (Trustpilot/G2) — use `online-reputation-mgmt-review-responses`.

## Setup

### Brand24 API

```bash
# https://brand24.com — $249-$799/mo plans
export BRAND24_TOKEN="<token>"
export BRAND24_PROJECT_ID="<id>"
export BRAND24_API_BASE="https://api.brand24.com/v3"
```

Includes Chatbeat AI dashboard (the only native AI search visibility dashboard as of 2026).

### Brandwatch API

```bash
# https://www.brandwatch.com — $800-$3K/mo
export BRANDWATCH_USERNAME="<account>"
export BRANDWATCH_API_KEY="<key>"
export BRANDWATCH_PROJECT_ID="<id>"
export BRANDWATCH_API_BASE="https://api.brandwatch.com/v2"
```

Brandwatch covers 100M+ sources, deep sentiment + sarcasm detection.

### Meltwater API

```bash
# https://www.meltwater.com — ~$25K/yr median per Vendr
export MELTWATER_API_KEY="<key>"
export MELTWATER_API_BASE="https://api.meltwater.com/v3"
```

Meltwater covers 300K+ sources including broadcast/podcast, plus its own journalist DB.

### Free fallback MCPs

`brave-search`, `reddit-mcp`, `twitter-mcp`, `firecrawl-mcp` — already in `agent.yaml`.

### Notion mention DB schema

Per mention:
- `mention_id` (text, dedup key)
- `source` (select: news, blog, twitter, reddit, podcast, video, forum)
- `outlet` (text)
- `url` (URL)
- `date` (datetime)
- `headline` (text)
- `body_snippet` (rich text)
- `sentiment` (select: positive, neutral, negative, mixed)
- `tier` (select: T1, T2, T3, T4 — auto-tag by outlet)
- `topics` (multi-select)
- `mentioned_competitors` (multi-text)
- `requires_response` (checkbox)
- `assigned_to` (text)

## Common recipes

### Recipe 1: Brand24 daily mention pull

```bash
# Get last 24h mentions
curl "$BRAND24_API_BASE/projects/$BRAND24_PROJECT_ID/mentions?period=last_24h&limit=500" \
  -H "Authorization: Bearer $BRAND24_TOKEN" \
| jq '.mentions[] | {
    id, source, outlet, url, date, content, sentiment, reach,
    influence_score, topic_tags
  }' > b24_mentions.json

# Sync to Notion
jq -c '.[]' b24_mentions.json | while read m; do
  notion-mcp upsert_page --db brand_mentions --properties "$m"
done
```

### Recipe 2: Brand24 sentiment velocity alert (webhook)

```bash
# One-time setup
curl -X POST "$BRAND24_API_BASE/projects/$BRAND24_PROJECT_ID/alerts" \
  -H "Authorization: Bearer $BRAND24_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "sentiment_change",
    "threshold_pct": -20,
    "window_hours": 4,
    "callback_url": "https://alert-handler.acme.com/brand24"
  }'

curl -X POST "$BRAND24_API_BASE/projects/$BRAND24_PROJECT_ID/alerts" \
  -H "Authorization: Bearer $BRAND24_TOKEN" \
  -d '{
    "type": "volume_spike",
    "threshold_multiplier": 3,
    "window_hours": 1,
    "callback_url": "https://alert-handler.acme.com/brand24"
  }'
```

Webhook handler:

```python
@app.post('/brand24')
def handle_alert(payload):
    if payload['type'] == 'sentiment_change' and payload['change_pct'] < -20:
        slack_mcp.send(
            channel='#comms-crisis',
            text=f"BRAND24 ALERT: Sentiment dropped {payload['change_pct']}% in {payload['window_hours']}h. Check dashboard: {payload['dashboard_url']}"
        )
        # Pull context
        recent = brand24.get_mentions(period='last_4_hours', sentiment='negative')
        # Pass to crisis-comms-24-48-72-hour-playbook skill if pattern indicates real issue
```

### Recipe 3: Brand24 Chatbeat (AI search citation)

```bash
# Native AI visibility tracking
curl "$BRAND24_API_BASE/projects/$BRAND24_PROJECT_ID/chatbeat?period=last_7_days" \
  -H "Authorization: Bearer $BRAND24_TOKEN" \
| jq '{
    chatgpt_citations: .by_engine.chatgpt,
    gemini_citations: .by_engine.gemini,
    perplexity_citations: .by_engine.perplexity,
    claude_citations: .by_engine.claude,
    top_cited_pages: .top_pages | .[0:10]
  }'
```

Pair with Profound/AthenaHQ for deeper AEO tracking; see role.md AEO section.

### Recipe 4: Brandwatch query (deeper sentiment + sarcasm)

```bash
# Brandwatch tags sarcasm separately
curl "$BRANDWATCH_API_BASE/projects/$BRANDWATCH_PROJECT_ID/mentions?\
filter=query:'Acme Corp'&\
sentiment=positive,neutral,negative,mixed&\
sarcasm_detection=true&\
start=$(date -d '7 days ago' -I)&\
end=$(date -I)" \
  -u "$BRANDWATCH_USERNAME:$BRANDWATCH_API_KEY" \
| jq '.mentions[] | {url, sentiment, sarcasm_detected, content_snippet}'
```

Sarcasm detection matters: "Oh great, another Acme outage!" reads as positive on naive classifiers, negative on Brandwatch.

### Recipe 5: Meltwater broadcast + podcast monitoring

```bash
# Meltwater's strength: broadcast + podcast media
curl "$MELTWATER_API_BASE/mentions?\
query=acme+corp&\
media_types=broadcast,podcast&\
limit=100" \
  -H "X-API-Key: $MELTWATER_API_KEY" \
| jq '.results[] | {
    outlet, show_name, air_date, mention_clip_url,
    transcript_snippet, audience_estimate, sentiment
  }'
```

### Recipe 6: Free fallback — brave-search + reddit + twitter cron

```bash
# Daily 8am ET
brand_keywords=("Acme Corp" "Acme product X" "Jane Smith Acme")

for kw in "${brand_keywords[@]}"; do
  # News mentions
  brave-search "$kw" --since "24h" --type "news" \
  | jq '.results[] | {url, title, snippet, date, source: "brave-news"}' \
  >> daily_mentions.json

  # Reddit
  reddit-mcp search --query "$kw" --since "24h" --sort "new" \
  | jq '.posts[] | {url, title, body, score, subreddit, source: "reddit"}' \
  >> daily_mentions.json

  # Twitter
  twitter-mcp search --query "\"$kw\" -is:retweet" --since "24h" --limit 100 \
  | jq '.tweets[] | {url: ("https://twitter.com/" + .author.username + "/status/" + .id), text, engagement: .public_metrics, source: "twitter"}' \
  >> daily_mentions.json
done

# Dedupe + classify sentiment via Claude
deduped=$(jq -s 'unique_by(.url)' daily_mentions.json)

echo "$deduped" | jq -c '.[]' | while read m; do
  sentiment=$(claude --prompt "Classify sentiment of this mention as positive/neutral/negative/mixed. Output JSON {sentiment: x, confidence: 0-1}. Mention: $m")
  notion-mcp create_page --db brand_mentions --properties "$(jq --arg s "$sentiment" '. + {sentiment: $s}' <<< $m)"
done

# Daily digest to client
gmail-mcp send --to "$CLIENT_EMAIL" \
  --subject "Acme brand monitoring digest $(date -I)" \
  --body "$(format_daily_digest.py)"
```

### Recipe 7: Share of voice calculation

```bash
# Paid (Brand24)
sov=$(curl "$BRAND24_API_BASE/projects/$BRAND24_PROJECT_ID/share-of-voice?\
period=last_7_days&\
competitors=$COMP_1,$COMP_2,$COMP_3" \
  -H "Authorization: Bearer $BRAND24_TOKEN")

echo "$sov" | jq '{
  brand_share: (.brand.mentions / .total),
  competitor_breakdown: .competitors,
  week_over_week: .wow_delta
}'

# Free fallback
brand_count=$(brave-search "Acme Corp" --since "7d" --type news | jq '.results | length')
total=0
for c in "$COMP_1" "$COMP_2" "$COMP_3"; do
  c_count=$(brave-search "$c" --since "7d" --type news | jq '.results | length')
  total=$((total + c_count))
done
total=$((total + brand_count))
echo "Free SoV: $brand_count / $total = $(echo "scale=3; $brand_count / $total" | bc)"
```

### Recipe 8: Weekly digest report

```python
# Cron Mon 9am ET
mentions_last_week = notion.query(
  filter={"date": {"after": (now() - timedelta(days=7)).isoformat()}}
)

digest = {
  'total_mentions': len(mentions_last_week),
  'by_tier': groupby(mentions_last_week, 'tier'),
  'sentiment_breakdown': groupby(mentions_last_week, 'sentiment'),
  'top_5_threads_by_reach': sorted(mentions_last_week, key='reach')[-5:],
  'sentiment_velocity': calc_velocity(mentions_last_week),
  'sov': calc_share_of_voice(mentions_last_week, competitors),
  'aeo_citation_share': brand24_chatbeat.get(period='7d')
}

report = render_docx(template='weekly_brand_digest.docx', data=digest)
gmail_mcp.send(
  to=CLIENT_EMAIL,
  subject=f"Acme weekly brand digest — week of {start_date}",
  body="See attached digest. Key takeaways: ...",
  attachments=[report]
)
```

## Examples — full monitoring program

```yaml
day_1_setup:
  - configure Brand24 / Brandwatch / Meltwater projects (if budgets allow)
  - configure free fallback cron (brave + reddit + twitter daily)
  - configure Notion mention DB
  - set alert thresholds (sentiment -20%, volume 3x)
  - integrate alerts to slack-mcp #comms-crisis

daily_cadence:
  - 0700 ET: free-tier cron runs (brave + reddit + twitter)
  - 0800 ET: brand24 webhook for any pending alerts
  - 0900 ET: claude sentiment classification on overnight mentions
  - throughout day: real-time webhook alerts
  - 1700 ET: end-of-day summary to comms team via slack-mcp

weekly_cadence:
  - mon 0900: digest report generated + emailed to client
  - mon 1000: comms team sentiment review meeting
  - fri 1500: weekly metrics: total mentions, sov, sentiment trend, top threads

monthly_cadence:
  - per-source ROI analysis (paid platforms worth their cost?)
  - alert threshold tuning (too many false positives?)
  - report to client: tier-1 placements, sov, EMV, sentiment trend
```

## Edge cases

### Free fallback covers Day 1 functionality
Recipient may not have Brand24/Brandwatch budget Day 1. Free fallback (`brave-search` + `reddit-mcp` + `twitter-mcp` + `firecrawl-mcp`) provides 60-70% coverage immediately. Upgrade to paid when budget allows.

### Sentiment classifier reliability
Claude sentiment classification is ~85% accurate on clear cases, ~60% on sarcasm/irony. Brandwatch's sarcasm detection is the differentiator for B2C brands with high meme exposure. B2B can lean on Claude.

### Volume baseline = past 14 days, not absolute
"Volume spike >3x" should be measured against trailing 14-day median, not absolute count. Brand size differs; spike that matters for a small brand is noise for a large one.

### Mention deduplication
News syndication = same article reposted on 50 sites. Dedupe by:
- Headline + first-100-chars of body match
- URL canonical (rel=canonical link)
- Outlet group (Reuters wire = group as one)

Without dedup, sentiment metrics get diluted.

### Competitor tracking creates noise
Tracking 10 competitors = 10x noise volume vs tracking 3 strategic competitors. Pick the 3-5 that matter most strategically. Add to/remove from list quarterly.

### Brand name disambiguation
If brand name = common word (Atlas, Pulse, Bridge), add disambiguation context:
- "Acme Corp" → require exact phrase
- "Acme" alone → require co-occurrence with "tech", "AI", "SaaS"
- Negative filter: -recipes, -children's book (if a famous "Acme" exists in another category)

### Tier 1 mentions need immediate triage
A tier-1 outlet (NYT, WSJ, Bloomberg) mention is signal, not noise. Set per-tier alerts:
- T1 mention → Slack immediate page
- T2 mention → daily digest
- T3-T4 → weekly digest

### AEO citation tracking via Chatbeat
Brand24 Chatbeat is the only native AI visibility dashboard. For more granular: pair with Profound API (see role.md AEO section). Track 50-500 brand-relevant prompts daily.

### Crisis detection thresholds
Two alert types for crisis detection:
1. **Sentiment velocity**: net sentiment drops >20% over 4-hour window
2. **Volume spike**: mention count >3x trailing 14-day median over 1-hour window

Both firing simultaneously = strong crisis signal. Auto-activate `crisis-comms-24-48-72-hour-playbook` skill.

### Podcast mention tracking
Meltwater is best for podcast mentions; Brand24 covers some. Free fallback via `youtube-mcp-transcript` + targeted searches for relevant podcasts. Podcast mentions are AEO-friendly (transcripts feed AI training).

### Print clipping OCR
Legacy print press clippings still arrive (esp. for regional / industry trade). Use `gemini-ocr-mcp` or `mistral-ocr-mcp` to digitize → feed into mention DB.

### Multi-language monitoring
For international brands, configure per-language keyword variants. `deepl-mcp` for translation of mentions back to English for unified reporting. Brandwatch + Meltwater both support multi-language natively.

### Influencer mention tracking
Some Brand24/Brandwatch plans include influence scoring. A 5K-follower mention from a category-relevant micro-influencer can outpunch a 500K-follower mention from a generic influencer. Weight by relevance, not raw reach.

### EMV calculation overlay
Per role.md EMV formula. Apply to each mention:
```
EMV = UVM × CPM × tier_multiplier × syndication_factor
```
Where UVM from outlet media kit or SimilarWeb, CPM from outlet's published display rates, tier from outlet rubric. Caveat: directional only.

### Hand-off to crisis comms
When alerts fire and sentiment indicates a real issue, hand off to `crisis-comms-24-48-72-hour-playbook`. This skill is monitoring; the playbook is response.

## Sources

- **Brand24 monitoring tools comparison**: https://brand24.com/blog/brand-monitoring-tools/
- **Brand24 API**: https://api.brand24.com/docs
- **Brand24 Chatbeat (AI visibility)**: https://brand24.com/ai-search/
- **Brandwatch**: https://www.brandwatch.com/
- **Brandwatch API**: https://developers.brandwatch.com/
- **Meltwater**: https://www.meltwater.com/
- **Meltwater API**: https://developer.meltwater.com/
- **Brave Search API**: https://brave.com/search/api/
- **5W PR predictive crisis comms**: https://www.5wpr.com/new/predictive-crisis-communications-using-ai-and-real-time-data/
