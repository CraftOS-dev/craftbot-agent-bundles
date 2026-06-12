<!--
Engagement-tier suppression: engaged / sometimes / dormant / sunset.
Reactivation only to dormant; sunset = suppressed.
-->
# Engagement-Based Suppression — SKILL

Engagement-tier suppression is the single highest-leverage deliverability lever. Define engaged / sometimes-engaged / dormant / sunset tiers; route campaigns only to active cohorts; reactivate dormant once; suppress sunset.

## When to use

- "Sender reputation is dropping — fix the list"
- "Define engagement tiers for our list"
- "Build reactivation flow for the 90-180d cohort"
- "Suppress 180+d inactive subscribers cleanly"
- "Reduce send volume to protect reputation"
- "Audit who's getting our newsletters and shouldn't be"

## Setup

No new tooling — works in any ESP. This skill defines the segments + send rules.

Required ESP capabilities:
- Segments based on `last_opened`, `last_clicked` per profile
- Per-flow / per-campaign segment filters (include / exclude)
- Suppression list (one-way out of marketing)

## Common recipes

### Recipe 1: Engagement tier definitions

| Tier | Definition | Send rule |
|---|---|---|
| **Engaged** | Opened OR clicked < 30 days | All campaigns + flows |
| **Sometimes engaged** | Opened OR clicked 30-90 days | Campaigns + non-aggressive flows |
| **Dormant** | Opened OR clicked 90-180 days | Reactivation sequence ONLY (once) |
| **Sunset** | No open AND no click > 180 days | Suppressed (no sends unless explicit re-opt) |
| **New profile** | < 30 days since signup, < 1 send received | All flows + welcome series |

Note: "Opened" is unreliable post-Apple MPP. Prefer "Clicked OR Placed Order OR Profile Updated" as engagement signal:

```
engagement_signal = MAX(
  last_clicked_email_date,
  last_placed_order_date,
  last_active_on_site_date,
  last_profile_update_date
)
```

### Recipe 2: Create Klaviyo segments (per tier)

```bash
# Engaged
curl -X POST "https://a.klaviyo.com/api/segments" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"segment","attributes":{
    "name":"Tier: Engaged (clicked 30d)",
    "definition":{"condition_groups":[{"conditions":[
      {"type":"profile-metric","metric":"Clicked Email","comparison_type":"at-least","value":1,
       "timeframe":{"key":"in_the_last","value":30,"unit":"days"}}
    ]}]}
  }}}'

# Sometimes engaged
curl -X POST "https://a.klaviyo.com/api/segments" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"segment","attributes":{
    "name":"Tier: Sometimes Engaged (clicked 30-90d)",
    "definition":{"condition_groups":[{"conditions":[
      {"type":"profile-metric","metric":"Clicked Email","comparison_type":"between","values":[30,90],
       "timeframe":{"key":"days_ago"}}
    ]}]}
  }}}'

# Dormant
curl -X POST "https://a.klaviyo.com/api/segments" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"segment","attributes":{
    "name":"Tier: Dormant (clicked 90-180d)",
    "definition":{"condition_groups":[{"conditions":[
      {"type":"profile-metric","metric":"Clicked Email","comparison_type":"between","values":[90,180],
       "timeframe":{"key":"days_ago"}}
    ]}]}
  }}}'

# Sunset (suppress these)
curl -X POST "https://a.klaviyo.com/api/segments" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"segment","attributes":{
    "name":"Tier: Sunset (no click 180d)",
    "definition":{"condition_groups":[{"conditions":[
      {"type":"profile-metric","metric":"Clicked Email","comparison_type":"at-most","value":0,
       "timeframe":{"key":"in_the_last","value":180,"unit":"days"}},
      {"type":"profile-metric","metric":"Placed Order","comparison_type":"at-most","value":0,
       "timeframe":{"key":"in_the_last","value":180,"unit":"days"}}
    ]}]}
  }}}'
```

### Recipe 3: Create Customer.io segments

```bash
# Engaged
curl -X POST "https://api.customer.io/v1/segments" \
  -H "Authorization: $CIO_APP_API_KEY" \
  -d '{
    "name":"Tier: Engaged 30d",
    "type":"data-driven",
    "conditions":{"or":[
      {"event":{"name":"email_clicked","performed":{"count":">=1","within":"30d"}}},
      {"event":{"name":"placed_order","performed":{"count":">=1","within":"30d"}}}
    ]}
  }'

# Sunset
curl -X POST "https://api.customer.io/v1/segments" \
  -H "Authorization: $CIO_APP_API_KEY" \
  -d '{
    "name":"Tier: Sunset (no click 180d)",
    "type":"data-driven",
    "conditions":{"and":[
      {"event":{"name":"email_clicked","performed":{"count":"=0","within":"180d"}}},
      {"event":{"name":"placed_order","performed":{"count":"=0","within":"180d"}}}
    ]}
  }'
```

