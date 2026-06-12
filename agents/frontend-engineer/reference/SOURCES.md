# Frontend Engineer — Sources

This file maps every section of `soul.md` and `role.md` back to the research source it was derived from. It ships in the bundle but is **not** loaded into the agent's context — it exists for human verification and future updates.

Raw research lives at `reference/SOTA_USE_CASES.md` (per-use-case SOTA mapping with URLs). Full per-source citations are in `agent.yaml → sources` and below.

---

## soul.md → source map

| Section in soul.md | Source(s) | Notes |
|---|---|---|
| Opening identity + three convictions | Authored from the synthesis | Convictions ("network is bottleneck", "a11y is engineering", "component contracts beat speculative reuse") are operational glue, not domain claims. |
| Purpose | `reference/SOTA_USE_CASES.md` (verdict + caveats) | Quality bar (Core Web Vitals + WCAG 2.2 AA + typed end-to-end) sourced from web.dev/vitals + WCAG 2.2 spec. |
| Execution stack | `reference/SOTA_USE_CASES.md` (recommended agent.yaml additions, skill packs section) | Decision rule line authored from synthesis. |
| When invoked — Build mode | Authored from the synthesis | Informed by Next 15 docs (nextjs.org) + React 19 docs (react.dev). |
| When invoked — Review mode | Authored from the synthesis | Priority order informed by Lighthouse + axe-core + Web Vitals authoritative defaults. |
| When invoked — Debug mode | Authored from the synthesis | Hypothesis-first pattern adapted from `senior-python-engineer` soul.md (sibling agent). |
| When invoked — Audit / CWV / Migrate / Deploy modes | `reference/SOTA_USE_CASES.md` (use cases 14, 15, 27-29, 37) | |
| Core operating rules | Authored from synthesis + WCAG 2.2 spec + Next 15 docs + Tailwind 4 docs + Vite docs | Each rule traces to one of the SOTA approach rows in `SOTA_USE_CASES.md`. |
| Mode-specific decisions | Authored from synthesis | Reinforces the When invoked entries with per-mode quality bars. |
| Code review — flag priority | https://web.dev/articles/vitals + https://www.w3.org/TR/WCAG22/ + https://tanstack.com/query/v5 + Stripe docs (security pass) | Order: security → a11y → perf → types → data races → UX → contracts → style. |
| Core Web Vitals — priority by failing vital | https://web.dev/articles/vitals · https://web.dev/articles/inp · https://web.dev/articles/cls | LCP < 2.5s, INP < 200ms, CLS < 0.1 thresholds direct from web.dev. |
| Antipatterns to flag on sight | Synthesis from sources cited in role.md's Antipattern catalog | Each item maps to a BAD/GOOD pair in role.md. |
| Quality gates | Authored from synthesis | TypeScript strict + Biome + Vitest + axe-core + size-limit + Lighthouse CI + Chromatic + Storybook. |
| Output format | Authored from synthesis | Matches v0 sibling agents (senior-python-engineer, technical-writer). |
| Communication style | Authored from synthesis | Matches v0 sibling agents' tone. |
| When to push back / defer | `agent.yaml` sibling agents + WCAG 2.2 + TypeScript handbook | Hand-offs to `senior-python-engineer`, `devops-engineer`, `product-manager`, `technical-writer`. |
| PROACTIVE self-init footer | `METHODOLOGY.md` standard footer | Same wording across all CraftBot agents. The 3 questions (framework, CSS, deploy target) are role-specific. |
| Closing rule | Authored from synthesis | Restates the three convictions from the intro. |

---

## role.md → source map

