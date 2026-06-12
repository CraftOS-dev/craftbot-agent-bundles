# Content Creator — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Newsletter publishing playbook", "Podcast production playbook", "Repurposing pipeline playbook", "Content series planning playbook", "LinkedIn carousel playbook", "X thread playbook", "Audiogram playbook", "Infographic playbook", "Podcast SEO playbook", "Monetization stack playbook", "Content analytics playbook", "Editorial calendar template", "Tentpole-to-derivative chain", "AI-slop catch list", "Sponsor read script template", "Show notes template", "Newsletter issue template", "LinkedIn carousel template", "Thread template", "Episode trailer template", "SOTA tool reference".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Content formats this agent handles

- Long-form newsletter issues (Beehiiv / Substack / Ghost / Kit / hybrid)
- Podcast episode scripts (interview / monologue / panel / narrative)
- Podcast show notes (pre-recorded + post-recorded variants)
- Podcast trailers (60-90s 3-act: hook → tease → CTA)
- Podcast guest preparation packets (Podchaser-sourced)
- Podcast season/series arc plans
- Podcast back-catalog audit + re-promotion plans
- Multi-format content series arcs (4-12 episode/issue themed runs)
- Repurposing pipelines (1 → 10+ derived assets)
- Short-form video scripts (Reels / TikTok / Shorts / YouTube Shorts)
- LinkedIn carousels (8-14 slides)
- X / Twitter / Threads / Bluesky / Mastodon threads
- Long-form blog posts (when blog is the tentpole, not newsletter)
- Audiograms (Headliner RSS autopilot + ffmpeg fallback)
- Infographics (data-heavy via Piktochart; branded social via Canva)
- Quote graphics + pull-quote social cards
- Newsletter audience surveys
- Editorial briefs (per-piece content briefs)
- Monetization stack decks
- Sponsorship pitch decks
- Creator collab / brand partnership briefs

### Platforms covered

- **Newsletter:** Beehiiv (default for media-product), Substack (default for low-friction), Ghost (default for independent publisher CMS), Kit / ConvertKit (default for course creator + advanced automation)
- **Podcast hosting:** Buzzsprout, Transistor, Captivate, Spotify for Podcasters (Anchor), Apple Podcasts Connect, RSS.com, Podbean, Megaphone, Acast
- **Podcast recording:** Riverside (HD multi-track), Descript (AI-edit + Studio Sound), SquadCast, Zencastr
- **Podcast intelligence:** Podchaser, Listen Notes, Chartable, Podtrac, Podscan.fm
- **Repurposing:** Castmagic (audio→text derivatives), OpusClip / Opus Pro / Munch (long→short video), Submagic (AI captions + B-roll), Headliner / Wavve (audiograms), Repurpose.io (cross-platform distribution)
- **LinkedIn carousel:** Postiv, Carosello, Taplio, Imejis.io, AuthoredUp
- **Thread authoring:** Typefully (best-in-class with agent CLI), TweetHunter, Hypefury
- **Cross-platform publishing:** Buffer (GraphQL + MCP), Hootsuite, Sprout Social
- **Design:** Canva, Adobe Express, Piktochart, Visme, Figma
- **Monetization:** Patreon, Substack, Beehiiv Boosts, Memberstack, Circle, Kajabi, Podia, Buy Me a Coffee, Gumroad, Stan Store, Beacons, Linktree, Bonsai
- **Transcripts:** Otter.ai, Whisper, Granola, Fathom
- **Analytics:** Beehiiv Analytics, Substack Stats, Apple Podcasts Connect Analytics, Spotify for Podcasters Analytics, Chartable, Podtrac, Plausible, GA4, PostHog

### Content categories (40/30/20/10 mix for short-form)

- **40% educational** — teach the audience something specific
- **30% entertainment** — make them feel something
- **20% inspirational** — make them want to be / do something
- **10% promotional** — explicit business ask

Flipping this ratio (e.g., 60% promotional) burns the audience and tanks algorithm performance.

---

## Newsletter publishing playbook

### Platform decision tree

- **Beehiiv** — default for media-product newsletter. Native MCP (March 24, 2026 launch). Built-in referral program, recommendation network, Boosts (paid acquisition), ad network monetization. 0% revenue share on paid tiers.
- **Ghost** — default for independent publisher CMS. Full Content API + Admin API for programmatic publishing. Better long-term member home; richer publication branding.
- **Substack** — default for low-friction start. No public API. 10% platform fee on paid subs but built-in network for discovery.
- **Kit (ConvertKit)** — default for course creator + complex automation. Advanced segmentation, tag-based flows, commerce features (digital products, checkout pages). Pricier than Beehiiv (~$135/mo at 10k subs vs Beehiiv $42).

### Cadence decisions

- **Weekly** — minimum sustainable cadence for compounding momentum
- **Biweekly** — acceptable if user can't sustain weekly; better than missed weekly
- **Monthly** — when content depth justifies long lead time (deep research, original data, 2,500+ words)
- **Daily** — only for high-frequency curation newsletters or trade-specific (e.g., AI news round-ups)

**SOTA send-time:** Tuesday 6am ET (creator-economy benchmark; aligns with knowledge-worker morning routine across US time zones).

### Newsletter issue template

```markdown
# Subject Line: [Hook — 30-50 chars; A/B test 2 variants]
# Preheader: [Continues the subject promise — 50-100 chars]

## Headline
[Lead with the outcome, not the topic]

## Hook (1-2 paragraphs)
[The pattern-interrupt; the surprising fact; the reframe]

## Body (3-5 sections)
- Section 1: [The thesis or surprising claim]
- Section 2: [The proof — data, story, example]
- Section 3: [The implication — what this means for the reader]
- Section 4 (optional): [The objection / nuance]
- Section 5 (optional): [The synthesis]

## Takeaway
[Single sentence the reader carries away]

## CTA
- Primary CTA: [What action — read more / book call / subscribe / reply]
- Secondary CTA: [Fallback]

## Sponsor read (if applicable)
[Host-voice in brand voice — 50-80 words]
```

### Newsletter brand voice rules

- Active voice, present tense, second person
- One idea per paragraph
- Strip "leverage," "utilize," "in today's fast-paced world," "navigating the landscape," "I've been thinking about" openers
- Length matches intent — short on Tuesday, long on Saturday (if biweekly)
- Embed one original data point or hot take per issue (no commodity content)
- UTM tag every CTA link (utm_source=newsletter / utm_medium=email / utm_campaign=ISSUE-NUMBER / utm_content=CTA-NAME)

### Newsletter quality gates

- [ ] Vale brand-voice slop scrub passes
- [ ] One original data point or hot take present
- [ ] CTA links UTM-tagged
- [ ] Mobile-render checked (Litmus / Email on Acid / `playwright-mcp`)
- [ ] Preheader text written and rendering correctly
- [ ] Subject line < 50 chars
- [ ] Preheader 50-100 chars
- [ ] Plain-text alternative auto-generated by ESP
- [ ] One-click unsubscribe present (RFC 8058)
- [ ] Sender domain SPF + DKIM + DMARC verified

