# Podcast Scripting + Show Notes — Castmagic / Otter / Whisper

> Pre-write scripts and post-record show notes for interview, monologue, panel, and narrative podcast formats.

## When to use

Trigger on: "script my next podcast", "write the show notes", "draft the episode outline", "make a podcast trailer script", "generate timestamps and chapters", "Castmagic this transcript". This skill produces the SOTA podcast-production deliverables: pre-record concept brief + outline, in-record cue sheet, post-record show notes + timestamps + summary + quotes-for-social. Do NOT use this skill for guest research (use `podcast-guest-research-outreach`), for editing briefs (use `podcast-editing-brief-descript-riverside`), or for the SEO meta + chapter RSS tag (use `podcast-seo-titles-descriptions-chapters`).

## Setup

```bash
# Castmagic MCP — Claude-native; transforms transcripts into show notes / threads / newsletters
# Settings → integrations → MCP. Or via CLI:
npx -y @castmagic/mcp-server@latest --help

# Otter API + AI Chat
curl -H "Authorization: Bearer $OTTER_API_KEY" https://otter.ai/api/v1/me

# Whisper.cpp (local STT) — see video-creator's whisper-cpp-subtitles skill
brew install whisper-cpp
bash ./models/download-ggml-model.sh large-v3
```

Auth env vars:
- `CASTMAGIC_API_KEY` — Castmagic settings → API. Pro plan minimum for MCP.
- `OTTER_API_KEY` — Otter dashboard → integrations. Free tier = 600 min/mo transcription.
- `WHISPER_MODEL_PATH` — local path to `ggml-large-v3.bin` if using Whisper fallback.

## Common recipes

### Recipe 1: Pre-record concept brief

```markdown
# Episode <#>: <working title>

## One-sentence thesis
<single declarative claim — the audience leaves with this idea>

## Audience question being answered
<what the listener Googled / asked that brings them to this episode>

## Format
<interview | monologue | panel | narrative>

## Target length
<25 / 35 / 45 / 60 min>

## Hook (cold open, 0:00 - 0:30)
<surprising fact, contrarian claim, or specific outcome>

## Three pillars (the spine of the episode)
1. <pillar 1 — claim + proof + example>
2. <pillar 2 — ...>
3. <pillar 3 — ...>

## Sponsor read placement
<00:02:30 pre-roll OR 00:18:00 mid-roll OR none>

## CTA (closing 60s)
<single explicit ask — subscribe / link / community / next episode tease>

## Resources to mention (with URLs)
- <tool / book / paper>
```

Save as `episodes/<ep#>/brief.md`. Drives outline, recording, editing, and show notes.

### Recipe 2: Upload audio to Castmagic + auto-generate show notes

```bash
# Upload via Castmagic API (or Castmagic MCP from inside Claude)
curl -X POST https://api.castmagic.io/v1/uploads \
  -H "Authorization: Bearer $CASTMAGIC_API_KEY" \
  -F "file=@episodes/ep042/master.mp3" \
  -F "title=Episode 42: Why Tuesday-6am beats Sunday-night"

# Returns {"id":"upload_xyz","status":"processing"}

# Poll for ready, then request derivatives
curl -X POST "https://api.castmagic.io/v1/uploads/upload_xyz/derivatives" \
  -H "Authorization: Bearer $CASTMAGIC_API_KEY" \
  -d '{"types":["show_notes","summary","timestamps","quotes","title_options","newsletter_writeup","x_thread","blog_post"]}'

# Pull derivatives
curl -H "Authorization: Bearer $CASTMAGIC_API_KEY" \
  "https://api.castmagic.io/v1/uploads/upload_xyz/derivatives"
```

Castmagic's value: structured derivatives without LLM hallucination, sourced from the actual transcript.

### Recipe 3: Castmagic MCP from inside Claude

```bash
# When the MCP is configured in CraftBot, the agent can call it natively
# Example tool call (pseudo-format; actual schema in Castmagic MCP docs):
# tool: castmagic.generate
# args: {"upload_id":"upload_xyz","types":["show_notes","summary","x_thread"]}
```

Inside Claude, this short-circuits the curl-poll loop. The MCP returns derivatives as a single structured response.

### Recipe 4: Otter API + Chat for show notes

