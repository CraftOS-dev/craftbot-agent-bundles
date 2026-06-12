<!--
Source: https://www.bevy.com/ + https://api.slack.com/connect + https://discord.com/developers/docs + https://developers.zoom.us/docs/api/
-->
# Customer Advisory Board — CAB — SKILL

Build and run a 8-12 customer Customer Advisory Board: roster curation, quarterly all-hands cadence, monthly drumbeat, between-meeting community channel (Bevy / Slack Connect / Discord). Roadmap previews via Loom + Figma; transcripts via Fathom; feedback log in Notion. Refresh roster annually; rotate 25% out.

## When to use

- **CAB founding** — first build of a CAB; need roster + cadence + first meeting.
- **Quarterly all-hands prep** — 21 days out; need agenda + panelists + materials.
- **Roster refresh** — annual; rotate 25%.
- **CAB Discord/Slack moderation** — between-meeting community signals to surface.
- **CAB feedback synthesis** — quarterly meeting outputs -> Linear roadmap input.
- **CAB advocacy synergies** — CAB members are natural references/case studies.

This skill **feeds** `voice-of-customer-reporting` (CAB feedback contributes to VOC themes) and `customer-advocacy-case-study-reference` (CAB members often advocate beyond reference).

Trigger phrases: "CAB", "customer advisory board", "advisory board meeting", "CAB community", "CAB roster", "roadmap preview".

## Setup

```bash
# Bevy (community platform)
export BEVY_API_KEY="<key>"

# Mighty Networks (alt)
export MIGHTY_API_KEY="<key>"

# Slack Connect for B2B CAB channels - slack-mcp wired
# Discord for community-style CAB - discord-mcp-full wired
# Zoom for quarterly all-hands - zoom-mcp wired
# Fathom for transcript - default skill
# Calendly for booking - default skill
# Notion for roster + feedback log - notion-mcp wired
# Loom share links via gmail-mcp
```

Workspace prerequisites:
- Notion "CAB Roster" DB: Customer, Member Name, Title, Email, Joined Date, Tier, Vertical, Geography, Active? (boolean), Term End Date.
- Notion "CAB Meeting Feedback" DB: Meeting Date, Member, Theme, Verbatim Quote, Impact (Hi/Med/Lo), Routed to (Linear ticket / cross-feed).
- Calendly event type: "CAB Quarterly All-hands" with 1.5h duration.
- Slack Connect channel #cab-acme-community (if Slack-flavored) OR Discord server (if Discord-flavored).

## Roster composition

- **Size:** 8-12 customers (smaller is intimate; bigger loses focus).
- **Mix:** Enterprise-weighted (50%+); Growth tier represented; rare Starter for SMB perspective.
- **Vertical/geo:** spread across 2-4 verticals + 2-3 geos.
- **Each member:** named exec sponsor on customer side (VP+).
- **Refresh:** annual; rotate 25% out gracefully (thank-you gift + offer return as alumni).

## Cadence

| Meeting | Frequency | Duration | Tool |
|---|---|---|---|
| Quarterly all-hands | Quarterly | 90 min | Zoom + Fathom |
| Monthly drumbeat | Monthly | Email | gmail-mcp |
| Roadmap preview | Quarterly | Loom (10-15min) | gmail-mcp share link |
| Community channel | Always-on | - | Slack Connect / Discord |
| 1:1 check-in | Quarterly | 30 min | Calendly + Zoom |

## Common recipes

### Recipe 1: Build initial roster

```python
# Query customers eligible for CAB
candidates = postgres.query("""
SELECT c.customer_id, c.name, c.tier, c.vertical, c.geo, c.csm_owner,
       h.health_score, p.last_promoter_score
FROM customers c
JOIN health_scores h USING (customer_id)
LEFT JOIN promoter_scores p USING (customer_id)
WHERE c.tier IN ('Enterprise', 'Growth')
  AND h.health_score >= 0.75
  AND c.tenure_months >= 6
  AND p.last_promoter_score >= 8
ORDER BY c.arr DESC
""")

# CSM Lead selects 8-12 from candidate list - human in the loop
# Once selected, push to Notion roster
for cab_member in selected:
    notion.create_page(
        parent={"database_id": CAB_ROSTER_DB_ID},
        properties={
            "Customer": {"title": [{"text": {"content": cab_member.name}}]},
            "Member Name": {"rich_text": [{"text": {"content": cab_member.contact_name}}]},
            "Title": {"select": {"name": cab_member.contact_title}},
            "Email": {"email": cab_member.contact_email},
            "Tier": {"select": {"name": cab_member.tier}},
            "Vertical": {"select": {"name": cab_member.vertical}},
            "Geo": {"select": {"name": cab_member.geo}},
            "Joined Date": {"date": {"start": today}},
            "Term End Date": {"date": {"start": one_year_from_today}},
            "Active": {"checkbox": True},
        },
    )
```

### Recipe 2: Onboard CAB member (welcome flow)

