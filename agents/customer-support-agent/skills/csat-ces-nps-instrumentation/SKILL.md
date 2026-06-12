<!--
Source: https://app.delighted.com/docs/api + Survicate + alternatives
NOTE (2026-06): Delighted (Qualtrics) is sunsetting June 30 2026.
-->
# CSAT / CES / NPS Instrumentation — SKILL

Post-ticket / quarterly survey delivery and response capture. Delighted (Qualtrics) was the historical SOTA; **Delighted is sunsetting June 30, 2026** so this skill leads with Survicate + Refiner as the primary path, with Wootric (InMoment) and Typeform as alternates. Detractor auto-routing to CSM is the highest-leverage workflow.

## When to use

- **Post-ticket-close CSAT** — send within 1h of closure.
- **Post-resolution CES** — "How easy was it to get this resolved?" within 24h.
- **Quarterly / milestone NPS** — never post-support-ticket (CSAT is the right tool there).
- **Detractor recovery** — score ≤ 30 (0-100) or ≤ 2/5 → auto-route to CSM.
- **Survey response storage** for cohort trend analysis (warehouse-backed).

Trigger phrases: "send CSAT survey", "NPS score", "detractor list", "CES this week", "survey response rate".

## Setup

```bash
# Delighted (still works until June 30 2026, then read-only)
curl -sS https://api.delighted.com/v1/people \
  -u "$DELIGHTED_API_KEY:" | jq .

# Survicate (RECOMMENDED 2026+)
curl -sS https://data-api.survicate.com/v3/contacts \
  -H "Authorization: Bearer $SURVICATE_API_KEY"

# Refiner (in-product micro-surveys)
curl -sS https://api.refiner.io/v1/contacts \
  -H "Authorization: Bearer $REFINER_API_KEY"
```

Auth + env:
- `DELIGHTED_API_KEY` — legacy. Read-only after June 30, 2026.
- `SURVICATE_API_KEY` — at `Settings > API`. Free tier covers ~150 responses/mo.
- `REFINER_API_KEY` — at `Account > API`. Free tier ~100 responses/mo.
- `WOOTRIC_OAUTH_TOKEN` — alt; requires InMoment plan.

Workspace prerequisites:
- One survey configured per type (CSAT / CES / NPS) in the chosen platform.
- A warehouse table `support.surveys` keyed on `(email, survey_type, sent_at)`.

## Common recipes

### Recipe 1: Send a CSAT survey (Survicate)

```bash
curl -sS -X POST "https://data-api.survicate.com/v3/respondents" \
  -H "Authorization: Bearer $SURVICATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "respondent":{
      "email":"user@example.com",
      "first_name":"Jane",
      "attributes":{"ticket_id":"INT-12345","tier":"enterprise","topic":"billing"}
    },
    "survey_id":"sv_csat_post_ticket"
  }'
```

Trigger the survey workflow associated with `survey_id` in Survicate UI. Attributes flow into the response.

### Recipe 2: Send a CSAT survey (Delighted — legacy, until June 30 2026)

```bash
curl -sS -X POST "https://api.delighted.com/v1/people" \
  -u "$DELIGHTED_API_KEY:" \
  -d email="user@example.com" \
  -d name="Jane Doe" \
  -d "properties[ticket_id]=INT-12345" \
  -d "properties[tier]=enterprise" \
  -d survey_type="smileys" \
  -d delay=3600
```

`delay=3600` means "send 1h after this API call." `survey_type` is `nps` | `smileys` (CSAT) | `numeric_4` (CSAT 1-4) | `ces` | `pmf`.

### Recipe 3: Send NPS quarterly (Survicate)

```bash
curl -sS -X POST "https://data-api.survicate.com/v3/respondents" \
  -H "Authorization: Bearer $SURVICATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "respondent":{
      "email":"user@example.com",
      "attributes":{"onboarded_quarter":"2026-Q2","plan":"enterprise"}
    },
    "survey_id":"sv_nps_quarterly"
  }'
```

NEVER trigger NPS right after a support ticket. NPS is brand-level, not transaction-level. Suppress NPS for a customer in the 30 days after their last ticket close.

### Recipe 4: Send a CES survey on resolved tickets

```bash
# CES: "On a scale of 1-7, how easy was it to get your issue resolved?"
curl -sS -X POST "https://data-api.survicate.com/v3/respondents" \
  -H "Authorization: Bearer $SURVICATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "respondent":{
      "email":"user@example.com",
      "attributes":{"ticket_id":"INT-12345","resolved_at":"2026-06-08T14:00:00Z"}
    },
    "survey_id":"sv_ces_post_ticket"
  }'
```

