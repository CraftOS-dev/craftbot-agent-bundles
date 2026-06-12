<!--
Sources: https://www.crunchbase.com/api
         https://www.apollo.io/product/api
         https://pipeline.zoominfo.com/sales/crunchbase-vs-apollo
         https://www.findymail.com/blog/best-email-finder-tools/
Crunchbase 4M+ private companies + predictive AI signals. Apollo 275M+ contacts +
company graph. Layoffs.fyi for high-intent passive signal.
-->
# Target Company Mapping — Crunchbase / LinkedIn / Apollo — SKILL

Build target-account lists via Crunchbase signal (funding stage + headcount + industry + layoff cross-reference), then per-company LinkedIn Sales Nav search for target roles, then Apollo contact enrichment. The pattern: company-first → role-first → contact-first.

## When to use

- User wants to **build a list of 20-100 target companies** for sourcing.
- User wants to **mine candidates from competitor companies** (similar stage / sector / scale).
- User wants to **layer layoff signal** for high-intent passive candidates.
- User wants to **enrich a candidate list with company-context** (funding, headcount, recent news).
- Trigger phrases: "target company list", "competitor sourcing", "Crunchbase search", "Apollo enrich", "layoffs signal", "account mapping", "company news in outreach".

Do not use for: individual exec sourcing (`cto-vp-eng-exec-sourcing` — exec workflow is different); diversity-channel sourcing (`diversity-channel-sourcing-dev-color-code2040`); GitHub-only candidate mining (`github-talent-mining-language-stars-commits`).

## Setup

```bash
# Crunchbase Enterprise API — paid tier $999+/mo for full graph.
# https://www.crunchbase.com/api
export CRUNCHBASE_API_KEY="xxx"

# Apollo.io — free tier covers MVP; paid tier ($79+/mo) for higher quotas.
# https://app.apollo.io/api
export APOLLO_API_KEY="xxx"

# LinkedIn Sales Navigator seat for per-company role search.
export LINKEDIN_SALES_NAV_SEAT="yes"

# Layoffs.fyi (free; no API — scrape via firecrawl-mcp).
# WARN database (state-mandated layoff notices) — also scrape.

# Optional: Glassdoor for rating + sentiment.
# Optional: G2 / Capterra for B2B product signal.
```

## Common recipes

### Recipe 1: Crunchbase signal pull (filter by funding stage + headcount + industry)

```bash
# Series B-D, 100-500 headcount, SaaS sector, US-based
curl -X POST "https://api.crunchbase.com/api/v4/searches/organizations" \
  -H "X-cb-user-key: $CRUNCHBASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "field_ids": ["identifier", "name", "short_description", "categories", "num_employees_enum", "last_funding_total", "last_funding_type", "founded_on"],
    "query": [
      {"type": "predicate", "field_id": "last_funding_type", "operator_id": "includes", "values": ["series_b", "series_c", "series_d"]},
      {"type": "predicate", "field_id": "num_employees_enum", "operator_id": "includes", "values": ["c_00101_00250", "c_00251_00500"]},
      {"type": "predicate", "field_id": "categories", "operator_id": "includes", "values": ["software", "saas"]},
      {"type": "predicate", "field_id": "location_identifiers", "operator_id": "includes", "values": ["united-states"]}
    ],
    "limit": 100
  }'
```

Crunchbase returns company-level data. Next: per-company LinkedIn search for target roles.

### Recipe 2: Recent-round signal (last 90 days)

```bash
# Companies that raised in last 90 days = scaling = hiring
curl -X POST "https://api.crunchbase.com/api/v4/searches/funding_rounds" \
  -H "X-cb-user-key: $CRUNCHBASE_API_KEY" \
  -d '{
    "field_ids": ["identifier", "funded_organization_identifier", "announced_on", "investment_type", "money_raised"],
    "query": [
      {"type": "predicate", "field_id": "announced_on", "operator_id": "gte", "values": ["2026-03-09"]},
      {"type": "predicate", "field_id": "investment_type", "operator_id": "includes", "values": ["series_b", "series_c", "series_d", "series_e"]}
    ],
    "order": [{"field_id": "announced_on", "sort": "desc"}],
    "limit": 100
  }'
```

Recent-funded companies are the highest-signal source — they're scaling, hiring, AND existing employees may be coast-to-coast on equity. Triple signal.

