<!--
Source: https://loris.ai/ + https://klausapp.com/api + Claude fallback
-->
# Sentiment Analysis + Cohort Trends — SKILL

Per-conversation sentiment scoring (Loris.ai / Klaus / Stylus) plus warehouse-backed cohort trend analysis. Free Claude-on-transcript fallback when no paid scoring tool is available. Outputs a 0-100 sentiment score + emotion classification (angry / frustrated / confused / neutral / satisfied / delighted).

## When to use

- **Score every closed ticket** with a sentiment value for weekly cohort tracking.
- **Detect cohort drops** — week-over-week sentiment decline > 20% → product regression flag.
- **Detractor auto-route** — score < 30 routes to CSM within 1h.
- **Cross-reference with releases** — sentiment drop post-release X = likely regression.
- **Free fallback workflow** when Loris / Klaus budget is unavailable — Claude on the transcript with a structured prompt.

Trigger phrases: "score this conversation sentiment", "cohort sentiment trend", "detractor list this week", "find frustrated customers".

## Setup

```bash
# Loris.ai: paid, contact-only. No public self-serve signup as of June 2026.
# Klaus (Zendesk QA): paid; API at https://api.klausapp.com
# Free fallback: Claude on transcript via cli-anything

# Loris (if you have API access)
curl -sS https://api.loris.ai/v1/health -H "Authorization: Bearer $LORIS_API_KEY"

# Klaus
curl -sS https://api.klausapp.com/v1/me \
  -H "Authorization: Bearer $KLAUS_API_KEY"
```

Auth + env:
- `LORIS_API_KEY` — provisioned by Loris during onboarding. Paid; contact sales.
- `KLAUS_API_KEY` — at Klaus settings; paid (Zendesk QA bundle).
- `ANTHROPIC_API_KEY` — for the free Claude fallback (always-available).

Prerequisites:
- A warehouse table `support.sentiment_scores` with columns `ticket_id`, `score`, `emotion`, `scored_at`, `source` (loris / klaus / claude). Use `postgresql-mcp` for queries.

## Common recipes

### Recipe 1: Score a transcript via Loris

```bash
TRANSCRIPT=$(jq -n --argjson msgs "$messages_json" '{transcript: $msgs, language: "en"}')

curl -sS -X POST "https://api.loris.ai/v1/transcripts/analyze" \
  -H "Authorization: Bearer $LORIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$TRANSCRIPT" | jq '{score: .sentiment_score, emotion: .emotion, drivers: .drivers, resolved: .resolution_status}'
```

Loris returns: numeric 0-100 score, dominant emotion label, top drivers (e.g., `pricing`, `outage`, `slow_response`), `resolution_status` boolean.

### Recipe 2: Score a transcript via Klaus

```bash
curl -sS -X POST "https://api.klausapp.com/v1/auto-qa/scores" \
  -H "Authorization: Bearer $KLAUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id":"int_abc123",
    "source":"intercom",
    "transcript":"...",
    "agent_id":"agent_001"
  }' | jq '{score: .sentiment, categories: .auto_categories}'
```

Klaus is QA-cohort-oriented (agent performance + conversation quality), Loris is sentiment-oriented (customer mood). Use both if budget allows.

### Recipe 3: Free fallback — Claude on transcript

```bash
TRANSCRIPT_TEXT=$(curl -sS https://api.intercom.io/conversations/$CONV_ID \
  -H "Authorization: Bearer $INTERCOM_TOKEN" -H "Intercom-Version: 2.13" \
  -G --data-urlencode "display_as=plaintext" | jq -r '.conversation_parts.conversation_parts[].body')

curl -sS https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d @<(cat <<EOF
{
  "model": "claude-sonnet-4-5-20250929",
  "max_tokens": 256,
  "messages": [{
    "role":"user",
    "content":"Score this support conversation 0-100 on customer sentiment (0=furious, 100=delighted). Classify dominant emotion (angry|frustrated|confused|neutral|satisfied|delighted). Output STRICT JSON only: {\"score\": int, \"emotion\": string, \"reason\": string}.\n\nTranscript:\n${TRANSCRIPT_TEXT}"
  }]
}
EOF
) | jq -r '.content[0].text' | jq .
```

Free and surprisingly accurate. Use for backfilling history when paid budgets are missing.

### Recipe 4: Bulk-score last 7 days of closed tickets

```bash
# 1. Pull closed tickets from platform
curl -sS "https://api.intercom.io/conversations/search" \
  -H "Authorization: Bearer $INTERCOM_TOKEN" -H "Intercom-Version: 2.13" \
  -d '{"query":{"operator":"AND","value":[
    {"field":"state","operator":"=","value":"closed"},
    {"field":"updated_at","operator":">","value":1748390400}
  ]}}' | jq -r '.conversations[].id' > closed.txt

# 2. For each, score + write to warehouse
while read id; do
  SCORE=$(score_transcript "$id")  # uses Recipe 1/2/3
  psql -c "INSERT INTO support.sentiment_scores (ticket_id, score, emotion, scored_at, source) VALUES ('$id', $SCORE_VAL, '$EMOTION', NOW(), '$SOURCE') ON CONFLICT (ticket_id) DO UPDATE SET score = EXCLUDED.score;"
done < closed.txt
```

