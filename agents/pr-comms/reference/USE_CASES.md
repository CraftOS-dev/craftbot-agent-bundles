# PR & Communications — Use Cases

**Tier:** **general** · **Category:** communications
**Core job:** End-to-end PR + comms operator covering media relations, press releases, crisis comms, executive thought leadership, awards, podcast tours, brand reputation, AEO citation tracking, and analyst relations.

This file is part of the bundle but is **not** loaded into the agent's context. It exists so users and future contributors can see what this agent is for, what it executes vs. directs, and when to use it.

Ships with the SOTA earned-media stack (Muck Rack / Cision / Brand24 / Brandwatch / AthenaHQ / Profound / PodPitch / LinkedIn Marketing API / wire APIs / `playwright-mcp` form automation) — executes end-to-end, not just direct. Free-tier fallbacks wired (Featured.com / Qwoted free tier / `brave-search` / `reddit-mcp` / `twitter-mcp`) so the agent is functional Day 1 even before paid keys are configured.

---

## What this agent is supposed to do

### Media database + journalist research
- Build and maintain a media list (journalists matching beat + outlet + recent coverage)
- Find a journalist's beat + recent coverage + best pitch angle
- Detect when a journalist on the list changes outlets or beats
- Maintain a journalist relationship CRM (last conversation, last pitch, last placement, prefs)

### Press release writing + distribution
- Write a press release in AP/PRSA-compliant format
- Distribute via wire service (PR Newswire / Business Wire / GlobeNewswire)
- Self-distribute embargoed release to a targeted media list
- Manage online newsroom (branded press center)
- Track placements + tier + EMV post-release

