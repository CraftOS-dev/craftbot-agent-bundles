# Knowledge Base Manager — Source Attribution

This file maps every section of `soul.md` and `role.md` back to its source (research URL or upstream reference file). It is part of the bundle but is **not** loaded into the agent's context — it exists for human verification and future updates.

Per the v1 build pass, upstream agent definitions were not downloaded into `reference/agents/`. Sourcing here is the SOTA-research URL set captured in `reference/SOTA_USE_CASES.md` plus the Diátaxis / Information Architecture / NN/g card-sorting canonical references. The technical-writer parent agent's reference set may be re-used in a future tightening pass.

---

## soul.md → source map

| Section in soul.md | Source(s) | Notes |
|---|---|---|
| Title + action-verb persona intro | `reference/SOTA_USE_CASES.md` (every verb → bundled skill pack mapping) | Verbs paired with concrete artifact + skill/MCP per methodology rule |
| Purpose | `reference/SOTA_USE_CASES.md` + role-brief framing | KB-as-product framing |
| Execution stack | `reference/SOTA_USE_CASES.md` (bundled skill packs section) | 18 bullet headliners selected from 24 bundled packs |
| When invoked — Taxonomy / IA design | NN/g card-sort + Diátaxis + OptimalSort TreeJack | https://www.nngroup.com/articles/card-sorting-definitive-guide/ + https://diataxis.fr/ |
| When invoked — Search optimization | Algolia DocSearch + Typesense docs | https://docsearch.algolia.com/ + https://typesense.org/ |
| When invoked — Content lifecycle | Notion DB property + automation docs; Confluence Page Approvals | https://developers.notion.com/ + https://developer.atlassian.com/cloud/confluence/rest/v2/ |
| When invoked — Doc analytics | Algolia Insights + Microsoft Clarity Data Export API + GA4 Data API | https://www.algolia.com/doc/rest-api/analytics/ + https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api |
| When invoked — ROI / deflection | Intercom + Zendesk Help Center reporting | https://www.intercom.com/help/en/articles/3539921-help-center-reporting + https://developer.zendesk.com/api-reference/help_center/help-center-api/articles/ |
| When invoked — KB migration | notion-to-md + confluence-to-markdown + Zendesk articles API | https://www.npmjs.com/package/notion-to-md + https://github.com/meridius/confluence-to-markdown |
| When invoked — AI doc assistant | Kapa + Inkeep + Mendable + Markprompt docs | https://docs.kapa.ai/ + https://docs.inkeep.com/ + https://docs.mendable.ai/ + https://markprompt.com/docs |
| When invoked — Multi-language localization | DeepL API + Crowdin API + Lokalise CLI | https://developers.deepl.com/ + https://developer.crowdin.com/ + https://docs.lokalise.com/ |
| When invoked — Content audit | Lychee + pytest-markdown-docs + simhash | https://github.com/lycheeverse/lychee + https://github.com/modal-labs/pytest-markdown-docs + https://pypi.org/project/simhash/ |
| When invoked — Authoring training | Write the Docs style-guide patterns + Vale | https://www.writethedocs.org/guide/writing/style-guides/ + https://vale.sh/ |
| Core operating rules | Synthesis from SOTA research + role-brief convictions | Mirrors the 3 load-bearing convictions in the persona intro |
| Mode-specific decisions | Per-mode SOTA research in `reference/SOTA_USE_CASES.md` | One row per mode |
| Quality gates | Composed from per-SOTA-tool eval criteria + KB best-practice common wisdom | Each gate is observable / verifiable |
| Output format | Common KB-platform conventions (Docusaurus / MkDocs / Mintlify / Astro) | Frontmatter + sidebars + redirect-map shape |
| Communication style | Authored synthesis | Mirrors `technical-writer` style; voice tuned to KB-operator analytics-driven communication |
| When to push back | Authored synthesis | Operational glue derived from antipattern catalog (role.md) |
| When to defer | Authored synthesis | Sibling-agent hand-offs explicit by slug |
| PROACTIVE self-init footer | `agent_bundle/METHODOLOGY.md` standard wording | Same wording across all agents; 3 role-specific questions adapted to KB |
| Closing rule | Restates the three load-bearing convictions | KB-as-product framing |

