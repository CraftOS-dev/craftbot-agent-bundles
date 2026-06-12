---
name: pci-dss-scope-reduction-saq-selection
description: Reduce PCI DSS v4.0 scope via tokenization (Stripe / Braintree / Adyen / Spreedly), iframe / hosted-fields, P2PE-validated POS. Pick the right SAQ (A / A-EP / B / B-IP / C / C-VT / D) based on acceptance channel. Plan v4.0 future-dated requirements (effective March 31, 2025; steady-state by 2026). Annual ASV scans + pen test + segmentation pen test. ROC for Level 1; SAQ for L2-L4.
---

# PCI DSS v4.0 Scope Reduction + SAQ Selection

PCI DSS v4.0 (effective March 2024; v4.0.1 minor 2024 update; future-dated requirements effective March 31, 2025 — steady-state by 2026). The fastest cost reduction is scope reduction via tokenization. The right SAQ depends on acceptance channel.

## When to use

User says:
- "PCI DSS" / "PCI compliance" / "PCI v4.0"
- "SAQ A" / "SAQ A-EP" / "SAQ D" / "ROC"
- "Tokenization" / "Stripe Checkout" / "Braintree iframe"
- "P2PE" / "Point-to-Point Encryption"
- "Network segmentation" / "CDE scope"
- "ASV scan" / "Quarterly external scan"
- "QSA" / "Qualified Security Assessor"
- "Level 1" / "Level 2" / "Level 4" merchant
- "Annual pen test PCI"

Companion skills: `vulnerability-mgmt-tenable-qualys-snyk`, `pentest-coordination-hackerone-bugcrowd`, `incident-response-nist-sp-800-61`.

## Setup

```bash
# PCI SSC Document Library (public docs free; some require free account)
curl -fsSL https://www.pcisecuritystandards.org/document_library/ > /tmp/pci_lib.html

# PCI DSS v4.0 (~400 pages)
# Download via PCI SSC site (requires free account for some docs)

# SAQ templates (public)
# https://www.pcisecuritystandards.org/document_library?category=saqs

# Stripe PCI Compliance Guide (free, comprehensive)
curl -fsSL https://stripe.com/guides/pci-compliance > /tmp/stripe_pci.html

# Braintree compliance
curl -fsSL https://www.braintreepayments.com/features/data-security > /tmp/braintree.html

# Adyen compliance
curl -fsSL https://www.adyen.com/knowledge-hub/pci-dss > /tmp/adyen.html

# Spreedly (cross-gateway tokenization)
curl -fsSL https://www.spreedly.com/blog/pci-compliance > /tmp/spreedly.html

# Approved ASV list (PCI SSC)
curl -fsSL https://www.pcisecuritystandards.org/assessors_and_solutions/approved_scanning_vendors > /tmp/asv.html

# Approved QSA list
curl -fsSL https://www.pcisecuritystandards.org/assessors_and_solutions/qualified_security_assessors > /tmp/qsa.html
```

Auth notes:
- PCI SSC documents largely free; some advisories require free account.
- ASV scans are paid services from PCI SSC-approved vendors (Qualys, Trustwave, Sysnet, ControlScan).

## Common recipes

### Recipe 1: Merchant Level determination

```text
Level 1: 6M+ Visa/MC card transactions/year (per brand), OR
         ANY breach history (regardless of volume), OR
         any merchant deemed Level 1 by acquirer/brand.
→ ROC (Report on Compliance) by QSA.
→ Annual external pen test + quarterly ASV scans + internal scans.

Level 2: 1M-6M card transactions/year.
→ SAQ + Attestation of Compliance (AOC) signed by exec.

Level 3: 20K-1M e-commerce transactions/year.
→ SAQ + AOC.

Level 4: <20K e-commerce OR <1M total card transactions.
→ SAQ + AOC.

Service providers:
- Level 1 SP: 300K+ transactions OR acquirer-designated → ROC.
- Level 2 SP: <300K → SAQ-D.
```

### Recipe 2: SAQ selection decision tree

