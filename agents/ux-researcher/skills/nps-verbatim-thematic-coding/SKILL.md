<!--
Sources:
NN/g — NPS — https://www.nngroup.com/articles/nps-net-promoter-score/
Sprig API — https://help.sprig.com/hc/en-us/articles/sprig-api
Dovetail v3 API — https://dovetail.com/help/api
Hugging Face — embedding clustering — https://huggingface.co/blog/text-clustering
-->
# NPS Verbatim Thematic Coding — SKILL

Pull NPS comments from Sprig / SurveyMonkey / Typeform / Delighted, cluster into themes via Dovetail tagging OR embedding-based clustering (Hugging Face) for high-volume. Per-segment promoter / passive / detractor themes drive the action plan.

## When to use

- Quarterly NPS pulse analysis.
- Detractor churn risk diagnosis.
- Promoter advocacy driver identification.
- Multi-segment NPS comparison (paid vs free, new vs existing).
- High-volume verbatim coding (1000+ comments).

Trigger phrases: "code NPS verbatims", "analyze NPS comments", "promoter / detractor themes", "what's driving the NPS score", "NPS dashboard themes".

## Setup

```bash
# Sprig (NPS survey)
curl -fsSL "https://api.sprig.com/v1/me" \
  -H "Authorization: Bearer $SPRIG_API_KEY"

# Survicate (multi-channel survey)
curl -fsSL "https://data-api.survicate.com/v1/me" \
  -H "Authorization: Bearer $SURVICATE_API_KEY"

# Dovetail (synthesis)
curl -fsSL "https://dovetail.com/api/v1/me" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN"

# Hugging Face MCP (clustering for high volume)
# huggingface-mcp in CraftBot catalog
```

## Common recipes

### Recipe 1: NPS basics (score calculation)

```python
def nps_score(responses):
    """
    NPS = % promoters (9-10) - % detractors (0-6)
    Range: -100 to +100
    """
    n = len(responses)
    promoters = sum(1 for r in responses if r["score"] >= 9)
    detractors = sum(1 for r in responses if r["score"] <= 6)
    return ((promoters - detractors) / n) * 100

def nps_segment(score):
    if score >= 9: return "promoter"
    if score >= 7: return "passive"
    return "detractor"

# Benchmarks (B2B SaaS, 2026)
# >40 = good
# >60 = great
# >70 = world-class
```

### Recipe 2: Pull NPS comments from Sprig

```bash
SURVEY_ID="<sprig-nps-survey-id>"

curl -fsSL "https://api.sprig.com/v1/surveys/$SURVEY_ID/responses?limit=1000" \
  -H "Authorization: Bearer $SPRIG_API_KEY" \
| jq '[.responses[] | {
    user_id,
    score: .answers["nps-score"],
    comment: .answers["nps-comment"],
    segment: (if .answers["nps-score"] >= 9 then "promoter"
              elif .answers["nps-score"] >= 7 then "passive"
              else "detractor" end),
    timestamp,
    user_plan: .user_properties.plan
  }]' \
> nps-responses.json
```

### Recipe 3: Pull NPS from Typeform

```bash
curl -fsSL "https://api.typeform.com/forms/$FORM_ID/responses?page_size=1000" \
  -H "Authorization: Bearer $TYPEFORM_API_TOKEN" \
| jq '[.items[] | {
    response_id,
    score: (.answers[] | select(.field.ref=="nps-score") | .number),
    comment: (.answers[] | select(.field.ref=="nps-why") | .text),
    submitted_at
  }]'
```

### Recipe 4: Pull NPS from Survicate

```bash
curl -fsSL "https://data-api.survicate.com/v1/surveys/$SURVEY_ID/responses" \
  -H "Authorization: Bearer $SURVICATE_API_KEY" \
| jq '[.responses[] | {response_id, answers}]'
```

### Recipe 5: Upload comments to Dovetail for tagging

