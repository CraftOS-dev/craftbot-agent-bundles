<!--
Source: https://web.dev/articles/vitals · https://github.com/GoogleChrome/web-vitals
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# Core Web Vitals — LCP, INP, CLS

INP **replaced FID in March 2024**. The three core metrics for 2026: **LCP**
(load — < 2.5s), **INP** (interactivity — < 200ms), **CLS** (layout stability
— < 0.1). This skill measures + diagnoses + fixes each one with the modern
toolchain.

## When to use

- "The app feels slow" / "Lighthouse score is bad"
- Pre-launch performance gate
- Production INP regression (most common 2025 issue)
- Setting up RUM (real-user monitoring) for Vitals
- Trigger phrases: "Core Web Vitals", "LCP", "INP", "CLS", "Lighthouse",
  "performance", "slow page", "long task", "layout shift"

## Setup

```bash
# Measurement
pnpm add web-vitals                          # RUM
pnpm add -D @lhci/cli                        # Lighthouse CI
pnpm add -D million                          # React VDOM optimizer (optional)

# Bundle analysis (related)
pnpm add -D rollup-plugin-visualizer
pnpm add -D @next/bundle-analyzer            # Next-specific
```

Optional: PageSpeed Insights API key (free, register at
https://developers.google.com/speed/docs/insights/v5/get-started).

## Common recipes

### Recipe 1 — Wire `web-vitals` for RUM

```ts
// src/lib/vitals.ts
import { onLCP, onINP, onCLS, onFCP, onTTFB } from "web-vitals";

function send(metric: { name: string; value: number; id: string; rating: string }) {
  const body = JSON.stringify(metric);
  if (navigator.sendBeacon) {
    navigator.sendBeacon("/api/vitals", body);
  } else {
    fetch("/api/vitals", { method: "POST", body, keepalive: true });
  }
}

onLCP(send);
onINP(send);
onCLS(send);
onFCP(send);
onTTFB(send);
```

```tsx
// app/layout.tsx — import once (it's a side effect)
import "@/lib/vitals";
```

### Recipe 2 — Lighthouse CI on every PR

```js
// lighthouserc.cjs
module.exports = {
  ci: {
    collect: {
      startServerCommand: "pnpm start",
      url: ["http://localhost:3000/", "http://localhost:3000/blog"],
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        "largest-contentful-paint": ["error", { maxNumericValue: 2500 }],
        "interaction-to-next-paint": ["error", { maxNumericValue: 200 }],
        "cumulative-layout-shift": ["error", { maxNumericValue: 0.1 }],
        "total-blocking-time": ["warn", { maxNumericValue: 300 }],
      },
    },
    upload: { target: "temporary-public-storage" },
  },
};
```

```bash
pnpm exec lhci autorun
```

### Recipe 3 — PageSpeed Insights (synthetic + CrUX field data)

```bash
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&strategy=mobile&category=PERFORMANCE&key=$PSI_KEY" | jq .lighthouseResult.audits."metrics".details.items[0]
```

## LCP fixes

### Recipe 4 — Identify the LCP element

Chrome DevTools → Performance → record → look for "Largest Contentful Paint"
marker. The element is annotated in the trace.

### Recipe 5 — Preload the LCP image

```tsx
// Next 15 — set `priority` on the LCP image
import Image from "next/image";

<Image src="/hero.webp" alt="..." width={1920} height={1080} priority />
```

```html
<!-- Or manual preload -->
<link
  rel="preload"
  as="image"
  href="/hero.webp"
  imagesrcset="/hero-mobile.webp 640w, /hero.webp 1920w"
  imagesizes="100vw"
/>
```

### Recipe 6 — Serve AVIF/WebP, never JPEG/PNG above-the-fold

```tsx
// Next.js
<Image src="/hero.jpg" alt="..." width={1920} height={1080} formats={["image/avif", "image/webp"]} />

// Astro
import hero from "../assets/hero.jpg";
<Image src={hero} alt="..." format="avif" />
```

### Recipe 7 — Self-host fonts (avoid blocking network request)

```tsx
// app/layout.tsx
import { Inter } from "next/font/google";
const inter = Inter({ subsets: ["latin"], display: "swap" });
export default function Layout({ children }) {
  return <html className={inter.className}><body>{children}</body></html>;
}
```

`next/font` self-hosts at build, no Google Fonts CDN round-trip.

### Recipe 8 — Move to the edge

```ts
// Next 15 route
export const runtime = "edge";   // ~50ms TTFB globally
```

For static sites, deploy to Cloudflare Pages or Vercel Edge Network.

## INP fixes

### Recipe 9 — Identify slow interactions

Chrome DevTools → Performance panel → enable "Interactions" track → record a
user flow. Each interaction shows total time. Look for any > 200ms.

### Recipe 10 — Break up long tasks with `scheduler.postTask`

```ts
async function processItems(items: Item[]) {
  for (const item of items) {
    await scheduler.yield(); // give the main thread a chance
    process(item);
  }
}

// Or schedule lower-priority work
scheduler.postTask(() => doExpensive(), { priority: "background" });
```

Polyfill: https://github.com/GoogleChromeLabs/scheduler-polyfill.

### Recipe 11 — Move heavy work to a Web Worker

```ts
// src/workers/parser.ts
self.onmessage = (e: MessageEvent<string>) => {
  const parsed = expensiveParse(e.data);
  postMessage(parsed);
};
```

```ts
// In a component
const worker = new Worker(new URL("@/workers/parser.ts", import.meta.url), { type: "module" });
worker.onmessage = (e) => setResult(e.data);
worker.postMessage(rawInput);
```

Use Comlink for ergonomic worker APIs:

```bash
pnpm add comlink
```

### Recipe 12 — `useTransition` for non-urgent state

```tsx
const [isPending, startTransition] = useTransition();

<input
  onChange={(e) => {
    setQuery(e.target.value);                  // urgent — update input value
    startTransition(() => {
      setFilteredList(filter(items, e.target.value)); // non-urgent — re-render list
    });
  }}
/>
```

### Recipe 13 — Million.js (auto-optimize React)

```bash
pnpm add million
```

```ts
// next.config.ts
import million from "million/compiler";

export default million.next({
  experimental: { ppr: true },
}, { auto: true });
```

Million wraps slow React components in a faster reconciler. 30-70% INP wins
in heavy list-rendering scenarios.

## CLS fixes

### Recipe 14 — Set `width` + `height` on every image / iframe

```tsx
// Even if you don't render at intrinsic size, set them — reserves space.
<Image src="/avatar.jpg" alt="..." width={64} height={64} />
<iframe src="https://www.youtube.com/embed/..." width="560" height="315" />
```

### Recipe 15 — `aspect-ratio` CSS for responsive media

```css
.responsive-image {
  width: 100%;
  height: auto;
  aspect-ratio: 16 / 9;
}
```

### Recipe 16 — Reserve space for late-loading content

```css
.ad-slot {
  min-height: 250px; /* match the size of the ad before it loads */
}
```

### Recipe 17 — Match fallback font metrics

```css
@font-face {
  font-family: "Inter Fallback";
  src: local("Arial");
  size-adjust: 107%;
  ascent-override: 90%;
  descent-override: 22%;
  line-gap-override: 0%;
}
```

`next/font` does this automatically; manually use https://screenspan.net/fallback
to compute values.

### Recipe 18 — Don't insert above existing content after load

```tsx
// BAD — newsletter banner appears above hero AFTER page load → CLS
<>
  <NewsletterBanner />     {/* lazy-fetches, then appears */}
  <Hero />
</>

// GOOD — fetch on the server / render hidden / use sticky bottom toast
<Hero />
<NewsletterBanner className="fixed bottom-0" />
```

## Examples

### Example 1: Lighthouse failed `largest-contentful-paint`

1. Find LCP element in trace
2. If image → add `priority` and switch to AVIF/WebP
3. If text → reduce blocking JS/CSS; use `next/font` for the font
4. Re-run Lighthouse, expect LCP drop of 1-2s

### Example 2: INP regression at p75

1. Open DevTools Performance, record clicking the slow button
2. Long task identified in a synchronous loop
3. Wrap in `startTransition` or `scheduler.postTask`
4. Verify with Performance trace: longest task < 50ms

## Edge cases / gotchas

- **INP is "worst" interaction**, not "average" — one bad interaction tanks
  the metric.
- **Field data vs lab data** — CrUX data (real users) is what Google ranks on.
  Lighthouse lab is a simulation. They can disagree.
- **Lighthouse runs on simulated Slow 4G + 4x CPU throttling** — match by
  setting your local DevTools to match conditions.
- **`priority` on multiple images** defeats the purpose — only the LCP image
  should have `priority`.
- **`loading="lazy"` on the LCP image** delays it. Set `loading="eager"` (or
  `priority` in Next).
- **Third-party scripts** (analytics, A/B testing) often dominate INP. Audit
  with the Performance panel's "Third parties" filter.
- **PartyTown** moves third-party JS to a Web Worker — useful when you can't
  remove the script.
- **`fetchpriority="high"`** on `<img>` and `<link>` boosts priority — use
  for LCP image. (Built into `next/image priority`.)
- **CLS is cumulative across the session** — one big shift early + small ones
  later all count.
- **`100vh` on iOS Safari** triggers CLS when address bar collapses — use
  `100svh` (small viewport) or JS-based viewport calc.
- **Animated dimensions** (transform/opacity-only) don't trigger CLS. Animate
  with `transform`, never `top`/`left`/`width`/`height`.

## Sources

- [web.dev — Core Web Vitals](https://web.dev/articles/vitals)
- [web.dev — INP](https://web.dev/articles/inp)
- [web.dev — Optimize LCP](https://web.dev/articles/optimize-lcp)
- [web.dev — Optimize CLS](https://web.dev/articles/optimize-cls)
- [web-vitals library](https://github.com/GoogleChrome/web-vitals)
- [Lighthouse CI docs](https://github.com/GoogleChrome/lighthouse-ci)
- [Million.js](https://million.dev/)
- [Scheduler API](https://developer.mozilla.org/en-US/docs/Web/API/Scheduler/postTask)
- [Chrome DevTools — Performance panel guide](https://developer.chrome.com/docs/devtools/performance/)
- [Vercel Speed Insights (2025)](https://vercel.com/docs/speed-insights) — RUM dashboard
