<!--
Source: https://www.atlassian.com/agile/software-development/3-amigos · https://dora.dev/research/ · https://martinfowler.com/articles/microservice-testing/
Authored: June 2026 for the qa-engineer agent bundle.
-->

# QA-Dev Shift-Left — 3-Amigos + TDD/BDD in PR + Retro KPI Review

DORA research shows shift-left practices correlate 4-5x with elite deploy
frequency. The 2026 SOTA: **3-amigo refinement** (PM + Dev + QA on every
story), **TDD/BDD inline with the feature PR**, **quality KPIs reviewed in
sprint retro**. Quality is everyone's job — but someone has to drive it.

## When to use

- New team forming; want quality culture from day 1
- Team's escape rate trending up; reactive QA isn't scaling
- Sprint retro lacks quality metrics
- Developers complain "QA blocks me" or QA complains "I find bugs too late"
- Trigger phrases: "shift left", "3-amigos", "story refinement", "TDD",
  "BDD", "definition of done", "DOR", "quality culture"

## Setup

```bash
# Tools
# - Jira / Linear (story templates)
# - Notion / Confluence (refinement notes, retros)
# - Test framework (pytest / vitest / Playwright)
# - Specflow / Cucumber / pytest-bdd (BDD)
```

Auth: project-management MCP tokens.

## Common recipes

### Recipe 1 — 3-amigo refinement template

```markdown
# 3-Amigo Refinement — <story>

## Attendees
- PM: <name>  Dev: <name>  QA: <name>

## Story
As a <persona>, I want to <action> so that <outcome>.

## Acceptance criteria
| ID | Criterion |
|---|---|
| AC-1 | <criterion> |
| AC-2 | <criterion> |

## Concrete examples (per AC)
- AC-1: "Alice enters bob@example.com → sees toast 'Invite sent'"
- AC-1: "Alice enters bob — sees inline error 'Must be email'"
- AC-2: "Bob receives email within 5 min"

## Risks (HTSM-lite)
- Email infra outage — Likelihood M, Impact H — mitigation: queue + retry
- Duplicate invite — Likelihood H, Impact L — mitigation: idempotent

## Test approach
- Unit: parser, sender (mock SMTP)
- Integration: testcontainers SMTP
- E2E: Playwright; toast assertion
- A11y: axe on invite modal
- Manual: 1 exploratory session on edge cases

## Definition of Ready (gate to start work)
- [ ] AC defined + examples
- [ ] Test approach agreed
- [ ] Estimate within team's spike threshold
- [ ] Dependencies identified

## Definition of Done (gate to merge)
- [ ] All AC have a green test
- [ ] No new P0/P1 defects
- [ ] CI green
- [ ] Docs updated
```

### Recipe 2 — TDD red-green-refactor inline with feature

```python
# Feature PR includes test + implementation in same commit
# tests/invites/test_send_invite.py
def test_send_invite_with_valid_email(invite_service):
    """AC-1: Valid email triggers invite send."""
    result = invite_service.send("alice@example.com")
    assert result.status == "queued"

def test_send_invite_with_invalid_email_raises(invite_service):
    """AC-1: Invalid email rejected."""
    with pytest.raises(InvalidEmail):
        invite_service.send("not-an-email")

# src/invites/service.py
class InviteService:
    def send(self, email: str) -> Result:
        if not is_valid_email(email):
            raise InvalidEmail(email)
        ...
```

PR description: each AC links to its test.

### Recipe 3 — BDD in PR (Gherkin alongside code)

```gherkin
# features/send_invite.feature
Feature: Send invite
  Scenario: Valid email — invite sent
    Given a logged-in admin
    When they invite "bob@example.com"
    Then the response shows "Invite sent to bob@example.com"
    And bob receives an email within 5 minutes

  Scenario: Invalid email — inline error
    Given a logged-in admin
    When they invite "not-an-email"
    Then the response shows "Must be a valid email"
    And no email is sent
```

Reviewers verify Gherkin matches AC; engineers verify step defs pass.

