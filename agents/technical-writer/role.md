# Technical Writer — deep reference

This appends to `AGENT.md`. It is **not** in the agent's default context. Grep it when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "README template", "OpenAPI template", "Tutorial template", "Docusaurus configuration", "ADR templates", "Conventional Commits reference", "Mermaid diagram catalog", "Reference doc entry format", "Doc co-authoring workflow detail", "Success metrics", "Documentation audit checklist".

For provenance of any section, see `SOURCES.md` in this bundle.

---

## Capability reference

Factual reference — tools, frameworks, and methodology details. SOUL.md does not carry these (they don't drive turn-by-turn decisions); grep here when the user asks "what should I use for X?"

### Documentation site generators

- **Docusaurus** — React-based, plugin ecosystem, good for product docs + blog combos
- **MkDocs** — Python, fast, great for technical docs with the Material theme
- **Sphinx** — Python ecosystem standard, autodoc for code reference, reStructuredText (also supports Markdown via MyST)
- **VitePress** — Vue-based, lightweight, blazing fast builds
- **Mintlify, ReadMe, Stoplight, Redoc** — hosted API documentation portals
- **Swagger UI** — interactive API reference from OpenAPI spec

### API documentation toolchain

- **OpenAPI 3.1+** — primary specification standard
- **AsyncAPI** — event-driven and real-time APIs
- **GraphQL SDL** — schema definitions
- **JSON Schema** — validation + documentation integration
- **Spectral** — OpenAPI linter for style enforcement
- **Stoplight Studio** — collaborative API design and documentation
- **Insomnia / Postman** — collection generation and maintenance

### SDK generation

- **OpenAPI Generator** — multi-language SDK generation from spec
- **Speakeasy, Fern, Stainless** — modern commercial SDK generators
- **Custom templates** — when generated SDKs need house-style tweaks

### Authoring quality tools

- **Vale** — prose linter, configurable style guides (Microsoft Style, Google Developer Documentation Style, etc.)
- **markdownlint** — Markdown style enforcement
- **textlint** — pluggable text linting
- **alex** — catches insensitive or unclear writing

### Diagramming

- **Mermaid** — text-to-diagram, embeddable in Markdown (preferred for docs-as-code)
- **PlantUML** — sequence, class, state, deployment diagrams
- **draw.io / diagrams.net** — for diagrams beyond Mermaid's vocabulary
- **C4 model** — context / containers / components / code for system architecture

### Documentation engineering checklist

- API documentation 100% coverage
- Code examples tested and working
- Search functionality implemented
- Version management active
- Mobile responsive design
- Page load time < 2s
- Accessibility WCAG AA compliant
- Analytics tracking enabled

### Documentation architecture concerns

- Information hierarchy design
- Navigation structure planning
- Content categorization
- Cross-referencing strategy
- Version control integration
- Multi-repository coordination
- Localization framework
- Search optimization

### Documentation testing

- Link checking
- Code example testing
- Build verification
- Screenshot updates
- API response validation against schema
- Performance testing
- SEO optimization
- Accessibility testing

### Multi-version docs

- Version switching UI
- Migration guides
- Changelog integration
- Deprecation notices
- Feature comparison
- Legacy documentation
- Beta documentation
- Release coordination

### Search optimization

- Full-text search
- Faceted search
- Search analytics — measure what users search for
- Query suggestions
- Result ranking
- Synonym handling
- Typo tolerance
- Index optimization

### Contribution workflows

- Edit on GitHub links
- PR preview builds
- Style guide enforcement (linters in CI)
- Review processes (engineering review for accuracy, peer review for clarity)
- Contributor guidelines
- Documentation templates
- Automated checks
- Recognition system

---

## README template

```markdown
# Project Name

> One-sentence description of what this does and why it matters.

[![npm version](https://badge.fury.io/js/your-package.svg)](https://badge.fury.io/js/your-package)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why This Exists

<!-- 2-3 sentences: the problem this solves. Not features — the pain. -->

## Quick Start

<!-- Shortest possible path to working. No theory. -->

```bash
npm install your-package
```

```javascript
import { doTheThing } from 'your-package';

const result = await doTheThing({ input: 'hello' });
console.log(result); // "hello world"
```

## Installation

**Prerequisites**: Node.js 18+, npm 9+

```bash
npm install your-package
# or
yarn add your-package
```

## Usage

### Basic Example

<!-- Most common use case, fully working -->

### Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `timeout` | `number` | `5000` | Request timeout in milliseconds |
| `retries` | `number` | `3` | Number of retry attempts on failure |

### Advanced Usage

<!-- Second most common use case -->

## API Reference

See [full API reference →](https://docs.yourproject.com/api)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT © [Your Name](https://github.com/yourname)
```

---

## OpenAPI template

```yaml
openapi: 3.1.0
info:
  title: Orders API
  version: 2.0.0
  description: |
    The Orders API allows you to create, retrieve, update, and cancel orders.

    ## Authentication
    All requests require a Bearer token in the `Authorization` header.
    Get your API key from [the dashboard](https://app.example.com/settings/api).

    ## Rate Limiting
    Requests are limited to 100/minute per API key. Rate limit headers are
    included in every response. See [Rate Limiting guide](https://docs.example.com/rate-limits).

    ## Versioning
    This is v2 of the API. See the [migration guide](https://docs.example.com/v1-to-v2)
    if upgrading from v1.

paths:
  /orders:
    post:
      summary: Create an order
      description: |
        Creates a new order. The order is placed in `pending` status until
        payment is confirmed. Subscribe to the `order.confirmed` webhook to
        be notified when the order is ready to fulfill.
      operationId: createOrder
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
            examples:
              standard_order:
                summary: Standard product order
                value:
                  customer_id: "cust_abc123"
                  items:
                    - product_id: "prod_xyz"
                      quantity: 2
                  shipping_address:
                    line1: "123 Main St"
                    city: "Seattle"
                    state: "WA"
                    postal_code: "98101"
                    country: "US"
      responses:
        '201':
          description: Order created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Order'
        '400':
          description: Invalid request — see `error.code` for details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
              examples:
                missing_items:
                  value:
                    error:
                      code: "VALIDATION_ERROR"
                      message: "items is required and must contain at least one item"
                      field: "items"
        '429':
          description: Rate limit exceeded
          headers:
            Retry-After:
              description: Seconds until rate limit resets
              schema:
                type: integer
```

### OpenAPI best practices

- Descriptive summaries (not just method names)
- Detailed descriptions with usage context
- Meaningful examples (real-world values, not "foo"/"bar")
- Consistent naming (snake_case or camelCase — pick one)
- Proper typing (no generic `object` where a schema fits)
- Reusable components (`$ref` for schemas, parameters, responses)
- Security definitions on every secured endpoint
- Extension usage where vendor-specific behavior matters

---

## Tutorial template

```markdown
# Tutorial: [What They'll Build] in [Time Estimate]

**What you'll build**: A brief description of the end result with a screenshot or demo link.

**What you'll learn**:
- Concept A
- Concept B
- Concept C

**Prerequisites**:
- [ ] [Tool X](link) installed (version Y+)
- [ ] Basic knowledge of [concept]
- [ ] An account at [service] ([sign up free](link))

---

## Step 1: Set Up Your Project

First, create a new project directory and initialize it.

```bash
mkdir my-project && cd my-project
npm init -y
```

You should see output like:
```
Wrote to /path/to/my-project/package.json: { ... }
```

> **Tip**: If you see `EACCES` errors, [fix npm permissions](https://link) or use `npx`.

## Step 2: Install Dependencies

## Step N: What You Built

You built a [description]. Here's what you learned:
- **Concept A**: How it works and when to use it
- **Concept B**: The key insight

## Next Steps

- [Advanced tutorial: Add authentication](link)
- [Reference: Full API docs](link)
- [Example: Production-ready version](link)
```

### Tutorial writing principles

- **Show, don't tell** — demonstrate with code, then explain
- **Fail forward** — include intentional errors to teach debugging
- **Incremental complexity** — each step builds on the previous
- **Frequent validation** — readers should run code often
- **Multiple perspectives** — explain the same concept different ways

### Exercise types

1. **Fill-in-the-Blank** — complete partially written code
2. **Debug Challenges** — fix intentionally broken code
3. **Extension Tasks** — add features to working code
4. **From Scratch** — build based on requirements
5. **Refactoring** — improve existing implementations

### Common tutorial formats

- **Quick Start** — 5-minute introduction to get running
- **Deep Dive** — 30-60 minute comprehensive exploration
- **Workshop Series** — multi-part progressive learning
- **Cookbook Style** — problem-solution pairs
- **Interactive Labs** — hands-on coding environments

---

## Docusaurus configuration

```javascript
// docusaurus.config.js
const config = {
  title: 'Project Docs',
  tagline: 'Everything you need to build with Project',
  url: 'https://docs.yourproject.com',
  baseUrl: '/',
  trailingSlash: false,

  presets: [['classic', {
    docs: {
      sidebarPath: require.resolve('./sidebars.js'),
      editUrl: 'https://github.com/org/repo/edit/main/docs/',
      showLastUpdateAuthor: true,
      showLastUpdateTime: true,
      versions: {
        current: { label: 'Next (unreleased)', path: 'next' },
      },
    },
    blog: false,
    theme: { customCss: require.resolve('./src/css/custom.css') },
  }]],

  plugins: [
    ['@docusaurus/plugin-content-docs', {
      id: 'api',
      path: 'api',
      routeBasePath: 'api',
      sidebarPath: require.resolve('./sidebarsApi.js'),
    }],
    [require.resolve('@cmfcmf/docusaurus-search-local'), {
      indexDocs: true,
      language: 'en',
    }],
  ],

  themeConfig: {
    navbar: {
      items: [
        { type: 'doc', docId: 'intro', label: 'Guides' },
        { to: '/api', label: 'API Reference' },
        { type: 'docsVersionDropdown' },
        { href: 'https://github.com/org/repo', label: 'GitHub', position: 'right' },
      ],
    },
    algolia: {
      appId: 'YOUR_APP_ID',
      apiKey: 'YOUR_SEARCH_API_KEY',
      indexName: 'your_docs',
    },
  },
};
```

---

## Reference doc entry format

For API references, configuration guides, schema documentation:

```markdown
### [Feature/Method/Parameter Name]

**Type**: [Data type or signature]
**Default**: [Default value if applicable]
**Required**: [Yes/No]
**Since**: [Version introduced]
**Deprecated**: [Version if deprecated]

**Description**:
[Comprehensive description of purpose and behavior]

**Parameters**:
- `paramName` (type): Description [constraints]

**Returns**:
[Return type and description]

**Throws**:
- `ExceptionType`: When this occurs

**Examples**:
[Multiple examples showing different use cases]

**See Also**:
- [Related Feature 1]
- [Related Feature 2]
```

### Hierarchical structure for reference docs

1. **Overview** — quick introduction to the module/API
2. **Quick Reference** — cheat sheet of common operations
3. **Detailed Reference** — alphabetical or logical grouping
4. **Advanced Topics** — complex scenarios and optimizations
5. **Appendices** — glossary, error codes, deprecations

### Navigation aids

- Table of contents with deep linking
- Alphabetical index
- Search functionality markers
- Category-based grouping
- Version-specific documentation

### Warnings and notes

- **Warning**: potential issues or gotchas
- **Note**: important information
- **Tip**: best practices
- **Deprecated**: migration guidance
- **Security**: security implications

---

## ADR templates

### Template 1: MADR (Markdown Architectural Decision Records)

```markdown
# ADR-0001: Use PostgreSQL as Primary Database

## Status
Accepted

## Context
We need to select a primary database...

## Decision Drivers
- Must have ACID compliance for payment processing
- Must support complex queries for reporting
- Should support full-text search
- Should have good JSON support
- Team familiarity reduces onboarding time

## Considered Options

### Option 1: PostgreSQL
- **Pros**: ACID compliant, excellent JSON support (JSONB), built-in full-text search, PostGIS for geospatial
- **Cons**: Slightly more complex replication setup than MySQL

### Option 2: MySQL
- **Pros**: Very familiar to team, simple replication, large community
- **Cons**: Weaker JSON support, no built-in full-text search

### Option 3: MongoDB
- **Pros**: Flexible schema, native JSON, horizontal scaling
- **Cons**: No ACID for multi-document transactions, team has limited experience

## Decision
We will use **PostgreSQL 15** as our primary database.

## Rationale
[Why this option won]

## Consequences

### Positive
- Single database handles transactions, search, and geospatial queries
- Reduced operational complexity

### Negative
- Need to learn PostgreSQL-specific features
- Vertical scaling limits may require read replicas sooner

### Risks
- [Mitigation strategy for each risk]

## Related Decisions
- ADR-0002: Caching Strategy (Redis)
- ADR-0005: Search Architecture
```

### Template 2: Lightweight ADR

```markdown
# ADR-0012: Adopt TypeScript for Frontend Development

**Status**: Accepted
**Date**: 2024-01-15
**Deciders**: @alice, @bob, @charlie

## Context
Our React codebase has grown to 50+ components with increasing bug reports
related to prop type mismatches.

## Decision
Adopt TypeScript for all new frontend code. Migrate existing code incrementally.

## Consequences
**Good**: Catch type errors at compile time, better IDE support, self-documenting code.
**Bad**: Learning curve, initial slowdown, build complexity increase.
**Mitigations**: TypeScript training, allow gradual adoption with `allowJs: true`.
```

### Template 3: Y-Statement Format

```markdown
# ADR-0015: API Gateway Selection

In the context of **building a microservices architecture**,
facing **the need for centralized API management, authentication, and rate limiting**,
we decided for **Kong Gateway**
and against **AWS API Gateway and custom Nginx solution**,
to achieve **vendor independence, plugin extensibility, and team familiarity with Lua**,
accepting that **we need to manage Kong infrastructure ourselves**.
```

### ADR lifecycle

```
Proposed → Accepted → Deprecated → Superseded
              ↓
           Rejected
```

### ADR directory structure

```
docs/
├── adr/
│   ├── README.md           # Index and guidelines
│   ├── template.md         # Team's ADR template
│   ├── 0001-use-postgresql.md
│   ├── 0002-caching-strategy.md
│   ├── 0003-mongodb-user-profiles.md  # [DEPRECATED]
│   └── 0020-deprecate-mongodb.md      # Supersedes 0003
```

### ADR automation

```bash
# Install adr-tools
brew install adr-tools

# Initialize
adr init docs/adr

# Create new ADR
adr new "Use PostgreSQL as Primary Database"

# Supersede an ADR
adr new -s 3 "Deprecate MongoDB in Favor of PostgreSQL"

# Generate table of contents
adr generate toc > docs/adr/README.md
```

### ADR review checklist

**Before Submission:**
- [ ] Context clearly explains the problem
- [ ] All viable options considered
- [ ] Pros/cons balanced and honest
- [ ] Consequences (positive and negative) documented
- [ ] Related ADRs linked

**During Review:**
- [ ] At least 2 senior engineers reviewed
- [ ] Affected teams consulted
- [ ] Security implications considered
- [ ] Cost implications documented
- [ ] Reversibility assessed

**After Acceptance:**
- [ ] ADR index updated
- [ ] Team notified
- [ ] Implementation tickets created
- [ ] Related documentation updated

### ADR best practices

- Write ADRs **early** — before implementation starts
- Keep them **short** — 1-2 pages maximum
- Be **honest about trade-offs** — include real cons
- **Link related decisions** — build a decision graph
- **Update status** — deprecate when superseded
- **Don't change accepted ADRs** — write new ones to supersede
- **Don't hide failures** — rejected decisions are valuable

---

## Conventional Commits reference

### Commit message examples

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

Fixes #456
Reviewed-by: @alice
```

### Commit types

| Type | Purpose | Version bump |
|---|---|---|
| `feat` | New feature | Minor |
| `fix` | Bug fix | Patch |
| `docs` | Documentation only | None |
| `style` | Formatting, no code change | None |
| `refactor` | Code restructuring | None |
| `perf` | Performance improvement | Patch |
| `test` | Test additions/changes | None |
| `build` | Build system / deps | None |
| `ci` | CI config changes | None |
| `chore` | Maintenance | None |
| `revert` | Revert previous commit | Patch |
| `feat!` / `BREAKING CHANGE` | Breaking change | Major |

### Keep a Changelog format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature X (#123)

### Changed
- Modified behavior of Y

### Fixed
- Bug in Z

### Deprecated
- Old API method (use new method instead, removal in v3.0)

### Removed
- Legacy endpoint /api/v1/users

### Security
- Patched XSS vulnerability in user profile rendering
```

### Release-notes structure

- **Summary** — short overview of release theme
- **Highlights** — major features with emoji headers
- **Breaking Changes** — explicitly called out with migration steps
- **Upgrade Guide** — what users need to do
- **Known Issues** — flag with target fix version
- **Dependencies Updated** — table of package updates

---

## Mermaid diagram catalog

Eight primary diagram types:

| Type | When to use |
|---|---|
| `graph` (flowchart) | Decision trees, process flows, system overviews |
| `sequenceDiagram` | API call sequences, component interactions |
| `classDiagram` | Object models, class hierarchies |
| `stateDiagram-v2` | State machines, lifecycle, order/payment states |
| `erDiagram` | Database schemas, entity relationships |
| `gantt` | Project timelines, release schedules |
| `pie` | Proportions, market share, traffic sources |
| `gitGraph` | Branch strategies, release flow |

### Mermaid methodology

1. Select appropriate diagram type for the concept
2. Maintain readability — avoid overcrowding
3. Apply consistent styling
4. Use clear, meaningful labels
5. Validate rendering quality before delivery

---

## Doc co-authoring workflow detail

For substantial writing tasks (PRDs, design docs, decision docs, RFCs), use the 3-stage workflow:

### Stage 1: Context Gathering

Goal: close the gap between what the user knows and what you know.

Initial questions:
1. What type of document is this?
2. Who's the primary audience?
3. What's the desired impact when someone reads this?
4. Is there a template or specific format to follow?
5. Any other constraints or context to know?

Then encourage info-dumping: background, related discussions, why alternatives aren't used, organizational context, timeline pressures, technical dependencies, stakeholder concerns.

When user signals they've done their initial dump, ask 5-10 numbered clarifying questions based on gaps. Let them answer in shorthand.

**Exit condition:** sufficient context when questions show understanding — can ask about edge cases and trade-offs without needing basics explained.

### Stage 2: Refinement & Structure

Build section by section. For each section:

1. **Clarifying questions** about what to include (5-10 specific questions)
2. **Brainstorming** — generate 5-20 numbered options
3. **Curation** — user indicates what to keep/remove/combine
4. **Gap check** — anything important missing?
5. **Drafting** — replace placeholder with drafted content
6. **Iterative refinement** — surgical edits based on feedback (never reprint the whole doc)

After 3 consecutive iterations with no substantial changes, ask if anything can be removed.

### Stage 3: Reader Testing

Test with fresh Claude (no context bleed) to catch blind spots.

1. **Predict reader questions** — 5-10 realistic questions
2. **Test** — invoke fresh Claude with the doc + question
3. **Check** — ambiguity, false assumptions, contradictions
4. **Report and fix** — loop back to refinement for problematic sections

Exit when reader Claude consistently answers correctly and surfaces no new gaps.

---

## Success metrics

Documentation works when:

- **Support ticket volume decreases** after docs ship — target 20% reduction for covered topics
- **Time-to-first-success** for new developers < 15 minutes (measured via tutorials)
- **Docs search satisfaction rate** ≥ 80% — users find what they're looking for
- **Zero broken code examples** in any published doc
- **100% of public APIs** have a reference entry, at least one code example, and error documentation
- **Developer NPS for docs** ≥ 7/10
- **PR review cycle for docs PRs** ≤ 2 days — docs are not a bottleneck

---

## Documentation audit checklist

Use when assessing existing docs.

**Coverage**:
- [ ] Every public API documented
- [ ] Every CLI flag and env var documented
- [ ] Every configuration option documented
- [ ] Every error code documented with resolution

**Accuracy**:
- [ ] Code examples tested in clean environment
- [ ] Commands match current implementation
- [ ] Screenshots reflect current UI
- [ ] Version numbers up to date

**Consistency**:
- [ ] Voice consistent (second person, active)
- [ ] Terminology consistent (glossary maintained)
- [ ] Code style consistent (formatter applied)
- [ ] Heading hierarchy consistent

**Discoverability**:
- [ ] Search index covers all pages
- [ ] Navigation is intuitive
- [ ] Cross-references work
- [ ] Sitemap and SEO basics in place

**Maintenance**:
- [ ] Each page has a "last updated" date
- [ ] Stale pages flagged for review
- [ ] Broken links checked weekly (CI)
- [ ] Code examples re-tested on dependency updates

**Accessibility**:
- [ ] Alt text on all images
- [ ] Color contrast WCAG AA
- [ ] Keyboard navigable
- [ ] Screen reader compatible

**Analytics-driven**:
- [ ] High-exit pages identified as bugs
- [ ] Top-searched terms cross-referenced with content gaps
- [ ] User feedback collected on every page

---

## Writing principles condensed

- **Lead with outcomes**: "After completing this guide, you'll have a working webhook endpoint" — not "This guide covers webhooks"
- **Use second person**: "You install the package" — not "The package is installed by the user"
- **Be specific about failure**: "If you see `Error: ENOENT`, ensure you're in the project directory"
- **Acknowledge complexity honestly**: "This step has a few moving parts — here's a diagram to orient you"
- **Cut ruthlessly**: If a sentence doesn't help the reader do something or understand something, delete it
- **Active voice**: "Configure the timeout" — not "the timeout can be configured"
- **Present tense**: "The API returns" — not "the API will return"
- **Consistent terminology**: maintain a project glossary

---

## SOTA tool reference (June 2026)

Grep-friendly per-tool reference. Each entry points at the bundled skill pack with the full recipe. Use this when deciding "what tool should I use for X?" Use the linked skill when actually executing.

### Mintlify CLI

Hosted, AI-first API docs with auto-generated playgrounds, llms.txt, and built-in MCP server.

- Install: `npm i -g mintlify`
- Use: `mintlify dev` for local preview, `mintlify deploy` to ship.
- Source the agent reads: OpenAPI spec referenced from `docs.json`.
- Best for: SaaS-acceptable orgs that want hosted, branded, AI-friendly API docs.
- Skill pack: `skills/mintlify-api-docs/SKILL.md`.

### Redocly CLI

Open-source OpenAPI lint + bundle + build-docs. Self-hosted; pair with Scalar or ReDoc renderer.

- Install: `npm i -g @redocly/cli`
- Use: `redocly lint openapi.yaml --extends=recommended`; `redocly bundle`; `redocly build-docs`.
- Best for: self-hosted API reference, CI gates on spec quality, multi-file specs.
- Skill pack: `skills/redocly-openapi-pipeline/SKILL.md`.

### Scalar CLI

Modern, fast API reference renderer (Stripe-style aesthetic).

- Install: `npm i -g @scalar/cli`
- Use: `scalar reference openapi.yaml --output dist/scalar.html`.
- Best for: when ReDoc looks dated and Mintlify isn't an option.
- Skill pack: `skills/redocly-openapi-pipeline/SKILL.md` (covered there).

### @hey-api/openapi-ts

TS-first SDK generator from OpenAPI. Modern fetch / axios / next clients.

- Install: `npm i -D @hey-api/openapi-ts`
- Use: `npx openapi-ts` with `openapi-ts.config.ts`.
- Best for: TypeScript-only SDKs with clean modern client code.
- Skill pack: `skills/openapi-sdk-generation/SKILL.md`.

### @openapitools/openapi-generator-cli

Multi-language SDK generator (TS / Python / Go / Java / C# / PHP / Ruby / Rust / Kotlin / Swift / Dart).

- Install: `npx @openapitools/openapi-generator-cli`
- Use: `... generate -i openapi.yaml -g typescript-axios -o packages/sdk-ts`.
- Best for: shipping SDKs in many languages from one spec.
- Skill pack: `skills/openapi-sdk-generation/SKILL.md`.

### Speakeasy / Fern

Paid SDK generation platforms; polished per-language idioms, auto-publish.

- Best for: when SDK quality and per-language ergonomics justify cost.
- Skill pack: `skills/openapi-sdk-generation/SKILL.md`.

### Log4brains

Modern ADR toolkit — visual site, CLI, git-log metadata inference.

- Install + use: `npx log4brains init docs/adr`; `npx log4brains new`; `npx log4brains build`.
- Best for: docs-as-code ADRs with a browsable visual site.
- Skill pack: `skills/log4brains-adr-management/SKILL.md`.

### adr-kit

CI-side MADR validation, indexing, supersession enforcement.

- Install: `pipx install adr-kit`
- Use: `adr-kit validate docs/adr/`; `adr-kit lint --check-supersession`.
- Best for: enforcing ADR quality in CI.
- Skill pack: `skills/log4brains-adr-management/SKILL.md`.

### adr-tools (npryce)

Legacy ADR CLI. Still works; prefer Log4brains for new projects.

- Install: `npx adr-tools init docs/adr`
- Skill pack: `skills/log4brains-adr-management/SKILL.md` (migration recipe).

### MADR 4.0 template

The 2026 standard markdown ADR template (YAML frontmatter + sections).

- Reference: https://adr.github.io/madr/
- Skill pack: `skills/log4brains-adr-management/SKILL.md`.

### git-cliff

Rust-fast (~120ms / 10k commits) Conventional Commits → CHANGELOG generator. No Node dependency.

- Install: `pipx install git-cliff` or `cargo install git-cliff`
- Use: `git-cliff -o CHANGELOG.md`; `git-cliff --bump`.
- Best for: fast, scriptable, language-agnostic changelog rendering.
- Skill pack: `skills/git-cliff-changelog/SKILL.md`.

### release-please (Google)

End-to-end release-PR automation — auto-PR with SemVer bump + CHANGELOG + tag on merge.

- Install: GitHub Actions workflow with `googleapis/release-please-action@v4`.
- Best for: zero-touch releases on GitHub.
- Skill pack: `skills/release-please-automation/SKILL.md`.

### conventional-changelog-cli

Legacy Node-based Conventional Commits changelog. Prefer git-cliff in 2026.

- Install: `npm i -g conventional-changelog-cli`
- Skill pack: covered in `skills/changelog-automation/SKILL.md` (bundled).

### Lychee link checker

Fastest 2026 link checker. JSON output, fragment checking, CI integration.

- Install: release binary, brew, cargo, or Docker.
- Use: `lychee --format json --output report.json .`
- Best for: every docs PR + nightly cron.
- Skill pack: `skills/lychee-link-checking/SKILL.md`.

### Vale

De facto SOTA prose linter. Google + Microsoft + write-good + proselint + alex style packs.

- Install: `brew install vale` or release binary.
- Use: `vale --output=JSON docs/`
- Best for: enforce voice, terminology, Diátaxis vocabulary, banned terms.
- Skill pack: `skills/vale-prose-linting/SKILL.md`.

### markdownlint-cli2

Markdown structure linter.

- Use: `npx markdownlint-cli2 "**/*.md"`
- Best for: heading hierarchy, list style, link style, fence style.
- Skill pack: paired with `vale-prose-linting` and `lychee-link-checking` workflows.

### alex

Insensitive / unclear language detector.

- Use: `npx alex .`
- Best for: pre-commit / PR gate.
- Skill pack: bundled into `vale-prose-linting` recipes.

### pytest-markdown-docs (Modal Labs)

Execute Python code fences in markdown under pytest. Catches drift between docs and code.

- Install: `uv add --dev pytest pytest-markdown-docs`
- Use: `pytest --markdown-docs docs/`
- Best for: every Python doc example.
- Skill pack: `skills/pytest-markdown-docs-validation/SKILL.md`.

### mktestdocs

Lighter alternative to pytest-markdown-docs for simpler setups.

- Skill pack: `skills/pytest-markdown-docs-validation/SKILL.md`.

### pa11y-ci + axe-core

WCAG 2.2 AA accessibility audit. axe-core is the rule engine (~57% WCAG coverage automated).

- Install: `npm i -g pa11y-ci`
- Use: `pa11y-ci --config .pa11yci.json`
- Best for: nightly + PR gate.
- Skill pack: `skills/pa11y-axe-accessibility-audit/SKILL.md`.

### Lighthouse CI

Accessibility + perf + SEO + best-practices in one tool.

- Install: `npm i -g @lhci/cli`
- Use: `lhci autorun`
- Best for: complementing pa11y with perf/SEO checks.
- Skill pack: `skills/pa11y-axe-accessibility-audit/SKILL.md`.

### Microsoft Clarity MCP

Free behavioral analytics — heatmaps, click-streams, rage clicks, dead clicks, session replays. Native MCP server.

- Install: add `@microsoft/clarity-mcp-server` to `.mcp.json`.
- Use: ask Claude for high-exit pages, rage-click URLs, scroll-depth heatmaps.
- Best for: behavioral audit of any docs site.
- Skill pack: `skills/microsoft-clarity-doc-analytics/SKILL.md`.

### GA4 Data API

Programmatic Google Analytics queries — sessions, exit rate, engaged time, content groupings.

- Install: `pip install google-analytics-data`
- Use: service-account auth + RunReportRequest.
- Best for: high-exit page detection, content-group rollups.
- Skill pack: `skills/ga4-doc-analytics/SKILL.md`.

### Algolia DocSearch Insights API

Top-searched terms, no-result searches, click-through rate per page.

- Install: free for OSS at https://docsearch.algolia.com/apply
- Use: REST calls to `insights.algolia.io`.
- Best for: identifying content gaps from search behavior.
- Skill pack: `skills/algolia-doc-search/SKILL.md`.

### Sphinx + sphinx-autodoc-typehints

Python reference docs auto-generated from source.

- Install: `uv add sphinx furo sphinx-autodoc-typehints myst-parser`
- Use: `sphinx-build -b html docs/ docs/_build/`
- Skill pack: `skills/sphinx-typedoc-reference-docs/SKILL.md`.

### TypeDoc

TypeScript reference docs.

- Install: `npm i -D typedoc typedoc-plugin-markdown`
- Use: `npx typedoc` (HTML) or `npx typedoc --plugin typedoc-plugin-markdown` (MDX for Docusaurus/Starlight).
- Skill pack: `skills/sphinx-typedoc-reference-docs/SKILL.md`.

### Doxygen

C / C++ reference docs.

- Install: `brew install doxygen graphviz`
- Use: `doxygen`
- Skill pack: `skills/sphinx-typedoc-reference-docs/SKILL.md`.

### rustdoc

Rust reference docs (built into cargo).

- Use: `cargo doc --no-deps`
- Skill pack: `skills/sphinx-typedoc-reference-docs/SKILL.md`.

### Docusaurus

React/MDX docs generator. Best for big sites + heavy versioning.

- Install: `npx create-docusaurus@latest docs classic --typescript`
- Skill pack: `skills/docusaurus-vitepress-starlight-mkdocs/SKILL.md`.

### VitePress

Vue-based docs generator. Fastest dev/build cycle.

- Install: `npm create vitepress@latest`
- Skill pack: `skills/docusaurus-vitepress-starlight-mkdocs/SKILL.md`.

### Astro Starlight

Astro-based, Islands architecture, fastest cold builds.

- Install: `npm create astro@latest -- --template starlight`
- Skill pack: `skills/docusaurus-vitepress-starlight-mkdocs/SKILL.md`.

### MkDocs Material

Python-based, simplest config, great for Python projects.

- Install: `uv add mkdocs-material`
- Skill pack: `skills/docusaurus-vitepress-starlight-mkdocs/SKILL.md`.

### D2 (Terrastruct)

Modern auto-layout diagram language. Multiple themes, beats Mermaid on large architectures.

- Install: `curl -fsSL https://d2lang.com/install.sh | sh -s --`
- Use: `d2 input.d2 output.svg`
- Best for: architecture diagrams > 8 nodes.
- Skill pack: `skills/d2-mermaid-diagrams/SKILL.md`.

### Mermaid CLI (mmdc)

Default for inline-in-markdown diagrams. GitHub renders natively.

- Install: `npm i -g @mermaid-js/mermaid-cli`
- Use: `mmdc -i diagram.mmd -o diagram.svg -t dark -b transparent`
- Best for: sequence, ER, state, flowchart, gantt.
- Skill pack: `skills/d2-mermaid-diagrams/SKILL.md`.

### PlantUML

Full UML completeness (deployment, component, activity, use-case). Requires JVM.

- Install: `brew install plantuml graphviz`
- Best for: enterprise UML completeness.
- Skill pack: `skills/d2-mermaid-diagrams/SKILL.md`.

### Structurizr DSL

C4 model architecture diagrams (Context / Container / Component / Code).

- Install: `brew install structurizr-cli`
- Skill pack: `skills/d2-mermaid-diagrams/SKILL.md`.

### DeepL API

SOTA machine translation for tech content. `tag_handling=markdown` preserves formatting.

- Install: `deepl-mcp` MCP server OR REST.
- Best for: high-quality machine translation.
- Skill pack: `skills/deepl-translation-i18n/SKILL.md`.

### Crowdin / Lokalise

Translator review workflows for docs i18n.

- Install: `npm i -g @crowdin/cli` or `@lokalise/cli-2`.
- Skill pack: `skills/deepl-translation-i18n/SKILL.md`.

### Pagefind / MeiliSearch / Typesense / Orama

Open-source doc search alternatives to Algolia.

- Skill pack: `skills/algolia-doc-search/SKILL.md` (alternatives section).

### Kapa.ai / Inkeep / Mendable / Markprompt

AI-powered doc search and chat (paid).

- Best for: large docs sites where DocSearch alone isn't enough.
- Skill pack: covered in `skills/algolia-doc-search/SKILL.md`.

### Diátaxis framework

Content organization framework: tutorial / how-to / reference / explanation. Never mix.

- Reference: https://diataxis.fr/
- Skill pack: `skills/diataxis-divio-system/SKILL.md`.

---

## SOTA execution playbook

When the user names a use case, the agent immediately picks the matching skill pack:

| User asks | Skill pack first stop |
|---|---|
| "Write a README" | `zero-hallucination-readme` |
| "Generate API docs from openapi.yaml" | `mintlify-api-docs` (hosted) OR `redocly-openapi-pipeline` (self-hosted) |
| "Generate TypeScript / Python / Go SDKs from this spec" | `openapi-sdk-generation` |
| "Write a tutorial" | `pytest-markdown-docs-validation` + `diataxis-divio-system` + `doc-coauthoring` |
| "Write reference docs for this library" | `sphinx-typedoc-reference-docs` |
| "Write an ADR" | `log4brains-adr-management` |
| "Generate the CHANGELOG" | `git-cliff-changelog` |
| "Automate releases" | `release-please-automation` |
| "Pick a docs generator" | `docusaurus-vitepress-starlight-mkdocs` |
| "Reorganize docs by Diátaxis" | `diataxis-divio-system` |
| "Audit docs for broken links" | `lychee-link-checking` |
| "Audit docs for prose quality" | `vale-prose-linting` |
| "Audit docs for accessibility" | `pa11y-axe-accessibility-audit` |
| "Show me what readers struggle with" | `microsoft-clarity-doc-analytics` |
| "Show me docs traffic" | `ga4-doc-analytics` |
| "What are readers searching for?" | `algolia-doc-search` |
| "Diagram this architecture" | `d2-mermaid-diagrams` |
| "Translate docs to French / German" | `deepl-translation-i18n` |
| "Co-author a design doc with me" | bundled `doc-coauthoring` |
