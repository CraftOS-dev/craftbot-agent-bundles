<!--
Sources: https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable
         https://www.outsail.co/post/greenhouse-vs-lever-vs-ashby
         https://www.metaview.ai/resources/blog/recruiting-trends
2026 benchmarks:
- source-to-contact >25% (acceptable), >40% (strong)
- contact-to-reply: eng 7-9%, sales 8-11%, PM 10-12%, HR 12%
- reply-to-screen 50-70%, screen-to-offer 30-50%, offer-acceptance >85%
-->
# Source-to-Contact + Funnel Metrics — SKILL

Calculate and report per-req funnel metrics: source-to-contact %, contact-to-reply %, reply-to-screen %, screen-to-offer %, offer-acceptance %. Pull from ATS REST APIs (Greenhouse/Ashby/Lever); aggregate weekly into Google Sheet or xlsx. Surface bottleneck stage; recommend interventions.

## When to use

- User asks for **per-req funnel report** for the week / month.
- User wants to **diagnose a low reply rate** on a specific sequence.
- User wants to **compare source channels** by funnel health.
- User asks "is my source-to-contact good?" or "why is my reply rate low?".
- Trigger phrases: "funnel metrics", "source-to-contact", "reply rate by source", "per-req funnel", "bottleneck stage", "funnel diagnosis".

Do not use for: aggregate source-of-hire reporting across all reqs (`source-of-hire-reporting`); diversity metrics specifically (overlapping with `source-of-hire-reporting`); candidate experience hygiene (`candidate-experience-hygiene-response-time`).

## Setup

```bash
# ATS keys
export GREENHOUSE_API_KEY="harvest_xxx"
export ASHBY_API_KEY="xxx"
export LEVER_API_KEY="xxx"

# CRM keys (for sourced-and-contacted counts pre-ATS)
export GEM_API_KEY="xxx"

# Output target
export GOOGLE_SHEET_ID="xxx"  # via google-workspace-mcp
```

## Common recipes

### Recipe 1: Funnel stage definitions (be precise)

| Stage | Definition | Source |
|-------|------------|--------|
| Sourced | Candidate identified and added to CRM with valid contact info | Gem / hireEZ / Beamery / Notion |
| Contacted | Outreach sent (InMail / email / Sales Nav msg) | Gem sequence step 1 sent |
| Replied | Candidate responded positively or neutrally | Gem reply detection |
| Screened | Recruiter screen completed (30-min call) | ATS application moved past initial screen stage |
| Offered | Offer extended | ATS offer object created |
| Hired | Offer accepted + start date confirmed | ATS hire date set |

### Recipe 2: 2026 benchmark table

| Metric | Healthy (eng) | Healthy (sales) | Healthy (PM) | Healthy (HR/ops) | Investigate at |
|--------|---------------|------------------|--------------|------------------|----------------|
| Source-to-contact | >40% | >40% | >40% | >40% | <25% — Boolean targeting wrong; tighten filters |
| Contact-to-reply | 7-9% | 8-11% | 10-12% | 10-15% | <5% (eng) / <6% (sales) — template / segmentation / subject |
| Reply-to-screen | 50-70% | 50-70% | 50-70% | 50-70% | <30% — wrong-fit replies; tighten ICP |
| Screen-to-offer | 30-50% | 30-50% | 30-50% | 30-50% | <20% — interview process leaks |
| Offer-acceptance | >85% | >80% | >85% | >85% | <70% — comp band / process speed |

### Recipe 3: Greenhouse — per-req funnel pull

```bash
# Pull all applications for a job
curl -u "$GREENHOUSE_API_KEY:" \
  "https://harvest.greenhouse.io/v1/applications?job_id={job_id}&per_page=500" \
  | jq '[.[] | {id, candidate_id, status, current_stage: .current_stage.name, applied_at, source: .source.public_name}]'

# Stage breakdown
curl -u "$GREENHOUSE_API_KEY:" \
  "https://harvest.greenhouse.io/v1/applications?job_id={job_id}" \
  | jq 'group_by(.current_stage.name) | map({stage: .[0].current_stage.name, count: length})'
```

### Recipe 4: Ashby — per-req funnel pull (deepest analytics)

