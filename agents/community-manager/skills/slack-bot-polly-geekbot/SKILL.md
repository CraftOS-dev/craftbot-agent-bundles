<!--
Sources: https://api.slack.com/ + https://www.polly.ai/ + https://geekbot.com/ + https://www.donut.com/ + https://standuply.com/ + https://api.slack.com/workflows
-->
# Slack Bot Setup (Polly / Geekbot / Donut) — SKILL

Engagement bot stack for Slack communities: Donut (intro coffees), Polly (polls + pulse surveys), Geekbot (async standups + scrum), Standuply (alt standup), Workast (task tracking), Birthday Bot (recognition). Plus native Slack Workflow Builder for onboarding + recurring reminders. Each bot replaces a manual prompt; layered properly they sustain weekly engagement without human prompting.

## When to use

- New Slack-based community / workspace launching engagement programming.
- Existing Slack community with low posting rate — needs intro pairing or polls to spark threads.
- Async-distributed team / community wanting daily/weekly standup cadence.
- Pulse-survey program (eNPS, community health, post-event NPS).
- Migrating from a single bot (e.g., just Polly) to a layered engagement stack.
- Workspace admin wants OAuth-approved engagement bots before launch invites.

Trigger phrases: "Slack bot", "Slack poll", "Polly setup", "Geekbot", "Donut intro", "Standuply", "async standup", "Slack engagement", "pulse survey", "Slack workflow builder".

## Setup

```bash
# Each bot needs OAuth install per workspace (one-time, admin-approved)
# Polly:    https://www.polly.ai/install
# Geekbot:  https://app.geekbot.com/signup
# Donut:    https://www.donut.com/install
# Standuply: https://app.standuply.com/

# slack-mcp for direct API operations (already in agent.yaml)
mcp tool slack-mcp.chat_postMessage --channel '#community' --text 'Hello'
mcp tool slack-mcp.chat_scheduleMessage --channel '#community' \
  --post_at 1717228800 --text 'Monday motivation drop'
mcp tool slack-mcp.conversations_list --types public_channel,private_channel

# Polly API (paid plan unlocks programmatic)
curl -X POST https://api.polly.ai/v1/polls \
  -H "Authorization: Bearer $POLLY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C0XXXX","question":"Which session?","options":["A","B","C"]}'

# Geekbot API
curl -H "Authorization: Token $GEEKBOT_TOKEN" \
  https://api.geekbot.com/v1/standups

# Donut — UI-only configuration; no public API. Configure via /donut command.
```

Auth + env:
- `SLACK_BOT_TOKEN` — `xoxb-` token. Scopes: `chat:write`, `channels:read`, `channels:history`, `users:read`, `reactions:read`, `pins:write`, `workflow.steps:execute`.
- `SLACK_USER_TOKEN` — `xoxp-` for admin actions (`admin.users:read`, `admin.invites:write`).
- `POLLY_TOKEN` — Polly dashboard → API. Pro plan ($24/user/mo) unlocks API.
- `GEEKBOT_TOKEN` — geekbot.com → Integrations → API. Free up to 10 participants.
- `STANDUPLY_TOKEN` — Standuply Pro+ ($1.5/user/mo).

Workspace prerequisites:
- Channels: `#welcome`, `#introductions`, `#announcements`, `#standup`, `#polls`, `#donut-pairings`, `#community-feedback`, `#general`.
- User groups: `@mods`, `@ambassadors`, `@champions`.
- Slack admin approval for each app (Settings → Manage apps → App approval policy).

## Common recipes

### Recipe 1: Engagement bot install order

Install layered, starting from leanest:

1. **slack-mcp baseline** — programmatic posting / scheduling (already in agent.yaml).
2. **Slack Workflow Builder** (native, free) — welcome message + recurring reminders. No external app.
3. **Donut** — intro coffees, 30-min pairings weekly. Lowest-effort engagement lift.
4. **Polly** — polls + pulse surveys + post-event NPS.
5. **Geekbot** — async standup rituals (3-question format).
6. **Standuply** (optional) — alt standup if Geekbot too lightweight.
7. **Birthday Bot** / **Disco** — recognition cadence.

