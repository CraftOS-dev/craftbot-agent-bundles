<!--
Source: https://www.mcpbundles.com/blog/linkedin-mcp-server
LinkedIn Marketing API: https://learn.microsoft.com/en-us/linkedin/marketing/overview
-->
# LinkedIn Marketing API — SKILL

MCPBundles LinkedIn MCP wraps the LinkedIn Community Management API + Marketing API. Org-mode is the practical default: set `LINKEDIN_MODE=organization` and `LINKEDIN_ORGANIZATION_ID=<urn>` to publish as the company page. Image, document, and carousel posts use a **mandatory 2-step URN upload** flow.

## When to use this skill

- **LinkedIn company page posts** — text, images, documents, video, carousels.
- **Executive personal profile posts** (when API access granted) — thought leadership.
- **LinkedIn ads** — `/rest/adAccounts/{id}/adCampaigns` for sponsored content + InMail + lead-gen forms.
- **LinkedIn newsletters** — long-form via the Articles API.
- **Multi-page document / PDF carousels** — Buffer cannot do these; LinkedIn API can.

**Do NOT use this skill when:**
- **Cross-platform cascade** including LinkedIn → use Buffer (`buffer-cross-platform-publishing` skill) for simple text+image. Only fall to native API when carousel / document required.
- **DM / inbox automation** — not in scope.

## Setup

### MCPBundles LinkedIn MCP install

```bash
npx -y @mcpbundles/linkedin-mcp@latest
```

### Auth — LinkedIn Community Management API

```bash
# 1. LinkedIn Developer Portal app with Community Management API approval (manual review)
# 2. OAuth scopes: w_member_social, w_organization_social, r_organization_admin, rw_ads
# 3. Generate token via 3-legged OAuth

export LINKEDIN_ACCESS_TOKEN="<token>"
export LINKEDIN_MODE="organization"            # vs "personal"
export LINKEDIN_ORGANIZATION_ID="urn:li:organization:<id>"
export LINKEDIN_AD_ACCOUNT_ID="<numeric>"      # for ads
```

### Tools available

- `create_post` — text-only org/personal post
- `register_upload` — step 1 of 2-step URN upload
- `upload_media` — step 2 (binary PUT)
- `create_image_post` / `create_video_post` / `create_document_post` / `create_carousel_post`
- `create_article` — long-form newsletter publishing
- `list_org_posts` / `get_post_analytics`
- Marketing API: `create_ad_campaign` / `create_creative` / `list_lead_gen_forms`

## Common recipes

### Recipe 1: Text-only org post

```bash
mcp tool linkedin.create_post \
  --author "$LINKEDIN_ORGANIZATION_ID" \
  --text "Our 2026 marketing playbook is live. <link>" \
  --visibility "PUBLIC"
```

### Recipe 2: Image post (2-step URN upload)

```bash
# STEP 1: register upload
upload_resp=$(mcp tool linkedin.register_upload \
  --owner "$LINKEDIN_ORGANIZATION_ID" \
  --recipe "urn:li:digitalmediaRecipe:feedshare-image")

upload_url=$(echo "$upload_resp" | jq -r .uploadUrl)
image_urn=$(echo "$upload_resp" | jq -r .imageUrn)

# STEP 2: upload binary via PUT
curl -X PUT "$upload_url" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  --data-binary "@hero.jpg"

# STEP 3: reference URN in post
mcp tool linkedin.create_image_post \
  --author "$LINKEDIN_ORGANIZATION_ID" \
  --text "Caption with hashtags." \
  --imageUrn "$image_urn" \
  --visibility "PUBLIC"
```

### Recipe 3: Document / PDF carousel (LinkedIn's native carousel)

LinkedIn's document upload renders multi-page PDFs as swipeable carousels. Best engagement format.

```bash
# Register
upload_resp=$(mcp tool linkedin.register_upload \
  --owner "$LINKEDIN_ORGANIZATION_ID" \
  --recipe "urn:li:digitalmediaRecipe:feedshare-document")

upload_url=$(echo "$upload_resp" | jq -r .uploadUrl)
doc_urn=$(echo "$upload_resp" | jq -r .documentUrn)

# Upload PDF
curl -X PUT "$upload_url" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  --data-binary "@carousel.pdf"

# Create post
mcp tool linkedin.create_document_post \
  --author "$LINKEDIN_ORGANIZATION_ID" \
  --text "10 lessons from Q1 — swipe through" \
  --documentUrn "$doc_urn" \
  --title "Q1 Lessons"
```

