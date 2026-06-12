# Newsletter Subscriber Growth — Beehiiv Referrals / Boosts / Kit Flows / Ghost Paywalls

> Grow newsletter list via referrals, paid acquisition (Boosts), tag-based automation, and paywall optimization.

## When to use

Trigger on: "grow my newsletter list", "Beehiiv referrals", "Beehiiv Boosts", "Kit tag flows", "Ghost paywall", "lead magnet for newsletter", "newsletter cross-promotion", "subscriber acquisition cost". This skill owns: subscriber-growth tactics specific to each newsletter platform. For platform decision tree see `long-form-newsletter-substack-beehiiv-ghost`. For lead-magnet design see the infographic + lead-magnet recipes in `infographic-canva-piktochart-visme`. For surveys/polls see `newsletter-audience-survey`.

## Setup

```bash
# Beehiiv MCP — read-only subscriber + referral data
npx @beehiiv/mcp-server query --help

# Kit (ConvertKit) — tag-based automation
curl -d "api_secret=$KIT_API_SECRET" https://api.convertkit.com/v3/account

# Ghost Admin API for paywall + tier management
# See long-form-newsletter-substack-beehiiv-ghost skill for JWT minting

# Beehiiv Boosts (paid acquisition) — dashboard + Beehiiv MCP for stats
```

Auth env vars (inherited from `long-form-newsletter-substack-beehiiv-ghost`):
- `BEEHIIV_API_KEY` + `BEEHIIV_PUBLICATION_ID`
- `KIT_API_KEY` + `KIT_API_SECRET`
- `GHOST_ADMIN_KEY` + `GHOST_ADMIN_URL`

## Common recipes

### Recipe 1: Beehiiv referral program setup

```markdown
## Beehiiv referrals (built-in)

Beehiiv has native referral mechanics that incentivize current subs to share.

**Setup (one-time, dashboard):**
1. Settings → Referral Program → Enable
2. Define rewards by referral count:
   - 1 referral: <small premium content unlock>
   - 5 referrals: <lead magnet PDF / template>
   - 10 referrals: <free month of paid tier>
   - 25 referrals: <swag / 1:1 access / cohort access>
3. Each sub gets a unique tracking link in every issue
4. Track conversions in dashboard

**Pull stats via MCP:**
```

```bash
npx @beehiiv/mcp-server query \
  --tool get_referral_program_stats \
  --args '{"publication_id":"'"$BEEHIIV_PUBLICATION_ID"'","range":"last_30_days"}'
```

Returns referrals_sent, referrals_converted, top_referrers, conversion_by_tier.

### Recipe 2: Beehiiv Boosts (paid acquisition)

```markdown
## Beehiiv Boosts

Paid sub acquisition by paying ANOTHER Beehiiv publication to recommend yours.

**How it works:**
- You set a CPA you'll pay per net-new sub (e.g., $1.50/sub)
- Beehiiv matches you with relevant publications in your niche
- Their newsletter recommends yours in their recommendation widget
- You pay per conversion (qualified sub)

**Setup (dashboard):**
1. Settings → Boosts → Enable + set max CPA
2. Set audience criteria (geo, niche tags)
3. Set daily budget cap
4. Monitor conversion + cost
```

```bash
# Pull Boost performance
npx @beehiiv/mcp-server query \
  --tool get_boost_stats \
  --args '{"publication_id":"'"$BEEHIIV_PUBLICATION_ID"'","range":"last_30_days"}'
# Returns spend, subs_acquired, CPA_actual, top_source_publications
```

CPA benchmarks (2026): $1-3 for general; $3-8 for niche B2B; $5-12 for high-LTV creators.

### Recipe 3: Beehiiv Recommendation Network (free)

