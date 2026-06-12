<!--
Source: https://docs.aws.amazon.com/marketplace-catalog/latest/api-reference/ + https://learn.microsoft.com/en-us/partner-center/marketplace/ + https://cloud.google.com/marketplace/docs/partners + https://tackle.io/api-documentation
Cloud marketplace listings via Tackle + native cloud catalog APIs (June 2026 SOTA).
-->
# AWS / Azure / GCP Marketplace Listings — SKILL

Publish (and maintain) SaaS listings on AWS Marketplace, Azure Marketplace, and GCP Marketplace. The SOTA orchestrator across all three is **Tackle.io** (single dashboard, private-offer generation, ACE/Co-Sell sync). For direct control or non-Tackle teams, each cloud has its own CLI + Catalog API.

## When to use

- **Launching SaaS on AWS / Azure / GCP Marketplace** — new listing end-to-end.
- **Publishing a Private Offer / CPPO** — custom-priced contract for a specific buyer, often co-sell.
- **Updating listing assets** — pricing, dimensions, marketing collateral, video.
- **Sync co-sell opportunity to ACE / Microsoft Co-Sell / Google Partner Advantage**.
- **Quarterly marketplace health review** — sales velocity, listing-asset freshness, contract expirations.
- **Trigger phrases**: "list on AWS Marketplace", "publish Azure SaaS offer", "GCP Marketplace listing", "private offer for X", "CPPO", "Co-Sell Ready", "Tackle".

Do NOT use this skill for: **SaaS marketplaces other than the big-3 cloud** (use `salesforce-appexchange-listing` or `hubspot-shopify-slack-marketplace-listings`); **billing reconciliation** (defer to `finance-controller`); **seller-registration KYC** (one-time human task).

## Setup

```bash
# One-time human tasks (cannot be automated)
# - AWS: Seller registration via AWS Marketplace Management Portal + tax/bank info
# - Azure: Partner Center enrollment + Microsoft Partner Network ID (MPN ID)
# - GCP: Cloud Identity verification + Producer Portal access

# CLI / SDK
aws --version              # AWS CLI v2.15+
az --version               # Azure CLI 2.55+
gcloud --version           # gcloud CLI 460+

# Auth
aws configure              # use seller-admin IAM credentials
az login                   # Partner Center tenant
gcloud auth login

# Tackle (SOTA orchestrator) via Maton
export MATON_API_KEY="<key>"
# Tackle pricing: ~$30k/yr starter, $80k+ enterprise — but unifies all 3 clouds
```

## Common recipes

### Recipe 1: Tackle — create private offer (AWS, single API call across clouds)

```bash
curl -X POST "https://gateway.maton.ai/tackle/v3/offers/private-offer" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "cloud":"aws",
    "buyer_account_id":"123456789012",
    "product_id":"<aws-marketplace-product-id>",
    "currency":"USD",
    "term_units":[
      {"start_date":"2026-07-01","end_date":"2027-06-30","amount":150000}
    ],
    "service_dimensions":[
      {"sku":"seats","dimension":"users","quantity":100,"unit_price":1500}
    ],
    "payment_schedule":[
      {"due_date":"2026-07-15","amount":75000},
      {"due_date":"2027-01-15","amount":75000}
    ],
    "metadata":{"hubspot_deal_id":"<deal-id>","ace_opportunity_id":"<aws-ace-opp-id>"}
  }'
```

Tackle handles the per-cloud SDK plumbing; same JSON works for `azure` or `gcp` cloud values.

### Recipe 2: AWS Marketplace Catalog API — direct listing update

```bash
# Describe current entity (product) state
aws marketplace-catalog describe-entity \
  --catalog AWSMarketplace \
  --entity-id <product-entity-id>

# Build change-set for pricing update
cat > /tmp/pricing-change.json <<'EOF'
{
  "Catalog": "AWSMarketplace",
  "ChangeSet": [{
    "ChangeType": "UpdateInformation",
    "Entity": {"Type":"SaaSProduct@1.0","Identifier":"<product-id>"},
    "Details": "{\"Description\":{\"ProductTitle\":\"Brand Analytics\",\"ShortDescription\":\"Real-time analytics for SaaS revenue teams\"}}"
  }]
}
EOF

aws marketplace-catalog start-change-set --cli-input-json file:///tmp/pricing-change.json
```

Doc: https://docs.aws.amazon.com/marketplace-catalog/latest/api-reference/welcome.html.

