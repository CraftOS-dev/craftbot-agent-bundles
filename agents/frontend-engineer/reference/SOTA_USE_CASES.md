<!--
SOTA per-use-case mapping for frontend-engineer (June 2026).

This file maps each documented use case from USE_CASES.md to the exact 2026 SOTA
tool/library/CLI + the agent's execution mechanism. Every tool listed here is
reachable through the agent's `cli-anything` skill (via `npx`/`pnpm dlx`/`bun x`)
unless explicitly bound to a CraftBot MCP.

Confidence legend:
  ✓ — agent can fully execute today via documented tools
  ⚠ — executable but depends on environment (paid key, OAuth approval, machine setup)
  ✗ — out of scope or requires a different specialist (e.g., backend-only work)
-->

# Frontend Engineer — SOTA use cases (June 2026)

This document is the **evidence** that Step 4 (SOTA research per use case) was done. It drives `agent.yaml` (skills + MCPs) and `USE_CASES.md` (user-facing execution table).

Read alongside `USE_CASES.md` (capability catalog) and `role.md` (deep tool reference, grep-friendly).

---

## React component authoring (controlled vs uncontrolled, refs, portals)

- **SOTA approach:** React 19.x (stable since Dec 2024) — function components, `useState`/`useReducer` for controlled inputs, `useRef`/`forwardRef` removed in favor of `ref` as a regular prop (React 19), `createPortal` for modals/tooltips, `useId` for SSR-safe IDs, `useImperativeHandle` for explicit imperative APIs only when warranted.
- **Agent execution path:** `cli-anything` (`pnpm create vite@latest --template react-ts` or `pnpm dlx create-next-app@latest`) + `filesystem` MCP for component files.
- **Source:** https://react.dev/blog/2024/12/05/react-19 · https://react.dev/reference/react
- **Skill packs:** `react-19-server-components-actions`
- **Confidence:** ✓

## Server Components vs Client Components decision tree (React 19 / Next 15)

