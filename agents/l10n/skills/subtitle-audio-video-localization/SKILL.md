---
name: subtitle-audio-video-localization
description: Subtitle + audio + video L10n. Whisper.cpp transcription, Subtitle Edit / Aegisub / Subly editing & translation, SRT/VTT/ASS formats, CPS reading-speed validation, dubbing handoff to video-creator agent. Use when the user asks "translate subtitles", "generate SRT", "VTT for YouTube", "burn-in captions", "Whisper", "Aegisub", or wants subtitle QA.
---

# Subtitle & Audio / Video Localization

Workflow: extract audio → Whisper STT → SRT/VTT → per-locale translate (DeepL / Subly) → CPS reading-speed check → burn-in or sidecar delivery. Dubbing (voice replacement) is out of scope here — hand off to `video-creator` agent for voice-cloning + audio mix + final render.

Reading speed bands per script (CLDR-aligned):
- European (Latin): target 17 CPS (15-21 range)
- CJK: 4-7 chars/sec (effectively 13-15 CPS — denser per char)
- Arabic / Hebrew (RTL): 16-18 CPS

Format choice: **SRT** for sidecar (YouTube, Vimeo, players); **VTT** for HTML5 `<track>`; **ASS / SSA** for styled subtitles (Aegisub, fansubs); **TTML/IMSC** for broadcast / streaming (Netflix, BBC).

## When to use

- Translating tutorial videos for 5+ locales.
- Localizing a video course catalog (LMS).
- Captioning corporate webinars / training.
- Generating sidecar SRT for YouTube playlist.
- QA on existing subtitle files (CPS, line length, timing overlaps).
- Workflow handoff: subs done → video-creator for dubbing.

Trigger phrases: "subtitle", "captions", "SRT", "VTT", "Whisper", "Aegisub", "Subtitle Edit", "Subly", "CPS", "dubbing", "burn-in", "fansub", "TTML".

## Setup

```bash
# ffmpeg + Whisper + Whisper.cpp + faster-whisper
brew install ffmpeg whisper-cpp                    # macOS (apt-get / choco on Linux/Win)
pip install -U openai-whisper faster-whisper srt pysubs2
whisper --model large-v3 --download-only           # ~3GB model

# Subtitle Edit (Windows GUI + cross-platform CLI):
#   https://github.com/SubtitleEdit/subtitleedit/releases
# Aegisub (ASS / SSA editor): https://aegisub.org/
# Subly API: https://www.getsubly.com/  (commercial, 255 langs)

npm i -g subtitle-converter                        # SRT ↔ VTT
```

Auth/env: `SUBLY_API_KEY`, `DEEPL_API_KEY`. Whisper local model = no auth.

## Subtitle format quick reference

| Format | Use | Styling | Tools |
|---|---|---|---|
| **SRT** | YouTube, Vimeo, sidecar | Minimal (italic/bold) | Subtitle Edit, ffmpeg, Subly |
| **VTT** | HTML5 `<track>`, WebVTT | CSS, positioning, regions | Subtitle Edit, browser |
| **ASS / SSA** | Anime fansubs, karaoke | Full styling, positioning, effects | Aegisub, Subtitle Edit |
| **TTML / IMSC** | Broadcast, Netflix delivery | XML; precise styling | Subtitle Edit, Caption Maker |
| **STL** | EBU broadcast | Binary; teletext | Subtitle Edit |
| **SBV** | YouTube legacy | Minimal | Subtitle Edit |
| **CapXML / DFXP** | Adobe Premiere | XML | Subtitle Edit, Premiere |

## Common recipes

### Recipe 1: Audio extraction from MP4

```bash
# Lossless mono 16kHz WAV (Whisper input)
ffmpeg -i input.mp4 -vn -ac 1 -ar 16000 -acodec pcm_s16le audio.wav

# If only stereo source
ffmpeg -i input.mp4 -vn -af "pan=mono|c0=0.5*c0+0.5*c1" -ar 16000 audio.wav

# Boost low-volume voice for STT
ffmpeg -i input.mp4 -vn -af "loudnorm=I=-16:LRA=11:TP=-1.5,highpass=f=80,lowpass=f=8000" \
       -ar 16000 -ac 1 audio.wav
```

### Recipe 2: Whisper transcription → SRT

