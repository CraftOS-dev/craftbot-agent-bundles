<!--
Sources: https://www.reforge.com/blog/community-led-growth + https://openviewpartners.com/blog/community-led-growth/ + https://posthog.com/docs + https://www.notion.com/help + https://www.linear.app/docs
-->
# Community-Led PLG Motion — SKILL

Design + instrument community handoff points for product-led growth: community drives top-of-funnel (members → free → paid), product virality (in-product community surfaces), and post-purchase retention. Examples: Notion's template gallery + Champions; Figma's Friends program; Webflow's University + forum; Linear's Slack community. PLG metrics: K-factor, time-to-aha, activation%, retention curve, NRR. PostHog event instrumentation; webhook fan-out to community platform on PLG milestones.

## When to use

- New PLG SaaS adding community to amplify product virality.
- Existing PLG-led product with disconnected community → instrument handoff points.
- Designing in-product surfaces (template gallery / "Ask community" link / forum embed).
- Activation-funnel debugging — where do users drop, and how can community catch?
- K-factor measurement + community-driven referral amplification.
- Quarterly PLG review tying community signals to product activation.
- Cross-link to `community-led-growth-measurement` (input metrics) and `community-roi-retention-expansion-advocacy` (output measurement).

Trigger phrases: "PLG community", "product-led growth", "K-factor", "activation funnel", "community handoff", "in-product community", "template gallery", "Notion Champions", "Figma Friends", "Linear community", "community virality", "product virality".

## Setup

```bash
# PostHog for event instrumentation
mcp tool posthog-mcp.capture --event "community.join_prompt_shown" \
  --properties '{"user_id":"U-123","stage":"trial_day_3","plg_milestone":"first_template_used"}'

# Cohorts via HogQL
mcp tool posthog-mcp.query --hogql "
  SELECT properties.plg_milestone, count(distinct distinct_id) AS users
  FROM events
  WHERE event = 'community.join_prompt_clicked'
    AND timestamp > now() - INTERVAL 30 DAY
  GROUP BY 1 ORDER BY 2 DESC;"

# Community platform side: webhook listener for community → product events
# e.g., "user signed up for community" → posthog event "community.joined"

# Linear for tracking PLG → community handoff projects
mcp tool linear-mcp.create_project \
  --team_id $TEAM --name "PLG community handoff points Q3"

# Notion for handoff documentation
mcp tool notion-mcp.databases_create --parent_id $PAGE_ID \
  --title "PLG handoff points" \
  --properties '{"Milestone":{"select":[]},"Surface":{"select":[]},"Community route":{"select":[]}}'
```

Auth + env:
- `POSTHOG_PROJECT_API_KEY` — Project settings → API key.
- `POSTHOG_PERSONAL_API_KEY` — for HogQL + cohort management.
- `DISCORD_BOT_TOKEN` / `SLACK_BOT_TOKEN` — community-side webhooks.
- `LINEAR_API_KEY` — track handoff-point projects.
- `NOTION_TOKEN` — documentation source-of-truth.

Workspace prerequisites:
- PostHog instrumented in product (web + mobile app).
- Community platform user_id → product user_id join table.
- Designated PM + community lead pair for handoff design.
- Notion DB: "PLG handoff points" — Milestone | Surface | Community route | Metric | Status | Owner.

## Common recipes

### Recipe 1: Map the PLG → community handoff points

Standard PLG funnel + community amplifiers:

| Stage | Product event | Community handoff | Why |
|---|---|---|---|
| Visit landing | landing_visit | "X members talking" social proof badge | Build pre-signup trust |
| Sign up | signup_completed | Welcome DM via community | Lowers join friction |
| First action | activation_event_1 | "Stuck? Ask community" link in-product | Catches drop-off |
| Aha moment | activation_event_n (defined) | "Share your win" prompt | Member testimonial flywheel |
| Day 7 nudge | day_7_login | "Pick a template by Champion" surface | Showcases members |
| Trial-end day -3 | trial_ending_in_3d | "Join VIP for Q&A office hours" | Conversion lift |
| Paid conversion | upgraded_to_paid | "Get VIP role in community" | Loyalty lift |
| Churn risk (30d no login) | session_count_drops | DM from community "what's blocking?" | Save-attempt |

