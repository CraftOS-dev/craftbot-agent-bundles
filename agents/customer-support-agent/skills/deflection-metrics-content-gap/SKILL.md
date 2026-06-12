<!--
Source: https://docs.kapa.ai/integrations/support-form-deflector/deflection-rates
-->
# Deflection Metrics + Content Gap Audit — SKILL

Combines Kapa.ai (or Inkeep / Markprompt) deflection analytics with a cross-reference against Notion KB content. Output: top-asked-with-no-coverage (content gaps → new articles) plus top-answered-but-still-escalates (article-quality gaps → rewrites).

## When to use

- **Weekly content-gap audit** — top zero-result queries → KB drafts.
- **Quarterly deflection-rate review** — am I deflecting more this quarter than last?
- **Pre-rewrite analysis** — surface articles with high citations + low helpfulness (rewrite candidates).
- **Cross-platform consistency** — find topics that Kapa cites docs A but ticket cluster suggests answer is in docs B.

This skill is a higher-level workflow over the `kapa-ai-doc-qa` and `notion-knowledge-base-management` skills.

Trigger phrases: "content gap audit", "deflection rate", "top unanswered questions", "weekly KB drift report", "what should we write next".

## Setup

```bash
# Inherits Kapa + Notion + Postgres setup from sibling skill packs
```

Auth + env: inherits `KAPA_API_KEY`, `NOTION_TOKEN`, `KB_DB_ID`, `postgresql-mcp` connection.

Prerequisites:
- `support.deflection_metrics` warehouse table: `(date, total_queries, deflected, escalated, deflection_rate)`.
- Notion KB DB with `Title`, `Status`, `Last Reviewed`, `Source Tickets`.

## Common recipes

### Recipe 1: Pull current deflection rate

```bash
curl -sS "https://api.kapa.ai/analytics/v1/projects/$KAPA_PROJECT_ID/deflection?period=30d" \
  -H "X-API-Key: $KAPA_API_KEY" | jq '{
    total_queries: .total_queries,
    deflected: .deflected_count,
    escalated: .escalation_count,
    rate: .deflection_rate
  }'
```

Benchmark: mature SaaS targets 40-55% deflection rate. Below 30% = either docs are poor or Kapa setup is incomplete.

### Recipe 2: Top zero-result queries (no KB answers)

```bash
curl -sS "https://api.kapa.ai/analytics/v1/projects/$KAPA_PROJECT_ID/queries/unanswered?period=30d&limit=20" \
  -H "X-API-Key: $KAPA_API_KEY" | jq '.queries[] | {query, count, last_asked_at}' > zero-result.json
```

These are the highest-leverage articles to write.

### Recipe 3: Top low-confidence answers (article exists but unclear)

```bash
curl -sS "https://api.kapa.ai/analytics/v1/projects/$KAPA_PROJECT_ID/queries/low-confidence?period=30d&threshold=0.6&limit=20" \
  -H "X-API-Key: $KAPA_API_KEY" | jq '.queries[] | {query, confidence, top_source}' > low-conf.json
```

These are rewrite candidates — readers can find an article but can't follow it.

### Recipe 4: Cross-reference zero-result with Notion KB

```bash
jq -c '.[]' zero-result.json | while read q; do
  QUERY=$(echo "$q" | jq -r '.query')
  COUNT=$(echo "$q" | jq -r '.count')

  # Search Notion KB
  HITS=$(curl -sS -X POST "https://api.notion.com/v1/search" \
    -H "Authorization: Bearer $NOTION_TOKEN" \
    -H "Notion-Version: 2022-06-28" \
    -d "{\"query\":\"$QUERY\",\"filter\":{\"property\":\"object\",\"value\":\"page\"}}" \
    | jq '.results | length')

  if [ "$HITS" -eq 0 ]; then
    echo "GAP: $QUERY ($COUNT asks)" >> content-gaps.txt
  else
    echo "EXISTS-BUT-FAILING: $QUERY ($COUNT asks, $HITS Notion hits)" >> rewrite-candidates.txt
  fi
done
```

