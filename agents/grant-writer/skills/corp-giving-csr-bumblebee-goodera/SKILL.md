---
name: corp-giving-csr-bumblebee-goodera
description: Research corporate giving / CSR programs and apply via the platform that mediates them (Benevity, YourCause, Bonterra, Goodera, MovingWorlds). Use when the user says "research <company>'s CSR" / "apply to Benevity" / "set up corp partnership" / "find corporate sponsors".
---

# Corporate giving + CSR (Benevity / YourCause / Bonterra / Goodera / MovingWorlds)

The 2026 corporate giving stack runs through a handful of platforms. Knowing which one mediates a target company's giving determines whether you apply to a corporate foundation, list as a Cause on a CSR platform, or pitch a corporate communications director directly. Multi-channel = direct giving + employee match + skills-based volunteering + workplace campaigns.

## When to use

- Researching a target Fortune 1000 corp's giving program
- Listing your org as a Cause on Benevity / YourCause / Bonterra
- Pitching a co-branded partnership (sponsorship + cause-marketing + employee volunteering)
- Applying for an employer match for an individual donor's gift
- Building a corporate-giving prospect list aligned to ESG / 10-K narrative
- Negotiating a multi-channel corporate partnership (cash + match + volunteer time)

Do NOT use this skill for:
- Foundation cultivation (private foundations) → `foundation-cultivation-program-officer`
- Federal grant prospect research → `grant-prospect-research-grants-gov-instrumentl-candid`
- Valuing volunteer hours as match against federal grants → `matching-funds-in-kind-strategy`
- General donor CRM tier decisions → `multi-grant-pipeline-mgmt`

## Setup

```bash
# No paid API for any CSR platform (you list your nonprofit and get discovered)
# Apply per platform via their nonprofit portal

# Benevity Causes
# https://causes.benevity.org/
# Pricing: free to list; Benevity takes ~2.9% disbursement fee

# YourCause CSRconnect (Blackbaud)
# Nonprofits register via Blackbaud GuideStar/Candid profile then claim
# https://www.blackbaud.com/products/yourcause-csrconnect

# Bonterra Causes
# https://www.bonterratech.com/

# Goodera (corporate volunteering)
# https://www.goodera.com/nonprofits

# MovingWorlds (skills-based volunteering)
# https://movingworlds.org/

# Optional: SEC EDGAR for corp 10-K research
# Tools: firecrawl-mcp, sec-edgar-mcp, gmail-mcp, notion-mcp
```

Auth / API key requirements:
- 501(c)(3) status verified via IRS Tax Exempt Org Search + Candid profile (claimed)
- W-9 on file
- Bank info (ACH) for Benevity disbursements
- An EIN-matched logo + 250-char mission statement + program-area tags
- For YourCause: claim your GuideStar/Candid profile first; CSRconnect pulls from there

## Common recipes

### Recipe 1: Identify which platform mediates a target corp's giving

```bash
# Step 1: Pull the corp's 10-K + sustainability report
curl "https://efts.sec.gov/LATEST/search-index?q=%22community+investment%22&forms=10-K&entityName=<CorpName>"

# Step 2: Scrape their Sustainability / Impact / ESG page
# via firecrawl-mcp
firecrawl scrape https://<corp>.com/sustainability

# Step 3: Look for platform name in:
# - "employee giving partner: Benevity" / "powered by YourCause" / "via Bonterra"
# - footer of giving page
# - employee handbook (if leaked / public)

# Step 4: Verify via Benevity Causes search
# https://causes.benevity.org/companies → search for your target corp
```

### Recipe 2: Apply to be a Benevity Cause

```markdown
## Benevity Causes application
1. Confirm 501(c)(3) IRS status active
2. Go to https://causes.benevity.org → Nonprofits → Register
3. Provide: EIN, legal name, DBA if used, mission (250 char), program areas, geo served
4. Upload: logo (PNG transparent), W-9, banking info (ACH)
5. Verification: Benevity confirms via IRS BMF + Candid
6. Profile live in 5-10 business days
7. Optional: enrich profile with photos, impact stories, video — improves discoverability
```

Benevity payout cadence: monthly ACH; ~2.9% admin fee deducted from grants.

### Recipe 3: Claim YourCause CSRconnect profile (Blackbaud)

