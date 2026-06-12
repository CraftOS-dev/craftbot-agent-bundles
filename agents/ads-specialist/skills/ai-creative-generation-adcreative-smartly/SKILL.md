<!--
Source: https://www.adcreative.ai/api
Source: https://www.smartly.io/products
Source: https://www.bannerbear.com/api
AI creative generation: AdCreative.ai + Smartly + Bannerbear + Creatify + handoff to video-creator.
-->
# AI Creative Generation — AdCreative.ai / Smartly / Bannerbear — SKILL

AI-gen creative scales the matrix at 5-10x lower per-asset cost than human production. **AdCreative.ai** for static banners + carousel. **Smartly.io** for enterprise cross-platform programmatic. **Bannerbear** for templated bulk static. **Creatify / Magic Hour / MotionDen** for AI video. Hand off to `video-creator` for Sora/Veo/Kling. This skill ships the API recipes + the brand-kit setup + the quality-gate workflow.

## When to use this skill

- **Matrix scale-up** — need 30-100 variants for testing matrix.
- **Bulk product carousel** — 50+ SKUs need same-format card per SKU.
- **Cross-platform creative** — same concept in 5 ratios × 5 lengths × 3 messages.
- **Brand-consistent variants** — multiple hooks within brand kit.
- **AI video for testing** — concept validation before commissioning live shoot.

**Do NOT use this skill when:**
- Bespoke brand campaign — defer to human designers / video-creator.
- Founder UGC required — AI can't replicate authenticity.
- Photorealistic product photography — use real product shots.

## Setup

### Tool comparison

| Tool | Best for | Pricing | API quality |
|---|---|---|---|
| **AdCreative.ai** | Static + carousel banner gen with brand kit | $29-$189/mo | REST API |
| **Smartly.io** | Enterprise cross-platform programmatic + auto-optimization | Custom ($50K+/yr) | REST + integrations |
| **Bannerbear** | Templated programmatic image (bulk product carousels) | $49-$249/mo | REST + Zapier |
| **Creatify** | AI video ads with avatars | $29-$99/mo | REST |
| **Magic Hour** | AI video character animation | $19-$249/mo | REST |
| **MotionDen** | AI video gen with templates | $14-$199/mo | API + UI |
| **Vidico** | Human production service | Project-based | n/a |

### API keys

```bash
export ADCREATIVE_API_KEY="<key>"
export SMARTLY_API_KEY="<key>"
export BANNERBEAR_API_KEY="<key>"
export CREATIFY_API_KEY="<key>"
```

### Brand kit registration (one-time)

```bash
# AdCreative.ai — set up brand kit via UI or API
curl -X POST "https://api.adcreative.ai/api/v1/brands" \
  -H "Authorization: Bearer $ADCREATIVE_API_KEY" \
  -d '{
    "name": "Brand X",
    "logo_url": "https://cdn.brand.com/logo.png",
    "primary_color": "#1A1A1A",
    "secondary_color": "#F4E5D2",
    "fonts": ["Inter"],
    "voice_tone": "warm, direct, no-jargon"
  }'
```

## Common recipes

### Recipe 1: AdCreative.ai — generate 10 static banner variants

```bash
curl -X POST "https://api.adcreative.ai/api/v1/generate-creative" \
  -H "Authorization: Bearer $ADCREATIVE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "brand_id": "'$BRAND_ID'",
    "creative_type": "DISPLAY_BANNER",
    "dimensions": ["1080x1080","1080x1920","1200x628"],
    "headline": "20% off this weekend only",
    "subheadline": "Free shipping over $50",
    "cta": "Shop now",
    "product_image_url": "https://cdn.brand.com/products/hero.jpg",
    "background_options": ["solid","gradient","lifestyle"],
    "variant_count": 10
  }' > adcreative-output.json

# Returns array of generated image URLs
jq '.data[] | {id, image_url, ratio: .dimension, variation: .variation_id}' adcreative-output.json
```

### Recipe 2: Bannerbear — templated bulk gen (50 SKU carousel cards)

```bash
# Template ID created once in Bannerbear UI with editable layers: 
#   {{product_name}}, {{price}}, {{image}}, {{cta}}

for sku in $(jq -r '.[].sku' products.json); do
  product=$(jq ".[] | select(.sku == \"$sku\")" products.json)
  
  curl -X POST "https://api.bannerbear.com/v2/images" \
    -H "Authorization: Bearer $BANNERBEAR_API_KEY" \
    -d "$(jq -n --arg tid "$TEMPLATE_ID" --argjson p "$product" '{
      template: $tid,
      modifications: [
        {name: "product_name", text: $p.title},
        {name: "price", text: $p.price},
        {name: "image", image_url: $p.image_link},
        {name: "cta", text: "Shop now"}
      ]
    }')" >> bannerbear-batch.json
done
```

