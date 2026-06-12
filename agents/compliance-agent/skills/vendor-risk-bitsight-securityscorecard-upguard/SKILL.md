---
name: vendor-risk-bitsight-securityscorecard-upguard
description: TPRM platform integration — BitSight (Forrester 2026 Wave Leader; outside-in cyber risk intelligence), SecurityScorecard (outside-in ratings), UpGuard (TPRM + ASM + data-leak detection combined), Vanta Vendor Risk (integrated with compliance automation), OneTrust TPRM, Whistic Trust Vault, RiskRecon (Mastercard), Black Kite (quant-leaning), ProcessUnity / Prevalent / Aravo (enterprise GRC).
---

# Vendor Risk Ratings + TPRM Platform Integration

Continuous vendor risk monitoring via outside-in ratings + questionnaire automation. 2026 leader: BitSight (Forrester Wave Q2 2026 highest possible score). Coverage of vendor + own attack-surface monitoring increasingly bundled (UpGuard).

## When to use

User says:
- "Vendor risk rating" / "BitSight" / "SecurityScorecard" / "UpGuard"
- "TPRM platform" / "third-party risk management"
- "Outside-in cyber rating"
- "Vendor scorecard"
- "Continuous monitoring vendor"
- "Vendor risk drift alert"
- "Trust Center" / "Whistic Trust Vault"
- "Vendor breach detection"

Companion skills: `tprm-third-party-risk-lifecycle`, `vendor-security-questionnaire-caiq-sig`, `drata-vanta-secureframe-soc2-monitoring`.

## Setup

```bash
# https://www.bitsight.com/
# https://securityscorecard.com/
# https://www.upguard.com/
# https://www.vanta.com/products/third-party-risk-management
# https://www.onetrust.com/products/third-party-management/
# https://www.whistic.com/
# https://riskrecon.com/
# https://blackkite.com/

export BITSIGHT_API_KEY=<dashboard>
export SECURITYSCORECARD_API_KEY=<dashboard>
export UPGUARD_API_KEY=<dashboard>
export VANTA_API_KEY=<dashboard>
export ONETRUST_API_KEY=<dashboard>
export WHISTIC_API_KEY=<dashboard>
```

Auth notes:
- BitSight rates ~600K orgs daily; sample reports free for self.
- SecurityScorecard free for self-rating (your own org); paid for vendor monitoring.
- UpGuard: BreachSight (own ASM) + Vendor Risk + Trust Exchange.

## Common recipes

### Recipe 1: Vendor tiering (drives rating service depth)

```text
Tier 1 (Critical) — handles personal data / financial / IP / business-critical:
- Continuous outside-in rating (BitSight / SecurityScorecard / UpGuard)
- Annual SIG Plus / SOC 2 Type II / ISO 27001 + DPA + BAA where applicable
- Quarterly mini-reassessment
- Real-time breach alerts

Tier 2 (High) — internal-only sensitive data / critical biz process:
- Continuous rating
- Biennial SIG Core / SOC 2 Type II + DPA
- Quarterly news + adverse-media monitoring

Tier 3 (Moderate) — non-sensitive but accesses systems:
- Optional outside-in rating (cost-driven)
- Triennial SIG Lite + DPA if any data
- News monitoring

Tier 4 (Low) — registration only:
- Standard contract + registration
- Annual contract review
```

### Recipe 2: BitSight API — pull company rating + findings

```bash
# https://help.bitsighttech.com/hc/en-us/articles/204676254-API-Documentation
# Get company by GUID
curl -X GET 'https://api.bitsighttech.com/ratings/v1/companies' \
  -H "Authorization: Token $BITSIGHT_API_KEY" \
  -H "Accept: application/json"

# Findings by company
curl -X GET 'https://api.bitsighttech.com/ratings/v1/companies/<guid>/findings' \
  -H "Authorization: Token $BITSIGHT_API_KEY"

# Subscriptions (create alert)
curl -X POST 'https://api.bitsighttech.com/ratings/v1/companies/<guid>/subscriptions' \
  -H "Authorization: Token $BITSIGHT_API_KEY" \
  -d '{"type":"alert","frequency":"daily"}'
```

