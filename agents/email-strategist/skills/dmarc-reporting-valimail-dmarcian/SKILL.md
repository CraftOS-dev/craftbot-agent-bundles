<!--
Source: dmarcian, Valimail, Postmark DMARC, EasyDMARC, ondmarc by Red Sift
RUA (aggregate) + RUF (forensic) report parsing. Sender alignment.
-->
# DMARC Reporting (Valimail / dmarcian / Postmark DMARC) — SKILL

Parse DMARC RUA (aggregate XML) and RUF (forensic) reports to identify misaligned senders, third-party tools mailing on your behalf, and spoofing attempts. Postmark DMARC is free for one domain; dmarcian, Valimail, EasyDMARC, ondmarc for multi-domain or enterprise.

## When to use

- "Analyze our DMARC reports — who's sending on our behalf?"
- "DMARC rollout stuck at p=none — what's not aligned?"
- "Identify the next sender to fix before advancing DMARC policy"
- "Get weekly DMARC digest for our ops team"
- "Compare RUA traffic week over week to spot new senders"
- "Forensic report on a spoofing attempt"

Pairs with `deliverability-deep-spf-dkim-dmarc-bimi-arc` skill (publish records) and `ip-reputation-google-postmaster-snds` (reputation signals).

## Setup

```bash
# parsedmarc — open-source, runs on your own infra
pipx install parsedmarc

# checkdmarc — comprehensive auth check
pipx install checkdmarc

# Or use hosted service — pick ONE based on tier:
#   Postmark DMARC      — free, 1 domain, weekly digest
#   dmarcian            — $40/mo+, multi-domain, deep alignment
#   Valimail            — enterprise, deep enforcement automation
#   EasyDMARC           — $30/mo+, modern UI
#   ondmarc (Red Sift)  — $99/mo+, threat intel
#   URI Ports           — free RUA viewer for self-hosted
```

Auth (per service):

```bash
export DMARCIAN_API_KEY="<dmarcian-key>"      # https://dmarcian.com → API tokens
export VALIMAIL_API_KEY="<valimail-key>"      # enterprise contract
export EASYDMARC_API_KEY="<easydmarc-key>"
export POSTMARK_DMARC_EMAIL="<your-id>@inbound.dmarc.postmarkapp.com"
```

## Common recipes

### Recipe 1: Set up DMARC reporting endpoint

Add `rua` (aggregate) and `ruf` (forensic) to your DMARC record:

```
_dmarc.brand.com.    TXT    "v=DMARC1; p=none; rua=mailto:rua@brand.com,mailto:<your-id>@inbound.dmarc.postmarkapp.com; ruf=mailto:ruf@brand.com; fo=1; adkim=r; aspf=r"
```

Multiple `mailto:` for parallel reporting (cross-checking dmarcian + Postmark, e.g.).

### Recipe 2: Postmark DMARC — set up free 1-domain monitoring

1. Sign up at https://dmarc.postmarkapp.com (free, no credit card).
2. Add domain — Postmark issues a unique reporting address: `<your-id>@inbound.dmarc.postmarkapp.com`.
3. Add to DMARC record (Recipe 1).
4. Wait 24-72h for first reports to arrive.
5. Login to weekly UI digest; receive email summaries.

### Recipe 3: dmarcian API — fetch reports programmatically

```bash
# Aggregate reports
curl "https://api.dmarcian.com/v1/domains/brand.com/reports/aggregate?from=2026-05-01&to=2026-06-01" \
  -H "Authorization: Bearer $DMARCIAN_API_KEY" | jq '.reports[] | {org_name, date_range, source_ips: [.records[].source_ip]}'

# Per-source IP breakdown
curl "https://api.dmarcian.com/v1/domains/brand.com/sources?from=2026-05-01&to=2026-06-01" \
  -H "Authorization: Bearer $DMARCIAN_API_KEY" | jq '.sources | sort_by(-.volume) | .[] | {ip, hostname, volume, alignment: {spf, dkim}, identity}'
```

### Recipe 4: parsedmarc — open-source self-hosted

