# Long-Form Newsletter — Beehiiv / Substack / Ghost / Kit

> Publish, analyze, and grow long-form newsletter issues across the 2026 SOTA newsletter stack.

## When to use

Reach for this skill when the user says any of: "write me a newsletter", "publish to my Beehiiv / Ghost / Substack / Kit", "draft the next issue", "schedule the Tuesday send", "pull subscriber stats", "audit my last issue", "migrate from Substack to Beehiiv". This skill owns drafting + publishing + post-publish analytics for the four major 2026 newsletter platforms. Do NOT use this skill for raw subscriber-growth tactics (use `newsletter-subscriber-growth`), for embedded surveys (use `newsletter-audience-survey`), or for cross-platform thread/social cascades (use `repurposing-pipeline-1-to-10` + `twitter-x-thread-authoring`).

## Setup

```bash
# Beehiiv MCP (read-only V1; GA March 24 2026)
npx -y @beehiiv/mcp-server@latest --help

# Ghost Admin API client (full write)
npm i -g @tryghost/admin-api
# or use raw curl + JWT (see Recipe 3)

# Kit (ConvertKit) — pure REST, no client needed
# uvx or curl works fine

# Substack — no public API. Use firecrawl-mcp for scrape; manual paste for publish.
```

Auth env vars:

- `BEEHIIV_API_KEY` — settings → integrations → API. **Paid plan only** (Scale tier minimum).
- `BEEHIIV_PUBLICATION_ID` — `pub_xxx` from `GET /publications`.
- `GHOST_ADMIN_URL` — `https://yoursite.ghost.io` (no trailing slash).
- `GHOST_ADMIN_KEY` — `<id>:<secret>`. Admin → integrations → custom integration → admin API key.
- `KIT_API_KEY` + `KIT_API_SECRET` — Kit account → advanced. Free plan covers most read ops; broadcast send needs Creator Pro.
- `SUBSTACK_SESSION_COOKIE` — optional; needed only for scrape via `firecrawl-mcp` of paid-only newsletters.

## Common recipes

### Recipe 1: Pull Beehiiv subscriber + post analytics via MCP

```bash
# One-off query via MCP CLI
npx @beehiiv/mcp-server query \
  --tool get_publication_analytics \
  --args '{"publication_id":"'"$BEEHIIV_PUBLICATION_ID"'","range":"last_30_days"}'

# Per-post analytics (CTR, CTOR, revenue per recipient)
npx @beehiiv/mcp-server query \
  --tool get_post_analytics \
  --args '{"publication_id":"'"$BEEHIIV_PUBLICATION_ID"'","post_id":"post_xxx"}'

# Subscriber growth + churn
npx @beehiiv/mcp-server query \
  --tool get_subscriptions \
  --args '{"publication_id":"'"$BEEHIIV_PUBLICATION_ID"'","status":"active","limit":1000}'
```

V1 is read-only. For writes, use Beehiiv's REST API directly (Recipe 2).

### Recipe 2: Beehiiv direct REST (POST a draft issue)

```bash
curl -X POST "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/posts" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY" \
  -H "Content-Type: application/json" \
  -d @issue.json
```

`issue.json`:

```json
{
  "title": "Why Tuesday-6am beats Sunday-night",
  "subtitle": "30 ESPs, 5 cohorts, one boring conclusion",
  "thumbnail_url": "https://cdn.example.com/issue-042-hero.png",
  "content": {"free": {"html": "<h1>...</h1>"}, "premium": {"html": "<h1>...</h1>"}},
  "status": "draft",
  "audience": "free",
  "platform": "both",
  "email_settings": {
    "preheader_text": "Plus: the one analytics trap every newsletter operator falls for",
    "from_name": "Operator Weekly"
  }
}
```

To schedule send, PATCH `status` to `scheduled` with `scheduled_at` (ISO8601 UTC).

### Recipe 3: Ghost Admin API — POST + publish + email-send

```bash
# 1. Mint a short-lived JWT from GHOST_ADMIN_KEY
KEY_ID="${GHOST_ADMIN_KEY%%:*}"
KEY_SECRET="${GHOST_ADMIN_KEY##*:}"
TOKEN=$(python3 -c "
import jwt, time
print(jwt.encode({'iat': int(time.time()), 'exp': int(time.time())+300, 'aud': '/admin/'},
  bytes.fromhex('$KEY_SECRET'), algorithm='HS256', headers={'kid':'$KEY_ID'}))
")

# 2. POST the post (draft)
curl -X POST "$GHOST_ADMIN_URL/ghost/api/admin/posts/?source=html" \
  -H "Authorization: Ghost $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"posts":[{
    "title": "Why Tuesday-6am beats Sunday-night",
    "html": "<p>Hook paragraph...</p>",
    "status": "draft",
    "email_only": false,
    "tags": ["operator-notes"],
    "newsletter": {"id":"<newsletter_id>"}
  }]}'

# 3. Schedule send (PUT publish at)
curl -X PUT "$GHOST_ADMIN_URL/ghost/api/admin/posts/<post_id>/" \
  -H "Authorization: Ghost $TOKEN" \
  -d '{"posts":[{"status":"scheduled","published_at":"2026-06-16T10:00:00.000Z","email_recipient_filter":"all","updated_at":"<current_updated_at>"}]}'
```