### Recipe 3: SecurityScorecard API

```bash
# https://platform-docs.securityscorecard.io/
curl -X GET 'https://api.securityscorecard.io/companies/<domain>' \
  -H "Authorization: Token $SECURITYSCORECARD_API_KEY"

# Issues for a company
curl -X GET 'https://api.securityscorecard.io/companies/<domain>/issues/<type>' \
  -H "Authorization: Token $SECURITYSCORECARD_API_KEY"
```

### Recipe 4: UpGuard API

```bash
# https://upguard.docs.apiary.io/
# List vendors
curl -X GET 'https://cyber-risk.upguard.com/api/public/vendors' \
  -H "Authorization: Token $UPGUARD_API_KEY"

# Vendor rating + issues
curl -X GET 'https://cyber-risk.upguard.com/api/public/vendors/<vendorId>/issues' \
  -H "Authorization: Token $UPGUARD_API_KEY"
```

### Recipe 5: Vanta Vendor Risk

```bash
# https://developer.vanta.com/
# Vendors list
curl -X GET 'https://api.vanta.com/v1/vendors' \
  -H "Authorization: Bearer $VANTA_API_KEY"

# Vendor questionnaire status
curl -X GET 'https://api.vanta.com/v1/vendors/<id>/questionnaires' \
  -H "Authorization: Bearer $VANTA_API_KEY"
```

### Recipe 6: OneTrust TPRM

```bash
# https://developer.onetrust.com/
curl -X GET 'https://app.onetrust.com/api/inventory/v2/inventories/vendors' \
  -H "Authorization: Bearer $ONETRUST_API_KEY"
```

### Recipe 7: Outside-in rating taxonomies

```text
BitSight grade ranges:
- 740-900 (Advanced) — top performers
- 640-740 (Intermediate)
- 250-640 (Basic / Poor) — high risk

Core categories (BitSight):
- Compromised systems
- Diligence (TLS, DNSSEC, SPF, DKIM, DMARC, web app headers, patching cadence)
- User behavior (file sharing, P2P, BitTorrent)
- Public disclosures (data breaches in news / leak forums)

SecurityScorecard categories:
- Network security
- DNS health
- Patching cadence
- Endpoint security
- IP reputation
- Application security
- Cubit score (composite)
- Hacker chatter
- Information leak
- Social engineering

UpGuard categories:
- Network security
- Website security
- Email security (SPF/DKIM/DMARC)
- Brand protection (phishing impersonation)
- Reputation risk (data leaks)
```

### Recipe 8: DMARC / SPF / DKIM check (a key outside-in signal)

```bash
# DMARC check for a vendor
dig +short TXT _dmarc.<vendor-domain>

# SPF
dig +short TXT <vendor-domain> | grep "v=spf1"

# DKIM (selector varies — default, google, k1)
dig +short TXT default._domainkey.<vendor-domain>
dig +short TXT google._domainkey.<vendor-domain>

# Use mxtoolbox / dmarcian for richer parsing
curl -fsSL "https://api.dmarcian.com/v1/dmarc/parse/<vendor-domain>"
```

A missing or weak DMARC (`p=none` instead of `p=reject`) is a common BitSight / SecurityScorecard demerit.

### Recipe 9: TLS cert + cipher audit

```bash
# Cert expiry + chain
echo | openssl s_client -servername <vendor> -connect <vendor>:443 2>/dev/null | \
  openssl x509 -noout -dates -subject -issuer

# Cipher audit (sslyze open-source)
pip install sslyze
sslyze <vendor>:443 --json_out=tls_audit.json

# Public scoring: SSL Labs (Qualys)
curl -fsSL "https://api.ssllabs.com/api/v3/analyze?host=<vendor>&publish=off"
```

### Recipe 10: Vendor scorecard template

