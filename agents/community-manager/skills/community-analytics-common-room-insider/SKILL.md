<!--
Sources: https://www.commonroom.io/product/intelligence/ + https://www.notable.so/ + https://threado.com/ + https://posthog.com/docs + https://www.metabase.com/ + https://docs.commonroom.io/api/
-->
# Community Analytics (Common Room / Insider Notable / Threado / custom PostHog) — SKILL

Community analytics stack picks: Common Room (mid-market+, paid) for full member-graph + sentiment + signal feed; Insider's Notable (SMB, launched 2025) for lightweight SaaS-side; Threado for Slack/Discord-only SMBs; custom PostHog + warehouse + Metabase / Looker for engineering-led communities. Output: weekly community-metrics digest (active members, posting frequency, sentiment, top topics, champion activity, journey-stage migrations).

## When to use

- New analytics stack — choose tool based on team size, budget, existing data infra.
- Existing community lacking weekly metrics digest.
- Switching from Orbit (deprecated) to current SOTA.
- Engineering-led community wanting custom PostHog + warehouse instead of paid SaaS.
- Quarterly community business review requiring active-member trends + ROI inputs.
- Channel-level engagement decomposition (which channel drives most repeat-posters).
- Champion / at-risk dashboards for ambassador program (cross-link to `ambassador-program-design`).

Trigger phrases: "community analytics", "community dashboard", "Common Room", "Notable", "Threado", "PostHog community", "weekly community digest", "active member metric", "Orbit alternative", "community KPI".

## Setup

```bash
# Common Room (paid, mid-market+)
export COMMON_ROOM_TOKEN=$(security find-generic-password -a $USER -s common_room_api -w)
curl -H "Authorization: Bearer $COMMON_ROOM_TOKEN" \
  https://app.commonroom.io/api/v1/community

# Notable (Insider) — SMB, paid
export NOTABLE_TOKEN=$(op item get notable-api --fields token)
curl -H "Authorization: Bearer $NOTABLE_TOKEN" https://api.notable.so/v1/me

# Threado (SMB, paid, mid-market)
curl -H "x-api-key: $THREADO_KEY" https://api.threado.com/v1/members

# Custom PostHog + warehouse + Metabase (free-ish, engineering-led)
mcp tool posthog-mcp.capture --event "community.message_posted" \
  --properties '{"channel":"general","member_id":"M-123","platform":"discord"}'
mcp tool postgresql-mcp.execute --query "
  SELECT date_trunc('week', ts) wk, count(distinct member_id) wau
  FROM community_events WHERE event = 'message_posted' AND ts > now() - interval '12 weeks'
  GROUP BY 1 ORDER BY 1;"
```

Auth + env:
- `COMMON_ROOM_TOKEN` — Settings → API. Starter tier ($800/mo+).
- `NOTABLE_TOKEN` — Notable workspace → Developer. $99/mo team plan.
- `THREADO_KEY` — Threado workspace → API.
- `POSTHOG_PROJECT_API_KEY` — PostHog → Project settings → API key.
- `METABASE_URL` + `METABASE_TOKEN` — for dashboard automation.

Workspace prerequisites:
- Source integrations connected per tool (Slack, Discord, GitHub, etc).
- Member-id → CRM-id mapping table (email or hash join key).
- Warehouse: postgres with `community_events`, `members`, `channels` tables.
- Slack channel `#community-metrics` for weekly digest delivery.

## Common recipes

### Recipe 1: Tool selection matrix

| Org size | Budget | Stack | Why |
|---|---|---|---|
| 1-10 employees | $0 | Custom: PostHog free + postgres + Metabase OSS | Engineering effort but $0 |
| 10-50 employees | $99-300/mo | Notable or Threado | SaaS lift, no custom code |
| 50-500 employees | $800-3k/mo | Common Room Starter or Pro | Mid-market SOTA |
| 500+ employees | $3k+/mo | Common Room Enterprise + warehouse | Multi-team CRM push |
| Engineering-led | $0-200/mo | PostHog + warehouse + Metabase | Full control |

