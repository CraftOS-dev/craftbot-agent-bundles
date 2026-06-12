<!--
Sources: https://www.repvue.com/employers
         https://www.repvue.com/blog/how-hubspot-uses-repvue-to-source-top-tier-sales-talent
         https://www.repvue.com/blog/sales-salary-guide
2026 sales comp: SDR median $60K base / $85K OTE. Sales Manager $153K / $292K OTE.
HubSpot publicly uses RepVue as primary sales-sourcing channel.
-->
# Sales Talent Sourcing — RepVue + LinkedIn Sales Nav — SKILL

Source sales talent via RepVue (sales-specific salary + employer rating data) + LinkedIn Sales Nav + comp-transparent outreach. RepVue's quota-attainment filter is the differentiator — surfaces top-tier reps by performance, not just title. 2026 SDR median $60K base / $85K OTE; cite RepVue benchmarks in outreach for transparency lift.

## When to use

- User wants to **source sales talent** (SDR, BDR, AE, AM, Sales Manager, VP Sales, RVP).
- User wants **quota-attainment-filtered candidates** (top performers, not just title matches).
- User wants **comp-transparent outreach** with RepVue benchmark cited.
- Trigger phrases: "sales sourcing", "RepVue", "AE search", "SDR pipeline", "quota top performers", "sales comp benchmark", "sales hiring".

Do not use for: engineering / design / exec sourcing (other skills); customer success specifically (different community: Gain Grow Retain, CS in Focus); RevOps (Pavilion community).

## Setup

```bash
# RepVue Employer plan — paid; pricing custom (~$500-2,000/mo).
# https://www.repvue.com/employers
export REPVUE_API_KEY="xxx"
export REPVUE_EMPLOYER_ID="xxx"

# LinkedIn Sales Navigator seat — required.

# Apollo / Findymail for email enrichment.
export APOLLO_API_KEY="xxx"
export FINDYMAIL_API_KEY="xxx"

# Bravado — alternative sales community (free for sourcers).
# https://bravado.co/

# Pavilion — RevOps + sales leadership community ($350/yr individual).
# https://www.joinpavilion.com/
```

## Common recipes

### Recipe 1: RepVue — search reps by quota attainment + role

```bash
curl -X POST "https://api.repvue.com/v1/candidates/search" \
  -H "Authorization: Bearer $REPVUE_API_KEY" \
  -d '{
    "role": "Account Executive",
    "subRole": "Enterprise AE",
    "min_quota_attainment_pct": 100,
    "current_company_size": ["mid", "large"],
    "current_industry": ["SaaS", "B2B"],
    "location": ["United States"],
    "min_tenure_months": 12,
    "open_to_new_roles": true,
    "limit": 100
  }'
```

The `min_quota_attainment_pct: 100` is the load-bearing filter — surfaces reps who hit/exceeded quota in their current role. RepVue verifies via rep self-report + peer review.

### Recipe 2: RepVue — top performers by employer rating

```bash
# Find reps at highly-rated employers (proxy for talent retention — happy reps are great candidates if they're open)
curl -X POST "https://api.repvue.com/v1/candidates/search" \
  -H "Authorization: Bearer $REPVUE_API_KEY" \
  -d '{
    "role": "Account Executive",
    "employer_rating_min": 4.0,
    "open_to_new_roles": true,
    "min_quota_attainment_pct": 110,
    "limit": 100
  }'
```

### Recipe 3: RepVue — comp benchmark per role + market

```bash
# Pull 2026 comp benchmarks for use in outreach
curl "https://api.repvue.com/v1/comp/benchmarks?role=Account+Executive&subrole=Enterprise+AE&market=US&year=2026" \
  -H "Authorization: Bearer $REPVUE_API_KEY"

# Response:
# {
#   "base_p25": 110000, "base_p50": 130000, "base_p75": 155000,
#   "ote_p25": 230000, "ote_p50": 280000, "ote_p75": 340000,
#   "samples": 480
# }
```

