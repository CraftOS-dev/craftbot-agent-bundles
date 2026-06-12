<!--
Source: https://www.smartly.io/blog/creative-testing-framework
Creative testing matrix: creative × audience × offer with z-test significance.
-->
# Creative Testing Matrix Design — SKILL

Creative is 70% of paid performance. The matrix is how you find the winner: **creative concepts × audiences × offers** in a structured grid with per-cell budget + statistical significance criteria. This skill ships the matrix design, the cell sizing, the z-test math, and the platform-specific deployment (Meta ABO + Dynamic Creative; Google RSA + PMax asset group; TikTok creative array).

## When to use this skill

- **New account ramp** — first 60 days, every $ goes to testing.
- **Creative refresh** — winning creative is fatiguing; need fresh contenders.
- **Offer test** — discount % vs free shipping vs bundle.
- **Hook concept hunt** — 5+ hook variants competing for one slot.
- **Audience hypothesis test** — does LAL-1% beat Interest Stack at same CPA?
- **Format test** — video vs carousel vs single image.

**Do NOT use this skill when:**
- Spend <$3K/month — cells too small for significance; iterate manually.
- Single creative on hand — write briefs first via `creative-brief-authoring-for-designers`.
- Pure brand awareness (CTR < $/conversion) — different KPI math.

## Setup

### Matrix anatomy

- **Cells** = creative × audience × offer combinations.
- **Per-cell budget** = `~100 conversions / target_CPA / test_days`. Typical: $25-50/day per cell at $50 target CPA.
- **Test duration**: 7-14 days minimum for daily seasonality wash.
- **Significance threshold**: p < 0.05 (z = 1.96) for CTR / CVR. CPA needs ~100 conversions per cell for 90% power on 15% delta.

### Significance math — z-test for CTR

```
p1 = clicks_A / impressions_A
p2 = clicks_B / impressions_B
p_pool = (clicks_A + clicks_B) / (impressions_A + impressions_B)

z = (p1 - p2) / sqrt(p_pool * (1 - p_pool) * (1/n_A + 1/n_B))

Reject H0 (no difference) if |z| > 1.96 (p < 0.05)
```

Python helper:
```python
from statsmodels.stats.proportion import proportions_ztest
counts = [clicks_A, clicks_B]
nobs = [impressions_A, impressions_B]
stat, pval = proportions_ztest(counts, nobs, alternative='two-sided')
# pval < 0.05 = significant
```

### Mode selection

| Mode | When | Pros | Cons |
|---|---|---|---|
| **Meta Advantage+ Dynamic Creative** | Fast concept hunt | Quick reads, Meta optimizes | Confounds hook + offer + format |
| **Meta ABO split (1 cell per adset)** | Winner confirmation | Clean per-cell reads | Slow, more budget per cell |
| **Google RSA** | Search copy variants | Auto rotation | Asset Strength bias |
| **Google PMax asset group** | Visual + headline mix | Cross-network | Reporting per-asset weak |
| **TikTok ad array in 1 adgroup** | TikTok native | Fast iteration | TikTok optimizes — not clean |

## Common recipes

### Recipe 1: Build the matrix in xlsx

```python
import openpyxl
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Creative Matrix"

# Headers
ws.append(["Cell #","Hook","Audience","Offer","Format","Ratio","Budget/day",
           "Target imps","Spend","Imps","Clicks","CTR","Convs","CPA","Z vs control","Sig?"])

# 30-cell matrix: 5 hooks × 3 audiences × 2 offers
hooks = ["Problem-aware Q","Founder UGC","Testimonial montage","Result-driven","Price anchor"]
audiences = ["LAL-1%","Interest Stack","Advantage+"]
offers = ["20% off","Free shipping"]

cell = 1
for h in hooks:
  for a in audiences:
    for o in offers:
      ws.append([f"C{cell}", h, a, o, "Video","9:16",50, 10000, 0,0,0,0,0,0,0,"TBD"])
      cell += 1

wb.save("creative-matrix-Q3.xlsx")
```

### Recipe 2: Deploy ABO matrix on Meta — 30 adsets