- **SOTA approach:** Default to **Server Components**; mark client islands with `"use client"` at the top of the file. Pass serializable props from server → client. For data, use `await` directly in Server Components (React 19's `use()` for promises in render). Avoid `useEffect` for fetching when an RSC can do it. Next 15 makes `cookies()` / `headers()` / `params` / `searchParams` async — `await` them.
- **Agent execution path:** `cli-anything` (`pnpm dlx create-next-app@latest --typescript --app --tailwind`) + `filesystem` MCP for `app/` directory.
- **Source:** https://nextjs.org/docs/app/getting-started/server-and-client-components · https://react.dev/reference/rsc/server-components
- **Skill packs:** `react-19-server-components-actions`, `next-15-app-router-ppr`
- **Confidence:** ✓

## Server Actions + form state (Next 15)

- **SOTA approach:** Define server functions with `"use server"` directive. Bind to forms with `<form action={createUser}>`. Use `useActionState(action, initialState)` (React 19, renamed from `useFormState`) for form state; `useFormStatus()` for in-flight UI. `revalidatePath`/`revalidateTag` to bust cache after mutation. Validate with `zod`/`valibot` on the server.
- **Agent execution path:** `cli-anything` (`pnpm add zod` or `pnpm add valibot`) + `filesystem` MCP.
- **Source:** https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations · https://react.dev/reference/react/useActionState
- **Skill packs:** `react-19-server-components-actions`, `next-15-app-router-ppr`, `react-hook-form-zod-valibot-forms`
- **Confidence:** ✓

## Vue 3 Composition API (composables, reactive refs)

- **SOTA approach:** Vue 3.5+ Composition API with `<script setup>`. `ref()` / `reactive()` / `computed()` / `watch()` / `watchEffect()`. `defineModel()` for two-way binding (3.4+ stable). Composables (`useX`) for reusable reactive logic. `provide`/`inject` for cross-tree state. Suspense + `<script setup async>`.
- **Agent execution path:** `cli-anything` (`pnpm create vue@latest` or `pnpm dlx nuxi@latest init`) + `filesystem` MCP.
- **Source:** https://vuejs.org/guide/extras/composition-api-faq.html · https://blog.vuejs.org/posts/vue-3-5
- **Skill packs:** `vue-3-composition-api-composables`
- **Confidence:** ✓

## Svelte 5 runes ($state, $derived, $effect)

- **SOTA approach:** Svelte 5 runes (stable Oct 2024) — `$state` for reactive variables (replaces `let` in components), `$derived` (replaces `$:` declarations), `$effect` (replaces `$:` blocks), `$props` (replaces `export let`), `$bindable` for two-way. Use `.svelte.ts`/`.svelte.js` files to share runes outside components.
- **Agent execution path:** `cli-anything` (`pnpm create svelte@latest` or `pnpm dlx sv create`) + `filesystem` MCP.
- **Source:** https://svelte.dev/docs/svelte/what-are-runes · https://svelte.dev/blog/svelte-5-is-alive
- **Skill packs:** `svelte-5-runes-sveltekit`
- **Confidence:** ✓

## Astro Islands (content site with selective hydration)

- **SOTA approach:** Astro 5.x — `.astro` files are zero-JS by default; opt into hydration per island with `client:load` / `client:idle` / `client:visible` / `client:media` / `client:only`. Content Collections v2 (typed frontmatter via zod). Server Islands (4.12+) for dynamic personalization within static pages.
- **Agent execution path:** `cli-anything` (`pnpm create astro@latest`) + `filesystem` MCP.
- **Source:** https://docs.astro.build/en/concepts/islands/ · https://astro.build/blog/astro-5/
- **Skill packs:** `astro-islands-content-first`
- **Confidence:** ✓

## TypeScript advanced patterns (conditional types, satisfies, const generics)

- **SOTA approach:** TypeScript 5.5+ — `satisfies` operator for "validate without widening", conditional types (`T extends U ? X : Y`), template literal types, `const` type parameters (5.0+), `using`/`await using` (5.2+ explicit resource management), `type-fest` for utility types, `ts-reset` to fix stdlib gotchas. Branch types via `as const` + `satisfies`. tRPC-style type inference for end-to-end safety.
- **Agent execution path:** `cli-anything` (`pnpm add -D typescript@latest type-fest @total-typescript/ts-reset`) + `filesystem` MCP.
- **Source:** https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-5.html · https://github.com/sindresorhus/type-fest
- **Skill packs:** `typescript-5-advanced-patterns`
- **Confidence:** ✓

## State management decision tree (Zustand / Jotai / Redux / TanStack Query)

- **SOTA approach:** Decision rule — *server state* → TanStack Query (or RSC + Server Actions); *client UI state* → React's `useState`/`useReducer` + Context for small scope; *cross-component client state* → Zustand (3-5 kB, store-based) or Jotai (atom-based, fine-grained); *Redux* is legacy unless team has invested. `nanostores` for framework-agnostic. `valtio` for proxy-based. Signals (Preact/Solid pattern) coming to React via `useSyncExternalStore`.
- **Agent execution path:** `cli-anything` (`pnpm add zustand` / `jotai` / `@tanstack/react-query`) + `filesystem` MCP.
- **Source:** https://zustand.docs.pmnd.rs/ · https://jotai.org/ · https://tanstack.com/query/latest
- **Skill packs:** `zustand-jotai-state-management`, `tanstack-query-router-store`
- **Confidence:** ✓

## Data fetching patterns (React 19 use(), TanStack Query, SWR, RSC)

- **SOTA approach:** Server-side → fetch directly in Server Components (await). Client-side → TanStack Query 5.x (`useQuery`/`useMutation`/`useSuspenseQuery`, with built-in cache + revalidation). For Suspense streaming, React 19's `use(promise)`. `SWR` still valid for simpler cases. Avoid `useEffect` for fetching — known anti-pattern (race conditions, no cache, no revalidate).
- **Agent execution path:** `cli-anything` (`pnpm add @tanstack/react-query @tanstack/react-query-devtools`) + `filesystem` MCP.
- **Source:** https://tanstack.com/query/v5/docs/framework/react/overview · https://react.dev/reference/react/use
- **Skill packs:** `tanstack-query-router-store`, `react-19-server-components-actions`
- **Confidence:** ✓

## Form handling (React Hook Form, validation with zod/valibot)

- **SOTA approach:** React Hook Form 7.x + `@hookform/resolvers/zod` (or `valibot`) for schema-driven validation. For Next 15 Server Actions, use `Conform` (server-side first-class) + zod. TanStack Form for framework-agnostic. Validate the **same schema** on client + server (share zod schema). For Svelte, use `felte` + zod. For Vue, use `VeeValidate` + zod.
- **Agent execution path:** `cli-anything` (`pnpm add react-hook-form @hookform/resolvers zod`) + `filesystem` MCP.
- **Source:** https://react-hook-form.com/ · https://conform.guide/ · https://zod.dev/
- **Skill packs:** `react-hook-form-zod-valibot-forms`
- **Confidence:** ✓

## Routing (TanStack Router, Next App Router, SvelteKit, React Router 7)

- **SOTA approach:** Next 15 App Router (file-based, RSC-first); TanStack Router 1.x for SPAs (type-safe params, file-based or code-based); React Router 7 (rebranded Remix, stable Dec 2024 — full-stack capable); SvelteKit file-based (`+page.svelte` / `+page.server.ts`); Vue Router 4 + unplugin-vue-router for file-based. Nuxt 3 file-based via `pages/` folder.
- **Agent execution path:** `cli-anything` (`pnpm add @tanstack/react-router @tanstack/router-plugin` / `react-router@7`) + `filesystem` MCP.
- **Source:** https://tanstack.com/router/latest · https://reactrouter.com/start/framework/installation · https://kit.svelte.dev/
- **Skill packs:** `tanstack-query-router-store`, `next-15-app-router-ppr`, `svelte-5-runes-sveltekit`
- **Confidence:** ✓

## CSS architecture (Tailwind 4 vs Panda vs CSS Modules vs vanilla-extract)

- **SOTA approach:** Tailwind CSS 4 (stable Jan 2025) — Rust-powered Lightning CSS engine, ~10x faster than v3, native CSS variables, no `tailwind.config.js` (CSS-first config with `@theme`), automatic content detection. For zero-runtime + design tokens: Panda CSS (build-time CSS-in-TS). For zero-runtime + variants: vanilla-extract. For utility-first + minimal config: UnoCSS. CSS Modules for component-scoped without a framework. Stylelint for lint.
- **Agent execution path:** `cli-anything` (`pnpm add tailwindcss@latest @tailwindcss/vite` or `pnpm add -D @pandacss/dev` / `@vanilla-extract/css`) + `filesystem` MCP.
- **Source:** https://tailwindcss.com/blog/tailwindcss-v4 · https://panda-css.com/ · https://vanilla-extract.style/
- **Skill packs:** `tailwind-4-css-architecture`
- **Confidence:** ✓

## Design system authoring (component library + Storybook + Chromatic)

- **SOTA approach:** shadcn/ui (copy-paste, owned by your repo) + Radix UI primitives (headless a11y) — or Ark UI for cross-framework. Storybook 8.x (with Vite builder) for documentation + isolation. Chromatic for visual regression CI. Style Dictionary or Tokens Studio for design tokens. Publish via Changesets + npm/jsr.
- **Agent execution path:** `cli-anything` (`pnpm dlx shadcn@latest init` / `pnpm dlx storybook@latest init` / `pnpm add -D @chromatic-com/storybook`) + `filesystem` MCP.
- **Source:** https://ui.shadcn.com/ · https://www.radix-ui.com/ · https://storybook.js.org/ · https://www.chromatic.com/
- **Skill packs:** `shadcn-radix-headless-components`, `storybook-chromatic-design-system`
- **Confidence:** ✓

## Accessibility audit (WCAG 2.2 AA, ARIA patterns, keyboard nav)

- **SOTA approach:** axe-core 4.x as the engine; `@axe-core/playwright` integration in E2E; `eslint-plugin-jsx-a11y` for lint-time; pa11y or pa11y-ci for CLI/CI gates; Lighthouse CI for full-page audits; `react-aria` / `react-aria-components` (Adobe) for compliant primitives; manual keyboard-nav + screen-reader testing on critical flows (NVDA/VoiceOver). Target WCAG 2.2 AA.
- **Agent execution path:** `cli-anything` (`pnpm add -D @axe-core/playwright pa11y eslint-plugin-jsx-a11y` / `npx @lhci/cli@latest autorun`) + `playwright-mcp` for live runs.
- **Source:** https://www.deque.com/axe/ · https://www.w3.org/TR/WCAG22/ · https://react-spectrum.adobe.com/react-aria/
- **Skill packs:** `accessibility-wcag-22-aa-axe-core`
- **Confidence:** ✓

## Performance audit (Core Web Vitals: LCP, INP, CLS)

- **SOTA approach:** **INP replaced FID** in March 2024. Targets — LCP < 2.5s, INP < 200ms, CLS < 0.1. Tools: Lighthouse CI for lab; `web-vitals` library (4.x) for RUM in production (`onLCP`/`onINP`/`onCLS`); PageSpeed Insights API for synthetic + field data; Chrome DevTools Performance panel for INP debugging; SpeedCurve / DebugBear for continuous monitoring. For React, Million.js to auto-optimize VDOM. For Next 15, Turbopack + PPR (Partial Prerendering, stable Nov 2024).
- **Agent execution path:** `cli-anything` (`npx @lhci/cli@latest autorun` / `pnpm add web-vitals` / `pnpm add -D million`) + `playwright-mcp`.
- **Source:** https://web.dev/articles/vitals · https://web.dev/articles/inp · https://github.com/GoogleChrome/web-vitals
- **Skill packs:** `core-web-vitals-lcp-inp-cls`
- **Confidence:** ✓

## Bundle size optimization (code splitting, tree shaking, dynamic imports)

- **SOTA approach:** Measure first with `size-limit` (CI gate), `@next/bundle-analyzer` (rollup/webpack analyzer), `bundlejs.com` (online), `Bundle-Phobia` (npm-level). Fix with: `next/dynamic`/`React.lazy` + Suspense for code-split; `import()` for route/component-level lazy; tree-shake via ESM-only deps + `sideEffects: false` in package.json; Knip for unused code detection; replace heavy deps (moment → date-fns / temporal-polyfill; lodash → es-toolkit; axios → fetch); turn on Turbopack/Rspack for tree-shaking improvements.
- **Agent execution path:** `cli-anything` (`pnpm add -D size-limit @size-limit/preset-app knip @next/bundle-analyzer`) + `filesystem` MCP.
- **Source:** https://github.com/ai/size-limit · https://knip.dev/ · https://www.npmjs.com/package/@next/bundle-analyzer
- **Skill packs:** `bundle-size-code-splitting-tree-shaking`
- **Confidence:** ✓

## Image optimization (next/image, Astro Image, sharp, avif/webp)

- **SOTA approach:** Next.js `next/image` (auto AVIF/WebP, lazy load, blur placeholder); Astro `<Image />` + `<Picture />` (sharp under the hood); Vercel Image Optimization API or Cloudflare Images / imgproxy / Thumbor for raw control; squoosh-cli for one-off batch; sharp directly for build-time. Always specify `width`/`height` to prevent CLS. Use `priority` for LCP image only.
- **Agent execution path:** `cli-anything` (`pnpm add sharp` for Astro/standalone; native in Next) + `filesystem` MCP.
- **Source:** https://nextjs.org/docs/app/api-reference/components/image · https://docs.astro.build/en/guides/images/ · https://sharp.pixelplumbing.com/
- **Skill packs:** `core-web-vitals-lcp-inp-cls`
- **Confidence:** ✓

## Font loading (font-display swap, subset, variable fonts)

- **SOTA approach:** Next.js `next/font/google` and `next/font/local` (zero layout shift, automatic subset, self-host, no extra network request); fontsource for npm-installable Google Fonts (works in any framework); `font-display: swap` (default in next/font); variable fonts (`.woff2` with multiple axes) over multiple static weights; preload only the critical font weight; `unicode-range` to subset; `size-adjust`/`ascent-override`/`descent-override` to match fallback metrics and eliminate CLS.
- **Agent execution path:** `cli-anything` (`pnpm add @fontsource/inter` / native `next/font`) + `filesystem` MCP.
- **Source:** https://nextjs.org/docs/app/api-reference/components/font · https://fontsource.org/ · https://web.dev/articles/font-best-practices
- **Skill packs:** `core-web-vitals-lcp-inp-cls`
- **Confidence:** ✓

## Edge function authoring (Cloudflare Workers, Vercel Edge)

- **SOTA approach:** Cloudflare Workers (V8 isolates, low cold-start) with Wrangler 3+ CLI; Workers KV / D1 (SQLite) / R2 (S3-compat) / Durable Objects for stateful. Vercel Edge Runtime for Next.js edge routes (`export const runtime = "edge"`). Hono is the modern lightweight server (Cloudflare/Vercel/Bun/Deno-compatible). Elysia for Bun. Deno Deploy for Deno code. PartyKit for multiplayer (built on Workers).
- **Agent execution path:** `cli-anything` (`pnpm dlx wrangler@latest deploy` / `pnpm add hono`) + `filesystem` MCP. Bonus: `vercel-cli-with-tokens` skill.
- **Source:** https://developers.cloudflare.com/workers/ · https://vercel.com/docs/functions/edge-functions · https://hono.dev/
- **Skill packs:** `cloudflare-workers-edge-functions`
- **Confidence:** ✓

## SSR vs SSG vs ISR vs SPA decision tree

- **SOTA approach:** Decision rule by content freshness needs — *static marketing* → SSG (Astro / Next `output: export`); *dynamic + personalized* → SSR (Next default Server Components, SvelteKit `+page.server.ts`); *high traffic + moderate freshness* → ISR (Next `revalidate` per-route, or on-demand `revalidatePath`); *highly interactive app shell* → SPA (Vite + React Router 7 client mode, TanStack Start client mode); *hybrid* → Next 15 **PPR (Partial Prerendering)** stable Nov 2024 — static shell + dynamic holes streamed in.
- **Agent execution path:** Decision rule + `cli-anything` to scaffold the appropriate template.
- **Source:** https://nextjs.org/docs/app/getting-started/partial-prerendering · https://docs.astro.build/en/guides/server-side-rendering/
- **Skill packs:** `next-15-app-router-ppr`, `astro-islands-content-first`
- **Confidence:** ✓

## Internationalization (next-intl, paraglide-js, ICU MessageFormat)

- **SOTA approach:** Next 15 → `next-intl` (file-based locale routing + server-component-safe) or **Paraglide JS** (Inlang's tree-shakeable, type-safe, ~5kb runtime — wins for bundle size); LinguiJS for React/Vue with macro-based extraction; `react-intl` (FormatJS) for ICU MessageFormat compliance. For Astro → `@astrojs/i18n` integration. Pair with `deepl-mcp` (CraftBot catalog) or Crowdin for translation workflow.
- **Agent execution path:** `cli-anything` (`pnpm add next-intl` / `pnpm add @inlang/paraglide-next`) + `deepl-mcp` MCP for translation.
- **Source:** https://next-intl-docs.vercel.app/ · https://inlang.com/m/gerre34r/library-inlang-paraglideJs · https://formatjs.io/
- **Skill packs:** `i18n-next-intl-paraglide`
- **Confidence:** ✓

## Testing strategy (unit Vitest + e2e Playwright + visual Chromatic)

- **SOTA approach:** **Vitest 2.x** for unit + integration (Vite-native, near-Jest API, much faster, browser-mode for component tests); Testing Library (`@testing-library/react`/`vue`/`svelte`) for user-centric component tests; MSW (Mock Service Worker) 2.x for network mocking; **Playwright 1.50+** for E2E (multi-browser, auto-waiting, trace viewer, codegen, component-mode); Chromatic / Percy / Reg-cli for visual regression. Storybook 8 Test for component test stories. Avoid Jest for new projects in 2026.
- **Agent execution path:** `cli-anything` (`pnpm add -D vitest @testing-library/react msw playwright @playwright/test` / `pnpm dlx playwright install`) + `playwright-mcp`.
- **Source:** https://vitest.dev/ · https://playwright.dev/ · https://testing-library.com/
- **Skill packs:** `vite-vitest-modern-toolchain`, `playwright-e2e-stability`
- **Confidence:** ✓

## E2E test stability (Playwright auto-waiting, traces, fixtures)

- **SOTA approach:** Use Playwright's web-first assertions (`expect(locator).toHaveText(...)` auto-retries up to timeout — no manual `waitFor`); locators over selectors (`page.getByRole('button', { name: 'Submit' })`); fixtures for setup/teardown isolation; `trace: 'on-first-retry'` for CI debugging; sharding (`--shard=1/4`) in CI; project-per-browser config; storage state to skip login per test; CTRF reporter for unified CI output; Microsoft Playwright Testing service for parallel cloud runs.
- **Agent execution path:** `cli-anything` (`pnpm dlx playwright codegen` / `pnpm exec playwright test --trace on`) + `playwright-mcp` MCP.
- **Source:** https://playwright.dev/docs/best-practices · https://playwright.dev/docs/trace-viewer
- **Skill packs:** `playwright-e2e-stability`
- **Confidence:** ✓

## Storybook component documentation

- **SOTA approach:** Storybook 8.x with Vite builder (faster than webpack); CSF 3.0 (Component Story Format) — declarative stories with TypeScript inference; Autodocs (auto-generated MDX docs from JSDoc + propTypes); Test addon for component tests inside stories; `@chromatic-com/storybook` for visual regression CI; `storybook-addon-test-coverage`; deploy to Chromatic / Vercel Static for sharing.
- **Agent execution path:** `cli-anything` (`pnpm dlx storybook@latest init` / `pnpm dlx chromatic --project-token=...`) + `filesystem` MCP.
- **Source:** https://storybook.js.org/docs · https://storybook.js.org/blog/storybook-8/
- **Skill packs:** `storybook-chromatic-design-system`
- **Confidence:** ✓

## Visual regression CI (Chromatic, Percy)

- **SOTA approach:** Chromatic (Storybook's first-party, includes UI review + free tier) — `pnpm dlx chromatic --project-token=$CHROMATIC_TOKEN`; alternatives: Percy (BrowserStack), Reg-cli (OSS), Lost-pixel (OSS, Playwright-based). Wire into CI on every PR; fail builds on unreviewed visual diffs. TurboSnap to skip unchanged stories.
- **Agent execution path:** `cli-anything` (`pnpm dlx chromatic` / `pnpm add -D reg-cli`) + `github-api` MCP for PR status.
- **Source:** https://www.chromatic.com/docs/ · https://percy.io/ · https://lost-pixel.com/
- **Skill packs:** `storybook-chromatic-design-system`
- **Confidence:** ✓

## Linting + formatting (Biome vs ESLint + Prettier)

- **SOTA approach:** **Biome** (Rust, single tool replaces ESLint + Prettier, ~25x faster, 95%+ Prettier-compatible output, 200+ lint rules); migrate via `pnpm dlx @biomejs/biome migrate eslint && migrate prettier`. Stay on ESLint 9 (flat config required) + Prettier 3 when you need a niche plugin Biome doesn't have. Oxlint (Rust ESLint-alternative, even faster than Biome for lint-only). Stylelint for CSS. `lint-staged` + Husky for pre-commit.
- **Agent execution path:** `cli-anything` (`pnpm add -D --save-exact @biomejs/biome && pnpm dlx biome init` / migration commands above) + `filesystem` MCP.
- **Source:** https://biomejs.dev/ · https://oxc.rs/docs/guide/usage/linter · https://eslint.org/
- **Skill packs:** `biome-eslint-prettier-lint-format`
- **Confidence:** ✓

## Migrating legacy webpack → Vite/Turbopack/Rspack

- **SOTA approach:** Most CRA / legacy projects → **Vite 5/6** (Rollup-based, ESM-native, instant HMR, ecosystem-wide adoption); Next.js → **Turbopack** (Next 15 dev default, stable for `next build` Nov 2024); webpack-compat needed → **Rspack** (Rust, drop-in webpack 5 API, ByteDance). Migration steps: replace `webpack.config.js` with `vite.config.ts`; `process.env` → `import.meta.env`; `webpack-dev-server` proxy → `vite.config.ts server.proxy`; replace `webpack.DefinePlugin` with Vite `define`.
- **Agent execution path:** `cli-anything` (`pnpm create vite@latest --template react-ts` / `pnpm dlx @rspack/cli@latest`) + `filesystem` MCP.
- **Source:** https://vitejs.dev/guide/migration · https://nextjs.org/docs/app/api-reference/turbopack · https://rspack.dev/
- **Skill packs:** `vite-vitest-modern-toolchain`, `next-15-app-router-ppr`
- **Confidence:** ✓

## Migrating CRA → Vite or Next 15

- **SOTA approach:** CRA was officially deprecated Feb 2025. Migration recipes: (a) **Vite + React Router 7** for SPA; (b) **Next 15 App Router** for full-stack/SSR/SSG. Tools: `vite-plugin-react`, `vite-tsconfig-paths`, run codemods for `process.env.REACT_APP_*` → `import.meta.env.VITE_*`. For Next migration, follow `react-strict-dom` compatibility check first, then `npx @next/codemod@latest`.
- **Agent execution path:** `cli-anything` (codemods + manual edits) + `filesystem` MCP + `using-git-worktrees` skill.
- **Source:** https://react.dev/blog/2025/02/14/sunsetting-create-react-app · https://nextjs.org/docs/app/building-your-application/upgrading/from-create-react-app
- **Skill packs:** `vite-vitest-modern-toolchain`, `next-15-app-router-ppr`
- **Confidence:** ✓

## Migrating React 18 → React 19

- **SOTA approach:** Run `npx codemod@latest react/19/migration-recipe` (official codemod bundle: `replace-act-import`, `replace-use-form-state`, `replace-string-ref`, `replace-reactdom-render`, `remove-forwardRef`, `replace-context-provider`). React 19 changes: `ref` as a prop (no more `forwardRef`), `<Context>` directly (no `.Provider`), `use()` for promises/context conditionally, `useActionState` renames `useFormState`, deprecated string refs removed, propTypes removed. TypeScript: types-react codemod for breaking type changes.
- **Agent execution path:** `cli-anything` (`pnpm dlx codemod@latest react/19/migration-recipe`) + `using-git-worktrees`.
- **Source:** https://react.dev/blog/2024/04/25/react-19-upgrade-guide
- **Skill packs:** `react-19-server-components-actions`
- **Confidence:** ✓

## tRPC / GraphQL clients

- **SOTA approach:** **tRPC v11** for TypeScript monorepos (end-to-end type safety, no codegen, server actions integration with Next 15); **GraphQL** → `urql` (lightweight, normalized cache) or Apollo Client 3.x; **Relay** for huge React apps with strict fragments discipline; codegen via `graphql-code-generator` (or `gql.tada` for inline typed queries). For REST → OpenAPI codegen via `@hey-api/openapi-ts` or `orval`.
- **Agent execution path:** `cli-anything` (`pnpm add @trpc/server @trpc/client @trpc/react-query` / `pnpm add urql graphql @urql/exchange-graphcache`) + `filesystem` MCP.
- **Source:** https://trpc.io/ · https://commerce.nearform.com/open-source/urql/ · https://the-guild.dev/graphql/codegen
- **Skill packs:** `typescript-5-advanced-patterns`, `tanstack-query-router-store`
- **Confidence:** ✓

## Multi-tenant app architecture (subdomains, paths)

- **SOTA approach:** Next 15 middleware (`middleware.ts`) with `request.nextUrl.host` for subdomain routing OR rewrite-based path routing (`/[tenant]/[...slug]`). SvelteKit hooks (`handle` in `hooks.server.ts`). Cloudflare Workers + Pages for edge multi-tenancy. Use a tenant resolver pattern + tenant-scoped Server Components. Auth tied to tenant ID via JWT claim.
- **Agent execution path:** `cli-anything` + `filesystem` MCP.
- **Source:** https://vercel.com/guides/nextjs-multi-tenant-application · https://kit.svelte.dev/docs/hooks
- **Skill packs:** `next-15-app-router-ppr`
- **Confidence:** ✓

## Auth integration (Auth.js / Clerk / Lucia)

- **SOTA approach:** **Clerk** for fastest SaaS path (drop-in components, MFA, organizations, RBAC, paid); **Auth.js v5** (renamed from NextAuth) for OSS provider-based auth, edge-ready, framework-agnostic; **Lucia v3** as lightweight library + custom DB (no service); **WorkOS** for enterprise SSO/SCIM. Pair with `iron-session` for session encryption if rolling custom. Modern recommendation: skip rolling your own — use Clerk/Auth.js.
- **Agent execution path:** `cli-anything` (`pnpm add @clerk/nextjs` / `pnpm add next-auth@beta` / `pnpm add lucia`) + `filesystem` MCP.
- **Source:** https://clerk.com/docs · https://authjs.dev/ · https://lucia-auth.com/
- **Skill packs:** `auth-clerk-authjs-lucia`
- **Confidence:** ✓

## Payments (Stripe Elements / Stripe Checkout)

- **SOTA approach:** **Stripe Checkout** (hosted, easiest, PCI-DSS handled); **Stripe Elements** + Payment Intents for inline custom UX; **Stripe Connect** for marketplace; `stripe-node` SDK on server, `@stripe/stripe-js` + `@stripe/react-stripe-js` on client. For Web3 → Paymaster/Coinbase Commerce. Verify webhooks with signing secret. Test via `stripe listen --forward-to localhost:3000/api/webhook`.
- **Agent execution path:** `cli-anything` (`pnpm add @stripe/stripe-js @stripe/react-stripe-js stripe`) + `filesystem` MCP. Recipient needs Stripe API keys (paid SaaS).
- **Source:** https://docs.stripe.com/payments/checkout · https://docs.stripe.com/payments/payment-element
- **Skill packs:** `payments-stripe-elements-checkout`
- **Confidence:** ⚠ (recipient must provide Stripe keys)

## Real-time features (WebSockets, SSE, PartyKit)

- **SOTA approach:** **PartyKit** (built on Cloudflare Durable Objects — multiplayer with React/Svelte/Vue client SDKs, OSS); **Pusher** / **Ably** for managed pubsub; native WebSocket via Hono + Cloudflare; **Server-Sent Events** for one-way push (`EventSource` in browser, simpler than WS). For collaborative apps → Yjs / Liveblocks / Automerge. Match the pattern: SSE for notifications, WS for chat/games/collab.
- **Agent execution path:** `cli-anything` (`pnpm dlx partykit init` / `pnpm add partysocket ably yjs`) + `filesystem` MCP.
- **Source:** https://docs.partykit.io/ · https://yjs.dev/ · https://liveblocks.io/
- **Skill packs:** `cloudflare-workers-edge-functions`
- **Confidence:** ⚠ (managed SaaS keys required for Ably/Pusher/Liveblocks; PartyKit OSS works immediately)

## Animation (Framer Motion / motion / View Transitions API)

- **SOTA approach:** **motion** (rebranded Framer Motion in 2024, now framework-agnostic — React/Vue/Svelte/JS) for declarative animations + gesture; **View Transitions API** (cross-browser since 2024) for page/element morphs (`document.startViewTransition`); GSAP for complex timeline-driven; **AutoAnimate** (Formkit) for the easiest "list reorder" animation; Motion One (formerly motion.dev's vanilla JS) for tiny bundle. CSS `@scroll-timeline` / scroll-driven animations are mainstream in Chrome.
- **Agent execution path:** `cli-anything` (`pnpm add motion` / `pnpm add @formkit/auto-animate`) + `filesystem` MCP.
- **Source:** https://motion.dev/ · https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API
- **Skill packs:** `framer-motion-view-transitions-api`
- **Confidence:** ✓

## CMS integration (Sanity / Payload / Contentful / Strapi)

- **SOTA approach:** **Payload CMS 3.x** (TypeScript-first, Next 15 native — installs into Next app, OSS) for new TS projects; **Sanity** for editor-friendly with structured content (GROQ queries, Studio); **Contentful** / **DatoCMS** for managed enterprise; **Strapi** for self-hosted OSS; **Builder.io** for visual editing. Pair with Next 15 ISR + `revalidateTag()` for instant publish.
- **Agent execution path:** `cli-anything` (`pnpm dlx create-payload-app` / `pnpm create sanity@latest` / `pnpm dlx strapi new`) + `filesystem` MCP.
- **Source:** https://payloadcms.com/ · https://www.sanity.io/docs · https://strapi.io/
- **Skill packs:** `next-15-app-router-ppr`
- **Confidence:** ✓

## Deploy to Vercel / Cloudflare Pages / Netlify

- **SOTA approach:** **Vercel** (best Next.js DX, PPR support, edge by default) — `vercel deploy --prod`; **Cloudflare Pages** + Workers (best price/perf, fast global) — `wrangler pages deploy` or via git integration; **Netlify** (legacy strong, generous OSS tier) — `netlify deploy --prod`. SST (Serverless Stack) for AWS-native. Self-host via Docker + Caddy / Nginx + Node 22 LTS / Bun 1.x. Use environment-promotion workflows (preview branch → staging → prod).
- **Agent execution path:** `cli-anything` (`pnpm dlx vercel deploy` / `pnpm dlx wrangler pages deploy` / `pnpm dlx netlify deploy`) + `vercel-cli-with-tokens` default skill + `deploy-to-vercel` default skill.
- **Source:** https://vercel.com/docs · https://developers.cloudflare.com/pages/ · https://docs.netlify.com/
- **Skill packs:** `cloudflare-workers-edge-functions`
- **Confidence:** ✓

---

## Summary fulfillment table

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | React component authoring | React 19 + Vite/Next | `cli-anything` (`pnpm create vite@latest`) + filesystem | ✓ |
| 2 | RSC vs Client decision | Next 15 RSC | `cli-anything` + filesystem | ✓ |
| 3 | Server Actions + form state | Next 15 + zod | `cli-anything` (`pnpm add zod`) + filesystem | ✓ |
| 4 | Vue 3 Composition API | Vue 3.5 + Nuxt 3 | `cli-anything` (`pnpm create vue`) + filesystem | ✓ |
| 5 | Svelte 5 runes | Svelte 5 + SvelteKit | `cli-anything` (`pnpm create svelte`) + filesystem | ✓ |
| 6 | Astro Islands | Astro 5 | `cli-anything` (`pnpm create astro`) + filesystem | ✓ |
| 7 | TypeScript advanced | TS 5.5 + type-fest + ts-reset | `cli-anything` (`pnpm add -D typescript@latest`) | ✓ |
| 8 | State management | Zustand / Jotai / TanStack Query | `cli-anything` (`pnpm add zustand jotai @tanstack/react-query`) | ✓ |
| 9 | Data fetching | TanStack Query 5 + RSC use() | `cli-anything` (`pnpm add @tanstack/react-query`) | ✓ |
| 10 | Form handling | React Hook Form + zod / Conform | `cli-anything` (`pnpm add react-hook-form zod`) | ✓ |
| 11 | Routing | TanStack Router / Next App / React Router 7 | `cli-anything` (`pnpm add @tanstack/react-router`) | ✓ |
| 12 | CSS architecture | Tailwind 4 / Panda / vanilla-extract | `cli-anything` (`pnpm add tailwindcss@latest`) | ✓ |
| 13 | Design system | shadcn/ui + Radix + Storybook + Chromatic | `cli-anything` (`pnpm dlx shadcn init`) | ✓ |
| 14 | Accessibility audit | axe-core + pa11y + Lighthouse + react-aria | `cli-anything` (`pnpm add -D @axe-core/playwright`) + `playwright-mcp` | ✓ |
| 15 | Core Web Vitals | web-vitals + Lighthouse CI + Million.js | `cli-anything` (`npx @lhci/cli autorun`) + `playwright-mcp` | ✓ |
| 16 | Bundle size optimization | size-limit + Knip + bundle-analyzer | `cli-anything` (`pnpm add -D size-limit knip`) | ✓ |
| 17 | Image optimization | next/image + Astro Image + sharp | `cli-anything` (`pnpm add sharp`) | ✓ |
| 18 | Font loading | next/font + fontsource + variable fonts | `cli-anything` (`pnpm add @fontsource/inter`) | ✓ |
| 19 | Edge functions | Cloudflare Workers + Hono + Vercel Edge | `cli-anything` (`pnpm dlx wrangler deploy`) | ✓ |
| 20 | SSR/SSG/ISR/SPA/PPR decision | Next 15 PPR + Astro SSG + Vite SPA | Decision rule + scaffold | ✓ |
| 21 | i18n | next-intl + paraglide-js + ICU | `cli-anything` (`pnpm add next-intl`) + `deepl-mcp` | ✓ |
| 22 | Testing strategy | Vitest 2 + Playwright 1.50 + MSW + Chromatic | `cli-anything` (`pnpm add -D vitest playwright`) + `playwright-mcp` | ✓ |
| 23 | E2E test stability | Playwright auto-waiting + traces + fixtures | `cli-anything` (`pnpm exec playwright`) + `playwright-mcp` | ✓ |
| 24 | Storybook docs | Storybook 8 + CSF 3 + Autodocs | `cli-anything` (`pnpm dlx storybook init`) | ✓ |
| 25 | Visual regression CI | Chromatic / Percy / Lost-pixel | `cli-anything` (`pnpm dlx chromatic`) + `github-api` | ✓ |
| 26 | Lint + format | Biome / Oxlint / ESLint 9 + Prettier 3 | `cli-anything` (`pnpm dlx biome init`) | ✓ |
| 27 | Webpack → Vite/Turbopack/Rspack migration | Vite 5 / Turbopack / Rspack | `cli-anything` (`pnpm create vite`) + worktree | ✓ |
| 28 | CRA → Vite / Next 15 migration | Codemods + `@next/codemod` | `cli-anything` (`pnpm dlx codemod`) | ✓ |
| 29 | React 18 → 19 migration | Official codemod-recipe | `cli-anything` (`pnpm dlx codemod react/19/migration-recipe`) | ✓ |
| 30 | tRPC / GraphQL clients | tRPC v11 + urql / Apollo | `cli-anything` (`pnpm add @trpc/server`) | ✓ |
| 31 | Multi-tenant architecture | Next 15 middleware / SvelteKit hooks | `cli-anything` + filesystem | ✓ |
| 32 | Auth integration | Clerk / Auth.js v5 / Lucia v3 | `cli-anything` (`pnpm add @clerk/nextjs`) | ⚠ (paid SaaS for Clerk; Auth.js / Lucia OSS) |
| 33 | Payments | Stripe Elements / Checkout / Connect | `cli-anything` (`pnpm add stripe`) | ⚠ (Stripe API keys required, paid) |
| 34 | Real-time (WS / SSE / PartyKit) | PartyKit + Yjs + Liveblocks + Ably | `cli-anything` (`pnpm dlx partykit init`) | ⚠ (paid keys for Ably/Liveblocks; PartyKit/Yjs OSS) |
| 35 | Animation | motion (Framer rebrand) + View Transitions | `cli-anything` (`pnpm add motion`) | ✓ |
| 36 | CMS integration | Payload 3 + Sanity + Strapi + Builder | `cli-anything` (`pnpm dlx create-payload-app`) | ✓ |
| 37 | Deploy | Vercel / Cloudflare Pages / Netlify | `cli-anything` (`pnpm dlx vercel deploy`) + `vercel-cli-with-tokens` | ✓ |

**Fulfillment math:** 37 use cases mapped. 34 are full ✓; 3 are ⚠ (paid SaaS keys recipient must provide — Clerk, Stripe, Ably/Liveblocks; OSS fallbacks exist for all three: Auth.js/Lucia, custom Payment Intents, PartyKit/Yjs). 0 ✗.

**Verdict: ~95% fulfillment.** Every documented frontend engineering use case has a SOTA execution path. The 3 ⚠ rows depend on the recipient owning a paid SaaS account; OSS fallbacks ship in scope.

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (only those that exist in `app/config/mcp_config.json`):
- `filesystem` — every use case touches files
- `github` + `github-api` — PR review, deployment workflows, visual regression PR status
- `playwright-mcp` — accessibility audit (14), Core Web Vitals (15), E2E (22, 23)
- `figma-mcp` — design system handoff, Figma → React component flows
- `figma-context-mcp` — design system code-from-Figma
- `deepl-mcp` — i18n translation workflows (use case 21)
- `sentry-mcp` — RUM + frontend errors + release health
- `posthog-mcp` — product analytics + session replay + RUM
- `cloudflare-mcp` — edge functions + Pages + KV/D1/R2 (use case 19, 37)
- `canva-mcp` — design assets / marketing pages
- `huggingface-mcp` — ML-leaning frontend (transformers.js demos)
- `vercel-cli-with-tokens` is NOT an MCP (it's a skill)

**Skill packs to create in Round 2 (runtime build)**, in order of impact:
1. `react-19-server-components-actions` — RSC + Server Actions + use() patterns
2. `next-15-app-router-ppr` — App Router, PPR, Turbopack, file conventions
3. `svelte-5-runes-sveltekit` — Svelte 5 runes + SvelteKit
4. `vue-3-composition-api-composables` — Vue 3.5 Composition API + Nuxt 3
5. `astro-islands-content-first` — Astro 5 Islands + Content Collections + Server Islands
6. `vite-vitest-modern-toolchain` — Vite 5/6 + Vitest 2 workflow
7. `typescript-5-advanced-patterns` — TS 5.5+ patterns, type-fest, ts-reset
8. `tanstack-query-router-store` — TanStack Query/Router/Store/Form
9. `zustand-jotai-state-management` — modern state libs decision tree
10. `tailwind-4-css-architecture` — Tailwind 4 + Panda + vanilla-extract decision
11. `shadcn-radix-headless-components` — shadcn/ui, Radix, react-aria primitives
12. `react-hook-form-zod-valibot-forms` — form patterns + validation
13. `accessibility-wcag-22-aa-axe-core` — a11y audit playbook
14. `core-web-vitals-lcp-inp-cls` — perf audit + LCP/INP/CLS fixes
15. `bundle-size-code-splitting-tree-shaking` — bundle optimization
16. `playwright-e2e-stability` — E2E test patterns + traces + fixtures
17. `storybook-chromatic-design-system` — component docs + visual regression CI
18. `biome-eslint-prettier-lint-format` — modern lint/format
19. `cloudflare-workers-edge-functions` — Workers/Pages/Hono/PartyKit
20. `i18n-next-intl-paraglide` — internationalization
21. `framer-motion-view-transitions-api` — animation patterns
22. `auth-clerk-authjs-lucia` — auth decision tree + Clerk/Auth.js/Lucia
23. `payments-stripe-elements-checkout` — Stripe Elements/Checkout/Connect

---

## Notes on remaining caveats (the ⚠ rows)

| Use case | Blocked by | Free fallback that ships immediately |
|---|---|---|
| Auth integration (Clerk) | Paid SaaS account | Auth.js v5 (OSS) + Lucia v3 (OSS) — fully documented in skill pack |
| Payments (Stripe) | Stripe API keys (production requires verified account) | Stripe test mode works with sandbox keys (free); other gateways (Paddle/Lemon Squeezy) covered as alternatives |
| Real-time (Ably/Liveblocks) | Managed SaaS keys | PartyKit (OSS on Cloudflare Workers) + Yjs (OSS CRDT) covered as primary path |

For each ⚠, the skill pack documents both the SaaS path and the OSS fallback so the agent can execute today regardless of recipient's account status.
