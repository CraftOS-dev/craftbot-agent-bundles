<!--
Source: https://svelte.dev/blog/svelte-5-is-alive · https://svelte.dev/docs/svelte/what-are-runes
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# Svelte 5 — Runes + SvelteKit

Svelte 5 (stable Oct 2024) replaces magic reactivity with explicit **runes** —
`$state`, `$derived`, `$effect`, `$props`, `$bindable`. The compiler is happier
about TypeScript, signals propagate finer-grained updates, and reactive logic
can live in `.svelte.ts` files outside components.

## When to use

- Greenfield Svelte project (always use 5 over 4 in 2026)
- Migrating a Svelte 4 codebase (run the official migrator)
- Wanting a tiny bundle + fastest hydration story for content + interactive
- Trigger phrases: "Svelte", "SvelteKit", "runes", "$state", "$derived",
  "$effect", "$props", "$bindable"

## Setup

```bash
# New SvelteKit project (Svelte 5 by default)
pnpm dlx sv create my-app
# choose: SvelteKit minimal, TypeScript, Vitest, Playwright, ESLint, Prettier

cd my-app
pnpm install
pnpm dev
```

Upgrade Svelte 4 → 5 in place:

```bash
pnpm dlx svelte-migrate@latest svelte-5
```

Verify: `pnpm exec svelte --version` → 5.x. Vite plugin: `@sveltejs/vite-plugin-svelte` 4.x.

No API keys required.

## Common recipes

### Recipe 1 — `$state` for reactive variables

```svelte
<!-- src/lib/Counter.svelte -->
<script lang="ts">
  let count = $state(0);
</script>

<button onclick={() => count++}>Clicks: {count}</button>
```

`let` alone is no longer reactive — you must mark it with `$state`.

### Recipe 2 — `$derived` replaces `$:` declarations

```svelte
<script lang="ts">
  let count = $state(0);
  let doubled = $derived(count * 2);
  let parity = $derived.by(() => {
    if (count % 2 === 0) return "even";
    return "odd";
  });
</script>

<p>{count} doubles to {doubled} ({parity})</p>
```

`$derived.by(fn)` is the longhand for complex derivations.

### Recipe 3 — `$effect` replaces `$:` blocks

```svelte
<script lang="ts">
  let query = $state("");

  $effect(() => {
    const t = setTimeout(() => console.log("search:", query), 300);
    return () => clearTimeout(t); // cleanup runs before next effect + on unmount
  });
</script>

<input bind:value={query} />
```

Use `$effect.pre()` to run before DOM updates and `$effect.root(() => ...)` to
detach an effect from its parent scope.

### Recipe 4 — `$props` replaces `export let`

```svelte
<!-- src/lib/Avatar.svelte -->
<script lang="ts">
  interface Props {
    src: string;
    alt: string;
    size?: number;
  }
  let { src, alt, size = 32 }: Props = $props();
</script>

<img {src} {alt} width={size} height={size} />
```

For "rest of the props" use `let { src, alt, ...rest }: Props = $props();`.

### Recipe 5 — `$bindable` for two-way bindings

```svelte
<!-- src/lib/TextInput.svelte -->
<script lang="ts">
  let { value = $bindable("") }: { value?: string } = $props();
</script>

<input bind:value />
```

Parent: `<TextInput bind:value={email} />` — value flows both directions.

### Recipe 6 — Share runes across files with `.svelte.ts`

```ts
// src/lib/cart.svelte.ts
export const cart = $state({
  items: [] as { id: string; qty: number }[],
});

export function addToCart(id: string) {
  cart.items.push({ id, qty: 1 });
}
```

```svelte
<script lang="ts">
  import { cart, addToCart } from "$lib/cart.svelte.ts";
</script>

<button onclick={() => addToCart("sku-1")}>Add ({cart.items.length})</button>
```

Reactive global state without a library.

### Recipe 7 — SvelteKit route files

```
src/routes/
  +layout.svelte          # shared layout (renders {@render children()} via $props)
  +layout.server.ts       # data loader for the layout (server only)
  +page.svelte            # /
  +page.ts                # universal loader (runs on server + client)
  +page.server.ts         # server-only loader (DB, secrets)
  blog/
    +page.svelte          # /blog
    [slug]/
      +page.svelte        # /blog/[slug]
      +page.server.ts     # load post by params.slug
  api/
    webhook/
      +server.ts          # GET/POST handlers
```

### Recipe 8 — `+page.server.ts` data loader

```ts
// src/routes/posts/[slug]/+page.server.ts
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ params, locals }) => {
  const post = await locals.db.post.findUnique({ where: { slug: params.slug } });
  if (!post) throw error(404, "Not found");
  return { post };
};
```

