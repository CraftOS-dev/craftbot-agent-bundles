<!--
Source: https://buffer.com/developers/api
Buffer MCP: https://github.com/bufferapp/buffer-mcp (Feb 2026 GA)
-->
# Buffer Cross-Platform Publishing — SKILL

One auth → cascade publish to LinkedIn, X, Threads, Bluesky, Instagram, TikTok, Facebook, Pinterest, Mastodon, YouTube Shorts. Buffer's GraphQL + MCP went public beta Feb 2026 and is the SOTA way to ship a single piece of content with platform-native variants without managing 10 auth flows.

## When to use this skill

- **Scheduled posting to >=2 platforms** — anything other than a single ad-hoc post on one channel. Buffer's queue is faster than orchestrating per-platform MCPs.
- **Content cascade strategy** — primary on LinkedIn, derivatives on X / Threads / Bluesky / Mastodon with platform-specific edits.
- **Team / advocacy programs** — Buffer organizes channels per team-member account; one cascade across executive accounts.
- **Editorial calendar to queue** — Notion calendar → Buffer queue via GraphQL `createUpdate`.

**Do NOT use this skill when:**
- You need a feature only the native API supports (e.g., X polls, LinkedIn Carousel documents — those go via `twitter-mcp` and `linkedin-marketing-api` skill).
- You need real-time DM / inbox automation (Buffer is publishing-only).
- Publishing a single post to a single platform — call the native MCP directly.

## Setup

### Buffer MCP install (cli-anything)

```bash
# Install the Buffer MCP server (Feb 2026 GA)
npx -y @buffer/mcp-server@latest
```

### Auth

Buffer uses Personal Access Tokens. Generate at https://publish.buffer.com/account/apps:

```bash
export BUFFER_ACCESS_TOKEN="<pat>"
# Optional org ID for team accounts
export BUFFER_ORGANIZATION_ID="<org-uuid>"
```

The MCP server reads `BUFFER_ACCESS_TOKEN` from env on start.

### Channel IDs (one-time discovery)

List connected channels to map platform names → channel IDs:

```bash
# Via Buffer MCP
mcp tool buffer.list_channels

# Or direct GraphQL
curl -X POST https://graph.buffer.com/v1 \
  -H "Authorization: Bearer $BUFFER_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ channels { id name service serviceType } }"}'
```

Store the mapping in `.buffer-channels.json`:

```json
{
  "linkedin_company": "5f8c1a...",
  "linkedin_executive": "5f8c1b...",
  "twitter": "5f8c1c...",
  "threads": "5f8c1d...",
  "bluesky": "5f8c1e...",
  "instagram": "5f8c1f...",
  "tiktok": "5f8c20...",
  "facebook": "5f8c21...",
  "youtube_shorts": "5f8c22..."
}
```

## Common recipes

### Recipe 1: Single post → cascade with platform variants

Buffer accepts per-channel text overrides on the same `createUpdate` mutation:

```bash
mcp tool buffer.create_update \
  --channelIds '["linkedin_company","twitter","threads","bluesky"]' \
  --text 'Default text (LinkedIn — long-form OK).' \
  --channelData '{
    "twitter": {"text":"Tweet-length, with #hashtags and @mention."},
    "threads": {"text":"Threads-native, conversational tone."},
    "bluesky": {"text":"Bluesky-native, includes alt:🏷"}
  }' \
  --scheduledAt "2026-06-12T14:00:00Z"
```

GraphQL equivalent:

```graphql
mutation CreatePost {
  createUpdate(input: {
    channelIds: ["chan_linkedin_company","chan_twitter","chan_threads","chan_bluesky"]
    text: "Default text"
    channelData: [
      { channelId: "chan_twitter", text: "Tweet variant" }
      { channelId: "chan_threads", text: "Threads variant" }
    ]
    scheduledAt: "2026-06-12T14:00:00Z"
  }) {
    id
    status
    channelUpdates { channelId scheduledAt }
  }
}
```

### Recipe 2: Image post (single image, all platforms)

Buffer accepts public image URLs (S3, CDN, Cloudinary). For Notion-stored images, use a CDN-fronted public URL.

```bash
mcp tool buffer.create_update \
  --channelIds '["instagram","facebook","linkedin_company"]' \
  --text 'Caption text. Alt text below.' \
  --mediaUrls '["https://cdn.example.com/img/abc.jpg"]' \
  --altText 'Descriptive alt for screen readers.'
```

### Recipe 3: Video / Reel (TikTok, IG Reel, YouTube Shorts cascade)

Vertical 9:16 video required. Buffer uploads to each platform; YouTube Shorts requires the channel be connected with publishing scope.

```bash
mcp tool buffer.create_update \
  --channelIds '["tiktok","instagram_reels","youtube_shorts"]' \
  --text 'Video caption.' \
  --mediaUrls '["https://cdn.example.com/vid/abc.mp4"]' \
  --channelData '{
    "tiktok": {"text":"Caption with #fyp #trending"},
    "instagram_reels": {"text":"Caption + 5 niche hashtags"},
    "youtube_shorts": {"text":"Shorts title (max 100 chars)"}
  }'
```

### Recipe 4: Queue from Notion editorial calendar

