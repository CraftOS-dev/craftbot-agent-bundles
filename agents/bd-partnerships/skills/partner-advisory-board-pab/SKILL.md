<!--
Source: https://www.crossbeam.com/blog/partner-advisory-board/ + https://www.forrester.com/report/the-forrester-wave-partner-advisory-board/ + https://www.allbound.com/blog/partner-advisory-board
Partner Advisory Board (PAB) — quarterly summit + roadmap synthesis (June 2026 SOTA).
-->
# Partner Advisory Board (PAB) — SKILL

Convene 6-12 strategic partners quarterly (annual in-person summit + quarterly virtual) to advise on roadmap, GTM, pricing, ecosystem. Produces prioritized partner-influenced roadmap items handed to `product-manager`. Operates membership selection, pre-read assembly, summit logistics, recording, structured feedback synthesis, action-item tracking, and next-quarter follow-through.

## When to use

- **Standing up a new PAB** — selection criteria + first-cohort invitation.
- **Quarterly virtual PAB meeting** — 60-90 min agenda + pre-read + minutes.
- **Annual in-person summit** — 2-day agenda + logistics + pre-read deck + post-summit synthesis.
- **Adding / rotating members** — annual refresh, performance-based.
- **Post-summit roadmap synthesis** — partner feedback → product-manager backlog inputs.
- **Tracking PAB action items** — owner + due-date + status.
- **Member NPS on PAB experience** — keeps engagement high.
- **Trigger phrases**: "schedule next PAB", "PAB members for Q3", "PAB pre-read deck", "PAB summit agenda", "PAB feedback synthesis", "promote partner X to PAB".

Do NOT use this skill for: **product roadmap planning** (cross-agent: `product-manager`); **per-partner QBR** (use `partner-scorecard-authoring` QBR sub-routine); **co-marketing campaign design** (use `co-marketing-campaign-design`); **partner certification programs** (use `partner-enablement-certification-programs`).

## Setup

```bash
export MATON_API_KEY="<key>"
export NOTION_API_KEY="<key>"
export GOOGLE_CALENDAR_TOKEN="<token>"
export ZOOM_OAUTH_TOKEN="<token>"
export GMAIL_OAUTH_TOKEN="<token>"
export SLACK_BOT_TOKEN="<token>"
```

**One-time Notion DBs:**
- `PAB Members` (member, partner_id, tier, term_start, term_end, attendance_rate, NPS_on_PAB, status)
- `PAB Meetings` (date, format, agenda, pre-read URL, recording URL, attendees, decisions)
- `PAB Action Items` (item, owner, due, status, linked partner, source meeting)
- `PAB Roadmap Inputs` (item, supporting members, theme, priority, product-manager hand-off date)

## Common recipes

### Recipe 1: Select PAB cohort (annual)

```sql
-- Candidate query: top-tier + 2+ quarters relationship + segment coverage
SELECT p.partner_id, p.partner_name, p.tier, p.motion,
       p.segment, p.geo,
       q.opps_sourced_l4q, q.closed_won_l4q, q.nps_score_last
FROM partners p
JOIN partner_quarterly_rollup q USING(partner_id)
WHERE p.status='active'
  AND p.tier IN ('gold','strategic')
  AND DATE_PART('month', AGE(NOW(), p.start_date)) >= 6
  AND q.nps_score_last >= 7
ORDER BY q.opps_sourced_l4q DESC, p.segment, p.geo;
```

Manual layer: balance for segment + geo + motion mix; target 6-12 members; document selection rationale in Notion.

### Recipe 2: Send PAB invitation

