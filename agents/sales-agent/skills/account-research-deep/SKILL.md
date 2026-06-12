<!--
Source: composite — Apollo + Clay + LinkedIn + BuiltWith + Crunchbase + brave-search
Deep account research with ICP scoring (June 2026).
-->
# Deep Account Research — SKILL

Take an account name (or domain), produce: firmographic profile, tech stack, recent triggers (funding / leadership / news / hiring), stakeholder candidates with personalization hooks, and an ICP fit score (0-100). Drives target-list creation, sequence enrollment, discovery prep, and multi-threading planning.

## When to use

- **Discovery prep** — 30-90 minutes before a discovery call.
- **Target-list build** — input ICP criteria → output 50-500 scored accounts.
- **ABM tier-1 deep-dive** — 25-50 accounts each getting 30-min research investment.
- **Champion-mover follow-up** — when a champion changes jobs, research the new company.
- **Trigger phrases**: "research <company>", "give me a brief on <account>", "find triggers at X", "what's their stack", "ICP fit score for these 50".

Do NOT use this skill for: **single-contact lookups** (use `apollo-clay-lead-enrichment`); **post-close customer research** (use `expansion-upsell-renewal-playbook`); **competitor research** (use `sales-enablement-battlecards-roi-calculators`).

## Setup

```bash
# Required keys
export MATON_API_KEY="<key>"          # for Apollo, Crunchbase, BuiltWith via gateway
export APOLLO_API_KEY="<direct-key>"  # if not using gateway
export CLAY_API_KEY="<clay-key>"      # for waterfall enrichment
export BRAVE_API_KEY="<brave-key>"    # for news + recent web mentions
export BUILTWITH_API_KEY="<key>"      # tech-stack — $295/mo Pro, $495/mo Enterprise

# Optional
export CRUNCHBASE_API_KEY="<key>"     # Crunchbase Enterprise $5k+/yr
# Playwright MCP for site browsing (no key needed)
```

## Common recipes

### Recipe 1: Apollo organization enrich (one-call snapshot)

```bash
curl -X GET "https://gateway.maton.ai/apollo/api/v1/organizations/enrich?domain=acme.com" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq '{
    name, industry, size: .estimated_num_employees, revenue: .annual_revenue_printed,
    funding_stage: .latest_funding_stage, last_round: .latest_funding_round_date,
    technologies: .technologies,
    locations: .locations,
    recent_news: .current_news[:5]
  }'
```

### Recipe 2: BuiltWith tech-stack lookup

```bash
curl -X GET "https://api.builtwith.com/v21/api.json?KEY=$BUILTWITH_API_KEY&LOOKUP=acme.com" | \
  jq '.Results[0].Result.Paths[0].Technologies[] | {Name, Categories, FirstDetected, LastDetected}'
```

Surfaces CRM, marketing automation, analytics, cloud provider, payment, ecommerce, dev tools. Compare to your "adjacent-tech-implies-need" list:

```yaml
# Example: signal we sell to companies with HubSpot + missing CRM-attribution tool
adjacent_signals:
  uses_hubspot_marketing: ["HubSpot", "Marketo", "Pardot"]
  uses_attribution: ["Bizible", "Dreamdata", "Hockeystack"]   # if any → less likely to need ours
  uses_analytics: ["Mixpanel", "Amplitude", "PostHog"]
```

### Recipe 3: LinkedIn employee + hiring signal (via api-gateway or Phantombuster)

```bash
# Via api-gateway if onboarded
curl -X GET "https://gateway.maton.ai/linkedin/v2/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity=urn:li:organization:<id>" \
  -H "Authorization: Bearer $MATON_API_KEY"

# Hiring signals: scrape /jobs/ via playwright-mcp
# Open https://www.linkedin.com/company/<slug>/jobs/
# Count open roles by function — expanding "demand-gen" hiring → buying-signal
```

