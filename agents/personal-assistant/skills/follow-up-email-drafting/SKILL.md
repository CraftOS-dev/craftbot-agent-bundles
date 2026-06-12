<!--
Source: https://blog.superhuman.com/superhuman-ai + https://www.shortwave.com/ + https://docs.fathom.video/api/
-->
# Follow-up Email Drafting — SKILL

Pull the meeting transcript, extract per-recipient commitments + action items, and draft a follow-up email for each attendee. Superhuman AI does drafting in-app (no public API); Shortwave has AI assistant on top of Gmail; the agent path uses `gmail-mcp` + transcript pull from Fathom / Fireflies.

## When to use this skill

- **"Send follow-up to meeting attendees"** — direct trigger.
- **"Draft thank-you + action items to <name>"** — post-meeting recap.
- **"Recap last call with sales team"** — multi-recipient version.
- **Sales-call follow-up** — each prospect gets personalized next steps.
- **Networking meeting recap** — thank you + offer + ask.

**Do NOT use this skill when:**
- Composing meeting brief BEFORE the meeting — see `meeting-prep-briefs-from-granola-fathom`.
- Inbox triage (responding to inbound) — see `email-triage-superhuman-shortwave`.
- Long-form newsletter / blog — out of personal-assistant scope.

## Setup

### Required MCPs (already in agent.yaml)

- `gmail-mcp` — draft + send
- `outlook-mcp` — for Outlook-shop users
- Transcript source: Fathom REST, Fireflies GraphQL, tl;dv REST, or Granola → Notion (see `meeting-prep-briefs-from-granola-fathom` for setup)

### Verify auth

```bash
mcp tool gmail.profile
# Should return user's email
```

### Optional: Shortwave web access

Shortwave has limited public API. For Shortwave users, agent works through Gmail layer. Recommend `gmail-mcp` always.

### Optional: Superhuman

No public API. Agent drafts in Gmail; user opens in Superhuman for keyboard-driven send.

## Common recipes

### Recipe 1: Pull meeting transcript

```bash
# Fathom
MEETING_ID="<id>"
curl -s "https://api.fathom.video/v1/meetings/$MEETING_ID" \
  -H "X-API-Key: $FATHOM_API_KEY" \
  | jq '{title, attendees, summary, action_items, transcript}' \
  > meeting.json
```

(Fireflies GraphQL or tl;dv REST alternates — see `meeting-prep-briefs-from-granola-fathom`.)

### Recipe 2: Extract per-recipient action items

```python
import json
m = json.load(open("meeting.json"))
attendees = [a['email'] for a in m['attendees']]
per_recipient = {a: {"theirs": [], "ours": []} for a in attendees}
me = "me@company.com"

for ai in m['action_items']:
    owner = ai.get('owner_email')
    if owner == me:
        for other in attendees:
            if other != me: per_recipient[other]["ours"].append(ai)
    elif owner in attendees:
        per_recipient[owner]["theirs"].append(ai)

# per_recipient now has each external attendee + their actions vs ours
```

### Recipe 3: Draft email per recipient (template)

```markdown
Subject: Follow-up from our {Topic} discussion

Hi {FirstName},

Thanks for the conversation today. Quick recap of what we landed on:

**You're going to:**
- {Their action 1, with deadline}
- {Their action 2, with deadline}

**I'll handle:**
- {My action 1, with deadline}
- {My action 2, with deadline}

**Open thread for next time:**
- {Topic to revisit}

Let me know if I missed anything. Looking forward to following up.

Best,
{MyName}
```

### Recipe 4: Use gmail-mcp to draft

```bash
mcp tool gmail.draft \
  --to "alex@external.com" \
  --subject "Follow-up from our Q3 planning discussion" \
  --body "$(cat draft_alex.txt)" \
  --cc "<optional>"
```

Returns draft ID; user reviews in Gmail before send.

### Recipe 5: Batch-draft per attendee

```python
import requests, os
for email, items in per_recipient.items():
    if email == me: continue
    first = email.split('@')[0].capitalize()
    body = render_template(first, items)
    requests.post("https://gmail.googleapis.com/upload/gmail/v1/users/me/drafts",
        headers={"Authorization": f"Bearer {os.environ['GMAIL_TOKEN']}"},
        json={"message": {"raw": encode_mime(email, "Follow-up", body)}})
```

Or use `gmail-mcp` if available.

### Recipe 6: Send-vs-draft policy

**Always draft, never auto-send** for follow-ups. Surface to user for explicit approval.

```bash
# Draft + notify user via Gmail draft URL
echo "3 drafts created: https://mail.google.com/mail/u/0/#drafts"
```

### Recipe 7: Insert calendar invite for next session

If next 1:1 not scheduled, include scheduling link:

```bash
# Pull user's link from Calendly
USER_URI=$(curl -s https://api.calendly.com/users/me \
  -H "Authorization: Bearer $CALENDLY_TOKEN" | jq -r '.resource.scheduling_url')

# Insert into body
echo "Schedule the next session: $USER_URI"
```

### Recipe 8: Track sent follow-ups in Notion CRM

After user sends, log to `notion-mcp` contact record:

```bash
mcp tool notion.add_page \
  --parent-database "<contacts-db-id>" \
  --properties '{
    "Name":{"title":[{"text":{"content":"Alex Johnson"}}]},
    "Last Touch":{"date":{"start":"2026-06-09"}},
    "Last Topic":{"rich_text":[{"text":{"content":"Q3 planning"}}]},
    "Open Threads":{"rich_text":[{"text":{"content":"...summary..."}}]}
  }'
```

### Recipe 9: Templated routine reply ("Great chat, will follow up")

For low-touch follow-ups (intro coffees), use a 3-line template:

```markdown
Subject: Great connecting

Hi {FirstName},

Thanks for the time today — I appreciated learning about {Topic}.
{1-line on what I'll do next OR what they should do}.
Looking forward to staying in touch.

Best,
{MyName}
```

### Recipe 10: Multi-language draft

If attendee is non-English speaker, translate via Claude:

```python
# Sketch: re-prompt the model to translate per-recipient
draft_es = translate(draft_en, target='Spanish formal')
```

### Recipe 11: Attach prior commitments tracker

Reference open commitments from prior meetings:

```python
# From meeting-prep-briefs skill, action_items_open.json
open_items = [a for a in all_open if recipient_email in a.get('participants',[])]
body += "\n\nOpen items still in progress:\n" + "\n".join(f"- {a['task']}" for a in open_items)
```

### Recipe 12: Send-time scheduling

Don't send 11pm — schedule for 8am next business day.

```bash
mcp tool gmail.schedule_send \
  --draft-id "<draft-id>" \
  --send-at "2026-06-10T08:00:00-07:00"
```

## Examples

### Example 1: 1:1 follow-up — standard

**Goal:** Just finished 1:1 with Alex; draft follow-up.

**Steps:**
1. Recipe 1: pull Fathom transcript (~30s after end).
2. Recipe 2: extract Alex's + my action items.
3. Recipe 3: render template.
4. Recipe 7: include Calendly link for next session.
5. Recipe 4: draft in Gmail.
6. Surface to user for review + send.
7. Recipe 8: log to Notion contact.

**Result:** Draft in Gmail in ~60s; user sends in 1 click.

### Example 2: Sales call — 5 attendees

**Goal:** Sales discovery call; 1 us + 4 prospects from BigCo.

**Steps:**
1. Recipe 1: transcript pull.
2. Recipe 2: per-attendee extract.
3. Recipe 5: batch-draft 4 emails (one per prospect with their actions).
4. Each email personalized with what THEY said + what THEY agreed to.
5. Recipe 12: schedule send for 8am next business day.

**Result:** 4 personalized follow-ups queued; consistent + fast.

### Example 3: Networking event recap

**Goal:** Conference; user had 8 brief meetings; needs to send "great chat" to each.

**Steps:**
1. User dictates 1-line per person ("met Sarah - works at Stripe - wants to hear about Q3 launch").
2. Agent generates 8 short Recipe-9 templates.
3. Recipe 4: 8 drafts in Gmail.
4. User reviews + sends.

**Result:** 8 light follow-ups in 5 min.

## Edge cases / gotchas

- **Auto-send vs draft**: ALWAYS draft, never auto-send. Personal correspondence requires user review. (See role.md antipattern 2 — one-way doors.)
- **Reply-all vs reply**: Personal follow-up is usually 1:1. Don't blanket reply-all the whole meeting unless team requires it.
- **CC the assistant ("loop in")**: Sometimes desired; ask user before adding default CCs.
- **Send-time**: 11pm send signals desperation. Schedule for 8am next biz day default (Recipe 12).
- **Transcript timing**: Fathom updates ~30s after end; Fireflies ~5 min; Granola Notion sync ~10 min. If user wants brief in 30s, may not have transcript yet — surface "transcript pending; check back in 1 min."
- **Attendee email mismatch**: User's company email vs personal email. Normalize before per-recipient extract.
- **"They committed" ambiguity**: If transcript says "We'll figure it out" — that's not a commitment. Mark ambiguous as "tentative — confirm with them."
- **Tone calibration**: Sales follow-up vs investor follow-up vs friend follow-up — different tone. Ask user before first draft if non-obvious.
- **External names with typos**: Transcribers mis-spell names. Pull canonical spelling from Gmail signature / LinkedIn.
- **PII handling**: Transcript may include customer details, salary, etc. Don't include in follow-up unless explicit + appropriate.
- **GDPR / privacy**: For EU contacts, ensure unsubscribe path if mass-emailing. Personal 1:1 follow-up doesn't need it; bulk follow-up does.
- **Translation quality**: Auto-translate is rough. For high-stakes, recommend user verify or call out "translated; please review."
- **Outlook fallback**: If user on Outlook, swap `gmail-mcp` → `outlook-mcp`; templates identical.
- **Superhuman keyboard chord**: Don't try to drive Superhuman directly — no API. Draft in Gmail; user opens in Superhuman for fast send.

## Sources

- [Superhuman AI](https://blog.superhuman.com/superhuman-ai)
- [Shortwave AI Inbox](https://www.shortwave.com/)
- [Fathom API](https://docs.fathom.video/api/)
- [Fireflies API](https://docs.fireflies.ai/api)
- [Gmail API drafts](https://developers.google.com/gmail/api/guides/drafts)
- [Best email follow-up templates 2026](https://www.shortwave.com/blog/best-email-clients-2026)