Document each in Notion DB. Each row owns: 1 PostHog event, 1 community route, 1 KPI.

### Recipe 2: Instrument core PLG events

```javascript
// Web app — capture PLG milestones
import posthog from "posthog-js";

posthog.capture("activation_first_template_used", {
  template_id: "tpl_abc123",
  template_author: "champion-username",
  is_community_template: true,
});

posthog.capture("trial_ending_in_3d", { plan: "team", trial_started_at: "..." });

posthog.capture("community.join_prompt_shown", {
  prompt_id: "trial_end_join_vip",
  variant: "v2_with_office_hours",
});

posthog.capture("community.join_prompt_clicked", { prompt_id: "trial_end_join_vip" });

posthog.capture("community.joined", {
  platform: "discord",
  invite_source: "trial_end_join_vip",
});
```

### Recipe 3: In-product "Join community" nudge (server-rendered)

```python
# Backend logic: decide which users see which prompts
def should_show_community_prompt(user) -> Optional[str]:
    if user.in_community():
        return None
    if user.signup_at > now() - timedelta(days=2):
        return None  # too early
    if user.trial_ends_in_days() == 3:
        return "trial_end_office_hours"
    if user.activation_events_count() == 0 and user.signup_at < now() - timedelta(days=7):
        return "stuck_help"  # save attempt
    if user.activation_events_count() >= 3:
        return "share_your_win"
    return None

# Frontend renders the right banner; tracks shown/clicked via posthog.
```

### Recipe 4: Linear's "Slack community" model

Linear's pattern:
- Free Slack community → public.
- Anyone (signup or not) can join.
- In-product: "Get help in community" CTA in support widget.
- Sales reps idle in community; jump on signal of intent.

```
# Replicate in your product:
1. Public Discord/Slack with anon read access.
2. In-product help widget: "Live community ↗" → opens community in new tab.
3. Track CTA click via posthog.capture("community.help_widget_clicked", {...}).
4. Sales/SE rotation: every weekday someone idles in #general for live help.
```

### Recipe 5: Notion's template gallery pattern

Notion's pattern:
- Templates created by community members surfaced in-product.
- Template → community member profile link.
- "Created by Champion @username" attribution.

```python
# Backend: serve community-created templates ranked by usage
def get_featured_templates(user):
    return Template.objects.filter(
        is_community=True,
        is_published=True,
    ).order_by("-monthly_usage_count")[:6]

# Track use → attribute back to creator member
posthog.capture("community_template_used", {
  "template_id": tpl.id,
  "creator_member_id": tpl.author_member_id,
  "tier": tpl.author_member.community_tier,
})
```

Webhook to community on usage milestone:
```python
if tpl.monthly_usage_count == 1000:
    discord_full.create_message(
        channel_id=CHAMPIONS_CH,
        content=f":star: Champion @{tpl.author.username}'s template hit 1k uses this month! "
                f"<{tpl.url}>",
    )
```

### Recipe 6: Figma Friends ambassador surface

Figma's pattern:
- Ambassador badges visible in community + on profile.
- Ambassador-created components / files showcased in featured gallery.
- Ambassadors get early-access to features.

Cross-link to `ambassador-program-design` Recipe 4 for tier rubric.

```python
# Surface ambassador-authored content in product
def get_inspiration_feed(user):
    return Asset.objects.filter(
        author__is_ambassador=True,
        is_public=True,
    ).order_by("-engagement_score")
```

### Recipe 7: K-factor measurement

```sql
-- K-factor = (referrals_per_user) × (referral_conversion_rate)
WITH referrals AS (
  SELECT
    referrer_id,
    COUNT(*) AS referrals_sent,
    COUNT(*) FILTER (WHERE signed_up_at IS NOT NULL) AS referrals_converted
  FROM referral_attributions
  WHERE referrer_id IN (SELECT user_id FROM users WHERE signup_at BETWEEN now() - interval '90 days' AND now() - interval '30 days')
  GROUP BY referrer_id
)
SELECT
  AVG(referrals_sent) AS avg_invites_per_user,
  SUM(referrals_converted)::numeric / NULLIF(SUM(referrals_sent), 0) AS conversion_rate,
  AVG(referrals_sent) * (SUM(referrals_converted)::numeric / NULLIF(SUM(referrals_sent), 0)) AS k_factor
FROM referrals;
```

