<!--
Source: https://www.shortwave.com/blog/best-email-clients-2026 + https://blog.superhuman.com/superhuman-ai
-->
# Email Triage — Superhuman / Shortwave — SKILL

Triage inbox to zero in 30 min via batch + filter + AI bundle. Superhuman is keyboard-fastest with built-in AI; Shortwave layers AI bundles + thread summaries on top of Gmail; both speak Gmail API underneath. Agent works via `gmail-mcp` — designs filter set, runs bulk classify, drafts replies, snoozes deferrals.

## When to use this skill

- **"Get my inbox to zero" / "inbox triage" / "clean up email"** — direct trigger.
- **Daily 9:30am + 4pm inbox windows** — recurring ritual.
- **Post-vacation catchup** — heavy batch.
- **New filter setup** — designing rules for "X always goes to label Y."
- **Inbox-zero onboarding** — Merlin Mann / Tiago Forte CODE pattern.

**Do NOT use this skill when:**
- Composing follow-up emails after meetings — see `follow-up-email-drafting`.
- Subscription cancellation outreach — see `subscription-tracker-cancellation`.
- Single ad-hoc email — call `gmail-mcp` directly.

## Pick the right tool

| User profile | Tool | Why |
|---|---|---|
| Keyboard-driven; fastest triage | **Superhuman** | Built-in AI + chord shortcuts ($30/mo) |
| AI-organized inbox bundles | **Shortwave** | AI bundles + thread summaries + free tier |
| Chat-style email | **Spike** | Inbox-as-chat |
| Opinionated (Imbox/Feed/Paper Trail) | **Hey.com** | $99/yr; philosophical |
| Mac-native Gmail | **Mimestream** | Native macOS; Gmail-only |
| Multi-platform smart | **Spark** | Free + premium AI |
| Default web | **Gmail / Outlook** | Baseline |

## Setup

### Gmail MCP (primary path)

```bash
# Already wired in agent.yaml
mcp tool gmail.profile
```

### Optional: Shortwave (limited API)

Shortwave reads from Gmail under the hood. Agent works through `gmail-mcp` for both clients.

### Optional: Superhuman

No public API. Agent designs rules in Gmail; user gets the keyboard speed benefit in Superhuman.

### Inbox-zero rule design

The agent's primary job: design + apply filter rules. See Recipe 3.

## Common recipes

### Recipe 1: Pull inbox stats

```bash
# Counts by label
mcp tool gmail.search --query "label:inbox" --max-results 0  # returns count
mcp tool gmail.search --query "label:inbox is:unread" --max-results 0
mcp tool gmail.search --query "label:inbox older_than:7d" --max-results 0
```

### Recipe 2: Classify by category — sample mode

```python
import requests
# Pull last 100 inbox messages metadata
msgs = gmail.messages.list(maxResults=100, q="label:inbox")
buckets = {'newsletter':0, 'receipt':0, 'marketing':0, 'calendar':0, 'personal':0, 'service':0}

for m in msgs:
    msg = gmail.messages.get(id=m['id'], format='metadata')
    sender = headers.get('From')
    subject = headers.get('Subject')
    if any(d in sender for d in ['substack.com','beehiiv.com','newsletter']):
        buckets['newsletter'] += 1
    elif any(d in sender for d in ['amazon.com','etsy.com','order','receipt','shipment']):
        buckets['receipt'] += 1
    elif 'unsubscribe' in subject.lower() or 'marketing' in sender:
        buckets['marketing'] += 1
    elif 'noreply@calendar' in sender or 'gcal' in sender:
        buckets['calendar'] += 1
    else:
        buckets['personal'] += 1
print(buckets)
```

### Recipe 3: Apply standard filter set

Standard inbox-zero filter set — apply via Gmail API:

```python
FILTERS = [
    {"criteria":{"from":"*@substack.com OR *@beehiiv.com OR *@newsletter.*"},
     "action":{"removeLabelIds":["INBOX"],"addLabelIds":["Label_Newsletter"]}},
    {"criteria":{"from":"*@amazon.com","subject":"order"},
     "action":{"removeLabelIds":["INBOX"],"addLabelIds":["Label_Receipts"]}},
    {"criteria":{"from":"noreply@calendar.google.com OR invite@gcal.google.com"},
     "action":{"addLabelIds":["Label_Calendar"]}},
    {"criteria":{"from":"*@marketing.* OR *@promo.*","query":"unsubscribe"},
     "action":{"removeLabelIds":["INBOX"],"addLabelIds":["Label_Marketing"]}},
    {"criteria":{"from":"*@github.com","subject":"notification"},
     "action":{"removeLabelIds":["INBOX"],"addLabelIds":["Label_GitHub"]}},
]

for f in FILTERS:
    gmail.users.settings.filters.create(userId='me', body=f)
```

### Recipe 4: Bulk archive matching pattern (one-time catch-up)

```bash
# Archive all newsletters older than 30 days
mcp tool gmail.batch_modify \
  --query "label:Newsletter older_than:30d" \
  --remove-labels '["INBOX"]'
```

### Recipe 5: VIP star + auto-keep

```python
VIP_LIST = ['boss@company.com','partner@personal.com','mom@family.com','spouse@family.com']
for vip in VIP_LIST:
    gmail.users.settings.filters.create(userId='me', body={
        "criteria":{"from":vip},
        "action":{"addLabelIds":["STARRED","IMPORTANT"]}
    })
```

### Recipe 6: AI bundle / thread summary

Shortwave does this natively. For raw Gmail, use Claude / GPT to bundle:

```python
unread_threads = gmail.threads.list(q="label:inbox is:unread", maxResults=50)
groups = ai_group_by_topic(unread_threads)
# e.g., {"Project Alpha":[t1,t2,t3], "Vendor X":[t4]}
```

Surface to user as bundles.

### Recipe 7: Compose batch replies

For routine inbox responses, use 5 templates:

```python
TEMPLATES = {
    "ack": "Got it, thanks — will get back to you by EOD.",
    "scheduling": "Happy to discuss. Here's my calendar: <link>",
    "decline": "Thanks for thinking of me — not the right fit right now.",
    "intro": "Happy to help. Best person at X is Y, looping them in.",
    "fwd_info": "Forwarding this to my assistant who can take it from here.",
}
```

### Recipe 8: Snooze for deferral

```bash
# Snooze a thread for Monday 9am
mcp tool gmail.snooze \
  --thread-id "<thread-id>" \
  --until "2026-06-15T09:00:00-07:00"
```

### Recipe 9: Inbox window — 30 min ritual

```markdown
1. Pull unread count + bundle (5 min)
2. Auto-archive matching patterns (2 min) — Recipe 4
3. Process bundles top-5 (15 min)
4. Compose reply pass (5 min) — Recipes 7 + 4
5. Snooze deferrals (2 min) — Recipe 8
6. Confirm zero or 1-digit count (1 min)
```

### Recipe 10: Daily inbox-window calendar holds

```bash
mcp tool google-calendar.create_event \
  --summary "Inbox Triage AM" \
  --start "2026-06-10T09:30:00-07:00" \
  --end   "2026-06-10T10:00:00-07:00" \
  --recurrence "RRULE:FREQ=DAILY;BYDAY=MO,TU,WE,TH,FR"

mcp tool google-calendar.create_event \
  --summary "Inbox Triage PM" \
  --start "2026-06-10T16:00:00-07:00" \
  --end   "2026-06-10T16:30:00-07:00" \
  --recurrence "RRULE:FREQ=DAILY;BYDAY=MO,TU,WE,TH,FR"
```

### Recipe 11: Vacation autoresponder

```bash
mcp tool gmail.update_vacation_responder \
  --enabled true \
  --start-time "2026-07-15T00:00:00Z" \
  --end-time "2026-07-21T23:59:00Z" \
  --subject "Out of Office through Jul 21" \
  --body "On vacation through Jul 21. I'll respond when back. For urgent, contact <delegate@>."
```

### Recipe 12: Unsubscribe bulk

```python
# Find unique senders with "unsubscribe" in body, last 90 days
candidates = gmail.search("unsubscribe newer_than:90d label:Marketing")
unique_senders = set(extract_sender(m) for m in candidates)

# Surface to user
for s in unique_senders:
    print(f"Unsubscribe from: {s}")
# User clicks "yes / no" per sender; agent calls Unroll.me-style or directly hits unsubscribe URL
```

