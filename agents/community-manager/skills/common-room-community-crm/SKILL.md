<!--
Sources: https://www.commonroom.io/ + https://docs.commonroom.io/api/ + https://developers.hubspot.com/docs/api/crm/contacts
-->
# Common Room Community CRM — SKILL

Common Room ingests Slack / Discord / GitHub / Twitter / LinkedIn / Reddit / forum / event signals into a member graph. Identifies champions, surfaces churn risk, alerts on key moments. Pumps signals to HubSpot / Salesforce as custom properties. This skill operates Common Room programmatically + builds the OSS fallback if no Common Room access.

## When to use

- New community CRM deployment — first 90 days.
- Existing Common Room — need to programmatically query champions / at-risk / segments.
- Push community signals into HubSpot/Salesforce for revenue team.
- Slack alert on "champion appearing in competitor community".
- Ambassador candidate identification (Recipe 2 in `ambassador-program-design`).
- Member-of-month nominations sourced from activity data.
- Building OSS alternative if Common Room out of budget.

Trigger phrases: "Common Room", "community CRM", "member graph", "champion identification", "at-risk signal", "HubSpot push", "Salesforce push", "Threado", "Orbit alternative".

## Setup

```bash
# Common Room API
export COMMON_ROOM_TOKEN=$(security find-generic-password -a $USER -s common_room_api -w)
curl -H "Authorization: Bearer $COMMON_ROOM_TOKEN" https://app.commonroom.io/api/v1/members?limit=10

# Webhook listener for outbound signals
mcp tool common-room.create_webhook --url https://webhook.brand.com/cr-signal

# HubSpot push
mcp tool hubspot.contacts_update --email $EMAIL \
  --properties '{"community_score": 92, "is_champion": true}'

# OSS fallback: Postgres warehouse with community_events table
psql -c "CREATE TABLE community_events (id BIGSERIAL, member_id TEXT, platform TEXT, event_type TEXT, payload JSONB, created_at TIMESTAMP DEFAULT NOW());"
```

Auth + env:
- `COMMON_ROOM_TOKEN` — Settings → API. Paid Starter+.
- `HUBSPOT_TOKEN` — Private app: scopes `crm.objects.contacts.read/write`, `crm.schemas.contacts.write`.
- `SALESFORCE_OAUTH_TOKEN` — Salesforce Connected App.
- `SLACK_BOT_TOKEN` — `chat:write` for alerts.

Workspace prerequisites:
- Common Room workspace with all source integrations connected (Slack, Discord, GitHub, etc).
- HubSpot custom properties: `community_score`, `is_champion`, `is_at_risk`, `last_community_activity`.
- Slack channel `#community-signals` for alerts.

## Common recipes

### Recipe 1: List members + segment filter

```bash
# All members
curl -H "Authorization: Bearer $COMMON_ROOM_TOKEN" \
  "https://app.commonroom.io/api/v1/members?limit=100" \
  | jq '.results[] | {id, name, email, score, last_active}'

# Segment-filtered (e.g., Champions)
curl -H "Authorization: Bearer $COMMON_ROOM_TOKEN" \
  "https://app.commonroom.io/api/v1/segments" | jq '.[] | {id, name, member_count}'

SEGMENT_ID=$(...)
curl -H "Authorization: Bearer $COMMON_ROOM_TOKEN" \
  "https://app.commonroom.io/api/v1/segments/$SEGMENT_ID/members?limit=100"
```

### Recipe 2: Activity feed for a member

```bash
MEMBER_ID=$(...)
curl -H "Authorization: Bearer $COMMON_ROOM_TOKEN" \
  "https://app.commonroom.io/api/v1/members/$MEMBER_ID/activities?limit=50" \
  | jq '.results[] | {source, type, content, occurred_at, sentiment}'
```

### Recipe 3: Champion identification + Slack alert

```python
champs = curl_cr("/api/v1/segments/champions/members")
for c in champs.recent_changes(since=last_run):
    slack.post(
      channel="#community-signals",
      text=f":star2: New champion: *{c.name}* (score {c.score}). Last activity: {c.last_activity_summary}."
    )
```

