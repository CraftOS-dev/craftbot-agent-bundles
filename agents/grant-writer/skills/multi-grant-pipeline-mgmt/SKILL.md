---
name: multi-grant-pipeline-mgmt
description: Build a portfolio-level grant pipeline (Instrumentl / Submittable / Fluxx / Foundant + Notion/Airtable) with win-rate metrics, by-stage tracking, and CRM tier matching org size. Use when the user says "build our pipeline" / "track all our grants" / "what's our win rate?" / "we have 20+ active grants".
---

# Multi-grant pipeline management

A grant pipeline is the org-level system that tracks every opportunity from prospect to closeout: stage, owner, deadline, amount, status, notes. At ≥10 active grants, Instrumentl is SOTA. Below that, Notion / Airtable + Google Calendar is sufficient. CRM tier matches org revenue: <$1M → Bloomerang + Notion; $1-10M → DonorPerfect; >$10M → Salesforce NPC. Win rate + average award size + funder concentration metrics drive strategy.

## When to use

- Org has 10+ active grants and wants a single source of truth
- Need to know "what's our win rate by funder type?"
- Building monthly pipeline review with ED / board
- Replacing spreadsheet-based tracking with a real system
- Selecting between Instrumentl / Submittable / Fluxx / Foundant
- Integrating grant pipeline with donor CRM (Bloomerang / DonorPerfect / Salesforce)
- Reporting pipeline health to board

Do NOT use this skill for:
- Specific grant prospect research → `grant-prospect-research-grants-gov-instrumentl-candid`
- Calendar-only deadline tracking → `grant-deadline-calendar-management`
- Foundation relationship cultivation → `foundation-cultivation-program-officer`
- Declined-grant pattern analysis → `declined-grant-iteration`

## Setup

```bash
# Tool tier by org size + grant volume

# < 10 active grants OR < $1M revenue
# - Notion (free → $8/user/mo) for pipeline DB
# - Google Calendar (free) for deadlines
# - Google Drive (free → Workspace) for proposal files

# 10-50 active grants OR $1-10M revenue
# - Instrumentl ($299/mo) for unified discovery + pipeline + AI assist
# OR
# - Submittable (free for nonprofits as applicants) for portal apps + Notion for cross-portal pipeline
# - DonorPerfect ($99-$329/mo) for donor + light grant tracking

# 50+ active grants OR > $10M revenue
# - Salesforce Nonprofit Cloud (free NPSP install; $20K-100K config) for full grant compliance
# - Fluxx Grantseeker (enterprise; sub via funder portals using Fluxx Grantmaker)
# - Foundant GrantHub ($1,500/yr) for dedicated grantseeker pipeline

# MCPs: notion-mcp, google-calendar-mcp, cli-anything (for Instrumentl/Salesforce REST), xlsx
```

Auth / API key requirements:
- Instrumentl: API key from account (Premium tier)
- Salesforce: connected app credentials + SOQL access
- Bloomerang: API key from account settings
- DonorPerfect: API key from account
- Notion: integration token via notion.so/my-integrations

## Common recipes

### Recipe 1: Pick the right tool tier

```markdown
## Tier decision tree

Annual grant revenue?
├── < $250K → Notion + Google Calendar (free)
├── $250K-1M → Notion + Google Calendar + light CRM (Bloomerang free tier)
├── $1M-5M → Instrumentl + DonorPerfect OR Foundant GrantHub
├── $5M-15M → Instrumentl + DonorPerfect/Salesforce NPSP (light)
└── $15M+ → Salesforce NPC fully configured + Fluxx Grantseeker for enterprise funders

## How many active grants at a time?
├── 1-5 → Spreadsheet OK
├── 6-15 → Notion DB minimum
├── 16-50 → Instrumentl / Foundant
└── 50+ → Salesforce or Fluxx
```

### Recipe 2: Pipeline DB schema (Notion / Airtable)

