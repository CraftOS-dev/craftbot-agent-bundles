<!--
Sources: https://www.tango.ai/blog/scribe-alternatives
         https://www.docsie.io/blog/articles/scribe-vs-tango-comparison-2026/
         https://www.tango.ai/blog/process-documentation-software
Scribe = live screen → step-by-step. Tango = screenshot + annotate. Whale = SOP draft + AI. Trainual = SOPs + training + tracking.
-->
# Process Documentation — Scribe / Tango / Whale / Trainual — SKILL

Author standard operating procedures (SOPs), runbooks, training pages — three approaches: **auto-capture** (Scribe live screen-record → step-by-step guide; Tango screenshot + annotation; Whale Step Recorder + AI draft) vs **training-driven** (Trainual: SOPs + quizzes + assignments + tracking) vs **manual** (Markdown in Notion).

## When to use

- New process needs documenting in 15-30 minutes (auto-capture).
- Training a cohort of new hires on N processes (Trainual).
- Existing process needs polish + versioning (manual Markdown in Notion).
- Trigger phrases: "SOP", "runbook for process", "how-to", "step-by-step", "screen-record", "documentation", "playbook", "guide".

## Setup

```bash
export SCRIBE_API_TOKEN="xxx"     # https://scribehow.com — Pro+ for API
export TANGO_TOKEN="xxx"          # https://tango.us — paid
export WHALE_TOKEN="xxx"          # https://usewhale.io
export TRAINUAL_TOKEN="xxx"       # https://trainual.com
export NOTION_TOKEN="xxx"         # fallback authoring
```

Tier notes:
- **Scribe** Pro $29/user/mo + Enterprise; AI-redaction; SOC 2.
- **Tango** free tier limited (up to 5 captures); Pro $20/user/mo.
- **Whale** $5/user/mo + AI tier.
- **Trainual** $250/mo team baseline.

## Common recipes

### Recipe 1: Decision tree — which tool?
```yaml
choose:
  one_off_screen_walkthrough:
    primary: Tango
    why: Fastest; in-browser; free tier covers occasional use
  recurring_process_with_updates:
    primary: Scribe
    why: Re-record updates; AI-redact PII; auto-detect step changes
  org_wide_training_with_tracking:
    primary: Trainual
    why: SOPs + quizzes + assignment + compliance trail
  ai_drafted_SOP_from_recording:
    primary: Whale
    why: Whale 2026 = Step Recorder + AI SOP draft
  versioned_text_first_SOPs:
    primary: Notion (manual Markdown)
    why: Best for engineering-style ops, version history natively
```

### Recipe 2: SOP template (Markdown)
```markdown
# SOP: <Name>

| Field        | Value             |
|--------------|-------------------|
| Owner        | @<owner>          |
| Version      | v2026.07          |
| Last reviewed| 2026-07-01        |
| Frequency    | Weekly / Monthly  |
| Time est.    | 30 min            |
| Backup       | @<backup>         |

## Purpose
1-2 sentences on the outcome.

## Prerequisites
- Account access: list
- Tools: list
- Information needed: list

## Steps
1. Step 1 — `command/screenshot/exact action`
2. Step 2 — ...
3. Step 3 — ...

## Verification
How to confirm the step worked.

## Troubleshooting
| Symptom | Cause | Fix |
|---------|-------|-----|
| | | |

## Change log
- v2026.07 — initial draft
- v2026.08 — added Step 4 for new vendor
```

### Recipe 3: Trainual SOP push via API
```bash
curl -s -X POST "https://api.trainual.com/v1/topics" \
  -H "Authorization: Bearer $TRAINUAL_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "title":"How to run weekly KPI digest",
    "category_id":"<ops-category>",
    "content_html":"<h1>...</h1><ol><li>Open Stripe...</li></ol>",
    "assigned_to_roles":["ops-team"],
    "due_within_days":7,
    "quiz":{"required_passing":80,"questions":[
      {"text":"At what time does the digest post?","correct":"09:00"},
      {"text":"Where is the failure-alert channel?","correct":"#automation-errors"}
    ]}
  }'
```

