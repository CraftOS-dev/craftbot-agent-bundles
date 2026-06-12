<!--
Source: https://docs.commonroom.io/ + https://www.pocus.com/ + https://www.koala.io/
Signal + intent monitoring (June 2026 SOTA).
-->
# Signal + Intent Monitoring (Pocus / Koala / Common Room) — SKILL

Aggregate buying signals from product usage (Pocus / Koala / PostHog), community + dark social (Common Room), job changes (Apollo), funding events (Crunchbase), tech-stack shifts (BuiltWith), and anonymous site traffic (RB2B / Default). Rank accounts by composite score; push the top-10 hot accounts into CRM as AE tasks daily.

## When to use

- **PLG / freemium motion** with product-usage signals to convert to paid.
- **Champion-mover monitoring** — when a champion changes jobs, re-engage at their new company.
- **Account-prioritization** — daily "what 10 accounts should the SDR team work today?".
- **Intent-driven outbound** — pause cold-only sequences; route warm-intent into AE-touched cadences instead.
- **Trigger phrases**: "hot accounts today", "who's showing intent", "PLG-to-sales", "champion moved", "intent signal review", "set up signal monitoring".

Do NOT use this skill for: **first-party CRM scoring** (use `hubspot-sales-mcp` recipe 3); **website traffic analytics** (use `posthog-mcp` / `mixpanel-mcp` directly); **broad market research** (use `account-research-deep`).

## Setup

```bash
# Most signal tools are paid SaaS — onboard via api-gateway for managed OAuth
export MATON_API_KEY="<key>"

# Direct keys (when gateway unavailable)
export COMMON_ROOM_API_KEY="<key>"   # $0 free tier (limited), $999/mo Pro
export POCUS_API_KEY="<key>"         # $1k+/mo, contracted
export KOALA_API_KEY="<key>"         # $399/mo Starter, $1k+ Pro
export RB2B_API_KEY="<key>"          # $0-499/mo (depends on monthly visitors revealed)
export APOLLO_API_KEY="<key>"        # for job-change webhook (in apollo-clay-lead-enrichment skill)

# Free fallback signal sources
# - PostHog product usage (posthog-mcp)
# - Crunchbase funding (free with limits)
# - LinkedIn job postings (via brightdata-mcp scraping)
# - G2 / Capterra category pages (via brave-search)

# Storage: postgresql-mcp or a single Notion DB
export PG_URI="postgresql://signals_db_uri"
```

## Common recipes

### Recipe 1: Common Room — community engagement signal

```bash
# Pull active members by activity score in the last 7 days
curl -X GET "https://gateway.maton.ai/commonroom/v1/community/members?activityScoreMin=70&timeRange=7d" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq '.members[] | {
    name, email, company, last_activity, activity_score,
    channels: [.signals[] | .source]
  }'
```

Common Room watches your Slack community, Discord, GitHub repo, Reddit, X, LinkedIn for mentions/engagement; surfaces high-activity people who work at target accounts.

### Recipe 2: Pocus — PLG product activity signal

```bash
curl -X POST "https://gateway.maton.ai/pocus/v2/signals/search" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "scoreMin":50,
    "dateRange":"last_14_days",
    "signalTypes":["product_qualified_lead","power_user","expansion_signal"]
  }'
```

Returns accounts where product-usage thresholds fired (>= 5 users / 2 modules / sessions > 30/wk etc.). Pair with `posthog-mcp` for raw events.

### Recipe 3: Koala — PLG signal feed

```bash
# Koala publishes a webhook per qualifying event
# Poll for high-score accounts via REST
curl -X GET "https://gateway.maton.ai/koala/v1/accounts?score_gte=70&since=2026-06-08" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq '.accounts[] | {
    domain, score, recent_pages: .visits[:5], users_count
  }'
```

Koala identifies the visiting *company* from anonymous traffic via reverse-IP; assigns score based on page mix (pricing > docs > marketing pages).

### Recipe 4: RB2B / Default — anonymous-visitor de-anonymization

```bash
# RB2B installs a script on your site that resolves a small % of US-based visitors to person + company
curl -X GET "https://gateway.maton.ai/rb2b/v1/visits?from=2026-06-08&min_pages=3" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq '.visits[] | {
    person, company, pages, last_visit
  }'
```

RB2B free tier: 100 reveals/mo; paid $99-499/mo. Default is the alternative ($0-1k/mo). Both have 5-15% US visitor reveal rate.

### Recipe 5: Apollo job-change webhook (see apollo-clay-lead-enrichment Recipe 8)

```bash
# Already covered there — re-included as a primary signal source for this skill
# Webhook fires when a tracked person (champion list, won-deal contact, lost-deal contact) changes jobs
```

### Recipe 6: BuiltWith tech-stack diff (added our adjacent tool)

