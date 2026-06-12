<!--
Source: Hightouch + Census (Fivetran 2025) docs + RudderStack vs Hightouch + Polytomic reverse-ETL
-->
# Reverse ETL — Hightouch / Census / Polytomic SKILL

> Sync warehouse audiences to growth tools (Klaviyo, Customer.io, HubSpot, Facebook Custom Audiences). Hightouch is Gartner MQ Leader; Census now part of Fivetran (May 2025). Composable CDP — no separate data store.

## When to use

Trigger phrases:
- "Sync our warehouse cohorts to [Klaviyo / Customer.io / HubSpot / Facebook]"
- "Reverse ETL"
- "Warehouse-as-CDP"
- "Activate warehouse data"
- "Composable CDP"

Pair: `cdp-segment-rudderstack-mparticle` (the source of warehouse events), `behavioral-cohort-design` (the cohort definition), `win-back-campaigns` / `free-to-paid-upgrade-prompts` (downstream activation).

## Setup

```bash
export HIGHTOUCH_API_KEY="ht_..."
export CENSUS_API_TOKEN="csn_..."      # now Fivetran-namespaced; legacy works
export POLYTOMIC_API_KEY="pty_..."
export RUDDERSTACK_REVERSE_ETL_KEY="rs_..."

# Warehouse credentials
export SNOWFLAKE_USER="..."
export SNOWFLAKE_PASSWORD="..."
export BIGQUERY_KEYFILE="path/to/sa.json"
export REDSHIFT_URL="..."
```

## Platform decision matrix (June 2026)

| Tool | Destinations | Pricing | Strengths | When to use |
|---|---|---|---|---|
| **Hightouch** | 200+ | Tiered $0-50K+/yr | Gartner MQ Leader; $1.2B; deepest catalog | Default; broad destination needs |
| **Census** (now Fivetran) | 150+ | Bundled w/ Fivetran usually | Acquired by Fivetran May 2025 | Already on Fivetran |
| **Polytomic** | 100+ | $0-15K+/yr | Embedded use cases (multi-tenant SaaS) | SaaS apps embedding reverse-ETL |
| **RudderStack Reverse ETL** | Same as RudderStack | Bundled w/ RudderStack | Free if on RudderStack OSS | Already on RudderStack |
| **Workato** | 1,200+ apps (not pure) | Enterprise | Full iPaaS | iPaaS-broader needs |
| **Tray.io** | 600+ | $0-50K+/yr | Workflow automation + reverse-ETL | iPaaS + reverse-ETL hybrid |

## Common use cases

| Use case | Source | Destination | Why warehouse-first |
|---|---|---|---|
| **Audience activation (email)** | warehouse cohort | Klaviyo / Customer.io / Iterable | Marketing wants SQL-defined cohort |
| **Ad-platform Custom Audiences** | warehouse cohort | Facebook / Google / TikTok / LinkedIn | Match offline customer LTV |
| **CRM enrichment** | warehouse user attributes | HubSpot / Salesforce | Augment sales CRM w/ product signals |
| **Personalization for in-product** | warehouse cohort | Intercom / Userpilot | Behavioral triggered in-app messages |
| **PQL handoff** | warehouse PQL score | HubSpot / Salesforce + Slack | See `pql-product-qualified-leads-framework` |
| **Support context** | warehouse usage data | Intercom / Zendesk | Agents see usage history |
| **Finance ops** | warehouse revenue rollup | NetSuite / QuickBooks | Single source of truth for revenue |

## Common recipes

### Recipe 1: Hightouch model + sync (warehouse → Klaviyo)

```bash
# 1. Create model (SQL definition of audience)
curl -X POST "https://api.hightouch.com/api/v1/models" \
  -H "Authorization: Bearer $HIGHTOUCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "PQL High",
    "source_id": "snowflake_prod_id",
    "query": "SELECT user_id, email, first_name, pql_score, plan_tier FROM analytics.user_features WHERE pql_score >= 70 AND last_active_at > current_date - 7",
    "primary_key": "user_id"
  }'

# 2. Create destination connection (Klaviyo)
curl -X POST "https://api.hightouch.com/api/v1/destinations" \
  -H "Authorization: Bearer $HIGHTOUCH_API_KEY" \
  -d '{
    "type": "klaviyo",
    "name": "Klaviyo Prod",
    "config": {"api_key": "$KLAVIYO_API_KEY"}
  }'

# 3. Create sync (model → destination mapping)
curl -X POST "https://api.hightouch.com/api/v1/syncs" \
  -H "Authorization: Bearer $HIGHTOUCH_API_KEY" \
  -d '{
    "model_id": "MODEL_ID",
    "destination_id": "DEST_ID",
    "config": {
      "object": "list",
      "list_name": "PQL High",
      "mappings": {
        "email": "email",
        "first_name": "first_name",
        "$first_name": "first_name",
        "pql_score": "pql_score",
        "plan_tier": "plan_tier"
      },
      "mode": "upsert"
    },
    "schedule": {"type": "cron", "cron": "0 */4 * * *"}  // every 4 hours
  }'
```

