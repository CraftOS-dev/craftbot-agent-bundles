<!--
Source: HubSpot Deals API + Salesforce SOQL + Gong pipeline research
Pipeline hygiene + stage criteria (June 2026 SOTA).
-->
# Pipeline Hygiene + Stage Criteria — SKILL

Pipeline is only as good as its hygiene. This skill defines explicit entry + exit criteria per stage, age-in-stage flagging, stalled-deal detection, coverage-ratio computation, and dedupe / archival rules. Runs weekly with output to a Notion pipeline review doc + Slack alerts; runs daily for hygiene flags.

## When to use

- **Weekly pipeline review prep** — pull open deals, flag stale + stalled + slip-risk.
- **Daily CRM hygiene cron** — dedupe, archive cold deals, enforce required fields.
- **Stage transition gate-keeping** — block deal advance unless exit criteria met.
- **Coverage ratio monitoring** — pipeline ÷ quota.
- **Trigger phrases**: "pipeline review", "stale deals", "stalled deals", "coverage check", "dedupe CRM", "stage criteria for X", "fix the pipeline".

Do NOT use this skill for: **deal-level next-best-action** (use `deal-coaching-next-best-action`); **forecast bucketing** (use `clari-forecasting-commit-accuracy`); **win/loss tagging** (use `win-loss-analysis-structured`).

## Setup

```bash
export MATON_API_KEY="<key>"   # CRM via api-gateway
export PG_URI="postgresql://..."  # for stage-median computation + history
export NOTION_TOKEN="<key>"       # pipeline review doc
export SLACK_TOKEN="<key>"        # alerts
```

One-time CRM setup: ensure each stage in your pipeline has a configured probability + a `dealstage` enum value with stable ID. Custom property `hs_time_in_dealstage` (HubSpot) or formula field (Salesforce) auto-populates age-in-stage.

## Common recipes

### Recipe 1: Pipeline stage criteria (canonical per role.md)

```yaml
1_prospect:
  entry:
    - account on ICP target list
    - first touch sent
  exit:
    - reply OR meaningful engagement (open + click + reply within 14d)
  typical_days: 0-14
  required_fields_to_advance: [icp_fit_score, lead_source]

2_discovery:
  entry:
    - discovery call scheduled OR completed
  exit:
    - MEDDIC: metrics + identify_pain at score >= 2
    - champion candidate named
  typical_days: 7-21
  required_fields: [meddic_metrics, meddic_identify_pain, meddic_champion_candidate]

3_evaluation:
  entry:
    - demo completed
    - technical eval underway
  exit:
    - decision criteria validated (meddic_decision_criteria score >= 2)
    - EB named (meddic_economic_buyer score >= 2)
  typical_days: 14-45
  required_fields: [meddic_decision_criteria, meddic_economic_buyer]

4_proposal:
  entry:
    - proposal sent (linked PandaDoc / DocuSign envelope ID)
    - mutual action plan signed
  exit:
    - all MEDDIC fields >= 2
    - competitor position known
  typical_days: 7-30
  required_fields: [proposal_doc_id, map_signed_date]

5_negotiation:
  entry:
    - verbal commit received
    - legal / procurement engaged
  exit:
    - redlines resolved
    - verbal close confirmed
  typical_days: 7-21
  required_fields: [legal_review_started_date, verbal_close_confirmed]

6_closed_won:
  entry:
    - contract signed (DocuSign/PandaDoc completed_at)
  exit:
    - implementation kickoff scheduled
  required_fields: [signed_date, kickoff_date]

6_closed_lost:
  entry:
    - prospect disqualified OR moved to competitor
  exit:
    - win/loss post-mortem completed
  required_fields: [lost_reason, postmortem_completed]
```

### Recipe 2: Pull open pipeline + bucket by stage

