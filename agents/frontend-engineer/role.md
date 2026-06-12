# Frontend Engineer — deep reference

This section appends to `AGENT.md`. It is **not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Headings are grep-friendly: "Capability reference", "Code review playbook", "Antipattern catalog", "Performance investigation playbook", "Accessibility audit playbook", "Migration procedures", "SOTA tool reference (June 2026)", "SOTA execution playbook".

For provenance of any section, see `SOURCES.md` in this bundle.

---

## Capability reference

> Pure factual lists banished from soul.md. Grep here when the user asks "what should I use for X?" or when you need to name a specific tool from the 2026 ecosystem.

### Supported frameworks

- **React 19.x** — function components, RSC, Server Actions, `use()`, `useActionState`, `useOptimistic`, `useFormStatus`
- **Next.js 15.x** — App Router, PPR, Turbopack (dev + build stable Nov 2024), async params/headers/cookies, Server Actions, Edge Runtime
- **Svelte 5** — runes (`$state`, `$derived`, `$effect`, `$props`, `$bindable`), `.svelte.ts` / `.svelte.js` files
- **SvelteKit** — file-based routing, `+page.svelte` / `+page.server.ts` / `+layout.svelte`, hooks (`handle`, `handleError`)
- **Vue 3.5** — Composition API, `<script setup>`, `defineModel`, props destructure, Suspense, async setup
- **Nuxt 3** — Nitro server, file-based pages, server routes, `useFetch` / `useAsyncData`
- **Astro 5** — Islands architecture, Content Collections v2 (zod-typed frontmatter), Server Islands (4.12+), View Transitions
- **TanStack Start** — modern alt to Next, file-based routing + RSC, server functions
- **Solid.js / SolidStart** — fine-grained reactivity, JSX-compatible
- **Qwik / Qwik City** — resumability instead of hydration
- **React Router 7** — rebranded Remix, full-stack, stable Dec 2024
- **Remotion** — programmatic video (React/TSX → MP4); skill exists as default

### Build tooling

- **Vite 5/6** — Rollup-based bundler, ESM-native dev, instant HMR; default for SPA + library work
- **Vitest 2.x** — Vite-native test runner, browser mode, jest-compatible API
- **Turbopack** — Next 15 dev + build default (stable Nov 2024)
- **Rspack** — Rust webpack-compatible bundler (ByteDance), drop-in for webpack 5 projects
- **Bun 1.x** — runtime + bundler + test runner + package manager (Bun.serve, Bun.file, bun test)
- **esbuild** — fast bundler, used internally by Vite and others
- **swc** — Rust compiler (used by Next.js to compile TS/JSX)
- **tsx** — TypeScript node-script runner (`tsx ./script.ts`)
- **tsdown** — Rolldown-based library bundler (Vite alt for libs)

### TypeScript ecosystem

- TypeScript 5.5+ (satisfies, conditional types, const generics, template literal types, `using`/`await using`)
- type-fest (utility types: SetRequired, ReadonlyDeep, Tagged, etc.)
- ts-reset (fixes stdlib gotchas: stricter `.filter(Boolean)`, `.json()` returns `unknown`)
- zod (runtime validation, schema-first types)
- valibot (lightweight zod alt — bundle-friendly)
- arktype (TS-syntax-based schema)
- @total-typescript/ts-reset

### CSS / styling