### Recipe 2: Hightouch — Facebook Custom Audience

```bash
curl -X POST "https://api.hightouch.com/api/v1/syncs" \
  -H "Authorization: Bearer $HIGHTOUCH_API_KEY" \
  -d '{
    "model_id": "HIGH_LTV_MODEL_ID",
    "destination_id": "FB_DEST_ID",
    "config": {
      "object": "custom_audience",
      "audience_name": "High LTV ($500+) — last 90d",
      "mappings": {
        "email": "email_sha256",  // Facebook requires SHA-256 hash
        "phone": "phone_sha256",
        "external_id": "user_id"
      },
      "mode": "replace"
    },
    "schedule": {"type": "cron", "cron": "0 6 * * 1"}  // weekly Mondays 6am
  }'
```

### Recipe 3: Hightouch — HubSpot contact enrichment

```bash
curl -X POST "https://api.hightouch.com/api/v1/syncs" \
  -H "Authorization: Bearer $HIGHTOUCH_API_KEY" \
  -d '{
    "model_id": "USER_FEATURES_MODEL",
    "destination_id": "HUBSPOT_DEST_ID",
    "config": {
      "object": "contact",
      "mappings": {
        "email": "email",
        "pql_score": "custom_pql_score",  // custom HubSpot property
        "last_active_at": "custom_last_active_date",
        "feature_adoption_count": "custom_feature_adoption_count",
        "monthly_revenue": "custom_mrr"
      },
      "mode": "upsert"
    },
    "schedule": {"type": "cron", "cron": "*/15 * * * *"}  // every 15 min
  }'
```

### Recipe 4: Census (now Fivetran) — same pattern

```bash
curl -X POST "https://app.getcensus.com/api/v1/syncs" \
  -H "Authorization: Bearer $CENSUS_API_TOKEN" \
  -d '{
    "label": "Warehouse → Customer.io",
    "operation": "upsert",
    "source": {"connection_id": "snowflake_001", "object": "models/pql_high"},
    "destination": {"connection_id": "customerio_001", "object": "customers"},
    "schedule_frequency": "hourly"
  }'
```

### Recipe 5: Polytomic for SaaS embedded

```bash
# Embed reverse-ETL into your own SaaS for your customers
curl -X POST "https://app.polytomic.com/api/syncs" \
  -H "Authorization: Bearer $POLYTOMIC_API_KEY" \
  -d '{
    "name": "Customer warehouse → their CRM",
    "source": {"type": "tenant_warehouse", "tenant_id": "{{customer_id}}"},
    "destination": {"type": "salesforce"},
    "mappings": {...}
  }'
```

Polytomic supports multi-tenant — each of YOUR customers has their own warehouse + sync.

### Recipe 6: Warehouse model SQL pattern

```sql
-- analytics.pql_high model (in Snowflake)
CREATE OR REPLACE VIEW analytics.pql_high AS
SELECT
  u.user_id,
  u.email,
  u.first_name,
  u.company,
  s.pql_score,
  s.signals_array,
  u.plan_tier,
  u.last_active_at,
  u.monthly_revenue
FROM users u
JOIN scores s ON s.user_id = u.user_id
WHERE s.pql_score >= 70
  AND u.last_active_at > CURRENT_DATE - 7
  AND u.lifecycle_stage = 'lead'
```

Hightouch / Census points at this view. Update the view; sync auto-picks up changes.

### Recipe 7: Sync latency vs use case

| Use case | Acceptable latency | Schedule |
|---|---|---|
| Trigger in-app message | < 5 min | Streaming or 5-min cron |
| PQL → CRM | < 30 min | 15-min cron |
| Email audience | < 4 hours | Hourly to 4-hourly cron |
| Ad audience | Daily | Daily |
| Finance rollup | Daily | Daily |

### Recipe 8: Identity matching

