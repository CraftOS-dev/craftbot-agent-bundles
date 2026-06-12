# Remotion — Programmatic Video in React/TSX

## When to use
- Frame-accurate keyframe animation (a designer-grade alternative to AE/MOGRT)
- Text-heavy explainer videos with deterministic layouts
- Batch / template-driven content (parameterized data → N renders)
- Cubic-bezier easing curves the agent can tune precisely
- Particle FX / 3D via `@remotion/three`
- Anywhere CapCut/Premiere would require GUI clicks — Remotion replaces them with code

Skip when: input is a single timeline cut-and-stitch (use FFmpeg `concat`); the user needs to interactively grade in DaVinci.

## Setup
```bash
# In project root
npm create video@latest -- --template hello-world myvideo
cd myvideo
npm install
# OR add to existing project:
npm install remotion @remotion/cli @remotion/three @remotion/lottie @remotion/google-fonts
```
Render binary lives at `node_modules/.bin/remotion`. Invoke via `npx remotion render`.

## Common recipes

### 1. Minimal composition (TSX)
```tsx
// src/Composition.tsx
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";
export const Hero: React.FC<{ title: string }> = ({ title }) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    easing: Easing.bezier(0.25, 0.1, 0.25, 1),
    extrapolateRight: "clamp",
  });
  return (
    <AbsoluteFill style={{ background: "#000", justifyContent: "center", alignItems: "center" }}>
      <h1 style={{ color: "#fff", fontSize: 120, opacity }}>{title}</h1>
    </AbsoluteFill>
  );
};
```

### 2. Register composition
```tsx
// src/Root.tsx
import { Composition } from "remotion";
import { Hero } from "./Composition";
export const RemotionRoot = () => (
  <Composition
    id="Hero"
    component={Hero}
    durationInFrames={120}     // 4s @ 30fps
    fps={30}
    width={1080}
    height={1920}              // vertical 9:16
    defaultProps={{ title: "I QUIT MY JOB" }}
  />
);
```

### 3. Render
```bash
npx remotion render src/index.tsx Hero out.mp4
# Specify codec, concurrency, crf:
npx remotion render src/index.tsx Hero out.mp4 \
  --codec=h264 --crf=18 --concurrency=8 \
  --props='{"title":"WAIT FOR IT"}'
```

### 4. Easing presets (the soul of motion)
```tsx
Easing.linear                          // bad default; mechanical
Easing.ease                            // CSS default; ok-ish
Easing.bezier(0.25, 0.1, 0.25, 1)      // smooth ease-in-out
Easing.bezier(0.68, -0.55, 0.27, 1.55) // back / overshoot
Easing.elastic(2)                      // bounce
Easing.out(Easing.exp)                 // exponential ease-out (snappy)
```
Rule from `role.md`: linear feels mechanical — use ease-in/out for natural motion, overshoot for liveliness.

### 5. Sequenced clips
```tsx
import { Sequence } from "remotion";
export const Reel = () => (
  <>
    <Sequence durationInFrames={60}>{/* Clip A 0-2s */}<ClipA /></Sequence>
    <Sequence from={60} durationInFrames={60}>{/* Clip B 2-4s */}<ClipB /></Sequence>
    <Sequence from={120} durationInFrames={60}><ClipC /></Sequence>
  </>
);
```

### 6. Audio embed
```tsx
import { Audio, staticFile } from "remotion";
<Audio src={staticFile("vo.mp3")} volume={0.8} />
```
Static assets live in `public/`. Volume can be a function of frame for ducking.

### 7. Text animation patterns
```tsx
// Typewriter
const charsShown = Math.floor(interpolate(frame, [0, 60], [0, text.length]));
return <h1>{text.slice(0, charsShown)}</h1>;

// Slide-up entrance with ease-out
const y = interpolate(frame, [0, 20], [200, 0], { easing: Easing.out(Easing.exp), extrapolateRight: "clamp" });
return <h1 style={{ transform: `translateY(${y}px)` }}>{text}</h1>;
```

### 8. Particle FX via `@remotion/three`
```tsx
import { ThreeCanvas } from "@remotion/three";
import { Points, PointMaterial } from "@react-three/drei";
<ThreeCanvas><Points positions={positions}><PointMaterial color="#fff" size={0.05} /></Points></ThreeCanvas>
```

