<!--
Source: https://pasqualepillitteri.it/en/news/1707/official-meta-ads-mcp-claude-29-tools-2026
Source: https://www.facebook.com/business/help/463088240976772
Meta Campaign Budget Optimization (CBO / Advantage Campaign Budget) vs Ad Set Budget Optimization (ABO).
-->
# Meta Ads — Campaign Structure (CBO vs ABO) — SKILL

The single highest-leverage structural decision on Meta is **CBO (Advantage Campaign Budget)** vs **ABO (Ad Set Budget)**. Wrong choice burns 20-40% of monthly spend on the wrong audience pool. This skill encodes the 2026 SOTA decision tree, the campaign object spec, and the bid-strategy layer-by-layer recipe.

## When to use this skill

- **New campaign launch** on Meta (Facebook, Instagram, Messenger, Audience Network).
- **Account audit** flagging suboptimal CBO/ABO mix.
- **Scale event** moving from $200/day to $2K/day — the right structure changes.
- **Creative testing matrix** rollout (ABO is the clean read for matrix; CBO is the scaling vehicle after).
- **Audience pyramid build** (cold / warm / hot) needs different structures per layer.

**Do NOT use this skill when:**
- Non-Meta platforms (see `google-ads-performance-max`, `tiktok-ads-spark-promote`, `linkedin-ads-abm-campaigns`, `reddit-ads-niche-targeting`).
- Creative production (defer to `creative-brief-authoring-for-designers` + `video-creator`).
- Pixel / CAPI signal recovery (see `meta-capi-tiktok-events-google-enhanced-conversions`).

## Setup

### MCP — official Meta Ads MCP (mcp.facebook.com/ads)

```bash
# OAuth at https://mcp.facebook.com/ads/oauth
export META_ADS_MCP_TOKEN="<oauth-token>"
export META_AD_ACCOUNT_ID="act_<numeric>"
export META_BUSINESS_ID="<business-id>"
```

```json
// claude-config.json
{
  "meta-ads": {
    "transport": "https",
    "url": "https://mcp.facebook.com/ads/v1",
    "auth": {"type":"bearer","token":"${META_ADS_MCP_TOKEN}"}
  }
}
```

### Decision tree — CBO vs ABO

| Situation | Use | Why |
|---|---|---|
| Spend ≥$500/day, 2-5 audiences, all known-performers | **CBO** | Meta optimizes spend across; cheaper than manual |
| Spend <$200/day, single audience | **CBO** | Default; no upside to ABO complexity |
| Creative testing matrix (clean reads required) | **ABO** | Per-audience budget forces equal read at adset level |
| One audience much larger than others (broad vs LAL-1%) | **ABO** | CBO under-spends the smaller pool |
| Audience under-spending in CBO (<60% of allocated) | **ABO** override | Reclaim spend |
| Cold prospecting + hot retargeting in one campaign | **Split into 2 campaigns** | Never mix funnel stages |
| New account, no signal history | **CBO + Advantage+ Audience** | Let Meta learn |

### Graph API endpoint cheat-sheet

- Campaigns: `POST /act_{ad_account_id}/campaigns`
- Ad sets: `POST /act_{ad_account_id}/adsets`
- Ads: `POST /act_{ad_account_id}/ads`
- Insights: `GET /{campaign_id|adset_id|ad_id}/insights`

## Common recipes

### Recipe 1: CBO campaign — cold prospecting, $500/day, 4 audiences

```bash
# Step 1: Campaign with CBO enabled
mcp tool meta-ads.create_campaign \
  --name "Q3-Cold-Prospecting-CBO" \
  --objective "OUTCOME_SALES" \
  --special_ad_categories "[]" \
  --buying_type "AUCTION" \
  --status "PAUSED" \
  --daily_budget 50000 \
  --bid_strategy "LOWEST_COST_WITHOUT_CAP" \
  --is_advantage_campaign_budget true

# Step 2: Adsets — no per-adset budget (CBO controls)
for audience in LAL_1pct LAL_3pct InterestStack AdvantagePlus; do
  mcp tool meta-ads.create_adset \
    --campaign_id "$CAMPAIGN_ID" \
    --name "Cold-$audience" \
    --optimization_goal "OFFSITE_CONVERSIONS" \
    --billing_event "IMPRESSIONS" \
    --targeting "$(cat targeting-$audience.json)" \
    --start_time "$(date -u +%Y-%m-%dT00:00:00Z)"
done
```

