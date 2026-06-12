# Social Media Manager — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Platform format spec", "Hashtag basket spec", "Influencer outreach playbook", "Community engagement playbook", "Crisis comms playbook", "Reddit AMA playbook", "Social listening playbook", "Trend monitoring playbook", "Social commerce setup", "Brand voice per platform", "UGC reposting workflow", "Account takeover playbook", "Multi-platform campaign playbook", "SOTA tool reference", "Success metrics", "Discord rule pack template", "Slack rule pack template".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Platforms this agent operates

| Tier | Platforms | Native MCP available? |
|---|---|---|
| Western mainstream | LinkedIn, X / Twitter, Instagram (Feed + Reels + Stories), TikTok, Threads, Bluesky, Mastodon, Reddit, YouTube (Community Posts + Shorts), Pinterest, Snapchat | most yes (see agent.yaml) |
| Messaging surfaces | WhatsApp Business, LINE, Telegram, Discord, Slack, MS Teams | yes |
| APAC | WeChat, Bilibili, Xiaohongshu, Lemon8, Douyin, Kuaishou, Weibo | partial (WeChat / Bilibili yes; others scrape fallback) |
| Niche / B2B | Substack Notes, Hacker News, Product Hunt comments, Indie Hackers | scrape / API |

### Formats this agent handles

- Static image post (single + carousel — IG carousel 10 cards / LinkedIn document carousel 100 pages)
- Short-form video (Reel 15-90s / TikTok 15-180s / Shorts ≤ 60s)
- Long-form video metadata only (hand to `video-creator` for production)
- Text post / thread (X thread 25+ / LinkedIn long-post 1300-1900 chars / Threads chain)
- Stories (IG / FB / LinkedIn / TikTok Stories — 24hr ephemeral)
- Live streams (IG Live / TikTok Live / X Spaces / LinkedIn Live — coordination only, not host)
- Pinterest pins (idea pin / static pin / shop pin)
- YouTube Community Posts (poll / image / text)
- Reddit text post / link post / image / AMA
- WhatsApp broadcast list + catalog
- Discord announcement + thread + poll
- Slack channel post + thread
- DMs (across IG / X / LinkedIn / TikTok / Threads / Discord / Slack)

### Tool categories with SOTA picks (2026)

| Category | SOTA picks |
|---|---|
| Cross-platform publishing | Buffer (MCP, May 2026 GA), Later (analytics-rich), Hootsuite (enterprise + Talkwalker), Sprout Social (collision detection + inbox routing), Sprinklr / Khoros (regulated enterprise), Agorapulse (SMB inbox assistant), Loomly (calendar-first), Publer (AI assist), SocialPilot, Sendible, MeetEdgar, CoSchedule |
| Social listening | Brand24 (Brand24 MCP, AI sentiment, $199+/mo), Talkwalker (now Hootsuite, 30+ networks + 150M web), Meltwater (TV/radio/podcast/print), Mention, Awario, Pulsar Platform, Audiense, Followerwonk |
| Influencer | Modash (350M+ profiles, Discovery API), Aspire (managed program CRM + payments), GRIN (CRM + payments), Tagger Media, Upfluence, Klear, CreatorIQ (regulated/enterprise), Linqia, Captiv8, IZEA, HypeAuditor (AQS fraud detection) |
| Content discovery | BuzzSumo, SparkToro, Linkfluence |
| Social commerce | TikTok Shop, Instagram Shop (Graph API product_tags), Pinterest Shop, Facebook Shops, YouTube Shopping; Shopify as catalog hub |
| Link-in-bio | Linktree (REST API), Beacons (AI brand outreach), Stan Store (creator monetization, no transaction fees), Bonsai |
| Discord moderation | Carl-bot, MEE6 (21M+ servers), Dyno, Moderator.fm cross-platform |
| Trend tracking | TikTok Creative Center, Tokchart (daily), Buffer trending lists, Brandwatch / Trends24 for X |
| UGC rights | Pixlee, Taggbox, Bazaarvoice, Flockler |

---

## Platform format spec (June 2026)

> Grep target: "Platform format spec"

### LinkedIn