```text
SAQ A — Card-not-present (CNP) e-commerce + mail/telephone order, FULLY
        OUTSOURCED to PCI DSS validated 3P.
- Examples: redirect to Stripe Checkout; PayPal redirect; iframe with
  Stripe / Braintree / Adyen hosted fields (no CHD touches your servers).
- Form: ~22 questions.
- EASIEST PATH.

SAQ A-EP — E-commerce, payment page hosted by 3P but merchant impacts
           security/integrity of payment page.
- Examples: merchant-served HTML + 3P JS (Stripe.js direct integration); 
  page is on merchant domain but cardholder data flows direct to 3P.
- Form: ~138 questions.
- More work than SAQ A; usually arises with custom checkout UI.

SAQ B — Imprint machine OR standalone dial-out terminal only. No
        internet-connected systems.

SAQ B-IP — Standalone IP-connected POS terminal only. No CHD electronic
           storage.

SAQ C — POS systems connected to internet. No e-commerce.
        ~162 questions.

SAQ C-VT — Virtual terminal only (one workstation, dial-out OR internet to
           PCI DSS validated 3P).

SAQ D — Catch-all: any merchant + ALL service providers not covered above.
        ~329 questions.

SAQ P2PE — Merchants using PCI P2PE-validated solution exclusively.
           Reduced scope.
```

### Recipe 3: Tokenization architecture (Stripe Checkout — SAQ A)

```text
Merchant site → "Pay" button → Redirect to checkout.stripe.com (on Stripe domain).
Cardholder enters CHD ON STRIPE'S DOMAIN.
Stripe returns payment_intent + token to merchant.
Merchant stores only Stripe ID (e.g., pi_xxxxx); NEVER touches CHD.

Result: zero CHD in merchant systems. SAQ A.

Stripe Elements (Recipe 4) is SAQ A if cardholder data flows direct to
Stripe (DOM is merchant's; iframe is Stripe's). Stripe.js direct
integration without iframe is SAQ A-EP because merchant page integrity
matters.

Verification: open browser dev tools at checkout. Confirm card field is in
an iframe with src="https://js.stripe.com" or similar. If card field is
merchant DOM, you're SAQ A-EP.
```

### Recipe 4: Stripe Elements (iframe / hosted fields) — SAQ A

```html
<!-- Merchant page -->
<form id="payment-form">
  <div id="payment-element"><!-- Stripe iframe injected here --></div>
  <button>Pay</button>
</form>

<script src="https://js.stripe.com/v3/"></script>
<script>
const stripe = Stripe('pk_live_xxx');
const elements = stripe.elements({clientSecret: '<from server>'});
const paymentElement = elements.create('payment');
paymentElement.mount('#payment-element');
// Card data never touches merchant servers.
</script>
```

### Recipe 5: Braintree Hosted Fields — SAQ A

```html
<!-- Card fields are iframes from Braintree -->
<div id="card-number"></div>
<div id="expiration-date"></div>
<div id="cvv"></div>

<script src="https://js.braintreegateway.com/web/3.x/js/hosted-fields.min.js"></script>
```

### Recipe 6: P2PE-validated POS (in-person)

```text
P2PE = Point-to-Point Encryption — PCI SSC-validated solution that encrypts
CHD at point of capture (POS terminal) and decrypts only at the acquirer.

Merchant systems NEVER see plaintext CHD.

Validated solutions: Adyen, Bluefin, Fiserv P2PE, Verifone P2PE.

Use case: brick-and-mortar retail, restaurants, kiosks.

Result: SAQ P2PE; massive scope reduction.
```

### Recipe 7: v4.0 12 Requirement areas (high-level)

