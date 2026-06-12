---
name: grant-prospect-research-grants-gov-instrumentl-candid
description: Discover federal, state, foundation, and corporate funding prospects via Grants.gov + SAM.gov + ProPublica 990s + Candid + Instrumentl + GrantStation. Use when the user says "find me grants" / "research funders for X" / "who funded our peer org".
---

# Grant prospect research — Grants.gov, SAM.gov, Candid, Instrumentl, ProPublica

The SOTA prospect-research stack as of June 2026. Free federal APIs (Grants.gov + SAM.gov + ProPublica) cover federal + 501(c)(3) discovery; paid databases (Candid + Instrumentl + GrantStation) cover the foundation + corporate long tail. Always start free, then layer paid only if the org subscribes.

## When to use

- User asks "find me grant prospects for <topic / population / geography>"
- User wants to mine 990s for foundations that funded a peer org
- User needs federal NOFO discovery for a specific CFDA / agency
- User wants to verify a funder's 501(c)(3) status or check their giving size
- Building or refreshing the funder pipeline at the start of a grant cycle

Do NOT use this skill for:
- Drafting the LOI / proposal (→ `loi-letter-of-inquiry-drafting`, `full-grant-proposal-narrative-methods-evaluation`)
- Tracking already-discovered prospects through the pipeline (→ `multi-grant-pipeline-mgmt`)
- Corporate CSR-specific research (→ `corp-giving-csr-bumblebee-goodera`)

## Setup

```bash
# Free APIs (no install)
curl --version

# Optional: SAM.gov API key (free, 7-day registration)
# Register at https://sam.gov/data-services
export SAM_API_KEY="..."

# Optional paid: Candid Search / Instrumentl / GrantStation (recipient subscription)
export CANDID_API_KEY="..."
export INSTRUMENTL_API_KEY="..."
```

Auth / API key requirements:
- Grants.gov Get Opportunities Public API — free, no auth
- SAM.gov Opportunities API — free SAM.gov account + API key
- ProPublica Nonprofit Explorer API — free, no auth
- Candid Search — $100/mo (down from $299 post-2026 GuideStar merger)
- Instrumentl — $299/mo
- GrantStation — $99/yr

## Common recipes

### Recipe 1: Search Grants.gov for active federal opportunities

```bash
curl -X POST https://api.grants.gov/v1/api/search2 \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "early childhood education",
    "oppStatuses": "forecasted|posted",
    "rows": 50,
    "sortBy": "closeDate|asc"
  }'
```

Returns JSON: `opportunityNumber`, `title`, `agencyCode`, `closeDate`, `awardCeiling`, `awardFloor`, `cfdaList`. Filter `oppStatuses` to `posted` only for currently open NOFOs.

### Recipe 2: Pull full NOFO detail for a specific opportunity

```bash
curl -X POST https://api.grants.gov/v1/api/fetchOpportunity \
  -H "Content-Type: application/json" \
  -d '{"opportunityId": "352421"}'
```

Returns full opportunity package metadata + attached documents list. The agency-specific NOFO PDF is in the `synopsisAttachments` array.

### Recipe 3: SAM.gov opportunity search

```bash
curl "https://api.sam.gov/opportunities/v2/search?\
api_key=$SAM_API_KEY&\
postedFrom=06/01/2026&\
postedTo=06/30/2026&\
ptype=g&\
limit=100"
```

`ptype=g` filters to grant notices. Use `ptype=o` for solicitations, `ptype=k` for combined.

### Recipe 4: ProPublica 990 search for a funder

```bash
# Search by name
curl "https://projects.propublica.org/nonprofits/api/v2/search.json?q=Hewlett+Foundation"

# Pull org detail + 990 PDFs by EIN
curl "https://projects.propublica.org/nonprofits/api/v2/organizations/941655673.json"
```

Returns `filings_with_data` array with `pdf_url` for each year. Pull last 3 years to assess giving trend.

### Recipe 5: Mine 990 Schedule I (grants to other organizations)

```bash
# Download a foundation's 990 PDF
curl -o foundation_990.pdf "https://projects.propublica.org/nonprofits/download-filing?path=..."

# Extract Schedule I (grants to organizations) via pdftotext
pdftotext -layout foundation_990.pdf foundation_990.txt
grep -A 5 "Schedule I" foundation_990.txt
```

Schedule I lists recipients + amounts. Filter to peer-org recipients to map who funded the same problem space.

### Recipe 6: Verify 501(c)(3) status via IRS EO Search

```bash
# IRS Tax Exempt Organization Search (no public API; scrape with firecrawl-mcp)
# Direct URL pattern:
echo "https://apps.irs.gov/app/eos/displayAll.do?dispatchMethod=displayAllInfo&Id=12345&ein=941655673"
```

For programmatic checks, ProPublica's API includes 501(c)(3) status flag (`subsection_code: 03`).

### Recipe 7: Candid Search REST (paid)

```bash
curl -H "Subscription-Key: $CANDID_API_KEY" \
  "https://api.candid.org/funders/v1?\
geographic_area_served=CA-Alameda&\
program_area=education&\
grant_size_min=10000&\
grant_size_max=250000"
```

Candid's geographic-mapping advantage: filter by congressional district, county, or city — invaluable for place-based funder discovery.

### Recipe 8: Instrumentl saved-search export

