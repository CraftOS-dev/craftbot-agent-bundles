<!--
Source: https://www.facebook.com/business/help/2030467957953706
Source: https://support.google.com/google-ads/answer/9270967
Structured account audit: signal health + structure + spend leak + bid strategy + audience overlap.
-->
# Account Audit — Meta + Google — SKILL

A structured audit pass finds the 5-15 leverage fixes that recover 10-30% of wasted spend in 1-2 weeks. This skill ships the audit framework — signal health, structure inventory, spend leak detection, bid strategy distribution, audience overlap, naming compliance — plus the xlsx deliverable template ranked by severity + revenue impact.

## When to use this skill

- **New client / new ad account** — first deliverable.
- **Quarterly health check** on accounts the agent manages.
- **Pre-scale audit** — fix issues before turning up budget.
- **Performance regression diagnosis** — ROAS dropped; audit to find why.
- **Inheritance from prior agency** — clean slate audit.

**Do NOT use this skill when:**
- Account brand-new with no spend (<7d) — nothing to audit.
- Pure creative-only audit (use `creative-testing-matrix-design` instead).
- Conversion tracking only (use `attribution-debugging-utm-hygiene`).

## Setup

### Audit dimensions (Meta + Google)

| Dimension | Tool | Severity weight |
|---|---|---|
| Signal health (CAPI + pixel + AEM) | Meta `check_signal_health`; Google EC status | P0 |
| Account structure complexity | Counts via MCP `list_*` | P1 |
| Spend leak (paused-parent, zero-conversion adsets) | Warehouse SQL | P0/P1 |
| Bid strategy distribution | Aggregate over campaigns | P1 |
| Audience overlap | Meta Audience Overlap Tool | P1 |
| UTM hygiene | `attribution-debugging-utm-hygiene` skill | P1 |
| Naming convention | regex audit | P2 |
| Ad fatigue | `ad-fatigue-rotation-strategy` skill output | P1 |
| Conversion-goal config (Google) | account-level review | P0 |
| Brand exclusion (PMax) | PMax campaign check | P1 |

### Severity legend

- **P0** — fix this week; >$1K/week revenue impact OR critical signal issue
- **P1** — fix this month; >$1K/month impact
- **P2** — data hygiene / organization
- **P3** — naming + minor cleanup

## Common recipes

### Recipe 1: Meta signal health check

```bash
mcp tool meta-ads.check_signal_health > meta-signal.json
# Returns:
# {
#   "pixel_id": "...",
#   "event_match_quality": 7.8,
#   "capi_status": "healthy",
#   "missing_parameters": ["em","ph"],
#   "deduplication_status": "good",
#   "aem_event_priority_set": true,
#   "recommendations": [...]
# }

# Triage:
# - event_match_quality < 7 → P0 (add CAPI params)
# - capi_status != "healthy" → P0
# - deduplication_status != "good" → P0
# - aem_event_priority_set != true → P0 (configure AEM)
```

### Recipe 2: Meta account structure inventory

```bash
# Counts
campaigns=$(mcp tool meta-ads.list_campaigns --status "ALL" | jq 'length')
adsets=$(mcp tool meta-ads.list_adsets --status "ALL" | jq 'length')
ads=$(mcp tool meta-ads.list_ads --status "ALL" | jq 'length')
echo "Campaigns: $campaigns, Adsets: $adsets, Ads: $ads"

# Paused parent + active children (spend leak)
mcp tool meta-ads.list_campaigns --filter '{"status":"PAUSED"}' | jq -r '.[].id' > paused-campaigns.txt
for cid in $(cat paused-campaigns.txt); do
  active_adsets=$(mcp tool meta-ads.list_adsets --campaign_id "$cid" --filter '{"status":"ACTIVE"}' | jq 'length')
  if [ "$active_adsets" -gt 0 ]; then
    echo "P1: Campaign $cid is paused but has $active_adsets active adsets"
  fi
done
```

### Recipe 3: Spend leak — zero-conversion / high-spend adsets

```sql
-- PostgreSQL warehouse query
SELECT 
  ad_set_id,
  ad_set_name,
  SUM(spend) AS spend_7d,
  SUM(conversions) AS conv_7d,
  SUM(spend) / 7 AS daily_spend,
  ROUND(SUM(spend) / NULLIF(SUM(conversions), 0), 2) AS cpa
FROM ads_warehouse.platform_daily_spend
WHERE platform = 'meta'
  AND date BETWEEN CURRENT_DATE - 7 AND CURRENT_DATE - 1
GROUP BY ad_set_id, ad_set_name
HAVING SUM(spend) > 100 AND SUM(conversions) = 0
ORDER BY spend_7d DESC;
```

For each: P0 if daily_spend > $50; P1 otherwise. Action: pause or rotate creative.

### Recipe 4: Bid strategy distribution

