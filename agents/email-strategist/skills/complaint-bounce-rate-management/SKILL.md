<!--
Complaint rate < 0.10% target (0.30% Google threshold).
Bounce categories. Alert thresholds. Auto-suppression rules.
-->
# Complaint + Bounce Rate Management — SKILL

Complaint rate target: < 0.10% (investigate); 0.30% triggers Google permanent rejections. Bounce categories: hard (suppress immediately), soft (suppress after 3-5 consecutive), spam-block (investigate reputation), auto-reply (ignore). Build dashboard + alert thresholds + auto-suppression workflows.

## When to use

- "Our complaint rate is climbing — diagnose and fix"
- "Set up alerting on complaint / bounce thresholds"
- "Hard bounce suppression workflow"
- "Pull complaint rate trend across campaigns"
- "We got a Google 'less than 0.30%' warning — what to do"

## Setup

No new tooling — uses ESP APIs + Postgres warehouse + Slack alerts.

```bash
# Required (already in agent.yaml):
#   cli-anything (curl)
#   postgresql-mcp (warehouse)
#   slack-mcp (alerts)
```

## Common recipes

### Recipe 1: Complaint rate thresholds + actions

| Rate | Status | Action |
|---|---|---|
| < 0.02% | Best-in-class | Maintain |
| 0.02-0.05% | Good | Maintain; routine hygiene |
| 0.05-0.10% | Watch | Audit recent campaigns; tighten segmentation |
| **0.10%** | **Investigate** | Pause aggressive sends; deep audit |
| 0.10-0.30% | Critical | Pause sunset / dormant sends; only engaged |
| **0.30%** | **Google rejection threshold** | Pause ALL marketing; emergency remediation |
| > 0.50% | Block territory | ESP may suspend account; immediate engagement w/ ESP support |

### Recipe 2: Bounce categories + suppression rules

| Bounce type | Code prefix | Action |
|---|---|---|
| **Hard bounce — invalid address** | 5.1.1, 5.1.2, 550 5.1.1, 550 user unknown | Suppress IMMEDIATELY |
| **Hard bounce — domain not found** | 5.4.1, 5.4.4 | Suppress immediately |
| **Soft bounce — mailbox full** | 4.2.2, 422 | Suppress after 3-5 consecutive |
| **Soft bounce — temp server error** | 4.x.x generally | Retry; suppress after 5 consecutive |
| **Spam block / Policy** | 5.7.1, 550 5.7.1 ("blocked"), policy reject | Investigate reputation; do NOT auto-suppress (often fixable on sender side) |
| **Auto-reply / OOO** | n/a (received as new email, not bounce) | Ignore |

### Recipe 3: Klaviyo — pull complaint rate trend

```bash
# Last 30 days, per-campaign
curl -X POST "https://a.klaviyo.com/api/campaign-values-reports" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"campaign-values-report","attributes":{
    "statistics":["delivered","spam_complaints","spam_complaint_rate","bounced","bounce_rate","unsubscribes","unsubscribe_rate"],
    "timeframe":{"key":"last_30_days"},
    "conversion_metric_id":"<placed-order-id>",
    "filter":"and(equals(send_channel,\"email\"))"
  }}}' | jq '.data.attributes.results | sort_by(-.statistics.spam_complaint_rate) | .[0:20] | .[] | {name: .groupings.campaign_name, sent: .statistics.delivered, complaints: .statistics.spam_complaints, complaint_rate: .statistics.spam_complaint_rate, bounce_rate: .statistics.bounce_rate}'
```

### Recipe 4: Postgres dashboard query

