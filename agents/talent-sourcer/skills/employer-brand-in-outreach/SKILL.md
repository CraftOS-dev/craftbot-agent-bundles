<!--
Sources: https://careery.pro/blog/recruiter-outreach-templates
         https://www.gem.com/blog/candidate-sourcing-software
         https://www.crunchbase.com/api
         https://www.glassdoor.com/employers/
         https://www.index.dev/blog/textio-review
         https://datapeople.io/comparison/datapeople-vs-textio/
         https://blog.ongig.com/job-descriptions/textio-competitors/
         https://www.linkedin.com/talent/talent-analytics
Top-performing outreach references recent funding + customer wins + Glassdoor + tech blog.
Pull last 30 days of company news; embed as {company_proof_point}.
Textio / Datapeople for JD scoring. Manual checklist fallback. LinkedIn employer brand analytics.
-->
# Employer Brand in Outreach — SKILL

Inject credible employer-brand proof points (recent funding, customer wins, Glassdoor rating, tech-blog posts, LinkedIn employer-brand metrics) into every outreach + JD. Pull last 30 days of company news via Crunchbase + Google News; verify Glassdoor ≥ 4.0; score JD via Textio / Datapeople; populate Gem / hireEZ token variables; auto-rotate every 30 days. The JD sub-skill is the gateway to applicant rate + female-applicant lift.

## When to use

- User wants to **refresh outreach tokens** with latest funding / news / customer win.
- User wants to **score / optimize a JD** before posting (gendered language, must-have count, comp transparency).
- User wants to **audit LinkedIn employer-brand metrics** (career page views, follower growth, content engagement).
- User wants to **verify a proof point is fresh** (Glassdoor rating current; news <30d).
- User asks: "employer brand", "company proof point", "JD optimization", "gendered language", "Textio score", "Datapeople review", "Glassdoor rating", "LinkedIn career page".

Do not use for: writing the cold InMail prose (`cold-inmail-warm-intro`); designing the sequence steps (`passive-candidate-outreach-campaigns`); the source attribution dashboard (`source-of-hire-reporting`).

## Setup

```bash
# Company news / signal sources
export CRUNCHBASE_API_KEY="xxx"        # https://data.crunchbase.com/docs
export NEWSAPI_KEY="xxx"               # https://newsapi.org/ — Google News alternative
export BRAVE_SEARCH_KEY="xxx"          # https://brave.com/search/api/

# Glassdoor (no public API in 2026; firecrawl-mcp for scrape)
export FIRECRAWL_KEY="xxx"

# JD scoring (paid)
export TEXTIO_API_KEY="xxx"            # https://textio.com — paid seat
export DATAPEOPLE_KEY="xxx"            # https://datapeople.io — paid seat

# LinkedIn Talent Analytics (Recruiter or Career Pages plan)
# Manual UI; no public API for employer-brand analytics in 2026

# Outreach CRM (where tokens live)
export GEM_API_KEY="xxx"

# Storage
export NOTION_API_KEY="secret_xxx"
export NOTION_PROOF_POINTS_DB="<db_id>"
```

## Common recipes

### Recipe 1: Proof-point token map (the canonical schema)

```yaml
# Per company; refresh every 30 days
company: "Acme"
proof_points:
  funding_recent:
    text: "Series C $80M led by Sequoia (May 2026)"
    source: "https://www.crunchbase.com/organization/acme/funding_rounds"
    expires: "2026-08-01"
  customer_win:
    text: "Onboarded 3 of top 10 US banks in Q1 2026"
    source: "https://acme.com/blog/q1-customer-update"
    expires: "2026-09-01"
  glassdoor:
    rating: 4.3
    reviews: 287
    ceo_approval: 89
    source: "https://glassdoor.com/Reviews/Acme-Reviews-E12345.htm"
    expires: "2026-07-01"
  tech_blog_post:
    text: "Engineering blog: How we scaled to 1B requests/day"
    url: "https://acme.com/blog/scaling-1b-rps"
    author: "VP Eng"
    date: "2026-05-15"
  press_mention:
    text: "Featured in The Information's '2026 AI Infra Top 50'"
    source: "https://www.theinformation.com/articles/..."
    expires: "2026-12-01"
  comp_transparency:
    text: "Bands published: Staff IC $250-310K + 0.15-0.30% equity"
    source: "internal-comp-band-2026Q2"
```