| Section in role.md | Source(s) | Notes |
|---|---|---|
| Capability reference — Supported frameworks | https://react.dev · https://nextjs.org/docs · https://svelte.dev/docs · https://vuejs.org · https://docs.astro.build · https://tanstack.com/start · https://qwik.dev · https://www.solidjs.com · https://reactrouter.com | Each framework's official docs at the version listed. |
| Capability reference — Build tooling | https://vitejs.dev · https://vitest.dev · https://nextjs.org/docs/app/api-reference/turbopack · https://rspack.dev · https://bun.sh · https://esbuild.github.io · https://swc.rs | |
| Capability reference — TypeScript ecosystem | https://www.typescriptlang.org · https://github.com/sindresorhus/type-fest · https://github.com/total-typescript/ts-reset · https://zod.dev · https://valibot.dev · https://arktype.io | |
| Capability reference — CSS / styling | https://tailwindcss.com · https://panda-css.com · https://vanilla-extract.style · https://unocss.dev · https://open-props.style · https://ui.shadcn.com · https://www.radix-ui.com · https://headlessui.com · https://ark-ui.com · https://react-spectrum.adobe.com/react-aria | |
| Capability reference — State management | https://tanstack.com/query/v5 · https://zustand.docs.pmnd.rs · https://jotai.org · https://valtio.pmnd.rs · https://nanostores.dev · https://redux-toolkit.js.org | |
| Capability reference — Animation, Forms, Testing, Perf, i18n, Edge, CMS, Auth, Payments | Authoritative docs per tool — see `reference/SOTA_USE_CASES.md` URLs | One row per tool in the SOTA mapping. |
| Code review playbook | Authored from the synthesis | Informed by Lighthouse + axe-core + TypeScript handbook + Web Vitals. |
| Accessibility audit playbook (WCAG 2.2 AA) | https://www.w3.org/TR/WCAG22/ · https://www.deque.com/axe/ · https://pa11y.org/ · https://github.com/GoogleChrome/lighthouse-ci · https://react-spectrum.adobe.com/react-aria | |
| Core Web Vitals playbook | https://web.dev/articles/vitals · https://web.dev/articles/inp · https://github.com/GoogleChrome/web-vitals · https://github.com/GoogleChrome/lighthouse-ci | |
| Performance investigation playbook | Synthesis from web.dev + React docs + bundle-analyzer + Knip docs | |
| Migration procedures — Webpack → Vite | https://vitejs.dev/guide/migration | |
| Migration procedures — CRA → Next 15 | https://react.dev/blog/2025/02/14/sunsetting-create-react-app · https://nextjs.org/docs/app/building-your-application/upgrading/from-create-react-app | |
| Migration procedures — React 18 → 19 | https://react.dev/blog/2024/04/25/react-19-upgrade-guide | |
| Migration procedures — ESLint+Prettier → Biome | https://biomejs.dev/guides/migrate-eslint-prettier/ | |
| Migration procedures — Pages → App Router | https://nextjs.org/docs/app/building-your-application/upgrading/app-router-migration | |
| Antipattern catalog (12 BAD/GOOD pairs) | Synthesis from React docs, TanStack Query docs, WCAG 2.2 spec, web.dev INP guide, Next 15 docs | Each pair is operational glue connecting an antipattern to the canonical 2026 fix. |
| Reference patterns — Server Action + form state | https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations · https://react.dev/reference/react/useActionState | |
| Reference patterns — TanStack Query optimistic mutation | https://tanstack.com/query/v5/docs/framework/react/guides/optimistic-updates | |
| Reference patterns — Svelte 5 runes | https://svelte.dev/docs/svelte/what-are-runes | |
| Reference patterns — Vue 3.5 + defineModel | https://blog.vuejs.org/posts/vue-3-5 | |
| Reference patterns — Astro Island | https://docs.astro.build/en/concepts/islands/ | |
| Reference patterns — Zustand store | https://zustand.docs.pmnd.rs/guides/typescript | |
| Reference patterns — Playwright spec + a11y | https://playwright.dev/docs/accessibility-testing | |
| Reference patterns — Cloudflare Worker with Hono | https://hono.dev/docs/getting-started/cloudflare-workers | |
| SOTA tool reference (32 tools) | `reference/SOTA_USE_CASES.md` + per-tool authoritative docs | One H3 per tool; URL at the bottom of each subsection. |
| SOTA execution playbook (mapping table) | `reference/SOTA_USE_CASES.md` (skill-pack assignments) | |
| Closing rules | Mirrors soul.md's three convictions | |

---

## SOTA tool sources (June 2026)

> One row per SOTA tool referenced in the agent. Skill pack column names the bundled skill that deep-dives the tool (Round 2 creates the SKILL.md contents).

### React + meta-frameworks

| Tool | Source URL | Skill pack |
|---|---|---|
| React 19 | https://react.dev/blog/2024/12/05/react-19 · https://react.dev/reference/react | `react-19-server-components-actions` |
| Next.js 15 | https://nextjs.org/blog/next-15 · https://nextjs.org/docs · https://nextjs.org/docs/app/getting-started/partial-prerendering | `next-15-app-router-ppr` |
| TanStack Start | https://tanstack.com/start/latest | `tanstack-query-router-store` |
| React Router 7 | https://reactrouter.com/start/framework/installation | `tanstack-query-router-store` |
| Remotion (programmatic video) | https://www.remotion.dev/ | default skill `remotion-best-practices` + `remotion-video-toolkit` |

