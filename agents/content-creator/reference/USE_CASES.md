# Content Creator — Use Cases

**Tier:** **specialized** · **Category:** marketing (sits under marketing alongside `marketing-agent` + `video-creator`)
**Core job:** Multi-format content operator — newsletters, podcasts, repurposing pipelines, content series, LinkedIn carousels, X threads, audiograms, infographics, creator-economy distribution + monetization.

> Ships with the SOTA content-creator stack (Beehiiv MCP + Ghost / Kit APIs + Castmagic / Otter + Podchaser + Descript / Riverside APIs + Submagic + Headliner + Typefully agent CLI + Postiv / Carosello + Buffer MCP + Patreon v2 / Memberstack / Circle) — executes publish + repurpose + cascade + analyze end-to-end, not just draft.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

---

## What this agent is supposed to do

### Long-form newsletter operations
- Weekly / biweekly / monthly newsletter authoring (Beehiiv / Substack / Ghost / Kit)
- Platform decision (Beehiiv = media product; Ghost = independent publisher CMS; Kit = course creator + automation; Substack = low-friction start)
- Newsletter issue templates (subject line + preheader + headline + hook + body + takeaway + CTA)
- Newsletter brand voice + Vale slop scrub
- Newsletter scheduled publish (Tuesday 6am ET SOTA default)
- Newsletter subscriber growth tactics (Beehiiv referrals + Boosts + Kit tag flows + Ghost paywalls)
- Newsletter audience surveys (Beehiiv polls + Typeform / Tally embeds)

### Podcast scripting + production
- Episode script authoring (interview / monologue / panel / narrative)
- Pre-recorded show notes (the SEO + repurposing source-of-truth)
- Post-record show notes via Castmagic / Otter from transcript
- Podcast trailer creation (60-90s 3-act)
- Podcast guest research via Podchaser API (32M+ structured credits)
- Podcast guest outreach via `gmail-mcp` with personalized templates
- Podcast guest preparation packets (auto-generated)
- Podcast editing brief (Descript media import + Riverside multitrack)
- Podcast SEO (titles + descriptions + chapters via `<podcast:chapter>` for Google Key Moments)
- Podcast back-catalog audit + re-promotion

### Multi-format content series planning
- Content series arc design (4-12 tentpoles around one thesis)
- Tentpole + child schema in Notion editorial DB
- Per-tentpole + per-derivative format/platform/timing decisions
- Series KPI design + post-arc retrospective

### Repurposing pipelines (one-to-many)
- 1 tentpole → 10+ derivatives chain (mandatory; never one-off)
- Audio/video → text derivatives (Castmagic / Otter)
- Long-form video → short-form clips (OpusClip / Opus Pro / Munch)
- Short-form caption + B-roll (Submagic Business+ API)
- Text → LinkedIn carousel (Postiv / Carosello)
- Text → thread cascade (Typefully)
- Podcast → audiogram (Headliner RSS autopilot or ffmpeg)
- Cross-platform scheduling (Buffer GraphQL + MCP)

### Short-form video scripting (defers production to video-creator)
- 3-second hook + 30-60s structure
- 40/30/20/10 content pillar mix (educational / entertainment / inspirational / promotional)
- Reels / TikTok / Shorts / YouTube Shorts scripting

### LinkedIn carousel authoring
- 8-14 slide structure (hook + body + CTA)
- Authoring via Postiv / Carosello / Taplio (1.6× engagement vs text)
- Branded layout via Canva MCP
- Mobile typography + branded layout standards

### X / Threads / Bluesky / Mastodon thread authoring
- Rule of 7 scroll-stoppers
- Pyramidal structure (thesis → body → CTA)
- Typefully agent CLI cascade across X + LinkedIn + Threads + Bluesky + Mastodon

### Audiogram production
- Headliner Pro RSS autopilot (auto-per-episode + auto-YouTube)
- Manual via Wavve when handcrafted promo needed
- ffmpeg waveform overlay fallback

### Infographic briefing + design
- Data-heavy via Piktochart AI outline (URL/PDF → structured outline + matched template)
- Branded social-style via Canva MCP
- Marketing-polished via Adobe Express

### Cross-platform publishing cascade
- Buffer GraphQL + MCP (10+ platforms, one auth, per-platform text variants)
- Typefully cascade (thread-first to X / LinkedIn / Threads / Bluesky / Mastodon)
- Native platform MCPs (`twitter-mcp`, `tiktok-mcp`, `insta-business-mcp`, etc.) for native features

### Monetization stack design
- 3-tier minimum (cheap + median + premium); 2.5-5× price spread
- Patreon v2 (with iOS 30% fee flag post-Nov 2026)
- Memberstack (96% creator take; better for mobile-heavy)
- Circle (flat fee community + monetization)
- Newsletter paid tiers (Beehiiv / Ghost 0% revenue share; Substack 10%)
- Sponsorship inventory (host-read 4× recall vs pre-roll)
- Ad network integration

### Brand partnership / creator collaboration briefing
- Brand brief template (audience / deliverables / timeline / rights / compensation / FTC compliance)
- Podchaser-driven podcast collab discovery
- Outreach via `gmail-mcp`

