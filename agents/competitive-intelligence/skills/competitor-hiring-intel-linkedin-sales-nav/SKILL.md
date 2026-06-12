<!--
Sources: LinkedIn Sales Navigator https://business.linkedin.com/sales-solutions/sales-navigator
         Sales Nav Filters Guide https://sbl.so/linkedin/sales-navigator-filters-guide/
         DemandSense Sales Nav https://www.demandsense.com/blog/how-to-use-linkedin-sales-navigator
         Glassdoor (ToS-sensitive) https://www.glassdoor.com/
         Levels.fyi compensation https://www.levels.fyi/
Companion playbook: role.md → "Continuous monitoring playbook" → Hiring layer + SOTA tool reference → LinkedIn Sales Navigator
-->

# Competitor hiring intel (LinkedIn Sales Navigator + careers-page + Glassdoor)

Detect competitor strategic intent through hiring patterns. Sales Navigator advanced filters (Current company + Department headcount growth + Job titles) surface where they're investing (eng hiring surge), what they're building (job-posting tech-stack disclosures), who's leaving (alumni filter), and exec moves (C-suite churn). Pair with careers-page scrape (free, ToS-permitted on most) and Glassdoor (ToS-sensitive — flag).

## When to use

- "Who's hiring at competitor X?"
- "Is [competitor] surging on engineering hires this quarter?"
- "Are key people leaving [competitor]?"
- "What tech stack are they hiring for?"
- New C-suite exec hire / departure detected
- Hiring layer of the continuous monitoring stack (bi-weekly cadence default)
- Pre-war-games scenario: signal on "they're building X feature"

## When NOT to use

- Pure exec-move alert without hiring depth → use `competitor-m-a-funding-crunchbase-pitchbook` (Owler exec-change tracking)
- Tech stack already deployed → use `competitor-tech-stack-builtwith-wappalyzer`
- Employee sentiment as proxy for product quality only → use `competitor-review-g2-trustradius-capterra` (Glassdoor lives there)
- Single-deal contact mapping → use `hot-deals-ci-deal-level`

## Setup

```bash
# LinkedIn Sales Navigator Core (~$100/mo/seat) - recipient supplies
export LINKEDIN_SALES_NAV_SEAT_EMAIL="..."
# OAuth via the `linkedin` skill (default in this bundle)
export LINKEDIN_OAUTH_CLIENT_ID="..."
export LINKEDIN_OAUTH_CLIENT_SECRET="..."

# Firecrawl for careers-page scrape (free tier)
export FIRECRAWL_API_KEY="..."

# Glassdoor scrape (ToS-grey - flag in deliverable)
# Levels.fyi (public; comp data)

# Anthropic for job-post theme extraction
export ANTHROPIC_API_KEY="sk-ant-..."

# Slack delivery
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

MCPs in `agent.yaml`: `linkedin`, `firecrawl-mcp`, `playwright-mcp`, `slack-mcp`, `notion-mcp`, `gmail-mcp`.

## Common recipes

### Recipe 1: Sales Nav saved search — hiring surge filter

In Sales Navigator UI, create a saved search per competitor with:

```yaml
saved_search_name: "Acme - Eng Hiring Surge"
filters:
  Current company: Acme Corp
  Department headcount growth: ">20% L6M"
  Department: Engineering
  Geo: United States
  Seniority: IC + Senior + Staff
  Date posted: last 30 days
```

Export weekly via the Sales Nav export endpoint or the `linkedin` skill OAuth.

### Recipe 2: Sales Nav alumni filter — attrition signal

```yaml
saved_search_name: "Acme - Recent Departures"
filters:
  Past company: Acme Corp
  Left in past: 90 days
  Seniority: Senior + above
  Function: Engineering OR Product OR Sales
```

Spike in senior departures = either RIF or losing key people. Triangulate with Levels.fyi pay-cut chatter and Glassdoor 1-star reviews.

### Recipe 3: Careers-page scrape (free, ToS-permitted on most)

```bash
curl -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://acme.example.com/careers",
    "formats": ["markdown", "json"],
    "schema": {
      "type": "object",
      "properties": {
        "jobs": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "title": {"type": "string"},
              "department": {"type": "string"},
              "location": {"type": "string"},
              "posted_at": {"type": "string"},
              "url": {"type": "string"}
            }
          }
        }
      }
    }
  }'
```

### Recipe 4: Greenhouse / Lever / Ashby ATS endpoints (free, public)

Many SaaS companies expose their ATS feed as JSON:

```bash
# Greenhouse (most common)
curl "https://boards-api.greenhouse.io/v1/boards/acme/jobs"