Persist in Notion `proof_points` DB; auto-flag stale (`expires < today`); recruiter refreshes monthly.

### Recipe 2: Pull latest funding events (Crunchbase API)

```bash
# Recent funding rounds for a company
curl "https://api.crunchbase.com/api/v4/entities/organizations/acme?card_ids=raised_funding_rounds&user_key=$CRUNCHBASE_API_KEY" \
  | jq '.cards.raised_funding_rounds.entities[0] | {round: .properties.investment_type, amount: .properties.money_raised.value_usd, date: .properties.announced_on, lead_investor: .properties.lead_investor_identifiers[0].value}'
```

Output:
```json
{"round": "series_c", "amount": 80000000, "date": "2026-05-12", "lead_investor": "Sequoia Capital"}
```

Compose into proof-point text: "Series C $80M led by Sequoia (May 2026)".

### Recipe 3: Pull recent news (NewsAPI / Brave Search)

```bash
# NewsAPI
curl "https://newsapi.org/v2/everything?q=Acme&from=$(date -u -d '30 days ago' +%Y-%m-%d)&sortBy=relevancy&apiKey=$NEWSAPI_KEY" \
  | jq '.articles[:5] | .[] | {title, source: .source.name, url, date: .publishedAt}'

# Brave Search alt
curl "https://api.search.brave.com/res/v1/news/search?q=Acme+funding&freshness=pm" \
  -H "X-Subscription-Token: $BRAVE_SEARCH_KEY" \
  | jq '.results[:5]'
```

### Recipe 4: Scrape Glassdoor rating (firecrawl-mcp, no public API)

```bash
# Glassdoor employer page
curl -X POST "https://api.firecrawl.dev/v1/scrape" \
  -H "Authorization: Bearer $FIRECRAWL_KEY" \
  -d '{
    "url": "https://www.glassdoor.com/Reviews/Acme-Reviews-E12345.htm",
    "formats": ["markdown"],
    "extract": {
      "schema": {
        "type": "object",
        "properties": {
          "overall_rating": {"type": "number"},
          "review_count": {"type": "number"},
          "ceo_approval_pct": {"type": "number"},
          "recommend_to_friend_pct": {"type": "number"}
        }
      }
    }
  }' | jq '.data.extracted'
```

Verify `overall_rating >= 4.0` before referencing in outreach. If <4.0, omit and pivot to alternate proof point (recent customer win, eng blog).

### Recipe 5: Score JD with Textio

```bash
# Submit JD text; receive language score
curl -X POST "https://api.textio.com/api/v1/scores" \
  -H "Authorization: Bearer $TEXTIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "We are looking for a rockstar engineer to join our fast-paced startup...",
    "type": "job_description"
  }' \
  | jq '{score: .textio_score, gender_tone: .gender_tone, age_tone: .age_tone, suggestions: .suggestions[:10]}'
```

Textio score >75 typically correlates with 15-20% applicant pool size lift. Score < 50 → rewrite.

### Recipe 6: Score JD with Datapeople (Textio alternative)

```bash
# Datapeople integration via JD posting workflow (no direct REST API exposed publicly in 2026)
# Pattern: use Datapeople Chrome extension OR ATS integration (Greenhouse / Ashby)

# Via Greenhouse integration: post JD to GH, Datapeople scores in dashboard
# Pull via Datapeople API (recipient holds seat):
curl "https://api.datapeople.io/v1/posts/{job_id}/score" \
  -H "Authorization: Bearer $DATAPEOPLE_KEY" \
  | jq '{readability: .readability_score, inclusive: .inclusive_score, completeness: .completeness_score, must_haves_count: .must_haves_count}'
```