### Recipe 3: Layoff signal layer (Layoffs.fyi + WARN cross-reference)

```python
# Layoffs.fyi has no public API; scrape via firecrawl-mcp
# https://layoffs.fyi/

import firecrawl
client = firecrawl.FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])

# Scrape recent layoffs
layoffs = client.scrape_url("https://layoffs.fyi/", {
    "extract": {
        "schema": {
            "company": "string",
            "layoff_date": "date",
            "headcount_cut": "number",
            "percent_cut": "number"
        }
    }
})

# WARN database (US state-mandated 60-day layoff notices) — many state portals; consolidated at warntracker.com
warn = client.scrape_url("https://www.warntracker.com/", {...})

# Cross-reference: companies in YOUR target list (Recipe 1) that ALSO appear in layoffs = high-intent passive pool
target_companies = set(c["name"] for c in crunchbase_results)
laid_off_companies = set(l["company"] for l in layoffs)
high_intent = target_companies & laid_off_companies
```

Layoff signal = "current employees of company X are open to outreach right now even if passive". Highest-intent passive signal in 2026.

### Recipe 4: LinkedIn Sales Nav per-company role search

```
# Sales Nav saved search per target company:
# Filters: current_company={company}, current_title contains "{target_role}", tenure>1yr
# Layer: years_experience, function, geography

# Example: Source senior backend engs from each of 50 target companies
for company in TARGET_COMPANIES:
    sales_nav_url = (
        f"https://www.linkedin.com/sales/search/people?"
        f"currentCompany=urn:li:fs_company:{company['linkedin_id']}"
        f"&title=Senior%20Software%20Engineer%20OR%20Staff%20Software%20Engineer"
        f"&yearsCurrentCompany=1-5"
    )
    # Run via playwright-mcp if no Talent Solutions API access
    candidates = playwright.scrape(sales_nav_url)
```

Sales Nav saved searches let you batch-process 50+ target companies in parallel.

### Recipe 5: Apollo contact enrichment (the email + phone fill)

```bash
# Mixed people search — filter by title + company + location
curl -X POST "https://api.apollo.io/v1/mixed_people/search" \
  -H "Cache-Control: no-cache" \
  -H "X-Api-Key: $APOLLO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "person_titles": ["Staff Engineer", "Senior Software Engineer", "Principal Engineer"],
    "organization_locations": ["Berlin", "Munich"],
    "organization_industry_tag_ids": ["5567cd4773696439c5400000"],  // SaaS industry tag
    "person_seniorities": ["senior", "staff", "principal"],
    "page": 1,
    "per_page": 100
  }'
```

Apollo returns full contact: email (with confidence band), phone, current company + tenure, LinkedIn URL, location.

### Recipe 6: Apollo organization search → people in target accounts

```bash
# Step 1 — find companies via Apollo's company graph
curl -X POST "https://api.apollo.io/v1/mixed_companies/search" \
  -H "X-Api-Key: $APOLLO_API_KEY" \
  -d '{
    "organization_locations": ["United States"],
    "organization_num_employees_ranges": ["101,250", "251,500"],
    "organization_industry_tag_ids": ["5567cd4773696439c5400000"],  // SaaS
    "page": 1,
    "per_page": 25
  }'

# Step 2 — per company, pull people in target roles
for company in companies_response["organizations"]:
    curl -X POST "https://api.apollo.io/v1/mixed_people/search" \
      -d '{
        "organization_ids": ["'$company.id'"],
        "person_titles": ["Staff Engineer", "Senior Software Engineer"]
      }'
```

Apollo is the Crunchbase alternative for users who can't afford CB Enterprise. Free tier covers MVP (25 records/search, 1,200 records/year).

### Recipe 7: Composite target-account list (cross-reference 3 signals)

```python
# Combine: Crunchbase funding signal + Layoffs.fyi signal + Glassdoor culture signal
def score_target_account(company):
    score = 0

    # Funding signal — recent round + growth stage
    if company["last_funding_in_90d"]:
        score += 30
    elif company["stage"] in ["series_b", "series_c", "series_d"]:
        score += 15

    # Layoff signal — high intent passive pool
    if company["recent_layoff_30d"]:
        score += 25
    elif company["recent_layoff_180d"]:
        score += 12

    # Glassdoor signal — high-rated companies have happier (less open) employees
    if company["glassdoor_rating"] < 3.5:
        score += 20  # easier to source from low-rated
    elif company["glassdoor_rating"] >= 4.2:
        score += 5   # hard to pry from happy employees

    # Acquired-recently signal — 2-3 years post-acquisition = talent looking
    if 2 <= company["years_since_acquisition"] <= 3:
        score += 15

    return score
```

