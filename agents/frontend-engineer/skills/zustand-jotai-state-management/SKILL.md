<!--
Source: https://zustand.docs.pmnd.rs/ · https://jotai.org/
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# Zustand + Jotai — Client UI state

For server state use TanStack Query / RSC. For **client UI state** the call is
between Zustand (store-shaped, ~3 kB, ideal for "the cart") and Jotai
(atom-shaped, fine-grained, ideal for "lots of small pieces"). This skill
documents both and gives a decision tree.

## When to use

- Cross-component client state that doesn't fit `useState` / Context
- Persisting state (cart, theme, user preferences) across reloads
- Splitting a large Redux store into a smaller, simpler tool
- Building a small reactive primitive without ceremony
- Trigger phrases: "Zustand", "Jotai", "atom", "global state", "client state",
  "no Redux", "lightweight store"

## Decision tree

| Shape | Pick |
|---|---|
| One "cart-like" object with actions | **Zustand** |
| Many independent values (atoms), often derived | **Jotai** |
| Need TypeScript inference of dispatch shape | **Zustand** |
| Need fine-grained subscriptions to a single atom | **Jotai** |
| Want to opt into Redux DevTools easily | **Zustand** (devtools middleware) |
| Need a tree of derived state (a la Recoil) | **Jotai** |
| Framework-agnostic / SSR-heavy | Zustand (slight edge) |

For everything else: **Zustand**.

## Setup

```bash
pnpm add zustand
pnpm add jotai
```

Verify: `pnpm list zustand jotai`.

No API keys.

## Common recipes — Zustand

### Recipe 1 — Basic store

```ts
// src/stores/cart.ts
import { create } from "zustand";

interface CartState {
  items: { id: string; qty: number }[];
  add: (id: string) => void;
  remove: (id: string) => void;
  clear: () => void;
}

export const useCart = create<CartState>((set) => ({
  items: [],
  add: (id) => set((s) => ({ items: [...s.items, { id, qty: 1 }] })),
  remove: (id) => set((s) => ({ items: s.items.filter(i => i.id !== id) })),
  clear: () => set({ items: [] }),
}));
```

```tsx
function CartButton() {
  const count = useCart((s) => s.items.length);
  const add = useCart((s) => s.add);
  return <button onClick={() => add("sku-1")}>Cart ({count})</button>;
}
```

The selector (`(s) => s.items.length`) means the component only re-renders when
`items.length` changes — not on every store update.

### Recipe 2 — Persist + devtools middleware

```ts
import { create } from "zustand";
import { devtools, persist, createJSONStorage } from "zustand/middleware";

export const useCart = create<CartState>()(
  devtools(
    persist(
      (set) => ({
        items: [],
        add: (id) => set((s) => ({ items: [...s.items, { id, qty: 1 }] })),
        remove: (id) => set((s) => ({ items: s.items.filter(i => i.id !== id) })),
        clear: () => set({ items: [] }),
      }),
      {
        name: "cart",                                   // localStorage key
        storage: createJSONStorage(() => localStorage),
        version: 1,
        migrate: (old: any, oldVersion) => {
          if (oldVersion === 0) return { items: old.items ?? [] };
          return old;
        },
      },
    ),
    { name: "Cart" },                                   // devtools instance name
  ),
);
```

### Recipe 3 — Immer middleware for nested updates

```bash
pnpm add immer
```

```ts
import { create } from "zustand";
import { immer } from "zustand/middleware/immer";

interface State {
  user: { name: string; prefs: { theme: "light" | "dark" } };
  setTheme: (t: "light" | "dark") => void;
}

export const useStore = create<State>()(
  immer((set) => ({
    user: { name: "", prefs: { theme: "light" } },
    setTheme: (t) => set((s) => { s.user.prefs.theme = t; }), // direct mutation
  })),
);
```

### Recipe 4 — Slicing pattern (organize a large store)

```ts
import { create, StateCreator } from "zustand";

interface AuthSlice {
  user: User | null;
  login: (u: User) => void;
  logout: () => void;
}

interface CartSlice {
  items: Item[];
  add: (i: Item) => void;
}

const createAuthSlice: StateCreator<AuthSlice & CartSlice, [], [], AuthSlice> = (set) => ({
  user: null,
  login: (user) => set({ user }),
  logout: () => set({ user: null, items: [] }),
});

const createCartSlice: StateCreator<AuthSlice & CartSlice, [], [], CartSlice> = (set) => ({
  items: [],
  add: (item) => set((s) => ({ items: [...s.items, item] })),
});

export const useStore = create<AuthSlice & CartSlice>()((...a) => ({
  ...createAuthSlice(...a),
  ...createCartSlice(...a),
}));
```

### Recipe 5 — Subscribe outside React

```ts
import { useCart } from "@/stores/cart";

// Subscribe in a non-component (analytics, side-effects)
const unsub = useCart.subscribe(
  (state) => state.items.length,
  (count) => analytics.track("cart_size", { count }),
  { equalityFn: Object.is },
);

// later: unsub();
```

### Recipe 6 — `useShallow` for object selectors

```ts
import { useShallow } from "zustand/react/shallow";

// Avoids re-render when other store fields change
const { name, theme } = useCart(useShallow((s) => ({ name: s.user.name, theme: s.user.theme })));
```

Without `useShallow`, returning an object literal would re-render on every store
update (new reference each time).

## Common recipes — Jotai

### Recipe 7 — Primitive atoms

