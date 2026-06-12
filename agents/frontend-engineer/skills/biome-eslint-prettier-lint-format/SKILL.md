<!--
Source: https://biomejs.dev/ · https://eslint.org/ · https://oxc.rs/
Authored: June 2026 for the frontend-engineer agent bundle.
-->

# Biome / ESLint 9 / Prettier — Lint + format

**Biome** (Rust) is the single-tool replacement for ESLint + Prettier — ~25x
faster, 95%+ Prettier-compatible. Use Biome for new projects. Stay on ESLint 9
(flat config required) + Prettier 3 only when you need a niche plugin Biome
doesn't have. Oxlint is the Rust ESLint-alternative if you want even faster
linting separate from formatting.

## When to use

- New project — Biome end-to-end
- Migrating an ESLint + Prettier project (one tool, one config)
- Speed regression in CI lint step
- Niche ESLint plugin requirement (Biome may not cover)
- Trigger phrases: "Biome", "ESLint", "Prettier", "lint", "format",
  "Oxlint", "flat config", "biome migrate"

## Decision tree

| Situation | Pick |
|---|---|
| Greenfield project, no exotic rules needed | **Biome** |
| Need a plugin Biome doesn't have (e.g., `eslint-plugin-storybook`) | **ESLint 9 + Prettier 3** |
| Want fastest lint, format unchanged | **Oxlint + Prettier 3** |
| Existing huge ESLint config that works | Stay on ESLint until you have a reason to move |

## Setup — Biome

```bash
pnpm add -D --save-exact @biomejs/biome

# Init config
pnpm dlx biome init

# Run
pnpm dlx biome check --write ./src
pnpm dlx biome check                     # CI gate (no writes)
pnpm dlx biome format --write ./src
pnpm dlx biome lint --write ./src
```

Verify: `pnpm dlx biome --version` → 1.9+ (June 2026).

## Setup — Migrate ESLint + Prettier → Biome

```bash
# 1. Install
pnpm add -D --save-exact @biomejs/biome

# 2. Run migrators (read .eslintrc + .prettierrc, emit biome.json)
pnpm dlx biome migrate eslint --write
pnpm dlx biome migrate prettier --write

# 3. Format + lint
pnpm dlx biome check --write .

# 4. Delete legacy configs once happy
git rm .eslintrc* .prettierrc* .eslintignore .prettierignore
pnpm remove eslint prettier $(pnpm list --depth 0 | grep eslint-)
```

Verify: `pnpm dlx biome check .` exits 0.

## Setup — ESLint 9 (flat config)

```bash
pnpm add -D eslint @eslint/js typescript-eslint
pnpm add -D eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-jsx-a11y
pnpm add -D eslint-config-prettier prettier
```

```ts
// eslint.config.ts
import js from "@eslint/js";
import ts from "typescript-eslint";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import jsxA11y from "eslint-plugin-jsx-a11y";
import prettier from "eslint-config-prettier";

export default ts.config(
  js.configs.recommended,
  ...ts.configs.strict,
  ...ts.configs.stylistic,
  react.configs.flat.recommended,
  react.configs.flat["jsx-runtime"],
  {
    plugins: { "react-hooks": reactHooks, "jsx-a11y": jsxA11y },
    rules: {
      ...reactHooks.configs.recommended.rules,
      ...jsxA11y.configs.recommended.rules,
      "react/prop-types": "off",       // TypeScript covers this
    },
    settings: { react: { version: "detect" } },
  },
  prettier,                            // last — disables stylistic rules Prettier owns
);
```

```js
// prettier.config.mjs
export default {
  semi: true,
  singleQuote: false,
  trailingComma: "all",
  printWidth: 100,
  tabWidth: 2,
};
```

## Common recipes — Biome

### Recipe 1 — `biome.json` baseline

```jsonc
{
  "$schema": "https://biomejs.dev/schemas/1.9.0/schema.json",
  "vcs": { "enabled": true, "clientKind": "git", "useIgnoreFile": true },
  "files": { "ignore": ["dist", "node_modules", ".next", "out", "storybook-static"] },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100,
    "lineEnding": "lf"
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "trailingCommas": "all",
      "semicolons": "always"
    }
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "a11y": { "useKeyWithClickEvents": "warn", "useValidAriaProps": "error" },
      "correctness": { "useExhaustiveDependencies": "error" },
      "suspicious": { "noExplicitAny": "warn", "noConsoleLog": "warn" },
      "style": { "noNonNullAssertion": "off" }
    }
  },
  "overrides": [
    { "include": ["*.tsx"], "linter": { "rules": { "style": { "noDefaultExport": "off" } } } }
  ]
}
```

### Recipe 2 — package.json scripts

```json
{
  "scripts": {
    "lint": "biome check .",
    "lint:fix": "biome check --write .",
    "format": "biome format --write .",
    "format:check": "biome format ."
  }
}
```

### Recipe 3 — Pre-commit with lefthook

