<!--
Source: https://react.dev/blog/2024/12/05/react-19 · https://react.dev/reference/rsc/server-components
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# React 19 — Server Components, Actions, and `use()`

React 19 (stable Dec 2024) is the baseline for new React work. The breaking
ideas you have to internalise: components are server-default in modern
meta-frameworks, mutations live in Server Actions, and `use()` reads promises
and context in render.

## When to use

- Authoring a Next 15 / TanStack Start / React Router 7 (Remix) app from scratch
- Migrating a React 18 app that uses `forwardRef`, `useFormState`, string refs,
  `propTypes`, or `ReactDOM.render`
- Reaching for `useEffect` to fetch data — STOP, use this skill instead
- Building forms that mutate server data (replace bespoke fetch handlers)
- Trigger phrases: "Server Component", "Server Action", "RSC", "useActionState",
  "useOptimistic", "use() promise", "ref as a prop", "React 19 upgrade"

## Setup

```bash
# New SPA (no SSR) — Vite + React 19
pnpm create vite@latest my-app --template react-ts

# New full-stack — Next 15 ships React 19 by default
pnpm dlx create-next-app@latest my-app --typescript --app --tailwind

# Upgrade an existing React 18 app
pnpm add react@latest react-dom@latest
pnpm add -D @types/react@latest @types/react-dom@latest
pnpm dlx codemod@latest react/19/migration-recipe ./src
```

Verify: `node -e "console.log(require('react').version)"` → 19.x.

No API keys required — React 19 is OSS.

## Common recipes

### Recipe 1 — Server Component fetching data directly

```tsx
// app/users/[id]/page.tsx
import { notFound } from "next/navigation";

// `params` is async in Next 15 — await it.
export default async function UserPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const user = await db.user.findUnique({ where: { id } });
  if (!user) notFound();
  return <article><h1>{user.name}</h1></article>;
}
```

No `useEffect`, no `useState`, no loading flag — Suspense handles streaming.

### Recipe 2 — Client island marked with `"use client"`

```tsx
// components/copy-button.tsx
"use client";
import { useState } from "react";

export function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      type="button"
      onClick={async () => {
        await navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 1500);
      }}
    >
      {copied ? "Copied!" : "Copy"}
    </button>
  );
}
```

Server Component renders it; only this leaf ships JS.

### Recipe 3 — Server Action + `useActionState`

```tsx
// app/_actions/create-comment.ts
"use server";
import { z } from "zod";
import { revalidatePath } from "next/cache";

const Schema = z.object({
  postId: z.string().min(1),
  body: z.string().min(1).max(500),
});

export type State = { error?: string; fieldErrors?: Record<string, string[]> };

export async function createComment(
  _prev: State,
  formData: FormData,
): Promise<State> {
  const parsed = Schema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) return { fieldErrors: parsed.error.flatten().fieldErrors };
  await db.comment.create({ data: parsed.data });
  revalidatePath(`/posts/${parsed.data.postId}`);
  return {};
}
```

```tsx
// components/comment-form.tsx
"use client";
import { useActionState } from "react";
import { useFormStatus } from "react-dom";
import { createComment, type State } from "@/app/_actions/create-comment";

function Submit() {
  const { pending } = useFormStatus();
  return (
    <button type="submit" disabled={pending}>
      {pending ? "Posting..." : "Post comment"}
    </button>
  );
}

export function CommentForm({ postId }: { postId: string }) {
  const [state, action] = useActionState<State, FormData>(createComment, {});
  return (
    <form action={action}>
      <input type="hidden" name="postId" value={postId} />
      <label htmlFor="body">Comment</label>
      <textarea
        id="body"
        name="body"
        required
        aria-invalid={!!state.fieldErrors?.body}
        aria-describedby={state.fieldErrors?.body ? "body-error" : undefined}
      />
      {state.fieldErrors?.body && (
        <p id="body-error" role="alert">{state.fieldErrors.body[0]}</p>
      )}
      <Submit />
    </form>
  );
}
```

`useActionState` replaces `useFormState`. `useFormStatus` reports the in-flight
state of the **closest ancestor form**.

### Recipe 4 — Optimistic UI with `useOptimistic`

```tsx
"use client";
import { useOptimistic, useTransition } from "react";
import { likePost } from "@/app/_actions/like-post";

export function LikeButton({ postId, initialLikes }: { postId: string; initialLikes: number }) {
  const [isPending, startTransition] = useTransition();
  const [optimistic, addOptimistic] = useOptimistic(
    initialLikes,
    (current, delta: number) => current + delta,
  );

  return (
    <button
      type="button"
      disabled={isPending}
      onClick={() => {
        startTransition(async () => {
          addOptimistic(1);
          await likePost(postId);
        });
      }}
    >
      {optimistic} likes
    </button>
  );
}
```

Server result reconciles automatically; on error, the optimistic value rolls back.

### Recipe 5 — `use()` to unwrap a promise in render

