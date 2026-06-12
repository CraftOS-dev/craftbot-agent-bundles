<!--
Source: https://api.builtwith.com/ + https://clay.com/docs/api + https://crossbeam.com/blog/ecosystem-map/
Ecosystem mapping + tech-stack discovery via BuiltWith / Clay + DrawIO / Figma visualization (June 2026 SOTA).
-->
# Ecosystem Mapping + Tech-Stack Discovery — SKILL

Map your category's ecosystem (direct competitors, complementary tools, integrators, consultancies, resellers, marketplaces) and discover per-account tech stacks. Output: ecosystem map (DrawIO/Figma) + per-account tech-stack report. Drives partner sourcing, joint-GTM motion, account-research depth.

## When to use

- **Annual ecosystem refresh** — refresh ecosystem map; identify category shifts.
- **New vertical / geo expansion** — map ecosystem for new market.
- **Account-research depth** — identify prospect's tech-stack for partner-led entry.
- **Competitive landscape** — where do we sit vs alternatives.
- **Marketplace ecosystem map** — which marketplaces matter for our category.
- **Trigger phrases**: "ecosystem map", "tech stack of X", "BuiltWith for", "Clay enrichment", "category ecosystem", "complementary tools".

Do NOT use this skill for: **the actual partner sourcing** (use `partner-sourcing-icp-definition`); **direct-sales prospect research** (use `sales-agent`'s `account-research-deep`); **competitor battlecards** (defer to `marketing-agent` or `sales-agent`).

## Setup

```bash
export MATON_API_KEY="<key>"
export BUILTWITH_API_KEY="<key>"      # $295/mo Pro
export CLAY_API_KEY="<key>"           # via Maton: $149-499/mo Clay subscription
export BRAVE_API_KEY="<key>"
# drawio-mcp + figma-mcp + canva-mcp configured
# firecrawl-mcp for site crawling
```

## Common recipes

### Recipe 1: BuiltWith — per-domain tech-stack lookup

```bash
curl "https://api.builtwith.com/v21/api.json?KEY=$BUILTWITH_API_KEY&LOOKUP=acme.com" | jq '.Results[0].Result.Paths[0].Technologies[] | {
    Name, Categories, FirstDetected, LastDetected, IsPremium
  }'
```

Returns: CRM, marketing automation, analytics, payment, ecommerce, cloud provider, dev tools, web framework, frontend lib. Reference: https://api.builtwith.com/.

### Recipe 2: BuiltWith — find all companies using specific tech (Lists API)

```bash
# All companies using Segment
curl "https://api.builtwith.com/lists/sm/v15/api.json?KEY=$BUILTWITH_API_KEY&TECH=Segment&META=yes" | jq '.Lookup[] | {Domain, Vertical, Spend, EmployeeCount}'

# All companies that ADDED Stripe in last 30 days
curl "https://api.builtwith.com/lists/sm/v15/api.json?KEY=$BUILTWITH_API_KEY&TECH=Stripe&SINCE=2026-05-01" | jq '.Lookup[]'
```

Useful for: identify prospects who recently adopted a complementary tech (buying signal).

### Recipe 3: BuiltWith — bulk per-domain (cached, 90-day TTL)

```python
import requests, os, time, json
from pathlib import Path

cache_dir = Path("/tmp/builtwith-cache")
cache_dir.mkdir(exist_ok=True)

def tech_stack(domain, max_age_days=90):
    cache_file = cache_dir / f"{domain}.json"
    if cache_file.exists() and (time.time() - cache_file.stat().st_mtime) < max_age_days * 86400:
        return json.load(cache_file.open())
    r = requests.get(f"https://api.builtwith.com/v21/api.json?KEY={os.environ['BUILTWITH_API_KEY']}&LOOKUP={domain}")
    data = r.json()
    json.dump(data, cache_file.open("w"))
    return data

# Bulk run
domains = open("/tmp/prospect-domains.txt").read().splitlines()
results = []
for d in domains:
    techs = [t["Name"] for t in tech_stack(d).get("Results",[{}])[0].get("Result",{}).get("Paths",[{}])[0].get("Technologies",[])]
    results.append({"domain": d, "techs": techs})
    time.sleep(0.6)  # respect rate limit

# Find prospects using complementary tool
hubspot_users = [r for r in results if "HubSpot" in r["techs"]]
```

### Recipe 4: Clay multi-source waterfall

```bash
# Trigger Clay table run
curl -X POST "https://gateway.maton.ai/clay/v1/tables/<table-id>/run" \
  -H "Authorization: Bearer $MATON_API_KEY"
```

Clay setup (one-time, in Clay UI):
- Input: 200 domains pasted
- Enrichment waterfall: Apollo → Crunchbase → BuiltWith → LinkedIn → Clearbit
- Output: full firmographic + tech-stack + funding + key contacts per row

Reference: https://clay.com/docs/api.

### Recipe 5: Category ecosystem map (DrawIO)

```yaml
ecosystem_map:
  category: "Revenue Operations (RevOps)"
  date: "2026-06-15"

  central_node: "Brand"

  zones:
    competitors:
      direct: ["Clari","Gong","Salesloft","Outreach","BoostUp"]
      indirect: ["Salesforce native","HubSpot native"]
    complementary:
      crm: ["HubSpot","Salesforce","Pipedrive","Attio"]
      marketing_automation: ["Marketo","Pardot","HubSpot"]
      data_platforms: ["Segment","Rudderstack","mParticle"]
      revenue_intelligence: ["Gong","Chorus","Salesloft"]
      analytics: ["Looker","Tableau","Mode","Hex"]
    integrators_consultancies:
      - "Sigma Partners","RevOps Co-op","Atrium","Demand Gen Co"
    resellers:
      - "Bluewolf (IBM)","Slalom","Deloitte Digital"
    marketplaces:
      - "Salesforce AppExchange","HubSpot App Marketplace","Slack App Directory","Atlassian Marketplace"

  partnership_relationships:
    brand_with_hubspot: "Integration partner; AppExchange listing"
    brand_with_salesforce: "Integration partner; AppExchange listing in progress"
    brand_with_segment: "Integration partner"
    brand_with_gong: "Co-marketing; no formal integration yet"
    brand_with_bluewolf: "Reseller agreement; Gold tier"

  gaps_opportunities:
    - "No Salesforce reseller yet — explore"
    - "No data platform partner in EU"
    - "Underexposed at AWS re:Invent ecosystem"
```

### Recipe 6: DrawIO ecosystem map render (programmatic)

```python
# drawio-mcp can render from XML schema OR use the MCP API
# Generate XML programmatically:
XML_TEMPLATE = """
<mxfile>
  <diagram name="Brand Ecosystem 2026">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- Central node -->
        <mxCell id="brand" value="Brand" style="rounded=1;fillColor=#1A2B3C;fontColor=#fff" vertex="1" parent="1">
          <mxGeometry x="400" y="300" width="100" height="60" as="geometry"/>
        </mxCell>
        <!-- Add other nodes programmatically -->
        {{NODES}}
        <!-- Add edges -->
        {{EDGES}}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

# Build nodes + edges from Recipe 5 YAML
# Write to drawio file or trigger drawio-mcp upload
```

Easier path: hand the YAML to `drawio-mcp` with a "render this ecosystem map" prompt; or use Figma for higher fidelity.

### Recipe 7: Per-prospect tech-stack report

```yaml
prospect: "Globex Corp"
domain: "globex.com"
date: "2026-06-15"

tech_stack:
  crm: ["HubSpot"]
  marketing: ["Marketo","Drift","Outreach"]
  cdp: ["Segment"]
  analytics: ["Mixpanel","Heap"]
  cloud: ["AWS","Cloudflare"]
  payment: ["Stripe"]
  data_warehouse: ["Snowflake"]
  collaboration: ["Slack","Notion"]
  design: ["Figma"]
  hr: ["Workday"]

partner_overlap:
  hubspot: "Brand integration listed on HubSpot App Marketplace — easy entry"
  segment: "Brand integration partner — joint customer story available"
  stripe: "Brand on Stripe Marketplace — billing integration possible"
  slack: "Brand Slack App in App Directory — immediate slack-based delivery"

partner_led_entry:
  primary: "HubSpot — customer of HubSpot; Brand's HubSpot listing is the natural entry"
  secondary: "Segment — joint customer story (FreshDirect) shows Globex peer adoption"

recent_tech_changes:
  - "Added Segment in March 2026 (BuiltWith first-detected)"
  - "Added Snowflake in Jan 2026"
  - "Decommissioned Pardot Sept 2025"

hypothesis: |
  Globex just adopted modern CDP + data warehouse (Segment + Snowflake) in 2026.
  Likely overhauling revenue stack. Now is buying-window for revenue-intelligence layer.
  Best entry: partner-led via HubSpot or Segment introduction.
```

### Recipe 8: Adjacent-tech-implies-need rules

```yaml
# Map tech to buying-signal
tech_implies_need:
  uses_HubSpot_and_no_attribution: ["Bizible","Dreamdata","Hockeystack","Brand"]  # we sell attribution
  uses_Segment_and_no_dashboard: "RevOps platform candidate"
  uses_Mixpanel_AND_HubSpot: "Probably has data silos — revenue ops opportunity"
  uses_Snowflake_AND_recent: "Data-mature buyer; sophisticated buying motion"
  uses_Stripe_AND_marketplace: "Cross-sell candidate — Stripe Marketplace channel"

partner_signals:
  uses_Segment: "Segment integration partner Brand can warm intro"
  uses_Salesforce_AND_Slack: "Bluewolf reseller could engage; joint pursuit"
  uses_HubSpot_AND_smaller: "HubSpot Solutions Partner can resell Brand"
```

### Recipe 9: Firecrawl ecosystem map auto-discovery

```bash
# Use firecrawl-mcp to crawl category-leading sites for partner directories
# E.g., HubSpot Solutions Partner directory
curl -X POST "https://gateway.maton.ai/firecrawl/v1/crawl" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "url":"https://ecosystem.hubspot.com/marketplace/agencies",
    "limit":500,
    "extract":{
      "fields":["agency_name","tier","specializations","location","website","customer_count"]
    }
  }'
```

Returns structured ecosystem data; output to `notion-mcp` partner-research DB.

### Recipe 10: G2 category-neighbor extraction (Playwright)

```python
# G2 doesn't have public API; scrape via playwright-mcp
# Open https://www.g2.com/categories/revenue-operations-platforms
# Extract: vendor name, rating, # reviews, "Top Alternatives" sidebar
# Each 4.0+ rated vendor with 50+ reviews is a candidate partner OR competitor

# In playwright-mcp:
# 1. open_page https://www.g2.com/categories/<slug>
# 2. wait_for_selector ".product-card"
# 3. extract via CSS selectors
```

### Recipe 11: Marketplace ecosystem discovery (per platform)

```yaml
marketplace_discovery:
  hubspot_app_marketplace:
    url: "https://ecosystem.hubspot.com/marketplace/apps/sales-revops"
    method: "firecrawl-mcp + parse list pages"
    extract: ["app_name","installs","rating","reviews","category"]

  salesforce_appexchange:
    url: "https://appexchange.salesforce.com/category/<slug>"
    method: "firecrawl-mcp"
    extract: ["app_name","rating","reviews","price_model"]

  shopify_app_store:
    url: "https://apps.shopify.com/categories/<slug>"
    method: "firecrawl-mcp"
    extract: ["app_name","rating","reviews","developer"]
```

### Recipe 12: Figma-rendered ecosystem map (high-fidelity)

```yaml
figma_ecosystem_map:
  use_case: "Marketing collateral — joint sales deck or PAB pre-read"
  steps:
    - "Hand to figma-mcp with YAML from Recipe 5"
    - "Use Figma's existing 'ecosystem map' component if available"
    - "Categorize zones: competitors (red zone), complementary (green), partners (blue)"
    - "Export PNG + Figma share link"
  alternative: "canva-mcp 'company ecosystem' template for SMB BD"
```

## Examples

### Example 1: Quarterly ecosystem map refresh

**Goal:** Update RevOps ecosystem map for FY2026 strategy session.

**Steps:**
1. Recipe 5 — Refresh ecosystem YAML; identify new competitors, partner shifts.
2. Recipe 10 — G2 scan; add new entrants to map.
3. Recipe 9 — Firecrawl HubSpot Solutions Partners directory; add any new specialists in our category.
4. Recipe 6 / 12 — Render new map.
5. Distribute to leadership; identify 3 partnership opportunities and 1 competitive concern.

**Result:** Annual ecosystem refresh; strategic clarity for next-quarter motion.

### Example 2: Account-research depth for ABM tier-1

**Goal:** 25 ABM tier-1 accounts; need tech-stack + partner-led-entry for each.

**Steps:**
1. Recipe 3 — Bulk BuiltWith; cache per account.
2. Recipe 7 — Per-account tech-stack report.
3. Recipe 8 — Apply implies-need rules.
4. Recipe 4 — Clay enrichment for stakeholder layer.
5. Output: per-account 1-pager for AE; partner-led-entry recommendation; hypothesis.

**Result:** ABM tier-1 has partner-led entry plan; conversion 2-3x vs cold ABM.

### Example 3: New geo expansion (EMEA) ecosystem map

**Goal:** Brand entering EMEA; map UK + DE + FR ecosystem.

**Steps:**
1. Recipe 5 — Build EMEA-specific ecosystem YAML.
2. Recipe 1 — Tech-stack survey of EMEA SaaS leaders.
3. Recipe 9 — Firecrawl EMEA-specific partner directories.
4. Cross-check with Reveal account mapping for EU-specific overlap.
5. Recipe 12 — Render EMEA ecosystem map for leadership.

**Result:** EMEA expansion has informed partner-acquisition plan; first 5 EMEA partners identified.

## Edge cases / gotchas

- **BuiltWith only sees public-facing tech** — frontend, payment, marketing. Cannot see internal CRM, data warehouse, HR. Use LinkedIn job postings + adjacent-tech inference.
- **BuiltWith data staleness** — first-detected can be 30-90 days late. Cross-check with company changelog / press.
- **Wappalyzer + Hunter** as BuiltWith alternatives — cheaper but less comprehensive.
- **Apollo's tech-stack is BuiltWith-sourced and ~30 days stale** — for real-time, query BuiltWith direct.
- **Clay rate limits** — 200 enrichments/min on Pro tier; 1000/min Enterprise. Batch sensibly.
- **Stale ecosystem map** — 6-month-old map is dangerous. Refresh quarterly minimum.
- **Competitor classification subjectivity** — some "competitors" are actually category-leaders for adjacent segments. Be precise.
- **Marketplace listing data** — many marketplaces hide install counts; show only "many" or "1000+." Crawl-fragile.
- **G2 selectors break** — DOM changes monthly. Maintain Playwright selectors.
- **HubSpot Solutions Partner directory** — public but rate-limited; respect robots.txt.
- **Salesforce ISV directory** — public; less rate-restricted; deeper data.
- **EU GDPR + tech-stack scraping** — most tech-stack APIs (BuiltWith, Apollo, Clay) lawful in B2B context, but EU-specific firms may have opt-out.
- **Cost discipline** — 500-account BuiltWith run = $250; Clay enrichment = $50-200; budget per discovery cycle.
- **Per-category granularity** — RevOps ecosystem ≠ Marketing Automation ecosystem. Build separately if relevant.
- **Acquired companies** — Pardot now part of Salesforce Marketing Cloud. Update map; can change partner positioning.
- **DrawIO vs Figma vs Canva**:
  - DrawIO — fastest, programmatic, internal use
  - Figma — best fidelity, designer-friendly, partner-facing
  - Canva — fast, template-driven, marketing-team-friendly
- **Map sharing** — internal ecosystem map can be competitively sensitive; don't share publicly. Marketing-facing version is sanitized.
- **Map storage** — Figma file + DrawIO XML + Notion narrative all needed. Single-source-of-truth in Notion; renders in Figma/DrawIO.
- **Map versioning** — quarterly version; archive old versions for trend.

## Sources

- BuiltWith API: https://api.builtwith.com/
- BuiltWith Lists API: https://api.builtwith.com/lists-api
- Clay API: https://clay.com/docs/api
- Wappalyzer: https://www.wappalyzer.com/
- Crossbeam ecosystem map blog: https://crossbeam.com/blog/ecosystem-map/
- DrawIO docs: https://www.diagrams.net/doc/
- Figma docs: https://help.figma.com/
- Canva developer docs: https://www.canva.com/developers/
- Firecrawl API: https://docs.firecrawl.dev/
- HubSpot Solutions Partner directory: https://ecosystem.hubspot.com/marketplace/agencies
- Salesforce AppExchange: https://appexchange.salesforce.com/
- G2 category search: https://www.g2.com/categories