```markdown
# Vendor Risk Scorecard — <Vendor>

**Date:** <YYYY-MM-DD>
**Reviewer:** <name>
**Tier:** <1 Critical / 2 High / 3 Moderate / 4 Low>
**Data sensitivity:** <PII / PHI / PCI / IP / public>
**Business criticality:** <Critical / Important / Useful>
**Contract value (annual):** $<amount>
**Renewal date:** <YYYY-MM-DD>

## Outside-in ratings
| Source | Score | Trend (90d) |
|---|---|---|
| BitSight | <score> | <+/-> |
| SecurityScorecard | <score> | <+/-> |
| UpGuard | <score> | <+/-> |

## Top findings
- <Finding 1 — severity — first-seen date>
- <Finding 2>
- <Finding 3>

## Inside-out evidence
- SOC 2 Type II: <on file? expiry?>
- ISO 27001: <on file? expiry?>
- HIPAA BAA (if applicable): <signed Y/N>
- DPA (GDPR): <signed Y/N>
- SCC + TIA (if EU transfer): <on file Y/N>
- Pen test report: <on file? date?>
- Insurance: <cyber liability $X coverage>

## Recommendations
- <Required remediation>
- <Conditional on>
- <Termination consideration if>

## Decision
- Approve / Approve conditional / Hold / Deny

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

### Recipe 11: Drift alert handling

```text
When BitSight / SecurityScorecard / UpGuard rating drops:

1. Triage severity:
   - Drop >25 points = critical (review urgent)
   - Drop 10-25 = moderate (review in 5 business days)
   - Drop <10 = informational (next quarterly review)

2. Identify cause:
   - New finding (CVE, breach, leak)
   - Lapsed cert
   - Adverse media

3. Contact vendor:
   - For Tier 1: Direct contact to vendor security team
   - For Tier 2+: Async email

4. Document outcome:
   - Vendor remediated (confirm score recovery)
   - Vendor explained (compensating control)
   - Vendor declined to address → escalate to risk committee

5. Re-tier if persistent:
   - Persistent low score may trigger Tier elevation or termination.
```

### Recipe 12: Whistic Trust Vault (vendor-shared evidence)

```text
Whistic operates a Trust Vault model:
- Vendor publishes SOC 2 / ISO / questionnaire answers once.
- Customers request access; vendor approves.
- Reduces "answer same SIG 1000 times" overhead for vendors.

Customer side:
1. Search Whistic for vendor.
2. Request Vault access.
3. Vendor approves; auto-imports evidence into your TPRM.

Vendor side:
- Curate Vault with current evidence.
- Set approval policies (auto for known logos, manual for new).
- Update SOC 2 + ISO + pen-test annually.

Similar: Vanta Trust Reports, Drata Trust Center, Secureframe Trust.
```

### Recipe 13: Vendor breach response

```text
When vendor announces breach:

1. Immediate (T+0):
   - Confirm if affected (vendor inquiry + UpGuard/BitSight breach feed).
   - Inventory data exposed (per ROPA).
   - Containment: rotate credentials / API keys with vendor.

2. T+1-3 days:
   - Engage vendor security team for forensics.
   - Trigger IR plan if confirmed exposure (`incident-response-nist-sp-800-61`).
   - Customer notification consideration (`breach-notification-gdpr-72hr-state-laws`).

3. T+7-14 days:
   - Demand vendor incident report.
   - Re-rate vendor; consider termination.
   - Document lessons learned.

4. T+30-60 days:
   - Reassess vendor TPRM tier.
   - Update vendor onboarding controls.