```yaml
# lefthook.yml
pre-commit:
  parallel: true
  commands:
    biome:
      glob: "*.{js,jsx,ts,tsx,json,jsonc}"
      run: pnpm dlx biome check --write --no-errors-on-unmatched {staged_files}
      stage_fixed: true
```

```bash
pnpm add -D lefthook
pnpm exec lefthook install
```

Or with Husky + lint-staged:

```json
// package.json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx,json}": ["biome check --write --no-errors-on-unmatched"]
  }
}
```

### Recipe 4 — CI workflow

```yaml
# .github/workflows/ci.yml
- uses: biomejs/setup-biome@v2
  with: { version: latest }
- run: biome ci .
```

`biome ci` is optimized for CI — single pass, focused output, fails fast.

### Recipe 5 — Disable a single rule for one line

```tsx
// biome-ignore lint/suspicious/noExplicitAny: third-party API returns any
const data: any = await thirdParty.fetch();
```

### Recipe 6 — Per-file overrides

```jsonc
{
  "overrides": [
    {
      "include": ["**/*.test.ts", "**/*.spec.ts"],
      "linter": { "rules": { "suspicious": { "noExplicitAny": "off" } } }
    }
  ]
}
```

## Common recipes — ESLint 9

### Recipe 7 — Run lint

```bash
pnpm exec eslint . --max-warnings=0          # CI gate
pnpm exec eslint . --fix                     # auto-fix
pnpm exec eslint --print-config src/file.tsx # inspect effective config
```

### Recipe 8 — TypeScript ESLint with typed lint rules

```ts
// eslint.config.ts
export default ts.config(
  ...ts.configs.recommendedTypeChecked,    // requires type info
  {
    languageOptions: {
      parserOptions: {
        project: "./tsconfig.json",
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
);
```

Slower but catches type-aware bugs (`no-floating-promises`,
`no-misused-promises`).

## Common recipes — Oxlint

```bash
pnpm add -D oxlint
pnpm exec oxlint --import-plugin --tsconfig=tsconfig.json src
```

Oxlint runs the most common ESLint rules ~50-100x faster. Pairs well with
Prettier (Oxlint doesn't format). Good if you want fast lint but stay on
Prettier for formatting.

## Examples

### Example 1: Migrate a CRA project to Biome

```bash
pnpm add -D --save-exact @biomejs/biome
pnpm dlx biome migrate eslint --write
pnpm dlx biome migrate prettier --write
pnpm dlx biome check --write src/
# Remove eslint / prettier deps
pnpm remove eslint prettier $(pnpm list --depth 0 --json | jq -r '.[0].dependencies | keys[] | select(test("^(eslint|prettier)"))')
git rm .eslintrc* .prettierrc* .eslintignore .prettierignore
```

### Example 2: ESLint flat config from scratch

```bash
pnpm create eslint                       # interactive config generator (ESLint 9+)
pnpm exec eslint . --fix
```

## Edge cases / gotchas

- **Biome v1 doesn't cover every ESLint rule** — exotic plugins
  (`eslint-plugin-storybook`, `eslint-plugin-tailwindcss`) may still need
  ESLint. Run both side-by-side until parity.
- **`useExhaustiveDependencies`** is Biome's `react-hooks/exhaustive-deps` —
  keep it enabled.
- **Biome's `noConsoleLog`** flags `console.log` — disable for dev or use
  per-file overrides.
- **Biome and Prettier output match >95%** but not 100% — expect a tiny diff
  on first migration. Review and accept.
- **ESLint 9 dropped `.eslintrc.*`** — flat config (`eslint.config.{js,ts}`) is
  the only supported format.
- **`eslint-config-prettier`** must be LAST in the config array — disables
  conflicting stylistic rules.
- **Type-aware ESLint** is 5-10x slower than syntactic — restrict it to
  pre-commit and CI, not editor.
- **Editor integration** — install the official Biome / ESLint / Prettier
  extension in VS Code. Set
  `"editor.defaultFormatter": "biomejs.biome"`.
- **`pnpm dlx biome` vs `pnpm exec biome`** — `exec` uses the local install
  (deterministic version); `dlx` downloads each time.
- **Don't run both Biome and Prettier** — they fight. Pick one formatter.
- **Don't run both Biome lint and ESLint** unless you've planned which rules
  each handles. Most teams pick one.

## Sources

- [Biome docs](https://biomejs.dev/)
- [Biome migrate from ESLint](https://biomejs.dev/guides/migrate-eslint-prettier/)
- [Biome rule index](https://biomejs.dev/linter/rules/)
- [ESLint flat config docs](https://eslint.org/docs/latest/use/configure/configuration-files)
- [typescript-eslint](https://typescript-eslint.io/)
- [Oxlint](https://oxc.rs/docs/guide/usage/linter)
- [Prettier 3 docs](https://prettier.io/)
- [Why we built Biome (Oxc author response)](https://oxc.rs/) — comparison rationale
- [Biome vs ESLint benchmark (Anthony Fu, 2025)](https://antfu.me/) — recent benchmarks