Datapeople target: readability >80, inclusive >85, must_haves_count ≤ 8.

### Recipe 7: Manual JD checklist (Textio / Datapeople fallback)

When no paid seat available, run JD through this pass:

```
1. Gendered language scrub:
   BAD: ninja, rockstar, guru, manpower, chairman, salesman, warrior, dominant, aggressive
   GOOD: lead, operate, build, drive, ship

2. Age-coded language scrub:
   BAD: digital native, energetic, young team, recent grad mindset
   GOOD: skill-tied phrasing (knows X, has shipped Y)

3. Must-have count: cap at 6-8.
   - 9+ must-haves drops female applicant rate ~30-40%
   - Move >6 to "nice to have"

4. Comp transparency:
   - CA / CO / NY / WA: required by law; include band
   - Elsewhere: voluntary but boosts apply rate ~25%

5. Concrete impact framing:
   BAD: "fast-paced startup", "wear many hats"
   GOOD: "30/60/90 ramp plan with measurable outcomes"

6. Skills > years:
   BAD: "10+ years experience"
   GOOD: "you've shipped X, scaled Y, debugged Z"

7. Inclusive culture statement:
   - Brief, specific, with measured progress
   - Not corporate boilerplate

8. Senior IC salary match:
   - If you want senior IC, post senior IC band
   - Underpriced JDs filter out the candidates you want
```

### Recipe 8: Inject proof point into Gem sequence template

```bash
# Pull proof point from Notion DB
PROOF=$(curl "https://api.notion.com/v1/databases/$NOTION_PROOF_POINTS_DB/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -d '{"filter":{"property":"company","title":{"equals":"Acme"}}}' \
  | jq -r '.results[0].properties["funding_recent"]["rich_text"][0].plain_text')

# Update Gem sequence template token
curl -X PATCH "https://api.gem.com/v1/sequences/<seq-id>" \
  -H "Authorization: Bearer $GEM_API_KEY" \
  -d "{\"tokens\":{\"company_proof_point\":\"$PROOF\"}}"
```

Template body using token:
```
Subject: {first}, after the {company} round

Hi {first} — congrats on {company_proof_point}. As you scale through this chapter, we're hiring a {role} at {our_company}. Worth a 20-min chat? Best, {recruiter}
```

### Recipe 9: Auto-rotate proof points every 30 days (cron)

```bash
#!/bin/bash
# Run 1st of each month
# For each company in Notion proof_points DB:
#   1. Pull latest funding (Recipe 2)
#   2. Pull last 30d news (Recipe 3)
#   3. Refresh Glassdoor (Recipe 4)
#   4. Update Notion entry
#   5. If proof_point text changed, update Gem sequence tokens (Recipe 8)
#   6. Slack notify recruiter team of what changed

COMPANIES=$(curl "https://api.notion.com/v1/databases/$NOTION_PROOF_POINTS_DB/query" \
  -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28" \
  | jq -r '.results[].properties.company.title[0].plain_text')

for CO in $COMPANIES; do
  ./refresh_proof_points.sh "$CO"
done
```

### Recipe 10: LinkedIn employer-brand metrics (Talent Analytics UI)

LinkedIn Talent Insights / Recruiter Analytics surfaces:
- Career page views (last 30d / 90d trend)
- Follower count + growth rate
- Job-post engagement rate (impressions → clicks → applies)
- InMail acceptance rate vs industry benchmark
- Employee advocacy posts (LinkedIn Elevate equivalent)

No public REST API in 2026 — pull via Talent Insights UI export OR LinkedIn Pages export CSV. Weekly export to Google Sheet:

```python
# Manual export pattern (no API)
# 1. LinkedIn Pages → Analytics → Export
# 2. Upload CSV to Google Sheet via gspread
# 3. Track weekly:
metrics = {
    "week_of": "2026-06-08",
    "career_page_views": 4280,
    "follower_count": 18420,
    "follower_growth_pct": 1.2,
    "job_post_impressions": 124000,
    "job_post_apply_rate_pct": 2.4,        # benchmark 1.5-3%
    "inmail_acceptance_pct": 41,            # vs industry 30-35
    "employee_advocacy_posts": 18,           # employee-shared content count
    "career_page_apply_conversion_pct": 12   # career page view -> application
}
```