```text
1.  Network security controls (was "firewalls")
2.  Secure system + software config (was "vendor default passwords")
3.  Protect stored CHD (encryption, key mgmt, PAN masking)
4.  Protect CHD in transit over open / public networks (TLS 1.2+)
5.  Protect against malicious software (anti-malware; v4.0 added scoping
    options)
6.  Develop + maintain secure systems + software (incl. PCI DSS Req. 6.5
    list of vulns to address)
7.  Restrict access by need-to-know (RBAC)
8.  Identify + authenticate users (MFA expanded in v4.0)
9.  Restrict physical access (CHD + facilities)
10. Log + monitor (log retention ≥1yr; 3mo immediately available)
11. Test security (ASV quarterly; internal scans quarterly; pen test annual
    + on change; segmentation pen test annual SP / biennial merchant)
12. Information security policy + risk + training (Req. 12.6 awareness;
    12.10 incident response; 12.8 vendor TPRM)
```

### Recipe 8: v4.0 future-dated requirements (effective March 31, 2025)

```text
v4.0 introduced several future-dated requirements. By 2026 these are in
steady-state — auditors expect full implementation.

Highlights:
- Req. 8.3.6 — authenticated internal vuln scans (was unauthenticated)
- Req. 8.4.2 — MFA for ALL access to CDE (was only admin/remote)
- Req. 8.5.1 — anti-phishing controls
- Req. 11.6.1 — change + tamper detection on payment pages
- Req. 12.3.1 — periodic risk-based review (RBA inventory)
- Req. 12.5.2 + 12.5.3 — annual PCI DSS scope confirmation
- Req. 12.6.3 — awareness training reflecting threats + responsibilities
- Customized Approach Option — alternative methods to satisfy a control
  with QSA validation (use cautiously).
```

### Recipe 9: Network segmentation pen test scoping

```text
Required (v4.0 Req. 11.4.5 + 11.4.6):
- Service providers: annually + on segmentation change.
- Merchants: biennially + on segmentation change.

Scope: validate that segmentation controls isolate CDE from out-of-scope
systems. Tester attempts pivot from out-of-scope into CDE.

Methodology:
1. Inventory all segmentation controls (firewalls, VLANs, SDN policies).
2. Diagram CDE + connected systems.
3. External tester attempts:
   - Pivot from out-of-scope LAN → CDE
   - Cross-VLAN traversal
   - Misconfigured firewall rules
4. Report: any successful pivot = scope failure; in-scope grows.

QSAs / pen test firms: Coalfire, A-LIGN, NCC Group, Bishop Fox,
SecurityMetrics.
```

### Recipe 10: ASV scan quarterly cadence

```text
PCI SSC-Approved Scanning Vendor (ASV) external scans.
Quarterly + after material change.

Process:
1. Provide ASV with internet-facing IPs / hostnames.
2. ASV runs vulnerability scan.
3. ASV issues "Attestation of Scan Compliance" (ASC) or non-compliance.
4. Failed scans: remediate + rescan within reasonable period.

Common ASVs: Qualys, Trustwave, ControlScan, Sysnet (Forter),
SecurityMetrics, Cipher.

Cost: $500-$5,000/year depending on IPs.

ASV scans are EXTERNAL. Quarterly INTERNAL scans (Req. 11.3.1) can be
self-conducted with any vuln scanner (Nessus, Qualys, OpenVAS, Rapid7).
```

### Recipe 11: Scope memo template

```markdown
# PCI DSS Scope Memo — <Co.>

**Effective:** <date>
**Owner:** <Sec Lead>
**Standard:** PCI DSS v4.0.1
**Card brands accepted:** Visa, MC, Amex, Discover
**Acquirer(s):** <name>
**Annual transactions (per brand):** <#>
**Merchant level (per brand):** <1/2/3/4>

## Acceptance channels
- E-commerce: Stripe Checkout redirect (SAQ A path)
- In-person: <none> / <P2PE Adyen terminal>
- Phone: <none> / <virtual terminal>

## CHD storage
- NEVER stored in merchant systems.
- Stripe stores tokenized CHD (pi_xxxx + cus_xxxx); merchant retains ID only.

## SAQ determination
- E-commerce: SAQ A (fully outsourced + iframe).
- (If applicable) In-person: SAQ P2PE.

## CDE inventory
- (List in-scope systems; for fully tokenized SAQ A, CDE may be empty or
  minimal — e.g., admin laptops with access to Stripe Dashboard.)

## Connected systems
- (List systems with connectivity to CDE; SAQ A typically has none.)

## Out-of-scope systems
- (Vast majority of merchant infra is out-of-scope when SAQ A applies.)

## Segmentation evidence
- (Firewall config, VLAN config, SDN policy reference.)
- Segmentation pen test: <date>; result: pass.

## Annual obligations
- SAQ + AOC signed by exec officer.
- Quarterly ASV scan (Qualys).
- Quarterly internal vuln scan.
- Annual pen test.
- Annual segmentation pen test (biennial for L4 merchant).
- Annual scope confirmation (Req. 12.5.2).
- Annual policy review.
- Annual training (Req. 12.6).

---
*This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.*
```

