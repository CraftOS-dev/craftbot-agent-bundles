<!--
Sources: https://www.embroker.com/coverage/startup-insurance/
         https://www.vouch.us/blog/what-is-startup-business-insurance-and-why-do-i-need-it
         https://www.svb.com/startup-insights/startup-strategy/startup-insurance-guide-for-founders/
Vouch = startup-only, digital, web3 + AI native coverage. Embroker = D&O + E&O + Cyber + EPLI instant bundle.
2026 median cyber premium ≈ $2,968.
-->
# Business Insurance Audit — Vouch / Embroker / Newfront — SKILL

Audit and right-size business insurance coverage: General Liability, Business Property, D&O, E&O / Tech E&O, EPLI, Cyber, Workers' Comp, Crime, International. Stage-based stack ordering. Renewal calendar with quote-shopping playbook. Vouch / Embroker / Newfront / Founder Shield / Coalition / At-Bay broker selection.

## When to use

- New company → first insurance stack.
- Fundraise close → D&O policy purchase.
- Customer security requirement → Cyber liability + SOC 2.
- Hiring first US employee → state-specific Workers' Comp.
- Annual renewal audit.
- Trigger phrases: "insurance", "D&O", "E&O", "EPLI", "Cyber", "Workers' Comp", "Vouch", "Embroker", "Newfront", "renewal", "coverage", "binder".

## Setup

```bash
export VOUCH_TOKEN="xxx"           # https://vouch.us — quote API limited to brokers/partners
export EMBROKER_TOKEN="xxx"        # https://embroker.com
export NEWFRONT_TOKEN="xxx"        # https://newfront.com
# Quote-pull endpoints largely partner-only; use Notion + Drive for tracking.
```

## Common recipes

### Recipe 1: Stage / stack ordering
```yaml
coverage_stack_by_stage:
  pre_seed_seed:
    must:
      - General Liability ($1M / $2M aggregate)
      - Business Personal Property (if office)
      - Cyber Liability (customer security req)
      - EPLI (any hire — wrongful term, discrimination claims)
      - Workers' Comp (any state per state-specific requirement)
    nice_to_have:
      - Crime / Employee Dishonesty
  series_a:
    add:
      - D&O Liability (post-priced-round; protects board + officers)
      - Tech E&O / Professional Liability
      - Cyber (raise limits to $3-5M)
    nice_to_have:
      - International coverage if hiring outside US
  series_b_plus:
    add:
      - Higher limits on D&O ($5-10M)
      - International package
      - Employed Lawyers if internal counsel
      - Crime ($1M+)
      - Product Liability if hardware
  series_c_plus_or_pre_ipo:
    add:
      - Excess/umbrella D&O ($25M-50M)
      - Side A D&O (covers individuals when company can't indemnify)
      - Fiduciary Liability (ERISA)
      - K&R if travel to high-risk geos
```

### Recipe 2: Broker / carrier selection
```yaml
choose:
  startup_only_digital_web3_ai:
    primary: Vouch
    why: Startup-specific carrier; web3 + AI-native coverage; entirely digital
  startup_package_instant_bundle:
    primary: Embroker
    why: Startup Package — D&O + E&O + Cyber + EPLI in one bundled instant quote
  white_glove_broker:
    primary: Newfront
    why: InsureTech broker; modern UX; deep market access
  cyber_specialist:
    primary: At-Bay or Coalition
    why: Best-of-breed cyber underwriting; active monitoring
  founder_shield:
    primary: Founder Shield
    why: Boutique startup broker; D&O specialty
  enterprise_carrier:
    primary: Hartford or Travelers or Chubb (via broker)
    why: Established carriers; lower premiums at scale
```

### Recipe 3: Coverage audit checklist (Notion DB row per policy)
```yaml
policy_record:
  type: D&O / E&O / Cyber / EPLI / WC / GL / Property / Crime / Tech E&O
  carrier: <name>
  policy_number: <num>
  broker: <name>
  effective_date: 2026-07-01
  expiry_date: 2027-06-30
  premium_USD: 12000
  limit_per_claim_USD: 2000000
  limit_aggregate_USD: 5000000
  deductible_USD: 25000
  retention_USD: 0
  notice_window_days: 60
  certificates_of_insurance_path: drive://Insurance/COIs/2026-07/
  binder_path: drive://Insurance/Binders/2026/d-and-o-binder.pdf
  application_path: drive://Insurance/Apps/2026-D-and-O-app.pdf
  exclusions_summary:
    - "Bodily injury (carve to GL)"
    - "Prior knowledge of claim"
    - "Insured-vs-insured (most modern D&O carves)"
  audit_findings:
    - "[ ] Limits adequate for current ARR?"
    - "[ ] Retroactive date covers prior work?"
    - "[ ] All controlling stakeholders covered?"
```

