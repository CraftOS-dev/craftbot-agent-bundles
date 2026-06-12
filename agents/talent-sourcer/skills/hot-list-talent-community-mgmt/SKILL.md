<!--
Sources: https://beamery.com/resources/blogs/why-enterprise-organizations-need-an-alumni-hiring-strategy
         https://www.metaview.ai/resources/blog/recruiting-trends
         https://www.gem.com/blog/candidate-sourcing-software
Hot-list patterns hire 30-50% faster. Tag by readiness (1-3 mo / 6-12 mo / future) + role family.
Quarterly newsletter via Gem / Mailchimp; ad-hoc query when req opens.
-->
# Hot-List + Talent Community Management — SKILL

Maintain pre-engaged candidate pools tagged by readiness + role family. Query first when a req opens (hot-list candidates convert 3-5× faster than cold). Quarterly newsletter nurture; ad-hoc event invites. Saves 30-50% time-to-fill on roles where the hot-list has matches.

## When to use

- User wants to **add a candidate to the hot-list** after a "not now" reply or pipeline-passive screen.
- User wants to **query the hot-list when a req opens** (BEFORE cold sourcing).
- User wants to **run a quarterly newsletter** to the talent community.
- User wants to **invite hot-list segments to a virtual event** (engineering AMA, design crit, etc.).
- Trigger phrases: "add to hot-list", "query hot-list", "talent community", "nurture newsletter", "AMA invite", "tag readiness".

Do not use for: boomerang / alumni-specific re-engagement (`boomerang-alumni-re-engagement` — alumni have different cadence + data schema); diversity-channel community management (`diversity-channel-sourcing-dev-color-code2040` — those are external communities).

## Setup

```bash
# Primary database — Notion.
# Schema: candidates table in candidate-database workspace.
export NOTION_API_KEY="secret_xxx"
export NOTION_HOT_LIST_DB="<database_id>"

# CRM (Gem / hireEZ / Beamery) — for sequence enrollment + tag-based queries.
export GEM_API_KEY="xxx"

# Newsletter — Mailchimp preferred; gmail-mcp fallback for <500 list.
export MAILCHIMP_API_KEY="xxx"
export MAILCHIMP_LIST_ID="xxx"
export MAILCHIMP_DC="us1"  # data center prefix
```

## Common recipes

### Recipe 1: Hot-list tag taxonomy (THE schema)

```
# Role × Level × Readiness (always 3 axes)
hot-list-eng-staff-3mo       # staff IC, ready 1-3 months
hot-list-eng-staff-6mo       # staff IC, ready 4-6 months
hot-list-eng-staff-12mo      # staff IC, future / passive
hot-list-eng-manager-6mo
hot-list-eng-manager-12mo
hot-list-design-pd-3mo
hot-list-design-pd-12mo
hot-list-ae-enterprise-3mo
hot-list-ae-smb-6mo
hot-list-exec-cto            # exec — no time-window (always ongoing)

# Source / channel (independent of role)
boomerang-eng                # alumni from your company
boomerang-12mo               # alumni at the 12-month post-departure window
target-account-{slug}        # account-based sourcing (e.g., target-account-stripe)
diversity-channel-devcolor
diversity-channel-code2040
referral-source-{employee-slug}   # referral attribution
silver-medalist-{req-id}     # interviewed-but-not-hired; "we'd hire them in a heartbeat" tag
```

A candidate can carry 3-5 tags. The role-readiness tag is mandatory.

### Recipe 2: Add a candidate to the hot-list (the moment of capture)

```bash
# When a candidate replies "not now" or after a silver-medalist screen:
curl -X POST "https://api.gem.com/v1/prospects/{prospect_id}/tags" \
  -H "Authorization: Bearer $GEM_API_KEY" \
  -d '{"tags": ["hot-list-eng-staff-12mo", "silver-medalist-ENG-2026-04", "referral-source-jdoe"]}'

# Mirror in Notion candidate DB
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "parent": {"database_id": "'$NOTION_HOT_LIST_DB'"},
    "properties": {
      "Name": {"title": [{"text": {"content": "Jane Doe"}}]},
      "Tags": {"multi_select": [{"name": "hot-list-eng-staff-12mo"}, {"name": "silver-medalist-ENG-2026-04"}]},
      "Last Touch": {"date": {"start": "2026-06-09"}},
      "Notes": {"rich_text": [{"text": {"content": "Strong staff IC. Joined Stripe 3 mo back; 12-18 mo window."}}]}
    }
  }'
```

