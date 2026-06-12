---
name: dynamic-pricing-variable-insertion
description: Insert dynamic pricing tables, variable line items, discount logic, optional / required items, and per-row formulas into proposals and contracts — PandaDoc pricing tables, Proposify quote builder, Qwilr interactive blocks, or custom Jinja2/Mustache + WeasyPrint pipelines. Use when the user says "dynamic pricing", "line-item loop", "pricing table", "optional add-ons", "discount logic", "per-tier pricing", "variable insertion in proposal".
---

# Dynamic pricing + variable insertion — PandaDoc / Proposify / Qwilr / custom

This skill ships the pricing engine layer for proposals + quotes. It handles the math (totals, taxes, discounts), the optional/required logic (add-on selection), and the template injection.

## When to use

User says:

- "Add a pricing table to this proposal"
- "Optional add-ons the buyer can toggle"
- "Tiered discount based on volume"
- "Quote with discounts off list"
- "PandaDoc pricing table API"
- "Loop line items into the doc"
- "CPQ-driven pricing → doc"

Companion skills:
- `proposal-automation-pandadoc-proposify-qwilr` — host platform.
- `salesforce-conga-composer` — CPQ-driven pricing input.
- `hubspot-doc-gen` — HubSpot Quotes / line items source.
- `bulk-document-gen-csv` — batch pricing-driven runs.

## Setup

```bash
# PandaDoc REST
# Required env: PANDADOC_API_KEY

# Proposify REST
# Required env: PROPOSIFY_API_KEY

# Qwilr API
# Required env: QWILR_API_KEY

# Custom rendering
pip install jinja2 weasyprint
# or
npm install handlebars puppeteer
```

## Common recipes

### Recipe 1: Pick the pricing approach

| Approach | When to use | Notes |
|---|---|---|
| PandaDoc pricing tables | Standard proposals; broad sales | Built-in totals + optional items + discount UI |
| Proposify quote builder | Agency proposals | Section-based with package selection |
| Qwilr interactive blocks | Modern web-style proposals | Toggle add-ons; live total |
| Salesforce CPQ Quote | Salesforce-resident | Catalog + price rules in SF |
| HubSpot Quotes line items | HubSpot-resident | Product library + line items |
| Custom Jinja2 + WeasyPrint | Edge cases / no SaaS budget | Full control; more dev work |

### Recipe 2: PandaDoc — pricing table on document create

```python
import requests

requests.post(
    "https://api.pandadoc.com/public/v1/documents",
    headers={"Authorization": f"API-Key {PANDADOC_KEY}"},
    json={
        "name": "Proposal - Acme",
        "template_uuid": TEMPLATE_UUID,
        "recipients": [{"email":"buyer@acme.com","first_name":"Jane","last_name":"Smith","role":"client"}],
        "pricing_tables": [{
            "name": "Pricing",
            "data_merge": False,
            "options": {"currency": "USD"},
            "sections": [{
                "title": "Subscription (required)",
                "default": True,
                "multichoice_enabled": False,
                "rows": [
                    {"options":{"qty_editable": False, "optional": False},
                     "data":{"name":"Pro Plan","description":"Up to 50 users","price":2000,"qty":12}},
                ]
            },{
                "title": "Optional add-ons",
                "multichoice_enabled": True,
                "rows": [
                    {"options":{"qty_editable": True, "optional": True, "optional_selected": False},
                     "data":{"name":"Premium Support","description":"24/7 dedicated CSM","price":500,"qty":12}},
                    {"options":{"qty_editable": False, "optional": True, "optional_selected": False},
                     "data":{"name":"SSO Add-on","description":"SAML / OIDC","price":1000,"qty":1}}
                ]
            }]
        }]
    }
)
```

Required fields: `name`, `qty`, `price` per row. Optional: `description`, `tax`, `discount`.

### Recipe 3: PandaDoc — discount logic per-row

