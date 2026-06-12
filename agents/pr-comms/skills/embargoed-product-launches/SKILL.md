<!--
Source: https://pr.co/pr-resources/crisis-communications-playbook
DocuSign API: https://developers.docusign.com/
role.md embargo policy: internal
-->
# Embargoed Product Launches — SKILL

Embargo discipline + NDA tracking + break monitoring. Individual `gmail-mcp` sends to tier-1 list (NEVER BCC). Embargo expiry in subject + body. Optional DocuSign NDA for materially sensitive embargoes. Brand mention monitoring during embargo window via `firecrawl-mcp` + `brave-search` + Brand24 alerts.

## When to use this skill

- **Major product launch** — exclusive preview to 10-25 tier-1 journalists 2-7 days before public.
- **Series funding announcement** — wire + tier-1 1:1 pre-brief at embargo lift.
- **M&A announcement** — sensitive, often NDA-required, narrow embargo.
- **Customer reference / case study with named customer** — pre-brief tier-1 outlets in customer's vertical.
- **Coordinated multi-region launch** — embargo across time zones with simultaneous lift.

**Do NOT use this skill when:**
- The news is routine (no exclusive value) — use `press-release-writing-distribution` direct.
- The news is internal / employee-only — outside agent scope.
- The news is breaking crisis comms — use `crisis-comms-24-48-72-hour-playbook` (different discipline).

## Setup

### gmail-mcp (individual sends only)

```bash
# Already in agent.yaml
# Critical: NEVER use BCC for embargo distribution
```

### DocuSign API (optional NDA)

```bash
# Used for materially sensitive embargoes (financial details, customer names not yet public)
export DOCUSIGN_API_KEY="<key>"
export DOCUSIGN_ACCOUNT_ID="<id>"
export DOCUSIGN_API_BASE="https://demo.docusign.net/restapi/v2.1"
```

### HelloSign / Adobe Sign as alternates

Same workflow, different API.

### Brand mention monitoring (during embargo)

Brand24 webhook + `firecrawl-mcp` cron + `brave-search` cron + `twitter-mcp` keyword stream. Watch headline keywords.

### Notion embargo tracking DB

Per embargo:
- `launch_name` (text)
- `embargo_lift_time` (datetime — explicit time zone)
- `wire_release_scheduled` (datetime — usually = embargo lift)
- `tier_1_list_ids` (multi-text — journalist Notion IDs)
- `nda_required` (checkbox)
- `nda_template_url` (URL)
- `journalist_status` (rich text — per-journalist: invited / signed-nda / accepted / pre-brief / break)
- `pre_brief_slots` (multi-text — Calendly links)
- `embargo_break_detected` (checkbox)
- `break_url` (URL, if applicable)
- `break_journalist` (text, if applicable)
- `lift_executed` (checkbox)
- `coverage_24h` (multi-text)

## Common recipes

### Recipe 1: Build embargo list from tier-1 media list

```bash
# Pull tier-1 journalists matching the launch topic
embargo_list=$(notion query "media_list 
  WHERE outlet_tier = 'T1' 
  AND beats CONTAINS 'AI' OR 'SaaS' 
  AND region = 'US'
  LIMIT 18")

# Save list with journalist details + last 5 article URLs (for personalization)
echo "$embargo_list" > embargo_list.json
```

### Recipe 2: Pre-embargo journalist verification

```python
# Don't add new journalists to embargo list at last minute
# Verify each journalist on embargo list is:
# 1. Currently at the outlet (Muck Rack webhook check)
# 2. Not on relationship blacklist (prior embargo break)
# 3. Has prior interaction (preferred — warm trumps cold for embargo)

for j in embargo_list:
    # Muck Rack outlet check
    current_outlet = muck_rack.get_journalist(j['muckrack_id'])['outlet']['name']
    if current_outlet != j['outlet']:
        # Journalist moved; reach out to confirm or remove from list
        notion.update(j['id'], status='outlet_changed_verify')
        continue

    # Blacklist check
    if j['notes'].get('blacklist'):
        notion.update(j['id'], status='blacklisted_skip')
        continue
```

### Recipe 3: DocuSign NDA workflow (optional)

