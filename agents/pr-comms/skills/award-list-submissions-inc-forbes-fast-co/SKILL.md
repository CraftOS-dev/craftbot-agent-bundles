<!--
Source: https://www.inc.com/inc5000/apply
Forbes 30 Under 30: https://www.forbes.com/30-under-30/
Fast Company MIC: https://www.fastcompany.com/most-innovative-companies
Bospar award guide: https://bospar.com/how-to-master-award-submissions/
-->
# Award + List Submissions — Inc 5000 / Forbes 30U30 / Fast Co MIC — SKILL

Award submissions via `playwright-mcp` form automation from a Notion criteria DB. Eligibility verification FIRST (revenue / age / category). Application tailored per award's judging criteria (not generic narrative). Quarterly `firecrawl-mcp` scan of award index sites for new deadlines.

## When to use this skill

- **Inc 5000** — US fastest-growing private companies (revenue-verified).
- **Forbes 30 Under 30** — under-30 individual or team achievement.
- **Fast Company Most Innovative Companies + Brands That Matter** — innovation per industry category.
- **BuiltIn Best Places to Work + Best Startups**.
- **G2 Best Software / Reports** — review-driven, requires G2 vendor profile.
- **Webby / Crunchies / Comparably / Glassdoor Best Places / AdWeek Brand Genius** — category-specific.
- **Industry-specific** — SaaStr Awards, Modern Healthcare 100, Inc Best Workplaces, etc.

**Do NOT use this skill when:**
- The submission is for an analyst MQ/Wave — use `analyst-relations-gartner-forrester-idc`.
- The submission is a conference CFP — use `conference-speaking-submission`.
- The "award" is pay-to-play (no judging, just payment) — push back; it's noise, not credibility.

## Setup

### playwright-mcp (form automation)

Already configured in `agent.yaml`. Most awards = bespoke web forms, no API. `playwright-mcp` scripts navigate, fill, upload, screenshot confirmation.

```bash
mcp tool playwright-mcp.browser_navigate --url "https://www.inc.com/inc5000/apply"
mcp tool playwright-mcp.browser_snapshot
```

### Notion criteria DB schema

Per award row:
- `award_name` (text)
- `category` (select: revenue-growth, workplace, innovation, etc.)
- `region` (select: US, Global, EU, etc.)
- `eligibility_criteria` (rich text — pulled from award site)
- `judging_criteria` (rich text — pulled from award site)
- `application_url` (URL)
- `deadline` (date)
- `result_date` (date)
- `application_essay_word_limit` (number)
- `last_year_submitted` (date)
- `last_year_result` (select: won, finalist, shortlisted, none)
- `supporting_docs_required` (multi-select: financials, pitch_deck, customer_refs, etc.)
- `status` (select: not-eligible, planned, drafting, submitted, won, lost)
- `playwright_script` (text — path to automation script per award)

### Company facts source DB

Pull from `notion-mcp`:
- Revenue (latest verified + prior 3 years)
- Headcount
- Founding year + HQ
- Customer count + named (with permission)
- Funding raised
- Press coverage placements (linked from coverage tracker)
- Customer outcomes / case studies

## Common recipes

### Recipe 1: Eligibility check (Claude verifies BEFORE drafting)

```python
# Pull eligibility criteria + company facts
criteria = notion.query(filter={"award_name": "Inc 5000"})[0]['eligibility_criteria']
company = notion.query(database="company_facts")[0]

prompt = f"""
You are checking eligibility for {criteria['award_name']}.

ELIGIBILITY CRITERIA:
{criteria}

COMPANY FACTS:
- Revenue 2022: {company['revenue_2022']}
- Revenue 2025: {company['revenue_2025']}
- HQ: {company['hq']}
- Founded: {company['founded']}
- For-profit: {company['for_profit']}
- Private: {company['private']}

For EACH criterion, output: ELIGIBLE / NOT ELIGIBLE / NEEDS DATA, with reasoning.
"""
eligibility = claude(prompt)
```

Inc 5000 checks (2026 cycle):
- $100K+ revenue 2022
- $2M+ revenue 2025
- US-based
- Privately held
- For-profit
- Independently operated (not subsidiary)