```python
def invite_to_pab(partner_id, member_email, member_name, partner_name, term_start, term_end):
    body = f"""Hi {member_name.split()[0]},

We'd be honored to invite {partner_name} to our Partner Advisory Board for the {term_start.year} cohort.

Commitment:
- 4 quarterly virtual meetings (60-90 min) + 1 annual in-person summit (2 days)
- Pre-read review (~30 min/quarter)
- Honest feedback on roadmap, GTM, pricing, ecosystem

What you'll get:
- Earliest preview of our roadmap
- Direct influence on what we build
- Peer network with other strategic partners
- $25K MDF credit per PAB-year (non-negotiable spend criteria)

Term: {term_start.strftime('%b %Y')} → {term_end.strftime('%b %Y')}

Reply YES to confirm. We'll send the first pre-read 2 weeks before the kickoff.

— Sarah, VP Partnerships"""
    gmail_send(to=member_email, subject=f"Invitation: {partner_name} → Partner Advisory Board", body=body)
    notion.pages.create(parent={"database_id":PAB_MEMBERS_DB},
        properties={
            "Member":{"title":[{"text":{"content":member_name}}]},
            "Partner ID":{"rich_text":[{"text":{"content":partner_id}}]},
            "Term start":{"date":{"start":term_start.isoformat()}},
            "Term end":{"date":{"start":term_end.isoformat()}},
            "Status":{"select":{"name":"invited"}},
        })
```

### Recipe 3: Schedule quarterly meeting (Zoom + Calendar)

```bash
# Create Zoom webinar/meeting via zoom-mcp
curl -X POST "https://api.zoom.us/v2/users/me/meetings" \
  -H "Authorization: Bearer $ZOOM_OAUTH_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "topic":"Partner Advisory Board — Q3 2026",
    "type":2,
    "start_time":"2026-08-15T15:00:00Z",
    "duration":90,
    "timezone":"UTC",
    "settings":{
      "host_video":true,"participant_video":true,
      "join_before_host":false,
      "auto_recording":"cloud",
      "registration_type":1
    }
  }'

# Calendar invites to all members
curl -X POST "https://www.googleapis.com/calendar/v3/calendars/primary/events" \
  -H "Authorization: Bearer $GOOGLE_CALENDAR_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "summary":"Partner Advisory Board — Q3 2026",
    "description":"Pre-read: [Notion link]. Agenda enclosed. Zoom link in calendar.",
    "start":{"dateTime":"2026-08-15T15:00:00Z"},
    "end":{"dateTime":"2026-08-15T16:30:00Z"},
    "attendees":[{"email":"member1@partnerA.com"},{"email":"member2@partnerB.com"}],
    "conferenceData":{"createRequest":{"requestId":"pab-q3-2026"}}
  }'
```

### Recipe 4: Assemble pre-read deck (1 week prior)

Pre-read structure (~15-20 slides, drafted in `pptx` via `canva-mcp`):

```
Slide 1: Agenda + outcomes
Slide 2: State of partner program (numbers: # partners, revenue, NPS, tier mix)
Slide 3-4: Year/Quarter wins (top 5)
Slide 5-6: Year/Quarter challenges (top 3, with asks)
Slide 7-10: Roadmap preview — items where we want PAB input (3-5 items)
Slide 11-12: GTM motions — where we'd like to align
Slide 13-14: Pricing / packaging shifts under consideration
Slide 15: Specific asks per member (acknowledge their context)
Slide 16-17: Discussion questions (3-5 prompts)
Slide 18: Logistics + Q&A
```

Render via `pptx`/`canva-mcp`; share via `notion` page + email (Recipe 5).

### Recipe 5: Distribute pre-read 7 days prior

```python
def distribute_pre_read(meeting_id):
    members = notion_query(PAB_MEMBERS_DB, filter={"Status":"active"})
    pre_read_url = notion_page_url(meeting_id)
    for m in members:
        gmail_send(to=m["email"], subject=f"PAB Pre-Read — {meeting_id}",
                   body=f"""Hi {m['first_name']},

Pre-read for our PAB session next week is here: {pre_read_url}

Specifically interested in your take on:
{m['custom_ask']}

See you {meeting_date_human()}.

— Sarah""")
```

### Recipe 6: Run feedback workshop (in-meeting facilitation)

Structured feedback format (during summit):

```
For each roadmap item:
  Round 1 (15 min): Silent post-it / Notion comment — "What's missing? What's surprising? What concerns?"
  Round 2 (15 min): Cluster + discuss top 3 themes
  Round 3 (10 min): Vote on priority (each member 5 dots)
  Round 4 (10 min): Capture commitments + open questions
```

Capture via `notion` page with sub-pages per roadmap item.

### Recipe 7: Annual summit logistics

