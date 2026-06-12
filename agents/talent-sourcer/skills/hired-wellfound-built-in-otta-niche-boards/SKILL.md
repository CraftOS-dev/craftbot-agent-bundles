<!--
Sources: https://wellfound.com/recruit/pricing
         https://www.glozo.com/blog/niche-it-job-boards-recruiters-2025
         https://proficiently.com/blog/best-tech-job-boards/
         https://www.remotejobassistant.com/blog/wellfound-review
2026 niche-board landscape: Wellfound (formerly AngelList Talent) — 35K+ companies,
10M+ candidates, Recruit Pro $499/mo. Built In — US tech metro employer brand.
Otta — curated startup, candidate-ranked. Hired — two-sided matching. YC Work at
a Startup — closed to YC companies, highest startup signal.
-->
# Niche Job Boards — Wellfound / Hired / Built In / Otta — SKILL

Post jobs to and pull candidates from the 2026 niche tech board layer. Wellfound for startups (free posting + paid sourcing API). Built In for US tech-metro employer brand. Otta for curation. Hired for two-sided matching. Y Combinator Work at a Startup for YC-internal. Don't blast every board — niche boards work because they have audience focus; over-postingmuddies the brand.

## When to use

- User wants to **post a job to niche tech boards** appropriate for their stage / metro / role family.
- User wants to **pull candidate lists** from Wellfound / Otta / Built In dashboards for sourcing.
- User wants to **mirror an ATS job to public niche feeds** (Wellfound API + Built In feed + Otta integration).
- User asks "where should I post this job besides LinkedIn?".
- Trigger phrases: "post job to Wellfound", "Built In presence", "Otta listing", "startup-only boards", "niche tech board", "YC Work at a Startup".

Do not use for: LinkedIn posting (covered by parent `operations-agent` ATS skill); Indeed (too broad — falls under parent `operations-agent` general posting); RepVue sales boards (`sales-talent-sourcing-repvue`); Behance / Dribbble (`product-designer-sourcing-dribbble-behance`).

## Setup

```bash
# Wellfound — formerly AngelList Talent. Recruit Pro $499/mo for sourcing; free posting for startups.
export WELLFOUND_API_KEY="xxx"  # https://wellfound.com/settings/api
export WELLFOUND_COMPANY_ID="xxx"

# Built In — paid metro plan per metro (Austin, Chicago, NYC, LA, Boston, SF, Seattle, Denver, DC).
# No public REST API; integration via JSON feed mirror + employer dashboard via playwright-mcp.
export BUILTIN_FEED_URL="https://builtin.com/jobs/{company-slug}.json"
export BUILTIN_DASHBOARD_USER="recruiter@yourco.com"

# Otta — curated startup roles, candidate-ranked. Employer dashboard via playwright-mcp; no public API.
export OTTA_DASHBOARD_USER="recruiter@yourco.com"

# Hired — curated two-sided matching marketplace. Employer dashboard via playwright-mcp.
export HIRED_DASHBOARD_USER="recruiter@yourco.com"

# YC Work at a Startup — closed to YC companies; employer dashboard at https://www.workatastartup.com
# Auth via YC's Bookface SSO.
```

## Common recipes

### Recipe 1: Wellfound — post a job via API

```bash
curl -X POST "https://wellfound.com/api/recruit/v1/jobs" \
  -H "Authorization: Bearer $WELLFOUND_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": "'$WELLFOUND_COMPANY_ID'",
    "title": "Staff Backend Engineer",
    "description": "<HTML JD>",
    "role_type": "full_time",
    "location_tags": ["san-francisco", "remote-us"],
    "skill_tags": ["python", "golang", "distributed-systems"],
    "experience_min": 5,
    "salary_min": 200000,
    "salary_max": 280000,
    "equity_min": 0.1,
    "equity_max": 0.5,
    "visa_sponsorship": true,
    "remote_ok": true
  }'
```

