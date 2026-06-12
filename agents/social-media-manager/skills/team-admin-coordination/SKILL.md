<!--
Source: https://buffer.com/resources/best-social-media-management-tools/
Sprout collision detection: https://sproutsocial.com/insights/social-media-scheduling-tools/
Role.md: governance + multi-admin
-->
# Team Admin Coordination — SKILL

Buffer Team plan with role-based approvals + collision detection + Notion DB row per scheduled post (status: draft / review / approved / scheduled / published) + Slack notifications via `slack-mcp` on state transitions. Sprout / Hootsuite as enterprise upgrades. Regulated-brand workflow with pre-publish approval gate.

## When to use this skill

- **Multi-admin social team** (>2 people scheduling).
- **Approval gate** for regulated industries (finance / healthcare / legal).
- **Editorial calendar with assignees + reviewers**.
- **Cross-team coordination** — social + design + product + executive sign-offs.
- **Audit-log requirements** for compliance.

**Do NOT use this skill when:**
- Solo creator / single admin — overkill.
- One-off post — direct publish, no approval.

## Setup

### Buffer Team plan

```bash
export BUFFER_ACCESS_TOKEN="<owner-token>"
export BUFFER_ORG_ID="<org-uuid>"
# Team plan $12/channel/mo: multi-user + approval flows
# Agency plan: white-label + per-client workspaces
```

### Sprout Social (enterprise)

```bash
export SPROUT_API_KEY="<key>"
export SPROUT_CUSTOMER_ID="<id>"
# Pricing: $249-$499/user/mo
# Collision detection: when two users start replying to same engagement, surface lock
```

### Hootsuite (enterprise)

```bash
export HOOTSUITE_TOKEN="<oauth-token>"
# Team coordination via Streams + assignment
```

### Notion Editorial Calendar DB

Columns: `Post ID / Title / Content / Channels (multi-select) / Format / Scheduled at / Assignee (Person) / Reviewer (Person) / Status (Select) / Approval notes / Buffer ID / Vale status / Published URL / Performance`.

Status options: `Draft / In review / Needs revision / Approved / Scheduled / Published / Failed`.

### Team-role matrix

```yaml
roles:
  owner:
    permissions: all + billing
    members: ['cmo@brand.com']
  editor:
    permissions: create + approve + publish to assigned channels
    members: ['social-lead@brand.com']
  author:
    permissions: create + edit + submit for approval (cannot publish)
    members: ['social-team-1@brand.com', 'social-team-2@brand.com']
  reviewer:
    permissions: approve + reject (cannot create)
    members: ['legal@brand.com', 'product@brand.com']
  viewer:
    permissions: read-only
    members: ['analyst@brand.com']
```

### Slack channels

```
#social-editorial — daily editorial calendar updates
#social-review    — pending approvals
#social-published — publish confirmations
#social-alerts    — SLA breach, failure, crisis
```

## Common recipes

### Recipe 1: Add team member to Buffer

```bash
curl -X POST https://graph.buffer.com/v1 \
  -H "Authorization: Bearer $BUFFER_ACCESS_TOKEN" \
  -d '{
    "query":"mutation { inviteUser(input: {email: \"author@brand.com\", role: \"AUTHOR\", channelIds: [\"chan_ig\",\"chan_x\",\"chan_threads\"]}) { id email role } }"
  }'
```

### Recipe 2: Create draft + assign reviewer

```bash
mcp tool buffer.create_update \
  --channelIds '["linkedin_company","instagram"]' \
  --text "Draft text" \
  --mediaUrls '["..."]' \
  --needsApproval true \
  --assignedReviewer "<reviewer_user_id>" \
  --scheduledAt "2026-06-18T14:00:00Z"

# Mirror in Notion
mcp tool notion.create_page \
  --database "editorial_calendar_db" \
  --properties '{
    "Title":"Summer-drop launch teaser",
    "Status":"In review",
    "Assignee":"social-team-1@brand.com",
    "Reviewer":"social-lead@brand.com",
    "Scheduled at":"2026-06-18T14:00:00Z",
    "Buffer ID":"<update_id>"
  }'

# Notify Slack
mcp tool slack.post_message \
  --channel "#social-review" \
  --text "@social-lead — new post needs review: <link to Notion>"
```

