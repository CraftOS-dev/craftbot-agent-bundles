---
name: sphinx-typedoc-reference-docs
description: Auto-generated language-native reference docs — Sphinx + sphinx-autodoc-typehints (Python), TypeDoc (TypeScript), Doxygen (C/C++), `cargo doc`/rustdoc (Rust). Pick by language; never hand-write reference docs that can be generated.
---

# Sphinx / TypeDoc / Doxygen / rustdoc — Reference Doc Generators

Reference docs are the lowest-leverage place to spend writer effort. Use language-native generators that extract docstrings, comments, and type information directly from source. The agent picks by language:

| Language | Generator | Install |
|---|---|---|
| Python | Sphinx + `sphinx-autodoc-typehints` + Furo theme | `uv add sphinx furo sphinx-autodoc-typehints myst-parser` |
| TypeScript / JavaScript | TypeDoc | `npm i -D typedoc` |
| C / C++ | Doxygen | `brew install doxygen` |
| Rust | rustdoc (built-in) | `cargo doc` |
| Go | `pkgsite` / `pkg.go.dev` | `go install golang.org/x/pkgsite/cmd/pkgsite@latest` |
| Java | Javadoc | shipped with JDK |
| Kotlin | Dokka | gradle plugin |
| Swift | DocC | `xcodebuild docbuild` |

## When to use this skill

- Authoring reference docs for a library or API surface.
- Setting up the docs build for a new project.
- Migrating from hand-written reference pages to generated ones.

## Setup — Python (Sphinx)

```bash
uv add --dev sphinx furo sphinx-autodoc-typehints myst-parser sphinx-copybutton
uv run sphinx-quickstart docs --quiet \
  --project="Acme API" \
  --author="Acme" \
  --release="1.0.0" \
  --language=en \
  --makefile --no-batchfile
```

Edit `docs/conf.py`:

```python
import os, sys
sys.path.insert(0, os.path.abspath("../src"))

project = "Acme API"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",          # Google + NumPy docstrings
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "myst_parser",                   # markdown alongside .rst
]

autosummary_generate = True
autodoc_typehints = "description"   # render hints in description, not signature
autodoc_member_order = "bysource"
napoleon_google_docstring = True

html_theme = "furo"
html_title = f"{project} {release}"

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "httpx":  ("https://www.python-httpx.org/", None),
}

myst_enable_extensions = ["colon_fence", "deflist", "tasklist"]
```

`docs/index.md`:

```markdown
# Acme API reference

```{toctree}
:maxdepth: 2

api/index
```
```

`docs/api/index.md`:

````markdown
# Modules

```{autosummary}
:toctree: generated
:recursive:

acme
acme.client
acme.orders
acme.exceptions
```
````

Build:

```bash
uv run sphinx-build -b html docs/ docs/_build/
# live reload
uv add --dev sphinx-autobuild
uv run sphinx-autobuild docs/ docs/_build/ --open-browser
```

## Setup — TypeScript (TypeDoc)

```bash
npm i -D typedoc
```

`typedoc.json`:

```json
{
  "$schema": "https://typedoc.org/schema.json",
  "entryPoints": ["src/index.ts"],
  "entryPointStrategy": "expand",
  "out": "docs/api",
  "tsconfig": "tsconfig.json",
  "excludePrivate": true,
  "excludeInternal": true,
  "excludeExternals": true,
  "includeVersion": true,
  "categorizeByGroup": true,
  "navigation": { "includeCategories": true, "includeGroups": true },
  "plugin": ["typedoc-plugin-markdown"]
}
```

```bash
# HTML output
npx typedoc
# Markdown output (drop into Docusaurus/Starlight)
npx typedoc --plugin typedoc-plugin-markdown --out docs/api
```

## Setup — C/C++ (Doxygen)

```bash
brew install doxygen graphviz       # graphviz for diagrams
doxygen -g                          # generates Doxyfile
```

Edit `Doxyfile`:

