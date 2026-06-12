<!--
Source: https://pitchbox.com/api/
Source: https://respona.com/api
Source: https://www.buzzstream.com/api/
Source: https://ahrefs.com/blog/broken-link-building/
Depth: outreach automation + broken-link reclamation + unlinked mentions + digital PR
-->
# Link Building Outreach — Pitchbox / Respona / BuzzStream

## When to use

Reach for this skill when the user asks for: "link building", "outreach automation", "broken link reclamation", "unlinked brand mention conversion", "digital PR", "Pitchbox setup", "Respona campaign", "BuzzStream outreach", "guest post outreach", "link velocity check". This is the depth specialist for white-hat link acquisition — covers prospect sourcing via Ahrefs (broken backlinks, unlinked mentions, competitor backlinks), outreach tool selection by volume (BuzzStream <50/mo / Respona <100/mo / Pitchbox ≥100/mo), template patterns, link-velocity anomaly detection.

## Setup

```bash
# Pick ONE outreach tool based on volume:

# Pitchbox — full automation, $499+/mo, for ≥100 outreaches/mo
export PITCHBOX_API_KEY="<from app.pitchbox.com/settings/api>"

# Respona — combined prospecting + outreach, $399+/mo, for ≥50/mo
export RESPONA_API_KEY="<from app.respona.com/settings/api>"

# BuzzStream — relationship management, $24+/mo, for <50/mo
export BUZZSTREAM_API_KEY="<from app.buzzstream.com/api>"

# Ahrefs for prospect sourcing
export AHREFS_MCP_TOKEN="<oauth-token>"

# gmail-mcp for direct outreach (lowest volume)
```

Auth/pricing:
- `PITCHBOX_API_KEY` — Pitchbox; reach out to https://pitchbox.com for trial
- `RESPONA_API_KEY` — Respona dashboard
- `BUZZSTREAM_API_KEY` — BuzzStream API key
- `AHREFS_MCP_TOKEN` — Lite plan minimum

## Common recipes

### Recipe 1: Broken-link reclamation prospect sourcing
```bash
# Links you used to have that are now 404
mcp tool ahrefs.broken_backlinks_lost \
  --target "yourbrand.com" \
  --mode "domain" \
  --limit 1000 \
  --filter '{"first_seen":{"after":"2024-01-01"},"ref_domain_dr":{">=":20}}' > broken_lost.json
```
Filter: DR ≥ 20 keeps quality prospects; date filter excludes ancient links.

### Recipe 2: Competitor broken backlinks (offer your equivalent)
```bash
mcp tool ahrefs.broken_backlinks \
  --target "competitor.com" \
  --mode "domain" \
  --limit 1000 \
  --filter '{"ref_domain_dr":{">=":30}}' > comp_broken.json
```
For each: identify your equivalent page → outreach offering replacement.

### Recipe 3: Unlinked brand mentions
```bash
mcp tool ahrefs.content_explorer \
  --query "\"yourbrand\"" \
  --filter '{"links_to":"-yourbrand.com","language":"en","domain_rating":">30","mentions_per_target":">=1"}' \
  --limit 500 > unlinked_mentions.json
```

### Recipe 4: Resource page prospects via Brave Search
```bash
# Brave for resource-page sourcing (free, no Ahrefs needed)
curl "https://api.search.brave.com/res/v1/web/search?q=%22marketing+automation%22+%22resources%22" \
  -H "X-Subscription-Token: $BRAVE_API_KEY"

# Also try:
# "[topic]" + "useful links"
# "[topic]" + "best of"
# "[topic]" + "recommended tools"
```

### Recipe 5: Pitchbox campaign creation
```bash
# Import contacts
curl -X POST https://app.pitchbox.com/api/v1/contacts/import \
  -H "Authorization: Bearer $PITCHBOX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id":"<campaign-id>",
    "contacts":[
      {"email":"author@site.com","first_name":"Jane","website":"https://site.com","custom_fields":{"broken_url":"https://site.com/old-page","dead_link":"https://yourbrand.com/old-resource"}},
      ...
    ]
  }'

# Create campaign with templates + sequence
curl -X POST https://app.pitchbox.com/api/v1/campaigns \
  -H "Authorization: Bearer $PITCHBOX_API_KEY" \
  -d '{
    "name":"Broken Link Reclamation Q3",
    "sequence":[
      {"step":1,"delay_days":0,"subject":"Quick FYI — {{first_name}}, broken link","template":"<bla bla>"},
      {"step":2,"delay_days":4,"subject":"Following up on link replacement","template":"<bla bla>"},
      {"step":3,"delay_days":10,"subject":"Closing the loop on {{broken_url}}","template":"<bla bla>"}
    ]
  }'
```

