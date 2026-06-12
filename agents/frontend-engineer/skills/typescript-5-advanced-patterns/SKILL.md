<!--
Source: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-5.html
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# TypeScript 5 — Advanced patterns

TypeScript 5.5+ gives you the tooling to write end-to-end-typed apps without
casting. The patterns the agent reaches for: `satisfies`, const type parameters,
conditional types, template literal types, `using` for resource cleanup, and
the `type-fest` + `ts-reset` packages for utility types and stdlib fixes.

## When to use

- Authoring shared types between frontend and backend (tRPC-style)
- Adding type-safe wrappers around dynamic APIs (route params, form data)
- Bringing strict types to an `any`-heavy codebase
- Designing component libraries with discriminated-union props
- Trigger phrases: "TypeScript", "type error", "satisfies", "const generic",
  "conditional type", "template literal", "ts-reset", "type-fest", "branded type"

## Setup

```bash
pnpm add -D typescript@latest type-fest @total-typescript/ts-reset
# Optional schema libs (often paired with these patterns)
pnpm add zod                                # most common
pnpm add valibot                            # bundle-friendlier
pnpm add arktype                            # TS-syntax-based
```

```jsonc
// tsconfig.json — strict baseline
{
  "compilerOptions": {
    "target": "es2022",
    "module": "esnext",
    "moduleResolution": "bundler",
    "lib": ["es2023", "dom", "dom.iterable"],
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true,
    "skipLibCheck": true,
    "jsx": "preserve"
  },
  "include": ["src/**/*", "reset.d.ts"]
}
```

```ts
// reset.d.ts (at project root)
import "@total-typescript/ts-reset";
```

Verify: `pnpm exec tsc --version` → 5.5+.

No API keys.

## Common recipes

### Recipe 1 — `satisfies` (validate without widening)

```ts
type RGB = [r: number, g: number, b: number];
type Palette = Record<string, RGB | string>;

const palette = {
  red: [255, 0, 0],
  green: "#00ff00",
} satisfies Palette;

// palette.red has type `[number, number, number]`, NOT widened to `RGB | string`.
// You still get autocompletion and an error if you typo a key.
const r = palette.red[0]; // number
```

Without `satisfies`, `as Palette` would widen the types. Without anything,
TypeScript widens to `{ red: number[]; green: string }` losing the tuple shape.

### Recipe 2 — `const` type parameters (5.0+)

```ts
function tuple<const T extends readonly unknown[]>(values: T): T {
  return values;
}

const t = tuple([1, "a", true]);
//    ^? readonly [1, "a", true]

// Without `const`, type would be `(string | number | boolean)[]`.
```

### Recipe 3 — Conditional types + `infer`

```ts
type ExtractParams<S extends string> =
  S extends `${string}/:${infer P}/${infer R}` ? P | ExtractParams<R>
  : S extends `${string}/:${infer P}` ? P
  : never;

type R1 = ExtractParams<"/users/:id">;          // "id"
type R2 = ExtractParams<"/users/:id/posts/:pid">; // "id" | "pid"
```

Combine with template literal types for type-safe route builders.

### Recipe 4 — Discriminated union props

```tsx
type ButtonProps =
  | { variant: "primary"; onClick: () => void }
  | { variant: "link"; href: string; onClick?: never };

function Button(props: ButtonProps) {
  if (props.variant === "link") {
    return <a href={props.href}>...</a>;
  }
  return <button onClick={props.onClick}>...</button>;
}

// Compiler enforces: <Button variant="link" href="/x" />
//                    <Button variant="primary" onClick={() => {}} />
//                    <Button variant="link" /> // ERROR — href missing
```

### Recipe 5 — Branded types (nominal typing)

```ts
type Brand<T, B> = T & { readonly __brand: B };

type UserId = Brand<string, "UserId">;
type PostId = Brand<string, "PostId">;

function asUserId(s: string): UserId { return s as UserId; }
function getUser(id: UserId) { /* ... */ }

const a = asUserId("u_123");
const b = "p_456" as PostId;
getUser(a);     // ok
getUser(b);     // ERROR — PostId is not assignable to UserId
```

Mixing IDs of different entities is a real bug class; brands eliminate it.

### Recipe 6 — `type-fest` utilities

```ts
import type {
  SetRequired, SetOptional, RequireAtLeastOne, ReadonlyDeep, Tagged, Promisable
} from "type-fest";

interface User { id: string; name?: string; email?: string; }

type Createable = SetRequired<User, "name" | "email">; // name + email mandatory
type Editable   = SetOptional<User, "id">;             // id optional
type Either     = RequireAtLeastOne<User, "name" | "email">; // at least one
type Frozen     = ReadonlyDeep<User>;                  // recursive readonly
type AsyncOrSync<T> = Promisable<T>;                   // T | Promise<T>
```

### Recipe 7 — `ts-reset` (fix stdlib gotchas)

After importing `@total-typescript/ts-reset`:

```ts
// `.filter(Boolean)` now narrows correctly
const items: (string | undefined)[] = ["a", undefined, "b"];
const cleaned = items.filter(Boolean); // string[] (not (string|undefined)[])

// `.json()` returns unknown (not any)
const data: unknown = await fetch("/api").then(r => r.json());

// JSON.parse returns unknown (not any)
const parsed: unknown = JSON.parse(input);
```

