# Podcast Sponsorship Integration — Host-Read Scripts + DAI via Captivate / Buzzsprout / Transistor

> Write host-read sponsor scripts (4× recall vs pre-roll) and place via dynamic ad insertion (DAI) per podcast host.

## When to use

Trigger on: "write a sponsor read", "host-read script", "DAI insertion", "podcast sponsorship integration", "Buzzsprout DAI", "Captivate ad inserter", "Transistor sponsorship", "mid-roll vs pre-roll". This skill owns: host-read script writing in brand voice, DAI configuration per podcast host, sponsor placement strategy (pre-roll vs mid-roll vs post-roll), sponsor performance tracking. For pitching sponsors + briefing the partnership see `creator-collab-brand-partnership-briefing`. For general newsletter / blog sponsorships see the monetization skill.

## Setup

```bash
# Buzzsprout API (Pro+ plan)
curl -H "Authorization: Token token=$BUZZSPROUT_API_KEY" \
  https://www.buzzsprout.com/api/<podcast_id>/episodes.json

# Captivate API (Pro+ plan)
curl -H "Authorization: Bearer $CAPTIVATE_API_KEY" \
  https://api.captivate.fm/shows

# Transistor API (Pro+ plan)
curl -H "x-api-key: $TRANSISTOR_API_KEY" \
  https://api.transistor.fm/v1/shows

# Megaphone Enterprise API
curl -H "Authorization: Bearer $MEGAPHONE_API_KEY" \
  https://cms.megaphone.fm/api/networks
```

Auth env vars:
- `BUZZSPROUT_API_KEY` + `BUZZSPROUT_PODCAST_ID` — Pro $24/mo+ for API.
- `CAPTIVATE_API_KEY` + `CAPTIVATE_SHOW_ID` — Captivate Pro $19/mo+ for API.
- `TRANSISTOR_API_KEY` + `TRANSISTOR_SHOW_ID` — Pro $19/mo+ for API.
- `MEGAPHONE_API_KEY` — Enterprise plan only.

## Common recipes

### Recipe 1: Host-read sponsor script template

```markdown
# Sponsor read: <Brand> on <Show Name> Episode <#>
**Placement:** Mid-roll (00:18:00) — SOTA timing for max recall
**Length:** 60-90 seconds
**Read type:** Host-read (4× recall vs voiced ad)
**Disclosure:** "This episode is sponsored by <Brand>" at the top

## Script (60-80 seconds at host's natural pace)

[HOST, in show voice, NOT brand-script voice]

"This episode is sponsored by <Brand>.

<one-sentence personal context — actual experience or specific reason this matters to host>

<the brand's value prop, but in host's words>

<one specific feature or use case that ties to the show's audience>

<the offer — code, URL, percentage off>

<repeat the URL once more>

Now back to the show."

## CTA UTM
- URL: <brand.com/showname>
- Override URL with: <brand.com/showname?utm_source=podcast&utm_medium=host-read&utm_campaign=ep042>

## Brand-required language (verbatim, if any)
- <legal disclaimer the brand requires word-for-word>

## Brand-prohibited language
- <any words the brand has flagged as off-brand>

## Recording note
- Record this LIVE during the episode, not as a separate clip — natural inflection raises recall
- Don't sound rehearsed; do a single take after reading once
```

### Recipe 2: Placement strategy (where to put the sponsor)

```markdown
## Pre-roll (0:00 - 0:30)
- Pros: every listener hears it
- Cons: 4× LOWER recall vs mid-roll; listeners scrub past or skip
- Use for: classified-style flat-fee reads where reach > recall

## Mid-roll (25% mark of episode)
- Pros: highest recall; listener already invested; SOTA timing
- Cons: lower total reach (some listeners drop before mid-roll)
- Use for: host-read flagship sponsors

## Mid-roll #2 (75% mark of episode)
- Pros: catches engaged listeners; pairs with CTA momentum
- Cons: some listeners gone by then
- Use for: second sponsor in episodes with 2 ad slots

## Post-roll (last 60s)
- Pros: only engaged listeners; high-intent audience
- Cons: smallest reach
- Use for: lead-magnet / newsletter own-product CTA, not paid sponsors

## SOTA placement for ONE sponsor
Mid-roll at 25% mark → 4× recall vs pre-roll, 2× recall vs post-roll
```

### Recipe 3: Dynamic Ad Insertion (DAI) via Buzzsprout

```bash
# Buzzsprout DAI = Dynamic Content + Affiliate Marketplace
# Step 1: Create ad slot in dashboard or via API
curl -X POST "https://www.buzzsprout.com/api/$BUZZSPROUT_PODCAST_ID/dynamic_content" \
  -H "Authorization: Token token=$BUZZSPROUT_API_KEY" \
  -d '{
    "name": "Sponsor: <Brand> Q3",
    "audio_url": "<host_read_recording_url>",
    "placement": "mid_roll",
    "start_date": "2026-07-01",
    "end_date": "2026-09-30",
    "max_impressions": 50000
  }'

# Step 2: Episodes published in date range auto-include the ad
# Step 3: Pull insertion stats
curl -H "Authorization: Token token=$BUZZSPROUT_API_KEY" \
  "https://www.buzzsprout.com/api/$BUZZSPROUT_PODCAST_ID/dynamic_content/<id>/stats.json"
```

