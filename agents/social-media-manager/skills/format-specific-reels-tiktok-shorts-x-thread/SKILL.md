<!--
Source: https://developers.facebook.com/docs/instagram-platform/reels/
TikTok Content API: https://developers.tiktok.com/doc/content-posting-api-get-started/
YouTube Shorts: https://developers.google.com/youtube/v3
X (Twitter) API v2: https://developer.twitter.com/en/docs/twitter-api
LinkedIn carousel doc: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/community-management/shares/document-share
-->
# Format-Specific Publishing — Reels / TikTok / Shorts / X Thread / LinkedIn Carousel — SKILL

Each platform's flagship format has spec quirks Buffer hides. This skill handles native-only features: TikTok product-tagged Shop video, IG Reel with sticker + product tag, YouTube Shorts with end-screen, X thread with media-per-tweet, LinkedIn document carousel (100-page PDF via Marketing API URN flow). Use after `platform-native-content-creation` to add format-specific extras.

## When to use this skill

- **TikTok Shop video** with product tags + Live Shopping link.
- **IG Reel** with collab partner, music sticker, product tag, location tag.
- **YouTube Shorts** with end-screen + Shorts shelf optimization.
- **X thread** with media on each tweet, scheduled per-post.
- **LinkedIn document carousel** (PDF upload, 100 pages max — Buffer can't do this).
- **Bluesky reply chains** with embed-quote.

**Do NOT use this skill when:**
- Simple cross-platform cascade — use `community-engagement-comments-dms-at-scale` Buffer recipes.
- Trend video where format is whatever sound demands — `social-trend-monitoring-tiktok-sounds-reels`.
- Story / ephemeral content — IG / FB Stories via `insta-business-mcp`.

## Setup

### TikTok Content Posting API

```bash
export TIKTOK_ACCESS_TOKEN="<token>"
# Endpoint: https://open.tiktokapis.com/v2/post/publish/video/init/
# Requires: TikTok for Business + Content Posting API approval (1-2 weeks)
```

### Instagram Graph API (Business / Creator)

```bash
export META_GRAPH_TOKEN="<token>"
export IG_BUSINESS_ID="<id>"
# Endpoint: https://graph.facebook.com/v20.0/
```

Native MCP: `insta-business-mcp` covers most calls.

### YouTube Data API v3

```bash
export YOUTUBE_API_KEY="<key>"
export YOUTUBE_CHANNEL_ID="<id>"
# Endpoint: https://www.googleapis.com/youtube/v3/
```

Native MCP: `youtube-mcp`.

### LinkedIn Marketing API

```bash
export LINKEDIN_ACCESS_TOKEN="<oauth-token>"
export LINKEDIN_ORG_URN="urn:li:organization:<id>"
# Endpoint: https://api.linkedin.com/rest/
# Requires: LinkedIn Marketing Developer Platform approval
```

### X API v2

```bash
export X_BEARER_TOKEN="<token>"
# Endpoint: https://api.twitter.com/2/
```

Native MCP: `twitter-mcp`.

## Common recipes

### Recipe 1: TikTok video with caption + cover + product tag

TikTok's two-step upload:

```bash
# 1. Init upload
curl -X POST https://open.tiktokapis.com/v2/post/publish/video/init/ \
  -H "Authorization: Bearer $TIKTOK_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "post_info": {
      "title": "Keyword-front-loaded caption (100-150 chars)",
      "privacy_level": "MUTUAL_FOLLOW_FRIENDS",
      "disable_duet": false,
      "disable_comment": false,
      "disable_stitch": false,
      "video_cover_timestamp_ms": 1000
    },
    "source_info": {
      "source": "PULL_FROM_URL",
      "video_url": "https://cdn.example.com/vid/abc.mp4"
    }
  }'
# Returns: {data: {publish_id, upload_url}}

# 2. Poll status
curl -G "https://open.tiktokapis.com/v2/post/publish/status/fetch/" \
  -H "Authorization: Bearer $TIKTOK_ACCESS_TOKEN" \
  --data-urlencode "publish_id=<id>"
```

For Shop product tag, use TikTok Shop API (see `social-commerce-tiktok-instagram-pinterest-shops`).

### Recipe 2: IG Reel publish with music + cover

```bash
# Step 1: create media container
curl -X POST "https://graph.facebook.com/v20.0/$IG_BUSINESS_ID/media" \
  -d "media_type=REELS" \
  -d "video_url=https://cdn.example.com/vid/abc.mp4" \
  -d "caption=Reel caption with hashtags" \
  -d "cover_url=https://cdn.example.com/cover.jpg" \
  -d "share_to_feed=true" \
  -d "audio_name=Trending Sound Name" \
  -d "access_token=$META_GRAPH_TOKEN"
# Returns: {id: "container_id"}

# Step 2: publish
curl -X POST "https://graph.facebook.com/v20.0/$IG_BUSINESS_ID/media_publish" \
  -d "creation_id=<container_id>" \
  -d "access_token=$META_GRAPH_TOKEN"
```

### Recipe 3: IG carousel with product tags

```bash
# Per-image: create child containers with product_tags
for img in $IMAGES; do
  curl -X POST "https://graph.facebook.com/v20.0/$IG_BUSINESS_ID/media" \
    -d "image_url=$img" \
    -d "is_carousel_item=true" \
    -d "product_tags=[{\"product_id\":\"$PROD_ID\",\"x\":0.5,\"y\":0.5}]" \
    -d "access_token=$META_GRAPH_TOKEN"
done

# Combine into carousel container
curl -X POST "https://graph.facebook.com/v20.0/$IG_BUSINESS_ID/media" \
  -d "media_type=CAROUSEL" \
  -d "children=$CHILD_IDS_COMMA_SEPARATED" \
  -d "caption=Carousel caption" \
  -d "access_token=$META_GRAPH_TOKEN"

# Publish carousel
curl -X POST "https://graph.facebook.com/v20.0/$IG_BUSINESS_ID/media_publish" \
  -d "creation_id=<carousel_container>" \
  -d "access_token=$META_GRAPH_TOKEN"
```

### Recipe 4: YouTube Shorts upload with metadata

```bash
# Resumable upload (use youtube-mcp wrapper)
mcp tool youtube.upload_video \
  --file_path "shorts.mp4" \
  --title "Shorts title (max 100 chars)" \
  --description "Description, first 100 chars critical. #Shorts #brand" \
  --category_id "22" \
  --tags '["shorts","brand","topic"]' \
  --privacy_status "public" \
  --made_for_kids false
```

YouTube auto-detects vertical 9:16 < 60s as Shorts. Include `#Shorts` in title or description for Shorts shelf placement.

### Recipe 5: X thread (multi-tweet with media)

```bash
# Tweet 1 (no in_reply_to)
RESPONSE=$(curl -X POST https://api.twitter.com/2/tweets \
  -H "Authorization: Bearer $X_BEARER_TOKEN" \
  -d '{"text":"1/ Hook line for thread.","media":{"media_ids":["<media_id_1>"]}}')
T1_ID=$(echo "$RESPONSE" | jq -r '.data.id')

# Tweet 2 (reply to T1)
curl -X POST https://api.twitter.com/2/tweets \
  -H "Authorization: Bearer $X_BEARER_TOKEN" \
  -d "{\"text\":\"2/ Second point.\",\"reply\":{\"in_reply_to_tweet_id\":\"$T1_ID\"}}"
# ...repeat for 3..N
```

Or via `twitter-mcp`:

```bash
mcp tool twitter.create_thread \
  --tweets '[
    {"text":"1/ Hook.","media_ids":["m1"]},
    {"text":"2/ Point 2.","media_ids":["m2"]},
    {"text":"3/ Point 3."},
    {"text":"4/ Lesson + CTA."}
  ]'
```

### Recipe 6: LinkedIn document carousel (100-page PDF)

LinkedIn's URN-based 2-step:

```bash
# Step 1: register upload
curl -X POST https://api.linkedin.com/rest/documents?action=initializeUpload \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "LinkedIn-Version: 202506" \
  -d "{
    \"initializeUploadRequest\": {
      \"owner\":\"$LINKEDIN_ORG_URN\"
    }
  }"
# Returns: {value: {uploadUrl, document}}

# Step 2: PUT the PDF bytes to uploadUrl
curl -X PUT "<uploadUrl>" \
  -H "Content-Type: application/pdf" \
  --data-binary @carousel.pdf

# Step 3: create post referencing the document URN
curl -X POST https://api.linkedin.com/rest/posts \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202506" \
  -d "{
    \"author\":\"$LINKEDIN_ORG_URN\",
    \"commentary\":\"Carousel caption — hook in first 210 chars.\",
    \"visibility\":\"PUBLIC\",
    \"distribution\":{\"feedDistribution\":\"MAIN_FEED\"},
    \"content\":{
      \"media\":{
        \"id\":\"<document_urn>\",
        \"title\":\"Carousel deck title\"
      }
    },
    \"lifecycleState\":\"PUBLISHED\"
  }"
```

### Recipe 7: Threads chain via Buffer or native

Buffer publishes a single Threads post. For chain, fall back to Threads native (when Threads API exposes chain endpoint, currently scrape via Playwright):

```bash
# Buffer for single Threads post
mcp tool buffer.create_update --channelIds '["threads"]' --text "First post in chain."

# Chain follow-ups via Playwright (Threads API doesn't yet support chain mutation)
playwright_mcp.run('threads_chain_script.js', input_chain=['post2','post3'])
```

### Recipe 8: Bluesky reply chain with embed-quote

Bluesky AT Protocol:

```bash
# Post root
curl -X POST https://bsky.social/xrpc/com.atproto.repo.createRecord \
  -H "Authorization: Bearer $BSKY_TOKEN" \
  -d '{
    "repo":"did:plc:<your-did>",
    "collection":"app.bsky.feed.post",
    "record":{"text":"Root post","createdAt":"2026-06-12T14:00:00Z"}
  }'
# Returns: {uri, cid}

# Reply chain
curl -X POST https://bsky.social/xrpc/com.atproto.repo.createRecord \
  -d '{
    "repo":"did:plc:<your-did>",
    "collection":"app.bsky.feed.post",
    "record":{
      "text":"Follow-up post",
      "reply":{"root":{"uri":"<root_uri>","cid":"<root_cid>"},
               "parent":{"uri":"<root_uri>","cid":"<root_cid>"}},
      "createdAt":"2026-06-12T14:01:00Z"
    }
  }'
```

## Examples

### Example A: TikTok product video (Shop-linked)

```yaml
spec:
  video: 30s vertical 1080x1920
  hook: "POV: you tried 5 face creams and this one actually worked"
  on_screen_text: keywords from "best face cream sensitive skin 2026" SEO query
  trending_sound: rising sound from social-trend-monitoring last 48hr
  product_tag: TIKTOK_SHOP_PRODUCT_ID
  caption: "Sensitive skin? My honest 30-day review. 🧴 #skincare #sensitive #honestreview #brandX"
  cover_timestamp_ms: 2500  # cover frame at 2.5s
```

### Example B: IG Reel + carousel campaign launch

```yaml
launch_day:
  reel:
    duration: 15s
    spec: 9:16 1080x1920
    cover: branded-cover-frame.jpg
    audio: trending_branded_sound_id
    caption: "We just launched ___. Tap below to see how it works ↓"
    hashtags: [25-tag basket per role.md spec]
  carousel:
    cards: 8
    layout: 1 hook + 6 feature + 1 CTA
    product_tags: PROD_1, PROD_2 (per card)
    caption: "Swipe → 6 reasons ___ matters. Shop in bio."
```

### Example C: LinkedIn 12-page carousel (highest organic engagement)

```yaml
linkedin_carousel:
  format: PDF document
  pages: 12 (cover + 10 lessons + CTA)
  aspect: 4:5 vertical for mobile reading
  text_per_page: 30-40 words MAX
  font: large-and-bold first line of each page
  commentary: "Lessons from scaling X to $1M ARR (carousel — swipe to read all)"
  hashtags: 3-5 industry + branded
```

## Edge cases

### TikTok Content Posting approval
1-2 week review; requires verified TikTok for Business. Until approved, use unverified upload through `tiktok-mcp` (limited features).

### IG Reel music availability
Music sticker only renders if track is in Meta's audio library AND your business account has commercial-music rights. Many trending pop songs are not commercial-licensed; use original audio or licensed alternatives.

### IG carousel product-tag limits
Max 5 products per image; max 10 images per carousel. Product IDs come from Meta Commerce Catalog (see `social-commerce-tiktok-instagram-pinterest-shops`).

### YouTube Shorts vs Long-form detection
Vertical 9:16 + < 60s + `#Shorts` tag = Shorts shelf. Wrong aspect or > 60s falls to long-form. YouTube auto-categorizes; can't override.

### LinkedIn carousel size limit
Max 100MB PDF, max 100 pages. For richer carousels, use designer tools (`figma-mcp` / `canva-mcp`) and pre-export.

### X media count per tweet
Max 4 images OR 1 video OR 1 GIF per tweet. For thread media on every tweet, attach per-tweet.

### X media reuse across thread
Cannot reuse media_id from a previous tweet's upload. Re-upload per tweet.

### X Premium long-form
Premium accounts can post 25,000 chars; algorithm still prefers concise. Long-form pollutes timeline reach.

### Thread + Bluesky chain rate
Threads chains rapidly = throttle (suspicious-bot heuristic). Add 30-60s between chain entries.

### Threads / Bluesky link previews
Bluesky renders Open Graph card if URL in body. Threads doesn't render card; URL becomes plain text. Use Bluesky for share-link drives, Threads for conversation.

### Pinterest pin vs Idea Pin
Idea Pin (multi-page) legacy in 2026; static + video pin take engagement. Pinterest API v5 covers static + video.

### TikTok Stitch / Duet permissions
Default permissive; disable per-video via `disable_duet` / `disable_stitch` in post_info. For controlled brand content, lock both; for UGC seeding, leave open.

### LinkedIn organization vs personal post
Org posts via org URN; personal posts via member URN. Token scope `w_organization_social` for org, `w_member_social` for personal.

### YouTube Shorts comments
Cannot disable comments on Shorts via API consistently; use studio.youtube.com manual flag. Spam-bot comments common on viral Shorts; monitor via `youtube-mcp`.

### Aspect ratio enforcement
Most APIs reject wrong aspect; some letterbox. Pre-validate via ffprobe before upload:
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 video.mp4
```

### Concurrent publish rate
Avoid > 10 parallel uploads to same platform; rate-limit risk. Sequential or batched (Buffer cascade) safer.

## Sources

- **TikTok Content Posting API**: https://developers.tiktok.com/doc/content-posting-api-get-started/
- **Instagram Graph API (Reels)**: https://developers.facebook.com/docs/instagram-platform/reels/
- **Instagram Graph API (Carousel)**: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media
- **YouTube Data API v3**: https://developers.google.com/youtube/v3
- **X API v2 (tweet creation)**: https://docs.x.com/x-api/posts/creation-of-a-post
- **LinkedIn Documents API (carousel)**: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/community-management/shares/document-share
- **Bluesky AT Protocol**: https://atproto.com/specs/xrpc
- **Pinterest API v5**: https://developers.pinterest.com/docs/api/v5/
