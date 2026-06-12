<!--
Source: https://github.com/ai/size-limit · https://knip.dev/
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# Bundle size — size-limit + Knip + analyzers

Measure first (`size-limit`, `@next/bundle-analyzer`, `rollup-plugin-visualizer`).
Fix by code-splitting (`React.lazy`, `next/dynamic`, route-level lazy), tree-
shaking (ESM-only deps, `sideEffects: false`), and dropping heavy deps
(moment → date-fns; lodash → es-toolkit; axios → fetch).

## When to use

- "First load JS is too big"
- CI bundle-size regression
- Choosing between two deps with similar features
- Cleaning up dead code in a 5-year-old codebase
- Trigger phrases: "bundle size", "first load", "code splitting", "lazy",
  "tree shaking", "dead code", "Knip", "size-limit", "bundle analyzer"

## Setup

```bash
# Measurement
pnpm add -D size-limit @size-limit/preset-app @size-limit/file
pnpm add -D knip

# Visualizers
pnpm add -D rollup-plugin-visualizer       # Vite
pnpm add -D @next/bundle-analyzer          # Next.js
pnpm add -D source-map-explorer            # CRA / generic

# Replacements
pnpm add date-fns es-toolkit               # lighter than moment/lodash
```

No API keys.

## Common recipes

### Recipe 1 — `size-limit` CI gate

```json
// package.json
{
  "size-limit": [
    {
      "name": "main bundle",
      "path": "dist/index-*.js",
      "limit": "100 kB",
      "gzip": true
    },
    {
      "name": "main bundle (uncompressed)",
      "path": "dist/index-*.js",
      "limit": "320 kB"
    },
    {
      "name": "vendor chunk",
      "path": "dist/vendor-*.js",
      "limit": "80 kB",
      "gzip": true
    }
  ],
  "scripts": {
    "size": "size-limit",
    "size:why": "size-limit --why"
  }
}
```

```bash
pnpm size           # CI gate — fails if any limit exceeded
pnpm size:why       # opens treemap of contributors
```

### Recipe 2 — Vite bundle visualizer

```ts
// vite.config.ts
import { visualizer } from "rollup-plugin-visualizer";

export default defineConfig({
  plugins: [
    visualizer({
      filename: "dist/stats.html",
      open: true,
      gzipSize: true,
      brotliSize: true,
      template: "treemap", // or "sunburst", "network"
    }),
  ],
});
```

`pnpm build` opens an interactive map showing what's eating bytes.

### Recipe 3 — Next.js bundle analyzer

```ts
// next.config.ts
import type { NextConfig } from "next";
import withBundleAnalyzer from "@next/bundle-analyzer";

const analyzer = withBundleAnalyzer({ enabled: process.env.ANALYZE === "true" });

const config: NextConfig = { /* ... */ };

export default analyzer(config);
```

```bash
ANALYZE=true pnpm build
# Opens .next/analyze/client.html
```

### Recipe 4 — Knip (unused code + deps + exports)

```jsonc
// knip.json
{
  "entry": ["src/main.tsx", "src/server/**/*.ts"],
  "project": ["src/**/*.{ts,tsx}"],
  "ignore": ["**/*.d.ts"],
  "ignoreDependencies": ["@types/*"]
}
```

```bash
pnpm exec knip --reporter compact
# Output: unused files, exports, deps, dev-deps, types
```

Run on CI; fail if any unused exports introduced. Knip also detects unused
npm scripts and config files.

### Recipe 5 — Route-level code splitting (Next App Router)

```tsx
// app/dashboard/page.tsx
import dynamic from "next/dynamic";

const HeavyChart = dynamic(() => import("@/components/HeavyChart"), {
  loading: () => <ChartSkeleton />,
  ssr: false,            // skip SSR if it touches window
});

export default function Dashboard() {
  return (
    <>
      <Header />
      <HeavyChart />
    </>
  );
}
```

`next/dynamic` returns a code-split component that loads on first render.

### Recipe 6 — `React.lazy` + Suspense

```tsx
import { lazy, Suspense } from "react";

const Editor = lazy(() => import("@/components/Editor"));

<Suspense fallback={<EditorSkeleton />}>
  <Editor />
</Suspense>
```

### Recipe 7 — Conditional dynamic import

```tsx
async function exportCSV() {
  const { utils, writeFile } = await import("xlsx"); // only loads when triggered
  const ws = utils.json_to_sheet(data);
  // ...
}
```

Heavy libs (xlsx, pdf-lib, html2canvas) should never sit in the main bundle.

### Recipe 8 — Tree-shake-friendly imports

```ts
// BAD — pulls the whole library
import _ from "lodash";
import * as dateFns from "date-fns";
import { Icon } from "@mui/material";

// GOOD — named imports from ESM packages
import { map, debounce } from "es-toolkit";    // (or lodash-es)
import { format, parseISO } from "date-fns";
import Icon from "@mui/material/Icon";          // package-internal deep import
```

