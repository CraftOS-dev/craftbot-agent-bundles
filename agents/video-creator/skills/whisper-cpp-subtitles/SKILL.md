# Whisper.cpp Subtitles — Local STT + Karaoke ASS

## When to use
- Local, offline transcription (privacy, no API cost)
- Word-level timestamps (for karaoke / per-word reveal)
- SRT / VTT / ASS export from voice
- Multilingual (99 languages via large-v3)
- Word-by-word highlight subtitles (TikTok / Reels style)

Skip when: budget allows Submagic ($69/mo) for premium animated templates without coding.

## Setup
```bash
# Install whisper.cpp
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp && make
# Or via Homebrew on Mac:
brew install whisper-cpp

# Download model
bash ./models/download-ggml-model.sh large-v3
# Result: models/ggml-large-v3.bin (~3 GB)
```

Model size vs accuracy:
| Model | Size | Speed | Accuracy |
|---|---|---|---|
| tiny | 75 MB | very fast | low (drafts) |
| base | 142 MB | fast | acceptable |
| small | 466 MB | medium | good |
| medium | 1.5 GB | slow | very good |
| large-v3 | 3 GB | slowest | best (recommended) |
| large-v3-turbo | 1.6 GB | ~3× faster than large-v3 | near-best |

## Common recipes

### 1. Basic SRT generation
```bash
whisper-cli -m models/ggml-large-v3.bin -osrt input.wav
# Output: input.wav.srt
```

### 2. SRT + VTT + word-level timestamps
```bash
whisper-cli -m models/ggml-large-v3.bin \
  -osrt -ovtt -owts \
  -ml 42 \
  input.wav
```
- `-osrt`: SRT
- `-ovtt`: WebVTT (for web players)
- `-owts`: word-level karaoke script (bash file)
- `-ml 42`: max segment length 42 chars (TikTok-friendly chunk size)

### 3. Specify language (skips auto-detect → faster + more accurate)
```bash
whisper-cli -m models/ggml-large-v3.bin -l en -osrt input.wav
```

### 4. Translate to English (any language → English subs)
```bash
whisper-cli -m models/ggml-large-v3.bin -l ja -tr -osrt input.wav
# Japanese audio → English SRT
```

### 5. JSON output (structured)
```bash
whisper-cli -m models/ggml-large-v3.bin -oj input.wav
# input.wav.json with segments, words, confidence
```

### 6. Word-level for karaoke
```bash
whisper-cli -m models/ggml-large-v3.bin -ow -oj input.wav
```
`-ow` is word-level timestamps. JSON output gives per-word `start` + `end` in ms.

### 7. Audio prep (Whisper expects 16kHz mono WAV)
```bash
ffmpeg -i raw.mp4 -ar 16000 -ac 1 -c:a pcm_s16le input.wav
```
Stereo or 48k input works but is silently downmixed/resampled — pre-convert for predictable results.

### 8. Convert word-level JSON → karaoke ASS (Python helper)
```python
# whisper_to_ass.py
import json, sys
with open(sys.argv[1]) as f: data = json.load(f)
def ms_to_ass(ms):
    h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h}:{m:02}:{s:02}.{ms//10:02}"
print("[Script Info]\nScriptType: v4.00+\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Outline, Alignment, MarginV\nStyle: Default,Inter,72,&H00FFFFFF,&H00000000,&H80000000,1,2,2,200\n\n[Events]\nFormat: Layer, Start, End, Style, Text")
for seg in data["transcription"]:
    words = seg.get("words", [])
    if not words: continue
    start, end = ms_to_ass(words[0]["t0"]*10), ms_to_ass(words[-1]["t1"]*10)
    parts = []
    for w in words:
        dur = (w["t1"] - w["t0"])  # in centiseconds in whisper.cpp
        parts.append(f"{{\\k{int(dur)}}}{w['text'].strip()}")
    print(f"Dialogue: 0,{start},{end},Default,, , 0,0,0,, {' '.join(parts)}")
```
Usage:
```bash
python whisper_to_ass.py input.wav.json > karaoke.ass
```

### 9. Burn ASS into video (FFmpeg subtitles filter)
```bash
ffmpeg -i video.mp4 -vf "subtitles=karaoke.ass:force_style='FontName=Inter,Outline=3,BorderStyle=1,Shadow=1'" -c:a copy out.mp4
```

### 10. Word-by-word highlight (TikTok style)
ASS `\k` tags advance per-word; combine with `\1c&Hffffff&` (white) base + `\1c&H00ffff&` (yellow) accent timed to word boundaries.

