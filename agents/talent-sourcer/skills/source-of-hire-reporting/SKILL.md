<!--
Sources: https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable
         https://www.outsail.co/post/greenhouse-vs-lever-vs-ashby
         https://www.metaview.ai/resources/blog/recruiting-trends
Source-of-hire = % of hires by channel. Pull via ATS REST candidate.source field.
Aggregate weekly + monthly dashboards in xlsx / Google Sheet. No single source >60% rule.
-->
# Source-of-Hire Reporting — SKILL

Aggregate hires by channel (LinkedIn / GitHub / Wellfound / Gem / Referral / Boomerang / Diversity Channel / etc.) for weekly + monthly + quarterly dashboards. Surfaces channel ROI + the "no single source >60%" diversification rule. Drives sourcing budget allocation.

## When to use

- User wants **monthly source-of-hire dashboard** to leadership.
- User wants **channel-by-channel cost-per-hire** comparison.
- User wants **quarterly source-mix audit** for diversification compliance.
- User asks "which channels are working?" or "where are our hires coming from?".
- Trigger phrases: "source of hire", "channel ROI", "cost per hire", "hiring dashboard", "source mix", "channel attribution".

Do not use for: per-req funnel diagnosis (`source-to-contact-metrics`); single-source attribution at moment of contact (handled by `gem-hireez-beamery-talent-crm` push-to-ATS recipe).

## Setup

```bash
# ATS keys
export GREENHOUSE_API_KEY="harvest_xxx"
export ASHBY_API_KEY="xxx"
export LEVER_API_KEY="xxx"

# Output target
export GOOGLE_SHEET_ID="xxx"
export NOTION_API_KEY="secret_xxx"

# Optional: PostHog for outreach A/B analytics
export POSTHOG_KEY="xxx"
```

## Common recipes

### Recipe 1: Source taxonomy (THE canonical list)

```
LinkedIn Recruiter        # Boolean + InMail outreach
LinkedIn Sales Nav        # 2nd-degree warm intro
GitHub mining             # contributor + commit-based sourcing
Stack Overflow            # reputation + tag sourcing
Wellfound                 # niche board candidate apply
Built In                  # metro board candidate apply
Otta                      # curated board candidate apply
Hired                     # two-sided match candidate apply
Gem outbound              # CRM sequence reply → applied
hireEZ outbound           # ditto
Beamery outbound          # ditto
Employee referral         # internal team referral
Boomerang                 # alumni return
Diversity Channel-{slug}  # /dev/color, Code2040, etc. (per channel)
Conference/event-{slug}   # AfroTech, Grace Hopper, KubeCon, etc.
Career site apply         # inbound to careers.acme.com
Indeed                    # generic job board
Other                     # everything else
```

Maintain this list as `sources` table in ATS configuration. Greenhouse: Configure → Sources. Ashby: Source.list. Lever: Settings → Sources.

### Recipe 2: Greenhouse — pull hires by source for a date range

```bash
# All hires in date range with source attribution
curl -u "$GREENHOUSE_API_KEY:" \
  "https://harvest.greenhouse.io/v1/candidates?status=hired&hired_after=2026-04-01&hired_before=2026-06-30&per_page=500" \
  | jq '[.[] | {id, name: (.first_name + " " + .last_name), source: .applications[0].source.public_name, hired_at: .applications[0].closed_at, job_id: .applications[0].jobs[0].id}]'

# Aggregate by source
curl -u "$GREENHOUSE_API_KEY:" \
  "https://harvest.greenhouse.io/v1/candidates?status=hired&hired_after=2026-04-01" \
  | jq 'group_by(.applications[0].source.public_name) | map({source: .[0].applications[0].source.public_name, count: length})'
```

### Recipe 3: Ashby — hires by source

```bash
curl -X POST "https://api.ashbyhq.com/candidate.list" \
  -u "$ASHBY_API_KEY:" \
  -H "Content-Type: application/json" \
  -d '{
    "limit": 500,
    "statuses": ["Hired"],
    "createdSince": "2026-04-01T00:00:00Z"
  }' \
  | jq '.results | group_by(.sourceTitle) | map({source: .[0].sourceTitle, count: length})'
```

### Recipe 4: Lever — hired opportunities by source

