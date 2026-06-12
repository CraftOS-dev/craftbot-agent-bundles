# Monetization Stack — Patreon v2 / Memberstack / Circle / Substack / Beehiiv Ad Network

> Design 3-tier monetization stacks across memberships, paid newsletters, sponsorships, and ad networks.

## When to use

Trigger on: "how should I monetize", "Patreon vs Memberstack vs Circle", "design a monetization stack", "tier pricing", "iOS 30% fee", "membership platform decision", "ad network for my newsletter", "podcast ad network". This skill owns: stack design, platform decision tree, pricing tier structure, churn benchmarks, Patreon iOS fee flag. For sponsorship-specific work see `podcast-sponsorship-integration` and `creator-collab-brand-partnership-briefing`. For newsletter-specific growth tactics see `newsletter-subscriber-growth`.

## Setup

```bash
# Patreon v2 (v1 deprecated)
curl -H "Authorization: Bearer $PATREON_ACCESS_TOKEN" \
  https://www.patreon.com/api/oauth2/v2/identity

# Memberstack
curl -H "X-API-KEY: $MEMBERSTACK_SECRET_KEY" \
  https://admin.memberstack.com/api/v1/members

# Circle
curl -H "Authorization: Bearer $CIRCLE_API_KEY" \
  https://app.circle.so/api/v1/community

# Substack — no public API for revenue data (manual export only)
# Beehiiv — via Beehiiv MCP (see long-form-newsletter skill)
```

Auth env vars:
- `PATREON_ACCESS_TOKEN` — OAuth 2.0 creator token; refresh every 30 days.
- `MEMBERSTACK_SECRET_KEY` — Memberstack admin dashboard → API.
- `CIRCLE_API_KEY` — Circle admin → developer.
- `BEEHIIV_API_KEY` / `BEEHIIV_PUBLICATION_ID` — for revenue + ad-network data via Beehiiv MCP.

## Common recipes

### Recipe 1: Monetization stack template

```markdown
# Monetization Stack: <Creator Name>

## Audience snapshot
- Total reach: <number across platforms>
- Newsletter subs: <number>
- Podcast monthly listens: <number>
- Social followers by platform: <breakdown>
- Engagement rate: <%>
- Mobile-vs-desktop subscriber mix: <% mobile>  # critical for Patreon iOS flag

## Current revenue
- Stream 1: <name + monthly + % of total>
- Stream 2: <...>
- Total MRR: $<>

## Proposed 3-tier stack
### Tier 1 — Free / $0
- What they get: <content access + community + ...>
- Free → Paid conversion target: <%>

### Tier 2 — Paid baseline / $<low>
- What they get: <premium content + community>
- Free → Tier 2 target: <%>
- Churn target: <% monthly>

### Tier 3 — Premium / $<high>
- What they get: <Tier 2 + exclusive + cohort + access>
- Paid → Premium target: <%>
- Churn target: <% monthly>

## Sponsorship inventory
- Newsletter mid-issue: $<CPM> × <issues/mo> = $<rev>
- Newsletter classified: $<flat> × <count> = $<rev>
- Podcast host-read: $<CPM> × <downloads/mo> = $<rev>
- YouTube integrated: $<flat> × <vids/mo> = $<rev>

## Ad networks
- Beehiiv Ad Network: <est. $<rev>>
- Spotify / Megaphone: <est. $<rev>>
- YouTube ads: <est. $<rev>>

## Products / digital
- Course / Kajabi: <est. $<rev>>
- PDF lead magnets via Gumroad / Stan Store: <est. $<rev>>

## Projected MRR by Month 6
- Tier 2 × price: $<>
- Tier 3 × price: $<>
- Sponsorship: $<>
- Ads: $<>
- Products: $<>
- **Total: $<>**

## iOS fee flag
- Mobile subscriber %: <%>
- If >40%, Patreon's 30% Apple fee passthrough = 12% margin hit
- Mitigation: <Memberstack / Circle migration | web-checkout-only | raise prices>

## Platform choices
- Newsletter: <Beehiiv | Substack | Ghost | Kit> because <rationale>
- Membership: <Patreon | Memberstack | Circle> because <rationale>
- Product: <Kajabi | Podia | Gumroad | Stan Store> because <rationale>
- Live: <Maven | Riverside Live | manual Zoom> because <rationale>
```

### Recipe 2: Platform decision tree

