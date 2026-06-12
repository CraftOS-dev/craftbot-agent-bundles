<!--
Source: https://www.pocus.com/ + https://docs.commonroom.io/ + https://posthog.com/docs/api/queries + https://developers.hubspot.com/docs/api/crm/companies
-->
# Expansion Opportunity Identification — SKILL

Aggregate expansion signals (feature-limit hits, multi-workspace creation, integration adoption, community intent, CSP health > 0.85, sponsor engaged) into a composite ExpansionScore, rank accounts, route to CSM (usage uplift) or AE (new SKU / multi-year). Sources: PostHog HogQL, Pocus, Common Room, Mixpanel, Amplitude, HubSpot/Salesforce, Vitally. Free fallback: PostHog composite only.

## When to use

- **Weekly expansion review** — CSM team needs the top 20 expansion-ready accounts.
- **Post-onboarding handoff** — Day 60 milestone hit; check expansion-readiness.
- **Renewal positioning** — T-60 pre-renewal, identify expansion to package with renewal.
- **Quota replan** — sales asks "which accounts to lean on for expansion next quarter?"
- **PLG -> sales handoff** — high-intent free user triggers AE attention.

This skill **feeds** `multi-product-cross-sell-uplift` (which executes outreach) and `renewal-management-90-day-prep` (which packages expansion with renewal). It **reads from** `customer-health-scoring-vitally-catalyst-churnzero` (health gate).

Trigger phrases: "expansion opportunities", "expansion-ready", "upsell candidates", "Pocus signals", "PLG signals", "feature limit hit", "multi-workspace".

## Setup

```bash
# Pocus (PLG signal aggregation)
export POCUS_API_KEY="<key>"

# Common Room (community + dark social)
export COMMON_ROOM_API_KEY="<key>"

# Koala (alt PLG intent)
export KOALA_API_KEY="<key>"

# Endgame (alt PLG sales)
export ENDGAME_API_KEY="<key>"

# Free fallback
# posthog-mcp + mixpanel-mcp + amplitude-mcp in agent.yaml
# HubSpot / Salesforce via api-gateway / salesforce-api default skills
```

Workspace prerequisites:
- PostHog event taxonomy includes `feature_limit_hit`, `workspace_created`, `integration_added`, `seat_added`.
- CSP traits include `health_score`, `sponsor_last_seen_days`.
- CRM deal stage taxonomy includes `post_onboarding`, `expansion_qualified`.
- Plan-tier-to-limit mapping (e.g., Starter = 5 seats, Growth = 25, Enterprise = unlimited).

## Composite ExpansionScore

```
ExpansionScore = 0.30 * usage_growth_30d_normalized
               + 0.25 * feature_limit_hit_normalized
               + 0.20 * multi_workspace_signal
               + 0.15 * csp_health_score
               + 0.10 * community_intent_signal
```

ExpansionScore >= 0.7 -> expansion-ready.

## Common recipes

### Recipe 1: PostHog HogQL - feature-limit-hit signal

```sql
SELECT
  properties.customer_id AS customer_id,
  count() AS limit_hits_30d,
  uniq(properties.feature_name) AS distinct_features_hit,
  max(timestamp) AS most_recent_hit
FROM events
WHERE event = 'feature_limit_hit'
  AND timestamp >= now() - INTERVAL 30 DAY
GROUP BY properties.customer_id
HAVING count() >= 3
ORDER BY count() DESC;
```

Via `posthog-mcp query`. Doc: https://posthog.com/docs/api/queries

### Recipe 2: PostHog HogQL - multi-workspace creation

```sql
SELECT
  properties.customer_id,
  count(DISTINCT properties.workspace_id) AS workspaces_30d
FROM events
WHERE event = 'workspace_created'
  AND timestamp >= now() - INTERVAL 90 DAY
GROUP BY properties.customer_id
HAVING count(DISTINCT properties.workspace_id) >= 2;
```

Multi-workspace = strong expansion signal in B2B SaaS.

### Recipe 3: PostHog HogQL - usage growth 30d

```sql
WITH cur AS (
  SELECT properties.customer_id, count() AS events_cur
  FROM events
  WHERE timestamp BETWEEN now() - INTERVAL 30 DAY AND now()
  GROUP BY properties.customer_id
),
prev AS (
  SELECT properties.customer_id, count() AS events_prev
  FROM events
  WHERE timestamp BETWEEN now() - INTERVAL 60 DAY AND now() - INTERVAL 30 DAY
  GROUP BY properties.customer_id
)
SELECT
  cur.properties_customer_id,
  cur.events_cur,
  prev.events_prev,
  (cur.events_cur - prev.events_prev) * 1.0 / nullif(prev.events_prev, 0) AS growth_30d
FROM cur JOIN prev ON cur.properties_customer_id = prev.properties_customer_id
WHERE prev.events_prev > 100
ORDER BY growth_30d DESC;
```

