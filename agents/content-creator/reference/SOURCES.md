# Content Creator — Sources

> Section→source map for `soul.md` and `role.md`. Ships in the bundle but is **not** loaded into the agent's context. For humans verifying provenance and for future updates.

## soul.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Title + persona intro | reference/SOTA_USE_CASES.md + adjacent v1 agents (`marketing-agent`, `video-creator`) | Action-verb-first per `_templates/soul_md_skeleton.md` operator framing rule |
| Convictions (3) | Synthesis grounded in 2026 creator-economy SOTA research; mirrors video-creator's conviction-anchor pattern | "Distribution > creation", "format is the message", "consistency compounds" |
| Purpose | reference/SOTA_USE_CASES.md + role mirroring of `marketing-agent` Purpose section | Defers explicitly to `marketing-agent` (broad) + `video-creator` (deep video) |
| Execution stack | reference/SOTA_USE_CASES.md | Per `_templates/soul_md_execution_stack_snippet.md` pattern. Lists 19 bundled skill packs. |
| When invoked | Synthesis of marketing-agent + video-creator When-invoked patterns adapted to content-creator's 8 modes | Newsletter / Podcast / Content series / Repurposing / Short-form / Carousel / Thread / Monetization / Analytics |
| Core operating rules | Convictions + 2026 SOTA grounding (host-read 4× recall; LTR 50% at 25-min; carousel 6.6% engagement; etc.) | Mirrors marketing-agent's compact-rules style |
| Mode-specific decisions | Mirrors marketing-agent + video-creator mode-decisions structure | Specific to content-creator's 9 modes |
| Quality gates | Per-mode SOTA benchmarks from research sources | Newsletter / Podcast / Series / Repurposing / Short-form / Carousel / Thread / Audiogram / Monetization / Analytics |
| Output format | Mirrors marketing-agent's output-format catalog | Specific to content-creator's 10 deliverable types |
| Communication style | Mirrors marketing-agent's communication-style rules | Lead-with-outcome, named-metric, active-voice, length-matches-channel |
| When to push back / defer | Synthesis grounded in 2026 SOTA evidence (Patreon iOS fee, Apple MPP, Headliner no API) + sibling-agent hand-off slugs | Hand-offs to `marketing-agent`, `video-creator`, `technical-writer` |
| PROACTIVE self-init footer | `METHODOLOGY.md` standard footer | Same wording across all agents; only routine questions differ |

## role.md → source map

| Section | Source(s) | Notes |
|---|---|---|
| Header note + grep headings | `_templates/role_md_skeleton.md` standard pattern | Lists all searchable H2/H3 headings |
| Capability reference | Synthesis from reference/SOTA_USE_CASES.md + marketing-agent's role.md capability-reference structure | 20+ content formats; 10 platform categories |
| Newsletter publishing playbook | Beehiiv vs Substack vs Ghost vs Kit comparisons (multiple 2026 sources); marketing-agent's lifecycle email patterns | Platform decision tree + cadence + issue template + brand voice rules + quality gates + analytics priorities |
| Podcast production playbook | Riverside vs Descript 2026; Cleanvoice podcast APIs; podcast SEO 2026 | Pre-production + production + post-production + show notes template + podcast SEO + analytics |
| Repurposing pipeline playbook | Castmagic + OpusClip + Munch + Submagic + Headliner research | Tentpole-to-derivative chain; 1→10 schedule template |
| Content series planning playbook | Notion editorial calendar template + Notion MCP usage | Parent/child Notion DB schema |
| LinkedIn carousel playbook | LinkedIn carousel engagement stats (Supergrow); Postiv / Carosello / Taplio tool research | 8-14 slide structure + authoring tools + quality gates |
| X thread playbook | Typefully + Posteverywhere thread-scheduler research | Rule of 7 + thread template + cross-platform cascade |
| Audiogram playbook | Headliner + Wavve + Recast + ffmpeg fallback research | ffmpeg recipe + tool choice + quality gates |
| Infographic playbook | Canva / Adobe Express / Piktochart 2026 research | Tool decision + brief template + quality gates |
| Monetization stack playbook | Patreon v2 + Memberstack + Circle research; Beehiiv vs Substack vs Ghost monetization | Stack components + pricing tiers + Patreon iOS fee flag |
| Content analytics playbook | Beehiiv Analytics + Spotify/Apple manual + Chartable/Podtrac + YouTube Data API research | Per-format primary signals + tool chain + reporting cadence |
| AI-slop catch list | Mirrored from marketing-agent's `vale-brand-voice` AI-slop catch list | Operational glue; banned openers + jargon + sycophancy + style problems |
| SOTA tool reference | reference/SOTA_USE_CASES.md + per-tool docs | H3 per tool with skill pack pointer + endpoint + auth + source |
| SOTA execution playbook (table) | reference/SOTA_USE_CASES.md verdict + skill pack inventory | User-request → first-stop skill pack mapping |

