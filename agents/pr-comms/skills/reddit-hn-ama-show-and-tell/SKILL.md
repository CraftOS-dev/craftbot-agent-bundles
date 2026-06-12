<!--
Source: https://www.stackmatix.com/blog/reddit-ama-marketing
Reddit AMA guidelines: https://www.reddit.com/r/IAmA/wiki/index
HN guidelines: https://news.ycombinator.com/showhn.html
Common Room: https://www.commonroom.io/
role.md Reddit AMA + Show HN playbooks: internal
-->
# Reddit AMA + HN Show HN + Community AMA — SKILL

Reddit AMA scheduling (`reddit-mcp` + mod outreach + verification), Show HN launch (`playwright-mcp` form submit, no API), and post-event Q&A archiving for repurposing. Community-led signal capture via Common Room. 2-3 hour live + 24-hour follow-up commitment. Founder responds to every comment within 30 minutes for first 4 hours of Show HN.

## When to use this skill

- **Founder / exec Reddit AMA** — r/IAmA (strict verification, highest visibility) or niche sub (r/SaaS, r/startups, r/devops, r/entrepreneur).
- **Show HN launch** — new product / OSS project / major feature. Tuesday-Thursday morning ET sweet spot.
- **Ask HN insight gathering** — strategic question to HN community pre-launch.
- **Customer / OSS contributor AMA** — third-party advocate (not founder) hosts; tags the brand.
- **Post-launch community wrap-up** — repurpose AMA / Show HN Q&A into thought-leadership content.
- **Industry-subreddit thought leadership** — bi-weekly senior-exec POV post (not promotional).

**Do NOT use this skill when:**
- The launch is broad-press (wire + tier-1 outreach) — use `press-release-writing-distribution`.
- The community is private Discord/Slack — use `dark-social-tracking`.
- The audience is enterprise buyers, not technical/developer — Reddit/HN won't reach them.

## Setup

### reddit-mcp

```bash
# Already in agent.yaml
# Requires Reddit app credentials (developer account)
export REDDIT_CLIENT_ID="<id>"
export REDDIT_CLIENT_SECRET="<secret>"
export REDDIT_USER_AGENT="acme-comms-bot/1.0"
export REDDIT_USERNAME="<account>"
export REDDIT_PASSWORD="<password>"
```

Use a dedicated spokesperson account, not company brand account. Reddit auto-flags brand accounts as promo.

### Hacker News submission

```bash
# HN has NO public submission API. Two paths:
# 1. Manual: founder submits via https://news.ycombinator.com/submit
# 2. Automated: playwright-mcp with founder's HN credentials (logged-in session)
export HN_USERNAME="<founder_username>"
export HN_PASSWORD="<founder_password>"  # store in vault, not env
```

HN strongly favors authenticity. Submission from a karma-aged personal account works better than a fresh "brand" account (which gets shadowbanned within hours).

### Common Room for AMA signal capture

```bash
# https://www.commonroom.io — community-led growth platform
# Identify which AMA participants are at target accounts
export COMMONROOM_API_KEY="<key>"
export COMMONROOM_API_BASE="https://api.commonroom.io/community/v1"
```

Connect Reddit + HN as sources. Common Room flags AMA participants who match target-account criteria.

### Notion AMA / Show HN tracking DB

Per event:
- `event_id` (text)
- `event_type` (select: reddit_ama, show_hn, ask_hn, community_ama, subreddit_thoughtleadership)
- `subreddit_or_platform` (text)
- `scheduled_time` (datetime — explicit timezone)
- `spokesperson` (text)
- `mod_approval_status` (select: pending, approved, declined, n/a)
- `verification_completed` (checkbox)
- `pre_announcement_url` (URL)
- `live_post_url` (URL)
- `q_and_a_archive_url` (URL — Notion page)
- `comments_responded_count` (number)
- `comments_total` (number)
- `upvotes_final` (number)
- `front_page_position_peak` (number, HN only)
- `community_followups_assigned` (multi-text — moderator + commenter follow-ups)
- `repurposed_content_links` (multi-URL — LinkedIn / Substack / blog from this AMA)

## Common recipes

### Recipe 1: Subreddit selection + mod DM (Reddit AMA)