```sql
-- Daily complaint + bounce metrics
WITH daily AS (
  SELECT
    DATE(sent_at) AS send_date,
    SUM(delivered) AS total_delivered,
    SUM(spam_complaints) AS total_complaints,
    SUM(bounced) AS total_bounces,
    SUM(hard_bounces) AS total_hard,
    SUM(soft_bounces) AS total_soft
  FROM klaviyo_campaign_metrics
  WHERE sent_at > NOW() - INTERVAL '30 days'
  GROUP BY 1
)
SELECT
  send_date,
  total_delivered,
  ROUND(100.0 * total_complaints::numeric / total_delivered, 4) AS complaint_pct,
  ROUND(100.0 * total_bounces::numeric / total_delivered, 4) AS bounce_pct,
  ROUND(100.0 * total_hard::numeric / total_delivered, 4) AS hard_pct,
  ROUND(100.0 * total_soft::numeric / total_delivered, 4) AS soft_pct
FROM daily
ORDER BY send_date DESC;
```

### Recipe 5: Daily complaint rate cron + Slack alert

```bash
#!/bin/bash
# /etc/cron.daily/complaint-alert.sh

YESTERDAY=$(date -d "1 day ago" +%Y-%m-%d)

# Pull yesterday's rate
RESULT=$(psql "$POSTGRES_URL" -t -c "
  SELECT
    SUM(delivered) AS sent,
    SUM(spam_complaints) AS complaints,
    SUM(spam_complaints)::float / NULLIF(SUM(delivered),0) AS rate
  FROM klaviyo_campaign_metrics
  WHERE DATE(sent_at) = '$YESTERDAY'
")

SENT=$(echo "$RESULT" | awk -F'|' '{print $1}' | xargs)
COMPLAINTS=$(echo "$RESULT" | awk -F'|' '{print $2}' | xargs)
RATE=$(echo "$RESULT" | awk -F'|' '{print $3}' | xargs)

if (( $(echo "$RATE > 0.0010" | bc -l) )); then
  curl -X POST "$SLACK_WEBHOOK" -d "{\"text\":\":rotating_light: Complaint rate $RATE on ${YESTERDAY} (${COMPLAINTS} complaints / ${SENT} sent). Threshold 0.10%.\"}"
fi

if (( $(echo "$RATE > 0.0030" | bc -l) )); then
  curl -X POST "$SLACK_WEBHOOK" -d "{\"text\":\":fire: CRITICAL complaint rate $RATE on ${YESTERDAY}. Pause sends.\"}"
fi
```

### Recipe 6: Klaviyo — get suppressed list

```bash
curl "https://a.klaviyo.com/api/profiles?filter=any(subscriptions.email.marketing.suppression.reason,[\"BOUNCED\",\"FBL\",\"INVALID_EMAIL\",\"HARD_BOUNCE\",\"UNSUBSCRIBE\",\"MANUAL_SUPPRESSION\"])&page[size]=100" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  | jq '.data[] | {email: .attributes.email, suppression: .attributes.subscriptions.email.marketing.suppression}'
```

### Recipe 7: Identify highest-complaint campaigns + diagnose

```bash
# Get top-3 highest complaint campaigns last 30 days, then drill in
curl -s -X POST "https://a.klaviyo.com/api/campaign-values-reports" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"campaign-values-report","attributes":{
    "statistics":["delivered","spam_complaint_rate"],
    "timeframe":{"key":"last_30_days"}
  }}}' | jq '.data.attributes.results | sort_by(-.statistics.spam_complaint_rate) | .[0:3]'

# For each, pull the campaign details to investigate:
# - Subject line
# - From-name
# - Send time
# - Audience segment definition
# - Frequency (was this profile mailed in the last 7d?)
```

### Recipe 8: Sources of complaints (root cause analysis)

| Cause | Symptom | Fix |
|---|---|---|
| Sent to wrong segment | Specific segment has 5x baseline | Tighten segment; suppress wrong-cohort overlap |
| Frequency overload | Complaint rate creeps over weeks | Cap profiles at N sends/week; honor preference center |
| Subject bait-and-switch | High open, high complaint | Match subject to body content |
| Unsubscribe is hard | High complaint + low unsub | Make unsub one-click; visible footer |
| Unfamiliar sender | New domain / new ESP | Warming + reputation building first |
| Mismatched intent | Transactional-sounding subject on marketing | Stream separation (see transactional-vs-marketing skill) |
| Stale list | Old contacts forget signup | Re-engagement before broadcast |

