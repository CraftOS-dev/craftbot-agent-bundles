<!--
Source: https://app.delighted.com/docs/api + https://docs.sprig.com/ + https://developers.survicate.com/ + https://www.inmoment.com/
-->
# NPS + CSAT + CES Tracking — SKILL

Survey operations: send NPS (quarterly), CSAT (post-support-close), CES (post-resolution), event-triggered in-product micro-surveys (Sprig). Delighted as one-stop SOTA; Survicate for multi-channel; Sprig for moment-specific. Auto-route detractors to CSM within 1h; auto-trigger advocacy flow on promoters. Cooldown enforcement.

## When to use

- **Quarterly NPS push** — 90d cooldown; sample all eligible customers.
- **Post-onboarding NPS** — Day 90 milestone hit; one-time send.
- **Post-support-close CSAT** — 1h after ticket close.
- **Post-resolution CES** — 24h after resolution.
- **In-product moment survey** — fired on event (e.g., first export).
- **Detractor follow-up** — score <= 6, route to CSM within 1h.
- **Promoter advocacy** — score >= 9, route to `customer-advocacy-case-study-reference`.

This skill is the **survey delivery + response routing** layer. The synthesis of survey responses into themes belongs to `voice-of-customer-reporting`.

Trigger phrases: "NPS", "CSAT", "CES", "Delighted", "Survicate", "Sprig", "detractor", "promoter", "survey", "feedback survey".

## Setup

```bash
# Delighted (SOTA one-stop)
export DELIGHTED_API_KEY="<key>"

# Survicate (multi-channel)
export SURVICATE_API_KEY="<key>"

# Sprig (in-product event-triggered)
export SPRIG_API_KEY="<key>"

# Wootric (InMoment) - incumbent fallback
export WOOTRIC_API_KEY="<key>"
```

Workspace prerequisites:
- Delighted "People" list synced with customer base nightly via reverse-ETL.
- Postgres tables: `survey_responses` (unified across vendors).
- Slack channel `#cs-detractors` for detractor escalation.
- Notion "Survey Operations" tracker: per-customer last_nps_sent_at, last_csat_sent_at, last_ces_sent_at.

## Cadence

| Survey | Trigger | Cooldown | Channel | Vendor |
|---|---|---|---|---|
| NPS | Quarterly | 90d minimum | Email | Delighted |
| NPS post-onboarding | Day 90 milestone | 90d | Email or in-app | Delighted / Sprig |
| CSAT | 1h post-ticket-close | 14d | Email | Delighted |
| CES | 24h post-resolution | 14d | Email | Delighted |
| In-product micro | Key event (e.g. first export) | 30d | In-app | Sprig |

## Common recipes

### Recipe 1: Enqueue NPS via Delighted

```bash
curl -sS -X POST "https://api.delighted.com/v1/people" \
  -u "$DELIGHTED_API_KEY:" \
  -d "email=$USER_EMAIL" \
  -d "name=$USER_NAME" \
  -d "send=true" \
  -d "survey_type=nps" \
  -d "delay=0" \
  -d "properties[customer_id]=$CUSTOMER_ID" \
  -d "properties[tier]=$TIER"
```

Doc: https://app.delighted.com/docs/api

### Recipe 2: Enqueue CSAT post-ticket-close

```bash
# After ticket close webhook fires:
curl -sS -X POST "https://api.delighted.com/v1/people" \
  -u "$DELIGHTED_API_KEY:" \
  -d "email=$USER_EMAIL" \
  -d "survey_type=csat" \
  -d "send=true" \
  -d "delay=3600" \
  -d "properties[ticket_id]=$TICKET_ID" \
  -d "properties[agent_id]=$AGENT_ID"
```

`delay=3600` = 1h delay so user has time to process resolution.

### Recipe 3: Enqueue CES

```bash
curl -sS -X POST "https://api.delighted.com/v1/people" \
  -u "$DELIGHTED_API_KEY:" \
  -d "email=$USER_EMAIL" \
  -d "survey_type=ces" \
  -d "send=true" \
  -d "delay=86400"
```

`delay=86400` = 24h.

### Recipe 4: Fire Sprig micro-survey on event

```bash
curl -sS -X POST "https://api.sprig.com/v1/surveys/$SURVEY_ID/responses/enqueue" \
  -H "Authorization: Bearer $SPRIG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "'$USER_ID'",
    "delay_minutes": 5,
    "context": {"event": "first_export_completed", "customer_id": "'$CUSTOMER_ID'"}
  }'
```

