<!--
Source: https://www.partnerstack.com/blog/partner-nps + https://www.netpromoter.com/know/ + https://www.delighted.com/docs/api + https://www.typeform.com/developers/ + https://help.survicate.com/en/articles/api
Partner NPS + satisfaction survey: distribution → response → trend analysis → detractor recovery (June 2026 SOTA).
-->
# Partner NPS + Satisfaction Survey — SKILL

Run quarterly Partner NPS with 5-6 follow-up scaled + open-ended questions. Distribute via Typeform / Delighted / Survicate / Wynter / HubSpot Surveys / Google Forms; collect responses; warehouse into Postgres; compute NPS per quarter + per tier + per motion; trend over time; trigger detractor-recovery workflow within 30 days. Industry benchmark: Partner NPS > 30 = healthy, > 50 = best-in-class.

## When to use

- **Quarterly Partner NPS launch** — distribute → 60% response target → 21-day window.
- **Mid-cycle pulse** — 3-question micro-survey post-major-program-change.
- **Detractor recovery workflow** — within 30 days of detractor response.
- **NPS trend reporting** — quarterly to leadership + board.
- **Per-tier / per-motion segmentation** — gold vs silver, reseller vs integration vs referral.
- **Feeds scorecard** — NPS is one of the partner-scorecard KPIs.
- **Trigger phrases**: "Partner NPS this quarter", "send NPS survey", "detractor recovery", "NPS trend", "what did Acme score us last quarter".

Do NOT use this skill for: **customer NPS** (defer to `customer-support-agent`); **partner scorecard rendering** (use `partner-scorecard-authoring`); **PAB member NPS** (use `partner-advisory-board-pab` Recipe 10); **employee/partner CSAT during onboarding** (use `partner-onboarding-90-day-plan`).

## Setup

```bash
export MATON_API_KEY="<key>"
export TYPEFORM_API_TOKEN="<token>"
export DELIGHTED_API_KEY="<key>"
export SURVICATE_API_KEY="<key>"
export GMAIL_OAUTH_TOKEN="<token>"
export SLACK_BOT_TOKEN="<token>"
export WAREHOUSE_CONN_STR="postgres://..."
export NOTION_API_KEY="<key>"
```

**One-time setup:**
- Create Typeform / Delighted / Survicate workspace + survey template (see Recipe 1)
- Postgres table `partner_nps_responses` (partner_id, contact_email, score, q2_working, q3_not_working, q4_one_change, q5_subscores JSONB, submitted_at, quarter)
- Notion `Detractor Recovery` DB (partner_id, contact, score, follow-up owner, recovery plan, status, 90d retest score)
- Slack `#partner-nps` for promoter shout-outs + `#partner-nps-detractors` for recovery alerts

## Common recipes

### Recipe 1: Build survey in Typeform (one-time per quarter)

```bash
curl -X POST "https://api.typeform.com/forms" \
  -H "Authorization: Bearer $TYPEFORM_API_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "title":"Partner NPS — Q3 2026",
    "fields":[
      {"title":"On a 0-10 scale, how likely are you to recommend our partner program to a peer?",
       "type":"opinion_scale","properties":{"steps":11,"start_at_one":false}},
      {"title":"What is working well in our partnership? (1-3 sentences)","type":"long_text"},
      {"title":"What is not working as well as it could be? (1-3 sentences)","type":"long_text"},
      {"title":"If we changed one thing next quarter, what would it be?","type":"long_text"},
      {"title":"Quality of partner enablement (training, certs, content)","type":"rating","properties":{"steps":5}},
      {"title":"Quality of co-marketing support","type":"rating","properties":{"steps":5}},
      {"title":"Speed of deal-reg approvals","type":"rating","properties":{"steps":5}},
      {"title":"MDF process clarity + speed","type":"rating","properties":{"steps":5}},
      {"title":"Channel-manager / PM support","type":"rating","properties":{"steps":5}},
      {"title":"Anything else?","type":"long_text"}
    ],
    "hidden":["partner_id","contact_email","tier","motion"]
  }'
```

Reference: https://www.typeform.com/developers/.

### Recipe 2: Delighted (NPS-specific tool, alternate)

