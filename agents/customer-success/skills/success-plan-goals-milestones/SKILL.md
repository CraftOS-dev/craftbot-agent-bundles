<!--
Source: https://docs.vitally.io/reference/projects + https://help.catalyst.io/ + https://developers.notion.com/ + https://help.fathom.video/en/articles/8430832-fathom-api
-->
# Success Plan — Goals / Milestones / Criteria — SKILL

Author and operationalize the customer success plan: a strict goal -> milestone -> success-criteria -> owner -> due-date structure tied to customer-measurable outcomes (not feature lists). Push to Vitally Projects (modern CSP), Catalyst Playbook Assignments (enterprise), Gainsight Success Plans (enterprise heavy), or Notion DB (no-CSP fallback). Refresh on QBR cadence; tag status Green/Yellow/Red.

## When to use

- **Net-new account onboarding** — within Day 0-7, draft success plan v1.
- **Stale plan refresh** — plan hasn't been edited in 60+ days while customer is mid-onboarding.
- **Pre-QBR prep** — refresh plan ahead of T-7 to align deck data with plan status.
- **Save-play customer** — at-risk customer with no documented outcomes; CSM needs to capture them fast.
- **Renewal positioning** — T-90 review of plan outcomes hits to justify uplift.

This skill **focuses on the artifact itself** (the plan structure + outcomes). For scheduling kickoffs/check-ins around it, use `customer-onboarding-day-0-90`. For QBR delivery, use `qbr-scheduling-facilitation`.

Trigger phrases: "success plan", "success plan template", "outcomes for this customer", "goal milestone", "draft a success plan".

## Setup

```bash
# Vitally (modern)
export VITALLY_SUBDOMAIN="acme"
export VITALLY_API_KEY="<key>"

# Catalyst / Gainsight (enterprise)
export CATALYST_API_KEY="<key>"
export GAINSIGHT_DOMAIN="acme.gainsightcloud.com"
export GAINSIGHT_TOKEN="<token>"

# Notion (fallback / always-on)
# notion-mcp already wired in agent.yaml

# Fathom (kickoff transcript -> plan inputs)
export FATHOM_API_KEY="<key>"
```

Workspace prerequisites:
- A Notion "Success Plans" database with schema: Customer (Title), CSM (People), Customer Owner (Text), Tier (Select), Last Reviewed (Date), Status (Status: Green/Yellow/Red), Outcomes (Relation -> Outcomes DB).
- A child "Outcomes" database with: Outcome Name, Owner (Customer / CSM), Metric, Target Value, Target Date, Status, Milestones (Relation -> Milestones DB), Risks (Text).
- In Vitally, "Project Templates" configured with default milestones for each tier.

## Plan structure (golden rule: outcomes, not features)

```
Goal -> Outcome (customer-measurable) -> Milestones (CSM- or customer-owned) -> Success criteria (metric + target) -> Owner -> Due date -> Status (G/Y/R) -> Risks
```

**BAD:** "Customer will adopt feature X."
**GOOD:** "Customer will reduce support ticket volume from 50/week to 35/week by end of Q3 via X."

## Common recipes

### Recipe 1: Author plan v1 from kickoff transcript

```bash
# Pull transcript via Fathom
curl -sS "https://api.fathom.video/external/v1/meetings/$MEETING_ID/transcript" \
  -H "X-Api-Key: $FATHOM_API_KEY" > kickoff.txt

# Feed to Claude with this prompt:
# "Extract 3 customer-measurable outcomes from this kickoff transcript.
#  For each: outcome name, current state, target state, target date, owner,
#  3-5 milestones, 1-2 risks. Output JSON matching schema."
```

The output JSON powers Recipe 2 (push to CSP) or Recipe 6 (Notion).

### Recipe 2: Push plan to Vitally as a Project

```bash
curl -sS -X POST "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/accounts/external/$CUSTOMER_ID/projects" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Success Plan v1 - Reduce ticket volume by Q3",
    "description": "Outcome: reduce support tickets from 50/wk to 35/wk by 2026-09-30",
    "owner": "csm@acme.com",
    "milestones": [
      {"name": "Workflow automation v1 deployed", "dueDate": "2026-07-01"},
      {"name": "Self-serve docs published to 50% top-ticket categories", "dueDate": "2026-08-01"},
      {"name": "Macro library audited + 5 new macros shipped", "dueDate": "2026-08-15"},
      {"name": "Ticket volume measured (target <= 35/wk for 4 consecutive weeks)", "dueDate": "2026-09-30"}
    ],
    "metadata": {
      "outcome_metric": "tickets_per_week",
      "current_value": 50,
      "target_value": 35,
      "owner_customer": "Champion Jane",
      "risks": "Macro adoption dependent on agent training; CSAT may dip during workflow rollout"
    }
  }'
```