### Recipe 4: Pocus signals

```bash
curl -sS "https://api.pocus.com/v1/signals?customer_id=$CUSTOMER_ID&since=30d" \
  -H "Authorization: Bearer $POCUS_API_KEY" | jq '.signals[] | {type, score, evidence}'
```

Doc: https://www.pocus.com/

Pocus aggregates: feature usage, seat growth, integration depth, billing approach.

### Recipe 5: Common Room community signals

```bash
curl -sS "https://api.commonroom.io/v1/signals?organization_id=$CUSTOMER_ID&type=intent" \
  -H "Authorization: Bearer $COMMON_ROOM_API_KEY" | jq '.results'
```

Doc: https://docs.commonroom.io/

Common Room surfaces: GitHub stars, Discord mentions, LinkedIn job changes, blog mentions.

### Recipe 6: Koala / Endgame alt signals

```bash
curl -sS "https://api.koala.live/v1/accounts/$CUSTOMER_ID/intent" \
  -H "Authorization: Bearer $KOALA_API_KEY"
```

### Recipe 7: Read CSP health gate

```bash
curl -sS "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/accounts/external/$CUSTOMER_ID?include=healthScores,traits" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" \
  | jq '{health: .healthScore.score, sponsor_active: (.traits.sponsor_last_seen_days < 14)}'
```

Health < 0.7 -> drop from expansion list (re-route to health/save).

### Recipe 8: CRM deal-stage filter

```bash
# HubSpot: customers post-onboarding, no open expansion deal
curl -sS "https://api.hubapi.com/crm/v3/objects/companies/search" \
  -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "filterGroups": [{
      "filters": [
        {"propertyName": "lifecyclestage", "operator": "EQ", "value": "customer"},
        {"propertyName": "days_since_onboarded", "operator": "GTE", "value": 60},
        {"propertyName": "open_expansion_deal", "operator": "EQ", "value": "false"}
      ]
    }],
    "properties": ["name", "arr", "tier", "csm_owner"]
  }'
```

### Recipe 9: Materialize ranked expansion list

```sql
WITH signals AS (
  SELECT customer_id,
         coalesce(limit_hits_30d, 0) AS limit_hits,
         coalesce(workspaces_30d, 1) AS workspaces,
         coalesce(growth_30d, 0) AS usage_growth,
         coalesce(health_score, 0.5) AS health,
         coalesce(community_intent_score, 0) AS community_intent
  FROM customers c
  LEFT JOIN feature_limit_hits USING (customer_id)
  LEFT JOIN workspace_signals USING (customer_id)
  LEFT JOIN usage_growth USING (customer_id)
  LEFT JOIN health_scores USING (customer_id)
  LEFT JOIN common_room_signals USING (customer_id)
)
SELECT
  customer_id,
  0.30 * least(1.0, greatest(0, usage_growth / 0.5))
  + 0.25 * least(1.0, limit_hits / 5.0)
  + 0.20 * least(1.0, (workspaces - 1) / 3.0)
  + 0.15 * health
  + 0.10 * community_intent
  AS expansion_score,
  -- Inputs for transparency
  jsonb_build_object(
    'usage_growth', usage_growth,
    'limit_hits', limit_hits,
    'workspaces', workspaces,
    'health', health,
    'community_intent', community_intent
  ) AS signal_inputs
FROM signals
WHERE health >= 0.7
ORDER BY expansion_score DESC
LIMIT 20;
```

### Recipe 10: Route to CSM vs AE

Routing decision per row:
- **CSM-led usage uplift** (seat expansion within current SKU, edition uplift): CSM owns. Calendly book "usage review", deck via `pptx`.
- **AE-led close** (new SKU, multi-year, contract changes): hand off to `sales-agent` with full context.

Heuristic:
- Small uplift (< $20k ARR) + same SKU -> CSM
- Big uplift (>= $20k ARR) or new SKU or multi-year -> AE

### Recipe 11: Slack post to CS-AE channel

```python
slack.chat_postMessage(
    channel="#cs-ae-expansion",
    text=f"""
:rocket: Top 5 expansion-ready accounts (week of {week_of}):

1. {acct1.name} - ${acct1.arr_potential:,.0f} potential
   Signals: usage +47%, hit limit 8x, 3 workspaces. Health 0.84.
   Route: CSM ({acct1.csm_owner})
   Action: book usage review by EOD Friday.

2. {acct2.name} - ${acct2.arr_potential:,.0f} potential
   Signals: hit Enterprise SSO limit 5x last week. Health 0.79.
   Route: AE handoff ({acct2.ae_owner}) - new SKU.
   Action: AE owns; CSM brief sent.

[continues]
"""
)
```

