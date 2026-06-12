# Business Development / Partnerships — deep reference

This appends to `AGENT.md`. **Not** in the agent's default context. Grep when the SOUL.md summary isn't enough.

Search-friendly headings: "Capability reference", "Partnership technology categories", "Partnership archetypes", "PICP scoring rubric", "Referral agreement template", "Affiliate agreement template", "Channel reseller agreement template", "Integration partnership agreement template", "OEM agreement template", "AWS Marketplace listing playbook", "Azure Marketplace listing playbook", "GCP Marketplace listing playbook", "Salesforce AppExchange listing playbook", "HubSpot App Marketplace listing playbook", "Shopify App Store listing playbook", "Slack App Directory listing playbook", "OpenAI GPT Store listing playbook", "Stripe Marketplace listing playbook", "Atlassian Marketplace listing playbook", "Microsoft AppSource listing playbook", "Partner enablement certification tier matrix", "Co-marketing campaign brief template", "Joint Marketing Agreement (JMA)", "MDF approval matrix", "MDF Proof of Performance (POP) requirements", "Channel pricing tier matrix", "Deal registration workflow", "Channel conflict resolution flow", "Integration roadmap template", "Partnerstack workflow reference", "Tackle workflow reference", "Allbound + Impartner workflow reference", "Crossbeam account mapping playbook", "Reveal account mapping playbook", "Snowflake Native Apps account mapping", "Partner scorecard template", "Partner-sourced pipeline attribution model", "Ecosystem map template", "Partner-led webinar playbook", "Partner Advisory Board (PAB) playbook", "Partner NPS survey template", "Partner NPS benchmarks", "90-day partner onboarding playbook", "Integration health monitoring stack", "Joint customer story production", "QBR template", "Off-boarding + termination playbook", "Partner technology categories", "Partnership success metrics", "Partner benchmarks", "SOTA tool reference".

For provenance, see `SOURCES.md`.

---

## Capability reference

### Partnership motions this agent handles

- Partner sourcing + PICP definition
- Referral partner program (agreement + commission + attribution)
- Affiliate program (CPA / CPL + cookie window + promotional channels)
- Channel reseller program (margin + MDF + certifications + deal-reg)
- Integration partnerships (joint roadmap + API surface + monitoring)
- OEM partnerships (private-label + revenue share + exclusivity)
- AWS / Azure / GCP cloud marketplace listings
- Salesforce AppExchange listing
- HubSpot / Shopify / Slack / OpenAI / Stripe / Atlassian / AppSource listings
- Partner enablement + certification programs
- Co-marketing campaign design + Joint Marketing Agreement
- MDF allocation + tracking
- Channel pricing + discount tier design
- Integration roadmap planning with product
- Partnerstack / Tackle / Allbound / Impartner channel management
- Crossbeam / Reveal account mapping for co-sell
- Quarterly partner scorecards
- Ecosystem mapping + tech-stack discovery
- Partner-led webinars + events
- Partner-sourced pipeline tracking
- Deal registration + channel conflict resolution
- Partner Advisory Board (PAB)
- Partner NPS + satisfaction survey
- 90-day partner onboarding plan
- Tech-partner integration health monitoring
- Joint customer story production
- Quarterly Business Reviews (QBR) with strategic partners
- Partner CRM / PRM hygiene
- Off-boarding + termination

### Partnership technology categories (for reference)

- **PRM (Partner Relationship Management):** Partnerstack, Tackle.io, Allbound, Impartner, Channeltivity, Magentrix, Mindmatrix, PartnerTap, ZINFI, Salesforce PRM (Sales Cloud Partner Communities), HubSpot Partner Hub
- **Account mapping / ecosystem intelligence:** Crossbeam, Reveal, PartnerTap, Snowflake Native Apps (Data Clean Room), Databricks Delta Sharing
- **Cloud marketplaces:** AWS Marketplace, Azure Marketplace, GCP Marketplace
- **SaaS marketplaces:** Salesforce AppExchange, HubSpot App Marketplace, Shopify App Store, Slack App Directory, OpenAI GPT Store, Stripe Marketplace, Atlassian Marketplace (Cloud + DC), Microsoft AppSource, Pipedrive Marketplace, Zoom App Marketplace, Notion Integration Gallery, Zapier Integrations
- **Marketplace co-sell orchestration:** Tackle.io, AWS APN Customer Engagements (ACE), Microsoft Co-Sell Ready, Google Cloud Partner Advantage
- **iPaaS / integration platforms:** Zapier, Make, Tray.io, Workato, Boomi, Mulesoft, Celigo
- **Partner LMS:** HubSpot Academy, Salesforce Trailhead, Allbound LMS, Mindtickle, Highspot, Seismic, Canvas LMS, LearnUpon, Litmos, Docebo
- **Contracts + e-sign:** PandaDoc, DocuSign, Ironclad, ContractWorks, HelloSign (Dropbox Sign), Adobe Acrobat Sign
- **Partner sourcing:** Crunchbase, Pitchbook, LinkedIn Sales Navigator, Apollo.io, Clay.com, G2, Capterra, BuiltWith, Wappalyzer, Owler, ZoomInfo
- **MDF management:** Partnerstack MDF module, Impartner MDF, Allbound MDF, Channel Mechanics
- **Partner analytics:** Partnerstack analytics, Tackle Cloud GTM dashboard, custom Snowflake / Databricks / BigQuery warehouse, PostHog (for integration adoption)
- **Joint webinar + event platforms:** Zoom Webinars, Goldcast, ON24, Demio, Restream, BigMarker, Zuddl, vFairs
- **Deal registration / opportunity management:** Salesforce PRM, HubSpot Deal Properties, Impartner Deal Reg, Allbound Deal Reg, Partnerstack opportunity tracking
- **Survey + Partner NPS:** Typeform, Google Forms, HubSpot Surveys, SurveyMonkey, Delighted, Qualtrics, Wootric (InMoment)

### Partnership archetypes (which contract shell to use)

| Archetype | Commercial mechanic | Key terms | Typical motion |
|---|---|---|---|
| Referral | One-time commission % per closed-won (10-30%) | Attribution window (60-90 days), no resale rights, who closes the deal (vendor closes) | Inbound referrer model — partner sends leads |
| Affiliate | CPA or CPL (per-action / per-lead) | Cookie window (30-90 days), allowed promotional channels (no brand-bidding paid search, no spam), payout cadence | Performance marketing partners + content creators |
| Channel reseller | Margin (15-30%) + MDF + deal-reg uplift | Tier (Authorized / Silver / Gold), certifications required, MDF eligibility, territory carve-outs, MAP enforcement | Reseller sells under own brand; vendor invoices reseller or end-customer |
| Integration partner | Mutual access (APIs, sandboxes, joint roadmap) + co-marketing rights | API access scope, joint roadmap, IP / data terms, co-branding rights, monitoring + ownership of post-launch metrics, no $$ between parties typically | Tech ecosystem motion — joint customers benefit |
| OEM | Private-label + revenue share + exclusivity windows | Revenue share % (10-50%), exclusivity (segment / geography / time-bound), white-label vs co-branded, IP escrow, transition rights on termination | Embedded / white-label use — partner re-sells under own brand |

---

## PICP scoring rubric

**Partner ICP (PICP) — 100-point composite, ≥ 70 enters pipeline.**

| Axis | Weight | Score 0 | Score 25 | Score 50 | Score 75 | Score 100 |
|---|---|---|---|---|---|---|
| Customer overlap (ICP fit) | 25 | Different ICP | Adjacent ICP | Partial overlap | Strong overlap | Same ICP, same segment, same geo |
| Tech-stack fit (complementary vs competitive) | 25 | Direct competitor | Adjacent / risk of cannibalization | Neutral | Complementary | Pre-existing integration interest + already adjacent in customer tech-stacks |
| Geography | 15 | No overlap | Regional only | Multi-region overlap | Same primary market | Same primary market + secondary expansion fit |
| Segment (SMB / Mid / Ent) | 15 | Different segment | Adjacent segment | Same segment broadly | Same segment + size band | Same segment + size band + similar buyer persona |
| Motion + commercial fit | 20 | Hostile motion | Awkward fit | Acceptable | Strong fit (referral or integration) | Strong fit + both-sides value already articulated |

**Roll-up:** Sum across 5 axes = score out of 100.
- **≥ 70:** Enter partnership pipeline. Outreach hypothesis required.
- **50-69:** Light-touch (link exchange, occasional co-content); not strategic.
- **< 50:** Decline — record reason in partner DB.

---

## Referral agreement template

