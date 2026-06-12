<!--
Source: https://tailwindcss.com/blog/tailwindcss-v4 · https://tailwindcss.com/docs
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# Tailwind CSS 4 — CSS architecture

Tailwind CSS 4 (stable Jan 2025) replaced the JS config with **CSS-first
`@theme`**, swapped PostCSS for the Rust-based **Lightning CSS** engine
(~10x faster), and gained automatic content detection. This skill also covers
when to prefer Panda, vanilla-extract, or UnoCSS instead.

## When to use

- New project — use Tailwind 4 by default for utility-first work
- Migrating from Tailwind 3 (run the upgrade tool)
- Choosing between Tailwind / Panda / vanilla-extract / UnoCSS for a design
  system
- Trigger phrases: "Tailwind", "Tailwind v4", "@theme", "Lightning CSS",
  "CSS-in-TS", "Panda", "vanilla-extract", "UnoCSS"

## Decision tree

| Need | Pick |
|---|---|
| Utility-first, fast iteration, ecosystem | **Tailwind 4** |
| Type-safe design tokens + zero-runtime + recipes (Chakra-like) | **Panda CSS** |
| Strictly typed CSS-in-TS, zero-runtime | **vanilla-extract** |
| Tailwind feel + smaller bundle + faster | **UnoCSS** |
| Component-scoped without a framework | **CSS Modules** |

## Setup — Tailwind 4 (Vite plugin path)

```bash
pnpm add tailwindcss @tailwindcss/vite
```

```ts
// vite.config.ts
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({ plugins: [tailwindcss()] });
```

```css
/* src/styles/app.css */
@import "tailwindcss";

@theme {
  --color-brand-50: #f0f9ff;
  --color-brand-500: #3b82f6;
  --color-brand-900: #1e3a8a;

  --font-sans: "Inter", "ui-sans-serif", system-ui;
  --font-mono: "JetBrains Mono", "ui-monospace";

  --spacing-128: 32rem;
  --radius-card: 0.75rem;
}
```

```tsx
import "./styles/app.css";
```

## Setup — Tailwind 4 (PostCSS path)

```bash
pnpm add tailwindcss @tailwindcss/postcss postcss
```

```js
// postcss.config.mjs
export default { plugins: { "@tailwindcss/postcss": {} } };
```

## Setup — Upgrade from Tailwind 3

```bash
pnpm dlx @tailwindcss/upgrade@latest
# - removes tailwind.config.js
# - migrates content paths
# - rewrites class names (gap-x-N → gap-N where applicable)
```

Verify: `pnpm list tailwindcss` → 4.x.

## Common recipes — Tailwind 4

### Recipe 1 — Custom theme tokens

```css
@import "tailwindcss";

@theme {
  --color-primary: oklch(0.72 0.18 250);
  --color-secondary: oklch(0.62 0.12 30);
  --breakpoint-3xl: 120rem;
}
```

Use as utilities: `bg-primary text-secondary`. Use the OKLCH color space —
better gamut, perceptually uniform.

### Recipe 2 — Dark mode (CSS-based, no config)

```css
@import "tailwindcss";

@custom-variant dark (&:where(.dark, .dark *));
```

```tsx
<html className={isDark ? "dark" : ""}>
  <body className="bg-white text-slate-900 dark:bg-slate-950 dark:text-slate-100">
    ...
  </body>
</html>
```

### Recipe 3 — Container queries (built in to v4)

```html
<div class="@container">
  <div class="grid grid-cols-1 @md:grid-cols-2 @xl:grid-cols-3">
    ...
  </div>
</div>
```

No plugin needed in v4.

### Recipe 4 — Group / peer / has / not utilities

```tsx
<label className="group flex items-center gap-2">
  <input type="checkbox" className="peer" />
  <span className="peer-checked:text-green-500 group-hover:underline">
    Subscribe
  </span>
</label>

<div className="not-data-[active]:opacity-50">...</div>
<div className="has-[:focus]:ring-2">...</div>
```

### Recipe 5 — Arbitrary values + named layers

```tsx
<div className="grid-cols-[200px_minmax(900px,1fr)_100px] [grid-template-areas:'sidebar_main_aux']">
  ...
</div>
```

```css
@layer components {
  .btn {
    @apply rounded px-4 py-2 font-medium;
  }
  .btn-primary {
    @apply btn bg-primary text-white hover:bg-primary/90;
  }
}
```

### Recipe 6 — Typography plugin for prose

```bash
pnpm add @tailwindcss/typography
```

```css
@import "tailwindcss";
@plugin "@tailwindcss/typography";
```

```tsx
<article className="prose prose-slate dark:prose-invert max-w-prose">
  <h1>Title</h1>
  <p>Body text styled automatically...</p>
</article>
```

### Recipe 7 — Animations + transitions

```tsx
<div className="transition-all duration-300 ease-out hover:scale-105 hover:shadow-xl" />

<div className="motion-safe:animate-pulse motion-reduce:animate-none" />
```

### Recipe 8 — Conditional className with `clsx` + `tailwind-merge`

```bash
pnpm add clsx tailwind-merge
```

```ts
// src/lib/cn.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

```tsx
import { cn } from "@/lib/cn";

