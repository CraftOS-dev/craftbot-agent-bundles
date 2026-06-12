# FFmpeg Audio Mastering — Broadcast-Spec Voice + Mix

## When to use
- You need to hit **-14 LUFS / ≤ -1 dBFS** (YouTube / Spotify / TikTok normalization target)
- Voice cleanup: high-pass, clarity EQ, compander
- BGM ducking under voice (sidechain compression)
- SFX mixing
- Batch normalization of an asset folder

## Setup
- `ffmpeg-mcp-advanced` MCP is the primary path
- Direct CLI via `cli-anything` + system `ffmpeg`
- For ElevenLabs Voice Isolator (better noise reduction than FFmpeg afftdn), see `elevenlabs-voice-production`

## Common recipes

### 1. Two-pass `loudnorm` (THE broadcast standard recipe)
Pass 1 — analyze:
```bash
ffmpeg -i in.wav -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null - 2> pass1.log
```
Parse the JSON at end of `pass1.log` for `input_i`, `input_tp`, `input_lra`, `input_thresh`, `target_offset`.

Pass 2 — apply with measured values:
```bash
ffmpeg -i in.wav -af "loudnorm=I=-14:TP=-1:LRA=11:measured_I=-22.5:measured_TP=-9.2:measured_LRA=8.1:measured_thresh=-32.8:offset=-0.4:linear=true:print_format=summary" -ar 48000 out.wav
```
- `I=-14`: integrated loudness target (LUFS)
- `TP=-1`: true peak (dBFS)
- `LRA=11`: loudness range
- `linear=true`: linear normalization (no dynamic compression)
Output: matches YouTube/Spotify/TikTok normalization without them re-touching it.

### 2. Voice chain — high-pass + clarity EQ + compander
```bash
ffmpeg -i raw_vo.wav -af "
  highpass=f=100,
  equalizer=f=3000:t=q:w=1:g=3,
  equalizer=f=8000:t=q:w=2:g=2,
  compand=attacks=0.01:decays=0.3:points=-70/-50|-30/-15:soft-knee=6:gain=0
" -ar 48000 voice_clean.wav
```
- `highpass=f=100`: cut mud + room rumble (80–120 Hz per role.md)
- `equalizer=f=3000:g=3`: boost clarity band (2–5 kHz)
- `equalizer=f=8000:g=2`: subtle air
- `compand`: 3:1-4:1 compression (per role.md), soft-knee for natural

### 3. De-essing
```bash
ffmpeg -i voice.wav -af "deesser=i=0.1:f=0.5:m=0.5" deessed.wav
```
Or use a narrow notch: `equalizer=f=6500:t=q:w=2:g=-4`.

### 4. Voice → BGM ducking (sidechain compression)
```bash
ffmpeg -i bgm.wav -i voice.wav -filter_complex "
  [0:a][1:a]sidechaincompress=threshold=0.05:ratio=8:attack=5:release=200:makeup=2[ducked];
  [ducked][1:a]amix=inputs=2:duration=longest:dropout_transition=2
" -c:a aac -b:a 256k mix.m4a
```
- `threshold=0.05`: voice level above which to duck
- `ratio=8`: aggressive duck (8:1)
- `attack=5ms`, `release=200ms`: snappy duck-in, smooth release

### 5. Three-track mix (voice + BGM + SFX) with proper bus levels
```bash
ffmpeg \
  -i voice.wav -i bgm.wav -i sfx.wav \
  -filter_complex "
    [0:a]volume=0dB[v];
    [1:a]volume=-18dB[b];
    [2:a]volume=-12dB[s];
    [b][v]sidechaincompress=threshold=0.05:ratio=6:attack=5:release=200[bd];
    [v][bd][s]amix=inputs=3:duration=longest:weights='1 1 0.8'[mix];
    [mix]loudnorm=I=-14:TP=-1:LRA=11
  " -c:a aac -b:a 256k -ar 48000 final.m4a
```
This hits role.md mix-balance levels (voice -12 to -6 dB, BGM -24 to -18 dB, SFX -18 to -12 dB) and ends at -14 LUFS.

### 6. Noise reduction (afftdn)
```bash
ffmpeg -i noisy.wav -af "afftdn=nr=15:nf=-25" cleaned.wav
```
- `nr`: noise reduction in dB (10–20 is sane; 30+ creates artifacts)
- `nf`: noise floor in dB (lower = more aggressive)
For better quality use ElevenLabs Voice Isolator (skill: `elevenlabs-voice-production`).

### 7. Audio normalize to peak only (`-1 dBFS`)
```bash
ffmpeg -i in.wav -af "alimiter=limit=0.891" out.wav   # 0.891 = -1 dBFS
```