```bash
# Parse a single XML (you have the .xml file from your inbox)
parsedmarc -o ./reports report.xml

# IMAP polling — auto-fetch reports from your DMARC mailbox
parsedmarc --imap-host imap.gmail.com --imap-user rua@brand.com --imap-password "$IMAP_PW" \
  --imap-reports-folder INBOX --delete --output reports/

# Elasticsearch sink for dashboarding
parsedmarc --elasticsearch-hosts http://localhost:9200 \
  --imap-host imap.gmail.com --imap-user rua@brand.com --imap-password "$IMAP_PW"
```

### Recipe 5: Parse a single RUA XML manually

A RUA report (gzipped, attached to email) looks like:

```xml
<feedback>
  <report_metadata>
    <org_name>google.com</org_name>
    <email>noreply-dmarc-support@google.com</email>
    <report_id>5234567890123</report_id>
    <date_range><begin>1717890000</begin><end>1717976400</end></date_range>
  </report_metadata>
  <policy_published>
    <domain>brand.com</domain>
    <adkim>r</adkim><aspf>r</aspf>
    <p>none</p><sp>none</sp><pct>100</pct>
  </policy_published>
  <record>
    <row>
      <source_ip>198.51.100.42</source_ip>
      <count>523</count>
      <policy_evaluated>
        <disposition>none</disposition>
        <dkim>pass</dkim>
        <spf>pass</spf>
      </policy_evaluated>
    </row>
    <identifiers>
      <header_from>brand.com</header_from>
    </identifiers>
    <auth_results>
      <dkim><domain>brand.com</domain><result>pass</result><selector>k1</selector></dkim>
      <spf><domain>brand.com</domain><result>pass</result></spf>
    </auth_results>
  </record>
  <record>
    <row>
      <source_ip>203.0.113.7</source_ip>
      <count>18</count>
      <policy_evaluated>
        <disposition>none</disposition>
        <dkim>fail</dkim>
        <spf>fail</spf>
      </policy_evaluated>
    </row>
    <identifiers><header_from>brand.com</header_from></identifiers>
    <auth_results>
      <dkim><domain>otherdomain.com</domain><result>none</result></dkim>
      <spf><domain>otherdomain.com</domain><result>none</result></spf>
    </auth_results>
  </record>
</feedback>
```

Parse with Python:

```python
import xml.etree.ElementTree as ET
from collections import defaultdict

tree = ET.parse('report.xml')
root = tree.getroot()

source_summary = defaultdict(lambda: {'count':0,'spf_pass':0,'dkim_pass':0,'identities':set()})

for record in root.findall('record'):
    ip = record.findtext('row/source_ip')
    count = int(record.findtext('row/count'))
    spf_eval = record.findtext('row/policy_evaluated/spf')
    dkim_eval = record.findtext('row/policy_evaluated/dkim')

    source_summary[ip]['count'] += count
    if spf_eval == 'pass':  source_summary[ip]['spf_pass']  += count
    if dkim_eval == 'pass': source_summary[ip]['dkim_pass'] += count

    for auth in record.findall('auth_results/dkim'):
        source_summary[ip]['identities'].add(auth.findtext('domain'))

for ip, s in sorted(source_summary.items(), key=lambda kv: -kv[1]['count']):
    print(f"{ip}: {s['count']} msgs, SPF pass {s['spf_pass']}, DKIM pass {s['dkim_pass']}, identities {s['identities']}")
```

### Recipe 6: Identify sender from source IP

```bash
# Reverse DNS
dig +short -x 198.51.100.42

# WHOIS (org owner)
whois 198.51.100.42 | grep -E '(OrgName|netname|owner)'

# Or use IPinfo
curl "https://ipinfo.io/198.51.100.42" -H "Authorization: Bearer $IPINFO_TOKEN"
```