```markdown
## Newsletter → recommended platform
- Media-product newsletter, want analytics + ad network → **Beehiiv** (0% rev share, native MCP)
- Indie publisher with brand-controlled CMS → **Ghost** (0% rev share, full Content + Admin API)
- Low-friction creator economy + built-in discovery → **Substack** (10% rev share)
- Course creator + complex automation + commerce → **Kit** (~$135/mo at 10k subs)

## Membership → recommended platform
- Mobile audience <40% → **Patreon v2** (88% creator take, large discovery network, iOS 30% post-Nov 2026)
- Mobile audience >40% → **Memberstack** (96% creator take, no Apple fee)
- Community-first (forum + events + courses bundled) → **Circle** (flat fee, SSO + API)
- Webflow stack → **Memberstack** (native integration)

## Product → recommended platform
- Course w/ video + cohort → **Kajabi** or **Podia**
- Digital download (PDF, template, asset pack) → **Gumroad** or **Stan Store**
- Bundle link aggregation → **Beacons** or **Linktree** (lower revenue, higher reach)

## Live events → recommended platform
- Paid webinars / cohort courses → **Maven** (cohort-based)
- Pop-up live → **Riverside Live** or **Streamyard**
- Annual conference → **Cvent** or custom
```

### Recipe 3: Tier pricing design

```markdown
## 3-tier sweet spot

Recommended tier structure:
- **Tier 1 (Free) — $0** — content lead magnet + community access
- **Tier 2 (Median sweet spot) — $X** — premium content + benefits
- **Tier 3 (Anchor) — $5X** — premium tier 5× median to anchor perception

## Pricing examples
- $0 / $20 / $100 — newsletter operator
- $0 / $10 / $50 — niche podcast
- $0 / $50 / $250 — high-touch B2B advisor

## Margin targets
- Paid newsletter: 70%+ contribution margin (platform 0-10% + payment processing)
- Membership community: 60%+ (more support burden)
- Course / product: 80%+ (one-time delivery cost)
```

### Recipe 4: Churn benchmarks

```markdown
| Stream | Healthy churn | Restructure if |
|---|---|---|
| Paid newsletter | <5%/mo | >10%/mo |
| Membership community | 5-8%/mo | >12%/mo |
| SaaS-style course | <3%/mo | >8%/mo |
| Course / product (one-time) | n/a, track refund rate | refund >5% |
```

### Recipe 5: Patreon iOS fee mitigation (critical post-Nov 2026)

```markdown
## The problem
- Apple's 30% in-app purchase fee enforcement on Patreon iOS app, Nov 2026
- Patreon passes the 30% through to creators
- If 40%+ of subs are mobile (iPhone), effective take drops from 88% → 76%
- = 12% margin hit on a substantial slice

## Mitigation options

### Option A: Migrate to Memberstack (96% creator take)
- Webflow-native; works for any site
- Slightly higher build complexity (you own the auth flow)
- Best for: creators with Webflow / Webflow-adjacent sites

### Option B: Migrate to Circle (flat fee)
- $99-799/mo flat regardless of MRR
- Save $600-800/mo vs Patreon at $10k MRR
- Best for: community-first creators where forum + events matter

### Option C: Push memberships to web checkout only
- Disable Patreon iOS app for new sign-ups
- Warn existing iOS users to migrate to web checkout
- Loses some mobile-only sign-ups
- Cheapest tactically; messiest UX

### Option D: Raise mobile-tier pricing to absorb the fee
- Add a "mobile" higher-priced tier that nets you the same after Apple fee
- Confuses pricing; not recommended
```

### Recipe 6: Patreon v2 API — pull member + tier data

```bash
# Identity (logged-in user)
curl -H "Authorization: Bearer $PATREON_ACCESS_TOKEN" \
  "https://www.patreon.com/api/oauth2/v2/identity?include=memberships&fields[user]=email,first_name,full_name"

# Campaign + tier structure
curl -H "Authorization: Bearer $PATREON_ACCESS_TOKEN" \
  "https://www.patreon.com/api/oauth2/v2/campaigns?include=tiers&fields[campaign]=patron_count,creation_count,published_at&fields[tier]=amount_cents,title,description,patron_count"

# Members (paginated)
curl -H "Authorization: Bearer $PATREON_ACCESS_TOKEN" \
  "https://www.patreon.com/api/oauth2/v2/campaigns/<campaign_id>/members?include=currently_entitled_tiers&fields[member]=email,full_name,patron_status,lifetime_support_cents,currently_entitled_amount_cents"
```

