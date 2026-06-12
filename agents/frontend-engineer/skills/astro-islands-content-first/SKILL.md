<!--
Source: https://astro.build/blog/astro-5/ · https://docs.astro.build/
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# Astro 5 — Islands + Content Collections

Astro (5.x, Dec 2024) is the SOTA framework for content-heavy sites — marketing,
docs, blogs, e-commerce catalogues. Zero JS by default; opt in to hydration per
component. Content Collections v2 add zod-typed frontmatter. Server Islands
(4.12+) bring dynamic personalization inside static pages.

## When to use

- Content sites: docs, blogs, marketing, portfolios
- Multi-framework projects (React + Svelte + Vue components on one page)
- SEO-critical, fast-LCP pages
- Hybrid static + dynamic personalization (Server Islands)
- Trigger phrases: "Astro", "content site", "MDX blog", "Server Islands",
  "Content Collections", "Islands architecture", "client:load", "client:visible"

## Setup

```bash
# New Astro project (interactive prompts)
pnpm create astro@latest my-site
# choose: Empty / Blog template, TypeScript strict, install deps

cd my-site
pnpm install
pnpm dev

# Add framework integrations
pnpm dlx astro add react        # React 19 islands
pnpm dlx astro add svelte       # Svelte 5 islands
pnpm dlx astro add vue          # Vue 3 islands
pnpm dlx astro add tailwind     # Tailwind 4 (uses @tailwindcss/vite)
pnpm dlx astro add mdx          # MDX support
pnpm dlx astro add sitemap      # auto-sitemap
pnpm dlx astro add cloudflare   # Cloudflare adapter for SSR
```

Verify: `pnpm exec astro --version` → 5.x.

No API keys required.

## Common recipes

### Recipe 1 — Page with zero-JS islands

```astro
---
// src/pages/index.astro
import Counter from "../components/Counter.tsx";          // React island
import Newsletter from "../components/Newsletter.svelte"; // Svelte island
import Footer from "../components/Footer.vue";            // Vue island
const buildTime = new Date().toISOString();
---

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>My site</title>
  </head>
  <body>
    <h1>Hello</h1>
    <!-- Static — ships as zero JS -->
    <p>Built at {buildTime}</p>

    <!-- Islands — opt-in hydration per component -->
    <Counter client:load />              <!-- hydrate immediately -->
    <Newsletter client:visible />        <!-- hydrate when scrolled into view -->
    <Footer client:idle />               <!-- hydrate after browser idle -->
  </body>
</html>
```

Available directives: `client:load`, `client:idle`, `client:visible`,
`client:media="(max-width: 50em)"`, `client:only="react"` (skip SSR).

### Recipe 2 — Content Collections v2 (typed frontmatter)

```ts
// src/content.config.ts
import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const blog = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    pubDate: z.coerce.date(),
    description: z.string().max(160),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
```

```astro
---
// src/pages/blog/[slug].astro
import { getCollection, render } from "astro:content";

export async function getStaticPaths() {
  const posts = await getCollection("blog", ({ data }) => !data.draft);
  return posts.map(post => ({ params: { slug: post.id }, props: { post } }));
}

const { post } = Astro.props;
const { Content } = await render(post);
---

<html>
  <body>
    <article>
      <h1>{post.data.title}</h1>
      <time>{post.data.pubDate.toISOString().slice(0, 10)}</time>
      <Content />
    </article>
  </body>
</html>
```

### Recipe 3 — Server Islands (dynamic inside static)

```astro
---
// src/pages/index.astro — page is statically rendered at build...
import StaticHero from "../components/StaticHero.astro";
import LoggedInBanner from "../components/LoggedInBanner.astro";
---

<StaticHero />
<!-- ...except for this island, which renders per-request server-side -->
<LoggedInBanner server:defer>
  <p slot="fallback">Welcome!</p>
</LoggedInBanner>
```

```astro
---
// src/components/LoggedInBanner.astro
const user = await getUserFromCookie(Astro.cookies);
---

{user ? <p>Welcome back, {user.name}</p> : <p>Sign in</p>}
```

Static shell ships from CDN; the banner streams in per request.

### Recipe 4 — `<Image />` with built-in optimization

```astro
---
import { Image, Picture } from "astro:assets";
import hero from "../assets/hero.jpg";
---

<Image src={hero} alt="Hero" width={1920} height={1080} format="avif" loading="eager" />
<Picture src={hero} alt="Hero" formats={["avif", "webp"]} widths={[640, 1280, 1920]} sizes="(max-width: 768px) 100vw, 50vw" />
```

Astro uses `sharp` under the hood; outputs AVIF + WebP fallback.

### Recipe 5 — MDX blog post