### Recipe 4: Captivate DAI workflow

```bash
# Captivate's "AMIE Ads" feature (built-in DAI)
# Create insertion via dashboard; pull metrics via API

curl -H "Authorization: Bearer $CAPTIVATE_API_KEY" \
  "https://api.captivate.fm/shows/$CAPTIVATE_SHOW_ID/insertions"
```

Captivate's DAI is GUI-only as of June 2026; API supports metrics retrieval but not insertion creation.

### Recipe 5: Transistor DAI workflow

```bash
# Transistor "Dynamic Pre-roll/Post-roll" — flat slot per episode
curl -X POST https://api.transistor.fm/v1/episodes/<id>/dynamic_content \
  -H "x-api-key: $TRANSISTOR_API_KEY" \
  -d '{
    "audio_url": "<host_read_recording_url>",
    "placement": "post_roll"
  }'
```

Transistor DAI is simpler — only supports pre-roll and post-roll, not mid-roll insertion. Mid-roll sponsors get baked into the episode master.

### Recipe 6: Brand-voice translation

```markdown
# Brand-supplied script:
"Our innovative SaaS platform leverages AI-powered analytics to optimize your marketing funnel."

# Translated to host voice:
"<Brand> built an analytics tool that I actually use. It connects to your stack and surfaces what's
actually moving the needle — instead of you guessing which campaign drove the deal. I've been using
it for two months and the AB test scoring alone has saved me ~5 hours/week. They're offering 30% off
the first 3 months — code is <SHOWNAME> at <brand.com/showname>."

# Key rules:
- "Leverage" → "use"
- "Innovative SaaS platform" → "[what it does]"
- "Optimize" → "show me what's working"
- Add personal anecdote
- Add specific outcome (time saved, money saved, problem solved)
- Specific offer + code + URL
```

### Recipe 7: Sponsor performance tracking

```python
# Pull sponsor metrics per episode + roll up
sponsor_metrics = {}
for episode_id in last_30_episodes:
    insertions = api.get(f"/episodes/{episode_id}/dynamic_content/stats")
    for ins in insertions:
        sponsor_name = ins['name']
        sponsor_metrics.setdefault(sponsor_name, {'impressions':0, 'clicks':0, 'conversions':0})
        sponsor_metrics[sponsor_name]['impressions'] += ins['impressions']
        sponsor_metrics[sponsor_name]['clicks'] += ins.get('clicks', 0)

# Compute CTR + cost per click
for name, m in sponsor_metrics.items():
    m['ctr'] = m['clicks'] / m['impressions'] if m['impressions'] else 0
    print(f"{name}: {m}")
```

### Recipe 8: CPM rate card (what to charge)

```markdown
## Standard CPM rates (2026)

| Format | CPM |
|---|---|
| Pre-roll (15-30s) | $15-25 |
| Mid-roll host-read (60-90s) | $25-50 |
| Mid-roll host-read PREMIUM (specific audience) | $50-100 |
| Post-roll (15-30s) | $10-20 |
| Branded segment (3-5 min) | $100-250 |
| Full episode sponsorship | flat $1,500-15,000 depending on downloads |

## Reach math
- 10k downloads/episode × $40 mid-roll CPM = $400/episode
- 10k × $25 pre-roll = $250/episode
- 50k downloads × $40 mid-roll = $2,000/episode
- 100k+ downloads = sponsorship marketplace tier (consider Megaphone)
```

### Recipe 9: Network-level sponsorship cascade (multi-show)

```markdown
## Network sponsorship structure

When a creator operates multiple shows or partners with a network (e.g., Megaphone, Acast, Wondery):

- Bundle deals across 3-5 shows = 20-30% discount per show but higher total
- Brand gets uniform creative across the network
- Performance metrics rolled up at network level
- Use for: lower CPM trade for high-volume / multi-touchpoint

Pitch: "$X for 5 shows × 4 episodes = 20 mid-roll impressions across <total downloads>"
```

### Recipe 10: FTC disclosure for podcast sponsorships

```markdown
## At the top of the sponsor read:
"This episode is sponsored by <Brand>." (clear + conspicuous + close to endorsement)

## In show notes:
"This episode is sponsored by <Brand>. Use code <SHOWNAME> for 30% off at <URL>."

## Apple Podcasts / Spotify metadata:
Some platforms surface sponsored disclosures separately. Check podcast host's
"sponsorship disclosure" toggle.

## DO NOT bury disclosure
- After the sponsor read (too late)
- In show notes only (insufficient)
- Without naming the brand (vague)
```

### Recipe 11: Sponsor-mention extraction from past transcripts

```bash
# Find recurring sponsors mentioned organically in past episodes — these are warm leads for pitching
grep -i "I use" episodes/*/transcript.txt | grep -E "<Tool|Brand>" | sort -u | head -20
```

### Recipe 12: Wrap report for sponsor

