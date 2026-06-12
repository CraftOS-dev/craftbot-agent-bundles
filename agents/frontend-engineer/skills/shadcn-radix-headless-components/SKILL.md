<!--
Source: https://ui.shadcn.com/ · https://www.radix-ui.com/ · https://react-spectrum.adobe.com/react-aria/
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# shadcn/ui + Radix + react-aria — Headless components

shadcn/ui is **copy-paste components** that you own in your repo. Underneath
they use Radix UI primitives (headless, accessible). For Adobe-grade
accessibility, `react-aria-components` is the alternative primitive set.

## When to use

- New design system — bootstrap with shadcn instead of importing a heavy lib
- Need WCAG-2.2-AA-compliant primitives (dialog, menu, listbox, combobox)
- Tailwind + Radix is the desired stack (default for Next + Tailwind projects)
- Cross-framework needs → Ark UI (Chakra team, React/Vue/Svelte/Solid)
- Trigger phrases: "shadcn", "shadcn/ui", "Radix", "headless", "dialog",
  "popover", "combobox", "accessible component", "react-aria"

## Decision tree

| Need | Pick |
|---|---|
| React + Tailwind + own the code | **shadcn/ui** |
| React + just primitives, custom styling | **Radix UI** |
| React + Adobe-grade a11y + i18n | **react-aria-components** |
| React + Vue + Svelte + Solid (cross-framework) | **Ark UI** |
| React + Tailwind + first-party design system | **Headless UI** |

## Setup — shadcn/ui

```bash
# Next.js 15 + Tailwind 4 + shadcn
pnpm dlx create-next-app@latest my-app --typescript --app --tailwind --src-dir
cd my-app
pnpm dlx shadcn@latest init
# answers: default style, Slate base color, CSS variables, components folder

# Add components as needed
pnpm dlx shadcn@latest add button card dialog form input label select
pnpm dlx shadcn@latest add toast dropdown-menu sheet tabs tooltip
```

The CLI writes components to `src/components/ui/*.tsx` — **you own them**.
Edit freely; future updates require re-running `add` or manual merging.

## Setup — Radix only (no shadcn)

```bash
pnpm add @radix-ui/react-dialog @radix-ui/react-dropdown-menu @radix-ui/react-tooltip
# (per-primitive install — tree-shake-friendly)
```

## Setup — react-aria-components

```bash
pnpm add react-aria-components
# Tailwind plugin for variant utilities
pnpm add -D tailwindcss-react-aria-components
```

## Common recipes — shadcn/ui

### Recipe 1 — Use a `Button`

```tsx
import { Button } from "@/components/ui/button";

<Button variant="default" size="lg" onClick={save}>Save</Button>
<Button variant="outline">Cancel</Button>
<Button variant="destructive" disabled={isPending}>Delete</Button>
<Button variant="ghost" asChild><a href="/help">Help</a></Button>
```

`asChild` passes props onto a child element instead of rendering a button —
Radix Slot pattern.

### Recipe 2 — Dialog with form

```tsx
import {
  Dialog, DialogContent, DialogDescription, DialogFooter,
  DialogHeader, DialogTitle, DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

export function CreateDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>New</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Create item</DialogTitle>
          <DialogDescription>Fill the form to create a new item.</DialogDescription>
        </DialogHeader>
        <form className="space-y-4">
          {/* form fields */}
        </form>
        <DialogFooter>
          <Button type="submit">Create</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
```

Focus management, Esc-to-close, scroll lock, focus trap — all handled by Radix.

### Recipe 3 — Form with React Hook Form + zod

```tsx
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const Schema = z.object({
  email: z.string().email("Invalid email"),
  name: z.string().min(1, "Required").max(100),
});
type FormValues = z.infer<typeof Schema>;

export function SignupForm() {
  const form = useForm<FormValues>({
    resolver: zodResolver(Schema),
    defaultValues: { email: "", name: "" },
  });

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit((v) => console.log(v))} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl><Input type="email" {...field} /></FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl><Input {...field} /></FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Submit</Button>
      </form>
    </Form>
  );
}
```

### Recipe 4 — Toast (Sonner under the hood)

```bash
pnpm dlx shadcn@latest add sonner
```

```tsx
import { Toaster } from "@/components/ui/sonner";
import { toast } from "sonner";

// in layout: <Toaster richColors />

// anywhere:
toast.success("Saved!");
toast.error("Failed to save", { description: "Check your connection." });
toast.promise(saveAsync(), {
  loading: "Saving...",
  success: "Saved!",
  error: "Failed",
});
```

### Recipe 5 — Combobox (autocomplete)

```tsx
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command";

<Command>
  <CommandInput placeholder="Search..." />
  <CommandList>
    <CommandEmpty>No results</CommandEmpty>
    <CommandGroup heading="Suggestions">
      {items.map(i => (
        <CommandItem key={i.id} value={i.label} onSelect={() => choose(i)}>
          {i.label}
        </CommandItem>
      ))}
    </CommandGroup>
  </CommandList>
</Command>
```

### Recipe 6 — Theming with CSS variables