```python
def book_summit_logistics(summit_dates, location, attendee_count):
    items = [
        ("Venue + AV", "external_vendor", summit_dates[0] - timedelta(days=90)),
        ("Hotel block + travel guidance", "ops", summit_dates[0] - timedelta(days=60)),
        ("Dietary survey to members", "ops", summit_dates[0] - timedelta(days=45)),
        ("Detailed agenda + speakers locked", "vp_partnerships", summit_dates[0] - timedelta(days=30)),
        ("Pre-read deck v1 shipped", "vp_partnerships", summit_dates[0] - timedelta(days=14)),
        ("Travel reminders", "ops", summit_dates[0] - timedelta(days=7)),
        ("Day-of run-of-show + speaker prep", "vp_partnerships", summit_dates[0] - timedelta(days=2)),
    ]
    for item, owner, due in items:
        notion.pages.create(parent={"database_id":PAB_ACTION_ITEMS_DB},
            properties={
                "Item":{"title":[{"text":{"content":item}}]},
                "Owner":{"rich_text":[{"text":{"content":owner}}]},
                "Due":{"date":{"start":due.isoformat()}},
                "Status":{"select":{"name":"open"}},
            })
```

### Recipe 8: Post-summit synthesis (1 week post)

```python
def synthesize_pab_feedback(meeting_id):
    # Pull all in-meeting Notion comments + recording transcript
    transcript = fathom_get_transcript(meeting_id)
    comments = notion_get_comments(meeting_id)
    raw = "\n".join([c["text"] for c in comments] + [transcript])

    # Cluster themes (manual or LLM-assisted)
    themes = cluster_themes(raw)  # e.g., ["Pricing simplification","Integration depth","EU GTM","SLA tiers"]

    # Create roadmap inputs in Notion
    for t in themes:
        notion.pages.create(parent={"database_id":PAB_ROADMAP_INPUTS_DB},
            properties={
                "Theme":{"title":[{"text":{"content":t['name']}}]},
                "Supporting members":{"multi_select":[{"name":m} for m in t['supporters']]},
                "Priority":{"select":{"name":t['vote_priority']}},
                "Source meeting":{"rich_text":[{"text":{"content":meeting_id}}]},
            })

    # Hand off to product-manager
    publish_event("product-manager.pab-roadmap-inputs", {"meeting":meeting_id, "themes":themes})
```

### Recipe 9: Thank-you + synthesis distribution

```python
def thank_you_and_synthesis(meeting_id):
    members = notion_query(PAB_MEMBERS_DB, filter={"Status":"active"})
    synthesis_url = notion_page_url(meeting_id + "-synthesis")
    for m in members:
        gmail_send(to=m["email"], subject=f"PAB {meeting_id} — Thank you + synthesis",
                   body=f"""Hi {m['first_name']},

Thank you for the candid feedback. Synthesis here: {synthesis_url}

Top 3 roadmap shifts your feedback drove:
{ format_top_3_changes() }

Next meeting: {next_meeting_date()}. Pre-read 2 weeks prior.

— Sarah""")
```

### Recipe 10: Member attendance + NPS tracking

```sql
-- Attendance rate per member (last 4 meetings)
SELECT m.member_name, m.partner_name,
       COUNT(*) FILTER (WHERE a.attended) AS attended,
       COUNT(*) AS scheduled,
       ROUND(COUNT(*) FILTER (WHERE a.attended)::numeric / COUNT(*), 2) AS attendance_rate
FROM pab_members m
JOIN pab_attendance a USING(member_id)
JOIN pab_meetings mt ON a.meeting_id = mt.id
WHERE mt.date >= NOW() - INTERVAL '12 months'
GROUP BY m.member_name, m.partner_name
HAVING ROUND(COUNT(*) FILTER (WHERE a.attended)::numeric / COUNT(*), 2) < 0.6;
```

< 60% attendance → rotation conversation.

### Recipe 11: Roadmap input hand-off to product-manager

```python
def handoff_to_product_manager(meeting_id):
    inputs = notion_query(PAB_ROADMAP_INPUTS_DB, filter={"Source meeting":meeting_id})
    publish_event("product-manager.pab-inputs", {
        "meeting": meeting_id,
        "inputs": [{
            "theme": i["theme"],
            "supporting_members": i["supporting_members"],
            "priority_vote": i["priority"],
            "context": i["notes"],
        } for i in inputs],
        "suggested_action": "review at next backlog refinement; status back to bd-partnerships in 30 days",
    })
```