```bash
curl -X POST "https://api.ashbyhq.com/application.list" \
  -u "$ASHBY_API_KEY:" \
  -H "Content-Type: application/json" \
  -d '{"jobId": "{job_id}", "limit": 500}' \
  | jq '.results[] | {id, candidate, status, currentStage: .currentInterviewStage.title, source: .sourceTitle, daysInStage: .currentStageDuration}'

# Time-in-stage breakdown (Ashby's strength)
curl -X POST "https://api.ashbyhq.com/application.list" \
  -u "$ASHBY_API_KEY:" \
  -d '{"jobId": "{job_id}"}' \
  | jq 'group_by(.currentInterviewStage.title) | map({stage: .[0].currentInterviewStage.title, count: length, avgDays: ([.[].currentStageDuration] | add / length)})'
```

Ashby is best for per-req funnel analytics due to `currentStageDuration` field.

### Recipe 5: Lever — opportunities + stage breakdown

```bash
curl -u "$LEVER_API_KEY:" \
  "https://api.lever.co/v1/opportunities?posting_id={job_id}&limit=100" \
  | jq '.data[] | {id, name, stage: .stage.text, sources, createdAt}'
```

### Recipe 6: Gem — pre-ATS counts (sourced + contacted + replied)

```bash
# Sourced count
curl "https://api.gem.com/v1/prospects?req_id={req_id}&limit=500" \
  -H "Authorization: Bearer $GEM_API_KEY" \
  | jq '. | length'

# Contacted count (those enrolled in sequence step 1+)
curl "https://api.gem.com/v1/sequences/{seq_id}/enrollments?status=active,completed,replied,paused" \
  -H "Authorization: Bearer $GEM_API_KEY" \
  | jq '. | length'

# Replied count
curl "https://api.gem.com/v1/sequences/{seq_id}/enrollments?status=replied" \
  -H "Authorization: Bearer $GEM_API_KEY" \
  | jq '. | length'
```

Pre-ATS counts (sourced + contacted + replied) come from CRM, NOT ATS. ATS starts counting at "Applied".

### Recipe 7: Funnel rate computation

```python
import requests, os

def compute_per_req_funnel(req_id, gem_key, ats_key, ats_type="greenhouse"):
    """Return funnel rates + counts for a single req."""

    # Pre-ATS (Gem)
    sourced = gem.get_prospect_count(req_id=req_id)
    contacted = gem.get_contacted_count(req_id=req_id)
    replied = gem.get_replied_count(req_id=req_id)

    # ATS
    if ats_type == "greenhouse":
        apps = greenhouse.get_applications(job_id=req_id)
        screened = sum(1 for a in apps if a["current_stage"]["name"] not in ["Application Review", "Rejected"])
        offered = sum(1 for a in apps if a.get("offers"))
        hired = sum(1 for a in apps if a["status"] == "hired")

    return {
        "sourced": sourced,
        "contacted": contacted,
        "replied": replied,
        "screened": screened,
        "offered": offered,
        "hired": hired,
        "source_to_contact_pct": contacted / sourced if sourced else 0,
        "contact_to_reply_pct": replied / contacted if contacted else 0,
        "reply_to_screen_pct": screened / replied if replied else 0,
        "screen_to_offer_pct": offered / screened if screened else 0,
        "offer_acceptance_pct": hired / offered if offered else 0,
    }
```

### Recipe 8: Per-source funnel breakdown (the diagnosis lever)

```python
# Same as Recipe 7 but split by source attribution
def compute_per_source_funnel(req_id):
    sources = ["LinkedIn", "GitHub", "Wellfound", "Gem outbound", "Referral", "Boomerang", "Diversity Channel"]
    funnels = {}

    for source in sources:
        apps = ats.get_applications(req_id=req_id, source=source)
        funnels[source] = compute_funnel_for_app_list(apps)

    return funnels
```

Per-source breakdown surfaces which channels are over- or under-performing.

### Recipe 9: Bottleneck stage detection

```python
def detect_bottleneck(funnel):
    """Returns the stage with the worst conversion vs benchmark."""
    benchmarks = {
        "source_to_contact_pct": 0.40,
        "contact_to_reply_pct": 0.08,
        "reply_to_screen_pct": 0.55,
        "screen_to_offer_pct": 0.35,
        "offer_acceptance_pct": 0.85
    }
    gaps = {stage: benchmarks[stage] - funnel[stage] for stage in benchmarks if funnel[stage] is not None}
    if not gaps:
        return None
    return max(gaps, key=gaps.get)

# Usage:
bottleneck = detect_bottleneck(funnel)
# → "contact_to_reply_pct" — meaning low reply rate is the constraint
```