```bash
# Campaign (ABO — no campaign budget)
campaign_id=$(mcp tool meta-ads.create_campaign \
  --name "Creative-Matrix-Q3-ABO" \
  --objective "OUTCOME_SALES" \
  --is_advantage_campaign_budget false)

# 30 adsets, one per cell
for cell in $(seq 1 30); do
  audience=$(yq ".cells[$((cell-1))].audience" matrix.yaml)
  offer=$(yq ".cells[$((cell-1))].offer" matrix.yaml)
  
  adset_id=$(mcp tool meta-ads.create_adset \
    --campaign_id "$campaign_id" \
    --name "Cell-$cell-$audience-$offer" \
    --daily_budget 5000 \
    --optimization_goal "OFFSITE_CONVERSIONS" \
    --billing_event "IMPRESSIONS" \
    --targeting "$(jq ".cells[$((cell-1))].targeting" matrix.json)")
  
  # 1 creative per cell
  mcp tool meta-ads.create_ad \
    --adset_id "$adset_id" \
    --name "Ad-Cell-$cell" \
    --creative_id "$(yq ".cells[$((cell-1))].creative_id" matrix.yaml)"
done
```

### Recipe 3: Meta Dynamic Creative — fast hook hunt

```bash
mcp tool meta-ads.create_ad \
  --adset_id "$ADSET_ID" \
  --name "DynCreative-HookHunt-V1" \
  --dynamic_creative_spec '{
    "videos": [{"video_id":"<v1>"},{"video_id":"<v2>"},{"video_id":"<v3>"},{"video_id":"<v4>"},{"video_id":"<v5>"}],
    "bodies": [{"text":"Hook A primary text"},{"text":"Hook B primary text"},{"text":"Hook C"}],
    "titles": [{"text":"Headline V1"},{"text":"Headline V2"}],
    "call_to_actions": [{"type":"SHOP_NOW"}]
  }'
```

### Recipe 4: Google RSA — 15 headlines + 4 descriptions

```bash
mcp tool google-ads.create_responsive_search_ad \
  --ad_group_id "$AG_ID" \
  --final_urls '["https://brand.com/lp"]' \
  --headlines "$(jq '.headlines' headlines-15.json)" \
  --descriptions "$(jq '.descriptions' descriptions-4.json)" \
  --path1 "test" --path2 "v2"
```

### Recipe 5: Read results — per-cell aggregate

```bash
# Pull adset-level insights for all matrix adsets
mcp tool meta-ads.get_campaign_insights \
  --campaign_id "$campaign_id" \
  --level "adset" \
  --breakdowns '[]' \
  --metrics '["spend","impressions","clicks","ctr","conversions","cost_per_conversion"]' \
  --date_preset "last_14d" > matrix-results.json

# Update xlsx with results, compute z-test vs control
python -c "
import json, openpyxl, math
from statsmodels.stats.proportion import proportions_ztest

with open('matrix-results.json') as f:
    results = json.load(f)['data']
wb = openpyxl.load_workbook('creative-matrix-Q3.xlsx')
ws = wb.active

control = next(r for r in results if r['adset_name'].endswith('Cell-1'))
ctrl_imps, ctrl_clicks = int(control['impressions']), int(control['clicks'])

for i, r in enumerate(results, start=2):
    imps, clicks = int(r['impressions']), int(r['clicks'])
    ws.cell(row=i+1, column=10, value=imps)
    ws.cell(row=i+1, column=11, value=clicks)
    ws.cell(row=i+1, column=12, value=clicks/imps if imps else 0)
    if i > 2:
        stat, pval = proportions_ztest([clicks, ctrl_clicks], [imps, ctrl_imps])
        ws.cell(row=i+1, column=15, value=round(stat,2))
        ws.cell(row=i+1, column=16, value='YES' if pval < 0.05 else 'NO')
wb.save('creative-matrix-Q3.xlsx')
"
```

### Recipe 6: Cell sizing calculator