### Recipe 7: Memberstack member ops

```bash
# List members
curl -H "X-API-KEY: $MEMBERSTACK_SECRET_KEY" \
  https://admin.memberstack.com/api/v1/members?limit=100

# Update member tier
curl -X PUT -H "X-API-KEY: $MEMBERSTACK_SECRET_KEY" \
  https://admin.memberstack.com/api/v1/members/<member_id> \
  -d '{"planId": "<tier_3_plan_id>"}'
```

### Recipe 8: Circle community + monetization ops

```bash
# List members
curl -H "Authorization: Bearer $CIRCLE_API_KEY" \
  https://app.circle.so/api/v1/community/members

# Membership tier
curl -H "Authorization: Bearer $CIRCLE_API_KEY" \
  https://app.circle.so/api/v1/paywalls
```

### Recipe 9: Beehiiv Ad Network revenue pull

```bash
# Via Beehiiv MCP (read-only V1)
npx @beehiiv/mcp-server query \
  --tool get_ad_network_earnings \
  --args '{"publication_id":"'"$BEEHIIV_PUBLICATION_ID"'","range":"last_90_days"}'
```

### Recipe 10: Monetization dashboard roll-up to Notion

```python
# Weekly: pull revenue across all streams, push to Notion dashboard
streams = {
    'Patreon': patreon_mrr(),
    'Beehiiv Ad Network': beehiiv_ad_revenue_last_30(),
    'Substack paid subs': substack_manual_export_last_30(),
    'Podcast sponsorships': podcast_sponsor_revenue_last_30(),
    'Course (Kajabi)': kajabi_revenue_last_30(),
    'Digital products (Gumroad)': gumroad_revenue_last_30(),
}
total = sum(streams.values())

for stream, rev in streams.items():
    notion.create_page(
        database_id=NOTION_REVENUE_DB,
        properties={
            'Stream': stream,
            'Month': datetime.now().strftime('%Y-%m'),
            'Revenue': rev,
            '% of total': rev/total if total else 0,
        }
    )
```

### Recipe 11: Tier conversion funnel analysis

```python
# What % of free → paid → premium?
free = newsletter.subs_count(tier='free')
paid_t2 = newsletter.subs_count(tier='paid_t2')
premium_t3 = newsletter.subs_count(tier='premium_t3')

print(f"Free → T2 conversion: {paid_t2/free*100:.1f}% (target: 2-5%)")
print(f"T2 → T3 conversion: {premium_t3/paid_t2*100:.1f}% (target: 5-15%)")
print(f"Free → T3 direct: trace via UTM source")
```

### Recipe 12: Revenue projection model

```python
# 6-month projection
months = 6
free_growth_rate = 0.05  # 5% MoM net new free subs
free_to_t2_conversion = 0.03  # 3% convert to T2 within 6 months
t2_to_t3_conversion = 0.08  # 8% of T2 upgrade to T3
churn_t2 = 0.05  # 5% monthly
churn_t3 = 0.03

free = current_free_subs
t2 = current_t2_subs
t3 = current_t3_subs

for m in range(months):
    new_free = free * free_growth_rate
    new_t2 = (free + new_free) * free_to_t2_conversion / 6  # spread over 6 mo
    new_t3 = t2 * t2_to_t3_conversion / 6
    churned_t2 = t2 * churn_t2
    churned_t3 = t3 * churn_t3

    free += new_free - new_t2
    t2 += new_t2 - new_t3 - churned_t2
    t3 += new_t3 - churned_t3

    mrr = t2 * 20 + t3 * 100  # $20 / $100 tiers
    print(f"Month {m+1}: free={int(free)} t2={int(t2)} t3={int(t3)} MRR=${mrr:.0f}")
```

## Examples

### Example 1: Newsletter operator $5k MRR → $20k MRR stack design

**Goal:** Operator at 8k free subs + $5k MRR needs path to $20k MRR.

**Steps:**
1. Recipe 1: audit current state.
2. Identify: 80% mobile-iPhone users → flag Recipe 5 Patreon iOS issue.
3. Recipe 2: choose Beehiiv (newsletter) + Memberstack (membership, mobile-safe).
4. Recipe 3: tier $0 / $20 / $100 design.
5. Recipe 12: project 6-month MRR with realistic conversions.
6. Add Beehiiv Ad Network (Recipe 9) for passive ad revenue.
7. Recipe 10: weekly Notion dashboard.
8. Quarterly: Recipe 4 churn audit; restructure if hot zones flagged.

