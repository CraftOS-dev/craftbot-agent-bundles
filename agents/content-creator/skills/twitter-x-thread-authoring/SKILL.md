# X / Twitter Thread Authoring — Typefully Agent CLI + Cross-Publish Cascade

> Write 7+ scroll-stopper threads and cascade to X / LinkedIn / Threads / Bluesky / Mastodon via Typefully.

## When to use

Trigger on: "write me an X thread", "Twitter thread", "thread on this topic", "cascade this thread", "Typefully this", "rule of 7 thread". This skill owns: thread structure (1/n thesis → body → CTA), rule-of-7 scroll-stoppers, Typefully agent CLI cross-publish, single-tweet vs thread decision. For single-tweet posts use `twitter-mcp` directly; for LinkedIn-only carousels see `linkedin-carousel-authoring`. Typefully cross-publishes to X + LinkedIn + Threads + Bluesky + Mastodon in one auth.

## Setup

```bash
# Typefully agent CLI
npm i -g @typefully/cli
# or one-shot:
npx typefully --help

# Twitter MCP for non-thread X publishing
npx -y @twitter/mcp-server@latest
```

Auth env vars:
- `TYPEFULLY_API_KEY` — Typefully account → settings → API key. Free plan = 3 drafts/day, Pro = unlimited.
- `TWITTER_ACCESS_TOKEN` — X / Twitter API v2 OAuth 2.0 PKCE token; only needed for direct twitter-mcp calls (Typefully handles its own auth).
- `LINKEDIN_ACCESS_TOKEN` — for direct LinkedIn publish if not via Typefully.
- `BLUESKY_HANDLE` + `BLUESKY_APP_PASSWORD` — for ATproto auth (Typefully handles natively).

## Common recipes

### Recipe 1: Thread template (the deliverable)

```markdown
# Thread: <working title>
**Length:** 8 / 10 / 12 / 14 tweets
**Hook style:** Surprising stat | Contrarian | Specific outcome | Story | Question

## 1/n THESIS TWEET (≤280 chars)
<single-line hook + (1/n) indicator + visual if relevant>

Example: "Open rates are the most lied-about metric in newsletters. After Apple MPP, they're ~75% noise. Here's what to track instead — and the math behind why. (1/12)"

## 2/n CONTEXT (≤280 chars)
<1-2 sentences setting up the proof>

## 3/n — N-1/n BODY (≤280 chars each)
<one specific claim per tweet + 1-line proof; scroll-stopper every 2-3 tweets>

## N/n CTA TWEET (≤280 chars)
<explicit ask: retweet, follow, link to newsletter / podcast / lead magnet>

Example: "If you found this useful, hit ❤ on tweet 1 — it tells the algo to show more nerdy newsletter ops takes. Newsletter (deeper takes, free): <URL> (12/12)"
```

### Recipe 2: Rule of 7 — scroll-stoppers

```markdown
A thread needs 7+ scroll-stopper moments across its length. One every 2-3 tweets.

Scroll-stopper types:
1. Surprising stat — "75% of Apple Mail opens are background prefetches"
2. Contrarian claim — "Everyone tracks opens. They're wrong."
3. Specific anecdote — "I tested 30 ESPs across 5 cohorts. Here's what broke."
4. Screenshot — image of CTR dashboard, before/after, redacted email
5. Before / after comparison — "Before MPP: 38% open rate, real engagement signal. After MPP: 65% open rate, mostly noise."
6. Question to the reader — "When's the last time YOU clicked an email from open-rate enthusiasm?"
7. Emoji-bullet list — "→ Track CTR → Track CTOR → Track revenue per recipient"
8. "But here's the catch" reframe — "The metric you're missing is..."

Without scroll-stoppers, readers drop after tweet 3. With 7+, completion rate is 4-5×.
```

### Recipe 3: Typefully draft via CLI

```bash
# Draft a thread (interactive — opens editor)
npx typefully draft

# Draft from file (non-interactive)
npx typefully draft \
  --content-file thread.md \
  --account "@yourhandle"

# Auto-split: Typefully splits long text into 280-char tweets with `\n\n` boundaries respected
```

### Recipe 4: Cross-publish cascade

