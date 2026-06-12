<!--
Sources:
Amplitude MCP — https://amplitude.com/docs/mcp
Mixpanel MCP — https://developer.mixpanel.com/docs/mcp
PostHog MCP — https://posthog.com/docs/model-context-protocol
-->
# Amplitude / Mixpanel / PostHog Product Analytics — SKILL

The three SOTA product-analytics platforms; pick by team adoption. This pack covers funnels, retention, activation, cohorts, and the North Star metric across all three. PostHog is the open-source SOTA; Amplitude is the enterprise default; Mixpanel sits in the middle.

## When to use

- Querying the activation funnel (sign-up → first value).
- Building D1/D7/D30 retention cohort curves.
- Behavioral cohort definition ("users who did X in the last 7 days").
- North Star metric weekly delta for stakeholder updates.
- Cohort-on-cohort comparison (e.g., onboarding-revamp vs baseline).
- Sunset analysis (how many users still use the deprecated feature).

Trigger phrases: "what's our D7 retention", "why is activation dropping", "how many users hit the funnel", "weekly KPI snapshot", "show the retention curve", "build the activation funnel".

## Setup

### PostHog (open-source SOTA — free self-host)

```bash
# PostHog MCP — HogQL, feature flags, retention, funnels, replay
npx -y @posthog/mcp-server@latest
```

Auth:
- `POSTHOG_API_KEY` — personal API key from PostHog → Settings → Personal API keys.
- `POSTHOG_HOST` — `https://app.posthog.com` (cloud) or self-host URL.

### Amplitude

```bash
# Amplitude MCP — official, GA early 2026
npx -y @amplitude/mcp-server@latest
```

Auth:
- `AMPLITUDE_API_KEY` + `AMPLITUDE_SECRET_KEY` — project pair from Amplitude → Settings → Projects.

### Mixpanel

```bash
# Mixpanel MCP
npx -y @mixpanel/mcp-server@latest
```

Auth:
- `MIXPANEL_SERVICE_ACCOUNT` + `MIXPANEL_SECRET` from Mixpanel → Personal Tokens.

## Common recipes

### Recipe 1: Funnel (sign-up → activation)

#### PostHog (HogQL)

```sql
-- Run via `posthog.query` HogQL tool
SELECT
  step,
  count(DISTINCT person_id) AS users,
  count(DISTINCT person_id) * 100.0 /
    FIRST_VALUE(count(DISTINCT person_id))
    OVER (ORDER BY step) AS pct_of_top
FROM (
  SELECT
    person_id,
    multiIf(event = 'signup_completed', 1,
            event = 'first_workspace_created', 2,
            event = 'first_invite_sent', 3, 0) AS step
  FROM events
  WHERE timestamp >= now() - INTERVAL 7 DAY
    AND event IN ('signup_completed','first_workspace_created','first_invite_sent')
)
WHERE step > 0
GROUP BY step
ORDER BY step;
```

#### Amplitude

```bash
mcp tool amplitude.funnel \
  --events '["signup_completed","first_workspace_created","first_invite_sent"]' \
  --startDate "2026-06-02" \
  --endDate "2026-06-09" \
  --groupBy "plan"
```

#### Mixpanel

```bash
mcp tool mixpanel.funnel \
  --eventNames '["Signup Completed","First Workspace Created","First Invite Sent"]' \
  --fromDate "2026-06-02" --toDate "2026-06-09" \
  --unit day
```

### Recipe 2: Retention curves (D1 / D7 / D30)

#### PostHog

```bash
mcp tool posthog.retention \
  --targetEvent "$any" \
  --returningEvent "$any" \
  --period "Day" \
  --totalIntervals 30
```

#### Amplitude

```bash
mcp tool amplitude.retention \
  --startEvent "signup_completed" \
  --returnEvent "active_session" \
  --measureType "n_day" \
  --intervals '[1,7,14,30]'
```

### Recipe 3: Behavioral cohort

