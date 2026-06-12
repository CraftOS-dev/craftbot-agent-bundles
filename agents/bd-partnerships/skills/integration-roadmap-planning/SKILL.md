<!--
Source: https://www.crossbeam.com/blog/integration-partnerships/ + https://www.tackle.io/playbook
Joint integration roadmap planning with product-manager hand-off (June 2026 SOTA).
-->
# Integration Roadmap Planning — SKILL

Plan, scope, and ship integration partnerships with a **roadmap, not a press release**. Quarterly joint roadmap session: identify use cases, map APIs on both sides, define data-flow architecture, contract API versioning + SLA, agree launch + GTM, set integration health monitoring. Tracked in Linear / Jira / Notion. Cross-agent hand-off to `product-manager` for scoping + engineering capacity; `tech-lead-cto` for technical architecture decisions.

## When to use

- **New integration partnership going from agreement → build phase**.
- **Quarterly joint roadmap session** with strategic integration partner.
- **API versioning + deprecation planning**.
- **Defining post-launch monitoring** (cross-link to `partnerstack-tackle-channel-management` for execution).
- **Integration scope refresh** — quarterly priority revision.
- **Trigger phrases**: "integration roadmap", "joint roadmap with X", "API access for partner", "deprecation notice", "integration scope".

Do NOT use this skill for: **API engineering work itself** (defer to `product-manager` + `tech-lead-cto`); **the actual integration code** (engineering team); **post-launch health monitoring** (use `partnerstack-tackle-channel-management`); **co-marketing campaign** for the integration (use `co-marketing-campaign-design`).

## Setup

```bash
export MATON_API_KEY="<key>"           # for Linear/Jira via api-gateway if configured
export LINEAR_API_KEY="<key>"
# Or use linear-mcp / jira-mcp directly
# Notion for the roadmap doc itself
```

## Common recipes

### Recipe 1: Joint roadmap kickoff agenda (template, write to Notion)

```yaml
joint_roadmap_kickoff:
  duration: "90 min"
  attendees:
    vendor_side: ["BD lead", "Product manager", "Engineering lead", "DevRel"]
    partner_side: ["BD lead", "Product manager", "Engineering lead"]
  agenda:
    - "5 min — Recap partnership + business goals"
    - "15 min — Joint customer interviews (read-out)"
    - "20 min — Use case prioritization (5-7 use cases ranked)"
    - "15 min — API surface mapping (both sides)"
    - "15 min — Data-flow architecture sketch"
    - "10 min — Launch plan + GTM commitment"
    - "10 min — Monitoring + SLAs + ownership"
  outputs:
    - "Top-3 use cases for Phase 1 ship"
    - "API surface diagram (drawio-mcp)"
    - "Joint roadmap doc (Notion)"
    - "Tickets created in Linear / Jira"
    - "DRIs assigned both sides"
```

### Recipe 2: Use case prioritization framework

```yaml
use_case_prioritization:
  scoring:
    customer_demand: "1-5 from joint customer interviews"
    revenue_impact: "1-5 from joint pipeline projection"
    engineering_effort: "1-5 (1 = small, 5 = large) — both sides"
    risk: "1-5 (1 = low, 5 = high) — security, compliance, deprecation"
    time_to_value: "1-5 (1 = same day, 5 = > 90 days)"

  composite_score: "customer_demand + revenue_impact - engineering_effort - risk - time_to_value"

  decision:
    score_> 5: "Phase 1 — ship this quarter"
    2-5: "Phase 2 — next quarter"
    < 2: "Backlog — re-evaluate next year"
```

Example output:

```yaml
use_cases:
  - name: "Sync joint customers' deal-stage between Acme CDP + Brand CRM"
    customer_demand: 5
    revenue_impact: 4
    engineering_effort: 2
    risk: 1
    time_to_value: 2
    composite: 4
    decision: "Phase 1"
  - name: "Two-way event streaming"
    customer_demand: 4
    revenue_impact: 5
    engineering_effort: 5
    risk: 3
    time_to_value: 4
    composite: -3
    decision: "Phase 2"
```

### Recipe 3: API surface mapping (per use case)

```yaml
use_case_1_deal_stage_sync:
  brand_apis_needed:
    read:
      - "GET /crm/v3/objects/deals?associations=companies — list deals + customer association"
      - "GET /crm/v3/objects/deals/<id>/history — stage change history"
    write:
      - "PATCH /crm/v3/objects/deals/<id> — update deal stage from Acme"
    auth_pattern: "OAuth scope crm.objects.deals.write"
    rate_limits: "100 req/10s per app"
  acme_apis_needed:
    read:
      - "GET /v2/customers/<id>/profile"
      - "GET /v2/customers/<id>/timeline"
    write:
      - "POST /v2/customers/<id>/events"
    auth_pattern: "API key + customer-bearer-token"
    rate_limits: "60 req/min per customer"
  data_residency: "EU customers stay in EU regions on both sides"
  pii_in_scope: "Customer email + name; documented in DPA"
```