```python
# Per-row discount
{"options":{"optional": False},
 "data":{
    "name":"Annual Subscription","price":24000,"qty":1,
    "discount":{"name":"Loyalty","type":"percent","value":15}    # 15% off
 }}
```

Discount types: `percent` or `amount`. For sticky-volume tiers, compute in script before POST.

### Recipe 4: PandaDoc — tax per-row

```python
{"data":{
    "name":"Hardware","price":5000,"qty":2,
    "tax":{"name":"Sales Tax","type":"percent","value":8.875}    # NYC sales tax
}}
```

### Recipe 5: PandaDoc — token replacement for non-pricing variables

```python
# In addition to pricing_tables, scalar tokens
{
  "tokens": [
    {"name":"customer.legal_name","value":"Acme Corp"},
    {"name":"customer.state","value":"Delaware"},
    {"name":"term.months","value":"36"},
    {"name":"effective_date","value":"2026-07-01"}
  ]
}
```

In template: `[Customer.Legal_Name]`, `[Customer.State]`, etc. Tokens are case-sensitive.

### Recipe 6: Volume-tier discount engine (Python pre-POST)

```python
def apply_volume_discount(rows):
    total_units = sum(r["data"]["qty"] for r in rows)
    if total_units >= 500:
        pct = 25
    elif total_units >= 100:
        pct = 15
    elif total_units >= 25:
        pct = 5
    else:
        pct = 0
    for r in rows:
        if pct:
            r["data"]["discount"] = {"name": f"Volume {pct}%", "type":"percent", "value": pct}
    return rows
```

Apply before Recipe 2 POST.

### Recipe 7: Proposify quote section

```bash
# Update a section with a pricing table inside an existing draft
curl -X PUT https://app.proposify.com/api/v3/proposals/$PROP_ID/sections/$SECTION_ID \
  -H "Authorization: Bearer $PROPOSIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "fees":[
      {"label":"Setup","price":2500,"quantity":1,"type":"one_time"},
      {"label":"Monthly subscription","price":1500,"quantity":12,"type":"recurring"}
    ]
  }'
```

### Recipe 8: Qwilr block — interactive pricing block

```bash
curl -X POST https://api.qwilr.com/v1/pages \
  -H "Authorization: Bearer $QWILR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Acme Proposal",
    "templateId": "tmpl_...",
    "tokens": {
      "customer_name": "Acme Corp"
    },
    "pricingBlocks": [{
      "title": "Choose your plan",
      "type": "tabbed",
      "tabs": [
        {"name":"Pro","items":[{"name":"Pro Plan","price":2000,"qty":12,"qtyEditable":true}]},
        {"name":"Enterprise","items":[{"name":"Enterprise","price":5000,"qty":12}]}
      ]
    }]
  }'
```

### Recipe 9: Custom Jinja2 + WeasyPrint pipeline

```python
from jinja2 import Template
from weasyprint import HTML

PROPOSAL_HTML = """
<html><body>
  <h1>Proposal for {{ customer.name }}</h1>
  <table>
    <tr><th>Item</th><th>Qty</th><th>Unit</th><th>Total</th></tr>
    {% for li in line_items %}
    <tr>
      <td>{{ li.name }}</td>
      <td>{{ li.qty }}</td>
      <td>${{ "%.2f"|format(li.price) }}</td>
      <td>${{ "%.2f"|format(li.qty * li.price) }}</td>
    </tr>
    {% endfor %}
    <tr><td colspan="3"><b>Subtotal</b></td><td><b>${{ "%.2f"|format(subtotal) }}</b></td></tr>
    {% if discount_pct %}
    <tr><td colspan="3">Discount ({{ discount_pct }}%)</td><td>-${{ "%.2f"|format(discount_amt) }}</td></tr>
    {% endif %}
    <tr><td colspan="3"><b>Total</b></td><td><b>${{ "%.2f"|format(total) }}</b></td></tr>
  </table>
</body></html>
"""

def render(customer, line_items, discount_pct=0):
    subtotal = sum(li["qty"] * li["price"] for li in line_items)
    discount_amt = subtotal * discount_pct / 100
    total = subtotal - discount_amt
    html = Template(PROPOSAL_HTML).render(
        customer=customer, line_items=line_items,
        subtotal=subtotal, discount_pct=discount_pct,
        discount_amt=discount_amt, total=total
    )
    HTML(string=html).write_pdf(f"proposals/{customer['name']}.pdf")

render(
    customer={"name":"Acme Corp"},
    line_items=[
        {"name":"Pro Plan","qty":12,"price":2000},
        {"name":"SSO","qty":1,"price":1000}
    ],
    discount_pct=15
)
```

