# Frontend Engineer — Use Cases

**Tier:** specialized · **Category:** engineering
**Core job:** Write, review, debug, refactor, optimize, audit, test, and deploy production frontend code in React 19 / Next 15 / Svelte 5 / Vue 3 / Astro on top of TypeScript.

> Ships with the SOTA 2026 frontend stack (React 19, Next 15 PPR, Svelte 5 runes, Vue 3.5, Astro 5, TanStack Query, Tailwind 4, Vitest 2, Playwright 1.50, Biome, shadcn/ui, web-vitals 4, axe-core, Chromatic). **Executes end-to-end** — scaffolds, writes, tests, audits, and deploys; does not stop at "here's a plan."

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it (vs. sibling agents).

---

## What this agent is supposed to do

### Build frontend code

- React 19 component authoring (controlled / uncontrolled, refs as props, portals, `useId`, `useImperativeHandle`)
- Server Components vs Client Components decision and authoring (RSC, Server Actions, `use()`, `useActionState`, `useOptimistic`)
- Next.js 15 App Router pages, layouts, route groups, parallel/intercepting routes, PPR
- Svelte 5 components with runes (`$state`, `$derived`, `$effect`, `$props`)
- Vue 3.5 + Nuxt 3 components (Composition API, `<script setup>`, `defineModel`, Suspense)
- Astro 5 Islands (content sites with selective hydration)
- TanStack Start / Solid / Qwik for non-React stacks when appropriate
- TypeScript 5.5+ advanced patterns (`satisfies`, conditional types, const generics, branded types)
- Forms with React Hook Form / Conform / VeeValidate / Felte + zod / valibot validation
- Animation with motion (Framer rebrand), View Transitions API, AutoAnimate, GSAP for timeline-driven

### Architect frontend systems

- State management decision (Zustand / Jotai / TanStack Query / RSC / Redux legacy)
- Data fetching strategy (RSC `await` / TanStack Query / SWR / `use()` promises)
- Routing (Next App Router / TanStack Router / React Router 7 / SvelteKit / Vue Router / Nuxt)
- CSS architecture (Tailwind 4 / Panda / vanilla-extract / CSS Modules / UnoCSS)
- SSR vs SSG vs ISR vs SPA vs PPR decision
- Multi-tenant architecture (subdomain / path-based, Next middleware, SvelteKit hooks)
- Edge function authoring (Cloudflare Workers + Hono / Vercel Edge / Deno Deploy / PartyKit)
- Design system architecture (shadcn/ui + Radix + Storybook + Chromatic + design tokens)
- tRPC v11 / GraphQL clients (urql, Apollo, Relay) — typed end-to-end

### Audit + optimize

- Accessibility audit (WCAG 2.2 AA via axe-core + pa11y + Lighthouse + manual screen-reader testing)
- Core Web Vitals diagnosis + fix (LCP / INP / CLS — note INP replaced FID in March 2024)
- Bundle size analysis + optimization (size-limit, Knip, bundle-analyzer, dynamic imports, tree-shaking)
- Image optimization (next/image, Astro Image, sharp, AVIF/WebP)
- Font loading (next/font, fontsource, variable fonts, fallback metric matching)
- Hydration mismatch debugging (server-only refs in client paths, locale differences, time-dependent renders)
- Render performance (React Profiler, Million.js, Web Worker offload, `startTransition`, `scheduler.postTask`)

### Test + verify

- Unit + integration with Vitest 2.x (browser-mode for component tests)
- Component testing with Testing Library (React / Vue / Svelte)
- Network mocking with MSW 2.x
- E2E with Playwright 1.50+ (multi-browser, auto-waiting, traces, sharding, codegen)
- E2E stability patterns (web-first assertions, locators over selectors, fixtures, storage state)
- Visual regression CI (Chromatic primary; Percy / Reg-cli / Lost-pixel as alts)
- Storybook 8 documentation + Autodocs + Test addon

### Migrate + modernize

- CRA → Vite or Next 15 (CRA deprecated Feb 2025)
- Webpack → Vite / Turbopack / Rspack
- React 18 → React 19 (official codemod recipe)
- Next Pages Router → App Router
- ESLint + Prettier → Biome (and back-out paths)
- JavaScript → TypeScript (incremental, with strict-mode rollout)

### Tooling + workflow

- Lint + format setup (Biome / Oxlint / ESLint 9 flat config + Prettier 3 / Stylelint)
- Modern Node / Bun / pnpm setup
- Git Conventional Commits + visual regression PR comments
- Pre-commit hooks (lint-staged + husky / lefthook)
- CI a11y gate, perf budget gate (size-limit), Lighthouse CI gate

### Integrate + deploy

- Auth integration (Clerk / Auth.js v5 / Lucia v3 / WorkOS / Supabase Auth)
- Payments (Stripe Elements / Checkout / Connect; Paddle / Lemon Squeezy alts)
- Real-time (PartyKit / Yjs / Liveblocks / Ably / Pusher / SSE / WebSocket)
- CMS integration (Payload 3 / Sanity / Strapi / Builder.io / Contentful)
- i18n (next-intl / Paraglide JS / Lingui / react-intl / @astrojs/i18n)
- Deploy to Vercel / Cloudflare Pages / Netlify / SST / self-hosted Docker

