<!--
Source: https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp
Source: https://docs.ahrefs.com/
Source: https://ahrefs.com/blog/parent-topic/
Depth: deep Ahrefs MCP cluster workflows beyond marketing-agent's surface keyword research
-->
# Ahrefs MCP — Deep Keyword + Cluster Research

## When to use

Reach for this skill when the user asks for: "keyword research at depth", "build cluster from Ahrefs", "intent-classified keywords", "keyword difficulty bulk score", "internal links per page via Ahrefs", "competitor organic keywords", "referring domains delta", "link velocity check", "broken backlinks list", "unlinked brand mentions". This is the depth specialist beyond marketing-agent's surface Ahrefs use — covers `keyword_difficulty_bulk` for 1000s of keywords, multi-country expansion, intent layering across `parent_topic`, internal link audit at URL-level, link-velocity anomaly detection.

## Setup

```bash
# Ahrefs remote MCP — OAuth at mcp.ahrefs.com
# Lite plan minimum ($129/mo); Standard ($249/mo) recommended for agent use
open https://mcp.ahrefs.com/oauth?client=craftbot
# Grant scopes: read:keywords, read:backlinks, read:content, write:projects

export AHREFS_MCP_TOKEN="<oauth-token>"
```

MCP server connection:
```json
{
  "ahrefs": {
    "transport": "https",
    "url": "https://mcp.ahrefs.com/v1",
    "auth": {"type":"bearer","token":"${AHREFS_MCP_TOKEN}"}
  }
}
```

Auth requirements:
- `AHREFS_MCP_TOKEN` — OAuth bearer; expires per Ahrefs cadence (renews via `oauth` flow)
- Plan tier: Lite ($129/mo, 500 credits) / Standard ($249/mo, 1500 credits) / Advanced ($449/mo, 5000 credits)

## Common recipes