### Recipe 3: AWS Channel Partner Private Offer (CPPO)

```bash
# CPPO = AWS Marketplace private offer routed through channel partner (resold)
# The vendor authorizes the channel partner; channel partner generates the offer

# Vendor authorizes channel partner one-time:
aws marketplace-catalog start-change-set \
  --catalog AWSMarketplace \
  --change-set '[{
    "ChangeType":"CreateChannelPartnerOffer",
    "Entity":{"Type":"SaaSProduct@1.0","Identifier":"<product-id>"},
    "Details":"{\"ChannelPartnerAccountId\":\"<partner-aws-account>\",\"ChannelPartnerRole\":\"CP_RESELLER\"}"
  }]'
```

Reference: https://docs.aws.amazon.com/marketplace/latest/userguide/channel-partner-private-offers.html.

### Recipe 4: AWS ACE — push co-sell opportunity

```bash
# ACE = APN Customer Engagements; co-sell pipeline sync to AWS sellers
# Best done via Tackle (handles CRM-to-ACE mapping); direct via Partner Central API:
curl -X POST "https://partnercentral-selling.us-east-1.api.aws/v1/opportunities" \
  -H "Authorization: AWS4-HMAC-SHA256 ..." \
  -d '{
    "customer":{"account":{"name":"Acme Inc","duns":"123456789"}},
    "project":{"description":"Acme rolling out Brand on AWS","customerBusinessProblem":"Need real-time revenue analytics"},
    "primaryContact":{"emailAddress":"sarah@acme.com","firstName":"Sarah","lastName":"Lee"},
    "lifecycle":{"stage":"Qualified"},
    "marketing":{"source":"Partner","awsFundingUsed":"No"}
  }'
```

Tackle is *strongly* recommended for ACE — manually pushing ACE is brittle and high-error-rate.

### Recipe 5: Azure Marketplace — Partner Center API SaaS offer create

```bash
# Auth via Microsoft Graph
ACCESS_TOKEN=$(curl -X POST https://login.microsoftonline.com/<tenant>/oauth2/v2.0/token \
  -d "client_id=$AZURE_CLIENT_ID&client_secret=$AZURE_CLIENT_SECRET&grant_type=client_credentials&scope=https%3A%2F%2Fapi.partner.microsoft.com%2F.default" \
  | jq -r '.access_token')

# Create SaaS offer
curl -X POST "https://api.partner.microsoft.com/v1.0/ingestion/products" \
  -H "Authorization: Bearer $ACCESS_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "resourceType":"AzureSaaSApplication",
    "name":"brand-analytics",
    "externalIDs":[{"type":"MPNID","value":"<your-mpn>"}],
    "isModularPublishing":true
  }'
```

Then PATCH `/products/<id>/listings`, `/products/<id>/plans` for plan + pricing.

Reference: https://learn.microsoft.com/en-us/partner-center/marketplace/api/.

### Recipe 6: Azure — MACC eligibility flag

```yaml
# MACC = Microsoft Azure Consumption Commitment
# Customers with MACC get marketplace spend counted toward their commit
# To be MACC-eligible:
azure_macc_checklist:
  - "Listed as SaaS offer in Azure Marketplace (Recipe 5)"
  - "Transactable through marketplace (not just listing)"
  - "MACC-eligible flag in offer setup → Marketplace tab"
  - "Co-Sell Ready status (Co-sell Ready / IP Co-Sell preferred)"
```

When MACC-eligible, you appear in customer's Azure portal "ways to use your commit" — huge driver of deals.

### Recipe 7: Azure — Co-Sell Ready / IP Co-Sell

```yaml
# Co-Sell Ready unlocks Microsoft seller co-selling
co_sell_ready_requirements:
  - "Transactable SaaS offer in Marketplace"
  - "Marketing materials: 1-pager + customer references + reference architecture"
  - "Solution overview deck (10-15 slides)"
  - "Validated customer wins (≥2 production customers in azure)"
  - "Joint case study (≥1)"
  - "Submit via Partner Center → Co-sell options → submit for review"
```

Submitting via Partner Center is currently a portal flow (Playwright if automating).

### Recipe 8: GCP Marketplace — Producer Portal listing via gcloud