## SOTA tool sources (June 2026)

> One row per SOTA tool referenced in the agent.

| Tool | Source URL | Used for |
|---|---|---|
| Beehiiv MCP (March 24, 2026 launch) | https://product.beehiiv.com/p/beehiiv-mcp | `long-form-newsletter-substack-beehiiv-ghost` skill pack — V1 read-only |
| Beehiiv MCP integration guide | https://www.buildmvpfast.com/blog/beehiiv-mcp-newsletter-ai-agent-integration-2026 | Skill pack workflow examples |
| Kit vs Beehiiv 2026 | https://www.knockedupmoney.com/blog/convertkit-vs-beehiiv-whats-the-best-newsletter-platform | Platform decision tree (newsletter mode) |
| Beehiiv vs Substack vs Ghost monetisation 2026 | https://earnifyhub.com/blog/blogging/beehiiv-vs-substack-vs-ghost-monetisation.php | 0% revenue share for Beehiiv + Ghost; Substack 10% |
| Ghost vs Beehiiv | https://ghost.org/vs/beehiiv/ | Ghost Content + Admin API + independent publisher CMS positioning |
| Sequenzy — Best newsletter platforms 2026 | https://www.sequenzy.com/blog/best-newsletter-platforms | Platform landscape (21 platforms tested) |
| Riverside vs Descript 2026 (Speakwise) | https://speakwiseapp.com/blog/descript-vs-riverside | Recording vs editing distinction; API capability boundaries |
| Descript vs Riverside 2026 (AI Productivity) | https://aiproductivity.ai/blog/descript-vs-riverside-2026/ | Tool decision tree (podcast mode) |
| Cleanvoice — Top podcast APIs 2026 | https://cleanvoice.ai/blog/best-podcast-api/ | Podcast API landscape (10 APIs surveyed) |
| Riverside API review | https://cleanvoice.ai/blog/riverside-api-review/ | API capability boundary (transcript+media YES, editing NO) |
| Castmagic Stormy AI repurposing 2026 | https://stormy.ai/blog/best-gpt-repurposing-tools-2026-opusclip-munch-castmagic | Castmagic MCP for Claude; tool positioning |
| Blotato — Best AI content repurposing 2026 | https://www.blotato.com/blog/ai-content-repurposing-tools | Tentpole-to-derivative decision matrix |
| Submagic | https://www.submagic.co/ | 99% caption accuracy in 48 langs; Business+ API; auto-edit |
| Submagic review 2026 | https://max-productive.ai/ai-tools/submagic/ | Short-form video AI editing |
| Headliner | https://www.headliner.app/ | RSS autopilot per-episode audiogram + YouTube auto-upload |
| Podosphere — Best audiogram tools 2026 | https://www.thepodosphere.com/blog/podcast-audiogram-tools-2026 | Audiogram landscape (Headliner / Wavve / Recast / Percify) |
| Podchaser API vs Listen Notes API | https://www.podchaser.com/articles/api/podchaser-api-vs-listen-notes-api | Guest research (6M+ podcasts, 32M+ structured credits) |
| Podcast SEO 2026 (Spear Point) | https://www.thespearpoint.com/blog/seo-for-podcasts | Chapter SEO + Google Key Moments + `<podcast:chapter>` |
| Shownotes — Podcast SEO tools 2026 | https://shownotes.ai/podcast-seo-tools | Podcast discoverability + chapter optimization |
| Typefully + agent CLI | https://typefully.com/x-twitter | Thread cascade (X/LinkedIn/Threads/Bluesky/Mastodon) |
| Posteverywhere — Best X schedulers 2026 | https://posteverywhere.ai/blog/best-x-twitter-scheduler | Typefully positioning as best thread composer |
| Supergrow — LinkedIn carousel generators 2026 | https://www.supergrow.ai/blog/linkedin-carousel-generators | 1.6× engagement vs text; 6.6% carousel rate |
| ContentIn — LinkedIn carousel generators 2026 | https://contentin.io/blog/best-linkedin-carousel-generators/ | Postiv / Carosello / Taplio tool positioning |
| Notion editorial calendar template | https://www.notion.com/templates/editorial-calendar | DB schema (parent tentpole + child derivative) |
| Notion AI content calendar with Claude | https://espressio.ai/blog/claude-notion-content-calendar | Notion MCP for editorial DB workflow |
| Patreon developer portal (v2) | https://www.patreon.com/portal | Patreon API v2; v1 deprecated; iOS 30% fee Nov 2026 |
| Memberstack content monetization | https://www.memberstack.com/webflow-templates/content-monetization-template | 96% creator take vs Patreon 88% |
| Circle community + monetization | https://circle.so/blog/best-membership-platforms | Flat-fee community + SSO + API |
| Otter podcast transcription | https://otter.ai/podcast-transcription | Otter AI Chat for show notes |
| Top transcription tools 2026 (Gupta) | https://guptadeepak.com/tools/top-5-ai-transcription-tools-2026/ | Whisper / Otter / Granola comparison |
| Buffer GraphQL + MCP | https://mcpmarket.com/server/buffer | Cross-platform cascade (10+ platforms one auth) |
| YouTube Upload API (quota reduced 1600→100 units Dec 4 2025) | https://zernio.com/blog/youtube-upload-api | Podcast clip / video upload free 100/day |
| YouTube API pricing 2026 | https://www.blotato.com/blog/youtube-api-pricing | Free tier quotas |
| Podosphere — Best podcast hosting 2026 | https://www.thepodosphere.com/blog/best-podcast-hosting-platforms-2026-comparison-guide | Buzzsprout / Transistor / Captivate positioning |
| ThoughtLeaders — Podcast trends 2026 | https://www.thoughtleaders.io/blog/podcast-trends-2026 | Host-read 4× recall; network-cascade sponsorship; video-first SOTA |
| Best infographic generators 2026 | https://washingtoncitypaper.com/article/782752/top-infographic-generators-in-2026/ | Piktochart AI outline; Canva vs Adobe Express vs Piktochart |
| Piktochart — Adobe Express alternatives | https://piktochart.com/blog/adobe-express-alternatives/ | Piktochart positioning for data-heavy infographics |

