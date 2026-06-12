<!--
Sources: https://ramp.com/blog/navan-vs-brex-vs-ramp
         https://www.brex.com/journal/press/brex-pay-for-navan
         https://receiptor.ai/blog/brex-alternatives-after-the-capital-one-acquisition-2026
Brex acquired by Capital One April 2026 ($5.15B). BrexPay for Navan since Oct 2024.
Navan AI assistant Ava + Expense Chat 94/100 CSAT beta; 70%+ corp-card txns zero manual.
Ramp = control-first; AI duplicate/anomaly flagging.
-->
# Travel + Expense Policy — Navan / Ramp / Brex — SKILL

Author T&E policy, configure corporate cards (Ramp / Brex / Navan Connect), set up travel booking (Navan / Ramp Travel / SAP Concur), automate expense reconciliation, route approvals. Brex acquired by Capital One April 2026 ($5.15B); BrexPay for Navan is the integrated travel+card stack since Oct 2024.

## When to use

- New corporate card rollout.
- Replacing manual expense reports with auto-reconciliation.
- Standing up travel booking with policy guardrails.
- Annual policy refresh.
- Trigger phrases: "T&E", "expense policy", "corp card", "card limits", "Ramp", "Brex", "Navan", "Expensify", "Concur", "receipts", "per diem", "travel booking".

## Setup

```bash
export RAMP_TOKEN="xxx"            # https://docs.ramp.com — Developer API
export BREX_TOKEN="xxx"            # https://developer.brex.com (post-Capital One; verify endpoints)
export NAVAN_TOKEN="xxx"           # https://docs.navan.com
export EXPENSIFY_TOKEN="xxx"
export CONCUR_TOKEN="xxx"
```

## Common recipes

### Recipe 1: Stage / org platform selection
```yaml
choose:
  control_first_modern_spend:
    primary: Ramp
    why: Customizable card limits + automated policy enforcement + AI duplicate flagging
  multi_entity_50_countries:
    primary: Brex
    why: Multi-entity / 50+ countries (Cap One owned post-Apr 2026; product evolving)
  travel_heavy_with_corp_card:
    primary: BrexPay for Navan
    why: Per-booking virtual cards + reconciliation across 50+ currencies; Ava AI assistant
  use_existing_bank_cards:
    primary: Navan Connect
    why: Links existing bank cards into Navan; no card replacement
  smb_expense_only:
    primary: Expensify
    why: SmartScan + integrations; SmartScan free for individuals
  enterprise:
    primary: SAP Concur
    why: Heaviest enterprise expense + travel
  eu:
    primary: Pleo or Spendesk
    why: EU-native; SCA/PSD2 native
```

### Recipe 2: T&E policy template
```markdown
# Travel + Expense Policy — [Co]

## Principles
- **Spend like it's your money. Travel like you have a flight tomorrow.**
- Default to lowest-reasonable; book early; refund unused.
- Receipts required for ≥ $25 OR per state law (NJ $1+).

## Card policy
- **Daily limit:** $1,000 default.
- **Monthly limit:** $5,000 default; manager can request increase.
- **MCC restrictions:** Cash advance, crypto, gambling — blocked.
- **Personal use:** Strictly prohibited (Ramp/Brex auto-flag).
- **Lost/stolen:** report within 24h via [app]; new card issued.

## Travel
- **Air:** Economy on flights < 5h; economy plus on 5-8h; business class on > 8h (one-way).
- **Hotel:** ≤ city-specific cap; mid-tier business hotels (Hyatt House / Marriott Courtyard tier).
- **Ground:** Uber/Lyft taxi tier preferred; ride-share over rental for < 3 days.
- **Meals while traveling:** $75/day per diem; or itemized actual.
- **Booking:** Through Navan / Ramp Travel; off-policy requires manager pre-approval.

## Per-city hotel caps (USD per night, mid-tier business)
| City        | Cap |
|-------------|-----|
| NYC         | 450 |
| SF / Bay    | 425 |
| London      | 425 |
| Tokyo       | 400 |
| Paris       | 400 |
| LA          | 350 |
| Boston      | 350 |
| DC          | 350 |
| Berlin      | 300 |
| Tier-2 US   | 275 |
| Other intl  | 300 |

## Meals — non-travel
- **Team meals:** $30 / person, $300 cap.
- **Client meals:** $100 / person.
- **Solo working meals:** prohibited (no expensing of solo lunches in own city).

## Approval thresholds
| Amount   | Approver                |
|----------|-------------------------|
| ≤ $250   | Auto                    |
| ≤ $1,000 | Direct manager          |
| ≤ $5,000 | Manager + finance lead  |
| > $5,000 | Manager + finance + CFO |

## Reimbursements
- Submit via [tool] within 30 days; expenses > 60 days denied.
- Paid on next pay cycle.

## Receipts
- Required for ≥ $25 (federal best practice).
- Card auto-pull preferred; manual scan via app.
- For meals: include attendees + business reason.

> **Defer to `legal-counsel` for binding interpretation of state-specific reimbursement law (CA Labor Code §2802 reimbursement obligations).**
```