### Recipe 4: Send-rule matrix (apply to every campaign + flow)

```
| Campaign type            | Engaged | Sometimes | Dormant | Sunset |
|--------------------------|---------|-----------|---------|--------|
| Promotional broadcast    |   yes   |   yes     |  no     |  no    |
| Newsletter               |   yes   |   yes     |  no     |  no    |
| Transactional            |   yes   |   yes     |  yes    |  yes   |  ← bypasses suppression
| Lifecycle flow (active)  |   yes   |   yes     |  no     |  no    |
| Reactivation sequence    |   no    |   no      |  yes    |  no    |
| Sunset suppression flow  |   no    |   no      |  no     |  yes (final + suppress)
```

Practical Klaviyo campaign config:

```bash
curl -X POST "https://a.klaviyo.com/api/campaigns" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"campaign","attributes":{
    "name":"June newsletter",
    "audiences":{
      "included":["<engaged-segment-id>","<sometimes-segment-id>"],
      "excluded":["<dormant-segment-id>","<sunset-segment-id>"]
    },
    "send_options":{"use_smart_sending":true}
  }}}'
```

### Recipe 5: Reactivation sequence (dormant → engaged or sunset)

```bash
curl -X POST "https://a.klaviyo.com/api/flows" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"flow","attributes":{
    "name":"Reactivation — 2 emails over 14d",
    "trigger":{"type":"segment","segment_id":"<dormant-segment-id>"},
    "steps":[
      {"type":"email","delay_seconds":0,
       "template_id":"<react-1>",
       "subject_variants":[{"text":"We miss you — still want to hear from us?"}]},
      {"type":"conditional_split",
       "condition":{"type":"metric","name":"Clicked Email","since":"now-336h"},
       "yes_branch":"exit",
       "no_branch":"continue"},
      {"type":"email","delay_seconds":1209600,
       "template_id":"<react-2>",
       "subject_variants":[{"text":"Last chance: keep getting our emails?"}]},
      {"type":"action","delay_seconds":604800,
       "action":"suppress",
       "reason":"No engagement in 30d after dormant reactivation"}
    ],
    "exit_conditions":["Clicked Email","Unsubscribed","Placed Order"]
  }}}'
```

### Recipe 6: Sunset suppression (one-time daily cron)

```python
# Move all profiles in Sunset segment to suppressed
import requests, os

KLAVIYO_KEY = os.environ['KLAVIYO_API_KEY']
SUNSET_SEGMENT_ID = '<sunset-id>'

# Fetch all profiles in sunset segment
def get_sunset_profiles():
    url = f"https://a.klaviyo.com/api/segments/{SUNSET_SEGMENT_ID}/profiles?page[size]=100"
    while url:
        r = requests.get(url, headers={'Authorization': f'Klaviyo-API-Key {KLAVIYO_KEY}', 'revision': '2024-10-15'})
        body = r.json()
        for p in body['data']:
            yield p['attributes']['email']
        url = body.get('links', {}).get('next')

# Bulk suppress in chunks
emails = list(get_sunset_profiles())
print(f"Sunsetting {len(emails)} profiles")

for chunk in [emails[i:i+100] for i in range(0, len(emails), 100)]:
    requests.post(
        'https://a.klaviyo.com/api/profile-suppression-bulk-create-jobs',
        headers={'Authorization': f'Klaviyo-API-Key {KLAVIYO_KEY}', 'revision': '2024-10-15', 'Content-Type': 'application/json'},
        json={'data':{'type':'profile-suppression-bulk-create-job','attributes':{
            'profiles':{'data':[{'type':'profile','attributes':{'email':e}} for e in chunk]},
            'reason':'Sunset: no engagement 180+ days'
        }}}
    )
```

### Recipe 7: Engagement-aware throttle (don't blast every segment)

```bash
# Per-flow audience filter — flow level filter
curl -X PATCH "https://a.klaviyo.com/api/flows/<flow-id>" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"flow","attributes":{
    "additional_filters":{
      "exclude":["<sunset-segment-id>"]
    }
  }}}'
```

### Recipe 8: Multi-list engagement reconciliation

For brands with multiple lists (EN / FR / DE), engagement is per-profile not per-list. A profile clicking an EN email is engaged across all lists they're on. Build engagement segments at profile level, not list level.

### Recipe 9: Re-opt-in for sunset cohort (rare, careful)

If business case warrants:

```bash
# Single email to sunset cohort with explicit re-opt-in CTA → click sets profile property + adds to "Active" list
# Reach rate will be 1-3%; do NOT do this on a hot reputation IP — use isolated send
curl -X POST "https://a.klaviyo.com/api/campaigns" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"campaign","attributes":{
    "name":"Sunset Re-opt-in (separate IP pool)",
    "audiences":{"included":["<sunset-segment-id>"]},
    "send_options":{"use_smart_sending":true},
    "tracking_options":{"add_utm":true},
    "send_strategy":{"sending_pool_id":"<isolated-pool>"}
  }}}'
```