Wellfound jobs surface to candidates filtered by skill tag + location + comp band. Comp transparency is mandatory (boost matching algorithm by 2-3×).

### Recipe 2: Wellfound — pull candidate matches (Recruit Pro tier required)

```bash
# Saved search returns candidates matching your role + open to your company size
curl -H "Authorization: Bearer $WELLFOUND_API_KEY" \
  "https://wellfound.com/api/recruit/v1/candidates/search?role=engineer&location=san-francisco&skill_tags=python,golang&experience_min=5&per_page=100"

# Per candidate
curl -H "Authorization: Bearer $WELLFOUND_API_KEY" \
  "https://wellfound.com/api/recruit/v1/candidates/{candidate_id}"
```

Response includes profile, GitHub link, current company, comp expectations, role preferences.

### Recipe 3: Wellfound — send a candidate message (intro)

```bash
curl -X POST "https://wellfound.com/api/recruit/v1/messages" \
  -H "Authorization: Bearer $WELLFOUND_API_KEY" \
  -d '{
    "candidate_id": "{id}",
    "job_id": "{job_id}",
    "subject": "Your Golang work",
    "body": "Hi {first} — saw your recent work on {open_source}; we're hiring a staff backend at {company}. Worth 20 min? Best, {recruiter}"
  }'
```

Wellfound intro messages avg ~25-35% reply rate (higher than LinkedIn InMail because candidates opted into discoverability).

### Recipe 4: Built In — mirror jobs to metro feed

Built In has no public API. Two integration paths:

```bash
# Path 1: JSON feed mirror — your ATS publishes feed; Built In ingests nightly
# Greenhouse board JSON feed works directly:
curl "https://boards-api.greenhouse.io/v1/boards/$GREENHOUSE_BOARD_TOKEN/jobs?content=true" > builtin_feed.json
# Then submit feed URL to Built In sales rep for ingest

# Path 2: Employer dashboard via playwright-mcp
# Authenticate → post job manually → tag with metro (Austin, NYC, etc.) → publish
```

Built In's value is employer brand (company page + Diversity & Inclusion section + employer benefits + tech stack badge), not posting volume. Worth the spend ($800-2,500/mo per metro) for companies committing to a metro for 12+ months.

### Recipe 5: Otta — employer dashboard via playwright-mcp

```python
# Pseudo — talent-sourcer wires via playwright-mcp
await playwright.goto("https://app.otta.com/")
await playwright.fill("[name=email]", OTTA_USER)
await playwright.fill("[name=password]", OTTA_PASS)
await playwright.click("button[type=submit]")

# Post a job
await playwright.goto("https://app.otta.com/employer/jobs/new")
await playwright.fill("[name=title]", "Staff Backend Engineer")
await playwright.fill("[name=description]", JD_HTML)
await playwright.select("[name=role-type]", "full-time")
# ... rest of form fields
await playwright.click("button[type=submit]")
```

Otta candidates are filtered by candidate preferences — they only see jobs that match their stated criteria. Conversion is high (3-5×) but reach is narrower.

### Recipe 6: Hired — two-sided matching workflow

```python
# Pseudo — Hired flips the script. Candidates set preferences (salary, role, location);
# employers send interview requests. No direct application form.

await playwright.goto("https://hired.com/employer/dashboard")
# Browse candidate list filtered by role / location / comp
await playwright.click("[data-test=candidate-card]:nth-child(1)")
# Send interview request
await playwright.click("[data-test=request-interview]")
await playwright.fill("[name=message]", INTERVIEW_REQUEST_MESSAGE)
await playwright.click("[data-test=send]")
```

Hired works best for senior IC + manager roles with clear comp bands. Less useful for exec roles (Hired candidates skew senior IC, not VP+).

### Recipe 7: YC Work at a Startup — for YC companies only

```python
# YC Work at a Startup uses Bookface SSO (YC alumni network).
# https://www.workatastartup.com/

await playwright.goto("https://www.workatastartup.com/companies/your-company/jobs/new")
# Post job — auto-filled from Bookface company profile
# Candidates: YC tracks engagement; companies with high response rates get search-rank boost
```

