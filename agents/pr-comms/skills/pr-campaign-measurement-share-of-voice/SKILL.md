<!--
Source: https://brand24.com/blog/brand-monitoring-tools/
EMV methodology: https://bospar.com/how-to-master-award-submissions/
role.md outlet-tier rubric: internal
-->
# PR Campaign Measurement — Share of Voice + EMV + Outlet Tier — SKILL

Outlet-tier rubric (T1-T4) + EMV formula (`UVM × CPM × tier_multiplier × syndication_factor`) + share-of-voice (paid via Brand24/Brandwatch OR free via `brave-search` mention count). Sentiment overlay via Brand24 OR Claude per-article. Monthly client digest via `docx` PR report.

## When to use this skill

- **Monthly client report** — share-of-voice + tier-1 placement count + EMV + sentiment summary.
- **Campaign post-mortem** — measure ROI of a specific launch / awards win / crisis response.
- **Competitive benchmarking** — quarterly SoV vs 3-5 named competitors.
- **Budget justification** — defend PR budget with measurable outcomes.
- **Show client the AEO bonus** — earned coverage that also feeds AI search citations.

**Do NOT use this skill when:**
- The metric is paid-ad performance — defer to `marketing-agent`.
- The metric is customer-support CSAT — defer to `customer-support-agent`.
- The metric is investor disclosure (8-K coverage) — defer to `investor-relations`.

## Setup

### Outlet-tier rubric in Notion

```yaml
T1:  # 5x EMV multiplier
  - NYT (nytimes.com)
  - WSJ (wsj.com)
  - Bloomberg (bloomberg.com)
  - Reuters (reuters.com)
  - AP (apnews.com)
  - FT (ft.com)
  - The Economist (economist.com)
  - CNN (cnn.com)
  - CNBC (cnbc.com)
  - BBC (bbc.co.uk)
  - Forbes (forbes.com)
  - Fortune (fortune.com)

T2:  # 3x EMV multiplier
  - TechCrunch (techcrunch.com)
  - The Information (theinformation.com)
  - Axios (axios.com)
  - Marketing Brew (marketingbrew.com)
  - AdAge (adage.com)
  - Modern Healthcare (modernhealthcare.com)
  - Bisnow (bisnow.com)
  - Wired (wired.com)
  - The Verge (theverge.com)
  - NPR (npr.org)
  - USA Today (usatoday.com)

T3:  # 1.5x EMV multiplier
  - [niche blogs, regional press, syndicated reposts, podcasts under 10K downloads]

T4:  # 0.5x EMV multiplier
  - [self-published, owned media, syndication-only]
```

Maintain as Notion DB. Auto-tag placements by outlet domain.

### Brand24 / Brandwatch / Meltwater

(See `brand-reputation-monitoring-brandwatch-meltwater` skill for setup.)

### posthog-mcp (PR landing page conversion)

```bash
export POSTHOG_PROJECT_API_KEY="<key>"
export POSTHOG_API_BASE="https://app.posthog.com/api/projects/<id>"
```

Used to track press release landing page traffic + AEO referrer attribution.

### Notion coverage tracker DB

Per placement:
- `date` (date)
- `outlet` (text)
- `outlet_tier` (select)
- `headline` (text)
- `url` (URL)
- `journalist` (text)
- `uvm` (number — unique visitors/month from outlet media kit)
- `cpm` (number — outlet display CPM, default $30)
- `tier_multiplier` (number — auto from rubric)
- `syndication_factor` (number — 1.0 standalone, 0.3 syndicated)
- `emv` (formula = uvm × cpm × multiplier × syndication)
- `sentiment` (select: positive, neutral, negative, mixed)
- `quote_included` (checkbox)
- `customer_named` (text)
- `aeo_relevant` (checkbox — extractable quotes / structured)
- `campaign_tag` (multi-select)

## Common recipes

### Recipe 1: Auto-tag placements with tier

```python
# When placement is logged
def tag_tier(placement_url):
    domain = urlparse(placement_url).netloc.replace('www.', '')

    tier_rubric = notion.query(database='outlet_tier_rubric')
    for tier_row in tier_rubric:
        if domain in tier_row['domain']:
            return tier_row['tier']
    return 'T4'  # default

placement['outlet_tier'] = tag_tier(placement['url'])
placement['tier_multiplier'] = {'T1': 5, 'T2': 3, 'T3': 1.5, 'T4': 0.5}[placement['outlet_tier']]
```