### Recipe 13: "Pretend I read it" — declare bankruptcy

For inbox > 1000 unread:

```bash
# Archive all older than 14 days
mcp tool gmail.batch_modify \
  --query "label:inbox older_than:14d" \
  --remove-labels '["INBOX"]' \
  --add-labels '["Label_BankruptcyAug2026"]'
```

Then start fresh.

## Examples

### Example 1: New user — set up inbox-zero

**Goal:** User has 5k unread; needs system.

**Steps:**
1. Recipe 1: stats — surface scale.
2. Recipe 2: classify last 100 → identify dominant categories.
3. Recipe 5: VIP star list (user provides).
4. Recipe 3: apply standard filter set.
5. Recipe 4: bulk archive newsletter / marketing.
6. Recipe 13: archive everything older than 14d to "Bankruptcy" label.
7. Recipe 10: schedule daily 9:30am + 4pm inbox windows.
8. Surface final count + next-window time.

**Result:** Inbox at single-digit count; filter set live; ritual scheduled.

### Example 2: Post-vacation catchup

**Goal:** Back from 1-week vacation; 400 emails in inbox.

**Steps:**
1. Recipe 2: classify.
2. Recipe 4: auto-archive newsletters + marketing + receipts (~250 gone).
3. Recipe 6: AI bundle remaining 150 into 8 topical groups.
4. Recipe 7: batch-reply ~30 with templates.
5. Recipe 8: snooze 40 to Monday next week.
6. Process remaining 80 in 25 min.
7. Result count.

**Result:** Inbox zero in 60 min.

### Example 3: Weekly review

**Goal:** Sunday 8pm; check filter set still doing its job.

**Steps:**
1. Recipe 1: stats.
2. Audit Label_Marketing for false positives (any actual important caught?).
3. Audit VIP star list — any new VIPs?
4. Adjust filters via Recipe 3.

**Result:** Filter set stays tuned.

## Edge cases / gotchas

- **Filter creation rate limit**: Gmail API limits filter creation; create in batches.
- **Filter ordering**: Gmail applies filters in insertion order; later filters can override. Test the chain.
- **"From:" wildcard support**: Gmail supports `*@domain.com` but not arbitrary regex. Use Gmail search syntax exactly.
- **Star vs Important vs Inbox**: 3 separate flags. Gmail's "Important" is ML-driven; can be off for VIPs. Always set both for true VIPs.
- **Snooze precision**: Snooze rounds to nearest 30 min; don't try to snooze to exact time.
- **Auto-archive risk**: New filter may catch important mail. Always test with a small batch before bulk.
- **Bankruptcy semantics**: Recipe 13 is destructive feeling but reversible — archived ≠ deleted. Search "label:Bankruptcy" any time.
- **Unsubscribe link risk**: Some unsubscribe links are tracking pixels. Use Recipe 12 only on legit-looking senders; verify domain.
- **Shortwave free tier**: 100 messages/day on AI; Pro $7/mo for unlimited. Source: https://www.shortwave.com/pricing
- **Superhuman billing**: $30/mo; no free tier. Source: https://superhuman.com/pricing
- **Vacation responder TZ**: Vacation responder uses Gmail TZ; doesn't auto-shift if user travels.
- **Calendar invite handling**: Gmail's "Calendar" label catches but doesn't auto-process. For auto-respond, use `google-calendar-mcp.respond_to_event`.
- **Threaded conversation**: Gmail threads by Subject + Reply-To; sometimes splits incorrectly. Don't assume thread = conversation.
- **EU GDPR**: For EU senders, respect their unsubscribe right.
- **Search performance**: `older_than:30d` is fast; `body:`-search is slow.

## Sources

- [Shortwave best email clients 2026](https://www.shortwave.com/blog/best-email-clients-2026)
- [Superhuman AI](https://blog.superhuman.com/superhuman-ai)
- [Gmail API filters](https://developers.google.com/gmail/api/guides/filter_settings)
- [Inbox Zero (Merlin Mann)](https://www.43folders.com/2007/03/12/inbox-zero)
- [Tiago Forte CODE method](https://fortelabs.com/blog/basboverview/)
- [Hey.com philosophy](https://www.hey.com/features/)
