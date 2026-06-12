---
name: cookie-consent-management-cookiebot-onetrust
description: Set up cookie consent banners + Consent Management Platform (CMP) via Cookiebot, OneTrust, Iubenda Cookie Solution, Osano, or TrustArc. IAB TCF v2.2 + Google Consent Mode v2 + GPC signal compliance. Use when implementing GDPR / ePrivacy / CCPA cookie consent. Output is the embed snippet + cookie policy + memo with the consult-an-attorney disclaimer.
---

# Cookie Consent Management — Cookiebot / OneTrust / Iubenda / Osano / TrustArc

## When to use

User says:

- "Set up a cookie banner"
- "Implement cookie consent for GDPR / CCPA"
- "Configure Cookiebot / OneTrust / Iubenda Cookie Solution"
- "Google Consent Mode v2 integration"
- "IAB TCF v2.2 compliance"
- "Why is my banner blocking ads?"
- "Add a cookie policy"

Companion skills:
- `privacy-policy-gdpr-ccpa` — privacy policy references cookies.
- `iubenda-termly-privacy-policy-generators` — Iubenda Cookie Solution overlaps.

## Setup

### Cookiebot (by Usercentrics)
```bash
# Sign up: https://www.cookiebot.com/
# Tiers (June 2026):
#   Free — single domain, <100 pages
#   Premium — €9-49/mo by domain size
#   Enterprise — multi-domain, custom

# Embed snippet:
# <script id="Cookiebot" src="https://consent.cookiebot.com/uc.js"
#         data-cbid="<DOMAIN_GROUP_ID>" type="text/javascript" async></script>
```

### OneTrust
```bash
# Enterprise consent + privacy management
# https://www.onetrust.com/products/cookie-consent/
# Enterprise quote; not for solo founders typically

# Embed: dashboard generates script
# <script src="https://cdn.cookielaw.org/scripttemplates/otSDKStub.js"
#         data-domain-script="<UUID>"></script>
```

### Iubenda Cookie Solution
```bash
# https://www.iubenda.com/en/cookie-solution
# Tiers — included in Iubenda Pro+ (€27+/mo)

# Embed: dashboard generates snippet (loads before other scripts)
```

### Osano
```bash
# https://www.osano.com/
# Free tier available

# Embed:
# <script src="https://cmp.osano.com/<CMP_ID>/osano.js"></script>
```

### TrustArc
```bash
# https://trustarc.com/
# Enterprise tier; ad-tech focused (IAB TCF leader)
```

Auth / API keys:
- `COOKIEBOT_DOMAIN_GROUP_ID` — from Cookiebot dashboard.
- `ONETRUST_DATA_DOMAIN_SCRIPT` — from OneTrust dashboard.
- `IUBENDA_COOKIE_POLICY_ID` — from Iubenda dashboard.

## Common recipes

### Recipe 1: Cookiebot — scan + categorize + embed
```text
1. Sign up at https://manage.cookiebot.com
2. Add domain → run cookie scanner (crawls 100-500 pages).
3. Review detected cookies; recategorize if needed:
   - Necessary (no consent required)
   - Preferences
   - Statistics
   - Marketing
4. Configure banner: position, layout, color, language.
5. "Get script" → copy the <script> tag.
6. Paste in <head> of every page BEFORE any non-essential script.
```
The Cookiebot script auto-blocks non-necessary scripts until consent granted (script tag rewriting).

### Recipe 2: Auto-blocking implementation
```html
<!-- Cookiebot must load FIRST in <head> -->
<script id="Cookiebot" src="https://consent.cookiebot.com/uc.js"
        data-cbid="00000000-0000-0000-0000-000000000000"
        data-blockingmode="auto" type="text/javascript"></script>

<!-- Other scripts: change type attribute -->
<!-- BAD: <script src="https://analytics.example.com/script.js"></script> -->
<!-- GOOD: -->
<script type="text/plain" data-cookieconsent="statistics"
        src="https://analytics.example.com/script.js"></script>
```
Cookiebot rewrites `type="text/plain"` to active scripts only AFTER user consents to the listed category.

### Recipe 3: Google Consent Mode v2 integration
```html
<!-- Initialize Consent Mode BEFORE GTM -->
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('consent', 'default', {
  'ad_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied',
  'analytics_storage': 'denied',
  'functionality_storage': 'granted',
  'personalization_storage': 'denied',
  'security_storage': 'granted',
  'wait_for_update': 500
});
</script>

<!-- Cookiebot will update consent state after user choice -->
<script id="Cookiebot" src="https://consent.cookiebot.com/uc.js"
        data-cbid="..." data-blockingmode="auto"></script>

<!-- GTM after Consent Mode -->
<script>
(function(w,d,s,l,i){...})(window,document,'script','dataLayer','GTM-XXXXX');
</script>
```
Google Consent Mode v2 required for EEA traffic to measure Google Ads conversions (since March 2024).