### Recipe 12: Common scope-creep traps

```text
Even with SAQ A path, scope can creep:
- Email contains last 4 + name + expiry — minimal exposure but Req. 3.3 PAN
  truncation still applies.
- CSR receives card on phone, enters into 3P virtual terminal — virtual
  terminal workstation is in-scope (SAQ C-VT).
- Call recording: any chance of full PAN spoken → out-of-scope by Pause-
  and-Resume OR scope in.
- Refund processing via dashboard: admin laptop in-scope for SAQ A if
  dashboard reveals full PAN.
- Customer support tickets — customer pastes full card # → in-scope unless
  PII redaction blocks it.

Mitigations:
- DLP rules block PAN patterns in email, tickets, Slack.
- Pause-and-Resume call recording.
- PAN masking in admin dashboards.
- Train staff not to take CHD outside payment workflow.
```

### Recipe 13: QSA selection (Level 1)

```text
PCI SSC-Approved Qualified Security Assessors.

Top QSAs (2026):
- A-LIGN — broad SaaS practice
- Coalfire — security-focused; popular SaaS pick
- Trustwave — mature global
- SecurityMetrics — mid-market SMB
- NCC Group — UK + global; tech-deep
- Schellman — SOC 2 + ISO + PCI combo
- Sysnet (Forter) — fraud + PCI combo
- Wesley K. Clark + Associates — smaller boutique
- Sword & Shield — defense-adjacent

Cost: $25K-$150K ROC depending on scope. SAQ-Plus advisory: $5K-$25K.

Reference-check on:
- Industry experience (your vertical)
- Acquirer alignment
- Documentation style (auditor-friendly vs gating)
```

## Examples

### Example 1: E-commerce startup minimizing scope

**Goal:** Launch with SAQ A, never touch CHD.

**Steps:**
1. Integrate Stripe Checkout (redirect) OR Stripe Elements iframe.
2. Verify in browser dev tools: card field is iframe from js.stripe.com.
3. Scope memo per Recipe 11.
4. Quarterly ASV via Qualys (~$1K/yr).
5. Quarterly internal scan via Nessus.
6. SAQ A completion (22 questions); AOC signed.
7. Train staff: never accept CHD over email / phone / chat.

**Result:** Full PCI DSS compliance at minimal cost (~$2K-$5K/year all-in).

### Example 2: Mid-market merchant moving from D to A-EP

**Goal:** Refactor checkout to drop SAQ D → SAQ A-EP via Braintree Hosted Fields.

**Steps:**
1. Replace own card form with Braintree Hosted Fields (Recipe 5).
2. Confirm cardholder data flows direct to Braintree (browser dev tools).
3. Re-scope per Recipe 11 — CDE shrinks dramatically.
4. New SAQ A-EP completion.
5. Annual pen test focuses on web app (preserving payment page integrity).

**Result:** SAQ D → SAQ A-EP. Audit effort drops ~70%; cost drops $30K → $8K.

### Example 3: Adding a virtual terminal for phone orders

**Goal:** CSR takes phone orders; how to scope.

