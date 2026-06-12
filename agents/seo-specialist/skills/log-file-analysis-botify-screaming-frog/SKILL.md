<!--
Source: https://www.screamingfrog.co.uk/log-file-analyser/
Source: https://www.botify.com/blog/log-analyzer
Source: https://www.oncrawl.com/oncrawl-log-analyzer/
Depth: enterprise log file analysis (Googlebot reverse-DNS, crawl-budget, bot classification)
-->
# Log File Analysis — Botify / OnCrawl / Screaming Frog Log Analyser

## When to use

Reach for this skill when the user asks for: "log file analysis", "crawl budget audit", "Googlebot behavior", "is Googlebot fake", "bot verification", "crawl-budget waste", "Apache log SEO", "Nginx access log Googlebot", "cloudflare log SEO". This is the depth specialist — beyond marketing-agent's "check crawl stats in GSC". Covers tool tier selection (SF Log Analyser SMB / OnCrawl mid / Botify enterprise), reverse-DNS Googlebot verification (mandatory — fake Googlebots common), per-template crawl-budget allocation, crawl-waste identification (parameter URLs, 4xx, redirect chains).

## Setup

```bash
# Screaming Frog Log File Analyser ($199/yr SMB)
# Download from screamingfrog.co.uk/log-file-analyser/
# CLI binary: ScreamingFrogLogFileAnalyser (Windows .exe / macOS .app / Linux not officially supported but works via Wine)
screamingfrogloganalyser --help

# OnCrawl ($169+/mo mid-market) — REST API only
export ONCRAWL_API_KEY="<from app.oncrawl.com/account/api>"

# Botify (enterprise — call sales)
export BOTIFY_API_KEY="<from app.botify.com/settings/api>"

# Raw log parsing (no tool) — Python
pip install pandas user-agents
```

Auth / pricing:
- `SF_LOG_LICENSE` — Screaming Frog Log Analyser, $199/yr, single seat
- `ONCRAWL_API_KEY` — OnCrawl Bot Analyzer add-on; entry $169/mo
- `BOTIFY_API_KEY` — enterprise; 5-figure annual
- Raw log Python — free

## Common recipes

### Recipe 1: Screaming Frog Log Analyser CLI (SMB ≤1M lines/day)
```bash
# Import logs into project
screamingfrogloganalyser \
  --import-logs ./apache-logs/ \
  --project-name "client-q3-logs" \
  --enable-bot-verification true \
  --crawl-data-import ./sf-crawl-out/internal_all.csv \
  --export-tabs "Overview,Verification Status,URLs:All,Bot Activity:All,Response Codes:All,Crawl Budget:Waste" \
  --output-folder ./log-analysis-out
```
Joins log entries with prior SF crawl (URL inventory + status codes) for crawl-vs-log gap analysis.

### Recipe 2: Googlebot reverse-DNS verification (mandatory)
```python
# Spoofed Googlebots are common — verify EVERY Googlebot hit
import socket

def verify_googlebot(ip):
    try:
        host = socket.gethostbyaddr(ip)[0]
        # Forward DNS confirmation: host must resolve back to original IP
        forward_ip = socket.gethostbyname(host)
        is_google = host.endswith('.googlebot.com') or host.endswith('.google.com')
        return is_google and forward_ip == ip
    except (socket.herror, socket.gaierror):
        return False

# Apply across all log rows
import pandas as pd
logs = pd.read_csv('access.log', sep=' ', names=['ip','user','ts','request','status','size','referer','ua'])
logs['claims_googlebot'] = logs['ua'].str.contains('Googlebot', case=False, na=False)
logs['verified_googlebot'] = logs[logs['claims_googlebot']]['ip'].apply(verify_googlebot)

fake_pct = (~logs[logs['claims_googlebot']]['verified_googlebot']).mean()
print(f"Fake Googlebot %: {fake_pct:.1%}")
```
SF Log Analyser does this automatically when `--enable-bot-verification true`.

### Recipe 3: Crawl-budget allocation per template
```python
import pandas as pd
import re

# Classify URLs by template via regex on path
def classify_template(url):
    path = url.split('?')[0]
    if re.match(r'.*/products/', path): return 'product'
    if re.match(r'.*/category/', path): return 'category'
    if re.match(r'.*/blog/', path): return 'blog'
    if path.endswith('/'): return 'homepage' if path == '/' else 'other'
    return 'other'

logs['template'] = logs['url'].apply(classify_template)

# Googlebot hits per template per day
googlebot = logs[logs['verified_googlebot'] == True]
template_hits = googlebot.groupby('template').size().sort_values(ascending=False)

# Crawl budget % per template
total = template_hits.sum()
template_pct = (template_hits / total * 100).round(1)
print("Crawl budget allocation:")
print(template_pct)

# Cross with GSC clicks per template (via Suganthan GSC) for value-vs-crawl gap analysis
```

