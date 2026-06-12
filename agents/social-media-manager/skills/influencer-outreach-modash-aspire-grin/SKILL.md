<!--
Source: https://www.modash.io/influencer-marketing-api/discovery
Modash 350M+ profile DB: https://www.modash.io/blog/influencer-marketing-platforms
Aspire CRM: https://www.aspire.io/
GRIN: https://grin.co/
-->
# Influencer Outreach — Modash + Aspire + GRIN — SKILL

Discover, vet, brief, and track creators end-to-end. Modash Discovery API (350M+ public IG / TikTok / YouTube profiles) is the agent-executable SOTA discovery layer. Aspire and GRIN handle managed-program CRM + payments for recipients who run paid creator programs. Every match passes `influencer-fraud-detection-hypeauditor` AQS ≥ 70 gate before outreach.

## When to use this skill

- **Sourcing creators** by audience demographic, niche, country, engagement rate, follower range.
- **Cold-list building** for a campaign brief.
- **Outreach pipeline** — discovery → vet → personalize → send → track response.
- **Campaign CRM** — when recipient pays creators, payments tracked in Aspire / GRIN.

**Do NOT use this skill when:**
- You need to verify a creator isn't a fraud — that's `influencer-fraud-detection-hypeauditor` (always run after Modash discovery).
- You need to track UGC reposting rights — `ugc-reposting-policy-workflow`.
- Creator account takeover — `account-takeovers-creator-handoff`.

## Setup

### Modash Discovery API

```bash
export MODASH_KEY="<api-key>"   # Paid plan, ~$120-$1000+/mo by volume
# Endpoint: https://api.modash.io/v1/
```

### Aspire (managed-program CRM)

```bash
export ASPIRE_API_KEY="<key>"
# Endpoint: https://api.aspireiq.com/v1/
```

### GRIN

```bash
export GRIN_API_KEY="<key>"
# Endpoint: https://api.grin.co/v1/
```

### HypeAuditor (mandatory vetting layer)

```bash
export HYPEAUDITOR_KEY="<key>"
# Endpoint: https://api.hypeauditor.com/v1/
# See influencer-fraud-detection-hypeauditor skill for full setup
```

### Notion Influencer CRM DB

Columns: `Handle / Platform / Followers / AQS / Audience-match% / Engagement rate / Status (sourced/vetted/pitched/negotiating/signed/shipping/posted/paid) / Brief sent date / Contract signed / Posts shipped / Posts published URL / Reach / Engagement / Clicks / Conversions / Total cost / ROI`.

## Common recipes

### Recipe 1: Modash Discovery search

```bash
curl -G "https://api.modash.io/v1/discovery/search" \
  -H "Authorization: Bearer $MODASH_KEY" \
  --data-urlencode "platform=instagram" \
  --data-urlencode "filter[audience_country]=US" \
  --data-urlencode "filter[audience_age]=18-34" \
  --data-urlencode "filter[audience_gender]=female:60" \
  --data-urlencode "filter[engagement_rate][gte]=2.0" \
  --data-urlencode "filter[followers][gte]=10000" \
  --data-urlencode "filter[followers][lte]=100000" \
  --data-urlencode "filter[niche]=fitness" \
  --data-urlencode "filter[recent_post_within_days]=30" \
  --data-urlencode "limit=100"
```

Returns: `[{user_id, handle, full_name, followers, engagement_rate, audience: {country_breakdown, age_breakdown, gender_breakdown}, recent_posts: [...]}]`.

### Recipe 2: Bulk profile details

```bash
curl -X POST https://api.modash.io/v1/profiles/lookup \
  -H "Authorization: Bearer $MODASH_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform": "instagram", "handles": ["creator1","creator2","creator3"]}'
```

### Recipe 3: Pipeline — discovery → AQS gate → Notion