```

## Examples

### Example 1: Onboarding Tier 1 vendor with rating + SIG

**Goal:** Add new Tier 1 vendor (data subprocessor) to TPRM stack.

**Steps:**
1. BitSight rating pull (Recipe 2) — score 720; no critical findings.
2. SIG Plus request (~1100 Q) via Vanta Vendor Risk (Recipe 5).
3. SOC 2 Type II review (carve-out for AWS sub-sub-service).
4. DPA + BAA execution (per `legal-counsel`).
5. Configure continuous monitoring alerts (drift >25 points → ticket).
6. Vendor scorecard (Recipe 10) → senior approval.
7. Onboarded; calendar annual reassessment.

**Result:** Compliant onboarding; continuous monitoring in place.

### Example 2: Drift alert response

**Goal:** BitSight score drops 30 points overnight; investigate.

**Steps:**
1. Severity = critical (Recipe 11).
2. Pull findings (Recipe 2). Root cause: leaked credentials on a paste site.
3. Contact vendor: confirm awareness + remediation timeline.
4. Vendor remediated within 48h; rating recovers.
5. Document; no termination needed.

**Result:** Drift handled within SLA; auditable trail.

### Example 3: Vendor sub-processor breach

**Goal:** Sub-processor breach announced; assess our exposure + notify customers.

**Steps:**
1. Inventory data shared with sub-processor (per ROPA + DPA).
2. Vendor incident report: 14 days from breach.
3. Forensics: 12% of our customer records exposed (email + name).
4. Risk assessment per `breach-notification-gdpr-72hr-state-laws`.
5. GDPR Art. 33 notification within 72h to lead SA (low risk → no individual notice).
6. CCPA: 500+ CA residents affected → Cal AG + individuals.
7. Re-rate vendor; consider termination; insurance claim.

**Result:** Compliant cascading breach response; vendor risk re-tiered.

## Edge cases / gotchas

- **Outside-in ratings are SIGNALS, not GROUND TRUTH.** They detect what's visible from the internet; can miss insider risk + internal control weaknesses.
- **False positives in adverse media + leak feeds.** Cross-verify before raising tickets.
- **Vendor disputes ratings** — BitSight + SS allow vendor-side appeals; expect 2-4 weeks resolution.
- **Free-tier ratings (self-rating only).** Vendor monitoring requires paid.
- **Coverage gaps** — outside-in services struggle with private cloud + on-prem-only vendors.
- **Cost** — enterprise tiers $50K-$500K/yr; budget per vendor monitored. Tier 1 + Tier 2 only typically.
- **Whistic Trust Vault adoption uneven** — many vendors still respond manually.
- **Multiple ratings vendors required for completeness** — BitSight + SecurityScorecard often disagree by 50+ points.
- **Brand impersonation findings** — domain squatting flagged but mostly false-positive noise; tune.
- **Acquisition / merger of vendor** — re-rate post-acquisition. GUID/domain changes can lose history.
- **SaaS sub-sub-processor visibility** — Vendor → Vendor → Vendor → ... external rating only covers top-level domain.
- **Regulatory expectations.** DORA (EU financial) + OCC (US bank) + NYDFS expect continuous vendor monitoring; outside-in rating is standard evidence.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [BitSight](https://www.bitsight.com/)
- [BitSight API Docs](https://help.bitsighttech.com/hc/en-us/articles/204676254-API-Documentation)
- [SecurityScorecard](https://securityscorecard.com/)
- [SecurityScorecard API Docs](https://platform-docs.securityscorecard.io/)
- [UpGuard](https://www.upguard.com/)
- [UpGuard API Docs](https://upguard.docs.apiary.io/)
- [Vanta Vendor Risk](https://www.vanta.com/products/third-party-risk-management)
- [OneTrust TPRM](https://www.onetrust.com/products/third-party-management/)
- [Whistic](https://www.whistic.com/)
- [RiskRecon (Mastercard)](https://riskrecon.com/)
- [Black Kite](https://blackkite.com/)
- [ProcessUnity](https://www.processunity.com/)
- [Prevalent](https://www.prevalent.net/)
- [Aravo](https://www.aravo.com/)
- [Forrester Wave: Cybersecurity Risk Ratings 2026](https://www.bitsight.com/resources/forrester-wave-cybersecurity-risk-ratings)
- [SSL Labs (Qualys)](https://www.ssllabs.com/ssltest/)
- [Dmarcian](https://dmarcian.com/)