### Recipe 4: Crawl-waste identification
```python
# Parameter URL waste
param_urls = googlebot[googlebot['url'].str.contains(r'\?', regex=True)]
print(f"Parameter URL hits: {len(param_urls)} ({len(param_urls)/len(googlebot)*100:.1f}% of crawl)")

# Top parameter patterns
import urllib.parse
param_urls['params'] = param_urls['url'].apply(
    lambda u: tuple(sorted(urllib.parse.parse_qs(u.split('?',1)[1] if '?' in u else '').keys()))
)
print(param_urls['params'].value_counts().head(10))

# 4xx crawl waste
status_4xx = googlebot[googlebot['status'].astype(int).between(400, 499)]
print(f"4xx hits: {len(status_4xx)} (Googlebot revisiting dead URLs)")
print(status_4xx['url'].value_counts().head(20))

# Redirect chain detection (multiple 301 hits to same destination)
status_3xx = googlebot[googlebot['status'].astype(int).between(300, 399)]
print(f"3xx hits: {len(status_3xx)} (each is a chain hop)")
```

### Recipe 5: OnCrawl Bot Analyzer REST API
```bash
# Trigger analysis
curl -X POST "https://app.oncrawl.com/api/v2/projects/<project-id>/crawls" \
  -H "Authorization: Bearer $ONCRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"q3-logs-import",
    "log_monitoring":true,
    "log_files":[{"url":"s3://logs-bucket/2026-06/*.log","format":"apache_combined"}]
  }'

# Pull bot data
curl "https://app.oncrawl.com/api/v2/projects/<project-id>/crawls/<crawl-id>/oql/urls?fields=url,bot.google.hits,bot.bing.hits,bot.openai.hits,bot.anthropic.hits&limit=10000" \
  -H "Authorization: Bearer $ONCRAWL_API_KEY"
```
OnCrawl auto-classifies AI training bots (GPTBot, Claude-Web, Google-Extended) separately.

### Recipe 6: Botify enterprise log query
```bash
# Botify uses BQL (Botify Query Language)
curl -X POST "https://api.botify.com/v1/projects/<slug>/queries" \
  -H "Authorization: Token $BOTIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "collections":["crawl_<analysis-id>","logs_<analysis-id>"],
    "query":{
      "dimensions":["url","segments.pagetype.value"],
      "metrics":["count_urls","logs.google.requests.nb","crawls.google.has_been_crawled","strategic.is_strategic"],
      "filters":{"and":[{"field":"logs.google.requests.nb","predicate":"gt","value":0}]},
      "sort":[{"metric":"logs.google.requests.nb","order":"desc"}]
    },
    "size":1000
  }'
```

### Recipe 7: AI training bot tracking (GPTBot, Claude-Web, Google-Extended)
```python
# 2024-2026 emergence — recipients may want to allow / disallow AI training bots
AI_BOTS = {
    'GPTBot': r'GPTBot/',
    'Claude-Web': r'Claude-Web/',
    'ClaudeBot': r'ClaudeBot/',
    'anthropic-ai': r'anthropic-ai/',
    'Google-Extended': r'Google-Extended',  # blocks Bard/Vertex training
    'CCBot': r'CCBot/',  # Common Crawl
    'Bytespider': r'Bytespider/',  # ByteDance
    'PerplexityBot': r'PerplexityBot/',
}

for name, pattern in AI_BOTS.items():
    matches = logs[logs['ua'].str.contains(pattern, regex=True, na=False)]
    print(f"{name}: {len(matches):,} hits, {matches['url'].nunique():,} unique URLs")
```
For AEO push: ALLOW these bots in robots.txt. For training-opt-out: DISALLOW.

### Recipe 8: Crawl velocity calculation
```python
# Googlebot crawl velocity (URLs/day)
googlebot['date'] = pd.to_datetime(googlebot['ts']).dt.date
daily_velocity = googlebot.groupby('date').size()
print(f"Avg Googlebot velocity: {daily_velocity.mean():.0f} URLs/day")
print(f"Peak: {daily_velocity.max():.0f}, Trough: {daily_velocity.min():.0f}")

# Compare to GSC Crawl Stats (Settings > Crawl Stats in Search Console)
# Diff suggests bot spoofing OR new bot variants not classified
```

### Recipe 9: Apache + Nginx + CloudFront + Cloudflare format parsing
```bash
# Apache combined log format
%h %l %u %t "%r" %>s %O "%{Referer}i" "%{User-Agent}i"

# Nginx default
$remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"

# CloudFront — needs CSV parsing
date,time,x-edge-location,sc-bytes,c-ip,cs-method,cs(Host),cs-uri-stem,sc-status,...

# Cloudflare — JSON Logpush
{"ClientIP":"...","EdgeStartTimestamp":"...","ClientRequestURI":"...","ClientRequestUserAgent":"...","EdgeResponseStatus":...,...}

# Python parser per format
import pandas as pd
def parse_apache(file):
    pattern = r'(\S+) (\S+) (\S+) \[([^\]]+)\] "([^"]+)" (\d+) (\S+) "([^"]*)" "([^"]*)"'
    return pd.read_csv(file, sep='|', names=['raw']).assign(
        # apply regex extraction
    )
```

