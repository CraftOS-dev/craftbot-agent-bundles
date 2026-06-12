<!--
Source: https://developers.highspot.com/ + https://developer.showpad.com/ + https://developer.seismic.com/
Sales enablement infrastructure — Highspot + Showpad + Seismic (June 2026 SOTA).
-->
# Sales Enablement Infrastructure — Highspot + Showpad + Seismic — SKILL

Centralized content library + tracking + sales-play playbooks. **Highspot** leads market share. **Showpad** + **Seismic** close behind. Tag-driven content surfacing per deal stage. Per-AE content consumption analytics. Tag taxonomy + orphan content quarantine.

## When to use

- **Roll out a new battlecard / case study** — push to Highspot/Showpad with proper tags.
- **Tag taxonomy maintenance** — keep stage / persona / industry / format consistent.
- **Orphan content quarantine** — find + archive 0-view content.
- **Per-AE consumption report** — who read what + share rate to prospects.
- **Content effectiveness analytics** — content-to-win correlation.
- **Trigger phrases**: "Highspot upload", "tag taxonomy", "Showpad content", "Seismic LiveDoc", "orphan content", "content analytics".

Do NOT use this skill for: **battlecard authoring** (use parent sales-agent `sales-enablement-battlecards-roi-calculators`); **training/LMS** (use `ramp-to-quota-analysis` Mindtickle/Lessonly); **win/loss tagging** (use `win-loss-reporting-at-scale`).

## Setup

```bash
# Highspot — API token (Settings → Developer → API Tokens)
export HIGHSPOT_TOKEN="<token>"
export HIGHSPOT_BASE="https://api.highspot.com/v0.5"

# Showpad — OAuth (Settings → Developer)
export SHOWPAD_TOKEN="<token>"
export SHOWPAD_BASE="https://api.showpad.biz/v3"

# Seismic — API key (Settings → Apps → API)
export SEISMIC_TOKEN="<token>"
export SEISMIC_BASE="https://api.seismic.com/v2"

# Or via api-gateway
export MATON_API_KEY="<key>"
```

Required:
- Highspot: enterprise plan with API access (~$70-100/seat/mo)
- Showpad: subscription (~$80-110/seat/mo)
- Seismic: enterprise (~$1K/seat/yr)

## Common recipes

### Recipe 1: Tag taxonomy (canonical)

```yaml
stage:
  - Prospecting
  - Discovery
  - Evaluation
  - Proposal
  - Negotiation
  - Closed-Won
  - Renewal

persona:
  - CEO
  - CFO
  - VP_Sales
  - VP_Marketing
  - VP_Engineering
  - VP_CustomerSuccess
  - Director_Ops
  - Manager
  - Individual_Contributor

industry:
  - SaaS
  - FinTech
  - HealthTech
  - Retail
  - Manufacturing
  - Government
  - Education

competitor:
  - CompetitorA
  - CompetitorB
  - DIY_inhouse_build

format:
  - Battlecard
  - Case_study
  - Demo_recording
  - Email_template
  - Slide_deck
  - One_pager
  - ROI_calculator
  - Whitepaper

intent:
  - Prospecting_outreach
  - Discovery_questions
  - Demo_setup
  - Objection_handling
  - Pricing_discussion
  - Champion_enablement
```

Store as notion canonical reference. Every content upload must include ≥ 1 tag per: stage, persona, format.

### Recipe 2: Highspot — upload content

```bash
# 1. Create item
curl -X POST "$HIGHSPOT_BASE/items" \
  -H "Authorization: Bearer $HIGHSPOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Acme Corp Case Study — $5M ARR Win",
    "description": "Manufacturing case study; CFO-targeted; champion enablement",
    "spot_id": "spot_case_studies",
    "properties": {
      "stage": "Evaluation",
      "persona": "CFO",
      "industry": "Manufacturing",
      "format": "Case_study",
      "intent": "Champion_enablement"
    }
  }'
# Returns item_id

# 2. Upload file content
curl -X POST "$HIGHSPOT_BASE/items/<item_id>/content" \
  -H "Authorization: Bearer $HIGHSPOT_TOKEN" \
  -F "file=@acme_case_study.pdf"

# 3. Publish (move from draft to active)
curl -X POST "$HIGHSPOT_BASE/items/<item_id>/publish" \
  -H "Authorization: Bearer $HIGHSPOT_TOKEN"
```

### Recipe 3: Highspot — list items by tag

```bash
curl "$HIGHSPOT_BASE/items?stage=Evaluation&persona=CFO&format=Case_study&limit=50" \
  -H "Authorization: Bearer $HIGHSPOT_TOKEN" \
  | jq '.results[] | {id, title, views_total, share_count, last_modified}'
```

### Recipe 4: Showpad — upload asset

```bash
curl -X POST "$SHOWPAD_BASE/assets" \
  -H "Authorization: Bearer $SHOWPAD_TOKEN" \
  -H "Content-Type: multipart/form-data" \
  -F "title=Discovery Question Bank — Enterprise" \
  -F "description=MEDDIC + SPIN questions for Eval stage" \
  -F "tags=[\"Discovery\",\"Battlecard\",\"Enterprise\"]" \
  -F "file=@discovery_questions.pdf"
```

