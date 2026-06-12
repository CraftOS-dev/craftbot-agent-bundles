<!--
Source: https://www.flexibits.com/cardhop + https://developers.notion.com/ + https://clay.com/ + https://developers.google.com/people/
-->
# Contact Book Maintenance — Cardhop / Notion / Clay / Cloze — SKILL

Dedup, enrich, sync, and maintain a personal CRM. Cardhop owns Mac/iOS contact management; Notion Contacts DB is the cross-link / cross-domain personal-CRM pattern; Clay does relationship intelligence + nudges; Cloze auto-pulls history from email/calendar.

## When to use this skill

- **"Update my contacts"** — direct trigger.
- **"Dedup my contacts"** — multi-source merge.
- **"Add new contact from email signature"** — single import.
- **"When did I last talk to X?"** — relationship intelligence.
- **"Birthday + relationship metadata cleanup"** — annual contact audit.

**Do NOT use this skill when:**
- Birthday reminders specifically — see `birthday-anniversary-tracking`.
- Gift research for a contact — see `gift-research-shopping`.
- Family-only coordination — see `family-calendar-coordination`.

## Pick the right tool

| Need | Tool | Why |
|---|---|---|
| Mac/iOS native CRM with bday + relationship | **Cardhop** | $20 one-time; iOS + Mac; URL scheme |
| Cross-link to projects/companies; relational DB | **Notion Contacts** | API-driven; integrates everything |
| Relationship intelligence + AI nudges | **Clay** | Auto-enriches; suggests reach-outs |
| Auto-history from email/calendar | **Cloze** | "People-first" CRM auto-builds itself |
| Native macOS/iOS sync | **Apple Contacts** | iCloud sync; free |
| Google ecosystem | **Google Contacts** | Sync across devices via Google |

## Setup

### Cardhop (URL scheme — Mac/iOS only)

```bash
# Open Cardhop and create contact
open "cardhop:///create?name=Alex+Johnson&phone=415-555-1234&email=alex@acme.com&company=Acme+Corp"
```

URL scheme docs: https://www.flexibits.com/cardhop/help

### Notion (REST)

```bash
export NOTION_TOKEN="secret_..."
# Get the Contacts DB ID from URL: notion.so/.../<32-char-id>?...
```

### Clay (REST API)

```bash
# Clay personal: https://www.clay.com/
export CLAY_TOKEN="<token>"
curl -s "https://api.clay.com/v1/contacts" \
  -H "Authorization: Bearer $CLAY_TOKEN"
```

Note: Clay has both consumer ("clay.com") and B2B ("clay.com" different surface). Personal-CRM at clay.com.

### Google Contacts (People API)

```bash
# OAuth required; user authenticates once
curl -s "https://people.googleapis.com/v1/people/me/connections?personFields=names,emailAddresses,phoneNumbers,birthdays" \
  -H "Authorization: Bearer $GOOGLE_TOKEN"
```

### iCloud Contacts (`icloud-mcp`)

```bash
mcp tool icloud.list_contacts
mcp tool icloud.create_contact \
  --name "Alex Johnson" \
  --email "alex@acme.com" \
  --phone "415-555-1234"
```

## Common recipes

### Recipe 1: Pull all Google Contacts

```bash
curl -s "https://people.googleapis.com/v1/people/me/connections?personFields=names,emailAddresses,phoneNumbers,birthdays,organizations,addresses&pageSize=1000" \
  -H "Authorization: Bearer $GOOGLE_TOKEN" \
  > google_contacts.json
```

### Recipe 2: Dedup (by email primary)

```python
import json
contacts = json.load(open("google_contacts.json"))["connections"]
seen, dupes = {}, []
for c in contacts:
    emails = [e['value'].lower() for e in c.get('emailAddresses', [])]
    for e in emails:
        if e in seen: dupes.append((seen[e], c))
        else: seen[e] = c

print(f"{len(dupes)} duplicate pairs found")
for a, b in dupes:
    # Merge: keep most-recent updated, merge fields
    pass
```

### Recipe 3: Add contact to Notion Contacts DB

