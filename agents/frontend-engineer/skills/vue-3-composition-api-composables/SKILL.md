<!--
Source: https://vuejs.org/ · https://blog.vuejs.org/posts/vue-3-5
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# Vue 3 — Composition API + Nuxt 3

Vue 3.5+ Composition API with `<script setup>` is the only style worth writing
in 2026. `defineModel` simplifies two-way bindings, props destructure preserves
reactivity (3.5+), and Nuxt 3 (Nitro under the hood) brings file-based routes
plus universal rendering.

## When to use

- New Vue projects — always 3.5+, never 2.x or Options API for new code
- Nuxt 3 apps (file-based routes, server routes, hybrid rendering)
- Migrating Options API → Composition API
- Building reusable composables (`useX`)
- Trigger phrases: "Vue", "Nuxt", "Composition API", "`<script setup>`",
  "ref", "reactive", "defineModel", "useFetch", "useAsyncData"

## Setup

```bash
# New Vue 3 SPA (Vite-based)
pnpm create vue@latest
# choose: TypeScript, Vue Router, Pinia, Vitest, Playwright, ESLint

# New Nuxt 3 app
pnpm dlx nuxi@latest init my-app
cd my-app
pnpm install
pnpm dev
```

Verify: `pnpm exec vue --version` → 3.5.x. Nuxt: `pnpm exec nuxi --version` → 3.x.

No API keys required.

## Common recipes

### Recipe 1 — `<script setup>` boilerplate

```vue
<script setup lang="ts">
import { ref, computed } from "vue";

const count = ref(0);
const doubled = computed(() => count.value * 2);

function increment() {
  count.value++;
}
</script>

<template>
  <button @click="increment">Clicks: {{ count }}</button>
  <p>Doubled: {{ doubled }}</p>
</template>
```

`ref().value` is required in JS; templates auto-unwrap.

### Recipe 2 — `reactive` for objects, `ref` for primitives

```ts
import { ref, reactive } from "vue";

const counter = ref(0);                                // primitive
const user = reactive({ name: "Ada", age: 30 });       // object
const items = ref<string[]>([]);                       // generic
```

Prefer `ref` everywhere if unsure — it composes more cleanly with destructuring
(via `toRefs`).

### Recipe 3 — `defineModel` (two-way binding, 3.4+ stable)

```vue
<!-- TextInput.vue -->
<script setup lang="ts">
const model = defineModel<string>({ required: true });
</script>

<template>
  <input v-model="model" />
</template>
```

Parent: `<TextInput v-model="email" />` — no manual emit/prop boilerplate.

### Recipe 4 — Props destructure with reactivity (3.5+)

```vue
<script setup lang="ts">
interface Props {
  name: string;
  age?: number;
}

// In 3.5+ this preserves reactivity (was previously lost on destructure).
const { name, age = 18 } = defineProps<Props>();
</script>

<template>
  <p>{{ name }} ({{ age }})</p>
</template>
```

### Recipe 5 — Composable (`useX`)

```ts
// composables/useMouse.ts
import { ref, onMounted, onUnmounted } from "vue";

export function useMouse() {
  const x = ref(0);
  const y = ref(0);
  function update(e: MouseEvent) {
    x.value = e.pageX;
    y.value = e.pageY;
  }
  onMounted(() => window.addEventListener("mousemove", update));
  onUnmounted(() => window.removeEventListener("mousemove", update));
  return { x, y };
}
```

```vue
<script setup lang="ts">
import { useMouse } from "@/composables/useMouse";
const { x, y } = useMouse();
</script>

<template>Mouse is at {{ x }}, {{ y }}</template>
```

### Recipe 6 — `watch` and `watchEffect`

```ts
import { ref, watch, watchEffect } from "vue";

const query = ref("");

// explicit watch — fires when `query` changes
watch(query, async (newQ, oldQ) => {
  const res = await fetch(`/api/search?q=${newQ}`);
  // ...
}, { debounce: 300 } as any);

// reactive auto-tracking
watchEffect(async () => {
  if (!query.value) return;
  const res = await fetch(`/api/search?q=${query.value}`);
  // ...
});
```

### Recipe 7 — Suspense + async setup

```vue
<!-- AsyncProfile.vue -->
<script setup lang="ts">
const user = await fetch("/api/me").then(r => r.json());
</script>

<template>
  <article><h1>{{ user.name }}</h1></article>
</template>
```

```vue
<!-- parent -->
<template>
  <Suspense>
    <AsyncProfile />
    <template #fallback>Loading...</template>
  </Suspense>
</template>
```

### Recipe 8 — Pinia store (modern Vuex replacement)

