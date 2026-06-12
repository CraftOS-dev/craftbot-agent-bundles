# Customer Success — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Onboarding playbook", "Success plan playbook", "QBR playbook", "Health scoring playbook", "Health score composite formula", "NRR GRR playbook", "Expansion opportunity playbook", "Renewal playbook (90-day)", "Churn save playbook", "At-risk identification playbook", "In-app onboarding playbook", "Survey ops playbook", "Voice of customer playbook", "CAB playbook", "Advocacy playbook", "Referral playbook", "Adoption tracking playbook", "Ramp-to-value playbook", "Multi-threading enterprise playbook", "Customer touchpoint cadence playbook", "AI-slop catch list — CS edition", "Antipattern catalog", "Renewal forecast template", "Success plan template", "QBR deck template", "Save plan template", "VOC report template", "Health score formula", "Reporting + dashboard patterns", "SOTA tool reference", "SOTA execution playbook".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Customer success platforms (CSPs)

- **Vitally** — modern CSP with rich integrations (PostHog, Mixpanel, Amplitude, Stripe, HubSpot, Salesforce). Projects = success plans. Playbooks = automation. Strong API.
- **Catalyst (Totango-owned)** — enterprise CSP. Playbooks + Customer Journey + Reports. Salesforce-native.
- **Gainsight** — enterprise incumbent. Journey Orchestrator (JO) for automation. CS Operations heavyweight.
- **ChurnZero** — retention-focused. ChurnZero Plays = automation. ChurnZero AI = signal extraction.
- **Totango** — composable success platform. Toolset for tier-based motions.
- **Custify** — SMB-friendly CSP.
- **Velaris** — modern entrant focused on signal aggregation.
- **Planhat** — European CSP alt; portfolio approach.

### Health + churn AI

- **ChurnZero AI** — first-party ML on usage + comms signals.
- **Vitally AI** — first-party ML embedded in Vitally workflows.
- **Sturdy AI** — third-party signal extraction from comms data (Slack, email, Zoom).
- **Custify AI** — first-party in Custify.

### In-product onboarding

- **Pendo** — incumbent. Pendo Engage = onboarding flows; Pendo Guide = walkthroughs; Pendo Adopt = adoption analytics.
- **Userpilot** — modern alt. Flow builder + checklists + experiments.
- **Appcues** — incumbent. Modal + tooltip + checklist patterns.
- **Chameleon** — modern alt. JavaScript SDK + REST.
- **Whatfix** — enterprise alt.
- **ProductFruits** — freemium alt with broad coverage.

### Product analytics tied to CS

- **PostHog** — open source product analytics. HogQL for cohort + funnel + retention queries. CraftBot MCP available.
- **Mixpanel** — incumbent. JQL queries + cohort + funnel. CraftBot MCP available.
- **Amplitude** — incumbent. Behavioral cohorts + retention curves + product KPI dashboards. CraftBot MCP available.
- **Heap** — autocapture-first analytics.
- **FullStory** — session replay + analytics.
- **LogRocket** — JS-error-focused session replay.

### Customer comms + outreach

- **Mixmax** — sales cadence + email tracking. Best for CSM renewal cadence.
- **Outreach** — sales engagement platform. Strong for multi-step expansion sequence.
- **Salesloft** — alt sales engagement.
- **Klaviyo** — product-led lifecycle email. Strong for in-app trigger-based sequences.
- **Customer.io** — lifecycle email + SMS.
- **Iterable** — enterprise lifecycle.

### Customer interview / call

- **Calendly** — round-robin + customer-facing booking. CraftBot default skill.
- **Zoom** — meeting + recording + transcription. CraftBot MCP.
- **Granola** — AI notetaker. Live note capture.
- **Fathom** — AI notetaker (free tier). CraftBot default skill.
- **tl;dv** — alt AI notetaker.
- **Otter.ai** — incumbent.

### Survey / VoC

- **Delighted** (Qualtrics) — one-stop NPS + CSAT + CES + multi-channel delivery.
- **Survicate** — multi-channel including in-app surveys.
- **Sprig** (UserLeap) — event-triggered in-product micro-surveys.
- **Wootric** (InMoment) — incumbent NPS.
- **Iterate** — Hotjar's survey product.
- **Hotjar** — in-product + survey.
- **Typeform** — generic with CSAT templates.

### Renewal + commercial

- **Stripe Subscriptions** — primary subscription state source for SMB / SaaS.
- **Salesforce CPQ** — enterprise CPQ for renewal uplift pricing.
- **Zuora** — enterprise billing + subscription mgmt.
- **PandaDoc** — proposal + e-sign workflow.
- **DocuSign** — enterprise e-sign.
- **Ironclad** — enterprise contract lifecycle.

### Advocacy + reference

- **Influitive** — points-based advocacy program. AdvocateHub product.
- **Slapfive** — case study + reference program management.
- **UserEvidence** — customer evidence + review program management.
- **Champion** — advocate program management alt.

### Customer academy / certification

- **Skilljar** — primary LMS for customer academies.
- **Northpass** — alt LMS.
- **WorkRamp** — sales + customer enablement LMS.
- **Intellum** — enterprise customer education platform.

### Referral programs

- **Friendbuy** — referral + advocate marketing platform.
- **Referral Rock** — SMB referral.
- **Mention Me** — enterprise referral.
- **GrowSurf** — modern referral SaaS.
- **Tremendous** — payout / gift card fulfillment for rewards.

### PLG + community signals (expansion)

- **Pocus** — PLG signal aggregation; product-activity → sales-action.
- **Koala** — PLG intent platform.
- **Endgame** — PLG sales platform.
- **Common Room** — community + dark social signal aggregation.

### CAB community

- **Bevy** — community platform; CAB community + events.
- **Mighty Networks** — alt community platform.
- **Slack Connect** — B2B Slack channels for CAB.
- **Discord** — alt CAB community (informal / dev-focused customers).

### CRM + customer record

- **HubSpot CRM** — primary SMB CRM. Custom properties = poor-man's CSP.
- **Salesforce** — enterprise CRM. Contact-role mapping for multi-threading.
- **Attio** — modern CRM alt. CraftBot default skill.
- **Pipedrive** — SMB CRM alt. CraftBot default skill.
- **Zoho CRM** — alt CRM. CraftBot default skill.

### Warehouse + reverse-ETL + BI

- **PostgreSQL warehouse** — CraftBot MCP for cohort math + reporting.
- **Census / Hightouch** — reverse-ETL: CSP + product analytics → warehouse → CRM.
- **dbt** — warehouse modeling layer.
- **Metabase / Looker / Hex / Mode** — BI dashboard layer.

---

## Onboarding playbook

### Day 0 / 7 / 30 / 60 / 90 framework

| Day | Milestone | Trigger | Success criteria | Owner |
|---|---|---|---|---|
| Day 0 | Kickoff call | Customer signed | Use case confirmed, exec sponsor named, success plan started | CSM |
| Day 7 | First aha event | PostHog event `first_aha_event` | Customer completes first end-to-end workflow | Customer (CSM nudge) |
| Day 30 | Activation | PostHog feature-adoption score ≥ 0.4 | Customer uses ≥ 3 key features actively | Customer (CSM monitors) |
| Day 60 | Expansion-readiness | DAU > MAU * 0.4 + sponsor active | Customer using product daily | Customer (CSM identifies expansion) |
| Day 90 | Health check | All milestones hit | Renewal probability > 80% | CSM (with exec sponsor) |

### Onboarding plan template