```bash
# One Typefully draft → publishes to multiple platforms
npx typefully publish \
  --content-file thread.md \
  --account "@yourhandle" \
  --cross-publish "x,linkedin,threads,bluesky,mastodon" \
  --schedule "2026-06-17T14:00:00Z"

# Per-platform behavior:
# - X / Twitter: native thread (each tweet a reply)
# - LinkedIn: collapsed into single long-form post
# - Threads: native thread
# - Bluesky: native thread, character-limit refit per tweet (300 chars vs X's 280)
# - Mastodon: native thread; per-instance char limits respected
```

### Recipe 5: Auto-split text → thread

```bash
# Paste any long-form text; Typefully auto-splits into 280-char tweets
echo "Open rates are the most lied-about metric in newsletters. After Apple MPP, they're ~75% noise. Here's what to track instead — and the math behind why. CTR is the only metric that survives MPP. Click-through rate is clicks divided by sends. Apple can't fake clicks. Apple can fake opens. The math: ..." | npx typefully draft --auto-split
```

### Recipe 6: Schedule for SOTA timing

```bash
# SOTA thread timing:
# - Mon 8am ET (thread-default day)
# - Tue/Wed 10am ET
# - Avoid Fri 4pm ET → Sunday (algorithm-suppressed)

npx typefully publish \
  --content-file thread.md \
  --schedule "2026-06-23T12:00:00Z"  # Monday 8am ET
```

### Recipe 7: Programmatic Typefully via REST API

```bash
# Direct API (skip the CLI wrapper)
curl -X POST https://api.typefully.com/v1/drafts/ \
  -H "X-API-KEY: $TYPEFULLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Open rates are the most lied-about metric.\n\n75% are MPP noise.\n\nHere'\''s what to track instead.\n\n(1/12)\n\nCTR is the only metric that survived MPP.\n\nClicks / sends.\n\nApple can'\''t fake clicks.\n\n(2/12)\n\n...",
    "threadify": true,
    "schedule-date": "2026-06-23T12:00:00Z",
    "share": true,
    "auto_retweet_enabled": true,
    "auto_plug_enabled": false
  }'
```

### Recipe 8: Auto-plug (post-thread CTA tweet)

```bash
# Configure auto-plug: a reply tweet auto-appended N hours after the thread publishes
curl -X POST https://api.typefully.com/v1/drafts/ \
  -H "X-API-KEY: $TYPEFULLY_API_KEY" \
  -d '{
    "content": "Thread body here...",
    "threadify": true,
    "auto_plug_enabled": true,
    "auto_plug": {
      "delay_minutes": 60,
      "content": "If this was useful, my newsletter goes deeper every Tuesday: <URL>"
    }
  }'
```

### Recipe 9: Castmagic / newsletter → thread

```bash
# Castmagic 'x_thread' derivative from podcast or newsletter source
THREAD_TEXT=$(curl -H "Authorization: Bearer $CASTMAGIC_API_KEY" \
  "https://api.castmagic.io/v1/uploads/$UPLOAD_ID/derivatives" | jq -r '.x_thread')

echo "$THREAD_TEXT" | npx typefully draft --auto-split --schedule "2026-06-23T12:00:00Z"
```

### Recipe 10: A/B hook test

```bash
# Two threads, same body, different hooks; publish 1 week apart
HOOKS=("Open rates lie. Here's the math." "After Apple MPP, 75% of opens are noise. Here's what survived.")

for i in "${!HOOKS[@]}"; do
  cat > thread_v$i.md <<EOF
${HOOKS[$i]}

(1/12)

<rest of thread body identical>
EOF
  npx typefully publish --content-file thread_v$i.md --schedule "2026-06-$((23+i*7))T12:00:00Z"
done

# Compare bookmarks + reposts to identify winning hook style
```

### Recipe 11: Bookmark-worthy thread structure

```markdown
# Bookmark-worthy threads share three traits:

1. **Tactical specificity** — "Use ffmpeg loudnorm with I=-16 TP=-1 LRA=11" (vs "use ffmpeg")
2. **Concrete numbers** — "I tested 30 ESPs across 5 cohorts" (vs "I tested some ESPs")
3. **Save-as-reference structure** — listicle, checklist, comparison table

Bookmark rate >3% = high-quality thread; track via X analytics.
```

### Recipe 12: Reply to your own thread for engagement boost

```bash
# Reply to your own thread 6-12 hours after publish with a "P.S." that adds new value
# This signals algo: "engagement is still alive on this thread" → boosts in feed
# Typefully supports scheduled self-replies via the auto-plug mechanism (Recipe 8)
```

