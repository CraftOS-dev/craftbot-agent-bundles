<!--
Source: https://www.gartner.com/en/sales/topics/channel-sales + https://www.canalys.com/insights/channel-pricing
Channel margin tier matrix + deal-reg pricing uplift + floor pricing approval (June 2026 SOTA).
-->
# Channel Pricing + Discount Tier Design — SKILL

Build (and maintain) channel pricing: three-tier reseller margins (**Authorized / Silver / Gold**), deal-registration uplift (5-10 pts), MAP enforcement, floor-pricing approval matrix. Tiers gated by certifications + revenue commitment + customer-sat score. Pricing matrix in `xlsx`/`google-sheets`; tier-eligibility via CRM; discount-approval Slack flow; pricing exceptions defer to `finance-controller`.

## When to use

- **Designing or revising channel pricing** — annual or motion-change.
- **Tier-upgrade or downgrade** — partner crosses threshold; update tier.
- **Discount approval routing** — partner requests below-floor pricing.
- **MAP enforcement** — partner advertising below MAP; remediation.
- **Margin model for new SKU** — adding new product to channel.
- **Trigger phrases**: "channel pricing", "margin tier", "deal reg uplift", "MAP price", "discount approval", "floor pricing", "tier downgrade".

Do NOT use this skill for: **direct-sales pricing** (use `sales-agent`); **commission accounting** (defer to `finance-controller`); **MDF allocation** (use `mdf-allocation-tracking`); **deal-reg form workflow** (use `deal-registration-channel-conflict-resolution`).

## Setup

```bash
export MATON_API_KEY="<key>"             # for CRM tier lookups + Slack
# Pricing matrix in xlsx / google-sheets
# Tier-eligibility table maintained in postgresql-mcp warehouse
```

## Common recipes

### Recipe 1: Standard margin tier matrix (canonical)

```yaml
margin_tiers:
  authorized:
    margin_pct: 15
    deal_reg_uplift_pct: 0
    mdf_eligible: false
    requirements:
      - "Foundation cert: ≥ 1 contact"
      - "Signed reseller agreement"
      - "Customer-sat NPS ≥ 0 (neutral or better)"
  silver:
    margin_pct: 20
    deal_reg_uplift_pct: 5
    mdf_eligible: true
    mdf_per_quarter_cap: 20000
    requirements:
      - "Foundation cert: ≥ 3 contacts"
      - "Specialist cert: ≥ 1 contact"
      - "$100K trailing-12-month revenue"
      - "Customer-sat NPS ≥ 20"
  gold:
    margin_pct: 25
    deal_reg_uplift_pct: 10
    mdf_eligible: true
    mdf_per_quarter_cap: 75000
    co_sell_enabled: true
    requirements:
      - "Foundation cert: ≥ 5 contacts"
      - "Specialist cert: ≥ 3 contacts"
      - "Expert cert: ≥ 1 contact"
      - "$500K trailing-12-month revenue"
      - "Customer-sat NPS ≥ 40"
      - "Joint customer story OR Co-Sell Ready"
```

Tier benchmarks: Gartner channel research; Canalys 2025 channel margin study. 15/20/25% is the modern SaaS norm.

### Recipe 2: Pricing matrix (xlsx / google-sheets)

```yaml
# Master pricing sheet — one row per SKU × tier × deal-reg state
sku: "BRAND-PRO-USER-MO"
list_price_per_user_mo: 50
tiers:
  authorized:
    regular_partner_price: 42.50     # 15% margin → partner buys at $42.50, sells at $50
    deal_reg_partner_price: 42.50    # no uplift at Authorized tier
  silver:
    regular_partner_price: 40        # 20% margin
    deal_reg_partner_price: 37.50    # +5% uplift = 25% effective margin on registered deal
  gold:
    regular_partner_price: 37.50     # 25% margin
    deal_reg_partner_price: 32.50    # +10% uplift = 35% effective margin on registered deal

map_price: 47.50                     # Minimum Advertised Price = 95% of list

floor_thresholds:
  partner_self_authority: 47.50      # can quote down to MAP
  manager_approval: 42.50            # below MAP up to 15% off list — manager approval
  finance_escalation: 40             # below 20% off list — finance + VP approval
```