```markdown
## Core pipeline columns

| Column | Type | Notes |
|---|---|---|
| Opportunity name | Text | "<Funder> <Project> <FY>" |
| Funder | Relation → Funders DB | |
| Funder type | Select | Federal / State / Foundation / Corporate / DAF / Individual |
| Program area | Multi-select | Mirror funder's stated areas |
| Stage | Select | Research / Cultivating / LOI / Proposal Drafting / Submitted / Under Review / Awarded / Declined / Active / Reporting / Closed |
| Owner | Person | Grant writer or program lead |
| Reviewer | Person | Second eyes; usually ED or finance |
| Amount requested | Currency | |
| Amount awarded | Currency | Backfill at notice |
| Match required | Currency | |
| Project period | Date range | |
| LOI deadline | Date | |
| Full proposal deadline | Date | |
| Decision expected | Date | |
| Submitted on | Date | |
| Tracking number | Text | Grants.gov tracking # if federal |
| Status notes | Text | Latest update; iterate by date |
| Next action | Text | "Email PO for clarification" |
| Next action date | Date | |
| Documents | Files / relation | Link to Drive folder |
| Probability % | Number | 0-100 rough estimate |
| Weighted value | Formula | Amount requested × Probability |
```

### Recipe 3: Stage definitions + criteria

```markdown
## Stage gates (each = explicit criteria before advancing)

| Stage | Definition | Advance criteria |
|---|---|---|
| Research | Identified as prospect; researching fit | Funder priorities documented; recent grantees listed |
| Cultivating | Multi-touch relationship building pre-LOI | PO contact made; warm path established |
| LOI | LOI drafted or submitted | LOI received / submitted on time |
| Proposal Drafting | Invited / open call; drafting | Outline approved by reviewer |
| Submitted | Proposal in funder's hands | Submission receipt obtained |
| Under Review | Funder reviewing | Funder confirmed receipt |
| Awarded | Notice of Award received | Award acceptance signed |
| Declined | Declined by funder | Feedback request sent (→ `declined-grant-iteration`) |
| Active | Award in execution | Project codes set up; spending begun |
| Reporting | Report due | All open reports tracked |
| Closed | Period of performance ended + final report submitted | Auditor sign-off if Single Audit applicable |
```

### Recipe 4: Pipeline health KPIs (monthly review)

```markdown
## Pipeline health metrics

| KPI | Target | Why it matters |
|---|---|---|
| # opportunities in pipeline | 3-5x annual revenue target | Funnel adequacy |
| # at proposal stage | 5-10 simultaneous | Capacity sanity check |
| Weighted pipeline value | ≥ annual revenue target | Forecast confidence |
| Win rate (12 mo trailing) | 25-40% typical for foundations; 10-20% for federal | Benchmark for capacity |
| Avg award size | Tracked by funder type | Strategy signal |
| Funder concentration | < 30% from any single funder | Risk indicator |
| Time-to-decision | Track by funder type | Cash-flow forecasting |
| Renewal rate | 60-80% for foundation; 40-60% for federal | Stewardship signal |
| Pipeline velocity | (Awards / month) / (avg stage time) | Pipeline efficiency |
```

### Recipe 5: Instrumentl pipeline integration

```bash
# Instrumentl REST API (Premium tier)
# Reference: https://help.instrumentl.com/

# List active grants in your pipeline
curl -H "Authorization: Bearer $INSTRUMENTL_API_KEY" \
  https://api.instrumentl.com/v2/grants?status=active

# Pull deadline-driven view
curl -H "Authorization: Bearer $INSTRUMENTL_API_KEY" \
  https://api.instrumentl.com/v2/grants?\
  filter[deadline_within]=30days

# Sync to Notion DB (via notion-mcp): for each Instrumentl record, upsert to Notion
```

### Recipe 6: Salesforce NPC grant tracking (large orgs)