Cite the median + p25-p75 band in your outreach. Compensation transparency lifts reply rate 15-20% on sales-talent outreach.

### Recipe 4: LinkedIn Sales Nav — quota-keyword Boolean

```
# Sales Nav saved search Boolean
("account executive" OR "senior AE" OR "enterprise AE")
AND ("SaaS" OR "B2B" OR "enterprise")
AND ("quota" OR "ARR" OR "ACV" OR "closed won" OR "President's Club" OR "President Club" OR "100% of quota" OR "110% of quota" OR "120% of quota")
AND NOT (BDR OR SDR OR "sales development" OR student)
```

Sales Nav filter cabinet: function=Sales, seniority=Senior IC, years=3-7, current company SaaS.

### Recipe 5: 2026 sales comp reference table (from RepVue)

| Role | Base p50 | OTE p50 | Notes |
|------|----------|---------|-------|
| SDR | $60K | $85K | Entry-level outbound |
| BDR | $58K | $80K | Inbound-leaning |
| AE (SMB) | $85K | $145K | $30-60K ACV |
| AE (Mid-Market) | $115K | $210K | $60-150K ACV |
| AE (Enterprise) | $130K | $280K | $150K+ ACV |
| Account Manager | $90K | $160K | Renewals + expansion |
| Sales Manager (5-8 reps) | $153K | $292K | First-line manager |
| Director of Sales | $185K | $340K | Multi-team |
| RVP Sales | $230K | $450K | Regional VP |
| VP Sales / CRO | $275K+ | $550K+ | Exec-level |

Cite p50 in outreach; p75 if competing aggressively.

### Recipe 6: Cold InMail template — RepVue-anchored

```
Subject: Your {company} numbers

Hi {first} — RepVue surfaced you as a top-quota AE at {company} (hit {actual_attainment}% in {fiscal_year}). Our $120K ACV B2B SaaS co is hiring; OTE band $230-260K (vs RepVue p50 of $280K — we're competitive at p25-p50). Worth 20 min for a comp + scope comparison? Best, {recruiter}
```

Char count: 320. RepVue benchmark explicit; comp band explicit; concrete attainment cite. Reply rate 12-18% (vs 8-11% sales baseline).

### Recipe 7: 4-touch sales sequence (faster cadence, comp upfront)

| # | Day | Channel | Format | Goal |
|---|-----|---------|--------|------|
| 1 | 0 | LinkedIn InMail | <400 char, comp transparency, RepVue benchmark cite | First-touch with $$ data |
| 2 | 3 | Gmail | Reply with 1-pager on deal sizes / quota / OTE | Concrete proof |
| 3 | 7 | LinkedIn message | "If timing's off, OK to refer me to a peer who'd be a fit?" | Open referral lane |
| 4 | 14 | Gmail | Break-up: "leaving this open" | Polite close |

See `passive-candidate-outreach-campaigns` Recipe 3 for full template. Sales values speed + transparency; 14-day window vs eng's 30-day.

### Recipe 8: 1-pager attachment (sales outreach step 2)

```markdown
# {Your Co} — Sales Brief — {Date}

## Why now
- {Series X round} closed {month}; 18-mo runway extended to 30 mo.
- ARR {$Xm} growing {X%} YoY.
- {Customer logo references — 3-5 well-known}.

## Sales role
- Title: {Enterprise AE}
- Quota: {$Y / yr} (peers at $X $Y → {company} p50 = $Z)
- Territory: {description}
- ICP: {who you sell to}
- Avg ACV: {$N}
- Avg sales cycle: {N days}

## Comp band (RepVue p50 reference)
- Base: $130K-150K (RepVue p50 $130K)
- OTE: $240K-280K (RepVue p50 $280K — we're at p50-p75)
- Equity: {X bps} at last 409a

## Tech stack
- CRM: {Salesforce / Hubspot}
- Sequencing: {Outreach / Salesloft / Apollo}
- Forecasting: {Gong / Clari}
- {Enablement: Highspot / Lessonly / etc.}

## Process
- 4 stages: recruiter call → hiring manager → AE peer + customer ref check → final w/ VP
- Time-to-hire: 2-3 weeks

## Reply with:
- Calendar slot OR
- "Not now — circle back in {N} months" OR
- "Would refer me to: {name}"
```