### Recipe 4: IAB TCF v2.2 compliance (ad-tech sites)
```text
1. Cookiebot / OneTrust / TrustArc dashboard → enable "IAB TCF v2.2"
2. Select Vendor List (IAB Global Vendor List — 1000+ vendors)
3. Map Purposes (1-11 in TCF v2.2):
   - Store info
   - Select basic ads
   - Personalised ads profile + selection
   - Personalised content profile + selection
   - Measure ad / content performance
   - Audience research
   - Develop + improve products
   - Use limited data to select content
   - etc.
4. Generate banner with full TCF UI (Purposes + Vendors + Special Features).
5. Test via IAB CMP Validator: https://cmpvalidator.iabtechlab.com/
```

### Recipe 5: Global Privacy Control (GPC) signal handling
```javascript
// Detect GPC signal (CCPA opt-out equivalent)
if (navigator.globalPrivacyControl) {
  // Treat as opt-out of sale/share
  gtag('consent', 'update', {
    'ad_storage': 'denied',
    'ad_user_data': 'denied'
  });
  // Send signal to CMP
  Cookiebot.renew(); // or equivalent
}
```
Required: CCPA / CPRA + CO + CT + several state privacy laws require GPC honor. Cookiebot, OneTrust, Iubenda CMPs handle this automatically; verify in your dashboard.

### Recipe 6: Cookie Policy page (auto-generated)
```text
Cookiebot / OneTrust / Iubenda dashboards → "Cookie Policy" tab → generates HTML / iframe
Embed at <yoursite>/cookies — link from privacy policy + footer + banner "Learn more."

Cookie Policy contents:
- What are cookies
- Categories (Necessary / Preferences / Statistics / Marketing)
- Detailed cookie list (auto-populated from scanner)
- How to manage / withdraw consent
- Third-party cookies notice
- Contact info
```

### Recipe 7: Geo-targeting (banner only for EU + CA, etc.)
```text
Cookiebot dashboard → "Behavior" → "Geo-IP targeting"
- EU only: banner shows for EU IPs
- US (CA / CO / VA / CT / etc.): different banner with "Do Not Sell or Share" link
- Rest of world: no banner OR informational only
```
Don't show a full consent banner for visitors NOT subject to ePrivacy / GDPR — adds friction without legal benefit. But for CCPA-applicable states (CA + others), the opt-out banner is required.

### Recipe 8: Cookiebot REST API — list cookies / sites programmatically
```bash
curl -X GET https://api.cookiebot.com/v2/cookies \
  -H "X-API-Key: $COOKIEBOT_API_KEY" \
  -H "Accept: application/json"
```

### Recipe 9: Banner copy + UX defaults (avoid dark patterns)
```text
Banner buttons (best practice):
- "Accept All" + "Reject All" + "Cookie Settings" — three equal-weight buttons
- NOT "Accept All" + "Cookie Settings" with no reject
- NOT bury "Reject" in a sub-menu

CNIL (France DPA) enforcement focus: equal prominence for Accept vs Reject.
ICO (UK DPA): "Reject all" must be as easy as "Accept all."
```

### Recipe 10: Consent record retention + audit log
```text
GDPR Art. 7(1): controller must demonstrate consent.
Cookiebot / OneTrust / Iubenda dashboards record:
- Timestamp
- IP (hashed) or session ID
- Consent string (TCF format)
- Categories accepted
- Banner version

Export for audit: dashboard → Consent Records → CSV / API.
```

## Examples

### Example 1: B2B SaaS — Cookiebot setup
**Goal:** GDPR + CCPA-compliant cookie consent.
**Steps:**
1. Sign up for Cookiebot (Recipe 1).
2. Scan site; categorize cookies.
3. Install snippet with auto-blocking (Recipe 2).
4. Integrate Google Consent Mode v2 (Recipe 3) — required for Google Ads in EEA.
5. Honor GPC signal (Recipe 5).
6. Generate cookie policy (Recipe 6).
7. Verify banner UX is balanced (Recipe 9).
8. Test in EU + CA + US (non-applicable) browser geo-locations.
9. Confirm consent log accessible (Recipe 10).

**Result:** Fully compliant cookie consent stack across major regulations.

