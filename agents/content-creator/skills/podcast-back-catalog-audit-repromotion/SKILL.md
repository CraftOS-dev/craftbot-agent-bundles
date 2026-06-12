---
name: podcast-back-catalog-audit-repromotion
description: Audit the back catalog — find top-N evergreen episodes by listens; repurpose via Castmagic into LinkedIn / X / blog derivatives; re-audiogram via Headliner; Buffer cascade. Use when episodes 12+ months old still get listens but stop getting promoted, or when a host wants to wring more value from existing inventory before recording new episodes.
---

# Podcast back-catalog audit + re-promotion

## When to use

Reach for this skill when the user says: "audit my back catalog", "which old episodes still get listens?", "re-promote old episodes", "evergreen podcast content", "we have 150 episodes and only push the new one", "rescue the back catalog", "long-tail listens", or "what should I re-share on social?". Pair with `repurposing-pipeline-1-to-10` for the derivative chain itself. Pair with `content-analytics-retention-open-rates-chartable` for the listening data. Skip for podcasts <20 episodes — too little catalog to audit.

## Setup

```bash
# Podcast hosting APIs (pick what user has)
# Buzzsprout, Captivate, Transistor, Megaphone, Acast, RSS.com — pure REST per platform
# Spotify for Podcasters / Apple Podcasts Connect — manual CSV export (no API as of June 2026)

# Castmagic for transcript → derivatives
# Headliner for audiogram regeneration (RSS-monitored autopilot covers new but you need manual for catalog)
# Buffer GraphQL + MCP for cross-platform scheduling
npx -y @buffer/mcp-server --help

# Local analytics rollup
pip install pandas
```

Auth / env vars:
- `BUZZSPROUT_API_TOKEN` + `BUZZSPROUT_PODCAST_ID` — Buzzsprout settings → API. Paid.
- `CAPTIVATE_API_KEY` + `CAPTIVATE_USER_ID` — Captivate Dashboard → API.
- `TRANSISTOR_API_KEY` + `TRANSISTOR_SHOW_ID` — Transistor Settings.
- `CASTMAGIC_API_KEY` — Castmagic Dashboard → API.
- `HEADLINER_API_TOKEN` — Headliner has limited public API; mostly RSS-autopilot.
- `BUFFER_ACCESS_TOKEN` — Buffer Personal Access Token.
- `OPUSCLIP_API_KEY` — for re-cutting clips from old video episodes if needed.

## Common recipes

### Recipe 1: Pull all episodes from podcast host (Buzzsprout example)

```bash
# Buzzsprout — all episodes (paginated)
curl -s "https://www.buzzsprout.com/api/${BUZZSPROUT_PODCAST_ID}/episodes.json" \
  -H "Authorization: Token token=$BUZZSPROUT_API_TOKEN" \
  > episodes.json

# Captivate
curl -s "https://api.captivate.fm/shows/$CAPTIVATE_SHOW_ID/episodes" \
  -H "Authorization: Bearer $CAPTIVATE_API_KEY" \
  > episodes.json

# Transistor
curl -s "https://api.transistor.fm/v1/episodes?show_id=$TRANSISTOR_SHOW_ID&pagination[per]=200" \
  -H "x-api-key: $TRANSISTOR_API_KEY" \
  > episodes.json
```

### Recipe 2: Identify top-N evergreen — sort by all-time downloads / age ratio

```python
import json, pandas as pd
from datetime import datetime, timezone

with open('episodes.json') as f:
    eps = json.load(f)

df = pd.DataFrame(eps)
df['published_at'] = pd.to_datetime(df['published_at'])
df['age_days'] = (datetime.now(timezone.utc) - df['published_at']).dt.days

# Filter: at least 90 days old (we want catalog, not new releases)
catalog = df[df['age_days'] >= 90].copy()

# Evergreen score: downloads_per_day_since_publish (high = sustained interest)
catalog['daily_listens'] = catalog['total_plays'] / catalog['age_days'].clip(lower=1)

# Top 10 evergreen
top = catalog.sort_values('daily_listens', ascending=False).head(10)
print(top[['title','total_plays','age_days','daily_listens']])

# Also: top-N by last-30d listens (the actually-still-trending ones)
catalog['recent_listens_30d'] = catalog.get('recent_plays', catalog['total_plays'] * 0)
trending = catalog.sort_values('recent_listens_30d', ascending=False).head(10)
```

