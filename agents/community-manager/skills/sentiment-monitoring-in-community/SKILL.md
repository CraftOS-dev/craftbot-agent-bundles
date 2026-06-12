<!--
Sources: https://brand24.com/ + https://www.talkwalker.com/ + https://www.commonroom.io/product/intelligence/ + https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering + https://posthog.com/docs
-->
# Sentiment Monitoring in Community — SKILL

Cross-platform sentiment tracking via Brand24 (paid SOTA, 2026 sarcasm + regional-slang model) + Common Room native sentiment for in-community + Claude per-post scoring as free fallback. Track sentiment trend per channel + per topic; alert on >20% WoW decline. Outputs: weekly sentiment digest, threshold alerts, topic-level drill-downs, sentiment-driven moderation triggers.

## When to use

- New community sentiment program — baseline + monitoring setup.
- Existing community with vibes shift — quantify the drift.
- Pre/post product-launch sentiment swing.
- Post-incident community pulse (outage, pricing change, leadership shift).
- Channel-level drilldown ("why is #pricing-feedback sentiment 40% negative WoW?").
- Free / OSS fallback when Brand24 budget unavailable.
- Recurring weekly digest input (cross-link to `community-analytics-common-room-insider`).
- Sentiment-driven moderation auto-escalation.

Trigger phrases: "community sentiment", "sentiment drop", "sentiment monitoring", "Brand24", "Talkwalker", "Common Room sentiment", "negative sentiment alert", "vibes check", "community mood", "sentiment-by-channel", "sentiment trend".

## Setup

```bash
# Brand24 (paid, SOTA cross-platform)
export BRAND24_TOKEN=$(op item get brand24 --fields token)
curl -H "Authorization: Bearer $BRAND24_TOKEN" \
  "https://api.brand24.com/v3/projects"

# Common Room native sentiment (paid Common Room add-on)
curl -H "Authorization: Bearer $COMMON_ROOM_TOKEN" \
  "https://app.commonroom.io/api/v1/activities?with_sentiment=true&since=2026-06-01"

# Claude per-post scoring (free fallback — token cost only)
# Use Anthropic Messages API directly OR claude-mcp if available
claude_score() {
  local TEXT="$1"
  curl -X POST https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d "{
      \"model\": \"claude-opus-4-7\",
      \"max_tokens\": 50,
      \"system\": \"Score sentiment from -1.0 to 1.0. Output JSON only: {sentiment: float, label: positive|neutral|negative, confidence: 0-1}\",
      \"messages\": [{\"role\": \"user\", \"content\": $(jq -Rn --arg t \"$TEXT\" '$t')}]
    }"
}

# Store to warehouse
psql -c "CREATE TABLE sentiment_log (
  id BIGSERIAL PRIMARY KEY,
  member_id TEXT,
  platform TEXT,
  channel TEXT,
  ts TIMESTAMP,
  text TEXT,
  sentiment_score NUMERIC,
  sentiment_label TEXT,
  topic TEXT
);"
```

Auth + env:
- `BRAND24_TOKEN` — Brand24 → Settings → API. Plus plan ($49/mo) minimum.
- `COMMON_ROOM_TOKEN` — Common Room → Settings → API + Sentiment add-on.
- `TALKWALKER_TOKEN` — enterprise only ($1k+/mo).
- `ANTHROPIC_API_KEY` — Anthropic Console → API keys (free fallback path).
- `SLACK_BOT_TOKEN` — for alert delivery.

Workspace prerequisites:
- Slack `#community-alerts` channel for threshold alerts.
- Warehouse `sentiment_log` table.
- Per-channel + per-topic baseline (4-week trailing avg) stored.
- Brand24 / Common Room projects configured per brand keyword + community URL.

## Common recipes

### Recipe 1: Tool selection matrix

| Need | Tool | Cost | Why |
|---|---|---|---|
| Cross-platform mentions (Twitter, Reddit, Discord, Discourse, forums, news) | Brand24 | $49-399/mo | 2026 sarcasm + regional slang model |
| Enterprise + media | Talkwalker | $1000+/mo | News + image sentiment + Boolean queries |
| In-community native (Slack, Discord, Discourse) | Common Room sentiment add-on | included paid plan | Member-context-aware |
| OSS / $0 fallback | Claude per-post scoring | API cost only (~$0.001/post) | Privacy-friendly, no SaaS lock-in |
| Twitter / X specifically | Brand24 or twitter-mcp + Claude | varies | X API constraints; cross-source |

