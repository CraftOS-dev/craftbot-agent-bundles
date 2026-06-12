<!--
Source: https://athenahq.ai/ + https://nicklafferty.com/blog/profound-vs-athena/
AthenaHQ + Profound API — AI search citation tracking
-->
# AEO / GEO AI Search Tracking — SKILL

AEO (Answer Engine Optimization) and GEO (Generative Engine Optimization) tracking measures brand citation share across AI search surfaces — ChatGPT, Gemini, Claude, Perplexity. AthenaHQ and Profound both offer real-time tracking with 5-min SLA. Profound has a public API; AthenaHQ has dashboard + paid API access.

## When to use this skill

- **AI search visibility audit** — does the brand show up in AI Overviews / ChatGPT answers?
- **Citation share monitoring** — % of relevant prompts that cite the brand.
- **Competitive AI visibility** — share-of-voice vs competitors in AI surfaces.
- **AEO content strategy** — which content patterns get cited (structured data, FAQ format, listicles).
- **GEO copy optimization** — direct-quote-friendly chunks for retrieval.
- **Prompt monitoring** — track 100s of brand-relevant prompts daily.

**Do NOT use this skill when:**
- **Traditional SEO ranking** — use Ahrefs / GSC skills.
- **Internal RAG / vector search tuning** — separate domain.

## Setup

### Profound API

```bash
# Sign up at https://tryprofound.com
# Generate API key in dashboard
export PROFOUND_API_KEY="<key>"
```

### AthenaHQ API

```bash
# Sign up at https://athenahq.ai
# API access on Growth plan and up
export ATHENA_API_KEY="<key>"
```

### Brand identity setup

Both tools track per-brand. Set up:
- Brand name (canonical)
- Brand domain
- Aliases / misspellings
- Competitor list (5-10 names)
- Topic prompts to monitor (50-500 prompts)

## Common recipes

### Recipe 1: Citation share daily snapshot (Profound)

```bash
curl "https://api.profound.com/v1/brand/<brand-id>/citations?period=last_7_days" \
  -H "Authorization: Bearer $PROFOUND_API_KEY" \
| jq '{
  total_prompts_monitored: .total_prompts,
  prompts_with_brand_citation: .prompt_citations,
  citation_share: (.prompt_citations / .total_prompts),
  by_engine: .citations_by_engine
}'
```

Returns:

```json
{
  "total_prompts_monitored": 250,
  "prompts_with_brand_citation": 47,
  "citation_share": 0.188,
  "by_engine": {
    "chatgpt": 23,
    "gemini": 14,
    "claude": 12,
    "perplexity": 18
  }
}
```

### Recipe 2: Competitive share-of-voice

```bash
curl "https://api.profound.com/v1/brand/<brand-id>/share-of-voice?\
period=last_7_days&\
competitors=brand_a,brand_b,brand_c" \
  -H "Authorization: Bearer $PROFOUND_API_KEY"
```

```json
{
  "your_brand": {"citations": 47, "share": 0.20},
  "brand_a": {"citations": 88, "share": 0.37},
  "brand_b": {"citations": 56, "share": 0.24},
  "brand_c": {"citations": 32, "share": 0.13},
  "uncited": 27
}
```

Tells you who's winning AI surfaces. If competitors dominate, audit their content patterns.

### Recipe 3: Prompt-level citation detail

```bash
curl "https://api.profound.com/v1/brand/<brand-id>/prompts/<prompt-id>?include_responses=true" \
  -H "Authorization: Bearer $PROFOUND_API_KEY"
```