```bash
# Python whisper
whisper audio.wav --model large-v3 --language en --output_format srt \
  --output_dir subs/ --temperature 0 --best_of 5 --beam_size 5 --word_timestamps True

# Whisper.cpp (CPU; no GPU)
whisper-cli -m models/ggml-large-v3.bin -f audio.wav -l en -osrt -ovtt --output-file subs/en

# faster-whisper (4x speedup, GPU)
python -c "
from faster_whisper import WhisperModel; from datetime import timedelta; import srt
model = WhisperModel('large-v3', device='cuda', compute_type='float16')
segs, _ = model.transcribe('audio.wav', beam_size=5, word_timestamps=True)
subs = [srt.Subtitle(i+1, timedelta(seconds=s.start), timedelta(seconds=s.end), s.text.strip())
        for i,s in enumerate(segs)]
open('subs/en.srt','w').write(srt.compose(subs))"
```

### Recipe 3: Whisper translate-to-English in one step

```bash
# JP/KO/ES source → English SRT (Whisper built-in translate task)
whisper jp_lecture.wav --model large-v3 --task translate --output_format srt
# For target other than English, transcribe then DeepL-translate (Recipe 4).
```

### Recipe 4: Translate SRT per locale (DeepL)

```python
import srt, requests, os; from pathlib import Path
KEY = os.environ['DEEPL_API_KEY']
def translate_srt(src, tgt_lang, out):
    subs = list(srt.parse(Path(src).read_text()))
    r = requests.post('https://api.deepl.com/v2/translate',
        headers={'Authorization': f'DeepL-Auth-Key {KEY}'},
        data={'text':[s.content for s in subs], 'target_lang':tgt_lang,
              'preserve_formatting':1, 'tag_handling':'xml'})
    for s, t in zip(subs, r.json()['translations']): s.content = t['text']
    Path(out).write_text(srt.compose(subs))

for lang in ['DE','FR','JA','ZH','AR']:
    translate_srt('subs/en.srt', lang, f'subs/{lang.lower()}.srt')
```

### Recipe 5: Translate via Subly API

```bash
# Subly: AI translation, timing-preserved, 255 languages
curl -X POST 'https://api.getsubly.com/v1/projects' \
  -H "Authorization: Bearer $SUBLY_API_KEY" \
  -F "media_url=https://cdn.example.com/lecture.mp4" \
  -F "source_language=en" -F "target_languages=de,fr,ja,zh-Hans,ar"

# Poll: GET /v1/projects/{id}   → status
# Download:  GET /v1/projects/{id}/exports/srt?lang=de  → subs/de.srt
```

### Recipe 6: Validate CPS (reading speed)

```python
import srt
from pathlib import Path

LIMITS = {
    # script_family: (min_cps, max_cps, max_line_chars, max_lines)
    'latin':    (5,  21, 42, 2),
    'cjk':      (4,  15, 16, 2),
    'cyrillic': (5,  19, 38, 2),
    'arabic':   (5,  18, 38, 2),
    'thai':     (5,  16, 38, 2),
}

def check_srt(path, script='latin'):
    min_cps, max_cps, max_chars, max_lines = LIMITS[script]
    subs = list(srt.parse(Path(path).read_text()))
    issues = []
    for s in subs:
        dur = (s.end - s.start).total_seconds()
        if dur < 1.0:
            issues.append(f'#{s.index}: duration {dur:.2f}s < 1.0s minimum')
        if dur > 7.0:
            issues.append(f'#{s.index}: duration {dur:.2f}s > 7.0s maximum')
        cps = len(s.content) / dur if dur > 0 else 0
        if cps > max_cps:
            issues.append(f'#{s.index}: CPS {cps:.1f} > {max_cps} max for {script}')
        if cps < min_cps and len(s.content) > 5:
            issues.append(f'#{s.index}: CPS {cps:.1f} < {min_cps} min — too slow')
        lines = s.content.split('\n')
        if len(lines) > max_lines:
            issues.append(f'#{s.index}: {len(lines)} lines > {max_lines}')
        for li, line in enumerate(lines):
            if len(line) > max_chars:
                issues.append(f'#{s.index} line {li+1}: {len(line)} chars > {max_chars}')
    return issues

for lang, script in [('de', 'latin'), ('ja', 'cjk'), ('zh', 'cjk'), ('ar', 'arabic')]:
    issues = check_srt(f'subs/{lang}.srt', script)
    print(f'{lang}: {len(issues)} issues')
    for i in issues[:5]: print(f'  {i}')
```

