<!--
Source: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/advertising-targeting/create-and-manage-segments
Source: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/lead-gen-forms/
LinkedIn Marketing API — via cli-anything curl (no public MCP yet).
-->
# LinkedIn Ads — ABM Campaigns + Matched Audiences + Lead Gen — SKILL

LinkedIn Ads is the B2B paid SOTA for account-based marketing (ABM). The lever is **Matched Audiences** uploaded from CRM (companies, contacts, websites) combined with **Sponsored Content** / **Message Ads** / **Lead Gen Forms**. No public MCP — execute via Marketing API REST through `cli-anything` curl.

## When to use this skill

- **ABM target-account list** activation across LinkedIn (Sponsored Content + Message Ads).
- **Lead Gen Forms** with profile autofill — 5-15% conversion typical (vs 2-3% on website forms).
- **Job-title / function targeting** — LinkedIn's signature lever for B2B.
- **Company-list retargeting** — upload Salesforce / HubSpot account list, run nurture campaigns.
- **Event promotion** — LinkedIn Event Ads for conferences / webinars.
- **Conversation Ads** — interactive Q&A in DMs for mid-funnel.

**Do NOT use this skill when:**
- B2C / DTC e-com — LinkedIn audience cost is 5-10x Meta; not cost-effective for low-AOV.
- LMDP access not granted — fall back to manual Campaign Manager UI; agent ships brief.

## Setup

### LinkedIn Marketing Developer Platform (LMDP) access

Apply at https://www.linkedin.com/developers/apps with privacy policy + use case description. Review 5-10 business days. Free for advertisers.

```bash
export LI_ACCESS_TOKEN="<3-legged-oauth-token>"
export LI_ACCOUNT_ID="<sponsored-account-numeric>"   # urn:li:sponsoredAccount:<id>
export LI_ORG_ID="<organization-urn>"                # urn:li:organization:<id>
```

### REST headers (always required)

```bash
-H "Authorization: Bearer $LI_ACCESS_TOKEN"
-H "LinkedIn-Version: 202406"
-H "X-Restli-Protocol-Version: 2.0.0"
-H "Content-Type: application/json"
```

### Key API endpoints (Marketing API v202406)

- DMP segments (Matched Audiences): `POST /rest/dmpSegments`
- Add users to segment: `POST /rest/dmpSegments/{id}/users`
- Campaign groups: `POST /rest/adCampaignGroups`
- Campaigns: `POST /rest/adCampaigns`
- Creatives: `POST /rest/adAccounts/{id}/creatives`
- Lead Gen Forms: `POST /rest/leadGenForms`
- Conversion events: `POST /rest/conversionEvents`
- Reporting: `GET /rest/adAnalytics`

## Common recipes

### Recipe 1: ABM target-account list — company match

```bash
# Step 1: Create Company-based DMP segment
curl -X POST "https://api.linkedin.com/rest/dmpSegments" \
  -H "Authorization: Bearer $LI_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -d '{
    "account": "urn:li:sponsoredAccount:'$LI_ACCOUNT_ID'",
    "destinations": [{"destination":"LINKEDIN"}],
    "name": "ABM_Tier1_FY26",
    "sourcePlatform": "API",
    "sourceSegmentId": "abm_tier1_fy26_companies",
    "type": "COMPANY"
  }'

# Step 2: Add companies by domain
curl -X POST "https://api.linkedin.com/rest/dmpSegments/$SEGMENT_ID/users" \
  -H "Authorization: Bearer $LI_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -d '{
    "elements": [
      {"action":"ADD","userIds":[{"idType":"DOMAIN_NAME","idValue":"acme-corp.com"}]},
      {"action":"ADD","userIds":[{"idType":"DOMAIN_NAME","idValue":"globex-inc.com"}]},
      {"action":"ADD","userIds":[{"idType":"DOMAIN_NAME","idValue":"initech.io"}]}
    ]
  }'
```

### Recipe 2: ABM contact list — hashed-email match

```bash
curl -X POST "https://api.linkedin.com/rest/dmpSegments" \
  -H "Authorization: Bearer $LI_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -d '{
    "account": "urn:li:sponsoredAccount:'$LI_ACCOUNT_ID'",
    "destinations": [{"destination":"LINKEDIN"}],
    "name": "ABM_Tier1_Contacts_FY26",
    "sourcePlatform": "API",
    "type": "USER"
  }'

# Add hashed contacts (SHA-256 of lowercased + trimmed email)
curl -X POST "https://api.linkedin.com/rest/dmpSegments/$SEGMENT_ID/users" \
  -H "Authorization: Bearer $LI_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -d '{
    "elements": [
      {"action":"ADD","userIds":[{"idType":"SHA256_EMAIL","idValue":"'$HASHED_EMAIL_1'"}]},
      {"action":"ADD","userIds":[{"idType":"SHA256_EMAIL","idValue":"'$HASHED_EMAIL_2'"}]}
    ]
  }'
```