### Recipe 3: Cross-platform listen rollup (Apple + Spotify exports)

```bash
# Manual export from Apple Podcasts Connect → CSV; same from Spotify for Podcasters
# Roll up in a single sheet
python -c "
import pandas as pd
apple = pd.read_csv('apple-listens.csv')
spotify = pd.read_csv('spotify-listens.csv')
host = pd.read_json('episodes.json')

# Match on title or guid
merged = host[['title','guid','total_plays']].merge(apple[['title','plays']].rename(columns={'plays':'apple'}), on='title', how='left')
merged = merged.merge(spotify[['title','starts']].rename(columns={'starts':'spotify'}), on='title', how='left')
merged['true_reach'] = merged[['total_plays','apple','spotify']].sum(axis=1)
merged.sort_values('true_reach', ascending=False).head(20).to_csv('cross-platform-top20.csv', index=False)
"
```

Cross-platform aggregation matters — host-side counts often miss Apple/Spotify private listens.

### Recipe 4: Identify "lost gems" — high-quality, low-promoted

```python
# Combine listen-through rate (LTR) with promotion count
# Episodes with high LTR but low recent share count = lost gems
df['promotion_score'] = df['recent_listens_30d'] / df['total_plays']  # 0 = forgotten
df['quality_score'] = df.get('completion_rate', 0.5)

# Lost gems: high quality, low promotion
lost_gems = df[(df['quality_score'] > 0.6) & (df['promotion_score'] < 0.05)].sort_values('quality_score', ascending=False).head(10)
```

### Recipe 5: Castmagic re-process — generate fresh derivatives from old episode

```bash
# Castmagic generates show notes + X thread + LinkedIn post + blog from transcript
curl -X POST 'https://api.castmagic.io/v1/projects' \
  -H "Authorization: Bearer $CASTMAGIC_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Re-promote Ep 42: SSO deep-dive",
    "media_url": "https://media.acme.com/podcast/ep-42.mp3",
    "generate": ["show_notes", "x_thread", "linkedin_post", "blog_post", "quote_graphics"]
  }'

# Fetch derivatives once processing completes
curl -s "https://api.castmagic.io/v1/projects/<project_id>/outputs" \
  -H "Authorization: Bearer $CASTMAGIC_API_KEY"
```

### Recipe 6: Headliner — generate fresh audiogram for an old episode

Headliner has no documented public API as of June 2026. Workflow:

1. Upload episode MP3 to Headliner dashboard.
2. Use "AI clipping" to find 3-5 quotable moments.
3. Apply current branded template (likely updated since the original episode).
4. Export 9:16 + 1:1 versions.

ffmpeg fallback (Recipe 8 in `audiogram-headliner-wavve` skill from this same agent bundle):

```bash
ffmpeg -i ep-42-quote-clip.mp3 \
  -i branded_background_2026.png \
  -filter_complex "[0:a]showwaves=s=1080x200:colors=white:mode=line:rate=30,format=rgba[wave];[1:v]scale=1080:1920[bg];[bg][wave]overlay=0:1700[out]" \
  -map "[out]" -map 0:a -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 192k -t 60 \
  ep-42-audiogram-2026.mp4
```

### Recipe 7: Buffer cascade — schedule re-promotion across platforms