PDF format requirements:
- Aspect ratio 1:1 (square) or 4:5 (portrait) — landscape gets letterboxed
- 1080x1080 px or 1080x1350 px per page
- Max 300 pages, max 100MB
- Pages 1-3 are key (most users only see first 3)

### Recipe 4: Video post

```bash
upload_resp=$(mcp tool linkedin.register_upload \
  --owner "$LINKEDIN_ORGANIZATION_ID" \
  --recipe "urn:li:digitalmediaRecipe:feedshare-video")

curl -X PUT "$(echo $upload_resp | jq -r .uploadUrl)" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  --data-binary "@video.mp4"

mcp tool linkedin.create_video_post \
  --author "$LINKEDIN_ORGANIZATION_ID" \
  --text "Video caption — first line is the hook" \
  --videoUrn "$(echo $upload_resp | jq -r .videoUrn)"
```

### Recipe 5: LinkedIn newsletter article

```bash
mcp tool linkedin.create_article \
  --author "$LINKEDIN_ORGANIZATION_ID" \
  --title "Marketing in 2026: 5 shifts" \
  --content "$(cat article.html)" \
  --coverImage "@cover.jpg" \
  --newsletterId "<newsletter-id>" \
  --publish true
```

Newsletter requires:
- Newsletter object created first (via Sales Navigator or manual UI)
- Cover image 1280x720
- 250+ word minimum
- Subscribers auto-notified

### Recipe 6: LinkedIn ads — sponsored content campaign

```bash
# Step 1: campaign group (organizational)
group_id=$(curl -X POST "https://api.linkedin.com/rest/adCampaignGroups" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -d '{
    "account":"urn:li:sponsoredAccount:'$LINKEDIN_AD_ACCOUNT_ID'",
    "name":"Q3-Launch-Group",
    "status":"ACTIVE",
    "totalBudget":{"currencyCode":"USD","amount":"10000"}
  }' | jq -r .id)

# Step 2: campaign
campaign_id=$(curl -X POST "https://api.linkedin.com/rest/adCampaigns" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -d '{
    "account":"urn:li:sponsoredAccount:'$LINKEDIN_AD_ACCOUNT_ID'",
    "campaignGroup":"urn:li:sponsoredCampaignGroup:'$group_id'",
    "name":"Q3-SponsoredContent-Tier1",
    "type":"SPONSORED_UPDATES",
    "costType":"CPC",
    "unitCost":{"currencyCode":"USD","amount":"5.00"},
    "dailyBudget":{"currencyCode":"USD","amount":"200"},
    "targetingCriteria":{
      "include":{
        "and":[
          {"or":{"urn:li:adTargetingFacet:industries":["urn:li:industry:6"]}},
          {"or":{"urn:li:adTargetingFacet:seniorities":["urn:li:seniority:7","urn:li:seniority:8"]}}
        ]
      }
    },
    "status":"ACTIVE",
    "format":"SINGLE_IMAGE"
  }' | jq -r .id)

# Step 3: creative (sponsored content needs an organic post to sponsor)
curl -X POST "https://api.linkedin.com/rest/creatives" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -d '{
    "campaign":"urn:li:sponsoredCampaign:'$campaign_id'",
    "type":"SPONSORED_UPDATE",
    "reference":"urn:li:share:<organic-post-urn>",
    "status":"ACTIVE"
  }'
```

### Recipe 7: Lead-gen forms

```bash
# Create form
curl -X POST "https://api.linkedin.com/rest/leadGenForms" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406" \
  -d '{
    "account":"urn:li:sponsoredAccount:'$LINKEDIN_AD_ACCOUNT_ID'",
    "name":"Q3-LeadMagnet-Form",
    "fields":[
      {"name":"EMAIL_ADDRESS","required":true},
      {"name":"FIRST_NAME","required":true},
      {"name":"LAST_NAME","required":true},
      {"name":"JOB_TITLE","required":false},
      {"name":"COMPANY_NAME","required":false}
    ],
    "privacyPolicyUrl":"https://yourbrand.com/privacy"
  }'

# Pull responses (daily)
curl "https://api.linkedin.com/rest/leadGenFormResponses?q=form&form=<form-urn>" \
  -H "Authorization: Bearer $LINKEDIN_ACCESS_TOKEN" \
  -H "LinkedIn-Version: 202406"
```