Forbes 30 Under 30:
- Nominee under 30 as of Jan 1, 2026
- Individual achievement (not company-level)
- US or named-region edition

Fast Co MIC:
- Innovation per industry category
- Demonstrable business impact in past 12 months
- Customer/market response evidence

### Recipe 2: Application essay generation (per award criteria)

```python
# DO NOT submit generic company narrative.
# Tailor to the award's STATED judging criteria.

prompt = f"""
Draft {award['application_essay_word_limit']}-word application essay for {award['name']}.

JUDGING CRITERIA: {award['judging_criteria']}

COMPANY FACTS: {company_facts}
RECENT MILESTONES: {milestones_last_12mo}
CUSTOMER OUTCOMES: {customer_proof}
PRESS COVERAGE: {coverage_highlights}

REQUIREMENTS:
- Hit EVERY judging criterion explicitly
- 1 specific number per claim (no "significant growth" — say "247% revenue growth")
- 2-3 named customers per case study (with permission)
- 1 outlet citation per credibility claim
- NO buzzwords ("game-changing", "industry-leading", "world-class")
- First sentence = the strongest claim
- Final paragraph = forward trajectory + why we deserve recognition

Output the essay only, no metadata.
"""
essay = claude(prompt)
```

### Recipe 3: Supporting documents prep

```bash
# Each award requires different supporting docs; pull from Notion criteria DB
docs=$(notion query "awards WHERE award_name='Inc 5000'" | jq -r .supporting_docs_required)

# For each doc type, render via skill
for doc in $docs; do
  case $doc in
    "audited_financials")
      # Pull from QuickBooks / Xero via cli-anything
      curl -X GET "https://quickbooks.api.intuit.com/v3/company/$COMPANY_ID/reports/ProfitAndLoss?start_date=2022-01-01&end_date=2025-12-31" \
        -H "Authorization: Bearer $QB_TOKEN" \
      > financials.json
      # Render as pdf
      python financials_to_pdf.py financials.json > supporting/inc5000_financials.pdf
      ;;
    "pitch_deck")
      # Pull latest from drive
      gdrive download --path "Brand Assets/Pitch Deck 2026.pptx" -o supporting/inc5000_deck.pptx
      ;;
    "customer_references")
      # Pull from notion reference DB
      notion query "customer_references WHERE press_permission=true" \
      | python format_refs.py > supporting/inc5000_refs.pdf
      ;;
  esac
done
```

### Recipe 4: Playwright form submission (Inc 5000)

```javascript
// playwright-mcp script: inc5000_submit.js
const browser = await playwright.chromium.launch();
const page = await browser.newPage();
await page.goto('https://www.inc.com/inc5000/apply');

// Click "Start Application"
await page.click('button:has-text("Start Application")');

// Fill company info
await page.fill('input[name="company_name"]', companyName);
await page.fill('input[name="company_website"]', companyWebsite);
await page.fill('input[name="hq_city"]', hqCity);
await page.selectOption('select[name="hq_state"]', hqState);
await page.fill('input[name="founding_year"]', foundingYear);

// Revenue verification
await page.fill('input[name="revenue_2022"]', revenue2022);
await page.fill('input[name="revenue_2023"]', revenue2023);
await page.fill('input[name="revenue_2024"]', revenue2024);
await page.fill('input[name="revenue_2025"]', revenue2025);

// Industry category
await page.selectOption('select[name="industry"]', industryCode);

// Upload financials
await page.setInputFiles('input[name="audited_financials"]', 'supporting/inc5000_financials.pdf');

// Application essay (250 words max)
await page.fill('textarea[name="growth_story"]', essay);

// Submit
await page.click('button:has-text("Submit Application")');

// Screenshot confirmation
await page.screenshot({ path: 'submissions/inc5000_confirmation_2026.png' });

// Extract confirmation number
const confirmationNumber = await page.textContent('.confirmation-number');
console.log({ award: 'Inc 5000', confirmation: confirmationNumber, status: 'submitted' });
```

### Recipe 5: Forbes 30 Under 30 nomination