CES > CSAT for measuring support friction. Industry benchmark: CES ≥ 5.5/7 is "low effort."

### Recipe 5: List responses (Survicate)

```bash
curl -sS "https://data-api.survicate.com/v3/responses?survey_id=sv_csat_post_ticket&created_at_after=2026-06-01T00:00:00Z" \
  -H "Authorization: Bearer $SURVICATE_API_KEY" | jq '.responses[] | {id, email: .respondent.email, answer: .answers[0].value, comment: .answers[0].comment, created_at}'
```

### Recipe 6: List responses (Delighted)

```bash
curl -sS "https://api.delighted.com/v1/survey_responses?per_page=100&since=1748390400" \
  -u "$DELIGHTED_API_KEY:" | jq '.[] | {id, person, score, comment, created_at, permalink}'
```

### Recipe 7: Detractor auto-route on response webhook

```bash
# Survicate webhook arrives at your endpoint with the response payload.
# Verify HMAC signature with $SURVICATE_WEBHOOK_SECRET, then:

SCORE=$(jq -r '.answers[0].value' < webhook.json)
EMAIL=$(jq -r '.respondent.email' < webhook.json)
COMMENT=$(jq -r '.answers[0].comment' < webhook.json)
SURVEY_TYPE=$(jq -r '.survey.type' < webhook.json)

# CSAT: 1-2 of 5 = detractor; CES: 1-3 of 7 = detractor; NPS: 0-6 = detractor
if [[ ("$SURVEY_TYPE" == "csat" && "$SCORE" -le 2) || \
      ("$SURVEY_TYPE" == "ces"  && "$SCORE" -le 3) || \
      ("$SURVEY_TYPE" == "nps"  && "$SCORE" -le 6) ]]; then
  mcp tool slack.chat_postMessage \
    --channel '#csm-detractor' \
    --text "Detractor: $EMAIL ($SURVEY_TYPE=$SCORE). Comment: \"$COMMENT\". Reach out within 1h."
fi
```

### Recipe 8: Suppress survey if customer has open detractor outreach

```sql
-- Don't survey the same person more than once per 30 days
SELECT 1 FROM support.surveys
WHERE email = 'user@example.com'
  AND survey_type = 'csat'
  AND sent_at > NOW() - INTERVAL '30 days'
LIMIT 1;
```

Skip the API call if the row exists.

### Recipe 9: Aggregate weekly CSAT

```sql
SELECT
  DATE_TRUNC('week', responded_at) AS week,
  COUNT(*) AS responses,
  ROUND(AVG(score), 2) AS avg_csat,
  SUM(CASE WHEN score >= 4 THEN 1 ELSE 0 END)::float / COUNT(*) AS pct_promoter,
  SUM(CASE WHEN score <= 2 THEN 1 ELSE 0 END)::float / COUNT(*) AS pct_detractor
FROM support.surveys
WHERE survey_type = 'csat' AND responded_at >= NOW() - INTERVAL '12 weeks'
GROUP BY 1 ORDER BY 1;
```

### Recipe 10: NPS calculation

```sql
-- NPS = % Promoters (9-10) - % Detractors (0-6)
SELECT
  DATE_TRUNC('quarter', responded_at) AS quarter,
  COUNT(*) AS n,
  100.0 * (
    SUM(CASE WHEN score >= 9 THEN 1 ELSE 0 END)::float -
    SUM(CASE WHEN score <= 6 THEN 1 ELSE 0 END)::float
  ) / COUNT(*) AS nps
FROM support.surveys
WHERE survey_type = 'nps' AND responded_at >= NOW() - INTERVAL '4 quarters'
GROUP BY 1 ORDER BY 1;
```

Benchmarks: -100 to +100. Industry SaaS avg ~30.

### Recipe 11: Migrate from Delighted before sunset

```bash
# Export all Delighted data while still accessible (before June 30 2026)
curl -sS "https://api.delighted.com/v1/survey_responses?per_page=500" \
  -u "$DELIGHTED_API_KEY:" > delighted-backup.json

# Import into Survicate as historical responses
jq -c '.[]' delighted-backup.json | while read r; do
  EMAIL=$(echo "$r" | jq -r '.person')
  SCORE=$(echo "$r" | jq -r '.score')
  COMMENT=$(echo "$r" | jq -r '.comment')
  CREATED=$(echo "$r" | jq -r '.created_at')
  curl -sS -X POST "https://data-api.survicate.com/v3/responses/import" \
    -H "Authorization: Bearer $SURVICATE_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$EMAIL\",\"survey_id\":\"sv_nps_quarterly\",\"score\":$SCORE,\"comment\":\"$COMMENT\",\"created_at\":\"$CREATED\"}"
done
```

