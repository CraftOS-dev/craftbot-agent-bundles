<!--
Sources: https://www.glassdoor.com/employers/
         https://www.comparably.com/companies
         https://www.workology.com/employer-branding-2026/
Glassdoor + Comparably APIs are limited / partner-only. 2026 SOTA = scrape with firecrawl-mcp for
monitoring + playwright-mcp UI automation for responses. Free Employer Account covers basic
response; paid Enhanced Profile adds testimonials, EVP, photos. Long-form brand campaigns
defer to marketing-agent.
-->
# Employer Brand — Glassdoor / Comparably — SKILL

Monitor + respond to employer-brand reviews on Glassdoor, Comparably, Indeed, Blind, and Levels.fyi. Includes scraping for new reviews, drafting empathy-first responses within the 7-day SLA, surfacing EVP testimonials, and tracking brand health metrics quarter-over-quarter. Defer long-form brand campaigns to `marketing-agent`.

## When to use

- Daily / weekly: poll Glassdoor + Comparably for new reviews; surface negatives.
- Response: draft 7-day-SLA empathy + action response per the review-response patterns in `role.md` "Glassdoor response patterns".
- Quarterly: pull review-trend metrics + EVP testimonial collection.
- Trigger phrases: "respond to Glassdoor", "negative review", "employer brand", "Comparably score", "Blind thread", "Levels.fyi reviews", "EVP statement".
- Defer to `marketing-agent` for: long-form brand campaigns, ad creative, paid LinkedIn / Built In sponsorship.

## Setup

```bash
# Scraping
export FIRECRAWL_API_KEY="fc-xxx"     # firecrawl-mcp
export BRIGHTDATA_API_TOKEN="xxx"     # paid scrape backstop for paywalled / aggressive AB

# UI automation for responses (no public API on Glassdoor / Comparably for responses)
# playwright-mcp covers session-cookied browser actions

# ATS + employee comm for testimonial collection
export GREENHOUSE_API_KEY="harvest_xxx"
export TYPEFORM_TOKEN="tfp_xxx"

# Glassdoor employer login (for paid Enhanced Profile API endpoints, if subscribed)
export GLASSDOOR_PARTNER_ID="xxx"
export GLASSDOOR_PARTNER_KEY="xxx"
```

Auth model:
- **Glassdoor responses:** No public response API. Free Employer Account is the manual path. Automate via `playwright-mcp` with stored session cookies.
- **Comparably responses:** Same — UI only, automate via `playwright-mcp`.
- **Glassdoor Job Search API:** Partner-only; rarely granted to non-job-board sites.
- **Levels.fyi:** Public data, scrape-friendly. No API.
- **Indeed Employer:** Limited API for company-profile + reviews-read; no response API.

## Common recipes

### Recipe 1: Scrape Glassdoor reviews page (firecrawl)
```bash
curl -s -X POST -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.firecrawl.dev/v2/scrape" \
  -d '{
    "url": "https://www.glassdoor.com/Reviews/Acme-Reviews-E12345.htm",
    "formats": ["markdown", "extract"],
    "extract": {
      "schema": {
        "reviews": [{
          "rating": "number",
          "date": "string",
          "title": "string",
          "pros": "string",
          "cons": "string",
          "advice_to_management": "string",
          "is_current_employee": "boolean"
        }]
      }
    }
  }'
```
Returns structured review JSON. Polite cadence: ≤2 req / min per page; respect robots.

### Recipe 2: Detect new negative reviews (Python diff loop)
```python
import json, requests, hashlib, pathlib, os
prev = pathlib.Path("glassdoor_state.json")
state = json.loads(prev.read_text()) if prev.exists() else {}
new = requests.post(
  "https://api.firecrawl.dev/v2/scrape",
  headers={"Authorization": f"Bearer {os.environ['FIRECRAWL_API_KEY']}"},
  json={"url": "https://www.glassdoor.com/Reviews/Acme-Reviews-E12345.htm",
        "formats": ["extract"], "extract": {"schema": {...}}}
).json()["data"]["extract"]["reviews"]
seen = set(state.get("seen", []))
new_neg = []
for r in new:
  key = hashlib.sha256(f"{r['date']}|{r['title']}".encode()).hexdigest()
  if key not in seen and r["rating"] <= 2:
    new_neg.append(r); seen.add(key)
prev.write_text(json.dumps({"seen": list(seen)}))
print(json.dumps(new_neg, indent=2))
```