### Recipe 4: Scribe — convert recorded session to article
```bash
# Capture done in Scribe browser extension. Pull article + push to Notion.
curl -s "https://scribehow.com/api/v1/scribes/<id>" \
  -H "Authorization: Bearer $SCRIBE_API_TOKEN" \
  | jq '{title, steps: [.steps[] | {text, screenshot_url}]}' > scribe-export.json

# Then push to Notion (manual or via Recipe 9 below)
```

### Recipe 5: Auto-redact PII (Scribe AI)
```bash
# Scribe Enterprise has AI-redaction of usernames, emails, tokens visible in screenshots
curl -s -X POST "https://scribehow.com/api/v1/scribes/<id>/redact" \
  -H "Authorization: Bearer $SCRIBE_API_TOKEN" \
  -d '{"types":["email","name","token","ip","credit_card"]}'
```

### Recipe 6: Notion SOP page with version DB
```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" \
  -d '{
    "parent":{"database_id":"<sop-db>"},
    "properties":{
      "Name":{"title":[{"text":{"content":"SOP: Weekly KPI digest"}}]},
      "Owner":{"people":[{"id":"<owner>"}]},
      "Version":{"rich_text":[{"text":{"content":"v2026.07"}}]},
      "Effective Date":{"date":{"start":"2026-07-01"}},
      "Status":{"select":{"name":"Live"}},
      "Frequency":{"select":{"name":"Weekly"}}
    }
  }'
```

### Recipe 7: SOP discoverability index
```markdown
# SOP Index — /Ops/SOPs

## Daily
- SOP: Morning team standup — @maria
- SOP: KPI digest 09:00 — @sam

## Weekly
- SOP: Weekly renewal calendar review — @alex
- SOP: Pipeline-velocity audit — @sam

## Monthly
- SOP: SaaS spend audit — @alex
- SOP: Comp-band refresh check — @maria

## Quarterly
- SOP: BCP tabletop exercise — @ops-lead
- SOP: Vendor questionnaire refresh — @security-lead

## Annual
- SOP: Insurance renewal audit — @ops-lead
- SOP: Performance review cycle close — @people-ops
```

### Recipe 8: Whale Step Recorder + AI draft
```bash
# Whale captures a screen recording; AI generates SOP draft you edit
curl -s -X POST "https://api.usewhale.io/v1/cards/draft_from_recording" \
  -H "Authorization: Bearer $WHALE_TOKEN" -H "Content-Type: application/json" \
  -d '{"recording_id":"<rec>","instructions":"Generate an SOP with numbered steps and a troubleshooting table."}'
```

### Recipe 9: Cross-tool sync (Scribe/Tango → Notion)
```python
import requests, os, base64

# Pull from Scribe, push to Notion
scribe = requests.get(
    f"https://scribehow.com/api/v1/scribes/{os.environ['SCRIBE_ID']}",
    headers={'Authorization': f"Bearer {os.environ['SCRIBE_API_TOKEN']}"}).json()

blocks = []
for step in scribe['steps']:
    blocks.append({'object':'block','type':'numbered_list_item','numbered_list_item':{
        'rich_text':[{'type':'text','text':{'content': step['text']}}]
    }})
    if step.get('screenshot_url'):
        blocks.append({'object':'block','type':'image','image':{'type':'external','external':{'url': step['screenshot_url']}}})

requests.post('https://api.notion.com/v1/pages',
    headers={'Authorization':f"Bearer {os.environ['NOTION_TOKEN']}",'Notion-Version':'2022-06-28','Content-Type':'application/json'},
    json={'parent':{'database_id':'<sop-db>'},'properties':{
        'Name':{'title':[{'text':{'content':scribe['title']}}]}
    },'children':blocks})
```