---

## role.md → source map

| Section in role.md | Source(s) | Notes |
|---|---|---|
| Capability reference — KB platforms (customer-facing) | Intercom / Zendesk / Salesforce / HubSpot / Help Scout / FreshDesk / Pylon / ProProfs docs | Standard vendor surveys |
| Capability reference — KB platforms (employee-facing) | Notion / Confluence / GitBook / Slab / Tettra / Document360 / Helpjuice / Bloomfire / Stack Overflow for Teams / Coda / Slite / Almanac docs | Standard vendor surveys |
| Capability reference — Search platforms | Algolia DocSearch + Typesense + MeiliSearch + Pagefind + Orama docs | https://docsearch.algolia.com/ + https://typesense.org/ + https://www.meilisearch.com/ + https://pagefind.app/ + https://oramasearch.com/ |
| Capability reference — Search analytics | Algolia Insights + Mintlify Analytics + GA4 + Microsoft Clarity | https://www.algolia.com/doc/rest-api/analytics/ + https://learn.microsoft.com/en-us/clarity/ |
| Capability reference — AI doc Q&A | Kapa / Inkeep / Mendable / Markprompt + Notion AI + Confluence AI (Rovo) docs | Standard vendor surveys |
| Capability reference — Process / video docs | Loom / Tango / Scribe / Guidde docs | Standard vendor surveys |
| Capability reference — Interactive guides | Stonly / Whatfix / Pendo Guides / Shepherd.js docs | https://stonly.com/ + https://docs.whatfix.com/ + https://shepherdjs.dev/ |
| Capability reference — Changelog tools | Beamer / Headway / LaunchNotes docs + feedgen Python | https://www.getbeamer.com/ + https://docs.headwayapp.co/ + https://www.launchnotes.com/ |
| Capability reference — Versioning | Docusaurus versioning + mike + Mintlify versions + sphinx-multiversion | https://docusaurus.io/docs/versioning + https://github.com/jimporter/mike |
| Capability reference — Content reuse | AsciiDoc + Antora + Docusaurus MDX + Mintlify Snippets + Astro Starlight content collections | https://docs.antora.org/ + https://mintlify.com/docs/reusable-snippets |
| Capability reference — Localization | DeepL + Crowdin + Lokalise + Argos Translate docs | https://developers.deepl.com/ + https://developer.crowdin.com/ |
| Capability reference — Diátaxis taxonomy | Diátaxis framework | https://diataxis.fr/ |
| Taxonomy design playbook | NN/g card-sorting + OptimalSort TreeJack + Diátaxis framework | https://www.nngroup.com/articles/card-sorting-definitive-guide/ + https://www.optimalworkshop.com/treejack |
| Search optimization playbook | Algolia synonyms / ranking docs + Typesense synonyms collection | https://www.algolia.com/doc/api-client/methods/synonyms/ + https://typesense.org/docs/0.25.2/api/synonyms.html |
| Content lifecycle playbook | Notion automation + Confluence Page Approvals + GitHub stale-bot Action | https://github.com/actions/stale |
| Doc analytics playbook | Algolia Insights + Clarity Data Export API + GA4 Data API | per-tool docs |
| Deflection rate playbook | Intercom + Zendesk webhook docs + per-account deflection formula | https://www.intercom.com/help/en/articles/3539921-help-center-reporting |
| Content audit playbook | Lychee + pytest-markdown-docs + simhash | per-tool docs |
| Migration playbook | notion-to-md + confluence-to-markdown + turndown / markdownify | https://www.npmjs.com/package/notion-to-md + https://github.com/meridius/confluence-to-markdown |
| AI doc assistant playbook | Kapa / Inkeep / Mendable / Markprompt eval-guide patterns | https://docs.kapa.ai/eval |
| Multi-language playbook | DeepL + Crowdin + Lokalise + Docusaurus i18n + Astro Starlight locales | per-tool docs |
| Antipattern catalog | Authored synthesis of common KB failure modes from the SOTA research + NN/g IA antipatterns | Each pair shows BAD / GOOD with rationale |
| KB taxonomy templates | Diátaxis applied to B2B SaaS + Notion internal-wiki conventions + Docusaurus per-version layout | Composed templates |
| Redirect map template | Netlify `_redirects` syntax + Vercel `vercel.json` redirects | https://docs.netlify.com/routing/redirects/ + https://vercel.com/docs/edge-network/redirects |
| Stale-bot workflow template | GitHub Actions schedule trigger + actions/stale + Slack incoming webhook | https://github.com/actions/stale + https://api.slack.com/messaging/webhooks |
| SOTA tool reference (June 2026) | One H3 per SOTA tool with install + skill-pack pointer; derived from `reference/SOTA_USE_CASES.md` | grep-friendly per-tool reference |
| SOTA execution playbook | One row per user-request → first-stop skill pack; derived from `reference/SOTA_USE_CASES.md` | Routing table for the agent |
| Closing rules | Restates the three load-bearing convictions | KB-as-product framing |