```python
gmail.send_email(
    to=[member.email],
    subject=f"Welcome to the {product} Customer Advisory Board",
    body=f"""
Hi {member.name},

You've joined our Customer Advisory Board for {term_length}. Quick onboarding:

1. Quarterly meeting calendar holds (4 dates) attached.
2. Slack Connect / Discord invite: {community_link}
3. CAB charter: {notion_charter_url}

First meeting: {first_meeting_date}. Agenda 3 days before.

Thanks for the time you're investing here.

- {csm_lead.name}, VP {function}
"""
)
```

### Recipe 3: Set up Bevy CAB community

```bash
# Create CAB chapter on Bevy
curl -sS -X POST "https://api.bevy.com/v1/chapters" \
  -H "Authorization: Bearer $BEVY_API_KEY" \
  -d '{
    "name": "Acme Customer Advisory Board",
    "type": "private",
    "members": [...]
  }'
```

Doc: https://www.bevy.com/

### Recipe 4: Set up Slack Connect CAB channel

Via `slack-mcp conversations_create` with `is_private: true`. Invite members one by one via Slack Connect.

Charter post (pin):
```
# CAB community channel

Use this channel for:
- Async questions on roadmap previews
- Sharing your use case wins
- Feedback on early-access features

We commit to:
- Replying within 1 business day
- Posting roadmap previews monthly
- Honoring confidentiality (no public sharing of preview material)

For sensitive feedback, DM {csm_lead.name}.
```

### Recipe 5: Set up Discord CAB server

Via `discord-mcp-full guild_create` if standing up a new server; or `channel_create` in existing community Discord.

Roles: `cab-member`, `cab-alumni`, `acme-team`. Channels: `#welcome`, `#roadmap-previews`, `#feedback`, `#community-share`.

### Recipe 6: T-21 quarterly meeting prep

```python
# Pull agenda items from:
# 1. Voice-of-customer themes since last meeting (voice-of-customer-reporting)
# 2. Roadmap themes from Linear (next 6 months)
# 3. Open feedback items from previous meeting

# Notion meeting page
notion.create_page(
    parent={"database_id": CAB_MEETINGS_DB_ID},
    properties={
        "Date": {"date": {"start": meeting_date}},
        "Attendees": {"people": cab_member_ids},
    },
    children=[
        {"object": "block", "type": "heading_2",
         "heading_2": {"rich_text": [{"text": {"content": "Agenda"}}]}},
        {"object": "block", "type": "numbered_list_item",
         "numbered_list_item": {"rich_text": [{"text": {"content": "Welcome + state of union (10min)"}}]}},
        # ... etc
    ],
)
```

### Recipe 7: Create Zoom for quarterly meeting

```bash
curl -sS -X POST "https://api.zoom.us/v2/users/me/meetings" \
  -H "Authorization: Bearer $ZOOM_OAUTH_TOKEN" \
  -d '{
    "topic": "CAB Q3 2026 - All-hands",
    "type": 2,
    "start_time": "2026-08-20T16:00:00Z",
    "duration": 90,
    "settings": {
      "auto_recording": "cloud",
      "host_video": true,
      "waiting_room": true
    }
  }'
```

### Recipe 8: T-3 monthly drumbeat email

```python
gmail.send_email(
    to=cab_member_emails,
    subject=f"CAB drumbeat - {month_name}",
    body=f"""
Hi CAB,

3 things this month:

1. Roadmap preview: {loom_link}
   (15 min video. Focus on {theme_1} + {theme_2}.)

2. Quick poll: how would you weigh {trade_off}?
   {survey_link}

3. Next meeting confirmed for {next_meeting_date}.

Anything you want on the agenda? Drop in #cab-community.

- {csm_lead.name}
"""
)
```

### Recipe 9: T+1 meeting recap + action items

```python
# After meeting, pull Fathom transcript + summary
transcript = fathom.get_transcript(meeting_id=zoom_id)
summary = fathom.get_summary(meeting_id=zoom_id)

# Claude extracts:
# - Themes raised by CAB members
# - Verbatim quotes worth saving
# - Action items (us + customer-side)

prompt = f"""
From this CAB meeting transcript, extract:
1. Top 3 themes raised by members
2. Best verbatim quotes (2-3 sentences each)
3. Action items - who, what, by when

Tag each theme: product / support / sales / marketing.
"""
extracted = claude.generate(prompt, attachments=[transcript])

# Write to Notion meeting feedback DB - one row per theme
for theme in extracted.themes:
    notion.create_page(
        parent={"database_id": CAB_FEEDBACK_DB_ID},
        properties={
            "Meeting Date": {"date": {"start": meeting_date}},
            "Theme": {"title": [{"text": {"content": theme.label}}]},
            "Verbatim": {"rich_text": [{"text": {"content": theme.quote}}]},
            "Impact": {"select": {"name": theme.impact}},
            "Tag": {"select": {"name": theme.tag}},
        },
    )

# Recap email
gmail.send_email(
    to=cab_member_emails,
    subject=f"CAB Q3 recap + next steps",
    body=recap_template,
)
```

