<!--
Source: https://partners.salesforce.com/partnerProgram + https://developer.salesforce.com/docs/atlas.en-us.code_analyzer.meta/code_analyzer/
Salesforce AppExchange listing via Code Analyzer + Partner Console + ISVForce (June 2026 SOTA).
-->
# Salesforce AppExchange Listing — SKILL

Publish (and maintain) Salesforce AppExchange listings end-to-end. AppExchange has the **Security Review** gate (6-12 weeks, Salesforce-side) plus a listing-asset bundle plus marketing plan plus ISVForce distribution. Pre-Security-Review uses **Salesforce Code Analyzer** (`sfdx scanner:run`); listing CRUD is via **Partner Console** (no public API — `playwright-mcp` for portal automation).

## When to use

- **Launching a Salesforce-native app** (managed package) on AppExchange.
- **Pre-Security-Review hardening** — run Code Analyzer; resolve critical + high findings.
- **Updating listing assets** — new screenshots, demo video, pricing tier changes.
- **Publishing a managed-package upgrade** — patch version vs minor version vs major version.
- **ISVForce distribution flow** — partner-to-customer org install.
- **Trigger phrases**: "AppExchange listing", "Security Review", "sfdx scanner", "managed package", "ISVforce", "publisher org".

Do NOT use this skill for: **non-Salesforce SaaS marketplaces** (use `hubspot-shopify-slack-marketplace-listings` or `aws-azure-gcp-marketplace-listings`); **app architecture / Apex code review** (defer to `tech-lead-cto`); **commercial Salesforce reseller motion** (use `channel-pricing-discount-tiers` + `referral-affiliate-channel-oem-agreement-structuring`).

## Setup

```bash
# Salesforce CLI (sf, replaces older sfdx)
npm install -g @salesforce/cli              # or brew install sfdx-cli
sf --version                                # require 2.20+

# Code Analyzer plugin
sf plugins install @salesforce/sfdx-scanner

# Authenticate to Partner Business Org (where you manage AppExchange)
sf org login web --alias partner-business --instance-url https://login.salesforce.com

# Authenticate to Packaging Org (where managed packages live)
sf org login web --alias packaging --instance-url https://login.salesforce.com

# Optional: API for app analytics (post-publish)
export SF_PARTNER_ANALYTICS_API_KEY="<key>"
```

**One-time human tasks:**
- Enroll in AppExchange Partner Program — https://partners.salesforce.com.
- Sign Partner Master Agreement.
- Get Partner Business Org + Packaging Org provisioned.
- Pay annual Partner Program fee.

## Common recipes

### Recipe 1: Code Analyzer — pre-Security-Review static scan

```bash
# Run all 5 engines: pmd, eslint, retire-js, cpd, sfge (Salesforce Graph Engine)
sf scanner:run --target . --format json --outfile /tmp/sf-scanner.json

# Run path-based (DFA — most powerful, slowest)
sf scanner:run:dfa --target ./force-app --projectdir ./force-app --format json \
  --outfile /tmp/sf-scanner-dfa.json

# Summarize critical + high findings
jq '[.[] | select(.severity <= 2)] | length' /tmp/sf-scanner.json
jq '.[] | select(.severity <= 2) | {file, line, rule, message}' /tmp/sf-scanner.json
```

Severity scale: 1 = Critical, 2 = High, 3 = Moderate, 4 = Low, 5 = Info. **Resolve all 1 + 2 before submitting Security Review.**

Reference: https://developer.salesforce.com/docs/atlas.en-us.code_analyzer.meta/code_analyzer/.

### Recipe 2: Bundle assessment — quick gate

```python
import json, sys
data = json.load(open("/tmp/sf-scanner.json"))
crit_high = [f for f in data if f.get("severity",5) <= 2]

if crit_high:
    print(f"BLOCKED: {len(crit_high)} critical/high findings:")
    for f in crit_high[:20]:
        print(f"  {f['fileName']}:{f.get('lineNumber','?')} — {f['ruleName']}")
    sys.exit(1)
print("CLEAN: no critical/high findings. Ready for Security Review submission.")
```

Wire into CI so every package version gates on Code Analyzer.

### Recipe 3: Create managed package (Second-Generation Packaging — 2GP)