Default to Common Room if budget allows; PostHog + warehouse for engineering control.

### Recipe 2: Common Room weekly digest pull

```python
# Weekly snapshot via Common Room API
import requests, datetime

since = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).isoformat()
headers = {"Authorization": f"Bearer {COMMON_ROOM_TOKEN}"}

active_members = requests.get(
    f"https://app.commonroom.io/api/v1/activities?since={since}",
    headers=headers
).json()
distinct_active = len({a["member_id"] for a in active_members["items"]})

champions = requests.get(
    "https://app.commonroom.io/api/v1/segments/champions/members",
    headers=headers
).json()

at_risk = requests.get(
    "https://app.commonroom.io/api/v1/segments/at-risk/members",
    headers=headers
).json()

# Post to Slack
slack.chat_postMessage(channel="#community-metrics", text=f"""
*Week ending {datetime.date.today()}*
- Active members: {distinct_active}
- Champions: {len(champions['items'])}
- At-risk: {len(at_risk['items'])}
- Top topic: {top_topic_via_query()}
""")
```

### Recipe 3: Custom PostHog event schema for community

```python
# Standard event taxonomy — emit to PostHog from every platform integration
events = [
    "community.member_joined",
    "community.message_posted",     # generic post
    "community.message_replied",
    "community.reaction_added",
    "community.dm_sent",
    "community.role_assigned",
    "community.event_attended",
    "community.first_post",         # activation milestone
    "community.ambassador_promoted",
    "community.tier_changed",
    "community.churned",            # 30d inactive
]

# Properties always set
properties = {
    "member_id": "M-...",
    "platform": "discord|slack|circle|discourse",
    "channel": "...",
    "tenure_days": 42,
    "is_employee": False,
    "ambassador_tier": "contributor|ambassador|champion",
}
```

Emit from Discord via `discord-mcp-full` webhook → posthog-mcp `capture`. Same pattern for Slack via slack-mcp event subscriptions.

### Recipe 4: HogQL weekly dashboard query

```sql
-- Weekly active community members
SELECT
  toStartOfWeek(timestamp) AS wk,
  uniq(properties.member_id) AS wac,
  uniqIf(properties.member_id, event = 'community.first_post') AS new_activated,
  countIf(event = 'community.message_posted') AS messages
FROM events
WHERE event LIKE 'community.%'
  AND timestamp > now() - INTERVAL 12 WEEK
  AND properties.is_employee = false
GROUP BY wk
ORDER BY wk;
```

Run via `posthog-mcp.query` HogQL endpoint; surface result in `#community-metrics`.

### Recipe 5: 90-day cohort retention curve

```sql
SELECT
  toStartOfMonth(joined_at) AS cohort,
  (active_month - cohort) / interval '30 days' AS week_offset,
  count(distinct member_id) AS retained
FROM (
  SELECT
    properties.member_id AS member_id,
    minMerge(properties.first_seen_at) AS joined_at,
    toStartOfWeek(timestamp) AS active_month
  FROM events
  WHERE event = 'community.message_posted'
  GROUP BY member_id, active_month
) cohort_long
GROUP BY cohort, week_offset
ORDER BY cohort, week_offset;
```

Surface as Metabase pivot. The retention shape tells you whether your activation flow works.

### Recipe 6: Notable (Insider) weekly digest

```bash
# Notable dashboard automatically generates weekly summary
curl -H "Authorization: Bearer $NOTABLE_TOKEN" \
  https://api.notable.so/v1/insights/weekly \
  | jq '{
    week: .week,
    growth: .growth.delta_pct,
    top_members: [.top_members[:5][] | .name],
    top_threads: [.top_threads[:3][] | .url]
  }'
```

Post to Slack via slack-mcp.chat_postMessage.

### Recipe 7: Threado champion query

```bash
curl -H "x-api-key: $THREADO_KEY" \
  "https://api.threado.com/v1/members?segment=champions&active_since=$(date -d '7 days ago' -I)" \
  | jq '.members[] | {name, score, recent_activity}'
```

