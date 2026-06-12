<!--
Sources: https://discord.com/developers/docs/resources/auto-moderation + https://carl.gg/ + https://mee6.xyz/ + https://dyno.gg/ + https://meta.discourse.org/c/dev/automation/ + https://www.reddit.com/r/AutoModerator/wiki/library
-->
# Moderation Policies + Bot Stack — SKILL

Multi-platform moderation: Discord (AutoMod + Carl-bot + MEE6 + Dyno + Wick), Slack (admin controls + AntiSpam), Discourse (trust levels + Akismet), Reddit (AutoModerator YAML + Toolbox). Severity ladder: warn → mute (1h/24h) → kick → ban. Output is a YAML rule pack per platform deployed via API.

## When to use

- New server going from invite-only to public (needs raid + spam defense before opening).
- Mod-incident spike — recent surge of harassment / spam / bot accounts.
- Coverage gap (no anti-raid; AutoMod off; no slur filter).
- Multi-platform community needing consistent enforcement.
- Volunteer mod team needs auto-actions for nights/weekends.
- Public-trust crisis — viral negative thread needs faster mod response.

Trigger phrases: "moderation policies", "AutoMod", "Carl-bot", "Dyno anti-raid", "Discord raid", "Discourse Akismet", "Reddit AutoModerator", "mod stack".

## Setup

```bash
# Discord MCP for direct AutoMod rules
mcp tool discord-mcp-full.create_automod_rule \
  --guild_id $GUILD_ID --name "slur-filter" --event_type 1 --trigger_type 4

# Carl-bot dashboard install (manual OAuth one-time)
# https://carl.gg/

# Reddit MCP for AutoMod YAML
mcp tool reddit.update_wiki_page \
  --subreddit yourproduct --page "config/automoderator" --content "$(cat automod.yaml)"

# Discourse via cli-anything
curl -X PUT -H "Api-Key: $DISCOURSE_KEY" \
  https://forum.brand.com/admin/site_settings/automatic_topic_heat_values.json
```

Auth + env:
- `DISCORD_BOT_TOKEN` — bot with `Manage Messages`, `Ban Members`, `Kick Members`, `Manage Roles`, `Moderate Members` scopes.
- `CARL_BOT_INVITE_URL` — `https://carl.gg/invite` (OAuth flow).
- `MEE6_DASHBOARD_URL` — `https://mee6.xyz/dashboard` (web UI).
- `DYNO_BOT_INVITE` — `https://dyno.gg/invite` (OAuth).
- `REDDIT_CLIENT_ID` + `REDDIT_CLIENT_SECRET` + mod-account refresh token.
- `DISCOURSE_KEY` — Admin → API.

Workspace prerequisites:
- Discord mod role `@mods` higher than member roles.
- Reddit mod permissions: `posts`, `mail`, `wiki`, `config`.
- Discourse `moderator` user level.

## Common recipes

### Recipe 1: Discord AutoMod rule (slur + keyword filter)

```bash
mcp tool discord-mcp-full.create_automod_rule \
  --guild_id $GUILD_ID \
  --name "Slur filter" \
  --event_type 1 \
  --trigger_type 4 \
  --trigger_metadata '{"keyword_filter": ["slur1", "slur2"], "regex_patterns": ["(?i)bad.*word"]}' \
  --actions '[{"type": 1, "metadata": {"custom_message": "Removed — see #rules"}}, {"type": 2, "metadata": {"channel_id": "$MOD_LOG"}}]'
```

`event_type 1` = MESSAGE_SEND. `trigger_type 4` = KEYWORD. Actions: `1` block, `2` send-alert.

### Recipe 2: Discord AutoMod — invite-link block

```bash
mcp tool discord-mcp-full.create_automod_rule \
  --guild_id $GUILD_ID \
  --name "Invite-link block" \
  --event_type 1 \
  --trigger_type 4 \
  --trigger_metadata '{"regex_patterns": ["discord\\.gg/[a-zA-Z0-9]+"]}' \
  --actions '[{"type": 1}]' \
  --exempt_roles '["$TRUSTED_ROLE"]'
```

