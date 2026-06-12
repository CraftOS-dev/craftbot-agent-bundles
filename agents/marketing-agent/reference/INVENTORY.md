# Marketing Agent (general) — Reference Inventory

8 SOTA reference agents covering the full marketing surface: content, SEO, social, email, growth, brand voice. **No bundled skills** for this agent — wshobson's `plugins/content-marketing/skills/` returned 404, msitarzewski has agents not skills, and Anthropic skills don't include marketing yet.

## Reference Agents (8 files)

| File | Source | Status |
|---|---|---|
| `agents/voltagent-content-marketer.md` | [VoltAgent/categories/08-business-product/content-marketer.md](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/content-marketer.md) — **CORE**: content strategy, SEO, social, email, lead gen, campaign management, analytics, brand building | full |
| `agents/voltagent-growth-loops.md` | [VoltAgent/categories/08-business-product/growth-loops.md](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/growth-loops.md) — funnels vs loops, 5 loop types, loop design process, viral coefficient | full |
| `agents/voltagent-content-quality-editor.md` | [VoltAgent/categories/08-business-product/content-quality-editor.md](https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/content-quality-editor.md) — AI-slop removal via `unslop` CLI, voice preservation | **summary** |
| `agents/msitarzewski-content-creator.md` | [msitarzewski/marketing/marketing-content-creator.md](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-content-creator.md) — multi-format strategy, brand storytelling, video, podcasts, success metrics | full |
| `agents/msitarzewski-growth-hacker.md` | [msitarzewski/marketing/marketing-growth-hacker.md](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-growth-hacker.md) — funnel optimization, viral mechanics, CAC/LTV, PLG, North Star, cohort | full |
| `agents/msitarzewski-seo-specialist.md` | [msitarzewski/marketing/marketing-seo-specialist.md](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-seo-specialist.md) — **RICHEST single file**: technical SEO, E-E-A-T, Core Web Vitals, **cannibalization audit** (SOTA), keyword strategy, on-page checklist, link building, AI search adaptation | full |
| `agents/msitarzewski-social-media-strategist.md` | [msitarzewski/marketing/marketing-social-media-strategist.md](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-social-media-strategist.md) — LinkedIn + Twitter cross-platform, B2B social selling, thought leadership, campaign frameworks | full |
| `agents/msitarzewski-email-strategist.md` | [msitarzewski/marketing/marketing-email-strategist.md](https://github.com/msitarzewski/agency-agents/blob/main/marketing/marketing-email-strategist.md) — **RICHEST single file**: lifecycle sequences, deliverability (SPF/DKIM/DMARC), post-Apple MPP measurement, 2024-2025 Google/Yahoo/Microsoft compliance, segmentation, GDPR, sequence/audit templates | full |

## Sources Considered But Not Downloaded

| Source | Why excluded |
|---|---|
| wshobson `plugins/content-marketing/skills/` | 404 on the API list — directory does not exist as expected |
| msitarzewski platform-specialist agents (tiktok-strategist, instagram-curator, linkedin-content-creator, douyin, weibo, twitter-engager, etc.) | Each is a thin slice of the general marketing agent. Better suited as separate specialist agents in v1 |
| msitarzewski regional agents (china-ecommerce-operator, baidu-seo-specialist, bilibili-content-strategist, wechat-official-account, xiaohongshu-specialist) | Region-specific; general marketing agent stays geography-neutral |
| msitarzewski PR/communications-manager | Adjacent (PR is its own discipline); specialist for v1 |
| wshobson plugins/social-publishing, /brand-landingpage, /seo-* | Plugins exist but adding more would duplicate the angles already covered |
| Anthropic skills | No marketing skills in their catalog yet (design/document/content only) |
| claudepro-directory | Tree not browseable at expected paths |