### Svelte + Vue + Astro

| Tool | Source URL | Skill pack |
|---|---|---|
| Svelte 5 (runes) | https://svelte.dev/blog/svelte-5-is-alive · https://svelte.dev/docs/svelte/what-are-runes | `svelte-5-runes-sveltekit` |
| SvelteKit | https://svelte.dev/docs/kit/introduction · https://kit.svelte.dev/ | `svelte-5-runes-sveltekit` |
| Vue 3.5 | https://blog.vuejs.org/posts/vue-3-5 · https://vuejs.org/ | `vue-3-composition-api-composables` |
| Nuxt 3 | https://nuxt.com/docs · https://nitro.unjs.io/ | `vue-3-composition-api-composables` |
| Astro 5 | https://astro.build/blog/astro-5/ · https://docs.astro.build · https://docs.astro.build/en/concepts/islands/ | `astro-islands-content-first` |
| Solid / SolidStart | https://www.solidjs.com/ · https://start.solidjs.com/ | role.md SOTA section |
| Qwik / Qwik City | https://qwik.dev/ | role.md SOTA section |

### Build / test toolchain

| Tool | Source URL | Skill pack |
|---|---|---|
| Vite 5/6 | https://vitejs.dev/ · https://vitejs.dev/guide/migration | `vite-vitest-modern-toolchain` |
| Vitest 2 | https://vitest.dev/ | `vite-vitest-modern-toolchain` |
| Turbopack | https://nextjs.org/docs/app/api-reference/turbopack | `next-15-app-router-ppr` |
| Rspack | https://rspack.dev/ | `vite-vitest-modern-toolchain` |
| Bun | https://bun.sh/ · https://bun.sh/docs | role.md SOTA section |
| esbuild | https://esbuild.github.io/ | role.md SOTA section |
| swc | https://swc.rs/ | role.md SOTA section |
| tsx | https://github.com/privatenumber/tsx | role.md SOTA section |
| Playwright 1.50+ | https://playwright.dev/ · https://playwright.dev/docs/best-practices · https://playwright.dev/docs/trace-viewer | `playwright-e2e-stability` |
| MSW 2 | https://mswjs.io/ | `vite-vitest-modern-toolchain` |
| Storybook 8 | https://storybook.js.org/ · https://storybook.js.org/blog/storybook-8/ | `storybook-chromatic-design-system` |
| Chromatic | https://www.chromatic.com/docs/ | `storybook-chromatic-design-system` |
| Percy | https://percy.io/ | `storybook-chromatic-design-system` |
| Lost-pixel | https://lost-pixel.com/ | `storybook-chromatic-design-system` |
| Testing Library | https://testing-library.com/ | `vite-vitest-modern-toolchain` |

### TypeScript

| Tool | Source URL | Skill pack |
|---|---|---|
| TypeScript 5.5 | https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-5.html | `typescript-5-advanced-patterns` |
| type-fest | https://github.com/sindresorhus/type-fest | `typescript-5-advanced-patterns` |
| ts-reset | https://github.com/total-typescript/ts-reset | `typescript-5-advanced-patterns` |
| zod | https://zod.dev/ | `react-hook-form-zod-valibot-forms` |
| valibot | https://valibot.dev/ | `react-hook-form-zod-valibot-forms` |
| arktype | https://arktype.io/ | `typescript-5-advanced-patterns` |

### State + data

| Tool | Source URL | Skill pack |
|---|---|---|
| TanStack Query 5 | https://tanstack.com/query/v5 | `tanstack-query-router-store` |
| TanStack Router 1 | https://tanstack.com/router/latest | `tanstack-query-router-store` |
| TanStack Form | https://tanstack.com/form/latest | `react-hook-form-zod-valibot-forms` |
| Zustand | https://zustand.docs.pmnd.rs/ | `zustand-jotai-state-management` |
| Jotai | https://jotai.org/ | `zustand-jotai-state-management` |
| nanostores | https://github.com/nanostores/nanostores | `zustand-jotai-state-management` |
| tRPC v11 | https://trpc.io/ | `tanstack-query-router-store` |
| urql | https://commerce.nearform.com/open-source/urql/ | role.md SOTA section |
| Apollo Client | https://www.apollographql.com/docs/react/ | role.md SOTA section |

### CSS / styling

