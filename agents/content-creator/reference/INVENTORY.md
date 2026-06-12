# content-creator — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`) plus mirroring of the adjacent `marketing-agent` (parent) and `video-creator` (sibling specialist) v1 bundles which had already been research-grounded.

For future tightening: pull 4-6 reference agents from `wshobson/agents`, `VoltAgent/awesome-claude-code-subagents`, `msitarzewski/agency-agents`, `vijaythecoder/awesome-claude-agents` into `reference/agents/`, and 6-10 reference skills into `reference/skills/`.

## Sources used (June 2026 web research)

| Source | URL | Used for |
|---|---|---|
| Beehiiv MCP (March 24, 2026 launch) | https://product.beehiiv.com/p/beehiiv-mcp | Newsletter MCP, read-only V1, paid plans |
| Beehiiv MCP integration guide | https://www.buildmvpfast.com/blog/beehiiv-mcp-newsletter-ai-agent-integration-2026 | MCP usage patterns |
| Kit vs Beehiiv 2026 | https://www.knockedupmoney.com/blog/convertkit-vs-beehiiv-whats-the-best-newsletter-platform | Newsletter platform choice (Beehiiv default for media product, Kit for courses+automation) |
| Beehiiv vs Substack vs Ghost monetisation | https://earnifyhub.com/blog/blogging/beehiiv-vs-substack-vs-ghost-monetisation.php | Substack/Ghost positioning |
| Ghost Content API | https://ghost.org/vs/beehiiv/ + Pipedream Ghost docs | Programmatic publishing API |
| Riverside vs Descript 2026 | https://speakwiseapp.com/blog/descript-vs-riverside | Recording vs editing distinction, Descript API |
| Cleanvoice — 10 podcast APIs 2026 | https://cleanvoice.ai/blog/best-podcast-api/ | Podcast hosting/analytics API survey |
| Riverside API review | https://cleanvoice.ai/blog/riverside-api-review/ | Riverside Business plan API, no editing operations |
| Castmagic — Best AI repurposing 2026 | https://stormy.ai/blog/best-gpt-repurposing-tools-2026-opusclip-munch-castmagic | Castmagic MCP for Claude |
| OpusClip vs Munch vs Castmagic | https://www.blotato.com/blog/ai-content-repurposing-tools | Repurposing pipeline tools |
| Submagic — viral captions | https://www.submagic.co/ | 99% caption accuracy, B-roll auto-edit, API on Business+ plan |
| Headliner audiograms | https://www.headliner.app/ | Automatic audiograms from RSS feeds |
| Podcast audiogram tools 2026 | https://www.thepodosphere.com/blog/podcast-audiogram-tools-2026 | Audiogram landscape |
| Best podcast hosting 2026 | https://www.thepodosphere.com/blog/best-podcast-hosting-platforms-2026-comparison-guide | Buzzsprout / Transistor / Captivate positioning |
| Podchaser API vs Listen Notes API | https://www.podchaser.com/articles/api/podchaser-api-vs-listen-notes-api | Podcast intelligence/discovery APIs |
| Podcast SEO tools 2026 | https://www.thespearpoint.com/blog/seo-for-podcasts | Chapter SEO, Google Key Moments |
| Typefully agent CLI | https://typefully.com/x-twitter | Thread writing + cross-publish to X/LinkedIn/Threads/Bluesky/Mastodon via npx typefully |
| LinkedIn carousel engagement | https://www.supergrow.ai/blog/linkedin-carousel-generators | 1.6× engagement vs text, 6.6% avg vs 1.11% |
| Postiv / Carosello / Taplio | https://contentin.io/blog/best-linkedin-carousel-generators/ | LinkedIn carousel SOTA tools |
| Notion content calendar + API | https://espressio.ai/blog/claude-notion-content-calendar | Notion MCP for editorial DB |
| Notion editorial calendar template | https://www.notion.com/templates/editorial-calendar | Reference template for the DB |
| Patreon developer portal | https://www.patreon.com/portal | Patreon API v2 (v1 deprecated) |
| Memberstack content monetization | https://www.memberstack.com/webflow-templates/content-monetization-template | Patreon alternative (96% creator take) |
| Circle community + API | https://circle.so/blog/best-membership-platforms | Community + monetization API |
| Otter / Whisper / Granola | https://guptadeepak.com/tools/top-5-ai-transcription-tools-2026/ | Transcription SOTA |
| OpenAI Whisper API | https://platform.openai.com/docs/api-reference/audio | Whisper foundation for SOTA tools |
| Otter podcast transcription | https://otter.ai/podcast-transcription | Otter MCP / Chat for show notes |
| Mintlify 2026 features | https://www.mintlify.com/library/best-technical-documentation-software-in-2026 | .md content support, OpenAPI |
| Buffer GraphQL + MCP | https://mcpmarket.com/server/buffer | Cross-platform publishing cascade |
| YouTube Data API v3 (videos.insert quota reduced 1600→100) | https://zernio.com/blog/youtube-upload-api | Video upload + scheduling for podcast clips |
| YouTube API pricing 2026 | https://www.blotato.com/blog/youtube-api-pricing | Free tier, 100 videos/day |
| Piktochart / Canva / Adobe Express infographics | https://washingtoncitypaper.com/article/782752/top-infographic-generators-in-2026/ | Infographic generation pathway |
| ConvertKit / Kit automation | https://www.sequenzy.com/blog/best-newsletter-platforms | Kit for course creators + advanced automation |

## Sources considered but not downloaded

- **wshobson/agents, VoltAgent, msitarzewski, vijaythecoder** — none have a clean `content-creator` archetype that covers newsletter + podcast + repurposing pipeline at once. The closest hits live under msitarzewski's "marketing-content-creator" and "podcast-strategist" roles, but the v1 build leans on the marketing-agent's already-research-grounded SOURCES.md plus fresh 2026 web research for content-specific tools (Beehiiv MCP, Castmagic MCP, Typefully agent CLI, Riverside/Descript API).
- **anthropics/skills** — no podcast/newsletter-specific skills shipped as of June 2026; `doc-coauthoring` covers long-form writing fundamentals (reused via the `marketing-agent` siblings).

## Future tightening

- Add `reference/agents/msitarzewski-marketing-content-creator.md` (full verbatim) on next pass.
- Add `reference/agents/wshobson-content-marketer.md` (if found in their content-marketing plugin).
- Add `reference/skills/` mirror of any SKILL.md from the marketing-skills bundle that's content-format-specific (long-form, podcast, UGC).
- Re-pull Beehiiv MCP V2 launch notes when write capabilities ship (V1 is read-only as of March 2026; write is committed for V2).