- **Tailwind CSS 4** (Lightning CSS engine, CSS-first `@theme` config, no JS config file by default)
- **Panda CSS** (build-time CSS-in-TS, design tokens, recipes)
- **vanilla-extract** (zero-runtime CSS-in-TS, type-safe)
- **CSS Modules** (component-scoped without a framework)
- **UnoCSS** (utility-first, minimal config, Lightning-fast)
- **Open Props** (CSS variables / design tokens)
- **shadcn/ui** (copy-paste primitives owned by your repo)
- **Radix UI** (headless a11y primitives)
- **Headless UI** (Tailwind-aligned headless)
- **Ark UI** (cross-framework headless, Chakra team)
- **react-aria / react-aria-components** (Adobe's a11y primitives)

### State management

- **TanStack Query** (server state, default)
- **Zustand** (3-5 kB store-based, default for client UI state)
- **Jotai** (atom-based, fine-grained)
- **valtio** (proxy-based)
- **nanostores** (framework-agnostic, ~265 bytes)
- **TanStack Store** (state primitive from TanStack)
- **Redux Toolkit** (legacy; only for teams already invested)
- **Signals** (Preact/Solid pattern, coming to React via `useSyncExternalStore`)

### Animation

- **motion** (Framer Motion rebrand — framework-agnostic in 2024)
- **Motion One** (vanilla JS, ~3 kB)
- **GSAP** (complex timeline-driven)
- **AutoAnimate** (Formkit, easy list reordering)
- **View Transitions API** (cross-browser stable in 2024 — `document.startViewTransition`)
- **CSS @scroll-timeline** / scroll-driven animations

### Forms

- **React Hook Form** (default for React)
- **TanStack Form** (framework-agnostic)
- **Conform** (Server Action–first for Next 15)
- **VeeValidate** (Vue)
- **Felte** (Svelte)
- **Formik** (legacy, not for new projects)
- **@hookform/resolvers** (zod / valibot / arktype adapters)

### Testing

- **Vitest 2.x** (unit + integration, Vite-native)
- **Playwright 1.50+** (E2E, multi-browser, traces, codegen, component-mode)
- **Cypress** (E2E alt, but slower; pick Playwright for new projects)
- **Testing Library** (React/Vue/Svelte — user-centric component tests)
- **MSW 2.x** (Mock Service Worker, network mocking)
- **Storybook 8.x** (component isolation + docs + tests)
- **Chromatic** (visual regression CI, Storybook-first)
- **Percy / Reg-cli / Lost-pixel** (visual regression alts)
- **@axe-core/playwright** (a11y in E2E)

### Performance / accessibility / quality

- **Lighthouse CI** (`@lhci/cli`, lab data)
- **web-vitals** (4.x) — RUM library (onLCP, onINP, onCLS, onFCP, onTTFB)
- **PageSpeed Insights API** (synthetic + field data)
- **axe-core** (a11y engine)
- **pa11y / pa11y-ci** (a11y CLI + CI gate)
- **eslint-plugin-jsx-a11y** (lint-time a11y rules)
- **Million.js** (auto-optimize React VDOM)
- **bundlejs.com / Bundle-Phobia** (npm bundle size lookup)
- **@next/bundle-analyzer** (Rollup/webpack analyzer for Next)
- **size-limit** (CI bundle-size gate)
- **Knip** (unused code/dep detection)
- **Biome** (Rust lint+format, single tool, ~25x faster than ESLint + Prettier)
- **Oxlint** (Rust lint-only, even faster than Biome's linter)
- **ESLint 9** (flat config mandatory)
- **Prettier 3** (when paired with ESLint)
- **Stylelint** (CSS)

### i18n

- **next-intl** (Next 15 + RSC + locale routing)
- **react-intl / FormatJS** (ICU MessageFormat, framework-agnostic)
- **Lingui** (macro-based extraction, React/Vue)
- **Paraglide JS** (Inlang, ~5kb runtime, tree-shakeable, type-safe)

### Edge / runtime

- **Cloudflare Workers** (V8 isolates, low cold-start)
- **Wrangler 3+** (Cloudflare CLI)
- **Workers KV / D1 / R2 / Durable Objects** (Cloudflare stateful primitives)
- **Vercel Edge Runtime** (Next.js `runtime: "edge"`)
- **PartyKit** (multiplayer on Cloudflare Workers + Durable Objects)
- **Hono** (modern lightweight web framework, multi-runtime)
- **Elysia** (Bun-native web framework)
- **Deno Deploy** (Deno runtime)
- **Liveblocks / Yjs / Automerge** (CRDT collaboration)

### CMS / e-commerce

- **Payload CMS 3.x** (Next 15–native, TypeScript-first, OSS)
- **Sanity** (structured content, GROQ queries)
- **Contentful / DatoCMS** (managed enterprise)
- **Strapi** (self-hosted OSS)
- **Builder.io** (visual editor)
- **Shopify Hydrogen** (Remix-based storefront framework)

### Auth

- **Clerk** (drop-in components, MFA, orgs, RBAC, paid SaaS)
- **Auth.js v5** (rebranded NextAuth, edge-ready, OSS)
- **Lucia v3** (lightweight library + custom DB, OSS)
- **WorkOS** (enterprise SSO/SCIM)
- **Supabase Auth** (paired with Postgres)
- **iron-session** (encrypted session cookies)

### Payments

- **Stripe** (Elements, Checkout, Connect, Payment Intents)
- **Paddle / Lemon Squeezy** (merchant-of-record for SaaS)
- **Adyen / Braintree** (enterprise gateways)

### File / data formats

- Markdown / MDX (content + JSX in markdown)
- JSON / YAML / TOML (config)
- SVG (vector graphics, inline preferred for icons)
- WebP / AVIF (modern image formats, default)
- WOFF2 (font format, mandatory in 2026)
- HTML5 / CSS3 / ES2024+
- WebAssembly (`.wasm`)

---

## Code review playbook

> Step-by-step procedure for reviewing a frontend PR.

### Step 1 — Context

- Read the PR description; if there's no description, ask for one or write what you understand
- Skim the changeset to map scope: files changed, lines added/removed, areas touched
- Identify the framework + meta-framework + CSS approach in use; review *that*, not what you'd prefer
- Check if the PR has tests + Storybook stories + visual regression baseline

### Step 2 — Review in priority order

Walk through the changed files in this order; stop and comment as you go:

1. **Security pass** — `dangerouslySetInnerHTML` (sanitize?), open redirects in middleware, secrets pulled into client bundle (`NEXT_PUBLIC_*` only — server-only vars must not leak), CSRF on Server Actions / API routes, eval / Function constructor
2. **Accessibility pass** — every interactive element has a name; keyboard reach + tab order; focus management on dialog/popover/menu open + close; color contrast (eyeball + axe report if available); `alt` on images (or `alt=""` for decorative); ARIA antipatterns (`role="button"` on a `<div>` instead of `<button>`)
3. **Performance pass** — bundle imports (`import _ from "lodash"` vs `import map from "lodash/map"`), Server Component shipping client lib, missing `next/image` (or `<Image />` for Astro), blocking fonts without `next/font`, `useEffect` chain that triggers re-fetch
4. **Type safety pass** — `any` in public props (refuse), missing return type on exported fn (warn), `as` cast (challenge: why?), runtime data without zod/valibot validation
5. **Data + races pass** — `useEffect` for fetch (suggest TanStack Query / RSC), stale closure (deps array correctness), missing `key`, derived state in `useState` instead of computed inline
6. **UX correctness pass** — loading state, error state, empty state — all three present? Optimistic UI for mutations? Back-button behavior intact (push vs replace)?
7. **Component contracts pass** — speculative reuse (premature abstraction), prop drilling > 2 levels (use Context or Server Component lift), internal types exported (mark `@internal`)
8. **Style nits last** — Biome / ESLint config will normalize most; flag only the patterns that survive

### Step 3 — Communicate

- Group findings: **Blocker** (security, a11y critical, type unsoundness in public API), **Should fix** (perf regression, missing test), **Consider** (alternative pattern), **Nit** (style)
- Concrete examples: paste the BAD pattern with line ref, then the suggested fix
- Acknowledge good patterns: "this loading skeleton + Suspense fallback is exactly right"
- One clarifying question if the PR's intent is ambiguous — don't guess

### Step 4 — Sign-off gate

Before approving:
- Tests run green
- Storybook (if applicable) builds clean
- a11y CI passes (axe-core / Lighthouse)
- Bundle size within budget (`size-limit`)
- No new `any` introduced in public APIs
- No regressions on Chromatic / Percy

---

## Accessibility audit playbook (WCAG 2.2 AA)

### Step 1 — Automated sweep

```bash
# axe-core via Playwright E2E
pnpm add -D @axe-core/playwright
# In test:
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("home page is accessible", async ({ page }) => {
  await page.goto("/");
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});

# pa11y-ci for static pages
pnpm dlx pa11y-ci --sitemap https://example.com/sitemap.xml

# Lighthouse a11y category
pnpm dlx @lhci/cli@latest autorun --collect.numberOfRuns=3 \
  --assert.assertions.categories:accessibility=0.95
```

### Step 2 — Categorize findings

| Severity | Definition | Action |
|---|---|---|
| Critical | Page unusable for screen-reader / keyboard users | Block release |
| Serious | Major task fails for a11y users (login, checkout, search) | Block release |
| Moderate | Workaround exists but degraded UX | Fix this sprint |
| Minor | Cosmetic / nice-to-have improvements | Backlog |

### Step 3 — Apply fixes by category

- **Missing name on interactive** → `<button aria-label="Close">` or visible text or `aria-labelledby` pointing to a label element
- **Color contrast** → meet 4.5:1 (normal text), 3:1 (large text and UI). Use https://webaim.org/resources/contrastchecker/
- **Focus management** — `:focus-visible` outline preserved (or restyled); dialog open → move focus to first focusable in dialog; close → return focus to opener
- **Keyboard nav** — every interactive element reachable by Tab; Esc closes dialog; arrow keys for menu/listbox; no keyboard traps
- **Semantic HTML** — `<button>` not `<div onClick>`; `<a href>` not `<div onClick navigate>`; `<nav>` / `<main>` / `<aside>` landmarks
- **Forms** — every input has a `<label for>` or `aria-labelledby`; error messages associated via `aria-describedby`; `aria-invalid` on bad input
- **Images** — `alt` describes meaning; `alt=""` if decorative (don't omit `alt` entirely)
- **Live regions** — `aria-live="polite"` for non-urgent updates, `assertive` for urgent (use sparingly)

### Step 4 — Manual verification on critical flows

- Tab through the page; can you reach everything? Can you skip to main?
- Use screen reader (VoiceOver on macOS, NVDA on Windows, TalkBack on Android) on top 3 user flows (login, primary CTA, settings)
- Zoom to 200% — does layout break? Does text overlap?
- Disable CSS / images — does content still make sense?

### Step 5 — Wire to CI

```yaml
# .github/workflows/a11y.yml — wire axe-core E2E + Lighthouse + pa11y-ci
# fail the PR if scores drop below threshold
```

---

## Core Web Vitals playbook

### Step 1 — Measure

```bash
# Lighthouse CI (lab)
pnpm dlx @lhci/cli@latest autorun \
  --collect.url=https://example.com/ \
  --collect.numberOfRuns=3 \
  --assert.preset=lighthouse:no-pwa

# web-vitals (RUM, prod)
pnpm add web-vitals
# In app shell:
import { onLCP, onINP, onCLS } from "web-vitals";
onLCP(metric => send({ name: "LCP", value: metric.value }));
onINP(metric => send({ name: "INP", value: metric.value }));
onCLS(metric => send({ name: "CLS", value: metric.value }));

# PageSpeed Insights (synthetic + CrUX field data)
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&strategy=mobile&key=$PSI_KEY"
```

### Step 2 — Diagnose by failing vital

#### LCP > 2.5s

- Identify the LCP element (Lighthouse → "Largest Contentful Paint element")
- If image → preload it (`<link rel="preload" as="image" href="...">` or `next/image priority`)
- Compress + serve AVIF/WebP via `next/image` or `astro:assets` or `sharp`
- Self-host fonts via `next/font`; `font-display: swap` (default in next/font)
- Reduce TTFB — move to edge (`runtime: "edge"`), enable CDN cache, ISR
- Eliminate render-blocking JS above the fold; defer non-critical scripts
- Use Server Components / Astro to keep above-the-fold JS-free

#### INP > 200ms

- Open Performance panel → "Interactions" track in Chrome 120+
- Identify the slow interaction
- Break up long tasks (`scheduler.postTask({ priority: "user-visible" }, work)`)
- Use Web Workers for heavy compute (`new Worker(new URL("./worker.ts", import.meta.url))`)
- Debounce expensive handlers
- Avoid `layout` reads after writes in handlers (forced reflow)
- Use `useTransition` / `startTransition` to mark non-urgent state updates

#### CLS > 0.1

- Identify the shifting element (Lighthouse → "Avoid large layout shifts")
- `width` and `height` on every `<img>` and `<iframe>` (or `aspect-ratio` in CSS)
- Reserve space for ads/banners with `min-height`
- Don't insert content above existing content after page load — insert below
- Match fallback font metrics with `size-adjust`, `ascent-override`, `descent-override` (or use `next/font` which does this automatically)
- Use `font-display: optional` for non-critical fonts

### Step 3 — Verify

Re-run Lighthouse CI. If the change isn't measurable, undo it.

### Step 4 — Wire continuous monitoring

- Sentry Performance or Datadog RUM with web-vitals integration
- Slack/Discord alert on p75 INP > 250ms
- Lighthouse CI on every PR with a hard budget assertion

---

## Performance investigation playbook

> When the user says "the app feels slow," do this:

### Step 1 — Baseline

- What page / interaction? Reproduce on the same device class the user reported
- Throttle network (Fast 3G or Slow 4G in DevTools) and CPU (4x slowdown)
- Capture a Lighthouse report + record a Performance trace

### Step 2 — Pick the lever

| Symptom | Tool / Fix |
|---|---|
| First page load slow | Lighthouse LCP; check TTFB, font/JS blocking, image size |
| App feels janky on click | Performance panel "Interactions"; check INP, long tasks, forced reflow |
| Re-renders too often | React DevTools Profiler; check missing memoization, prop equality, context boundaries |
| Bundle too big | `pnpm dlx @next/bundle-analyzer` or `vite-bundle-analyzer`; check unused deps, full-lib imports, missing tree-shake |
| Hydration mismatch warning | Check server-only refs (`window`, `Date.now()`) in client paths; use `suppressHydrationWarning` only as last resort |
| Memory grows over time | Chrome → Memory → Heap snapshot diff; check forgotten event listeners, detached DOM nodes, growing arrays in closures |

### Step 3 — Order of typical wins (frontend)

1. **Render less** — Server Components, conditional render, virtualization (`@tanstack/react-virtual`)
2. **Render later** — Suspense + streaming, `next/dynamic`, `React.lazy`, `client:idle` / `client:visible` (Astro)
3. **Hydrate less** — Astro Islands; partial hydration; signals
4. **Ship less JS** — code-split per route, tree-shake, replace heavy deps (es-toolkit > lodash; date-fns > moment)
5. **Cache more** — TanStack Query staleTime, Next ISR, Cloudflare cache, service worker
6. **Move to edge** — `runtime: "edge"` on Next routes, Workers / Pages for static
7. **Image / font discipline** — `next/image priority` on LCP, `next/font` self-host
8. **Web Worker / Wasm** — for genuinely CPU-heavy client work

---

## Migration procedures

### Webpack → Vite

```bash
git worktree add ../proj-vite migrate-to-vite
cd ../proj-vite
pnpm create vite@latest . --template react-ts
# preserve src/, move webpack.config.js → vite.config.ts
# process.env.X → import.meta.env.VITE_X (note: must be prefixed VITE_)
# replace webpack-dev-server proxy with vite.config.ts server.proxy
# replace webpack.DefinePlugin with vite.config.ts define
pnpm run build && pnpm run preview
```

### CRA → Next 15

```bash
# Step 1 — codemod
pnpm dlx @next/codemod@latest cra-to-nextjs ./src

# Step 2 — manual cleanup
# REACT_APP_X → NEXT_PUBLIC_X
# react-router → next/navigation (or stay on react-router 7)
# CSS Modules: file.module.css works as-is
# public/index.html → app/layout.tsx + app/page.tsx
# react-scripts test → vitest
pnpm install && pnpm exec next build
```

### React 18 → React 19

```bash
pnpm dlx codemod@latest react/19/migration-recipe ./src
# replaces: forwardRef, useFormState, Context.Provider, string refs, ReactDOM.render
# Then manual: remove propTypes (deprecated), check Suspense behavior changes
pnpm exec tsc --noEmit && pnpm run build
```

### ESLint + Prettier → Biome

```bash
pnpm add -D --save-exact @biomejs/biome
pnpm dlx @biomejs/biome migrate eslint --write
pnpm dlx @biomejs/biome migrate prettier --write
pnpm dlx @biomejs/biome check --write ./src
# update package.json scripts: replace "lint" and "format" with biome
# delete .eslintrc, .prettierrc — biome.json replaces both
```

### Pages Router (Next ≤14) → App Router (Next 15)

- Migrate top-level layout: `pages/_app.tsx` + `pages/_document.tsx` → `app/layout.tsx`
- Routes: `pages/foo.tsx` → `app/foo/page.tsx`; `pages/foo/[id].tsx` → `app/foo/[id]/page.tsx`
- API routes: `pages/api/foo.ts` → `app/api/foo/route.ts` (with `GET` / `POST` exports)
- Data fetching: `getServerSideProps` → Server Component `await` directly; `getStaticProps` → Server Component + `unstable_cache` / `fetch` with `next.revalidate`
- `useRouter` (next/router) → `useRouter` (next/navigation) — different API surface (`router.push("/x")` still works, but `router.query` is now params separately)

---

## Antipattern catalog

> BAD / GOOD pairs the agent flags in review.

### Antipattern 1: Fetching in useEffect

**BAD:**
```tsx
function UserProfile({ id }: { id: string }) {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetch(`/api/users/${id}`).then(r => r.json()).then(setUser);
  }, [id]);
  if (!user) return <Spinner />;
  return <div>{user.name}</div>;
}
```
**Why it's bad:** Race conditions on `id` change (stale response wins), no cache, no revalidate, no error state, no abort signal, double-fetch in React 18 StrictMode.

**GOOD (TanStack Query):**
```tsx
function UserProfile({ id }: { id: string }) {
  const { data: user, isPending, isError } = useQuery({
    queryKey: ["user", id],
    queryFn: ({ signal }) => fetch(`/api/users/${id}`, { signal }).then(r => r.json()),
  });
  if (isPending) return <Spinner />;
  if (isError) return <ErrorBanner />;
  return <div>{user.name}</div>;
}
```

**GOOD (RSC):**
```tsx
// app/users/[id]/page.tsx — Server Component, no useEffect at all
export default async function UserProfile({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const user = await db.user.findUnique({ where: { id } });
  if (!user) notFound();
  return <div>{user.name}</div>;
}
```

### Antipattern 2: `any` in public component props

**BAD:**
```tsx
interface ButtonProps {
  onClick: any;
  data: any;
}
```
**Why it's bad:** `any` silently disables every check downstream. Public API contract is broken.

**GOOD:**
```tsx
interface ButtonProps<T = unknown> {
  onClick: (event: React.MouseEvent<HTMLButtonElement>) => void;
  data: T;
}
```

### Antipattern 3: Missing accessible name

**BAD:**
```tsx
<button onClick={close}><Icon name="x" /></button>
```
**Why it's bad:** Screen reader announces "button" with no purpose.

**GOOD:**
```tsx
<button onClick={close} aria-label="Close dialog">
  <Icon name="x" aria-hidden="true" />
</button>
```

### Antipattern 4: Removing focus outline

**BAD:**
```css
button:focus { outline: none; }
```
**Why it's bad:** Keyboard users lose visual feedback. WCAG 2.4.7 violation.

**GOOD:**
```css
button:focus-visible {
  outline: 2px solid var(--brand);
  outline-offset: 2px;
}
```

### Antipattern 5: Synchronous heavy work in event handler

**BAD:**
```tsx
<button onClick={() => {
  const result = expensiveComputeOver10000Items(items);
  setState(result);
}}>Compute</button>
```
**Why it's bad:** INP regression — main thread blocks for hundreds of ms.

**GOOD:**
```tsx
<button onClick={() => {
  startTransition(async () => {
    const result = await new Promise(resolve => {
      scheduler.postTask(() => resolve(expensiveComputeOver10000Items(items)), { priority: "user-visible" });
    });
    setState(result);
  });
}}>Compute</button>
```

(Or move `expensiveComputeOver10000Items` to a Web Worker entirely.)

### Antipattern 6: Mixing CSS strategies

**BAD:** project has Tailwind + styled-components + CSS Modules + inline styles + global stylesheets — no documented strategy.

**Why it's bad:** Specificity wars, undisplayed dead CSS, unpredictable cascade order.

**GOOD:** pick one primary strategy (Tailwind or Panda or vanilla-extract or CSS Modules); document it in `CONTRIBUTING.md`; only deviate for documented reasons (e.g., "MDX content uses Tailwind Prose plugin").

### Antipattern 7: Importing entire libraries

**BAD:**
```tsx
import _ from "lodash";
import * as dateFns from "date-fns";
```
**Why it's bad:** Defeats tree-shaking (well-formed ESM should tree-shake `lodash-es` correctly, but the bare `lodash` package is CJS and doesn't). Bundle bloats by 70+ KB.

**GOOD:**
```tsx
import map from "lodash-es/map";
import { format, parseISO } from "date-fns";
// or replace with es-toolkit (lodash-like, smaller, modern)
import { map } from "es-toolkit";
```

### Antipattern 8: Loading state without skeleton

**BAD:**
```tsx
if (isLoading) return <Spinner />;
```
**Why it's bad:** CLS regression when content loads in. User sees a jumping page.

**GOOD:**
```tsx
if (isLoading) return <UserProfileSkeleton />; // same layout as the real component
```

### Antipattern 9: `dangerouslySetInnerHTML` without sanitization

**BAD:**
```tsx
<div dangerouslySetInnerHTML={{ __html: userInput }} />
```
**Why it's bad:** XSS vector.

**GOOD:**
```tsx
import DOMPurify from "isomorphic-dompurify";
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userInput) }} />
// Or render Markdown via react-markdown + rehype-sanitize
```

### Antipattern 10: Form without server validation

**BAD:**
```tsx
"use server";
export async function createUser(formData: FormData) {
  const email = formData.get("email") as string;
  await db.user.create({ data: { email } }); // trusts client
}
```
**Why it's bad:** Bypasses client validation easily; runtime errors and bad data.

**GOOD:**
```tsx
"use server";
import { z } from "zod";

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

export async function createUser(formData: FormData) {
  const parsed = CreateUserSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) return { error: parsed.error.flatten() };
  await db.user.create({ data: parsed.data });
  return { success: true };
}
```

### Antipattern 11: E2E test with `waitForTimeout`

**BAD:**
```ts
await page.click("button.submit");
await page.waitForTimeout(2000);
await expect(page.locator(".success")).toBeVisible();
```
**Why it's bad:** Flaky on slow CI, slow on fast CI, brittle.

**GOOD:**
```ts
await page.getByRole("button", { name: "Submit" }).click();
await expect(page.getByText("Order placed")).toBeVisible(); // auto-waits up to timeout
```

### Antipattern 12: Color-only state

**BAD:**
```tsx
<div className={isError ? "text-red-500" : "text-green-500"}>Status</div>
```
**Why it's bad:** Colorblind users can't tell error from success. WCAG 1.4.1.

**GOOD:**
```tsx
<div className={isError ? "text-red-500" : "text-green-500"}>
  {isError ? <ErrorIcon aria-label="Error" /> : <SuccessIcon aria-label="Success" />}
  {isError ? "Error: " : "Success: "}
  Status
</div>
```

### Common fixes summary

| Antipattern | Fix |
|---|---|
| `useEffect` for fetch | RSC `await` / TanStack Query / `use()` |
| `any` in public props | `unknown` + narrowing, or proper type |
| No accessible name | `aria-label` or visible text or `aria-labelledby` |
| Removed focus outline | `:focus-visible` with brand-styled outline |
| Heavy sync work in handler | `startTransition` / Web Worker / `scheduler.postTask` |
| Mixed CSS strategies | Pick one, document in CONTRIBUTING |
| Whole-library imports | Named imports + ESM-friendly packages |
| Spinner without skeleton | Skeleton matching real component layout |
| Unsanitized HTML | DOMPurify + sanitize before render |
| No server validation | zod/valibot on server in addition to client |
| `waitForTimeout` in E2E | Web-first assertions (`toBeVisible`, `toHaveText`) |
| Color-only state | Icon + text + color (never color alone) |

---

## Reference patterns

### Pattern: Server Action + form state (Next 15)

```tsx
// app/_actions/create-user.ts
"use server";
import { z } from "zod";
import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";

const Schema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

export type FormState = { error?: string; fieldErrors?: Record<string, string[]> };

export async function createUser(_prev: FormState, formData: FormData): Promise<FormState> {
  const parsed = Schema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) {
    return { fieldErrors: parsed.error.flatten().fieldErrors };
  }
  await db.user.create({ data: parsed.data });
  revalidatePath("/users");
  redirect("/users");
}

// app/users/new/page.tsx
"use client";
import { useActionState } from "react";
import { useFormStatus } from "react-dom";
import { createUser, type FormState } from "@/app/_actions/create-user";

function SubmitButton() {
  const { pending } = useFormStatus();
  return <button type="submit" disabled={pending}>{pending ? "Creating..." : "Create"}</button>;
}

export default function NewUserPage() {
  const [state, action] = useActionState<FormState, FormData>(createUser, {});
  return (
    <form action={action}>
      <label htmlFor="email">Email</label>
      <input id="email" name="email" type="email" required aria-invalid={!!state.fieldErrors?.email} />
      {state.fieldErrors?.email && <p role="alert">{state.fieldErrors.email[0]}</p>}
      <SubmitButton />
    </form>
  );
}
```

### Pattern: TanStack Query mutation with optimistic UI

```tsx
const queryClient = useQueryClient();
const mutation = useMutation({
  mutationFn: (newTodo: Todo) => fetch("/api/todos", { method: "POST", body: JSON.stringify(newTodo) }).then(r => r.json()),
  onMutate: async (newTodo) => {
    await queryClient.cancelQueries({ queryKey: ["todos"] });
    const previous = queryClient.getQueryData<Todo[]>(["todos"]);
    queryClient.setQueryData<Todo[]>(["todos"], old => [...(old ?? []), newTodo]);
    return { previous };
  },
  onError: (_err, _newTodo, ctx) => queryClient.setQueryData(["todos"], ctx?.previous),
  onSettled: () => queryClient.invalidateQueries({ queryKey: ["todos"] }),
});
```

### Pattern: Svelte 5 runes

```svelte
<script lang="ts">
  let count = $state(0);
  let doubled = $derived(count * 2);
  $effect(() => {
    console.log("count changed:", count);
  });
  let { name = "world" }: { name?: string } = $props();
</script>

<h1>Hello {name}</h1>
<button onclick={() => count++}>Clicks: {count}</button>
<p>Doubled: {doubled}</p>
```

### Pattern: Vue 3.5 Composition API + defineModel

```vue
<script setup lang="ts">
import { ref, computed } from "vue";

const model = defineModel<string>({ required: true });
const length = computed(() => model.value.length);
</script>

<template>
  <input v-model="model" />
  <p>Length: {{ length }}</p>
</template>
```

### Pattern: Astro Island with selective hydration

```astro
---
import Counter from "../components/Counter.tsx";
import Newsletter from "../components/Newsletter.tsx";
---
<html>
  <body>
    <h1>Welcome</h1>
    <!-- ships as zero JS -->
    <Counter client:visible /> <!-- hydrates when scrolled into view -->
    <Newsletter client:idle />  <!-- hydrates after main thread idle -->
  </body>
</html>
```

### Pattern: Zustand store with TypeScript

```ts
import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";

interface CartState {
  items: { id: string; qty: number }[];
  add: (id: string) => void;
  remove: (id: string) => void;
  clear: () => void;
}

export const useCart = create<CartState>()(
  devtools(persist((set) => ({
    items: [],
    add: (id) => set(s => ({ items: [...s.items, { id, qty: 1 }] })),
    remove: (id) => set(s => ({ items: s.items.filter(i => i.id !== id) })),
    clear: () => set({ items: [] }),
  }), { name: "cart" }))
);
```

### Pattern: Playwright spec with a11y check + traces

```ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test.use({ trace: "on-first-retry" });

test("checkout flow is keyboard accessible and a11y-clean", async ({ page }) => {
  await page.goto("/checkout");
  await page.getByRole("button", { name: "Continue" }).focus();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("heading", { name: "Payment" })).toBeVisible();

  const a11y = await new AxeBuilder({ page }).analyze();
  expect(a11y.violations).toEqual([]);
});
```

### Pattern: Cloudflare Worker with Hono

```ts
// src/index.ts
import { Hono } from "hono";
import { cors } from "hono/cors";

const app = new Hono<{ Bindings: { DB: D1Database } }>();
app.use("*", cors({ origin: "https://example.com" }));

app.get("/api/users/:id", async (c) => {
  const id = c.req.param("id");
  const user = await c.env.DB.prepare("SELECT * FROM users WHERE id = ?").bind(id).first();
  if (!user) return c.notFound();
  return c.json(user);
});

export default app;
// wrangler.toml — set [[d1_databases]] binding, then: `wrangler deploy`
```

---

## SOTA tool reference (June 2026)

> One H3 per tool. Grep-friendly. Each subsection 10-30 lines naming the verb, the source, the canonical command(s), and the bundled skill pack that deep-dives. The skill pack folders are RESERVED in Round 1; Round 2 creates the SKILL.md contents.

### React 19

The 2024-2025 baseline. Server Components, Server Actions, Actions, `useActionState`, `useOptimistic`, `useFormStatus`, `use()` for promises and context, `ref` as a regular prop (forwardRef gone), Context directly (no `.Provider`).

- `pnpm create vite@latest --template react-ts` for SPA
- `pnpm dlx create-next-app@latest` for Next 15 (with React 19)
- Migration: `pnpm dlx codemod@latest react/19/migration-recipe`

Source: https://react.dev/blog/2024/12/05/react-19 · Skill: `react-19-server-components-actions`

### Next.js 15

App Router default, **PPR stable Nov 2024** (Partial Prerendering — static shell + streamed dynamic), Turbopack default for dev + stable for `next build`, `cookies()`/`headers()`/`params`/`searchParams` async.

- `pnpm dlx create-next-app@latest --typescript --app --tailwind`
- `next.config.ts` (TypeScript config) + `experimental: { ppr: true }`
- Server Actions in `app/_actions/*.ts` with `"use server"`

Source: https://nextjs.org/blog/next-15 · Skill: `next-15-app-router-ppr`

### Svelte 5

Runes (`$state`, `$derived`, `$effect`, `$props`, `$bindable`) replace `let`-based reactivity. `.svelte.ts` files for shared rune logic. Stable Oct 2024.

- `pnpm create svelte@latest` (will install SvelteKit)
- `pnpm dlx sv create` (newer CLI)

Source: https://svelte.dev/blog/svelte-5-is-alive · Skill: `svelte-5-runes-sveltekit`

### Vue 3.5 + Nuxt 3

Composition API (`<script setup>` default), `defineModel` for two-way (3.4+), Suspense, async setup, props destructure (3.5).

- `pnpm create vue@latest`
- `pnpm dlx nuxi@latest init` for Nuxt 3

Source: https://blog.vuejs.org/posts/vue-3-5 · Skill: `vue-3-composition-api-composables`

### Astro 5

Islands architecture (zero JS by default, opt into hydration). Content Collections v2 (zod-typed). Server Islands (4.12+) for dynamic-within-static. View Transitions baked in.

- `pnpm create astro@latest`

Source: https://astro.build/blog/astro-5/ · Skill: `astro-islands-content-first`

### Vite 5/6 + Vitest 2

Vite is the default bundler/dev server for new SPA/library projects. Vitest is Vite-native unit test (jest-API compatible, browser mode).

- `pnpm create vite@latest`
- `pnpm add -D vitest @vitest/ui happy-dom`
- `vitest --browser=chromium` for browser-mode component tests

Source: https://vitejs.dev/ · https://vitest.dev/ · Skill: `vite-vitest-modern-toolchain`

### Turbopack

Next 15's default dev bundler; stable for `next build` Nov 2024. Rust-powered, replaces webpack inside Next.

- Native to Next 15 — `pnpm next dev --turbo` (default)

Source: https://nextjs.org/docs/app/api-reference/turbopack

### Rspack

ByteDance's Rust webpack-compatible bundler. Drop-in for webpack 5 projects.

- `pnpm dlx @rspack/cli@latest`

Source: https://rspack.dev/

### Bun

Runtime + bundler + test runner + package manager in one binary. Use as alternative to Node + pnpm for self-hosted runs.

- `bun install`, `bun run dev`, `bun test`, `bun build ./src/index.ts --outdir ./dist`

Source: https://bun.sh/

### TypeScript 5.5+

`satisfies` for "validate without widen", const type parameters, conditional types, template literal types, `using`/`await using`.

- `pnpm add -D typescript@latest type-fest @total-typescript/ts-reset`
- `tsconfig.json`: `strict: true`, `noUncheckedIndexedAccess: true`

Source: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-5.html · Skill: `typescript-5-advanced-patterns`

### TanStack Query 5

Server state library. `useQuery`, `useMutation`, `useSuspenseQuery`, optimistic updates, cache invalidation.

- `pnpm add @tanstack/react-query @tanstack/react-query-devtools`

Source: https://tanstack.com/query/v5 · Skill: `tanstack-query-router-store`

### TanStack Router 1

Type-safe file-based routing for SPAs (alt to Next App Router for non-SSR).

- `pnpm add @tanstack/react-router @tanstack/router-plugin`

Source: https://tanstack.com/router/latest · Skill: `tanstack-query-router-store`

### Zustand / Jotai

Client UI state. Zustand for store-shaped. Jotai for atom-shaped.

- `pnpm add zustand` or `pnpm add jotai`

Source: https://zustand.docs.pmnd.rs/ · https://jotai.org/ · Skill: `zustand-jotai-state-management`

### Tailwind CSS 4

Lightning CSS engine (Rust), CSS-first `@theme` config (no JS config), ~10x faster than v3. Stable Jan 2025.

- `pnpm add tailwindcss@latest @tailwindcss/vite` (Vite plugin)
- `pnpm add tailwindcss @tailwindcss/postcss` (PostCSS pipeline)

Source: https://tailwindcss.com/blog/tailwindcss-v4 · Skill: `tailwind-4-css-architecture`

### shadcn/ui + Radix UI

shadcn/ui is copy-paste components (you own them); Radix UI is headless a11y primitives underneath. react-aria for Adobe's a11y primitives.

- `pnpm dlx shadcn@latest init`
- `pnpm dlx shadcn@latest add button card dialog`

Source: https://ui.shadcn.com/ · https://www.radix-ui.com/ · Skill: `shadcn-radix-headless-components`

### React Hook Form + zod

Default form library for React + schema validation.

- `pnpm add react-hook-form @hookform/resolvers zod`
- For Server Actions: `pnpm add conform-to/react conform-to/zod`

Source: https://react-hook-form.com/ · https://zod.dev/ · Skill: `react-hook-form-zod-valibot-forms`

### axe-core + pa11y + Lighthouse

a11y audit toolchain. axe-core for engine-level checks; pa11y-ci for CI gates; Lighthouse for full-page audit.

- `pnpm add -D @axe-core/playwright`
- `pnpm dlx pa11y-ci --sitemap https://example.com/sitemap.xml`
- `pnpm dlx @lhci/cli@latest autorun`

Source: https://www.deque.com/axe/ · https://pa11y.org/ · Skill: `accessibility-wcag-22-aa-axe-core`

### web-vitals 4 + Lighthouse CI + Million.js

Core Web Vitals measurement (`onLCP`/`onINP`/`onCLS`) + lab measurement + React VDOM auto-optimization.

- `pnpm add web-vitals`
- `pnpm dlx @lhci/cli@latest autorun`
- `pnpm add million` (Vite/Next plugin → automatic React perf)

Source: https://github.com/GoogleChrome/web-vitals · https://million.dev/ · Skill: `core-web-vitals-lcp-inp-cls`

### size-limit + Knip + bundle-analyzer

Bundle-size CI gate + unused code detection + visualizer.

- `pnpm add -D size-limit @size-limit/preset-app knip`
- `pnpm add -D @next/bundle-analyzer`
- `pnpm dlx knip --reporter compact`

Source: https://github.com/ai/size-limit · https://knip.dev/ · Skill: `bundle-size-code-splitting-tree-shaking`

### Playwright 1.50+

E2E + a11y + component tests. Multi-browser. Web-first assertions auto-wait.

- `pnpm add -D @playwright/test`
- `pnpm dlx playwright install`
- `pnpm exec playwright codegen` (record + replay)

Source: https://playwright.dev/ · Skill: `playwright-e2e-stability`

### Storybook 8 + Chromatic

Component isolation, docs, visual regression CI.

- `pnpm dlx storybook@latest init`
- `pnpm add -D @chromatic-com/storybook`
- `pnpm dlx chromatic --project-token=$CHROMATIC_TOKEN`

Source: https://storybook.js.org/ · https://www.chromatic.com/ · Skill: `storybook-chromatic-design-system`

### Biome

Rust lint+format single tool. ESLint + Prettier replacement, ~25x faster.

- `pnpm add -D --save-exact @biomejs/biome`
- `pnpm dlx biome init`
- `pnpm dlx biome check --write ./src`
- Migration: `pnpm dlx biome migrate eslint --write` / `migrate prettier --write`

Source: https://biomejs.dev/ · Skill: `biome-eslint-prettier-lint-format`

### Oxlint

Rust ESLint-alt — even faster than Biome's linter, ESLint-rule-compatible.

- `pnpm add -D oxlint && pnpm exec oxlint`

Source: https://oxc.rs/

### MSW 2

Mock Service Worker — network mocking for tests + dev.

- `pnpm add -D msw`
- `pnpm dlx msw init public/ --save`

Source: https://mswjs.io/

### Cloudflare Workers + Wrangler 3

Edge functions, KV/D1/R2/Durable Objects.

- `pnpm dlx wrangler@latest init my-worker`
- `pnpm dlx wrangler deploy`
- `pnpm dlx wrangler pages deploy ./dist`

Source: https://developers.cloudflare.com/workers/ · Skill: `cloudflare-workers-edge-functions`

### Hono

Modern lightweight web framework. Cloudflare/Vercel/Bun/Deno/Node compatible.

- `pnpm add hono`

Source: https://hono.dev/

### PartyKit

Multiplayer on Cloudflare Durable Objects.

- `pnpm dlx partykit@latest init`
- `pnpm dlx partykit deploy`

Source: https://docs.partykit.io/

### motion (Framer Motion rebrand)

Declarative animations + gestures. Framework-agnostic since 2024 rebrand.

- `pnpm add motion`

Source: https://motion.dev/ · Skill: `framer-motion-view-transitions-api`

### View Transitions API

Native browser API for cross-page or cross-element morphs.

- `document.startViewTransition(() => updateDOM())`
- Stable in Chrome / Edge / Safari Tech Preview / Firefox Nightly

Source: https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API

### next-intl / Paraglide JS

i18n for Next 15. next-intl for locale routing + RSC-safe; Paraglide JS for tree-shakeable + type-safe (smaller bundle).

- `pnpm add next-intl`
- `pnpm add @inlang/paraglide-next`

Source: https://next-intl-docs.vercel.app/ · https://inlang.com/m/gerre34r/library-inlang-paraglideJs · Skill: `i18n-next-intl-paraglide`

### Clerk / Auth.js v5 / Lucia v3

Auth options. Clerk = paid SaaS, drop-in. Auth.js v5 = OSS, framework-agnostic. Lucia v3 = lightweight lib.

- `pnpm add @clerk/nextjs` (Clerk)
- `pnpm add next-auth@beta` (Auth.js v5)
- `pnpm add lucia` (Lucia v3)

Source: https://clerk.com/ · https://authjs.dev/ · https://lucia-auth.com/ · Skill: `auth-clerk-authjs-lucia`

### Stripe Elements / Checkout

Payments. Checkout = hosted (simplest, PCI handled). Elements = inline custom UX with Payment Intents. Connect = marketplace.

- `pnpm add stripe @stripe/stripe-js @stripe/react-stripe-js`
- `stripe listen --forward-to localhost:3000/api/webhook` (for testing)

Source: https://docs.stripe.com/ · Skill: `payments-stripe-elements-checkout`

### Payload CMS 3 / Sanity / Strapi

Payload = TS-first, installs into Next 15. Sanity = structured content + Studio. Strapi = self-hosted OSS.

- `pnpm dlx create-payload-app`
- `pnpm create sanity@latest`
- `pnpm dlx strapi new`

Source: https://payloadcms.com/ · https://www.sanity.io/ · https://strapi.io/

### Vercel CLI / wrangler / netlify-cli

Deployment CLIs.

- `pnpm dlx vercel deploy --prod`
- `pnpm dlx wrangler pages deploy ./dist`
- `pnpm dlx netlify deploy --prod`

Source: https://vercel.com/docs/cli · https://developers.cloudflare.com/workers/wrangler/

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| New Next.js project | `next-15-app-router-ppr` | + `tailwind-4-css-architecture`, `typescript-5-advanced-patterns` |
| New Svelte app | `svelte-5-runes-sveltekit` | + `vite-vitest-modern-toolchain` |
| New Vue / Nuxt app | `vue-3-composition-api-composables` | + `tailwind-4-css-architecture` |
| Content site / blog / docs | `astro-islands-content-first` | minimal JS, SEO-strong |
| RSC vs client decision | `react-19-server-components-actions` | + `next-15-app-router-ppr` |
| Form with validation | `react-hook-form-zod-valibot-forms` | + Server Action via `react-19-server-components-actions` |
| State management | `zustand-jotai-state-management` | + `tanstack-query-router-store` for server state |
| Design system | `shadcn-radix-headless-components` | + `storybook-chromatic-design-system`, `tailwind-4-css-architecture` |
| a11y audit | `accessibility-wcag-22-aa-axe-core` | + `playwright-e2e-stability` for E2E a11y |
| Slow page / Lighthouse fail | `core-web-vitals-lcp-inp-cls` | + `bundle-size-code-splitting-tree-shaking` |
| Big JS bundle | `bundle-size-code-splitting-tree-shaking` | size-limit + Knip + bundle-analyzer |
| E2E tests | `playwright-e2e-stability` | + `accessibility-wcag-22-aa-axe-core` for a11y E2E |
| Visual regression | `storybook-chromatic-design-system` | Chromatic primary; Percy / Lost-pixel alts |
| Lint + format setup | `biome-eslint-prettier-lint-format` | Biome migration from ESLint+Prettier |
| Edge function | `cloudflare-workers-edge-functions` | + Hono / PartyKit |
| Animation | `framer-motion-view-transitions-api` | motion + View Transitions |
| i18n setup | `i18n-next-intl-paraglide` | next-intl OR Paraglide JS; + `deepl-mcp` |
| Auth | `auth-clerk-authjs-lucia` | Clerk paid → Auth.js OSS → Lucia minimal |
| Payments | `payments-stripe-elements-checkout` | Stripe Elements + Checkout + Connect |
| CRA → Vite / Next migration | `vite-vitest-modern-toolchain` + `next-15-app-router-ppr` | + codemods |
| React 18 → 19 migration | `react-19-server-components-actions` | `codemod react/19/migration-recipe` |
| Webpack → Vite migration | `vite-vitest-modern-toolchain` | + worktree, manual config port |
| Type complexity | `typescript-5-advanced-patterns` | satisfies + conditional types + type-fest |
| Deploy to Vercel/CF/Netlify | `cloudflare-workers-edge-functions` | + default skill `vercel-cli-with-tokens` / `deploy-to-vercel` |

---

## Closing rules

Ship typed, accessible, fast, tested frontend code. Treat bytes shipped and a11y compliance as hostile budgets you have to defend. Reach for the SOTA skill pack first; only direct (write a plan instead of code) when the user explicitly asks.