Top-50 by composite score → highest-leverage target list.

### Recipe 8: Bulk enroll into Gem hot-list with target-account tag

```bash
# After contact-enrich a candidate, push to Gem with target-account tag
curl -X POST "https://api.gem.com/v1/prospects" \
  -H "Authorization: Bearer $GEM_API_KEY" \
  -d '{
    "first_name": "Jane",
    "last_name": "Doe",
    "linkedin_url": "https://linkedin.com/in/janedoe",
    "email": "jane@stripe.com",
    "current_company": "Stripe",
    "current_title": "Staff Software Engineer",
    "tags": ["target-account-stripe", "hot-list-eng-staff-12mo", "source-crunchbase-signal"]
  }'
```

Tag with `target-account-{slug}` so future ATS reporting can attribute hires to the targeting strategy.

### Recipe 9: Outreach personalization with company news token

```python
# Pull last 30 days of company news for outreach personalization
import requests

def get_company_news_token(company_slug):
    # Crunchbase news endpoint
    news = requests.get(
        f"https://api.crunchbase.com/api/v4/searches/press_references",
        headers={"X-cb-user-key": CRUNCHBASE_API_KEY},
        params={
            "organization_identifier": company_slug,
            "from_date": (datetime.now() - timedelta(days=30)).isoformat()
        }
    ).json()

    if news.get("entities"):
        latest = news["entities"][0]
        return f"the {latest['identifier']['value']} announcement"  # e.g., "the Series C announcement"
    return None

# Use in InMail:
# "Congrats on {company_news_token} — as you scale, we're hiring a staff platform eng..."
```

Token rotation per 30 days keeps outreach fresh; same template + same news = stale within 60 days.

### Recipe 10: Glassdoor + Comparably culture signal (firecrawl)

```bash
# Scrape Glassdoor rating before targeting a company
# Skip companies with rating <3.0 — sourced candidates may have negative associations

GLASSDOOR_URL="https://www.glassdoor.com/Overview/Working-at-{company-slug}.htm"

firecrawl.scrape($GLASSDOOR_URL, {
  "extract": {
    "schema": {
      "overall_rating": "number",  // 1-5
      "ceo_approval": "number",    // 0-100
      "recommend_to_friend": "number",  // 0-100
      "recent_reviews_count": "number"
    }
  }
})
```

Glassdoor signal is heuristic — heavily moderated, biased toward extremes. Cross-validate with Comparably (more granular) when high-stakes.

## Examples

### Example 1: Build a 50-company target list for staff backend sourcing
**Goal:** Identify 50 SaaS companies (Series B-D, 100-500 headcount, US) for parallel sourcing.
**Steps:**
1. Crunchbase Recipe 1: filter `series_b/c/d`, headcount 100-500, SaaS, US → 200 companies.
2. Crunchbase Recipe 2: layer recent-round signal → narrow to 60 companies funded in 90d.
3. Layoffs.fyi cross-reference (Recipe 3) → flag 8 with recent cuts (top priority — high-intent pool).
4. Apollo Recipe 6: per company, count staff-backend headcount → drop companies with <3 backend engs (not enough pool).
5. Composite score (Recipe 7) → top 50.
6. Per company, Sales Nav saved search (Recipe 4) for `Staff Backend Engineer` filter.
7. Apollo enrich (Recipe 5) for email + phone.
8. Bulk enroll in Gem with `target-account-{slug}` tag.

**Result:** 200-400 contact-enriched staff backend candidates across 50 target accounts; per-account funnel attribution; layoff-tagged companies prioritized in sequence.

### Example 2: Mine ex-Stripe engineers (account-specific)
**Goal:** Find ex-Stripe staff backend engineers (Stripe = strong infra alumni signal).
**Steps:**
1. Crunchbase: pull Stripe profile + acquisitions (Bouncer, Bridge, Lemon Squeezy).
2. LinkedIn Sales Nav: `past_company=Stripe OR Bouncer OR Bridge OR Lemon Squeezy AND current_title="staff engineer"`.
3. Apollo enrich for email + current company + tenure.
4. Filter by `tenure_at_current_co > 1yr` (stable but not too long).
5. Tag in Gem: `target-account-ex-stripe`, `hot-list-eng-staff-6mo`.
6. Personalize outreach: reference shared Stripe alumni network.

