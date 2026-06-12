<!--
Sources: https://orbit.love/blog/the-orbit-model/ + https://www.commonroom.io/blog/community-engagement-funnel/ + https://docs.commonroom.io/api/
-->
# Member Journey — Lurker to Ambassador — SKILL

Funnel: Lurker → Reader → Reactor → Commenter → Contributor → Connector → Ambassador → Champion. Activation playbook per tier: nudge prompts, role unlocks, recognition, rewards. Common Room activity score → stage assignment → fired nudge via Discord DM / Slack DM / Circle post / email. Weekly stage-migration report.

## When to use

- Existing community with high join volume but low engagement (lurker problem).
- Need to design intentional progression — not random.
- Engagement plateauing — many readers but few contributors.
- Building ambassador funnel (this is the upstream of `ambassador-program-design`).
- Member retention dropping at a specific stage — need to diagnose where they fall off.
- Quarterly engagement review — want stage-migration KPI.

Trigger phrases: "member journey", "lurker to ambassador", "engagement funnel", "Orbit model", "journey stage", "nudge", "activation playbook".

## Setup

```bash
# Common Room — activity score
curl -H "Authorization: Bearer $COMMON_ROOM_TOKEN" \
  https://app.commonroom.io/api/v1/members?limit=200

# Postgres — stage assignment + migration tracking
psql -c "CREATE TABLE member_stage_history (member_id TEXT, stage TEXT, assigned_at TIMESTAMP DEFAULT NOW());"

# Discord / Slack nudge channels
mcp tool discord-mcp-full.send_dm --user_id $UID --content "..."
mcp tool slack.chat_postMessage --channel $DM_CH --text "..."
```

Auth + env:
- `COMMON_ROOM_TOKEN` — Common Room API.
- Postgres warehouse for `member_stage_history`.
- `DISCORD_BOT_TOKEN` with `Send Messages` to DMs.
- `SLACK_BOT_TOKEN` with `im:write`.

Workspace prerequisites:
- Postgres tables `community_members`, `community_events`, `member_stage_history`.
- Notion DB `Journey Playbook` with per-stage nudge templates.

## Common recipes

### Recipe 1: 8-stage journey rubric

| Stage | Definition | Trigger to next | Nudge |
|---|---|---|---|
| Lurker | Joined but no activity 7d | First reaction | "Welcome! What brought you here?" |
| Reader | Read 5+ posts 30d, 0 actions | First like/emoji | "Anything you'd like to learn about?" |
| Reactor | 5+ reactions 30d | First reply | "What do you think about [member's recent post]?" |
| Commenter | 1-5 replies 30d | 5+ replies | "Have a question? Ask it; this group's helpful." |
| Contributor | 5+ posts/replies 30d | Help another member | "Your post got 12 reactions — share your story?" |
| Connector | Introduces 2+ members | Public advocacy | "Would you co-host an AMA?" |
| Ambassador | Public advocacy + sustained | Drives external growth | "Quarterly retreat + ambassador kit" |
| Champion | 12mo+ ambassador, drives growth | n/a | Annual all-expenses retreat |

### Recipe 2: Stage assignment SQL

```sql
-- Recompute weekly
INSERT INTO member_stage_history (member_id, stage)
SELECT
  m.member_id,
  CASE
    WHEN MAX(ce.created_at) IS NULL OR MAX(ce.created_at) < NOW() - INTERVAL '7 days' AND COUNT(ce.id) = 0 THEN 'lurker'
    WHEN COUNT(*) FILTER (WHERE ce.event_type='read') >= 5 AND COUNT(*) FILTER (WHERE ce.event_type IN ('reaction','reply','post')) = 0 THEN 'reader'
    WHEN COUNT(*) FILTER (WHERE ce.event_type='reaction') >= 5 AND COUNT(*) FILTER (WHERE ce.event_type IN ('reply','post')) = 0 THEN 'reactor'
    WHEN COUNT(*) FILTER (WHERE ce.event_type='reply') BETWEEN 1 AND 4 THEN 'commenter'
    WHEN COUNT(*) FILTER (WHERE ce.event_type IN ('reply','post')) >= 5 THEN 'contributor'
    WHEN COUNT(*) FILTER (WHERE ce.event_type='intro_member') >= 2 THEN 'connector'
    WHEN COUNT(*) FILTER (WHERE ce.event_type='public_advocacy') >= 3 THEN 'ambassador'
    ELSE 'lurker'
  END AS stage
FROM community_members m
LEFT JOIN community_events ce ON ce.member_id = m.member_id
  AND ce.created_at > NOW() - INTERVAL '30 days'
GROUP BY m.member_id;
```

