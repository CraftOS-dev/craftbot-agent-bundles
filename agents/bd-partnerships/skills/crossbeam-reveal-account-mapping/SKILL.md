<!--
Source: https://crossbeam.com/docs/api + https://docs.reveal.co/ + https://www.snowflake.com/blog/native-apps-collaboration/
Crossbeam + Reveal + Snowflake account mapping for co-sell motion (June 2026 SOTA).
-->
# Crossbeam + Reveal Account Mapping — SKILL

Run **secure, privacy-preserving account overlap** between two companies' CRMs to surface shared customers, shared opportunities, and outbound targets. **Crossbeam** = 650K+ companies, US-leading. **Reveal** = European-leaning alternative. **Snowflake Native Apps / Data Clean Room** = warehouse-native for data-mature partners. Output drives joint-GTM motion, outbound list, joint pipeline.

## When to use

- **Onboarding new strategic partner** — first overlap report.
- **Joint-target-account list build** — for ABM motions with partner.
- **Joint pipeline review** — accounts in active opps on both sides.
- **Co-marketing audience sizing** — overlap = shared audience.
- **Lapsed customer re-engagement** — their customer that we lost / our customer that they lost.
- **Trigger phrases**: "account mapping with X", "Crossbeam overlap", "joint target accounts", "shared customers count", "Reveal report", "Snowflake clean room".