Threado's "Members at risk" segment is the dual query.

### Recipe 8: Metabase dashboard auto-creation

```python
# Programmatically create dashboard from template
import requests
metabase = "https://metabase.brand.com"
session = requests.post(
    f"{metabase}/api/session",
    json={"username": MB_USER, "password": MB_PASSWORD}
).json()["id"]

dashboard = requests.post(
    f"{metabase}/api/dashboard",
    headers={"X-Metabase-Session": session},
    json={"name": "Community Health — Weekly", "collection_id": 5}
).json()

cards = [
    {"name": "Weekly Active Community", "sql": WAC_SQL},
    {"name": "New Members Activated 7d", "sql": ACTIVATION_SQL},
    {"name": "Top Channels by Posts", "sql": CHANNELS_SQL},
    {"name": "Sentiment Trend", "sql": SENTIMENT_SQL},
]
for c in cards:
    requests.post(
        f"{metabase}/api/card",
        headers={"X-Metabase-Session": session},
        json={"name": c["name"], "dataset_query": {"type":"native","native":{"query":c["sql"]},"database":1}}
    )
```

### Recipe 9: Weekly digest template (Markdown for Notion or Slack canvas)

```markdown
# Community Health — Week of {{week_start}}

## Headline numbers
- Weekly active community (WAC): {{wac}} ({{wac_delta_pct}}% WoW)
- New members: {{new_members}}
- 7-day activation rate: {{activation_rate}}%
- Champions: {{champions_count}} (Δ {{champ_delta}})
- At-risk: {{at_risk_count}}

## Top moments
{{#top_moments}}
- {{title}} — {{member}} in #{{channel}} → {{reaction_count}} reactions
{{/top_moments}}

## Sentiment
{{sentiment_chart_url}}
- Positive: {{pos_pct}}% (WoW {{pos_delta}})
- Negative: {{neg_pct}}%

## Top topics this week
{{#topics}}
- {{topic}} ({{count}} mentions)
{{/topics}}

## What needs attention
{{#concerns}}
- {{summary}} — {{recommended_action}}
{{/concerns}}

## Wins
{{#wins}}
- {{description}}
{{/wins}}
```

Render via Jinja2/Mustache; post to `#community-metrics` Slack canvas + Notion DB row.

### Recipe 10: Common Room → HubSpot dual-write

```python
# Pump community_score, is_champion, last_community_activity into HubSpot custom properties
for member in common_room_members():
    if not member.get("email"):
        continue
    hubspot.contacts_update(
        email=member["email"],
        properties={
            "community_score": member["affinity_score"],
            "is_champion": member["segments"].get("champion", False),
            "is_at_risk": member["segments"].get("at-risk", False),
            "last_community_activity": member["last_activity_at"],
            "community_tier": classify_tier(member["affinity_score"]),
        },
    )
```

Cross-link to `common-room-community-crm` Recipe 4.

## Examples

### Example 1: SMB SaaS launching community (Notable)

**Goal:** Sales-led SaaS company with 25 employees launches Slack community, needs weekly metrics.

**Steps:**
1. Tool choice: Notable ($99/mo, SMB-grade).
2. Connect Slack + Discord integrations.
3. Define "active" = posted in last 7 days.
4. Set up auto-digest delivery to `#leadership` channel via Notable native Slack integration.
5. Set up at-risk alert: member with score >70 falls below 30 → DM to community manager.

**Result:** Weekly metrics flow without engineering work. Cost = $99/mo. Limitation: no custom segments.

### Example 2: Engineering-led OSS community (custom PostHog)

**Goal:** Open-source project with Discord + Discourse + GitHub. Wants full control + $0 SaaS spend.

**Steps:**
1. Stand up PostHog OSS (self-hosted Docker).
2. Webhook from Discord → posthog-mcp `capture` (Recipe 3 schema).
3. Discourse webhook → same.
4. GitHub Actions on PR-merged-by-non-employee → same.
5. Metabase OSS connects to PostHog Postgres mirror.
6. Weekly digest auto-runs (Recipe 8) → posts to Discord `#metrics` channel.