Idempotent. Cron weekly.

### Recipe 5: Weekly cohort report (warehouse query)

```sql
-- Run via postgresql-mcp
WITH weekly AS (
  SELECT
    DATE_TRUNC('week', scored_at) AS week,
    AVG(score) AS avg_score,
    COUNT(*) AS n,
    SUM(CASE WHEN score <= 30 THEN 1 ELSE 0 END)::float / COUNT(*) AS pct_detractors,
    SUM(CASE WHEN score >= 80 THEN 1 ELSE 0 END)::float / COUNT(*) AS pct_promoters
  FROM support.sentiment_scores
  WHERE scored_at >= NOW() - INTERVAL '13 weeks'
  GROUP BY 1
  ORDER BY 1
)
SELECT
  week,
  ROUND(avg_score, 1) AS avg,
  n,
  ROUND(pct_detractors * 100, 1) AS detractor_pct,
  ROUND(pct_promoters * 100, 1) AS promoter_pct,
  ROUND((avg_score - LAG(avg_score) OVER (ORDER BY week)), 2) AS wow_delta
FROM weekly;
```

`wow_delta` < -10 = alert candidate (raw delta on 0-100 scale; the "20% drop" rule from `role.md` translates to ~-15 here).

### Recipe 6: Cohort drop alert

```bash
WOW_DELTA=$(psql -tA -c "SELECT ROUND(this.avg_score - prev.avg_score, 1) FROM (...)" )
if (( $(echo "$WOW_DELTA < -10" | bc -l) )); then
  mcp tool slack.chat_postMessage \
    --channel '#support-alerts' \
    --text "Sentiment cohort dropped ${WOW_DELTA} this week. See: <kb.brand.com/sentiment-runbook>."
fi
```

Wire to a daily cron.

### Recipe 7: Detractor auto-route to CSM

```sql
-- Find detractors from last 24h not yet routed
SELECT s.ticket_id, t.customer_email, s.score, s.emotion
FROM support.sentiment_scores s
JOIN support.tickets t ON s.ticket_id = t.id
LEFT JOIN support.csm_outreach c ON s.ticket_id = c.ticket_id
WHERE s.score <= 30
  AND s.scored_at >= NOW() - INTERVAL '24 hours'
  AND c.ticket_id IS NULL;
```

For each row: ping CSM via `slack-mcp` + log into `support.csm_outreach` (idempotent).

### Recipe 8: Cross-reference sentiment with releases

```sql
WITH releases AS (
  SELECT release_at, version FROM product.releases WHERE released_at >= NOW() - INTERVAL '90 days'
),
sentiment_by_day AS (
  SELECT DATE_TRUNC('day', scored_at) AS day, AVG(score) AS avg_score
  FROM support.sentiment_scores
  WHERE scored_at >= NOW() - INTERVAL '90 days'
  GROUP BY 1
)
SELECT
  r.release_at,
  r.version,
  ROUND(AVG(s_before.avg_score), 1) AS avg_before_3d,
  ROUND(AVG(s_after.avg_score), 1) AS avg_after_3d,
  ROUND(AVG(s_after.avg_score) - AVG(s_before.avg_score), 1) AS delta
FROM releases r
LEFT JOIN sentiment_by_day s_before ON s_before.day BETWEEN r.release_at - INTERVAL '3 days' AND r.release_at
LEFT JOIN sentiment_by_day s_after ON s_after.day BETWEEN r.release_at AND r.release_at + INTERVAL '3 days'
GROUP BY 1, 2
HAVING ABS(AVG(s_after.avg_score) - AVG(s_before.avg_score)) >= 8;
```

Surfaces releases that materially shifted sentiment.

### Recipe 9: Per-agent sentiment (QA-style)

```sql
SELECT
  t.assignee_id,
  t.assignee_name,
  COUNT(*) AS tickets,
  ROUND(AVG(s.score), 1) AS avg_sentiment,
  SUM(CASE WHEN s.score >= 80 THEN 1 ELSE 0 END) AS promoter_count
FROM support.sentiment_scores s
JOIN support.tickets t ON s.ticket_id = t.id
WHERE s.scored_at >= NOW() - INTERVAL '30 days'
GROUP BY 1, 2
ORDER BY avg_sentiment DESC;
```

Use sparingly — sentiment-per-agent can become a punishing KPI if not contextualized (some agents own harder ticket pools).

### Recipe 10: Topic-level sentiment