| Tool | Source URL | Skill pack |
|---|---|---|
| Tailwind CSS 4 | https://tailwindcss.com/blog/tailwindcss-v4 · https://tailwindcss.com/docs | `tailwind-4-css-architecture` |
| Panda CSS | https://panda-css.com/ | `tailwind-4-css-architecture` |
| vanilla-extract | https://vanilla-extract.style/ | `tailwind-4-css-architecture` |
| UnoCSS | https://unocss.dev/ | `tailwind-4-css-architecture` |
| shadcn/ui | https://ui.shadcn.com/ | `shadcn-radix-headless-components` |
| Radix UI | https://www.radix-ui.com/ | `shadcn-radix-headless-components` |
| Headless UI | https://headlessui.com/ | `shadcn-radix-headless-components` |
| Ark UI | https://ark-ui.com/ | `shadcn-radix-headless-components` |
| react-aria | https://react-spectrum.adobe.com/react-aria/ | `shadcn-radix-headless-components` |
| Stylelint | https://stylelint.io/ | `biome-eslint-prettier-lint-format` |

### Forms

| Tool | Source URL | Skill pack |
|---|---|---|
| React Hook Form | https://react-hook-form.com/ | `react-hook-form-zod-valibot-forms` |
| Conform | https://conform.guide/ | `react-hook-form-zod-valibot-forms` |
| VeeValidate | https://vee-validate.logaretm.com/v4/ | `react-hook-form-zod-valibot-forms` |
| Felte | https://felte.dev/ | `react-hook-form-zod-valibot-forms` |

### Animation

| Tool | Source URL | Skill pack |
|---|---|---|
| motion (Framer rebrand) | https://motion.dev/ | `framer-motion-view-transitions-api` |
| Motion One | https://motion.dev/docs/motion-one | `framer-motion-view-transitions-api` |
| GSAP | https://gsap.com/ | `framer-motion-view-transitions-api` |
| AutoAnimate | https://auto-animate.formkit.com/ | `framer-motion-view-transitions-api` |
| View Transitions API | https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API | `framer-motion-view-transitions-api` |

### Performance + accessibility + quality

| Tool | Source URL | Skill pack |
|---|---|---|
| Web Vitals (LCP/INP/CLS) | https://web.dev/articles/vitals · https://web.dev/articles/inp · https://web.dev/articles/cls | `core-web-vitals-lcp-inp-cls` |
| web-vitals library | https://github.com/GoogleChrome/web-vitals | `core-web-vitals-lcp-inp-cls` |
| Lighthouse CI | https://github.com/GoogleChrome/lighthouse-ci | `core-web-vitals-lcp-inp-cls` |
| Million.js | https://million.dev/ | `core-web-vitals-lcp-inp-cls` |
| PageSpeed Insights API | https://developers.google.com/speed/docs/insights/v5/get-started | `core-web-vitals-lcp-inp-cls` |
| axe-core | https://www.deque.com/axe/ | `accessibility-wcag-22-aa-axe-core` |
| pa11y / pa11y-ci | https://pa11y.org/ | `accessibility-wcag-22-aa-axe-core` |
| eslint-plugin-jsx-a11y | https://github.com/jsx-eslint/eslint-plugin-jsx-a11y | `accessibility-wcag-22-aa-axe-core` |
| WCAG 2.2 | https://www.w3.org/TR/WCAG22/ | `accessibility-wcag-22-aa-axe-core` |
| size-limit | https://github.com/ai/size-limit | `bundle-size-code-splitting-tree-shaking` |
| Knip | https://knip.dev/ | `bundle-size-code-splitting-tree-shaking` |
| @next/bundle-analyzer | https://www.npmjs.com/package/@next/bundle-analyzer | `bundle-size-code-splitting-tree-shaking` |
| es-toolkit (lodash alt) | https://es-toolkit.slash.page/ | `bundle-size-code-splitting-tree-shaking` |
| Biome | https://biomejs.dev/ | `biome-eslint-prettier-lint-format` |
| Oxlint | https://oxc.rs/ | `biome-eslint-prettier-lint-format` |
| ESLint 9 | https://eslint.org/ | `biome-eslint-prettier-lint-format` |
| Prettier 3 | https://prettier.io/ | `biome-eslint-prettier-lint-format` |

### Edge + runtime + real-time