Ghost requires `updated_at` to match the server's current value (optimistic-lock). Pull it via `GET /posts/<id>/` first.

### Recipe 4: Kit broadcast (full write)

```bash
# Create broadcast (draft state)
curl -X POST "https://api.convertkit.com/v3/broadcasts" \
  -d "api_secret=$KIT_API_SECRET" \
  -d "subject=Why Tuesday 6am beats Sunday night" \
  -d "content=<p>Hook paragraph...</p>" \
  -d "description=Issue 042" \
  -d "preview_text=Plus: the one analytics trap..."

# Returns {"broadcast":{"id": 9876543, ...}}

# Send (or schedule via send_at)
curl -X POST "https://api.convertkit.com/v3/broadcasts/9876543/send" \
  -d "api_secret=$KIT_API_SECRET"
```

For tag-segmented sends, pre-create a segment via `POST /tags` + `POST /broadcasts` with the `subscriber_filter` field referencing the tag ID.

### Recipe 5: Substack stats via firecrawl-mcp (no public API)

```bash
# Substack exposes a public stats page at /publish/stats (logged-in)
# Use firecrawl-mcp with SUBSTACK_SESSION_COOKIE
npx @firecrawl/mcp scrape \
  --url "https://yoursubstack.substack.com/publish/post/<post-id>/stats" \
  --headers '{"Cookie":"substack.sid='"$SUBSTACK_SESSION_COOKIE"'"}' \
  --output stats.json

# Extract opens / clicks / paid conversions from the parsed HTML
jq '.openRate, .clickRate, .paidConversions' stats.json
```

Substack stats are scrape-only; refresh weekly into Notion/PostgreSQL.

### Recipe 6: Vale slop scrub before publish

```bash
uvx vale --config=.vale.ini --output=JSON content/issue-042.md \
  | jq '.[]|.[]|{Check,Severity,Message,Line}'
```

`.vale.ini` should reference the AI-slop catch list from role.md (banned openers, leverage→use, em-dash storms, sycophancy). Bounce the issue back to draft if any `error`-severity hit.

### Recipe 7: Mobile-render QA via playwright-mcp

```bash
npx @playwright/mcp navigate \
  --url "https://yoursite.ghost.io/p/issue-042-preview-token/" \
  --viewport "375x812" \
  --screenshot issue-042-iphone.png
```

Eyeball the screenshot in iPhone viewport. Litmus / Email on Acid are the paid alternatives but Playwright covers 90% of catches.

### Recipe 8: A/B subject line test (Beehiiv)

```bash
curl -X POST "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/posts" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY" \
  -d '{
    "title": "Variant A: 30 ESPs, one boring conclusion",
    "subject_line_split_test": {
      "enabled": true,
      "subject_line_b": "Variant B: Why Tuesday-6am beats Sunday-night",
      "split_pct": 20,
      "winner_metric": "open_rate"
    }
  }'
```

20% of list gets the split; winner sends to the remaining 80% after 2 hours.

### Recipe 9: Migrate Substack → Beehiiv

```bash
# 1. Export Substack subscribers
# Substack dashboard → Subscribers → Export CSV (manual)

# 2. Import into Beehiiv via Subscriptions API
curl -X POST "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/subscriptions" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email":"sub@example.com","reactivate_existing":false,"send_welcome_email":false,"utm_source":"substack-migration"}'

# Batch via xargs / loop for the CSV
xargs -a subs.csv -I{} curl -X POST ... -d '{"email":"{}"}'
```

### Recipe 10: Roll up cross-platform analytics into Notion

```bash
# Fetch Beehiiv → Notion analytics dashboard row
BEEHIIV_CTR=$(npx @beehiiv/mcp-server query --tool get_post_analytics --args '{"post_id":"<id>"}' | jq .click_rate)
GHOST_OPENS=$(curl -s -H "Authorization: Ghost $TOKEN" "$GHOST_ADMIN_URL/ghost/api/admin/posts/<id>/email/" | jq .emails[0].opened_count)

# Push to Notion editorial DB
npx @notionhq/mcp create_page \
  --database_id "$NOTION_EDITORIAL_DB" \
  --properties '{"Issue":{"title":[{"text":{"content":"Issue 042"}}]},"CTR":{"number":'"$BEEHIIV_CTR"'},"Opens":{"number":'"$GHOST_OPENS"'}}'
```

## Examples

### Example 1: End-to-end weekly issue → Beehiiv send

**Goal:** Draft, scrub, schedule Issue 042 to free + premium for Tuesday 6am ET send.