```markdown
# Sponsor Wrap: <Brand> on <Show> — <Quarter>

## Insertions
- Episode 42 (mid-roll, host-read, 75s) — 8,200 impressions
- Episode 43 (mid-roll, host-read, 80s) — 7,900 impressions
- Episode 44 (mid-roll, host-read, 78s) — 8,400 impressions

## Total
- Impressions: 24,500
- Click-throughs: 612 (CTR 2.5%)
- Code redemptions: 89
- Attributable revenue: $4,200 (avg basket $47)

## ROI
- Sponsor spend: $1,800 (CPM $73)
- Sponsor return: $4,200
- ROI: 2.3×

## Recommended for renewal: YES
- Renewal pitch: 4-episode block at same CPM with 1 free episode for repeat-partner discount
```

## Examples

### Example 1: New sponsor onboarded mid-quarter

**Goal:** Brand wants 4-episode mid-roll campaign Q3.

**Steps:**
1. Brand briefs deliverables + budget via `creator-collab-brand-partnership-briefing` skill.
2. Recipe 6: translate brand-supplied copy to host voice.
3. Recipe 1: write 4 versions (1 per episode); avoid repetition.
4. Record each during episode prep.
5. Recipe 3 or 5: configure DAI insertion in podcast host for the 4 episodes.
6. Recipe 7: track clicks + conversions weekly.
7. Recipe 12: wrap report at quarter end.

**Result:** $1,800 quarterly sponsor deal with 2.3× ROI, pitched for renewal.

### Example 2: Pre-roll + mid-roll bundle for hero sponsor

**Goal:** Single sponsor wants both pre-roll (reach) and mid-roll (recall).

**Steps:**
1. Recipe 1: write 2 different scripts (30s pre-roll + 75s mid-roll); not copy-paste.
2. Recipe 8: charge bundle CPM: $25 + $40 = $65 CPM.
3. Recipe 3: configure two DAI insertions; one pre-roll, one mid-roll, both linked to same code.
4. Recipe 10: single disclosure works for both.

**Result:** Higher per-episode revenue from one sponsor without overstuffing the episode.

### Example 3: Network bundle pitch

**Goal:** Operator with 3 shows wants to bundle sponsorships.

**Steps:**
1. Recipe 9: build network bundle structure — 3 shows × 4 episodes × mid-roll = 12 impressions.
2. Total downloads across 3 shows × episodes: ~120k.
3. Pitch: $4,500 for the 12-insertion bundle (CPM $37.50 vs solo CPM $40).
4. Sign; configure DAI across 3 hosts; report per-show stats + roll-up.

**Result:** Higher absolute revenue for operator + lower per-impression cost for brand.

## Edge cases / gotchas

- **Host-read = 4× recall vs voiced ad** — host's voice tied to listener trust. Don't sub a brand-supplied VO.
- **Read it once first, then record.** Multiple takes sound rehearsed and tank recall.
- **DAI placement varies per host.** Buzzsprout / Captivate / Transistor / Megaphone all have different APIs and slot rules.
- **Mid-roll insertion is best implemented BAKED INTO MASTER**, not as DAI overlay — DAI overlays jar the listening experience.
- **DAI works best for pre-roll and post-roll** (clean cut-points). Mid-roll DAI is rough on most hosts.
- **Code uniqueness per show** — give each show its own code for accurate attribution.
- **UTM-tag the URL** — same code may not be enough; URL with `utm_source=podcast&utm_medium=host-read&utm_campaign=ep042` gives per-episode attribution.
- **Don't accept exclusivity beyond 90 days** for category exclusivity — kills your pipeline.
- **Disclose at the top, not after the read** — FTC compliance + listener trust.
- **CPM benchmarks vary by niche**: niche B2B podcasts command $50-100 CPM; general consumer might be $15-25.
- **Don't run 3+ sponsor reads in a 30-min episode** — listener fatigue tanks completion rate.
- **Don't read for products you wouldn't use** — audience detects fake endorsement; long-term trust loss > short-term sponsor revenue.
- **Megaphone is enterprise-only** ($1k+/mo); for indie shows Buzzsprout / Captivate / Transistor are the standard.
- **Sponsor scripts more than 90s tank completion**. Tight is better.
- **Always wrap-report.** 2-3× ROI gets renewals; renewals are 10× cheaper than new-sponsor acquisition.
- **Disclosure language differs per platform** — Apple Podcasts vs Spotify vs YouTube vs RSS — same disclosure works everywhere if it's verbal + named.

## Sources

- [ThoughtLeaders — Podcast trends 2026 (host-read 4× recall)](https://www.thoughtleaders.io/blog/podcast-trends-2026)
- [Best podcast hosting 2026 (Podosphere)](https://www.thepodosphere.com/blog/best-podcast-hosting-platforms-2026-comparison-guide)
- [Buzzsprout API](https://github.com/Buzzsprout/buzzsprout-api)
- [Captivate API](https://captivate.fm/help/api)
- [Transistor API](https://developers.transistor.fm/)
- [Megaphone Enterprise](https://megaphone.spotify.com/)
- [FTC influencer disclosures 101](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers)
- [Podcast sponsorship CPM benchmarks](https://rss.com/blog/best-podcast-hosting-platforms/)