```bash
# Compare last week's stack vs this week's; fire if "Stripe" or "Snowflake" was newly added
LAST_WEEK=$(curl -s "https://api.builtwith.com/v21/api.json?KEY=$BUILTWITH_API_KEY&LOOKUP=acme.com" | jq '.Results[0].Result.Paths[0].Technologies' | sha256sum)
THIS_WEEK=$(curl -s "https://api.builtwith.com/v21/api.json?KEY=$BUILTWITH_API_KEY&LOOKUP=acme.com" | jq '.Results[0].Result.Paths[0].Technologies' | sha256sum)
# If hashes differ, diff and check for our adjacent-tool list
```

Or use BuiltWith's "Recently Added Technologies" filter in their Pro UI.

### Recipe 7: Crunchbase funding webhook

```bash
# Crunchbase Enterprise plans support webhooks; otherwise daily poll
curl -X POST "https://api.crunchbase.com/api/v4/searches/funding_rounds" \
  -H "X-cb-user-key: $CRUNCHBASE_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "field_ids":["identifier","investment_type","money_raised","announced_on"],
    "query":[
      {"type":"predicate","field_id":"announced_on","operator_id":"gte","values":["2026-06-01"]},
      {"type":"predicate","field_id":"investment_type","operator_id":"includes","values":["series_a","series_b","series_c"]}
    ],
    "limit":50
  }'
```

### Recipe 8: G2 + Capterra intent (comparison-page visits)

```bash
# G2 publishes "Buyer Intent" signals on their Pro plan ($499+/mo)
curl -X GET "https://gateway.maton.ai/g2/v2/intent?category=sales_engagement&since=2026-06-01" \
  -H "Authorization: Bearer $MATON_API_KEY"

# Capterra has a similar product ($999+/mo)
```

### Recipe 9: Composite scoring (combine all signals → top-10 hot accounts)

```python
# Pull all signals, score each account, rank
import requests, os, collections
SIGNAL_WEIGHTS = {
    "common_room_active": 10,
    "pocus_pql": 20,
    "koala_high_intent": 20,
    "rb2b_pricing_page": 25,
    "apollo_job_change_champion": 30,
    "builtwith_adjacent_tech_added": 15,
    "crunchbase_recent_funding": 15,
    "g2_compare_page_visit": 15,
}

scores = collections.defaultdict(lambda: {"score":0,"signals":[]})

# (illustrative; in practice paginate + dedupe)
for member in commonroom_active_members():
    if member["activity_score"] > 70:
        scores[member["company"]]["score"] += SIGNAL_WEIGHTS["common_room_active"]
        scores[member["company"]]["signals"].append("commonroom_active")

for acct in koala_high_intent():
    scores[acct["domain"]]["score"] += SIGNAL_WEIGHTS["koala_high_intent"]
    scores[acct["domain"]]["signals"].append("koala_high_intent")

# ...repeat per source

# Top 10
top = sorted(scores.items(), key=lambda x: -x[1]["score"])[:10]
for company, data in top:
    print(company, data["score"], data["signals"])
```

### Recipe 10: Push top-10 → CRM tasks (daily cron)

```python
# Continuing Recipe 9 — write to HubSpot
import requests, os
for company, data in top:
    # Find owner via Recipe 1 from hubspot-sales-mcp
    contact_resp = requests.post(
        "https://gateway.maton.ai/hubspot/crm/v3/objects/contacts/search",
        headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"},
        json={"filterGroups":[{"filters":[{"propertyName":"company","operator":"EQ","value":company}]}],"properties":["hubspot_owner_id","email"],"limit":1},
    ).json()
    owner_id = contact_resp["results"][0]["properties"].get("hubspot_owner_id") if contact_resp["results"] else None

    requests.post(
        "https://gateway.maton.ai/hubspot/crm/v3/objects/tasks",
        headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"},
        json={
            "properties":{
                "hs_task_subject":f"Hot signals at {company}: {', '.join(data['signals'])}",
                "hs_task_body":f"Composite score {data['score']}. Work this account today.",
                "hs_timestamp":"<today-end-of-day-ms>",
                "hubspot_owner_id":owner_id,
                "hs_task_priority":"HIGH"
            }
        },
    )
```

Wire as a daily 7am cron via `postgresql-mcp` or a small Python script.

### Recipe 11: Storage schema (postgresql-mcp)

```sql
-- One row per (account, day) — denormalized for dashboards
CREATE TABLE signals_daily (
    id SERIAL PRIMARY KEY,
    account_domain TEXT NOT NULL,
    account_name TEXT,
    signal_date DATE NOT NULL,
    common_room_score INT DEFAULT 0,
    pocus_score INT DEFAULT 0,
    koala_score INT DEFAULT 0,
    rb2b_visits INT DEFAULT 0,
    apollo_job_change BOOLEAN DEFAULT false,
    builtwith_diff JSONB,
    crunchbase_funding JSONB,
    composite_score INT DEFAULT 0,
    signals_array TEXT[],
    UNIQUE (account_domain, signal_date)
);
CREATE INDEX ON signals_daily (signal_date, composite_score DESC);
```

Daily run upserts; weekly rollup feeds the sales-leader dashboard.

### Recipe 12: Champion-mover specific play

