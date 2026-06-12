<!--
Source: https://sproutsocial.com/insights/social-media-scheduling-tools/
Sprout Social inbox routing
HubSpot ticketing
SLA matrix: role.md "Community engagement playbook"
-->
# Social Customer Service Handoff — SKILL

Triage social-channel complaints, acknowledge within 15-min SLA, hand off to `customer-support-agent` via HubSpot / Zendesk ticket. Sprout Social rule-based routing (keyword + sentiment) for enterprise; Agorapulse Inbox Assistant for mid-market; Buffer engagements + regex classifier for SMB. Always acknowledge publicly + take to DM for resolution.

## When to use this skill

- **A complaint in public comments / DM** that needs the support team.
- **Repeated complaints** about same product issue (recurring-pattern).
- **Refund requests / billing issues** surfaced via social.
- **Outage reports** from customers in social channels.

**Do NOT use this skill when:**
- General brand question (non-complaint) — `community-engagement-comments-dms-at-scale`.
- Negative sentiment at scale (crisis) — `social-crisis-comms`.
- Customer praise / testimonial — that's UGC, route to `ugc-reposting-policy-workflow`.

## Setup

### Buffer engagements feed (SMB)

Already set up in `community-engagement-comments-dms-at-scale`.

### Sprout Social inbox routing (enterprise)

```bash
export SPROUT_API_KEY="<key>"
export SPROUT_CUSTOMER_ID="<id>"
# Configure inbox rules in Sprout dashboard:
# - Keywords: 'refund', 'broken', 'doesn't work', 'help', 'cancel', 'where is my order'
# - Auto-tag: "support_queue"
# - Auto-assign: support team
# - SLA: 15 min acknowledgment, 4 hr resolution
```

### Agorapulse Inbox Assistant (mid-market)

```bash
export AGORAPULSE_API_KEY="<key>"
# Inbox Assistant rules
curl -X POST https://api.agorapulse.com/api/v2/inbox/rules \
  -H "Authorization: Bearer $AGORAPULSE_API_KEY" \
  -d '{
    "name": "Auto-route support",
    "conditions": [{"field":"text","operator":"contains_any","value":["refund","broken","help","cancel"]}],
    "actions": [{"type":"tag","value":"support_queue"},
                {"type":"assign","value":"support_user_id"},
                {"type":"set_sla","value":"15min"}]
  }'
```

### HubSpot / Zendesk MCP

```bash
# HubSpot MCP for ticket creation (inherited from marketing-agent ecosystem)
mcp tool hubspot.create_ticket \
  --subject "Social — DM from @user about broken product" \
  --pipeline "support" \
  --priority "high"

# Zendesk fallback
mcp tool zendesk.create_ticket \
  --subject "..." --requester_email "<from_dm>" --priority "high"
```

### Notion Triage Log

Columns from `community-engagement-comments-dms-at-scale` triage DB + `Ticket ID / Resolved at / Resolution notes / Public-thread reply URL`.

## Common recipes

### Recipe 1: Classify + acknowledge

```python
# Per engagement classified as 'complaint' by community engagement skill
@on_classification('complaint')
def handle_complaint(eng):
    # 1. Public acknowledge within 15 min
    public_reply = f"@{eng['author_handle']} Sorry that happened — DMing you now to get this fixed."
    mcp.buffer.respond_to_engagement(id=eng['id'], text=public_reply)
    
    # 2. Open DM (if not already DM)
    if eng['type'] != 'dm':
        dm_text = (f"Hi @{eng['author_handle']} — thanks for flagging this in our comments. "
                   "Could you share your order number or account email so we can look into it?")
        mcp.platform[eng['channel']].send_dm(to=eng['author_handle'], text=dm_text)
    
    # 3. Create HubSpot ticket
    ticket = mcp.hubspot.create_ticket(
        subject=f"Social — {eng['channel']} — {eng['author_handle']}",
        pipeline='support',
        priority=determine_priority(eng),  # high if 'urgent', medium otherwise
        properties={
            'social_channel': eng['channel'],
            'author_handle': eng['author_handle'],
            'original_post_url': eng['url'],
            'original_text': eng['text'],
            'sentiment_score': eng['sentiment']
        }
    )
    
    # 4. Update triage DB
    notion.update_page(eng['notion_id'], {
        'Status': 'escalated',
        'Ticket ID': ticket['id'],
        'Public-thread reply URL': eng['response_url']
    })
```

### Recipe 2: SLA breach watchdog (15 min)

```python
# Every 5 min, check
unacked = notion.query(triage_db, filter={'Type':'complaint','Status':'open'})
for eng in unacked:
    elapsed = (now() - eng['received_at']).total_seconds() / 60
    if elapsed > 15:
        slack.post('#support-sla',
            f"⚠ SLA BREACH: {eng['id']} ({eng['channel']}) — {int(elapsed)} min elapsed, not acknowledged")
    elif elapsed > 12:
        slack.post('#support-sla',
            f"SLA risk: {eng['id']} — 3 min to acknowledge")
```