Always isolate. The bounce + complaint rate from sunset is multiples of normal; protect primary reputation.

### Recipe 10: Dashboard query for tier sizes

```sql
-- Postgres / warehouse query
WITH engagement AS (
  SELECT
    profile_id, email,
    MAX(event_date) FILTER (WHERE event_name = 'Clicked Email' OR event_name = 'Placed Order') AS last_engaged
  FROM events
  GROUP BY profile_id, email
)
SELECT
  CASE
    WHEN last_engaged > NOW() - INTERVAL '30 days' THEN 'Engaged'
    WHEN last_engaged > NOW() - INTERVAL '90 days' THEN 'Sometimes Engaged'
    WHEN last_engaged > NOW() - INTERVAL '180 days' THEN 'Dormant'
    ELSE 'Sunset'
  END AS tier,
  COUNT(*) AS profiles,
  ROUND(COUNT(*)::numeric / SUM(COUNT(*)) OVER () * 100, 1) AS pct_of_list
FROM engagement
GROUP BY 1
ORDER BY profiles DESC;
```

Healthy list shape: Engaged 25-40%, Sometimes 20-30%, Dormant 10-20%, Sunset <30%. Sunset > 50% = neglected hygiene; tighten suppression.

## Examples

### Example 1: Stop sender reputation slide

**Goal:** complaint rate climbed from 0.05% to 0.12% over 8 weeks; rescue reputation.

**Steps:**

1. Define engagement tiers (Recipe 1).
2. Create segments per tier (Recipe 2).
3. Pull tier counts (Recipe 10). Sunset is 45% of list — too large.
4. Run reactivation sequence on Dormant (Recipe 5) for 14 days.
5. After 30 days, suppress everyone still in Sunset (Recipe 6).
6. Update all campaign audiences to exclude Sunset (Recipe 4).
7. Monitor next 4 weeks: complaint rate should fall toward 0.05%; spam rate (Postmaster) toward 0.05%.

### Example 2: Quarterly hygiene playbook

**Goal:** maintain healthy tier mix.

**Steps:**

1. Monday morning of quarter-start: pull tier sizes (Recipe 10).
2. If Sunset > 30%: run reactivation on Dormant; suppress Sunset after 30 days.
3. If Engaged < 25%: investigate frequency, relevance, content quality — sender problem not list problem.
4. Re-test deliverability via Glock Apps (separate skill) at end of quarter.
5. Document tier distribution in monthly Notion (notion-mcp) page for trend tracking.

## Edge cases

- **MPP-only opens** (Apple Mail pre-fetch) inflate "engaged" via opens. Use clicks (or orders) as primary engagement signal; opens are advisory only.
- **B2B engagement is rare** — many B2B subscribers never click. Define engagement broader: includes "visited site within X days" or "logged into product within X days". Pull from PostHog / Mixpanel.
- **Transactional bypass** — transactional sends (receipts, password reset) must NEVER be filtered by engagement tier. They're consent-bypass and required.
- **Cold leads from imports** — newly-imported lists have no engagement history. Treat as "New profile" tier for first 30 days; do NOT classify as Sunset just because no clicks yet.
- **Re-engagement spam-trap risk** — sending to long-dormant addresses risks hitting recycled spam traps (old addresses now repurposed as traps). Validate Dormant via ZeroBounce before reactivation.
- **Suppression is one-way (mostly)** — Klaviyo's `suppress_profiles` marks as non-mailable. Reactivation requires explicit profile update via API. Don't suppress accidentally.
- **Click-to-engage attribution lag** — Klaviyo updates `last_clicked` within minutes; warehouse-based dashboards may be hours behind. Don't fire reactivation flow immediately after a sunset suppression — wait 24h.
- **Multi-language engagement** — if you send EN to a BG-preference subscriber, low clicks may reflect language mismatch not lack of interest. Cross-reference Language attribute + clicks.

## Sources

- [Klaviyo segmentation](https://help.klaviyo.com/hc/en-us/articles/115002542091)
- [Klaviyo suppression](https://help.klaviyo.com/hc/en-us/articles/360046068731)
- [Klaviyo list cleaning + deliverability](https://www.klaviyo.com/blog/list-cleaning-deliverability)
- [Customer.io segments](https://customer.io/docs/journeys/segments-overview/)
- [Apple Mail Privacy Protection](https://www.klaviyo.com/blog/apple-mail-privacy-protection)
- [Email engagement metrics post-MPP](https://www.litmus.com/blog/the-impact-of-apple-mail-privacy-protection-on-email-marketing/)
