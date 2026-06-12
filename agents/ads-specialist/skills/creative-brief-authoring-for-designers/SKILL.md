<!--
Source: https://www.vidico.com/news/video-creative-brief/
Creative brief authoring for designers / video team / external production.
-->
# Creative Brief Authoring (for Designers / Video Team) — SKILL

The creative brief is the artifact that hands the matrix cell to the producer. Vague briefs = wrong assets = burned testing budget. This skill ships a structured brief template, the hook-first format, the deliverable spec (per platform), and the hand-off path to `video-creator` for AI gen.

## When to use this skill

- **Matrix cell → asset request** for designer / video team.
- **External production brief** (Vidico / Magic Hour / freelance designer).
- **AI gen brief** for `video-creator` (Sora / Veo / Kling / Flux) or `imagegen-mcp`.
- **Creator partnership brief** for Spark Ads / influencer UGC.
- **Refresh brief** when fatigue triggers rotation (`ad-fatigue-rotation-strategy`).

**Do NOT use this skill when:**
- Pure copy-only test (Google RSA headline variants — use the RSA spec directly).
- Bulk programmatic creative (use `ai-creative-generation-adcreative-smartly` skill).
- Brand identity work (defer to `marketing-agent` Vale brand voice).

## Setup

### Brief template structure

1. **Cell reference** — matrix ID + hypothesis being tested
2. **Hook (first 3 seconds)** — concrete description of opening frame
3. **Story arc** — problem → product reveal → social proof → CTA
4. **Deliverables** — formats, ratios, lengths, asset count
5. **Brand constraints** — voice, color, logo, type
6. **Legal / claims** — what can / cannot be said
7. **Inspiration references** — links to comparable winning ads
8. **Timeline + ownership**

### Hook format (the 3-second rule)

Every video / static must justify continued attention within 3 seconds. Categories:
- **Pattern interrupt** — visual shock / unexpected motion / direct address
- **Problem-aware question** — "Tired of [X]?"
- **Result-first** — show outcome before context
- **Social proof up-front** — "30K customers love this"
- **Founder-direct** — talking-head founder address
- **Demo-first** — product action in frame 1

### Output formats

- `.docx` (deliverable to external designer)
- `.pdf` (signed brief for production sign-off)
- Notion page (linked from creative-library DB)

## Common recipes

### Recipe 1: Standard brief template (.docx)

```python
from docx import Document
from docx.shared import Pt, Inches

doc = Document()
doc.add_heading('Creative Brief — Cell C7', 0)

doc.add_heading('Matrix reference', 1)
doc.add_paragraph('Cell ID: C7')
doc.add_paragraph('Hypothesis: Founder-UGC hook + free-shipping offer + LAL-1% audience')
doc.add_paragraph('Sibling cells: C1 (control), C3, C5, C7, C9, C11')

doc.add_heading('Hook (first 3 seconds)', 1)
doc.add_paragraph('Founder Hannah on camera, no makeup, looking directly into lens.')
doc.add_paragraph('First spoken line: "I built this because my dermatologist gave up on me."')
doc.add_paragraph('Visual: Vertical 9:16, natural daylight, slight handheld feel.')

doc.add_heading('Story arc (15s spot)', 1)
doc.add_paragraph('00:00-00:03 — Hook (founder direct address)')
doc.add_paragraph('00:03-00:07 — Problem framing ("4 years of trying everything")')
doc.add_paragraph('00:07-00:11 — Product reveal (cream applied; 14-day before/after split)')
doc.add_paragraph('00:11-00:14 — Social proof callout ("rated 4.9 by 30K customers")')
doc.add_paragraph('00:14-00:15 — CTA card ("Shop now — free shipping")')

doc.add_heading('Deliverables', 1)
table = doc.add_table(rows=5, cols=4)
table.style = 'Light Grid'
hdr = table.rows[0].cells
hdr[0].text, hdr[1].text, hdr[2].text, hdr[3].text = "Ratio","Length","Platform","Variants"
rows = [
    ("9:16","15s","Meta Reels, IG Stories, TikTok In-Feed","2 (V1 controlled, V2 punchier hook)"),
    ("1:1","15s","Meta Feed, IG Feed","2"),
    ("16:9","15s","YouTube Shorts, Google Display","1"),
    ("9:16","30s","TikTok Spark Ads","1 (extended UGC version)"),
]
for i, r in enumerate(rows, 1):
    for j, v in enumerate(r):
        table.rows[i].cells[j].text = v

doc.add_heading('Brand constraints', 1)
doc.add_paragraph('Voice: warm, direct, no jargon. Tier: Founder-VO.')
doc.add_paragraph('Logo: lower-right corner CTA card only; no watermark.')
doc.add_paragraph('Type: Inter (already in brand kit). Hex #1A1A1A on cream.')

doc.add_heading('Legal / claims', 1)
doc.add_paragraph('PERMITTED: "87% saw clearer skin in 14 days" (back-substantiated, clinical-trial source).')
doc.add_paragraph('PROHIBITED: "cure", "guaranteed", any treatment claim.')
doc.add_paragraph('Disclaimer required if before/after used: "Individual results vary."')

doc.add_heading('Inspiration', 1)
doc.add_paragraph('Reference winner from competitor X (Meta Ad Library snapshot in /assets/refs/).')
doc.add_paragraph('Avoid: stock-footage cliché, salesy VO, generic CTA card.')

doc.add_heading('Timeline + ownership', 1)
doc.add_paragraph('Owner: Designer Name (slack: @designer)')
doc.add_paragraph('Hand-off: 2026-06-12')
doc.add_paragraph('First review: 2026-06-16')
doc.add_paragraph('Final delivery: 2026-06-19')
doc.add_paragraph('Launch: 2026-06-21')

doc.save('brief-cell-C7.docx')
```

