<!--
Source: https://react-hook-form.com/ · https://zod.dev/ · https://conform.guide/
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# React Hook Form + zod / valibot + Conform — Forms

Form handling in 2026 splits between **React Hook Form** (default for client-side
React), **Conform** (Server Action-first for Next 15), and schema libs (**zod**
default, **valibot** for bundle savings, **arktype** for TS-syntax schemas).

## When to use

- React form with client-side validation, controlled inputs, dynamic fields
  → **React Hook Form + zod**
- Next 15 Server Action with progressive enhancement → **Conform + zod**
- Bundle-size critical (mobile) → **valibot** instead of zod
- Framework-agnostic / Vue / Svelte / Solid → **TanStack Form** (covered in
  `tanstack-query-router-store`)
- Trigger phrases: "form", "validation", "zod", "valibot", "React Hook Form",
  "Conform", "Server Action form", "useFormState"

## Setup

```bash
# React Hook Form + zod
pnpm add react-hook-form @hookform/resolvers zod

# Conform + zod (Next 15 Server Actions)
pnpm add @conform-to/react @conform-to/zod

# valibot alternative
pnpm add valibot @hookform/resolvers
```

Verify: `pnpm list react-hook-form` → 7.x.

No API keys.

## Common recipes — React Hook Form + zod

### Recipe 1 — Basic form

```tsx
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const Schema = z.object({
  email: z.string().email("Please enter a valid email"),
  password: z.string().min(8, "Min 8 characters"),
  remember: z.boolean().default(false),
});
type FormData = z.infer<typeof Schema>;

export function LoginForm() {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<FormData>({
    resolver: zodResolver(Schema),
    defaultValues: { email: "", password: "", remember: false },
  });

  return (
    <form onSubmit={handleSubmit(async (data) => {
      await api.login(data);
    })}>
      <label htmlFor="email">Email</label>
      <input
        id="email"
        type="email"
        autoComplete="email"
        {...register("email")}
        aria-invalid={!!errors.email}
        aria-describedby={errors.email ? "email-err" : undefined}
      />
      {errors.email && <p id="email-err" role="alert">{errors.email.message}</p>}

      <label htmlFor="password">Password</label>
      <input
        id="password"
        type="password"
        autoComplete="current-password"
        {...register("password")}
        aria-invalid={!!errors.password}
        aria-describedby={errors.password ? "pw-err" : undefined}
      />
      {errors.password && <p id="pw-err" role="alert">{errors.password.message}</p>}

      <label>
        <input type="checkbox" {...register("remember")} /> Remember me
      </label>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Signing in..." : "Sign in"}
      </button>
    </form>
  );
}
```

### Recipe 2 — `Controller` for custom inputs (Combobox, Date picker)

```tsx
import { useForm, Controller } from "react-hook-form";
import { Combobox } from "@/components/Combobox";

const { control } = useForm<{ country: string }>({ resolver: zodResolver(Schema) });

<Controller
  control={control}
  name="country"
  render={({ field, fieldState }) => (
    <>
      <Combobox value={field.value} onChange={field.onChange} options={countries} />
      {fieldState.error && <p role="alert">{fieldState.error.message}</p>}
    </>
  )}
/>
```

Use `Controller` only when a 3rd-party input doesn't support `ref` / standard
event signatures. Native inputs use `register`.

### Recipe 3 — Field arrays (dynamic lists)

```tsx
import { useForm, useFieldArray } from "react-hook-form";

const { control, register } = useForm<{ items: { name: string; qty: number }[] }>({
  defaultValues: { items: [{ name: "", qty: 1 }] },
});

const { fields, append, remove } = useFieldArray({ control, name: "items" });

return (
  <>
    {fields.map((field, idx) => (
      <div key={field.id} className="flex gap-2">
        <input {...register(`items.${idx}.name`)} placeholder="Name" />
        <input type="number" {...register(`items.${idx}.qty`, { valueAsNumber: true })} />
        <button type="button" onClick={() => remove(idx)}>×</button>
      </div>
    ))}
    <button type="button" onClick={() => append({ name: "", qty: 1 })}>Add</button>
  </>
);
```

### Recipe 4 — Watching specific fields (`watch`)

```tsx
const { watch, register } = useForm<{ password: string; confirm: string }>();
const password = watch("password");

<input
  type="password"
  {...register("confirm", { validate: (v) => v === password || "Passwords don't match" })}
/>
```

For cross-field validation, prefer zod `.refine()`:

```ts
const Schema = z.object({
  password: z.string().min(8),
  confirm: z.string(),
}).refine(d => d.password === d.confirm, {
  message: "Passwords don't match",
  path: ["confirm"],
});
```

### Recipe 5 — Server validation errors → field errors

```tsx
const { handleSubmit, setError } = useForm<FormData>();

const onSubmit = handleSubmit(async (data) => {
  const result = await api.signup(data);
  if (!result.ok) {
    Object.entries(result.fieldErrors).forEach(([field, msgs]) => {
      setError(field as keyof FormData, { message: msgs[0] });
    });
  }
});
```

### Recipe 6 — Async validation (debounced uniqueness check)

```tsx
const Schema = z.object({
  username: z.string().min(3).refine(async (v) => {
    const res = await fetch(`/api/users/check?u=${v}`);
    return res.ok && (await res.json()).available;
  }, "Username taken"),
});
```

Use `mode: "onBlur"` to avoid running the async check on every keystroke.

## Common recipes — Conform + zod (Next 15 Server Actions)