```markdown
# Onboarding Plan: [Customer Name]

**Signup date:** YYYY-MM-DD
**Plan:** [Enterprise/Growth/Starter]
**Exec sponsor:** [name + title]
**Customer-side champion:** [name + title]
**CSM owner:** [name]
**Primary use case:** [outcome-led, not feature-led]

## Outcomes by month 3 / 6 / 12

- **Month 3:** [measurable outcome]
- **Month 6:** [measurable outcome]
- **Month 12:** [measurable outcome — usually renewal-readiness]

## Milestones

### Day 0 — Kickoff
- [ ] Kickoff call held (Zoom + Fathom)
- [ ] Use case confirmed in writing
- [ ] Exec sponsor named + connected
- [ ] Success plan v1 published

### Day 7 — First value
- [ ] First aha event fired (PostHog)
- [ ] Workspace setup complete
- [ ] First end-to-end workflow run
- [ ] CSM 1:1 with champion

### Day 30 — Activation
- [ ] Feature adoption score ≥ 0.4
- [ ] ≥ 3 key features used actively
- [ ] CSAT survey sent + ≥ 4/5 average
- [ ] Day 30 health check call

### Day 60 — Expansion readiness
- [ ] DAU / MAU > 0.4
- [ ] Sponsor still active (last seen < 14d)
- [ ] Expansion opportunity identified or ruled out
- [ ] Day 60 health check call

### Day 90 — Health check + renewal forecast
- [ ] Composite health score ≥ 0.7
- [ ] All milestones hit
- [ ] Renewal probability ≥ 80%
- [ ] QBR scheduled for month 3
```

### Onboarding execution

- **CSP path:** `cli-anything` `curl POST https://api.vitally.io/resources/customers/<id>/projects -d @plan.json` creates the project + milestones.
- **No-CSP path:** `notion-mcp` `create_page` in "Onboarding Plans" DB with same structure.
- **Trigger wiring:** PostHog event `first_aha_event` fires Day 7 milestone complete; cohort `feature_adoption_score > 0.4` fires Day 30.
- **Email cadence:** `gmail-mcp` schedules Day 0 welcome + Day 7 nudge + Day 30 review + Day 60 expansion + Day 90 QBR-confirm.
- **In-product cards:** `cli-anything` curl Pendo / Userpilot to enroll customer in onboarding-flow audience.

---

## Success plan playbook

### Outcomes (not features) framework

- **BAD:** "Customer will adopt feature X."
- **GOOD:** "Customer will reduce support ticket volume from 50/week to 35/week by month 3 via X."

### Success plan template

```markdown
# Success Plan: [Customer Name]

**Created:** YYYY-MM-DD
**Last reviewed:** YYYY-MM-DD
**CSM owner:** [name]
**Customer-side owner:** [name]

## Strategic context

[1-2 sentences: customer's business goal, why they bought, what good looks like]

## Outcomes

### Outcome 1: [Customer-measurable result]
- **Why it matters:** [business impact]
- **Success criteria:** [specific metric + target value + measurement method]
- **Target date:** [end of month X]
- **Owner:** [customer-side + CSM-side]
- **Milestones:**
  - [ ] [milestone 1 + due date]
  - [ ] [milestone 2 + due date]
  - [ ] [milestone 3 + due date]
- **Risks + mitigations:**
  - [risk] → [mitigation]
- **Status:** Green / Yellow / Red

### Outcome 2: ...
### Outcome 3: ...

## Review cadence

- Bi-weekly: CSM + customer-side champion sync (Zoom)
- Monthly: Exec sponsor update (email)
- Quarterly: QBR (Zoom + deck)
```

### Push to CSP / Notion

- **Vitally:** `cli-anything` `curl POST https://api.vitally.io/resources/customers/<id>/projects -d @plan.json` with milestones array.
- **Catalyst:** `cli-anything` `curl POST https://api.catalyst.io/v1/playbooks/<id>/assignments` with customer id.
- **Notion fallback:** `notion-mcp` `create_page` in "Success Plans" DB.

---

## QBR playbook

### T-21 → T+1 cadence

| Days | Action | Tool |
|---|---|---|
| T-21 | Confirm date via round-robin | `calendly-api` |
| T-21 | Reserve Zoom meeting | `zoom-mcp` create_meeting |
| T-7 | Pull QBR data | `posthog-mcp` HogQL + Vitally curl + Linear + Postgres |
| T-3 | Draft deck (15 slides max) | `pptx` skill |
| T-1 | CSM review + customer pre-share | `gmail-mcp` |
| T-0 | Run QBR | Zoom + Fathom transcript |
| T+1 | Action item recap email | `gmail-mcp` |
| T+2 | Sync action items to CSP | `cli-anything` curl Vitally + Linear |

### QBR deck template (15 slides max)

1. Cover — Customer Name, Quarter, CSM, Date
2. Executive summary — 3 sentences
3. Wins this quarter — 3 bullets
4. Adoption snapshot — DAU/MAU/WAU + key feature adoption %
5. Health score trajectory — score over time chart
6. Open items — 3 in-flight outcomes from success plan
7. Open items — risks + mitigations
8. Voice of customer — what we heard from your team
9. Roadmap update — what's shipped + what's next (from `linear-mcp`)
10. Roadmap update — what's deprioritized + why (honest)
11. Renewal outlook — risk classification + forecast
12. Expansion opportunities — if identified
13. Action items for customer
14. Action items for us
15. Next QBR + close

### Action item recap template

```markdown
Subject: QBR recap + next steps — [Customer Name]

Hi [name],

Thanks for the time today. Here's what we agreed:

**For you / your team:**
1. [action + owner + due date]
2. [action + owner + due date]

**For us:**
1. [action + owner + due date]
2. [action + owner + due date]

**Roadmap commitments:**
- [item] — tracked as ENG-1234, ship target [date or no-ETA]

**Next QBR:** [date], same time. Calendar hold sent.

Anything to add? Reply by EOD Friday.

— [CSM]
```

---

## Health scoring playbook

### Health score composite formula

```
Health = 0.40 * (adoption_score)
       + 0.20 * (csat_nps_recency_score)
       + 0.15 * (sentiment_score)
       + 0.10 * (1 - support_ticket_volume_normalized)
       + 0.10 * (exec_sponsor_engagement_score)
       + 0.05 * (renewal_stage_score)
```