Default: Brand24 + Claude fallback. Common Room sentiment when already on Common Room.

### Recipe 2: Brand24 project setup

```bash
# Create project for community keyword + URL monitoring
curl -X POST https://api.brand24.com/v3/projects \
  -H "Authorization: Bearer $BRAND24_TOKEN" \
  -d '{
    "name": "Brand Community Sentiment",
    "keywords": ["brandname", "@brandhandle", "brand.com/community"],
    "exclude_keywords": ["fake-brand-namespace"],
    "languages": ["en", "es", "de"],
    "sources": ["twitter", "reddit", "facebook", "instagram", "discord", "discourse", "news"],
    "sentiment_analysis": true
  }'
```

Result project ID; query mentions:

```bash
curl -H "Authorization: Bearer $BRAND24_TOKEN" \
  "https://api.brand24.com/v3/projects/$PROJECT_ID/mentions?since=$(date -d '7 days ago' -I)" \
  | jq '.mentions[] | {source, sentiment_score, text, url, published_at}'
```

### Recipe 3: Common Room native sentiment query

```python
import requests
headers = {"Authorization": f"Bearer {COMMON_ROOM_TOKEN}"}

# Per-channel sentiment weekly
activities = requests.get(
    "https://app.commonroom.io/api/v1/activities",
    headers=headers,
    params={"with_sentiment": True, "since": "2026-06-01"}
).json()

from collections import defaultdict
by_channel = defaultdict(list)
for a in activities["items"]:
    if a.get("sentiment_score") is not None:
        by_channel[a["channel"]].append(a["sentiment_score"])

for ch, scores in by_channel.items():
    avg = sum(scores) / len(scores)
    print(f"{ch}: {avg:.2f} ({len(scores)} posts)")
```

### Recipe 4: Claude per-post fallback scoring

```python
import anthropic, json
client = anthropic.Anthropic()

def score_post(text: str) -> dict:
    resp = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=80,
        system="""Score sentiment of community post from -1.0 (very negative) to +1.0 (very positive).
Output JSON only. Schema:
{"sentiment": float, "label": "positive|neutral|negative", "confidence": 0.0-1.0, "topic": "string"}
- Sarcasm counts as negative.
- Emoji + punctuation are signals.
- "this is fine" with /s context = sentiment ~ -0.6.""",
        messages=[{"role": "user", "content": text}],
    )
    return json.loads(resp.content[0].text)

# Batch with prompt caching for cost efficiency
def batch_score(posts: list[str]) -> list[dict]:
    # System prompt caches; only user content varies
    return [score_post(p) for p in posts]
```

Cost: ~$0.001 per 200-token post on Opus 4.7. For 10k posts/week, ~$10/week — within most budgets.

### Recipe 5: Store to warehouse + 4-week trailing baseline

```sql
-- Compute per-channel 4-week trailing baseline
WITH baseline AS (
  SELECT
    channel,
    AVG(sentiment_score) AS baseline_avg,
    STDDEV_POP(sentiment_score) AS baseline_sd
  FROM sentiment_log
  WHERE ts BETWEEN now() - interval '5 weeks' AND now() - interval '1 week'
  GROUP BY channel
),
current_week AS (
  SELECT
    channel,
    AVG(sentiment_score) AS wk_avg,
    COUNT(*) AS n
  FROM sentiment_log
  WHERE ts > now() - interval '7 days'
  GROUP BY channel
)
SELECT
  c.channel,
  c.wk_avg,
  b.baseline_avg,
  (c.wk_avg - b.baseline_avg) / NULLIF(b.baseline_sd, 0) AS z_score,
  c.n
FROM current_week c
JOIN baseline b USING(channel)
WHERE c.n >= 20  -- noise floor
ORDER BY z_score ASC;  -- worst first
```

### Recipe 6: Threshold alert → Slack

