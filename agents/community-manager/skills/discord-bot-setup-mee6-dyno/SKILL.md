<!--
Sources: https://mee6.xyz/ + https://carl.gg/ + https://dyno.gg/ + https://discord.com/developers/docs/ + https://statbot.net/
-->
# Discord Bot Setup (MEE6 / Dyno / Carl-bot) — SKILL

Layered bot stack: MEE6 (leveling + auto-mod + reaction roles), Carl-bot (advanced auto-mod + embeds), Dyno (anti-raid + mod logs), Wick (anti-raid premium), Statbot (analytics), Tickets (DM-to-ticket bridge). Each replaces a manual mod action. Config via dashboards or `playwright-mcp` automation + `discord-mcp-full` for direct API ops.

## When to use

- New Discord server going live (essential setup).
- Existing server lacking mod automation / leveling / welcome flow.
- Anti-raid hardening before a large announcement / launch.
- Bot stack migration (e.g., MEE6 → Carl-bot) to reduce cost.
- Adding ticket / support flow.
- Public-facing analytics + leaderboards.

Trigger phrases: "Discord bot", "MEE6 setup", "Carl-bot config", "Dyno", "anti-raid", "leveling bot", "reaction roles", "tickets bot", "Statbot".

## Setup

```bash
# Bot OAuth install (manual, one-time per server)
# MEE6: https://mee6.xyz/add
# Carl-bot: https://carl.gg/invite
# Dyno: https://dyno.gg/invite
# Wick: https://wickbot.com/invite
# Statbot: https://statbot.net/invite
# Tickets: https://tickets.bot/invite

# discord-mcp-full for direct operations
mcp tool discord-mcp-full.list_guild_roles --guild_id $GUILD_ID
mcp tool discord-mcp-full.create_role --guild_id $GUILD_ID --name "Verified"

# playwright-mcp for dashboard automation
mcp tool playwright.navigate --url "https://carl.gg/dashboard/$GUILD_ID/welcome"
```

Auth + env:
- `DISCORD_BOT_TOKEN` — for direct API.
- Manual install: each bot needs OAuth (open browser, click Authorize, pick server).
- Carl-bot Premium $5/mo unlocks anti-raid + extended limits.

Workspace prerequisites:
- Server with mod role above bot roles.
- Channels: `#welcome`, `#rules`, `#mod-log`, `#bot-spam`, `#roles`, `#tickets`.
- Roles: `Member`, `Verified`, `Booster`, `Mod`, `Admin`.

## Common recipes

### Recipe 1: Bot install order

Install in this order (each builds on prior):

1. **discord-mcp-full** — programmatic baseline (token bot).
2. **MEE6** — welcome + leveling + basic auto-mod.
3. **Carl-bot** — reaction roles + advanced auto-mod (replace MEE6 auto-mod).
4. **Dyno** — anti-raid + mod logs (Carl-bot has lite version; Dyno is stronger).
5. **Statbot** — server analytics (read-only).
6. **Tickets** — support ticket DM bridge (only if support volume warrants).

Why this order: each replaces overlapping features of the previous one progressively.

### Recipe 2: MEE6 config (manual via dashboard)

`mee6.xyz/dashboard/<guild_id>`:

```yaml
welcome:
  enabled: true
  channel: '#welcome'
  message: |
    Welcome {user.mention} to {server.name}!
    Read <#rules> then react ✅ to verify.
  dm: |
    Hey {user.name}! Quick tour: {server.docs_url}
leveling:
  enabled: true
  xp_per_message: 15-25 random
  cooldown: 60s
  rewards:
    5: 'Member'
    20: 'Active Member'
    50: 'VIP'
custom_commands:
  '!docs': 'See {docs_url}'
  '!rules': 'See <#rules>'
```

### Recipe 3: Carl-bot reaction-roles

`carl.gg/dashboard/<guild_id>/rr`:

```yaml
reaction_role_message:
  channel: '#roles'
  embed_title: 'Pick your interests'
  embed_description: 'React to assign yourself a role'
  reactions:
    - emoji: '🎨'
      role: 'Design'
    - emoji: '💻'
      role: 'Frontend'
    - emoji: '⚙️'
      role: 'Backend'
    - emoji: '📈'
      role: 'Growth'
    - emoji: '🤖'
      role: 'AI/ML'
  type: 'normal'  # or 'unique', 'verify'
```

Or via `discord-mcp-full` direct API:

```bash
mcp tool discord-mcp-full.create_message \
  --channel_id $ROLES_CH \
  --content "Pick your interests by reacting below" \
  --embed '{"title":"Roles","fields":[...]}'

mcp tool discord-mcp-full.add_reaction \
  --channel_id $ROLES_CH --message_id $MSG_ID --emoji "🎨"
```

### Recipe 4: Carl-bot advanced auto-mod

`carl.gg/dashboard/<guild_id>/automod`:

```yaml
automod:
  filters:
    invites:
      block: true
      whitelist: ['discord.gg/our-server']
    bad_words:
      list: ['slur1', 'slur2']
      action: delete
    spam:
      duplicates: 5  # 5 same msgs in 10s
      mentions: 8    # 8 mentions in 1 msg
      caps_pct: 0.7  # 70% caps in 10+ char msg
      action: mute_10m
    nitro_scam:
      regex: 'free.nitro|gift\\.discord'
      action: delete + ban
  exempt_roles: ['Mod', 'Admin']
```

### Recipe 5: Dyno anti-raid

`dyno.gg/manage/<guild_id>/automod`:

```yaml
anti_raid:
  join_rate: 10  # 10 joins in 60s → trigger
  account_age_min_days: 7
  action_on_trigger:
    - lockdown_new_joins: true
    - ping_role: '@mods'
    - log: '#mod-log'
  duration: 10m
```

