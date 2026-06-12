---
name: iubenda-termly-privacy-policy-generators
description: Generate privacy policies, cookie policies, ToS, and DPAs via Iubenda and Termly. Both auto-update on regulation change. Use when speed matters and the policy is "off-the-shelf" — for highly customized policies, use `privacy-policy-gdpr-ccpa` (manual draft) instead. Output requires sub-processor + custom-data-flow customization + the consult-an-attorney disclaimer before publication.
---

# Iubenda + Termly Privacy / Cookie / ToS Generators

## When to use

User says:

- "Generate a privacy policy fast"
- "I have Iubenda / Termly — how do I configure it?"
- "What's the difference between Iubenda and Termly?"
- "Embed the privacy policy in my site"
- "Auto-update privacy policy when regulations change"

Companion skills:
- `privacy-policy-gdpr-ccpa` — manual / handcrafted alternative.
- `cookie-consent-management-cookiebot-onetrust` — cookie banner specifically.
- `gdpr-readiness-audit` + `ccpa-cpra-readiness-audit` — underlying compliance.

## Setup

### Iubenda
```bash
# Sign up: https://www.iubenda.com/
# Tiers (June 2026 approx):
#   Free — basic privacy policy only
#   Pro — €27/mo — full policy + cookie + ToS
#   Ultra — €59/mo — DPA + DSAR + multi-domain
#   Iubenda for Business / Enterprise — quote

# Embed via JavaScript snippet OR HTML link
# Get embed: Iubenda dashboard → Privacy Policy → Embed code
```

### Termly
```bash
# Sign up: https://termly.io/
# Tiers (June 2026 approx):
#   Free — basic policy + cookie consent (limited)
#   Pro — $10/mo — full policy + ToS + EULA
#   Pro Plus — $30/mo — DSAR + GDPR + CCPA + multi-policy
#   Enterprise — quote

# Embed via JavaScript snippet OR direct hosted URL
```

### Both — API access
```bash
# Iubenda REST API — Pro tier and up
# https://www.iubenda.com/api/
export IUBENDA_PRIVATE_KEY=<from dashboard>
export IUBENDA_PUBLIC_KEY=<from dashboard>

# Termly REST API — Pro Plus and up (more limited)
export TERMLY_API_KEY=<from dashboard>

pip install requests
```

## Common recipes

### Recipe 1: Iubenda — generate a privacy policy (web app)
```text
1. Sign in to https://www.iubenda.com/en/dashboard
2. "Create new Policy" → enter site URL + name.
3. Click "Privacy Policy" tab.
4. Add Services from Iubenda catalog (1700+ pre-mapped — Stripe, Google Analytics, etc.).
5. For each service, Iubenda fills in: purpose, lawful basis, retention, sub-processor.
6. Add any custom processing activities (Iubenda's "Custom Service" template).
7. Select jurisdictions (US states, EU, UK, etc.) — Iubenda layers requirements.
8. Click "Embed" → choose Direct Link / Button / Inline HTML / Multi-domain.
9. Add the embed snippet to your site footer.
```
The generator's catalog covers most B2B SaaS sub-processors out of the box. For NEW sub-processors not in the catalog, use "Custom Service."

### Recipe 2: Termly — generate a privacy policy (web app)
```text
1. Sign in to https://app.termly.io
2. "Generate a Policy" → "Privacy Policy" → Wizard:
   - Business info
   - Data collected (categories)
   - Third parties (analytics, ads, payments)
   - Cookies (auto-scan optional)
   - Compliance regions (US CA / VA / CO etc. / EU / UK / Canada / others)
3. Termly produces a draft.
4. Edit any auto-generated section.
5. Embed: dashboard → Embed → JavaScript snippet OR Direct Link.
```
Termly's strength: faster wizard. Weakness: smaller catalog than Iubenda; more custom-service entries required.

### Recipe 3: Iubenda — auto-scan cookies + cookie policy
```text
1. Dashboard → "Cookie Solution" → Add website.
2. Click "Scan" — Iubenda crawls site, identifies cookies + their providers.
3. Map detected cookies to categories (Necessary / Preferences / Statistics / Marketing).
4. Generate Cookie Policy + banner snippet.
5. Embed banner snippet in <head> (must load before other scripts to gate non-essential cookies).
```