### Recipe 3: Approval action (review side)

```python
@slack_command('/approve')
def approve(post_id, approver_email):
    post = notion.get(editorial_db, post_id)
    if approver_email != post['Reviewer']:
        return slack.respond("Not assigned to you")
    if post['Status'] != 'In review':
        return slack.respond(f"Cannot approve: status is {post['Status']}")
    
    # Buffer approval
    mcp.buffer.approve_update(id=post['Buffer ID'])
    # Notion update
    notion.update(post['id'], {
        'Status': 'Approved',
        'Approval notes': f"Approved by {approver_email} on {now()}",
        'Approved at': now()
    })
    # Slack confirmation
    slack.post('#social-editorial', f"✅ Approved: '{post['Title']}' — scheduled at {post['Scheduled at']}")

@slack_command('/reject')
def reject(post_id, approver_email, reason):
    notion.update(post_id, {
        'Status': 'Needs revision',
        'Approval notes': f"Rejected by {approver_email}: {reason}"
    })
    slack.post('#social-editorial', f"❌ Rejected: '{notion.get(editorial_db, post_id)['Title']}' — {reason}")
```

### Recipe 4: Collision detection (Sprout / Agorapulse pattern)

For shops with Sprout, native. For Buffer-only, simulate via Notion lock:

```python
def claim_engagement(engagement_id, assignee):
    record = notion.query(triage_db, filter={'Engagement ID': engagement_id})[0]
    if record['Claimed by']:
        return f"Already claimed by {record['Claimed by']}"
    notion.update(record['id'], {
        'Claimed by': assignee,
        'Claimed at': now(),
        'Lock expires': now() + 30 * 60  # 30-min auto-release
    })
    return "Claimed"

@scheduled('*/5 * * * *')
def release_stale_locks():
    stale = notion.query(triage_db, filter={'Lock expires__lt': now(), 'Status': 'open'})
    for r in stale:
        notion.update(r['id'], {'Claimed by': None, 'Claimed at': None, 'Lock expires': None})
```

### Recipe 5: Approval-SLA watchdog

```python
@scheduled('0 * * * *')  # hourly
def approval_sla():
    pending = notion.query(editorial_db, filter={'Status': 'In review'})
    for p in pending:
        elapsed_hr = (now() - p['Submitted at']).total_seconds() / 3600
        sla_hr = APPROVAL_SLA.get(p['Tier'], 24)
        if elapsed_hr > sla_hr:
            slack.post('#social-alerts',
                f"⚠ Approval SLA breach: '{p['Title']}' — pending {int(elapsed_hr)} hrs. Reviewer: {p['Reviewer']}")
        elif elapsed_hr > sla_hr * 0.8:
            slack.post('#social-review',
                f"Heads-up: '{p['Title']}' — {int(sla_hr - elapsed_hr)} hrs to SLA breach.")
```

### Recipe 6: Daily editorial calendar standup

```python
@scheduled('0 9 * * 1-5')  # weekday 9am
def daily_standup():
    today_posts = notion.query(editorial_db, filter={'Scheduled at__date': today()})
    tomorrow_posts = notion.query(editorial_db, filter={'Scheduled at__date': tomorrow()})
    
    summary = f"""📋 Editorial standup — {today()}

Today scheduled: {len(today_posts)} ({status_counts(today_posts)})
Tomorrow drafts: {len(tomorrow_posts)} ({status_counts(tomorrow_posts)})

Pending review (>4hr):
{pending_review_summary()}

Vale failures requiring rewrite:
{vale_failures_summary()}
"""
    slack.post('#social-editorial', summary)
```

### Recipe 7: Publish-state transition notifications