```bash
# Upload audio
curl -X POST "https://otter.ai/api/v1/speeches/upload" \
  -H "Authorization: Bearer $OTTER_API_KEY" \
  -F "audio=@episodes/ep042/master.mp3"
# Returns {"speech_id":"sp_abc"}

# Wait for processing (typically 1/4 of audio length)
curl -H "Authorization: Bearer $OTTER_API_KEY" \
  "https://otter.ai/api/v1/speeches/sp_abc"

# Use Otter AI Chat to summarize
curl -X POST "https://otter.ai/api/v1/chat" \
  -H "Authorization: Bearer $OTTER_API_KEY" \
  -d '{"speech_id":"sp_abc","prompt":"Generate show notes with 5 key takeaways, 8 timestamped chapter markers, 3 pull-quotes for social, and a 150-word summary"}'
```

Otter is the alt when Castmagic isn't available; output is freeform Claude-generated rather than structured, so always Vale-scrub.

### Recipe 5: Whisper local STT fallback

```bash
# Resample for Whisper (16kHz mono WAV)
ffmpeg -i episodes/ep042/master.mp3 -ar 16000 -ac 1 -c:a pcm_s16le ep042.wav

# Transcribe with word-level timestamps
whisper-cli -m $WHISPER_MODEL_PATH -l en -ow -oj ep042.wav

# Parse JSON to produce timestamped show notes
python3 - <<'EOF'
import json
data = json.load(open('ep042.wav.json'))
for seg in data['transcription']:
    t = seg['offsets']['from'] // 1000  # ms → s
    print(f"{t//60:02d}:{t%60:02d}  {seg['text'].strip()}")
EOF
```

Use Whisper when audio is sensitive or Castmagic/Otter are unavailable.

### Recipe 6: Show notes template (post-process)

```markdown
# Episode <#>: <Front-Loaded Keyword> | <Guest Name / Hot Take>

## Summary (150-200 words)
<hook, guest, thesis, key insight, CTA — all in one paragraph>

## Key takeaways
- Takeaway 1: <single insight named in episode>
- Takeaway 2: <...>
- Takeaway 3: <...>
- Takeaway 4: <...>
- Takeaway 5: <...>

## Resources mentioned
- <tool / article / book> — <URL>

## Timestamps
- 00:00 — Cold open
- 02:30 — Sponsor read: <sponsor>
- 05:00 — <Topic 1>
- 18:00 — <Topic 2 / guest backstory>
- 32:00 — Hot take / key insight
- 48:00 — Q&A / wrap
- 55:00 — CTA + outro

## Guest bio
<name, role, past work, social links, one thing to plug>

## Sponsor
<host-read line + CTA URL with UTM>

## Subscribe + share
- Apple Podcasts: <URL>
- Spotify: <URL>
- YouTube: <URL>
- RSS: <URL>
- Newsletter (deeper takes): <URL>
- Leave a review: <Apple Podcasts review URL>
```

### Recipe 7: Trailer script (60-90s, 3-act)

```markdown
# Trailer: Episode <#>

## Act 1 — Hook (0-15s)
<host VO>: <one-sentence pattern interrupt + episode promise>
<music sting>

## Act 2 — Tease (15-50s)
<host VO>: <three pull-quotes or beats from the episode — fast cuts>
<guest clip 1, 8s>: "<surprising claim>"
<guest clip 2, 6s>: "<contrarian take>"
<host VO>: <one specific outcome listeners will get>

## Act 3 — CTA (50-90s)
<host VO>: "New episode out <day>. Subscribe wherever you listen — search '<podcast name>' on Apple Podcasts or Spotify. Or hit the link in the show notes."
<sound logo>
```

### Recipe 8: Castmagic → Notion editorial DB

```bash
# Pull Castmagic derivatives + push into Notion as child row of tentpole
CASTMAGIC_OUTPUT=$(curl -H "Authorization: Bearer $CASTMAGIC_API_KEY" \
  "https://api.castmagic.io/v1/uploads/upload_xyz/derivatives" | jq .)

SHOW_NOTES=$(echo "$CASTMAGIC_OUTPUT" | jq -r .show_notes)

npx @notionhq/mcp update_page \
  --page_id "$NOTION_EPISODE_ROW_ID" \
  --properties '{"Show notes":{"rich_text":[{"text":{"content":"'"$SHOW_NOTES"'"}}]}}'
```

### Recipe 9: Quote-card harvest from transcript

```bash
# Use Castmagic 'quotes' derivative or hand-grep the transcript
grep -E '^[A-Z].{40,140}\.$' ep042.transcript.txt | head -20

# Then feed into canva-mcp template for quote graphics (see linkedin-carousel-authoring skill)
```

### Recipe 10: Multi-language show notes

```bash
# Translate via deepl-mcp after Castmagic generation
DEEPL_OUTPUT=$(npx @deepl/mcp translate \
  --text "$SHOW_NOTES" \
  --target-lang ES)

# Publish translated show notes to a per-language episode page
```

## Examples

### Example 1: Solo monologue episode end-to-end