Always capture the moment + the reason for tagging. "Why" matters when re-engaging in 6+ months.

### Recipe 3: Hot-list query when a req opens (THE highest-leverage workflow)

```bash
# Step 1: Query Gem CRM for matching tags + recent touch window
curl "https://api.gem.com/v1/prospects?tags=hot-list-eng-staff-3mo,hot-list-eng-staff-6mo&last_touch_gt=30days&limit=200" \
  -H "Authorization: Bearer $GEM_API_KEY"

# Step 2: Cross-reference Notion candidate DB for full context (notes, last conversation)
curl -X POST "https://api.notion.com/v1/databases/$NOTION_HOT_LIST_DB/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "filter": {
      "and": [
        {"property": "Tags", "multi_select": {"contains": "hot-list-eng-staff-3mo"}},
        {"property": "Last Touch", "date": {"before": "2026-05-09"}}
      ]
    }
  }'
```

Always query hot-list BEFORE cold sourcing. Antipattern 4 in role.md: skipping the hot-list wastes nurture investment.

### Recipe 4: Personalized hook for hot-list re-enrollment

```
# Generic cold InMail subject: "Your ray-core PR" (Recipe 2 in cold-inmail-warm-intro)
# Hot-list re-enrollment subject: "{first}, back when we chatted — your timing might fit now"
# Body opens with: "Hi {first} — when we connected in {month} you mentioned {their_constraint}.
#   That constraint should be resolved now (we just closed Series C). Wanted to reopen the chat."
```

Reference the prior conversation. Hot-list re-engagement that ignores prior context reads as cold.

### Recipe 5: Quarterly newsletter to talent community

```python
# Per-segment newsletter — different content per role family
import mailchimp_marketing as MailchimpMarketing

mailchimp = MailchimpMarketing.Client()
mailchimp.set_config({"api_key": MAILCHIMP_API_KEY, "server": MAILCHIMP_DC})

# Step 1 — segment the list by hot-list-eng vs hot-list-design vs hot-list-sales
segments = ["eng", "design", "sales", "exec"]

for seg in segments:
    campaign = mailchimp.campaigns.create({
        "type": "regular",
        "recipients": {
            "list_id": MAILCHIMP_LIST_ID,
            "segment_opts": {"saved_segment_id": SEGMENT_IDS[seg]}
        },
        "settings": {
            "subject_line": f"Q3 update — {seg} team",
            "from_name": "Sarah Chen — Acme Talent",
            "reply_to": "talent@acme.com"
        }
    })
    # Content per segment: 1 product win + 1 culture story + open roles + alumni spotlight
    mailchimp.campaigns.set_content(campaign["id"], {"html": NEWSLETTER_HTML[seg]})
    mailchimp.campaigns.send(campaign["id"])
```

Newsletter cadence: quarterly. Monthly is annoying; semi-annual loses retention.

### Recipe 6: Newsletter content template (light touch — not a pitch)

```markdown
# Subject: Q3 update — {segment} team

## What we shipped (1 win)
{2-3 sentences on the recent product launch / milestone / metric}. {Link to blog post / video}.

## What we learned (1 culture story)
{1 short story — engineer-perspective; not corporate marketing}. {Link to engineer blog post}.

## Roles open
- {Role 1} — {seniority}, {location}, {comp band if public}. [Apply link]
- {Role 2} — ...

## Alumni spotlight
{Brief story of an alum who joined a great new role}. {Encourage opt-in to LinkedIn alumni group}.

## You can:
- {Reply to chat 1:1 with recruiter}
- {Join Slack community / Discord}
- {Unsub}
```

Keep under 400 words. Open + reply > scroll-through.

### Recipe 7: Quarterly virtual event (AMA with engineering / design / sales leader)