### Recipe 5: Seismic — upload LiveDoc + tags

```bash
curl -X POST "$SEISMIC_BASE/contents" \
  -H "Authorization: Bearer $SEISMIC_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ROI Calculator — SaaS Mid-Market",
    "type": "LiveDoc",
    "library_id": "lib_xyz789",
    "tags": ["ROI_calculator","Mid-Market","SaaS"],
    "properties": {"stage": "Evaluation", "persona": "VP_Sales"}
  }'
```

### Recipe 6: Orphan content scan (0 views > 90 days)

```python
import requests, os
from datetime import datetime, timedelta

token = os.environ["HIGHSPOT_TOKEN"]
cutoff = datetime.now() - timedelta(days=90)

# Pull all items + view stats
r = requests.get(f"{os.environ['HIGHSPOT_BASE']}/items",
                 params={"limit": 500},
                 headers={"Authorization": f"Bearer {token}"}).json()

orphans = []
for item in r["results"]:
    views = item.get("views_total", 0)
    created = datetime.fromisoformat(item["created_at"].replace("Z","+00:00"))
    if views == 0 and created < cutoff.replace(tzinfo=created.tzinfo):
        orphans.append({"id": item["id"], "title": item["title"], "created": item["created_at"]})

print(f"Orphan content (0 views, > 90d old): {len(orphans)}")
for o in orphans[:20]:
    print(f"- {o['title']} (created {o['created']})")
```

### Recipe 7: Quarantine orphan content (Highspot)

```bash
# Move to "Quarantine" spot for review; don't auto-delete
curl -X PATCH "$HIGHSPOT_BASE/items/<item_id>" \
  -H "Authorization: Bearer $HIGHSPOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"spot_id": "spot_quarantine", "status": "review_required"}'

# After 30 more days in quarantine + no view: archive
curl -X POST "$HIGHSPOT_BASE/items/<item_id>/archive" \
  -H "Authorization: Bearer $HIGHSPOT_TOKEN"
```

### Recipe 8: Per-AE consumption report

```bash
# Highspot analytics — per user
curl "$HIGHSPOT_BASE/analytics/users/<user_id>/activity?from=2026-04-01&to=2026-06-30" \
  -H "Authorization: Bearer $HIGHSPOT_TOKEN" \
  | jq '{user: .user_id,
         items_viewed: .total_views,
         unique_items: .unique_items_viewed,
         shares_to_prospects: .external_share_count,
         top_5_content: (.top_items[:5] | map({title, views}))}'
```

### Recipe 9: Content-to-win correlation analysis

```python
# Cross-reference: which content was shared on closed-won deals vs closed-lost
import pandas as pd
import requests, os

# Pull Highspot shares with deal_id metadata
shares = requests.get(f"{os.environ['HIGHSPOT_BASE']}/analytics/shares",
                      params={"from": "2026-01-01", "to": "2026-06-30"},
                      headers={"Authorization": f"Bearer {os.environ['HIGHSPOT_TOKEN']}"}).json()
shares_df = pd.json_normalize(shares["results"])

# Pull deal outcomes from CRM
import requests
q = "SELECT Id, IsWon, IsClosed FROM Opportunity WHERE IsClosed = TRUE AND CloseDate >= 2026-01-01"
deals = requests.get(f"https://gateway.maton.ai/salesforce/services/data/v60.0/query",
                     params={"q": q},
                     headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"}).json()
deals_df = pd.DataFrame(deals["records"])

merged = shares_df.merge(deals_df, left_on='deal_id', right_on='Id', how='inner')

# Per-item win rate
analytics = merged.groupby(['item_id','item_title']).agg(
    shares=('Id','count'),
    wins=('IsWon', 'sum')
).reset_index()
analytics['win_rate'] = analytics['wins'] / analytics['shares']
analytics = analytics.sort_values('win_rate', ascending=False)
print(analytics.head(20))  # top correlated content
```

### Recipe 10: Bulk tag update (Highspot)

```python
import requests, os

# Update tags on multiple items (e.g., persona reclassification)
items_to_retag = ["item_111","item_222","item_333"]

for item_id in items_to_retag:
    requests.patch(f"{os.environ['HIGHSPOT_BASE']}/items/{item_id}",
                   headers={"Authorization": f"Bearer {os.environ['HIGHSPOT_TOKEN']}"},
                   json={"properties": {"persona": "VP_Sales", "industry": "FinTech"}})
```

### Recipe 11: Seismic LiveDoc auto-personalization

```bash
# LiveDoc with dynamic fields (account name, deal context)
curl -X POST "$SEISMIC_BASE/contents/<livedoc_id>/personalize" \
  -H "Authorization: Bearer $SEISMIC_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "context": {
      "account_name": "Acme Corp",
      "deal_value": "$250K",
      "champion_name": "Sarah Patel",
      "competitor": "CompetitorA"
    }
  }'
# Returns personalized PDF URL
```