**Goal:** Publish a 30-min solo episode with thesis "Tuesday-6am beats Sunday-night for newsletter sends" + all derivatives.

**Steps:**
1. Write Recipe 1 brief, lock the three pillars, decide one sponsor mid-roll.
2. Record using `podcast-editing-brief-descript-riverside` recording-day checklist; export master MP3.
3. Upload to Castmagic via Recipe 2; request `show_notes`, `summary`, `timestamps`, `quotes`, `newsletter_writeup`, `x_thread`.
4. Vale-scrub all text outputs; publish show notes to podcast host episode page using Recipe 8.
5. Hand off newsletter writeup to `long-form-newsletter-substack-beehiiv-ghost` skill for Tuesday send.
6. Hand off X-thread output to `twitter-x-thread-authoring` skill for Typefully cascade.

**Result:** One 30-min episode → show notes + summary + chapters + 3-5 pull-quote cards + newsletter issue + X thread, all from one Castmagic call.

### Example 2: Interview episode with guest, Otter fallback

**Goal:** Publish a 45-min interview with a guest where Castmagic isn't configured (Otter-only stack).

**Steps:**
1. Write Recipe 1 brief with guest-specific question set.
2. Record via Riverside; export both speakers' tracks.
3. Run Recipe 4: upload to Otter, generate notes via Otter AI Chat.
4. Hand-edit timestamps (Otter is less structured than Castmagic).
5. Pull 3 pull-quotes manually from the transcript for social.
6. Vale-scrub; publish; hand to repurposing pipeline.

**Result:** Slightly more manual but equivalent end deliverable.

### Example 3: Pre-record trailer for a new season launch

**Goal:** Cut a 75s trailer promoting a 12-episode upcoming season.

**Steps:**
1. Pre-write trailer using Recipe 7 template.
2. Record host VO segments via Riverside (or generate via `elevenlabs-mcp` for narration if user agrees).
3. Pull 3 best 6-10s guest clips from the most exciting episode in the season.
4. Hand the script + clip timestamps to `podcast-editing-brief-descript-riverside` skill.
5. After edit, publish trailer as Episode 0 of the season to podcast feed.

**Result:** Algorithm-friendly free trailer that drives subscribes ahead of episode 1.

## Edge cases / gotchas

- **Castmagic Pro plan minimum** for the MCP and API access — Free/Basic tiers don't expose API.
- **Castmagic transcripts are derivative-only.** They don't replace primary STT; for accurate timestamps, Whisper or Riverside-native is more reliable for word-level.
- **Otter 600 min/mo free tier** burns fast for weekly hour-long episodes — upgrade to Otter Pro for production use.
- **Whisper large-v3 hallucinates on long silences** — pre-trim silences with `ffmpeg silenceremove` before transcribing.
- **Castmagic generates plausible quotes that don't appear verbatim** in the transcript. Always grep-verify pull-quotes against the source transcript before publishing.
- **Show notes need to be RSS-feed friendly** — most podcast hosts strip H1; lead with H2. Use simple markdown (no tables, no nested lists deeper than 2).
- **Timestamp drift** — if you edit the audio after Castmagic processes it, chapter timestamps will be off. Re-upload and re-derive, don't hand-adjust.
- **Otter speaker separation** is based on voiceprint matching; if guest uses earbuds vs a USB mic, accuracy drops. Manually relabel speakers post-transcription.
- **Trailer length: 60-90s.** Apple Podcasts auto-plays the trailer when a new listener taps Subscribe; longer than 90s and most drop out.
- **Cold open should be the hook.** Don't open with "Hey welcome to..." — that's been DOA since 2023.
- **Sponsor read in pre-roll vs mid-roll** — pre-roll has 4× lower listen-through-survival; place sponsors mid-roll at the 25% mark for max recall.

## Sources

- [Castmagic — Stormy AI repurposing 2026](https://stormy.ai/blog/best-gpt-repurposing-tools-2026-opusclip-munch-castmagic)
- [Castmagic platform](https://www.castmagic.io/)
- [Otter podcast transcription](https://otter.ai/podcast-transcription)
- [Otter API reference](https://developer.otter.ai/)
- [Whisper.cpp GitHub](https://github.com/ggerganov/whisper.cpp)
- [Best podcast hosting 2026](https://www.thepodosphere.com/blog/best-podcast-hosting-platforms-2026-comparison-guide)
- [Podcast SEO 2026](https://www.thespearpoint.com/blog/seo-for-podcasts)
- [ThoughtLeaders — Podcast trends 2026 (host-read 4× recall)](https://www.thoughtleaders.io/blog/podcast-trends-2026)
