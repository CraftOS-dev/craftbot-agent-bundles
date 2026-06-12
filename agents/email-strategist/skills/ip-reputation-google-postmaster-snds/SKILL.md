<!--
Source: https://developers.google.com/gmail/postmaster + Microsoft SNDS
+ Yahoo Postmaster + Apple iCloud Postmaster
Daily monitoring of spam rate / IP rep / domain rep / FBL / auth results.
-->
# IP Reputation (Google Postmaster v2 / SNDS / Yahoo / Apple) — SKILL

Daily reputation polling from the only authoritative sources: Google Postmaster Tools v2 (free, JSON API), Microsoft SNDS (free, CSV), Yahoo Postmaster (free, web), Apple iCloud Mail Postmaster (free, web). Alert on threshold breaches before they cascade to blocks.

## When to use

- "Set up daily reputation monitoring for our sending domain"
- "Investigate sudden delivery drop at Gmail / Outlook"
- "Track spam rate trend to stay under Google's 0.10% / 0.30% thresholds"
- "Get alerts when domain reputation drops a tier"
- "Audit IP reputation across all our dedicated IPs"

## Setup

### Google Postmaster Tools v2

```bash
# One-time GCP project setup
gcloud projects create email-postmaster-monitoring
gcloud config set project email-postmaster-monitoring

# Enable Postmaster Tools API
gcloud services enable gmailpostmastertools.googleapis.com

# Create service account
gcloud iam service-accounts create postmaster-bot \
  --display-name="Postmaster monitoring bot"

# Download key
gcloud iam service-accounts keys create ~/postmaster-key.json \
  --iam-account=postmaster-bot@email-postmaster-monitoring.iam.gserviceaccount.com

# Add the service account email as a "domain admin" in Postmaster Tools UI
# https://postmaster.google.com/managedomains?pli=1
```

```bash
export GPMT_SA_KEY="$HOME/postmaster-key.json"
export GPMT_DOMAIN="notify.brand.com"
```

### Microsoft SNDS

```bash
# Web signup at https://sendersupport.olc.protection.outlook.com/snds/
# Per-IP enrollment + verification
# Once authorized, get authenticated CSV URL with token
export SNDS_KEY="<your-snds-data-token>"
```

### Yahoo Postmaster

```bash
# Web signup at https://senders.yahooinc.com/
# Per-domain registration; no API, only web dashboards + FBL email subscription
```

### Apple iCloud Mail Postmaster

```bash
# Web signup at https://support.apple.com/en-us/HT204137
# Per-domain registration; no API; manual web reports
```

## Common recipes

### Recipe 1: Google Postmaster — daily traffic stats

```bash
# Get OAuth bearer token
GPMT_TOKEN=$(gcloud auth application-default print-access-token \
  --scopes=https://www.googleapis.com/auth/postmaster.readonly)

# List monitored domains
curl -s "https://gmailpostmastertools.googleapis.com/v1/domains" \
  -H "Authorization: Bearer $GPMT_TOKEN" | jq '.domains[] | .name'

# Daily traffic stats for a domain — last 30 days
for d in $(seq 1 30); do
  DATE=$(date -d "$d days ago" +%Y/%m/%d)
  Y=$(echo $DATE | cut -d/ -f1)
  M=$(echo $DATE | cut -d/ -f2)
  D=$(echo $DATE | cut -d/ -f3)
  curl -s "https://gmailpostmastertools.googleapis.com/v1/domains/${GPMT_DOMAIN}/trafficStats/${Y}${M}${D}" \
    -H "Authorization: Bearer $GPMT_TOKEN" \
    | jq '{date:"'"$DATE"'", spamRate, domainReputation, ipReputations: [.ipReputations[]?|{reputation,ipCount}], deliveryErrors: [.deliveryErrors[]?|{errorClass,errorType,errorRatio}], inboundEncryptionRatio, outboundEncryptionRatio, dkimSuccessRatio, spfSuccessRatio, dmarcSuccessRatio}'
done
```