### Recipe 4: 2026 premium benchmarks (per Vouch/Embroker public reports)
```yaml
typical_annual_premium_ranges_USD:
  general_liability_1m_2m:
    pre_seed: 400-700
    series_a: 600-1500
  business_personal_property: 500-2000
  cyber_liability_2m_3m:
    pre_seed: 1500-3500
    series_a: 2500-5500     # 2026 median ~ $2,968
    series_b: 5500-15000
  d_and_o_2m:
    series_a: 8000-15000
    series_b: 15000-30000
    series_c: 30000-75000
  e_and_o_tech_2m:
    series_a: 6000-12000
    series_b: 12000-25000
  epli_2m:
    series_a: 3000-7000
    series_b: 7000-15000
  workers_comp:
    per_payroll_pct: 0.5-2.5     # by state + class code; CA + NY heaviest
  crime_500k:
    typical: 2000-5000
```

### Recipe 5: 2026 cyber-coverage scope (what insurers expect to see)
```yaml
cyber_underwriting_checklist:
  required_to_get_decent_quote:
    - MFA on email + admin tools (Recipe: sso-okta-jumpcloud-workos)
    - Endpoint detection (EDR — CrowdStrike / SentinelOne / Iru)
    - Email security (DMARC + SPF + DKIM)
    - Backups + tested restore (Recipe: business-continuity-disaster-recovery)
    - Patch cadence (≤ 30 days on critical CVEs)
    - Employee phishing training annual
    - Incident response plan (tabletop tested)
  enhances_quote:
    - SOC 2 Type II / ISO 27001
    - Pen test annual
    - Bug bounty program
    - Data classification policy
    - Zero-trust networking (Tailscale / Cloudflare Zero Trust)
```

### Recipe 6: Renewal calendar (60/30/14-day alerts)
```python
import datetime, requests, os
# Pull all policies from Notion DB, build renewal events
policies = requests.post(f"https://api.notion.com/v1/databases/<insurance-db>/query",
    headers={'Authorization': f"Bearer {os.environ['NOTION_TOKEN']}", 'Notion-Version':'2022-06-28','Content-Type':'application/json'},
    json={}).json()
for p in policies['results']:
    expiry = datetime.date.fromisoformat(p['properties']['Expiry']['date']['start'])
    name = p['properties']['Name']['title'][0]['plain_text']
    for days_out in [60, 30, 14]:
        trigger = expiry - datetime.timedelta(days=days_out)
        # POST to gcal
        # Action by tier: pull quotes, broker outreach, re-bind
```

### Recipe 7: Broker RFQ template (email)
```markdown
Subject: 2026 renewal — [Coverage] for [Co]

Hi [Broker],

We're approaching renewal for our [D&O / E&O / Cyber / EPLI] policy:
- **Current carrier:** [carrier]
- **Current limit:** $[X] per claim / $[Y] aggregate
- **Current premium:** $[Z]/yr
- **Current expiry:** [date]

Company snapshot for the application:
- ARR / revenue (TTM): $[X]
- Headcount: [N]
- Geographies: [list]
- Customers (with concentration if > 10%): [list]
- Material incidents past 12 months: [yes/no — details if yes]

We're shopping [3 markets]. Could you bind quotes from at least:
- [Carrier A]
- [Carrier B]
- [Carrier C]

Please send draft applications by [date]; we'll re-bind by [date - 7 days].

— [Name]
```

### Recipe 8: Certificates of Insurance (COI) bulk pull
```bash
# Customer often needs us to provide COI naming them as Additional Insured (AI)
# Newfront / Embroker self-service portal
curl -s -X POST "https://api.newfront.com/v1/coi/generate" \
  -H "Authorization: Bearer $NEWFRONT_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "policies":["GL","Cyber"],
    "additional_insured":"Customer Inc, 100 Main St, Anytown",
    "delivery_email":"customer-procurement@example.com"
  }'
```

