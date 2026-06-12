<!--
Sources: https://www.commonroom.io/use-cases/find-advocates/ + https://socialladder.tech/ + https://www.mavrck.co/ + https://bevy.com/ + https://roster.media/
-->
# Ambassador Program Design — SKILL

Tier structure (Member → Contributor → Ambassador → Champion) with criteria + perks per tier. Common Room / Insider Notable for candidate identification. Ambassador-platform: Mavrck / Bevy Ambassadors / SocialLadder / Roster (enterprise) or HubSpot custom property + Notion (lean). Perks: early access + swag + co-branding + revenue share.

## When to use

- Community has 500+ active members but no formal advocate program.
- Top-of-funnel growth has plateaued — need member-led marketing.
- Existing power-users helping for free; risk of burnout / leaving.
- B2B SaaS hitting community-led growth chapter — formal ambassadors lift TOFU 20-40%.
- Web3 / DAO community formalizing contributor tiers.
- Pre-launch: building an army of beta-evangelists.

Trigger phrases: "ambassador program", "champion program", "advocate program", "MVP program", "community evangelist", "Notion Champions", "Figma Friends".

## Setup

```bash
# Common Room — identify candidates (paid)
curl -H "Authorization: Bearer $COMMON_ROOM_TOKEN" \
  "https://app.commonroom.io/api/v1/segments/$ADVOCATE_SEGMENT/members"

# HubSpot custom property — fallback (free)
curl -H "Authorization: Bearer $HUBSPOT_TOKEN" \
  -X POST https://api.hubapi.com/properties/v1/contacts/properties \
  -d '{"name":"ambassador_tier","label":"Ambassador tier","type":"enumeration","options":[{"label":"Member","value":"member"},{"label":"Contributor","value":"contributor"},{"label":"Ambassador","value":"ambassador"},{"label":"Champion","value":"champion"}]}'

# Notion ambassador DB
mcp tool notion.create_database --parent_id $COMM_PAGE \
  --title "Ambassador Program" \
  --properties '{"Name":{"title":{}},"Tier":{"select":{}},"Email":{"email":{}},"Activities":{"number":{}},"Perks unlocked":{"multi_select":{}},"Renewal":{"date":{}}}'

# Outreach via gmail-mcp
mcp tool gmail.drafts_create --to candidate@example.com --subject "..."
```

Auth + env:
- `COMMON_ROOM_TOKEN` — Settings → API. Paid Starter+ tier.
- `HUBSPOT_TOKEN` — Private app token.
- `SOCIALLADDER_API_KEY` or `MAVRCK_API_KEY` — paid enterprise.

## Common recipes

### Recipe 1: Tier rubric

| Tier | Criteria | Perks | Identification signal |
|---|---|---|---|
| Member | Joined | Access | Default |
| Contributor | 10+ posts in 90d, 1+ helpful answer | Early access to features, Discord role badge | Common Room activity score 50+ |
| Ambassador | 30+ posts in 90d, sustained help, public advocacy | Quarterly swag, beta features, founder access, $50/mo stipend (optional) | Common Room score 80+, GitHub stars, social mentions |
| Champion | 12mo+ ambassador, drives external growth, conference speaker | Annual all-expenses retreat, co-branded content, revenue share, advisory equity | Manual nomination + activity verification |

### Recipe 2: Common Room candidate-finder

```bash
# Top contributors in last 90 days
curl -H "Authorization: Bearer $COMMON_ROOM_TOKEN" \
  "https://app.commonroom.io/api/v1/members?segment=top-contributors-90d&limit=50" \
  | jq -r '.results[] | {id, name, email, score, activities: .activity_count}'
```

Filter:
- Activity score ≥80 (Ambassador candidate).
- Positive sentiment in recent posts.
- Not currently employed by competitor (LinkedIn cross-check via `linkedin-mcp`).
- Cross-platform presence (helpful both Discord + GitHub).

### Recipe 3: Lean fallback — Postgres + scoring