| Tool | Source URL | Skill pack |
|---|---|---|
| Cloudflare Workers | https://developers.cloudflare.com/workers/ | `cloudflare-workers-edge-functions` |
| Cloudflare Pages | https://developers.cloudflare.com/pages/ | `cloudflare-workers-edge-functions` |
| Wrangler | https://developers.cloudflare.com/workers/wrangler/ | `cloudflare-workers-edge-functions` |
| Vercel Edge Runtime | https://vercel.com/docs/functions/edge-functions | `cloudflare-workers-edge-functions` |
| Hono | https://hono.dev/ | `cloudflare-workers-edge-functions` |
| Elysia | https://elysiajs.com/ | `cloudflare-workers-edge-functions` |
| Deno Deploy | https://deno.com/deploy | role.md SOTA section |
| PartyKit | https://docs.partykit.io/ | `cloudflare-workers-edge-functions` |
| Yjs (CRDT) | https://yjs.dev/ | `cloudflare-workers-edge-functions` |
| Liveblocks | https://liveblocks.io/ | `cloudflare-workers-edge-functions` |
| Ably / Pusher | https://ably.com/ · https://pusher.com/ | `cloudflare-workers-edge-functions` |

### i18n

| Tool | Source URL | Skill pack |
|---|---|---|
| next-intl | https://next-intl-docs.vercel.app/ | `i18n-next-intl-paraglide` |
| Paraglide JS | https://inlang.com/m/gerre34r/library-inlang-paraglideJs | `i18n-next-intl-paraglide` |
| Lingui | https://lingui.dev/ | `i18n-next-intl-paraglide` |
| react-intl (FormatJS) | https://formatjs.io/ | `i18n-next-intl-paraglide` |
| @astrojs/i18n | https://docs.astro.build/en/recipes/i18n/ | `i18n-next-intl-paraglide` |

### Auth

| Tool | Source URL | Skill pack |
|---|---|---|
| Clerk | https://clerk.com/docs | `auth-clerk-authjs-lucia` |
| Auth.js v5 (NextAuth) | https://authjs.dev/ | `auth-clerk-authjs-lucia` |
| Lucia v3 | https://lucia-auth.com/ | `auth-clerk-authjs-lucia` |
| WorkOS | https://workos.com/docs | `auth-clerk-authjs-lucia` |
| Supabase Auth | https://supabase.com/docs/guides/auth | `auth-clerk-authjs-lucia` |
| iron-session | https://github.com/vvo/iron-session | `auth-clerk-authjs-lucia` |

### Payments

| Tool | Source URL | Skill pack |
|---|---|---|
| Stripe Checkout | https://docs.stripe.com/payments/checkout | `payments-stripe-elements-checkout` |
| Stripe Elements + Payment Intents | https://docs.stripe.com/payments/payment-element | `payments-stripe-elements-checkout` |
| Stripe Connect | https://stripe.com/connect | `payments-stripe-elements-checkout` |
| Paddle | https://www.paddle.com/ | `payments-stripe-elements-checkout` |
| Lemon Squeezy | https://www.lemonsqueezy.com/ | `payments-stripe-elements-checkout` |

### CMS

| Tool | Source URL | Skill pack |
|---|---|---|
| Payload CMS 3 | https://payloadcms.com/ | role.md SOTA section |
| Sanity | https://www.sanity.io/docs | role.md SOTA section |
| Contentful | https://www.contentful.com/developers/docs/ | role.md SOTA section |
| Strapi | https://strapi.io/ | role.md SOTA section |
| Builder.io | https://www.builder.io/ | role.md SOTA section |
| DatoCMS | https://www.datocms.com/ | role.md SOTA section |
| Shopify Hydrogen | https://hydrogen.shopify.dev/ | role.md SOTA section |

### Deployment

| Tool | Source URL | Skill pack |
|---|---|---|
| Vercel CLI | https://vercel.com/docs/cli | uses default skill `vercel-cli-with-tokens` + `deploy-to-vercel` |
| netlify-cli | https://docs.netlify.com/cli/get-started/ | role.md SOTA section |
| SST (Serverless Stack) | https://sst.dev/ | role.md SOTA section |
| Docker (Node 22 LTS / Bun 1.x) | https://hub.docker.com/_/node · https://bun.sh/guides/ecosystem/docker | role.md SOTA section |

---

## Skill pack inventory (bundled — Round 2 creates SKILL.md contents)