### Recipe 4: At-risk signal (engagement decay)

```bash
# Members who scored 80+ but dropped to <40 in last 30 days
curl -H "Authorization: Bearer $COMMON_ROOM_TOKEN" \
  "https://app.commonroom.io/api/v1/segments/at-risk-champions/members" \
  | jq '.results[]'
```

Slack alert template:
```
:warning: Champion at risk: *Jane Doe*
- Score: 92 → 35 (last 30d)
- Last post: 28d ago in #help
- Recent activity in competitor.community? : NO
Owner: @founder — DM?
```

### Recipe 5: HubSpot push (custom properties)

```bash
# For each member, sync score + flags
curl -H "Authorization: Bearer $COMMON_ROOM_TOKEN" \
  "https://app.commonroom.io/api/v1/members" | jq -c '.results[]' | \
  while read m; do
    EMAIL=$(echo "$m" | jq -r .email)
    SCORE=$(echo "$m" | jq -r .score)
    IS_CHAMP=$(echo "$m" | jq -r '.tags | contains(["champion"])')

    curl -X PATCH -H "Authorization: Bearer $HUBSPOT_TOKEN" \
      "https://api.hubapi.com/crm/v3/objects/contacts/$EMAIL?idProperty=email" \
      -d "{\"properties\":{\"community_score\":$SCORE,\"is_champion\":$IS_CHAMP}}"
  done
```

### Recipe 6: Webhook to HubSpot on milestone

```bash
# Common Room webhook config (UI: Settings → Webhooks)
# Event: member.tagged
# URL: https://webhook.brand.com/cr-tagged

# Handler (Cloudflare Worker / Lambda)
on_request(body) {
  if (body.tag === 'champion') {
    fetch('https://api.hubapi.com/crm/v3/objects/contacts/' + body.member.email + '?idProperty=email', {
      method: 'PATCH',
      headers: {...},
      body: JSON.stringify({properties: {is_champion: true, became_champion_at: new Date()}})
    })
  }
}
```

### Recipe 7: OSS fallback — Postgres scoring

```sql
-- Build a Common Room-style score in Postgres
CREATE OR REPLACE VIEW v_member_score AS
WITH activity AS (
  SELECT
    member_id,
    COUNT(*) FILTER (WHERE platform='discord' AND created_at > NOW() - INTERVAL '30 days') AS d_posts,
    COUNT(*) FILTER (WHERE platform='github' AND event_type='comment') AS gh_comm,
    COUNT(*) FILTER (WHERE event_type='helpful_answer') AS help,
    COUNT(DISTINCT platform) AS breadth,
    MAX(created_at) AS last_active
  FROM community_events
  GROUP BY member_id
)
SELECT
  member_id,
  LEAST(100, (d_posts * 2 + gh_comm * 3 + help * 5 + breadth * 10))::INT AS score,
  last_active,
  CASE
    WHEN LEAST(100, (d_posts*2 + gh_comm*3 + help*5 + breadth*10)) >= 80 THEN 'champion'
    WHEN LEAST(100, (d_posts*2 + gh_comm*3 + help*5 + breadth*10)) >= 50 THEN 'contributor'
    WHEN LEAST(100, (d_posts*2 + gh_comm*3 + help*5 + breadth*10)) >= 20 THEN 'member'
    ELSE 'lurker'
  END AS tier
FROM activity;
```

### Recipe 8: Cross-community signal scan

```bash
# Has any of our champions appeared in competitor's Discord / Discourse / subreddit?
COMPETITORS=("r/competitor" "https://forum.competitor.com")

for champ in $(curl -H "..." "$CR/segments/champions/members" | jq -r '.results[].name'); do
  for comp in "${COMPETITORS[@]}"; do
    mcp tool brave-search.web_search --query "$champ site:$comp" --count 3
  done
done
```

Alert if hit found: "Champion Jane Doe posted in competitor.community/help."

### Recipe 9: Member-of-month nomination feed