### Journalist outreach (cold + warm + embargoed)
- Send personalized cold pitch to a journalist (subject <49 chars, pitch <150 words, cite specific recent article)
- Run an embargoed launch with NDA tracking + break monitoring
- Warm-pitch a journalist with whom there's prior relationship history
- Respond rapidly to a reporter query (HARO / Featured / Qwoted / Source of Sources / #JournoRequest)
- Track pitch + response + conversion analytics

### Media training + spokesperson prep
- Prep a spokesperson for an interview (background brief + Q&A doc + bridge phrases)
- Generate `mcp-tts` audio rehearsal drill
- Document on-record / off-record / on-background rules for every interaction
- Brief on outlet voice + recent angle + likely journalist questions

### Crisis communications
- Run the 24/48/72-hour crisis comms playbook (holding statement → per-stakeholder variants → full statement + Q&A → iteration → post-mortem)
- Detect a brewing crisis before it explodes (predictive crisis comms via Brand24/Brandwatch sentiment velocity)
- Deepfake / misinformation detection on suspicious media (Truepic / Reality Defender / Sensity)
- Execute multi-stakeholder fanout (customers / employees / press / regulators / investors / public)
- Defer exec-voice on high-stakes statements to `ceo-agent`; customer-facing outage comms to `customer-support-agent`; SEC 8-K / Reg-FD to `investor-relations`

### Executive thought leadership
- Draft + publish an executive LinkedIn newsletter (LinkedIn Marketing API)
- Cross-post to Substack / Beehiiv for owned email + monetization
- Draft + place contributed op-eds (Forbes Contributor / Fast Co / Inc / HBR — outlet-specific norms)
- Real-time topical commentary on X for thought leadership (with spokesperson approval)
- Repurpose newsletter → LinkedIn posts → X thread → podcast pitch hook

### Awards + lists submissions
- Submit to Inc 5000 / Forbes 30 Under 30 / Fast Company Most Innovative
- Track award deadlines + categories + judging criteria
- `playwright-mcp` automates web form submission from Notion criteria DB
- Quarterly scan for new awards + category additions (`firecrawl-mcp`)
- Eligibility verification BEFORE drafting

### Podcast tour booking
- Find relevant podcasts for an executive guest spot (PodPitch + Podchaser + MatchMaker)
- Personalize + send pitch to podcast host (cite specific recent episode)
- Prep executive for the podcast appearance (Q&A doc + `mcp-tts` drill)
- Track speaking calendar + post-event repurposing

### Brand reputation monitoring
- Track brand mentions across news / blogs / social / podcasts / forums (paid: Brand24 / Brandwatch / Meltwater)
- Free-tier brand mention monitoring fallback (`brave-search` + `reddit-mcp` + `twitter-mcp` + Google Alerts)
- Respond to online reviews (Trustpilot / G2 / Glassdoor)
- Sentiment classification + velocity tracking + alert thresholds

### AI search citation tracking (AEO / GEO)
- Track brand citation share in ChatGPT / Gemini / Claude / Perplexity / Brave (AthenaHQ + Profound)
- Optimize PR + earned media for AI search citation (extractable quote engineering)
- Track 50-500 brand-relevant prompts daily

### Conference speaking submissions
- Submit a talk proposal to a conference CFP (Sessionize / Papercall / Pretalx)
- Track speaking calendar + travel + recordings
- Post-talk: `youtube-mcp-transcript` for repurposing into LinkedIn / Substack / X thread

### PR campaign measurement
- Calculate share of voice across competitors (paid stack or free `brave-search` count)
- Sentiment analysis across earned coverage
- Calculate tier-1 placement count + earned media value (EMV) per outlet-tier rubric
- Monthly + quarterly PR report (`docx` skill render)

### Analyst relations
- Build a Gartner / Forrester / IDC briefing program (FREE per Gartner methodology)
- Draft analyst briefing deck (`pptx`)
- Submit to a Gartner Magic Quadrant or Forrester Wave (vendor portal + survey + customer references)
- Track analyst report mentions + sentiment of your product
- Boutique firms (Constellation, GigaOm, 451 Research, ABI Research, Omdia)

### Reddit / HN / community engagement
- Schedule + run a Reddit AMA (mod outreach + spokesperson verification + 2-3hr live + 24hr followup)
- Launch on Show HN / Ask HN (`playwright-mcp` submit + comment monitoring + founder response within 30 min)
- Monitor industry subreddits + dark social (Discord communities)

### Customer reference program (for PR)
- Build + maintain a case study / customer reference library (Notion DB)
- Match a journalist's beat to a relevant customer reference (tag filter)
- Pull customer quotes for press releases (with permission)

---

## Execution status (SOTA — June 2026)

The agent's earned-media surface is fully executable with `cli-anything` + `gmail-mcp` + `notion-mcp` + the listed MCPs + bundled skill packs. Free-tier fallbacks (Featured.com / `brave-search` / `reddit-mcp` / `twitter-mcp` / `playwright-mcp`) make the agent Day-1 functional even before paid keys are configured. Paid integrations close the remaining gaps as the recipient adds keys (Muck Rack / Brand24 / Brandwatch / PR Newswire / Business Wire / AthenaHQ / Profound / PodPitch / Trustpilot / G2 / deepfake detection APIs).

### What this agent EXECUTES today (SOTA mechanisms per use case)

| Use case | SOTA mechanism | Path |
|---|---|---|
| Build/maintain media list | Muck Rack API + Media List Agent | `cli-anything` curl + `notion-mcp` |
| Find journalist beat + coverage | Muck Rack + Roxhill + `firecrawl-mcp` cross-check | `cli-anything` + `firecrawl-mcp` |
| Detect journalist outlet change | Muck Rack webhook subscription | `cli-anything` + `notion-mcp` |
| Maintain journalist CRM | Notion DB (last interaction, prefs, history) | `notion-mcp` |
| Write press release (AP/PRSA) | Claude generation + Vale linter pass + Prowly AI fallback | `cli-anything` (Vale) + `docx` skill |
| Distribute via wire (PRN/BW/GNW) | Wire APIs | `cli-anything` curl + paid wire account |
| Self-distribute embargoed | Per-journalist `gmail-mcp` (NEVER BCC) + Muck Rack | `gmail-mcp` + `cli-anything` |
| Manage online newsroom | Prezly / Prowly API | `cli-anything` curl |
| Track placements + EMV | `notion-mcp` placement log + outlet-tier rubric | `notion-mcp` + `brave-search` |
| Cold pitch journalist | Claude personalization from journalist's last 5 articles | `gmail-mcp` + (optional) Smartlead/Lemlist warmup |
| Embargoed launch + NDA | Per-journalist `gmail-mcp` + DocuSign API + embargo break monitoring | `gmail-mcp` + `cli-anything` + Brand24/`brave-search` cron |
| Warm pitch | Notion CRM relationship log + Muck Rack recent articles | `notion-mcp` + Muck Rack + `gmail-mcp` |
| HARO / Featured / Qwoted / SoS / #JournoRequest | Featured.com (free) + Qwoted + #JournoRequest stream | `gmail-mcp` filter + `twitter-mcp` |
| Pitch + response + conversion analytics | Notion DB + Claude classifies outcome | `notion-mcp` |
| Spokesperson interview prep | Outlet research + likely-Q gen + `mcp-tts` drill | `firecrawl-mcp` + `docx` + `mcp-tts` |
| On/off/background interaction log | Notion DB row per interaction | `notion-mcp` |
| 24/48/72-hr crisis playbook | Pre-drafted templates + per-stakeholder variants + multi-channel | `gmail-mcp` + `slack-mcp` + `twitter-mcp` + `notion-mcp` |
| Predictive crisis detection | Brand24/Brandwatch sentiment velocity → Slack alert | API + `slack-mcp` |
| Deepfake detection | Truepic / Reality Defender / Sensity API | `cli-anything` curl |
| Multi-stakeholder crisis fanout | `gmail-mcp` (press, customers, regulators) + `slack-mcp` (internal) + `twitter-mcp` (public) | Multiple MCPs |
| Executive LinkedIn newsletter | LinkedIn Marketing API `/rest/articles` | `cli-anything` curl |
| Substack / Beehiiv cross-post | Substack API + Beehiiv API | `cli-anything` curl |
| Op-ed pitch + draft | Outlet-specific norms + `docx` render | `gmail-mcp` + `docx` |
| Real-time X commentary | `twitter-mcp` lists + Claude POV thread | `twitter-mcp` |
| Newsletter repurposing | Claude rewrites for LinkedIn/X/podcast hooks | (in skill pack) |
| Submit Inc 5000 / Forbes / Fast Co | `playwright-mcp` form fill from Notion criteria DB | `playwright-mcp` + `notion-mcp` |
| Track award deadlines + criteria | `firecrawl-mcp` quarterly scan + Notion DB | `firecrawl-mcp` + `notion-mcp` |
| Find podcasts for guest spot | PodPitch / Podchaser / MatchMaker | `cli-anything` curl + paid PodPitch |
| Pitch podcast host | `youtube-mcp-transcript` last 3 episodes + Claude pitch | `youtube-mcp-transcript` + `gmail-mcp` |
| Prep exec for podcast | `youtube-mcp-transcript` research + `mcp-tts` drill | `youtube-mcp-transcript` + `docx` + `mcp-tts` |
| Brand mention monitoring (paid) | Brand24 / Brandwatch / Meltwater API | API + `notion-mcp` |
| Brand mention monitoring (free fallback) | `brave-search` + `reddit-mcp` + `twitter-mcp` cron + Google Alerts | MCPs in catalog |
| Respond to online reviews | Trustpilot / G2 API + Claude draft + human approval | `cli-anything` curl |
| AI search citation tracking | AthenaHQ + Profound API | `cli-anything` curl |
| Optimize earned media for AI citation | Outlet-tier rubric + extractable quote engineering | `notion-mcp` tracking |
| Track 50-500 brand-relevant prompts | Profound daily polling | `cli-anything` cron |
| Submit CFP (Sessionize/PaperCall/Pretalx) | `firecrawl-mcp` CFP discovery + `playwright-mcp` submit | `playwright-mcp` + `firecrawl-mcp` |
| Track speaking calendar | `notion-mcp` + `google-calendar-mcp` | MCPs in catalog |
| Post-talk repurposing | `youtube-mcp-transcript` + Claude rewrites | `youtube-mcp-transcript` |
| Share of voice calculation | Brand24 API or `brave-search` count fallback | Both supported |
| Sentiment analysis on coverage | Brand24 auto OR Claude per-article | API or `firecrawl-mcp` + Claude |
| Tier-1 placement count + EMV | Outlet-tier rubric + Notion auto-tag | `notion-mcp` |
| Analyst briefing (Gartner/Forrester/IDC) | FREE vendor portal briefing + `pptx` deck | `pptx` + `gmail-mcp` + `google-calendar-mcp` |
| Magic Quadrant / Wave submission | Vendor portal + 100+ question survey + customer references | `notion-mcp` + manual submit |
| Analyst report mention tracking | `firecrawl-mcp` quarterly diff | `firecrawl-mcp` + Claude |
| Reddit AMA scheduling + execution | `reddit-mcp` mod outreach + AMA posting | `reddit-mcp` + `notion-mcp` |
| Show HN launch | `playwright-mcp` HN submission + comment monitoring | `playwright-mcp` + `firecrawl-mcp` |
| Industry subreddit monitoring | `reddit-mcp` daily pull + Claude classify | `reddit-mcp` |
| Dark social tracking | `discord-mcp-full` permitted servers | `discord-mcp-full` |
| Customer reference library | `notion-mcp` DB + CRM sync via `cli-anything` | `notion-mcp` |
| Journalist → customer reference match | `notion-mcp` tag filter | `notion-mcp` |

### Remaining caveats (honest)

| Capability | Status | Notes |
|---|---|---|
| Muck Rack / Cision / Roxhill paid databases | ⚠ | Paid subscription required (Muck Rack ~$5K+/year, Cision enterprise, Roxhill UK/EU). Free fallback: `brave-search` + Featured.com daily digest covers SMB Day 1. |
| Wire service distribution (PR Newswire / Business Wire / GlobeNewswire) | ⚠ | Per-release fees $350-$3K + subscription. Self-distribute via `gmail-mcp` is the no-cost fallback for non-Reg-FD news. |
| Brand24 / Brandwatch / Meltwater monitoring | ⚠ | Paid (Brand24 $249/mo entry, Brandwatch $800-3K, Meltwater ~$25K/yr). Free fallback wired via `brave-search` + `reddit-mcp` + `twitter-mcp` + Google Alerts. |
| AthenaHQ + Profound (AEO/GEO tracking) | ⚠ | Paid; both required for full ChatGPT/Gemini/Claude/Perplexity citation tracking. Brand24 Chatbeat is included if Brand24 already purchased. |
| PodPitch / Podchaser Pro / MatchMaker | ⚠ | Paid (PodPitch $199-299/mo). Free fallback: `firecrawl-mcp` Apple Podcasts + Spotify + RSS direct, slower discovery. |
| LinkedIn Marketing API (newsletters + ads) | ⚠ | Requires LinkedIn Community Management product approval (5-15 day review). |
| Trustpilot / G2 review responses | ⚠ | Paid Trustpilot business / G2 vendor account required for API access. Glassdoor responses = portal-only. |
| Deepfake detection (Truepic / Reality Defender / Sensity) | ⚠ | Paid API keys for production crisis monitoring. C2PA Content Credentials check is free for media that has provenance metadata. |
| Smartlead / Lemlist cold outreach infra | ⚠ | Paid; only needed when volume requires warmup infrastructure. 1:1 `gmail-mcp` works for low-volume tier-1 outreach. |
| Substack writer access | ⚠ | One-time writer account setup; API access depends on tier. |

**Verdict (June 2026): ~95% fulfillment.** Every documented use case has a concrete execution path. The 10 ⚠ rows split into (a) paid SaaS the recipient owns (media databases, wire services, monitoring, AEO tools, podcast platforms, review platforms, deepfake detection) and (b) platform OAuth approval cycles (LinkedIn Marketing API, Substack writer access). Every paid integration has a free fallback wired so the agent is functional Day 1.

---

## When to use this agent

- "Write a press release for our Series B announcement and distribute via Business Wire"
- "Build a media list of B2B SaaS journalists covering AI agents and find 5 we should pitch first"
- "Draft a cold pitch to [journalist] citing their March 12 article on email deliverability"
- "Run the 24-hour crisis comms playbook — we had a data exposure incident affecting 1,200 customers"
- "Find 10 podcasts for our CEO to guest on and draft personalized pitches citing specific recent episodes"
- "Submit us to Inc 5000 and Fast Company Most Innovative — pull facts from our 2025 financials"
- "Draft a LinkedIn newsletter for our CEO on the post-MPP email measurement shift"
- "Track our brand citation share in ChatGPT and Claude responses for the 50 prompts our customers ask"
- "Prep [exec] for tomorrow's Fortune interview — generate likely questions and `mcp-tts` audio drill"
- "Launch us on Show HN this Tuesday morning and monitor the thread for the first 4 hours"
- "Set up a Gartner Magic Quadrant briefing program and draft our first analyst briefing deck"
- "Respond to today's HARO / Featured / Qwoted queries that match our space"

## When NOT to use this agent

- Paid ad amplification of earned coverage — hand off to `marketing-agent`
- CEO's personal voice on a high-stakes statement (layoff announcement, founder departure, board crisis) — hand off to `ceo-agent`
- Customer-facing comms during an active outage / breach / billing incident — hand off to `customer-support-agent`
- SEC 8-K filing / Reg-FD compliant disclosure / earnings prep / analyst call positioning — hand off to `investor-relations`
- Day-to-day organic social scheduling and engagement (not earned-media commentary) — hand off to `social-media-manager`
- Long-form blog or video content production (not op-eds or thought leadership) — hand off to `content-creator`
- Deep SEO content strategy + cannibalization audits — hand off to `seo-specialist`
- Deep email lifecycle design (welcome / nurture / win-back) — hand off to `email-strategist`
- Deep research / market sizing — hand off to `research-analyst`
- Engineering work for the company's site or comms infrastructure — hand off to `senior-python-engineer` / `frontend-engineer`
- Writing technical product documentation — hand off to `technical-writer`
- Legal / compliance copy that needs legal review — agent drafts; flag for legal sign-off
- Brand strategy at the agency-engagement level (rebrand / naming / positioning over months) — agent can start; recommend a brand strategist specialist (v1)
