<!--
Source: https://developer.calendly.com/api-docs/ + https://developers.zoom.us/docs/api/ + https://help.fathom.video/en/articles/8430832-fathom-api + https://posthog.com/docs/api/queries
-->
# QBR Scheduling + Facilitation — SKILL

End-to-end Quarterly Business Review delivery: T-21 round-robin booking via Calendly, Zoom create_meeting with auto-recording, T-7 data pull (PostHog usage, Vitally health, Linear roadmap, Postgres NRR), T-3 deck assembly via pptx, T-1 customer pre-share, T+0 Fathom transcription, T+1 action-item recap, T+2 sync action items back to CSP Project.

## When to use

- **Customer is approaching QBR cadence boundary** — Enterprise quarterly, Growth biannual, Starter annual.
- **Mid-cycle renewal positioning** — T-60 QBR with renewal pricing intro.
- **Save-play QBR** — at-risk customer needs special-purpose business review.
- **CAB-member account** — quarterly all-hands plus QBR.
- **New CSM assignment** — first QBR after handoff; relationship-rebuild.

This skill **complements** `success-plan-goals-milestones` (plan refresh feeds QBR slide 6) and `customer-health-scoring-vitally-catalyst-churnzero` (health score chart on slide 5).

Trigger phrases: "run QBR", "schedule QBR", "QBR deck", "quarterly review", "business review", "T-21".

## Setup

```bash
# Calendly + Zoom + Fathom (CraftBot default skills, but exposed for direct curl)
export CALENDLY_TOKEN="<token>"
export ZOOM_OAUTH_TOKEN="<token>"
export FATHOM_API_KEY="<key>"

# Data sources
export VITALLY_SUBDOMAIN="acme"
export VITALLY_API_KEY="<key>"
# posthog-mcp / postgresql-mcp / linear-mcp already in agent.yaml

# Deck output
# pptx skill is a CraftBot default
```

Workspace prerequisites:
- Calendly event types: "QBR - 60 min" with round-robin of CSM + CSM Lead.
- Zoom OAuth app with `meeting:write` scope.
- Branded pptx template in `templates/qbr-deck-v3.pptx`.
- Vitally Projects exist for the customer (or Notion fallback - `success-plan-goals-milestones`).

## QBR cadence

| Days | Action | Tool |
|---|---|---|
| T-21 | Book the date | `calendly-api` round-robin |
| T-21 | Reserve Zoom | `zoom-mcp create_meeting` |
| T-14 | Confirm attendees | `gmail-mcp` |
| T-7 | Pull QBR data | `posthog-mcp` + Vitally curl + `linear-mcp` + `postgresql-mcp` |
| T-3 | Draft deck (15 slides max) | `pptx` skill |
| T-1 | CSM internal review + customer pre-share | `gmail-mcp` |
| T-0 | Run QBR | Zoom + Fathom auto-record |
| T+1 | Action item recap email | `gmail-mcp` |
| T+2 | Sync action items to CSP Project | `cli-anything` curl Vitally + `linear-mcp` |

## Common recipes

### Recipe 1: T-21 - book QBR via Calendly round-robin

```bash
# Create a single-use scheduling link for the customer
curl -sS -X POST "https://api.calendly.com/scheduling_links" \
  -H "Authorization: Bearer $CALENDLY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "max_event_count": 1,
    "owner": "https://api.calendly.com/event_types/'$QBR_EVENT_TYPE_UUID'",
    "owner_type": "EventType"
  }' | jq -r '.resource.booking_url'
```

Embed in T-21 email: "Time to book your Q3 review. Pick a slot here: [link]."

Doc: https://developer.calendly.com/api-docs/

### Recipe 2: T-21 - reserve Zoom meeting (skeleton)

```bash
curl -sS -X POST "https://api.zoom.us/v2/users/me/meetings" \
  -H "Authorization: Bearer $ZOOM_OAUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Q3 QBR - Acme Corp",
    "type": 2,
    "start_time": "2026-09-15T15:00:00Z",
    "duration": 60,
    "settings": {
      "join_before_host": false,
      "auto_recording": "cloud",
      "approval_type": 0,
      "host_video": true,
      "participant_video": true
    }
  }' | jq '{join_url, password, id}'
```

Sync the `join_url` into the Calendly event description after customer picks slot.

### Recipe 3: T-7 - pull usage from PostHog (HogQL)