```python
# Power analysis: given baseline CTR + minimum detectable effect + alpha + power → impressions per cell
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

baseline_ctr = 0.015   # 1.5%
mde = 0.0025           # detect +0.25% absolute
alpha = 0.05
power = 0.90

es = proportion_effectsize(baseline_ctr + mde, baseline_ctr)
analysis = NormalIndPower()
n_per_cell = analysis.solve_power(effect_size=es, alpha=alpha, power=power, alternative='two-sided')
print(f"{int(n_per_cell):,} impressions per cell")
# ≈ 25,500 impressions per cell for this scenario
```

### Recipe 7: Winner promotion — duplicate top cell into scaling campaign

```bash
# After significance, clone winning adset into a CBO scaling campaign
mcp tool meta-ads.duplicate_adset \
  --adset_id "$WINNER_ADSET" \
  --rename "Winner-Cell-$N-Scaled-CBO" \
  --new_campaign_id "$SCALING_CAMPAIGN_CBO"
```

## Examples — 30-cell matrix (DTC skincare)

```yaml
matrix:
  hooks:
    - H1: "Problem-aware: Tired of breakouts that won't quit?"
    - H2: "Founder UGC: I built this when my dermatologist gave up on me"
    - H3: "Testimonial montage: 30 customers, 30 transformations"
    - H4: "Result-driven: 87% saw clearer skin in 14 days"
    - H5: "Price anchor: $19 routine that replaced my $200 stack"
  
  audiences:
    - A1: LAL-1% Top25LTV
    - A2: Interest Stack (skincare + dermatology + acne products)
    - A3: Advantage+ Audience (broad)
  
  offers:
    - O1: "20% off first order"
    - O2: "Free shipping + free returns"
  
  cell_budget: $50/day
  test_days: 14
  control: C1 (H1×A1×O1)
  success_criterion: CPA ≤ $30 AND z >1.96 vs control on CTR

predicted_outcome:
  if winner_hook_concentrates: scale top hook across all audiences + offers
  if winner_audience_concentrates: scale audience with all hooks
  if no_significance: extend test 7d; if still no, kill matrix concept
```

## Edge cases

### Sample size minimum
30 conversions per cell = noise. 100 conversions per cell = ~90% power for 15% delta. Don't declare winners at <50.

### Confounded variables
If both hook AND offer differ, you can't isolate. Either fix offer and rotate hooks (1 dimension), or use full matrix with enough cells.

### Meta optimization within adset
If multiple ads in one adset, Meta's optimization picks. You CAN'T use that for clean reads — only across adsets (ABO splits).

### CTR vs CPA significance
CTR pure-engagement signal: needs 10K impressions per cell. CPA needs 100 conversions. CPA is what matters but CTR is faster — use CTR for kill decisions, CPA for winner declaration.

### Frequency effect
Cells running 14d at $50/day on small audience hit frequency 2.5+. Frequency confounds CTR (declines naturally). Pause at frequency 3 or expand audience.

### Multi-armed bandit alternative
Instead of static matrix → Thompson Sampling rotation. Tools: Optimizely, GrowthBook (`growthbook-experiments` skill). Trade: faster winner, less clean per-cell read.

### Statistical correction for multiple comparisons
30 cells = 30 simultaneous tests. False positive rate inflates. Use Bonferroni correction (alpha / N) OR Benjamini-Hochberg FDR. Conservative for small matrices.

### Creative quality variance
A single brilliant cell can confound a single-dimension test. Run 2-3 creative variants per concept to wash out execution variance.

### Pre-launch QA
Every cell creative must pass: brand voice (Vale), policy (Meta `validate_creative`), pixel firing (test event in staging).

### Confidence interval reporting
Don't report just point estimates. Always report CI: `CPA = $32 [$25-$40]` is honest. Hides if interval overlaps control.

## Sources

- Smartly creative testing framework: https://www.smartly.io/blog/creative-testing-framework
- Meta Dynamic Creative: https://www.facebook.com/business/help/170469011742507
- Google RSA best practices: https://support.google.com/google-ads/answer/7684791
- statsmodels proportions z-test: https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportions_ztest.html
- Power analysis: https://www.statsmodels.org/stable/generated/statsmodels.stats.power.NormalIndPower.solve_power.html
- Bonferroni correction: https://en.wikipedia.org/wiki/Bonferroni_correction
- Benjamini-Hochberg FDR: https://en.wikipedia.org/wiki/False_discovery_rate