```bash
curl -u "$LEVER_API_KEY:" \
  "https://api.lever.co/v1/opportunities?stage_id=hired&created_at_start=2026-04-01&limit=500" \
  | jq '.data | group_by(.sources[0]) | map({source: .[0].sources[0], count: length})'
```

### Recipe 5: Per-source dashboard schema (the canonical table)

```python
# Google Sheet or xlsx schema
schema = {
    "week_of": "date",
    "source": "enum",  # from Recipe 1 taxonomy
    "req_id": "string",
    "sourced": "int",      # CRM (Gem) — see source-to-contact-metrics
    "contacted": "int",    # CRM
    "replied": "int",      # CRM
    "screened": "int",     # ATS — past initial screen stage
    "offered": "int",      # ATS — offer object created
    "hired": "int",        # ATS — hire date set
    "source_to_contact_pct": "derived",
    "contact_to_reply_pct": "derived",
    "reply_to_screen_pct": "derived",
    "screen_to_offer_pct": "derived",
    "offer_acceptance_pct": "derived",
    "cost_per_hire": "derived"  # via cost allocation per Recipe 9
}
```

### Recipe 6: Weekly per-source aggregation script

```python
from datetime import date, timedelta
import gspread

def run_weekly_source_aggregation():
    week_start = date.today() - timedelta(days=date.today().weekday())
    week_end = week_start + timedelta(days=6)

    # Per source × per req
    open_reqs = greenhouse.list_open_jobs()
    rows = []

    for req in open_reqs:
        per_source = greenhouse.get_per_source_funnel(req["id"], week_start, week_end)
        for source, funnel in per_source.items():
            rows.append([
                week_start.isoformat(),
                source,
                req["id"],
                funnel["sourced"], funnel["contacted"], funnel["replied"],
                funnel["screened"], funnel["offered"], funnel["hired"],
                funnel["source_to_contact_pct"], funnel["contact_to_reply_pct"],
                funnel["reply_to_screen_pct"], funnel["screen_to_offer_pct"],
                funnel["offer_acceptance_pct"],
                funnel.get("cost_per_hire", "")
            ])

    sheet = gspread.open_by_key(os.environ["GOOGLE_SHEET_ID"]).worksheet("Weekly Source Funnel")
    sheet.append_rows(rows)

# Cron: Mondays 9am
```

### Recipe 7: Monthly source-of-hire summary

```markdown
# Source-of-Hire Summary — {month}

| Source | Hires | % of total | Avg time-to-hire | Avg cost-per-hire | Quality score (3-mo) |
|--------|-------|------------|------------------|-------------------|---------------------|
| LinkedIn Recruiter | 8 | 32% | 28 days | $1,200 | 4.2 |
| GitHub mining | 4 | 16% | 22 days | $400 | 4.5 |
| Employee referral | 7 | 28% | 18 days | $0 (internal) | 4.7 |
| Wellfound | 2 | 8% | 32 days | $499/mo / 2 = $250 | 3.8 |
| Gem outbound | 2 | 8% | 26 days | $200/seat/mo allocated | 4.0 |
| Boomerang | 1 | 4% | 14 days | $0 | 5.0 |
| Diversity Channel-devcolor | 1 | 4% | 24 days | $5K sponsorship | 4.4 |
| **Total** | **25** | **100%** | **24 days avg** | | |

**Flags:**
- LinkedIn at 32% — healthy, under 60% rule.
- Employee referral at 28% — strong; consider referral bonus increase.
- Wellfound at 8% — low; verify ROI vs $499/mo spend.
- Diversity channels at 4% — could be higher; check Q3 sponsor cycle.
- Quality scores (post-90-day performance review) — all >3.8, healthy.
```

### Recipe 8: Quality score — 90-day post-hire (the ROI completion signal)

```bash
# Pull 90-day performance ratings for each hire (via parent operations-agent's lattice/15five skill)
# Quality score = manager rating 1-5 at 90 days
# Per source, compute avg quality score over last 12 months

# This is the lagging KPI — sources that produce high reply rate but low 90-day quality (e.g., wide-aggregator
# spam-style sourcing) get deprioritized in budget allocation.
```