### Recipe 2: EMV calculation per placement

```python
# UVM: pull from outlet media kit; fallback to SimilarWeb
def get_uvm(outlet_domain):
    # Notion override first
    override = notion.query(filter={'outlet_domain': outlet_domain})
    if override:
        return override[0]['uvm']

    # SimilarWeb fallback
    sw_resp = requests.get(
      f"https://api.similarweb.com/v1/website/{outlet_domain}/total-traffic-and-engagement/visits",
      headers={'X-API-Key': SIMILARWEB_KEY},
      params={'start_date': '2026-04', 'end_date': '2026-06', 'granularity': 'monthly'}
    )
    return sw_resp.json()['visits'][-1]

# CPM: outlet's published display rate or industry average
CPM_DEFAULT = 30  # $30 USD per 1000 impressions
def get_cpm(outlet_domain):
    return notion.query(filter={'outlet_domain': outlet_domain})[0].get('cpm', CPM_DEFAULT)

# Syndication: is this a primary or syndicated copy?
def get_syndication_factor(placement_url, headline):
    # Check if 3+ other URLs have near-identical headline within 24h
    candidates = brave_search(f'"{headline}"', since='24h')
    if len(candidates) > 3:
        return 0.3  # syndicated copy
    return 1.0

# Final EMV
emv = uvm * (cpm / 1000) * tier_multiplier * syndication_factor
```

### Recipe 3: Share of voice — paid path

```bash
# Brand24
curl "$BRAND24_API_BASE/projects/$BRAND24_PROJECT_ID/share-of-voice?\
period=last_30_days&\
competitors=$COMP_1,$COMP_2,$COMP_3,$COMP_4" \
  -H "Authorization: Bearer $BRAND24_TOKEN" \
| jq '{
    your_share: .brand.share_pct,
    competitor_shares: .competitors,
    wow_delta: .wow_delta_pct
  }'

# Brandwatch (more granular)
curl "$BRANDWATCH_API_BASE/projects/$BRANDWATCH_PROJECT_ID/share-of-voice?\
period=last_30_days&\
queries=brand,$COMP_1,$COMP_2,$COMP_3" \
  -u "$BRANDWATCH_USERNAME:$BRANDWATCH_API_KEY"
```

### Recipe 4: Share of voice — free fallback

```python
window = 'past_30_days'
brands = ['Acme Corp', 'Competitor A', 'Competitor B', 'Competitor C']

mention_counts = {}
for b in brands:
    # News
    news_results = brave_search(b, since=window, type='news')
    news_count = len(news_results['results'])

    # Reddit
    reddit_results = reddit_mcp.search(query=b, since=window)
    reddit_count = len(reddit_results['posts'])

    # Twitter
    tw_results = twitter_mcp.search(query=f'"{b}" -is:retweet', since=window, limit=500)
    tw_count = len(tw_results['tweets'])

    mention_counts[b] = news_count + reddit_count + tw_count

total = sum(mention_counts.values())
sov = {b: count / total for b, count in mention_counts.items()}
print(f"Acme Corp SoV: {sov['Acme Corp']:.2%}")
```

### Recipe 5: Sentiment aggregation

```python
# Per placement, classify sentiment via Claude (free path)
placements = notion.query(filter={'date': {'after': 30_days_ago}})

for p in placements:
    if p['sentiment']:
        continue  # already classified

    body = firecrawl.scrape(p['url'])['markdown']
    sentiment = claude(f"""
    Classify sentiment toward Acme Corp in this article.

    ARTICLE: {body[:3000]}

    Output JSON: {{
      sentiment: positive/neutral/negative/mixed,
      confidence: 0-1,
      key_phrases: ["..."]
    }}
    """)

    notion.update(p['id'], sentiment=sentiment['sentiment'])

# Aggregate
sentiment_breakdown = {
    'positive': sum(1 for p in placements if p['sentiment'] == 'positive'),
    'neutral': sum(1 for p in placements if p['sentiment'] == 'neutral'),
    'negative': sum(1 for p in placements if p['sentiment'] == 'negative'),
    'mixed': sum(1 for p in placements if p['sentiment'] == 'mixed'),
}
print(sentiment_breakdown)
```

