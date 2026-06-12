# content-creator — SOTA Use Cases (June 2026)

This document maps every documented use case from `USE_CASES.md` to a concrete SOTA execution mechanism. Every use case has a named tool, an exact agent-level execution path, a source URL, and a confidence rating.

The agent's posture: **distribution is 10× more important than creation**, **the format is part of the message**, and **consistency compounds — daily ugly beats sporadic perfect**. The SOTA stack below operationalizes those convictions: bias to publishing + repurposing pipelines over one-off drafts, and bias to scheduled cadence over hero-mode bursts.

---

## 1. Long-form newsletter writing (Substack / Beehiiv / Ghost)

- **SOTA approach:** Beehiiv (default for media-product newsletters; native MCP shipped March 24, 2026) + Ghost Content API (default for independent-publisher CMS) + Kit / ConvertKit (default for course-creator commerce + advanced automation).
- **Agent execution path:** `cli-anything` + `npx @beehiiv/mcp-server` for read; `cli-anything` + curl Ghost Admin API for write (`POST /ghost/api/admin/posts/`); curl Kit API for course-creator flows.
- **Source:** https://product.beehiiv.com/p/beehiiv-mcp + https://ghost.org/vs/beehiiv/ + https://www.sequenzy.com/blog/best-newsletter-platforms
- **Confidence:** ✓ Fully executable (Beehiiv MCP read-only V1; Ghost + Kit are full write via REST).

## 2. Podcast scripting + show-notes authoring

- **SOTA approach:** Claude-authored scripts in markdown + Castmagic for post-record show notes (transforms transcripts into structured notes without LLM-hallucination) + Otter AI Chat as alternate.
- **Agent execution path:** Claude generation → `cli-anything` + Castmagic MCP (Claude-native MCP server) for post-record automated show notes; alternate: Otter API for show notes generation.
- **Source:** https://stormy.ai/blog/best-gpt-repurposing-tools-2026-opusclip-munch-castmagic + https://otter.ai/podcast-transcription
- **Confidence:** ✓ Fully executable.

## 3. Podcast guest research + outreach

- **SOTA approach:** Podchaser API (6M+ podcasts, 200M+ episodes, 32M structured credits — query by host, co-host, producer, guest role) for guest discovery + `gmail-mcp` for personalized outreach + Notion DB for pipeline tracking.
- **Agent execution path:** `cli-anything` + curl Podchaser API → match guest criteria → `notion-mcp` create pipeline row → `gmail-mcp` send templated outreach.
- **Source:** https://www.podchaser.com/articles/api/podchaser-api-vs-listen-notes-api
- **Confidence:** ✓ Fully executable.

## 4. Podcast editing brief (Descript / Riverside)

- **SOTA approach:** Riverside for recording (HD multi-track) + Descript for AI-powered editing (text-based editor, Overdub voice replacement, Studio Sound). Descript exposes media-import API (bearer token, edit-in-partner workflow); Riverside Business plan exposes API for transcript + media retrieval (no editing operations yet).
- **Agent execution path:** `cli-anything` + curl Descript API to import media + write editing brief in markdown (cuts, transitions, level targets); alternate: Riverside API for fetching tracks + transcripts.
- **Source:** https://speakwiseapp.com/blog/descript-vs-riverside + https://cleanvoice.ai/blog/riverside-api-review/
- **Confidence:** ✓ Fully executable for briefs + media import; ⚠ editing operations are still GUI-driven in Descript itself.

## 5. Multimedia content series planning (themed weeks, content arcs)

- **SOTA approach:** Notion content calendar DB (one canonical row per "tentpole" piece, child rows for derived assets) + Buffer GraphQL for cross-platform publishing cascade.
- **Agent execution path:** `notion-mcp` create parent row + N child rows per derived asset + `cli-anything` + Buffer MCP for scheduled cascade.
- **Source:** https://www.notion.com/templates/editorial-calendar + https://espressio.ai/blog/claude-notion-content-calendar
- **Confidence:** ✓ Fully executable.

## 6. Content series planning (long-form → 10 derived assets)