Highest-signal startup board if your company is YC. Reach is small but candidate quality is high (vetted via apply).

### Recipe 8: Niche-board posting matrix (which board for which role)

| Role family | Stage | Wellfound | Built In | Otta | Hired | YC W@S |
|-------------|-------|-----------|----------|------|-------|--------|
| Engineering IC | Seed-A | ✓ free | skip | ✓ | ✓ | ✓ if YC |
| Engineering IC | B-D | ✓ paid Pro | ✓ metro | ✓ | ✓ | ✓ if YC |
| Engineering IC | Late/PubCo | ✓ paid Pro | ✓ metro | skip | skip | n/a |
| Engineering Mgr | B+ | ✓ paid Pro | ✓ metro | ✓ | skip | ✓ if YC |
| Design | All | ✓ | ✓ metro | ✓ | skip — Hired weak on design | ✓ if YC |
| Sales | B+ | skip | skip | skip | skip | ✓ if YC |
| Product | All | ✓ | ✓ metro | ✓ | ✓ | ✓ if YC |
| Ops / G&A | All | skip | ✓ metro | skip | skip | skip |
| Customer Success | B+ | ✓ | ✓ metro | skip | skip | ✓ if YC |
| Exec (CTO/VP) | All | DO NOT POST — use `cto-vp-eng-exec-sourcing` | | | | |

### Recipe 9: Wellfound — scrape candidate list via firecrawl-mcp (when no Recruit Pro)

```bash
# When you can't afford Recruit Pro ($499/mo), use firecrawl-mcp to scrape candidate profiles
# ToS-aligned only if you have a free employer account + are within rate limits

# Pseudo — agent-side via firecrawl-mcp
firecrawl.scrape("https://wellfound.com/jobs/{job_id}/applicants", {
  "extract": {
    "name": "h3.applicant-name",
    "github": "a[href*='github.com']",
    "linkedin": "a[href*='linkedin.com']",
    "current_company": ".applicant-company"
  }
})
```

### Recipe 10: Built In — employer brand audit

```bash
# Before paying for Built In metro, verify the metro's audience fits
# Built In publishes monthly metro reports (Austin, NYC, etc.)
curl "https://builtin.com/austin/companies?industry=Software"
# Manual: visit https://builtin.com/austin/jobs/dev-engineering — is the org list relevant?

# Glassdoor 4.0+ floor recommended before paying for Built In employer brand
# (Built In surfaces Glassdoor rating in company profile; <4.0 is brand-damaging)
```

## Examples

### Example 1: Series B SaaS startup hiring 5 engineers in NYC
**Goal:** Maximize NYC engineering reach without LinkedIn-only dependence.
**Steps:**
1. Wellfound: post all 5 roles free (free posting for startups; Recipe 1). Add `nyc` + `remote-us` location tags.
2. Built In NYC: pay for NYC metro plan ($1,200/mo); mirror Greenhouse feed (Recipe 4).
3. Otta: post all 5 roles (Recipe 5).
4. YC W@S: if YC company, post (Recipe 7).
5. Track per-board source attribution via UTM params on apply URLs.

**Result:** 4-board mirror with per-board source attribution; expect 30-40% of pipeline from non-LinkedIn sources.

### Example 2: Series A startup needs Recruit Pro sourcing surface
**Goal:** Sourcing 50-100 passive candidates for a staff backend role; budget tight.
**Steps:**
1. Activate Wellfound Recruit Pro ($499/mo) — gives candidate search API (Recipe 2).
2. Search: `role=engineer, location=san-francisco OR remote-us, skill_tags=python,golang, experience_min=5`.
3. Filter to candidates open to seed-to-A-stage; sort by activity recency.
4. Send intros via Recipe 3 (avg 25-35% reply rate).
5. Push positive replies to ATS via parent `operations-agent` ATS skill.