```python
@on_buffer_status_change
def status_notify(post):
    notion_record = notion.query(editorial_db, filter={'Buffer ID': post['id']})[0]
    new_status = map_buffer_to_notion_status(post['status'])
    notion.update(notion_record['id'], {'Status': new_status, 'Last updated': now()})
    
    if new_status == 'Published':
        notion.update(notion_record['id'], {
            'Published URL': post['publish_url'],
            'Published at': now()
        })
        slack.post('#social-published', f"✅ Published: '{notion_record['Title']}' — {post['publish_url']}")
    elif new_status == 'Failed':
        slack.post('#social-alerts', f"❌ Publish FAILED: '{notion_record['Title']}' — {post['error']}")
```

### Recipe 8: Per-channel role permissions

```yaml
# In Buffer Team plan, restrict per-channel access by role
linkedin_company:
  authors: [@brand-social-1]
  reviewers: [@cmo, @legal]
  publishers: [@social-lead]

instagram:
  authors: [@brand-social-1, @brand-social-2]
  reviewers: [@social-lead]
  publishers: [@social-lead, @brand-social-1]

tiktok:
  authors: [@brand-social-3]
  reviewers: [@social-lead]
  publishers: [@social-lead]
```

### Recipe 9: Audit log export

```python
# Quarterly: full audit log for compliance
@scheduled('0 0 1 */3 *')  # quarterly
def quarterly_audit():
    actions = mcp.buffer.get_audit_log(since=quarter_start_minus_3_months, until=quarter_start)
    notion_actions = notion.query(editorial_db, filter={'Last updated__gte': quarter_start_minus_3_months})
    
    audit = {
        'Quarter': previous_quarter_label(),
        'Total posts published': len([a for a in actions if a['action']=='publish']),
        'Approval cycles': len([a for a in actions if a['action']=='approve_or_reject']),
        'Failed publishes': len([a for a in actions if a['action']=='publish' and a['status']=='failed']),
        'Approval-SLA-breaches': count_sla_breaches(actions),
        'Per-channel volume': per_channel_breakdown(actions),
        'Audit-log URL': upload_audit_to_s3(actions)
    }
    notion.create(audit_log_db, audit)
    slack.post('#leadership', format_audit_report(audit))
```

### Recipe 10: Reviewer-load balancing

```python
# Detect if one reviewer is bottleneck
@scheduled('0 9 * * 1')  # weekly Monday 9am
def reviewer_load_audit():
    last_week = notion.query(editorial_db, filter={'Submitted at__gte': now()-7d})
    by_reviewer = defaultdict(list)
    for p in last_week:
        by_reviewer[p['Reviewer']].append(p)
    
    for reviewer, posts in by_reviewer.items():
        avg_approval_time = mean([(p['Approved at'] - p['Submitted at']).total_seconds()/3600
                                  for p in posts if p['Approved at']])
        if avg_approval_time > 24:
            slack.post('#leadership',
                f"⚠ Reviewer load: {reviewer} averaging {avg_approval_time:.1f}-hr approval time on {len(posts)} posts. Consider adding backup reviewer.")
```

## Examples

### Example A: SMB brand team (3 people, 5 channels)

```yaml
team:
  - role: owner: cmo@brand.com (oversees, approves all)
  - role: editor: social-lead@brand.com (manages calendar, publishes)
  - role: author: social-team-1@brand.com (drafts, submits)
plan: Buffer Team $12/channel/mo × 5 channels = $60/mo
approval_flow:
  - Author drafts in Buffer → Status: In review
  - Notion mirror created
  - Slack ping to Editor
  - Editor approves → Status: Approved → Buffer auto-schedules
  - On publish, Slack #social-published confirmation
SLA: 24-hr approval; 4-hr if urgent flag
```

### Example B: Enterprise regulated brand (10+ people, 15 channels)

```yaml
team:
  - 1 owner (CMO)
  - 2 editors (LinkedIn lead + IG/TikTok lead)
  - 5 authors (per-vertical specialists)
  - 3 reviewers (legal, compliance, brand)
plan: Sprout Social Premium + Buffer Agency for cascade
approval_flow:
  - Author drafts → Editor first-review (tone + voice)
  - Editor approves → routes to Compliance reviewer (legal-flagged content)
  - Compliance approves → CMO final-sign-off (regulated content only)
  - 3-tier approval can take 24-72 hrs; build into editorial calendar
audit_log: weekly export, quarterly compliance review
SLA: 72-hr approval default; 24-hr for executive priorities
```

