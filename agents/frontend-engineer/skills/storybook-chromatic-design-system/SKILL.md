<!--
Source: https://storybook.js.org/ · https://www.chromatic.com/
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# Storybook 8 + Chromatic — Design system

Storybook 8 (April 2024) ships with Vite builder by default, has a first-class
Test addon, and pairs with Chromatic for visual regression in CI. The combo
gives you isolated component dev, docs, a11y checks, and pixel diffs on every PR.

## When to use

- Building a component library / design system
- Adding component documentation
- Visual regression CI for an app's UI
- Showing UI to designers/PMs in isolation
- Trigger phrases: "Storybook", "design system", "component library",
  "visual regression", "Chromatic", "Percy", "Autodocs", "CSF 3"

## Setup

```bash
# Bootstrap Storybook in an existing project
pnpm dlx storybook@latest init
# detects framework (React / Vue / Svelte / Angular / Web Components)

# Or upgrade from older Storybook
pnpm dlx storybook@latest upgrade

# Run locally
pnpm storybook              # default port 6006

# Visual regression
pnpm add -D @chromatic-com/storybook chromatic

# Additional addons
pnpm add -D @storybook/addon-a11y         # axe-core in Storybook
pnpm add -D @storybook/test-runner        # run play functions as Jest tests
```

Verify: `pnpm exec storybook --version` → 8.x.

Chromatic key:
- `CHROMATIC_PROJECT_TOKEN` — sign up at https://www.chromatic.com/ (free
  tier: 5,000 snapshots/month)

## Common recipes

### Recipe 1 — `main.ts` baseline

```ts
// .storybook/main.ts
import type { StorybookConfig } from "@storybook/react-vite";

const config: StorybookConfig = {
  stories: ["../src/**/*.mdx", "../src/**/*.stories.@(ts|tsx)"],
  addons: [
    "@storybook/addon-essentials",         // controls, actions, viewport, backgrounds
    "@storybook/addon-a11y",
    "@storybook/addon-interactions",
    "@chromatic-com/storybook",
  ],
  framework: { name: "@storybook/react-vite", options: {} },
  typescript: { reactDocgen: "react-docgen-typescript" },
  staticDirs: ["../public"],
};
export default config;
```

### Recipe 2 — `preview.ts` global decorators

```ts
// .storybook/preview.ts
import type { Preview } from "@storybook/react";
import "../src/styles/app.css";              // load Tailwind / globals

const preview: Preview = {
  parameters: {
    controls: { matchers: { color: /(background|color)$/i, date: /Date$/i } },
    backgrounds: {
      default: "light",
      values: [
        { name: "light", value: "#ffffff" },
        { name: "dark", value: "#0a0a0a" },
      ],
    },
    a11y: { config: { rules: [{ id: "color-contrast", enabled: true }] } },
  },
  globalTypes: {
    theme: {
      defaultValue: "light",
      toolbar: { items: ["light", "dark"], icon: "circlehollow" },
    },
  },
  decorators: [
    (Story, ctx) => (
      <div className={ctx.globals.theme === "dark" ? "dark" : ""}>
        <Story />
      </div>
    ),
  ],
};
export default preview;
```

### Recipe 3 — CSF 3 story (TypeScript-typed)

```tsx
// src/components/Button.stories.tsx
import type { Meta, StoryObj } from "@storybook/react";
import { Button } from "./Button";

const meta = {
  title: "Components/Button",
  component: Button,
  tags: ["autodocs"],          // enables MDX docs page
  args: { children: "Click me" },
  argTypes: {
    variant: { control: "select", options: ["primary", "ghost", "destructive"] },
    size: { control: "radio", options: ["sm", "md", "lg"] },
    onClick: { action: "clicked" },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = { args: { variant: "primary" } };
export const Ghost: Story = { args: { variant: "ghost" } };
export const Destructive: Story = { args: { variant: "destructive" } };
export const Large: Story = { args: { variant: "primary", size: "lg" } };
export const Disabled: Story = { args: { variant: "primary", disabled: true } };
```

### Recipe 4 — Interaction tests (play function)

```tsx
import { userEvent, within, expect } from "@storybook/test";
import type { Meta, StoryObj } from "@storybook/react";
import { LoginForm } from "./LoginForm";

const meta = { component: LoginForm } satisfies Meta<typeof LoginForm>;
export default meta;
type Story = StoryObj<typeof meta>;

export const HappyPath: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await userEvent.type(canvas.getByLabelText(/email/i), "user@example.com");
    await userEvent.type(canvas.getByLabelText(/password/i), "hunter2!");
    await userEvent.click(canvas.getByRole("button", { name: /sign in/i }));
    await expect(canvas.getByText(/welcome/i)).toBeInTheDocument();
  },
};
```

Run all play functions in CI:

```bash
pnpm exec test-storybook --ci
```

### Recipe 5 — Autodocs (auto-generated MDX from props)

Add `tags: ["autodocs"]` to a story's meta (Recipe 3) — Storybook generates a
docs page from JSDoc / TypeScript types.

```tsx
interface ButtonProps {
  /** Display variant of the button */
  variant?: "primary" | "ghost" | "destructive";
  /** Click handler */
  onClick?: () => void;
}
```

JSDoc descriptions appear in the props table.

### Recipe 6 — Custom MDX docs