### Recipe 4 — Story template (Jira / Linear)

```markdown
## User story
As a <persona>, I want to <action>, so that <outcome>.

## Acceptance criteria
- [ ] AC-1: ...
- [ ] AC-2: ...

## Test plan link
docs/test-plans/<feature>.md

## Definition of Ready
- [ ] 3-amigo refinement done
- [ ] AC examples written
- [ ] Test approach agreed

## Definition of Done
- [ ] All AC have a passing test (link)
- [ ] PR reviewed by 2
- [ ] No P0/P1 defects opened during work
- [ ] CI green (smoke + a11y + security)
- [ ] Docs / runbook updated
- [ ] Feature flag default-off (if risk medium+)
- [ ] PM walkthrough done (if UI-facing)
```

### Recipe 5 — 3-amigo cadence

```markdown
## Weekly 3-amigo
- Day 1 of sprint: 60 min — refine top 3-5 stories
- Mid-sprint: 30 min — refine the next 2-3 stories
- Output: story marked Ready; AC + examples in ticket; test approach noted

## Single-story 3-amigo (async)
- PM writes draft story + AC
- Dev + QA comment in 24h: estimate, risks, test approach
- 15 min sync if disagreement
- Story moves to Ready
```

### Recipe 6 — Pair on PR (Dev + QA)

```markdown
## Dev-QA pairing on PR
- Dev opens draft PR with code + happy-path test
- QA pairs 30 min:
  - Walks through AC; verifies each has assertion
  - Adds edge-case tests (boundary, empty, oversize, unicode)
  - Suggests exploratory charters for post-merge
- QA reviews PR with "approve with notes" / "request changes"
- Test owner is the merging dev; QA is reviewer
```

### Recipe 7 — Sprint retro KPI review

```markdown
# Retro — Sprint <NN>

## Quality KPIs this sprint
| KPI | Target | Actual | Trend |
|---|---|---|---|
| Escape rate (defects found post-release) | < 5% | 3% | ▼ |
| MTTR P0 | < 24h | n/a | — |
| MTTR P1 | < 7d | 3d | ▼ |
| Flakiness | < 2% | 4% | ▲ |
| Coverage delta | > -1% | +2.3% | ▲ |
| Mutation score | > 60% | 67% | ▲ |
| Smoke duration | < 5 min | 4m 23s | flat |
| DORA change-failure | < 5% | 8% | ▲ |

## Wins
- 0 P0 defects this sprint
- Mutation score on payments module up to 78%

## Misses
- Flakiness up — investigation: new Playwright tests for checkout flaky.
  Action: timing-fix PR by Alice; SLA Mon.
- Change-failure 8% — driven by 1 escape (refund off-by-one). Add property
  test to catch.

## Actions for next sprint
- [ ] Pair Bob + Carol on Playwright timing playbook
- [ ] Add Hypothesis-based property tests to refund module
- [ ] Promote 1 critical test from extended → smoke (admin invite)
```

### Recipe 8 — DORA-aligned KPIs in retro

```markdown
| DORA metric | Elite | This team | Trend |
|---|---|---|---|
| Lead time (commit → prod) | < 1 day | 1.4 days | ▼ |
| Deploy frequency | multiple/day | daily | flat |
| Change failure rate | < 5% | 4% | ▼ |
| Mean time to restore | < 1h | 45 min | ▼ |
```

Connect to quality: escape rate = inverse of change-failure rate confidence.

### Recipe 9 — Shift-left signals to track

```markdown
- % of defects found in dev / unit (target > 80%)
- % of defects found in QA / E2E (target ~15%)
- % of defects found in UAT (target < 5%)
- % of defects found in production (target < 1%)
- % of stories with 3-amigo before sprint start (target > 80%)
- % of PRs with test added (target 100% on feature)
- % of PRs reviewed by QA (target > 60%)
- Avg time from defect filed to fixed (target < 7 days median)
```

### Recipe 10 — TDD-coaching playbook for QA