```markdown
# Referral Partnership Agreement — [Vendor] × [Partner]

## 1. Parties + effective date
**Vendor:** [Legal name + address]
**Partner:** [Legal name + address]
**Effective date:** [YYYY-MM-DD]

## 2. Referral mechanics
- **Definition:** A "Referral" = an introduction to a Prospect that meets Vendor's ICP and has not been in Vendor's CRM with active engagement in the past 90 days.
- **Submission:** Referrals submitted via [Vendor referral portal URL] or Partnerstack with: Prospect company, contact name + email, brief context.
- **Vendor confirmation:** Vendor confirms within 5 business days: accepted / declined / duplicate.
- **Attribution window:** 90 days from confirmed Referral.

## 3. Commission
- **Rate:** [X%] of net new ARR / contract value from closed-won deal originating from an accepted Referral within attribution window.
- **Payment:** Paid quarterly within 30 days of customer payment received; subject to customer not churning within 90 days (clawback).
- **Cap:** [optional cap per deal or annual cap].

## 4. Restrictions
- No resale rights; Vendor closes the deal and invoices the customer directly.
- No representation of Vendor as agent or authorized reseller.
- No brand-bidding on Vendor's trademarks in paid search.
- No spam / unsolicited bulk email tactics.

## 5. Term + termination
- **Term:** 1 year, auto-renewing in 1-year increments unless either party gives 60 days written notice.
- **Termination for convenience:** 60-day notice; commission obligations for Referrals already in pipeline survive termination.
- **Termination for cause:** material breach + 30-day cure period.

## 6. Confidentiality + IP
- Mutual NDA; standard 3-year obligation; trade secrets perpetual.
- No transfer of IP between parties.

## 7. General
- Independent contractors; no agency / partnership / joint venture.
- Governing law: [State].
- Dispute resolution: [arbitration / venue].
- Limitation of liability: capped at fees paid in trailing 12 months.

[Signature blocks]
```

---

## Affiliate agreement template

Differences from referral: payout per action (signup / trial / lead) not per closed-won; cookie window 30-90 days; explicit allowed/banned promotional channels; payout often via Partnerstack / Impact / Tune affiliate platform; lower commission %; higher volume / less customization.

Key clauses to add:
- **Allowed channels:** content marketing, owned email list, social, paid (with brand-bid restrictions), webinars.
- **Banned channels:** brand-bid PPC on Vendor trademarks, spam, comparison-fraud sites, paid placements on blacklisted networks, incentivized signup.
- **Cookie window:** 60 days standard; first-touch or last-touch attribution model spelled out.
- **Payout:** monthly via Partnerstack / Impact; minimum $50 threshold.
- **Performance review:** at 90 days, affiliate must have produced > [N] qualified actions or risks deactivation.

---

## Channel reseller agreement template

```markdown
# Channel Reseller Agreement — [Vendor] × [Reseller]

## 1. Parties + effective date
[…]

## 2. Reseller appointment
- **Territory:** [Geographic carve-out, e.g., "United States, excluding Federal/State govt"]
- **Segment:** [SMB / Mid-market / Enterprise / Industry-vertical]
- **Tier:** [Authorized / Silver / Gold] — see Tier Matrix exhibit
- **Non-exclusive** unless explicitly agreed.

## 3. Tier criteria + margin
| Tier | Margin % | Annual revenue commit | Certifications required | MDF eligibility |
|---|---|---|---|---|
| Authorized | 15% | $0 (no commit) | None | No |
| Silver | 20% | $100K | 1 cert / 2 reps | Yes ($5K/quarter cap) |
| Gold | 25% | $500K | 3 certs / 5 reps + cust-sat ≥ 8 | Yes ($25K/quarter cap) |

- **Deal-reg uplift:** +5 pts margin on validated deal registrations.
- **MAP (minimum advertised price):** Reseller may not advertise below Vendor's MAP without prior approval.

## 4. Deal registration
- Reseller submits via [portal] within 5 business days of qualified opportunity discovery.
- Vendor confirms approval / conflict within 48 hours.
- Approved registration grants 60-day protected window with margin uplift.
- Vendor maintains right to direct-sell to accounts where no valid registration exists.

## 5. MDF (Market Development Fund)
- Eligibility tied to tier; cap per quarter per tier.
- Each MDF request requires: activity, business case, expected pipeline, claim period.
- Proof of Performance (POP) required before payout: receipts, attendance lists, UTM-tagged metrics.

## 6. Certifications
- Reseller reps must complete Vendor-certified training program; certification renewable annually.
- Tier eligibility tied to certified-rep count.

## 7. Customer relationship + data
- Reseller owns customer relationship; Vendor entitled to customer-success data (NPS, usage) for joint-account customers.
- DPA exhibit if applicable; sub-processor disclosure required.

## 8. Term + termination
- **Term:** 1 year, auto-renew with annual review.
- **Termination for convenience:** 90-day notice. Open opportunities at termination: 60-day wind-down to close or transition.
- **Termination for cause:** material breach + 30-day cure; customer-sat detractor for 2 consecutive quarters; certification revocation.

## 9. Confidentiality + IP + general
[Standard]
```

---

## Integration partnership agreement template

Distinct from referral / reseller — typically no $$ between parties; agreement is API access + co-marketing rights + roadmap commitment + monitoring ownership.

Key clauses:
- **API access scope:** which APIs each side gives the other, rate limits, sandbox terms.
- **Joint roadmap:** quarterly roadmap session; minimum 30-day notice on deprecating features that affect joint customers.
- **Co-marketing rights:** logo usage, joint customer story rights (each side approves), joint case studies subject to customer sign-off.
- **Integration health monitoring:** named owner on each side; SLA on outage response (e.g., 4 business hours for P0 customer-impacting integration breakage); monitoring stack (Sentry + PostHog tags + shared dashboard).
- **IP + data:** customer data flowing through integration governed by each side's DPA; no derivative-IP claims; integration code IP per "joint work" classification (typically: each side owns its own contribution).
- **Term + termination:** 1-year auto-renewing; 90-day notice; obligation to support joint customers for 6 months post-termination.

---

## OEM agreement template

Highest-complexity archetype — typically multi-quarter negotiation; lawyered.

Key clauses:
- **Scope of license:** which features / version branches the partner may embed.
- **White-label vs co-branded:** per-customer decision or fixed in agreement.
- **Revenue share:** 10-50% to vendor depending on integration depth + brand value.
- **Exclusivity:** segment / geography / time-bound; usually mutual + bounded.
- **MFN (most-favored-nation):** common ask; carefully bounded.
- **IP escrow:** source-code escrow on vendor side for business-continuity.
- **Transition rights:** on termination, partner has rights to support existing customers for N months and migrate them off.
- **Audit rights:** vendor's right to audit partner's revenue calc 1×/yr.
- **Hand-off:** binding redlines + IP escrow + transition mechanics → `legal-counsel`.

---

## AWS Marketplace listing playbook

### Prerequisites
- AWS Seller registration (1 week — KYC, tax, banking).
- AWS Marketplace Management Portal (AMMP) access.
- ACE program enrollment for co-sell (separate ~1 week onboarding).

### Listing types
| Type | When | Mechanic |
|---|---|---|
| SaaS Contracts | Annual / multi-year deals; sales-led | Customer subscribes via private-offer or public listing; flat-fee or usage-fee |
| SaaS Subscriptions | Self-serve, hourly / monthly billing | API-metered usage; customer billed by AWS |
| Container | Containerized SaaS | ECR repo + container product |
| AMI | EC2-instance-based | AMI in EC2 + product listing |
| Professional Services | Implementation / consulting | Service product type |

### Listing asset checklist
- [ ] Logo (256×256 PNG, transparent background)
- [ ] Product hero image (1024×512)
- [ ] 4-6 product screenshots (1280×720+)
- [ ] Demo video (2-5 min, YouTube/Vimeo hosted; embed URL)
- [ ] Product title (60 char) + tagline (160 char)
- [ ] Product description (long-form, supports markdown)
- [ ] Categories + search keywords
- [ ] Pricing tiers (Public listing or Private offer)
- [ ] Support email + support tier description
- [ ] EULA (custom or AWS Standard Contract for SaaS — SCS)
- [ ] Compliance attestations (SOC 2, HIPAA, FedRAMP if applicable)
- [ ] Refund policy
- [ ] Region availability

### Co-sell readiness (ACE)
- [ ] APN account linked
- [ ] Sales Customer Engagement (SCE) workflow set up
- [ ] CRM integration for ACE opportunity sync (Tackle.io is the SOTA orchestrator)
- [ ] First reference customer story

### Submission flow
1. AMMP → Create Product
2. Upload listing assets via AMMP UI or AWS Marketplace Catalog API (`aws marketplace-catalog start-change-set`)
3. Submit for AWS review (typically 3-7 business days)
4. Address reviewer feedback
5. Publish

### CPPO (Channel Partner Private Offers)
For co-sell: allow channel partner to resell vendor SaaS via private offer in their own AWS account. Tackle.io's primary value-prop.

---

## Azure Marketplace listing playbook

### Prerequisites
- Microsoft Partner Center account (1 week — KYC, banking).
- Cloud Partner Portal (legacy) → Partner Center migration if pre-2022 onboarded.

### Listing types
- **SaaS offer** (recurring billing per customer, metered or flat)
- **Azure Application** (ARM-template deployment)
- **VM offer** (image-based)
- **Container offer** (AKS / ACR)
- **Consulting service**

### Listing asset checklist (SaaS)
- [ ] Logo (multiple sizes: 48×48, 90×90, 216×216, 350×350)
- [ ] Hero image (815×290)
- [ ] 4-9 screenshots (1280×720)
- [ ] Demo video URL
- [ ] Offer name + summary + description (markdown)
- [ ] Industries + categories
- [ ] Pricing plans (flat-rate, per-user, metered)
- [ ] Technical configuration (landing page URL, connection webhook for subscription events)
- [ ] EULA + privacy policy + support URLs
- [ ] Trial offer (optional)

### Co-Sell Ready / IP Co-Sell
- [ ] Co-Sell Ready: solution doc, references, partner sales / marketing assets
- [ ] IP Co-Sell: incremental — gets Microsoft seller incentives
- [ ] MACC eligibility for enterprise customer pre-commits

