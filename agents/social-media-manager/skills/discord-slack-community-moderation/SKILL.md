<!--
Source: https://blog.communityone.io/best-discord-bots/
Carl-bot: https://carl.gg/
MEE6: https://mee6.xyz/
Dyno: https://dyno.gg/
Slack API: https://api.slack.com/
Discord rule pack: role.md "Discord rule pack template"
-->
# Discord + Slack Community Moderation — SKILL

Carl-bot / MEE6 / Dyno deploy YAML rule packs (role.md template). Discord-MCP + Slack-MCP for direct admin actions (ban / role / channel). Spam + raid detection, toxicity threshold 0.8 (Perspective API), link allowlist, onboarding DM flow, mod-log audit channel. For Slack: workspace governance template + channel-purpose enforcement.

## When to use this skill

- **Setting up moderation rules** on Discord / Slack workspace.
- **Anti-raid lockdown** during attack.
- **Onboarding new members** with welcome DM + rule acknowledgment.
- **Toxicity / hate-speech triage** via Perspective API integration.
- **Channel + role architecture** redesign.
- **Auditing mod actions** + escalation handling.

**Do NOT use this skill when:**
- Brand publishing in Discord (announcement channel) — `community-engagement-comments-dms-at-scale`.
- Cross-platform community engagement — that skill covers per-channel reply.

## Setup

### Discord MCPs

```bash
# Two layers
mcp tool discord.authenticate  # basic operations
mcp tool discord_full.authenticate  # bans, audit log, advanced

export DISCORD_BOT_TOKEN="<token>"
export DISCORD_GUILD_ID="<guild_id>"
```

### Carl-bot

Invite via OAuth: `https://carl.gg/invite`. Required permissions: Manage Roles, Manage Channels, Manage Messages, Ban Members, Read Audit Log, View Channels, Send Messages, Embed Links, Attach Files.

### MEE6

Invite: `https://mee6.xyz/invite`. Premium features ($11.95/mo) unlock advanced moderation.

### Dyno

Invite: `https://dyno.gg/invite`. Premium $$7.99/mo for analytics + advanced auto-mod.

### Slack MCP

```bash
mcp tool slack.authenticate  # OAuth bot token
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_WORKSPACE_ID="T<id>"
```

### Perspective API (toxicity scoring)

```bash
export PERSPECTIVE_API_KEY="<key>"
# Endpoint: https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze
```

### Notion Moderation DB

Columns: `Event ID / Server / Channel / User ID / Type (spam/toxicity/raid/link/manual) / Severity / Action taken / Mod / Timestamp / Resolution`.

## Common recipes

### Recipe 1: Carl-bot YAML rule pack deploy

Per role.md "Discord rule pack template":

```yaml
# carl-bot-rules.yml — paste into Carl-bot dashboard or invoke via:
moderation:
  spam_detection:
    enabled: true
    threshold: 5_messages_per_10_seconds
    action: timeout_10min

  link_policy:
    block_unverified_urls: true
    allowlist:
      - youtube.com/@brand
      - twitch.tv/brand
      - brand.com
      - github.com/brand
    action_on_violation: delete + warn

  toxicity:
    enabled: true
    threshold: 0.8
    action: timeout_24h + mod_log

  raid_protection:
    enabled: true
    new_account_age_min: 7d
    join_velocity_threshold: 10_per_minute
    action: lockdown + mod_alert

onboarding:
  welcome_dm: |
    Welcome to the [brand] community!
    Please read #rules and introduce yourself in #welcome.
    Pick your roles in #roles.
  rules_acknowledge_required: true
  intro_channel_ping: true

engagement:
  daily_question_post: true
  weekly_recap: true
  ama_scheduler: true

mod_log_channel: "#mod-logs"
```

Deploy via cli-anything:

```bash
cli-anything curl -X POST https://carl.gg/api/v1/automod/<guild_id>/rules \
  -H "Authorization: Bearer $CARL_API_TOKEN" \
  --data-binary @carl-bot-rules.yml
```

(Carl-bot dashboard offers YAML import; API may be Premium-tier only — fall to dashboard if not.)

### Recipe 2: Discord raid lockdown

```bash
# Disable verification level escalation if attack detected
mcp tool discord_full.set_verification_level --guild_id "$DISCORD_GUILD_ID" --level "HIGH"

# Slowmode all public channels
for ch in $PUBLIC_CHANNELS; do
  mcp tool discord_full.set_slowmode --channel_id "$ch" --seconds 60
done

# Ban join velocity > threshold
mcp tool discord_full.set_join_gate --guild_id "$DISCORD_GUILD_ID" --action "kick" --threshold 10
```