Pipe responses to HubSpot via `hubspot-crm-marketing-mcp` skill `create_contact`.

### Recipe 8: Post analytics

```bash
mcp tool linkedin.get_post_analytics \
  --postUrn "urn:li:share:<id>" \
  --metrics '["impressions","clicks","reactions","comments","shares","unique_impressions","follows"]'
```

## Examples — executive thought leadership program

```yaml
# Weekly cadence
monday:
  - executive_text_post: industry commentary, 200-400 words
tuesday:
  - org_carousel: data-driven insight (5-7 pages PDF)
thursday:
  - executive_video_post: 60-90s talking head
friday:
  - org_text_post: customer story or behind-the-scenes

monthly:
  - newsletter_article: 1000-1500 word deep dive
quarterly:
  - sponsored_thought_leadership_campaign: $5K boost on best-performing organic
```

## Edge cases

### App approval reality
LinkedIn Community Management API requires:
- App in LinkedIn Developer Portal
- Company verification (D-U-N-S or domain)
- Use case description
- Manual review (typically 5-15 business days)

Marketing Solutions API (ads) is easier — most ads platforms get approved.

While waiting for approval, the agent should use Buffer for posting (which has its own pre-approved LinkedIn integration).

### Version header
LinkedIn API requires `LinkedIn-Version: 202406` (or current month). Update quarterly.

### URN format gotchas
- Org URN: `urn:li:organization:<id>` (numeric)
- Person URN: `urn:li:person:<id>` (alphanumeric)
- Sponsored account URN: `urn:li:sponsoredAccount:<id>` (numeric)
- Share URN: `urn:li:share:<id>` (numeric, returned on post creation)
- UGCPost URN: `urn:li:ugcPost:<id>` (newer format for some endpoints)

### Image carousel vs document carousel
LinkedIn has two carousel types:
1. **Image carousel** — up to 10 separate images, fewer rendering controls
2. **Document carousel (PDF)** — multi-page PDF, looks polished, higher engagement

Document carousel is preferred for content marketing.

### Visibility
- `PUBLIC` — visible to anyone
- `CONNECTIONS` (personal only) — first-degree connections only
- `LOGGED_IN` — LinkedIn users only

For org posts always use `PUBLIC`.

### Hashtags
LinkedIn's algorithm de-prioritizes hashtags as of 2024. Use 0-3 hashtags max. Inline #brand for tracking, that's it.

### Mention syntax
`@[Name]` won't auto-link via API. Use proper mention attributes:

```json
{
  "specificContent": {
    "com.linkedin.ugc.ShareContent": {
      "shareCommentary": {
        "text": "Working with @[Person Name] on this.",
        "attributes": [
          {
            "start": 13,
            "length": 14,
            "value": {"com.linkedin.common.MemberAttributedEntity": {"member":"urn:li:person:<id>"}}
          }
        ]
      }
    }
  }
}
```

### Rate limits
- Community Management API: 500 / day per app per org
- Marketing API: 100,000 / day per ad account
- Lead gen form responses: 1,000 / day

### Ads — targeting facet IDs
LinkedIn uses URN-based targeting. Common facets:
- `industries`: `urn:li:industry:<id>` (4 = Construction, 6 = Software, etc.)
- `seniorities`: `urn:li:seniority:<id>` (7 = Director, 8 = VP, 9 = CXO)
- `jobFunctions`: `urn:li:function:<id>` (10 = Engineering, 25 = Marketing)
- `companySize`: `urn:li:companySize:F` (F = 5,001-10,000)

Get the full list: `curl https://api.linkedin.com/rest/adTargetingEntities?q=facets&facet=<facet>`

## Sources

- **MCPBundles LinkedIn MCP**: https://www.mcpbundles.com/blog/linkedin-mcp-server
- **Community Management API**: https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management
- **Marketing API overview**: https://learn.microsoft.com/en-us/linkedin/marketing/overview
- **Ads campaigns API**: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-campaigns
- **Lead gen forms API**: https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/lead-gen-forms/lead-gen-forms
