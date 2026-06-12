<!--
Sources: https://www.greenhouse.io/job-board
         https://www.ashbyhq.com/job-board
         https://www.pinpointhq.com/career-sites/
         https://developers.google.com/search/docs/appearance/structured-data/job-posting
Career site 2026: ATS-native job board (free) + EVP layer (paid Pinpoint/Phenom) + structured-data
Job Posting schema (SEO). Long-form brand campaigns → marketing-agent.
-->
# Employer Brand Campaigns + Career Site — SKILL

Build and operate the career site: ATS job-board configuration, EVP statement + employee testimonial surfacing, Job Posting structured-data SEO, mobile-first + ≤3s load, day-in-the-life content, transparent comp/process/values display. Long-form paid brand campaigns defer to `marketing-agent`.

## When to use

- Net-new career site or refresh.
- New EVP statement after culture-survey insights.
- New role launch — verify Job Posting schema + structured data + comp transparency compliance.
- Trigger phrases: "career site", "EVP statement", "job board", "Greenhouse job board", "Ashby job board", "Pinpoint Career Sites", "structured data", "career page SEO", "day in the life".

Defer to `marketing-agent` for: long-form paid LinkedIn / Built In sponsorships, video production beyond simple day-in-the-life, paid Glassdoor sponsored placements.

## Setup

```bash
# ATS job boards
export GREENHOUSE_API_KEY="harvest_xxx"
export GH_USER_ID="123456"
export GREENHOUSE_BOARD_TOKEN="company"   # public slug
export ASHBY_API_KEY="xxx"
export ASHBY_BOARD_NAME="company"
export LEVER_API_KEY="xxx"; export LEVER_SITE="company"

# Paid career-site layer (optional)
export PINPOINT_API_KEY="xxx"             # https://www.pinpointhq.com/developers
export PHENOM_API_KEY="xxx"

# Testimonial collection + assets
export TYPEFORM_TOKEN="tfp_xxx"
export GOOGLE_DRIVE_OAUTH="<bearer>"

# SEO audit
# Lighthouse via playwright-mcp; PageSpeed Insights API
export PAGESPEED_API_KEY="xxx"            # https://developers.google.com/speed/docs/insights/v5/get-started
```

Auth model: ATS job-board public endpoints are unauthenticated (`boards-api.greenhouse.io`, `api.ashbyhq.com/posting-api/job-board/<name>`). Mutations to job content via Harvest / Ashby internal API with seat.

## Common recipes

### Recipe 1: Pull Greenhouse public Job Board
```bash
curl -s "https://boards-api.greenhouse.io/v1/boards/$GREENHOUSE_BOARD_TOKEN/jobs?content=true" \
  | jq '.jobs[] | {id, title, location: .location.name, department: .departments[].name, content_preview: (.content | .[0:200])}'
```
Use for: career-page rendering, structured-data injection, sitemap.xml.

### Recipe 2: Update Greenhouse job content (with structured data hints)
```bash
# Greenhouse stores JD as HTML; embed Microdata or push JSON-LD via your own page wrapper.
curl -s -X PATCH -u "$GREENHOUSE_API_KEY:" \
  -H "On-Behalf-Of: $GH_USER_ID" \
  -H "Content-Type: application/json" \
  "https://harvest.greenhouse.io/v1/jobs/<job_id>" \
  -d '{"name": "Senior Backend Engineer (Python / Go)", "notes": "Includes comp band per CA SB 1162"}'
```

### Recipe 3: Pull Ashby Job Board with compensation
```bash
curl -s "https://api.ashbyhq.com/posting-api/job-board/$ASHBY_BOARD_NAME?includeCompensation=true" \
  | jq '.jobs[] | {id, title, location: .location.locationName, comp: .compensation}'
```
Critical for CA SB 1162, NY pay transparency, CO Equal Pay.

