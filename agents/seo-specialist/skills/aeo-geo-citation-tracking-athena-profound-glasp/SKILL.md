<!--
Source: https://athenahq.ai/
Source: https://www.profound.ai/
Source: https://otterly.ai/
Source: https://peec.ai/
Depth: multi-vendor AEO/GEO citation tracking across ChatGPT/Gemini/Claude/Perplexity
-->
# AEO / GEO Citation Tracking — AthenaHQ / Profound / Otterly / Peec

## When to use

Reach for this skill when the user asks for: "AEO citation tracking", "track ChatGPT citations", "Perplexity brand mentions", "AI search visibility", "Gemini citation share", "Claude citation share", "share of voice in AI search", "GEO tracking", "generative engine optimization tracking". This is the dedicated AEO measurement skill — picks ONE vendor (AthenaHQ / Profound / Otterly / Peec) and runs daily polling. AEO and SEO are **different jobs** as of 2026 — measure separately. Citation share can drop while organic clicks hold steady, or vice versa.

## Setup

```bash
# Pick ONE vendor per engagement:

# AthenaHQ — UI leader, $249+/mo
export ATHENA_API_KEY="<from athenahq.ai/settings/api>"

# Profound — public API, custom pricing
export PROFOUND_API_KEY="<from profound.ai/settings>"

# Otterly — EU-focused, $49+/mo (Cologne-based)
export OTTERLY_API_KEY="<from otterly.ai/dashboard/api>"

# Peec.ai — EU alt, $79+/mo
export PEEC_API_KEY="<from peec.ai/settings/api>"

# Goodie — AI-search-only brand monitoring (free tier available)
export GOODIE_API_KEY="<from goodie.ai/dashboard>"

# Surfer GEO — AEO content scoring (different from citation tracking)
# See content-cluster-architecture-marketmuse skill for Surfer setup
```

Auth / pricing summary:
| Tool | Tier | Geography | Surfaces | API |
|---|---|---|---|---|
| AthenaHQ | $249+/mo | Global | ChatGPT, Gemini, Claude, Perplexity, Brave AI, You.com | Yes |
| Profound | Custom | US-focused | ChatGPT, Perplexity, Gemini, Claude | Yes (public) |
| Otterly | $49+/mo | EU | ChatGPT, Perplexity, Gemini, Bing Chat | Yes |
| Peec.ai | $79+/mo | EU | ChatGPT, Perplexity, Gemini, Claude | Yes |
| Goodie | Free + paid | Global | ChatGPT, Perplexity | Limited |

## Common recipes