```bash
# Send NDA via DocuSign for each journalist on embargo list
for j in $(jq -c '.[]' embargo_list.json); do
  name=$(echo "$j" | jq -r .name)
  email=$(echo "$j" | jq -r .email)

  # Create envelope from NDA template
  envelope_id=$(curl -X POST "$DOCUSIGN_API_BASE/accounts/$DOCUSIGN_ACCOUNT_ID/envelopes" \
    -H "Authorization: Bearer $DOCUSIGN_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"templateId\": \"$NDA_TEMPLATE_ID\",
      \"templateRoles\": [{
        \"roleName\": \"Journalist\",
        \"name\": \"$name\",
        \"email\": \"$email\"
      }],
      \"status\": \"sent\"
    }" | jq -r .envelopeId)

  notion-mcp update_row --filter "journalist=$name" \
    --nda_envelope_id "$envelope_id" \
    --nda_status "sent"
done

# Check signing status before sending embargo content
curl "$DOCUSIGN_API_BASE/accounts/$DOCUSIGN_ACCOUNT_ID/envelopes/$envelope_id" \
  -H "Authorization: Bearer $DOCUSIGN_API_KEY" \
| jq .status
```

### Recipe 4: Embargo pitch sends (T-5 to T-2 days)

```bash
# Loop per journalist — individual sends, NEVER BCC
for j in $(jq -c '.[]' embargo_list.json); do
  name=$(echo "$j" | jq -r .name)
  email=$(echo "$j" | jq -r .email)
  outlet=$(echo "$j" | jq -r .outlet)
  last_article=$(echo "$j" | jq -r .last_5_article_urls[0])

  # Claude personalizes per journalist
  pitch=$(claude --prompt "Generate embargoed launch pitch for $name at $outlet, referencing their article: $last_article. Subject under 49 chars. Body under 150 words. Hard embargo language at top.")

  gmail-mcp send \
    --to "$email" \
    --subject "EMBARGOED Jun 18 6am ET: Acme Series B launch" \
    --body "**EMBARGOED UNTIL Tuesday, June 18, 2026, 6:00 AM ET / 11:00 AM UK / 1:00 PM CET**

$pitch

EMBARGO RULES:
- Do not publish before Jun 18, 6:00 AM ET.
- Do not share with other journalists.
- Reply 'embargo confirmed' if accepting.

Pre-brief slots Friday Jun 14, 1-5pm PT: https://calendly.com/acme-press/embargo-jun18-prebrief

NDA: https://docusign.acme.com/embargo-jun18 (optional but appreciated for materially sensitive details)

Media kit: https://acme.com/press/series-b-kit

— Maria Chen, press@acme.com"

  # Log
  notion-mcp update_row --filter "journalist=$name" \
    --embargo_pitch_sent "$(date -Iseconds)" \
    --embargo_status "pitched"

  # Throttle
  sleep 60
done
```

### Recipe 5: Embargo confirmation tracking

```bash
# Monitor gmail-mcp for "embargo confirmed" replies
gmail-mcp search --query "subject:'embargo confirmed' OR body:'embargo confirmed'" \
  --since "$(date -d '7 days ago' -I)" \
| jq '.messages[] | {from, subject, snippet}'

# Per confirmation, update Notion
for confirmation in $confirmations; do
  journalist_email=$(echo "$confirmation" | jq -r .from)
  notion-mcp update_row --filter "email=$journalist_email" \
    --embargo_status "confirmed"
done

# 24 hours before embargo lift, send reminder to confirmed list
gmail-mcp send --to "$confirmed_journalist_email" \
  --subject "Reminder: Acme embargo lifts in 24 hours" \
  --body "Embargo lifts: Jun 18, 6:00 AM ET. Wire release queued. Last call for pre-brief if you need it."
```

### Recipe 6: Embargo break monitoring (during window)

```bash
# Cron every 15 min during embargo window
embargo_lift_ts="2026-06-18T13:00:00Z"  # 6am ET = 13:00 UTC
now=$(date -u +%s)
embargo_lift_unix=$(date -d "$embargo_lift_ts" +%s)

while [ "$now" -lt "$embargo_lift_unix" ]; do
  # Search for embargoed headline keywords across outlets
  brand_keywords=("Acme Series B" "Sequoia leads Acme" "Acme Corp $50M")

  for kw in "${brand_keywords[@]}"; do
    # Brave search since 1hr ago
    recent=$(brave-search "$kw" --since "1h" --type "news" | jq -c '.results[]')

    for r in $recent; do
      url=$(echo "$r" | jq -r .url)
      date=$(echo "$r" | jq -r .date)

      # Skip our own newsroom
      if [[ "$url" =~ acme\.com ]]; then continue; fi

      # Check if URL date is BEFORE embargo lift
      url_unix=$(date -d "$date" +%s)
      if [ "$url_unix" -lt "$embargo_lift_unix" ]; then
        # EMBARGO BREAK
        slack-mcp send --channel "#comms-crisis" \
          --text "EMBARGO BREAK DETECTED: $url published at $date (before lift $embargo_lift_ts)"

        notion-mcp update_row --filter "launch_name='Series B Jun 18'" \
          --embargo_break_detected true \
          --break_url "$url"

        # Trigger embargo break protocol
        ./embargo_break_protocol.sh
        exit 0
      fi
    done
  done

  # Twitter monitor
  twitter-mcp search --query "Acme Series B OR Sequoia Acme" --since "1h" | jq '.tweets[]' >> tweet_check.json
  # Reddit monitor
  reddit-mcp search --query "Acme Series B" --since "1h" | jq '.posts[]' >> reddit_check.json

  sleep 900 # 15 min
  now=$(date -u +%s)
done
```