```css
/* src/app/globals.css */
@import "tailwindcss";

@theme {
  --color-background: oklch(1 0 0);
  --color-foreground: oklch(0.15 0 0);
  --color-primary: oklch(0.4 0.18 250);
  --color-primary-foreground: oklch(0.98 0 0);
  --color-border: oklch(0.9 0.005 250);
  --radius: 0.5rem;
}

.dark {
  --color-background: oklch(0.15 0 0);
  --color-foreground: oklch(0.98 0 0);
}
```

shadcn components reference these via `bg-background`, `text-foreground`,
`border-border`. Toggle a `.dark` class on `<html>` to switch.

### Recipe 7 — `cn` helper (already added by shadcn init)

```ts
// src/lib/utils.ts
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

## Common recipes — Radix raw

### Recipe 8 — Tooltip with arrow

```tsx
import * as Tooltip from "@radix-ui/react-tooltip";

<Tooltip.Provider delayDuration={150}>
  <Tooltip.Root>
    <Tooltip.Trigger asChild>
      <button aria-label="Settings"><GearIcon /></button>
    </Tooltip.Trigger>
    <Tooltip.Portal>
      <Tooltip.Content className="bg-slate-900 text-white px-2 py-1 rounded text-sm" sideOffset={6}>
        Settings
        <Tooltip.Arrow className="fill-slate-900" />
      </Tooltip.Content>
    </Tooltip.Portal>
  </Tooltip.Root>
</Tooltip.Provider>
```

### Recipe 9 — Dropdown menu with keyboard nav

```tsx
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";

<DropdownMenu.Root>
  <DropdownMenu.Trigger asChild><Button>Open menu</Button></DropdownMenu.Trigger>
  <DropdownMenu.Portal>
    <DropdownMenu.Content className="rounded-md border bg-white p-1 shadow-md" sideOffset={4}>
      <DropdownMenu.Item onSelect={profile} className="px-3 py-2 outline-none data-[highlighted]:bg-slate-100">
        Profile
      </DropdownMenu.Item>
      <DropdownMenu.Item onSelect={logout}>Logout</DropdownMenu.Item>
    </DropdownMenu.Content>
  </DropdownMenu.Portal>
</DropdownMenu.Root>
```

## Common recipes — react-aria-components

### Recipe 10 — Searchable combobox

```tsx
import { ComboBox, Input, Label, Popover, ListBox, ListBoxItem } from "react-aria-components";

<ComboBox aria-label="Country">
  <Label>Country</Label>
  <Input />
  <Popover>
    <ListBox>
      {countries.map(c => <ListBoxItem key={c.code} id={c.code}>{c.name}</ListBoxItem>)}
    </ListBox>
  </Popover>
</ComboBox>
```

react-aria-components handles screen-reader announcements, type-to-search, and
RTL natively.

## Examples

### Example 1: Bootstrap a Next 15 + shadcn + Tailwind 4 project

```bash
pnpm dlx create-next-app@latest my-app --typescript --app --tailwind --src-dir
cd my-app
pnpm dlx shadcn@latest init
pnpm dlx shadcn@latest add button card dialog form input label
pnpm dev
```

### Example 2: Replace a `react-modal` import with shadcn Dialog

1. `pnpm dlx shadcn@latest add dialog`
2. Replace `<Modal isOpen={x}>` with `<Dialog open={x} onOpenChange={setX}>`
3. Trigger via `<DialogTrigger>` instead of imperative open
4. Remove `react-modal` from package.json

## Edge cases / gotchas

- **shadcn components live in YOUR repo** — `pnpm dlx shadcn add` re-installs
  files, possibly overwriting your edits. Diff before accepting.
- **`asChild`** delegates rendering to children — children MUST forward refs and
  spread props.
- **Radix Portal escapes z-index** — content renders at document end, so set
  z-index inside `Content`, not on the trigger.
- **Tailwind 4 + shadcn** works but tokens differ slightly — the shadcn init
  detects v4 and generates `@theme`-based tokens automatically.
- **`Toast` lib was Radix's own, now Sonner** — shadcn updated to Sonner in
  2024. Old `useToast` API still exists for back-compat.
- **`Combobox` is not in core shadcn** — built from `Command` (cmdk lib) +
  `Popover`. Reference https://ui.shadcn.com/docs/components/combobox.
- **Forms require RHF + zod** — shadcn `<Form>` is a thin wrapper around RHF.
  Plain forms work too but lose the auto-wired label/error a11y.
- **react-aria-components** are unstyled by default — use the official Tailwind
  plugin (`tailwindcss-react-aria-components`) for data-attribute variants.
- **Ark UI** has the broadest framework coverage but smaller component set —
  pick when targeting Vue/Svelte alongside React.
- **Headless UI** is Tailwind Labs' own — fewer components than Radix, simpler
  API. Pick if you want fewer dependencies.

## Sources

- [shadcn/ui docs](https://ui.shadcn.com/)
- [shadcn/ui components list](https://ui.shadcn.com/docs/components)
- [Radix UI primitives](https://www.radix-ui.com/primitives)
- [react-aria-components](https://react-spectrum.adobe.com/react-aria/components.html)
- [Ark UI](https://ark-ui.com/)
- [Headless UI](https://headlessui.com/)
- [Sonner (toast)](https://sonner.emilkowal.ski/)
- [cmdk (Command)](https://cmdk.paco.me/)
- [shadcn — copy-paste philosophy explained](https://shadcn.com/) — author posts