```markdown
## YourCause via Blackbaud nonprofit portal
1. Sign in at https://www.blackbaud.com/nonprofits
2. "Claim your organization" → search EIN
3. Verify ownership (board member contact / email at org domain)
4. Update mission, programs, locations, impact metrics
5. Visible to YourCause CSRconnect member-corp employees within 24 hrs
6. Receive disbursements quarterly via Blackbaud check or ACH
```

### Recipe 4: Apply to Bonterra Causes

```markdown
## Bonterra Causes (formerly EveryAction / Network for Good / Salsa merger)
1. https://www.bonterratech.com/causes → Get listed
2. Verify EIN; upload W-9 + IRS letter
3. Set up disbursement (ACH preferred)
4. Tag program areas + impact stats
5. Bonterra mediates ~mid-market corp giving + DAF grants
```

### Recipe 5: Goodera nonprofit network (corporate volunteering)

```markdown
## Goodera — for volunteer-hour partnerships
1. https://www.goodera.com/nonprofits → Register
2. Define: volunteer opportunity types (1-hr virtual, half-day on-site, multi-week skills-based)
3. Set: max group size, ideal skills, prep time required from corp team
4. Goodera matches to 50K+ corporate clients
5. You host; corp pays per-volunteer fee to Goodera; you receive volunteer hours valued at Independent Sector rate
6. Track hours toward grant match using `matching-funds-in-kind-strategy`
```

### Recipe 6: MovingWorlds skills-based volunteering

```markdown
## MovingWorlds (skills-based, longer engagements)
1. https://movingworlds.org → For Social Enterprises and Nonprofits
2. Scope: project briefs (4-12 weeks, pro bono, defined deliverable)
3. Match: senior corporate employees on sabbatical / loaned executive programs
4. Common partners: Microsoft Garage, SAP Social Sabbatical, Salesforce Pro Bono
5. Output: deliverable that compounds capacity (strategy doc, system buildout, training)
```

### Recipe 7: Research a corporate prospect end-to-end

```markdown
## Corp prospect dossier (build in Notion)

| Field | Source |
|---|---|
| Legal name + DBA | SEC EDGAR + corp About page |
| Industry / NAICS | SEC EDGAR |
| HQ city + footprint | 10-K Item 2 (Properties) |
| Revenue + employee count | 10-K |
| ESG / CSR narrative | Sustainability report + 10-K Item 1A risk factors |
| Stated giving priorities | CSR report |
| Recent grantees | Press releases + corp foundation 990 (if foundation) + Benevity Causes |
| Giving platform | Identified per Recipe 1 |
| Foundation EIN (if has one) | ProPublica Nonprofit Explorer (search "<corp> Foundation") |
| Foundation avg grant | 990 PF Schedule I |
| Contact | LinkedIn for Head of Philanthropy / CSR / Community Affairs |
| Match policy | Workplace giving FAQ / Benevity company page |
```

### Recipe 8: Corporate proposal — different from foundation

```markdown
## Corp proposal sections (1-page brief + appendix)
1. Hook: corp's ESG narrative tie-in (3 sentences)
2. Project: our project + how it advances their stated priority + headline number
3. Visibility: co-branding, logo use, press release, event recognition
4. Employee engagement: volunteer opportunities, ERG match, lunch & learn
5. Ask: cash $ + match cap $ + volunteer hours target + multi-year? (most corps annual)
6. Impact reporting: 1-pager quarterly + headline metric annually
7. Appendix: 501(c)(3) letter, W-9, financials, prior corp partnerships

Length: 1-2 pages. Corps don't read 20-page proposals.
```

### Recipe 9: Multi-channel partnership ask

```markdown
## Stack the asks
- Cash sponsorship: $25K
- Employee match: up to $50K via Benevity (your existing program)
- Skilled volunteer: 200 hours through MovingWorlds (= ~$33.49/hr × 200 = $6,698 in-kind value)
- Volunteer day: 50 employees × 8 hours = 400 hours = ~$13,396 in-kind
- Cause marketing: holiday round-up campaign at point-of-sale
- Total program value: ~$95K cash + in-kind for a $25K cash ask
```

### Recipe 10: Corporate vs foundation cycle differences

```markdown
| Dimension | Corporate | Foundation |
|---|---|---|
| Fiscal year | Often calendar | Often July-June or Jan-Dec |
| Decision speed | Faster (weeks-months) | Slow (3-6 months) |
| Application | 1-2 page brief | 10-20 page proposal |
| Multi-year | Rare; annual renewal | Common (2-5 year) |
| Reporting | 1-page quarterly | Per-funder formal |
| Renewal driver | ESG narrative alignment | Outcomes + relationship |
| Decline reason | "Not aligned with this year's focus" | "Capacity constrained this cycle" |
| Recognition | Co-branding + press | Sometimes none requested |
```