### Recipe 3: Respond to a Glassdoor review (Playwright)
```python
# playwright-mcp / sync_playwright pattern
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
  ctx = p.chromium.launch_persistent_context("./gd_profile", headless=False)  # use saved login
  page = ctx.new_page()
  page.goto("https://www.glassdoor.com/employers/<your-company>/respond")
  page.get_by_role("button", name="Respond").click()
  page.get_by_label("Your response").fill(open("response.md").read())
  page.get_by_role("button", name="Post response").click()
```
Pull response from `role.md` "Glassdoor response patterns" → fill specifics → review with HR before posting.

### Recipe 4: Scrape Comparably company page
```bash
curl -s -X POST -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "Content-Type: application/json" \
  "https://api.firecrawl.dev/v2/scrape" \
  -d '{
    "url": "https://www.comparably.com/companies/acme",
    "formats": ["extract"],
    "extract": {
      "schema": {
        "culture_score": "number",
        "compensation_score": "number",
        "leadership_score": "number",
        "recent_reviews": [{"rating": "number", "category": "string", "text": "string"}]
      }
    }
  }'
```

### Recipe 5: Scrape Blind workplace topic threads
```bash
# Blind doesn't allow logged-out access for many threads; use Brightdata for paywalled scrape.
curl -s -X POST -H "Authorization: Bearer $BRIGHTDATA_API_TOKEN" \
  -d '{"url": "https://www.teamblind.com/company/Acme", "country": "us"}'
```
Blind threads are recruiter-sensitive; flag negative themes to HR; do NOT respond on Blind (anonymity is a tripwire — explicit Blind responses backfire).

### Recipe 6: Pull Levels.fyi company comp page
```bash
curl -s -X POST -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -d '{
    "url": "https://www.levels.fyi/companies/acme/salaries/software-engineer",
    "formats": ["extract"],
    "extract": {"schema": {"levels": [{"level": "string", "base": "number", "stock": "number", "bonus": "number"}]}}
  }'
```

### Recipe 7: Collect candidate-experience testimonials via Typeform
```bash
# Build a 5-question Typeform: net-promoter + verbatim quote consent + role + start date + photo opt-in
LINK="https://acme.typeform.com/to/<form_id>?employee_id={{employee_id}}"
# Pull responses:
curl -s -H "Authorization: Bearer $TYPEFORM_TOKEN" \
  "https://api.typeform.com/forms/<form_id>/responses?since=2026-01-01T00:00:00Z" \
  | jq '.items[] | {role: .answers[0].text, quote: .answers[1].text, nps: .answers[2].number}'
```

### Recipe 8: Update Greenhouse careers page testimonials via Job Board API
```bash
# Greenhouse Job Board: testimonials appear in the careers page; managed in UI but content
# can be pushed via Custom Branding (paid Inclusion + Career Sites tier).
# Free path: render testimonials in your own /careers page; embed Greenhouse job-board iframe.
curl -s "https://boards-api.greenhouse.io/v1/boards/$GREENHOUSE_BOARD_TOKEN/jobs" \
  | jq '.jobs[] | {id, title, departments: .departments[].name}'
```

### Recipe 9: Pull Glassdoor Job Search API (partner-only)
```bash
# If granted partner credentials:
curl -s "https://api.glassdoor.com/api/api.htm?v=1&format=json&t.p=$GLASSDOOR_PARTNER_ID&t.k=$GLASSDOOR_PARTNER_KEY&action=jobs&q=engineer&l=san-francisco"
```
Rarely granted; treat as fallback.

### Recipe 10: Weekly review digest to Slack
```bash
# Aggregate: # new reviews / avg rating / new negatives / response SLA breach count
# Output to slack-mcp #employer-brand channel weekly.
```

### Recipe 11: Trigger employer-brand badge re-issue (Comparably annual cycle)
```bash
# Comparably issues "Best Companies for X" badges based on Q1-Q4 data; encourage employees
# to refresh reviews 30 days before badge cycle close (typically Nov + May).
# Send slack-mcp company-wide message + Typeform link 30 days pre-cycle.
```

## Examples