### Recipe 6: Monthly client digest (docx)

```python
import datetime
from docx_skill import render_docx

month_start = datetime.date.today().replace(day=1) - datetime.timedelta(days=30)
month_end = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)

placements = notion.query(filter={
    'date': {'between': [month_start, month_end]}
})

# Aggregations
total_placements = len(placements)
tier_breakdown = {
    'T1': sum(1 for p in placements if p['outlet_tier'] == 'T1'),
    'T2': sum(1 for p in placements if p['outlet_tier'] == 'T2'),
    'T3': sum(1 for p in placements if p['outlet_tier'] == 'T3'),
    'T4': sum(1 for p in placements if p['outlet_tier'] == 'T4'),
}
total_emv = sum(p['emv'] for p in placements)
sov = calc_share_of_voice(window='30d')
sentiment = calc_sentiment(placements)

# Top 5 placements by EMV
top5 = sorted(placements, key=lambda p: p['emv'], reverse=True)[:5]

# AEO-relevant placements (extractable quotes)
aeo_relevant = [p for p in placements if p['aeo_relevant']]

report = render_docx(
    template='monthly_pr_report.docx',
    output=f'reports/PR_report_{month_start.strftime("%Y_%m")}.docx',
    data={
        'period': f"{month_start.strftime('%b %Y')}",
        'total_placements': total_placements,
        'tier_breakdown': tier_breakdown,
        'total_emv': f"${total_emv:,.0f}",
        'sov': sov,
        'sentiment': sentiment,
        'top5_placements': top5,
        'aeo_relevant_count': len(aeo_relevant),
        'campaign_summaries': summarize_campaigns(placements),
    }
)

gmail_mcp.send(
    to=CLIENT_EMAIL,
    subject=f"Acme PR monthly report — {month_start.strftime('%B %Y')}",
    body="Monthly PR performance attached. Key wins: ...",
    attachments=[report]
)
```

### Recipe 7: Campaign-tagged measurement

```python
# Tag placements with campaign at time of logging
campaigns = {
    'series_b_announcement': '2026-06-11 to 2026-06-25',
    'aeo_thought_leadership_q2': '2026-04-01 to 2026-06-30',
    'inc5000_press': '2026-08-10 to 2026-08-24',
}

# Per campaign retrospective
for campaign, dates in campaigns.items():
    start, end = parse_dates(dates)
    placements = notion.query(filter={
        'campaign_tag': campaign,
        'date': {'between': [start, end]}
    })

    print(f"\n=== {campaign} ===")
    print(f"Total placements: {len(placements)}")
    print(f"Tier-1: {sum(1 for p in placements if p['outlet_tier'] == 'T1')}")
    print(f"Total EMV: ${sum(p['emv'] for p in placements):,.0f}")
    print(f"AEO-relevant: {sum(1 for p in placements if p['aeo_relevant'])}")
```

### Recipe 8: posthog-mcp PR landing page conversion

```bash
# Track conversion from press release landing page
posthog-mcp query --filter "url contains '/press/series-b-2026'" \
| jq '{
    unique_visitors: .stats.unique_visitors,
    time_on_page_sec: .stats.avg_time_on_page,
    scroll_depth_pct: .stats.scroll_depth,
    demo_signups: .conversions.demo_signups,
    contact_form: .conversions.contact_form
  }'

# AEO referrer attribution
posthog-mcp query --filter "url contains '/press/series-b-2026' AND referrer contains 'chatgpt|gemini|perplexity'" \
| jq '.stats.referrer_breakdown'
```

## Examples — monthly measurement workflow

```yaml
day_1_of_month:
  - close prior month's data
  - run all aggregations (recipes 1-7)
  - top 5 EMV placements identified
  - sentiment breakdown calculated
  - share of voice vs competitors

day_2:
  - draft client report (docx)
  - claude-augmented narrative (highlights + lowlights)
  - human review

day_3:
  - finalize + send to client

day_5:
  - 30-min client call walking through report
  - identify focus areas for next month

day_15:
  - mid-month check-in (placements pacing)
  - adjust pitch list if needed

ongoing:
  - real-time placement logging in Notion
  - sentiment classification within 24hr of placement
  - tier auto-tag on log
  - emv calc on log
  - campaign tag at log time
```