### Recipe 7: Embargo break protocol

```bash
#!/bin/bash
# embargo_break_protocol.sh — activated when break detected

# 1. Lift embargo immediately to remaining journalists
remaining=$(notion query "embargo_list WHERE embargo_status='confirmed' AND lifted!=true")

for j in $remaining; do
  email=$(echo "$j" | jq -r .email)

  gmail-mcp send \
    --to "$email" \
    --subject "Embargo lifted EFFECTIVE IMMEDIATELY: Acme Series B" \
    --body "The embargo on the Acme Series B announcement is lifted effective immediately due to early publication elsewhere.

Wire release is firing now. Full press kit + briefing material attached.

CEO + Series B lead investor available for next 2 hours for any tier-1 outlet that wants to publish ASAP.

— Maria"
done

# 2. Fire wire release NOW (if scheduled for later)
curl -X PATCH "$PRN_API_BASE/releases/$release_id" \
  -u "$PRN_USERNAME:$PRN_PASSWORD" \
  -d '{"release_date": "'$(date -Iseconds)'"}'

# 3. Public statement on newsroom
notion-mcp create_page --db public_statements --properties "..."

# 4. Update Notion with break details
notion-mcp update_row --filter "launch_name='Series B Jun 18'" \
  --lift_executed true \
  --lift_executed_at "$(date -Iseconds)" \
  --lift_reason "embargo break"

# 5. Log breaker for future relationship blacklist conversation (NOT auto-ban)
notion-mcp create_page --db relationship_log --properties "{
  type: 'embargo_break',
  journalist: '$break_journalist',
  outlet: '$break_outlet',
  date: '$(date -I)',
  url: '$break_url',
  notes: 'PR lead decision on future relationship status'
}"

# 6. DO NOT publicly shame the breaker. Private conversation only.
```

### Recipe 8: Coordinated lift execution (no break)

```bash
# T+0 = embargo lift moment
# 1. Wire release fires automatically (was scheduled at this moment)
# 2. Newsroom page updates
# 3. CEO LinkedIn post + Twitter thread
# 4. Confirm tier-1 stories publishing

# Confirmation check 30 min post-lift
sleep 1800
expected_outlets=("nytimes.com" "bloomberg.com" "techcrunch.com" "theinformation.com")
for outlet in "${expected_outlets[@]}"; do
  found=$(brave-search "Acme Series B site:$outlet" --since "1h" | jq '.results | length')
  if [ "$found" -gt 0 ]; then
    echo "Confirmed: $outlet published"
  else
    echo "Pending: $outlet not yet published"
  fi
done
```

## Examples — full embargo launch

```yaml
launch: Acme Series B announcement
embargo_lift: 2026-06-18 06:00 ET (US East Coast morning)
list_size: 18 tier-1 journalists across US + UK + EU

T-7_days:
  - confirm news + spokesperson + customer/partner quotes
  - draft press release
  - vale lint pass
  - legal review
  - boilerplate updated

T-5_days:
  - build embargo list from tier-1 media list (18 names)
  - DocuSign NDA created (optional, for materially sensitive financial detail)
  - pre-brief slots open on calendly
  - wire release scheduled for embargo lift

T-5 to T-2_days:
  - individual embargoed pitches sent via gmail-mcp (NEVER BCC)
  - personalization per journalist (cite their recent article)
  - track confirmations in notion

T-1_day:
  - reminder email to confirmed journalists
  - mock spokesperson interview (via media-training-spokesperson-prep)
  - prep room logistics
  - confirm wire release scheduling correct

T-0 (embargo lift moment):
  - wire release fires
  - newsroom page live
  - CEO LinkedIn post + Twitter thread
  - 30-min check: confirm tier-1 stories publishing
  - any pending NDA signers: extension or skip per status

T+30min to T+4hr:
  - monitor for additional pickup (wire syndication wave)
  - brand mention monitoring continues (Brand24 / brave-search)
  - respond to follow-up journalist questions

T+24h:
  - placement report pull (recipe 8 in press-release-writing-distribution)
  - tier auto-tag
  - EMV calculation
  - notion coverage log update

T+72h:
  - second pass placement gathering
  - sentiment overlay
  - client digest sent
```

