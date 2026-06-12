# LinkedIn Carousel Authoring — Postiv / Carosello / Taplio + Canva MCP

> Write + design swipeable 8-14-slide LinkedIn carousels with 6.6% engagement (6× lift over text).

## When to use

Trigger on: "make a LinkedIn carousel", "write a 10-slide deck", "carousel from this post", "Postiv this", "Carosello carousel", "branded carousel via Canva". This skill owns: 8-14 slide structure, hook design, mobile-readable typography rules, branded layout via Canva MCP, publishing to LinkedIn. Carousels generate 1.6× engagement vs standard text + 6.6% engagement rate vs 1.11% text-only. For quote graphics (1-3 slides) see `infographic-canva-piktochart-visme`. For thread-style multi-post LinkedIn cascade see `twitter-x-thread-authoring`.

## Setup

```bash
# Postiv — end-to-end carousel generator (writes + designs)
curl -H "Authorization: Bearer $POSTIV_API_KEY" https://api.postiv.com/v1/me

# Carosello — BYOK Gemini API at ~$0.10/carousel
curl -H "Authorization: Bearer $CAROSELLO_API_KEY" \
  -H "X-Gemini-Key: $GEMINI_API_KEY" \
  https://api.carosello.app/v1/projects

# Taplio
curl -H "Authorization: Bearer $TAPLIO_API_KEY" https://api.taplio.com/v1/me

# Canva MCP (branded template fallback)
npx @canva/mcp --help

# LinkedIn Marketing API (publishing)
curl -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  https://api.linkedin.com/v2/me
```

Auth env vars:
- `POSTIV_API_KEY` — Postiv dashboard; Pro plan for API. $39/mo.
- `CAROSELLO_API_KEY` + `GEMINI_API_KEY` — Carosello BYOK; cheaper at scale (~$0.10/carousel via your Gemini key).
- `TAPLIO_API_KEY` — Taplio account.
- `CANVA_API_KEY` — Canva for Teams enterprise API.
- `CANVA_CAROUSEL_TEMPLATE_ID` — pre-built branded template ID.
- `LINKEDIN_ACCESS_TOKEN` — OAuth 2.0 with `w_member_social` scope.

## Common recipes

### Recipe 1: Carousel structure template

```markdown
# Carousel: <working title>
**Slides:** 10
**Hook style:** Curiosity gap | Surprising stat | Contrarian | Specific outcome

## Slide 1 (Hook)
**Headline:** <pull-scroll line — 6-10 words>
**Supporting:** <1-line proof or specificity>
**Visual:** <background style / icon / emoji>

## Slides 2-9 (Body — one insight per slide)
- Slide 2: <headline + 1-2 sentence support + visual>
- Slide 3: <...>
- Slide 4: <...>
- Slide 5: <...>
- Slide 6: <...>
- Slide 7: <...>
- Slide 8: <...>
- Slide 9: <...>

## Slide 10 (CTA)
**Headline:** <explicit ask>
**Body:** <what they get from the action>
**Visual:** <brand mark + URL or @username>

## Caption (under the carousel post)
- Hook line — pull from slide 1
- Context — 2-3 sentences
- CTA — drive to bio link / DM / comment
- Hashtags — 3-5 (1-2 branded + 2-3 niche)
```

### Recipe 2: Postiv end-to-end (writes + designs)

```bash
# One-shot: topic → 10-slide branded carousel
curl -X POST https://api.postiv.com/v1/carousels \
  -H "Authorization: Bearer $POSTIV_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Newsletter operators: stop tracking open rates",
    "tone": "direct, data-driven",
    "slides": 10,
    "include_hook": true,
    "include_cta": true,
    "cta_text": "Save this for your next quarterly review",
    "brand_colors": ["#0A0A0A", "#FFFFFF", "#FF6B35"],
    "brand_font": "Inter"
  }'

# Returns {"carousel_id":"car_xyz","status":"generating"}

# Poll
curl -H "Authorization: Bearer $POSTIV_API_KEY" \
  "https://api.postiv.com/v1/carousels/car_xyz" \
  | jq '{status, download_url, slides:.slides|length, caption}'

# Download as PDF / PNG sequence
curl -L -o carousel.pdf "<download_url>"
```

Postiv generates everything in <5 min from topic or URL.

### Recipe 3: Carosello BYOK Gemini

```bash
curl -X POST https://api.carosello.app/v1/carousels \
  -H "Authorization: Bearer $CAROSELLO_API_KEY" \
  -H "X-Gemini-Key: $GEMINI_API_KEY" \
  -d '{
    "topic": "Newsletter operators: stop tracking open rates",
    "slides": 10,
    "style": "minimal",
    "include_images": true
  }'
```