```bash
curl -X POST "https://gateway.maton.ai/hubspot/crm/v3/objects/deals/search" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "filterGroups":[{"filters":[
      {"propertyName":"dealstage","operator":"NOT_IN","values":["closedwon","closedlost"]},
      {"propertyName":"closedate","operator":"GTE","value":"'$(date -u +%Y-%m-%d)'"}
    ]}],
    "properties":["dealname","amount","dealstage","closedate","hs_time_in_dealstage","hubspot_owner_id","meddic_score","notes_last_contacted","createdate"],
    "limit":200,
    "sorts":[{"propertyName":"hs_time_in_dealstage","direction":"DESCENDING"}]
  }'
```

### Recipe 3: Stage median computation (one-time + refresh quarterly)

```sql
-- Median days-in-stage for closed-won deals (the realistic benchmark)
SELECT
    dealstage,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY days_in_stage) AS median_days,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY days_in_stage) AS p75_days,
    PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY days_in_stage) AS p90_days,
    COUNT(*) AS sample_size
FROM deal_stage_history
WHERE deal_id IN (SELECT id FROM deals WHERE dealstage = 'closedwon')
  AND entered_at > NOW() - INTERVAL '12 months'
GROUP BY dealstage
HAVING COUNT(*) >= 10
ORDER BY dealstage;
```

Refresh quarterly. Below 10 samples per stage, use industry benchmarks (SMB cycle 14-30d, Mid 45-90d, Enterprise 90-180d+).

### Recipe 4: Stale-deal flagging (age-in-stage > 1.5x median)

```python
STAGE_MEDIANS = {
    "qualifiedtobuy": 14, "presentationscheduled": 30, "decisionmakerboughtin": 21,
    "contractsent": 14, "closedwon": 0, "closedlost": 0,
}

def is_stale(deal):
    days_in_stage = int(deal["properties"].get("hs_time_in_dealstage", 0)) / 86400000  # ms → days
    median = STAGE_MEDIANS.get(deal["properties"]["dealstage"], 30)
    return days_in_stage > 1.5 * median, days_in_stage, median

# Apply to all open deals
stale_deals = [d for d in open_deals if is_stale(d)[0]]
```

### Recipe 5: Stalled-deal detection (no activity 14d)

```python
import datetime
def is_stalled(deal):
    last_contacted = deal["properties"].get("notes_last_contacted")
    if not last_contacted: return True
    days_silent = (datetime.datetime.now() - datetime.datetime.fromisoformat(last_contacted.replace("Z","+00:00"))).days
    return days_silent > 14

stalled_deals = [d for d in open_deals if is_stalled(d)]
```

### Recipe 6: Required-field enforcement (block stage advance)

```python
REQUIRED_FIELDS_BY_STAGE = {
    "discovery": ["meddic_metrics","meddic_identify_pain","meddic_champion_candidate"],
    "evaluation": ["meddic_decision_criteria","meddic_economic_buyer"],
    "proposal": ["proposal_doc_id","map_signed_date"],
    "negotiation": ["legal_review_started_date","verbal_close_confirmed"],
    "closedwon": ["signed_date","kickoff_date"],
    "closedlost": ["lost_reason","postmortem_completed"],
}

def can_advance(deal, target_stage):
    missing = [f for f in REQUIRED_FIELDS_BY_STAGE.get(target_stage, []) if not deal["properties"].get(f)]
    return (len(missing) == 0, missing)

# Block via HubSpot workflow OR via agent guard before PATCH
```

### Recipe 7: Coverage-ratio check (daily)

```python
quota_remaining = ae_quota - already_closed_won
total_pipe = sum(float(d["properties"].get("amount") or 0) for d in open_deals)
coverage = total_pipe / quota_remaining if quota_remaining > 0 else float("inf")

if coverage < 3.0:
    slack_alert(f"Coverage {coverage:.1f}× (target 3-4×). Trigger pipe-gen sprint.")
elif coverage > 5.0:
    slack_info(f"Coverage {coverage:.1f}× — likely some deals are mis-stage; review for over-counting")
```

### Recipe 8: Dedupe contacts (HubSpot built-in or query-based)