Differentiates true gaps (no article exists) from quality gaps (article exists but Kapa doesn't surface it).

### Recipe 5: Cross-reference with ticket clusters

```sql
-- Top topic clusters from last 30 days (from your sentiment + tags warehouse)
SELECT topic_tag, COUNT(*) AS volume
FROM support.tickets
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY topic_tag
ORDER BY volume DESC LIMIT 20;
```

Compare against KB articles tagged with the same topic. Topics with high volume + low article count = priority.

### Recipe 6: Highest-citation, lowest-helpfulness articles

```bash
curl -sS "https://api.kapa.ai/analytics/v1/projects/$KAPA_PROJECT_ID/sources/usage?period=30d" \
  -H "X-API-Key: $KAPA_API_KEY" \
  | jq '[.[] | select(.citation_count > 50 and .helpfulness_rate < 0.5)] | sort_by(.citation_count) | reverse | .[] | {url, citations: .citation_count, helpful: .helpfulness_rate}'
```

These articles are seen by users but failing them. Rewrite priorities.

### Recipe 7: Deflection-rate trend (12 weeks)

```sql
SELECT
  DATE_TRUNC('week', date) AS week,
  AVG(deflection_rate) AS avg_rate
FROM support.deflection_metrics
WHERE date >= NOW() - INTERVAL '12 weeks'
GROUP BY 1 ORDER BY 1;
```

Negative trend = content quality decay or AI degradation. Investigate.

### Recipe 8: Weekly content-gap digest (Markdown)

```markdown
# Content Gap Audit — Week of {{date}}

## Deflection rate
- This week: 47.3% (n=2,143 queries)
- Last week: 49.8%
- Trend: ⬇ -2.5pp (escalation up)

## Top gaps (no article yet)
1. "How do I rotate the API key?" — 18 asks
2. "Webhook retry policy?" — 12 asks
3. "Why was my refund denied?" — 9 asks

## Top rewrite candidates (article exists, Kapa low-confidence)
1. "SSO Okta setup" — 47 asks, 0.42 confidence (current article: KB-123)
2. "Plan downgrade flow" — 32 asks, 0.49 confidence (current article: KB-456)

## Recommended actions
- [ ] Draft "How to rotate the API key" (owner: @docs)
- [ ] Rewrite KB-123 SSO Okta setup (owner: @docs)
- [ ] Review KB-456 plan downgrade (owner: @docs)
```

Generate via `cli-anything python` + the queries above; deliver via `gmail-mcp`.

### Recipe 9: Auto-draft new KB article from a gap

```bash
# For each top gap, hand off to Claude for a first draft
QUERY="How do I rotate the API key?"
PROMPT="You are a technical writer. Draft a KB article answering this question: $QUERY.
Use the KB article template:
- Title (concrete user query)
- TL;DR (≤50 words)
- Detailed walkthrough
- Common errors

Use first-principles knowledge of a typical SaaS API. Mark unknowns with [TODO]."

claude_response=$(curl -sS https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"claude-sonnet-4-5-20250929\",\"max_tokens\":2000,\"messages\":[{\"role\":\"user\",\"content\":\"$PROMPT\"}]}" \
  | jq -r '.content[0].text')

# Push to Notion KB DB as Draft
curl -sS -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -d "{\"parent\":{\"database_id\":\"$KB_DB_ID\"},\"properties\":{\"Title\":{\"title\":[{\"text\":{\"content\":\"$QUERY\"}}]},\"Status\":{\"status\":{\"name\":\"Draft\"}}},\"children\":[{\"object\":\"block\",\"type\":\"paragraph\",\"paragraph\":{\"rich_text\":[{\"text\":{\"content\":\"$claude_response\"}}]}}]}"
```

Hand off to `technical-writer` agent for human-quality polish.

### Recipe 10: Track rewrite outcomes

```sql
-- Did the rewrite improve confidence?
SELECT
  source_url,
  AVG(confidence) FILTER (WHERE date < '2026-06-01') AS confidence_before,
  AVG(confidence) FILTER (WHERE date >= '2026-06-01') AS confidence_after
FROM kapa.query_log
WHERE source_url IN (SELECT url FROM kb.rewritten_articles WHERE rewrite_date = '2026-06-01')
GROUP BY 1;
```

If confidence didn't move post-rewrite → the rewrite missed the mark. Retry.

### Recipe 11: Tag content gaps in Notion review DB

```bash
# Create a "Content Gap" entry per gap, with owner + due date
curl -sS -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "parent":{"database_id":"'$GAPS_DB_ID'"},
    "properties":{
      "Query":{"title":[{"text":{"content":"How do I rotate the API key?"}}]},
      "Ask Count":{"number":18},
      "Status":{"status":{"name":"Draft Needed"}},
      "Owner":{"people":[{"id":"$DOCS_USER_ID"}]},
      "Due":{"date":{"start":"2026-06-16"}}
    }
  }'
```

Treats content debt as managed work, not implicit.

### Recipe 12: Deflection rate by topic

```sql
-- Are some topics easier to deflect than others?
SELECT
  topic_tag,
  COUNT(*) FILTER (WHERE deflected) AS deflected,
  COUNT(*) FILTER (WHERE NOT deflected) AS escalated,
  ROUND(100.0 * COUNT(*) FILTER (WHERE deflected) / COUNT(*), 1) AS rate
FROM kapa.query_log
WHERE date >= NOW() - INTERVAL '30 days'
GROUP BY topic_tag
ORDER BY rate ASC LIMIT 10;
```

Lowest-rate topics need either (a) better docs or (b) human-required (e.g., billing disputes).

## Examples

### Example 1: Weekly Monday morning audit

**Goal:** Stand up a recurring content-gap workflow.

**Steps:**
1. 06:00 UTC Monday: Cron runs Recipes 1, 2, 3 → JSON outputs.
2. Recipe 4: Cross-reference with Notion KB.
3. Recipe 8: Format Markdown digest.
4. `gmail-mcp send_email` to docs team @ 08:00 UTC.
5. For top 3 gaps: Recipe 11 creates Notion review tickets.
6. For top 2 rewrites: tag the existing article with "needs-rewrite" status.

**Result:** Predictable weekly cadence; gaps become managed work.

### Example 2: Pre-quarterly deflection-rate review

**Goal:** Surface why deflection dropped quarter-over-quarter.

**Steps:**
1. Recipe 7: pull 12-week trend, confirm material drop.
2. Recipe 12: split deflection by topic; which topic dropped?
3. For the worst topic, run Recipe 5 ticket-cluster cross-reference + Recipe 6 article-quality check.
4. Output narrative: "Deflection dropped on `topic-billing` because article KB-456 hasn't been updated since the new plan structure rolled out."
5. Recommended fix attached.

**Result:** Quarterly deflection numbers connected to specific content actions, not vague "AI quality" hand-waves.

## Edge cases / gotchas

- **Kapa metrics lag 24h** — `period=30d` doesn't include today. Account for this when alerting.
- **Article URLs change** — Notion-published article URLs change if you rename the page. Maintain a URL alias / redirect table.
- **Notion search false negatives** — Notion search is fuzzy and inconsistent. Recipe 4 may flag a gap when an article exists with a slightly different title. Manually verify before drafting.
- **Topic tagging schema must be consistent** — `topic-billing` vs `Billing` vs `topic: billing` will fragment metrics. Pick one (the Notion + ESP-tag canonical) and enforce.
- **Deflection != resolution** — Kapa deflection counts "user didn't escalate after seeing the answer." If the user gave up rather than escalated, that's still counted as deflection. Cross-check with downstream CSAT / churn.
- **Article-quality gaps can be in the indexer, not the article** — Kapa low-confidence might mean the indexer didn't ingest the article well, not that the article is bad. Re-index before rewriting.
- **Drafts from Claude need human review** — Recipe 9 produces a first draft. Don't auto-publish.
- **Owner-less work decays** — if "Owner" on Notion gap entries isn't filled, the work doesn't happen. Always assign.
- **Don't measure tools by deflection rate alone** — a 90% deflection rate with bad answers is worse than 50% with good answers. Pair with CSAT on Kapa-resolved sessions.
- **Quarterly review fatigue** — auto-generate the digest, but keep human review weekly. Don't outsource judgment.

## Sources

- [Kapa.ai deflection rates docs](https://docs.kapa.ai/integrations/support-form-deflector/deflection-rates)
- [Kapa Analytics dashboard](https://docs.kapa.ai/analytics/dashboard)
- [Kapa support-form deflector FAQ](https://docs.kapa.ai/integrations/support-form-deflector/faq)
- [Notion API search](https://developers.notion.com/reference/post-search)
- [Kapa enterprise alternatives review (PixieBrix)](https://www.pixiebrix.com/tool/kapa-ai)