### Recipe 3: Tier eligibility query (warehouse)

```sql
-- Recalculate tier eligibility for all partners
WITH partner_certs AS (
  SELECT partner_id,
         COUNT(*) FILTER (WHERE level='foundation' AND status='active') AS foundation_count,
         COUNT(*) FILTER (WHERE level='specialist' AND status='active') AS specialist_count,
         COUNT(*) FILTER (WHERE level='expert' AND status='active') AS expert_count
  FROM partner_certifications
  GROUP BY partner_id
),
partner_revenue AS (
  SELECT partner_id, SUM(closed_won_amount) AS trailing_12m_revenue
  FROM partner_deals
  WHERE closed_at >= now() - interval '12 months'
  GROUP BY partner_id
),
partner_sat AS (
  SELECT partner_id, AVG(score) AS nps_score
  FROM partner_nps_responses
  WHERE responded_at >= now() - interval '12 months'
  GROUP BY partner_id
)
SELECT
  p.partner_id,
  p.partner_name,
  COALESCE(c.foundation_count, 0) AS f,
  COALESCE(c.specialist_count, 0) AS s,
  COALESCE(c.expert_count, 0) AS e,
  COALESCE(r.trailing_12m_revenue, 0) AS rev,
  COALESCE(n.nps_score, 0) AS nps,
  CASE
    WHEN COALESCE(c.expert_count,0) >= 1 AND COALESCE(c.specialist_count,0) >= 3
         AND COALESCE(c.foundation_count,0) >= 5
         AND COALESCE(r.trailing_12m_revenue,0) >= 500000
         AND COALESCE(n.nps_score,-100) >= 40 THEN 'gold'
    WHEN COALESCE(c.specialist_count,0) >= 1 AND COALESCE(c.foundation_count,0) >= 3
         AND COALESCE(r.trailing_12m_revenue,0) >= 100000
         AND COALESCE(n.nps_score,-100) >= 20 THEN 'silver'
    WHEN COALESCE(c.foundation_count,0) >= 1 THEN 'authorized'
    ELSE 'pending'
  END AS tier_eligible
FROM partners p
LEFT JOIN partner_certs c ON c.partner_id=p.partner_id
LEFT JOIN partner_revenue r ON r.partner_id=p.partner_id
LEFT JOIN partner_sat n ON n.partner_id=p.partner_id;
```

Run quarterly; surface to BD lead for tier-change decisions.

### Recipe 4: Tier change communication

```bash
# Quarterly tier-change letter — congratulate upgrades; coach for downgrades
cat <<'EOF'
Subject: Q3 Tier Review — Congratulations: Silver → Gold

Hi Sarah,

Your trailing-12-month review:
- Revenue: $620K (above $500K Gold threshold)
- Certs: 6 Foundation, 4 Specialist, 1 Expert (all thresholds met)
- NPS: 47 (above Gold threshold of 40)

Effective Aug 1, 2026, Acme Solutions moves to GOLD tier.

What changes:
- Margin: 20% → 25%
- Deal-reg uplift: 5% → 10% on registered deals
- MDF cap: $20K/qtr → $75K/qtr
- Co-Sell program access unlocked

Action: re-sign Schedule A of MSA (PandaDoc link).

— Pat (Partnerships Lead)
EOF
```

For downgrades: same letter, gentler tone, with specific remediation path back.

### Recipe 5: Floor pricing approval workflow (Slack)

