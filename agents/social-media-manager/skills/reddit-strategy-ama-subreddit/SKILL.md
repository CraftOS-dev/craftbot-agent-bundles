<!--
Source: Reddit API: https://www.reddit.com/dev/api
Reddit MCP entry: app/config/mcp_config.json
AMA playbook: role.md "Reddit AMA playbook"
Subreddit health scoring: about.json + mod-removal rate
-->
# Reddit Strategy — AMA + Subreddit Health + Posting Discipline — SKILL

Reddit MCP for posts / comments / DMs. Subreddit health scoring via `/r/<sub>/about.json` (subscribers, recent activity, mod strictness). AMA playbook: T-7 pre-announce + cross-post + first-15-min question seed + live answer queue in Notion. 80/20 rule strict — 4 community contributions per 1 brand post or get mod-banned.

## When to use this skill

- **Subreddit selection** for a campaign — health score + relevance + rules read.
- **AMA planning + execution** — r/IAmA or niche sub.
- **Native Reddit posting** — text, link, image, video per sub.
- **Community engagement** — replies, value-add contributions to maintain 80/20.
- **Crisis listening** — Reddit threads can become PR fires (role.md social listening + crisis comms feeds Reddit signals).

**Do NOT use this skill when:**
- Cross-platform cascade — Reddit doesn't fit Buffer's flow. Always native via `reddit-mcp`.
- Brand-mention monitoring — `social-listening-brandwatch-mention-talkwalker` (Brand24 covers Reddit).

## Setup

### Reddit MCP

```bash
# Native MCP in CraftBot catalog
mcp tool reddit.authenticate
# OAuth via reddit.com/prefs/apps
export REDDIT_CLIENT_ID="<id>"
export REDDIT_CLIENT_SECRET="<secret>"
export REDDIT_USERNAME="<bot_or_brand_user>"
export REDDIT_PASSWORD="<pass>"
export REDDIT_USER_AGENT="brand-agent/1.0 (by /u/youruser)"
```

### Reddit Official REST API

```bash
# Endpoint: https://oauth.reddit.com/
# Rate limit: 60 req/min per OAuth token
# OAuth flow: https://www.reddit.com/api/v1/access_token
```

### Notion Subreddit DB

Columns: `Subreddit / Subscribers / Activity (posts/day) / Mod-strictness (loose/normal/strict) / Promotion policy / Top-flair / Best posting time (ET) / Karma threshold to post / Last brand post date / Result (upvote ratio, comments, traffic)`.

### Notion AMA DB

Columns: `AMA URL / Question / Question author / Upvotes / Sentiment / Answer (draft / sent) / Answered by / Follow-up needed`.

## Common recipes

### Recipe 1: Subreddit health scoring

```bash
mcp tool reddit.get_subreddit_info --subreddit "<sub>"
# Or REST:
curl -H "Authorization: Bearer $REDDIT_OAUTH_TOKEN" \
  -H "User-Agent: $REDDIT_USER_AGENT" \
  "https://oauth.reddit.com/r/<sub>/about.json"
```

Score formula:

```python
def health_score(sub_about, recent_posts_24h, mod_removal_rate):
    subs = sub_about['subscribers']
    active = sub_about['active_user_count']
    score = 0
    if subs > 10_000: score += 2
    if subs > 100_000: score += 1
    if active / subs > 0.005: score += 2
    if recent_posts_24h > 10: score += 1
    if mod_removal_rate > 0.20: score -= 2  # strict moderation
    if 'no_self_promotion' in sub_about.get('rules', []): score -= 1
    return score  # 4-6 = healthy, 2-3 = borderline, 0-1 = risky, <0 = avoid
```

### Recipe 2: Read subreddit rules (every time)

```bash
mcp tool reddit.get_subreddit_rules --subreddit "<sub>"
# Returns: list of rules with title + description + violation_reason
```

Common rule patterns to watch for:
- No self-promotion / 9-to-1 ratio enforced
- No drop-and-go links
- Karma minimum to post
- Account-age minimum
- Title format requirements (e.g., `[Discussion]`, `[Help]`)
- Flair required

### Recipe 3: Post text (with flair)

```bash
mcp tool reddit.submit_post \
  --subreddit "Entrepreneur" \
  --title "How I scaled a SaaS to $1M ARR without raising VC — AMA tomorrow 2pm ET" \
  --selftext "I'm hosting an AMA tomorrow at /r/IAmA. Quick thread to invite questions in advance... [body]" \
  --flair_id "<flair_uuid_for_AMA_or_Discussion>"
```

### Recipe 4: Post link (with first-comment own-link)

Per role.md: first comment in own thread with link/CTA amplifies thread momentum.