```markdown
## Recommendation Network (free, opt-in)

Beehiiv's free recommendation graph — your subs see a list of recommended newsletters
after subscribing; other publications can recommend yours. Free reach.

**Setup:**
1. Settings → Recommendation Network → Enable
2. Pick categories that match your niche
3. Set how many recommendations show post-subscribe (default 3)
4. Monitor incoming/outgoing referrals
```

```bash
npx @beehiiv/mcp-server query \
  --tool get_recommendation_network_stats \
  --args '{"publication_id":"'"$BEEHIIV_PUBLICATION_ID"'"}'
```

### Recipe 4: Kit tag-based welcome flow

```bash
# Step 1: Create tag for lead magnet downloaders
curl -X POST "https://api.convertkit.com/v3/tags" \
  -d "api_secret=$KIT_API_SECRET" \
  -d "tag[name]=leadmag-newsletter-2026-report"

# Step 2: Create sequence (welcome flow)
# In Kit dashboard: Automate → Sequences → New
# Email 1 (immediate): "Here's your PDF — and what to expect"
# Email 2 (day 2): "The one chart you missed in the report"
# Email 3 (day 5): "Quick survey — which topic should I cover next?"
# Email 4 (day 10): "Want more? Here's a paid tier preview"

# Step 3: Tag subs as they enter from lead magnet
curl -X POST "https://api.convertkit.com/v3/tags/<tag_id>/subscribe" \
  -d "api_key=$KIT_API_KEY" \
  -d "email=sub@example.com"

# Step 4: Tag triggers sequence
# (auto-configured in dashboard)
```

### Recipe 5: Ghost member tier paywall

```bash
# Define member tiers via Ghost Admin API (JWT auth from long-form-newsletter skill)
curl -X POST "$GHOST_ADMIN_URL/ghost/api/admin/tiers/" \
  -H "Authorization: Ghost $TOKEN" \
  -d '{
    "tiers": [{
      "name": "Premium",
      "description": "Access to the full member-only archive + weekly deep dive",
      "monthly_price": 1500,
      "yearly_price": 15000,
      "currency": "usd",
      "active": true,
      "visibility": "public"
    }]
  }'

# Mark posts as member-only when publishing
curl -X POST "$GHOST_ADMIN_URL/ghost/api/admin/posts/" \
  -H "Authorization: Ghost $TOKEN" \
  -d '{
    "posts": [{
      "title": "...",
      "html": "...",
      "visibility": "paid",
      "tiers": [{"id":"<premium_tier_id>"}]
    }]
  }'
```

### Recipe 6: Lead-magnet → newsletter sign-up funnel

```markdown
## Funnel structure

1. **Tentpole content** drives traffic (newsletter / podcast / blog / social)
2. **Lead magnet pitch** at end of tentpole: "Get the PDF version + bonus data"
3. **Landing page** (Beehiiv / Ghost / Kit form): single field (email) + clear value prop
4. **Email confirmation + instant delivery** of lead magnet
5. **Welcome sequence (Recipe 4)** nurtures new sub from cold → engaged → paid

## Lead magnet types ranked by conversion
- **Templates** (Notion DB, spreadsheet, brief template) — 30-50% landing-page conversion
- **PDF lead magnet** (state-of report, definitive guide) — 20-35% conversion
- **Mini-course** (5-day email course) — 15-25% conversion
- **Newsletter swap** (cross-promotion with another newsletter) — 10-20% conversion
- **Webinar registration** — 10-15% conversion (high effort)
```

### Recipe 7: Newsletter cross-promotion (organic swap)

```markdown
## Swap structure

Find a complementary creator (same audience, different angle); each promotes the other:
- Issue 1 of yours: dedicated mention + CTA
- Issue 1 of theirs: dedicated mention + CTA
- Optional: co-branded lead magnet for both audiences

**Negotiate via:**
- DM on social or Gmail outreach
- Reference specific issues you've read
- Propose specific date window
- Use UTM tags for attribution

**Track attribution:**
- Your CTA URL: yourdomain.com/?utm_source=swap-<theirs>&utm_medium=newsletter
- Their CTA URL: theirdomain.com/?utm_source=swap-<yours>
```