Response fields:
- `spamRate` — float, fraction marked as spam by Gmail users. Target < 0.001 (0.10%). Alert at 0.001; pause at 0.003.
- `domainReputation` — `HIGH` / `MEDIUM` / `LOW` / `BAD` for whole domain.
- `ipReputations` — per-IP HIGH/MEDIUM/LOW/BAD with count of IPs at each tier.
- `deliveryErrors` — bounce categories + ratio (RATE_LIMITED, IP_LISTED, SPAM_RATE, etc.).
- `dkimSuccessRatio` / `spfSuccessRatio` / `dmarcSuccessRatio` — auth pass percent.
- `inboundEncryptionRatio` / `outboundEncryptionRatio` — TLS handshake success.

### Recipe 2: Daily polling cron + Slack alert

```bash
#!/bin/bash
# /etc/cron.daily/postmaster-check.sh
set -e

GPMT_TOKEN=$(gcloud auth application-default print-access-token --scopes=https://www.googleapis.com/auth/postmaster.readonly)
YESTERDAY=$(date -d "1 day ago" +%Y/%m/%d)
Y=$(date -d "1 day ago" +%Y)
M=$(date -d "1 day ago" +%m)
D=$(date -d "1 day ago" +%d)

RESPONSE=$(curl -s "https://gmailpostmastertools.googleapis.com/v1/domains/${GPMT_DOMAIN}/trafficStats/${Y}${M}${D}" \
  -H "Authorization: Bearer $GPMT_TOKEN")

SPAM_RATE=$(echo "$RESPONSE" | jq -r '.spamRate // 0')
DOMAIN_REP=$(echo "$RESPONSE" | jq -r '.domainReputation // "UNKNOWN"')

if (( $(echo "$SPAM_RATE > 0.001" | bc -l) )); then
  curl -X POST "$SLACK_WEBHOOK_URL" -H "Content-type: application/json" -d "{
    \"text\":\":rotating_light: Spam rate alert: ${SPAM_RATE} for ${GPMT_DOMAIN} on ${YESTERDAY}. Threshold 0.10%.\"
  }"
fi

if [ "$DOMAIN_REP" = "LOW" ] || [ "$DOMAIN_REP" = "BAD" ]; then
  curl -X POST "$SLACK_WEBHOOK_URL" -d "{
    \"text\":\":rotating_light: Domain reputation: ${DOMAIN_REP} on ${YESTERDAY}. Pause sends + investigate.\"
  }"
fi
```

### Recipe 3: Microsoft SNDS — daily CSV pull

```bash
# Authenticated CSV download
curl -s "https://sendersupport.olc.protection.outlook.com/snds/data.aspx?key=$SNDS_KEY" \
  -o snds-today.csv

# CSV columns: IP, Activity period start, Activity period end, RCPT commands, DATA commands, MessageRecipients, Filter Result, complaint Rate, Trap Hits, Sample HELO, Sample From
# Filter Result: GREEN / YELLOW / RED

# Aggregate by filter result
awk -F, 'NR>1 {count[$7]++} END {for (k in count) print k, count[k]}' snds-today.csv
# Expected:
# GREEN 5
# YELLOW 1
# RED 0

# Alert if any RED
RED_COUNT=$(awk -F, 'NR>1 && $7=="RED" {count++} END {print count+0}' snds-today.csv)
if [ "$RED_COUNT" -gt 0 ]; then
  curl -X POST "$SLACK_WEBHOOK_URL" -d "{\"text\":\":rotating_light: SNDS RED for ${RED_COUNT} IPs today\"}"
fi
```

### Recipe 4: SNDS Data + IPs detail

```bash
# Full data with IP details
curl -s "https://sendersupport.olc.protection.outlook.com/snds/ipStatus.aspx?key=$SNDS_KEY" \
  -o snds-ip-status.csv

# Columns: IP, From/To dates, Status (Normal/Some Problems/Many Problems/Severe Problems)
```