### Submission flow
1. Partner Center → New offer
2. Configure offer + listing via Partner Center UI or Partner Center API
3. Submit for Microsoft review (3-10 business days)
4. Address feedback
5. Publish (live or preview)

---

## GCP Marketplace listing playbook

### Prerequisites
- Google Cloud account + Producer Portal access
- Cloud Identity verification + Vendor agreement

### Listing types
- **SaaS via Integrated Billing** (recurring per-customer billing via GCP)
- **Click-to-Deploy** (Marketplace VM / Kubernetes app deployable from GCP)
- **Container Image**
- **Solutions** (consulting / packaged)

### Listing asset checklist
- [ ] Logo (256×256)
- [ ] Hero image (740×420)
- [ ] Screenshots (4-8, 1280×720)
- [ ] Demo video URL
- [ ] Solution name + tagline + description
- [ ] Categories + search tags
- [ ] Pricing (subscription tiers + metered usage)
- [ ] EULA + privacy policy + support
- [ ] Compliance attestations

### Co-sell motion
- Google Cloud Partner Advantage program enrollment
- Partner Sales Console for opportunity sync (Tackle.io = SOTA orchestrator)

### Submission flow
1. Producer Portal → Create solution
2. Upload listing assets + technical config
3. Submit for Google review (5-10 business days)
4. Address feedback
5. Publish

---

## Salesforce AppExchange listing playbook

### Prerequisites
- AppExchange Partner Program enrollment (free tier exists; paid tiers for distribution / advanced features)
- Org type: Developer Edition or Partner Business Org (PBO) for packaging
- Security Review readiness — this is the long pole

### Security Review (6-12 weeks)
- Mandatory for any package distributed on AppExchange
- **Pre-submit:**
  - Run `sfdx scanner:run` over the package — resolve all critical + high findings
  - Run penetration test if Vendor has resources (required for some categories)
  - Complete Security Review Questionnaire (200+ questions on data handling, OAuth scopes, sub-processors)
  - Review the OWASP Top 10 against your codebase
- **Submission flow:**
  1. Submit Security Review request via Partner Console
  2. Salesforce reviewer assigned (3-5 business days)
  3. Initial review (3-4 weeks); response within 5 business days
  4. Address findings; resubmit
  5. Final approval (1-2 weeks)

### Listing Asset Bundle
- [ ] Listing logo (256×256)
- [ ] Featured image (1280×400)
- [ ] Screenshots (5-15, 1280×720)
- [ ] Demo video (mandatory, 2-3 min, AppExchange-hosted or YouTube)
- [ ] Listing title + tagline + description
- [ ] Categories + industries + Salesforce editions supported
- [ ] Pricing tiers
- [ ] Support email + support tier description
- [ ] Trial / managed package installation URL

### Marketing Plan
Required by AppExchange — outlines GTM, target customers, marketing budget. Reviewed by Salesforce.

### ISVForce program
For ISV partners distributing via AppExchange. Provides packaging environment + Trial Org Templates + co-marketing + AppExchange placement.

### Trailblazer DX badge
Once approved, get the Trailblazer DX badge on AppExchange — increases visibility.

---

## HubSpot App Marketplace listing playbook

### Prerequisites
- HubSpot App Partner Program enrollment (free)
- Developer account + App created (OAuth 2.0)

### Asset checklist
- [ ] App logo (square)
- [ ] Screenshots (4-8)
- [ ] Demo video URL
- [ ] App name + tagline + description (markdown)
- [ ] Pricing tier
- [ ] OAuth scopes (minimize ask)
- [ ] Privacy policy + terms + support URLs
- [ ] HubSpot integrations (data sync depth, custom objects, webhooks used)

### Submission
- Developer Account → Apps → Submit for review (typically 2-4 weeks)
- HubSpot reviews on: OAuth scope justification, user experience, listing completeness, app testing

---

## Shopify App Store listing playbook

### Prerequisites
- Shopify Partners account
- App created via Partners dashboard
- Embedded App SDK or Custom App framework

### Built for Shopify badge
Additional certification — requires meeting performance, UX, accessibility standards. Gives prominence in App Store.

### Asset checklist
- [ ] App icon (1200×1200 PNG)
- [ ] Screenshots (3-5, 1600×1000)
- [ ] Demo video URL
- [ ] App title + tagline + description
- [ ] Categories + search tags
- [ ] Pricing model (free / one-time / recurring / usage)
- [ ] OAuth scopes
- [ ] Privacy policy + terms + support
- [ ] Demo store URL (highly recommended)

### Submission
- Partners → Apps → App listing → Submit for review (typically 1-3 weeks)
- Reviews focus on UX, performance (Core Web Vitals on embedded pages), and feature claims

---

## Slack App Directory listing playbook

### Prerequisites
- Slack App created via api.slack.com
- App manifest (manifest.yml) + OAuth scopes minimized

### Asset checklist
- [ ] App icon (512×512 PNG)
- [ ] Screenshots (1-5, 1920×1080)
- [ ] Demo video (recommended)
- [ ] App name + short + long description
- [ ] Categories + search tags
- [ ] Privacy policy + terms + support URL
- [ ] Pricing (free / paid / freemium)
- [ ] Distribution scope (workspace / org / enterprise)

### Slack App Directory submission
- Slack reviews: OAuth justification, distribution method, listing quality, feature claims (typically 2-3 weeks)

---

## OpenAI GPT Store listing playbook

### Prerequisites
- ChatGPT Plus or Team or Enterprise subscription
- Builder Profile (verified domain or LinkedIn)
- GPT created via builder.openai.com or via Custom Actions API

### Asset checklist
- [ ] GPT icon (1024×1024 PNG)
- [ ] GPT name + description
- [ ] Conversation starters (3-4 prompts)
- [ ] Instructions (system prompt)
- [ ] Capabilities enabled (Web browsing, DALL-E, Code Interpreter, Actions)
- [ ] Actions (if any) — OpenAPI schema + auth scheme
- [ ] Privacy policy URL (required for Actions)

### Submission
- Submit via builder.openai.com → Publish
- GPT Store auto-approves most non-Action GPTs; Actions get a human review (1-7 days)

---

## Stripe Marketplace listing playbook

### Prerequisites
- Stripe account + Stripe Connect platform setup
- Verified business profile

