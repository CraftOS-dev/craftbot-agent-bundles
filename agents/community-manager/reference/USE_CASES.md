# Community Manager — Use Cases

**Tier:** **general** · **Category:** community
**Core job:** End-to-end community operator for teams running real member volume — platform selection, charter + code of conduct, welcome flow, moderation, engagement programming, ambassador program, UGC, community-led growth measurement, Common Room CRM, member journey, events, gated tiers, Web3, ROI math, PLG motion, library curation.

> Ships with the SOTA community-operator stack (Circle / Discord / Slack / Discourse / Bevy / Skool platform expertise; Carl-bot / MEE6 / Dyno / Polly / Geekbot / Donut bot setup; Common Room community CRM; Contributor Covenant 2.1 CoC; Bevy / Lu.ma / Goldcast events; Memberstack / Outseta / Substack / Whop gating; Snapshot / Mirror / Lens / Collab.Land Web3; Brand24 / Threado sentiment; Productboard / Canny / Linear feedback) — executes end-to-end, not just direct. This file is bundled but **not** loaded into the agent's context.

---

## What this agent is supposed to do

### Community platform selection
- Score 5-7 candidate platforms (Circle / Discord / Slack / Discourse / Bevy / Skool / Mighty / Heartbeat / Substack / Whop)
- Decision matrix: audience habit × monetization × tooling depth × SEO need × moderation surface × team size
- 90-day setup checklist returned with recommendation
- 2026 pricing + migration cost named explicitly
- Flag wrong-platform decisions and propose alternative

### Community onboarding + welcome flow
- 7-day onboarding cascade per platform (Discord auto-greeter / Slack workflow / Circle native)
- Code-of-conduct acknowledgment gate
- First-week activation nudges (introduce-yourself, pinned threads, first question)
- KPI: % joiners posting in 7d (target 60%+)

### Community charter + code of conduct
- Charter authoring (purpose / audience / what to expect / what we ask / rules / dispute process)
- Code of conduct from Contributor Covenant 2.1 base
- Severity ladder (warn / mute / kick / ban)
- Appeals process
- Per-platform publish (Discord pin, Slack canvas, Circle About, Discourse FAQ, Reddit wiki)

### Moderation policies + automation
- Per-platform YAML rule packs (Discord AutoMod + Carl-bot + MEE6; Discourse trust levels + Akismet; Reddit AutoModerator; Slack admin controls)
- Severity ladder enforcement
- Bot stack deployment (MEE6 + Carl-bot + Dyno + Wick on Discord; Polly + Geekbot + Donut on Slack)
- Enforcement-action audit trail
- Anti-raid + spam-pattern + slur-filter + invite-filter

### Engagement programming
- 4-week editorial calendar with recurring formats (Monday motivation / Tuesday tactics / Wednesday wins / Thursday discussion / Friday wrap)
- Monthly AMA cadence
- Quarterly town hall
- Member spotlights (weekly + monthly member-of-the-month)
- Annual community wrap report

### AMAs end-to-end
- Pre-AMA (T-7): announcement, question form, speaker prep, tech check
- Live (T-0): run-of-show, queue management, lightning round, wrap
- Post-AMA (T+1 to T+7): top-Q&A digest, cross-post, archive, speaker thank-you

### Ambassador program design
- Tier rubric (Member → Contributor → Ambassador → Champion)
- Perks per tier (badge / exclusive channel / co-branded asset / quarterly swag / VIP summit)
- Common Room affinity screen for nomination (> 0.6 threshold)
- 1:1 personalized outreach via gmail-mcp
- Onboarding kit + quarterly check-ins + deactivation playbook

### UGC cultivation + spotlights
- Surface candidates via Common Room + Brand24 + community search
- Rights-request DM template (perpetual vs per-campaign vs 90-day)
- Notion UGC rights DB (audit trail)
- Repost with attribution + UTM
- FTC disclosure check via Vale
- Member spotlight cadence (weekly + monthly)