### Newsletter analytics priorities

- **CTR (clicks / sends)** — primary engagement signal post-MPP
- **CTOR (clicks / opens)** — engagement among engaged
- **Subscriber growth** — net new (gross + churn)
- **Revenue per recipient** — economic value
- **Reply rate** — top-of-funnel signal for upcoming launches
- **Open rate** — directional only, never quoted as success

---

## Podcast production playbook

### Pre-production (script + show notes BEFORE recording)

1. **Concept brief** — episode thesis (one sentence), audience question being answered, format (interview / monologue / panel / narrative), target length, hook, CTA
2. **Guest research** — Podchaser API (32M+ structured credits by host/co-host/producer/guest role) → assemble guest packet (past episodes, recurring themes, audience size, fresh angle) → custom question set
3. **Outreach** — `gmail-mcp` send templated outreach referencing specific past work; pipeline tracking in Notion DB
4. **Pre-write show notes outline** — episode summary + key takeaways skeleton + planned resources + chapter markers; this becomes the structural guide during recording and the SEO + repurposing source-of-truth post

### Production (recording brief for Riverside / SquadCast / Zencastr)

- **Riverside default** — HD multi-track recording, Magic Audio noise removal, Magic Clips auto-clip generation, AI Show Notes auto-summary, Smooth Speech disfluency removal
- **Track separation** — each speaker on isolated track for post-editing flexibility
- **Audio targets at source** — voice at -12 to -6 dB, no clipping, no room echo
- **Backup recording** — local backup on each guest's device (Riverside captures this natively)
- **Pre-record checklist** — mic check, headphone check, lighting (if video), Wi-Fi stability, lavalier/USB mic priority over built-in

### Post-production (Descript editing brief)

```markdown
# Editing Brief: [Episode Title]

## Source files
- Main track: [Riverside export URL]
- Guest tracks: [list]
- Resource files: [transcripts / pre-write notes]

## Cuts (timestamped to source)
- 00:00:00 - 00:01:30 — intro music + host greeting (KEEP)
- 00:01:30 - 00:02:15 — false start, off-topic chat (CUT)
- 00:02:15 - 00:05:30 — pre-roll sponsor read (KEEP — host voice)
- ...

## Level targets
- Voice: -8 dB peak, -16 dB average
- BGM intro: -18 dB
- Sponsor read BGM (if any): -22 dB
- Final loudness: -16 LUFS (podcast platform standard), peak ≤ -1 dBFS

## Transitions
- Hard cuts default; one dissolve at the topic turn (00:23:15)
- BGM fade-out 2s at end of intro
- BGM fade-in 1s at sponsor break

## Chapters (for RSS + Google Key Moments + listener navigation)
- 00:00 — Cold open hook
- 02:30 — Sponsor read
- 05:00 — Topic 1: [name]
- 18:00 — Guest backstory
- 32:00 — Hot take / key insight
- 48:00 — Q&A / wrap
- 55:00 — CTA + outro

## Output
- MP3 192kbps stereo for podcast distribution
- MP4 1080p for YouTube version
- WAV master for archive
```

### Show notes template (publish post-edit)

```markdown
# [Episode Number]: [Episode Title with Front-Loaded Keyword]

## Episode Summary (150-200 words)
[The hook, the guest, the thesis, the key insight, the CTA — all in one paragraph]

## Key Takeaways
- Takeaway 1: [single insight, named in the episode]
- Takeaway 2: [single insight, named]
- Takeaway 3: [single insight, named]
- Takeaway 4 (optional): [...]
- Takeaway 5 (optional): [...]

## Resources Mentioned
- [Tool / article / book mentioned + URL]
- [Tool / article / book mentioned + URL]

## Timestamps
- 00:00 — Cold open
- 02:30 — Sponsor read: [sponsor name]
- 05:00 — [Topic 1 name]
- 18:00 — [Guest backstory or topic 2]
- 32:00 — [Hot take / key insight]
- 48:00 — [Q&A or wrap]
- 55:00 — CTA + outro

## Guest Bio
[Name, current role, past relevant work, social links, book/podcast/newsletter to plug]

## Sponsor
[Name, host-read line, CTA URL with UTM]

## Subscribe + Share
- Apple Podcasts: [URL]
- Spotify: [URL]
- YouTube: [URL]
- RSS: [URL]
- Newsletter (for deeper takes): [URL]
- Leave a review: [Apple Podcasts review URL]
```

### Podcast SEO playbook

- **Title format:** `[Episode #]: [Front-Loaded Keyword] | [Guest Name or Hot Take]`
- **Description:** 150-200 words; include 2-3 long-tail keywords naturally; link to show notes URL; link to sponsor URL with UTM
- **Chapters:** Embed via `<podcast:chapter>` RSS namespace; Google Key Moments displays these in Search results as rich result cards
- **Transcripts:** Publish full transcripts on episode page (boosts indexable content; rankable on long-tail queries; accessibility win)
- **Thumbnail:** YouTube version requires high-contrast thumbnail; person-fills-60%+ vertical OR text-image-split horizontal; 3-8 character text overlay
- **RSS metadata:** `<itunes:keywords>`, `<itunes:category>`, `<itunes:summary>`, `<itunes:image>` all populated; subtitle + description distinct

### Podcast analytics priorities

- **Listen-through rate (LTR)** — primary signal; 50% at 25-min mark = professional; below 30% = restructure
- **Avg listens per episode** — growth signal over time
- **Chartable / Podtrac cross-platform** — true reach (Spotify + Apple + others combined)
- **Subscriber growth** — Apple Podcasts new follows / Spotify new follows
- **Geographic distribution** — where the audience actually is (often surprises)
- **Episode completion rate** — proxy for content-market fit
- **Web traffic to episode page** — show notes SEO indicator

---

## Repurposing pipeline playbook

### Tentpole-to-derivative chain

The fundamental rule: every long-form piece spawns ≥10 derivatives. Never ship a one-off.

```
TENTPOLE (1) → DERIVATIVES (10+)
├── Podcast episode (45-60 min)
│   ├── Audiogram (60s) — Headliner RSS autopilot or ffmpeg + waveform
│   ├── Short clip (60-90s) — OpusClip / Opus Pro AI-selected viral moment
│   ├── Short clip (60-90s) — second viral moment
│   ├── LinkedIn carousel (10 slides) — key insights from transcript via Castmagic + Postiv/Carosello
│   ├── X thread (12 tweets) — top takeaway thread via Castmagic + Typefully
│   ├── Newsletter issue (1) — episode write-up via Castmagic + author + Vale scrub
│   ├── Blog post (1) — long-form version via Castmagic transcript + author
│   ├── Quote graphic (3-5) — Canva MCP from pull-quotes
│   ├── YouTube full video (1) — if recorded video; auto-upload via `youtube-mcp`
│   └── YouTube Shorts (3-5) — vertical export of OpusClip moments
│
├── Long-form newsletter issue (2,000-3,000 words)
│   ├── LinkedIn carousel (10 slides) — restructured to swipeable insights
│   ├── X thread (10 tweets) — distilled to thesis tweets
│   ├── LinkedIn long-form post (1) — re-cut for LinkedIn audience
│   ├── Audio version (1) — ElevenLabs voice-read + RSS-private feed
│   ├── Blog post (1) — same content with SEO header structure
│   ├── Quote graphics (3-5) — Canva from pull-quotes
│   ├── Instagram carousel (10 slides) — visual-first restructure
│   ├── Reddit cross-post (1-2 communities) — adapted to community norms
│   ├── Email-newsletter cross-promotion partners (paid Boosts or organic swap)
│   └── Podcast monologue episode (1) — if cadence allows
│
└── YouTube long-form video (10-20 min)
    ├── YouTube Shorts (3-5) — vertical clips of best moments
    ├── TikTok / Reels (3-5) — same clips on different platforms
    ├── LinkedIn video (1) — top moment, 60-90s landscape
    ├── X thread (10 tweets) — script-derived
    ├── Newsletter issue (1) — video write-up + embed
    ├── Blog post with embed (1) — SEO + searchable transcript
    ├── Audiogram (1) — audio-only excerpt for podcast feed
    ├── Quote graphics (3-5) — Canva from script
    └── Email teaser to newsletter list (1) — drive views
```

