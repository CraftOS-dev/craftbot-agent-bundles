<!--
Source: https://commitizen-tools.github.io/commitizen/ · https://github.com/commitizen-tools/commitizen
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# commitizen — Conformant Commits + Semver Bump + CHANGELOG

`commitizen` enforces Conventional Commits 1.0 and automates semver bumps +
CHANGELOG generation directly from commit history. The 2026 default for any
project that ships a versioned package.

## When to use this skill

- New project setup — enforce Conventional Commits from day 1
- Migrating from manual version bumps
- Automating CHANGELOG generation
- CI release pipeline (cut version, write changelog, tag, push)
- Pre-commit hook for commit message validation
- Multi-package monorepo version coordination

Do NOT use commitizen when: project has no version (long-running service
that doesn't ship); team intentionally uses non-conventional commits;
release-please / standard-version already adopted (they overlap).

## Setup

```bash
uv add --dev commitizen
# OR ephemeral
uvx cz --version
```

```bash
uvx cz init
# Interactive setup — choose convention (`cz_conventional_commits` by default),
# version files, etc. Writes [tool.commitizen] in pyproject.toml.
```

## Common recipes

### Recipe 1 — Bootstrap config

```toml
# pyproject.toml
[tool.commitizen]
name = "cz_conventional_commits"
version = "0.1.0"
version_provider = "pep621"              # read from [project] version
version_files = [
    "src/my_pkg/__init__.py:__version__",
    "pyproject.toml:version",
]
update_changelog_on_bump = true
changelog_incremental = true
tag_format = "v$version"
major_version_zero = true                 # 0.x bumps stay in 0.x until 1.0
```

### Recipe 2 — Conformant commit (interactive)

```bash
uvx cz commit
# OR alias
uvx cz c
```

Walks you through:
1. Type: `fix`, `feat`, `chore`, `docs`, `style`, `refactor`, `perf`,
   `test`, `build`, `ci`, `revert`.
2. Scope: optional (`auth`, `db`, etc.).
3. Subject: short imperative summary.
4. Body: optional longer explanation.
5. Breaking change: yes/no — if yes, generates `BREAKING CHANGE:` footer.
6. Issue refs: optional `Closes #123`.

Resulting message:

```
feat(auth): add OAuth2 PKCE flow

Supports the public-client OAuth2 PKCE flow per RFC 7636.
BREAKING CHANGE: old `oauth2_callback` removed.

Closes #142
```

### Recipe 3 — Semver bump (automatic)

```bash
uvx cz bump
```

Reads git history since the last tag. Determines bump level:
- `feat` → minor
- `fix` / `perf` / `revert` → patch
- `BREAKING CHANGE:` footer → major

Bumps the version in all configured `version_files`, writes/updates
`CHANGELOG.md`, commits, tags. One command.

### Recipe 4 — Bump + CHANGELOG only (no commit / tag)

```bash
uvx cz bump --dry-run                   # preview
uvx cz changelog                        # write CHANGELOG without bumping
uvx cz bump --no-tag                    # bump + commit but no tag
uvx cz bump --files-only                # only update version files
```

### Recipe 5 — CI release pipeline

```yaml
# GitHub Actions — on push to main
name: Release
on:
  push:
    branches: [main]
jobs:
  release:
    runs-on: ubuntu-latest
    permissions: { contents: write }
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }       # need full history for cz
      - uses: astral-sh/setup-uv@v3
      - run: |
          git config user.name "release-bot"
          git config user.email "release-bot@noreply"
      - run: uvx cz bump --yes
      - run: git push --follow-tags
      # Optionally: build + publish to PyPI
      - run: uv build
      - run: uv publish --token ${{ secrets.PYPI_TOKEN }}
```

### Recipe 6 — Pre-commit hook (validate messages)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.13.0
    hooks:
      - id: commitizen
        stages: [commit-msg]
      - id: commitizen-branch
        stages: [pre-push]
```

```bash
uvx pre-commit install --hook-type commit-msg --hook-type pre-push
```

Now every commit message is validated; non-conformant messages are rejected
with a clear error.

### Recipe 7 — Customise the convention

For projects that need different commit types:

```toml
[tool.commitizen]
name = "cz_customize"

[tool.commitizen.customize]
message_template = "{{change_type}}{{scope}}: {{message}}"
example = "feat: add OAuth2 PKCE flow"
schema = "<type>(<scope>): <subject>"
schema_pattern = "(feat|fix|chore|docs|style|refactor|perf|test|build|ci|revert)(\\(.+\\))?:.+"

[[tool.commitizen.customize.questions]]
type = "list"
name = "change_type"
choices = [
    {value = "feat", name = "feat: A new feature"},
    {value = "fix", name = "fix: A bug fix"},
    {value = "ops", name = "ops: Operational change"},     # custom type
]
```

### Recipe 8 — Multi-package monorepo

```bash
# Per-package version bump
uvx cz bump --config packages/api/.cz.toml
uvx cz bump --config packages/cli/.cz.toml
```

Each package has its own `[tool.commitizen]` config; `cz` is invoked
per-package. Use `cz check --rev-range origin/main..HEAD` to validate
messages on the branch.

### Recipe 9 — Validate one or many commits

```bash
uvx cz check --rev-range HEAD~5..HEAD
uvx cz check --commit-msg-file .git/COMMIT_EDITMSG
```

Used in pre-commit and CI to fail bad messages early.

## Conventional Commits 1.0 cheat-sheet

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

Common types:

| Type | When | Semver |
|---|---|---|
| `feat` | new feature | minor |
| `fix` | bug fix | patch |
| `perf` | perf improvement | patch |
| `refactor` | code change, no feat/fix | none |
| `docs` | documentation | none |
| `style` | formatting | none |
| `test` | tests | none |
| `build` | build system | none |
| `ci` | CI config | none |
| `chore` | maintenance | none |
| `revert` | revert prior commit | patch |

Footers:
- `BREAKING CHANGE: <description>` → major bump
- `Closes #N`, `Refs #N` → issue linkage

## Edge cases

- **First release (0.0.0 → 0.1.0)**: `cz bump --increment minor` to seed.
- **Reset version**: `cz bump --increment major --increment-mode exact` to
  force a specific bump.
- **Skip CI loop**: use `[skip ci]` in the bump commit body if needed.
- **Custom version provider**: `version_provider = "scm"` to read from git
  tags directly (no version_files).
- **Pre-releases**: `cz bump --prerelease alpha --prerelease-offset 1` to
  cut `1.0.0-alpha1`.
- **Rebase conflicts**: avoid rebasing across a `cz bump` commit — the
  CHANGELOG diff is order-sensitive.
- **Branches with merge commits**: `cz check --rev-range` may flag merge
  messages. Set `bump_message = "bump: ..."` and exempt those.

## Comparison

| Tool | Notes |
|---|---|
| **commitizen** | most flexible, Python-native, multi-language support |
| release-please (Google) | GitHub-integrated, PR-based releases; great if you want PR review |
| standard-version (deprecated) | succeeded by release-please |
| semantic-release (npm) | Node-focused but works for Python |
| python-semantic-release | Python port of semantic-release; good alternative |

commitizen is the most-adopted Python-first option. For "release via PR"
workflow, release-please is more polished.

## Sources

- https://commitizen-tools.github.io/commitizen/ — full docs
- https://github.com/commitizen-tools/commitizen — source
- https://www.conventionalcommits.org/en/v1.0.0/ — Conventional Commits spec
- https://semver.org/ — Semantic Versioning 2.0
- https://keepachangelog.com/ — CHANGELOG format