### Community-led growth (CLG) measurement
- Reforge CLG framework input → middle → output metrics
- Member → MQL conversion rate
- Members vs non-members retention curve (Day 1 / 7 / 30 / 90 / 180)
- Members vs non-members NRR delta
- Community-sourced referral close-rate vs paid CAC
- Support deflection rate (community-answered % of would-be tickets)
- dbt model joining Common Room members → HubSpot deals → product events → revenue

### Common Room community CRM operations
- Integration setup (Slack / Discord / GitHub / Twitter / LinkedIn / Reddit / Discourse / Circle / forum)
- Identity-resolution across platforms
- Affinity scoring + segments (Champions / At-risk / New ambassadors)
- Activity feed monitoring (champion off-network alert)
- HubSpot custom-property writeback for CRM visibility

### Member journey design (lurker → ambassador)
- Journey stage rubric (Lurker → Reader → Reactor → Commenter → Contributor → Connector → Ambassador → Champion)
- Stage-specific nudges (DM + channel prompts + role unlocks)
- Weekly journey-stage migration report
- Quarterly cohort retention by stage

### Community events (virtual + in-person + Bevy)
- Event-type decision (intimate / hybrid / large-scale virtual / in-person regional / chapter-based)
- Tool recommend (Lu.ma / Goldcast / Bevy / Eventbrite / Zoom + Discord Stage)
- Run-of-show + speaker brief + attendee comms cascade
- Post-event: attendee sync to Common Room + thank-you cascade + top-Q&A digest

### Discord bot setup
- MEE6 (leveling + welcome + auto-mod baseline)
- Carl-bot (advanced auto-mod + reaction roles + embed templates)
- Dyno (anti-raid + moderation logs)
- Wick (anti-raid premium)
- AutoMod (slur + invite + spam patterns)
- Statbot (analytics)
- Tickets (DM-to-ticket bridge)
- Collab.Land / Vulcan (NFT-token-gated roles)

### Slack bot setup
- Polly (polls + pulse surveys)
- Geekbot (async standups)
- Donut (member-to-member intro coffees)
- Standuply (alt standup)
- Workast (task tracking)
- Birthday Bot (recognition)
- Native Slack workflows (onboarding + recurring reminders)

### Community analytics (Common Room / Insider Notable / dashboards)
- Weekly digest (active members, posting frequency, sentiment, top topics, champion activity)
- Cohort segmentation (by join cohort, by journey stage, by channel)
- Common Room / Notable (paid) + Threado (SMB) + custom PostHog + warehouse → Metabase / Looker

### Sentiment monitoring in community
- Cross-platform via Brand24 (sarcasm + slang model)
- In-community via Common Room native sentiment
- Per-post Claude scoring as free fallback
- Per-channel cohort trend (alert on > 20% WoW decline)
- Root-cause hypothesis + comms playbook on alert

### Community feedback loop → product
- Daily poll feedback channel (Discord / Slack / Discourse / Circle)
- Cluster via embeddings (threshold ≥ 5 unique members)
- Push to Productboard / Canny / Linear with `community-source` label
- Member-list attribution
- Reverse-sync on ship (tag original posters with release announcement)
- Weekly + monthly + quarterly status cadence

### Gated community access
- Memberstack (Webflow-friendly paywall)
- Outseta (all-in-one CRM + paywall + community)
- Substack Paid (newsletter + Chat + Notes)
- Whop (creator gated Discord access)
- Skool (course + community bundle)
- Patreon / Ko-fi (creator subscription)
- Role-sync webhook (Memberstack → Discord role on payment event)
- Tier-perks difference enforcement

### Web3 community ops
- Snapshot off-chain governance voting
- Mirror token-gated content publishing
- Lens Protocol decentralized social graph
- Collab.Land NFT-token-gated Discord/Telegram roles
- Farcaster crypto-native social
- Cross-publication coordination