```bash
# When partner requests below-MAP pricing
DEAL_AMOUNT=85000
DISCOUNT_PCT=18      # > 15% but < 20%, manager approval level

curl -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $SLACK_TOKEN" -H "Content-Type: application/json" \
  -d "{
    \"channel\": \"#pricing-approval-managers\",
    \"text\": \":bell: Discount request — 18% off list — Acme Solutions × Globex Corp deal\",
    \"blocks\": [
      {\"type\":\"section\",\"text\":{\"type\":\"mrkdwn\",\"text\":\"*Discount request* — 18% off list (above 15% threshold)\nPartner: Acme Solutions (Gold)\nEnd-customer: Globex Corp\nDeal: \$$DEAL_AMOUNT\nRequested price: \$40/user/mo (list \$50)\nJustification: Globex competing offer at \$38 from Brand competitor\nDeal-reg status: registered Aug 5\"}},
      {\"type\":\"actions\",\"elements\":[
        {\"type\":\"button\",\"text\":{\"type\":\"plain_text\",\"text\":\"Approve 18%\"},\"value\":\"approve-18\"},
        {\"type\":\"button\",\"text\":{\"type\":\"plain_text\",\"text\":\"Counter 15%\"},\"value\":\"counter-15\"},
        {\"type\":\"button\",\"text\":{\"type\":\"plain_text\",\"text\":\"Escalate Finance\"},\"value\":\"escalate-finance\"}
      ]}
    ]
  }"
```

Approver clicks → webhook updates deal record + notifies partner.

### Recipe 6: Discount approval matrix

```yaml
discount_approval:
  partner_self_authority:
    threshold: "0-5% off list"
    note: "Standard volume / start-date / annual-prepay flex"
  manager_approval:
    threshold: "5-15% off list"
    approver: "BD Manager"
    sla: "8 business hours"
    required_inputs: ["competitive justification","deal size","partner tier"]
  director_approval:
    threshold: "15-20% off list"
    approver: "BD Director"
    sla: "1 business day"
    required_inputs: ["above + customer-side BANT confirmation"]
  finance_escalation:
    threshold: "> 20% off list OR < cost"
    approver: "VP Partnerships + CFO"
    sla: "2 business days"
    required_inputs: ["above + 3-yr LTV projection + churn risk"]
  exception_reasons_allowed:
    - "Strategic logo win"
    - "Multi-year prepay (≥ 3-yr)"
    - "Reference customer with case study commitment"
    - "Specific competitive deflection (must name competitor)"
```

### Recipe 7: MAP (Minimum Advertised Price) enforcement

```yaml
map_policy:
  definition: "Partner may not advertise below MAP ($47.50/user/mo) in any public channel without written approval"
  monitoring:
    - "Quarterly scrape of partner websites (playwright-mcp + brave-search)"
    - "Slack alerts on detected violations"
  remediation:
    first_offense: "Written warning; 7 days to comply"
    second_offense: "Loss of deal-reg uplift for 1 quarter"
    third_offense: "Tier downgrade; possible termination"
  exclusions:
    - "Private quotes to customers (not public advertising)"
    - "End-of-life SKU clearance with written approval"
    - "Bundle pricing where line-item attribution is unclear"
```

### Recipe 8: MAP violation scan (Playwright)

```python
# Quarterly scan partner sites
import asyncio
from playwright.async_api import async_playwright

PARTNERS = [
    {"name": "Acme Solutions", "url": "https://acme.com/products/brand-reseller"},
    # ...
]

async def scan(p_browser, partner):
    page = await p_browser.new_page()
    await page.goto(partner["url"])
    text = await page.inner_text("body")
    # Look for any "/user/mo" pricing
    import re
    matches = re.findall(r'\$([\d,]+(?:\.\d+)?)\s*(?:per|/)\s*user', text)
    for m in matches:
        price = float(m.replace(",", ""))
        if price < 47.50:  # MAP
            print(f"VIOLATION: {partner['name']} advertising ${price} on {partner['url']}")
    await page.close()

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for partner in PARTNERS:
            await scan(b, partner)
        await b.close()
```

