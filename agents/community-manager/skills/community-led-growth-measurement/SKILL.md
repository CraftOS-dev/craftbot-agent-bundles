<!--
Sources: https://www.reforge.com/blog/community-led-growth + https://www.commonroom.io/blog/measuring-community-roi/ + https://docs.commonroom.io/api/ + https://posthog.com/docs/hogql
-->
# Community-Led Growth Measurement — SKILL

Reforge CLG framework: input metrics (members joined, % activated, % posting weekly) → middle metrics (member → MQL, support deflection rate) → output metrics (retention lift, expansion lift, advocacy lift, CAC reduction). Common Room + PostHog + warehouse join. Output: dbt model + weekly digest + dashboard.

## When to use

- Leadership asks "what's our community worth?" — need measurable answer.
- CMO/CEO planning next-year budget; community team needs to justify headcount.
- Acquiring B2B SaaS where community is the moat — diligence requires CLG model.
- Quarterly board meeting where community team presents impact.
- Pre-hiring next community manager; need impact baseline.
- Pivoting strategy — knowing which lever (acquisition / retention / advocacy / deflection) is the engine.

Trigger phrases: "CLG", "community-led growth", "community ROI", "member-to-MQL", "support deflection", "retention lift", "Reforge CLG".

## Setup

```bash
# Common Room — member graph
curl -H "Authorization: Bearer $COMMON_ROOM_TOKEN" \
  https://app.commonroom.io/api/v1/members?limit=1000

# PostHog — product events
mcp tool posthog.query --query "SELECT distinct_id, MAX(timestamp) FROM events WHERE event='\$identify' GROUP BY distinct_id"

# Postgres warehouse for dbt
psql -h $WAREHOUSE -U $USER -c "\dt staging.*"

# dbt
dbt run --select community_clg
```

Auth + env:
- `COMMON_ROOM_TOKEN` — Common Room API.
- `POSTHOG_API_KEY` — PostHog project API key.
- `HUBSPOT_TOKEN` or `SALESFORCE_TOKEN` — CRM join.
- `WAREHOUSE_URL` — Postgres / Snowflake / BigQuery.

Workspace prerequisites:
- Warehouse with `community_members`, `product_events`, `crm_contacts`, `revenue_events` tables.
- dbt project for CLG models.
- BI tool (Metabase / Looker / Mode / Hex) for dashboards.

## Common recipes

### Recipe 1: Reforge 5-tier metric stack

| Tier | Metric | Definition | Target |
|---|---|---|---|
| Input | Members joined / mo | New community joins | growth +20% MoM |
| Input | Activation % | % joined posting in 7d | 25%+ B2C, 15%+ B2B |
| Input | Weekly active % | % MAU posting weekly | 8-15% |
| Middle | Member → MQL conversion | members reaching MQL threshold | 5-12% |
| Middle | Support deflection rate | % support qs answered by community vs ticket | 30-60% |
| Output | Retention lift | LTV(member) / LTV(non-member) | 1.3-1.8x |
| Output | Expansion lift | NRR(member) / NRR(non-member) | 1.15-1.3x |
| Output | Advocacy lift | referral CVR vs paid | 2-4x |
| Output | Brand love | NPS(member) - NPS(non-member) | +10-20 |

### Recipe 2: Common Room → warehouse sync

```bash
# Daily extract via Common Room API → S3 → warehouse
curl -H "Authorization: Bearer $COMMON_ROOM_TOKEN" \
  "https://app.commonroom.io/api/v1/members?updated_since=$LAST_RUN" \
  | jq -c '.results[]' \
  | aws s3 cp - s3://warehouse-raw/community/members/$(date +%Y%m%d).jsonl

# COPY into Postgres
psql -c "COPY staging.community_members_raw FROM 's3://warehouse-raw/community/members/$(date +%Y%m%d).jsonl' WITH (FORMAT JSON);"
```

### Recipe 3: dbt model — member identity

