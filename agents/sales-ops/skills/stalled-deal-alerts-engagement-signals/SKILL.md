<!--
Source: https://www.gong.io/blog/stalled-deal/ + Salesforce best practices
Stalled-deal alerts + engagement signals (June 2026 SOTA).
-->
# Stalled-Deal Alerts + Engagement Signals — SKILL

Stale-deal detection: deal in stage > 1.5× median, no logged activity in 14+ days. Engagement signals: email opens/clicks, call recency, Gong sentiment shift, calendar engagement. Auto-alert AE + manager via Slack. Aging report weekly.

## When to use

- **Daily stale-deal scan** — find at-risk deals.
- **Engagement signal monitoring** — sentiment shift, ghost detection.
- **Slack alert deployment** — AE + manager pings.
- **Aging report** — weekly Friday digest by stage.
- **Multi-thread depth check** — single-threaded deals flagged.
- **Trigger phrases**: "stale deals", "deal at risk", "stalled opportunity", "Gong sentiment alert", "engagement scoring", "no recent activity".

Do NOT use this skill for: **deal-level NBA coaching** (use parent sales-agent `deal-coaching-next-best-action`); **forecasting bucket changes** (use `forecasting-clari-boostup-aviso`); **win/loss post-mortem** (use `win-loss-reporting-at-scale`).

## Setup

```bash
# CRM via api-gateway
export MATON_API_KEY="<key>"

# Gong
export GONG_BASIC=$(printf "$GONG_ACCESS_KEY:$GONG_SECRET" | base64)
export GONG_BASE="https://api.gong.io"

# Slack
export SLACK_TOKEN="<token>"

# Outreach / Salesloft for engagement
export OUTREACH_TOKEN="<token>"
export SALESLOFT_TOKEN="<token>"

# Warehouse for stage-median
export PG_URI="postgresql://..."
```

Required:
- CRM admin read access (SOQL or HubSpot)
- Gong API (Premium tier) for call sentiment
- Slack bot user + channel access

## Common recipes

### Recipe 1: Stale-deal definition (canonical)

```yaml
stale_criteria:
  - days_in_stage > 1.5 * stage_median_days
  - last_activity_date < (TODAY - 14)
  - is_closed = false

flag_severity:
  warning: 1.5x median OR 14d no activity
  critical: 2.0x median AND 21d no activity
  ghost: 30+d no activity (likely lost)

stage_median_lookup:
  source: warehouse fct_opportunity_stage_history
  measure: median days at-stage of last 4Q closed-won
  refresh: weekly

# Engagement signal scores (additive 0-100)
signal_scoring:
  recent_activity_log_2d: +20
  recent_activity_log_7d: +10
  champion_engaged_7d: +25
  meeting_scheduled_14d: +20
  gong_sentiment_positive_shift: +15
  gong_sentiment_negative_shift: -30
  multi_thread_depth_3plus: +15
  multi_thread_depth_1: -20
  decision_maker_silent_14d: -25
  competitor_mention_unresolved: -15

deal_health_threshold:
  green: > 60
  yellow: 30-60
  red: < 30
```

### Recipe 2: SOQL stale-deal query

```sql
SELECT Id, Name, Amount, StageName, Owner.Name, Owner.Email,
       CreatedDate, Last_Activity_Date__c,
       LastModifiedDate, Stage_Entered_Date__c,
       Champion__r.Name
FROM Opportunity
WHERE IsClosed = FALSE
  AND (Last_Activity_Date__c < N_DAYS_AGO:14
       OR Last_Activity_Date__c = NULL)
  AND Stage_Entered_Date__c < (TODAY - INTEGER_VALUE(1.5 * Current_Stage_Median_Days__c))
ORDER BY Amount DESC
```

Run via api-gateway:
```bash
curl "https://gateway.maton.ai/salesforce/services/data/v60.0/query?q=..." \
  -H "Authorization: Bearer $MATON_API_KEY"
```

