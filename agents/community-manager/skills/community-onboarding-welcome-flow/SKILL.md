<!--
Sources: https://help.circle.so/p/onboarding-members + https://mee6.xyz/en/welcome + https://api.slack.com/workflows + https://carl.gg/commands
-->
# Community Onboarding & Welcome Flow — SKILL

Multi-step onboarding: welcome DM → introduce-yourself prompt → guided tour → role-claim self-serve → first-action nudge within 7 days. Cross-platform (Discord / Slack / Circle / Discourse / Mighty / Skool). KPI: % joiners who post in 7 days.

## When to use

- New community spin-up — need welcome flow before opening invites.
- Existing community where activation rate (post-in-7d) is <15% — onboarding is leaking.
- Adding a new channel/category requiring its own intro flow.
- Re-onboarding ghost members (joined >30d, no activity).
- Cohort onboarding for course/event-driven communities.

Trigger phrases: "welcome flow", "onboarding", "activation rate", "introduce-yourself", "first 7 days", "role-claim".

## Setup

```bash
# Discord MCP (already in agent.yaml)
mcp tool discord-mcp-full.create_webhook --channel_id $WELCOME --name "OnboardBot"

# Slack workflows (Workflow Builder API)
mcp tool slack.admin.workflows_listSteps

# Circle API via cli-anything
curl -H "Authorization: Bearer $CIRCLE_TOKEN" \
  https://app.circle.so/api/v1/spaces

# Notion for onboarding-playbook source of truth
mcp tool notion.create_database --parent_id $COMMUNITY_PAGE --title "Onboarding playbook"
```

Auth + env:
- `DISCORD_BOT_TOKEN` — bot with `Send Messages`, `Manage Roles`, `Read Message History`. Add to welcome channel.
- `SLACK_BOT_TOKEN` — scopes: `chat:write`, `users:read`, `im:write`, `workflow:write`.
- `CIRCLE_TOKEN` — Settings → Developers → API. Owner role only.
- `MEE6_DASHBOARD_URL` — manual one-time install via OAuth at `mee6.xyz`.

Workspace prerequisites:
- Discord: `#welcome`, `#introduce-yourself`, `#start-here`, `#announcements`, `#roles` channels.
- Slack: `#welcome`, `#introductions`, `#start-here`.
- Roles: `Member`, `Verified`, `Contributor`, plus opt-in interest roles (`#frontend`, `#design`, `#backend`).

## Common recipes

### Recipe 1: Discord welcome DM via MEE6 / Carl-bot

In Carl-bot dashboard (`carl.gg/dashboard/<guild_id>/welcome`):

```yaml
welcome_message:
  channel: '#welcome'
  message: |
    Welcome {user.mention} to {guild.name}!
    1. Read the rules in <#rules>
    2. Introduce yourself in <#introduce-yourself>
    3. Claim interest roles in <#roles>
  dm: |
    Hey {user.name} — thanks for joining! Here's the 60-second tour: {tour_link}
```

Or via `discord-mcp-full`:

```bash
mcp tool discord-mcp-full.send_dm \
  --user_id $USER_ID \
  --content "Welcome to the $COMMUNITY! Three things to do in your first day: ..."
```

### Recipe 2: Auto-role on join (Discord)

```bash
mcp tool discord-mcp-full.add_member_role \
  --guild_id $GUILD_ID \
  --user_id $USER_ID \
  --role_id $MEMBER_ROLE_ID
```

Or fire on `GUILD_MEMBER_ADD` event via Carl-bot/MEE6 native config.

### Recipe 3: Reaction-roles for interests (Carl-bot)

```yaml
reaction_role:
  channel_id: $ROLES_CHANNEL
  message: "React to claim your interest role"
  reactions:
    "🎨": Design
    "💻": Frontend
    "⚙️": Backend
    "📈": Growth
```

Members self-serve which firehose they want.

### Recipe 4: Slack Workflow Builder onboarding

```bash
# Workflow JSON for "new member joined" trigger
cat <<'JSON' > welcome_workflow.json
{
  "title": "New member welcome",
  "trigger": "channel_join",
  "channel": "#welcome",
  "steps": [
    {"type": "send_dm", "to": "{{user}}", "text": "Welcome! Share what brought you here in #introductions."},
    {"type": "post_in_channel", "channel": "#welcome", "text": ":wave: {{user}} just joined — say hi!"},
    {"type": "delay", "minutes": 60},
    {"type": "send_dm", "to": "{{user}}", "text": "Quick tour: 1. About → #start-here, 2. Goals → #goals-2026, 3. Help → #help."}
  ]
}
JSON

# Workflow installs via Slack UI (Workflow Builder); manual one-time
```

### Recipe 5: Circle "Welcome posts" auto-create

```bash
# Pin a welcome post in every space
for SPACE_ID in $(curl -s -H "Authorization: Bearer $CIRCLE_TOKEN" https://app.circle.so/api/v1/spaces | jq -r '.[].id'); do
  curl -X POST -H "Authorization: Bearer $CIRCLE_TOKEN" \
    -H "Content-Type: application/json" \
    https://app.circle.so/api/v1/spaces/$SPACE_ID/posts \
    -d '{"name": "Welcome — start here", "body": "<welcome markdown>", "pinned": true}'
done
```

### Recipe 6: 7-day activation drip (Discord)