```python
# 1. Discover
matches = modash.search(
    platform='instagram',
    filter={'audience_country':'US','engagement_rate':{'gte':2.0},
            'followers':{'gte':10000,'lte':100000},'niche':'fitness'},
    limit=200
)

# 2. AQS gate (HypeAuditor)
qualified = []
for m in matches:
    aqs = hypeauditor.get_aqs(handle=m['handle'], platform='instagram')
    if aqs['aqs'] >= 70:
        m['aqs'] = aqs['aqs']
        m['audience_authenticity'] = aqs['audience_quality']
        qualified.append(m)

# 3. Audience-match score (additional filter)
target = {'country':'US','age':'18-34','gender':'female'}
for m in qualified:
    match_score = (
        m['audience']['country_breakdown'].get(target['country'], 0) +
        m['audience']['age_breakdown'].get(target['age'], 0) +
        m['audience']['gender_breakdown'].get(target['gender'], 0)
    ) / 3
    m['audience_match'] = match_score

shortlist = sorted([m for m in qualified if m['audience_match'] > 0.5],
                   key=lambda x: -x['audience_match'])[:50]

# 4. Upsert into Notion CRM
for c in shortlist:
    notion.create_page(crm_db, {
        'Handle': c['handle'], 'Platform': 'instagram',
        'Followers': c['followers'], 'AQS': c['aqs'],
        'Audience-match%': int(c['audience_match']*100),
        'Engagement rate': c['engagement_rate'],
        'Status': 'sourced'
    })
```

### Recipe 4: Personalized outreach via Gmail MCP

```python
for c in shortlist:
    # Pull most recent post to reference
    recent = modash.get_profile(c['handle'])['recent_posts'][0]
    body = OUTREACH_TEMPLATE.format(
        first_name=c['full_name'].split()[0],
        recent_post_ref=summarize_post(recent),
        why_aligns=brand_alignment(c),
        budget_range='$500-$2000',
        deliverable='1 Reel + 3 Stories',
        booking_link='https://cal.com/brand/influencer-collab'
    )
    gmail.send(to=c.get('email') or find_email(c['handle']),
               subject=f"Quick collab idea — Brand x @{c['handle']}",
               body=body)
    notion.update_page(c['notion_id'], {'Status': 'pitched',
                                         'Brief sent date': today()})
```

Outreach template (see role.md):

```
Subject: Quick collab idea — [brand] x [@handle]

Hi {first_name},

Just watched {recent_post_ref} — {why_we_noticed_them}.

We're [brand]. Launching [campaign], looking for [N] creators who actually use [category]. Your audience overlap looks strong: {data_point}.

If booking [time window]:
- Deliverable: {deliverable}
- Compensation: ${budget_range} flat OR rate-card if higher
- Usage rights: organic + paid boost for 30 days
- Disclosure: #ad / #sponsored
- Approval: light pre-approval; not gate-keeping your voice

Two paths to yes:
1. Reply with "interested" + your rate
2. Book here: {booking_link}

— [name]
```

### Recipe 5: Aspire managed-program sync

```bash
# Push qualified shortlist into Aspire campaign
curl -X POST https://api.aspireiq.com/v1/campaigns/$CAMPAIGN_ID/creators \
  -H "Authorization: Bearer $ASPIRE_API_KEY" \
  -d '{"creator_handles":["creator1","creator2"], "platform":"instagram", "status":"invited"}'
```

### Recipe 6: GRIN payment workflow

```bash
# Create payout after creator delivers
curl -X POST https://api.grin.co/v1/payments \
  -H "Authorization: Bearer $GRIN_API_KEY" \
  -d '{
    "creator_id":"crt_abc",
    "amount_cents":150000,
    "currency":"USD",
    "deliverable_ids":["dlv_123"],
    "payment_terms":"net_30"
  }'
```

### Recipe 7: Performance tracking

```python
# Per published creator post, pull metrics via native MCP
for c in notion.query(crm_db, filter={'Status':'posted'}):
    metrics = insta_business.get_post_insights(media_id=c['published_media_id'])
    notion.update_page(c['notion_id'], {
        'Reach': metrics['reach'],
        'Engagement': metrics['engagement'],
        'Clicks': metrics.get('clicks', 0)
    })
```

### Recipe 8: Tiered creator-mix strategy

