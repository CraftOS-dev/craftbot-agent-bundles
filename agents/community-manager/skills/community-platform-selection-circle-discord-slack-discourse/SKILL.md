<!--
Sources: https://www.circle.so/pricing + https://discord.com/safety + https://api.slack.com + https://meta.discourse.org/ + https://www.mightynetworks.com/ + https://bevy.com/ + https://www.skool.com/ + https://www.heartbeat.chat/
-->
# Community Platform Selection — SKILL

Decision matrix for picking the right community home: Circle / Discord / Slack / Discourse / Bevy / Skool / Mighty Networks / Heartbeat / Substack / Outseta / Memberstack / Whop. Output is a ranked recommendation with 2026 pricing, capability map, and migration-cost notes.

## When to use

- Founder asks "where should I host my community?" (most common starting question).
- Existing community is on the wrong platform — symptom: <2% weekly posting rate, runaway moderation cost, no SEO surface, no monetization path.
- Multi-region expansion forcing a re-platform (e.g., adding a paid tier requires Outseta / Memberstack / Circle Paid Memberships).
- Audit before a Round 2 community-led-growth bet — wrong platform caps the ceiling.
- B2B vs B2C vs creator-economy vs OSS — each has a different SOTA platform.

Trigger phrases: "which community platform", "Circle vs Discord", "should we move to Discourse", "gated community platform", "newsletter community platform".

## Setup

```bash
# Firecrawl MCP for live pricing-page diffing (already in agent.yaml)
mcp tool firecrawl.scrape --url https://www.circle.so/pricing --formats markdown

# Brave / DDG for SERP — competitor-platform reviews
mcp tool brave-search.web_search --query "Circle vs Mighty Networks 2026"

# Notion MCP for the decision matrix output
mcp tool notion.create_page --parent_id $NOTION_DB --title "Platform recommendation: $BRAND"
```

Workspace prerequisites:
- Notion DB with cols `Platform | Monthly cost | Audience fit | Mod surface | SEO | Monetization | Migration cost | Score`.
- Optional: Common Room sandbox (`commonroom.io`) for evaluating Circle / Discord integration coverage.

## Common recipes

### Recipe 1: Structured intake (8 questions)

Before recommending anything, gather:
1. Goal (support / advocacy / paid product / OSS / events).
2. Audience size (today and 12mo target).
3. Audience habit (tech-savvy / casual / enterprise / Web3 / creator-economy).
4. Monetization model (free / freemium / paid tier / course bundle / DAO).
5. Tech literacy of mod team (dev / marketer / VA).
6. SEO need (community-as-SEO surface y/n).
7. Real-time vs forum-style discussion preference.
8. Team headcount on community ops.

### Recipe 2: Apply the decision matrix