```bash
# Schedule a LinkedIn post + X thread + Reels audiogram across 3 days
npx @buffer/mcp-server query \
  --tool create_update \
  --args '{
    "profile_ids": ["LINKEDIN_PROFILE_ID","TWITTER_PROFILE_ID"],
    "text": "Three years ago we recorded the SSO deep-dive ... 🎧 Listen → https://acme.fm/ep-42",
    "scheduled_at": "2026-06-12T14:00:00Z"
  }'

# Audiogram to Instagram Reels + TikTok via Buffer
npx @buffer/mcp-server query \
  --tool create_update \
  --args '{
    "profile_ids": ["INSTAGRAM_PROFILE_ID","TIKTOK_PROFILE_ID"],
    "media_url": "https://media.acme.com/audiograms/ep-42-2026.mp4",
    "text": "🔁 From the back catalog — SSO without tears",
    "scheduled_at": "2026-06-13T16:00:00Z"
  }'
```

### Recipe 8: Update old episode metadata for SEO refresh

```bash
# Buzzsprout — patch episode title + description with refreshed long-tail keywords
curl -X PATCH "https://www.buzzsprout.com/api/${BUZZSPROUT_PODCAST_ID}/episodes/<episode_id>.json" \
  -H "Authorization: Token token=$BUZZSPROUT_API_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "SSO Without Tears: Okta, Auth0, Azure AD — 2026 update",
    "description": "Three years on, our SSO deep-dive still ranks. Updated 2026 with current IdP integrations and SCIM patterns.",
    "summary": "Updated 2026 — Okta, Auth0, Azure AD SAML + SCIM integration patterns."
  }'

# Captivate
curl -X POST 'https://api.captivate.fm/episodes/<episode_id>' \
  -H "Authorization: Bearer $CAPTIVATE_API_KEY" \
  -d '{"title":"...", "shownotes":"..."}'
```

### Recipe 9: Add "Updated 2026" badge to refreshed show notes

```markdown
---
title: "Ep 42: SSO Without Tears"
updated_in: "2026-06"
original_publish_date: "2023-04-15"
---

> 🔄 **Updated June 2026** — Original episode from April 2023. Show notes refreshed with current IdP integrations (Okta 2025+ admin panel, Auth0 2026 universal login, Azure AD's renamed admin UX).

## Episode Summary
...
```

Helps SEO + listener trust.

### Recipe 10: Repromotion cadence — top-10 evergreen on rotation

```python
# Build a re-promotion calendar — top-10 evergreen each get promoted once per month rotation
import pandas as pd
from datetime import datetime, timedelta

top10 = pd.read_csv('top-evergreen.csv').head(10).to_dict('records')
start = datetime(2026, 6, 15)
schedule = []
for i, ep in enumerate(top10):
    schedule.append({
        'date': (start + timedelta(days=3*i)).isoformat(),
        'title': ep['title'],
        'platforms': ['linkedin','twitter','instagram'],
        'asset_type': 'audiogram' if i % 2 == 0 else 'quote_graphic'
    })

# Push to Notion editorial DB or Buffer cascade
import json; print(json.dumps(schedule, indent=2))
```

### Recipe 11: Identify dead episodes (candidate for unpublish or archive)

```python
# Episodes with <100 lifetime listens after 12+ months = dead weight in feed
dead = df[(df['age_days'] > 365) & (df['total_plays'] < 100)]

# Consider unpublishing (or marking as "archive only"); keeps feed lean
```

Don't auto-unpublish — review with the host; may be intentional in-flight.

## Examples

### Example 1: Quarterly back-catalog audit + re-promotion plan

**Goal:** Host has 80 episodes; ID top-10 evergreen, build a 90-day re-promotion calendar.

**Steps:**
1. Pull all episodes (Recipe 1).
2. Sort by daily_listens (Recipe 2).
3. Cross-reference with Apple + Spotify exports for true reach (Recipe 3).
4. Identify "lost gems" — high quality, low recent promotion (Recipe 4).
5. Castmagic-process each (Recipe 5).
6. Refresh audiograms for current brand (Recipe 6).
7. Build 90-day calendar (Recipe 10).
8. Push schedule to Buffer (Recipe 7).
9. Optionally refresh metadata + show notes with "Updated 2026" badge (Recipes 8-9).

**Result:** 10 evergreen episodes get fresh life on social; ~25% lift in catalog listens over 90 days.