Common IP ranges:
| Range | Sender |
|---|---|
| 198.61.254.0/22, 168.245.0.0/16 | SendGrid |
| 50.31.32.0/19 | Mailgun (US) |
| 161.0.0.0/8 | Mailchimp |
| 199.122.0.0/16 | Salesforce Marketing Cloud |
| 138.91.0.0/16 | Klaviyo |
| 23.83.0.0/16 | HubSpot |
| 67.231.144.0/20 | Postmark |
| 52.0.0.0/8 | AWS SES (multiple ranges) |
| 192.124.249.0/24 | Stripe email |
| 64.18.0.0/20 | Google Workspace |

### Recipe 7: Per-source remediation matrix

Build a tracking doc:

| Source IP | Hostname | Identity (DKIM) | Volume | SPF aligned | DKIM aligned | Action |
|---|---|---|---|---|---|---|
| 138.91.10.5 | klaviyo.com | brand.com | 5,234 | pass | pass | OK |
| 192.124.249.10 | stripe.com | stripe.com | 234 | fail | fail | Subdomain delegation: stripe.brand.com CNAME stripe |
| 161.0.5.42 | mailchimp.com | mailchimp.com | 89 | fail | fail | Add Mailchimp SPF include OR remove legacy account |
| 198.51.100.99 | (unknown — Russia) | - | 12 | fail | fail | Spoofing — leave for DMARC enforcement |

### Recipe 8: Weekly digest report (custom)

```python
import parsedmarc
from glob import glob

reports = []
for f in glob('reports/*.xml'):
    r = parsedmarc.parse_aggregate_report_file(f)
    reports.append(r)

# Aggregate
total_messages = sum(rec['count'] for r in reports for rec in r['records'])
aligned = sum(rec['count'] for r in reports for rec in r['records']
              if rec['policy_evaluated']['dkim'] == 'pass'
              and rec['policy_evaluated']['spf'] == 'pass')

print(f"Total: {total_messages}, Aligned: {aligned} ({aligned/total_messages:.1%})")

# Per-source
sources = {}
for r in reports:
    for rec in r['records']:
        ip = rec['source']['ip_address']
        sources.setdefault(ip, {'count':0,'aligned':0,'orgs':set()})
        sources[ip]['count'] += rec['count']
        if rec['policy_evaluated']['dkim'] == 'pass' and rec['policy_evaluated']['spf'] == 'pass':
            sources[ip]['aligned'] += rec['count']
        for ident in rec.get('identifiers',{}).values():
            sources[ip]['orgs'].add(ident)

for ip, s in sorted(sources.items(), key=lambda x: -x[1]['count'])[:20]:
    pct = s['aligned']/s['count'] if s['count'] else 0
    print(f"{ip:20s} {s['count']:6d} msgs  {pct:.0%} aligned  {s['orgs']}")
```

### Recipe 9: Valimail Monitor — enterprise multi-domain

```bash
# List all monitored domains
curl "https://api.valimail.com/v1/monitor/domains" \
  -H "X-Api-Key: $VALIMAIL_API_KEY" | jq '.'

# Get senders for a domain
curl "https://api.valimail.com/v1/monitor/domains/brand.com/senders?from=2026-05-01&to=2026-06-01" \
  -H "X-Api-Key: $VALIMAIL_API_KEY" | jq '.senders | sort_by(-.volume) | .[] | {sender_name, sender_domain, volume, dmarc_pct_aligned, action_required}'
```

### Recipe 10: EasyDMARC + ondmarc

```bash
# EasyDMARC
curl "https://api.easydmarc.com/v3/domains/brand.com/reports?period=last_week" \
  -H "Authorization: Bearer $EASYDMARC_API_KEY" | jq '.data'

# ondmarc (Red Sift)
curl "https://api.redsift.com/v1/ondmarc/brand.com/reports" \
  -H "X-API-Key: $ONDMARC_KEY" | jq '.'
```

### Recipe 11: RUF (forensic) report — individual failure deep dive

RUF is per-message (full or partial), more privacy-sensitive. Google does NOT send RUF; Yahoo, Microsoft, AOL do.