```sql
-- models/community_member_identity.sql
WITH cr AS (
  SELECT id AS commonroom_id, email, name FROM staging.commonroom_members
),
ph AS (
  SELECT distinct_id, email, properties FROM staging.posthog_persons
),
hs AS (
  SELECT id AS hubspot_id, email, lifecyclestage, mrr FROM staging.hubspot_contacts
)
SELECT
  COALESCE(cr.email, ph.email, hs.email) AS email,
  cr.commonroom_id,
  ph.distinct_id AS posthog_id,
  hs.hubspot_id,
  hs.lifecyclestage,
  hs.mrr
FROM cr
FULL OUTER JOIN ph USING (email)
FULL OUTER JOIN hs USING (email);
```

### Recipe 4: Member-to-MQL conversion

```sql
-- models/clg_member_mql.sql
WITH joined AS (
  SELECT email, MIN(joined_at) AS joined_at FROM community_member_identity
  WHERE commonroom_id IS NOT NULL
  GROUP BY email
),
mql_hit AS (
  SELECT email, MIN(date) AS mql_at FROM hubspot_lifecycle_history
  WHERE lifecyclestage = 'marketingqualifiedlead'
  GROUP BY email
)
SELECT
  DATE_TRUNC('month', j.joined_at) AS cohort,
  COUNT(*) AS joined,
  COUNT(m.email) FILTER (WHERE m.mql_at > j.joined_at) AS became_mql_post_join,
  ROUND(100.0 * COUNT(m.email) FILTER (WHERE m.mql_at > j.joined_at) / COUNT(*), 1) AS mql_conversion_pct
FROM joined j
LEFT JOIN mql_hit m USING (email)
GROUP BY 1 ORDER BY 1 DESC;
```

### Recipe 5: Support deflection rate

```sql
-- models/clg_support_deflection.sql
WITH q AS (
  SELECT id, channel, body, answered_in_community, answered_by_support, created_at
  FROM community_questions
  WHERE created_at > NOW() - INTERVAL '30 days'
)
SELECT
  COUNT(*) AS total_questions,
  COUNT(*) FILTER (WHERE answered_in_community) AS comm_answered,
  COUNT(*) FILTER (WHERE NOT answered_in_community AND answered_by_support) AS ticket_answered,
  ROUND(100.0 * COUNT(*) FILTER (WHERE answered_in_community) / COUNT(*), 1) AS deflection_pct,
  ROUND(COUNT(*) FILTER (WHERE answered_in_community) * 12.50, 2) AS dollars_saved -- $12.50/avg ticket
FROM q;
```

### Recipe 6: Retention lift

```sql
-- models/clg_retention_lift.sql
WITH cohorts AS (
  SELECT
    email, joined_at,
    CASE WHEN commonroom_id IS NOT NULL THEN 'member' ELSE 'non_member' END AS segment
  FROM community_member_identity
),
retention AS (
  SELECT c.email, c.segment, c.joined_at,
    MAX(CASE WHEN sub.cancelled_at IS NULL THEN 1 ELSE 0 END) AS still_active_24mo
  FROM cohorts c
  JOIN subscription_events sub ON sub.email = c.email
  WHERE c.joined_at < NOW() - INTERVAL '24 months'
  GROUP BY 1, 2, 3
)
SELECT
  segment,
  COUNT(*) AS cohort_size,
  ROUND(100.0 * AVG(still_active_24mo), 1) AS retention_24mo_pct
FROM retention GROUP BY segment;
-- Retention lift = retention(member) / retention(non_member)
```

### Recipe 7: Expansion lift (NRR)

```sql
-- models/clg_expansion_lift.sql
WITH base AS (
  SELECT email, MRR_at_start, MRR_at_end_12mo, segment
  FROM nrr_cohort_calc
)
SELECT
  segment,
  ROUND(100.0 * AVG(MRR_at_end_12mo / NULLIF(MRR_at_start, 0)), 1) AS nrr_pct
FROM base GROUP BY segment;
-- Expansion lift = NRR(member) / NRR(non_member)
```

### Recipe 8: Advocacy lift

```sql
-- models/clg_advocacy_lift.sql
WITH refs AS (
  SELECT
    referrer_email,
    COUNT(*) AS referrals,
    COUNT(*) FILTER (WHERE converted) AS conversions
  FROM referral_events
  GROUP BY referrer_email
),
classified AS (
  SELECT
    r.*,
    CASE WHEN cmi.commonroom_id IS NOT NULL THEN 'member' ELSE 'non_member' END AS segment
  FROM refs r
  LEFT JOIN community_member_identity cmi USING (email)
)
SELECT segment,
  COUNT(*) AS referrers,
  SUM(referrals) AS total_referrals,
  ROUND(100.0 * SUM(conversions) / NULLIF(SUM(referrals), 0), 1) AS referral_cvr
FROM classified GROUP BY segment;
```