### Recipe 9 — `sideEffects: false` in your own package

```json
// package.json (libraries you ship)
{
  "sideEffects": false,
  "exports": {
    ".": { "import": "./dist/index.js", "types": "./dist/index.d.ts" }
  }
}
```

Or list the side-effectful files:

```json
{ "sideEffects": ["**/*.css", "./src/polyfills.ts"] }
```

This unlocks tree-shaking for consumers.

### Recipe 10 — Replace heavy deps

| Heavy | Lightweight |
|---|---|
| moment (290kb) | date-fns / dayjs (12kb) |
| lodash (24kb after tree-shake) | es-toolkit (smaller, modern API) |
| axios (15kb gzip) | native `fetch` + tiny wrapper |
| chart.js (45kb gzip) | recharts (better tree-shake) or visx |
| @sentry/browser-tracing (40kb) | `@sentry/replay` separately, lazy-load |
| react-icons (full set) | `lucide-react` (icon-per-import) |
| jwt-decode (10kb) | `jose` if you need crypto, otherwise parse manually |

Audit with https://bundlephobia.com/ before adding any dep > 10kb gzip.

### Recipe 11 — Manual chunking (Vite)

```ts
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: (id) => {
          if (id.includes("node_modules/react/")) return "react";
          if (id.includes("node_modules/@tanstack")) return "tanstack";
          if (id.includes("node_modules/")) return "vendor";
        },
      },
    },
  },
});
```

Stable chunk names = better browser cache hit rate across releases.

### Recipe 12 — Preload critical chunks

```html
<link rel="modulepreload" href="/assets/react-abc123.js" />
<link rel="modulepreload" href="/assets/main-def456.js" />
```

Vite emits these automatically for `import()` you `<Suspense>` wrap.

## Examples

### Example 1: First Load JS > 200kb on Next.js

1. `ANALYZE=true pnpm build` — open report
2. Identify chunk hot-spots (e.g., `moment` showing 290kb)
3. Replace: `pnpm remove moment && pnpm add date-fns`
4. Codemod usages
5. Re-run analyzer → confirm chunk dropped
6. Add `size-limit` budget so it can't regress

### Example 2: Knip-driven cleanup

```bash
pnpm exec knip --reporter compact > knip-report.txt
# Review unused exports, files, deps
pnpm exec knip --fix          # auto-removes unused exports (review the diff!)
# Then manually:
pnpm remove $(grep -A 100 "Unused dependencies" knip-report.txt | head -20)
```

## Edge cases / gotchas

- **Tree-shaking only works on ESM** — CJS deps (`lodash` without `-es`) ship
  everything. Check `package.json` `type: "module"` or `exports` field.
- **Barrel files** (`export * from "./foo"`) defeat tree-shaking in some
  bundlers. Use explicit named re-exports.
- **`sideEffects: true`** (or missing) means bundlers can't drop unused
  exports. Set `false` in your packages.
- **Dynamic imports must be statically analyzable** — `import(varName)` works
  in modern bundlers but `import("./" + varName)` may not.
- **`React.lazy` requires `<Suspense>` ancestor** — without it, loading throws.
- **`next/dynamic` with `ssr: false`** doesn't render on server — pair with
  fallback skeleton.
- **Source maps inflate bundles** — `sourcemap: "hidden"` (Vite) emits maps to
  disk without referencing them in JS.
- **CSS bundle is separate** — size-limit may not measure it; use
  `@size-limit/file` or audit `dist/*.css` separately.
- **Knip flags re-exports as unused** if no entry point references them — list
  public-API entry points in `knip.json`.
- **Build-time CSS-in-JS** (Panda, vanilla-extract) has zero runtime weight;
  styled-components / Emotion have runtime ~10kb gzip.
- **Server Components ship zero JS** to the client — if a component doesn't
  need `useState`/`useEffect`, keep it as RSC.

## Sources

- [size-limit docs](https://github.com/ai/size-limit)
- [Knip docs](https://knip.dev/)
- [Bundle Phobia](https://bundlephobia.com/) — npm dep size lookup
- [@next/bundle-analyzer](https://www.npmjs.com/package/@next/bundle-analyzer)
- [rollup-plugin-visualizer](https://github.com/btd/rollup-plugin-visualizer)
- [es-toolkit](https://es-toolkit.slash.page/) — modern lodash replacement
- [Vite — Library mode](https://vitejs.dev/guide/build.html#library-mode)
- [Anthony Fu — Bundle analysis (2025)](https://antfu.me/) — recent posts
- [Vercel — Optimizing First Load JS](https://vercel.com/blog/) — Next-specific guide
