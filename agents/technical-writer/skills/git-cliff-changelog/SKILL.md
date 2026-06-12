---
name: git-cliff-changelog
description: Generate CHANGELOG.md from Conventional Commits with git-cliff — Rust-fast (~120ms for 10k commits), no Node dependency, full template control. Use when the user wants a fast, scriptable, language-agnostic changelog tool.
---

# git-cliff — Changelog Automation

git-cliff is the 2026 SOTA Conventional Commits → CHANGELOG.md generator. Written in Rust, it processes 10k commits in ~120ms and has zero runtime dependencies (no Node.js required). It supports Tera templates for arbitrary changelog shapes, monorepos, and integration with release-please / semantic-release.

## When to use this skill

- The user wants CHANGELOG.md from `git log` + Conventional Commits.
- The user is in a non-Node ecosystem (Python / Go / Rust / mixed) and doesn't want a Node dependency.
- The user wants a customizable changelog template (Keep a Changelog, Angular, GitLab-style, etc).
- The user wants integration with release tooling (release-please, semantic-release, goreleaser).

**Pair with:** `release-please-automation` for full release-PR automation. git-cliff handles the changelog rendering; release-please handles the release-PR + tag + GitHub Release.

## Setup

### Install

```bash
# Option A — pipx (Python-managed, no compile)
pipx install git-cliff

# Option B — cargo (latest)
cargo install git-cliff

# Option C — brew
brew install git-cliff

# Option D — release binary
curl -fsSL https://github.com/orhun/git-cliff/releases/latest/download/git-cliff-x86_64-unknown-linux-gnu.tar.gz | tar xz
sudo mv git-cliff /usr/local/bin/

git-cliff --version
```

### Initialize config

```bash
git-cliff --init
```

Writes `cliff.toml` with the default Keep a Changelog template. Edit to taste.

## Common recipes

### Recipe 1: Generate CHANGELOG.md from scratch

```bash
git-cliff -o CHANGELOG.md
```

### Recipe 2: Append the latest release only

```bash
git-cliff --unreleased --tag v1.4.0 --prepend CHANGELOG.md
```

### Recipe 3: Bump version + tag + changelog in one shot

```bash
git-cliff --bump --tag-pattern "v[0-9]*"
# detects next version from commits (feat → minor, fix → patch, breaking → major)
```

### Recipe 4: Monorepo per-package changelogs

```bash
git-cliff --include-path "packages/api/**" -o packages/api/CHANGELOG.md
git-cliff --include-path "packages/web/**" -o packages/web/CHANGELOG.md
```

### Recipe 5: GitHub Actions integration

```yaml
# .github/workflows/changelog.yml
name: Update CHANGELOG
on:
  push:
    tags: ['v*']
jobs:
  changelog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: orhun/git-cliff-action@v3
        with:
          config: cliff.toml
          args: --latest --strip header
        env:
          OUTPUT: CHANGELOG.md
      - uses: peter-evans/create-pull-request@v6
        with:
          title: 'docs(changelog): update for ${{ github.ref_name }}'
          commit-message: 'docs(changelog): update for ${{ github.ref_name }}'
          branch: changelog-update
```

### Recipe 6: Custom template (Tera)

Snippet of `cliff.toml`:

```toml
[changelog]
header = """
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
"""

body = """
{% if version %}\
    ## [{{ version | trim_start_matches(pat="v") }}] - {{ timestamp | date(format="%Y-%m-%d") }}
{% else %}\
    ## [Unreleased]
{% endif %}\
{% for group, commits in commits | group_by(attribute="group") %}
    ### {{ group | upper_first }}
    {% for commit in commits %}
        - {{ commit.message | upper_first }}{% if commit.github.pr_number %} ([#{{ commit.github.pr_number }}]({{ commit.github.pr_url }})){% endif %}
    {% endfor %}
{% endfor %}\n
"""

[git]
conventional_commits = true
filter_unconventional = true
commit_parsers = [
  { message = "^feat",     group = "Added" },
  { message = "^fix",      group = "Fixed" },
  { message = "^docs",     group = "Documentation" },
  { message = "^perf",     group = "Performance" },
  { message = "^refactor", group = "Refactored" },
  { message = "^style",    group = "Style", skip = true },
  { message = "^test",     group = "Tests", skip = true },
  { message = "^chore",    skip = true },
  { body = ".*security",   group = "Security" },
]
filter_commits = true
tag_pattern = "v[0-9].*"
```

### Recipe 7: GitHub integration (commit → PR link)

```toml
[remote.github]
owner = "acme"
repo  = "api"
```

Then commits show as ` ([#123](https://github.com/acme/api/pull/123))` in the rendered changelog. Requires `GITHUB_TOKEN` in env for unauthenticated rate limits.

## Conventional Commits cheat sheet

| Type | Section in CHANGELOG | SemVer bump |
|---|---|---|
| `feat` | Added | minor |
| `fix` | Fixed | patch |
| `perf` | Performance | patch |
| `docs` | Documentation | none |
| `refactor` | Refactored | none |
| `revert` | Reverted | patch |
| `chore` | (skipped) | none |
| `feat!` / `BREAKING CHANGE:` | **Breaking** | major |

## Edge cases

- **Pre-existing CHANGELOG.md (non-cliff format):** `--prepend` preserves the header; commit before regenerating to allow rollback.
- **Squash merges:** Conventional Commits messages must be on the merge commit. Configure GitHub: Repo Settings → "Default to PR title for squash merges" → ON.
- **Monorepo + release-please:** let release-please own the release-PR; git-cliff renders the per-package changelog inside that PR via an action step.
- **Pre-release tags (v2.0.0-rc.1):** add `tag_pattern = "v[0-9].*"` and `--bump --tag v2.0.0-rc.2` to bump pre-releases.
- **No commits yet:** git-cliff exits 0 with empty output; do not gate CI on non-empty output.

## Sources

- git-cliff: https://github.com/orhun/git-cliff
- git-cliff docs: https://git-cliff.org/docs/
- git-cliff-action: https://github.com/orhun/git-cliff-action
- Conventional Commits: https://www.conventionalcommits.org/
- Keep a Changelog: https://keepachangelog.com/en/1.1.0/
