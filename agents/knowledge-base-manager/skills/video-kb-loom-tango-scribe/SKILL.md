---
name: video-kb-loom-tango-scribe
description: Video + step-by-step process guides for KB — Loom (narrated screencasts + transcript API), Tango / Scribe (auto-captured browser step-by-step), Guidde (AI-narrated walkthroughs). Use when a static article doesn't show the click path well — short-async explainer vs SOP-style step guide vs AI-voiceover walkthrough.
---

# Video KB — Loom narrated, Tango/Scribe auto-captured, Guidde AI-narrated

## When to use

Reach for this skill when the user says: "make a Loom for this", "auto-capture the steps", "Tango", "Scribe", "video walkthrough", "screen-record the setup", "SOP", "AI-narrated demo", or "the article needs a video". Decision tree: short async explainer (5-10min) = Loom; SOP-style step guide (auto-captured clicks → markdown + screenshots) = Tango/Scribe; AI-voiceover walkthrough = Guidde. Skip for full marketing video (defer to `video-creator`).

## Setup

```bash
# Loom CLI/SDK is browser/desktop app-driven; no install for content
# For transcripts via Loom Public API
curl -fsSL https://example.com/install-loom.sh   # desktop app
# OR record in-browser at loom.com

# Tango: browser extension (Chrome / Edge) — install from store
# Scribe: browser extension — install from store
# Guidde: browser extension OR webapp.guidde.com
```

Auth / env vars:
- `LOOM_API_KEY` — Loom Pro/Business → Settings → API. Pro tier required for API.
- `TANGO_API_KEY` — Tango settings → API. Paid (Premium+).
- `SCRIBE_API_KEY` — Scribe settings → API. Paid (Pro+).
- `GUIDDE_API_KEY` — Guidde dashboard → API. Paid.

## Common recipes

### Recipe 1: Pull Loom video metadata + transcript via Public API

```bash
# List recent videos
curl -s 'https://www.loom.com/v1/videos?limit=20' \
  -H "Authorization: Bearer $LOOM_API_KEY" \
  | jq '.results[] | {id, name, public_url, duration, shared_at}'

# Fetch transcript (auto-generated)
curl -s "https://www.loom.com/v1/videos/<video_id>/transcript" \
  -H "Authorization: Bearer $LOOM_API_KEY" \
  | jq -r '.transcript[] | "[\(.timestamp_start)] \(.text)"'

# Save transcript as SRT for caption burn-in
curl -s "https://www.loom.com/v1/videos/<video_id>/transcript?format=srt" \
  -H "Authorization: Bearer $LOOM_API_KEY" \
  > $(date +%Y%m%d)-loom-$video_id.srt
```

### Recipe 2: Embed Loom in a KB article (Docusaurus / MDX)

```mdx
import Loom from '@site/src/components/Loom';

# Configure webhooks

<Loom id="abc123xyz" />

The full walkthrough is in the video above. Step-by-step below if you prefer text...
```

```jsx
// src/components/Loom.jsx
export default function Loom({ id }) {
  return (
    <div style={{ position: 'relative', paddingBottom: '56.25%', height: 0 }}>
      <iframe
        src={`https://www.loom.com/embed/${id}?hideEmbedTopBar=true`}
        frameBorder="0"
        allowFullScreen
        style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' }}
      />
    </div>
  );
}
```

### Recipe 3: Tango — capture → export to markdown

Workflow (browser-driven):
1. Install Tango extension; click "Start capturing" in Tango toolbar.
2. Perform the click path in the app.
3. Click "Stop capturing"; Tango auto-generates a workflow with screenshots + numbered steps.
4. Click "Export" → markdown.

```bash
# Pull the workflow via API after capture
curl -s "https://api.tango.us/v1/workflows/<workflow_id>?format=markdown" \
  -H "Authorization: Bearer $TANGO_API_KEY" \
  > how-to/configure-webhook.md

# Or get the JSON for custom rendering
curl -s "https://api.tango.us/v1/workflows/<workflow_id>" \
  -H "Authorization: Bearer $TANGO_API_KEY" \
  | jq '.steps[] | {step: .order, title, description, screenshot_url}'