---

## Execution status (SOTA — June 2026)

> Mandatory per-use-case table. One row per use case. The path column names the concrete agent execution mechanism. See `reference/SOTA_USE_CASES.md` for source URLs and per-use-case detail.

| # | Use case | SOTA mechanism | Path |
|---|---|---|---|
| 1 | React component authoring | React 19.x | `cli-anything` (`pnpm create vite@latest --template react-ts`) + `filesystem` |
| 2 | RSC vs Client decision | Next 15 RSC + `"use client"` | `cli-anything` (`pnpm dlx create-next-app`) + `filesystem` |
| 3 | Server Actions + form state | Next 15 + zod + `useActionState` | `cli-anything` (`pnpm add zod`) + `filesystem` |
| 4 | Vue 3 Composition API | Vue 3.5 + Nuxt 3 | `cli-anything` (`pnpm create vue@latest`) + `filesystem` |
| 5 | Svelte 5 runes | Svelte 5 + SvelteKit | `cli-anything` (`pnpm create svelte@latest`) + `filesystem` |
| 6 | Astro Islands | Astro 5 + Content Collections v2 | `cli-anything` (`pnpm create astro@latest`) + `filesystem` |
| 7 | TypeScript advanced patterns | TS 5.5+ + type-fest + ts-reset | `cli-anything` (`pnpm add -D typescript@latest type-fest`) |
| 8 | State management | Zustand / Jotai / TanStack Query | `cli-anything` (`pnpm add zustand jotai @tanstack/react-query`) |
| 9 | Data fetching | TanStack Query 5 + RSC `use()` | `cli-anything` (`pnpm add @tanstack/react-query`) |
| 10 | Form handling | React Hook Form + zod / Conform | `cli-anything` (`pnpm add react-hook-form @hookform/resolvers zod`) |
| 11 | Routing | TanStack Router 1 / Next App / React Router 7 / SvelteKit | `cli-anything` (`pnpm add @tanstack/react-router`) |
| 12 | CSS architecture | Tailwind 4 + Panda + vanilla-extract | `cli-anything` (`pnpm add tailwindcss@latest`) |
| 13 | Design system | shadcn/ui + Radix + Storybook 8 + Chromatic | `cli-anything` (`pnpm dlx shadcn@latest init`) |
| 14 | Accessibility audit | axe-core + pa11y + Lighthouse + react-aria | `cli-anything` (`pnpm add -D @axe-core/playwright`) + `playwright-mcp` |
| 15 | Core Web Vitals (LCP/INP/CLS) | web-vitals 4 + Lighthouse CI + Million.js | `cli-anything` (`pnpm dlx @lhci/cli autorun`) + `playwright-mcp` |
| 16 | Bundle size optimization | size-limit + Knip + bundle-analyzer | `cli-anything` (`pnpm add -D size-limit knip`) |
| 17 | Image optimization | next/image + Astro Image + sharp | `cli-anything` (`pnpm add sharp`) |
| 18 | Font loading | next/font + fontsource + variable fonts | `cli-anything` (native to Next; `pnpm add @fontsource/inter`) |
| 19 | Edge functions | Cloudflare Workers + Hono + Vercel Edge | `cli-anything` (`pnpm dlx wrangler@latest deploy`) + `cloudflare-mcp` |
| 20 | SSR/SSG/ISR/SPA/PPR decision | Next 15 PPR + Astro SSG + Vite SPA | Decision rule + scaffold via `cli-anything` |
| 21 | Internationalization | next-intl + Paraglide JS + ICU | `cli-anything` (`pnpm add next-intl`) + `deepl-mcp` |
| 22 | Testing strategy | Vitest 2 + Playwright 1.50 + MSW 2 + Chromatic | `cli-anything` (`pnpm add -D vitest playwright msw`) + `playwright-mcp` |
| 23 | E2E test stability | Playwright web-first assertions + traces | `cli-anything` (`pnpm exec playwright test --trace on`) + `playwright-mcp` |
| 24 | Storybook documentation | Storybook 8 + CSF 3 + Autodocs | `cli-anything` (`pnpm dlx storybook@latest init`) |
| 25 | Visual regression CI | Chromatic / Percy / Lost-pixel | `cli-anything` (`pnpm dlx chromatic --project-token`) + `github-api` |
| 26 | Lint + format | Biome / Oxlint / ESLint 9 + Prettier 3 | `cli-anything` (`pnpm dlx biome init`) |
| 27 | Webpack → Vite/Turbopack/Rspack migration | Vite 5/6 / Turbopack / Rspack | `cli-anything` (`pnpm create vite@latest`) + `using-git-worktrees` |
| 28 | CRA → Vite or Next 15 migration | Codemods + `@next/codemod` | `cli-anything` (`pnpm dlx @next/codemod cra-to-nextjs`) |
| 29 | React 18 → React 19 migration | Official codemod recipe | `cli-anything` (`pnpm dlx codemod react/19/migration-recipe`) |
| 30 | tRPC / GraphQL clients | tRPC v11 + urql + Apollo | `cli-anything` (`pnpm add @trpc/server @trpc/client`) |
| 31 | Multi-tenant architecture | Next middleware + SvelteKit hooks | `cli-anything` + `filesystem` |
| 32 | Auth integration | Clerk / Auth.js v5 / Lucia v3 | `cli-anything` (`pnpm add @clerk/nextjs` / `next-auth@beta` / `lucia`) |
| 33 | Payments | Stripe Elements / Checkout / Connect | `cli-anything` (`pnpm add stripe @stripe/react-stripe-js`) |
| 34 | Real-time (WS / SSE / multiplayer) | PartyKit + Yjs + Liveblocks + Ably | `cli-anything` (`pnpm dlx partykit init`) |
| 35 | Animation | motion (Framer rebrand) + View Transitions | `cli-anything` (`pnpm add motion`) |
| 36 | CMS integration | Payload 3 + Sanity + Strapi + Builder | `cli-anything` (`pnpm dlx create-payload-app`) |
| 37 | Deploy (Vercel / Cloudflare / Netlify) | Vercel CLI / wrangler / netlify-cli | `cli-anything` (`pnpm dlx vercel deploy --prod`) + default skills `vercel-cli-with-tokens` / `deploy-to-vercel` |