```sql
-- Q3 adoption snapshot for QBR slide 4
SELECT
  toStartOfMonth(timestamp) AS month,
  uniq(properties.user_id) AS mau,
  count() AS events,
  uniq(distinct_id) FILTER (WHERE event = 'key_feature_used') AS key_feature_users,
  uniq(distinct_id) FILTER (WHERE event = 'user_action') AS active_users,
  (uniq(distinct_id) FILTER (WHERE event = 'user_action' AND timestamp >= now() - INTERVAL 1 DAY) * 1.0
   / nullif(uniq(distinct_id) FILTER (WHERE event = 'user_action' AND timestamp >= now() - INTERVAL 30 DAY), 0)) AS dau_mau
FROM events
WHERE properties.customer_id = '$CUSTOMER_ID'
  AND timestamp >= now() - INTERVAL 90 DAY
GROUP BY month
ORDER BY month;
```

Via `posthog-mcp query`. Output -> slide 4 chart.

### Recipe 4: T-7 - pull health score from Vitally

```bash
curl -sS "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/accounts/external/$CUSTOMER_ID?include=healthScores,traits" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" \
  | jq '{
      name,
      health: .healthScore.score,
      breakdown: [.healthScore.breakdown[] | {name, score, weight}],
      mrr: .mrr,
      arr: (.mrr * 12)
    }'
```

Plot 90d health trajectory -> slide 5.

### Recipe 5: T-7 - pull roadmap commits from Linear

Via `linear-mcp issues_search`:
- Filter: `label = vox-of-customer` AND `assignee.team IN (Eng/Product)` AND `state IN (In Progress, Done, Cancelled)`.
- Pull last 90d. Split: Done (slide 9), In Progress (slide 9), Cancelled (slide 10 - "deprioritized").

### Recipe 6: T-7 - pull NRR from Postgres warehouse

```sql
-- Customer's cohort NRR for this quarter
WITH revenue AS (
  SELECT date_trunc('month', period_start) AS month,
         sum(amount_decimal) / 100.0 AS mrr
  FROM stripe_invoices
  WHERE customer_id = '$CUSTOMER_ID' AND status = 'paid'
  GROUP BY 1
)
SELECT month, mrr,
       lag(mrr) OVER (ORDER BY month) AS prev_mrr,
       mrr / nullif(lag(mrr) OVER (ORDER BY month), 0) - 1.0 AS mom_change
FROM revenue
ORDER BY month DESC LIMIT 6;
```

Via `postgresql-mcp`. Pipe to slide 11 (renewal outlook).

### Recipe 7: T-3 - build the QBR deck (pptx skill)

15-slide structure (no more, no less):
1. Cover - Customer, Quarter, CSM, Date
2. Executive summary - 3 sentences
3. Wins this quarter - 3 concrete bullets
4. Adoption snapshot (PostHog chart from Recipe 3)
5. Health score trajectory (Recipe 4)
6. Open items - 3 in-flight outcomes from success plan
7. Open items - risks + mitigations
8. Voice of customer - synthesized themes from `voice-of-customer-reporting`
9. Roadmap update - what shipped + what's next (Recipe 5)
10. Roadmap update - what's deprioritized + why (honest)
11. Renewal outlook - forecast + classification (Recipe 6)
12. Expansion opportunities (if any from `expansion-opportunity-identification`)
13. Action items for customer
14. Action items for us
15. Next QBR + close

Use `pptx` skill `populate_from_template(template='qbr-deck-v3.pptx', data={...})`.

### Recipe 8: T-1 - pre-share with customer

```python
# gmail-mcp send_email
subject = f"Pre-read: {customer} Q3 QBR ({qbr_date})"
body = f"""
Hi {champion_name},

Attached is the QBR pre-read. Two asks before we meet:

1. Skim slides 6-7 (open outcomes + risks). Let me know if anything is mis-stated.
2. Skim slide 11 (renewal outlook). I'll walk you through it live but worth a heads-up.

Looking forward to {qbr_date}.

{csm_name}
"""
gmail.send_email(to=[champion_email], subject=subject, body=body, attachments=['qbr.pptx'])
```

No "hope you're doing well." Be direct.

### Recipe 9: T-0 - Fathom auto-transcribe + summary

```bash
# After the QBR call, pull transcript (Fathom auto-attaches)
curl -sS "https://api.fathom.video/external/v1/meetings/$MEETING_ID/summary" \
  -H "X-Api-Key: $FATHOM_API_KEY" | jq '.summary, .action_items'
```

Doc: https://help.fathom.video/en/articles/8430832-fathom-api

### Recipe 10: T+1 - action-item recap email

Template:
```
Subject: QBR recap + next steps - [Customer]

Hi [name],

Thanks for the time today. Here's what we agreed:

For your team:
1. [action + owner + due date]
2. [action + owner + due date]

For us:
1. [action + owner + due date]
2. [action + owner + due date]

Roadmap commitments:
- [item] - tracked as ENG-1234, ship target [date or "no ETA - voice-of-customer queue"]

Next QBR: [date], calendar hold sent.

Reply by EOD Friday if anything to add.

- [CSM]
```