### Recipe 3: Ramp — issue card with limits + policy
```bash
curl -s -X POST "https://api.ramp.com/developer/v1/cards" \
  -H "Authorization: Bearer $RAMP_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "display_name":"Avery Lee Corp",
    "user_id":"<user>",
    "spending_restrictions":{
      "interval":"MONTHLY",
      "limit_amount_cents":500000,
      "blocked_categories":["cash_advance","gambling","crypto"],
      "allowed_vendors":[],
      "limits":[
        {"interval":"DAILY","amount_cents":100000}
      ]
    }
  }'
```

### Recipe 4: Ramp — travel booking limit (Ramp Travel)
```bash
# Auto-bind T&E policy to traveler
curl -s -X POST "https://api.ramp.com/developer/v1/travel/policies" \
  -H "Authorization: Bearer $RAMP_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "name":"Standard traveler",
    "users":["<user>"],
    "flight":{"max_class_short_haul":"economy","max_class_long_haul":"business","over_8h_threshold":true},
    "hotel":{"city_caps":{"NYC":450,"SF":425,"LON":425}},
    "ground":{"rideshare_allowed":true,"car_rental":"under_3_days_only"}
  }'
```

### Recipe 5: Navan booking via API
```bash
curl -s -X POST "https://api.navan.com/v1/bookings" \
  -H "Authorization: Bearer $NAVAN_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "user_id":"<user>",
    "trip_type":"round_trip",
    "origin":"JFK","destination":"LHR",
    "depart":"2026-09-10T18:00",
    "return":"2026-09-15T08:00",
    "cabin":"business",
    "hotel":{"city":"London","nights":5,"max_per_night_USD":425}
  }'
```

### Recipe 6: Auto-reconciliation — Ramp transaction → category mapping
```python
# Map MCC to GL account; auto-categorize
MCC_TO_GL = {
    '5812':'6100-Meals & Entertainment',
    '4111':'6200-Travel-Ground',
    '4511':'6210-Travel-Air',
    '7011':'6220-Travel-Hotel',
    '5942':'6300-Office Supplies',
    '4814':'6400-Telecom',
    '5734':'6500-Software',
}
def categorize(tx):
    return MCC_TO_GL.get(tx['mcc'], '6900-Other')
```

### Recipe 7: Receipt auto-pull (gmail-mcp)
```bash
# Forward receipts to Ramp via dedicated email; or use Gmail mcp to pull
# Ramp dedicated email: receipts@ramp.com (auto-matches to txn)
# For non-Ramp, route via gmail-mcp filter:
curl -s -X POST "https://gmail.googleapis.com/gmail/v1/users/me/settings/filters" \
  -H "Authorization: Bearer $GMAIL_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "criteria":{"from":"receipts@","subject":"receipt"},
    "action":{"addLabelIds":["Label_Receipts"],"forward":"receipts@expense-tool.com"}
  }'
```

### Recipe 8: Policy violation alert
```bash
# Ramp webhook on policy violation
curl -s -X POST "https://api.ramp.com/developer/v1/webhooks" \
  -H "Authorization: Bearer $RAMP_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "url":"https://hooks.example.com/ramp-policy-violation",
    "events":["transaction.policy.violation"]
  }'
# Endpoint posts to Slack #ops-finance
```

### Recipe 9: Monthly close — export to Xero/QBO
```bash
# Ramp → Xero monthly sync
curl -s -X POST "https://api.ramp.com/developer/v1/accounting/sync" \
  -H "Authorization: Bearer $RAMP_TOKEN" -H "Content-Type: application/json" \
  -d '{"target":"xero","period":"2026-06"}'
```