### Recipe 3: Sponsored Content campaign — ABM Tier 1

```bash
# Step 1: Campaign group (parent for budget pacing)
curl -X POST "https://api.linkedin.com/rest/adCampaignGroups" \
  -H "Authorization: Bearer $LI_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -d '{
    "account": "urn:li:sponsoredAccount:'$LI_ACCOUNT_ID'",
    "name": "ABM_Tier1_FY26",
    "status": "ACTIVE",
    "totalBudget": {"amount":"50000","currencyCode":"USD"},
    "runSchedule": {"start": '$(date +%s000)'}
  }'

# Step 2: Sponsored Content campaign with Matched Audience
curl -X POST "https://api.linkedin.com/rest/adCampaigns" \
  -H "Authorization: Bearer $LI_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -d '{
    "account": "urn:li:sponsoredAccount:'$LI_ACCOUNT_ID'",
    "campaignGroup": "urn:li:sponsoredCampaignGroup:'$GROUP_ID'",
    "name": "ABM_Tier1_Awareness_SC",
    "type": "SPONSORED_UPDATES",
    "objectiveType": "BRAND_AWARENESS",
    "costType": "CPM",
    "unitCost": {"amount":"25.00","currencyCode":"USD"},
    "dailyBudget": {"amount":"100","currencyCode":"USD"},
    "targetingCriteria": {
      "include": {
        "and": [
          {"or":{"urn:li:adTargetingFacet:matchedAudiences":["urn:li:dmpSegment:'$SEGMENT_ID'"]}},
          {"or":{"urn:li:adTargetingFacet:jobFunctions":["urn:li:jobFunction:25","urn:li:jobFunction:13"]}},
          {"or":{"urn:li:adTargetingFacet:seniorities":["urn:li:seniority:8","urn:li:seniority:9","urn:li:seniority:10"]}}
        ]
      }
    },
    "status": "ACTIVE"
  }'
```

### Recipe 4: Lead Gen Form — profile-autofill

```bash
# Step 1: Create form
curl -X POST "https://api.linkedin.com/rest/leadGenForms" \
  -H "Authorization: Bearer $LI_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -d '{
    "owner": "urn:li:sponsoredAccount:'$LI_ACCOUNT_ID'",
    "name": "Q3-EnterpriseDemo-LGF",
    "headline": "Book a 15-min demo",
    "description": "Show us your stack — we''ll show you a custom workflow.",
    "questions": [
      {"questionDetails":{"question":"What''s your monthly volume?","answers":[
        {"answer":"<10K"},{"answer":"10K-100K"},{"answer":">100K"}]}}
    ],
    "consents": [{"required":true,"consentText":"By submitting, you agree to our privacy policy."}],
    "fieldDetails": [
      {"field":"FIRST_NAME","required":true},
      {"field":"LAST_NAME","required":true},
      {"field":"EMAIL","required":true},
      {"field":"COMPANY_NAME","required":true},
      {"field":"JOB_TITLE","required":true},
      {"field":"WORK_EMAIL","required":false}
    ],
    "privacyPolicyUrl": "https://brand.com/privacy",
    "thankYouMessage": "Thanks! We''ll be in touch within 24h."
  }'

# Step 2: Attach to creative
curl -X POST "https://api.linkedin.com/rest/adAccounts/$LI_ACCOUNT_ID/creatives" \
  -H "Authorization: Bearer $LI_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -d '{
    "campaign": "urn:li:sponsoredCampaign:'$CAMPAIGN_ID'",
    "type": "SPONSORED_STATUS_UPDATE",
    "leadGenForm": "urn:li:leadGenForm:'$LGF_ID'",
    "content": {"reference":"urn:li:share:'$SHARE_URN'"},
    "status": "ACTIVE"
  }'
```

### Recipe 5: Message Ads (formerly Sponsored InMail)

```bash
curl -X POST "https://api.linkedin.com/rest/adCampaigns" \
  -H "Authorization: Bearer $LI_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -d '{
    "account": "urn:li:sponsoredAccount:'$LI_ACCOUNT_ID'",
    "campaignGroup": "urn:li:sponsoredCampaignGroup:'$GROUP_ID'",
    "name": "ABM_Tier1_MessageAds_Q3",
    "type": "SPONSORED_INMAILS",
    "objectiveType": "WEBSITE_VISITS",
    "costType": "CPS",
    "unitCost": {"amount":"0.75","currencyCode":"USD"},
    "dailyBudget": {"amount":"100","currencyCode":"USD"},
    "targetingCriteria": {
      "include": {"and":[
        {"or":{"urn:li:adTargetingFacet:matchedAudiences":["urn:li:dmpSegment:'$SEGMENT_ID'"]}}
      ]}
    }
  }'
```

### Recipe 6: LinkedIn Conversions API — server-side