K-factor segments:
- Community-active users (posted ≥ 1 community message).
- Non-community users.
- Difference = community-driven K-factor lift.

### Recipe 8: Activation funnel with community drop-off catch

```sql
-- Each step in activation funnel + community catch effect
WITH funnel AS (
  SELECT
    user_id,
    MAX(CASE WHEN event = 'signup_completed' THEN 1 ELSE 0 END) AS signed_up,
    MAX(CASE WHEN event = 'activation_event_1' THEN 1 ELSE 0 END) AS step_1,
    MAX(CASE WHEN event = 'activation_event_2' THEN 1 ELSE 0 END) AS step_2,
    MAX(CASE WHEN event = 'activation_event_3' THEN 1 ELSE 0 END) AS aha,
    MAX(CASE WHEN event = 'community.joined' THEN 1 ELSE 0 END) AS joined_community,
    MIN(CASE WHEN event = 'community.joined' THEN timestamp END) AS community_join_at
  FROM events
  WHERE timestamp > now() - interval '60 days'
  GROUP BY user_id
)
SELECT
  joined_community,
  COUNT(*) AS n,
  AVG(signed_up::numeric) AS signed_up_rate,
  AVG(step_1::numeric) AS step_1_rate,
  AVG(aha::numeric) AS aha_rate
FROM funnel
GROUP BY joined_community;
```

Compare aha-rate between community-joined vs non. The lift quantifies community's role in PLG activation.

### Recipe 9: "Save attempt" via community DM on churn risk

```python
# Identify churn-risk: 14+ days no login but in trial / paid
churn_risk_users = posthog.query("""
SELECT distinct_id
FROM events
WHERE event = 'session_start'
GROUP BY distinct_id
HAVING max(timestamp) < now() - INTERVAL 14 DAY
   AND max(timestamp) > now() - INTERVAL 21 DAY
   AND any(properties.plan) IN ('trial', 'paid_member')
""")

for user_id in churn_risk_users:
    discord_id = lookup_discord_id(user_id)
    if discord_id and not has_recent_dm(discord_id, days=14):
        discord_full.create_dm(
            user_id=discord_id,
            content=(
                f"Hey! I'm @community-bot. Noticed you haven't logged in for a couple weeks. "
                f"Anything blocking you? Drop a message in #help and someone in the community will jump in. "
                f"Or just reply here."
            ),
        )
        posthog.capture(
            event="community.save_attempt_dm_sent",
            distinct_id=user_id,
            properties={"channel": "discord_dm"},
        )
```

Measure: save-attempt → next-30d-login conversion rate.

### Recipe 10: Quarterly PLG-community review

```markdown
# PLG-Community Review Q3 2026

## Funnel impact
| Step | Non-community | Community | Lift |
|---|---|---|---|
| Signup → activation step 1 | 62% | 78% | +16pp |
| Step 1 → aha | 41% | 59% | +18pp |
| Aha → trial-end conversion | 28% | 41% | +13pp |
| Paid → 12mo retained | 76% | 84% | +8pp |

## Handoff points status
| Point | Surface | Status | Notes |
|---|---|---|---|
| Trial-end nudge | "Join VIP" banner | ✓ Live | 8.2% click; 4% conv to community |
| Stuck nudge (day 7, no activation) | In-product modal | ✓ Live | 22% click; 11% activation lift |
| Template gallery | Home page | ✓ Live | 38% of users use community template in 30d |
| Save attempt DM | Discord DM | ⚠ Partial | 14% reply; rolling out to Slack next month |
| Champion AMA | Calendar widget | ✗ Not built | Q4 |

## K-factor
- Overall K = 0.32
- Community-active K = 0.61
- Non-community K = 0.18
- Community uplift: 3.4x K-factor

## What we ship next
- Champion AMA widget (target Q4)
- Slack save-attempt rollout
- Template-gallery "Created by tier X" badge experiment
```