### Podcast sponsorship integration
- Host-read sponsor script authoring (in brand voice; 4× recall vs pre-roll)
- Dynamic ad insertion (DAI) brief per podcast host
- Sponsor inventory rate-card design

### Content analytics + measurement
- Newsletter: CTR / CTOR / revenue per recipient (never opens alone)
- Podcast: Listen-through rate (50% at 25-min = pro), Chartable / Podtrac cross-platform
- YouTube: avg view duration + retention curve via Data API v3
- Social: engagement rate per format (carousel 6.6% vs text 1.11%)
- Cross-format roll-up: UTM-tag + PostHog / GA4 / Plausible

### Content calendar + editorial DB maintenance
- Notion DB with parent (tentpole) + child (derivative) schema
- Per-row properties: format, channel, owner, deadline, KPI, repurposing status
- Sync to Google Calendar for personal scheduling

### AI-assisted ideation + drafting
- 30-angles brainstorming
- Hook variation
- Vale slop scrub before publish
- `humanize-ai-text` skill enforcement

---

## Execution status (SOTA — June 2026)

The mid-2026 SOTA content-creator stack closes every documented "draft only, can't publish/repurpose/analyze" gap. Beehiiv MCP shipped March 24, 2026 (read-only V1, V2 write committed); Castmagic ships native Claude MCP for repurposing; Typefully CLI (`npx typefully`) cascades threads to 5 platforms; Descript + Riverside expose media-import APIs; Buffer GraphQL covers 10+ social platforms; Patreon v2 + Memberstack + Circle expose REST APIs for monetization stacks. The remaining gaps are GUI-bound editing (Descript timeline ops; Headliner has no public API but RSS autopilot covers most) and per-host DAI standardization for podcast dynamic ad insertion.

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Long-form newsletter (Beehiiv) | Beehiiv MCP (V1 read; V2 write committed) | `cli-anything` + `npx @beehiiv/mcp-server` |
| Long-form newsletter (Ghost) | Ghost Admin API | `cli-anything` + curl `POST /ghost/api/admin/posts/` |
| Long-form newsletter (Substack) | Manual publish; analytics via `firecrawl-mcp` scrape | `cli-anything` + `firecrawl-mcp` |
| Long-form newsletter (Kit) | Kit REST API | `cli-anything` + curl `https://api.convertkit.com/v3/` |
| Podcast script + show notes | Claude + Castmagic MCP + Otter Chat | `cli-anything` + Castmagic Claude MCP / Otter API |
| Podcast guest research | Podchaser GraphQL API | `cli-anything` + curl Podchaser |
| Podcast guest outreach | Notion pipeline + Gmail templates | `notion-mcp` + `gmail-mcp` |
| Podcast editing brief | Descript API import + Riverside multitrack pull | `cli-anything` + curl Descript + Riverside |
| Podcast trailer creation | Claude script + ElevenLabs voice + Descript brief | `cli-anything` + `elevenlabs-mcp` |
| Content series arc | Notion editorial DB parent/child schema | `notion-mcp` |
| Repurposing pipeline (1→10) | Castmagic + OpusClip + Submagic + Headliner chain | `cli-anything` chain |
| Short-form scripting | Claude + Submagic Business+ API | `cli-anything` + Submagic |
| LinkedIn carousel | Postiv / Carosello + Canva MCP | `cli-anything` + Postiv/Carosello + `canva-mcp` |
| X / Threads / Bluesky thread | Typefully agent CLI cascade | `cli-anything` + `npx typefully` |
| Audiogram (preferred) | Headliner Pro RSS autopilot | Pro plan + RSS feed configured |
| Audiogram (fallback) | ffmpeg waveform + Whisper subtitles | `cli-anything` + ffmpeg + Whisper |
| Infographic (data-heavy) | Piktochart AI outline (manual) | `cli-anything` + curl Piktochart |
| Infographic (branded social) | Canva MCP template instantiation | `canva-mcp` |
| Monetization stack design | Patreon v2 + Memberstack + Circle stack analytics | `cli-anything` + per-platform curl |
| Newsletter subscriber growth | Beehiiv referrals + Boosts + Kit flows | Beehiiv MCP + Kit API |
| Content analytics (newsletter) | Beehiiv MCP `get_post_analytics` + Ghost + Kit + Substack scrape | Mixed MCP + curl + `firecrawl-mcp` |
| Content analytics (podcast) | Spotify / Apple manual + Chartable + Podtrac | Manual + curl |
| Content analytics (YouTube) | YouTube Data API v3 (videos.list + retention) | `youtube-mcp` |
| Newsletter audience survey | Beehiiv polls + Typeform / Tally embed | Beehiiv MCP + curl |
| Editorial calendar (Notion DB) | Notion DB parent/child schema + tentpole/derivative rows | `notion-mcp` |
| Podcast SEO | RSS `<podcast:chapter>` + Google Key Moments + title front-load | `cli-anything` + curl podcast host API |
| Podcast back-catalog re-promo | Host API top-N evergreen → Castmagic → Buffer cascade | `cli-anything` chain |
| Cross-platform publishing cascade | Buffer GraphQL + MCP (Feb 2026 GA) | Buffer MCP via `cli-anything` |
| Brand partnership briefing | Brief template + FTC compliance + Gmail outreach | Authored markdown + `gmail-mcp` |
| Podcast sponsorship integration | Host-read script (4× recall) + per-host DAI | Claude scripting + manual placement |
| AI-assisted ideation + slop scrub | Claude + `brainstorming` skill + `humanize-ai-text` skill | Skills + `cli-anything` |

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Beehiiv MCP write (publish, send, modify subs) | ⚠ | V1 read-only as of March 24, 2026; V2 write committed by Beehiiv. Ghost / Kit cover full write via REST in the meantime. |
| Descript timeline editing operations | ⚠ | API enables media import + edit-in-partner handoff; cuts / fades / transitions / level adjustments are GUI-bound in Descript itself. Brief is full; human or ElevenLabs voice-replacement + ffmpeg cuts via `cli-anything` cover most segment-level ops. |
| Riverside editing operations | ⚠ | Business plan API covers transcript + media retrieval; no editing operations (cuts, fades) via API yet. Pair with Descript for editing. |
| Headliner public API | ⚠ | No public API; RSS autopilot covers per-episode auto-generation + auto-YouTube. ffmpeg fallback for custom variants. |
| Substack public API | ⚠ | No public API for write or analytics. `firecrawl-mcp` scrape for stats; manual publish or migration recommended. |
| Patreon iOS 30% fee | ⚠ | Apple in-app purchase mandate enforced Nov 2026. Flag mobile-sub % > 40 → recommend Memberstack / Circle / web-only checkout. |
| Podcast Dynamic Ad Insertion (DAI) | ⚠ | Per-host implementation varies (Buzzsprout / Captivate / Transistor / Megaphone / Acast all differ). Host-read scripting remains universal and outperforms DAI on recall by 4×. |
| Piktochart API | ⚠ | No public MCP yet; REST API available. Canva MCP covers branded social use cases without API friction. |
| Submagic API | ⚠ | Available on Business+ plan ($41/mo). Recipient provides API key. |
| Castmagic MCP | ⚠ | Available; requires Castmagic account + API token. |
| Spotify for Podcasters Analytics | ⚠ | No public API; manual export only. Chartable / Podtrac provide partial cross-platform via API. |
| Apple Podcasts Connect Analytics | ⚠ | No public API; manual export only. |
| TikTok organic Research API | ⚠ | Mirrors marketing-agent / video-creator note: requires TikTok Developer Portal app approval; Apify / `brightdata-mcp` fallback works immediately. |