### Recipe 3: Per-stage nudge templates (Notion DB)

```bash
mcp tool notion.create_page --parent_id $JOURNEY_PLAYBOOK \
  --properties '{
    "Stage": "Lurker",
    "Trigger": "joined 7d ago, 0 activity",
    "Channel": "DM",
    "Message": "Hey {{name}} — welcome! What brought you here?",
    "Cadence": "once at d7"
  }'
```

Repeat for each of 8 stages.

### Recipe 4: Fire stage-transition nudge

```python
# Cron daily
for member in get_members_changed_stage_today():
    template = notion.get_template(member.new_stage)
    msg = template.format(name=member.name, last_post=member.last_post_excerpt)
    if member.platform == 'discord':
        discord_full.send_dm(user_id=member.discord_id, content=msg)
    elif member.platform == 'slack':
        slack.chat_postMessage(channel=member.slack_dm_channel, text=msg)
    else:
        gmail.send(to=member.email, subject=f"Hi {member.name}", body=msg)
    log_nudge_sent(member.id, member.new_stage)
```

### Recipe 5: Stage-migration weekly report

```sql
WITH today AS (
  SELECT member_id, stage FROM member_stage_history WHERE assigned_at > NOW() - INTERVAL '1 day'
),
last_week AS (
  SELECT member_id, stage FROM member_stage_history WHERE assigned_at BETWEEN NOW() - INTERVAL '8 days' AND NOW() - INTERVAL '7 days'
)
SELECT
  lw.stage AS from_stage,
  t.stage AS to_stage,
  COUNT(*) AS members
FROM last_week lw
JOIN today t USING (member_id)
WHERE lw.stage != t.stage
GROUP BY 1, 2 ORDER BY 1, 2;
```

Output table: rows like "reader → reactor: 47 members" = upward; "contributor → reader: 8 members" = downward = risk.

### Recipe 6: Lurker → Reader nudge (Day 7)

```python
LURKER_PROMPT = """
Hey {{name}} — we noticed you joined a week ago but haven't said hi.

Totally cool to lurk! But if you want to dive in:
- What's one challenge on your plate this week?
- Drop it in #general — the group's quick to help.

Or just react 👋 to this and we'll consider you officially welcomed.
"""
```

### Recipe 7: Commenter → Contributor nudge

```python
# Trigger: 3+ replies but 0 original posts
COMMENTER_PROMPT = """
Hey {{name}} — you've been adding great replies in #help. We see you 👀

Want to start your own thread? People sharing problems get faster answers than people lurking.

Idea-starter: what's something you wish more people in this community talked about?
"""
```

### Recipe 8: Connector recognition

```bash
# When a member intros 2+ others, role unlock + public shoutout
mcp tool discord-mcp-full.add_member_role --user_id $UID --role_id $CONNECTOR_ROLE

mcp tool discord-mcp-full.create_message \
  --channel_id $WINS_CH \
  --content "🤝 @$NAME just earned the Connector role for introducing 2+ members. Thank you!"
```

### Recipe 9: Quarterly stage-distribution report