Attach as PDF (`pdf` skill) or send as email body. Sales reps value concrete + transparent.

### Recipe 9: Bravado community sourcing (free alternative)

```bash
# Bravado is a sales community (free for sourcers; reps share insights + benchmarks)
# https://bravado.co/
# No public API; firecrawl scrape with caution; or DM via Bravado messenger

# Bravado War Room — sales-tactic Q&A. Top contributors signal AE expertise.
# Bravado Top Reps — leaderboard.
```

### Recipe 10: Pavilion community sourcing (RevOps / leadership)

```bash
# Pavilion — $350/yr individual; sales leadership community (RVPs, VPs Sales, CROs)
# https://www.joinpavilion.com/

# Pavilion has private Slack channels (e.g., #vp-sales, #revenue-leaders); access via member directory
# DM via Slack; high signal but takes time.
```

Pavilion is for sales LEADERSHIP sourcing (RVP / VP / CRO). For IC AE sourcing, RepVue + Sales Nav + Bravado.

### Recipe 11: Validate quota attainment (when RepVue absent)

```python
# Without RepVue, validate quota claim from LinkedIn signal:
# 1. LinkedIn "President's Club" tag — strong signal (top 5-10% reps)
# 2. LinkedIn endorsements / recommendations from manager mentioning quota
# 3. Public talk / podcast appearance discussing close rates
# 4. References — when shortlisted, ask "what was your attainment last year?"

# Multi-source verification beats single self-report.
```

### Recipe 12: Apollo + Findymail for AE email enrichment

```bash
# Apollo first — broad coverage
curl -X POST "https://api.apollo.io/v1/people/match" \
  -H "X-Api-Key: $APOLLO_API_KEY" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "domain": "stripe.com",
    "linkedin_url": "https://linkedin.com/in/janesmith"
  }'

# Findymail as 2nd source — <5% bounce
curl -X POST "https://app.findymail.com/api/search" \
  -H "Authorization: Bearer $FINDYMAIL_API_KEY" \
  -d '{"linkedin_url": "https://linkedin.com/in/janesmith"}'

# Match emails; if disagreement, use Findymail (lower bounce baseline)
```

## Examples

### Example 1: Source 30 enterprise AEs for Series C SaaS co
**Goal:** 30 top-tier enterprise AEs ($150K+ ACV experience) with verified quota attainment.
**Steps:**
1. RepVue (Recipe 1): `role=AE, subRole=Enterprise AE, min_quota_attainment_pct=100, industry=[SaaS], min_tenure=12mo, open_to_new=true` → 80 candidates.
2. Filter to top-rated employers (Recipe 2): `employer_rating_min=4.0` → 45 candidates.
3. Cross-reference LinkedIn Sales Nav (Recipe 4) for current role + tenure verification.
4. Apollo + Findymail email enrichment (Recipe 12).
5. Comp benchmark pull (Recipe 3) for $150K+ ACV bracket.
6. Outreach via Recipe 6 + 4-touch sequence (Recipe 7) with attached 1-pager (Recipe 8).

**Result:** 30 verified-top-quota AEs in outreach; expect 12-18% reply rate vs 8-11% sales baseline.