---

## Notes on "authored from synthesis"

Small sections were composed locally rather than lifted verbatim from a single source:

- **Core operating rules (15 bullets in soul.md)** — synthesis of SOTA-tool best-practices into one-line agent-firable rules. Each bullet maps to a concrete SOTA mechanism documented in `reference/SOTA_USE_CASES.md`.
- **Mode-specific decisions** — synthesis. Each mode pulls from the matching SOTA playbook section in role.md.
- **Antipattern catalog (10 pairs in role.md)** — synthesis of common KB failure modes encountered across the SOTA research. Each pair is grounded in a SOTA convention (Diátaxis non-mixing, archive ≠ delete, SSO over ACLs, etc.).
- **KB taxonomy templates** (3 templates in role.md) — composed templates applying Diátaxis to common KB shapes (customer SaaS, internal company wiki, developer-facing versioned KB).
- **First-conversation routine questions** — adapted from the standard PROACTIVE.md self-init pattern (METHODOLOGY.md standard footer). The three role-specific questions cover platform, audience, and biggest pain.

These are operational glue and SOTA-research-informed synthesis, not standalone domain claims that lack a source.

---

## SOTA tool sources (June 2026)

> One row per SOTA tool referenced in `role.md → SOTA tool reference` and the bundled skill packs.