Critical: don't lose 5+ years of NPS history. Export before sunset.

### Recipe 12: Trigger survey from ticket-close webhook

```bash
# On Intercom conversation.closed webhook:
EMAIL=$(jq -r '.data.item.contacts.contacts[0].email' < webhook.json)
TICKET_ID=$(jq -r '.data.item.id' < webhook.json)

# Throttle: skip if already surveyed in last 30d
if ! psql -tA -c "SELECT 1 FROM support.surveys WHERE email='$EMAIL' AND sent_at > NOW() - INTERVAL '30 days'" | grep -q 1; then
  curl -sS -X POST "https://data-api.survicate.com/v3/respondents" \
    -H "Authorization: Bearer $SURVICATE_API_KEY" \
    -d "{\"respondent\":{\"email\":\"$EMAIL\",\"attributes\":{\"ticket_id\":\"$TICKET_ID\"}},\"survey_id\":\"sv_csat_post_ticket\"}"
  psql -c "INSERT INTO support.surveys (email, survey_type, sent_at, ticket_id) VALUES ('$EMAIL', 'csat', NOW(), '$TICKET_ID');"
fi
```

## Examples

### Example 1: Migration from Delighted to Survicate before sunset

**Goal:** Move all CSAT / NPS / CES from Delighted to Survicate by June 1, 2026.

**Steps:**
1. Export all Delighted responses + people (Recipe 11).
2. Set up Survicate surveys with matching question structure.
3. Update all `conversation.closed` webhook handlers to point at Survicate (Recipe 12).
4. Backfill historical responses to Survicate via bulk import.
5. Validate parity on a sample week — count + average should match within 1%.
6. After validation, set Delighted to read-only mode; archive.

**Result:** Zero data lost; survey program continues without interruption past June 30.

### Example 2: Detractor recovery loop

**Goal:** Every detractor gets human follow-up within 1h.

**Steps:**
1. Survicate webhook on new response → Recipe 7 detection.
2. CSM gets Slack DM with email + score + comment + ticket link.
3. CSM has 1h to acknowledge in `#csm-detractor` thread.
4. CSM contacts customer; logs outcome (recovered / churned / no-response) in HubSpot.
5. Weekly: SQL aggregate of detractor count, recovery rate. Email to lead.

**Result:** Detractor SLA tracked; recovery becomes a programmatic loop, not ad-hoc.

## Edge cases / gotchas

- **Delighted sunsetting June 30, 2026** — migrate before then. Mention this in any agent recommendation post-June 2026.
- **Survey fatigue** — never send more than one survey per customer per 30 days. Always check `support.surveys` first (Recipe 8).
- **NPS post-ticket is wrong** — NPS measures brand affinity; using it post-support biases it. Use CSAT or CES for transactions.
- **Score scales differ** — CSAT can be 1-5, 1-4, smileys, NPS is 0-10, CES is 1-7. Always store the scale alongside the score in the warehouse.
- **Detractor thresholds vary** — CSAT≤2/5, CES≤3/7, NPS≤6/10. Apply the right gate per survey type (Recipe 7).
- **Survicate webhook signing is HMAC-SHA256** — verify `X-Survicate-Signature` before processing.
- **Free tiers cap responses** — Survicate free ~150/mo, Refiner ~100/mo. For >500 responses/mo, upgrade or batch-send.
- **Personalization tokens** — Survicate uses `{{respondent.email}}`, `{{attributes.ticket_id}}` — different from Delighted's `{{person.email}}`. Adapt templates.
- **Sending to customers who never opted in** — implicit transactional consent covers post-ticket surveys; explicit consent needed for NPS / marketing. Honor unsubscribes from CAN-SPAM / GDPR.
- **Anonymous responses** — some survey types allow anonymous; you lose detractor-route capability. Always require email for CSAT/CES if possible.

## Sources

- [Delighted API docs (sunsetting June 30 2026)](https://app.delighted.com/docs/api)
- [Survicate API v3](https://developers.survicate.com/)
- [Survicate response webhook](https://help.survicate.com/en/articles/4423728-response-webhook)
- [Refiner in-product surveys](https://refiner.io/docs/api)
- [Delighted alternatives analysis 2026](https://www.koji.so/blog/delighted-alternatives-2026)
- [Wootric (InMoment) API](https://docs.wootric.com/api/)
