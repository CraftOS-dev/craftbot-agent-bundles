<!--
Source: https://buffer.com/developers/api
Account-takeover playbook: role.md "Account takeover playbook" reference
Buffer dual-publisher approval flow
-->
# Account Takeovers — Creator Handoff — SKILL

Documented playbook for handing brand account to a guest creator: briefing doc + posting schedule + voice guidelines + approval flow + safety net. Channel-handoff via temporary access tokens. Buffer `createUpdate({needsApproval: true})` for dual-publisher review. Revocation script post-takeover. Common formats: 24-hr account takeover, "guest week" series, exec-led week, creator-co-host AMA.

## When to use this skill

- **Guest creator runs brand account for 24-48 hrs or a week**.
- **Executive (CEO / founder) takeover series** of company channel.
- **Customer-takeover** as testimonial / advocacy program.
- **Cross-brand swap** (partner brand runs each other's account for a day).

**Do NOT use this skill when:**
- Creator just publishes one sponsored post — `influencer-outreach-modash-aspire-grin`.
- Internal employee posting under personal advocacy — `team-admin-coordination`.

## Setup

### Buffer with approval workflow

```bash
export BUFFER_ACCESS_TOKEN="<pat>"
export BUFFER_ORGANIZATION_ID="<org-uuid>"
# Team / Agency plan required for approval flow
```

### Notion Takeover Brief DB

Columns: `Takeover ID / Creator handle / Brand channels (multi-select) / Start date / End date / Approval flow (auto/pre-review) / Voice guidelines link / Off-limits topics / Approved hashtag set / Crisis-contact name / Status (draft/active/closed) / Token revoked? / Post count / Reach / Engagement / Follower delta`.

### Token rotation pre-built script

```bash
# scripts/revoke-takeover-tokens.sh
#!/bin/bash
# Revoke after takeover ends
mcp tool buffer.remove_user --user_id "$CREATOR_USER_ID"
mcp tool buffer.regenerate_org_token --reason "post-takeover rotation"
```

### Native MCP per-platform token revoke

```bash
# Per platform, audit access
mcp tool insta_business.list_active_tokens
mcp tool twitter.list_authorized_apps
mcp tool tiktok.list_seller_tokens
# Revoke as needed
```

## Common recipes

### Recipe 1: Pre-takeover briefing doc (Notion)

Template (per role.md influencer brief + this specialization):

```markdown
# Brand Takeover Brief — @creator_handle

## Window
- Start: 2026-06-20 09:00 ET
- End:   2026-06-22 21:00 ET
- Total: 60 hrs

## Channels
- Instagram (Feed + Stories + Reels)
- TikTok
- Threads
- LinkedIn company (executive co-sign required)

## Posting cadence
- IG Stories: 3-5 frames/day
- IG Feed/Reels: 2 posts/day
- TikTok: 2-3 videos/day
- Threads: 5-8 posts/day
- LinkedIn: 1 post (executive review required)

## Brand voice
- See `styles/Brand/<Platform>.yml` per channel
- Tone: [3 adjectives] e.g. "candid, curious, technical"
- Off-limits topics: competitor names, pricing, roadmap details, internal HR
- Voice latitude: creator can riff; keep brand-safe and FTC-compliant

## Approval flow
- Tier 1 (Stories, X replies, comment engagement): auto-publish, post-review
- Tier 2 (Feed posts, Reels, TikTok): pre-publish review via Buffer needsApproval
- Tier 3 (LinkedIn company, anything controversial): executive sign-off required

## Crisis contact
- Primary: @comms-lead (Slack)
- Secondary: @social-team-lead (Slack)
- After hours: <phone>

## Hashtag basket
- Required campaign tag: #BrandCreatorWeek
- Branded: #BrandX
- Niche: <per role.md hashtag basket spec>
- Disclosure: #ad / #sponsored mandatory

## Performance targets
- Reach baseline + 30%
- Engagement rate baseline + 50%
- Follower delta: 1-3% gain
- Post count: 15-20 over window
```

### Recipe 2: Tier-based Buffer approval

```bash
# Tier 1 — auto-publish (e.g. Stories, replies)
mcp tool buffer.create_update \
  --channelIds '["instagram"]' \
  --text "Today's update from @creator..." \
  --needsApproval false

# Tier 2 — pre-publish review
mcp tool buffer.create_update \
  --channelIds '["instagram_reels","tiktok"]' \
  --text "Behind-the-scenes Reel" \
  --mediaUrls '["https://..."]' \
  --needsApproval true \
  --assignedReviewer "social-team-lead"

# Tier 3 — executive
mcp tool buffer.create_update \
  --channelIds '["linkedin_company"]' \
  --text "From @creator with @ceo's intro..." \
  --needsApproval true \
  --assignedReviewer "ceo"
```

### Recipe 3: Token-scoped access (Buffer team workspaces)

```bash
# Add creator as Buffer team member with limited permissions
curl -X POST https://graph.buffer.com/v1 \
  -H "Authorization: Bearer $BUFFER_ACCESS_TOKEN" \
  -d '{
    "query":"mutation { inviteUser(input: {email: \"creator@email.com\", role: \"AUTHOR\", channelIds: [\"chan_ig\",\"chan_tiktok\",\"chan_threads\"]}) { id } }"
  }'
```

`AUTHOR` role: can draft + submit for approval; can't publish directly or modify settings.

### Recipe 4: Platform-native token sharing (no Buffer)

When creator needs platform-native features Buffer doesn't expose:

```bash
# IG: invite as collaborator (limited posting access without password share)
mcp tool insta_business.add_collaborator \
  --account_id "$IG_BUSINESS_ID" \
  --collaborator_handle "$CREATOR_HANDLE" \
  --role "Content Creator"

# TikTok: Creator Marketplace partnership (no token share; creator posts via Buy)
# X: temporary post-publish access via Teams (Premium)
# LinkedIn: add as company-page admin (requires existing employment relationship)
```

### Recipe 5: Daily content review checkpoint

```python
# Each morning of takeover, review yesterday's posts
yesterday = date.today() - timedelta(days=1)
posts = mcp.buffer.get_published_updates(creator_user_id=CREATOR_USER_ID, since=yesterday)
for p in posts:
    perf = mcp.buffer.get_update_analytics(p['id'])
    notion.upsert(takeover_post_db, {
        'Post ID': p['id'], 'Platform': p['channel'], 'Text': p['text'],
        'Reach': perf['reach'], 'Engagement': perf['engagement'],
        'Vale errors': vale_check(p['text']),
        'Brand-voice flag': perf.get('voice_drift_flag'),
        'Approval status': 'auto-approved' if not p['needsApproval'] else 'review'
    })

# Slack daily summary
slack.post('#takeover-watch', daily_summary(notion.query(takeover_post_db, filter={'Date': yesterday})))
```

### Recipe 6: Crisis-trigger flag during takeover

```python
# Brand24 webhook auto-elevates to takeover-watch tier
@webhook_handler('/takeover-crisis')
def on_takeover_crisis(payload):
    if active_takeover_running():
        slack.post('#takeover-watch', f"""🚨 ALERT during takeover by @{CREATOR_HANDLE}
Trigger: {payload['condition']}
Reach: {payload['cluster_reach']}
Immediate action: pause creator publishing access pending review.""")
        # Pause Buffer publishing
        mcp.buffer.pause_user(CREATOR_USER_ID)
```

### Recipe 7: Takeover-end revocation script

```bash
#!/bin/bash
TAKEOVER_ID="$1"

# 1. Revoke Buffer access
mcp tool buffer.remove_user --user_id "$CREATOR_USER_ID"

# 2. Revoke platform-native tokens
mcp tool insta_business.remove_collaborator --handle "$CREATOR_HANDLE"
# X / TikTok / LinkedIn: per platform

# 3. Audit log
mcp tool buffer.get_audit_log --since "$TAKEOVER_START" > audit-$TAKEOVER_ID.log

# 4. Update Notion
mcp tool notion.update_page --id "$NOTION_TAKEOVER_PAGE_ID" \
  --properties '{"Status":"closed","Token revoked?":true,"End date":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}'

# 5. Slack confirmation
slack post '#takeover-watch' "Takeover $TAKEOVER_ID closed. Tokens revoked. Audit log: <s3-link>"

# 6. Send thank-you DM to creator
mcp tool gmail.send --to "$CREATOR_EMAIL" --subject "Thank you" --body "$THANK_YOU_TEMPLATE"
```

### Recipe 8: Performance retrospective

```python
def takeover_retro(takeover_id):
    t = notion.get(takeover_db, takeover_id)
    posts = notion.query(takeover_post_db, filter={'Takeover ID': takeover_id})
    
    retro = {
        'Takeover ID': takeover_id,
        'Creator': t['Creator handle'],
        'Duration_hrs': (t['End date'] - t['Start date']).total_seconds() / 3600,
        'Posts shipped': len(posts),
        'Total reach': sum(p['Reach'] for p in posts),
        'Avg engagement rate': mean(p['Engagement'] / max(p['Reach'], 1) for p in posts),
        'Reach vs baseline': sum(p['Reach'] for p in posts) / baseline_reach_period - 1,
        'Follower delta': follower_count_end - follower_count_start,
        'Crisis triggers': len([p for p in posts if p.get('Crisis flag')]),
        'Brand-voice flags': len([p for p in posts if p.get('Brand-voice flag')]),
        'Recommendation': retro_recommendation(t, posts)
    }
    notion.create(takeover_retro_db, retro)
    slack.post('#leadership', format_retro(retro))
```

### Recipe 9: Pre-takeover dry-run

```python
# 48 hrs before takeover, test approval flow with creator
test_post = mcp.buffer.create_update(
    channelIds=['internal_test_channel'],  # dummy channel
    text="Dry-run test post — please ignore",
    needsApproval=True,
    assignedReviewer='social-team-lead'
)
# Verify creator can submit, reviewer can approve, post publishes
assert test_post['status'] == 'approved'
```

### Recipe 10: Multi-creator takeover (week-long series)

```yaml
takeover_series:
  name: "BrandWeek 2026 — 5 voices, 5 days"
  creators:
    - @creator-mon: Monday
    - @creator-tue: Tuesday
    - @creator-wed: Wednesday
    - @creator-thu: Thursday
    - @creator-fri: Friday
  shared_briefing_doc: <link>
  channels: [IG, TikTok, Threads]
  daily_passing:
    - 8am: incoming creator brief overlap call (15 min)
    - 9am: outgoing creator hands off; incoming starts
    - 11am: first post live
    - 9pm: end-of-day check-in
```

## Examples

### Example A: 48-hr influencer takeover (cooking brand)

```yaml
takeover_id: COOK-TAKEOVER-001
creator: '@chef_amelia'
window: 2026-06-20 09:00 → 2026-06-22 09:00 ET
brief:
  voice: "warm, technical, food-first"
  off_limits: ["competitor brands", "diet politics"]
  hashtag_required: ["#BrandCookWeek", "#ad"]
channels: [IG, TikTok, Threads]
approval_tier:
  - Stories: auto-publish
  - Feed/Reels: review by social-team-lead
  - TikTok: review by social-team-lead
performance_targets:
  reach: +30% vs baseline
  ER: +50% vs baseline
  followers: +1500 net
```

### Example B: Exec series (founder Monday-takeovers)

```yaml
series_name: "Founder Mondays"
cadence: every Monday for Q3 2026 (13 sessions)
duration_per_session: 4 hrs (10am-2pm)
channels: [LinkedIn company, X corporate, Threads]
voice: "candid, founder-energy, no PR-speak"
brief_per_session: founder + comms-lead 30-min prep call
performance_targets:
  - LinkedIn reach +50% on Mondays vs baseline
  - X engagement +75% during window
```

### Example C: Brand-swap (2-day mutual)

```yaml
brand_a_runs_b: 2026-07-10 to 2026-07-12 (BrandA team takes over BrandB IG)
brand_b_runs_a: 2026-07-13 to 2026-07-15 (BrandB team takes over BrandA IG)
co-announce: joint Story announcement T-3 days
hashtag: #BrandSwap2026
revoke_after: scripted Recipe 7 both directions
```

## Edge cases

### Creator goes off-brief
Use brand-voice doc + Vale per-platform packs as published guardrail. If creator drifts, daily review (Recipe 5) catches; reach out via DM to recalibrate. Final option: pause Buffer publishing (Recipe 6).

### Approval-flow backlog
Reviewer offline during creator's posting window → delays. Buffer Team plan allows multiple reviewers. Set 2-3 backup reviewers per tier.

### Sensitive PII in creator posts
Creator may inadvertently expose user data / internal info. Vale rule + manual review for screenshots / DMs / order numbers visible in media.

### FTC disclosure on takeovers
Creator-led brand-account posts ARE sponsored content (even if no payment to creator beyond barter). Must include #ad / #sponsored on every post. Brand bears liability for disclosure.

### Cross-platform handoff timing
IG vs TikTok vs LinkedIn have different optimal post times. Brief should outline per-channel cadence so creator doesn't try to fire-everything-at-once.

### Token-leak risk
Direct password share = fired-on-sight. Never share platform passwords. Use:
- Buffer team workspace (preferred)
- IG Collaborator role (per-account)
- LinkedIn page admin role (requires employment)
- X / TikTok teams feature (Premium)

### Creator account vs brand account
Creator's personal handle may not match brand identity. Pre-agree which voice dominates (recommend brand-voice with creator personality injected).

### Approval-fatigue
Tier-1 + Tier-2 every post = burnout for reviewer. Brief should clarify tier system + delegated authority.

### Performance attribution
Reach lift during takeover may be creator's personal audience pull-in vs brand audience activation. Track which followers stick post-takeover (60-day retention).

### Negative-response cluster
Creator's audience may dislike brand fit. Pre-screen via Modash audience-match. Mid-takeover: if sentiment dips > 30%, end takeover early.

### Algorithm-shift on creator content
Creator's posting may train algorithm to surface different content type post-takeover. Monitor next 30 days; recalibrate cadence.

### Cancellation mid-takeover
Crisis on either side may necessitate early end. Pre-agreed cancellation clause + pro-rated compensation + PR statement template.

### Audit-log for compliance
Regulated industries (finance / healthcare) require full audit log of every post + approver. Recipe 7 step 3 essential.

### Visa / international creator
International creator may have different platform restrictions. Pre-check creator's platform-region access.

### Brand-voice document update
Post-takeover learnings often refine brand voice doc. Schedule recipe-10 retro within 7 days; update brand-voice doc with creator-insights.

## Sources

- **Buffer Developers API (createUpdate / needsApproval)**: https://buffer.com/developers/api
- **Buffer team workspaces + roles**: https://support.buffer.com/article/520-buffer-team-roles
- **Instagram Collaborators**: https://help.instagram.com/268523068844180
- **TikTok Creator Marketplace**: https://creatormarketplace.tiktok.com/
- **FTC sponsored-content rules**: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- **Role.md "Account takeover" playbook**: brief + Buffer approval + revoke tokens