```svelte
<!-- +page.svelte -->
<script lang="ts">
  import type { PageProps } from "./$types";
  let { data }: PageProps = $props();
</script>

<article>
  <h1>{data.post.title}</h1>
  <div>{@html data.post.body}</div>
</article>
```

### Recipe 9 — Form Actions (SvelteKit's mutation primitive)

```ts
// src/routes/login/+page.server.ts
import { fail, redirect } from "@sveltejs/kit";
import type { Actions } from "./$types";

export const actions: Actions = {
  default: async ({ request, cookies }) => {
    const data = await request.formData();
    const email = String(data.get("email") ?? "");
    const password = String(data.get("password") ?? "");
    if (!email) return fail(400, { email, missing: true });
    const sessionId = await login(email, password);
    cookies.set("session", sessionId, { path: "/", httpOnly: true, secure: true });
    throw redirect(303, "/");
  },
};
```

```svelte
<script lang="ts">
  import { enhance } from "$app/forms";
  let { form } = $props();
</script>

<form method="POST" use:enhance>
  <input name="email" type="email" required />
  <input name="password" type="password" required />
  {#if form?.missing}<p class="error">Email required</p>{/if}
  <button type="submit">Log in</button>
</form>
```

`use:enhance` upgrades the form to a fetch-based submission with progressive
enhancement (works without JS).

### Recipe 10 — Snippets (replace slots)

```svelte
<!-- src/lib/Card.svelte -->
<script lang="ts">
  import type { Snippet } from "svelte";
  let { header, children }: { header?: Snippet; children: Snippet } = $props();
</script>

<section class="card">
  {#if header}<header>{@render header()}</header>{/if}
  <div>{@render children()}</div>
</section>
```

Parent:
```svelte
<Card>
  {#snippet header()}<h2>Title</h2>{/snippet}
  Body content here.
</Card>
```

Slots are deprecated; snippets are more powerful (parameterized, typed).

## Examples

### Example 1: Migrate a Svelte 4 store to runes

**Before (`src/lib/counter.ts`):**
```ts
import { writable, derived } from "svelte/store";
export const count = writable(0);
export const doubled = derived(count, $c => $c * 2);
```

**After (`src/lib/counter.svelte.ts`):**
```ts
export const state = $state({ count: 0 });
export const doubled = $derived(state.count * 2); // (use inside .svelte.ts at top level)
```

Migrator: `pnpm dlx svelte-migrate@latest svelte-5` handles most of this.

### Example 2: E2E test a SvelteKit form action

```ts
// tests/login.spec.ts
import { test, expect } from "@playwright/test";

test("login redirects to dashboard", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill("user@example.com");
  await page.getByLabel("Password").fill("hunter2");
  await page.getByRole("button", { name: "Log in" }).click();
  await expect(page).toHaveURL("/");
});
```

## Edge cases / gotchas

- **`$state` is not deep-reactive by default for primitives in objects** — for
  plain objects/arrays it IS deep-reactive via Proxy; for primitives wrap in
  `$state({ value: 0 })` if you need to pass a reference.
- **`$derived` must be synchronous** — for async derivations use `$effect` to
  set a `$state` variable.
- **`$effect` runs after the DOM updates** — `$effect.pre` runs before; use it
  when reading layout.
- **`$bindable` can be one-way** — the parent doesn't have to bind; default
  value applies.
- **`{@render children()}` is mandatory** — `<slot />` works but is deprecated.
- **SvelteKit `+page.ts` runs on both server and client** — `+page.server.ts`
  is server-only. Use server-only when you read secrets or hit a DB.
- **`enhance` requires `method="POST"`** — otherwise it falls back to native form
  submit.
- **Vite + Svelte 5 + Tailwind 4** — install both Vite plugins:
  `@sveltejs/vite-plugin-svelte` + `@tailwindcss/vite`. Order in
  `vite.config.ts` matters (Tailwind before Svelte).
- **Class binding syntax updated** — `class:active={isActive}` still works.
  String-form interpolation: `class={isActive ? "active" : ""}` is also valid.
- **`onMount`/`onDestroy` still exist** but `$effect` covers most cases.

## Sources

- [Svelte 5 release post](https://svelte.dev/blog/svelte-5-is-alive)
- [Runes documentation](https://svelte.dev/docs/svelte/what-are-runes) — concept + API
- [SvelteKit routing](https://svelte.dev/docs/kit/routing) — file conventions
- [SvelteKit form actions](https://svelte.dev/docs/kit/form-actions)
- [Snippets reference](https://svelte.dev/docs/svelte/snippet)
- [Svelte migration guide](https://svelte.dev/docs/svelte/v5-migration-guide)
- [Rich Harris — Svelte 5 talk (Svelte Summit Fall 2024)](https://www.youtube.com/@SvelteSociety)