### 9. Image / video clip embed
```tsx
import { Img, Video, staticFile } from "remotion";
<Img src={staticFile("hero.png")} />
<Video src={staticFile("broll.mp4")} startFrom={30} endAt={150} />
```

### 10. Parameterized batch render (data → N videos)
```bash
for ROW in $(cat campaigns.jsonl); do
  TITLE=$(echo $ROW | jq -r .title)
  OUT=$(echo $ROW | jq -r .out)
  npx remotion render src/index.tsx Hero "out/$OUT.mp4" --props="$ROW"
done
```

### 11. Lambda render (cloud, parallel)
```bash
npx remotion lambda render --function-name=remotion-render-prod \
  --serve-url=https://your-bucket.s3/site \
  --composition=Hero --output=s3://outputs/hero.mp4
```

### 12. Lottie integration
```tsx
import { Lottie } from "@remotion/lottie";
import animation from "./loading.json";
<Lottie animationData={animation} />
```

### 13. Subtitle burn-in via Remotion (alternative to FFmpeg)
Parse SRT into array of `{from, to, text}`. Map to `Sequence` blocks with `durationInFrames=(to-from)*fps`.

### 14. Programmatic FFmpeg post-pass
After `remotion render` produces `out.mp4`, call FFmpeg for color grade or platform-export (see `ffmpeg-color-grading`, `ffmpeg-multi-platform-export`).

### 15. Frame-rate choice
- 30 fps — default for vertical short-form
- 60 fps — sports / gaming / smooth-motion content
- 24 fps — cinematic feel for long-form

## Examples

### A. 6-second TikTok hook (typewriter + slide-in)
```tsx
// 0-30: typewriter title; 30-60: B-roll image slides in; 60-180: VO continues
```
`durationInFrames={180}` @ 30fps = 6s. Render: `npx remotion render src/index.tsx Hook hook.mp4 --crf=18`. Wrap in `cli-anything` call.

### B. Batch — 50 testimonial videos
Input CSV with `{name, quote, headshot_url}`. Loop → render 50 9:16 vertical videos with consistent template. Total render: ~30 min on 8-core, fully parametric.

### C. Data viz explainer
React component reads JSON, renders chart frame-by-frame with d3-shape interpolated values. Result: animated chart that's pixel-accurate, no AE required.

### D. Particle reveal intro
`@remotion/three` particles converge into logo over 2 seconds, ease-out elastic. Renders to MP4 ready for FFmpeg color pass.

## Edge cases / gotchas

1. **`Easing.linear` is the wrong default.** Always specify a bezier or named easing.
2. **`useCurrentFrame()` only inside a composition's render tree.** Calling at top-level throws.
3. **`staticFile()` is required for public assets.** Plain `./hero.png` doesn't resolve in render.
4. **Codec matters.** `--codec=h264` for MP4. For lossless interim, `--codec=prores`. H.265 (`--codec=h265`) supported but slower.
5. **Concurrency caps at CPU cores.** `--concurrency=8` on 4-core wastes context-switches.
6. **Audio sync drift** if `Audio` start frame doesn't align with `Sequence from=`. Always test 30s+ audio for drift.
7. **No GPU acceleration by default.** Lambda is much faster for parallel batches.
8. **Fonts must be loaded.** `@remotion/google-fonts/Inter` import + `loadFont()` call, or fonts render as fallback.
9. **`extrapolateRight: "clamp"`** prevents `interpolate` from overshooting your target after the end frame — almost always what you want.
10. **`durationInFrames` must be set per composition.** Frames, not seconds. Convert: `seconds × fps`.
11. **CRF lower = higher quality.** 18 = visually lossless; 23 = default; 28 = small file, visible compression.
12. **Lambda quotas.** AWS Lambda has 15-min max per invocation; long renders must be split.

## Sources
- https://www.remotion.dev/docs/renderer
- https://www.remotion.dev/docs/animating-properties
- https://www.remotion.dev/docs/easing
- https://www.remotion.dev/docs/three
- https://www.remotion.dev/docs/lambda