```

### Recipe 4: Scribe — pull captured workflow as markdown

```bash
curl -s "https://api.scribehow.com/v1/scribes/<scribe_id>" \
  -H "Authorization: Bearer $SCRIBE_API_KEY" \
  | jq -r '.steps[] | "\(.order). \(.title)\n   ![](\(.image_url))\n\n   \(.description)\n"' \
  > how-to/configure-webhook.md
```

Captures click-by-click; screenshots auto-uploaded to Scribe CDN. Edit the markdown to add narrative voice.

### Recipe 5: Guidde — AI-narrated walkthrough

Workflow (browser-driven):
1. Open `app.guidde.com`; click "New video → Capture from browser".
2. Walk the flow; Guidde captures + transcribes + generates AI voiceover from the captured text.
3. Adjust voice (multiple AI voices available) + add intro / outro slides.
4. Publish → get embed URL.

```bash
# Pull the video via API
curl -s "https://api.guidde.com/v1/videos/<video_id>" \
  -H "Authorization: Bearer $GUIDDE_API_KEY" \
  | jq '{title, public_url, transcript_url, embed_url}'
```

### Recipe 6: ffmpeg fallback — convert Loom recording to MP4 with caption burn-in

```bash
# Download Loom MP4 + SRT (from Recipe 1)
curl -L -o loom-video.mp4 "https://www.loom.com/v1/videos/<video_id>/download"

# Burn captions
ffmpeg -i loom-video.mp4 -vf "subtitles=loom-transcript.srt:force_style='FontSize=18,PrimaryColour=&HFFFFFF&,BackColour=&H80000000&'" \
  -c:a copy -c:v libx264 -preset medium -crf 23 loom-with-captions.mp4
```

### Recipe 7: Auto-publish weekly Loom digest to KB index page

```bash
#!/usr/bin/env bash
# In cron / GitHub Action
SINCE=$(date -d '7 days ago' --iso-8601)
videos=$(curl -s "https://www.loom.com/v1/videos?limit=50" \
  -H "Authorization: Bearer $LOOM_API_KEY" \
  | jq --arg s "$SINCE" '[.results[] | select(.shared_at >= $s)] | map({title: .name, url: .public_url, duration})')

# Render to markdown
echo "# Loom updates — week of $SINCE" > docs/loom-updates.md
echo "$videos" | jq -r '.[] | "- [\(.title)](\(.url)) — \(.duration / 60 | floor)m"' >> docs/loom-updates.md
git add docs/loom-updates.md && git commit -m "loom digest: $SINCE" && git push
```

### Recipe 8: Capture cost-of-clicks — Tango step count vs Scribe step count

```bash
# Compare workflow lengths to identify confusing flows
tango=$(curl -s "https://api.tango.us/v1/workflows/<wf_id>" -H "Authorization: Bearer $TANGO_API_KEY" | jq '.steps | length')
scribe=$(curl -s "https://api.scribehow.com/v1/scribes/<scribe_id>" -H "Authorization: Bearer $SCRIBE_API_KEY" | jq '.steps | length')
echo "Tango: $tango steps | Scribe: $scribe steps"
# >12 steps for a single task = flow needs simplification (PM signal, not docs signal)
```

### Recipe 9: Transcript → searchable docs index (Loom video → SEO content)

```bash
# Loom transcript becomes part of the article so users can search the spoken content
curl -s "https://www.loom.com/v1/videos/<video_id>/transcript" \
  -H "Authorization: Bearer $LOOM_API_KEY" \
  | jq -r '.transcript[].text' \
  | tr '\n' ' ' \
  > video-transcript.txt

# Embed at bottom of article
cat <<EOF >> docs/how-to/configure-webhook.md
<details>
<summary>Full video transcript</summary>

$(cat video-transcript.txt)
</details>
EOF
```

### Recipe 10: Choose tool per use case

```python
def pick_tool(use_case: str) -> str:
    if "explainer" in use_case or "5-10min" in use_case:
        return "Loom"  # narrated screencast
    if "click-by-click" in use_case or "SOP" in use_case:
        return "Tango or Scribe"  # auto-captured steps
    if "ai voiceover" in use_case.lower() or "no recording" in use_case.lower():
        return "Guidde"  # AI-narrated
    if "demo for sales" in use_case.lower():
        return "Loom (Studio Sound)"
    if "internal training" in use_case.lower():
        return "Scribe (free tier covers most)"
    return "Loom"  # default
