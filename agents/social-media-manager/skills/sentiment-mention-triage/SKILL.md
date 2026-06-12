<!--
Source: https://brand24.com/
Brandwatch listening: https://www.brandwatch.com/blog/social-listening-tools/
Brand24 2026 AI sentiment (sarcasm + regional slang)
-->
# Sentiment + Mention Triage — SKILL

Daily Brand24 export → triage table (positive / neutral / negative / urgent) → action assignments (positive → reshare / negative → DM author / urgent → crisis-comms). 2026 Brand24 model handles sarcasm, regional slang, complex syntax. Falls to Talkwalker AI sentiment for enterprise. Hand-tuned classifier via `cli-anything` + Claude when paid tools unavailable.

## When to use this skill

- **Daily inbox of brand mentions** to act on (already pulled by `social-listening-brandwatch-mention-talkwalker`).
- **Weekly trend report** — positive / negative breakdown + top drivers.
- **Mention-to-action assignment** — what does each mention earn from us.
- **Sentiment drift alert** — week-over-week negative spike.

**Do NOT use this skill when:**
- The mention is from your own followers in your own comments — that's community engagement.
- Crisis-level (volume spike > 2x baseline) — `social-crisis-comms`.
- Single customer complaint — `social-customer-service-handoff`.

## Setup

### Brand24 MCP

Already in `social-listening-brandwatch-mention-talkwalker`.

### Notion Triage Table DB

Columns: `Mention URL / Date / Channel / Author / Sentiment (positive/neutral/negative) / Sentiment confidence / Reach / Topic / Action assigned / Status (new/in-progress/done/skipped) / Assignee / Outcome`.

### Optional: secondary classifier (Claude / OpenAI)

When Brand24 confidence < 70%, run secondary check:

```bash
# Claude API for sarcasm / contextual analysis
curl -X POST https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-7-20260101",
    "max_tokens": 100,
    "messages": [{"role":"user","content":"Classify sentiment (positive/neutral/negative) and confidence (0-1) of this social mention. Account for sarcasm and slang. Just respond JSON: {sentiment, confidence}.\n\nMention: <text>"}]
  }'
```

## Common recipes

### Recipe 1: Daily 9am triage pull

```python
# 1. Pull last 24hr mentions
mentions = mcp.brand24.get_mentions(project_id=BRAND24_PROJECT_ID, since='yesterday', limit=500)

# 2. Classify (Brand24 ships sentiment + confidence)
for m in mentions:
    if m['sentiment_confidence'] < 0.70:
        # Secondary check via Claude
        secondary = call_claude_sentiment(m['content'])
        if secondary['confidence'] > 0.80 and secondary['sentiment'] != m['sentiment']:
            m['sentiment'] = secondary['sentiment']
            m['flagged_for_review'] = True
    
    notion.upsert(triage_db, {
        'Mention URL': m['url'],
        'Date': m['created_at'],
        'Channel': m['source'],
        'Author': m['author'],
        'Sentiment': m['sentiment'],
        'Sentiment confidence': m['sentiment_confidence'],
        'Reach': m['reach'],
        'Topic': extract_topic(m['content']),
        'Action assigned': decide_action(m),
        'Status': 'new'
    })
```

### Recipe 2: Action-assignment rules

```python
def decide_action(m):
    # Per role.md sentiment-mention triage logic
    if m['sentiment'] == 'positive':
        if m['reach'] > 10_000:
            return 'reshare'  # high-reach positive → reshare / quote
        if 'UGC' in m['flags'] or 'tagged photo' in m['flags']:
            return 'ugc-rights-request'  # → ugc-reposting-policy-workflow
        return 'testimonial-bank'  # → log for case-study sourcing
    
    if m['sentiment'] == 'negative':
        if m['reach'] > 100_000 or 'press' in m['flags']:
            return 'crisis-watch'  # → social-crisis-comms
        return 'dm-author'  # quiet 1:1 resolution → social-customer-service-handoff
    
    if m['sentiment'] == 'neutral' and m['reach'] > 1_000_000:
        return 'opportunity-watch'  # could become positive with engagement
    
    return 'log-only'
```

### Recipe 3: Sentiment delta alert (rolling baseline)