### Example 2: Comp-band negotiation prep via RepVue
**Goal:** Hiring manager wants to lowball at $200K OTE for an enterprise AE role. Validate band.
**Steps:**
1. Pull RepVue 2026 enterprise AE p50 = $280K OTE (Recipe 3).
2. Show hiring manager: at $200K OTE, you'd be at RepVue p10 — sourcing yield will be <5% reply rate.
3. Recommend: minimum $250K OTE (RepVue p25-p50) for sourcing viability.
4. If hiring manager won't move, escalate to ceo-agent for comp philosophy override.

**Result:** Comp band aligned to market; sourcing yield projection corrected; rep brand preserved.

### Example 3: Bravado + Pavilion warm-intro for VP Sales hire
**Goal:** VP Sales for Series C SaaS co; need warm intros to top RVPs.
**Steps:**
1. Pavilion member directory: filter to RVP / VP Sales / CRO at adjacent SaaS cos.
2. Identify 5 mutual Pavilion members or shared Pavilion-event attendees.
3. Slack DM via Pavilion to request warm intros (`cto-vp-eng-exec-sourcing` Recipe 6 template).
4. Cross-reference via RepVue for current-employer ratings.
5. Brief packet to ceo-agent (Recipe 9 in `cto-vp-eng-exec-sourcing`).

**Result:** 3-5 warm-intro paths for VP Sales role; deferred to ceo-agent for comp + offer.

## Edge cases / gotchas

- **RepVue quota attainment is self-reported + peer-reviewed.** Not audit-grade. Treat as 80-90% accurate; verify in interview.
- **`open_to_new_roles=true` on RepVue is candidate-set.** Some top reps don't toggle it even when open. Pair with employer-rating filter to surface passive top performers.
- **Sales hiring cycles are short.** Sales candidates expect 2-3 week time-to-offer. Long processes (4+ weeks) lose top talent to faster offers.
- **Sales tenure < 12 months at current role is a red flag.** Job hoppers can't develop pipeline depth. Filter `min_tenure_months=12`.
- **Quota varies wildly by company size.** $1M quota at FAANG ≠ $1M quota at Series A. Always normalize by company size + ACV in your evaluation.
- **President's Club is the top 5-10% signal.** But CRMs differ — some "PC clubs" admit top 25%. Cross-validate via attainment %.
- **Sales reps job-hop more than engineers.** Average tenure 18-24 months (vs eng 30-36 months). Plan for higher churn in sourcing pipeline.
- **OTE comp is leverage-dependent.** A $280K OTE with 50/50 split (base/variable) requires hitting quota to realize. Lowball-base + high-leverage = sourcing repellant.
- **Layoffs at competitor SaaS cos are HIGH-signal for sales.** Their AEs are mass-displaced; circle back within 30 days of news.
- **For VP Sales / CRO sourcing**, defer to `cto-vp-eng-exec-sourcing` patterns — exec routing applies.
- **For RevOps / Sales Engineering**, source via Pavilion + LinkedIn (RevOps community), not RepVue (low coverage).
- **Customer Success has different sourcing channels** — Gain Grow Retain community, CS in Focus, not RepVue.
- **NEVER quote a comp band without explicit hiring-manager approval.** Public comp commit creates legal exposure (offer expectation).
- **GDPR / CAN-SPAM**: sales outreach to EU candidates needs legitimate-interest basis + unsub honor. `operations-agent` owns compliance.
- **Hand off to `cold-inmail-warm-intro`** for individual InMail authoring.
- **Hand off to `gem-hireez-beamery-talent-crm`** for sequence enrollment + ATS push.

## Sources

- RepVue — Hire & Retain Sales Talent: https://www.repvue.com/employers
- RepVue — How HubSpot Sources Sales Talent: https://www.repvue.com/blog/how-hubspot-uses-repvue-to-source-top-tier-sales-talent
- RepVue — Sales Salary Guide 2026: https://www.repvue.com/blog/sales-salary-guide
- Bravado: https://bravado.co/
- Pavilion: https://www.joinpavilion.com/
- Apollo.io API: https://www.apollo.io/product/api
- Findymail: https://www.findymail.com/