```bash
# Meta — bid strategy mix
mcp tool meta-ads.list_adsets --fields '["id","name","bid_strategy"]' --status "ACTIVE" \
  | jq -r '.[] | .bid_strategy' \
  | sort | uniq -c | sort -rn
# Output:
#   124 LOWEST_COST_WITHOUT_CAP
#    47 LOWEST_COST_WITH_BID_CAP
#    18 LOWEST_COST_WITH_MIN_ROAS
#     8 COST_CAP

# Flag: if >70% are one strategy, likely missing prospecting (Lowest Cost) or retargeting (Min ROAS).
```

### Recipe 5: Meta Audience Overlap (manual check)

```python
# No public API for Audience Overlap Tool. Use Custom Audience size + adset targeting overlap heuristic
import requests, os
audiences = requests.get(
  f"https://graph.facebook.com/v19.0/act_{AD_ACCOUNT_ID}/customaudiences",
  params={"access_token": META_TOKEN, "fields": "id,name,approximate_count"}).json()["data"]

# For each pair: if both are used by adsets in same campaign AND sizes are similar → flag for manual overlap tool check
flagged_pairs = []
for a in audiences:
    for b in audiences:
        if a["id"] < b["id"] and abs(a["approximate_count"] - b["approximate_count"]) / max(a["approximate_count"], 1) < 0.30:
            flagged_pairs.append((a["name"], b["name"]))
print(flagged_pairs)
# Then check Audience Overlap Tool in UI for each pair
```

### Recipe 6: Google account audit — recommendations + GAQL

```bash
# Recommendations
mcp tool google-ads.get_recommendations --customer_id "$CID" > recs.json

# Classify by type
jq '.[] | {type: .type, impact: .impact, dismissed: .dismissed}' recs.json | jq -s 'group_by(.type) | map({type: .[0].type, count: length})'
# Output:
# [
#   {"type": "KEYWORD", "count": 23},
#   {"type": "CAMPAIGN_BUDGET", "count": 5},
#   {"type": "MAXIMIZE_CONVERSIONS_OPT_IN", "count": 3},
#   {"type": "RESPONSIVE_SEARCH_AD", "count": 12}
# ]

# GAQL — quality score distribution
mcp tool google-ads.search --customer_id "$CID" --query "
  SELECT ad_group_criterion.quality_info.quality_score,
         COUNT(ad_group_criterion.keyword.text) AS keywords
  FROM keyword_view
  WHERE ad_group_criterion.status = 'ENABLED'
  GROUP BY ad_group_criterion.quality_info.quality_score"
```

### Recipe 7: PMax brand exclusion check

```bash
# Verify PMax campaigns have brand exclusion
mcp tool google-ads.search --customer_id "$CID" --query "
  SELECT campaign.id, campaign.name, campaign.brand_guidelines_enabled
  FROM campaign
  WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'"

# Check campaign-level negative keywords
for cid in $(...); do
  mcp tool google-ads.search --customer_id "$CID" --query "
    SELECT campaign_negative_criterion.keyword.text
    FROM campaign_negative_criterion
    WHERE campaign.id = $cid"
done
# Flag: PMax with no brand exclusion = P0 (cannibalizing brand search)
```

### Recipe 8: Generate audit deliverable xlsx

```python
import openpyxl
wb = openpyxl.Workbook()

# Summary tab
summary = wb.active
summary.title = "Summary"
summary.append(["Severity","Count","Est weekly $ impact"])
summary.append(["P0", 4, 7200])
summary.append(["P1", 9, 5400])
summary.append(["P2", 12, 1100])
summary.append(["P3", 18, 0])
summary.append([])
summary.append(["TOTAL", 43, 13700])

# Findings tab
findings = wb.create_sheet("Findings")
findings.append(["#","Severity","Area","Description","Est $/week impact","Owner","Status","Due"])
findings.append([1,"P0","Signal","CAPI dedup broken — Meta showing 47% duplicate events","$4,200","ads-team","open","this week"])
findings.append([2,"P0","Signal","Pixel match rate 41% (target 75%+). Add em/ph to CAPI","$2,800","ads-team","open","this week"])
findings.append([3,"P0","Spend leak","7 paused campaigns with active adsets — $340/day total","$2,380","ads-team","open","this week"])
findings.append([4,"P1","Audience","LAL-1% × LAL-3% overlap >50% — cannibalizing","$1,800/mo","ads-team","open","this month"])
# ... etc

# Remediation timeline tab
timeline = wb.create_sheet("Timeline")
timeline.append(["Week","Findings to address","Owner","Status"])
timeline.append([1,"P0 — Signal + Spend leak","ads-team",""])
timeline.append([2,"P1 — Audience overlap + UTM fix","ads-team",""])
timeline.append([3,"P2 — Naming + frequency","ads-team",""])
timeline.append([4,"P3 — Lookalike seed refresh","ads-team",""])

wb.save("Meta-Audit-Brand-2026Q3.xlsx")
```

