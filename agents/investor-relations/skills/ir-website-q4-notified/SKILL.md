<!--
Source: https://www.q4inc.com/products/website-platform/
Source: https://www.notified.com/products/investor-website
Source: https://www.q4inc.com/blog/capital-markets-day-best-practices
Source: https://www.deque.com/axe/
Reference role.md: "IR website playbook"
Round 2 enrichment: monthly playwright-mcp audit script + Q4 vs Notified comparison + CMS edit recipes + AGM virtual + accessibility checklist.
-->

# IR website management (Q4 Inc. / Notified)

Manages the public-company IR website (events calendar, stock quote, news room, SEC filings linkout, ESG hub, AGM virtual). Q4 Inc. is the 2026 dominant platform; Notified is the alt with AI-personalization for institutional landing pages. Runs monthly QA via `playwright-mcp` for broken links + load times + WCAG 2.1 accessibility.

## When to use

- Monthly IR website audit (broken links / load time / accessibility / SEC filings freshness).
- Updating events calendar (earnings calls, conference appearances, investor day, AGM).
- ESG hub / sustainability report linkout updates.
- Coordinating AGM virtual + investor day registration pages.
- Posting earnings deck, press release, transcript within minutes of earnings call.
- Trigger phrases: "IR website audit", "update events calendar", "Q4 update", "Notified update", "IR site QA", "IR website accessibility".

NOT for: drafting press releases (use `quarterly-earnings-press-release`); investor day deck (use `investor-day-capital-markets-day`); SEC filings drafting (use `10k-10q-drafting-workiva`).

## Setup

```bash
# Q4 Inc. (preferred 2026)
export Q4_API_KEY="<from Q4 Admin -> Integrations>"
export Q4_TENANT_ID="<from Q4 Admin>"

# Notified (alt)
export NOTIFIED_API_KEY="<from Notified Admin>"

# Tools: playwright-mcp for audits; firecrawl-mcp for competitor benchmark; axe-core CLI
npm i -g @axe-core/cli
```

Auth / API key requirements:
- `Q4_API_KEY` — Q4 Platform subscription ($20-$100K/yr).
- `NOTIFIED_API_KEY` — Notified Investor Website ($15-$50K/yr).
- Free fallback: WordPress + custom IR template + manual EDGAR linkout. Most public cos use Q4 or Notified.

Data inputs:
- Stock quote widget data feed (Q4/Notified provide; if custom: Yahoo Finance or alpha-vantage-mcp).
- SEC filings list (auto from SEC EDGAR).
- Upcoming events list (curated by IR).
- ESG report URLs (latest + 3 prior years).
- AGM proxy + virtual meeting URL.

## Standard IR website sections

| Section | Owner | Update Frequency | Source |
|---------|-------|-----------------|--------|
| Home (latest stock, news, events) | IR | Real-time | Auto |
| Press Releases | IR | Per release | Wire feed |
| SEC Filings | IR | Auto from EDGAR | `sec-edgar-mcp` |
| Events Calendar | IR | Weekly | Manual + Q4/Notified |
| Earnings Center (recordings, transcripts, decks) | IR | Per Q | Q4/Notified webcast asset |
| Stock Quote + Chart | Auto | Real-time | Q4/Notified widget |
| Financial Information | IR | Per Q | Workiva linkout |
| ESG / Sustainability Hub | IR + ESG team | Per report | PDF linkout |
| Governance (board, committees, ethics) | IR + GC | Per proxy | `proxy-statement-drafting` |
| AGM Information | IR | Annual | Q4/Notified AGM module |
| Analyst Coverage | IR | Quarterly | Bloomberg ANR |
| Investor FAQ | IR | Quarterly | `shareholder-qa-maintenance` |
| Contact | IR | Static | Manual |
| Email Alerts Signup | IR | Auto | Q4/Notified |

## Monthly audit (playwright-mcp)

```python
from playwright.sync_api import sync_playwright
import json

PAGES = ["/", "/news", "/sec-filings", "/financials", "/events",
         "/esg", "/governance", "/agm", "/faq", "/contact"]

results = {}
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for path in PAGES:
        url = f"https://ir.company.com{path}"
        page.goto(url, wait_until="networkidle")
        load_ms = page.evaluate("performance.timing.loadEventEnd - performance.timing.navigationStart")
        broken = []
        for link in page.locator("a").all():
            href = link.get_attribute("href")
            if href and href.startswith("http"):
                # HEAD request via fetch
                status = page.evaluate(f"fetch('{href}', {{method: 'HEAD'}}).then(r => r.status).catch(() => 0)")
                if status >= 400 or status == 0:
                    broken.append((href, status))
        results[path] = {"load_ms": load_ms, "broken_links": broken}
    browser.close()
print(json.dumps(results, indent=2))
```

