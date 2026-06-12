<!--
Source: https://tanstack.com/query/v5 · https://tanstack.com/router/latest
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# TanStack — Query, Router, Store, Form

TanStack Query 5 is the standard for server state in React/Vue/Svelte/Solid.
TanStack Router 1 is the type-safe file-based router for SPAs (alternative to
Next App Router when you don't need SSR). Store is a tiny reactive primitive;
Form is the framework-agnostic form library.

## When to use

- **Query**: server data needs caching, retry, revalidation, optimistic UI,
  background refresh
- **Router**: SPA needs type-safe params, search params, code/file-based routes
  without Next/Remix
- **Store**: ultra-light client state (single primitive, not Zustand replacement)
- **Form**: framework-agnostic forms (React Hook Form is React-only)
- Trigger phrases: "TanStack Query", "useQuery", "useMutation", "TanStack
  Router", "type-safe routing", "optimistic update", "infinite query"

## Setup

```bash
# Query
pnpm add @tanstack/react-query @tanstack/react-query-devtools

# Router (file-based via Vite plugin)
pnpm add @tanstack/react-router
pnpm add -D @tanstack/router-plugin

# Store + Form
pnpm add @tanstack/store @tanstack/react-form

# Persistence / Sync alternatives
pnpm add @tanstack/query-async-storage-persister @tanstack/react-query-persist-client
```

Verify: `pnpm list @tanstack/react-query` → 5.x.

No API keys.

## Common recipes

### Recipe 1 — QueryClient provider

```tsx
// src/main.tsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

const qc = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,         // data is fresh for 1 minute
      gcTime: 5 * 60_000,        // garbage-collect after 5 minutes idle
      retry: 2,
      refetchOnWindowFocus: true,
    },
  },
});

createRoot(document.getElementById("root")!).render(
  <QueryClientProvider client={qc}>
    <App />
    {import.meta.env.DEV && <ReactQueryDevtools />}
  </QueryClientProvider>,
);
```

### Recipe 2 — `useQuery` with typed key + abort

```tsx
import { useQuery } from "@tanstack/react-query";

interface User { id: string; name: string }

function UserCard({ id }: { id: string }) {
  const { data, isPending, isError, error } = useQuery({
    queryKey: ["user", id] as const,
    queryFn: async ({ signal }) => {
      const res = await fetch(`/api/users/${id}`, { signal });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json() as Promise<User>;
    },
    enabled: !!id,
  });

  if (isPending) return <p>Loading...</p>;
  if (isError) return <p role="alert">{error.message}</p>;
  return <p>{data.name}</p>;
}
```

`signal` enables auto-abort on unmount.

### Recipe 3 — `useSuspenseQuery` (React Suspense integration)

```tsx
import { useSuspenseQuery } from "@tanstack/react-query";
import { Suspense, ErrorBoundary } from "react";

function User({ id }: { id: string }) {
  const { data } = useSuspenseQuery({
    queryKey: ["user", id],
    queryFn: () => fetch(`/api/users/${id}`).then(r => r.json()),
  });
  return <p>{data.name}</p>;
}

// Parent: <Suspense fallback={...}><ErrorBoundary>...<User id={...} /></ErrorBoundary></Suspense>
```

No `isPending` / `isError` branches — Suspense + ErrorBoundary handle them.

### Recipe 4 — `useMutation` with optimistic updates + rollback

```tsx
import { useMutation, useQueryClient } from "@tanstack/react-query";

function TodoList() {
  const qc = useQueryClient();
  const addTodo = useMutation({
    mutationFn: (text: string) =>
      fetch("/api/todos", { method: "POST", body: JSON.stringify({ text }) }).then(r => r.json()),

    onMutate: async (text) => {
      await qc.cancelQueries({ queryKey: ["todos"] });
      const previous = qc.getQueryData<Todo[]>(["todos"]);
      qc.setQueryData<Todo[]>(["todos"], (old = []) => [
        ...old,
        { id: `tmp-${Date.now()}`, text },
      ]);
      return { previous };
    },

    onError: (_err, _vars, ctx) => qc.setQueryData(["todos"], ctx?.previous),
    onSettled: () => qc.invalidateQueries({ queryKey: ["todos"] }),
  });

  return <button onClick={() => addTodo.mutate("Buy milk")}>Add</button>;
}
```

### Recipe 5 — `useInfiniteQuery`

```tsx
import { useInfiniteQuery } from "@tanstack/react-query";

function Feed() {
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = useInfiniteQuery({
    queryKey: ["feed"],
    queryFn: ({ pageParam }) =>
      fetch(`/api/feed?cursor=${pageParam ?? ""}`).then(r => r.json()),
    initialPageParam: "",
    getNextPageParam: (last) => last.nextCursor ?? undefined,
  });

  return (
    <>
      {data?.pages.flatMap(p => p.items).map(item => <Item key={item.id} {...item} />)}
      {hasNextPage && (
        <button onClick={() => fetchNextPage()} disabled={isFetchingNextPage}>
          {isFetchingNextPage ? "Loading..." : "Load more"}
        </button>
      )}
    </>
  );
}
```

### Recipe 6 — Persistent cache (offline support)

```tsx
import { persistQueryClient } from "@tanstack/react-query-persist-client";
import { createAsyncStoragePersister } from "@tanstack/query-async-storage-persister";

const persister = createAsyncStoragePersister({ storage: localStorage });
persistQueryClient({ queryClient: qc, persister, maxAge: 1000 * 60 * 60 * 24 });
```

App resumes from cache on reload. Pair with `refetchOnReconnect: true`.

### Recipe 7 — TanStack Router (file-based, Vite plugin)

```ts
// vite.config.ts
import { TanStackRouterVite } from "@tanstack/router-plugin/vite";

export default defineConfig({
  plugins: [TanStackRouterVite(), react()],
});
```

```
src/routes/
  __root.tsx         # root layout
  index.tsx          # /
  posts/
    index.tsx        # /posts
    $postId.tsx      # /posts/$postId  (params)
  about.tsx          # /about
```

```tsx
// src/routes/posts/$postId.tsx
import { createFileRoute } from "@tanstack/react-router";
import { useSuspenseQuery } from "@tanstack/react-query";

export const Route = createFileRoute("/posts/$postId")({
  loader: ({ params, context }) =>
    context.queryClient.ensureQueryData({
      queryKey: ["post", params.postId],
      queryFn: () => fetch(`/api/posts/${params.postId}`).then(r => r.json()),
    }),
  component: PostComponent,
  errorComponent: ({ error }) => <p>Error: {error.message}</p>,
});

function PostComponent() {
  const { postId } = Route.useParams(); // fully typed!
  const { data } = useSuspenseQuery({
    queryKey: ["post", postId],
    queryFn: () => fetch(`/api/posts/${postId}`).then(r => r.json()),
  });
  return <article><h1>{data.title}</h1></article>;
}
```

### Recipe 8 — Typed search params

```tsx
import { z } from "zod";
import { zodValidator } from "@tanstack/zod-adapter";

export const Route = createFileRoute("/search")({
  validateSearch: zodValidator(z.object({
    q: z.string().default(""),
    page: z.number().int().min(1).default(1),
  })),
  loaderDeps: ({ search }) => ({ q: search.q, page: search.page }),
  loader: ({ deps }) => fetchResults(deps.q, deps.page),
  component: SearchPage,
});

function SearchPage() {
  const { q, page } = Route.useSearch();  // typed!
  const navigate = Route.useNavigate();
  return (
    <input
      value={q}
      onChange={e => navigate({ search: prev => ({ ...prev, q: e.target.value, page: 1 }) })}
    />
  );
}
```

### Recipe 9 — TanStack Form (framework-agnostic)

```tsx
import { useForm } from "@tanstack/react-form";
import { z } from "zod";

const Schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

function LoginForm() {
  const form = useForm({
    defaultValues: { email: "", password: "" },
    onSubmit: async ({ value }) => {
      await api.login(Schema.parse(value));
    },
    validators: { onChange: Schema },
  });

  return (
    <form onSubmit={(e) => { e.preventDefault(); form.handleSubmit(); }}>
      <form.Field name="email">
        {(field) => (
          <>
            <label htmlFor={field.name}>Email</label>
            <input
              id={field.name}
              value={field.state.value}
              onChange={(e) => field.handleChange(e.target.value)}
              aria-invalid={field.state.meta.errors.length > 0}
            />
            {field.state.meta.errors[0] && <p role="alert">{field.state.meta.errors[0]}</p>}
          </>
        )}
      </form.Field>
      <button type="submit">Log in</button>
    </form>
  );
}
```

### Recipe 10 — TanStack Store

```ts
import { Store } from "@tanstack/store";
import { useStore } from "@tanstack/react-store";

export const counter = new Store(0);

// In a component
function Counter() {
  const count = useStore(counter);
  return <button onClick={() => counter.setState(c => c + 1)}>{count}</button>;
}
```

For richer state, prefer Zustand. Store is intended as a primitive used by
other TanStack libraries.

## Examples

### Example 1: Convert `useEffect` fetch to `useQuery`

**Before:**
```tsx
useEffect(() => {
  let cancel = false;
  fetch(`/api/posts/${id}`)
    .then(r => r.json())
    .then(d => !cancel && setPost(d));
  return () => { cancel = true; };
}, [id]);
```

**After:**
```tsx
const { data: post } = useQuery({
  queryKey: ["post", id],
  queryFn: ({ signal }) => fetch(`/api/posts/${id}`, { signal }).then(r => r.json()),
});
```

### Example 2: Cache invalidation after mutation

```tsx
const mutation = useMutation({
  mutationFn: updatePost,
  onSuccess: (_data, vars) => {
    qc.invalidateQueries({ queryKey: ["post", vars.id] });
    qc.invalidateQueries({ queryKey: ["posts"] }); // list view
  },
});
```

## Edge cases / gotchas

- **`queryKey` is an array** — order matters, contents must be serializable.
  Avoid passing functions/classes.
- **`staleTime: 0`** (default) refetches on every mount — set 60s+ for read-heavy
  endpoints.
- **`gcTime` is when unused cache is freed** — not "data expiry". Data goes stale
  before GC.
- **`enabled: false`** suspends the query — use for dependent queries.
- **Suspense queries** must be inside `<Suspense>` AND `<ErrorBoundary>` — without
  ErrorBoundary, errors crash the app.
- **`useQueries`** for parallel queries with dynamic count.
- **TanStack Router needs `<RouterProvider router={router} />`** at the root —
  `__root.tsx` defines the layout component but NOT the provider.
- **`Route.useParams()` is per-route hook** — typed to that route's params.
- **`zodValidator` adapter** required for search params with zod; without it,
  validation runs but types stay `unknown`.
- **Devtools** ship code in production unless you guard with
  `import.meta.env.DEV` / `process.env.NODE_ENV`.
- **Server-side rendering** with TanStack Query — use `dehydrate` / `hydrate`
  helpers to ship the cache to the client. In Next App Router, prefer Server
  Components directly for the initial data.

## Sources

- [TanStack Query docs](https://tanstack.com/query/v5/docs/framework/react/overview)
- [TanStack Router docs](https://tanstack.com/router/latest/docs/framework/react/overview)
- [TanStack Form docs](https://tanstack.com/form/latest)
- [TanStack Store docs](https://tanstack.com/store/latest)
- [Query optimistic updates](https://tanstack.com/query/v5/docs/framework/react/guides/optimistic-updates)
- [Tanner Linsley — Query 5 talk (React Summit 2024)](https://www.reactsummit.com/)
- [TkDodo's Practical React Query series](https://tkdodo.eu/blog/practical-react-query) — gold-standard tutorial