Run quarterly; alert via `slack-mcp`.

### Recipe 9: Pricing matrix update (annual)

```yaml
annual_pricing_review:
  inputs:
    - "List price changes (from product team)"
    - "Margin benchmarks (Canalys / Gartner channel research)"
    - "Competitive margin moves (annual industry scan)"
    - "Partner feedback (PAB + Partner NPS open responses)"
  outputs:
    - "Updated tier-margin matrix (xlsx)"
    - "Updated MAP per SKU"
    - "Communication letter to all active partners (PandaDoc bulk)"
    - "Updated reseller-agreement Schedule A (PandaDoc templates)"
  cadence: "October each year; effective Jan 1"
  approval: "VP Partnerships + CFO"
```

### Recipe 10: Effective margin calculator (for internal use)

```python
def effective_margin(list_price, partner_buy_price, deal_reg=False, deal_reg_uplift_pct=0):
    """
    Given list, partner buy, and deal-reg flag → effective margin.
    """
    if deal_reg:
        effective_buy = partner_buy_price * (1 - deal_reg_uplift_pct / 100)
    else:
        effective_buy = partner_buy_price
    margin = (list_price - effective_buy) / list_price * 100
    return round(margin, 1)

# Example
print(effective_margin(50, 37.50, deal_reg=True, deal_reg_uplift_pct=10))
# → 35.0 (Gold tier registered deal: 25% base + 10% uplift)
```

### Recipe 11: CRM tier-field update

```bash
# After Recipe 3 query, update partner records
curl -X PATCH "https://gateway.maton.ai/hubspot/crm/v3/objects/companies/<partner-id>" \
  -H "Authorization: Bearer $MATON_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "partner_tier": "gold",
      "partner_tier_effective_date": "2026-08-01",
      "partner_margin_pct": "25",
      "partner_deal_reg_uplift_pct": "10",
      "partner_mdf_quarterly_cap": "75000"
    }
  }'
```

Sales reps see partner tier on the deal record; quotes auto-populate at correct partner price.

### Recipe 12: Pricing FAQ (for partner portal)

```yaml
pricing_faq:
  q_how_is_margin_calculated:
    a: "Margin = (List Price - Partner Buy Price) / List Price. Tier sets the partner buy price; deal-reg adds uplift."
  q_can_i_discount_below_map:
    a: "Public advertising: no, requires written approval. Private quotes: see discount approval matrix; partner self-authority up to 5%."
  q_when_does_tier_change:
    a: "Quarterly review. Eligibility recalculated each quarter end; new tier effective first of following month."
  q_what_if_i_lose_certs:
    a: "Loss of cert puts you in remediation; tier reduced after one quarter. Renewal restores tier next review."
  q_mdf_vs_margin:
    a: "MDF is co-marketing budget against approved activities. Margin is your purchase discount. Separate. You can claim both on the same deal."
  q_co_sell:
    a: "Gold tier only. Co-Sell program assigns a vendor AE to joint deals; vendor commits to participate."
```

## Examples

### Example 1: Quarterly tier review + upgrade

**Goal:** Q3 tier review; identify and upgrade qualifying partners.

**Steps:**
1. Recipe 3 — Warehouse query identifies 4 partners now Silver-eligible, 2 now Gold-eligible.
2. Recipe 4 — Communication letters drafted for each (PandaDoc bulk).
3. Schedule A amendments via `referral-affiliate-channel-oem-agreement-structuring` for re-sign.
4. Recipe 11 — CRM tier fields updated.
5. New pricing flows to next-quarter quotes.

**Result:** Partners upgraded systematically; pricing aligned to performance.

### Example 2: Below-floor discount request

**Goal:** Gold partner requests 22% off for competitive deflection; needs finance escalation.