### Recipe 9: D&O Side-A / B / C explainer for founders
```markdown
D&O Liability has 3 sides:
- **Side A:** Pays the INDIVIDUAL director/officer when company CAN'T indemnify (bankruptcy, derivative suit excluded from indemnification).
- **Side B:** Pays the COMPANY when it DOES indemnify directors/officers.
- **Side C:** Pays the COMPANY for securities claims against the company itself.

For pre-IPO companies:
- A + B is the standard policy.
- Side A excess often added at Series C+ (covers individuals beyond primary).
- Side C heavy at IPO and post-IPO (securities-claim exposure).
```

### Recipe 10: Workers' Comp class-code mapping
```yaml
# WC premium = payroll × class-code rate × experience modifier (mod)
common_class_codes:
  '8810': 'Clerical office'         # cheapest, typical SaaS HQ
  '8859': 'Computer programming'    # most engineering remote
  '8868': 'College / professional services'
  '5183': 'Plumbing'                # construction trades much higher
  '7380': 'Drivers / chauffeurs'    # ride-share / delivery higher
# Misclassification = audit penalty. Annual payroll audit reconciles.
```

## Examples

### Example 1: First insurance stack for a Seed-stage 12-person SaaS
**Goal:** Compliant + customer-ready stack in 3 weeks.
**Steps:**
1. Recipe 1: Seed must-have list.
2. Recipe 2: Vouch or Embroker for instant bundle quotes.
3. Recipe 5: prep Cyber underwriting evidence (MFA, EDR, backups).
4. Bind GL + Cyber + EPLI + WC; D&O after priced round.
5. Recipe 3: log each policy in Notion DB.
6. Recipe 6: renewal calendar.

**Result:** Compliant stack ~$8-15k/yr; ready for SOC 2 + enterprise customers.

### Example 2: D&O renewal at Series B
**Goal:** Bring premium down or expand limits.
**Steps:**
1. Recipe 6 fires 60 days out.
2. Recipe 7: RFQ to 3 brokers + 6 markets.
3. Compare quotes; identify retroactive date + exclusions deltas.
4. Bind better-of; cancel prior.
5. Recipe 3: update Notion + Drive.

**Result:** Market-priced D&O; better limits or premium.

### Example 3: Customer asks for COI naming them AI
**Goal:** 24-hr turn.
**Steps:**
1. Recipe 8: portal self-serve.
2. Email customer the COI.

**Result:** Sales unblocked.

## Edge cases / gotchas

- **Retroactive date.** D&O / E&O policies cover claims from work done back to retro date. Going to a new carrier with a later retro date = gap. Negotiate "prior acts" coverage.
- **Claims-made vs occurrence.** Most modern D&O / E&O / Cyber = claims-made (must report during policy period). Don't lapse coverage even briefly without "tail" (extended reporting endorsement).
- **Cyber war/state-actor exclusion.** Post Lloyd's 2023 rules, war exclusions broadened. Review attack-attribution clauses.
- **Ransomware sub-limits.** Many cyber policies cap ransomware payouts at 20-50% of policy limit. Confirm before counting on coverage.
- **EPLI in CA.** CA-specific high exposure (LWDA / PAGA); ensure EPLI carrier knows + prices accordingly. **Defer to `legal-counsel`.**
- **Customer-required indemnity caps.** MSA L of L cap should be ≥ insurance limit. Mismatch = uncovered exposure.
- **Misrepresentation on application.** Material misstatement → rescission. Have founder + CFO + counsel sign the app.
- **Side-A is for individuals.** Company can pay premium but proceeds protect the individual; ensure standard form not modified.
- **International coverage.** US policies often don't cover overseas claims. Add international package if employees / contracts abroad.
- **Cancellation notice (in-policy).** Carriers can cancel for non-payment with 10-15 days notice; for other reasons 60-90. Don't miss a payment.
- **Defer to `legal-counsel` for binding policy review, contract indemnification reconciliation, and incident-response coordination with carrier.**

## Sources

- Embroker — Startup Insurance Coverage: https://www.embroker.com/coverage/startup-insurance/
- Vouch — Startup Insurance Guide: https://www.vouch.us/blog/what-is-startup-business-insurance-and-why-do-i-need-it
- SVB — Startup Insurance Guide for Founders: https://www.svb.com/startup-insights/startup-strategy/startup-insurance-guide-for-founders/
- Newfront: https://newfront.com/
- Coalition (cyber): https://www.coalitioninc.com/
- At-Bay (cyber): https://www.at-bay.com/
- Founder Shield: https://foundershield.com/
- Lloyd's war exclusion update (2023): https://www.lloyds.com/news-and-insights/news/state-backed-cyber-attacks-exclusion-clauses
