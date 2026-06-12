<!--
Sources: https://ks-agents.com/blog/boomerang-employees-alumni-network-strategy/
         https://peoplepath.com/blog/attract-and-rehire-boomerang-employees-through-your-corporate-alumni-network/
         https://beamery.com/resources/blogs/why-enterprise-organizations-need-an-alumni-hiring-strategy
         https://www.gem.com/blog/candidate-sourcing-software
         https://www.enterprisealumni.com
         https://www.metaview.ai/resources/blog/recruiting-trends
35% of 2025 hires were returning employees (up from 31%).
$4,200 avg savings per boomerang hire (Bain).
Pattern: alumni DB + LinkedIn change tracking + quarterly newsletter + ATS auto-flag on return.
Gem / Beamery re-engagement sequences. 12-18 month window is peak.
-->
# Boomerang + Alumni Re-engagement — SKILL

Maintain alumni database + LinkedIn change tracking + quarterly newsletter cadence + ATS auto-flag on return. Trigger re-engagement at 12-18 months post-departure (the peak window). Gem / Beamery re-engagement sequences operationalize at scale. 35% of 2025 hires were returning employees; $4,200 avg savings per boomerang hire (Bain). Don't leave this on the table.

## When to use

- User wants to **add a departing employee to the alumni DB** at offboarding.
- User wants to **run the quarterly alumni newsletter** + invite to events.
- User wants to **set up LinkedIn change tracking** for alumni (job-change alerts).
- User wants to **fire a "we miss you" outreach** at 12-18 month post-departure.
- User wants to **auto-flag returning alumni** in Greenhouse / Ashby / Lever.
- User wants to **plan an alumni event** (founders dinner, product update, etc.).
- Trigger phrases: "boomerang", "alumni", "rehire", "former employee", "ex-Acme", "we miss you", "alumni network", "alumni newsletter", "Enterprise Alumni", "PeoplePath".