```bash
# Send NPS survey to a partner contact via Delighted
curl -X POST "https://api.delighted.com/v1/people.json" \
  -u "$DELIGHTED_API_KEY:" \
  -d "email=sarah@acme.com&name=Sarah Lee&delay=0&properties[partner_id]=acme-001&properties[tier]=gold&properties[motion]=reseller"

# Pull responses (NPS auto-computed by Delighted)
curl "https://api.delighted.com/v1/survey_responses.json?per_page=100" \
  -u "$DELIGHTED_API_KEY:" | jq '.[] | {score, comment, person, properties, created_at}'
```

Reference: https://www.delighted.com/docs/api.

### Recipe 3: Survicate (multi-channel: email + portal + chat)

```bash
# Send a contact via API
curl -X POST "https://api.survicate.com/v3/contacts" \
  -H "Authorization: Bearer $SURVICATE_API_KEY" -H "Content-Type: application/json" \
  -d '{"email":"sarah@acme.com","attributes":{"partner_id":"acme-001","tier":"gold","motion":"reseller"}}'

# Trigger a specific NPS campaign
curl -X POST "https://api.survicate.com/v3/campaigns/<campaign_id>/trigger" \
  -H "Authorization: Bearer $SURVICATE_API_KEY" \
  -d '{"contact_email":"sarah@acme.com"}'
```

Reference: https://help.survicate.com/en/articles/api.

### Recipe 4: Wynter (B2B-grade research panel, alternate)

For deep qualitative segments (e.g., 20 strategic partners): Wynter panels collect long-form structured feedback. Manual setup via wynter.com dashboard; results exported via CSV → warehouse via Recipe 6.

### Recipe 5: Mail-merge distribution via gmail-mcp

```python
def distribute_quarterly_nps(quarter, survey_url):
    contacts = warehouse_query("""
      SELECT pc.email, pc.first_name, p.partner_name, p.partner_id, p.tier, p.motion
      FROM partner_contacts pc
      JOIN partners p USING(partner_id)
      WHERE pc.is_primary_contact=true AND p.status='active'
    """)
    for c in contacts:
        url = f"{survey_url}#partner_id={c['partner_id']}&tier={c['tier']}&motion={c['motion']}"
        gmail_send(to=c["email"], subject=f"Quick {quarter} feedback (~3 min)",
                   body=f"""Hi {c['first_name']},

It's NPS time. Quick favor: 3 minutes of your honest feedback shapes how we serve {c['partner_name']} next quarter.

{url}

Single most-valuable thing you can tell us: what should we change?

— Sarah, VP Partnerships""")
```

### Recipe 6: Webhook → warehouse

```python
# Typeform / Delighted / Survicate webhook → POST /nps-ingest
def on_nps_response(payload):
    warehouse_exec("""
      INSERT INTO partner_nps_responses(
        partner_id, contact_email, score, q2_working, q3_not_working, q4_one_change,
        q5_subscores, submitted_at, quarter
      ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        payload["hidden"]["partner_id"], payload["respondent_email"],
        int(payload["answers"][0]["number"]),
        payload["answers"][1]["text"], payload["answers"][2]["text"], payload["answers"][3]["text"],
        json.dumps({"enablement":payload["answers"][4]["number"], "co_mktg":payload["answers"][5]["number"]}),
        payload["submitted_at"], current_quarter(),
    ))
    # Detractor → immediate alert
    if int(payload["answers"][0]["number"]) <= 6:
        slack_chat_post("#partner-nps-detractors",
                        f"Detractor: {payload['respondent_email']} scored {payload['answers'][0]['number']}. Recovery within 30d.")
```

### Recipe 7: Compute NPS per quarter

```sql
SELECT
  quarter,
  COUNT(*)                                                              AS responses,
  COUNT(*) FILTER (WHERE score >= 9)                                    AS promoters,
  COUNT(*) FILTER (WHERE score BETWEEN 7 AND 8)                         AS passives,
  COUNT(*) FILTER (WHERE score <= 6)                                    AS detractors,
  ROUND(100.0 * COUNT(*) FILTER (WHERE score >= 9)::numeric /
        NULLIF(COUNT(*), 0) -
        100.0 * COUNT(*) FILTER (WHERE score <= 6)::numeric /
        NULLIF(COUNT(*), 0), 1)                                         AS nps
FROM partner_nps_responses
GROUP BY quarter
ORDER BY quarter DESC;
```