Do NOT use this skill for: **direct-sales prospect list build** (use `sales-agent`'s `account-research-deep`); **the co-sell sales motion itself** (use `sales-agent`); **CRM hygiene** (use `partnerstack-tackle-channel-management`); **partner sourcing** (use `partner-sourcing-icp-definition`).

## Setup

```bash
export MATON_API_KEY="<key>"
export CROSSBEAM_API_KEY="<key>"       # if direct, not via Maton
export REVEAL_API_KEY="<key>"
# Snowflake: postgresql-mcp configured against Snowflake endpoint
export SNOWFLAKE_CONN_STR="snowflake://user:pass@account/db/schema?warehouse=wh"
```

**One-time setup:**
- Crossbeam Free Tier or Connector tier — sign up at crossbeam.com
- Connect HubSpot / Salesforce
- Invite each partner; partner accepts; first overlap report generated automatically
- Snowflake Native Apps requires both sides on Snowflake

## Common recipes

### Recipe 1: Crossbeam — list partners + invite new

```bash
# List currently connected partners
curl "https://gateway.maton.ai/crossbeam/v0.3/partners" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq '.partners[] | {id, name, status}'

# Invite a new partner
curl -X POST "https://gateway.maton.ai/crossbeam/v0.3/partners/invitations" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "partner_company_name": "Acme Analytics",
    "partner_invitee_email": "sarah@acme.com",
    "message": "Excited to map accounts; first report should be ready within 24h after you accept."
  }'
```

Reference: https://crossbeam.com/docs/api.

### Recipe 2: Crossbeam — define population (filtered subset of your CRM)

```bash
# Population = filtered view of your records (e.g., active customers only)
curl -X POST "https://gateway.maton.ai/crossbeam/v0.3/populations" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name": "Active Customers",
    "source_id": "<hubspot-source-id>",
    "filters": [
      {"field":"customer_status","operator":"equals","value":"active"}
    ],
    "shared_with_partners": ["acme-partner-id"]
  }'

# Other populations to define:
# - "Open Opportunities"
# - "Recently Churned (last 90d)"
# - "Prospects in active sequence"
```

### Recipe 3: Crossbeam — generate overlap report

```bash
curl -X POST "https://gateway.maton.ai/crossbeam/v0.3/reports" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name": "Q3 Brand × Acme — Customers Overlap",
    "your_populations": ["<active-customers-pop-id>"],
    "partner_id": "acme-partner-id",
    "partner_populations": ["<their-active-customers-pop-id>"],
    "overlap_type": "AND"
  }'
```

`overlap_type` values:
- `AND` — accounts in BOTH populations (joint customers)
- `LEFT` — accounts in your population NOT in partner's (your customer, not theirs)
- `RIGHT` — accounts in partner's population NOT in yours (their customer, not yours)

### Recipe 4: Crossbeam — pull overlap report results

```bash
curl "https://gateway.maton.ai/crossbeam/v0.3/reports/<report-id>/results?limit=500" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq '.matches[] | {
    company_name,
    your_record_url,
    partner_record_url,
    your_account_owner_email,
    partner_account_owner_email,
    matched_on
  }'
```

Output a CSV; ingest into CRM as account tags.

### Recipe 5: Crossbeam — population analytics

```bash
curl "https://gateway.maton.ai/crossbeam/v0.3/reports/<report-id>/analytics" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq '{
    total_matches,
    matched_accounts,
    estimated_pipeline_uplift,
    geographies: .breakdown.country,
    segments: .breakdown.employee_range
  }'
```

### Recipe 6: Reveal — partner CRUD + report (European partners)

```bash
# Reveal API equivalent
curl "https://gateway.maton.ai/reveal/v1/partners" \
  -H "Authorization: Bearer $MATON_API_KEY"

curl -X POST "https://gateway.maton.ai/reveal/v1/overlaps" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "partner_id":"acme-partner-id",
    "your_segment_filter":"active_customer",
    "their_segment_filter":"active_customer"
  }'
```

Reference: https://docs.reveal.co/.

### Recipe 7: Snowflake Native App — data clean room

For data-mature partners; both on Snowflake; privacy-preserving join.

```sql
-- 1. Vendor provisions native app via Snowflake Marketplace
-- 2. Partner installs from Snowflake Marketplace
-- 3. Both sides expose tables via Application Package
-- 4. Vendor queries joined results (neither side sees raw rows)

-- Example: shared-customers query
SELECT
  COUNT(DISTINCT v.account_name) AS overlap_count,
  AVG(v.arr) AS avg_arr_vendor,
  AVG(p.arr) AS avg_arr_partner
FROM vendor_accounts v
INNER JOIN partner_accounts p ON v.normalized_domain = p.normalized_domain;
-- The native app returns only the aggregated results, not the raw account names
```

Snowflake Data Clean Room patterns: https://www.snowflake.com/blog/native-apps-collaboration/.

### Recipe 8: CSV-fallback overlap (free; works without any tool)

```bash
# Free fallback when no Crossbeam/Reveal/Snowflake
# Both sides export account-CSV with hashed normalized domain
python -c "
import hashlib
domain = 'acme.com'
salt = 'pre-agreed-salt-2026-08-15'
h = hashlib.sha256((domain.lower().strip() + salt).encode()).hexdigest()
print(h)
"

# Step 1: both sides hash own domain list with same salt
# Step 2: exchange CSVs
# Step 3: intersection → match count
# Privacy: hashed, salt-protected; no raw domains exchanged
```

Works for first-overlap-only; for ongoing tracking, upgrade to Crossbeam free tier.

### Recipe 9: Output to CRM as account tags

```bash
# For each matched account, tag in HubSpot
for ACCOUNT in $(jq -r '.matches[].company_name' overlap.json); do
  COMPANY_ID=$(curl "https://gateway.maton.ai/hubspot/crm/v3/objects/companies/search" \
    -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
    -d "{\"filterGroups\":[{\"filters\":[{\"propertyName\":\"name\",\"operator\":\"EQ\",\"value\":\"$ACCOUNT\"}]}]}" | jq -r '.results[0].id')

  curl -X PATCH "https://gateway.maton.ai/hubspot/crm/v3/objects/companies/$COMPANY_ID" \
    -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
    -d "{\"properties\":{\"partner_overlap_acme\":\"customer_match\",\"partner_overlap_last_updated\":\"$(date -u +%Y-%m-%d)\"}}"
done
```

### Recipe 10: Co-sell motion — joint-target prioritization

```yaml
joint_target_motion:
  list_build:
    overlap_AND: "Joint customers — expansion + cross-sell"
    overlap_LEFT_partner_target: "Your customers in partner ICP — partner can sell to them"
    overlap_RIGHT_vendor_target: "Their customers in your ICP — you can sell to them"
    overlap_neither_AND_joint_ICP: "Net-new prospects shared by ICP — joint outbound"
  prioritization:
    tier_1: "Joint open opportunities (highest priority)"
    tier_2: "Joint customer expansion targets"
    tier_3: "Your customer, partner ICP (warm intros via you)"
    tier_4: "Their customer, your ICP (warm intros via them)"
  motion:
    - "Tier 1 → joint pursuit; co-pitch within 14 days"
    - "Tier 2 → joint expansion pitch via CSMs"
    - "Tier 3 → BD warms; partner takes over for pitch"
    - "Tier 4 → partner warms; you take over for pitch"
```

### Recipe 11: Overlap report scheduling (recurring sync)

```bash
# Crossbeam reports refresh daily by default; explicit refresh:
curl -X POST "https://gateway.maton.ai/crossbeam/v0.3/reports/<report-id>/refresh" \
  -H "Authorization: Bearer $MATON_API_KEY"

# Weekly cron: refresh + post counts to Slack
cat <<'PYEOF' | python3
import requests, os, json
report_id = "<id>"
r = requests.get(f"https://gateway.maton.ai/crossbeam/v0.3/reports/{report_id}/analytics",
                 headers={"Authorization": f"Bearer {os.environ['MATON_API_KEY']}"})
data = r.json()
msg = f":bar_chart: Crossbeam — {data['name']}: {data['total_matches']} matches"
requests.post(f"https://slack.com/api/chat.postMessage",
              headers={"Authorization": f"Bearer {os.environ['SLACK_TOKEN']}"},
              json={"channel":"#partner-acme","text":msg})
PYEOF
```

### Recipe 12: Joint-GTM dashboard (Google Sheets)

```yaml
dashboard_columns:
  - "Account name"
  - "Vendor owner (CSM/AE)"
  - "Partner owner (their CSM/AE)"
  - "Overlap type (joint customer / joint pipeline / partner-target / vendor-target)"
  - "Joint pipeline amount (if any)"
  - "Last activity vendor side"
  - "Last activity partner side"
  - "Next-step (joint-pitch scheduled / intro pending / nurture)"
  - "Tier (1-4 per Recipe 10)"

sync_cadence: "Weekly Mon 9am from Crossbeam → CSV → Google Sheets"
review_cadence: "Weekly Wed 30-min joint stand-up"
```

## Examples

### Example 1: First overlap report with new partner

**Goal:** Acme partnership signed; need first overlap report.

**Steps:**
1. Day 1 — Recipe 1 — Invite Acme via Crossbeam.
2. Day 2 — Acme accepts.
3. Day 2 — Recipe 2 — Define populations on both sides.
4. Day 2 — Recipe 3 — Generate AND, LEFT, RIGHT overlap reports.
5. Day 3 — Recipe 5 — Read analytics: 60 joint customers, 240 your-not-theirs, 180 theirs-not-yours.
6. Day 3 — Recipe 4 — Pull match details to CSV.
7. Day 4 — Recipe 10 — Tier 1-4 prioritization.
8. Day 5 — Joint stand-up to align on top-30 joint-target list.

**Result:** Joint motion live within a week; 60 expansion targets + 30 prioritized co-sell prospects.

### Example 2: ABM campaign with partner

**Goal:** Joint paid ABM on 50 highest-value joint targets.

**Steps:**
1. Recipe 4 — Pull top-50 joint targets (AND or joint-ICP overlap).
2. Recipe 9 — Tag in CRM as `joint_abm_acme_q3`.
3. Cross-hand to `marketing-agent`: feed list to LinkedIn ABM + Meta Custom Audiences.
4. Recipe 12 — Track per-account engagement.
5. 90 days later: pipeline + closed-won analysis tied back to ABM exposure.

**Result:** Joint ABM 2-3x conversion vs single-vendor ABM; partner contribution measured.

### Example 3: Free-tier CSV-hash fallback (early-stage)

**Goal:** Founder-led BD; no Crossbeam budget yet; first partnership wants overlap visibility.

**Steps:**
1. Recipe 8 — Both sides hash own customer-domain list with shared salt.
2. Exchange CSVs.
3. Intersection: 22 joint customers identified.
4. Manual outreach to top 5 joint customers for case-study eligibility.
5. Outcome drives Crossbeam paid-tier purchase.

**Result:** Partnership unblocked without tooling investment; ROI proven before purchase.

## Edge cases / gotchas

- **Free tier limits** — Crossbeam Connector tier: limited reports + 1 partner. Real use of joint-GTM motion = paid tier.
- **Domain normalization** — `acme.com`, `acme.co`, `acme.com/`, `ACME.COM` all the same. Normalize lowercase + strip path + strip www.
- **Multi-brand parents** — Acme owns Globex; their CRM has both. Match by parent company UUID + domain list.
- **Subsidiary detection** — same parent, different domains; matched on `acme.com` will miss `acme-eu.com`. Crossbeam handles via "Account Groups."
- **Privacy / legal** — both sides must consent to data sharing; Crossbeam has explicit consent flow. EU partners need DPA.
- **Stale data** — both sides' CRMs lag; overlap can include stale records. Refresh weekly.
- **Population definition mismatch** — "customer" definition differs across teams. Pre-discuss.
- **Overlap inflation** — same account in 5 populations; double-counts unless de-duped.
- **Joint customer disagreement** — Vendor thinks Acme is a customer; Acme records show "lost." Crossbeam exposes the data difference for discussion.
- **Pricing tier vs scale** — Crossbeam pricing scales with population size; reduce population by tightening filters before scaling.
- **Reveal vs Crossbeam choice** — Crossbeam wins US scale (650K+ companies); Reveal wins EU + free tier depth.
- **Snowflake Native Apps require Snowflake on both sides** — viable for data-mature; overkill for SMB.
- **CSV-hash fallback** has limitations — only single-overlap snapshot; no ongoing tracking; no rich match metadata.
- **Cross-CRM mappings** — vendor on HubSpot, partner on Salesforce: Crossbeam handles via connectors; both connect their own CRM.
- **Hubspot + Salesforce sync lag** — Crossbeam pulls every 24h; for daily-pipeline accuracy enable real-time webhooks (paid tier).
- **Account-owner email accuracy** — Crossbeam shows account owner; if your CRM has stale owner data, the joint motion misroutes.
- **Joint-pipeline vs joint-customer** — "Joint open opportunity" is the highest-value overlap; not all overlaps are equal.
- **Overlap fatigue** — large overlap (1000+ matches) is unmanageable. Filter by ICP + engagement freshness before joint motion.
- **Co-sell competitor risk** — vendor's competitor is the same partner's partner; overlap data could leak strategy. Partner-side trust check before sharing populations.

## Sources

- Crossbeam API: https://crossbeam.com/docs/api
- Crossbeam Reports endpoint: https://crossbeam.com/docs/api#tag/Reports
- Crossbeam Populations: https://crossbeam.com/docs/api#tag/Populations
- Reveal docs: https://docs.reveal.co/
- Snowflake Native Apps: https://www.snowflake.com/blog/native-apps-collaboration/
- Snowflake Data Clean Rooms: https://docs.snowflake.com/en/user-guide/cleanrooms
- Crossbeam Partnership Economy: https://www.crossbeam.com/blog/the-partnership-economy/
- Account mapping best practices: https://www.crossbeam.com/blog/account-mapping-101/
- PartnerTap (alternative): https://www.partnertap.com/