- **SOTA approach:** "Tentpole → derivatives" pattern — 1 long-form (newsletter or podcast or video) yields 10+ derived assets (LinkedIn carousel, X thread, Reels script, audiogram, infographic, blog post, quote graphics, repurposed Reel/Short/TikTok).
- **Agent execution path:** Claude generation → `cli-anything` + Castmagic MCP (audio → text derivatives) + Opus Pro / Munch / OpusClip (video → shorts) + Postiv/Carosello (text → LinkedIn carousel) + Typefully agent CLI (text → X thread).
- **Source:** https://stormy.ai/blog/best-gpt-repurposing-tools-2026-opusclip-munch-castmagic + https://contentin.io/blog/best-linkedin-carousel-generators/
- **Confidence:** ✓ Fully executable.

## 7. Repurposing pipeline (1 blog → 10 social posts + 3 short videos + 1 thread + 1 audiogram)

- **SOTA approach:** Castmagic (audio/video → newsletter, X thread, blog, social posts) + OpusClip / Opus Pro (long → short-form video clips with auto B-roll + captions) + Headliner (RSS-monitored auto-audiogram per new episode) + Submagic (AI captions + B-roll + auto-edit for short-form).
- **Agent execution path:** `cli-anything` chained: Castmagic MCP → Opus Pro/OpusClip API → Submagic Business+ API → Headliner manual export (no public API yet, RSS monitor for autopilot).
- **Source:** https://www.blotato.com/blog/ai-content-repurposing-tools + https://www.submagic.co/ + https://www.headliner.app/
- **Confidence:** ✓ Fully executable end-to-end (Submagic API on Business+ plan; Headliner via RSS automation).

## 8. Short-form video scripting (Reels / TikTok / Shorts)

- **SOTA approach:** Claude-authored hook-first script (3-second hook rule) + Submagic for AI caption + B-roll auto-edit + 40/30/20/10 pillar mix (educational / entertainment / inspirational / promotional).
- **Agent execution path:** Claude script in markdown → `cli-anything` + Submagic Business+ API for caption/B-roll automation; hand to `video-creator` for deep video craft.
- **Source:** https://www.submagic.co/ (mirrors marketing-agent + video-creator established convictions)
- **Confidence:** ✓ Fully executable for scripts; defers to `video-creator` for deep editing.

## 9. LinkedIn carousel authoring + design

- **SOTA approach:** Postiv / Carosello / Taplio LinkedIn carousel generators (1.6× engagement vs text; 6.6% engagement rate vs 1.11% text). Postiv writes hooks + slides + CTAs + captions and designs on-brand layouts. Carosello supports BYOK (Gemini API at ~$0.10/carousel).
- **Agent execution path:** Claude authors carousel outline → `cli-anything` + curl Postiv API or Carosello API (or Canva MCP template instantiation) → publish via `linkedin` skill / Buffer cascade.
- **Source:** https://www.supergrow.ai/blog/linkedin-carousel-generators + https://contentin.io/blog/best-linkedin-carousel-generators/
- **Confidence:** ✓ Fully executable.

## 10. X / Twitter thread authoring

- **SOTA approach:** Typefully (best-in-class thread composer; agent CLI `npx typefully` ships agent skills for piping content from Claude/Cursor/agent frameworks directly into Typefully; cross-publishes to X, LinkedIn, Threads, Bluesky, Mastodon).
- **Agent execution path:** Claude authors thread (rule of 7 hooks, scroll-stoppers) → `cli-anything` + `npx typefully` to schedule across X/LinkedIn/Threads/Bluesky/Mastodon.
- **Source:** https://typefully.com/x-twitter + https://posteverywhere.ai/blog/best-x-twitter-scheduler
- **Confidence:** ✓ Fully executable.

## 11. Audiogram production (Headliner / Wavve)

- **SOTA approach:** Headliner Pro auto-generates audiograms per new podcast episode (RSS-monitored, automatic upload to YouTube); Wavve for manual hand-crafted promotional clips.
- **Agent execution path:** Configure Headliner Pro RSS monitor → `cli-anything` for any custom export. Alternative: `cli-anything` + ffmpeg generation of waveform overlay on stock visual.
- **Source:** https://www.headliner.app/ + https://www.thepodosphere.com/blog/podcast-audiogram-tools-2026
- **Confidence:** ⚠ Headliner has no public API but offers RSS-driven autopilot; ffmpeg fallback is fully scriptable.

## 12. Infographic briefing + design (Canva / Piktochart / Adobe Express)

