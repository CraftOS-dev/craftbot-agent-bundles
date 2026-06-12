<!--
Source: https://github.com/thomvaill/log4brains · https://adr.github.io/madr/
Authored: June 2026 for the senior-python-engineer agent bundle.
-->

# log4brains + MADR 4.0 — Architecture Decision Records

`log4brains` (Thomas Vaillant) is a CLI + visual web UI for managing
Architecture Decision Records (ADRs). MADR 4.0 (Markdown ADR) is the de
facto 2026 ADR format. Together: write decision records as Markdown,
preview them in a Vercel-style static site, link supersessions, infer
metadata from git.

Alternatives that fit the same niche: `adr-tools` (npryce, minimal shell),
`adr-kit` (kschlt, full Python toolkit with validation + indexing +
enforcement), or hand-authored Markdown if you don't want the tooling.

## When to use this skill

- Recording a load-bearing architectural decision (chose X over Y because Z)
- Documenting deprecations / migrations / supersessions
- Onboarding new engineers (browseable history of "why")
- Periodic architecture review (revisit superseded decisions)
- "Why is this code shaped this way?" lookups
- Compliance / audit trails for design decisions

Do NOT write an ADR for: small tactical choices ("renamed function X");
implementation details ("used a list here"); reversible choices made in
1-line PRs.

## Setup

```bash
# log4brains (Node-based — uses npx for ephemeral run)
npx log4brains init                          # interactive bootstrap
npm install --save-dev log4brains            # or persistent install

# Pure-CLI alternative
npx adr-tools init docs/adr

# Python toolkit alternative
pipx install adr-kit
adr-kit init
```

For Python-first projects, `adr-kit` keeps tooling inside the Python venv.

## MADR 4.0 template

```markdown
---
status: "accepted"
date: 2026-06-09
deciders: ["alice", "bob"]
consulted: ["security-team"]
informed: ["all-eng"]
---

# {Title — short noun phrase, e.g., "Use FastAPI for the public API"}

## Context and Problem Statement

{What is the problem we are facing? Why now?}

## Decision Drivers

* {Driver 1, e.g., "must serve OpenAPI to mobile clients"}
* {Driver 2, e.g., "team familiarity with Starlette ecosystem"}

## Considered Options

* {Option 1, e.g., "FastAPI"}
* {Option 2, e.g., "Litestar"}
* {Option 3, e.g., "Robyn"}

## Decision Outcome

Chosen option: "{Option 1}", because {rationale}.

### Consequences

* Good, because {good consequence, e.g., "huge ecosystem"}
* Bad, because {bad consequence, e.g., "slower than Litestar at scale"}

## More Information

{Additional context, links, follow-up decisions.}
```

This is the canonical 4.0 layout. The frontmatter is YAML; the body is
plain Markdown.

## Common recipes

### Recipe 1 — Create a new ADR

```bash
npx log4brains adr new "Adopt FastAPI for the public API"
# Opens $EDITOR with the MADR template pre-filled
```

ADRs live under `docs/adr/` (configurable) numbered `NNNN-kebab-case.md`.

For `adr-tools`:

```bash
npx adr-tools new "Adopt FastAPI"
```

For `adr-kit`:

```bash
adr-kit new "Adopt FastAPI"
```

For pure Markdown — just write `docs/adr/0001-adopt-fastapi.md` directly.

### Recipe 2 — Visual UI (log4brains)

```bash
npx log4brains preview
# Serves at http://localhost:4004 — browsable, search, supersession graph
```

```bash
npx log4brains build
# Builds a static site to .log4brains/out/ — deploy to GitHub Pages / Vercel
```

This is log4brains' killer feature: a Vercel-style static site for your
ADRs, including a graph of decisions linked by supersession.

### Recipe 3 — Supersede a previous decision

```markdown
---
status: "accepted"
date: 2026-06-09
supersedes: ["0007-use-flask"]
---

# Migrate from Flask to FastAPI

## Context and Problem Statement
ADR-0007 chose Flask. We now need async; this supersedes it.
...
```

In the old ADR:

```markdown
---
status: "superseded by 0014-migrate-to-fastapi"
---
```

log4brains will render the supersession arrow in the graph view.

### Recipe 4 — Status lifecycle