### Recipe 6: Respona link-builder-in-a-box
```bash
# Respona combines prospecting + sequences
curl -X POST https://app.respona.com/api/v1/campaigns \
  -H "Authorization: Bearer $RESPONA_API_KEY" \
  -d '{
    "name":"Unlinked Mention Conversion Q3",
    "search_query":"\"yourbrand\" -site:yourbrand.com",
    "filters":{"min_dr":30,"language":"en"},
    "outreach":{
      "template_id":"unlinked-mention-conversion",
      "follow_ups":2
    }
  }'
```

### Recipe 7: BuzzStream relationship management
```bash
# Add prospect to BuzzStream project
curl -X POST https://api.buzzstream.com/api/v1/contacts \
  -H "Authorization: Bearer $BUZZSTREAM_API_KEY" \
  -d '{
    "project_id":"<project-id>",
    "first_name":"Jane",
    "email":"jane@site.com",
    "website":"https://site.com",
    "tags":["broken-link","q3-2026"]
  }'
```

### Recipe 8: Direct gmail-mcp outreach (≤20/mo)
```python
# When volume is too low for paid tool
prospects = json.load(open('broken_lost.json'))

for p in prospects[:20]:
    body = f"""Hi {p.get('author_name','there')},

I was reading {p['source_url']} and noticed the link to {p['target_url']} returns a 404.

We have a current resource on the same topic at {p['our_replacement_url']} — feel free to update if useful.

No worries either way — just thought you'd want to know.

Thanks,
{your_name}
"""

    mcp.call('gmail.send',
        to=p['contact_email'],
        subject=f"Quick FYI - your link to {p['target_url']} is broken",
        body=body,
        labels=['outreach','broken-link-q3']
    )
```

### Recipe 9: Outreach templates (white-hat only)

**Broken-link reclamation:**
```
Subject: Quick FYI — your link to {topic} is broken

Hi {first_name},

I was reading {source_url} and noticed the link to {broken_url} returns a 404.

We have a current resource at {our_replacement_url} that covers the same topic if that's useful.

No worries either way — just thought you'd want to know.

Thanks,
{your_name}
```

**Unlinked mention conversion:**
```
Subject: Thanks for the mention!

Hi {first_name},

Saw the mention of {brand_name} on your {source_url} — really appreciated it.

If you wanted to link, our canonical URL is {brand_url}.

Either way, thanks for the kind words.

{your_name}
```

**Digital PR pitch (with original data):**
```
Subject: Original data on {topic} — exclusive for {publication}

Hi {first_name},

I just finished analyzing {sample_size} {data_points} on {topic}.

Top finding: {surprising_stat}.

Happy to share the full dataset + give you exclusive access before publishing more widely. Let me know if useful for an upcoming piece.

{your_name}
```

**Resource page pitch:**
```
Subject: Resource for your {topic} list

Hi {first_name},

I noticed your {resource_page_url} curates {topic} resources.

I recently published {our_resource_url} which {brief_value_prop_in_one_line}.

If it'd fit, I'd love to be included. Either way, great resource — bookmarked!

{your_name}
```

### Recipe 10: Reply parsing via gmail-mcp
```python
# After outreach, classify replies via gmail-mcp polling
import re

POSITIVE_PATTERNS = [r'will add', r'link added', r'done', r'updated', r'happy to', r'will include']
NEGATIVE_PATTERNS = [r'not interested', r'no thanks', r'remove me', r'unsubscribe', r"can't"]

def classify_reply(email_body):
    body_lower = email_body.lower()
    if any(re.search(p, body_lower) for p in POSITIVE_PATTERNS):
        return 'POSITIVE'
    if any(re.search(p, body_lower) for p in NEGATIVE_PATTERNS):
        return 'NEGATIVE'
    return 'NEUTRAL'

# Daily cron
replies = mcp.call('gmail.search', query='label:outreach-broken-link-q3 newer_than:1d is:reply')
for reply in replies:
    classification = classify_reply(reply['body'])
    notion.update_page(prospect_id=reply['thread_id'], status=classification)
```

### Recipe 11: Link verification (post-outreach)
```python
# Check if the linking site actually added the link
import requests
from bs4 import BeautifulSoup

def verify_link_added(linking_url, our_url):
    r = requests.get(linking_url, timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = [a.get('href') for a in soup.find_all('a', href=True)]
    return our_url in links or any(our_url in link for link in links)

# Run weekly across positive-reply prospects
for prospect in positive_reply_prospects:
    if verify_link_added(prospect['source_url'], prospect['our_url']):
        notion.update(prospect_id=prospect['id'], status='LINK_LIVE')
```