### Recipe 4: Data flow diagram (DrawIO)

```yaml
# In drawio-mcp, create:
data_flow:
  description: "Bidirectional deal-stage sync"
  components:
    - "Brand CRM (source for stage change)"
    - "Brand webhook → Joint Integration Service (lightweight)"
    - "Joint Integration Service → Acme API"
    - "Acme stores event in customer timeline"
    - "Reverse: Acme webhook → Joint Integration Service → Brand CRM"
  observability:
    - "Sentry tagged integration_partner_id=acme"
    - "PostHog event integration_event_processed"
    - "Latency target p95 < 500ms end-to-end"
  failure_modes:
    - "Brand API rate-limited → queue with exponential backoff"
    - "Acme API down → buffer events for 24h, alert if longer"
    - "Auth token expired → automated refresh; alert if fail"
```

Render to PNG via `drawio-mcp`; embed in roadmap doc.

### Recipe 5: API versioning + SLA contract

```yaml
api_versioning_contract:
  current_version: "Brand v3 (stable), Acme v2 (stable)"
  next_version: "Brand v4 in beta Aug 2026, Acme v3 in dev"
  deprecation_policy:
    breaking_change_notice: "180 days written notice to all integration partners"
    sunset_period: "365 days from notice"
    parallel_support: "Both versions live during transition"
  sla:
    uptime_target: "99.9% per quarter"
    error_rate_target: "< 0.5% per quarter"
    response_time_p95: "< 500ms"
    incident_notification: "Status page + Slack to partner contact within 15 min"
  backwards_compatibility: "Additive changes only in v3.x; breaking changes only at major version boundary"
```

This goes in the Integration Partnership Agreement (see `referral-affiliate-channel-oem-agreement-structuring`).

### Recipe 6: Create tickets in Linear (cross-agent hand-off)

```bash
# Linear API — create issue + assign team
curl -X POST "https://api.linear.app/graphql" \
  -H "Authorization: $LINEAR_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "query":"mutation IssueCreate($input: IssueCreateInput!) { issueCreate(input: $input) { issue { id identifier title } } }",
    "variables":{
      "input":{
        "teamId":"<team-id>",
        "title":"Integration: Acme CDP — deal-stage sync (Phase 1)",
        "description":"Build bidirectional deal-stage sync between Brand CRM and Acme CDP per joint roadmap doc [Notion link].\n\nDRI: <pm-name>\nAcme DRI: <their-pm>\nTarget ship: Sep 30, 2026",
        "priority":2,
        "labelIds":["integration","partner-acme"],
        "projectId":"<integration-partnerships-project>"
      }
    }
  }'
```

Reference: https://developers.linear.app/docs/graphql/working-with-the-graphql-api.

### Recipe 7: Jira fallback (alternative tracker)

```bash
curl -X POST "https://your-domain.atlassian.net/rest/api/3/issue" \
  -H "Authorization: Basic $(echo -n email:apitoken | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "fields":{
      "project":{"key":"INT"},
      "summary":"Integration: Acme CDP — deal-stage sync (Phase 1)",
      "description":{"type":"doc","version":1,"content":[
        {"type":"paragraph","content":[{"type":"text","text":"Build bidirectional deal-stage sync. See [Notion roadmap doc]."}]}
      ]},
      "issuetype":{"name":"Story"},
      "labels":["integration","partner-acme"]
    }
  }'
```

### Recipe 8: Roadmap doc (canonical Notion template)

```yaml
integration_roadmap_doc:
  partner: "Acme Analytics"
  start_quarter: "2026-Q3"
  business_goal: "200 joint customers using integration by Q4; $1.2M joint pipeline"

  phase_1_ship_by_2026_09_30:
    use_cases:
      - "Bidirectional deal-stage sync"
      - "Joint customer onboarding flow"
    vendor_engineering_estimate: "3 engineer-weeks"
    partner_engineering_estimate: "2 engineer-weeks"
    qa_plan: "Co-developed test suite; sandbox + production smoke tests"
    launch_announcement: "Joint blog post + customer webinar; cross-team comms"

  phase_2_ship_by_2026_12_31:
    use_cases:
      - "Two-way event streaming"
      - "Joint segmentation builder"
    pre_work: "Architecture spike Q3; finalize scope by Oct 1"

  phase_3_ship_by_2027_q1_q2:
    candidate_use_cases:
      - "ML-shared model training"
      - "Joint pricing endpoint"

  metrics:
    - "Joint customers with integration active (target 60% of joint customers by Q4)"
    - "API call volume + error rate"
    - "Joint pipeline + closed-won attributed to integration"

  monitoring_stack:
    error_tracking: "Sentry tagged integration_partner_id=acme"
    adoption_analytics: "PostHog event integration_action_taken"
    health_digest: "Weekly Slack to both BD + PM teams"

  ownership:
    vendor_dri_pm: "<pm-name>"
    vendor_dri_eng: "<eng-lead>"
    partner_dri_pm: "<their-pm>"
    partner_dri_eng: "<their-eng-lead>"
    bd_owner: "<bd-lead>"
```