### Listing types
- **App** (Stripe App built with Stripe Apps SDK, distributed in App Marketplace)
- **Partner directory** (vendor profile in Stripe's Partner Ecosystem)

### Asset checklist (Stripe App)
- [ ] App icon
- [ ] Screenshots
- [ ] App name + description
- [ ] Pricing (free / paid)
- [ ] Privacy + terms + support
- [ ] Stripe Connect role (Express / Custom / Standard) if applicable

### Submission via Stripe Dashboard → Apps (1-3 week review)

---

## Atlassian Marketplace listing playbook

### Prerequisites
- Atlassian Marketplace Vendor account
- App built for Atlassian Forge (cloud) or Connect framework (older cloud) or Server / Data Center

### Versions
- Cloud (Forge or Connect) — most growth
- Data Center (Forge for DC + Plugin framework) — enterprise
- Server (deprecated — Atlassian sunsetting)

### Asset checklist
- [ ] App logo + banner
- [ ] Screenshots
- [ ] Description + features
- [ ] Pricing tiers (per-user, flat, free)
- [ ] Security + privacy (Atlassian Cloud Fortified program for enterprise creds)
- [ ] App version compatibility

### Submission
- Marketplace Vendor portal → Submit for approval (typically 1-2 weeks)
- Cloud Fortified program adds 4-6 weeks but unlocks enterprise customers

---

## Microsoft AppSource listing playbook

### Prerequisites
- Microsoft Partner Center account
- AppSource publishing entity registered

### Listing types
- **SaaS offer** (most common — recurring billing via AppSource or external)
- **Office Add-in** / **Teams app** / **Dynamics 365 app**
- **Consulting service**

### Asset checklist (similar to Azure Marketplace)
- [ ] Logo + hero + screenshots + video
- [ ] Offer name + summary + description
- [ ] Industries + categories
- [ ] Pricing tiers
- [ ] Trial offer (optional)
- [ ] Co-Sell Ready / IP Co-Sell readiness

### Submission via Partner Center → Marketplace → New offer → AppSource (3-10 business days)

---

## Partner enablement certification tier matrix

### Three-tier certification pattern

| Tier | Training | Assessment | Practical | Outcome |
|---|---|---|---|---|
| Foundation | 2-hour LMS module | 20-question MC quiz, 80% pass | None | "Aware" — basic product knowledge |
| Specialist | 8-hour course + product playbook | 40-question case-based + scenario | Live demo to certified instructor | "Capable" — can pitch + demo solo |
| Expert | 20-hour deep dive + integration architecture | 60-question + presentation | Build a custom integration / configure complex scenario | "Authoritative" — can lead joint customer engagements |

### Annual renewal cadence
- All certs expire 12 months from issue date
- 4-hour "delta" module covers product changes; assessment 60% length of original

### Tracking
- Per-partner certification status stored in CRM custom object (`Partner_Certification__c`); fields: cert level, issue date, expiry date, renewal status, certified rep names
- Quarterly hygiene: flag expiring within 60 days; send renewal reminder via `gmail-mcp`

### LMS platform choices
- HubSpot Academy (free + branded for HubSpot partners)
- Salesforce Trailhead (free + Trailblazer DX badges)
- Allbound LMS (paid PRM-integrated)
- Canvas LMS (open-source, self-hosted)
- Mindtickle / Highspot / Litmos (paid, enterprise)

---

## Co-marketing campaign brief template

```markdown
# Co-Marketing Campaign Brief — [Vendor] × [Partner]

## 1. Objective
- Joint goal (1 sentence): ___
- Measurable target: [pipeline $ / signups / webinar attendees / co-branded asset downloads]

## 2. Audience
- Joint ICP: ___
- Distribution split:
  - Vendor audience size: ___ (channels)
  - Partner audience size: ___ (channels)

## 3. Messaging frame
- Joint positioning (1 paragraph): ___
- Vendor's angle: ___
- Partner's angle: ___
- Joint customer benefit: ___

## 4. Asset suite
| Asset | Owner | Due date | Distribution | UTM |
|---|---|---|---|---|
| Joint 1-pager | Vendor design | YYYY-MM-DD | Both sites | utm_source=joint-1pager |
| Webinar deck | Vendor PM | YYYY-MM-DD | Webinar | utm_source=joint-webinar |
| Customer story | Partner content | YYYY-MM-DD | Both blogs + LinkedIn | utm_source=joint-customer-story |
| Demo video | Joint produce | YYYY-MM-DD | YouTube + both sites | utm_source=joint-demo-video |
| Blog series | Vendor + Partner | YYYY-MM-DD | Both blogs | utm_source=joint-blog-N |
| Email blast | Both lists | YYYY-MM-DD | Vendor + Partner email | utm_source=joint-email-N |

## 5. Distribution + cadence
- Week 1: announcement blog + email; LinkedIn organic both sides
- Week 2: joint webinar (registration page = HubSpot landing page; UTM split by partner)
- Week 3: customer story published both sides + paid retargeting (cross-agent: `marketing-agent`)
- Week 4: post-webinar follow-up; lead-routing (Vendor leads → Vendor CRM; Partner leads → Partner CRM; joint leads → both)

## 6. Measurement
- Shared dashboard URL: ___
- Reporting cadence: weekly during campaign + post-mortem in week 6

## 7. Budget
- Vendor contribution: $___ (MDF eligible?)
- Partner contribution: $___ (MDF eligible?)
- Joint paid spend: $___

## 8. JMA (Joint Marketing Agreement)
- Signed: yes / no — link to PandaDoc envelope
- Brand-usage rules: logos, taglines, customer-name usage all signed off
```

---

## MDF approval matrix

| Activity | Tier eligibility | Cap per quarter | Required POP |
|---|---|---|---|
| Local event sponsorship | Silver+ | $5K | Invoice + attendance list + post-event report |
| Joint webinar production | Silver+ | $3K | Recording + registration list + analytics screenshot |
| Joint paid ads | Gold | $10K | UTM-tagged campaign metrics + invoices |
| Custom co-marketing asset (case study, video) | Silver+ | $5K | Asset published on partner site + view metrics |
| BDR campaign (cold outbound to overlap accounts) | Gold | $15K | Outreach data + meetings booked + post-campaign report |
| Sales enablement (training program for partner sellers) | Gold | $10K | Attendance + assessment results |
| Customer-event hosted by partner | Gold | $20K | Registration + attendance + customer testimonials |

### Approval routing
- Request submitted → channel manager review → if > $5K → finance reviewer → if > $15K → director sign-off
- 5-business-day SLA on approval / rejection
- Approved requests get pre-auth code; partner executes; submits POP within 30 days of activity end; payout within 30 days of POP approval

---

## Channel pricing tier matrix

| Tier | Margin % | Annual revenue commit | Certifications | MDF | Deal-reg uplift | MAP compliance |
|---|---|---|---|---|---|---|
| Authorized | 15% | $0 | 0 | No | 0 | Required |
| Silver | 20% | $100K | 1 cert / 2 reps | Yes ($5K/qtr) | +5 pts on deal-reg | Required |
| Gold | 25% | $500K | 3 certs / 5 reps + cust-sat ≥ 8 | Yes ($25K/qtr) | +10 pts on deal-reg | Required |

### Tier transitions
- Reviewed quarterly + at annual renewal
- Upgrade triggers: hitting next-tier commit + cert + cust-sat thresholds
- Downgrade triggers: missing commit for 2 quarters + cust-sat detractor; 90-day cure period offered first

### Discount approval matrix
- Reseller discount to customer up to MAP: no Vendor approval needed
- 0-10% below MAP: channel manager approval
- 10-20% below MAP: director approval
- > 20% below MAP: escalate to `finance-controller`

---

## Deal registration workflow

```
Partner discovers opportunity
  ↓
Partner submits via [portal] within 5 business days
  Form fields: prospect company, contact name + email, deal size hypothesis,
              close date hypothesis, current eval status, scope, justification
  ↓
Vendor channel manager reviews within 48 hours
  Checks:
    ✓ Not already registered by another partner
    ✓ No active direct sales pursuit
    ✓ ICP fit
    ✓ Scope realistic
  ↓
Approve / Reject / Counter-offer
  ↓
Approved: 60-day protected window starts; deal-reg uplift +5 to +10 pts margin
Rejected: partner notified with reason (conflict / not ICP / scope issue)
Counter-offer: reduced scope or shared rep model
  ↓
Conflict path:
  First-to-register wins by default
  Tie-break: customer preference (if expressed)
  Appeal: partner → channel manager → director (escalation log in notion)
  Quarterly conflict report: # conflicts / first-to-register % / appeal-overturn %
```

---

## Channel conflict resolution flow

When two parties claim the same opportunity:

1. **Verify timestamps + scope.** Pull both submissions; check first-to-register; check scope overlap.
2. **Default rule:** first valid registration wins.
3. **Exceptions:**
   - Customer expressed preference for a specific party → honor customer preference
   - Scope mostly non-overlapping → split (one party on Module A, other on Module B)
   - Pre-existing relationship documented → grandparent
4. **Appeal path:** losing party may appeal to channel manager within 5 business days.
5. **Channel manager decision** (binding) within 5 business days.
6. **Logged** in conflict register (`notion` DB) for quarterly trend review.

### Quarterly conflict report
- Total conflicts
- First-to-register sustained %
- Appeals filed / overturned
- Customer-preference-driven overrides
- Per-partner conflict rate (high → audit territory/segment design)

---

## Integration roadmap template

```markdown
# Joint Integration Roadmap — [Vendor] × [Partner]

## 1. Vision (1 paragraph)
What the integration enables for joint customers.

## 2. Use cases (top 3-5)
| Use case | Trigger | Data flow | Customer value |
|---|---|---|---|
| ___ | ___ | Vendor → Partner | ___ |

## 3. API surface
- **Vendor APIs we'll expose:** [list endpoints, auth, rate limits, versioning]
- **Partner APIs we'll consume:** [list endpoints, auth, rate limits, versioning]
- **Webhook events on both sides:** [list]

## 4. Architecture diagram (DrawIO link)
[link to architecture diagram showing data flow + auth + monitoring]

## 5. Versioning + SLA
- API versioning model: [SemVer / dated]
- Deprecation notice: 90 days minimum for breaking changes
- Customer-impacting outage SLA: P0 = 4 business hours response; P1 = 24 hr; P2 = 5 business days

## 6. Launch milestones
| Milestone | Owner | Due date | Status |
|---|---|---|---|
| Joint design review complete | Both PMs | YYYY-MM-DD | ☐ |
| Sandbox access mutual | Both Eng | YYYY-MM-DD | ☐ |
| First joint customer beta-tested | Both CSMs | YYYY-MM-DD | ☐ |
| Co-marketing launch package ready | Both Mktg | YYYY-MM-DD | ☐ |
| Joint launch announcement | Both | YYYY-MM-DD | ☐ |
| Integration health monitoring stack live | Both Eng | YYYY-MM-DD | ☐ |
| 30-day post-launch joint retro | Both | YYYY-MM-DD | ☐ |

## 7. Joint customer commit list (≥ 3)
| Customer | Status | Owner |
|---|---|---|

## 8. Monitoring stack (post-launch)
- Vendor side: Sentry (errors), PostHog (adoption), shared dashboard
- Partner side: [their stack]
- Joint dashboard: [URL]
- Owner of integration health on each side: [name]

## 9. Co-marketing rights
- Logo usage: both sides approved
- Joint case study rights: subject to customer approval
- Co-branded asset library URL: ___

## 10. Hand-offs
- Scoping + engineering capacity: `product-manager` (Vendor side); their equivalent on partner side
- Legal terms (API access, data, IP): `legal-counsel`
- Customer-success hand-off post-launch: their CSM team + ours
```

---

## Crossbeam account mapping playbook

### Setup (one-time per partner)
1. Onboard partner to Crossbeam (free tier supports first overlap report; paid for ongoing).
2. Connect both sides' CRMs to Crossbeam (HubSpot / Salesforce / Pipedrive).
3. Each side defines populations: Customers, Open Pipeline, Lead List.

### Overlap reports
- Run "Joint Overlap" report — automatic privacy-preserving join.
- Categorize results:
  - **Their customers we're not in** → outbound list for joint outreach (use partner's customer relationship to warm intro)
  - **Our customers they're not in** → reverse outbound (we intro)
  - **Joint pipeline** (both in active opps with same prospect) → co-sell motion + deal-reg sync
  - **Joint customers** → upsell / cross-sell + joint customer story candidates
- Refresh weekly.

### Co-sell motion
- For joint pipeline accounts: shared Slack channel; joint discovery; joint demo; joint MAP
- Use `partner-sourced-pipeline-tracking` skill to attribute correctly