### Repurposing pipeline tool chain

- **Audio/video → text derivatives:** Castmagic MCP (Claude-native) — transforms transcripts into newsletter issue + X thread + blog + show notes + social posts without LLM hallucination
- **Long video → short-form clips:** OpusClip / Opus Pro — AI-identifies viral moments + auto-caption + B-roll + 9:16 export
- **Short-form caption + B-roll:** Submagic (Business+ API) — 99% caption accuracy in 48 languages; auto-edit dead air, B-roll search, 1-click polish
- **Text → LinkedIn carousel:** Postiv (writes + designs) or Carosello (BYOK Gemini at ~$0.10/carousel)
- **Text → thread cascade:** Typefully agent CLI (`npx typefully`) — schedules across X / LinkedIn / Threads / Bluesky / Mastodon
- **Podcast → audiogram:** Headliner Pro RSS autopilot (auto-generates per new episode, auto-uploads to YouTube) OR ffmpeg waveform overlay fallback
- **Cross-platform scheduling:** Buffer GraphQL + MCP — one auth, cascade to 10+ platforms with per-platform text variants
- **Quote graphics:** Canva MCP — branded template instantiation
- **Newsletter → blog SEO:** Same content; restructure headers; add schema markup; add UTM-tagged internal links

### Repurposing schedule example (per tentpole)

| Day | Asset | Platform | Owner |
|---|---|---|---|
| Mon AM | Tentpole (newsletter / podcast / video) | Native + RSS | Author |
| Mon PM | LinkedIn carousel | LinkedIn | Buffer schedule |
| Tue AM | X thread | X / Threads / Bluesky | Typefully cascade |
| Tue PM | Short clip 1 | TikTok / Reels / Shorts | Buffer schedule |
| Wed AM | Audiogram | Instagram / LinkedIn | Headliner RSS |
| Wed PM | Quote graphic 1 | Instagram / X / LinkedIn | Buffer schedule |
| Thu AM | Short clip 2 | TikTok / Reels / Shorts | Buffer schedule |
| Thu PM | Blog post (if newsletter or podcast) | Owned blog | Manual publish |
| Fri AM | LinkedIn long-form (if video) | LinkedIn | Buffer schedule |
| Fri PM | Reddit cross-post | r/relevant | Manual |
| Sun AM | Quote graphic 2 + Newsletter teaser | Instagram + email | Buffer + ESP |

---

## Content series planning playbook

### Series arc design

A series is 4-12 tentpoles around a single thesis or audience question. Examples:

- "How I built a $1M newsletter" (12-week interview series with 12 newsletter operators)
- "AI for non-engineers" (8-week explainer series on practical AI applications)
- "The Solo Founder's Playbook" (10-week deep dive on each operational discipline)
- "What I Learned" (open-ended monthly retrospective format)

### Notion editorial DB schema

```
Editorial Calendar DB
├── Parent properties (per tentpole)
│   ├── Title (string)
│   ├── Series (relation → Series DB)
│   ├── Format (select: Newsletter / Podcast / Video / Blog)
│   ├── Tentpole publish date (date)
│   ├── Author (person)
│   ├── Editor (person)
│   ├── Status (select: Drafting / Review / Scheduled / Published / Repurposing)
│   ├── Primary URL (url — once published)
│   ├── KPI target (string)
│   ├── KPI actual (number — post-publish)
│   └── Tags (multi-select)
│
└── Child properties (per derivative, related to parent)
    ├── Title (string)
    ├── Tentpole (relation → Parent)
    ├── Format (select: LinkedIn carousel / X thread / Reel / Short / TikTok / Audiogram / Quote graphic / Blog / Newsletter cross-promo / etc.)
    ├── Channel (select: LinkedIn / X / Threads / Bluesky / Instagram / TikTok / YouTube / Newsletter / Blog / Reddit / Mastodon)
    ├── Schedule date (date)
    ├── Owner (person)
    ├── Status (select: Drafting / Scheduled / Published)
    ├── Asset URL (url — once produced)
    ├── KPI target (string)
    └── KPI actual (number — post-publish)
```

### Series quality gates

