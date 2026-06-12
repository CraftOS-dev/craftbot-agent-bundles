<!--
Sources: Sensor Tower (post-2024 data.ai merger) https://sensortower.com/
         Apptopia https://apptopia.com/
         Appfigures (free tier) https://appfigures.com/
         data.ai legacy https://www.data.ai/
         Slashdot comparison https://slashdot.org/software/comparison/Apptopia-vs-Sensor-Tower-vs-data.ai-Intelligence/
         Sensor Tower acquisition https://dexteragent.ai/companies/sensor-tower-1771769454
Companion playbook: role.md → "SOTA tool reference" → Sensor Tower + Apptopia + signal-layer cadence app-store row
-->

# Competitor app intelligence (Sensor Tower / data.ai / Apptopia / Appfigures)

Mobile app intelligence — downloads, revenue estimates, store rankings, SDK adoption, retention proxies, in-app-purchase tiers, ad-network presence. Sensor Tower (post-2024 data.ai merger = industry standard, broadest panel + historical depth). Apptopia (bundles more at base + better API at higher tiers). Appfigures (free tier for indie use). Pair with App Store + Play Store review scrape (free + ToS-permitted) for qualitative.

## When to use

- "Track [competitor]'s mobile app rankings"
- "Are downloads growing or shrinking?"
- "What's their estimated MRR/ARR from mobile?"
- "Which SDKs are they using (analytics / ad networks / auth)?"
- New mobile app launch by competitor
- App-store review sentiment shift detection
- Weekly cadence per role.md signal layer table

## When NOT to use

- Web SEO + paid → use `competitor-seo-ahrefs-semrush-organic` and `competitor-ad-pathmatics-spyfu-semrush`
- Web tech stack → use `competitor-tech-stack-builtwith-wappalyzer`
- Mobile ad creative inventory → use `competitor-ad-pathmatics-spyfu-semrush` (Meta Ad Library covers mobile placements)
- Cohort retention internal analytics → out of scope

## Setup

```bash
# Sensor Tower ($1k-10k+/mo enterprise)
export SENSOR_TOWER_API_KEY="..."
export SENSOR_TOWER_AUTH_TOKEN="..."

# Apptopia (similar enterprise pricing)
export APPTOPIA_API_KEY="..."

# Appfigures (free tier + paid)
export APPFIGURES_CLIENT_ID="..."
export APPFIGURES_CLIENT_SECRET="..."

# Google Play unofficial scraping libs (free)
# pip install google-play-scraper app-store-scraper

# Firecrawl for review pages
export FIRECRAWL_API_KEY="..."

# Slack delivery
export SLACK_WEBHOOK_URL="..."
```

MCPs in `agent.yaml`: `google-play`, `firecrawl-mcp`, `playwright-mcp`, `slack-mcp`, `notion-mcp`.

## Common recipes

### Recipe 1: Sensor Tower — downloads + revenue estimates

```bash
# By app id (iOS) or package name (Android)
curl -H "Authorization: Bearer $SENSOR_TOWER_AUTH_TOKEN" \
  "https://api.sensortower.com/v1/ios/sales_report_estimates?\
app_ids=123456789&\
countries=US,GB,DE&\
date_granularity=daily&\
start_date=2026-05-01&\
end_date=2026-06-10"
```

Returns: estimated downloads, IAP revenue. Caveat — estimates not actuals; Sensor Tower triangulates panel data + store rank curves. Confidence higher for large apps.

### Recipe 2: Sensor Tower — store rank history

```bash
curl -H "Authorization: Bearer $SENSOR_TOWER_AUTH_TOKEN" \
  "https://api.sensortower.com/v1/ios/category/category_history?\
app_id=123456789&\
category=6020&\
chart_type_ids=topfreeapplications,toppaidapplications,topgrossingapplications&\
countries=US&\
start_date=2026-05-01&\
end_date=2026-06-10"
```

### Recipe 3: Sensor Tower — SDK adoption

```bash
curl -H "Authorization: Bearer $SENSOR_TOWER_AUTH_TOKEN" \
  "https://api.sensortower.com/v1/ios/apps/sdks?app_ids=123456789"
```

Returns: SDKs detected (analytics: Mixpanel/Amplitude/Firebase; ad networks: AdMob/AppLovin/Unity Ads; auth: Auth0/Okta; payments: Stripe; observability: Sentry/Bugsnag).

### Recipe 4: Apptopia — app intelligence