Rule of thumb: every layer must replace a recurring manual prompt. If no one would have manually run the prompt, do not add the bot.

### Recipe 2: Welcome workflow via Slack Workflow Builder (native, no bot install)

```json
{
  "trigger": "user_joined_channel",
  "channel": "#welcome",
  "steps": [
    {
      "type": "send_message",
      "channel": "{user_who_joined}",
      "message": "Hi {user_name}! Welcome. Three things:\n1. Drop a hello in <#C-introductions>\n2. Pick interests in <#C-roles>\n3. Reply with one goal for this month."
    },
    {
      "type": "send_message",
      "channel": "#welcome",
      "message": "Welcome <@{user_id}>! Quick tour: <https://docs.brand.com/community-guide|guide>."
    },
    {
      "type": "wait",
      "duration_minutes": 4320
    },
    {
      "type": "send_message",
      "channel": "{user_who_joined}",
      "message": "Hey {user_name} — how's it going? Reply with 1-10."
    }
  ]
}
```

Build via Slack → Tools → Workflow Builder → New workflow. Export JSON for version control via the steps-as-code feature in paid plans.

### Recipe 3: Donut intro coffees

Install Donut → `/donut connect` in `#donut-pairings`. Default config:

```yaml
donut:
  channel: '#donut-pairings'
  cadence: bi-weekly  # weekly, bi-weekly, monthly
  pair_size: 2        # 2, 3, or 4 person rounds
  exclude_from_pairing:
    - bot_users
    - timezone_conflict_>_8h
  intro_message: |
    You've been Donut-paired! Drop a 30-min slot below.
    Bonus: share one thing you're working on this week.
  recurrence_day: monday
  recurrence_time: '09:00 LOCAL'
```

For programmatic-style overrides, manage via the Donut UI; no public API. Slack-side: use `slack-mcp.conversations_history` to scrape `#donut-pairings` for pairing-completion sentiment.

### Recipe 4: Polly polls (manual + API)

Manual: `/polly Should we host the next AMA on Tues or Thurs? Tues | Thurs`

API for programmatic launch (Pro+):

```bash
curl -X POST https://api.polly.ai/v1/polls \
  -H "Authorization: Bearer $POLLY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C-COMMUNITY",
    "question": "Vote on next month theme:",
    "options": ["Growth tactics", "Engineering deep-dive", "Founder stories"],
    "type": "multiple_choice",
    "anonymous": false,
    "duration_hours": 72
  }'
```

Pulse survey (recurring eNPS):

```bash
curl -X POST https://api.polly.ai/v1/templates/pulse \
  -H "Authorization: Bearer $POLLY_TOKEN" \
  -d '{
    "name": "Monthly Community Pulse",
    "cadence": "monthly",
    "day_of_month": 1,
    "questions": [
      {"text":"How likely are you to recommend this community? (0-10)", "type":"nps"},
      {"text":"What did you find most valuable?", "type":"text"},
      {"text":"One thing we should add?", "type":"text"}
    ],
    "audience": "channel:#community"
  }'
```

### Recipe 5: Geekbot async standup

Install Geekbot → `/geekbot setup`. Standup config (community version, 3-question weekly):

```yaml
standup:
  name: "Community Champions Weekly"
  participants:
    - user_group: '@ambassadors'
  schedule:
    days: [monday]
    time: '09:00'
    timezone: participant_local
  questions:
    - "What did you ship for the community last week?"
    - "What are you working on this week?"
    - "Where do you need help from the rest of us?"
  report_channel: '#ambassador-standup'
  reminder_after_minutes: 60
  anonymous: false
```

API for management:

```bash
# Create standup
curl -X POST https://api.geekbot.com/v1/standups \
  -H "Authorization: Token $GEEKBOT_TOKEN" \
  -d '{"name":"Engineering Champions","channel":"#eng-champs","time":"09:00","days":["mon","thu"]}'

# Pull last week's reports
curl -H "Authorization: Token $GEEKBOT_TOKEN" \
  "https://api.geekbot.com/v1/reports?after=$(date -d '7 days ago' +%s)"
```

### Recipe 6: Recurring engagement schedule via `slack-mcp.chat_scheduleMessage`