```bash
# Per-comment upload as Dovetail note
while read -r ROW; do
  USER_ID=$(echo "$ROW" | jq -r '.user_id')
  SEGMENT=$(echo "$ROW" | jq -r '.segment')
  COMMENT=$(echo "$ROW" | jq -r '.comment')

  curl -X POST "https://dovetail.com/api/v1/projects/$DOVETAIL_PROJECT/notes" \
    -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
    -d "{
      \"title\": \"$USER_ID — $SEGMENT\",
      \"body\": \"$COMMENT\",
      \"tags\": [\"$SEGMENT\", \"q3-nps\"]
    }"
done < <(jq -c '.[]' nps-responses.json)
```

### Recipe 6: Embedding-based clustering for high volume (1000+ comments)

```python
# Use Hugging Face sentence-transformers + UMAP + HDBSCAN
import requests
import numpy as np
from sklearn.cluster import HDBSCAN
import umap

# 1. Get embeddings via HF inference API
def embed(texts, hf_token, model="sentence-transformers/all-MiniLM-L6-v2"):
    r = requests.post(
        f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model}",
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": texts}
    )
    return np.array(r.json())

# 2. Reduce dimensions
embeddings = embed([r["comment"] for r in nps_responses], hf_token)
reduced = umap.UMAP(n_components=10, metric="cosine").fit_transform(embeddings)

# 3. Cluster
clustering = HDBSCAN(min_cluster_size=10, metric="euclidean").fit(reduced)
labels = clustering.labels_

# 4. Per-cluster sample 5 representative comments
for cluster_id in set(labels):
    if cluster_id == -1: continue  # noise
    members = [nps_responses[i] for i, l in enumerate(labels) if l == cluster_id]
    print(f"Cluster {cluster_id}: {len(members)} comments")
    for m in members[:5]:
        print(f"  - [{m['segment']}] {m['comment'][:100]}")
```

### Recipe 7: Tag taxonomy for NPS

```markdown
# Suggested NPS tag taxonomy

## Driver tags (top-level — why they gave the score)
- driver/product-value
- driver/support-quality
- driver/pricing-fit
- driver/ease-of-use
- driver/feature-gap
- driver/reliability
- driver/onboarding

## Sub-driver tags
- driver/feature-gap/missing-integration
- driver/feature-gap/missing-export
- driver/pricing-fit/too-expensive
- driver/pricing-fit/value-for-money

## Segment tags (cross-reference)
- segment/promoter
- segment/passive
- segment/detractor

## Plan tags
- plan/free
- plan/pro
- plan/enterprise
```

### Recipe 8: Per-segment theme report

```markdown
# NPS Verbatim Coding: Q3 2026

**N=347 responses · Score: 42 (good for B2B SaaS)**
**Segments:** 132 promoters · 87 passives · 128 detractors

## TL;DR
- Promoters love: speed + UI + Slack integration
- Detractors blocked by: pricing perceived too high; missing features in [X]
- Top action: ship [feature gap] → addresses 30% of detractor mentions

## Promoter themes (132 promoters)

### Theme 1: Speed (mentioned 67%)
- "Loads instantly compared to [competitor]."
- "I can be in and out in 30 seconds."
**Driver:** ease-of-use / performance

### Theme 2: Slack integration (mentioned 41%)
- "Killed our standup; Slack updates handle it."
- "Best Slack integration I've seen."
**Driver:** product-value

## Passive themes (87 passives)

### Theme 1: Works but unremarkable (mentioned 52%)
- "Does what I need."
- "Good enough."

## Detractor themes (128 detractors)

### Theme 1: Pricing (mentioned 38%)
- "Pro tier is overpriced for what you get."
- "Started cheap, became expensive."
**Driver:** pricing-fit/too-expensive
**Recommendation:** consider segmented pricing tier

### Theme 2: Missing CSV import (mentioned 22%)
- "Can't bulk import; deal-breaker for migration."
**Driver:** feature-gap/missing-export
**Recommendation:** ship CSV import in next sprint
```