```bash
# Step 1: identify subreddit by topic match + audience size
# Don't aim for r/IAmA only — niche subs have higher signal-to-noise

subreddits=("IAmA" "startups" "SaaS" "devops" "entrepreneur")

for sub in "${subreddits[@]}"; do
  reddit-mcp get_subreddit_info --name "$sub" \
  | jq '{
      subscribers, active_users, 
      ama_friendly: (.rules[] | select(.short_name | test("AMA|self-promo"; "i"))),
      mods: .moderators[0:5]
    }'
done

# Step 2: DM mods 1-2 weeks ahead — include verification offer + topic
for mod in "${MODS[@]}"; do
  reddit-mcp send_dm --to "$mod" --subject "AMA pitch: [Topic]" \
    --body "$(cat <<'EOF'
Hi [Mod],

I'd like to host an AMA with [Spokesperson Name, Title at Company]
on [Topic the sub cares about] — happy to follow your verification
process and commit to 2-3 hours live + 24-hour comment followup.

Proposed window: [date + ET time]. Open to alternative slots.

Background on spokesperson: [brief 2-line bio + recent press link].

Verification: photo with handwritten note matching username,
LinkedIn match, or whatever method you prefer.

Let me know if this fits the sub. Happy to adjust topic to better
match what your community wants to hear from this kind of guest.

Thanks,
[Comms lead name + role]
EOF
)"
done
```

Save the mod conversation in `notion-mcp` AMA DB. Without written mod approval, do NOT proceed (mod can lock + ban the post, killing brand goodwill).

### Recipe 2: Spokesperson verification

```bash
# Per subreddit rules. Common: handwritten note + photo
# Generate verification image, then spokesperson takes the photo

cat > verification_note.txt <<EOF
Hi r/$SUBREDDIT! This is [Spokesperson Name, Title at Company].
I'm doing an AMA on $(date +%Y-%m-%d). Username: u/$REDDIT_USERNAME.

Verification: https://[company]/ama-$(date +%Y-%m-%d)
EOF

# Spokesperson writes this by hand, photographs with face visible
# Upload to imgur or i.redd.it via reddit-mcp media upload
# Embed image in opening post
```

### Recipe 3: Pre-AMA FAQ doc

```python
# Generate 20-30 likely questions + recommended answers
# Tag each with: must-answer vs nice-to-have vs banned (legal-cleared)

faq = claude.generate(
    prompt=f"""
    You are prepping {spokesperson_name} for a Reddit AMA on {topic}.
    
    Subreddit: r/{subreddit} ({subscribers} subscribers, {avg_post_karma} avg karma).
    Spokesperson background: {bio}.
    Recent company milestones: {milestones}.
    Sensitive topics to redirect: {banned_topics}.
    
    Generate 25 likely questions, sorted by likelihood. For each:
    - Recommended answer (under 100 words, candid, Reddit-tone)
    - If banned topic → recommended redirect ("I can't speak to that, but here's what I can share")
    - If technical → include source / spec / data
    """
)

notion_mcp.create_page(
    db="ama_prep",
    properties={
        "event_id": event_id,
        "spokesperson": spokesperson_name,
        "faq_questions": faq,
        "banned_topics": banned_topics,
    }
)
```

### Recipe 4: Pre-announcement post (24h before)

```bash
# Day before AMA: announcement post in the sub

reddit-mcp create_post --subreddit "$SUBREDDIT" \
  --title "Tomorrow at 10am ET: AMA with $SPOKESPERSON_NAME, $SPOKESPERSON_TITLE at $COMPANY — [Topic]" \
  --text "$(cat <<EOF
Hi r/$SUBREDDIT!

Tomorrow at 10am ET, [Spokesperson Name] ($SPOKESPERSON_TITLE at $COMPANY) is doing an AMA here on [Topic]. They've spent [N years] working on [domain] and [recent notable achievement].

Drop questions in this thread or wait until tomorrow — they'll answer in the live thread.

Verification will be in the live post.

See you tomorrow!
EOF
)"
```

### Recipe 5: Live AMA execution