## Examples

### Example 1: Q3 2026 virtual PAB — pricing simplification feedback drives roadmap shift

**Goal:** 90-min Q3 PAB; gather feedback on proposed pricing simplification.

**Steps:**
1. Recipe 3 — Zoom + Calendar invites to 10 members 30 days prior.
2. Recipe 4 — Pre-read deck (15 slides) authored; pricing scenarios on slides 8-12.
3. Recipe 5 — Pre-read distributed 7 days prior; 80% read-completion.
4. Recipe 6 — In-meeting structured feedback: 6/10 members support simplification; 4/10 raise channel-conflict concerns about discount tiers.
5. Recipe 8 — Post-meeting synthesis identifies "discount-tier conflict" as a theme.
6. Recipe 11 — Hand off to `product-manager` with cited PAB-member feedback.
7. Pricing v2 ships next quarter incorporating PAB input.

**Result:** Pricing decision risk-mitigated; PAB feels heard; product-manager has clean roadmap input.

### Example 2: Annual summit — partners co-define 2027 ecosystem strategy

**Goal:** 2-day in-person summit with 12 PAB members.

**Steps:**
1. Recipe 7 — Logistics locked 90 days prior.
2. Day 1 morning: vendor strategic update + roadmap preview.
3. Day 1 afternoon: structured feedback workshop on 4 roadmap items.
4. Day 2 morning: joint GTM session.
5. Day 2 afternoon: ecosystem strategy co-design.
6. Recipe 8 + 9 — Within 7 days, synthesis published + emailed.
7. 3 roadmap shifts attributed to summit feedback in next product release.

**Result:** Highest-engagement PAB event; partner buy-in for 2027 strategy; partners share strategy at QBRs.

### Example 3: Member rotation — replacing low-attendance member

**Goal:** One member missed 3 of last 4 meetings; rotate.

**Steps:**
1. Recipe 10 — Attendance query surfaces 50% rate.
2. 1:1 call with member — life context; offers to step off.
3. Recipe 1 — Candidate query identifies replacement; segment + motion balance preserved.
4. Recipe 2 — Invitation sent to replacement.
5. Notion DB updated: outgoing → `inactive`, incoming → `invited` → `active`.
6. Thank-you note + farewell to outgoing.

**Result:** PAB cohort stays high-engagement; member-relationship preserved on the way out.

## Edge cases / gotchas

- **Membership selection bias** — top-revenue partners only blinds you to mid-tier voices. Reserve 2-3 seats for "rising-star" partners.
- **Geo + motion coverage** — APAC/EMEA/AMER reps + referral/reseller/integration/OEM mix or feedback is narrow.
- **Member tenure cap** — 2-year terms; renewal up to 4 years max.
- **NDA scope** — must cover roadmap + financials + pricing.
- **Pre-read read-rate** — < 60% completion = meeting wastes 20 min. Track via Notion analytics; chase non-readers 48h prior.
- **Feedback workshop facilitation** — loudest voice dominates without structure. Use silent post-its first.
- **Action-item rot** — un-actioned items destroy trust. Publish dashboard quarterly.
- **Conflict of interest** — competitor partners disclosed; sub-session for sensitive topics.
- **Cancellation cascade** — hold at 60% threshold; document decisions for absent members.
- **Vendor stakeholder bloat** — cap to CRO + CPO + VP Partnerships + 1 PM.
- **Time-zone tax + post-summit drop-off** — rotate meeting time zones quarterly; Recipe 9 synthesis within 7 days.

## Sources

- Crossbeam PAB guide: https://www.crossbeam.com/blog/partner-advisory-board/
- Forrester partner advisory board wave: https://www.forrester.com/report/the-forrester-wave-partner-advisory-board/
- Allbound PAB: https://www.allbound.com/blog/partner-advisory-board
- Zoom Meetings API: https://developers.zoom.us/docs/api/rest/reference/zoom-api/
- Notion API: https://developers.notion.com/