```bash
# Create package definition (one-time)
sf package create --name "Brand Analytics" --package-type Managed \
  --path force-app --target-dev-hub partner-business

# Create new version
sf package version create --package "Brand Analytics" \
  --installation-key-bypass --wait 30 --target-dev-hub partner-business \
  --version-number "1.2.0.NEXT"

# List versions
sf package version list --target-dev-hub partner-business --package "Brand Analytics"
```

2GP managed packages are the modern path. 1GP managed packages are legacy and limited (one-package-per-namespace).

### Recipe 4: Install package to a scratch / test org

```bash
sf package install --package "04t..." --wait 30 \
  --installation-key "<install-key-if-set>" \
  --target-org test-org
```

Before Security Review, install in clean scratch org + Trailhead Playground; run regression tests.

### Recipe 5: AppExchange listing asset bundle (canonical)

```yaml
listing_assets:
  app_logo:        "256x256px PNG, transparent background"
  cover_image:     "1432x676px PNG (visible on tile)"
  featured_image:  "2880x720px PNG (listing top banner)"
  screenshots:
    - "1432x988px — Dashboard view"
    - "1432x988px — Setup wizard"
    - "1432x988px — Reports panel"
    - "1432x988px — Lightning component example"
    - "1432x988px — Mobile view"
  demo_video:      "YouTube unlisted URL OR uploaded MP4, 60-180s, 1080p"
  short_description: "≤ 250 chars"
  full_description:  "Markdown, 500-2000 words; what + who + key features + pricing"
  key_features:    "5 bullets, ≤ 150 chars each"
  pricing_tiers:
    - {name:"Free",price:"$0",dimensions:"1 user, basic features"}
    - {name:"Standard",price:"$50/user/mo",dimensions:"unlimited users"}
    - {name:"Premier",price:"Contact us",dimensions:"enterprise features + SLA"}
  edition_support:
    - "Enterprise Edition: Yes"
    - "Professional Edition: Limited"
    - "Lightning Experience: Yes"
    - "Salesforce Classic: No"
  ux_compatible:   "Lightning, Mobile, Experience Cloud"
  customer_references: "3 production-deployed customers; ≥ 1 case study URL"
  trial_org_url:   "Set up Trial Org template; provides 1-click trial install"
  support_contact: "support@brand.com, +1-800-..., docs.brand.com"
  legal_docs:      "EULA URL, Privacy URL, Terms URL"
```

Render screenshots via `imagegen-mcp` / Figma component capture; hero via `canva-mcp` or `figma-mcp`.

### Recipe 6: Marketing Plan submission (required for AppExchange listing)

```yaml
marketing_plan:
  launch_announcement: "Brand × Salesforce launch blog post + LinkedIn"
  trailblazer_community: "1 post in Trailblazer Community/Group + AppExchange Connect"
  webinar: "Joint webinar within 60 days of listing-live (use partner-led-webinars-events skill)"
  dreamforce_demo: "Booked Dreamforce 2026 demo theater + sponsorship tier"
  customer_co_marketing: "≥1 customer-story video within 90 days"
  paid_acquisition: "$10k LinkedIn ABM targeting Salesforce admins + RevOps"
  organic_seo: "Landing page brand.com/salesforce + content cluster (5 posts)"
  trailblazer_dx_badge: "Submit for community Trailblazer DX badge after listing-live"
```

Marketing plan is reviewed in addition to Security Review. AppExchange wants to see commitment.

### Recipe 7: Security Review submission (Partner Console portal flow)

```python
# No public API for Security Review submission — use playwright-mcp
# Steps in Partner Console (https://partners.salesforce.com/login.jsp):
# 1. Navigate Manage Listings → Edit Listing → Security Review tab
# 2. Upload package version ID (04t...) + Test Org credentials + Listing details
# 3. Complete Security Review questionnaire (privacy, data residency, OAuth scope, encryption)
# 4. Submit
# 5. Receive case # → track via Partner Community case page

# Playwright-mcp recipe:
# Open https://partners.salesforce.com/login.jsp
# Login → Manage Listings → click edit → Security Review tab → upload artifacts → submit
```

Security Review timeline: 6-12 weeks median; can be 16+ weeks for complex packages.

Reference: https://developer.salesforce.com/docs/atlas.en-us.packagingGuide.meta/packagingGuide/security_review.htm.

### Recipe 8: Listing CRUD via Partner Console (Playwright)