```sql
SELECT
  stage,
  COUNT(*) AS members,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM (
  SELECT DISTINCT ON (member_id) member_id, stage
  FROM member_stage_history
  ORDER BY member_id, assigned_at DESC
) latest
GROUP BY stage ORDER BY array_position(ARRAY['lurker','reader','reactor','commenter','contributor','connector','ambassador','champion'], stage);
```

Healthy distribution (1k member community):
- Lurker 50%
- Reader 25%
- Reactor 10%
- Commenter 8%
- Contributor 5%
- Connector 1.5%
- Ambassador 0.4%
- Champion 0.1%

### Recipe 10: Up-funnel vs down-funnel KPI

```sql
-- Up-funnel rate (good)
SELECT ROUND(100.0 * SUM(CASE WHEN to_stage > from_stage THEN 1 ELSE 0 END) / COUNT(*), 1) AS up_pct
FROM stage_transitions WHERE transition_at > NOW() - INTERVAL '30 days';

-- Down-funnel rate (risk)
SELECT ROUND(100.0 * SUM(CASE WHEN to_stage < from_stage THEN 1 ELSE 0 END) / COUNT(*), 1) AS down_pct
FROM stage_transitions WHERE transition_at > NOW() - INTERVAL '30 days';
```

Target: up_pct > 15%; down_pct < 5%.

## Examples

### Example 1: SaaS Discord — fix the lurker problem

**Goal:** 800-member Discord with 60% never-posted (lurker). Need 25% lurker→reactor migration in 90 days.

**Steps:**
1. Build Recipe 2 stage table.
2. Day 7 lurker nudge (Recipe 6) → expect 10% lift.
3. Reactor nudge with personalized member-post reference (Recipe 1).
4. Connector role unlock at 2 intros (Recipe 8).
5. Quarterly stage report (Recipe 9).

**Result:** Lurker rate 60% → 42% in 90d; contributor count 32 → 81.

### Example 2: Tracking churn at the contributor stage

**Goal:** Diagnose why contributors are dropping to commenter.

**Steps:**
1. Recipe 5 weekly migration report shows 8 contributors→reader downgrades.
2. DM those 8: "Anything we did wrong?"
3. Find: 5 felt their posts went unanswered; 3 burned out.
4. Fix: pin "we'll always reply within 24h" + rotate weekly "feature poster".

**Result:** Contributor-stage retention +20% next quarter.

## Edge cases / gotchas

- **Stage definitions are arbitrary** — pick clean thresholds early; don't refactor mid-quarter (breaks longitudinal data).
- **Stage demotion stigma** — never publicize demotions ("you're a reader again!"). Demotions = internal data only.
- **Read-event tracking is hard** — Discord doesn't expose "user read this message" reliably. Use channel-visit proxy.
- **Common Room stages ≠ this rubric** — Common Room's are CR-defined; if you use both, document the mapping.
- **Nudge fatigue** — 1 nudge / month maximum / member. Otherwise spam.
- **DM blocking** — many users disable DMs; have fallback channel-mention nudge.
- **Cohort effects** — members from launch event behave differently from organic-search joiners. Tag at join.
- **Stage = activity ≠ value** — a quiet long-time member who occasionally drops gold > a noisy contributor.
- **Activity attribution across platforms** — same human posting on Discord + GitHub is one journey. Stitch identity first.
- **Connector role gaming** — fake intros (same person under multiple accounts) — verify via account-age + IP.
- **Down-funnel often = vacation** — cross-check before flagging at-risk; pause nudges in summer/holidays.
- **Ambassador stage handoff** — when member reaches ambassador, switch to `ambassador-program-design` playbook + perks.

## Sources

- [Orbit Model](https://orbit.love/blog/the-orbit-model/)
- [Common Room engagement funnel](https://www.commonroom.io/blog/community-engagement-funnel/)
- [Common Room API](https://docs.commonroom.io/api/)
- [Discord create-DM API](https://discord.com/developers/docs/resources/user#create-dm)
- [Slack im.open](https://api.slack.com/methods/conversations.open)
- [Notion API](https://developers.notion.com/)