Doc: https://docs.vitally.io/reference/projects

### Recipe 3: Push to Catalyst as Playbook Assignment

```bash
curl -sS -X POST "https://api.catalyst.io/v1/playbooks/$SUCCESS_PLAN_PLAYBOOK_ID/assignments" \
  -H "Authorization: Bearer $CATALYST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": "'$CUSTOMER_ID'",
    "owner_email": "csm@acme.com",
    "variables": {
      "outcome_metric": "tickets_per_week",
      "current_value": "50",
      "target_value": "35",
      "target_date": "2026-09-30"
    }
  }'
```

Doc: https://help.catalyst.io/

### Recipe 4: Push to Gainsight Success Plan

```bash
curl -sS -X POST "https://$GAINSIGHT_DOMAIN/v1/api/cta" \
  -H "accesskey: $GAINSIGHT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": "'$CUSTOMER_ID'",
    "type": "Objective",
    "name": "Reduce ticket volume to 35/wk by Q3",
    "priority": "High",
    "due_date": "2026-09-30",
    "tasks": [
      {"name": "Workflow automation v1 deployed", "due_date": "2026-07-01"},
      {"name": "Self-serve docs published", "due_date": "2026-08-01"}
    ]
  }'
```

Doc: https://support.gainsight.com/

### Recipe 5: Push plan to ChurnZero as Plan + Tasks

```bash
# ChurnZero has Success Plans + Tasks
curl -sS -X POST "https://api.churnzero.net/i/v1/accounts/$CUSTOMER_ID/success_plans" \
  -H "Authorization: Bearer $CHURNZERO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Q3 Outcomes", "owner_email": "csm@acme.com", "due_date": "2026-09-30"}'
```

Doc: https://help.churnzero.com/

### Recipe 6: Notion fallback - one page per plan

```python
# notion-mcp create_page
notion.create_page(
    parent={"database_id": SUCCESS_PLANS_DB_ID},
    properties={
        "Customer": {"title": [{"text": {"content": "Acme Corp"}}]},
        "CSM": {"people": [{"id": csm_user_id}]},
        "Tier": {"select": {"name": "Enterprise"}},
        "Last Reviewed": {"date": {"start": "2026-06-11"}},
        "Status": {"status": {"name": "Green"}},
    },
    children=[
        {"object": "block", "type": "heading_2",
         "heading_2": {"rich_text": [{"text": {"content": "Outcome 1: Reduce tickets to 35/wk"}}]}},
        {"object": "block", "type": "bulleted_list_item",
         "bulleted_list_item": {"rich_text": [{"text": {"content": "Why it matters: $80k annual support cost reduction"}}]}},
        {"object": "block", "type": "to_do",
         "to_do": {"rich_text": [{"text": {"content": "Workflow automation v1 deployed (due 2026-07-01)"}}], "checked": False}},
    ],
)
```

### Recipe 7: Tag status from milestone completion

```sql
-- Derive plan status from milestone state
SELECT
  plan_id,
  customer_id,
  count(*) AS total,
  count(*) FILTER (WHERE completed_at IS NOT NULL) AS done,
  count(*) FILTER (WHERE completed_at IS NULL AND due_date < CURRENT_DATE) AS overdue,
  CASE
    WHEN count(*) FILTER (WHERE completed_at IS NULL AND due_date < CURRENT_DATE) >= 2 THEN 'Red'
    WHEN count(*) FILTER (WHERE completed_at IS NULL AND due_date < CURRENT_DATE) = 1 THEN 'Yellow'
    ELSE 'Green'
  END AS status
FROM success_plan_milestones
GROUP BY plan_id, customer_id;
```

Write status back to CSP via Recipe 2/3/4 pattern (`PATCH` instead of `POST`).

### Recipe 8: Pre-QBR plan refresh checklist