Carosello uses your Gemini API key directly = ~$0.10/carousel vs Postiv's flat plan fee. Better for high-volume creators.

### Recipe 4: Canva MCP branded template instantiation

```bash
# Use Canva MCP when brand fidelity matters more than AI generation
# Pre-build a 10-slide carousel template in Canva with placeholders for {{headline}}, {{body}}, {{slide_number}}

npx @canva/mcp create_design \
  --template_id "$CANVA_CAROUSEL_TEMPLATE_ID" \
  --customizations '[
    {"name":"slide_1_headline","value":"Open rates lie. Heres what to track."},
    {"name":"slide_1_body","value":"After Apple MPP, opens are vanity."},
    {"name":"slide_2_headline","value":"Track CTR instead"},
    {"name":"slide_2_body","value":"Clicks per send, not opens per send."},
    ...
  ]' \
  --output carousel_export
```

### Recipe 5: From newsletter / blog → carousel via Castmagic

```bash
# Castmagic 'linkedin_carousel_outline' derivative
curl -H "Authorization: Bearer $CASTMAGIC_API_KEY" \
  "https://api.castmagic.io/v1/uploads/$UPLOAD_ID/derivatives" \
  | jq -r '.linkedin_carousel_outline'

# Outline returns slide-by-slide breakdown; pass into Postiv/Carosello/Canva
```

### Recipe 6: Publish carousel to LinkedIn

```bash
# LinkedIn carousels = uploaded as PDF "document" post
# Step 1: register upload
curl -X POST https://api.linkedin.com/rest/documents?action=initializeUpload \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "LinkedIn-Version: 202404" \
  -d '{"initializeUploadRequest":{"owner":"urn:li:person:<PROFILE_ID>"}}' \
  > upload_init.json

UPLOAD_URL=$(jq -r .value.uploadUrl upload_init.json)
DOC_URN=$(jq -r .value.document upload_init.json)

# Step 2: upload PDF
curl -X PUT "$UPLOAD_URL" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  --data-binary @carousel.pdf

# Step 3: create the post with the document attached
curl -X POST https://api.linkedin.com/rest/posts \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202404" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -d '{
    "author": "urn:li:person:<PROFILE_ID>",
    "commentary": "Most newsletter operators are measuring the wrong thing. Save this for your next quarterly review.\n\n→ Carousel below ↓\n\n#newsletter #operator #marketing",
    "visibility": "PUBLIC",
    "distribution": {"feedDistribution": "MAIN_FEED"},
    "content": {
      "media": {
        "title": "Open rates lie",
        "id": "'"$DOC_URN"'"
      }
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": false
  }'
```

### Recipe 7: Schedule via Buffer

```bash
# Buffer supports LinkedIn carousels as document posts
npx @buffer/mcp-server create_post \
  --platform linkedin \
  --content "$(cat caption.md)" \
  --media-file carousel.pdf \
  --media-type document \
  --scheduled-at "2026-06-17T13:00:00Z"
```

Schedule for Tuesday-Thursday 8-10am ET (carousel SOTA timing).

### Recipe 8: Mobile typography check

```bash
# Render PDF at iPhone viewport
npx @playwright/mcp navigate \
  --url "file:///$(pwd)/carousel.pdf" \
  --viewport "375x812" \
  --screenshot carousel_mobile.png

# Eyeball: text at 24pt+ at smallest, single-thought-per-slide, brand consistent
```

### Recipe 9: A/B hook test

```bash
# Generate 3 variant first slides via Postiv
for HOOK in "Open rates lie" "Stop measuring opens" "After Apple MPP open rates broke"; do
  curl -X POST https://api.postiv.com/v1/carousels \
    -d '{"topic":"'"$HOOK"'","slides":10}'
done

# Publish each as a separate carousel, 1 week apart. Track engagement to identify winning hook style.
```

### Recipe 10: Bulk-author for series

```python
# Author 12 carousels for a 12-week series in one pass
topics = [
    "Newsletter open rates lie",
    "CTR is the only metric that matters",
    "Why Tuesday 6am wins",
    # ...
]
for topic in topics:
    response = requests.post(
        "https://api.carosello.app/v1/carousels",
        headers={
            "Authorization": f"Bearer {os.environ['CAROSELLO_API_KEY']}",
            "X-Gemini-Key": os.environ['GEMINI_API_KEY'],
        },
        json={"topic": topic, "slides": 10, "style": "minimal"}
    )
    # Push carousel_id + topic into Notion editorial DB
```