### Recipe 8: NPS by tier + motion

```sql
SELECT
  p.tier, p.motion,
  COUNT(r.*) AS responses,
  ROUND(100.0 * COUNT(*) FILTER (WHERE r.score >= 9)::numeric / NULLIF(COUNT(*), 0) -
        100.0 * COUNT(*) FILTER (WHERE r.score <= 6)::numeric / NULLIF(COUNT(*), 0), 1) AS nps
FROM partner_nps_responses r
JOIN partners p USING(partner_id)
WHERE r.quarter = :quarter
GROUP BY p.tier, p.motion
ORDER BY p.tier, p.motion;
```

### Recipe 9: Detractor recovery workflow

```python
def create_detractor_recovery(partner_id, contact_email, score, comments):
    notion.pages.create(parent={"database_id":DETRACTOR_RECOVERY_DB},
        properties={
            "Partner":{"title":[{"text":{"content":lookup_partner_name(partner_id)}}]},
            "Contact":{"rich_text":[{"text":{"content":contact_email}}]},
            "Score":{"number":score},
            "Comments":{"rich_text":[{"text":{"content":comments[:1900]}}]},
            "Status":{"select":{"name":"open"}},
            "Owner":{"rich_text":[{"text":{"content":lookup_channel_manager(partner_id)}}]},
            "Recovery due":{"date":{"start":(today()+timedelta(days=30)).isoformat()}},
        })
    # Auto-schedule 1:1 with detractor within 7 days
    schedule_recovery_call(partner_id, contact_email)
```

### Recipe 10: 90-day retest after recovery

```sql
-- Find detractors from quarter N; check their score in quarter N+1
SELECT prev.partner_id, prev.contact_email, prev.score AS prev_score,
       curr.score AS curr_score, (curr.score - prev.score) AS delta
FROM partner_nps_responses prev
LEFT JOIN partner_nps_responses curr
  ON curr.partner_id = prev.partner_id AND curr.contact_email = prev.contact_email
WHERE prev.quarter = :prev_quarter AND prev.score <= 6
  AND curr.quarter = :curr_quarter
ORDER BY delta DESC;
```

Target: > 50% of detractors moved to passive (7-8) or promoter (9-10).

### Recipe 11: Promoter outreach (case-study candidates)

```python
def promoter_outreach(quarter):
    rows = warehouse_query("""
      SELECT partner_id, contact_email, score, q2_working
      FROM partner_nps_responses
      WHERE quarter = %s AND score >= 9
    """, (quarter,))
    for r in rows:
        # Ask for case study + LinkedIn quote + referral
        gmail_send(to=r["contact_email"],
                   subject=f"Quick ask — you scored us {r['score']}/10 this quarter",
                   body=f"""Hi,

Loved your feedback: "{r['q2_working'][:150]}..."

Two asks:
1) Can we feature {lookup_partner_name(r['partner_id'])} in a joint case study?
2) Know one peer who'd benefit from our partner program? Warm intro?

— Sarah""")
```

### Recipe 12: Quarterly trend chart to leadership

```python
def render_nps_trend(quarters_back=8):
    rows = warehouse_query(NPS_TREND_SQL, (quarters_back,))
    chart = build_chart(rows, x="quarter", y="nps", target_line=30)
    save_to_drive(chart, f"partner-nps-trend-{today()}.png")
    gmail_send(to="leadership@vendor.com",
               subject=f"Partner NPS — Q{current_quarter()}",
               body=f"NPS = {rows[0]['nps']}. Trend attached.", attachments=[chart])
```

## Examples

### Example 1: Q3 2026 launch — 67% response rate; NPS = 42; 8 detractors recovered

**Goal:** Launch quarterly Partner NPS; collect; analyze; recovery loop.

