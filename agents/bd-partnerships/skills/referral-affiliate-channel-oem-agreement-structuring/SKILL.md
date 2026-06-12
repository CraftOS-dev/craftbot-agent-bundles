<!--
Source: https://developers.pandadoc.com/ + https://developers.docusign.com/docs/esign-rest-api/
Five partnership archetypes with template + e-sign automation (June 2026 SOTA).
-->
# Referral / Affiliate / Channel / Integration / OEM Agreement Structuring — SKILL

Generate the right partnership agreement from one of five archetypes — **referral**, **affiliate**, **channel reseller**, **integration partner**, **OEM** — populate from CRM tokens, route for e-sign. Five contract shells live in PandaDoc/DocuSign template gallery; this skill picks the right shell, fills tokens, sends for signature, and tracks status back into the partner DB.

## When to use

- **A new partner candidate is ready to formalize** — PICP ≥ 70 + commercial terms agreed.
- **Existing partner upgrades motion** — e.g., referral upgrades to channel reseller.
- **Renew / amend** — annual auto-renew, scope amendment, MDF allocation amendment.
- **Off-board / terminate** — termination letter sub-routine (see Recipe 11).
- **Trigger phrases**: "draft referral agreement for X", "send reseller agreement", "OEM contract for Y", "amend partnership", "terminate partner", "e-sign this".

Do NOT use this skill for: **binding legal redlines** (defer to `legal-counsel`); **commission accounting** (defer to `finance-controller`); **deal-reg form** (use `deal-registration-channel-conflict-resolution`); **template authoring from scratch** (one-time human + legal task).

## Setup

```bash
# Managed OAuth via Maton
export MATON_API_KEY="<key>"

# Direct fallbacks
export PANDADOC_API_KEY="<key>"        # PandaDoc Business $49/seat/mo
export DOCUSIGN_INTEGRATION_KEY="<key>"
export DOCUSIGN_USER_GUID="<guid>"
export DOCUSIGN_ACCOUNT_ID="<id>"
export DOCUSIGN_RSA_PRIVATE_KEY_PATH="/path/to/private.key"
# DocuSign $40/user/mo Business Pro, enterprise quote
```

**One-time setup:** Build 5 templates in PandaDoc (one per archetype). Token markers must match Recipe 12 schema. Have legal-counsel approve each template ONCE; future runs are template-merge + e-sign.

## Common recipes

### Recipe 1: List partner-agreement templates (find the right ID)

```bash
curl "https://gateway.maton.ai/pandadoc/public/v1/templates?tag=partnership" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq '.results[] | {id, name, tags}'
```

Expected templates: `Referral-v3`, `Affiliate-v3`, `ChannelReseller-v3`, `IntegrationPartner-v3`, `OEM-v3`.

### Recipe 2: Generate Referral Partnership Agreement

```bash
curl -X POST "https://gateway.maton.ai/pandadoc/public/v1/documents" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"Referral Agreement — Acme × Brand",
    "template_uuid":"<referral-template-id>",
    "owner":{"email":"partnerships@brand.com"},
    "recipients":[
      {"email":"sarah@acme.com","first_name":"Sarah","last_name":"Lee","role":"Partner"},
      {"email":"coo@brand.com","first_name":"Pat","last_name":"Vendor","role":"Vendor"}
    ],
    "tokens":[
      {"name":"Partner.Name","value":"Acme Analytics"},
      {"name":"Partner.LegalEntity","value":"Acme Analytics, Inc."},
      {"name":"Partner.Address","value":"500 Market St, San Francisco, CA"},
      {"name":"Vendor.Name","value":"Brand Inc"},
      {"name":"EffectiveDate","value":"2026-06-15"},
      {"name":"InitialTerm","value":"12 months"},
      {"name":"AutoRenew","value":"12 months"},
      {"name":"CommissionPct","value":"15%"},
      {"name":"AttributionWindow","value":"90 days"},
      {"name":"PayoutCadence","value":"Quarterly, NET-45"},
      {"name":"TerritoryScope","value":"United States and Canada"}
    ],
    "metadata":{"partner_id":"acme-123","archetype":"referral","hubspot_company_id":"abc"}
  }'
```

### Recipe 3: Generate Affiliate Agreement