### Recipe 4: Crunchbase funding webhook (or one-time lookup)

```bash
curl -X GET "https://api.crunchbase.com/api/v4/entities/organizations/acme?card_ids=raised_funding_rounds,key_employees" \
  -H "X-cb-user-key: $CRUNCHBASE_API_KEY" | jq '{
    funding_total: .properties.funding_total.value_usd,
    last_round: .cards.raised_funding_rounds.entities[0],
    key_employees: .cards.key_employees.entities[:5]
  }'
```

### Recipe 5: Brave Search — recent news (90-day window)

```bash
curl -X GET "https://api.search.brave.com/res/v1/news/search?q=%22Acme%22%20funding%20OR%20layoff%20OR%20launch&freshness=pm" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" | jq '.results[] | {title, url, description, age}'
```

`freshness=pm` returns past month; `pw` past week; `pd` past day.

### Recipe 6: Apollo people search at the company (stakeholder candidates)

```bash
curl -X POST "https://gateway.maton.ai/apollo/api/v1/mixed_people/search" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "organization_ids":["<apollo-org-id>"],
    "person_titles":["VP Sales","Head of Sales","Director Sales","RevOps","Chief Revenue Officer"],
    "person_seniorities":["c_suite","vp","director","head"],
    "per_page":25
  }'
```

Returns up to 25 candidates with title, LinkedIn URL, email_status. Cross-reference against existing CRM contacts to find net-new vs revisit.

### Recipe 7: ICP fit scoring (0-100 composite)

```python
def icp_score(account):
    score = 0

    # Firmographic (40 points)
    if 51 <= account["employees"] <= 500: score += 20
    elif 501 <= account["employees"] <= 2000: score += 15
    if account["industry"] in ("SaaS", "Technology", "Marketing"): score += 10
    if account.get("hq_country") in ("US", "UK", "CA"): score += 10

    # Pain-signal fit (30 points)
    if account.get("uses_competitor"): score += 15
    if account.get("hiring_target_function"): score += 10  # e.g., "demand-gen"
    if account.get("revenue_band") in ("$10-50M", "$50-200M"): score += 5

    # Tech-stack fit (20 points)
    if "HubSpot" in account.get("tech_stack", []): score += 10
    if "Snowflake" in account.get("tech_stack", []): score += 5
    if "Stripe" in account.get("tech_stack", []): score += 5

    # Trigger-event recency (10 points)
    days_since_trigger = account.get("days_since_trigger", 365)
    if days_since_trigger <= 30: score += 10
    elif days_since_trigger <= 90: score += 5

    return min(score, 100)
```

Per role.md threshold: ICP score >= 70 = enter sequence; 50-70 = nurture; < 50 = skip.

### Recipe 8: Hiring-signal heuristic (expanding teams = buying signal)

```python
# Pull LinkedIn jobs page via playwright-mcp, count by function
HIRING_FUNCTIONS = {
    "demand_generation": ["growth", "demand", "marketing operations"],
    "sales_development": ["SDR", "BDR", "outbound"],
    "rev_ops": ["revenue operations", "salesforce admin"],
    "engineering_target": ["platform engineer", "data engineer"],
}

def hiring_score(jobs_text):
    score = 0
    for fn, kws in HIRING_FUNCTIONS.items():
        if any(kw.lower() in jobs_text.lower() for kw in kws):
            score += 10
    return min(score, 30)
```

### Recipe 9: Account research brief (final render)