### Recipe 3: Stage median pull (from warehouse)

```sql
-- weekly refresh into Salesforce custom field Current_Stage_Median_Days__c
WITH closed_history AS (
  SELECT opportunity_id, stage_entered, stage_exited, stage_name,
         DATE_DIFF('day', stage_entered, stage_exited) AS days_in_stage
  FROM fct_opportunity_stage_history
  WHERE stage_exited >= NOW() - INTERVAL '12 months'
    AND stage_exited IS NOT NULL
)
SELECT stage_name,
       PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY days_in_stage) AS median_days
FROM closed_history
GROUP BY stage_name;
```

Push back to Salesforce per-Opportunity via Composite API:
```bash
sf data upsert bulk --target-org prod --sobject Opportunity \
  --external-id Id --file stage_median_updates.csv
```

### Recipe 4: Daily stale-deal scan + Slack alert

```python
import requests, os
from datetime import datetime, timedelta

# 1. Query stale deals
q = """
SELECT Id, Name, Amount, StageName, Owner.Name, Owner.Email,
       Last_Activity_Date__c, Stage_Entered_Date__c,
       Days_In_Stage__c, Current_Stage_Median_Days__c
FROM Opportunity
WHERE IsClosed = FALSE
  AND (Last_Activity_Date__c < N_DAYS_AGO:14 OR Last_Activity_Date__c = NULL)
"""
deals = requests.get(f"https://gateway.maton.ai/salesforce/services/data/v60.0/query",
                     params={"q": q},
                     headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"}).json()["records"]

# 2. Filter to >= 1.5× median
stale = [d for d in deals
         if d.get("Current_Stage_Median_Days__c", 0) > 0
         and d.get("Days_In_Stage__c", 0) > 1.5 * d["Current_Stage_Median_Days__c"]]

# 3. Recommend NBA per stage
def nba(deal):
    stage = deal["StageName"]
    if stage in ("Evaluation","Proposal"):
        return "Multi-thread to economic buyer this week"
    if stage in ("Discovery"):
        return "Diagnose stall — call champion"
    return "Forecast review: bucket to pipeline"

# 4. Slack alert per stale deal
for deal in stale[:20]:  # top 20 by amount
    url = f"https://co.lightning.force.com/lightning/r/Opportunity/{deal['Id']}/view"
    msg = (f":warning: STALE: *{deal['Name']}* ${deal['Amount']:,.0f}\n"
           f"Stage: {deal['StageName']} ({deal['Days_In_Stage__c']:.0f}d, median {deal['Current_Stage_Median_Days__c']:.0f}d)\n"
           f"Last activity: {deal.get('Last_Activity_Date__c','never')}\n"
           f"Owner: {deal['Owner']['Name']}\n"
           f"NBA: {nba(deal)}\n"
           f"<{url}|view>")
    requests.post("https://slack.com/api/chat.postMessage",
                  headers={"Authorization": f"Bearer {os.environ['SLACK_TOKEN']}"},
                  json={"channel": "#sales-alerts", "text": msg})
```

### Recipe 5: Gong sentiment signal

```bash
# Pull recent calls + sentiment per deal owner
curl -X POST "$GONG_BASE/v2/calls/extensive" \
  -H "Authorization: Basic $GONG_BASIC" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {
      "fromDateTime": "2026-06-01T00:00:00Z",
      "toDateTime": "2026-06-11T23:59:59Z",
      "primaryUserIds": ["5012345"]
    },
    "contentSelector": {
      "exposedFields": {
        "interaction": {"sentiment": true},
        "content": {"trackers": true, "topics": true}
      }
    }
  }' \
  | jq '.calls[] | {id, title, sentiment_score: .interaction.sentiment_score, date}'
```

### Recipe 6: Engagement signal compute (per deal)

