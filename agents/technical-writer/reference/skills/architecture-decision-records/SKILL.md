<!--
Source: https://github.com/wshobson/agents/blob/main/plugins/documentation-generation/skills/architecture-decision-records/SKILL.md
Repo: wshobson/agents
-->
---
name: architecture-decision-records
description: Write and maintain Architecture Decision Records (ADRs) following best practices for technical decision documentation. Use when documenting significant technical decisions, reviewing past architectural choices, or establishing decision processes.
---

# Architecture Decision Records

Comprehensive patterns for creating, maintaining, and managing Architecture Decision Records (ADRs) that capture the context and rationale behind significant technical decisions.

## When to Use This Skill

- Making significant architectural decisions
- Documenting technology choices
- Recording design trade-offs
- Onboarding new team members
- Reviewing historical decisions
- Establishing decision-making processes

## Core Concepts

### 1. What is an ADR?
- **Context**: Why we needed to make a decision
- **Decision**: What we decided
- **Consequences**: What happens as a result

### 2. When to Write an ADR

| Write ADR | Skip ADR |
|---|---|
| New framework adoption | Minor version upgrades |
| Database technology choice | Bug fixes |
| API design patterns | Implementation details |
| Security architecture | Routine maintenance |
| Integration patterns | Configuration changes |

### 3. ADR Lifecycle

```
Proposed → Accepted → Deprecated → Superseded
              ↓
           Rejected
```

## Templates

### Template 1: Standard ADR (MADR Format)

```markdown
# ADR-0001: Use PostgreSQL as Primary Database

## Status
Accepted

## Context
We need to select a primary database for our new e-commerce platform...

## Decision Drivers
- **Must have ACID compliance** for payment processing
- **Must support complex queries** for reporting
- **Should support full-text search**
- **Should have good JSON support**
- **Team familiarity**

## Considered Options
### Option 1: PostgreSQL
- **Pros**: ACID compliant, excellent JSON support (JSONB), built-in full-text search, PostGIS for geospatial
- **Cons**: Slightly more complex replication setup than MySQL

### Option 2: MySQL
- **Pros**: Very familiar, simple replication, large community
- **Cons**: Weaker JSON support, no built-in full-text search

### Option 3: MongoDB
- **Pros**: Flexible schema, native JSON, horizontal scaling
- **Cons**: No ACID for multi-document transactions

## Decision
We will use **PostgreSQL 15** as our primary database.

## Rationale
1. ACID compliance essential for e-commerce transactions
2. Built-in capabilities reduce infrastructure complexity
3. Team familiarity with SQL databases
4. Mature ecosystem

## Consequences

### Positive
- Single database handles transactions, search, and geospatial queries
- Reduced operational complexity
- Strong consistency guarantees
- Team can leverage existing SQL expertise

### Negative
- Need to learn PostgreSQL-specific features
- Vertical scaling limits may require read replicas sooner

### Risks
- Full-text search may not scale as well as dedicated search engines
- Mitigation: Design for potential Elasticsearch addition if needed

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
related to prop type mismatches and undefined errors.

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

### Template 4: Deprecation ADR

Use when superseding a previous decision. Include migration plan with phased rollout, lessons learned, and link to original ADR being superseded.

### Template 5: RFC Style

Use for major decisions requiring broader discussion. Include Summary, Motivation, Detailed Design, Drawbacks, Alternatives, Unresolved Questions, and Implementation Plan.

## ADR Management

### Directory Structure

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

### ADR Index (README.md)

```markdown
# Architecture Decision Records

## Index

| ADR | Title | Status | Date |
|---|---|---|---|
| 0001 | Use PostgreSQL as Primary Database | Accepted | 2024-01-10 |
| 0002 | Caching Strategy with Redis | Accepted | 2024-01-12 |
| 0003 | MongoDB for User Profiles | Deprecated | 2023-06-15 |
| 0020 | Deprecate MongoDB | Accepted | 2024-01-15 |

## Creating a New ADR
1. Copy `template.md` to `NNNN-title-with-dashes.md`
2. Fill in the template
3. Submit PR for review
4. Update this index after approval

## ADR Status
- **Proposed**: Under discussion
- **Accepted**: Decision made, implementing
- **Deprecated**: No longer relevant
- **Superseded**: Replaced by another ADR
- **Rejected**: Considered but not adopted
```

### Automation (adr-tools)

```bash
# Install
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

## Review Process

### Before Submission
- [ ] Context clearly explains the problem
- [ ] All viable options considered
- [ ] Pros/cons balanced and honest
- [ ] Consequences (positive and negative) documented
- [ ] Related ADRs linked

### During Review
- [ ] At least 2 senior engineers reviewed
- [ ] Affected teams consulted
- [ ] Security implications considered
- [ ] Cost implications documented
- [ ] Reversibility assessed

### After Acceptance
- [ ] ADR index updated
- [ ] Team notified
- [ ] Implementation tickets created
- [ ] Related documentation updated

## Best Practices

### Do's
- Write ADRs early — before implementation starts
- Keep them short — 1-2 pages maximum
- Be honest about trade-offs — include real cons
- Link related decisions — build decision graph
- Update status — deprecate when superseded

### Don'ts
- Don't change accepted ADRs — write new ones to supersede
- Don't skip context — future readers need background
- Don't hide failures — rejected decisions are valuable
- Don't be vague — specific decisions, specific consequences
- Don't forget implementation — ADR without action is waste