```javascript
// Self-nomination OR third-party nomination
const browser = await playwright.chromium.launch();
const page = await browser.newPage();
await page.goto('https://www.forbes.com/nominate-30-under-30/');

await page.fill('input[name="nominee_name"]', nominee.name);
await page.fill('input[name="nominee_email"]', nominee.email);
await page.fill('input[name="nominee_linkedin"]', nominee.linkedin);
await page.fill('input[name="nominee_age_jan2026"]', nominee.age);
await page.selectOption('select[name="category"]', nominee.category); // Tech, Finance, etc.

await page.fill('textarea[name="why_nominate"]', whyNominate); // 500 char max

await page.click('button:has-text("Submit Nomination")');
await page.screenshot({ path: 'submissions/forbes_30u30_confirmation.png' });
```

### Recipe 6: Fast Co MIC (essay-heavy)

Fast Company Most Innovative Companies has industry-specific categories. Pick correctly.

```python
# Generate per-category positioning
prompt = f"""
Draft a 750-word Fast Company MIC application for category "{category}".

CATEGORY CRITERIA: {fastco_categories[category]['criteria']}
PAST WINNERS IN CATEGORY: {fastco_categories[category]['past_winners']}
WHAT FASTCO LOOKS FOR: innovation that drives industry change, evidence of business impact, customer/market response

COMPANY ACHIEVEMENTS LAST 12 MONTHS:
{company['achievements_2025_2026']}

Structure:
- Paragraph 1: The thesis — what we innovated (1-line hook)
- Paragraph 2: The market context — why this innovation matters NOW
- Paragraph 3: The impact — measurable customer / market response
- Paragraph 4: The forward — what's next
"""
essay = claude(prompt)
```

### Recipe 7: Quarterly award discovery (firecrawl-mcp)

```bash
# Scan major award index sites for new deadlines
award_sites=(
  "https://www.inc.com/awards"
  "https://www.fastcompany.com/awards"
  "https://www.forbes.com/lists"
  "https://www.builtin.com/awards"
  "https://www.g2.com/awards"
  "https://www.webbyawards.com/"
  "https://www.glassdoor.com/award/best-places-to-work"
  "https://saastr.com/awards"
)

for url in "${award_sites[@]}"; do
  firecrawl scrape --url "$url" --output "awards/$(basename $url).md"
done

# Claude diffs new awards / deadlines
prompt="Compare current awards index against prior month. Surface NEW awards, NEW deadlines, NEW categories. Output as Notion-import JSON."
new_awards=$(claude --files awards/ --prompt "$prompt")

notion-mcp upsert_pages --db awards --data "$new_awards"
```

### Recipe 8: Post-submission tracking

```bash
# Update Notion with submission status + confirmation number
notion-mcp update_row --filter "award_name=Inc 5000 AND submission_year=2026" \
  --status "submitted" \
  --confirmation_number "$confirmation" \
  --submission_screenshot "submissions/inc5000_confirmation_2026.png"

# Calendar reminders for result dates
google-calendar-mcp create_event \
  --title "Inc 5000 2026 results expected" \
  --date "$result_date" \
  --reminder_minutes "1440"

# Result notification handling
# If shortlisted: prepare additional material
# If won: press release + LinkedIn + thought leadership angle
# If lost: log learning + iterate next cycle
```

## Examples — annual awards calendar

```yaml
Q1:
  - Inc 5000 (deadline March; results August)
  - Fast Co Most Innovative Companies (deadline Q4 prior year)
  - Comparably Best Places to Work (rolling)

Q2:
  - Forbes 30 Under 30 NA (deadline June)
  - SaaStr Awards (deadline May)

Q3:
  - Inc Best Workplaces (deadline April; results September)
  - Glassdoor Best Places to Work (Aug-Sep)
  - Webby Awards (deadline October)

Q4:
  - G2 Best Software (annual report submission deadline)
  - BuiltIn Best Places to Work (deadline October)
  - AdWeek Brand Genius (rolling nominations)

automation:
  - quarterly firecrawl scan for new awards/deadlines
  - notion calendar with deadlines + result dates
  - playwright scripts version-controlled per award
  - eligibility check claude run pre-draft
  - submission screenshot archived per attempt
  - result tracking + press release prep on win
```

## Edge cases