```sql
-- If no Common Room, build activity score in warehouse
CREATE TABLE member_activity AS
SELECT
  user_id,
  COUNT(*) FILTER (WHERE platform='discord' AND created_at > NOW() - INTERVAL '90 days') AS discord_posts,
  COUNT(*) FILTER (WHERE platform='github' AND event='issue_comment' AND created_at > NOW() - INTERVAL '90 days') AS gh_comments,
  COUNT(*) FILTER (WHERE platform='discord' AND helpful_react > 0) AS helpful_answers,
  COUNT(DISTINCT platform) AS platform_breadth
FROM community_events GROUP BY user_id;

-- Composite score
SELECT user_id,
  (discord_posts * 1 + gh_comments * 2 + helpful_answers * 5 + platform_breadth * 10) AS score
FROM member_activity
ORDER BY score DESC LIMIT 50;
```

### Recipe 4: Nomination form (Notion DB)

```bash
mcp tool notion.create_page \
  --parent_id $AMBASSADOR_DB \
  --properties '{
    "Name": "Jane Doe",
    "Tier": "Ambassador (proposed)",
    "Nominator": "@founder",
    "Reason": "Posts 4x/week, answered 35 support qs in 60d, hosted last 2 AMAs",
    "Status": "Pending review"
  }'
```

Weekly mod-team review of nominations.

### Recipe 5: Ambassador outreach email

```bash
mcp tool gmail.drafts_create \
  --to jane@example.com \
  --subject "An invitation — $COMMUNITY Ambassador program" \
  --body "
Hey Jane,

Over the past few months, you've shown up in $COMMUNITY in a way that's frankly setting the standard — your answers in #help saved dozens of new members, and your AMAs blew us away.

We're formalizing an Ambassador program. You're one of the first 5 people we want to invite.

Perks:
- Quarterly swag drop (next box ships in 2 weeks)
- Beta access to upcoming features (NDA but real preview)
- Monthly 30min sync with the founders
- Dedicated 'Ambassador' Discord role + private channel
- (Optional) $50/mo stipend in exchange for ~4 hours/mo of program work

If you're in: reply YES + your t-shirt size. Onboarding doc attached.

— $FOUNDER_NAME
"
```

### Recipe 6: Onboarding doc (Ambassador kit)

```markdown
# Ambassador Onboarding Kit

## What we ask of you (4h/month)
- 1 community AMA / month
- 1 piece of public content (blog / video / tweet) / quarter
- Respond to flagged help tickets in your timezone
- Provide feedback on betas before launch

## What you get
- Quarterly swag box (next ships $DATE)
- Beta program access — feature branch + #ambassador-beta Discord
- Co-branded content opportunities — we'll amplify
- Founder office hours — monthly 30min open Zoom
- Stipend — $50/mo via Stripe (if accepted)

## NDA + IP
[Standard NDA template — see /legal/nda.pdf]
- You may share publicly anything in the #public-roadmap channel
- No unannounced features in public until the launch date

## Renewal cycle
- Annual review every $DATE
- Re-up: based on activity + retained NPS
- Off-ramp: graceful — keep role + swag, lose stipend
```

### Recipe 7: Discord role + private channel

```bash
# Create role
ROLE_ID=$(mcp tool discord-mcp-full.create_role \
  --guild_id $GUILD_ID --name "Ambassador" --color 0xFFD700 --hoist true \
  | jq -r '.id')

# Assign
mcp tool discord-mcp-full.add_member_role \
  --guild_id $GUILD_ID --user_id $USER_ID --role_id $ROLE_ID

# Private channel
mcp tool discord-mcp-full.create_channel \
  --guild_id $GUILD_ID --name "ambassadors-only" --type 0 \
  --permission_overwrites "[{\"id\":\"$ROLE_ID\",\"type\":0,\"allow\":\"3072\"},{\"id\":\"$GUILD_ID\",\"type\":0,\"deny\":\"1024\"}]"
```

### Recipe 8: Quarterly swag trigger

```bash
# Reachdesk: trigger shipment on Ambassador tier
curl -X POST -H "Authorization: Bearer $REACHDESK_TOKEN" \
  https://api.reachdesk.com/v1/campaigns/$AMBASSADOR_KIT/recipients \
  -d "{\"email\":\"$EMAIL\",\"shipping_address\":\"$ADDRESS\"}"

# Manual fallback: Printful order via API
curl -X POST -H "Authorization: Bearer $PRINTFUL_TOKEN" \
  https://api.printful.com/orders \
  -d "@order.json"
```