```
PROJECT_NAME           = "Acme C++ SDK"
INPUT                  = src/
RECURSIVE              = YES
EXTRACT_ALL            = NO
EXTRACT_PRIVATE        = NO
GENERATE_HTML          = YES
GENERATE_LATEX         = NO
HAVE_DOT               = YES        # call graphs via graphviz
UML_LOOK               = YES
HTML_OUTPUT            = docs/api
WARN_AS_ERROR          = YES        # fail CI on missing doc comments
```

```bash
doxygen
```

For modern HTML output, use **doxygen-awesome-css** theme:

```bash
git clone https://github.com/jothepro/doxygen-awesome-css.git docs/theme
# in Doxyfile:
#   HTML_EXTRA_STYLESHEET = docs/theme/doxygen-awesome.css
```

## Setup — Rust (rustdoc)

```bash
cargo doc --no-deps --document-private-items=false
# open in browser
cargo doc --open
```

Best practices:

```rust
//! # Acme SDK
//!
//! Quick start:
//! ```
//! use acme::Client;
//! let c = Client::new("sk_test_...");
//! ```

/// Creates a new order.
///
/// # Errors
///
/// Returns [`Error::Validation`] if `items` is empty.
///
/// # Examples
///
/// ```
/// # use acme::Client;
/// # let client = Client::new("sk_test_...");
/// let order = client.create_order(/* ... */).await?;
/// ```
pub async fn create_order(&self, req: CreateOrderRequest) -> Result<Order, Error> { /* ... */ }
```

rustdoc executes the `# Examples` doctest blocks during `cargo test --doc`.

## Common recipes (cross-language)

### Recipe 1: Wire into the docs site

| Target site | Mechanism |
|---|---|
| Docusaurus | Sphinx HTML → `static/`, TypeDoc markdown plugin → `docs/api/` |
| Starlight | TypeDoc markdown → `src/content/docs/api/` |
| MkDocs Material | `mkdocstrings[python]` is alternative to Sphinx for MkDocs sites |
| VitePress | TypeDoc markdown → `docs/api/` |
| Mintlify | TypeDoc markdown → `api-reference/`, Mintlify renders MDX directly |

### Recipe 2: CI gate — undocumented public API

Python:

```bash
uv run interrogate -v --fail-under=90 src/
```

TypeScript:

```bash
# TypeDoc with --treatWarningsAsErrors
npx typedoc --treatWarningsAsErrors
```

C++:

```
WARN_AS_ERROR = YES
```

Rust:

```bash
cargo doc --no-deps  # warns on missing docs
RUSTDOCFLAGS="-D missing_docs" cargo doc
```

### Recipe 3: Multi-version reference docs

Sphinx: `sphinx-multiversion` plugin OR check out each tag and build separately.

TypeDoc: build per-tag and deploy to `/<version>/` paths.

Rust: `docs.rs` auto-hosts every published crate version.

## Edge cases

- **Type hints inside docstrings (Sphinx):** prefer real Python type hints + `sphinx-autodoc-typehints` over `:type x: int` in docstring — the former renders cleaner and stays in sync with `mypy`.
- **TypeDoc with monorepo:** use `entryPoints: ["packages/*/src/index.ts"]` and `entryPointStrategy: "packages"`.
- **Doxygen with modern C++:** enable `BUILTIN_STL_SUPPORT = YES` for STL types in signatures.
- **rustdoc nightly features:** `cargo +nightly doc -Z rustdoc-scrape-examples` auto-scrapes example code from `examples/` into the docs.
- **Mixed-language repos:** generate each separately, then combine via the site's nav.

## Sources

- Sphinx: https://www.sphinx-doc.org/
- sphinx-autodoc-typehints: https://github.com/tox-dev/sphinx-autodoc-typehints
- Furo theme: https://github.com/pradyunsg/furo
- TypeDoc: https://typedoc.org/
- typedoc-plugin-markdown: https://typedoc-plugin-markdown.org/
- Doxygen: https://www.doxygen.nl/
- doxygen-awesome-css: https://github.com/jothepro/doxygen-awesome-css
- rustdoc: https://doc.rust-lang.org/rustdoc/