```sql
-- HogQL: "engaged users" = ≥3 active sessions in past 7 days
SELECT person_id
FROM events
WHERE event = 'active_session'
  AND timestamp >= now() - INTERVAL 7 DAY
GROUP BY person_id
HAVING count() >= 3;
```

```bash
# Amplitude — save as a behavioral cohort for future use
mcp tool amplitude.create_cohort \
  --name "Engaged 7d" \
  --definition '{"events":[{"name":"active_session","count":{"min":3,"interval":7,"unit":"day"}}]}'
```

### Recipe 4: North Star metric weekly snapshot

```bash
# Define North Star = "Weekly Engaged Users × Value Created per User"
# Pulling each piece from PostHog HogQL

WEU=$(mcp tool posthog.query --query "
  SELECT count(DISTINCT person_id) AS weu
  FROM events WHERE event='active_session'
    AND timestamp >= now() - INTERVAL 7 DAY
" | jq '.results[0].weu')

VALUE_PER_USER=$(mcp tool posthog.query --query "
  SELECT avg(properties.value_created) AS v
  FROM events WHERE event='value_created'
    AND timestamp >= now() - INTERVAL 7 DAY
" | jq '.results[0].v')

NORTH_STAR=$(echo "$WEU * $VALUE_PER_USER" | bc)
echo "Weekly North Star: $NORTH_STAR"
```

### Recipe 5: Activation rate (% of new users hitting "value moment")

```sql
-- Activation = "first 3 actions within first 7 days"
WITH new_users AS (
  SELECT person_id, min(timestamp) AS signup_at
  FROM events WHERE event='signup_completed'
    AND timestamp >= now() - INTERVAL 30 DAY
  GROUP BY person_id
),
activated AS (
  SELECT n.person_id
  FROM new_users n
  JOIN events e ON e.person_id = n.person_id
  WHERE e.event = 'key_action'
    AND e.timestamp BETWEEN n.signup_at AND n.signup_at + INTERVAL 7 DAY
  GROUP BY n.person_id
  HAVING count() >= 3
)
SELECT
  count(*) AS new_users,
  (SELECT count(*) FROM activated) AS activated,
  (SELECT count(*) FROM activated) * 100.0 / count(*) AS activation_rate
FROM new_users;
```

### Recipe 6: Cohort-on-cohort retention compare

```bash
# Pre/post onboarding-revamp launch (2026-06-09)
mcp tool amplitude.retention \
  --segmentDefinitions '[
    {"name":"pre-launch","filter":{"signup_date":{"before":"2026-06-09"}}},
    {"name":"post-launch","filter":{"signup_date":{"on_or_after":"2026-06-09"}}}
  ]' \
  --measureType "n_day" \
  --intervals '[7]'
```

### Recipe 7: Funnel-drop diagnostics (where do users fall off)

```sql
-- HogQL — order by drop-off %, return the biggest leak
WITH funnel AS (
  SELECT 'signup' AS step, count() AS users FROM events WHERE event='signup_completed' AND timestamp >= now() - INTERVAL 7 DAY
  UNION ALL SELECT 'create_workspace', count() FROM events WHERE event='first_workspace_created' AND timestamp >= now() - INTERVAL 7 DAY
  UNION ALL SELECT 'invite_sent', count() FROM events WHERE event='first_invite_sent' AND timestamp >= now() - INTERVAL 7 DAY
)
SELECT step, users, lagInFrame(users) OVER () - users AS dropped
FROM funnel ORDER BY users DESC;
```

### Recipe 8: Save a HogQL/Amplitude query as a scheduled chart

```bash
# PostHog — save as Insight
mcp tool posthog.create_insight \
  --name "Activation rate (7d)" \
  --query '{"kind":"HogQLQuery","query":"<the Recipe 5 SQL>"}' \
  --dashboard "<exec-dashboard-id>"
```

### Recipe 9: Power-user identification (segmentation)