## Examples

### Example 1: Thread cascade from newsletter

**Goal:** Tuesday newsletter publishes; Wednesday a 12-tweet thread distilling the thesis cascades to X / LinkedIn / Threads / Bluesky / Mastodon.

**Steps:**
1. Tuesday: newsletter publishes via `long-form-newsletter-substack-beehiiv-ghost`.
2. Tuesday PM: Castmagic generates x_thread derivative (Recipe 9).
3. Vale-scrub the thread for AI-slop.
4. Recipe 2: confirm 7+ scroll-stoppers present.
5. Recipe 6: schedule Wed 10am ET cross-publish via Recipe 4.
6. Recipe 8: configure auto-plug for newsletter sign-up 60 minutes after publish.
7. Thursday: pull engagement stats (bookmarks, reposts, profile clicks).

**Result:** Thread compounds newsletter reach across 5 platforms in 24h.

### Example 2: Stand-alone original thread (no source content)

**Goal:** Original Tuesday thread on a hot take that doesn't have a tentpole behind it.

**Steps:**
1. Recipe 1: write thread in template.
2. Recipe 2: scroll-stopper audit; add stat in tweet 3, screenshot in tweet 6, reframe in tweet 9.
3. Recipe 3: Typefully draft via CLI; review auto-split.
4. Recipe 6: Tuesday 10am ET schedule.
5. Recipe 12: schedule self-reply for Tuesday 6pm ET with "P.S." tweet.

**Result:** Stand-alone thread with manufactured engagement waves.

### Example 3: Series of 5 threads matching a 5-week content series

**Goal:** Each week of a 5-week series, publish a companion thread.

**Steps:**
1. Pre-write all 5 threads at series kickoff (use `brainstorming` + Claude long-context).
2. Recipe 10: A/B hook styles across the 5; identify winning style by week 3.
3. Recipe 4: schedule all 5 in Typefully at once.
4. Recipe 9: each week, swap in any Castmagic-generated quotes from that week's podcast/newsletter.

**Result:** 5-week thread series synchronized with content series.

## Edge cases / gotchas

- **Free Typefully = 3 drafts/day.** Production cadence needs Pro ($12/mo).
- **X Premium = 500-char tweets**; 280 still default. If your audience is mostly Premium, you can write longer per-tweet but body tweets still hit harder at 220-240 chars.
- **Threads (Meta) auto-thread feature ≠ Typefully thread** — Threads native lets you write a single long post; Typefully splits into proper thread.
- **Bluesky char limit is 300** — Typefully refits automatically but check.
- **Mastodon per-instance limits vary** — some are 500, some 1000. Typefully respects per-instance.
- **LinkedIn collapses thread to single post.** This is correct for LinkedIn audience but check rendering.
- **Don't reply to your own thread within 5 minutes** — algo treats as spam. Wait 6+ hours.
- **Self-quote-tweet at +24h** with extra context to re-surface in feed.
- **Don't thread-jack** — replying to a popular tweet with your own thread is heavily downranked.
- **Image attached to tweet 1** boosts scroll-stop 2-3×. But the image must be relevant; meme images underperform contextual screenshots.
- **CTA tweet (final) must have explicit ask.** "Thanks for reading" tanks engagement; "Hit ❤ on tweet 1 if this was useful" works.
- **Bookmark rate >3% is the high-quality threshold.** Track via X analytics; bookmarks are stronger signal than likes.
- **Auto-retweet** (Typefully) re-shares your own thread 12-24h after publish for visibility wave. Use sparingly (not every thread).
- **First tweet of a thread is the entire thread's hook.** Spend 70% of authoring time there.
- **Thread quality > frequency** — 1 great thread/week > 5 mediocre threads/week.
- **Don't thread on a hot political topic without a strong stake** — toxic reply rate cratics your reach permanently.

## Sources

- [Typefully + agent CLI](https://typefully.com/x-twitter)
- [Typefully API docs](https://help.typefully.com/en/articles/8718287-typefully-api)
- [Posteverywhere — Best X schedulers 2026](https://posteverywhere.ai/blog/best-x-twitter-scheduler)
- [Bluesky ATproto docs](https://atproto.com/)
- [Threads (Meta) developer guide](https://developers.facebook.com/docs/threads)
- [X API v2 docs](https://developer.x.com/en/docs/x-api)
- [Castmagic API](https://docs.castmagic.io/)