Do not use for: silver-medalist re-engagement (interviewed-but-not-hired — they're hot-list, not alumni; use `hot-list-talent-community-mgmt`); current-employee referrals (different cadence + relationship); 90-day re-engagement of cold prospects (handled in `passive-candidate-outreach-campaigns`).

## Setup

```bash
# Primary alumni DB
export NOTION_API_KEY="secret_xxx"
export NOTION_ALUMNI_DB="<db_id>"

# Alumni network platforms (enterprise scale, optional)
export ENTERPRISE_ALUMNI_KEY="xxx"     # https://www.enterprisealumni.com
export PEOPLEPATH_KEY="xxx"            # https://peoplepath.com

# CRM for re-engagement sequences
export GEM_API_KEY="xxx"
export BEAMERY_API_KEY="xxx"

# Newsletter
export MAILCHIMP_API_KEY="xxx"
export MAILCHIMP_ALUMNI_LIST_ID="xxx"
export MAILCHIMP_DC="us1"

# LinkedIn change tracking
export SEEKOUT_API_KEY="xxx"            # SeekOut alerts
# (Gem also offers prospect.job_change_within_30d alerts)

# ATS auto-flag
export GREENHOUSE_API_KEY="harvest_xxx"
export ASHBY_API_KEY="xxx"
export LEVER_API_KEY="xxx"

# Comms
export GMAIL_TOKEN="xxx"
export SLACK_BOT_TOKEN="xoxb-xxx"
```

## Common recipes

### Recipe 1: Alumni DB schema (the canonical model)

```yaml
# Notion DB: one row per departed employee
schema:
  name: "Jane Doe"
  linkedin_url: "https://linkedin.com/in/janedoe"
  last_role: "Staff Software Engineer"
  team: "Platform"
  manager_at_departure: "Sarah Chen"
  start_date: "2022-03-01"
  departure_date: "2025-09-15"
  tenure_years: 3.5
  departure_reason: "voluntary"     # voluntary | involuntary | rif | retirement | other
  sentiment_at_exit: "positive"      # positive | neutral | negative
  eligibility_flag: "eligible"       # eligible | ineligible (legal-flagged for non-rehire)
  current_company: "Stripe"
  current_role: "Senior Staff Engineer"
  current_company_start: "2025-10-01"
  tenure_at_current_months: 8
  last_touch_date: "2026-04-15"
  last_touch_type: "newsletter Q1"
  touch_history:
    - {date: "2026-01-10", type: "newsletter Q4", channel: "email"}
    - {date: "2026-04-15", type: "newsletter Q1", channel: "email"}
  linkedin_change_alert_subscribed: true
  re_engagement_priority: "high"    # high | medium | low (based on role + sentiment + tenure)
  notes: "Star backend eng. Left amicably for IC growth. Manager would rehire tomorrow."
```

### Recipe 2: Offboarding intake (the moment of capture)

```python
# Run at exit interview / last-day workflow
# Auto-create alumni DB row via Notion API

departure_data = {
    "name": "Jane Doe",
    "linkedin_url": linkedin_lookup("Jane Doe", company="Acme"),
    "last_role": "Staff Software Engineer",
    "team": "Platform",
    "manager_at_departure": "Sarah Chen",
    "start_date": "2022-03-01",
    "departure_date": "2025-09-15",
    "departure_reason": "voluntary",     # captured at exit interview
    "sentiment_at_exit": "positive",      # captured via 1-5 exit survey
    "eligibility_flag": "eligible",       # confirmed by People-Ops
}

# Hard rules:
# - Skip add if eligibility_flag == "ineligible" (legal-flagged for non-rehire)
# - Skip add if sentiment_at_exit == "negative" AND departure_reason == "involuntary" (unless legal clears)
# - Always add if voluntary + positive/neutral sentiment

notion.pages.create(
    parent={"database_id": "$NOTION_ALUMNI_DB"},
    properties=...
)

# Auto-subscribe to LinkedIn change alerts
seekout_subscribe(linkedin_url=departure_data["linkedin_url"], tag="alumni-acme")
```

### Recipe 3: Subscribe LinkedIn change alerts (SeekOut)

```bash
# Subscribe alumni to job-change alerts via SeekOut
curl -X POST "https://api.seekout.com/v1/alerts" \
  -H "Authorization: Bearer $SEEKOUT_API_KEY" \
  -d '{
    "alert_type": "linkedin_role_change",
    "linkedin_urls": ["https://linkedin.com/in/janedoe","..."],
    "tag": "alumni-acme",
    "callback_url": "https://acme.com/webhooks/alumni-job-change"
  }'
```

Alternative — Gem alerts:

```bash
curl -X POST "https://api.gem.com/v1/alerts" \
  -H "Authorization: Bearer $GEM_API_KEY" \
  -d '{
    "alert_type": "prospect.job_change_within_30d",
    "tag": "alumni-acme",
    "webhook_url": "https://acme.com/webhooks/alumni-job-change"
  }'
```

### Recipe 4: Quarterly newsletter (Mailchimp)

```bash
# 4 sections — keep it short, valuable, no hard sell
# 1. Product win (1 paragraph)
# 2. Culture update (1 paragraph) — team milestones, new hires, anniversary callouts
# 3. Open roles (3-5 bullets with apply links)
# 4. Alumni spotlight — quote from a recent boomerang or an alum's win at their current company

# Create campaign in Mailchimp
curl -X POST "https://$MAILCHIMP_DC.api.mailchimp.com/3.0/campaigns" \
  -u "anystring:$MAILCHIMP_API_KEY" \
  -d '{
    "type": "regular",
    "recipients": {"list_id": "'$MAILCHIMP_ALUMNI_LIST_ID'"},
    "settings": {
      "subject_line": "Acme Q3 2026 — quick update from your old team",
      "from_name": "Sarah Chen (Eng Director)",
      "reply_to": "alumni@acme.com",
      "title": "Alumni Newsletter Q3 2026"
    }
  }'
```

Open rate benchmark: 35-55% (vs 18-22% for cold prospects). Click rate 5-12%. Treat as relationship marketing, not pipeline conversion.

### Recipe 5: 12-18 month re-engagement sequence (Gem)

Peak boomerang window is 12-18 months post-departure. Set up Gem sequence:

```bash
# Define alumni-re-engage-12mo sequence
curl -X POST "https://api.gem.com/v1/sequences" \
  -H "Authorization: Bearer $GEM_API_KEY" \
  -d '{
    "name": "alumni-re-engage-12mo",
    "steps": [
      {
        "step": 1,
        "channel": "email",
        "delay_days": 0,
        "subject": "Miss you, {first}",
        "body": "{first} — its been {months_since_departure} months since you left Acme. Team has grown; just shipped {recent_milestone}. If your current role isnt quite right, wed love to chat about {role_we_have} — different scope from when you were here. Coffee? Best, {recruiter}"
      },
      {
        "step": 2,
        "channel": "linkedin_message",
        "delay_days": 7,
        "body": "{first} — sent you an email last week; LinkedIn here too in case it landed in spam. No pressure; just keeping the door open. Best, {recruiter}"
      },
      {
        "step": 3,
        "channel": "email",
        "delay_days": 14,
        "subject": "Last note, {first}",
        "body": "Final note — leaving this open for whenever it makes sense. Acme has changed a lot since {departure_year}; happy to share a 15-min update over coffee anytime. Best, {recruiter}"
      }
    ]
  }'

# Enroll alumni hitting 12-month window
ALUMNI=$(curl "https://api.notion.com/v1/databases/$NOTION_ALUMNI_DB/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28" \
  -d '{
    "filter": {
      "and": [
        {"property":"departure_date","date":{"on_or_before":"'$(date -u -d '12 months ago' +%Y-%m-%d)'"}},
        {"property":"departure_date","date":{"on_or_after":"'$(date -u -d '18 months ago' +%Y-%m-%d)'"}},
        {"property":"sentiment_at_exit","select":{"does_not_equal":"negative"}},
        {"property":"eligibility_flag","select":{"equals":"eligible"}}
      ]
    }
  }' | jq -r '.results[].properties.name.title[0].plain_text')

for ALUM in $ALUMNI; do
  GEM_PROSPECT_ID=$(./resolve_prospect.sh "$ALUM")
  curl -X POST "https://api.gem.com/v1/sequences/alumni-re-engage-12mo/enroll" \
    -H "Authorization: Bearer $GEM_API_KEY" \
    -d "{\"prospect_id\":\"$GEM_PROSPECT_ID\",\"start_step\":1}"
done
```

### Recipe 6: Beamery alumni re-engagement (enterprise alternative)

```bash
# Beamery has native alumni hiring features
curl -X POST "https://api.beamery.com/v1/talent-pool/alumni/campaigns" \
  -H "Authorization: Bearer $BEAMERY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "alumni-re-engage-q3-2026",
    "audience_filter": {
      "tags": ["alumni-acme"],
      "departure_window_months_min": 12,
      "departure_window_months_max": 18,
      "eligibility": "eligible",
      "sentiment_exit_min": "neutral"
    },
    "sequence_template_id": "<template-id>",
    "personalization_tokens": ["months_since_departure","recent_milestone","role_we_have","departure_year"]
  }'
```

### Recipe 7: ATS auto-flag returning alumni (Greenhouse)

```bash
# Webhook: candidate.created -> check if linkedin_url matches alumni DB
# If match: auto-tag BOOMERANG + fast-track

# Manual lookup pattern:
NEW_CANDIDATE_LINKEDIN="$1"
IS_ALUM=$(curl "https://api.notion.com/v1/databases/$NOTION_ALUMNI_DB/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28" \
  -d "{\"filter\":{\"property\":\"linkedin_url\",\"url\":{\"equals\":\"$NEW_CANDIDATE_LINKEDIN\"}}}" \
  | jq -r '.results | length')

if [ "$IS_ALUM" -gt 0 ]; then
  TENURE=$(curl "https://api.notion.com/v1/databases/$NOTION_ALUMNI_DB/query" \
    -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28" \
    -d "{\"filter\":{\"property\":\"linkedin_url\",\"url\":{\"equals\":\"$NEW_CANDIDATE_LINKEDIN\"}}}" \
    | jq -r '.results[0].properties.tenure_years.number')

  curl -X POST "https://harvest.greenhouse.io/v1/applications/{application_id}/tags" \
    -u "$GREENHOUSE_API_KEY:" \
    -d "{\"tags\":[\"BOOMERANG\",\"fast-track\",\"previous-tenure-${TENURE}-yrs\"]}"

  # Notify previous manager via Slack
  curl -X POST "https://slack.com/api/chat.postMessage" \
    -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
    -d "channel=@sarah.chen&text=Heads up — {name} just applied to {role}. Previous tenure ${TENURE}y on your team."
fi
```

### Recipe 8: Ashby + Lever auto-flag

```bash
# Ashby
curl -X POST "https://api.ashbyhq.com/candidate.addTag" \
  -u "$ASHBY_API_KEY:" \
  -d '{"candidateId":"{id}","tagId":"<boomerang-tag-id>"}'

# Lever
curl -X POST "https://api.lever.co/v1/opportunities/{id}/tags" \
  -u "$LEVER_API_KEY:" \
  -d '{"tags":["BOOMERANG","fast-track"]}'
```

### Recipe 9: Departure-decision-matrix (who to keep warm)

```
Sentiment x Departure-Reason matrix → re-engagement priority

                     | Voluntary  | Involuntary | RIF       | Retired   |
---------------------|------------|-------------|-----------|-----------|
| Positive sentiment | HIGH       | (rare)      | HIGH      | MEDIUM    |
|                    | re-engage  | manual rev  | re-engage | event-inv |
| Neutral sentiment  | MEDIUM     | LOW         | MEDIUM    | LOW       |
|                    | re-engage  | quarterly   | re-engage | newsletter|
| Negative sentiment | LOW        | NONE        | LOW       | NONE      |
|                    | newsletter | exclude     | manual rev| exclude   |
```

Apply during Recipe 2 intake; set `re_engagement_priority` field.

### Recipe 10: Alumni event (founders dinner, product update)

```python
# Quarterly alumni event template
event = {
    "name": "Acme Alumni Dinner — Fall 2026",
    "venue": "SF / NYC / Remote",
    "date": "2026-10-15",
    "format": "30-min product update + open Q&A + dinner",
    "invitees_filter": {
        "geo": "us_west OR us_east",
        "departure_within_years": 5,
        "sentiment_at_exit": "positive OR neutral",
        "re_engagement_priority": "high OR medium"
    },
    "ceo_speaker": True,
    "hiring_pitch_minutes": 5,    # keep light; relationship over conversion
    "follow_up_30d": True,
}
```

Track RSVPs in Notion; trigger 1:1 outreach to invitees who don't reply.

### Recipe 11: Cost-of-hire benchmark (boomerang vs net-new)

| Metric | Boomerang | Net-new external | Lift |
|---|---|---|---|
| Cost-per-hire | $X - $4,200 | $X | Bain study: $4,200 avg savings |
| Time-to-fill | ~50% of net-new | baseline | Familiarity skips onboarding ramp |
| First-90d performance | higher | baseline | Cultural fit + institutional knowledge |
| 12-mo retention | higher | baseline | Self-selected return = stronger commitment |
| Onboarding cost | minimal | $5-15K | Tooling/access setup only |

Track these in `source-of-hire-reporting` slice. Boomerang typically tops cost-per-hire efficiency.

### Recipe 12: Manager-led outreach (the strongest pull)

The most effective alumni outreach comes from the alum's previous manager, not a recruiter. Recipe 5 fires the cadence; in parallel, push managers to do personal touches.

```python
# Monthly: send managers a list of their high-priority alumni due for outreach
managers_outreach_brief = {
    "manager": "Sarah Chen",
    "alumni_to_reach_this_month": [
        {"name": "Jane Doe", "departure_months_ago": 12, "current_company": "Stripe", "last_touch_days_ago": 90, "suggested_role": "Staff IC platform-eng"},
        {"name": "Alex K.", "departure_months_ago": 18, "current_company": "Snowflake", "last_touch_days_ago": 180, "suggested_role": "Senior IC infra"},
    ],
    "template": "Manager-personalized {first}, hope youre well at {current_company}. Was thinking about {specific_project_together} the other day. Would love to grab coffee + share whats happening at Acme. ..."
}
```

### Recipe 13: Year-over-year metrics

```yaml
# Track quarterly + annually
metrics:
  alumni_db_size: 487
  alumni_active_subscribed: 312     # opted in to newsletter
  newsletter_q3_open_rate: 0.42
  newsletter_q3_click_rate: 0.08
  re_engagement_sequences_sent: 65
  re_engagement_replies: 18         # 27% reply rate -> healthy
  hires_from_alumni_ytd: 11
  hires_from_alumni_pct_of_total: 0.14   # ~14% of hires -> on Bain's 35% benchmark we have headroom
  cost_savings_estimated: 11 * 4200       # $46,200 estimated savings
```

## Examples

### Example 1: New TA leader — no alumni DB exists
**Goal:** Just inherited TA function. No alumni tracking. Build foundation.
**Steps:**
1. Pull HR exit-interview data from People-Ops for last 3 years.
2. Create Notion DB per Recipe 1 schema; populate 200-400 rows.
3. Enrich each row with current LinkedIn role via SeekOut bulk-lookup.
4. Subscribe all to LinkedIn change alerts (Recipe 3).
5. Author + send Q3 newsletter (Recipe 4); track open rate as baseline.
6. Enroll alumni in 12-18 month window in re-engagement sequence (Recipe 5).
7. Wire Greenhouse webhook for ATS auto-flag (Recipe 7).
8. Schedule monthly manager-outreach brief (Recipe 12).

**Result:** Foundation in 4-6 weeks; first re-engagement hires within 2 quarters; year-1 boomerang share lifts from ~5% to 15-25% of hires.

### Example 2: Star eng left 13 months ago — re-engage
**Goal:** Notion alert: Jane Doe (Staff IC, 3.5y tenure, positive exit) hit 13-month departure window. She's at Stripe.
**Steps:**
1. Recipe 5 sequence auto-enrolls; step 1 sends today.
2. Sarah Chen (previous manager) gets the monthly Recipe 12 brief listing Jane as high-priority.
3. Sarah sends personal email same-day: "Hi Jane, been thinking about {our project together}; would love to grab coffee + tell you about what we're working on now."
4. Jane replies positive within 4 days; books coffee with Sarah.
5. Sarah loops in recruiter for Acme update + open Staff IC role; Jane interviews 3 weeks later.
6. Offer extended; declined initially (Stripe equity vesting); kept warm for 6-month follow-up.

**Result:** Even non-conversion is a relationship win; future window stays open + Jane refers 2 ex-Stripe eng colleagues to Acme over next 12 months.

### Example 3: Auto-flag boomerang at ATS
**Goal:** Alum (Alex K., left 14 mo ago) applied to careers page directly. Should get fast-track.
**Steps:**
1. Greenhouse webhook fires `candidate.created`; LinkedIn URL matches Notion alumni DB.
2. Recipe 7 auto-tags `BOOMERANG` + `fast-track` + `previous-tenure-2-yrs`.
3. Slack DM to Sarah Chen (previous manager) within 30 seconds.
4. Recruiter sees BOOMERANG tag in Greenhouse review queue; routes around standard application-review queue → directly to recruiter screen.
5. Recruiter sends personalized email same-day: "Alex — welcome back! Saw you applied to {role}; let's chat tomorrow."
6. Time-from-apply to recruiter-screen: <24h vs ~7d standard.

**Result:** Boomerang candidate feels valued; high offer-acceptance rate; positive employer-brand signal in alumni network.

## Edge cases / gotchas

- **Sentiment_at_exit must be honest.** Recording every departure as "positive" turns the field into noise. Calibrate via exit interview structured questions, not casual recall.
- **Eligibility flag is legal-owned.** People-Ops + legal set it; recruiters don't override. Common reasons: post-termination cooling-off, non-rehire clause in separation agreement, prior misconduct.
- **Sensitive RIF / layoff handling.** RIF'd alumni need explicit re-engage opt-in; pushing newsletter to someone you just laid off is a brand catastrophe. Default `subscribed = False` for RIF cohorts; require manual opt-in.
- **Non-compete enforcement varies by state.** California voids most non-competes; Texas / New York enforce some. Confirm with legal before recruiting an alum into a similar role at a competitor.
- **Confidential info during interviews.** Alum knows internal information; structure the interview to test current-state skill, not assume retained context. Re-NDA before scope discussions.
- **Manager turnover orphans alumni.** If Sarah left 6 months after Jane, who owns Jane's relationship? Solution: alumni assigned to current owner of the prior team, not the departed manager.
- **The "fast-track" tag is fast-track to recruiter screen, NOT to offer.** Boomerang still goes through full interview process; "previous tenure" is signal, not pass.
- **Newsletter frequency tuning.** Quarterly is right; monthly is too much. Annual = forgotten. Stick to 4/year.
- **Alumni event budget.** Founders dinner is $5-15K per event (food + venue + travel for org speakers). Plan budget at sponsor-cycle time.
- **EU alumni and GDPR.** EU alumni under GDPR have right-to-erasure; honor immediately. Distinguish lawful-basis (legitimate interest) for newsletter from explicit-consent (recruiting outreach).
- **Comp lift expectations.** Alumni returning typically expect ~15-25% lift vs prior comp + accounting for market. Underwhelming comp = "they remember when I was here last time" = decline.
- **Boomerang as Trojan horse.** Rare but real: alum returns for short stint to fill knowledge gap then leaves. Spot via 90-day intent conversation upfront.
- **Don't re-engage everyone at 12 months.** Negative-sentiment cohort = skip; involuntary departure = require explicit human review; ineligible = never.
- **Quarterly newsletter content discipline.** 1 product win + 1 culture + open roles + 1 alumni spotlight. NOT a sales blast. Open-rate signal will collapse if you over-pitch.
- **LinkedIn change alerts can be noisy.** Filter: title-change OR company-change with >30-day tenure at current. Ignore intra-company moves.
- **Hand off compensation discussion** to `ceo-agent` for execs / VPs; `operations-agent` for IC/manager comp framework. This skill sets up the conversation, doesn't close it.
- **Hand off contract execution + ATS administration** to `operations-agent` once boomerang accepts.
- **Hand off process upgrades** to People-Ops if alumni hiring becomes >25% of total — workflows need formal program (Enterprise Alumni or PeoplePath at scale).
- **Track cost-of-hire savings explicitly** (Recipe 11 + 13). Leadership wants the ROI story; "we hired some boomerangs" doesn't fund the newsletter budget.

## Sources

- KS-Agents — Boomerang + Alumni Network Strategy 2026: https://ks-agents.com/blog/boomerang-employees-alumni-network-strategy/
- PeoplePath — Boomerang re-engagement playbook: https://peoplepath.com/blog/attract-and-rehire-boomerang-employees-through-your-corporate-alumni-network/
- Beamery — Why enterprises need an alumni strategy: https://beamery.com/resources/blogs/why-enterprise-organizations-need-an-alumni-hiring-strategy
- Gem — Best Candidate Sourcing Software 2026: https://www.gem.com/blog/candidate-sourcing-software
- Enterprise Alumni platform: https://www.enterprisealumni.com
- Metaview — Recruiting Trends 2026 (alumni stats): https://www.metaview.ai/resources/blog/recruiting-trends
- SeekOut — LinkedIn change alerts: https://www.seekout.com
- Mailchimp API: https://mailchimp.com/developer/marketing/api/
- Greenhouse Harvest API — Application tags: https://developers.greenhouse.io/harvest.html#application-tags
- Ashby API — candidate.addTag: https://developers.ashbyhq.com/reference/candidateaddtag
- Lever API — Opportunity tags: https://hire.lever.co/developer/documentation