### Recipe 4: Inject Job Posting structured data (JSON-LD)
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "JobPosting",
  "title": "Senior Backend Engineer",
  "description": "<full HTML JD>",
  "identifier": {"@type": "PropertyValue", "name": "Acme", "value": "GH-12345"},
  "datePosted": "2026-06-09",
  "validThrough": "2026-08-09",
  "employmentType": "FULL_TIME",
  "hiringOrganization": {"@type": "Organization", "name": "Acme", "sameAs": "https://acme.com", "logo": "https://acme.com/logo.png"},
  "jobLocation": {"@type": "Place", "address": {"@type": "PostalAddress", "addressLocality": "San Francisco", "addressRegion": "CA", "addressCountry": "US"}},
  "baseSalary": {"@type": "MonetaryAmount", "currency": "USD",
                 "value": {"@type": "QuantitativeValue", "minValue": 175000, "maxValue": 220000, "unitText": "YEAR"}}
}
</script>
```
Required for Google for Jobs eligibility. Validate via Rich Results Test (https://search.google.com/test/rich-results).

### Recipe 5: Career-page Lighthouse audit (playwright)
```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  browser = p.chromium.launch()
  page = browser.new_page()
  page.goto("https://acme.com/careers")
  # Run Lighthouse via CLI for richer output
import subprocess
subprocess.run(["npx", "lighthouse", "https://acme.com/careers",
                "--output=json", "--output-path=careers_audit.json",
                "--only-categories=performance,accessibility,seo,best-practices",
                "--chrome-flags=--headless"], check=True)
```

### Recipe 6: PageSpeed Insights API
```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https%3A%2F%2Facme.com%2Fcareers&strategy=mobile&key=$PAGESPEED_API_KEY" \
  | jq '.lighthouseResult.categories | {performance: .performance.score, seo: .seo.score, accessibility: .accessibility.score}'
```
Target: performance ≥0.90, SEO ≥0.95.

### Recipe 7: Pinpoint Career Sites — create branded page
```bash
curl -s -X POST -H "Authorization: Bearer $PINPOINT_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.pinpointhq.com/v1/career_sites" \
  -d '{
    "name": "Acme Careers",
    "domain": "careers.acme.com",
    "evp_statement": "We build for the long arc...",
    "testimonial_count": 12,
    "include_comp_band": true,
    "include_process_transparency": true
  }'
```

### Recipe 8: Day-in-the-life content collection (Typeform → Drive)
```bash
# Typeform survey: "Tell us your day. 3-5 prompts: morning ritual / favorite collaboration / hardest day / what kept you / advice."
LINK="https://acme.typeform.com/to/<form_id>"
# Pull responses
curl -s -H "Authorization: Bearer $TYPEFORM_TOKEN" \
  "https://api.typeform.com/forms/<form_id>/responses?since=2026-04-01" \
  | jq '.items[] | {employee: .hidden.employee_name, role: .answers[0].text, quotes: [.answers[1].text, .answers[2].text, .answers[3].text]}'