**Result:** 25-35 interested candidates from a single $499/mo investment; lower cost than LinkedIn Recruiter seat ($899/mo Lite / $11k/yr Corporate).

### Example 3: Curated startup-only candidate flow via Otta
**Goal:** High-quality top-of-funnel from candidates who already prefer startups.
**Steps:**
1. Otta employer dashboard: post all open roles (Recipe 5).
2. Set candidate-fit filters: years exp, role type, comp band, remote OK.
3. Otta only surfaces your roles to candidates whose preferences match — natural filter.
4. Expect 5-15 high-fit applications per role per month at $500-900/mo employer fee.

**Result:** Lower volume but higher fit-rate than LinkedIn; ~50-70% reply-to-screen vs LinkedIn's 30-50%.

## Edge cases / gotchas

- **Wellfound's name change** — was "AngelList Talent", now "Wellfound" (since Nov 2022). Old URLs still redirect; old docs still ranked. Use wellfound.com canonically.
- **Wellfound free posting is genuine free for startups (<200 employees).** Beyond that you need Recruit Pro. Don't pay if not needed.
- **Wellfound Recruit Pro API has tier limits.** $499/mo = 100 messages/mo; higher tiers for unlimited. Plan candidate-outreach volume against tier.
- **Wellfound candidates DO see when you view them** (like LinkedIn Recruiter). View profile first → boosts intro acceptance.
- **Built In has NO public REST API.** All integration via Greenhouse / Lever / Ashby JSON feed mirror or playwright-mcp. Engaged sales rep is needed for feed ingest.
- **Built In is metro-paid.** $800-2,500/mo per metro. Posting alone doesn't unlock employer-brand features (D&I section, tech stack badge). Bundle = brand value.
- **Otta only surfaces jobs to candidates whose preferences match.** Don't post a 5+ years exp role and expect early-career flow. Audience is candidate-curated.
- **Otta's reach is European-skewed** (originated London 2019; expanded to US 2022). Strongest signal in EU metros.
- **Hired's two-sided matching means YOU send interview requests — candidates don't apply.** Inverts typical job-board mental model. Allocate sourcer time accordingly.
- **Hired skews senior IC + manager.** Exec roles via Hired typically yield mismatched candidates (the platform's algorithm doesn't differentiate IC8 from VP).
- **YC Work at a Startup is closed to non-YC companies.** Don't try to post; refer YC companies to `https://www.workatastartup.com/`.
- **Cross-posting risk: brand muddiness.** Posting same role to 8 boards looks desperate. 3-4 niche boards + LinkedIn + careers-page is the maximum healthy mix.
- **Salary-transparency requirements (CA, CO, NY, WA, IL)** — Wellfound mandates comp; Built In strongly recommends; Otta optional. Comply per posting metro.
- **YC W@S Bookface SSO requires YC partner approval** for sub-accounts (recruiters who aren't founders).
- **Defer ATS handoff** to parent `operations-agent`'s `hiring-pipeline-greenhouse-ashby-lever` skill — this skill produces source flow, not in-ATS workflow.
- **firecrawl-mcp scraping at scale violates Wellfound + Built In ToS.** Use only at low-volume MVP stage; activate API tier for production.

## Sources

- Wellfound (formerly AngelList Talent) — Recruit Pricing 2026: https://wellfound.com/recruit/pricing
- Glozo — 10 Niche IT Job Boards Recruiters Use 2026: https://www.glozo.com/blog/niche-it-job-boards-recruiters-2025
- Proficiently — 7 Best Tech Job Boards 2026: https://proficiently.com/blog/best-tech-job-boards/
- Remote Job Assistant — Wellfound Review 2026: https://www.remotejobassistant.com/blog/wellfound-review
- Built In — employer plans: https://builtin.com/employer
- Otta — employer dashboard: https://app.otta.com/
- Hired — employer platform: https://hired.com/employers
- YC Work at a Startup: https://www.workatastartup.com/
