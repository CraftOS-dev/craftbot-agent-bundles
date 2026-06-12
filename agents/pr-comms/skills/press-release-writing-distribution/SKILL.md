<!--
Source: https://www.prezly.com/academy/business-wire-vs-pr-newswire
Wire API integration: https://signalgenesys.com/news-api-integration/
AP/PRSA format: https://www.prsa.org/article/the-prsa-press-release-template
Prowly AI generator: https://prowly.com/ai-press-release-generator/
-->
# Press Release Writing + Distribution — SKILL

End-to-end press release workflow: AP/PRSA-format draft, Vale brand-voice lint, wire-service distribution via PR Newswire / Business Wire / GlobeNewswire APIs, embargo discipline, and post-distribution placement tracking. The default for any "material" news (launch, funding, partnership, milestone). Routine news routes through the newsroom-only path.

## When to use this skill

- **Material news** — launch, funding round, partnership, acquisition, major hire, milestone — gets wire distribution.
- **Routine news** — minor updates, hires, awards earned — newsroom-only + 1:1 tier-1 outreach.
- **Reg-FD disclosure** for public companies — Business Wire (only major wire that's certified Reg-FD compliant).
- **Embargoed launches** — self-distribute via `gmail-mcp` per-journalist; coordinate wire release at embargo lift.
- **Multi-language launches** — translate via `deepl-mcp`; route per-region wire (PRN Europe, PRN Asia, etc.).

**Do NOT use this skill when:**
- The release is a SEC 8-K / earnings disclosure — defer to `investor-relations` agent.
- The "release" is actually customer-facing incident comm — defer to `customer-support-agent`.
- The story has no actual news (rewording an existing announcement) — push back on the brief.

## Setup

### Vale linter (brand voice + AI-slop)

```bash
uvx vale --version
# Config file at .vale.ini with PR + AI-slop rules
ls styles/PR/APStyle.yml styles/Brand/AISlop.yml
```

### PR Newswire (Cision) API

```bash
# Get account credentials from Cision dashboard
export PRN_USERNAME="<account>"
export PRN_PASSWORD="<password>"
export PRN_API_BASE="https://api.prnewswire.com/v1"
```

Per-release distribution fees: $350 (local), $1,200 (national), $3,000 (national + photo + key targeting).

### Business Wire (Berkshire) API

```bash
# Get NewsHQ account credentials
export BW_USERNAME="<account>"
export BW_API_KEY="<key>"
export BW_API_BASE="https://newshq.businesswire.com/api/v2"
```

Per-release fees: $760-$2,300; only major wire with certified Reg-FD distribution to AP/Reuters/Dow Jones terminals.

### GlobeNewswire (Notified) API

```bash
export GNW_USERNAME="<account>"
export GNW_PASSWORD="<password>"
export GNW_API_BASE="https://newshq.notified.com/api/v1"
```

Mid-tier pricing $400-$1,500 per release.

### Prowly newsroom (optional alt distribution surface)

```bash
export PROWLY_API_KEY="<key>"
export PROWLY_NEWSROOM_ID="<id>"
```

$369/mo Prowly subscription includes newsroom + media DB + AI release generator.

## Common recipes

### Recipe 1: AP/PRSA-format release draft

```markdown
**FOR IMMEDIATE RELEASE**
[or EMBARGOED UNTIL Tuesday, January 14, 2026, 6:00 AM ET]

# [Headline — 8-12 words, active verb, news-forward, no buzzwords]

## [Subhead — 12-20 words clarifying who/why]

**SAN FRANCISCO, CA — June 11, 2026 —** Acme Corp today announced [the news, 30-50 words, inverted pyramid: most important fact first].

[Paragraph 2: Context — why this matters. 50-80 words. Cite specific data, market, or customer.]

"[CEO quote — substantive, attributable, not corporate jargon. 40-80 words.]" said [Name], [Title], Acme Corp.

[Paragraph 3: Customer or partner detail. 50-80 words.]

"[Customer/partner quote with permission. 40-60 words.]" said [Name], [Title], [Company].

[Paragraph 4: Availability / pricing / next steps.]

## About Acme Corp

[Boilerplate — 50-100 words. Latest approved version from Notion.]

## Media Contact

press@acme.com
+1 415 555 0100

###
```

### Recipe 2: Vale lint pass (kills AI slop + buzzwords)

```bash
uvx vale \
  --config=.vale.ini \
  --output=JSON \
  release.md \
| jq '.["release.md"][] | {Line, Severity, Message, Match}'
```

Vale rules to enforce (in `styles/PR/APStyle.yml` and `styles/Brand/AISlop.yml`):
- Ban "leverage", "utilize", "synergize", "best-in-class", "game-changing", "cutting-edge", "revolutionary", "world-class", "industry-leading", "disrupting"
- Ban opener clichés: "thrilled to announce", "in today's fast-paced world", "look no further than"
- Em-dash density warning (>1 per paragraph)
- Passive-voice chain warning (>3 in a row)
- AP style: numbers <10 written, percentages with %, dates in Month Day, Year form

### Recipe 3: PR Newswire submission

```bash
curl -X POST "$PRN_API_BASE/releases" \
  -u "$PRN_USERNAME:$PRN_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "Acme Corp Raises $50M Series B Led by Sequoia",
    "subheadline": "Funding accelerates AI infrastructure expansion across North America",
    "body": "<release body in HTML>",
    "release_date": "2026-06-11T13:00:00Z",
    "distribution": {
      "geography": ["US"],
      "industries": ["TECH","AI","FINTECH"],
      "targets": ["national","trade","top-tier"]
    },
    "contact": {
      "name": "Press Team",
      "email": "press@acme.com",
      "phone": "+1-415-555-0100"
    },
    "summary_keywords": ["AI infrastructure","Series B","Sequoia"],
    "include_photo": true,
    "photo_urls": ["https://acme.com/press/founder-headshot.jpg"]
  }'
```

Returns `release_id` and `distribution_receipt`. Pull placement report 24-72hrs later via `/releases/{id}/placements`.

### Recipe 4: Business Wire submission (Reg-FD compliant)

```bash
curl -X POST "$BW_API_BASE/news/release" \
  -H "X-API-Key: $BW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "headline": "Acme Corp Reports Q1 2026 Results",
    "release_type": "earnings",
    "regulatory_compliance": "Reg-FD",
    "release_body": "<full body>",
    "ticker_symbols": ["ACME"],
    "release_time": "2026-04-25T20:30:00Z",
    "distribution_circuit": "US1+CA1+UK1",
    "target_industries": ["I:CPR","I:TEC"]
  }'
```

For non-Reg-FD news, use `"release_type": "general"`.

### Recipe 5: GlobeNewswire submission

```bash
curl -X POST "$GNW_API_BASE/release/submit" \
  -u "$GNW_USERNAME:$GNW_PASSWORD" \
  -H "Content-Type: application/json" \
  -d @release.json
```

Where `release.json` follows GNW schema: `{headline, dateline, body, contact, distribution_codes, embargo_time}`.

### Recipe 6: Self-distribute embargoed release (tier-1 individual sends)

```bash
# Pull tier-1 list from notion-mcp
# Loop per journalist — NEVER BCC

for journalist in $(notion query 'media_list/tier_1_tech'); do
  name=$(echo "$journalist" | jq -r .name)
  email=$(echo "$journalist" | jq -r .email)
  last_article_url=$(echo "$journalist" | jq -r .last_article_url)

  # Claude personalizes opening line citing last article
  personal_hook=$(claude-personalize --journalist "$journalist" --release release.md)

  gmail-mcp send \
    --to "$email" \
    --subject "EMBARGOED Jun 18 6am ET: Acme Series B" \
    --body "$personal_hook

$(cat release.md)

Embargo: Tuesday, June 18, 2026, 6:00 AM ET.
Pre-brief slots: Friday 1-5pm PT (book via $CALENDLY_URL).

Media kit: https://acme.com/press/series-b-kit"
done
```

### Recipe 7: Wire + supplementary tier-1 outreach (standard launch)

```bash
# Step 1: schedule wire at embargo lift
prn_release_id=$(curl ... | jq -r .release_id)

# Step 2: 5-7 days BEFORE embargo, individual outreach to 10-15 tier-1 journalists
# (see Recipe 6)

# Step 3: at embargo lift moment (e.g., Tuesday 6am ET), wire fires automatically.
# Tier-1 stories publish; tier-2/3 cover with 4-24hr delay.

# Step 4: 1 hour pre-lift, send terse confirmation to embargo list
for j in $(notion query 'media_list/embargo_jun18'); do
  gmail-mcp send --to $(echo "$j" | jq -r .email) \
    --subject "Reminder: Acme embargo lifts in 1 hour" \
    --body "Hi [name] — embargo lifts at 6am ET. Wire release is queued. Any final questions?"
done
```

### Recipe 8: Placement tracking 24-72hrs post-release

```bash
# Pull placement report from wire
curl -s "$PRN_API_BASE/releases/$prn_release_id/placements" \
  -u "$PRN_USERNAME:$PRN_PASSWORD" \
| jq '.placements[] | {outlet, url, audience, date}' \
> placements.json

# Cross-reference via firecrawl + brave-search for headline keywords
brave-search "Acme Series B Sequoia" --since "2026-06-18" \
| jq '.results[] | {url, title, snippet}' \
>> placements.json

# Tag each placement with tier from outlet rubric in notion
# Calculate EMV: UVM x CPM x tier_multiplier x syndication_factor
python calculate_emv.py placements.json > emv_report.json

# Log to Notion coverage tracker
notion-mcp create_page --db coverage_log --properties "$(cat emv_report.json)"
```

## Examples — full launch workflow

```yaml
T-14_days:
  - confirm news + strategy + spokesperson availability
  - draft press release in markdown
  - vale lint pass
  - legal + marketing review
  - boilerplate update if needed
  - select wire service (PRN/BW/GNW) by audience match

T-7_days:
  - identify 10-15 tier-1 journalists in notion media list
  - build customer + partner quote with sign-off
  - prepare media kit (canva-mcp + figma-mcp): logos, headshots, product shots
  - calendly pre-brief slots open
  - if embargoed: NDA via DocuSign optional

T-5_days:
  - send embargoed pitches via gmail-mcp (1:1, never BCC)
  - submit wire release scheduled for embargo lift moment

T-1_day:
  - send reminder embargo notice
  - brief spokesperson via mcp-tts audio drill (handoff to media-training-spokesperson-prep)
  - confirm wire submission scheduled correctly

T-0 (embargo lift):
  - wire release fires
  - newsroom page updated
  - LinkedIn org post + CEO LinkedIn newsletter teaser
  - twitter-mcp thread from spokesperson
  - monitor brand mentions every 30 min for first 4 hours

T+24h:
  - pull placement report from wire
  - cross-reference brave-search + firecrawl-mcp
  - tag placements by tier
  - calculate EMV
  - log to notion coverage DB

T+72h:
  - second pass placement gathering
  - sentiment overlay (Brand24 or Claude classifier)
  - weekly digest to client via gmail-mcp
  - feed coverage URLs into AEO citation tracker
```

## Edge cases

### Reg-FD compliance for public companies
Only Business Wire carries certified Reg-FD distribution to AP, Reuters, Dow Jones, Bloomberg terminals. PR Newswire and GlobeNewswire are NOT Reg-FD compliant for material disclosure. For 8-K-level news, route through Business Wire OR defer to `investor-relations` for direct EDGAR filing.

### Embargo break protocol
If a journalist publishes before embargo lift:
1. Immediately lift embargo to remaining list (individual sends, "Embargo is lifted effective immediately")
2. Fire the wire release NOW if it was scheduled for later
3. Log the break in `notion-mcp` (offending outlet + journalist, for the relationship blacklist conversation — never auto-ban)
4. Don't shame the breaker publicly; private conversation only

### Photo + video distribution
Wire services charge extra for photo ($200-$500) and video ($500-$2,000) attachments. Always include photo for product launches and funding — boosts pickup rate. Use 1200x675 (16:9), under 5MB, JPG or PNG. Source from `canva-mcp` or `figma-mcp` brand kit.

### Multi-language international launches
Translate via `deepl-mcp` per target language. Route through regional wire (PRN Europe for EU, Kyodo for Japan, Xinhua for China). Local journalist lists in `notion-mcp` per region; per-language template stored separately. Don't auto-translate boilerplate quotes — get native review.

### Headline length + SEO
Wire headline limits: PRN 200 chars, BW 150 chars, GNW 130 chars. AI search engines (ChatGPT/Perplexity) preferentially cite headlines under 80 chars. Front-load brand + verb + outcome.

### What NOT to put in a release
- Forward-looking statements without safe-harbor language (public co. lawsuit risk)
- Customer names without explicit written permission
- Competitor names (creates ad opportunity for them in syndication)
- Pricing details that conflict with the website
- Internal jargon, product code names, unannounced roadmap items

### Newsroom-only path (routine news)
For news that doesn't warrant wire:
1. Publish to Prezly/Prowly newsroom via API
2. SEO-optimize landing page (schema.org NewsArticle, headline H1, structured data)
3. Tweet from company account
4. LinkedIn org post
5. No wire distribution → no fees

Routine news = hires under VP, single-product updates, generic awards.

### Wire pickup expectations
Realistic pickup rates by tier:
- Tier-1 (NYT/WSJ/Bloomberg): wire alone won't earn this — needs embargo + 1:1
- Tier-2 (trades): 30-60% pickup from wire with strong news
- Tier-3 (niche/regional): 70-90% via syndication, mostly headline-only reposts

Don't sell the client on "wire = NYT" — that's not how it works.

### When AI press release generators are okay
Prowly AI Press Release Generator produces a usable first draft from a brief. Claude in this skill is better for the second pass (humanization, news-forward verbs, killing buzzwords). Don't ship the AI-generator draft without a human/Claude edit pass.

## Sources

- **AP/PRSA format**: https://www.prsa.org/article/the-prsa-press-release-template
- **PR Newswire vs Business Wire comparison**: https://www.prezly.com/academy/business-wire-vs-pr-newswire
- **PR Newswire API**: https://www.prnewswire.com/products-services/distribution/
- **Business Wire NewsHQ API**: https://www.businesswire.com/portal/site/home/template.MAXIMIZE/menuitem.fd2f2c01da08ce4dffcefb024500aa0c/?javax.portlet.tpst=12b517fdf12f3b1d33eb71a85fc3dac0_ws_MX
- **GlobeNewswire Notified API**: https://www.notified.com/products/news-distribution
- **News API integration overview**: https://signalgenesys.com/news-api-integration/
- **Distribution pricing 2026**: https://pressonify.ai/blog/press-release-distribution-pricing-comparison-2026
- **Prowly AI release generator**: https://prowly.com/ai-press-release-generator/
- **Vale linter**: https://vale.sh/