```tsx
import { use, Suspense } from "react";

function UserName({ promise }: { promise: Promise<{ name: string }> }) {
  const user = use(promise); // suspends until resolved
  return <span>{user.name}</span>;
}

export default function Page() {
  const promise = fetch("/api/me").then(r => r.json());
  return (
    <Suspense fallback={<span>Loading...</span>}>
      <UserName promise={promise} />
    </Suspense>
  );
}
```

`use()` can also read context conditionally — something hooks can't.

### Recipe 6 — `ref` as a regular prop (no more `forwardRef`)

```tsx
// React 19: just declare ref in props.
interface InputProps extends React.ComponentPropsWithoutRef<"input"> {
  ref?: React.Ref<HTMLInputElement>;
}

export function Input({ ref, ...rest }: InputProps) {
  return <input ref={ref} {...rest} />;
}

// Usage
const inputRef = useRef<HTMLInputElement>(null);
<Input ref={inputRef} />;
```

Migration: `pnpm dlx codemod@latest react/19/replace-forwardRef ./src`.

### Recipe 7 — Context without `.Provider`

```tsx
const ThemeContext = createContext<"light" | "dark">("light");

// React 19 — render the context directly
export function App() {
  return (
    <ThemeContext value="dark">
      <Page />
    </ThemeContext>
  );
}
```

`<Context.Provider>` still works but is deprecated.

### Recipe 8 — Async transitions and pending UI

```tsx
"use client";
import { useTransition, useState } from "react";

export function SaveButton() {
  const [isPending, startTransition] = useTransition();
  const [error, setError] = useState<string>();
  return (
    <>
      <button
        type="button"
        disabled={isPending}
        onClick={() => {
          startTransition(async () => {
            try { await saveDraft(); }
            catch (e) { setError((e as Error).message); }
          });
        }}
      >
        {isPending ? "Saving..." : "Save"}
      </button>
      {error && <p role="alert">{error}</p>}
    </>
  );
}
```

`startTransition` now accepts async functions (React 19 expansion of the React 18 API).

### Recipe 9 — Document metadata in components

```tsx
export default function PostPage({ post }: { post: Post }) {
  return (
    <>
      <title>{post.title}</title>
      <meta name="description" content={post.excerpt} />
      <link rel="canonical" href={`https://example.com/posts/${post.slug}`} />
      <article>{post.body}</article>
    </>
  );
}
```

React 19 hoists `<title>`, `<meta>`, `<link>` into `<head>` automatically.

## Examples

### Example 1: Migrate a stateful React 18 component to RSC

**Goal:** A `UserProfile` that currently uses `useEffect` + `fetch` should be RSC.

**Before:**
```tsx
function UserProfile({ id }: { id: string }) {
  const [user, setUser] = useState(null);
  useEffect(() => { fetch(`/api/users/${id}`).then(r => r.json()).then(setUser); }, [id]);
  if (!user) return <Spinner />;
  return <div>{user.name}</div>;
}
```

**After:**
```tsx
// app/users/[id]/page.tsx — Server Component, no hooks
export default async function UserProfile({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const user = await db.user.findUnique({ where: { id } });
  if (!user) notFound();
  return <div>{user.name}</div>;
}
```

Race conditions gone, no client JS, no loading state needed (Suspense boundary in
`loading.tsx` takes over).

### Example 2: Convert a `useFormState` form to `useActionState`

```bash
pnpm dlx codemod@latest react/19/replace-use-form-state ./src
```

Verifies: `useFormState` → `useActionState` import + call signature, no manual edits.

## Edge cases / gotchas

- **`"use client"` is contagious downward** — anything imported by a client
  component is also client. Keep the boundary as deep as possible.
- **You cannot import a Server Component from a Client Component** — pass it as
  `children` or a prop instead.
- **Server Actions are POST endpoints with hashed names** — never return secrets
  from them, never trust client-side validation alone.
- **`useOptimistic` requires a transition** — it must be inside `startTransition`
  or React throws. Use the `useTransition` pair, not bare `useOptimistic`.
- **PropTypes removed** — strip them; TypeScript types are the runtime contract.
- **`ReactDOM.render` removed** — use `ReactDOM.createRoot(el).render(<App />)`.
- **String refs removed** — codemod replaces with `useRef`.
- **`forwardRef` still works** but is no longer needed; the codemod removes it.
- **`use()` is for render only** — calling it in an event handler throws. For
  handlers, `await` the promise directly.
- **Document metadata hoisting only works server-side** — for client-only apps,
  use `react-helmet-async` or framework-specific equivalents.

## Sources

- [React 19 announcement](https://react.dev/blog/2024/12/05/react-19) — official release
- [React 19 upgrade guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide) — codemod recipes + breaking changes
- [Server Components reference](https://react.dev/reference/rsc/server-components) — RSC semantics
- [Server Actions reference](https://react.dev/reference/rsc/server-actions) — `"use server"` directive
- [`useActionState` reference](https://react.dev/reference/react/useActionState)
- [`useOptimistic` reference](https://react.dev/reference/react/useOptimistic)
- [`use()` reference](https://react.dev/reference/react/use)
- [Next.js + React 19 best practices (Vercel, 2025)](https://vercel.com/blog/whats-new-in-react-19)