### Recipe 2: AI gen brief → `video-creator` handoff

```yaml
# Format for video-creator (Sora / Veo / Kling / Runway)
brief_for_ai:
  reference_matrix_cell: C7
  duration_s: 15
  aspect_ratio: "9:16"
  prompt: |
    Vertical 9:16, natural-daylight shot of a woman in her 30s with bare skin,
    holding a small white cream jar. Direct address to camera, warm and casual,
    no makeup. Then dissolve to: hand applying cream, then 14-day timelapse
    showing skin clearing. End on product shot with "Shop now" overlay.
    Tone: founder-direct UGC, NOT polished commercial. Slight handheld camera feel.
  voice_over:
    text: "I built this because my dermatologist gave up on me. After 4 years..."
    voice_id: "elevenlabs:sarah:warm"
    pacing: conversational, slight pause before product reveal
  music: subtle, acoustic guitar undertone (Epidemic Sound: "Soft Reflection")
  variants_required: 3
  delivery_format: mp4, H.264, 4-8 Mbps
```

### Recipe 3: Static creative brief — Meta carousel

```yaml
brief:
  cell_ref: C12
  format: carousel
  card_count: 5
  ratio: "1:1"
  cards:
    1:
      headline: "The 4-step routine"
      body: "Cleanse → Treat → Moisturize → Protect"
      image: product family lifestyle shot
    2:
      headline: "Step 1: Gentle cleanser"
      body: "Removes makeup without stripping"
      image: cleanser on white background
    3-5: [analogous steps]
  cta: "Shop the routine"
  destination: https://brand.com/routine?utm_content=cell-c12
```

### Recipe 4: Spark Ads creator brief

```markdown
# Creator Brief — Hannah Lee (@hannahleeskin), $X budget

## Asset
- 9:16 vertical video, 30-60s
- Posted natively on @hannahleeskin TikTok
- Tagged: #ad #partnership (FTC compliant)

## Required elements
- Mention "Brand" by name within first 5s
- Demonstrate product application (any step)
- Personal verdict / opinion (authentic, not script)
- End with "you can find the link in my bio" (no hard CTA)

## What to AVOID
- Script-reading or stilted delivery
- Before/after claims without "individual results vary"
- Stock B-roll feel
- Direct competitor mentions

## Whitelist for Spark Ad
- Provide auth_code via Creator Tools → Authorize Ads
- Code valid 7d; ad will boost the post
- Budget: $X, runs 14d

## Deliverable
- Native TikTok post live by [date]
- Send auth_code to [email]
```