| Platform | Best for | Pricing tier (2026) | SEO | Real-time | Monetization | Mod depth |
|---|---|---|---|---|---|---|
| Circle | SaaS / brand community + paid courses | Pro $99 / Business $399 / Enterprise custom | No | Limited | Native paid memberships | Medium |
| Discord | Real-time + voice + gaming + creator + Web3 | Free (Nitro perks) | No | Yes | Patreon / Whop integration | High via bots |
| Slack | B2B + paid enterprise + design partners | Free / Pro $7.25/mo/user / Business+ $12.50 | No | Yes | Indirect | Medium |
| Discourse | OSS / FOSS / community-as-SEO | Self-host free or Hosted $50–500/mo | Yes (best) | No | Donate / Patreon | Trust-levels (excellent) |
| Bevy | Chapter-based enterprise community + events | Custom enterprise | No | No | Indirect | N/A |
| Skool | Course + community bundle | $99/mo flat | Limited | Limited | Native paid | Medium |
| Mighty Networks | Course + community + paid | Community $41 / Business $119 / Plus $360 | Limited | Limited | Native paid | Medium |
| Heartbeat | SMB creator-led | $9–149/mo | No | Yes | Native paid | Medium |
| Substack | Newsletter + community + paid | Free + 10% revenue | Yes | No | Native paid (sub) | Low |
| Memberstack | Gated community paywall (any host) | $25–199/mo | n/a | n/a | Native paid | n/a (it's auth) |
| Outseta | All-in-one CRM + paywall + community | $39–349/mo | Some | Limited | Native paid | Medium |
| Whop | Creator-economy gated Discord access | Free + 3% revenue | No | n/a | Native paid | n/a (gate only) |

### Recipe 3: Live pricing diff (Firecrawl)

```bash
# Pricing pages change quarterly — never quote stale numbers
for url in \
  "https://www.circle.so/pricing" \
  "https://www.mightynetworks.com/pricing" \
  "https://www.skool.com/about" \
  "https://www.heartbeat.chat/pricing" \
  "https://www.memberstack.com/pricing" \
  "https://www.outseta.com/pricing" \
  "https://whop.com/business"; do
  mcp tool firecrawl.scrape --url "$url" --formats markdown --only_main_content true \
    | jq -r '.markdown' > "pricing_$(echo $url | md5sum | cut -c1-8).md"
done
```

Diff against last run; flag price changes >10%.

### Recipe 4: Migration-cost estimator

```python
MIGRATION_COST_DAYS = {
  ("discord", "circle"): 14,   # member CSV export + invites; lose voice
  ("circle", "discord"): 7,
  ("slack", "discord"): 21,    # auth diverges, channel re-map
  ("any", "discourse"): 30,    # taxonomy re-design + theming
  ("substack", "circle"): 14,
  ("circle", "skool"): 10,
}
```

Always include "12-month total cost of ownership" — platform fee × 12 + mod headcount × $X + migration days × consulting rate.

### Recipe 5: Output ranked recommendation to Notion

```bash
mcp tool notion.create_page \
  --parent_id $RECO_DB \
  --title "Platform reco for $BRAND ($DATE)" \
  --properties '{
    "Top pick": "Circle",
    "Runner-up": "Discord",
    "Why": "Paid memberships native + 200+ members already on email list; SEO not a goal",
    "12mo TCO": "$4,788 (Pro plan) + migration $3k",
    "Trade-offs": "No real-time voice; need Discord later for power-users"
  }'
```

### Recipe 6: Decision rules (default playbook)

- **OSS / SDK / dev tooling** → Discourse + GitHub Discussions.
- **B2B SaaS, mid-market** → Slack (design partners) + Circle (broader community).
- **Creator economy with paid tier** → Whop-gated Discord or Skool.
- **Course business** → Skool or Mighty Networks (course + community bundle).
- **Newsletter primary** → Substack + Substack Chat; add Discord only at scale.
- **Web3 / DAO** → Discord + Snapshot + Mirror + Collab.Land.
- **Enterprise community at scale** → Bevy chapters + Circle/Slack base.
- **SMB creator-led, casual** → Heartbeat or Circle Basic.

## Examples

### Example 1: SaaS founder, 800 users, no community yet

**Intake:** B2B SaaS dev-tools, 800 paying customers, mostly devs, want feedback loop + champion identification, mod team = 1 marketer + 1 founder, no SEO need.

**Recommendation:** Slack (design-partner channel for top 50) + Discourse (broader community-as-SEO + bug reports + feature requests indexed in Google). Skip Discord — wrong density for B2B asynchronous discussion.

**12mo TCO:** Slack Pro ~$1,000 (top 50 invited free) + Discourse self-hosted $0 or hosted $600. Migration: zero (greenfield).

### Example 2: Creator with 2k newsletter subs, wants paid community

**Intake:** Solo creator, 2k newsletter, wants $20/mo paid tier with private Discord, no enterprise.

**Recommendation:** Whop + Discord (creator-economy SOTA). Whop handles paywall + role-sync to private Discord; Stripe-backed. Substack Chat is a free fallback if creator doesn't want a new login surface.

**12mo TCO:** Whop 3% revenue cut ($720 on $24k ARR) + Discord free. Migration: 2 days.

## Edge cases / gotchas

- **Don't pick on features alone** — audience habit beats feature richness. Devs avoid Mighty; non-tech audiences struggle with Discord channels.
- **Multi-platform fragmentation** — running Circle + Discord + Slack triples mod load. Pick one primary; others are spokes.
- **Pricing on the wrong tier** — Circle Pro 100 member cap is a frequent surprise; check the cap before recommending.
- **SEO assumption** — only Discourse and Substack are indexed by Google. Circle, Discord, Slack are dark to search.
- **Discord ≠ free at scale** — voice / video on a 10k-server requires Nitro perks for raid protection, custom bots ($), and at least one paid mod.
- **Migration breaks identity** — usernames don't carry over; pre-warn members + send "claim your handle" DM during cutover.
- **Substack now competes with Twitter / Notes** — but its "community" is mostly comments + Chat; not a real forum substitute.
- **Whop's revenue cut compounds** — at $1M+ ARR, 3% becomes $30k/yr; revisit at $250k ARR threshold.
- **Outseta locks you in** — CRM + paywall + community + email all coupled; migration cost is brutal. Recommend only if budget for "all in".
- **Don't ignore Mattermost / Rocket.Chat / Element** for privacy-first / self-host requirements.

## Sources

- [Circle pricing](https://www.circle.so/pricing)
- [Discord safety + community](https://discord.com/safety)
- [Discourse meta](https://meta.discourse.org/)
- [Mighty Networks](https://www.mightynetworks.com/)
- [Skool](https://www.skool.com/)
- [Heartbeat](https://www.heartbeat.chat/)
- [Bevy](https://bevy.com/)
- [Memberstack](https://www.memberstack.com/)
- [Outseta](https://www.outseta.com/)
- [Whop](https://whop.com/)
- [Substack community](https://substack.com/community)
