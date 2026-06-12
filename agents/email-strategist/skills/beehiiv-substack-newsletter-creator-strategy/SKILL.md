<!--
Source: https://developers.beehiiv.com/ + Substack
Newsletter creator economy. Beehiiv API (publishing + analytics + referrals).
Substack migration. Monetization math.
-->
# Beehiiv + Substack Newsletter Creator Strategy — SKILL

Newsletter creator economy: Beehiiv (ad network + paid subscriptions + referrals + recommendations) vs Substack (paid-subscription default + writer brand). Beehiiv API is comprehensive; Substack API limited (RSS + CSV export). Monetization math: free-to-paid conversion, ad CPM, boost rate, LTV.

## When to use

- "Launch a paid newsletter"
- "Migrate from Substack to Beehiiv (or vice versa)"
- "Programmatic publishing via Beehiiv API"
- "Set up referral program for newsletter"
- "Newsletter monetization math (CPM vs paid subs)"
- "Substack to ConvertKit / Ghost / Beehiiv migration"

## Setup

```bash
# Beehiiv — sign up at https://www.beehiiv.com
export BEEHIIV_API_KEY="<your-key>"      # https://app.beehiiv.com/settings/integrations/api
export BEEHIIV_PUBLICATION_ID="pub_<id>"

# Substack — no first-party API for write operations
# Read via RSS + CSV export
export SUBSTACK_PUB="<your-substack-handle>"
```

Costs:
- Beehiiv: free for free newsletters (with Beehiiv branding); Scale $39/mo, Max $99/mo. Boost / ads revenue share at higher tiers.
- Substack: free; 10% revenue cut on paid subs + Stripe fees (2.9% + $0.30).
- ConvertKit (alt): $9/mo+ depending on subscribers.
- Ghost (self-hosted alt): $11/mo Ghost Pro, or self-host on $5/mo VPS.

## Common recipes

### Recipe 1: Beehiiv — create a post

```bash
curl -X POST "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/posts" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"This Week in AI",
    "subtitle":"Three things I learned",
    "status":"draft",
    "body_content":"<h2>Hello!</h2><p>This week...</p>",
    "audience":"both",
    "platform":"both",
    "thumbnail_image_url":"https://cdn.brand.com/cover.jpg",
    "preview_text":"Three things I learned this week",
    "send_email":true,
    "scheduled_at":null
  }'
```

### Recipe 2: Beehiiv — publish (send to subscribers)

```bash
POST_ID="<post-id>"

# Schedule publish
curl -X PATCH "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/posts/$POST_ID" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY" \
  -d '{
    "status":"confirmed",
    "scheduled_at":"2026-06-10T14:00:00Z"
  }'

# Or publish immediately
curl -X PATCH "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/posts/$POST_ID" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY" \
  -d '{"status":"confirmed","send_email":true}'
```

### Recipe 3: Beehiiv — subscriber sync (write)

```bash
# Add subscriber
curl -X POST "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/subscriptions" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY" \
  -d '{
    "email":"new@example.com",
    "reactivate_existing":true,
    "send_welcome_email":true,
    "utm_source":"website",
    "utm_medium":"footer",
    "utm_campaign":"homepage_subscribe",
    "referring_site":"https://brand.com"
  }'

# Bulk import (CSV)
curl -X POST "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/subscriptions/imports" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY" \
  -F "file=@subscribers.csv"
```

### Recipe 4: Beehiiv — analytics

```bash
# Publication-level stats
curl "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/stats" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY" | jq

# Per-post stats
curl "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/posts/$POST_ID/stats" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY" | jq '{
    sent, opens, opens_unique, clicks, clicks_unique,
    revenue_attributed,
    open_rate,
    click_through_rate
  }'

# Subscriber count history
curl "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/subscribers/count?from=2026-01-01&to=2026-06-09" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY"
```

### Recipe 5: Beehiiv — referral program

```bash
# Get referral leaderboard
curl "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/referrals/leaderboard" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY" | jq '.data[] | {email, total_referrals, total_unlocked_referrals}'

# Referral milestones (3 = exclusive content, 10 = swag, 25 = paid sub)
# Configured in Beehiiv UI; API exposes leaderboard data
```

### Recipe 6: Beehiiv — boosts (paid recommendations)

```bash
# List boost campaigns
curl "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/boosts" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY"

# Create boost (pay other newsletters to recommend yours)
curl -X POST "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/boosts" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY" \
  -d '{
    "target_publication_id":"<other-pub>",
    "cost_per_subscriber":3.50,
    "max_subscribers":500,
    "max_spend":1750
  }'
```

