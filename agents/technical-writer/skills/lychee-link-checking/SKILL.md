---
name: lychee-link-checking
description: Fast, modern link checker for docs and markdown — Lychee (Rust). JSON output for CI, custom exclusion patterns, fragment + self-hosted checking, GitHub Action integration. Use whenever auditing or gating a docs PR for broken links.
---

# Lychee Link Checking

Lychee is the 2026 SOTA link checker for docs-as-code. Written in Rust, it processes thousands of links per second, supports markdown / HTML / plain text / OpenAPI / GitHub Actions YAML, and emits JSON for CI gates. It replaces html-proofer, markdown-link-check, and awesome_bot.

## When to use this skill

- Audit existing docs for broken links (one-shot).
- CI gate on every docs PR.
- Verify external links + internal anchors + fragment IDs.
- Check links in mixed-content repos (markdown + HTML + YAML).

## Setup

### Install

```bash
# Option A — release binary (no compile)
curl -fsSL https://github.com/lycheeverse/lychee/releases/latest/download/lychee-x86_64-unknown-linux-gnu.tar.gz | tar xz
sudo mv lychee /usr/local/bin/

# Option B — cargo
cargo install lychee

# Option C — brew
brew install lychee

# Option D — Docker
docker run --rm -v "$PWD":/app lycheeverse/lychee:latest /app

lychee --version
```

### Optional: project config

`lychee.toml`:

```toml
# Files / globs to check
include = ["**/*.md", "**/*.html"]

# Files / globs to skip
exclude_path = ["node_modules", ".git", "dist", "target"]

# URL exclusions (regex)
exclude = [
  "https://example.com",
  "https://twitter.com/.*",   # often rate-limited
  "^https?://localhost",
]

# Behavior
max_redirects = 5
max_concurrency = 64
timeout = 20
retry_wait_time = 2

# Network
accept = ["200..=299", "403"]  # 403 OK for paywalled / login-gated
scheme = ["https", "http"]
require_https = false

# Caching
cache = true
max_cache_age = "1d"

# Auth
basic_auth = []
github_token = "env:GITHUB_TOKEN"

# Fragment checking (anchors)
include_fragments = true
```

## Common recipes

### Recipe 1: Audit current directory

```bash
lychee .
```

### Recipe 2: JSON output for parsing

```bash
lychee --format json --output report.json .
jq '.fail_map' report.json    # only failed URLs
```

### Recipe 3: Markdown only, exclude vendored content

```bash
lychee --include-path "docs/**/*.md" --exclude-path "docs/vendor/**" .
```

### Recipe 4: CI gate (GitHub Actions)

```yaml
# .github/workflows/links.yml
name: Link check
on:
  pull_request:
    paths: ['docs/**', '**/*.md']
  schedule:
    - cron: '0 6 * * 1'   # weekly Monday
jobs:
  lychee:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: lycheeverse/lychee-action@v2
        with:
          args: --verbose --no-progress --format json --output report.json 'docs/**/*.md' '*.md'
          fail: true
          token: ${{ secrets.GITHUB_TOKEN }}
      - if: always()
        uses: actions/upload-artifact@v4
        with:
          name: link-check-report
          path: report.json
```

### Recipe 5: Check the deployed site (not just markdown source)

```bash
lychee --base-url https://docs.example.com https://docs.example.com/sitemap.xml
# or crawl
lychee --remap "https://docs.example.com,/" public/
```

### Recipe 6: Fragment (anchor) checking

```bash
lychee --include-fragments docs/
# Catches:
#   [link](./other-page.md#section-that-doesnt-exist)
```

This is the highest-signal check for docs sites — typos in anchors are invisible until someone clicks.

### Recipe 7: Excluding social / rate-limited domains

In `lychee.toml`:

```toml
exclude = [
  "twitter.com",
  "x.com",
  "linkedin.com",
  "discord.gg",
  "^https?://localhost",
  "^mailto:",
]
```

Or per-run: `lychee --exclude twitter.com .`.

### Recipe 8: Self-hosted/internal-network links

```bash
lychee --insecure --header "Authorization: Bearer $INTERNAL_TOKEN" \
  --include "https://internal.example.com/.*" .
```

### Recipe 9: Performance — cache + concurrency

```bash
lychee --cache --max-cache-age 1d --max-concurrency 64 .
```

The cache persists in `.lycheecache` (gitignore it). Cache hits skip the network entirely.

## Reading JSON output

```jsonc
{
  "total":   3421,
  "successful": 3398,
  "fail_map": {
    "docs/api.md": [
      { "url": "https://broken.example.com", "status": { "code": 404 } }
    ]
  },
  "errors":  ["..."]
}
```

CI gate pattern: fail if `fail_map` is non-empty (the action does this with `fail: true`).

## Edge cases

- **GitHub rate limits:** Provide `--token` (or `GITHUB_TOKEN`) — Lychee uses it for the GitHub API to avoid 60-req/hour anonymous limit.
- **Cloudflare-protected docs:** add `--user-agent "Mozilla/5.0 (compatible; lychee/0.x)"`.
- **Mailto and tel: schemes:** included by default; exclude with `--exclude-mail` or `exclude = ["^mailto:"]`.
- **Private repos / authenticated docs:** pass `--basic-auth user:token` per host.
- **Markdown reference-style links:** Lychee handles `[ref]: https://...` definitions natively.
- **HTML+JS rendered sites:** Lychee does NOT execute JS. For SPA crawling, build the static export first (`mintlify deploy`, `mkdocs build`) and run Lychee against the built HTML.
- **Slow runs locally:** enable `--cache`; reduce `--max-concurrency` if hitting rate limits.

## Pairs well with

- `vale-prose-linting` — linguistic linting.
- `pa11y-axe-accessibility-audit` — WCAG audit (Lychee handles link reachability; pa11y handles a11y).
- `markdownlint-cli2` — markdown structure.

## Sources

- Lychee: https://github.com/lycheeverse/lychee
- lychee-action: https://github.com/lycheeverse/lychee-action
- Lychee docs: https://lychee.cli.rs/