- [ ] Series thesis clear and one-sentence statable
- [ ] 4-12 tentpoles planned with publish dates
- [ ] Each tentpole has ≥10 derivatives queued
- [ ] Per-tentpole format/platform/timing chosen for audience mode
- [ ] Notion parent + child rows synced
- [ ] KPIs set per tentpole and per derivative format
- [ ] Cadence sustainable (don't promise weekly if monthly is realistic)

---

## LinkedIn carousel playbook

### Why carousels

- **1.6× higher engagement** vs standard text posts
- **6.6% avg engagement rate** for carousels vs 2.18% image vs 1.11% text-only
- **77% of technical audiences** prefer carousels over any other content type
- LinkedIn's swipe behavior on mobile favors swipeable assets

### Structure (8-14 slides)

1. **Slide 1 — Hook** — curiosity gap, contrarian claim, surprising stat, or specific outcome promise
2. **Slides 2-12 — Body** — one insight per slide; visual hierarchy (headline + supporting); use diagrams/lists/screenshots
3. **Slide N — CTA** — explicit ask: comment, share, save, follow, click bio link

### LinkedIn carousel template

```markdown
# Carousel: [Working Title]

## Slide 1 (Hook)
**Headline:** [Curiosity gap or surprising stat]
**Supporting:** [One-line proof]
**Visual:** [Background style / emoji / icon]

## Slide 2-12 (Body)
- Slide 2 — [Insight 1: headline + 1-2 sentences + visual]
- Slide 3 — [Insight 2: ...]
- Slide 4 — [Insight 3: ...]
- ...

## Slide N (CTA)
**Headline:** [Explicit ask]
**Body:** [What they get from the action]
**Visual:** [Brand mark + URL or @username]

## Caption (under the carousel post)
- [Hook line — pull from slide 1]
- [Context — 2-3 sentences]
- [CTA — drive to bio link / DM / comment]
- [3-5 hashtags — niche + branded]
```

### Authoring tools

- **Postiv** — writes hooks + slides + CTAs + captions, auto on-brand layouts, end-to-end in <5 minutes from topic or URL
- **Carosello** — BYOK Google Gemini API (~$0.10/carousel); generates written content + custom images; users describe topic or upload document
- **Taplio** — LinkedIn carousel generator with native scheduling integration
- **Canva MCP** — branded template instantiation; reuse brand colors + fonts + slide dimensions

### LinkedIn carousel quality gates

- [ ] 8-14 slides total
- [ ] Slide 1 hook tested (would I swipe?)
- [ ] One insight per body slide
- [ ] Mobile-readable typography (24pt+ at smallest)
- [ ] Branded layout via Canva MCP
- [ ] Slide N CTA clear
- [ ] Caption pulls hook from slide 1
- [ ] 3-5 hashtags (1-2 branded + 2-3 niche)
- [ ] Posted Tuesday-Thursday 8-10am for SOTA timing

---

## X thread playbook

### Rule of 7

A thread needs 7+ scroll-stopper moments across its length. One every 2-3 tweets. Without scroll-stoppers, readers drop after tweet 3.

Scroll-stoppers include: surprising stat, contrarian claim, specific anecdote, screenshot, before/after comparison, question to the reader, emoji-bullet list, "but here's the catch" reframe.

### Thread template

```markdown
# Thread: [Working Title]

1/n THESIS TWEET (≤280 chars)
[Curiosity gap or specific promise + n/total indicator + visual if possible]

2/n CONTEXT (≤280 chars)
[1-2 sentences setting up the proof]

3/n [Body tweet — one specific claim] (≤280 chars)
[Claim + 1-line proof]

4/n [Body tweet — second claim] (≤280 chars)
...

n/n CTA TWEET (≤280 chars)
[Explicit ask: retweet, follow, link to newsletter / podcast / lead magnet]
```

### Cross-platform cascade

Typefully agent CLI (`npx typefully`) cascades the thread to:
- **X / Twitter** (native format)
- **LinkedIn** (collapsed into single long-form post)
- **Threads** (native format)
- **Bluesky** (native format with character-limit re-fit)
- **Mastodon** (native format)

### Thread quality gates

- [ ] 7+ scroll-stoppers across length
- [ ] Thesis tweet pulls scroll
- [ ] Each body tweet has one specific claim
- [ ] CTA tweet closes the loop
- [ ] Numbering present (1/n, 2/n, ...)
- [ ] No tweet exceeds 280 chars (or 500 for X Premium)
- [ ] Typefully cascade configured for cross-publish
- [ ] Posted Mon 8am ET (thread-default) or Tue/Wed 10am ET

---

## Audiogram playbook

### Why audiograms

Audiograms turn audio content into shareable video for visual platforms (Instagram, TikTok, LinkedIn, X). Animated waveform + caption synced to voice. Effective for podcast promotion because they preserve the host's voice while making the audio scrollable.

### Tool choice

- **Headliner Pro** — RSS-monitored autopilot; auto-generates audiogram per new podcast episode; auto-uploads to YouTube; AI clipping for 10+ social-ready clips from full episode; AI captions
- **Wavve** — manual hand-crafted promotional clips; AI moment identification; design templates; brand customization; multi-format export
- **ffmpeg fallback** — fully scriptable via `cli-anything`: waveform filter (`showwaves`) + voice track + branded background + caption overlay

### ffmpeg audiogram recipe

```bash
# Generate animated waveform overlay on branded background with voice + captions
ffmpeg -i podcast_clip.mp3 \
  -i branded_background.png \
  -filter_complex "
    [0:a]showwaves=s=1080x200:colors=white:mode=line:rate=30,format=rgba[wave];
    [1:v]scale=1080:1920[bg];
    [bg][wave]overlay=0:1700[out]
  " \
  -map "[out]" -map 0:a \
  -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 192k \
  -t 60 \
  audiogram_60s.mp4

# Then burn-in captions via Whisper transcript → SRT → ffmpeg subtitles filter
```

### Audiogram quality gates

- [ ] Hook in first 3 seconds (audible or visible)
- [ ] Vertical 9:16 for Reels / TikTok / Shorts; square 1:1 for X / LinkedIn / Facebook
- [ ] Branded colors + logo (subtle, not dominant)
- [ ] Captions burned in (99% accurate via Submagic or manual Whisper review)
- [ ] Voice at -6 dB peak, BGM at -24 dB
- [ ] Total length 30-90s (60s SOTA default)
- [ ] CTA in last 3 seconds (Subscribe / Listen now / Link in bio)

---

## Infographic playbook

### When to choose which tool

- **Piktochart** — data-heavy infographics; AI outline extracts key points from URL or PDF and matches to structured templates
- **Canva MCP** — branded social-style infographics; speed + accessibility; pre-designed templates
- **Adobe Express** — marketing-polished visuals; brand-aligned outputs; less data-structure depth
- **Visme** — interactive infographics; embed-friendly for web; chart-heavy

### Infographic brief template

```markdown
# Infographic: [Working Title]

## Headline (max 10 words)
[The promise the infographic delivers]

## Subheading (1 line)
[What the reader gets from scanning]

## Data points (3-7)
- Stat 1: [number + source]
- Stat 2: [number + source]
- Stat 3: [number + source]

## Sections
- Section 1: [headline + supporting visual idea]
- Section 2: [...]

## Visual style
- Color: [brand palette]
- Type: [headline / body / caption fonts]
- Iconography: [icon set or inline emoji]
- Charts: [bar / pie / line / dot — match to data type]

## Sources (footer)
- Source 1 — URL + date
- Source 2 — URL + date

## Distribution
- LinkedIn carousel slide deck adaptation
- Embedded in blog post
- Pinterest pin (if relevant)
- Shared as PDF lead magnet
```

### Infographic quality gates

- [ ] Headline + subhead readable at thumbnail size
- [ ] 3-7 data points with sources cited
- [ ] Chart type matches data (bar for comparisons, line for time, dot for distribution)
- [ ] Brand palette + fonts consistent
- [ ] Source footer present (E-E-A-T signal)
- [ ] Mobile-vertical version exists (9:16) for Reels / Stories distribution
- [ ] Square version exists (1:1) for Instagram / LinkedIn feed

---

## Monetization stack playbook

### Stack components

- **Subscriptions (free + paid tiers)** — Beehiiv / Substack / Ghost / Kit (all 0% revenue share on paid except Substack's 10%)
- **Memberships** — Patreon (88% creator take; iOS 30% fee post-Nov 2026), Memberstack (96% creator take), Circle (flat-fee community)
- **Sponsorships** — host-read podcast sponsorship (4× recall vs pre-roll); newsletter classified / mid-issue sponsor; YouTube integrated sponsorship
- **Ad networks** — Beehiiv ad network for newsletters; Spotify / Megaphone for podcasts; YouTube ads
- **Products** — Kajabi / Podia for courses; Gumroad / Stan Store for digital products; Beacons / Linktree for link aggregation
- **Tipping / donations** — Buy Me a Coffee; Patreon one-time tier
- **Live / events** — paid webinars, virtual workshops, conferences

### Pricing tier design

- **3 tiers minimum** — cheap (entry), median (sweet spot), premium (anchor)
- **2.5-5× price spread** between tiers — e.g., $5 / $20 / $100; or $10 / $50 / $250
- **Anchoring** — premium tier 5× median makes median look like a steal
- **Margin targets** — paid newsletter: 70%+ contribution margin; membership community: 60%+; products: 80%+

### Churn benchmarks

- **Paid newsletter** — 5% monthly churn = professional; 10%+ = restructure
- **Membership community** — 5-8% monthly churn = expected; 12%+ = restructure
- **Course / product** — one-time; track refund rate (5% = expected)

### Patreon iOS fee flag (November 2026 enforcement)

If 40%+ of subscribers are mobile users (iPhone), Patreon's 30% Apple in-app fee passthrough = 12% margin hit. For creators with significant mobile audience:
- Switch to Memberstack or Circle for higher creator take
- OR push memberships to web checkout only (warn users in onboarding)
- OR raise mobile-tier pricing to absorb the fee

### Monetization stack deck template

```markdown
# Monetization Stack: [Creator Name]

## Audience
- Total reach: [number across platforms]
- Newsletter subs: [number]
- Podcast monthly listens: [number]
- Social followers (by platform): [breakdown]
- Engagement rate: [% benchmark]

## Current revenue (if any)
- Stream 1: [name, monthly, % of total]
- Stream 2: [name, monthly, % of total]
- Total MRR: $[number]

## Proposed stack (3-tier minimum)
### Tier 1 — Free / $0
- What they get: [content access + community + ...]
- Conversion target: [free → paid X%]

### Tier 2 — Paid baseline / $[low price]
- What they get: [premium content + community + ...]
- Tier conversion target: [free → this X%]
- Churn target: [%]

### Tier 3 — Premium / $[high price]
- What they get: [tier 2 + exclusive + cohort access + ...]
- Tier conversion target: [paid → premium Y%]
- Churn target: [%]

## Sponsorship inventory
- Newsletter mid-issue: $[CPM] × [issues/month] = $[revenue]
- Newsletter classified: $[flat] × [count] = $[revenue]
- Podcast host-read: $[CPM] × [downloads/month] = $[revenue]
- YouTube integrated: $[flat] × [videos/month] = $[revenue]

## Projected MRR by Month 6
- Tier 2 subs × price: $[]
- Tier 3 subs × price: $[]
- Sponsorship: $[]
- Product sales: $[]
- Total: $[]

## Platform choice rationale
- Newsletter: [Beehiiv / Substack / Ghost / Kit] because [...]
- Membership: [Patreon / Memberstack / Circle] because [...]
- Product: [Kajabi / Podia / Gumroad / Stan Store] because [...]

## iOS fee flag
- [If mobile sub % > 40, document Patreon 30% Apple fee impact and mitigation]
```

---

## Content analytics playbook

### Per-format primary signals

| Format | Primary signal | What good looks like |
|---|---|---|
| Newsletter | CTR + CTOR + revenue per recipient | CTR > 2%, CTOR > 10%, revenue per recipient > $0.50/issue |
| Podcast | Listen-through rate (LTR) at 25-min | 50% LTR = pro; below 30% = restructure |
| YouTube long-form | Avg view duration + retention curve | 50% retention at 3-min mark = pro |
| YouTube Shorts | Avg view duration + share rate | 75% completion + 2-3% share rate |
| LinkedIn carousel | Engagement rate | 6.6% = carousel benchmark |
| LinkedIn text | Engagement rate | 1.11% = benchmark |
| X thread | Profile clicks + bookmark rate | 3% bookmark rate = high quality |
| TikTok | Completion rate + share rate | 30%+ completion + 2-3% share |
| Reels | Completion rate + share rate | 30%+ completion + 2-3% share |
| Blog post | Time-on-page + scroll-depth + organic ranking | 2+ min ToP, 60%+ scroll, rank in top 10 in 3 months |

### Analytics tool chain

- **Newsletter** — Beehiiv MCP (`get_campaign_metrics`), Substack stats via `firecrawl-mcp` scrape, Ghost native dashboard, Kit native dashboard
- **Podcast** — Spotify for Podcasters Analytics (manual export), Apple Podcasts Connect Analytics (manual export), Chartable / Podtrac cross-platform (curl API), Podscan.fm for podcast intel
- **YouTube** — YouTube Data API v3 via `youtube-mcp` (videos.list, search.list, retention)
- **Social** — `twitter-mcp` + `linkedin` skill + `tiktok-mcp` + native platform analytics
- **Cross-format roll-up** — UTM-tag every URL → roll up via PostHog / GA4 / Plausible
- **Funnel + cohort** — `posthog-mcp` HogQL for retention curves, cohort survival, funnel analysis

### Reporting cadence

- **Weekly** — newsletter CTR + subscriber growth; podcast LTR + downloads; top-performing derivative
- **Monthly** — full content series engagement audit; per-format performance; per-derivative ROI; monetization tier movement
- **Quarterly** — audience survey; competitor benchmark; channel mix review; series arc retrospective

---

## AI-slop catch list

Before any piece publishes, run the editor pass and strip:

**Banned openers**:
- "In today's fast-paced world..."
- "In a world where..."
- "It's no secret that..."
- "Navigating the landscape of..."
- "I've been thinking about..."
- "Look no further than..."

**Corporate jargon**:
- "Leverage" → "use"
- "Utilize" → "use"
- "Synergize" → cut
- "Best-in-class" → cut or specify
- "Game-changing" → cut or specify the change
- "Cutting-edge" → cut or describe specifics

**Sycophancy and hedging**:
- "Great question!" — cut
- "Certainly!" — cut
- "Absolutely!" — cut
- "Maybe could potentially possibly" — pick one or cut
- "I think that maybe perhaps it might..." — cut hedging chain to one or zero hedges

**Stock transitions**:
- "Moreover," "Furthermore," "However" overuse
- "Whether you're X or Y" framing without specificity
- "Not only A but also B" formula

**Style problems**:
- Excessive em-dashes (more than 1 per paragraph)
- Passive voice chains
- Reading-level mismatched with audience
- Sensational opening without substance

**What stays protected**:
- Code blocks
- URLs + technical terminology
- Original author voice
- Sentence structure unless pattern-matched as slop

Use the `humanize-ai-text` skill and `vale-brand-voice` (from marketing-agent siblings) for mechanical enforcement when available.

---

## SOTA tool reference (June 2026)

This section is grep-only — the agent uses keyword-driven retrieval to surface the right skill pack for the user's task. Headings are intentionally search-friendly. Every entry links to a detailed `SKILL.md` in `skills/` that ships in this bundle and loads on demand.

**Full coverage map:** see `reference/SOTA_USE_CASES.md` for the per-use-case mapping and confidence rating.

### Beehiiv MCP (newsletter)

Beehiiv MCP went GA March 24, 2026 — first major newsletter platform operable from Claude / ChatGPT / Gemini / Perplexity. V1 is read-only (subscriber data, post analytics, segments); V2 will add write (publish + send + modify subscriptions). Paid plans only. Use as DEFAULT for media-product newsletters. Read for analytics; switch to Ghost Content API or Kit API for programmatic write until Beehiiv V2 ships.

- **Skill pack:** `skills/long-form-newsletter-substack-beehiiv-ghost/SKILL.md`
- **Endpoint:** `npx @beehiiv/mcp-server`
- **Auth:** Beehiiv API token → `BEEHIIV_API_KEY`
- **Key calls (V1):** `get_publication`, `get_subscriptions`, `get_posts`, `get_post_analytics`, `get_segments`, `get_referral_program_stats`
- **Source:** https://product.beehiiv.com/p/beehiiv-mcp

### Ghost Content + Admin API (newsletter / CMS)

Ghost Admin API for programmatic content publishing (POST /ghost/api/admin/posts/) + Content API for read. Default for independent publisher CMS where the user owns the publication brand. Full schema for posts, tags, authors, members, tiers, subscriptions, paywalled content.

- **Skill pack:** `skills/long-form-newsletter-substack-beehiiv-ghost/SKILL.md`
- **Endpoint:** `https://<site>/ghost/api/admin/`
- **Auth:** Admin API key → `GHOST_ADMIN_KEY`
- **Key calls:** `POST /posts`, `PUT /posts/:id`, `GET /members`, `POST /tiers`, `GET /posts/:id/email`
- **Source:** https://ghost.org/docs/admin-api/

### Kit (ConvertKit) API (newsletter automation)

Kit API for advanced segmentation + tag-based flows + commerce. Default for course creator with complex marketing funnels. Tag-based automation more powerful than Beehiiv's; commerce features (digital products, checkout pages) deeper.

- **Skill pack:** `skills/long-form-newsletter-substack-beehiiv-ghost/SKILL.md`
- **Endpoint:** `https://api.convertkit.com/v3/`
- **Auth:** API key + secret → `KIT_API_KEY` / `KIT_API_SECRET`
- **Key calls:** `POST /subscribers`, `POST /forms/:id/subscribe`, `GET /sequences`, `POST /tags`, `GET /broadcasts`
- **Source:** https://developers.convertkit.com/

### Castmagic MCP (podcast repurposing)

Castmagic Claude-native MCP — entire media library, transcripts, AI-generated content becomes queryable knowledge base. Transforms raw podcast/meeting transcripts into structured show notes, newsletters, X threads without LLM-hallucination risk. Default for audio-tentpole-to-text-derivatives pipeline.

- **Skill pack:** `skills/podcast-scripting-show-notes/SKILL.md` + `skills/repurposing-pipeline-1-to-10/SKILL.md`
- **Endpoint:** Castmagic MCP server
- **Auth:** Castmagic API token → `CASTMAGIC_API_KEY`
- **Key flows:** transcript upload → show notes / newsletter / thread / blog derivatives
- **Source:** https://stormy.ai/blog/best-gpt-repurposing-tools-2026-opusclip-munch-castmagic

### Riverside API (podcast recording)

Riverside Business plan API — full media + transcripts retrieval; no editing operations (cuts / trim / fade) via API yet. Used for: programmatic media fetching, transcript extraction, deletion for storage management. Pair with Descript API for editing-handoff.

- **Skill pack:** `skills/podcast-editing-brief-descript-riverside/SKILL.md`
- **Endpoint:** Riverside REST API
- **Auth:** Business plan + API key (contact Riverside to enable) → `RIVERSIDE_API_KEY`
- **Key calls:** `get_recordings`, `get_transcripts`, `delete_recording`
- **Source:** https://cleanvoice.ai/blog/riverside-api-review/

### Descript API (podcast editing)

Descript API enables media import + edit-in-partner workflow handoff (bearer token, secure backend-to-backend calls). User clicks CTA → lands in Descript with media imported + ready to edit. AI-powered: text-based editing, Overdub voice replacement, Studio Sound, Magic Audio. Transcribes in 23 languages with speaker detection at 95%+ accuracy.

- **Skill pack:** `skills/podcast-editing-brief-descript-riverside/SKILL.md`
- **Endpoint:** Descript REST API
- **Auth:** Bearer token → `DESCRIPT_API_KEY`
- **Key calls:** `import_media`, `generate_edit_url`, `get_transcript`
- **Source:** https://speakwiseapp.com/blog/descript-vs-riverside

### Otter.ai API + Chat (transcription + show notes)

Otter podcast transcription with high-quality automated transcripts + AI Chat for generating show notes, episode summaries, highlight quotes for social media. Alternate to Castmagic for show notes when user is already in Otter ecosystem.

- **Skill pack:** `skills/podcast-scripting-show-notes/SKILL.md`
- **Endpoint:** Otter REST API + AI Chat
- **Auth:** Otter API key → `OTTER_API_KEY`
- **Source:** https://otter.ai/podcast-transcription

### Podchaser API (guest research)

Podchaser API — 6M+ podcasts, 200M+ episodes, 32M+ structured credits (host, co-host, producer, guest). Default for guest discovery + collab research because it answers queries Listen Notes can't: "who's been a guest on these specific shows?", "who's hosted with this person before?". Native transcripts for 150K+ podcasts (5-year backfill).

- **Skill pack:** `skills/podcast-guest-research-outreach/SKILL.md`
- **Endpoint:** `https://api.podchaser.com/graphql`
- **Auth:** GraphQL API key → `PODCHASER_API_KEY`
- **Key calls:** podcast search, episode search, credit role search, person search, transcript search
- **Source:** https://www.podchaser.com/articles/api/podchaser-api-vs-listen-notes-api

### Submagic API (short-form video captions + B-roll)

Submagic Business+ plan API — 99% caption accuracy in 48 languages natively + 100+ languages for AI Video Translator. AI Auto-Edit handles caption placement, dead-air cutting, B-roll search in one click. Use as DEFAULT for short-form video (Reels / TikTok / Shorts) post-production.

- **Skill pack:** `skills/short-form-video-script-reels-shorts-tiktok/SKILL.md` + `skills/repurposing-pipeline-1-to-10/SKILL.md`
- **Endpoint:** Submagic REST API
- **Auth:** Business+ plan + API key → `SUBMAGIC_API_KEY`
- **Source:** https://www.submagic.co/

### OpusClip / Opus Pro (long-form → short-form video)

OpusClip / Opus Pro — AI identifies viral moments from long-form video, auto-captions, auto B-roll, auto-9:16 export. Default for podcast → short clips (3-5 per episode) and YouTube long-form → Shorts pipeline.

- **Skill pack:** `skills/repurposing-pipeline-1-to-10/SKILL.md`
- **Endpoint:** OpusClip API
- **Auth:** API key → `OPUSCLIP_API_KEY`
- **Source:** https://www.blotato.com/blog/ai-content-repurposing-tools

### Headliner Pro (audiograms + RSS autopilot)

Headliner Pro auto-generates audiograms per new podcast episode (RSS-monitored), with AI clipping for 10+ social-ready clips from full-length video + AI captioning + auto-upload to YouTube. No public API but RSS autopilot mode covers most workflow.

- **Skill pack:** `skills/audiogram-headliner-wavve/SKILL.md`
- **Configuration:** Pro plan + RSS feed configured
- **Source:** https://www.headliner.app/

### ffmpeg audiogram fallback

ffmpeg-based audiogram via `cli-anything`: `showwaves` filter for animated waveform + branded background overlay + caption burn-in (Whisper transcript → SRT → subtitles filter). Fully scriptable; no API dependency.

- **Skill pack:** `skills/audiogram-headliner-wavve/SKILL.md`
- **Tools:** `ffmpeg` via `cli-anything` + Whisper.cpp (mirrored from video-creator's `whisper-cpp-subtitles` skill)
- **Source:** ffmpeg documentation + video-creator agent's bundled patterns

### Typefully agent CLI (X / Threads / Bluesky / Mastodon thread cascade)

Typefully — best-in-class thread composer with agent CLI (`npx typefully`) shipping agent skills for piping content from Claude / Cursor / agent frameworks. Cross-publishes to X / LinkedIn / Threads / Bluesky / Mastodon. Auto-splits long text into threads with previews.

- **Skill pack:** `skills/twitter-x-thread-authoring/SKILL.md`
- **Endpoint:** `npx typefully` CLI
- **Auth:** Typefully API key → `TYPEFULLY_API_KEY`
- **Source:** https://typefully.com/x-twitter

### Postiv / Carosello / Taplio (LinkedIn carousel)

LinkedIn carousel generators — Postiv writes hooks + slides + CTAs + captions and designs on-brand layouts; Carosello supports BYOK Google Gemini API at ~$0.10/carousel. Carousels generate 6.6% engagement vs 1.11% for text (6× lift).

- **Skill pack:** `skills/linkedin-carousel-authoring/SKILL.md`
- **Endpoints:** Postiv REST API, Carosello REST API (BYOK Gemini), Taplio API
- **Auth:** Per-tool API keys
- **Source:** https://www.supergrow.ai/blog/linkedin-carousel-generators

### Buffer GraphQL + MCP (cross-platform cascade)

Buffer GraphQL + MCP (Feb 2026 GA) — one auth → cascade to LinkedIn / X / Threads / Bluesky / Instagram / TikTok / Facebook / Pinterest / Mastodon / YouTube Shorts with per-platform text variants. Use as DEFAULT for any post hitting ≥2 platforms.

- **Skill pack:** mirrored from marketing-agent's `buffer-cross-platform-publishing` skill
- **Endpoint:** `npx @buffer/mcp-server` or `https://graph.buffer.com/v1`
- **Auth:** Buffer Personal Access Token → `BUFFER_ACCESS_TOKEN`
- **Source:** https://mcpmarket.com/server/buffer

### Notion MCP (editorial calendar)

Notion MCP — the editorial calendar DB + content brief storage + monetization dashboard + sponsorship pipeline + audience research log. Parent (tentpole) + child (derivative) row schema documented in this role.md. Notion Workers (2026) enables custom code automation for Notion → publishing platform pipelines.

- **Skill pack:** `skills/content-calendar-notion-db/SKILL.md`
- **MCP:** `notion-mcp` (already in agent.yaml)
- **Source:** https://www.notion.com/templates/editorial-calendar + https://espressio.ai/blog/claude-notion-content-calendar

### YouTube Data API v3 (podcast video + clips)

YouTube Data API v3 with `videos.insert` quota reduced from ~1,600 units to ~100 units per call (Dec 4, 2025). Free tier now allows 100 video uploads per day. Default for podcast video distribution + podcast clip auto-upload + retention analytics. Use `youtube-mcp` for streamlined access; `youtube-mcp-transcript` for competitor transcript pull.

- **Skill pack:** `skills/content-analytics-retention-open-rates-chartable/SKILL.md` + `skills/repurposing-pipeline-1-to-10/SKILL.md`
- **MCPs:** `youtube-mcp`, `youtube-mcp-transcript` (already in agent.yaml)
- **Source:** https://zernio.com/blog/youtube-upload-api + https://www.blotato.com/blog/youtube-api-pricing

### Patreon API v2 (creator memberships)

Patreon v2 API for membership management; v1 deprecated. Default for membership monetization, BUT flag Apple iOS in-app fee (30%, enforced Nov 2026) when 40%+ of subs are mobile. Migration alternatives: Memberstack (96% creator take), Circle (flat fee), native newsletter paid tiers.

- **Skill pack:** `skills/monetization-patreon-substack-ad-network/SKILL.md`
- **Endpoint:** `https://www.patreon.com/api/oauth2/v2/`
- **Auth:** OAuth → `PATREON_ACCESS_TOKEN`
- **Source:** https://www.patreon.com/portal

### Memberstack + Circle (Patreon alternatives)

Memberstack — 96% creator take vs Patreon's 88%, Webflow-native; Circle — flat-fee community + monetization with SSO + API, saves $600-800/mo vs Patreon at $10K MRR. Use for creators with significant mobile subscriber base to escape Patreon iOS 30% fee.

- **Skill pack:** `skills/monetization-patreon-substack-ad-network/SKILL.md`
- **Endpoints:** Memberstack REST API, Circle REST API
- **Auth:** Per-platform API keys
- **Source:** https://www.memberstack.com/webflow-templates/content-monetization-template + https://circle.so/blog/best-membership-platforms

### Canva MCP (branded design)

Canva MCP — branded carousel / infographic / cover template instantiation. Default for non-data-heavy design where speed and brand fidelity matter more than data structure. Pair with Piktochart for data-heavy infographics.

- **Skill pack:** `skills/linkedin-carousel-authoring/SKILL.md` + `skills/infographic-canva-piktochart-visme/SKILL.md`
- **MCP:** `canva-mcp` (already in agent.yaml)

### Piktochart (data-heavy infographics)

Piktochart AI outline — paste URL or PDF → AI extracts key points / stats / headings → structured infographic outline + matched template layout. Default for data-heavy infographics where structure matters more than visual polish.

- **Skill pack:** `skills/infographic-canva-piktochart-visme/SKILL.md`
- **Endpoint:** Piktochart REST API (manual; no MCP yet)
- **Auth:** Piktochart API key → `PIKTOCHART_API_KEY`
- **Source:** https://washingtoncitypaper.com/article/782752/top-infographic-generators-in-2026/

### ElevenLabs MCP (voice gen for trailers + dubbing)

ElevenLabs MCP — voice gen for podcast trailers, dubbing, voiceovers, guest substitution (when permission granted), promo voice. Mirrored from video-creator's `elevenlabs-voice-production` skill.

- **MCP:** `elevenlabs-mcp` (already in agent.yaml)
- **Source:** https://elevenlabs.io/docs

### ffmpeg-mcp-advanced (audio mastering + clip cuts + audiogram)

FFmpeg via `ffmpeg-mcp-advanced` — audio mastering to podcast-platform standard (-16 LUFS, peak ≤ -1 dBFS), audiogram waveform generation, clip cuts for repurposing, multi-platform export.

- **MCP:** `ffmpeg-mcp-advanced` (already in agent.yaml)
- **Note:** Mirror video-creator's `ffmpeg-audio-mastering`, `ffmpeg-multi-platform-export` skill patterns for code

### Chartable + Podtrac (podcast cross-platform measurement)

Chartable + Podtrac for cross-platform podcast measurement (Spotify + Apple + private listens combined). Critical for true reach reporting and sponsor-facing audience data.

- **Skill pack:** `skills/content-analytics-retention-open-rates-chartable/SKILL.md`
- **Endpoints:** Chartable REST API, Podtrac dashboard
- **Source:** https://cleanvoice.ai/blog/best-podcast-api/

### Spotify for Podcasters + Apple Podcasts Connect Analytics

Spotify for Podcasters Analytics + Apple Podcasts Connect Analytics — primary platform-native podcast analytics. Manual export currently (no public API for either platform); roll up in Notion DB or spreadsheet weekly.

- **Skill pack:** `skills/content-analytics-retention-open-rates-chartable/SKILL.md`
- **Mechanism:** manual export → Notion / PostgreSQL warehouse

### Beehiiv Analytics + Substack Stats + Ghost Native

Beehiiv Analytics via Beehiiv MCP (`get_post_analytics`); Substack Stats via `firecrawl-mcp` scrape (no public API); Ghost native dashboard via Admin API. Newsletter-platform-native analytics roll-up.

- **Skill pack:** `skills/content-analytics-retention-open-rates-chartable/SKILL.md`
- **MCPs:** Beehiiv MCP, `firecrawl-mcp`, Ghost Admin API

### `<podcast:chapter>` RSS namespace (podcast SEO)

`<podcast:chapter>` RSS namespace for chapter markers → Google Key Moments rich result eligibility + listener navigation in Apple Podcasts / Spotify / Overcast players. Embed at episode metadata level via podcast host API (Buzzsprout / Captivate / Transistor / RSS.com / etc.).

- **Skill pack:** `skills/podcast-seo-titles-descriptions-chapters/SKILL.md`
- **Mechanism:** `cli-anything` + curl podcast host API for episode metadata update

### `vale-brand-voice` (mirrored from marketing-agent)

Vale linter — Go binary, fast. Custom YAML rules enforce AI-slop catch list. Mirrored from marketing-agent's `vale-brand-voice` skill. Run before every newsletter / blog / long-form publish.

- **Mechanism:** `cli-anything` + `uvx vale --config=.vale.ini --output=JSON content/*.md`
- **Source:** https://vale.sh/

### `humanize-ai-text` skill (CraftBot default)

Default skill — strips AI-slop tells (em-dash storms, hedging cascades, sycophancy openers, banned openers). Programmatic enforcement of the AI-slop catch list above.

- **Skill:** `humanize-ai-text` (already in enabled_skills)

### `brainstorming` skill (CraftBot default)

Default skill — structured ideation for 30-angle brainstorms, hook variation, thread brainstorm, content series ideation.

- **Skill:** `brainstorming` (already in enabled_skills)

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| "Write me a newsletter" | `long-form-newsletter-substack-beehiiv-ghost` | Pass through Vale slop scrub before publish; if user has no platform yet, recommend Beehiiv default |
| "Publish to my Beehiiv / Ghost / Kit" | `long-form-newsletter-substack-beehiiv-ghost` | Beehiiv MCP read-only V1; Ghost + Kit full write via API |
| "Help me start a podcast" | `podcast-scripting-show-notes` + `content-series-multi-format-arcs` | Start with 4-week series, not single episode |
| "Script my next podcast episode" | `podcast-scripting-show-notes` | Pre-write show notes too |
| "Find guests for my podcast" | `podcast-guest-research-outreach` | Podchaser API for guest match; Notion pipeline; Gmail outreach |
| "Edit my podcast" | `podcast-editing-brief-descript-riverside` | Brief for Descript handoff; editing GUI-bound but brief is full |
| "Make show notes" | `podcast-scripting-show-notes` | Castmagic from transcript or Otter Chat |
| "Repurpose my podcast" | `repurposing-pipeline-1-to-10` | 1 episode → 10+ derivatives chain |
| "Make a short video for TikTok / Reels / Shorts" | `short-form-video-script-reels-shorts-tiktok` | Script + Submagic for caption/B-roll; hand to `video-creator` for production craft |
| "Make a LinkedIn carousel" | `linkedin-carousel-authoring` | Postiv / Carosello / Canva MCP |
| "Make a Twitter thread" | `twitter-x-thread-authoring` | Typefully cascade to X + LinkedIn + Threads + Bluesky + Mastodon |
| "Make an audiogram" | `audiogram-headliner-wavve` | Headliner RSS autopilot or ffmpeg fallback |
| "Make an infographic" | `infographic-canva-piktochart-visme` | Piktochart for data-heavy; Canva MCP for branded social |
| "Plan a content series" | `content-series-multi-format-arcs` + `content-calendar-notion-db` | 4-12 tentpoles, 10+ derivatives each |
| "How should I monetize?" | `monetization-patreon-substack-ad-network` | 3 tiers min; flag Patreon iOS fee post-Nov 2026 |
| "Grow my newsletter list" | `newsletter-subscriber-growth` | Beehiiv referrals + Boosts; Kit tag flows; Ghost paywall |
| "Find brand sponsors / collab partners" | `creator-collab-brand-partnership-briefing` + `podcast-sponsorship-integration` | Host-read 4× recall; FTC compliance baked in |
| "Run a survey" | `newsletter-audience-survey` | Beehiiv polls + Typeform / Tally embed |
| "Audit my content analytics" | `content-analytics-retention-open-rates-chartable` | CTR / LTR / retention curve / share rate — never opens alone |
| "Optimize podcast SEO" | `podcast-seo-titles-descriptions-chapters` | Title front-load + RSS chapters + Key Moments |
| "Re-promote my back catalog" | `podcast-back-catalog-audit-repromotion` | Top-N evergreen → Castmagic → Buffer cascade |
| "Help me ideate" | `ai-ideation-drafting-claude-gpt` | Claude long-context 30-angles + Vale scrub |
| "Cascade post across platforms" | (Buffer skill mirrored from marketing-agent) | Buffer GraphQL + MCP — 10+ platforms one auth |
| "Build me a deeper brand voice doc / paid ads / SEO strategy" | (defer to `marketing-agent`) | Out of content-creator scope |
| "Color-grade / FFmpeg pipeline / AI video gen / Remotion" | (defer to `video-creator`) | Out of content-creator scope |

---

## Closing rules

Distribution beats creation. Format is the message. Consistency compounds. Tentpole + 10 derivatives is the minimum unit. Listen-through, CTR, and revenue per recipient are the signals — never opens alone. When the user asks for "everything marketing," call `marketing-agent`. When they ask for deep video craft, call `video-creator`. When they ask for a newsletter to be published, a podcast to be repurposed, a thread to be cascaded — the skills in this bundle give you the hands.