### Community ROI (retention + expansion + advocacy + deflection + brand love)
- Reforge 5-dim framework
- Retention lift: member_LTV vs non_member_LTV delta * customer_count
- Expansion lift: member_NRR vs non_member_NRR delta * ARR_base
- Advocacy lift: community-source close-rate / paid close-rate * paid_CAC * referral_count
- Support deflection: community_answered_count * cost_per_ticket
- Brand love delta: NPS / share-of-positive-sentiment vs control
- Board-grade pptx with comparison cohort + assumptions + statistical significance

### Community-led PLG motion
- PLG → community handoff points (signup → join nudge; first-aha → community pinpoint; trial-end → community help nudge; churn risk → CSM in community; power user → ambassador)
- PostHog event instrumentation (community.joined, community.first_post, community.ambassador_promoted)
- K-factor + time-to-aha + activation% + retention curve
- Member-vs-non-member retention comparison

### Community library + KB curation
- Notion / Slab / Tettra / Stack Overflow for Teams selection
- Weekly drift report (articles unviewed in 90d, zero-result searches, dead links via Lychee)
- Content-gap audit (top community feedback themes vs existing KB)
- Auto-draft new KB entries with member-question citations
- Cross-link from KB to community for "still stuck?" path

### Bevy chapter program operation
- Chapter standards + toolkit + speaker pool
- Chapter lead recruitment (sourcing + application + interview + onboarding)
- Bevy event creation + RSVP + venue + speaker brief
- Post-event sync (attendees → Common Room + chapter-lead retrospective)

### Discourse FOSS forum operation
- Self-hosted Discourse setup (Docker $5 VPS)
- Trust levels (TL0 → TL4) auto-moderation
- Akismet + bouncer + watched-words plugins
- Theme components for branding
- SEO optimization (sitemap + indexable pages + cross-link to KB)

### Streaming community (Twitch / YouTube Live / Discord Stage)
- Multi-platform broadcast via Restream / Streamyard
- Chat bot stack (Nightbot / StreamElements / Streamlabs)
- Highlight clip extraction post-stream (via ffmpeg + Twitch clip API)
- Cross-post highlights to community Discord / Slack / newsletter

### Newsletter+community hybrid (Substack / Beehiiv / Subkit)
- Newsletter → community thread auto-open
- Community responses → next newsletter post
- Subscriber → community handoff
- New community member → opt-in newsletter form

### Beta program management
- Private Discord channel / Circle space with `beta` role
- Beta-rules charter (non-disclosure, feedback expectations, exit criteria)
- Structured bug template
- Feedback → Linear with `beta-feedback` label
- Weekly beta cohort digest
- Beta → GA cutover comms

### Reddit ops + AMAs
- Own subreddit (r/yourproduct) management
- AutoModerator YAML rules in subreddit wiki
- Toolbox Chrome extension for mod power tools
- AMA in r/IAmA (verification + cross-promote + post-AMA digest)
- Subreddit health audits for cross-posting

### Community swag + recognition
- Recognition cadence (weekly spotlight / monthly member-of-month / quarterly ambassador kit / annual VIP summit)
- Swag tier table (Member sticker → Contributor T-shirt → Ambassador quarterly kit → Champion VIP)
- Reachdesk / Sendoso execution for B2B at scale
- Printful DTC fallback for per-item ordering

---

## Execution status (SOTA — June 2026)