### Recipe 8: Welcome sequence quality gates

```markdown
- [ ] Email 1 sent within 5 minutes of sign-up (instant delivery)
- [ ] Email 1 includes the promised lead magnet + 1 paragraph on what to expect
- [ ] Email 2 (day 2) provides additional value beyond lead magnet
- [ ] Email 3 (day 5) ask a question (reply rate boost)
- [ ] Email 4 (day 10) introduces paid tier — soft pitch, not hard sell
- [ ] All emails: plain-text + minimal HTML (better deliverability than image-heavy)
- [ ] All emails: from a person, not "noreply@"
- [ ] Unsubscribe link in every email (one-click RFC 8058)
```

### Recipe 9: Engagement-based segmentation (Kit advanced)

```bash
# Tag subs by engagement to focus retention efforts
# Kit's tag system:

# Tag highly engaged
curl -X POST "https://api.convertkit.com/v3/forms/<form_id>/subscribers" \
  -d "api_key=$KIT_API_KEY" \
  -d "email=sub@example.com" \
  -d "tags[]=engaged-30d"

# Tag cold (no opens in 30 days)
curl -X POST "https://api.convertkit.com/v3/tags/<cold_tag_id>/subscribe" \
  -d "email=cold-sub@example.com"

# Run a "reactivation" sequence on cold tag
# Or sunset (remove) cold subs after 90 days for deliverability hygiene
```

### Recipe 10: Beehiiv subscriber growth metrics

```bash
# Per-channel attribution
npx @beehiiv/mcp-server query \
  --tool get_subscriptions \
  --args '{"publication_id":"'"$BEEHIIV_PUBLICATION_ID"'","limit":1000,"utm_source_filter":"twitter"}'

# Aggregate by UTM source to identify top growth channels
```

### Recipe 11: Acquisition cost analysis

```python
# Compute blended CAC
channels = {
    'Beehiiv Boosts': {'spend': 800, 'subs': 600},
    'Newsletter swap': {'spend': 0, 'subs': 350, 'time_hours': 10},
    'Twitter thread': {'spend': 0, 'subs': 200, 'time_hours': 4},
    'LinkedIn carousel': {'spend': 0, 'subs': 150, 'time_hours': 3},
    'Podcast guest spot': {'spend': 0, 'subs': 500, 'time_hours': 8},
}

for ch, data in channels.items():
    cac = data['spend'] / data['subs'] if data['subs'] else 0
    # Add time cost @ $100/hr
    full_cac = (data['spend'] + data.get('time_hours', 0) * 100) / data['subs']
    print(f"{ch}: CAC ${cac:.2f}, fully-loaded ${full_cac:.2f}")
```

### Recipe 12: Sunset cold subs (deliverability hygiene)

```bash
# Subs who haven't opened in 90+ days hurt deliverability scores
# Run sunset list:

# Beehiiv
npx @beehiiv/mcp-server query \
  --tool get_subscriptions \
  --args '{"status":"active","engagement_score":"low","last_open_before":"2026-03-12"}'

# Unsubscribe via Beehiiv API (or send goodbye-or-stay re-engagement email first)
```

## Examples

### Example 1: 0 → 5k subs in 6 months on Beehiiv

**Goal:** New Beehiiv newsletter goes from 0 → 5k subs.

**Steps:**
1. Recipe 6: build lead magnet (PDF / template) — highest-conversion form.
2. Recipe 1: enable referrals with milestone rewards.
3. Recipe 3: opt into Recommendation Network for free reach.
4. Per Tuesday issue: include referral link + recent referral leaders shout-out.
5. Week 4 onward: Recipe 2 Boosts with $1.50 CPA cap, $300/mo budget = ~200 subs/mo.
6. Recipe 7: 2-3 swaps with creators of similar size.
7. Week 12: Recipe 11 CAC analysis; double down on best channel.