Doc: https://docs.sprig.com/

### Recipe 5: Survicate multi-channel

```bash
# Survey via Survicate API (email channel)
curl -sS -X POST "https://api.survicate.com/v1/surveys/$SURVEY_ID/respondents" \
  -H "Authorization: Bearer $SURVICATE_API_KEY" \
  -d '{
    "email": "'$USER_EMAIL'",
    "channel": "email",
    "metadata": {"customer_id": "'$CUSTOMER_ID'"}
  }'
```

Doc: https://developers.survicate.com/

### Recipe 6: Cooldown enforcement

```sql
SELECT email, customer_id
FROM customers
WHERE email NOT IN (
  SELECT email FROM survey_send_log
  WHERE survey_type = 'nps'
    AND sent_at >= now() - INTERVAL '90 days'
)
AND tenure_months >= 1
LIMIT 500;  -- batch size
```

Pass result to Recipe 1; ensures 90d cooldown.

### Recipe 7: Pull responses from Delighted

```bash
# Last 7 days, paginated
PAGE=1
while true; do
  RESP=$(curl -sS "https://api.delighted.com/v1/responses?page=$PAGE&per_page=100&since=$(date -u -d '7 days ago' +%s)&expand=person" \
    -u "$DELIGHTED_API_KEY:")
  echo "$RESP" | jq -c '.[]' >> responses.jsonl
  COUNT=$(echo "$RESP" | jq 'length')
  [ "$COUNT" -lt 100 ] && break
  PAGE=$((PAGE+1))
done
psql -c "\\COPY survey_responses FROM 'responses.jsonl' WITH (FORMAT json)"
```

### Recipe 8: Detractor auto-route to CSM

```sql
-- Nightly: route detractors to CSMs
SELECT r.email, r.score, r.comment, c.csm_owner, c.tier, c.name
FROM survey_responses r
JOIN customers c ON c.email = r.email
WHERE r.score <= 6
  AND r.received_at >= now() - INTERVAL '24 hours'
  AND r.survey_type IN ('nps', 'csat')
  AND r.routed_at IS NULL;
```

For each row:

```python
slack.chat_postMessage(
    channel="#cs-detractors",
    text=f"""
:bangbang: Detractor signal: {row.name}
Score: {row.score}/10 ({row.survey_type})
Comment: "{row.comment}"
CSM: {row.csm_owner}
Action: reach out within 48h. Reply :white_check_mark: when contacted.
"""
)
# Mark routed_at
postgres.execute("UPDATE survey_responses SET routed_at = now() WHERE id = %s", row.id)
```

### Recipe 9: Promoter auto-trigger advocacy

```sql
SELECT email, score, comment
FROM survey_responses
WHERE score >= 9
  AND received_at >= now() - INTERVAL '24 hours'
  AND survey_type = 'nps'
  AND advocacy_invited = FALSE;
```

For each row -> invoke `customer-advocacy-case-study-reference` Recipe 3 (advocacy invite).

### Recipe 10: Build NPS dashboard data

```sql
-- 90d rolling NPS
SELECT
  date_trunc('week', received_at) AS week,
  count(*) AS responses,
  count(*) FILTER (WHERE score >= 9) AS promoters,
  count(*) FILTER (WHERE score BETWEEN 7 AND 8) AS passives,
  count(*) FILTER (WHERE score <= 6) AS detractors,
  100.0 * (count(*) FILTER (WHERE score >= 9) - count(*) FILTER (WHERE score <= 6)) / count(*)::numeric AS nps
FROM survey_responses
WHERE survey_type = 'nps'
  AND received_at >= now() - INTERVAL '90 days'
GROUP BY week
ORDER BY week;
```

### Recipe 11: Per-CSM book NPS / CSAT

```sql
SELECT
  c.csm_owner,
  count(*) AS responses,
  round(avg(r.score)::numeric, 2) AS avg_score,
  100.0 * count(*) FILTER (WHERE r.score >= 9) / count(*)::numeric AS promoter_pct
FROM survey_responses r
JOIN customers c USING (customer_id)
WHERE r.received_at >= now() - INTERVAL '90 days'
  AND r.survey_type = 'nps'
GROUP BY c.csm_owner
ORDER BY avg_score DESC;
```

### Recipe 12: Update Vitally trait `nps_latest`