### Mapped attributes
- Customer name, industry, size, geo, our deal stage, their deal stage, joint owner

---

## Reveal account mapping playbook

Same shape as Crossbeam. Reveal is stronger in Europe; Crossbeam stronger in US. Some partners use both. The Reveal API is functionally equivalent.

---

## Snowflake Native Apps account mapping

For data-mature partners with Snowflake warehouses, native Snowflake account mapping = Snowflake Native Apps + Data Clean Room.

- Each side publishes a Native App with their CRM data tables (de-identified or hashed PII).
- Joint app computes overlap inside the Clean Room — neither side sees raw rows.
- Result tables shared back to each side's warehouse.
- Best for: data teams; large strategic partners; regulated industries.

---

## Partner scorecard template

```markdown
# Partner Scorecard — [Partner Name] · Q[N] [Year]

## Tier + status
- Current tier: ___ (Authorized / Silver / Gold)
- Tier eligibility next quarter: ___ (per upgrade/downgrade criteria)
- Overall health: 🟢 Green / 🟡 Yellow / 🔴 Red

## Pipeline metrics
| Metric | This quarter | Last quarter | Target | Status |
|---|---|---|---|---|
| Opportunities sourced | ___ | ___ | ≥ N | 🟢/🟡/🔴 |
| Pipeline $ sourced | $___ | $___ | ≥ $N | 🟢/🟡/🔴 |
| Closed-won | ___ | ___ | ≥ N | 🟢/🟡/🔴 |
| Closed-won $ | $___ | $___ | ≥ $N | 🟢/🟡/🔴 |
| Win rate | __% | __% | ≥ 25% | 🟢/🟡/🔴 |

## Enablement metrics
| Metric | Status |
|---|---|
| Certified reps: foundation / specialist / expert | ___ / ___ / ___ |
| Active reps in last 90 days | ___ |
| Sandbox access utilization | __% |

## MDF metrics (resellers / channel partners)
| Metric | Status |
|---|---|
| MDF allocated this quarter | $___ |
| MDF spent | $___ |
| Spend ratio | __% |
| Pipeline generated from MDF | $___ |
| MDF ROI (pipeline $ / MDF spent) | __× |

## Customer satisfaction
| Metric | Status |
|---|---|
| Joint customer NPS | ___ |
| Joint customer count (active) | ___ |
| Joint customer churn (this quarter) | ___ |

## Integration health (tech partners)
| Metric | Status |
|---|---|
| Integration error rate | __% |
| Integration adoption (% of joint customers using) | __% |
| API call volume (this quarter) | ___ |
| Customer-impacting incidents | ___ |

## Top 3 wins this quarter
1. ___
2. ___
3. ___

## Top 3 challenges
1. ___
2. ___
3. ___

## Next-quarter joint goals
1. ___ (owner: ___, due: ___)
2. ___
3. ___

## Asks from partner / asks from us
- Partner asks: ___
- Vendor asks: ___
```

---

## Partner-sourced pipeline attribution model

### CRM source-field discipline
- Every opportunity has a `Source` field (Partner, Direct, Inbound-self-serve, Marketing-content, Event)
- For Partner-source: required sub-field `Partner_ID` (link to partner record)
- Required for commission accounting and scorecard generation

### Attribution model choices
| Model | When | Impact |
|---|---|---|
| First-touch | Partner-originated leads | Simple; rewards initial discovery |
| Last-touch | Multi-touch deals | Rewards closer; Partnerstack default |
| Multi-touch | Mature partner programs | Splits commission across partners who touched |
| Position-based (W-shape) | Enterprise complex deals | First-touch 30% + middle 40% + last-touch 30% |

### Weekly partner pipeline rollup
```sql
-- partner-sourced pipeline rollup (Postgres / Snowflake)
SELECT
  partner_id,
  partner_name,
  COUNT(*) AS opps_sourced,
  SUM(amount) AS pipeline_total,
  COUNT(*) FILTER (WHERE stage = 'Closed Won') AS closed_won,
  SUM(amount) FILTER (WHERE stage = 'Closed Won') AS revenue,
  ROUND(
    COUNT(*) FILTER (WHERE stage = 'Closed Won')::numeric /
    NULLIF(COUNT(*) FILTER (WHERE stage IN ('Closed Won', 'Closed Lost')), 0),
    3
  ) AS win_rate
FROM opportunities
WHERE source = 'Partner'
  AND created_at >= DATE_TRUNC('quarter', NOW())
GROUP BY partner_id, partner_name
ORDER BY pipeline_total DESC;
```

---

## Ecosystem map template

```
Center: [Your product]
Layer 1 (direct adjacent / complementary):
  - Cluster A: [tool 1, tool 2, tool 3]
  - Cluster B: [tool 4, tool 5]
Layer 2 (integrators / consultancies):
  - Cluster C: [SI 1, SI 2]
Layer 3 (related but not core):
  - Cluster D: [tool 6, tool 7]
Layer 4 (resellers + marketplaces):
  - Marketplaces: AWS, Azure, GCP, AppExchange, HubSpot, Shopify, ...
Outer ring: competitors (visible but not in partnership scope)
```

Render via `drawio-mcp` or `figma-mcp` or `canva-mcp`. Update quarterly. Share with strategic partners at QBR.

---

## Partner-led webinar playbook

### Pre-event (4 weeks out)
- Confirm topic + agenda + speakers (1 from each side preferred)
- Build registration page: HubSpot landing page + UTM split (utm_source=partner-webinar-[partner-id])
- Build co-branded email invitation (Vendor + Partner brand-approved)
- Schedule Zoom Webinar via `zoom-mcp` (`/scheduled-webinars`)
- Build co-branded deck (deck owner: Vendor PM; reviewer: Partner PM)
- 2 weeks: First invitation blast (both lists); LinkedIn organic + paid (`marketing-agent`)
- 1 week: Second invitation; speaker prep call
- 2 days: Final reminders; tech check

### Day-of
- Speaker prep 30 min before
- Webinar live: vendor opens, partner co-presents, joint Q&A
- Record via Zoom; auto-uploaded to cloud
- Post-event email immediately: "Thanks for joining; here's the recording + slides + offer"

### Post-event (1-2 weeks)
- Lead routing: Vendor leads → Vendor CRM; Partner leads → Partner CRM; joint leads → both
- Follow-up cadence (cross-agent: `sales-agent` runs the post-webinar SDR cadence)
- Recording + slides published on YouTube + both sites
- Post-mortem doc to `notion`: registrations / attendance / attendance rate / poll responses / leads-per-segment / pipeline-attributed (4 weeks post-event)

### Targets
- Registration → attendance: ≥ 35%
- Attendance → SQL: ≥ 8% (for ICP-tight registration list)
- SQL → pipeline: tracked at 60 days

---

## Partner Advisory Board (PAB) playbook

### Membership
- 6-12 strategic partners
- Top-tier (Gold reseller, top integration partners, OEM partners)
- ≥ 2 quarters of relationship
- Coverage: segment + geo + motion mix

### Cadence
- Quarterly meeting (60-90 min virtual or 2-day in-person summit annually)
- Annual in-person summit recommended

### Agenda template (annual summit)
- Day 1:
  - Morning: Vendor strategic update (CEO/CRO/CPO)
  - Late morning: Roadmap deep-dive (CPO + product-manager)
  - Afternoon: Partner feedback workshop (small groups, structured)
  - Evening: Networking dinner
- Day 2:
  - Morning: Joint GTM session (CRO + CMO)
  - Late morning: Co-marketing + co-sell case studies (partners present)
  - Afternoon: Next-year commitments + joint asks
  - Wrap: Joint commitment statement

### Pre-read deck (shipped 1 week prior)
- Vendor business update + state of partnership program
- Year-in-review: top-5 wins + top-3 challenges
- Roadmap items requesting partner input
- Specific asks per partner (acknowledge their context)

### Post-summit synthesis (1 week post)
- Synthesize partner feedback into prioritized partner-influenced roadmap items
- Share with `product-manager` for backlog prioritization
- Send thank-you + synthesis doc to all attendees
- Track action items in `notion` DB; revisit at quarterly PAB

---

## Partner NPS survey template

```markdown
# Partner NPS Survey — Q[N] [Year]

## Question 1 (NPS scale)
On a scale from 0 to 10, how likely are you to recommend our partner program to a peer or industry colleague?

## Question 2 (open-ended)
What's working well in our partnership? (1-3 sentences)

## Question 3 (open-ended)
What's not working as well as it could be? (1-3 sentences)

## Question 4 (open-ended)
If we could change one thing in the next quarter to improve your experience, what would it be? (1-3 sentences)

## Question 5 (closed scale, 1-5)
Rate the following:
- Quality of partner enablement (training, certifications, content): __/5
- Quality of co-marketing support: __/5
- Quality of channel manager / partner manager support: __/5
- Speed of deal-reg approvals: __/5
- MDF process clarity + speed: __/5
- Quality of joint roadmap / integration health (tech partners only): __/5

## Question 6 (optional)
Anything else you'd like to tell us?
```

### Distribution + analysis
- Send via Typeform or HubSpot Survey or Google Form
- Distribute via `gmail-mcp` (1×) + `slack-mcp` reminder to partner channel (1×)
- Target ≥ 60% response rate
- Compute NPS = (% promoters 9-10) − (% detractors 0-6); industry benchmark: > 30 healthy, > 50 best-in-class
- Segment by tier; trend over time
- Detractor recovery within 30 days (call from channel manager; recovery plan)