### Recipe 10: Route product-tagged feedback to Linear

```python
# For each product-tagged theme, create Linear issue
for theme in extracted.themes:
    if theme.tag == "product":
        linear.create_issue(
            title=f"[CAB] {theme.label}",
            description=f"""
Source: CAB Q3 2026 ({meeting_date})
Members agreeing: {member_count}
Verbatim: "{theme.quote}"
Impact: {theme.impact}
""",
            labels=["cab", "voice-of-customer"],
            team_id=PRODUCT_TEAM_ID,
        )
```

### Recipe 11: Quarterly 1:1 check-ins

For each CAB member, book a 30-min 1:1 with their CSM via Calendly. Calendar holds + check-in agenda.

```python
calendly.create_scheduling_link(
    event_type=ONE_ON_ONE_EVENT_TYPE,
    max_event_count=1,
)
```

### Recipe 12: Annual roster refresh

```python
# Identify rotation candidates (term end approaching + low engagement)
expiring = postgres.query("""
SELECT * FROM cab_roster
WHERE term_end_date < CURRENT_DATE + INTERVAL '60 days'
ORDER BY engagement_score ASC LIMIT 3
""")

# For each: thank-you email + alumni invitation
for member in expiring:
    gmail.send_email(
        to=[member.email],
        subject=f"Thank you - {term_length} of CAB membership",
        body=alumni_invitation_template,
    )
    # Mark as alumni in Notion
    notion.update_page(page_id=member.notion_id, properties={
        "Active": {"checkbox": False},
        "Alumni": {"checkbox": True},
    })

# Recipe 1 again to identify replacements
```

## Examples

### Example 1: Stand up CAB from scratch

**Goal:** Founding 8-member CAB live within 30 days.

**Steps:**
1. Week 1: Recipe 1 (build candidate list).
2. Week 1-2: CSM Lead does 1:1 outreach to invite top 8.
3. Week 2: Recipe 2 onboarding emails sent.
4. Week 3: Recipe 4 / 5 (community channel) live.
5. Week 4: Recipe 6 / 7 first quarterly meeting prepped.

**Result:** CAB launched, first meeting on calendar.

### Example 2: Quarterly meeting end-to-end

**Goal:** Q3 all-hands runs smoothly; outputs synthesized within 3 days.

**Steps:**
1. T-21: Recipe 6 agenda drafted; Recipe 7 Zoom + Fathom set.
2. T-7: pre-read sent (roadmap Loom + previous quarter's actions).
3. T-3: Recipe 8 reminder email.
4. T-0: Meeting held with Fathom recording.
5. T+1: Recipe 9 recap + Recipe 10 Linear issues.
6. T+3: Loom of meeting highlights to absentees.

**Result:** CAB feedback loop closes within 72h.

## Edge cases / gotchas

- **CAB members not equal customers** — they're a specific contact at a customer. Customer can be Yellow health and still have an awesome CAB member.
- **NDA-bound feedback** — CAB is private; never quote a CAB member publicly without explicit permission.
- **Member churns from customer org mid-term** — replace with another contact at same customer if possible; else rotate.
- **Customer churns** — if customer churns mid-term, CAB member becomes alumni; do exit interview as bonus VOC input.
- **Discord vs Slack** — pick one; running both = no one in either.
- **Bevy is paid + heavyweight** — for <12 members, Slack Connect or Discord is sufficient.
- **Loom roadmap preview leaks** — competitor sees your roadmap; require auth-gate or watermark Loom.
- **CAB doesn't get to dictate roadmap** — they advise. Product owns decisions. Set expectation at onboarding.
- **CAB fatigue** — same 8 people 4x/year + monthly nudges = burnout. Track engagement (Recipe 12 input); rotate proactively.
- **Compensation / sponsorship** — for CAB members investing significant time, formal compensation possible (gift cards, conference stipends, equity advisory in rare cases). Check tax + legal.
- **CSM Lead absent for CAB meeting** — chair must be senior + named. VP CS chairs; CSM Leads support.
- **Action items go cold** — pin in Notion CAB meetings DB; review every quarter; close or revisit explicitly.

## Sources

- [Bevy chapter API docs](https://www.bevy.com/)
- [Mighty Networks API](https://www.mightynetworks.com/)
- [Slack Connect docs](https://api.slack.com/connect)
- [Slack conversations.create](https://api.slack.com/methods/conversations.create)
- [Discord guild/channel create](https://discord.com/developers/docs/resources/guild)
- [Zoom Meetings API](https://developers.zoom.us/docs/api/meetings/)
- [Fathom transcripts API](https://help.fathom.video/en/articles/8430832-fathom-api)
- [Linear issues API](https://developers.linear.app/docs/graphql/working-with-the-graphql-api)
- [Notion API create page](https://developers.notion.com/reference/post-page)
- [Forrester CAB best practices](https://www.forrester.com/blogs/category/customer-advisory-board/)
- [Calendly scheduling links](https://developer.calendly.com/api-docs/)