### Recipe 9: Naming convention compliance

```bash
# Pull all campaign names
mcp tool meta-ads.list_campaigns --fields '["id","name"]' | jq -r '.[].name' > names.txt

# Validate against convention: <Tier>-<Funnel>-<Audience>-<Offer>-<Period>
# e.g., "Cold-Prospecting-LAL1pct-20off-Q3"
python -c "
import re
PATTERN = re.compile(r'^(Cold|Warm|Hot)-(Prospecting|Retargeting|Cross-sell)-[A-Z0-9_-]+-[A-Z0-9_-]+-Q[1-4]\$', re.I)
with open('names.txt') as f:
    violations = [n.strip() for n in f if not PATTERN.match(n.strip())]
print(f'{len(violations)} of {sum(1 for _ in open(\"names.txt\"))} campaigns violate naming convention')
"
```

## Examples — full audit deliverable

```markdown
# Meta Account Audit — Brand X — 2026-06-09

## Executive summary
- Total findings: 43 (4 P0, 9 P1, 12 P2, 18 P3)
- Est revenue impact (recovery): $13,700/week if all P0+P1 fixed
- Account spend: $87K/month
- ROAS (last 30d): 2.8x blended
- Recommended scaling: HOLD until P0 fixed; revisit week 3

## P0 findings (fix this week, >$1K/week impact each)
1. **CAPI dedup broken**. Meta Events Manager shows 47% duplicate events 
   across pixel + CAPI. Meta is retraining on duped signal. 
   Impact: $4,200/week wasted spend.
   Action: Fix Stape GTM-S template — event_id passthrough.
   
2. **Pixel match rate 41%** (target 75%+). Email hash missing on 60% of CAPI events.
   Impact: $2,800/week (reduced learning signal).
   Action: Add `em` to all CAPI payloads from server template.

3. **7 paused campaigns with active adsets** spending $340/day total.
   Impact: $2,380/week direct leak.
   Action: Pause all child adsets via bulk update.

4. **AEM 8-event priority not configured** for iOS traffic.
   Impact: ~$1,800/week (iOS optimization signal lost).
   Action: Configure priorities via Meta MCP `manage_aem_events`.

## P1 findings (fix this month)
... 9 items

## P2 findings (data hygiene)
... 12 items

## P3 findings (naming + cleanup)
... 18 items

## Remediation timeline
- Week 1: All P0 (CAPI, pixel, spend leak, AEM)
- Week 2-3: P1 (audience overlap, UTM, bid strategy mix)
- Week 4: P2 (frequency rotation, fatigue audit)
- Quarterly: P3 (lookalike refresh, naming bulk rename)

## Re-audit cadence
- Weekly: signal health + spend leak
- Monthly: full audit
- Quarterly: full audit + benchmark vs Q-1
```

## Edge cases

### Account too small for full audit
<$10K/month spend: skip audience overlap + bid distribution. Focus signal + spend leak + naming.

### Multi-account / MCC
Run audit per child account; roll up to MCC-level summary.

### Recent changes hide issues
Significant edits (last 7d) confound diagnosis. Note "audit data baseline excludes changes after [date]."

### Brand vs non-brand conflation
PMax cannibalizing brand search is hidden unless you check brand exclusion explicitly. Always include in P0 review.

### Conversion goals (Google) — single primary
PMax with multiple primary conversion goals = optimization confusion. Recommended: one primary per campaign or account-level.

### Quality Score < 7
Audit: how many keywords at QS ≤ 6? If >30% of spend in QS≤6 keywords → P1, ad relevance / LP issue.

### Audience approval pending
LinkedIn / Reddit custom audiences sometimes stay pending for days. Note status in audit.

### Naming convention rewrite risk
Bulk rename can break attribution joins. Mark P2/P3; coordinate with reporting changes.

### Audit vs improvement
Audit identifies; doesn't fix. Owner column makes accountability explicit.

### Quarterly comparison
Save audit findings to Notion or `notion-mcp` for QoQ progress tracking.

## Sources

- Meta signal health: https://www.facebook.com/business/help/2030467957953706
- Meta CAPI signal: https://developers.facebook.com/docs/marketing-api/conversions-api/business-tools/signal-status
- Meta Audience Overlap Tool: https://www.facebook.com/business/help/516840952922734
- Google Recommendations: https://support.google.com/google-ads/answer/9270967
- Google Recommendations API: https://developers.google.com/google-ads/api/docs/recommendations
- Google Quality Score: https://support.google.com/google-ads/answer/6167118
- Google account structure best practices: https://support.google.com/google-ads/answer/1704396
- PMax brand exclusion: https://support.google.com/google-ads/answer/12252233
- Account-level negative keyword list: https://support.google.com/google-ads/answer/3273460