### Recipe 2: ABO matrix — 6 cells × $50/day, creative test

```bash
# Step 1: Campaign with ABO (NO daily_budget at campaign)
mcp tool meta-ads.create_campaign \
  --name "Q3-Creative-Test-ABO" \
  --objective "OUTCOME_SALES" \
  --is_advantage_campaign_budget false \
  --buying_type "AUCTION"

# Step 2: 6 adsets, $50/day each, one cell per
for cell in C1 C2 C3 C4 C5 C6; do
  mcp tool meta-ads.create_adset \
    --campaign_id "$CAMPAIGN_ID" \
    --name "Test-$cell" \
    --daily_budget 5000 \
    --optimization_goal "OFFSITE_CONVERSIONS" \
    --billing_event "IMPRESSIONS" \
    --bid_strategy "LOWEST_COST_WITHOUT_CAP" \
    --targeting "$(cat targeting-$cell.json)"
done
```

### Recipe 3: Bid strategy by funnel layer

```bash
# Cold: Lowest Cost (no cap) — maximize volume
mcp tool meta-ads.update_adset \
  --adset_id "$COLD_ADSET" \
  --bid_strategy "LOWEST_COST_WITHOUT_CAP"

# Warm: Cost Cap at target CPA
mcp tool meta-ads.update_adset \
  --adset_id "$WARM_ADSET" \
  --bid_strategy "LOWEST_COST_WITH_BID_CAP" \
  --bid_amount 2500   # $25.00 in cents

# Hot retargeting: Minimum ROAS (Advantage+ Shopping only)
mcp tool meta-ads.update_adset \
  --adset_id "$HOT_ADSET" \
  --bid_strategy "LOWEST_COST_WITH_MIN_ROAS" \
  --roas_average_floor 250   # 2.5x ROAS floor
```

### Recipe 4: Raw Graph API — when MCP doesn't expose a field

```bash
# Direct Graph API call for CBO toggle on existing campaign
curl -X POST "https://graph.facebook.com/v19.0/$CAMPAIGN_ID" \
  -H "Authorization: Bearer $META_ACCESS_TOKEN" \
  -d "is_advantage_campaign_budget=true" \
  -d "daily_budget=50000"
```

### Recipe 5: ABO override when CBO under-spends a pool

```python
# Detect under-spending
import requests, os
campaign = os.environ["CAMPAIGN_ID"]
r = requests.get(
  f"https://graph.facebook.com/v19.0/{campaign}/insights",
  params={
    "access_token": os.environ["META_ACCESS_TOKEN"],
    "fields": "adset_id,adset_name,spend",
    "level": "adset",
    "date_preset": "last_7d",
  })
adsets = r.json()["data"]
total = sum(float(a["spend"]) for a in adsets)
underspent = [a for a in adsets if float(a["spend"]) / total < 0.10]

# Convert under-spent adset to ABO with its own budget
for a in underspent:
    requests.post(
      f"https://graph.facebook.com/v19.0/{a['adset_id']}",
      data={"daily_budget": 10000, "access_token": os.environ["META_ACCESS_TOKEN"]})
```

### Recipe 6: Structural duplication — clone winning adset into new audience

```bash
mcp tool meta-ads.duplicate_adset \
  --adset_id "$WINNER_ADSET" \
  --rename "Winner-Clone-LAL_5pct" \
  --new_targeting "$(cat targeting-LAL_5pct.json)"
```

## Examples — three reference structures

### Structure A — Lean DTC, $1K/day

