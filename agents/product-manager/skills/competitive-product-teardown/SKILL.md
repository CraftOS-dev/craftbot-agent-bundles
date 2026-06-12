<!--
Sources:
Reforge — https://www.reforge.com/blog/competitive-analysis-template
Firecrawl — https://docs.firecrawl.dev
BrightData — https://docs.brightdata.com
-->
# Competitive Product Teardown — SKILL

Structured competitor analysis: positioning, pricing tiers, feature surface, onboarding flow, retention mechanics, and recent releases. This pack uses Firecrawl for structured scraping, Playwright for interactive flow capture, and BrightData for paid-wall content.

## When to use

- Building a 1-pager competitor brief before a strategy session.
- Producing an "us vs them" matrix for sales enablement.
- Auditing a competitor's onboarding to inform our own redesign.
- Tracking competitor changelog signals (releases, pricing changes).
- Monthly competitive intel digest.

Trigger phrases: "teardown competitor X", "competitive analysis", "what features does X have", "compare us to X", "how does X onboard", "X just shipped Y".

## Setup

```bash
# Firecrawl MCP — structured competitor scraping
mcp tool firecrawl.viewer

# Playwright MCP — interactive flow capture (clickable screenshots)
mcp tool playwright.viewer

# BrightData MCP — paid-wall / anti-bot content
mcp tool brightdata.viewer

# Brave Search — open-web SERP queries
mcp tool brave-search.viewer
```

Auth:
- `FIRECRAWL_API_KEY` — from https://firecrawl.dev/dashboard. Free tier: 500 pages/mo.
- `BRIGHTDATA_API_TOKEN` — paid, ~$0.50-2.00 per page through Web Unlocker.
- `BRAVE_SEARCH_API_KEY` — free tier 2k queries/mo.

## Common recipes

### Recipe 1: Scrape the competitor's marketing site

```bash
mcp tool firecrawl.scrape \
  --url "https://competitor.com" \
  --formats '["markdown","links"]' \
  --onlyMainContent true \
| jq '{title: .data.metadata.title, content: .data.markdown}'
```

### Recipe 2: Crawl the pricing page (structured extract)

```bash
mcp tool firecrawl.scrape \
  --url "https://competitor.com/pricing" \
  --formats '["json"]' \
  --jsonOptions '{"prompt":"Extract every pricing tier with: tier name, monthly price, annual price, features list, seat limit, target audience"}' \
| jq '.data.json'
```

Returns structured tiers, e.g.:
```json
{
  "tiers": [
    {"name":"Starter","monthly_usd":29,"annual_usd":290,"features":["3 projects","2 seats"],"target":"solo founders"},
    {"name":"Pro","monthly_usd":79,"annual_usd":790,"features":["unlimited projects","10 seats","API access"],"target":"small teams"}
  ]
}
```

### Recipe 3: Crawl the changelog for recent releases

```bash
mcp tool firecrawl.scrape \
  --url "https://competitor.com/changelog" \
  --formats '["markdown"]' \
| jq -r '.data.markdown' \
| head -200
```

Then parse with a Claude prompt: "Summarize the last 30 days of releases; flag any feature that overlaps with our roadmap."

### Recipe 4: Playwright — capture onboarding flow screenshots

```python
# Use playwright-mcp to simulate the signup → first-action path
import asyncio
from playwright.async_api import async_playwright

async def capture_onboarding(competitor_url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(competitor_url)
        await page.screenshot(path="01-landing.png")

        # Click "Sign up free"
        await page.click("text=Sign up free")
        await page.screenshot(path="02-signup.png")

        # Fill the form
        await page.fill('input[type="email"]', "research+pm@yourdomain.com")
        await page.fill('input[type="password"]', "SafeResearch!2026")
        await page.click('button[type="submit"]')
        await page.screenshot(path="03-after-signup.png")

        # Walk the onboarding
        for i in range(4, 10):
            await page.wait_for_timeout(1500)
            await page.screenshot(path=f"{i:02d}-step.png")
            # Click "Next" or "Continue" if present
            try:
                await page.click("text=/Next|Continue|Get started/i", timeout=3000)
            except:
                break

        await browser.close()
asyncio.run(capture_onboarding("https://competitor.com"))
```

### Recipe 5: Map competitor features against ours (feature matrix)

```bash
# 1. Get our feature list from Notion / product page
# 2. Get competitor features (Recipe 2 jsonOptions prompt)
# 3. Build matrix

mcp tool notion.create_page \
  --parent '{"page_id":"<competitive-folder>"}' \
  --properties '{"title":[{"text":{"content":"Us vs Competitor X — Feature matrix"}}]}' \
  --children '[
    {"type":"table","table":{"table_width":4,"has_column_header":true,"has_row_header":true,"children":[
      {"type":"table_row","table_row":{"cells":[
        [{"text":{"content":"Capability"}}],[{"text":{"content":"Us"}}],[{"text":{"content":"Competitor X"}}],[{"text":{"content":"Gap"}}]
      ]}},
      {"type":"table_row","table_row":{"cells":[
        [{"text":{"content":"In-product notifications"}}],[{"text":{"content":"Yes (in-app)"}}],[{"text":{"content":"Yes (in-app + email)"}}],[{"text":{"content":"They have email; we do not"}}]
      ]}}
    ]}}
  ]'
```

### Recipe 6: BrightData — pull a paywalled/anti-bot competitor doc

```bash
# Use BrightData Web Unlocker for sites that block Firecrawl
curl -X POST "https://api.brightdata.com/unlocker" \
  -H "Authorization: Bearer $BRIGHTDATA_API_TOKEN" \
  -d '{"url":"https://hard-to-scrape-competitor.com/docs/api","format":"raw"}' \
| jq -r '.html' | pandoc -f html -t markdown
```