### Recipe 9: Weekly cross-team standup (recurring)

```yaml
weekly_sync:
  cadence: "Wednesdays 30 min"
  format: "Round-table per workstream"
  attendees: ["BD leads both sides","PMs both sides","DRI engineers if blocking"]
  agenda:
    - "5 min — Customer feedback (joint customers using or asking)"
    - "10 min — Workstream status (per Phase 1 use case)"
    - "10 min — Blockers (API gaps, design decisions, customer escalations)"
    - "5 min — Next-week commitments"
  notes_doc: "Notion linked from roadmap doc"
  action_items_tracker: "Linear / Jira tickets"
```

### Recipe 10: Launch readiness checklist

```yaml
launch_readiness:
  technical:
    - "Both APIs documented + versioned"
    - "Sandbox available for joint customers"
    - "Production smoke tests pass"
    - "Error monitoring tagged integration_partner_id=acme"
    - "Rate-limit handling validated"
    - "DPA / privacy review signed off"
  product:
    - "Setup flow tested with 3 internal users"
    - "Documentation published on both sides"
    - "Pricing impact understood (if any)"
    - "Customer success team briefed"
  gtm:
    - "Co-marketing brief signed off (per co-marketing-campaign-design)"
    - "Joint customer webinar scheduled"
    - "Pricing page updated on both sides"
    - "Sales decks updated"
  monitoring:
    - "Health dashboard live"
    - "Weekly digest mailing list configured"
    - "Escalation path documented"
  legal:
    - "Integration partnership agreement signed"
    - "DPA in place if PII shared"
    - "Brand-usage guidelines exchanged"
```

### Recipe 11: Quarterly roadmap review (recurring)

```yaml
quarterly_review:
  cadence: "Last Thursday of quarter, 60 min"
  attendees: "PMs + Eng leads + BD leads both sides"
  agenda:
    - "Status: what shipped this Q"
    - "Adoption: joint customer install + active count"
    - "Pipeline: integration-attributed pipeline + closed-won"
    - "Issues: top 3 customer escalations + RCA"
    - "Next Q priorities: use case re-rank per Recipe 2"
    - "API roadmap from both sides (breaking changes, new endpoints)"
    - "Joint marketing alignment"
  outputs:
    - "Updated roadmap doc (Recipe 8)"
    - "New Linear / Jira tickets"
    - "QBR-ready slide for partner scorecard"
```

### Recipe 12: Deprecation notice handoff

```yaml
deprecation_workflow:
  trigger: "Vendor product team plans breaking change to API"
  step_1: "vendor PM notifies BD partnerships lead 270 days before sunset"
  step_2: "BD reviews all integration partners using deprecated endpoint via warehouse query (postgresql-mcp)"
  step_3: "Formal deprecation notice email to each affected partner — 180 days notice"
  step_4: "Joint plan: parallel-support window, migration guide, who-pays-for-engineering"
  step_5: "Weekly sync on migration progress (Recipe 9 cadence)"
  step_6: "Sunset old endpoint; confirm all partners migrated"
```

Cross-team: `product-manager` provides deprecation rationale; `tech-lead-cto` reviews migration path; partner side does their own work.

## Examples

### Example 1: New integration partnership kickoff

**Goal:** Integration agreement signed last week with Acme; need roadmap session + tickets created by end of week.

**Steps:**
1. Day 1 — Recipe 1 — Kickoff scheduled; pre-read sent.
2. Day 2 — 90-min kickoff held (Zoom).
3. Recipe 2 — Use cases prioritized; top 3 in Phase 1.
4. Recipe 3 + 4 — API mapping + data flow diagram drafted in `drawio-mcp`.
5. Recipe 5 — API versioning + SLA contract added to integration agreement.
6. Recipe 6 — Linear tickets created with DRI assignments.
7. Recipe 8 — Roadmap doc written in Notion + linked from partner DB.
8. Day 5 — Recipe 9 — Weekly sync calendar invites set.