## Notes on authored-from-synthesis

Sections that aren't directly lifted from a single source (all are operational glue, not domain claims):

- **soul.md Communication style** — operational glue extracted from marketing-agent's communication-style rules and adapted to content-creator's tone; no single canonical source.
- **soul.md Output format** — synthesis of marketing-agent + video-creator output-format catalogs adapted to content-creator's 10 deliverable types.
- **role.md AI-slop catch list** — mirrored from marketing-agent's `vale-brand-voice` catch list with content-creator-specific additions (banned openers like "I've been thinking about"); operational glue.
- **role.md Newsletter quality gates / Podcast quality gates / etc.** — operational synthesis of per-format SOTA benchmarks from cited sources; no single canonical checklist source per format.
- **role.md ffmpeg audiogram recipe** — operational glue authored from ffmpeg docs + video-creator's bundled ffmpeg skill patterns; no single canonical recipe source.
- **role.md Repurposing pipeline 1→10 schedule** — operational synthesis from Castmagic + OpusClip + Submagic + Headliner per-tool research; no single canonical schedule.

## Refreshing from upstream

When SOTA tools change (e.g., Beehiiv MCP V2 write capabilities ship, Headliner releases public API, Patreon iOS fee enforcement date changes):

1. Update the relevant skill pack(s) in `agents/content-creator/skills/<name>/SKILL.md` (Round 2 will create these folders).
2. Update the SOTA sources table above.
3. Update `reference/SOTA_USE_CASES.md` confidence ratings if applicable.
4. Update `USE_CASES.md` Remaining caveats section to reflect new status.
5. Re-run `python verify.py content-creator` to confirm structure intact.
6. Re-build: `python build.py content-creator` produces a fresh `.craftbot`.

For the canonical reference repos (Step 2):
- `wshobson/agents` — re-pull every quarter for SOTA content/marketing agent definitions.
- `VoltAgent/awesome-claude-code-subagents` — same cadence.
- `msitarzewski/agency-agents` — same cadence (look for `marketing-content-creator` and `marketing-podcast-strategist`).
- Beehiiv MCP changelog — monitor for V2 write capabilities launch.
- Castmagic MCP changelog — monitor for new transformation types.
- Typefully CLI changelog — monitor for new platform integrations.
