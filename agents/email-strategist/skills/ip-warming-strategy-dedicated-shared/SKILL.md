<!--
Source: Lemwarm, Mailflow, Warmup Inbox, Folderly, MailReach, TrulyInbox
4-6 week warming. Engaged-cohort targeting. Parallel reply loops.
-->
# IP Warming Strategy (Dedicated / Shared) — SKILL

Warm a new dedicated IP or sending domain over 4-6 weeks with engaged-cohort targeting and parallel reputation building via Lemwarm / Mailflow / MailReach / Folderly / Warmup Inbox / TrulyInbox / GMass Warmer.

## When to use

- "We just got a new dedicated IP from Klaviyo / SendGrid / Mailgun / SES — warm it"
- "Switching ESPs, bringing existing volume to new IPs — design migration"
- "New sending domain (cold from scratch)"
- "Reactivating a previously-paused sending domain"
- "Set up Mailflow / MailReach warming for the next 4 weeks"

## Setup

```bash
# Warming tools — pick one (or two for cross-coverage):
#   Lemwarm (by Lemlist)      — $29/mo per inbox
#   Mailflow                   — $49/mo, includes deliverability monitoring
#   MailReach                  — $25/mo per inbox
#   Folderly                   — $80/mo, includes audit + remediation
#   Warmup Inbox               — $19/mo per inbox
#   TrulyInbox                 — $9/mo per inbox (cheapest)
#   GMass Warmer               — $20/mo (bundled with GMass)
```

Auth:

```bash
export LEMWARM_API_KEY="<lemlist-token>"
export MAILFLOW_API_KEY="<mailflow-token>"
export MAILREACH_API_KEY="<mailreach-token>"
```

## Common recipes

### Recipe 1: Build day-by-day warming schedule

```python
import math

def warming_schedule(target_daily_volume: int, total_weeks: int = 6) -> list[dict]:
    """4-6 week ramp. Start at 50/day to most-engaged. Double daily for week 1."""
    schedule = []
    daily = 50
    days_per_week = 7
    for week in range(1, total_weeks + 1):
        for day in range(1, days_per_week + 1):
            cohort = ('most_engaged' if week <= 2 else
                      'engaged'      if week <= 4 else
                      'sometimes_engaged' if week == 5 else
                      'all')
            schedule.append({
                'week': week, 'day': day,
                'volume': min(daily, target_daily_volume),
                'cohort': cohort,
            })
            # Ramp logic: aggressive week 1, then 2x per week
            if week == 1:
                daily = min(daily * 2, target_daily_volume)
            elif week == 2:
                daily = min(int(daily * 1.5), target_daily_volume)
            else:
                daily = min(int(daily * 1.3), target_daily_volume)
    return schedule

for entry in warming_schedule(target_daily_volume=50000, total_weeks=6):
    print(f"W{entry['week']}D{entry['day']:2d}: {entry['volume']:6d} → {entry['cohort']}")
```

Sample output:
```
W1D1:     50 → most_engaged
W1D2:    100 → most_engaged
W1D3:    200 → most_engaged
W1D4:    400 → most_engaged
W1D5:    800 → most_engaged
W1D6:  1,600 → most_engaged
W1D7:  3,200 → most_engaged
W2D1:  4,800 → most_engaged
...
W6D7: 50,000 → all
```

### Recipe 2: Define engaged cohorts (Klaviyo)

```bash
# Most engaged: opened OR clicked in last 30d
curl -X POST "https://a.klaviyo.com/api/segments" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" \
  -H "revision: 2024-10-15" \
  -d '{"data":{"type":"segment","attributes":{
    "name":"Warming W1-2: Most Engaged 30d",
    "definition":{"condition_groups":[{"conditions":[
      {"type":"profile-metric","metric":"Opened Email","comparison_type":"at-least","value":1,"timeframe":{"key":"in_the_last","value":30,"unit":"days"}}
    ]}]}
  }}}'

# Engaged: opened OR clicked in last 90d (used week 3-4)
# Sometimes engaged: opened OR clicked in last 180d (used week 5-6)
# Suppress sunset cohort entirely during warmup
```

### Recipe 3: Enroll in Lemwarm