### Recipe 7: Convert + batch-process SRT / VTT / ASS

```bash
# Format conversion — pick one tool
ffmpeg -i en.srt en.vtt                                  # SRT → VTT
ffmpeg -i en.srt en.ass                                  # SRT → ASS
npx subtitle-converter en.srt en.vtt                     # alt
python -c "import pysubs2; s=pysubs2.load('en.srt'); s.save('en.vtt'); s.save('en.ass')"

# Subtitle Edit CLI (Windows; Wine on macOS/Linux)
SubtitleEdit /convert *.srt webvtt /outputfolder:./vtt/
SubtitleEdit /convert en.srt subrip /offset:+00:00:02.000   # shift +2s
SubtitleEdit /convert en.srt subrip \
  /fixcommonerrors:RemoveEmptyLines,FixOverlappingDisplayTimes,FixShortDisplayTimes
```

### Recipe 8: Aegisub ASS styling (per-locale fonts + alignment)

```ass
[V4+ Styles]
Style: Default,Roboto,52,&H00FFFFFF,...,40,40,60,1
Style: CJK,Noto Sans JP,48,&H00FFFFFF,...
Style: RTL,Noto Sans Arabic,52,&H00FFFFFF,...

[Events]
Dialogue: 0,0:00:01.00,0:00:04.00,CJK,,0,0,0,,東京へようこそ。
Dialogue: 0,0:00:01.00,0:00:04.00,RTL,,0,0,0,,أهلا بكم في الفصل.
```

For DE/RU expansion, prepend `{\fscx95\fscy95}` per-line to scale text 5%. Aegisub Lua macros automate this for the whole script.

### Recipe 9: Burn-in subtitles into video

```bash
# Hard-burn SRT into MP4 (for platforms without sidecar support)
ffmpeg -i input.mp4 -vf "subtitles=en.srt:force_style='FontName=Roboto,FontSize=24,PrimaryColour=&HFFFFFF'" \
  -c:v libx264 -crf 22 -c:a copy output_burned.mp4

# Per-locale burn loop
for lang in en de fr ja zh ar; do
  ffmpeg -y -i input.mp4 \
    -vf "subtitles=subs/$lang.srt:force_style='FontName=Noto Sans'" \
    -c:v libx264 -crf 22 -c:a copy out/lecture-$lang.mp4
done
```

### Recipe 10: Mux sidecar (no burn-in)

```bash
# MKV with multiple sub tracks (selectable in player)
ffmpeg -i input.mp4 -i subs/en.srt -i subs/de.srt -i subs/ja.srt -i subs/ar.srt \
  -map 0 -map 1 -map 2 -map 3 -map 4 -c copy -c:s srt \
  -metadata:s:s:0 language=eng -metadata:s:s:1 language=ger \
  -metadata:s:s:2 language=jpn -metadata:s:s:3 language=ara output.mkv

# MP4 mov_text (limited player support — prefer sidecar SRT for MP4)
ffmpeg -i input.mp4 -i en.srt -c copy -c:s mov_text output.mp4
```

### Recipe 11: HTML5 player sidecar VTT

```html
<video controls>
  <source src="lecture.mp4" type="video/mp4">
  <track default kind="captions" srclang="en" label="English" src="subs/en.vtt">
  <track          kind="captions" srclang="de" label="Deutsch" src="subs/de.vtt">
  <track          kind="captions" srclang="ja" label="日本語"   src="subs/ja.vtt">
  <track          kind="captions" srclang="ar" label="العربية" src="subs/ar.vtt">
</video>
```

```vtt
WEBVTT
STYLE
::cue { background: rgba(0,0,0,.6); color: #fff; font-family: 'Noto Sans Arabic'; }
::cue(:lang(ar)) { direction: rtl; }

00:00:01.000 --> 00:00:04.000 line:80% align:start
Welcome to lecture one.
```

### Recipe 12: YouTube upload — sidecar SRT (multi-lang)

```bash
# YouTube Data API v3 — caption upload
curl -X POST "https://www.googleapis.com/upload/youtube/v3/captions?part=snippet&uploadType=multipart" \
  -H "Authorization: Bearer $YT_TOKEN" \
  -F 'snippet={"videoId":"VIDEO_ID","language":"de","name":"Deutsch","isDraft":false};type=application/json' \
  -F 'file=@subs/de.srt;type=application/octet-stream'

# Repeat per locale; YouTube auto-shows lang menu
```