**Steps:**
1. Recipe 1 — Typeform built; pre-fills `partner_id` + `tier` + `motion` via hidden fields.
2. Recipe 5 — Distributed to 180 primary contacts via gmail-mcp Monday.
3. Day 7 — 38% response. Slack reminder.
4. Day 14 — 58% response. Personal nudge from channel managers.
5. Day 21 — Window closes at 67%.
6. Recipe 7 — NPS = 42 (healthy, up from 36 Q2).
7. Recipe 8 — Reseller motion NPS = 48 vs Integration motion NPS = 31 (concern).
8. Recipe 9 — 22 detractors identified; recovery DB seeded.
9. Recipe 11 — 36 promoters; 4 say yes to case studies.
10. Recipe 10 (Q4) — 14/22 detractors moved to passive/promoter.

**Result:** NPS trend up; detractor recovery > 50% target; promoter cohort drives case studies.

### Example 2: Detractor recovery — Acme scored 4

**Goal:** Acme's primary contact scored 4 citing MDF delays.

**Steps:**
1. Recipe 6 webhook fires; Slack alert in `#partner-nps-detractors`.
2. Recipe 9 — Notion recovery card created; channel manager owns.
3. Day 3 — Channel manager calls; documents root cause: MDF approval cycle > 3 weeks.
4. 30-day recovery plan: switch Acme to fast-track MDF queue; weekly status update.
5. Q+1 — Recipe 10 — Acme's primary scored 7. Moved to passive.

**Result:** Recovery action ties to systemic improvement; detractor → passive shift.

### Example 3: Integration motion NPS gap → product hand-off

**Goal:** Recipe 8 shows Integration partners score 11 pts lower than reseller. Investigate.

**Steps:**
1. Recipe 8 segmentation surfaces gap.
2. Filter q3 (not working) comments for integration partners → cluster.
3. Top complaint: API rate limits + deprecation notice too short.
4. Cross-agent hand-off: `product-manager` for API roadmap; raise at next `partner-advisory-board-pab`.
5. Q+1 — Add 90-day deprecation policy; rate-limit increase. Integration NPS rebounds to 41.

**Result:** Segmentation isolates systemic issue; product fix closes loop.

## Edge cases / gotchas

- **Survey fatigue** — partners receive 4+ vendor NPS surveys/year. Keep yours under 3 min; pre-fill via hidden fields; offer mid-cycle 1-question pulse instead of full survey.
- **Selection bias toward promoters** — happy partners respond; unhappy go silent. Personal channel-manager outreach to lower-tier partners boosts response rate.
- **Single-respondent bias** — one contact per partner = one opinion. For Strategic+ partners, survey 2-3 contacts and average.
- **Wrong contact** — sales lead at partner ≠ partner program owner. Ensure `is_primary_contact` flag in CRM is accurate; quarterly audit.
- **NPS during transition** — major program changes mid-quarter skew results. Note in trend chart; don't over-react.
- **Comments anonymity tension** — fully anonymous lowers response rate from execs but raises candor from ICs. Default identified for trends + offer anonymous channel for raw feedback.
- **Score game-playing** — 7-8 "safe passive" zone underestimates dissatisfaction. Always weight follow-up Q5 sub-scores for nuance.
- **Detractor recovery time** — 30 days is tight for systemic issues. Document recovery plan + ETA; honest > fake.
- **Promoter inflation** — if score > 65, audit response composition (top-tier overrepresented?).
- **Quarterly cadence too frequent for small programs** — < 30 active partners → semiannual.
- **Comparison across motions** — apples-to-oranges. Always present segmented + headline.
- **Cultural NPS interpretation** — EMEA / APAC partners score conservatively (8 = excellent). Segment by region; adjust expectations.
- **Detractor → churn correlation** — 2 consecutive detractor quarters = strong churn signal. Trigger off-board / save-conversation.
- **Tool lock-in** — Delighted is NPS-only; Typeform/Survicate more flexible; Wynter for deep qual. Match tool to question type.
- **Webhook reliability** — if webhook fails, response lost. Daily reconciliation pull (Recipe 2 GET endpoint) catches misses.
- **Privacy + GDPR** — store email + score with lawful basis (legitimate interest in partner relationship); honor delete requests.

## Sources

- Partnerstack Partner NPS: https://www.partnerstack.com/blog/partner-nps
- Net Promoter primary: https://www.netpromoter.com/know/
- Delighted API: https://www.delighted.com/docs/api
- Typeform API: https://www.typeform.com/developers/
- Survicate API: https://help.survicate.com/en/articles/api
- Wynter B2B research: https://wynter.com/