### Recipe 3: Toxicity check (Perspective API)

```bash
curl -X POST "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=$PERSPECTIVE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "comment": {"text": "<message_text>"},
    "languages": ["en"],
    "requestedAttributes": {"TOXICITY":{}, "SEVERE_TOXICITY":{}, "INSULT":{}, "THREAT":{}}
  }'
# Returns: attributeScores.TOXICITY.summaryScore.value 0..1
```

Pipeline: every message → Perspective → if > 0.8, Discord MCP `timeout_member`.

### Recipe 4: Discord ban / kick / role action

```bash
# Ban
mcp tool discord_full.ban_member \
  --guild_id "$DISCORD_GUILD_ID" \
  --user_id "<uid>" \
  --reason "toxicity x3 — see mod-log" \
  --delete_message_days 1

# Timeout (10 min)
mcp tool discord_full.timeout_member \
  --guild_id "$DISCORD_GUILD_ID" \
  --user_id "<uid>" \
  --duration_seconds 600

# Add / remove role
mcp tool discord_full.add_role \
  --guild_id "$DISCORD_GUILD_ID" \
  --user_id "<uid>" \
  --role_id "<role>"
```

### Recipe 5: Welcome DM + rule acknowledge

```python
# On member_join event
@discord_event('on_member_join')
def welcome(member):
    mcp.discord.send_dm(user_id=member['id'], message=WELCOME_TEMPLATE.format(name=member['name']))
    mcp.discord.add_role(member['id'], role_id=ROLE_UNVERIFIED)
    # User must react with ✅ in #rules to unlock community
```

### Recipe 6: Slack channel governance

```python
# Audit channel purposes vs spec
expected = {
    'general':       'Brand-wide announcements only',
    'community':     'Open community chat',
    'introductions': 'New-member intros',
    'feedback':      'Product feedback to team',
    'off-topic':     'Non-brand chat'
}
channels = mcp.slack.list_channels()
for ch in channels:
    if ch['name'] in expected and ch['purpose'] != expected[ch['name']]:
        mcp.slack.update_channel(ch['id'], purpose=expected[ch['name']])
```

### Recipe 7: Slack auto-thank intros

```python
# When user posts in #introductions, auto-add :wave: reaction + thank reply
@slack_event('message.channels')
def auto_intro(event):
    if event['channel'] == INTRO_CHANNEL_ID:
        mcp.slack.add_reaction(channel=event['channel'], timestamp=event['ts'], reaction='wave')
        mcp.slack.post_thread(channel=event['channel'], thread_ts=event['ts'],
                              text=f"Welcome, <@{event['user']}>! Drop a 👋 in #community when ready.")
```

### Recipe 8: Slack link allowlist

```python
ALLOWLIST = ['brand.com', 'github.com/brand', 'docs.brand.com']
@slack_event('message.channels')
def link_check(event):
    urls = extract_urls(event['text'])
    for u in urls:
        if not any(allowed in u for allowed in ALLOWLIST):
            mcp.slack.delete_message(channel=event['channel'], ts=event['ts'])
            mcp.slack.post_ephemeral(user=event['user'], channel=event['channel'],
                                     text="Link removed: please use allowlist domains.")
```

### Recipe 9: Mod-log audit

```python
# Every mod action logs to Notion + #mod-logs
def log_mod_action(server, channel, user_id, action_type, severity, mod, resolution=None):
    notion.create(mod_db, {
        'Server': server, 'Channel': channel, 'User ID': user_id,
        'Type': action_type, 'Severity': severity, 'Mod': mod,
        'Timestamp': now(), 'Resolution': resolution or 'pending'
    })
    mcp.discord.send_message(channel='#mod-logs',
        text=f"[{severity}] {mod} → {action_type} on <@{user_id}> in #{channel}")
```

### Recipe 10: Daily engagement metrics

```python
# Per-server daily report
metrics = {
    'new_joins': mcp.discord.get_member_growth_24h(guild_id),
    'active_users': mcp.discord.get_active_count_24h(guild_id),
    'messages': mcp.discord.get_message_count_24h(guild_id),
    'mod_actions': len(notion.query(mod_db, filter={'Timestamp__gte': yesterday})),
    'top_channels': mcp.discord.get_top_channels(guild_id, period='24h', limit=3),
}
mcp.discord.send_message('#admin-daily', format_metrics_report(metrics))
```

