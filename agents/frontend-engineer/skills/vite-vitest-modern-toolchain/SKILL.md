<!--
Source: https://vitejs.dev/ · https://vitest.dev/
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# Vite 5/6 + Vitest 2 — Modern toolchain

Vite is the default bundler/dev server for SPAs and libraries. Vitest is the
Vite-native unit + integration test runner (jest-API compatible). Together they
form the fastest dev loop in the JS ecosystem outside Bun.

## When to use

- New SPA project (React, Vue, Svelte, Solid, vanilla TS)
- Library / SDK packaging (`vite build --mode lib` or `tsdown`)
- Migrating from webpack / CRA / Parcel
- Replacing Jest (Vite-native, faster, ESM-friendly, browser mode)
- Trigger phrases: "Vite", "Vitest", "Rollup", "HMR", "library build",
  "browser-mode test", "jest replacement"

## Setup

```bash
# New project
pnpm create vite@latest my-app
# choose: framework (vanilla / react / vue / svelte / solid / lit / qwik),
#         variant (ts / ts-swc)

cd my-app
pnpm install
pnpm dev          # instant HMR on port 5173

# Add Vitest to an existing Vite project
pnpm add -D vitest @vitest/ui happy-dom @testing-library/jest-dom

# Library mode bootstrap
pnpm add -D vite-plugin-dts        # emit .d.ts
```

Verify: `pnpm exec vite --version` → 6.x. Vitest: `pnpm exec vitest --version` → 2.x.

No API keys.

## Common recipes

### Recipe 1 — `vite.config.ts` baseline

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";

export default defineConfig({
  plugins: [react(), tsconfigPaths()],
  server: {
    port: 5173,
    proxy: { "/api": "http://localhost:8787" },
  },
  build: {
    target: "es2022",
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          react: ["react", "react-dom"],
          vendor: ["lodash-es", "date-fns"],
        },
      },
    },
  },
});
```

### Recipe 2 — Environment variables

```bash
# .env.local
VITE_API_URL=https://api.example.com
VITE_SENTRY_DSN=https://...
```

```ts
const apiUrl = import.meta.env.VITE_API_URL;
// MUST be prefixed VITE_ — anything else is dropped from the client bundle
```

For type safety:

```ts
// src/vite-env.d.ts
/// <reference types="vite/client" />
interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_SENTRY_DSN: string;
}
interface ImportMeta { readonly env: ImportMetaEnv; }
```

### Recipe 3 — Library mode (publish to npm)

```ts
// vite.config.ts
import { defineConfig } from "vite";
import dts from "vite-plugin-dts";

export default defineConfig({
  plugins: [dts({ rollupTypes: true })],
  build: {
    lib: {
      entry: "src/index.ts",
      formats: ["es", "cjs"],
      fileName: (format) => `index.${format === "es" ? "js" : "cjs"}`,
    },
    rollupOptions: {
      external: ["react", "react-dom"], // peer deps must be external
    },
  },
});
```

```json
// package.json
{
  "type": "module",
  "main": "./dist/index.cjs",
  "module": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": { "import": "./dist/index.js", "require": "./dist/index.cjs", "types": "./dist/index.d.ts" }
  },
  "files": ["dist"],
  "sideEffects": false
}
```

### Recipe 4 — Vitest config (single file)

```ts
// vite.config.ts (Vitest reads the same config)
/// <reference types="vitest" />
import { defineConfig } from "vite";

export default defineConfig({
  test: {
    environment: "happy-dom",      // or "jsdom", or "node"
    globals: true,                  // test/expect/describe as globals (jest-like)
    setupFiles: ["./src/test/setup.ts"],
    coverage: {
      provider: "v8",
      reporter: ["text", "html", "lcov"],
      thresholds: { lines: 80, functions: 80, branches: 75, statements: 80 },
    },
  },
});
```

```ts
// src/test/setup.ts
import "@testing-library/jest-dom/vitest";
import { afterEach } from "vitest";
import { cleanup } from "@testing-library/react";

afterEach(() => cleanup());
```

### Recipe 5 — Component test (React + Testing Library + Vitest)

```tsx
// src/components/Counter.test.tsx
import { test, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Counter } from "./Counter";

test("increments on click", async () => {
  const user = userEvent.setup();
  render(<Counter />);
  await user.click(screen.getByRole("button", { name: /increment/i }));
  expect(screen.getByText(/count: 1/i)).toBeInTheDocument();
});
```

### Recipe 6 — Vitest browser mode (component test in real browser)

```bash
pnpm add -D @vitest/browser playwright
pnpm exec playwright install chromium
```

```ts
// vitest.workspace.ts
import { defineWorkspace } from "vitest/config";