### Recipe 10: docxtpl line-item loop (Word output)

```python
from docxtpl import DocxTemplate

doc = DocxTemplate("templates/msa-pricing.docx")
doc.render({
    "customer_name": "Acme",
    "line_items": [
        {"name":"Pro","qty":12,"price":2000,"total":24000},
        {"name":"SSO","qty":1,"price":1000,"total":1000}
    ],
    "subtotal": 25000,
    "discount_pct": 15,
    "total": 21250
})
doc.save("dist/msa-acme.docx")
```

Inside template:

```text
{%tr for li in line_items %}
| {{ li.name }} | {{ li.qty }} | ${{ li.price }} | ${{ li.total }} |
{%tr endfor %}
```

### Recipe 11: Currency localization + rounding

```python
import babel.numbers
total_usd = 21250.00
print(babel.numbers.format_currency(total_usd, "USD", locale="en_US"))   # $21,250.00
print(babel.numbers.format_currency(21250, "EUR", locale="de_DE"))        # 21.250,00 €
print(babel.numbers.format_currency(21250, "JPY", locale="ja_JP"))        # ￥21,250
```

Always use `Decimal` not `float` for money; round per locale (JPY = 0 decimals; USD/EUR = 2).

### Recipe 12: Stripe price ID → pricing table

```python
# Pull live Stripe prices to keep proposal in sync
import stripe
stripe.api_key = os.environ["STRIPE_SECRET"]

p = stripe.Price.retrieve("price_1OabcXX")
unit_amount_dollars = p.unit_amount / 100   # cents to dollars
pricing_row = {"data":{"name": p.nickname or p.id, "price": unit_amount_dollars, "qty": 12}}
```

### Recipe 13: CPQ output → proposal pricing rows (Salesforce CPQ)

```python
# QuoteLineItem from Salesforce CPQ
ql_items = sf.query("""
  SELECT Product2.Name, Quantity, UnitPrice, Discount, ListPrice, NetPrice
  FROM QuoteLineItem WHERE QuoteId = 'a0Q...'
""")
rows = []
for li in ql_items["records"]:
    rows.append({
        "data": {
            "name": li["Product2"]["Name"],
            "qty": li["Quantity"],
            "price": li["UnitPrice"],
            "discount": {"type":"amount","value": li["Discount"]} if li["Discount"] else None
        }
    })
# Then Recipe 2 POST
```

## Examples

### Example 1: Subscription proposal with tiered volume discount

**Goal:** Quote 60 seats with auto-applied 15% volume discount.
**Steps:**
1. Recipe 6 — compute discount tier (60 → 15%).
2. Recipe 3 — apply per-row in pricing table.
3. Recipe 2 — POST PandaDoc.
4. Recipe 5 — also fill scalar tokens (customer name, dates).

**Result:** Pricing math correct + buyer sees the discount line item.

### Example 2: Optional add-ons toggleable by buyer

**Goal:** Buyer can opt in to SSO + Premium Support; total updates live.
**Steps:**
1. Recipe 2 — section 1 (required), section 2 (multichoice optional).
2. Buyer toggles in PandaDoc viewer; final total recomputes.
3. Webhook on signature → push toggled state to CRM as opportunity update.