For each engine: the full AI response, which sources cited, where your brand appears (or doesn't), surrounding context.

### Recipe 4: Track new prompts / topics

```bash
curl -X POST "https://api.profound.com/v1/brand/<brand-id>/prompts" \
  -H "Authorization: Bearer $PROFOUND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompts": [
      "best marketing automation tool 2026",
      "what is the difference between klaviyo and mailchimp",
      "how to set up GA4 attribution",
      ...
    ],
    "frequency": "daily",
    "engines": ["chatgpt","gemini","claude","perplexity"]
  }'
```

Cost: $0.05-0.20 per prompt per engine per day. Budget for 100-500 prompts.

### Recipe 5: Brand mention rate (mentioned but not linked)

```bash
curl "https://api.profound.com/v1/brand/<brand-id>/mentions?period=last_30_days" \
  -H "Authorization: Bearer $PROFOUND_API_KEY"
```

Mentions without citations = opportunity for content creation (the AI knows you but isn't sourcing your content).

### Recipe 6: Content-pattern analysis (what gets cited)

```python
# Cross-reference your cited pages with non-cited pages
cited_urls = profound.get_cited_urls(brand_id, period='last_30_days')
non_cited_urls = ahrefs.site_explorer(target='yourbrand.com', mode='organic_keywords')

# What's different about cited content?
for url in cited_urls:
    page = firecrawl.scrape(url)
    print({
        'url': url,
        'has_faq_schema': 'FAQPage' in page.json_ld,
        'has_howto_schema': 'HowTo' in page.json_ld,
        'word_count': len(page.text.split()),
        'has_listicle_format': page.text.count('\n## ') > 5,
        'has_data_table': '<table>' in page.html,
        'reading_grade': page.flesch_kincaid_grade,
    })
```

Common AI-citation-friendly patterns:
- FAQ / HowTo schema
- 1500-3000 word "definitive guide" depth
- Listicle structure (clear H2/H3 hierarchy)
- Data tables / benchmarks
- Direct quote-friendly sentences (declarative, fact-based)
- Author with credentials (E-E-A-T)

### Recipe 7: AthenaHQ comparison

AthenaHQ's product overlaps; pull both for triangulation:

```bash
curl "https://api.athenahq.ai/v1/visibility?brand=<id>&period=7d" \
  -H "Authorization: Bearer $ATHENA_API_KEY"
```

If they disagree, AthenaHQ tracks more LLM-driven citations (incl. ChatGPT Plus search); Profound tracks more public-search-AI (Google AIO, Bing).

### Recipe 8: Alert on share drop

```bash
# Cron daily
yesterday=$(curl -s "https://api.profound.com/v1/brand/<id>/citations?period=yesterday" -H "Authorization: Bearer $PROFOUND_API_KEY" | jq .citation_share)
prior_week=$(curl -s "https://api.profound.com/v1/brand/<id>/citations?period=last_7_days_avg" -H "Authorization: Bearer $PROFOUND_API_KEY" | jq .citation_share)

drop=$(echo "($prior_week - $yesterday) / $prior_week" | bc -l)
if (( $(echo "$drop > 0.20" | bc -l) )); then
  # Alert via gmail-mcp
  echo "Profound citation share dropped 20%+ overnight" | gmail-mcp send --to "ops@brand.com"
fi
```

## Examples — full AEO/GEO program

```yaml
weekly_cadence:
  monday:
    - poll Profound + AthenaHQ for last-7d citation share
    - compare vs competitors
    - flag any prompts where competitor cited and we weren't
  tuesday-thursday:
    - if any flagged prompts, identify content pattern competitor uses
    - draft AI-citation-friendly content (FAQ format + structured data + data table)
  friday:
    - submit new URLs via suganthan-gsc-mcp submit_url
    - schedule social/email amplification

quarterly:
  - audit which content gets cited most
  - double down on those patterns
  - sunset content with zero citations after 6 months
```

## Edge cases

### LLM training cutoffs
LLMs cite content from training data; content < 6 months old may not appear until next model update. Set realistic expectations for new content velocity.

### "Real-time" SLA reality
- Profound polls engines on schedule (every 15 min for top prompts, hourly for tail)
- "5-min SLA" = report freshness, not query freshness
- For exec-facing reports, use 24h aggregates

### Citation vs mention
- **Citation**: source link in the AI response (the highest-value signal)
- **Mention**: brand name in response text, no source link (medium value)
- **Recommendation**: brand suggested but not by name (lower value)

Track all three; citations are gold.

### Brand confusion
If brand name overlaps with common words ("Atlas", "Pulse", "Bridge"), expect noise. Add disambiguation context to brand setup.

### Multi-brand portfolios
Track each brand separately; cross-tabulate at report layer. Profound supports parent/child brand grouping.

### Cost discipline
At ~$0.10/prompt/engine/day, 500 prompts × 4 engines × 30 days = $6000/mo. Prioritize:
- High-volume topic prompts (transactional intent)
- Branded prompts (sanity check)
- Competitor head-to-head prompts

### Engines covered (June 2026)
- ChatGPT (with web browsing)
- Google AIO / Gemini
- Anthropic Claude (with web search)
- Perplexity
- Meta AI (limited coverage)
- Microsoft Copilot
- You.com
- Brave Leo

Not all engines have stable APIs; both Profound + Athena use a mix of API + headless browser polling.

### Hallucination effect
AI may "cite" your brand for unrelated topics if your domain is high authority. Audit prompt-level results to ensure relevance — un-relevant citations dilute brand position.

### Structured data alone isn't enough
Schema.org markup helps but won't single-handedly drive citations. Combine with:
- Author credentials (E-E-A-T)
- Original data / research
- Clear topical authority (cluster pages)
- Active link-earning (Ahrefs MCP)

### Alternatives & free fallbacks
- Manually query ChatGPT / Gemini / Claude / Perplexity weekly with 10 brand-relevant prompts
- Document responses in a spreadsheet
- Free but doesn't scale > 50 prompts

## Sources

- **AthenaHQ**: https://athenahq.ai/
- **Profound**: https://tryprofound.com
- **Profound API docs**: https://docs.tryprofound.com
- **Comparison + methodology**: https://nicklafferty.com/blog/profound-vs-athena/
- **AEO concept**: https://searchengineland.com/aeo-answer-engine-optimization-440158
- **GEO research**: https://generative-engines.com/GEO/
- **AI Overviews + citations behavior**: https://developers.google.com/search/docs/appearance/ai-features