### Recipe 5: PMax asset group brief

```yaml
asset_group: PMax-AG-EcoConsciousBuyers
hypothesis: "Eco-message attracts conversion in this audience signal"

assets_required:
  headlines: 10  # ≤30 chars, examples:
    - "Eco-friendly skincare"
    - "Sustainable formulas"
    - "Cruelty-free + plant-based"
    - "Refillable packaging"
    [...6 more]
  long_headlines: 3   # ≤90 chars
    - "Sustainable, dermatologist-tested formulas — refillable, cruelty-free."
    [...2 more]
  descriptions: 5  # ≤90 chars
  marketing_images: 8  # 1200x628 + 1200x1200, lifestyle + product shots
  logo: 1   # 1200x1200
  square_marketing_image: 4
  youtube_video: 1 (15-30s product-story)

audience_signal:
  custom_audience: "in_market:sustainability_eco_products"
  user_list: "customer_match_eco_buyers"
```

### Recipe 6: Brief hand-off Slack template

```
:art: New brief: Cell C7 (Founder-UGC + Free-shipping × LAL-1%)
- File: <link to brief.pdf>
- Notion: <link>
- Hypothesis: founder-direct hook outperforms problem-aware Q at same CPA
- Deliverable: 4 versions (9:16 + 1:1 + 16:9 + 30s Spark)
- Hand-off: <designer>
- Review: 2026-06-16
- Launch: 2026-06-21
- Budget: $50/day for 14d in matrix
- Brief author: @ads-specialist
```

## Examples — three brief archetypes

### Archetype A — DTC e-com video, founder-led

15s, 9:16, 1:1, 16:9 deliverables. Founder direct address → problem → product → 14-day result → CTA. Free shipping offer overlay at 12s. 3 variants per ratio.

### Archetype B — B2B SaaS demo

30s product demo. Voice-over narrating problem → workflow → measurable result. 1:1 LinkedIn Feed + 16:9 YouTube Pre-roll. Tier: explainer style.

### Archetype C — App install gameplay

15s + 30s versions. Open with 3s gameplay action (no UI logo). Beat 1: gameplay highlight. Beat 2: progression / reward. Beat 3: app icon + "Install now". Vertical 9:16 + 1:1.

## Edge cases

### Brief too vague
"Make a video showing the product" is not a brief. Force specifics: hook frame, length, ratio, exact opening line.

### Brand voice conflict
If brief copy violates Vale brand-voice rules → run through `vale-brand-voice` (marketing-agent skill) before send.

### Claim substantiation
Any quantitative claim needs source link. Without it, ad rejection on Meta / Google. Document substantiation in brief footer.

### Talent / model release
UGC with creator or actor needs signed release. Brief footer: "Talent release on file: yes/no" with link to PDF.

### Reuse / variation
Brief should distinguish "new creative" vs "variation of winning creative." Variations reuse 80% of assets + tweak hook / CTA.

### Hook misread by designer
Always include reference video link (Meta Ad Library snapshot or competitor) to anchor visual interpretation.

### Cell duplication
Two cells with same brief = identical creative = no test signal. Always vary at least one dimension (hook OR offer OR audience).

### Designer iteration cycle
1 round of feedback baked into timeline. >2 rounds = brief was unclear.

### File deliverable spec
Format: MP4 H.264, 4-8 Mbps, AAC audio 128 kbps. Max 4 GB per Meta upload. Specify in brief.

### Lost-in-translation for international
Multi-market briefs: list translations needed (`deepl-mcp`); flag market-specific claims.

## Sources

- Vidico video brief guide: https://www.vidico.com/news/video-creative-brief/
- Meta video ad specs: https://www.facebook.com/business/ads-guide/video
- Google Ads video specs: https://support.google.com/google-ads/answer/2375464
- TikTok video specs: https://ads.tiktok.com/help/article?aid=10000388
- LinkedIn ad specs: https://www.linkedin.com/help/lms/answer/a420652
- FTC influencer disclosure: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- Meta ad policy: https://transparency.fb.com/policies/ad-standards