### Example 2: Ad-tech site — OneTrust + IAB TCF v2.2
**Goal:** Programmatic ad delivery while respecting TCF.
**Steps:**
1. Sign up for OneTrust + select IAB TCF v2.2 mode.
2. Configure Purposes + Vendor List.
3. Test consent string generation.
4. Validate at https://cmpvalidator.iabtechlab.com/
5. Add disclaimer + verify IAB framework version (2.2 as of 2024-2026).

**Result:** Compliant ad-tech consent infrastructure.

### Example 3: Switching from Cookiebot to Iubenda (or vice versa)
**Goal:** Migrate CMP without losing consent records.
**Steps:**
1. Export consent log from old CMP (Recipe 10).
2. Configure new CMP (e.g., Iubenda Cookie Solution — Recipe 1 of `iubenda-termly-privacy-policy-generators`).
3. Replace embed snippet.
4. Force re-consent (recommended for material UX change).
5. Update privacy policy to reference new CMP.
6. Test auto-blocking still works.

**Result:** Migration complete with continuous compliance.

## Edge cases / gotchas

- **Banner loads after analytics scripts.** If your Cookiebot/OneTrust snippet is not first in `<head>`, non-essential scripts may fire BEFORE consent. Auto-blocking only works if CMP loads first.
- **GTM-loaded scripts bypass CMP.** Scripts loaded via Google Tag Manager need Consent Mode v2 integration; otherwise they fire regardless of cookie banner. Always pair with Recipe 3.
- **Server-side cookies aren't blocked by client CMP.** Server-set cookies (Set-Cookie header from your backend) bypass client-side blocking. Audit server-side cookie issuance separately.
- **Localhost / dev environments.** CMP banners often disabled on localhost; verify in staging matching production.
- **CNIL + Italy DPA enforcement on banner UX.** "Reject All" must be one click; dark patterns (pre-checked boxes, "Accept All" highlighted) → fines. €60M+ Google fine in France 2021.
- **California auto-renewal text on banner.** Some CA AG enforcement actions flag CMP banners that don't display "Do Not Sell or Share" prominently for CA IPs. Geo-target the banner copy.
- **IAB TCF v2.2 is mandatory for IAB participants** — v2.1 deprecated September 2023; v2.2 enforces stricter Vendor accountability + LI removal for personalised ads.
- **Cookie policy ≠ privacy policy.** Most regulators require both; cookie policy enumerates cookies, privacy policy explains data use.
- **GPC signal coverage expanding.** CCPA + CO + CT + several others recognize GPC; FTC has signaled GPC honor may be required. CMP must respect.
- **Free tier limits.** Cookiebot free is limited to single domain + 100 pages; Iubenda free is bare-bones. Premium often required for production.
- **EU-US Data Privacy Framework + cookie consent overlap.** DPF resolves transfer issue but doesn't override ePrivacy consent requirement. Banner still required for EU.
- **Children + COPPA cookie restrictions.** Sites directed to under-13 face stricter cookie rules (16 CFR §312). Don't drop marketing cookies for under-13 even with parent consent.

> Warning: **This is informational guidance from an AI agent. Always consult a licensed attorney in your jurisdiction before relying on cookie consent configuration for regulatory compliance.**

## Sources

- [Cookiebot](https://www.cookiebot.com/) — leading cookie scanner + CMP (acquired by Usercentrics 2022).
- [OneTrust Cookie Consent](https://www.onetrust.com/products/cookie-consent/) — enterprise CMP.
- [Iubenda Cookie Solution](https://www.iubenda.com/en/cookie-solution) — generator-bundled CMP.
- [Osano](https://www.osano.com/) — CMP with free tier.
- [TrustArc](https://trustarc.com/) — ad-tech focused CMP.
- [IAB TCF v2.2](https://iabeurope.eu/transparency-consent-framework/) — Transparency & Consent Framework spec.
- [IAB CMP Validator](https://cmpvalidator.iabtechlab.com/) — TCF compliance test.
- [Google Consent Mode v2](https://developers.google.com/tag-platform/security/guides/consent) — required for EEA Google Ads measurement.
- [Global Privacy Control (GPC)](https://globalprivacycontrol.org/) — opt-out signal spec.
- [CNIL Cookie Guidelines](https://www.cnil.fr/en/cookies-and-other-trackers) — France DPA enforcement.
- [ICO Cookies Guidance](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/cookies-and-similar-technologies/) — UK ICO.
- Sister skills: `privacy-policy-gdpr-ccpa`, `iubenda-termly-privacy-policy-generators`.