**Result:** Self-serve add-on selection inside the doc.

### Example 3: Custom-rendered legal MSA with pricing exhibit

**Goal:** Brand-restricted MSA where PandaDoc pricing isn't an option; need pixel-perfect.
**Steps:**
1. Recipe 10 — docxtpl renders Word with loop.
2. LibreOffice headless → PDF.
3. Send to DocuSign (`e-signature-docusign-adobe-sign-pandadoc`).

**Result:** Branded MSA with dynamic pricing exhibit.

## Edge cases / gotchas

- **Floating-point money math.** Always use `Decimal` (Python) or money library (Dinero.js, Money.js). Floats round wrong at scale.
- **Discount stacking.** PandaDoc applies row discount + section discount + doc discount additively — pre-compute the effective rate to avoid surprises.
- **Tax-inclusive vs tax-exclusive jurisdictions.** EU / Australia: usually tax-inclusive; US: tax-exclusive. Set per locale.
- **PandaDoc pricing tables vs free text math.** Free text doesn't compute; pricing tables do. Don't mix.
- **Currency on multi-currency deal.** Set at document level; rows can override per item but UX gets messy.
- **Number formatting differs by locale.** Use `babel.numbers.format_currency` not f-strings.
- **PandaDoc max rows per table.** ~250 rows. For big BOMs, split per section or use CSV-driven mode.
- **Optional items default state.** Default unselected unless `optional_selected=true`. Decide whose tax this is.
- **Webhook contains buyer toggles.** Read `pricing_tables` from webhook payload post-signature to capture what was bought.
- **Per-row description gets truncated in some templates.** Test with longest expected description; redesign if cropping.
- **Discount % vs amount mismatch.** Two integrations using same name "Loyalty" but different types → CFO sees inconsistent numbers. Standardize.
- **Recurring vs one-time fees.** Most proposal platforms model both; CRM systems often don't — map carefully.
- **Quote expiration vs price expiration.** Quote may be valid 30d but underlying Stripe price changed in week 2 — re-render on send.
- **Test in PandaDoc sandbox before production.** Pricing table options changed in 2024 (added multichoice + new discount struct).
- **Avoid hidden total fields.** Buyer should see subtotal + discount + tax + total separately; one rolled-up number invites disputes.
- **Hand off to `legal-counsel` on fee terms.** Net 30 vs Net 60, prepay vs invoice — these are legal terms, not pricing math.

## Sources

- [PandaDoc Pricing Tables API](https://developers.pandadoc.com/reference/document) — `pricing_tables` schema.
- [PandaDoc Pricing Tables Guide](https://support.pandadoc.com/hc/en-us/articles/360011434953-Pricing-tables) — UI feature parity.
- [Proposify Quotes](https://support.proposify.com/en/articles/2611011-quotes) — section + fees API.
- [Qwilr Quote Blocks](https://qwilr.com/features/quote-blocks/) — interactive pricing.
- [WeasyPrint docs](https://doc.courtbouillon.org/weasyprint/) — HTML/CSS → PDF.
- [Jinja2 docs](https://jinja.palletsprojects.com/) — templating.
- [docxtpl](https://docxtpl.readthedocs.io/) — Word templating with loops.
- [Stripe Prices API](https://stripe.com/docs/api/prices) — live price catalog sync.
- [Babel — Currency formatting](https://babel.pocoo.org/en/latest/numbers.html) — locale-aware.
- [Salesforce CPQ Developer](https://developer.salesforce.com/docs/atlas.en-us.cpq_dev_api.meta/cpq_dev_api/) — QuoteLineItem.
- Sister skills: `proposal-automation-pandadoc-proposify-qwilr`, `salesforce-conga-composer`, `hubspot-doc-gen`, `bulk-document-gen-csv`.