### Recipe 3: Recurring-pattern detection

```python
# Daily: top complaint topics last 7 days
weekly_complaints = notion.query(triage_db, filter={'Type':'complaint','Received_at__gte': now - 7d})
topics = Counter(extract_topic(c['text']) for c in weekly_complaints)
for topic, count in topics.most_common(5):
    if count >= 3:
        slack.post('#product-feedback',
            f"Recurring complaint: '{topic}' — {count} reports in 7 days")
        # Auto-create HubSpot deal / issue ticket
        mcp.hubspot.create_ticket(
            subject=f"Recurring social complaint: {topic}",
            pipeline='product_feedback', priority='medium',
            properties={'count_7d': count, 'sample_urls': [c['url'] for c in weekly_complaints[:5]]}
        )
```

### Recipe 4: Hand-off DM template

```
Hi {first_name},

Thanks for flagging this on {channel}.

Could you share:
1. Your order number / account email
2. A brief description of what went wrong
3. Any screenshots if relevant

Our support team will reply within 4 hrs (often faster). I'll keep an eye on this thread.

— {social_team_member_name}
```

### Recipe 5: Handoff to customer-support-agent

```python
# Once context gathered in DM, escalate
mcp.customer_support_agent.handle(
    channel=eng['channel'],
    customer_email=customer_email,
    issue_summary=summary_from_dm,
    ticket_id=hubspot_ticket_id,
    priority='high' if eng['urgency'] == 'urgent' else 'medium',
    social_context_url=eng['url']
)
```

### Recipe 6: Public-resolution loop-back

```python
# After support resolves ticket, agent posts public-thread update
@on_ticket_resolved(channel='support')
def loop_back(ticket):
    if ticket['source'] != 'social':
        return
    original_engagement = notion.query(triage_db, filter={'Ticket ID': ticket['id']})[0]
    public_update = (f"@{original_engagement['author_handle']} — happy to confirm this is resolved. "
                     "Thanks for the patience. DMs open if anything else comes up.")
    mcp.buffer.respond_to_engagement(id=original_engagement['response_id'], text=public_update)
    notion.update(original_engagement['notion_id'], {
        'Status': 'closed',
        'Resolved at': now(),
        'Resolution notes': ticket['resolution_summary']
    })
```

### Recipe 7: Priority assignment

```python
def determine_priority(eng):
    text = eng['text'].lower()
    if any(w in text for w in ['lawsuit', 'sue', 'reporter', 'press', 'illegal', 'fraud']):
        return 'critical'  # PR-level
    if eng.get('reach', 0) > 100_000:
        return 'critical'  # high-visibility
    if any(w in text for w in ['refund', 'broken', 'down', 'outage']):
        return 'high'
    if any(w in text for w in ['question', 'how do i']):
        return 'medium'
    return 'low'
```

### Recipe 8: Sprout Social inbox-routing rule (enterprise)

```python
# Configure rule via Sprout API
mcp.sprout.create_inbox_rule(
    name='Auto-route support requests',
    conditions={
        'message_type': 'inbound',
        'keywords': ['refund', 'broken', 'help', 'cancel', 'where is my order', 'lost package']
    },
    actions={
        'add_tags': ['support_queue', 'sla_15min'],
        'assign_user_id': SUPPORT_LEAD_ID,
        'priority': 'high',
        'notify_via_webhook': WEBHOOK_URL
    }
)
```

### Recipe 9: Auto-generated public-acknowledge response variants

```python
# Avoid identical replies (algorithm flag)
ACK_VARIANTS = [
    "Sorry to hear this — DMing you now to make it right.",
    "That's not the experience we want. DMing you to get this fixed.",
    "Apologies for the trouble — sliding into your DMs to sort this out.",
    "On it — opening a DM now to help.",
    "Genuinely sorry. DMing you for the details.",
]
def pick_ack(): return random.choice(ACK_VARIANTS)
```

### Recipe 10: Weekly support-from-social report

```python
weekly = notion.query(triage_db, filter={'Type':'complaint','Received_at__gte': week_start})
report = {
    'total_complaints': len(weekly),
    'avg_ack_time_min': mean([c['ack_at'] - c['received_at'] for c in weekly]),
    'resolved_within_4h': len([c for c in weekly if c['resolved_at'] - c['received_at'] < 4*3600]),
    'sla_breaches': len([c for c in weekly if c['ack_at'] - c['received_at'] > 15*60]),
    'top_topics': Counter([c['topic'] for c in weekly]).most_common(5),
    'top_channels': Counter([c['channel'] for c in weekly]).most_common(),
}
slack.post('#support-weekly', format_report(report))
```

