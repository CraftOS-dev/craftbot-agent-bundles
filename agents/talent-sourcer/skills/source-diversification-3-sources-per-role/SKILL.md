<!--
Sources: https://www.lupahire.com/blog/candidate-sourcing-tools-for-recruiters
         https://www.metaview.ai/resources/blog/sourcing-tools-for-recruiters
         https://www.sourcecon.com/
         https://www.metaview.ai/resources/blog/recruiting-trends
         https://www.outsail.co/post/greenhouse-vs-lever-vs-ashby
Best-in-class teams use >=3 sources per role; no single source >60% of pipeline.
Weekly review per req tracking source mix + diversity index.
SourceCon source-of-hire dashboards are the community-standard reference.
-->
# Source Diversification — 3+ Sources Per Role — SKILL

Enforce the "≥3 active sources per role, no single source >60% of pipeline" rule. Pull per-req source breakdown from Greenhouse / Ashby / Lever, surface single-source-dominant reqs, and prescribe the rebalance channel + Boolean. Pipeline resilience to single-channel disruption (LinkedIn pricing change, seat loss, policy shift) is the explicit goal. SourceCon's source-of-hire dashboards are the community-standard pattern this skill operationalizes.

## When to use

- User wants a **weekly per-req source-mix audit** ("which reqs need a 3rd channel?").
- User wants to **rebalance a LinkedIn-heavy req** (80%+ pipeline from one source).
- User wants to **prescribe the next channel** to activate for a stalled req.
- User asks: "source mix", "channel concentration", "diversification check", "rebalance pipeline", "3-source rule", "single-source risk".