### Recipe 9: Cost-per-hire calculation

```python
def cost_per_hire(source, period_start, period_end):
    """Per-source cost allocation."""
    hires = ats.count_hires(source=source, since=period_start, until=period_end)

    if source == "LinkedIn Recruiter":
        cost = LINKEDIN_RECRUITER_MONTHLY * months_in_period  # $899/mo Lite or seat allocation
    elif source == "Wellfound":
        cost = 499 * months_in_period  # Recruit Pro
    elif source == "Gem outbound":
        cost = (GEM_SEAT_MONTHLY * months_in_period) * (HIRES_THIS_SOURCE / TOTAL_GEM_HIRES_THIS_PERIOD)
    elif source == "Employee referral":
        cost = REFERRAL_BONUS * hires
    elif source.startswith("Diversity Channel"):
        cost = SPONSORSHIP_SPEND[source]  # /dev/color, Code2040, etc.
    elif source == "Boomerang":
        cost = 0  # alumni newsletter cost trivial
    else:
        cost = 0

    return cost / hires if hires else None
```

### Recipe 10: 12-month source-of-hire trend

```python
def trend_source_of_hire_12mo():
    """For each source, compute monthly hire count over last 12 months."""
    monthly = {}
    for month_start in last_12_months():
        for source in SOURCES:
            count = ats.count_hires(source=source, since=month_start, until=month_start + timedelta(days=30))
            monthly.setdefault(source, []).append({"month": month_start, "count": count})
    return monthly

# Plot as stacked area chart in Google Sheet
```

Trend reveals sourcing-mix shifts over time — e.g., LinkedIn declining as Boomerang rises.

### Recipe 11: Diversification check (the 60% rule enforcement)

```python
def diversification_check(monthly_hires):
    """Flag if any single source >60% of hires in the period."""
    total = sum(monthly_hires.values())
    for source, count in monthly_hires.items():
        share = count / total
        if share > 0.60:
            return {
                "violation": True,
                "source": source,
                "share": share,
                "action": f"REBALANCE — {source} at {share:.0%}; activate underused sources"
            }
    return {"violation": False}
```

Single-source >60% = pipeline-resilience risk (Antipattern 5 in role.md). Triggers rebalance.

### Recipe 12: Per-source quality + retention combined

```python
# 12-month retention rate by source (post-hire 12 months still employed)
# A source can hire fast + cheap but if 6/12 mo retention is 50%, ROI is negative
def retention_by_source():
    for source in SOURCES:
        hires_12mo_ago = ats.list_hires(source=source, hired_between=(today - 540, today - 360))
        still_employed = sum(1 for h in hires_12mo_ago if not h["terminated"])
        retention = still_employed / len(hires_12mo_ago) if hires_12mo_ago else None
        yield {"source": source, "12mo_retention": retention}
```

Add to monthly dashboard. Sources with retention <70% need investigation (mis-leveling, comp mismatch, culture-fit).

## Examples

### Example 1: Monthly source-of-hire dashboard generation
**Goal:** Q3 month-end source dashboard for ops leadership.
**Steps:**
1. Recipe 2 / 3 / 4 — pull hires by source for the month from primary ATS.
2. Recipe 7 — generate markdown summary table.
3. Recipe 9 — calculate cost-per-hire per source.
4. Recipe 8 — pull 90-day quality scores from `lattice` / `15five` (via parent operations-agent skill).
5. Recipe 11 — diversification check (60% rule).
6. Publish to Notion + Google Sheet; Slack post to `#hiring` channel.

**Result:** Leadership dashboard published; budget rebalance decisions data-driven.

### Example 2: Diagnose LinkedIn over-dependence
**Goal:** Last quarter, LinkedIn = 65% of hires. Trigger diversification.
**Steps:**
1. Recipe 11 — flagged LinkedIn at 65%, action required.
2. Recipe 10 — 12-month trend confirms LinkedIn climbing.
3. Per Antipattern 5 in role.md: activate ≥3 alternative sources.
4. Plan:
   - GitHub mining: invest 1 sourcer-day/week.
   - Employee referrals: bonus increase from $2K to $3K.
   - Diversity channels: activate Q4 AfroTech sponsorship.
   - Boomerang: re-engage 50 alumni this quarter.