```python
# Per channel + overall, week-over-week
baseline_neg_per_day_30d = mean([
    notion.count(triage_db, filter={'Sentiment':'negative', 'Date': d})
    for d in last_30_days
])
today_neg = notion.count(triage_db, filter={'Sentiment':'negative', 'Date': today})

if today_neg > 2 * baseline_neg_per_day_30d:
    slack.post('#social-listening',
        f"⚠ Negative volume 2x baseline: {today_neg} vs {baseline_neg_per_day_30d:.0f}/day")
    trigger_crisis_watch_review()
```

### Recipe 4: Topic clustering (recurring themes)

```python
# Group negative mentions by topic for product-feedback signal
neg_30d = notion.query(triage_db, filter={'Sentiment':'negative','Date__gte': now-30d})
topic_counts = Counter(m['Topic'] for m in neg_30d)
for topic, n in topic_counts.most_common(5):
    if n >= 10:
        slack.post('#product-feedback',
            f"Negative cluster: '{topic}' — {n} mentions in 30 days")
```

### Recipe 5: Positive-mention reshare candidate

```python
# Daily: top 5 positive mentions by reach + relevance
top_positive = sorted(
    notion.query(triage_db, filter={'Sentiment':'positive','Status':'new','Date': today}),
    key=lambda m: -m['Reach']
)[:5]

for m in top_positive:
    if m['Reach'] > 10_000:
        notion.update(m['id'], {'Action assigned': 'reshare', 'Assignee': '@social-team-lead'})
```

### Recipe 6: Negative-mention low-reach DM-author flow

```python
for m in notion.query(triage_db, filter={'Sentiment':'negative','Reach__lt':100_000,'Status':'new'}):
    notion.update(m['id'], {'Action assigned': 'dm-author'})
    # Auto-handoff to social-customer-service-handoff
    social_customer_service.handle(
        engagement_id=m['mention_id'],
        channel=m['Channel'],
        author=m['Author'],
        original_text=m['content']
    )
```

### Recipe 7: Sarcasm-detection edge cases

```python
# When Brand24 sentiment positive but content has sarcasm-markers
SARCASM_MARKERS = ['/s', '"great"', '*wonderful*', '😒', 'sure jan', 'yeah right']
for m in notion.query(triage_db, filter={'Date': today, 'Sentiment': 'positive'}):
    if any(marker in m['content'].lower() for marker in SARCASM_MARKERS):
        # Re-classify
        secondary = call_claude_sentiment(m['content'])
        if secondary['sentiment'] == 'negative':
            notion.update(m['id'], {
                'Sentiment': 'negative',
                'Sentiment confidence': secondary['confidence'],
                'Notes': 'Re-classified — sarcasm detected'
            })
```

### Recipe 8: Per-channel sentiment health board

```python
# Weekly: per channel, positive % vs baseline
for channel in CHANNELS:
    last_7d = notion.query(triage_db, filter={'Channel': channel, 'Date__gte': now-7d})
    pos_pct = len([m for m in last_7d if m['Sentiment']=='positive']) / max(len(last_7d), 1)
    notion.upsert(channel_sentiment_db, {'Channel': channel, 'Week': week_start,
        'Positive %': pos_pct * 100,
        'Volume': len(last_7d)})
    if pos_pct < 0.50:
        slack.post('#social-listening',
            f"{channel}: positive sentiment dropped to {pos_pct*100:.0f}% — review topics")
```

### Recipe 9: Author-level patterns (advocate vs detractor)

```python
# Identify recurring authors: brand advocates + brand detractors
authors = defaultdict(list)
for m in last_90d_mentions:
    authors[m['Author']].append(m['Sentiment'])
brand_advocates = {a: s for a, s in authors.items()
                   if len(s) >= 3 and Counter(s).most_common(1)[0][0] == 'positive'}
brand_detractors = {a: s for a, s in authors.items()
                    if len(s) >= 3 and Counter(s).most_common(1)[0][0] == 'negative'}

# Advocates → influencer-outreach candidates (low cost; already a fan)
# Detractors → outreach with care; may be addressable
```

### Recipe 10: Quarterly sentiment retrospective

```python
quarter_data = notion.query(triage_db, filter={'Date__gte': q_start, 'Date__lte': q_end})
report = {
    'total_mentions': len(quarter_data),
    'positive_pct': len([m for m in quarter_data if m['Sentiment']=='positive']) / len(quarter_data) * 100,
    'negative_pct': len([m for m in quarter_data if m['Sentiment']=='negative']) / len(quarter_data) * 100,
    'top_positive_drivers': top_topics(quarter_data, sentiment='positive', limit=5),
    'top_negative_drivers': top_topics(quarter_data, sentiment='negative', limit=5),
    'reshare_count': len([m for m in quarter_data if m['Status']=='done' and m['Action assigned']=='reshare']),
    'crisis-watch triggered': len([m for m in quarter_data if m['Action assigned']=='crisis-watch']),
}
slack.post('#leadership', format_quarterly_report(report))
```