## Edge cases

### EMV is directional, not financial
EMV approximates what an equivalent paid-ad spend would cost. It's NOT audited financial value. Don't pitch as ROI dollars to CFO. Pair with: tier-1 placement count, share of voice, qualitative sentiment, sales pipeline impact.

### Syndication double-counting
Wire releases spawn 50-200 syndicated copies. Don't count each as a separate placement. Use:
- Primary placement: full EMV
- Syndicated copy: 0.3 multiplier
- Pure repost (headline only): 0.1 or exclude

Dedupe via canonical URL or headline+first-paragraph match.

### Sentiment classifier accuracy
Claude sentiment classification works on ~85% of clear cases. For B2C with high sarcasm (memes, ironic tweets), Brandwatch sarcasm detection is the differentiator. For B2B, Claude is sufficient.

### CPM defaults vary by outlet
Tier-1 outlets publish CPM rates of $30-$80. Tier-2 trades $15-$40. Tier-3 niche $5-$25. Use:
- Outlet's published CPM if available
- Industry average $30 as default
- Don't inflate to justify EMV

### Tier rubric maintenance
Outlets shift over time (a tier-2 trade becomes tier-1 in its category). Annual rubric review:
- Add new outlets that emerged
- Move outlets up/down based on reach + credibility shift
- Remove dead outlets

### What counts as a "placement"
Strict: byline in a news article with named coverage of company/product.
Liberal: any mention in any article (even passing).

Be consistent. Pick one, document, stick with it. Strict is better for tier-1 reporting; liberal inflates volume but dilutes signal.

### Hand-off to AEO measurement
AEO-relevant placements (extractable quotes + named source + specific number) feed into the AEO citation tracker. Tag at placement time. Pair with `posthog-mcp` referrer tracking for AI search engine → company site attribution.

### Customer-named placements
Placements that name a customer = customer-reference value. Track separately:
- Pre-clear customer mention (via `customer-reference-program-pr`)
- Tag in Notion `customer_named` field
- Higher EMV multiplier (customers in articles convert better)

### Negative coverage = still tracked
A negative tier-1 placement is reach (eyeballs on brand), but EMV calc should incorporate sentiment:
- Positive: full EMV
- Neutral: full EMV
- Mixed: 0.7 EMV
- Negative: 0.3 EMV or report separately (don't aggregate with positive)

### Sales pipeline overlay
If sales tags inbound to source channels (HubSpot/Salesforce), join PR placements to pipeline:
- Demo signups within 7 days of T1 placement
- Pipeline created within 14 days
- Revenue from sources tagged "PR"

Pair with `hubspot-crm-marketing-mcp` skill (marketing-agent) for join.

### Reporting cadence
- Monthly: detailed digest (this recipe)
- Quarterly: trend + campaign retrospective
- Annual: full PR program ROI

Don't overload monthly reports with annual-trend graphs. Keep tactical for monthly.

### Visual report quality
Use `pdf` skill or `pptx` skill for client-facing reports. Branded template via `canva-mcp` or `figma-mcp`. Charts via Python matplotlib → embed.

### What clients actually care about
Behind the metrics:
- Tier-1 placement count (most valued)
- Share of voice vs competitors (board-level metric)
- Customer mentions in coverage
- AEO citation share (newer metric, growing important)
- Sentiment trend

EMV is a useful framing but not the headline. Lead with placement count + SoV.

## Sources

- **Brand24 SoV methodology**: https://brand24.com/blog/brand-monitoring-tools/
- **EMV industry framing**: https://bospar.com/how-to-master-award-submissions/
- **Outlet tier rubric (industry standard)**: internal role.md
- **SimilarWeb API (for UVM lookup)**: https://developers.similarweb.com/
- **PostHog landing page analytics**: https://posthog.com/docs/api
- **Brandwatch SoV**: https://www.brandwatch.com/p/share-of-voice/
- **Meltwater PR measurement**: https://www.meltwater.com/en/pr-measurement