### Recipe 5: Yahoo FBL (Feedback Loop)

Yahoo sends complaint data via email to your FBL subscription:

```bash
# Sign up at https://senders.yahooinc.com/feedback-loop/
# Provide complaint receipt address, e.g., yahoo-fbl@brand.com
# Yahoo sends Abuse Reporting Format (ARF) emails per complaint
# Parse ARF emails to auto-suppress complainants
```

ARF email parser (Python):

```python
import email, re
def parse_arf(eml_bytes):
    msg = email.message_from_bytes(eml_bytes)
    for part in msg.walk():
        if part.get_content_type() == 'message/feedback-report':
            body = part.get_payload()
            m = re.search(r'Original-Rcpt-To:\s*(\S+)', body)
            return m.group(1) if m else None
```

### Recipe 6: AOL FBL + Comcast + Cox + others

Major US ISPs offer FBL at https://postmaster.aol.com/, http://feedback.comcast.net/, etc. Each requires per-domain registration. Track all enrollments centrally.

### Recipe 7: TLS-RPT — receive TLS handshake failure reports

Publish:
```
_smtp._tls.notify.brand.com.    TXT    "v=TLSRPTv1; rua=mailto:tls-rpt@brand.com"
```

Receive daily JSON reports (gzipped, attached):

```python
import gzip, json
def parse_tls_rpt(json_bytes):
    data = json.loads(gzip.decompress(json_bytes))
    for policy in data.get('policies', []):
        ftype = policy.get('policy', {}).get('policy-type')
        success = sum(s['total-successful-session-count'] for s in policy.get('summary', {}).values() if isinstance(s, dict))
        fail = sum(s['total-failure-session-count'] for s in policy.get('summary', {}).values() if isinstance(s, dict))
        print(f"{ftype}: success={success}, fail={fail}")
```

### Recipe 8: Per-IP reputation cross-reference

```bash
# Across all dedicated IPs, build reputation matrix
IPS=$(curl -s "https://gmailpostmastertools.googleapis.com/v1/domains/${GPMT_DOMAIN}/trafficStats/${YEAR}${MONTH}${DAY}" \
  -H "Authorization: Bearer $GPMT_TOKEN" | jq -r '.ipReputations[]? | "\(.reputation) \(.sampleIps[]?)"')

echo "$IPS" | sort | uniq -c
# Expected:
#   5 HIGH 198.51.100.10
#   3 HIGH 198.51.100.11
#   1 MEDIUM 198.51.100.12
```

### Recipe 9: Compare across receivers (Google vs Outlook vs Yahoo)

Build a daily dashboard:

| Date | Sender IP | Volume | Google rep | Google spam % | Outlook (SNDS) | Yahoo FBL |
|---|---|---|---|---|---|---|
| 2026-06-08 | 198.51.100.10 | 12,400 | HIGH | 0.04% | GREEN | 2 complaints |
| 2026-06-08 | 198.51.100.11 | 8,300 | MEDIUM | 0.12% | YELLOW | 5 complaints |

Visualize trends week over week.

### Recipe 10: Push reputation to PostgreSQL for analytics

```sql
CREATE TABLE postmaster_daily (
  date date,
  domain text,
  spam_rate numeric,
  domain_reputation text,
  ip_reputation_high integer,
  ip_reputation_medium integer,
  ip_reputation_low integer,
  ip_reputation_bad integer,
  dkim_success_ratio numeric,
  spf_success_ratio numeric,
  dmarc_success_ratio numeric,
  delivery_errors jsonb,
  PRIMARY KEY (date, domain)
);

CREATE INDEX ON postmaster_daily (date);
CREATE INDEX ON postmaster_daily (domain, date);
```

Daily upsert via psycopg2:

```python
import psycopg2
conn = psycopg2.connect(os.environ['POSTGRES_URL'])
with conn.cursor() as cur:
    cur.execute("""
        INSERT INTO postmaster_daily (date, domain, spam_rate, domain_reputation, ...)
        VALUES (%s, %s, %s, %s, ...)
        ON CONFLICT (date, domain) DO UPDATE SET
          spam_rate = EXCLUDED.spam_rate,
          domain_reputation = EXCLUDED.domain_reputation
    """, (date, domain, spam_rate, domain_rep, ...))
conn.commit()
```

## Examples

### Example 1: Set up cross-receiver reputation monitoring

**Goal:** daily reputation report covering Google + Microsoft + Yahoo.

**Steps:**

1. Enroll domain in Google Postmaster Tools (24h TXT verification).
2. Set up GCP service account + Postmaster API access (Setup above).
3. Enroll each sending IP in Microsoft SNDS (per-IP verification).
4. Sign up for Yahoo + AOL FBL.
5. Build daily cron (Recipe 2) — Postmaster pull → Postgres → Slack alert if spam_rate > 0.001.
6. Build SNDS daily CSV puller (Recipe 3).
7. Wire FBL emails to auto-suppression flow (Recipe 5).
8. Weekly digest email to ops team aggregating all three sources.

### Example 2: Investigate "Gmail delivery dropped 40% overnight"

**Goal:** identify cause and remediate.

**Steps:**

1. Pull yesterday's Postmaster stats (Recipe 1). Check:
   - `domainReputation` — drop a tier?
   - `spamRate` — spike?
   - `deliveryErrors` — RATE_LIMITED? SPAM_RATE? IP_LISTED?
2. If `IP_LISTED` — check Spamhaus / Barracuda / SORBS:
   ```bash
   curl "https://api.mxtoolbox.com/api/v1/lookup/blacklist/<ip>" -H "Authorization: $MXTOOLBOX_KEY"
   ```
3. If `SPAM_RATE` — last 7d trend; identify campaign that pushed over.
4. If `RATE_LIMITED` — check send velocity; throttle below Gmail's hint.
5. Pause aggressive sends to dormant cohorts.
6. Open ESP support ticket with details.

## Edge cases

- **Postmaster Tools requires domain verification** — 24h after adding TXT, you can authorize service accounts.
- **Postmaster Tools data lag** — yesterday's stats available the next day around UTC noon. Real-time monitoring not possible.
- **Postmaster requires minimum volume** — < 100 messages/day = no data (privacy threshold).
- **Postmaster `ipReputation` only on dedicated IPs** — shared pools don't show per-IP detail.
- **SNDS web UI lags 2-3 days behind reality** — API CSV is fresher.
- **SNDS RED is a critical signal** — start incident response immediately; Outlook is already throttling.
- **Yahoo FBL emails arrive minutes after complaint** — set up auto-process to suppress quickly.
- **Apple iCloud Postmaster has minimal data** — registration mostly enables abuse reporting.
- **Free GCP quota is generous for Postmaster API** — basic monitoring stays free; just don't loop with no rate limit.
- **OAuth scopes** — `postmaster.readonly` is sufficient; don't request more.
- **One service account per project** — Google rate-limits per project; if monitoring 100+ domains, you may need to shard projects.

## Sources

- [Google Postmaster Tools v2 API](https://developers.google.com/gmail/postmaster)
- [Google Postmaster UI](https://postmaster.google.com/)
- [Microsoft SNDS](https://sendersupport.olc.protection.outlook.com/snds/)
- [Yahoo Postmaster](https://senders.yahooinc.com/)
- [Yahoo FBL](https://senders.yahooinc.com/feedback-loop/)
- [Apple iCloud Postmaster](https://support.apple.com/en-us/HT204137)
- [Google sender guidelines](https://support.google.com/mail/answer/81126)
- [Yahoo sender best practices](https://senders.yahooinc.com/best-practices/)
- [RFC 5965 (ARF for FBL)](https://datatracker.ietf.org/doc/html/rfc5965)
- [RFC 8460 (TLS-RPT)](https://datatracker.ietf.org/doc/html/rfc8460)