```python
# T-0: opening post with verification image
opening = reddit_mcp.create_post(
    subreddit=subreddit,
    title=f"I'm {spokesperson_name}, {title} at {company}. Building {product}. AMA!",
    text=f"""
Hi r/{subreddit}!

Verification: [verification image link]

I'm {spokesperson_name}, {title} at {company}. [2-3 sentence background.]

I'll be answering questions live for the next 2-3 hours, then continuing to respond in 24-hour followup window.

Ask me anything about [topic + 2-3 sample sub-topics]. I'll be candid where I can and clear when I can't.
"""
)

# Monitoring loop during live window
while time_elapsed < 3 * 3600:
    new_comments = reddit_mcp.get_post_comments(
        post_id=opening.id,
        since=last_check,
    )
    
    for comment in new_comments:
        # Claude drafts response
        draft = claude.generate(
            prompt=f"""
            Respond to this Reddit AMA comment in {spokesperson_name}'s voice.
            FAQ doc: {faq_doc}
            Banned topics: {banned_topics}
            Comment: {comment.body}
            
            Be candid, specific, Reddit-tone (no corporate jargon, no PR-speak).
            Under 200 words. If banned topic → redirect per FAQ.
            """,
        )
        
        # Human (spokesperson) approves OR edits before posting
        approved = await spokesperson_approval(draft, comment)
        if approved:
            reddit_mcp.reply_to_comment(comment.id, approved)
        
        # Log
        notion_mcp.update_page(
            event_id=event_id,
            properties={"comments_responded_count": +1}
        )
    
    sleep(60)  # 1-min poll
```

### Recipe 6: Show HN submission via playwright-mcp

```python
# No HN submission API. Use playwright-mcp with founder's logged-in session.

# Title format: "Show HN: [Product] – [One-liner]"
# Optimal: Tuesday-Thursday, 7-10am ET

await playwright_mcp.navigate("https://news.ycombinator.com/login")
await playwright_mcp.fill("[name=acct]", HN_USERNAME)
await playwright_mcp.fill("[name=pw]", HN_PASSWORD)
await playwright_mcp.click("input[type=submit]")

await playwright_mcp.navigate("https://news.ycombinator.com/submit")
await playwright_mcp.fill("[name=title]", f"Show HN: {product_name} – {one_liner}")
await playwright_mcp.fill("[name=url]", landing_page_url)
await playwright_mcp.click("input[type=submit]")

# Capture submission URL
post_url = await playwright_mcp.current_url()
post_id = post_url.split("id=")[-1]

# Post the first comment from founder (THIS IS CRITICAL — sets the tone)
await playwright_mcp.navigate(f"https://news.ycombinator.com/item?id={post_id}")
await playwright_mcp.fill(
    "textarea",
    f"""Hi HN — {founder_name} here, {role} at {company}.

We built {product_name} because [authentic origin story, 2-3 sentences].

What's new: [3-bullet feature summary, no marketing-speak].
Try it: {url} (free tier, no signup required).

Pricing: {pricing_summary}.

Tech stack: [be specific — HN appreciates this].

Open questions for you all: [genuine question about a design tradeoff].

Happy to answer everything. I'll be here for the next 4 hours."""
)
await playwright_mcp.click("input[type=submit]")
```

### Recipe 7: Show HN comment monitoring + response

```python
# First 4 hours: founder responds to EVERY comment within 30 min
# HN ranking algorithm favors high-quality discussion

while time_elapsed < 4 * 3600:
    thread = firecrawl_mcp.scrape(f"https://news.ycombinator.com/item?id={post_id}")
    new_comments = parse_hn_thread(thread, since=last_check)
    
    for comment in new_comments:
        # Show HN comments often: technical question, criticism, comparison, feature request
        comment_type = claude.classify(comment.body, types=[
            "technical_question", "criticism", "comparison", 
            "feature_request", "compliment", "off_topic"
        ])
        
        draft = claude.generate(
            prompt=f"""
            Founder response to HN comment. Use {founder_name}'s voice.
            Comment type: {comment_type}.
            Comment: {comment.body}.
            
            HN style: technically substantive, no marketing-speak, candid about
            shortcomings, specific about future work. Under 200 words usually.
            
            If criticism: acknowledge + specific response + open to feedback.
            If comparison: factual differences, not dunking on alt.
            If feature request: be specific about whether/when, or honestly "not on roadmap."
            """
        )
        
        approved = await founder_approval(draft, comment)
        if approved:
            await playwright_mcp.reply_to_hn_comment(comment.id, approved)
    
    # Position tracking
    position = await playwright_mcp.find_post_position(post_id)
    notion_mcp.update_page(event_id, {"front_page_position_peak": min(current, position)})
    
    sleep(120)  # 2-min poll during launch
```

