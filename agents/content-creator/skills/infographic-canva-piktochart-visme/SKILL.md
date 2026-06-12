# Infographic Design — Piktochart AI / Canva MCP / Visme

> Pick the right infographic tool by use case, brief the design, and ship via API / MCP.

## When to use

Trigger on: "make an infographic", "data infographic from this report", "Piktochart this URL", "Canva infographic", "visualize these stats", "lead magnet PDF infographic". This skill owns: tool decision (data-heavy = Piktochart, branded social = Canva, interactive = Visme), brief authoring, API/MCP execution. For LinkedIn-specific carousel infographics see `linkedin-carousel-authoring`. For 1-3 pull-quote graphics see the quote-card recipes in `linkedin-carousel-authoring`.

## Setup

```bash
# Piktochart — data-heavy AI outline (no MCP yet; REST + GUI workflow)
curl -H "Authorization: Bearer $PIKTOCHART_API_KEY" https://api.piktochart.com/v1/me

# Canva MCP — branded templates
npx @canva/mcp --version

# Visme — interactive infographics + chart-heavy
curl -H "X-API-KEY: $VISME_API_KEY" https://api.visme.co/v1/users/me

# Adobe Express — marketing-polished alt (limited API)
# Manual via web app for most workflows
```

Auth env vars:
- `PIKTOCHART_API_KEY` — Piktochart Team plan ($29/mo) for API access.
- `CANVA_API_KEY` — Canva for Teams enterprise.
- `CANVA_INFOGRAPHIC_TEMPLATE_ID` — pre-built branded infographic template.
- `VISME_API_KEY` — Visme Pro plan.

## Common recipes

### Recipe 1: Tool decision tree

```markdown
## Choose by use case

**Piktochart** — DATA-HEAVY infographics
- 5+ data points to visualize
- Source data has structure (CSV, JSON, URL with stats)
- Goal: information density + scannable
- Best for: research reports, statistics roundups, comparison tables, timeline visualizations

**Canva MCP** — BRANDED SOCIAL infographics
- 1-5 data points; mostly visual storytelling
- Goal: brand fidelity + speed
- Best for: social-feed infographics, mini-explainers, quote-card-adjacent designs
- Reuses your brand colors + fonts + logo

**Visme** — INTERACTIVE / EMBED-FRIENDLY infographics
- Chart-heavy with interactive elements
- Goal: web embed (hover states, click-through layers)
- Best for: blog post embeds, interactive reports, dashboards

**Adobe Express** — MARKETING-POLISHED static
- 3-7 data points
- Goal: hand-tuned visual polish
- Best for: lead magnets, brochures, brand-aligned PDFs
- Slower workflow; less API; better for hero pieces

## Decision shortcut
- Source = URL or PDF with extractable structure → Piktochart AI outline
- Source = brand-driven, social-feed audience → Canva MCP
- Source = chart-heavy and goal is web embed → Visme
- Source = hero piece needing polish → Adobe Express (manual)
```

### Recipe 2: Infographic brief template

```markdown
# Infographic: <working title>

## Headline (max 10 words)
<the promise the infographic delivers>

## Subheading (1 line)
<what the reader gets from scanning>

## Data points (3-7)
- Stat 1: <number + source URL + date>
- Stat 2: <number + source URL + date>
- Stat 3: <number + source URL + date>
- Stat 4: <number + source URL + date>
- Stat 5 (optional): <...>

## Sections
- Section 1: <headline + supporting visual idea>
- Section 2: <...>
- Section 3: <...>

## Visual style
- Color palette: <brand colors as hex>
- Typography: <headline / body / caption fonts>
- Iconography: <icon set or inline emoji>
- Charts: <bar / pie / line / dot — match to data type>

## Sources (footer)
- Source 1 — URL + date accessed
- Source 2 — URL + date

## Distribution targets
- [ ] LinkedIn feed (1080×1080 square)
- [ ] Pinterest pin (1000×1500 vertical)
- [ ] Embed in blog post (responsive)
- [ ] Lead-magnet PDF download (8.5"×11" or A4)
- [ ] Twitter / X (1080×1080 square)
```

### Recipe 3: Piktochart AI outline from URL

```bash
# Piktochart's "AI Outline" takes a URL or PDF and extracts headings + stats + structure
curl -X POST https://api.piktochart.com/v1/ai-outline \
  -H "Authorization: Bearer $PIKTOCHART_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "source_url": "https://yoursite.com/2026-newsletter-report",
    "template_category": "report",
    "language": "en"
  }'

# Returns outline + template_id
# Use the outline to populate a Piktochart template via dashboard or follow-up API call
```

Note: Piktochart's public API is limited; AI Outline + Template instantiation are the two primary endpoints. Final tweaking often requires dashboard.