```bash
curl -X POST "https://gateway.maton.ai/pandadoc/public/v1/documents" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"Affiliate Agreement — Acme × Brand",
    "template_uuid":"<affiliate-template-id>",
    "recipients":[{"email":"creator@acme.com","role":"Affiliate"}],
    "tokens":[
      {"name":"Affiliate.Name","value":"Acme Creator LLC"},
      {"name":"CpaOrCpl","value":"CPA"},
      {"name":"Payout","value":"$200 per closed-won"},
      {"name":"CookieWindow","value":"60 days"},
      {"name":"AllowedChannels","value":"Owned blog, YouTube, newsletter; NOT paid search on brand terms, NOT spam, NOT incentivized installs"},
      {"name":"PayoutCadence","value":"Monthly, NET-30 via Partnerstack"},
      {"name":"PromoCode","value":"ACME20"},
      {"name":"TrackingDomain","value":"brand.com/?ref=acme"}
    ],
    "metadata":{"partner_id":"acme-aff-001","archetype":"affiliate"}
  }'
```

Affiliate agreements MUST be precise on "allowed channels" — brand-bidding paid search is the #1 affiliate-program failure mode.

### Recipe 4: Generate Channel Reseller Agreement

```bash
curl -X POST "https://gateway.maton.ai/pandadoc/public/v1/documents" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"Reseller Agreement — Acme × Brand (Gold Tier)",
    "template_uuid":"<reseller-template-id>",
    "recipients":[
      {"email":"sarah@acme.com","role":"Reseller"},
      {"email":"coo@brand.com","role":"Vendor"}
    ],
    "tokens":[
      {"name":"Reseller.Name","value":"Acme Solutions Group"},
      {"name":"Tier","value":"Gold"},
      {"name":"MarginPct","value":"25%"},
      {"name":"DealRegUpliftPct","value":"10%"},
      {"name":"MdfEligible","value":"Yes — $25,000/yr per qualifying activity"},
      {"name":"CertsRequired","value":"3 Specialist certifications by Day 60, 1 Expert cert by Day 180"},
      {"name":"Territory","value":"EMEA — UK, FR, DE, NL, IE primary"},
      {"name":"MAP","value":"Reseller may not advertise below 95% of MAP without written approval"},
      {"name":"InvoicingMode","value":"Vendor invoices end-customer; reseller paid commission"},
      {"name":"DealRegSLA","value":"48 hours business-day approval"}
    ],
    "metadata":{"partner_id":"acme-resel-eu","archetype":"channel_reseller","tier":"gold"}
  }'
```

### Recipe 5: Generate Integration Partnership Agreement

```bash
curl -X POST "https://gateway.maton.ai/pandadoc/public/v1/documents" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"Integration Partnership — Acme × Brand",
    "template_uuid":"<integration-template-id>",
    "recipients":[
      {"email":"vp.partnerships@acme.com","role":"Partner"},
      {"email":"vp.partnerships@brand.com","role":"Vendor"}
    ],
    "tokens":[
      {"name":"Partner.Name","value":"Acme Analytics"},
      {"name":"ApiScope","value":"Read-only access to Brand REST API v2; write access for /events endpoint only"},
      {"name":"JointRoadmap","value":"Quarterly joint roadmap reviews; commit to 2 jointly-shipped features per year"},
      {"name":"CoBrandRights","value":"Each party may co-brand integration page with partner logo + half-page joint story"},
      {"name":"DataTerms","value":"No customer PII shared between parties; usage telemetry only; DPA signed under MSA"},
      {"name":"IpAssignment","value":"Each party retains IP in own product; jointly-developed connector code under MIT license"},
      {"name":"HealthMonitoring","value":"Vendor monitors API error rate; partner notified within 24h of >5x baseline error spike"},
      {"name":"DeprecationNotice","value":"180-day notice on breaking API changes"},
      {"name":"CommercialTerms","value":"No commercial $$ exchange between parties; joint customers paid each side independently"}
    ],
    "metadata":{"partner_id":"acme-int-001","archetype":"integration_partner"}
  }'
```

Integration partner agreements are typically **mutual / no-money** — coordinate roadmap, share rights, monitor health. Money is in joint customers.

### Recipe 6: Generate OEM Agreement