```bash
curl -X POST "https://api.linkedin.com/rest/conversionEvents" \
  -H "Authorization: Bearer $LI_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -d '{
    "conversion": "urn:lla:llaPartnerConversion:'$CONVERSION_ID'",
    "conversionHappenedAt": '$(date +%s000)',
    "conversionValue": {"currencyCode":"USD","amount":"99.99"},
    "user": {
      "userIds": [
        {"idType":"SHA256_EMAIL","idValue":"'$EMAIL_SHA256'"},
        {"idType":"LINKEDIN_FIRST_PARTY_ADS_TRACKING_UUID","idValue":"'$LI_FAT_UUID'"}
      ]
    }
  }'
```

### Recipe 7: Reporting — campaign performance last 30d

```bash
curl "https://api.linkedin.com/rest/adAnalytics?\
q=analytics&\
pivot=CAMPAIGN&\
campaigns=List(urn%3Ali%3AsponsoredCampaign%3A$CAMPAIGN_ID)&\
dateRange.start.year=2026&dateRange.start.month=5&dateRange.start.day=10&\
dateRange.end.year=2026&dateRange.end.month=6&dateRange.end.day=9&\
fields=impressions,clicks,costInUsd,externalWebsiteConversions,oneClickLeads" \
  -H "Authorization: Bearer $LI_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -H "X-Restli-Protocol-Version: 2.0.0"
```

## Examples — ABM playbook

```yaml
campaign_group:
  name: "ABM_Tier1_FY26"
  total_budget: $50K
  daily_budget: $250
  
campaigns:
  awareness_SC:
    type: SPONSORED_UPDATES
    objective: BRAND_AWARENESS
    audience: Matched Audience (Tier1 200 companies) + Director+ seniority
    creative: single-image thought-leadership posts
    budget: $80/day
    bid: CPM $22
  
  engagement_video:
    type: SPONSORED_UPDATES  
    objective: VIDEO_VIEW
    audience: Awareness video-viewers 50% (retargeting)
    creative: 60s product demo
    budget: $50/day
    bid: CPV $0.15
  
  lead_capture_LGF:
    type: SPONSORED_UPDATES
    objective: LEAD_GENERATION
    audience: Awareness + Engagement audiences retargeted
    creative: Lead Gen Form attached
    budget: $80/day
    bid: CPC $12
  
  message_ads:
    type: SPONSORED_INMAILS
    audience: Tier1 contacts only (hashed-email match, decision-makers)
    creative: 1-1 message from sales VP
    budget: $40/day
    bid: CPS $0.75
```

## Edge cases

### Minimum audience size for delivery
DMP segment: **300 members minimum** to start delivering. Below = held in pending. Mix Matched Audience with job-title / function targeting to reach min.

### LMDP review timeline
5-10 business days standard. Reject reasons: vague use case, missing privacy policy, attempting end-user data scraping. Fix and resubmit.

### Hashing format
SHA-256 of lowercased + trimmed email/phone. NOT base64. Pass as lowercase hex string.

### Cost types per campaign type
- Sponsored Content: CPM, CPC
- Message Ads / InMail: CPS (cost per send)
- Lead Gen Forms: CPC, CPM
- Conversation Ads: CPS
- Dynamic Ads: CPC, CPM

### Job Function URN
`urn:li:jobFunction:NN`. Reference: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/community-management/shares/share-api#job-functions

### Seniority targeting
`urn:li:seniority:8` (Director), `9` (VP), `10` (CXO). Most ABM targets Director+.

### Lead Gen Form fields available
FIRST_NAME, LAST_NAME, EMAIL, PHONE_NUMBER, COMPANY_NAME, JOB_TITLE, COMPANY_SIZE, INDUSTRY, COUNTRY/REGION, POSTAL_CODE, WORK_EMAIL.

### CPM benchmarks
B2B Sponsored Content $25-$80 CPM (highest of any major platform). Message Ads $0.50-$2.00 per send. CPC $7-$15.

### Audience expansion
By default LinkedIn applies "Audience expansion" — adds similar profiles. Disable for strict ABM:
```json
"audienceExpansionEnabled": false
```

### Rate limits
Standard: 100 calls / minute / app. Marketing API uses per-account throttles, batch with bulk endpoints when available.

### Format constraints
- Single image: 1.91:1 or 1:1 ratio, min 1200x627px
- Video: 30s-30min, max 200MB, MP4
- Carousel: 2-10 cards
- Document Ad (PDF): up to 10MB

## Sources

- LinkedIn Marketing API base: https://learn.microsoft.com/en-us/linkedin/marketing/
- Matched Audiences / DMP Segments: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/advertising-targeting/create-and-manage-segments
- Campaigns API: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/ads-reporting/ad-campaign-groups
- Lead Gen Forms: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/lead-gen-forms/
- Conversion Events (CAPI): https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversions-api
- Analytics API: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting
- LMDP app application: https://www.linkedin.com/developers/apps