```mdx
{/* src/components/Button.mdx */}
import { Meta, Story, Canvas, Controls } from "@storybook/blocks";
import * as ButtonStories from "./Button.stories";

<Meta of={ButtonStories} />

# Button

Standard button component used across the design system.

## Variants
<Canvas of={ButtonStories.Primary} />
<Canvas of={ButtonStories.Ghost} />

## Props
<Controls of={ButtonStories.Primary} />
```

### Recipe 7 — Chromatic CI (visual regression)

```yaml
# .github/workflows/chromatic.yml
name: Chromatic
on: { pull_request: {}, push: { branches: [main] } }
jobs:
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }     # required for baseline diffing
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with: { node-version: 22, cache: pnpm }
      - run: pnpm install --frozen-lockfile
      - uses: chromaui/action@latest
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          exitOnceUploaded: true     # don't wait for review
```

Each PR gets a Chromatic deployment with diffs to review. TurboSnap skips
unchanged stories (huge perf win).

### Recipe 8 — A11y addon in dev

The `@storybook/addon-a11y` panel shows axe-core findings per story. Configure
rules in `preview.ts` (Recipe 2). Fail CI if violations exist:

```ts
// .storybook/test-runner.ts
import type { TestRunnerConfig } from "@storybook/test-runner";
import { injectAxe, checkA11y } from "axe-playwright";

const config: TestRunnerConfig = {
  async preVisit(page) { await injectAxe(page); },
  async postVisit(page) { await checkA11y(page, "#storybook-root", { detailedReport: false }); },
};
export default config;
```

### Recipe 9 — Deploy Storybook (Chromatic or static)

```bash
# Chromatic hosts it for free
pnpm exec chromatic --project-token=$CHROMATIC_TOKEN

# OR static deploy
pnpm exec storybook build --output-dir storybook-static
pnpm dlx vercel deploy --prebuilt storybook-static
pnpm dlx netlify deploy --dir storybook-static
```

### Recipe 10 — Story per state, not per variant

```tsx
export const LoadingState: Story = { args: { isLoading: true } };
export const ErrorState: Story = { args: { error: new Error("Network") } };
export const EmptyState: Story = { args: { data: [] } };
export const HasData: Story = { args: { data: mockData } };
export const DisabledState: Story = { args: { disabled: true } };
```

One story per UI state → Chromatic catches state-specific regressions.

### Recipe 11 — Decorator wrappers (providers)

```tsx
// .storybook/preview.tsx
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });

export const decorators = [
  (Story) => <QueryClientProvider client={qc}><Story /></QueryClientProvider>,
];
```

## Examples

### Example 1: Bootstrap Storybook + Chromatic in a Next 15 + shadcn project

```bash
pnpm dlx storybook@latest init
# pick "Visual tests" addon when prompted (installs Chromatic addon)
pnpm exec chromatic --project-token=ckxxx --auto-accept-changes  # baseline
# commit + push; subsequent PRs get diff reviews
```

### Example 2: Catch a regression

1. Designer changes `Button` padding from `px-4` to `px-3`
2. PR opens; CI runs Chromatic
3. Chromatic posts PR comment with visual diffs of 7 stories that use Button
4. Reviewer accepts or rejects; the baseline updates on merge

## Edge cases / gotchas

- **CSF 3 stories must use the `satisfies` pattern** for full type safety —
  see Recipe 3.
- **`tags: ["autodocs"]`** is the v8 replacement for v7's `docs:
  { autodocs: true }`.
- **Vite builder is default** in Storybook 8 — webpack5 builder still exists
  but is slower; switch via `--builder=@storybook/builder-vite`.
- **Tailwind 4 + Storybook 8** — install `@tailwindcss/vite` and import
  `app.css` in `preview.ts`.
- **Chromatic TurboSnap** requires the build to embed the Webpack/Vite
  dependency graph — pass `--only-changed` to enable.
- **Stories with random data** flicker on Chromatic — use a fixed seed or
  freeze the date.
- **Animation timing** can cause diff false positives — set `delay: 500` per
  story or disable animations in Storybook (CSS `animation: none`).
- **`@storybook/test`** replaces `@storybook/jest` + `@storybook/testing-library`
  in v8.
- **CI runs `pnpm exec test-storybook`** — requires Storybook running OR
  `--config-dir` pointing to a built static site.
- **Storybook 9 alpha** is out (mid-2025); 8.x is the stable production
  recommendation through 2026.
- **Don't over-Storybook** — every isolated component is a maintenance cost.
  Prioritise components used in 3+ places.

## Sources

- [Storybook 8 announcement](https://storybook.js.org/blog/storybook-8/)
- [Storybook docs](https://storybook.js.org/docs/)
- [CSF 3 reference](https://storybook.js.org/docs/api/csf)
- [Chromatic docs](https://www.chromatic.com/docs/)
- [Chromatic TurboSnap](https://www.chromatic.com/docs/turbosnap/)
- [Storybook test-runner](https://storybook.js.org/docs/writing-tests/test-runner)
- [Storybook addon-a11y](https://storybook.js.org/addons/@storybook/addon-a11y)
- [Michael Chan — Storybook patterns (2025)](https://chan.dev/) — frequent posts
- [Chromatic free tier docs](https://www.chromatic.com/pricing) — 5k snapshots/month