```bash
curl -X POST "https://gateway.maton.ai/pandadoc/public/v1/documents" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"OEM Agreement — Acme × Brand",
    "template_uuid":"<oem-template-id>",
    "recipients":[
      {"email":"ceo@acme.com","role":"OEM"},
      {"email":"ceo@brand.com","role":"Vendor"}
    ],
    "tokens":[
      {"name":"OEM.Name","value":"Acme Platform Holdings"},
      {"name":"WhiteLabelOrCoBrand","value":"White-label — distributed under Acme brand only"},
      {"name":"RevenueSharePct","value":"30% to Brand"},
      {"name":"ExclusivityScope","value":"Vertical: legal-tech in North America. Brand may not OEM the same product to other legal-tech OEMs for 24 months."},
      {"name":"InitialTerm","value":"36 months"},
      {"name":"AutoRenew","value":"Annual unless terminated 180 days prior"},
      {"name":"MinimumCommitment","value":"$500,000/yr Brand revenue; ramp 200/350/500 over 3 years"},
      {"name":"IpEscrow","value":"Source code escrow via Iron Mountain; released on Brand bankruptcy or end-of-life"},
      {"name":"TransitionRights","value":"On termination, 90-day customer transition window; OEM may license customers direct from Brand at then-current pricing"},
      {"name":"BrandingRules","value":"OEM may not reference Brand publicly without written approval"}
    ],
    "metadata":{"partner_id":"acme-oem-001","archetype":"oem"}
  }'
```

OEM agreements are **high-stakes**; ALWAYS route through `legal-counsel` for redlines. Template is a starting point only.

### Recipe 7: Send for e-sign (PandaDoc)

```bash
curl -X POST "https://gateway.maton.ai/pandadoc/public/v1/documents/<doc-id>/send" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "message":"Hi Sarah — attached is the Referral Partnership Agreement we discussed. Two clauses highlighted for your review (Section 4 commission, Section 9 territory). Happy to walk through.",
    "subject":"Brand × Acme — Referral Partnership Agreement",
    "silent":false
  }'
```

### Recipe 8: DocuSign envelope for legal-mature redlined PDF

When legal redlines turn the PandaDoc draft into a Word/PDF, send via DocuSign:

```bash
PDF_B64=$(base64 -w 0 final-redlined-agreement.pdf)
curl -X POST "https://gateway.maton.ai/docusign/restapi/v2.1/accounts/$DOCUSIGN_ACCOUNT_ID/envelopes" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "emailSubject":"Please sign — Acme × Brand Reseller Agreement",
    "documents":[{"documentBase64":"'$PDF_B64'","name":"Reseller Agreement","fileExtension":"pdf","documentId":"1"}],
    "recipients":{"signers":[
      {"email":"sarah@acme.com","name":"Sarah Lee","recipientId":"1","routingOrder":"1",
       "tabs":{"signHereTabs":[{"anchorString":"/sig-partner/","anchorYOffset":"10","documentId":"1"}]}},
      {"email":"coo@brand.com","name":"Pat Vendor","recipientId":"2","routingOrder":"2",
       "tabs":{"signHereTabs":[{"anchorString":"/sig-vendor/","anchorYOffset":"10","documentId":"1"}]}}
    ]},
    "status":"sent"
  }'
```

### Recipe 9: Webhook for status (PandaDoc) → update partner DB

```bash
# One-time setup
curl -X POST "https://gateway.maton.ai/pandadoc/public/v1/webhook-subscriptions" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"Partner agreement status sync",
    "url":"https://your-app.com/webhook/pandadoc-partner",
    "triggers":["document_state_changed","document_completed"],
    "shared_key":"<secret>"
  }'
```

On `document_completed`:
1. Patch Notion partner DB: `status = "active"`, `agreement_signed_date = now`, `agreement_url = pandadoc_url`.
2. Trigger `partner-onboarding-90-day-plan` skill — Day 0 kickoff.
3. Post in `#partnerships` Slack channel.

### Recipe 10: Decision tree — which archetype to use