```yaml
campaigns:
  - name: "Cold-CBO"
    budget: $600/day  (CBO)
    bid: Lowest Cost no cap
    adsets:
      - LAL-1% (purchasers 180d)
      - LAL-3%
      - Interest Stack
      - Advantage+ Audience (broad)
    exclusions: purchasers 90d, customer-list current
  - name: "Warm-CBO"
    budget: $250/day  (CBO)
    bid: Cost Cap $25 CPA
    adsets:
      - Video viewers 50%+ 30d
      - Page engagers 30d
      - ATC 7d minus PUR 7d
  - name: "Hot-Advantage+-Shopping"
    budget: $150/day  (CBO)
    bid: Min ROAS 2.5x
    catalog: shopify-feed-2026
```

### Structure B — Scaling DTC, $10K/day

```yaml
campaigns:
  - name: "Cold-CBO-Tier1"
    budget: $5K/day
    bid: Lowest Cost
    adsets: [LAL-1%, LAL-2%, LAL-3%, LAL-5%, AdvantagePlus]
  - name: "Cold-ABO-Tests"
    budget: $1K/day  (ABO, $200/cell)
    adsets: 5 cells testing new creative concepts
  - name: "Warm-CBO"
    budget: $2K/day
  - name: "Hot-Advantage+"
    budget: $1.5K/day
  - name: "Customer-Retention-CBO"
    budget: $500/day
    seed: top 25% LTV customer list
```

### Structure C — B2B lead-gen, $300/day

```yaml
campaigns:
  - name: "Cold-Awareness-CBO"
    objective: OUTCOME_AWARENESS
    budget: $100/day
  - name: "Cold-Lead-CBO"
    objective: OUTCOME_LEADS
    budget: $150/day
    bid: Cost Cap $40 per lead
  - name: "Hot-Lead-Retarget"
    objective: OUTCOME_LEADS
    budget: $50/day
    bid: Lowest Cost
```

## Edge cases

### CBO daily_budget vs lifetime_budget
CBO supports both. `daily_budget` simpler. `lifetime_budget` requires `end_time` and prorates within. Use lifetime only for finite promotions (Black Friday, launch week).

### Advantage Campaign Budget rename
Meta renamed CBO to "Advantage Campaign Budget" in Ads Manager UI but the API field remains `is_advantage_campaign_budget`. Old-school CBO docs still apply.

### Minimum daily budget per adset (ABO)
$1 minimum. Recommended $25-50 minimum for any adset hoping to exit learning phase (50 conversions / 7d).

### Learning phase
A new adset (or significant edit) enters Learning. Don't touch for 7d. Significant edits = budget +20% / -20%, creative swap, targeting change, bid strategy change. Avoid mid-learning edits — restart.

### Special ad categories
Housing, employment, credit, social issues — required if applicable:
```bash
--special_ad_categories '["EMPLOYMENT"]'
```
Limits targeting (no detailed demographics, narrower geo). Ad rejection without this set if subject-matter triggers.

### Audience overlap
Use Audience Overlap Tool (Meta Ads Manager → Audiences → Show Audience Overlap). >30% overlap between two adsets in the same CBO campaign = cannibalization. Either merge audiences OR add hard exclusion.

### CBO and ABO can not co-exist in same campaign
You toggle at campaign creation. Can't have CBO at campaign with one ABO adset override. Workaround = split into two campaigns.

### Rate limits
200 calls / hour / ad account default. Bulk endpoints (`POST /act_{id}/campaigns?bulk=true`) consume less. For >100 adset creates, batch.

### Buying type AUCTION vs RESERVED
99% of performance use AUCTION. RESERVED (Reach + Frequency) only for upper-funnel guaranteed-delivery brand work.

## Sources

- Official Meta Ads MCP (29 tools, GA April 2026): https://pasqualepillitteri.it/en/news/1707/official-meta-ads-mcp-claude-29-tools-2026
- Meta Marketing API — Campaigns: https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group
- Meta Marketing API — Ad sets: https://developers.facebook.com/docs/marketing-api/reference/ad-campaign
- CBO (Advantage Campaign Budget): https://www.facebook.com/business/help/258945788433077
- Bid strategies: https://www.facebook.com/business/help/463088240976772
- Learning phase: https://www.facebook.com/business/help/112167992830700
- Audience Overlap Tool: https://www.facebook.com/business/help/516840952922734