```text
Hightouch / Census handle identity matching by primary_key (e.g., email).

If destination is Facebook → SHA-256 hash email + phone for matching.
If destination is Klaviyo → use email as upsert key.
If destination is HubSpot → use email + create-if-missing.

Test in destination's "audience overlap" UI before full launch.
```

### Recipe 9: Trigger sync on schema change

```bash
# Webhook from warehouse (dbt run completion) → trigger Hightouch sync
curl -X POST "https://api.hightouch.com/api/v1/syncs/SYNC_ID/runs" \
  -H "Authorization: Bearer $HIGHTOUCH_API_KEY"
```

Couple with dbt CI/CD: model build → run tests → trigger downstream syncs.

### Recipe 10: Cost optimization

```text
Reverse-ETL pricing usually = monthly active records synced.

To reduce cost:
1. Filter aggressively — only sync who needs to be in destination
2. Don't sync stale records (filter by last_active_at)
3. Use full-sync only when necessary; usually incremental
4. Combine related models into one sync (multi-mapping)
5. RudderStack OSS = self-host; $0 marginal
```

### Recipe 11: Monitoring + alerts

```python
# Hightouch API — get last 7 sync runs per sync
syncs = requests.get(
    f"https://api.hightouch.com/api/v1/syncs/{sync_id}/runs?limit=7",
    headers={"Authorization": f"Bearer {HIGHTOUCH_API_KEY}"}
).json()

failed = [r for r in syncs["runs"] if r["status"] == "failed"]
if failed:
    slack.send("#data-alerts", f"Hightouch sync {sync_id} failed {len(failed)}x in last 7 runs")
```

## Examples

### Example 1: PostHog → Klaviyo via Hightouch (PQL high audience)

1. PostHog cohort "PQL High" exported nightly to Snowflake (or PostHog → warehouse via Fivetran).
2. Snowflake view `analytics.pql_high` (Recipe 6).
3. Hightouch model + Klaviyo destination (Recipe 1).
4. Schedule: hourly.
5. Klaviyo flow: "PQL High Welcome" triggers on list add.

### Example 2: Salesforce CRM enrichment

Source: warehouse `users` with computed product signals.
Destination: Salesforce contact custom fields.
Schedule: every 15 min.

Recipient: AEs see in-product behavior in Salesforce account view.

### Example 3: Facebook Custom Audience for retargeting

Source: warehouse `high_ltv_active` (purchased $500+ in last 90d).
Destination: Facebook Custom Audience.
Schedule: weekly.

Use case: paid retargeting + lookalike modeling.

## Edge cases / gotchas

- **Sync deletes destination data** — full-sync overwrites destination list. Use upsert mode + carefully define primary_key.
- **Race conditions w/ destination's own changes** — if destination tool (e.g., Klaviyo) has user-edit, sync may overwrite. Define source-of-truth contract.
- **Schema drift** — warehouse columns change; sync breaks silently. Use dbt + tests.
- **Hashing for ad platforms** — Facebook / TikTok / Google require SHA-256 hashed email + phone. Use Hightouch's built-in hash transform.
- **PII leak** — syncing internal data to external tool = compliance risk. Audit who has access.
- **Cost from over-sync** — incremental syncs save $$; full-sync inflates MTU.
- **Real-time vs near-real-time** — reverse-ETL is typically NOT real-time; latency 5min-4h. For < 1s triggers, use event-based CDP.
- **Identity match failure** — emails change; user_ids fork. Track match rate; alert on degradation.
- **GDPR — right-to-delete propagation** — if deleted in warehouse, must propagate to all destinations. Hightouch supports delete-mode.
- **Sandbox / test sync mode** — don't run new syncs on prod without dry-run.
- **Multi-tenant SaaS** — for embedded use case, Polytomic > Hightouch.
- **Census migration** — Fivetran acquired May 2025; some legacy API endpoints deprecating. Check before relying.

## Sources

- Hightouch docs: https://hightouch.com/docs/reverse-etl
- Census docs (Fivetran-namespaced now): https://docs.getcensus.com/
- Polytomic: https://www.polytomic.com/
- RudderStack Reverse ETL: https://www.rudderstack.com/docs/reverse-etl/
- RudderStack vs Hightouch vs Census: https://www.rudderstack.com/competitors/hightouch-vs-census/
- Domo — best reverse-ETL: https://www.domo.com/learn/article/best-reverse-etl-platforms
- Integrate.io — Census review: https://www.integrate.io/blog/census-review/
- Gartner MQ Customer Data Platforms: https://hightouch.com/blog/gartner-2024-magic-quadrant-cdp