## Examples

### Example A: Discord launch-day raid response

```yaml
event: 50+ accounts joined in 2 min, posting same link
detection: Carl-bot raid_protection triggered
auto_action:
  - lockdown server (set verification to HIGH)
  - kick all accounts with account_age < 24h
  - send mod-alert ping
manual_followup:
  - mods review raid logs in #mod-logs
  - ban velocity-rule-violators permanently
  - cooldown verification 6 hrs then lift to NORMAL
```

### Example B: Toxicity-strike workflow

```yaml
violation_1:
  perspective_score: 0.82
  action: timeout 10 min + DM warning
violation_2_within_30d:
  perspective_score: 0.85
  action: timeout 24 hr + DM final warning
violation_3:
  any score > 0.8
  action: ban + cross-post to other servers in admin federation
```

### Example C: Slack quarterly health check

```yaml
quarterly_audit:
  - channel purposes correct? (Recipe 6)
  - active members count + growth %
  - intro-channel response rate (warm community signal)
  - mod-action count + categories (escalation trends)
  - off-topic ratio in non-off-topic channels (flag noise)
  - bot health: all integrations responding < 24 hr response
```

## Edge cases

### Carl-bot vs MEE6 vs Dyno feature parity
- Carl-bot strongest for granular YAML rules + reaction roles
- MEE6 strongest for leveling + auto-moderation Premium
- Dyno strongest for moderation primitives + analytics

Pick one as primary; second as fallback for missing feature. Don't run all 3 — duplicate action firing.

### Perspective API rate limits
1 QPS default, raise via Google Cloud quota request. For 100+ messages/sec channel, batch or run secondary classifier.

### Toxicity language coverage
Perspective: English, Spanish, French, German, Portuguese, Italian, Polish, Dutch, Indonesian, Russian. For other languages (Mandarin / Japanese / Arabic), fall to OpenAI/Claude moderation API or per-language model.

### False positives on slang
"Sick!" / "killer!" / "savage!" often score high. Tune threshold per community vocabulary. Brand voice doc should list community-specific allowed terms.

### Discord rate limits
50 messages / 5 sec per channel per bot. For mass DM (welcome wave), throttle and queue.

### Mass-DM trips Discord spam-detection
Welcome DMs to bulk new joiners get bot banned. Use per-server welcome message in dedicated channel instead, OR throttle DMs to 1/sec.

### Slack workspace tier
Free plan: 10k message history, basic bot integrations. Pro $7.25/user/mo: unlimited history + premium bot features. Bot scope matters more than plan for governance.

### Slack workspace bot count limit
Free plan limits installed apps. Audit + uninstall unused before adding new ones.

### Mod team coordination
Multiple mods can step on each other (one bans, another un-bans). Mod-log audit channel + clear ownership matrix (per-server).

### Ban appeals
Brand needs a process. Suggested: Notion form linked from ban DM. Auto-create review ticket. SLA: 7 days to respond.

### GDPR data on banned users
Storing user IDs + ban reasons constitutes data processing. Document retention period (suggest 365 days), data export on user request.

### Cross-platform offender federation
Multi-server admin federations share bad-actor lists. Tools: Discord Trust & Safety + 3rd-party ferret lists. Use with care; false positives blanket-ban innocent users.

### Bot account compromise
If bot token leaks, attacker has god-mode. Rotate immediately, audit log, revoke compromised invite.

### Onboarding drop-off
Welcome DM + rule acknowledge: ~40% completion rate. Don't gate community access too aggressively or lose new members. Iterate on flow length.

### Toxic-stream desensitization
Mods burn out on toxic-message firehose. Rotate mod schedules; pair mods; auto-escalate `severity: critical` only to humans.

## Sources

- **Best Discord moderation bots 2026 (CommunityOne)**: https://blog.communityone.io/best-discord-bots/
- **Carl-bot**: https://carl.gg/
- **MEE6 (21M+ servers)**: https://mee6.xyz/
- **Dyno**: https://dyno.gg/
- **Discord API**: https://discord.com/developers/docs/
- **Slack API**: https://api.slack.com/
- **Perspective API (toxicity)**: https://perspectiveapi.com/
- **Discord rate limits**: https://discord.com/developers/docs/topics/rate-limits
- **Moderator.fm cross-platform mod**: https://moderator.fm/
- **Role.md "Discord rule pack template" + "Slack rule pack template"**