```python
# When Apollo fires person_job_changed for a contact tagged "champion":
def champion_moved(payload):
    person = payload["person"]
    old_co = payload["old_organization"]["name"]
    new_co = payload["new_organization"]["name"]

    # 1. Create new contact at new company
    new_contact_id = hubspot_create_contact({
        "email": person.get("email"),  # may be guessed; verify before sending
        "firstname": person["first_name"],
        "lastname": person["last_name"],
        "company": new_co,
        "lead_source": "champion-mover-alert",
        "lifecyclestage": "lead",
        "previous_company": old_co,
        "was_champion_at": old_co,
    })

    # 2. Task the old owner (likely AE who owned the prior account)
    hubspot_create_task({
        "subject": f"Re-engage {person['name']} at new company {new_co}",
        "body": f"Was champion at {old_co}. Likely same pain at {new_co}. Book a quick re-intro.",
        "owner_id": prior_account_owner_id,
        "priority": "HIGH",
        "due": "+7 days",
    })

    # 3. Slack DM to AE
    slack_dm(prior_account_owner_id, f"Champion moved: {person['name']} {old_co} → {new_co}")
```

## Examples

### Example 1: Daily 7am hot-accounts digest

**Goal:** Every weekday at 7am, the top-10 hot accounts surface as tasks for the SDR team.

**Steps:**
1. Cron triggers at 7am UTC (or per-region adjusted).
2. Pull signals from each source (Recipes 1-8) for the last 24h.
3. Recipe 9 composite-scores and ranks.
4. Recipe 10 writes top-10 as HubSpot tasks; one per account, assigned by territory / round-robin.
5. Slack post in `#sdr-room` lists the top-10 with composite score + signal mix.
6. Recipe 11 archives the full table to `postgresql-mcp` for trend analysis.

**Result:** SDRs start each day with a prioritized list grounded in real intent, not gut feel.

### Example 2: PLG signup → AE-touched cadence

**Goal:** When a freemium signup hits "power user" threshold (Pocus PQL), pause cold-only sequences and route to AE.

**Steps:**
1. Pocus webhook fires on PQL threshold breach.
2. Lookup CRM: is this contact already in a cold sequence?
3. If yes → call `outreach-salesloft-sequences` recipe 11 to pause; then enroll in "warm-intent-AE-touched" cadence.
4. Create AE task: "PQL signal — 5 users at <company>, 2 modules used in last 7 days. Book exec call."
5. Update lead score +25 in HubSpot.

**Result:** Hot intent doesn't get burned by cold-tone messaging; AE owns the close.

## Edge cases / gotchas

- **Signal noise vs signal-of-real-intent**: visiting a pricing page once does not = buying intent. Calibrate thresholds on closed-won historical data (e.g., "in won deals, the avg signal-composite-score 30 days before close was 75").
- **Source-overlap inflates scores**: Pocus + Koala both surface PLG signals from the same product event. De-dupe by event type + 24h window.
- **Common Room mis-attributes**: a community member can be associated with a company they no longer work at. Cross-check `company` against LinkedIn current employer via `apollo-clay-lead-enrichment` enrich before counting.
- **RB2B / Default coverage is regional**: ~5-15% reveal rate on US traffic, much lower outside. EU-traffic reveal often blocked by GDPR design.
- **GDPR + signal data**: pre-registered intent (Common Room from your own community) is generally fine; third-party intent (G2 buyer intent) requires careful legal-basis documentation in EU.
- **Webhook reliability**: Apollo, Crunchbase, and most signal tools drop ~1-2% of webhooks. Always pair with a daily reconciliation poll.
- **Pocus + Koala are not free**: Pocus is contract-based ($1k+/mo), Koala $399+/mo. For solo/early-stage, prefer PostHog product analytics ($0-2k/mo depending on volume) + manual review.
- **Signal scoring drifts**: a 3-month-old signal scoring model misses what's actually predictive now. Re-tune weights quarterly against won-deal data.
- **CRM task fatigue**: if you create > 5 signal tasks per AE per day, they'll start ignoring them. Cap at 3 / day / AE; over-flow goes to a "watch list" not a task.
- **Champion-mover false positives**: Apollo's job-change fires on LinkedIn title edit, not just employer change. Filter for `new_organization != old_organization` strictly.
- **Tech-stack diff false-positives**: BuiltWith re-detects tools on site re-render; a tool flicking on/off across daily diffs is noise. Require 7+ day persistence before firing a signal.

## Sources

- Common Room docs: https://docs.commonroom.io/
- Pocus home + product overview: https://www.pocus.com/
- Koala docs: https://docs.getkoala.com/
- RB2B (anonymous visitor reveal): https://www.rb2b.com/
- Default (signals dashboard): https://www.default.com/
- BuiltWith API: https://api.builtwith.com/
- Crunchbase API: https://data.crunchbase.com/docs/getting-started
- G2 Buyer Intent API: https://api.g2.com/docs/
- 2026 PLG-to-sales signal stack comparison: https://www.pocus.com/blog/plg-signal-stack-2026
- "Champion-mover playbook" — Gong (2024): https://www.gong.io/blog/champion-tracker/