### Recipe 8: Post-event archive + repurpose

```bash
# Archive Q&A to Notion knowledge base + repurpose

# Pull all comments
all_comments=$(reddit-mcp get_post_comments --post-id "$POST_ID" --depth all)
echo "$all_comments" | jq '.' > ama_archive.json

# Save to Notion as searchable page
notion-mcp create_page --db ama_archive \
  --title "AMA: $SPOKESPERSON — $TOPIC — $(date +%Y-%m-%d)" \
  --content "$(jq -r '.[] | "### Q: " + .question + "\n\nA: " + .answer + "\n\n---\n"' ama_archive.json)"

# Pull 5 best moments for repurposing
best=$(echo "$all_comments" | jq '[.[] | select(.score > 10)] | sort_by(-.score) | .[0:5]')

# Generate LinkedIn post + Substack newsletter draft + X thread
claude --prompt "Generate 3 repurposed content pieces from these AMA highlights: [LinkedIn 800-1500 char post, Substack newsletter 800-word draft, X thread 6-tweet]. AMA highlights: $best"
```

### Recipe 9: Common Room AMA signal capture

```bash
# Connect Reddit + HN to Common Room
curl "$COMMONROOM_API_BASE/sources/configure" \
  -H "X-API-Key: $COMMONROOM_API_KEY" \
  -d '{
    "source_type": "reddit",
    "subreddits": ["SaaS", "startups", "devops"],
    "keywords": ["Acme", "our-product"]
  }'

# After AMA: pull list of participants who are at target accounts
curl "$COMMONROOM_API_BASE/members/from-event?event_id=$EVENT_ID" \
  -H "X-API-Key: $COMMONROOM_API_KEY" \
| jq '.members[] | select(.company_match == true) | {
    name, company, email_or_handle, signal_context
  }'

# Hand off to sales for warm follow-up
```

## Examples — full Show HN launch program

```yaml
pre_launch_week:
  - landing page polished + mobile tested
  - founder + technical team on standby for 4-hour launch window
  - faq doc drafted (technical questions, pricing, comparison, roadmap)
  - pricing transparent on landing page (HN hates evasion)
  - backup plan: founder scheduled tweet at submission moment

launch_day:
  - 0700 ET: founder submits via playwright-mcp with karma-aged account
  - 0701 ET: first comment from founder (origin + features + open question)
  - 0700-1100 ET: respond to every comment within 30 min
  - cron firecrawl every 2 min for thread updates
  - track: upvotes/1hr, front page position, comment count, sentiment
  - parallel: slack-mcp #show-hn-launch channel for team coordination

day_after:
  - founder responds to overnight comments
  - archive thread to notion ama-archive db
  - pull 5 feedback themes into product backlog
  - claude drafts "what we learned" post for owned blog

day_3:
  - publish "what we learned from Show HN" on company blog + linkedin
  - reach out to commenters who showed product interest (per common-room enrichment)
  - update faq based on questions repeated 3+ times

week_after:
  - retrospective: what we'd do differently
  - update show-hn playbook template in notion
```

## Edge cases

### Mod relationships are the gate
r/IAmA + r/startups + r/SaaS mods see 100s of AMA pitches/week. Without prior subreddit participation by spokesperson (or relationship with mods), pitches get ignored. Build credibility 3-6 months ahead — spokesperson should be a real commenter, not just an AMA opportunist.

### Verification photo failures
Spokesperson sends low-res photo / missing date / username off-screen → mod removes post. Reshoot with clear visibility. Pre-flight: PR lead reviews photo before spokesperson hits submit.

### Show HN karma threshold
Brand-new HN accounts get shadowbanned. Spokesperson account should have 3-6 months of organic comments + 100+ karma minimum. If founder doesn't have one, build it (real comments on real threads) before launch — months ahead.