```bash
# Step 1: Send invite via Mailchimp segmented campaign (Recipe 5) — call it "AMA"
# Step 2: Open registration via Notion form or Google Form
# Step 3: Calendar invite (google-calendar-mcp) — Zoom / Google Meet link
# Step 4: Day-of: 30-min AMA; record; post highlights to LinkedIn

# Auto-invite to active hot-list segments on calendar event:
curl -X POST "https://www.googleapis.com/calendar/v3/calendars/primary/events" \
  -H "Authorization: Bearer $GOOGLE_TOKEN" \
  -d '{
    "summary": "AMA with Acme Eng Leadership",
    "start": {"dateTime": "2026-07-15T17:00:00Z"},
    "end": {"dateTime": "2026-07-15T17:30:00Z"},
    "attendees": [{"email": "jane@example.com"}, ...]  # pulled from hot-list query
  }'
```

Event attendance: 8-20% of invited; conversion to interview within 90 days: 15-25% of attendees.

### Recipe 8: Tag refresh cadence (hygiene — quarterly)

Tags drift over time. Quarterly review:

```sql
-- Pseudo — Notion query equivalent
-- "hot-list-eng-staff-3mo" candidates whose last touch > 6 months ago: drift
-- Action: re-tag to -12mo OR archive

-- "boomerang-12mo" candidates whose departure_date > 30 months: stale
-- Action: archive (alumni cadence not productive past 30 months)

-- "silver-medalist-{req-id}" tagged on req that is closed and filled: remove req-id tag
-- Keep silver-medalist parent tag for future req matching
```

Without refresh, hot-list query results pull stale signals → wasted re-enrollment touches.

### Recipe 9: Hot-list health metrics

Track in Notion or xlsx:

| Metric | Healthy | Investigate at |
|--------|---------|----------------|
| Hot-list size by segment | 50-200 per role family | <30 → underseeded; >300 → tag dilution |
| Avg days since last touch | <120 | >180 → nurture lapse; refresh newsletter |
| Hot-list → cold ratio when req opens | ≥30% hot-list | <10% → hot-list under-tagged at moment of capture |
| Hot-list reply rate vs cold | 25-40% (2-3× cold) | <15% → tagging mis-segments; tighten readiness criteria |
| Quarterly newsletter open rate | 40-55% | <30% → subject + content fatigue; refresh format |

### Recipe 10: Slack / Discord community channel

Some teams run an external Slack / Discord for talent community (vs newsletter-only):

```python
# Pseudo — slack-mcp
# Channel: #acme-engineering-community (invite-only, hot-list members)

# Quarterly: post product update + tag interested in DM
slack.post(channel="#acme-engineering-community", message="""
We just shipped {feature}. Engineering team will be in #ama on July 15 at 9am PT.
React with 🙋 if you'd like a 1:1 with hiring manager.
""")

# Track 🙋 reactions; DM each with a calendar link
reactors = slack.get_reactions("#acme-engineering-community", message_ts, "raised_hand")
for user in reactors:
    slack.send_dm(user, "Hi! Saw your 🙋 — here's my calendar: {link}")
```

Community channel works for >100-member hot-lists where 1:1 nurture is impractical.

## Examples

### Example 1: Add silver-medalist to hot-list after final-round
**Goal:** Staff backend candidate interviewed but lost to internal candidate; team rates 9/10.
**Steps:**
1. Tag in Gem: `hot-list-eng-staff-6mo`, `silver-medalist-ENG-2026-04`, `referral-source-{interviewer-name}`.
2. Notion entry with hiring manager's quote + reason for not hiring + recommended re-engage window.
3. Send personal close-loop note: "Wanted you to know we hired internally; you were extremely close. We'd jump at the chance to interview again in 6-12 months — happy to grab coffee in the meantime."
4. Schedule 6-month follow-up in Linear.

**Result:** 30-50% of silver-medalists accept re-interview within 12 months; 60% conversion to offer once re-interviewed.