```python
# Weekly community-led posts via slack-mcp (no third-party bot)
import datetime
from zoneinfo import ZoneInfo

base = datetime.datetime(2026, 6, 15, 9, 0, tzinfo=ZoneInfo("America/New_York"))
schedule = [
    ("monday",    "Monday motivation: drop one win from last week."),
    ("tuesday",   "Tuesday tactics: share a tool that saved you an hour."),
    ("wednesday", "Wednesday wins: tag someone who helped you this week."),
    ("thursday",  "Thursday discussion: <topic>?"),
    ("friday",    "Friday wrap: TGIF — one ship / one ask / one cheer."),
]
for i, (day, text) in enumerate(schedule):
    post_at = int((base + datetime.timedelta(days=i)).timestamp())
    slack_mcp.chat_scheduleMessage(
        channel="C-COMMUNITY",
        post_at=post_at,
        text=text,
    )
```

### Recipe 7: Slack Canvas for charter + CoC pinning

```bash
mcp tool slack-mcp.canvases_create \
  --channel_id C-COMMUNITY \
  --title "Community Charter + CoC" \
  --document_content '# Charter
This community is for X. We value Y. See <#rules> for the full Code of Conduct.

# CoC summary
- Respect everyone.
- No harassment. Zero tolerance.
- Stay on-topic.
- Report issues to @mods.

Full CoC: https://docs.brand.com/coc'
```

Canvases replace pinned-message-walls; they live in the channel sidebar.

### Recipe 8: Pulse-survey results → warehouse for trend tracking

```python
# Pull Polly results weekly, store in postgres for trend
import requests, json
from datetime import datetime

resp = requests.get(
    "https://api.polly.ai/v1/results",
    headers={"Authorization": f"Bearer {POLLY_TOKEN}"},
    params={"template": "monthly-pulse", "since": "2026-05-01"}
)
for r in resp.json()["results"]:
    cur.execute(
        "INSERT INTO community_pulse (ts, nps, free_text, member_id) VALUES (%s,%s,%s,%s)",
        (r["completed_at"], r["nps_score"], json.dumps(r["text_answers"]), r["respondent_id"])
    )
```

Then HogQL via posthog-mcp or postgres query for nps_trend / cohort_nps / segment-by-tenure NPS.

### Recipe 9: Anti-spam + invite controls (admin)

```bash
# Block external invite links via Slack admin (Enterprise Grid)
mcp tool slack-mcp.admin_conversations_setTeams --channel_id C-XX --team_ids T-MAIN

# Approval policy
# Settings → Manage apps → App approval → Require approval

# Anti-DM-spam: limit DMs to verified members only via slack-mcp scim
# Setup via Admin → People → User groups → "Verified" group
```

For non-Grid plans, configure via slackbot keyword responses + manual mod review.

### Recipe 10: Workflow Builder kudos channel

```json
{
  "trigger": "shortcut",
  "name": "Give kudos",
  "form": [
    {"label":"Recipient","type":"user","required":true},
    {"label":"What did they do?","type":"text","required":true}
  ],
  "steps": [
    {
      "type":"send_message",
      "channel":"#kudos",
      "message":":raised_hands: <@{recipient}> got kudos from <@{user_id}>: {what_did_they_do}"
    },
    {
      "type":"send_message",
      "channel":"{recipient}",
      "message":"You got kudos! <#kudos>"
    }
  ]
}
```

Surfaces recognition without bot install. Tie completion to ambassador-tier nomination criteria.

## Examples

### Example 1: New B2B community Slack launch (0 → 500 members)

**Goal:** Standup engagement stack before invites open.

**Steps:**
1. Slack workspace + channels + user groups created (admin step).
2. App approval policy set: only Polly, Geekbot, Donut, slack-mcp pre-approved.
3. Workflow Builder welcome flow (Recipe 2) deployed.
4. Donut connected to `#donut-pairings`, cadence bi-weekly (Recipe 3).
5. Polly install for ad-hoc polls + monthly pulse template (Recipe 4).
6. Geekbot setup but disabled until 50+ ambassadors.
7. Engagement schedule via `slack-mcp.chat_scheduleMessage` (Recipe 6).
8. Invite link opened.

