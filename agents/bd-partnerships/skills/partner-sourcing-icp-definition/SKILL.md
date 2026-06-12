<!--
Source: https://data.crunchbase.com/docs + https://docs.apollo.io/reference/organization-search + https://pitchbook.com/api
Partner ICP (PICP) scoring + Crunchbase/Apollo/LinkedIn waterfall sourcing (June 2026).
-->
# Partner Sourcing + ICP Definition — SKILL

Take a partner motion (referral / affiliate / channel / integration / OEM) and a sourcing mandate; produce a scored, ranked pipeline of candidate partners. Defines **Partner ICP (PICP)** along five axes (customer overlap, tech-stack fit, geography, segment, motion fit) and runs a waterfall across Crunchbase, Pitchbook, Apollo, LinkedIn Sales Navigator, G2, and BuiltWith.

## When to use

- **New partner program kickoff** — define PICP first, source second; never source without a scored rubric.
- **Quarterly pipeline refresh** — re-score and prune the existing pipeline; add new candidates.
- **Vertical / geo expansion** — adjust PICP weights for new ICP, re-source for that vertical.
- **Champion-mover follow-up** — a partner contact moves jobs; research the new company.
- **Trigger phrases**: "find partners for X", "build a partner pipeline", "who are our ICP partners", "score these 50 partners", "PICP rubric", "complementary tech stack to ours".