Forces validation at boundaries — drop the import once you've added zod
schemas everywhere.

### Recipe 8 — `using` and `await using` (5.2+)

```ts
class FileHandle implements Disposable {
  [Symbol.dispose]() { this.close(); }
  close() { /* ... */ }
}

function readConfig() {
  using fh = new FileHandle("/etc/config");
  // fh is disposed when the scope exits, even on throw
}

class DBConn implements AsyncDisposable {
  async [Symbol.asyncDispose]() { await this.close(); }
  async close() { /* ... */ }
}

async function query() {
  await using db = new DBConn();
  return await db.fetchAll();
}
```

Replaces try/finally cleanup boilerplate.

### Recipe 9 — Zod schema → TypeScript type

```ts
import { z } from "zod";

const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().int().min(0).optional(),
  role: z.enum(["admin", "user"]),
});

export type User = z.infer<typeof UserSchema>;

export function parseUser(input: unknown): User {
  return UserSchema.parse(input); // throws ZodError on mismatch
}
```

One source of truth — schema + type together.

### Recipe 10 — Template literal types for type-safe events

```ts
type EventMap = {
  "user:created": { id: string };
  "user:deleted": { id: string };
  "post:published": { postId: string };
};

function emit<E extends keyof EventMap>(event: E, payload: EventMap[E]) {
  // ...
}

emit("user:created", { id: "u_1" });     // ok
emit("user:created", { postId: "p_1" }); // ERROR
emit("unknown", { id: "x" });            // ERROR
```

### Recipe 11 — Exhaustive switch with `never`

```ts
type Shape = { kind: "circle"; r: number } | { kind: "square"; s: number };

function area(s: Shape): number {
  switch (s.kind) {
    case "circle": return Math.PI * s.r ** 2;
    case "square": return s.s ** 2;
    default: {
      const _exhaustive: never = s;
      throw new Error(`Unhandled: ${_exhaustive}`);
    }
  }
}
```

Adding a new `Shape` variant causes a compile error here — forcing you to
update every consumer.

## Examples

### Example 1: Type-safe `fetch` wrapper

```ts
import { z } from "zod";

async function api<S extends z.ZodTypeAny>(
  path: string,
  schema: S,
  init?: RequestInit,
): Promise<z.infer<S>> {
  const res = await fetch(path, init);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const json: unknown = await res.json();
  return schema.parse(json);
}

const User = z.object({ id: z.string(), name: z.string() });
const user = await api(`/api/users/1`, User);
//    ^? { id: string; name: string }
```

### Example 2: Convert `any` to `unknown` with narrowing

**Before:**
```ts
function processData(data: any) {
  console.log(data.user.name); // crashes at runtime
}
```

**After:**
```ts
function processData(data: unknown) {
  if (
    typeof data === "object" && data !== null && "user" in data &&
    typeof data.user === "object" && data.user !== null && "name" in data.user
  ) {
    console.log(data.user.name); // narrowed
  }
}

// Better: parse with a schema
const Schema = z.object({ user: z.object({ name: z.string() }) });
const parsed = Schema.parse(data);
console.log(parsed.user.name);
```

## Edge cases / gotchas

- **`satisfies` vs `as` vs annotation** — pick `satisfies` when you want the
  literal's narrow type AND validation. Use annotation when you want widening
  (`const x: Palette = ...`). Avoid `as` except for branded types or DOM casts.
- **`noUncheckedIndexedAccess: true`** changes every array/object index to
  `T | undefined`. Adopt this in new projects.
- **`exactOptionalPropertyTypes: true`** stops `{ x: undefined }` from satisfying
  `{ x?: T }`. Often surfaces real bugs but breaks libraries that emit explicit
  `undefined`.
- **`verbatimModuleSyntax: true`** requires `import type` for type-only imports.
- **Recursive types depth** — TypeScript caps at ~50 deep. Use the
  `[any] extends [Foo]` trick to break recursion when needed.
- **`infer extends Foo`** (5.0+) narrows within `infer`.
- **`ts-reset` is global** — once imported, every project file gets the
  overrides. Don't import it in a published library.
- **TS errors on optional chaining + non-null assertion** — `foo?.bar!` is
  legal but a code smell. Refactor to narrowing.
- **`as const`** widens differently per nesting level. Combine with `satisfies`
  for full control: `[1, 2, 3] as const satisfies readonly number[]`.
- **Don't widen schemas** — `z.string()` then `.refine(x => isEmail(x))` keeps
  type `string`. Use `z.string().email()` for the canonical email type.

## Sources

- [TypeScript handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [TypeScript 5.5 release](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-5.html)
- [type-fest README](https://github.com/sindresorhus/type-fest)
- [ts-reset README](https://github.com/total-typescript/ts-reset)
- [Zod docs](https://zod.dev/)
- [Matt Pocock — Total TypeScript](https://www.totaltypescript.com/) — modern TS patterns
- [Anders Hejlsberg — TS at Build 2024](https://www.typescriptlang.org/) — annual roadmap