## Examples

### Example 1: Tuesday 8am ET carousel from newsletter

**Goal:** Publish a 10-slide LinkedIn carousel based on this week's Tuesday newsletter.

**Steps:**
1. Recipe 5: Castmagic linkedin_carousel_outline from newsletter.md.
2. Recipe 2: Postiv generates 10 slides + branded design.
3. Recipe 8: mobile-typography QA.
4. Write caption (Recipe 1 caption section).
5. Recipe 6: publish directly via LinkedIn API (or Recipe 7 schedule via Buffer for Tuesday 8am next week).
6. 24h later: pull engagement stats; compare to text-post baseline.

**Result:** Carousel at 6.6%+ engagement vs the 1.11% text-only baseline.

### Example 2: Branded carousel via Canva MCP (no AI generator)

**Goal:** Brand wants control over every visual element; Postiv's auto-design is too generic.

**Steps:**
1. Build branded 10-slide template in Canva with `{{slide_N_headline}}` + `{{slide_N_body}}` placeholders.
2. Save template; capture `CANVA_CAROUSEL_TEMPLATE_ID`.
3. Write all 10 slide headlines + bodies in Markdown.
4. Recipe 4: Canva MCP instantiate template with customizations.
5. Download PDF; Recipe 6 publish.

**Result:** On-brand carousel without sacrificing AI-speed for AI-generic-look.

### Example 3: BYOK Gemini for high-volume creator (50 carousels/month)

**Goal:** Reduce per-carousel cost from $39/mo flat (Postiv) to ~$5 in API costs (Carosello + Gemini).

**Steps:**
1. Provision Gemini API key (~$0.10/carousel call).
2. Recipe 10: bulk-author 50 carousels via Carosello.
3. Total API cost: ~$5/month vs $39 Postiv flat fee.

**Result:** 87% cost reduction at scale; ownership of generation model.

## Edge cases / gotchas

- **8-14 slides is the sweet spot.** Under 8 = thin; over 14 = swipe fatigue.
- **Slide 1 hook decides 70%+ of engagement.** Test 3 hooks per topic when possible.
- **Mobile-readable typography = 24pt+ at smallest.** Under 20pt unreadable on iPhone in feed.
- **One idea per slide.** Two ideas = unconfident structure; viewers swipe past.
- **Don't repeat the hook on slide 2.** Slide 2 is the proof, not the restated hook.
- **Carousel post caption should hook from slide 1.** Caption + slide 1 should reinforce, not contradict.
- **3-5 hashtags — niche + branded only.** Avoid spammy generic tags (#marketing).
- **LinkedIn document posts = PDF format, not image carousel.** Don't try to upload as multi-image post; LinkedIn won't render as swipeable.
- **PDF must be ≤300 pages, ≤100MB.** Way under your limit for 10-slide carousels.
- **CTA on final slide should be explicit.** "Save", "Share", "Comment 'X' for the link", "Follow for more" — vague CTAs fall flat.
- **Posting time: Tuesday-Thursday 8-10am ET.** Friday afternoon and weekend carousels suppress in feed algo.
- **Postiv vs Carosello vs Canva decision tree:**
  - Postiv = fastest, AI generates everything (best for non-designers).
  - Carosello = cheapest at scale (BYOK), more control over Gemini prompt.
  - Canva = best brand fidelity (slower but on-brand).
- **Native LinkedIn carousel format DEPRECATED** — current best practice is uploaded PDF as document post. Multi-image swipeable post still works but has lower reach in 2026 algo.
- **A/B test cadence:** 1 carousel/week minimum to get statistically meaningful engagement signal.
- **Taplio combines authoring + scheduling** but its design is more generic. Use when speed > design polish.
- **LinkedIn doesn't show document analytics in basic dashboard** — pull via API for impressions, clicks, dwell time.

## Sources

- [LinkedIn carousel engagement (Supergrow)](https://www.supergrow.ai/blog/linkedin-carousel-generators)
- [ContentIn — LinkedIn carousel generators 2026](https://contentin.io/blog/best-linkedin-carousel-generators/)
- [Postiv](https://www.postiv.com/)
- [Carosello](https://carosello.app/)
- [Taplio](https://taplio.com/)
- [Canva MCP](https://www.canva.com/developers/)
- [LinkedIn Marketing API — Posts](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/community-management/shares/posts-api)
- [LinkedIn document upload guide](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/community-management/shares/documents-api)