Map bottleneck stage to intervention:

| Bottleneck | Likely cause | Intervention |
|-----------|-------------|--------------|
| Source-to-contact <25% | Boolean too broad → too many invalid contacts | Tighten Boolean (`linkedin-recruiter-boolean-search-strings`) |
| Contact-to-reply <5% (eng) | Template generic / wrong subject / no profile-view | Rewrite InMail (`cold-inmail-warm-intro`) + A/B subject |
| Reply-to-screen <30% | Wrong-fit replies → too broad ICP | Tighten ICP segmentation (`passive-candidate-outreach-campaigns`) |
| Screen-to-offer <20% | Interview process leaks | Audit interview rubric (defer to `operations-agent`) |
| Offer-acceptance <70% | Comp below market / slow process | Audit comp band (defer to `ceo-agent` for exec, `operations-agent` for IC) |

### Recipe 10: Weekly funnel snapshot to Google Sheet

```python
# Pseudo — runs Monday 9am via cron
import gspread
from datetime import date

OPEN_REQS = greenhouse.list_open_jobs()
funnel_rows = []

for req in OPEN_REQS:
    f = compute_per_req_funnel(req["id"])
    bottleneck = detect_bottleneck(f)
    funnel_rows.append([
        date.today().isoformat(),
        req["id"],
        req["name"],
        f["sourced"], f["contacted"], f["replied"],
        f["screened"], f["offered"], f["hired"],
        f["source_to_contact_pct"], f["contact_to_reply_pct"],
        f["reply_to_screen_pct"], f["screen_to_offer_pct"], f["offer_acceptance_pct"],
        bottleneck or ""
    ])

sheet = gspread.open_by_key(os.environ["GOOGLE_SHEET_ID"]).worksheet("Weekly Funnel")
sheet.append_rows(funnel_rows)
```

### Recipe 11: Sample size warning (don't read tea leaves on N<30)

```python
def warn_low_sample(funnel, stage):
    """Returns True if sample size at stage is too low for confident inference."""
    counts = {
        "source_to_contact_pct": funnel["sourced"],
        "contact_to_reply_pct": funnel["contacted"],
        "reply_to_screen_pct": funnel["replied"],
        "screen_to_offer_pct": funnel["screened"],
        "offer_acceptance_pct": funnel["offered"]
    }
    return counts[stage] < 30  # 30 is the minimum for statistical confidence
```

If `warn_low_sample == True`, present rate as "preliminary" — don't trigger interventions on noise.

### Recipe 12: Per-segment funnel (when segmenting by role family)

```python
# Same as Recipe 7 but per-role-family
SEGMENTS = ["staff-backend", "staff-frontend", "eng-manager", "product-designer", "enterprise-AE"]

for seg in SEGMENTS:
    reqs_in_segment = [r for r in OPEN_REQS if r["job_family"] == seg]
    funnel = aggregate_funnels([compute_per_req_funnel(r["id"]) for r in reqs_in_segment])
    print(f"{seg}: {funnel}")
```

Segment funnels reveal which role families are healthy and which need targeted intervention.

## Examples

### Example 1: Diagnose 3% reply rate on staff backend sequence
**Goal:** Sourcer reports 3% reply rate on a sequence; benchmark is 7-9% for eng.
**Steps:**
1. Recipe 7 — compute funnel for the req.
2. Recipe 9 — detect bottleneck → confirmed `contact_to_reply_pct = 0.03`.
3. Recipe 11 — sample size check: N=180 contacts → above 30 → real signal.
4. Diagnose: pull 20 sample InMails. Are they <400 chars? 16-27 char subject? Profile-view-first?
5. Hypothesis: subjects generic ("Job opportunity at our co"). Rewrite per Recipe 10 in `cold-inmail-warm-intro`.
6. A/B test new template; track reply rate over 14 days.

**Result:** Reply rate climbs from 3% to 9-12% after subject + template rewrite.