```bash
# Submit link post
mcp tool reddit.submit_post \
  --subreddit "marketing" \
  --title "How we 3x'd our content output with one workflow change" \
  --url "https://yourblog.com/3x-content-workflow"

# Wait 60s for thread to populate then drop owner comment
sleep 60
mcp tool reddit.add_comment \
  --thing_id "t3_<thread_id>" \
  --text "OP here — happy to AMA in this thread. The TL;DR: ..."
```

### Recipe 5: AMA pre-announce (T-7 to T-1)

```bash
# T-7: r/IAmA submission for verification
mcp tool reddit.submit_post \
  --subreddit "IAmA" \
  --title "I'm <name>, founder of <brand>, scaled to $1M ARR. AMA on June 18 at 2pm ET" \
  --selftext "Verification: [link to verification photo or post on company blog]\nDate: June 18, 2pm-5pm ET\nWill cover: scaling SaaS / hiring / pricing / what I'd do differently" \
  --flair_id "<scheduled_AMA_flair>"

# T-3 to T-1: cross-post to 3-5 niche subs
for sub in Entrepreneur SaaS smallbusiness startups; do
  mcp tool reddit.submit_post \
    --subreddit "$sub" \
    --title "AMA Tuesday at /r/IAmA: $1M ARR SaaS founder, scaling without VC. Drop Qs here too?" \
    --selftext "..."
done
```

### Recipe 6: AMA day-of execution

```python
# 30 min before live window
mcp.reddit.submit_post(
    subreddit='IAmA',
    title="I'm <name>, founder of <brand>. Just hit $1M ARR. AMA!",
    selftext=AMA_INTRO_TEMPLATE
)
ama_thread_id = post['id']

# Throughout window, pull comments + queue answers
while in_ama_window:
    comments = mcp.reddit.get_comments(thing_id=ama_thread_id, sort='top', limit=100)
    for c in comments:
        if c['id'] not in answered:
            notion.create(ama_db, {
                'AMA URL': c['permalink'],
                'Question': c['body'],
                'Question author': c['author'],
                'Upvotes': c['ups'],
                'Sentiment': sentiment(c['body']),
                'Answer (draft / sent)': 'pending'
            })
    # Sort by upvotes; answer top-3 next
    next_q = top_unanswered_by_upvotes(notion.query(ama_db, filter={'Answer': 'pending'}))
    draft_answer = generate_answer(next_q['Question'], brand_voice)
    # Human review then send
    mcp.reddit.add_comment(thing_id=next_q['id'], text=approved_answer)
    notion.update(next_q['notion_id'], {'Answer (draft / sent)': 'sent', 'Answered by': 'founder'})
```

### Recipe 7: First-15-min seed questions

NOT planted but anticipated. Real internal team members chime in:

```yaml
seed_questions:
  - "How did you handle pricing experiments at $100k ARR?"
  - "What's the one tool you wish you'd adopted earlier?"
  - "How do you balance founder-led marketing vs hiring?"
  - "Did you ever consider raising VC? Why not?"
seed_protocol:
  - 3-5 team members upvote AMA post within 5 min
  - Each posts one seed Q from list (not from script — genuine angle)
  - DM founder to coordinate which Qs first
```

### Recipe 8: Post-AMA digest

```python
# T+24h: top 10 Q&A → cross-promote
top_10 = notion.query(ama_db, sort='-Upvotes', limit=10)
digest = format_qa_digest(top_10)

# Cross-post derivatives
buffer.create_update(channelIds=['linkedin','x'], 
                     text=f"From yesterday's r/IAmA AMA — the top 10 questions:\n{digest_short}\n\nFull thread: {ama_url}")

# Update FAQ
for qa in top_10:
    if qa['Question'] in new_topic:
        notion.create(faq_db, {'Q': qa['Question'], 'A': qa['Answer'], 'Source': 'r/IAmA 2026-06'})
```

### Recipe 9: 80/20 community participation

```python
# Track ratio per sub
weekly_summary = {}
for sub in target_subs:
    posts = mcp.reddit.get_user_history(username=BRAND_USER, sub=sub, since='7d')
    brand_posts = [p for p in posts if 'brand' in p['flair'] or links_to_own(p)]
    community_posts = [p for p in posts if p not in brand_posts]
    ratio = len(community_posts) / max(len(brand_posts), 1)
    weekly_summary[sub] = ratio
    if ratio < 4:
        slack.post('#reddit', f"⚠ /r/{sub}: only {ratio:.1f} community per brand — top up by Friday")
```

### Recipe 10: Subreddit-specific posting time

```python
# Pull per-sub top-posts of week and infer optimal time
def best_post_time(sub):
    top = mcp.reddit.get_top_posts(sub=sub, period='month', limit=100)
    hours = [datetime.fromtimestamp(p['created_utc']).hour for p in top]
    return Counter(hours).most_common(3)
# Cache per-sub for daily content calendar
```

