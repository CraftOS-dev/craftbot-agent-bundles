---
name: release-please-automation
description: End-to-end release automation with Google's release-please — auto-PR with SemVer bump, CHANGELOG diff, and tag on merge. Conventional Commits + SemVer + GitHub Releases. Use when the user wants a fully automated release pipeline.
---

# release-please — Release Automation

`release-please` is Google's release-PR automation. It watches commits on the default branch, opens (and continuously updates) a "release PR" that bumps the version, regenerates CHANGELOG.md, and creates a GitHub Release + git tag when the PR merges. SemVer bumps follow Conventional Commits (feat → minor, fix → patch, breaking → major).

## When to use this skill

- The user wants zero-touch releases — merge feature PRs, get a release PR for free.
- The user uses GitHub.
- The repo uses Conventional Commits (or can adopt them).
- The user wants per-language version files updated automatically (`package.json`, `pyproject.toml`, etc).

**Pair with:** `git-cliff-changelog` if the team wants more control over CHANGELOG rendering — release-please can call git-cliff or use its built-in renderer.

## Setup

### Minimal — single package, npm

```yaml
# .github/workflows/release-please.yml
name: release-please
on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - uses: googleapis/release-please-action@v4
        with:
          release-type: node          # auto-bumps package.json + CHANGELOG.md
          token: ${{ secrets.GITHUB_TOKEN }}
```

That's it. On the next push to `main`, release-please opens a PR titled `chore(main): release 1.2.0`. Merging the PR creates the release.

### Multi-language single repo

```yaml
- uses: googleapis/release-please-action@v4
  with:
    release-type: python            # uses pyproject.toml
    token: ${{ secrets.GITHUB_TOKEN }}
```

Supported `release-type`:

- `node` (package.json)
- `python` (pyproject.toml / setup.py)
- `go`
- `rust` (Cargo.toml)
- `java` (Maven/Gradle)
- `php`, `ruby`, `terraform-module`, `helm`, `dart`, `simple` (plain VERSION file)

### Monorepo (manifest mode)

`release-please-config.json`:

```json
{
  "packages": {
    "packages/api":    { "release-type": "node",   "package-name": "@acme/api" },
    "packages/web":    { "release-type": "node",   "package-name": "@acme/web" },
    "services/worker": { "release-type": "python", "package-name": "acme-worker" }
  },
  "release-type": "node",
  "bump-minor-pre-major": true,
  "bump-patch-for-minor-pre-major": true,
  "changelog-sections": [
    { "type": "feat",     "section": "Features" },
    { "type": "fix",      "section": "Bug Fixes" },
    { "type": "perf",     "section": "Performance" },
    { "type": "deps",     "section": "Dependencies" },
    { "type": "docs",     "section": "Documentation", "hidden": false },
    { "type": "chore",    "hidden": true },
    { "type": "refactor", "section": "Code Refactoring", "hidden": false }
  ]
}
```

`.release-please-manifest.json` (initial state — release-please updates this):

```json
{
  "packages/api":    "1.0.0",
  "packages/web":    "0.5.0",
  "services/worker": "2.1.3"
}
```

Workflow:

```yaml
- uses: googleapis/release-please-action@v4
  with:
    config-file: release-please-config.json
    manifest-file: .release-please-manifest.json
    token: ${{ secrets.GITHUB_TOKEN }}
```

## Conventional Commits → SemVer mapping

| Commit | Effect on next release |
|---|---|
| `feat: ...` | minor bump (or patch if pre-1.0 with `bump-minor-pre-major`) |
| `fix: ...` | patch bump |
| `feat!: ...` or footer `BREAKING CHANGE:` | major bump |
| `docs:`, `chore:`, `test:`, `style:`, `ci:` | no bump (still appears in changelog if `hidden: false`) |
| `perf:` | patch bump |

## Common recipes

### Recipe 1: Publish to npm after merge

```yaml
# .github/workflows/release-please.yml
- uses: googleapis/release-please-action@v4
  id: release
  with:
    release-type: node
    token: ${{ secrets.GITHUB_TOKEN }}

- if: ${{ steps.release.outputs.release_created }}
  uses: actions/setup-node@v4
  with: { node-version: 20, registry-url: 'https://registry.npmjs.org' }

- if: ${{ steps.release.outputs.release_created }}
  run: npm ci && npm publish --provenance --access public
  env:
    NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### Recipe 2: Publish to PyPI after merge

```yaml
- if: ${{ steps.release.outputs.release_created }}
  uses: actions/setup-python@v5
  with: { python-version: '3.12' }
- if: ${{ steps.release.outputs.release_created }}
  run: |
    pip install uv
    uv build
    uv publish --token ${{ secrets.PYPI_TOKEN }}
```

### Recipe 3: Custom changelog (delegate to git-cliff)

`release-please-config.json`:

```json
{
  "changelog-host": "https://github.com",
  "changelog-type": "github",
  "extra-files": ["src/version.ts"]
}
```

For richer customization, render with git-cliff in a separate step that runs after release-please opens its PR (see `git-cliff-changelog`).

### Recipe 4: Skip release for a commit

Add `Release-As: skip` to the commit footer, or use `--skip-ci` in the PR title.

### Recipe 5: Pre-release / RC versions

```bash
git commit -m "chore: release v2.0.0-rc.1

Release-As: 2.0.0-rc.1"
```

release-please will use that exact version on the next release-PR.

### Recipe 6: Hotfix to a previous major

Target a release branch (`release-1.x`) instead of `main`:

```yaml
on:
  push:
    branches: [main, 'release-*']
```

release-please handles each branch independently.

## Edge cases

- **Squash vs merge commits:** release-please prefers squash merges. Configure GitHub: Settings → Pull Requests → "Allow squash merging" + "Default to PR title".
- **First-time setup:** release-please needs at least one Conventional Commit on `main` to open the first release PR.
- **Manual version bump:** add a commit with `Release-As: 3.0.0` footer.
- **Migrating from semantic-release:** delete `.releaserc.yml`, install release-please action; the next push opens a release PR at your current version.
- **Tags created locally:** release-please owns tags. Don't create them manually after adoption.
- **Multiple package managers in one repo:** use manifest mode; each path gets its own `release-type`.

## release-please vs git-cliff (decision rule)

| Need | Use |
|---|---|
| Full release-PR + tag + GitHub Release on merge | release-please |
| Pure CHANGELOG rendering, scriptable, fast | git-cliff |
| Both (CHANGELOG by git-cliff, release flow by release-please) | both, with git-cliff invoked from the release-please workflow |

## Sources

- release-please: https://github.com/googleapis/release-please
- release-please-action: https://github.com/googleapis/release-please-action
- Conventional Commits: https://www.conventionalcommits.org/
- SemVer: https://semver.org/