Where:
- `adoption_score`: 0-1, composite from DAU/MAU + feature adoption rate (PostHog HogQL)
- `csat_nps_recency_score`: latest CSAT/NPS / max, with 90d decay
- `sentiment_score`: avg ticket sentiment 90d (from `customer-support-agent` warehouse)
- `support_ticket_volume_normalized`: tickets last 90d / customer baseline (more isn't always bad; context-dependent)
- `exec_sponsor_engagement_score`: last sponsor activity recency (login + email reply); 1 = within 7d, 0.7 = within 14d, 0.4 = within 30d, 0 = > 60d
- `renewal_stage_score`: 1 = post-renewal, 0.7 = mid-cycle, 0.4 = T-90 to T-30, 0 = T-30 to T-0

### Risk flags

| Score / Trend | Flag | Action |
|---|---|---|
| Score < 0.4 | At-risk (Red) | Fire churn save play within 7d |
| 30d decline > 0.1 | Trending down (Yellow) | CSM reach-out within 7d |
| 30d decline > 0.2 | Trending down sharp (Yellow → Red) | CSM reach-out within 48h |
| > 3 SLA breaches in 30d | Support-driven risk | Cross-flag with `customer-support-agent` |
| Sponsor not seen 30d | Sponsor risk | Multi-threading playbook fires |
| Score > 0.85 + NPS ≥ 9 | Advocacy candidate | Fire advocacy flow |

### CSP writeback

- **Vitally:** `cli-anything` `curl POST https://api.vitally.io/resources/customers/<id>/traits -d '{"health_score": 0.72, "health_score_trend_30d": -0.04, "at_risk": false}'`
- **Catalyst:** similar `companies/<id>/properties` PATCH.
- **ChurnZero / Gainsight / Totango:** vendor-specific custom-attribute PATCH via REST.
- **HubSpot fallback:** `api-gateway` skill `POST /crm/v3/objects/companies/<id> -d '{"properties":{"health_score":"0.72"}}'`.

### Free fallback (no CSP)

```sql
-- dbt model: customer_health_score.sql (run nightly)
SELECT
  c.id AS customer_id,
  0.40 * COALESCE(a.adoption_score, 0)
  + 0.20 * COALESCE(s.csat_nps_score, 0)
  + 0.15 * COALESCE(t.sentiment_score, 0)
  + 0.10 * (1 - COALESCE(t.ticket_volume_normalized, 0))
  + 0.10 * COALESCE(e.sponsor_engagement_score, 0)
  + 0.05 * COALESCE(r.renewal_stage_score, 0) AS health_score
FROM customers c
LEFT JOIN adoption_metrics a ON a.customer_id = c.id
LEFT JOIN survey_metrics s ON s.customer_id = c.id
LEFT JOIN ticket_metrics t ON t.customer_id = c.id
LEFT JOIN engagement_metrics e ON e.customer_id = c.id
LEFT JOIN renewal_metrics r ON r.customer_id = c.id;
```

Write back via Census / Hightouch sync into HubSpot custom property.

---

## NRR GRR playbook

### Definitions

- **NRR (Net Revenue Retention):** `(Starting MRR + Expansion - Contraction - Churn) / Starting MRR`
- **GRR (Gross Revenue Retention):** `(Starting MRR - Contraction - Churn) / Starting MRR`

NRR > 100% means a cohort grows revenue without new customers. Best-in-class SaaS: NRR ≥ 115%; GRR ≥ 90%.

### Cohort computation

```sql
-- Materialize monthly cohorts in `postgresql-mcp` warehouse
WITH monthly_cohort AS (
  SELECT
    DATE_TRUNC('month', signup_date) AS cohort_month,
    customer_id
  FROM customers
), monthly_revenue AS (
  SELECT
    DATE_TRUNC('month', period_start) AS month,
    customer_id,
    SUM(amount_decimal) / 100.0 AS mrr
  FROM stripe_invoices
  WHERE status = 'paid'
  GROUP BY 1, 2
), cohort_revenue AS (
  SELECT
    mc.cohort_month,
    mr.month,
    SUM(mr.mrr) AS cohort_mrr
  FROM monthly_cohort mc
  JOIN monthly_revenue mr ON mr.customer_id = mc.customer_id
  GROUP BY 1, 2
)
SELECT
  cohort_month,
  month,
  cohort_mrr,
  LAG(cohort_mrr) OVER (PARTITION BY cohort_month ORDER BY month) AS prev_mrr,
  (cohort_mrr / NULLIF(LAG(cohort_mrr) OVER (PARTITION BY cohort_month ORDER BY month), 0)) AS nrr
FROM cohort_revenue
ORDER BY cohort_month, month;
```

### Report format

- `xlsx` skill: cohort math sheet + summary sheet (NRR by cohort + by tier + by vertical + monthly trend)
- `pptx` skill: 3-slide board summary (NRR trend + cohort drilldown + outlook)

---

## Expansion opportunity playbook

### Signal sources

1. **PostHog HogQL:** feature-limit-hit events; multi-workspace creation; integration adoption.
2. **Pocus / Common Room:** community signal + dark social + product-activity intent.
3. **CRM:** deal stage = "post-onboarding" + tier = "enterprise" or "growth".
4. **CSP:** health score > 0.85 + sponsor engaged.

### Composite signal score

```
ExpansionScore = 0.30 * (usage_growth_30d_normalized)
              + 0.25 * (feature_limit_hit_normalized)
              + 0.20 * (multi_workspace_signal)
              + 0.15 * (csp_health_score)
              + 0.10 * (community_intent_signal)
```

`ExpansionScore ≥ 0.7` → ready for expansion outreach.

### Routing decision

- **AE-led close** (new SKU, multi-year, contract changes): hand off to `sales-agent` with full context.
- **CSM-led uplift** (seat expansion, in-current-SKU usage): CSM owns; `calendly-api` books usage review; deck via `pptx`.

### Outreach template (CSM-led usage uplift)

```markdown
Subject: 30-min usage review — [Customer]

Hi [name],

I've been watching your usage over the last 30 days — your team's run [X] [feature]
[Y] times, up [Z%] from last month. You're brushing up against the [limit] cap.

Worth a 30-min usage review to walk through what's driving the growth + show you
the path to expand without disruption?

[Calendly link]

— [CSM]
```

### Expansion board (Notion DB)

| Customer | Signal | ARR Potential | Tier | Sponsor | CSM/AE | Status | Next action |
|---|---|---|---|---|---|---|---|

---

## Renewal playbook (90-day)

### T-90 / T-60 / T-30 / T-7 cadence

| T-X days | Action | Tool | Output |
|---|---|---|---|
| T-90 | Risk classification (Green/Yellow/Red) | health score + Stripe + CSP | Risk tag in renewal board |
| T-90 | Forecast probability | composite signal | NRR / GRR forecast |
| T-60 | QBR with renewal pricing | `qbr-scheduling-facilitation` | Deck + customer-side buy-in |
| T-60 | Save play if Red | `churn-save-motion-intervention` | Exec outreach + offer |
| T-30 | Contract draft | `cli-anything` PandaDoc + `xlsx` pricing | Proposal sent to customer |
| T-30 | Approval routing | Notion renewal board | Internal sign-off |
| T-7 | E-sign send | `cli-anything` DocuSign | Envelope sent |
| T-7 | Slack pin renewal status | `slack-mcp` | CSM channel update |
| T-0 | Renewal closed | `stripe-mcp` invoice + `notion-mcp` update | Subscription renewed |
| T+1 | Handoff to expansion mode | `expansion-opportunity-identification` | Next-phase plan |

### Renewal status board (Notion)

| Customer | Renewal Date | Risk | Stage | Owner | Forecast | Notes |
|---|---|---|---|---|---|---|

### Renewal pricing template (xlsx tab)

| Item | Current | Renewal | Delta | Notes |
|---|---|---|---|---|
| Base subscription | $X | $X * 1.07 | +7% (CPI uplift) | |
| Seat expansion | 50 → 75 seats | +25 seats * $Y | +$Y * 25 | |
| Multi-product add | — | + $Z (new SKU) | +$Z | |
| Multi-year discount | — | -3% | -3% (3-yr) | |
| **Total ACV** | $T | $T' | **+X%** | |

### Forecast accuracy logging

- Forecast at T-90 vs actual at T-0.
- Target: 95% accuracy. Weekly review of misses; tighten classification.

---

## Churn save playbook

### Composite signal trigger (4 of 6 fires the play)

1. Usage drop > 30% week-over-week
2. Exec sponsor not seen > 30d
3. NPS detractor (≤ 6) within last 90d
4. Avg ticket sentiment dropped > 20% week-over-week
5. SLA breach count > 3 in last 30d
6. Renewal stage = T-90 to T-30 + risk = Yellow/Red

### Save plan template

```markdown
# Save Plan: [Customer Name]

**Triggered:** YYYY-MM-DD
**Trigger signals (≥ 4):**
- [x] Usage drop X%
- [x] Sponsor not seen Yd
- [x] NPS detractor (score, comment)
- [ ] Sentiment drop
- [x] SLA breaches
- [ ] Renewal-stage risk

## Health snapshot
- Current health score: X (was Y, 30d ago)
- ARR at risk: $X
- Renewal date: YYYY-MM-DD

## Diagnosis hypothesis
[1-2 sentences: what we think went wrong]

## Save play

### Exec outreach
- **Who:** [CSM Lead + VP Customer Success]
- **To:** [exec sponsor or replacement]
- **Channel:** email (Gmail) + LinkedIn DM if no reply 3d
- **Ask:** 30-min save call
- **Date:** within 7d of trigger

### Save call agenda
1. Acknowledge the friction (specific, not generic)
2. Listen — diagnose what changed
3. Commercial offer if appropriate (per policy)
4. Roadmap commitment if product-driven (Linear ticket required)
5. Joint success plan refresh

### Commercial offer (if applicable)
- **Type:** [pause, discount, free month, custom-term]
- **Approval:** [Slack #renewal-saves approval gate]
- **Documented:** Notion save plan

### Roadmap commitment (if product-driven)
- **Linear ticket:** ENG-XXXX
- **Customer expectation:** [specific, not "soon"]
- **Owner:** [PM]

## Status tracking
- [ ] Outreach sent
- [ ] Save call held
- [ ] Diagnosis complete
- [ ] Plan agreed
- [ ] 30-day check-in held
- **Outcome:** Recovered / Churned / Extended runway (state + ARR)
```

### Save call communication rules

- **Acknowledge specifically.** "Your team's usage dropped 35% after the 3.2 release" — not "We've noticed some changes in your engagement."
- **Don't apologize generically.** Targeted ownership: "We pushed the 3.2 release without enough customer-readiness review. That's on us."
- **Don't promise what you can't deliver.** Roadmap commitment requires Linear ticket. No "we're working on it" without one.
- **Don't undercut sales.** Commercial offers go through approval gate; same policy across customers.

---

## At-risk identification playbook

### Nightly composite risk model

```sql
-- Risk identification view (refreshed nightly)
SELECT
  c.id AS customer_id,
  c.name,
  c.tier,
  c.arr,
  h.health_score,
  h.health_score_trend_30d,
  s.last_sponsor_activity_days_ago,
  t.ticket_count_30d,
  t.sentiment_avg_30d,
  r.days_to_renewal,
  CASE
    WHEN h.health_score < 0.4 THEN 'Red'
    WHEN h.health_score_trend_30d < -0.15 THEN 'Red'
    WHEN h.health_score < 0.6 AND s.last_sponsor_activity_days_ago > 30 THEN 'Red'
    WHEN h.health_score < 0.7 THEN 'Yellow'
    WHEN h.health_score_trend_30d < -0.05 THEN 'Yellow'
    ELSE 'Green'
  END AS risk_flag
FROM customers c
LEFT JOIN health_scores h ON h.customer_id = c.id
LEFT JOIN sponsor_activity s ON s.customer_id = c.id
LEFT JOIN ticket_metrics t ON t.customer_id = c.id
LEFT JOIN renewal_metrics r ON r.customer_id = c.id;
```

### Escalation tiers

- **Red:** CSM Lead Slack alert + auto-create Linear "save plan" issue + add to renewal board
- **Yellow:** CSM weekly review queue + ping for action plan
- **Green:** standard cadence

### Slack alert format

```
:warning: At-risk: [Customer Name] — Red
Health: 0.38 (was 0.62, 30d ago)
ARR: $X
Renewal: T-Y days
Trigger: [primary signal]
Owner: [CSM]
Save plan: [Linear link or "draft"]
```

---

## In-app onboarding playbook

### Flow design schema

```json
{
  "flow_id": "onboarding-day-7-aha",
  "trigger": {
    "type": "event",
    "event_name": "workspace_setup_complete"
  },
  "audience": {
    "filter": "tier IN ('starter', 'growth') AND days_since_signup BETWEEN 5 AND 10"
  },
  "steps": [
    {"type": "modal", "title": "Welcome — let's get you to your first aha", "body": "..."},
    {"type": "tooltip", "target": "#create-button", "body": "Create your first [thing]"},
    {"type": "checklist", "items": ["Create [thing]", "Invite teammate", "Run first [workflow]"]}
  ],
  "exit": {
    "type": "event",
    "event_name": "first_aha_event"
  },
  "metric": "first_aha_rate_within_7d"
}
```

### Push to platform

- **Pendo:** `cli-anything` `curl -X POST https://app.engage.pendo.io/api/v1/guides -d @flow.json`
- **Userpilot:** `cli-anything` `curl -X POST https://api.userpilot.io/v1/flows -d @flow.json`
- **Appcues:** `cli-anything` `curl -X POST https://api.appcues.com/v1/flows -d @flow.json`
- **Chameleon:** `cli-anything` `curl -X POST https://api.trychameleon.com/v3/...` (SDK-first)
- **ProductFruits:** similar curl pattern (free tier available)

### A/B test pattern

1. Build flow variant A + variant B (different copy / different order / different exit event).
2. Audience split 50/50.
3. Run 14 days.
4. Compare `first_aha_rate_within_7d` per variant (PostHog cohort query).
5. Promote winner; archive loser.

---

## Survey ops playbook

### Survey types + cadence

| Survey | Trigger | Cooldown | Channel |
|---|---|---|---|
| NPS | Quarterly | 90d minimum | Email (Delighted) |
| NPS post-onboarding | Day 90 milestone | 90d | Email or in-app |
| CSAT | 1h post-support-close | 14d | Email (Delighted) |
| CES | 24h post-resolution | 14d | Email (Delighted) |
| In-product micro | Key event (e.g. first export) | 30d | Sprig in-app |

### Detractor playbook

- NPS ≤ 6 or CSAT ≤ 2 → auto-route to CSM via `slack-mcp` within 1h.
- CSM reads original survey comment + last 5 tickets + health score.
- CSM personal outreach within 48h: "Saw your feedback; what would have made this better?"
- Log outcome: recovered / churned / no-response.

### Promoter playbook

- NPS ≥ 9 or CSAT 5/5 → trigger `customer-advocacy-case-study-reference` flow.
- Send advocacy invite within 7d.

### Delivery via Delighted

```bash
# cli-anything: enqueue NPS survey
curl -X POST https://api.delighted.com/v1/people \
  -u $DELIGHTED_API_KEY: \
  -d email=user@customer.com \
  -d send=true \
  -d survey_type=nps \
  -d delay=0
```

---

## Voice of customer playbook

### Synthesis sources

1. Customer interview transcripts (`fathom-api` + `notion-mcp` insights DB)
2. NPS comments (Delighted)
3. CSAT/CES comments (Delighted)
4. Ticket-cluster themes (from `customer-support-agent` Postgres warehouse)
5. Churn-reason tags (from CSP)
6. In-product Sprig survey results

### Quarterly synthesis process

1. Pull all 6 sources for the quarter.
2. Embed comments (Voyage/OpenAI ada/Cohere).
3. Cluster via HDBSCAN; threshold ≥ 3 customers per cluster.
4. For each cluster: theme label + customer count + revenue impact + recommended action.
5. Tag each theme: product / support / sales / marketing.
6. Route:
   - **Product-tagged** → `linear-mcp` `create_issue` with `voice-of-customer` label + metadata
   - **Support-tagged** → cross-feed to `customer-support-agent`
   - **Sales-tagged** → cross-feed to `sales-agent` battlecards
   - **Marketing-tagged** → cross-feed to `marketing-agent` content strategy
7. Render quarterly VOC report via `docx` skill.

### VOC report template

```markdown
# Voice of Customer Report — [Quarter]

**Period:** YYYY-MM-DD to YYYY-MM-DD
**Customers represented:** N
**Themes identified:** M

## Top themes (ranked by customer count × revenue)

### Theme 1: [theme]
- **Customers:** N (representing $X ARR)
- **Source mix:** [interviews / NPS / tickets / churn / surveys]
- **Direct quotes:**
  - "[verbatim quote 1]" — [Customer, tier]
  - "[verbatim quote 2]"
  - "[verbatim quote 3]"
- **Tag:** [product / support / sales / marketing]
- **Recommended action:** [Linear issue / cross-feed]
- **Linear:** ENG-XXXX (if product)

### Theme 2: ...

## Trends quarter-over-quarter
- [theme] mentions up X% from last quarter
- [theme] dropped — likely fix from release Y

## Recommended product roadmap input (top 3)
1. [item] — N customers, $X ARR
2. ...

## Recommended support / docs input
1. [item] — N customers
2. ...
```

---

## CAB playbook

### Roster

- 8-12 customers.
- Mix of tiers (Enterprise weighted heavier), verticals, geographies.
- Each has named exec sponsor on customer side.
- Refresh annually; rotate 25% out.

### Cadence

- **Quarterly all-hands:** 90-min Zoom; roadmap preview; customer panel; feedback session.
- **Monthly drumbeat:** roadmap update email + early-access offers + exclusive content.
- **CAB Discord/Slack Connect:** between-meeting community channel.

### Quarterly meeting agenda

1. Welcome + state of the union (10min)
2. Roadmap preview — 3 themes (20min)
3. Customer panel — 2 customers share use case (20min)
4. Open feedback — facilitated discussion (25min)
5. Q&A + close (15min)

### Tools

- `notion-mcp` — CAB roster + meeting notes + feedback log
- `zoom-mcp` — meeting + recording
- `fathom-api` — transcript + action item extraction
- `discord-mcp-full` or `slack-mcp` — CAB community channel
- `gmail-mcp` — drumbeat emails

---

## Advocacy playbook

### Promoter qualification

- **Trigger:** Delighted `score ≥ 9` (NPS) or `CSAT = 5/5` or milestone hit (Year 1 anniversary, etc.)
- **Cooldown:** don't ask the same customer twice within 6 months.

### Advocacy asks (in priority order)

1. **G2 / Capterra review** — easiest ask; high SEO + sales-collateral value.
2. **Reference call** — for active sales opportunities; book via `calendly-api`.
3. **Case study** — higher commitment; book filming via `calendly-api`; transcribe via `fathom-api`; draft via `docx` skill.
4. **Conference speaking** — highest commitment; opt-in only.

### Rewards

- **G2 review:** $50 Tremendous gift card or 1-month service credit.
- **Reference call:** $100 gift card or 1-month credit.
- **Case study:** $250 gift card or 3-month credit + 5% renewal discount.
- **Speaking:** travel + custom acknowledgment.

### Outreach template

```markdown
Subject: [name], 5 min for a quick thank you?

Hi [name],

Your NPS response from last week made our day — saw you'd rate us 10/10 + mentioned
[specific thing from comment].

Two things:
1. Would you be willing to leave a quick G2 review? Takes < 5min, totally voluntary.
   [G2 review link]
2. We're collecting customer stories for a case study program. Would you be open to
   a 30-min conversation about how [outcome from success plan] played out? We'll
   share a draft before publishing anything.
   [Calendly link]

Either way — thanks for being a great customer.

— [CSM]
```

### Tools

- **Promoter list:** `cli-anything` `curl https://api.delighted.com/v1/responses?score=9..10` + CSAT filter
- **Influitive (paid):** `cli-anything` `curl https://api.influitive.com/api/v1/members/<id>/challenges/<id>/activities`
- **Notion fallback:** advocacy tracker DB with promoter / status / outcome
- **Reward fulfillment:** `stripe-mcp` credit_create OR `cli-anything` curl Tremendous payout

---

## Referral playbook

### Referral program structure

- **Who refers:** existing happy customers (NPS ≥ 8).
- **Reward refer:** $X service credit per qualified lead; $Y per closed-won.
- **Reward referee:** 10% off first 3 months or comparable.

### Tools

- **Friendbuy (paid):** orchestrates link generation + tracking + reward fulfillment via REST API.
- **Referral Rock / Mention Me / GrowSurf:** alts.
- **Stripe credit fallback:** `stripe-mcp` `customer_balance_transactions.create` to issue credit.
- **Tremendous gift card:** `cli-anything` curl Tremendous payout API.

### Cadence

- Trigger on NPS ≥ 8 + active >= 6 months.
- Invite via `gmail-mcp`.
- Quarterly reminder for inactive referrers.

---

## Adoption tracking playbook

### Daily / weekly / monthly metrics per customer

```sql
-- adoption_metrics view
SELECT
  customer_id,
  DATE_TRUNC('day', timestamp) AS day,
  COUNT(DISTINCT user_id) FILTER (WHERE event = 'user_action') AS dau,
  COUNT(DISTINCT user_id) FILTER (WHERE event = 'user_action' AND timestamp > NOW() - INTERVAL '7 days') AS wau,
  COUNT(DISTINCT user_id) FILTER (WHERE event = 'user_action' AND timestamp > NOW() - INTERVAL '30 days') AS mau,
  COUNT(DISTINCT event_name) AS feature_breadth,
  COUNT(DISTINCT user_id) FILTER (WHERE event = 'key_feature_used') / NULLIF(COUNT(DISTINCT user_id) FILTER (WHERE event = 'user_action'), 0) AS key_feature_adoption_rate
FROM events
GROUP BY 1, 2;
```

### Adoption score (rolled up to customer)

```
AdoptionScore = 0.40 * (DAU / MAU normalized)
              + 0.30 * (key_feature_adoption_rate)
              + 0.20 * (feature_breadth normalized)
              + 0.10 * (login_recency_score)
```

### Trigger derived signals

- Adoption < 0.3 → at-risk adoption flag
- Adoption > 0.6 + sponsor active → expansion-ready flag
- Key feature not used by Day 30 → feature intervention flow

---

## Ramp-to-value playbook

### TTFV (Time to First Value)

- **Definition:** Days from signup to `first_aha_event`.
- **Target:** < 7d for self-serve; < 30d for enterprise.
- **Measurement:**

```sql
-- TTFV per customer
SELECT
  customer_id,
  DATE_DIFF('day',
    MIN(timestamp) FILTER (WHERE event = 'signup'),
    MIN(timestamp) FILTER (WHERE event = 'first_aha_event')
  ) AS ttfv_days
FROM events
GROUP BY customer_id;
```

### TTRV (Time to Repeat Value)

- **Definition:** Days from first aha event to second meaningful event (`second_aha_event`).
- **Target:** < 14d.
- **Indicates:** habit formation.

### Intervention if TTFV slipping

- Day 5 if no `first_aha_event` → CSM outreach
- Day 7 if still no → in-app card via Pendo/Userpilot
- Day 10 if still no → 1:1 call via `calendly-api`

---

## Multi-threading enterprise playbook

### Role mapping (every enterprise account)

- **Champion** — Director+ daily user; advocate internally
- **Exec sponsor** — VP+ accountable for the relationship
- **Economic buyer** — CFO / VP P&L who signs the contract
- **Technical evaluator** — engineering manager who vets integration
- **End users** — multiple front-line

### Touchpoint cadence per role

| Role | Touchpoint frequency | Owner | Channel |
|---|---|---|---|
| Champion | Bi-weekly | CSM | Zoom / email / Slack Connect |
| Exec sponsor | Monthly + QBR | CSM Lead / VP CS | Email + occasional Zoom |
| Economic buyer | Quarterly (QBR + renewal) | CSM Lead / VP CS / VP Sales | Email |
| Technical evaluator | Quarterly + as-needed | CSM / SE | Slack Connect / email |
| End users | Ongoing in-product | CS Ops | Pendo/Userpilot in-app + community |

### Risk: single point of failure

- **Signal:** only 1 contact has logged in / replied in last 30d.
- **Action:** multi-thread immediately — request intro from champion; CSM Lead emails exec sponsor.
- **Document:** named contacts per role in CSP or HubSpot custom property.

---

## Customer touchpoint cadence playbook

### Tier-based cadence

| Tier | CSM touch | Exec touch | QBR | NPS | CSAT |
|---|---|---|---|---|---|
| Enterprise | Weekly | Monthly | Quarterly | Quarterly | Per close |
| Growth | Bi-weekly | Quarterly | Quarterly | Quarterly | Per close |
| Starter | Monthly | Bi-annually | Annually | Quarterly | Per close |
| Free | Quarterly nudge | None | None | Quarterly | None |

### Tools

- **Cadence orchestration:** Mixmax / Outreach / Salesloft via `cli-anything` curl
- **Email:** `gmail-mcp`
- **Slack Connect:** `slack-mcp` Connect for B2B
- **In-product card:** `cli-anything` curl Pendo / Userpilot

---

## AI-slop catch list — CS edition

Before any customer-facing email / renewal note / advocacy invite ships, strip:

**Generic openers (sales-y, not CS-y):**
- "Hope you're doing well!" — cut
- "I wanted to reach out" — cut
- "Just touching base" — cut
- "Circling back" — cut
- "Per my last email" — cut (passive-aggressive)
- "Quick question" — cut
- "Let me know your thoughts" — cut, ask the specific question

**Performative empathy:**
- "I completely understand" — cut (you don't, be specific)
- "Your success is our priority" — cut (everyone says this)
- "We hear you" — cut (only useful if followed by a specific action)
- "We're committed to your success" — cut

**Fake commitment language:**
- "Working on it" — cut unless you have a Linear ticket
- "Soon" — replace with date
- "Going forward" — cut
- "At your earliest convenience" — cut
- "In the near future" — cut

**Corporate jargon:**
- "Leverage" → "use"
- "Utilize" → "use"
- "Touch base" → "talk" or "meet"
- "Synergies" → just don't
- "Move the needle" → name the metric

**Vanity framing:**
- "Excited to share" — cut, share the thing
- "Thrilled to announce" — cut
- "Honored to" — cut

**What stays protected:**
- Customer's exact language
- Specific numbers / metrics / dates
- Concrete next steps
- Brand voice cues from voice doc

---

## Antipattern catalog

### Antipattern 1: Feature list as success plan

**BAD:**
> Customer will adopt features X, Y, and Z by end of Q1.

**Why bad:** Feature adoption ≠ outcome. Customer doesn't measure success by features used.

**GOOD:**
> Customer will reduce manual data-entry time from 12h/week to 4h/week by Q1, via feature X workflow.

**Why better:** Outcome-led + measurable + tied to customer's own KPI.

---

### Antipattern 2: Vanity QBR

**BAD:**
> QBR slide 1: "We've had a great quarter together!"
> Slide 2: "Look at all this usage!"
> Slide 3: "Here's our new feature list!"

**Why bad:** Doesn't drive any decision. Doesn't address open issues. Doesn't position renewal.

**GOOD:** Wins (3 concrete) / Adoption snapshot (data) / Open items + risks / Roadmap with honest deprioritization / Renewal outlook with forecast.

**Why better:** Decision-driving + honest + positions renewal.

---

### Antipattern 3: Health score dishonesty

**BAD:**
> CSM tells customer their health score is "looking strong" when it's 0.42 (Red) because they don't want to alarm the customer.

**Why bad:** Misleads customer; loses CSM credibility when truth surfaces at renewal; CSM management can't make decisions.

**GOOD:** Internal health score is honest. Customer-facing language frames concretely: "Your usage dropped 30% after the org change in March. Let's talk about what to do."

**Why better:** Truth surfaces actionably, not at renewal.

---

### Antipattern 4: Renewal at T-30

**BAD:**
> CSM doesn't think about renewal until 30 days out. Customer is surprised by upsell pitch.

**Why bad:** No time for save play. No time for negotiation. Customer feels rushed and exploited.

**GOOD:** T-90 risk classification → T-60 QBR with pricing intro → T-30 contract draft → T-7 e-sign. Customer is part of the process.

**Why better:** Forecast accuracy + customer trust + room to save.

---

### Antipattern 5: Voice-of-customer as anecdotes

**BAD:**
> "Customer X mentioned they want a dashboard. Customer Y wanted SSO. Customer Z wants better search."

**Why bad:** Anecdotes don't drive product prioritization. Product team can't act.

**GOOD:** Synthesize into themes with customer count + revenue impact. "Theme: better-search-and-filter requested by 14 customers representing $X ARR; recommended Linear issue ENG-1234."

**Why better:** Product can prioritize; CS proves value.

---

### Antipattern 6: Single-threaded enterprise account

**BAD:**
> CSM has one contact, Champion Sarah at the customer. Sarah leaves. Renewal is in 60 days. Nobody else knows the CSM.

**Why bad:** Single point of failure. By the time CSM finds a new contact, momentum is lost.

**GOOD:** Champion + Exec sponsor + Economic buyer + Technical evaluator + End users all mapped. Sarah leaves; CSM has 4 other touchpoints.

**Why better:** Resilience.

---

### Antipattern 7: Promising roadmap items not in flight

**BAD:**
> "I'm sure that feature is on the roadmap — should be coming soon."

**Why bad:** Fabricated. Builds trust debt that explodes when feature doesn't ship.

**GOOD:** "That's not in current commits. I'll log it as a Voice-of-Customer item with [N similar requests] and revisit at next roadmap planning. No commitment on timing."

**Why better:** Honest. Earns credibility.

---

## Reporting + dashboard patterns

### Daily ops digest

- At-risk customers (Red flagged today)
- Health score declines > 0.1 today
- Renewals in next 30d (status snapshot)
- Open save plans (status)
- Promoter signals from yesterday's NPS

### Weekly CS team report

- Per-CSM book of business: customer count, ARR, average health, at-risk count, save outcomes this week
- Renewals this week + next 4 weeks (status)
- Expansion opportunities identified this week
- VOC themes from week's NPS comments

### Monthly executive report

- NRR / GRR for month
- Renewal forecast accuracy
- Save rate (saved / churned of at-risk customers)
- Expansion ARR added
- Top 3 churn reasons
- Top 5 VOC themes (recommended action)

### Quarterly board summary (pptx)

- North-Star: NRR trend
- Cohort NRR by acquisition quarter
- Renewal forecast actuals
- Top expansion wins
- Top churn losses + lessons
- VOC themes routed to product
- CAB highlights

---

## SOTA tool reference (June 2026)

This section is grep-only — the agent uses keyword-driven retrieval to surface the right skill pack for the user's task. Headings are intentionally search-friendly. Every entry links to a detailed `SKILL.md` in `skills/` that ships in this bundle (Round 2 populates the SKILL.md contents).

**Full coverage map:** see `reference/SOTA_USE_CASES.md` for the per-use-case mapping and confidence rating.

### Vitally CSP

Modern CSP with rich integrations (PostHog, Mixpanel, Amplitude, Stripe, HubSpot, Salesforce). Projects = success plans. Playbooks = automation. Traits = custom attributes for health scoring. Strong REST API.

- **Skill:** `skills/customer-health-scoring-vitally-catalyst-churnzero/SKILL.md`
- **Endpoint:** `https://api.vitally.io/resources/`
- **Auth:** API key → `VITALLY_API_KEY`
- **Key calls:** `POST /customers/<id>/traits`, `GET /customers/<id>`, `POST /customers/<id>/projects`, `POST /playbooks`
- **Source:** https://docs.vitally.io/reference

### Catalyst (Totango) CSP

Enterprise CSP. Playbooks + Customer Journey + Reports. Salesforce-native integration.

- **Skill:** `skills/customer-health-scoring-vitally-catalyst-churnzero/SKILL.md`
- **Endpoint:** `https://api.catalyst.io/v1/`
- **Auth:** API key → `CATALYST_API_KEY`
- **Key calls:** `POST /companies/<id>/properties`, `POST /playbooks/<id>/assignments`
- **Source:** https://help.catalyst.io/

### Gainsight Journey Orchestrator

Enterprise CSP incumbent. Journey Orchestrator (JO) for automation. CS Operations heavyweight.

- **Skill:** `skills/playbook-automation-churnzero-plays/SKILL.md`
- **Endpoint:** Gainsight Connect REST API
- **Auth:** API key
- **Source:** https://help.gainsight.com/docs/journey-orchestrator/

### ChurnZero Plays + ChurnZero AI

Retention-focused. ChurnZero Plays = if-this-then-that workflows. ChurnZero AI = first-party ML on usage + comms signals.

- **Skill:** `skills/playbook-automation-churnzero-plays/SKILL.md` + `skills/churn-save-motion-intervention/SKILL.md`
- **Endpoint:** `https://api.churnzero.net/`
- **Auth:** API key → `CHURNZERO_API_KEY`
- **Source:** https://help.churnzero.com/hc/en-us

### Pendo Engage + Adopt

Incumbent in-product onboarding. Pendo Engage = flows + walkthroughs; Pendo Adopt = adoption analytics. Strong REST API.

- **Skill:** `skills/in-app-onboarding-userpilot-appcues-pendo/SKILL.md`
- **Endpoint:** `https://app.engage.pendo.io/api/v1/`
- **Auth:** API key → `PENDO_API_KEY`
- **Key calls:** `POST /guides`, `GET /guides/<id>/metrics`, `POST /segments`
- **Source:** https://developers.pendo.io/

### Userpilot

Modern in-app onboarding alt. Flow builder + checklists + experiments. REST API.

- **Skill:** `skills/in-app-onboarding-userpilot-appcues-pendo/SKILL.md`
- **Endpoint:** `https://api.userpilot.io/v1/`
- **Auth:** API key → `USERPILOT_API_KEY`
- **Key calls:** `POST /flows`, `POST /audiences`, `GET /flows/<id>/analytics`
- **Source:** https://docs.userpilot.com/

### Appcues

Incumbent in-app onboarding. Modal + tooltip + checklist patterns.

- **Skill:** `skills/in-app-onboarding-userpilot-appcues-pendo/SKILL.md`
- **Endpoint:** `https://api.appcues.com/v1/`
- **Auth:** API key → `APPCUES_API_KEY`
- **Source:** https://help.appcues.com/en/articles/123-appcues-rest-api

### PostHog (product analytics + funnels + cohorts)

Open source product analytics. HogQL for cohort + funnel + retention. CraftBot MCP available. Foundation for adoption + expansion + churn signal detection.

- **Skill:** `skills/adoption-metric-feature-usage/SKILL.md` + `skills/ramp-to-value-tracking/SKILL.md` + `skills/expansion-opportunity-identification/SKILL.md`
- **MCP:** `posthog-mcp` (already in agent.yaml)
- **Key calls:** `query` (HogQL), `cohorts`, `feature_flags`
- **Source:** https://posthog.com/docs/api/queries

### Mixpanel

Incumbent product analytics. JQL queries + cohort + funnel. CraftBot MCP available.

- **MCP:** `mixpanel-mcp` (already in agent.yaml)
- **Source:** https://developer.mixpanel.com/reference/query-api

### Amplitude

Incumbent product analytics. Behavioral cohorts + retention curves. CraftBot MCP available.

- **MCP:** `amplitude-mcp` (already in agent.yaml)
- **Source:** https://amplitude.com/docs/apis/analytics

### Pocus + Common Room (PLG / community signals)

Pocus: PLG signal aggregation. Common Room: community + dark social signal. Both surface expansion intent.

- **Skill:** `skills/expansion-opportunity-identification/SKILL.md`
- **Endpoints:** `https://api.pocus.com/` + `https://api.commonroom.io/v1/`
- **Auth:** API keys per platform
- **Source:** https://www.pocus.com/ + https://docs.commonroom.io/

### Calendly (scheduling)

QBR + customer interview + reference call + CAB meeting scheduling. CraftBot default skill.

- **Skill:** `calendly-api` (default)
- **Auth:** OAuth → managed via `api-gateway`
- **Source:** https://developer.calendly.com/api-docs/

### Zoom (meetings + recording)

QBR + interview + CAB meeting hosting. CraftBot MCP.

- **MCP:** `zoom-mcp` (already in agent.yaml)
- **Source:** https://developers.zoom.us/docs/api/

### Fathom (AI notetaker)

QBR + interview transcript + action-item extraction. Free tier. CraftBot default skill.

- **Skill:** `fathom-api` (default)
- **Source:** https://help.fathom.video/en/articles/8430832-fathom-api

### Delighted (CSAT / CES / NPS)

One-stop CSAT + CES + NPS + multi-channel delivery. Promoter list for advocacy program. Detractor escalation.

- **Skill:** `skills/nps-csat-ces-tracking/SKILL.md`
- **Endpoint:** `https://api.delighted.com/v1/`
- **Auth:** API key → `DELIGHTED_API_KEY`
- **Key calls:** `POST /people`, `GET /responses`
- **Source:** https://app.delighted.com/docs/api

### Sprig (in-product micro-surveys)

Event-triggered in-product micro-surveys. Best for moment-specific feedback.

- **Skill:** `skills/nps-csat-ces-tracking/SKILL.md`
- **Endpoint:** `https://api.sprig.com/v1/`
- **Auth:** API key → `SPRIG_API_KEY`
- **Source:** https://docs.sprig.com/

### Mixmax (CSM cadence)

CSM renewal cadence + email tracking. Strong for personal touchpoint cadence.

- **Skill:** `skills/renewal-management-90-day-prep/SKILL.md` (cadence component)
- **Endpoint:** `https://api.mixmax.com/v1/`
- **Source:** https://help.mixmax.com/hc/en-us

### Outreach + Salesloft (multi-step sequences)

Multi-step expansion sequence orchestration.

- **Skill:** `skills/multi-product-cross-sell-uplift/SKILL.md`
- **Endpoints:** `https://api.outreach.io/api/v2/` + `https://api.salesloft.com/v2/`
- **Source:** https://developers.outreach.io/api/ + https://developers.salesloft.com/api.html

### Klaviyo + Customer.io + Iterable (lifecycle email)

Product-led lifecycle email for expansion sequences. Klaviyo is SOTA for ecom-style triggers.

- **Skill:** `skills/multi-product-cross-sell-uplift/SKILL.md`
- **Endpoints:** `https://a.klaviyo.com/api/` + `https://api.customer.io/v1/` + `https://api.iterable.com/api/`
- **Source:** https://developers.klaviyo.com/en/reference/api_overview

### PandaDoc + DocuSign + Ironclad (contracts)

Renewal proposal generation + e-sign workflow. PandaDoc for SMB; DocuSign for enterprise; Ironclad for CLM.

- **Skill:** `skills/renewal-management-90-day-prep/SKILL.md`
- **Endpoints:** `https://api.pandadoc.com/public/v1/` + `https://www.docusign.net/restapi/`
- **Source:** https://developers.pandadoc.com/ + https://developers.docusign.com/

### Stripe (subscriptions + credits)

Subscription state for renewal cadence + referral reward credits + commercial offer fulfillment.

- **MCP:** `stripe-mcp` (already in agent.yaml)
- **Key calls:** `subscription_list`, `invoice_list`, `customer_balance_transactions.create` (for credit issuance), `refund_create`
- **Source:** https://stripe.com/docs/api/subscriptions

### Influitive + Slapfive + UserEvidence (advocacy)

Customer advocacy program management. Influitive = points + challenges + rewards. Slapfive + UserEvidence = case studies + references.

- **Skill:** `skills/customer-advocacy-case-study-reference/SKILL.md`
- **Endpoints:** `https://docs.influitive.com/` + `https://help.slapfive.com/` + `https://help.userevidence.com/`
- **Source:** https://docs.influitive.com/

### Skilljar + Northpass + WorkRamp (customer academy)

LMS for customer academies + certification tracking.

- **Skill:** `skills/success-enablement-academy-certification/SKILL.md`
- **Endpoint:** `https://api.skilljar.com/v2/`
- **Source:** https://help.skilljar.com/hc/en-us/categories/200182230

### Friendbuy + Referral Rock + Tremendous (referrals)

Referral program orchestration + reward fulfillment.

- **Skill:** `skills/referral-programs/SKILL.md`
- **Endpoints:** `https://developers.friendbuy.com/` + Tremendous API
- **Source:** https://developers.friendbuy.com/

### HubSpot + Salesforce (CRM)

Contact + deal stage + custom-property writeback (free CSP fallback) + exec-sponsor tracking. Routed via `api-gateway` skill or `salesforce-api` default skill.

- **Skill:** `api-gateway` + `salesforce-api` (default)
- **Source:** https://developers.hubspot.com/docs/api/crm/contacts + https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/

### Notion (success plans + CAB roster + VOC insights DB)

CSP-fallback for success plans; CAB roster; VOC insights DB; renewal board; advocacy tracker.

- **MCP:** `notion-mcp` (already in agent.yaml)
- **Source:** https://developers.notion.com/

### PostgreSQL warehouse + dbt

Cohort math for NRR/GRR + health score nightly model + risk identification view.

- **MCP:** `postgresql-mcp` (already in agent.yaml)
- **Use cases:** NRR/GRR cohorts, health score nightly, at-risk view, adoption metrics

### Slack Connect + Discord (B2B comms + CAB)

Slack Connect for B2B customer Slack channels (and CAB Connect). Discord for community-style customers.

- **MCPs:** `slack-mcp` + `discord-mcp-full` (already in agent.yaml)
- **Source:** https://api.slack.com/connect

### DeepL (multilingual)

Multilingual customer comms (renewal + onboarding emails for non-English-primary customers).

- **MCP:** `deepl-mcp` (already in agent.yaml)
- **Source:** https://www.deepl.com/docs-api

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| Onboard this customer | `customer-onboarding-day-0-90` | Day 0/7/30/60/90 milestones |
| Build a success plan | `success-plan-goals-milestones` | Outcomes not features |
| Run a QBR | `qbr-scheduling-facilitation` | T-21/7/3/+1 cadence |
| Compute health scores | `customer-health-scoring-vitally-catalyst-churnzero` | Composite formula → CSP writeback |
| Compute NRR / GRR | `nrr-grr-ownership-metrics` | Stripe + CRM + warehouse |
| Find expansion opportunities | `expansion-opportunity-identification` | PostHog + Pocus + CRM signals |
| Plan a renewal | `renewal-management-90-day-prep` | T-90 to T-0 |
| Save this at-risk customer | `churn-save-motion-intervention` | Composite signal → save play |
| Flag at-risk customers | `at-risk-identification-escalation` | Nightly view + Slack alerts |
| Design in-app onboarding | `in-app-onboarding-userpilot-appcues-pendo` | Pendo / Userpilot / Appcues |
| Send NPS / CSAT / CES | `nps-csat-ces-tracking` | Delighted / Survicate / Sprig |
| Track adoption | `adoption-metric-feature-usage` | PostHog HogQL cohorts |
| Synthesize voice of customer | `voice-of-customer-reporting` | Themes + Linear handoff |
| Build a CAB | `customer-advisory-board-cab` | Roster + cadence + community |
| Get case studies / G2 reviews | `customer-advocacy-case-study-reference` | Promoter list → invite → reward |
| Automate playbooks | `playbook-automation-churnzero-plays` | CSP plays or Python orchestration |
| Track ramp-to-value | `ramp-to-value-tracking` | TTFV / TTRV funnels |
| Build a customer academy | `success-enablement-academy-certification` | Skilljar / Northpass / Notion |
| Run referrals | `referral-programs` | Friendbuy + Stripe credit |
| Celebrate milestones | `customer-milestone-anniversary` | Anniversary cron triggers |
| Drive feature adoption | `feature-adoption-interventions` | Cohort + Pendo nudge + follow-up |
| Cross-sell multi-product | `multi-product-cross-sell-uplift` | Klaviyo / Customer.io / Outreach |
| Multilingual customer comms | `deepl-mcp` | Translation in cadence |

---

## Updated mappings — replace outdated patterns

Where role.md sections name generic categories ("CSP", "in-app onboarding", "advocacy platform"), the SOTA replacement is:

- **CSP** (Vitally / Catalyst / Gainsight / ChurnZero / Totango / Custify / Velaris / Planhat) → **Vitally** for modern SaaS, **Catalyst (Totango)** for enterprise, **Gainsight** for enterprise CS Ops heavy, **HubSpot custom property + dbt model** for no-CSP fallback.
- **In-app onboarding** (Pendo / Userpilot / Appcues / Chameleon / Whatfix / ProductFruits) → **Pendo** primary, **Userpilot** modern alt, **ProductFruits** free fallback.
- **Sentiment / health AI** (ChurnZero AI / Vitally AI / Sturdy) → **ChurnZero AI** for first-party retention ML, **Sturdy** for cross-system signal extraction.
- **Product analytics** (PostHog / Mixpanel / Amplitude / Heap / FullStory) → **PostHog** primary (CraftBot MCP + open source), **Mixpanel** / **Amplitude** alts.
- **Survey** (Delighted / Survicate / Sprig / Wootric / Iterate) → **Delighted** primary, **Sprig** for in-product micro-surveys.
- **CSM cadence** (Mixmax / Outreach / Salesloft) → **Mixmax** primary for CSM use case, **Outreach** for multi-step expansion sequences.
- **Lifecycle email** (Klaviyo / Customer.io / Iterable) → **Klaviyo** SOTA for product-led, **Customer.io** for in-product trigger-based.
- **Renewal contracts** (PandaDoc / DocuSign / Ironclad / Salesforce CPQ / Zuora) → **PandaDoc** primary for SMB, **DocuSign** for enterprise e-sign, **Ironclad** for CLM.
- **Advocacy** (Influitive / Slapfive / UserEvidence / Champion) → **Influitive** primary for points-based program, **Notion fallback** for low-volume programs.
- **Customer academy** (Skilljar / Northpass / WorkRamp / Intellum) → **Skilljar** primary, **Notion + Loom** fallback.
- **Referrals** (Friendbuy / Referral Rock / Mention Me / GrowSurf / Tremendous) → **Friendbuy** primary for SaaS, **Tremendous** for reward fulfillment, **Stripe credit** as native alt.
- **PLG signal** (Pocus / Koala / Endgame / Common Room) → **Pocus** primary, **Common Room** for community-driven, **PostHog composite** as free fallback.
- **CAB community** (Bevy / Mighty Networks / Slack Connect / Discord) → **Bevy** for purpose-built CAB platforms, **Slack Connect** for B2B-native, **Discord** for community-style customers.
- **Notetaker** (Granola / Fathom / tl;dv / Otter.ai) → **Fathom** primary (free CraftBot skill), **Granola** for in-meeting live notes.