Do not use for: total monthly source-of-hire dashboard (`source-of-hire-reporting` — that's hire outcomes); per-channel funnel diagnosis (`source-to-contact-metrics`); diversity-demographic channel routing (`diversity-channel-sourcing-dev-color-code2040`).

## Setup

```bash
# ATS keys for per-req source pull
export GREENHOUSE_API_KEY="harvest_xxx"
export ASHBY_API_KEY="xxx"
export LEVER_API_KEY="xxx"

# CRM for top-of-funnel source counts (Gem / hireEZ)
export GEM_API_KEY="xxx"

# Notion for the weekly review doc
export NOTION_API_KEY="secret_xxx"
export NOTION_REVIEW_DB="<db_id>"

# Optional — Slack for breach alerts
export SLACK_BOT_TOKEN="xoxb-xxx"
```

## Common recipes

### Recipe 1: The diversification rule (canonical thresholds)

| Metric | Pass | Investigate | Breach |
|---|---|---|---|
| Active sources per req | ≥3 | 2 | 1 |
| Single source share of pipeline | <40% | 40-60% | >60% |
| Channels touched in last 14 days | ≥3 | 2 | ≤1 |
| Diversity channels engaged | ≥2 | 1 | 0 |
| GitHub/SO/portfolio channel for tech roles | active | warming | inactive |

Apply per requisition. Breach = remediate within 7 days (add channel + Boolean + outreach quota).

### Recipe 2: The 5-tier source-mix model

```
Tier 1 — Primary (always on):
  - LinkedIn Recruiter + Sales Nav
  - Internal ATS (alumni, past applicants, hot-list)
  - Employee referrals

Tier 2 — Channel-specific by role family:
  - Engineering: GitHub, Stack Overflow, Kaggle, DEV.to, conference speaker lists
  - Design: Behance, Dribbble, Awwwards, Twine
  - Sales: RepVue, Bravado, Pavilion
  - CS: Gain Grow Retain, CS in Focus

Tier 3 — Niche boards:
  - Wellfound (startups), Hired (curated), Built In (US metros), Otta, YC Work at a Startup

Tier 4 — Diversity channels:
  - /dev/color, Code2040, Lesbians Who Tech, Out in Tech, Latinas in Tech, AfroTech, Grace Hopper, Tapia

Tier 5 — Outbound CRM sequences:
  - Gem, hireEZ, Beamery (sourcing automation)
```

Rule of thumb: pull from 1 channel per active tier minimum. Engineering req without GitHub = breach. Sales req without RepVue = breach. Senior tech without diversity channel engagement = breach.

### Recipe 3: Greenhouse — pull per-req source breakdown (last 30d)

```bash
# Per-req active candidate source distribution
REQ_ID=12345
curl -u "$GREENHOUSE_API_KEY:" \
  "https://harvest.greenhouse.io/v1/applications?job_id=$REQ_ID&status=active&created_after=$(date -u -d '30 days ago' +%Y-%m-%dT%H:%M:%SZ)&per_page=500" \
  | jq 'group_by(.source.public_name) | map({source: .[0].source.public_name, count: length}) | sort_by(-.count)'
```

Output:
```
[
  {"source": "LinkedIn Recruiter", "count": 87},
  {"source": "Employee Referral", "count": 12},
  {"source": "Wellfound", "count": 4}
]
```

Compute share: LinkedIn = 87/(87+12+4) = 84% → BREACH (single source >60%). Action: rebalance.

### Recipe 4: Ashby — per-req source mix

```bash
JOB_ID="<ashby-job-id>"
curl -X POST "https://api.ashbyhq.com/application.list" \
  -u "$ASHBY_API_KEY:" \
  -d "{\"jobId\":\"$JOB_ID\",\"limit\":500,\"createdSince\":\"$(date -u -d '30 days ago' +%Y-%m-%dT%H:%M:%SZ)\"}" \
  | jq '.results | group_by(.source.title) | map({source: .[0].source.title, count: length}) | sort_by(-.count)'
```

### Recipe 5: Lever — per-posting source mix

```bash
POSTING_ID="<lever-posting-id>"
curl -u "$LEVER_API_KEY:" \
  "https://api.lever.co/v1/opportunities?posting_id=$POSTING_ID&created_at_start=$(date -d '30 days ago' +%s)000&limit=500" \
  | jq '[.data[] | {source: (.sources[0] // "Unknown")}] | group_by(.source) | map({source: .[0].source, count: length}) | sort_by(-.count)'
```

### Recipe 6: Compute concentration index (HHI for sourcing)

```python
# Herfindahl-Hirschman Index applied to sourcing
# Score < 0.25: well-diversified
# Score 0.25-0.5: moderate concentration; investigate
# Score > 0.5: dominant single source; REBALANCE

def hhi(source_counts: dict) -> float:
    total = sum(source_counts.values())
    if total == 0: return 0
    shares = [count / total for count in source_counts.values()]
    return sum(s * s for s in shares)

# Example
sources = {"LinkedIn Recruiter": 87, "Referral": 12, "Wellfound": 4}
print(f"HHI = {hhi(sources):.3f}")    # 0.732 -> heavy concentration, breach
```

### Recipe 7: SourceCon-style per-req dashboard (Google Sheet schema)

```python
# Per-req weekly tracker — matches SourceCon source-of-hire dashboard pattern
schema = {
    "req_id": "ENG-2026-STAFF-PLATFORM-04",
    "week_of": "2026-06-08",
    "active_sources": 4,                     # how many distinct sources had >0 candidates this week
    "channels_touched_14d": 5,
    "top_source": "LinkedIn Recruiter",
    "top_source_share_pct": 47,              # PASS (<60)
    "hhi": 0.31,                              # moderate concentration
    "diversity_channels_engaged": 2,         # /dev/color + Lesbians Who Tech
    "tier1_active": True,                    # LinkedIn + Referral + ATS-hot-list
    "tier2_active": True,                    # GitHub mining running
    "tier3_active": False,                   # Wellfound dormant
    "tier4_active": True,                    # diversity channels
    "tier5_active": True,                    # Gem sequence
    "breach": False,
    "recommended_action": "Activate Wellfound (Tier 3); add 20 candidates from YC W25 batch"
}
```

### Recipe 8: Rebalance prescription — when LinkedIn is dominant

When Recipe 3 shows LinkedIn >60%:

| Role family | Add this channel | Boolean / activation |
|---|---|---|
| Backend Eng | GitHub mining | `github` MCP: `language:python+location:berlin+followers:>50` |
| Frontend Eng | GitHub + DEV.to | GitHub: `language:typescript+repos:>10`; DEV.to: top tags `react`, `nextjs` |
| ML / AI Eng | Kaggle + GitHub | Kaggle Grandmasters list; GitHub `language:python+topic:machine-learning+stars:>100` |
| Product Designer | Behance + Dribbble | Behance `/v2/users?available_for_hire=1`; Dribbble "for hire" filter |
| Sales (AE) | RepVue + Bravado | RepVue employer plan filter: `quota_attainment>=110%` |
| Customer Success | Gain Grow Retain + CS in Focus | Slack community warm intros |
| Marketing | Demand Curve + Superpath | Community sourcing + LinkedIn |
| Eng Manager | Internal referral + Lattice connections | Referral nudge to current managers |
| Senior IC for diversity goal | /dev/color + Lesbians Who Tech | See `diversity-channel-sourcing-dev-color-code2040` |
| Contractor / fractional | Toptal + Turing + Lemon.io | See `contractor-sourcing-toptal-turing-pesto` |
| CTO / VP Eng | Lusha + RocketReach + warm-intro via investors | See `cto-vp-eng-exec-sourcing` |

### Recipe 9: Weekly review meeting agenda (Notion template)

```markdown
# Sourcing Diversification Review — {date}

## Reqs in breach (single source >60% or <3 active sources)
- REQ-XXX | top source: LinkedIn 84% | action: activate GitHub + Wellfound by {date+7d}
- REQ-YYY | active sources: 2 | action: add diversity channel + outbound sequence by {date+7d}

## Reqs in investigation (40-60% concentration)
- REQ-ZZZ | top: LinkedIn 52% | watch; add 1 more channel if it climbs

## Reqs healthy
- REQ-AAA: 4 sources active, HHI 0.22, top source 38%

## Cross-cutting actions
- LinkedIn seat saturation across all reqs — invest in Gem outbound at seat level
- Diversity channels under-engaged on 5 reqs — schedule channel warm-intros
```

### Recipe 10: Automated weekly breach detector (cron)

```bash
#!/bin/bash
# Run every Monday 08:00
# Output: Slack alert with list of breaching reqs

OPEN_REQS=$(curl -u "$GREENHOUSE_API_KEY:" "https://harvest.greenhouse.io/v1/jobs?status=open&per_page=200" | jq -r '.[].id')

BREACHES=""
for REQ in $OPEN_REQS; do
  SOURCES=$(curl -u "$GREENHOUSE_API_KEY:" "https://harvest.greenhouse.io/v1/applications?job_id=$REQ&status=active&per_page=500" \
    | jq '[group_by(.source.public_name) | map({source: .[0].source.public_name, count: length})] | flatten')

  TOTAL=$(echo "$SOURCES" | jq '[.[].count] | add')
  TOP=$(echo "$SOURCES" | jq -r 'sort_by(-.count) | .[0]')
  TOP_COUNT=$(echo "$TOP" | jq '.count')
  ACTIVE_COUNT=$(echo "$SOURCES" | jq 'length')

  if [ "$TOTAL" -gt 10 ]; then
    SHARE=$((TOP_COUNT * 100 / TOTAL))
    if [ "$SHARE" -gt 60 ] || [ "$ACTIVE_COUNT" -lt 3 ]; then
      BREACHES+="REQ $REQ: $ACTIVE_COUNT sources, top $SHARE%\n"
    fi
  fi
done

if [ -n "$BREACHES" ]; then
  curl -X POST "https://slack.com/api/chat.postMessage" \
    -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
    -d "channel=$SLACK_RECRUITER_CHANNEL&text=:bar_chart: Source-mix breaches this week:\n$BREACHES"
fi
```

### Recipe 11: Channel activation playbook (the "how do I add Wellfound?" recipe)

When prescribing Wellfound activation:
1. Post job to Wellfound (free for startups; Recruit Pro $499/mo for sourcing): https://wellfound.com/recruit
2. Set up saved search for `role + location + experience`
3. Run candidate-search filter; target 20 prospects in 7 days
4. Enroll matching candidates in `wellfound-outbound` Gem sequence (template tagged `source=Wellfound`)
5. Confirm ATS `source = Wellfound` on each push so attribution lands

Repeat per channel. For diversity channels, see `diversity-channel-sourcing-dev-color-code2040` (warm-intro patterns differ; sponsor cycle required for some).

## Examples

### Example 1: Staff Backend Eng req — 84% LinkedIn, need to rebalance
**Goal:** REQ ENG-2026-STAFF-PLATFORM-04 has 87 candidates from LinkedIn, 12 referral, 4 Wellfound. Diversify.
**Steps:**
1. Run Recipe 3 → confirm LinkedIn 84% breach.
2. Compute HHI (Recipe 6) → 0.73, heavy.
3. Prescribe Tier 2 + Tier 3 + Tier 4 (Recipe 8):
   - Tier 2 (GitHub): target 25 contributors from top-starred Python+Go infra repos
   - Tier 3 (Wellfound + YC Work at a Startup): post + saved search
   - Tier 4 (/dev/color staff Slack channel): warm-intro request
4. Set 7-day target: bring LinkedIn share to <50% via 30 new candidates from GitHub + Wellfound + /dev/color.
5. Hand off Boolean to `github-talent-mining-language-stars-commits` + Wellfound activation to `hired-wellfound-built-in-otta-niche-boards`.

**Result:** Within 14 days, source mix = LinkedIn 49%, GitHub 22%, Wellfound 14%, Referral 11%, /dev/color 4%. HHI drops to 0.32. No breach.

### Example 2: Sales AE req with 0 RepVue presence
**Goal:** REQ SALES-AE-ENTERPRISE-02 sources 100% from LinkedIn Sales Nav. RepVue is the SOTA sales channel; not activated.
**Steps:**
1. Run Recipe 3 → single source breach (LinkedIn 100%).
2. Prescribe RepVue activation (Recipe 11, sales row of Recipe 8 table).
3. Activate RepVue employer plan; filter by `quota_attainment >= 110%` AND `tenure_at_company >= 18mo`.
4. Bring 15 RepVue candidates into pipeline within 7 days.
5. Activate Bravado as Tier 2 fallback for further diversification.

**Result:** Within 21 days, mix = LinkedIn 55%, RepVue 30%, Bravado 10%, Referral 5%. HHI 0.40.

### Example 3: Weekly review — surface 4 breaches across portfolio
**Goal:** Run weekly diversification check across 18 open reqs.
**Steps:**
1. Run Recipe 10 (automated detector) Monday 08:00.
2. Slack alert lists 4 reqs in breach.
3. Open Notion Recipe 9 template; populate the 3 sections.
4. Schedule 30min Tuesday review with sourcing team — each breach gets owner + 7d deadline.
5. Follow up Friday: confirm remediation actions complete; re-run Recipe 3 to verify.

**Result:** 4 breaches remediated within the week; pipeline resilience to LinkedIn outage / pricing change drastically improved across portfolio.

## Edge cases / gotchas

- **"Pipeline" definition matters.** Counting only `Applied` stage misses sourced-but-not-yet-applied prospects (CRM-tracked). Use union of (Gem prospects with last_touch<30d) + (ATS applications status=active).
- **Single-source IS healthy for some specialist roles.** A nuclear-physicist req from a single Tapia Conference warm intro may be the only viable channel. Use judgement — breach threshold is heuristic, not law.
- **HHI is sensitive to small denominators.** A req with 3 candidates total (2 from LinkedIn + 1 referral) shows HHI 0.56. Don't apply breach logic until total >10.
- **Source mis-tagging poisons everything.** If recruiters file all candidates as "Other" or "Sourced", you can't compute mix. Enforce: every ATS push includes `source = {LinkedIn | GitHub | Wellfound | Gem-sequence | Boomerang | Code2040 | etc.}` — see role.md Antipattern 6.
- **CRM-to-ATS handoff loses source.** Gem prospect with `source = LinkedIn Recruiter` becomes Greenhouse application with `source = Sourced` unless you propagate. Configure Gem → Greenhouse mapping per source.
- **"Referral" hides a lot.** Always sub-tag by `referral_source_{employee_slug}`. If 90% of "referrals" come from one engineer's personal network, that's a different concentration risk (key-person dependency).
- **Diversity channels appear small but are high-quality.** A /dev/color warm-intro candidate may be 1 of 100 in the funnel but 1 of 5 hires. Don't deprecate based on raw count.
- **LinkedIn seat saturation creates artificial concentration.** If your team only has 3 LinkedIn Recruiter seats and they're at InMail cap, you can't scale that channel — diversification becomes forced. Solve by adding Gem outbound (Tier 5).
- **Boomerang as a "source" is technically a channel but operationally a fast-track.** Tag boomerang candidates separately; don't let them inflate your "Internal ATS" tier.
- **Weekly review fatigue.** Don't run weekly if you have <10 open reqs; run biweekly. Don't run breach alert daily — Mondays only.
- **Add-a-channel is easy; remove-a-channel is hard.** Once recruiters get used to a niche board, they don't stop using it even if ROI dies. Track per-channel cost-per-hire monthly via `source-of-hire-reporting`; sunset losers explicitly.
- **Diversity-channel engagement is a relationship, not a switch.** "Activate /dev/color" implies sponsor cycle, attended events, warm intros built over months. Don't expect Day-1 candidate flow. See `diversity-channel-sourcing-dev-color-code2040`.
- **The "3 sources" rule is the floor, not the ceiling.** Top-tier teams use 5-7 active sources per role; the rule prevents the 1-source disaster, not optimizes the upside.
- **Hand off rebalance Boolean / activation work** to the matching skill: GitHub → `github-talent-mining-language-stars-commits`; Wellfound → `hired-wellfound-built-in-otta-niche-boards`; diversity → `diversity-channel-sourcing-dev-color-code2040`; sales → `sales-talent-sourcing-repvue`.

## Sources

- LupaHire — Candidate sourcing tools 2026: https://www.lupahire.com/blog/candidate-sourcing-tools-for-recruiters
- Metaview — Sourcing tools 2026: https://www.metaview.ai/resources/blog/sourcing-tools-for-recruiters
- Metaview — Recruiting Trends 2026: https://www.metaview.ai/resources/blog/recruiting-trends
- SourceCon — community-standard source-of-hire dashboards: https://www.sourcecon.com/
- Outsail — Greenhouse vs Lever vs Ashby (source field per ATS): https://www.outsail.co/post/greenhouse-vs-lever-vs-ashby
- Greenhouse Harvest API — Applications: https://developers.greenhouse.io/harvest.html#applications
- Ashby API — application.list: https://developers.ashbyhq.com/reference/applicationlist
- Lever API — Opportunities: https://hire.lever.co/developer/documentation