### Recipe 12: Showpad weekly digest to AE pod

```python
# Friday: per-AE pod, top 5 content + their consumption stats
import requests, os
from datetime import datetime, timedelta

token = os.environ["SHOWPAD_TOKEN"]
ae_pod_users = ["alice@co.com","bob@co.com","carol@co.com"]
week_start = (datetime.now() - timedelta(days=7)).isoformat()

for ae in ae_pod_users:
    r = requests.get(f"{os.environ['SHOWPAD_BASE']}/users/{ae}/analytics",
                     params={"from": week_start},
                     headers={"Authorization": f"Bearer {token}"}).json()
    # Slack DM each AE their weekly recap
    print(f"{ae}: {r.get('items_viewed_count',0)} items viewed, {r.get('shares_external',0)} shares")
```

## Examples

### Example 1: New battlecard rollout

**Goal:** Sales enablement built a competitor battlecard; need to deploy to Highspot.

**Steps:**
1. Build PDF + accompanying SOC2 talking points.
2. Recipe 2 — upload + tag (stage=Evaluation, persona=Director_Ops, format=Battlecard, competitor=CompetitorA, intent=Objection_handling).
3. Add to Recommended Plays for Evaluation stage.
4. Notify AE pod via Slack with link.
5. Track usage via Recipe 8 weekly.
6. After 30 days: Recipe 9 — did battlecard correlate to wins?

**Result:** Battlecard surfaced in deal context; usage tracked; iteration data.

### Example 2: Quarterly content audit (orphan quarantine)

**Goal:** Cull stale + unused content; keep library lean.

**Steps:**
1. Recipe 6 — scan all content for 0 views in 90+ days.
2. Identify ~150 orphan items.
3. Review with enablement: which still relevant?
4. Recipe 7 — quarantine spot for 30 days.
5. After 30 days: any still 0 view → archive permanently.
6. Document tagging pattern (which tags led to invisibility?).

**Result:** Content library down 30%; reps find what they need faster.

### Example 3: Tag taxonomy migration

**Goal:** Reorganize persona tags — separate VP_CS from VP_Marketing (was conflated).

**Steps:**
1. Recipe 3 — list all items currently tagged persona=VP_Marketing.
2. Review each: actually VP_CS? Or actually VP_Marketing?
3. Recipe 10 — batch retag the misclassified.
4. Update tag taxonomy canonical (notion).
5. Communicate to enablement team for future uploads.

**Result:** Search by persona returns the right content for the right buyer.

## Edge cases / gotchas

- **Tag governance is the whole game** — without it, search fails, content goes unused.
- **Highspot "Spot" vs item taxonomy** — Spot is a content collection (e.g., "Battlecards"); item lives in a Spot. Don't conflate.
- **Showpad "Channels" concept** — content surfaced to specific personas/regions; channel rules vs tag-search differ.
- **Seismic LiveDocs vs static PDF** — LiveDoc dynamically personalizes; PDF static. Use LiveDoc for ROI calculators, account-specific plans.
- **API rate limits** — Highspot: 100 req/min. Showpad: 1000/hr. Seismic: low (consult).
- **External sharing tracking** — Highspot Smart Pages track external opens; Showpad Visit Reports same. Use for buyer signal.
- **Search relevance tuning** — Highspot uses term frequency + recency + popularity. Bury old content via Recipe 7 to surface new.
- **Multi-language content** — tag locale per item; default search filters by user locale.
- **Versioning** — Highspot supports v1, v2 of same content; bury old version.
- **Quarantine isn't deletion** — items recoverable for 90d after archive in Highspot. Don't lose institutional knowledge.
- **CRM-integration share tracking** — Highspot's Salesforce package writes share events to Activity History; verify install.
- **GDPR + external shares** — recipient tracking requires consent banner.
- **Seismic pricing tier matters** — base plan lacks LiveDoc; need higher tier.
- **Content effectiveness correlation isn't causation** — Recipe 9 win rates can be spurious (e.g., AE who shares this also closes more).
- **Permissions per Spot** — restrict Spots to certain AE pods (e.g., enterprise-only).
- **Mobile rendering** — battlecards designed for desktop look bad on mobile; preview before publish.

## Sources

- [Highspot Developer docs](https://developers.highspot.com/)
- [Highspot Items + Spots API](https://developers.highspot.com/docs/items)
- [Highspot Analytics API](https://developers.highspot.com/docs/analytics)
- [Showpad Developer docs](https://developer.showpad.com/)
- [Showpad API reference](https://developer.showpad.com/api)
- [Seismic Developer Portal](https://developer.seismic.com/)
- [Seismic LiveDoc Guide](https://developer.seismic.com/docs/livedoc)
- [Sales enablement content benchmarks (Highspot 2026)](https://www.highspot.com/research/state-of-sales-enablement/)
- [Tag taxonomy best practices (G2 enablement)](https://www.g2.com/articles/sales-enablement-content)