```bash
curl -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id":"<contacts-db-id>"},
    "properties":{
      "Name":{"title":[{"text":{"content":"Alex Johnson"}}]},
      "Email":{"email":"alex@acme.com"},
      "Phone":{"phone_number":"415-555-1234"},
      "Company":{"select":{"name":"Acme Corp"}},
      "Role":{"rich_text":[{"text":{"content":"VP Sales"}}]},
      "Met":{"date":{"start":"2026-06-09"}},
      "Source":{"select":{"name":"LinkedIn"}},
      "Birthday":{"date":{"start":"1985-03-15"}},
      "Last Touch":{"date":{"start":"2026-06-09"}},
      "Relationship":{"select":{"name":"Professional"}}
    }
  }'
```

### Recipe 4: Update "Last Touch" from email

```python
# Pull latest sent email per recipient via gmail-mcp
import requests
contacts = notion_query_contacts()
for c in contacts:
    email = c['properties']['Email']['email']
    latest = gmail.search(f"to:{email} OR from:{email}", maxResults=1)
    if latest:
        # Update Notion Last Touch
        notion_update(c['id'], "Last Touch", latest[0]['date'])
```

### Recipe 5: Enrich from email signature

```python
# Pull email; extract signature; parse
msg = gmail.get(message_id)
body = decode_body(msg)
sig = extract_signature(body)
# Use AI/regex to extract: name, title, company, phone, address, social
parsed = {
    "name": "Alex Johnson",
    "title": "VP Sales",
    "company": "Acme Corp",
    "phone": "415-555-1234",
    "linkedin": "https://linkedin.com/in/alex-johnson",
}
# Push to Notion
```

### Recipe 6: Bulk import to Cardhop from CSV

Cardhop accepts vCard import. Convert CSV → vCard:

```python
import csv
with open("contacts.csv") as f, open("contacts.vcf","w") as out:
    for r in csv.DictReader(f):
        out.write(f"""BEGIN:VCARD
VERSION:3.0
N:{r['last']};{r['first']};;;
FN:{r['first']} {r['last']}
EMAIL:{r['email']}
TEL:{r['phone']}
ORG:{r['company']}
TITLE:{r['title']}
NOTE:{r.get('notes','')}
END:VCARD
""")
```

Then drag .vcf into Cardhop / Apple Contacts.

### Recipe 7: Add birthday from contact

```bash
mcp tool google-calendar.create_event \
  --calendarId "addressbook@group.v.calendar.google.com" \
  --summary "Alex's Birthday" \
  --start "2026-03-15" \
  --end "2026-03-16" \
  --recurrence "RRULE:FREQ=YEARLY"
```

Or use the dedicated `birthday-anniversary-tracking` skill.

### Recipe 8: Clay relationship intelligence

If user has Clay:

```bash
# Clay surfaces "people you should reach out to"
curl -s "https://api.clay.com/v1/nudges" \
  -H "Authorization: Bearer $CLAY_TOKEN" \
  | jq '.[] | {name, last_contact_days_ago, suggested_reason}'
```

### Recipe 9: Cardhop create contact via URL scheme

```bash
# Mac
NAME="Alex Johnson"
PHONE="415-555-1234"
EMAIL="alex@acme.com"
COMPANY="Acme Corp"

open "cardhop:///create?name=$(echo $NAME | sed 's/ /+/g')&phone=$PHONE&email=$EMAIL&company=$(echo $COMPANY | sed 's/ /+/g')"
```

### Recipe 10: Sync Notion → Google Contacts (one-way)

```python
notion_contacts = notion_query_contacts()
for c in notion_contacts:
    # Create or update Google Contact via People API
    requests.post("https://people.googleapis.com/v1/people:createContact",
        headers={"Authorization":f"Bearer {GOOGLE_TOKEN}"},
        json={
            "names":[{"givenName": c['name'].split()[0], "familyName": c['name'].split()[-1]}],
            "emailAddresses":[{"value": c['email']}],
            "phoneNumbers":[{"value": c['phone']}],
            "organizations":[{"name": c['company']}],
        })
```

### Recipe 11: Audit stale contacts (no touch in 12 months)