```

## Examples

### Example 1: Webhook setup — Loom explainer + Tango step guide

**Goal:** Customers either watch the 6-min walkthrough OR follow the screenshots.

**Steps:**
1. Record a 6-min Loom walking through webhook setup; share publicly.
2. Use Tango to auto-capture the click path; export markdown (Recipe 3).
3. Embed Loom at top of `docs/how-to/configure-webhook.md` (Recipe 2).
4. Paste Tango steps below the video.
5. Add `<details>` transcript (Recipe 9).

**Result:** Article serves visual + textual learners; transcript indexable for SEO.

### Example 2: Internal SOP for new joiners using Scribe

**Goal:** New support agents need click-by-click for ticket workflow; ship in 10 minutes.

**Steps:**
1. Install Scribe extension; click "Start capturing".
2. Walk the entire workflow once at human pace.
3. Stop capturing; Scribe auto-generates markdown.
4. Edit screenshots' annotations (red boxes, arrows) directly in Scribe.
5. Pull via Recipe 4; commit to internal wiki.

**Result:** Onboarding SOP in 10min; updates with one re-capture.

### Example 3: AI-narrated walkthrough for non-recording-friendly users

**Goal:** Product manager wants demo video but doesn't want to record their voice.

**Steps:**
1. Capture flow in Guidde browser extension.
2. Pick AI voice from Guidde voice library; tweak transcript text.
3. Add brand intro slide.
4. Pull embed URL via Recipe 5.
5. Embed in newsletter / docs.

**Result:** Professional-feeling video without recording the PM's voice; updates with text edits.

## Edge cases / gotchas

- **Loom Pro tier required for API** — free Loom = no transcript API. Pay or skip Recipe 1.
- **Loom transcript accuracy ~95%** for clear US English; degrades with accents or technical jargon. Manually edit for product terminology.
- **Tango / Scribe screenshots embed brand logos / UI strings** — if your UI updates, screenshots stale instantly. Re-capture per release.
- **Tango max workflow length** ~50 steps; longer = split into multi-part SOP.
- **Scribe free tier** captures and exports markdown; paid tier needed for API + branding control.
- **Guidde AI voice has uncanny-valley moments** — preview every video before publishing; manual narration sometimes better.
- **Loom shared-link permissions** — default "anyone with link"; if hosting in customer docs, lock to org domain or password.
- **Loom video privacy** — uploaded recordings count toward your storage quota; archive or delete old recordings (Pro = unlimited; free = 25 vids).
- **Screen recordings leak PII** — Tango / Scribe auto-blur form inputs; verify before publishing. Loom doesn't blur — manually re-record if needed.
- **Mobile flows** — Loom mobile app for mobile-screen recordings; Tango / Scribe are browser-only (desktop app flows only).
- **Don't embed without a text alternative** — accessibility AND searchability. Always include `<details>` transcript (Recipe 9) or the Tango-exported markdown next to the video.
- **CDN bandwidth bills** — Tango / Scribe screenshots served from their CDN under Pro plans; if you self-host markdown, download images locally or live with their CDN dependency.
- **Auto-generated narration tone-mismatch** — Tango / Scribe step-titles can sound robotic ("Step 1: Click the button"). Rewrite for human voice.
- **No-API workflow for Loom embeds** — public URLs work with the Loom embed iframe even without the Public API; for non-API use cases stay on the iframe (Recipe 2).

## Sources

- [Loom Public API docs](https://www.loom.com/developers)
- [Loom embed iframe](https://support.loom.com/hc/en-us/articles/360002208618-Embedding-a-Loom-video)
- [Tango API docs](https://help.tango.us/article/61-tango-api)
- [Tango export to Markdown](https://help.tango.us/article/95-export-tango-workflows)
- [Scribe API docs](https://scribehow.com/library/api)
- [Scribe Chrome extension](https://chrome.google.com/webstore/detail/scribe)
- [Guidde docs](https://docs.guidde.com/)
- [ffmpeg subtitles filter](https://ffmpeg.org/ffmpeg-filters.html#subtitles-1)
- [Video accessibility — W3C](https://www.w3.org/WAI/media/av/)
- [Loom vs Tango vs Scribe comparison](https://www.scribehow.com/library/loom-alternative)
