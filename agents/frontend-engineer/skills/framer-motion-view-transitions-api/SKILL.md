<!--
Source: https://motion.dev/ · https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# Animation — motion + View Transitions API

**motion** is the 2024+ name for Framer Motion — now framework-agnostic
(React, Vue, Svelte, vanilla JS). The browser-native **View Transitions API**
(cross-browser stable in 2024) handles cross-page and cross-element morphs with
zero JS. Use both together: View Transitions for navigation; motion for
declarative gesture / spring animation.

## When to use

- Page transitions in an MPA (Astro / multi-page) or App Router navigation
- Declarative animations with spring physics + gestures
- Reorderable lists, drag-and-drop, parallax
- Mobile-feel transitions (shared element morphs)
- Trigger phrases: "animation", "Framer Motion", "motion", "View Transitions",
  "spring", "drag", "AnimatePresence", "shared element"

## Setup

```bash
# motion (Framer rebrand) — React
pnpm add motion

# Vue
pnpm add motion-v

# Vanilla
pnpm add motion

# Auto-animate (list reorder, Formkit) — lightest possible option
pnpm add @formkit/auto-animate
```

Verify: `pnpm list motion` → 11.x or 12.x.

No API keys.

## Common recipes — motion

### Recipe 1 — Declarative animation

```tsx
import { motion } from "motion/react";

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3, ease: "easeOut" }}
>
  Hello
</motion.div>
```

### Recipe 2 — Spring physics

```tsx
<motion.div
  animate={{ x: 100 }}
  transition={{ type: "spring", stiffness: 260, damping: 20 }}
/>
```

### Recipe 3 — `AnimatePresence` for exit animations

```tsx
import { AnimatePresence, motion } from "motion/react";

function Modal({ open }: { open: boolean }) {
  return (
    <AnimatePresence>
      {open && (
        <motion.div
          key="modal"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          transition={{ duration: 0.2 }}
        >
          ...
        </motion.div>
      )}
    </AnimatePresence>
  );
}
```

### Recipe 4 — Drag gestures

```tsx
<motion.div
  drag
  dragConstraints={{ left: -100, right: 100, top: -100, bottom: 100 }}
  dragElastic={0.2}
  whileDrag={{ scale: 1.05 }}
/>

<motion.div
  drag="x"
  dragMomentum={false}
  onDragEnd={(_, info) => console.log("offset", info.offset.x)}
/>
```

### Recipe 5 — `layout` animations (reorder lists, accordion)

```tsx
import { motion, Reorder } from "motion/react";

function TodoList({ items, setItems }: { items: Todo[]; setItems: (t: Todo[]) => void }) {
  return (
    <Reorder.Group axis="y" values={items} onReorder={setItems}>
      {items.map((item) => (
        <Reorder.Item key={item.id} value={item} className="p-3 bg-white border rounded">
          {item.text}
        </Reorder.Item>
      ))}
    </Reorder.Group>
  );
}
```

### Recipe 6 — `whileHover` / `whileTap` / `whileInView`

```tsx
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
>
  Click me
</motion.button>

<motion.div
  initial={{ opacity: 0 }}
  whileInView={{ opacity: 1 }}
  viewport={{ once: true, amount: 0.3 }}
>
  Fades in once when 30% visible
</motion.div>
```

### Recipe 7 — Variants for orchestrating

```tsx
const container = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 },
  },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 },
};

<motion.ul variants={container} initial="hidden" animate="visible">
  {items.map((it) => (
    <motion.li key={it.id} variants={item}>{it.text}</motion.li>
  ))}
</motion.ul>
```

### Recipe 8 — `useScroll` + `useTransform` (scroll-driven)

```tsx
import { motion, useScroll, useTransform } from "motion/react";

function Parallax() {
  const { scrollY } = useScroll();
  const y = useTransform(scrollY, [0, 500], [0, -150]);
  return <motion.div style={{ y }}>Parallax</motion.div>;
}
```

### Recipe 9 — Shared layout (cross-component morph)

```tsx
{!isExpanded ? (
  <motion.div layoutId="card" onClick={() => setExpanded(true)} className="w-32 h-32 bg-blue-500" />
) : (
  <motion.div layoutId="card" onClick={() => setExpanded(false)} className="absolute inset-10 bg-blue-500" />
)}
```

The element morphs smoothly between layouts — same `layoutId` is the link.

## Common recipes — View Transitions API

### Recipe 10 — Single-page transition (DOM update)

```ts
async function navigate(href: string) {
  if (!document.startViewTransition) {
    // fallback for browsers without support
    location.assign(href);
    return;
  }
  document.startViewTransition(async () => {
    const html = await fetch(href).then((r) => r.text());
    document.documentElement.innerHTML = new DOMParser().parseFromString(html, "text/html").documentElement.innerHTML;
  });
}
```