```python
top_5 = run_sql("""
  SELECT m.name, m.email, vms.score, vms.tier, last_active
  FROM v_member_score vms
  JOIN community_members m USING (member_id)
  WHERE vms.last_active > NOW() - INTERVAL '30 days'
    AND m.is_employee = false
  ORDER BY vms.score DESC LIMIT 5
""")

slack.post(channel="#mod-team", text=f"Member-of-month nominees: {top_5}")
```

### Recipe 10: Weekly community-CRM digest

```python
metrics = {
  'total_members': cr_query('/segments/all/count'),
  'active_30d': cr_query('/segments/active-30d/count'),
  'new_champions': cr_query('/segments/new-champions-7d/count'),
  'at_risk': cr_query('/segments/at-risk-30d/count'),
}

email_body = f"""
# Community CRM weekly digest

- Total members: {metrics['total_members']}
- Active (30d): {metrics['active_30d']}
- New champions this week: {metrics['new_champions']}
- At-risk champions: {metrics['at_risk']}

Top 3 newly-active power users this week: ...
Top 3 at-risk to outreach: ...
"""

gmail.send(to="cmo@brand.com", subject=f"Community CRM · {date.today()}", body=email_body)
```

## Examples

### Example 1: SaaS — daily HubSpot sync

**Goal:** Sales team sees `community_score` on every contact.

**Steps:**
1. Common Room workspace with Slack + Discord + GitHub integrations live.
2. Cron daily 02:00 — Recipe 5 sync.
3. HubSpot custom property `community_score` (0-100) + `is_champion` boolean.
4. Sales playbook: if `community_score > 80` and a deal opens — assign to top-tier AE.

**Result:** Champion deals close 2.1x faster; community team gets quarterly attribution credit.

### Example 2: OSS dev community — no Common Room budget

**Goal:** 5k member Discord/GitHub community without $X/mo budget.

**Steps:**
1. Build community_events Postgres table (Recipe 7).
2. Ingest Discord + GitHub events via webhooks + APIs.
3. Daily Recipe 7 view refresh.
4. Recipe 9 + Recipe 10 digest email to founder.
5. Recipe 5 push to HubSpot custom property.

**Result:** 80% of Common Room value at $0/mo Common Room cost; brittle on multi-platform but works.

## Edge cases / gotchas

- **Identity stitching is messy** — same human is `jane@x.com` in HubSpot, `janedoe` in Discord, `j-doe` on GitHub. Common Room handles this well; OSS fallback needs member-supplied connection.
- **Rate limit** — Common Room API has 100 req/min default; batch + retry with backoff.
- **Score volatility** — scores can swing 20+ in a week. Use 30-day rolling avg for actions like "promote to champion".
- **Champion ≠ NPS promoter** — Common Room scoring is activity-based; NPS is sentiment. Track both.
- **At-risk false positives** — vacation = no activity. Cross-check with calendar (HubSpot vacation field or company directory).
- **HubSpot rate limit** — 100 req/10s on Pro; bulk operations endpoint preferred.
- **Webhook idempotency** — Common Room may resend; dedupe by event_id.
- **Cross-community signal** — surfacing "champion in competitor" must be private alert, not Slack-wide.
- **Common Room paywall** — Starter $X/mo; OSS Postgres alternative loses cross-platform identity + sentiment ML.
- **Salesforce custom field limits** — narrow contact field schema; use account-level fields for high-cardinality data.
- **GDPR right to delete** — Common Room respects deletion; ensure OSS Postgres also handles `DELETE FROM community_events WHERE member_id = ?`.
- **Tag taxonomy drift** — keep tags doc canonical; rename in UI breaks API consumers.

## Sources

- [Common Room](https://www.commonroom.io/)
- [Common Room API docs](https://docs.commonroom.io/api/)
- [HubSpot Contacts API](https://developers.hubspot.com/docs/api/crm/contacts)
- [HubSpot custom properties](https://developers.hubspot.com/docs/api/crm/properties)
- [Threado](https://threado.com/)
- [Salesforce REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/)
- [Orbit Model (legacy ref)](https://orbit.love/blog/the-orbit-model/)