## Edge cases

### NEVER BCC
The single hardest rule. BCC = reply-all leaks the embargo list = embargo broken trust. Individual sends only. Throttle with sleep 60 if needed.

### Subject line includes embargo expiry
Format: `EMBARGOED <date> <time> <timezone>: <topic>`. Examples:
- `EMBARGOED Jun 18 6am ET: Acme Series B`
- `EMBARGOED until Tue 6am ET / 11am UK: Acme Q2 results`

Triple-include: subject + body top + body bottom.

### Time zone discipline
US ET is the default for US embargoes. UK embargo at 6am ET = 11am UK = 1pm CET. State all three for cross-region launches. Don't assume journalist is in your time zone.

### Pre-brief slots are valuable
Tier-1 journalists want to research before publishing. Open calendly slots Friday-before:
- 30-min slots with CEO + product lead
- Optional NDA signing in advance
- They can ask questions, see demo, validate facts

This investment increases tier-1 pickup rate.

### NDA is optional, not universal
Most embargoes don't need NDA. Use NDA only for:
- Materially sensitive financial details (pre-Reg-FD)
- Customer names not yet public
- Acquisition / strategic deal terms

Over-NDA-ing creates friction. Journalists may skip the story.

### Confirmation reply tracking
Get explicit "embargo confirmed" reply from journalists before sharing the press release. If they don't reply, don't share. Saves you on the break-list later.

### Embargo break detection latency
Brand24 alerts fire within 15 min of publication. `firecrawl-mcp` cron at 15 min interval. `brave-search` may lag 30-60 min. Manual journalist check via direct DM trumps automation.

### Don't email-shame the breaker
Private conversation with the offending journalist. "Hey, the embargo was Jun 18, 6am ET — I want to understand what happened on your end before we work together again." Relationship preservation; outlet blacklist is PR lead decision, not automated.

### Auto-blacklist vs case-by-case
Some PR shops auto-blacklist after one break. CraftBot default: PR lead decides per case. Log break in Notion for future reference but don't ban automatically.

### Tier-1 publishing first matters
Order of publication: tier-1 stories at embargo lift → tier-2 trade press 1-4 hr later → tier-3 syndication 4-24 hr later. If tier-1 fails to publish, the launch loses momentum. Pre-brief tier-1 hard.

### Multi-region simultaneous lift
For global launches, embargo lifts simultaneously in all regions (typically morning ET = afternoon CET = morning Asia next day). Coordinate per region:
- Regional wire (PRN Europe, Kyodo, Xinhua)
- Per-language press release (via `deepl-mcp`)
- Regional spokesperson availability

### Embargo + analyst pre-brief
Tier-1 analyst (Gartner / Forrester) pre-brief ≠ embargo for press. Analysts get briefed under NDA 6-12 weeks before, separate workflow. Press embargo is 2-7 days. Don't conflate.

### Customer-named launches
If launch features a named customer (case study), customer has right to:
- Approve final quote
- Approve outlet list
- Decline appearing in specific outlets

Pre-clear all via `customer-reference-program-pr` skill.

### After-action embargo review
Per launch:
- How many on embargo list confirmed?
- How many published at lift?
- How many pre-briefed?
- Any breaks?
- Time-to-publish for tier-1?

Use to refine list + process for next launch.

### Embargo for tier-1 only
Tier-2/T3 outlets don't usually get embargoes — they cover from wire. Embargo discipline only for tier-1. Tier-2 should get wire release at lift moment + optional 1:1 follow-up.

### M&A embargo extra caution
M&A leaks move stocks. Reg-FD applies for public companies. Coordinate tightly with `investor-relations` agent. Often NDA + narrow tier-1 list + simultaneous SEC filing + wire release.

## Sources

- **PR.co embargo discipline**: https://pr.co/pr-resources/crisis-communications-playbook
- **DocuSign API**: https://developers.docusign.com/
- **HelloSign API**: https://developers.hellosign.com/
- **role.md embargo policy**: internal
- **role.md embargo break monitoring**: internal
- **role.md embargo break protocol**: internal
