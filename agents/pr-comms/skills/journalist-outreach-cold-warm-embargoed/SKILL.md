<!--
Source: https://magicpitch.com/blog/email-outreach-for-pr-complete-automation-guide-2026
Smartlead: https://www.smartlead.ai/blog/ai-cold-email-outreach-tools
Lemlist: https://www.lemlist.com/
Embargo discipline: https://pr.co/pr-resources/crisis-communications-playbook
-->
# Journalist Outreach — Cold / Warm / Embargoed — SKILL

Personalized journalist pitching across three modes: cold (no prior relationship), warm (Notion CRM relationship history), and embargoed (individual sends with timed lift). Claude personalization is mandatory — journalists detect generic AI personalization in sentence 1. Subject lines under 49 chars. Pitches under 150 words. Cite specific recent articles.

## When to use this skill

- **Cold pitch** — first-time outreach to a journalist on your media list.
- **Warm pitch** — Notion CRM shows prior relationship (coffee, intro, prior placement).
- **Embargoed pitch** — exclusive opportunity before public lift; tier-1 only.
- **Re-engagement** — journalist went silent for 3+ months; re-warm with a specific story angle.
- **High-volume cold** — when sending >50 individual pitches in a week, route through Smartlead/Lemlist warmup infra to preserve deliverability.

**Do NOT use this skill when:**
- The journalist is responding to a HARO/Featured/Qwoted query — use `haro-qwoted-featured-sme-quotes` (4-hour window).
- Pitching a podcast host — use `podcast-tour-booking-for-execs`.
- Submitting a contributed op-ed — use `op-ed-contributed-article-placement`.
- The "outreach" is a crisis comm — use `crisis-comms-24-48-72-hour-playbook`.

## Setup

### gmail-mcp (default for tier-1 individual sends)

Already configured in `agent.yaml`. Verify auth:

```bash
gmail-mcp get_profile
```

### Smartlead (high-volume warmup infra)

```bash
# Plans: $39-$199/mo
export SMARTLEAD_API_KEY="<key>"
export SMARTLEAD_API_BASE="https://server.smartlead.ai/api/v1"
```

Inbox rotation across 10+ sending domains preserves deliverability when volume exceeds 30 emails/day per inbox. Use ONLY for cold outreach, never for tier-1 embargo distribution.

### Lemlist (creative personalization)

```bash
export LEMLIST_API_KEY="<key>"
export LEMLIST_API_BASE="https://api.lemlist.com/api"
```