### Recipe 7: Substack — RSS feed ingest (for migration)

```bash
# Substack RSS
curl "https://${SUBSTACK_PUB}.substack.com/feed" | xmllint --format -

# Parse posts
curl "https://${SUBSTACK_PUB}.substack.com/feed" | \
  python3 -c "
import sys, feedparser
feed = feedparser.parse(sys.stdin.read())
for entry in feed.entries:
    print(f\"{entry.title}\t{entry.link}\t{entry.published}\")
"
```

### Recipe 8: Substack → Beehiiv migration

```bash
# 1. Export subscribers from Substack (UI: Dashboard → Subscribers → Export to CSV)
# 2. Export post archive (UI: Settings → Exports → Download .zip)
# 3. Push subscribers to Beehiiv (Recipe 3)
# 4. Import historic posts to Beehiiv

for HTML_FILE in substack_export/posts/*.html; do
  TITLE=$(grep -oP '(?<=<title>).*?(?=</title>)' "$HTML_FILE")
  CONTENT=$(cat "$HTML_FILE")
  curl -X POST "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/posts" \
    -H "Authorization: Bearer $BEEHIIV_API_KEY" \
    -d "{
      \"title\":\"$TITLE\",
      \"body_content\":$(echo "$CONTENT" | jq -Rs .),
      \"status\":\"published\",
      \"send_email\":false
    }"
done

# 5. DNS migration if using custom domain
# 6. Coordinate Substack cancellation for paid subs (Substack support involved)
```

### Recipe 9: Newsletter economics math

```python
# Free-to-paid conversion
SUBSCRIBERS = 25000
FREE_TO_PAID_RATE = 0.05         # 5%, industry typical
MONTHLY_PRICE = 8                # $8/mo
AVG_MONTHS = 18                  # avg sub lifetime
STRIPE_FEE = 0.029 + (0.30 / MONTHLY_PRICE)
PLATFORM_FEE = 0.00              # Beehiiv 0% on Max plan, Substack 10%

paid_subs = SUBSCRIBERS * FREE_TO_PAID_RATE
ltv_per_sub = MONTHLY_PRICE * AVG_MONTHS * (1 - STRIPE_FEE - PLATFORM_FEE)
annual_paid_rev = paid_subs * MONTHLY_PRICE * 12 * (1 - STRIPE_FEE - PLATFORM_FEE)

print(f"Paid subs: {paid_subs:,.0f}")                    # 1,250
print(f"LTV per sub: ${ltv_per_sub:,.0f}")               # $134
print(f"Annual paid revenue: ${annual_paid_rev:,.0f}")   # $116K

# Ad CPM math
OPENS_PER_ISSUE = 12000
ISSUES_PER_YEAR = 50
CPM = 25                          # $/1000 opens — niche newsletter
ANNUAL_AD_REV = (OPENS_PER_ISSUE / 1000) * CPM * ISSUES_PER_YEAR
print(f"Annual ad revenue: ${ANNUAL_AD_REV:,.0f}")       # $15K

# Boost revenue (Beehiiv recommendations — Boost feed)
BOOST_SUBS_PER_ISSUE = 30
BOOST_REVENUE_PER_SUB = 3.50
ANNUAL_BOOST_REV = BOOST_SUBS_PER_ISSUE * BOOST_REVENUE_PER_SUB * ISSUES_PER_YEAR
print(f"Annual boost revenue: ${ANNUAL_BOOST_REV:,.0f}") # $5,250
```

### Recipe 10: Premium content gating (Beehiiv)

```bash
# Mark post as premium-only
curl -X POST "https://api.beehiiv.com/v2/publications/$BEEHIIV_PUBLICATION_ID/posts" \
  -H "Authorization: Bearer $BEEHIIV_API_KEY" \
  -d '{
    "title":"Deep Dive — Premium",
    "audience":"premium",                  # free | premium | both
    "platform":"both",                      # email | web | both
    "body_content":"...",
    "send_email":true
  }'

# Or partial gating: free preview + premium tail
# Use Beehiiv's [premium-only] markdown block in body_content
```

### Recipe 11: Custom domain setup (Beehiiv)

```bash
# In Beehiiv UI: Settings → Custom domain → add newsletter.brand.com
# Beehiiv issues DNS records:
newsletter.brand.com.    CNAME   <pub-slug>.beehiiv.com
```

Plus DKIM + SPF for email-from-domain alignment:

```
newsletter.brand.com.    TXT  "v=spf1 include:mail.beehiiv.com ~all"
bhv1._domainkey.newsletter.brand.com.   CNAME   bhv1.dkim.beehiiv.com
bhv2._domainkey.newsletter.brand.com.   CNAME   bhv2.dkim.beehiiv.com
```

### Recipe 12: Ghost (self-hosted alternative)

```bash
# Ghost via Docker
docker run -d --name ghost \
  -p 2368:2368 \
  -v ghost-content:/var/lib/ghost/content \
  -e url=https://newsletter.brand.com \
  -e database__client=sqlite3 \
  ghost:5-alpine

# Or Ghost Pro hosted
# https://ghost.org — $11/mo starter
```

Ghost has full API, no platform fees, more dev-flexible than Beehiiv / Substack.

### Recipe 13: Comparison table

| Feature | Beehiiv | Substack | ConvertKit | Ghost |
|---|---|---|---|---|
| Free plan | yes (with branding) | yes (free pubs) | yes (1K subs) | no |
| Ad network | yes (built-in) | no | no | no |
| Paid subs | yes (0% on Max) | yes (10% cut) | yes | yes |
| Boost (paid recs) | yes | no | no | no |
| Referral program | built-in | plugin | built-in | plugin |
| API | comprehensive | limited (read) | comprehensive | comprehensive |
| Custom domain | paid plan | paid plan | paid plan | paid/self-host |
| Audience portability | full | full | full | full |
| Best for | scale + ads | writers + paid | course creators | dev-flexibility |

## Examples

### Example 1: Launch a paid newsletter

**Goal:** monetize an audience of 15K free subscribers.

**Steps:**

1. Choose platform: Beehiiv (low platform cut, ad-revenue option) OR Substack (writer-brand recognition).
2. Set up tier structure:
   - Free tier: weekly newsletter, archive access
   - Paid tier ($8/mo or $80/yr): premium analysis, deep dives, Q&A
3. Build referral program (Recipe 5).
4. First paid issue: send "Here is what's behind the paywall" preview to free list.
5. Track conversion (Recipe 4). Industry typical 5-10% free-to-paid.
6. Estimate revenue (Recipe 9). 15K × 5% × $8 × 12 = $7,200/mo gross.

### Example 2: Migrate from Substack to Beehiiv

**Goal:** Substack writer with 8K subs wants ad-revenue model (Beehiiv).

**Steps:**

1. Export from Substack (Recipe 8 step 1-2).
2. Set up Beehiiv publication.
3. Push subscribers (Recipe 8 step 3-4).
4. Import historic posts (Recipe 8 step 5).
5. Setup custom domain in Beehiiv (Recipe 11).
6. Cancel Substack paid (coordinate w/ Substack support); pro-rated refund handling.
7. Send migration announcement to free list.
8. Enroll in Beehiiv Boost network for distribution growth.

## Edge cases

- **Substack write API doesn't exist** — programmatic publishing to Substack requires browser automation (Playwright). Read via RSS only.
- **Beehiiv free plan adds "Send via Beehiiv" branding** — fine for casual newsletters; remove on paid plan.
- **Substack ownership** — Substack hosts content. If you ever leave, you take subscribers but not URLs (broken links from external sites).
- **Beehiiv revenue share** — Beehiiv keeps ~5% of ad revenue on Scale; smaller % on Max. Paid subs are 0% platform fee on Max plan.
- **Beehiiv API rate limits** — 100 req/min for most endpoints; 10 req/min for bulk imports.
- **Boost program quality** — Boost results vary. Some boost-network newsletters are tiny / off-topic. Vet target publications.
- **Substack paid sub migration** — Stripe customer IDs don't transfer cleanly. Coordinate with Substack to issue refunds; have users re-subscribe on new platform.
- **Custom domain affects deliverability** — new domain = cold reputation. Warm for 4-6 weeks before high-volume sends.
- **iOS Mail / Apple's MPP** affects open rates on Beehiiv / Substack too. Track clicks not opens.
- **Newsletter sponsorship** beyond Beehiiv's network — sites like Swapstack, Paved, Sponsored.studio mediate sponsorships for newsletters under 100K subs.

## Sources

- [Beehiiv API docs](https://developers.beehiiv.com/)
- [Beehiiv API v2 reference](https://developers.beehiiv.com/api-reference)
- [Substack help (no public API)](https://support.substack.com/)
- [Ghost docs](https://ghost.org/docs/)
- [ConvertKit API](https://developers.convertkit.com/)
- [Swapstack newsletter sponsorships](https://swapstack.co/)
- [Paved newsletter sponsorships](https://paved.com/)
- [Beehiiv vs Substack comparison](https://www.beehiiv.com/vs/substack)