```python
# Day 0: welcome DM
# Day 1: "Have you introduced yourself yet?" DM if no posts
# Day 3: "Here are 3 great recent discussions" DM
# Day 7: "Need help getting started? Reply to this and we'll match you with a mentor."

import time, datetime as dt

PROMPTS = [
  (0,  "welcome_initial"),
  (1,  "intro_nudge_if_no_post"),
  (3,  "top_discussions_digest"),
  (7,  "mentor_match_offer"),
]

for member in list_recently_joined():
  for day, key in PROMPTS:
    if member.day_since_join == day and not member.has_posted:
      send_dm(member.id, render_template(key, member))
```

### Recipe 7: Track activation rate (7d post-rate)

```sql
-- Postgres / warehouse query
WITH joins AS (
  SELECT user_id, joined_at FROM community_members
  WHERE joined_at >= NOW() - INTERVAL '30 days'
),
posts AS (
  SELECT user_id, MIN(created_at) AS first_post_at FROM community_posts
  GROUP BY user_id
)
SELECT
  COUNT(*) AS joined,
  COUNT(p.user_id) FILTER (WHERE p.first_post_at <= j.joined_at + INTERVAL '7 days') AS activated,
  ROUND(100.0 * COUNT(p.user_id) FILTER (WHERE p.first_post_at <= j.joined_at + INTERVAL '7 days') / COUNT(*), 1) AS activation_pct
FROM joins j
LEFT JOIN posts p USING (user_id);
```

Target: >25% (B2C) or >15% (B2B). <10% = onboarding broken.

### Recipe 8: Intro-channel template post

```markdown
**Welcome — please copy/paste and fill in:**

- **Name + handle:**
- **Where you work / what you build:**
- **One thing you're hoping to learn here:**
- **One thing you can help others with:**
- **Random fun fact:**

(React with 👋 to any intro you want to chat with)
```

Lowers the friction of "what do I say?" by 80%.

### Recipe 9: Reverse-funnel ghost re-onboarding

```bash
# Members who joined >30d ago but haven't posted: send "we miss you" DM
psql -c "SELECT user_id FROM members WHERE joined_at < NOW() - INTERVAL '30 days' AND last_post_at IS NULL" | \
  while read user_id; do
    mcp tool discord-mcp-full.send_dm --user_id $user_id \
      --content "Hey — noticed you're not active yet. Anything we can help with?"
  done
```

## Examples

### Example 1: 100-user Discord — 9% → 28% activation

**Setup:** Existing 100-member Discord with 9% post-in-7d. Add Carl-bot welcome + reaction-roles + 7-day drip + intro-template.

**Steps:**
1. Carl-bot welcome message (Recipe 1).
2. Auto-assign `Member` role on join (Recipe 2).
3. `#roles` reaction-role for 6 interests (Recipe 3).
4. 7-day drip via `discord-mcp-full` cron (Recipe 6).
5. Pin intro-template in `#introduce-yourself` (Recipe 8).
6. After 30 days, query Recipe 7 — expect 25–30%.

**Result:** Reachedactivation 28% in 4 weeks; mentor-match driving second-post.

### Example 2: Slack design-partner channel for 20 customers

**Setup:** Private Slack with 20 enterprise design partners. Need warm welcome + quick activation; CX team checks daily.

**Steps:**
1. Slack workflow trigger on join → DM (Recipe 4).
2. Pin `#start-here` canvas: roadmap, contacts, weekly office hours.
3. Day-3 personalized DM from CSM offering a 15-min intro call.
4. Day-7 "share a request or pain point" DM.

**Result:** 19/20 partners post within 7d; 8 books CSM call.

## Edge cases / gotchas

- **Bot install scopes** — Carl-bot welcome needs `Manage Roles` higher than the role it assigns. Hierarchy gotcha.
- **DM blocking** — Discord users can disable DMs from server members; have a fallback channel-mention.
- **Slack workflow rate limit** — 1 workflow run / user / minute. Don't fire multiple at once.
- **Circle pinned-post limit** — only 1 pin per space; rotate quarterly.
- **Over-onboarding** — 4+ messages in first 24h causes mute. Pace: Day 0, Day 1 nudge, Day 3 digest, Day 7 mentor.
- **Privacy** — don't surface joiners by name unless they've posted (some prefer lurk-first).
- **GDPR DM consent** — EU members may flag automated DMs; include opt-out language ("reply STOP to stop").
- **Time-zone shift** — fire welcome 9am–6pm member local time, not server UTC.
- **Cohort onboarding** — for course communities, schedule whole-cohort kickoff post, not individual DMs (creates collective momentum).
- **Re-onboarding ghosts** — Cap to 1 attempt/quarter; more feels desperate.
- **Activation rate ≠ engagement** — 25% activation but 5% week-2 retention means content not channel. Diagnose separately.

## Sources

- [Circle onboarding guide](https://help.circle.so/p/onboarding-members)
- [MEE6 welcome plugin](https://mee6.xyz/en/welcome)
- [Carl-bot commands](https://docs.carl.gg/)
- [Slack Workflow Builder](https://slack.com/help/articles/360035692513)
- [Discord developer add-member-role](https://discord.com/developers/docs/resources/guild#add-guild-member-role)
- [Reforge community-engagement funnel](https://www.commonroom.io/blog/community-engagement-funnel/)
