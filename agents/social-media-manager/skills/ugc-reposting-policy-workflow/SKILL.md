<!--
Source: https://www.showca.se/post/ugc-usage-rights
Flockler UGC rights: https://flockler.com/features/ugc-rights-management
Pixlee / Taggbox / Bazaarvoice paid scale tools
Role.md "UGC reposting workflow"
-->
# UGC Reposting — Policy + Workflow — SKILL

Discovery via Brand24 (mentions + brand-hashtag uses) + Buffer (per-channel comments + tags). Rights-request DM per platform → Notion DB tracking (pending / granted / denied / expired). Auto-repost via Buffer with attribution. 2026 best practice: paid-licensing per-campaign-window vs perpetual. FTC disclosure on paid UGC mandatory.

## When to use this skill

- **Discovered UGC** featuring brand product / tag / hashtag.
- **Rights-request workflow** for branded campaign uses.
- **Brand-feed UGC reposting cadence** (e.g., 1-2 reposts/week).
- **Customer-testimonial sourcing** for case studies (with permission).
- **Campaign-driven UGC contest** with prize for top-3 entries.

**Do NOT use this skill when:**
- You need to reach the original creator privately (DM, support) — `community-engagement-comments-dms-at-scale`.
- The "UGC" is influencer-led (paid) — `influencer-outreach-modash-aspire-grin`.

## Setup

### Discovery sources

- **Brand24** (already configured in `social-listening-brandwatch-mention-talkwalker`) — tag + brand-mention monitoring
- **Buffer mentions** (already configured) — per-channel mentions + tags
- **Per-platform native search** — `#brandhashtag` + `@brand` on IG / TikTok / X
- **Manual weekly @search / hashtag-search** per platform

### Pixlee / Taggbox / Bazaarvoice (paid scale tools)

```bash
# Pixlee
export PIXLEE_API_KEY="<key>"
# Endpoint: https://api.pixlee.com/

# Taggbox
export TAGGBOX_API_KEY="<key>"
# Endpoint: https://api.taggbox.com/

# Bazaarvoice
export BV_API_KEY="<key>"
# Endpoint: https://api.bazaarvoice.com/
```

These automate rights-request flow + display. Use when recipient has license.

### Notion UGC DB

Columns: `Source URL / Creator handle / Platform / Date discovered / Rights-request sent date / Rights-request status (pending/granted/denied/expired) / License window (perpetual / campaign-only / 30-day / 90-day) / Brand-fit score (1-10) / Repost date / Repost URL / Engagement (reach, likes, comments)`.

### Per-platform DM templates (role.md)

Stored in `templates/ugc-rights-request-<platform>.md`.

## Common recipes

### Recipe 1: Daily UGC discovery

```python
# Pull last 24-hr UGC candidates
ugc = []
ugc += mcp.brand24.get_mentions(
    project_id=BRAND24_PROJECT_ID,
    keywords=['#brand', '#brandcampaign', '#brandlive'],
    since='yesterday'
)
ugc += mcp.buffer.get_engagements(channels=ALL_CHANNELS, types=['mention','tag'], since='yesterday')

for u in ugc:
    if is_ugc_repost_worthy(u):
        notion.upsert(ugc_db, {
            'Source URL': u['url'], 'Creator handle': u['author'],
            'Platform': u['channel'], 'Date discovered': today(),
            'Rights-request status': 'pending-review',
            'Brand-fit score': compute_brand_fit(u, BRAND_VOICE)
        })
```

### Recipe 2: Brand-fit scoring

```python
def compute_brand_fit(u, brand_voice):
    score = 0
    # Content matches brand-niche topic
    if topic_relevance(u['content']) > 0.5: score += 3
    # Original creator's audience quality
    creator_aqs = check_creator_aqs(u['author'])
    if creator_aqs and creator_aqs >= 70: score += 2
    # Visual quality (image / video aesthetics)
    if visual_quality_score(u.get('media_url')) > 0.7: score += 2
    # Sentiment (positive only)
    if u.get('sentiment') == 'positive': score += 2
    # No competitor mention
    if not contains_competitor(u['content']): score += 1
    return score  # 0-10
```

### Recipe 3: Rights-request DM per platform

```python
RIGHTS_TEMPLATES = {
    'instagram': """Hey {first_name}! Love this post 💛 We'd love to share it on our @{BRAND} account with full credit to you. Mind if we repost? Just reply with "yes" if you're cool with it. We'll tag you and link back.""",
    'tiktok': """{handle} this 👀 Mind if we share this on our @{BRAND} TikTok with credit? Reply "yes" if good with you!""",
    'x': """Love this @{handle} — mind if we share on our brand account with credit? Reply yes if OK!""",
    'threads': """@{handle} this is genuinely good. Mind if we share with credit on @{BRAND}? Reply yes if cool with you.""",
    'tiktok_alt': """@{handle} — love this. Can we share with credit?"""
}

for u in notion.query(ugc_db, filter={'Rights-request status': 'pending-review',
                                       'Brand-fit score__gte': 7}):
    template = RIGHTS_TEMPLATES[u['Platform']]
    msg = template.format(handle=u['Creator handle'],
                          first_name=parse_name(u['Creator handle']),
                          BRAND=BRAND_HANDLE)
    mcp.platform[u['Platform']].send_dm(to=u['Creator handle'], text=msg)
    notion.update(u['id'], {
        'Rights-request sent date': today(),
        'Rights-request status': 'pending'
    })
```