| Tool / framework | Source URL | Used in |
|---|---|---|
| Algolia DocSearch | https://docsearch.algolia.com/ | `skills/algolia-typesense-search-optimization/` |
| Algolia Analytics / Insights API | https://www.algolia.com/doc/rest-api/analytics/ | `skills/doc-analytics-clarity-ga4-algolia-insights/` |
| Algolia synonyms API | https://www.algolia.com/doc/api-client/methods/synonyms/ | `skills/algolia-typesense-search-optimization/` |
| Typesense synonyms | https://typesense.org/docs/0.25.2/api/synonyms.html | `skills/algolia-typesense-search-optimization/` |
| Typesense | https://typesense.org/ | `skills/algolia-typesense-search-optimization/` |
| MeiliSearch | https://www.meilisearch.com/ | `skills/algolia-typesense-search-optimization/` |
| Pagefind | https://pagefind.app/ | `skills/algolia-typesense-search-optimization/` |
| Orama | https://oramasearch.com/ | `skills/algolia-typesense-search-optimization/` |
| Microsoft Clarity | https://clarity.microsoft.com/ | `skills/doc-analytics-clarity-ga4-algolia-insights/` |
| Clarity Data Export API | https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api | `skills/doc-analytics-clarity-ga4-algolia-insights/` |
| Clarity MCP server | https://learn.microsoft.com/en-us/clarity/third-party-integrations/clarity-mcp-server | `skills/doc-analytics-clarity-ga4-algolia-insights/` |
| GA4 Data API | https://developers.google.com/analytics/devguides/reporting/data/v1 | `skills/doc-analytics-clarity-ga4-algolia-insights/` |
| google-analytics-data (PyPI) | https://pypi.org/project/google-analytics-data/ | `skills/doc-analytics-clarity-ga4-algolia-insights/` |
| Mintlify Analytics | https://mintlify.com/docs/analytics | `skills/doc-analytics-clarity-ga4-algolia-insights/` |
| Kapa.ai | https://docs.kapa.ai/ | `skills/ai-doc-assistant-kapa-inkeep-mendable/` |
| Inkeep | https://docs.inkeep.com/ | `skills/ai-doc-assistant-kapa-inkeep-mendable/` |
| Mendable | https://docs.mendable.ai/ | `skills/ai-doc-assistant-kapa-inkeep-mendable/` |
| Markprompt | https://markprompt.com/docs | `skills/ai-doc-assistant-kapa-inkeep-mendable/` |
| Notion API | https://developers.notion.com/ | `skills/employee-facing-internal-wiki-notion-slab/`, `skills/content-lifecycle-draft-review-publish-archive/` |
| Confluence REST API v2 | https://developer.atlassian.com/cloud/confluence/rest/v2/ | `skills/employee-facing-internal-wiki-notion-slab/`, `skills/content-lifecycle-draft-review-publish-archive/` |
| Document360 workflows | https://docs.document360.com/docs/workflows | `skills/content-lifecycle-draft-review-publish-archive/` |
| Slab Team Owner | https://help.slab.com/en/ | `skills/employee-facing-internal-wiki-notion-slab/` |
| Tettra | https://tettra.com/ | `skills/employee-facing-internal-wiki-notion-slab/` |
| Guru | https://app.getguru.com/api/v1/docs | `skills/employee-facing-internal-wiki-notion-slab/` |
| Intercom Articles | https://www.intercom.com/help/en/articles/2398029-articles | `skills/customer-facing-kb-support-deflection/` |
| Intercom Help Center reporting | https://www.intercom.com/help/en/articles/3539921-help-center-reporting | `skills/kb-roi-deflection-rate/` |
| Zendesk Help Center API | https://developer.zendesk.com/api-reference/help_center/help-center-api/articles/ | `skills/customer-facing-kb-support-deflection/`, `skills/kb-roi-deflection-rate/` |
| Pylon docs | https://docs.pylon.com/ | `skills/customer-facing-kb-support-deflection/` |
| Help Scout Docs | https://help.helpscout.com/hc/en-us/articles/115001596571 | `skills/customer-facing-kb-support-deflection/` |
| Salesforce REST API | https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/ | `skills/kb-roi-deflection-rate/` (KB-to-CRM section) |
| HubSpot CRM Properties API | https://developers.hubspot.com/docs/api/crm/properties | `skills/kb-roi-deflection-rate/` |
| Diátaxis framework | https://diataxis.fr/ | `skills/kb-taxonomy-design-categories-tags-hierarchy/`, `skills/kb-governance-style-vale-rules/` |
| NN/g card sorting | https://www.nngroup.com/articles/card-sorting-definitive-guide/ | `skills/kb-taxonomy-design-categories-tags-hierarchy/` |
| OptimalSort TreeJack | https://www.optimalworkshop.com/treejack | `skills/kb-taxonomy-design-categories-tags-hierarchy/` |
| Vale | https://vale.sh/ | `skills/kb-governance-style-vale-rules/` |
| Vale styles | https://vale.sh/docs/topics/styles/ | `skills/kb-governance-style-vale-rules/` |
| markdownlint | https://www.markdownguide.org/tools/markdownlint/ | `skills/kb-governance-style-vale-rules/` |
| alex (inclusive language) | https://github.com/get-alex/alex | `skills/kb-governance-style-vale-rules/` |
| Lychee | https://github.com/lycheeverse/lychee | `skills/content-audit-stale-inaccurate-redundant/` |
| pytest-markdown-docs (Modal) | https://github.com/modal-labs/pytest-markdown-docs | `skills/content-audit-stale-inaccurate-redundant/` |
| simhash | https://pypi.org/project/simhash/ | `skills/content-audit-stale-inaccurate-redundant/` |
| datasketch | https://github.com/ekzhu/datasketch | `skills/content-audit-stale-inaccurate-redundant/` |
| notion-to-md | https://www.npmjs.com/package/notion-to-md | `skills/content-migration-between-platforms/` |
| confluence-to-markdown | https://github.com/meridius/confluence-to-markdown | `skills/content-migration-between-platforms/` |
| turndown | https://github.com/mixmark-io/turndown | `skills/content-migration-between-platforms/` |
| markdownify (Python) | https://github.com/matthewwithanm/python-markdownify | `skills/content-migration-between-platforms/` |
| Schema.org Article | https://schema.org/Article | `skills/kb-seo-aeo-geo-public-ranking/` |
| Schema.org FAQPage | https://schema.org/FAQPage | `skills/kb-seo-aeo-geo-public-ranking/` |
| Schema.org HowTo | https://schema.org/HowTo | `skills/kb-seo-aeo-geo-public-ranking/` |
| llms.txt standard | https://llmstxt.org/ | `skills/kb-seo-aeo-geo-public-ranking/` |
| Ahrefs API | https://ahrefs.com/api | `skills/kb-seo-aeo-geo-public-ranking/` |
| AthenaHQ | https://docs.athenahq.ai/ | `skills/kb-seo-aeo-geo-public-ranking/` |
| DeepL API | https://developers.deepl.com/ | `skills/multi-language-localized-kb-deepl-crowdin/` |
| Crowdin API | https://developer.crowdin.com/ | `skills/multi-language-localized-kb-deepl-crowdin/` |
| Lokalise CLI | https://github.com/lokalise/lokalise-cli-2-go | `skills/multi-language-localized-kb-deepl-crowdin/` |
| Lokalise docs | https://docs.lokalise.com/ | `skills/multi-language-localized-kb-deepl-crowdin/` |
| Argos Translate | https://www.argosopentech.com/ | `skills/multi-language-localized-kb-deepl-crowdin/` |
| Okta developer (SAML/OIDC) | https://developer.okta.com/docs/concepts/saml/ | `skills/sso-gated-kb-okta-auth0/` |
| Auth0 SAML | https://auth0.com/docs/authenticate/protocols/saml | `skills/sso-gated-kb-okta-auth0/` |
| SCIM 2.0 spec | https://scim.cloud/ | `skills/sso-gated-kb-okta-auth0/` |
| Docusaurus versioning | https://docusaurus.io/docs/versioning | `skills/kb-versioning-per-product-docusaurus-mike/` |
| mike (MkDocs) | https://github.com/jimporter/mike | `skills/kb-versioning-per-product-docusaurus-mike/` |
| sphinx-multiversion | https://github.com/Holzhaus/sphinx-multiversion | `skills/kb-versioning-per-product-docusaurus-mike/` |
| Antora | https://docs.antora.org/antora/latest/ | `skills/content-reuse-single-source-asciidoc-antora/` |
| Mintlify Snippets | https://mintlify.com/docs/reusable-snippets | `skills/content-reuse-single-source-asciidoc-antora/` |
| Mintlify Feedback | https://mintlify.com/docs/settings/ai/feedback | `skills/kb-feedback-collection-helpful-open/` |
| Document360 article feedback | https://docs.document360.com/docs/article-feedback | `skills/kb-feedback-collection-helpful-open/` |
| Cloudflare Workers | https://developers.cloudflare.com/workers/ | `skills/kb-feedback-collection-helpful-open/` |
| GitHub Actions schedule | https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule | `skills/content-review-cadence-monthly-quarterly/` |
| actions/stale | https://github.com/actions/stale | `skills/content-review-cadence-monthly-quarterly/` |
| Stonly API | https://stonly.com/help/en/category/api-1hjhf32/ | `skills/interactive-guide-stonly-whatfix/` |
| Whatfix docs | https://docs.whatfix.com/ | `skills/interactive-guide-stonly-whatfix/` |
| Shepherd.js | https://shepherdjs.dev/ | `skills/interactive-guide-stonly-whatfix/` |
| Loom developers | https://loom.com/developers | `skills/video-kb-loom-tango-scribe/` |
| Tango API | https://www.tango.us/api | `skills/video-kb-loom-tango-scribe/` |
| Scribe API | https://scribehow.com/api | `skills/video-kb-loom-tango-scribe/` |
| Beamer API | https://www.getbeamer.com/help/en/articles/3438037-api | `skills/changelog-beamer-headway-inproduct/` |
| Headway API | https://docs.headwayapp.co/ | `skills/changelog-beamer-headway-inproduct/` |
| LaunchNotes API | https://www.launchnotes.com/api-docs | `skills/changelog-beamer-headway-inproduct/` |
| feedgen (Python) | https://pypi.org/project/feedgen/ | `skills/changelog-beamer-headway-inproduct/` |
| Stack Overflow for Teams | https://stackoverflowteams.com/ | `skills/expert-finder-who-knows-x/` |
| Glean expert finder | https://www.glean.com/product/expert-finder | `skills/expert-finder-who-knows-x/` |
| Notion databases intro | https://www.notion.com/help/intro-to-databases | `skills/expert-finder-who-knows-x/`, `skills/knowledge-ops-owner-contributor-flow/` |
| Write the Docs style guides | https://www.writethedocs.org/guide/writing/style-guides/ | `skills/kb-authoring-training-non-doc-team/`, `skills/kb-governance-style-vale-rules/` |
| Atlassian RACI guide | https://www.atlassian.com/work-management/project-management/raci-chart | `skills/knowledge-ops-owner-contributor-flow/` |
| GitHub CODEOWNERS | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners | `skills/knowledge-ops-owner-contributor-flow/` |
| Netlify _redirects | https://docs.netlify.com/routing/redirects/ | `skills/content-migration-between-platforms/` (redirect map) |
| Vercel redirects | https://vercel.com/docs/edge-network/redirects | `skills/content-migration-between-platforms/` (redirect map) |
| Slack incoming webhooks | https://api.slack.com/messaging/webhooks | `skills/content-review-cadence-monthly-quarterly/` |

These sources informed the `SOTA tool reference (June 2026)` section in `role.md`, the per-use-case mapping in `reference/SOTA_USE_CASES.md`, and will inform the bundled SOTA skill packs in Round 2.

---

## Refreshing from upstream

When SOTA tools change (new launch, deprecated API, pricing model change):

1. Update the relevant skill pack(s) in `skills/<name>/SKILL.md` (Round 2).
2. Update the SOTA sources table above.
3. Update `reference/SOTA_USE_CASES.md` confidence ratings if applicable.
4. Re-run `python verify.py knowledge-base-manager` to confirm structure intact.
5. Re-build: `python build.py knowledge-base-manager` produces a fresh `.craftbot`.

For the canonical reference repos (when downloaded in a future tightening pass):
- `wshobson/agents` — repull every quarter (search `content-strategist`, `documentation-engineer`, `support-engineer`).
- `VoltAgent/awesome-claude-code-subagents` — same cadence.
- `msitarzewski/agency-agents` — same cadence.
- Anthropic skills repo — check for new doc-related skills.