```bash
curl -H "X-API-KEY: $APPTOPIA_API_KEY" \
  "https://api.apptopia.com/v2/apps/123456789/performance?\
metric=downloads,revenue,daus,maus&\
start_date=2026-05-01&\
end_date=2026-06-10"
```

### Recipe 5: Apptopia — SDK pipeline (better than ST for fast-moving)

```bash
curl -H "X-API-KEY: $APPTOPIA_API_KEY" \
  "https://api.apptopia.com/v2/apps/123456789/sdks?\
since=2026-04-01"
```

Returns: SDK adoption + removal events with detected timestamps. Use for "they switched from Firebase Analytics to Amplitude" signal.

### Recipe 6: Appfigures — free tier alternative

```bash
# OAuth-based
curl -H "Authorization: Bearer $APPFIGURES_ACCESS_TOKEN" \
  "https://api.appfigures.com/v2/products/<product_id>/ranks?\
start_date=2026-05-01&\
end_date=2026-06-10&\
granularity=daily"
```

Appfigures free tier covers ranking + reviews + ratings. Estimates available on paid tiers.

### Recipe 7: Google Play scrape (free, unofficial)

```python
from google_play_scraper import app, reviews_all
info = app("com.acme.app", lang="en", country="us")
print(info["installs"], info["score"], info["ratings"])
# Reviews
rs = reviews_all("com.acme.app", lang="en", country="us", sleep_milliseconds=100)
print(len(rs), "reviews")
```

### Recipe 8: App Store scrape (free, unofficial)

```python
from app_store_scraper import AppStore
app = AppStore(country="us", app_name="acme-pro", app_id="123456789")
app.review(how_many=500)
for r in app.reviews[:5]:
    print(r["date"], r["rating"], r["title"], r["review"][:100])
```

### Recipe 9: Review theme extraction (negative + positive)

```python
import anthropic
client = anthropic.Anthropic()
reviews_text = "\n\n".join(f"{r['rating']}* — {r['review']}" for r in app.reviews[:200])
prompt = f"""From these App Store reviews of Acme Pro, extract:
- top 5 negative themes with example reviews
- top 5 positive themes with example reviews
- emerging concern (any theme growing L30D vs prior 60D)

Reviews:
{reviews_text}
"""
msg = client.messages.create(
    model="claude-opus-4-7-1m",
    max_tokens=3000,
    messages=[{"role":"user","content":prompt}],
)
```

### Recipe 10: Per-app YAML snapshot

```yaml
# data/app-intel/acme.yaml
competitor: acme-corp
app:
  ios:
    bundle_id: com.acme.app
    app_id: 123456789
    snapshot_date: 2026-06-11
  android:
    package: com.acme.app
    snapshot_date: 2026-06-11
metrics:
  L30D:
    downloads_est: 142000
    rev_est_usd: 218000
    rank_us_top_overall: 247
    rank_us_top_business: 14
    rating: 4.6
    review_count: 84112
sdks_detected:
  - Firebase Analytics
  - Amplitude (added 2026-05-12)
  - AppsFlyer (removed 2026-04-22)
  - Stripe
  - Sentry
top_neg_themes:
  - "crash on Android 14"
  - "sync delay"
  - "pricing change confusion"
top_pos_themes:
  - "fast onboarding"
  - "good Slack integration"
```

### Recipe 11: Weekly app digest

```python
# Aggregate L7D vs prior 7D
delta = {
    "downloads": "+12%",
    "rev_est":   "+8%",
    "rating":    -0.1,
    "rank_us_business": "-3 positions",
}
# Add to weekly CI digest
```

### Recipe 12: Slack hot signal on rank surge

```python
def alert_rank_surge(competitor, app_id, prior_rank, curr_rank, category):
    if prior_rank - curr_rank >= 20:  # jumped 20+ positions up
        requests.post(SLACK_WEBHOOK_URL, json={
            "text": f":rocket: {competitor} {app_id} rank surge in {category}: "
                    f"{prior_rank} -> {curr_rank} (L7D)",
            "channel": "#ci-hotline",
        })
```

### Recipe 13: SDK switch detection

```python
prior = set(yaml.safe_load(open("data/app-intel/acme-2026-06-04.yaml"))["sdks_detected"])
curr  = set(yaml.safe_load(open("data/app-intel/acme-2026-06-11.yaml"))["sdks_detected"])
added = curr - prior; removed = prior - curr
for sdk in added: print("ADDED:", sdk)
for sdk in removed: print("REMOVED:", sdk)
```

## Examples

### Example 1: Detect Acme mobile launch + ramp

**Goal:** Track Acme's mobile app from launch through first 90 days.