```ts
// src/atoms.ts
import { atom } from "jotai";

export const countAtom = atom(0);
export const userAtom = atom<{ name: string } | null>(null);
```

```tsx
import { useAtom, useAtomValue, useSetAtom } from "jotai";
import { countAtom, userAtom } from "@/atoms";

function Counter() {
  const [count, setCount] = useAtom(countAtom);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}

// Read-only
function Label() {
  const count = useAtomValue(countAtom);
  return <span>{count}</span>;
}

// Set-only
function Resetter() {
  const setCount = useSetAtom(countAtom);
  return <button onClick={() => setCount(0)}>Reset</button>;
}
```

### Recipe 8 — Derived atoms

```ts
import { atom } from "jotai";

export const itemsAtom = atom<{ id: string; qty: number; price: number }[]>([]);

// Read-only derived atom
export const totalAtom = atom((get) => {
  const items = get(itemsAtom);
  return items.reduce((sum, i) => sum + i.qty * i.price, 0);
});

// Read-write derived atom
export const cartCountAtom = atom(
  (get) => get(itemsAtom).length,
  (_get, set, newItems: typeof itemsAtom["init"]) => set(itemsAtom, newItems),
);
```

Derived atoms recompute only when their dependencies change. Components only
re-render if the atom they subscribe to changes.

### Recipe 9 — Persist with atomWithStorage

```ts
import { atomWithStorage } from "jotai/utils";

export const themeAtom = atomWithStorage<"light" | "dark">("theme", "light");
```

`atomWithStorage` writes to localStorage by default; pass a custom storage for
sessionStorage or IndexedDB.

### Recipe 10 — Async atom (data fetching)

```ts
import { atom } from "jotai";

const userIdAtom = atom("u_1");

export const userAtom = atom(async (get) => {
  const id = get(userIdAtom);
  const res = await fetch(`/api/users/${id}`);
  return res.json() as Promise<{ name: string }>;
});
```

```tsx
import { Suspense } from "react";
import { useAtomValue } from "jotai";

function UserName() {
  const user = useAtomValue(userAtom); // suspends!
  return <span>{user.name}</span>;
}

// <Suspense fallback={...}><UserName /></Suspense>
```

For complex server state, prefer TanStack Query — Jotai async atoms are best
for lightweight, infrequent fetches tied to UI state.

### Recipe 11 — Atom families (parameterized atoms)

```ts
import { atomFamily } from "jotai/utils";

export const todoAtom = atomFamily((id: string) =>
  atom({ id, text: "", done: false }),
);

// Usage
const todo = useAtomValue(todoAtom("todo-1"));
```

## Examples

### Example 1: Migrate `useState` + Context → Zustand

**Before:**
```tsx
const ThemeContext = createContext<{theme: string; setTheme: (t: string) => void}>(...);
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState("light");
  return <ThemeContext.Provider value={{ theme, setTheme }}>{children}</ThemeContext.Provider>;
}
```

**After:**
```ts
// stores/theme.ts
export const useTheme = create<{ theme: string; set: (t: string) => void }>((set) => ({
  theme: "light",
  set: (theme) => set({ theme }),
}));
```
```tsx
// Anywhere in the tree, no Provider needed
const theme = useTheme((s) => s.theme);
```

### Example 2: Convert Redux Toolkit slice → Zustand

```ts
// before (RTK)
const cartSlice = createSlice({
  name: "cart",
  initialState: { items: [] },
  reducers: {
    add: (s, a) => { s.items.push(a.payload); },
    remove: (s, a) => { s.items = s.items.filter(i => i.id !== a.payload); },
  },
});

// after (Zustand + immer)
export const useCart = create<CartState>()(immer((set) => ({
  items: [],
  add: (item) => set((s) => { s.items.push(item); }),
  remove: (id) => set((s) => { s.items = s.items.filter(i => i.id !== id); }),
})));
```

## Edge cases / gotchas

- **Zustand selector returns a new reference → re-render every update**. Use
  `useShallow` for object/array selectors.
- **Persist middleware loads asynchronously** on web — for SSR-safe loading
  check `useStore.persist.hasHydrated()`.
- **Devtools middleware breaks immer Map/Set serialization** — pass
  `serialize: { options: { map: true } }` to devtools.
- **Don't put computed values in store state** — derive them in selectors.
- **Jotai re-renders are atom-scoped** — that's why it's fast, but you can't
  read multiple atoms in one selector unless via derived atom.
- **Jotai's `useAtom` returns `[value, setter]`** like `useState`. For setter
  only, use `useSetAtom` (skips subscription).
- **Async Jotai atoms** rely on Suspense — without `<Suspense>` they throw.
- **SSR + Jotai** needs `<Provider>` wrap or use `jotai-scope` for isolated
  stores per request.
- **Atom families** must be created outside render; recreating them re-derives
  every consumer.
- **`atomWithStorage` runs on first render** — for SSR, default to a static
  value and let it hydrate.

## Sources

- [Zustand docs](https://zustand.docs.pmnd.rs/)
- [Zustand middleware](https://zustand.docs.pmnd.rs/middlewares/persist)
- [Jotai docs](https://jotai.org/)
- [Jotai atom utilities](https://jotai.org/docs/utilities)
- [Jotai vs Zustand discussion](https://tkdodo.eu/blog/zustand-and-react-context) — TkDodo comparison
- [State of React State Management 2025](https://jscamp.dev/2025-state-management-survey) — recent survey
- [Daishi Kato — Jotai author talks](https://blog.axlight.com/)