**Steps:**
1. Partner emails BD with discount request.
2. Recipe 5 routes to `#pricing-approval-finance` Slack with deal details.
3. Recipe 6 — Above 20% → finance + VP review required.
4. BD director checks competitive justification; CFO checks margin impact + LTV.
5. Approved at 20% (not 22%) with 3-year commit; communicated to partner.
6. Deal closes; metadata logged for next-quarter pricing-trend review.

**Result:** Discipline maintained; competitive deal won; data captured for trend.

### Example 3: MAP violation enforcement

**Goal:** Scan finds Silver partner advertising $35/user/mo (below $47.50 MAP).

**Steps:**
1. Recipe 8 scan flags violation.
2. Recipe 7 first-offense: written warning email; 7-day compliance window.
3. Partner removes pricing from public site within 5 days.
4. Re-scan confirms; case closed.
5. Logged in partner record for future reference.

**Result:** MAP discipline; no escalation needed.

## Edge cases / gotchas

- **Tier downgrade is politically hard** — partner that lost an Expert (turnover) drops Silver eligibility. Provide grace period (1 quarter) before official downgrade.
- **Deal-reg uplift stacking** — partner may try to combine multiple uplifts (deal-reg + strategic-account + product-launch). Limit to one stack per deal.
- **MAP vs MRP** — MAP = Minimum *Advertised* Price (public listing). MRP = Manufacturer's Recommended Price. Different concepts; use MAP for channel.
- **Bundle pricing** muddles attribution — if SKU-A discount is 30% but bundle SKU-A+B is 18%, which is "the deal"? Use total bundle price for MAP comparison.
- **Multi-year prepay discounts** are NOT discounts off MAP; they're term-multiplier discounts. Track separately.
- **Promotional / seasonal pricing** — vendor-led promos override MAP temporarily; communicate clearly with start/end dates.
- **Currency** — list price in USD; partner currencies follow daily FX. Periodically refresh local MAPs; FX swings of >10% trigger interim updates.
- **Stacked margins** — partner that sells via another reseller (sub-reseller) — multi-tier channels need separate margin model. Out of scope; defer to channel architecture review.
- **Cost-plus pricing** — for some enterprise deals, customer demands "cost + 15%"; the cost is your channel partner buy price. Reveals partner buy; only allow with NDA.
- **Tier ratchets up but not down** — some programs make tier downgrades hard. Be deliberate; recommendation: ratchet down after 2 consecutive quarters below threshold (not 1).
- **NPS as tier criteria** is reasonable but noisy — small response counts inflate variance. Require ≥ 5 responses for NPS to count.
- **Pricing exception "specific competitive deflection (must name competitor)"** — over time you'll see partners always cite the same competitor. Validate with sales-agent.
- **Co-sell access** is Gold-only in most modern programs — opening to Silver dilutes co-sell investment.
- **Cross-region channel arbitrage** — partner in low-cost region buys at local price, sells in high-cost region. Address with territory carve-outs in agreement.
- **Pricing matrix versioning** — annual revision; partners on prior-year terms grandfathered until contract renewal. Version every xlsx; archive in `notion-mcp`.
- **Pricing communication is a relationship event** — tier change emails are read carefully. Tone matters; lead with appreciation; data second; action last.
- **MAP is not a price floor for the END customer**; partner can sell at lower price privately. MAP governs PUBLIC ADVERTISING.

## Sources

- Gartner channel sales: https://www.gartner.com/en/sales/topics/channel-sales
- Canalys channel pricing benchmarks: https://www.canalys.com/insights/channel-pricing
- Forrester partner programs: https://www.forrester.com/research/partner-ecosystems/
- Partnerstack tier-design: https://partnerstack.com/blog/partner-tiers
- Channel margin benchmarks: https://www.canalys.com/insights/
- MAP policy legal guidance (US): https://www.ftc.gov/business-guidance/resources/online-resale-price-maintenance
- HubSpot PRM tier tracking: https://developers.hubspot.com/docs/api/crm/companies