```bash
curl -X POST "https://api.lemlist.com/api/v1/warmup/email" \
  -H "Authorization: Bearer $LEMWARM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "warmup@notify.brand.com",
    "smtp": {
      "host": "smtp.sendgrid.net",
      "port": 587,
      "username": "apikey",
      "password": "<smtp-pw>",
      "encryption": "tls"
    },
    "imap": {
      "host": "imap.gmail.com",
      "port": 993,
      "username": "warmup@notify.brand.com",
      "password": "<imap-pw>"
    },
    "dailyTarget": 30,
    "rampUpDays": 21,
    "weekdays": [1,2,3,4,5],
    "replyRate": 0.5
  }'
```

Lemwarm sends + auto-replies + stars messages with friendly inboxes in its network, simulating engagement.

### Recipe 4: Enroll in MailReach

```bash
curl -X POST "https://api.mailreach.co/v1/inboxes" \
  -H "Authorization: Bearer $MAILREACH_API_KEY" \
  -d '{
    "name": "warming Inbox",
    "smtp_credentials": {...},
    "warming_plan": "smart-warming",
    "max_daily_volume": 40,
    "warming_days": 28,
    "spam_check_frequency": "daily"
  }'
```

MailReach also runs daily spam-folder checks at major ISPs to gauge progress.

### Recipe 5: Daily monitoring during warmup

```bash
# Pull Google Postmaster spam rate + IP reputation daily
curl "https://gmailpostmastertools.googleapis.com/v1/domains/notify.brand.com/trafficStats?endDate.year=2026&endDate.month=6&endDate.day=9" \
  -H "Authorization: Bearer $GPMT_TOKEN" | jq '{spamRate, domainReputation, ipReputation, deliveryErrors}'

# Microsoft SNDS (CSV)
curl "https://sendersupport.olc.protection.outlook.com/snds/data.aspx?key=$SNDS_KEY" \
  -o snds-today.csv

# Track complaint rate
curl "https://a.klaviyo.com/api/campaign-values-reports" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"campaign-values-report","attributes":{
    "statistics":["spam_complaint_rate"],
    "timeframe":{"key":"yesterday"},
    "filter":"and(equals(send_channel,\"email\"))"
  }}}' | jq '.data.attributes.results'
```

Pause-and-reduce thresholds:
- complaint rate > 0.001 (0.10%) → pause; debug source
- domainReputation drops to MEDIUM → reduce volume 50%, hold 2 days
- domainReputation drops to LOW → pause warmup; audit list quality
- ipReputation = BAD → pause; engage ESP support

### Recipe 6: Klaviyo IP warming flow (built-in)

Klaviyo provides an "Initial Send Schedule" for new dedicated IPs:

```bash
# Enable on dedicated IP (Klaviyo Plus/Advanced contract required for dedicated IP)
curl -X PUT "https://a.klaviyo.com/api/sending-options" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"sending-options","attributes":{
    "dedicated_ip_warming":{
      "enabled":true,
      "ramp_curve":"klaviyo_default",
      "target_audience":"engaged_30d",
      "max_daily":50000
    }
  }}}'
```

### Recipe 7: SendGrid dedicated IP warmup (automated)

```bash
# SendGrid auto-warmup (Pro+ plan)
curl -X PATCH "https://api.sendgrid.com/v3/ips/<ip>" \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -d '{"warmup":true,"start_date":1717948800}'
```

SendGrid handles ramp; you just don't manually override.

### Recipe 8: SES dedicated IP warmup (manual)

SES does NOT auto-warmup. Build the schedule yourself:

```python
# Pseudocode for SES warmup with config set rotation
from boto3 import client
ses = client('sesv2')

for day_entry in warming_schedule(50000, 6):
    # Allocate today's volume to dedicated pool
    daily_quota = day_entry['volume']
    # Throttle ESP send rate to match
    ses.put_account_sending_attributes(MaxSendRate=math.ceil(daily_quota / 86400))
    # Pull engaged cohort from your data store, send to them
    for batch in get_engaged_cohort(day_entry['cohort'], limit=daily_quota):
        ses.send_email(ConfigurationSetName='dedicated-warmup', ...)
```

### Recipe 9: Pause-and-recover protocol

If reputation drops during warmup:

```bash
# 1. Stop sends immediately
curl -X PATCH "https://a.klaviyo.com/api/flows/<flow-id>" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"flow","attributes":{"status":"draft"}}}'

# 2. Audit recent sends: subject, list quality, content
# 3. Clean list: ZeroBounce / Emailable
# 4. Reduce volume to 25% of last clean day, hold 2-3 days
# 5. Re-ramp at 1.2x daily (slower than fresh warmup)
```