```xml
<feedback>
  <version>0.1</version>
  <report_metadata>
    <feedback_type>auth-failure</feedback_type>
    <user_agent>Yahoo!-Mail-Feedback/2.0</user_agent>
    <auth-failure>dmarc</auth-failure>
  </report_metadata>
  <delivery-result>policy</delivery-result>
  <source>
    <ip-address>203.0.113.99</ip-address>
  </source>
  <message>
    <from>spoofed@brand.com</from>
    <to>victim@yahoo.com</to>
    <subject>Urgent: Update payment</subject>
    ...
  </message>
</feedback>
```

Use RUF to forensically confirm spoofing patterns and report attackers (abuse contacts via WHOIS).

## Examples

### Example 1: Diagnose stuck-at-p=none rollout

**Goal:** identify which legitimate sender is failing alignment so we can fix and advance DMARC.

**Steps:**

1. Set up Postmark DMARC (free) → publish updated record (Recipe 2).
2. Wait 7 days for reports to flow.
3. Pull all source IPs > 50 messages, classify each (Recipes 5-7).
4. For each unaligned legitimate sender, document the fix:
   - Stripe email failing alignment → enable Stripe's "branded email" feature; add CNAME for Stripe DKIM.
   - Legacy Mailchimp account still sending → either properly delegate or kill the account.
5. Implement fixes. Wait another week. Verify alignment ≥ 95%.
6. Advance DMARC to `p=quarantine; pct=10`.

### Example 2: Detect spoofing attempt

**Goal:** verify if recent customer complaints are due to a phishing campaign impersonating us.

**Steps:**

1. Pull last 30d RUA: filter source IPs with `disposition=quarantine|reject` AND not in known-good list.
2. For each suspicious IP:
   ```bash
   whois <ip> | grep -iE 'org|country|abuse'
   dig +short -x <ip>
   ```
3. Cross-check Yahoo / Microsoft RUF reports for sample messages.
4. Report to abuse@<ISP> + add IP to your own block list at WAF if reflected.
5. Advance DMARC to `p=reject` immediately if not already — this hardens future spoofing.

## Edge cases

- **DMARC reports lag** — Google sends daily after UTC midnight; some receivers (Microsoft) weekly. Wait 7-14 days before judging "clean."
- **RUF privacy controls** — many receivers (especially in EU) do not send RUF to avoid GDPR concerns. Don't expect Google or major EU receivers.
- **`fo=` flag interpretations vary** — `fo=1` (any auth failure) is most informative but generates more reports. `fo=0` (both SPF and DKIM fail) is minimal.
- **Multiple `rua` mailboxes** — RFC permits up to 2 per record. Use both for redundancy (dmarcian + Postmark, e.g.).
- **Reports often gzipped or zipped** — tools auto-handle; manual parsing requires `gunzip` first.
- **Report parsing tools handle XML schema drift poorly** — Microsoft has a slightly different schema than Google. `parsedmarc` handles both; rolling your own may break.
- **Forwarders generate noise** — RUA reports show forwarders as `source_ip` with `from=brand.com`. Often SPF fails (forwarder didn't rewrite envelope-from) but DKIM passes if signature intact. ARC helps preserve original auth.
- **High-volume domains** can receive 100+ RUA reports per day. Auto-archive + machine-parse; don't try to read manually.
- **Privacy: don't share RUA externally** — reports identify your senders + customers (limited PII in headers).

## Sources

- [dmarcian API](https://dmarcian.com/api/)
- [Valimail DMARC Monitor](https://www.valimail.com/dmarc-monitor/)
- [Postmark DMARC](https://dmarc.postmarkapp.com/)
- [EasyDMARC API](https://easydmarc.com/docs/)
- [ondmarc by Red Sift](https://redsift.com/products/ondmarc)
- [parsedmarc](https://github.com/domainaware/parsedmarc)
- [URI Ports DMARC viewer](https://uriports.com/dmarc-viewer/)
- [RFC 7489 (DMARC)](https://datatracker.ietf.org/doc/html/rfc7489)
- [RFC 6591 (RUF)](https://datatracker.ietf.org/doc/html/rfc6591)