### Recipe 1: AthenaHQ — track citation share per prompt
```bash
# List tracked prompts
curl https://api.athenahq.ai/v1/prompts \
  -H "Authorization: Bearer $ATHENA_API_KEY"

# Add a tracked prompt
curl -X POST https://api.athenahq.ai/v1/prompts \
  -H "Authorization: Bearer $ATHENA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt":"What is the best marketing automation tool for B2B?",
    "frequency":"daily",
    "surfaces":["chatgpt","gemini","claude","perplexity","brave","you"]
  }'

# Pull citation results
curl "https://api.athenahq.ai/v1/citations?prompt_id=<id>&since=2026-06-01" \
  -H "Authorization: Bearer $ATHENA_API_KEY"
```
Returns per-surface: citations (URLs Athena's LLM clients pulled), brand mention count, share-of-voice vs configured competitors.

### Recipe 2: Profound — citation tracking via API
```bash
curl "https://api.profound.com/v1/brand/citations?brand=Example&surfaces=chatgpt,gemini,claude,perplexity&since=2026-06-01" \
  -H "Authorization: Bearer $PROFOUND_API_KEY"

# Per-prompt drill-down
curl "https://api.profound.com/v1/prompts/<prompt-id>/results?surface=chatgpt&date=2026-06-09" \
  -H "Authorization: Bearer $PROFOUND_API_KEY"
```

### Recipe 3: Otterly EU tracking
```bash
curl "https://api.otterly.ai/v1/brands/<brand-id>/mentions?since=2026-06-01&surfaces=chatgpt,perplexity,gemini" \
  -H "Authorization: Bearer $OTTERLY_API_KEY"
```

### Recipe 4: Peec.ai — alt EU vendor
```bash
curl "https://api.peec.ai/v1/citations?brand=Example&date_range=last_30_days" \
  -H "Authorization: Bearer $PEEC_API_KEY"
```

### Recipe 5: Daily citation share dashboard (vendor-agnostic)
```python
import requests, datetime, pandas as pd

VENDOR = 'athena'  # or 'profound' / 'otterly' / 'peec'
PROMPTS = [
    'What is the best marketing automation tool?',
    'What are the top CRM software options?',
    'Which email marketing platform is best for B2B?',
    # ... 20-50 tracked prompts per cluster
]

def pull_athena_citation(prompt, date):
    r = requests.get(
        'https://api.athenahq.ai/v1/citations',
        params={'prompt': prompt, 'date': date},
        headers={'Authorization': f'Bearer {ATHENA_API_KEY}'}
    )
    return r.json()

today = datetime.date.today()
snapshots = []
for prompt in PROMPTS:
    data = pull_athena_citation(prompt, today)
    for surface in ['chatgpt','gemini','claude','perplexity','brave','you']:
        surf_data = data.get('by_surface',{}).get(surface,{})
        snapshots.append({
            'date': today,
            'prompt': prompt,
            'surface': surface,
            'cited': 'example.com' in surf_data.get('citations',[]),
            'cited_url': next((c for c in surf_data.get('citations',[]) if 'example.com' in c), None),
            'competitor_cited': [c for c in surf_data.get('citations',[]) if any(comp in c for comp in ['competitor1','competitor2'])],
            'brand_mentioned': 'Example' in surf_data.get('text',''),
        })

df = pd.DataFrame(snapshots)
df.to_csv(f'citation-{today}.csv', index=False)
```

### Recipe 6: Citation-share trend (week-over-week)
```python
import pandas as pd
import glob

# Aggregate 7-day window
files = glob.glob('citation-2026-06-*.csv')
df = pd.concat([pd.read_csv(f) for f in files])

# Citation share per surface
share = df.groupby(['surface','date']).agg({'cited': 'mean'}).reset_index()
share['date'] = pd.to_datetime(share['date'])

# Week-over-week delta
weekly = share.set_index('date').groupby('surface').rolling('7D')['cited'].mean().reset_index()
print(weekly.tail(20))

# Alert on >20% drop
latest = share.groupby('surface').tail(1).set_index('surface')['cited']
baseline = share.groupby('surface').apply(lambda x: x.iloc[:-7]['cited'].mean()).rename('baseline')
delta = (latest - baseline) / baseline
alerts = delta[delta < -0.20]
if not alerts.empty:
    print(f"ALERTS — citation drop >20%:")
    print(alerts)
```

### Recipe 7: Per-surface share-of-voice vs competitors
```python
# Profound's share-of-voice endpoint
r = requests.get(
    'https://api.profound.com/v1/brand/share-of-voice',
    params={'brand': 'Example', 'competitors': 'competitor1,competitor2,competitor3', 'surface': 'chatgpt', 'since': '2026-05-01'},
    headers={'Authorization': f'Bearer {PROFOUND_API_KEY}'}
)
sov = r.json()
# {'Example': 0.18, 'competitor1': 0.32, 'competitor2': 0.25, 'competitor3': 0.15, 'other': 0.10}
print(f"SOV in ChatGPT: {sov}")
```

### Recipe 8: Drill-down — what URLs are being cited
```python
# For surfaces where you're winning citations, identify which URLs Athena/Profound find
df_cited = df[df['cited'] == True]
url_freq = df_cited['cited_url'].value_counts()
print("Top-cited URLs of yours:")
print(url_freq.head(20))

# Pattern check — these URLs likely follow AEO content optimization patterns:
# direct-answer block, entity-rich, schema depth (see aeo-content-optimization-entity-rich skill)
```

### Recipe 9: Alert on citation drop via gmail-mcp
```python
# Daily cron after Recipe 6
if not alerts.empty:
    alert_body = f"Citation share dropped >20% on surfaces: {alerts.to_dict()}\n\n"
    alert_body += f"Investigate: latest data {df.tail(20).to_string()}"

    gmail.send(
        to='seo-team@example.com',
        subject=f'AEO ALERT: Citation drop on {len(alerts)} surfaces',
        body=alert_body
    )
```

### Recipe 10: Prompt set construction (which prompts to track)
```
Prompts should mirror real user search queries that AI surfaces answer:
- "What is the best X?" (comparison intent)
- "How do I [verb] [object]?" (instructional intent)
- "What is X?" (definitional intent)
- "Best X for Y in 2026" (specific year + persona)

Source from:
- GSC top-impressions queries (Suganthan GSC)
- Ahrefs questions modifier filter
- DataForSEO PAA scrape (serp-analysis-intent-snippet-paa skill)
- Athena/Profound built-in prompt libraries
- Manual customer interview themes

Aim for: 20-50 prompts per cluster; quarterly review + refresh.
```

### Recipe 11: GoogleAI Overviews tracking (separate surface, no third-party tracker reliable yet)
```bash
# Workaround: Suganthan GSC `serp_features --features ai_overview` (when supported)
mcp tool suganthan-gsc.serp_features \
  --site_url "sc-domain:example.com" \
  --features "ai_overview" \
  --days 28
```
AI Overviews citation tracking still emerging — Athena added partial coverage Q1 2026; Profound + others lag.

## Examples

### Example 1: Initial AEO baseline + 90-day tracking
**Goal:** Establish citation share baseline; track quarterly.

**Steps:**
1. Pick vendor (Athena for global, Otterly/Peec for EU, Profound for API-first stack).
2. Recipe 10: build initial 30-prompt tracking set per cluster.
3. Recipe 1 (or vendor equivalent): configure daily polling.
4. After 7 days: Recipe 5 → first baseline snapshot.
5. After 30/60/90 days: Recipe 6 → trend report.
6. Pair with AEO content optimization (`aeo-content-optimization-entity-rich`) → before/after measurement.

**Result:** Quantified AEO baseline + trend; informs content strategy.

### Example 2: Diagnose sudden citation drop
**Goal:** Citations dropped 25% on Perplexity in last 7 days — why?

**Steps:**
1. Recipe 9 alert fires.
2. Recipe 8: which URLs WERE being cited?
3. Check those URLs:
   - Recent rewrites that removed direct-answer block?
   - Schema deprecated?
   - dateModified reset (article looks "stale" to LLM retrievers)?
   - Competitor published equivalent content with stronger signals?
4. Hypothesize + remediate.

**Result:** Diagnostic with action plan; track recovery via Recipe 6.

### Example 3: Share-of-voice slide for executive report
**Goal:** Executive summary showing AEO position vs competitors per surface.

**Steps:**
1. Recipe 7 × 4 surfaces (ChatGPT / Gemini / Claude / Perplexity).
2. Generate bar chart per surface with brand + 3 competitors.
3. Embed in `pptx` via the deck skill.
4. Caption: "Our citation share is X% on Y; competitor lead by Z%."

**Result:** Executive-grade visualization for QBR.

## Edge cases / gotchas

- **Different vendors produce different citation results** — Athena and Profound poll their own LLM accounts; results diverge ~10-30%. Pick ONE for trend consistency; don't cross-vendor compare.
- **Citation share != organic clicks** — AEO citation in ChatGPT doesn't necessarily produce traffic. Some sources show citation lift WITHOUT click lift (zero-click consumption).
- **AI Overviews from Google still maturing** — Suganthan GSC supports partially; full-coverage trackers landing late 2026.
- **Prompts must reflect real queries** — tracking made-up prompts gives garbage data. Source from GSC + PAA + customer themes.
- **Daily polling cost adds up** — 50 prompts × 6 surfaces × 30 days = 9000 LLM calls/mo. Vendor pricing reflects this.
- **LLM responses non-deterministic** — same prompt different day = different citations. Average over 7-day window.
- **Citation URL vs citation text** — some LLMs surface the URL; some name the brand without URL. Track both metrics.
- **`brand_mentioned` vs `cited`** — brand named in answer ≠ URL linked. Both matter for AEO — name-mention drives recall, URL-cite drives traffic.
- **Region-restricted models** — Gemini Europe behaves differently from US Gemini. Match tracker region to audience region.
- **Hallucination risk** — LLMs sometimes cite URLs that don't exist on your domain. Don't celebrate hallucinated citations.
- **Anthropic / OpenAI API price changes** — vendor pricing can shift overnight. Lock in annual where possible.

## Sources

- [AthenaHQ — homepage and docs](https://athenahq.ai/)
- [Profound — AI search citation API](https://www.profound.ai/)
- [Otterly — European AEO tracking](https://otterly.ai/)
- [Peec.ai — European AEO](https://peec.ai/)
- [Surfer GEO blog](https://surferseo.com/blog/geo-optimization/)
- [Goodie — AI search brand monitoring](https://goodie.ai/)
- [Search Engine Land — AI search tracking tools 2026](https://searchengineland.com/aeo-tracking-tools)
- [Google AI Overviews documentation](https://developers.google.com/search/docs/appearance/ai-features)