### Recipe 11: A/B test proof point in outreach

```python
# Compare 2 proof points in step-1 InMail
# Arm A: recent funding
# Arm B: recent customer win

prospects = load_segment("staff-backend-q3", 200)
import random; random.shuffle(prospects)

for i, p in enumerate(prospects):
    arm = "A" if i % 2 == 0 else "B"
    proof = "Series C $80M (May 2026)" if arm == "A" else "Onboarded 3 of top 10 US banks (Q1 2026)"
    gem.enroll(p, sequence=f"staff-backend-{arm}", tokens={**p, "company_proof_point": proof})

# After 14 days, query Gem analytics:
# - Reply rate Arm A vs Arm B
# - "Saw your X" mention in candidate reply (signals proof point landed)
```

Funding events typically out-perform customer wins for IC engineering. Customer wins out-perform for sales / CS. Verify per role.

### Recipe 12: Refresh cadence calendar

| Proof point type | Refresh cadence | Source |
|---|---|---|
| Recent funding | Monthly (or on event) | Crunchbase API |
| Customer win | Quarterly | Internal sales-marketing |
| Glassdoor rating | Monthly | firecrawl scrape |
| Tech blog post | Quarterly (or on publish) | Internal eng blog RSS |
| Press mention | Quarterly | NewsAPI + Brave Search |
| Comp band | Annually + on band update | Internal Pave / Carta |
| LinkedIn metrics | Weekly | Talent Insights export |
| Textio JD score | On every JD update | Textio API |

## Examples

### Example 1: Refresh proof points for Q3 outreach cycle
**Goal:** Quarterly proof-point refresh across 12 outreach sequences for company Acme.
**Steps:**
1. Run Recipe 2 (Crunchbase) → no new funding in last 30d; keep current Series C proof.
2. Run Recipe 3 (NewsAPI) → press mention in The Information's 2026 AI Infra Top 50; new proof point.
3. Run Recipe 4 (Glassdoor scrape) → 4.3 holding steady; keep referencing.
4. Pull eng-blog RSS → new post "How we scaled to 1B requests/day"; new proof.
5. Update Notion proof_points DB with refresh date + 3 new entries.
6. Run Recipe 8 to push refreshed tokens into 12 Gem sequences.
7. Run Recipe 11 A/B between funding + The Information mention; let data pick winner.

**Result:** All 12 sequences referencing current proof; reply-rate baseline lifts ~10-15% on rotation alone.

### Example 2: Optimize a JD scoring 38 on Textio
**Goal:** "Senior Software Ninja" JD scores 38 on Textio (target: >75). Diagnose + rewrite.
**Steps:**
1. Run Recipe 5 → Textio response identifies "ninja" + "rockstar" + 14 must-haves.
2. Apply Recipe 7 manual checklist:
   - Replace "ninja" with "engineer"; "rockstar" with "lead"
   - Cap must-haves at 6 (move 8 to nice-to-have)
   - Add comp band ($250-310K base + 0.15-0.30% equity)
   - Replace "10+ years experience" with "you've shipped distributed systems at scale, debugged production at 3am"
   - Add 30/60/90 plan section
3. Re-score → 78. Above target.
4. Verify Datapeople (Recipe 6) → readability 84, inclusive 88, must-haves 6. Pass.
5. Post to ATS; track applicant pool size vs prior JD over 30d.

**Result:** Applicant pool 2.1x; female applicant share rises from 18% to 31% based on Textio benchmark.