```bash
# Verify Cloud Identity + Marketplace producer role
gcloud auth list

# Submit solution definition (YAML manifest)
cat > /tmp/gcp-solution.yaml <<'EOF'
apiVersion: marketplace.cloud.google.com/v1
kind: Solution
metadata:
  name: brand-analytics
spec:
  publisher: brand
  shortDescription: "Real-time analytics for SaaS revenue teams"
  longDescription: "..."
  categories: [analytics, business-intelligence]
  pricing:
    - planId: standard
      pricePerUserMonth: 1500
EOF

gcloud marketplace solutions create brand-analytics \
  --solution-file=/tmp/gcp-solution.yaml \
  --producer-project=<your-gcp-project>
```

Reference: https://cloud.google.com/marketplace/docs/partners.

### Recipe 9: GCP — integrated billing setup

```bash
# Customer pays via their GCP billing account; you receive payout via Cloud Billing
# Onboard via Producer Portal once; then per-listing flag:
gcloud marketplace solutions update brand-analytics \
  --integrated-billing=enabled \
  --billing-model=usage-based
```

Integrated billing is the SOTA model — customer doesn't separately negotiate; you appear on their GCP invoice.

### Recipe 10: Listing-asset bundle (common across all 3 clouds)

```yaml
# Build once, reuse across clouds (with platform-specific tweaks)
listing_assets:
  logo: "<= 300x300px, transparent PNG, brand-only no taglines"
  hero_image: "1920x1080 PNG, product UI screenshot, light theme"
  screenshots:
    - "Dashboard view 1280x720"
    - "Pricing dashboard 1280x720"
    - "Settings panel 1280x720"
  demo_video: "YouTube unlisted URL, 60-120s, 1080p"
  short_description: "120 chars max — appears in search results"
  long_description: "300-500 words; what + who-for + key value props (3-5 bullets) + pricing model"
  key_features: "5-7 bullets, ≤ 60 chars each"
  pricing_tiers:
    - {name:"Starter",dimensions:"5 users",price:"$1500/user/yr"}
    - {name:"Growth",dimensions:"25 users",price:"$1200/user/yr (volume)"}
    - {name:"Enterprise",dimensions:"Custom",price:"Contact sales"}
  contact: "support email, phone, support URL"
  legal: "EULA URL or upload; Privacy policy URL"
```

Render with `imagegen-mcp` for screenshots, `canva-mcp` for hero, `pdf` for EULA.

### Recipe 11: Asset checklist + readiness gate

```python
def listing_ready(cloud, assets):
    required = {
        "aws":  ["logo","hero","short_desc","long_desc","screenshots","pricing","support_url","eula","privacy"],
        "azure":["logo","hero","short_desc","long_desc","screenshots","video","pricing","mpn_id","privacy","tou"],
        "gcp":  ["logo","short_desc","long_desc","screenshots","integrated_billing","cloud_identity"],
    }
    missing = [r for r in required[cloud] if r not in assets]
    if missing: raise ValueError(f"{cloud} listing missing: {missing}")
    return True
```

Run before any `start-change-set`. Marketplace reviewers reject incomplete bundles immediately.

### Recipe 12: Status / health monitoring

```bash
# AWS — list pending change-sets
aws marketplace-catalog list-change-sets \
  --catalog AWSMarketplace --filter-list 'Name=Status,ValueList=APPLYING,PREPARING,REVIEW'

# Azure — get offer status
curl "https://api.partner.microsoft.com/v1.0/ingestion/products/<id>" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq '.status'

# GCP — list solutions
gcloud marketplace solutions list --producer-project=<your-project>
```

Schedule weekly via `postgresql-mcp` cron → digest to `slack-mcp` `#marketplace`.

## Examples

### Example 1: New AWS Marketplace SaaS listing via Tackle

**Goal:** SaaS company launching on AWS Marketplace; first listing; want fast time-to-listing without learning Catalog API.

**Steps:**
1. Day 0 — One-time AWS Seller registration via portal; tax/bank info; ~3 days to approval.
2. Day 3 — Asset bundle assembled (Recipe 10); reviewed in Notion checklist.
3. Day 4 — Tackle.io onboarding (orchestrator); listing definition entered in Tackle UI.
4. Day 5-7 — AWS Marketplace review (~7-14 days for SaaS).
5. Day 14 — Listing live; Recipe 1 used for first private offer to design partner.

**Result:** Tackle abstracts the Catalog API + ACE plumbing; team focuses on commercial motion, not API plumbing.

### Example 2: Private offer for enterprise buyer with custom pricing

**Goal:** Enterprise buyer wants $250K/yr custom contract via AWS Marketplace (so it counts against their EDP commit).