### Recipe 7: SERP intelligence — what queries does the competitor rank for

```bash
# Brave search results for branded + non-branded terms
for QUERY in "best project management for solo founders" "competitorX vs us" "competitorX review"; do
  mcp tool brave.search --query "$QUERY" --count 10 \
  | jq -r '.web.results[] | "\(.title) — \(.url)"'
  echo "---"
done
```

### Recipe 8: Onboarding flow audit (with screenshots)

```markdown
# Competitor X — Onboarding Audit (June 2026)

## Flow length
6 steps from signup → first value (~ 4 min)

## Step 1: Landing
![](01-landing.png)
- Hero copy: "Plan your next launch in 5 minutes"
- Primary CTA: "Sign up free" (top right + center)
- Social proof: customer logos x 8

## Step 2: Signup form
![](02-signup.png)
- Email + password only (no SSO option visible — gap?)
- "By signing up you agree..." link to ToS

## Step 3: Workspace setup
![](03-workspace.png)
- Forced: workspace name + URL slug
- Friction: no inline error if URL slug is taken; must submit to find out

[... continue per step]

## Observations vs us
- They have email-only signup; we have SSO from step 1 (advantage us)
- They surface social proof on every step; we only on landing (gap us)
- They have a "skip onboarding" link; we force completion (deliberate? hypothesis test)
```

### Recipe 9: Monthly competitive digest

```python
# Run weekly: scrape changelog, summarize, alert if new feature overlaps our roadmap
import requests, os, datetime

competitors = ["competitorA","competitorB","competitorC"]
this_month = datetime.date.today().strftime("%Y-%m")
report = f"# Competitive digest — {this_month}\n\n"

for c in competitors:
    r = requests.post("https://api.firecrawl.dev/v1/scrape",
        headers={"Authorization": f"Bearer {os.environ['FIRECRAWL_API_KEY']}"},
        json={"url": f"https://{c}.com/changelog","formats":["markdown"]}
    ).json()
    md = r["data"]["markdown"][:5000]
    report += f"## {c}\n\n{md}\n\n---\n\n"

# Send to Notion + Slack
# (use notion-mcp + slack-mcp)
```

### Recipe 10: Pricing-change watch

```bash
# Diff this month's pricing scrape vs last month's
mcp tool firecrawl.scrape --url "https://competitor.com/pricing" --formats '["markdown"]' \
| jq -r '.data.markdown' > pricing-current.md

diff pricing-last-month.md pricing-current.md > pricing-diff.txt

# If non-empty diff → alert Slack
if [ -s pricing-diff.txt ]; then
  mcp tool slack.post --channel "#product-leads" --text "Competitor X changed pricing this month. Diff: $(cat pricing-diff.txt | head -50)"
fi
```

## Examples

### Example 1: Strategy-session prep deck
**Goal:** 1-pager teardown of 3 competitors for tomorrow's strategy meeting.

**Steps:**
1. For each competitor: scrape marketing site + pricing + changelog (Recipes 1-3).
2. Capture onboarding screenshots via Playwright (Recipe 4).
3. Build feature matrix (Recipe 5).
4. Write the teardown into Notion using the Reforge structure (positioning / pricing / features / onboarding / retention / recent releases).
5. Export to PDF/PPTX for the meeting via `pdf` / `pptx` skills.

**Result:** 1-pager per competitor + a comparison matrix + an exec-ready deck.

### Example 2: New-feature competitive check
**Goal:** Engineering wants to ship "notifications center" — has competitor X done this?

**Steps:**
1. Search competitor docs (Recipe 1 on `competitor.com/docs/notifications`).
2. If they have it, watch their onboarding mention (Recipe 4 with specific path).
3. Audit their notification UX; capture screenshots.
4. Write up: what they do well, what we can differentiate on.
5. Feed into the PRD's "Solution approach — alternatives considered" section.

**Result:** PRD has cited competitive context; engineering avoids re-inventing.

## Edge cases / gotchas

- **Anti-bot detection.** Many SaaS sites block scrapers; Firecrawl handles most but BrightData is the escape hatch.
- **JavaScript-heavy sites.** Firecrawl renders JS; raw curl will miss content. Always use `firecrawl.scrape` for SPAs.
- **Terms of Service.** Scraping public pages is legal in most jurisdictions but read the competitor's robots.txt / ToS. Don't bypass paywalls with stolen credentials.
- **Account creation friction.** To audit onboarding, create a real account — use a research email (`pm-research+competitorX@your.com`). Don't use a teammate's email.
- **Rate limits.** Firecrawl free tier: 500 pages/mo. Plan crawls; cache results.
- **Outdated screenshots.** Pricing + onboarding pages change weekly. Re-capture before each big use.
- **Don't extrapolate from public.** Public site ≠ paid-tier reality. For deep audits, account for "what we see at $79/mo plan."
- **Don't trust the changelog.** Some competitors hide breaking changes. Cross-check with the support docs + community forums.
- **Avoid competitive paralysis.** A teardown informs strategy; it doesn't dictate it. Pick what we'll do *differently*, not just match.
- **Watch for legal lines.** Reverse-engineering an algorithm or scraping behind authentication may violate CFAA. Stay on the open web.

## Sources

- [Reforge — Competitive analysis template](https://www.reforge.com/blog/competitive-analysis-template)
- [Firecrawl docs](https://docs.firecrawl.dev)
- [BrightData Web Unlocker](https://brightdata.com/products/web-unlocker)
- [Playwright docs](https://playwright.dev/docs/intro)
- [Brave Search API](https://api.search.brave.com/app/documentation)
- [Mike Maples — How to do competitive analysis](https://www.floodgate.com)
- [Marty Cagan — Competitive context](https://www.svpg.com/competition)