# Lever
curl "https://api.lever.co/v0/postings/acme?mode=json"

# Ashby (newer; less consistent)
curl "https://jobs.ashbyhq.com/api/non-user-graphql?operationName=ApiJobBoardWithTeams" \
  -H "Content-Type: application/json" \
  -d '{"variables":{"organizationHostedJobsPageName":"acme"}, "query": "..."}'
```

Identify which ATS via the careers-page redirect or HTML inspection.

### Recipe 5: Tech-stack from job-post requirements

```python
import anthropic
client = anthropic.Anthropic()

JOB_TEXT = open("acme_senior_eng_job.md").read()
prompt = f"""Extract the explicit tech stack mentioned as required or
preferred in this job posting. Return JSON with keys:
languages, frameworks, databases, infra, observability, ml_stack, other.

Job posting:
{JOB_TEXT}
"""
msg = client.messages.create(
    model="claude-opus-4-7-1m",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}],
)
print(msg.content[0].text)
```

Run across all open eng job posts → frequency table → signal: "Acme hiring 8 Rust + 5 ClickHouse roles last 60 days = building real-time analytics."

### Recipe 6: Headcount-by-function timeseries

```python
# Snapshot Sales Nav "Current company = Acme" filtered by Department,
# capture count weekly, store as time series.
import pandas as pd
df = pd.DataFrame({
    "week": ["2026-04-01", "2026-04-08", ..., "2026-06-10"],
    "Engineering": [220, 224, ..., 238],
    "Sales": [80, 80, ..., 82],
    "Product": [35, 35, ..., 38],
})
df["Engineering_d_l6w"] = df["Engineering"].diff(6)
print(df.tail())
```

### Recipe 7: Glassdoor scrape (ToS-grey — flag)

```bash
curl -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -d '{
    "url": "https://www.glassdoor.com/Reviews/Acme-Corp-Reviews-E123456.htm",
    "formats": ["markdown"]
  }'
```

**Flag in deliverable provenance footer: `glassdoor — ToS-grey-flagged`.** Note the SCIP soft-caution — only include if approved by recipient.

### Recipe 8: Levels.fyi compensation signal (public)

```bash
# Public comp data; legitimately public via API or page scrape
curl "https://www.levels.fyi/companies/acme-corp/salaries/software-engineer"
```

Use for: signal on whether they're paying above/below market (over-paying = attracting talent fast; under-paying = retention risk).

### Recipe 9: Exec move flash brief

```python
# Triggered when Sales Nav alumni filter flags a C-suite departure
def flash_brief(competitor, exec_name, prior_role, departure_date, public_quote=None):
    return f"""**FLASH CI BRIEF — {competitor}**
Exec move detected: {exec_name} ({prior_role}) departed {departure_date}.
Public confirmation: {public_quote or 'pending'}
Implications:
  - Strategic continuity risk in {prior_role.split()[-1]}
  - Possible roadmap delay / repositioning
  - Watch: replacement hire signal in next 30 days
Battlecard pane 3 (Latest deal intel) auto-flagged for refresh.
"""
```

### Recipe 10: Weekly hiring digest

```python
# Aggregate across competitors for the bi-weekly digest
digest_sections = [
    "TOP 3 HIRING SURGES THIS PERIOD",
    "TOP 3 ATTRITION SIGNALS THIS PERIOD",
    "NEW EXEC HIRES",
    "TECH STACK SHIFTS DETECTED IN JOB POSTS",
]
# Render → Slack via webhook + gmail digest
```

### Recipe 11: Tag battlecard with hiring signal

```python
# When hiring surge in a specific function detected, flag battlecard
def flag_battlecard(competitor, signal):
    payload = {
        "competitor_id": competitor,
        "pane": "swot",
        "annotation": f"Hiring signal: {signal} (auto-detected {today})",
    }
    requests.post(f"{KLUE_API_BASE}/battlecards/annotate", json=payload,
                  headers={"Authorization": f"Bearer {KLUE_API_KEY}"})
