<!--
Source: https://www.thegutenberg.com/blog/crisis-comms-3-0-ai-crisis-communication-strategies-for-navigating-misinformation/
PR.co playbook: https://pr.co/pr-resources/crisis-communications-playbook
5W PR predictive: https://www.5wpr.com/new/predictive-crisis-communications-using-ai-and-real-time-data/
-->
# Crisis Comms 24/48/72-hour Playbook — SKILL

Pre-drafted templates + multi-stakeholder variants + multi-channel distribution + sentiment monitoring. Activated by Slack alert from monitoring; Claude generates holding statement in <5 min; human approves; distribute via `gmail-mcp` (press), `slack-mcp` (internal), `twitter-mcp` (public thread). Day-2/3 escalation tree documented. 53% of consumers expect brand response within first hour (2026 data).

## When to use this skill

- **Data breach / security incident** — customer data exposure, ransomware, third-party leak.
- **Product safety / recall** — physical harm risk, regulatory recall.
- **Executive misconduct** — public allegation, departure announcement, board action.
- **Service outage with reputational angle** — major SaaS outage that draws press coverage (pair with `customer-support-agent` for customer comm).
- **PR backlash / viral negative content** — competitor attack, customer story going viral, social pile-on.
- **Misinformation / deepfake circulating** — fabricated quote, doctored video, AI-cloned audio.
- **Regulatory action** — DOJ inquiry, FTC settlement, congressional hearing.
- **M&A / leadership transition controversy** — leak, hostile bid, abrupt CEO departure.

**Do NOT use this skill when:**
- The incident is a routine service blip handled by customer support (no press attention) — defer to `customer-support-agent`.
- The disclosure is a Reg-FD 8-K event — defer to `investor-relations` (but coordinate timing).
- The "crisis" is internal HR (use HR comms, not press) — generally outside agent scope.

## Setup

### Pre-loaded Notion assets

Crisis-comms DB with rows for:
- `pre_drafted_holding_statements` per incident category (data breach, outage, etc.)
- `contact_tree` per crisis trigger (T+0 to T+2hr roles + backups)
- `spokesperson_assignments` — primary + backup per topic
- `q_a_docs` per incident type — 20-30 likely questions
- `boilerplate_versions` — current approved company description
- `monitoring_keywords` per crisis category (brand + product + likely-incident vocabulary)

### Monitoring infrastructure

Brand24 / Brandwatch / Meltwater + `firecrawl-mcp` + `brave-search` + `twitter-mcp` keyword stream + `reddit-mcp` subreddit watch — all running pre-crisis to detect signal early.

```bash
# Brand24 webhook for sentiment velocity alert
curl -X POST "https://api.brand24.com/v3/projects/<id>/alerts" \
  -H "Authorization: Bearer $BRAND24_TOKEN" \
  -d '{
    "type": "sentiment_drop",
    "threshold_pct": 20,
    "window_hours": 4,
    "callback_url": "https://crisis-handler.acme.com/webhook"
  }'
```

### Deepfake detection (Truepic / Reality Defender / Sensity)

```bash
export TRUEPIC_API_KEY="<key>"
export REALITY_DEFENDER_API_KEY="<key>"
# Used when suspicious media surfaces during a crisis
```

### Slack crisis channel pre-built

`#comms-crisis` (private, comms team + legal + CEO). Pre-populated bookmarks with contact tree, holding statement template, Q&A doc template, escalation tree.

## Common recipes

### Recipe 1: Truth-first protocol (hour 0-1)

Before any outbound communication, the comms lead answers in writing:

```markdown
## Truth-first triage (timestamp: T+0)

### What do we know is TRUE right now?
- [Confirmed fact 1, with source]
- [Confirmed fact 2, with source]
- [Confirmed fact 3, with source]

### What are we still investigating?
- [Investigation thread 1] — owner: [name]
- [Investigation thread 2] — owner: [name]

### What CAN'T we say?
- [Legal constraint, e.g., active investigation]
- [Customer privacy constraint]
- [NDA constraint]

### Who's the spokesperson?
Primary: [Name + Title]
Backup: [Name + Title]
Brief deadline: T+30 min

### Who's been notified?
- [ ] CEO + General Counsel (T+0)
- [ ] Comms team (T+5)
- [ ] PR / IR / CS leads (T+15)
- [ ] Spokesperson briefed (T+30)
- [ ] Board chair (T+45 via investor-relations)
```

### Recipe 2: Holding statement (T+0 to T+1)