### Recipe 11 — Named shared elements (CSS view transitions)

```css
/* Old page */
.hero {
  view-transition-name: hero;
}

/* New page — same name → automatic morph */
.product-image {
  view-transition-name: hero;
}

/* Customize the transition */
::view-transition-old(hero),
::view-transition-new(hero) {
  animation-duration: 300ms;
  animation-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Recipe 12 — Astro View Transitions

```astro
---
import { ClientRouter } from "astro:transitions";
---
<html>
  <head>
    <ClientRouter />
  </head>
  <body>
    <main transition:name="main">
      <slot />
    </main>
  </body>
</html>
```

Astro wires the View Transitions API automatically.

### Recipe 13 — Next 15 view transitions

```tsx
"use client";
import { useRouter } from "next/navigation";

const router = useRouter();

function navigate(href: string) {
  if (!document.startViewTransition) return router.push(href);
  document.startViewTransition(() => router.push(href));
}
```

Next 15.x has experimental built-in support — check
`experimental: { viewTransition: true }` in `next.config.ts`.

### Recipe 14 — Reduced motion

```tsx
import { useReducedMotion } from "motion/react";

function FadeIn({ children }) {
  const reduce = useReducedMotion();
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: reduce ? 0 : 0.4 }}
    >
      {children}
    </motion.div>
  );
}
```

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

Mandatory for WCAG compliance.

## Common recipes — AutoAnimate

### Recipe 15 — AutoAnimate (FormKit)

```tsx
import { useAutoAnimate } from "@formkit/auto-animate/react";

function TodoList({ items }: { items: Todo[] }) {
  const [parent] = useAutoAnimate();
  return (
    <ul ref={parent}>
      {items.map((t) => <li key={t.id}>{t.text}</li>)}
    </ul>
  );
}
```

One hook → smooth add/remove/reorder. Smallest API surface for simple cases.

## Examples

### Example 1: Page-transition morph between list + detail

```css
/* list page */
.product-card[data-id="42"] img { view-transition-name: product-42; }
```
```css
/* detail page */
.product-detail img { view-transition-name: product-42; }
```

Astro / Next router triggers a `document.startViewTransition` on navigation;
the browser morphs `product-42` between the two pages automatically.

### Example 2: Drag-to-reorder list with motion

```tsx
import { Reorder } from "motion/react";

const [items, setItems] = useState(initial);

<Reorder.Group axis="y" values={items} onReorder={setItems}>
  {items.map((i) => (
    <Reorder.Item key={i.id} value={i} whileDrag={{ scale: 1.02 }}>
      {i.text}
    </Reorder.Item>
  ))}
</Reorder.Group>
```

## Edge cases / gotchas

- **motion replaced Framer Motion** in 2024 — old `framer-motion` package is
  still maintained but new APIs land in `motion`.
- **`AnimatePresence` needs stable `key`** — without it, exit animation
  doesn't fire.
- **`layout` animations cause re-layouts** — slow on large lists; use
  `layout="position"` to constrain.
- **`useScroll` triggers reflows** — wrap heavy work in `useTransform`'s
  return path, not in `useEffect` reading `.get()`.
- **View Transitions are MPA + SPA capable** — `same-document` SPA needs
  `document.startViewTransition(callback)`; cross-document MPA needs
  `@view-transition { navigation: auto; }` in CSS (Chrome 126+).
- **Firefox support** for View Transitions landed late — check
  `caniuse.com/view-transitions`. Always feature-detect.
- **`view-transition-name` must be unique per element** at any time — if
  multiple elements have the same name, the API picks one (undefined which).
- **Reduced motion is non-negotiable** — every animation must respect
  `prefers-reduced-motion` or you fail WCAG 2.3.3.
- **GSAP** (paid for commercial — actually free since 2024) is still the
  gold standard for complex timeline animations. Use when motion can't do it.
- **Performance** — animate `transform` and `opacity`, never `width`/`height`/
  `top`/`left`. Stay on the compositor thread.
- **`will-change`** can hurt — only use on elements about to animate and
  remove after.

## Sources

- [motion docs (formerly Framer Motion)](https://motion.dev/)
- [View Transitions API — MDN](https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API)
- [View Transitions guide — Chrome](https://developer.chrome.com/docs/web-platform/view-transitions/)
- [@formkit/auto-animate](https://auto-animate.formkit.com/)
- [GSAP](https://gsap.com/)
- [Astro view transitions](https://docs.astro.build/en/guides/view-transitions/)
- [Next.js view transitions experiment](https://nextjs.org/docs/canary/app/api-reference/config/next-config-js/viewTransition)
- [Sam Selikoff — motion patterns (2025)](https://samselikoff.com/) — regular animation tutorials
- [Codrops — animation tutorials](https://tympanus.net/codrops/) — recent posts