```

### Recipe 12: SCIP-compliant outreach guardrail

Sales Nav permits messaging current employees via InMail; **do NOT** message them for CI purposes (pretexting risk). Only:
- View their public profile (public-source).
- Read public posts / articles they authored.
- Track job-history changes (alumni filter).

## Examples

### Example 1: "Is Acme building an AI Copilot?" — answer from job posts

**Goal:** Detect new product investment direction from hiring signal.

**Steps:**
1. Recipe 4 → pull Acme's Greenhouse ATS feed.
2. Recipe 5 → LLM-extract tech stack from last 60 days of eng job posts.
3. Find: 6 LLM-eng roles + 4 vector-DB roles + 2 ML-infra roles.
4. Cross-reference with Recipe 1 Sales Nav surge filter — Eng headcount +18% L6M.
5. Cross-reference Sensor Tower + changelog → no shipped AI feature yet.

**Verdict:** Strong signal Acme is building AI capability shipping Q3-Q4 2026. Battlecard pane 4 (feature parity) flagged for "expected AI feature add Q3-Q4."

### Example 2: Attrition signal — Acme losing engineers

**Goal:** Identify whether Acme is in a key-person crisis.

**Steps:**
1. Recipe 2 → Sales Nav alumni filter shows 12 senior eng departures L90D vs 4 in prior quarter.
2. Recipe 8 → Levels.fyi shows recent comp-band cut (pay-band moved down 5%).
3. Recipe 7 → Glassdoor 1-star reviews L30D mention "RIF + culture" (3 of 5 new 1-stars). FLAG: ToS-grey.
4. Synthesize: likely RIF or strategic restructure. PMM flash brief sent.

**Result:** Battlecard pane 3 ("latest deal intel") updated to flag "competitor in restructure — exploit during deals."

### Example 3: Hiring digest sent bi-weekly to PMM

**Goal:** Standard CI digest with hiring section.

**Steps:**
1. Recipes 1, 2, 4 → pull all data for 5 competitors.
2. Recipe 10 → render digest sections.
3. Post to Slack `#ci-digest`; email to PMM lead via gmail-mcp.

**Result:** PMM sees the hiring picture without needing Sales Nav seat themselves.

## Edge cases / gotchas

- **LinkedIn ToS** — Sales Nav permits *viewing* + *saved search export* via the OAuth-permitted endpoints. Bulk scraping LinkedIn pages is a ToS violation and a SCIP soft-caution. Stick to the `linkedin` skill.
- **Sales Nav seat cost** — $100/mo per seat. CI team typically needs 1 dedicated seat. Recipient supplies.
- **Sales Nav saved-search export limits** — 25 rows per export; up to 1000/month. Heavy hiring surges may exceed; paginate.
- **Headcount-by-function noise** — LinkedIn "department" field is self-reported and stale. Triangulate with ATS open-req counts.
- **ATS feeds vary** — Greenhouse most common; Lever, Workday, Ashby, Recruitee, Personio all common. Auto-detect ATS via HTTP redirect / homepage script.
- **Workday is hard** — Workday tenants vary; usually need site-specific scraping logic or LinkedIn Jobs API as fallback.
- **Department field stale** — employees rename their department on profile months after a re-org; trust ATS over LinkedIn for current state.
- **Glassdoor ToS-grey** — flag in provenance footer. Some recipients refuse Glassdoor data entirely; check before including.
- **Don't pretexting employees** — SCIP hard no. No "I'm a recruiter from [vendor]" outreach for CI; no fake job offers.
- **Time zones** — Greenhouse `updated_at` is UTC; LinkedIn local; normalize to UTC.
- **False surge** — a single recruiting agency posting may inflate count for a few days. Smooth via 7-day rolling average.
- **PROACTIVE.md scheduling** — bi-weekly default cadence; document the cron + competitor list in PROACTIVE.md.
- **Job-post deletion** — Greenhouse removes filled reqs; snapshot daily to preserve historical signal even after they delete.
- **Multi-brand parent company** — if Acme is a subsidiary of MegaCorp, include both LinkedIn pages in the Current company filter.

## Sources

- LinkedIn Sales Navigator — https://business.linkedin.com/sales-solutions/sales-navigator
- Sales Nav Filters Guide — https://sbl.so/linkedin/sales-navigator-filters-guide/
- DemandSense — How to use LinkedIn Sales Navigator — https://www.demandsense.com/blog/how-to-use-linkedin-sales-navigator
- Greenhouse Job Board API — https://developers.greenhouse.io/job-board.html
- Lever Postings API — https://github.com/lever/postings-api
- Levels.fyi — https://www.levels.fyi/
- SCIP Code of Ethics — https://www.scip.org/page/Ethical-Intelligence
- role.md → "Capability reference" → Hiring layer; "SOTA tool reference" → LinkedIn Sales Navigator

## Related skills

- `competitor-m-a-funding-crunchbase-pitchbook` — exec moves + leadership tracking combined
- `competitor-tech-stack-builtwith-wappalyzer` — what they've already deployed
- `continuous-competitor-monitoring-klue-kompyte-crayon` — hiring layer in fan-out
- `battlecard-authoring-maintenance` — surface hiring signal as SWOT input
- `ethical-public-source-methodology` — SCIP code compliance on Glassdoor + LinkedIn