```bash
# HubSpot Pro+ has a built-in deduper UI; via API:
curl "https://gateway.maton.ai/hubspot/crm/v3/objects/contacts?properties=email,firstname,lastname,company&limit=100" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq -r '.results[] | [.id, .properties.email, .properties.firstname, .properties.lastname] | @tsv' | \
  sort -t$'\t' -k2 | awk -F'\t' 'NR==FNR{count[$2]++; next} count[$2]>1' /dev/fd/0 /dev/fd/0 > dupes.tsv
```

For Salesforce, use the Duplicate Management module or Cloudingo ($1k+/mo).

### Recipe 9: Archive cold deals (>90 days no activity, not closed)

```python
ARCHIVE_THRESHOLD_DAYS = 90

for deal in open_deals:
    if is_stalled(deal):  # uses Recipe 5
        last_contacted = deal["properties"].get("notes_last_contacted")
        days_silent = (datetime.datetime.now() - datetime.datetime.fromisoformat(last_contacted.replace("Z","+00:00"))).days
        if days_silent > ARCHIVE_THRESHOLD_DAYS:
            # Move to closed-lost with "no_decision" reason
            requests.patch(
                f"https://gateway.maton.ai/hubspot/crm/v3/objects/deals/{deal['id']}",
                headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"},
                json={"properties":{"dealstage":"closedlost","closed_lost_reason":"no_decision","postmortem_required":"true"}}
            )
```

Don't keep stale deals in open pipeline — they inflate coverage falsely.

### Recipe 10: Weekly pipeline review doc (Notion render)

```python
# Compose everything
review = f"""# Pipeline Review — Week of {today}

## Coverage
- Quota: ${ae_quota:,}
- Pipeline: ${total_pipe:,}
- Coverage: {coverage:.1f}× (target 3-4×)

## Per-AE
| AE | Open $ | Stale | Stalled | Coverage |
|---|---|---|---|---|
"""
for ae_id, ae_name in team:
    ae_deals = [d for d in open_deals if d["properties"]["hubspot_owner_id"] == ae_id]
    ae_pipe = sum(float(d["properties"].get("amount") or 0) for d in ae_deals)
    ae_stale = sum(1 for d in ae_deals if is_stale(d)[0])
    ae_stalled = sum(1 for d in ae_deals if is_stalled(d))
    review += f"| {ae_name} | ${ae_pipe:,.0f} | {ae_stale} | {ae_stalled} | {ae_pipe/(ae_quota_for(ae_id) or 1):.1f}× |\n"

review += """
## Top 10 stale deals (age > 1.5× median)
"""
for d in sorted(stale_deals, key=lambda x: -is_stale(x)[1])[:10]:
    days, _, median = is_stale(d)[1], 0, is_stale(d)[2]
    review += f"- {d['properties']['dealname']} ({d['properties']['dealstage']}, {int(days)}d / median {median}d)\n"

# Push to Notion
```

### Recipe 11: Daily hygiene cron tasks

```yaml
07:00_utc: pull open deals (Recipe 2)
07:05: stale flag (Recipe 4) → CRM property `is_stale = true/false`
07:10: stalled flag (Recipe 5) → CRM property `is_stalled = true/false`
07:15: coverage check (Recipe 7) → Slack alert if < 3×
07:30: dedupe scan (Recipe 8) → report only, no auto-merge (false-positives risky)
weekly_friday_18:00: archive cold deals (Recipe 9) — manual review of marked list, not auto-execute
weekly_monday_09:00: pipeline review doc (Recipe 10) → Notion + Slack
```

### Recipe 12: Velocity computation (median deal cycle)

```sql
SELECT
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY (closedate - createdate)) AS median_days_total,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY (closedate - createdate)) FILTER (WHERE amount < 25000) AS median_smb,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY (closedate - createdate)) FILTER (WHERE amount BETWEEN 25000 AND 100000) AS median_mid,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY (closedate - createdate)) FILTER (WHERE amount > 100000) AS median_ent
FROM deals
WHERE dealstage = 'closedwon' AND closedate > NOW() - INTERVAL '12 months';
```

Track quarter-over-quarter; rising velocity is a healthy signal.

## Examples

### Example 1: Monday pipeline-review doc

**Goal:** Every Monday 9am, sales leadership has a Notion doc + Slack ping with pipeline state.