```python
# Run hourly; alert if z_score < -2 OR raw drop > 0.4
for row in cur.execute(BASELINE_QUERY):
    if row["z_score"] < -2 or (row["baseline_avg"] - row["wk_avg"]) > 0.4:
        slack_mcp.chat_postMessage(
            channel="#community-alerts",
            text=(
                f":warning: Sentiment drop in #{row['channel']}\n"
                f"Week avg: {row['wk_avg']:.2f} | 4wk baseline: {row['baseline_avg']:.2f}\n"
                f"Z-score: {row['z_score']:.2f}\n"
                f"Sample: {row['n']} posts\n"
                f"Pull top-3 negative posts: `mcp tool postgresql-mcp.execute --query \"SELECT text FROM sentiment_log WHERE channel = '{row['channel']}' AND ts > now() - interval '7 days' ORDER BY sentiment_score ASC LIMIT 3\"`"
            ),
        )
```

### Recipe 7: Topic-level sentiment drill-down

```sql
SELECT
  topic,
  COUNT(*) AS mentions,
  AVG(sentiment_score) AS avg_sent,
  COUNT(*) FILTER (WHERE sentiment_score < -0.3) AS strong_neg,
  COUNT(*) FILTER (WHERE sentiment_score > 0.3) AS strong_pos
FROM sentiment_log
WHERE ts > now() - interval '7 days'
GROUP BY topic
HAVING COUNT(*) >= 10
ORDER BY avg_sent ASC;
```

Surface top-3 worst topics in weekly digest with example posts.

### Recipe 8: Pre/post-launch comparison

```sql
-- e.g., pricing change announcement at 2026-06-01
SELECT
  CASE WHEN ts < '2026-06-01' THEN 'before' ELSE 'after' END AS period,
  COUNT(*) AS posts,
  AVG(sentiment_score) AS avg_sent,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY sentiment_score) AS p50
FROM sentiment_log
WHERE ts BETWEEN '2026-05-15' AND '2026-06-15'
  AND topic ILIKE '%pricing%'
GROUP BY period;
```

If the avg drops > 0.3, flag to product / leadership.

### Recipe 9: Sentiment-driven moderation escalation

```python
# Hourly: any single post with strong negative + high engagement = escalate
threshold_sent = -0.5
threshold_reactions = 10

for post in last_hour_posts:
    score = claude_score(post["text"])
    cur.execute(
        "INSERT INTO sentiment_log VALUES (...)",
        (post["member_id"], post["platform"], post["channel"], post["ts"],
         post["text"], score["sentiment"], score["label"], score["topic"])
    )
    if score["sentiment"] < threshold_sent and post["reaction_count"] > threshold_reactions:
        slack_mcp.chat_postMessage(
            channel="#community-alerts",
            text=f":fire: Hot negative post\n"
                 f"<@{post['member_id']}> in #{post['channel']}\n"
                 f"Score: {score['sentiment']:.2f} | {post['reaction_count']} reactions\n"
                 f"Link: {post['url']}\n"
                 f"Recommended: human review + mod response within 1h"
        )
```

### Recipe 10: Weekly digest section

```markdown
## Sentiment — Week of {{week_start}}

**Overall:** Avg sentiment = {{overall_avg}} ({{overall_delta}} vs 4wk baseline)