function Button({ variant, className }: { variant: "primary" | "ghost"; className?: string }) {
  return (
    <button
      className={cn(
        "rounded px-4 py-2 font-medium",
        variant === "primary" && "bg-blue-600 text-white",
        variant === "ghost" && "bg-transparent text-blue-600 hover:bg-blue-50",
        className,
      )}
    />
  );
}
```

`twMerge` resolves conflicting Tailwind classes (`bg-red-500 bg-blue-500` →
`bg-blue-500`).

## Common recipes — Panda CSS

```bash
pnpm add -D @pandacss/dev
pnpm dlx panda init --postcss
```

```ts
// panda.config.ts
import { defineConfig } from "@pandacss/dev";

export default defineConfig({
  preflight: true,
  include: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      tokens: {
        colors: { brand: { value: "#3b82f6" } },
      },
    },
  },
  outdir: "styled-system",
});
```

```ts
// src/components/Card.tsx
import { css } from "../../styled-system/css";

export function Card() {
  return <div className={css({ bg: "brand", p: "4", rounded: "md", color: "white" })}>...</div>;
}
```

Build-time CSS-in-TS — zero runtime, fully typed tokens.

## Common recipes — vanilla-extract

```bash
pnpm add -D @vanilla-extract/css @vanilla-extract/vite-plugin
```

```ts
// vite.config.ts
import { vanillaExtractPlugin } from "@vanilla-extract/vite-plugin";
export default defineConfig({ plugins: [vanillaExtractPlugin()] });
```

```ts
// src/components/Button.css.ts
import { style } from "@vanilla-extract/css";

export const button = style({
  borderRadius: 6,
  padding: "0.5rem 1rem",
  background: "#3b82f6",
  color: "white",
});
```

```tsx
import * as styles from "./Button.css";
export const Button = (props) => <button className={styles.button} {...props} />;
```

Strictly typed, zero-runtime, type-checked at build.

## Common recipes — UnoCSS

```bash
pnpm add -D unocss
```

```ts
// vite.config.ts
import UnoCSS from "unocss/vite";
export default defineConfig({ plugins: [UnoCSS()] });
```

```ts
// uno.config.ts
import { defineConfig, presetUno } from "unocss";
export default defineConfig({ presets: [presetUno()] });
```

```tsx
import "virtual:uno.css";

export const App = () => <div className="p-4 bg-blue-500 text-white">UnoCSS</div>;
```

Tailwind-compatible syntax + faster + smaller. Good when Tailwind feels heavy.

## Examples

### Example 1: shadcn/ui-style design tokens in Tailwind 4

```css
@import "tailwindcss";

@theme {
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.15 0 0);
  --color-primary: oklch(0.4 0.18 250);
  --color-primary-foreground: oklch(0.98 0 0);
  --color-muted: oklch(0.96 0.005 250);
  --color-muted-foreground: oklch(0.5 0.02 250);
  --color-border: oklch(0.9 0.005 250);
  --radius: 0.5rem;
}

.dark {
  --color-background: oklch(0.15 0 0);
  --color-foreground: oklch(0.98 0 0);
  /* ... */
}
```

`shadcn` components reference these tokens (`bg-background`, `border-border`).

### Example 2: Migrate `tailwind.config.js` to CSS-first

**Before (v3):**
```js
module.exports = {
  theme: { extend: { colors: { brand: "#3b82f6" } } },
};
```

**After (v4):**
```css
@import "tailwindcss";

@theme {
  --color-brand: #3b82f6;
}
```

Delete `tailwind.config.js`. Content paths are detected automatically.

## Edge cases / gotchas

- **Tailwind 4 dropped IE 11 support** — uses native CSS cascade layers, OKLCH
  colors, container queries.
- **JS config not used by default** — opt back in with
  `@config "./tailwind.config.js";` only when needed.
- **Class name changes** — `gap-x-N` / `gap-y-N` → `gap-N` is one of many; run
  the upgrade tool, don't hand-edit.
- **`@apply` in Tailwind 4** still works but discouraged — prefer composing
  utilities in JSX with `cn()` helper.
- **`tailwind-merge` adds a few KB** — for tiny libs, write a manual override
  function or skip it (accept duplicate classes).
- **`@tailwindcss/vite` vs `@tailwindcss/postcss`** — Vite plugin is faster,
  but PostCSS path is needed if you compose with other PostCSS plugins
  (autoprefixer, postcss-nesting).
- **Dark mode `darkMode: 'class'`** is gone — use `@custom-variant dark` instead.
- **Mixing strategies** (Tailwind + styled-components + CSS Modules) creates
  specificity wars — pick one primary, document deviations.
- **Panda's `styled-system/` directory** must be regenerated after token changes
  (`pnpm dlx panda codegen`).
- **vanilla-extract requires a build-time plugin** — won't work in
  no-build-step projects.
- **Tailwind 4 breakpoints use new tokens** (`--breakpoint-md`) — overwriting
  in `@theme` adjusts every responsive variant.

## Sources

- [Tailwind CSS 4 announcement](https://tailwindcss.com/blog/tailwindcss-v4)
- [Tailwind CSS 4 docs](https://tailwindcss.com/docs)
- [Tailwind upgrade guide](https://tailwindcss.com/docs/upgrade-guide)
- [Panda CSS docs](https://panda-css.com/docs)
- [vanilla-extract docs](https://vanilla-extract.style/)
- [UnoCSS docs](https://unocss.dev/)
- [Adam Wathan — Tailwind 4 walkthrough](https://www.youtube.com/@TailwindLabs) — official channel
- [Frontend Masters — Tailwind in 2025](https://frontendmasters.com/blog/) — recent best-practices