```yaml
# Output template — write to notion-mcp
account: "Acme Inc"
domain: acme.com
icp_score: 82
firmographic:
  industry: "SaaS"
  employees: 240
  revenue: "$25M ARR (estimated)"
  hq: "San Francisco, CA"
  funding: "Series B — $40M raised Jan 2026 (Insight Partners)"
tech_stack:
  - HubSpot (CRM + Marketing)
  - Snowflake (warehouse)
  - Segment (CDP)
  - Stripe (billing)
recent_triggers:
  - "Series B closed Jan 2026 (Crunchbase)"
  - "Hired VP Demand Gen, ex-Drift, started Mar 2026 (LinkedIn)"
  - "Posted 8 sales / growth roles in last 30 days"
stakeholders:
  - name: "Sarah Lee"
    title: "VP Sales"
    linkedin: "https://linkedin.com/in/sarahlee"
    hook: "Hiring SDR team aggressively"
    influence: "high"
  - name: "Alex Cruz"
    title: "Head of RevOps"
    linkedin: "https://linkedin.com/in/alexcruz"
    hook: "Posted on LinkedIn about pipeline visibility 2 weeks ago"
    influence: "medium"
hypothesis: |
  Acme just funded; aggressively hiring SDR; uses HubSpot. They likely need
  pipeline-visibility tooling to scale outbound from 5 to 25 reps. Our pitch:
  "we plug into HubSpot and surface MEDDIC + signal data so your new SDRs
  start scored / coached on day 1".
suggested_entry:
  channel: "LinkedIn DM to Sarah Lee"
  hook: "Saw your Series B + the 8 SDR job posts. Curious how you're handling pipeline visibility as the team scales."
  sequence: "Q3 — Series-B-Just-Funded"
```

### Recipe 10: Bulk ICP scoring (200 accounts in one pass)

```python
import requests, os, time
DOMAINS = open("/tmp/target-domains.txt").read().splitlines()

results = []
for d in DOMAINS:
    apollo = requests.get(
        f"https://gateway.maton.ai/apollo/api/v1/organizations/enrich?domain={d}",
        headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"},
    ).json().get("organization", {})

    bw = requests.get(
        f"https://api.builtwith.com/v21/api.json?KEY={os.environ['BUILTWITH_API_KEY']}&LOOKUP={d}",
    ).json()

    account = {
        "domain": d,
        "name": apollo.get("name"),
        "employees": apollo.get("estimated_num_employees", 0),
        "industry": apollo.get("industry"),
        "tech_stack": [t["name"] for t in (apollo.get("technologies") or [])],
        "days_since_trigger": 30,  # placeholder; pull from current_news
    }
    account["icp_score"] = icp_score(account)
    results.append(account)
    time.sleep(0.6)  # rate-limit padding

# Filter and sort
top = sorted([a for a in results if a["icp_score"] >= 70], key=lambda x: -x["icp_score"])
```

### Recipe 11: Personalization-hook miner

For each stakeholder, generate a 1-line hook tied to a real, recent event:

```python
HOOK_SOURCES = [
    "recent funding round",        # from Crunchbase / Apollo
    "leadership change",           # from LinkedIn job-change
    "product launch",              # from brave-search news
    "hiring spike in their team",  # from LinkedIn jobs
    "their own LinkedIn post",     # from LinkedIn /posts/
    "their podcast / interview",   # from brave-search
    "tech-stack addition",         # from BuiltWith diff
]

def best_hook(stakeholder, account):
    # priority: their own action > company action > industry trend
    if stakeholder.get("recent_linkedin_post"):
        return f"Saw your post on {stakeholder['recent_linkedin_post_topic']}"
    if account.get("funding_recent"):
        return f"Saw the {account['funding_stage']} round in {account['funding_month']}"
    if stakeholder.get("recently_started"):
        return f"Saw you joined {account['name']} from {stakeholder['prior_company']} — congrats"
    return f"Following {account['name']} for a while — caught {account['most_recent_news']}"
```

Hook quality matters more than enrichment depth — a thin but specific hook beats a comprehensive but generic one.

## Examples

### Example 1: 50-account target list for Q3 outbound

**Goal:** 50 enriched, scored, ranked accounts ready for the SDR team Monday.