```yaml
decide_archetype:
  partner_sends_leads_no_resale: "referral"
  partner_paid_per_action_via_promo_link: "affiliate"
  partner_resells_to_endcustomer: "channel_reseller"
  joint_api_integration_no_money: "integration_partner"
  partner_distributes_under_own_brand_with_revshare: "oem"

choose_payment_mechanic:
  referral: "Commission % per closed-won; Partnerstack tracks; NET-45 quarterly"
  affiliate: "CPA or CPL via Partnerstack or Impact; monthly NET-30"
  channel_reseller: "Margin discount on invoice; vendor invoices end-customer in most modern motions; reseller paid commission"
  integration_partner: "No $$ between parties typically"
  oem: "Revenue share % paid quarterly; minimums + ramp"
```

### Recipe 11: Termination letter sub-routine

```bash
curl -X POST "https://gateway.maton.ai/pandadoc/public/v1/documents" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "name":"Termination Notice — Acme × Brand",
    "template_uuid":"<termination-template-id>",
    "recipients":[{"email":"sarah@acme.com","role":"Partner"}],
    "tokens":[
      {"name":"Partner.Name","value":"Acme Analytics"},
      {"name":"AgreementExecutedDate","value":"2025-03-15"},
      {"name":"TerminationEffectiveDate","value":"2026-08-15"},
      {"name":"NoticePeriod","value":"60 days per Section 12"},
      {"name":"GroundsForTermination","value":"Missed quarterly KPI thresholds in Q1 + Q2 2026; pre-discussed in QBR May 22"},
      {"name":"TransitionPlan","value":"Joint customers transition by Aug 30; MDF unused balance ($8,200) reconciled by Sep 15; portal access revoked Aug 15"},
      {"name":"PostTerminationConfidentiality","value":"NDA survives for 3 years per Section 18"}
    ],
    "metadata":{"partner_id":"acme-123","archetype":"termination"}
  }'
```

Defer redlines to `legal-counsel`; AR reconciliation to `finance-controller`.

### Recipe 12: Token reference (canonical schema across templates)

```yaml
# Identity tokens (all templates)
Partner.Name, Partner.LegalEntity, Partner.Address, Partner.Country
Vendor.Name, Vendor.LegalEntity, Vendor.Address

# Term tokens (all templates)
EffectiveDate, InitialTerm, AutoRenew, NoticePeriod

# Commercial tokens (varies by archetype)
CommissionPct, AttributionWindow, PayoutCadence              # referral
CpaOrCpl, Payout, CookieWindow, AllowedChannels, PromoCode  # affiliate
Tier, MarginPct, DealRegUpliftPct, MdfEligible, Territory,
  CertsRequired, MAP, InvoicingMode, DealRegSLA              # channel_reseller
ApiScope, JointRoadmap, CoBrandRights, DataTerms, IpAssignment,
  HealthMonitoring, DeprecationNotice, CommercialTerms       # integration_partner
WhiteLabelOrCoBrand, RevenueSharePct, ExclusivityScope,
  MinimumCommitment, IpEscrow, TransitionRights, BrandingRules # oem

# Legal-boilerplate tokens (all templates) — DO NOT redefine without legal-counsel
LimitOfLiability, IndemnityScope, GoverningLaw, Arbitration,
  NoticeAddress, AssignmentAllowed, ChangeOfControlClause
```

Store this schema in `notion-mcp`; reference at draft time to avoid silent token misses.

## Examples

### Example 1: Activate Acme as a Gold Tier Reseller

**Goal:** Acme PICP-scored 88, commercial terms agreed (25% margin, EMEA, Gold tier with cert requirements). Goal: signed agreement within 7 days.

**Steps:**
1. Day 1 — Recipe 4 generates draft. Internal review (commercial owner + legal-counsel cross-agent).
2. Day 2-3 — Legal redlines in PandaDoc; partner countersigns inline.
3. Day 4 — Recipe 7 sends final for e-sign.
4. Day 5-6 — Partner signs, vendor countersigns.
5. Day 7 — Recipe 9 webhook flips partner DB to "active"; triggers `partner-onboarding-90-day-plan`.

**Result:** Acme onboarded; commercial relationship is contractual; metadata flows downstream.

### Example 2: Integration partner with mutual API access + co-marketing

**Goal:** Acme (CDP vendor, complementary tech) ready for integration partner status; commercial: no $$ exchange, joint roadmap commitment.