## Examples

### Example 1: First-time PLG-community wiring (B2B SaaS)

**Goal:** Existing PLG SaaS, free Discord community sitting separate.

**Steps:**
1. Map handoff points (Recipe 1) — 8 points identified.
2. Instrument PostHog events (Recipe 2).
3. Build trial-end "Join VIP" nudge (Recipe 3).
4. Build stuck-user nudge (Recipe 9).
5. Quarterly review (Recipe 10).

**Result:** Trial → paid conversion +5pp in 90 days. Community joiners 2.3x more likely to convert.

### Example 2: Notion-style template gallery for a design tool

**Goal:** Surface community-created templates in-product.

**Steps:**
1. Build asset publication flow for community members.
2. Surface in onboarding (Recipe 5) for new users.
3. Attribution: badge each template "Created by @ambassador".
4. Track usage → milestone → community celebration (Recipe 5 webhook).

**Result:** 38% of new users use a community template within 7 days; ambassador retention +18%.

### Example 3: Linear-style help in community

**Goal:** Replace expensive support tier 1 with public community help.

**Steps:**
1. Public Slack workspace (no signup gate).
2. In-product "Live help ↗" widget.
3. Sales / SE rotation in #general.
4. Track resolution time + CSAT vs ticket-based.

**Result:** 18% of would-be tickets resolved via community at ~$0 marginal cost. Avg time-to-first-response 9 min vs 4hr for tickets.

## Edge cases / gotchas

- **Nudge fatigue** — too many in-product community nudges = banner blindness. Cap at 2 active prompts per user; rotate by stage.
- **Activation-defined-poorly** — "aha" must map to a real PostHog event the team agrees on. Otherwise PLG lift is illusory.
- **Mid-trial community joiners** — already-engaged users; convert higher regardless. Use causal inference (synthetic control, geo-split) for clean lift.
- **Privacy on save-attempt DMs** — unsolicited DMs to inactive paid users may feel creepy. Require opt-in at signup or use email instead.
- **Discord DM bot block** — many users disable DMs from server members. Fallback: email or in-product banner.
- **K-factor noise** — small cohorts give noisy K; require ≥ 200 invites per arm for credible compare.
- **Template-gallery quality** — opening template authoring to community can degrade quality. Curate top tier; require ambassador-tier approval for featured.
- **Ambassador burnout** — heavy reliance on a few champions for community help → they burn out. Distribute via "first responder rotation" + recognition.
- **Cross-functional friction** — product team doesn't see community as PLG lever. Show K-factor delta + activation lift to align.
- **Attribution complexity** — community joiner may have come from organic search, then community, then paid. Attribute via UTM source-of-truth + first-touch / last-touch alternates.
- **Community user_id ≠ product user_id** — Discord ID 12345 ≠ Stripe customer ID cus_abc. Build join table at signup (OAuth) or via email link.
- **Free-rider risk** — too much help in public community = paid customers don't see value in support tier. Tier-gate VIP office hours, while public help stays public.
- **Bot-prevention on community help** — anti-spam bots block legit AI-generated answers from new accounts. Whitelist community-bot account.
- **PLG-engineering bandwidth** — every nudge requires in-product work. Prioritize 3 nudges/quarter with measurable lift.

## Sources

- [Reforge — Community-Led Growth](https://www.reforge.com/blog/community-led-growth)
- [OpenView — CLG framework](https://openviewpartners.com/blog/community-led-growth/)
- [PostHog — PLG instrumentation](https://posthog.com/product-engineers/plg-metrics)
- [PostHog — K-factor measurement](https://posthog.com/tutorials/k-factor)
- [Linear customer community case](https://linear.app/blog/building-a-community)
- [Notion Champions program](https://www.notion.com/community/champions)
- [Figma Friends](https://www.figma.com/community)
- [Webflow University + forum](https://discourse.webflow.com/)
- [Stripe community programming](https://stripe.com/blog/community)