### Recipe 12: Notion expansion board

```python
# notion-mcp create_page in "Expansion Board" DB
notion.create_page(
    parent={"database_id": EXPANSION_BOARD_DB_ID},
    properties={
        "Customer": {"title": [{"text": {"content": acct.name}}]},
        "Signal": {"multi_select": [{"name": s} for s in acct.top_signals]},
        "ARR Potential": {"number": acct.arr_potential},
        "Tier": {"select": {"name": acct.tier}},
        "Sponsor": {"rich_text": [{"text": {"content": acct.sponsor_name}}]},
        "CSM": {"people": [{"id": acct.csm_user_id}]},
        "AE": {"people": [{"id": acct.ae_user_id}] if acct.ae_user_id else []},
        "Status": {"status": {"name": "Identified"}},
        "Next Action": {"rich_text": [{"text": {"content": acct.next_action}}]},
    },
)
```

## Examples

### Example 1: Weekly expansion review (Monday morning)

**Goal:** Monday 09:00 UTC, CS-AE team has the top 20 expansion list.

**Steps:**
1. Sunday 23:00 UTC: Recipes 1-7 (signals) feed into Postgres.
2. Monday 06:00 UTC: Recipe 9 computes ExpansionScore + ranks.
3. Recipe 10 routes each (CSM vs AE).
4. Recipe 11 posts top 5 to Slack.
5. Recipe 12 updates Notion expansion board.

**Result:** Team has prioritized expansion list to start the week.

### Example 2: AE flagged a no-signal expansion lead

**Goal:** AE says "expand Acme this quarter." Agent's data shows ExpansionScore = 0.42 (below threshold). What's missing?

**Steps:**
1. Pull individual signal breakdown for Acme.
2. Health = 0.78 (good), but usage_growth = -8% (flat-to-down). No limit hits.
3. Counter to AE: usage data doesn't support expansion narrative. Risk: pitching uplift to flat user.
4. Recommend: book usage review with CSM first; uncover real business outcomes; revisit in 30d.

**Result:** Honest signal pushback; quarterly motion stays disciplined.

## Edge cases / gotchas

- **Pocus / Common Room paid** — free fallback is PostHog-only composite (Recipes 1-3, 9 with `community_intent_signal = 0`). Workable but loses community intent.
- **Feature-limit event missing** — instrument it. Without `feature_limit_hit`, you can't detect upgrade-pressure. PR product to fire on near-limit (e.g., 80% of cap).
- **Plan-tier-to-limit mapping** — Starter = 5 seats; Growth = 25; Enterprise = unlimited. Hardcoded means re-deploy on pricing changes; better: read from product config table.
- **Community-intent noise** — GitHub stars from a single contributor != company intent. Common Room dedupes; verify before triggering AE outreach.
- **Multi-workspace = consolidation, not expansion** — some customers create lots of workspaces to test; not buying signal. Cross-check with seat growth.
- **CRM duplicate companies** — same customer logged under HubSpot domain mismatch. Dedupe before scoring; otherwise score the wrong account.
- **AE-CSM handoff handoff loss** — AE takes the expansion; CSM never hears back; renewal forecast is stale. Force linked Linear / SFDC opp + status sync.
- **Routing heuristic over-simplifies** — sometimes CSM should own a $50k uplift because they have the champion relationship. Override rule should exist in Notion expansion board.
- **Customers don't want unsolicited expansion outreach** — health > 0.7 + sponsor engaged + signal is the gate. Don't pitch low-health customers.
- **Score drift after weight change** — if you tune weights (e.g., bump usage_growth to 0.35), recompute everyone before publishing. Don't surprise sales with shuffled ranking.
- **Expansion fatigue** — same accounts top of list 4 weeks running with no movement. Tag "stuck"; CSM needs to call champion, not just re-rank.

## Sources

- [PostHog HogQL Query API](https://posthog.com/docs/api/queries)
- [PostHog Cohorts](https://posthog.com/docs/data/cohorts)
- [Pocus PLG signals docs](https://www.pocus.com/)
- [Common Room API](https://docs.commonroom.io/)
- [Koala API](https://www.getkoala.com/)
- [Endgame intent](https://www.endgame.io/)
- [HubSpot Companies API](https://developers.hubspot.com/docs/api/crm/companies)
- [Salesforce SOQL reference](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql.htm)
- [Vitally Accounts API](https://docs.vitally.io/reference/accounts)
- [Notion API create page](https://developers.notion.com/reference/post-page)