```python
import pandas as pd, requests, os
from datetime import datetime, timedelta

def signal_score(deal, gong_calls, emails, meetings):
    score = 50  # baseline
    now = datetime.now()

    last_act = deal.get("Last_Activity_Date__c")
    if last_act:
        days_since = (now - datetime.fromisoformat(last_act)).days
        if days_since <= 2: score += 20
        elif days_since <= 7: score += 10

    # Champion engaged
    if deal.get("Champion_Last_Touched__c"):
        cdays = (now - datetime.fromisoformat(deal["Champion_Last_Touched__c"])).days
        if cdays <= 7: score += 25

    # Future meeting
    if meetings and any(m['scheduled_for'] > now for m in meetings):
        score += 20

    # Gong sentiment
    recent_gong = [c for c in gong_calls if (now - c['date']).days <= 14]
    if recent_gong:
        latest = max(recent_gong, key=lambda c: c['date'])
        if latest['sentiment_score'] > 0.6: score += 15
        elif latest['sentiment_score'] < 0.3: score -= 30

    # Multi-thread depth
    stakeholders = deal.get("Stakeholders_Count__c", 0)
    if stakeholders >= 3: score += 15
    elif stakeholders == 1: score -= 20

    return min(100, max(0, score))

# Apply per deal
for deal in open_deals:
    deal['health_score'] = signal_score(deal, get_gong_calls(deal),
                                         get_emails(deal), get_meetings(deal))
    deal['health_color'] = "green" if deal['health_score'] > 60 else \
                            ("yellow" if deal['health_score'] > 30 else "red")
```

### Recipe 7: Multi-thread depth check

```sql
-- Count distinct contacts engaged on deal in last 30d
SELECT
  o.Id AS opp_id,
  o.Name,
  COUNT(DISTINCT t.WhoId) AS unique_contacts_engaged_30d,
  COUNT(DISTINCT t.WhoId) FILTER (WHERE c.Title ILIKE '%VP%' OR c.Title ILIKE '%C_O') AS exec_contacts
FROM Opportunity o
LEFT JOIN Task t ON t.WhatId = o.Id AND t.CreatedDate >= NOW() - INTERVAL '30 days'
LEFT JOIN Contact c ON c.Id = t.WhoId
WHERE o.IsClosed = FALSE
GROUP BY 1, 2
HAVING COUNT(DISTINCT t.WhoId) <= 1   -- single-threaded = at risk
ORDER BY o.Amount DESC;
```

### Recipe 8: Aging report (weekly Friday)

```python
import pandas as pd, requests, os
from datetime import datetime

q = """
SELECT StageName, COUNT(Id) deal_count, SUM(Amount) total_value,
       AVG(Days_In_Stage__c) avg_days, MAX(Days_In_Stage__c) max_days
FROM Opportunity
WHERE IsClosed = FALSE
GROUP BY StageName
ORDER BY StageName
"""
r = requests.get(f"https://gateway.maton.ai/salesforce/services/data/v60.0/query",
                 params={"q": q},
                 headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"}).json()

msg = "Pipeline aging report (Friday):\n\n"
msg += "| Stage | Deals | Value | Avg Days | Max Days |\n|---|---|---|---|---|\n"
for row in r['records']:
    msg += f"| {row['StageName']} | {row['deal_count']} | ${row['total_value']:,.0f} | {row['avg_days']:.0f}d | {row['max_days']:.0f}d |\n"

requests.post("https://slack.com/api/chat.postMessage",
              headers={"Authorization": f"Bearer {os.environ['SLACK_TOKEN']}"},
              json={"channel": "#sales-leadership", "text": msg})
```

### Recipe 9: Ghost detection (30d+ no contact)

```python
# "Ghost" = decision-makers silent > 30 days; likely lost
import requests, os

q = """
SELECT Id, Name, Amount, StageName, Owner.Email,
       Champion_Last_Touched__c, Economic_Buyer_Last_Touched__c
FROM Opportunity
WHERE IsClosed = FALSE
  AND (Champion_Last_Touched__c < N_DAYS_AGO:30
       OR Economic_Buyer_Last_Touched__c < N_DAYS_AGO:30)
"""
r = requests.get(f"https://gateway.maton.ai/salesforce/services/data/v60.0/query",
                 params={"q": q},
                 headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"}).json()

ghosts = r['records']
print(f"Ghost candidates: {len(ghosts)}")
# Slack to manager with recommendation: revive or bucket to Lost
```

