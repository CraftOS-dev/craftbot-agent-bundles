<!--
Source: https://www.atlassian.com/agile/project-management/user-acceptance-testing · https://www.scrumguides.org/scrum-guide.html
Authored: June 2026 for the qa-engineer agent bundle.
-->

# UAT Coordination — Scenarios + Sign-off + Evidence

User Acceptance Testing happens whether you plan it or not — plan it. QA owns
facilitation: PM/PO writes scenarios from acceptance criteria; stakeholders
execute on a staging env; evidence captured via Loom + screenshots; sign-off
committed to Notion / Confluence. Avoids the "demo demo demo, then prod
breaks" pattern.

## When to use

- Feature merged to staging; stakeholders need to verify before prod
- Multi-team release where PM, ops, support, sales need to sanity-check
- Regulated launch needing user/business sign-off evidence
- Beta program with external customers
- Trigger phrases: "UAT", "user acceptance", "sign-off", "stakeholder
  review", "demo", "beta", "preview env"

Do NOT use for: dev-side smoke tests; functional QA (that's the regression
suite); exploratory testing (use SBTM).

## Setup

```bash
# Loom CLI for async walkthroughs
brew install --cask loom

# Notion / Confluence for sign-off page (via notion-mcp)
# Jira / Linear ticket integration (via jira-mcp / linear-mcp)
```

Auth: Notion API token (in notion-mcp); Loom API key optional.

## Common recipes

### Recipe 1 — UAT scenario template

```markdown
# UAT Scenario — <Feature> — UAT-<slug>-<NN>

## Scenario name
Add a new payment method as a paying customer.

## Persona
Paying customer "Alice" (existing account, has 1 saved card).

## Acceptance criteria covered
- AC-1: User can add a new card via Stripe Elements
- AC-2: New card becomes default; receipt of next charge reflects this
- AC-3: User can remove old card after add

## Pre-conditions
- Logged in as alice@example.com on staging
- Stripe test mode active

## Steps
1. Navigate to Settings → Payment Methods
2. Click "Add card"
3. Enter Stripe test card 4242 4242 4242 4242, exp 12/30, CVC 123
4. Submit
5. Verify card appears in list, marked "Default"
6. Remove old card via trash icon

## Expected outcome
- Success toast: "Card added"
- Old card no longer in list
- Next charge (manual trigger via admin) uses new card

## Evidence to capture
- Loom 60-second walkthrough
- Screenshot of payment-methods page before and after
- Stripe dashboard screenshot of new payment method

## Sign-off
- [ ] PM (Bob)
- [ ] Support lead (Carol)
- [ ] QA (Dan) — facilitator
```

### Recipe 2 — UAT plan structure (Notion / Confluence page)

```markdown
# UAT — <Feature> — <release>

## Owner
QA: <name>  PM: <name>  EM: <name>

## Schedule
- Scenarios drafted: <date>
- Stakeholder kickoff: <date>
- Execution window: <date range>
- Sign-off target: <date>

## Scenarios
| ID | Scenario | Owner | Status |
|---|---|---|---|
| UAT-pm-01 | Add payment method | PM | Pending |
| UAT-pm-02 | Remove last payment method (error path) | Support | Pending |
| UAT-pm-03 | Default card on subscription renewal | PM | Pending |

## Environment
- URL: https://staging.example.com
- Account: alice@example.com / Test1234!
- Test data: 1 default card already on file
- Stripe mode: test

## Sign-off
- [ ] PM
- [ ] Support
- [ ] Sales / Customer Success
- [ ] Compliance (if regulated)
- [ ] QA — final sign

## Evidence repo
Loom videos: <link>  Screenshots: <link>  Jira tickets: <filter link>
```

### Recipe 3 — Loom async walkthrough

```bash
# Record on staging
loom record --output uat-walkthrough.mp4

# Or via Loom desktop — share link with stakeholders
# Naming convention: UAT-<feature>-<scenario-id>-<actor>
```

Share link in Notion sign-off page. Async stakeholders watch + check the box.

### Recipe 4 — Stakeholder kickoff agenda

```markdown
# UAT Kickoff — <date>

## Agenda (30 min)
- 5m: Feature recap (PM)
- 10m: Demo on staging (QA)
- 5m: UAT scenarios walkthrough (QA)
- 5m: Sign-off mechanics (QA)
- 5m: Q&A

## Decisions to make
- Severity thresholds — any S1/S2 blocks launch
- Async vs synchronous — Loom walkthrough vs live demo
- Sign-off deadline — <date>
- Escape route if HOLD — push 1 sprint? feature flag?
```

### Recipe 5 — UAT feedback capture template

```markdown
## UAT Feedback — <scenario-id>

**Stakeholder:** Bob (PM)
**Date:** 2026-06-11
**Verdict:** PASS / PASS-WITH-NOTES / FAIL

### Notes
- ✓ Add card works as expected
- ✓ Default card flag updates
- ⚠ Removing all cards shows "0 cards" but no CTA to add — minor UX
- ✗ Receipt email shows old card last-4 instead of new — bug

### Bugs filed
- UAT-pm-01-B1 — receipt email — S2 — PROJ-1284

### Sign-off
- [ ] Conditional on B1 fix
```

### Recipe 6 — Acceptance criteria → UAT scenario mapping

```markdown
| AC ID | Scenario(s) | Coverage |
|---|---|---|
| AC-1 | UAT-pm-01 | full |
| AC-2 | UAT-pm-01, UAT-pm-03 | full |
| AC-3 | UAT-pm-01 | full |
| AC-4 (rate limit) | UAT-pm-04 | partial — manual only |
```