### Recipe 9: PostHog event for community handoff

```javascript
// In your app, fire on community join via webhook
posthog.capture('community_joined', {
  platform: 'discord',
  member_id: '...',
  $set: {is_community_member: true, joined_community_at: new Date()}
});
```

```bash
mcp tool posthog.query --query "
SELECT properties.platform, COUNT(*) AS joins
FROM events WHERE event = 'community_joined'
  AND timestamp > now() - INTERVAL 7 day
GROUP BY properties.platform"
```

### Recipe 10: Weekly digest email

```python
metrics = {
  'joined': run_sql("SELECT COUNT(*) FROM cmi WHERE joined_at > NOW() - INTERVAL '7 days'"),
  'activation_pct': run_sql("SELECT ROUND(100.0 * activated / joined, 1) FROM weekly_activation"),
  'deflection_pct': run_sql("SELECT * FROM clg_support_deflection"),
  'champion_count': run_sql("SELECT COUNT(*) FROM commonroom_segments WHERE name='Champions'"),
}

email_body = render_template("weekly_clg.md", metrics=metrics)
mcp.gmail.send(to="ceo@brand.com", subject=f"Weekly CLG · {date.today()}", body=email_body)
```

## Examples

### Example 1: SaaS B2B model

**Goal:** Quarterly board slide proving community justifies $250k/yr team.

**Steps:**
1. Build community-member-identity model (Recipe 3).
2. Run Recipes 4-8 across 24mo data.
3. Output: retention lift 1.4x, expansion 1.2x, advocacy 3.1x, deflection 42%.
4. Math: 1,200 community members × $X retention dollars + $Y deflection = $1.3M impact.
5. Quarterly slide via pptx skill.

**Result:** Board approves headcount expansion; community team becomes revenue line.

### Example 2: PLG SaaS — community as activation

**Goal:** Tie community joins to free-to-paid CVR.

**Steps:**
1. PostHog `community_joined` event (Recipe 9).
2. Cohort: free users → joined community in trial vs not.
3. Compare 30-day paid CVR.
4. Result: joined cohort 3.4x CVR.
5. Optimization: nudge community-join in trial Day 3.

**Result:** Trial-to-paid CVR +18% after nudge rollout.

## Edge cases / gotchas

- **Correlation ≠ causation** — heavy users join community; community doesn't cause heavy use. Use cohort matching by tenure + ICP.
- **Identity stitching gaps** — Discord username ≠ email; need member-supplied connection or manual map. Coverage <70% breaks the math.
- **Survivorship bias** — only retained members reach community; comparing to all non-members overstates lift.
- **Common Room paywall** — Starter $X/mo minimum; lean alternatives: Threado, custom Postgres scoring.
- **PostHog event mismatch** — `$identify` not always called; check coverage before trusting.
- **Quarterly vs monthly cadence** — CLG metrics are slow; report monthly trends but value-prop quarterly.
- **Deflection over-counting** — community-answered ≠ would-have-ticketed. Use control: "would you have opened a ticket?" survey.
- **Expansion lift confounders** — enterprise plan members are both in community AND on high-touch CSM. Isolate.
- **Brand love NPS** — keep member NPS panel separate from product NPS.
- **Membership recency decay** — joining 18mo ago ≠ active. Use rolling activity score, not lifetime tag.
- **Don't gold-plate** — VP wants 1 number, not 18. Headline: "Community LTV 1.4x non-community LTV."

## Sources

- [Reforge — Community-Led Growth](https://www.reforge.com/blog/community-led-growth)
- [Common Room — Measuring Community ROI](https://www.commonroom.io/blog/measuring-community-roi/)
- [Common Room API](https://docs.commonroom.io/api/)
- [PostHog HogQL](https://posthog.com/docs/hogql)
- [dbt project structure](https://docs.getdbt.com/docs/build/projects)
- [HubSpot CRM Properties API](https://developers.hubspot.com/docs/api/crm/properties)