### Recipe 4: Termly — auto-scan cookies + cookie consent banner
```text
1. Dashboard → "Consent Management" → New website.
2. Scan site (or upload list manually).
3. Map categories.
4. Generate banner; embed snippet.
5. Configure: position, color, language, geo-targeting (e.g., banner only for EU IPs).
```

### Recipe 5: Iubenda API — programmatic policy generation
```python
import os, requests

API = "https://www.iubenda.com/api/privacy-policy"
key = os.environ["IUBENDA_PRIVATE_KEY"]

# Create / update a privacy policy programmatically
resp = requests.post(
    f"{API}",
    headers={"ApiKey": key, "Content-Type": "application/json"},
    json={
        "name": "My App Privacy Policy",
        "url": "https://myapp.com",
        "services": ["stripe-payments", "google-analytics", "sendgrid"],
        "jurisdictions": ["EU", "US", "CA", "VA", "CO"]
    }
)
policy_id = resp.json()["id"]

# Get hosted URL
hosted = requests.get(
    f"{API}/{policy_id}/embed",
    headers={"ApiKey": key}
).json()
print("Embed URL:", hosted["url"])
```

### Recipe 6: DPA generation (Iubenda Pro Plus / Ultra)
```text
1. Iubenda dashboard → "DPA Module" → New DPA.
2. Enter controller info + processor info.
3. Iubenda inserts GDPR Art. 28(3) mandatory terms.
4. Customize: sub-processor list, technical/organizational measures, audit rights.
5. Export to PDF / DOCX.
6. Sign + share with counterparty.
```

### Recipe 7: DSAR (Data Subject Access Request) intake (Iubenda DSAR)
```text
1. Iubenda dashboard → "DSAR / Privacy Requests" → Enable.
2. Iubenda hosts a request portal at <yoursite>/privacy-portal.
3. Users submit access / delete / correct requests.
4. Iubenda routes to designated email + tracks SLA (1 month GDPR / 45 days CCPA).
5. Manual response: download data export, write deletion confirmation, etc.
```

### Recipe 8: Termly — DSAR request handling (Pro Plus)
```text
1. Termly dashboard → "Consent Management" → "Subject Rights Requests".
2. Hosted intake form at a Termly-provided URL.
3. Email forwarding + status tracking.
4. Verification flow per CCPA §1798.130.
```

### Recipe 9: Iubenda vs Termly comparison
| Feature | Iubenda | Termly |
|---|---|---|
| Service catalog | 1700+ pre-mapped | ~500 pre-mapped |
| Pricing | €27-59+/mo | $10-30+/mo |
| Cookie scanner | Yes | Yes |
| CMP IAB TCF v2.2 | Yes (Pro+) | Yes (Pro+) |
| DPA generator | Yes (Ultra) | Yes (Pro Plus) |
| DSAR portal | Yes (Ultra) | Yes (Pro Plus) |
| Multi-language | 13 | 8 |
| Multi-jurisdiction layering | Strong | Moderate |
| API for automation | Yes | Limited |
| Best for | Multi-jurisdiction SaaS | US-first SMB |

### Recipe 10: Customize generator output before publication
```bash
# Always add these to generator output:
# 1. Specific sub-processor list (Iubenda may miss custom integrations)
# 2. Retention periods (generators use generic "as needed" — be specific)
# 3. Lawful basis mapping (verify generator's defaults match your operations)
# 4. International transfer mechanism (SCC version + TIA reference)
# 5. Disclaimer

cat >> generated_policy.md <<'EOF'

---
**Disclaimer:** This is informational guidance from an AI agent and an automated generator. Always consult a licensed attorney in your jurisdiction before publishing or relying on a privacy policy.
EOF
```

## Examples

### Example 1: B2B SaaS startup — Iubenda full stack
**Goal:** Launch with privacy policy + cookie banner + DPA + DSAR portal.
**Steps:**
1. Sign up for Iubenda Ultra (Recipe 1 + 6).
2. Run Recipe 1 to generate privacy policy; pick all sub-processors from catalog.
3. Run Recipe 3 to auto-scan cookies + generate cookie banner.
4. Run Recipe 6 to generate a DPA template (used in B2B sales).
5. Run Recipe 7 to enable DSAR portal.
6. Embed all four snippets in site footer + relevant pages.
7. Verify against `privacy-policy-gdpr-ccpa` Recipe 7 checklist.
8. Add disclaimer; send to licensed counsel for sign-off before launch.