### Recipe 11: T+2 - sync action items to Vitally Project as milestones

```bash
# For each action item:
curl -sS -X POST "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/projects/$PROJECT_ID/milestones" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" \
  -d '{"name": "QBR action: '$ACTION'", "dueDate": "'$DUE_DATE'", "assignee": "'$OWNER'"}'
```

And create Linear issues for the eng/product items:
- Via `linear-mcp create_issue`, label `qbr-action`, customer_id property set.

### Recipe 12: Post-QBR sentiment check

After T+3, send a 1-question Sprig in-product micro-survey to the QBR attendees: "How useful was today's QBR?" 1-5. Use to tune cadence.

```bash
curl -sS -X POST "https://api.sprig.com/v1/surveys/$POST_QBR_SURVEY_ID/responses/enqueue" \
  -H "Authorization: Bearer $SPRIG_API_KEY" \
  -d '{"user_id": "'$CHAMPION_USER_ID'", "delay_minutes": 10}'
```

## Examples

### Example 1: First QBR with newly assigned CSM

**Goal:** New CSM took over Acme last week. First QBR in 21 days. Relationship-rebuild + position renewal.

**Steps:**
1. Recipe 1 (Calendly) + Recipe 2 (Zoom) at T-21.
2. New CSM listens to previous QBR's Fathom recording (Recipe 9 reverse) - get context.
3. T-7 Recipe 3-6 data pull.
4. T-3 deck (Recipe 7) - extra emphasis on slide 1: "Your new CSM, [name]; here's how I'm picking up where [predecessor] left off."
5. T-1 pre-share (Recipe 8) + explicitly ask champion: "Any open issues from previous QBR I should know about?"
6. T+0 run; capture extra notes on relationship continuity.
7. T+1 recap + T+2 sync (Recipes 10-11).

**Result:** Smooth handoff, relationship trust preserved.

### Example 2: At-risk customer T-60 QBR with pricing intro

**Goal:** Acme is Yellow health, renewal T-60. QBR doubles as save play + renewal positioning.

**Steps:**
1. Confirm classification from `at-risk-identification-escalation`.
2. Internal alignment with sales-agent on pricing before deck assembly.
3. Recipe 7 deck adjustments: slide 11 (renewal) becomes load-bearing - include 3 commercial options.
4. Slide 7 (risks) names the explicit at-risk signals; slide 6 (open outcomes) shows save plan progress.
5. Run QBR with CSM Lead joining.
6. T+1 recap *also* CCs sales-agent; T+2 routes commercial decision to renewals workflow.

**Result:** Honest QBR, save play armed, renewal positioned.

## Edge cases / gotchas

- **Customer reschedules at T-3** — deck is half-built. Don't rebuild; reuse for new date. Just refresh data on day-of via Recipe 3-6.
- **Champion not attending** — exec sponsor only. Adjust slide order: lead with strategic outlook (slide 11), de-emphasize tactical (slide 4).
- **No data for slide 4 (low-volume customer)** — replace adoption chart with a use-case-progress chart. Don't show empty graphs.
- **Roadmap slide 10 honesty** — naming deprioritized features = trust-building, not trust-destroying. Do it.
- **Action item recap goes unread** — link single-use Calendly for follow-through if needed; don't let recap die.
- **Fathom recording missing** — customer denied recording. Use Granola (local) for personal notes; document plain-text action items.
- **CSP doesn't sync milestones** — confirm Vitally Project ID exists; Recipe 11 fails silently if not. Add Sentry alert.
- **Slide count creep** — 15 slides is the hard cap. If you have 17, two need to die. Don't run a 30-min deck in 60 min.
- **Customer asks for the deck to be edited post-QBR** — push back unless it was factually wrong. Send recap email instead.
- **Time zone alignment** — Calendly auto-converts; Zoom does NOT. Triple-check Zoom `start_time` is UTC.

## Sources

- [Calendly API v2 docs](https://developer.calendly.com/api-docs/)
- [Calendly scheduling links](https://developer.calendly.com/api-docs/UG9zdA-create-a-single-use-scheduling-link)
- [Zoom Meetings API](https://developers.zoom.us/docs/api/meetings/)
- [Fathom API docs](https://help.fathom.video/en/articles/8430832-fathom-api)
- [PostHog HogQL Query API](https://posthog.com/docs/api/queries)
- [Vitally Accounts API](https://docs.vitally.io/reference/accounts)
- [Linear API docs](https://developers.linear.app/docs/graphql/working-with-the-graphql-api)
- [Stripe Subscriptions API](https://stripe.com/docs/api/subscriptions)
- [Sprig API surveys](https://docs.sprig.com/)
- [Gainsight QBR best practices](https://www.gainsight.com/blog/quarterly-business-review/)