1. `notion-mcp` query the editorial calendar database for entries with `status = "Approved"` and `scheduled_at >= now`.
2. For each row, call `buffer.create_update` with the row's `channels`, `text`, `media_urls`, `scheduled_at`.
3. On success, `notion-mcp` update row `status = "Scheduled"` and store `buffer_update_id`.
4. Daily cron via `cli-anything` re-syncs in case calendar changes.

```python
# Pseudo-flow run via cli-anything python -c
for row in notion.query(db_id, filter={status:'Approved'}):
    update = buffer.create_update(
        channelIds=row['channels'],
        text=row['text'],
        mediaUrls=row['media_urls'] or [],
        scheduledAt=row['scheduled_at'],
        channelData=row.get('channel_variants', {}),
    )
    notion.update_page(row['id'], {'status':'Scheduled', 'buffer_id': update['id']})
```

### Recipe 5: Cancel / reschedule / delete

```bash
# Reschedule
mcp tool buffer.update_update \
  --id "<update_id>" \
  --scheduledAt "2026-06-14T09:00:00Z"

# Delete
mcp tool buffer.delete_update --id "<update_id>"
```

### Recipe 6: Get analytics per post

```bash
mcp tool buffer.get_update_analytics --id "<update_id>"
# Returns: impressions, clicks, engagements, reach per channel
```

### Recipe 7: Cascade with hashtag-mix strategy (per platform)

```python
HASHTAG_MIX = {
    'twitter':   ['#startup','#growth','#marketing'],          # 3 max, sparingly
    'instagram': ['#startup','#growth','#marketing'] + niche10 + branded3,  # 16 max
    'tiktok':    ['#fyp','#smallbusiness','#growthhacking'] + trending3,
    'linkedin_company': [],                                    # LinkedIn doesn't reward hashtags
    'threads':   ['#startup','#growth'],
}
```

## Examples

### Example A: Product launch cascade (LinkedIn-first)

```yaml
# editorial-calendar.yaml
launch_post:
  primary: linkedin_company
  variants:
    linkedin_company:
      text: |
        We just launched X. Here's why this matters: (3 paragraph long-form)
      media: launch-hero.jpg
    twitter:
      text: "Just shipped X. The 3 biggest things: 1/ ... 2/ ... 3/ ...  Read more: <bitly-link>"
      media: launch-hero.jpg
    threads:
      text: "Launch day. We built X to solve <problem>. Here's the journey..."
      media: launch-hero.jpg
    bluesky:
      text: "X is live. <one-line value prop>. <bitly-link>"
      media: launch-hero.jpg
    instagram:
      text: "X is here. <hook>. <CTA>. #productlaunch #startup #saas #growth #marketing"
      media: launch-hero-square.jpg
```

Run:

```bash
cat editorial-calendar.yaml | yq '.launch_post' | \
  mcp tool buffer.create_update_from_yaml --scheduledAt "2026-06-15T14:00:00Z"
```

### Example B: Weekly newsletter promotion cascade

Run every Monday at 9am via cron-style schedule:

```bash
mcp tool buffer.create_update \
  --channelIds '["linkedin_company","twitter","threads"]' \
  --text "This week's newsletter: <topic>. Read: <link>" \
  --scheduledAt "next Monday 09:00 UTC"
```

## Edge cases

### Rate limits
Buffer GraphQL: 60 req/min per token. For bulk queue ops (>1000 posts), use `bulk_create_updates` mutation (max 500 per call).

### Platform-specific gotchas
- **LinkedIn**: Buffer can publish to company pages and executive personal profiles, but for image documents / PDFs / carousels, use the `linkedin-marketing-api` skill (Buffer doesn't support multi-page documents).
- **X/Twitter**: Buffer respects the 280-char limit; longer text is truncated. Use `channelData.twitter.text` to override.
- **Instagram**: First image only on feed posts. Carousels need >=2 image URLs; Buffer supports up to 10.
- **TikTok**: Video must be uploaded to Buffer Drive first or accessible via public CDN. Buffer doesn't render captions on-video.
- **Threads**: Max 500 chars. Buffer truncates.
- **Bluesky**: Max 300 chars. Buffer truncates. Custom domain handles must be pre-verified in Buffer.
- **YouTube Shorts**: Requires YouTube channel connection with publishing scope. Buffer cannot publish long-form YouTube — only Shorts.

### Failure modes
- **403 on channel**: token doesn't have access to that channel. Re-auth via Buffer UI.
- **422 on text**: per-platform char limit hit; check `channelData` overrides.
- **Image URL fetch fail**: Buffer fetches images server-side; URL must be public + CDN-stable.
- **Schedule in past**: Buffer rejects. Round up to current time + 5 min.
- **Scheduled but not published**: check channel queue at https://publish.buffer.com/queue — channel may be paused.

### Buffer plan limits
- **Free**: 3 channels, 10 queued posts/channel. Not enough for cascade.
- **Essentials ($6/channel/mo)**: 1 user, unlimited posts.
- **Team ($12/channel/mo)**: multi-user, approval flows.
- **Agency**: white-label.

For a marketing-agent deployment, Team plan minimum.

## Sources

- **Buffer GraphQL API**: https://buffer.com/developers/api
- **Buffer MCP server**: https://github.com/bufferapp/buffer-mcp (Feb 2026 GA)
- **Channel-specific limits**: https://support.buffer.com/article/501-which-social-media-platforms-can-i-use-with-buffer
- **Rate limits**: https://buffer.com/developers/api/rate-limits