```bash
curl -H "Authorization: Bearer $INSTRUMENTL_API_KEY" \
  "https://api.instrumentl.com/v1/searches/<search_id>/funders?\
limit=100&\
include_dafs=true"
```

Instrumentl uniquely includes Donor-Advised Funds (DAFs) — Fidelity Charitable, Schwab Charitable, Vanguard Charitable — that don't appear in Candid.

### Recipe 9: Scrape foundation pages with firecrawl when no API exists

```bash
# Via firecrawl-mcp tool (in agent context)
firecrawl_scrape url="https://hewlett.org/grants/" formats=["markdown"]
```

Most family + community foundations publish current priorities + recent grantees on a `/grants` page; scrape and structure into the Notion funder profile card.

### Recipe 10: Build a funder shortlist CSV

```bash
# After running recipes 1-3, normalize into a CSV
echo "funder,type,priority_match,avg_grant,geo,deadline,priority_score" > prospects.csv
# Append one row per qualified prospect; priority_score = funder priority overlap * geo fit * grant size fit
```

Aim for 20-40 qualified prospects per active program area, not 200 unqualified.

## Examples

### Example 1: Find funders for a place-based early childhood program in Oakland

**Goal:** Build a 30-prospect shortlist mixing federal + foundation + corp for an Oakland-based ECE org.

**Steps:**
1. Federal: `curl -X POST https://api.grants.gov/v1/api/search2 -d '{"keyword":"early childhood","oppStatuses":"posted"}'` — pull active NOFOs from ED, HHS ACF, HRSA.
2. Foundation: query Candid filtered to Alameda County + program area = early childhood + grant size $25K-$250K. Cross-reference with ProPublica 990s of community foundations (Silicon Valley CF, San Francisco Foundation, East Bay Community Foundation) to see which already fund peer ECE orgs.
3. Mine Schedule I of 3 community-foundation 990s for peer-org recipients; for each peer org, pull THEIR 990 Schedule B (top donors) — that's the second-degree funder network.
4. Corp: search Benevity Causes for ECE listings local to Bay Area + check Salesforce.org, Genentech, and Chevron community-giving pages via `firecrawl-mcp`.
5. Score each on (priority match × geo fit × grant size fit) and rank top 30.

**Result:** Notion table of 30 ranked prospects with funder, type, avg grant, deadline, priority score, and the 990-derived signal that brought them onto the list.

### Example 2: Identify federal NOFOs for a national workforce-development nonprofit

**Goal:** Find FY26 federal opportunities for a workforce-development org.

**Steps:**
1. `curl -X POST https://api.grants.gov/v1/api/search2 -d '{"keyword":"workforce development","fundingCategories":"ET","oppStatuses":"posted|forecasted"}'` (CFDA category ET = Employment, Labor, Training).
2. Cross-reference with SAM.gov search filtered to DOL + ED + Commerce.
3. For each posted opportunity, `fetchOpportunity` for full text and check eligibility (501(c)(3)? state agency? both?).
4. Pull last cycle's award abstracts via `usaspending.gov` API to see who won.
5. Schedule each deadline in Google Calendar via `google-calendar-mcp`.

**Result:** 8-12 active or forecasted federal NOFOs with eligibility, deadlines, and historical award context.

## Edge cases / gotchas

- **Grants.gov API has no search-by-EIN.** Use ProPublica for 990 mining; Grants.gov is opportunity-side only.
- **SAM.gov API rate limit:** 1000 requests/hour per API key — paginate aggressively, cache results.
- **ProPublica latency:** 990 filings appear 6-18 months after fiscal year end. A "FY24" 990 may not appear until late 2025 or early 2026.
- **Candid post-merger:** GuideStar APIs are deprecated as of January 2026; migrate to Candid Search API. Old endpoints return 410 Gone.
- **DAFs are mostly opaque:** Even Instrumentl can identify a DAF sponsor (Fidelity, Schwab, Vanguard) but cannot identify the donor-advisor. Sponsor outreach goes via the philanthropic services team.
- **Foundation cycles:** Many family foundations have 1-2 LOI windows per year; missing the window means a 6-12 month wait. Calendar cycle dates from the Foundation's "How to apply" page.
- **Forecasted vs Posted:** Always filter Grants.gov to `oppStatuses: posted` for actionable deadlines; `forecasted` is informational only.
- **Federal funding flux 2026:** Per Instrumentl's 2026 federal funding report, the OMB May 29 2026 rewrite + agency reorgs mean many CFDAs are in flux — verify the NOFO is still active before drafting.
- **Eligibility traps:** Some NOFOs require state designation, county pre-approval, or membership in a coalition — read eligibility section 3 of every NOFO before drafting.

## Sources

- Grants.gov Get Opportunities Public API: https://open.gsa.gov/api/get-opportunities-public-api/
- SAM.gov Opportunities API: https://open.gsa.gov/api/opportunities-api/
- ProPublica Nonprofit Explorer API v2: https://projects.propublica.org/nonprofits/api
- Candid: https://candid.org/
- Instrumentl: https://www.instrumentl.com/
- GrantStation: https://www.grantstation.com/
- IRS Tax Exempt Organization Search: https://apps.irs.gov/app/eos/
- 2026 prospect-research database comparison: https://sparkthefiregrantwriting.com/blog/best-grant-prospect-research-databases-of-2026
- Instrumentl 2026 federal funding report: https://www.instrumentl.com/blog/federal-funding-changes-report