### Recipe 4: Rights-response tracking (auto)

```python
# Monitor DM replies for rights-grant signals
@on_dm_reply(filter='rights-request')
def on_response(reply):
    ugc_record = notion.query(ugc_db, filter={'Creator handle': reply['from']})[0]
    text = reply['text'].lower()
    
    if any(g in text for g in ['yes','sure','go for it','please','of course','definitely']):
        notion.update(ugc_record['id'], {
            'Rights-request status': 'granted',
            'License window': '30-day',  # default; adjust per agreement
        })
        # Reply with thanks + repost timeline
        mcp.platform[ugc_record['Platform']].send_dm(
            to=reply['from'],
            text=f"Thank you! We'll repost in the next 7 days and tag you."
        )
    elif any(d in text for d in ['no','prefer not','please don\'t']):
        notion.update(ugc_record['id'], {'Rights-request status': 'denied'})
        # Polite respect-decision reply
        mcp.platform[ugc_record['Platform']].send_dm(
            to=reply['from'],
            text="Totally understand! Thanks for taking the time to respond."
        )
```

### Recipe 5: License-window pricing tier

```python
LICENSE_TIERS = {
    'organic-only-30d': {'pay':0,    'usage':'organic feed only', 'window':'30 days'},
    'organic-90d':     {'pay':50,   'usage':'organic feed only', 'window':'90 days'},
    'paid-30d':        {'pay':150,  'usage':'organic + paid boost', 'window':'30 days'},
    'paid-90d':        {'pay':300,  'usage':'organic + paid boost', 'window':'90 days'},
    'perpetual':       {'pay':1000, 'usage':'all uses + repurpose',  'window':'perpetual'},
}
# Per role.md: "paid-licensing-per-campaign-window vs perpetual" — prefer windowed
```

### Recipe 6: Reposting with attribution

```python
# Per granted UGC, schedule repost via Buffer
for u in notion.query(ugc_db, filter={'Rights-request status':'granted','Repost date': None}):
    repost_caption = f"""{quote_caption_from_original(u['Source URL'])}

📸 / 🎥 by @{u['Creator handle']} — thanks for sharing!

{hashtag_basket(platform=u['Platform'])}
"""
    update = mcp.buffer.create_update(
        channelIds=[map_platform(u['Platform'])],
        text=repost_caption,
        mediaUrls=[u['Source media URL']],
        scheduledAt=schedule_for_optimal_time(u['Platform'])
    )
    notion.update(u['id'], {
        'Repost date': schedule_for_optimal_time(u['Platform']),
        'Repost URL': f"https://publish.buffer.com/{update['id']}"
    })
```

### Recipe 7: Disclosure compliance

```python
# Per role.md: "For paid UGC (creator was compensated), add #ad / #sponsored per FTC"
for u in notion.query(ugc_db, filter={'Repost date__gte': today() - 7d,
                                       'License': 'paid-30d'}):
    # Verify caption includes disclosure
    if '#ad' not in u['Repost caption'].lower() and '#sponsored' not in u['Repost caption'].lower():
        slack.post('#compliance', f"⚠ Missing FTC disclosure on {u['Repost URL']}")
        # Auto-edit if possible
        mcp.buffer.update_update(id=u['Buffer ID'], text=u['Repost caption'] + ' #ad')
```

### Recipe 8: License-expiry watchdog

```python
@scheduled('@daily')
def expiry_watchdog():
    expired = notion.query(ugc_db, filter={
        'License window__lt': now(),
        'Rights-request status': 'granted',
        'Repost URL__isnotnull': True
    })
    for u in expired:
        # Auto-delete repost OR notify
        mcp.platform[u['Platform']].delete_post(post_url=u['Repost URL'])
        notion.update(u['id'], {'Rights-request status': 'expired'})
        slack.post('#social-team', f"Expired UGC repost deleted: {u['Repost URL']}")
```

### Recipe 9: UGC contest campaign

```yaml
contest_name: "Best Summer Recipe with Brand X"
contest_window: T-0 to T+30
prize: $500 + featured spot
entry_mechanic: post with #BrandRecipe + tag @brand
winners: top-3 by community-vote + brand-fit score
rights: contest entry = automatic-grant for 90-day usage + paid boost (per terms)
disclosure: contest entries from prize winners get #ad on brand repost
```

### Recipe 10: At-scale tools integration (Pixlee / Taggbox / Bazaarvoice)