**Steps:**
1. Recipe 5 generates draft. No legal redlines required; both sides legal-approved template.
2. Recipe 7 sends for e-sign.
3. Within 48h, both sides counter-sign.
4. Recipe 9 webhook → partner DB → triggers `integration-roadmap-planning` for Q3 joint roadmap session.
5. Hand-off to `product-manager` for first joint roadmap session within 14 days.

**Result:** Integration partnership formalized; roadmap session scheduled; joint customers benefit.

### Example 3: OEM termination after 18 months, missed minimums

**Goal:** OEM partner missed $200K Year-1 minimum; missed $350K Year-2 commit; mutual decision to wind down.

**Steps:**
1. Recipe 11 generates termination notice. ROUTE through `legal-counsel` (mandatory for OEM).
2. Termination notice sent via DocuSign (legal-redlined).
3. Transition plan in Notion: customers re-contracted direct to Brand at Y2 pricing.
4. `finance-controller` reconciles unpaid minimums + revenue share.
5. Source code escrow status confirmed via Iron Mountain.

**Result:** Clean wind-down; no customer disruption; legal + AR loose ends closed.

## Edge cases / gotchas

- **Tokens are case-sensitive.** `Partner.Name` and `partner.name` are different. Templates silently render `{{token}}` literal if not matched. Validate via PandaDoc preview before sending.
- **PandaDoc free tier is API-limited.** Need Business ($49/seat) or higher for API access + bulk send.
- **DocuSign JWT auth is one-time fiddly.** Integration Key + RSA pair + admin consent. Cache token (1h expiry).
- **Anchor tabs in DocuSign fail silently if PDF rendering changes.** Always preview the final PDF before bulk-sending.
- **Sequential routing in PandaDoc is a Workflow feature** (not in Essentials tier). DocuSign handles routingOrder natively.
- **"Boilerplate" tokens are not boilerplate** — Limitation of Liability, Indemnity scope, Governing Law are deal-breakers in legal review. NEVER edit these without `legal-counsel`.
- **Channel reseller invoicing mode** matters: "vendor invoices end-customer" is modern (cleaner revenue rec); "reseller invoices end-customer + remits" is legacy. Pick deliberately.
- **OEM exclusivity is the #1 negotiation point** — overly broad exclusivity kills future partnerships; too narrow makes the deal not worth it. Get exclusivity scope BEFORE drafting.
- **Affiliate "allowed channels" is the #1 program failure** — without precise "no brand-bidding on paid search" wording, you'll burn ad budget paying affiliates to compete with your own SEO.
- **Integration partner DPA**: if partner has access to PII (even metadata), DPA is required under GDPR. Check before sending.
- **Webhook signature validation matters.** Anyone can POST fake "document_completed" events to your webhook and flip Notion to "active." Verify HMAC on every event.
- **Re-send semantics**: PandaDoc `/resend` keeps the same URL; `/send` again creates a new doc. Don't confuse on amendments.
- **Voided envelopes count against DocuSign quota** — high-iteration negotiations burn credits via voids.
- **Jurisdiction matters for e-sign validity.** Standard e-sign (DocuSign / PandaDoc) is valid in most US/EU contexts; some EU (Germany, France) qualified-electronic-signature (QES) requirements for specific contract types may need Adobe Sign + national ID schemes.
- **Cross-border tax**: Reseller margins in cross-border deals trigger VAT / sales-tax in some jurisdictions. Defer to `finance-controller`.
- **Storage of signed agreements**: PDF copies to Google Drive partner folder + Notion partner DB row; original lives in PandaDoc / DocuSign envelope; AR-relevant copies routed to `finance-controller` workspace.

## Sources

- PandaDoc API: https://developers.pandadoc.com/
- PandaDoc Documents endpoint: https://developers.pandadoc.com/reference/documents
- PandaDoc Webhooks: https://developers.pandadoc.com/reference/webhook-subscriptions
- DocuSign eSignature REST API: https://developers.docusign.com/docs/esign-rest-api/
- DocuSign JWT auth: https://developers.docusign.com/platform/auth/jwt/jwt-get-token/
- Crossbeam — Partnership Economy report: https://www.crossbeam.com/blog/the-partnership-economy/
- Partnership archetype methodology — IBM channel research: https://www.ibm.com/blog/channel-partner-archetypes
- Adobe Acrobat Sign (QES alternative): https://developer.adobe.com/document-services/docs/overview/sign-api/