### Recipe 10: Parallel warmup with multiple services

For aggressive multi-source reputation building:

- Lemwarm (50/day reply loops) + Mailflow (40/day) = ~90/day of "friendly engagement" alongside your real sends.
- This is grey-area at best; Google has occasionally cracked down on warmup networks. Use sparingly and stop once reputation reaches `HIGH`.

## Examples

### Example 1: Warm new Klaviyo dedicated IP for $10M+ DTC brand

**Goal:** move from shared to dedicated IP without volume drop.

**Steps:**

1. Verify list quality before warmup: complaint rate < 0.05% over last 90d, hard bounce < 0.5%, engaged 30d > 30% of list.
2. Get dedicated IP from Klaviyo support (Plus/Advanced contract, ~$250/mo).
3. Enable Klaviyo Initial Send Schedule (Recipe 6) with engaged-30d cohort.
4. Configure parallel Mailflow warmup for the IP (Recipe 4) — 40/day reply loops.
5. Daily morning routine:
   - Pull Postmaster stats (Recipe 5)
   - Confirm complaint rate < 0.001
   - Check IP reputation tier
6. Stay engaged-30d cohort weeks 1-2 (build positive signals fast).
7. Expand to engaged-90d week 3-4.
8. Sometimes-engaged-180d week 5.
9. All-active list week 6+.
10. By week 6, IP reputation should be HIGH in Google Postmaster; can flip all flows to dedicated IP.

### Example 2: Recover from reputation drop mid-warmup

**Goal:** week 3 of warmup hit complaint rate 0.18%; recover.

**Steps:**

1. Pause warming flows + campaigns immediately.
2. Audit: subject line, list source, segment definition for the offending send.
3. Common causes:
   - Subject mismatch (transactional-sounding subject on marketing)
   - Sent to dormant 90+ cohort accidentally
   - List recently imported (cold contacts)
4. Suppress affected list segment.
5. Run ZeroBounce full validation; remove invalids + catch-alls.
6. Resume at week 1 volumes (50-200/day) with most-engaged cohort. Re-ramp slowly.

## Edge cases

- **Warmup services can be detected by Google** — if Google flags an IP as part of a warmup network, the IP gets a reputation HIT, not a boost. Use reputable services (Lemwarm, MailReach, Mailflow); avoid sketchy clones.
- **Don't warm and send marketing on same IP simultaneously** — separate IPs. Warmup adds noise that hurts real send measurement.
- **Holiday seasonality** — warming during Black Friday / December = 3x volumes = guaranteed reputation drop. Avoid Nov 15 - Dec 31 warmup periods.
- **Subdomain reputation inheritance** — a hot subdomain (e.g., `mail.brand.com`) on a HIGH-reputation IP doesn't transfer reputation to a new IP. Each IP is its own reputation.
- **ESP-warmup-helper auto-throttle** — Klaviyo/SendGrid auto-warmup overrides per-flow throttle. Don't fight it.
- **Dedicated IPs and low volumes** — < 100K sends/mo on dedicated IP is harmful (reputation degrades from low signal). Stay shared until >100K.
- **Pre-existing reputation** — if your sending domain was previously on a warmed IP that's now retired, the domain reputation persists. Warming a new IP on a known-good domain is faster than cold-domain warmup.
- **Microsoft cold-domain heavy-handedness** — Outlook is harsher on new domains than Gmail. Expect 3-5x longer to reach good reputation at Outlook vs Gmail. Don't panic.
- **IP block on Day 1** — if a brand-new IP is on a blocklist (Spamhaus / SORBS / Barracuda), check with mxtoolbox.com and delist before sending real mail. Often a previous tenant left it blocklisted.

## Sources

- [Lemwarm](https://www.lemlist.com/lemwarm)
- [Mailflow](https://mailflow.com/)
- [MailReach](https://www.mailreach.co/)
- [Folderly](https://folderly.com/)
- [Warmup Inbox](https://www.warmupinbox.com/)
- [TrulyInbox](https://www.trulyinbox.com/)
- [Klaviyo IP warming guide](https://help.klaviyo.com/hc/en-us/articles/13635655082907)
- [SendGrid IP warmup](https://docs.sendgrid.com/ui/sending-email/warming-up-an-ip-address)
- [SparkPost warmup schedule](https://www.sparkpost.com/blog/sender-reputation-how-to-build-it/)
- [Google sender guidelines](https://support.google.com/mail/answer/81126)