### HN comment authenticity
HN spots "marketing speak" within seconds. Banned phrases in Show HN comments: "we're thrilled," "leveraging," "best-in-class," "revolutionary." Use spokesperson's actual voice. Run Vale lint on opening comment.

### Negative thread momentum
A bad first hour on Show HN tanks the launch. If thread goes negative (downvotes, hostile criticism), DON'T delete or argue. Acknowledge specific criticisms, ship same-day fixes if possible, post the fix. Letting the thread die naturally is better than fighting it.

### Brand vs spokesperson account
Reddit + HN both penalize brand-named accounts. Use spokesperson's personal account (u/janesmith) not company account (u/acme-co). Disclosure of affiliation in opening post is required — but the account is personal.

### Subreddit anti-spam timing
Most subs have anti-spam rules: max 1 self-promo post per N days, max promo ratio (e.g., 9:1 community-content : self-promo). Spokesperson should have built community engagement history before AMA. r/entrepreneur is especially strict.

### Cross-posting fragmentation
DON'T cross-post the same AMA to multiple subs. Each AMA dilutes signal. Pick ONE primary sub. If multiple categories matter (founders + technical), do TWO separate AMAs spaced 2+ weeks apart.

### Show HN vs Ask HN vs Tell HN
- **Show HN**: working product/demo for users to try. URL required.
- **Ask HN**: question to community. No URL.
- **Tell HN**: announcement of HN-relevant thing. Rare; mostly for outages or HN-meta news.

Use Show HN for product launches; Ask HN for strategic input pre-launch.

### Comment moderation discipline
NEVER edit a posted comment after publish. Reddit shows edit marks; HN does too. If you made an error, post a correction reply. Edits look defensive.

### Time-zone optimization
- **Reddit AMA**: 10am-1pm ET = peak US activity, decent EU overlap.
- **Show HN**: 7-10am ET = HN morning crowd wakes up + has time to engage.

Tuesday-Thursday best both. Monday is slow; Friday afternoon dies fast.

### Common Room target-account enrichment
Common Room flags AMA participants who work at named target accounts. Hand off to sales for warm intro. PR keeps the AMA signal; sales gets the lead.

### Hand-off to thought leadership
AMA / Show HN content repurposes well: best Q&A → LinkedIn post, full archive → blog post, recurring themes → Substack newsletter. Hand off to `executive-thought-leadership-linkedin-substack` for cadenced repurposing.

### Dark social spillover
Strong AMAs/Show HNs spawn Discord/Slack conversation within hours. Configure `dark-social-tracking` to monitor for the post-event ripple. Often dark-social mentions exceed direct AMA engagement 5-10x.

### Crisis-mode AMA pivot
If a brand is in crisis, an AMA can be the response channel — but ONLY if spokesperson can be radically transparent. Defer to `crisis-comms-24-48-72-hour-playbook`; AMA is one possible tactic within the broader response.

### Subreddit thought-leadership cadence
Beyond AMAs: senior exec can post substantive POV (no link) to relevant subs bi-weekly. Builds account karma + reputation for future AMA. r/SaaS / r/startups / r/devops appreciate technical depth + candor.

### Failure recovery
AMA flops (low engagement, hostile crowd): do NOT delete. Let it close naturally. Post-mortem: was the topic mismatched? spokesperson too corporate? time-zone wrong? sub too niche/broad? Apply lessons to next AMA. Reddit memory is long but forgiving with consistent good-faith participation.

## Sources

- **Reddit AMA marketing guide (Stackmatix)**: https://www.stackmatix.com/blog/reddit-ama-marketing
- **r/IAmA wiki + rules**: https://www.reddit.com/r/IAmA/wiki/index
- **Reddit Developer API**: https://www.reddit.com/dev/api
- **Hacker News guidelines**: https://news.ycombinator.com/newsguidelines.html
- **HN Show HN guidelines**: https://news.ycombinator.com/showhn.html
- **HN submission endpoint**: https://news.ycombinator.com/submit
- **Common Room community-led growth**: https://www.commonroom.io/
- **Common Room API**: https://www.commonroom.io/docs/api
- **role.md Reddit AMA + Show HN playbooks**: internal `agent_bundle/agents/pr-comms/role.md`