## Common recipes

### Recipe 1 — Q4: list upcoming events
```bash
curl -H "Authorization: Bearer $Q4_API_KEY" \
  "https://api.q4inc.com/v1/events?upcoming=true&tenant=$Q4_TENANT_ID"
```

### Recipe 2 — Q4: create new event (earnings call)
```bash
curl -X POST -H "Authorization: Bearer $Q4_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "earnings_call",
    "title": "Q2 2026 Earnings Call",
    "start": "2026-07-30T17:00:00Z",
    "webcast_url": "https://webcast.notified.com/...",
    "dial_in": "+1-800-XXX-XXXX",
    "passcode": "XXXXXX"
  }' \
  "https://api.q4inc.com/v1/events"
```

### Recipe 3 — Q4: post earnings asset (deck/transcript)
```bash
curl -X POST -H "Authorization: Bearer $Q4_API_KEY" \
  -F "type=earnings_deck" \
  -F "file=@Q2_2026_Earnings_Deck.pdf" \
  -F "publish_at=2026-07-30T17:00:00Z" \
  "https://api.q4inc.com/v1/assets"
```

### Recipe 4 — Notified: AI-personalization config
```bash
curl -X POST -H "Authorization: Bearer $NOTIFIED_API_KEY" \
  -d '{
    "segment": "institutional_traffic",
    "landing_emphasis": ["earnings_center", "financial_information", "investor_day"],
    "auto_detect_referrer": true
  }' \
  "https://api.notified.com/v1/website/personalization"
```

### Recipe 5 — Competitor IR benchmarking (Firecrawl)
```bash
for peer_url in $PEER_IR_URLS; do
  mcp call firecrawl-mcp scrape --url $peer_url/investors --formats markdown
done
# Compare event-update cadence, ESG hub depth, AGM module completeness
```

### Recipe 6 — Accessibility audit (axe-core)
```bash
npx @axe-core/cli https://ir.company.com --tags wcag2aa --save ax_report.json
# Returns WCAG 2.1 AA violations; fix all critical + serious
```

### Recipe 7 — SEC filings sync check
```bash
# Compare Q4 SEC filings list to actual EDGAR
curl -H "Authorization: Bearer $Q4_API_KEY" \
  "https://api.q4inc.com/v1/sec-filings" > q4_filings.json

mcp call sec-edgar-mcp list_filings --ticker=$TICKER --limit=30 > edgar_filings.json

# Diff to ensure all EDGAR filings appear on IR site
python -c "
import json
q4 = {f['accession']: f for f in json.load(open('q4_filings.json'))}
edgar = {f['accession']: f for f in json.load(open('edgar_filings.json'))}
missing = set(edgar) - set(q4)
print(f'Missing from IR site: {missing}')
"
```

### Recipe 8 — Load-time benchmark
```bash
# Target: <2s LCP (Largest Contentful Paint) per Q4/Notified IR standard
mcp call playwright-mcp run_script \
  --script "(async () => { const t = await page.evaluate('performance.getEntriesByType(\"largest-contentful-paint\")'); return t; })()"
```

### Recipe 9 — AGM virtual setup (Broadridge / Q4)
```bash
# Q4 AGM module
curl -X POST -H "Authorization: Bearer $Q4_API_KEY" \
  -d '{
    "type": "agm_virtual",
    "date": "2027-05-15T14:00:00Z",
    "broadridge_meeting_id": "XXX",
    "voting_deadline": "2027-05-14T17:00:00Z",
    "registration_url": "..."
  }' \
  "https://api.q4inc.com/v1/agm"
```

### Recipe 10 — ESG hub URL refresh
```bash
curl -X POST -H "Authorization: Bearer $Q4_API_KEY" \
  -d '{
    "type": "esg_report",
    "year": 2026,
    "url": "https://cdn.../sustainability_2026.pdf",
    "framework": ["IFRS_S1", "IFRS_S2", "GRI", "SASB"]
  }' \
  "https://api.q4inc.com/v1/esg"
```

## Examples