### Example 2: Weekly Monday dashboard update
**Goal:** Refresh weekly funnel dashboard for sourcing-team standup.
**Steps:**
1. Monday 9am cron → Recipe 10 — pull per-req funnels for all open reqs.
2. Append to Google Sheet "Weekly Funnel" tab.
3. Slack post to `#sourcing-team`: "Funnel updated. Top 3 bottlenecks: REQ-2026-04 contact-to-reply, REQ-2026-09 source-to-contact, REQ-2026-12 reply-to-screen."
4. Per req with bottleneck → tag interventions in Linear.

**Result:** Visibility on per-req health; recruiter-coord intervenes same-day.

### Example 3: Per-source funnel diagnoses underperforming channel
**Goal:** Sourcing manager asks "which channel is underperforming on engineering reqs?"
**Steps:**
1. Recipe 8 — compute per-source funnel for last 90 days of eng reqs.
2. Surface results:
   - LinkedIn Recruiter: source-to-contact 45%, contact-to-reply 9%, reply-to-screen 60% — healthy.
   - GitHub mining: source-to-contact 60%, contact-to-reply 6%, reply-to-screen 40% — reply-to-screen low (wrong-fit replies).
   - Wellfound: source-to-contact 25%, contact-to-reply 15%, reply-to-screen 70% — source-to-contact low (post yields weak top-of-funnel).
3. Recommendations:
   - GitHub: tighten ICP — getting replies but wrong people. Add filters for years_experience + location.
   - Wellfound: re-evaluate posting tier — if not on Recruit Pro, upgrade for better matching.

**Result:** Per-channel intervention plan; channels rebalanced over 30 days.

## Edge cases / gotchas

- **Pre-ATS data lives in CRM (Gem); ATS-stage data lives in ATS.** Don't try to compute "sourced" from ATS — ATS starts at Applied. CRM holds Sourced + Contacted + Replied.
- **Source attribution at ATS push is critical.** Without source_id set at push, per-source funnel is impossible. Antipattern 6 in role.md.
- **Sample size <30 = noise.** Don't trigger interventions on N=5 contacts; wait for sample.
- **Replied count from Gem may underreport.** Gem detects email + LinkedIn replies; some candidates reply via phone or alt channel. Treat as ~95% accurate.
- **"Screened" definition varies by ATS.** Greenhouse: past Application Review stage. Ashby: past Initial Screen. Lever: past Phone Screen. Standardize per recipient's ATS.
- **Offer-acceptance <85% has multiple causes:** comp below market, slow process, counter-offer at current employer, role-shape mismatch. Diagnose before intervention.
- **Per-req funnel rates fluctuate weekly.** Smooth over 4-week trailing window for trend signals.
- **Diversity channels have different baselines.** /dev/color / Code2040 channel reply rates often 15-25% (warm) vs 7-9% LinkedIn (cold). Don't compare directly.
- **Layoff-triggered sourcing surges have abnormal reply rates** (20-30%) — temporary. Reset baseline after wave.
- **Seasonal effects.** Q4 holiday + Q1 enrollment cycles depress reply rates ~30%. Adjust expectations Dec-Feb.
- **Defer to `source-of-hire-reporting`** for aggregate across-reqs reporting and source-of-hire attribution.
- **Defer to `candidate-experience-hygiene-response-time`** for 24h reply SLA + 7d stage SLA tracking.
- **Defer interview-stage diagnostics (screen-to-offer < 20%)** to `operations-agent`'s interview-rubric skill — sourcer doesn't own interview process.
- **Defer offer-band diagnostics (offer-accept <70%)** to `operations-agent` (IC roles) or `ceo-agent` (exec) for comp philosophy.

## Sources

- Unified.to — 15 ATS APIs 2026: https://unified.to/blog/15_ats_apis_to_integrate_with_in_2026_greenhouse_lever_workable
- Outsail — Greenhouse vs Lever vs Ashby: https://www.outsail.co/post/greenhouse-vs-lever-vs-ashby
- Metaview — Recruiting Trends 2026: https://www.metaview.ai/resources/blog/recruiting-trends
- Greenhouse Harvest API: https://developers.greenhouse.io/harvest.html
- Ashby API: https://developers.ashbyhq.com/
- Lever API: https://hire.lever.co/developer/documentation
- Gem API: https://www.gem.com/api