```markdown
**Acme Corp Statement on [Incident Title]**

[City], [Date] — [Time ET]

Acme Corp is aware of [incident in neutral terms]. We are actively investigating
[scope of investigation]. The [safety / privacy / continuity] of [affected
stakeholders] is our priority.

[1-2 sentence framing of what we know and what we don't — without speculation.]

We are committed to transparency and will provide updates as we learn more.
Our next update will be issued by [specific time, max 4 hours from now].

For media inquiries: press@acme.com
For affected customers: [support channel + phone]

[Spokesperson Name], [Title]
Acme Corp
```

Generate via Claude with prompt:

```python
prompt = f"""
Generate a truth-first crisis holding statement.

INCIDENT TYPE: {incident['type']}
CONFIRMED FACTS: {incident['confirmed_facts']}
UNDER INVESTIGATION: {incident['investigating']}
LEGAL CONSTRAINTS: {incident['cannot_say']}
NEXT UPDATE COMMITMENT: {incident['next_update_time']}
SPOKESPERSON: {incident['spokesperson']}

Use the template structure. NO speculation. NO blame. NO marketing language.
Maximum 150 words. Specific commit to next update time within 4 hours.
"""
holding = claude(prompt)
```

### Recipe 3: Per-stakeholder variant generation

```python
stakeholders = ['customers', 'employees', 'press', 'regulators', 'investors', 'public']

for s in stakeholders:
    prompt = f"""
    Generate the {s} variant of the crisis communication.

    BASE FACTS: {holding_statement}
    STAKEHOLDER: {s}
    TONE FOR {s}: {tone_per_stakeholder[s]}
    CHANNEL: {channel_per_stakeholder[s]}
    DETAIL LEVEL: {detail_per_stakeholder[s]}

    For customers: direct, ownership-taking, what they need to DO.
    For employees: transparent, candid, how to talk about it externally.
    For press: factual, on-record, full context + spokesperson availability.
    For regulators: compliant, legal-reviewed, per their requirements.
    For investors: Reg-FD compliant (defer to investor-relations).
    For public: truthful, accountable.

    Output the message body only.
    """
    variants[s] = claude(prompt)
```

### Recipe 4: Distribute via multi-channel (T+1 to T+4)

```bash
# Press wire
gmail-mcp send \
  --to "$(notion query 'media_list/tier_1_crisis_press' | jq -r '.[].email' | tr '\n' ',')" \
  --subject "Acme Corp statement on [incident]" \
  --body "${variants[press]}"
# (gmail-mcp will split to individual sends — never BCC)

# Internal (Slack)
slack-mcp send \
  --channel "#all-hands" \
  --text "${variants[employees]}"

# Customer (email + product banner; defer to customer-support-agent for the latter)
gmail-mcp send-bulk \
  --segment "customers_affected" \
  --subject "Important update from Acme" \
  --body "${variants[customers]}"

# Public statement on newsroom
notion-mcp create_page --db public_statements --properties "$(prep_statement.py)"

# LinkedIn org post + CEO post (hand voice to ceo-agent)
linkedin create_post --org "$ORG_URN" --text "${variants[public]}"

# Twitter thread (factual)
twitter-mcp create_thread --segments "$(format_thread.py ${variants[public]})"
```

### Recipe 5: Contact tree activation

```yaml
# In notion as a structured doc per incident type
T+0_min:
  - CEO (Slack DM + phone backup)
  - General Counsel (Slack DM + phone)
T+5_min:
  - CFO (Slack)
  - Head of Customer Success (Slack)
T+10_min:
  - Comms team channel — full team
T+15_min:
  - PR lead, IR lead, CS lead — individually
T+30_min:
  - On-call media spokesperson briefed (Q&A doc + bridge phrases ready)
T+45_min:
  - Board Chair + lead investor (via investor-relations agent)
T+60_min:
  - Holding statement issued to press wire + 1:1 tier-1 sends
T+90_min:
  - Customer-facing comm issued (via customer-support-agent for product banner)
T+2hr:
  - Internal town-hall scheduled within 24 hours
```

Auto-execute via `slack-mcp` page tree:

```bash
# Activate contact tree on incident trigger
incident_id="$1"

slack-mcp send --to "@$CEO_SLACK_ID,@$GC_SLACK_ID" \
  --text "CRISIS T+0: $incident_id activated. Comms lead: $COMMS_LEAD. Contact tree running."

sleep 300 # 5 min
slack-mcp send --to "@$CFO_SLACK_ID,@$CS_HEAD_SLACK_ID" \
  --text "CRISIS T+5: $incident_id update; CEO+GC briefed; contact tree continuing."

# ... continue for each step
```

### Recipe 6: Sentiment monitoring during crisis