### Recipe 12: Link velocity monitoring (anomaly detection)
```python
# Monitor new referring domains; alert on anomalies
import datetime, pandas as pd

# Daily Ahrefs poll
new_rds = mcp.call('ahrefs.referring_domains_new',
    target='yourbrand.com',
    since=str(datetime.date.today() - datetime.timedelta(days=7))
)

# Anomaly detection
baseline_velocity = 8  # RDs/week average
current_velocity = len(new_rds)

if current_velocity > baseline_velocity * 10:
    # Possible negative-SEO attack
    spam_tlds = ['.xyz','.top','.icu','.cn']
    spam_rds = [r for r in new_rds if any(r['domain'].endswith(t) for t in spam_tlds)]
    avg_dr = sum(r['dr'] for r in new_rds) / len(new_rds)

    if avg_dr < 10 and len(spam_rds) > 5:
        gmail.send(to='seo-team@example.com',
            subject='ALERT: Possible negative-SEO attack',
            body=f'Velocity {current_velocity} RDs (10× baseline), avg DR {avg_dr:.1f}, {len(spam_rds)} spam-TLD domains.')
```

## Examples

### Example 1: Quarterly broken-link reclamation campaign
**Goal:** Reclaim 30-50 links from broken backlinks over 90 days.

**Steps:**
1. Recipe 1: pull broken backlinks lost (DR ≥ 20, last 12 months).
2. For each broken target URL: identify your closest live replacement page.
3. Find contact email per linking domain (Hunter.io / Apollo / manual).
4. Recipe 5 (Pitchbox) or Recipe 8 (gmail direct).
5. Outreach with template (Recipe 9 broken-link).
6. Recipe 10: reply classification + Notion CRM.
7. Recipe 11: post-90-day link verification.

**Result:** Typical 10-20% conversion rate on broken-link reclamation = 30-100 reclaimed links from 300-500 prospects.

### Example 2: Unlinked brand mention conversion
**Goal:** Convert 20-30 unlinked mentions to linked mentions.

**Steps:**
1. Recipe 3: pull unlinked mentions (DR ≥ 30, English).
2. Confirm mentions via Firecrawl scrape (filter false positives).
3. Recipe 8 (gmail direct) with Recipe 9 unlinked-mention template.
4. Recipe 11: verification.

**Result:** 15-25% conversion rate; high ROI per outreach.

### Example 3: Digital PR campaign with original data study
**Goal:** Earn 20+ links from a "We analyzed 10K [data point] on [topic]" study.

**Steps:**
1. Conduct original study (in-house data + Python analysis).
2. Publish study landing page with shareable graphics.
3. Identify 100 prospect journalists / publications covering the topic.
4. Recipe 9 digital-PR pitch template.
5. Track via Recipe 12 link velocity post-publish.

**Result:** 5-15% pitch acceptance = 5-15 links + multiple unlinked mentions to convert later.

## Edge cases / gotchas

- **White-hat only — NEVER trade links** — "I'll link to you if you link to me" = Google link scheme.
- **Paid links require `rel="sponsored"` or `rel="nofollow"`** — undisclosed paid links = manual action risk.
- **Disclose business relationships** — affiliate / partner / sponsored links must be transparent.
- **Anchor text from outreach prospects unpredictable** — they'll use what feels natural to them. Don't dictate anchor text; that's manipulative.
- **Don't outreach at scale to spam prospects** — DR < 10 + irrelevant TLD = avoid; will hurt link profile.
- **Pitchbox / Respona AI personalization** — useful but verify output doesn't sound robotic. Some "personalized" emails read as AI-generated and get spam-flagged.
- **gmail-mcp sending limits** — 500/day Gmail consumer; 2000/day Workspace; rate-limit at 100/hr to avoid spam classification.
- **Reply rate ~5-15% across templates** — anything claiming 30%+ is selling you snake oil.
- **Link verification 30-90 days** — sites take time to update. Don't classify as NEGATIVE prematurely.
- **Negative-SEO disavow rarely warranted** — Google's 2024 reaffirmation: 99% of cases handled algorithmically. Disavow only after confirmed manual action.
- **DR-weighted growth > raw RDs** — 1 RD with DR 80 worth ~10× one with DR 20. Track quality, not quantity.
- **Outreach saturation** — same journalist gets 200+ pitches/week. Personalization + genuine value differentiation matters.

## Sources

- [Pitchbox API documentation](https://pitchbox.com/api/)
- [Respona API documentation](https://respona.com/api)
- [BuzzStream API documentation](https://www.buzzstream.com/api/)
- [Ahrefs broken backlinks endpoint](https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp)
- [Ahrefs blog — broken link building](https://ahrefs.com/blog/broken-link-building/)
- [Ahrefs blog — unlinked mentions](https://ahrefs.com/blog/unlinked-mentions/)
- [Backlinko — link building guide](https://backlinko.com/link-building)
- [Google Search Central — disavow rare 2024](https://developers.google.com/search/blog/2024/04/disavow-rare)
- [Google Search Central — link spam guidance](https://developers.google.com/search/docs/essentials/spam-policies#link-spam)