**Result:** 5k subs in 6 months, blended CAC ~$1-3.

### Example 2: Kit migration from Beehiiv for advanced automation

**Goal:** Beehiiv creator with course product wants Kit's tag-based automation.

**Steps:**
1. Export Beehiiv subs CSV.
2. Import into Kit with tags by acquisition source.
3. Recipe 4: build welcome sequences (cold sub → engaged → paying).
4. Recipe 9: segment by engagement; sunset cold subs at day 90.
5. Promote course product via tag-triggered sequence post-engagement.

**Result:** Higher per-sub LTV via course bundling; better segmentation.

### Example 3: Ghost paywall design for indie publisher

**Goal:** Indie publisher Ghost site wants $15/mo paid tier with paywall.

**Steps:**
1. Recipe 5: create Premium tier at $15/mo.
2. Mark 70% of posts as free, 30% as paid (or freemium with paywall mid-post).
3. Add paywall CTA mid-post for free posts ("Subscribe to read the rest").
4. Welcome flow for new free subs nurturing to paid.
5. Monthly: Recipe 4 churn check; survey lapsing subs.

**Result:** 2-5% free → paid conversion within 6 months.

## Edge cases / gotchas

- **Apple MPP (Mail Privacy Protection)** inflates Beehiiv / Substack open rates to 60%+. Use CTR + CTOR as real engagement signals, not opens.
- **Sunset cold subs every 90 days** for deliverability score; cold subs tank inbox placement for engaged subs.
- **Beehiiv Boosts CPA can balloon** in niche markets; cap CPA + watch daily.
- **Recommendation Network is free reach but mid-quality** — subs from recommendations sometimes don't engage. Track retention vs your own subs.
- **Lead magnet must deliver value in <60s of sign-up** — delayed delivery = user forgets they signed up.
- **Don't over-segment too early.** 3-5 tags max until you have 5k+ subs.
- **Subject line still matters** even with MPP-inflated opens; CTR is downstream of open click-through.
- **One-click unsubscribe (RFC 8058)** is required by all platforms now; don't override.
- **Confirmed opt-in (double opt-in)** drops sign-ups by 20-30% but improves engagement quality. Default ON for B2B.
- **Don't buy email lists.** Burns sender reputation, illegal in many jurisdictions, doesn't work anyway.
- **Cross-promotion swaps have a ceiling** — same audience repeatedly = diminishing returns. Rotate partners.
- **Welcome sequence open rate >40% is healthy.** Below 25% = sequence content needs work.
- **Free → paid conversion benchmark**: 2-5% over 6 months is solid. Above 8% is exceptional (or you're under-pricing free).
- **Kit pricing scales aggressively** — at 10k subs it's ~$135/mo vs Beehiiv $42. Worth it only if commerce / automation are deep needs.
- **Newsletter classified ads** (small per-issue placements) can monetize without paywalling content — alt to converting free to paid.

## Sources

- [Beehiiv MCP guide](https://www.buildmvpfast.com/blog/beehiiv-mcp-newsletter-ai-agent-integration-2026)
- [Beehiiv referrals docs](https://www.beehiiv.com/referral-program)
- [Beehiiv Boosts](https://www.beehiiv.com/boosts)
- [Kit (ConvertKit) automation docs](https://help.kit.com/en/articles/4053547-getting-started-with-automations)
- [Ghost member tiers](https://ghost.org/docs/admin-api/#tiers)
- [Kit vs Beehiiv 2026](https://www.knockedupmoney.com/blog/convertkit-vs-beehiiv-whats-the-best-newsletter-platform)
- [RFC 8058 — one-click unsubscribe](https://datatracker.ietf.org/doc/html/rfc8058)
- [Email deliverability best practices](https://www.litmus.com/blog/the-ultimate-guide-to-email-deliverability/)