**Result:** $20k MRR target in 9 months via paid tier + ads + occasional product.

### Example 2: Podcast operator mid-iOS Patreon migration

**Goal:** Podcaster at $8k MRR, 60% iPhone subs, on Patreon — needs migration before Nov 2026 fee.

**Steps:**
1. Recipe 5: confirm Patreon iOS will cost ~$960/mo.
2. Choose Memberstack (96% take) for 1:1 tier migration.
3. Build Memberstack tier mirroring Patreon tiers.
4. Email all Patreon subs: 60-day migration window + 10% discount incentive.
5. Recipe 7: bulk-import members via API.
6. Cancel Patreon campaign Day 60.
7. Recipe 10: track MRR through migration (expect 10-20% leakage).

**Result:** $7-7.5k MRR retained at 96% take = net positive vs Patreon iOS scenario.

### Example 3: Multi-stream creator monetization audit

**Goal:** Multi-channel creator at $30k MRR — which streams to double down on.

**Steps:**
1. Recipe 1 + Recipe 10: full stream-by-stream revenue snapshot.
2. Compute revenue per hour-invested per stream.
3. Identify top 2 ROI streams; cut bottom-quartile.
4. Recipe 12: project 6-month MRR with reallocated time.
5. Recipe 4: churn audit on cut streams; transition members gracefully.

**Result:** Concentrated effort on top streams → 30% MRR lift in 6 months.

## Edge cases / gotchas

- **Patreon v1 is fully deprecated.** Migrate to v2 OAuth + endpoint patterns; old integrations break silently.
- **Patreon iOS fee = 30% Apple passthrough**, enforced Nov 2026. Mobile-heavy creators MUST flag and mitigate.
- **Memberstack requires building your own auth UX** — more work upfront but 96% take long-term.
- **Circle's flat-fee structure is cheaper at $10k+ MRR** but $99/mo even at $0 MRR.
- **Substack's 10% rev share = real cost** at scale; on $30k MRR that's $3k/mo to Substack. Migrate to Beehiiv (0% share) for material savings.
- **Beehiiv Ad Network revenue is passive but per-subscriber yield is small** ($0.10-0.50 per sub per month). Not a primary monetization stream.
- **Don't price-anchor below market.** $5 tier on a creator-economy podcast signals low value; raise to $10-15 minimum.
- **3 tiers is the cognitive max.** 4+ tiers = analysis paralysis = lower conversion.
- **5× spread between Tier 2 and Tier 3** makes T2 look like the deal. Smaller spread = T3 doesn't anchor.
- **Churn is the lagging indicator.** Engagement (open rate, post engagement, community activity) is the leading. Track both.
- **Don't double-charge** by running Patreon + paid newsletter simultaneously at the same price point.
- **Annual discount on tiers** (20% off annual) cuts churn ~30% but requires absorbing the discount upfront.
- **Bundle add-ons (course + membership)** outperform standalone — increases average revenue per user.
- **Don't reduce free-tier value** to push paid conversion — kills top-of-funnel; net negative long-term.
- **Tax + payment processing fees** = ~3-5% on top of platform fees. Factor into margin math.
- **Patreon's Apple fee passthrough is regulator-driven** (DMA / Apple antitrust); subject to change. Track Patreon developer changelog quarterly.

## Sources

- [Patreon developer portal (v2)](https://www.patreon.com/portal)
- [Memberstack content monetization](https://www.memberstack.com/webflow-templates/content-monetization-template)
- [Circle community + monetization](https://circle.so/blog/best-membership-platforms)
- [Beehiiv vs Substack vs Ghost monetization 2026](https://earnifyhub.com/blog/blogging/beehiiv-vs-substack-vs-ghost-monetisation.php)
- [Patreon iOS fee enforcement (Nov 2026)](https://www.patreon.com/portal)
- [Beehiiv Ad Network](https://www.beehiiv.com/ad-network)
- [Kit (ConvertKit) v3 API](https://developers.convertkit.com/)
- [Kajabi platform](https://kajabi.com/)
- [Gumroad creator monetization](https://gumroad.com/)
- [Apple App Store guidelines 2026 (in-app purchase 30%)](https://developer.apple.com/app-store/guidelines/)