Tied to the test plan's AC table — sign-off has 1:1 coverage.

### Recipe 7 — Sign-off mechanics in Jira/Linear

```markdown
## Per-scenario subtask
- Title: "UAT-pm-01 — Add payment method"
- Assignee: PM
- Acceptance: Loom + checkbox + bug filed if any
- Status flow: To Do → In Review → Approved | Rejected
```

```python
# Pseudo via jira-mcp:
# Create issue "UAT-<scenario>" linked to parent epic
# On approval, transition + leave comment with Loom URL
```

### Recipe 8 — Async UAT (distributed team)

```markdown
## Async UAT — for distributed / cross-tz team
- Day 1: QA shares Notion page + Loom of demo
- Day 2-3: Stakeholders execute scenarios at their pace
- Day 4: QA chases pending; daily Slack ping
- Day 5: All sign-off captured; HOLD decisions documented
```

### Recipe 9 — Sign-off PR (Git-tracked evidence)

```markdown
# .github/PULL_REQUEST_TEMPLATE/uat_signoff.md
## UAT Sign-off — <feature>

- [ ] All scenarios PASS or PASS-WITH-NOTES
- [ ] All S1/S2 bugs closed
- [ ] PM approved (via Notion page)
- [ ] Support approved
- [ ] QA approved

Notion page: <link>
Loom walkthroughs: <link>
Open issues: <filter>
```

### Recipe 10 — UAT escape-rate metric

After release, track:

```markdown
## UAT escape rate (post-release defects not caught in UAT) — Sprint <NN>
- Defects found post-release: 3 (1 S2 + 2 S3)
- Scenarios that should have caught: UAT-pm-02 (S2 missed)
- Action: add edge case "remove last card" to UAT-pm-02 next release
```

### Recipe 11 — Compliance / regulated UAT

```markdown
## Regulated UAT add-ons
- Auditor-friendly evidence: signed PDF (Notion export)
- Per-scenario timestamp + signer name + signer role
- Retention: 7 years per SOX / 10 years per FDA (depends on regulation)
- Storage: Git + WORM bucket; not Notion alone
```

### Recipe 12 — Beta UAT (external customers)

```markdown
## Beta UAT
- Feature flag: `beta-payments-v2` (default-off; ON for 5 customer accounts)
- Feedback form: Notion-embed Typeform
- Weekly digest: top 5 themes + bugs filed
- Exit criteria: 80%+ "would use again"; 0 critical bugs
- Sunset: feature flag default-on; remove flag in 30 days
```

## Examples

### Example 1: Greenfield feature — full UAT

**Goal:** Ship "Bulk export" with sign-off from 3 stakeholders.

1. PM drafts 5 scenarios from AC (Recipe 1); QA reviews.
2. Notion UAT page created (Recipe 2); linked in epic.
3. Kickoff meeting (Recipe 4); walkthrough Loom (Recipe 3).
4. Stakeholders execute over 3 days; capture feedback (Recipe 5).
5. Bugs filed S1/S2 → fix → re-verify; PASS-WITH-NOTES allowed for S3.
6. Sign-off PR (Recipe 9) merged when all green; release proceeds.

### Example 2: Hotfix — abbreviated UAT

**Goal:** Critical fix to ship within 4 hours.

1. QA drafts 1 scenario covering the fix + 1 regression scenario.
2. Loom of fix on staging — 5 min.
3. PM + EM async sign-off via Slack thread (captured as Notion comment).
4. Deploy; canary 30 min; full rollout.
5. Post-incident: add scenario to standing UAT for that feature.

## Edge cases / gotchas

- **Stakeholders skip UAT** — make sign-off mechanical (checkbox + Loom);
  6 hours per release saves 60 hours of post-release escalation.
- **Scenarios that read like specs** — UAT is "does this feel right", not
  "does each field validate". Keep scenarios outcome-focused.
- **No environment** — staging that mirrors prod is the bare minimum; if
  team lacks one, that's the first ask before UAT can be planned.
- **PM tests as "user"** — PM is not the user. Use real users where possible
  (beta) or proxy users (customer success).
- **Conflating UAT with QA** — QA already passed regression; UAT is the
  business owner's check.
- **No defined exit** — "is this good?" never ends. Define PASS / FAIL
  criteria up front.
- **Sign-off in Slack thread alone** — gone in 14 days on free tier. Always
  mirror to Notion / Confluence / Jira.
- **External beta with PII** — sign NDA + DPA; mask production data; never
  share screenshots with real PII.
- **Loom retention** — Loom free tier auto-deletes after 90 days. Pay for
  Workspace or export critical UAT videos to S3 / Google Drive.
- **Sign-off without bugs filed** — stakeholder said "kind of works" — that's
  a bug. Capture every concern; severity is for later.

## Sources

- [Atlassian — User Acceptance Testing](https://www.atlassian.com/agile/project-management/user-acceptance-testing)
- [Scrum Guide — Definition of Done](https://www.scrumguides.org/scrum-guide.html)
- [Ministry of Testing — UAT essentials](https://www.ministryoftesting.com/dojo/lessons/user-acceptance-testing)
- [Atlassian — Definition of Done](https://www.atlassian.com/agile/project-management/definition-of-done)
- [Loom for async walkthroughs](https://www.loom.com/)
- [Notion docs](https://www.notion.so/help)
- [Confluence team collaboration](https://www.atlassian.com/software/confluence)
- [SOX / regulated evidence retention](https://www.sarbanes-oxley-101.com/)
