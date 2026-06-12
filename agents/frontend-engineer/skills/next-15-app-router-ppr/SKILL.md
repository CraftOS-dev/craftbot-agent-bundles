<!--
Source: https://nextjs.org/blog/next-15 · https://nextjs.org/docs
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# Next.js 15 — App Router, PPR, Turbopack

Next 15 (Oct 2024) made App Router the only first-class option, shipped
**Partial Prerendering (PPR)** stable in Nov 2024, made Turbopack the default
dev bundler (and stable for `next build`), and changed `cookies()` / `headers()`
/ `params` / `searchParams` to async.

## When to use

- Scaffolding any production Next.js app in 2026
- Migrating from Pages Router (`pages/`) to App Router (`app/`)
- Reaching for fastest dev iteration (Turbopack > webpack)
- Deciding between SSR / SSG / ISR / PPR (PPR is the answer for most hybrid pages)
- Trigger phrases: "Next.js", "App Router", "PPR", "Partial Prerendering",
  "Turbopack", "Server Action", "middleware.ts", "Vercel deploy"

## Setup

```bash
# New project — App Router + Tailwind + TypeScript
pnpm dlx create-next-app@latest my-app \
  --typescript --app --tailwind --turbopack --src-dir

cd my-app
pnpm dev      # uses Turbopack by default in Next 15
```

Upgrade an existing app:

```bash
pnpm add next@latest react@latest react-dom@latest
pnpm dlx @next/codemod@latest upgrade latest
```

Verify: `pnpm next --version` → 15.x.

No API keys required. For deploy: `VERCEL_TOKEN` (or use git integration).

## Common recipes

### Recipe 1 — Bootstrap `next.config.ts` with PPR

```ts
// next.config.ts (TypeScript config is supported in Next 15)
import type { NextConfig } from "next";

const config: NextConfig = {
  experimental: {
    ppr: "incremental", // opt-in per-route via `export const experimental_ppr = true`
    reactCompiler: true, // React 19 compiler — auto memoization
  },
  images: {
    formats: ["image/avif", "image/webp"],
    remotePatterns: [{ protocol: "https", hostname: "**.cdn.example.com" }],
  },
};

export default config;
```

### Recipe 2 — File conventions cheat sheet

```
app/
  layout.tsx          # root layout (must define <html> + <body>)
  page.tsx            # /
  loading.tsx         # streaming Suspense fallback
  error.tsx           # error boundary (client component)
  not-found.tsx       # 404 UI
  global-error.tsx    # root-level fallback (replaces root layout on crash)
  template.tsx        # like layout but remounts on navigation
  middleware.ts       # edge runtime, runs before render
  app/blog/
    page.tsx          # /blog
    [slug]/
      page.tsx        # /blog/[slug]
      opengraph-image.tsx  # dynamic OG image
  app/api/webhook/
    route.ts          # Route Handler (POST/GET exports)
```

### Recipe 3 — Async dynamic APIs (BREAKING CHANGE from Next 14)

```tsx
// app/posts/[slug]/page.tsx
import { cookies, headers } from "next/headers";

export default async function Post({
  params,
  searchParams,
}: {
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ ref?: string }>;
}) {
  const [{ slug }, { ref }, cookieStore, hdrs] = await Promise.all([
    params,
    searchParams,
    cookies(),
    headers(),
  ]);
  const theme = cookieStore.get("theme")?.value ?? "light";
  const ua = hdrs.get("user-agent");
  // ...
}
```

Codemod the migration: `pnpm dlx @next/codemod@canary next-async-request-api ./app`.

### Recipe 4 — Partial Prerendering route

```tsx
// app/dashboard/page.tsx
import { Suspense } from "react";

export const experimental_ppr = true; // opt this route in to PPR

export default function DashboardPage() {
  return (
    <>
      <StaticShell />                              {/* prerendered */}
      <Suspense fallback={<RecentSkeleton />}>
        <RecentActivity />                         {/* streamed at request */}
      </Suspense>
    </>
  );
}

async function RecentActivity() {
  const recent = await db.activity.findMany({ take: 10 });
  return <ul>{recent.map(a => <li key={a.id}>{a.label}</li>)}</ul>;
}
```

Build emits the static shell once; the Suspense boundary streams per request.

### Recipe 5 — Route Handler (replaces `pages/api/*`)

```ts
// app/api/checkout/route.ts
import { NextResponse, type NextRequest } from "next/server";
import { z } from "zod";

export const runtime = "edge"; // or "nodejs" (default)
export const dynamic = "force-dynamic";

const Schema = z.object({ priceId: z.string().min(1) });

export async function POST(req: NextRequest) {
  const body = Schema.safeParse(await req.json());
  if (!body.success) return NextResponse.json({ error: body.error.flatten() }, { status: 400 });
  const session = await stripe.checkout.sessions.create({ /* ... */ });
  return NextResponse.json({ url: session.url }, { status: 200 });
}
```

### Recipe 6 — Middleware with multi-tenant subdomain routing