### Recipe 13: Re-time SRT after video edit

```python
# CUTS = list of (timestamp, delta) — apply progressively to shift every cue after each cut.
import srt; from datetime import timedelta; from pathlib import Path
CUTS = [(timedelta(seconds=30), timedelta(seconds=5)),     # at 0:30 add 5s
        (timedelta(seconds=105), timedelta(seconds=-3))]   # at 1:45 remove 3s
def shift(t):
    for ct, dt in CUTS:
        if t >= ct: t += dt
    return t
subs = list(srt.parse(Path('subs/en.srt').read_text()))
for s in subs: s.start, s.end = shift(s.start), shift(s.end)
Path('subs/en-retimed.srt').write_text(srt.compose(subs))
```

### Recipe 14: Hand-off to video-creator for dubbing

```yaml
# Brief for video-creator agent
project: Lecture 1 dubbing
source_video: gs://cdn/lecture1.mp4
locales:
  - { lang: de, srt: subs/de.srt, voice: ElevenLabs/de-DE-Conrad, timing: time-stretch }
  - { lang: ja, srt: subs/ja.srt, voice: ElevenLabs/ja-JP-Yuki,   timing: replace_silence }
  - { lang: ar, srt: subs/ar.srt, voice: ElevenLabs/ar-SA-Hamid,  timing: time-stretch (AR is ~30% longer; pre-tighten SRT) }
deliverables: dubbed MP4 + sidecar SRT per locale
qa_pass: { lip_sync: ±100ms, music_bed: unchanged, sidecar_srt: preserved }
```

`video-creator` handles voice cloning (ElevenLabs / Play.ht / OpenAI TTS), audio mix (ducking music for VO), final render. Subtitle agent's job ends at translated SRT delivery.

### Recipe 15: Subtitle QA gate (CI)

```bash
# CI script (run after translation step)
#!/usr/bin/env bash
set -e
fails=0
for f in subs/*.srt; do
  lang=$(basename "$f" .srt)
  script=latin
  case "$lang" in
    ja|zh*|ko) script=cjk ;;
    ar|he|fa)  script=arabic ;;
    ru|uk|bg)  script=cyrillic ;;
    th)        script=thai ;;
  esac
  issues=$(python scripts/check_cps.py "$f" --script "$script" 2>&1)
  count=$(echo "$issues" | wc -l)
  echo "$lang: $count issues"
  if (( count > 5 )); then fails=$((fails+1)); fi
done
exit $fails
```

## Examples

### Example 1: 30-min lecture → 6-locale subtitles in 1 hour

**Goal:** EN source MP4; deliver SRT for DE, FR, JA, ZH, AR, KO + sidecar VTT for HTML5 player.

**Steps:**
1. Extract audio (Recipe 1) → `audio.wav` (16kHz mono).
2. Whisper.cpp transcribe (Recipe 2) → `subs/en.srt` (~15 min on M2 with large-v3).
3. Translate via DeepL (Recipe 4) for DE/FR; Subly (Recipe 5) for JA/ZH/AR/KO (better CJK + RTL handling). ~10 min total.
4. CPS validate per locale (Recipe 6) — JA and ZH need 16-char-per-line wrapping; AR needs RTL marker.
5. Auto-fix common issues: `SubtitleEdit /fixcommonerrors:RemoveEmptyLines,FixOverlappingDisplayTimes` per file.
6. Convert SRT → VTT for HTML5 (Recipe 7).
7. Embed in player markup (Recipe 12).
8. Optional: YouTube upload caption tracks (Recipe 13).

**Result:** 6 locales delivered in ~45 min compute + 15 min QA; CPS within band; sidecar VTT + SRT for both web and YouTube.

### Example 2: Course platform needs burn-in MP4s for offline distribution

**Goal:** Existing 50 lecture videos + en.srt; produce DE / JA / AR burned-in copies for offline distribution.

**Steps:**
1. Translate `en.srt` for DE / JA / AR via DeepL Pro Document API (preserves SRT structure).
2. CPS validate; manual-edit any cue > 21 CPS (DE expansion).
3. For AR: pre-tighten SRT (Arabic text is 30%+ wider; truncate lines that exceed 38 chars).
4. Burn-in loop (Recipe 10) with locale-appropriate Noto font:
   - DE: `Noto Sans`
   - JA: `Noto Sans JP`
   - AR: `Noto Sans Arabic` + ASS-level `\an2` alignment for RTL flow