# Curate top 3-5 voices per role family; layout via Recipe 7 (Pinpoint) or custom page.
```

### Recipe 9: Comp-transparency block per geo
```text
# CA SB 1162 (eff Jan 2023, broader 2026): comp range required on all CA-applicant-facing JDs
# NY Pay Transparency (eff Sep 2023): comp range + good-faith range
# CO Equal Pay for Equal Work (eff Jan 2021): comp band + benefits summary
# WA + IL + MD + DC + Cincinnati + Toledo + more
# Default 2026: ALWAYS publish comp range in JD; failure = legal exposure + brand damage
# Block template:
"Base salary: $175K-$220K USD per year. Equity grant subject to Board approval per company plan.
Health, dental, vision, 401(k), unlimited PTO. Full benefits summary at <link>."
```

### Recipe 10: ATS job-board iframe embed (free path)
```html
<!-- Greenhouse public-jobs iframe -->
<div id="grnhse_app"></div>
<script src="https://boards.greenhouse.io/embed/job_board/js?for=acme"></script>
<!-- Ashby embed -->
<iframe src="https://jobs.ashbyhq.com/acme" width="100%" height="800" frameborder="0"></iframe>
```
For zero-build career site, embed ATS-native; add EVP + testimonials in surrounding HTML.

### Recipe 11: Sitemap + JD validity refresh (cron)
```python
import requests, os, datetime
jobs = requests.get(f"https://boards-api.greenhouse.io/v1/boards/{os.environ['GREENHOUSE_BOARD_TOKEN']}/jobs").json()["jobs"]
with open("sitemap.xml", "w") as f:
  f.write('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
  for j in jobs:
    f.write(f"<url><loc>https://acme.com/careers/{j['id']}</loc><lastmod>{datetime.date.today()}</lastmod></url>")
  f.write("</urlset>")
```

### Recipe 12: Career-site A/B test (apply-rate lift)
```python
# A: comp range visible, EVP top-of-page, 3 testimonials.
# B: same but with day-in-the-life video.
# Track apply-rate per variant via UTM + posthog-mcp.
# 4-week test → keep winner.
```

## Examples

### Example 1: New career site for Series-A startup (zero-build)
**Goal:** Launch in 1 week using Greenhouse + EVP wrapper.
**Steps:**
1. Recipe 10 embeds Greenhouse job-board iframe.
2. Recipe 8 collects 5 employee day-in-the-life voices.
3. Recipe 9 adds comp-transparency block.
4. Recipe 4 injects JSON-LD per job (use Recipe 1 + template).
5. Recipe 6 / Recipe 5 verifies Lighthouse + Rich Results.

**Result:** Career site live in 1 week; SEO-eligible; comp-compliant; voice-rich.

### Example 2: Comp-transparency refresh across all live JDs
**Goal:** Comply with NY + CA + CO + WA in one push.
**Steps:**
1. Recipe 1 lists all jobs.
2. For each: pull comp band from `offer-negotiation-comp-band-equity-perks` skill (Pave benchmark) or HR config.
3. Recipe 2 patches `notes` / JD body with comp block per Recipe 9.
4. Recipe 11 refreshes sitemap.

**Result:** All JDs comp-compliant within 1 day; legal risk closed.

### Example 3: Day-in-the-life campaign with marketing handoff
**Goal:** Build a 6-employee day-in-life video series.
**Steps:**
1. Recipe 8 collects 20 written voices.
2. Curate 6 most-resonant.
3. Hand off to `marketing-agent` for video production + paid LinkedIn distribution.
4. Recruiter: embed final videos on career-page role pages + use in outreach links.

**Result:** Authentic content; clean split of duty.

## Edge cases / gotchas

- **Comp transparency varies by state.** CA / NY / CO / WA / IL / MD / DC / Cincinnati / Toledo / Jersey City + . Default 2026: post comp on every JD that may be viewed by applicants in those states (= almost any remote JD). Mid-2026 trend: federal-level mandate proposed.
- **Google for Jobs requires structured data.** Without JSON-LD JobPosting schema, your JD won't surface in Google for Jobs results. Significant traffic loss.
- **Greenhouse job-board cache lag.** `boards-api.greenhouse.io` is cached ~2-5 min behind Harvest. Don't gate publishing on instant consistency.
- **Ashby `includeCompensation=true` is empty if comp not set in-app.** Always set comp on the job in Ashby admin before exposing the public page.
- **iframe SEO penalty.** Embedded iframe contents are not always crawled. For SEO, render server-side via API (Recipe 1) — not iframe.
- **Mobile-first matters.** >70% of applicant traffic is mobile in 2026. Lighthouse mobile score is the right target.
- **Testimonial consent.** Get written consent before publishing employee voices. Defer wording to `legal-counsel`.
- **Pinpoint / Phenom lock-in.** Paid career-site platforms own the URL; switching costs are real. ATS-native iframe is cheaper for <100-employee orgs.
- **EVP without substance.** "We have great culture" written 1000× isn't an EVP. EVP = the 3 specific things you trade off (e.g., "we pay 50th percentile + grant 75th equity; we ship features over polish; we're remote-first without office requirement"). If your EVP could be on any company's careers page, it's not an EVP.
- **Built In / The Muse / Comparably profiles.** Free profiles available; light EVP content surface. Don't compete with these — link to them from your career site.
- **Defer to `marketing-agent`** for: long-form paid campaigns, video production beyond day-in-life, brand identity refresh, EVP as part of company-wide brand strategy. Recruiter owns career-site execution; marketing owns brand strategy.

## Sources

- [Greenhouse Job Board API](https://developers.greenhouse.io/job-board.html)
- [Ashby Posting API](https://developers.ashbyhq.com/reference/postingapijobboard)
- [Lever Postings API](https://hire.lever.co/developer/documentation#postings)
- [Pinpoint Career Sites](https://www.pinpointhq.com/career-sites/)
- [Google Job Posting structured data](https://developers.google.com/search/docs/appearance/structured-data/job-posting)
- [Rich Results Test](https://search.google.com/test/rich-results)
- [PageSpeed Insights API](https://developers.google.com/speed/docs/insights/v5/get-started)
- [CA SB 1162 — Pay Transparency](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202120220SB1162)
- [NY Pay Transparency Law](https://www.labor.ny.gov/pay-transparency)
- [CO Equal Pay for Equal Work](https://cdle.colorado.gov/dlss/equal-pay-for-equal-work-act)