MADR 4.0 statuses:
- `proposed` — under discussion
- `accepted` — agreed upon
- `rejected` — considered but not adopted
- `deprecated` — no longer recommended but not yet replaced
- `superseded by NNNN` — replaced by a later ADR

Add the new status, commit, link from successors.

### Recipe 5 — Git-inferred metadata (adr-kit)

```bash
adr-kit infer --since "v1.0.0"
```

Walks git history since v1.0.0, lists changes that look load-bearing
(new packages, large refactors, deleted modules) and suggests ADRs to
write. Don't auto-create — use it as a checklist.

### Recipe 6 — Validate (adr-kit)

```bash
adr-kit validate
# Checks all ADRs:
#   - YAML frontmatter parses
#   - Required fields present
#   - status is one of the allowed values
#   - supersession links resolve
#   - dates are valid
```

CI gate to prevent broken ADRs from landing.

### Recipe 7 — Index (adr-kit)

```bash
adr-kit index > docs/adr/README.md
```

Generates a Markdown table of contents — number, title, status, date —
linked to each ADR.

### Recipe 8 — Enforcement (adr-kit)

```yaml
# adr-kit.yaml
enforcement:
  - rule: "Database choice must reference ADR"
    when: "src/db/**.py"
    require_adr_with: ["sqlalchemy", "asyncpg"]
```

For specific paths, require the commit message or a sibling file to
reference an ADR. Useful for high-blast-radius areas.

### Recipe 9 — Deploy to GitHub Pages

```yaml
# .github/workflows/adr-site.yml
name: ADR Site
on:
  push:
    branches: [main]
    paths: ["docs/adr/**"]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npx log4brains build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./.log4brains/out
```

## When to write an ADR (heuristics)

Write one when:
- A senior engineer 6 months from now would ask "why this?"
- The decision is hard to reverse (DB choice, framework, deployment target).
- Multiple options were seriously considered.
- A specific constraint (perf, security, compliance) drove the choice.
- The decision deprecates a previous approach.

Don't write one for:
- "Used a dict here." (implementation detail)
- "Named this function `process`." (style)
- "Bumped numpy 1.26 → 1.27." (mechanical update)
- Reversible choices made by a single developer.

## ADR title patterns

Good: noun phrases stating the decision.
- "Adopt FastAPI for the public API"
- "Use PostgreSQL row-level security for tenant isolation"
- "Migrate to OpenTelemetry for observability"

Bad: questions or vague summaries.
- "What framework should we use?"  (it's a decision, not a question)
- "API choices"                     (too vague)
- "FastAPI"                         (no context)

## Edge cases

- **Massive backlog of past decisions**: don't backfill all of them.
  Backfill only the ones you genuinely revisit.
- **Disagreement**: record dissent in the "Decision Drivers" section.
  ADRs aren't consensus — they're a snapshot of what the team agreed on.
- **Multi-repo / monorepo**: one ADR collection per repo; cross-repo links
  via URL.
- **Private vs public ADRs**: store internal ADRs in a private repo; public
  ones (open-source projects) in `docs/adr/` of the public repo.
- **ADR vs RFC**: RFCs are PROPOSAL-stage; ADRs are DECISION-stage. Many
  teams use both — RFC drafts in `docs/rfc/`, accepted decisions become
  `docs/adr/NNNN-...md`.

## Comparison

| Tool | Notes |
|---|---|
| **log4brains** | Best visual UI; static-site preview; Node-based |
| **adr-tools** (npryce) | Minimal shell; widely used; classic |
| **adr-kit** (kschlt) | Python-native; validation + enforcement; CI-friendly |
| **dotnet-adr** | Richer templates; .NET-focused |
| **Hand-authored Markdown** | Zero tooling; works fine for small teams |
| **Notion / Confluence pages** | Not version-controlled; not browsable in git |

For Python projects: `adr-kit` if you want enforcement; log4brains if you
want a pretty site; pure Markdown if you want zero tooling.

## Sources

- https://adr.github.io/madr/ — MADR 4.0 spec
- https://github.com/thomvaill/log4brains — log4brains source
- https://github.com/npryce/adr-tools — adr-tools source
- https://github.com/kschlt/adr-kit — adr-kit source
- https://adr.github.io/ — ADR community
- https://github.com/joelparkerhenderson/architecture-decision-record — examples