### Recipe 3: Carl-bot reaction-roles + auto-mod

In Carl-bot dashboard `carl.gg/dashboard/<guild_id>/automod`:

```yaml
spam_filter:
  duplicate_messages: 5  # 5 same messages → mute 10m
  mention_spam: 8        # 8 mentions in one msg → mute 1h
  caps_filter: 0.7       # 70% caps in 10+ char msg → warn
  link_filter: whitelist_only
welcome_message:
  channel: '#welcome'
  message: "Welcome {user.mention} — react ✅ in #rules to verify"
```

### Recipe 4: Dyno anti-raid

In Dyno dashboard `dyno.gg/manage/<guild_id>/automod`:

```yaml
anti_raid:
  join_rate: 10  # 10 joins in 60s → lockdown
  account_age_min_days: 7
  auto_action: kick
mute_role: '@Muted'
```

Lockdown auto-prevents new joins for 10min while mods inspect.

### Recipe 5: Severity ladder + audit log

```python
# Centralized mod-action log (any platform)
LADDER = {
  1: ("warn", "Private DM warning"),
  2: ("mute_1h", "1h timeout"),
  3: ("mute_24h", "24h timeout"),
  4: ("kick", "kick from server"),
  5: ("ban", "permanent ban"),
}

def escalate(user_id, current_tier, reason):
    new_tier = min(current_tier + 1, 5)
    action, desc = LADDER[new_tier]
    mod_action_log(user_id, action, reason)
    # Discord
    if action.startswith("mute_"):
        hrs = int(action.split("_")[1].rstrip("h"))
        mcp.discord_full.timeout_member(user_id, duration=hrs * 3600)
    elif action == "kick":
        mcp.discord_full.kick_member(user_id)
    elif action == "ban":
        mcp.discord_full.ban_member(user_id, reason=reason)
```

### Recipe 6: Slack admin tightening

```bash
# Tighten member-invite permissions
curl -X POST -H "Authorization: Bearer $SLACK_ADMIN_TOKEN" \
  https://slack.com/api/admin.teams.settings.setInvitedPermissions \
  -d '{"team_id": "$TEAM_ID", "invited_user_permissions": "admin_only"}'

# Disable @channel for non-admins
curl -X POST -H "Authorization: Bearer $SLACK_ADMIN_TOKEN" \
  https://slack.com/api/admin.conversations.setConversationPrefs \
  -d '{"channel_id": "$CH_ID", "prefs": {"who_can_post": "admins_only_for_general"}}'
```

### Recipe 7: Discourse trust-level + Akismet

```bash
# Enable Akismet spam filter (Admin → Settings → akismet_api_key)
curl -X PUT -H "Api-Key: $DISCOURSE_KEY" \
  https://forum.brand.com/admin/site_settings/akismet_api_key.json \
  -d "{\"akismet_api_key\":\"$AKISMET_KEY\"}"

# TL3 grant criteria (Admin → Settings → "tl3 requires_*")
# tl3_requires_likes_given: 30
# tl3_requires_topics_replied_to: 10
# Auto-promote raises mod-capacity for free
```

### Recipe 8: Reddit AutoModerator YAML

```yaml
# Posted to /r/yourproduct/wiki/config/automoderator
# Doc: https://www.reddit.com/r/AutoModerator/wiki/library

---
type: submission
title+body (regex): "(?i)(buy|sale|discount|click my link)"
action: remove
action_reason: "self-promo blocked"
modmail_subject: "Auto-removed self-promo"
comment: |
  Hi — your post was removed for self-promotion. See [rule 3](/r/yourproduct/about/rules).
---
type: comment
author:
  comment_karma: "< -10"
action: filter
action_reason: "low-karma filter"
---
type: any
body (regex): "\\b(slur1|slur2|slur3)\\b"
action: remove
action_reason: "slur filter"
```

```bash
mcp tool reddit.update_wiki_page \
  --subreddit yourproduct --page "config/automoderator" \
  --content "$(cat automod.yaml)" --reason "AutoMod v$(date +%Y%m%d)"
```