Do NOT use this skill for: **direct-sales prospects** (use `sales-agent`'s `account-research-deep`); **drafting the partnership agreement** (use `referral-affiliate-channel-oem-agreement-structuring`); **post-signed partner onboarding** (use `partner-onboarding-90-day-plan`).

## Setup

```bash
# Managed OAuth via Maton (preferred for solo founders)
export MATON_API_KEY="<key>"

# Direct API keys (fallback)
export APOLLO_API_KEY="<key>"          # Apollo: $99/mo Pro, $149 Org, custom Enterprise
export CRUNCHBASE_API_KEY="<key>"      # Crunchbase Enterprise $5k+/yr; Basic API free with attribution
export PITCHBOOK_API_KEY="<key>"       # Pitchbook quote-only; $15k+/yr typical
export BUILTWITH_API_KEY="<key>"       # $295/mo Pro
export BRAVE_API_KEY="<key>"
# LinkedIn Sales Navigator: $99-149/mo per seat — used via linkedin default skill + brightdata-mcp
```

PICP scoring runs locally; sourcing pulls hit the data providers. Free fallback: brave-search + manual LinkedIn.

## Common recipes

### Recipe 1: PICP rubric definition (write to Notion first)

```yaml
# Partner ICP — example for integration partner motion (B2B SaaS)
weights:
  customer_overlap: 25
  tech_stack_fit: 25
  geography: 15
  segment: 15
  motion_fit: 20
thresholds:
  enter_pipeline: 70
  light_touch: 50
  decline: 0
axes:
  customer_overlap:
    100: "Same ICP, same segment, same geo"
    75:  "Strong overlap"
    50:  "Partial overlap"
    25:  "Adjacent ICP"
    0:   "Different ICP"
  tech_stack_fit:
    100: "Pre-existing integration interest + adjacent in customer stacks"
    75:  "Complementary"
    50:  "Neutral"
    25:  "Risk of cannibalization"
    0:   "Direct competitor"
```

Render via `notion-mcp` so the scoring is auditable.

### Recipe 2: Crunchbase organization search (funded mid-market candidates)

```bash
# Crunchbase API v4 — organization search by industry + funding + size
curl -X POST "https://api.crunchbase.com/api/v4/searches/organizations" \
  -H "X-cb-user-key: $CRUNCHBASE_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "field_ids":["identifier","short_description","website_url","categories","funding_total","num_employees_enum","location_identifiers"],
    "query":[
      {"type":"predicate","field_id":"category_groups","operator_id":"includes","values":["software"]},
      {"type":"predicate","field_id":"num_employees_enum","operator_id":"includes","values":["c_51_100","c_101_250","c_251_500"]},
      {"type":"predicate","field_id":"location_identifiers","operator_id":"includes","values":["6106f5dc-823e-5da8-40d7-51612c0b2c4e"]},
      {"type":"predicate","field_id":"funding_total","operator_id":"gte","values":[10000000]}
    ],
    "order":[{"field_id":"rank_org","sort":"asc"}],
    "limit":50
  }'
```

Field IDs and operators documented at https://data.crunchbase.com/docs/using-the-api. Location UUIDs: query `/searches/locations` once and cache.

### Recipe 3: Apollo organization search (richer firmographics + tech-stack)

```bash
# Apollo mixed-companies search via api-gateway
curl -X POST "https://gateway.maton.ai/apollo/api/v1/mixed_companies/search" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "q_organization_keyword_tags":["marketing automation","CDP","attribution"],
    "organization_num_employees_ranges":["51,200","201,500"],
    "organization_locations":["United States","United Kingdom","Canada"],
    "currently_using_any_of_technology_uids":["hubspot","salesforce"],
    "page":1,
    "per_page":50
  }'
```

`currently_using_any_of_technology_uids` is gold for tech-stack-complementary partner sourcing. Reference: https://docs.apollo.io/reference/organization-search.

### Recipe 4: Apollo organization enrichment (per-domain deep)

```bash
curl "https://gateway.maton.ai/apollo/api/v1/organizations/enrich?domain=hubspot.com" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq '{
    name, industry, size: .organization.estimated_num_employees,
    revenue: .organization.annual_revenue_printed,
    tech: [.organization.technologies[]?.name],
    funding: .organization.latest_funding_stage,
    keywords: .organization.keywords
  }'
```

Doc: https://docs.apollo.io/reference/organization-enrichment.

### Recipe 5: Pitchbook private-company deep query

```bash
# Pitchbook Enterprise API — private company search; requires paid Pitchbook seat
curl -X POST "https://api-v2.pitchbook.com/companies/search" \
  -H "Authorization: Bearer $PITCHBOOK_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "primaryIndustryCodes":["SOFT"],
    "employeesMin":50,
    "employeesMax":500,
    "fundingTotalMin":10000000,
    "geographyCodes":["US","GB","CA"],
    "limit":100
  }'
```

Pitchbook is the strongest depth for private companies that aren't well-tracked in Crunchbase. Reference: https://pitchbook.com/api.

### Recipe 6: LinkedIn Sales Navigator partner search (via brightdata-mcp)

```python
# Sales Nav search filter — saved search URL
# Build via UI: Filter by Industry + Headcount + Geo + Years Founded + Keywords
search_url = "https://www.linkedin.com/sales/search/company?keywords=attribution&industryIncluded=4&headCountIncluded=C%2CD%2CE&geoIncluded=103644278"

# Scrape results via brightdata-mcp
# brightdata-mcp linkedin-sales-nav scrape -> save first 100 results
# Each result: company name, LinkedIn URL, industry, headcount, location
```

LinkedIn Sales Nav scraping requires Sales Nav seat + bright-data + careful rate limits. Direct API not publicly available; brightdata-mcp / Phantombuster are the SOTA paths.

### Recipe 7: G2 category neighbor discovery (no API — Playwright)

```python
# G2 has no public API for category browsing. Use playwright-mcp:
# 1. Navigate to https://www.g2.com/categories/<category-slug>
# 2. Extract: vendor name, average rating, # reviews, "Top Alternative" sidebar
# 3. Note that any vendor showing 4.0+ with 50+ reviews is a candidate partner
#    if PICP fit is high.

# In your skill orchestration:
# Use playwright-mcp open_page(...) + extract via CSS selectors
```

Reference: https://www.g2.com/categories.

### Recipe 8: BuiltWith adjacent-tech inference (who is already in our stack?)

```bash
# BuiltWith Lists API — find all companies using a specific tech
curl "https://api.builtwith.com/lists/sm/v15/api.json?KEY=$BUILTWITH_API_KEY&TECH=Segment&META=yes" | jq '.Lookup[] | {Domain, Vertical, Spend}'
```

If we sell to "companies using Segment", every Segment user with PICP fit is a candidate either for direct sales OR for a co-sell partner who is also Segment-integrated.

### Recipe 9: Clay multi-source waterfall (single call, full picture)

```bash
# Clay enrichment table — paste 200 domains, run waterfall:
# 1. Apollo enrich (firmographic + tech)
# 2. Crunchbase enrich (funding)
# 3. BuiltWith enrich (full tech stack)
# 4. LinkedIn employee count
# 5. Clearbit enrich (description + logo)
# Output: CSV of 200 fully-enriched candidate rows

# Trigger Clay table run via API
curl -X POST "https://gateway.maton.ai/clay/v1/tables/<table-id>/run" \
  -H "Authorization: Bearer $MATON_API_KEY"
```

Clay is the SOTA enrichment orchestrator — single table, hundreds of providers. Reference: https://clay.com/docs/api.

### Recipe 10: PICP scoring function (Python)

```python
def picp_score(p, weights):
    """Score 0-100 across 5 PICP axes."""
    score = 0

    # Customer overlap (default 25)
    overlap = p.get("customer_overlap_label", "different")
    overlap_pts = {"same_icp_segment_geo":100, "strong":75, "partial":50, "adjacent":25, "different":0}
    score += overlap_pts.get(overlap, 0) * weights["customer_overlap"] / 100

    # Tech-stack fit (default 25)
    tech = p.get("tech_stack_label", "neutral")
    tech_pts = {"integration_intent":100, "complementary":75, "neutral":50, "cannibalization_risk":25, "competitor":0}
    score += tech_pts.get(tech, 0) * weights["tech_stack_fit"] / 100

    # Geography (default 15)
    geo = p.get("geography_label", "no_overlap")
    geo_pts = {"same_primary_plus_expansion":100, "same_primary":75, "multi_region":50, "regional_only":25, "no_overlap":0}
    score += geo_pts.get(geo, 0) * weights["geography"] / 100

    # Segment (default 15)
    seg = p.get("segment_label", "different")
    seg_pts = {"same_seg_size_persona":100, "same_seg_size":75, "same_seg_broad":50, "adjacent":25, "different":0}
    score += seg_pts.get(seg, 0) * weights["segment"] / 100

    # Motion fit (default 20)
    motion = p.get("motion_label", "hostile")
    motion_pts = {"strong_both_sides":100, "strong":75, "acceptable":50, "awkward":25, "hostile":0}
    score += motion_pts.get(motion, 0) * weights["motion_fit"] / 100

    return round(score)
```

Calibrate weights by scoring 10 known-good and 10 known-bad partners; tune so good/bad separate at ≥ 20 points.

### Recipe 11: Bulk sourcing run (200 candidates → ranked pipeline → Notion)

```python
import requests, os, time, json

WEIGHTS = {"customer_overlap":25,"tech_stack_fit":25,"geography":15,"segment":15,"motion_fit":20}
DOMAINS = open("/tmp/candidate-domains.txt").read().splitlines()

results = []
for d in DOMAINS:
    apollo = requests.get(
        f"https://gateway.maton.ai/apollo/api/v1/organizations/enrich?domain={d}",
        headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"}
    ).json().get("organization", {})

    candidate = {
        "domain": d,
        "name": apollo.get("name"),
        "employees": apollo.get("estimated_num_employees", 0),
        "industry": apollo.get("industry"),
        "tech_stack": [t.get("name") for t in (apollo.get("technologies") or [])],
        "hq_country": (apollo.get("primary_country") or "US"),
        # Heuristic-label inference (replace with rules for your motion):
        "customer_overlap_label": "strong" if "B2B" in (apollo.get("keywords") or []) else "partial",
        "tech_stack_label": "complementary" if "HubSpot" in [t.get("name") for t in (apollo.get("technologies") or [])] else "neutral",
        "geography_label": "same_primary" if (apollo.get("primary_country")=="United States") else "regional_only",
        "segment_label": "same_seg_size" if 50 <= apollo.get("estimated_num_employees",0) <= 500 else "adjacent",
        "motion_label": "strong",
    }
    candidate["picp_score"] = picp_score(candidate, WEIGHTS)
    results.append(candidate)
    time.sleep(0.5)

# Filter, sort, post to Notion partner DB
ranked = sorted([r for r in results if r["picp_score"] >= 70], key=lambda x: -x["picp_score"])
print(f"{len(ranked)} candidates passed PICP >= 70.")
# Use notion-mcp to upsert each row into the partner DB.
```

### Recipe 12: Partner-pipeline render (Notion DB row template)

```yaml
partner:
  name: "Acme Analytics"
  domain: "acmeanalytics.com"
  picp_score: 86
  motion: "integration_partner"
  status: "pipeline"
  axes:
    customer_overlap: 90 ("same ICP, US mid-market SaaS")
    tech_stack_fit: 85 ("complementary — they're CDP, we're attribution")
    geography: 80 ("primary US, secondary UK")
    segment: 90 ("same segment, similar size band")
    motion_fit: 90 ("both-sides value: their customers want attribution")
  signals:
    - "$18M Series B closed Mar 2026 (Crunchbase)"
    - "Hired VP Partnerships ex-Segment, started Apr 2026 (LinkedIn)"
    - "Customer overlap: ~60 shared customers (Crossbeam est)"
  outreach_hypothesis: |
    Acme just funded with explicit "ecosystem expansion" in their PR.
    They sell to our exact ICP. Their CDP lacks attribution; our roadmap
    has a Segment-style CDP source. Co-sell motion likely; integration
    motion certain.
  suggested_first_meeting:
    target: "VP Partnerships (Sarah Lee)"
    channel: "LinkedIn warm intro via Crossbeam → CDP CEO connection"
    week: "Week of June 17"
  owner: "<partnerships-lead>"
  next_step: "Send connect → 15-min intro → joint customer count via Crossbeam"
```

## Examples

### Example 1: First-time partner sourcing for a new integration program

**Goal:** Solo founder launching an integration partner program; needs 20 viable candidates by end of week.

**Steps:**
1. Recipe 1 — Define PICP in Notion. Get stakeholder sign-off.
2. Recipe 3 — Apollo mixed-companies search filtered to ICP firmographic + uses-HubSpot. Pull 200 candidates.
3. Recipe 4 — Apollo enrich each domain (rate-limited loop, 200 × 0.5s ≈ 2 min).
4. Recipe 10 — Score each candidate.
5. Recipe 12 — Top 20 ranked to Notion partner DB.
6. Outreach kicked off by Day 3 with personalized "we already have N joint customers via Crossbeam" first-line.

**Result:** Friday morning, 20 PICP ≥ 70 candidates in pipeline; 4 first meetings booked the following week.

### Example 2: Quarterly pipeline refresh + prune

**Goal:** Existing partner pipeline of 80; 6 months old; needs re-score + 30 new adds.

**Steps:**
1. Pull all 80 from Notion partner DB.
2. Recipe 4 — Re-enrich each domain (stale firmographic data after 90 days).
3. Recipe 10 — Re-score under updated weights (we shifted focus to UK from CA — change `geography` weight + acceptable values).
4. Drop any that fell below 70; demote to "light touch" archive.
5. Recipe 2 + 3 — Source 60 new candidates → score → top 30 added.
6. Pipeline now: 60 active (50 refreshed + 10 new top-scorers), 30 light touch, 20 declined.

**Result:** Pipeline pruned, refreshed, and grown to 90; alignment with new geo focus.

### Example 3: Vertical expansion (FinTech) requires new PICP

**Goal:** Existing partner program is general SaaS; FinTech vertical launching; need 15 FinTech partners.

**Steps:**
1. Clone PICP rubric; modify weights: `customer_overlap → 35`, `geography → 25` (regulatory tight), `tech_stack_fit → 20`.
2. Recipe 2 — Crunchbase search filtered to `financial_services` + funding > $20M.
3. Recipe 5 — Pitchbook deep query for compliance-mature FinTech mid-market.
4. Recipe 6 — Sales Nav search for "VP Partnerships" titles at the 50 candidates.
5. Recipe 10 — Score each; output 15 ≥ 70 to Notion.
6. Hand off to outreach with FinTech-vertical messaging.

**Result:** FinTech partner pipeline launched with vertical-tuned PICP, not general.

## Edge cases / gotchas

- **PICP weights are opinionated; not universal.** A referral program weights `motion_fit` highest (incentive alignment); an integration program weights `tech_stack_fit` highest (technical complement). Don't reuse the same rubric across motions.
- **Crunchbase data lag.** Funding events publish 2-6 weeks late; private-company employee counts can be 6+ months stale. Cross-reference with Apollo + LinkedIn.
- **Apollo's tech-stack data is BuiltWith-sourced and stale** (30-60 day lag). For real-time tech-stack diff, query BuiltWith directly (Recipe 8).
- **Pitchbook is gated** — most usage is via the web UI; the API requires Enterprise contract and is rate-limited. Plan for batch nightly runs, not real-time.
- **LinkedIn Sales Nav scraping is fragile** — DOM changes monthly; bright-data is best, but rate-limit aggressively (1 search per 30s).
- **G2 has no public category-browse API** — Playwright scraping is the only path; selectors break monthly. Cache results.
- **Free-tier fallback** when no paid keys: `brave-search "<vertical> SaaS companies 50-500 employees"` + LinkedIn manual search; PICP scoring still applies.
- **PII regulation by region**: EU partner-contact data falls under GDPR; legitimate-interest basis documented. Apollo + LinkedIn allow opt-out; honor it.
- **"Strong overlap" inflation** — agents tend to over-score `customer_overlap` because most B2B SaaS sells to "tech companies." Force specificity: same SEGMENT + same SIZE BAND + same GEO.
- **De-duping** — same parent company under multiple subsidiary domains will pollute the pipeline. De-dupe by Crunchbase `entity_id` not by domain.
- **Cost discipline** — 200-account waterfall via Apollo + Crunchbase + BuiltWith can run $50-200 in API spend. Set hard daily budgets; cache enrichments 90 days.
- **Partner contact ≠ partner company.** PICP scores the company. After score, identify the right human contact via Apollo people search (recipe 4 in `account-research-deep`) — usually titled "VP Partnerships", "Head of BD", "Director Ecosystem", "Director Alliances".
- **Saturated category problem** — in categories with 100+ vendors (CRM, analytics), PICP yields too many candidates. Add a "strategic importance" tiebreaker: prefer category leaders (G2 top-3) over long-tail.

## Sources

- Crunchbase API v4: https://data.crunchbase.com/docs
- Apollo organization search: https://docs.apollo.io/reference/organization-search
- Apollo organization enrich: https://docs.apollo.io/reference/organization-enrichment
- Pitchbook API: https://pitchbook.com/api
- BuiltWith Lists API: https://api.builtwith.com/lists-api
- Clay API: https://clay.com/docs/api
- LinkedIn Sales Navigator: https://www.linkedin.com/help/sales-navigator/
- G2 categories: https://www.g2.com/categories
- Partner ICP methodology — Crossbeam: https://www.crossbeam.com/blog/the-partnership-economy/
- Tackle.io partner-sourcing playbook: https://tackle.io/state-of-cloud-marketplaces/