### Example 3: Glassdoor rating dropped to 3.6 — pivot proof points
**Goal:** Recipe 4 surfaces Glassdoor dropped 4.3 → 3.6 (40 new reviews, layoff coverage).
**Steps:**
1. Stop referencing Glassdoor rating in outreach immediately.
2. Update Notion proof_points DB; remove `glassdoor` entry; set expires=now.
3. Pivot to alternate proofs: tech-blog post + funding + customer win.
4. Slack-alert recruiter team: "Glassdoor rating dropped; do not cite in outreach until reviewed."
5. Flag to internal People team: 3.6 rating + layoff sentiment requires response strategy (separate workstream).
6. Continue outreach without Glassdoor reference until rating recovers.

**Result:** Outreach reply rate stays stable; brand risk contained; People team owns recovery.

## Edge cases / gotchas

- **Stale proof points are worse than no proof points.** "Series A $5M (Feb 2024)" in June 2026 outreach reads as out-of-touch. Set `expires` field + auto-flag.
- **Press mention paywalls.** The Information, WSJ, FT all paywall articles. Reference the headline + outlet, not a URL the candidate can't read.
- **Glassdoor reviews are gameable + biased.** A 3.8 from a recently-laid-off cohort doesn't reflect current culture. Cross-check with Comparably, Blind, Levels.fyi sentiment.
- **Textio is the standard but $$$.** Textio seat is $300-500/user/mo. For low-volume teams (<10 JDs/month), Recipe 7 manual checklist covers 80% of the value.
- **Datapeople has weaker bias engine than Textio** but is half the price. Acceptable for early-stage teams.
- **Customer-win proof points need legal review.** "Onboarded JPMorgan" may violate the customer's PR policy. Confirm with marketing before referencing in outreach.
- **Comp transparency varies by jurisdiction.** CA/CO/NY/WA require bands in JDs; voluntary elsewhere boosts apply rate but exposes the band publicly. Discuss with People-Ops before publishing.
- **LinkedIn employer-brand metrics have no API in 2026.** Manual export only. Schedule weekly to avoid drift.
- **A/B test proof points only with N ≥ 30/arm.** Smaller samples lock in noise as "winner".
- **Recent layoff = inverse proof point.** Don't reference recent funding if you just had layoffs. Candidates Google your company first.
- **Crunchbase free tier is rate-limited.** Enterprise key required for high-volume refresh. Free tier covers monthly refresh for <50 companies.
- **NewsAPI free tier: 100 req/day.** Sufficient for monthly refresh of 50-100 companies; batch if more.
- **Glassdoor ToS prohibits scraping.** firecrawl-mcp may be challenged. Manual quarterly review by recruiter is safest. Comparably has friendlier API.
- **Brave Search returns SEO-optimized results.** Quality varies; cross-verify any major proof point from at least 2 sources.
- **Proof-point freshness signals investment.** Candidates notice when outreach references something from this month vs 18 months ago. Refresh discipline matters more than the proof point itself.
- **Hand off to `cold-inmail-warm-intro`** for the prose authoring once tokens are populated.
- **Hand off to `passive-candidate-outreach-campaigns`** for sequence-step design + A/B test mechanics.
- **JD posting + ATS sync** is owned by `operations-agent` (parent) — this skill provides the optimization, that skill does the posting.

## Sources

- Careery — Recruiter Outreach Templates 2026: https://careery.pro/blog/recruiter-outreach-templates
- Gem — Best Candidate Sourcing Software 2026: https://www.gem.com/blog/candidate-sourcing-software
- Crunchbase API docs: https://www.crunchbase.com/api + https://data.crunchbase.com/docs
- Glassdoor for employers: https://www.glassdoor.com/employers/
- Index.dev — Textio Review 2026: https://www.index.dev/blog/textio-review
- Datapeople vs Textio comparison: https://datapeople.io/comparison/datapeople-vs-textio/
- Ongig — Textio Competitors 2026: https://blog.ongig.com/job-descriptions/textio-competitors/
- LinkedIn Talent Analytics: https://www.linkedin.com/talent/talent-analytics
- NewsAPI docs: https://newsapi.org/docs
- Brave Search API: https://brave.com/search/api/
- Firecrawl docs: https://docs.firecrawl.dev