### Recipe 6: Carl-bot embed welcome

```yaml
welcome_embed:
  channel: '#welcome'
  embed:
    title: 'Welcome to $COMMUNITY'
    description: '{user.mention} just joined!'
    fields:
      - name: 'Member #'
        value: '{server.member_count}'
        inline: true
      - name: 'First step'
        value: 'React ✅ to verify in <#rules>'
        inline: true
    color: 0x5865F2
    thumbnail: '{user.avatar_url}'
```

### Recipe 7: Tickets bot config

`tickets.bot/dashboard/<guild_id>`:

```yaml
tickets:
  panel:
    channel: '#tickets'
    message: 'Need help? Click 🎫'
    button_label: 'Open ticket'
    button_emoji: '🎫'
  channels:
    create_in_category: 'TICKETS'
    naming: 'ticket-{user.name}-{ticket.id}'
  permissions:
    only_visible_to: ['user', 'staff']
  close_after_inactivity: 48h
  transcript: true
```

### Recipe 8: Statbot dashboard config

`statbot.net/dashboard/<guild_id>/config`:

```yaml
public_dashboard:
  enabled: true
  url: stats.brand.com
  show: ['member-count', 'top-channels', 'top-members', 'activity-graph']
  exclude_channels: ['#mod-log', '#tickets', '#private']
```

### Recipe 9: Verify-on-react flow (Carl-bot)

```yaml
# In #rules
verify_message:
  channel: '#rules'
  embed:
    description: 'Read all the rules. React ✅ to verify and unlock the rest of the server.'
  reaction_role:
    emoji: '✅'
    role: 'Verified'
    type: 'verify'  # one-time; can't unreact to un-verify
```

Permission override: `@everyone` denied view of all channels except `#rules` + `#welcome`. `@Verified` granted view of all.

### Recipe 10: Bot health monitor

```python
# Daily check: are bots online + responding?
for bot_id in [MEE6, CARL, DYNO, STATBOT, TICKETS]:
    member = discord_full.get_member(guild_id=GUILD, user_id=bot_id)
    if member.status != 'online':
        slack.alert(f"Discord bot {bot_id} offline since {member.last_seen}")

# Carl-bot specifically — test by mentioning
discord_full.send_message(
  channel_id=BOT_TEST_CH,
  content="!ping"
)
# Expected response within 5s
```

## Examples

### Example 1: Greenfield server, 0 → 1k members in 30 days

**Goal:** Launch new community Discord with full safety + engagement stack before invites open.

**Steps:**
1. Install order (Recipe 1) — Day 0.
2. MEE6 welcome + leveling (Recipe 2) — Day 0.
3. Carl-bot reaction-roles + auto-mod (Recipes 3, 4) — Day 1.
4. Dyno anti-raid (Recipe 5) — Day 2.
5. Verify-on-react flow (Recipe 9) — Day 2.
6. Tickets bot (Recipe 7) — Day 7 once support volume warrants.
7. Statbot dashboard (Recipe 8) — Day 14.
8. Health monitor (Recipe 10) — ongoing.

**Result:** 0 raids, ≥25% activation, mod-action automation handling 80%.

### Example 2: Migrate from MEE6 Premium to Carl-bot Premium ($30/mo savings)

**Goal:** Cut bot costs without losing features.

**Steps:**
1. Map MEE6 features → Carl-bot equivalents.
2. Export MEE6 levels via dashboard CSV.
3. Carl-bot leveling import via Premium add-on.
4. Reaction roles re-created in Carl-bot (Recipe 3).
5. Disable MEE6 auto-mod; enable Carl-bot (Recipe 4).
6. Uninstall MEE6 (kick bot from server).

**Result:** $30/mo saved; feature parity; smoother UI.

## Edge cases / gotchas

- **Bot role hierarchy** — bot must have role higher than roles it assigns. New custom role = re-check.
- **Overlap conflicts** — MEE6 + Carl-bot + Dyno all do auto-mod. Pick one per feature; disable in others.
- **Premium feature lock** — Carl-bot Premium = $5/mo; without it, no anti-raid, limited reaction roles.
- **MEE6 ads** — Free tier shows MEE6 ads on level-up; Premium removes.
- **Verify-flow gotcha** — must deny `@everyone` view of channels EXCEPT `#rules`/`#welcome`, else verify gates nothing.
- **Reaction-role limit** — Discord allows 20 reactions per message; needing more requires multiple messages.
- **Tickets bot DM blocked** — users with DMs off can't ticket; provide fallback `#help` channel.
- **Statbot privacy** — public dashboard exposes member counts + names. Some communities want private-only.
- **Bot rate limits** — when 5+ bots fire on same event, rate-limit cascade. Stagger triggers.
- **Discord API outages** — bots disable; have manual mod team for downtime.
- **Anti-raid false positives** — high-energy launch can trigger lockdown; raise threshold during planned waves.
- **Custom command spam** — `!docs`, `!rules`, etc. can flood; rate-limit per user per command.
- **Audit log noise** — too many bot actions = audit log overflow; route bot actions to dedicated `#mod-log`.
- **License + ToS** — MEE6 ToS forbids self-hosting; Wick custom bots are okay.

## Sources

- [Discord developer docs](https://discord.com/developers/docs/intro)
- [MEE6 plugins](https://mee6.xyz/en/plugins)
- [Carl-bot docs](https://docs.carl.gg/)
- [Carl-bot reaction-roles](https://docs.carl.gg/#/reactionroles)
- [Dyno modules](https://dyno.gg/modules)
- [Statbot dashboard](https://statbot.net/)
- [Tickets bot docs](https://docs.discordtickets.app/)
- [Wick anti-raid](https://wickbot.com/)
