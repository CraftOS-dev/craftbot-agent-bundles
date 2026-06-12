<!--
Source: https://www.qwoted.com/connectively-haro-is-going-away-heres-how-qwoted-can-help/
Backlinko HARO alternatives: https://backlinko.com/haro-alternatives
Featured.com: https://featured.com/
-->
# HARO / Qwoted / Featured / Source-of-Sources — SME Quotes — SKILL

Featured.com (revived HARO brand, April 2025) + Qwoted (highest reported conversion per 2026 backlinko data) + Source of Sources + #JournoRequest on X. Respond to journalist queries within the 4-hour relevance window. Subject: under 200 words, named expert + specific number + no promotion.

## When to use this skill

- **Daily SME pitch routing** — journalist publishes a query; you have a relevant exec/spokesperson with credibility.
- **Niche category authority building** — sustained presence on relevant queries builds brand association over months.
- **Cold media coverage path** — for outlets where direct pitching has zero traction, query response is the entry point.
- **Quote bank for SEO + AEO** — sourced quotes in articles become AI search citations.

**Do NOT use this skill when:**
- The query asks for a sponsored placement (it's an ad disguised as a query) — skip.
- The query is for a tier of expert you don't have (e.g., "PhD in oncology" and you don't) — don't fake it.
- The query is from an outlet you wouldn't want backlinking your brand — skip.

## Setup

### Featured.com (revived HARO)

```bash
# Free tier: daily email digest with queries
# Paid tier ($59-$249/mo): faster query alerts + filtered topics
# https://featured.com

# Set up subscriber profile
# 1. Topic categories: AI, SaaS, Marketing, Climate, etc.
# 2. Expert profile: name, title, brand, credentials
# 3. Daily digest delivery email (route to gmail-mcp filter)
```

Configure Gmail filter to label all Featured.com emails `Label: Featured-HARO` and auto-forward to triage script.

### Qwoted API

```bash
# Free tier: 5 queries/day; Pro: $59-$199/mo
export QWOTED_API_KEY="<key>"
export QWOTED_API_BASE="https://www.qwoted.com/api/v1"
```

Qwoted has the highest reported conversion rate among HARO alternatives — verified expert + journalist matching.

### Source of Sources

```bash
# Free, lower volume than Featured/Qwoted
# https://sourceofsources.com
# Daily email digest
```

### #JournoRequest on X via twitter-mcp

```bash
# Real-time stream
mcp tool twitter-mcp.search --query "#JournoRequest OR #PRrequest" \
  --since "1h" \
  --filter "lang:en"
```

### Notion query-response tracking DB