```ts
// stores/cart.ts
import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useCart = defineStore("cart", () => {
  const items = ref<{ id: string; qty: number }[]>([]);
  const total = computed(() => items.value.reduce((sum, i) => sum + i.qty, 0));

  function add(id: string) {
    items.value.push({ id, qty: 1 });
  }
  function clear() { items.value = []; }

  return { items, total, add, clear };
});
```

```vue
<script setup lang="ts">
import { useCart } from "@/stores/cart";
const cart = useCart();
</script>

<template>
  <button @click="cart.add('sku-1')">Add ({{ cart.total }})</button>
</template>
```

### Recipe 9 — Nuxt 3 `useFetch` (typed, SSR-safe)

```vue
<!-- pages/posts/[slug].vue -->
<script setup lang="ts">
const route = useRoute();
const { data: post, pending, error } = await useFetch(`/api/posts/${route.params.slug}`);
</script>

<template>
  <article v-if="post">
    <h1>{{ post.title }}</h1>
    <div v-html="post.body" />
  </article>
  <p v-else-if="pending">Loading...</p>
  <p v-else-if="error">Failed: {{ error.message }}</p>
</template>
```

### Recipe 10 — Nuxt 3 server route

```ts
// server/api/posts/[slug].get.ts
export default defineEventHandler(async (event) => {
  const slug = getRouterParam(event, "slug");
  const post = await usePrisma().post.findUnique({ where: { slug } });
  if (!post) throw createError({ statusCode: 404, statusMessage: "Not found" });
  return post;
});
```

### Recipe 11 — File-based routing (Nuxt)

```
pages/
  index.vue            # /
  about.vue            # /about
  blog/
    index.vue          # /blog
    [slug].vue         # /blog/[slug]
  [...catch].vue       # 404 catch-all
```

For SPA without Nuxt, install `unplugin-vue-router` to get the same convention
on Vite.

## Examples

### Example 1: Convert Options API to `<script setup>`

**Before:**
```vue
<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({
  props: { id: String },
  data() { return { count: 0 }; },
  computed: { doubled() { return this.count * 2; } },
  methods: { inc() { this.count++; } },
});
</script>
```

**After:**
```vue
<script setup lang="ts">
import { ref, computed } from "vue";
const { id } = defineProps<{ id: string }>();
const count = ref(0);
const doubled = computed(() => count.value * 2);
const inc = () => count.value++;
</script>
```

### Example 2: Lazy-load a heavy component

```vue
<script setup lang="ts">
import { defineAsyncComponent } from "vue";
const HeavyChart = defineAsyncComponent(() => import("@/components/HeavyChart.vue"));
</script>

<template>
  <Suspense>
    <HeavyChart />
    <template #fallback><div class="chart-skeleton" /></template>
  </Suspense>
</template>
```

## Edge cases / gotchas

- **`ref().value` is mandatory in JS** — forgetting `.value` is the #1 Vue bug.
- **`reactive` loses reactivity on destructure** — use `toRefs` or `storeToRefs`
  (Pinia) to preserve it.
- **`defineProps` / `defineEmits` / `defineModel` are macros** — they only work
  inside `<script setup>`, never imported.
- **`v-model` arg names** — `v-model:modelValue` is default; for named models,
  `defineModel("query")` and `v-model:query="..."`.
- **Nuxt `useFetch` vs `useAsyncData`** — `useFetch` wraps `$fetch`;
  `useAsyncData` is for arbitrary async work. Both dedupe on key.
- **`v-html` is unsanitized** — sanitize user-provided HTML with DOMPurify before
  binding.
- **SSR + composables** — only call composables inside `setup` or other
  composables; calling them in event handlers loses the active instance.
- **Vue 3.4 added `defineModel` as stable** — earlier you needed
  `experimentalDefineModel: true`. Remove that flag in 3.5+.
- **Pinia stores returned from `defineStore`** are factories — call them
  (`useCart()`) inside `setup` every time.
- **Vapor mode** (no virtual DOM) is in alpha — pick when stable. For now use
  default mode.

## Sources

- [Vue 3 docs](https://vuejs.org/guide/introduction.html)
- [Vue 3.5 release notes](https://blog.vuejs.org/posts/vue-3-5)
- [`<script setup>` reference](https://vuejs.org/api/sfc-script-setup.html)
- [`defineModel` reference](https://vuejs.org/api/sfc-script-setup.html#definemodel)
- [Composables guide](https://vuejs.org/guide/reusability/composables.html)
- [Nuxt 3 docs](https://nuxt.com/docs)
- [Pinia docs](https://pinia.vuejs.org/)
- [Evan You — State of Vue 2025](https://blog.vuejs.org/) — quarterly recap posts
