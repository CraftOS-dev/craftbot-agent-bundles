<!--
Source: https://glockapps.com/ + https://inboxable.com/
Pre-send seed-list inbox placement. 60+ ISPs. ISP-specific matrix.
-->
# Glock Apps + Inboxable Inbox Placement Testing — SKILL

Pre-send seed-list inbox placement: send draft to seed inboxes across 60+ ISPs (Gmail, Outlook, Yahoo, Apple, ProtonMail, Mail.ru, regional) → measure inbox vs spam vs missing vs Promotions tab. Glock Apps, Inboxable, mail-tester for one-off. Run before every major campaign, after DMARC changes, post-warmup.

## When to use

- "Run pre-send inbox placement test for upcoming campaign"
- "Diagnose ISP-specific spam folder issue"
- "Test deliverability after DMARC enforcement change"
- "Quarterly inbox placement baseline"
- "Compare placement before/after warming completion"
- "Test placement at Gmail Promotions vs Primary tab"

## Setup

```bash
# Glock Apps
# https://glockapps.com — sign up, get API token; $129/mo+ depending on tier
export GLOCK_API_KEY="<your-token>"

# Inboxable
# https://inboxable.com — $59/mo+
export INBOXABLE_API_KEY="<your-token>"

# mail-tester (free, one-off test)
# https://www.mail-tester.com — no auth, get unique address per test

# GMass inbox placement (within GMass tool)
# https://www.gmass.co/inbox

# Mailtrap (staging, NOT real ISPs)
# https://mailtrap.io
```

## Common recipes

### Recipe 1: Glock Apps — start a seed test

```bash
# Create test (returns test ID + list of seed addresses to send to)
curl -X POST "https://api.glockapps.com/v1/tests" \
  -H "Authorization: Bearer $GLOCK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"June newsletter — placement test",
    "size":"medium",
    "providers":["gmail","outlook","yahoo","apple","aol","protonmail","fastmail","gmx","mailru","yandex","tutanota","mailcom"],
    "description":"Pre-send for June campaign"
  }'

# Response includes seed_emails array — send your draft to each address
```

### Recipe 2: Send draft to seed list

```bash
# From your ESP (Klaviyo / Customer.io / etc.):
# Either:
#   - Send actual campaign to a Klaviyo segment containing the seed addresses
#   - Or use ESP's "send test" function to email all seeds

# In Klaviyo, create segment of seed addresses, send a test campaign
curl -X POST "https://a.klaviyo.com/api/campaigns" \
  -H "Authorization: Klaviyo-API-Key $KLAVIYO_API_KEY" -H "revision: 2024-10-15" \
  -d '{"data":{"type":"campaign","attributes":{
    "name":"Placement test — June",
    "audiences":{"included":["<seed-segment-id>"]},
    "campaign_messages":{"data":[{"type":"campaign-message","attributes":{
      "channel":"email",
      "content":{"subject":"Test: June newsletter","preview_text":"","from_email":"hello@mail.brand.com"},
      "template_id":"<template-id>"
    }}]}
  }}}'
```

### Recipe 3: Poll for results

```bash
# Wait 30-60 min for ISPs to deliver and Glock to scan
curl "https://api.glockapps.com/v1/tests/<test-id>" \
  -H "Authorization: Bearer $GLOCK_API_KEY" | jq '.results'
```

Response includes per-ISP matrix:

```json
{
  "test_id": "<id>",
  "status": "completed",
  "summary": {
    "total_seeds": 60,
    "inbox": 48,
    "spam": 4,
    "missing": 2,
    "promotions_tab": 6,
    "inbox_rate": 0.80,
    "spam_rate": 0.067,
    "deliverability_score": 8.3
  },
  "results": [
    {"provider":"gmail","email":"seed1@gmail.com","placement":"inbox","tab":"primary","auth":{"spf":"pass","dkim":"pass","dmarc":"pass"}},
    {"provider":"gmail","email":"seed2@gmail.com","placement":"inbox","tab":"promotions","auth":{...}},
    {"provider":"outlook","email":"seed3@outlook.com","placement":"spam","auth":{"spf":"pass","dkim":"pass","dmarc":"fail"}},
    {"provider":"yahoo","email":"seed4@yahoo.com","placement":"inbox","auth":{...}}
  ]
}
```

### Recipe 4: Produce per-ISP placement matrix

```python
import requests, os
from collections import defaultdict

KEY = os.environ['GLOCK_API_KEY']
TEST = os.environ['TEST_ID']

r = requests.get(f'https://api.glockapps.com/v1/tests/{TEST}', headers={'Authorization': f'Bearer {KEY}'}).json()

# Aggregate by provider
matrix = defaultdict(lambda: {'inbox':0, 'spam':0, 'missing':0, 'promotions':0, 'total':0})
for result in r['results']:
    p = result['provider']
    matrix[p]['total'] += 1
    placement = result['placement']
    if placement == 'inbox' and result.get('tab') == 'promotions':
        matrix[p]['promotions'] += 1
    elif placement == 'inbox':
        matrix[p]['inbox'] += 1
    elif placement == 'spam':
        matrix[p]['spam'] += 1
    else:
        matrix[p]['missing'] += 1

# Print
print(f"{'Provider':<15}{'Inbox':>7}{'Promo':>7}{'Spam':>7}{'Miss':>7}{'Rate':>8}")
for p, m in sorted(matrix.items()):
    inbox_pct = (m['inbox'] + m['promotions']) / m['total'] if m['total'] else 0
    print(f"{p:<15}{m['inbox']:>7}{m['promotions']:>7}{m['spam']:>7}{m['missing']:>7}{inbox_pct:>7.0%}")
```