### Recipe 10: Manager weekly digest (per pod)

```python
# Pod-level rollup: stale deals + healthy deals + at-risk top 5
import requests, os

managers = [{"name": "Alice", "email": "alice@co.com", "pod_id": 1, "channel": "#pod-alice"}]

for mgr in managers:
    q = f"""
    SELECT Id, Name, Amount, Days_In_Stage__c, Current_Stage_Median_Days__c, Health_Score__c
    FROM Opportunity
    WHERE IsClosed = FALSE
      AND Owner.Manager.Email = '{mgr['email']}'
    ORDER BY Amount DESC
    """
    r = requests.get(f"https://gateway.maton.ai/salesforce/services/data/v60.0/query",
                     params={"q": q},
                     headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"}).json()
    deals = r['records']
    stale = [d for d in deals if d.get('Days_In_Stage__c', 0) > 1.5 * d.get('Current_Stage_Median_Days__c', 30)]

    msg = (f"Pod {mgr['name']} pipeline digest:\n"
           f"- {len(deals)} open deals, ${sum(d['Amount'] for d in deals):,.0f}\n"
           f"- {len(stale)} stale (1.5× median)\n"
           f"- Top 3 at-risk:\n")
    for d in sorted(stale, key=lambda x: -x['Amount'])[:3]:
        msg += f"  * {d['Name']} ${d['Amount']:,.0f} ({d['Days_In_Stage__c']:.0f}d in stage)\n"

    requests.post("https://slack.com/api/chat.postMessage",
                  headers={"Authorization": f"Bearer {os.environ['SLACK_TOKEN']}"},
                  json={"channel": mgr['channel'], "text": msg})
```

### Recipe 11: Auto-task creation on stall

```bash
# Create Salesforce Task on stale deal for the owner
curl -X POST "https://gateway.maton.ai/salesforce/services/data/v60.0/sobjects/Task" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "Subject": "Stale Deal Review — multi-thread or bucket down",
    "Status": "Not Started",
    "Priority": "High",
    "WhatId": "006XX0000123ABC",
    "OwnerId": "005XX0000456DEF",
    "ActivityDate": "2026-06-12"
  }'
```

### Recipe 12: Sentiment-shift critical alert

```python
# Detect: deal had positive Gong sentiment last call; now negative
import requests, os
from datetime import datetime, timedelta

# Pull all calls for owners with open enterprise deals last 30d
calls = gong_pull_calls(filter={"fromDateTime": (datetime.now()-timedelta(days=30)).isoformat()})

# Group by opportunity
by_deal = {}
for call in calls:
    deal_id = call.get('crm_opportunity_id')
    if deal_id:
        by_deal.setdefault(deal_id, []).append(call)

for deal_id, deal_calls in by_deal.items():
    if len(deal_calls) < 2: continue
    sorted_calls = sorted(deal_calls, key=lambda c: c['date'])
    last_two = sorted_calls[-2:]
    if last_two[0]['sentiment_score'] > 0.6 and last_two[1]['sentiment_score'] < 0.3:
        # Critical shift
        msg = (f":rotating_light: SENTIMENT SHIFT — deal {deal_id}\n"
               f"Last call ({last_two[1]['date']}) score: {last_two[1]['sentiment_score']:.2f}\n"
               f"Previous call ({last_two[0]['date']}) score: {last_two[0]['sentiment_score']:.2f}\n"
               f"Recommend: AE investigate concerns this week")
        requests.post("https://slack.com/api/chat.postMessage",
                      headers={"Authorization": f"Bearer {os.environ['SLACK_TOKEN']}"},
                      json={"channel": "#sales-alerts", "text": msg})
```