**Result:** $0/mo external. Engineering cost: 1 engineer × 2 weeks. Total ownership.

### Example 3: Mid-market B2B (Common Room + warehouse)

**Goal:** B2B SaaS with 300 employees, Slack + Discord + Discourse community, sales-led.

**Steps:**
1. Common Room Starter ($800/mo).
2. Connect all integrations including HubSpot bi-directional.
3. Build champion / at-risk segments in Common Room UI.
4. Pump custom properties to HubSpot via Common Room native push (Recipe 10).
5. Weekly digest (Recipe 2) → `#community-metrics`.
6. Sales weekly review uses Common Room + HubSpot dashboard.

**Result:** Sales sees community signals on contact records. Avg deal size for "champion" contacts +35% vs baseline.

### Example 4: Migration from Orbit (deprecated)

**Goal:** Existing community on Orbit (acquired, deprecated) needs migration.

**Steps:**
1. Export Orbit members + activity CSV via Settings → Export.
2. Map fields: orbit_member_id → notable_member_id (or common_room_id).
3. Bulk import to new tool via API or CSV.
4. Re-establish source integrations (Slack/Discord/etc).
5. Validate: WAC numbers should match within ±5%.
6. Sunset Orbit instance.

**Result:** 2-week migration; ~5% loss in historical signal granularity (different activity schema).

## Edge cases / gotchas

- **Common Room paid tier required for API** — free trial has no API access. Budget Starter+ for programmatic.
- **Notable lacks custom segments** — segments are hard-coded. If you need bespoke tiering, use Common Room or custom.
- **Threado Slack/Discord-focused only** — does not ingest Discourse, forums, or GitHub. Use Common Room if multi-platform.
- **PostHog free tier event cap** — 1M events/mo. Bursty community traffic can blow past. Plan budget.
- **Self-host PostHog OS** complexity — non-trivial: Postgres + Kafka + ClickHouse. Cloud is simpler unless engineering-rich.
- **Dedupe member identity** — same person on Discord + Slack + GitHub = 3 different ids. Use email as join key when possible; hash key for privacy.
- **Survivorship bias in champion segment** — champions only have data because they engaged. Track funnel from join too, not just top-of-pyramid.
- **PostHog sampling** — default 100% but enterprise can sample down. Verify before trusting WAC numbers.
- **Sentiment in Common Room is a separate add-on** — not bundled in Starter. Brand24 + Claude fallback in `sentiment-monitoring-in-community`.
- **Common Room webhook quotas** — 1000 events/min on Starter. Burst over = lag. Pro/Enterprise scale up.
- **Privacy + GDPR** — community-activity data is personal data. SCC + DPA needed for EU members. Common Room is DPA-compliant.
- **Cohort retention skews early-cohort** — older cohorts have more time to churn. Always compare same-week-old cohorts.
- **Bot activity pollution** — bots posting to community channels inflate message counts. Tag bot users + exclude.
- **Employee vs external** — separate metrics for employee participation vs external. Otherwise WAC inflates artificially in eng-led.
- **Common Room URL change 2025** — migrated from `commonroom.io` to `app.commonroom.io` — update old runbooks.

## Sources

- [Common Room product intelligence](https://www.commonroom.io/product/intelligence/)
- [Common Room API](https://docs.commonroom.io/api/)
- [Common Room weekly digest blog](https://www.commonroom.io/blog/community-weekly-digest/)
- [Notable (Insider)](https://www.notable.so/)
- [Threado](https://threado.com/)
- [PostHog docs](https://posthog.com/docs)
- [PostHog community use case](https://posthog.com/tutorials/community-analytics)
- [Metabase dashboard API](https://www.metabase.com/docs/latest/api/dashboard)
- [Orbit Model retrospective (legacy)](https://orbit.love/blog/the-orbit-model/)