**Steps:**
1. Draft markdown using role.md newsletter issue template; save as `content/issue-042.md`.
2. Run Vale: `uvx vale content/issue-042.md` — fix any errors flagged.
3. Convert to HTML: `pandoc content/issue-042.md -o issue-042.html`.
4. POST draft via Recipe 2; capture `post_id`.
5. Mobile-render QA via Recipe 7 against the Beehiiv preview URL.
6. PATCH `status=scheduled`, `scheduled_at=2026-06-16T10:00:00Z`.
7. Day-of-send: at +24h, run Recipe 1 to capture analytics into Notion (Recipe 10).

**Result:** Issue published, analytics-tracked, derivatives queued via `repurposing-pipeline-1-to-10`.

### Example 2: Ghost member-only paid issue with email-recipient filter

**Goal:** Publish a deep-dive analysis behind a paid-tier paywall, send to paid members only.

**Steps:**
1. Author markdown with `<!--members-only-->` divider where the paywall should drop.
2. POST via Recipe 3 with `visibility: "paid"` and `email_recipient_filter: "status:-free"`.
3. Confirm tier-gating by hitting the post URL while logged out.

**Result:** Free preview above the fold; full body emailed and visible only to paid tier.

### Example 3: Migrate from Substack to Beehiiv preserving paid subs

**Goal:** Move 8k free + 400 paid Substack subs to Beehiiv without losing paid status.

**Steps:**
1. Export both CSVs from Substack dashboard.
2. POST free list via Recipe 9 batched loop, marking `utm_source=substack-migration`.
3. POST paid list using `tier: <beehiiv_paid_tier_id>` in the body; map Stripe customer IDs over.
4. Send a one-time welcome explaining the platform move.
5. Schedule Substack final issue announcing the move with a clickable link to confirm.

**Result:** 95%+ free-list retention; paid sub continuity via Stripe customer ID preservation.

## Edge cases / gotchas

- **Beehiiv MCP V1 is read-only.** Drafting and sending requires direct REST. V2 write capabilities not yet shipped as of June 2026.
- **Beehiiv MCP requires paid plan.** Free Beehiiv accounts can't use the MCP; Scale tier minimum (\$42/mo at 10k subs in 2026).
- **Ghost JWT expires in 5 minutes.** Mint per-request; don't cache.
- **Ghost `updated_at` optimistic-lock** — fetch current value before any PUT.
- **Kit free plan caps broadcasts** — for production cadence, Creator Pro is required.
- **Substack has NO public API.** Stats and content extraction is firecrawl-mcp scrape only; will break if Substack changes its DOM.
- **Beehiiv `subject_line_split_test`** can't be combined with `audience: premium` — splits only run against free lists.
- **Apple MPP (Mail Privacy Protection) inflates open rates.** Quote CTR/CTOR instead. Beehiiv's `open_rate` includes MPP unless you set `exclude_apple_mpp: true` in analytics queries.
- **One-click unsubscribe (RFC 8058)** is auto-added by all four platforms; don't override the header.
- **SPF/DKIM/DMARC must validate** — Beehiiv and Ghost let you bring your own sending domain; misconfigured DMARC tanks deliverability silently. Verify via `dig TXT _dmarc.yourdomain.com`.
- **Rate limits**: Beehiiv 60 req/min; Ghost 100 req/min default; Kit 600 req/min; Substack scrape — limit yourself to 1 req/3s to avoid soft-ban.
- **UTM hygiene** — every CTA link must include `utm_source=newsletter&utm_medium=email&utm_campaign=<issue-slug>&utm_content=<cta-name>`. Misnamed UTMs poison roll-up analytics.

## Sources

- [Beehiiv MCP launch — March 24 2026](https://product.beehiiv.com/p/beehiiv-mcp)
- [Beehiiv MCP AI agent integration guide 2026](https://www.buildmvpfast.com/blog/beehiiv-mcp-newsletter-ai-agent-integration-2026)
- [Beehiiv API v2 reference](https://developers.beehiiv.com/)
- [Ghost Admin API docs](https://ghost.org/docs/admin-api/)
- [Ghost Content API docs](https://ghost.org/docs/content-api/)
- [Ghost vs Beehiiv positioning](https://ghost.org/vs/beehiiv/)
- [Kit (ConvertKit) v3 API](https://developers.convertkit.com/)
- [Kit vs Beehiiv 2026 — decision tree](https://www.knockedupmoney.com/blog/convertkit-vs-beehiiv-whats-the-best-newsletter-platform)
- [Beehiiv vs Substack vs Ghost monetization 2026](https://earnifyhub.com/blog/blogging/beehiiv-vs-substack-vs-ghost-monetisation.php)
- [Best newsletter platforms 2026](https://www.sequenzy.com/blog/best-newsletter-platforms)
- [RFC 8058 — one-click list unsubscribe](https://datatracker.ietf.org/doc/html/rfc8058)