```ts
// middleware.ts
import { NextResponse, type NextRequest } from "next/server";

export const config = { matcher: "/((?!api|_next|favicon.ico).*)" };

export function middleware(req: NextRequest) {
  const host = req.headers.get("host") ?? "";
  const subdomain = host.split(".")[0];
  if (subdomain && subdomain !== "www" && subdomain !== "app") {
    const url = req.nextUrl.clone();
    url.pathname = `/_tenants/${subdomain}${url.pathname}`;
    return NextResponse.rewrite(url);
  }
  return NextResponse.next();
}
```

### Recipe 7 — `next/image` with priority on LCP

```tsx
import Image from "next/image";

export function Hero() {
  return (
    <Image
      src="/hero.jpg"
      alt="Spring catalogue"
      width={1920}
      height={1080}
      priority           // preload, skip lazy-load
      sizes="100vw"
      className="h-auto w-full"
    />
  );
}
```

Only the single LCP image should have `priority`; everything else stays lazy.

### Recipe 8 — `next/font` (self-host, zero CLS)

```tsx
// app/layout.tsx
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"], display: "swap" });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.className}>
      <body>{children}</body>
    </html>
  );
}
```

### Recipe 9 — `revalidatePath` and `revalidateTag`

```ts
"use server";
import { revalidatePath, revalidateTag } from "next/cache";

export async function publishPost(id: string) {
  await db.post.update({ where: { id }, data: { published: true } });
  revalidatePath("/blog");
  revalidatePath(`/blog/${id}`);
  revalidateTag("posts"); // invalidates anything fetched with { next: { tags: ["posts"] } }
}
```

### Recipe 10 — `unstable_cache` for memoized data

```ts
import { unstable_cache } from "next/cache";

export const getTopPosts = unstable_cache(
  async (limit: number) => db.post.findMany({ orderBy: { views: "desc" }, take: limit }),
  ["top-posts"],
  { revalidate: 60, tags: ["posts"] },
);
```

### Recipe 11 — Deploy

```bash
pnpm dlx vercel deploy --prod                            # Vercel (best DX)
pnpm dlx wrangler pages deploy ./out                     # Cloudflare Pages (run `next build && next export` first OR @cloudflare/next-on-pages)
pnpm dlx netlify deploy --prod                           # Netlify (use @netlify/plugin-nextjs)
```

## Examples

### Example 1: Migrate `pages/api/foo.ts` to `app/api/foo/route.ts`

**Before (`pages/api/users.ts`):**
```ts
export default function handler(req, res) {
  if (req.method !== "POST") return res.status(405).end();
  res.json({ ok: true });
}
```

**After (`app/api/users/route.ts`):**
```ts
import { NextResponse } from "next/server";
export async function POST() {
  return NextResponse.json({ ok: true });
}
```

### Example 2: Migrate `getServerSideProps` to async Server Component

**Before:**
```tsx
export async function getServerSideProps({ params }) {
  const post = await db.post.findUnique({ where: { id: params.id } });
  return { props: { post } };
}
export default function Page({ post }) { return <article>{post.body}</article>; }
```

**After:**
```tsx
export default async function Page({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const post = await db.post.findUnique({ where: { id } });
  return <article>{post.body}</article>;
}
```

## Edge cases / gotchas

- **`params` / `searchParams` / `cookies()` / `headers()` are now async** — Next
  14 sync calls throw at runtime in 15. Run the codemod.
- **`useRouter` lives in `next/navigation`**, NOT `next/router` (App Router only).
- **Client Components can't await** — `await` only works in Server Components.
  Wrap in `Suspense` and let `loading.tsx` show a fallback.
- **Server Action arg shape** — `useActionState` callback receives `(prevState,
  formData)`. Bind extra args with `.bind(null, extra)` or hidden form fields.
- **PPR is opt-in per route** — `experimental.ppr: "incremental"` requires
  exporting `experimental_ppr = true` from the route. Setting it to `true`
  globally is allowed but uncommon.
- **Turbopack doesn't support all webpack plugins** — check
  https://nextjs.org/docs/app/api-reference/turbopack for parity. If a plugin
  isn't supported, fall back to webpack (`pnpm next dev` without `--turbo`).
- **`next/dynamic` for client-only imports** — `dynamic(() => import("./Chart"),
  { ssr: false })` skips SSR rendering. Useful for components that touch
  `window`.
- **Static assets in `public/`** — referenced as `/foo.svg`, NOT `/public/foo.svg`.
- **Server Action body size cap** — default 1 MB; raise via `serverActions:
  { bodySizeLimit: "2mb" }` in `next.config.ts`.

## Sources

- [Next 15 release post](https://nextjs.org/blog/next-15) — feature summary
- [App Router docs](https://nextjs.org/docs/app) — full conventions
- [PPR explainer](https://nextjs.org/learn/dashboard-app/partial-prerendering) — official tutorial
- [Async dynamic APIs codemod](https://nextjs.org/docs/app/api-reference/cli/next-codemod#next-async-request-api)
- [Turbopack reference](https://nextjs.org/docs/app/api-reference/turbopack) — supported/unsupported list
- [Vercel deploy docs](https://vercel.com/docs/deployments)
- [Theo Browne — Next 15 deep dive (2025)](https://www.youtube.com/@t3dotgg) — recent video walkthroughs