### Recipe 4: Piktochart from PDF source

```bash
# Upload a PDF report; AI extracts key data
curl -X POST https://api.piktochart.com/v1/ai-outline \
  -H "Authorization: Bearer $PIKTOCHART_API_KEY" \
  -F "source_pdf=@2026_state_of_newsletters.pdf" \
  -F "template_category=report"

# Returns suggested template + populated data points
```

### Recipe 5: Canva MCP branded infographic from template

```bash
# Pre-build a branded infographic template in Canva
# Use {{placeholder_n}} for swappable text/stat blocks

npx @canva/mcp create_design \
  --template_id "$CANVA_INFOGRAPHIC_TEMPLATE_ID" \
  --customizations '[
    {"name":"headline","value":"State of Newsletters 2026"},
    {"name":"subhead","value":"5 stats reshaping the creator economy"},
    {"name":"stat_1_number","value":"42%"},
    {"name":"stat_1_label","value":"of newsletters now use Beehiiv"},
    {"name":"stat_2_number","value":"$1.2B"},
    {"name":"stat_2_label","value":"creator-economy newsletter revenue"},
    {"name":"stat_3_number","value":"6.6%"},
    {"name":"stat_3_label","value":"LinkedIn carousel engagement"},
    {"name":"source_footer","value":"Beehiiv 2026 + Supergrow + ThoughtLeaders"}
  ]' \
  --output infographic_export

# Export to PNG / PDF / SVG
npx @canva/mcp export_design \
  --design_id "$CANVA_DESIGN_ID" \
  --format pdf \
  --output infographic.pdf
```

### Recipe 6: Visme interactive infographic

```bash
# Visme via REST (chart-heavy + interactive)
curl -X POST https://api.visme.co/v1/projects \
  -H "X-API-KEY: $VISME_API_KEY" \
  -d '{
    "template_id": "<infographic_template_id>",
    "type": "infographic",
    "data": {
      "headline": "...",
      "data_source": "<csv_url_or_json>",
      "chart_type": "bar"
    }
  }'

# Visme generates an embed URL for blog posts:
# <iframe src="https://my.visme.co/projects/<id>"></iframe>
```

### Recipe 7: Multi-format export (Canva)

```bash
# After design is finalized, export multiple aspect ratios for distribution
DESIGN_ID="<canva_design_id>"

# Square (1:1) for LinkedIn / X / IG feed
npx @canva/mcp export_design --design_id $DESIGN_ID --format png --width 1080 --height 1080 --output square.png

# Pinterest (2:3 vertical)
npx @canva/mcp export_design --design_id $DESIGN_ID --format png --width 1000 --height 1500 --output pinterest.png

# Blog post (full width)
npx @canva/mcp export_design --design_id $DESIGN_ID --format png --width 1920 --height 1080 --output blog.png

# Lead magnet PDF
npx @canva/mcp export_design --design_id $DESIGN_ID --format pdf --output leadmag.pdf
```

### Recipe 8: Chart type → data type matching

```markdown
| Chart type | Best for | Worst for |
|---|---|---|
| Bar | Comparing distinct values across categories | Continuous time-series |
| Line | Continuous trends over time | Categorical comparisons |
| Pie / donut | Composition where total = 100% and ≤6 segments | More than 6 segments (use bar) |
| Dot / scatter | Distribution patterns; correlation | Direct comparisons |
| Sankey / flow | Process / journey visualization | Static states |
| Treemap | Hierarchical proportions | Time-series |
| Heatmap | Density + 2-axis correlation | Single-axis distributions |
| Area | Cumulative trends over time | Categorical comparisons |
```

### Recipe 9: Source-cite hygiene

```markdown
Every infographic MUST include:
- Source URL for each stat (or grouped if from same source)
- Date data was accessed
- Methodology one-liner (e.g., "n=500 newsletter operators surveyed Q2 2026")

Source footer template:
"Sources: <Source A>, <Source B>. Data as of <date>. Methodology: <one-line>."

E-E-A-T signal — undated/uncited infographics get downranked in Pinterest + Google Image Search.
```

### Recipe 10: Distribute infographic

```bash
# Multi-platform distribution
# LinkedIn feed (square)
npx @buffer/mcp-server create_post --platform linkedin --media-file square.png --content "Caption"
# Pinterest (vertical pin)
npx @buffer/mcp-server create_post --platform pinterest --media-file pinterest.png --content "Caption" --board "<board_id>"
# X feed
npx @buffer/mcp-server create_post --platform twitter --media-file square.png --content "Caption"
# Embed in blog post (Ghost / Wordpress / Substack)
# Lead-magnet gating via newsletter-subscriber-growth skill
```

### Recipe 11: Update infographic when data changes