## Examples

### Example 1: Roll out daily stale-deal alerts

**Goal:** No more "I forgot about that deal" — automated reminders.

**Steps:**
1. Recipe 3 — refresh stage medians weekly.
2. Add Salesforce field `Current_Stage_Median_Days__c` populated from warehouse.
3. Recipe 4 — daily 9am cron scans + Slacks.
4. Pair with Recipe 11 — auto-task to AE for top stale deals.
5. After 2 weeks: measure stale-deal rate trend.

**Result:** Stale-deal % drops 30% in first month; AEs act on signal.

### Example 2: Gong sentiment shift early warning

**Goal:** Catch deals turning negative before they go silent.

**Steps:**
1. Recipe 5 — daily pull Gong sentiment for all open-deal-related calls.
2. Recipe 12 — sentiment shift detection.
3. Alert AE + manager when positive → negative shift.
4. Hand off to sales-agent for diagnosis call.
5. Track: % of alerts that recover vs. lose.

**Result:** Earlier intervention saves ~15% of at-risk enterprise deals.

### Example 3: Multi-thread depth audit

**Goal:** Identify single-threaded deals at risk of champion-vacuum.

**Steps:**
1. Recipe 7 — query weekly.
2. Filter: deal > $50K + single contact engaged + > 14d into stage.
3. Slack to AE: "your deal is single-threaded; recommend introducing decision-maker."
4. Track multi-thread depth quarter-over-quarter.

**Result:** Multi-thread depth lifts; champion-leaves disasters reduce.

## Edge cases / gotchas

- **`Last_Activity_Date__c` is a formula or rollup** — must include emails, calls, meetings. Activity logs differ across CRMs.
- **Median-stage-days bias** — using closed-won only skews short; using closed-lost adds context. Use both.
- **Weekend/holiday adjustments** — 14d through Christmas isn't necessarily stalled. Use business-days median.
- **Newly-created deals** — < 5d old shouldn't trigger; filter.
- **Deals re-stamped to current stage** — backwards advancement resets `Stage_Entered_Date__c`; need history table.
- **Slack alert fatigue** — > 20/day = nobody reads. Cap; only top N by value.
- **Owner OOO** — alerts during vacation = annoying. Suppress if owner OOO.
- **Gong API quota** — heavy daily pulls hit rate limit; batch.
- **Sentiment scores are model-dependent** — Gong vs Chorus vs Fathom differ; calibrate baseline.
- **Champion field empty** — many AEs don't fill it. Validation rule enforces (`salesforce-admin-custom-fields-flows`).
- **HubSpot equivalents** — `Last_Activity_Date` vs `hs_lastactivitydate`. Confirm field name.
- **Multi-AE deals (splits)** — alert one or both? Define.
- **Auto-task vs Slack** — pick one channel; both = noise.
- **False positives on "stale"** — sometimes deal is paused intentionally (procurement delay). Add pause field.
- **Manager digest interval** — daily = too much. Weekly Friday = right cadence.
- **Stage criteria change** — new stage "Evaluation 2.0" requires median rebuild; lookback breaks.

## Sources

- [Gong — Stalled Deal Research](https://www.gong.io/blog/stalled-deal/)
- [Gong API — calls + sentiment](https://app.gong.io/settings/api/documentation)
- [Salesforce Last Activity Date](https://help.salesforce.com/s/articleView?id=sf.activities_intro.htm)
- [HubSpot Recent Engagement](https://knowledge.hubspot.com/contacts/activity-history)
- [Sales activity benchmarks (Outreach 2026)](https://www.outreach.io/resources/state-of-sales)
- [Multi-thread depth research (Force Management)](https://www.forcemanagement.com/blog/multi-threading-sales)
- [MEDDIC champion enforcement (Force Mgmt)](https://www.forcemanagement.com/blog/meddic-meddpicc)
- [Slack chat.postMessage](https://api.slack.com/methods/chat.postMessage)