```python
import datetime
threshold = datetime.datetime.now() - datetime.timedelta(days=365)
stale = [c for c in notion_contacts
         if last_touch_date(c) < threshold and c['relationship'] in ['Professional','Networking']]
print(f"{len(stale)} contacts stale 12+ months")
# Surface to user for reach-out planning
```

### Recipe 12: Bulk update relationship metadata

```python
RELATIONSHIPS = {
    "alex@acme.com": "Professional",
    "mom@personal.com": "Family",
    "tony@gym.com": "Local",
}
for email, rel in RELATIONSHIPS.items():
    page_id = find_notion_contact(email)
    notion_update(page_id, "Relationship", {"select":{"name":rel}})
```

## Examples

### Example 1: New contact from business card / email

**Goal:** Just met Alex at a conference; have email signature; add to Notion + Cardhop + Google.

**Steps:**
1. Recipe 5: parse email signature → structured contact.
2. Recipe 3: add to Notion Contacts (Source: Conference, Met date: today).
3. Recipe 9: Cardhop URL scheme.
4. Recipe 10: sync to Google Contacts.
5. Optional: Recipe 7 (birthday if available).

**Result:** One contact in 3 places + synced.

### Example 2: Annual contact audit

**Goal:** January 1; audit all professional contacts.

**Steps:**
1. Recipe 1: pull all Google Contacts.
2. Recipe 2: dedup pairs.
3. Recipe 11: identify stale (12+ months no touch).
4. For stale: surface as "potential reach-out list" via gmail-mcp.
5. Recipe 12: update relationship metadata.

**Result:** Clean book + reach-out queue.

### Example 3: Networking reach-out planning

**Goal:** Q1 networking — reach out to 10 stale professional contacts.

**Steps:**
1. Recipe 8 (or 11) — surface candidates.
2. For each: pull last context from `meeting-prep-briefs-from-granola-fathom` if recent meeting.
3. Draft per-recipient outreach email via `follow-up-email-drafting`.
4. Schedule send Monday morning.

**Result:** 10 personalized outreach emails queued.

## Edge cases / gotchas

- **Multiple emails per contact**: Personal vs work. Always store both; normalize on primary.
- **Phone formatting**: E.164 vs national; normalize before dedup.
- **Cardhop URL scheme limits**: Max URL ~2k chars; for big imports use vCard (Recipe 6).
- **Notion relations**: For Contact ↔ Company ↔ Project, build all 3 DBs + relations. Easier than flat list.
- **Apple iCloud auth**: `icloud-mcp` may need re-auth periodically when iCloud session expires.
- **People API quota**: 90 req/min default; bulk operations need batch.
- **Clay personal vs B2B**: Clay.com has two products. Don't confuse the consumer CRM with the B2B sales intelligence product.
- **Cloze auto-history privacy**: Cloze reads ALL email; surface this to user before recommending.
- **Cardhop is Mac/iOS only**: Don't recommend if user is on Windows / Linux.
- **vCard version**: Some apps require 3.0, others 4.0. Use 3.0 for broadest compat (Recipe 6).
- **Profile photos**: Cardhop / Apple Contacts pull photos; agent doesn't have access. Surface as "add photo manually."
- **Last-touch accuracy**: Recipe 4 captures email touch; doesn't capture text / Slack / WhatsApp. Recommend `whatsapp-mcp` + `slack-mcp` for true last-touch.
- **Family contacts**: Don't treat family same as professional. Separate DB or "Relationship" property.
- **Deceased contacts**: Mark + archive; don't auto-dedup or delete (sentimental).
- **GDPR**: For EU contacts, respect right-to-delete on request.
- **Annual review fatigue**: Don't over-engineer. Recipe 11 quarterly is plenty.

## Sources

- [Cardhop](https://www.flexibits.com/cardhop)
- [Notion API](https://developers.notion.com/)
- [Clay personal CRM](https://clay.com/)
- [Cloze](https://www.cloze.com/)
- [Google People API](https://developers.google.com/people/)
- [Apple Contacts Help](https://support.apple.com/guide/contacts/welcome/mac)