```bash
# SOQL via Salesforce CLI
sf data query -q "SELECT Id, Name, npsp__Grant_Period_Begin_Date__c, \
  npsp__Grant_Period_End_Date__c, Amount, StageName, CloseDate \
  FROM Opportunity \
  WHERE RecordType.Name = 'Grant' \
  AND StageName IN ('Submitted','Under Review','Awarded') \
  ORDER BY CloseDate"

# Common NPSP grant fields (with config):
# - Opportunity record type "Grant"
# - npsp__Grant_Period_Begin/End
# - Grant Probability (rollup to weighted pipeline)
# - Sub-recipient lookup
# - SF-425 due dates
# - Single Audit threshold rollup
```

### Recipe 7: CRM tier match — pick CRM + grant module

```markdown
## CRM tier by org revenue

| Revenue | CRM | Grant strategy |
|---|---|---|
| < $1M | Bloomerang (free / $99-$179/mo) | No native grants → pair with Notion pipeline |
| < $1M | Givebutter (free) | No native grants → pair with Notion |
| $1-10M | DonorPerfect ($99-$329/mo) | Light grants module (awards + deadlines) |
| $1-10M | Little Green Light ($39-$224/mo) | No native grants → pair with Notion |
| $5-15M | Bloomerang Standard ($499/mo) | Add Foundant GrantHub for pipeline |
| $10M+ | Salesforce NPC ($0 license + $20K-100K config) | Full grant compliance possible |
| Enterprise | Bonterra Guided Fundraising | Bundled grants + giving |
| Enterprise | Blackbaud Raiser's Edge NXT ($5K+/yr) | Bundled grants + giving |

## Migration risk
Switching CRM mid-cycle = high risk. Pick well; commit 3+ years.
```

### Recipe 8: Funder DB linked from pipeline

```markdown
## Funders DB (separate from pipeline)

| Column | Notes |
|---|---|
| Funder name | |
| EIN | |
| Type | Federal / State / Foundation / Corp / DAF |
| Avg grant size | From last 10 grants |
| Grant range | Min / max |
| Geographic focus | |
| Program areas | |
| Cycle dates | LOI / proposal / decision per year |
| PO name + contact | |
| PO background | |
| LinkedIn | |
| Recent grantees | Peer signal |
| Our touches log | All cultivation history |
| Latest 990 PF | Link to ProPublica PDF |
| Notes | Strategy / context |

Pipeline opportunities relate to one Funder. Funder relationships persist across cycles.
```

### Recipe 9: Reporting deadlines fed into pipeline

```markdown
## Awarded → Active → Reporting

After award, add reporting line items to pipeline:
| Field | Value |
|---|---|
| Stage | Reporting |
| Sub-stage | SF-425 Q1 / SF-PPR Annual / Final Report |
| Report due date | Per award terms |
| Owner | Grant writer + finance |

Federal: SF-425 quarterly + SF-PPR annual + Final SF-425 + Final SF-PPR
Foundation: per-funder (often annual narrative + financial)

Tied to → `grant-reporting-interim-final` for execution.
```

### Recipe 10: Monthly pipeline review meeting

```markdown
## Standard monthly agenda (60 min)

1. (5 min) KPI dashboard review (Recipe 4)
2. (15 min) Stage transitions since last review
   - New prospects added
   - Promoted to LOI / Drafting
   - Submissions in last month
   - Decisions received
3. (20 min) Next 60-day forecast
   - All deadlines in next 60 days
   - Resource conflicts (writer capacity)
4. (10 min) Funder concentration check
   - Any funder > 30% of revenue?
5. (10 min) Pipeline gaps + diversification asks
   - Where do we need more prospects?

Output: notes back to Notion pipeline + actions assigned.
```

## Examples

### Example 1: Mid-size nonprofit ($5M revenue, 25 active grants) builds Instrumentl-backed pipeline

**Goal:** Replace spreadsheet with Instrumentl + Notion + DonorPerfect stack.