---

## Partner NPS benchmarks (June 2026)

| Industry | Partner NPS healthy threshold | Best-in-class |
|---|---|---|
| Cloud / infrastructure | > 30 | > 50 |
| SaaS / horizontal | > 35 | > 55 |
| Vertical SaaS | > 40 | > 60 |
| Devtool / API | > 35 | > 55 |

Detractor recovery rate target: > 50% of detractors moved to passive or promoter within 2 quarters.

---

## 90-day partner onboarding playbook

### Day 0 — Contract signed
- Welcome email from channel manager via `gmail-mcp`
- Slack channel created via `slack-mcp` `conversations.create` (#partner-[partner-id])
- LMS access provisioned (`canvas-lms-mcp` or HubSpot Academy invite)
- CRM partner record created via `api-gateway` (HubSpot custom object / Salesforce partner record)
- Onboarding task list auto-created in `notion` partner DB

### Day 1-7
- Kickoff call (60 min) with: channel manager + sponsor on both sides + product touchpoint
- Walk through: program overview, certification path, deal-reg + MDF process, joint roadmap (if integration partner)
- First training module assigned (Foundation cert)
- Sandbox / dev-env access provisioned (integration partners)

### Day 7-30
- Foundation certification completion target
- First joint customer-account list identified (Crossbeam mapping for strategic partners)
- First marketing/co-marketing brief sketched
- Weekly 30-min sync established

### Day 30
- Day-30 review call:
  - Foundation cert complete? Yes/No
  - First joint accounts identified?
  - First deal-reg submitted? (target by Day 45 for resellers)
  - Friction points

### Day 30-60
- Specialist certification (resellers) or Joint integration scoping (integration partners)
- First joint customer plan or first co-marketing campaign in flight
- First deal-reg submitted

### Day 60
- Day-60 review:
  - Specialist cert progress
  - First pipeline submission status
  - Co-marketing campaign launch status

### Day 60-90
- First joint customer story (integration partners) or first closed-won (resellers)
- Joint roadmap doc signed (integration partners)
- Tier-eligibility check

### Day 90
- Day-90 scorecard review (use `partner-scorecard-authoring` skill)
- Tier upgrade if eligible
- QBR setup
- Promote partner to active in PRM portal

---

## Integration health monitoring stack

### Metrics to track post-launch
- **Adoption:** % of joint customers using the integration (computed from CRM joint-customer list ∩ integration-active list via `posthog-mcp` `tracking_event`)
- **Volume:** API calls per partner per customer per day
- **Errors:** error rate per endpoint via `sentry-mcp`
- **Latency:** p50 / p95 / p99 per endpoint
- **Deprecation events:** scheduled vs surprise; counted per side

### Alerting thresholds
- Adoption < 30% at 90 days post-launch → ⚠ partner-manager intervention
- Error rate > 5x baseline → P0 incident (4-hr response SLA)
- Single-customer error rate > threshold → notify customer + partner CSM
- Latency p95 > 2× baseline → escalate to engineering

### Dashboard
- Shared dashboard in `posthog-mcp` or `mixpanel-mcp` or `amplitude-mcp` tagged `integration_partner_id`
- Weekly health digest → `slack-mcp` partner channel + `gmail-mcp` to channel manager
- Quarterly trend → integrated into partner scorecard

### Ownership
- Engineering: error monitoring + latency
- Product: adoption + deprecation planning
- Channel manager: customer impact + partner relationship recovery
- Cross-agent hand-off: integration scoping / deprecation planning → `product-manager`

---

## Joint customer story production

### Pre-flight checklist
- [ ] Joint customer identified with measurable outcome (cost saved, revenue gained, time reduced)
- [ ] Customer champion willing to be quoted
- [ ] Customer legal sign-off obtained
- [ ] Vendor + Partner brand + legal sign-off
- [ ] Story angle agreed (problem → both vendors' role → outcome)

### Production
1. Joint customer interview (45-60 min) via `zoom-mcp` + transcript via `fathom-api` or `gong-chorus-call-intelligence`
2. Draft 1-pager (Vendor content; Partner review)
3. Draft long-form case study (Vendor or jointly)
4. Video case study (cross-agent: `video-creator` for editing; raw interview Zoom file → MP4)
5. Quote block + win-wire (Vendor)
6. Final customer sign-off (mandatory)
7. Both sides legal sign-off

### Distribution
- Both vendors' websites + blog
- Joint LinkedIn announcement (both companies)
- Partner email list + Vendor email list (segmented to ICP-fit)
- Joint webinar + sales enablement asset

---

## QBR template

```markdown
# Quarterly Business Review — [Partner Name] · Q[N] [Year]

## Attendees
- Vendor: [Channel mgr, AE if joint customer, Product PM if integration]
- Partner: [Their channel mgr, AE, Product PM]

## Agenda (60 min)
1. (5 min) Welcome + agenda
2. (15 min) Vendor scorecard review (see attached)
3. (10 min) Partner scorecard / health (from partner side)
4. (10 min) Joint customer wins + losses
5. (10 min) Next-quarter joint goals + asks on each side
6. (5 min) Joint marketing + co-sell roadmap
7. (5 min) Action items + DRIs + due dates

## Pre-read (sent 1 week before)
- Scorecard PDF (see `partner-scorecard-authoring`)
- Joint customer list status (Crossbeam map snapshot)
- Joint roadmap update (if integration partner)
- Top-3 vendor asks + top-3 partner asks (pre-collected)

## Outcomes (logged in notion)
- Tier review: keep / upgrade / downgrade
- Next-quarter joint goals (3-5)
- Action items (each with DRI + due)
- Risks logged
- Schedule next QBR
```

---

## Off-boarding + termination playbook

### Termination triggers (documented at agreement signing)
- Missed annual revenue commit for 2 consecutive quarters
- Customer-sat detractor for 2 consecutive quarters
- Certification revoked (Reseller)
- Material breach of agreement (any partner type)
- Strategic pivot (either side discontinuing the segment / product)
- Compliance violation (data, IP, antitrust)

### Notice period
- Honor contractual notice period (typically 60-90 days)
- During notice: open opportunities continue; new deal-reg paused; MDF accrual frozen

### Off-boarding checklist
- [ ] Termination letter via PandaDoc/DocuSign (legal-counsel reviewed)
- [ ] PRM portal access revoked (`api-gateway` mass-update)
- [ ] Sandbox / dev-env access revoked (integration partners)
- [ ] LMS access revoked (or transitioned to alumni status)
- [ ] MDF unused balance reconciled (`xlsx` ledger; reconcile with `finance-controller`)
- [ ] Commission accrual finalized + paid through last quarter
- [ ] Joint customer transition plan (who supports each joint customer)
- [ ] Joint marketing assets ownership clarified (logos, joint case studies — typically removed; mutual NDA continues)
- [ ] Internal Slack channel archived
- [ ] CRM partner record marked "terminated" with reason code

### Public vs silent disposition
- Silent by default (no public announcement)
- Public only if legally mandated (material public partner) or both sides agree
- Coordinate with `marketing-agent` for messaging if public

---

## Partner technology categories quick reference

| Category | Top tools (2026) | When to use |
|---|---|---|
| PRM | Partnerstack (referral/affiliate focus), Tackle.io (cloud marketplace), Allbound (LMS-strong), Impartner (enterprise) | When > 25 partners or > 1 motion |
| Account mapping | Crossbeam (US), Reveal (EU), PartnerTap (enterprise) | When ≥ 3 strategic partners and CRM data |
| Cloud marketplace orchestration | Tackle.io | When listed on ≥ 2 of AWS/Azure/GCP |
| iPaaS / integration | Zapier (SMB), Make (mid), Tray / Workato (ent), Boomi (ent legacy) | When building no-code integration partners |
| LMS | HubSpot Academy (free for HubSpot partners), Trailhead (Salesforce), Allbound LMS (PRM-integrated), Mindtickle/Highspot (ent) | When cert program > 5 partners |
| Contracts | PandaDoc (most flex), DocuSign (enterprise), Ironclad (legal-led) | All partners |

---

## Partnership success metrics

### Partner-sourced pipeline metrics
- Partner-sourced pipeline as % of total pipeline (target: 20-30% for mature programs)
- Partner-sourced win rate vs direct (target: parity or 5% lower)
- Avg ACV partner-sourced vs direct (target: parity)
- # active partners (sourced ≥ 1 opp this quarter)
- # certified reps per active partner (target: ≥ 2)

### Program-health metrics
- Partner NPS (target: > 30; best-in-class > 50)
- % of partners with active joint roadmap (integration partners)
- % of partners with active co-marketing (channel + integration)
- MDF utilization rate (target: 70-90%)
- MDF ROI: pipeline $ per MDF $ (target: > 5×)

### Marketplace metrics
- # active marketplace listings
- Marketplace-sourced pipeline as % of total (target: 10-20%)
- Marketplace listing visibility (Tackle tracks; for AppExchange, Trailblazer DX badge)
- AppExchange security-review-pass rate (target: 100% on first cycle for healthy programs)

### Channel-conflict metrics
- Conflicts per quarter (low is good)
- First-to-register sustained %
- Appeals overturned %
- Per-partner conflict rate (high = territory/segment design issue)

---

## SOTA tool reference (June 2026)

This section is grep-only — the agent uses keyword-driven retrieval to surface the right skill pack for the user's task. Headings are intentionally search-friendly. Every entry links to a detailed `SKILL.md` in `skills/` that ships in this bundle and loads on demand.

**Full coverage map:** see `reference/SOTA_USE_CASES.md` for the per-use-case mapping and confidence rating.

### Partnerstack (referral / affiliate / reseller PRM)

Partnerstack is the SOTA PRM for referral + affiliate + reseller programs (SMB-to-mid market). Covers partner portal, commission tracking, payouts, marketing assets, lead submissions. API for partner CRUD, commission posting, payout scheduling.

- **Skill:** `skills/partnerstack-tackle-channel-management/SKILL.md`
- **Endpoint:** `https://gateway.maton.ai/partnerstack/v3/...` via `api-gateway`
- **Auth:** Maton API key → managed OAuth
- **Key calls:** `POST /partners`, `POST /transactions/commissions`, `POST /payouts/schedule`, `GET /partners/{id}/performance`
- **Source:** https://partnerstack.com/api

### Tackle.io (cloud marketplace co-sell)

Tackle is the SOTA orchestrator across AWS / Azure / GCP marketplaces — single dashboard, co-sell automation, private-offer generation, ACE / Co-Sell Ready opportunity sync. The "Salesforce of cloud marketplaces."

- **Skill:** `skills/aws-azure-gcp-marketplace-listings/SKILL.md` + `skills/partnerstack-tackle-channel-management/SKILL.md`
- **Endpoint:** `https://gateway.maton.ai/tackle/...` via `api-gateway` (if onboarded)
- **Key calls:** `POST /offers/private-offer`, `GET /opportunities/co-sell`, `POST /sync/ace-opportunity`
- **Source:** https://tackle.io/api-documentation

### AWS Marketplace Catalog API

For direct AWS Marketplace CRUD without Tackle. Authenticated via AWS CLI (`aws marketplace-catalog`) with seller-admin credentials.

- **Skill:** `skills/aws-azure-gcp-marketplace-listings/SKILL.md`
- **Tools:** `cli-anything` + `aws marketplace-catalog start-change-set`
- **Key calls:** `start-change-set` for listing updates; `describe-entity` for current state; `list-changesets` for review status
- **Source:** https://docs.aws.amazon.com/marketplace-catalog/latest/api-reference/

### Azure Partner Center API

For direct Azure Marketplace CRUD. Authenticated via Microsoft Graph + Partner Center API.

- **Skill:** `skills/aws-azure-gcp-marketplace-listings/SKILL.md`
- **Tools:** `cli-anything` + `az partner-center` or Partner Center REST
- **Key calls:** `POST /products/saas`, `PATCH /listings/{listingId}`, `POST /publications`
- **Source:** https://learn.microsoft.com/en-us/partner-center/marketplace/

### GCP Marketplace Producer Portal

For direct GCP Marketplace CRUD. Authenticated via gcloud CLI + Producer Portal REST.

- **Skill:** `skills/aws-azure-gcp-marketplace-listings/SKILL.md`
- **Tools:** `cli-anything` + `gcloud marketplace`
- **Key calls:** `gcloud marketplace solutions create`, `gcloud marketplace solutions update`
- **Source:** https://cloud.google.com/marketplace/docs/partners

### Salesforce AppExchange + Code Analyzer

Salesforce Code Analyzer is the SOTA pre-Security-Review static analysis tool. Run before submitting AppExchange package; resolve all critical + high findings.

- **Skill:** `skills/salesforce-appexchange-listing/SKILL.md`
- **Tools:** `cli-anything` + `sfdx scanner:run` (Salesforce CLI plugin)
- **Key calls:** `sfdx scanner:run --target . --format json`; AppExchange Listing CRUD via Partner Console (no public API — `playwright-mcp` for portal automation)
- **Source:** https://developer.salesforce.com/docs/atlas.en-us.code_analyzer.meta/code_analyzer/

### HubSpot App Marketplace

HubSpot Apps via OAuth 2.0; App Partner Program; listing via developer account.

- **Skill:** `skills/hubspot-shopify-slack-marketplace-listings/SKILL.md`
- **Endpoint:** `https://gateway.maton.ai/hubspot/integrations/v1/...`
- **Key calls:** OAuth app config; listing submission via developer account portal
- **Source:** https://developers.hubspot.com/docs/api/marketplace

### Shopify Partners + App Store

Shopify App Store via Shopify Partners GraphQL Admin API.

- **Skill:** `skills/hubspot-shopify-slack-marketplace-listings/SKILL.md`
- **Tools:** `cli-anything` + Shopify Partners GraphQL or `playwright-mcp` for portal upload
- **Key calls:** Partners API for app config; portal for listing CRUD
- **Source:** https://shopify.dev/docs/apps

### Slack App Directory

Slack App config + manifest.yml + App Directory submission. Native Slack MCP for app management.

- **Skill:** `skills/hubspot-shopify-slack-marketplace-listings/SKILL.md`
- **Endpoint:** `slack-mcp` for app config; Slack App Directory submission via api.slack.com portal
- **Key calls:** `apps.manifest.create`, `apps.manifest.update`, `apps.manifest.validate`
- **Source:** https://api.slack.com/start/distributing

### OpenAI GPT Store

OpenAI GPT Store + Custom Actions. Builder profile + OpenAPI schema for Actions.

- **Skill:** `skills/hubspot-shopify-slack-marketplace-listings/SKILL.md`
- **Tools:** `playwright-mcp` for builder.openai.com automation; OpenAPI schema authored in `docx`/JSON
- **Source:** https://platform.openai.com/docs/actions

### Stripe Marketplace + Stripe Connect

Stripe Apps SDK for app development; Stripe Connect for payment flows; Marketplace listing via Stripe Dashboard.

- **Skill:** `skills/hubspot-shopify-slack-marketplace-listings/SKILL.md`
- **Endpoint:** `stripe-mcp` for Connect ops; Stripe Apps SDK for app development
- **Key calls:** `POST /accounts` (Connect), `POST /transfers` (payouts to partners)
- **Source:** https://docs.stripe.com/connect

### Atlassian Marketplace API

Atlassian Marketplace + Cloud Fortified for enterprise readiness.

- **Skill:** `skills/hubspot-shopify-slack-marketplace-listings/SKILL.md`
- **Tools:** `cli-anything` + Marketplace API or `playwright-mcp` for portal
- **Source:** https://developer.atlassian.com/platform/marketplace/

### Microsoft AppSource via Partner Center

Microsoft AppSource SaaS offer + Office Add-in + Teams app + Dynamics 365 app + Consulting service.

- **Skill:** `skills/hubspot-shopify-slack-marketplace-listings/SKILL.md`
- **Tools:** `cli-anything` + Partner Center API or `playwright-mcp` for Partner Center portal
- **Source:** https://learn.microsoft.com/en-us/partner-center/marketplace/

### Crossbeam (US-leading account mapping)

Crossbeam is the SOTA account mapping platform — privacy-preserving overlap of two companies' CRMs. 650K+ companies onboarded. Strong in US.

- **Skill:** `skills/crossbeam-reveal-account-mapping/SKILL.md`
- **Endpoint:** `https://gateway.maton.ai/crossbeam/v0.3/...` via `api-gateway`
- **Key calls:** `POST /partners/search`, `POST /populations`, `GET /reports/{id}`, `POST /actions/share-overlap`
- **Source:** https://crossbeam.com/docs/api

### Reveal (EU-leading account mapping)

Reveal is the European-leaning alternative to Crossbeam. Functionally equivalent API.

- **Skill:** `skills/crossbeam-reveal-account-mapping/SKILL.md`
- **Endpoint:** `https://gateway.maton.ai/reveal/...` if onboarded
- **Source:** https://docs.reveal.co/

### Snowflake Native Apps + Data Clean Room

For data-mature partners with Snowflake warehouses. Account mapping via Native App in Data Clean Room — neither side sees raw rows; only joined / aggregated results.

- **Skill:** `skills/crossbeam-reveal-account-mapping/SKILL.md`
- **Tools:** `postgresql-mcp` (Snowflake compatible)
- **Source:** https://www.snowflake.com/blog/native-apps-collaboration/

### PandaDoc / DocuSign (partner agreements + e-sign)

PandaDoc for proposal-native partner agreements with template + CRM tokens + e-sign. DocuSign for enterprise e-sign with custom legal-source documents.

- **Skill:** `skills/referral-affiliate-channel-oem-agreement-structuring/SKILL.md`
- **Endpoints:** `https://gateway.maton.ai/pandadoc/public/v1/...`; `https://gateway.maton.ai/docusign/restapi/v2.1/...`
- **Key calls:** PandaDoc `POST /documents` (from archetype template); DocuSign `POST /envelopes`
- **Source:** https://developers.pandadoc.com/ + https://developers.docusign.com/docs/esign-rest-api/

### Allbound + Impartner + Channeltivity + Magentrix (PRM portals)

Enterprise + mid-market PRM portals with deal-reg, MDF, LMS, certifications. Allbound: LMS-strong. Impartner: enterprise. Channeltivity: mid-market. Magentrix: Salesforce-anchored.

- **Skill:** `skills/partnerstack-tackle-channel-management/SKILL.md`
- **Endpoints:** `https://gateway.maton.ai/{allbound|impartner|channeltivity|magentrix}/...` (where onboarded) or direct curl via `cli-anything`
- **Source:** https://www.allbound.com/ + https://www.impartner.com/ + https://www.channeltivity.com/

### Apollo + Crunchbase + Pitchbook (partner sourcing)

Apollo for partner-org enrichment; Crunchbase for funding events + company data; Pitchbook for private-company depth; G2 for category neighbors; BuiltWith / Wappalyzer for tech-stack discovery (via Clay).

- **Skill:** `skills/partner-sourcing-icp-definition/SKILL.md`
- **Endpoints:** `https://gateway.maton.ai/apollo/api/v1/...`, `https://gateway.maton.ai/crunchbase/api/v4/...`
- **Key calls:** Apollo `POST /api/v1/mixed_companies/search`; Crunchbase `POST /searches/organizations`
- **Source:** https://docs.apollo.io/reference/organization-search + https://data.crunchbase.com/docs

### Canvas LMS (partner certification programs)

Canvas LMS is the SOTA open-source LMS for self-hosted partner training. Native MCP available.

- **Skill:** `skills/partner-enablement-certification-programs/SKILL.md`
- **Endpoint:** `canvas-lms-mcp` for course CRUD, enrollment, assessment, certification issuance
- **Key calls:** `POST /api/v1/courses`, `POST /api/v1/enrollments`, `POST /api/v1/quizzes/{id}/submissions`
- **Source:** https://canvas.instructure.com/doc/api/

### Zoom Webinars + Goldcast + ON24 (joint webinars)

Zoom Webinars for SMB-to-mid; Goldcast for SaaS-native polished events; ON24 for enterprise with analytics depth.

- **Skill:** `skills/partner-led-webinars-events/SKILL.md`
- **Endpoint:** `zoom-mcp` for Zoom Webinars; Goldcast / ON24 via `api-gateway` if onboarded
- **Key calls:** `zoom-mcp` `/scheduled-webinars`, `/users/me/recordings`
- **Source:** https://developers.zoom.us/docs/api/rest/reference/zoom-api/

### Fathom / Gong (joint customer interviews)

For joint customer story production — record interview, transcript, extract quotes.

- **Skill:** `skills/co-marketing-campaign-design/SKILL.md` (sub-routine)
- **Endpoint:** `fathom-api` default skill or `api-gateway` Gong
- **Source:** https://help.fathom.video/en/articles/8430832-fathom-api

### Sentry (integration error monitoring)

Native MCP for integration error tracking. Tag errors by `integration_partner_id` for per-partner visibility.

- **Skill:** `skills/partnerstack-tackle-channel-management/SKILL.md` (integration health sub-routine)
- **Endpoint:** `sentry-mcp`
- **Source:** https://docs.sentry.io/

### PostHog / Mixpanel / Amplitude (integration adoption)

Track integration adoption per joint customer; tag events by `integration_partner_id`.

- **Skill:** `skills/partnerstack-tackle-channel-management/SKILL.md`
- **Endpoint:** `posthog-mcp` / `mixpanel-mcp` / `amplitude-mcp`
- **Source:** https://posthog.com/docs/api

### BuiltWith / Clay (ecosystem mapping + tech-stack)

BuiltWith for prospect tech-stack discovery; Clay for multi-source enrichment waterfall.

- **Skill:** `skills/ecosystem-mapping-tech-stack-discovery/SKILL.md`
- **Tools:** `cli-anything` + `curl https://api.builtwith.com/v15/api.json` ; Clay via `api-gateway`
- **Source:** https://api.builtwith.com/ + https://clay.com/docs/api

### DrawIO + Figma + Canva (ecosystem maps + co-branded assets)

DrawIO for ecosystem maps + integration architecture; Figma for design fidelity; Canva for co-branded assets.

- **Skill:** `skills/ecosystem-mapping-tech-stack-discovery/SKILL.md` + `skills/co-marketing-campaign-design/SKILL.md`
- **Endpoint:** `drawio-mcp` / `figma-mcp` / `canva-mcp`
- **Source:** https://www.diagrams.net/ + https://www.figma.com/ + https://www.canva.com/

### Typeform (Partner NPS surveys)

Typeform for Partner NPS distribution. HubSpot Surveys + Google Forms as alternatives.

- **Skill:** `skills/partner-nps-satisfaction-survey/SKILL.md`
- **Endpoint:** `typeform` default skill
- **Source:** https://www.typeform.com/

### Notion (partner DB + playbooks + QBR records)

Notion as the partner system of record for partner DB, playbooks, QBR records, scorecards, MDF tracking, onboarding plans, action items.

- **Endpoint:** `notion-mcp`
- **Source:** https://developers.notion.com/

### Slack + MS Teams (partner channels + alerts)

Per-partner Slack channel; deal-reg alerts; MDF approval routing; weekly digest delivery.

- **Endpoint:** `slack-mcp` + `ms-teams-mcp`
- **Key calls:** `conversations.create` (per partner); `chat.postMessage` (alerts); `slack-mcp` `webhooks`

### Maton API gateway (managed OAuth for 100+ apps)

Default skill `api-gateway` covers managed OAuth for: HubSpot, Salesforce, Apollo, Partnerstack, Tackle, Crossbeam, Reveal, PandaDoc, DocuSign, Crunchbase, Allbound, Impartner, Channeltivity, Magentrix, and 90+ more.

- **Endpoint:** `https://gateway.maton.ai/{app}/...`
- **Source:** https://gateway.maton.ai/

---

## SOTA execution playbook (which skill pack to reach for)

| User asks for | First-stop skill pack | Notes |
|---|---|---|
| Source new partner candidates | `partner-sourcing-icp-definition` | PICP rubric; Crunchbase + Apollo + LinkedIn + G2 |
| Draft a referral / affiliate / reseller / integration / OEM agreement | `referral-affiliate-channel-oem-agreement-structuring` | 5 archetypes; PandaDoc + DocuSign templates |
| Launch on AWS / Azure / GCP Marketplace | `aws-azure-gcp-marketplace-listings` | Tackle.io + cloud CLIs; asset checklist; Co-Sell Ready |
| Launch on Salesforce AppExchange | `salesforce-appexchange-listing` | sfdx scanner pre-check; Security Review prep; Listing Asset Bundle |
| Launch on HubSpot / Shopify / Slack / OpenAI / Stripe / Atlassian / AppSource | `hubspot-shopify-slack-marketplace-listings` | Per-marketplace portal + API patterns |
| Build a tiered certification program | `partner-enablement-certification-programs` | Foundation / Specialist / Expert; LMS choice |
| Design a co-marketing campaign | `co-marketing-campaign-design` | Joint plan + JMA + UTM split + measurement |
| Allocate / track MDF | `mdf-allocation-tracking` | MDF approval matrix; POP discipline; payout routing |
| Set channel pricing + deal-reg | `channel-pricing-discount-tiers` + `deal-registration-channel-conflict-resolution` | Margin tier matrix + 48h SLA + conflict log |
| Plan integration roadmap with PM | `integration-roadmap-planning` | Joint roadmap doc; API versioning; monitoring stack; cross-agent `product-manager` |
| Run Partnerstack / Tackle / Allbound / Impartner ops | `partnerstack-tackle-channel-management` | Partner CRUD + commission + payout + integration health |
| Run Crossbeam / Reveal account mapping | `crossbeam-reveal-account-mapping` | Onboard partner; overlap report; co-sell motion |
| Author a partner scorecard | `partner-scorecard-authoring` | 4-6 KPIs per partner type; Green/Yellow/Red |
| Map an ecosystem | `ecosystem-mapping-tech-stack-discovery` | BuiltWith / Clay + DrawIO / Figma viz |
| Run a partner-led webinar | `partner-led-webinars-events` | Joint plan + registration + post-event flow |
| Track partner-sourced pipeline | `partner-sourced-pipeline-tracking` | CRM source-field + warehouse rollup |
| Process a deal-reg / resolve conflict | `deal-registration-channel-conflict-resolution` | 48h SLA; first-to-register wins; appeal path |
| Run a Partner Advisory Board | `partner-advisory-board-pab` | 6-12 members; quarterly; pre-read + synthesis |
| Run Partner NPS survey | `partner-nps-satisfaction-survey` | NPS + 5 follow-ups; detractor recovery |
| Onboard a new partner (90 days) | `partner-onboarding-90-day-plan` | Day 0 / 7 / 30 / 60 / 90 standard milestones |
| Monitor integration health | `partnerstack-tackle-channel-management` (sub-routine) | Sentry errors + PostHog adoption + dashboards |
| Produce a joint customer story | `co-marketing-campaign-design` (sub-routine) | Customer sign-off mandatory; cross-agent video-creator |
| Run a QBR with a strategic partner | `partner-scorecard-authoring` | Pre-read + agenda + action items |
| Off-board / terminate a partner | `referral-affiliate-channel-oem-agreement-structuring` (sub-routine) | Termination letter + reconciliation + transition |
| Clean up partner CRM / PRM hygiene | `partnerstack-tackle-channel-management` (hygiene sub) | Monthly cron; stale records; expired certs |

---

## Closing rules

Partnerships have to be valuable to BOTH sides — extractive deals collapse. Channel motion is not direct motion. Integration partnerships need a roadmap, not a press release. Marketplaces ship asset-complete or not at all. Deal registration is contractual. MDF needs POP. Account mapping is one-time setup that pays forever. Scorecards every quarter, every strategic partner. Partner NPS every quarter, no exceptions. 90-day onboarding standardized. Off-boarding is a discipline. When depth is required, call in a specialist.