```python
# Partner Console URLs:
# - Edit listing: https://partners.salesforce.com/sf/PartnerListingEdit?listingId=<id>
# - Listing analytics: https://partners.salesforce.com/sf/PartnerListingAnalytics?listingId=<id>
# - License management: https://partners.salesforce.com/sf/PartnerLicenseManagement

# Automate with playwright-mcp:
# 1. open_page partner console
# 2. fill listing description, upload assets via file inputs
# 3. preview → save → submit for review (small changes auto-publish; major changes re-review)
```

Track per-listing state via `notion-mcp` DB with status `(draft|security-review|approved|published)` + last-edit-date.

### Recipe 9: License management (ISVForce)

```bash
# Manage subscriber org licenses
sf apex run --target-org partner-business --file query-licenses.apex
```

```apex
// query-licenses.apex
List<sfLma__License__c> lics = [
  SELECT Id, sfLma__Subscriber_Org_ID__c, sfLma__Status__c, sfLma__Seats__c, sfLma__Expiration__c
  FROM sfLma__License__c
  WHERE sfLma__Status__c = 'Active'
];
System.debug(JSON.serialize(lics));
```

License records live in your Partner Business Org's LMA (License Management App). Adjust seats / expiration here when commercial terms change.

### Recipe 10: Post-publish analytics (Partner Console + manual export)

```python
# Partner Console → Analytics tab has:
# - Listing views, install starts, install completes
# - Trial org provisioning rate
# - 30/60/90-day retention of installed orgs
# - Top-referrer dashboards

# Export weekly via Playwright:
# 1. Navigate to Analytics
# 2. Set date range (last 30 days)
# 3. Export CSV
# 4. Load into postgresql-mcp warehouse view

# Then surface in QBR via partner-scorecard-authoring
```

### Recipe 11: Multi-version upgrade rollout (patch / minor / major)

```yaml
upgrade_decision_matrix:
  patch (1.2.3 → 1.2.4):
    - "Bug fixes only; no schema changes"
    - "Push automatically to subscriber orgs"
    - "No Security Review delta required"
  minor (1.2 → 1.3):
    - "Backward-compatible new features"
    - "Subscribers see in 'Available Updates' tab; not auto-pushed"
    - "Security Review delta required (lighter review, ~3-4 weeks)"
  major (1.x → 2.0):
    - "Breaking changes possible; new namespace optional"
    - "Subscribers opt-in install; can't auto-upgrade"
    - "Full Security Review required (6-12 weeks)"
```

### Recipe 12: Listing checklist (Notion DB row)

```yaml
listing:
  name: "Brand Analytics"
  package_id: "04t1A000000XXXX"
  status: "published"
  last_security_review_date: "2026-03-15"
  next_security_review_due: "2027-03-15"
  code_analyzer_last_clean: "2026-05-20"
  asset_bundle_complete: true
  asset_last_updated: "2026-05-22"
  customer_references: 5
  install_count_30d: 145
  trial_install_to_paid_pct_30d: 12
  monthly_active_orgs: 280
  feedback_summary: "Lightning-only customers asking for Classic compat"
  next_action: "Q3 minor release planned for July; add Mobile-View enhancements"
  owner: "<partnerships-lead>"
```

## Examples

### Example 1: First-time AppExchange listing for a 2GP managed package

**Goal:** Salesforce-native app ready for AppExchange; first listing.

**Steps:**
1. Day 0 — Enroll in Partner Program (one-time); Partner Business Org provisioned (~5 days).
2. Day 5 — Recipe 3 creates managed package + version.
3. Day 6 — Recipe 1 + 2 — Run Code Analyzer; resolve all critical + high (~1-2 weeks dev work).
4. Day 20 — Recipe 5 — Asset bundle assembled.
5. Day 21 — Recipe 6 — Marketing plan drafted.
6. Day 22 — Recipe 7 — Submit Security Review.
7. Day 22 - Day 80 — Salesforce reviews (typical 6-12 weeks). Respond to RFIs within 48h.
8. Day 85 — Listing approved; published; install URL live.
9. Day 85+ — Recipe 10 — Weekly analytics tracking.

**Result:** First AppExchange listing live ~3 months from start.

### Example 2: Listing-asset refresh (no Security Review)

**Goal:** New customer story + better demo video; listing already approved.

