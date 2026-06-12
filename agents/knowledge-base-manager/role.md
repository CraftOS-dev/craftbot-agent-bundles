# Knowledge Base Manager — deep reference

This appends to `AGENT.md`. It is **not** in the agent's default context. Grep it when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Taxonomy design playbook", "Search optimization playbook", "Content lifecycle playbook", "Doc analytics playbook", "Deflection rate playbook", "Content audit playbook", "Migration playbook", "AI doc assistant playbook", "Multi-language playbook", "Antipattern catalog", "SOTA tool reference", "SOTA execution playbook", "KB taxonomy templates", "Redirect map template", "Stale-bot workflow template", "Deflection report template".

For provenance of any section, see `SOURCES.md` in this bundle.

---

## Capability reference

Factual reference — tools, frameworks, taxonomy patterns. SOUL.md does not carry these (they don't drive turn-by-turn decisions); grep here when the user asks "what should I use for X?"

### KB platforms (customer-facing)

- **Intercom Articles** — in-product Help widget + KB; deflection-tracking native; paid
- **Zendesk Guide / Help Center** — mature; SCIM SSO; broad integrations
- **Salesforce Knowledge** — CRM-integrated; multi-channel; heavy enterprise
- **HubSpot Knowledge Base** — paired with HubSpot Service Hub; lighter weight
- **Help Scout Docs** — small-team support KB
- **FreshDesk KB** — alternative to Zendesk
- **Pylon Help Center** — modern B2B-support-focused KB
- **ProProfs Knowledge Base** — simpler small-business KB

### KB platforms (employee-facing / internal wiki)

- **Notion** — collaborative all-purpose; teamspaces; native MCP
- **Confluence (Atlassian)** — enterprise standard; Page Approvals app; SCIM
- **GitBook** — dev-leaning; git-sync
- **Slab** — Slack-native; "Team Owner"
- **Tettra** — Slack-native; lightweight
- **Document360** — self-serve focus; workflows + version control
- **Helpjuice** — KB-focused; analytics
- **Bloomfire** — enterprise expertise sharing
- **Stack Overflow for Teams** — Q&A-shaped KB
- **Coda** — docs + DB hybrid
- **Slite** — minimalist team wiki
- **Almanac** — async / async-doc workflow

### Search platforms

- **Algolia DocSearch** — free for OSS; paid for closed; Insights API for analytics
- **Typesense** — self-hosted; sub-50ms; synonyms collection
- **MeiliSearch** — self-hosted; typo-tolerant; fast indexing
- **Pagefind** — static-site search; zero infra; client-side
- **Orama** — full-text + vector + embeddings; FOSS + cloud tiers
- **Lucene / Elasticsearch** — enterprise full-text; heavyweight
- **Mintlify Search** — built into Mintlify; AI-augmented
- **Document360 Search** — built in; analytics

### Search analytics

- **Algolia Insights** — top-searched, no-result, CTR per page; native MCP via cli-anything curl
- **Mintlify Analytics** — native KB analytics for Mintlify sites
- **GA4** — sessions, exit rate, engaged time, content groupings
- **Microsoft Clarity** — free heatmaps, rage clicks, scroll depth, session replays

### AI doc Q&A platforms

- **Kapa.ai** — verified citations; used by OpenAI / Reddit / Mapbox; paid
- **Inkeep** — search-first + chat fallback; paid
- **Mendable** — SDK for product embedding; paid
- **Markprompt** — FOSS / self-hostable backbone
- **Notion AI** — Notion-native Q&A
- **Confluence AI (Rovo)** — Atlassian-native Q&A

### Doc analytics tooling

- **Mintlify Analytics** — built into Mintlify sites
- **Document360 Analytics** — search analytics + visit data
- **Bloomfire Analytics** — enterprise engagement metrics
- **Microsoft Clarity** — free behavioral / session replays
- **GA4 Data API** — programmatic queries

### Process / video docs

- **Loom** — narrated screencasts (5-10min); transcript API
- **Tango** — auto-generated step-by-step from browser captures
- **Scribe** — alternative to Tango
- **Guidde** — AI-narrated walkthroughs

### Interactive guides

- **Stonly** — decision-tree style step guides
- **Whatfix** — in-product Self-Help widget
- **Pendo Guides** — lighter, analytics-driven
- **Shepherd.js** — FOSS in-product tour library

### Changelog tools

- **Beamer** — in-product changelog widget
- **Headway** — alt in-product changelog
- **LaunchNotes** — segmented (admin / end-user / dev) changelog
- **RSS feed (feedgen)** — FOSS fallback

### Versioning tools

- **Docusaurus versions config** — `docusaurus docs:version 2.0`
- **mike (MkDocs)** — `mike deploy 2.0 latest`
- **Mintlify versions.json** — declarative
- **sphinx-multiversion** — Sphinx-based per-branch docs

### Content reuse / single-source

- **AsciiDoc + Antora** — DITA-style multi-output for enterprise KBs
- **Docusaurus MDX partials** — `@theme/MDXComponents`
- **Mintlify Snippets** — reusable blocks
- **Astro Starlight content collections** — `astro:content`

### Localization

- **DeepL Pro** — `tag_handling=markdown`; SOTA for technical content
- **Crowdin** — translator workflow + TM + glossary
- **Lokalise** — alt translation management
- **Argos Translate** — FOSS local-model alternative

### PKM (personal knowledge — out of scope for KB-as-product but relevant)

- **Roam Research** — bidirectional links
- **Logseq** — FOSS Roam clone
- **Obsidian** — local-first, plugin-rich
- **Foam** — VS Code based
- **Mem.ai** — AI-augmented
- **Reflect** — networked notes

### Diátaxis taxonomy (customer-facing KB overlay)

| Tier | Reader's question | Mode |
|---|---|---|
| Tutorial | "Teach me" | Learning-oriented |
| How-to | "How do I X?" | Task-oriented |
| Reference | "What does X do?" | Information-oriented |
| Explanation | "Why?" | Understanding-oriented |

Never mix tiers in one article.

### KB ownership patterns

- **CODEOWNERS-style** (git-backed) — `OWNERS.md` per folder
- **RACI matrix** (Notion db / Confluence properties) — per content area
- **Team Owner** (Slab feature) — top-level team-aligned
- **Notion teamspace owners** — Notion-native

### Quality signals (per article)

- **Last-modified** (auto)
- **Last-verified** (manual stamp; >90d → "verify before relying on" badge)
- **Owner** (named person)
- **Status** (Draft / In review / Published / Stale / Archived)
- **Helpful?** rating (binary + open feedback)
- **Views** (rolling 30d)
- **Search-discovery** rate (% of views from search vs nav)
- **Exit rate**
- **Deflection rate** (per category, not per article)

---

## Taxonomy design playbook

Step-by-step procedure for designing or restructuring KB IA.

1. **Gather signals.** Pull data from (a) support-ticket categories from last 90d, (b) Algolia / DocSearch no-result-found queries, (c) Microsoft Clarity rage-click URLs, (d) GA4 high-exit pages.
2. **Card-sort with users (or proxy via tickets).** 30-50 representative articles + 5-10 real users. Optimal Workshop OptimalSort. Output: 3-7 top-level groupings.
3. **Apply Diátaxis overlay** (customer-facing only). Top-level slices are Get-started / How-to / Concept / Reference / Troubleshooting.
4. **5-tier IA:** Domain (3-7) → Category (4-10 per domain) → Subcategory (4-12) → Article → Tag overlay (cross-cutting concerns like "billing", "enterprise", "v2", "mobile").
5. **First-click test.** TreeJack or Maze. Target: ≥80% find the right article on first click for top 20 use cases.
6. **Build sidebar mapping.** Mirror the taxonomy in `sidebars.js` (Docusaurus) / `nav` (MkDocs) / `docs.json` (Mintlify).
7. **Write redirect map** for every renamed section. Format: `redirects.json` (`{from: to}`) or platform-native (`_redirects` Netlify, `vercel.json` redirects).
8. **Ship taxonomy doc** — `docs/_taxonomy.md` capturing the rationale + tag glossary + section vocabulary.

### Concrete example: customer-facing KB for a B2B SaaS

```
Get-started/
  Quickstart/
  First integration/
  Account setup/
How-to/
  Authentication/
    Single sign-on (Okta)
    Single sign-on (Auth0)
    API keys
  Webhooks/
    Configure
    Verify signatures
    Retry strategy
  Billing/
    Update payment method
    Switch plans
    Cancel subscription
Concept/
  How auth works/
  How webhooks work/
  Rate limits/
Reference/
  API reference
  Webhook event types
  Error codes
Troubleshooting/
  Common auth errors/
  Webhooks not received/
  Billing failed/

Tags (cross-cutting): #v2, #enterprise, #mobile, #legacy
```

---

## Search optimization playbook

1. **Audit current state.** Pull top-100 search queries, no-result-found list, CTR per page, time-to-click.
2. **Pick platform.** Decision tree:
   - OSS docs site → Algolia DocSearch (free)
   - Self-hosted, small budget → Pagefind (static) or MeiliSearch
   - Self-hosted, scale → Typesense
   - Enterprise + vector → Orama or Algolia
   - Closed-source SaaS docs → Algolia paid or Typesense Cloud
3. **Configure ranking.** `title > h1 > description > content > tags`. Custom ranking on `last_modified` (recency) + `views` (popularity) + `helpful_pct` (quality).
4. **Load synonyms.** Build initial list from no-result-found terms. Algolia Rules API or Typesense `synonyms` collection. Example:
   ```json
   { "synonyms": [
     ["sso", "single sign on", "single-sign-on", "saml", "oidc"],
     ["webhook", "webhooks", "callback", "callbacks", "event subscription"],
     ["api key", "token", "bearer", "auth token"]
   ]}
   ```
5. **Autocomplete on top-50 queries** + popular categories.
6. **Federated search** if multiple products (one index per product, one search box).
7. **Wire Insights API** before declaring done. Top-searched + no-result + CTR feed the synonyms + content-roadmap loop.

### Synonyms file lifecycle

- Weekly: review no-result-found terms; add new synonyms; ship in CI.
- Monthly: prune synonyms that don't fire (zero hits).
- Quarterly: review CTR per page; demote low-CTR results in ranking.

---

## Content lifecycle playbook

1. **Define the 5 states.** Draft → In review → Published → Stale → Archived.
2. **Pick automation per platform:**
   - **Notion:** Status property (single-select) + Database automation (when status = "Stale", send Slack DM to Owner)
   - **Confluence:** Page Approvals app + Page Properties for status + Atlassian Automation
   - **Document360:** Workflows + version control
   - **Git-backed:** GitHub Actions stale-bot + frontmatter `status: published`
3. **Set owner per content area.** CODEOWNERS-style (`OWNERS.md`) or RACI db (Notion).
4. **Stale-bot rules.** Last-modified > 180d + last-verified > 90d → ping owner.
5. **Archive ≠ delete.** Hide from navigation but keep in search index with "Archived — verify before relying on" banner. Delete only after 12 months in archive.
6. **Per-release review.** Every product release ships with KB diff: which articles were edited, who owns the unchanged ones for that area, mandatory verify-stamp refresh.

### Concrete example: GitHub Actions stale-bot for git-backed KB

```yaml
# .github/workflows/stale-content.yml
name: Stale KB content
on:
  schedule:
    - cron: '0 9 * * 1'  # every Monday 9am UTC
jobs:
  stale-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Find stale articles
        run: |
          # find articles where last commit > 180d
          git log --pretty=format:"%ai %f" --name-only -- 'docs/**/*.md' \
            | awk '...' > stale.txt
      - name: Ping owners on Slack
        run: |
          for f in $(cat stale.txt); do
            owner=$(grep -h "$f" .github/OWNERS.md | awk '{print $2}')
            curl -X POST -H 'Content-Type: application/json' \
              -d "{\"text\":\"Stale: $f — owner $owner\"}" \
              "$SLACK_WEBHOOK"
          done
```

---

## Doc analytics playbook

Build the always-on report: **Write next** (top no-result + content gaps) and **Fix first** (high-exit + rage-click pages).

1. **Wire Algolia Insights** (free with DocSearch). Pull weekly: top-searched, no-result, CTR per page.
2. **Wire Microsoft Clarity** (free for unlimited sessions). Pull: rage clicks, dead clicks, scroll depth heatmaps, session replays for high-exit pages.
3. **Wire GA4 Data API** (free). Pull: sessions, exit rate, engaged time, content-grouping rollups.
4. **Optional: PostHog / Mixpanel / Amplitude** if recipient already uses one of these for product analytics — overlay KB events into the same warehouse.
5. **Cross-reference:**
   - Top no-result-found → content-gap roadmap (write these next)
   - High-exit + high-traffic → content-bug list (fix these first)
   - Top-searched terms not in any title → synonyms loop
6. **Output weekly report** as markdown + JSON (parseable for automation):

```markdown
# KB Analytics Weekly — 2026-W23

## Write next (top no-result-found)
| Query | Count | Suggested article | Owner |
|---|---|---|---|
| webhook retry strategy | 47 | How-to → Webhooks → Retry strategy | @alice |
| sso group sync | 38 | How-to → Authentication → SSO group sync | @bob |

## Fix first (high-exit + high-traffic)
| Article | Views (7d) | Exit rate | Rage clicks | Owner |
|---|---|---|---|---|
| Get-started / Quickstart | 8,420 | 76% | 14% | @alice |

## Search health
| Metric | Value | Δ vs last week |
|---|---|---|
| No-result rate | 8.2% | -1.4 pts |
| Avg CTR | 62% | +3 pts |
| Top-search coverage | 92% (46/50) | +2 |
```

---

## Deflection rate playbook

Definition: **Deflection rate per category = (article views with no follow-up support ticket within 24h) / total article views**.

1. **Wire KB view event** → analytics warehouse. Each view tagged with `kb_article_id`, `account_id` (via UTM or first-party cookie), `category`.
2. **Wire support-ticket open event** → same warehouse. Tagged with `account_id`, `category`, `timestamp`.
3. **Join.** For each KB view event, check whether the same `account_id` opened a ticket in the same `category` within 24h.
4. **Calculate per-category** (not per-article — too noisy). Per-category deflection × monthly views × support-cost-per-ticket = dollars saved.
5. **Surface in CRM.** Salesforce / HubSpot custom property "Self-Serve Health" on the account record.

### Deflection report template

```markdown
# Deflection — 2026-Q2

| Category | Views | Tickets (same category, 24h) | Deflection rate | Est. $ saved |
|---|---|---|---|---|
| Authentication | 12,400 | 480 | 96.1% | $59,520 |
| Billing | 8,200 | 690 | 91.6% | $37,560 |
| Webhooks | 4,800 | 510 | 89.4% | $21,450 |
| **Total** | **25,400** | **1,680** | **93.4%** | **$118,530** |

Assumes: support-cost-per-ticket = $50 (loaded). Adjust to your org.
```

---

## Content audit playbook

Three-axis audit:

### Axis 1: Stale

- Filter: last-modified > 180d AND last-verified > 90d.
- Action: ping owner; if owner unresponsive 14d, escalate to KB team for triage (update / archive / merge).

### Axis 2: Inaccurate

- **Broken links:** `lychee --format json docs/` → flag `failed` entries.
- **Failing code-fences:** `uvx pytest --markdown-docs docs/` → fix or remove failing examples.
- **Version mismatch:** parse `version:` frontmatter + check against current product version; flag mismatches.

### Axis 3: Redundant

- Use `simhash` or `datasketch.MinHash` to compute pairwise text similarity.
- Flag pairs with similarity > 80% → review for merge / redirect.
- Example Python:
  ```python
  from simhash import Simhash
  import pathlib

  articles = {p: Simhash(p.read_text().split()) for p in pathlib.Path('docs').rglob('*.md')}
  for a, ha in articles.items():
      for b, hb in articles.items():
          if a < b and ha.distance(hb) < 12:  # ~80% sim
              print(f"DUP: {a} <-> {b}")
  ```

### Audit output template

```markdown
# KB Audit — 2026-Q2

## Stale (47 articles)
| Article | Last modified | Last verified | Owner | Action |
|---|---|---|---|---|
| ... | 2025-09-01 | 2025-05-01 | @alice | update |

## Inaccurate (12 articles)
| Article | Issue | Action |
|---|---|---|
| how-to/webhooks/retry-strategy.md | 3 broken links | fix |
| concept/auth.md | code-fence fails on Python 3.13 | update |

## Redundant (5 pairs)
| A | B | Similarity | Action |
|---|---|---|---|
| how-to/sso.md | how-to/single-sign-on.md | 87% | merge → sso.md, redirect single-sign-on.md |
```

---

## Migration playbook

Two-phase migration: export → transform → validate → cutover.

### Phase 1: Inventory + export

- **Notion → markdown:** `npx notion-to-md` (via Notion API integration token).
- **Confluence → markdown:** `npx confluence-to-markdown` (storage format → CommonMark) preserving attachments.
- **Zendesk Guide → markdown:** `cli-anything` curl `/api/v2/help_center/articles.json` (paginate), transform HTML → markdown via `turndown` or Python `markdownify`.
- **Intercom Articles → markdown:** `cli-anything` curl `/articles` REST; transform HTML body → markdown.
- **Salesforce Knowledge → markdown:** export via Data Loader → CSV → transform.

### Phase 2: Transform

- Preserve: frontmatter (title, slug, tags, author, last-modified), attachments (`/assets/`), internal links (rewrite to new URL structure), code blocks (language hint preserved).
- Apply target-platform conventions (MDX components for Docusaurus, Mintlify snippets, Astro Starlight components).
- Build redirect map: old URL → new URL.

### Phase 3: Validate

- Lychee link-check: 100% pass.
- Page-count parity: source count == target count (excluding intentional merges).
- Spot-check sample of 10-20 articles for visual diff (screenshots match).
- Search index built; top-10 search queries return correct article.

### Phase 4: Cutover

- Deploy new KB to staging URL.
- Configure redirects (Netlify `_redirects`, Vercel `vercel.json`, Cloudflare Pages, server-level rewrites).
- Soft launch (banner: "We've moved! Beta link below.").
- DNS swap.
- Keep old KB read-only for 30d as rollback.

---

## AI doc assistant playbook

1. **Choose the platform** based on need:
   - **Verified citations + AI Q&A on tech docs** → Kapa.ai
   - **Search-first + chat fallback** → Inkeep
   - **Product-embedded SDK** → Mendable
   - **FOSS / self-host** → Markprompt

2. **Index the KB.** Auto-crawl with exclusion list for stale / archived.

3. **Build ground-truth eval set.** 50-100 questions covering top-searched + edge cases. Score each answer on:
   - **Accuracy** — does it match the source article?
   - **Citation** — does it cite the source article?
   - **Hallucination rate** — does it invent facts?
   - **Completeness** — does it cover the full answer?

4. **Eval loop.** Track per-release. Ship only when accuracy ≥90%, hallucination <5%.

5. **Embed in product.** In-app help widget + KB search results showing AI answer first, then matching articles.

6. **Feedback loop.** Each AI answer has thumbs up/down + optional text. Weekly review of thumbs-down → tune system prompt + add missing context articles.

---

## Multi-language playbook

1. **Lock source-of-truth locale.** Usually `en`. Every other locale is downstream.
2. **Pick locales.** Don't over-localize — pick 2-3 with concrete user count + revenue support.
3. **Set up DeepL Pro.** API key, `tag_handling=markdown`, glossary per locale, formality control.
4. **Wire Crowdin or Lokalise.** Connect source repo + target locale folders. Translation memory (TM) auto-suggests previous translations. Glossary enforces terminology.
5. **Per-locale review gate.** Native speaker SME reviews TM-suggested translations before publish.
6. **Site routing.** Docusaurus `i18n.locales: ['en','de','fr']`, Astro Starlight `locales`, MkDocs Material `i18n` plugin.
7. **CI gate.** Source change → translation queue (Crowdin auto-pulls). Block release if any locale missing > 5% of source content.

---

## Antipattern catalog

BAD / GOOD pairs the agent flags on review.

### Antipattern 1: deep IA (10+ levels)

**BAD:** docs → users → admins → enterprise → sso → okta → group-sync → troubleshooting → known-issues → article.

**Why it's bad:** Users can't navigate past 3-4 levels. First-click test fails.

**GOOD:** docs → How-to → Authentication → "SSO group sync (Okta)" (3 levels + tag `enterprise`).

**Why it's better:** Tag overlays handle cross-cutting concerns without deepening the tree.

### Antipattern 2: deleting stale articles instead of archiving

**BAD:** Delete article that's 12 months old.

**Why it's bad:** Loses inbound links, breaks SEO, loses retroactive context for support tickets that referenced it.

**GOOD:** Archive (hidden from navigation, kept in search with "Archived — verify before relying on" banner). Delete only after 12 months in archive.

### Antipattern 3: per-article ACLs

**BAD:** Each article has unique view permissions.

**Why it's bad:** Becomes unmaintainable. SSO group claims solve 95% of access control.

**GOOD:** SSO + SCIM + group-based ACLs at the section / category level. Per-article ACLs only for compliance-driven exceptions.

### Antipattern 4: launching AI doc assistant without eval

**BAD:** "Let's plug Kapa.ai into our docs and see how it goes."

**Why it's bad:** Hallucination is the killer. One wrong answer about billing destroys trust.

**GOOD:** Build 50-100 ground-truth Q&A pairs. Eval accuracy + citation + hallucination. Launch only at ≥90% / <5%.

### Antipattern 5: raw machine translation (no TM, no glossary)

**BAD:** Run all docs through DeepL on every release.

**Why it's bad:** Terminology drift. "Webhook" becomes "Webhook" in release 1, "callback" in release 2, "event hook" in release 3.

**GOOD:** TM + glossary per locale. Native-speaker SME review.

### Antipattern 6: tracking everything

**BAD:** Dashboard with 47 metrics nobody reads.

**Why it's bad:** Noise drowns signal.

**GOOD:** Top-searched + no-result + high-exit + deflection rate. That's 90% of decisions. Everything else is noise.

### Antipattern 7: mixing Diátaxis tiers in one article

**BAD:** "Get started with webhooks" article that mixes tutorial (do this step-by-step), reference (full event-type table), and explanation (why webhooks vs polling).

**Why it's bad:** Loses reader who wanted tutorial in reference details; loses reader who wanted reference in tutorial preamble.

**GOOD:** Split into:
- Tutorial: "Send your first webhook in 5 minutes"
- Reference: "Webhook event types"
- Explanation: "Why webhooks vs polling"

### Antipattern 8: no named owner

**BAD:** "Docs are owned by the team."

**Why it's bad:** No accountability = guaranteed stale.

**GOOD:** Each content area has a named owner. CODEOWNERS / RACI matrix / Slab Team Owner. Owner notified on stale-bot fire.

### Antipattern 9: KB built in isolation from support data

**BAD:** "Let's write KB articles about features."

**Why it's bad:** Articles cover what's interesting to the dev team, not what's painful to users.

**GOOD:** Top 10 ticket categories drive top 10 KB articles. KB roadmap = support pain prioritized.

### Antipattern 10: AI assistant without citations

**BAD:** AI assistant gives a confident-sounding answer with no source link.

**Why it's bad:** User can't verify; if wrong, user discovers it the hard way; trust erodes.

**GOOD:** Every AI answer cites the source article + paragraph. If no citation, prefix with "I'm not certain — this isn't in our KB. Could you …"

---

## KB taxonomy templates

### Template 1: B2B SaaS customer-facing KB (Diátaxis overlay)

```
docs/
  get-started/
    01-quickstart.md
    02-first-integration.md
    03-account-setup.md
  how-to/
    authentication/
      sso-okta.md
      sso-auth0.md
      api-keys.md
    webhooks/
      configure.md
      verify-signatures.md
      retry-strategy.md
    billing/
      update-payment.md
      switch-plans.md
      cancel.md
  concept/
    how-auth-works.md
    how-webhooks-work.md
    rate-limits.md
  reference/
    api/
    webhook-event-types.md
    error-codes.md
  troubleshooting/
    auth-errors.md
    webhooks-not-received.md
    billing-failures.md
  _archived/
  _redirects.json
  _taxonomy.md
  _OWNERS.md
```

### Template 2: Internal company wiki (Notion teamspace)

```
🏢 Company
  📋 Onboarding (new joiner checklist)
  💼 People & Culture
  💰 Finance & Procurement
  🛠️ IT & Security
🔧 Engineering
  🚀 Onboarding (engineering-specific)
  📚 Runbooks
  🧪 RFCs / ADRs
  🔐 Security
📈 Product
  🗺️ Roadmap
  📊 Metrics
  📝 Specs
🎨 Design
  🖼️ Design system
  📚 Brand guide
🚀 Go-to-market
  📝 Sales playbook
  🎯 Marketing
  💬 Support
📅 Meetings & Operations
🗄️ Archive (auto-hidden after 12 months)
```

### Template 3: Developer-facing KB (Docusaurus + versioned)

```
docs/
  intro.md
  guides/
    getting-started/
    deployment/
    monitoring/
  api/
    rest/
    graphql/
    webhooks/
  reference/
    cli/
    config/
    env-vars/
  changelog.md
  community.md
versioned_docs/
  version-1.0/
  version-2.0/
versions.json
```

---

## Redirect map template

```json
{
  "redirects": [
    { "from": "/docs/sso", "to": "/docs/how-to/authentication/sso-okta", "code": 301 },
    { "from": "/docs/single-sign-on", "to": "/docs/how-to/authentication/sso-okta", "code": 301 },
    { "from": "/docs/v1/api", "to": "/docs/v2/reference/api", "code": 301 },
    { "from": "/docs/old-quickstart", "to": "/docs/get-started/quickstart", "code": 301 }
  ]
}
```

Platform-native equivalents:

**Netlify `_redirects`:**
```
/docs/sso              /docs/how-to/authentication/sso-okta              301!
/docs/single-sign-on   /docs/how-to/authentication/sso-okta              301!
```

**Vercel `vercel.json`:**
```json
{ "redirects": [ { "source": "/docs/sso", "destination": "/docs/how-to/authentication/sso-okta", "permanent": true } ] }
```

**Cloudflare Pages:** same as Netlify `_redirects` syntax.

---

## Stale-bot workflow template

```yaml
# .github/workflows/stale-content.yml
name: KB stale content
on:
  schedule:
    - cron: '0 9 * * 1'  # Monday 9am UTC
  workflow_dispatch:

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }

      - name: Find stale articles
        id: stale
        run: |
          THRESHOLD_DAYS=180
          NOW=$(date -u +%s)
          find docs -name '*.md' -print0 | while IFS= read -r -d '' f; do
            ts=$(git log -1 --format=%ct -- "$f")
            age=$(( (NOW - ts) / 86400 ))
            if [ "$age" -gt "$THRESHOLD_DAYS" ]; then
              owner=$(grep -h "^${f}" .github/OWNERS.txt | awk '{print $2}')
              echo "$f|$age|$owner" >> stale.txt
            fi
          done

      - name: Ping owners on Slack
        env:
          SLACK_WEBHOOK: ${{ secrets.SLACK_WEBHOOK_DOCS }}
        run: |
          if [ -s stale.txt ]; then
            payload=$(awk -F'|' '{printf "%s (%sd) — %s\\n", $1, $2, $3}' stale.txt)
            curl -X POST -H 'Content-Type: application/json' \
              -d "{\"text\":\"Stale KB articles this week:\\n$payload\"}" \
              "$SLACK_WEBHOOK"
          fi

      - name: Open issue digest
        if: hashFiles('stale.txt') != ''
        uses: peter-evans/create-issue-from-file@v5
        with:
          title: 'Stale KB content — week of ${{ github.run_id }}'
          content-filepath: stale.txt
```

---

## SOTA tool reference (June 2026)

Grep-friendly per-tool reference. Each entry points at the bundled skill pack with the full recipe. Use this when deciding "what tool should I use for X?" Use the linked skill when actually executing.

### Algolia DocSearch

Free for open-source docs; the de facto SOTA for hosted KB search; Insights API surfaces top-searched, no-result, click-through.

- Apply: https://docsearch.algolia.com/apply/
- Use: `algolia init`, then drop the snippet in the docs site.
- Best for: OSS docs, any KB that wants minimum-effort hosted search.
- Skill pack: `skills/algolia-typesense-search-optimization/SKILL.md`.

### Typesense

Self-hosted SOTA. Sub-50ms latency. Synonyms collection + custom ranking.

- Install: `docker run -p 8108:8108 typesense/typesense:0.25.2 --data-dir=/data --api-key=xyz`
- Best for: self-hosted, mid-scale KBs.
- Skill pack: `skills/algolia-typesense-search-optimization/SKILL.md`.

### MeiliSearch

Self-hosted alternative. Typo-tolerant, fast indexing, simple deploy.

- Install: `curl -L https://install.meilisearch.com | sh`
- Skill pack: `skills/algolia-typesense-search-optimization/SKILL.md`.

### Pagefind

Client-side static-site search. Zero infrastructure.

- Install: `npx pagefind --site dist`
- Best for: static KBs that don't want any backend.
- Skill pack: `skills/algolia-typesense-search-optimization/SKILL.md`.

### Orama

Vector + full-text in one. FOSS + cloud tiers.

- Install: `npm i @orama/orama`
- Best for: KBs wanting embedding-based semantic search alongside lexical.
- Skill pack: `skills/algolia-typesense-search-optimization/SKILL.md`.

### Microsoft Clarity

Free behavioral analytics — heatmaps, click-streams, rage clicks, dead clicks, session replays. Native MCP server.

- Install: add Clarity tag to KB site; add `@microsoft/clarity-mcp-server` to `.mcp.json`.
- Best for: behavioral audit of any KB site.
- Skill pack: `skills/doc-analytics-clarity-ga4-algolia-insights/SKILL.md`.

### GA4 Data API

Programmatic Google Analytics queries — sessions, exit rate, engaged time, content groupings.

- Install: `pip install google-analytics-data`
- Use: service-account auth + RunReportRequest.
- Skill pack: `skills/doc-analytics-clarity-ga4-algolia-insights/SKILL.md`.

### Algolia DocSearch Insights API

Top-searched, no-result-found, CTR per page.

- Use: REST calls to `insights.algolia.io`.
- Skill pack: `skills/doc-analytics-clarity-ga4-algolia-insights/SKILL.md`.

### Kapa.ai

Verified AI for tech docs. Used by OpenAI / Reddit / Mapbox.

- Sign up: https://www.kapa.ai/
- Best for: tech docs needing high-accuracy AI Q&A.
- Skill pack: `skills/ai-doc-assistant-kapa-inkeep-mendable/SKILL.md`.

### Inkeep

Search-first + chat fallback. Lighter weight than Kapa.

- Sign up: https://inkeep.com/
- Skill pack: `skills/ai-doc-assistant-kapa-inkeep-mendable/SKILL.md`.

### Mendable

SDK for product embedding.

- Install: `npm i @mendable/sdk`
- Skill pack: `skills/ai-doc-assistant-kapa-inkeep-mendable/SKILL.md`.

### Markprompt

FOSS / self-hostable AI doc backbone.

- Install: https://markprompt.com/docs
- Best for: self-hosted, FOSS-friendly orgs.
- Skill pack: `skills/ai-doc-assistant-kapa-inkeep-mendable/SKILL.md`.

### Notion (KB platform + MCP)

Collaborative wiki. Native MCP. Databases + automation.

- MCP: `notion-mcp`
- Best for: internal wikis, RACI matrices, expert finder, lifecycle automation.
- Skill pack: `skills/employee-facing-internal-wiki-notion-slab/SKILL.md`.

### Confluence

Enterprise standard wiki. Page Approvals app + SCIM.

- API: `https://your-org.atlassian.net/wiki/rest/api/`
- Skill pack: `skills/employee-facing-internal-wiki-notion-slab/SKILL.md` (Confluence section).

### Document360

Self-serve customer KB platform. Workflows + version control + analytics built in.

- Skill pack: `skills/customer-facing-kb-support-deflection/SKILL.md`.

### Slab

Slack-native wiki. "Team Owner" feature.

- Skill pack: `skills/employee-facing-internal-wiki-notion-slab/SKILL.md`.

### Tettra

Slack-native lightweight wiki.

- Skill pack: `skills/employee-facing-internal-wiki-notion-slab/SKILL.md`.

### Guru

KB cards surfaced in Slack via "Card of the Day".

- Skill pack: `skills/employee-facing-internal-wiki-notion-slab/SKILL.md`.

### Intercom Articles

In-product Help widget + customer-facing KB. Deflection-tracking native.

- API: `https://api.intercom.io/articles`
- Skill pack: `skills/customer-facing-kb-support-deflection/SKILL.md`.

### Zendesk Guide

Mature customer KB. SCIM SSO. Broad integration ecosystem.

- API: `https://your-org.zendesk.com/api/v2/help_center/`
- Skill pack: `skills/customer-facing-kb-support-deflection/SKILL.md`.

### Pylon Help Center

Modern B2B-focused customer KB.

- Skill pack: `skills/customer-facing-kb-support-deflection/SKILL.md`.

### Vale (prose lint for KB)

Custom Diátaxis + brand-voice + Microsoft / Google style packs.

- Install: `brew install vale`
- Use: `vale --output=JSON docs/`
- Skill pack: `skills/kb-governance-style-vale-rules/SKILL.md`.

### Lychee (link checker for KB)

Fastest 2026 link checker. JSON output, fragment checking, CI integration.

- Install: release binary, `brew`, `cargo`, or Docker.
- Use: `lychee --format json --output report.json .`
- Skill pack: `skills/content-audit-stale-inaccurate-redundant/SKILL.md`.

### pytest-markdown-docs

Modal Labs' executable code-fence validator.

- Install: `uv add --dev pytest pytest-markdown-docs`
- Use: `pytest --markdown-docs docs/`
- Skill pack: `skills/content-audit-stale-inaccurate-redundant/SKILL.md`.

### simhash / datasketch

Text-similarity for redundant-content detection.

- Install: `pip install simhash datasketch`
- Skill pack: `skills/content-audit-stale-inaccurate-redundant/SKILL.md`.

### notion-to-md

Notion → markdown migration.

- Install: `npm i -g notion-to-md`
- Skill pack: `skills/content-migration-between-platforms/SKILL.md`.

### confluence-to-markdown

Confluence storage format → CommonMark migration.

- Install: `npm i -g confluence-to-markdown`
- Skill pack: `skills/content-migration-between-platforms/SKILL.md`.

### DeepL Pro API

SOTA machine translation for KB. `tag_handling=markdown` preserves formatting.

- Install: `deepl-mcp` MCP server OR REST.
- Skill pack: `skills/multi-language-localized-kb-deepl-crowdin/SKILL.md`.

### Crowdin

Translator workflow + TM + glossary.

- Install: `npm i -g @crowdin/cli`
- Skill pack: `skills/multi-language-localized-kb-deepl-crowdin/SKILL.md`.

### Lokalise

Alt to Crowdin.

- Install: `npm i -g @lokalise/cli-2`
- Skill pack: `skills/multi-language-localized-kb-deepl-crowdin/SKILL.md`.

### Argos Translate (FOSS fallback)

Local-model machine translation. Free.

- Install: `pip install argostranslate`
- Skill pack: `skills/multi-language-localized-kb-deepl-crowdin/SKILL.md`.

### Stonly

Decision-tree style interactive KB guides.

- Skill pack: `skills/interactive-guide-stonly-whatfix/SKILL.md`.

### Whatfix

In-product Self-Help widget overlaying real UI.

- Skill pack: `skills/interactive-guide-stonly-whatfix/SKILL.md`.

### Pendo Guides

Lighter, analytics-driven in-product guides.

- Skill pack: `skills/interactive-guide-stonly-whatfix/SKILL.md`.

### Shepherd.js

FOSS in-product tour library.

- Install: `npm i shepherd.js`
- Skill pack: `skills/interactive-guide-stonly-whatfix/SKILL.md`.

### Loom

Narrated screencasts. Public API for embeds + transcripts.

- API: `https://loom.com/developers`
- Skill pack: `skills/video-kb-loom-tango-scribe/SKILL.md`.

### Tango / Scribe

Auto-generated step-by-step process guides from browser captures.

- Skill pack: `skills/video-kb-loom-tango-scribe/SKILL.md`.

### Guidde

AI-narrated walkthroughs.

- Skill pack: `skills/video-kb-loom-tango-scribe/SKILL.md`.

### Beamer / Headway / LaunchNotes

In-product changelog widgets.

- Skill pack: `skills/changelog-beamer-headway-inproduct/SKILL.md`.

### feedgen (FOSS RSS fallback)

Generate RSS / Atom feeds for changelog.

- Install: `pip install feedgen`
- Skill pack: `skills/changelog-beamer-headway-inproduct/SKILL.md`.

### Antora (AsciiDoc multi-output)

Enterprise docs-as-code with topic reuse.

- Install: `npx antora`
- Skill pack: `skills/content-reuse-single-source-asciidoc-antora/SKILL.md`.

### Docusaurus versions

Per-product-version snapshots.

- Use: `npm run docusaurus docs:version 2.0`
- Skill pack: `skills/kb-versioning-per-product-docusaurus-mike/SKILL.md`.

### mike (MkDocs versioning)

Version dropdown UI + alias management for MkDocs.

- Install: `pip install mike`
- Use: `mike deploy 2.0 latest --push`
- Skill pack: `skills/kb-versioning-per-product-docusaurus-mike/SKILL.md`.

### sphinx-multiversion

Sphinx per-branch docs.

- Install: `pip install sphinx-multiversion`
- Skill pack: `skills/kb-versioning-per-product-docusaurus-mike/SKILL.md`.

### Okta / Auth0 / Azure AD (SSO)

SAML / OIDC + SCIM for KB gating.

- Skill pack: `skills/sso-gated-kb-okta-auth0/SKILL.md`.

### Schema.org Article + FAQPage + HowTo

Structured data for KB SEO + AI-search citation.

- Reference: https://schema.org/Article
- Skill pack: `skills/kb-seo-aeo-geo-public-ranking/SKILL.md`.

### llms.txt

Standard for AEO/GEO — being citable by ChatGPT / Perplexity / Gemini.

- Reference: https://llmstxt.org/
- Skill pack: `skills/kb-seo-aeo-geo-public-ranking/SKILL.md`.

### Cloudflare Workers

FOSS KB-feedback backend.

- Install: `npx wrangler init`
- Skill pack: `skills/kb-feedback-collection-helpful-open/SKILL.md`.

### OptimalSort TreeJack

First-click testing for KB taxonomy.

- Sign up: https://www.optimalworkshop.com/treejack
- Skill pack: `skills/kb-taxonomy-design-categories-tags-hierarchy/SKILL.md`.

### GitHub stale-bot Action

Automated stale-content workflow.

- Reference: https://github.com/actions/stale
- Skill pack: `skills/content-review-cadence-monthly-quarterly/SKILL.md`.

---

## SOTA execution playbook (which skill pack to reach for)

When the user names a use case, the agent picks the matching skill pack:

| User asks | First-stop skill pack | Notes |
|---|---|---|
| "Design our KB taxonomy" | `kb-taxonomy-design-categories-tags-hierarchy` | Pull ticket data + Algolia Insights first |
| "Search is bad" | `algolia-typesense-search-optimization` | Audit no-result-found, build synonyms |
| "Articles go stale" | `content-lifecycle-draft-review-publish-archive` + `content-review-cadence-monthly-quarterly` | Stale-bot + owner pings |
| "Set up KB analytics" | `doc-analytics-clarity-ga4-algolia-insights` | Free signals first (Clarity + Algolia Insights) |
| "What's our deflection rate?" | `kb-roi-deflection-rate` | Per-category, not per-article |
| "Audit our docs" | `content-audit-stale-inaccurate-redundant` | Three-axis: stale / inaccurate / redundant |
| "Migrate KB from Notion to Docusaurus" | `content-migration-between-platforms` | Always validate w/ link-checker + page-count parity |
| "Migrate from Confluence" | `content-migration-between-platforms` | Use `confluence-to-markdown` |
| "Add AI Q&A to our docs" | `ai-doc-assistant-kapa-inkeep-mendable` | Build ground-truth eval BEFORE launch |
| "Translate docs into German/Japanese" | `multi-language-localized-kb-deepl-crowdin` | DeepL + Crowdin + TM + glossary |
| "Gate KB behind SSO" | `sso-gated-kb-okta-auth0` | SAML/OIDC + SCIM |
| "Version our docs per release" | `kb-versioning-per-product-docusaurus-mike` | Docusaurus / mike / Mintlify versions |
| "Reuse content across product manuals" | `content-reuse-single-source-asciidoc-antora` | AsciiDoc + Antora |
| "Collect article feedback" | `kb-feedback-collection-helpful-open` | Free fallback: Cloudflare Workers + Notion |
| "Build internal wiki" | `employee-facing-internal-wiki-notion-slab` | Notion teamspaces + Slack surfacing |
| "Set up customer KB" | `customer-facing-kb-support-deflection` | Intercom / Pylon / Helpdesk + in-product widget |
| "Add interactive guides" | `interactive-guide-stonly-whatfix` | Free fallback: Shepherd.js |
| "Add video walkthroughs" | `video-kb-loom-tango-scribe` | Loom for narrated; Tango for SOP |
| "Launch a changelog" | `changelog-beamer-headway-inproduct` | Free fallback: RSS via feedgen |
| "Who knows about X internally?" | `expert-finder-who-knows-x` | Notion db + Slack history + git author |
| "Train our team to write docs" | `kb-authoring-training-non-doc-team` | Checklist + templates + Vale-as-tutor |
| "Set up KB governance" | `kb-governance-style-vale-rules` | Vale + markdownlint + last-verified stamp |
| "Build KB-to-CRM deflection report" | `kb-roi-deflection-rate` | Salesforce / HubSpot custom property |
| "Improve KB SEO + AI citation" | `kb-seo-aeo-geo-public-ranking` | Schema.org + llms.txt + Ahrefs/AthenaHQ |
| "Set up RACI for KB ownership" | `knowledge-ops-owner-contributor-flow` | Named owner per content area |

---

## Closing rules

Always treat the KB as a product. Taxonomy is half the search experience. Stale content is worse than missing content. Doc analytics tell you what to write next. Instrument before opining; ship the running system, not advice.
