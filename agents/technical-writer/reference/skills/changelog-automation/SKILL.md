<!--
Source: https://github.com/wshobson/agents/blob/main/plugins/documentation-generation/skills/changelog-automation/SKILL.md
Repo: wshobson/agents
-->
---
name: changelog-automation
description: Automate changelog generation from commits, PRs, and releases following Keep a Changelog format. Use when setting up release workflows, generating release notes, or standardizing commit conventions.
---

# Changelog Automation

Patterns and tools for automating changelog generation, release notes, and version management following industry standards.

## When to Use This Skill

- Setting up automated changelog generation
- Implementing Conventional Commits
- Creating release note workflows
- Standardizing commit message formats
- Generating GitHub/GitLab release notes
- Managing semantic versioning

## Core Concepts

### Keep a Changelog Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
```

### Release Note Sections

**Summary** — short overview of release theme
**Highlights** — major features with emoji headers
**Breaking Changes** — explicitly called out
**Upgrade Guide** — what users need to do
**Known Issues** — flag with target fix version
**Dependencies Updated** — table of package updates

## Conventional Commits

### Commit Message Examples

```bash
# Feature with scope
feat(auth): add OAuth2 support for Google login

# Bug fix with issue reference
fix(checkout): resolve race condition in payment processing

Closes #123

# Breaking change
feat(api)!: change user endpoint response format

BREAKING CHANGE: The user endpoint now returns `userId` instead of `id`.
Migration guide: Update all API consumers to use the new field name.

# Multiple paragraphs
fix(database): handle connection timeouts gracefully

Previously, connection timeouts would cause the entire request to fail
without retry. This change implements exponential backoff with up to
3 retries before failing.

The timeout threshold has been increased from 5s to 10s based on p99
latency analysis.

Fixes #456
Reviewed-by: @alice
```

### Commit Types

| Type | Purpose | Triggers |
|---|---|---|
| `feat` | New feature | Minor version bump |
| `fix` | Bug fix | Patch version bump |
| `docs` | Documentation only | No version bump |
| `style` | Formatting, no code change | No version bump |
| `refactor` | Code restructuring | No version bump |
| `perf` | Performance improvement | Patch bump |
| `test` | Test additions/changes | No version bump |
| `build` | Build system / deps | No version bump |
| `ci` | CI config changes | No version bump |
| `chore` | Maintenance | No version bump |
| `revert` | Revert previous commit | Patch bump |
| `feat!` or `BREAKING CHANGE` | Breaking change | Major version bump |

## Best Practices

### Do's
- **Follow Conventional Commits** — enables automation
- **Write clear messages** — future you will thank you
- **Reference issues** — link commits to tickets
- **Use scopes consistently** — define team conventions
- **Automate releases** — reduce manual errors

### Don'ts
- Don't mix changes — one logical change per commit
- Don't skip validation — use commitlint
- Don't manual edit — generated changelogs only
- Don't forget breaking changes — mark with `!` or footer
- Don't ignore CI — validate commits in pipeline