### 8. Extract audio from video
```bash
ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 48000 voice.wav
```

### 9. Mux mastered audio back into video
```bash
ffmpeg -i video.mp4 -i mastered.m4a -map 0:v -map 1:a -c:v copy -c:a copy -shortest final.mp4
```

### 10. Batch normalize a folder
```bash
for F in raw/*.wav; do
  OUT="mastered/$(basename $F)"
  # 2-pass loudnorm wrapped — first run prints analysis
  ffmpeg -i "$F" -af loudnorm=I=-14:TP=-1:LRA=11 -ar 48000 "$OUT"
done
```
(Single-pass is fast; 2-pass is precise — use 2-pass for hero VO.)

### 11. Music-only video target (different bus balance)
- Music: -12 to -6 dB
- SFX: -18 to -12 dB
- Final loudness still -14 LUFS

### 12. Stereo widening (Mid-Side)
```bash
ffmpeg -i mono.wav -af "haas" wide.wav
```
Subtle widening for BGM.

### 13. Phase-correct mixdown to mono (when delivering to phones)
```bash
ffmpeg -i stereo.wav -ac 1 -af "pan=mono|c0=0.5*c0+0.5*c1" mono.wav
```

### 14. Crossfade between two tracks
```bash
ffmpeg -i a.wav -i b.wav -filter_complex "[0][1]acrossfade=d=2:c1=tri:c2=tri" xf.wav
```

### 15. Auto-trim silence
```bash
ffmpeg -i voice.wav -af "silenceremove=start_periods=1:start_silence=0.5:start_threshold=-50dB:detection=peak" trimmed.wav
```

## Examples

### A. Talking-head VO master
1. Capture raw `voice.wav` (mic + treated room).
2. ElevenLabs Voice Isolator pass for serious noise.
3. FFmpeg voice chain (recipe 2).
4. Mix with BGM + SFX (recipe 5).
5. Two-pass loudnorm (recipe 1) → final delivery.

### B. Music-led TikTok
1. ElevenLabs Multilingual v2 generates 8s VO.
2. Suno generates 30s BGM.
3. FFmpeg recipe 4 ducks BGM under VO.
4. Loudnorm pass to -14 LUFS.

### C. Batch dubbed-language exports
1. ElevenLabs Multilingual dubbing for each language (`en`, `es`, `pt`, `de`).
2. For each: FFmpeg recipe 5 to remix at language-specific levels.
3. Mux back into the video → 4 language SKUs.

### D. Quick podcast normalize
```bash
ffmpeg -i ep.wav -af "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11" ep_master.wav
```
Podcast target -16 LUFS (per Apple/Spotify spec) vs -14 for video.

## Edge cases / gotchas

1. **`loudnorm` single-pass is approximate.** Always 2-pass for hero deliverables.
2. **`-ar 48000`** is the broadcast/video standard. 44.1k is for music masters. Pick one and stick to it across the project to avoid resampling artifacts.
3. **`amix=inputs=N`** auto-attenuates by `1/N` by default. Use `weights='1 0.5 0.3'` to override.
4. **Sidechain `threshold` is amplitude (0–1), not dB.** 0.05 ≈ -26 dB.
5. **`compand` syntax** uses `|` not `,` to separate breakpoints in newer FFmpeg builds.
6. **`afftdn` artifacts** on speech with vibrato sound underwater — keep `nr` below 20.
7. **`loudnorm=linear=true`** is preferred for hero VO; `linear=false` does additional compression you may not want.
8. **AAC encoder quality.** Use `-c:a aac -b:a 256k` (libfdk_aac is better, but GPL-incompatible in most builds).
9. **Loudness "drift" across long files.** `loudnorm` is integrated — for a 60-min podcast it averages, so brief loud SFX won't blow it out.
10. **TikTok normalizes to -14 LUFS but caps TP at -2 dBFS** post-platform-encode — your -1 TP master is fine; their downstream encoder eats 1 dB.
11. **`silenceremove` thresholds are sensitive** — -50 dB threshold can swallow soft breaths. Try -45.
12. **`amix` with mismatched sample rates** silently resamples. Pre-resample all inputs to 48k.

## Sources
- https://ffmpeg.org/ffmpeg-filters.html#loudnorm
- https://ffmpeg.org/ffmpeg-filters.html#compand
- https://ffmpeg.org/ffmpeg-filters.html#sidechaincompress
- https://ffmpeg.org/ffmpeg-filters.html#afftdn
- https://support.google.com/youtube/answer/9890749 (YouTube loudness norm)
- https://artists.spotify.com/en/help/article/loudness-normalization