**Steps:**
1. Tier decision (Recipe 1): $5M revenue + 25 grants → Instrumentl + DonorPerfect.
2. Set up Instrumentl (recipient pays $299/mo): import existing grants.
3. Build Notion DB (Recipe 2) as cross-platform pipeline; sync to Instrumentl via API.
4. Set up DonorPerfect for donor side; tag grants as constituent type.
5. Wire pipeline KPIs (Recipe 4) to Notion dashboard.
6. Train team: stage gates (Recipe 3); monthly review cadence (Recipe 10).
7. After 3 months, calculate baseline win rate; set improvement target.

**Result:** Single source of truth; weekly pipeline review under 30 min; win rate visible.

### Example 2: Large org ($25M revenue) configures Salesforce NPC for grant compliance

**Goal:** Move from manual spreadsheet to full Salesforce grant compliance.

**Steps:**
1. Confirm tier: $25M → Salesforce NPC.
2. Hire Salesforce nonprofit implementation partner ($20K-100K).
3. NPSP install (free); configure Opportunity record type "Grant" with custom fields.
4. Set up Account record type "Funder" with separate handling from Donors.
5. Build SF-425 due date rollup; flag when due.
6. Build sub-recipient tracking (junction object).
7. Build Single Audit threshold rollup (cumulative federal expenditures by FY).
8. Pipeline review dashboard built in Salesforce reports.
9. SOQL queries (Recipe 6) drive monthly review.

**Result:** Audit-ready system; pipeline + compliance + reporting in one platform.

## Edge cases / gotchas

- **CRM migration is expensive.** Salesforce NPC config is $20K-100K of services. Pick well; commit 3+ years.
- **Instrumentl AI summarization quality varies.** Use as draft, not as truth.
- **Funder concentration risk.** Any single funder > 30% of org revenue = strategic risk; diversify proactively.
- **Renewal grants in pipeline.** Renewal LOIs should appear in pipeline 6+ months before current grant ends.
- **Notion DB performance.** Above ~5K records, Notion DB queries slow. Migrate to Airtable or Postgres.
- **Federal pass-through complexity.** Federal funds passed through a state still subject to 2 CFR 200; track in pipeline as "Federal (state pass-through)".
- **DAF grants.** DAF grants (Fidelity, Schwab) come from individuals via DAF; track as individual donor → DAF advisor. Different stewardship than foundation.
- **Multi-year grants.** Tracked as single opportunity with multiple report due dates and a renewal touch 6 mo before end.
- **Workspace owner vs grant owner.** Grants.gov Workspace owner can differ from your internal grant owner. Document both.
- **Donor vs grant in one CRM.** Bloomerang doesn't separate; Salesforce NPC can if configured. Choose deliberately.
- **Pipeline noise.** Adding every cold prospect = clutter. Use stage gate "Research" with explicit qualification criteria.

## Sources

- Instrumentl pipeline: https://www.instrumentl.com/
- Submittable for applicants: https://submit.com/
- Fluxx Grantseeker: https://www.fluxx.io/products/grantseeker
- Foundant GrantHub: https://www.foundant.com/grant-management/
- Bloomerang: https://bloomerang.com/
- DonorPerfect: https://www.donorperfect.com/
- Salesforce Nonprofit Cloud: https://www.salesforce.org/products/nonprofit-cloud/
- Instrumentl grant management software comparison: https://www.instrumentl.com/blog/best-grant-management-software
- Submittable grant mgmt software roundup: https://submit.com/resources/blog/best-grant-management-software-for-nonprofits-2026/
- Plinth grant mgmt systems comparison: https://www.plinth.org.uk/en-US/complete-guide/grant-management-systems-compared
- Cube84 Bloomerang vs Salesforce NPC: https://cube84.com/blog/bloomerang-vs-salesforce-nonprofit-cloud-vs-npsp-which-crm-is-best-for-your-nonprofit
- Nonprofit Point best CRM 2026: https://nonprofitpoint.com/best-crm-for-nonprofits/