### Example 1: 7-day SLA negative review response
**Goal:** New 1-star review on Glassdoor about onboarding → respond within 7 days, empathy + action.
**Steps:**
1. Recipe 2 fires (daily cron) → new 1-star detected.
2. Pull response template from `role.md` "Glassdoor response patterns".
3. Fill specifics: acknowledge the onboarding gap; cite the change in flight ("we shipped new 30-60-90 plans in Q2; details: <link>"); offer offline conversation.
4. Route to HR head for sign-off.
5. Recipe 3 (Playwright) posts the response.

**Result:** Response live within 7 days; future candidates see the company engaging; 30% reduction in negative-review weighting observed industry-wide.

### Example 2: EVP testimonial library for career site
**Goal:** Replace 3 generic testimonials with 12 role-diverse + identity-diverse real-voice quotes.
**Steps:**
1. Recipe 7: send Typeform to 100 employees across role / level / tenure / EEO-1 categories.
2. Filter for `nps>=9` + photo-opt-in + quote-consent.
3. Curate 12; pair with role / tenure / 1-line "why I stay".
4. Coordinate with `marketing-agent` for visual treatment + career-page rebuild.
5. Surface on Greenhouse Inclusion-enabled career page + LinkedIn Life page.

**Result:** Career site reflects real voices; applicant rate lifts; CandE survey "do you trust the company's brand?" lifts 15-25 points.

### Example 3: Quarterly employer-brand health review
**Goal:** Surface trends to People leadership.
**Steps:**
1. Recipe 1 + Recipe 4 + Recipe 6 scrape last 90 days of reviews.
2. Score: avg Glassdoor stars trend, % positive, top 3 themes from negative reviews (use sentiment + keyword bucketing), Comparably culture/comp/leadership scores trend.
3. Cross-cut with attrition data (handoff to `operations-agent`).
4. Output: 1-page pulse + recommended actions.

**Result:** Brand-health data → action plan → owner per theme.

## Edge cases / gotchas

- **Glassdoor + Comparably APIs are limited.** No bulk-response API. Plan around Playwright UI automation; rate-limit and use a stable session profile.
- **Glassdoor displays only verified employer responses.** A free Employer Account is required to respond; "claim your company" first.
- **Defamation + retraction.** Reviews violating Glassdoor's Community Guidelines (specific defamation, real names, threats) can be flagged for removal; don't lean on this — it's slow + denial rate is high. Focus on response, not removal.
- **Blind is a tripwire.** Don't post on Blind as the company. Anonymity culture is hostile to corporate accounts; backlash is severe. Flag themes internally only.
- **Levels.fyi accuracy.** Crowdsourced; outliers + role-title noise common. Use for ranges, not precise points.
- **Response template robotics.** Avoid `Dear valued teammate, your feedback is important to us` — universally hated. Use `role.md` patterns: specific acknowledgment + specific change + offline channel.
- **Astroturfing risk.** Don't incentivize 5-star reviews ("post a 5-star and we'll Venmo $20" violates TOS + FTC). Just ask employees to share; let stars happen.
- **Scrape cadence.** Don't aggressive-scrape Glassdoor — Cloudflare/bot-detection blocks you. firecrawl-mcp's rotating IPs handle moderate volume; for paywalled / aggressive AB use brightdata-mcp.
- **PII in testimonials.** Get explicit written consent (Typeform consent question + opt-out window). Defer GDPR / CCPA wording to `legal-counsel`.
- **Defer to `marketing-agent`** for: long-form EVP campaign, paid LinkedIn Life / Built In sponsorship, video production. Recruiter owns brand monitoring + review response + EVP testimonial collection — marketing owns brand creation.

## Sources

- [Glassdoor for Employers](https://www.glassdoor.com/employers/)
- [Glassdoor — claim your free employer account](https://www.glassdoor.com/employers/account/account.htm)
- [Comparably for Employers](https://www.comparably.com/companies)
- [Workology — Employer Branding 2026](https://www.workology.com/employer-branding-2026/)
- [Levels.fyi (public data)](https://www.levels.fyi/)
- [Firecrawl docs](https://docs.firecrawl.dev/)
- [Indeed Employer reviews](https://www.indeed.com/companies)
- [Talent Board — CandE Awards](https://www.thetalentboard.org/cande-research-reports/)