### Recipe 9: NPS dashboard — Notion table

```markdown
# NPS dashboard (live, updated quarterly)

| Quarter | Score | Promoters | Passives | Detractors | Top promoter theme | Top detractor theme |
|---|---|---|---|---|---|---|
| Q1 2026 | 38 | 30% | 28% | 22% | Speed | Pricing |
| Q2 2026 | 40 | 32% | 27% | 21% | Speed | Pricing |
| Q3 2026 | 42 | 38% | 25% | 21% | Speed | Pricing |

## Trend annotations
- Q3: Speed mention rate up 6pts after caching release
- Q3: Pricing theme persistent across 3 quarters — needs business decision
```

### Recipe 10: Action ownership matrix

```markdown
# Action plan from NPS findings

| Theme | Segment | % mentions | Action | Owner | ETA |
|---|---|---|---|---|---|
| Pricing perceived high | Detractors | 38% | Segmented pricing review | PM + finance | Q4 |
| CSV import missing | Detractors | 22% | Ship CSV import | Eng | Sprint 14 |
| Speed (love it) | Promoters | 67% | Keep investing in perf | Eng | Ongoing |
| Slack integration | Promoters | 41% | Marketing case study | Marketing | Q4 |
| Support response time | Passives | 35% | SLA review | Support lead | Q4 |
```

## Examples

### Example 1: Quarterly NPS analysis
**Goal:** Theme NPS comments for executive readout.

**Steps:**
1. Pull comments from Sprig (Recipe 2) — 347 responses.
2. Tag via Dovetail with taxonomy (Recipe 5, 7).
3. Per-segment cluster (Recipe 8).
4. Report (Recipes 8-9).
5. Action ownership (Recipe 10).

**Result:** Defensible action plan tied to NPS movement.

### Example 2: High-volume coding (5000 comments)
**Goal:** Code 5000 quarterly NPS comments.

**Steps:**
1. Pull from Survicate / Sprig combined.
2. Embedding cluster (Recipe 6) → 12 candidate clusters.
3. Human-review cluster labels; merge / split as needed.
4. Push final tags to Dovetail.
5. Per-segment report (Recipe 8).

**Result:** Scalable thematic analysis without manual tagging.

## Edge cases / gotchas

- **NPS without comments.** Useless — score alone tells you nothing. Always pair with verbatim.
- **Combining segments in same report.** Promoter + detractor themes have different actions. Always per-segment.
- **Single theme dominates.** "Pricing" mentioned by 38% doesn't mean fix pricing — investigate sub-themes.
- **Score change without verbatim shift.** May be measurement artifact (timing, sample). Always check.
- **Low response rate.** <5% → biased sample. Re-target intercept timing.
- **Survey on every page.** Annoys; drops response rate over time.
- **NPS in onboarding.** Too early — score is anchored to hope, not experience.
- **Embedding clusters as final answer.** Always human-review. Embeddings catch surface similarity, not semantic.
- **Tag taxonomy explosion.** >15 tags = noise. Cluster + collapse.
- **Per-quarter compare with sample drift.** Filter by same segment when comparing scores.
- **Detractor themes without action.** Becomes vanity. Pair every theme with action + owner.

## Sources

- [NN/g — Net Promoter Score: Lacking Context](https://www.nngroup.com/articles/nps-net-promoter-score/)
- [Sprig API](https://help.sprig.com/hc/en-us/articles/sprig-api)
- [Survicate API](https://survicate.com/api)
- [Typeform API](https://www.typeform.com/developers/create)
- [Dovetail v3 API](https://dovetail.com/help/api)
- [Hugging Face — text clustering](https://huggingface.co/blog/text-clustering)
- [sentence-transformers](https://www.sbert.net/)
- [HDBSCAN](https://hdbscan.readthedocs.io/en/latest/)
- [UMAP](https://umap-learn.readthedocs.io/en/latest/)