### Example 2: Find lost-gem SSO episode to re-promote alongside new SSO release

**Goal:** Product just shipped SSO v2; host has an old SSO episode worth re-surfacing.

**Steps:**
1. Filter catalog for episodes tagged or titled with "SSO".
2. Score by quality (LTR > 60%) + recent-promotion-decay.
3. Castmagic-process the highest-scoring episode (Recipe 5).
4. Refresh show notes with "Updated 2026" SSO v2 context (Recipe 9).
5. Schedule cross-platform re-promo aligned with product launch week.

**Result:** Old episode rides the product launch coverage; double-dips on attention.

### Example 3: Identify dead episodes to clean up feed bloat

**Goal:** 200-episode catalog feels overwhelming; want to slim down.

**Steps:**
1. Pull all episodes (Recipe 1).
2. Run Recipe 11 for dead-weight candidates.
3. Review with host; archive (not delete) any agreed.
4. Update RSS to exclude archived; keep show-notes pages live for SEO.

**Result:** Cleaner feed for new subscribers; SEO preserved.

## Edge cases / gotchas

- **Host-side download counts are inflated by bots** — Apple Podcasts Connect "unique listeners" is more honest than RSS host's "downloads". Cross-reference (Recipe 3).
- **Spotify for Podcasters has no API** — manual CSV export only as of June 2026. Schedule monthly export into Notion / sheet.
- **Apple Podcasts Connect has no API** — same constraint. Manual export required.
- **Chartable + Podtrac** for cross-platform aggregation (paid). Use if budget supports it.
- **"Listens" vs "downloads"** — `total_plays` from RSS hosts = downloads. Apple `played` = actual listens. Be specific in reports.
- **Don't auto-PATCH old episode titles** — RSS-cached title changes confuse subscribers' players. Host edits, then warn audience.
- **Headliner has no public API** — manual workflow or RSS-autopilot only-for-new-episodes. ffmpeg fallback covers older episodes.
- **Castmagic costs $$** — per-minute pricing; budget cap when batch-processing old episodes. Start with top-10 only.
- **Show-notes URL changes break inbound links** — if updating slugs, add redirects. Inherits `kb-taxonomy-design` redirect-map discipline.
- **GUID changes break subscriber listening history** — never change episode GUIDs. PATCH metadata, not GUID.
- **Buffer cascade rate limits** — Pro tier needed for >10 posts/day across profiles.
- **Don't re-promote evergreen too often** — 1×/quarter per episode max; otherwise stale.
- **Refresh social-share image + headline** — platforms penalize obvious reposts; new audiogram + headline reads as a new asset.
- **YouTube old episodes** — re-upload as separate "Shorts" cuts via OpusClip; don't replace originals (loses lifetime metrics).

## Sources

- [Buzzsprout API](https://github.com/Buzzsprout/buzzsprout-api)
- [Captivate API](https://captivate.fm/api)
- [Transistor API](https://developers.transistor.fm/)
- [Megaphone API](https://developers.megaphone.fm/)
- [Castmagic — best-of-2026 podcast tools](https://stormy.ai/blog/best-gpt-repurposing-tools-2026-opusclip-munch-castmagic)
- [Headliner Pro RSS autopilot](https://www.headliner.app/podcasters)
- [Buffer GraphQL + MCP](https://mcpmarket.com/server/buffer)
- [Spotify for Podcasters Analytics](https://podcasters.spotify.com/dashboard)
- [Apple Podcasts Connect Analytics](https://help.apple.com/itc/podcasts_connect/#/itca0a18256d)
- [Chartable cross-platform podcast measurement](https://chartable.com/)
- [Podtrac cross-platform measurement](https://podtrac.com/)
- [Best podcast hosting platforms 2026 comparison](https://www.thepodosphere.com/blog/best-podcast-hosting-platforms-2026-comparison-guide)
- [Evergreen content strategy for podcasts](https://www.thespearpoint.com/blog/seo-for-podcasts)
- [ffmpeg `showwaves` filter](https://ffmpeg.org/ffmpeg-filters.html#showwaves)