## Examples

### Example A: Single-complaint flow

```yaml
timeline:
  t+0: customer @user posts "My order #1234 arrived broken" on IG
  t+3min: agent classifies as complaint
  t+5min: agent public-replies "Sorry — DMing you now to fix this"
  t+5min: agent opens IG DM, asks for details
  t+12min: customer replies with photo + details
  t+13min: agent creates HubSpot ticket, hands off to customer-support-agent
  t+30min: support replies with refund + replacement offer
  t+45min: agent loops back to public thread with resolution note
metrics:
  ack_time: 5 min (within 15-min SLA)
  resolution_time: 45 min (well within 4-hr SLA)
```

### Example B: Recurring complaint pattern → product feedback

```yaml
week_of: 2026-06-08
recurring_complaint:
  topic: "checkout broken on Safari"
  count: 7 complaints in 5 days
  channels: [3 IG, 2 X, 1 TikTok, 1 LinkedIn]
detection: Recipe 3 trigger
escalation:
  - HubSpot product-feedback ticket created
  - Slack #engineering ping with ticket link
  - Internal: schedule emergency review
external_messaging:
  - update brand bio link to "Safari checkout issue — fix in progress"
  - DM all 7 affected customers when fix ships
```

### Example C: Critical complaint (PR risk)

```yaml
trigger: viral X thread "Brand X stole my data" with 50k retweets
classifier_output: priority=critical (lawsuit + press keywords + reach > 100k)
escalation_chain:
  - immediate Slack #crisis ping
  - escalate to social-crisis-comms skill
  - legal team CC
  - PR team CC
public_response:
  - 60-min holding statement (from social-crisis-comms 3-variant draft)
  - acknowledge, commit to investigation timeline
  - reply individually to top-amplifier accounts (not just OP)
```

## Edge cases

### Channel-specific DM availability
- IG: must follow customer for some DM features
- X: open DMs vs message requests
- LinkedIn: connection request needed for personal accounts
- TikTok: DMs limited to mutual follows in some regions

Workaround: ask customer to follow / send connection request first. Slows resolution but unavoidable.

### Customer doesn't reply in DM
After 24 hrs no response, polite check-in:
"Hi @user — still here when you're ready to dig into this. Just reply when you have time."

After 72 hrs, close ticket as "abandoned" with note. Reopen if customer returns.

### Sentiment classifier wrong on sarcasm
"Great product!" with -0.8 sentiment (sarcasm) — Brand24 2026 model handles; baseline VADER may miss. Hand-review borderline cases.

### Confidential info in public thread
Customer pastes order number / email publicly. Acknowledge, then DM and ask to delete the public comment with PII.

### Complaint-baiting (manufactured outrage)
Some accounts post to bait response. Quick public acknowledgment but don't engage in back-forth publicly. Document in triage DB.

### Repeat-complainer escalation
Same user, 5+ complaints in 90 days = pattern. Flag account: chronic-issue OR potentially-a-troll. Loop-back to support manager for review.

### Cross-platform same-customer
@user_X on Twitter = @user_ig on Instagram (same human). If posting same complaint across, consolidate to one ticket; don't double-ack.

### Brand-bait by competitor
Competitor's marketing team posing as upset customer. Look for new accounts, no profile, generic complaints. Don't ban-hammer; ack politely + escalate internally.

### Language coverage
Spanish / Portuguese / Mandarin DMs require multilingual support. Use `deepl-mcp` to translate; route to language-specific support tier.

### After-hours coverage
Brand without 24/7 social support: automated ack response — "Got it; team's offline, will reply by 9am [local time tomorrow]."

### Cross-platform routing visibility
Customer posts on IG; support resolves via email; customer wonders why no IG reply. Recipe 6 loop-back handles.

### GDPR / CCPA on DMs + tickets
DM transcripts contain PII. Document retention 365 days. User can request export / deletion under GDPR.

### Escalating internally
Don't keep escalating up org chart on every complaint. Tier 1 social-agent → tier 2 customer-support-agent → tier 3 manager (only for critical / VIP).

## Sources

- **Sprout Social — scheduling + inbox tools**: https://sproutsocial.com/insights/social-media-scheduling-tools/
- **Sprout Social — customer-care SLA**: https://sproutsocial.com/insights/social-customer-care-benchmark/
- **Agorapulse Inbox Assistant**: https://www.agorapulse.com/inbox-assistant/
- **HubSpot Service Hub API**: https://developers.hubspot.com/docs/api/conversations/conversations
- **Zendesk API**: https://developer.zendesk.com/api-reference/
- **Buffer engagements API**: https://buffer.com/developers/api
- **Role.md "Community engagement playbook" — SLA matrix**