**Result:** Partnership transitions from signed agreement → in-flight engineering; both sides aligned.

### Example 2: Quarterly review + Phase 2 scope decisions

**Goal:** End of Q3; review what shipped, re-rank Phase 2.

**Steps:**
1. Recipe 11 — Quarterly review scheduled.
2. Phase 1 status: deal-stage sync shipped; joint customer onboarding shipped.
3. Adoption: 35% of joint customers active (target was 40% — slight miss).
4. Customer feedback: top ask is two-way event streaming (originally Phase 2).
5. Re-score Phase 2: two-way streaming moves up; "joint segmentation builder" moves to Phase 3.
6. Recipe 6 — New Linear tickets for Phase 2 commit.
7. Recipe 8 — Roadmap doc updated.

**Result:** Roadmap responsive to customer signal; team aligned on next-Q deliverables.

### Example 3: Deprecation notice to integration partner

**Goal:** Vendor product team is sunsetting deprecated `/v2/events` endpoint in 9 months; integration partner uses it.

**Steps:**
1. Recipe 12 step 1 — vendor PM flags BD.
2. Recipe 12 step 2 — warehouse query: 4 integration partners use `/v2/events`.
3. Step 3 — formal email to each: deprecation timeline + replacement endpoint.
4. Step 4 — joint plan with Acme PM: 4 engineer-weeks of work on their side; we offer 2 weeks DevRel support.
5. Step 5 — weekly sync for migration tracking.
6. Day 270 — migration complete; old endpoint sunset.

**Result:** Customer-disrupting deprecation handled cleanly without integration-partner outage.

## Edge cases / gotchas

- **"Press release" trap** — partner wants to launch announcement BEFORE engineering builds. Resist. Joint announcement only after Phase 1 ships.
- **API rate-limit asymmetry** — vendor allows 100 req/10s; partner allows 60 req/min. Lowest common denominator gates throughput. Plan for it.
- **Auth-token-storage liability** — if vendor stores partner's customer tokens, vendor is liable for breach. Use OAuth refresh tokens with minimum scopes; don't store long-lived tokens.
- **Joint customer onboarding complexity** — customer signs up via partner UI BUT data lands in vendor — confusing onboarding flow. Co-design the customer experience.
- **PII / DPA** — most integrations exchange PII. DPA + privacy review BEFORE engineering.
- **Sandbox environment drift** — partner sandbox out of sync with production. Schedule monthly sandbox refresh.
- **Engineering capacity** is the #1 schedule risk — partner committed 2 weeks but only delivered 1; project slips. Build in 30% buffer; track weekly.
- **Cross-team dependencies** — vendor PM is busy on roadmap; partner PM is busy. Make BD the escalation owner; weekly sync is the forcing function.
- **Customer expectations of integration depth** — joint customers want more than initial scope. Manage expectations with phased messaging.
- **Versioning + parallel support cost** — running v3 + v4 in parallel for 365 days is real engineering cost. Budget for it.
- **Co-developed connector code** — who owns the IP? Per Recipe 6 of `referral-affiliate-channel-oem-agreement-structuring`, default to MIT license for jointly-developed code.
- **Partner side gets distracted** — strategic priority shifts; integration de-prioritized mid-build. BD must catch early.
- **Customer escalations route differently** — joint customer has issue: who owns first response? Document in roadmap doc Recipe 8.
- **Deprecation notice timing** — earlier is better; 180 days is the floor. Some partners need 270+.
- **Migration cost negotiation** — when vendor deprecates, partner asks vendor to fund migration. Sometimes reasonable; document in integration agreement.
- **Joint roadmap as competitive intel** — be careful what's shared cross-partner. Don't tell Partner A about Partner B's roadmap.
- **Integration health is post-launch territory** — once shipped, monitoring + adoption + RCA become `partnerstack-tackle-channel-management` skill.
- **Cross-agent coordination**: this skill talks to `product-manager` (scoping) and `tech-lead-cto` (architecture) — use Linear ticket as the cross-agent artifact; clear ownership prevents drops.

## Sources

- Crossbeam integration partnerships: https://www.crossbeam.com/blog/integration-partnerships/
- Tackle.io integration playbook: https://www.tackle.io/playbook
- Linear API: https://developers.linear.app/docs/graphql/working-with-the-graphql-api
- Jira REST API: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- API versioning best practices: https://github.com/microsoft/api-guidelines/blob/vNext/Guidelines.md#12-versioning
- Postel's law + API stability: https://www.iana.org/assignments/uri-schemes/prov/http
- Partner ecosystem roadmap planning — Forrester: https://www.forrester.com/research/partner-ecosystems/
- DrawIO docs: https://www.diagrams.net/doc/