```markdown
## When pairing with a junior dev on TDD
1. Ask: "What's the test that proves your AC?"
2. Write the failing test together — RED
3. Implement minimum to pass — GREEN
4. Refactor — improve naming, extract method, keep test green
5. Move to next test
6. After PR: review test names; should describe behavior not implementation
```

### Recipe 11 — Quality champion rotation

```markdown
## Quality Champion of the Sprint
- Rotates across team (devs + QA)
- Responsibilities:
  - Curate quality KPI digest for retro
  - Triage flakes + mutation regressions
  - Champion 1 specific improvement
- 1 day/week capacity allocation
- Rotation visible on team page; "this sprint: Alice"
```

### Recipe 12 — Refinement output template (Notion / Confluence)

```markdown
# Refinement — <date>
| Story | Verdict | Notes |
|---|---|---|
| APP-1284 Send invite | Ready | AC + tests defined |
| APP-1285 Bulk export | Spike | Unknown perf risk; 1-day spike first |
| APP-1286 Theme switcher | Ready | Visual diff coverage agreed |
```

## Examples

### Example 1: New team — bootstrap shift-left

**Goal:** Quality culture sprint 1.

1. Adopt story template (Recipe 4) + DoR + DoD.
2. Set 3-amigo cadence (Recipe 5).
3. KPI dashboard in Notion (Recipe 7).
4. First retro: review process, not numbers (no data yet).
5. By sprint 3: KPI trend visible; act on it.

### Example 2: Quality regression — escape rate up

**Goal:** Last 2 sprints: 12% escape rate, target < 5%.

1. Retro analysis: where are escapes coming from?
   - 6 of 10 from "refund" module → mutation score 38%.
2. Action: add property tests + raise mutation floor to 70% on refund.
3. Story for sprint: refactor + harden refund.
4. Shift-left: every refund-touching PR auto-tags QA for review.
5. Re-measure 2 sprints later; expect < 5%.

## Edge cases / gotchas

- **3-amigo without examples** — abstract AC = ambiguous AC. Force concrete
  examples per AC.
- **QA absent from refinement** — defeats the point. Block stories from
  moving to Ready without QA sign.
- **TDD-as-ceremony** — devs write tests after the fact ("post-development
  TDD"). Look at git log: test commit vs impl commit.
- **DoD never enforced** — checklist becomes vanity. PR template + CI
  status checks enforce mechanically.
- **Retro without data** — feelings retro misses systemic issues. Bring KPI
  dashboard.
- **KPI tunnel vision** — chasing 100% coverage misses mutation gap.
  Multi-metric scorecard.
- **QA as gatekeeper not coach** — adversarial. QA pairs early; devs ship
  with confidence.
- **3-amigo skipping spike work** — spike stories need 3-amigo too, often
  more.
- **DORA metrics gaming** — splitting PRs to inflate deploy frequency
  defeats the metric. Measure intent, not count.
- **Shift-left on bug-heavy legacy** — apply to new code first; legacy
  retrofit is a long arc.
- **Single QA across many teams** — bottleneck. Either embed QA per team
  or rotate champions.

## Sources

- [3 Amigos collaboration — Atlassian](https://www.atlassian.com/agile/software-development/3-amigos)
- [DORA research](https://dora.dev/research/)
- [Definition of Done — Atlassian](https://www.atlassian.com/agile/project-management/definition-of-done)
- [Specification by Example — Gojko Adzic](https://gojko.net/books/specification-by-example/)
- [Test Driven Development — Kent Beck](https://www.oreilly.com/library/view/test-driven-development/0321146530/)
- [Microservice testing — Martin Fowler](https://martinfowler.com/articles/microservice-testing/)
- [Continuous Delivery — Jez Humble, Dave Farley](https://continuousdelivery.com/)
- [Modern Software Engineering — Dave Farley](https://www.continuous-delivery.co.uk/)
- [DORA shift-left correlation](https://dora.dev/capabilities/shift-left-on-security/)