5. Re-measure 90 days; expect LinkedIn share to drop to 40-50%.

**Result:** Pipeline resilient to LinkedIn-tier-change risk; source mix diversified.

### Example 3: Cost-per-hire ROI audit for Wellfound
**Goal:** $499/mo Wellfound Recruit Pro yielding 2 hires/quarter; is it worth it?
**Steps:**
1. Recipe 9 — cost-per-hire = $1,497 ($499 × 3 mo / 2 hires) = $748 per hire.
2. Compare LinkedIn Recruiter cost-per-hire: $899/mo × 3 / 8 hires = $337 per hire.
3. Wellfound is 2.2× LinkedIn cost per hire. Investigate quality:
   - Recipe 8 — 90-day quality from Wellfound: 3.8 vs LinkedIn 4.2.
4. Decision: downgrade Wellfound to free (startups only); reallocate $499/mo to GitHub mining sourcer time.

**Result:** Lower cost-per-hire + higher quality through reallocation; Wellfound retained for free for niche apply flow.

## Edge cases / gotchas

- **Source attribution must be set at moment of ATS push.** If candidate is pushed with `source = "Other"`, dashboard counts wrong. See `gem-hireez-beamery-talent-crm` Recipe 10. Antipattern 6 in role.md.
- **Source taxonomy must match between CRM (Gem) and ATS.** Use IDENTICAL strings. Standardize via Recipe 1.
- **Inbound career-site applies often get `source = "Career site"` but actually came from LinkedIn/Wellfound posting.** UTM parameters on apply URLs resolve this: `?utm_source=wellfound`.
- **Referral attribution** — Greenhouse and Ashby expose `referrer.user_id` on application; reconcile against employee directory for credit.
- **Boomerang attribution** — alumni who self-apply often get `source = "Career site"` instead of "Boomerang". Auto-flag returning alumni via ATS tag at moment of apply (see `boomerang-alumni-re-engagement`).
- **Sample size <5 hires/source/month = noise.** Don't draw conclusions; smooth over 3-month trailing window.
- **Diversity-channel attribution is sometimes implicit.** Candidate sourced via warm intro from Code2040 contact may end up `source = "LinkedIn"`. Cross-reference via tag `diversity-channel-code2040` set at CRM enrollment.
- **Cost-per-hire allocation is approximate.** Sourcer salary + recruiter salary + ATS fees + tool licenses all contribute. Decide on a consistent allocation model and stick with it.
- **Quality score requires post-hire data flow.** Lattice / 15Five / Culture Amp integration needed. Defer to parent operations-agent's `performance-review-cycle-lattice-15five` skill.
- **Retention by source needs 12+ months of historical data.** Don't expect signal until at least 6-12 months post-launch.
- **Quarterly trends matter more than weekly.** Hiring cadence noise dominates week-to-week; quarter-over-quarter trend is the signal.
- **Diversification flagging at 60% is heuristic** — startups with one obvious source channel may legitimately exceed 60%. Adjust threshold per team maturity.
- **Some hires are multi-source.** A candidate sourced via GitHub, contacted via LinkedIn, accepted from a referral. Decide attribution policy (first-touch / last-touch / weighted) and stick with it.
- **Defer to `source-to-contact-metrics`** for per-req funnel diagnosis.
- **Defer to `source-diversification-3-sources-per-role`** for per-req source-mix enforcement.
- **Defer to `operations-agent`** for performance/retention data pipeline.

## Sources

- Unified.to — 15 ATS APIs 2026: https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable
- Outsail — Greenhouse vs Lever vs Ashby: https://www.outsail.co/post/greenhouse-vs-lever-vs-ashby
- Metaview — Recruiting Trends 2026: https://www.metaview.ai/resources/blog/recruiting-trends
- Lupahire — 20 Best Candidate Sourcing Tools 2026 (diversification benchmarks): https://www.lupahire.com/blog/candidate-sourcing-tools-for-recruiters
- Greenhouse Harvest API — `/candidates`: https://developers.greenhouse.io/harvest.html#candidates
- Ashby API — `candidate.list`: https://developers.ashbyhq.com/
- Lever API — `/opportunities`: https://hire.lever.co/developer/documentation