**Steps:**
1. Recipe 2 — pull all open deals.
2. Recipes 4 + 5 — stale + stalled flags.
3. Recipe 7 — coverage by AE.
4. Recipe 10 — render to Notion; Slack post in `#sales-leadership` with top-3 alerts.
5. Manager runs 1:1s referencing this doc.

**Result:** Pipeline state visible without manual querying; coaching anchored on data.

### Example 2: Required-field gate prevents bad data

**Goal:** AE tries to move a deal from Discovery → Evaluation without `meddic_decision_criteria` set.

**Steps:**
1. PATCH request to update `dealstage` hits the agent's guard.
2. Recipe 6 — check required fields for target stage.
3. Missing: `meddic_decision_criteria`. Return error: "Cannot advance — fill <field> first".
4. (Optional) HubSpot workflow `required_property_validation` enforces the same rule at CRM level.

**Result:** Stage data is honest; downstream forecast + accuracy queries work.

### Example 3: Q-end cold-deal cleanup

**Goal:** End of quarter, clean out stalled deals so next quarter starts honest.

**Steps:**
1. Recipe 9 — list all deals > 90 days no activity.
2. Manager reviews list (some may be legitimate parking lots).
3. Approve closes; batch-update to `closedlost` with `lost_reason=no_decision`.
4. Win/loss post-mortems queued for the > $25K losses.

**Result:** New quarter starts with clean pipe, not lying-to-itself coverage.

## Edge cases / gotchas

- **`hs_time_in_dealstage` resets when you move backward** — moving from Proposal to Discovery (down-stage) resets the timer. The deal's true age is the cumulative time, not the current stage's clock.
- **Stage probabilities are NOT auto-updated** when you change `dealstage` via API — Recipe 6 of `hubspot-sales-mcp` shows the manual patch. Forgetting this leaves stale probabilities → bad forecast roll-up.
- **Stage definitions drift over time.** Re-audit stage criteria quarterly; what was "Evaluation" 2 years ago may map to "Discovery" today as sales motion matures.
- **Auto-archive risks**: not every cold deal is dead — strategic accounts can sit dormant 6 months legitimately. Tag those `do_not_auto_archive=true`.
- **Coverage > 5x** is suspicious, not great — often means stale deals are inflating pipe. Audit for stalled deals before celebrating "lots of pipeline".
- **Median-stage benchmarks need closed-won samples**, not closed-lost (losses cycle differently). Recipe 3 filters correctly.
- **Industry / segment / size variation**: SMB Discovery median is 7-14 days; Enterprise is 30-60. Compute medians per segment to avoid bad benchmarks.
- **Required-field workflow gotcha**: HubSpot's "Required to close" property setting only blocks at `closedwon`, not at mid-stage. Build the validation at the agent layer (Recipe 6) for mid-stage gates.
- **Dedupe false-positives**: Sam Jones at Acme is NOT the same person as Sam Jones at Globex. Match on email + LinkedIn URL, not name.
- **Stage history reliability**: Salesforce's OpportunityHistory is robust; HubSpot's stage timeline requires Marketing Hub Pro+ or a custom snapshot table (`postgresql-mcp` cron).
- **AE-level coverage**: team coverage of 4x can hide an AE at 1.5x. Always disaggregate.
- **Newly-created deals = noise** in coverage. Filter by `createdate > 30 days ago` for "qualified pipe" reporting; include all for raw coverage.

## Sources

- HubSpot Deals API: https://developers.hubspot.com/docs/api/crm/deals
- Salesforce Opportunity object + StageName: https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_objects_opportunity.htm
- Gong pipeline management research: https://www.gong.io/blog/sales-pipeline-management/
- Sales pipeline stage definitions 2026 (Sequoia): https://www.sequoiacap.com/article/sales-pipeline-stages/
- HubSpot duplicate management: https://knowledge.hubspot.com/contacts/manage-duplicate-contacts
- Cloudingo (Salesforce dedupe): https://cloudingo.com/
- Pipeline coverage benchmarks (CSO Insights 2026): https://cso-insights.com/research/pipeline-coverage