**Steps:**
1. Option A: CSR uses Stripe Dashboard manual payment (3P virtual terminal).
   - In-scope: CSR workstation, network path to Stripe Dashboard.
   - SAQ C-VT.
2. Option B: CSR sends Stripe Payment Link to customer.
   - Customer enters CHD on Stripe domain.
   - SAQ A (no CSR exposure to CHD).
3. Pick Option B.

**Result:** Maintain SAQ A by structuring workflow to route customers to Stripe-hosted form.

## Edge cases / gotchas

- **Stripe Elements direct vs iframe is a SUBTLE distinction.** Direct = SAQ A-EP. Iframe = SAQ A. Read Stripe docs carefully.
- **3P scripts on payment page (analytics, A/B testing, chat widgets) can compromise SAQ A.** v4.0 Req. 6.4.3 + 11.6.1 require change + tamper detection. Block third-party scripts on checkout pages.
- **Stripe Checkout drops you to SAQ A;** Stripe Connect adds nuance for marketplaces.
- **Apple Pay / Google Pay / wallets do NOT exempt PCI DSS** but typically maintain SAQ A path because wallets handle tokenization.
- **Saved cards / vault** — Stripe Customer + payment_method API stores cards in Stripe Vault; merchant stores only IDs. Maintains SAQ A.
- **AWS / GCP / Azure are PCI DSS Level 1 Service Providers** (their controls list). You still need YOUR SAQ/ROC; their AOC covers infrastructure CUEC.
- **Logs containing PAN are bad.** Centralized logging (Datadog, Splunk) — apply PAN masking at ingest. Otherwise log infra becomes in-scope.
- **Email-from-customer with full PAN** — by accepting it, you scoped yourself in. Reject + redirect to secure payment link.
- **PCI DSS does NOT preempt state breach notification.** A CHD breach triggers state + PCI brand notification (acquirer agreement).
- **Compliance ≠ security.** PCI DSS sets a floor; breaches happen to PCI-compliant orgs. Don't conflate.
- **Customized Approach Option (v4.0)** is powerful but requires QSA validation. Don't use for first audit.
- **Penalties.** Card brand fines $5K-$100K/month per acquirer; acquirers can suspend merchant accounts. Indirect: forensic costs, brand damage, breach litigation.
- **Annual scope confirmation (Req. 12.5.2)** — auditors now expect a documented scope review every year. Calendar it.

> ⚠ **This is informational guidance from an AI agent. Always consult a qualified compliance professional, auditor, or privacy attorney in your jurisdiction before submitting audit responses, accepting auditor findings, or implementing binding control changes.**

## Sources

- [PCI Security Standards Council](https://www.pcisecuritystandards.org/)
- [PCI DSS Document Library](https://www.pcisecuritystandards.org/document_library/)
- [PCI DSS v4.0 + v4.0.1 Standard](https://www.pcisecuritystandards.org/document_library?category=pcidss&document=pci_dss)
- [SAQs](https://www.pcisecuritystandards.org/document_library?category=saqs)
- [Stripe PCI Compliance Guide](https://stripe.com/guides/pci-compliance)
- [Stripe Checkout — SAQ A](https://stripe.com/docs/payments/checkout)
- [Stripe Elements](https://stripe.com/docs/payments/elements)
- [Braintree Hosted Fields](https://developers.braintreepayments.com/guides/hosted-fields/overview)
- [Adyen PCI DSS](https://www.adyen.com/knowledge-hub/pci-dss)
- [Spreedly tokenization](https://www.spreedly.com/)
- [P2PE Validated Solutions](https://www.pcisecuritystandards.org/assessors_and_solutions/point_to_point_encryption_solutions)
- [ASV Approved List](https://www.pcisecuritystandards.org/assessors_and_solutions/approved_scanning_vendors)
- [QSA Approved List](https://www.pcisecuritystandards.org/assessors_and_solutions/qualified_security_assessors)
- [Coalfire PCI](https://www.coalfire.com/services/payment-card-industry/pci-compliance-validation)
- [A-LIGN PCI](https://www.a-lign.com/services/pci-dss)