```sql
-- Top 5% by event count in 30d
SELECT person_id, count() AS events
FROM events
WHERE timestamp >= now() - INTERVAL 30 DAY
GROUP BY person_id
ORDER BY events DESC
LIMIT 100;
```

### Recipe 10: Tracking spec verification (events firing as expected)

```sql
-- Quick health check: did the new event fire in the last 24h?
SELECT
  event,
  count() AS volume,
  min(timestamp) AS first_seen,
  max(timestamp) AS last_seen
FROM events
WHERE timestamp >= now() - INTERVAL 24 HOUR
  AND event IN ('onboarding_started','onboarding_step_completed','onboarding_dismissed')
GROUP BY event;
```

## Examples

### Example 1: "Why is D7 retention dropping?"
**Goal:** Diagnose the retention drop reported by the head of growth.

**Steps:**
1. Pull D7 retention curve for last 8 weeks (Recipe 2).
2. Spot the inflection week.
3. Pull activation-rate trend (Recipe 5) for the same period.
4. If activation drops first → onboarding regression. Use `fullstory-logrocket-session-replay` skill on activation-funnel exits.
5. If activation holds but D7 drops → 2nd-session re-engagement issue. Check `last_session_age` distribution.
6. Write findings into a Notion analysis doc; create Linear issues per actionable insight.

**Result:** Cause-effect chain documented with charts; engineering knows what to fix.

### Example 2: Weekly stakeholder metric snapshot
**Goal:** Auto-generate the metrics block for the Lenny weekly update.

**Steps:**
1. Pull WAU, D7 retention, activation rate, NPS via Recipe 4 + Recipe 5.
2. Compute week-over-week deltas.
3. Format as Markdown table for the `stakeholder-update-format` skill.

**Result:** No manual KPI compilation — the update auto-fills.

## Edge cases / gotchas

- **PostHog vs PostHog Cloud.** Self-host PostHog has identical HogQL surface but query cost is yours; Cloud limits free tier to 1M events/mo.
- **Event volume cost.** Amplitude charges per MTU (monthly tracked user); Mixpanel and PostHog charge per event. High-frequency events (e.g., scroll) burn budget fast.
- **Identity resolution.** Logged-out → logged-in user merging is platform-specific. PostHog uses `identify`; Mixpanel `alias`; Amplitude `userId`. Mismatch creates phantom users.
- **HogQL is ClickHouse SQL with sugar.** Some PostgreSQL functions don't translate. Test in the PostHog query editor first.
- **Funnel step ordering matters.** A user firing step 3 before step 2 will not count in a strict funnel. Configure "allow any order" for non-sequential funnels.
- **Retention period mismatch.** "D7 retention" can mean "returns on day 7" (n-day) or "any day in days 1-7" (rolling). Document which.
- **Time zones.** Default UTC; some platforms allow per-project TZ. KPIs differ by TZ; pick once and stick.
- **Sampling.** Some Amplitude charts auto-sample above N users; check chart settings for "Full Dataset" toggle. Funnels under-report otherwise.
- **Cohort sync lag.** Behavioral cohorts in Amplitude refresh every 1-24h depending on plan; not real-time.
- **PII leakage.** Don't put PII in event properties; use server-side property scrubbing (PostHog `process_person_profile`).

## Sources

- [PostHog Model Context Protocol docs](https://posthog.com/docs/model-context-protocol)
- [PostHog HogQL reference](https://posthog.com/docs/hogql)
- [Amplitude MCP](https://amplitude.com/docs/mcp)
- [Amplitude Chart API](https://developers.amplitude.com/docs/dashboard-rest-api)
- [Mixpanel MCP](https://developer.mixpanel.com/docs/mcp)
- [Mixpanel JQL → segmentation API](https://developer.mixpanel.com/reference)
- [Reforge — Activation metric framework](https://www.reforge.com/blog/activation-metric)
- [North Star metric — Sean Ellis](https://blog.growthhackers.com/the-north-star-metric)