### Example C: Agency managing 5 clients

```yaml
plan: Buffer Agency white-label
clients:
  - client_A: 6 channels, 1 reviewer (client CMO)
  - client_B: 4 channels, 2 reviewers (client CMO + legal)
  - client_C: 8 channels, 1 reviewer
  - client_D: 3 channels, 1 reviewer
  - client_E: 5 channels, 1 reviewer
total: 26 channels × $12 = $312/mo
team:
  - 4 agency authors (assigned per client)
  - 1 agency editor
  - Client reviewers (external)
notion_setup:
  - Top-level editorial DB
  - Per-client filtered views
  - Per-client Slack channel
```

## Edge cases

### Reviewer offline / vacation
Auto-route to backup reviewer after 4 hrs no-action. Backup defined per role in Buffer settings.

### Approval cascade lock
Author submits → reviewer rejects → author edits → re-submits → reviewer needs to re-review. Sometimes pings get lost. Daily standup (Recipe 6) catches.

### Cross-platform inconsistency
LinkedIn approved + ready, but IG variant pending. Cascade may go out partial. Hold all-or-nothing or per-channel.

### Approval bypass risk
"Urgent" tag overuse → effective bypass of governance. Cap urgent posts at 10% of weekly volume.

### Notion + Buffer drift
Status in Buffer ≠ status in Notion. Webhook (Recipe 7) keeps in sync. If drift detected, Buffer is source of truth for scheduled / published; Notion for approval state.

### Multi-language reviewer
Spanish content needs Spanish reviewer. Add language flag in Notion + auto-route to language-specific reviewer.

### Tier conflict (rule clash)
Vale lint flags but reviewer approves anyway. Vale = automated check; reviewer = final authority. Document override in approval notes.

### Audit-log GDPR
Audit log contains email + IP + decision timestamps. Personal data — apply GDPR retention. 365-day default; user can request export.

### Compliance audit reach
Regulated brands may need 7-year retention. Use S3 with retention policy + Notion archive view.

### Buffer plan upgrade
Buffer's per-channel pricing scales. At 20+ channels, Agency plan ($120/mo flat) often cheaper.

### Sprout Social cost
$249-$499/user/mo. For 5+ users, breakeven vs Buffer Agency requires need for inbox routing + collision detection.

### Hootsuite scale
For 30+ channels + 10+ users, Hootsuite Enterprise unlocks Talkwalker listening + Sparkcentral inbox.

### Team handoff (offboarding)
When team member leaves, revoke Buffer + Sprout + Slack access. Rotate org token. Audit prior 30-day actions for unfinished posts → reassign.

### Approval-flow training
New reviewer needs 1-2 hrs walkthrough of brand voice + tier rules. Document in `team-handbook.md`.

### Compliance escalation
Sensitive content (legal, regulatory, executive-named) — pre-flight legal opinion. Cap legal-review SLA at 48 hrs; escalate to chief legal if breach.

### Crisis interrupts approval queue
Crisis flag pauses non-essential approvals. Pre-define what "pauses": branded campaigns yes; SLA replies no.

### After-hours approval
If publishing window outside business hours, pre-approve or delegate. Don't push for after-hours approvals (burnout).

### Multi-brand reviewer coverage
Same reviewer can't cover 5 brands. Add per-brand reviewer pool; rotate.

## Sources

- **Buffer team workspaces + roles**: https://support.buffer.com/article/520-buffer-team-roles
- **Buffer Developers API (approval flow)**: https://buffer.com/developers/api
- **Sprout Social — scheduling + multi-user**: https://sproutsocial.com/insights/social-media-scheduling-tools/
- **Hootsuite team workflows**: https://help.hootsuite.com/hc/en-us/categories/204612247-Teams
- **Notion API**: https://developers.notion.com/
- **Slack API (commands + interactivity)**: https://api.slack.com/interactivity
- **Buffer best-tools for management**: https://buffer.com/resources/best-social-media-management-tools/