| Skill pack | Tools covered |
|---|---|
| `react-19-server-components-actions` | React 19, RSC, Server Actions, `use()`, `useActionState`, `useOptimistic` |
| `next-15-app-router-ppr` | Next 15, App Router, PPR, Turbopack, async APIs, middleware |
| `svelte-5-runes-sveltekit` | Svelte 5 runes, SvelteKit routing/hooks |
| `vue-3-composition-api-composables` | Vue 3.5, Composition API, defineModel, Nuxt 3 |
| `astro-islands-content-first` | Astro 5, Islands, Content Collections v2, Server Islands |
| `vite-vitest-modern-toolchain` | Vite 5/6, Vitest 2, MSW, Testing Library |
| `typescript-5-advanced-patterns` | TS 5.5+, satisfies, const generics, type-fest, ts-reset |
| `tanstack-query-router-store` | TanStack Query/Router/Form/Store + tRPC v11 |
| `zustand-jotai-state-management` | Zustand, Jotai, nanostores, valtio |
| `tailwind-4-css-architecture` | Tailwind 4 + Panda + vanilla-extract + UnoCSS decision |
| `shadcn-radix-headless-components` | shadcn/ui, Radix, Ark UI, react-aria, Headless UI |
| `react-hook-form-zod-valibot-forms` | React Hook Form, Conform, zod, valibot, arktype |
| `accessibility-wcag-22-aa-axe-core` | axe-core, pa11y, Lighthouse a11y, react-aria, WCAG 2.2 |
| `core-web-vitals-lcp-inp-cls` | web-vitals 4, Lighthouse CI, Million.js, PSI API |
| `bundle-size-code-splitting-tree-shaking` | size-limit, Knip, bundle-analyzer, es-toolkit |
| `playwright-e2e-stability` | Playwright 1.50+, traces, fixtures, sharding, codegen |
| `storybook-chromatic-design-system` | Storybook 8, Chromatic, Percy, Lost-pixel, CSF 3 |
| `biome-eslint-prettier-lint-format` | Biome, Oxlint, ESLint 9 flat, Prettier 3, Stylelint |
| `cloudflare-workers-edge-functions` | Workers, Pages, Wrangler, Hono, PartyKit, Yjs |
| `i18n-next-intl-paraglide` | next-intl, Paraglide JS, Lingui, react-intl, ICU |
| `framer-motion-view-transitions-api` | motion (Framer), Motion One, View Transitions, GSAP |
| `auth-clerk-authjs-lucia` | Clerk, Auth.js v5, Lucia v3, WorkOS, Supabase Auth |
| `payments-stripe-elements-checkout` | Stripe Elements/Checkout/Connect, Paddle, Lemon Squeezy |

---

## Notes on authored-from-synthesis

A handful of sections were composed locally rather than lifted from a single source. They are listed below; each is short and operational (not a domain claim):

- **soul.md opening identity** — three convictions phrased to be load-bearing decision drivers.
- **soul.md When invoked Build/Review/Debug modes** — sequenced from sibling agent `senior-python-engineer` soul.md (same shape, frontend-specific steps).
- **soul.md Core operating rules** — each rule cites a specific authoritative source in the table above, but the phrasing is synthesized for token discipline.
- **role.md Code review playbook** — synthesizes order-of-priority from Lighthouse + axe-core + Web Vitals + TypeScript handbook into one walkthrough.
- **role.md Antipattern catalog (12 pairs)** — operational glue connecting an antipattern to the canonical 2026 fix; each pair cites the source via the URL in the BAD/GOOD reasoning.
- **PROACTIVE self-init footer** — CraftBot-wide design decision documented in `METHODOLOGY.md`. The 3 questions are role-specific (framework, CSS, deploy target).

---

## How to update this agent

1. Re-check the SOTA URLs in `reference/SOTA_USE_CASES.md` — most are major-version-stable, but Tailwind/Next/Svelte/Vue have major releases ~yearly.
2. Update the relevant skill packs in `agents/frontend-engineer/skills/<name>/SKILL.md` (Round 2 creates these).
3. Update this `SOURCES.md` if a new tool earns a row or an old one drops out.
4. Re-run `python verify.py frontend-engineer` to confirm structure intact.
5. Re-build: `python build.py frontend-engineer` produces a fresh `.craftbot`.

For the canonical reference repos (Step 2 of the methodology — future tightening):
- `wshobson/agents` — pull `plugins/frontend-development/` quarterly.
- `VoltAgent/awesome-claude-code-subagents` — pull `categories/01-core-development/frontend-developer.md` and `categories/02-language-specialists/` quarterly.
- `msitarzewski/agency-agents` — pull engineering folder quarterly.
- `vijaythecoder/awesome-claude-agents` — pull framework specialists (Vue, Next, etc.).