### Eligibility lies = disqualification
Don't fudge revenue, dates, headcount. Inc audits revenue against tax returns. False claims = blacklist + public embarrassment if discovered post-publication. Better to skip a year than risk disqualification.

### "Pay to win" awards
Many awards require entry fees. Distinguish:
- **Legitimate**: entry fee ($100-$500) covers judging admin (Webbies, AdWeek, most legit awards). Judging is editorial.
- **Pay-to-play**: $5K-$50K "fee" guarantees inclusion. Skip these. Not credible. Often visible as such on the application page itself.

### Multi-year strategy
Some awards (Inc 5000) reward sustained growth. Plan multi-year:
- Year 1: enter to establish baseline + learn process
- Year 2: optimize positioning + supporting docs
- Year 3: target rank improvement

Track year-over-year in Notion.

### Customer reference logistics
Awards often require 5-15 customer references for interview. Pull from `customer-reference-program-pr` skill DB. Pre-clear with each reference: "Award X may contact you for a 30-min call about our partnership; OK?"

### Application deadline = real
Awards don't accept late submissions. Build 7-day buffer:
- Internal deadline: 7 days before public deadline
- Legal review: 5 days before
- Final approval: 3 days before
- Submit: 1-2 days before

Don't submit at 11:59 PM — server outages happen, time zones differ.

### Essay length discipline
Awards specify essay word/character limits HARD. Going over → silent rejection on some platforms. Use `awk` or `wc -w` to verify before submit. Claude tends to overshoot — manually trim.

### Industry category selection
For multi-category awards (Fast Co MIC), submit in the category where competition is THINNEST + fit is highest. Pick wrong category → lost in a sea of equivalents.

### Forbes 30 Under 30 age trap
Age cutoff is Jan 1 of the publication year, not application year. Forbes 30U30 2026 list = nominees under 30 on Jan 1, 2026. Miss this by a month → ineligible.

### Past winners as benchmarks
Pull past 3 years' winners in your category via `firecrawl-mcp`. Study what they emphasized. Don't copy positioning, but understand the bar.

### Wins → press release amplification
Award win = press release angle. Workflow:
1. Win confirmed → notify via Notion
2. Press release scheduled within 24 hours (use `press-release-writing-distribution`)
3. LinkedIn org post + CEO post
4. Twitter announcement
5. Customer reference outreach: "We just won X; thanks for being part of the story"
6. Update website "Awards" page
7. Add to all future pitch decks + media kit

### Lost / not finalist → still useful
- Log learnings: what positioning didn't resonate?
- Some awards offer feedback request (uncommon, but ask)
- Iterate for next cycle
- Don't announce a loss; just don't mention it

### Form abandonment risk
Long forms (Fast Co MIC = 90+ min to complete) — browser timeouts, session expiry. Build playwright script to save state at each step. Resume from saved state on failure.

### Notion criteria DB upkeep
Award criteria change yearly. Run `firecrawl-mcp` quarterly to refresh criteria text. Don't rely on cached criteria from 2024 when applying in 2026.

### Anti-spam captcha workaround
Many submission forms have hCaptcha / reCAPTCHA. `playwright-mcp` can't solve these. Workflow:
1. Run automation up to captcha
2. Pause for human to solve (15-30 sec)
3. Continue automation post-captcha

Don't bypass captchas via third-party service — terms of service violation + ban risk.

## Sources

- **Inc 5000 application**: https://www.inc.com/inc5000/apply
- **Forbes 30 Under 30 nominations**: https://www.forbes.com/30-under-30/
- **Forbes 30U30 Wikipedia**: https://en.wikipedia.org/wiki/Forbes_30_Under_30
- **Fast Company MIC**: https://www.fastcompany.com/most-innovative-companies
- **Bospar award submission guide**: https://bospar.com/how-to-master-award-submissions/
- **BuiltIn Awards**: https://www.builtin.com/awards
- **Webby Awards**: https://www.webbyawards.com/
- **G2 Reports**: https://www.g2.com/categories
- **Glassdoor Best Places**: https://www.glassdoor.com/Award/Best-Places-to-Work-LST_KQ0,19.htm
- **Playwright docs**: https://playwright.dev/