Every documented use case has a concrete SOTA execution mechanism. The "draft only, can't act" gaps are closed via shipped MCPs (Discord / Slack / Discourse via Discourse + reddit / Linear / PostHog / Stripe / Twitter / Twitch / YouTube / WhatsApp / WeChat / LINE / Zoom / Shopify / Notion / Gmail / Postgres) and well-documented APIs (Circle / Bevy / Lu.ma / Common Room / Notable / Threado / Brand24 / Productboard / Canny / Memberstack / Outseta / Substack / Whop / Skool / Snapshot / Mirror / Lens / Mavrck / SocialLadder / Reachdesk / Sendoso) reachable through `cli-anything` curl.

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Community platform selection | Circle / Discord / Slack / Discourse / Bevy / Skool / Mighty / Substack / Whop | `community-platform-selection-circle-discord-slack-discourse` skill + `cli-anything` Firecrawl pricing |
| Community onboarding + welcome flow | MEE6 / Carl-bot / native Slack workflows / Circle native | `discord-mcp-full schedule_message` + `slack-mcp` workflow + `cli-anything` curl Circle |
| Charter + code of conduct | Contributor Covenant 2.1 base + Notion SoT | `notion-mcp` + per-platform-API push |
| Moderation policies + automation | Discord AutoMod + Carl-bot + Discourse trust levels + Reddit AutoMod | `discord-mcp-full set_automod_rules` + `cli-anything` curl + `reddit-mcp` |
| Engagement programming | Notion editorial calendar + scheduled posts per platform | `discord-mcp-full schedule_message` + `slack-mcp chat_scheduleMessage` |
| AMAs end-to-end | Discord Stage / Twitch / Zoom + Notion AMA DB | `discord-mcp-full` + `twitch-mcp` + `zoom-mcp` + `notion-mcp` |
| Ambassador program design | Common Room nominate + Mavrck / SocialLadder / Bevy Ambassadors | `cli-anything` Common Room API + `gmail-mcp` |
| UGC cultivation + spotlights | Common Room + Brand24 + native repost + Notion rights DB | `cli-anything` + `notion-mcp` + `discord-mcp-full` / Circle / Slack |
| CLG measurement | Reforge framework + Common Room + dbt + warehouse | `postgresql-mcp` + `posthog-mcp` + `cli-anything` |
| Common Room community CRM | Common Room API | `cli-anything` curl Common Room |
| Member journey design | Common Room activity scoring + journey-stage rubric | `cli-anything` + `discord-mcp-full` DM + `gmail-mcp` |
| Community events | Bevy + Lu.ma + Goldcast + Eventbrite + Zoom Events | `cli-anything` curl + Common Room sync + `zoom-mcp` |
| Discord bot setup | MEE6 + Carl-bot + Dyno + Wick + Statbot | `discord-mcp-full` + `playwright-mcp` (dashboards) |
| Slack bot setup | Polly + Geekbot + Donut + Standuply | `cli-anything` Slack Admin API + Polly/Geekbot APIs |
| Community analytics | Common Room + Notable + Threado + custom PostHog | `cli-anything` + `posthog-mcp` + `postgresql-mcp` |
| Sentiment monitoring | Brand24 + Common Room native + Claude fallback | `cli-anything` Brand24 + Claude per-post |
| Feedback loop → product | Productboard + Canny + Linear + Featurebase | `cli-anything` Productboard + `linear-mcp` |
| Gated community access | Memberstack + Outseta + Substack + Whop + Skool | `cli-anything` curl + Discord/Slack role-sync webhook |
| Web3 community ops | Snapshot + Mirror + Lens + Collab.Land + Farcaster | `cli-anything` curl Snapshot Graph + Mirror REST |
| Community ROI 5-dim | Reforge model + Common Room + warehouse | `postgresql-mcp` + dbt + `posthog-mcp` |
| Community-led PLG motion | PostHog event instrumentation + Discord/Slack join nudge | `posthog-mcp` + `discord-mcp-full` + `slack-mcp` |
| Library + KB curation | Notion + Slab + Tettra + Stack Overflow for Teams | `notion-mcp` + `cli-anything` Lychee link sweep |
| Bevy chapter program | Bevy + chapter playbook | `cli-anything` Bevy API + Common Room sync |
| Discourse FOSS forum | Discourse + Akismet + Discourse Theme CLI | `cli-anything` curl Discourse REST |
| Streaming community | Twitch + Kick + YouTube Live + Discord Stage + Nightbot | `twitch-mcp` + `youtube-mcp` + `discord-mcp-full` |
| Newsletter+community hybrid | Substack + Beehiiv + Subkit + Kit | `cli-anything` curl + cross-post pipeline |
| Beta program management | Centercode + private Discord channel + Linear sync | `discord-mcp-full` + `linear-mcp` |
| Reddit ops + AMA | r/yourproduct + AutoMod YAML + Toolbox + r/IAmA playbook | `reddit-mcp` + `cli-anything` AutoMod config |
| Community swag + recognition | Reachdesk + Sendoso + Postal + Printful DTC | `cli-anything` curl Reachdesk + manual DTC fallback |