### Recipe 1: Deep keyword research with intent + parent_topic + SERP features
```bash
mcp tool ahrefs.keywords_explorer \
  --keyword "marketing automation" \
  --country "US" \
  --limit 500 \
  --include_metrics '["volume","difficulty","intent","cpc","parent_topic","serp_features","global_volume","clicks_per_search","return_rate"]'
```
Returns up to 500 related keywords with `intent` (Informational/Commercial/Transactional/Navigational), `parent_topic` (Ahrefs' semantic group), `serp_features` (which SERP features dominate), `clicks_per_search` (how many of the searches result in a click — low = SERP-feature-stolen).

### Recipe 2: Keyword difficulty bulk for an entire cluster (100s of keywords)
```bash
mcp tool ahrefs.keyword_difficulty_bulk \
  --keywords_file "@/tmp/cluster-kws.txt" \
  --country "US" \
  --include_metrics '["difficulty","volume","intent","parent_topic"]'
```
`keywords_file` accepts one keyword per line. Bulk endpoint uses fewer credits/keyword than individual `keywords_explorer` calls.

### Recipe 3: Multi-country expansion (one seed → 5 markets)
```bash
for COUNTRY in US UK CA AU IN; do
  mcp tool ahrefs.keywords_explorer \
    --keyword "best CRM software" \
    --country "$COUNTRY" \
    --limit 100 \
    --include_metrics '["volume","difficulty","intent","parent_topic"]' \
    > "kws-$COUNTRY.json"
done
```
Outputs per-country volume splits — feeds hreflang planning + market prioritization.

### Recipe 4: Site Explorer overview (own + competitor benchmark)
```bash
mcp tool ahrefs.site_explorer \
  --target "example.com" \
  --mode "overview" \
  --metrics '["dr","ur","organic_keywords","organic_traffic","organic_traffic_value","referring_domains","referring_domains_dr_30_plus","backlinks"]'
```
DR (Domain Rating) / UR (URL Rating) anchor your authority baseline. Run for own domain + 3-5 competitors before any cluster planning.

### Recipe 5: Competitor organic keywords (winners list)
```bash
mcp tool ahrefs.site_explorer \
  --target "competitor.com" \
  --mode "organic_keywords" \
  --filter '{"position":{"between":[1,10]},"volume":{">=":500},"kd":{"<=":50}}' \
  --limit 1000 \
  --sort "traffic_desc"
```
Surfaces keywords competitor ranks top-10 for with reasonable difficulty + volume. Pair with `content_gap` for "keywords competitor has, you don't".

### Recipe 6: Internal link audit (URL-level inbound link map)
```bash
mcp tool ahrefs.internal_links \
  --target "example.com/page-to-audit" \
  --mode "inbound" \
  --include_metrics '["source_url","anchor_text","link_type","is_dofollow","traffic"]'
```
Returns every internal page linking TO a given URL with anchor text. Feed into `internal-linking-strategy-orphan-hub-spoke` skill for anchor diversity scoring + hub-spoke verification.

### Recipe 7: Broken backlinks (reclamation prospect list)
```bash
# Links you used to have that are now 404
mcp tool ahrefs.broken_backlinks_lost \
  --target "yourbrand.com" \
  --mode "domain" \
  --limit 1000 \
  --filter '{"first_seen":{"after":"2024-01-01"}}'

# Broken links pointing to competitor pages (offer your equivalent)
mcp tool ahrefs.broken_backlinks \
  --target "competitor.com" \
  --mode "domain" \
  --limit 1000 \
  --filter '{"ref_domain_dr":{">=":30}}'
```
Pair with `link-building-outreach-pitchbox-respona` skill for outreach automation.

### Recipe 8: Unlinked brand mention list
```bash
mcp tool ahrefs.content_explorer \
  --query "\"yourbrand\"" \
  --filter '{"links_to":"-yourbrand.com","language":"en","domain_rating":">30","mentions_per_target":">=1"}' \
  --limit 500 \
  --sort "domain_rating_desc"
```
Pages mentioning your brand without linking. Filter `dr >30` to skip low-quality prospects.

### Recipe 9: Referring domains new/lost (link velocity monitoring)
```bash
# New RDs in last 7 days
mcp tool ahrefs.referring_domains_new \
  --target "yourbrand.com" \
  --since "$(date -d '7 days ago' +%Y-%m-%d)" \
  --include_metrics '["domain","first_seen","dr","traffic","links_count"]'

# Lost RDs
mcp tool ahrefs.referring_domains \
  --target "yourbrand.com" \
  --mode "lost" \
  --since "$(date -d '7 days ago' +%Y-%m-%d)"
```
Flag negative-SEO patterns: >10× normal new-RD velocity from spam TLDs (.xyz, .top, .icu) signals an attack — escalate to disavow consideration (rarely warranted, see `role.md` "Antipattern 6").

### Recipe 10: SERP comparison for cluster borderline pairs
```bash
mcp tool ahrefs.serp_comparison \
  --keywords '["best running shoes 2026","running shoes 2026 review"]' \
  --country "US" \
  --include_metrics '["overlap_count","overlap_percent","common_urls"]'
```
Returns SERP overlap % between two keywords. ≥40% → semantically equivalent → consolidate into one cluster pillar; <40% → separate intents → keep as distinct cluster.

### Recipe 11: Rank tracker (long-running monitoring)
```bash
# Add cluster keywords to rank tracker
mcp tool ahrefs.rank_tracker \
  --action "add_keywords" \
  --project_id "<project-uuid>" \
  --keywords '["primary kw","supporting kw1","supporting kw2"]' \
  --frequency "weekly" \
  --countries '["US","UK"]' \
  --tags '["pillar","cluster-a"]'

# Pull historical positions
mcp tool ahrefs.rank_tracker \
  --action "get_history" \
  --project_id "<project-uuid>" \
  --date_range "last_90_days" \
  --group_by "tag"
```
Weekly cadence sufficient for organic; daily wastes credits.

### Recipe 12: Anchor Diversification Pattern check
```python
import pandas as pd

# Pull all inbound to a URL
inbound = ahrefs.internal_links(target='example.com/cluster-pillar', mode='inbound', limit=1000)

# Anchor distribution
df = pd.DataFrame(inbound)
anchor_dist = df['anchor_text'].value_counts(normalize=True)

# Flag if any single anchor >25% — over-optimized
over_optimized = anchor_dist[anchor_dist > 0.25]
print(f"Over-optimized anchors: {over_optimized.to_dict()}")

# Healthy distribution: top anchor 15-25%, long tail diverse
# Anchor types: exact match, partial match, branded, naked URL, generic ("click here"), image alt
```
Anchor Diversification Pattern: no single anchor text >25% on internal links to one URL; sprinkle branded + generic + naked-URL anchors to look natural.

## Examples

### Example 1: Build cluster architecture for "marketing automation" topic
**Goal:** 1 pillar + 15 supporting pages with intent + difficulty + traffic projection.

**Steps:**
1. Recipe 1: `keyword "marketing automation"`, limit 500 → seed set.
2. Group by `parent_topic` → first-pass clusters.
3. Recipe 2: `keyword_difficulty_bulk` for top 100 kws → KD scores.
4. Filter: volume ≥ 500, KD ≤ 50, intent in [Informational, Commercial].
5. Designate pillar = highest-volume head term in dominant `parent_topic`.
6. Recipe 10: SERP comparison for borderline pairs to merge/split.
7. Output Notion DB via `notion-mcp` (schema in `role.md` "Cluster architecture deliverable").

**Result:** Cluster Notion DB with pillar + 15 supporting URLs, primary keyword per page, projected traffic.

### Example 2: Pre-engagement competitive intelligence
**Goal:** Identify the 3 top competitors + their winning keywords + your gaps.

**Steps:**
1. Recipe 4: own domain `site_explorer` overview → baseline DR / RDs / organic traffic.
2. Identify 3 competitors via `site_explorer` mode `competing_domains`.
3. Recipe 4 × 3 for each competitor → benchmark deltas.
4. Recipe 5 per competitor → their top-10 winning kws.
5. `content_gap` (see `content-gap-analysis-competitive` skill) → kws all 3 rank for, you don't.
6. Pair with `internal-linking-strategy-orphan-hub-spoke` for internal link audit.

**Result:** Competitive deck slide + opportunity backlog.

### Example 3: Link-velocity anomaly investigation
**Goal:** Diagnose sudden traffic drop — is it a Google update or a negative-SEO attack?

**Steps:**
1. Recipe 9: new RDs in last 14 days vs trailing 90-day baseline.
2. If new RDs >10× baseline AND avg DR <10 AND TLDs in [.xyz, .top, .icu]: negative-SEO pattern.
3. Otherwise: cross-check Google update tracker (Sistrix / Semrush Sensor / mozcast.com).
4. If neg-SEO confirmed AND manual action received: build disavow file (rare).

**Result:** Diagnostic with recommendation (disavow / wait-out / take action).

## Edge cases / gotchas

- **Credit consumption** — `keywords_explorer limit=500` uses ~3-5 credits; bulk endpoints (`keyword_difficulty_bulk`) ~0.5 credit/keyword. Monitor at https://ahrefs.com/api/dashboard.
- **Intent classification 80% accurate** — Ahrefs intent is heuristic. For high-stakes decisions cross-check via SERP features (shopping ads + product listings = transactional; PAA dominant = informational).
- **`global_volume` vs country `volume`** — `global_volume` sums all tracked countries; use for multi-region opportunity sizing.
- **KD calibration** — KD 0-30 winnable for new sites; 30-60 needs DR>40; 60+ needs DR>60 + topical authority.
- **Rate limit 100 req/min per token** — bulk endpoints respect this.
- **Ahrefs vs GSC volume conflicts** — GSC reports actual impressions for queries Google attributes; Ahrefs estimates volume. Always validate top opps against GSC via `suganthan-gsc-cannibalization-decay-indexing`.
- **Weekly data refresh** — keyword volume + KD update weekly. Cache responses 24-48h; don't re-call same keyword multiple times/day.
- **`parent_topic` lag for new keywords** — keywords <30 days old may have null `parent_topic`. Re-poll after 30 days.
- **`content_explorer mentions_per_target`** — set ≥1 to avoid noise from passing mentions; set ≥3 for high-signal prospects.
- **DataForSEO cheap alt** — when Ahrefs paid tier unavailable, use DataForSEO `keywords_data/google/keyword_suggestions/live` at $0.0006/keyword (no intent classification, no `parent_topic`, no internal links).

## Sources

- [Ahrefs MCP getting started](https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp)
- [Ahrefs API reference](https://docs.ahrefs.com/)
- [Ahrefs parent_topic methodology](https://ahrefs.com/blog/parent-topic/)
- [Ahrefs search intent classification](https://ahrefs.com/blog/search-intent/)
- [Ahrefs KD calibration](https://ahrefs.com/blog/keyword-difficulty/)
- [DataForSEO cheap alt](https://docs.dataforseo.com/v3/keywords_data/google/keyword_suggestions/live/)