**Result:** A complete privacy compliance stack live in <2 hours.

### Example 2: US-first SMB — Termly minimum viable
**Goal:** US-only SaaS, need privacy policy + cookie banner.
**Steps:**
1. Sign up for Termly Pro ($10/mo).
2. Run Recipe 2 to generate privacy policy.
3. Run Recipe 4 to set up cookie banner.
4. Embed both.
5. Walk Recipe 10 customization.
6. Add disclaimer; send to licensed counsel.

**Result:** US-compliant privacy stack at minimal cost.

### Example 3: Auto-update policies when GDPR enforcement changes
**Goal:** Keep policy current when EDPB issues new guidance.
**Steps:**
1. Iubenda / Termly auto-update generator output as their team incorporates new EDPB / DPA / state-law changes.
2. The embed snippet always serves the latest version.
3. Set up a calendar reminder quarterly to review the auto-update changelog.
4. For material changes (e.g., new lawful basis category), trigger user notification per `privacy-policy-gdpr-ccpa` §11.

**Result:** Continuous compliance with minimal manual upkeep.

## Edge cases / gotchas

- **Generator catalog gaps.** If you use a sub-processor not in Iubenda's catalog (custom CRM, internal analytics, niche AI vendor), the generator won't auto-list it. ALWAYS verify and add via "Custom Service."
- **Retention defaults are vague.** Generators often say "as long as necessary" — specify actual retention periods for compliance.
- **Lawful basis defaults can be wrong.** Iubenda defaults Google Analytics to "consent"; verify your implementation actually uses consent (rather than running unconditionally).
- **Multi-jurisdiction layering doesn't equal compliance.** Selecting "EU + US + CA + VA" doesn't auto-comply with all. Audit each jurisdiction's specific requirements.
- **Iubenda + Termly copyright on output.** The generated text is licensed for use on YOUR site only — don't republish elsewhere. Switching providers requires regeneration.
- **Embed snippet performance.** Some snippets block render until consent loads. Use async loading; place after critical CSS.
- **GDPR + ePrivacy require consent BEFORE non-essential cookies fire.** A banner that drops cookies on page-load (pre-consent) is non-compliant. Test with a fresh browser session.
- **CCPA "Do Not Sell or Share" link must be present on homepage** even if your generated policy includes the disclosure within it. Verify the link is rendered.
- **DSAR SLA risk.** Iubenda / Termly portals route requests but YOU still must respond within 1 month (GDPR) / 45 days (CCPA). Missed deadlines = enforcement risk.
- **California Privacy Protection Agency (CPPA) signal compliance.** GPC (Global Privacy Control) signals must be honored as opt-out. Confirm generator's CMP respects GPC (Iubenda yes; Termly yes — but always verify in current dashboard).
- **EU-US Data Privacy Framework status.** Validated 2023; Schrems III challenge expected. Generators include DPF language; verify still current.

> Warning: **This is informational guidance from an AI agent. Always consult a licensed attorney in your jurisdiction before publishing or relying on a privacy policy generated by a third-party tool.**

## Sources

- [Iubenda](https://www.iubenda.com/) — privacy + cookie + DPA + DSAR generator.
- [Iubenda Privacy Policy Generator](https://www.iubenda.com/en/privacy-policy-generator)
- [Iubenda API Documentation](https://www.iubenda.com/api/)
- [Termly](https://termly.io/) — privacy + cookie + ToS generator.
- [Termly Privacy Policy Generator](https://termly.io/products/privacy-policy-generator/)
- [Termly Cookie Consent Manager](https://termly.io/products/cookie-consent-manager/)
- [IAB TCF v2.2](https://iabeurope.eu/transparency-consent-framework/) — CMP compliance framework.
- [GPC Specification](https://globalprivacycontrol.org/) — Global Privacy Control signal.
- Sister skills: `privacy-policy-gdpr-ccpa`, `cookie-consent-management-cookiebot-onetrust`, `dpa-data-processing-agreement`.