## Examples

### Example A: Daily triage output

```
Sentiment Triage — 2026-06-11 (last 24hr)

Total mentions: 142
Positive: 78 (55%)  Neutral: 41 (29%)  Negative: 23 (16%)

Top actions assigned:
  - 5 reshare candidates (reach > 10k each)
  - 4 ugc-rights-request flows
  - 18 dm-author (low-reach negatives)
  - 2 crisis-watch (high-reach negatives, monitor)

Top positive drivers (topics):
  1. customer onboarding experience (12 mentions)
  2. customer support response time (8 mentions)
  3. product reliability (6 mentions)

Top negative drivers:
  1. checkout broken on Safari (7 mentions) — recurring, escalate to product
  2. shipping delay (4 mentions) — operations
  3. pricing change (3 mentions) — communicate transparency
```

### Example B: Sarcasm catch

```yaml
mention: "Wow, brand X really 'fixed' my issue 😒"
brand24_initial: positive (0.62 confidence)
secondary_check: claude → negative (0.91 confidence)
final: negative
action: dm-author
```

### Example C: Advocate identification

```yaml
author: '@superfan_dani'
90d_mentions: 14 (12 positive, 2 neutral, 0 negative)
suggestion: invite to advocate program
outreach: 'Hey Dani — you've been such a champion lately. Would you be open to a Lunch Series interview?'
```

## Edge cases

### Confidence-threshold edge
Brand24 confidence 70-85% = ambiguous. Decide threshold: 80% → trust, < 80% → secondary check. Tune per false-positive rate.

### Language coverage
Brand24 2026 model strong in EN / ES / FR / DE / PT / IT. Other languages drop to baseline confidence. Use Claude / OpenAI for cross-language sarcasm.

### Region-specific slang
Brand24 handles regional slang in supported languages. For dialect-heavy markets (UK / Australia), occasional false-positive on humor. Quarterly calibration helps.

### Bot-generated mentions
Spam bot mentions clog triage. Filter via heuristics: handle pattern (e.g., 8-digit suffix), low followers, account age < 30 days. Drop from triage; don't escalate.

### Sentiment vs intent
A neutral fact-mention isn't a complaint or compliment. Don't auto-action neutrals; log only.

### High-reach neutral
Mention reaches 1M but sentiment neutral. Likely a news article or viral fact. "Opportunity watch" — engage to nudge positive if relevant.

### Mass-mention from one user
Single user spamming 50 mentions = artificial sentiment skew. Dedupe by author within window.

### Sentiment shift on the same post
A positive post can attract negative comments. Triage individual mentions, not just the original post.

### Brand-name homonyms
"Apple" matches fruit posts. Use AND / NOT operators in Brand24 project config to filter. False positives drain triage capacity.

### Mention-vs-tag distinction
@mention vs #brand-tag vs unstructured "Brand X" string detection. Brand24 catches all; differentiate in triage so action rules calibrate.

### Action assignment workflow
Don't auto-action without human review on critical / crisis-watch tier. Auto-action OK for reshare (low risk) and log-only (zero action).

### Reshare permissions
Always check rights before quoting customer content. UGC rights workflow (see `ugc-reposting-policy-workflow`) applies even to reshares.

### Detractor-engagement risk
DMing a detractor can backfire if they screenshot the DM. Public-first response often safer for low-reach. Private DM only after public ack.

### Sentiment baseline drift
Industry events (recession, regulation, scandal) can shift baseline. Recompute baseline monthly, not annually.

## Sources

- **Brand24 AI sentiment 2026**: https://brand24.com/
- **Brand24 sarcasm + slang model**: https://brand24.com/blog/sentiment-analysis-ai-update/
- **Brandwatch — listening + sentiment 2026**: https://www.brandwatch.com/blog/social-listening-tools/
- **Talkwalker AI sentiment**: https://www.talkwalker.com/blog/ai-social-listening
- **Anthropic Claude API (secondary classifier)**: https://docs.anthropic.com/
- **Role.md "Social listening playbook" — sentiment thresholds + action assignments**