## Examples

### Example 1: Research Microsoft Philanthropies giving for an education nonprofit

**Goal:** Pitch Microsoft on a STEM education partnership.

**Steps:**
1. Pull Microsoft 10-K (FY2025); locate "Community Investment" section.
2. Scrape https://www.microsoft.com/en-us/corporate-responsibility — note: AI for Good + Skills for Jobs are flagship priorities.
3. Confirm Microsoft uses Benevity for employee match; YourCause for some programs.
4. List your org as a Benevity Cause if not already.
5. Search LinkedIn → Microsoft Philanthropies Head of Education Programs.
6. Draft 1-page pitch tying STEM curriculum to Microsoft Skills for Jobs narrative.
7. Stack ask: $50K cash + employee match up to $25K + 5 days of Microsoft Garage skills-based volunteer.

**Result:** Multi-channel ask aligned to corp narrative; total value ~$90K against a $50K cash ask.

### Example 2: Apply for an employer match

**Goal:** Donor at Salesforce wants to match a $1K gift.

**Steps:**
1. Verify org is listed in Salesforce's giving portal (which runs on Bonterra + Benevity).
2. If not listed: register with Benevity (Recipe 2).
3. Donor submits match request via Salesforce.org Concierge.
4. Match processed within 30-60 days.
5. Acknowledge donor + log corporate match separately in CRM (so soft credit goes to donor, hard credit to Salesforce).

**Result:** $2K total ($1K + $1K match); donor stewarded; corp logged as repeat-engagement prospect.

## Edge cases / gotchas

- **Benevity 2.9% fee.** Net to nonprofit is 97.1% of gross gift. Budget accordingly.
- **YourCause profile claim requires Candid/GuideStar profile first.** Claim your free Candid profile; then claim in Blackbaud.
- **Disbursement cadence varies.** Benevity monthly; YourCause quarterly; Bonterra varies. Cash-flow plan accordingly.
- **Skills-based volunteering = in-kind, NOT cash.** Don't book as revenue; book as in-kind contribution at fair value per `matching-funds-in-kind-strategy`.
- **Corporate foundations vs direct giving.** Microsoft has BOTH a corporate foundation (Microsoft Philanthropies) AND direct corporate giving. Different application paths. Check 990 PF for foundation; check CSR report for direct.
- **Annual cycles.** Most corp giving rebases each January or each FY. Renewal asks belong in Q3-Q4 of the prior year.
- **ERG-driven giving.** Employee Resource Groups (women, BIPOC, LGBTQ+, veteran) often drive grant decisions. Identify the right ERG sponsor.
- **Cause-marketing legal review.** Co-branded campaigns may require state charitable solicitation registration; route binding contract review through `legal-counsel`.
- **Recipient stewardship.** Corp partnerships die without proactive reporting. Quarterly 1-pager is the minimum.
- **CSR narrative drift.** Reread the corp's latest CSR report annually; priorities shift (e.g., post-2024 many corps deprioritized DEI language).
- **Disclaimer.** For binding co-branding contracts, state charitable solicitation registration, or tax classification of donated goods, consult a qualified nonprofit attorney or CPA.

## Sources

- Benevity: https://benevity.com/
- Benevity Causes (nonprofit side): https://causes.benevity.org/
- YourCause CSRconnect (Blackbaud): https://www.blackbaud.com/products/yourcause-csrconnect
- Bonterra: https://www.bonterratech.com/
- Goodera: https://www.goodera.com/
- MovingWorlds: https://movingworlds.org/
- Stratus Live workplace giving comparison: https://stratuslive.com/blog/7-best-workplace-giving-platforms/
- Vantage Circle employee giving software roundup: https://www.vantagecircle.com/en/blog/best-employee-giving-software/
- MovingWorlds skills-based volunteering CSR software guide: https://movingworlds.org/blog/skills-based-volunteering-csr-software-for-employee-engagement/
- Independent Sector volunteer time rate (for in-kind valuation): https://independentsector.org/resource/value-of-volunteer-time/
- SEC EDGAR (for 10-K + CSR research): https://www.sec.gov/edgar