- **Feed post**: 1300-1900 chars optimal, max 3000. First 210 chars are above-fold (hook).
- **Carousel (document)**: 100 pages max (PDF upload via Marketing API 2-step URN flow); highest organic engagement format.
- **Article**: long-form (1500-2500 words ideal); separate from feed; not shown in feed by default.
- **Newsletter**: subscriber-cultivated, separate publish surface; LinkedIn promotes via notifications.
- **Live + Audio events**: scheduling + promotion; hand to `video-creator` for production.
- **Hashtags**: 3-5 max. Branded + niche industry tags. No spammy general tags (e.g. #motivation).
- **Emoji**: minimal (1-3 per post). Professional tone.
- **Mentions**: tag relevant people / orgs sparingly; spammy tagging is flagged.
- **Posting time**: weekday 8-10am or 12-1pm local; Tue/Wed/Thu highest engagement.

### X (Twitter)

- **Post**: 280 chars (X Premium: 25,000 chars; but algorithm prefers concise).
- **Thread**: 5-25 posts; first post is the hook; thread for storytelling or framework.
- **Reply**: opportunity to add value to conversations; algorithm boosts replies in original thread context.
- **Hashtags**: 1-2 max. Overuse penalized.
- **Emoji**: moderate. Brand-relevant.
- **Media**: image / GIF / video / poll; native media outperforms link-with-image.
- **Posting time**: weekday 9am or 1-3pm; spike around news cycle.

### Instagram

- **Feed post (single image)**: 138-150 chars in caption first chunk visible.
- **Carousel**: 10 cards max; first card is hook; swipe completion is engagement signal.
- **Reels**: 15-90s; vertical 9:16; trending audio = 3-5x reach; first 3s critical.
- **Stories**: 24hr ephemeral; 15s per slide; stickers + polls + Q&A drive engagement.
- **IG Live**: not host (hand to `video-creator` for production support).
- **Hashtags**: 20-30 in caption or first comment; mix branded + niche + community + trending.
- **Emoji**: moderate-high.
- **Posting time**: weekday 11am-1pm or 7-9pm.

### TikTok

- **Video**: 15-180s; vertical 9:16; hook in first 1-3s; on-screen text + caption + voiceover.
- **Caption**: 100-150 chars; keyword-front-loaded for TikTok SEO.
- **On-screen text**: TikTok SEO signal — keywords visible to OCR.
- **Alt text** (2026 feature): TikTok SEO signal — populate it.
- **Hashtags**: 3-5; #fyp does not work; mix trending + niche + branded.
- **Trending sound**: 48-hour window gives 3-5x algorithmic push.
- **Posting time**: Tue-Thu 6-10am or 7-11pm.

### Threads

- **Post**: 500 chars; chains for deeper takes.
- **Tone**: conversational, longer than X, less polished than LinkedIn.
- **Hashtags**: 0-3.
- **Reply**: high-leverage engagement; native to Threads culture.
- **Posting time**: not algorithm-bound to time-of-day as tightly; rhythm matters more.

### Bluesky

- **Post**: 300 chars; reply chains supported.
- **Tone**: tech-savvy, decentralized-friendly, less PR-flavored.
- **Hashtags**: 0-3.
- **Lists / custom feeds**: Bluesky-specific; encourage community curation.

### Reddit

- **Title**: 300 chars; keyword-front-loaded for Reddit SEO.
- **Body**: markdown allowed; long-form OK in relevant subs.
- **Comment-link in first hour**: amplifies thread momentum.
- **Image / video**: native upload beats link-out.
- **Flair**: per subreddit rules.
- **80/20 rule**: 4 community contributions per 1 brand post.

### Pinterest

- **Pin**: 1000×1500 vertical optimal; title 100 chars; description 100-200 chars.
- **Idea Pin** (legacy): multi-page format.
- **Shop Pin**: links to product page.
- **Boards**: themed; SEO matters in board title + description.

### YouTube Shorts + Community Posts

- **Shorts**: ≤60s vertical 9:16; first 3s critical.
- **Community Post**: text / poll / image / GIF; for engaging existing subscribers.
- **Title + description**: keyword-front-loaded for YouTube SEO.
- **Tags**: 5-10 relevant; less impactful than title.

### WhatsApp Business

- **Broadcast list**: 256 contacts max per list; opt-in required.
- **Catalog**: product showcase; clickable from chat.
- **Greeting message**: auto-reply on first contact.

---

## Hashtag basket spec

> Grep target: "Hashtag basket spec"

### Instagram (20-30 tags optimal)

- **Trending** (5): pulled from TikTok Creative Center cross-platform reads + Brand24 co-occurrence
- **Niche** (15): industry-specific, 10k-500k usage range (sweet spot for discoverability without saturation)
- **Branded** (5): #yourbrand, #yourbrandX_Y campaign tags, employee advocacy tags
- **Community** (5): #catsofinstagram, #foodie, #sundayvibes — broad-affinity discovery tags

### TikTok (3-5 tags)

- 1 trending hashtag (TikTok Creative Center top 20 last 7 days)
- 1-2 niche hashtags (industry / topic)
- 1 branded hashtag
- 0-1 challenge/community hashtag if relevant
- **Never use #fyp** — TikTok algorithm ignores it as ranking signal

### X (1-2 tags)

- 1 high-relevance, 1 branded if applicable
- Hashtag spam penalized

### LinkedIn (3-5 tags)

- 1-2 industry hashtags (#marketing, #saas)
- 1 branded
- 1-2 niche professional (#contentstrategy, #b2bsaas)

### Threads (0-3 tags)

- Sparse — Threads culture prefers fewer
- Trending or branded if used

### Reddit

- No hashtags. Subreddit choice is the discovery vector.

### Hashtag rotation rule

- **Never repeat the same exact basket twice in a week.** Algorithms penalize repeated-pattern accounts as bots.
- Track hashtag performance per post in Notion DB: reach / engagement rate / discovery share.

---

## Community engagement playbook

> Grep target: "Community engagement playbook"

### SLA matrix

| Type | SLA | Rationale |
|---|---|---|
| Urgent (complaint, crisis-adjacent, named-person mention) | 15 min | Crisis-prevention window |
| Question | 4 hrs | Engagement velocity boost while still timely |
| Praise / positive engagement | 24 hrs | Reciprocal engagement; testimonial source |
| DM (general) | 4 hrs | Personal-channel expectations |
| Spam | n/a | Mark + delete; no reply |

### Engagement queue workflow

1. Pull engagements via Buffer MCP `getEngagements({since: lastRun, channels: enabled})` — covers comments + DMs + brand mentions for connected channels.
2. Classify per matrix above. Tag in Notion DB: `urgent / question / praise / complaint / spam / DM / tag-only`.
3. Reply queue prioritized by SLA breach risk. Auto-route complaints → `social-customer-service-handoff` skill.
4. Track recurring patterns:
   - Recurring complaint (>3 in 7 days, same topic) → flag product team via `slack-mcp`.
   - Recurring question → FAQ candidate in `notion-mcp` FAQ DB.
   - Recurring praise (>5 in 7 days) → testimonial candidate (with permission).

### Reply quality bar

- 2-line minimum substantive reply (or genuine 1-line if context makes it natural)
- Personalize: use @ handle / first name
- Reference what they said specifically — generic "thanks!" replies are flagged as bot-like
- Add value where possible: link to helpful resource, answer their underlying question, offer to take it to DM if complex

### Comment moderation

- **Hide** spam, hate speech, off-topic (per platform tools)
- **Pin** stellar examples — algorithms reward pinned-comment engagement
- **Engage early** — replies in first hour signal "active community" to the algorithm

---

## Influencer outreach playbook

> Grep target: "Influencer outreach playbook"

### Brief required before outreach

```markdown
# Influencer Campaign Brief: [Campaign Name]

## Objective
- Goal: [awareness / conversion / community-building / SEO backlinks / UGC seeding]
- Success metric: [reach / engagement rate / clicks / conversions / GMV]

## Audience
- Target demographic: [age / gender / country / interest overlap]
- Platform: [IG / TikTok / YouTube / LinkedIn / X]
- Creator tier: [nano (1k-10k) / micro (10k-100k) / mid (100k-500k) / macro (500k-1M) / mega (1M+)]

## Constraints
- AQS threshold (HypeAuditor): ≥ 70 (reject below)
- Engagement rate floor: nano/micro > 2% / mid > 1% / macro > 0.5%
- Brand-safety check: no controversy in last 6 months
- Audience match: > 60% in target country + > 50% in target age

## Budget
- Per-creator range: $X-$Y
- Total budget: $Z
- Payment terms: 50% upfront / 50% post-publish; or flat fee per deliverable

## Deliverables
- Format: [Reel / TikTok / Story / IG post / YouTube integration]
- Quantity: [N posts]
- Usage rights: [organic only / paid-boost / repurpose window]
- Hashtag set: [#brand #campaign #ad]
- Disclosure: #ad #sponsored mandatory (FTC)
- Approval flow: [pre-approval required / post-publish review]

## Timeline
- Outreach window: [date range]
- Content production: [date range]
- Publish window: [date range]
- Performance review: [date]
```

### Modash Discovery filters

```
audience_country=[target]
audience_age=18-34
audience_gender=female_60_pct
engagement_rate>2.0
followers_range=10000-100000
niche=[fitness | beauty | gaming | etc.]
recent_post_within_days=30
```

### HypeAuditor AQS gate

- AQS 70-79: viable, monitor audience-authenticity breakdown
- AQS 80-89: strong; default-include
- AQS 90+: premium
- AQS < 70: **REJECT** — bots, mass-followers, or growth-trick farm signals

### Personalized outreach copy structure

1. **Why them specifically** — reference a recent post you actually watched
2. **Why this campaign aligns** — link to their content style + audience overlap
3. **Concrete offer** — deliverables + budget range upfront (no "let's chat")
4. **Easy yes path** — calendar link OR one-question reply ("Are you booking July?")

### Campaign tracking (Notion DB columns)

`Handle / Platform / Followers / AQS / Audience-match % / Engagement rate / Status (pitched/negotiating/signed/shipping/posted/paid) / Brief sent date / Contract signed date / Posts shipped / Posts published URL / Reach / Engagement / Clicks / Conversions / Total cost / ROI`

---

## Social listening playbook

> Grep target: "Social listening playbook"

### Daily triage workflow

1. Brand24 / Talkwalker daily export → ingest into Notion DB or local CSV
2. Triage table:

| Mention URL | Date | Channel | Author | Sentiment | Reach | Action | Status |
|---|---|---|---|---|---|---|---|

3. Action assignments:
   - **Positive + high reach**: reshare candidate / quote-tweet / testimonial DB
   - **Negative + low reach**: DM author, ask what went wrong, resolve quietly
   - **Negative + high reach**: trigger crisis-comms watch — re-evaluate every 30 min
   - **Neutral + high reach**: opportunity-watch — could it become positive with engagement?

### Sentiment thresholds (alert triggers)

| Threshold | Trigger |
|---|---|
| Negative volume > 2x baseline (rolling 7d) | crisis-watch flag |
| Single mention reach > 1M | manual amplification or watch |
| Named-person mention | personal-comms protocol |
| Branded hashtag spike > 3x baseline | trend opportunity or threat |

### Tool comparison

| Tool | Strength | Weakness | Price tier |
|---|---|---|---|
| Brand24 | AI sentiment 2026 model, MCP server, SMB-friendly | source breadth narrower than Talkwalker | $199-$499/mo |
| Talkwalker (Hootsuite) | 30+ networks + 150M web sources; 5-year historical | enterprise pricing; learning curve | $$$ enterprise |
| Meltwater | TV + radio + podcast + print earned-media reach | overkill for purely social | $$$ enterprise |
| Mention | low-cost entry-tier | simpler features | $41+/mo |
| Awario | Boolean-search ops, dark-social capture | smaller AI-sentiment depth | $39+/mo |

---

## Trend monitoring playbook

> Grep target: "Trend monitoring playbook"

### Daily 9am cron job

1. `cli-anything curl https://www.tiktok.com/business/creativecenter/inspiration/popular/music` — top 20 trending sounds
2. `cli-anything curl https://tokchart.com/api/trending` — daily TikTok chart with delta
3. Filter by brand-fit (genre + tone + audience overlap)
4. Output: 3 accelerating / 3 declining / 1 unusual
5. Ship-by deadline per trend: 48 hours from emergence to publish

### Trend brief format

```markdown
# Trend Brief — [Date]

## Top accelerating (3)
1. [Sound name / hashtag] — Source: [URL] — Delta: +XX% vs yesterday — Brand fit: [why] — Ship-by: [date+time] — Hook idea: [1-line concept]
2. ...
3. ...

## Declining (3)
- Brief mention to avoid late adoption

## Unusual / Watch (1)
- [Out-of-genre signal worth noting]
```

### Trending audio 48-hour rule

- TikTok algorithm gives 3-5x algorithmic push to posts using sounds in their first 48 hrs of viral acceleration
- If a sound is at 50k uses and growing 30%/day → still in the window
- If a sound is at 500k uses and growing 5%/day → window closed; not worth adopting

---

## Reddit AMA playbook

> Grep target: "Reddit AMA playbook"

### Pre-AMA (7 days before)

- **Subreddit health audit**: subscribers (10k+) / recent post velocity / mod-removal rate / promotional-content policy
- **Schedule confirmation with mods** — most large subs require pre-approval
- **r/IAmA verification** if hosting there (proof photo / video required)
- **Cross-post announcement** to 3-5 niche subs 24-48 hrs before live window
- **First-15-min seed questions**: 3-5 friendly questions queued (NOT planted but anticipated)
- **Team coordination**: question-router + answer-drafter + cross-poster + comment-monitor

### Day-of (live window, 1-3 hrs)

- Top-of-thread comment: bio + verification + intro
- Set tone: enthusiastic, candid, brand-voice-clean
- Answer top-by-upvotes first
- Acknowledge controversies head-on if they arise — Reddit punishes evasion
- Live-log answers in `notion-mcp` AMA DB (Question / Answer / Upvotes / Sentiment / Followup)
- Reply velocity matters — 30+ answers in first hour signals "real" AMA

### Post-AMA (within 48 hrs)

- Top-10 Q&A digest → cross-post to LinkedIn / X thread / blog post
- Update site FAQ with new questions surfaced
- Thank-you message in thread + DM to mods
- Track: subscriber growth, mentions in other subs, click-throughs to brand

---

## Crisis comms playbook

> Grep target: "Crisis comms playbook"

### Detection thresholds

| Signal | Threshold | Action |
|---|---|---|
| Negative mention velocity | > 100/hr OR > 2x baseline | crisis-watch |
| Negative sentiment cluster reach | > 100k aggregate | crisis-watch |
| Named-person mention | any | personal-comms protocol |
| Customer harm mentions | any | legal hook + crisis-watch |
| Hashtag formation against brand | new + > 1k uses in 24h | crisis-watch + monitor |

### Response SLAs

| Phase | Window | Output |
|---|---|---|
| Acknowledge | < 60 min | "We're aware and looking into it" — owned channels |
| Position statement | < 4 hrs | Holding statement with key facts + timeline |
| Detailed response | < 24 hrs | Full statement: what happened / what we're doing / what's next |
| Follow-up | < 72 hrs | Resolution update or status report |

### Three-variant draft engine

For every crisis trigger, draft 3 statement variants:

1. **Apology** — when fault is clear; lead with accountability + concrete action
2. **Clarification** — when facts are being misrepresented; lead with what's accurate + verifiable detail
3. **Holding statement** — when facts still unclear; "We're investigating; will share details when confirmed" + timeline commitment

Show all 3 to user; ship the one matching the actual fact pattern after legal review (if applicable).

### Cascade

- Owned: website pinned banner + email opt-in alert + Buffer cascade to LinkedIn / X / IG / TikTok / Threads / Bluesky
- Earned: press release to top 5 outlets via Gmail outreach + journalist list from prior PR work
- Internal: Slack #all-hands message; CEO Loom video for staff (if material)

---

## Brand voice per platform (Vale style packs)

> Grep target: "Brand voice per platform"

### File structure

```
styles/
├── Brand/
│   ├── LinkedIn.yml    # formal-but-human, no slang, 1-3 emoji max
│   ├── X.yml           # punchy, contractions OK, 1-2 emoji
│   ├── TikTok.yml      # casual, on-trend slang, 3-5 emoji
│   ├── Threads.yml     # conversational, informal, 2-4 emoji
│   ├── Instagram.yml   # warm, narrative-friendly, 2-4 emoji
│   ├── Reddit.yml      # community-fluent, sub-specific vernacular, no #
│   └── Common.yml      # banned across all (corporate jargon, AI-slop)
└── .vale.ini
```

### Common (Vale rule pack — banned across all platforms)

- "leverage", "utilize", "synergize", "ideate", "circle back", "ping me"
- "In today's fast-paced world", "in a world where", "look no further", "without a doubt"
- "It's no secret that", "best-in-class", "game-changing" (unless specifying what changed)
- Excessive em-dashes (>1 per paragraph)
- "Great question!", "Certainly!", "Absolutely!" (sycophancy)
- Passive voice chains (>2 in a row)
- "Moreover", "Furthermore", "However" overuse (>2 in same post)

### LinkedIn-specific style pack additions

- No first-line "I'm humbled..." / "Excited to announce" without substance after
- No 5+ line first sentence — hook is one tight clause
- No spammy emoji rows (🚀🚀🚀)
- Tag people sparingly (1-3 max per post)

### X-specific style pack additions

- No 280-char wall-of-text without line breaks
- Hook in first 7 words
- Threads: one idea per post; numbered "1/" to "N/" optional but signals serial

### TikTok-specific style pack additions

- Caption keyword-front-loaded (TikTok SEO)
- On-screen text matches caption hook (TikTok OCR signal)
- 3-5 hashtags only; no #fyp

### Vale execution

```bash
uvx vale --config=.vale.ini --output=JSON --filter='.Level=="error"' content/post-linkedin.md
uvx vale --config=.vale.ini --output=JSON --filter='.Level=="error"' content/post-x.md
# zero errors = ship; any errors = revise
```

---

## UGC reposting workflow

> Grep target: "UGC reposting workflow"

### Discovery

- Brand24 mention feed (mentions + brand-hashtag uses + tagged-photos)
- Buffer mentions feed (per-channel comments + tags)
- Manual @search / hashtag-search per platform weekly

### Rights-request DM templates

**Instagram:**
> Hey [name]! Love this post 💛 We'd love to share it on our @[brand] account with full credit to you. Mind if we repost? Just reply with "yes" if you're cool with it. We'll tag you and link back.

**TikTok:**
> [name] this 👀 Mind if we share this on our @[brand] TikTok with credit? Reply "yes" if good with you!

**X:**
> Love this @[name] — mind if we share on our brand account with credit? Reply yes if OK!

### Notion UGC DB columns

`Source URL / Creator handle / Platform / Date discovered / Rights-request sent date / Rights-request status (pending/granted/denied/expired) / License window (perpetual / campaign-only / 30-day / 90-day) / Brand-fit score (1-10) / Repost date / Repost URL / Engagement (reach, likes, comments)`

### Repost copy template

```
[Quote-style caption riffing on the original]

[Attribution]: 📸 / 🎥 by @[creator handle] — thanks for sharing!

[Hashtag basket per platform spec]
```

### Disclosure

- Original creator attribution mandatory on every UGC repost
- For paid UGC (creator was compensated), add #ad / #sponsored per FTC

---

## Multi-platform campaign playbook

> Grep target: "Multi-platform campaign playbook"

### T-7 to T-0 (pre-launch week)

- Tease: 1-2 cryptic posts per platform; "something's coming" energy
- Email opt-in for early access (hand to `email-strategist` or `marketing-agent`)
- Influencer seeding: campaign brief sent to confirmed creators
- Asset finalization: per-platform variants in Buffer queue with approval state

### T-0 (launch day)

- 6+ platforms cascade in the same 2-hour window
- Pinned post on owned channels
- Influencer posts go live (coordinated calendar)
- Paid amplification kicks in (Meta + TikTok)
- Reddit AMA scheduled within first 24-48 hrs

### T+1 to T+7 (amplification)

- UGC discovery + repost workflow active
- Influencer post #2 / #3 per creator
- Repurpose top-performing content into Stories + Shorts + Threads
- Daily analytics check: reach, engagement, click, conversion per platform
- Mid-flight pivots: if hashtag dies, swap; if creator under-delivers, surface to `account-takeovers-creator-handoff`

### Campaign brief template

```markdown
# Campaign: [Name]

## Objective
- Primary: [reach / engagement / clicks / conversions / GMV]
- Success metric: [specific KPI with target]
- Kill criteria: [thresholds to pause/end]

## Channels and mix
- LinkedIn: [budget %, content type]
- X: [...]
- IG: [...]
- TikTok: [...]
- Threads: [...]
- Bluesky: [...]
- Reddit: [...]
- YouTube: [...]
- Pinterest: [...]

## Asset matrix
| Asset ID | Channel | Format | Variant | Status | Owner |
|---|---|---|---|---|---|
| A1 | LinkedIn | Carousel | Authority | Approved | @editor |
| A2 | TikTok | Video | Trend-audio | In review | @creator1 |

## Timeline
- T-7: Tease cascade
- T-3: Influencer briefs sent
- T-0: Launch
- T+1 to T+7: Amplification
- T+14: Retrospective

## Hashtag basket per platform
- [per-platform tag mix]

## Tracking
- UTM convention: utm_source/medium/campaign/content/term
- Attribution: PostHog UTM + native platform analytics

## Budget
- Total: $X
- Per channel: [breakdown]
- Influencer: $Y
- Paid boost: $Z
```

---

## Discord rule pack template

> Grep target: "Discord rule pack template"

```yaml
# Carl-bot YAML rule pack — paste into Carl-bot dashboard
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
    action_on_violation: delete + warn

  toxicity:
    enabled: true
    threshold: 0.8  # Perspective API toxicity score
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

---

## Slack rule pack template

> Grep target: "Slack rule pack template"

```yaml
# Slack workspace governance template
channels:
  general:
    purpose: "Brand-wide announcements only"
    posting: admin_only

  community:
    purpose: "Open community chat"
    posting: all_members

  introductions:
    purpose: "New-member intros"
    posting: all_members
    auto_thank: true

  feedback:
    purpose: "Product feedback to team"
    posting: all_members
    route_to: product@brand.com

  off-topic:
    purpose: "Non-brand chat"
    posting: all_members

moderation:
  banned_words: ["spam-pattern-1", "spam-pattern-2"]
  link_policy:
    block_unverified: true
    allowlist: ["brand.com", "github.com/brand"]
  toxicity_threshold: 0.8

onboarding:
  welcome_dm: |
    Welcome to the [brand] Slack!
    Check out #rules, intro yourself in #introductions, and join channels that interest you.

  rules_acknowledge_required: true
  channel_recommendation: ["community", "introductions"]
```

---

## Social commerce setup

> Grep target: "Social commerce setup"

### Shopify-hub-first architecture

1. Shopify catalog as single source of truth
2. Sync to Meta Catalog (Instagram Shop + Facebook Shops) via Meta Commerce Manager
3. Sync to TikTok Shop via TikTok Seller Center (manual or Shopify app)
4. Sync to Pinterest Shop via Pinterest Catalog API
5. Sync to YouTube Shopping via channel-to-Shopify integration

### TikTok Shop setup

1. Apply to TikTok Seller Center (1-4 week approval)
2. Verify business documents + tax info
3. Connect Shopify (TikTok Shop Shopify app)
4. Upload catalog (CSV or sync)
5. Live shopping setup if planning live commerce
6. **From July 2026**: budget 1.5-5% of GMV for GMV Max ads (mandatory)

### Product tagging workflow

- Every commerce post tags 1-3 products
- IG Graph API: `media.product_tags` field on creation
- TikTok: product tag via Shop module
- Pinterest: pin links directly to product page

### Attribution

- Native shop dashboards: TikTok Shop / Meta Commerce / Pinterest Analytics
- Cross-channel: UTM convention via `bitly-utm-campaign-tracking` (inherited from `marketing-agent`)
- PostHog MCP: `query` with HogQL to join social-attributed traffic to commerce conversion

---

## Success metrics

> Grep target: "Success metrics"

### Per-platform engagement

| Platform | Good | Great | Alert (under-performing) |
|---|---|---|---|
| LinkedIn | engagement rate 2-4% | > 5% | < 1% |
| X | engagement rate 1-2% | > 3% | < 0.5% |
| Instagram | engagement rate 3-5% | > 6% | < 2% |
| TikTok | engagement rate 5-9% | > 10% | < 3% |
| Threads | reply rate > follow rate (different dynamic) | viral chains | low reply rate |
| Bluesky | reply + repost engagement | active feed presence | crickets |
| Reddit | upvote ratio > 80% | > 90% | < 60% (mod-removal risk) |

### Growth metrics

- Follower growth: 5-10% MoM organic = healthy; 20%+ = on fire (or paid boost)
- Audience demographic shifts: track quarterly via native analytics + Audiense
- Share of voice (hashtag / brand-mention): track weekly via Brand24

### Community engagement metrics

- Comment reply rate: > 80% within SLA = healthy
- DM reply rate: > 90% within 4 hrs = healthy
- Mentions triaged daily: > 95% = healthy

### Influencer campaign metrics

- AQS distribution of partnered creators: median > 80
- Engagement rate on partnered posts: > 1.5x creator's baseline = strong fit
- Conversion attribution: native pixel + UTM
- ROI: revenue attributed / total campaign cost; target > 3x

### Crisis metrics

- Acknowledge SLA met: < 60 min
- Statement SLA met: < 4 hrs
- Sentiment recovery: negative-mention share back to baseline within 72 hrs

---

## SOTA tool reference (June 2026)

> Generated from `reference/SOTA_USE_CASES.md`. Each H3 maps to a bundled skill pack (Round 2 creates `SKILL.md` content; this references the name the agent greps for).

### Buffer cross-platform publishing

Buffer GraphQL + MCP server (May 2026 GA). One auth → cascade to LinkedIn / X / Threads / Bluesky / IG / TikTok / FB / Pinterest / Mastodon / YouTube Shorts with per-channel content variants. SOTA default for cross-platform publishing AND comment/DM engagement (via `getEngagements` API).

- **Skill pack:** `skills/community-engagement-comments-dms-at-scale/SKILL.md` (Round 2)
- **Endpoint:** `npx @buffer/mcp-server` or `https://graph.buffer.com/v1`
- **Auth:** `BUFFER_ACCESS_TOKEN`
- **Key calls:** `createUpdate({channels, perChannelContent, scheduledAt, needsApproval})`, `getEngagements({channel, since})`, `respondToEngagement({id, text})`
- **Source:** https://buffer.com/developers/api

### Brand24 social listening

Brand24 MCP launched Jan 2026. 25M+ sources, 2026 AI sentiment model (sarcasm-aware, regional slang, complex syntax). Best for SMB-to-mid-market listening; webhook fires on threshold breach for crisis-comms flow.

- **Skill pack:** `skills/social-listening-brandwatch-mention-talkwalker/SKILL.md`
- **Endpoint:** `npx @brand24/mcp-server` + `https://api.brand24.com/v3`
- **Auth:** `BRAND24_API_KEY` (paid plan $199+/mo)
- **Key calls:** `get_mentions({project_id, since})`, `get_sentiment_breakdown`, `subscribe_webhook({event: threshold_breach})`
- **Source:** https://brand24.com/

### Talkwalker (Hootsuite ecosystem)

SOTA enterprise listening. 30+ networks + 150M web sources, 5-year historical. Use when recipient has Hootsuite + Talkwalker enterprise.

- **Skill pack:** `skills/social-listening-brandwatch-mention-talkwalker/SKILL.md` (Talkwalker tier)
- **Endpoint:** `https://api.talkwalker.com/v1/`
- **Auth:** OAuth — `TALKWALKER_ACCESS_TOKEN`
- **Source:** https://www.talkwalker.com/

### Modash Discovery API

350M+ public creator profiles across IG / TikTok / YouTube with audience-quality heuristics. SOTA discovery for influencer outreach pipeline.

- **Skill pack:** `skills/influencer-outreach-modash-aspire-grin/SKILL.md`
- **Endpoint:** `https://api.modash.io/v1/discovery/search`
- **Auth:** `MODASH_KEY`
- **Key call:** `GET /discovery/search?filter[audience_country]=US&filter[engagement_rate][gte]=2`
- **Source:** https://www.modash.io/influencer-marketing-api/discovery

### HypeAuditor AQS

SOTA influencer fraud detection. AQS 1-100 score; 95%+ fraud detection rate; 53+ behavioral patterns. Gate every outreach at AQS ≥ 70.

- **Skill pack:** `skills/influencer-fraud-detection-hypeauditor/SKILL.md`
- **Endpoint:** `https://api.hypeauditor.com/v1/instagram/account?username=<handle>`
- **Auth:** `HYPEAUDITOR_KEY`
- **Source:** https://hypeauditor.com/

### TikTok Creative Center + Tokchart (trend monitoring)

Daily trending sounds + hashtags. 48-hour adoption window for 3-5x algorithmic push. Tokchart provides daily TikTok chart with delta.

- **Skill pack:** `skills/social-trend-monitoring-tiktok-sounds-reels/SKILL.md`
- **Endpoints:** `https://www.tiktok.com/business/creativecenter` + `https://tokchart.com/api/trending`
- **Auth:** none (public)
- **Source:** https://www.tiktok.com/business/creativecenter

### TikTok Shop API

SOTA social commerce on TikTok. Catalog sync, orders, inventory, ads. From July 2026: 1.5-5% GMV Max budget mandatory.

- **Skill pack:** `skills/social-commerce-tiktok-instagram-pinterest-shops/SKILL.md`
- **Endpoint:** `https://open-api.tiktokglobalshop.com/`
- **Auth:** TikTok Seller OAuth
- **Source:** https://developers.tiktok.com/doc/research-api-specs-query-tiktok-shop-info?enter_method=left_navigation

### Instagram Graph API (Shop + Reels + comments)

SOTA Instagram surface for Business accounts. Product tagging on posts/Reels, comment management, Reels publishing, Stories.

- **Skill pack:** `skills/social-commerce-tiktok-instagram-pinterest-shops/SKILL.md` (IG tier)
- **Endpoint:** `https://graph.facebook.com/v20.0/`
- **Auth:** Meta OAuth — `META_GRAPH_TOKEN`
- **Native MCP:** `insta-business-mcp` already in agent.yaml

### Pinterest Shop API

SOTA Pinterest commerce. Pin → product link, Shopping ads, catalog upload.

- **Skill pack:** `skills/social-commerce-tiktok-instagram-pinterest-shops/SKILL.md` (Pinterest tier)
- **Endpoint:** `https://api.pinterest.com/v5/`
- **Auth:** OAuth — `PINTEREST_ACCESS_TOKEN`

### Linktree API (link-in-bio)

SOTA link-in-bio with REST API. Beacons + Stan are Playwright fallback.

- **Skill pack:** `skills/link-in-bio-linktree-beacons-stan/SKILL.md`
- **Endpoint:** `https://api.linktree.com/v1/`
- **Auth:** `LINKTREE_TOKEN`

### Carl-bot + MEE6 (Discord moderation)

SOTA Discord moderation. Carl-bot most trusted; MEE6 21M+ servers; Dyno for moderation primitives. YAML rule packs deployed via dashboards or `cli-anything` OAuth flow.

- **Skill pack:** `skills/discord-slack-community-moderation/SKILL.md`
- **Native MCPs:** `discord-mcp`, `discord-mcp-full`, `slack-mcp` (in agent.yaml)
- **Source:** https://blog.communityone.io/best-discord-bots/

### Reddit official API + Reddit MCP

SOTA Reddit publishing + AMA + community insight. Reddit MCP in CraftBot catalog. Subreddit health scoring via `about.json` endpoint.

- **Skill pack:** `skills/reddit-strategy-ama-subreddit/SKILL.md`
- **Native MCP:** `reddit-mcp` (in agent.yaml)
- **Endpoint:** `https://www.reddit.com/api/v1/`

### Vale linter (per-platform brand voice)

SOTA brand voice enforcement. Per-platform YAML rule packs (LinkedIn / X / TikTok / Threads / IG / Reddit / Common). 60% of marketing materials fail brand guidelines without enforcement.

- **Skill pack:** `skills/brand-voice-consistency-platforms/SKILL.md`
- **Tool:** `uvx vale --config=.vale.ini --output=JSON`
- **Source:** https://vale.sh/

### Native platform MCPs

Direct platform publishing and engagement when Buffer doesn't expose a needed feature:

- `twitter-mcp` — X post, thread, reply
- `insta-business-mcp` — IG post, Reel, Stories, product tags
- `facebook-mcp-server` — FB page, groups
- `tiktok-mcp` — TikTok post, trending discovery
- `reddit-mcp` — Reddit post, AMA, comments
- `youtube-mcp` + `youtube-mcp-transcript` — YouTube Community Posts, Shorts metadata, transcripts
- `bilibili-mcp` — Bilibili (China)
- `whatsapp-mcp` — WhatsApp Business broadcast + catalog
- `wechat-mcp` — WeChat Official Account
- `line-mcp` — LINE Business

### Listening + competitive intelligence MCPs

- `firecrawl-mcp` — competitor social-page structured pull
- `brightdata-mcp` — TikTok / IG scraping fallback when official APIs gated
- `brave-search` — query-based competitive monitoring

### Asset generation MCPs

- `canva-mcp` — platform-native templates (Reels covers, Pinterest pins, carousel)
- `figma-mcp` — design system asset pulls for brand-consistent visuals
- `imagegen-mcp` + `stability-ai-mcp` — AI image gen for posts and carousels

### Commerce hub

- `shopify-mcp` — catalog hub for TikTok Shop / IG Shop / Pinterest Shop sync

### Multi-language

- `deepl-mcp` — post translation for multi-market publishing; cross-checked with brand voice per-language Vale pack

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Publish this across all our channels" | `community-engagement-comments-dms-at-scale` (Buffer cascade) | Falls to native MCPs for advanced format-specific features |
| "Reply to all our comments and DMs from yesterday" | `community-engagement-comments-dms-at-scale` | SLA matrix in role.md |
| "Who's saying what about us this week?" | `social-listening-brandwatch-mention-talkwalker` + `sentiment-mention-triage` | Brand24 MCP / Talkwalker fallback |
| "Find me 50 micro-influencers in the fitness space" | `influencer-outreach-modash-aspire-grin` | Modash Discovery + HypeAuditor AQS 70+ gate |
| "Are these influencers legit?" | `influencer-fraud-detection-hypeauditor` | AQS 70 threshold; reject below |
| "What trending sounds should we use this week?" | `social-trend-monitoring-tiktok-sounds-reels` | 48-hour adoption window |
| "Build us hashtag baskets for IG + TikTok" | `hashtag-strategy-trending-niche-branded` | 30-tag basket spec |
| "Set up our TikTok Shop / IG Shop" | `social-commerce-tiktok-instagram-pinterest-shops` | Shopify hub + per-platform sync |
| "Refresh our Linktree" | `link-in-bio-linktree-beacons-stan` | Linktree API or Playwright |
| "Plan an AMA on r/IAmA" | `reddit-strategy-ama-subreddit` | Subreddit health + 7-day prep |
| "Moderate our Discord better" | `discord-slack-community-moderation` | Carl-bot + YAML rule pack |
| "Make sure our copy is on-brand for each platform" | `brand-voice-consistency-platforms` | Vale per-platform style packs |
| "Help us go viral / grow followers" | `follower-growth-organic` | Trend first-mover + cadence + collab |
| "There's a crisis — help" | `social-crisis-comms` | 3-variant draft engine + cascade |
| "Our customer is angry on Twitter — help" | `social-customer-service-handoff` | 15-min SLA + route to support |
| "Coordinate this big launch across all platforms" | `multi-platform-campaign-launches` | T-7 / T-0 / T+7 |
| "Set up UGC reposting" | `ugc-reposting-policy-workflow` | Rights-request workflow |
| "Hand the account over to a creator for a takeover" | `account-takeovers-creator-handoff` | Buffer approval + token revoke |
| "Coordinate our 5-person social team" | `team-admin-coordination` | Buffer approval + Notion + Slack |

---

## Influencer brief / output templates

> Grep target: "Influencer brief templates"

(See `Influencer outreach playbook` above for the full brief template.)

### Outreach email template

```
Subject: Quick collab idea — [brand] x [creator handle]

Hi [first name],

Just watched [specific recent post] — [concrete reason it caught us, brand-relevant].

We're [brand]. We're launching [campaign] and looking for [N] creators who actually use [product/service category]. Your audience overlap with ours looks strong: [data point — e.g., "62% women 25-34 in fitness niche, per Modash"].

If you're booking [time window]:
- Deliverable: [1 Reel + 3 Stories] over [campaign window]
- Compensation: $[X] flat OR rate-card if higher
- Usage rights: [organic + paid boost for 30 days]
- Disclosure: #ad / #sponsored
- Approval: light pre-approval pass; not gate-keeping your voice

Two paths to yes:
1. Email me back with "interested" + your rate if higher
2. Book here: [calendar link]

Want to send specs / contract / mood board the moment you're in.

Thanks,
[your name]
```

### Influencer brief one-pager

```markdown
# [Brand] Collab Brief — [Creator handle]

## The product
- What it is: [1 sentence]
- Why audiences love it: [1 sentence + proof point]
- Brand voice: [1-3 adjectives + link to voice doc]

## The ask
- N posts: [breakdown by format]
- Hashtags: [#brand #campaign #ad]
- Caption: [creator's voice; light suggested hooks below]
- Visual direction: [mood board link + product mailer status]
- Posting window: [date range]
- Approval flow: [pre-approval or post]

## What's off-limits
- Don't use [competitor brand] mentions
- Don't make medical / financial claims about [product]
- Don't tag [bad-actor accounts]

## Suggested hooks (creator can riff)
1. [hook 1 — for trending audio fit]
2. [hook 2 — for product-feature angle]
3. [hook 3 — for community-vibe angle]

## Tracking + payment
- UTM tracking link: [link]
- Discount code: [code] (creator gets X% on conversions)
- Payment: 50% upfront / 50% post-publish; 30-day net

## Contact
- Manager: [name + email]
- Brand voice questions: [name]
```

---

## Closing rules

Social is two-way; platform-native beats repurposed; comments are content too. The agent publishes, listens, replies, routes — not just drafts. Defers cleanly when depth is required (video-creator, customer-support-agent, marketing-agent for broader strategy).
