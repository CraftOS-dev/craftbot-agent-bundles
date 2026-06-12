---
name: log4brains-adr-management
description: Modern ADR workflow with Log4brains (visual site + CLI + git-log inference), MADR 4.0 template, Y-statement variants, and adr-kit for CI validation/indexing. Use when authoring or maintaining Architecture Decision Records.
---

# Log4brains ADR Management

Log4brains is the 2026 leader for ADR tooling because it ships a visual site (browse / search / filter), a CLI (`log4brains new`), and git-log metadata inference (auto-detects authors, dates, file paths). It supports MADR 4.0 (the current ADR markdown standard) and supersession links.

For CI-side validation + MADR enforcement + indexing, pair with `adr-kit` (kschlt). For legacy projects already using `adr-tools` (npryce), see the migration recipe below.

## When to use this skill

- The team wants ADRs in markdown alongside the code (docs-as-code).
- The team wants a browsable ADR site (Log4brains generates a Gatsby-based one).
- The team uses Conventional Commits and wants ADR metadata pulled from git automatically.
- The team is starting fresh OR migrating from `adr-tools`.

## Setup

### Install + initialize

```bash
# init in the repo (interactive — agent runs with --silent if scripting)
npx log4brains@latest init
```

The wizard asks for:

- ADR directory (default `docs/adr`)
- Project name
- Whether to include the welcome ADR

It writes `.log4brains.yml`:

```yaml
project:
  name: My project
  tz: Europe/Berlin
  adrFolder: ./docs/adr
```

### Install adr-kit for CI validation

```bash
pipx install adr-kit       # or: pip install adr-kit
adr-kit --version
```

## Common recipes

### Recipe 1: Author a new ADR

```bash
npx log4brains new
# prompts for: title, status, supersedes (if applicable)
```

The resulting file is `docs/adr/YYYYMMDD-<slug>.md` with the MADR 4.0 skeleton:

```markdown
---
status: proposed
date: 2026-06-09
deciders: [@alice, @bob]
consulted: [@carol]
informed: [@team-platform]
---

# Use PostgreSQL as primary database

## Context and Problem Statement

<!-- Why we needed to make a decision -->

## Decision Drivers

- ACID compliance for payment processing
- Complex query support for reporting
- Team familiarity

## Considered Options

- PostgreSQL
- MySQL
- MongoDB

## Decision Outcome

Chosen option: "PostgreSQL", because <reasons>.

### Consequences

- Good: single database handles transactions, search, geospatial.
- Bad: vertical scaling limits may require read replicas sooner.

## Pros and Cons of the Options

### PostgreSQL
- Good: ACID, JSONB, full-text search built-in.
- Bad: replication setup slightly more complex than MySQL.

### MySQL
- Good: familiar, simple replication.
- Bad: weaker JSON support.

### MongoDB
- Good: flexible schema, native JSON.
- Bad: no ACID for multi-document transactions.
```

### Recipe 2: Preview + build the ADR site

```bash
npx log4brains preview      # http://localhost:4004
npx log4brains build        # static site → ./.log4brains/out
```

Deploy `.log4brains/out` to GitHub Pages / Cloudflare Pages.

### Recipe 3: CI enforcement with adr-kit

```bash
adr-kit validate docs/adr/
adr-kit index docs/adr/ --output docs/adr/README.md
adr-kit lint docs/adr/ --check-supersession
```

CI workflow:

```yaml
# .github/workflows/adrs.yml
name: ADRs
on: [pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pipx install adr-kit
      - run: adr-kit validate docs/adr/
      - run: adr-kit lint docs/adr/ --check-supersession
```

### Recipe 4: Supersede an existing ADR

```bash
npx log4brains new --supersede docs/adr/20240115-mongodb-user-profiles.md
```

Log4brains links the new ADR to the old one and flips the old status to `superseded`. adr-kit's `--check-supersession` lint enforces that no `accepted` ADR contradicts an existing `accepted` one without superseding it.

### Recipe 5: Y-statement format (lightweight)

When the team wants a single-paragraph ADR:

```markdown
---
status: accepted
date: 2026-06-09
---

# API Gateway Selection

In the context of **building a microservices architecture**,
facing **the need for centralized API management, authentication, and rate limiting**,
we decided for **Kong Gateway**
and against **AWS API Gateway and custom Nginx solution**,
to achieve **vendor independence, plugin extensibility, and team familiarity with Lua**,
accepting that **we need to manage Kong infrastructure ourselves**.
```

### Recipe 6: Migrate from adr-tools (npryce)

`adr-tools` ADRs use `NNN-title.md` numbering and a slightly different template. Migration:

```bash
# 1. Rename files to Log4brains date-prefix convention
for f in docs/adr/[0-9]*-*.md; do
  date=$(git log --format=%cs --reverse "$f" | head -1 | tr -d -)
  mv "$f" "docs/adr/${date}-${f#*/[0-9]*-}"
done

# 2. Add YAML frontmatter (status/date/deciders) — script or hand-edit
# 3. Run adr-kit validate to catch any malformed entries
adr-kit validate docs/adr/
```

## When to write an ADR (vs skip)

| Write ADR | Skip ADR |
|---|---|
| New framework / library adoption | Patch-level dep updates |
| Database / queue / cache choice | Routine refactors |
| API design patterns | Bug fixes |
| Security architecture | Configuration tweaks |
| Integration patterns | Bikeshed-level naming |

## ADR lifecycle

```
Proposed → Accepted → Deprecated → Superseded
              ↓
           Rejected
```

Never edit an `accepted` ADR's decision. Write a new ADR that supersedes it.

## Edge cases

- **Multi-repo ADRs:** Log4brains is single-repo by default; for cross-repo decisions, keep ADRs in a dedicated `architecture` repo and reference them from product repos via permalink.
- **Long deciders list:** put the full list in frontmatter; the ADR site renders them as a chip group.
- **Diagrams in ADRs:** Mermaid and D2 both render inline in Log4brains; see `d2-mermaid-diagrams`.
- **Slack/Teams integration:** Log4brains has no native integration; pair with a CI step that posts new-ADR PRs to a channel.

## Sources

- Log4brains: https://github.com/thomvaill/log4brains
- adr-kit: https://github.com/kschlt/adr-kit
- MADR 4.0 template: https://adr.github.io/madr/
- adr-tools (legacy): https://github.com/npryce/adr-tools