**Result:** Week 1: 80% of joiners complete welcome flow. Week 4: avg 4 Donut intros per user. Month 2: first monthly pulse NPS = 47.

### Example 2: Async-distributed Ambassador standup ritual

**Goal:** 30 ambassadors across 8 timezones share weekly progress without sync meeting.

**Steps:**
1. Create `@ambassadors` user group with 30 members.
2. Geekbot standup config (Recipe 5) targeting `@ambassadors`, weekly Monday.
3. Report channel `#ambassador-standup` (private, visible only to ambassador group + mods).
4. Reminder after 60 min if not responded.
5. Weekly digest: scrape Geekbot report → summarize top wins/asks via Claude → post to `#ambassador-leadership` channel.

**Result:** 22 of 30 (73%) respond by Tuesday EOD. Top wins surfaced as monthly community recap content.

### Example 3: Replace failing single-bot stack

**Goal:** Community uses only Polly; engagement stalled. Add Donut + Workflow Builder welcome.

**Steps:**
1. Audit existing Polly usage — 60% poll engagement but no new-member retention.
2. Identify gap: welcome flow + intro pairing absent.
3. Add Workflow Builder welcome flow (Recipe 2) — free, native.
4. Add Donut (Recipe 3) cadence bi-weekly.
5. Track: 7-day post-rate of new members + repeat-Donut acceptance.

**Result:** 7-day post-rate rose from 18% → 41% after 30 days. Donut acceptance 68%.

## Edge cases / gotchas

- **Slack OAuth scopes** — Polly + Geekbot + Donut each request broad scopes (`chat:write`, `users:read`, `channels:history`). Admin approval needed for Enterprise plans; expect 1-3 day review.
- **App approval policy lockout** — if admin enables "require approval for all apps", new bots block until manual approval. Pre-approve Polly + Geekbot + Donut + slack-mcp before launch.
- **Donut no API** — Donut has no public REST API as of June 2026. All config via `/donut` slash command + dashboard. Programmatic alternatives: build pairing via `slack-mcp.users_list` + random shuffle + `chat_postMessage` to a created MPIM.
- **Polly free tier** — free Polly limited to 25 polls/month; pulse-survey templates require Pro ($24/user/mo).
- **Geekbot timezone bugs** — participant timezone setting in Slack must be correct; otherwise reminders fire at wrong local time. Validate via Geekbot dashboard → Members → Timezone column.
- **Standup-channel noise** — daily standups in shared channel clutter feed. Always send to private `#standup-<team>` channel; cross-post weekly digest only.
- **Workflow Builder paid plans** — Workflow Builder is free for Basic+ but some features (forms, multi-step, custom integrations) require paid plan.
- **chat_scheduleMessage limits** — max 1024 scheduled messages per workspace at once; queue overruns silently drop.
- **Channel rate limits** — 1 msg/sec/channel sustained. Bursty bots hit Tier 3 (50 req/min). Batch where possible.
- **DM-spam law** — unsolicited DMs to all members violate Slack ToS + GDPR. Use channel posts + opt-in workflows.
- **Multi-workspace setup** — Donut + Geekbot are workspace-scoped. Connect each workspace separately for Enterprise Grid orgs.
- **Bot retention costs** — auditing 5 bots/year shows ~80% of engagement lift comes from Donut + Workflow Builder + native scheduling. Polly + Geekbot add 20%. Don't over-stack.
- **Polly anonymous vs named** — anonymous polls reduce response bias but hide patterns. Default named for community spirit; anonymous for sensitive topics only.
- **App quota** — workspaces capped at 10 apps on free plan, unlimited paid. Pre-budget before launch.

## Sources

- [Slack Web API reference](https://api.slack.com/methods)
- [Slack Workflow Builder](https://api.slack.com/workflows)
- [Slack Canvas API](https://api.slack.com/methods/canvases.create)
- [Polly developer docs](https://www.polly.ai/api)
- [Geekbot API reference](https://geekbot.com/developers/)
- [Donut help center](https://help.donut.com/)
- [Slack rate limits](https://api.slack.com/docs/rate-limits)
- [Standuply API](https://standuply.com/api-doc)
- [Slack Enterprise app approval](https://slack.com/help/articles/360011484311-Manage-apps-with-Enterprise-Grid)