```bash
# Brand24 / Brandwatch sentiment velocity alert
while [ "$crisis_active" = "true" ]; do
  current=$(curl -s "https://api.brand24.com/v3/projects/$PROJECT_ID/sentiment?period=1h" \
    -H "Authorization: Bearer $BRAND24_TOKEN" | jq .net_sentiment)

  baseline=$(cat baseline_sentiment.txt)

  drop=$(echo "($baseline - $current) / $baseline" | bc -l)

  if (( $(echo "$drop > 0.20" | bc -l) )); then
    slack-mcp send --channel "#comms-crisis" \
      --text "ALERT: Sentiment dropped 20%+ in past hour. Current: $current. Pull Brand24 dashboard."
  fi

  # Volume spike
  volume=$(curl -s "https://api.brand24.com/v3/projects/$PROJECT_ID/mentions?period=1h" \
    -H "Authorization: Bearer $BRAND24_TOKEN" | jq .count)
  baseline_vol=$(cat baseline_volume.txt)
  if (( volume > baseline_vol * 3 )); then
    slack-mcp send --channel "#comms-crisis" \
      --text "ALERT: Mention volume spiked 3x+ in past hour. Current: $volume. Likely amplification event."
  fi

  sleep 300
done
```

### Recipe 7: Q&A doc generation

```python
prompt = f"""
Generate 25 likely questions for spokesperson during this crisis.

INCIDENT: {incident['summary']}
CONFIRMED FACTS: {incident['confirmed_facts']}
LEGAL CONSTRAINTS: {incident['cannot_say']}
SPOKESPERSON: {spokesperson['name']}, {spokesperson['title']}

Mix:
- 10 fastball factual (what happened, when, scope)
- 8 medium (what are you doing about it, who's accountable, what's next)
- 5 hostile (why didn't you catch this sooner, will heads roll, will customers leave)
- 2 personal (CEO emotional response, board pressure)

For each: 60-word recommended answer + bridge phrase + what NOT to say.
"""
qa = claude(prompt)
```

Pair with `media-training-spokesperson-prep` skill for `mcp-tts` audio drill.

### Recipe 8: Deepfake / misinformation detection

When suspicious media surfaces:

```bash
# Truepic check on suspected fabricated video
curl -X POST "https://api.truepic.com/v2/verify" \
  -H "X-API-Key: $TRUEPIC_API_KEY" \
  -F "media=@suspicious.mp4" \
| jq '{
  is_authentic: .verification.authentic,
  manipulation_score: .verification.manipulation_score,
  c2pa_credentials: .c2pa.present,
  recommendation: .recommendation
}'

# Reality Defender for audio deepfake
curl -X POST "https://api.realitydefender.com/v1/scan" \
  -H "Authorization: Bearer $REALITY_DEFENDER_API_KEY" \
  -F "audio=@suspicious.mp3"

# If confirmed fake:
slack-mcp send --channel "#comms-crisis" \
  --text "DEEPFAKE CONFIRMED: $url. Activating takedown + counter-statement."

# Coordinate legal -> platform takedown request
# Issue factual public statement via newsroom (not panicked, just factual)
notion-mcp create_page --db public_statements --properties "$(prep_deepfake_statement.py)"
```

## Examples — 72-hour escalation timeline

```yaml
T+0 (hour 0-1):
  - truth-first triage (recipe 1)
  - holding statement drafted via Claude (recipe 2)
  - human approval (CEO + GC + comms lead)
  - contact tree activated (recipe 5)
  - spokesperson briefed with Q&A doc (recipe 7)

T+1 to T+4 (hour 1-4):
  - holding statement issued via multi-channel (recipe 4)
  - per-stakeholder variants generated + distributed (recipe 3)
  - brand mention monitoring + sentiment velocity tracking (recipe 6)
  - deepfake check on any suspicious incoming media (recipe 8)

T+4 to T+24 (hour 4-24):
  - full statement (what happened + impact + what we're doing + commitments)
  - Q&A doc expanded (5-10 new likely questions surfaced from press/social)
  - CEO LinkedIn post (hand voice to ceo-agent if exec-personal)
  - internal Slack town hall scheduled
  - customer email + product banner (hand to customer-support-agent)
  - public statement on newsroom
  - sentiment alert thresholds (>20% drop OR 3x volume spike)

T+24 to T+48 (day 2):
  - Q&A doc update from real questions surfacing
  - misinformation amplification watch (deepfake recheck on viral clips)
  - per-stakeholder iteration based on response sentiment
  - tier-1 journalist sit-down requests prioritized (route through media-training-spokesperson-prep)
  - investor coordination (via investor-relations)

T+48 to T+72 (day 3):
  - post-mortem comm
  - what we learned (factually, not defensively)
  - what changes (specific, time-bound)
  - when we'll report back (committed date)
  - public statement via newsroom + LinkedIn

T+7d (week post):
  - retrospective doc (what worked / didn't)
  - update pre-drafted holding statements in notion based on learnings
  - debrief with executive team
```