**Steps:**
1. Recipe 1 + 2 → Sensor Tower daily downloads + rank.
2. Recipe 3 → SDK inventory (analytics, ad networks, auth).
3. Recipe 8 → App Store reviews; Recipe 9 → theme extraction weekly.
4. Recipe 10 → daily YAML snapshot; Recipe 11 → weekly digest.
5. Recipe 12 → hot signal on any 20-position rank surge.

**Result:** Continuous mobile signal feed; battlecard pane 4 (parity) updated when ranking enters top-50 in category.

### Example 2: SDK switch detection — Acme moved from AppsFlyer to Branch

**Goal:** Detect attribution-platform switch (signals mobile-marketing strategy shift).

**Steps:**
1. Recipe 3 (ST) + Recipe 5 (Apptopia) weekly.
2. Recipe 13 → set-diff vs prior week.
3. ADDED: Branch; REMOVED: AppsFlyer.
4. Cross-reference hiring intel (Recipe 5 of hiring skill) → confirmed 2 Mobile Marketing Lead job posts mentioning Branch.

**Verdict:** Confirmed switch; pricing leverage opportunity if we partner with AppsFlyer.

### Example 3: Free path — Appfigures + Play scrape only

**Goal:** Track competitor mobile signal on $0 budget.

**Steps:**
1. Recipe 6 → Appfigures free tier for rankings + reviews.
2. Recipe 7 + 8 → scrape Play + App Store for reviews directly.
3. Recipe 9 → LLM theme extraction.
4. No download estimates; rely on rank-curve as proxy.

**Result:** Workable mobile CI for $0; missing revenue estimates.

## Edge cases / gotchas

- **Sensor Tower estimates** — algorithmic, ~70-85% accurate for top-1000 apps; less for long-tail.
- **Apptopia methodology** — different panel mix; usually different absolute numbers vs Sensor Tower. Pick one as canonical; treat the other as cross-check.
- **data.ai legacy data** — pre-2024 historical data is now under Sensor Tower; some old API endpoints deprecated; check current docs.
- **Google Play scrape rate limits** — `google_play_scraper` library: ~1 req/sec safe; respect.
- **App Store scrape rate limits** — `app_store_scraper`: country-specific; some countries throttle harder.
- **Country-specific data** — store rankings + downloads vary widely by country; sample at least US + GB + DE + JP + key markets.
- **SDK detection lag** — both ST and Apptopia rely on bundle decompilation; new SDKs may take 1-2 weeks to detect.
- **Unofficial scrape lib breakage** — Google Play / App Store DOM changes; libs may break monthly. Pin versions; have firecrawl fallback.
- **Review language** — country-specific Review pulls return native-language reviews; use `deepl-mcp` to translate before theme extraction.
- **In-app subscription pricing tiers** — Sensor Tower exposes IAP tier prices; useful for pricing intelligence cross-reference.
- **Privacy nutrition labels** — App Store privacy labels are public; can detect data-collection practices changes.
- **Don't trust review count over time** — Apple/Google occasionally purge fake reviews; sudden review-count drops aren't sentiment shifts.
- **Children's apps / regulated categories** — different metrics and restrictions; tag in YAML.
- **PROACTIVE.md cadence** — weekly default per signal layer cadence; daily during launch detection.
- **Provenance footer** — Sensor Tower / Apptopia data is paid-source-class; store reviews are public.

## Sources

- Sensor Tower — https://sensortower.com/
- Sensor Tower acquisition of data.ai — https://dexteragent.ai/companies/sensor-tower-1771769454
- Apptopia — https://apptopia.com/
- Apptopia vs Sensor Tower vs data.ai — https://slashdot.org/software/comparison/Apptopia-vs-Sensor-Tower-vs-data.ai-Intelligence/
- Appfigures — https://appfigures.com/
- google-play-scraper — https://github.com/JoMingyu/google-play-scraper
- app-store-scraper — https://github.com/cowboy-bebug/app-store-scraper
- role.md → "SOTA tool reference" → Sensor Tower + Apptopia

## Related skills

- `competitor-review-g2-trustradius-capterra` — qualitative review intel paired with app store reviews
- `competitor-ad-pathmatics-spyfu-semrush` — mobile creative + spend
- `continuous-competitor-monitoring-klue-kompyte-crayon` — weekly app intel in fan-out
- `feature-parity-tracking` — mobile-only features in the parity matrix
- `competitor-hiring-intel-linkedin-sales-nav` — cross-reference SDK switches with hiring