### Recipe 9: Activity dashboard (Metabase / Looker)

```sql
-- Ambassador-tier monthly health
SELECT
  ambassador.name,
  ambassador.tier,
  COUNT(act.id) FILTER (WHERE act.kind='post' AND act.created_at > NOW() - INTERVAL '30 days') AS posts_30d,
  COUNT(act.id) FILTER (WHERE act.kind='help_answer') AS help_answers_30d,
  COUNT(act.id) FILTER (WHERE act.kind='public_advocacy') AS public_30d,
  MAX(act.created_at) AS last_activity
FROM ambassadors a
LEFT JOIN community_activity act ON act.member_id = a.member_id
GROUP BY ambassador.name, ambassador.tier
HAVING COUNT(act.id) FILTER (WHERE act.created_at > NOW() - INTERVAL '30 days') < 4
ORDER BY last_activity ASC;
-- Low-activity ambassadors = at-risk for off-ramp
```

### Recipe 10: Annual renewal flow

```python
# Annual: every ambassador gets a survey + renewal interview
for amb in list_ambassadors_due():
  send_renewal_survey(amb.email)
  schedule_30min_call(amb.email, founder_calendar)
  # Decision: continue / off-ramp / promote to Champion
  if amb.activity_30d < 4 and amb.nps < 7:
    off_ramp(amb)
  elif amb.activity_30d > 20 and amb.public_advocacy_count > 5:
    promote_to_champion(amb)
```

## Examples

### Example 1: SaaS — 50 ambassadors from 2k members

**Goal:** Build Ambassador tier from existing 2k Slack/Discord community.

**Steps:**
1. Tier rubric (Recipe 1).
2. Common Room candidate query (Recipe 2) → 75 candidates.
3. Mod team review → 50 invite.
4. Outreach emails (Recipe 5).
5. Onboard 35 (70% acceptance).
6. Discord role + private channel (Recipe 7).
7. Quarterly Reachdesk swag (Recipe 8).

**Result:** Ambassadors drive 40% of help-answers, 8 became Champions in 12mo.

### Example 2: Lean — solopreneur with 300-member Discord

**Goal:** No Common Room budget; identify advocates manually.

**Steps:**
1. Postgres scoring (Recipe 3) from Discord export.
2. Pick top 10 by score.
3. Manual outreach (Recipe 5).
4. Notion DB tracking (Recipe 4).
5. Printful merch quarterly (Recipe 8).

**Result:** 7 of 10 accept; 4 stay active 12mo; community NPS +15.

## Edge cases / gotchas

- **Paid stipend complicates** — IRS 1099 reporting >$600/yr; many programs avoid stipend, use swag + access instead.
- **Cross-employer NDA conflicts** — ambassador's employer may forbid; clarify before NDA.
- **Champion → employee pipeline risk** — Top Champions get hired; ambassador role is often a recruiting funnel. Be transparent.
- **Over-perking** — too generous = mercenary energy. Lean on access + belonging, not just stuff.
- **Burnout signal** — Ambassador activity decay >50% MoM = check in, don't auto-off-ramp.
- **Geographic equity** — global community = global swag-shipping cost; Reachdesk handles, manual Printful doesn't.
- **AI-generated ambassador content** — require human authorship for advocacy posts; AI-written endorsements feel hollow.
- **Power imbalance** — Champions feel they're "doing your job for free". Acknowledge this; pay or rotate.
- **Off-ramp grace** — never cold-cut an ambassador; let role persist for 3 months as goodbye.
- **Common Room paywall** — Starter $X/mo; lean teams can build scoring DIY in Postgres for free.
- **NDA enforcement** — leak risk is real; tier 4 → permanent removal + recovery email.

## Sources

- [Common Room — find advocates](https://www.commonroom.io/use-cases/find-advocates/)
- [SocialLadder](https://socialladder.tech/)
- [Mavrck](https://www.mavrck.co/)
- [Bevy ambassador program](https://bevy.com/products/community-led-events-platform)
- [Roster](https://roster.media/)
- [Reachdesk API](https://www.reachdesk.com/integrations)
- [HubSpot custom properties](https://developers.hubspot.com/docs/api/crm/properties)