### 11. SRT to ASS converter (FFmpeg)
```bash
ffmpeg -i in.srt out.ass
```
Quick path if you don't need karaoke.

### 12. Subtitle style cheat sheet (ASS `\` codes)
- `\b1` — bold on; `\b0` off
- `\1c&Hxxxxxx&` — primary color (BGR, not RGB!)
- `\3c&Hxxxxxx&` — outline color
- `\fs72` — font size
- `\fade(255,0,255,0,300,1700,2000)` — fade-in/out
- `\move(x1,y1,x2,y2)` — pan
- `\an2` — anchor (2 = bottom-center, lower-third style)

### 13. Whisper diarization (multi-speaker)
Whisper.cpp doesn't natively diarize. Pipeline:
1. `pyannote-audio` for speaker labels.
2. Whisper.cpp transcript.
3. Merge by timestamp.

### 14. Real-time / streaming
```bash
whisper-cli -m models/ggml-base.en.bin --step 1000 --length 5000 --keep 200 --vad-thold 0.6 -t 8 -c 0
```
For live captioning. Use smaller model for low latency.

### 15. GPU acceleration
```bash
WHISPER_CUDA=1 make
# OR for Apple Silicon (Metal):
WHISPER_METAL=1 make
```
Then large-v3 runs ~5× faster on a GPU/Apple Silicon.

## Examples

### A. TikTok karaoke captions
1. `ffmpeg -i video.mp4 -ar 16000 -ac 1 audio.wav`
2. `whisper-cli -m large-v3.bin -ow -oj -l en audio.wav`
3. `python whisper_to_ass.py audio.wav.json > captions.ass`
4. `ffmpeg -i video.mp4 -vf "subtitles=captions.ass" -c:a copy out.mp4`

### B. Multilingual SRT for 5 languages
Run Whisper with `-l <lang>` per language. Output 5 SRTs. Soft-subtitle via:
```bash
ffmpeg -i video.mp4 -i en.srt -i es.srt -i ja.srt \
  -map 0 -map 1 -map 2 -map 3 \
  -c:v copy -c:a copy -c:s mov_text \
  -metadata:s:s:0 language=eng \
  -metadata:s:s:1 language=spa \
  -metadata:s:s:2 language=jpn \
  multi.mp4
```

### C. Quick draft with `base` model
For a 1-min YouTube draft: use `ggml-base.en.bin` — 4× faster than large-v3, accuracy good enough for review.

### D. ASS-styled lower-third with brand color
```ass
Style: Brand,Inter,64,&H00FFFFFF,&H00FFA500,&H80000000,1,4,2,200
Dialogue: 0,0:00:01.00,0:00:04.00,Brand,, , 0,0,0,, This is the hook
```
White text + orange outline + semi-transparent backdrop bar, anchored bottom-center.

## Edge cases / gotchas

1. **Whisper.cpp `\k` units are centiseconds** (not ms). Convert properly when building ASS.
2. **`-ml` does NOT split on word boundaries.** It can chop mid-word. Word-level post-processing fixes this.
3. **`large-v3` hallucinates on long silences.** Pre-trim silences with `ffmpeg silenceremove`.
4. **Punctuation is inconsistent** across runs. Post-process with regex if you need uniform style.
5. **Whisper transcribes filler words** ("um", "uh"). For clean subs, post-process to strip.
6. **Acronym capitalization** — Whisper rarely capitalizes. Manual review.
7. **ASS colors are BGR not RGB.** Red is `&H0000FF&`, not `&HFF0000&`.
8. **`subtitles=` filter needs the FONT installed on the rendering machine.** Otherwise falls back to default sans.
9. **GPU build (`WHISPER_CUDA=1`)** doesn't load `ggml-large-v3-q5_0.bin` quantized models on some setups; use full-precision.
10. **Numbers vs words.** "I'll be there at 2pm" might transcribe as "two PM" — Whisper isn't deterministic.
11. **English-only models (`.en.bin`)** are 2× faster than multilingual but only do English.
12. **VAD (voice activity detection)** isn't enabled by default; turn on with `--vad-thold` for noisy input.

## Sources
- https://github.com/ggerganov/whisper.cpp
- https://github.com/ggerganov/whisper.cpp/blob/master/README.md
- http://www.tcax.org/docs/ass-specs.htm (ASS subtitle format spec)
- https://ffmpeg.org/ffmpeg-filters.html#subtitles