---

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Common Room community CRM | ⚠ | Paid Starter+ tier required; HubSpot custom property + Notion-CRM is free fallback |
| Mavrck / SocialLadder ambassador platform | ⚠ | Paid SaaS; Common Room + manual outreach + HubSpot custom property is free fallback |
| Brand24 / Talkwalker sentiment | ⚠ | Paid SaaS; Claude per-post scoring on transcript is free fallback |
| Notable / Threado community CRM | ⚠ | Paid SaaS; custom PostHog event stream + Metabase dashboards is free fallback |
| Bevy community-led events | ⚠ | Org-level paid subscription; Lu.ma / Eventbrite are free alts for non-chapter events |
| Reachdesk / Sendoso swag | ⚠ | Paid SaaS + per-shipment funded; Printful / Printify DTC manual ordering is fallback |
| Centercode beta program | ⚠ | Paid enterprise; private Discord channel + Linear sync covers most needs |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a concrete execution path. The 5% residual is paid SaaS APIs the recipient owns (Common Room, Mavrck/SocialLadder, Brand24, Notable, Bevy, Reachdesk, Centercode) — each has a documented free or open-source fallback. The previous "community manager only drafts strategy decks" gap is closed via shipped MCPs (Discord / Slack / Reddit / Linear / Twitch / YouTube / Notion / Postgres / PostHog / Stripe / Shopify / Zoom) and `cli-anything` curl against documented APIs.

---

## When to use this agent

- "Help me pick the right community platform for a B2B SaaS support deflection use case"
- "Write our community charter + code of conduct based on Contributor Covenant"
- "Set up a 7-day onboarding flow for our new Discord"
- "Deploy a moderation rule pack for our Discord (Carl-bot + MEE6 + AutoMod)"
- "Plan our 4-week engagement calendar with themed days + monthly AMA"
- "Design our ambassador program with tiers + perks + nomination workflow"
- "Surface UGC candidates from Common Room and send rights-request DMs"
- "Calculate our community ROI across the 5 Reforge dimensions for the board"
- "Set up Common Room and pipe affinity scores back to HubSpot"
- "Build the journey-stage migration report (Lurker → Ambassador)"
- "Schedule a community town hall via Bevy or Lu.ma + run-of-show"
- "Set up our gated paid Discord with Memberstack role-sync"
- "Configure Snapshot governance + Collab.Land token-gating for our DAO"
- "Sentiment dropped 25% WoW in #feedback — run the playbook"
- "Push this week's #feedback cluster to Productboard with member attribution"
- "Curate our community KB — drift report + zero-result gaps"
- "Set up our Discourse forum with trust levels + Akismet + theme"
- "Run our quarterly AMA in r/IAmA with verification + cross-promote"
- "Build the community-streaming cadence with Twitch + Discord Stage"
- "Ship the Q2 ambassador swag kit via Reachdesk"

## When NOT to use this agent

- Paid brand campaigns + multi-channel ads — hand off to `marketing-agent`
- Public social posting + DMs at scale (LinkedIn / X / IG / TikTok) — hand off to `social-media-manager`
- Ticket triage / SLA / refund execution / KB-as-support — hand off to `customer-support-agent`
- Post-sale relationship + expansion motion + customer-health scoring + QBR planning — hand off to `customer-success`
- Newsletter mechanics + lifecycle email build (Substack/Beehiiv lifecycle) — hand off to `email-strategist`
- Long-form content + pillar articles + case studies — hand off to `content-creator`
- 30-minute YouTube production / video editing / thumbnail design — hand off to `video-creator`
- Developer docs / API reference / tutorial systems — hand off to `technical-writer`
- Engineering work for the community-tooling stack itself — hand off to `senior-python-engineer`
- Legal review of community ToS / DMCA / privacy compliance — flag for legal sign-off
- Real-time crisis comms across mainstream media — coordinate with `pr-comms`