export default defineWorkspace([
  // unit tests in happy-dom
  { extends: "./vite.config.ts", test: { include: ["src/**/*.test.{ts,tsx}"], environment: "happy-dom" } },
  // browser tests in real Chromium
  {
    extends: "./vite.config.ts",
    test: {
      include: ["src/**/*.browser.test.{ts,tsx}"],
      browser: { enabled: true, provider: "playwright", instances: [{ browser: "chromium" }] },
    },
  },
]);
```

```bash
pnpm exec vitest --workspace=vitest.workspace.ts
```

### Recipe 7 — Run + watch + UI

```bash
pnpm exec vitest                           # watch mode (default)
pnpm exec vitest run                       # single-run (CI mode)
pnpm exec vitest --ui                      # browser UI dashboard
pnpm exec vitest --coverage                # coverage report
pnpm exec vitest src/components/Foo.test.ts  # narrow to one file
pnpm exec vitest -t "increments"           # filter by test name
```

### Recipe 8 — Mocking with MSW 2

```bash
pnpm add -D msw
pnpm dlx msw init public/ --save
```

```ts
// src/mocks/handlers.ts
import { http, HttpResponse } from "msw";

export const handlers = [
  http.get("/api/users/:id", ({ params }) => HttpResponse.json({ id: params.id, name: "Test" })),
];
```

```ts
// src/test/setup.ts
import { setupServer } from "msw/node";
import { handlers } from "../mocks/handlers";

const server = setupServer(...handlers);
beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### Recipe 9 — `vi.mock` for module mocks

```ts
import { vi, test, expect } from "vitest";
import * as analytics from "@/lib/analytics";

vi.mock("@/lib/analytics", () => ({ track: vi.fn() }));

test("track is called on submit", async () => {
  // ...
  expect(analytics.track).toHaveBeenCalledWith("submit", { id: 1 });
});
```

### Recipe 10 — Build + preview

```bash
pnpm exec vite build                      # outputs ./dist
pnpm exec vite preview --port 4173        # serve the production build locally
pnpm exec vite --debug                    # debug HMR + plugin chain
```

### Recipe 11 — Bundle analysis

```bash
pnpm add -D rollup-plugin-visualizer
```

```ts
// vite.config.ts
import { visualizer } from "rollup-plugin-visualizer";

export default defineConfig({
  plugins: [visualizer({ filename: "dist/stats.html", open: true, gzipSize: true })],
});
```

`pnpm build` opens an interactive treemap.

## Examples

### Example 1: Bootstrap a Vite + React + Vitest project

```bash
pnpm create vite@latest my-app --template react-ts
cd my-app
pnpm install
pnpm add -D vitest @vitest/ui happy-dom @testing-library/react @testing-library/user-event @testing-library/jest-dom
# Add `"test": "vitest"` and `"coverage": "vitest --coverage"` to package.json scripts
pnpm test
```

### Example 2: Migrate Jest → Vitest

```bash
# 1. Install Vitest
pnpm add -D vitest @vitest/ui happy-dom

# 2. Replace jest imports with vitest (codemod)
pnpm dlx jest-to-vitest "src/**/*.test.{ts,tsx}"

# 3. Move jest.config to vitest config under vite.config.ts test:
# 4. Remove jest, ts-jest, @types/jest from package.json
pnpm remove jest ts-jest @types/jest
```

API is near-identical: `describe`, `test`, `expect`, `vi` replaces `jest`.

## Edge cases / gotchas

- **Env vars must start with `VITE_`** — anything else is stripped. Use
  `envPrefix: ["VITE_", "PUBLIC_"]` to allow more.
- **`import.meta.env` is build-time** — for runtime vars (e.g., per-deployment),
  inject via `window.__CONFIG__` or fetch a config endpoint.
- **CJS deps need `optimizeDeps`** — Vite pre-bundles CJS to ESM. If a dep
  isn't being pre-bundled, add `optimizeDeps: { include: ["legacy-cjs-pkg"] }`.
- **Tailwind 4 with Vite** — use `@tailwindcss/vite` plugin, NOT PostCSS.
- **HMR breaks with side-effect imports** — modules with top-level side effects
  may need `if (import.meta.hot) import.meta.hot.accept(...)`.
- **`vitest --workspace`** is required when you have multiple projects in a
  monorepo with different configs.
- **Happy-dom vs jsdom** — happy-dom is faster but less complete. Switch to
  jsdom if a test needs `XPath`, full HTML parsing, or `localStorage` quirks.
- **Browser-mode tests are slower** — keep them for true integration; use
  happy-dom for the bulk of component tests.
- **`coverage.provider: "v8"`** is faster than `"istanbul"` but less accurate
  on branch coverage. Pick istanbul if branch fidelity matters.
- **`vite.config.ts` typed `test` block** requires `/// <reference types="vitest" />`
  or the type errors silently fail.

## Sources

- [Vite docs](https://vitejs.dev/)
- [Vitest docs](https://vitest.dev/)
- [Vite config reference](https://vitejs.dev/config/)
- [Vitest browser mode](https://vitest.dev/guide/browser/)
- [Vite library mode](https://vitejs.dev/guide/build.html#library-mode)
- [MSW v2 docs](https://mswjs.io/docs/)
- [Testing Library queries](https://testing-library.com/docs/queries/about)
- [Anthony Fu — State of Vite (2025)](https://antfu.me/) — frequent updates