**Steps:**
1. AE qualifies deal in CRM; flags "marketplace private offer required."
2. Recipe 1 — Tackle creates private offer with custom dimensions + payment schedule.
3. AE shares the AWS-generated buyer URL with the buyer; buyer accepts in AWS portal.
4. On acceptance, Tackle webhook → HubSpot deal → `closedwon` + `marketplace_listing_id`.
5. `finance-controller` notified for revenue rec.

**Result:** $250K deal closes via marketplace; counts against buyer EDP; no procurement friction.

### Example 3: Co-Sell Ready submission to Microsoft

**Goal:** Already listed on Azure Marketplace; want to unlock Microsoft seller co-sell.

**Steps:**
1. Recipe 10 — Build assets including reference architecture diagram (`drawio-mcp`).
2. Customer references list: ≥2 production-deployed Azure customers + 1 case study.
3. Submit via Partner Center → Co-sell options (Playwright if automating).
4. 4-8 week Microsoft review.
5. Granted "Co-Sell Ready" status; Microsoft sellers add to their co-sell deck rotation.

**Result:** Microsoft sellers actively pitching joint deals; co-sell pipeline 2-3x organic marketplace pipeline.

## Edge cases / gotchas

- **Seller registration is human + KYC** — 3-10 days. Can't be automated; budget for this in launch timeline.
- **AWS Catalog API change-sets are async** — `start-change-set` returns immediately; actual application takes hours-to-days. Poll via `list-change-sets`.
- **AWS Marketplace SaaS contracts vs subscriptions** — Contracts = annual commit, simpler; Subscriptions = metered, more API surface. Pick deliberately; SaaS Contracts cover 80% of cases.
- **CPPO requires both vendor + channel partner have AWS Marketplace accounts** — pre-flight check.
- **Azure Partner Center API uses two different auth flows** — old Cloud Partner Portal API (deprecated) vs new Partner Center API. Use new only.
- **Azure SaaS offers require validation against your auth endpoint** during purchase flow — non-trivial backend work; not just listing.
- **MACC eligibility ≠ Co-Sell Ready** — separate flags; MACC = customer can use their Azure commit; Co-Sell Ready = Microsoft sellers earn quota credit. Get both.
- **GCP Marketplace requires Cloud Identity** — your company must have Workspace or Cloud Identity verified.
- **GCP "integrated billing" requires deeper integration** than just listing — your service must accept Cloud Marketplace entitlement tokens on every API request.
- **Tackle.io cost is $30k-100k+/yr** — for solo founders, sometimes direct cloud-CLI is more economical until $1M+ marketplace ARR. Re-evaluate quarterly.
- **Private-offer pricing can't be edited after acceptance** — generate carefully. Voids count against quotas.
- **Marketplace fees vary**: AWS 3-5% fee on SaaS contracts; Azure 3% (down from earlier); GCP 3%. Build into pricing model.
- **ACE / Co-Sell opportunity sync is fragile** without Tackle — duplicate opportunities, sync conflicts. Tackle de-dupes and reconciles.
- **Listing-asset rejection** is the most common reason for review delay. Pre-review against Recipe 11 checklist.
- **EULA / Privacy URLs must be accessible** at submission — broken URLs auto-reject the listing.
- **Currency support varies by cloud + buyer region** — USD always; EUR, GBP, JPY widely; some smaller currencies only on some clouds.
- **Marketplace listing is not GTM** — listing is a contractual mechanism; you still need marketing + sales to drive demand to the listing.

## Sources

- AWS Marketplace user guide: https://docs.aws.amazon.com/marketplace/latest/userguide/
- AWS Marketplace Catalog API: https://docs.aws.amazon.com/marketplace-catalog/latest/api-reference/
- AWS CPPO docs: https://docs.aws.amazon.com/marketplace/latest/userguide/channel-partner-private-offers.html
- AWS ACE: https://aws.amazon.com/partners/programs/ace/
- Azure Marketplace Partner Center: https://learn.microsoft.com/en-us/partner-center/marketplace/
- Azure Partner Center API: https://learn.microsoft.com/en-us/partner-center/marketplace/api/
- Azure Co-Sell Ready: https://learn.microsoft.com/en-us/partner-center/marketplace/co-sell-overview
- GCP Marketplace producer docs: https://cloud.google.com/marketplace/docs/partners
- Tackle.io API: https://tackle.io/api-documentation
- Tackle State of Cloud Marketplaces: https://tackle.io/state-of-cloud-marketplaces/