```python
TIERS = {
    'nano':   {'followers':(1_000, 10_000),    'er_min':3.0, 'pay':(50,200)},
    'micro':  {'followers':(10_000, 100_000),  'er_min':2.0, 'pay':(200,2000)},
    'mid':    {'followers':(100_000, 500_000), 'er_min':1.0, 'pay':(2000,10000)},
    'macro':  {'followers':(500_000, 1_000_000),'er_min':0.5,'pay':(10000,50000)},
    'mega':   {'followers':(1_000_000, None),  'er_min':0.3, 'pay':(50000,None)},
}
# Recommended mix for SMB: 80% micro + 15% mid + 5% macro for reach amplification
```

## Examples

### Example A: 50-creator fitness campaign

```yaml
campaign: spring_strength_2026
brief:
  goal: awareness + UGC seeding
  target_audience: US women 25-34, fitness niche
  budget: $40,000
  tier_mix: 40 micro + 8 mid + 2 macro

pipeline:
  1. Modash search → 200 matches
  2. HypeAuditor AQS gate → 130 pass
  3. Audience-match filter > 60% → 75 pass
  4. Manual brand-safety review → 55 shortlisted
  5. Outreach Gmail merge → 55 emails
  6. Response rate target: 25% = 14 booked
  7. Negotiation + contract → 12 signed
  8. Production + publish (T+30)
  9. Analytics rollup (T+45)
```

### Example B: Quarterly creator-pool refresh

```bash
# Run quarterly to refresh the discovery pool
modash.search(...) > discovery-Q3-2026.json
python pipeline.py discovery-Q3-2026.json
# Pushes new candidates into Notion 'sourced' bucket
```

## Edge cases

### Modash plan caps
Discovery API charged per-result and per-detail-call. 200k searches/mo on starter plan. Budget alerts at 80% cap.

### Email discoverability
Modash returns public-bio email for ~30% of profiles. For others, use Apollo / Hunter / Findymail (fall to `cli-anything curl`). Some creators only respond via DM — fall to platform MCP.

### Audience overlap with other brands
A creator promoting a competitor in last 30 days = risk. Pull recent posts; if competitor mention found, deprioritize or address explicitly in outreach.

### Disclosure mandate
FTC requires #ad / #sponsored on every sponsored post. Make this contractual; check published posts; if missing, contact creator immediately and document.

### Payment compliance
1099-MISC required for US creators paid > $600/yr. GRIN / Aspire handle. For ad-hoc DIY, use `cli-anything` Stripe / Wise for international.

### Rate negotiation
Don't open with budget cap. Ask creator rate; ~30% of replies will be under your max. Set internal floor and ceiling per tier.

### Engagement rate inflation
Some creators run engagement pods or bot-like comments. Pair Modash ER with HypeAuditor authenticity breakdown. Reject if `real_followers < 60%` even when AQS marginal.

### Recent-post recency
Don't pitch creators silent > 14 days; they may be on hiatus or have churned the platform. Modash `recent_post_within_days` filter is the gate.

### Brand-safety review
Manual review for last 6 months controversial content / banned topics / discriminatory speech. Modash has light flagging; HypeAuditor adds Brand Safety score. Never skip the manual pass on macro+ tier.

### Multi-platform creator
A creator on IG + TikTok + YouTube — check the post you're pitching applies to the right platform. Discovery returns per-platform profiles.

### Contract scope
Always specify deliverable count, posting window, exclusivity terms (if any), usage rights (organic only / paid-boost / repurpose window). See role.md influencer brief template.

### Modash + Aspire / GRIN duplication
If recipient runs Aspire / GRIN program, don't double-load creators into Notion. Make Aspire / GRIN the system of record; Notion = staging for not-yet-onboarded.

## Sources

- **Modash — Discovery API**: https://www.modash.io/influencer-marketing-api/discovery
- **Modash — best influencer platforms 2026**: https://www.modash.io/blog/influencer-marketing-platforms
- **Aspire**: https://www.aspire.io/
- **GRIN**: https://grin.co/
- **HypeAuditor (fraud screen)**: https://hypeauditor.com/
- **FTC disclosure guide**: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- **OutlierKit — best influencer APIs**: https://outlierkit.com/resources/best-influencer-marketing-platform-apis/