**Result:** 30-80 ex-Stripe staff backend engineers identified; warm-intro paths via mutual Stripe alumni (`cold-inmail-warm-intro` Recipe 8).

### Example 3: Layoff-signal blitz outreach
**Goal:** Company X just announced 15% layoffs; sales team is panicked; 30 sales reps potentially open.
**Steps:**
1. Layoffs.fyi confirms company X cut 15% on date Y.
2. LinkedIn search: `current_company={X}, title contains "account executive" OR "AE", tenure>1yr`.
3. Apollo enrich for 30 reps' personal email (since work email may be revoked imminently).
4. Send same-week outreach via personal email; subject: "{X} update — and what's next" (acknowledge tactfully, don't gloat).
5. RepVue benchmark in outreach body for comp transparency (`sales-talent-sourcing-repvue`).
6. Tag in Gem: `layoff-signal-{X}-{date}`, `hot-list-ae-3mo`.

**Result:** 15-25 reply rate (vs 8-11% sales baseline) due to layoff timing.

## Edge cases / gotchas

- **Crunchbase Enterprise API is expensive ($999+/mo).** Free Crunchbase Pro covers limited search; Apollo's company graph is the alternative for cost-sensitive recipients.
- **Apollo's company graph is smaller than Crunchbase** (~10M companies vs Crunchbase 4M private + Apollo's 30M+ orgs lifetime data). Different shape — Apollo strong on small companies (B2B SaaS), Crunchbase strong on funded startups.
- **Layoffs.fyi data lags 5-15 days behind actual announcement.** WARN database is more current for US state-mandated notices but only covers companies > 50 employees.
- **Glassdoor scraping is gray-zone ToS.** Use sparingly + cache results; alternative: pay for Comparably API.
- **Apollo's email confidence band is real.** `verified` = 95%+ deliverable; `guessed` = 50-70%. Outreach to `guessed` tanks sender reputation. Reject or 2-source verify.
- **LinkedIn Sales Nav saved searches cap at 2,500 results.** Beyond that, paginate with filter splits.
- **Cross-referencing company-news tokens stale within 30 days.** Set up cron to refresh outreach token map monthly.
- **Layoff-signal outreach must be tonal.** Don't gloat ("we're hiring — perfect timing!"). Acknowledge the news, lead with the candidate. Sample: "Hi {first} — saw the {company} update. Whenever you're ready to think about next, we're a {sector} co {hiring details}. No rush; just on your radar."
- **Crunchbase Enterprise rate limit: 200 req/min.** Apollo: 50 req/min on paid tier. Batch + cache.
- **Some companies' LinkedIn employees can't be searched directly** (Sales Nav blocks specific company filters for ToS reasons — most often: Google, Meta, Apple at certain tiers). Workaround: search by past-employer tags.
- **Acquired-2-3-years-ago is real signal** — first cohort post-acquisition is usually vested + looking. Crunchbase exposes acquisition date.
- **Apollo's `person_seniorities` enum is fixed:** `owner, founder, c_suite, partner, vp, head, director, manager, senior, entry, intern`. Maps to your seniority taxonomy only loosely; cross-validate via title.
- **Defer outreach prose** to `cold-inmail-warm-intro` — this skill builds the target-account list + enriches contacts.
- **Defer exec sourcing** to `cto-vp-eng-exec-sourcing` — execs need 2-source contact verification + warm-intro path.
- **GDPR / CAN-SPAM:** Apollo + Crunchbase data is B2B contact data, legitimate-interest basis covered for commercial outreach with unsub honor. Personal email outreach (post-layoff signal) has higher scrutiny — defer compliance review to `operations-agent`.

## Sources

- Crunchbase Enterprise API: https://www.crunchbase.com/api
- Apollo.io API: https://www.apollo.io/product/api
- Apollo vs Crunchbase comparison: https://pipeline.zoominfo.com/sales/crunchbase-vs-apollo
- Findymail — Best Email Finder Tools 2026: https://www.findymail.com/blog/best-email-finder-tools/
- Layoffs.fyi: https://layoffs.fyi/
- WARN tracker: https://www.warntracker.com/
- Glassdoor: https://www.glassdoor.com