```bash
# Annual report update? Reuse Canva template with refreshed customizations
npx @canva/mcp create_design \
  --template_id "$CANVA_INFOGRAPHIC_TEMPLATE_ID" \
  --customizations '[
    {"name":"headline","value":"State of Newsletters 2027"},
    {"name":"stat_1_number","value":"58%"},
    ...
  ]' \
  --output 2027_version
```

Maintain a Notion DB of "Infographic templates" with refresh cadence + last-updated dates.

### Recipe 12: Lead-magnet PDF version

```bash
# Build a 4-8 page version for newsletter sign-up lead magnet
# Same source data + Canva template, but multi-page PDF instead of single image
# Gate behind email capture in newsletter-subscriber-growth skill
```

## Examples

### Example 1: Data report → branded social infographic

**Goal:** Turn a 20-page state-of-newsletters report into a single square infographic for LinkedIn.

**Steps:**
1. Recipe 2: write brief — 5 data points, brand color palette, single-source citation.
2. Recipe 4: Piktochart AI Outline from the PDF report.
3. Recipe 5: hand-translate Piktochart outline into Canva customizations (Canva for brand fidelity).
4. Recipe 9: add source footer with URL + date + methodology.
5. Recipe 7: export square + Pinterest + blog variants.
6. Recipe 10: Buffer cascade to LinkedIn + Pinterest + X + IG.

**Result:** Report condensed to scannable visual with proper citations; distributed across 4 platforms.

### Example 2: Interactive embed for blog post

**Goal:** Long-form blog post needs an interactive chart embed showing newsletter platform market share over 3 years.

**Steps:**
1. Recipe 2: brief — chart-heavy, web-embed target.
2. Recipe 6: Visme project with bar-chart-over-time template.
3. Upload CSV of platform market share by year.
4. Visme generates embed URL.
5. Paste `<iframe>` into blog post body via Ghost admin API or Wordpress.

**Result:** Interactive chart in blog post with hover states.

### Example 3: Lead-magnet PDF infographic for newsletter signup

**Goal:** Multi-page infographic PDF gated behind email capture.

**Steps:**
1. Recipe 2: brief — 6 pages, brand-aligned, gated download.
2. Recipe 5: Canva multi-page template instantiated with stats.
3. Recipe 12: export as PDF.
4. Upload PDF to Kit / Beehiiv / Ghost lead-magnet flow.
5. Tag-segment newsletter subscribers who download (for follow-up automation).

**Result:** New email subs + qualified lead-magnet downloads.

## Edge cases / gotchas

- **Piktochart public API is limited.** AI Outline + template instantiation work; deep customization often requires GUI. Plan for 30% manual finishing.
- **Canva MCP requires Teams enterprise** for API access ($300/mo+). For solo creators, Canva GUI + manual export.
- **Visme embeds slow blog page load** if multiple on one page. Use Visme for primary embed only; static for the rest.
- **Adobe Express has no proper API** for infographic generation as of June 2026 — included for completeness only.
- **Chart type matters more than design polish.** Wrong chart (pie for time-series) kills credibility regardless of visual quality.
- **Color-vision accessibility** — avoid red/green for binary distinctions (8% of men colorblind). Use blue/orange or shape differentiation.
- **Mobile-readable headline** — 36pt+ at thumbnail size for feed posts.
- **Source citation = E-E-A-T signal.** Pinterest and Google Image Search downrank uncited infographics.
- **Don't repurpose square infographic to Pinterest** — Pinterest pin aspect is 2:3 vertical. Use Recipe 7 for proper resize, not stretching.
- **Lead-magnet PDF size matters** — under 5MB for email-friendly download. Compress images at export.
- **Update cadence for evergreen infographics** — yearly refresh keeps the stat citations current and signals SEO freshness.
- **Don't overload with data points** — 3-7 is the cognitive sweet spot. 10+ becomes scroll fatigue.
- **One typeface family per infographic** — don't mix more than 2 fonts (1 headline + 1 body).
- **Iconography consistency** — use one icon set throughout; mixing flat + outlined + colored icons looks unprofessional.

## Sources

- [Best infographic generators 2026](https://washingtoncitypaper.com/article/782752/top-infographic-generators-in-2026/)
- [Piktochart — Canva alternatives](https://piktochart.com/blog/canva-alternatives/)
- [Piktochart](https://piktochart.com/)
- [Canva MCP](https://www.canva.com/developers/)
- [Visme](https://www.visme.co/)
- [Adobe Express](https://www.adobe.com/express/)
- [WCAG color-contrast accessibility](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)
- [E-E-A-T Google quality guidelines](https://developers.google.com/search/blog/2022/12/google-raters-guidelines-e-e-a-t)