### Recipe 10: Trainual training rollout
```bash
# Assign topic + send Slack DM to each assigned user
curl -s -X POST "https://api.trainual.com/v1/assignments" \
  -H "Authorization: Bearer $TRAINUAL_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "topic_id":"<topic>",
    "user_ids":["<u1>","<u2>","<u3>"],
    "due_at":"2026-07-15",
    "notify_via":["email","slack"]
  }'
```

### Recipe 11: Quarterly SOP refresh sweep
```python
# Find stale SOPs (last reviewed > 90d), surface to owners
import datetime, requests, os
ninety_days = (datetime.date.today() - datetime.timedelta(days=90)).isoformat()

stale = requests.post(f"https://api.notion.com/v1/databases/<sop-db>/query",
    headers={'Authorization': f"Bearer {os.environ['NOTION_TOKEN']}", 'Notion-Version':'2022-06-28','Content-Type':'application/json'},
    json={'filter':{'property':'Effective Date','date':{'before': ninety_days}}}).json()

for s in stale['results']:
    owner = s['properties']['Owner']['people'][0]['name']
    name = s['properties']['Name']['title'][0]['plain_text']
    # post to slack
```

## Examples

### Example 1: SOP for new vendor onboarding
**Goal:** Capture the 12-step process from intake to contract storage.
**Steps:**
1. Recipe 1: pick Scribe (recurring + AI-redact).
2. Walk the actual process in Scribe browser extension.
3. Recipe 5 redact PII in screenshots.
4. Recipe 9: push to Notion.
5. Recipe 6: add metadata row (owner, version, frequency).
6. Recipe 7: add to index.
7. Recipe 10: assign in Trainual to procurement team.

**Result:** Documented, indexed, training-rollout-ready SOP in ~45 min.

### Example 2: Refresh existing SOPs quarterly
**Goal:** Keep SOPs current.
**Steps:**
1. Recipe 11 finds stale ones.
2. Slack DMs each owner with "review or archive."
3. Updates pushed via Recipe 6 with new version.

**Result:** No SOP older than 90 days unreviewed.

## Edge cases / gotchas

- **PII in screen captures.** Scribe Enterprise AI-redact handles most; Tango free does not. Don't capture screens that show customer PII without redaction.
- **Auto-capture step misordering.** Browser pop-ups, modals, and async loads can cause mis-detected step boundaries. Always edit the captured draft.
- **Trainual quiz fatigue.** > 10 questions per topic kills completion rates. Aim 3-5 with clear-correct answers.
- **Notion search recall.** SOP titles must be greppable — start with `SOP:` prefix; include process name + the verb (e.g., "SOP: Run weekly KPI digest" not "Weekly KPI").
- **Owner orphaning.** Owner leaves → SOP becomes stale. Recipe 11 + reassignment policy is mandatory.
- **Cross-tool diffs.** Scribe ↔ Notion sync (Recipe 9) requires conflict resolution. Pick a source of truth (typically Notion if non-engineering team; Scribe if engineering-friendly + audit-heavy).
- **Quizzes as ACK.** Trainual quiz ≠ legal acknowledgment for handbook. Use Gusto / DocuSign for binding ACK.
- **Capture security on shared screens.** Recording must NOT include private channels, ticket detail pages, or admin consoles. Use a sterile sandbox environment for SOPs that show production-like flows.
- **Multi-language SOPs.** Tango / Scribe don't auto-translate; pair with `markdown-converter` skill + DeepL.
- **Defer to `legal-counsel` for binding training-completion compliance attestations (e.g., harassment training in CA/NY/IL/CT/DE/ME/WA).**

## Sources

- Tango — Scribe Alternatives 2026: https://www.tango.ai/blog/scribe-alternatives
- Docsie — Scribe vs Tango 2026: https://www.docsie.io/blog/articles/scribe-vs-tango-comparison-2026/
- Tango — Best Process Doc Software 2026: https://www.tango.ai/blog/process-documentation-software
- Scribe API: https://scribehow.com/api
- Whale: https://usewhale.io/
- Trainual API: https://docs.trainual.com/
- Notion API: https://developers.notion.com/