**Steps:**
1. Apollo `people-search` filtered to ICP firmographic (Recipe 1 from `apollo-clay-lead-enrichment` for contacts).
2. For each unique company, Recipe 1 (Apollo enrich), Recipe 2 (BuiltWith stack), Recipe 4 (Crunchbase funding).
3. Recipe 7 (ICP score) per account; filter score >= 70.
4. Recipe 6 — pull 2-3 stakeholder candidates per top-50.
5. Recipe 11 — generate per-stakeholder hook.
6. Render via Recipe 9 to Notion page; CSV export for sequence load via `outreach-salesloft-sequences`.

**Result:** Monday morning, SDRs have 50 brief docs + ready-to-enroll contacts with personalized first lines.

### Example 2: Tier-1 ABM deep-dive (25 accounts, 30 min each)

**Goal:** Tier-1 list of 25 accounts gets human-grade research depth.

**Steps:**
1. Recipes 1-5 (all sources).
2. `playwright-mcp` browse their /careers/ + /blog/ + /about/ for context.
3. Brave Search recent podcast / interview appearances of stakeholders.
4. Render per-account brief to Notion; share with marketing-agent for paid ABM targeting.

**Result:** Marketing runs LinkedIn ABM + Meta retargeting on the same 25 accounts; sales runs 1:1 multi-thread; shared engagement dashboard.

## Edge cases / gotchas

- **Apollo's tech-stack data is BuiltWith-sourced and stale** — typically 30-60 days behind. For real-time stack diffs, query BuiltWith direct (Recipe 2).
- **BuiltWith only shows public-facing tech** (frontend, marketing tools, payment). It cannot see internal CRM, data warehouse, or HR systems — use LinkedIn job postings + adjacent-tech inference for those.
- **"Industry" labels are inconsistent** across Apollo / LinkedIn / Crunchbase — Acme might be "SaaS" in Apollo, "Computer Software" on LinkedIn, "Internet" on Crunchbase. Normalize to your own taxonomy.
- **Employee counts are estimates** — Apollo / LinkedIn often within 20%, but for stealth or newly-rebranded companies can be wildly off. Cross-reference with Crunchbase if it matters.
- **Stakeholder data drifts fast** — title changes, departures, lateral moves. Re-enrich a target list older than 60 days before re-engaging.
- **Hiring-page scraping is fragile** — LinkedIn changes the DOM; `playwright-mcp` selectors will break monthly. Prefer Apollo's job-change signals + LinkedIn job-search alerts.
- **Funding data is biased toward US / Europe** — APAC + emerging-market funding under-reported in Crunchbase / Apollo. For those regions add region-specific sources (Tracxn, DealStreetAsia).
- **PII regulation by region**: EU + UK PII has GDPR; California has CCPA. Storing stakeholder data for "research" without a legal basis is risky. Document a legitimate-interest basis or stick to non-EU data.
- **Cost discipline**: Apollo enrich is 1-2 credits per call; BuiltWith is $0.005 per lookup; Crunchbase is $0.05+. A 500-account research pass can cost $50-200. Set hard credit budgets per run.
- **"ICP score" inflation** — agents tend to score too generously. Calibrate by manually scoring 20 known-good and 20 known-bad accounts; tune weights so good/bad separate at >= 20 points.
- **No recent triggers ≠ bad account.** Some great-fit accounts are quiet for 6-12 months. Don't auto-disqualify on trigger-recency alone — give a base-score of 50 even for trigger-less accounts.

## Sources

- Apollo organization enrich API: https://docs.apollo.io/reference/organizations-enrich
- BuiltWith API: https://api.builtwith.com/
- Crunchbase API: https://data.crunchbase.com/
- Brave Search API: https://api.search.brave.com/app/documentation
- LinkedIn Sales Navigator help: https://www.linkedin.com/help/sales-navigator/
- "How to research accounts" — Gong: https://www.gong.io/blog/account-research/
- 2026 ICP scoring guide: https://www.demandbase.com/blog/icp-scoring-model/