### Recipe 7 — Server Action form with Conform

```ts
// app/_actions/signup.ts
"use server";
import { parseWithZod } from "@conform-to/zod";
import { z } from "zod";
import { redirect } from "next/navigation";

const Schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export async function signup(_prev: unknown, formData: FormData) {
  const submission = parseWithZod(formData, { schema: Schema });
  if (submission.status !== "success") return submission.reply();

  await db.user.create({ data: submission.value });
  redirect("/welcome");
}
```

```tsx
// app/signup/page.tsx
"use client";
import { useActionState } from "react";
import { getFormProps, getInputProps, useForm } from "@conform-to/react";
import { parseWithZod } from "@conform-to/zod";
import { signup } from "@/app/_actions/signup";
// reuse Schema in both client + server
import { Schema } from "@/lib/schemas";

export default function SignupPage() {
  const [lastResult, action] = useActionState(signup, undefined);
  const [form, fields] = useForm({
    lastResult,
    onValidate: ({ formData }) => parseWithZod(formData, { schema: Schema }),
    shouldValidate: "onBlur",
    shouldRevalidate: "onInput",
  });

  return (
    <form {...getFormProps(form)} action={action}>
      <label htmlFor={fields.email.id}>Email</label>
      <input
        {...getInputProps(fields.email, { type: "email" })}
        autoComplete="email"
      />
      {fields.email.errors && <p role="alert">{fields.email.errors[0]}</p>}

      <label htmlFor={fields.password.id}>Password</label>
      <input
        {...getInputProps(fields.password, { type: "password" })}
        autoComplete="new-password"
      />
      {fields.password.errors && <p role="alert">{fields.password.errors[0]}</p>}

      <button type="submit">Sign up</button>
    </form>
  );
}
```

Form works without JS (progressive enhancement); with JS, errors appear inline
without a roundtrip.

## Common recipes — valibot (bundle-friendly)

### Recipe 8 — valibot schema

```ts
import * as v from "valibot";

const Schema = v.object({
  email: v.pipe(v.string(), v.email("Invalid email")),
  password: v.pipe(v.string(), v.minLength(8, "Min 8 chars")),
  age: v.optional(v.pipe(v.number(), v.minValue(18))),
});

type FormData = v.InferOutput<typeof Schema>;

// Use with RHF
import { valibotResolver } from "@hookform/resolvers/valibot";

const form = useForm<FormData>({ resolver: valibotResolver(Schema) });
```

valibot bundles ~95% smaller than zod for typical schemas (tree-shakes
unused validators).

## Examples

### Example 1: Share a zod schema between client + server

```ts
// src/lib/schemas/user.ts
import { z } from "zod";
export const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});
export type CreateUserInput = z.infer<typeof CreateUserSchema>;
```

```tsx
// Client form
import { CreateUserSchema } from "@/lib/schemas/user";
const form = useForm({ resolver: zodResolver(CreateUserSchema) });
```

```ts
// Server Action
import { CreateUserSchema } from "@/lib/schemas/user";
const parsed = CreateUserSchema.safeParse(Object.fromEntries(formData));
if (!parsed.success) return { errors: parsed.error.flatten() };
```

Same schema, both runtimes — single source of truth.

### Example 2: Multi-step wizard with persistence

```tsx
const { trigger, getValues, setValue } = useForm<WizardForm>({ shouldUnregister: false });

async function next() {
  const valid = await trigger(["email", "password"]); // validate current step
  if (!valid) return;
  setStep((s) => s + 1);
}
```

`shouldUnregister: false` keeps prior step values around across step changes.

## Edge cases / gotchas

- **`register` vs `Controller`** — register for native inputs (input/textarea/
  select). Controller for anything custom. Don't mix.
- **`valueAsNumber: true`** for number inputs — otherwise you get a string.
  Also `valueAsDate: true` for date inputs.
- **Default values** — set `defaultValues` on `useForm`, NOT on inputs. RHF
  manages the source of truth.
- **`mode: "onBlur"` vs `"onChange"` vs `"onSubmit"`** — onBlur is the most
  common UX; onChange shows errors as you type (annoying for new users).
- **`reset()` clears the form** — call after successful submission. Pass an
  object to reset to specific values.
- **`isDirty` vs `isValid`** — `isDirty` = any field changed; `isValid` = no
  validation errors. Use `isValid` to enable Submit button.
- **`zodResolver` doesn't pass undefined** — for `z.string().optional()` use
  `z.string().optional().or(z.literal(""))` if your form might emit "".
- **Conform `getInputProps` requires the type** — `{ type: "email" }` matters
  for `aria-invalid` + browser validation hints.
- **Server Action progressive enhancement** — works without JS only if you
  use `<form action={...}>` (not `onSubmit`).
- **valibot resolvers are separate** from zod resolvers — install
  `@hookform/resolvers` once; import the specific resolver per schema lib.
- **Don't validate twice** — if the Server Action validates, the client form
  is for UX only. The server is the source of truth.

## Sources

- [React Hook Form docs](https://react-hook-form.com/)
- [Conform docs](https://conform.guide/)
- [Zod docs](https://zod.dev/)
- [Valibot docs](https://valibot.dev/)
- [@hookform/resolvers](https://github.com/react-hook-form/resolvers)
- [arktype docs](https://arktype.io/)
- [Bulletproof React forms guide (2025)](https://github.com/alan2207/bulletproof-react) — production patterns
- [Conform vs RHF blog (Vercel, 2024)](https://vercel.com/blog/forms-with-react-19)