### Recipe 9: Hard bounce auto-suppression (Klaviyo)

Klaviyo auto-suppresses hard bounces. Customer.io similarly. SES / Mailgun do NOT — you must build it.

```python
# SES bounce-event handler (SNS-driven Lambda)
import json, requests

def lambda_handler(event, context):
    for record in event['Records']:
        msg = json.loads(record['Sns']['Message'])
        bounce = msg.get('bounce', {})
        bounce_type = bounce.get('bounceType')  # Permanent / Transient / Undetermined
        bounce_subtype = bounce.get('bounceSubType')

        for recipient in bounce.get('bouncedRecipients', []):
            email = recipient['emailAddress']
            if bounce_type == 'Permanent':
                # Hard bounce — suppress
                suppress_in_klaviyo(email, reason=f'SES Hard bounce: {bounce_subtype}')
                suppress_in_warehouse(email)
            elif bounce_type == 'Transient':
                # Soft bounce — increment counter; suppress at threshold
                increment_soft_bounce(email)

def suppress_in_klaviyo(email, reason):
    requests.post(
        'https://a.klaviyo.com/api/profile-suppression-bulk-create-jobs',
        headers={'Authorization': f'Klaviyo-API-Key {KLAVIYO_KEY}', 'revision': '2024-10-15'},
        json={'data':{'type':'profile-suppression-bulk-create-job','attributes':{
            'profiles':{'data':[{'type':'profile','attributes':{'email':email}}]},
            'reason': reason
        }}}
    )
```

### Recipe 10: Soft bounce counter + threshold suppression

```sql
-- Postgres table for soft bounce tracking
CREATE TABLE bounce_counter (
  email text PRIMARY KEY,
  soft_bounces integer DEFAULT 0,
  last_soft_bounce timestamptz,
  last_hard_bounce timestamptz,
  status text DEFAULT 'active'
);

-- Increment on soft bounce
INSERT INTO bounce_counter (email, soft_bounces, last_soft_bounce)
VALUES ($1, 1, NOW())
ON CONFLICT (email) DO UPDATE
SET soft_bounces = bounce_counter.soft_bounces + 1, last_soft_bounce = NOW();

-- Suppress when ≥ 5 soft bounces within 30 days
SELECT email FROM bounce_counter
WHERE soft_bounces >= 5
  AND last_soft_bounce > NOW() - INTERVAL '30 days'
  AND status = 'active';
```

### Recipe 11: Complaint-driven cohort investigation

When complaint spikes:

```sql
-- Profiles that complained in last 7d — what's in common?
SELECT
  p.signup_source,
  p.signup_date,
  p.last_engagement_date,
  COUNT(*) AS complaints,
  AVG(DATE_PART('day', NOW() - p.signup_date)) AS avg_days_since_signup
FROM profile_events e
JOIN profiles p ON p.id = e.profile_id
WHERE e.event_name = 'Spam Complained'
  AND e.event_date > NOW() - INTERVAL '7 days'
GROUP BY 1, 2, 3
ORDER BY complaints DESC
LIMIT 20;
```

Look for: shared signup source (suspicious list?), recent signup (no relationship built?), specific campaign cohort (content / subject problem).

### Recipe 12: ISP-specific bounce code lookup

```python
# Common SMTP bounce codes
BOUNCE_CODES = {
    '5.1.1': ('Hard', 'Bad destination mailbox', 'Suppress'),
    '5.1.2': ('Hard', 'Bad destination domain', 'Suppress'),
    '5.1.10': ('Hard', 'Recipient address rejected', 'Suppress'),
    '5.2.1': ('Hard', 'Mailbox disabled', 'Suppress'),
    '5.4.4': ('Hard', 'Unable to route', 'Suppress'),
    '5.7.1': ('Spam-block', 'Message refused by policy', 'Investigate reputation'),
    '5.7.26': ('Spam-block', 'Authentication required', 'Fix SPF/DKIM/DMARC'),
    '4.2.0': ('Soft', 'Mail system error', 'Retry'),
    '4.2.2': ('Soft', 'Mailbox full', 'Suppress after 5'),
    '4.4.1': ('Soft', 'Connection time-out', 'Retry'),
    '4.7.0': ('Soft', 'Temp auth failure', 'Retry'),
}
def categorize_bounce(code):
    return BOUNCE_CODES.get(code, ('Unknown', 'Unrecognized code', 'Manual review'))
```