### Recipe 3: Smartly — Dynamic Product Ads cross-platform

```bash
# Smartly's "Predictive Budget Allocation" auto-distributes creative across Meta + Google + TikTok
# Configure via Smartly UI; document for repro

# Programmatic via API:
curl -X POST "https://api.smartly.io/v3/campaigns" \
  -H "Authorization: Bearer $SMARTLY_API_KEY" \
  -d '{
    "name": "Cross-Platform-DPA-Q3",
    "platforms": ["meta","google","tiktok","pinterest"],
    "catalog_id": "'$CATALOG_ID'",
    "creative_set_id": "'$CREATIVE_SET_ID'",
    "audience_segments": ["abandoners_7d","viewers_30d"],
    "budget_allocation_strategy": "auto",
    "total_budget_usd": 5000
  }'
```

### Recipe 4: Creatify — AI video with avatar

```bash
curl -X POST "https://api.creatify.ai/api/v1/videos" \
  -H "X-Api-Id: $CREATIFY_API_ID" \
  -H "X-Api-Key: $CREATIFY_API_KEY" \
  -d '{
    "name": "Cell-C7-FounderHook-AI-V1",
    "script": "I built this because my dermatologist gave up on me. After 4 years of trying every cream, I formulated this in my kitchen — and now 30,000 customers use it daily. Free shipping on your first order.",
    "avatar_id": "sarah_female_30s_warm",
    "voice_id": "elevenlabs:sarah:warm",
    "aspect_ratio": "9:16",
    "duration_target_s": 15,
    "background_music": "soft_acoustic",
    "captions": true,
    "brand_kit_id": "'$BRAND_ID'"
  }'
```

### Recipe 5: Handoff to `video-creator` for Sora / Veo / Kling

```yaml
handoff_brief:
  to: video-creator agent
  cell_ref: C7
  brief: |
    9:16 vertical, 15s. Natural daylight, woman in 30s with bare skin, 
    direct address to camera then product application + 14-day timelapse 
    of skin clearing. Founder-UGC feel, not polished commercial. 
    Slight handheld camera.
  voice_over: 
    script: "I built this because my dermatologist gave up on me..."
    voice: elevenlabs:sarah:warm
  music: subtle acoustic
  recommended_models:
    primary: kling-v2  # best for human realism
    fallback: veo-3    # if Kling overloaded
  variants_required: 3
  output_format: mp4, H.264, 4-8 Mbps
```

### Recipe 6: Magic Hour — AI character animation

```bash
curl -X POST "https://api.magichour.ai/v1/animations" \
  -H "Authorization: Bearer $MAGICHOUR_API_KEY" \
  -d '{
    "type": "image-to-video",
    "source_image_url": "https://cdn.brand.com/founder-static.jpg",
    "motion_prompt": "subtle head turn + smile + natural breathing, no exaggerated movement",
    "duration_s": 10,
    "aspect_ratio": "9:16",
    "fps": 30
  }'
```

### Recipe 7: Pre-launch QA — policy + brand voice check

```python
# Run AI-gen creative through validators before launch
import requests, anthropic

client = anthropic.Anthropic()

for asset in generated_assets:
    # 1. Brand voice check via Vale (cross-grep marketing-agent skill)
    vale_result = subprocess.run(["vale", "--config", ".vale.ini", asset["copy"]], capture_output=True)
    if vale_result.returncode != 0:
        flag_for_review(asset, "brand_voice_violation")
        continue
    
    # 2. Meta policy pre-flight
    pre_check = mcp_call("meta-ads.validate_creative", {"text": asset["copy"], "image_url": asset["url"]})
    if pre_check["policy_check"] == "failed":
        flag_for_review(asset, f"meta_policy: {pre_check['issues']}")
        continue
    
    # 3. LLM tone check
    r = client.messages.create(
      model="claude-sonnet-4-5-20250929",
      max_tokens=100,
      messages=[{"role":"user","content":
        f"Does this ad match brand voice? Brand voice: warm, direct, no jargon. Ad copy: '{asset['copy']}'. Answer YES/NO + 1-line reason."
      }])
    if "NO" in r.content[0].text:
        flag_for_review(asset, "tone_mismatch")
```

### Recipe 8: Auto-deploy winning AI variants