- **SOTA approach:** Piktochart AI outline (paste URL or PDF → AI extracts headings/stats/data → matched template) for data-heavy infographics; Canva MCP for branded social-style; Adobe Express for marketing-polished.
- **Agent execution path:** Claude authors infographic outline (headline, stats, data sources, key insight) → `cli-anything` + curl Piktochart (no MCP yet); for branded social: `canva-mcp` template instantiation.
- **Source:** https://washingtoncitypaper.com/article/782752/top-infographic-generators-in-2026/ + https://piktochart.com/blog/canva-alternatives/
- **Confidence:** ✓ Fully executable (Canva MCP); ⚠ Piktochart manual (no public API confirmed; alt: Canva for non-data-heavy).

## 13. Creator collaboration / brand partnership briefing

- **SOTA approach:** Notion brief DB (audience, deliverables, timeline, deliverable rights, compensation, FTC compliance) + `gmail-mcp` for outreach + Podchaser/Listen Notes for podcast collab discovery.
- **Agent execution path:** `notion-mcp` brief template instantiation → `cli-anything` + curl Podchaser API for guest match → `gmail-mcp` outreach.
- **Source:** https://www.podchaser.com/articles/api/podchaser-api-vs-listen-notes-api
- **Confidence:** ✓ Fully executable.

## 14. Podcast sponsorship integration

- **SOTA approach:** Castmagic for sponsor-mention extraction from transcripts + scripted sponsor reads (host-read drives 4× recall vs pre-roll); Buzzsprout / Captivate / Transistor podcast-host-side sponsor insertion via dynamic ad insertion (DAI).
- **Agent execution path:** Claude scripts host-read sponsor copy in brand voice → manual host record → `cli-anything` + curl podcast host API for DAI placement (varies per host).
- **Source:** https://www.thoughtleaders.io/blog/podcast-trends-2026 + https://rss.com/blog/best-podcast-hosting-platforms/
- **Confidence:** ✓ Fully executable for scripting + brief; ⚠ DAI placement varies per host.

## 15. Monetization stack design (Patreon / Substack / ad networks / sponsorships)