**Steps:**
1. Recipe 5 — Update only assets that need refresh (screenshots, video URL).
2. Recipe 8 — Playwright update via Partner Console.
3. Minor description / asset changes auto-publish in 24h; no Security Review delta.
4. Update Notion checklist (Recipe 12) with new `asset_last_updated`.

**Result:** Listing freshness without re-review cycle.

### Example 3: Major version 2.0 with breaking changes

**Goal:** New architecture in 2.0; current 1.x subscribers can't auto-upgrade.

**Steps:**
1. Recipe 3 — New package version (2.0.0); could use new namespace.
2. Recipe 1 + 2 — Code Analyzer; resolve findings.
3. Recipe 7 — Full Security Review submission.
4. Communication plan: existing 1.x subscribers get migration guide + grace period.
5. After approval, 2.0 published as separate listing OR 1.x users invited to manual upgrade.

**Result:** Clean major-version path without disrupting existing subscriber base.

## Edge cases / gotchas

- **No public API for AppExchange listing CRUD** — Partner Console + Playwright is the path. Selectors break occasionally; verify with smoke test before bulk operations.
- **Security Review is the bottleneck** — 6-12 weeks median, sometimes 16+. Plan launches with margin. Resolve all Code Analyzer critical/high findings BEFORE submission; failed reviews cost 4+ weeks more.
- **Code Analyzer engines have different findings** — PMD is Apex linting; sfge (Salesforce Graph Engine) is DFA (data flow analysis), catches real security vulns; retire-js for JS. Run all engines.
- **DFA scans are slow** — for large codebases, 30 min to several hours. Run nightly in CI; not on every commit.
- **2GP vs 1GP** — 2GP supports multiple packages per namespace, branchable versions, modern dev. 1GP is legacy. Always 2GP for new packages.
- **Managed-Released vs Beta** versions — only Managed-Released versions can go through Security Review or be published.
- **Apex test coverage requirement** — 75% test coverage org-wide + 100% trigger coverage. Run `sf apex run test` pre-submission.
- **Trial Org setup is fiddly** — Custom Object setup, sample data, Trial Org template. Worth the effort for trial conversion rate.
- **Listing fields are auto-translatable** to other locales — pre-translate via `deepl-mcp` if listing-eligible markets include non-English.
- **Customer references must be reachable** — Salesforce may call to verify. Pre-coach customers; explicitly ask permission.
- **Marketing Plan rejection** is rare but happens — most common reason: too thin (just "we'll do a blog post"). Include 5+ activities + measurable goals.
- **Dreamforce window** — listings approved Aug-Sep get priority Dreamforce slotting. Submit by July 1 if Dreamforce demo matters.
- **AppExchange pricing edits trigger re-review** — partial. Tier rename = quick; new tier or pricing model change = full review. Plan pricing carefully at launch.
- **Lightning vs Classic compat** is a buyer filter. Lightning-only listings filter out a large customer pool. Decide based on segment.
- **Edition restrictions** — Enterprise + Performance edition packages are most flexible; Professional is limited (no custom Apex). Pricing tiers should match edition.
- **License-management Apex** lives in your Partner Business Org — not in subscriber orgs. Mistakenly editing in subscriber org just confuses; always edit in partner business org.
- **Post-launch refunds + churn** — if a customer cancels, you may need to revoke license via LMA. Don't forget this in 2026 SaaS contracts.

## Sources

- AppExchange Partner Program: https://partners.salesforce.com/partnerProgram
- Salesforce Code Analyzer: https://developer.salesforce.com/docs/atlas.en-us.code_analyzer.meta/code_analyzer/
- Code Analyzer CLI: https://forcedotcom.github.io/sfdx-scanner/en/scanner-commands/run/
- Security Review: https://developer.salesforce.com/docs/atlas.en-us.packagingGuide.meta/packagingGuide/security_review.htm
- 2GP Packaging guide: https://developer.salesforce.com/docs/atlas.en-us.pkg2_dev.meta/pkg2_dev/
- ISVForce guide: https://resources.docs.salesforce.com/sfdc/pdf/salesforce_isvforce_guide.pdf
- AppExchange listing best practices: https://partners.salesforce.com/s/article/Listing-Best-Practices
- Trailhead Partner trail: https://trailhead.salesforce.com/users/partners