```bash
# After AI gen + QA, upload to Meta + launch in test matrix cell
for asset_id in $(jq -r '.[] | select(.qa_passed == true) | .id' qa-results.json); do
  url=$(jq -r ".[] | select(.id == \"$asset_id\") | .url" generated.json)
  
  # Upload to Meta
  image_hash=$(curl -X POST "https://graph.facebook.com/v19.0/act_$AD_ACCOUNT_ID/adimages" \
    -F "filename=@$url" -F "access_token=$META_TOKEN" | jq -r '.images[].hash')
  
  # Create ad creative
  creative_id=$(mcp_call meta-ads.create_ad_creative \
    --name "AI-Gen-$asset_id" --image_hash "$image_hash" --link "$LP_URL" --message "$COPY")
  
  # Add to test adset
  mcp_call meta-ads.create_ad --adset_id "$TEST_ADSET" --creative_id "$creative_id" --name "AI-$asset_id"
done
```

## Examples — workflow for $200 budget AI matrix test

```yaml
goal: validate 5 new hook concepts on $200 budget in 5 days

step_1_brief:
  cells: 5 hooks × 1 audience × 1 offer = 5 cells
  budget_per_cell: $40 over 5 days
  format: 9:16 video, 15s
  hook_concepts:
    - C1: problem-aware question
    - C2: founder UGC
    - C3: testimonial montage
    - C4: result-driven
    - C5: price anchor

step_2_generate:
  - AdCreative.ai: 5 static thumbnails (one per hook, for fallback)
  - Creatify: 5 avatar-led videos (one per hook)
  - video-creator handoff: 1 Sora/Veo "premium" variant for control
  total_assets: 11
  generation_time: ~2h (Creatify queue)
  generation_cost: ~$30 ($6/asset average)

step_3_qa:
  - Vale brand voice on copy
  - Meta validate_creative pre-check
  - human review (15 min)
  pass_rate_expected: 70-80% (some AI quirks need re-gen)

step_4_deploy:
  - Upload to Meta via Marketing API
  - Create 5 adsets (ABO, $40/day each)
  - Launch with 24h delay (overnight, capacity for replay)

step_5_read:
  - Day 5: CTR + CPA per cell
  - z-test vs control (C1 = problem-aware Q)
  - Promote winners to scaling campaign
```

## Edge cases

### AI uncanny-valley
AI-generated faces sometimes look "off." Test against control (human creative); if AI underperforms by 30%+, the issue is not concept but perceived authenticity.

### Copy hallucination
AI tools sometimes generate copy that violates brand voice OR makes unsubstantiated claims. Always run through Vale + LLM tone check.

### Watermark on free tier
Free / lower-tier plans may add watermark. Verify before launch.

### Resolution / quality
Bannerbear / AdCreative.ai output: 72 DPI typically. Meta Reels prefers 1080p+. Check resolution before upload.

### Style drift
AI variant 5 may look stylistically different from variant 1. Use seed parameter when supported to lock style.

### API rate limits
- AdCreative.ai: 100/hour standard; 500/hour pro
- Bannerbear: 50/min default
- Creatify: 10 concurrent renders standard
- Magic Hour: 5 concurrent

### Cost per asset
- AdCreative.ai static: $0.10-$0.50/variant
- Bannerbear: $0.10/image
- Creatify video: $3-$10/clip
- Magic Hour: $1-$5/clip
- Sora/Veo via video-creator: $5-$20/clip

### Iteration latency
Most AI tools have 30s-5min render queue. Plan briefs with batch generation (5-20 variants per request) vs per-variant requests.

### Brand kit drift
Brand kit changes (new color, new font) require re-registering. Maintain version control.

### Multi-language
AdCreative.ai + Smartly support multi-language. For Creatify avatar, voice + script language must match.

### Legal — talent / avatar likeness
AI avatars: most platforms use licensed AI avatars (no real person). If you upload a real person's image to animate, you need release. Document.

### Hand-off path to video-creator
For premium / brand-critical video, defer to `video-creator` (Sora/Veo/Kling/Runway). AI-gen tools are for matrix scale-up, not flagship.

## Sources

- AdCreative.ai API: https://www.adcreative.ai/api
- AdCreative.ai docs: https://docs.adcreative.ai/
- Smartly.io products: https://www.smartly.io/products
- Smartly.io API: https://help.smartly.io/hc/en-us/articles/360001687449
- Bannerbear API: https://www.bannerbear.com/api
- Bannerbear templates: https://www.bannerbear.com/help/articles/
- Creatify API: https://docs.creatify.ai/
- Magic Hour API: https://docs.magichour.ai/
- MotionDen API: https://www.motionden.com/api
- Vidico: https://www.vidico.com/
- Meta validate_creative: https://developers.facebook.com/docs/marketing-api/reference/ad-creative/
- ElevenLabs voices (for VO): https://elevenlabs.io/docs/api-reference/text-to-speech