Per query response:
- `query_source` (select: Featured, Qwoted, SoS, #JournoRequest)
- `query_date` (date+time)
- `journalist` (text)
- `outlet` (text)
- `topic` (multi-select)
- `query_text` (rich text)
- `response_sent_at` (datetime)
- `response_time_hours` (number — calc)
- `response_body` (rich text)
- `spokesperson` (text — who from company)
- `outcome` (select: placed, no-reply, response-only, declined)
- `placement_url` (URL, if placed)

## Common recipes

### Recipe 1: Triage daily Featured.com digest

```bash
# Pull today's Featured digest from Gmail
gmail-mcp search --query "from:queries@featured.com newer_than:1d" --limit 1 \
| jq -r '.messages[0].body' \
> featured_digest.html

# Claude triages by topical relevance
prompt="Read this HARO/Featured digest. For each journalist query, output:
{
  query_id,
  journalist,
  outlet,
  topic_tags: [...],
  relevance_score: 1-10 (based on our SMEs in: AI infra, MarTech, SaaS sales, GTM, dev tools),
  deadline,
  query_text
}
Filter to relevance >= 7.
Output as JSON array."

candidates=$(claude --file featured_digest.html --prompt "$prompt")
echo "$candidates" | jq -c '.[]' | while read q; do
  notion-mcp create_page --db query_responses --properties "$q"
done
```

### Recipe 2: Qwoted query polling

```bash
# Poll every 30 min during business hours
curl "$QWOTED_API_BASE/queries?status=open&topic=ai,saas,marketing&limit=50" \
  -H "Authorization: Bearer $QWOTED_API_KEY" \
| jq '.queries[] | {id, journalist, outlet, topic, query_text, deadline, expertise_required}' \
> qwoted_open.json

# Match against SME bench
sme_bench=$(notion query "sme_bench")
for q in $(jq -c '.[]' qwoted_open.json); do
  match=$(claude --prompt "Does any expert in our bench match this query? $q vs $sme_bench. Output JSON: {match: bool, expert: name, match_reason: text}.")
  if [ "$(echo "$match" | jq -r .match)" = "true" ]; then
    # Queue for response
    notion-mcp create_page --db query_responses --properties "$q + $match"
  fi
done
```

### Recipe 3: 4-hour relevance window response

```python
# Triage queue: sort by deadline-proximity, respond within 4hr of query post

for q in notion.query(filter={"status": "queued"}):
    age_hours = (now - q['query_date']).total_seconds() / 3600
    if age_hours > 4:
        # Outside window; deprioritize
        notion.update(q['id'], status='deprioritized')
        continue

    # Generate response
    prompt = f"""
    Draft a 200-word SME response to this journalist query.

    QUERY: {q['query_text']}
    JOURNALIST: {q['journalist']} at {q['outlet']}
    OUR SPOKESPERSON: {sme['name']}, {sme['title']}, {company}
    SME BACKGROUND: {sme['background']}
    SME RELEVANT EXPERIENCE: {sme['relevant_creds']}

    REQUIREMENTS:
    - Direct answer in first 1-2 sentences (with a specific number or named example)
    - Supporting detail in 2-3 sentences (with brand-relevant proof point but NO pitch)
    - Background: name, title, brand, 1-line credibility
    - Available for follow-up: phone / email / LinkedIn

    Total: under 200 words.
    No fluff. No "I hope this helps." No promotion.
    """
    response = claude(prompt)

    # Send within window
    gmail_mcp.send(
        to=q['journalist_email'],
        subject=f"Re: {q['query_topic']} — quote from {sme['name']}",
        body=response
    )

    notion.update(q['id'],
        status='sent',
        response_sent_at=now(),
        response_time_hours=age_hours,
        spokesperson=sme['name']
    )
```

### Recipe 4: Response template (literal)

```markdown
Hi [Reporter],

Re: your question about [topic from query].

[Direct answer in 1-2 sentences with a specific number or named example.]

[Supporting detail in 2-3 sentences. Include a brand-relevant proof point — but don't pitch.]

Background: [Name], [Title at Brand]. [One line of credibility — years in field / customer count / prior coverage.]

Available for follow-up: [phone] / [email] / [LinkedIn].

Cheers,
[Name]
```

Total: under 200 words. Named expert + specific number + no promotion = highest accept rate.

### Recipe 5: #JournoRequest on X (twitter-mcp)

```bash
# Real-time stream
while true; do
  recent=$(mcp tool twitter-mcp.search \
    --query "#JournoRequest OR #JournoRequests" \
    --since "30m" \
    --limit 50 \
    --filter "lang:en AND -is:retweet")

  for tweet in $(echo "$recent" | jq -c '.tweets[]'); do
    text=$(echo "$tweet" | jq -r .text)
    author=$(echo "$tweet" | jq -r .author.username)
    tweet_id=$(echo "$tweet" | jq -r .id)

    # Check if topic matches our SME bench
    match=$(claude --prompt "Does our SME bench match this query? '$text'. Output JSON: {match: bool, expert: name}")

    if [ "$(echo "$match" | jq -r .match)" = "true" ]; then
      # Respond via reply (briefer than email)
      response="Hi @$author — happy to help. [Expert name], [title at brand]. [1-line direct answer with number]. DM for full quote or email me at press@acme.com."
      mcp tool twitter-mcp.reply --in_reply_to "$tweet_id" --text "$response"

      notion-mcp create_page --db query_responses --properties "{
        query_source: 'X-JournoRequest',
        journalist_handle: $author,
        tweet_id: $tweet_id,
        response_body: $response,
        response_sent_at: $(date -Iseconds)
      }"
    fi
  done

  sleep 1800 # 30 min
done
```

### Recipe 6: Source of Sources (free, lower volume)

```bash
# Subscribe to digest at https://sourceofsources.com
# Daily email; triage same as Featured (Recipe 1)
```

### Recipe 7: Conversion tracking per platform

```bash
# Weekly cron: pull all responses sent in last 30 days; check for placement
sent=$(notion query "query_responses WHERE response_sent_at > '$(date -d '30 days ago' -I)'")

for r in $sent; do
  journalist=$(echo "$r" | jq -r .journalist)
  outlet=$(echo "$r" | jq -r .outlet)

  # brave-search for byline + topic keyword
  results=$(brave-search "site:$outlet $journalist $topic_keywords" --since "30d")

  for result in $(echo "$results" | jq -c '.results[]'); do
    url=$(echo "$result" | jq -r .url)
    body=$(firecrawl scrape --url "$url" | jq -r .markdown)

    # Check if our SME is quoted
    if echo "$body" | grep -i "$sme_name"; then
      notion-mcp update_row --filter "id=$r" \
        --outcome "placed" \
        --placement_url "$url"
    fi
  done
done

# Compute conversion per platform
conversion=$(notion query "query_responses GROUP BY query_source AGGREGATE outcome=placed")
echo "$conversion"
```

### Recipe 8: SME bench in Notion

```yaml
sme_bench:
  - name: Jane Smith
    title: CEO
    expertise: AI infrastructure, SaaS pricing, GTM strategy
    available_topics: company building, AI policy, climate tech investment
    credentials: founder of Acme, ex-Google PM, MIT '15
    typical_response_time_hours: 2

  - name: Maria Lopez
    title: VP Engineering
    expertise: distributed systems, MLOps, dev tools
    available_topics: AI infra, technical hiring, engineering culture
    credentials: prev SRE Stripe, Stanford CS PhD
    typical_response_time_hours: 4

  - name: Sam Patel
    title: CMO
    expertise: B2B marketing, email deliverability, MPP measurement
    available_topics: martech trends, attribution, brand-vs-direct
    credentials: prev growth Stripe, Wharton MBA
    typical_response_time_hours: 1
```

Match queries against bench expertise tags. Route to fastest-responding SME for tight deadlines.

## Examples — daily SME workflow

```yaml
0700 ET:
  - Featured.com digest arrives in gmail
  - Source of Sources digest arrives in gmail
  - twitter-mcp #JournoRequest poll catches overnight queries

0700-0900:
  - claude triages all queries; ranks by relevance
  - top 10 candidates queued in notion

0900-1300:
  - SME (or PR lead) reviews queued queries
  - claude drafts responses for approved queries
  - human approves + edits each
  - gmail-mcp sends within 4-hour window

throughout_day:
  - twitter-mcp polls #JournoRequest every 30 min
  - real-time response for urgent (<2 hr deadline) queries

eod:
  - notion summary of queries triaged, responded, declined
  - weekly placement tracking cron checks for byline mentions

monthly:
  - per-platform conversion calculation
  - reallocate effort to highest-conversion platforms
  - update sme bench based on what topics convert
```

## Edge cases

### 4-hour window is real
After 4 hours from query post, response rate drops sharply. Journalists triage in the first 4 hours; later responses get skimmed or ignored.

### Named expert + specific number = key signal
Generic responses fail. Successful response pattern:
- Specific named expert (not "industry observers say")
- Specific number ("47% of our 200 customers" beats "the majority")
- Specific timeframe ("Q1 2026" beats "recently")
- Named brand involved (yours)

### Don't promote
HARO/Featured/Qwoted journalists hate pitches disguised as quotes. The query is "what's a trend in X?" — answer it. Don't pivot to "and our product solves it."

### Quality > quantity
Better to respond to 3 highly-relevant queries with strong SME match than 30 queries with stretch matches. Stretch matches damage future credibility.

### Verify journalist legitimacy
Featured + Qwoted verify journalists. Source of Sources less so. #JournoRequest = anyone can use it (scammers do). Before responding to unverified queries:
- Check journalist's outlet exists
- Check their byline on the outlet
- Skip if it's a "freelancer" with no past coverage on the topic

### Backlinks vs branded mentions
Some queries are link-building scams disguised as journalism — "give me a quote for my blog and I'll link your site." Generally low value. Skip unless the outlet is genuinely credible.

### SME availability tracking
Brief each SME on response time expectation:
- Tier-1 query → 1-hour SLA
- Tier-2 query → 4-hour SLA
- Tier-3 query → 24-hour SLA

Update Notion `sme_bench` with current availability (out of office, etc.).

### Topical drift detection
SME bench expertise expands over time. Quarterly: update each SME's `available_topics` based on what they've actually said yes to. Don't keep matching to topics they declined.

### Conversion benchmarks
Realistic conversion (response → published quote):
- Qwoted: 25-40%
- Featured.com: 15-25%
- Source of Sources: 10-15%
- #JournoRequest: 5-15%

If conversion drops below these, audit response quality.

### Outlet quality tier matters
Match query response volume to outlet tier:
- T1 query (NYT, WSJ, Bloomberg) → full attention, CEO response if applicable, 1-hour SLA
- T2 query (TechCrunch, trades) → standard response, VP-level SME, 4-hour SLA
- T3 query (niche blogs) → quick response, manager-level SME, 24-hour SLA
- T4 query (dubious) → skip

### Multiple SMEs responding to same query
Some platforms (Featured) allow multiple responses per query. If two SMEs at your company are both relevant, only ONE responds. Picking the right one matters more than two responses.

### Repurposing successful quotes
Track which quotes get published. Pull the article via `firecrawl-mcp`. Repurpose:
- LinkedIn post: "Quoted in [Outlet] on [topic]..."
- Twitter share with snippet
- Add to media kit for future pitches
- Feed quote text into AEO citation tracker

### Building SME track record
After 5-10 published quotes, SME builds credibility with journalists. Next outreach: name-drop prior publications ("Maria has been quoted in TechCrunch + The Verge on this topic before").

### When to escalate to direct pitch
If 3 queries from the same outlet/journalist get strong placement, that journalist becomes a warm lead. Move to `journalist-outreach-cold-warm-embargoed` skill — direct warm pitch with relationship signal.

## Sources

- **Qwoted (HARO transition)**: https://www.qwoted.com/connectively-haro-is-going-away-heres-how-qwoted-can-help/
- **Featured.com (revived HARO)**: https://featured.com/
- **Backlinko HARO alternatives 2026**: https://backlinko.com/haro-alternatives
- **Source of Sources**: https://sourceofsources.com/
- **#JournoRequest discovery**: https://twitter.com/search?q=%23JournoRequest
- **Qwoted API**: https://www.qwoted.com/api
- **Featured.com expert program**: https://featured.com/experts