### Example 2: New staff backend req opens; query hot-list first
**Goal:** New req posted; don't cold-source immediately.
**Steps:**
1. Query Gem (Recipe 3): `tags=hot-list-eng-staff-3mo OR hot-list-eng-staff-6mo OR silver-medalist-*, last_touch_gt=30days` → 40 matches.
2. Cross-reference Notion for context: who said "not now" 9 months ago? Who's a silver-medalist?
3. Author personalized hook (Recipe 4) per match — reference prior conversation.
4. Enroll in priority sequence (3-step, not 5 — already-warmed candidates need less ramp).
5. THEN start cold sourcing for the remainder per `source-diversification-3-sources-per-role`.

**Result:** 8-15 active conversations within 48h; cold sourcing handles the gap not the lead.

### Example 3: Q3 newsletter to 800-candidate talent community
**Goal:** Quarterly nurture touch.
**Steps:**
1. Segment Mailchimp list: eng (520), design (130), sales (90), exec (60).
2. Author per-segment newsletter (Recipe 6) — eng version references engineering blog; design references portfolio page.
3. A/B test subject: "Q3 update — eng team" vs "What we shipped — Q3".
4. Send Tuesday 10am ET (highest open rate by historical data).
5. Track open + reply + click-to-apply; tag respondents.

**Result:** 40-55% open rate; 2-5% reply rate (reply = interest in 1:1); 1-2% click-to-apply on open roles.

## Edge cases / gotchas

- **Tag at moment of capture, not later.** "I'll tag her tomorrow" → never happens. Tag in the same workflow as the reply.
- **Without role-readiness tag, hot-list query is useless.** Always include `hot-list-{role}-{window}` tag.
- **Don't tag everyone as hot-list-3mo.** Tag dilution. Reserve -3mo for candidates whose stated timing is within 90 days. Default to -12mo for open-ended interest.
- **Silver-medalist tag scales beyond the original req.** A staff backend silver-medalist on REQ-2026-04 should be considered for REQ-2026-09 if the role-shape matches. Don't auto-archive on req-close.
- **Stale hot-list pollutes query results.** Quarterly refresh (Recipe 8) is non-negotiable. Set a calendar recurring event.
- **Newsletter open rate >55% may signal a too-small / too-cherry-picked list.** Healthy lists have 40-55%. Too-high means you're only retaining super-fans (signal of healthy nurture but small reach).
- **Newsletter reply asks (e.g., "reply if interested") only work when reply-to is a real human.** `noreply@acme.com` → ignored. Use `talent@acme.com` or `recruiter@acme.com`.
- **Slack / Discord community channels need active moderation.** Empty community channels signal dead brand. Either invest in moderation (~2-4h/week) or skip in favor of newsletter-only.
- **Notion DB grows fast.** 1,000+ candidates queryable but Notion API gets slow >2,000 rows. Archive candidates last-touched > 18 months OR migrate to dedicated CRM at 2,000+ rows.
- **GDPR: hot-list candidates have right to be forgotten.** Honor immediately; remove from both Gem + Notion + Mailchimp. Maintain suppression list per email hash to prevent re-add.
- **CCPA / state opt-outs:** same — honor within statutory window.
- **Don't blast newsletter to candidates who replied "not now".** Tag `replied_not_now` segment for personalized 1:1 instead of mass newsletter.
- **Calendar invites from unrecognized senders flag as spam.** Use a shared talent@acme.com address that candidates have interacted with before.
- **Defer to `boomerang-alumni-re-engagement`** for ex-employees — they have separate schema + cadence.
- **Defer to `passive-candidate-outreach-campaigns`** for sequence design — this skill manages the pool, not the touch design.
- **Hot-list size optimum: 50-200 per role family.** Larger = tag dilution; smaller = underseeded (insufficient capture cadence at moment of decline).

## Sources

- Beamery — Alumni Hiring Strategy (talent community ROI): https://beamery.com/resources/blogs/why-enterprise-organizations-need-an-alumni-hiring-strategy
- Metaview — Recruiting Trends 2026: https://www.metaview.ai/resources/blog/recruiting-trends
- Gem — Candidate Sourcing Software (CRM-based talent community): https://www.gem.com/blog/candidate-sourcing-software
- Mailchimp API docs: https://mailchimp.com/developer/marketing/api/
- Notion API docs: https://developers.notion.com/