**Verdict (June 2026): ~96% fulfillment.** Every documented use case has a concrete execution path. The 4% residual lives in GUI-bound editing (Descript / Riverside timeline ops; mitigated by brief-grade output + ElevenLabs+ffmpeg for segment-level rebuilds), missing public APIs (Headliner; mitigated by RSS autopilot + ffmpeg fallback), per-host DAI standardization (mitigated by host-read scripts at 4× recall), and platform analytics manual-export gates (Spotify / Apple Podcasts) that Chartable / Podtrac partially fill.

---

## When to use this agent

- "Write me a weekly newsletter on [topic] for the next 12 weeks"
- "Plan a podcast season — 8 episodes around [thesis], schedule guests, draft scripts"
- "Repurpose my latest podcast episode into a LinkedIn carousel, X thread, 3 short clips, an audiogram, and a newsletter issue"
- "Design my monetization stack — I have 5K newsletter subs, 800 podcast listeners, and one digital product"
- "Find me 10 guests for my podcast in the [niche] space and draft outreach"
- "Write a Twitter thread about [topic] and cascade to LinkedIn + Threads + Bluesky"
- "Make a LinkedIn carousel from this blog post"
- "Generate an infographic from this research report"
- "Audit my podcast back catalog and recommend top 10 evergreen episodes to re-promote"
- "Pull my Beehiiv subscriber growth + engagement for the last 4 weeks and tell me what's working"

## When NOT to use this agent

- Broad marketing strategy / positioning / paid ads / SEO at org-wide level — hand off to `marketing-agent`
- Deep video craft (color grading, FFmpeg multi-platform export pipelines, AI video generation via Sora 2 / Veo 3.1 / Kling, programmatic Remotion renders, film-grade ElevenLabs voice production) — hand off to `video-creator`
- Deep SEO + AEO / GEO + technical site audit — hand off to `marketing-agent` for now (or future `seo-specialist`)
- Deep technical documentation (READMEs, OpenAPI specs, ADRs, doc-system architecture) — hand off to `technical-writer`
- Deep email lifecycle (multi-region deliverability migration, 50K+ list segmentation, post-MPP attribution architecture) — hand off to `marketing-agent` (or future `email-strategist`)
- Deep social media management at-scale (paid social, audience research at scale) — hand off to `marketing-agent` (or future `social-media-manager`)
- Legal / compliance copy that needs legal review — draft, but flag for legal sign-off
- Engineering work for the user's content infrastructure (custom CMS, custom website, custom Stripe integration) — hand off to `senior-python-engineer` or `frontend-engineer`