Sample output:

```
Provider         Inbox  Promo   Spam   Miss   Rate
apple              5      0      0      0    100%
fastmail           4      0      0      0    100%
gmail              6      4      0      0    100%
outlook            3      0      2      1     50%
protonmail         4      0      0      0    100%
yahoo              5      0      0      1     83%
```

### Recipe 5: Inboxable — alt service

```bash
# Start test
curl -X POST "https://api.inboxable.com/v2/tests" \
  -H "Authorization: Bearer $INBOXABLE_API_KEY" \
  -d '{
    "test_name":"June newsletter",
    "seed_list_id":"<seed-list-id>"
  }'

# Get results
curl "https://api.inboxable.com/v2/tests/<test-id>/results" \
  -H "Authorization: Bearer $INBOXABLE_API_KEY"
```

### Recipe 6: mail-tester (free, one-off)

```bash
# Get one-time test address
TEST_ID=$(curl -s "https://www.mail-tester.com/" -L | grep -oP 'test-[a-z0-9]+(?=@srv1.mail-tester.com)' | head -1)
TEST_ADDR="${TEST_ID}@srv1.mail-tester.com"
echo "Send draft to: $TEST_ADDR"

# After send, fetch result
sleep 30
curl -s "https://www.mail-tester.com/${TEST_ID}&format=json" | jq '{
  score: .score,
  spam_assassin: .results[] | select(.type=="spam") | .details,
  auth: .results[] | select(.type=="auth"),
  blocklist: .results[] | select(.type=="blocklist")
}'
```

Score 10/10 = clean; 8-9 = minor issues; < 7 = serious.

### Recipe 7: Diagnose common spam-folder issues

For each ISP in spam:

| Reason | How to verify | Fix |
|---|---|---|
| DKIM signature missing | Check email header for `DKIM-Signature` | Configure ESP DKIM record |
| DMARC fail | Check DMARC report or test header | Fix alignment per dmarc-reporting skill |
| Bad sender reputation | Google Postmaster tier check | Reduce volume, clean list, warm up |
| Subject spam triggers | mail-tester SpamAssassin report | Rewrite subject without trigger words |
| Link-to-text ratio high | Count links vs text length | Add more text; fewer links |
| URL shortener | Check links for bit.ly / t.co | Use branded domain |
| Image-only email | No text content | Add real text |
| All-caps subject | Check subject | Lowercase |
| IP blocklisted | mxtoolbox blacklist check | Delist OR move to clean IP |

### Recipe 8: Compare before/after fix

```bash
# Before fix: spam at Outlook 40%
# After fix: spam at Outlook 5%

# Run two tests; compare matrices
RUN_1=$(curl -s "https://api.glockapps.com/v1/tests/<test-id-before>" -H "Authorization: Bearer $GLOCK_API_KEY")
RUN_2=$(curl -s "https://api.glockapps.com/v1/tests/<test-id-after>" -H "Authorization: Bearer $GLOCK_API_KEY")

# Print delta
echo "=== Before === "; echo "$RUN_1" | jq '.summary'
echo "=== After ==="; echo "$RUN_2" | jq '.summary'
```

### Recipe 9: Pre-send test workflow (canonical)

```bash
#!/bin/bash
# pre_send_test.sh

set -e

CAMPAIGN_NAME="$1"
TEMPLATE_ID="$2"

# 1. Start Glock test
TEST_ID=$(curl -s -X POST "https://api.glockapps.com/v1/tests" \
  -H "Authorization: Bearer $GLOCK_API_KEY" \
  -d "{\"name\":\"$CAMPAIGN_NAME\",\"providers\":[\"gmail\",\"outlook\",\"yahoo\",\"apple\"],\"size\":\"medium\"}" \
  | jq -r '.id')

# 2. Get seed list
SEEDS=$(curl -s "https://api.glockapps.com/v1/tests/$TEST_ID/seeds" \
  -H "Authorization: Bearer $GLOCK_API_KEY" | jq -r '.[].email')

# 3. Create Klaviyo segment from seeds (one-time helper)
echo "$SEEDS" | jq -R . > seeds.json
# ... bulk import to Klaviyo, attach to test segment ...

# 4. Send test campaign to seed segment from Klaviyo
# (Use Klaviyo API to create + send test campaign)

# 5. Wait 45 min for ISPs to deliver + Glock to scan
echo "Waiting 45 min for results..."
sleep 2700

# 6. Pull results
curl -s "https://api.glockapps.com/v1/tests/$TEST_ID" \
  -H "Authorization: Bearer $GLOCK_API_KEY" | jq '.summary, .results[] | {provider, placement}'

# 7. Alert if spam rate > 5%
SPAM_RATE=$(curl -s "https://api.glockapps.com/v1/tests/$TEST_ID" -H "Authorization: Bearer $GLOCK_API_KEY" | jq '.summary.spam_rate')
if (( $(echo "$SPAM_RATE > 0.05" | bc -l) )); then
  echo "ALERT: spam rate $SPAM_RATE — DO NOT SEND campaign as-is"
fi
```