---

## Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Auth via Clerk | ⚠ | Clerk requires paid SaaS plan for production volume. Free tier works for prototyping. OSS fallbacks (Auth.js v5, Lucia v3) ship in the skill pack and work immediately. |
| Payments via Stripe | ⚠ | Stripe production requires a verified merchant account. Test mode works with sandbox keys (free). Alts (Paddle, Lemon Squeezy as merchant-of-record) covered. |
| Real-time via Ably / Liveblocks / Pusher | ⚠ | Managed SaaS plans (paid). OSS fallback (PartyKit on Cloudflare Workers + Yjs CRDTs) ships in scope and works immediately. |
| Cross-browser visual regression for non-Chromium engines | ⚠ | Chromatic covers Chrome by default; multi-browser coverage requires the Storybook play-function E2E approach or Percy enterprise plan. |
| Production backend / database design | ✗ | Out of scope. Hand off to `senior-python-engineer`. |
| CI infrastructure setup (Docker, GitHub Actions, Kubernetes) | ✗ | Out of scope beyond writing the workflow .yml. Hand off to `devops-engineer`. |
| Product strategy / user research / spec authoring | ✗ | Out of scope. Hand off to `product-manager`. |
| Component-library reference docs (long-form) | ✗ | Out of scope beyond Storybook Autodocs. Hand off to `technical-writer`. |
| Native mobile (iOS/Android/React Native) | ✗ | This agent is web-only. React Native / Expo would be a separate specialist (v1). |

**Verdict (June 2026): ~95% fulfillment.** Every documented frontend engineering use case has a SOTA execution path via `cli-anything` + the bundled skill pack. The 3 ⚠ rows depend on the recipient owning paid SaaS accounts; OSS fallbacks ship in scope for all three. The 5 ✗ rows are genuine sibling-agent hand-offs (backend, devops, product, docs, mobile).

---

## When to use this agent

- "Build a Next 15 app with Server Components + Server Actions for a SaaS dashboard"
- "Review this React PR for a11y, perf, and bundle impact"
- "Our INP is 450ms on the search page — diagnose and fix"
- "Migrate this CRA app to Vite (or to Next 15)"
- "Set up Storybook 8 with Chromatic visual regression in CI"
- "Add Playwright E2E tests with a11y assertions to the checkout flow"
- "Replace ESLint + Prettier with Biome"
- "Build a design system from shadcn/ui primitives with Storybook docs"
- "Add i18n with next-intl (or Paraglide JS) for English + Japanese + Spanish"
- "Wire Stripe Checkout into the Next.js pricing page"
- "Deploy this app to Cloudflare Pages with a Hono Worker for the API"
- "Audit this site against WCAG 2.2 AA and produce a fix list"

---

## When NOT to use this agent

- **Backend Python / FastAPI / Django / data pipelines** → hand off to `senior-python-engineer`
- **CI infrastructure / Docker / Kubernetes / production hosting strategy** → hand off to `devops-engineer`
- **Product / spec / user research / feature prioritization** → hand off to `product-manager`
- **Component library long-form documentation / API reference docs** → hand off to `technical-writer`
- **Native mobile (React Native, Expo, iOS, Android)** → out of scope (v1 specialist planned)
- **Visual / brand design itself** (you implement design; design is upstream) → defer to the user's design lead or a design specialist (v1)
- **Anything outside frontend web engineering** — answer briefly and stay focused on the role