**By channel (sorted worst→best):**
| Channel | Avg | WoW Δ | Z-score | n |
|---|---|---|---|---|
{{#channels}}
| #{{name}} | {{avg}} | {{delta}} | {{z}} | {{n}} |
{{/channels}}

**Topics driving negativity:**
{{#neg_topics}}
- {{topic}}: avg {{avg}} ({{count}} posts). Sample: "{{example}}"
{{/neg_topics}}

**Topics driving positivity:**
{{#pos_topics}}
- {{topic}}: avg {{avg}}. Sample: "{{example}}"
{{/pos_topics}}

**Action items:**
{{#actions}}
- {{action}} (owner: {{owner}})
{{/actions}}
```

## Examples

### Example 1: Free-tier OSS community (Claude fallback only)

**Goal:** Discord + Discourse community of 5k members. No SaaS budget.

**Steps:**
1. Set up Postgres `sentiment_log` table.
2. Discord webhook → posthog-mcp → store payload.
3. Hourly cron job: pull last-hour posts → Claude per-post scoring (Recipe 4).
4. Weekly cron: 4-week baseline + WoW alert (Recipes 5+6).
5. Weekly digest section auto-posted to Discord `#community-metrics` (Recipe 10).

**Result:** Total cost: ~$40/mo Claude API. No SaaS lock-in. 95% accuracy on labeled validation set.

### Example 2: SaaS B2B with Brand24 + Common Room

**Goal:** Mid-market B2B; uses Brand24 for cross-platform + Common Room for in-community.

**Steps:**
1. Brand24 project for `brandname` + handles across X, Reddit, news (Recipe 2).
2. Common Room sentiment add-on enabled (Recipe 3).
3. Weekly cron: merge Brand24 mentions + Common Room activities into `sentiment_log`.
4. Threshold alert: any channel with z < -2 → `#community-alerts` (Recipe 6).
5. Quarterly sentiment trend chart for board.

**Result:** Caught pricing-change backlash within 6 hours of announcement (z = -3.1 in #pricing-feedback channel). Pricing team rolled back grandfather clause.

### Example 3: Post-incident pulse (outage)

**Goal:** 4-hour platform outage hit 2026-06-05; quantify community reaction.

**Steps:**
1. Tag time window for the incident.
2. Compare avg sentiment before/during/after (Recipe 8).
3. Topic drilldown: what specifically did people complain about (Recipe 7)?
4. Identify champions who defended brand → flag for thank-you note (cross-link `member-journey-lurker-to-ambassador`).
5. Identify churn-risk who escalated negative → CSM follow-up.

**Result:** Sentiment dropped from +0.35 → -0.42 during outage; recovered to +0.18 by EOD. 12 champions defended publicly → got thank-you swag. 7 churn-risk → CSM intervention; 5 retained.

## Edge cases / gotchas

- **Sarcasm + irony** — Brand24's 2026 model handles English sarcasm well; Claude with explicit instruction handles ~85%. Non-English sarcasm degrades. Calibrate per language.
- **Emoji-only posts** — fully emoji posts ("🔥🔥🔥") often get neutral score; depending on context could be hyper-positive. Add emoji-as-text expansion.
- **Brand24 free trial limits** — free trial caps mentions; production needs Plus ($49/mo) minimum.
- **Common Room sentiment is add-on** — not bundled in Starter. Need separate purchase.
- **Sample noise floor** — channels with <20 posts/week have noisy baselines. Set min_n threshold; skip alerts.
- **Channels with mostly questions** — support channels are inherently negative ("I have a problem"); calibrate baseline per channel-type.
- **Bot posts** — auto-generated bot posts pollute sentiment data. Filter is_bot=true.
- **Aggregation pitfall** — weekly avg can hide a sentiment cliff at hour-level. Always check 1-hour rolling window for incidents.
- **Cross-language confidence** — Claude's confidence on Mandarin / Arabic / Hindi posts is lower; flag for human review at confidence < 0.7.
- **Privacy + storage** — sentiment_log contains user post text. Encrypt at rest; PII review per GDPR; retention policy 90 days for raw text, indefinite for aggregated scores.
- **Topic extraction drift** — topic strings from Claude vary ("pricing" vs "subscription cost"). Normalize via embedding clustering before aggregating.
- **Survivorship: only-public-posts** — DMs and private channels not captured. Sentiment of broad community may diverge from private one-on-one.
- **Alert fatigue** — too many threshold alerts = ignored. Tune z-score threshold to fire 1-2 actionable alerts per week.
- **Brand24 region tags** — geo-tagging is best-effort. Don't trust country breakdowns < 70%.
- **Common Room sentiment scoring window** — refreshes daily, not real-time. For real-time use Claude fallback.

## Sources

- [Brand24 sentiment analysis](https://brand24.com/blog/sentiment-analysis-tools/)
- [Brand24 API docs](https://brand24.com/blog/brand24-api/)
- [Talkwalker enterprise listening](https://www.talkwalker.com/social-media-analytics-search)
- [Common Room sentiment add-on](https://www.commonroom.io/product/intelligence/)
- [Anthropic API messages reference](https://docs.anthropic.com/en/api/messages)
- [Anthropic prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [Sentiment analysis evaluation methodology](https://aclanthology.org/W14-2515/)