### Recipe 10: Slack alert on bad placement

```bash
if (( $(echo "$INBOX_RATE < 0.80" | bc -l) )); then
  curl -X POST "$SLACK_WEBHOOK" -d "{
    \"text\":\":rotating_light: Placement test for '$CAMPAIGN_NAME' — inbox rate $INBOX_RATE. Review before send.\",
    \"attachments\":[{\"text\":\"Worst ISPs: $WORST_ISPS\"}]
  }"
fi
```

### Recipe 11: Test Gmail Promotions vs Primary tab

Gmail places promotional content (multiple links, image-heavy, "Save 20%" style) in Promotions tab. To land in Primary:

- Plain-text feel, single CTA
- No unsubscribe link visible (still in headers; for Promotions Gmail re-sorts to Primary if behaviorally engaged)
- "Person to person" From-name pattern
- Conversational subject

Test in Glock Apps — `tab` field returns `primary | promotions | updates | forums | social`.

### Recipe 12: ISP-specific deep-dive

```bash
# Pull only Gmail seeds + their auth status
curl "https://api.glockapps.com/v1/tests/<id>/results?provider=gmail" \
  -H "Authorization: Bearer $GLOCK_API_KEY" | jq '.[] | {email, placement, tab, auth, headers}'

# Check each Gmail seed's full header detail
# Common Gmail-specific diagnostics:
#   - "Authentication-Results: gmail.com; spf=pass; dkim=pass; dmarc=pass" → all good
#   - "spf=neutral" → SPF not aligned with From domain
#   - "dkim=fail" → DKIM signature broken (often a forwarder)
#   - "dmarc=fail" → DMARC alignment failure
#   - Above + "policy.spf-source=" → who Gmail thinks sent it
```

## Examples

### Example 1: Pre-send test for high-stakes campaign

**Goal:** $500K-revenue-impact campaign — must hit inbox.

**Steps:**

1. Build campaign in Klaviyo (draft).
2. Run Glock Apps test (Recipe 1).
3. Send draft to all seed addresses via Klaviyo test-campaign feature.
4. Wait 45 min.
5. Pull results (Recipe 3-4). Confirm inbox rate ≥ 90%.
6. Identify failures (Recipe 7). Fix any auth or content issues.
7. If inbox rate < 90%, fix and re-test before live send.
8. On clean, proceed with send.

### Example 2: Quarterly baseline placement audit

**Goal:** track placement health quarter-over-quarter; catch slow drift.

**Steps:**

1. Run standardized test each quarter with the same campaign-style template (not actual marketing — a placement-test template).
2. Compare Q1 / Q2 / Q3 / Q4 matrices.
3. Watch for ISP-specific trend (e.g., Outlook inbox rate dropping from 95% to 80% over 6 months → reputation slide; intervene).
4. Document in Notion (notion-mcp).

## Edge cases

- **Seed addresses are well-known to ISPs** — sending to seed lists doesn't perfectly mimic real-user reception. Use as directional, not absolute.
- **Provider mix matters** — test must include the ISPs your real list skews toward. For US lists: Gmail + Outlook + Yahoo + Apple. For EU: also GMX, Mail.ru if relevant.
- **Time-of-day** — placement varies by time. Test during your usual send window for best signal.
- **Glock free trial limits** — 1 test on signup. Real ongoing use requires paid plan.
- **mail-tester** is single-test only; doesn't show ISP-specific. Use for one-off quick check.
- **Mailtrap is for STAGING, not real ISPs** — Mailtrap is a developer's sandbox. Does not represent real deliverability.
- **B2B address placement** — corporate inboxes (Office 365 tenants, G Suite tenants) often have stricter filtering than consumer Outlook / Gmail. Add a few business-domain seeds if your audience is B2B.
- **AMP for Email placement** — Promotions tab in Gmail tends to be home for AMP. Don't expect AMP in Primary.
- **Promotion tab is not "spam"** — Gmail Promotions tab is delivered, just sorted. Distinguish in your reporting.
- **Seed list rotation** — services rotate seed addresses to avoid being trained as "always inbox." Don't game.

## Sources

- [Glock Apps](https://glockapps.com/)
- [Glock Apps API](https://glockapps.com/api/)
- [Inboxable](https://inboxable.com/)
- [mail-tester](https://www.mail-tester.com/)
- [GMass Inbox Placement](https://www.gmass.co/inbox)
- [Mailtrap](https://mailtrap.io/)
- [Putsmail (Litmus)](https://putsmail.com/)
- [Gmail tab placement guide](https://support.google.com/mail/answer/9259701)
- [MXToolbox blacklist check](https://mxtoolbox.com/blacklists.aspx)