```mdx
---
title: "Hello"
pubDate: 2026-06-01
description: "An MDX post."
---
import Counter from "../../components/Counter.tsx";

# Hello

This is **MDX**. Inline a React island:

<Counter client:visible />
```

Just add `pnpm dlx astro add mdx` first.

### Recipe 6 — File-based routing

```
src/pages/
  index.astro                # /
  about.astro                # /about
  blog/
    index.astro              # /blog (lists posts)
    [slug].astro             # /blog/[slug]
  api/
    posts.json.ts            # /api/posts.json (endpoint)
  [...catch].astro           # 404 catch-all
```

### Recipe 7 — API endpoint

```ts
// src/pages/api/posts.json.ts
import { getCollection } from "astro:content";
import type { APIRoute } from "astro";

export const GET: APIRoute = async () => {
  const posts = await getCollection("blog");
  return new Response(JSON.stringify(posts.map(p => p.data)), {
    headers: { "Content-Type": "application/json" },
  });
};
```

### Recipe 8 — View Transitions

```astro
---
import { ClientRouter } from "astro:transitions";
---
<html>
  <head>
    <ClientRouter />
  </head>
  <body>
    <a href="/blog">Blog</a>
    <main transition:name="main" transition:animate="slide">
      <slot />
    </main>
  </body>
</html>
```

Adds SPA-feel page transitions on top of MPA navigation. Falls back gracefully.

### Recipe 9 — Tailwind 4 integration

```js
// astro.config.mjs
import { defineConfig } from "astro/config";
import tailwind from "@tailwindcss/vite";

export default defineConfig({
  vite: { plugins: [tailwind()] },
});
```

```css
/* src/styles/global.css */
@import "tailwindcss";
```

```astro
---
import "../styles/global.css";
---
<body class="bg-slate-50 text-slate-900">
  <h1 class="text-3xl font-bold">Hello</h1>
</body>
```

### Recipe 10 — Deploy

```bash
# Static (default) — deploys anywhere
pnpm build && pnpm dlx vercel deploy --prod --prebuilt
pnpm build && pnpm dlx wrangler pages deploy ./dist
pnpm build && pnpm dlx netlify deploy --prod --dir=./dist

# SSR mode — add adapter first
pnpm dlx astro add cloudflare     # or vercel, netlify, node, deno
pnpm dlx wrangler pages deploy
```

## Examples

### Example 1: Markdown blog from scratch

```bash
pnpm create astro@latest my-blog -- --template blog --typescript strict --install
cd my-blog
pnpm dlx astro add mdx
pnpm dev
```

Drop posts into `src/content/blog/post-1.md` with frontmatter; the route
`/blog/post-1` renders automatically.

### Example 2: Hybrid static + dynamic personalized homepage

1. `pnpm dlx astro add cloudflare` (adapter for SSR)
2. Add `server:defer` to the dynamic component
3. `astro build && wrangler pages deploy ./dist`

Result: page is mostly served from CDN; the personalized island streams in.

## Edge cases / gotchas

- **Astro components don't ship JS** — `.astro` files are server-rendered HTML
  templates. Only `client:*` directives ship a framework runtime.
- **`client:only` skips SSR** — use for components that touch `window` /
  `document` (e.g., canvas, web audio). Cost: blank during initial paint.
- **Hydration cost** — each island ships its framework runtime. Mixing React +
  Vue + Svelte triples the JS. Prefer one framework per project.
- **`astro:content` queries are typed** but require running `astro sync` after
  schema changes (auto-runs in dev).
- **Server Islands require SSR mode** — set `output: "server"` or `"hybrid"` in
  `astro.config.mjs` and an adapter.
- **`Astro.cookies` / `Astro.request` only work in SSR** — static builds throw.
- **Image optimization needs `sharp`** — bundled by default; on Cloudflare Pages
  the `sharp` binary is too heavy → use `sharp: false` and rely on Cloudflare
  Images.
- **MDX components need `client:*`** to hydrate — without it they render as
  static markup only.
- **View Transitions need same-origin** — won't work for cross-domain links.

## Sources

- [Astro 5 announcement](https://astro.build/blog/astro-5/)
- [Islands architecture](https://docs.astro.build/en/concepts/islands/)
- [Content Collections v2](https://docs.astro.build/en/guides/content-collections/)
- [Server Islands](https://astro.build/blog/future-of-astro-server-islands/)
- [View Transitions](https://docs.astro.build/en/guides/view-transitions/)
- [Image optimization](https://docs.astro.build/en/guides/images/)
- [Astro Tutorial — official](https://docs.astro.build/en/tutorial/0-introduction/)
- [Fred Schott — Astro 5 keynote (2024)](https://www.youtube.com/@withastro)