## Edge cases

### CEO is the story
When the crisis IS about the CEO (misconduct allegation, departure, board pressure), the CEO can't be the spokesperson. Identify backup (often Chair, CFO, or Chief People Officer). Brief them HARD via `media-training-spokesperson-prep`. Hand exec-voice on personal-tone messaging to `ceo-agent`.

### Active legal investigation
Anything that could become discoverable in litigation requires legal pre-clearance. Build into workflow: every statement to press / regulators / public passes legal in writing BEFORE distribution. Slow but non-negotiable.

### Reg-FD intersection
If the crisis is material to a public company's financials, SEC 8-K filing may be required within 4 business days. Defer mechanics to `investor-relations` agent. Coordinate timing so press release doesn't trigger Reg-FD violation.

### Customer outage handled by support, not comms
A simple service outage with no press angle = `customer-support-agent` handles. Crisis comms kicks in ONLY when press picks up OR sentiment alert fires. Decision tree:
- Outage + 0 press inquiries + sentiment normal → support handles
- Outage + 1+ press inquiry → comms activates, customer-support continues customer-facing

### Misinformation amplification
A false story can outrun the truth in 24 hours. Counter quickly with:
- Single authoritative statement on newsroom (don't fragment)
- Repost via CEO LinkedIn + X
- Don't quote-tweet the original (amplifies it)
- Brief tier-1 journalists directly with primary-source documents

### Internal leak during crisis
If internal Slack / email leaks to press during the crisis, address head-on. Don't deny if true. Reframe + provide context. Trying to silence internal voice rarely works and erodes trust.

### Mid-crisis spokesperson change
If primary spokesperson becomes unavailable (sick, on plane, became part of story), backup steps in. Update Notion contact tree mid-flight. Re-brief backup with same Q&A doc + key messages.

### "No comment" is sometimes correct
On active legal matters, "We don't comment on active investigations" is the correct answer. Don't pretend transparency you can't deliver. Bridge to: "What I CAN tell you is..."

### Multi-region / multi-language crisis
Translate per-stakeholder variants via `deepl-mcp`. Issue simultaneously across regions to avoid an information vacuum in any one geography. Coordinate with regional PR leads.

### After-action review (the 7-day mark)
Within 7 days post-crisis, run a written retrospective:
- What we got right (preserve)
- What was slow / wrong (fix)
- What we missed (add to monitoring)
- Update pre-drafted holding statements
- Update Q&A doc with newly surfaced questions
- Update contact tree if roles shifted

Don't skip this — it's the only way the playbook improves.

### Predictive crisis monitoring
Brand24/Brandwatch sentiment velocity tracking + `sec-edgar-mcp` for competitor 8-K disclosures + Reddit/Twitter monitoring can detect brewing crises hours before they explode. Set alert thresholds:
- Sentiment drop >20% over 4-hour window
- Volume spike >3x baseline
- New negative content from a tier-1 journalist
- Competitor crisis bleeds into your category

### Hand-off matrix
- Exec personal voice on crisis statement → `ceo-agent`
- Customer-facing outage comm → `customer-support-agent`
- SEC 8-K filing → `investor-relations`
- HR-internal investigation comm → outside agent scope
- Cybersecurity technical incident response → SecOps team, agent supports comms only

## Sources

- **Crisis Comms 3.0 — Gutenberg**: https://www.thegutenberg.com/blog/crisis-comms-3-0-ai-crisis-communication-strategies-for-navigating-misinformation/
- **PR.co crisis playbook**: https://pr.co/pr-resources/crisis-communications-playbook
- **5W PR predictive crisis comms**: https://www.5wpr.com/new/predictive-crisis-communications-using-ai-and-real-time-data/
- **PRSA AI + crisis comms**: https://www.prsa.org/article/ai-and-the-new-era-of-crisis-comms-ST-May25
- **FullIntel real-time PR crisis**: https://fullintel.com/blog/real-time-pr-crisis-management-a-playbook-for-resilient-teams/
- **Truepic API**: https://www.truepic.com/
- **Reality Defender API**: https://www.realitydefender.com/
- **C2PA Content Credentials**: https://c2pa.org/