## Examples

### Example 1: Diagnose climbing complaint rate

**Goal:** complaint rate climbed from 0.04% to 0.14% over 6 weeks; rescue.

**Steps:**

1. Pull complaint rate trend per day (Recipe 4).
2. Identify start of climb. Cross-reference: what changed?
   - New campaign cadence?
   - New list import?
   - Segment definition broadened?
   - Subject style shift?
3. Pull top 5 complaint campaigns (Recipe 7). Inspect each:
   - Subject + content mismatch?
   - Audience overlap (mailing same profile too often)?
   - Time of day off (Saturday 6am gets disproportionate complaints)?
4. Run complaint cohort analysis (Recipe 11). Shared signup source?
5. Remediations:
   - Suppress problematic source list
   - Cap mailing frequency per profile (≤ 3/week)
   - Tighten segments (engaged-30d only for next 2 weeks)
   - Pause specific aggressive campaigns
6. Monitor next 2-4 weeks; expect complaint rate to fall toward 0.05% as engaged-only sends restore reputation.

### Example 2: Set up production-grade alert flow

**Goal:** never get caught off-guard by complaint spike.

**Steps:**

1. Daily cron (Recipe 5) — alerts at 0.10% (yellow) and 0.30% (red).
2. Weekly digest to ops team: complaint rate, bounce rate, top-3 campaigns by complaint, sunset cohort size (Recipe 4).
3. Real-time webhook: ESP fires on complaint events; auto-suppress + log to warehouse.
4. Quarterly: review ESP feedback loop subscriptions (Yahoo FBL, AOL, Comcast, Cox); ensure all senders' FBLs are active.

## Edge cases

- **Apple iCloud Mail does NOT provide FBL** — Apple users mark spam, but you don't get notified. Track Apple complaints indirectly via sender-domain reputation.
- **Gmail user marks "not spam" or "report spam"** — both events. Klaviyo / Customer.io expose `spam_complaints` (report spam only).
- **Compliance**: hard bounces don't unsubscribe the profile; they just block sending. Profile is still "subscribed" technically. Some teams add manual `bounced` status.
- **5.7.1 from Microsoft** — usually reputation-based ("Connecting IP has too many complaints"). Not a per-user issue; sender-wide problem.
- **Auto-replies (OOO) come back as new inbound emails** — not bounces. Should be filtered in ESP or your inbound handler.
- **Greylisting (4.x.x temp errors)** — server saying "try again later" to filter spam. Most ESPs auto-retry; not your problem.
- **Implicit unsubscribe = complaint** for some users — they hit "spam" instead of "unsubscribe". Make unsubscribe trivially easy (one-click, visible footer link).
- **Sender Score (Validity / Return Path)** — third-party reputation metric, less authoritative than Google/Microsoft post-mailer-tier. Use for trend only.
- **Bounce categorization varies per ESP** — Klaviyo's "hard" may include some 5.7.1 spam-blocks. Always log the raw SMTP code.

## Sources

- [Google bulk sender guidelines (0.10% / 0.30% thresholds)](https://support.google.com/mail/answer/81126)
- [Yahoo sender best practices](https://senders.yahooinc.com/best-practices/)
- [SES bounce + complaint handling](https://docs.aws.amazon.com/ses/latest/dg/notification-contents.html)
- [Klaviyo bounce + complaint reports](https://help.klaviyo.com/hc/en-us/articles/360046068731)
- [Customer.io bounce + complaint](https://customer.io/docs/journeys/managing-deliverability/)
- [RFC 3463 (SMTP enhanced status codes)](https://datatracker.ietf.org/doc/html/rfc3463)
- [RFC 5965 (ARF for FBL)](https://datatracker.ietf.org/doc/html/rfc5965)