```bash
curl -sS -X PUT "https://$VITALLY_SUBDOMAIN.rest.vitally.io/resources/accounts/external/$CUSTOMER_ID/traits" \
  -H "Authorization: Basic $(echo -n $VITALLY_API_KEY: | base64)" \
  -d '{"nps_latest": '$SCORE', "nps_latest_received_at": "'$DATE'"}'
```

Feeds composite health score (Recipe 1 in `customer-health-scoring-vitally-catalyst-churnzero`).

### Recipe 13: Quarterly NPS batch send (the "big one")

```bash
# Step 1: Recipe 6 - eligible customers
# Step 2: Batch Recipe 1 across 500 emails per batch
# Step 3: Rate limit ~1 per second to respect Delighted limit

while read email; do
  Recipe 1 with $email
  sleep 1
done < eligible.csv
```

For very large lists, use Delighted's bulk endpoint via SFTP CSV upload.

## Examples

### Example 1: Quarterly NPS rollout

**Goal:** First Monday of new quarter, send NPS to ~3000 eligible customers.

**Steps:**
1. Sunday 23:00 UTC: Recipe 6 cooldown eligibility.
2. Monday 08:00 UTC: Recipe 13 batch send.
3. Tuesday: First responses start streaming in.
4. Tuesday onward: Recipe 7 pull responses; Recipe 8 detractor route; Recipe 9 promoter advocacy; Recipe 10 dashboard.
5. End of week: Recipe 11 per-CSM rollup; share with team.

**Result:** Quarterly NPS pulse complete; detractors hit within 48h.

### Example 2: Sprig event-triggered micro-survey

**Goal:** When customer fires first `export_completed`, ask "How useful was this export?"

**Steps:**
1. Configure Sprig survey "First Export Feedback" - 1 question, 1-5 scale + free text.
2. Backend instrumentation: on `export_completed` event, call Recipe 4 with user_id.
3. Sprig fires in-product 5 min later.
4. Responses pulled nightly via Sprig API into `survey_responses`.
5. < 4 score routes to CSM (modified Recipe 8 for Sprig).

**Result:** Moment-specific feedback captured at point of value.

## Edge cases / gotchas

- **Survey fatigue** — same customer hit with NPS + CSAT + CES same week = bad UX. Coordinate via Notion send log (Recipe 6 extended for all survey types).
- **GDPR consent** — EU customers may not have opted in. Filter by consent flag before send.
- **Email deliverability** — Delighted's IP reputation matters; gmail-mcp send is alt for personal touches. For volume, Delighted handles deliverability.
- **Comment-less detractor** — score 4 with no comment = uninterpretable. Still route to CSM but with "no comment" flag.
- **CSAT scale variation** — 1-5 vs 1-7; standardize internally (1-5 SOTA).
- **NPS calculation pedantry** — 0-10 scale; 9-10 promoters, 7-8 passives, 0-6 detractors. Don't shift the bands.
- **CES question format** — "How easy was X?" 1-7 scale; standardize question per survey-type.
- **Multi-recipient per customer** — large enterprise = 100 users; do you sample, send-all, or pick champion? Default: champion + top 5 users by activity.
- **Survey to churned customer** — recently-churned customer shouldn't get NPS. Filter by `churned_at IS NULL`.
- **Vitally trait push race** — Recipe 12 fires alongside health-score writeback; throttle to avoid overwriting.
- **Promoter advocacy loop with cooldown** — `customer-advocacy-case-study-reference` has 6mo cooldown; Recipe 9 must check.
- **Sprig sample size for in-product** — low-volume events = low sample = unreliable. Aggregate per surface, not per event.

## Sources

- [Delighted API reference](https://app.delighted.com/docs/api)
- [Delighted People API](https://app.delighted.com/docs/api/people)
- [Delighted Responses API](https://app.delighted.com/docs/api/responses)
- [Sprig API docs](https://docs.sprig.com/)
- [Sprig Survey Enqueue API](https://docs.sprig.com/reference/api-overview)
- [Survicate developer docs](https://developers.survicate.com/)
- [Wootric (InMoment)](https://www.inmoment.com/)
- [NPS calculation methodology](https://www.netpromoter.com/know/)
- [CSAT vs CES (CustomerGauge)](https://customergauge.com/blog/csat-vs-nps-vs-ces)
- [Hotjar surveys docs](https://help.hotjar.com/hc/en-us/categories/115000482147-Surveys-NPS-Polls)