For each outcome on the plan:
1. Pull current metric value from `postgresql-mcp` / `posthog-mcp`.
2. Compare to target_value + target_date.
3. Compute % progress.
4. Update milestone statuses.
5. Set plan-level Status (Recipe 7).
6. Write back to CSP and Notion mirror.

Output goes into QBR slide 6 ("Open items - 3 in-flight outcomes").

### Recipe 9: Add a mid-cycle outcome

```bash
# Append to Vitally project
curl -sS -X POST "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/projects/$PROJECT_ID/milestones" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" \
  -H "Content-Type: application/json" \
  -d '{"name": "New outcome: SSO rolled out to 100% workforce", "dueDate": "2026-08-15"}'
```

When the customer's business changes (acquisition, leadership shift), add an outcome - don't rewrite the plan.

### Recipe 10: Archive on renewal

```bash
# Vitally - close project, create new one for next year
curl -sS -X PATCH "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/projects/$PROJECT_ID" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" \
  -d '{"status": "Closed", "closedAt": "2026-09-30T00:00:00Z", "outcome": "Achieved 38/wk (target 35/wk; 76% to goal)"}'
```

Then Recipe 2 again for year 2 plan, referencing year 1 outcomes in description.

## Examples

### Example 1: Convert feature-list plan to outcomes-led

**Goal:** Plan currently reads "Adopt features X, Y, Z." CSM needs to fix before QBR.

**Steps:**
1. Pull customer ticket data + product analytics + last QBR notes.
2. Identify the *business* problem each feature was supposed to solve.
3. Rewrite outcomes: "Reduce time-to-publish from 4h to 1h by Q3 via X workflow" rather than "Adopt X."
4. Recipe 2 -> push new outcomes to Vitally.
5. Slack CSM + champion: "Updated success plan ahead of QBR; review by EOD."

**Result:** Plan tied to measurable customer business outcomes.

### Example 2: Stalled plan rescue

**Goal:** Plan last edited 90 days ago; customer at-risk.

**Steps:**
1. Recipe 7 - status is Red.
2. Slack CSM lead + auto-create Linear "save plan" issue (handoff to `churn-save-motion-intervention`).
3. Re-draft plan v2 from latest QBR transcript (Recipe 1).
4. Push to CSP and Notion (Recipe 2 + Recipe 6).
5. Book customer-side check-in via Calendly (single-use link).

**Result:** Plan refreshed; save play armed.

## Edge cases / gotchas

- **Outcomes must be customer-measurable** — "Customer is happy" is not an outcome. "Customer NPS >= 8 sustained 90d" is.
- **One owner per milestone** — shared ownership = no ownership. Designate either CSM or customer per item.
- **No more than 3 outcomes** — past 3, focus is lost and plan becomes a checklist. Park extras for next QBR.
- **Don't backdate plans** — plan v1 in month 4 is suspicious; document why and what changed.
- **Risks section is required** — "no risks" means you haven't asked the customer. Force at least 1 risk per outcome.
- **CSP terminology mismatch** — Vitally "Projects", Catalyst "Playbook Assignments", Gainsight "Success Plans / CTAs", ChurnZero "Success Plans". Mental model = same; UI labels differ.
- **Notion + CSP mirror drift** — if you mirror, designate one as source-of-truth and reverse-ETL from there. Recommended: CSP = source, Notion = view.
- **Plan rewrite on champion change** — new champion has different KPIs. Plan needs a v2 not a continuation.
- **Outcome metric not in warehouse** — if you don't have the metric instrumented, plan is unmeasurable; flag instrumentation as Milestone 1.
- **Customer pushback on metric targets** — they want soft targets ("improve a lot"). Push back; document target as customer's own number.

## Sources

- [Vitally Projects API reference](https://docs.vitally.io/reference/projects)
- [Vitally Projects in product docs](https://docs.vitally.io/en/articles/9880654-rest-api-accounts)
- [Catalyst Playbooks](https://help.catalyst.io/)
- [Gainsight CTAs / Success Plans](https://support.gainsight.com/gainsight_nxt/CTAs_and_Playbooks)
- [ChurnZero Success Plans](https://help.churnzero.com/)
- [Notion API create page](https://developers.notion.com/reference/post-page)
- [Fathom API meeting transcripts](https://help.fathom.video/en/articles/8430832-fathom-api)
- [Outcome-led success planning (Gainsight blog)](https://www.gainsight.com/guides/customer-success-plan/)