Lemlist excels at dynamic image personalization (journalist's name on a custom landing page screenshot). Use sparingly — gimmicks turn off serious journalists.

### Notion journalist CRM

Pull from `media-list-muck-rack-cision` skill — same DB. Required fields per journalist:
- `last_5_article_urls`
- `last_pitched` (date)
- `last_placement` (date + URL)
- `relationship_signal` (text)
- `prefs` (text)
- `attribution_default`

### Vale linter for pitch quality

```bash
uvx vale --config=.vale.ini --output=JSON pitch.md
```

Custom rules: ban "thrilled to announce", "leverage", "hope this email finds you well", flag sentences >25 words.

## Common recipes

### Recipe 1: Cold pitch — the 5-line framework

```markdown
**Subject:** Klaviyo MPP measurement data for your inbox piece

Sarah —

Your March 14 piece on post-MPP CTR vs open rate measurement caught us — we ran a 90-day cohort across 47M sends. CTR-only segmentation lifted revenue per send 22% vs hybrid CTR+open.

Want exclusive numbers for a follow-up? CEO + the data scientist who ran it available Thursday.

Embargo until Jan 18, 6am ET. Media kit: https://acme.com/press/mpp-kit

— Maria
press@acme.com
```

Rules:
- Subject <49 chars, cite the angle (not the company)
- First line: reference their LAST article, specific moment, no generic praise
- Lines 2-3: the angle — what's the exclusive? Why now?
- Line 4: 1 data point + 1 spokesperson + 1 next step
- Line 5: logistics + media kit link
- Total <150 words

### Recipe 2: Cold pitch generation (Claude personalization)

```python
# Pull journalist profile from Muck Rack via media-list skill
journalist = notion.query(filter={"name": "Sarah Perez"})[0]
recent_article = firecrawl.scrape(journalist['last_5_article_urls'][0])

# Claude generates personalized pitch
prompt = f"""
Generate a 150-word cold pitch from these inputs.

JOURNALIST: {journalist['name']}, {journalist['outlet']}
RECENT ARTICLE (cite a specific moment): {recent_article['title']} - {recent_article['url']}
KEY ARGUMENT IN RECENT ARTICLE: {recent_article['summary']}

OUR ANGLE: {launch_brief['angle']}
OUR EXCLUSIVE OFFER: {launch_brief['exclusive']}
OUR DATA POINT: {launch_brief['data_point']}
OUR SPOKESPERSON AVAILABLE: {launch_brief['spokesperson']}, {launch_brief['title']}

Subject line MUST be under 49 chars and cite the angle.
First line MUST reference a SPECIFIC moment from their recent article.
NO banned openers: "thrilled to announce", "hope this finds you well", "I'm reaching out because".
"""

pitch = claude(prompt)
```

### Recipe 3: Warm pitch — relationship layer

Pull from Notion CRM. Reference the relationship signal in line 1:

```markdown
**Subject:** Acme Q1 results + the cohort question you asked at SaaStr

Sarah —

Since the SaaStr coffee in March, you've been all over the post-MPP measurement angle — figured you'd want this.

Q1 cohort across 47M sends shows CTR-only segmentation lifting revenue 22% vs hybrid. Sequoia-led Series B closes today; CEO + data scientist available for 30 min Wednesday.

Embargo until 6am ET tomorrow. Numbers and methodology in attached deck.

— Maria
```

### Recipe 4: Embargoed launch — individual sends only

```bash
# Pull tier-1 embargo list (NEVER BCC, NEVER auto-loop)
embargo_list=$(notion query 'media_list/tier_1_tech AND embargo_jun18=true')

# Loop, but each send is individual
echo "$embargo_list" | jq -c '.[]' | while read journalist; do
  name=$(echo "$journalist" | jq -r .name)
  email=$(echo "$journalist" | jq -r .email)
  recent_url=$(echo "$journalist" | jq -r .last_5_article_urls[0])

  # Claude personalizes per journalist
  pitch=$(generate_pitch.py --journalist "$journalist" --release release.md)

  gmail-mcp send \
    --to "$email" \
    --subject "EMBARGOED Jun 18 6am ET: Acme Series B" \
    --body "$pitch

EMBARGO: Tuesday, June 18, 2026, 6:00 AM ET.
Pre-brief slots: Fri 1-5pm PT, https://calendly.com/acme-press/embargo-jun18.
NDA: https://docusign.acme.com/embargo-jun18 (optional but appreciated).
Media kit: https://acme.com/press/series-b-kit"

  # Log to Notion
  notion-mcp update_row --filter "name=$name" --last_pitched "$(date -I)"

  # Throttle to avoid Gmail rate limit
  sleep 30
done
```

### Recipe 5: Smartlead high-volume sequence (cold only)

```bash
# Create campaign
curl -X POST "$SMARTLEAD_API_BASE/campaigns" \
  -H "X-API-Key: $SMARTLEAD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Q3-cold-pitch-tech-trade",
    "sender_inboxes": ["press@acme.com","maria@acme.com","sam@acme.com"],
    "daily_limit_per_inbox": 25,
    "tracking": {"opens": true, "clicks": true, "replies": true}
  }'

# Add prospects with personalization
curl -X POST "$SMARTLEAD_API_BASE/campaigns/$campaign_id/leads" \
  -H "X-API-Key: $SMARTLEAD_API_KEY" \
  -d @leads.json
# Where leads.json contains [{email, first_name, outlet, last_article_url, custom_intro}]

# Sequence steps:
# Day 0: personalized pitch (<150 words)
# Day 3: follow-up if no open ("did you see this?")
# Day 7: final follow-up ("last chance to scoop")
# Stop sequence on ANY reply (positive or negative)
```

### Recipe 6: Subject-line A/B test

Smartlead supports subject A/B at the campaign level:

```json
{
  "step_id": "intro",
  "subjects": [
    {"text": "MPP measurement data for your inbox piece", "weight": 50},
    {"text": "47M-send cohort: MPP ≠ what we thought", "weight": 50}
  ]
}
```

Auto-route winner after 100 sends per variant.

### Recipe 7: Re-engagement (journalist gone silent)

Pull journalists with `last_pitched > 90 days AND last_placement is null`:

```bash
silent=$(notion query 'media_list/last_pitched_over_90d')

for j in $silent; do
  # Don't re-pitch with same angle. Generate fresh hook.
  hook=$(claude --prompt "Re-engagement hook for $j based on their last 3 articles + our Q1 data.")

  gmail-mcp send \
    --to $(echo "$j" | jq -r .email) \
    --subject "$hook" \
    --body "<personalized re-warm>"
done
```

### Recipe 8: Embargo break monitoring

During an embargo window, monitor for premature publication:

```bash
# Cron every 15 min during embargo window
for keyword in "Acme Series B" "Sequoia leads Acme"; do
  results=$(brave-search "$keyword" --since "1h" | jq -c '.results[]')
  for r in $results; do
    url=$(echo "$r" | jq -r .url)
    if [[ ! "$url" =~ acme\.com ]]; then
      slack-mcp send --channel comms-crisis --text "EMBARGO BREAK SUSPECTED: $url"
      # Activate embargo break protocol (see role.md)
    fi
  done
done
```

## Examples — high-volume cold campaign

```yaml
campaign: Q3 thought leadership cold outreach
target: 150 journalists across 3 tier brackets
infra: Smartlead with 4 sender inboxes
cadence:
  day_0: personalized pitch (Claude generation per journalist)
  day_3: follow-up_1 if no_open
  day_7: follow-up_2 if no_reply
  day_14: stop_sequence

quality_gates:
  - vale lint pass per pitch
  - claude humanize pass (humanize-ai-text skill)
  - subject <49 chars
  - body <150 words
  - first line cites SPECIFIC recent article moment
  - no banned openers / buzzwords

success_metrics:
  open_rate: target 35-45%
  reply_rate: target 8-15%
  placement_rate: target 2-5%
  unsubscribe_rate: keep <1%
```

## Edge cases

### Banned openers (kill immediately)
- "I hope this email finds you well"
- "Thrilled to announce"
- "I'm reaching out because"
- "Great article!" / "Loved your piece on..."
- "Quick question for you"
- "Hi there!"
- "Hope your week is going well"

Journalists run mental autocomplete on these. The pitch goes to trash before sentence 2.

### Personalization signal beyond {first_name}
Variable replacement is NOT personalization. Tip-offs of generic AI personalization:
- "Your work on X has been impressive" — empty praise
- "I came across your article on X" — passive verb
- "I noticed you cover X" — restating their bio

Real signal: "Your March 14 piece argued [specific quote]; our data says [counterpoint with number]."

### Subject line limit truly <49 chars
Gmail truncates at 60 chars on desktop, 45 chars on mobile. 49 is the safe ceiling. Test with `echo -n "subject" | wc -c`.

### Embargo discipline — NEVER BCC
BCC = embargo break risk (reply-all leaks the list). Individual sends only. Track each send in Notion with timestamp + body delta if any.

### Follow-up cadence — don't be a pest
2 follow-ups MAX after the initial pitch. After follow-up 2 with no reply: STOP. Re-engage with a fresh angle in 90 days. Spamming kills future relationship.

### Smartlead vs gmail-mcp decision tree
- Volume ≤30/day per inbox + tier-1 + embargo = `gmail-mcp` individual sends
- Volume >30/day + cold + no embargo = Smartlead with warmup
- ANY embargo = `gmail-mcp` only (Smartlead's inbox rotation breaks embargo trust)
- ANY warm (Notion CRM relationship signal) = `gmail-mcp` only

### What if the journalist replies "no"
- Reply thanking them, log "declined" in Notion
- Don't argue
- Don't re-pitch the same angle within 90 days
- Note the reason if given ("not a fit", "already covered", "moving beats") in `prefs` field

### Humanize-AI-text pass on cold pitches
Run every cold pitch through `humanize-ai-text` skill before send. Strips AI-detection signals (em-dash density, certain transitional phrases, sentence-length variance patterns). Reduces "this is AI" perception.

### Deliverability check before high-volume
Before launching a 150-journalist cold campaign:
1. Check SPF + DKIM + DMARC alignment on sending domain (see `email-deliverability-spf-dkim-dmarc` skill if marketing-agent is in scope)
2. Warm sending inboxes for 2-3 weeks before high volume (10/day → 25/day → 50/day)
3. Test with 5 friendly addresses; check spam folder placement

### Attribution status before substance
If a journalist replies asking to chat — first message in the call confirms attribution status. "Quick check: are we on-record by default for this conversation? Happy to go on-background for sensitive parts." Log in Notion interaction DB BEFORE the substantive call.

### Late-night and weekend sends
US tier-1 journalists check email mornings 7-9am ET. EU equivalents 8-10am UK. Avoid sending Fri pm, Sat, Sun. Best windows: Tue-Thu, 7-9am local to the journalist.

## Sources

- **Magic Pitch outreach automation guide 2026**: https://magicpitch.com/blog/email-outreach-for-pr-complete-automation-guide-2026
- **Smartlead AI cold email tooling**: https://www.smartlead.ai/blog/ai-cold-email-outreach-tools
- **Lemlist**: https://www.lemlist.com/
- **Embargo discipline**: https://pr.co/pr-resources/crisis-communications-playbook
- **Vale linter**: https://vale.sh/
- **Gmail API**: https://developers.google.com/gmail/api