### Recipe 10: Per diem + foreign currency handling
```python
# Per-day cap in local currency converted at OECD rate
import requests
FX = requests.get('https://api.exchangerate.host/latest?base=USD').json()['rates']
def per_diem(city, days, local_ccy):
    cap_usd = 75  # default; adjust per HMRC scale rates / GSA M&IE
    return round(cap_usd * days / FX[local_ccy], 2)
```

### Recipe 11: Brex card admin (verify endpoints post-Capital One April 2026)
```bash
# Verify base path; the platform has been migrating post-acquisition
curl -s "https://platform.brexapis.com/v1/cards" \
  -H "Authorization: Bearer $BREX_TOKEN" \
  | jq '.[] | {id, last_four, holder, limit, status}'
```

## Examples

### Example 1: Roll out Ramp cards to 30-person team
**Goal:** Replace personal-card-and-reimburse with corp cards in 2 weeks.
**Steps:**
1. Recipe 2: write T&E policy; publish in handbook.
2. Recipe 3: issue cards via API with limits per role.
3. Recipe 4: Ramp Travel policy.
4. Recipe 7: receipt auto-pull setup.
5. Recipe 8: violation alerts → #ops-finance.
6. Recipe 9: monthly Xero sync.
7. Trainual training on policy + card use.

**Result:** Auto-categorized close; receipts inline; ops handles 90% close in 4 hours.

### Example 2: Navan + Brex (BrexPay) for travel-heavy sales team
**Goal:** Per-booking virtual card + automated reconciliation in 50 currencies.
**Steps:**
1. Recipe 5: Navan booking with cabin / hotel limits.
2. BrexPay for Navan auto-issues per-trip virtual card.
3. Recipe 6: auto-categorize.
4. Recipe 8: off-policy bookings flagged.

**Result:** Sales books own travel within guardrails; finance reconciles automatically.

### Example 3: Annual policy review
**Goal:** Refresh caps + per-city tiers for 2027.
**Steps:**
1. Pull current spend by city + traveler.
2. Compare to GSA M&IE + HMRC + benchmark cap.
3. Adjust Recipe 2 caps.
4. Re-publish to handbook; Recipe 4 updates Ramp policy.

**Result:** Caps reflect market; no policy drift.

## Edge cases / gotchas

- **CA Labor Code §2802 reimbursement.** California requires reasonable business expense reimbursement; restrictive caps can be challenged. **Defer to `legal-counsel`.**
- **Brex transition.** Capital One acquired April 2026 ($5.15B). API endpoints + product surface evolving through 2026-2027. Verify before automating critical flows.
- **Per diem vs actual.** Both legal under IRS, but mix-and-match (per diem some days, actual others) draws audit attention. Pick one.
- **Foreign card surcharge.** 1.5-3% on non-US cards in foreign currency unless using Navan/Ramp multi-currency. Audit FX line on close.
- **Lost-receipt declarations.** ≥ $75 requires written attestation per IRS Pub 463. Build "lost receipt" form in expense tool.
- **Owner draws on corp card.** S-corp / LLC owners using corp card for personal = constructive distribution / accountable-plan failure. Hard line, audit annually.
- **Crypto / wallet-loaded cards.** Block via Recipe 3 `blocked_categories`. Compliance + tax mess.
- **Sales-tax recovery (EU VAT).** Recipe 6 should preserve VAT detail for recovery; Navan + Pleo + Spendesk auto-extract.
- **Travel + immigration.** Some countries require business visas for "business trips" of certain length. Don't book without checking. **Defer to `legal-counsel` + immigration advisor.**
- **Non-employee travel.** Candidates' onsite travel — book under a "guest traveler" account; don't issue them a corp card.
- **Auto-flag duplicate transactions.** Ramp + Navan AI flag duplicates; close team should still spot-check monthly.

## Sources

- Ramp — Navan vs Brex vs Ramp: https://ramp.com/blog/navan-vs-brex-vs-ramp
- Brex — BrexPay for Navan: https://www.brex.com/journal/press/brex-pay-for-navan
- Receiptor — Brex Alternatives After Capital One 2026: https://receiptor.ai/blog/brex-alternatives-after-the-capital-one-acquisition-2026
- Navan blog — best travel analytics tools: https://navan.com/blog/best-travel-analytics-tools-ai
- Ramp Developer API: https://docs.ramp.com/
- Navan docs: https://docs.navan.com/
- Brex Developer Portal: https://developer.brex.com/
- IRS Pub 463 (Travel & Expense): https://www.irs.gov/publications/p463
- CA Labor Code §2802: https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=2802&lawCode=LAB