```sql
SELECT
  topic_tag,
  COUNT(*) AS n,
  ROUND(AVG(score), 1) AS avg_sentiment
FROM support.sentiment_scores s
JOIN support.ticket_tags t ON s.ticket_id = t.ticket_id
WHERE s.scored_at >= NOW() - INTERVAL '30 days'
  AND topic_tag LIKE 'topic-%'
GROUP BY topic_tag
ORDER BY avg_sentiment ASC LIMIT 10;
```

Worst-sentiment topics → priority for KB / product fixes.

### Recipe 11: Webhook-driven real-time scoring

```bash
# On conversation.closed webhook from Intercom / Zendesk:
# 1. Verify signature
# 2. Pull transcript
# 3. Score via Loris/Klaus/Claude (pick whichever's configured)
# 4. UPSERT into support.sentiment_scores
# 5. If score <= 30 -> trigger Recipe 7 detractor flow
```

Closing-time scoring is more meaningful than daily batch — recency matters.

### Recipe 12: Backfill historical sentiment

```python
# Process 90 days of historical Intercom conversations in batches of 100
import os, requests, time

def page():
    cursor = None
    while True:
        body = {"query":{"operator":"AND","value":[{"field":"updated_at","operator":">","value":int(time.time()) - 90*86400}]},"pagination":{"per_page":100}}
        if cursor: body['pagination']['starting_after'] = cursor
        r = requests.post("https://api.intercom.io/conversations/search", json=body, headers={
            "Authorization":f"Bearer {os.environ['INTERCOM_TOKEN']}", "Intercom-Version":"2.13"})
        data = r.json()
        for c in data['conversations']:
            yield c['id']
        cursor = data.get('pages', {}).get('next', {}).get('starting_after')
        if not cursor: break

for cid in page():
    score_and_upsert(cid)  # Recipe 3 + INSERT
```

Run once on backfill; afterwards Recipe 11 keeps current.

## Examples

### Example 1: Daily cohort report

**Goal:** Daily snapshot of cohort sentiment trend.

**Steps:**
1. Run Recipe 5 (weekly cohort SQL).
2. Compute current-week vs previous-week delta.
3. If delta < -10 (Recipe 6), alert in `#support-alerts`.
4. Format markdown digest of top-5 worst-sentiment topics (Recipe 10).
5. Email support-lead via `gmail-mcp`.

**Result:** Lead sees the trend + the topics driving it in 5 lines.

### Example 2: Release-sensitive regression detection

**Goal:** Confirm whether last week's release shifted sentiment.

**Steps:**
1. Run Recipe 8 — get pre / post release deltas.
2. For releases with delta < -8, pull the worst-affected topics by joining sentiment + tags by date.
3. If a topic shows up sharply (e.g., `topic-checkout` post-`v4.12.0`), open a Linear `support-flagged-regression` issue (use the `bug-report-normalization-linear` skill).

**Result:** Sentiment becomes leading indicator of regressions in addition to Sentry crash counts.

## Edge cases / gotchas

- **Loris is contact-sales only** — no self-serve. Onboarding takes 2-4 weeks; budget accordingly.
- **Klaus's `auto-qa` requires the Zendesk-QA Pro bundle** — basic Klaus doesn't have the API; UI-only.
- **Claude fallback drift** — re-prompt to JSON every call; LLMs drift on output format without explicit "STRICT JSON only" instruction.
- **Sentiment != satisfaction** — sentiment scores conversation mood; CSAT scores resolution quality. Don't conflate. Use both for the full picture.
- **Mid-conversation sentiment swings** — opening message may be angry, closing may be happy. Loris / Klaus track aggregate; Claude prompt can specify "weight closing message higher."
- **Multilingual coverage** — Loris supports 24 languages; Claude supports 100+. For deep multilingual, prefer Claude.
- **Don't surface per-agent scores publicly** — sentiment as a punishing KPI degrades agent behavior (over-apologetic, performative). Use as a coaching signal only.
- **Detractor false positives** — sometimes the customer is just venting before they accept the resolution. Look at `resolution_status` (Loris) or score the closing message separately.
- **Warehouse schema cost** — `support.sentiment_scores` should index on `ticket_id` (UPSERT primary key) and `scored_at` (date queries). Without indexes, weekly cohort queries scan the entire table.
- **GDPR / data residency** — feeding transcripts to Loris (US-hosted) may violate EU data residency commitments. Confirm region pinning.

## Sources

- [Loris.ai (Conversation Intelligence)](https://loris.ai/)
- [Loris integrations](https://loris.ai/integrations/)
- [Klaus / Zendesk QA API](https://klausapp.com/api)
- [Best AI sentiment analysis tools 2026](https://www.cloudtalk.io/blog/ai-sentiment-analysis-tool/)
- [AssemblyAI sentiment introduction (for free transcription path)](https://www.assemblyai.com/blog/introducing-sentiment-analysis)
- [Anthropic Messages API](https://docs.anthropic.com/en/api/messages)