### Recipe 10: Pipe to ELK or Splunk for custom enterprise analysis
```bash
# Filebeat → Logstash → Elasticsearch → Kibana
# filebeat.yml
filebeat.inputs:
  - type: log
    paths: ['/var/log/nginx/access.log']
    fields:
      log_type: 'web-access'

# Logstash filter for Googlebot enrichment
filter {
  grok { match => { "message" => "%{COMBINEDAPACHELOG}" } }
  if [agent] =~ /Googlebot/ {
    dns { reverse => [ "clientip" ] target => "host" }
    mutate { add_field => { "verified_googlebot" => "%{[host]} matches googlebot.com" } }
  }
}
```

## Examples

### Example 1: SMB site (200K monthly Googlebot hits)
**Goal:** Identify crawl-budget waste; quantify Googlebot value per template.

**Steps:**
1. Pull 30 days Apache logs from server.
2. Recipe 1: SF Log Analyser import with crawl join.
3. Recipe 2: SF auto-verifies Googlebot; manual spot-check 5% sample.
4. Recipe 3: per-template crawl % vs GSC clicks % gap analysis.
5. Recipe 4: crawl-waste — parameter URLs, 4xx, redirect chains.
6. Output recommendations: robots.txt parameter rules, 410 noindex on dead URLs, redirect chain compression.

**Result:** Audit report with actionable robots.txt + redirect cleanup.

### Example 2: Enterprise programmatic SEO (10M URL site, 5M Googlebot hits/mo)
**Goal:** Crawl-budget reallocation toward high-value templates.

**Steps:**
1. Logs land in S3 via CloudFront Logpush.
2. Recipe 6: Botify BQL query joining crawl + log + strategic flag.
3. Identify templates with high crawl % but low strategic-page-count % → de-prioritize via robots.txt or noindex.
4. Identify templates with low crawl % but high strategic % → boost via internal linking + sitemap priority.
5. Re-measure 30 days later.

**Result:** Strategic crawl share lift from 35% to 65%.

### Example 3: Negative-SEO attack via fake Googlebot
**Goal:** Suspected bot scraping using fake Googlebot UA.

**Steps:**
1. Recipe 2: reverse-DNS on all Googlebot-UA hits.
2. If `fake_pct > 5%`: investigate IPs.
3. Add fake IPs to firewall block list (Cloudflare WAF, AWS WAF).
4. Re-verify clean log stream after 7 days.

**Result:** Reduced server load + cleaner crawl-stat reporting.

## Edge cases / gotchas

- **Spoofed Googlebot is COMMON** — always reverse-DNS verify. SF Log Analyser does it automatically; raw Python parsing needs Recipe 2.
- **Forward-DNS check mandatory** — `gethostbyaddr` alone can be tricked via PTR record manipulation. Add `gethostbyname` round-trip.
- **Googlebot crawl velocity != crawl budget budget** — Google's "crawl budget" is host-capacity-driven. Increasing velocity = serve faster, return fewer 5xx, fewer 429s.
- **`.googlebot.com` vs `.google.com` hostnames** — both are Google-owned; `.googlebot.com` for desktop+smartphone bots, `.google.com` for AdsBot and Mobile-Friendly Test.
- **AI training bot UA strings evolve** — Anthropic added `ClaudeBot/1.0` separately from `Claude-Web/1.0`; check https://darkvisitors.com periodically.
- **Cloudflare logs cost** — Logpush to S3 costs $0.05/GB; Enterprise plan only.
- **CloudFront standard logs delayed 30-60 min** — real-time logs need Kinesis + extra cost.
- **Apache `LogFormat` customization** — many sites have non-standard log formats; verify config before parsing.
- **Log retention 30-90 days typical** — extract before rotation. Set up daily incremental import.
- **SF Log Analyser Windows-only by default** — macOS works; Linux via Wine or skip in favor of OnCrawl/Botify or raw Python.
- **OnCrawl + Botify slow ingestion** — 100M lines takes hours.
- **Privacy / GDPR** — IPs are PII in EU. Anonymize after Googlebot verification (truncate last octet).

## Sources

- [Screaming Frog Log File Analyser](https://www.screamingfrog.co.uk/log-file-analyser/)
- [Screaming Frog log analyser docs](https://www.screamingfrog.co.uk/log-file-analyser/user-guide/)
- [Botify log analyzer overview](https://www.botify.com/blog/log-analyzer)
- [Botify BQL API](https://developers.botify.com/reference/queries-overview)
- [OnCrawl Log Analyzer](https://www.oncrawl.com/oncrawl-log-analyzer/)
- [Google Search Central — verifying Googlebot](https://developers.google.com/search/docs/crawling-indexing/verifying-googlebot)
- [Google Search Central — crawler user agents](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers)
- [Google — Google-Extended for AI training](https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers#google-extended)
- [DarkVisitors AI bot directory](https://darkvisitors.com/agents)