5. Output: 50 × 4 locales × MP4 = 200 files; ~3 hrs compute on a workstation.
6. QA spot-check 10% of files: subs readable, no overflow, correct font per script.

**Result:** Offline-distributable localized videos; one MP4 per locale; no player config needed at the LMS.

## Edge cases / gotchas

- **Whisper hallucinates on silence** — phantom "Thanks for watching!" lines. Use `--no_speech_threshold 0.6` `--logprob_threshold -1.0`.
- **Whisper word timestamps drift** — `large-v3 + word_timestamps=True` is best; smaller models ±2s at clip ends.
- **CPS varies by script** — European 21 CPS applied to JA is unreadable. Use per-script limits (Recipe 6).
- **Arabic CPS** — count graphemes not codepoints (combining marks + ligatures). Python `regex` `\X` matches grapheme.
- **DeepL preserves XML tags** but not all SRT styling; verify `<i>`, `<b>` survive.
- **Subly free tier** — 5 min/mo; quality drops on heavy accents.
- **VTT positioning quirks in Safari** — `line:`, `align:` partly supported; test on iOS.
- **MP4 embedded subs (`mov_text`)** — limited player support. Prefer sidecar SRT/VTT.
- **MKV unplayable in stock iOS / Safari** — MP4+sidecar VTT for web; MKV for desktop/Plex.
- **Burn-in is destructive** — keep sidecar SRT alongside even when shipping burned-in.
- **Linux CI font rendering** — `apt-get install fonts-noto-cjk fonts-noto-color-emoji` before ffmpeg burn-in.
- **ASS escaping** — `\N` newline, `{}` style brackets; escape user text.
- **YouTube auto-translate** — poor quality on technical content; always upload explicit DeepL/Subly SRT.
- **TTML for Netflix** — IMSC 1.1 profile, line:5% rules; validate at https://sandflow.com/imsc1_1/.
- **Dubbing timing** — DE/FI/RU dubs ~30% longer; pre-shrink SRT or hand to video-creator for time-stretch.
- **HoH captions vs subtitles** — captions include `[door slams]`, `[music swells]`; use `kind="captions"`.
- **Forced narratives** — translation of on-screen signs/titles; separate VTT, `default` off.
- **Whisper.cpp model size** — large-v3 3GB, medium 1.5GB. CPU-only: `medium --threads 8` is sweet spot.
- **Diarization** — Whisper doesn't diarize; use whisperx or pyannote.audio.
- **Audio normalization** — `loudnorm` filter (Recipe 1) improves STT accuracy 5-10% on quiet sources.

## Sources

- Whisper: https://github.com/openai/whisper  +  whisper.cpp https://github.com/ggerganov/whisper.cpp  +  faster-whisper https://github.com/SYSTRAN/faster-whisper
- whisperx (diarization): https://github.com/m-bain/whisperX
- Subtitle Edit: https://github.com/SubtitleEdit/subtitleedit  + CLI docs https://www.nikse.dk/subtitleedit/help
- Aegisub: https://aegisub.org/  + manual http://docs.aegisub.org/
- Subly: https://www.getsubly.com/  + translator https://www.getsubly.com/features/subtitle-translator  + API https://docs.getsubly.com/
- ffmpeg subtitles filter: https://ffmpeg.org/ffmpeg-filters.html#subtitles-1
- pysubs2: https://pysubs2.readthedocs.io/  +  srt (Python) https://pypi.org/project/srt/
- WebVTT: https://www.w3.org/TR/webvtt1/  +  SRT https://en.wikipedia.org/wiki/SubRip  +  ASS/SSA http://www.tcax.org/docs/ass-specs.htm
- TTML2 / IMSC 1.1: https://www.w3.org/TR/ttml-imsc1.1/
- Netflix Timed Text Style Guide: https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617
- BBC Subtitle Guidelines: https://bbc.github.io/subtitle-guidelines/
- EBU Tech 3360 (broadcast reading speed): https://www.ebu.ch/publications/tech3360
- YouTube Data API captions: https://developers.google.com/youtube/v3/docs/captions
- HTML5 `<track>`: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/track
- ElevenLabs (dubbing handoff): https://elevenlabs.io/