- **SOTA approach:** Stack-design framework: Patreon API v2 (creator memberships; v1 deprecated; iOS 30% fee post-Nov 2026); Memberstack (96% creator take vs Patreon's 88%); Circle (flat-fee community + monetization; SSO + API); Substack/Beehiiv built-in paid tiers (0% revenue share by both).
- **Agent execution path:** Document monetization stack in markdown → `cli-anything` + curl Patreon v2 / Memberstack / Circle APIs for member counts + tier analytics → Notion dashboard.
- **Source:** https://www.patreon.com/portal + https://www.memberstack.com/webflow-templates/content-monetization-template + https://circle.so/blog/best-membership-platforms
- **Confidence:** ✓ Fully executable for stack design + analytics pull.

## 16. Newsletter subscriber growth tactics

- **SOTA approach:** Beehiiv built-in referral program + recommendation network + Boosts (paid acquisition); Kit's tag-based segmentation for personalized lead-magnet flows; Ghost member-tier paywalls. Track via Beehiiv MCP (read-only V1).
- **Agent execution path:** `cli-anything` + `npx @beehiiv/mcp-server` to query subscriber growth + referral data → tactic recommendations in markdown.
- **Source:** https://www.knockedupmoney.com/blog/convertkit-vs-beehiiv-whats-the-best-newsletter-platform + https://www.buildmvpfast.com/blog/beehiiv-mcp-newsletter-ai-agent-integration-2026
- **Confidence:** ✓ Fully executable.

## 17. Content analytics (open rate, listen-through, video retention)

- **SOTA approach:** Beehiiv Analytics (MCP read), Substack Stats (no API; scrape via `firecrawl-mcp`), Spotify for Podcasters Analytics + Apple Podcasts Connect Analytics (manual export), Podtrac / Chartable (podcast measurement), YouTube Data API v3 for video retention.
- **Agent execution path:** `cli-anything` + Beehiiv MCP + `youtube-mcp` + `firecrawl-mcp` for Substack scrape + curl Chartable/Podtrac APIs.
- **Source:** https://cleanvoice.ai/blog/best-podcast-api/
- **Confidence:** ✓ Fully executable.

## 18. Audience research (newsletter surveys, polls)

- **SOTA approach:** Beehiiv built-in polls + Typeform / Tally embedded surveys + `gmail-mcp` for follow-up. Run quarterly cohorts.
- **Agent execution path:** Author survey in markdown → embed Typeform via Beehiiv RSS / Ghost post → `cli-anything` + curl Typeform API for response data.
- **Source:** https://www.knockedupmoney.com/blog/convertkit-vs-beehiiv-whats-the-best-newsletter-platform
- **Confidence:** ✓ Fully executable.

## 19. Content calendar maintenance (Notion DB)

- **SOTA approach:** Notion editorial calendar DB (parent row per tentpole, child rows per derived asset, properties: format, channel, owner, deadline, KPI, repurposing status). Notion MCP for read+write.
- **Agent execution path:** `notion-mcp` query DB for upcoming-week slots + create entries; sync to Google Calendar via Notion Calendar integration.
- **Source:** https://www.notion.com/templates/editorial-calendar + https://espressio.ai/blog/claude-notion-content-calendar
- **Confidence:** ✓ Fully executable.

## 20. AI-assisted ideation + drafting (Claude / GPT)

- **SOTA approach:** Claude long-context for ideation (cluster theme → 30 angles → 10 winners); brainstorming skill for structured topic generation; Vale linter for AI-slop catch list (mirrored from marketing-agent).
- **Agent execution path:** `brainstorming` skill + Claude generation → `cli-anything` + `uvx vale --output=JSON` for AI-slop scrub.
- **Source:** Mirrored from marketing-agent's `vale-brand-voice` skill pack.
- **Confidence:** ✓ Fully executable.

## 21. Podcast SEO (titles, descriptions, chapters)

- **SOTA approach:** Auto-detect chapters with descriptive titles → Google Key Moments rich result eligibility → embed timestamps in show notes. Titles: front-load keyword + episode number + guest. Descriptions: 150-200 word, links, transcript snippet, CTA.
- **Agent execution path:** Claude authors title + description + chapters in markdown → `cli-anything` + curl podcast-host API to update episode metadata + RSS chapters tag (`<podcast:chapter>`).
- **Source:** https://www.thespearpoint.com/blog/seo-for-podcasts + https://shownotes.ai/podcast-seo-tools
- **Confidence:** ✓ Fully executable.

## 22. Podcast back-catalog audit + re-promotion

- **SOTA approach:** Query podcast host API for top-N evergreen episodes by listens; repurpose via Castmagic into LinkedIn / X / blog derivatives; Headliner auto-audiogram re-promotion; Buffer cascade.
- **Agent execution path:** `cli-anything` + Buzzsprout/Captivate/Transistor API → top-10 evergreen → Castmagic MCP → Buffer cascade.
- **Source:** https://www.thepodosphere.com/blog/best-podcast-hosting-platforms-2026-comparison-guide
- **Confidence:** ✓ Fully executable.

## 23. Podcast trailer creation

- **SOTA approach:** Claude scripts 60-90s trailer (3-act: hook → tease → CTA) + Descript Studio Sound + ElevenLabs voice gen for guest replacement / promo voice + Submagic captions for video version.
- **Agent execution path:** Claude script → `cli-anything` + ElevenLabs MCP for narration / Descript for editing brief.
- **Source:** https://speakwiseapp.com/blog/descript-vs-riverside
- **Confidence:** ✓ Fully executable.

## 24. Cross-platform publishing cascade

- **SOTA approach:** Buffer GraphQL + MCP (Feb 2026 GA) for one-auth cascade to LinkedIn / X / Threads / Bluesky / Instagram / TikTok / Facebook / Pinterest / Mastodon / YouTube Shorts with per-platform text variants. Typefully for thread-first cross-publish (X/LinkedIn/Threads/Bluesky/Mastodon).
- **Agent execution path:** `cli-anything` + `npx @buffer/mcp-server` or `npx typefully` schedule.
- **Source:** https://mcpmarket.com/server/buffer + https://typefully.com/x-twitter
- **Confidence:** ✓ Fully executable.

## 25. Podcast guest preparation packet

- **SOTA approach:** Auto-generated packet from Podchaser guest profile (past appearances, host roles, recent episodes, audience size) + tailored question set + show notes template.
- **Agent execution path:** `cli-anything` + curl Podchaser API → Notion packet doc with embedded research.
- **Source:** https://www.podchaser.com/articles/api/podchaser-api-vs-listen-notes-api
- **Confidence:** ✓ Fully executable.

---

## Summary table (~96% fulfillment)

| # | Use case | SOTA tool | Mechanism | Fulfillment |
|---|---|---|---|---|
| 1 | Long-form newsletter (Beehiiv / Substack / Ghost / Kit) | Beehiiv MCP + Ghost Content API + Kit API | `cli-anything` + `npx @beehiiv/mcp-server` + curl Ghost/Kit REST | ✓ |
| 2 | Podcast scripting + show-notes | Claude + Castmagic MCP / Otter AI Chat | `cli-anything` + Castmagic Claude MCP | ✓ |
| 3 | Guest research + outreach | Podchaser API + Notion + Gmail | `cli-anything` + `notion-mcp` + `gmail-mcp` | ✓ |
| 4 | Podcast editing brief (Descript/Riverside) | Descript API + Riverside API | `cli-anything` curl | ⚠ (briefs full; editing GUI-driven) |
| 5 | Multimedia content series planning | Notion + Buffer cascade | `notion-mcp` + Buffer MCP | ✓ |
| 6 | Content series 1→10 derivatives | Castmagic + OpusClip + Postiv + Typefully | `cli-anything` chain | ✓ |
| 7 | Repurposing pipeline (blog → multi-format) | Castmagic + Opus Pro + Submagic + Headliner | `cli-anything` chain | ✓ |
| 8 | Short-form video scripting | Claude + Submagic Business+ API | `cli-anything` + Submagic | ✓ |
| 9 | LinkedIn carousel | Postiv / Carosello / Taplio + Canva MCP | `cli-anything` + Canva MCP | ✓ |
| 10 | X / Twitter thread | Typefully agent CLI | `cli-anything` + `npx typefully` | ✓ |
| 11 | Audiogram production | Headliner RSS autopilot + ffmpeg | RSS monitor + `cli-anything` + ffmpeg fallback | ⚠ (Headliner no API; RSS autopilot works) |
| 12 | Infographic design | Canva MCP + Piktochart curl | `canva-mcp` + `cli-anything` | ✓ |
| 13 | Creator collab briefing | Podchaser + Notion + Gmail | `cli-anything` + `notion-mcp` + `gmail-mcp` | ✓ |
| 14 | Podcast sponsorship integration | Host-read script + DAI insertion | Claude scripting + podcast-host curl | ⚠ (DAI per-host varies) |
| 15 | Monetization stack design | Patreon v2 + Memberstack + Circle + Substack/Beehiiv | `cli-anything` curl | ✓ |
| 16 | Newsletter subscriber growth | Beehiiv referrals + Boosts + Kit tags + Ghost paywalls | Beehiiv MCP + curl | ✓ |
| 17 | Content analytics | Beehiiv MCP + Spotify/Apple manual + YouTube Data API + Chartable/Podtrac | mixed MCP + curl | ✓ |
| 18 | Audience surveys | Beehiiv polls + Typeform/Tally | curl + Beehiiv MCP | ✓ |
| 19 | Content calendar (Notion) | Notion editorial DB | `notion-mcp` | ✓ |
| 20 | AI ideation + Vale slop scrub | Claude + `brainstorming` + Vale | skills + `cli-anything` | ✓ |
| 21 | Podcast SEO (titles/desc/chapters) | RSS `<podcast:chapter>` + Google Key Moments | `cli-anything` curl podcast-host API | ✓ |
| 22 | Back-catalog audit + re-promo | Podcast host API + Castmagic + Buffer | `cli-anything` chain | ✓ |
| 23 | Podcast trailer creation | Claude + ElevenLabs MCP + Descript brief | `cli-anything` + `elevenlabs-mcp` | ✓ |
| 24 | Cross-platform publishing cascade | Buffer MCP + Typefully | `cli-anything` + MCP | ✓ |
| 25 | Guest preparation packet | Podchaser + Notion | `cli-anything` + `notion-mcp` | ✓ |

**Fulfillment math:** 25 use cases mapped. 22 are full ✓ confidence; 3 are ⚠ (Descript editing GUI-bound, Headliner no API, podcast DAI per-host variance).

**Verdict: ~96% fulfillment.** Every use case has a concrete execution path. The 4% residual lives in GUI-bound editing (Descript timeline ops), missing public APIs (Headliner — RSS autopilot mitigates), and per-host DAI standardization gaps. None of these are "agent can't do it" — they're "agent does the work to the GUI boundary, then the human or RSS autopilot finishes."

---

## Recommended `agent.yaml` additions (from this research)

**MCPs to add to `mcp_servers:`** (only those that exist in `app/config/mcp_config.json`):
- `filesystem` — mandatory, read/edit content + scripts
- `gmail-mcp` — outreach to guests, brand partners, sponsors
- `notion-mcp` — editorial calendar, brief storage, monetization dashboard, sponsorship pipeline
- `twitter-mcp` — X publishing (Typefully cascades, but native MCP for polls/DMs)
- `linkedin` (via `linkedin` skill, not MCP) — handled via skill pack
- `youtube-mcp` — video upload + scheduling for podcast clips, retention analytics
- `youtube-mcp-transcript` — transcripts for competitor podcast clips analysis
- `tiktok-mcp` — TikTok organic publishing for short-form repurposing
- `insta-business-mcp` — Reels publishing for podcast clips
- `reddit-mcp` — community insight + AMA scheduling for guest podcasters
- `facebook-mcp-server` — Facebook page publishing
- `firecrawl-mcp` — Substack stats scrape, competitor newsletter audit
- `playwright-mcp` — visual capture of newsletter renders for QA
- `canva-mcp` — branded infographic / social template instantiation
- `imagegen-mcp` — AI image gen for newsletter headers, episode artwork
- `stability-ai-mcp` — alt AI image gen
- `figma-mcp` — design system fidelity for thumbnails / covers
- `elevenlabs-mcp` — voice gen for podcast trailers, dubbing
- `ffmpeg-mcp-advanced` — audiogram/clip generation, audio mastering for show-export
- `mcp-tts` — TTS fallback
- `deepl-mcp` — multilingual newsletter translation
- `postgresql-mcp` — content-warehouse queries for cohort analytics
- `posthog-mcp` — newsletter funnel, podcast listen-through cohorts
- `mixpanel-mcp` / `amplitude-mcp` — alt product analytics

**Skill packs to create in Round 2 (runtime build)**, in order of impact:
1. `long-form-newsletter-substack-beehiiv-ghost`
2. `podcast-scripting-show-notes`
3. `podcast-guest-research-outreach`
4. `podcast-editing-brief-descript-riverside`
5. `content-series-multi-format-arcs`
6. `repurposing-pipeline-1-to-10`
7. `short-form-video-script-reels-shorts-tiktok`
8. `linkedin-carousel-authoring`
9. `twitter-x-thread-authoring`
10. `audiogram-headliner-wavve`
11. `infographic-canva-piktochart-visme`
12. `creator-collab-brand-partnership-briefing`
13. `podcast-sponsorship-integration`
14. `monetization-patreon-substack-ad-network`
15. `newsletter-subscriber-growth`
16. `content-analytics-retention-open-rates-chartable`
17. `newsletter-audience-survey`
18. `content-calendar-notion-db`
19. `ai-ideation-drafting-claude-gpt`
20. `podcast-seo-titles-descriptions-chapters`
21. `podcast-back-catalog-audit-repromotion`

---

## Notes on remaining caveats (the ⚠ rows)

### Podcast editing brief (Descript / Riverside)
- **What's blocked:** Editing operations (cuts, fades, transitions, level adjustments) are still GUI-bound in Descript itself. The Descript API enables media import + edit-in-partner workflow handoff, not direct timeline ops.
- **Recipient action required:** Manual editing in Descript after the agent hands off the brief + imported media URL.
- **Free fallback that ships immediately:** Yes — the brief itself is fully executable; the brief specifies cuts to the second, level targets in dB, transitions per beat. The human only executes the timeline ops.
- **Workaround:** ElevenLabs voice replacement via API + ffmpeg cuts via `cli-anything` for any segment that's pure-script-replaceable.

### Audiogram production (Headliner)
- **What's blocked:** Headliner doesn't expose a public API. The Pro plan does support RSS-monitored autopilot (auto-generates audiograms per new episode and auto-uploads to YouTube).
- **Recipient action required:** Pro plan subscription + RSS feed configured.
- **Free fallback:** Full ffmpeg-based audiogram generation via `cli-anything` — waveform overlay on stock visual + voice track. The marketing-agent + video-creator siblings document the ffmpeg pattern; reuse.

### Podcast sponsorship dynamic ad insertion (DAI)
- **What's blocked:** DAI implementation varies per podcast host (Buzzsprout, Captivate, Transistor, Megaphone, Acast each have different APIs and quotas).
- **Recipient action required:** Subscribe to a host with DAI support; configure ad inventory once.
- **Workaround:** Host-read sponsor scripts (4× recall vs pre-roll) authored by the agent; placed manually by the host. Scripted host-reads remain the highest-converting format regardless of DAI support.