## Examples

### Example A: r/Entrepreneur weekly cadence

```yaml
mon: community contribution — answer 3 high-upvote questions
tue: optional brand post (only if value-driven discussion topic)
wed: community contribution — meaningful comment on weekly stickied thread
thu: community contribution — share resource (non-self-link)
fri: optional case-study post (if relevant)
weekend: community engagement only
ratio: ~5 community : 1 brand per week — safe within 80/20
```

### Example B: 3-hour AMA execution timeline

```
T-30 min: post AMA intro thread
T-0:      live window opens — top-of-thread updates
T+15:     first-15-min queue should have 30+ questions; seed Qs visible
T+30-90:  answer in upvote-sorted order; aim 30+ answers in first hour
T+90:     mid-window: switch to typed-fast mode; bypass top-1, hit broader Qs
T+120:    last-hour push: clean tail of low-upvote but interesting Qs
T+180:    closing comment: "Thanks for the questions! I'll come back tonight for stragglers."
T+24h:    return for stragglers; thank-you DM to mods; digest cross-post
T+48h:    cross-post top-10 Q&A to LinkedIn / X / blog
```

### Example C: Subreddit health-score gate

```yaml
target_sub: SaaS
about_json:
  subscribers: 132,431
  active_users: 1,847
  rules:
    - no link drops without context
    - 9:1 community to self-promo
    - flair required: [Discussion] [Help] [Case Study]
  recent_post_velocity: 18/day
health_score: 5/6 (subs healthy, activity strong, strict-but-clear rules)
verdict: GREEN — post case-study with proper flair, prepare for moderation
```

## Edge cases

### Mod removal rates
Some subs auto-remove links from new accounts. Build 100+ karma in target sub via comments before posting.

### Shadow-removal
Posts may show as live to OP but invisible to others. Verify by checking thread in incognito. If shadow-removed, message mods politely; never re-post immediately.

### Karma + age minimums
Many subs require account age > 30 days + comment karma > 50. Use the brand-rep user (not throwaway) with established history.

### Verification protocol (AMAs)
r/IAmA requires verification — typically photo with handwritten note OR link from company-verified domain. Pre-prep and embed in submission body.

### Hostile audience
If thread tone turns hostile, lean in transparency. Address concerns head-on. Reddit punishes evasion + corporate-speak. Per role.md AMA playbook: "acknowledge controversies head-on".

### Brigading
Linking to other subs from a thread can summon brigades. Don't link sub-to-sub when sentiment is heated. Use `np.reddit.com` (no-participation) links if you must.

### Post too quickly after AMA
Cool-down 2-4 weeks between major brand activities in same sub. Don't drop AMA + product launch + case study back-to-back.

### Reddit search penalty for self-promo
Reddit search ranks self-promo low. Use Reddit MCP search via API to monitor own content discovery.

### Comment vote-manipulation rules
Don't ask staff / friends to upvote — Reddit detects coordinated voting. Genuine community-built momentum only.

### Mod relations
Pre-engage with mods 7+ days before high-profile post. DM with summary, ask if topic OK. Mods can pin / golden-flair / boost or quietly nuke.

### Sentiment swing
Reddit threads can swing positive → negative in minutes. Monitor via `reddit-mcp` thread fetch every 5-15 min during launch / AMA. If sentiment flips, address in next answer.

### Disclosure on sponsored posts
Mods enforce sponsor-disclosure tags (most subs). Add `[Sponsored]` or `[Promo]` in title; subs without auto-flair require manual marker.

### Cross-posting throttle
Cross-posting 5+ subs in 24 hrs triggers Reddit's anti-spam. Stagger across 7-14 days; vary intro text per sub.

### Account suspension
Bans cascade — if brand account gets sub-banned, similar offenses across other subs flag. Build community goodwill before any single brand post.

### Search ranking + SEO
Reddit results rank high in Google. A well-titled thread = SEO win. Title front-load with target query verbatim per role.md "Reddit" section.

### NSFW / quarantined subs
Even relevant niche subs in quarantined state hurt brand reputation. Avoid entirely.

## Sources

- **Reddit API documentation**: https://www.reddit.com/dev/api
- **Reddit MCP entry**: `app/config/mcp_config.json`
- **Reddit OAuth flow**: https://github.com/reddit-archive/reddit/wiki/OAuth2
- **r/IAmA rules**: https://www.reddit.com/r/IAmA/wiki/index
- **Reddit moderation guide**: https://mods.reddithelp.com/
- **AMA playbook**: role.md "Reddit AMA playbook"
- **Subreddit health metrics**: https://www.reddit.com/r/redditdev/wiki/index
- **Reddit best post times**: https://blog.hootsuite.com/best-time-to-post-on-reddit/