```python
# Pixlee: bulk rights-request
curl -X POST https://api.pixlee.com/v3/rights/request \
  -H "Authorization: Bearer $PIXLEE_API_KEY" \
  -d '{
    "media_ids": ["mid1","mid2","mid3"],
    "rights_template_id": "tpl_30day_organic",
    "auto_message": true
  }'

# Taggbox: tag-driven discovery
curl -G https://api.taggbox.com/feeds \
  -H "Authorization: Bearer $TAGGBOX_API_KEY" \
  -d "hashtag=brandcampaign"

# Bazaarvoice: review syndication + UGC
curl -G https://api.bazaarvoice.com/data/ugc.json \
  -H "passkey: $BV_API_KEY"
```

## Examples

### Example A: Weekly UGC reposting cadence

```yaml
weekly_repost_schedule:
  monday: 1 IG Reel UGC (granted week prior)
  wednesday: 1 IG carousel UGC
  friday: 1 TikTok UGC + 1 Story-mention reshare
output_metrics: 4 reposts/week, 3-5% engagement boost vs brand-original content
```

### Example B: Campaign-specific UGC pipeline

```yaml
campaign: summer_skincare_drop
discovery: weekly Brand24 sweep on #BrandSummerSkin + @brand mentions
rights_request_target: top 30 per week (brand-fit score >= 7)
expected_response_rate: 40%
expected_reposts: 12/week × 4 weeks = 48 reposts
license: 30-day organic-only (per campaign window)
budget_for_paid_UGC: $5,000 across top 10 creators
```

### Example C: UGC moderation + quality bar

```yaml
quality_bar:
  must_have: clear lighting, brand product visible, < 5s on-screen-text overflow
  must_not_have: competitor visible, off-brand language, low-resolution, blurry
auto_reject: skip + don't request rights
borderline: review with social-team-lead before requesting
```

## Edge cases

### Creator deletes original after we repost
License terminates. Delete brand repost within 48 hrs (manual notification). Don't argue with creator.

### Creator changes mind
Granted then revokes. Delete repost within 7 days. Document in Notion + thank-you-for-original-grant DM.

### Creator profile turns private / unavailable
Brand-fit score drops if we can't link back. Delete repost; don't pursue.

### Multiple creators in single UGC
Tag all visible creators; rights from each. If one denies, can't repost.

### Minors in UGC
Under-18 creators may not have legal capacity to grant. Require parent / guardian consent OR skip.

### UGC with brand competitor visible
Skip — don't promote competitor inadvertently.

### Repost driver: vanity vs marketing
Don't repost purely for vanity (flattering brand mention with no story). Brand-fit and storytelling value drive selection.

### Trademark / copyright in UGC media
Creator's UGC may include third-party music / logos. Brand assumes some liability on repost. Vet for trademark/copyright issues; substitute if needed.

### Disclosure on contest-driven UGC
Contest entries with prize = material-connection per FTC. Brand repost requires #ad. Document terms in contest rules.

### License-window-too-short
30-day window may expire while paid boost still serving. Coordinate paid amp end-date with license window.

### Cross-platform repost license
"Granted on IG" doesn't auto-cover X / TikTok repost. Clarify in DM "all-platforms" or "IG-only".

### Disclosure for unpaid UGC
Unpaid UGC doesn't require #ad. But: must always include creator attribution.

### Rights-confusion language barrier
DM template English-only. For non-English creators, use `deepl-mcp` for translation. Use clear-language phrasing.

### Rights-template international variation
EU / California GDPR + CCPA may require more explicit consent language. Use legal-reviewed template per region.

### Pre-existing legacy UGC
Brand may have reposted UGC without explicit rights years ago. Audit; reach out for retroactive grant or delete.

### Discovery-fatigue
Mid-tier brand may discover only 5-10 UGC/week. Lower brand-fit threshold (6+) and broaden hashtag list.

### Creator-fatigue
Same creators repeatedly requested = annoying. Cap: max 2 rights-requests per creator per quarter.

### Spam-bot account UGC
Bot accounts use brand hashtags. Filter via account-age + follower threshold. Don't request rights from bot accounts.

### Brand-jacking via fake reviews
Some "UGC" is competitor-planted. Cross-check authenticity before featuring.

### Compensation disclosure
"Paid for UGC" + #ad. "Sent free product" + #gifted. "Volunteer post" no required disclosure (but attribute).

## Sources

- **ShowCa — UGC usage rights 2026**: https://www.showca.se/post/ugc-usage-rights
- **Flockler — UGC rights management**: https://flockler.com/features/ugc-rights-management
- **Pixlee**: https://www.pixlee.com/
- **Taggbox**: https://taggbox.com/
- **Bazaarvoice**: https://www.bazaarvoice.com/
- **FTC disclosure rules**: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- **Brand24 mention-tracking**: https://brand24.com/
- **Role.md "UGC reposting workflow"**: rights-request DM templates + Notion DB schema