### Example 1: Earnings day playbook

**Goal:** Q2 2026 call July 30, 4:00 PM ET; deck + press release + transcript live on IR site within minutes.

**Steps:**
1. T-3 days: confirm event already posted (Recipe 2).
2. T-1 day: stage earnings deck PDF + speaker notes (Recipe 3, future-dated publish).
3. T-30 min: press release wire (paired with `quarterly-earnings-press-release`).
4. T-0 (4:00 PM ET): earnings call begins; live webcast on Q4 module.
5. T+5 min: press release auto-syncs to IR site via wire feed.
6. T+30 min: deck publishes (Recipe 3 scheduled).
7. T+24h: transcript posts (Q4 auto-pulls from Notified webcast).
8. T+48h: SEC filings sync check (Recipe 7) — 8-K Item 2.02 on EDGAR + IR.

**Result:** No gap; all assets accessible same day; analyst notes cite IR-website availability.

### Example 2: Monthly site audit

**Goal:** First Monday of each month — full QA before any quarterly cycle starts.

**Steps:**
1. Run playwright-mcp audit script (above) across 10 sections.
2. Run axe-core (Recipe 6).
3. Run SEC filings sync (Recipe 7).
4. Benchmark vs 3 peer IR sites (Recipe 5).
5. Compile issues into Linear tickets (via `linear-mcp`).
6. Fix critical/serious within 5 business days; backlog medium.
7. Quarterly: re-baseline LCP (Recipe 8) — target <2s.

**Result:** No broken links; WCAG 2.1 AA compliance; load times competitive.

## Edge cases / gotchas

- **Q4 vs Notified switching cost.** Migration takes 3-6 months; preserve URL structure during migration to avoid SEO loss.
- **SEC EDGAR auto-sync lag.** Q4/Notified pull EDGAR filings hourly; if you need same-minute appearance, push via API simultaneously with EDGAR submission.
- **Webcast asset rights.** Notified-hosted webcasts often have replay-window limits (1 year typical); check before relying on long-term archive.
- **AGM virtual + Broadridge integration.** Broadridge meeting ID required for proxy voting integration; Q4 AGM module integrates but config is tricky.
- **ESG hub framework labels.** IFRS S1/S2 + SASB + GRI + TCFD labels matter for ratings agency scrapers; consistency required.
- **Accessibility WCAG 2.1 AA.** Required for federal contractors + best practice for all. Top violations: missing alt text, low contrast, focus indicators.
- **CMS edit permissions.** Q4 lets you create role-tiers; default everyone-editor is a risk. IR + GC + comms only with publish rights.
- **Real-time stock quote widget delay.** Free feeds = 20 min delayed; paid = real-time. Investors expect real-time.
- **Conference appearance URL sync.** Coordinate with sell-side host calendar; don't double-book.
- **ESG report PDF size.** >25MB PDFs annoy mobile; offer HTML version or chaptered PDFs.
- **Investor day registration page.** Q4/Notified module collects RSVP + emails; comply with GDPR if EU registrants.
- **Email alerts subscriber consent.** Opt-in only; CAN-SPAM + GDPR compliance.
- **Mobile-friendly check.** 30%+ of IR traffic mobile in 2026; responsive must work.

> Mandatory disclaimer (when material disclosures touch IR website): if IR website is used as a recognized channel of distribution for Regulation FD purposes, **consult licensed securities counsel** for Reg FD compliance, especially for pre-announced material information posting timing and channel-of-distribution sufficiency.

## Sources

- Q4 Inc. Website Platform: https://www.q4inc.com/products/website-platform/
- Notified Investor Website: https://www.notified.com/products/investor-website
- Q4 Capital Markets Day Best Practices: https://www.q4inc.com/blog/capital-markets-day-best-practices
- WCAG 2.1 AA Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- Deque axe-core: https://www.deque.com/axe/
- Broadridge Virtual AGM: https://www.broadridge.com/solution/virtual-annual-meetings
- SEC Reg FD Channels of Distribution: https://www.sec.gov/divisions/corpfin/guidance/regfd-interp.htm
- See `role.md` -> "IR website playbook"

## Related skills

- `investor-day-capital-markets-day` — investor day registration + livestream.
- `quarterly-earnings-press-release` — earnings asset publishing.
- `esg-investor-reporting-gri-sasb-tcfd` — ESG hub content.
- `proxy-statement-drafting` — AGM + governance page updates.
