# pr-comms — Reference Inventory

This agent's authoritative SOTA research lives at `reference/SOTA_USE_CASES.md`. Upstream agent definitions were not downloaded in the v1 build pass — the SOTA mapping was derived from web research (URLs cited in `SOTA_USE_CASES.md` and `SOURCES.md`).

The agent is adjacent to `agent_bundle/agents/marketing-agent/`, which we mirrored for structure and quality bar. Where the marketing agent owns publishing/SEO/ads/email/growth, this agent owns the earned-media surface: journalists, press releases, crisis comms, awards, podcast tours, analyst relations, AEO citation share, exec thought leadership, and brand-mention reputation work.

## Sibling agents already in the catalog (referenced for hand-off)

| Slug | What we defer to them for |
|---|---|
| `marketing-agent` | Broad marketing strategy, paid ads, SEO content, growth loops |
| `ceo-agent` | Exec voice on crisis statements + board/investor crisis decisions |
| `customer-support-agent` | Customer-facing incident communication during outages/breaches |
| `investor-relations` | Reg-FD disclosure, SEC 8-K, analyst earnings prep |
| `social-media-manager` | Day-to-day organic social scheduling and engagement |
| `content-creator` | Long-form blog/video content production |

## Sources used for SOTA research

See `reference/SOTA_USE_CASES.md` for the full per-use-case source URLs. Key research clusters:

- **Media databases**: Muck Rack (API + Media List Agent), Cision (CisionOne), Roxhill, Meltwater
- **Wire services**: PR Newswire/Cision, Business Wire, GlobeNewswire/Notified, eReleases
- **SME platforms**: Featured.com (revived HARO), Qwoted, Source of Sources, JustReachOut
- **PR workflow software**: Prowly, Prezly, Notified, PressFriendly
- **Reputation monitoring**: Brand24, Brandwatch, Meltwater, Mention.com, Awario
- **AI search citation tracking**: AthenaHQ, Profound, Otterly.ai
- **AI pitch personalization**: Smartlead, Lemlist, Instantly (deliverability infra), Claude API direct
- **Podcast booking**: PodPitch, Podchaser Pro, MatchMaker.fm, Podseeker
- **Thought leadership**: LinkedIn Marketing API, Substack API, X v2 API
- **Crisis comms**: 5W PR predictive AI playbooks, Gutenberg AI rapid response, PR.co playbook
- **Analyst relations**: Gartner Magic Quadrant briefing process, Spotlight AR, ARchitect
- **Awards lists**: Inc 5000, Forbes 30 Under 30, Fast Company Most Innovative, G2 reports
- **Speaking submissions**: Sessionize, Papercall.io, Pretalx, Call4Papers

## For future tightening

Pull 4-6 reference agents into `reference/agents/`:
- VoltAgent `categories/08-business-product/pr-specialist.md` (if it ships)
- wshobson `plugins/pr-communications/agents/` (if it ships)
- msitarzewski `marketing/marketing-pr-communications-manager.md`
- agency-agents crisis-comms agent

Pull 6-10 reference skills into `reference/skills/`:
- press-release SKILL pack from wshobson plugins
- media-list SKILL pack from any catalog that ships one
- HARO/Featured/Qwoted SKILL packs