### Recipe 9: Discourse automation plugin (replace TL3 abuse)

```yaml
# Admin → Plugins → Discourse Automation → Add automation
trigger: post_created_edited
conditions:
  - flagged_post_count: ">= 3"
action: send_pms
recipients: '@mods'
title: "User flagged 3x in 24h"
```

### Recipe 10: Cross-platform mod-action audit

```sql
-- Postgres warehouse — keep all mod actions in one table
CREATE TABLE mod_actions (
  id BIGSERIAL PRIMARY KEY,
  platform TEXT,        -- discord / slack / discourse / reddit
  user_id TEXT,
  username TEXT,
  action TEXT,          -- warn / mute / kick / ban
  reason TEXT,
  evidence_url TEXT,
  acting_mod TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Weekly mod-load report
SELECT acting_mod, COUNT(*) AS actions, MAX(created_at) AS last
FROM mod_actions WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY acting_mod ORDER BY actions DESC;
```

## Examples

### Example 1: New public Discord — full mod stack

**Goal:** 0 → 1k member Discord launch.

**Steps:**
1. AutoMod slur filter + invite filter (Recipes 1, 2).
2. Carl-bot install for reaction-roles + spam-mute + welcome (Recipe 3).
3. Dyno install for anti-raid (Recipe 4).
4. Severity ladder coded in Python wrapper (Recipe 5).
5. `#mod-log` channel + audit table (Recipe 10).

**Result:** 0 successful raids in 90 days; mod incidents resolved in <10min average.

### Example 2: Subreddit hardening

**Goal:** 5k subscriber subreddit, recurring spam waves.

**Steps:**
1. Author AutoModerator YAML (Recipe 8).
2. Push via wiki API.
3. Install Reddit Toolbox extension for mod team.
4. Weekly mod-load report (Recipe 10).

**Result:** Spam → 70% reduction; mod hours/week dropped from 12 to 3.

## Edge cases / gotchas

- **AutoMod regex DoS** — overly complex regex (lookarounds, backrefs) cause AutoMod to silently drop. Test with simple patterns first.
- **Carl-bot premium gate** — anti-raid + advanced features require Carl-bot Premium ($5/mo).
- **Dyno + MEE6 + Carl conflict** — multiple bots applying actions to same message → race. Disable overlapping features in each.
- **Bot hierarchy** — bot's top role must be above any role it moderates. New custom role = re-check hierarchy.
- **Discord AutoMod 6-rule limit** per guild per trigger type. Combine smartly.
- **Reddit AutoModerator silent failures** — bad YAML doesn't error; rules just don't fire. Test in modmail with regex sandbox.
- **Discourse Akismet false positives** — non-English posts often flagged; whitelist trusted users.
- **Slack admin scopes** — `admin.*` API requires Enterprise Grid. Pro plan has limited automation.
- **Ban appeals via DM** — Discord disables DMs to banned users; provide an email channel.
- **Mod-of-the-mods accountability** — keep mod-action log to prevent volunteer mods from going rogue.
- **Don't auto-ban based on keywords alone** — false positives create resentment. Use auto-mute + mod review.
- **Public mod-actions** — Discord audit log is visible to mods; redact sensitive context in `reason`.
- **Volunteer mod burnout** — cap solo mod hours; rotate weeks. AutoMod offloads ~70% of routine.

## Sources

- [Discord AutoModeration API](https://discord.com/developers/docs/resources/auto-moderation)
- [Carl-bot docs](https://docs.carl.gg/)
- [MEE6 plugins](https://mee6.xyz/en/plugins)
- [Dyno modules](https://dyno.gg/modules)
- [Discourse automation](https://meta.discourse.org/c/dev/automation/)
- [Reddit AutoModerator library](https://www.reddit.com/r/AutoModerator/wiki/library)
- [Reddit Toolbox](https://www.reddit.com/wiki/toolbox)
- [Akismet docs](https://akismet.com/developers/)
